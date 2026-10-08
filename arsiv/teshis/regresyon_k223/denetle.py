"""Regresyon k223'ün iki ek denetimi (ölçüt `beklenti.md`, 9 Ekim 2026).

1. İlan edilmiş değişen referans vakalarında `konfig` farkı YALNIZ
   `yeniden_deneme_siniri` 7 → 6 mı (davranış farkının kaynağı tek mi)?
2. Yeni evre vakası: geçerli, çizelge 15/15, evre alanları dolu, açık + sessiz
   doğum sayısı pencerenin doğumuna eşit, `ham_denetimi` tutuyor.

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/regresyon_k223/denetle.py
"""
import json
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KOK))
from analiz.satir import ham_denetimi  # noqa: E402

DIZIN = KOK / "ciktilar2" / "regresyon"
YENI = "u-birincil-evre-en_guvenilir_kahin"


def oku(etiket):
    return {s["kimlik"]["not_"]: s for s in
            (json.loads(x) for x in
             (DIZIN / f"{etiket}.jsonl").read_text(encoding="utf-8").splitlines()
             if x.strip())}


a, b = oku("k220"), oku("k223")
hata = []
referans = sorted(k for k in a if k.startswith(("r-referans-", "u-")))
print(f"1 · referans vakalarinda konfig farki ({len(referans)} vaka)")
for k in referans:
    fark = {f for f in set(a[k]["konfig"]) | set(b[k]["konfig"])
            if a[k]["konfig"].get(f) != b[k]["konfig"].get(f)}
    tamam = fark == {"yeniden_deneme_siniri"} and (
        a[k]["konfig"]["yeniden_deneme_siniri"],
        b[k]["konfig"]["yeniden_deneme_siniri"]) == (7, 6)
    pa = a[k]["metrikler"].get("pdr_pencere")
    pb = b[k]["metrikler"].get("pdr_pencere")
    d = (pb - pa) if pa is not None and pb is not None else None
    print(f"  {'OK ' if tamam else '🔴 '} {k:<44} fark {sorted(fark)} · "
          f"PDR {pa} → {pb}" + (f" (Δ {d:+.4f})" if d is not None else ""))
    if not tamam:
        hata.append(f"konfig farki {k}: {sorted(fark)}")
    if d is not None and abs(d) > 0.10:
        hata.append(f"|ΔPDR| > 0,10 {k}: {d:+.4f} (teshis gerekir)")

print(f"\n2 · yeni evre vakasi {YENI}")
s = b.get(YENI)
if s is None:
    hata.append("yeni vaka yok")
else:
    m = s["metrikler"]
    bas, bitis = s["kapsam"]["olcum_penceresi_s"]
    # Ölçüm penceresi ısınmadan başlar (10 s); açık + sessiz dönemler
    # karıştırıcının açılmasından (40 s) pencerenin sonuna kadardır.
    acilma = s["konfig"]["karistirici_baslangic_s"]
    dogan = sum(1 for d in s["ham"]["dogum_s"] if acilma <= d < bitis)
    kontroller = [
        ("gecerli", s["korunum"]["gecerli"]),
        ("cizelge 15/15", m.get("evre_cizelge_s") == [15.0, 15.0]),
        ("pencere 10-100, acilma 40", (bas, bitis, acilma) == (10.0, 100.0, 40.0)),
        *((f"{f} dolu", m.get(f) is not None)
          for f in ("pdr_temiz", "pdr_acik", "pdr_sessiz", "sok_derinligi")),
        (f"acik_n + sessiz_n = dogan ({dogan})",
         (m.get("pdr_acik_n") or 0) + (m.get("pdr_sessiz_n") or 0) == dogan),
    ]
    for ad, (sv, hv, tut) in ham_denetimi(s).items():
        kontroller.append((f"ham_denetimi {ad} ({sv} = {hv})", tut))
    for ad, ok in kontroller:
        print(f"  {'OK ' if ok else '🔴 '} {ad}")
        if not ok:
            hata.append(ad)
    print(f"  PDR temiz {m.get('pdr_temiz')} · acik {m.get('pdr_acik')} · "
          f"sessiz {m.get('pdr_sessiz')}")

print()
print("🟢 GECTI" if not hata else "🔴 KALDI:\n  " + "\n  ".join(hata))
raise SystemExit(1 if hata else 0)
