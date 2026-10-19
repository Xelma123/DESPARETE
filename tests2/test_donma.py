"""Taban protokollerin donması ve okunan gözlemin kökeni (denetim 2026-10-08).

D-12: `protokol_hash` paket düzeyindedir — DESPARETE'nin bir dosyası değişince
taban protokol satırlarının kimliği de değişir, yani satır kimliği "taban
protokoller dondu" iddiasını kanıtlayamaz. Bu test dosyaların kendisini
bağlar: bir taban protokol dosyası değişirse kırılır ve yeni bir K kaydı,
U1 ve regresyon ister (`v2/04` §5). Değerler K-224'ün donmuş hâli; Faz 4b'nin
rakipleri (JarmRout-b · OLSRv2-b) K-239'da eklendi; AODV-k ve Babel-a
K-249'da (K-244 kuyruğu).

D-16: protokol bir ölçüm alanını okumaya başlarsa mimari denetimi o alanın
köken kaydını DUYARSIZ bırakmaz.
"""
from __future__ import annotations

import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.cekirdek.kimlik import dosya_hash  # noqa: E402

# K-224 (10 Ekim 2026): AOMDV-f (K-218'den beri aynı) · OLSR-d (K-223)
# + koşum protokolleri. AODV K-249'da `AODV-k`ye geçti (aşağıda).
DONMUS: dict[str, str] = {
    # K-249 (17 Ekim 2026): `AODV-k` (K-243 · K-244) — ölçülen kopya
    # 1163f81 (K-244 kuyruğu) ile birebir; AODV-j'ninkiler 1d39ba7d · 73ba004b.
    "aodv.py": "70b5e9d2d57faee1405b060f78f1c586",
    "aodv_bicim.py": "8e36200e4375a460d7586ae14a090df2",
    "olsr.py": "f5a93933860a05221ee8866d6df455ed",
    "olsr_bicim.py": "b813f12cad77454da1e134af4a45c151",
    "aomdv.py": "3d2d037a012431b21ab1381e22d3882f",
    "aomdv_bicim.py": "ca9c20feaafb51dac524c9af14238a48",
    "kosum_kosumu.py": "e175ba6cc74a80a5cca9c7789ac39ac7",
    # K-239 (13 Ekim 2026): Faz 4b'nin rakipleri — JarmRout-b (K-234) ·
    # OLSRv2-b (K-236). Ölçülen kopya d3fd674 ile birebir.
    "jarmrout.py": "569dcc17f51a0607cef3d01a7f1753f1",
    "jarmrout_bicim.py": "7bc03996f72b77630cea67f348fbfbe4",
    "olsrv2.py": "d7ab18d98bb5df8854c65fa5de5ffc5a",
    "olsrv2_bicim.py": "70f2b15bb75888b5048db1ed59372420",
    "olsrv2_rfc5444.py": "f0ec7db0405cbbf355d3117c81484811",
    # K-249 (17 Ekim 2026): `Babel-a` (RFC 8966, hakem babeld; K-244) —
    # ölçülen kopya 1163f81 ile birebir.
    "babel.py": "bc71fcd06163355be67d5f538e8de9d1",
    "babel_bicim.py": "b5938c5d63bb2e6cd272952634f7698a",
}


def test_TABAN_PROTOKOLLER_DONMUS():
    degisen = sorted(ad for ad, h in DONMUS.items()
                     if dosya_hash(KOK / "protokoller" / ad) != h)
    assert not degisen, (
        f"🔴 donmuş taban protokol dosyası değişti: {degisen} — yeni K kaydı, "
        f"U1 ve regresyon gerekir; sonra bu tablo güncellenir")


def test_OKUNAN_GOZLEM_KOKENI_kapisi_ates_ediyor(tmp_path, monkeypatch):
    """Bir protokol `kendi_konum` okursa `gps_dikey_sigma_m` DUYARSIZ kalamaz.

    Kayıt bugün SINANMAMIŞ (K-233: JarmRout konum okuyor); kapı kaydın
    DUYARSIZ hâliyle sınanır, defterin bugünkü durumundan bağımsız."""
    from kalibrasyon import mimari_denetimi as M
    from sim2.yapilandirma import kokenler
    monkeypatch.setitem(kokenler.KOKENLER, "gps_dikey_sigma_m",
                        ("DUYARSIZ", "sınama"))
    (tmp_path / "protokoller").mkdir()
    (tmp_path / "protokoller" / "deneme.py").write_text(
        "def f(gozlem):\n    return gozlem.kendi_konum\n", encoding="utf-8")
    monkeypatch.setattr(M, "KOK", tmp_path)
    monkeypatch.setattr(M, "bulgular", [])
    M.d17_okunan_gozlem_kokenleri()
    assert any("gps_dikey_sigma_m" in b for b in M.bulgular), M.bulgular
