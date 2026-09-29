"""K-163 §3 — tam ölçekte v0.2 + V1 + V5 + V7.

Üretici: PYTHONIOENCODING=utf-8 python arsiv/teshis/desparete_analiz_2026-09-24/ab_v1v5v7.py
Tam ölçek (N = 40), yere toplama, C, v0.2 + üç seçenek; 40 s (ısınma 10 ·
ölçüm 25 · boşalma 5 — K-161 §6 ile AYNI pencere: `olcum_bitis_s` 35,
`kosu_bitis_s` 40), tohum 1000–1002 × dört `-yok` kolu. v0.2 ve kâhin
değerleri K-161 §6'dan. Bir SONUÇ değil: aday iyileştirmenin ölçümü.
"""
import sys
import time
from multiprocessing import Pool

sys.path.insert(0, ".")

PENCERE = {"isinma_s": 10.0, "olcum_bitis_s": 35.0, "kosu_bitis_s": 40.0}
KOLLAR = ("statik-yok", "bagimsiz-yok", "gorev-yok", "formasyon-yok")
TOHUMLAR = (1000, 1001, 1002)
# K-161 §6 (dogrulama.py): (v0.2 PDR, kâhin PDR, v0.2 kontrol/veri)
V02 = {("statik-yok", 1000): (0.875, 0.985, 1.12),
       ("statik-yok", 1001): (0.864, 0.996, 1.10),
       ("statik-yok", 1002): (0.878, 0.998, 1.27),
       ("bagimsiz-yok", 1000): (0.595, 0.762, 1.44),
       ("bagimsiz-yok", 1001): (0.704, 0.885, 1.64),
       ("bagimsiz-yok", 1002): (0.589, 0.819, 1.48),
       ("gorev-yok", 1000): (0.756, 0.969, 2.11),
       ("gorev-yok", 1001): (0.619, 0.844, 1.56),
       ("gorev-yok", 1002): (0.694, 0.860, 1.58),
       ("formasyon-yok", 1000): (0.670, 0.765, 1.60),
       ("formasyon-yok", 1001): (0.726, 0.791, 1.53),
       ("formasyon-yok", 1002): (0.642, 0.756, 1.60)}


def kos(is_):
    kol, tohum = is_
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_bayrak import PROFIL_V02, Secenekler
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.kurulum import kurulum_yap
    from sim2.kosum.sonuc import sonuc_satiri
    from sim2.yapilandirma.konfig import Konfig
    s = Secenekler(yanit_yalniz_onaysiz=True, ihtiyac_nitelik=True,
                   nitelik_olcumu=True)
    kfg = Konfig(kol="u1", senaryo=kol, tohum=tohum,
                 trafik_deseni="yere_toplama", **PENCERE)
    t0 = time.perf_counter()
    kur = kurulum_yap(kfg)
    kosu = Kosu(kur, lambda i: DESPARETE(i, kfg.gecit, bayraklar=PROFIL_V02,
                                         secenekler=s))
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "u1")
    m = satir["metrikler"]
    return (kol, tohum, satir["korunum"]["gecerli"], m["pdr"],
            (m.get("kontrol_airtime_s") or 0.0) / (m.get("veri_airtime_s") or 1e-9),
            m.get("gecikme_p95_s"), time.perf_counter() - t0)


if __name__ == "__main__":
    isler = [(k, t) for k in KOLLAR for t in TOHUMLAR]
    sira = sorted(isler, key=lambda g: g[0].startswith("statik"))
    t0 = time.perf_counter()
    with Pool(8) as havuz:
        ham = {(r[0], r[1]): r for r in havuz.map(kos, sira, chunksize=1)}
    print(f"{'kol':15}{'tohum':>6}{'v0.2':>7}{'V157':>7}{'fark':>7}{'oran':>7}"
          f"{'k/v v0.2':>10}{'k/v V157':>10}{'p95 s':>8}{'gecerli':>9}")
    for k in KOLLAR:
        for t in TOHUMLAR:
            _, _, gec, pdr, kv, p95, sure = ham[(k, t)]
            v02, kahin, kv02 = V02[(k, t)]
            print(f"{k:15}{t:>6}{v02:>7.3f}{pdr:>7.3f}{pdr - v02:>+7.3f}"
                  f"{pdr / kahin:>7.3f}{kv02:>10.2f}{kv:>10.2f}"
                  f"{(p95 or 0):>8.2f}{str(gec):>9}   ({sure:.0f} s)",
                  flush=True)
    print(f"duvar {time.perf_counter() - t0:.0f} s")
