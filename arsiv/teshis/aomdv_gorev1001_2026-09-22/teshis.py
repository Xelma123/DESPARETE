"""`gorev-yok/1001` teşhisi — AOMDV ve AODV, TAM pencere (ön-kayıt: onkayit.md).

Protokolü yalnız SAYAN bir alt sınıfla koşar (davranış değişmez): veri
kararında kullanılan bağ ve veri iletim başarısızlığı, 50 s'lik kovalara
ayrılarak sayılır. Koşudan sonra her (bağ, kova) için kanal grafiğinden
kovanın orta anındaki tek deneme başarısı okunur.

Üretici: `python teshis.py` (iki koşum paralel, tam pencere).
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

from kahin import KanalGrafigi  # noqa: E402
from protokoller.aodv import AODV  # noqa: E402
from protokoller.aomdv import AOMDV  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.kosum.sonuc import sonuc_satiri  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402

KOVA_S = 50.0
CIKTI = Path(__file__).parent / "teshis.json"


def _izli(taban):
    class Izli(taban):
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            self.kullanim = Counter()
            self.basarisiz = Counter()

        def sonraki_atlama(self, gozlem):
            karar = super().sonraki_atlama(gozlem)
            if gozlem.paket is not None and karar.sonraki is not None:
                kova = int(float(gozlem.saat_s) // KOVA_S)
                self.kullanim[(int(gozlem.dugum), int(karar.sonraki), kova)] += 1
            return karar

        def iletim_basarisiz(self, gozlem, hedef, tur):
            if tur == "veri" and hedef is not None:
                kova = int(float(gozlem.saat_s) // KOVA_S)
                self.basarisiz[(int(gozlem.dugum), int(hedef), kova)] += 1
            return super().iletim_basarisiz(gozlem, hedef, tur)
    return Izli


def _is(ad):
    t0 = time.perf_counter()
    kfg = Konfig(kol="u1", senaryo="gorev-yok", tohum=1001)
    kur = kurulum_yap(kfg)
    kosu = Kosu(kur, _izli({"aodv": AODV, "aomdv": AOMDV}[ad]))
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "teshis")
    kullanim, basarisiz = Counter(), Counter()
    for d in kosu.dugumler:
        kullanim.update(d.protokol.kullanim)
        basarisiz.update(d.protokol.basarisiz)
    grafik = KanalGrafigi(kur)
    deneme = kfg.yeniden_deneme_siniri + 1
    baglar = []
    for (i, j, kova), n in kullanim.items():
        t = (kova + 0.5) * KOVA_S
        p = grafik._tek_deneme_basarisi(i, j, t)
        baglar.append({"i": i, "j": j, "kova": kova, "t_s": t, "kullanim": n,
                       "basarisiz": basarisiz.get((i, j, kova), 0), "p_tek": p,
                       "p_atlama": 1.0 - (1.0 - p) ** deneme})
    bas, bitis = kfg.olcum_penceresi
    uretilen = Counter(dg.akis_kimligi for dg in kur.trafik.cizelge
                       if bas <= dg.t_s < bitis)
    h = satir["ham"]
    teslim = Counter(a for a, t in zip(h["teslim_akis_kimlikleri"],
                                       h["teslim_dogum_s"]) if bas <= t < bitis)
    akislar = [{"akis": a.kimlik, "kaynak": a.kaynak, "hedef": a.hedef,
                "uretilen": uretilen[a.kimlik], "teslim": teslim[a.kimlik]}
               for a in kur.trafik.akislar]
    top = Counter()
    for dt in satir["teshis"]["dugum"]:
        for k, v in dt.items():
            if isinstance(v, (int, float)):
                top[k] += v
    m = satir["metrikler"]
    return {"ad": ad, "pdr": m["pdr"], "dusen": satir["korunum"]["dusen"],
            "gecerli": satir["korunum"]["gecerli"], "akislar": akislar,
            "baglar": baglar, "teshis": dict(top),
            "kontrol_cerceve": m["kontrol_cerceve"], "sure_s": time.perf_counter() - t0}


if __name__ == "__main__":
    with Pool(2) as havuz:
        sonuc = havuz.map(_is, ["aomdv", "aodv"], chunksize=1)
    CIKTI.write_text(json.dumps(sonuc, ensure_ascii=False, indent=1),
                     encoding="utf-8")
    for r in sonuc:
        tb = sum(b["basarisiz"] for b in r["baglar"])
        zayif = [b for b in r["baglar"] if b["p_atlama"] < 0.90]
        print(f"{r['ad']:<6} pdr {r['pdr']:.4f}  gecerli {r['gecerli']}  "
              f"dusen {r['dusen']}  sure {r['sure_s']:.0f} s")
        print(f"       veri basarisizligi {tb} · bunun "
              f"{sum(b['basarisiz'] for b in zayif)}'i (%"
              f"{100 * sum(b['basarisiz'] for b in zayif) / max(tb, 1):.0f}) "
              f"p_atlama < 0,90 olan baglarda "
              f"(kullanim payi %{100 * sum(b['kullanim'] for b in zayif) / max(sum(b['kullanim'] for b in r['baglar']), 1):.0f})")
        print("       akis teslim/uretilen: " + " ".join(
            f"{a['akis']}:{a['teslim']}/{a['uretilen']}" for a in r["akislar"]))
