"""Referans dünyada bir koşunun maliyeti nereye gidiyor? (ajan, K-190)

AODV, statik-yok, yere toplama, 33 km, kısa pencere (20 s koşu) — cProfile.
Kod değiştirmez.

    PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
        python arsiv/teshis/faz4_2026-09-26/j_profil.py
"""
import cProfile
import io
import os
import pathlib
import pstats
import sys
import time

KOK = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KOK))
os.environ["DESPARETE_DUNYA"] = "referans_2026"

from kalibrasyon import dunya_secimi as DS  # noqa: E402
from protokoller.aodv import AODV  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402

if __name__ == "__main__":
    kfg = DS.konfig(kol="profil", senaryo="statik-yok", tohum=1000,
                    trafik_deseni="yere_toplama", isinma_s=5.0,
                    olcum_bitis_s=15.0, kosu_bitis_s=20.0)
    kur = kurulum_yap(kfg)
    print(f"duyanlar_menzili_m {kur.duyanlar_menzili_m:.0f} · alan "
          f"{kfg.alan_en_m:.0f}")
    kosu = Kosu(kur, lambda i: AODV(i))
    bas = time.perf_counter()
    pr = cProfile.Profile()
    pr.enable()
    kosu.kostur()
    pr.disable()
    sure = time.perf_counter() - bas
    s = kur.sayaclar.disa_ver()
    print(f"20 s koşu: {sure:.1f} s duvar · islenen olay "
          f"{s.get('islenen_olay')} · mac_deneme {s.get('mac_deneme')} · "
          f"alim denemesi (alim_*) "
          f"{sum(v or 0 for k, v in s.items() if k.startswith('alim_') and not k.endswith('_pencere'))}")
    cikti = io.StringIO()
    pstats.Stats(pr, stream=cikti).sort_stats("cumulative").print_stats(30)
    print(cikti.getvalue()[:7000])
    cikti = io.StringIO()
    pstats.Stats(pr, stream=cikti).sort_stats("tottime").print_stats(20)
    print(cikti.getvalue()[:5000])
