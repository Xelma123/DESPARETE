"""
DESPARETE — öğrencinin protokolü; simülatöre bağlanan sınıf.

Bugünkü hâl **v0.4.1** = `PROFIL_V02` + `SECENEK_V041` (`desparete_bayrak.py`,
K-172). Bağlayıcı olan bu kod; tasarımın ilk taslağı
`arsiv/DESPARETE_TASARIM_PAKETI_v0.1_2026-09-22/` (tek okuma `36`). Sürümler:
v0.1 tasarım paketi (bütün bayraklar açık) · v0.2 yalın profil (K-161) ·
v0.3 + V1 · V5 · V7 (K-164) · v0.4 + V8 · V10 (K-167) · v0.4.1 + V11 komut
geri izi (K-172).

Parçalar: biçimler `desparete_bicim` · M0.1 metrik `desparete_metrik` ·
komşu yaşamı `desparete_komsu` · alan ve ardıl `desparete_alan` · edinim ve
onarım `desparete_edinim` · postür `desparete_politika` · bayraklar
`desparete_bayrak`. Her parça kendi testiyle (`tests2/test_desparete.py`).

🔒 KÂHİN ERİŞİMİ YOK
Yalnız `sim2/gozlem/`i içe aktarır (içe aktarma testi bağlar). Bildiği her
şey aldığı bir DESPARETE mesajından, kendi MAC'inin sonucundan
(`iletim_sonucu`, K-151) ya da kendi saatinden gelir.

🔒 HEDEF — tek-sink profili (K-160 §10)
SinkID (geçit) yapılandırmadır (`36` §2): kurucu `sink`i alır, yalnız geçit
alanı kurulur. Geçit dışı hedefli veri yerel politika hatasıdır (`23` §7):
V11 açıkken komut telemetrinin geri iziyle taşınır, kapalıyken `politika`
ile düşer (K-172). `komut_alanlari=True` K-150 §4 A'dır; tam ölçekte kontrol
yükünden çöktüğü ölçüldü (K-160), yalnız o bulgu için durur.

🔒 KOMŞU ADAYI (K-154)
Koşum beacon'ı kapalı; aday, duyulan her DESPARETE kontrol çerçevesinin
göndereni. V5 açıkken yalnız uygulanabilir ilanın sahibi (K-163).

🔒 OLAYIN SIRASI (`22` §3)
Her kancada önce komşu değişimleri alanlara verilir, sonra alan işlemi,
sonra alanın doğurduğu edinim ve tampon olayları. Ters sıra, ardılı kopan
bir alanın kopmayı beyan etmeden yeni ardıla geçmesine izin verirdi (K-160).

🔒 BEYANLAR — taban protokollerle aynı tanım (K-139 · K-141)
`kopma(j)`: ACTIVE olmaktan çıkan `j` bir iletilebilir alanın ardılıysa ·
`rota_kuruldu(j)`: etkilenen alan yeniden iletilebilir olunca ·
`rota_gecersiz(hedef)`: alanı bilinen ama iletilemeyen hedefe paket düşerken.
Niyet döndüremeyen sonuç kancasında doğan kurtarma, niyet döndürebilen ilk
kancada (en geç 0,5 s sonra) beyan edilir.

🔒 ONARIM TAMPONU (`36` §6 · `22` §8.1 · `21` §2.4)
REPAIRING alana giden paket simülatörün bekleme tamponunda tutulur
(`Karar.beklet`); alan iletilebilir ya da ulaşılamaz olunca bir uyandırma
tamponu yeniden sordurur. Onarım en çok `T_repair_max` (6 s) sürer. Alan
başına en çok `TAMPON_KOTASI` (6) ayrı paket tutulur, Data-ID'siyle
`(kaynak, kaynak_sira)` tanınır; fazlası `rota_gecersiz` ile düşer (K-157).
UNREACHABLE alana yeni paket tampona girmez.

🔒 YENİDEN EDİNİM (K-152 §2)
Düğümün KENDİ paketi ulaşılamaz ya da bilinmeyen hedefe giderken, son
edinim bölümünün bitişinden en az `T_repair_max` geçmişse yeni edinim
başlar; röleler başlatmaz; paket düşer.

POSTÜR (`22` §7 · K-158)
İletilebilir her alan epochta bir kez, en son değerlendirilir. STEADY →
CAUTION girişinde seçili ardıla bir doğrulama oturumu. Yedeklilik yok →
PROTECT yok; postür ardıl seçimine, maliyete ve kapılara dokunmaz.
"""

from __future__ import annotations

from sim2.gozlem.karar import Beyan, Karar
from sim2.gozlem.kontrol import KontrolIstegi, Uyandirma
from sim2.gozlem.pencere import Gozlem
from protokoller.desparete_alan import (ESIT, FORWARDABLE, REPAIRING, YENI,
                                        AlanTablosu, seri_karsilastir)
from protokoller.desparete_bayrak import (PROFIL_V02, SECENEK_V041,
                                         Bayraklar, Secenekler)
from protokoller.desparete_bicim import (
    BAYRAK_BAGLAM, DFSN_REQUEST, DURUM_REACHABLE, FIELD_SOLICIT, FIELD_UPDATE,
    H_DATA, H_REQ, J_ADV_S, J_CONTROL_S, K_YEDEK_CANLI, L_ADV_MAX_S,
    L_ADV_SENT_KUANTA,
    OMUR_KUANTA_S, PROBE, PROBE_REPLY, PROBE_YANIT_ISTE, SEBEP_ACLIK,
    SEBEP_EDINIM, SURUM, T_ADV_REFRESH_S,
    T_GERI_IZ_S, T_REQ_DUPLICATE_S, TAMPON_KOTASI, TIP_DFSN_REQUEST, TIP_FIELD_SOLICIT,
    TIP_FIELD_UPDATE, TIP_PROBE, TIP_PROBE_REPLY, VERI_BASLIK_BAYT,
    tel_kimligi)
from protokoller.desparete_edinim import EdinimDenetcisi, EdinimEylemi
from protokoller.desparete_komsu import (ACTIVE, EXPIRED, ZAMAN_PAYI_S,
                                         KomsuTablosu, ProbeIstegi)
from protokoller.desparete_metrik import (SONSUZ, T_EPOCH_S, c_kalite, c_risk,
                                          maliyet)
from protokoller.desparete_politika import PolitikaTablosu

__all__ = ["DESPARETE"]

_ALAN_32 = (1 << 32) - 1
_ORNEK = 1              # yeniden başlatma yok → örnek kimliği ve OIID sabit
_KOMSU, _ALAN, _ILAN, _EDINIM = "komsu:", "alan:", "ilan:", "edinim:"
_TAMPON = "tampon"


class DESPARETE:
    """DESPARETE — komşu, alan, edinim ve onarım. Profil kurucudan
    (varsayılan v0.4.1 = `PROFIL_V02` + `SECENEK_V041`, K-172;
    v0.1 = `PROFIL_V01` + `SECENEK_YOK`)."""

    ad = "desparete"
    kosum_beaconi = False
    veri_baslik_bayt = VERI_BASLIK_BAYT

    __slots__ = ("kimlik", "sink", "bayraklar", "secenekler", "komut_alanlari",
                 "komsular", "alanlar", "edinim", "politika", "_sira",
                 "_kopuk", "_beyanlar", "_planli", "_istek_gorulen", "_sayac",
                 "_kota", "_tutulan", "_olcum_bekleyen", "_saklanan",
                 "_tanidik", "_geri_iz", "cerceve_duyuldu")

    def __init__(self, kimlik: int, sink: int,
                 tampon_kotasi: int = TAMPON_KOTASI,
                 bayraklar: Bayraklar = PROFIL_V02,
                 komut_alanlari: bool = False,
                 secenekler: Secenekler = SECENEK_V041) -> None:
        self.kimlik = kimlik
        self.sink = sink
        # K-159 ablasyon · varsayılan v0.2 yalın profil (K-161, öğrenci).
        self.bayraklar = bayraklar
        # K-163 iyileştirmeler · varsayılan v0.4 = v0.3 + V8 + V10 (K-167).
        self.secenekler = secenekler
        self._olcum_bekleyen: list[int] = []    # V7: ölçüm PROBE'u bekleyen
        # V5a: ACTIVE olmayan komşu → son uygulanabilir ilanı ve varış anı
        self._saklanan: dict[int, tuple] = {}
        # V8 (K-167): bana hedefli PROBE gönderen komşu → son varış anı —
        # `23` §2'nin ilk kabul durumu (`AR_i` tanımlı). Süresiz: tasarımda
        # da örnek değişmedikçe düşmez; çerçevenin varışı bağı kanıtlar.
        self._tanidik: dict[int, float] = {}
        # V11 (K-172): kaynak → (komşu, kaynak_sira, varış anı) — geçide giden
        # DATA'nın bana geldiği komşu; komut bu izi tersinden izler.
        self._geri_iz: dict[int, tuple[int, int, float]] = {}
        # 🔒 Kanca YALNIZ V11 açıkken sunulur (`__slots__`ta bir yuva; boş
        # kalırsa simülatör kancayı "yok" görür). Kapalıyken çerçeve başına
        # hiçbir çağrı doğmaz ve satır v0.4 ile birebir kalır.
        if secenekler.komut_ters_yol:
            self.cerceve_duyuldu = self._cerceve_duyuldu
        # K-160 §10 C: v0.1 yalnız geçit alanıyla çalışır. `True` = K-150
        # §4 A (komut hedefleri için isteğe bağlı alanlar) — tam ölçekte
        # çöktüğü ölçüldü; yalnız o bulguyu yeniden üretmek ve v0.2 için.
        self.komut_alanlari = komut_alanlari
        self._kota = tampon_kotasi              # 3.9: 6 ↔ 32 (K-152 §3)
        # alan → onarım bölümünde tutulan Data-ID'ler `(kaynak, kaynak_sira)`
        self._tutulan: dict[int, set[tuple[int, int]]] = {}
        self._sira = 0                  # Control Sender Block — düğüm başına
        # V2+ (K-165): boşta sondalama yalnız gerekli komşuya — açıkken
        # bayraktan bağımsız etkin, filtreyle.
        hedefli = secenekler.hedefli_canlilik
        self.komsular = KomsuTablosu(
            self._sira_al, self._gerekli_mi,
            bayraklar.bosta_sondalama or hedefli,
            self._canli_tut if hedefli else None)
        self.alanlar = AlanTablosu(self._aktif_mi, self._maliyet)
        self.edinim = EdinimDenetcisi()
        # Koruma izni YOK: yedeklilik ilk gerçeklemede yok (K-150 §4) → PROTECT
        # yok; koşulların izinsiz sağlandığı anlar sayılır (K-158).
        self.politika = PolitikaTablosu(koruma_izni=False)
        if kimlik == sink:
            self.alanlar.kendi_alani(kimlik, dfsn=1)
        self._kopuk: dict[int, set[int]] = {}      # kopan komşu → etkilenen
        self._beyanlar: list[Beyan] = []
        # (önek, anahtar) → kurulmuş en erken uyandırma (tekrarı önlemek için)
        self._planli: dict[tuple[str, int], float] = {}
        # Request-ID → önbellekten düşeceği an (`23` §5.3, `T_req_duplicate`)
        self._istek_gorulen: dict[tuple[int, int, int], float] = {}
        self._sayac: dict[str, int] = {
            "ilan_gonderilen": 0, "ilan_alinan": 0, "probe_alinan": 0,
            "probe_yaniti_gonderilen": 0, "veri_iletilen": 0,
            "veri_ardilsiz": 0, "veri_hop_siniri": 0, "veri_bekletilen": 0,
            "solicit_gonderilen": 0, "solicit_yanitlanan": 0,
            "istek_gonderilen": 0, "istek_iletilen": 0,
            "istek_yanitlanan": 0, "istek_tekrar": 0, "istek_aktif_disi": 0,
            "hedefte_istek": 0, "hedef_alani_acildi": 0,
            "tampon_alinan": 0, "tampon_kota_disi": 0, "tampon_tepe": 0,
            # K-159 — mekanizmanın GERÇEKTEN işlediğinin sayaçları: edinim
            # oturumu tetikleyicisine göre; maliyet terimi sıfırdan büyükken
            # uygulanan (komşu × epoch).
            "edinim_ilk": 0, "edinim_yeniden": 0, "edinim_onarim": 0,
            "edinim_koruma": 0, "epoch_risk_cezali": 0,
            "epoch_kalite_cezali": 0,
            "veri_sink_disi": 0,          # K-160 §10 C: `23` §7 politika hatası
            "probe_yanitsiz": 0,          # K-163 V1: yanıt istenmedi
            "nitelik_ertelendi": 0,       # K-163 V5: yararsız komşu sondalanmadı
            "ilan_saklandi": 0, "saklanan_uygulandi": 0,   # K-164 V5a
            "saklanan_eskidi": 0,
            "istek_tanidik_kabul": 0,     # K-167 V8: ACTIVE değil, tanıdık
            "soru_nitelik": 0,            # K-167 V9: soru nitelik açtı
            "istek_aclik": 0, "hedefte_aclik": 0,   # K-167: açlık nedenli
            # K-172 V11: geri iz öğrenildi · silindi · komut izle iletildi ·
            # iz yok/bayat
            "geri_iz_ogrenilen": 0, "geri_iz_silinen": 0,
            "komut_iz_iletilen": 0, "komut_izsiz": 0,
        }

    # ==================================================================
    # KOMŞU ↔ ALAN ↔ EDİNİM
    # ==================================================================
    def _sira_al(self) -> int:
        self._sira = (self._sira + 1) & _ALAN_32
        return self._sira

    def _aktif_mi(self, j: int) -> bool:
        return self.komsular.durum(j) == ACTIVE

    def _maliyet(self, j: int) -> int | None:
        """M0.1 `C(i,j)` — ACTIVE ve en az bir uygun sonucu olan komşuda.
        Terimler ablasyon bayraklarıyla (K-159); ikisi açıkken `Olcum.c`."""
        k = self.komsular.kayit(j)
        if k is None or k.durum != ACTIVE or k.son_olcum is None \
                or k.son_olcum.q is None:
            return None
        b = self.bayraklar
        return maliyet(k.son_olcum.q, k.son_olcum.r, b.kalite_maliyeti,
                       b.risk_maliyeti)

    def _canli_tut(self, j: int, t: float) -> bool:
        """V2+ (K-165): `j` bir iletilebilir alanın ardılı ya da en iyi
        `K_YEDEK_CANLI` uygulanabilir yedeğinden biri mi?"""
        for a in self.alanlar.alanlar.values():
            if a.kendi or a.durum != FORWARDABLE:
                continue
            if a.ardil == j:
                return True
            yedek = [x for _, x in sorted(self.alanlar._guvenli_adaylar(a, t))
                     if x != a.ardil]
            if j in yedek[:K_YEDEK_CANLI]:
                return True
        return False

    def _gerekli_mi(self, j: int) -> bool:
        """`23` §3.2: bir alan `j`yi doğrulamaya ihtiyaç duyuyor mu — ardılsa."""
        return j in self.alanlar.ardillar()

    def _komsu_olaylari(self, t: float) -> None:
        """Komşu değişimleri alanlara — alan işleminden ÖNCE (`22` §3).

        🔴 K-160 §2: etkilenen alanlar yığının BAŞINDAKİ ardıllardan
        belirlenir. Önceden her değişim hemen alanlara veriliyordu; yığında
        önce işlenen bir değişim alanı yeniden hesaplatınca alan kopan
        komşunun güncel durumunu görüp ardılı SESSİZCE değiştiriyor, sıra
        kopan komşuya gelince kopma beyan edilmiyordu.
        """
        degisen = self.komsular.degisenleri_al()
        ardil = {h: a.ardil for h, a in self.alanlar.alanlar.items()
                 if a.durum == FORWARDABLE}
        kopan: set[int] = set()
        for j, yeni in degisen:
            if yeni != ACTIVE and j not in kopan:
                etkilenen = {h for h, s in ardil.items() if s == j}
                if etkilenen:
                    kopan.add(j)
                    self._beyanlar.append(Beyan("kopma", komsu=j))
                    self._kopuk.setdefault(j, set()).update(etkilenen)
        for j, yeni in degisen:
            self.alanlar.komsu_degisti(j, t, silindi=(yeni == EXPIRED))
            if yeni == ACTIVE and self.secenekler.nitelik_olcumu:
                self._olcum_bekleyen.append(j)
            if yeni == ACTIVE and j in self._saklanan:
                self._saklanani_uygula(j, t)

    def _saklanani_uygula(self, j: int, t: float) -> None:
        """V5a (K-164): saklanan ilan, komşu ACTIVE olunca OLAĞAN yoldan —
        kalan ömrüyle (orijinal bitiş anı korunur)."""
        h, dfsn, ads, durum, potansiyel, omur, gelis = self._saklanan.pop(j)
        gecen = int((t - gelis) / OMUR_KUANTA_S + 0.999999)
        kalan = omur - gecen
        if kalan <= 0:
            self._sayac["saklanan_eskidi"] += 1
            return
        self._sayac["saklanan_uygulandi"] += 1
        self.alanlar.ilan_al(j, h, dfsn, ads, durum, potansiyel, kalan, t)

    def _alan_olaylari(self, t: float) -> list:
        """Alanın doğurduğu olaylar → edinim eylemleri ve tampon (3.5)."""
        cikti: list = []
        tampon = False
        while self.alanlar.olaylar:
            olay, h = self.alanlar.olaylar.pop(0)
            if olay in ("onarim", "koruma"):
                if olay == "onarim":
                    self.politika.etkisiz(h)        # `22` §7: kanıt sıfır
                if (self.bayraklar.onarim_edinimi if olay == "onarim"
                        else self.bayraklar.ilan_korumasi):
                    eylem = self.edinim.baslat(h, t)
                    if eylem:
                        self._sayac[f"edinim_{olay}"] += 1
                    cikti += self._edinim_eylemleri(eylem, t)
            elif olay == "iletilebilir":
                self.edinim.basarili(h, t)
                self._tutulan.pop(h, None)          # bölüm bitti → kota boş
                self.politika.yeniden(h)            # STEADY; PROTECT dirilmez
                tampon = True
            elif olay == "ulasilamaz":
                self.edinim.zaman_asimi_bitir(h, t)
                self._tutulan.pop(h, None)
                self.politika.etkisiz(h)
                tampon = True
        if tampon:
            # Simülatör bekleme tamponunu `uyandi`dan sonra yeniden sorar.
            cikti.append(Uyandirma(ZAMAN_PAYI_S, _TAMPON))
        return cikti

    def _politika(self, t: float) -> list:
        """`35` §6 `EvaluatePolicy` — iletilebilir her alan, epochta bir kez.
        CAUTION'a giren alanın ardılına doğrulama oturumu (K-150 §4)."""
        probelar: list = []
        for h in sorted(self.alanlar.alanlar):
            a = self.alanlar.alanlar[h]
            if a.kendi or a.durum != FORWARDABLE:
                continue
            k = self.komsular.kayit(a.ardil)
            if k is None or k.son_olcum is None:
                continue
            if self.politika.degerlendir(h, t, a.ardil, k.son_olcum,
                                         self.alanlar.ek_ardil_var(h, t)):
                probelar += self.komsular.dogrula(a.ardil, t)
        return probelar

    def _niyetler(self, probelar, t: float, ek: tuple = (),
                  politika: bool = False) -> tuple:
        """Her kancanın ortak sonu: bekleyenler + beyanlar + uyandırmalar.
        Sıra `21` §3 madde 4: komşu → alan → (epochta) politika EN SON."""
        self._komsu_olaylari(t)
        niyet = list(ek) + self._alan_olaylari(t)
        if politika:
            probelar = list(probelar) + self._politika(t)
        if self._olcum_bekleyen:                    # V7 (K-163)
            bekleyen, self._olcum_bekleyen = self._olcum_bekleyen, []
            probelar = list(probelar)
            for j in bekleyen:
                probelar += self.komsular.olcum(j, t)
        for j in sorted(self._kopuk):
            if any(self.alanlar.durum(h) == FORWARDABLE
                   for h in self._kopuk[j]):
                del self._kopuk[j]
                self._beyanlar.append(Beyan("rota_kuruldu", komsu=j))
        niyet += [self._probe(p) for p in probelar]
        for r in self.alanlar.istekler:
            niyet.append(Uyandirma(max(r.en_erken_s - t, ZAMAN_PAYI_S),
                                   f"{_ILAN}{r.hedef}", jitter_s=r.pencere_s))
        self.alanlar.istekler.clear()
        niyet += [Uyandirma(g, f"{_KOMSU}{j}")
                  for j, g in self.komsular.uyandirmalar(t)]
        for h in sorted(self.alanlar.alanlar):
            niyet += self._kur(_ALAN, h, self.alanlar.son_tarih(h), t)
        for h in sorted(self.edinim._oturum):
            niyet += self._kur(_EDINIM, h, self.edinim.son_tarih(h), t)
        beyan, self._beyanlar = tuple(self._beyanlar), []
        return tuple(niyet) + beyan

    def _kur(self, onek: str, h: int, son: float | None, t: float) -> list:
        """Anahtar başına tekrarsız uyandırma (komşu tablosuyla aynı kural)."""
        planli = self._planli.get((onek, h))
        if son is None or (planli is not None
                           and planli <= son + ZAMAN_PAYI_S):
            return []
        self._planli[(onek, h)] = son
        return [Uyandirma(max(son - t, ZAMAN_PAYI_S), f"{onek}{h}")]

    def _uyandi_planli(self, onek: str, h: int, t: float) -> None:
        if self._planli.get((onek, h), float("inf")) <= t + ZAMAN_PAYI_S:
            del self._planli[(onek, h)]

    # ==================================================================
    # KANCALAR — veri
    # ==================================================================
    def sonraki_atlama(self, gozlem: Gozlem) -> Karar:
        """Ardıla ilet · REPAIRING'de kota içinde tampona al · aksi hâlde
        düşür."""
        t = float(gozlem.saat_s)
        p = gozlem.paket
        ek: tuple = ()
        durum = None if p is None else self.alanlar.durum(p.hedef)
        # `23` §7: hedefi geçit olmayan DATA yerel politika hatasıdır (C).
        sink_disi = (p is not None and p.hedef != self.sink
                     and not self.komut_alanlari)
        if p is not None and not sink_disi \
                and self.alanlar.ardil(p.hedef) is None \
                and durum != REPAIRING and p.kaynak == self.kimlik \
                and (durum is None or self.bayraklar.yeniden_edinim):
            # K-152 §2 — kendi paketim, alan ulaşılamaz ya da yok. Hiç
            # bilinmeyen hedefin İLK edinimi bayrakla kapanmaz (K-159).
            eylem = self.edinim.yeniden_edinim(p.hedef, t)
            if eylem:
                self._sayac["edinim_ilk" if durum is None
                            else "edinim_yeniden"] += 1
            ek = tuple(self._edinim_eylemleri(eylem, t))
        niyet = self._niyetler((), t, ek)
        beyan = tuple(n for n in niyet if isinstance(n, Beyan))
        niyet = tuple(n for n in niyet if not isinstance(n, Beyan))
        if p is None:
            return Karar(beyan=beyan, niyetler=niyet)
        if sink_disi and self.secenekler.komut_ters_yol:
            return self._komut_ilet(p, t, beyan, niyet)
        if sink_disi:
            # v0.1 geçit dışı hedefi BİLEREK taşımaz (K-160 §10 C): düşme
            # sebebi `politika`, `hedef_yok` değil (K-171 — eskiden beyansız
            # düşüştü ve "rota bulunamadı" ile aynı sayıya karışıyordu).
            self._sayac["veri_sink_disi"] += 1
            return Karar(beyan=beyan + (Beyan("politika"),), niyetler=niyet)
        # `23` §7: Hop Limit 16'dan başlar ve her atlamada azalır; ≤ 1 → bırak.
        if H_DATA - p.atlama_sayisi <= 1:
            self._sayac["veri_hop_siniri"] += 1
            return Karar(beyan=beyan, niyetler=niyet)
        j = self.alanlar.ardil(p.hedef)
        if j is not None and self._aktif_mi(j):
            self._sayac["veri_iletilen"] += 1
            return Karar(sonraki=j, beyan=beyan, niyetler=niyet)
        if self.alanlar.durum(p.hedef) == REPAIRING \
                and self.bayraklar.onarim_tamponu:
            if self._tampona_al(p.hedef, (p.kaynak, p.kaynak_sira)):
                self._sayac["veri_bekletilen"] += 1
                return Karar(beklet=True, beyan=beyan, niyetler=niyet)
        else:
            self._sayac["veri_ardilsiz"] += 1
        if self.alanlar.durum(p.hedef) is not None:
            beyan += (Beyan("rota_gecersiz", komsu=p.hedef),)
        return Karar(beyan=beyan, niyetler=niyet)

    # ==================================================================
    # V11 — KOMUT GERİ İZİ (K-172)
    # ==================================================================
    def _cerceve_duyuldu(self, gozlem: Gozlem, gonderen: int, tur: str,
                         hedef: int | None, rssi_dbm: int, paket) -> None:
        """`v2/15` B1 kancası — yalnız bana adreslenen, geçide giden DATA.

        🔒 İz yalnız DAHA YENİ `kaynak_sira` ile güncellenir. Böylece izden
        izle ilerleyen her adımda sıra azalmaz; bir döngü ancak AYNI paketin
        yolunda olabilir, o yol da ardıl alanında döngüsüzdür (`36` §3.3).
        Sırasız güncelleme, çapraz iki paketle iki düğümü birbirine
        gösterebilirdi.
        """
        if tur != "veri" or hedef != self.kimlik or paket is None \
                or paket.hedef != self.sink or paket.kaynak == self.kimlik:
            return None
        eski = self._geri_iz.get(paket.kaynak)
        if eski is not None and paket.kaynak_sira <= eski[1]:
            return None
        self._geri_iz[paket.kaynak] = (gonderen, paket.kaynak_sira,
                                       float(gozlem.saat_s))
        self._sayac["geri_iz_ogrenilen"] += 1
        return None

    def _komut_ilet(self, p, t: float, beyan: tuple, niyet: tuple) -> Karar:
        """Geçit dışı hedef (komut): hedefin geri izinin komşusuna.

        İz yoksa ya da `T_GERI_IZ_S`den eskiyse düşer — beyansız, yani
        `hedef_yok`: rota bilinmiyor. Hop Limit veri yolundakiyle aynı.
        """
        if H_DATA - p.atlama_sayisi <= 1:
            self._sayac["veri_hop_siniri"] += 1
            return Karar(beyan=beyan, niyetler=niyet)
        iz = self._geri_iz.get(p.hedef)
        if iz is None or t - iz[2] > T_GERI_IZ_S:
            self._sayac["komut_izsiz"] += 1
            return Karar(beyan=beyan, niyetler=niyet)
        self._sayac["komut_iz_iletilen"] += 1
        return Karar(sonraki=iz[0], beyan=beyan, niyetler=niyet)

    def _geri_izi_sil(self, komsu: int) -> None:
        """MAC `komsu`dan vazgeçti: o komşuya giden bütün izler bayat."""
        for kaynak in [k for k, v in self._geri_iz.items() if v[0] == komsu]:
            del self._geri_iz[kaynak]
            self._sayac["geri_iz_silinen"] += 1

    def _tampona_al(self, h: int, veri_kimligi: tuple[int, int]) -> bool:
        """`21` §2.4 alan kotası. Kümede olan paket yeniden sorulmuştur: yine
        bekler, yeniden sayılmaz. Kota doluysa YENİ paket düşer."""
        kume = self._tutulan.setdefault(h, set())
        if veri_kimligi in kume:
            return True
        if len(kume) >= self._kota:
            self._sayac["tampon_kota_disi"] += 1
            return False
        kume.add(veri_kimligi)
        self._sayac["tampon_alinan"] += 1
        self._sayac["tampon_tepe"] = max(self._sayac["tampon_tepe"], len(kume))
        return True

    def beacon_yuku(self, gozlem: Gozlem) -> dict:
        return {}

    def beacon_alindi(self, gozlem: Gozlem, komsu: int, yuk) -> None:
        return None

    # ==================================================================
    # KANCALAR — kontrol düzlemi
    # ==================================================================
    def zamanlayicilar(self) -> dict:
        # `metrik`: M0.1 epoch (`35` §3.2) · `ilan`: alan tazeleme (`21` §2.2).
        return {"metrik": T_EPOCH_S, "ilan": T_ADV_REFRESH_S}

    def zamanlayici_doldu(self, gozlem: Gozlem, etiket: str) -> tuple:
        t = float(gozlem.saat_s)
        self._komsu_olaylari(t)
        ek: tuple = ()
        if etiket == "metrik":
            self.komsular.epoch(t)
            self._terim_sayaci()
            # `35` §6: maliyet bandı değişince ilgili alanlar yeniden hesaplanır.
            self.alanlar.hepsini_hesapla(t)
            for r in [r for r, son in self._istek_gorulen.items() if son <= t]:
                del self._istek_gorulen[r]
            # V5a: ömrü kesin dolmuş saklı ilan atılır (bellek sınırı).
            for j in [j for j, s in self._saklanan.items()
                      if t - s[6] >= L_ADV_MAX_S]:
                del self._saklanan[j]
                self._sayac["saklanan_eskidi"] += 1
        elif etiket == "ilan":
            ek = tuple(m for h in sorted(self.alanlar.alanlar)
                       if (m := self._alan_ilani(h, tetik=False)) is not None)
        return self._niyetler((), t, ek, politika=(
            etiket == "metrik" and self.bayraklar.postur))

    def _terim_sayaci(self) -> None:
        """K-159: maliyet terimi bu epochta kaç ACTIVE komşuda UYGULANDI."""
        b = self.bayraklar
        for j in self.komsular.aktifler():
            o = self.komsular.kayit(j).son_olcum
            if o is None or o.q is None:
                continue
            if b.risk_maliyeti and c_risk(o.r) > 0:
                self._sayac["epoch_risk_cezali"] += 1
            if b.kalite_maliyeti and c_kalite(o.q) > 0:
                self._sayac["epoch_kalite_cezali"] += 1

    def uyandi(self, gozlem: Gozlem, etiket: str) -> tuple:
        t = float(gozlem.saat_s)
        self._komsu_olaylari(t)
        probelar: list = []
        ek: list = []
        if etiket.startswith(_KOMSU):
            probelar = self.komsular.zaman(int(etiket[len(_KOMSU):]), t)
        elif etiket.startswith(_ALAN):
            h = int(etiket[len(_ALAN):])
            self._uyandi_planli(_ALAN, h, t)
            self.alanlar.zaman(h, t, ZAMAN_PAYI_S)
        elif etiket.startswith(_EDINIM):
            h = int(etiket[len(_EDINIM):])
            self._uyandi_planli(_EDINIM, h, t)
            gerekli = self.alanlar.durum(h) != FORWARDABLE
            ek = self._edinim_eylemleri(
                self.edinim.zaman(h, t, ZAMAN_PAYI_S, gerekli), t)
        elif etiket.startswith(_ILAN):
            h = int(etiket[len(_ILAN):])
            m = self._alan_ilani(h, tetik=True)
            if m is not None:
                self.alanlar.tetik_gonderildi(h, t)
                ek = [m]
        return self._niyetler(probelar, t, tuple(ek))

    def kontrol_alindi(self, gozlem: Gozlem, gonderen: int, bicim: str,
                       yuk, yayin: bool) -> tuple:
        t = float(gozlem.saat_s)
        y = dict(yuk)
        # Pasif duyma → aday (K-154). Kanıt DEĞİL. V5 (K-163): yalnız
        # uygulanabilir bir ilanın sahibi nitelendirilir.
        if not self.secenekler.ihtiyac_nitelik or self._nitelige_deger(bicim, y):
            probelar = self.komsular.aday(gonderen, t)
            if probelar and bicim == FIELD_SOLICIT.ad \
                    and self.secenekler.ihtiyac_nitelik:
                self._sayac["soru_nitelik"] += 1         # V9 (K-167)
        else:
            probelar = []
            if self.komsular.kayit(gonderen) is None:
                self._sayac["nitelik_ertelendi"] += 1
        ek: list = []
        ben = tel_kimligi(self.kimlik)
        if y.get("gonderen") != tel_kimligi(gonderen):
            return self._niyetler(probelar, t)       # biçim ↔ bağ çelişkisi
        if bicim == PROBE.ad and y["hedef_komsu"] == ben:
            self._sayac["probe_alinan"] += 1
            self._tanidik[gonderen] = t                  # V8: `23` §2
            if (not self.secenekler.yanit_yalniz_onaysiz
                    or y["probe_bayraklar"] & PROBE_YANIT_ISTE):
                ek = [self._probe_yaniti(gonderen, y)]
            else:
                self._sayac["probe_yanitsiz"] += 1   # V1: MAC onayı yeter
        elif bicim == PROBE_REPLY.ad and y["asil_isteyen"] == ben:
            self.komsular.probe_yaniti(gonderen, y["probe_sira"], t)
        elif bicim == FIELD_UPDATE.ad and y["hop_siniri"] == 1 \
                and y["oiid"] == _ORNEK:
            self._sayac["ilan_alinan"] += 1
            self._komsu_olaylari(t)
            if (self.secenekler.ilan_sakla and not self._aktif_mi(gonderen)
                    and self._nitelige_deger(bicim, y)):
                # V5a: reddedilecekti — sakla, ACTIVE olunca uygula.
                self._saklanan[gonderen] = (
                    y["hedef"] - 1, y["dfsn"], y["ads"], y["durum"],
                    y["potansiyel"], y["omur"], t)
                self._sayac["ilan_saklandi"] += 1
            else:
                self.alanlar.ilan_al(gonderen, y["hedef"] - 1, y["dfsn"],
                                     y["ads"], y["durum"], y["potansiyel"],
                                     y["omur"], t)
        elif bicim == FIELD_SOLICIT.ad and y["hop_siniri"] == 1:
            ek = self._solicit_al(gonderen, y)
        elif bicim == DFSN_REQUEST.ad:
            ek = self._istek_al(gonderen, y, t)
        return self._niyetler(probelar, t, tuple(ek))

    def _nitelige_deger(self, bicim: str, y: dict) -> bool:
        """K-163 V5: bu çerçevenin sahibi bizim için UYGULANABİLİR bir aday mı?
        Yalnız sonlu bir FIELD_UPDATE: alan ya da FD yoksa, ilan daha yeni bir
        turdansa, ya da aynı turda potansiyeli FD'nin altındaysa (`23` §4.2).
        V9 (K-167): iletilebilir alanımız varken gelen tek atlamalı
        FIELD_SOLICIT de — soran bir alan istiyor, yanıt ACTIVE ister.
        V10 (K-167): alanımız iletilebilir değilken aynı turdan her sonlu
        ilan — yeni turdan sonra ardıl adayı; açlık onsuz görünmez."""
        if bicim == FIELD_SOLICIT.ad:
            return (self.secenekler.soru_nitelik and y.get("hop_siniri") == 1
                    and self.alanlar.durum(y["hedef"] - 1) == FORWARDABLE)
        if bicim != FIELD_UPDATE.ad or y.get("durum") != DURUM_REACHABLE \
                or y.get("potansiyel", SONSUZ) >= SONSUZ:
            return False
        a = self.alanlar.alanlar.get(y["hedef"] - 1)
        if a is None:
            return True
        if a.kendi:
            return False
        if a.fd is None or a.dfsn is None \
                or seri_karsilastir(y["dfsn"], a.dfsn) == YENI:
            return True
        if y["dfsn"] != a.dfsn:
            return False
        if self.secenekler.aclik_nitelik and a.durum != FORWARDABLE:
            return True      # V10 (K-167): yeni turdan sonra ardıl adayı
        return y["potansiyel"] < a.fd[1]

    def iletim_basarisiz(self, gozlem: Gozlem, hedef: int | None,
                         tur: str) -> tuple:
        t = float(gozlem.saat_s)
        if hedef is not None and self._geri_iz:
            self._geri_izi_sil(hedef)
        probelar = [] if hedef is None else self.komsular.bag_hatasi(hedef, t)
        return self._niyetler(probelar, t)

    def iletim_sonucu(self, gozlem: Gozlem, hedef: int, basarili: bool,
                      tekrar: int, tur: str) -> None:
        """K-151 Y1 — MAC'in her unicast sonucu. NİYET DÖNDÜRMEZ.

        Başarı ileri yönlü kanıttır (`23` §3.1); ACTIVE komşuya giden her
        sonuç M0.1'e bir örnektir. Doğan komşu değişimi, niyet döndürebilen
        ilk kancada alanlara verilir.
        """
        self.komsular.sonuc(hedef, float(gozlem.saat_s), basarili, tekrar)

    # ==================================================================
    # EDİNİM — FIELD_SOLICIT · DFSN_REQUEST (`23` §5)
    # ==================================================================
    def _edinim_eylemleri(self, eylemler: list[EdinimEylemi],
                          t: float) -> list:
        cikti: list = []
        for e in eylemler:
            if e.tur == "solicit":
                cikti.append(self._solicit(e.hedef))
            elif e.tur == "istek":
                cikti.append(self._istek(e.hedef, e.sira, t))
            elif e.tur == "bitti":
                self.alanlar.ulasilamaz_yap(e.hedef)
        return cikti

    def _baglam(self, h: int) -> tuple[int, int]:
        """(HAS_CONTEXT, bilinen DFSN) — alan ve turu biliniyorsa."""
        a = self.alanlar.alanlar.get(h)
        if a is None or a.dfsn is None:
            return 0, 0
        return BAYRAK_BAGLAM, a.dfsn

    def _solicit(self, h: int) -> KontrolIstegi:
        """`19` §7 — tek atlamalı YAYIN (`18` §5.2: alıcı tek-atlama komşular)."""
        baglam, dfsn = self._baglam(h)
        yuk = self._baslik(FIELD_SOLICIT, TIP_FIELD_SOLICIT, self._sira_al())
        yuk.update(hedef=tel_kimligi(h), bilinen_oiid=_ORNEK if baglam else 0,
                   bilinen_dfsn=dfsn, sbayraklar=baglam, solicit_ayrilmis=0)
        self._sayac["solicit_gonderilen"] += 1
        return KontrolIstegi.kur(None, FIELD_SOLICIT, yuk,
                                 jitter_s=J_CONTROL_S)

    def _istek(self, h: int, sira: int, t: float) -> KontrolIstegi:
        """Yeni bir dalga — neden DALGA ANINDA alandan (K-156)."""
        baglam, dfsn = self._baglam(h)
        sebep = (SEBEP_ACLIK if baglam and self.alanlar.aclik_mi(h, t)
                 else SEBEP_EDINIM)
        istek = {"isteyen": tel_kimligi(self.kimlik), "isteyen_ornek": _ORNEK,
                 "istek_sira": sira, "istek_ayrilmis": 0,
                 "hedef": tel_kimligi(h),
                 "bilinen_oiid": _ORNEK if baglam else 0,
                 "istenen_en_az_dfsn": (dfsn + 1) & _ALAN_32 if baglam else 0,
                 "sebep": sebep, "rbayraklar": baglam, "istek_ayrilmis2": 0}
        self._istek_gorulen[(istek["isteyen"], _ORNEK, sira)] = (
            t + T_REQ_DUPLICATE_S)
        self._sayac["istek_gonderilen"] += 1
        if sebep == SEBEP_ACLIK:
            self._sayac["istek_aclik"] += 1              # K-167 teşhis
        return self._istek_cercevesi(istek, H_REQ)

    def _istek_cercevesi(self, istek: dict, hop: int) -> KontrolIstegi:
        yuk = self._baslik(DFSN_REQUEST, TIP_DFSN_REQUEST, self._sira_al())
        yuk.update(istek)
        yuk["hop_siniri"] = hop
        return KontrolIstegi.kur(None, DFSN_REQUEST, yuk, jitter_s=J_CONTROL_S)

    def _solicit_al(self, gonderen: int, y: dict) -> list:
        """`23` §5.2 — ACTIVE komşuya güncel ilanı BİR kez, tek alıcılı."""
        if not self._aktif_mi(gonderen):
            return []
        if y["sbayraklar"] & BAYRAK_BAGLAM and y["bilinen_oiid"] != _ORNEK:
            return []
        m = self._alan_yaniti(y["hedef"] - 1, gonderen)
        if m is None:
            return []
        self._sayac["solicit_yanitlanan"] += 1
        return [m]

    def _istek_al(self, gonderen: int, y: dict, t: float) -> list:
        """`23` §5.3 — tekrar bastırma, hedefte işleme, yanıt ve iletme."""
        if not self._aktif_mi(gonderen):
            if not (self.secenekler.istek_tanidik
                    and gonderen in self._tanidik):
                self._sayac["istek_aktif_disi"] += 1  # K-150 §4: kabul kapısı
                return []
            self._sayac["istek_tanidik_kabul"] += 1   # V8 (K-167): `23` §2
        rid = (y["isteyen"], y["isteyen_ornek"], y["istek_sira"])
        if self._istek_gorulen.get(rid, float("-inf")) > t:
            self._sayac["istek_tekrar"] += 1
            return []
        self._istek_gorulen[rid] = t + T_REQ_DUPLICATE_S
        h = y["hedef"] - 1
        if h == self.kimlik:
            self._hedefte(y, t)
            return []
        cikti: list = []
        a = self.alanlar.alanlar.get(h)
        if a is not None and a.durum == FORWARDABLE and (
                not y["rbayraklar"] & BAYRAK_BAGLAM
                or seri_karsilastir(a.dfsn, y["istenen_en_az_dfsn"])
                in (YENI, ESIT)):
            m = self._alan_yaniti(h, gonderen)
            if m is not None:
                self._sayac["istek_yanitlanan"] += 1
                cikti.append(m)
        if y["hop_siniri"] > 1:
            istek = {k: y[k] for k, _ in DFSN_REQUEST.alanlar[9:]}
            cikti.append(self._istek_cercevesi(istek, y["hop_siniri"] - 1))
            self._sayac["istek_iletilen"] += 1
        return cikti

    def _hedefte(self, y: dict, t: float) -> None:
        """`23` §5.4 `HandleAtTarget` — öğrencinin onaylı dar yetkisi."""
        self._sayac["hedefte_istek"] += 1
        if y["sebep"] == SEBEP_ACLIK:
            self._sayac["hedefte_aclik"] += 1            # K-167 teşhis
        h = self.kimlik
        if h not in self.alanlar.alanlar:
            if not self.komut_alanlari:
                return                  # C: geçit dışında alan açılmaz
            # K-150 §4 A: komut alacak düğüm kendi alanını İLK istekte üretir.
            self.alanlar.kendi_alani(h, dfsn=1)
            self._sayac["hedef_alani_acildi"] += 1
            self.alanlar.kaynak_ilani(h, t)
            return
        a = self.alanlar.alanlar[h]
        if not y["rbayraklar"] & BAYRAK_BAGLAM or y["bilinen_oiid"] != _ORNEK:
            return self.alanlar.kaynak_ilani(h, t)
        bilinen = (y["istenen_en_az_dfsn"] - 1) & _ALAN_32
        kiyas = seri_karsilastir(a.dfsn, bilinen)
        if kiyas == YENI:
            return self.alanlar.kaynak_ilani(h, t)
        if kiyas != ESIT:
            return None                              # eski ya da belirsiz
        if y["sebep"] != SEBEP_ACLIK:
            return self.alanlar.kaynak_ilani(h, t)
        self.alanlar.tur_artir(h, t)                 # tek artış, ilanla

    # ==================================================================
    # MESAJLAR
    # ==================================================================
    def _baslik(self, bicim, tip: int, sira: int) -> dict:
        """Taban başlık (`19` §2) + Kontrol Gönderen Bloğu (§5)."""
        return {"surum": SURUM, "tip": tip,
                "baslik_uzunlugu": bicim.bayt({}), "hop_siniri": 1,
                "taban_bayraklari": 0, "gonderen": tel_kimligi(self.kimlik),
                "gonderen_ornek": _ORNEK, "mesaj_sira": sira,
                "gonderen_ayrilmis": 0}

    def _probe(self, p: ProbeIstegi) -> KontrolIstegi:
        yuk = self._baslik(PROBE, TIP_PROBE, p.sira)
        # V1 (K-163): yanıt yalnız ilk deneme MAC onayıyla kanıtlanmadıysa.
        iste = (PROBE_YANIT_ISTE if self.secenekler.yanit_yalniz_onaysiz
                and p.deneme >= 2 else 0)
        yuk.update(hedef_komsu=tel_kimligi(p.komsu), probe_bayraklar=iste,
                   probe_ayrilmis=0)
        return KontrolIstegi.kur(p.komsu, PROBE, yuk, jitter_s=p.jitter_s)

    def _probe_yaniti(self, gonderen: int, y: dict) -> KontrolIstegi:
        yuk = self._baslik(PROBE_REPLY, TIP_PROBE_REPLY, self._sira_al())
        yuk.update(asil_isteyen=y["gonderen"],
                   asil_isteyen_ornek=y["gonderen_ornek"],
                   probe_sira=y["mesaj_sira"], yanit_ayrilmis=0)
        self._sayac["probe_yaniti_gonderilen"] += 1
        return KontrolIstegi.kur(gonderen, PROBE_REPLY, yuk)

    def _field_update(self, h: int, icerik: tuple, hedef: int | None,
                      jitter_s: float) -> KontrolIstegi:
        dfsn, ads, durum, potansiyel = icerik
        yuk = self._baslik(FIELD_UPDATE, TIP_FIELD_UPDATE, self._sira_al())
        yuk.update(hedef=tel_kimligi(h), oiid=_ORNEK, dfsn=dfsn, ads=ads,
                   potansiyel=potansiyel,
                   omur=L_ADV_SENT_KUANTA if durum == DURUM_REACHABLE else 0,
                   durum=durum, alan_bayraklari=0)
        self._sayac["ilan_gonderilen"] += 1
        return KontrolIstegi.kur(hedef, FIELD_UPDATE, yuk, jitter_s=jitter_s)

    def _alan_ilani(self, h: int, tetik: bool) -> KontrolIstegi | None:
        """FIELD_UPDATE yayını — içerik GÖNDERİM anında alandan okunur."""
        icerik = self.alanlar.ilan_icerigi(h, tetik)
        if icerik is None:
            return None
        return self._field_update(h, icerik, None,
                                  0.0 if tetik else J_ADV_S)

    def _alan_yaniti(self, h: int, j: int) -> KontrolIstegi | None:
        """Tek alıcılı FIELD_UPDATE (`23` §5.2 *"once to j"*, K-150)."""
        icerik = self.alanlar.yanit_icerigi(h)
        if icerik is None:
            return None
        return self._field_update(h, icerik, j, 0.0)

    # ==================================================================
    # KİMLİK — koşu kimliğine giren parametreler (K-171, `v2/15` A1)
    # ==================================================================
    def kimlik_parametreleri(self) -> dict:
        """Davranışı değiştiren kurucu değerleri — düğümden bağımsız olanlar.

        🔒 Bayrak ya da seçenek demeti farklı iki koşu artık aynı kimliği
        taşımaz; eskiden yalnız `teshis`te görünüyordu, kimliğe girmiyordu.
        """
        return {"sink": self.sink, "tampon_kotasi": self._kota,
                "bayraklar": self.bayraklar, "secenekler": self.secenekler,
                "komut_alanlari": self.komut_alanlari}

    # ==================================================================
    # TEŞHİS — yalnız sonuç satırına (en çok 32 alan; gruplar ad + değer)
    # ==================================================================
    def teshis(self, dugum: int) -> dict:
        # 🔒 K-159: düğümün GERÇEKTEN kullandığı ablasyon bayrakları satırda.
        cikti: dict = {"komsu_active": len(self.komsular.aktifler()),
                       "bayraklar_adlari": Bayraklar.adlar(),
                       "bayraklar": self.bayraklar.degerler(),
                       "secenekler_adlari": Secenekler.adlar(),
                       "secenekler": self.secenekler.degerler(),
                       "komut_alanlari": self.komut_alanlari}
        for ad, sayac in (("protokol", self._sayac),
                          ("komsu", self.komsular.sayac),
                          ("alan", self.alanlar.sayac),
                          ("edinim", self.edinim.sayac),
                          ("politika", self.politika.sayac)):
            cikti[f"{ad}_adlari"] = tuple(sayac)
            cikti[f"{ad}_sayac"] = tuple(sayac.values())
        return cikti
