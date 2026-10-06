"""Faz 4.4 · kanıtla kapanan kalemler — regresyon satırlarından okuma.

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz4_4_birincil_2026-10-02/k_kalemleri.py [etiket]

Simülasyon koşmaz. `ciktilar2/regresyon/<etiket>.jsonl` (varsayılan k204,
taban protokoller dondu, K-211) satırlarından:
  · `BEKLEYEN_UYANDIRMA_TAVANI` — kontrol düzlemi olan her satırın tepe
    bekleyen uyandırma sayısı (`teshis` içinde `tepe_bekleyen_uyandirma`),
  · `ttl_baslangic` — satır başına TTL ölümü (koşu ve pencere).
Kâhin satırlarında kontrol düzlemi yoktur; tepe alanı taşımazlar.
"""
import json
import pathlib
import sys
from collections import Counter

KOK = pathlib.Path(__file__).resolve().parents[3]
ETIKET = sys.argv[1] if len(sys.argv) > 1 else "k204"
yol = KOK / "ciktilar2" / "regresyon" / f"{ETIKET}.jsonl"
satirlar = [json.loads(s) for s in yol.read_text(encoding="utf-8").splitlines()
            if s.strip()]


def ara(d, anahtar):
    if isinstance(d, dict):
        for k, v in d.items():
            if k == anahtar:
                return v
            r = ara(v, anahtar)
            if r is not None:
                return r
    return None


print(f"{yol.name}: {len(satirlar)} satir")
tepeli, tepesiz = [], Counter()
for s in satirlar:
    k, m = s["kimlik"], s["metrikler"]
    tepe = ara(s.get("teshis", {}), "tepe_bekleyen_uyandirma")
    if tepe is None:
        tepesiz[k["protokol"]] += 1
        continue
    tavan = ara(s.get("teshis", {}), "bekleyen_uyandirma_tavani")
    tepeli.append(tepe)
    print(f"  {k['protokol']:14} {k['senaryo']:26} {k['tohum']}  tepe {tepe:3}/{tavan}"
          f"  ttl_olumu {m.get('ttl_olumu'):6.0f} (pencere {m.get('ttl_olumu_pencere'):4.0f}"
          f" / dogum {ara(s, 'penceredeki_dogum')})")
print(f"kontrol duzlemli satir {len(tepeli)} · en yuksek tepe {max(tepeli)}")
print(f"tepe alani olmayan satirlar (protokole gore): {dict(tepesiz)}")
