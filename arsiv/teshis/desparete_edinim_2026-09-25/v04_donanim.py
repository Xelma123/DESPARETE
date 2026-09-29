"""K-167 §8 — v0.4 (varsayılan) test donanımında: testlerin senaryoları.

Üretici: PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python -u arsiv/teshis/desparete_edinim_2026-09-25/v04_donanim.py
`_desparete_kos_denetimli` (her kancadan sonra döngü ve FD denetimi) ile:
statik 12 s ve formasyon 60 s, v0.4 ve v0.3 (profil AÇIKÇA).
"""
import sys
import time
from multiprocessing import Pool

sys.path.insert(0, ".")
sys.path.insert(0, "tests2")


def kos(is_):
    senaryo, bitis, profil = is_
    from test_desparete import _desparete_kos_denetimli
    from protokoller.desparete_bayrak import (PROFIL_V02, SECENEK_V03,
                                              SECENEK_V04)
    sec = {"v04": SECENEK_V04, "v03": SECENEK_V03}[profil]
    t0 = time.perf_counter()
    kfg, kosu, satir, ihlal = _desparete_kos_denetimli(
        senaryo, bitis, PROFIL_V02, False, sec)
    p = [d.protokol for d in kosu.dugumler]
    g = kfg.gecit
    top = lambda ad: sum(q._sayac[ad] for q in p)
    return (senaryo, bitis, profil, round(time.perf_counter() - t0), ihlal,
            round(satir["metrikler"]["pdr"], 4),
            {"gecit_hedefte": p[g]._sayac["hedefte_istek"],
             "gecit_aclik": p[g]._sayac["hedefte_aclik"],
             "gecit_tur": p[g].alanlar.sayac["tur_artirildi"],
             "gecit_aday": p[g].komsular.sayac["aday_acilan"],
             **{ad: top(ad) for ad in ("istek_gonderilen", "istek_iletilen",
                                       "istek_aktif_disi",
                                       "istek_tanidik_kabul",
                                       "solicit_gonderilen",
                                       "solicit_yanitlanan")}})


if __name__ == "__main__":
    isler = [("formasyon-yok", 60.0, "v04"), ("statik-yok", 12.0, "v04"),
             ("statik-yok", 12.0, "v03")]
    t0 = time.perf_counter()
    with Pool(3) as havuz:
        for r in havuz.imap(kos, isler):
            print(r, flush=True)
    print(f"duvar {time.perf_counter() - t0:.0f} s")
