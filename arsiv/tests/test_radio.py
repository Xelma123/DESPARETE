"""
Radyo katmanı testleri.

⭐ Bu dosyanın ilk bölümü AİLE 0 / K3'ün kendisidir: "analitik kontroller".
Yani buradaki testler yalnızca kodun çalıştığını değil, ARACIN FİZİĞE
UYDUĞUNU gösterir. Rapora doğrudan girerler.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sim.config import DIRSEK_TARAMASI_DBM, Konfig, SENARYO_TANIMLARI  # noqa: E402
from sim.radio import (  # noqa: E402
    BOLTZMANN, ISIK_HIZI, Karistirici, Radyo, db_to_lin, dbm_to_w, w_to_dbm,
)
from sim.rng import Akislar  # noqa: E402


@pytest.fixture
def kon() -> Konfig:
    return Konfig(kol="test")


@pytest.fixture
def radyo(kon: Konfig) -> Radyo:
    return Radyo.kur(kon)


# ==========================================================================
# AİLE 0 / K3 — ANALİTİK DOĞRULAMA
# ==========================================================================

def test_termal_gurultu_ders_kitabi_degeri(kon):
    """290 K'de 1 MHz bant için kTB ≈ -114 dBm."""
    termal = BOLTZMANN * kon.sicaklik_k * kon.bant_genisligi_hz
    assert w_to_dbm(termal) == pytest.approx(-114.0, abs=0.1)


def test_gurultu_tabani_figurle_birlikte(kon):
    n = Radyo.gurultu_tabani_w(kon)
    assert w_to_dbm(n) == pytest.approx(-114.0 + kon.gurultu_figuru_db, abs=0.1)


def test_yol_kaybi_1m_de_friis(radyo, kon):
    """1 m referansta log-mesafe modeli serbest uzaya (Friis) EŞİT olmalı."""
    friis = 20.0 * math.log10(4.0 * math.pi * 1.0 * kon.frekans_hz / ISIK_HIZI)
    assert radyo.yol_kaybi_db(1.0) == pytest.approx(friis, abs=1e-9)


def test_yol_kaybi_dekat_basina_10alfa(radyo, kon):
    """Mesafe 10 katına çıkınca kayıp tam 10·α dB artmalı."""
    for d in (5.0, 28.0, 100.0):
        artis = radyo.yol_kaybi_db(d * 10) - radyo.yol_kaybi_db(d)
        assert artis == pytest.approx(10.0 * kon.yol_kaybi_usteli, abs=1e-9)


def test_menzil_sinirinda_sinr_tam_esik(radyo, kon):
    """🔑 TANIM: iletim menzili, girişimsiz SINR'in tam eşiğe eşit olduğu mesafedir.

    Bu test tutmazsa, topolojinin geometrik menzili ile radyonun fiziği
    çelişiyor demektir — ve hangi düğümlerin komşu olduğu iki farklı cevap
    verir.
    """
    s = radyo.alinan_guc_w(kon.iletim_menzili_m)
    assert radyo.sinr_db(s) == pytest.approx(kon.sinr_esigi_db, abs=1e-9)


def test_verici_gucu_makul_araliкta(radyo):
    """Türetilen Pt fiziksel olarak anlamlı olmalı (küçük İHA telsizi)."""
    pt_dbm = w_to_dbm(radyo.verici_gucu_w)
    assert 0.0 < pt_dbm < 30.0, f"Pt = {pt_dbm:.1f} dBm — gerçekçi değil"


def test_girisim_orani_turetilmis_ve_tutarli(kon, radyo):
    """Girişim menzilindeki bir kaynağın gücü GÜRÜLTÜ TABANINA eşit olmalı.

    Bu, girisim_orani = β^(1/α) türetiminin doğrudan sınanmasıdır. Oran elle
    yazılmış olsaydı (eski hâli 2,2) bu test kırılırdı.
    """
    assert kon.girisim_orani == pytest.approx(
        db_to_lin(kon.sinr_esigi_db) ** (1.0 / kon.yol_kaybi_usteli)
    )
    guc = radyo.alinan_guc_w(kon.girisim_menzili_m)
    # 🔴 B-22: `abs=0.0` ZORUNLU. pytest.approx'un varsayılan MUTLAK
    # toleransı 1e-12'dir ve yalnızca `rel` verildiğinde tolerans
    # max(rel*beklenen, 1e-12) olur. Karşılaştırılan güçler ~1e-14 W
    # olduğu için taban her farkı yutuyordu: bu iddia KIRILAMIYORDU.
    assert guc == pytest.approx(radyo.gurultu_gucu_w, rel=1e-9, abs=0.0)


def test_girisim_menzili_iletimden_genis(kon):
    """Gizli terminalin ön koşulu — Li replikasyonu buna bağlı."""
    assert kon.girisim_menzili_m > kon.iletim_menzili_m


# ==========================================================================
# Hata modeli
# ==========================================================================

def test_ber_kapali_form(radyo):
    """Eşevresiz DBPSK: BER = ½·e^(−γ)."""
    for gamma in (0.5, 1.0, 5.0, 10.0, 20.0):
        # 🔴 B-35 — `abs=0.0` ZORUNLU (Y10, kalan vaka).
        # γ = 20'de beklenen değer 1,031e−9; `approx`ın varsayılan mutlak
        # tabanı 1e−12 → ETKİN göreli tolerans 9,7e−4, yani ilan edilen
        # `rel=1e-6`'nın **970 katı**. Kırılamaz değildi ama ilan edilen
        # hassasiyette BAĞLAYICI değildi. B-22 beş vakayı düzeltmişti;
        # tarama yalnızca denetimin adını verdiklerine uygulanmıştı.
        assert radyo.bit_hata_orani(gamma) == pytest.approx(
            0.5 * math.exp(-gamma), rel=1e-9, abs=0.0)


def test_ber_sinirlari(radyo):
    assert radyo.bit_hata_orani(0.0) == pytest.approx(0.5)
    assert radyo.bit_hata_orani(1e6) == pytest.approx(0.0, abs=1e-12)


def test_per_monoton_azalan(radyo, kon):
    """SINR arttıkça PER kesinlikle azalmalı."""
    onceki = 1.1
    for sinr_db in range(-10, 41, 2):
        per = radyo.paket_hata_olasiligi(db_to_lin(sinr_db), kon.paket_bayt)
        assert per <= onceki
        onceki = per


def test_per_uzun_pakette_daha_yuksek(radyo):
    """Aynı SINR'de uzun paket daha çok hata yapar."""
    g = db_to_lin(11.0)
    assert (radyo.paket_hata_olasiligi(g, 2048)
            > radyo.paket_hata_olasiligi(g, 1024)
            > radyo.paket_hata_olasiligi(g, 64))


def test_per_tasma_yapmiyor(radyo):
    """Çok uzun paket + çok düşük SINR'de (1-BER)^n taşmamalı."""
    per = radyo.paket_hata_olasiligi(db_to_lin(-30.0), 65535)
    assert 0.0 <= per <= 1.0 and not math.isnan(per)


def test_per_cok_kucuk_deger_de_dogru(radyo):
    """Yüksek SINR'de PER sıfıra yuvarlanmamalı — expm1/log1p kullanımı.

    Naif (1-ber)**n hesabı burada kayan nokta hassasiyetinde sıfır verir
    ve ETX = 1.000 sanılır. Gerçekte küçük ama sıfır olmayan bir kayıp var.
    """
    per = radyo.paket_hata_olasiligi(db_to_lin(20.0), 1024)
    assert 0.0 < per < 1e-6


# ==========================================================================
# Karıştırıcı
# ==========================================================================

def test_s0_karistirici_yok():
    kon = Konfig(kol="t", senaryo="S0")
    assert kon.karistirici_var_mi is False
    assert Karistirici.senaryodan(kon, Akislar(1)) is None


@pytest.mark.parametrize("senaryo", ["S1", "S2", "S3", "S4", "S5"])
def test_karistiricili_senaryolarda_karistirici_var(senaryo):
    kon = Konfig(kol="t", senaryo=senaryo)
    assert Karistirici.senaryodan(kon, Akislar(1)) is not None


def test_karistirici_gucu_mesafeyle_azaliyor(kon):
    kj = Karistirici.senaryodan(Konfig(kol="t", senaryo="S2"), Akislar(1))
    merkez = kon.karistirici_merkez
    yakin = kj.alinan_guc_w((merkez[0] + 50, merkez[1]), 0.0)
    uzak = kj.alinan_guc_w((merkez[0] + 500, merkez[1]), 0.0)
    assert yakin > uzak > 0.0


def test_darbeli_gorev_cevrimi_dogru():
    """Açık kalma oranı, görev çevrimine eşit olmalı."""
    kon = Konfig(kol="t", senaryo="S4")
    kj = Karistirici.senaryodan(kon, Akislar(1))
    assert kj.darbeli is True
    ornek = 200_000
    adim = kon.darbe_periyodu_s * 7.13 / ornek     # periyotla ölçüşmeyen adım
    acik = sum(1 for i in range(ornek) if kj.acik_mi(i * adim))
    assert acik / ornek == pytest.approx(kon.darbe_gorev_cevrimi, abs=0.01)


def test_darbe_fazi_tohuma_gore_degisiyor():
    """🔴 REZONANS KORUMASI.

    Faz sabit olsaydı, darbe treni her tohumda aynı anda başlar ve CBR
    trafiğiyle sistematik olarak aynı fazda karşılaşırdı.
    """
    kon = Konfig(kol="t", senaryo="S4")
    fazlar = {Karistirici.senaryodan(kon, Akislar(t)).faz_kesri for t in range(1, 21)}
    assert len(fazlar) == 20


def test_darbe_periyodu_cbr_araligiyla_olcusmuyor():
    """Periyotlar ölçüşürse (biri diğerinin tam katıysa) örnekler kilitlenir."""
    kon = Konfig(kol="t")
    oran = kon.darbe_periyodu_s / kon.cbr_araligi_s
    assert abs(oran - round(oran)) > 0.1, "darbe periyodu CBR aralığının katı"


def test_darbeli_tepe_gucu_ortalamayi_esitliyor():
    """⭐ H1.3'ün kurulumu: S2 ile S4 aynı ORTALAMA güce sahip olmalı.

    Eşit değilse H1.3 "aynı ortalama güçte yapı fark eder mi" sorusunu
    değil, "daha çok güç daha çok zarar verir mi" sorusunu sorar — ki o
    zaten bilinen bir şeydir.
    """
    for sabit, darbeli in (("S1", "S3"), ("S2", "S4")):
        # 🔴 B-07: sayı artık tablodan DEĞİL, koşan sistemin kullandığı
        # `Konfig.karistirici_guc_dbm` property'sinden okunuyor. Tablodan
        # okumak, kodun fiilen kullandığı yolu ATLAMAK olurdu.
        p_sabit = dbm_to_w(Konfig(kol="t", senaryo=sabit).karistirici_guc_dbm)
        kon = Konfig(kol="t", senaryo=darbeli)
        p_tepe = dbm_to_w(kon.karistirici_guc_dbm)
        # 🔴 B-22: `abs=0.0` ZORUNLU. pytest.approx'un varsayılan MUTLAK
        # toleransı 1e-12'dir ve yalnızca `rel` verildiğinde tolerans
        # max(rel*beklenen, 1e-12) olur. Karşılaştırılan güçler ~1e-14 W
        # olduğu için taban her farkı yutuyordu: bu iddia KIRILAMIYORDU.
        assert p_tepe * kon.darbe_gorev_cevrimi == pytest.approx(
            p_sabit, rel=1e-9, abs=0.0)


def test_hareketli_karistirici_konumu_degisiyor():
    kon = Konfig(kol="t", senaryo="S5")
    kj = Karistirici.senaryodan(kon, Akislar(1))
    assert kj.hareketli is True
    konumlar = {kj.konum_t(t) for t in (0.0, 10.0, 30.0, 60.0)}
    assert len(konumlar) == 4


def test_hareketli_yorunge_yaricapi_sabit():
    """Yörünge dairesel: merkeze uzaklık her zaman yarıçapa eşit."""
    kon = Konfig(kol="t", senaryo="S5")
    kj = Karistirici.senaryodan(kon, Akislar(1))
    for t in (0.0, 7.3, 55.1, 300.0):
        x, y = kj.konum_t(t)
        d = math.hypot(x - kj.konum[0], y - kj.konum[1])
        assert d == pytest.approx(kon.karistirici_yorunge_yaricap_m)


def test_sabit_karistirici_hareket_etmiyor():
    kon = Konfig(kol="t", senaryo="S2")
    kj = Karistirici.senaryodan(kon, Akislar(1))
    assert kj.konum_t(0.0) == kj.konum_t(1000.0) == kj.konum


def test_sabit_karistirici_hep_acik():
    kon = Konfig(kol="t", senaryo="S2")
    kj = Karistirici.senaryodan(kon, Akislar(1))
    assert all(kj.acik_mi(t) for t in (0.0, 1.3, 99.9, 350.0))


# ==========================================================================
# Senaryo bütünlüğü
# ==========================================================================

def test_karistirici_gucu_elle_ayarlanamiyor():
    """Senaryo etiketi yalan söyleyemez: güç senaryodan türetilir."""
    kon = Konfig(kol="t", senaryo="S2")
    assert kon.karistirici_guc_dbm == SENARYO_TANIMLARI["S2"]["esdeger_sabit_guc_dbm"]
    with pytest.raises(Exception):
        kon.karistirici_guc_override_dbm = 99.0   # type: ignore[misc]


def test_dirsek_taramasi_pencereyi_kapsiyor():
    """Tarama, 'etki yok'tan 'ağ bölündü'ye kadar uzanmalı.

    Aksi hâlde 'düz eğri' ile 'aracımız göremiyor' ayırt edilemez.
    """
    assert min(DIRSEK_TARAMASI_DBM) <= -10.0
    assert max(DIRSEK_TARAMASI_DBM) >= 10.0
    assert len(DIRSEK_TARAMASI_DBM) >= 8


def test_override_sonuc_satirinda_gorunuyor():
    """Dirsek taraması gücü konfigürasyonda AÇIKÇA görünmeli."""
    kon = Konfig(kol="t", senaryo="S2", karistirici_guc_override_dbm=7.5)
    assert kon.karistirici_guc_dbm == 7.5
    assert kon.sozluk()["karistirici_guc_override_dbm"] == 7.5


# ==========================================================================
# 🔴 B-14 — `Karistirici` dataclass'ında ikinci "doğru" kaynağı
# ==========================================================================

def test_b14_karistiricinin_hicbir_alaninda_varsayilan_yok():
    """🔴 B-14 REGRESYONU — varsayılan = sessiz ikinci doğru kaynağı.

    Dört alan (`periyot_s · gorev_cevrimi · hiz_ms · yorunge_yaricap_m`)
    `Konfig`in birebir kopyasıydı; `faz_kesri` ise varsayılan `0.0` ile
    REZONANS KORUMASININ KAPALI hâliydi.

    Bugün zararsızdı (tek çağıran `senaryodan()` hepsini geçiyor) — ama tam
    olarak bu desen bir kez gerçek bir hataya yol açtı: `rng.kanal_cekimi`in
    varsayılan dilimi 1 ms'de kalırken `Konfig` 100 µs'ye inmişti (K-024).

    Bu test, varsayılanın GERİ EKLENMESİNİ engeller.
    """
    from dataclasses import MISSING, fields

    varsayilanli = [
        f.name for f in fields(Karistirici)
        if f.default is not MISSING or f.default_factory is not MISSING
    ]
    assert varsayilanli == [], (
        f"Karistirici alanlarına varsayılan geri gelmiş: {varsayilanli}. "
        f"Her varsayılan, Konfig ile ikinci bir 'doğru' kaynağıdır (B-14)."
    )


def test_b14_senaryodan_her_alani_acikca_geciyor():
    """Y8 — bozulan yolun sağlam koşuda TETİKLENDİĞİNİ önce göster.

    Varsayılan yasağı ancak `senaryodan()` gerçekten her alanı geçiyorsa
    anlamlıdır. Aksi hâlde yukarıdaki test bir `TypeError`ı garanti eder,
    bir sözleşmeyi değil.
    """
    from dataclasses import fields

    kon = Konfig(kol="t", senaryo="S5")
    kj = Karistirici.senaryodan(kon, Akislar(7))
    assert kj is not None
    for f in fields(Karistirici):
        assert getattr(kj, f.name) is not None, f.name
    # Konfig'ten gelmesi gereken dördü birebir eşleşmeli
    assert kj.periyot_s == kon.darbe_periyodu_s
    assert kj.gorev_cevrimi == kon.darbe_gorev_cevrimi
    assert kj.hiz_ms == kon.karistirici_hiz_ms
    assert kj.yorunge_yaricap_m == kon.karistirici_yorunge_yaricap_m
    assert 0.0 <= kj.faz_kesri < 1.0
