"""OLSR statik düşük hücre teşhisi — aşama 3 (kusur dışlama + nedensel sınama).

Ön-kayıt (ölçümden ÖNCE, 22 Eylül 2026):
  K1 · BAYAT ROTA (kusur adayı): her veri kararında seçilen sonraki atlama, O
       ANDA `_simetrik_mi` ile simetrik mi? İhlal > 0 ise rota bayat → kusur.
  K2 · `hedef_yok` NE ZAMAN: ısınmada (t < 50 s) mı, pencerede mi? Pencerede
       belirginse rota tablosunda boşluk var → ayrıca incelenir.
  N1 · NEDENSEL: RFC 3626 §13 HARFİYEN (bağ katmanı "koptu" deyince
       L_LOST_LINK_time = L_time = şimdi + NEIGHB_HOLD_TIME, §8.5 kaybı).
       Öngörü YAZILMIYOR — §13 histerezisle birlikte yaşar (§14.3: kalite eşiği
       aşınca L_LOST_LINK_time = şimdi − 1) ve gri bölgede kontrol paketleri
       geçtiği için etkisi kısa sürebilir. Sonuç neyse o.
Bu betik repoyu DEĞİŞTİRMEZ; §13 yalnız bu teşhis alt sınıfında.
"""
import json
import sys
import time
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KOK))
sys.path.insert(0, str(KOK / "kalibrasyon"))

from protokoller.olsr import OLSR  # noqa: E402
from protokoller.olsr_bicim import NEIGHB_HOLD_TIME_S  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.kosum.sonuc import sonuc_satiri  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402

CIKTI = Path(__file__).parent / "olsr_teshis2.json"


class Izli(OLSR):
    PENCERE = (50.0, 320.0)

    def __init__(self, kimlik):
        super().__init__(kimlik)
        self.iz = Counter()

    def sonraki_atlama(self, gozlem):
        karar = super().sonraki_atlama(gozlem)
        if gozlem.paket is None:
            return karar
        t = float(gozlem.saat_s)
        evre = ("isinma" if t < self.PENCERE[0] else
                "pencere" if t < self.PENCERE[1] else "bosalma")
        if karar.sonraki is None:
            self.iz["rotasiz_" + evre] += 1
        else:
            self.iz["karar"] += 1
            if not self._simetrik_mi(karar.sonraki, t):
                self.iz["bayat_" + evre] += 1
        return karar

    def iletim_basarisiz(self, gozlem, hedef, tur):
        if tur == "veri":
            self.iz["veri_basarisiz"] += 1
        return super().iletim_basarisiz(gozlem, hedef, tur)


class IzliS13(Izli):
    """RFC 3626 §13 — harfiyen, YALNIZ teşhis için."""

    def iletim_basarisiz(self, gozlem, hedef, tur):
        super().iletim_basarisiz(gozlem, hedef, tur)
        simdi = float(gozlem.saat_s)
        b = self._bag.get(hedef)
        if b is None:
            return ()
        sinir = simdi + NEIGHB_HOLD_TIME_S
        b.bitis = sinir                               # L_time
        h = self._hist.get(hedef)
        if h is not None:
            h.kayip_bitis = sinir                     # L_LOST_LINK_time
        self._kirli = True
        self.iz["s13_bildirim"] += 1
        beyanlar, ek = self._guncelle(simdi)          # §8.5
        return beyanlar + ek


def _is(gorev):
    ad, tohum = gorev
    t0 = time.perf_counter()
    kfg = Konfig(kol="u1", senaryo="statik-yok", tohum=tohum)
    assert (kfg.isinma_s, kfg.olcum_bitis_s) == Izli.PENCERE
    kur = kurulum_yap(kfg)
    kosu = Kosu(kur, {"olsr": Izli, "olsr_s13": IzliS13}[ad])
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "teshis")
    iz = Counter()
    for d in kosu.dugumler:
        iz.update(d.protokol.iz)
    m = satir["metrikler"]
    return {"ad": ad, "tohum": tohum, "pdr": m["pdr"],
            "dusen": satir["korunum"]["dusen"],
            "kontrol_cerceve": m["kontrol_cerceve"], "iz": dict(iz),
            "sure_s": time.perf_counter() - t0}


if __name__ == "__main__":
    gorevler = [(ad, t) for ad in ("olsr", "olsr_s13") for t in (1000, 1001, 1002)]
    with Pool(len(gorevler)) as havuz:
        sonuc = havuz.map(_is, gorevler, chunksize=1)
    CIKTI.write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
    for r in sonuc:
        print(r["ad"], r["tohum"], "pdr", round(r["pdr"], 4), "dusen", r["dusen"],
              "kontrol", r["kontrol_cerceve"], "iz", r["iz"], "sure", round(r["sure_s"]))
