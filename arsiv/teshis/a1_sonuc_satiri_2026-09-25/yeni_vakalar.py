"""A1 (K-171) · regresyonun yeni `k-` vakalarının özeti.

Kullanım: PYTHONIOENCODING=utf-8 python arsiv/teshis/a1_sonuc_satiri_2026-09-25/yeni_vakalar.py
"""
import json
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
YOL = KOK / "ciktilar2" / "regresyon" / "k171.jsonl"

for metin in YOL.read_text(encoding="utf-8").splitlines():
    s = json.loads(metin)
    vaka = s["kimlik"]["not_"]
    if not vaka.startswith("k-"):
        continue
    m, k = s["metrikler"], s["korunum"]
    d = k["dusen"]
    print(f"{vaka}")
    print(f"  gecerli={k['gecerli']} · pdr={m['pdr']:.4f} · "
          f"pdr_pencere={m['pdr_pencere']:.4f}")
    if "pdr_telemetri" in m:
        print(f"  pdr_telemetri={m['pdr_telemetri']:.4f} · "
              f"pdr_komut={m['pdr_komut']} · "
              f"pdr_komut_pencere={m['pdr_komut_pencere']}")
    print("  dusen: " + " · ".join(f"{a}={v}" for a, v in d.items() if v))
    print(f"  politika_dusen={m['politika_dusen']} · "
          f"beyan_etmiyor={m['beyan_etmiyor']}")
