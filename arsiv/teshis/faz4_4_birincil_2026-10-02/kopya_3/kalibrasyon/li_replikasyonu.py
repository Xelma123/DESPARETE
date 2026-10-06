"""
Lİ vd. REPLİKASYONU — aletin TEK dış çapası.

Üretici:
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/li_replikasyonu.py

Ön-kayıt: `v2/09-LI-REPLIKASYONU.md` — ÖLÇÜMDEN ÖNCE yazıldı.
Kaynak: `02-DOGRULANMIS-KAYNAKLAR.md` A5b ✅
Şartname: `07-SIMULATOR-TASARIMI.md` §10, seviye 3.

🔴 NEDEN BU ÖLÇÜM HER ŞEYDEN ÖNEMLİ
===================================
Bugüne kadarki bütün doğrulama İÇ TUTARLILIKTIR. Bianchi doğrulaması MAC'i
**tek çarpışma alanında** sınıyor; bu projenin ölçtüğü şey ise **çok
atlamalı** teslim. Aradaki boşluk — uzamsal yeniden kullanım, kendi kendine
girişim, zincir boyunca çarpışma — hiç sınanmadı. Bir alet kendi içinde
tutarlı ve tamamen yanlış olabilir.

🔒 REPLİKE EDİLEN: uzun bir zincirde uçtan uca verim, tek atlamanın **1/7**'si
(802.11 temel erişim). İdeal MAC'te 1/4 olurdu; aradaki fark 802.11'in kendi
verimsizliğidir.

🔒 ZİNCİR BİR DENEY KOLU DEĞİL, ÖLÇÜM ALETİDİR — kâhinlerle aynı gerekçe.
`senaryolar.py` büyümez, ön-kayıtta bir aile değildir. Kendi dünyasını
burada kurar.

🔒 FAZ 4 (K-183) — `--dunya referans_2026`: aynı düzenek referans dünyanın
telsiziyle (1:1, işlem kazancı, güç kipi taşıyıcı dinleme, ARF, yayılım
gecikmesi). Aralık yine `iletim_menzili_m` (referansta 10 dB paylı nominal
bağ, 1664 m); duyma kümesi kurulumla TEK türetimden (`duyma_turetimi`).

🔴 KANALDA HİÇBİR ŞEY DEĞİŞMEZ. Aynı yayılım, aynı MAC, aynı girişim, aynı
gölgeleme ve sönümleme. Zincir için ayarlanmış bir kanal hiçbir şey
doğrulamaz — sınanan şey, deneyde kullanılan aletin ta kendisidir.
"""

from __future__ import annotations

import statistics as ist
import sys
import time
from dataclasses import dataclass
from multiprocessing import Pool
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.ag.kuyruk import Kuyruk  # noqa: E402
from sim2.ag.paket import Paket, PaketSayaci  # noqa: E402
from sim2.ag.trafik import Akis, Dogum  # noqa: E402
from sim2.cekirdek.korunum import KorunumDefteri  # noqa: E402
from sim2.cekirdek.olaylar import OlayKuyrugu  # noqa: E402
from sim2.cekirdek.rng import Akislar  # noqa: E402
from sim2.cekirdek.saat import Saatler  # noqa: E402
from sim2.cekirdek.sayaclar import Sayaclar  # noqa: E402
from sim2.dunya.geometri import Nokta3  # noqa: E402
from sim2.dunya.mobilite import Sabit  # noqa: E402
from sim2.dunya.topoloji import Topoloji  # noqa: E402
from sim2.gozlem.karar import Karar  # noqa: E402
from sim2.kanal.cerceve import cerceve_kur  # noqa: E402
from sim2.kanal.kanal import Kanal  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kayip import olum_anlari  # noqa: E402
from sim2.kosum.kurulum import Kurulum, duyma_turetimi  # noqa: E402
from sim2.mac.dcf import DcfZamanlari  # noqa: E402
from sim2.olcum.kayip_yeri import KayipYeri  # noqa: E402
from sim2.olcum.paket_defteri import PaketDefteri  # noqa: E402
from sim2.olcum.rota_olaylari import RotaDefteri  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402
from kalibrasyon import dunya_secimi as DS  # noqa: E402

# 🔒 ÖN-KAYITLI BAND — `09-LI-REPLIKASYONU.md` §04, ölçümden ÖNCE ilan
# edildi ve sonradan genişletilmeyecek.
HEDEF_ORAN = 1.0 / 7.0
BAND = (0.10, 0.20)
IDEAL_MAC_TAVANI = 0.25          # Li L2 — uzamsal yeniden kullanım tavanı

TOHUMLAR = (1000, 1001, 1002, 1003, 1004)

# 🔒 TEMİZ KANAL — gerekçesi `09` §03.1b, ölçülerek varıldı.
# Li'nin kurulumunda ne gölgeleme ne sönümleme var. Açık bırakıldığında
# statik koldaki DONMUŞ Rician çekimi bağların %2-6'sını tamamen öldürüyor
# ve zincirin beşte biri tek bir ölü bağ yüzünden SIFIR teslim ediyor —
# yani ölçülen şey MAC verimliliği değil, bağ kesintisi olurdu.
# ⚠️ Bedeli: replikasyon kanalın TAMAMINI değil, MAC + girişim + uzamsal
# yeniden kullanımı doğrular. Bu beyan edilir.
TEMIZ_KANAL = dict(golgeleme_acik=False, sonumleme_acik=False)


# ==========================================================================
class ZincirYonlendirici:
    """Sonraki atlama = hedefe doğru KOMŞU. Kâhin değil, DOĞRU rota.

    🔒 Zincirde yönlendirme diye bir sorun yoktur: tek bir rota vardır ve
    hepsi onu bilir. Bu yüzden burada ölçülen şey yönlendirmenin değil,
    MAC + girişim + uzamsal yeniden kullanımın davranışıdır.
    """

    ad = "zincir"
    __slots__ = ("kimlik",)

    def __init__(self, kimlik: int) -> None:
        self.kimlik = kimlik

    def sonraki_atlama(self, gozlem) -> Karar:
        if gozlem.paket is None:
            return Karar()
        hedef = gozlem.paket.hedef
        if hedef == self.kimlik:
            return Karar()
        return Karar(sonraki=self.kimlik + (1 if hedef > self.kimlik else -1))

    def beacon_yuku(self, gozlem) -> dict:
        return {}

    def beacon_alindi(self, gozlem, komsu, yuk) -> None:
        return None

    def teshis(self, dugum: int) -> dict:
        return {}


@dataclass(frozen=True, slots=True)
class ZincirTrafik:
    """Tek akış, `0 → N−1`, doygun. `TrafikUreteci`nin yerine geçer.

    🔒 Aynı yüzey: `cizelge` · `toplam_dogum` · `akis(kimlik)`. Kalıtım yok —
    `sim2/`ye bir "zincir" kavramı sızmasın diye.
    """

    _cizelge: tuple[Dogum, ...]
    _akis: Akis
    _paket_bayt: int
    _ttl: int
    _olcum_bitis_s: float
    _pencere: tuple[float, float]

    @property
    def cizelge(self) -> tuple[Dogum, ...]:
        return self._cizelge

    @property
    def toplam_dogum(self) -> int:
        return len(self._cizelge)

    def akis(self, kimlik: int) -> Akis:
        return self._akis

    def paket_kur(self, dogum: Dogum, sayac) -> Paket:
        return Paket(kimlik=sayac.yeni(), akis_kimligi=self._akis.kimlik,
                     kaynak=self._akis.kaynak, hedef=self._akis.hedef,
                     dogum_s=dogum.t_s, boyut_bayt=self._paket_bayt,
                     ttl_kalan=self._ttl)

    def sunulan_hiz_hz(self) -> float:
        if self._olcum_bitis_s <= 0.0:
            return 0.0
        return self.toplam_dogum / self._olcum_bitis_s

    def penceredeki_dogum(self) -> int:
        bas, bitis = self._pencere
        return sum(1 for d in self._cizelge if bas <= d.t_s < bitis)


def zincir_kurulumu(n: int, aralik_m: float, tohum: int, yuk_hz: float,
                    bitis_s: float, duyma_m: float | None = None,
                    **ek) -> Kurulum:
    """N düğümlü düz zincir; tek doygun akış `0 → N−1`."""
    kfg = DS.konfig(kol="li", senaryo="statik-yok", tohum=tohum,
                 dugum_sayisi=n, akis_sayisi=1,
                 # 🔒 Mufreze sayisi dugum sayisini asamaz (Konfig kapisi).
                 # Statik zincirde mobilite yok, deger davranisa girmiyor —
                 # ama gecerli olmak ZORUNDA ve bu kapi haklidir.
                 gorev_grup_sayisi=min(10, n),
                 isinma_s=0.2 * bitis_s, olcum_bitis_s=0.8 * bitis_s,
                 kosu_bitis_s=bitis_s, **ek)
    akislar = Akislar(tohum)
    irtifa = 0.5 * (kfg.irtifa_min_m + kfg.irtifa_maks_m)
    konumlar = tuple(Nokta3(i * aralik_m, 0.0, irtifa) for i in range(n))
    topoloji = Topoloji(mobilite=Sabit(konumlar), menzil_m=kfg.iletim_menzili_m,
                        dugum_sayisi=n)
    kanal = Kanal(kfg, topoloji)

    # Doygun CBR: kaynak her zaman gönderecek paket bulmalı.
    periyot = 1.0 / yuk_hz
    adet = int(kfg.olcum_bitis_s / periyot)
    akis = Akis(kimlik=0, kaynak=0, hedef=n - 1)
    cizelge = tuple(Dogum(k * periyot, 0) for k in range(adet))

    veri = cerceve_kur(kfg, "veri")
    onay = cerceve_kur(kfg, "onay")
    beacon = cerceve_kur(kfg, "beacon")
    r_faz = akislar["beacon_faz"]
    return Kurulum(
        konfig=kfg, akislar=akislar, topoloji=topoloji,
        saatler=Saatler(dugum_sayisi=n,
                        ofset_araligi_s=kfg.saat_ofset_araligi_s,
                        sapma_ppm=kfg.saat_sapma_ppm,
                        senkron=kfg.saat_senkron, akislar=akislar),
        kanal=kanal,
        trafik=ZincirTrafik(cizelge, akis, kfg.paket_bayt,
                            kfg.ttl_baslangic, kfg.olcum_bitis_s,
                            kfg.olcum_penceresi),
        olaylar=OlayKuyrugu(), sayaclar=Sayaclar(),
        korunum=KorunumDefteri(),
        paket_defteri=PaketDefteri(pencere_bas_s=kfg.olcum_penceresi[0],
                                   pencere_bitis_s=kfg.olcum_penceresi[1]),
        rota_defteri=RotaDefteri(), paket_sayaci=PaketSayaci(),
        kuyruklar=tuple(Kuyruk(kfg.kuyruk_kapasitesi) for _ in range(n)),
        beacon_fazlari=tuple(r_faz.uniform(0.0, kfg.beacon_araligi_s)
                             for _ in range(n)),
        veri_cercevesi=veri, onay_cercevesi=onay, beacon_cercevesi=beacon,
        zamanlar=DcfZamanlari.kur(kfg, veri, onay),
        # 🔴 KİM KİMİ DUYAR — varsayılan `girisim_menzili_m`dir ve BU BİR
        # TASARIM KARARIDIR, fizik değil: taşıyıcı dinleme eşiği GÜRÜLTÜ
        # TABANI seçilmiş. `duyma_m` bunu taramak için var (bölüm D).
        # 🔴 26 Eylül 2026 (K-183) — AYNI KUSUR İKİNCİ KEZ: A5/C1'in alanları
        # eksikti, zincir yine KURULAMIYORDU. Aşağıdaki "ifade aynı tutulur"
        # notu yetmedi, çünkü formül KOPYAYDI. Artık türetim kurulumla TEK
        # (`duyma_turetimi`) ve bir duman testi aracı her takımda kurar.
        **dict(zip(("duyanlar_menzili_m", "maks_gecikme_s"),
                   duyma_turetimi(kfg, beacon, duyma_m))),
        yayilim_gecikmeli=kfg.yayilim_gecikmesi,
        olum_anlari=olum_anlari(kfg),
        # 🔴 15 Eylül 2026'da EKLENDİ — bu alet bunsuz ÇÖKÜYORDU.
        # `Kurulum`a `kayip_yeri` bir yapı adımında eklendi; bu dosya
        # zincir topolojisini KENDİ kurduğu için imza değişikliğini
        # almadı ve 10 Eylül'den beri hiç koşulmadığı için kimse
        # görmedi. D1 doğrulama listesinin var oluş sebebi budur.
        # 🔒 İfade `kosum/kurulum.py`dekiyle AYNI tutulur; iki yerde
        # iki farklı kural yazmak, ayrışmayı davet etmek olurdu.
        kayip_yeri=(KayipYeri(kfg.iletim_menzili_m)
                    if kfg.yere_toplama else None))


def _kos(n: int, aralik_m: float, tohum: int, yuk_hz: float,
         bitis_s: float = 30.0, duyma_m: float | None = None, **ek):
    """Bir zincir koşusu → (verim pkt/s, PDR, kuyruk doluluk kanıtı)."""
    kur = zincir_kurulumu(n, aralik_m, tohum, yuk_hz, bitis_s,
                          duyma_m=duyma_m, **{**TEMIZ_KANAL, **ek})
    Kosu(kur, ZincirYonlendirici).kostur()
    d = kur.paket_defteri
    pencere = kur.konfig.olcum_penceresi
    sure = pencere[1] - pencere[0]
    teslim = d.pencerede_teslim
    uretilen = d.pencerede_uretilen
    return {"verim_hz": teslim / sure,
            "pdr": teslim / uretilen if uretilen else None,
            "uretilen": uretilen,
            "kuyruk_tasmasi": int(kur.sayaclar.oku("kuyruk_tasmasi"))}


def _is(gorev):
    try:
        n, aralik, tohum, yuk, bitis, *kuyruk = gorev
        duyma = kuyruk[0] if kuyruk else None
        return _kos(n, aralik, tohum, yuk, bitis, duyma_m=duyma), None
    except Exception as hata:                        # noqa: BLE001
        return None, f"{type(hata).__name__}: {hata}"


def _baslik(metin: str) -> None:
    print()
    print("=" * 88)
    print(metin)
    print("=" * 88)


# ==========================================================================
def a_aralik(isci: int = 8) -> float:
    """Düğüm aralığı — TÜRETİLİR, ve bir KAPIDAN geçer.

    🔒 Aralık = `iletim_menzili_m`, yani VERİCİ GÜCÜNÜN ÇAPASI. O mesafede
    girişimsiz SINR tam olarak eşiğe eşittir; böylece *"bir atlama = bir
    iletim menzili"* yapı gereği doğrudur ve zincir geometrisi Li'nin
    varsayımıyla (duyma menzili ≈ 2 × iletim menzili) örtüşür.

    🔴 İLK ÖLÇÜTÜM *"PDR ≥ 0,99 olan EN BÜYÜK aralık"* idi ve fiziği
    yanlıştı: i±2/i±3 girişimi bir artefakt değil, Li'nin ölçtüğü
    MEKANİZMADIR. Aralığı büyütmek onu zayıflatır ve oranı yapay olarak
    yükseltir. Ayrıntı `09` §03.1.

    🔒 Eski ölçüt KAPI olarak kalır: seçilen aralıkta zincirin HER bağı
    atlama başarısı ≥ 0,99 vermek zorunda. Kapı burada koşar.
    """
    from sim2.kanal.cerceve import cerceve_kur as _cer
    _baslik("A - DUGUM ARALIGI  (turetilmis: guc capasi; kapi: her bag >= 0,99)")
    n = 11
    aralik = DS.konfig(kol="li").iletim_menzili_m
    print(f"  aralik = iletim_menzili_m = {aralik:.0f} m  (turetilmis capa)")
    print()
    print(f"  {'kanal':<28} {'en kotu bag':>12} {'ortalama':>10} {'kapi':>8}")
    gecti = False
    for etiket, ek in (("golgeleme+sonumleme ACIK", {}),
                       ("TEMIZ (ikisi de kapali)", dict(TEMIZ_KANAL))):
        en_kotu, hepsi = 1.0, []
        for tohum in TOHUMLAR:
            kur = zincir_kurulumu(n, aralik, tohum, 0.2, 40.0, **ek)
            kanal = kur.kanal
            c, o = _cer(kur.konfig, "veri"), _cer(kur.konfig, "onay")
            d = kur.konfig.yeniden_deneme_siniri + 1
            for i in range(n - 1):
                p = ((1 - kanal.alim_per(i, i + 1, c, bas_s=10.0))
                     * (1 - kanal.alim_per(i + 1, i, o, bas_s=10.0)))
                at = 1 - (1 - p) ** d
                en_kotu = min(en_kotu, at)
                hepsi.append(at)
        ok = en_kotu >= 0.99
        if "TEMIZ" in etiket:
            gecti = ok
        print(f"  {etiket:<28} {en_kotu:>12.4f} {ist.mean(hepsi):>10.4f} "
              f"{'GECER' if ok else 'kalir':>8}")
    print()
    if not gecti:
        print("  🔴 TEMIZ KANALDA BILE KAPI GECILMEDI — replikasyon kosulamaz")
        return None
    print("  🟢 Kapi TEMIZ kanalda geciliyor; verdikt orada verilir.")
    print("  ⚠️ Acik kanaldaki en kotu bag ~0 — donmus derin Rician cekimi.")
    print("     Aletin bilinen ozelligi (K-096); Li'nin kurulumunda YOK.")
    return aralik


def b_zincir(aralik_m: float, isci: int = 8) -> dict:
    """Zincir uzunluğu taraması — TEK SAYI DEĞİL, EĞRİ.

    🔴 Tek bir N'de tek bir oran zayıf bir sınavdır; bir sayı tesadüfen
    tutabilir. Li'nin asıl iddiası bir ŞEKİLDİR: kullanım N ile düşer ve
    N ≳ 7'de düzleşir. Eğrinin kendisi raporlanır.

    🔒 DOYGUNLUK ÖLÇÜLEREK KURULUR: önce tek atlama kapasitesi çok yüksek
    bir yükle ölçülür, sonra bütün zincirler onun İKİ KATI yükle koşar.
    Kaynağın hiç boş kalmadığının kanıtı `kuyruk_tasmasi > 0`dır ve
    raporlanır — doygunluk bir varsayım değil, bir gözlemdir.
    """
    _baslik(f"B - ZINCIR UZUNLUGU  (aralik {aralik_m:.0f} m · "
            f"{len(TOHUMLAR)} tohum)")

    # --- doygunluk: once tek atlama kapasitesi -------------------------
    gorevler = [(2, aralik_m, t, 1200.0, 30.0) for t in TOHUMLAR]
    with Pool(isci) as havuz:
        ham = havuz.map(_is, gorevler, chunksize=1)
    tek = [s["verim_hz"] for s, h in ham if h is None]
    tasma = [s["kuyruk_tasmasi"] for s, h in ham if h is None]
    if not tek:
        print("  🔴 tek atlama kosumu basarisiz:", ham[0][1])
        return {}
    kapasite = ist.mean(tek)
    yuk = 2.0 * kapasite
    print(f"  tek atlama kapasitesi : {kapasite:.1f} pkt/s "
          f"(1200 Hz sunulan yukte)")
    print(f"  kuyruk tasmasi        : {ist.mean(tasma):.0f} — "
          f"{'DOYGUN' if min(tasma) > 0 else '🔴 DOYGUN DEGIL'}")
    print(f"  zincir taramasinda sunulan yuk: {yuk:.0f} pkt/s "
          f"(kapasitenin 2 kati)")
    print()

    # --- egri ----------------------------------------------------------
    uzunluklar = tuple(range(2, 12))
    gorevler = [(n, aralik_m, t, yuk, 30.0)
                for n in uzunluklar for t in TOHUMLAR]
    t0 = time.perf_counter()
    with Pool(isci) as havuz:
        ham = havuz.map(_is, gorevler, chunksize=1)
    print(f"  kosum suresi: {(time.perf_counter() - t0) / 60:.1f} dk")
    print()
    print(f"  {'dugum':>6} {'atlama':>7} {'verim_hz':>10} {'2SE':>8} "
          f"{'tek atlamaya oran':>18} {'doygun':>8}")
    egri: dict[int, float] = {}
    taban = None
    for k, n in enumerate(uzunluklar):
        dilim = ham[k * len(TOHUMLAR):(k + 1) * len(TOHUMLAR)]
        v = [s["verim_hz"] for s, h in dilim if h is None]
        t_ = [s["kuyruk_tasmasi"] for s, h in dilim if h is None]
        if not v:
            print(f"  {n:>6} {'—':>7} {'KOSMADI':>10}")
            continue
        ort = ist.mean(v)
        se = 2.0 * ist.stdev(v) / len(v) ** 0.5 if len(v) > 1 else 0.0
        if taban is None:
            taban = ort
        egri[n] = ort
        print(f"  {n:>6} {n - 1:>7} {ort:>10.2f} {se:>8.2f} "
              f"{ort / taban:>18.4f} "
              f"{'evet' if min(t_) > 0 else '🔴 HAYIR':>8}")
    return {"egri": egri, "kapasite": taban, "yuk": yuk}


def c_karar(sonuc: dict) -> bool:
    """🔴 ÖN-KAYITLI HİPOTEZLERE KARŞI KARAR — band SONRADAN genişletilmez."""
    _baslik("C - ON-KAYITLI HIPOTEZLER  (09-LI-REPLIKASYONU.md §04)")
    egri = sonuc.get("egri") or {}
    if len(egri) < 8:
        print("  🔴 egri eksik — karar verilemez")
        return False
    taban = egri[2]
    # Uzun zincir = N >= 8 (Li'nin duzlestigini soyledigi bolge).
    uzun = [egri[n] / taban for n in egri if n >= 8]
    oran = ist.mean(uzun)
    print(f"  H1 · uzun zincir / tek atlama : {oran:.4f}   "
          f"(hedef {HEDEF_ORAN:.4f} · band {BAND})")
    h1 = BAND[0] <= oran <= BAND[1]
    print(f"       {'🟢 TUTTU' if h1 else '🔴 TUTMADI'}")

    oranlar = [egri[n] / taban for n in sorted(egri)]
    dususler = all(b <= a * 1.02 for a, b in zip(oranlar, oranlar[1:]))
    son_uc = oranlar[-3:]
    duz = (max(son_uc) - min(son_uc)) <= 0.05
    print(f"  H2 · egri dusuyor mu           : "
          f"{'🟢 EVET' if dususler else '🔴 HAYIR'}")
    print(f"       N >= 9'da duzlesiyor mu   : "
          f"{'🟢 EVET' if duz else '🔴 HAYIR'}  "
          f"(son uc oran {', '.join(f'{o:.3f}' for o in son_uc)})")
    h3 = oran < IDEAL_MAC_TAVANI
    print(f"  H3 · ideal MAC tavaninin (1/4) altinda mi : "
          f"{'🟢 EVET' if h3 else '🔴 HAYIR — uzamsal yeniden kullanim FAZLA iyimser'}")

    hepsi = h1 and dususler and duz and h3
    print()
    print(f"  REPLIKASYON : {'🟢 TUTTU' if hepsi else '🔴 TUTMADI'}")
    if not hepsi:
        print("  🔴 Sartname §10: 'Tutmazsa MAC ya da girisim modelinde bir")
        print("     sey yanlistir ve BULMADAN DEVAM EDILMEZ.' Once")
        print("     `09` §04.1'deki ilan edilmis model farklarinin buyuklugu")
        print("     OLCULUR; hicbiri aciklamiyorsa kusur alettedir.")
    return hepsi


def d_duyma_menzili(aralik_m: float, isci: int = 8) -> None:
    """🔴 H1 NEDEN TUTMADI — hipotez kuruluyor ve SINANIYOR.

    Ölçülen eğri şunu söylüyor: `oran × atlama ≈ 0,7` ve N ≥ 5'ten sonra
    SABİT. Yani verim atlama sayısıyla TERS ORANTILI — **uzamsal yeniden
    kullanım YOK**. Li'nin 1/4'ü ise tam olarak uzamsal yeniden kullanımdan
    geliyor: 4 atlama ötedeki düğüm aynı anda konuşabilmeli.

    🔴 ŞÜPHE: `duyanlar_menzili_m` = `girisim_menzili_m` = 1 767 m, iletim
    menzilinin **6,3 katı**. Li'nin (ve tipik 802.11'in) varsayımı ~2 kat.
    280 m aralıkla 11 düğümlük zincir 2 800 m; yani neredeyse HER DÜĞÜM HER
    DÜĞÜMÜ DUYUYOR ve zincir tek bir çarpışma alanı hâline geliyor.

    🔒 SINAV: duyma menzili taranır. Şüphe doğruysa, oran 2 kata inince
    ölçülen değer 1/7 bandına GİRMELİ. Girmezse şüphe düşer ve başka bir
    sebep aranır.
    """
    _baslik("D - DUYMA MENZILI  (H1'in tutmama sebebi sinaniyor)")
    print("  🔒 Olculen egri: oran x atlama ~ 0,7 SABIT → verim atlamayla")
    print("     ters orantili → UZAMSAL YENIDEN KULLANIM YOK.")
    print("  🔴 Supheli: duyma menzili / iletim menzili = 6,3 (Li ~2 varsayar)")
    print()
    kfg = DS.konfig(kol="li")
    catlar = (1.0, 1.5, 2.0, 3.0, 4.5, 6.31)
    gorevler = []
    for c in catlar:
        duyma = c * kfg.iletim_menzili_m
        for n in (2, 11):
            for t in TOHUMLAR:
                gorevler.append((n, aralik_m, t, 1200.0, 30.0, duyma))
    with Pool(isci) as havuz:
        ham = havuz.map(_is, gorevler, chunksize=1)
    print(f"  {'duyma/iletim':>13} {'duyma_m':>9} {'tek atlama':>11} "
          f"{'11 dugum':>10} {'ORAN':>8} {'band icinde':>13}")
    k = 0
    for c in catlar:
        tek = [s["verim_hz"] for s, h in ham[k:k + len(TOHUMLAR)] if h is None]
        k += len(TOHUMLAR)
        uzun = [s["verim_hz"] for s, h in ham[k:k + len(TOHUMLAR)] if h is None]
        k += len(TOHUMLAR)
        if not tek or not uzun:
            print(f"  {c:>13.2f} KOSMADI")
            continue
        a, b = ist.mean(tek), ist.mean(uzun)
        oran = b / a if a else 0.0
        icinde = BAND[0] <= oran <= BAND[1]
        print(f"  {c:>13.2f} {c * kfg.iletim_menzili_m:>9.0f} {a:>11.1f} "
              f"{b:>10.2f} {oran:>8.4f} "
              f"{'🟢 EVET' if icinde else 'hayir':>13}")
    print()
    print(f"  🔒 Li'nin varsayimi ~2,0. Orada oran {BAND} bandina giriyorsa")
    print("     supher DOGRULANIR: kusur tasiyici dinleme esiginde.")


if __name__ == "__main__":
    # 🔒 Windows `spawn` korumasi — calisma kurali 11.
    DS.secimi_oku()                         # Faz 4 (K-183): --dunya
    print(f"  DUNYA: {DS.secili()}")
    aralik = a_aralik()
    if aralik is None:
        raise SystemExit(1)
    sonuc = b_zincir(aralik)
    if not c_karar(sonuc):
        # 🔴 Sartname §10: tutmazsa BULMADAN DEVAM EDILMEZ.
        d_duyma_menzili(aralik)
