"""K-167 §8 — v0.4'ün uçtan uca tur artışı testine senaryo: ilk artışın anı.

Üretici: PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python -u arsiv/teshis/desparete_edinim_2026-09-25/v04_senaryo.py
Test donanımının yapılandırması (`_konfig`, yere toplama, küçük dünya), 120 s,
üç hareketli kol × tohum 1000 · 1001 · 1002; v0.4 AÇIKÇA. Denetimsiz (hızlı).
"""
import sys
import time
from multiprocessing import Pool

sys.path.insert(0, ".")
sys.path.insert(0, "tests2")

BITIS = 120.0


def kos(is_):
    senaryo, tohum = is_
    from test_kosum import _konfig
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_bayrak import PROFIL_V02, SECENEK_V04
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.kurulum import kurulum_yap
    kfg = _konfig(senaryo, tohum, BITIS, trafik_deseni="yere_toplama")
    t0 = time.perf_counter()
    kur = kurulum_yap(kfg)
    g = kfg.gecit
    tur: list = []

    class Olcen(DESPARETE):
        __slots__ = ()

        def _hedefte(self, y, t):
            once = self.alanlar.alanlar[self.kimlik].dfsn
            r = super()._hedefte(y, t)
            if self.alanlar.alanlar[self.kimlik].dfsn != once:
                tur.append(round(t, 1))
            return r

    kosu = Kosu(kur, lambda i: Olcen(i, g, bayraklar=PROFIL_V02,
                                     secenekler=SECENEK_V04))
    kosu.kostur()
    return senaryo, tohum, round(time.perf_counter() - t0), tur


if __name__ == "__main__":
    isler = [(s, t) for s in ("bagimsiz-yok", "gorev-yok", "formasyon-yok")
             for t in (1000, 1001, 1002)]
    t0 = time.perf_counter()
    with Pool(8) as havuz:
        for r in havuz.imap(kos, isler):
            print(r, flush=True)
    print(f"duvar {time.perf_counter() - t0:.0f} s")
