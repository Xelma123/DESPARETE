"""Birincil hücrede bir koşunun maliyeti nereye gidiyor? (ajan, 28 Eylül 2026)

formasyon · yere toplama · derin_sizma (10 W) · sürekli · AODV · tohum 1003 — KISA (3 s),
karıştırıcı 2 s'de açılır, 3 s koşu (ısınma 1 s). cProfile. Kod değiştirmez.
K-190'ın statik profiliyle (`faz4_2026-09-26/j_profil.py`) aynı biçim.

    PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
        python arsiv/teshis/performans_2026-09-28/profil_birincil.py [protokol]
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
from kalibrasyon.aodv_uygunluk import _fabrika  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402

if __name__ == "__main__":
    protokol = sys.argv[1] if len(sys.argv) > 1 else "aodv"
    kfg = DS.konfig(kol="profil", senaryo="formasyon-surekli", tohum=1003,
                    trafik_deseni="yere_toplama",
                    tehdit_senaryosu="derin_sizma",
                    karistirici_baslangic_s=1.0, isinma_s=0.5,
                    olcum_bitis_s=2.5, kosu_bitis_s=3.0)
    kur = kurulum_yap(kfg)
    kosu = Kosu(kur, _fabrika(protokol, kfg))
    bas = time.perf_counter()
    pr = cProfile.Profile()
    pr.enable()
    kosu.kostur()
    pr.disable()
    sure = time.perf_counter() - bas
    s = kur.sayaclar.disa_ver()
    print(f"{protokol} · 3 s koşu: {sure:.1f} s duvar · islenen olay "
          f"{s.get('islenen_olay')} · mac_deneme {s.get('mac_deneme')} · "
          f"alim denemesi "
          f"{sum(v or 0 for k, v in s.items() if k.startswith('alim_') and not k.endswith('_pencere'))}"
          f" · kontrol_cerceve {s.get('kontrol_cerceve')}")
    cikti = io.StringIO()
    pstats.Stats(pr, stream=cikti).sort_stats("cumulative").print_stats(35)
    print(cikti.getvalue()[:8000])
    cikti = io.StringIO()
    pstats.Stats(pr, stream=cikti).sort_stats("tottime").print_stats(25)
    print(cikti.getvalue()[:6000])
