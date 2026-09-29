# ⚠️ K-166 (bağımsız denetim Y-6): bu betik DESPARETE'nin profilini TAM
# vermez; kayıttaki sayılar O GÜNÜN varsayılanıyla üretildi. O gün seçenek
# yoktu (bugünkü karşılığı `secenekler=SECENEK_YOK`); bayraklar ve komut
# alanları kaydın tarihine göre (K-159'a kadar v0.1 = `PROFIL_V01` ve
# `komut_alanlari=True`; K-160 §12'den sonra `komut_alanlari=False`; K-161'den
# sonra `PROFIL_V02`; postür K-158'den önce yoktu). Bugünkü varsayılan v0.3:
# betik DEĞİŞTİRİLMEDEN koşulursa kayıttaki sayıyı ÜRETMEZ (denetçi ölçtü:
# K-157 §6'nın bir satırı bugün 0,766 · 0,380; o günün profiliyle 0,829 ·
# 2,168 birebir). Yeniden üretmek için profili açıkça ver.
"""K-160 §9 — yükün kaynağı (alan ve tetikleyici) ve ikinci tohum.

Üretici: PYTHONIOENCODING=utf-8 python arsiv/teshis/desparete_kabul_2026-09-23/olcek3.py
`olcek.py` ile aynı dünya (N = 40, yere toplama, `statik-yok`, 60 s).
(i) tohum 1000 varsayılan: her kancanın döndürdüğü kontrol çerçevesi,
alanın geçit mi komut hedefi mi olduğuna göre; alan olayları türe ve alana
göre. Sayım yalnız GÖZLER (protokolün kararına dokunmaz). (ii) tohum
1001'de varsayılan ve komutsuz.
"""
import sys
import time
from collections import Counter
from multiprocessing import Pool

sys.path.insert(0, ".")

PENCERE = {"isinma_s": 10.0, "olcum_bitis_s": 50.0, "kosu_bitis_s": 60.0}
_KANCALAR = ("zamanlayici_doldu", "uyandi", "kontrol_alindi",
             "iletim_basarisiz")


def kos(is_):
    ad, tohum, konfig_ek, say = is_
    from protokoller.desparete import DESPARETE
    from sim2.gozlem.kontrol import KontrolIstegi
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.kurulum import kurulum_yap
    from sim2.kosum.sonuc import sonuc_satiri
    from sim2.yapilandirma.konfig import Konfig
    kfg = Konfig(kol="u1", senaryo="statik-yok", tohum=tohum,
                 trafik_deseni="yere_toplama", **konfig_ek, **PENCERE)
    cerceve: Counter = Counter()
    olay: Counter = Counter()
    gecit_tel = kfg.gecit + 1                     # `tel_kimligi`

    def tally(niyetler):
        for n in niyetler:
            if isinstance(n, KontrolIstegi):
                hedef = dict(n.yuk).get("hedef")
                if hedef is None:
                    cerceve[(n.bicim.ad, "-")] += 1
                else:
                    cerceve[(n.bicim.ad, "gecit" if hedef == gecit_tel
                             else "komut")] += 1

    class Sayan(DESPARETE):
        __slots__ = ()

        def _alan_olaylari(self, t):
            for o, h in self.alanlar.olaylar:
                olay[(o, "gecit" if h == self.sink else "komut")] += 1
            return super()._alan_olaylari(t)

        def sonraki_atlama(self, gozlem):
            k = super().sonraki_atlama(gozlem)
            tally(k.niyetler)
            return k

    for kanca in _KANCALAR:
        def sar(asil=getattr(DESPARETE, kanca)):
            def f(self, *a):
                sonuc = asil(self, *a)
                tally(sonuc)
                return sonuc
            return f
        setattr(Sayan, kanca, sar())
    sinif = Sayan if say else DESPARETE
    t0 = time.perf_counter()
    kur = kurulum_yap(kfg)
    kosu = Kosu(kur, lambda i: sinif(i, kfg.gecit))
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "u1")
    p = [d.protokol for d in kosu.dugumler]
    cikti = {"pdr": satir["metrikler"]["pdr"],
             "edinim_tetik": {a: sum(q._sayac[a] for q in p) for a in (
                 "edinim_ilk", "edinim_yeniden", "edinim_onarim",
                 "edinim_koruma")}}
    if say:
        cikti["cerceve_alana_gore"] = dict(sorted(cerceve.items()))
        cikti["olay_alana_gore"] = dict(sorted(olay.items()))
    return ad, cikti, time.perf_counter() - t0


if __name__ == "__main__":
    isler = (("1000_varsayilan_sayimli", 1000, {}, True),
             ("1001_varsayilan", 1001, {}, False),
             ("1001_komut_yok", 1001, {"komut_akis_sayisi": 0}, False))
    with Pool(3) as havuz:
        sonuc = havuz.map(kos, isler, chunksize=1)
    for ad, c, sure in sonuc:
        print(f"== {ad} · {sure:.0f} s", flush=True)
        for k, v in c.items():
            print(f"   {k}: {v}")
