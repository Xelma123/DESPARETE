"""K-198 · İki sönümleme üreteci GERÇEK topolojide aynı kanal istatistiğini
veriyor mu? (ajan, 28 Eylül 2026 — ölçüt ölçmeden önce yazıldı)

Birincil hücrenin dünyası (referans, formasyon, derin sızma, tohum 1003).
Simülasyon KOŞMAZ: aynı topoloji ve karıştırıcı üstünde iki `Sonumleme`
(`tekil`, `blok`) kurulur; 60 düğüm çifti × 240 an (1–75 s) için güç
kazancı, bir parça sonraki kazanç (ardışık ilinti) ve 40 düğüm × 240 an
için karıştırıcı bağı kazancı okunur.

ÖLÇÜT (önceden):
    ortalama farkı            ≤ 0,03
    varyans oranı             0,90 – 1,10
    p1 · p5 · p50 (dB) farkı  ≤ 0,5 dB
    ardışık ilinti farkı      ≤ 0,03
Tek tohum, tek dünya: iki üretecin aynı sayıları DEĞİL aynı dağılımı
vermesi beklenir; fark örneklem gürültüsü kadar olmalı.

    DESPARETE_DUNYA yok — dünya burada açıkça kurulur.
    PYTHONIOENCODING=utf-8 python arsiv/teshis/performans_2026-09-28/denklik.py
"""
import dataclasses
import math
import pathlib
import statistics as ist
import sys

KOK = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KOK))

from sim2.kanal.dunya import referans_2026  # noqa: E402
from sim2.kanal.sonumleme import Sonumleme  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402


def _yuzdelik(x, q):
    s = sorted(x)
    return s[min(len(s) - 1, int(q * len(s)))]


def _ozet(ad, a):
    db = [10 * math.log10(max(v, 1e-12)) for v in a]
    return {"ad": ad, "ort": ist.mean(a), "var": ist.pvariance(a),
            "p1": _yuzdelik(db, 0.01), "p5": _yuzdelik(db, 0.05),
            "p50": _yuzdelik(db, 0.50)}


def main() -> int:
    kfg = referans_2026(kol="denklik", senaryo="formasyon-surekli",
                        tohum=1003, trafik_deseni="yere_toplama",
                        tehdit_senaryosu="derin_sizma")
    kur = kurulum_yap(kfg)
    top = kur.topoloji
    kar = kur.kanal.karistirici
    uye = getattr(kar, "uyeler", (kar,))[0]
    son = {u: Sonumleme(dataclasses.replace(kfg, sonumleme_uretec=u), top)
           for u in ("tekil", "blok")}
    dt = kfg.sonumleme_parca_suresi_s
    n = kfg.dugum_sayisi
    ciftler = [(i, (i * 7 + 3) % n) for i in range(n)] + \
              [(i, (i * 13 + 11) % n) for i in range(20)]
    ciftler = [(i, j) for i, j in ciftler if i != j][:60]
    anlar = [1.0 + 0.31 * k for k in range(240)]
    gecti = True
    for tur in ("dugum", "karistirici"):
        sonuc = {}
        for u, s in son.items():
            a, b = [], []
            for t in anlar:
                if tur == "dugum":
                    for i, j in ciftler:
                        a.append(s.guc_kazanci(i, j, t))
                        b.append(s.guc_kazanci(i, j, t + dt))
                else:
                    for d in range(n):
                        v = uye._bagil_hiz_ms(d, t)
                        a.append(s.karistirici_kazanci(-1, d, t, v))
                        b.append(s.karistirici_kazanci(-1, d, t + dt, v))
            oz = _ozet(u, a)
            ma, mb = ist.mean(a), ist.mean(b)
            kov = ist.mean((x - ma) * (y - mb) for x, y in zip(a, b))
            oz["ilinti"] = kov / math.sqrt(ist.pvariance(a) * ist.pvariance(b))
            oz["n"] = len(a)
            sonuc[u] = oz
        t_, b_ = sonuc["tekil"], sonuc["blok"]
        kosul = {
            "ortalama farkı ≤ 0,03": abs(t_["ort"] - b_["ort"]) <= 0.03,
            "varyans oranı 0,90–1,10": 0.90 <= b_["var"] / t_["var"] <= 1.10,
            "yüzdelikler ≤ 0,5 dB": all(abs(t_[q] - b_[q]) <= 0.5
                                        for q in ("p1", "p5", "p50")),
            "ardışık ilinti farkı ≤ 0,03":
                abs(t_["ilinti"] - b_["ilinti"]) <= 0.03,
        }
        print(f"\n{tur} bağı (n = {t_['n']})")
        for oz in (t_, b_):
            print(f"  {oz['ad']:<6} ort {oz['ort']:.4f} · var {oz['var']:.4f} · "
                  f"p1 {oz['p1']:+.2f} dB · p5 {oz['p5']:+.2f} · p50 "
                  f"{oz['p50']:+.2f} · ardışık ilinti {oz['ilinti']:.4f}")
        for ad, ok in kosul.items():
            print(f"  {'✅' if ok else '🔴'} {ad}")
            gecti &= ok
    print(f"\nDENKLİK: {'GEÇTİ' if gecti else 'KALDI'}")
    return 0 if gecti else 1


if __name__ == "__main__":
    raise SystemExit(main())
