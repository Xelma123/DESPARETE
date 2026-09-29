"""K-166 — test donanımının (`_desparete_kos_denetimli`) kendisiyle: süre ve
sayaçlar. Önbellekli 12 s statik koşular (v0.2 · v0.3) ve formasyon 60 s
v0.2 (tur artışı 50,9 s'de; `uctan_uca_senaryo.py`). Depoya yazmaz.
"""
import sys
import time
from multiprocessing import Pool

KOK = "."                    # depo kökünden koşulur
sys.path.insert(0, KOK)
sys.path.insert(0, KOK + r"\tests2")


def kos(is_):
    senaryo, bitis, profil = is_
    from test_desparete import _desparete_kos_denetimli
    from protokoller.desparete_bayrak import PROFIL_V02, SECENEK_V03, SECENEK_YOK
    t0 = time.perf_counter()
    kfg, kosu, satir, ihlal = _desparete_kos_denetimli(
        senaryo, bitis, PROFIL_V02, False,
        SECENEK_YOK if profil == "v02" else SECENEK_V03)
    p = [d.protokol for d in kosu.dugumler]
    g = kfg.gecit
    top = lambda ad: sum(q._sayac[ad] for q in p)
    return (senaryo, bitis, profil, round(time.perf_counter() - t0), ihlal,
            {"gecit_hedefte": p[g]._sayac["hedefte_istek"],
             "gecit_tur": p[g].alanlar.sayac["tur_artirildi"],
             **{ad: top(ad) for ad in ("istek_gonderilen", "istek_iletilen",
                                       "istek_aktif_disi",
                                       "solicit_gonderilen",
                                       "solicit_yanitlanan")}})


if __name__ == "__main__":
    isler = [("formasyon-yok", 60.0, "v02"), ("formasyon-yok", 60.0, "v03"),
             ("statik-yok", 12.0, "v02"), ("statik-yok", 12.0, "v03")]
    t0 = time.perf_counter()
    with Pool(4) as havuz:
        for r in havuz.imap(kos, isler):
            print(r, flush=True)
    print(f"duvar {time.perf_counter() - t0:.0f} s")
