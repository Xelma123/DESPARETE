"""Faz 5-2 teşhis (d) · karar kuralının hesabı — `beklenti.md` §3 (koşudan
ÖNCE yazıldı). Simülasyon yok; kayıtları okur.

    PYTHONIOENCODING=utf-8 py -3.11 \\
        arsiv/teshis/faz5_2_isaretler_2026-11-16/sonuc_hesap.py [kayıt dizini]

Kayıt dizini verilmezse bu klasör. Birebirlik için teşhis (c)'nin
kayıtları `../faz5_2_rakip_cizgisi_2026-11-15/`den okunur.
"""
from __future__ import annotations

import json
import statistics as ist
import sys
from collections import Counter
from pathlib import Path

D = Path(__file__).resolve().parent
C = D.parent / "faz5_2_rakip_cizgisi_2026-11-15"
HUCRE = ("ikiz", "birincil", "dayaniklilik")
KARISIK = ("birincil", "dayaniklilik")
ALANLAR = ("ed", "girisim")
TEMIZ = ("once|ed", "once|girisim", "once|uzak")
ISARETLER = ("mesgul", "aciklanamayan", "phy", "cozulen", "sessizlik",
             "selam_kaybi")
GUCLU, ZAYIF = 0.80, 0.70           # ayırma gücü G = max(AUC, 1 − AUC)
TOHUM_PAYI = 0.75                   # tohumların ≥ 3/4'ünde aynı yön
YAKALAMA = 0.80                     # eşik: karıştırılanların %80'ini yakalar
FA_SINIRI = 1e-3                    # S2: çerçeve başına yanlış alarm
GECIKME_SINIRI_S = 3.0              # S2: ortanca tespit süresi
ULASMA_PAYI = 0.50                  # S2: dönem içinde ulaşılan pay
S3_BANT_SINIRI = 0.10               # S3: bant değişim oranı
N_DIZI = (1, 2, 3, 4, 5)
BIREBIR = ("gecerli", "pdr", "pdr_pencere", "uretilen", "teslim",
           "sayaclar")


# ---------------------------------------------------------------- okuma
def oku(dizin: Path) -> dict[str, dict[int, dict]]:
    kayit: dict[str, dict[int, dict]] = {}
    for h in HUCRE:
        yol = dizin / f"kayit_{h}.json"
        if yol.exists():
            rs = json.loads(yol.read_text(encoding="utf-8"))["sonuc"]
            kayit[h] = {r["tohum"]: r for r in rs}
    return kayit


def birebirlik(kayit: dict) -> list[str]:
    """Kaydedici davranışı değiştirmedi: teşhis (c)'nin Babel satırı."""
    fark: list[str] = []
    for h, rs in kayit.items():
        yol = C / f"kayit_{h}.json"
        if not yol.exists():
            fark.append(f"{h}: teşhis (c) kaydı yok")
            continue
        c = {r["tohum"]: r for r in json.loads(
            yol.read_text(encoding="utf-8"))["sonuc"]
            if r["protokol"].startswith("babel")}
        for t, r in rs.items():
            if t not in c:
                fark.append(f"{h} {t}: teşhis (c)'de yok")
                continue
            for a in BIREBIR:
                if r[a] != c[t][a]:
                    if a == "sayaclar":
                        ks = sorted(k for k in set(r[a]) | set(c[t][a])
                                    if r[a].get(k) != c[t][a].get(k))
                        fark.append(f"{h} {t}: sayaç farkı {ks[:8]}")
                    else:
                        fark.append(f"{h} {t}: {a} {r[a]} ≠ {c[t][a]}")
    return fark


# ------------------------------------------------------------ yardımcı
def topla(rs, siniflar, alan_adi, isaret=None) -> Counter:
    """Histogramları toplar (kutu → adet); "yok" dışarıda."""
    c: Counter = Counter()
    for r in rs:
        for s in siniflar:
            h = r[alan_adi].get(s, {})
            if isaret is not None:
                h = h.get(isaret, {})
            for k, v in h.items():
                if k != "yok":
                    c[k] += v
    return c


def auc(poz: Counter, neg: Counter) -> float | None:
    """P(X_poz > X_neg) + ½ P(=) — sıralı kutular (tamsayı)."""
    np_, nn = sum(poz.values()), sum(neg.values())
    if not np_ or not nn:
        return None
    kutular = sorted({int(k) for k in poz} | {int(k) for k in neg})
    alt = 0.0
    toplam = 0.0
    for b in kutular:
        p = poz.get(str(b), 0) / np_
        q = neg.get(str(b), 0) / nn
        toplam += p * (alt + 0.5 * q)
        alt += q
    return toplam


def guc(a: float | None) -> tuple[float | None, int]:
    if a is None:
        return None, 0
    return max(a, 1.0 - a), (1 if a > 0.5 else (-1 if a < 0.5 else 0))


def esik_ve_fa(poz: Counter, neg: Counter, yon: int) -> tuple[int, float]:
    """Karıştırılanların ≥ %80'ini yakalayan en seçici kutu ve o eşikte
    karıştırıcısız ikizdeki yanlış alarm payı."""
    np_, nn = sum(poz.values()), sum(neg.values())
    kutular = sorted({int(k) for k in poz} | {int(k) for k in neg})
    if yon < 0:
        kutular = kutular[::-1]
    secilen = kutular[0]
    for b in kutular:
        yakalanan = sum(v for k, v in poz.items()
                        if (int(k) >= b if yon > 0 else int(k) <= b)) / np_
        if yakalanan >= YAKALAMA:
            secilen = b
    fa = sum(v for k, v in neg.items()
             if (int(k) >= secilen if yon > 0 else int(k) <= secilen)) / nn
    return secilen, fa


# ------------------------------------------------------------------- S1
def s1a(kayit: dict) -> dict:
    """Düğüm-saniye işaretleri: karıştırılan alan ↔ temiz (aynı koşu)."""
    print("\n== S1a · düğüm-saniye işaretleri (G = ayırma gücü, yön "
          "+: karıştırılanda büyük) ==")
    sonuc: dict = {}
    for alan in ALANLAR:
        for isaret in ISARETLER:
            satir = {}
            for h in KARISIK:
                rs = list(kayit.get(h, {}).values())
                poz = topla(rs, (f"acik|{alan}",), "dugum_saniye", isaret)
                neg = topla(rs, TEMIZ, "dugum_saniye", isaret)
                g, yon = guc(auc(poz, neg))
                tohum_yon = []
                for r in rs:
                    gt, yt = guc(auc(topla([r], (f"acik|{alan}",),
                                           "dugum_saniye", isaret),
                                     topla([r], TEMIZ, "dugum_saniye",
                                           isaret)))
                    tohum_yon.append(yt)
                ayni = sum(y == yon for y in tohum_yon)
                satir[h] = (g, yon, ayni, len(rs), sum(poz.values()))
            gs = [satir[h][0] for h in KARISIK]
            yonler = {satir[h][1] for h in KARISIK}
            tutarli = (len(yonler) == 1 and all(
                satir[h][2] >= TOHUM_PAYI * satir[h][3] for h in KARISIK))
            if None in gs or not tutarli:
                hukum = "dışarıda"
            elif min(gs) >= GUCLU:
                hukum = "güçlü"
            elif min(gs) >= ZAYIF:
                hukum = "zayıf"
            else:
                hukum = "dışarıda"
            sonuc[(alan, isaret)] = (satir, hukum)
            print(f"  {alan:<8} {isaret:<14} " + " · ".join(
                f"{h[:3]} G {satir[h][0]:.3f} yön {satir[h][1]:+d} "
                f"tohum {satir[h][2]}/{satir[h][3]} n {satir[h][4]}"
                if satir[h][0] is not None else f"{h[:3]} —"
                for h in KARISIK) + f" → {hukum}")
    return sonuc


def s1a_esik(kayit: dict, s1: dict) -> None:
    print("\n  Güçlü ve zayıf işaretlerde %80 yakalayan eşik ve "
          "karıştırıcısız ikizdeki yanlış alarm:")
    ikiz = list(kayit.get("ikiz", {}).values())
    for (alan, isaret), (satir, hukum) in s1.items():
        if hukum == "dışarıda" or not ikiz:
            continue
        yon = satir["birincil"][1]
        for h in KARISIK:
            rs = list(kayit[h].values())
            poz = topla(rs, (f"acik|{alan}",), "dugum_saniye", isaret)
            neg = topla(ikiz, ("ikiz",), "dugum_saniye", isaret)
            b, fa = esik_ve_fa(poz, neg, yon)
            print(f"    {alan:<8} {isaret:<14} {h[:3]} eşik kutusu {b} · "
                  f"ikizde yanlış alarm {fa:.3%}")


def s1_kontrol(kayit: dict) -> dict:
    """Karıştırılmayan sınıflar temizden ayrışmamalı (öngörü 11–13)."""
    print("\n  Karıştırılmayanlar temizden ayrışıyor mu (en büyük G):")
    sonuc: dict = {}
    for ad, kaynak, siniflar in (
            ("acik|uzak", KARISIK, ("acik|uzak",)),
            ("sessiz", KARISIK, ("sessiz|ed", "sessiz|girisim",
                                 "sessiz|uzak"))):
        en = 0.0
        for h in kaynak:
            rs = list(kayit.get(h, {}).values())
            for isaret in ISARETLER:
                g, _ = guc(auc(topla(rs, siniflar, "dugum_saniye", isaret),
                               topla(rs, TEMIZ, "dugum_saniye", isaret)))
                if g is not None:
                    en = max(en, g)
        sonuc[ad] = en
        print(f"    {ad:<10} en büyük G {en:.3f}")
    en = 0.0
    ikiz = list(kayit.get("ikiz", {}).values())
    for h in KARISIK:
        rs = list(kayit.get(h, {}).values())
        for isaret in ISARETLER:
            g, _ = guc(auc(topla(ikiz, ("ikiz",), "dugum_saniye", isaret),
                           topla(rs, TEMIZ, "dugum_saniye", isaret)))
            if g is not None:
                en = max(en, g)
    sonuc["ikiz"] = en
    print(f"    {'ikiz':<10} en büyük G {en:.3f}")
    return sonuc


def s1b(kayit: dict) -> dict:
    """Bağ düzeyi tutarlılık: düşük deneme başarısında RSSI."""
    print("\n== S1b · düşük teslimli (< 0,5) bağ birimlerinde RSSI "
          "(karıştırılan alıcı ↔ temiz) ==")
    sonuc: dict = {}
    poz_s = tuple(f"acik|{a}" for a in ALANLAR)

    def rssi(rs, siniflar) -> tuple[Counter, int, int]:
        c: Counter = Counter()
        dusuk = toplam = 0
        for r in rs:
            for s in siniflar:
                for k, v in r["bag_teslim_rssi"].get(s, {}).items():
                    t, _, q = k.partition("|")
                    toplam += v
                    if int(t) < 5:
                        dusuk += v
                        if q != "yok":
                            c[q] += v
        return c, dusuk, toplam

    for h in KARISIK:
        rs = list(kayit.get(h, {}).values())
        pz, pd, pt = rssi(rs, poz_s)
        ng, nd, nt = rssi(rs, TEMIZ)
        a = auc(pz, ng)
        ayni = sum(1 for r in rs
                   if (x := auc(rssi([r], poz_s)[0], rssi([r], TEMIZ)[0]))
                   is not None and x > 0.5)
        sonuc[h] = (a, ayni, len(rs), pd / pt if pt else None,
                    nd / nt if nt else None)
        print(f"  {h:<12} AUC (karıştırılanda güçlü) "
              f"{'—' if a is None else f'{a:.3f}'} · tohum {ayni}/{len(rs)}"
              f" · düşük teslim payı: karıştırılan "
              f"{'—' if not pt else f'{pd / pt:.1%}'} ({pt}) · temiz "
              f"{'—' if not nt else f'{nd / nt:.1%}'} ({nt})")
    aucs = [sonuc[h][0] for h in KARISIK if h in sonuc]
    tutarli = all(sonuc[h][1] >= TOHUM_PAYI * sonuc[h][2] for h in sonuc)
    if len(aucs) < 2 or None in aucs or not tutarli:
        hukum = "dışarıda"
    else:
        hukum = ("güçlü" if min(aucs) >= GUCLU else
                 "zayıf" if min(aucs) >= ZAYIF else "dışarıda")
    print(f"  → tutarlılık kuralı: {hukum}")
    sonuc["hukum"] = hukum
    return sonuc


# ------------------------------------------------------------------- S2
def s2(kayit: dict) -> dict:
    print("\n== S2 · art arda MAC vazgeçmesi ==")

    def oranlar(rs, siniflar) -> dict[int, float | None]:
        dizi: Counter = Counter()
        cerceve = 0
        for r in rs:
            for s in siniflar:
                cerceve += r["cerceve_n"].get(s, 0)
                for k, v in r["vazgecme_dizisi"].get(s, {}).items():
                    dizi[int(k)] += v
        return {n: (sum(v for L, v in dizi.items() if L >= n) / cerceve
                    if cerceve else None) for n in N_DIZI}

    def deneme_ort(rs, siniflar) -> float | None:
        top = say = 0
        for r in rs:
            for s in siniflar:
                for k, v in r["deneme"].get(s, {}).items():
                    top += int(k) * v
                    say += v
        return top / say if say else None

    ikiz = list(kayit.get("ikiz", {}).values())
    r_ikiz = oranlar(ikiz, ("ikiz",))
    print(f"  ikiz        dizi ≥ n / çerçeve: " + " · ".join(
        f"{n}: {r_ikiz[n]:.2e}" for n in N_DIZI if r_ikiz[n] is not None)
        + f" · deneme ort {deneme_ort(ikiz, ('ikiz',)) or 0:.2f}")
    sonuc: dict = {"ikiz": r_ikiz}
    for h in KARISIK:
        rs = list(kayit.get(h, {}).values())
        for ad, s in (("temiz", TEMIZ), ("ed", ("acik|ed",)),
                      ("girisim", ("acik|girisim",)),
                      ("uzak", ("acik|uzak",))):
            r = oranlar(rs, s)
            sonuc[(h, ad)] = r
            print(f"  {h[:3]} {ad:<8} dizi ≥ n / çerçeve: " + " · ".join(
                f"{n}: {r[n]:.2e}" for n in N_DIZI if r[n] is not None)
                + f" · deneme ort {deneme_ort(rs, s) or 0:.2f}")
        for n in N_DIZI:
            gecikme = [g for r in rs for a in ALANLAR
                       for g in r["tespit_gecikmesi_s"].get(a, {}).get(
                           str(n), [])]
            ulasan = [g for g in gecikme if g is not None]
            sonuc[(h, "gecikme", n)] = (
                ist.median(ulasan) if ulasan else None,
                len(ulasan) / len(gecikme) if gecikme else None,
                len(gecikme))
        print(f"  {h[:3]} tespit (ED + girişim; ortanca s · ulaşılan pay · "
              f"bağ-dönem): " + " · ".join(
                  f"n={n}: {sonuc[(h, 'gecikme', n)][0]} · "
                  f"{(sonuc[(h, 'gecikme', n)][1] or 0):.0%} · "
                  f"{sonuc[(h, 'gecikme', n)][2]}" for n in N_DIZI))
    yildiz = None
    for n in N_DIZI:
        fa = [sonuc[(h, "temiz")][n] for h in KARISIK] + [r_ikiz[n]]
        if None not in fa and max(fa) <= FA_SINIRI:
            yildiz = n
            break
    if yildiz is None:
        hukum = "yetmez (hiçbir n yanlış alarm sınırının altında değil)"
    else:
        iyi = all(sonuc[(h, "gecikme", yildiz)][0] is not None
                  and sonuc[(h, "gecikme", yildiz)][0] <= GECIKME_SINIRI_S
                  and sonuc[(h, "gecikme", yildiz)][1] >= ULASMA_PAYI
                  for h in KARISIK)
        hukum = (f"n* = {yildiz}; tek başına "
                 f"{'yeter' if iyi else 'yetmez (tespit geç ya da seyrek)'}")
    print(f"  → {hukum}")
    sonuc["yildiz"] = yildiz
    sonuc["hukum"] = hukum
    return sonuc


# ------------------------------------------------------------------- S3
def s3(kayit: dict) -> dict:
    print("\n== S3 · bağ kalitesinin değişim hızı (kâhin, ikiz) ==")
    rs = [r for r in kayit.get("ikiz", {}).values() if r.get("s3")]
    if not rs:
        print("  —")
        return {}
    taular = sorted({int(t) for r in rs for t in r["s3"]["bant_degisim"]})
    ort = {t: ist.mean(r["s3"]["bant_degisim"][str(t)] for r in rs)
           for t in taular}
    fark = {t: ist.mean(r["s3"]["ort_fark"][str(t)] for r in rs)
            for t in taular}
    for t in taular:
        print(f"  τ {t:>2} s · bant değişimi {ort[t]:.1%} · ortalama "
              f"|Δp| {fark[t]:.3f}")
    yildiz = max((t for t in taular if ort[t] <= S3_BANT_SINIRI),
                 default=None)
    print(f"  → bant değişimi ≤ %10 olan en uzun τ: {yildiz} s "
          f"(bağ sayısı {[r['s3']['bag'] for r in rs]})")
    return {"oran": ort, "yildiz": yildiz}


def main() -> int:
    dizin = Path(sys.argv[1]) if len(sys.argv) > 1 else D
    kayit = oku(dizin)
    print("== 0 · geçerlilik ==")
    for h, rs_ in kayit.items():
        rs = list(rs_.values())
        print(f"  {h:<12} koşu {len(rs)} · geçerli "
              f"{sum(r['gecerli'] for r in rs)} · süre "
              f"{min(r['sure_s'] for r in rs) / 3600:.2f}–"
              f"{max(r['sure_s'] for r in rs) / 3600:.2f} sa")
    fark = birebirlik(kayit)
    print(f"  birebirlik (teşhis (c)'nin Babel satırı): "
          f"{'tam' if not fark else f'{len(fark)} FARK'}")
    for f in fark[:20]:
        print(f"    {f}")
    s1 = s1a(kayit)
    s1a_esik(kayit, s1)
    s1_kontrol(kayit)
    s1b(kayit)
    s2(kayit)
    s3(kayit)
    return 1 if fark else 0


if __name__ == "__main__":
    raise SystemExit(main())
