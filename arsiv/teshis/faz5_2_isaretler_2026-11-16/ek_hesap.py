"""Faz 5-2 (d) · ek sayılar — koşudan SONRA yazıldı, karar girdisi değildir.

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz5_2_isaretler_2026-11-16/ek_hesap.py

Karar kuralının hesabı `sonuc_hesap.py`dedir; burası `sonuc.md` §5'in
("kuraldan sonra görülenler") sayılarını üretir. Simülasyon yok.
"""
import statistics as ist

from sonuc_hesap import (ALANLAR, D, ISARETLER, KARISIK, TEMIZ, auc, guc,
                         oku, topla)

# Kaydedicinin kutuları (`kalibrasyon/karistirma_isaretleri.KUTULAR`).
KUTULAR = {"mesgul": (0.0, 1.0, 50), "aciklanamayan": (0.0, 1.0, 50),
           "phy": (0.0, 100.0, 100), "cozulen": (0.0, 300.0, 300),
           "sessizlik": (0.0, 30.0, 300), "selam_kaybi": (0.0, 1.0, 20)}


def KUTU_ORTA(isaret: str, k: int) -> float:
    alt, ust, n = KUTULAR[isaret]
    return alt + (k + 0.5) * (ust - alt) / n

kayit = oku(D)
ikiz = list(kayit["ikiz"].values())

print("== A · sınıf büyüklüğü (düğüm-saniye, 8 tohum toplamı) ==")
for h in ("ikiz",) + KARISIK:
    c = {}
    for r in kayit[h].values():
        for s, n in r["dugum_saniye_n"].items():
            c[s] = c.get(s, 0) + n
    print(f"  {h:<12} " + " · ".join(f"{s} {n}" for s, n in sorted(c.items())))

print("\n== B · sınıf başına ortalama değer (kutu ortası) ==")


def ortalama(rs, siniflar, isaret):
    c = topla(rs, siniflar, "dugum_saniye", isaret)
    n = sum(c.values())
    return sum(KUTU_ORTA(isaret, int(k)) * v for k, v in c.items()) / n if n else None


for isaret in ISARETLER:
    parca = [f"ikiz {ortalama(ikiz, ('ikiz',), isaret):.3f}"]
    for h in KARISIK:
        rs = list(kayit[h].values())
        for ad, s in (("temiz", TEMIZ), ("ed", ("acik|ed",)),
                      ("gir", ("acik|girisim",)), ("uzak", ("acik|uzak",)),
                      ("ses-gir", ("sessiz|girisim",))):
            v = ortalama(rs, s, isaret)
            parca.append(f"{h[:3]}-{ad} {'—' if v is None else f'{v:.3f}'}")
    print(f"  {isaret:<14} " + " · ".join(parca))

print("\n== C · açık evrede uzak alan ↔ temiz, işaret başına G (yön) ==")
for h in KARISIK:
    rs = list(kayit[h].values())
    print(f"  {h:<12} " + " · ".join(
        f"{i} {guc(auc(topla(rs, ('acik|uzak',), 'dugum_saniye', i), topla(rs, TEMIZ, 'dugum_saniye', i)))[0]:.3f}"
        f"({guc(auc(topla(rs, ('acik|uzak',), 'dugum_saniye', i), topla(rs, TEMIZ, 'dugum_saniye', i)))[1]:+d})"
        for i in ISARETLER))

print("\n== D · tespit süresi alana göre (ortanca s · ulaşılan pay · "
      "bağ-dönem) ==")
for h in KARISIK:
    rs = list(kayit[h].values())
    for a in ALANLAR:
        parca = []
        for n in range(1, 6):
            g = [x for r in rs for x in
                 r["tespit_gecikmesi_s"].get(a, {}).get(str(n), [])]
            u = [x for x in g if x is not None]
            parca.append(f"n={n} {ist.median(u) if u else float('nan'):.2f}"
                         f" · {len(u) / len(g) if g else 0:.0%}")
        print(f"  {h[:3]} {a:<8} ({len(g)}) " + " · ".join(parca))

print("\n== E · girişimde yakalama payına göre ikizdeki yanlış alarm ==")
for isaret, yon in (("cozulen", -1), ("selam_kaybi", +1), ("mesgul", -1),
                    ("phy", -1)):
    neg = topla(ikiz, ("ikiz",), "dugum_saniye", isaret)
    nn = sum(neg.values())
    for h in KARISIK:
        rs = list(kayit[h].values())
        poz = topla(rs, ("acik|girisim",), "dugum_saniye", isaret)
        np_ = sum(poz.values())
        kutular = sorted({int(k) for k in poz} | {int(k) for k in neg},
                         reverse=yon < 0)
        satir = []
        for hedef in (0.2, 0.35, 0.5, 0.8):
            secilen = None
            for b in kutular:
                yak = sum(v for k, v in poz.items()
                          if (int(k) >= b if yon > 0 else int(k) <= b)) / np_
                if yak >= hedef:
                    secilen = b
            fa = sum(v for k, v in neg.items()
                     if (int(k) >= secilen if yon > 0 else int(k) <= secilen)
                     ) / nn
            satir.append(f"yakalama ≥ {hedef:.0%}: kutu {secilen} · FA {fa:.1%}")
        print(f"  {isaret:<12} {h[:3]} " + " · ".join(satir))

print("\n== F · S1b: düşük teslimli birimlerde RSSI ortancası (dBm) ==")
for h in KARISIK:
    rs = list(kayit[h].values())
    for ad, s in (("karıştırılan", ("acik|ed", "acik|girisim")),
                  ("temiz", TEMIZ)):
        dagilim = []
        for r in rs:
            for sn in s:
                for k, v in r["bag_teslim_rssi"].get(sn, {}).items():
                    t, _, q = k.partition("|")
                    if int(t) < 5 and q != "yok":
                        dagilim += [-110 + 2 * int(q) + 1] * v
        print(f"  {h:<12} {ad:<12} n {len(dagilim)} · ortanca "
              f"{ist.median(dagilim) if dagilim else float('nan')}")
