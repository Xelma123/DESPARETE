"""JarmRout RREQ seli teşhisi — salt okur, simülatörü değiştirmez."""
import sys, time, json
from collections import Counter, defaultdict
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
import protokoller.jarmrout as J
from sim2.kanal.dunya import referans_2026
from sim2.kosum.kosu import Kosu
from sim2.kosum.kurulum import kurulum_yap
from sim2.kosum.sonuc import sonuc_satiri

senaryo, tohum, desen, bitis = sys.argv[1], int(sys.argv[2]), sys.argv[3], float(sys.argv[4])
olay = defaultdict(list)
uretim = Counter()            # (S, D) -> RREQ sayısı (yeniden denemeler dahil)
deneme = Counter()            # deneme numarası dağılımı
ilet = Counter()              # (S, seq) -> toplam yeniden yayın
dugum_ilet = Counter()        # (node, S, seq) -> o düğümün yaydığı kopya
atilan = Counter()
kesif_bas = {}                # (S, D) -> ilk RREQ anı
rrep_sure = []
hedef_rreq = Counter()        # (D, S, seq) -> hedefe varan kopya
yol_say = Counter()

o_gonder = J.JarmRout._rreq_gonder
def rreq_gonder(self, hedef):
    k = self._kesif[hedef]
    r = o_gonder(self, hedef)
    uretim[(self.kimlik, hedef)] += 1
    deneme[k[0]] += 1
    return r
J.JarmRout._rreq_gonder = rreq_gonder

o_baslat = J.JarmRout._kesif_baslat
def kesif_baslat(self, hedef, simdi):
    if hedef not in self._kesif:
        kesif_bas[(self.kimlik, hedef)] = simdi
    return o_baslat(self, hedef, simdi)
J.JarmRout._kesif_baslat = kesif_baslat

o_isle = J.JarmRout._rreq_isle
def rreq_isle(self, gozlem, gonderen, y):
    r = o_isle(self, gozlem, gonderen, y)
    key = (y["kaynak"], y["pkt_seq"])
    if y["hedef"] == self.kimlik:
        hedef_rreq[(self.kimlik,) + key] += 1
    elif r:
        ilet[key] += 1
        dugum_ilet[(self.kimlik,) + key] += 1
    else:
        atilan[key] += 1
    return r
J.JarmRout._rreq_isle = rreq_isle

o_sec = J.JarmRout._yol_sec
def yol_sec(self, kaynak, sira):
    kayit = self._hedef_kayit.get((kaynak, sira))
    yol_say[len(kayit) if kayit else 0] += 1
    return o_sec(self, kaynak, sira)
J.JarmRout._yol_sec = yol_sec

o_rrep = J.JarmRout._rrep_isle
def rrep_isle(self, y, simdi):
    if y["ip_hedef"] == self.kimlik:
        d = y["yol"][-1]
        if (self.kimlik, d) in kesif_bas and d in self._kesif:
            rrep_sure.append(simdi - kesif_bas[(self.kimlik, d)])
    return o_rrep(self, y, simdi)
J.JarmRout._rrep_isle = rrep_isle

kfg = referans_2026(kol="teshis", senaryo=senaryo, tohum=tohum, trafik_deseni=desen,
                    isinma_s=min(50.0, bitis * 0.3), olcum_bitis_s=bitis * 0.9, kosu_bitis_s=bitis)
kur = kurulum_yap(kfg)
pr = []
def fab(i):
    p = J.JarmRout(i); pr.append(p); return p
t0 = time.time()
Kosu(kur, fab).kostur()
satir = sonuc_satiri(kur, [], "jarmrout") if False else None
top = Counter()
for p in pr:
    for a, v in p.teshis(0).items(): top[a] += v
c = kur.sayaclar.disa_ver()
print("sure", round(time.time() - t0), "s · bitis", bitis)
print("teshis", dict(top))
print("kontrol_cerceve", c.get("kontrol_cerceve"), "yayin", c.get("kontrol_yayin_gonderilen"), "airtime_s", round(c.get("kontrol_airtime_s", 0), 1))
print("kesif (S,D) sayisi", len(uretim), "· toplam RREQ uretimi", sum(uretim.values()))
print("deneme no dagilimi", sorted(deneme.items())[:20])
ilet_d = sorted(ilet.values())
if ilet_d:
    n = len(ilet_d)
    print("RREQ basina yeniden yayin: ort %.1f · medyan %d · p90 %d · max %d" % (sum(ilet_d)/n, ilet_d[n//2], ilet_d[int(n*0.9)], ilet_d[-1]))
dn = Counter(dugum_ilet.values())
print("bir dugumun ayni RREQ'yu yayma sayisi dagilimi", sorted(dn.items())[:15])
hv = sorted(hedef_rreq.values())
if hv: print("hedefe varan kopya: ort %.1f · max %d" % (sum(hv)/len(hv), hv[-1]))
print("t_wait sonunda kayitli yol sayisi", sorted(yol_say.items()))
rs = sorted(rrep_sure)
if rs: print("kesif->ilk RREP sure: n %d · medyan %.3f · p90 %.3f · max %.3f" % (len(rs), rs[len(rs)//2], rs[int(len(rs)*0.9)], rs[-1]))
