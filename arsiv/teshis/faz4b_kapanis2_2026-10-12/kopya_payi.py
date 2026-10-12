"""Kopya kuralı (K-238) — kâhini aşan bir JarmRout hücresinde, teslimlerin
kaçı YALNIZ kopya sayesinde? Hedefe varan her örnek (asıl = kopya 0, eş =
kopya ≥ 1) kaydedilir; teslim edilmiş ama aslı hedefe hiç varmamış paket
"yalnız kopyayla teslim"dir. Oran o paketler çıkarılarak yeniden hesaplanır.
Simülatörün kodu değişmez: `sim2.kosum.teslim._yerlestir` teşhis için sarılır.

    (depo kökünde ya da dondurulmuş kopyada)
    py -3.11 -u <yol>/kopya_payi.py <kol> <tohum> <desen> <kahin_pdr>
"""
import sys
from collections import defaultdict
from pathlib import Path
# Kod ÇALIŞMA DİZİNİNDEN alınır: kuyruk dondurulmuş kopyanın içinden koşar.
sys.path.insert(0, str(Path.cwd()))
import sim2.kosum.teslim as T
from protokoller.jarmrout import JarmRout
from sim2.kanal.dunya import referans_2026
from sim2.kosum.kosu import Kosu
from sim2.kosum.kurulum import kurulum_yap
from sim2.kosum.sonuc import sonuc_satiri

R = 0.0126                                    # K-224 (`04` §8)
kol, tohum, desen, kahin = sys.argv[1], int(sys.argv[2]), sys.argv[3], float(sys.argv[4])
varis: dict[int, set[int]] = defaultdict(set)
asil = T._yerlestir


def yerlestir(kosu, d, paket):
    if paket.hedef == d.kimlik:
        varis[paket.kimlik].add(paket.kopya)
    return asil(kosu, d, paket)


T._yerlestir = yerlestir
kfg = referans_2026(kol="u1", senaryo=kol, tohum=tohum, trafik_deseni=desen)
kur = kurulum_yap(kfg)
kosu = Kosu(kur, lambda i: JarmRout(i))
kosu.kostur()
satir = sonuc_satiri(kur, kosu.dugumler, "u1")
pdr = satir["metrikler"]["pdr"]
pd = kur.paket_defteri
yalniz_kopya = sum(1 for k, s in varis.items() if 0 not in s)
print(f"{kol} · {tohum} · {desen} · korunum gecerli {satir['korunum']['gecerli']}")
print(f"  PDR {pdr:.4f} (U1 kaydiyla ayni olmali) · uretilen {pd.uretilen} · teslim {pd.teslim}")
print(f"  hedefe varan paket {len(varis)} · yalniz kopyayla teslim {yalniz_kopya}")
pdr_tek = (pd.teslim - yalniz_kopya) / pd.uretilen
print(f"  kopyasiz PDR {pdr_tek:.4f} · kahin {kahin:.4f} · oran {pdr / kahin:.4f} -> kopyasiz {pdr_tek / kahin:.4f}")
print(f"  KURAL: kopyasiz oran <= 1 + R ({1 + R:.4f}) -> {'SAGLANDI' if pdr_tek / kahin <= 1 + R else 'SAGLANMADI'}")
