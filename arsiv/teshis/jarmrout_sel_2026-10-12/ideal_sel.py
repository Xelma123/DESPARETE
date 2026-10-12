"""Simülatörden bağımsız sayım: ideal kanalda (çarpışma yok) RREQ selinin
kurala göre yeniden yayın sayısı. Ağ: referans dünya, statik-yok, tohum 1000."""
import sys, heapq, random, statistics as st
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from sim2.kanal.dunya import referans_2026
from sim2.kosum.kurulum import kurulum_yap
from kalibrasyon.kahin import KanalGrafigi

kfg = referans_2026(kol="t", senaryo="statik-yok", tohum=1000, trafik_deseni="yere_toplama")
kur = kurulum_yap(kfg)
g = KanalGrafigi(kur)
N = kfg.dugum_sayisi
P = [[(g._tek_deneme_basarisi(i, j, 60.0) if i != j else 0.0) for j in range(N)] for i in range(N)]
komsu = [[j for j in range(N) if P[i][j] > 0.05] for i in range(N)]
derece = [sum(1 for j in range(N) if P[i][j] >= 0.5) for i in range(N)]
gecit = kfg.gecit
# en kısa atlama (P >= 0.5 bağlarla)
def bfs(s):
    d = {s: 0}; q = [s]
    for u in q:
        for v in range(N):
            if P[u][v] >= 0.5 and v not in d:
                d[v] = d[u] + 1; q.append(v)
    return d
ds = bfs(gecit)
print(f"N {N} · gecit {gecit} · ort derece (P>=0,5) {st.mean(derece):.1f} · gecide ort atlama {st.mean(v for k,v in ds.items() if k!=gecit):.2f} · en uzak {max(ds.values())}")

def sel(S, D, kural, rnd):
    t_bit = lambda n: 192e-6 + (19 + 8 * n) * 8 / 1e6   # temel hızda yayın süresi
    olay = [(0.0, S, 0, (S,))]          # (zaman, gönderen, C_hop, rota)
    onbellek = {}
    ilet = 0; hedefe = 0
    sayac = 0
    while olay:
        t, u, c, rota = heapq.heappop(olay)
        for v in komsu[u]:
            if rnd.random() >= P[u][v]:
                continue
            if v in rota:
                continue
            if v == D:
                hedefe += 1; continue
            if v not in onbellek:
                onbellek[v] = c
            else:
                if kural == "dsr":
                    continue
                if c > onbellek[v]:
                    continue
                if kural == "enkucuk":
                    onbellek[v] = min(onbellek[v], c)
            ilet += 1
            gecikme = rnd.uniform(0, 0.010) + t_bit(len(rota))
            heapq.heappush(olay, (t + gecikme, v, c + 1, rota + (v,)))
            sayac += 1
            if sayac > 200000:
                return ilet, hedefe, True
    return ilet, hedefe, False

rnd = random.Random(1)
for kural in ("harfiyen", "enkucuk", "dsr"):
    ilet, hedef = [], []
    tasti = 0
    for S in range(N):
        if S == gecit: continue
        for _ in range(3):
            a, h, t = sel(S, gecit, kural, rnd)
            ilet.append(a); hedef.append(h); tasti += t
    print(f"{kural:9s} RREQ basina yeniden yayin: ort {st.mean(ilet):7.1f} · medyan {st.median(ilet):6.0f} · en cok {max(ilet):6d} · hedefe varan kopya ort {st.mean(hedef):6.1f} · sinir asimi {tasti}")
