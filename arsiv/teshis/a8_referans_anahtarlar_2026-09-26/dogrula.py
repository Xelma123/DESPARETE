"""A8 beklentisinin sayısal maddeleri — `k180` ↔ `k181` `r-` vakaları
(koşu değil, satır okuma).

    PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
        python arsiv/teshis/a8_referans_anahtarlar_2026-09-26/dogrula.py
"""
import json
import pathlib

KOK = pathlib.Path(__file__).resolve().parents[3]


def oku(etiket):
    cikti = {}
    with open(KOK / "ciktilar2" / "regresyon" / f"{etiket}.jsonl",
              encoding="utf-8") as f:
        for metin in f:
            s = json.loads(metin)
            cikti[s["kimlik"]["not_"]] = s
    return cikti


once, sonra = oku("k180"), oku("k181")
ALANLAR = (
    ("gecerli", lambda s: s["korunum"]["gecerli"]),
    ("pdr", lambda s: round(s["metrikler"]["pdr"], 4)),
    ("pdr_pencere", lambda s: round(s["metrikler"]["pdr_pencere"], 4)),
    ("uretilen", lambda s: s["korunum"]["uretilen"]),
    ("kuyrukta (son)", lambda s: s["korunum"]["kuyrukta"]),
    ("dusen", lambda s: {k: v for k, v in s["korunum"]["dusen"].items() if v}),
    ("gonderim_s", lambda s: round(s["korunum"]["enerji_gonderim_s"], 2)),
    ("mac_deneme", lambda s: s["korunum"]["mac_deneme"]),
    ("modellenmeyen", lambda s: sorted(s["kapsam"]["modellenmeyen"])),
)
for k in sorted(sonra):
    if not k.startswith("r-"):
        continue
    print(f"\n{k}")
    for ad, fn in ALANLAR:
        print(f"  {ad:<16} k180 {fn(once[k])!s:<58} k181 {fn(sonra[k])}")

# `r-` dışı vakalarda kapsam farkı: hangi sınır düştü
print("\nkapsam.modellenmeyen farkı (`r-` dışı):")
for k in sorted(sonra):
    if k.startswith("r-") or k not in once:
        continue
    a = set(once[k]["kapsam"]["modellenmeyen"])
    b = set(sonra[k]["kapsam"]["modellenmeyen"])
    if a != b:
        print(f"  {k:<64} düşen {sorted(a - b)} · eklenen {sorted(b - a)}")
