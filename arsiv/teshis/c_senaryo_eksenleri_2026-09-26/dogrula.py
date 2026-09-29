"""C beklentisinin sayısal maddeleri — `k180` satırlarından (koşu değil).

    PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
        python arsiv/teshis/c_senaryo_eksenleri_2026-09-26/dogrula.py
"""
import json
import pathlib

KOK = pathlib.Path(__file__).resolve().parents[3]
satirlar = {}
with open(KOK / "ciktilar2" / "regresyon" / "k180.jsonl", encoding="utf-8") as f:
    for metin in f:
        s = json.loads(metin)
        satirlar[s["kimlik"]["not_"]] = s

# --- enerji aralıkları -------------------------------------------------
disinda = []
for k, s in sorted(satirlar.items()):
    m, kr, kf = s["metrikler"], s["korunum"], s["konfig"]
    n, sure = kf["dugum_sayisi"], kf["kosu_bitis_s"]
    taban = n * sure * kf["enerji_alim_w"]
    tam = sure > 100
    alt, ust = ((28000, 30000) if tam else (4000, 4400))
    p50 = m["enerji_dugum_p50_j"]
    p50_alt, p50_ust = (2.0 * sure, 2.2 * sure)
    ok = (alt <= m["enerji_toplam_j"] <= ust and p50_alt <= p50 <= p50_ust
          and kr["enerji_sure_tamam"])
    if not ok or k.startswith("t-"):
        disinda.append(k)
    print(f"{'  ' if ok else '❌'} {k:<62} N={n} T={sure:>4.0f} s · toplam "
          f"{m['enerji_toplam_j']:8.0f} J (taban {taban:6.0f}) · p50 "
          f"{p50:6.1f} J · gönderim {kr['enerji_gonderim_s']:6.2f} s")
print(f"\naralık dışı / işaretli: {disinda}")

# --- t- vakaları ikizleriyle ------------------------------------------
IKIZ = {"t-bagimsiz-surekli-dogrudan_komsu-dugum_kaybi":
        "m-bagimsiz-surekli-dogrudan_komsu",
        "t-statik-surekli-aodv-dugum_kaybi": "k-statik-surekli-aodv"}
for t, ikiz in IKIZ.items():
    a, b = satirlar[t], satirlar[ikiz]
    print(f"\n{t}  ↔  {ikiz}")
    for ad, fn in (
            ("gecerli", lambda s: s["korunum"]["gecerli"]),
            ("uretilen", lambda s: s["korunum"]["uretilen"]),
            ("pdr", lambda s: s["metrikler"]["pdr"]),
            ("dusen.dugum_kaybi", lambda s: s["korunum"]["dusen"]["dugum_kaybi"]),
            ("dugum_kaybi_dusen", lambda s: s["metrikler"]["dugum_kaybi_dusen"]),
            ("mac_kayip_askida", lambda s: s["metrikler"]["mac_kayip_askida"]),
            ("dusen (tümü)", lambda s: s["korunum"]["dusen"]),
            ("enerji_toplam_j", lambda s: s["metrikler"]["enerji_toplam_j"])):
        print(f"  {ad:<20} {fn(a)!s:<60} ikiz {fn(b)}")
    ua, ub = a["korunum"]["uretilen"], b["korunum"]["uretilen"]
    print(f"  üretim düşüşü %{100 * (ub - ua) / ub:.1f} · enerji farkı "
          f"{b['metrikler']['enerji_toplam_j'] - a['metrikler']['enerji_toplam_j']:.0f} J")
