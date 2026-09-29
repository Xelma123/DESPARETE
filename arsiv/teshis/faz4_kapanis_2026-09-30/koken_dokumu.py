"""Köken defterinin dökümü — kova · ad · referans ve eski dünyadaki değer ·
gerekçe. Faz 4 kapanış denetimi D1 (B1, B5).

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz4_kapanis_2026-09-30/koken_dokumu.py [kova ...]
"""
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KOK))

from sim2.kanal.dunya import referans_2026  # noqa: E402
from sim2.yapilandirma import kokenler as K  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402

eski, ref = Konfig(kol="x"), referans_2026(kol="x")
kovalar = sys.argv[1:] or [k for k in K.KOVALAR if k != "TEDAVI"]
for kova in kovalar:
    print(f"===== {kova}")
    for defter in (K.KOKENLER, K.MODUL_KOKENLERI):
        for ad, (kv, gerekce) in defter.items():
            if kv != kova:
                continue
            deger = f"ref={getattr(ref, ad)!r}" if hasattr(ref, ad) else ""
            if hasattr(eski, ad) and getattr(eski, ad) != getattr(ref, ad):
                deger += f" eski={getattr(eski, ad)!r}"
            print(f"* {ad} {deger}\n    {gerekce}")
print({k: v for k, v in K.kova_sayimi().items()})
print("duyarlılık borcu:", sorted(K.DUYARLILIK_BEKLEYEN))
