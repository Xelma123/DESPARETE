"""Birincil hücre partisinin özeti (K-200) — `kayit.json`dan.

    PYTHONIOENCODING=utf-8 python arsiv/teshis/birincil_2026-09-28/ozet.py
"""
import json
import pathlib
import statistics as ist
from collections import defaultdict

YER = pathlib.Path(__file__).resolve().parent
S = json.loads((YER / "kayit.json").read_text(encoding="utf-8"))["sonuc"]
by = defaultdict(dict)
for r in S:
    by[r["protokol"]][r["tohum"]] = r
T = [1003, 1004, 1005, 1006]
kahin = by["en_guvenilir_kahin"]
KOLLAR = ["olsr", "olsr_s13", "aodv", "aodv@rota_tamponu_kapasitesi=256",
          "aodv@rota_tamponu_omru_s=60", "aomdv", "desparete",
          "en_guvenilir_kahin"]
print("KOL · PDR(pencere) ort [1003 1004 1005 1006] · kahin-prot · doguma gore once/acik/sessiz")
for p in KOLLAR:
    rs = by[p]
    v = [rs[t]["pdr_pencere"] for t in T]
    fark = ist.mean(kahin[t]["pdr_pencere"] - rs[t]["pdr_pencere"] for t in T)
    e = {k: ist.mean(rs[t]["karistirici_evresi"][k]["pdr"] for t in T)
         for k in ("once", "acik", "sessiz")}
    print(f"{p:<37} {ist.mean(v):.3f} [{' '.join(f'{x:.3f}' for x in v)}]"
          f"  {fark:+.3f}  {e['once']:.3f}/{e['acik']:.3f}/{e['sessiz']:.3f}")
print("\nESLI FARKLAR")
for a, b in (("olsr", "olsr_s13"), ("desparete", "aodv"), ("desparete", "aomdv"),
             ("desparete", "olsr"), ("aomdv", "aodv")):
    f = [by[a][t]["pdr_pencere"] - by[b][t]["pdr_pencere"] for t in T]
    print(f"  {a} - {b}: " + " ".join(f"{x:+.3f}" for x in f)
          + f"  ort {ist.mean(f):+.3f} · sd {ist.stdev(f):.3f}")
for v in KOLLAR[3:5]:
    ayni = all(by[v][t]["pdr"] == by["aodv"][t]["pdr"]
               and by[v][t]["tablo"] == by["aodv"][t]["tablo"] for t in T)
    print(f"  {v}: temel AODV ile birebir: {ayni}")
print("\nDUSUS SEBEBI (uretilene oran) · bolge dagilimi (ANLIK — sessizde hep uzak)")
for p in ["aodv", "olsr", "aomdv", "desparete", "en_guvenilir_kahin"]:
    seb = defaultdict(lambda: defaultdict(int))
    uret = sum(by[p][t]["uretilen"] for t in T)
    for t in T:
        for k, n in by[p][t]["tablo"].items():
            s, b = k.split("|")
            seb[s][b] += n
    parca = []
    for s, bd in sorted(seb.items(), key=lambda x: -sum(x[1].values()))[:4]:
        top = sum(bd.values())
        parca.append(f"{s} {top / uret:.1%} (ed {bd.get('ed', 0) / top:.0%} "
                     f"gir {bd.get('girisim', 0) / top:.0%} "
                     f"uzak {bd.get('uzak', 0) / top:.0%})")
    print(f"  {p:<20} " + " · ".join(parca))
print("\nKARAR / BASARISIZ BAG BANDI")
for p in ["aodv", "olsr", "aomdv", "desparete", "en_guvenilir_kahin"]:
    kb, bb = defaultdict(int), defaultdict(int)
    for t in T:
        for k, n in by[p][t]["karar_bant"].items():
            kb[k] += n
        for k, n in by[p][t]["basarisiz_bant"].items():
            bb[k] += n
    tk, tb = sum(kb.values()) or 1, sum(bb.values()) or 1
    print(f"  {p:<20} karar iyi {kb['iyi'] / tk:.0%} · basarisiz iyi "
          f"{bb['iyi'] / tb:.0%} orta {bb['orta'] / tb:.0%} kotu {bb['kotu'] / tb:.0%}")
print("\nEVRE METRIKLERI (tohum ortalamasi; None sayilmaz)")
for p in ["aodv", "olsr", "aomdv", "desparete", "en_guvenilir_kahin"]:
    def ort(a):
        v = [x for x in (by[p][t]["evre"].get(a) for t in T) if x is not None]
        return f"{ist.mean(v):.3f} (n={len(v)})" if v else "—"
    print(f"  {p:<20} sok {ort('sok_derinligi')} · toparlanma_s "
          f"{ort('toparlanma_suresi_s')} · tespit_s {ort('tespit_gecikmesi_s')}")
