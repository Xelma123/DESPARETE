"""Uçtan uca canlılık testi için senaryo seçimi (K-166).

Test donanımının yapılandırması (`_konfig`, tohum 1000, yere toplama,
küçük dünya) ile 60 s; v0.2 ↔ v0.3. Geçitte işlenen istek ve tur artışının
ZAMANLARI kaydedilir → testin en kısa süresi seçilir. Depoya yazmaz.
"""
import sys
import time
from multiprocessing import Pool

KOK = "."                    # depo kökünden koşulur
sys.path.insert(0, KOK)
sys.path.insert(0, KOK + r"\tests2")

BITIS = 60.0


def kos(is_):
    senaryo, profil = is_
    from test_kosum import _konfig
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_bayrak import PROFIL_V02, SECENEK_V03, SECENEK_YOK
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.kurulum import kurulum_yap
    sec = SECENEK_V03 if profil == "v03" else SECENEK_YOK
    kfg = _konfig(senaryo, 1000, BITIS, trafik_deseni="yere_toplama")
    t0 = time.perf_counter()
    kur = kurulum_yap(kfg)
    g = kfg.gecit
    zaman = {"hedefte": [], "tur": []}

    class Olcen(DESPARETE):
        __slots__ = ()

        def _hedefte(self, y, t):
            zaman["hedefte"].append(round(t, 2))
            once = self.alanlar.alanlar[self.kimlik].dfsn \
                if self.kimlik in self.alanlar.alanlar else None
            r = super()._hedefte(y, t)
            sonra = self.alanlar.alanlar[self.kimlik].dfsn \
                if self.kimlik in self.alanlar.alanlar else None
            if once != sonra:
                zaman["tur"].append(round(t, 2))
            return r

    kosu = Kosu(kur, lambda i: Olcen(i, g, bayraklar=PROFIL_V02,
                                     secenekler=sec))
    kosu.kostur()
    p = [d.protokol for d in kosu.dugumler]
    top = lambda ad: sum(q._sayac[ad] for q in p)
    return (senaryo, profil, round(time.perf_counter() - t0), zaman,
            {ad: top(ad) for ad in ("istek_gonderilen", "istek_iletilen",
                                    "istek_aktif_disi", "solicit_gonderilen",
                                    "solicit_yanitlanan")})


if __name__ == "__main__":
    isler = [(s, pr) for s in ("bagimsiz-yok", "gorev-yok", "formasyon-yok",
                               "statik-yok") for pr in ("v02", "v03")]
    t0 = time.perf_counter()
    with Pool(8) as havuz:
        for r in havuz.imap(kos, isler):
            print(r, flush=True)
    print(f"duvar {time.perf_counter() - t0:.0f} s")
