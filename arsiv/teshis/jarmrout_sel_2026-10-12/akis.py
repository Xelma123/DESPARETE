"""JarmRout (harfiyen) — eşzamanlı akış sayısına göre PDR ve sel (teşhis)."""
import sys, time
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import protokoller.jarmrout as J
from sim2.kanal.dunya import referans_2026
from sim2.kosum.kosu import Kosu
from sim2.kosum.kurulum import kurulum_yap
from sim2.kosum.sonuc import korunum_bolumu
akis, bitis = int(sys.argv[1]), float(sys.argv[2])
kfg = referans_2026(kol="teshis", senaryo="statik-yok", tohum=1000, trafik_deseni="esler_arasi",
                    akis_sayisi=akis, isinma_s=30.0, olcum_bitis_s=bitis * 0.9, kosu_bitis_s=bitis)
kur = kurulum_yap(kfg); pr = []
def fab(i):
    p = J.JarmRout(i); pr.append(p); return p
t0 = time.time(); k = Kosu(kur, fab); k.kostur()
r = korunum_bolumu(kur, k.dugumler); top = Counter()
for p in pr:
    for a, v in p.teshis(0).items(): top[a] += v
c = kur.sayaclar.disa_ver()
print(f"akis {akis:3d} · sure {time.time()-t0:5.0f} s · PDR {r['teslim']/r['uretilen']:.3f} · rreq uretim {top['rreq_uretilen']} · "
      f"ilet {top['rreq_iletilen']} (RREQ basina {top['rreq_iletilen']/max(1,top['rreq_uretilen']):.0f}) · rerr {top['rerr_uretilen']} · kontrol airtime {c.get('kontrol_airtime_s',0):.0f} s")
