"""
Kalibrasyon araçlarının DÜNYA seçimi — Faz 4.0 (K-183).

Araç `--dunya referans_2026` alır. `secimi_oku()` argümanı listeden çıkarır
ve ortam değişkenine yazar: havuz işçileri (Windows `spawn`) onu devralır.
Verilmezse `olcek_1_50` — araçların bugüne kadarki bütün çıktıları birebir.

🔒 Ölçütler dünyaya göre DEĞİŞMEZ; değişen yalnız konfigürasyon ve tarama
aralıklarıdır (her araçta `--dunya`ya bağlı, gerekçeli).
"""

from __future__ import annotations

import os
import sys

from sim2.cekirdek.degismezler import dogrula
from sim2.yapilandirma.konfig import Konfig

__all__ = ["ORTAM", "DUNYALAR", "secimi_oku", "secili", "referans_mi",
           "konfig", "etiket"]

ORTAM = "DESPARETE_DUNYA"
# Faz 4.1 (K-185): alan × güç ortak taraması için referans alanını geçersiz
# kılar (yalnız referans dünyada; kare alan). Verilmezse `REFERANS_ALAN_M`.
ALAN_ORTAM = "DESPARETE_ALAN_M"
DUNYALAR = ("olcek_1_50", "referans_2026")


def secimi_oku(argv: list[str] | None = None) -> str:
    """`--dunya X`i argüman listesinden çıkarır ve ortama yazar."""
    argv = sys.argv if argv is None else argv
    if "--dunya" in argv:
        i = argv.index("--dunya")
        dogrula(i + 1 < len(argv), "--dunya bir ad ister")
        ad = argv[i + 1]
        dogrula(ad in DUNYALAR, f"bilinmeyen dünya: {ad!r} — {DUNYALAR}")
        del argv[i:i + 2]
        os.environ[ORTAM] = ad
    if "--alan" in argv:
        i = argv.index("--alan")
        dogrula(i + 1 < len(argv), "--alan bir metre değeri ister")
        alan = float(argv[i + 1])
        dogrula(alan > 0.0, "alan pozitif olmalı")
        del argv[i:i + 2]
        os.environ[ALAN_ORTAM] = repr(alan)
    return secili()


def secili() -> str:
    ad = os.environ.get(ORTAM, "olcek_1_50")
    dogrula(ad in DUNYALAR, f"bilinmeyen dünya: {ad!r}")
    return ad


def referans_mi() -> bool:
    return secili() == "referans_2026"


def konfig(**ek) -> Konfig:
    """Seçili dünyanın konfigürasyonu — `Konfig(**ek)` ya da
    `referans_2026(**ek)` (türetilen alanlar verilemez)."""
    if referans_mi():
        from sim2.kanal.dunya import referans_2026
        alan = os.environ.get(ALAN_ORTAM)
        if alan is not None and "alan_en_m" not in ek:
            # Görev yarıçapı `referans_2026`daki gibi eski dünyanın alan
            # oranıyla (650/1800) ölçeklenir; yoksa küçük alana sığmaz.
            v = Konfig.__dataclass_fields__
            oran = (v["gorev_grup_yaricapi_m"].default
                    / v["alan_en_m"].default)
            ek = {"gorev_grup_yaricapi_m": oran * float(alan), **ek,
                  "alan_en_m": float(alan), "alan_boy_m": float(alan)}
        return referans_2026(**ek)
    return Konfig(**ek)


def etiket(ad: str) -> str:
    """Çıktı adı — referans dünyada sonek alır, eski çıktılar ezilmez."""
    if not referans_mi():
        return ad
    alan = os.environ.get(ALAN_ORTAM)
    return (f"{ad}_referans_2026" if alan is None
            else f"{ad}_referans_2026_alan{float(alan):.0f}")
