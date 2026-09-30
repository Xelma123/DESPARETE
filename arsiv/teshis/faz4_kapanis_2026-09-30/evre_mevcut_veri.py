"""Evre önerisi v2'nin dayandığı sayılar — yeni koşu yok, K-200 partisinden.

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz4_kapanis_2026-09-30/evre_mevcut_veri.py

Kaynak: `arsiv/teshis/birincil_2026-09-28/kayit.jsonl` (birincil hücre,
geliştirme tohumları 1003–1006). Çizelge: T_j 150 s, 15 s açık · 15 s sessiz,
ölçüm sonu 320 s → açık dönemler 150, 180, …, 300 başlar.
"""
import json
import statistics as st
from pathlib import Path

KAYIT = Path(__file__).resolve().parents[1] / "birincil_2026-09-28" / "kayit.jsonl"
TJ, ACIK, SESSIZ = 150.0, 15.0, 15.0


def acik_donem(t_s: float) -> str:
    """Mutlak an → kaçıncı açık dönem (1'den) ya da sessiz."""
    tur, faz = divmod(t_s - TJ, ACIK + SESSIZ)
    return f"{int(tur) + 1}. açık" if faz < ACIK else f"{int(tur) + 1}. sessiz"


satirlar = [json.loads(s) for s in KAYIT.open(encoding="utf-8")]
top: dict[str, list[tuple[float, float, float]]] = {}
print(f"{'protokol':>12} tohum   önce   açık  sessiz |    M1    M3   M4 (tespit anı)   sessiz/önce")
for s in sorted(satirlar, key=lambda s: (s["protokol"], s["tohum"])):
    if "@" in s["protokol"]:
        continue            # K-200'ün tampon kolları: AODV'yle birebir
    k, e = s["karistirici_evresi"], s["evre"]
    o, a, z = (k[x]["pdr"] for x in ("once", "acik", "sessiz"))
    m4 = e["tespit_gecikmesi_s"]
    anı = "-" if m4 is None else f"{m4:.0f} s ({acik_donem(TJ + m4)})"
    top.setdefault(s["protokol"], []).append((e["sok_derinligi"], z / o, o))
    print(f"{s['protokol'][:12]:>12} {s['tohum']}  {o:.3f}  {a:.3f}  {z:.3f} | "
          f"{e['sok_derinligi']:+.3f} {e['toparlanma_suresi_s']!s:>5}  {anı:<20} {z / o:.3f}")
print()
for p, v in top.items():
    oran = [x[1] for x in v]
    print(f"{p[:12]:>12}  sessiz/önce ort {st.mean(oran):.3f}  aralık {min(oran):.2f}–{max(oran):.2f}")
