"""JarmRout seli — varyant karşılaştırması (yalnız teşhis; kod değişmez)."""
import sys, time
from collections import Counter
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import protokoller.jarmrout as J
from sim2.kanal.dunya import referans_2026
from sim2.kosum.kosu import Kosu
from sim2.kosum.kurulum import kurulum_yap
from sim2.kosum.sonuc import korunum_bolumu

varyant, senaryo, tohum, desen, bitis = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4], float(sys.argv[5])
if varyant == "enkucuk":          # önbellekteki C_hop kabul edilen kopyayla en küçüğe
    def bul(self, kaynak, sira):
        c = [c for s, c in self._istek.get(kaynak, ()) if s == sira]
        return min(c) if c else None
    J.JarmRout._istek_bul = bul
    o = J.JarmRout._rreq_isle
    def isle(self, gozlem, gonderen, y):
        once = self._istek_bul(y["kaynak"], y["pkt_seq"])
        r = o(self, gozlem, gonderen, y)
        if r and once is not None and y["hedef"] != self.kimlik:
            self._istek_kaydet(y["kaynak"], y["pkt_seq"], y["c_hop"])
        return r
    J.JarmRout._rreq_isle = isle
elif varyant == "dsr":            # yinelenen RREQ hiç yayılmaz
    def bul(self, kaynak, sira):
        return -1 if any(s == sira for s, _c in self._istek.get(kaynak, ())) else None
    J.JarmRout._istek_bul = bul
elif varyant == "periyot1":
    J.REQUEST_PERIOD_S = 1.0
kfg = referans_2026(kol="teshis", senaryo=senaryo, tohum=tohum, trafik_deseni=desen,
                    isinma_s=min(50.0, bitis * 0.3), olcum_bitis_s=bitis * 0.9, kosu_bitis_s=bitis)
kur = kurulum_yap(kfg)
pr = []
def fab(i):
    p = J.JarmRout(i); pr.append(p); return p
t0 = time.time()
k = Kosu(kur, fab); k.kostur()
r = korunum_bolumu(kur, k.dugumler)
top = Counter()
for p in pr:
    for a, v in p.teshis(0).items(): top[a] += v
c = kur.sayaclar.disa_ver()
print(f"{varyant:9s} sure {time.time()-t0:6.0f} s · PDR(kosu) {r['teslim']/r['uretilen']:.3f} · "
      f"rreq uretim {top['rreq_uretilen']} · ilet {top['rreq_iletilen']} · rerr {top['rerr_uretilen']} · "
      f"iki_yol {top['iki_yol']}/{top['iki_yol']+top['tek_yol']} · kontrol airtime {c.get('kontrol_airtime_s',0):.0f} s")
