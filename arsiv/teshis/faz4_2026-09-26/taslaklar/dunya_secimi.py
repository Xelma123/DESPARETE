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
        return referans_2026(**ek)
    return Konfig(**ek)


def etiket(ad: str) -> str:
    """Çıktı adı — referans dünyada sonek alır, eski çıktılar ezilmez."""
    return f"{ad}_referans_2026" if referans_mi() else ad
