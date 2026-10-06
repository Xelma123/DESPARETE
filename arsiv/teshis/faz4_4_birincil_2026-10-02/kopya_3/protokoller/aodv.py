"""
AODV — RFC 3561'e sadık gerçekleme (`AODV-i`: kara liste K-194 · sıra
numarası kuralları §6.2/§6.7/§6.11, K-205 · sadakat denetimi H1–H11, K-208 ·
(ii)'nin RERR'i öncül süzmesiz, K-210 ·
`arsiv/teshis/aodv_sadakat_2026-09-30/denetim.md`).

🔒 KÂHİN ERİŞİMİ YOK
====================
Bu modül yalnız `sim2/gozlem/`i içe aktarır. Konum, topoloji, `Konfig`, kanal,
karıştırıcı — hiçbiri görünmez; içe aktarma grafiği testi bunu bağlar. Bildiği
her şey ya aldığı bir mesajdan ya kendi donanımının ölçtüğünden gelir
(`v2/05` §2).

🔒 PARAMETRELER RFC VARSAYILANIDIR, SEÇİLMEDİ
=============================================
Hepsi `aodv_bicim.py`de ve hepsi RFC 3561 §10'un bastığı değer. `06` §4.4'ün
sadakat protokolü: *"hiçbir parametre senaryoya göre değiştirilmez"*. Bu
dosyada ayarlanabilir tek bir sayı yoktur.

🔴 KENDİ HELLO'SUNU GÖNDERİR — ve bu bir STRAW-MAN'İ KAPATIR
============================================================
`kosum_beaconi = False`: koşum düzeyindeki 1 s'lik beacon bu protokolde hiç
çizelgelenmez, komşuluk AODV'nin kendi HELLO'sundan kurulur (`13` §03.8).

`02` §R3 bunu bir straw-man RİSKİ olarak kaydetmişti: koşum beacon'ı 1 s ve o
tam olarak AODV'nin `HELLO_INTERVAL`ı, ama OLSR'ın RFC'si 2 s diyor — yani
ortak beacon OLSR'ı kendi RFC'sinin İKİ KATI hızda koşturuyor ve kontrol
yükünü şişiriyordu. Her protokol kendi HELLO'sunu kendi RFC hızında
gönderince o asimetri **yapısal olarak** kapanır: AODV 1 s öder, OLSR 2 s.

⚠️ Bedeli açık: komşu tablosu artık `gozlem.komsular`dan GELMEZ (o liste boş
kalır ve satırda beyan edilir). AODV komşularını `kontrol_alindi`den kendisi
kurar — RFC'nin zaten söylediği şey.

🔴 ROTA BEKLERKEN PAKET DÜŞMEZ
==============================
RFC 3561 §6.3 rota keşfi sırasında paketlerin tamponlanmasını ŞART koşar.
`Karar(beklet=True)` tam bunu yapar (K-131); tamponun iki tavanı da
simülatörde (ns-3 değerleri, K-198) ve satırda beyanlı.

🔒 ÜÇ ZAMANLAYICI, HEPSİ RFC'DEN
=================================
    hello   1,0 s   — §6.9, `HELLO_INTERVAL`
    bakim   1,0 s   — rota ömrü ve komşu ömrü süpürmesi; ızgara `HELLO`nunki
                      (RFC ayrı bir periyot tanımlamıyor, süpürme bir
                      GERÇEKLEME ayrıntısıdır ve en hızlı olayla hizalandı)

Keşif zaman aşımları periyodik DEĞİL, `Uyandirma` ile isteğe bağlıdır
(§6.3'ün `RING_TRAVERSAL_TIME`ı); periyodik bir süpürmeye bağlansalardı
zamanlama ızgaraya yuvarlanır ve RFC'nin ölçüsü bozulurdu.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from sim2.gozlem.karar import Beyan, Karar
from sim2.gozlem.kontrol import KontrolIstegi, Uyandirma
from sim2.gozlem.pencere import Gozlem
from protokoller.aodv_bicim import (
    ACTIVE_ROUTE_TIMEOUT_S, ALLOWED_HELLO_LOSS, BLACKLIST_TIMEOUT_S,
    DELETE_PERIOD_S,
    HELLO_INTERVAL_S, MY_ROUTE_TIMEOUT_S, NET_DIAMETER, NET_TRAVERSAL_TIME_S,
    NODE_TRAVERSAL_TIME_S,
    PATH_DISCOVERY_TIME_S, RERR, RERR_RATELIMIT, RREP, RREQ, RREQ_RATELIMIT,
    RREQ_RETRIES, SONSUZ_SIRA, TIP_RERR, TIP_RREP, TIP_RREQ, TTL_INCREMENT,
    TTL_START, TTL_THRESHOLD, halka_suresi_s)

__all__ = ["AODV", "Rota"]

# 32 bitlik alanların taşmaması için sıra numarası ve RREQ kimliği burada
# sarmalanır. RFC §6.1 sıra numaralarını işaretli 32 bit sayar ve sarma
# karşılaştırmasını tarif eder; bu koşularda sayılar binleri geçmiyor, yani
# sarma hiç tetiklenmiyor — ama alan genişliğini aşan bir değer `KontrolIstegi`
# tarafından REDDEDİLİR ve koşu durur, o yüzden sınır burada tutuluyor.
_ALAN_32 = (1 << 32) - 1


@dataclass(slots=True)
class Rota:
    """RFC 3561 §6.2 · rota tablosu girdisi.

    🔒 `gecerli=False` bir girdiyi SİLMEZ. RFC §6.11: geçersiz bir girdi
    `DELETE_PERIOD` boyunca tutulur, çünkü taşıdığı SIRA NUMARASI hâlâ
    değerlidir — silinirse düğüm bayat bir rotayı taze sanıp geri kabul eder.
    """

    sonraki: int
    atlama: int
    hedef_sira: int
    gecerli: bool = True
    son_gecerli_s: float = 0.0          # ömrün bittiği AN (yerel saat)
    silme_s: float = 0.0                # geçersizken silinme anı
    oncular: set[int] = field(default_factory=set)


@dataclass(slots=True)
class _Kesif:
    """Süren bir rota keşfi — §6.3."""

    deneme: int
    ttl: int
    baslangic_s: float
    # 🔒 Zamanlayıcı İPTAL EDİLEMEZ; biten bir keşfin eski zaman aşımı aynı
    # hedefin YENİ keşfini erken ilerletmesin diye etiket nesli taşır
    # (ns-3 zamanlayıcıyı iptal eder, K-208 H11).
    nesil: int = 0


class AODV:
    """Ad hoc On-Demand Distance Vector — RFC 3561."""

    ad = "aodv"
    # 🔒 `13` §03.8 — kendi HELLO'sunu gönderir, koşum beacon'ını kapatır.
    kosum_beaconi = False

    __slots__ = ("kimlik", "_sira", "_rreq_kimlik", "_rota", "_komsu",
                 "_gorulen_rreq", "_kesif", "_son_yayin_s", "_rreq_pencere",
                 "_rerr_pencere", "_sayac", "_kopuk", "_bekleyen_beyan",
                 "_kara_liste", "_kesif_nesli")

    def __init__(self, kimlik: int) -> None:
        self.kimlik = kimlik
        # RFC §6.1 — kendi sıra numarası; 1'den başlar (0 "bilinmiyor" demek).
        self._sira = 1
        self._rreq_kimlik = 0
        self._rota: dict[int, Rota] = {}
        # Komşu → son HELLO'nun duyulduğu an. `gozlem.komsular` BOŞ kalır.
        self._komsu: dict[int, float] = {}
        # (kaynak, rreq_kimlik) → görülme anı. §6.5 tekrar bastırma.
        self._gorulen_rreq: dict[tuple[int, int], float] = {}
        self._kesif: dict[int, _Kesif] = {}
        self._kesif_nesli = 0
        # §6.9 — HELLO yalnız son aralıkta BAŞKA bir yayın yapılmadıysa.
        self._son_yayin_s = -math.inf
        # §10 hız sınırları: (pencere başı, o pencerede gönderilen).
        self._rreq_pencere: list[float] = [-math.inf, 0.0]
        self._rerr_pencere: list[float] = [-math.inf, 0.0]
        # 🔒 ÖLÇÜM DURUMU — karara GİRMEZ (19 Eylül 2026, `04` K-139).
        # Kopan komşu → o bağ koptuğunda onun üzerinden geçen hedefler.
        # Bu hedeflerden birine rota yeniden kurulunca `rota_kuruldu(komşu)`
        # beyan edilir ve defter Δ'yı kapatır.
        self._kopuk: dict[int, set[int]] = {}
        # Rota kuran yardımcılar kanca değil; beyanlarını burada biriktirir,
        # `kontrol_alindi` boşaltır.
        self._bekleyen_beyan: list = []
        # 🔒 §6.8 KARA LİSTE (K-194): RREP'i bağ katmanında onaylanmayan
        # komşu → listeden çıkış anı. Listedeki komşunun RREQ'leri YOK
        # SAYILIR — tek yönlü bir bağ üzerinden gelen ilk RREQ, çift yönlü
        # bir yoldan gelecek sonrakini bastırmasın diye.
        self._kara_liste: dict[int, float] = {}
        self._sayac: dict[str, int] = {
            "rreq_uretilen": 0, "rreq_iletilen": 0, "rreq_bastirilan": 0,
            "rrep_uretilen": 0, "rrep_iletilen": 0, "rerr_uretilen": 0,
            "kesif_basarili": 0, "kesif_basarisiz": 0,
            "komsu_zaman_asimi": 0, "rota_gecersizlestirilen": 0,
            "hiz_siniri_engelledi": 0, "rerr_onculsuz": 0,
            "kara_liste_eklenen": 0, "rreq_kara_listeden": 0,
            "rreq_ertelenen": 0,
        }

    # ==================================================================
    # YARDIMCILAR
    # ==================================================================
    def _taze_mi(self, r: Rota, simdi_s: float) -> bool:
        return r.gecerli and r.son_gecerli_s > simdi_s

    def _rota_al(self, hedef: int, simdi_s: float) -> Rota | None:
        r = self._rota.get(hedef)
        return r if r is not None and self._taze_mi(r, simdi_s) else None

    def _sira_artir(self) -> None:
        self._sira = (self._sira + 1) & _ALAN_32

    def _hiz_sinirli_mi(self, pencere: list[float], sinir: int,
                        simdi_s: float) -> bool:
        """RFC §10 · `RREQ_RATELIMIT` ve `RERR_RATELIMIT` — saniyede en çok n.

        🔒 Kayan değil SABİT bir saniye penceresi: RFC *"per second"* diyor ve
        kayan pencere düğüm başına bir zaman damgası listesi gerektirirdi.
        Fark, sınırın tam kenarındaki bir yayının bir sonraki saniyeye
        kaymasıdır; sayılıyor (`hiz_siniri_engelledi`) ve beyan ediliyor.
        """
        if simdi_s - pencere[0] >= 1.0:
            pencere[0] = simdi_s
            pencere[1] = 0.0
        if pencere[1] >= sinir:
            self._sayac["hiz_siniri_engelledi"] += 1
            return True
        pencere[1] += 1.0
        return False

    def _rreq_kur(self, hedef: int, ttl: int, simdi_s: float) -> KontrolIstegi:
        """§6.3 · RREQ üretimi — kendi sırası artar, RREQ kimliği artar."""
        self._rreq_kimlik = (self._rreq_kimlik + 1) & _ALAN_32
        self._sira_artir()
        bilinen = self._rota.get(hedef)
        hedef_sira = bilinen.hedef_sira if bilinen else SONSUZ_SIRA
        self._gorulen_rreq[(self.kimlik, self._rreq_kimlik)] = simdi_s
        self._son_yayin_s = simdi_s
        self._sayac["rreq_uretilen"] += 1
        return KontrolIstegi.kur(None, RREQ, {
            "tip": TIP_RREQ,
            "bayraklar": 1 if hedef_sira == SONSUZ_SIRA else 0,   # U bayrağı
            "ayrilmis": 0,
            "atlama": 0,
            "rreq_kimlik": self._rreq_kimlik,
            "hedef": hedef,
            "hedef_sira": hedef_sira,
            "kaynak": self.kimlik,
            "kaynak_sira": self._sira,
            "ttl": ttl,
        })

    def _rrep_kur(self, hedef_adres: int, hedef_sira: int, atlama: int,
                  kaynak: int, omur_s: float,
                  sonraki: int | None) -> KontrolIstegi:
        """§5.2 · RREP. `sonraki=None` ise YAYIN (HELLO, §6.9)."""
        return KontrolIstegi.kur(sonraki, RREP, {
            "tip": TIP_RREP,
            "bayraklar": 0,
            "ayrilmis": 0,
            "onek_boyu": 0,
            "atlama": atlama,
            "hedef": hedef_adres,
            "hedef_sira": hedef_sira,
            "kaynak": kaynak,
            "omur_ms": int(omur_s * 1000.0),
        })

    # ==================================================================
    # KANCA · sonraki_atlama
    # ==================================================================
    def sonraki_atlama(self, gozlem: Gozlem) -> Karar:
        """Rota varsa gönder; yoksa BEKLET ve keşfi başlat (§6.3 · §6.11)."""
        if gozlem.paket is None:
            return Karar()
        simdi = float(gozlem.saat_s)
        hedef = gozlem.paket.hedef
        r = self._rota_al(hedef, simdi)
        if r is not None and r.sonraki in self._komsu:
            # §6.2 — kullanılan rotanın ömrü tazelenir.
            r.son_gecerli_s = max(r.son_gecerli_s,
                                  simdi + ACTIVE_ROUTE_TIMEOUT_S)
            # 🔴 RFC 3561 §6.9, BİRİNCİL BELGEDEN (17 Eylül 2026):
            #   "...for that neighbor does not receive any packets (Hello
            #    messages or otherwise) for more than ALLOWED_HELLO_LOSS *
            #    HELLO_INTERVAL milliseconds, the node SHOULD assume that
            #    the link to this neighbor is currently lost."
            # 🔒 "ANY PACKETS — OR OTHERWISE". İlk yazımda komşuluğu YALNIZ
            # kontrol mesajları tazeliyordu (`kontrol_alindi`) ve bu, veri
            # taşıyan bir bağı HELLO'su çakıştığı an ölü ilan ediyordu.
            # Bedeli ÖLÇÜLDÜ — `statik-yok/1002`, topolojinin hiç
            # değişmediği bir koşuda:
            #     komsu_zaman_asimi 7 671 · rerr_uretilen 11 961
            #     rreq_bastirilan 96 992 · iletim_basarisiz 1 450
            # Statik bir ağda tek bir komşunun bile kaybolmaması gerekirdi.
            # Doğan şey bir GERİ BESLEMEYDİ: sahte kopma → RERR → yeniden
            # keşif → RREQ seli → daha çok çarpışma → daha çok sahte kopma.
            # 🔒 Paketi X'e devretmek bir TEMAS kanıtıdır: MAC ya onaylar
            # (yani X'ten bir çerçeve gelir — §6.9'un saydığı şey) ya da
            # vazgeçer, ve vazgeçerse `iletim_basarisiz` komşuyu ZATEN aynı
            # anda düşürür. Yani bu tazeleme ölü bir bağı ayakta tutamaz.
            self._komsu[r.sonraki] = simdi
            # 🔴 RFC 3561 §6.2, BİRİNCİL BELGEDEN (17 Eylül 2026):
            #   "Each time a route is used to forward a data packet, its
            #    Active Route Lifetime field of the SOURCE, destination and
            #    the next hop on the path to the destination is updated to
            #    be no less than the current time plus ACTIVE_ROUTE_TIMEOUT."
            # 🔒 Hedefin ömrü yukarıda tazelendi; sonraki atlamanın ve
            # KAYNAĞIN ömrü de tazelenmeli. Kaynağa giden girdi RREQ'in ters
            # rotasıdır ve RERR ile RREP onun üzerinden döner — süresi
            # dolarsa kopma haberi kaynağa ULAŞAMAZ.
            for komsu_hedef in (r.sonraki, gozlem.paket.kaynak):
                rk = self._rota.get(komsu_hedef)
                if rk is not None and rk.gecerli:
                    rk.son_gecerli_s = max(rk.son_gecerli_s,
                                           simdi + ACTIVE_ROUTE_TIMEOUT_S)
            return Karar(sonraki=r.sonraki)

        eski = self._rota.get(hedef)
        if eski is not None and not eski.gecerli:
            # §6.11: *"If a data packet is received for an invalid route, the
            # Lifetime field is updated to current time plus DELETE_PERIOD."*
            eski.silme_s = simdi + DELETE_PERIOD_S
        if gozlem.paket.kaynak != self.kimlik:
            # 🔒 §6.11 (ii) — ARA DÜĞÜMÜN ETKİN ROTASI YOK: RERR (öncülü
            # varsa) ve paket DÜŞER; keşif kaynağın işidir. Düşme sebebi
            # rota VARDIYSA `rota_gecersiz` (K-134), hiç yoksa `hedef_yok`.
            # 🔴 K-208 H8: süresi dolmuş (ya da sonraki atlaması artık komşu
            # olmayan) geçerli girdide ve girdisiz hedefte ara düğüm paketi
            # tamponlayıp KENDİSİ keşif başlatıyordu — RFC'de yok.
            # 🔴 K-210: (ii)'nin RERR'i ÖNCÜL LİSTESİNE BAKMADAN gider. RFC'nin
            # süzme cümlesi küçük harf ("The RERR should contain … non-empty
            # precursor list") — normatif değil; ns-2 ve ns-3 bu durumda süzmez.
            # Süzülünce, ters yoldan öğrenilmiş rotayla gönderen (öncül değil)
            # hiç haber almıyor ve akış kara deliğe düşüyordu (AOMDV, eşler
            # arası statik 1001: 1 225 paket). (i)'nin süzmesi (K-143) kalır.
            if eski is None:
                return Karar(sonraki=None, niyetler=self._rerr_kur(
                    (hedef,), simdi, oncul_suz=False))
            if eski.gecerli:
                self._gecersizlestir(eski, simdi)       # (ii): sıra artar
            niyet = self._rerr_kur((hedef,), simdi, oncul_suz=False)
            return Karar(sonraki=None,
                         beyan=(Beyan("rota_gecersiz", komsu=hedef),),
                         niyetler=niyet)

        # 🔒 KAYNAK: rota yok → paket TAMPONA, keşif başlar (§6.3).
        niyetler: tuple = ()
        if hedef not in self._kesif:
            niyetler = self._kesif_baslat(hedef, simdi)
        return Karar(beklet=True, niyetler=niyetler)

    def _son_atlama(self, r) -> int | None:
        """Girdinin son bilinen atlama sayısı (§6.4); AOMDV'de yolu kalmayan
        geçersiz girdi bunu bilmez."""
        return r.atlama

    def _kesif_baslat(self, hedef: int, simdi_s: float) -> tuple:
        """§6.3 + §6.4 · genişleyen halka araması ile RREQ.

        🔒 §6.4 (K-208 H7): geçersiz bir girdi varsa ilk TTL *"the Hop Count
        plus TTL_INCREMENT"* (ns-3 `SendRequest` ile aynı); yoksa `TTL_START`.
        """
        bilinen = self._rota.get(hedef)
        atlama = None if bilinen is None else self._son_atlama(bilinen)
        ttl = (TTL_START if atlama is None
               else min(atlama + TTL_INCREMENT, NET_DIAMETER))
        self._kesif_nesli += 1
        self._kesif[hedef] = _Kesif(deneme=1 if ttl >= NET_DIAMETER else 0,
                                    ttl=ttl, baslangic_s=simdi_s,
                                    nesil=self._kesif_nesli)
        return self._kesif_gonder(hedef, simdi_s)

    def _kesif_gonder(self, hedef: int, simdi_s: float) -> tuple:
        """Süren keşfin RREQ'ini gönderir ve zaman aşımını kurar.

        🔒 §10 `RREQ_RATELIMIT` aşılırsa RREQ ERTELENİR (ns-3 `SendRequest`:
        pencere dolunca yeniden dener). 🔴 K-208 H10: ilk yazımda ilk keşif
        bırakılıyor, yeniden denemede ise zamanlayıcı kurulmadan dönülüyordu;
        keşif kaydı silinmediği için o hedefe bir daha keşif başlamıyordu.
        🔒 Bekleme §6.3–§6.4: halkada `RING_TRAVERSAL_TIME`; ağ çapında
        `NET_TRAVERSAL_TIME`, her ek denemede iki katı (ilk bekleme tek kat —
        K-208 H11, ns-3 ile aynı; ilk yazım iki katından başlıyordu).
        """
        k = self._kesif[hedef]
        if self._hiz_sinirli_mi(self._rreq_pencere, RREQ_RATELIMIT, simdi_s):
            self._sayac["rreq_ertelenen"] += 1
            kalan = max(self._rreq_pencere[0] + 1.0 - simdi_s, 0.0)
            return (Uyandirma(kalan + 1e-4, f"kesif_ertele:{hedef}:{k.nesil}"),)
        bekleme = (NET_TRAVERSAL_TIME_S * (2 ** (k.deneme - 1))
                   if k.ttl >= NET_DIAMETER else halka_suresi_s(k.ttl))
        return (self._rreq_kur(hedef, k.ttl, simdi_s),
                Uyandirma(bekleme, f"kesif:{hedef}:{k.nesil}"))

    def _rerr_kur(self, hedefler: tuple[int, ...], simdi_s: float,
                  oncul_suz: bool = True) -> tuple:
        """§6.11 · RERR — ulaşılamaz hedefler ve sıra numaraları.

        🔴 RFC 3561 §6.11, BİRİNCİL BELGEDEN (19 Eylül 2026, `04` K-143):
          *"The RERR should contain those destinations that are part of the
           created list of unreachable destinations and have a non-empty
           precursor list."*
        Öncülü olmayan bir hedef için RERR GÖNDERİLMEZ: kimse o hedefe bu
        düğüm üzerinden gitmiyorsa kopmayı duyurmanın alıcısı yoktur. İlk
        yazımda etkilenen rota varsa her zaman yayın yapılıyordu; öncül
        listeleri tutuluyordu ama KULLANILMIYORDU. Statik ağda bile keşif
        susmuyordu (U3 oranı 1,854): boştaki bir komşunun zaman aşımı
        gereksiz bir RERR yayıyor, onu duyan komşular rotalarını
        geçersizleştiriyor, yeniden keşif başlıyordu.
        🔒 Süzme hız sınırından ÖNCE: öncülsüz bir aday, `RERR_RATELIMIT`
        penceresinden boşuna bir hak tüketmemeli.
        """
        onculu = (tuple(h for h in hedefler
                        if h in self._rota and self._rota[h].oncular)
                  if oncul_suz else tuple(hedefler))
        self._sayac["rerr_onculsuz"] += len(hedefler) - len(onculu)
        hedefler = onculu
        if not hedefler or self._hiz_sinirli_mi(self._rerr_pencere,
                                                RERR_RATELIMIT, simdi_s):
            return ()
        siralar = tuple(self._rota[h].hedef_sira if h in self._rota
                        else SONSUZ_SIRA for h in hedefler)
        self._sayac["rerr_uretilen"] += 1
        self._son_yayin_s = simdi_s
        # 🔒 YAYIN olarak gönderiliyor. RFC §6.11 öncü sayısı birden çoksa
        # yayını, bir tekse unicast'i söyler. Öncü listesi bu gerçeklemede
        # tutuluyor ama RERR HER ZAMAN yayın: unicast dalı, öncüsü tek olan
        # ender bir durumda bir çerçeve kazandırırdı ve iki kod yolu doğururdu.
        # ⚠️ Yönü AODV'yi olduğundan PAHALI gösterir; sapma listesinde.
        return (KontrolIstegi.kur(None, RERR, {
            "tip": TIP_RERR,
            "bayraklar": 0,
            "ayrilmis": 0,
            "hedef_sayisi": len(hedefler),
            "ulasilamaz": hedefler,
            "ulasilamaz_sira": siralar,
        }),)

    # ==================================================================
    # KANCA · beacon (koşum beacon'ı KAPALI — bu kancalar boş)
    # ==================================================================
    def beacon_yuku(self, gozlem: Gozlem) -> dict:
        return {}

    def beacon_alindi(self, gozlem: Gozlem, komsu: int, yuk) -> None:
        return None

    # ==================================================================
    # KANCA · zamanlayıcılar
    # ==================================================================
    def zamanlayicilar(self) -> dict:
        return {"hello": HELLO_INTERVAL_S, "bakim": HELLO_INTERVAL_S}

    def zamanlayici_doldu(self, gozlem: Gozlem, etiket: str) -> tuple:
        simdi = float(gozlem.saat_s)
        if etiket == "hello":
            return self._hello(simdi)
        return self._bakim(simdi)

    def _hello(self, simdi_s: float) -> tuple:
        """§6.9 · HELLO = TTL 1 olan, hedefi kendisi olan bir RREP.

        🔒 RFC: *"yalnız son `HELLO_INTERVAL` içinde BAŞKA bir yayın
        göndermediyse"*. Bu koşul gerçek bir tasarruftur — RREQ yayını zaten
        komşulara varlığını duyurur — ve uygulanmazsa AODV'nin kontrol yükü
        olduğundan yüksek ölçülürdü.
        """
        if simdi_s - self._son_yayin_s < HELLO_INTERVAL_S:
            return ()
        self._son_yayin_s = simdi_s
        return (self._rrep_kur(
            hedef_adres=self.kimlik, hedef_sira=self._sira, atlama=0,
            kaynak=self.kimlik,
            omur_s=ALLOWED_HELLO_LOSS * HELLO_INTERVAL_S, sonraki=None),)

    def _bakim(self, simdi_s: float) -> tuple:
        """Komşu ömrü ve rota ömrü süpürmesi (§6.2 · §6.9 · §6.11)."""
        niyetler: list = []
        omur = ALLOWED_HELLO_LOSS * HELLO_INTERVAL_S
        kayip = [n for n, t in self._komsu.items() if simdi_s - t > omur]
        for n in kayip:
            del self._komsu[n]
            self._sayac["komsu_zaman_asimi"] += 1
            niyetler.extend(self._bag_koptu(n, simdi_s))
        # §6.11 — süresi dolan geçerli rotalar geçersizleşir; `DELETE_PERIOD`
        # dolunca girdi silinir (sıra numarası o ana kadar korunur).
        # 🔒 K-208 H9: ömür dolması RERR durumu DEĞİLDİR (§6.11 madde 1 sırayı
        # yalnız (i)–(iii)'te değiştirir; ns-3 `Purge` de dokunmaz). İlk yazımda
        # burada da artıyordu: yerel sıra hedefin gerçek sırasını geçebiliyordu.
        for hedef, r in list(self._rota.items()):
            if r.gecerli and r.son_gecerli_s <= simdi_s:
                self._gecersizlestir(r, simdi_s, suresi_doldu=True)
            elif not r.gecerli and r.silme_s <= simdi_s:
                del self._rota[hedef]
        # §6.5 — tekrar bastırma kayıtları `PATH_DISCOVERY_TIME` yaşar.
        for anahtar, t in list(self._gorulen_rreq.items()):
            if simdi_s - t > PATH_DISCOVERY_TIME_S:
                del self._gorulen_rreq[anahtar]
        return tuple(niyetler)

    def _gecersizlestir(self, r: Rota, simdi_s: float,
                        rerr_sira: int | None = None,
                        suresi_doldu: bool = False) -> None:
        """§6.11 · geçersizleştirme — girdi SİLİNMEZ.

        🔒 Madde 1: sıra numarası, *"if it exists and is valid"*, yerel
        kopmada bir ARTAR, RERR ile öğrenilen kopmada RERR'den KOPYALANIR.
        Bilinmeyen sıra (`SONSUZ_SIRA`, komşu rotası §6.2) bilinmeyen kalır:
        artırılsaydı hedefin hiç söylemediği bir sıra uydurulurdu (K-205).
        """
        r.gecerli = False
        if r.hedef_sira != SONSUZ_SIRA and not suresi_doldu:
            if rerr_sira is None:
                r.hedef_sira = (r.hedef_sira + 1) & _ALAN_32
            elif rerr_sira != SONSUZ_SIRA:
                r.hedef_sira = rerr_sira
        r.silme_s = simdi_s + DELETE_PERIOD_S
        self._sayac["rota_gecersizlestirilen"] += 1

    def _bag_koptu(self, komsu: int, simdi_s: float) -> tuple:
        """Bir komşu kayboldu: onu sonraki atlama yapan rotalar düşer.

        🔒 BEYAN BURADAN GELİYOR ve bu K-134'ün sebebidir: kopma burada
        öğrenilir, veri gönderme kararında değil. Kanalın açılmasından önce
        kuyruğu boş bir düğüm bunu hiç bildiremezdi.
        """
        etkilenen = tuple(h for h, r in self._rota.items()
                          if r.sonraki == komsu and r.gecerli)
        for h in etkilenen:
            self._gecersizlestir(self._rota[h], simdi_s)
        # 🔴 KOPMA YALNIZ ETKİN ROTA TAŞIYAN BİR BAĞDA BEYAN EDİLİR (K-139).
        # RFC 3561 §6.11 bağ kopmasını *"etkin bir rotanın sonraki
        # atlaması"* için tanımlar. Önceden her komşu kaybı beyan ediliyordu —
        # §6.9'un HELLO bastırması yüzünden boştaki komşuların tablodan düşmesi
        # dâhil. Ölçüldü: `statik-yok`ta, topoloji hiç değişmezken, 50 s'de
        # **1 082** kopma; `bagimsiz-yok`ta algılama duyarlılığı **430**.
        # Davranış değişmedi: RERR zaten yalnız `etkilenen` doluysa gidiyordu.
        if not etkilenen:
            return ()
        self._kopuk.setdefault(komsu, set()).update(etkilenen)
        beyanlar: tuple = (Beyan("kopma", komsu=komsu),)
        return beyanlar + self._rerr_kur(etkilenen, simdi_s)

    def _kurtarma(self, hedef: int) -> None:
        """Bir hedefe rota GEÇERLİ olarak kuruldu — bekleyen bir kopmayı kapatır mı?

        🔒 Δ'nın anahtarı `(düğüm, KOPAN KOMŞU)`dur, rotanın hedefi değil:
        `olcum/rota_olaylari.py` `rota_etkilendi`yi *"kopma beyan edilen ayrı
        BAĞ sayısı"* diye tanımlıyor ve `algilama_duyarliligi` paydasını
        fiziksel BAĞ kopmalarından alıyor. İlk kurtarılan hedef Δ'yı kapatır —
        defter zaten yalnız ilk `rota_kuruldu`yu sayıyor.
        """
        for komsu in [k for k, h in self._kopuk.items() if hedef in h]:
            del self._kopuk[komsu]
            self._bekleyen_beyan.append(Beyan("rota_kuruldu", komsu=komsu))

    def _beyan_bosalt(self) -> tuple:
        cikti = tuple(self._bekleyen_beyan)
        self._bekleyen_beyan.clear()
        return cikti

    # ==================================================================
    # KANCA · uyandı (keşif zaman aşımları)
    # ==================================================================
    def uyandi(self, gozlem: Gozlem, etiket: str) -> tuple:
        # 🔒 "tampon" etiketi bir İŞ YAPMAZ: tek amacı simülatörün bekleyen
        # paketleri yeniden sormasıdır (`kosum/kontrol.py`, K-135). Protokol
        # burada hiçbir şey döndürmez.
        tur, _, geri = etiket.partition(":")
        if tur not in ("kesif", "kesif_ertele"):
            return ()
        hedef_s, _, nesil_s = geri.partition(":")
        hedef = int(hedef_s)
        k = self._kesif.get(hedef)
        simdi = float(gozlem.saat_s)
        if k is None or (nesil_s and int(nesil_s) != k.nesil):
            return ()                  # keşif bitmiş ya da bu eski bir nesil
        if self._rota_al(hedef, simdi) is not None:
            del self._kesif[hedef]
            return ()
        if tur == "kesif_ertele":
            return self._kesif_gonder(hedef, simdi)   # aynı adımı yeniden dene
        # §6.4 — genişleyen halka: TTL eşiği aşınca NET_DIAMETER'a atla.
        if k.ttl < TTL_THRESHOLD:
            k.ttl = min(k.ttl + TTL_INCREMENT, TTL_THRESHOLD)
        else:
            k.ttl = NET_DIAMETER
            k.deneme += 1
        if k.deneme > RREQ_RETRIES:
            del self._kesif[hedef]
            self._sayac["kesif_basarisiz"] += 1
            # 🔒 Tamponlanan paketleri DÜŞÜRMEK simülatörün işi: tamponun
            # süre tavanı onları zaten alacak. Protokol burada yalnız keşfi
            # bırakır — RFC de *"the application is notified"* der, paketleri
            # protokolün kendisi silmez.
            return ()
        return self._kesif_gonder(hedef, simdi)

    # ==================================================================
    # KANCA · kontrol mesajı alındı
    # ==================================================================
    def kontrol_alindi(self, gozlem: Gozlem, gonderen: int, bicim: str,
                       yuk, yayin: bool) -> tuple:
        simdi = float(gozlem.saat_s)
        y = dict(yuk)
        # 🔒 §6.8 (K-194): *"A node ignores all RREQs received from any node
        # in its blacklist set."* Yok sayılan RREQ alınmamış gibidir — komşu
        # kanıtı, ters rota ve iletme de doğmaz (o bağın bu yönü çalışmıyor).
        if bicim == "RREQ" and self._kara_listede(gonderen, simdi):
            self._sayac["rreq_kara_listeden"] += 1
            return self._beyan_bosalt()
        # 🔒 Her alınan kontrol mesajı komşuluğun KANITIDIR (§6.9): mesaj
        # geldiyse bağ o an çalışıyordu. Komşu tablosu buradan dolar —
        # `gozlem.komsular` boştur, çünkü koşum beacon'ı kapalı.
        self._komsu[gonderen] = simdi
        self._komsu_rotasi(gonderen, simdi)
        if bicim == "RREQ":
            niyet = self._rreq_isle(gonderen, y, simdi)
        elif bicim == "RREP":
            niyet = self._rrep_isle(gonderen, y, simdi)
        else:
            niyet = self._rerr_isle(gonderen, y, simdi)
        # 🔒 Rota kuran üç yardımcının biriktirdiği kurtarma beyanları.
        # Üçü de YALNIZ bu kancadan erişiliyor, dolayısıyla tek boşaltma
        # noktası burası. Beyanlar sona eklenir: niyetlerin sırası (ve
        # dolayısıyla titreşim çekimlerinin sırası) değişmez.
        return niyet + self._beyan_bosalt()

    def _komsu_rotasi(self, komsu: int, simdi_s: float) -> None:
        """Bir atlamalık rota — §6.2, `ACTIVE_ROUTE_TIMEOUT` ömürlü.

        🔒 §6.2 · §6.5 · §6.7: önceki atlamaya rota *"without a valid
        sequence number"* kurulur (ns-3 `UpdateRouteToNeighbor`: vSeqNo
        false, seqNo 0). Eski sıra taşınsaydı, yerelde artırılmış bir sıra
        (§6.11) hedefin gerçek sırasını geçer ve hedefin kendi RREP'i
        §6.7'de bayat sayılırdı (AOMDV'de 22 Eylül'de ölçülen tuzak, K-205).
        """
        r = self._rota.get(komsu)
        if r is None or not r.gecerli or r.atlama > 1:
            self._rota[komsu] = Rota(
                sonraki=komsu, atlama=1, hedef_sira=SONSUZ_SIRA,
                son_gecerli_s=simdi_s + ACTIVE_ROUTE_TIMEOUT_S,
                oncular=(r.oncular if r else set()))
            self._kurtarma(komsu)
        else:
            r.son_gecerli_s = max(r.son_gecerli_s,
                                  simdi_s + ACTIVE_ROUTE_TIMEOUT_S)

    def _ters_rota(self, kaynak: int, kaynak_sira: int, atlama: int,
                   sonraki: int, simdi_s: float) -> None:
        """§6.5 · RREQ'in kaynağına doğru TERS rota — oluşturulur ya da
        güncellenir (tekrar olmayan her RREQ'te; ns-3 `RecvRequest` ile aynı).

        🔒 (1) sıra *"copied if greater than the existing value"* · (2) sıra
        geçerli · (3) sonraki atlama gönderen · (4) atlama RREQ'ten · (5) ömür
        `max(mevcut, şimdi + 2·NET_TRAVERSAL_TIME − 2·atlama·NODE_TRAVERSAL_TIME)`.
        🔴 K-208 H2: ilk yazımda güncelleme koşullu, ömür tabanı RFC'de olmayan
        `ACTIVE_ROUTE_TIMEOUT`tu ve mevcut ömür kısalabiliyordu.
        """
        r = self._rota.get(kaynak)
        sira = (kaynak_sira if r is None or r.hedef_sira == SONSUZ_SIRA
                else max(r.hedef_sira, kaynak_sira))
        omur = (simdi_s + 2 * NET_TRAVERSAL_TIME_S
                - 2 * atlama * NODE_TRAVERSAL_TIME_S)
        if r is not None and r.gecerli:
            omur = max(omur, r.son_gecerli_s)
        self._rota[kaynak] = Rota(
            sonraki=sonraki, atlama=atlama, hedef_sira=sira,
            son_gecerli_s=omur, oncular=(r.oncular if r else set()))
        self._kurtarma(kaynak)

    def _rreq_isle(self, gonderen: int, y: dict, simdi_s: float) -> tuple:
        """§6.5 · RREQ işleme."""
        # 🔒 K-208 H1 · §6.5 ilk cümle: önceki atlamaya rota *"without a valid
        # sequence number"* (ns-3 `RecvRequest`: `toNeighbor.SetValidSeqNo
        # (false)`). Rota `kontrol_alindi`de kuruldu; burada sırası düşer.
        onceki = self._rota.get(gonderen)
        if onceki is not None and onceki.atlama == 1 \
                and onceki.sonraki == gonderen:
            onceki.hedef_sira = SONSUZ_SIRA
        kaynak, kimlik = y["kaynak"], y["rreq_kimlik"]
        if (kaynak, kimlik) in self._gorulen_rreq:
            self._sayac["rreq_bastirilan"] += 1
            return ()
        self._gorulen_rreq[(kaynak, kimlik)] = simdi_s
        atlama = y["atlama"] + 1
        self._ters_rota(kaynak, y["kaynak_sira"], atlama, gonderen, simdi_s)

        hedef = y["hedef"]
        if hedef == self.kimlik:
            # §6.6.1 — hedefin kendisi RREP üretir.
            if y["hedef_sira"] == self._sira + 1:
                self._sira_artir()
            self._sayac["rrep_uretilen"] += 1
            return (self._rrep_kur(
                hedef_adres=self.kimlik, hedef_sira=self._sira, atlama=0,
                kaynak=kaynak, omur_s=MY_ROUTE_TIMEOUT_S,
                sonraki=gonderen),)

        r = self._rota_al(hedef, simdi_s)
        bilinmiyor = y["hedef_sira"] == SONSUZ_SIRA          # U bayrağı
        if (r is not None and r.hedef_sira != SONSUZ_SIRA
                and (bilinmiyor or r.hedef_sira >= y["hedef_sira"])):
            # §6.6.2 — etkin rotası ve GEÇERLİ, yeterince büyük sırası olan
            # ARA düğüm RREP üretir. 🔒 K-208 H4: U bayraklı RREQ'e de (ns-3
            # hakem) ve iki öncül: ileri rotaya gönderen, TERS rotaya hedefe
            # doğru sonraki atlama.
            r.oncular.add(gonderen)
            ters = self._rota.get(kaynak)
            if ters is not None:
                ters.oncular.add(r.sonraki)
            self._sayac["rrep_uretilen"] += 1
            return (self._rrep_kur(
                hedef_adres=hedef, hedef_sira=r.hedef_sira, atlama=r.atlama,
                kaynak=kaynak, omur_s=max(0.0, r.son_gecerli_s - simdi_s),
                sonraki=gonderen),)

        ttl = y["ttl"] - 1
        if ttl <= 0:
            return ()
        # 🔒 K-208 H3 · §6.5: iletilen RREQ'in hedef sırası *"set to the
        # maximum of"* gelen değer ile bu düğümün bildiği GEÇERLİ sıra; düğüm
        # kendi değerini DEĞİŞTİRMEZ.
        bildigi = self._rota.get(hedef)
        yeni = dict(y, atlama=atlama, ttl=ttl)
        if bildigi is not None and bildigi.hedef_sira != SONSUZ_SIRA and (
                bilinmiyor or bildigi.hedef_sira > y["hedef_sira"]):
            yeni["hedef_sira"] = bildigi.hedef_sira
            yeni["bayraklar"] = 0                        # U bayrağı iner
        self._sayac["rreq_iletilen"] += 1
        self._son_yayin_s = simdi_s
        return (KontrolIstegi.kur(None, RREQ, yeni),)

    def _rrep_isle(self, gonderen: int, y: dict, simdi_s: float) -> tuple:
        """§6.7 · RREP işleme. HELLO da buraya gelir (§6.9).

        🔒 HELLO AYIRACI `kaynak == hedef` — RFC §6.9'un tanımı: HELLO, düğümün KENDİSİ hakkında
        yayınladığı bir RREP'tir — yani `kaynak == hedef == gönderen`. Gerçek
        bir RREP'te `kaynak` RREQ'i başlatan düğümdür ve hedeften farklıdır.
        """
        # 🔒 HELLO: iletilmez (§6.9). Ayıraç `kaynak == hedef`.
        # 🔒 K-208 H6 · §6.9: komşuya etkin rota, ömür ≥ `ALLOWED_HELLO_LOSS ×
        # HELLO_INTERVAL`, sıra *"MUST … the latest Destination Sequence
        # Number from the Hello"* (ns-3 `ProcessHello`). Rota
        # `kontrol_alindi`de kuruldu; burada sırası ve ömrü yazılır.
        if y["kaynak"] == y["hedef"]:
            k = self._rota.get(gonderen)
            if k is not None and k.gecerli and k.atlama == 1:
                k.hedef_sira = y["hedef_sira"]
                k.son_gecerli_s = max(
                    k.son_gecerli_s,
                    simdi_s + ALLOWED_HELLO_LOSS * HELLO_INTERVAL_S)
            return ()
        hedef, hedef_sira = y["hedef"], y["hedef_sira"]
        atlama = y["atlama"] + 1
        omur = simdi_s + y["omur_ms"] / 1000.0

        r = self._rota.get(hedef)
        # 🔴 §6.7 (i)–(iv), BİRİNCİL BELGEDEN ve ns-3 `RecvReply` ile aynı:
        # sıra bilinmiyor · daha büyük · EŞİT ve rota etkin değil · EŞİT ve
        # daha az atlama. İlk yazımda *"rota geçersizse her RREP"* kabul
        # ediliyordu — daha KÜÇÜK sıralı, yani bu düğümün kopmasından önceki
        # bir yolu anlatan bayat RREP dâhil. Ölçüldü (30 Eylül, statik-yok
        # 1000): 331 bayat kabul, döngülü 77 paketin 61'inde döngüyü kuran
        # buydu; TTL düşüşü 42 (K-205, `arsiv/teshis/u1_2026-09-29/aciklama/`).
        daha_iyi = (r is None
                    or r.hedef_sira == SONSUZ_SIRA                  # (i)
                    or hedef_sira > r.hedef_sira                    # (ii)
                    or (hedef_sira == r.hedef_sira
                        and (not r.gecerli or atlama < r.atlama)))  # (iii)·(iv)
        if daha_iyi:
            self._rota[hedef] = Rota(
                sonraki=gonderen, atlama=atlama, hedef_sira=hedef_sira,
                son_gecerli_s=omur,
                oncular=(r.oncular if r else set()))
            self._kurtarma(hedef)
            # ⚠️ ARA DÜĞÜMDE DE rota kuruldu: burada bekleyen paketler de
            # artık gönderilebilir olabilir. Uyandırma aşağıda, iletme
            # dalında ekleniyor.
        # 🔴 K-208 H5: reddedilen RREP mevcut rotanın ömrünü UZATMAZ (ilk
        # yazımda uzatıyordu; RFC'de ve ns-3'te yok).

        kaynak = y["kaynak"]
        if kaynak == self.kimlik:
            # 🔒 Keşif yalnız kullanılabilir bir rota VARSA biter: reddedilen
            # (bayat) bir RREP keşfi "başarılı" sayıp kapatsaydı tampondaki
            # paketler rotasız beklerdi (AOMDV'de 22 Eylül'de ölçüldü).
            if (hedef in self._kesif
                    and self._rota_al(hedef, simdi_s) is not None):
                del self._kesif[hedef]
                self._sayac["kesif_basarili"] += 1
            if not daha_iyi:
                return ()
            # 🔒 TAMPONU YENİDEN SORDURAN ŞEY BU UYANDIRMADIR (K-135).
            # Simülatör "rota bulundu mu" diye tahmin etmez; bilen taraf
            # protokoldür ve bir `Uyandirma` döndürerek söyler. `Beyan`a
            # bağlanmadı: beyan YALNIZ ölçüme gider ve bir eyleme bağlanamaz.
            # 🔴 `rota_kuruldu(hedef)` BURADAN KALKTI (K-139): anahtarı
            # HEDEFTİ ve kopmanın anahtarı KOMŞU olduğu için Δ neredeyse hiç
            # kapanmıyordu (bagimsiz-yok: 789 kopma anahtarına karşı 9 kurulum
            # anahtarı, 6'sı ortak). Kurtarma artık `_kurtarma` ile, rota
            # kurulan HER yerde, kopan komşu anahtarıyla beyan ediliyor.
            return (Uyandirma(NODE_TRAVERSAL_TIME_S, "tampon"),)
        # 🔒 K-208 H5 · §6.7: RREP yalnız ileri rota *"created or updated"*
        # ise iletilir (ns-3 koşulsuz iletir — RFC'den sapma, alınmadı).
        # Kabul edilmeyen bir RREP'i iletmek, bu düğümün KULLANMADIĞI bir yolu
        # aşağıya duyurmaktı.
        if not daha_iyi:
            return ()
        geri = self._rota_al(kaynak, simdi_s)
        if geri is None:
            return ()
        # §6.7: ileri rotanın öncülüne kaynağa doğru sonraki atlama · ters
        # rotanın ömrü `max(mevcut, şimdi + ACTIVE_ROUTE_TIMEOUT)` · hedefe
        # doğru sonraki atlamanın (gönderen) girdisinin öncülüne kaynağa
        # doğru sonraki atlama.
        self._rota[hedef].oncular.add(geri.sonraki)
        geri.son_gecerli_s = max(geri.son_gecerli_s,
                                 simdi_s + ACTIVE_ROUTE_TIMEOUT_S)
        komsu = self._rota.get(gonderen)
        if komsu is not None:
            komsu.oncular.add(geri.sonraki)
        self._sayac["rrep_iletilen"] += 1
        iletim = self._rrep_kur(
            hedef_adres=hedef, hedef_sira=hedef_sira, atlama=atlama,
            kaynak=kaynak, omur_s=max(0.0, omur - simdi_s),
            sonraki=geri.sonraki)
        return (iletim, Uyandirma(NODE_TRAVERSAL_TIME_S, "tampon"))

    def _rerr_isle(self, gonderen: int, y: dict, simdi_s: float) -> tuple:
        """§6.11 · RERR işleme — etkilenen rotalar geçersizleşir."""
        ulasilamaz = y["ulasilamaz"]
        etkilenen: list[int] = []
        for h, sira in zip(ulasilamaz, y["ulasilamaz_sira"], strict=True):
            r = self._rota.get(h)
            if r is not None and r.gecerli and r.sonraki == gonderen:
                self._gecersizlestir(r, simdi_s, rerr_sira=sira)
                etkilenen.append(h)
        if not etkilenen:
            return ()
        # 🔴 RERR bir KOPMA BEYANI DEĞİLDİR (K-139). Uzaktaki bir bağın
        # kopmasının haberidir; bu düğümün kendi bağı sağlam. Önceden her
        # ulaşılamaz HEDEF bir `kopma` sayılıyordu ve algılama duyarlılığı
        # (fiziksel BAĞ kopmalarına oran) bu yüzden şişiyordu.
        return self._rerr_kur(tuple(etkilenen), simdi_s)

    # ==================================================================
    # KANCA · iletim başarısız
    # ==================================================================
    def iletim_basarisiz(self, gozlem: Gozlem, hedef: int | None,
                         tur: str) -> tuple:
        """§6.11 · MAC vazgeçti = bağ koptu. Kopmanın ÖĞRENİLDİĞİ yer.

        🔒 Kanca (`13` R3) ve beyan kanalı (K-134) olmadan AODV bir kopmayı
        ne öğrenebilir ne söyleyebilirdi.
        """
        if hedef is None:
            return ()
        simdi = float(gozlem.saat_s)
        if tur == "kontrol":
            # 🔒 §6.8 (K-194): bu gerçeklemede tek yönlü giden TEK kontrol
            # mesajı RREP'tir (RREQ ve RERR yayın) — yani bu, *"its
            # transmission of a RREP message has failed"* durumudur ve bağ
            # katmanı onayının gelmemesiyle sezilir (RFC'nin izin verdiği yol).
            self._kara_liste[hedef] = simdi + BLACKLIST_TIMEOUT_S
            self._sayac["kara_liste_eklenen"] += 1
        self._komsu.pop(hedef, None)
        return self._bag_koptu(hedef, simdi)

    def _kara_listede(self, komsu: int, simdi_s: float) -> bool:
        """§6.8 — `BLACKLIST_TIMEOUT` dolmadıysa listede; dolmuşsa çıkarılır."""
        bitis = self._kara_liste.get(komsu)
        if bitis is None:
            return False
        if simdi_s >= bitis:
            del self._kara_liste[komsu]
            return False
        return True

    # ==================================================================
    # KANCA · teşhis
    # ==================================================================
    def teshis(self, dugum: int) -> dict:
        """🔴 Yalnız sonuç satırına; karara GİRMEZ."""
        gecerli = sum(1 for r in self._rota.values() if r.gecerli)
        return {**self._sayac,
                "rota_girdisi": len(self._rota),
                "rota_gecerli": gecerli,
                "komsu": len(self._komsu),
                "suren_kesif": len(self._kesif)}
