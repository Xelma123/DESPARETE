"""A8 beklentisi için ANALİTİK türetim (koşu değil): referans dünyanın
`r-` vakalarında karıştırıcı açıkken sürünün ne kadarı ED eşiğinin
(−76 dBm) üstünde karıştırıcı gücü alır — yani güç kipinde susar.

Kurulum yapılır, olay döngüsü KOŞMAZ; karıştırıcının `alinan_guc_w`i
(yavaş kayıp + gölgeleme + sönümleme, A8'de gerçekçi karıştırıcı) düğüm
konumlarında okunur. Geçici `Konfig` alanları `yama_a8`in açtığı dört
anahtarla aynı (burada elle verilir; yama uygulanmadan önce koşulabilsin).

    PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
        python arsiv/teshis/a8_referans_anahtarlar_2026-09-26/ed_payi.py
"""
import math
import pathlib
import statistics as ist
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3]))

from sim2.kanal.dunya import referans_2026  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402

ANAHTAR = dict(tasiyici_dinleme="guc", hiz_uyarlamasi=True,
               yayilim_gecikmesi=True, karistirici_gercekci=True)
PENCERE = dict(karistirici_baslangic_s=5.0, isinma_s=10.0,
               olcum_bitis_s=40.0, kosu_bitis_s=50.0)


def main() -> None:
    for senaryo, tohum in (("statik-surekli", 1009),
                           ("bagimsiz-surekli", 1000)):
        for ad, ek in (("A7 (bugün)", {}), ("A8", ANAHTAR)):
            kfg = referans_2026(kol="regresyon", senaryo=senaryo,
                                tohum=tohum, **PENCERE, **ek)
            kur = kurulum_yap(kfg)
            kar = kur.kanal.karistirici
            for t in (10.0, 25.0, 40.0):
                dbm = []
                for n in range(kfg.dugum_sayisi):
                    w = kar.alinan_guc_w(n, kur.topoloji.konum(n, t), t)
                    dbm.append(10 * math.log10(w * 1e3) if w > 0 else -300)
                ustte = sum(p >= kfg.ed_esigi_dbm for p in dbm)
                print(f"{senaryo:<17} {ad:<11} t={t:>4.0f} s · ED üstü "
                      f"{ustte:>2}/{kfg.dugum_sayisi} · ortanca "
                      f"{ist.median(dbm):6.1f} dBm · en yüksek "
                      f"{max(dbm):6.1f} dBm")


if __name__ == "__main__":
    main()
