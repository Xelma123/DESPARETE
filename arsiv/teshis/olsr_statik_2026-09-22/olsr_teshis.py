"""OLSR statik düşük hücre teşhisi — aşama 1+2 (ön-kayıt: olsr_teshis_onkayit.md).

Protokolü SAYAN ama davranışını değiştirmeyen bir alt sınıfla koşar:
veri kararlarında kullanılan bağlar ve veri iletim başarısızlıkları bağ
başına sayılır. Koşudan sonra kullanılan her bağın kanal kalitesi kâhin
grafiğinden okunur (statik kolda sönümleme donuk → bağ kalitesi sabit).
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

from protokoller.aodv import AODV  # noqa: E402
from protokoller.olsr import OLSR  # noqa: E402
from kahin import KanalGrafigi  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.kosum.sonuc import sonuc_satiri  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402

CIKTI = Path(__file__).parent / "olsr_teshis.json"


def _izli(taban):
    class Izli(taban):
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            self.iz_kullanim = Counter()
            self.iz_basarisiz = Counter()
            self.iz_kimlik = a[0] if a else None

        def sonraki_atlama(self, gozlem):
            karar = super().sonraki_atlama(gozlem)
            if gozlem.paket is not None and karar.sonraki is not None:
                self.iz_kullanim[(int(gozlem.dugum), int(karar.sonraki))] += 1
            return karar

        def iletim_basarisiz(self, gozlem, hedef, tur):
            if tur == "veri" and hedef is not None:
                self.iz_basarisiz[(int(gozlem.dugum), int(hedef))] += 1
            return super().iletim_basarisiz(gozlem, hedef, tur)
    Izli.__name__ = "Izli" + taban.__name__
    return Izli


def _is(gorev):
    ad, kol, tohum = gorev
    t0 = time.perf_counter()
    kfg = Konfig(kol="u1", senaryo=kol, tohum=tohum)
    kur = kurulum_yap(kfg)
    sinif = _izli({"olsr": OLSR, "aodv": AODV}[ad])
    kosu = Kosu(kur, sinif)
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "teshis")
    kullanim, basarisiz = Counter(), Counter()
    for d in kosu.dugumler:
        kullanim.update(d.protokol.iz_kullanim)
        basarisiz.update(d.protokol.iz_basarisiz)
    grafik = KanalGrafigi(kur)
    deneme = kfg.yeniden_deneme_siniri + 1
    baglar = []
    for (i, j), n in kullanim.items():
        p = grafik._tek_deneme_basarisi(i, j, 0.0)
        baglar.append({"i": i, "j": j, "kullanim": n,
                       "basarisiz": basarisiz.get((i, j), 0),
                       "p_tek": p, "p_atlama": 1.0 - (1.0 - p) ** deneme})
    bas, bitis = kfg.olcum_penceresi
    uretilen = Counter(dg.akis_kimligi for dg in kur.trafik.cizelge
                       if bas <= dg.t_s < bitis)
    h = satir["ham"]
    teslim = Counter(a for a, t in zip(h["teslim_akis_kimlikleri"],
                                       h["teslim_dogum_s"]) if bas <= t < bitis)
    akislar = [{"akis": a.kimlik, "kaynak": a.kaynak, "hedef": a.hedef,
                "uretilen": uretilen[a.kimlik], "teslim": teslim[a.kimlik]}
               for a in kur.trafik.akislar]
    m = satir["metrikler"]
    teshis_top = Counter()
    for dt in satir["teshis"]["dugum"]:
        for k, v in dt.items():
            if isinstance(v, (int, float)):
                teshis_top[k] += v
    return {"ad": ad, "kol": kol, "tohum": tohum, "pdr": m["pdr"],
            "dusen": satir["korunum"]["dusen"],
            "mac_vazgecme": m["mac_vazgecme"], "kontrol_cerceve": m["kontrol_cerceve"],
            "kuyruk_tasmasi": m["kuyruk_tasmasi"], "ttl_olumu": m["ttl_olumu"],
            "hedef_yok": m["hedef_yok"], "akislar": akislar, "baglar": baglar,
            "teshis": dict(teshis_top), "sure_s": time.perf_counter() - t0}


if __name__ == "__main__":
    gorevler = [("olsr", "statik-yok", 1000), ("olsr", "statik-yok", 1001),
                ("olsr", "statik-yok", 1002), ("aodv", "statik-yok", 1001),
                ("aodv", "statik-yok", 1002)]
    with Pool(len(gorevler)) as havuz:
        sonuc = havuz.map(_is, gorevler, chunksize=1)
    CIKTI.write_text(json.dumps(sonuc, ensure_ascii=False, indent=1), encoding="utf-8")
    for r in sonuc:
        print(r["ad"], r["kol"], r["tohum"], "pdr", round(r["pdr"], 4),
              "dusen", r["dusen"], "sure", round(r["sure_s"]))
