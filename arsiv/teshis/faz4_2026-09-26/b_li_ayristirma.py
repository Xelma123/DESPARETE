"""4.2 · Li zinciri referans dünyada — anahtar ayrıştırması (ajan, K-187).

H1 (11 düğüm / 2 düğüm verimi) A8 ve tek anahtar kapalı kollarda; aralık
`iletim_menzili_m`, 1200 Hz doygun yük, 5 tohum, temiz kanal (Li aracıyla
AYNI `_kos`).

    PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
        python -u arsiv/teshis/faz4_2026-09-26/b_li_ayristirma.py <kod_koku>
"""
import os
import statistics as ist
import sys
from multiprocessing import Pool

KOD = sys.argv[1] if len(sys.argv) > 1 else os.environ["FAZ4_KOD_KOKU"]
os.environ["FAZ4_KOD_KOKU"] = KOD
os.environ["DESPARETE_DUNYA"] = "referans_2026"
sys.path.insert(0, KOD)

KOLLAR = {"A8": {}, "A8-arf": {"hiz_uyarlamasi": False},
          "A8-guc": {"tasiyici_dinleme": "geometrik"},
          "A8-gecikme": {"yayilim_gecikmesi": False},
          "A8-arf-guc": {"hiz_uyarlamasi": False,
                         "tasiyici_dinleme": "geometrik"}}
TOHUMLAR = range(1000, 1005)


def _is(is_):
    kol, n, tohum = is_
    from kalibrasyon import li_replikasyonu as L
    from kalibrasyon import dunya_secimi as DS
    k = DS.konfig(kol="li")
    # K-220: alan `nominal_bag_m` oldu; eski kopyalarda `iletim_menzili_m`.
    aralik = getattr(k, "nominal_bag_m", None) or k.iletim_menzili_m
    s = L._kos(n, aralik, tohum, 1200.0, 30.0, **KOLLAR[kol])
    return kol, n, tohum, s["verim_hz"]


if __name__ == "__main__":
    isler = [(k, n, t) for k in KOLLAR for n in (2, 11) for t in TOHUMLAR]
    with Pool(8) as havuz:
        sonuc = havuz.map(_is, isler, chunksize=1)
    print(f"{'kol':<12} {'tek atlama':>11} {'11 dugum':>10} {'H1 orani':>9}")
    for k in KOLLAR:
        tek = ist.mean(v for kk, n, _, v in sonuc if kk == k and n == 2)
        uzun = ist.mean(v for kk, n, _, v in sonuc if kk == k and n == 11)
        print(f"{k:<12} {tek:>11.1f} {uzun:>10.2f} {uzun / tek:>9.4f}")
