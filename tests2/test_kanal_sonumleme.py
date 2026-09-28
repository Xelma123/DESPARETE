"""
ADIM 4 — `kanal/sonumleme.py` kapanış ölçütleri.

Yol haritasının bu modül için istedikleri:
    (c) K → ∞'da Rician sabite gidiyor
    (d) sönümleme otokorelasyonu `exp(−kΔt/T_c)` ile ±%10
    (e) paket başına ortalama parça ≥ 2
    (g) aynı tohumda iki protokol → sönümleme izleri **birebir eşit**

🔴 (g) bu projenin en kritik yapısal testidir. AR(1) doğal olarak durumludur;
durumlu yazılsaydı kanalın gördüğü dizi *hangi protokolün kaç kez çektiğine*
bağlı olur ve iki kol aynı tohumda farklı kanallar görürdü. 30 tohum bunu
kurtarmaz — eşleştirme yapısal olarak kırılır.
"""

from __future__ import annotations

import math
import pathlib
import statistics as ist
import sys

import pytest

KOK = pathlib.Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.cekirdek.rng import Akislar  # noqa: E402
from sim2.dunya.geometri import Nokta3  # noqa: E402
from sim2.dunya.topoloji import topoloji_kur  # noqa: E402
from sim2.kanal.cerceve import cerceve_kur  # noqa: E402
from sim2.kanal.sonumleme import (BAGIL_HIZ_TABANI_MS,  # noqa: E402
                                  FIR_EN_COK_KATSAYI, YENILIK_ONBELLEK_SINIRI,
                                  Sonumleme)
from sim2.kanal.yayilim import ISIK_HIZI  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402


class SabitHizTopoloji:
    """Denetimli bağıl hız — otokorelasyonu analitikle karşılaştırmak için.

    Gerçek `Topoloji` kullanılsaydı bağıl hız zamanla değişir ve ölçülen
    otokorelasyon hangi ρ ile karşılaştırılacağı belirsiz kalırdı.
    """

    def __init__(self, hiz_ms: float, hareketli: bool = True) -> None:
        self.hiz_ms = hiz_ms
        self.hareketli = hareketli
        self.mobilite_kolu = "bagimsiz" if hareketli else "statik"

    def konum(self, dugum: int, t_s: float) -> Nokta3:
        if dugum == 0:
            return Nokta3(0.0, 0.0, 70.0)
        return Nokta3(100.0 + self.hiz_ms * t_s, 0.0, 70.0)


def _sonumleme(hiz_ms: float = 30.0, hareketli: bool = True, **ek) -> Sonumleme:
    return Sonumleme(Konfig(kol="t", **ek), SabitHizTopoloji(hiz_ms, hareketli))


def _kazanclar(son: Sonumleme, adet: int = 8000) -> list[float]:
    dt = son.konfig.sonumleme_parca_suresi_s
    return [son.guc_kazanci(0, 1, k * dt) for k in range(adet)]


# ==========================================================================
# İSTATİSTİK — Rician'ın kendisi
# ==========================================================================

def test_ortalama_guc_kazanci_TAM_BIR():
    """Sönümleme ortalama gücü değiştirmemeli; yalnız dağıtmalı.

    Değiştirseydi, sönümlemeyi açmak menzili de değiştirirdi ve ablasyon
    "sönümlemenin etkisi" yerine "gücün değişmesi"ni ölçerdi.
    """
    g = _kazanclar(_sonumleme())
    assert ist.mean(g) == pytest.approx(1.0, abs=0.05)


def test_rician_varyansi_ANALITIK():
    """E|g|² = 1 iken Var|g|² = (1+2K)/(1+K)²."""
    for k_db in (0.0, 6.0, 12.0):
        k_lin = 10.0 ** (k_db / 10.0)
        beklenen = (1.0 + 2.0 * k_lin) / (1.0 + k_lin) ** 2
        g = _kazanclar(_sonumleme(rician_k_db=k_db))
        assert ist.pvariance(g) == pytest.approx(beklenen, rel=0.15), (
            f"K = {k_db} dB: ölçülen {ist.pvariance(g):.3f}, "
            f"analitik {beklenen:.3f}")


def test_K_SONSUZDA_sabite_gidiyor():
    """🔒 Kapanış ölçütü (c). K büyüdükçe dağılım 1'de toplanmalı."""
    onceki = 1.0
    for k_db in (0.0, 6.0, 20.0, 40.0):
        g = _kazanclar(_sonumleme(rician_k_db=k_db), adet=3000)
        yayilim = ist.pstdev(g)
        assert yayilim < onceki
        onceki = yayilim
    cok_buyuk = _kazanclar(_sonumleme(rician_k_db=60.0), adet=500)
    assert all(abs(x - 1.0) < 0.02 for x in cok_buyuk)


def test_K_SIFIRDA_Rayleigh():
    """K = 0 → güç kazancı üstel dağılım: ortalama 1, varyans 1."""
    g = _kazanclar(_sonumleme(rician_k_db=-90.0))
    assert ist.mean(g) == pytest.approx(1.0, abs=0.06)
    assert ist.pvariance(g) == pytest.approx(1.0, rel=0.2)


def test_ablasyon_sonumleme_KAPALI():
    kapali = _sonumleme(sonumleme_acik=False)
    assert all(kapali.guc_kazanci(0, 1, t) == 1.0
               for t in (0.0, 1.0, 17.3, 200.0))


# ==========================================================================
# 🔒 (d) OTOKORELASYON
# ==========================================================================

def test_otokorelasyon_exp_ile_UYUSUYOR():
    """🔒 Kapanış ölçütü (d): ölçülen ρ(kΔt) ilan edilenle ±%10.

    Karşılaştırma hedefi analitiktir: ρ = exp(−Δt/T_c), T_c = 0,423·λ/v.
    """
    hiz = 30.0
    son = _sonumleme(hiz)
    dt = son.konfig.sonumleme_parca_suresi_s
    lam = ISIK_HIZI / son.konfig.frekans_hz
    tc = 0.423 * lam / hiz
    ro = math.exp(-dt / tc)
    m = min(FIR_EN_COK_KATSAYI,
            max(1, math.ceil(math.log(0.01) / (2.0 * math.log(ro)))))

    iz = [son._fir("sonumleme_i", 0, 1, k, ro, m) for k in range(30000)]
    ort = ist.mean(iz)
    var = ist.pvariance(iz)
    assert var == pytest.approx(1.0, rel=0.05), (
        f"🔴 marjinal varyans {var:.3f} — `c` düzeltmesi çalışmıyor")

    for gecikme in (1, 2, 3, 5, 8):
        pay = sum((iz[n] - ort) * (iz[n + gecikme] - ort)
                  for n in range(len(iz) - gecikme)) / (len(iz) - gecikme)
        olculen = pay / var
        beklenen = ro ** gecikme
        assert abs(olculen - beklenen) < 0.10 * beklenen + 0.02, (
            f"gecikme {gecikme}: ölçülen ρ {olculen:.4f}, "
            f"beklenen {beklenen:.4f}")


def test_hizli_bag_HIZLI_dekorele_oluyor():
    """T_c hıza ters — hızlı bağ daha çabuk dekorele olmalı."""
    # 🔴 DOPPLER TAM ÖLÇEK HIZINDAN hesaplanır (8 Eylül 2026): dalga boyu
    # ölçeklenemediği için `f_d = v/λ` ölçekli hızla kullanılsaydı sönümleme
    # `olcek` kat yavaşlar ve çerçeve içi değişim yok olurdu. Beklenti bu
    # yüzden `olcek` taşır ve konfigden TÜRETİLİR, elle yazılmaz.
    def _tc(son, hiz):
        return (0.423 * (ISIK_HIZI / son.konfig.frekans_hz)
                / (hiz * son.konfig.olcek))

    def bir_gecikme_korelasyonu(hiz):
        son = _sonumleme(hiz)
        return math.exp(-son.konfig.sonumleme_parca_suresi_s / _tc(son, hiz))
    assert bir_gecikme_korelasyonu(50.0) < bir_gecikme_korelasyonu(10.0)
    for hiz in (5.0, 20.0, 50.0):
        son = _sonumleme(hiz)
        assert son.tutarlilik_suresi_s(0, 1, 0.0) == pytest.approx(
            _tc(son, hiz), rel=1e-9)


def test_DAGILIM_her_hizda_AYNI():
    """🔴 `c` düzeltmesinin varlık sebebi.

    `√(1−ρ²)` ile ölçeklemek yalnız M → ∞ için doğru. Sonlu M'de yavaş
    bağlarda (ρ → 1) varyans 1'in altına iner ve sönümleme ilan edilenden
    SIĞ olurdu — üstelik yavaş bağlarda, yani ağın çoğunda. Marjinal dağılım
    hızdan BAĞIMSIZ olmalı: hız yalnız kazancın ne kadar HIZLI değiştiğini
    belirler, ne kadar DERİN olduğunu değil.

    ⚠️ ÖRNEK SAYISI 60 000 — keyfi değil. Ardışık örnekler korelasyonlu
    olduğu için bağımsız örnek sayısı `süre / korelasyon süresi`dir; 1 m/s'te
    korelasyon süresi 15,4 ms ve 6 000 örnek yalnızca ~94 bağımsız örnek
    eder (ortalamanın standart hatası ≈ 0,06). Ölçüldü — 6 000'de 1,086,
    60 000'de 1,013, 200 000'de 0,9997.
    """
    k_lin = 10.0 ** (Konfig(kol="t").rician_k_db / 10.0)
    beklenen_var = (1.0 + 2.0 * k_lin) / (1.0 + k_lin) ** 2
    for hiz in (1.0, 5.0, 25.0, 60.0):
        g = _kazanclar(_sonumleme(hiz), adet=60000)
        assert ist.mean(g) == pytest.approx(1.0, abs=0.03), f"hız {hiz}"
        assert ist.pvariance(g) == pytest.approx(beklenen_var, rel=0.15), (
            f"hız {hiz}: varyans {ist.pvariance(g):.3f}, "
            f"analitik {beklenen_var:.3f} — sönümleme derinliği hıza bağlı "
            f"olmamalı")


def test_bagil_hiz_TABANI_uygulaniyor():
    """Sıfıra giden hız T_c'yi sonsuza götürür ve M'i patlatır."""
    son = _sonumleme(0.0)
    tc = son.tutarlilik_suresi_s(0, 1, 0.0)
    beklenen = 0.423 * (ISIK_HIZI / son.konfig.frekans_hz) / BAGIL_HIZ_TABANI_MS
    assert tc == pytest.approx(beklenen, rel=1e-9)


# ==========================================================================
# 🔴 (g) DURUMSUZLUK — tasarımın kilit taşı
# ==========================================================================

def test_IZLER_cagri_sirasindan_BAGIMSIZ():
    """🔒 Kapanış ölçütü (g).

    İki "protokol" taklit edilir: biri araya bir sürü başka çekim sıkıştırır,
    öteki sıkıştırmaz. Durumlu bir AR(1) olsaydı izler ayrışırdı.
    """
    a = _sonumleme()
    b = _sonumleme()
    zamanlar = [0.0007 * n for n in range(200)]

    iz_a = [a.guc_kazanci(0, 1, t) for t in zamanlar]

    iz_b = []
    for n, t in enumerate(zamanlar):
        # "öteki protokol" başka bağlardan ve başka zamanlardan çekiyor
        for baska in range(3):
            b.guc_kazanci(2 + baska, 9, t * 1.7 + baska)
        if n % 3 == 0:
            b.guc_kazanci(0, 1, t + 5.0)
        iz_b.append(b.guc_kazanci(0, 1, t))

    assert iz_a == iz_b, "🔴 sönümleme izi çağrı sırasına bağlı — DURUMLU"


def test_TERS_SIRADA_okumak_ayni_sonucu_veriyor():
    son = _sonumleme()
    zamanlar = [0.001 * n for n in range(150)]
    ileri = [son.guc_kazanci(0, 1, t) for t in zamanlar]
    taze = _sonumleme()
    geri = {t: taze.guc_kazanci(0, 1, t) for t in reversed(zamanlar)}
    assert ileri == [geri[t] for t in zamanlar]


def test_BAG_SIMETRIK():
    son = _sonumleme()
    for t in (0.0, 0.13, 7.77):
        assert son.guc_kazanci(0, 1, t) == son.guc_kazanci(1, 0, t)


def test_farkli_bag_ve_tohum_FARKLI_iz():
    a = _sonumleme()
    assert a.guc_kazanci(0, 1, 1.0) != a.guc_kazanci(0, 2, 1.0)
    b = _sonumleme(tohum=Konfig(kol="t").tohum + 1)
    assert a.guc_kazanci(0, 1, 1.0) != b.guc_kazanci(0, 1, 1.0)


def test_STATIK_kolda_sonumleme_DONUK():
    """🔒 Hareket yoksa Doppler yoktur; kanal zamanla değişmez.

    U1 sanity testi (*"statik + bağlı → PDR ≈ 1"*) ancak böyle anlamlı kalır:
    çerçeveden çerçeveye bağımsız derin fadingler PDR'yi sebepsiz düşürürdü.
    """
    son = _sonumleme(hareketli=False)
    ilk = son.guc_kazanci(0, 1, 0.0)
    assert all(son.guc_kazanci(0, 1, t) == ilk
               for t in (0.001, 1.0, 55.5, 349.9))
    # ama bağdan bağa yine de değişir
    assert son.guc_kazanci(0, 2, 0.0) != ilk


def test_gercek_topolojiyle_de_calisiyor():
    for senaryo in ("statik-yok", "bagimsiz-yok", "gorev-yok"):
        k = Konfig(kol="t", senaryo=senaryo)
        son = Sonumleme(k, topoloji_kur(k, Akislar(3)))
        g = [son.guc_kazanci(0, 5, 50.0 + 0.001 * n) for n in range(400)]
        assert all(x > 0.0 for x in g)
        assert ist.mean(g) == pytest.approx(1.0, abs=0.6)


# ==========================================================================
# 🔒 (e) PARÇALAMA
# ==========================================================================

def test_paket_basina_parca_sayisi_IKIDEN_COK():
    """🔒 Kapanış ölçütü (e). Ölçüldü — kanal bir çerçeve süresince
    ortancada 1,06, p95'te 1,98 kez değişiyor; tek çekim yanlış olurdu."""
    k = Konfig(kol="t")
    son = _sonumleme()
    assert son.parca_sayisi(cerceve_kur(k, "veri").sure_s) >= 2
    assert son.parca_sayisi(cerceve_kur(k, "onay").sure_s) >= 2
    # ⚠️ Değişim dedektörü: sayı KONFİGDEN türer, elle yazılmaz. Eskiden
    # "== 10" yazıyordu ve parça süresi 240 → 190 µs olunca kırıldı.
    beklenen = math.ceil(cerceve_kur(k, "veri").sure_s
                         / k.sonumleme_parca_suresi_s)
    assert son.parca_sayisi(cerceve_kur(k, "veri").sure_s) == beklenen


def test_parca_sinirlari_cerceveyi_TAM_ortuyor():
    son = _sonumleme()
    for bas, sure in ((0.0, 2240e-6), (13.37, 2240e-6), (0.00013, 248e-6)):
        s = son.parca_sinirlari(bas, sure)
        assert s[0] == bas
        assert s[-1] == pytest.approx(bas + sure)
        assert all(x < y for x, y in zip(s, s[1:])), "sınırlar artan değil"
        toplam = sum(y - x for x, y in zip(s, s[1:]))
        assert toplam == pytest.approx(sure, rel=1e-12)


def test_parca_sinirlari_IZGARAYA_hizali():
    """Sınırlar mutlak zaman ızgarasındadır; çerçeve başlangıcına göre
    kaydırılsaydı iki farklı çerçeve aynı anda farklı kazanç görürdü."""
    son = _sonumleme()
    dt = son.konfig.sonumleme_parca_suresi_s
    s = son.parca_sinirlari(0.5 * dt, 4.0 * dt)
    ic = s[1:-1]
    for kenar in ic:
        assert (kenar / dt) == pytest.approx(round(kenar / dt), abs=1e-9)


def test_gecersiz_sure_reddediliyor():
    from sim2.cekirdek.degismezler import DegismezHatasi
    son = _sonumleme()
    with pytest.raises(DegismezHatasi):
        son.parca_sinirlari(0.0, 0.0)


# ==========================================================================
# 🔴 (h) ÖNBELLEK TAVANI — tahliye ALTINDA da durumsuz
#
# ⚠️ Yukarıdaki (g) testleri 200–600 çağrı yapıyor; üretim tavanı 250 000.
# Yani sınırlı önbellek BOZUK yazılsa o testler yine geçerdi — tahliye hiç
# tetiklenmez. Buradaki testler tavanı küçültüp tahliyeyi ZORLAR; ölçtüğü
# şey "önbellek çalışıyor mu" değil, "tahliye edilmiş bir girdi geri
# geldiğinde aynı sayıyı mı veriyor"dur.
# ==========================================================================

def _kucuk_sinirli(tavan: int = 50, **ek) -> Sonumleme:
    son = _sonumleme(**ek)
    son._sinir = tavan
    return son


def test_onbellek_TAVANI_ASILMIYOR():
    son = _kucuk_sinirli(50)
    for n in range(3000):
        son.guc_kazanci(0, 1, 0.001 * n)
        assert len(son._memo) <= 50
    assert son._tahliye > 0, "🔴 tahliye hiç tetiklenmedi — test bir şey ölçmüyor"


def test_TAHLIYE_altinda_izler_DEGISMIYOR():
    """🔒 Asıl kapı: tavan sonucu değiştirmemeli.

    Aynı izi iki kez alır — biri tahliyenin sürekli tetiklendiği küçük
    tavanla, öteki hiç tetiklenmediği büyük tavanla.
    """
    zamanlar = [0.0013 * n for n in range(1200)]
    dar = _kucuk_sinirli(40)
    genis = _kucuk_sinirli(10_000_000)
    iz_dar = [dar.guc_kazanci(0, 1, t) for t in zamanlar]
    iz_genis = [genis.guc_kazanci(0, 1, t) for t in zamanlar]
    assert dar._tahliye > 0 and genis._tahliye == 0
    assert iz_dar == iz_genis, "🔴 tahliye değeri değiştirdi — memo saf değil"


def test_TAHLIYE_altinda_TERS_SIRA_da_ayni():
    """Tahliye + ters sıra birlikte: en zor hâl."""
    zamanlar = [0.0007 * n for n in range(900)]
    ileri = _kucuk_sinirli(30)
    geri = _kucuk_sinirli(30)
    a = [ileri.guc_kazanci(0, 1, t) for t in zamanlar]
    b = {t: geri.guc_kazanci(0, 1, t) for t in reversed(zamanlar)}
    assert ileri._tahliye > 0 and geri._tahliye > 0
    assert a == [b[t] for t in zamanlar]


def test_ARADAN_BASKA_BAGLAR_cekilince_de_ayni():
    """Tahliyeyi başka bağların çekimleri tetiklerken iz bozulmamalı."""
    zamanlar = [0.0011 * n for n in range(600)]
    temiz = _kucuk_sinirli(10_000_000)
    beklenen = [temiz.guc_kazanci(0, 1, t) for t in zamanlar]
    karisik = _kucuk_sinirli(25)
    bulunan = []
    for n, t in enumerate(zamanlar):
        for baska in range(4):
            karisik.guc_kazanci(2 + baska, 9, t * 1.9 + baska)
        bulunan.append(karisik.guc_kazanci(0, 1, t))
    assert karisik._tahliye > 0
    assert bulunan == beklenen


def test_onbellek_raporu_ISKALAMAYI_kestiriyor(monkeypatch):
    """🔴 Rapor bir TAHMİN; sapması sınırlı kalmalı.

    Tahliye başına tam olarak `tavan` kadar ıskalama varsayılır. Gerçek
    ıskalama burada DOĞRUDAN sayılır — çekim fonksiyonu sarmalanarak, çünkü
    ıskalamayı sözlük boyutundan çıkarmak tahliyenin ortasına denk gelen
    çağrılarda yanlış sayardı.
    """
    import sim2.kanal.sonumleme as SM

    sayac = {"n": 0}
    asil = SM.normal_cekimi

    def sayan(alan, ana_tohum, *anahtarlar):
        sayac["n"] += 1
        return asil(alan, ana_tohum, *anahtarlar)

    monkeypatch.setattr(SM, "normal_cekimi", sayan)

    tavan = 200
    son = _kucuk_sinirli(tavan)
    for n in range(4000):
        son.guc_kazanci(0, 1, 0.0009 * n)

    rapor = son.onbellek_raporu()
    assert son._tahliye > 0, "🔴 tahliye tetiklenmedi — test bir şey ölçmüyor"
    assert rapor["sinir"] == tavan
    assert rapor["tahliye"] == son._tahliye
    assert rapor["girdi"] == len(son._memo)
    assert rapor["iskalama_tahmini"] == pytest.approx(sayac["n"], rel=0.05)


def test_STATIK_kolda_onbellek_KUCUK_kalir():
    """Donuk sönümlemede tek indeks kullanılır — tavan hiç devreye girmez."""
    son = _sonumleme(hareketli=False)
    for n in range(2000):
        son.guc_kazanci(0, 1, 0.01 * n)
    assert son._tahliye == 0
    assert len(son._memo) <= 2


# ==========================================================================
# K-198 · BLOK ÜRETECİ — aynı model, başka sayı kaynağı
# ==========================================================================

def _blok(hiz_ms: float = 30.0, hareketli: bool = True, **ek) -> Sonumleme:
    return _sonumleme(hiz_ms, hareketli, sonumleme_uretec="blok", **ek)


def test_K198_varsayilan_TEKIL_referans_dunya_BLOK():
    from sim2.cekirdek.degismezler import DegismezHatasi
    from sim2.kanal.dunya import referans_2026
    assert Konfig(kol="t").sonumleme_uretec == "tekil"
    assert referans_2026(kol="t").sonumleme_uretec == "blok"
    assert _blok()._blok and not _sonumleme()._blok
    with pytest.raises(DegismezHatasi):
        Konfig(kol="t", sonumleme_uretec="numpy")


def test_K198_blok_ORTALAMA_ve_RICIAN_varyansi():
    for k_db in (0.0, 6.0, 12.0):
        k_lin = 10.0 ** (k_db / 10.0)
        beklenen = (1.0 + 2.0 * k_lin) / (1.0 + k_lin) ** 2
        g = _kazanclar(_blok(rician_k_db=k_db), adet=20000)
        assert ist.mean(g) == pytest.approx(1.0, abs=0.05), f"K = {k_db}"
        assert ist.pvariance(g) == pytest.approx(beklenen, rel=0.15), (
            f"K = {k_db} dB: ölçülen {ist.pvariance(g):.3f}, "
            f"analitik {beklenen:.3f}")


def test_K198_blok_OTOKORELASYON_ve_marjinal_varyans():
    """Kapanış ölçütü (d) blok üretecinde: I ve Q ayrı ayrı."""
    hiz = 30.0
    son = _blok(hiz)
    dt = son.konfig.sonumleme_parca_suresi_s
    tc = 0.423 * (ISIK_HIZI / son.konfig.frekans_hz) / hiz
    ro = math.exp(-dt / tc)
    m = min(FIR_EN_COK_KATSAYI,
            max(1, math.ceil(math.log(0.01) / (2.0 * math.log(ro)))))
    ciftler = [son._fir_blok(0, 1, k, ro, m) for k in range(30000)]
    for bilesen in (0, 1):
        iz = [c[bilesen] for c in ciftler]
        ort, var = ist.mean(iz), ist.pvariance(iz)
        assert var == pytest.approx(1.0, rel=0.05), f"bileşen {bilesen}"
        for gecikme in (1, 2, 3, 5, 8):
            pay = sum((iz[n] - ort) * (iz[n + gecikme] - ort)
                      for n in range(len(iz) - gecikme)) / (len(iz) - gecikme)
            olculen, beklenen = pay / var, ro ** gecikme
            assert abs(olculen - beklenen) < 0.10 * beklenen + 0.02, (
                f"bileşen {bilesen} gecikme {gecikme}: {olculen:.4f} ≠ "
                f"{beklenen:.4f}")
    iq = sum(a * b for a, b in ciftler) / len(ciftler)
    assert abs(iq) < 0.05, f"I ile Q ilintili: {iq:.3f}"


def test_K198_blok_DAGILIM_her_hizda_AYNI():
    k_lin = 10.0 ** (Konfig(kol="t").rician_k_db / 10.0)
    beklenen_var = (1.0 + 2.0 * k_lin) / (1.0 + k_lin) ** 2
    for hiz in (1.0, 25.0):
        g = _kazanclar(_blok(hiz), adet=60000)
        assert ist.mean(g) == pytest.approx(1.0, abs=0.03), f"hız {hiz}"
        assert ist.pvariance(g) == pytest.approx(beklenen_var, rel=0.15)


def test_K198_blok_IZLER_cagri_sirasindan_ve_TAHLIYEDEN_BAGIMSIZ():
    """🔒 (g) + (h) blok kipinde: durumsuz, ters sırada aynı, tahliye
    altında aynı, başka bağların çekimleri araya girse de aynı."""
    zamanlar = [0.0011 * n for n in range(1500)]
    temiz = _blok()
    beklenen = [temiz.guc_kazanci(0, 1, t) for t in zamanlar]
    dar = _blok()
    dar._pencere_sinir = 3
    karisik = []
    for n, t in enumerate(zamanlar):
        for baska in range(3):
            dar.guc_kazanci(2 + baska, 9, t * 1.7 + baska)
        karisik.append(dar.guc_kazanci(0, 1, t))
    assert dar._tahliye > 0, "🔴 tahliye tetiklenmedi — test bir şey ölçmüyor"
    assert karisik == beklenen
    geri_son = _blok()
    geri = {t: geri_son.guc_kazanci(0, 1, t) for t in reversed(zamanlar)}
    assert beklenen == [geri[t] for t in zamanlar]
    assert len(dar._pencereler) <= 3


def test_K198_blok_SIMETRIK_DONUK_ve_AYIRT_EDICI():
    son = _blok()
    for t in (0.0, 0.13, 7.77):
        assert son.guc_kazanci(0, 1, t) == son.guc_kazanci(1, 0, t)
    assert son.guc_kazanci(0, 1, 1.0) != son.guc_kazanci(0, 2, 1.0)
    baska = _blok(tohum=Konfig(kol="t").tohum + 1)
    assert son.guc_kazanci(0, 1, 1.0) != baska.guc_kazanci(0, 1, 1.0)
    donuk = _blok(hareketli=False)
    ilk = donuk.guc_kazanci(0, 1, 0.0)
    assert all(donuk.guc_kazanci(0, 1, t) == ilk for t in (0.001, 55.5, 349.9))
    assert donuk.guc_kazanci(0, 2, 0.0) != ilk
    # karıştırıcı bağı da aynı yoldan (negatif kimlik)
    k1 = son.karistirici_kazanci(-1, 3, 2.0, 30.0)
    assert k1 > 0.0 and k1 == son.karistirici_kazanci(-1, 3, 2.0, 30.0)


def test_K198_iki_uretec_AYNI_dagilim_FARKLI_sayilar():
    """Aynı tohumda iki üreteç farklı iz, aynı istatistik (ortalama ve
    varyans iki örneklem SE'si içinde)."""
    a = _kazanclar(_sonumleme(), adet=40000)
    b = _kazanclar(_blok(), adet=40000)
    assert a[:50] != b[:50]
    assert ist.mean(a) == pytest.approx(ist.mean(b), abs=0.04)
    assert ist.pvariance(a) == pytest.approx(ist.pvariance(b), rel=0.12)


def test_MODUL_SABITI_ornege_BAGLI():
    """🔴 Bildirim ≠ kullanım: sabit gerçekten örneğin tavanı mı?

    `YENILIK_ONBELLEK_SINIRI` ilan edilmiş ama `__init__` onu okumuyor olsaydı,
    sabiti değiştirmek hiçbir şeyi değiştirmezdi ve bunu kimse fark etmezdi.
    Modül sabitini yamalayıp YENİ bir örneğin onu aldığını doğrular.
    """
    import sim2.kanal.sonumleme as SM
    assert _sonumleme()._sinir == YENILIK_ONBELLEK_SINIRI
    eski = SM.YENILIK_ONBELLEK_SINIRI
    try:
        SM.YENILIK_ONBELLEK_SINIRI = 1234
        assert _sonumleme()._sinir == 1234, (
            "🔴 modül sabiti örneğe bağlı değil — tavan sessizce sabitlenmiş")
    finally:
        SM.YENILIK_ONBELLEK_SINIRI = eski
    assert YENILIK_ONBELLEK_SINIRI > 0
