"""K-164 §3 — tam ölçekte v0.3 + V5a (ilanı sakla).

Üretici: PYTHONIOENCODING=utf-8 python arsiv/teshis/desparete_analiz_2026-09-24/v5a.py
Tam ölçek (N = 40), yere toplama, C, v0.3 + V5a; 40 s (K-161 §6 penceresi),
tohum 1000–1002 × dört `-yok` kolu. v0.3 değerleri K-163 §4 · §5'ten.
"""
import sys
import time
from multiprocessing import Pool

sys.path.insert(0, ".")

PENCERE = {"isinma_s": 10.0, "olcum_bitis_s": 35.0, "kosu_bitis_s": 40.0}
KOLLAR = ("statik-yok", "bagimsiz-yok", "gorev-yok", "formasyon-yok")
TOHUMLAR = (1000, 1001, 1002)
# K-163 §4 · §5 (v0.3 = V157): (PDR, kâhin PDR, kontrol/veri, hedef_yok, pencere PDR)
V03 = {("statik-yok", 1000): (0.834, 0.985, 0.57, 118, 0.902),
       ("statik-yok", 1001): (0.824, 0.996, 0.54, 113, 0.879),
       ("statik-yok", 1002): (0.857, 0.998, 0.58, 116, 0.904),
       ("bagimsiz-yok", 1000): (0.607, 0.762, 0.66, None, None),
       ("bagimsiz-yok", 1001): (0.710, 0.885, 0.73, None, None),
       ("bagimsiz-yok", 1002): (0.639, 0.819, 0.69, None, None),
       ("gorev-yok", 1000): (0.791, 0.969, 0.91, None, None),
       ("gorev-yok", 1001): (0.651, 0.844, 0.70, None, None),
       ("gorev-yok", 1002): (0.704, 0.860, 0.74, None, None),
       ("formasyon-yok", 1000): (0.707, 0.765, 0.74, None, None),
       ("formasyon-yok", 1001): (0.721, 0.791, 0.79, None, None),
       ("formasyon-yok", 1002): (0.719, 0.756, 0.77, None, None)}


def kos(is_):
    kol, tohum = is_
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_bayrak import PROFIL_V02, Secenekler
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.kurulum import kurulum_yap
    from sim2.kosum.sonuc import sonuc_satiri
    from sim2.yapilandirma.konfig import Konfig
    s = Secenekler(yanit_yalniz_onaysiz=True, ihtiyac_nitelik=True,
                   nitelik_olcumu=True, ilan_sakla=True)
    kfg = Konfig(kol="u1", senaryo=kol, tohum=tohum,
                 trafik_deseni="yere_toplama", **PENCERE)
    t0 = time.perf_counter()
    kur = kurulum_yap(kfg)
    kosu = Kosu(kur, lambda i: DESPARETE(i, kfg.gecit, bayraklar=PROFIL_V02,
                                         secenekler=s))
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "u1")
    m, kor = satir["metrikler"], satir["korunum"]
    p = [d.protokol for d in kosu.dugumler]
    return (kol, tohum, satir["korunum"]["gecerli"], m["pdr"],
            m["pdr_pencere"],
            (m.get("kontrol_airtime_s") or 0.0) / (m.get("veri_airtime_s") or 1e-9),
            kor["dusen"]["hedef_yok"], m.get("gecikme_p95_s"),
            sum(q._sayac["saklanan_uygulandi"] for q in p),
            time.perf_counter() - t0)


if __name__ == "__main__":
    isler = [(k, t) for k in KOLLAR for t in TOHUMLAR]
    sira = sorted(isler, key=lambda g: g[0].startswith("statik"))
    t0 = time.perf_counter()
    with Pool(8) as havuz:
        ham = {(r[0], r[1]): r for r in havuz.map(kos, sira, chunksize=1)}
    print(f"{'kol':15}{'tohum':>6}{'v0.3':>7}{'+V5a':>7}{'fark':>7}{'oran':>7}"
          f"{'pencere':>9}{'hedef_yok':>11}{'k/v':>6}{'p95':>6}{'uygulanan':>11}")
    for k in KOLLAR:
        for t in TOHUMLAR:
            _, _, gec, pdr, pp, kv, hy, p95, uyg, sure = ham[(k, t)]
            v03, kahin, _kv3, hy3, pp3 = V03[(k, t)]
            hy_s = f"{hy3}->{hy}" if hy3 is not None else f"{hy}"
            pp_s = f"{pp3:.3f}->{pp:.3f}" if pp3 is not None else f"{pp:.3f}"
            print(f"{k:15}{t:>6}{v03:>7.3f}{pdr:>7.3f}{pdr - v03:>+7.3f}"
                  f"{pdr / kahin:>7.3f}  {pp_s:>13} {hy_s:>9}{kv:>6.2f}"
                  f"{(p95 or 0):>6.2f}{uyg:>11}  {'' if gec else 'GECERSIZ'}"
                  f" ({sure:.0f} s)", flush=True)
    print(f"duvar {time.perf_counter() - t0:.0f} s")
