"""Sönümlemenin bağıl hız tabanı (`sonumleme.py::BAGIL_HIZ_TABANI_MS`, 1 m/s)
referans dünyada ne sıklıkla bağlıyor? Faz 4 kapanışı D1. Yalnız topoloji;
simülasyon koşmaz.

    PYTHONIOENCODING=utf-8 py -3.11 kalibrasyon/bagil_hiz_tabani.py

30 Eylül 2026 çıktısı (tohum 1003, t = 60 · 150 · 250 s, < 12 km çiftler):
formasyon %0,2 (p10 3,49 · medyan 7,53 m/s) · bağımsız %0,0 · görev %0,0.
"""
import os
import statistics as ist
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK))
os.environ["DESPARETE_DUNYA"] = "referans_2026"

from kalibrasyon import dunya_secimi as DS  # noqa: E402
from sim2.kanal.sonumleme import BAGIL_HIZ_TABANI_MS  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402

for kol in ("formasyon", "bagimsiz", "gorev"):
    kfg = DS.konfig(kol="x", senaryo=f"{kol}-surekli", tohum=1003,
                    trafik_deseni="yere_toplama",
                    tehdit_senaryosu="derin_sizma")
    kur = kurulum_yap(kfg)
    s = kur.kanal.sonumleme
    hizlar = sorted(s.bagil_hiz_ms(i, j, t) * s._olcek
                    for t in (60.0, 150.0, 250.0)
                    for i in range(kfg.dugum_sayisi)
                    for j in range(i + 1, kfg.dugum_sayisi)
                    if kur.topoloji.mesafe(i, j, t) < 12_000)
    alt = sum(v < BAGIL_HIZ_TABANI_MS for v in hizlar) / len(hizlar)
    print(f"{kol:10} çift-an {len(hizlar)} · taban payı {alt:.1%} · "
          f"p10 {hizlar[len(hizlar) // 10]:.2f} · medyan "
          f"{ist.median(hizlar):.2f} m/s")
