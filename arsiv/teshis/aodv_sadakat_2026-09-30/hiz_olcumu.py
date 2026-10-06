"""AODV-h neden yavaş? — kısa pencere, statik-yok 1000, eski (U1 kopyası) ve yeni kod.

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/aodv_sadakat_2026-09-30/hiz_olcumu.py [kok]

`kok` verilirse o kod ağacı koşar (ör. `arsiv/teshis/u1_2026-09-29/kopya` = AODV-f).
Süre, olay sayısı, kontrol mesajları ve bekleyen uyandırma tepe değeri basılır.
"""
import collections
import os
import pathlib
import sys
import time

KOK = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else \
    pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KOK))
os.environ["DESPARETE_DUNYA"] = "referans_2026"

from kalibrasyon import dunya_secimi as DS  # noqa: E402
from kalibrasyon.aodv_uygunluk import _fabrika  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.kosum.sonuc import sonuc_satiri  # noqa: E402

kfg = DS.konfig(kol="u1", senaryo="statik-yok", tohum=1000,
                trafik_deseni="yere_toplama", isinma_s=10.0,
                olcum_bitis_s=40.0, kosu_bitis_s=50.0)
kur = kurulum_yap(kfg)
kosu = Kosu(kur, _fabrika("aodv", kfg))
uyandi = collections.Counter()
from protokoller import aodv as A  # noqa: E402
asil_uyandi = A.AODV.uyandi


def sar(self, gozlem, etiket):
    uyandi[etiket.split(":")[0]] += 1
    return asil_uyandi(self, gozlem, etiket)


A.AODV.uyandi = sar
t0 = time.perf_counter()
kosu.kostur()
sure = time.perf_counter() - t0
satir = sonuc_satiri(kur, kosu.dugumler, "aodv")
toplam = collections.Counter()
for d in kosu.dugumler:
    toplam.update(d.protokol._sayac)
m = satir["metrikler"]
print(f"kod {KOK.name} · sure {sure:.1f} s · pdr {m['pdr']:.4f}")
print("  sayac:", {k: v for k, v in toplam.items() if v})
print("  uyandi:", dict(uyandi))
print("  kontrol:", {k: v for k, v in satir["teshis"].get("kontrol_duzlemi", {}).items()
                    if "uyandirma" in k or "mesaj" in k})
