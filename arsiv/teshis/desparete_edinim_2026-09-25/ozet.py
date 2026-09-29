"""K-167 §5 — `uzun_ab_cikti.txt`nin özeti (yalnız okur).

Üretici: PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python arsiv/teshis/desparete_edinim_2026-09-25/ozet.py [çıktı dosyası]
"""
import ast
import statistics as ist
import sys
from pathlib import Path

DOSYALAR = [Path(a) for a in sys.argv[1:]] or [
    Path(__file__).with_name(ad) for ad in ("uzun_ab_cikti.txt", "uzun_ab_v10_cikti.txt")]
PROFILLER = ("v02", "v03", "v03+V8", "v03+V8V9", "v03+V8V10")

satirlar = [ast.literal_eval(s) for d in DOSYALAR
            for s in d.read_text(encoding="utf-8").splitlines()
            if s.startswith("{")]
ham = {r["is"]: r for r in satirlar}     # aynı iş iki dosyada: sonuncusu
kollar = sorted({k for k, _, _ in ham})
tohumlar = sorted({t for _, t, _ in ham})
print(f"{len(ham)} iş · geçersiz: "
      f"{[r['is'] for r in satirlar if not r['gecerli']]}")

print("\nkol · tohum · profil: pencere PDR | tüm PDR | k/v | p95 | geçit istek·tur"
      " | istek gön→ilt (ret · tanıdık) | soru gön→yan (V9) | ulaşılamaz · onarım"
      " | PROBE nitelik·ölçüm")
for k in kollar:
    for t in tohumlar:
        for pr in PROFILLER:
            r = ham.get((k, t, pr))
            if r is None:
                continue
            print(f"{k:14}{t:5} {pr:9} {r['pdr_pencere']:.3f} | {r['pdr']:.3f} |"
                  f" {r['kv']:.2f} | {(r['p95'] or 0):5.2f} |"
                  f" {r['gecit_hedefte']:2}·{r['gecit_tur']} |"
                  f" {r['istek_gonderilen']:3}→{r['istek_iletilen']:4}"
                  f" ({r['istek_aktif_disi']:3}·{r['istek_tanidik_kabul']:3}) |"
                  f" {r['solicit_gonderilen']:3}→{r['solicit_yanitlanan']:3}"
                  f" ({r['soru_nitelik']:3}) | {r['ulasilamaz']:3}·{r['onarim']:4} |"
                  f" {r['probe_nitelik']:5}·{r['probe_olcum']:4}"
                  + (f" | açlık istek {r['istek_aclik']}→geçitte"
                     f" {r['hedefte_aclik']}" if "istek_aclik" in r else ""))

print("\nortalama (kol başına, 3 tohum): pencere PDR · k/v · p95 · ulaşılamaz")
for k in kollar:
    for pr in PROFILLER:
        rs = [ham[(k, t, pr)] for t in tohumlar if (k, t, pr) in ham]
        if not rs:
            continue
        print(f"{k:14} {pr:9} {ist.mean(r['pdr_pencere'] for r in rs):.4f}"
              f" · {ist.mean(r['kv'] for r in rs):.3f}"
              f" · {ist.mean((r['p95'] or 0) for r in rs):.3f}"
              f" · {ist.mean(r['ulasilamaz'] for r in rs):.1f}")

print("\neşli fark (pencere PDR), 6 kol-tohum: ortalama · en küçük · en büyük · artan")
for a, b in (("v02", "v03"), ("v03", "v03+V8"), ("v03", "v03+V8V9"),
             ("v03+V8", "v03+V8V9"), ("v02", "v03+V8V9"),
             ("v03", "v03+V8V10"), ("v03+V8", "v03+V8V10"),
             ("v02", "v03+V8V10")):
    d = [ham[(k, t, b)]["pdr_pencere"] - ham[(k, t, a)]["pdr_pencere"]
         for k in kollar for t in tohumlar
         if (k, t, a) in ham and (k, t, b) in ham]
    if d:
        print(f"{a:9} → {b:9} {ist.mean(d):+.4f} · {min(d):+.3f} ·"
              f" {max(d):+.3f} · {sum(x > 0 for x in d)}/{len(d)}")
d03 = [ham[(k, t, "v03")]["pdr_pencere"] - ham[(k, t, "v02")]["pdr_pencere"]
       for k in kollar for t in tohumlar]
for pr in PROFILLER[2:]:
    dfx = [ham[(k, t, pr)]["pdr_pencere"] - ham[(k, t, "v03")]["pdr_pencere"]
           for k in kollar for t in tohumlar if (k, t, pr) in ham]
    if ist.mean(d03) < 0 and len(dfx) == len(d03):
        print(f"açığın kapanan payı ({pr}): {-ist.mean(dfx) / ist.mean(d03):.2f}")

print("\ndoğuma göre 30 s dilimli teslim — kol başına 3 tohum ortalaması")
for k in kollar:
    for pr in PROFILLER:
        rs = [ham[(k, t, pr)] for t in tohumlar if (k, t, pr) in ham]
        n = len(rs[0]["dilim_pdr"])
        dil = []
        for i in range(n):
            v = [r["dilim_pdr"][i] for r in rs if r["dilim_pdr"][i] is not None]
            dil.append(f"{ist.mean(v):.2f}" if v else "  —")
        print(f"{k:14} {pr:9} " + " ".join(dil))

print("\nröle durumu dilimlerde (iletilebilir payı / güvenli aday / 'ACTIVE ama"
      " uygulanabilir olmayan komşu var' payı) — 3 tohum ortalaması")
for k in kollar:
    for pr in PROFILLER:
        rs = [ham[(k, t, pr)] for t in tohumlar if (k, t, pr) in ham]
        n = len(rs[0]["dilim_durum"])
        hucre = []
        for i in range(n):
            v = [r["dilim_durum"][i] for r in rs if r["dilim_durum"][i]]
            hucre.append("/".join(f"{ist.mean(x[j] for x in v):.2f}"
                                  for j in (0, 2, 3)))
        print(f"{k:14} {pr:9} " + " ".join(hucre))
