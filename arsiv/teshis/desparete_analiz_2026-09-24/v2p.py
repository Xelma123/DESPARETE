"""K-165 §2 — tam ölçekte v0.3 + V2+ (hedefli canlılık).

Üretici: PYTHONIOENCODING=utf-8 python arsiv/teshis/desparete_analiz_2026-09-24/v2p.py
Tam ölçek (N = 40), yere toplama, C; 40 s (K-161 §6 penceresi); v0.3 + V2+
tohum 1000–1002 × dört `-yok` kolu; eşleşik onarım sayımı için tohum 1000'de
üç hareketli kolda v0.3. v0.3'ün PDR ve kontrol/veri değerleri K-163 §4'ten.
"""
import sys
import time
from multiprocessing import Pool

sys.path.insert(0, ".")

PENCERE = {"isinma_s": 10.0, "olcum_bitis_s": 35.0, "kosu_bitis_s": 40.0}
KOLLAR = ("statik-yok", "bagimsiz-yok", "gorev-yok", "formasyon-yok")
TOHUMLAR = (1000, 1001, 1002)
# K-163 §4 (v0.3 = V157): (PDR, kâhin PDR, kontrol/veri)
V03 = {("statik-yok", 1000): (0.834, 0.985, 0.57),
       ("statik-yok", 1001): (0.824, 0.996, 0.54),
       ("statik-yok", 1002): (0.857, 0.998, 0.58),
       ("bagimsiz-yok", 1000): (0.607, 0.762, 0.66),
       ("bagimsiz-yok", 1001): (0.710, 0.885, 0.73),
       ("bagimsiz-yok", 1002): (0.639, 0.819, 0.69),
       ("gorev-yok", 1000): (0.791, 0.969, 0.91),
       ("gorev-yok", 1001): (0.651, 0.844, 0.70),
       ("gorev-yok", 1002): (0.704, 0.860, 0.74),
       ("formasyon-yok", 1000): (0.707, 0.765, 0.74),
       ("formasyon-yok", 1001): (0.721, 0.791, 0.79),
       ("formasyon-yok", 1002): (0.719, 0.756, 0.77)}


def kos(is_):
    kol, tohum, v2p = is_
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_bayrak import PROFIL_V02, Secenekler
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.kurulum import kurulum_yap
    from sim2.kosum.sonuc import sonuc_satiri
    from sim2.yapilandirma.konfig import Konfig
    s = Secenekler(yanit_yalniz_onaysiz=True, ihtiyac_nitelik=True,
                   nitelik_olcumu=True, hedefli_canlilik=v2p)
    kfg = Konfig(kol="u1", senaryo=kol, tohum=tohum,
                 trafik_deseni="yere_toplama", **PENCERE)
    t0 = time.perf_counter()
    kur = kurulum_yap(kfg)
    kosu = Kosu(kur, lambda i: DESPARETE(i, kfg.gecit, bayraklar=PROFIL_V02,
                                         secenekler=s))
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "u1")
    m = satir["metrikler"]
    p = [d.protokol for d in kosu.dugumler]
    return (kol, tohum, v2p, satir["korunum"]["gecerli"], m["pdr"],
            (m.get("kontrol_airtime_s") or 0.0) / (m.get("veri_airtime_s") or 1e-9),
            m.get("gecikme_p95_s"),
            sum(q.alanlar.sayac["onarima_girdi"] for q in p),
            sum(q.komsular.sayac["probe_bosta"] for q in p),
            sum(q.komsular.sayac["bosta_atlandi"] for q in p),
            time.perf_counter() - t0)


if __name__ == "__main__":
    isler = [(k, t, True) for k in KOLLAR for t in TOHUMLAR]
    isler += [(k, 1000, False) for k in KOLLAR if not k.startswith("statik")]
    sira = sorted(isler, key=lambda g: g[0].startswith("statik"))
    t0 = time.perf_counter()
    with Pool(8) as havuz:
        ham = {(r[0], r[1], r[2]): r for r in havuz.map(kos, sira, chunksize=1)}
    print(f"{'kol':15}{'tohum':>6}{'v0.3':>7}{'+V2+':>7}{'fark':>7}{'oran':>7}"
          f"{'k/v v0.3':>9}{'k/v':>6}{'p95':>6}{'onarim':>8}{'bosta':>7}"
          f"{'atlandi':>9}")
    for k in KOLLAR:
        for t in TOHUMLAR:
            r = ham[(k, t, True)]
            v03, kahin, kv3 = V03[(k, t)]
            _, _, _, gec, pdr, kv, p95, onr, bos, atl, sure = r
            print(f"{k:15}{t:>6}{v03:>7.3f}{pdr:>7.3f}{pdr - v03:>+7.3f}"
                  f"{pdr / kahin:>7.3f}{kv3:>9.2f}{kv:>6.2f}{(p95 or 0):>6.2f}"
                  f"{onr:>8}{bos:>7}{atl:>9}  {'' if gec else 'GECERSIZ'}"
                  f" ({sure:.0f} s)", flush=True)
    for k in KOLLAR:
        if (k, 1000, False) in ham:
            r = ham[(k, 1000, False)]
            print(f"v0.3 esles {k:15} 1000 pdr {r[4]:.3f} k/v {r[5]:.2f} "
                  f"p95 {(r[6] or 0):.2f} onarim {r[7]}  ({r[10]:.0f} s)")
    print(f"duvar {time.perf_counter() - t0:.0f} s")
