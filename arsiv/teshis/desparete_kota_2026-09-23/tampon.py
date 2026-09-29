# ⚠️ K-166 (bağımsız denetim Y-6): bu betik DESPARETE'nin profilini TAM
# vermez; kayıttaki sayılar O GÜNÜN varsayılanıyla üretildi. O gün seçenek
# yoktu (bugünkü karşılığı `secenekler=SECENEK_YOK`); bayraklar ve komut
# alanları kaydın tarihine göre (K-159'a kadar v0.1 = `PROFIL_V01` ve
# `komut_alanlari=True`; K-160 §12'den sonra `komut_alanlari=False`; K-161'den
# sonra `PROFIL_V02`; postür K-158'den önce yoktu). Bugünkü varsayılan v0.3:
# betik DEĞİŞTİRİLMEDEN koşulursa kayıttaki sayıyı ÜRETMEZ (denetçi ölçtü:
# K-157 §6'nın bir satırı bugün 0,766 · 0,380; o günün profiliyle 0,829 ·
# 2,168 birebir). Yeniden üretmek için profili açıkça ver.
"""K-157 — DESPARETE'nin alan başına tampon kotası, küçük dünyada.

Üretici: PYTHONIOENCODING=utf-8 python arsiv/teshis/desparete_kota_2026-09-23/tampon.py
Küçük dünya (14 düğüm), yere toplama, 30 s, tohum 1000 — K-156 §5 ile aynı
koşu. Her senaryo iki kez: kota 6 (varsayılan) ve kota ∞ (kotasız; K-156'nın
davranışı). Bir SONUÇ değil: kotanın bu koşuda ne kadar bağladığına bakar.
"""
import sys
import time
from multiprocessing import Pool

sys.path.insert(0, ".")
sys.path.insert(0, "tests2")

SINIRSIZ = 10 ** 9


def kos(is_):
    senaryo, kota = is_
    from sim2.kosum.kurulum import kurulum_yap
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.sonuc import sonuc_satiri
    from protokoller.desparete import DESPARETE
    from test_kosum import _konfig
    kfg = _konfig(senaryo, 1000, 30.0, trafik_deseni="yere_toplama")
    kur = kurulum_yap(kfg)
    kosu = Kosu(kur, lambda i: DESPARETE(i, kfg.gecit, tampon_kotasi=kota))
    t0 = time.perf_counter()
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "desparete")
    m = satir["metrikler"]
    s = [d.protokol._sayac for d in kosu.dugumler]
    return (senaryo, "inf" if kota == SINIRSIZ else str(kota),
            satir["korunum"]["gecerli"], m["pdr_pencere"],
            m["nrl_bayt_pencere"],
            sum(x["veri_bekletilen"] for x in s),
            sum(x["tampon_alinan"] for x in s),
            sum(x["tampon_kota_disi"] for x in s),
            max(x["tampon_tepe"] for x in s),
            kur.sayaclar.oku("tampon_giris"), kur.sayaclar.oku("tampon_dusen"),
            time.perf_counter() - t0)


if __name__ == "__main__":
    isler = [(s, k) for s in ("statik-yok", "bagimsiz-surekli")
             for k in (6, SINIRSIZ)]
    with Pool(4) as havuz:
        for r in havuz.map(kos, isler):
            print(f"{r[0]:17} kota {r[1]:>3} · gecerli {r[2]} · "
                  f"pdr_pencere {r[3]:.3f} · nrl_bayt_pencere {r[4]:.3f} · "
                  f"bekletme_karari {r[5]} · ayri_paket {r[6]} · "
                  f"kota_disi {r[7]} · alan_tepe {r[8]} · "
                  f"sim_tampon_giris {r[9]:.0f} · sim_tampon_dusen {r[10]:.0f}"
                  f" · {r[11]:.0f} s", flush=True)
