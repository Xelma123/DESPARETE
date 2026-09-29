# ⚠️ K-166 (bağımsız denetim Y-6): bu betik DESPARETE'nin profilini TAM
# vermez; kayıttaki sayılar O GÜNÜN varsayılanıyla üretildi. O gün seçenek
# yoktu (bugünkü karşılığı `secenekler=SECENEK_YOK`); bayraklar ve komut
# alanları kaydın tarihine göre (K-159'a kadar v0.1 = `PROFIL_V01` ve
# `komut_alanlari=True`; K-160 §12'den sonra `komut_alanlari=False`; K-161'den
# sonra `PROFIL_V02`; postür K-158'den önce yoktu). Bugünkü varsayılan v0.3:
# betik DEĞİŞTİRİLMEDEN koşulursa kayıttaki sayıyı ÜRETMEZ (denetçi ölçtü:
# K-157 §6'nın bir satırı bugün 0,766 · 0,380; o günün profiliyle 0,829 ·
# 2,168 birebir). Yeniden üretmek için profili açıkça ver.
"""3.5 akıl sağlığı kontrolü — DESPARETE, AODV ve OLSR aynı küçük dünyada.

Üretici: PYTHONIOENCODING=utf-8 python arsiv/teshis/desparete_onarim_2026-09-23/ayna.py
Küçük dünya (14 düğüm), yere toplama, 30 s, tohum 1000. Bir SONUÇ değil:
DESPARETE'nin taban protokollerle aynı mertebede teslim edip etmediğine bakar.
"""
import sys, time
sys.path.insert(0, "."); sys.path.insert(0, "tests2")
from sim2.kosum.kurulum import kurulum_yap
from sim2.kosum.kosu import Kosu
from sim2.kosum.sonuc import sonuc_satiri
from protokoller.desparete import DESPARETE
from protokoller.aodv import AODV
from protokoller.olsr import OLSR
from test_kosum import _konfig

for senaryo in ("statik-yok", "bagimsiz-surekli"):
    for ad in ("desparete", "aodv", "olsr"):
        kfg = _konfig(senaryo, 1000, 30.0, trafik_deseni="yere_toplama")
        kur = kurulum_yap(kfg)
        fab = {"desparete": lambda i: DESPARETE(i, kfg.gecit), "aodv": AODV,
               "olsr": OLSR}[ad]
        kosu = Kosu(kur, fab)
        t0 = time.perf_counter()
        kosu.kostur()
        m = sonuc_satiri(kur, kosu.dugumler, ad)["metrikler"]
        print(f"{senaryo:17} {ad:10} pdr_pencere {m['pdr_pencere']:.3f} · "
              f"nrl_bayt_pencere {m['nrl_bayt_pencere']:.3f} · "
              f"kontrol_cerceve {m['kontrol_cerceve']:.0f} · "
              f"{time.perf_counter() - t0:.0f} s", flush=True)
