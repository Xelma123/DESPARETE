"""K-223 regresyonunun iki büyük farkının teşhisi (ölçüt `teshis_beklenti.md`).

Birincil hücre, regresyonun kısa penceresi ve kimlik etiketleri; DESPARETE ·
AODV · `OLSR-d` × deneme sınırı {7, 6} + `OLSR-c` (`olsr_c.py`, c8b1b44'ün
birebir kopyası) × 7; tohum 1003–1010. Satırlar `teshis_birincil.jsonl`e
(ara kayıt: kesilirse kaldığı yerden sürer), özet ekrana.

    TESHIS_KOK=<kopya> PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
        py -3.11 -u arsiv/teshis/denetim_duzeltme_2026-10-09/teshis_birincil.py
"""
import json
import os
import statistics as ist
import sys
import time
from multiprocessing import Pool
from pathlib import Path

D = Path(__file__).resolve().parent
KOK = Path(os.environ.get("TESHIS_KOK") or D.parents[2])
for _yol in (KOK, KOK / "tests2", D):
    if str(_yol) not in sys.path:
        sys.path.insert(0, str(_yol))

TOHUMLAR = tuple(range(1003, 1011))
KOLLAR = (("desparete", 7), ("desparete", 6), ("aodv", 7), ("aodv", 6),
          ("olsr", 7), ("olsr", 6), ("olsr_c", 7))
PENCERE = dict(karistirici_baslangic_s=5.0, isinma_s=10.0,
               olcum_bitis_s=40.0, kosu_bitis_s=50.0)
ARA = D / "teshis_birincil.jsonl"
ANA = D.parents[2] / "ciktilar2" / "regresyon"


def _is(is_):
    protokol, sinir, tohum = is_
    from kalibrasyon.regresyon_satirlari import _fabrika
    from sim2.kanal.dunya import referans_2026
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.kurulum import kurulum_yap
    from sim2.kosum.sonuc import sonuc_satiri
    p = "olsr" if protokol == "olsr_c" else protokol
    t0 = time.perf_counter()
    kur = kurulum_yap(referans_2026(
        kol="regresyon", senaryo="formasyon-surekli", tohum=tohum,
        not_=f"u-birincil-{p}", tehdit_senaryosu="derin_sizma",
        trafik_deseni="yere_toplama", yeniden_deneme_siniri=sinir,
        **PENCERE))
    if protokol == "olsr_c":
        from olsr_c import OLSR as OLSRc
        fabrika = lambda i: OLSRc(i)                    # noqa: E731
    else:
        fabrika = _fabrika(protokol, kur)
    kosu = Kosu(kur, fabrika)
    kosu.kostur()
    s = sonuc_satiri(kur, kosu.dugumler, p)
    return {"protokol": protokol, "sinir": sinir, "tohum": tohum,
            "pdr": s["metrikler"]["pdr_pencere"],
            "gecerli": s["korunum"]["gecerli"],
            "dusen": s["korunum"]["dusen"],
            "sure_s": round(time.perf_counter() - t0, 1)}


def _oku_ara() -> dict:
    if not ARA.exists():
        return {}
    cikti = {}
    for x in ARA.read_text(encoding="utf-8").splitlines():
        if x.strip():
            r = json.loads(x)
            cikti[(r["protokol"], r["sinir"], r["tohum"])] = r
    return cikti


def _regresyon(etiket: str) -> dict:
    return {s["kimlik"]["not_"]: s for s in
            (json.loads(x) for x in (ANA / f"{etiket}.jsonl").read_text(
                encoding="utf-8").splitlines() if x.strip())}


def main() -> int:
    sonuc = _oku_ara()
    isler = [(p, n, t) for t in TOHUMLAR for p, n in KOLLAR
             if (p, n, t) not in sonuc]
    print(f"TESHIS — {len(isler)} kosu ({len(sonuc)} ara kayitta) · kok {KOK}")
    with Pool(8) as havuz, ARA.open("a", encoding="utf-8") as f:
        for r in havuz.imap_unordered(_is, isler):
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
            f.flush()
            os.fsync(f.fileno())
            sonuc[(r["protokol"], r["sinir"], r["tohum"])] = r
            print(f"  {r['protokol']:>9}@{r['sinir']} {r['tohum']} · PDR "
                  f"{r['pdr']:.4f} · gecerli {r['gecerli']} · {r['sure_s']} s")
    hata = [k for k, r in sonuc.items() if not r["gecerli"]]

    print("\nT0 · KIMLIK (1003, regresyon satirlariyla birebir)")
    k220, k223 = _regresyon("k220"), _regresyon("k223")
    for (p, n), ref in ((("desparete", 7), k220), (("aodv", 7), k220),
                        (("olsr_c", 7), k220), (("desparete", 6), k223),
                        (("aodv", 6), k223), (("olsr", 6), k223)):
        s = ref[f"u-birincil-{'olsr' if p == 'olsr_c' else p}"]
        r = sonuc[(p, n, 1003)]
        tut = (r["pdr"] == s["metrikler"]["pdr_pencere"]
               and r["dusen"] == s["korunum"]["dusen"])
        print(f"  {'OK ' if tut else '🔴 '} {p}@{n} {r['pdr']!r} = "
              f"{s['metrikler']['pdr_pencere']!r}")
        if not tut:
            hata.append(f"kimlik {p}@{n}")

    def esli(a, b):
        d = [sonuc[(*a, t)]["pdr"] - sonuc[(*b, t)]["pdr"] for t in TOHUMLAR]
        return d, ist.mean(d), ist.stdev(d) / len(d) ** 0.5

    print("\nT1 · DENEME SAYISI  Δ = PDR(6) − PDR(7)  (8 tohum)")
    dm = {}
    for p in ("desparete", "aodv", "olsr"):
        d, ort, se = esli((p, 6), (p, 7))
        dm[p] = d
        print(f"  {p:>9}: ort {ort:+.4f} · SE {se:.4f} · tohumlar "
              + " ".join(f"{x:+.3f}" for x in d))
    ff = [a - b for a, b in zip(dm["desparete"], dm["aodv"])]
    print(f"  DESPARETE − AODV (fark-farki): ort {ist.mean(ff):+.4f} · SE "
          f"{ist.stdev(ff) / len(ff) ** 0.5:.4f}")

    print("\nT2 · §8.2.1  Δ = PDR(OLSR-d@7) − PDR(OLSR-c@7)  (8 tohum)")
    d, ort, se = esli(("olsr", 7), ("olsr_c", 7))
    print(f"  ort {ort:+.4f} · SE {se:.4f} · tohumlar "
          + " ".join(f"{x:+.3f}" for x in d))

    print("\nT3 · 1003'te OLSR farkinin ayrismasi")
    a = sonuc[("olsr", 6, 1003)]["pdr"] - sonuc[("olsr", 7, 1003)]["pdr"]
    b = sonuc[("olsr", 7, 1003)]["pdr"] - sonuc[("olsr_c", 7, 1003)]["pdr"]
    print(f"  deneme {a:+.4f} · §8.2.1 {b:+.4f} · toplam {a + b:+.4f}")

    print("\nTOHUM BASINA PDR")
    for p, n in KOLLAR:
        print(f"  {p:>9}@{n}: " + " ".join(
            f"{sonuc[(p, n, t)]['pdr']:.3f}" for t in TOHUMLAR)
            + f" · ort {ist.mean(sonuc[(p, n, t)]['pdr'] for t in TOHUMLAR):.4f}")
    print("\n" + ("🟢 T0 GECTI" if not hata else "🔴 " + " · ".join(hata)))
    return 1 if hata else 0


if __name__ == "__main__":
    raise SystemExit(main())
