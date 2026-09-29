"""Denetim K-1'in mekanizma iddiasının bağımsız kısa sınaması.

Küçük dünya (tests2 KUCUK), yere toplama, C; v0.2 (SECENEK_YOK) ↔ v0.3
(varsayılan). Sayılan: geçitte işlenen istek, geçitte tur artışı, ağda
istek gönderilen/iletilen/ACTIVE-dışı ret, solicit gönderilen/yanıtlanan,
geçidin açtığı aday, pencere PDR'si. Depoya yazmaz.
"""
import sys
import time
from multiprocessing import Pool

KOK = "."                    # depo kökünden koşulur
sys.path.insert(0, KOK)
sys.path.insert(0, KOK + r"\tests2")

BITIS = 120.0


def kos(is_):
    senaryo, tohum, profil = is_
    from test_kosum import KUCUK
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_bayrak import PROFIL_V02, SECENEK_V03, SECENEK_YOK
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.kurulum import kurulum_yap
    from sim2.kosum.sonuc import sonuc_satiri
    from sim2.yapilandirma.konfig import Konfig
    ek = dict(KUCUK)
    if not senaryo.endswith("-yok"):
        ek.setdefault("karistirici_guc_override_dbm", 0.0)
    kfg = Konfig(kol="k1_" + profil, senaryo=senaryo, tohum=tohum,
                 trafik_deseni="yere_toplama", isinma_s=20.0,
                 olcum_bitis_s=110.0, kosu_bitis_s=BITIS, **ek)
    sec = SECENEK_V03 if profil == "v03" else SECENEK_YOK
    t0 = time.perf_counter()
    kur = kurulum_yap(kfg)
    g = kfg.gecit
    kosu = Kosu(kur, lambda i: DESPARETE(i, sink=g, bayraklar=PROFIL_V02,
                                        secenekler=sec))
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "desparete")
    p = [d.protokol for d in kosu.dugumler]

    def top(ad):
        return sum(q._sayac[ad] for q in p)

    return {
        "is": is_, "sure": time.perf_counter() - t0,
        "pdr_pencere": satir["metrikler"]["pdr_pencere"],
        "gecit_hedefte_istek": p[g]._sayac["hedefte_istek"],
        "gecit_tur_artis": p[g].alanlar.sayac["tur_artirildi"],
        "gecit_aday": p[g].komsular.sayac["aday_acilan"],
        "istek_gonderilen": top("istek_gonderilen"),
        "istek_iletilen": top("istek_iletilen"),
        "istek_aktif_disi": top("istek_aktif_disi"),
        "solicit_gonderilen": top("solicit_gonderilen"),
        "solicit_yanitlanan": top("solicit_yanitlanan"),
    }


if __name__ == "__main__":
    isler = [(s, 1000, pr) for s in ("bagimsiz-yok", "formasyon-yok")
             for pr in ("v02", "v03")]
    t0 = time.perf_counter()
    with Pool(4) as havuz:
        for r in havuz.imap(kos, isler):
            print(r, flush=True)
    print(f"duvar {time.perf_counter() - t0:.0f} s")
