"""
AOMDV — Marina & Das (ICNP 2001) + RFC 3561. Üçüncü taban protokol.

🔒 NEDEN AODV'NİN ALT SINIFI
============================
Makale AOMDV'yi AODV'nin bir UZANTISI olarak tanımlıyor ve ilkesi açık:
*"the use of routing information already available in the underlying AODV
protocol as much as possible"*. Bu yüzden RFC 3561'in makalenin değiştirmediği
her parçası — HELLO (§6.9), genişleyen halka araması ve yeniden deneme (§6.3 ·
§6.4), rota bekleme tamponu, hız sınırları (§10), RERR'in öncül kuralı
(§6.11), sıra numarası kuralları, zaman aşımları, komşu ömrü — `AODV`dan
MİRAS alınır ve burada yeniden yazılmaz. Aynı kuralı iki yerde yazmak bu
projenin bilinen hata sınıfıdır (`03` §B5): iki kopya bir gün ayrışır.

Yeniden yazılan yalnız makalenin DEĞİŞTİRDİĞİ yerlerdir: rota girdisi
(Şekil 2b), güncelleme kuralı (Şekil 3), RREQ'in `ilk_atlama` alanı ve
yinelenen kopyaların işlenmesi (§3.2), hedefin k kopyaya cevabı (§3.2),
RREP'in farklı ters yollardan dönmesi (§3.2) ve rota bakımı (§1: *"a new
route discovery is needed only when all paths to the destination break"*).

AODV'nin beyanlı sapmaları (`aodv_bicim.py`: yerel onarım · RREP-ACK · G
bayrağı · önek · önceki atlamanın ömrü) AOMDV için de AYNEN geçerlidir.

🔴 BEYANLI SEÇİMLER — ne makalede ne RFC 3561'de (`v2/02` §R4.1 seçenek a)
=========================================================================
| # | boşluk | seçim | gerekçe · yön |
|---|---|---|---|
| S1 | veri hangi yoldan | TEK yol: en az atlamalı yol (eşitlikte küçük komşu kimliği); o yol düşünce sıradaki | makale §3.2: *"we are interested in investigating the fault tolerance property of multipath routing, and not the load balancing property"* |
| S2 | yol başına zaman aşımı | YOK — girdi başına tek ömür (Şekil 2b'nin tablosu tek bir `expiration timeout` gösteriyor); bir yol yalnız bağ kopması ya da RERR ile düşer | ⚠️ yedek yol BAYATLAYABİLİR: birincil düşünce yedeğe geçiş bir MAC vazgeçmesine mal olabilir → AOMDV'yi ZAYIFLATABİLİR |
| S3 | bağ kopunca | kopan komşudan geçen YOLLAR silinir; yolu kalmayan hedef geçersizleşir ve RFC §6.11'le RERR'e girer; yolu kalan hedef için RERR YOK | makale §1 · §3 |
| S4 | RERR alınca | yalnız GÖNDERENDEN geçen yol silinir; yolu kalmayan hedef geçersizleşir ve RERR iletilir | S3'ün aynısı |
| S5 | RREP'i ara düğüm iletirken | düğüm KENDİ ilanını (sıra, ilan edilen atlama) taşır ve RREP'i bu keşifte henüz kullanılmamış bir ters yoldan gönderir; hepsi kullanıldıysa birincilden | makale §3.2: *"Each RREP arriving at an intermediate node takes a different reverse route when multiple routes are already available"* · §3.1: ilan edilen atlama, ilan GÖNDERİLİRKEN güncellenir |
| S6 | `ilk_atlama` alanının genişliği | 32 bit | `aomdv_bicim.py` — AOMDV'yi pahalı yöne |
| S7 | hedefte ters rota | yalnız YENİ `ilk_atlama` taşıyan kopya kurar (ara düğümle aynı); cevap ise k benzersiz KOMŞUYA, ilk atlamadan bağımsız | makale §3.2: *"At the destination, reverse routes are set up just like in the case of intermediate nodes"* |
| S8 | tek atlamalı komşu rotası | kontrol mesajı alınan komşuya `(n, 1)` yolu güncelleme kuralının DIŞINDAN eklenir | AODV'nin §6.2 komşu rotası; sonraki atlaması hedefin kendisi olan yol döngü kuramaz ve ilan edilen atlamayı büyütmez |
| S9 | ölçüm beyanı (K-139 anlamı) | `kopma(K)`: geçerli bir girdinin BİRİNCİL yolu K'dan geçiyordu · `rota_kuruldu(K)`: etkilenen hedeflerden birine yol KALDIYSA aynı anda (Δ = 0) | AOMDV'nin hızlı kurtarması tam olarak budur. 🔒 Yalnız BİRİNCİL yol sayılıyor: yedeği düşen bir hedef "etkilenmedi" — aksi hâlde Δ AOMDV lehine yazılırdı |
| S10 | geçersiz girdiye gelen ilan | Şekil 3'ün (1) dalı — sıra karşılaştırılmadan kabul; RFC 3561 ve `AODV` ile aynı | Şekil 3 geçersiz girdiyi ele almıyor. Harfiyen uygulanınca yerel sıra şişmesi rotayı kilitliyordu — ölçüm `_kural`da |

🔒 KÂHİN ERİŞİMİ YOK — `aodv.py` ile aynı: yalnız `sim2/gozlem/` ve kendi
biçim dosyaları.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sim2.gozlem.karar import Beyan
from sim2.gozlem.kontrol import KontrolIstegi, Uyandirma
from protokoller.aodv import AODV
from protokoller.aodv_bicim import (
    ACTIVE_ROUTE_TIMEOUT_S, MY_ROUTE_TIMEOUT_S, NET_TRAVERSAL_TIME_S,
    NODE_TRAVERSAL_TIME_S, PATH_DISCOVERY_TIME_S, SONSUZ_SIRA)
from protokoller.aomdv_bicim import K_CEVAP, RREQ

__all__ = ["AOMDV", "CokluRota"]

# Şekil 3'ün ∞'u — "bu sıra numarasıyla henüz ilan edilmedi".
_SONSUZ = float("inf")


@dataclass(slots=True)
class CokluRota:
    """Şekil 2(b) · AOMDV girdisi — RFC 3561 §6.2 alanları + yol listesi.

    🔒 `sonraki` ve `atlama` BİRİNCİL yoldur (S1). AODV'nin veri gönderme
    kodu (`sonraki_atlama`) onları okur ve bu sayede AOMDV'de yeniden
    yazılmaz. 🔒 DEĞİŞMEZ: geçerli bir girdinin en az bir yolu vardır — yol
    silen her yer, yolu kalmayan girdiyi geçersizleştirir.
    """

    hedef_sira: int
    yollar: dict[int, int] = field(default_factory=dict)   # sonraki → atlama
    ilan_atlama: float = _SONSUZ                           # advertised_hopcount
    gecerli: bool = True
    son_gecerli_s: float = 0.0
    silme_s: float = 0.0
    oncular: set[int] = field(default_factory=set)

    def _sirali(self) -> list[tuple[int, int]]:
        return sorted((a, s) for s, a in self.yollar.items())

    @property
    def sonraki(self) -> int:
        return self._sirali()[0][1]

    @property
    def atlama(self) -> int:
        return self._sirali()[0][0]

    def ilan_et(self) -> int:
        """§3.1 · *"advertised hopcount ... is updated whenever it sends a
        route advertisement"* — yolların atlama sayılarının EN BÜYÜĞÜ."""
        self.ilan_atlama = max(self.yollar.values())
        return int(self.ilan_atlama)


class AOMDV(AODV):
    """Ad hoc On-demand Multipath Distance Vector — Marina & Das 2001."""

    ad = "aomdv"

    __slots__ = ("_ilk_atlama", "_cevaplanan", "_rrep_yolu")

    def __init__(self, kimlik: int) -> None:
        super().__init__(kimlik)
        # §3.2 · (kaynak, rreq_kimlik) → RREQ'in geldiği ilk atlamalar.
        self._ilk_atlama: dict[tuple[int, int], set[int]] = {}
        # §3.2 · hedefte: (kaynak, rreq_kimlik) → cevap verilen komşular.
        self._cevaplanan: dict[tuple[int, int], set[int]] = {}
        # S5 · (kaynak, hedef, sıra) → [ilk görülme, kullanılan ters yollar].
        self._rrep_yolu: dict[tuple[int, int, int], tuple[float, set[int]]] = {}
        self._sayac.update({"rreq_yeni_yol": 0, "yol_dusen": 0,
                            "yedek_yola_gecis": 0, "cevap_siniri": 0})

    # ==================================================================
    # ŞEKİL 3 · GÜNCELLEME KURALI
    # ==================================================================
    def _kural(self, hedef: int, sira_j: int, ilan_j: int, j: int,
               omur_s: float) -> bool:
        """Şekil 3, satır satır. Döner: j üzerinden yeni bir yol KURULDU mu.

            (1) if seq_i < seq_j:            (2) seq_i := seq_j
            (3)   if i ≠ d: (4) adv_i := ∞   (5) route_list := NULL
                            (6) insert (j, adv_j + 1)
            (7)   else: (8) adv_i := 0
            (9) elif seq_i = seq_j and (adv_i, i) > (adv_j, j):
            (10)  insert (j, adv_j + 1)

        (9) SÖZLÜK SIRASIYLA karşılaştırır; makaleye göre döngüsüzlüğü (1) ile
        (9)–(10) birlikte sağlar. Yol listesi girdisi yoksa `seq_i` tanımsızdır
        ve (1) dalı işler. (7)–(8): bir düğüm kendine rota TUTMAZ.

        🔴 S10 · GEÇERSİZ GİRDİDE (1) dalı işler — Şekil 3 geçersiz girdiyi
        ele almıyor; burada *"rota geçersizse ilan kabul edilir"*. ⚠️ Bu RFC
        3561'in kuralı DEĞİL: §6.7 geçersiz girdide yalnız eşit ya da büyük
        sırayı kabul eder ve `AODV` K-205'te ona döndü (bayat kabul AODV'de
        döngü kuruyordu). AOMDV'de sapma aşağıdaki ölçümle duruyor; döngü
        etkisi AOMDV'de ölçülmedi.
        Sebebi ÖLÇÜLDÜ (22 Eylül 2026, küçük dünya `bagimsiz-yok`): RFC §6.11
        her geçersizleştirmede sıra numarasını YEREL olarak bir artırır; bir
        komşunun rotası kopup (S8 ile) yeniden kurulup yeniden kopunca yerel
        sıra hedefin gerçek sırasını GEÇER. Şekil 3 harfiyen uygulanınca
        kaynak hedefin kendi cevabını *"bayat"* diye reddediyordu: 184 RREP
        rotayı kurmadı, keşif *"başarılı"* sayılıp kapandı ve 79 paket tampon
        tavanından düştü (PDR 0,323; AODV 0,510).
        """
        if hedef == self.kimlik:
            return False
        r = self._rota.get(hedef)
        if r is None or not r.gecerli or r.hedef_sira < sira_j:
            onculer = r.oncular if r is not None else set()
            self._rota[hedef] = CokluRota(
                hedef_sira=sira_j, yollar={j: ilan_j + 1},
                son_gecerli_s=omur_s, oncular=onculer)
            return True
        if r.hedef_sira == sira_j and (r.ilan_atlama, self.kimlik) > (ilan_j, j):
            yeni = j not in r.yollar
            r.yollar[j] = ilan_j + 1
            r.son_gecerli_s = max(r.son_gecerli_s, omur_s)
            return yeni
        return False

    def _gecersizlestir(self, r, simdi_s: float) -> None:
        """RFC §6.11 (miras) + yol listesi ve ilan boşalır — girdi SİLİNMEZ.

        🔒 Sıra numarası AOMDV'de K-205'ten ÖNCEKİ gibi her geçersizleştirmede
        bir artar, bilinmeyen sıra dâhil: AODV'nin §6.11 düzeltmesi (K-205)
        AOMDV'nin ölçülmüş sıra kuralına (yukarıdaki `_kural`, S10)
        dokunmaz — `AOMDV-b` U1'i bu hâliyle geçti, davranışı birebir kalır.
        """
        bilinmeyen = r.hedef_sira == SONSUZ_SIRA
        super()._gecersizlestir(r, simdi_s)
        if bilinmeyen:
            r.hedef_sira = SONSUZ_SIRA + 1
        r.yollar.clear()
        r.ilan_atlama = _SONSUZ

    # ==================================================================
    # RREQ
    # ==================================================================
    def _rreq_kur(self, hedef: int, ttl: int, simdi_s: float) -> KontrolIstegi:
        """RFC §6.3 (miras) + `ilk_atlama` alanı. Kaynağın kendi RREQ'inde
        alan anlamsızdır — ilk atlama, RREQ'i KAYNAKTAN duyan komşunun
        kendisidir (`_rreq_isle`); kaynak kendi kimliğini yazar."""
        ist = super()._rreq_kur(hedef, ttl, simdi_s)
        return KontrolIstegi.kur(None, RREQ, {**dict(ist.yuk),
                                              "ilk_atlama": self.kimlik})

    def _ters_omur(self, atlama: int, simdi_s: float) -> float:
        """RFC §6.5'in ters rota ömrü — `AODV._ters_rota` ile aynı formül."""
        omur = simdi_s + 2 * NET_TRAVERSAL_TIME_S - 2 * atlama * NODE_TRAVERSAL_TIME_S
        return max(omur, simdi_s + ACTIVE_ROUTE_TIMEOUT_S)

    def _rreq_isle(self, gonderen: int, y: dict, simdi_s: float) -> tuple:
        """§3.2 · yinelenen kopyalar HEMEN ATILMAZ."""
        kaynak, kimlik, hedef = y["kaynak"], y["rreq_kimlik"], y["hedef"]
        anahtar = (kaynak, kimlik)
        if kaynak == self.kimlik:
            self._sayac["rreq_bastirilan"] += 1
            return ()
        # İlk atlama: RREQ'i kaynağın kendisinden duyduysam ilk atlama BENİM.
        ilk = self.kimlik if gonderen == kaynak else y["ilk_atlama"]
        ilk_kopya = anahtar not in self._gorulen_rreq
        gorulen = self._ilk_atlama.setdefault(anahtar, set())
        yeni_ilk = ilk not in gorulen
        if ilk_kopya:
            self._gorulen_rreq[anahtar] = simdi_s
        elif not yeni_ilk and hedef != self.kimlik:
            self._sayac["rreq_bastirilan"] += 1
            return ()
        yeni_yol = False
        if yeni_ilk:
            gorulen.add(ilk)
            yeni_yol = self._kural(kaynak, y["kaynak_sira"], y["atlama"], gonderen,
                                   self._ters_omur(y["atlama"] + 1, simdi_s))
            if yeni_yol:
                self._kurtarma(kaynak)
                if not ilk_kopya:
                    self._sayac["rreq_yeni_yol"] += 1

        if hedef == self.kimlik:
            # §3.2 · "looser reply policy": en çok k BENZERSİZ KOMŞUYA,
            # ilk atlamadan bağımsız. RFC §6.6.1'in sıra kuralı miras.
            cevap = self._cevaplanan.setdefault(anahtar, set())
            if gonderen in cevap or len(cevap) >= K_CEVAP:
                self._sayac["cevap_siniri"] += 1
                return ()
            cevap.add(gonderen)
            if y["hedef_sira"] == self._sira + 1:
                self._sira_artir()
            self._sayac["rrep_uretilen"] += 1
            return (self._rrep_kur(
                hedef_adres=self.kimlik, hedef_sira=self._sira, atlama=0,
                kaynak=kaynak, omur_s=MY_ROUTE_TIMEOUT_S, sonraki=gonderen),)

        r = self._rota_al(hedef, simdi_s)
        taze = (r is not None and r.hedef_sira >= y["hedef_sira"]
                and y["hedef_sira"] != SONSUZ_SIRA)
        if taze and (ilk_kopya or yeni_yol):
            # §3.2 · *"If a reverse path is set up and a valid route to the
            # destination is available at the intermediate node, it sends
            # back a RREP"* — RFC §6.6.2'nin tazelik koşuluyla.
            r.oncular.add(gonderen)
            self._sayac["rrep_uretilen"] += 1
            return (self._rrep_kur(
                hedef_adres=hedef, hedef_sira=r.hedef_sira, atlama=r.ilan_et(),
                kaynak=kaynak, omur_s=max(0.0, r.son_gecerli_s - simdi_s),
                sonraki=gonderen),)
        # §3.2 · *"Just as in AODV, only the first arriving RREQ copy is
        # forwarded"*.
        if not ilk_kopya:
            return ()
        ttl = y["ttl"] - 1
        if ttl <= 0:
            return ()
        geri = self._rota.get(kaynak)
        if geri is None or not geri.gecerli:
            return ()
        self._sayac["rreq_iletilen"] += 1
        self._son_yayin_s = simdi_s
        # §3.1 · RREQ, kaynak için bir İLANDIR: `atlama` = ilan edilen atlama.
        return (KontrolIstegi.kur(None, RREQ, {**y, "atlama": geri.ilan_et(),
                                               "ttl": ttl, "ilk_atlama": ilk}),)

    # ==================================================================
    # RREP
    # ==================================================================
    def _rrep_isle(self, gonderen: int, y: dict, simdi_s: float) -> tuple:
        """§3.1 · §3.2 · RREP bir hedef İLANIDIR; güncelleme kuralından geçer."""
        if y["kaynak"] == y["hedef"]:
            return ()                              # HELLO (§6.9, miras)
        hedef, kaynak = y["hedef"], y["kaynak"]
        omur = simdi_s + y["omur_ms"] / 1000.0
        yeni = self._kural(hedef, y["hedef_sira"], y["atlama"], gonderen, omur)
        if yeni:
            self._kurtarma(hedef)
        if kaynak == self.kimlik:
            if hedef in self._kesif:
                del self._kesif[hedef]
                self._sayac["kesif_basarili"] += 1
            if not yeni:
                return ()
            return (Uyandirma(NODE_TRAVERSAL_TIME_S, "tampon"),)
        r = self._rota_al(hedef, simdi_s)
        geri = self._rota_al(kaynak, simdi_s)
        if r is None or geri is None:
            return ()
        # S5 · bu keşifte henüz kullanılmamış bir ters yol.
        anahtar = (kaynak, hedef, r.hedef_sira)
        _t, kullanilan = self._rrep_yolu.setdefault(anahtar, (simdi_s, set()))
        adaylar = [s for _a, s in geri._sirali()
                   if s in self._komsu and s not in kullanilan]
        yol = adaylar[0] if adaylar else geri.sonraki
        kullanilan.add(yol)
        r.oncular.add(yol)
        self._sayac["rrep_iletilen"] += 1
        iletim = self._rrep_kur(
            hedef_adres=hedef, hedef_sira=r.hedef_sira, atlama=r.ilan_et(),
            kaynak=kaynak, omur_s=max(0.0, r.son_gecerli_s - simdi_s),
            sonraki=yol)
        if yeni:
            return (iletim, Uyandirma(NODE_TRAVERSAL_TIME_S, "tampon"))
        return (iletim,)

    # ==================================================================
    # KOMŞU ROTASI · BAĞ KOPMASI · RERR
    # ==================================================================
    def _komsu_rotasi(self, komsu: int, simdi_s: float) -> None:
        """S8 · tek atlamalı yol, `ACTIVE_ROUTE_TIMEOUT` ömürlü (RFC §6.2)."""
        r = self._rota.get(komsu)
        if r is None or not r.gecerli:
            self._rota[komsu] = CokluRota(
                hedef_sira=(r.hedef_sira if r else SONSUZ_SIRA),
                yollar={komsu: 1},
                son_gecerli_s=simdi_s + ACTIVE_ROUTE_TIMEOUT_S,
                oncular=(r.oncular if r else set()))
            self._kurtarma(komsu)
            return
        r.yollar.setdefault(komsu, 1)
        r.son_gecerli_s = max(r.son_gecerli_s, simdi_s + ACTIVE_ROUTE_TIMEOUT_S)

    def _bag_koptu(self, komsu: int, simdi_s: float) -> tuple:
        """S3 · S9 — kopan komşudan geçen YOLLAR düşer."""
        etkilenen: list[int] = []
        olen: list[int] = []
        for h, r in self._rota.items():
            if not r.gecerli or komsu not in r.yollar:
                continue
            birincil = r.sonraki == komsu
            del r.yollar[komsu]
            self._sayac["yol_dusen"] += 1
            if birincil:
                etkilenen.append(h)
            if not r.yollar:
                self._gecersizlestir(r, simdi_s)
                olen.append(h)
        if not etkilenen:
            return ()
        self._kopuk.setdefault(komsu, set()).update(etkilenen)
        beyanlar: tuple = (Beyan("kopma", komsu=komsu),)
        if any(self._rota[h].gecerli for h in etkilenen):
            # AOMDV'nin kurtarması: yedek yol ZATEN var (S9).
            del self._kopuk[komsu]
            self._sayac["yedek_yola_gecis"] += 1
            beyanlar += (Beyan("rota_kuruldu", komsu=komsu),)
        return beyanlar + self._rerr_kur(tuple(olen), simdi_s)

    def _rerr_isle(self, gonderen: int, y: dict, simdi_s: float) -> tuple:
        """S4 · yalnız GÖNDERENDEN geçen yol düşer. RERR bir kopma beyanı
        değildir (K-139, miras anlam)."""
        olen: list[int] = []
        for h in y["ulasilamaz"]:
            r = self._rota.get(h)
            if r is None or not r.gecerli or gonderen not in r.yollar:
                continue
            del r.yollar[gonderen]
            self._sayac["yol_dusen"] += 1
            if not r.yollar:
                self._gecersizlestir(r, simdi_s)
                olen.append(h)
        if not olen:
            return ()
        return self._rerr_kur(tuple(olen), simdi_s)

    # ==================================================================
    # BAKIM
    # ==================================================================
    def _bakim(self, simdi_s: float) -> tuple:
        """Miras süpürme + §3.2'nin kopya kayıtları `PATH_DISCOVERY_TIME` yaşar."""
        niyetler = super()._bakim(simdi_s)
        for d in (self._ilk_atlama, self._cevaplanan):
            for k in [k for k in d if k not in self._gorulen_rreq]:
                del d[k]
        for k in [k for k, (t, _) in self._rrep_yolu.items()
                  if simdi_s - t > PATH_DISCOVERY_TIME_S]:
            del self._rrep_yolu[k]
        return niyetler

    def teshis(self, dugum: int) -> dict:
        """🔴 Yalnız sonuç satırına; karara GİRMEZ."""
        t = super().teshis(dugum)
        gecerli = [r for r in self._rota.values() if r.gecerli]
        t["yol_toplam"] = sum(len(r.yollar) for r in gecerli)
        t["cok_yollu_girdi"] = sum(1 for r in gecerli if len(r.yollar) > 1)
        return t
