"""
ADIM 4 — `kanal/cerceve.py` ve `kanal/yayilim.py` kapanış ölçütleri.

Bu dosyanın koruduğu iki şey:
  1. 🔴 **Kusur 1**: çerçeve süresi ve hataya açık bit TEK yerde tanımlı.
     Ölçüldü — yeni parametrelerde iki tanım arasındaki fark %2,34'ten
     **%9,38'e** çıkıyor, yani kusur büyüyordu.
  2. Yayılımın her parçasının **analitik** karşılığı var: Friis · kTB ·
     dekat başına 10α · dipol kapalı formu · menzilde SINR = β.
"""

from __future__ import annotations

import ast
import math
import pathlib
import statistics as ist
import sys

import pytest

KOK = pathlib.Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))
SIM2 = KOK / "sim2"

from sim2.dunya.geometri import Nokta3  # noqa: E402
from sim2.kanal.cerceve import CERCEVE_TIPLERI, cerceve_kur  # noqa: E402
from sim2.kanal.yayilim import (BOLTZMANN, Yayilim, db_to_lin,  # noqa: E402
                                lin_to_db, w_to_dbm)
from sim2.yapilandirma.konfig import Konfig  # noqa: E402

K = Konfig(kol="test")
Y = Yayilim(K)


# ==========================================================================
# ÇERÇEVE — kusur 1
# ==========================================================================

def test_cerceve_suresi_ANALITIK():
    """512 B @ 2 Mb/s + 192 µs önbelge = 2240 µs."""
    c = cerceve_kur(K, "veri")
    assert c.sure_s == pytest.approx(192e-6 + 4096 / 2e6)
    assert c.sure_s == pytest.approx(2240e-6)
    o = cerceve_kur(K, "onay")
    assert o.sure_s == pytest.approx(192e-6 + 112 / 2e6)
    assert o.sure_s == pytest.approx(248e-6)


def test_hataya_acik_bit_ONBELGEYI_SAYMIYOR():
    """🔴 Kusur 1'in kalbi.

    Önbelge 1 Mb/s DBPSK ile gönderilir, gövde 2 Mb/s DQPSK ile. Süreyi gövde
    bit hızıyla çarpmak, 192 µs'lik dayanıklı önbelgeyi 384 kırılgan gövde
    biti gibi saymak olurdu — yalnızca tutarsız değil, fiziksel olarak yanlış.
    """
    c = cerceve_kur(K, "veri")
    assert c.hataya_acik_bit == 4096
    yanlis = round(c.sure_s * K.bit_hizi_bps)
    assert yanlis == 4480
    assert (yanlis / c.hataya_acik_bit - 1) == pytest.approx(0.09375, abs=1e-6)


def test_sure_ONBELGEYI_iceriyor():
    """İki büyüklük ayrı olduğu için ikisi de doğru olabiliyor: kanal
    önbelge boyunca meşguldür, gövde hatası onu içermez."""
    c = cerceve_kur(K, "veri")
    assert c.sure_s > c.hataya_acik_bit / K.bit_hizi_bps
    assert c.govde_suresi_s == pytest.approx(4096 / 2e6)


def test_tip_basina_boyut_KONFIGDEN():
    assert cerceve_kur(K, "veri").bayt == K.paket_bayt
    assert cerceve_kur(K, "onay").bayt == K.onay_bayt
    assert cerceve_kur(K, "beacon").bayt == K.beacon_bayt
    assert cerceve_kur(K, "veri").veri_duzlemi_mi is True
    assert cerceve_kur(K, "onay").veri_duzlemi_mi is False


def test_bilinmeyen_tip_ve_gecersiz_boyut_REDDEDILIYOR():
    from sim2.cekirdek.degismezler import DegismezHatasi
    with pytest.raises(ValueError):
        cerceve_kur(K, "telepati")
    with pytest.raises(DegismezHatasi):
        cerceve_kur(K, "veri", bayt=0)


def test_cerceve_DONDURULMUS():
    import dataclasses
    c = cerceve_kur(K, "veri")
    with pytest.raises(dataclasses.FrozenInstanceError):
        c.sure_s = 1.0  # type: ignore[misc]


def test_TEK_bit_sayimi_VAR():
    """🔴 Kusur 1'in geri gelme yolunu kapatan test.

    `bit_hizi_bps` veya `onbelge_s` ile ARİTMETİK yapan tek yer
    `kanal/cerceve.py` olmalı. Karşılaştırma (doğrulama) serbesttir;
    çarpma/bölme değil.
    """
    yasak = {"bit_hizi_bps", "onbelge_s"}
    ihlal: list[str] = []
    for yol in sorted(SIM2.rglob("*.py")):
        if "__pycache__" in yol.parts or yol.name == "cerceve.py":
            continue
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        for n in ast.walk(agac):
            if not isinstance(n, ast.BinOp):
                continue
            for alt in ast.walk(n):
                if isinstance(alt, ast.Attribute) and alt.attr in yasak:
                    ihlal.append(
                        f"{yol.relative_to(KOK).as_posix()}:{n.lineno} "
                        f"→ {alt.attr}")
    assert not ihlal, (
        f"🔴 İKİNCİ bir bit/süre sayımı yazılmış: {ihlal}. Ölçüldü — iki "
        f"tanım 512 B @ 2 Mb/s'te %9,38 ayrışıyor.")


# ==========================================================================
# GÜRÜLTÜ ve VERİCİ GÜCÜ — analitik
# ==========================================================================

def test_gurultu_tabani_kTB_ANALITIK():
    """N = k·T·B·F. 290 K, 2 MHz, 6 dB → ≈ −105,0 dBm."""
    beklenen = BOLTZMANN * 290.0 * 2e6 * db_to_lin(6.0)
    assert Y.gurultu_w == pytest.approx(beklenen, rel=1e-12)
    assert w_to_dbm(Y.gurultu_w) == pytest.approx(-104.97, abs=0.02)


def test_bant_iki_katina_cikinca_gurultu_3dB_artiyor():
    dar = Yayilim(Konfig(kol="t", bant_genisligi_hz=1e6))
    assert (w_to_dbm(Y.gurultu_w) - w_to_dbm(dar.gurultu_w)) \
        == pytest.approx(10.0 * math.log10(2.0), abs=1e-9)


def test_yol_kaybi_1m_FRIIS():
    """PL(1 m) = 20·log10(4π·f/c). 2,4 GHz'de ≈ 40,05 dB."""
    assert Y.yol_kaybi_db(1.0) == pytest.approx(40.05, abs=0.02)


def test_dekat_basina_10_alfa():
    for d in (10.0, 50.0, 200.0):
        fark = Y.yol_kaybi_db(10.0 * d) - Y.yol_kaybi_db(d)
        assert fark == pytest.approx(10.0 * K.yol_kaybi_usteli, abs=1e-9)


def test_verici_gucu_MENZILDEN_turetiliyor():
    """🔒 Kapalı devre: menzilde SINR tam olarak β olmalı."""
    assert Y.menzilde_yavas_sinr_db() == pytest.approx(K.sinr_esigi_db, abs=1e-9)
    # ⚠️ DEĞER İKİ KEZ DEĞİŞTİ ve ikisi de TÜRETİLMİŞ bir sonucun kaymasıdır:
    #   β 10 → 16 dB   (5 Eylül)  →  18,50 → 24,50 dBm
    #   α  3 → 2       (5 Eylül)  →  24,50 →  0,03 dBm
    #
    # 🔴 0,03 dBm ≈ 1 mW İLK BAKIŞTA SAÇMA GÖRÜNÜR — değildir. Bu simülatör
    # 1:50 geometrik ölçek modelidir; aynı SINR'ı korumak için
    #     Pt_gerçek = Pt_sim + 10·α·log₁₀(50) = 0,03 + 34,0 = 34,0 dBm
    # yani **2,5 W** — makul bir taktik İHA veri bağı. α = 3 iken aynı hesap
    # 75,5 dBm = 35 kW veriyordu, yani var olamayacak bir telsiz. Ölçek
    # tutarlılığı, α'yı seçen iki hesaptan biriydi (K-096).
    #
    # 🔒 Bu sayı bir GİRDİ değil; menzil + eşik + yol kaybı üstelinden ÇIKAR.
    # Burada sabitlenmesinin sebebi onu dondurmak değil, sessizce kaymasını
    # engellemek: değiştiğinde bu test kırılır ve gerekçesi yazılmak zorunda
    # kalır. Yukarıdaki ilk `assert` ise gerçek kapalı devre kapısıdır ve
    # α'dan da β'dan da bağımsız olarak tutmak zorundadır.
    assert w_to_dbm(Y.verici_gucu_w) == pytest.approx(0.03, abs=0.02)


def test_menzil_degisince_guc_DA_degisiyor():
    """Elle yazılmış olsaydı menzil ile fizik çelişebilirdi."""
    uzak = Yayilim(Konfig(kol="t", nominal_bag_m=560.0))
    fark = w_to_dbm(uzak.verici_gucu_w) - w_to_dbm(Y.verici_gucu_w)
    assert fark == pytest.approx(10.0 * K.yol_kaybi_usteli * math.log10(2.0),
                                 abs=1e-9)
    assert uzak.menzilde_yavas_sinr_db() == pytest.approx(K.sinr_esigi_db,
                                                          abs=1e-9)


# ==========================================================================
# ANTEN DESENİ — kapalı form
# ==========================================================================

def test_dipol_yatayda_KAYIPSIZ():
    assert Y.anten_kaybi_db(0.0) == pytest.approx(0.0, abs=1e-12)


def test_dipol_kaybi_yukselisle_ARTIYOR_ve_kapali_formu_tutuyor():
    onceki = -1.0
    for derece in (0, 10, 20, 30, 40, 50, 60, 70, 80):
        phi = math.radians(derece)
        kayip = Y.anten_kaybi_db(phi)
        beklenen = -20.0 * math.log10(
            math.cos(0.5 * math.pi * math.sin(phi)) / math.cos(phi))
        assert kayip == pytest.approx(beklenen, abs=1e-9)
        assert kayip > onceki
        onceki = kayip


def test_dipol_OLCULEN_p95_degerini_veriyor():
    """🔒 Anten kararını çeviren ölçüm: 120 m bandında yükseliş p95 = 40,6°
    ve orada tek uç kaybı 3,27 dB. 300 m bandında p95 = 66,4° → 9,70 dB."""
    assert Y.anten_kaybi_db(math.radians(40.6)) == pytest.approx(3.27, abs=0.05)
    assert Y.anten_kaybi_db(math.radians(66.4)) == pytest.approx(9.70, abs=0.1)


def test_bagda_IKI_anten_var():
    a, b = Nokta3(0.0, 0.0, 20.0), Nokta3(100.0, 0.0, 120.0)
    tek = Y.anten_kaybi_db(math.atan2(100.0, 100.0))
    assert Y.bag_anten_kaybi_db(a, b) == pytest.approx(2.0 * tek)
    assert Y.bag_anten_kaybi_db(a, b) == pytest.approx(Y.bag_anten_kaybi_db(b, a))


def test_anten_ablasyonu():
    kapali = Yayilim(Konfig(kol="t", anten_deseni_acik=False))
    for derece in (0, 30, 60, 85):
        assert kapali.anten_kaybi_db(math.radians(derece)) == 0.0


# ==========================================================================
# GÖLGELEME
# ==========================================================================

def _rastgele_noktalar(n, tohum=5):
    import random
    r = random.Random(tohum)
    return [(Nokta3(r.uniform(0, 1000), r.uniform(0, 1000), r.uniform(20, 120)),
             Nokta3(r.uniform(0, 1000), r.uniform(0, 1000), r.uniform(20, 120)))
            for _ in range(n)]


def test_sigma_SIFIRDA_golgeleme_kapali_haline_BIREBIR():
    """🔒 Kapanış ölçütü (b)."""
    sifir = Yayilim(Konfig(kol="t", golgeleme_sigma_db=0.0))
    kapali = Yayilim(Konfig(kol="t", golgeleme_acik=False))
    for i, (a, b) in enumerate(_rastgele_noktalar(50)):
        assert sifir.golgeleme_db(i, i + 1, a, b) == 0.0
        assert kapali.golgeleme_db(i, i + 1, a, b) == 0.0
        assert (sifir.yavas_kayip_db(i, i + 1, a, b)
                == kapali.yavas_kayip_db(i, i + 1, a, b))


def test_golgeleme_ILAN_EDILEN_sigmayi_veriyor():
    """🔴 Trilineer ağırlıklar varyansı düşürür; düzeltme olmasaydı ilan
    edilen σ alanın çoğunda GERÇEKLEŞMEZDİ (hücre merkezinde 1/8'e kadar)."""
    ornekler = [Y.golgeleme_db(i % 40, (i * 7 + 3) % 40, a, b)
                for i, (a, b) in enumerate(_rastgele_noktalar(3000, tohum=11))]
    olculen = ist.pstdev(ornekler)
    assert olculen == pytest.approx(K.golgeleme_sigma_db, rel=0.08), (
        f"ölçülen σ {olculen:.3f}, ilan edilen {K.golgeleme_sigma_db}")
    assert abs(ist.mean(ornekler)) < 0.3


def test_golgeleme_BAG_SIMETRIK():
    for i, (a, b) in enumerate(_rastgele_noktalar(40)):
        assert Y.golgeleme_db(3, 17, a, b) == Y.golgeleme_db(17, 3, a, b)
        assert Y.golgeleme_db(3, 17, a, b) == Y.golgeleme_db(3, 17, b, a)


def test_golgeleme_SUREKLI_isinlanma_yok():
    """🔒 Hareket eden düğüm gölgeleme alanında sürekli ilerlemeli.

    Hücre sınırını geçerken de sıçrama olmamalı — trilineer yumuşatmanın
    varlık sebebi budur.
    """
    h = K.golgeleme_hucre_m
    a = Nokta3(500.0, 500.0, 70.0)
    en_buyuk = 0.0
    for adim in range(400):
        # Bağ ortası tam olarak hücre sınırlarından geçsin diye seçildi.
        b1 = Nokta3(500.0 + adim * h / 20.0, 500.0, 70.0)
        b2 = Nokta3(500.0 + (adim + 1) * h / 20.0, 500.0, 70.0)
        fark = abs(Y.golgeleme_db(1, 2, a, b1) - Y.golgeleme_db(1, 2, a, b2))
        en_buyuk = max(en_buyuk, fark)
    assert en_buyuk < 1.5, (
        f"🔴 gölgeleme {en_buyuk:.2f} dB sıçradı — düğüm ışınlanıyor")


def test_golgeleme_FARKLI_baglar_farkli_deger():
    a, b = Nokta3(300.0, 300.0, 60.0), Nokta3(450.0, 320.0, 80.0)
    degerler = {Y.golgeleme_db(i, i + 20, a, b) for i in range(15)}
    assert len(degerler) == 15


def test_golgeleme_BELIRLENIMCI():
    a, b = Nokta3(123.0, 456.0, 78.0), Nokta3(321.0, 654.0, 87.0)
    assert Y.golgeleme_db(2, 9, a, b) == Y.golgeleme_db(2, 9, a, b)
    baska = Yayilim(Konfig(kol="t", tohum=K.tohum + 1))
    assert baska.golgeleme_db(2, 9, a, b) != Y.golgeleme_db(2, 9, a, b)


# ==========================================================================
# YAVAŞ SINR — `kopma_fiziksel`in temeli
# ==========================================================================

def test_yavas_sinr_menzilde_ESIGE_esit_temiz_kosulda():
    kapali = Yayilim(Konfig(kol="t", golgeleme_acik=False,
                            anten_deseni_acik=False))
    a = Nokta3(0.0, 0.0, 70.0)
    b = Nokta3(K.nominal_bag_m, 0.0, 70.0)   # yatay bağ → yükseliş 0
    assert kapali.yavas_sinr_db(0, 1, a, b) == pytest.approx(K.sinr_esigi_db,
                                                             abs=1e-9)
    assert kapali.bag_kopuk_mu(0, 1, a, b) is False


def test_menzil_disi_bag_KOPUK():
    kapali = Yayilim(Konfig(kol="t", golgeleme_acik=False,
                            anten_deseni_acik=False))
    a = Nokta3(0.0, 0.0, 70.0)
    b = Nokta3(K.nominal_bag_m * 1.5, 0.0, 70.0)
    assert kapali.bag_kopuk_mu(0, 1, a, b) is True


def test_girisim_SINRi_dusuruyor():
    a, b = Nokta3(0.0, 0.0, 70.0), Nokta3(200.0, 0.0, 70.0)
    temiz = Y.yavas_sinr_db(0, 1, a, b)
    kirli = Y.yavas_sinr_db(0, 1, a, b, girisim_w=Y.gurultu_w)
    assert kirli == pytest.approx(temiz - 10.0 * math.log10(2.0), abs=1e-9)
