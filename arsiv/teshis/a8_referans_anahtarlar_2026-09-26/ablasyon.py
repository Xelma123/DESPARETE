"""A8 ayrıştırması (ajan, 26 Eylül 2026): referans dünyanın üç `r-` vakası,
dört anahtar tek tek — A7 + biri (tek açık) ve A8 − biri (biri kapalı).

Soru: A8'de PDR neden beklenen yöne gitmedi (K-181)? Hangi anahtar ne yaptı?
`A7` ve `A8` satırları `k180` ile `k181`i YENİDEN ÜRETMELİ (aynı konfig) —
üretmezse ayrıştırma geçersiz.

    PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
        python -u arsiv/teshis/a8_referans_anahtarlar_2026-09-26/ablasyon.py
"""
import pathlib
import sys
import time
from multiprocessing import Pool

KOK = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KOK))

VAKALAR = (("r-referans-statik-yok-dogrudan_komsu", "statik-yok",
            "dogrudan_komsu"),
           ("r-referans-bagimsiz-surekli-dogrudan_komsu", "bagimsiz-surekli",
            "dogrudan_komsu"),
           ("r-referans-statik-surekli-aodv", "statik-surekli", "aodv"))
KAPALI = dict(tasiyici_dinleme="geometrik", hiz_uyarlamasi=False,
              yayilim_gecikmesi=False, karistirici_gercekci=False)
ACIK = dict(tasiyici_dinleme="guc", hiz_uyarlamasi=True,
            yayilim_gecikmesi=True, karistirici_gercekci=True)
KISA = {"tasiyici_dinleme": "guc", "hiz_uyarlamasi": "arf",
        "yayilim_gecikmesi": "gecikme", "karistirici_gercekci": "kar"}


def kollar():
    yield "A7", dict(KAPALI)
    for a in KAPALI:
        yield f"A7+{KISA[a]}", {**KAPALI, a: ACIK[a]}
    yield "A8", dict(ACIK)
    for a in ACIK:
        yield f"A8-{KISA[a]}", {**ACIK, a: KAPALI[a]}


def _is(is_):
    from kalibrasyon.regresyon_satirlari import _fabrika
    from sim2.kanal.dunya import referans_2026
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.kurulum import kurulum_yap
    from sim2.kosum.sonuc import sonuc_satiri
    kol, anahtar, (kimlik, senaryo, protokol) = is_
    bas = time.perf_counter()
    kfg = referans_2026(kol="regresyon", senaryo=senaryo, tohum=1010,
                        not_=kimlik, karistirici_baslangic_s=5.0,
                        isinma_s=10.0, olcum_bitis_s=40.0, kosu_bitis_s=50.0,
                        **anahtar)
    kur = kurulum_yap(kfg)
    kosu = Kosu(kur, _fabrika(protokol, kur))
    kosu.kostur()
    s = sonuc_satiri(kur, kosu.dugumler, protokol)
    kr, m = s["korunum"], s["metrikler"]
    return (kimlik, kol, s["korunum"]["gecerli"], m["pdr"], m["pdr_pencere"],
            {k: v for k, v in kr["dusen"].items() if v}, kr["kuyrukta"],
            kr["mac_deneme"], kr["enerji_gonderim_s"],
            time.perf_counter() - bas)


def main():
    isler = [(kol, a, v) for v in VAKALAR for kol, a in kollar()]
    # uzun vakalar önce — havuz dengesi
    isler.sort(key=lambda i: i[2][1] != "bagimsiz-surekli")
    sonuc = {}
    with Pool(8) as havuz:
        for r in havuz.imap_unordered(_is, isler, chunksize=1):
            sonuc[(r[0], r[1])] = r
    for kimlik, _, _ in VAKALAR:
        print(f"\n{kimlik}")
        print(f"  {'kol':<12} {'gecerli':<7} {'pdr':>7} {'pdr_p':>7} "
              f"{'deneme':>7} {'tx_s':>6} {'kuyruk':>6}  düşenler")
        for kol, _ in kollar():
            r = sonuc[(kimlik, kol)]
            print(f"  {kol:<12} {r[2]!s:<7} {r[3]:7.4f} {r[4]:7.4f} "
                  f"{r[7]:7.0f} {r[8]:6.2f} {r[6]:6d}  {r[5]}")


if __name__ == "__main__":
    main()
