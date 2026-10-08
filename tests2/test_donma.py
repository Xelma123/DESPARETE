"""Taban protokollerin donması ve okunan gözlemin kökeni (denetim 2026-10-08).

D-12: `protokol_hash` paket düzeyindedir — DESPARETE'nin bir dosyası değişince
taban protokol satırlarının kimliği de değişir, yani satır kimliği "taban
protokoller dondu" iddiasını kanıtlayamaz. Bu test dosyaların kendisini
bağlar: bir taban protokol dosyası değişirse kırılır ve yeni bir K kaydı,
U1 ve regresyon ister (`v2/04` §5). Değerler K-218'in donmuş hâli.

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

# K-218 (8 Ekim 2026): AODV-j · AOMDV-f + koşum protokolleri; OLSR-d K-223.
DONMUS: dict[str, str] = {
    "aodv.py": "1d39ba7da14c91f8931556742ca9a806",
    "aodv_bicim.py": "73ba004bad94deac158e5ea48b80db66",
    "olsr.py": "f5a93933860a05221ee8866d6df455ed",
    "olsr_bicim.py": "b813f12cad77454da1e134af4a45c151",
    "aomdv.py": "3d2d037a012431b21ab1381e22d3882f",
    "aomdv_bicim.py": "ca9c20feaafb51dac524c9af14238a48",
    "kosum_kosumu.py": "e175ba6cc74a80a5cca9c7789ac39ac7",
}


def test_TABAN_PROTOKOLLER_DONMUS():
    degisen = sorted(ad for ad, h in DONMUS.items()
                     if dosya_hash(KOK / "protokoller" / ad) != h)
    assert not degisen, (
        f"🔴 donmuş taban protokol dosyası değişti: {degisen} — yeni K kaydı, "
        f"U1 ve regresyon gerekir; sonra bu tablo güncellenir")


def test_OKUNAN_GOZLEM_KOKENI_kapisi_ates_ediyor(tmp_path, monkeypatch):
    """Bir protokol `kendi_konum` okursa `gps_dikey_sigma_m` DUYARSIZ kalamaz."""
    from kalibrasyon import mimari_denetimi as M
    (tmp_path / "protokoller").mkdir()
    (tmp_path / "protokoller" / "deneme.py").write_text(
        "def f(gozlem):\n    return gozlem.kendi_konum\n", encoding="utf-8")
    monkeypatch.setattr(M, "KOK", tmp_path)
    monkeypatch.setattr(M, "bulgular", [])
    M.d17_okunan_gozlem_kokenleri()
    assert any("gps_dikey_sigma_m" in b for b in M.bulgular), M.bulgular
