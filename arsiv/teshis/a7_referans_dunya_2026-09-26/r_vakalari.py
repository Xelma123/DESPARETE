"""A7 (K-178) — regresyonun referans dünya vakalarına bir bakış (ölçüm DEĞİL:
kısa pencere, tek tohum, A2 dışındaki anahtarlar kapalı).

Kullanım:
    PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python \
        arsiv/teshis/a7_referans_dunya_2026-09-26/r_vakalari.py
"""
import json
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
for metin in (KOK / "ciktilar2" / "regresyon" / "k178.jsonl").read_text(
        encoding="utf-8").splitlines():
    s = json.loads(metin)
    ad = s["kimlik"]["not_"]
    if not ad.startswith("r-"):
        continue
    m, k = s["metrikler"], s["konfig"]
    print(f"{ad}\n  menzil {k['iletim_menzili_m']:.0f} m · β {k['sinr_esigi_db']:.2f}"
          f" dB · pdr {m['pdr']:.3f} · pdr_pencere {m['pdr_pencere']:.3f} · psr "
          f"{m.get('psr')} · düşen {({a: v for a, v in s['korunum']['dusen'].items() if v})}")
