# ⚠️ K-166 (bağımsız denetim Y-6): bu betik DESPARETE'nin profilini TAM
# vermez; kayıttaki sayılar O GÜNÜN varsayılanıyla üretildi. O gün seçenek
# yoktu (bugünkü karşılığı `secenekler=SECENEK_YOK`); bayraklar ve komut
# alanları kaydın tarihine göre (K-159'a kadar v0.1 = `PROFIL_V01` ve
# `komut_alanlari=True`; K-160 §12'den sonra `komut_alanlari=False`; K-161'den
# sonra `PROFIL_V02`; postür K-158'den önce yoktu). Bugünkü varsayılan v0.3:
# betik DEĞİŞTİRİLMEDEN koşulursa kayıttaki sayıyı ÜRETMEZ (denetçi ölçtü:
# K-157 §6'nın bir satırı bugün 0,766 · 0,380; o günün profiliyle 0,829 ·
# 2,168 birebir). Yeniden üretmek için profili açıkça ver.
"""K-158 §4 — postürün bedeli: aynı tohumlarda postürlü ↔ postürsüz.

Üretici: PYTHONIOENCODING=utf-8 python arsiv/teshis/desparete_postur_2026-09-23/ab.py
Küçük dünya (14 düğüm), yere toplama, 30 s, tohum 1000–1004, iki senaryo.
Postürsüz varyant: politika değerlendirmesi hiç yapılmaz (3.5 + K-157
davranışı). Kontrol baytı PENCERE içinde, mesaj biçimine göre dökülür.
Bir SONUÇ değil: ek yük farkının kaynağını ve tohumlar arası yayılımı ayırır.
"""
import sys
import time
from multiprocessing import Pool

sys.path.insert(0, ".")
sys.path.insert(0, "tests2")

TOHUMLAR = (1000, 1001, 1002, 1003, 1004)
SENARYOLAR = ("statik-yok", "bagimsiz-surekli")


def kos(is_):
    senaryo, tohum, posturlu = is_
    from sim2.kosum.kurulum import kurulum_yap
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.sonuc import sonuc_satiri
    from protokoller.desparete import DESPARETE
    from test_kosum import _konfig

    class Postursuz(DESPARETE):
        __slots__ = ()

        def _politika(self, t):
            return []

    sinif = DESPARETE if posturlu else Postursuz
    kfg = _konfig(senaryo, tohum, 30.0, trafik_deseni="yere_toplama")
    kur = kurulum_yap(kfg)
    kosu = Kosu(kur, lambda i: sinif(i, kfg.gecit))
    t0 = time.perf_counter()
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "desparete")
    m = satir["metrikler"]
    bicim = satir["teshis"]["kontrol_duzlemi"]["bicim"]["pencere"]
    return (senaryo, tohum, posturlu, satir["korunum"]["gecerli"],
            m["pdr_pencere"], m["nrl_bayt_pencere"],
            m.get("kontrol_bayt_pencere"), m.get("veri_bayt_pencere"),
            {ad: b["bayt"] for ad, b in bicim.items()},
            time.perf_counter() - t0)


if __name__ == "__main__":
    isler = [(s, t, p) for s in SENARYOLAR for t in TOHUMLAR
             for p in (False, True)]
    with Pool(8) as havuz:
        sonuc = havuz.map(kos, isler)
    for (s, t, p, gecerli, pdr, nrl, kb, vb, bicim, sure) in sonuc:
        print(f"{s:17} {t} {'postur ' if p else 'yok    '} gecerli {gecerli}"
              f" · pdr {pdr:.3f} · nrl {nrl:.3f} · kontrol_bayt {kb:.0f} · "
              f"veri_bayt {vb:.0f} · {sure:.0f} s", flush=True)
        print("    " + " · ".join(f"{ad} {b}" for ad, b in bicim.items()))
