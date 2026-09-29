"""Yenilik önbelleğinin ıskalamaları zorunlu mu, kapasite mi? (ajan, 28 Eylül)

Birincil hücre, AODV, 1003, 4 s koşu; önbellek tavanı YALNIZ bu süreçte
argümanla verilir (depo değişmez). Tavan büyüyünce ıskalama düşüyorsa
ıskalamaların bir kısmı "dolunca boşalt"tan doğan kapasite ıskalamasıdır.

    python iskalama.py <tavan>
"""
import os
import pathlib
import sys
import time

KOK = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KOK))
os.environ["DESPARETE_DUNYA"] = "referans_2026"

from sim2.kanal import sonumleme as S  # noqa: E402

S.YENILIK_ONBELLEK_SINIRI = int(sys.argv[1])

from kalibrasyon import dunya_secimi as DS  # noqa: E402
from kalibrasyon.aodv_uygunluk import _fabrika  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402

kfg = DS.konfig(kol="iskalama", senaryo="formasyon-surekli", tohum=1003,
                trafik_deseni="yere_toplama", tehdit_senaryosu="derin_sizma",
                karistirici_baslangic_s=1.0, isinma_s=0.5, olcum_bitis_s=3.5,
                kosu_bitis_s=4.0)
kur = kurulum_yap(kfg)
kosu = Kosu(kur, _fabrika("aodv", kfg))
bas = time.perf_counter()
kosu.kostur()
print(f"tavan {S.YENILIK_ONBELLEK_SINIRI}: {time.perf_counter() - bas:.1f} s "
      f"· {kur.kanal.sonumleme.onbellek_raporu()}")
