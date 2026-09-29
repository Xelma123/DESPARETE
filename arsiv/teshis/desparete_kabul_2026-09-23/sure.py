# ⚠️ K-166 (bağımsız denetim Y-6): bu betik DESPARETE'nin profilini TAM
# vermez; kayıttaki sayılar O GÜNÜN varsayılanıyla üretildi. O gün seçenek
# yoktu (bugünkü karşılığı `secenekler=SECENEK_YOK`); bayraklar ve komut
# alanları kaydın tarihine göre (K-159'a kadar v0.1 = `PROFIL_V01` ve
# `komut_alanlari=True`; K-160 §12'den sonra `komut_alanlari=False`; K-161'den
# sonra `PROFIL_V02`; postür K-158'den önce yoktu). Bugünkü varsayılan v0.3:
# betik DEĞİŞTİRİLMEDEN koşulursa kayıttaki sayıyı ÜRETMEZ (denetçi ölçtü:
# K-157 §6'nın bir satırı bugün 0,766 · 0,380; o günün profiliyle 0,829 ·
# 2,168 birebir). Yeniden üretmek için profili açıkça ver.
"""K-160 — DESPARETE'nin U1 koşumunun süre bandı, KISA koşuyla.

Üretici: PYTHONIOENCODING=utf-8 python arsiv/teshis/desparete_kabul_2026-09-23/sure.py
Tam ölçek (varsayılan `Konfig`), yere toplama, 60 s'lik koşu (ısınma 10 ·
ölçüm 50), tohum 1000; dört `-yok` kolu × (DESPARETE, ETX kâhini) = 8 iş,
8 işçi — U1'in gerçek koşumuyla aynı eşzamanlılık. Bastığı PDR kapının
PDR'si DEĞİLDİR (kısa pencere); yalnız süre ölçülür.
"""
import sys
import time
from multiprocessing import Pool

sys.path.insert(0, ".")

KOLLAR = ("statik-yok", "bagimsiz-yok", "gorev-yok", "formasyon-yok")
PENCERE = {"isinma_s": 10.0, "olcum_bitis_s": 50.0, "kosu_bitis_s": 60.0}


def kos(is_):
    kol, kahin = is_
    from kalibrasyon.kahin import EnGuvenilirKahin, KanalGrafigi
    from protokoller.desparete import DESPARETE
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.kurulum import kurulum_yap
    from sim2.kosum.sonuc import sonuc_satiri
    from sim2.yapilandirma.konfig import Konfig
    kfg = Konfig(kol="u1", senaryo=kol, tohum=1000,
                 trafik_deseni="yere_toplama", **PENCERE)
    t0 = time.perf_counter()
    kur = kurulum_yap(kfg)
    if kahin:
        grafik = KanalGrafigi(kur)
        kosu = Kosu(kur, lambda i: EnGuvenilirKahin(i, grafik))
    else:
        kosu = Kosu(kur, lambda i: DESPARETE(i, kfg.gecit))
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "u1")
    return (kol, kahin, kfg.dugum_sayisi, satir["korunum"]["gecerli"],
            satir["metrikler"]["pdr"], time.perf_counter() - t0)


if __name__ == "__main__":
    isler = [(k, h) for k in KOLLAR for h in (False, True)]
    t0 = time.perf_counter()
    with Pool(8) as havuz:
        sonuc = havuz.map(kos, isler, chunksize=1)
    duvar = time.perf_counter() - t0
    olcek = 350.0 / PENCERE["kosu_bitis_s"]
    for kol, kahin, n, gecerli, pdr, sure in sonuc:
        print(f"{kol:15} {'kahin    ' if kahin else 'desparete'} N={n} "
              f"gecerli {gecerli} · pdr(kisa) {pdr} · {sure:.0f} s · "
              f"350 s'ye olcekli ~{sure * olcek / 60:.0f} dk", flush=True)
    print(f"duvar {duvar:.0f} s")
