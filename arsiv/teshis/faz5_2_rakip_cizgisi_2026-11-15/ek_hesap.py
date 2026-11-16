"""Faz 5-2 (c) · ek sayılar — koşudan SONRA yazıldı, karar girdisi değildir.

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz5_2_rakip_cizgisi_2026-11-15/ek_hesap.py

Karar kuralının hesabı `sonuc_hesap.py`dedir; burası `sonuc.md` §5'in
("kuraldan sonra görülenler") sayılarını üretir. Simülasyon yok.
"""
from sonuc_hesap import (AD, D, HUCRE, KAHIN, KOLLAR, donem, dizi, esli,
                         gruplar, olcu, oku, oran, ort)

kayit, _ = oku(D)

print("== A · koşu süresi (saat; 8 işçi, 350 s'lik koşu) ==")
for kol in KOLLAR:
    print(f"  {AD[kol]:<7} " + " · ".join(
        f"{h} {min(r['sure_s'] for r in kayit[h][kol].values()) / 3600:.2f}–"
        f"{max(r['sure_s'] for r in kayit[h][kol].values()) / 3600:.2f}"
        for h in HUCRE))

print("\n== B · dayanıklılık ↔ birincil, kâhine göre ==")
print("  kâhine oran (B → D) · D − B farkının kâhinin farkından sapması "
      "(eşli, tohum ortalaması)")
kd = dizi(kayit, "dayaniklilik", KAHIN, lambda r: olcu("dayaniklilik", r))
kb = dizi(kayit, "birincil", KAHIN, lambda r: olcu("birincil", r))
for kol in KOLLAR:
    b = dizi(kayit, "birincil", kol, lambda r: olcu("birincil", r))
    d = dizi(kayit, "dayaniklilik", kol, lambda r: olcu("dayaniklilik", r))
    sapma = esli({t: d[t] - b[t] for t in b},
                 {t: kd[t] - kb[t] for t in kb})
    print(f"  {AD[kol]:<7} {ort(b) / ort(kb):.3f} → {ort(d) / ort(kd):.3f} · "
          f"sapma {sapma[0]:+.3f} (artı {sapma[1]}/8 · eksi {sapma[2]}/8)")

print("\n== C · evreler: önce · açık · sessiz (8 tohum ortalaması) ==")
for h in ("birincil", "dayaniklilik"):
    print(f"  {h}")
    for kol in KOLLAR:
        o = ort(dizi(kayit, h, kol, lambda r: oran(r["ikincil"]["once"])))
        a = ort(dizi(kayit, h, kol, lambda r: olcu(h, r)))
        s = ort(dizi(kayit, h, kol, lambda r: oran(donem(h, r, "sessiz"))))
        print(f"    {AD[kol]:<7} önce {o:.3f} · açık {a:.3f} · sessiz {s:.3f}"
              f" · sessiz − önce {s - o:+.3f}")

print("\n== D · açık dönemde doğan paketlerin kaybı, ikizdeki pencereye göre "
      "artış ==")
gi = {k: gruplar("ikiz", kayit["ikiz"][k].values()) for k in KOLLAR}
for h in ("birincil", "dayaniklilik"):
    print(f"  {h}")
    for kol in KOLLAR:
        g = gruplar(h, kayit[h][kol].values())
        print(f"    {AD[kol]:<7} R {gi[kol]['R']:.3f} → {g['R']:.3f} "
              f"({g['R'] - gi[kol]['R']:+.3f}) · İ {gi[kol]['I']:.3f} → "
              f"{g['I']:.3f} ({g['I'] - gi[kol]['I']:+.3f})")

print("\n== E · v0.4.1'in açığı tohum yarılarında (G = Babel − v0.4.1) ==")
for h in HUCRE:
    b = dizi(kayit, h, "babel", lambda r: olcu(h, r))
    v = dizi(kayit, h, "desparete", lambda r: olcu(h, r))
    ilk = ort({t: b[t] - v[t] for t in b if t <= 1006})
    son = ort({t: b[t] - v[t] for t in b if t >= 1007})
    print(f"  {h:<12} 1003–1006 {ilk:+.3f} · 1007–1010 {son:+.3f}")

print("\n== F · tohumlar arası yayılım: en zor tohum ==")
for h in HUCRE:
    sira = {}
    for kol in KOLLAR:
        d = dizi(kayit, h, kol, lambda r: olcu(h, r))
        sira[kol] = min(d, key=d.get)
    print(f"  {h:<12} " + " · ".join(f"{AD[k]} {t}" for k, t in sira.items()))
