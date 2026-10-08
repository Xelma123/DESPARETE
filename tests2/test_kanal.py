"""
ADIM 4 — `kanal/girisim.py` ve `kanal/kanal.py` kapanış ölçütleri.

Yol haritasının kalan iki maddesi:
    (a) sabit girişimde **parçalı PER == tek parça** (analitik)
    (f) **TEK** `per()` (AST)

🔴 (a) kusur 1'in kapandığının kanıtıdır. Eski simülatörde kâhin PER ile
gerçek alım PER'i ayrı gövdelerdi ve sistematik olarak ayrışıyorlardı —
yeni parametrelerde ölçülen fark %9,38. Burada eşitlik yaklaşık değil,
cebirsel: bit toplamı korunduğu sürece sabit SINR'de iki hesap AYNI sayıdır.
"""

from __future__ import annotations

import ast
import math
import pathlib
import sys

import pytest

KOK = pathlib.Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))
SIM2 = KOK / "sim2"

from sim2.cekirdek.degismezler import DegismezHatasi  # noqa: E402
from sim2.cekirdek.rng import Akislar  # noqa: E402
from sim2.dunya.topoloji import topoloji_kur  # noqa: E402
from sim2.kanal.cerceve import cerceve_kur  # noqa: E402
from sim2.kanal.girisim import Iletim, Ortam  # noqa: E402
from sim2.kanal.kanal import Kanal, ber_dbpsk, ber_dqpsk  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402


def _kanal(senaryo: str = "statik-yok", **ek):
    k = Konfig(kol="t", senaryo=senaryo, **ek)
    return Kanal(k, topoloji_kur(k, Akislar(1)))


# ==========================================================================
# MODÜLASYON — DQPSK kapalı formu
# ==========================================================================

def test_ber_sinirlarda():
    for ber in (ber_dqpsk, ber_dbpsk):
        assert ber(0.0) == pytest.approx(0.5)
        assert ber(-1.0) == pytest.approx(0.5)
        assert 0.0 <= ber(1e6) < 1e-12
    # γ arttıkça BER monoton azalmalı
    onceki = 1.0
    for db in range(0, 20, 2):
        b = ber_dqpsk(10.0 ** (db / 10.0))
        assert b < onceki
        onceki = b


def test_DQPSK_kapali_formu_MONTE_CARLO_ile_dogrulaniyor():
    """🔴 Bu testin varlık sebebi bir HATA DÜZELTMESİ.

    Kapalı form ilk yazıldığında "yayınlanmış eğrilerde BER = 1e-3 ≈ 9,9 dB"
    hatırlamasıyla karşılaştırıldı ve 9,20 dB çıktı; formül yanlış sanıldı.
    Bağımsız bir Monte Carlo (diferansiyel QPSK, Gray eşlemeli, diferansiyel
    algılama) formülü doğruladı — hatalı olan hatırlanan sayıydı.

    Ölçüldü (4–20 milyon sembol): oran 1,002 · 1,001 · 1,000 · 1,006 · 1,015
    (2 · 4 · 6 · 8 · 10 dB). Buradaki test hızlı olsun diye küçük örneklemle
    ve yüksek BER bölgesinde koşar.
    """
    import numpy as np
    rng = np.random.default_rng(20260904)

    def mc(gamma_b, n):
        n0 = 1.0 / (2.0 * gamma_b)              # Es = 1, Es/N0 = 2·Eb/N0
        bit = rng.integers(0, 2, size=(n, 2))
        esleme = np.array([0, 1, 3, 2])         # ikili → Gray
        dphi = esleme[bit[:, 0] * 2 + bit[:, 1]] * (np.pi / 2)
        s = np.exp(1j * np.cumsum(np.concatenate(([0.0], dphi))))
        g = (rng.normal(0, math.sqrt(n0 / 2), s.shape)
             + 1j * rng.normal(0, math.sqrt(n0 / 2), s.shape))
        r = s + g
        karar = np.mod(np.rint(np.angle(r[1:] * np.conj(r[:-1]))
                               / (np.pi / 2)).astype(int), 4)
        kod = np.array([0, 1, 3, 2])[karar]     # Gray → ikili
        return float(np.mean(
            np.stack([kod // 2, kod % 2], axis=1) != bit))

    for db, n in ((2, 400_000), (6, 400_000)):
        gamma = 10.0 ** (db / 10.0)
        assert mc(gamma, n) == pytest.approx(ber_dqpsk(gamma), rel=0.06), (
            f"{db} dB'de kapalı form Monte Carlo ile uyuşmuyor")


def test_DQPSK_DBPSKden_asimptotik_2_32_dB_KOTU():
    """Analitik: üstel katsayıların oranı (√(1+1/√2) − √(1−1/√2))⁻² = 1,707
    → 2,32 dB. Kapalı formun kendi asimptotu."""
    beklenen = 10.0 * math.log10(
        1.0 / (math.sqrt(1 + math.sqrt(0.5)) - math.sqrt(1 - math.sqrt(0.5))) ** 2)
    assert beklenen == pytest.approx(2.32, abs=0.01)
    gamma = 10.0 ** (2.0)                        # 20 dB — asimptot bölgesi
    hedef = ber_dqpsk(gamma)
    alt, ust = 0.01, 1e6
    for _ in range(200):
        orta = (alt + ust) / 2
        if ber_dbpsk(orta) > hedef:
            alt = orta
        else:
            ust = orta
    ceza = -10.0 * math.log10(alt / gamma)
    assert ceza == pytest.approx(beklenen, abs=0.25)


def test_bilinmeyen_modulasyon_REDDEDILIYOR():
    k = Konfig(kol="t", modulasyon="mors")
    with pytest.raises(ValueError):
        Kanal(k, topoloji_kur(Konfig(kol="t"), Akislar(1)))


def test_modulasyon_ABLASYONU():
    """🔒 A4 (K-177): modülasyon çerçevenin özelliği (hızı belirler); her
    çerçeve kendi konfigünden kurulur. Eskiden kanalın özelliğiydi ve bu test
    DBPSK konfigünün çerçevesini DQPSK kanalında değerlendiriyordu —
    koşularda çerçeve ve kanal hep aynı konfigden, sonuç birebir."""
    kanal = _kanal(modulasyon="dbpsk")
    dbpsk = kanal.kahin_per(cerceve_kur(kanal.konfig, "veri"), 10.0)
    kanal2 = _kanal()
    dqpsk = kanal2.kahin_per(cerceve_kur(kanal2.konfig, "veri"), 10.0)
    assert dqpsk > dbpsk, "DQPSK aynı SINR'de daha kırılgan olmalı"


# ==========================================================================
# 🔒 (a) PARÇALI PER == TEK PARÇA
# ==========================================================================

@pytest.mark.parametrize("sinr_db", [4.0, 8.0, 10.0, 13.0, 18.0])
@pytest.mark.parametrize("parca", [2, 5, 10, 37])
def test_PARCALI_PER_tek_parcaya_CEBIRSEL_esit(sinr_db, parca):
    """🔒 Kapanış ölçütü (a). Yaklaşık değil, birebir."""
    kanal = _kanal()
    c = cerceve_kur(kanal.konfig, "veri")
    sinr = 10.0 ** (sinr_db / 10.0)
    bit = c.hataya_acik_bit / parca
    iz = tuple((bit, sinr) for _ in range(parca))
    assert kanal.per(c, iz) == pytest.approx(kanal.kahin_per(c, sinr),
                                             rel=1e-12)


def test_esit_olmayan_parcalar_da_esit():
    kanal = _kanal()
    c = cerceve_kur(kanal.konfig, "veri")
    sinr = 10.0 ** 1.1
    paylar = (0.05, 0.3, 0.01, 0.44, 0.2)
    iz = tuple((c.hataya_acik_bit * p, sinr) for p in paylar)
    assert sum(paylar) == pytest.approx(1.0)
    assert kanal.per(c, iz) == pytest.approx(kanal.kahin_per(c, sinr),
                                            rel=1e-12)


def test_BIT_TOPLAMI_degismezi_ATESLENIYOR():
    """🔴 Bu değişmez olmasaydı parçalı PER sessizce tek parçadan ayrışırdı —
    kusur 1'in tam olarak geri gelmesi."""
    kanal = _kanal()
    c = cerceve_kur(kanal.konfig, "veri")
    with pytest.raises(DegismezHatasi):
        kanal.per(c, ((c.hataya_acik_bit * 0.5, 10.0),))
    with pytest.raises(DegismezHatasi):
        kanal.per(c, ((c.hataya_acik_bit * 1.2, 10.0),))
    with pytest.raises(DegismezHatasi):
        kanal.per(c, ())


def test_kotu_parca_TUM_cerceveyi_bozuyor():
    """Tek bir kötü parça çerçeveyi düşürebilmeli — patlamalı hatanın kaynağı."""
    kanal = _kanal()
    c = cerceve_kur(kanal.konfig, "veri")
    iyi = 10.0 ** 2.0
    n = 10
    bit = c.hataya_acik_bit / n
    temiz = tuple((bit, iyi) for _ in range(n))
    bozuk = ((bit, 0.05),) + tuple((bit, iyi) for _ in range(n - 1))
    assert kanal.per(c, temiz) < 1e-6
    assert kanal.per(c, bozuk) > 0.99


def test_per_sinirlarda():
    kanal = _kanal()
    c = cerceve_kur(kanal.konfig, "veri")
    assert kanal.kahin_per(c, 0.0) == 1.0
    assert kanal.kahin_per(c, 1e9) == pytest.approx(0.0, abs=1e-12)
    for db in range(0, 25):
        p = kanal.kahin_per(c, 10.0 ** (db / 10.0))
        assert 0.0 <= p <= 1.0


def test_menzilde_PER_gecis_bandi():
    """Ölçülmüş bulguyu sabitler: geçiş bandı gölgeleme σ'sından dar."""
    kanal = _kanal()
    c = cerceve_kur(kanal.konfig, "veri")
    def sinr_icin(hedef):
        alt, ust = 0.05, 500.0
        for _ in range(300):
            orta = (alt + ust) / 2
            if kanal.kahin_per(c, orta) > hedef:
                alt = orta
            else:
                ust = orta
        return 10.0 * math.log10(alt)
    bant = sinr_icin(0.01) - sinr_icin(0.99)
    assert 1.0 < bant < 6.0, f"geçiş bandı {bant:.2f} dB"
    assert bant < 2.0 * kanal.konfig.golgeleme_sigma_db, (
        "🔴 geçiş bandı gölgeleme σ'sının iki katından dar olmalı — "
        "gölgelemenin eklenme gerekçesi buydu")


# ==========================================================================
# 🔒 (f) TEK `per()` GÖVDESİ
# ==========================================================================

def test_TEK_per_govdesi_VAR():
    """🔒 Kapanış ölçütü (f).

    ⚠️ Ne kanıtlar: `sim2/` altında PER'e benzer ikinci bir gövde YOK.
    Ne kanıtlamaz: `kanal.py` içindeki gövdenin doğru olduğunu — onu
    yukarıdaki cebirsel eşitlik testleri kanıtlar.
    """
    per_fonksiyonlari: list[str] = []
    olasilik_govdesi: list[str] = []
    for yol in sorted(SIM2.rglob("*.py")):
        if "__pycache__" in yol.parts:
            continue
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        for n in ast.walk(agac):
            if isinstance(n, ast.FunctionDef) and "per" in n.name.lower():
                if yol.name != "kanal.py":
                    per_fonksiyonlari.append(
                        f"{yol.relative_to(KOK).as_posix()}:{n.lineno} "
                        f"→ {n.name}")
            # `1 − (1−p)^n` imzası: `expm1`/`log1p` bu depoda PER'e aittir
            if isinstance(n, ast.Attribute) and n.attr in ("expm1", "log1p"):
                if yol.name != "kanal.py":
                    olasilik_govdesi.append(
                        f"{yol.relative_to(KOK).as_posix()}:{n.lineno} "
                        f"→ {n.attr}")
    assert not per_fonksiyonlari, (
        f"🔴 `kanal.py` dışında PER fonksiyonu: {per_fonksiyonlari}")
    assert not olasilik_govdesi, (
        f"🔴 `kanal.py` dışında olasılık gövdesi: {olasilik_govdesi}")


def test_kahin_ve_gercek_alim_AYNI_govdeyi_cagiriyor():
    """Sabit kanalda (statik kol, gölgeleme/sönümleme kapalı, girişim yok)
    gerçek alım PER'i kâhin PER'e birebir eşit olmalı."""
    kanal = _kanal("statik-yok", golgeleme_acik=False, sonumleme_acik=False,
                   anten_deseni_acik=False)
    c = cerceve_kur(kanal.konfig, "veri")
    gercek = kanal.alim_per(0, 1, c, bas_s=10.0)
    a = kanal.topoloji.konum(0, 10.0)
    b = kanal.topoloji.konum(1, 10.0)
    sinr = (kanal.yayilim.yavas_alinan_w(0, 1, a, b) / kanal.yayilim.gurultu_w)
    assert gercek == pytest.approx(kanal.kahin_per(c, sinr), rel=1e-9)


# ==========================================================================
# SINR İZİ ve GİRİŞİM
# ==========================================================================

def test_sinr_izi_BIT_TOPLAMI_tam():
    kanal = _kanal("bagimsiz-yok")
    for tip in ("veri", "onay", "beacon"):
        c = cerceve_kur(kanal.konfig, tip)
        iz = kanal.sinr_izi(0, 1, c, bas_s=25.0)
        assert len(iz) >= 1
        assert math.fsum(b for b, _ in iz) == pytest.approx(
            c.hataya_acik_bit, rel=1e-12)


def test_ONBELGE_bit_tasimiyor():
    """Önbelgeye düşen parçanın bit payı sıfır olmalı — kusur 1'in fiziği."""
    kanal = _kanal("bagimsiz-yok")
    c = cerceve_kur(kanal.konfig, "veri")
    iz = kanal.sinr_izi(0, 1, c, bas_s=0.0)
    # ⚠️ BEKLENTİ KONFİGDEN TÜRETİLİR. Eskiden "240e-6" elle yazılıydı ve
    # parça süresi 190 µs olunca (8 Eylül 2026, Doppler tam ölçek hızına
    # bağlandı) testi kırdı — iddiası hâlâ doğruyken.
    #
    # 🔴 VE YAPI DEĞİŞTİ: parça süresi artık ÖNBELGEDEN KISA (190 < 192 µs).
    # Yani ilk parça tamamen önbelgenin içinde kalıyor ve hiç gövde biti
    # taşımıyor; `_iz` sıfır örtüşmeli parçayı atladığı için bit taşıyan
    # İLK parça, önbelgeyi geçen ilk sınıra kadar olan paydır.
    # İddia değişmedi: önbelgeye düşen pay SIFIRDIR.
    dt = kanal.konfig.sonumleme_parca_suresi_s
    onbelge = kanal.konfig.onbelge_s
    ilk_sinir = math.ceil(onbelge / dt) * dt
    beklenen_ilk = (c.hataya_acik_bit * (ilk_sinir - onbelge)
                    / c.govde_suresi_s)
    assert iz[0][0] == pytest.approx(beklenen_ilk, rel=1e-9)


def _iyi_bag(kanal, t_s=10.0):
    """Gerçekten alınabilen bir bağ ve ona yakın bir girişimci bulur.

    ⚠️ Rastgele bir çift seçmek yanlış olurdu: 0–1 çifti bu tohumda menzil
    dışında ve PER'i zaten 1,0 — girişim eklemek onu "daha kötü" yapamaz ve
    test hiçbir şey ölçmez.
    """
    a = kanal.topoloji.anlik(t_s)
    for i, komsular in enumerate(a.komsular):
        for j in komsular:
            for k in a.komsular[j]:
                if k not in (i, j):
                    return i, j, k
    raise AssertionError("uygun üçlü bulunamadı")


def test_girisim_SINRi_dusuruyor_ve_PERi_yukseltiyor():
    kanal = _kanal("statik-yok", golgeleme_acik=False, sonumleme_acik=False)
    c = cerceve_kur(kanal.konfig, "veri")
    i, j, k = _iyi_bag(kanal)
    temiz = kanal.alim_per(i, j, c, bas_s=10.0)
    assert temiz < 0.5, "menzil içi bağ alınabilir olmalı"
    # 🔴 Girişimci ZAMANDA ÖRTÜŞMELİ. İlk yazımda 9,5 s'de başlıyordu ve
    # 2,24 ms sonra bitiyordu — alım 10,0 s'de başlarken çoktan susmuştu,
    # test hiçbir şey ölçmüyordu (kirli == temiz, birebir).
    kanal.ortam.ekle(Iletim(gonderen=k, cerceve=c, baslangic_s=9.9995,
                            guc_w=kanal.yayilim.verici_gucu_w))
    kirli = kanal.alim_per(i, j, c, bas_s=10.0)
    assert kirli > temiz


def test_ALICI_kendi_gucunu_girisime_KATAMIYOR():
    """🔴 Eski simülatörde bu bir `assert` ile korunuyordu ve `-O` altında
    kalkıyordu."""
    kanal = _kanal("statik-yok")
    c = cerceve_kur(kanal.konfig, "veri")
    kanal.ortam.ekle(Iletim(gonderen=0, cerceve=c, baslangic_s=10.0,
                            guc_w=kanal.yayilim.verici_gucu_w))
    assert kanal.girisim.girisim_w(1, 10.1, haric=0) == 0.0
    with pytest.raises(DegismezHatasi):
        kanal.girisim.girisim_w(1, 10.1, haric=1)


def test_parca_sinirlari_GIRISIM_olaylarini_da_iceriyor():
    """🔒 İki kaynağın BİRLEŞİMİ. Yalnız sönümleme ızgarası alınsaydı,
    çerçevenin ortasında başlayan bir iletimin yarattığı SINR sıçraması
    ortalamaya gömülürdü."""
    kanal = _kanal("statik-yok")
    c = cerceve_kur(kanal.konfig, "veri")
    once = kanal.girisim.parca_sinirlari(10.0, c.sure_s)
    olay = 10.0 + 0.000731                    # ızgaraya denk gelmeyen an
    assert olay not in once
    kanal.ortam.ekle(Iletim(gonderen=3, cerceve=c, baslangic_s=olay,
                            guc_w=kanal.yayilim.verici_gucu_w))
    sonra = kanal.girisim.parca_sinirlari(10.0, c.sure_s)
    assert olay in sonra
    assert len(sonra) == len(once) + 1
    assert list(sonra) == sorted(sonra)


def test_ortam_defteri():
    kanal = _kanal()
    c = cerceve_kur(kanal.konfig, "veri")
    ortam = kanal.ortam
    assert ortam.bos_mu()
    ortam.ekle(Iletim(gonderen=1, cerceve=c, baslangic_s=5.0, guc_w=0.01))
    assert not ortam.bos_mu()
    assert len(ortam.aktif(5.001)) == 1
    assert len(ortam.aktif(5.0 + c.sure_s + 1e-9)) == 0
    assert len(ortam.pencerede(4.0, 5.5)) == 1
    ortam.bitenleri_at(5.0 + c.sure_s)
    assert ortam.bos_mu()


def test_CSMA_mesgul_algilama():
    kanal = _kanal("statik-yok", golgeleme_acik=False, sonumleme_acik=False)
    c = cerceve_kur(kanal.konfig, "veri")
    assert kanal.girisim.kanal_mesgul_mu(1, 10.0) is False
    kanal.ortam.ekle(Iletim(gonderen=0, cerceve=c, baslangic_s=10.0,
                            guc_w=kanal.yayilim.verici_gucu_w))
    assert kanal.girisim.kanal_mesgul_mu(1, 10.001) is True
    # kendi iletimini meşgul saymaz
    assert kanal.girisim.kanal_mesgul_mu(0, 10.001) is False


def test_kendi_kendine_gonderim_REDDEDILIYOR():
    kanal = _kanal()
    c = cerceve_kur(kanal.konfig, "veri")
    with pytest.raises(DegismezHatasi):
        kanal.sinr_izi(3, 3, c, bas_s=1.0)


def test_uc_kolda_da_calisiyor():
    for senaryo in ("statik-yok", "bagimsiz-yok", "gorev-yok"):
        kanal = _kanal(senaryo)
        c = cerceve_kur(kanal.konfig, "veri")
        p = kanal.alim_per(0, 1, c, bas_s=100.0)
        assert 0.0 <= p <= 1.0


# ==========================================================================
# A2 · DSSS İŞLEM KAZANCI — `v2/15` A2 (K-173)
# ==========================================================================
def _a2_kanal():
    return _kanal(islem_kazanci=True, bant_genisligi_hz=22e6,
                  gurultu_figuru_db=7.0)


def test_A2_KAPALIYKEN_carpan_TAM_BIR_acikken_22_ve_11():
    c0 = cerceve_kur(Konfig(kol="t"), "veri")
    assert (c0.govde_ebn0_carpani, c0.onbelge_ebn0_carpani) == (1.0, 1.0)
    c = cerceve_kur(_a2_kanal().konfig, "veri")
    assert (c.govde_ebn0_carpani, c.onbelge_ebn0_carpani) == (11.0, 22.0)


def test_A2_ACIKKEN_bant_22_MHz_ZORUNLU():
    """Çarpan B/R_b ancak gerçek kanal bandında fiziksel — 2 MHz eski
    dünyanın birim seçimidir."""
    from sim2.cekirdek.degismezler import DegismezHatasi
    with pytest.raises(DegismezHatasi):
        Konfig(kol="t", islem_kazanci=True)


def test_A2_gurultu_tabani_22_MHz_NF7():
    import math
    n = _a2_kanal().yayilim.gurultu_w
    assert 10 * math.log10(n * 1e3) == pytest.approx(-93.55, abs=0.01)


def _esik_db(per_fn, hedef):
    alt, ust = -20.0, 30.0
    for _ in range(80):
        orta = 0.5 * (alt + ust)
        if per_fn(10.0 ** (orta / 10.0)) > hedef:
            alt = orta
        else:
            ust = orta
    return 0.5 * (alt + ust)


def test_A2_PER_SINR_egrisi_ns3_ile_ORTUSUR():
    """🔒 KAPI (`v2/15` A2). ns-3 `DsssErrorRateModel` (depodaki kopya,
    satır 34–57; G1 Pei & Henderson): DBPSK ½e^(−22γ) · DQPSK Ferrari–
    Corazza yaklaşımı x = 11γ. Bizim DQPSK'mız kesin kapalı form → gövde
    eşikleri 0,1 dB içinde; önbelge formülü aynı → birebir. Ölçülen fark
    en çok 0,05 dB (`arsiv/teshis/a2_islem_kazanci_2026-09-26/`)."""
    import math
    kanal = _a2_kanal()
    c = cerceve_kur(kanal.konfig, "veri")
    n, nb = c.hataya_acik_bit, c.onbelge_bit

    def ns3_govde(s):
        x = s * 22e6 / 1e6 / 2.0
        ber = ((math.sqrt(2) + 1.0) / math.sqrt(8.0 * math.pi * math.sqrt(2))
               / math.sqrt(x) * math.exp(-(2.0 - math.sqrt(2)) * x))
        return 1.0 - (1.0 - min(ber, 1.0)) ** n

    for hedef in (0.9, 0.5, 0.1, 0.01):
        bizim = _esik_db(lambda s: kanal.kahin_per(c, s), hedef)
        assert bizim == pytest.approx(_esik_db(ns3_govde, hedef), abs=0.1)
    for db in (-8.0, -6.0, -4.0):
        s = 10.0 ** (db / 10.0)
        ns3 = 1.0 - (1.0 - 0.5 * math.exp(-s * 22.0)) ** nb
        assert kanal.onbelge_per(c, ((float(nb), s),)) == pytest.approx(
            ns3, rel=1e-9)


def test_A2_girisime_karsi_kazanc_TAM_10log11():
    """Açık kanalın PER(γ) = kapalı modelin PER(11γ): girişim ve karıştırma
    SINR'a gürültü gibi girer ve kazancı aynen alır."""
    acik, kapali = _a2_kanal(), _kanal()
    c, c0 = cerceve_kur(acik.konfig, "veri"), cerceve_kur(kapali.konfig, "veri")
    for db in (-2.0, 0.0, 1.0, 2.0):
        s = 10.0 ** (db / 10.0)
        assert acik.kahin_per(c, s) == pytest.approx(
            kapali.kahin_per(c0, 11.0 * s), rel=1e-12)


# ==========================================================================
# A4 · HIZ UYARLAMASI — `v2/15` A4 (K-177)
# ==========================================================================
def _a4_konfig(**ek):
    return Konfig(kol="t", islem_kazanci=True, bant_genisligi_hz=22e6,
                  gurultu_figuru_db=7.0, hiz_uyarlamasi=True, **ek)


def test_A4_KAPALIYKEN_cerceve_BUGUNKU_acikken_HIZ_ve_MODULASYON():
    c0 = cerceve_kur(Konfig(kol="t"), "veri")
    assert (c0.hiz_bps, c0.govde_modulasyonu) == (2e6, "dqpsk")
    k = _a4_konfig()
    assert cerceve_kur(k, "onay").hiz_bps == 1e6
    assert cerceve_kur(k, "beacon").hiz_bps == 1e6
    assert cerceve_kur(k, "veri").hiz_bps == 2e6
    c11 = cerceve_kur(k, "veri", hiz_bps=11e6)
    assert (c11.govde_modulasyonu, c11.govde_ebn0_carpani) == ("cck", 2.0)
    assert c11.sure_s < cerceve_kur(k, "veri", hiz_bps=1e6).sure_s


def test_A4_ISLEM_KAZANCI_ZORUNLU():
    from sim2.cekirdek.degismezler import DegismezHatasi
    with pytest.raises(DegismezHatasi):
        Konfig(kol="t", hiz_uyarlamasi=True)


def test_A4_CCK_SEP16_tablosu_DOGRUDAN_integralle_ORTUSUR():
    """ns-3 GSL formu: SEP₁₆(e) = 1 − ∫_{−β}^{∞} (2Φ(x+β) − 1)^7 φ(x) dx."""
    import math
    import numpy as np
    from scipy.integrate import quad
    from scipy.special import ndtr
    from sim2.kanal.kanal import sep16
    for e in (0.01, 0.3, 1.0, 3.0, 8.0, 15.0):
        b = math.sqrt(2 * e)
        ic = quad(lambda x: (2 * ndtr(x + b) - 1) ** 7 * math.exp(-x * x / 2)
                  / math.sqrt(2 * math.pi), -b, math.inf)[0]
        assert float(sep16(np.array([e]))[0]) == pytest.approx(1 - ic,
                                                               rel=1e-3)


def test_A4_dort_HIZIN_esikleri_SIRALI_ve_KAYNAKLA_UYUMLU():
    """Duyarlılık (PER %10, 512 B, 22 MHz, NF 7): ölçülen −97,0 · −92,5 ·
    −89,9 · −86,9 dBm; 1 ve 2 Mb/s `v2/14`ün kaynaklı değerleriyle aynı."""
    import math
    k = _a4_konfig()
    kanal = Kanal(k, topoloji_kur(k, Akislar(1)))
    gurultu = 10 * math.log10(kanal.yayilim.gurultu_w * 1e3)
    duyarlilik = []
    for h in (1e6, 2e6, 5.5e6, 11e6):
        c = cerceve_kur(k, "veri", hiz_bps=h)
        duyarlilik.append(gurultu + _esik_db(lambda s: kanal.kahin_per(c, s),
                                             0.1))
    assert duyarlilik == sorted(duyarlilik), "yüksek hız daha güçlü sinyal ister"
    for olcu, beklenen in zip(duyarlilik, (-97.0, -92.5, -89.9, -86.9)):
        assert olcu == pytest.approx(beklenen, abs=0.2)


# ==========================================================================
# A7 · REFERANS DÜNYA — `v2/15` A7 (K-178)
# ==========================================================================
def test_A7_referans_BAG_BUTCESI_ile_AYNI_SAYILAR():
    """🔒 KAPI (`v2/15` A7): `arsiv/teshis/referans_dunya_2026-09-25/
    bag_butcesi.py` — EIRP 20 dBm, 22 MHz, NF 7 → gürültü −93,6 dBm; 2 Mb/s
    sönümsüz duyarlılık menzili 5,2 km; 10 dB payla nominal bağ 1,65 km.
    (Betik 576 B'lık çerçeveyle, simülatörün veri çerçevesi 512 B.)"""
    from sim2.kanal.dunya import referans_2026, snr_esigi_db
    from sim2.kanal.kanal import cerceve_per
    from sim2.kanal.yayilim import Yayilim, lin_to_db
    k = referans_2026(kol="t")
    y = Yayilim(k)
    assert y.verici_gucu_w == pytest.approx(0.1)
    assert lin_to_db(y.gurultu_w * 1e3) == pytest.approx(-93.55, abs=0.02)
    assert k.nominal_bag_m == pytest.approx(1650.0, rel=0.03)
    assert y.menzilde_yavas_sinr_db() == pytest.approx(k.menzil_snr_db,
                                                        abs=0.05)
    c = cerceve_kur(k, "veri")
    s10 = snr_esigi_db(lambda s: cerceve_per(c, s), 0.10)
    s50 = snr_esigi_db(lambda s: cerceve_per(c, s), 0.50)
    duyarlilik_menzili = k.nominal_bag_m * 10 ** (
        (k.menzil_snr_db - s10) / (10 * k.yol_kaybi_usteli))
    assert duyarlilik_menzili == pytest.approx(5200.0, rel=0.03)
    assert k.sinr_esigi_db == pytest.approx(s50 + 2 * k.golgeleme_sigma_db)
    # K-185/K-188 (Faz 4.1a): alan 7 km → 33 km — bağ 1 Mb/s'te ~9–10 km
    assert (k.olcek, k.alan_en_m, k.irtifa_min_m, k.irtifa_maks_m) == (
        1.0, 33000.0, 50.0, 300.0)
    assert (k.gm_hiz_min_ms * 3.6, k.gm_hiz_maks_ms * 3.6) == pytest.approx(
        (40.0, 120.0))
    assert (k.yeniden_deneme_siniri, k.cca_s, k.rician_k_db) == (7, 15e-6, 10.0)


def test_A7_ESKI_DUNYA_AYNI_ve_TUTARSIZ_referans_REDDEDILIR():
    from dataclasses import replace
    from sim2.cekirdek.degismezler import DegismezHatasi
    from sim2.kanal.dunya import referans_2026
    from sim2.kanal.yayilim import Yayilim
    k = Konfig(kol="t")
    assert (k.dunya, k.verici_eirp_dbm, k.menzil_snr_db) == (
        "olcek_1_50", None, None)
    with pytest.raises(DegismezHatasi):
        Konfig(kol="t", dunya="referans_2026")
    with pytest.raises(DegismezHatasi):
        Konfig(kol="t", verici_eirp_dbm=20.0)
    r = referans_2026(kol="t")
    with pytest.raises(DegismezHatasi):
        Yayilim(replace(r, nominal_bag_m=2.0 * r.nominal_bag_m))
    with pytest.raises(DegismezHatasi):
        referans_2026(kol="t", sinr_esigi_db=10.0)


def test_A7_referans_KARISTIRICI_TABAN_gucu_darbelide_TELAFI():
    from sim2.kanal.dunya import REFERANS_KARISTIRICI_DBM, referans_2026
    k = referans_2026(kol="t", senaryo="statik-surekli")
    assert k.karistirici_guc_dbm == REFERANS_KARISTIRICI_DBM
    d = referans_2026(kol="t", senaryo="statik-surekli_darbeli")
    assert d.karistirici_guc_dbm == pytest.approx(
        REFERANS_KARISTIRICI_DBM + d.tepe_telafisi_db)


# ==========================================================================
# A8 · REFERANS DÜNYADA BÜTÜN ANAHTARLAR — `v2/15` A8 (K-181)
# ==========================================================================
_ANAHTARLI_SINIRLAR = ("hiz_uyarlamasi", "yayilma_kazanci",
                       "enerji_sezmeli_cca", "yayilim_gecikmesi")


def test_A8_referans_dunyada_BUTUN_anahtarlar_ACIK():
    from sim2.kanal.dunya import referans_2026
    k = referans_2026(kol="t")
    assert (k.islem_kazanci and k.hiz_uyarlamasi and k.yayilim_gecikmesi
            and k.karistirici_gercekci)
    assert k.tasiyici_dinleme == "guc"
    eski = Konfig(kol="t")
    assert not (eski.islem_kazanci or eski.hiz_uyarlamasi
                or eski.yayilim_gecikmesi or eski.karistirici_gercekci), \
        "varsayılan eski dünyada kalır"


def test_A8_kapsam_ANAHTARLI_siniri_satirdan_OKUR():
    """🔴 Anahtarı açık koşu o sınırı "modellenmeyen" diye beyan etmez;
    kapalı koşu eder. Liste Faz 1'de güncellenmemişti (K-181)."""
    from sim2.kanal.dunya import referans_2026
    from sim2.yapilandirma.kapsam import MODELLENMEYEN, kapsam_bolumu
    tam = {ad for ad, _ in MODELLENMEYEN}
    assert set(_ANAHTARLI_SINIRLAR) <= tam
    assert set(kapsam_bolumu(Konfig(kol="t"))["modellenmeyen"]) == tam
    ref = kapsam_bolumu(referans_2026(kol="t"))["modellenmeyen"]
    assert set(ref) == tam - set(_ANAHTARLI_SINIRLAR)
    tek = kapsam_bolumu(Konfig(kol="t", tasiyici_dinleme="guc"))
    assert set(tek["modellenmeyen"]) == tam - {"enerji_sezmeli_cca"}


def test_K188_kapsam_THETA_ve_BOLUNME_satirin_DUNYASINDAN():
    """🔴 K-188: referans satırı eski dünyanın Θ'sını ve bölünme payını
    beyan ediyordu. Satır kendi dünyasının tablosunu okur."""
    from sim2.kanal.dunya import referans_2026
    from sim2.yapilandirma.kapsam import kapsam_bolumu
    from sim2.yapilandirma.senaryolar import (MOBILITE_THETA,
                                              MOBILITE_THETA_REFERANS)
    ref = kapsam_bolumu(referans_2026(kol="t", senaryo="bagimsiz-yok",
                                      tohum=2007))
    assert ref["theta_olsr"] == MOBILITE_THETA_REFERANS["bagimsiz"][0]
    assert ref["bolunme_payi"] == pytest.approx(0.2222)
    eski = kapsam_bolumu(Konfig(kol="t", senaryo="bagimsiz-yok", tohum=2007))
    assert eski["theta_olsr"] == MOBILITE_THETA["bagimsiz"][0]
    assert eski["bolunme_payi"] == pytest.approx(0.1111)
