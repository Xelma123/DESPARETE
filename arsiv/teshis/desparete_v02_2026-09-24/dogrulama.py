# ⚠️ K-166 (bağımsız denetim Y-6): bu betik DESPARETE'nin profilini TAM
# vermez; kayıttaki sayılar O GÜNÜN varsayılanıyla üretildi. O gün seçenek
# yoktu (bugünkü karşılığı `secenekler=SECENEK_YOK`); bayraklar ve komut
# alanları kaydın tarihine göre (K-159'a kadar v0.1 = `PROFIL_V01` ve
# `komut_alanlari=True`; K-160 §12'den sonra `komut_alanlari=False`; K-161'den
# sonra `PROFIL_V02`; postür K-158'den önce yoktu). Bugünkü varsayılan v0.3:
# betik DEĞİŞTİRİLMEDEN koşulursa kayıttaki sayıyı ÜRETMEZ (denetçi ölçtü:
# K-157 §6'nın bir satırı bugün 0,766 · 0,380; o günün profiliyle 0,829 ·
# 2,168 birebir). Yeniden üretmek için profili açıkça ver.
"""K-161 §6 — v0.2 (yalın profil) tam ölçekte kısa pencere doğrulaması.

Üretici: PYTHONIOENCODING=utf-8 python arsiv/teshis/desparete_v02_2026-09-24/dogrulama.py
Tam ölçek (N = 40), yere toplama, C, v0.2; 40 s (ısınma 10 · ölçüm 35);
U1'in tohumları 1000–1002 × dört `-yok` kolu; ETX kâhini AYNI pencere ve
tohumda. Kapının oranı DEĞİLDİR (kısa pencere) — resmi U1'den önce işaret.
"""
import sys
import time
from multiprocessing import Pool

sys.path.insert(0, ".")

PENCERE = {"isinma_s": 10.0, "olcum_bitis_s": 35.0, "kosu_bitis_s": 40.0}
KOLLAR = ("statik-yok", "bagimsiz-yok", "gorev-yok", "formasyon-yok")
TOHUMLAR = (1000, 1001, 1002)


def kos(is_):
    kol, tohum, kahin = is_
    from kalibrasyon.kahin import EnGuvenilirKahin, KanalGrafigi
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_bayrak import PROFIL_V02
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.kurulum import kurulum_yap
    from sim2.kosum.sonuc import sonuc_satiri
    from sim2.yapilandirma.konfig import Konfig
    kfg = Konfig(kol="u1", senaryo=kol, tohum=tohum,
                 trafik_deseni="yere_toplama", **PENCERE)
    t0 = time.perf_counter()
    kur = kurulum_yap(kfg)
    if kahin:
        grafik = KanalGrafigi(kur)
        kosu = Kosu(kur, lambda i: EnGuvenilirKahin(i, grafik))
    else:
        kosu = Kosu(kur, lambda i: DESPARETE(i, kfg.gecit,
                                             bayraklar=PROFIL_V02))
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "u1")
    m = satir["metrikler"]
    return (kol, tohum, kahin, satir["korunum"]["gecerli"], m["pdr"],
            m.get("kontrol_airtime_s") or 0.0, m.get("veri_airtime_s") or 0.0,
            time.perf_counter() - t0)


if __name__ == "__main__":
    isler = [(k, t, h) for k in KOLLAR for t in TOHUMLAR for h in (False, True)]
    # Uzun işler önce (hareketli DESPARETE) — yalnız süreyi etkiler.
    sira = sorted(isler, key=lambda g: (g[0].startswith("statik"), g[2]))
    t0 = time.perf_counter()
    with Pool(8) as havuz:
        ham = dict(zip(sira, havuz.map(kos, sira, chunksize=1)))
    print(f"{'kol':15}{'tohum':>6}{'DESP':>8}{'kahin':>8}{'oran':>7}"
          f"{'esik':>6}{'kontrol/veri':>14}{'gecerli':>9}")
    for k in KOLLAR:
        esik = 0.90 if k.startswith("statik") else 0.60
        for t in TOHUMLAR:
            d = ham[(k, t, False)]
            h = ham[(k, t, True)]
            oran = d[4] / h[4] if h[4] else float("nan")
            kv = d[5] / d[6] if d[6] else float("inf")
            print(f"{k:15}{t:>6}{d[4]:>8.3f}{h[4]:>8.3f}{oran:>7.3f}"
                  f"{esik:>6.2f}{kv:>14.2f}{str(d[3] and h[3]):>9}"
                  f"   ({d[7]:.0f} s / {h[7]:.0f} s)", flush=True)
    print(f"duvar {time.perf_counter() - t0:.0f} s")
