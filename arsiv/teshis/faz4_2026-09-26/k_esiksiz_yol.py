"""U1-B açıklaması (K-137 §4 yöntemi, referans dünyada) — ajan, K-190.

Her (kol, tohum) hücresinde ve üç anda: kâhin grafiğinin EŞİKSİZ hâli
(tek deneme başarısı p > 0 olan her yönlü bağ), her kaynaktan geçide EN AZ
ATLAMALI yol (AODV'nin RREQ'suyla bulduğu yapıya en yakın) ve o yolun uçtan
uca teslimi Π [1 − (1 − p)^(deneme)]. Eski dünyada her kolun en düşük U1
hücresi bu sayının en düşük olduğu hücreydi (K-137 §4). Simülasyon koşmaz.

    PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
        python arsiv/teshis/faz4_2026-09-26/k_esiksiz_yol.py
"""
import os
import pathlib
import statistics as ist
import sys
from collections import deque
from multiprocessing import Pool

KOK = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KOK))
os.environ["DESPARETE_DUNYA"] = "referans_2026"

KOLLAR = ("statik-yok", "bagimsiz-yok", "gorev-yok", "formasyon-yok")
TOHUMLAR = (1000, 1001, 1002)
ANLAR = (100.0, 200.0, 300.0)


def _is(is_):
    from kalibrasyon import dunya_secimi as DS
    from kalibrasyon.kahin import KanalGrafigi
    from sim2.kosum.kurulum import kurulum_yap
    kol, tohum = is_
    kfg = DS.konfig(kol="u1b", senaryo=kol, tohum=tohum,
                    trafik_deseni="yere_toplama")
    kur = kurulum_yap(kfg)
    g = KanalGrafigi(kur)
    deneme = kfg.yeniden_deneme_siniri + 1
    gecit = kfg.gecit
    kaynaklar = sorted({a.kaynak for a in kur.trafik.akislar
                        if a.hedef == gecit})
    teslimler, atlamalar = [], []
    for t in ANLAR:
        g._tazele(t)
        n = kur.dugum_sayisi
        for s in kaynaklar:
            onceki = {s: None}
            kuyruk = deque([s])
            while kuyruk and gecit not in onceki:
                u = kuyruk.popleft()
                for v in g._etx[u]:
                    if v not in onceki:
                        onceki[v] = u
                        kuyruk.append(v)
            if gecit not in onceki:
                teslimler.append(0.0)
                continue
            yol, v = [], gecit
            while onceki[v] is not None:
                yol.append((onceki[v], v))
                v = onceki[v]
            ptop = 1.0
            for u, w in yol:
                p = 1.0 / g._etx[u][w]
                ptop *= 1.0 - (1.0 - p) ** deneme
            teslimler.append(ptop)
            atlamalar.append(len(yol))
    return kol, tohum, ist.mean(teslimler), ist.mean(atlamalar)


if __name__ == "__main__":
    isler = [(k, t) for k in KOLLAR for t in TOHUMLAR]
    with Pool(4) as havuz:
        sonuc = havuz.map(_is, isler, chunksize=1)
    print(f"{'kol':<16}{'tohum':>6}{'esiksiz en kisa yol teslimi':>30}"
          f"{'ort. atlama':>13}")
    for kol, tohum, teslim, atlama in sonuc:
        print(f"{kol:<16}{tohum:>6}{teslim:>30.4f}{atlama:>13.2f}")
