"""KR-E beklentisinin sayısal maddeleri — `k181` ↔ `k182` (satır okuma).

    PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
        python arsiv/teshis/kre_metrik_2026-09-26/dogrula.py
"""
import json
import pathlib

KOK = pathlib.Path(__file__).resolve().parents[3]


def oku(etiket):
    with open(KOK / "ciktilar2" / "regresyon" / f"{etiket}.jsonl",
              encoding="utf-8") as f:
        return {s["kimlik"]["not_"]: s for s in map(json.loads, f)}


once, sonra = oku("k181"), oku("k182")
esit_degil = [k for k, s in sonra.items() if not k.startswith("t-") and (
    s["metrikler"]["gorev_teslim_orani"] != s["metrikler"]["pdr"]
    or s["metrikler"]["gorev_teslim_orani_pencere"]
    != s["metrikler"]["pdr_pencere"]
    or s["ham"]["olu_hedefe_dogum_s"] or s["ham"]["uretilmeyen_dogum_s"])]
print(f"t- dışı {sum(1 for k in sonra if not k.startswith('t-'))} vaka · "
      f"görev oranı = PDR ve ham diziler boş olmayan: {esit_degil or 'YOK'}")
for k in sorted(k for k in sonra if k.startswith("t-")):
    a, b = once[k], sonra[k]
    ma, mb, hb = a["metrikler"], b["metrikler"], b["ham"]
    print(f"\n{k}")
    print(f"  korunum k181 ile aynı : {a['korunum'] == b['korunum']}")
    print(f"  pdr                   : {ma['pdr']:.4f} → {mb['pdr']:.4f}")
    print(f"  pdr_pencere           : {ma['pdr_pencere']:.4f} → "
          f"{mb['pdr_pencere']:.4f}")
    print(f"  gorev_teslim_orani    : {mb['gorev_teslim_orani']:.4f} "
          f"(pencere {mb['gorev_teslim_orani_pencere']:.4f})")
    print(f"  ölü hedefe doğan {len(hb['olu_hedefe_dogum_s'])} · doğamayan "
          f"{len(hb['uretilmeyen_dogum_s'])} · kohort "
          f"{len(hb['dogum_s'])} · korunum üretilen "
          f"{b['korunum']['uretilen']}")
