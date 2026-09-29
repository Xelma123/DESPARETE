"""Kayıtlı U1 koşularındaki iş sürelerinin özeti (yalnız okur)."""
import json
import statistics as st
from pathlib import Path

KOK = Path("ciktilar2/aodv_uygunluk")
for ad in ("aodv_son.json", "olsr_son.json", "aomdv_son.json"):
    veri = json.loads((KOK / ad).read_text(encoding="utf-8"))
    kova: dict[tuple[str, bool], list[float]] = {}
    for h in veri["hucreler"]:
        if h.get("olcum") is None:
            continue
        kol = h["kol"].split("-")[0]
        kova.setdefault((kol, h["kahin"]), []).append(h["olcum"]["sure"] / 60)
    toplam = sum(sum(v) for v in kova.values())
    print(f"{veri['protokol']:6s} iş={sum(len(v) for v in kova.values())} "
          f"toplam iş-dk={toplam:.0f}")
    for (kol, kahin), v in sorted(kova.items()):
        print(f"   {kol:9s} {'kahin' if kahin else 'prot.'}  n={len(v)} "
              f"ort {st.mean(v):5.1f} dk  en çok {max(v):5.1f} dk")
