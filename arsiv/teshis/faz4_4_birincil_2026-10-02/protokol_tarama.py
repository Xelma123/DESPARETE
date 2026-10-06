"""Kâhinle ÖLÇÜLEMEYEN parametreler taban protokollerle (Faz 4.4, K-214).

    TESHIS_KOK=<kopya> PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
        py -3.11 -u arsiv/teshis/faz4_4_birincil_2026-10-02/protokol_tarama.py

Neden: T1 taramasında `kuyruk_kapasitesi`, `saat_ofset_araligi_s`,
`saat_sapma_ppm` ÖLÇÜLEMEDİ çıktı (kâhin koşusunun izi birebir aynı). Aracın
kuralı: "canlı olduğu bir kolda yeniden taranmalı". Kâhinin zamanlayıcısı
yok (saat okumaz) ve kuyruğu 25 pakete bile dolmuyor; bu parametreler
gerçek protokolde canlıdır (birincil hücrede kuyruk taşması bugün 0, ama
başka hücrelerde 90 — regresyon k204).

Grup 1 · AODV · AOMDV · OLSR × {taban, her parametre ×0,5 · ×2} × tohum
1000–1004, birincil hücre, duyarlılık taramasının kısa penceresi (105 koşu).
Oynatılan değerler duyarlılık aracının `_oynat`ı (dünyanın değerine göre).
Grup 2 · BİREBİRLİK: DESPARETE (RSSI kancası olan tek protokol) tohum 1003,
taban + `gps_dikey_sigma_m` · `gps_hiz_sigma_ms` · `rssi_olcum_sigma_db` ×2
(4 koşu). Bugün hiçbir protokol konum ya da RSSI okumuyor (kodda), iz birebir
aynı olmalı.

Ölçüt ölçmeden (grup 1, protokol ve çarpan başına):
  · Δ = tohum başına (PDR_oynatılmış − PDR_taban) ortalaması, band = 2·SD/√5;
  · beş tohumda iz birebir aynı → BAĞLAMIYOR (DUYARSIZ, birebir);
  · |Δ| < R (0,0188) ve |Δ| ≤ band → DUYARSIZ; aksi DUYARLI.
Parametre, üç protokolün hepsinde DUYARSIZ ya da BAĞLAMIYOR ise DUYARSIZ.
Grup 2: dört koşunun izi birebir aynı → BİREBİR; değilse kodla çelişki, aranır.
DESPARETE grup 1'de yok: Faz 5'te değişecek; mühürden önce son hâliyle
yeniden ölçülür.
"""
import os
import pathlib
import statistics as ist
import sys
import time
from multiprocessing import Pool

KOK = pathlib.Path(os.environ.get("TESHIS_KOK")
                   or pathlib.Path(__file__).resolve().parents[3])
for yol in (KOK, KOK / "tests2"):
    if str(yol) not in sys.path:
        sys.path.insert(0, str(yol))
os.environ["DESPARETE_DUNYA"] = "referans_2026"

from kalibrasyon import dunya_secimi as DS  # noqa: E402
from kalibrasyon import duyarlilik as D  # noqa: E402
from kalibrasyon.regresyon_satirlari import _fabrika  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.olcum.metrikler import metrik_sozlugu  # noqa: E402

TOHUMLAR = (1000, 1001, 1002, 1003, 1004)
PROTOKOLLER = ("aodv", "aomdv", "olsr")
PARAMETRELER = ("kuyruk_kapasitesi", "saat_ofset_araligi_s", "saat_sapma_ppm")
BIREBIR = ("gps_dikey_sigma_m", "gps_hiz_sigma_ms", "rssi_olcum_sigma_db")


def _is(gorev):
    protokol, ad, deger, tohum = gorev
    t0 = time.perf_counter()
    try:
        ek = {} if ad is None else {ad: deger}
        kfg = DS.konfig(kol="protokol_tarama", senaryo="formasyon-surekli",
                        tohum=tohum, **{**D.PENCERE, **D.HUCRE_EKLERI["birincil"],
                                        **ek})
        kur = kurulum_yap(kfg)
        Kosu(kur, _fabrika(protokol, kur)).kostur()
        s = metrik_sozlugu(kur.sayaclar.disa_ver(), kur.paket_defteri,
                           kur.rota_defteri)
        say = kur.sayaclar
        izi = (int(say.oku("teslim_paket")), int(say.oku("mac_deneme")),
               int(say.oku("kontrol_cerceve")),
               repr(s["gecikme_ort_s_pencere"]))
        return gorev, (s["pdr_pencere"], int(say.oku("kuyruk_tasmasi")), izi), \
            None, time.perf_counter() - t0
    except Exception as hata:                       # noqa: BLE001
        return gorev, None, f"{type(hata).__name__}: {hata}", 0.0


def main() -> None:
    DS.secimi_oku(["--dunya", "referans_2026"])
    degerler = {(ad, c): D._oynat(ad, c) for ad in PARAMETRELER + BIREBIR
                for c in D.CARPANLAR}
    gorevler = [(p, None, None, t) for p in PROTOKOLLER for t in TOHUMLAR]
    gorevler += [(p, ad, degerler[(ad, c)], t) for p in PROTOKOLLER
                 for ad in PARAMETRELER for c in D.CARPANLAR for t in TOHUMLAR]
    gorevler += [("desparete", None, None, 1003)]
    gorevler += [("desparete", ad, degerler[(ad, 2.0)], 1003) for ad in BIREBIR]
    print(f"kopya: {KOK}\ntoplam kosu {len(gorevler)} · 8 isci · R {D.R_ESLESTIRILMIS}")
    print("degerler:", {f"{a}x{c}": v for (a, c), v in degerler.items()})
    t0 = time.perf_counter()
    with Pool(8) as havuz:
        ham = havuz.map(_is, gorevler, chunksize=1)
    print(f"sure {(time.perf_counter() - t0) / 60:.1f} dk\n")
    sonuc = {}
    for gorev, deger, hata, s in ham:
        if hata:
            print("  HATA", gorev, hata)
            continue
        sonuc[gorev] = deger
        print(f"  {gorev[0]:10} {str(gorev[1]):22} {str(gorev[2]):>8} {gorev[3]}  "
              f"pdr {deger[0]:.4f}  kuyruk_tasmasi {deger[1]:4}  "
              f"iz {deger[2][:3]}  {s / 60:.1f} dk")

    print(f"\n{'parametre':22} {'carpan':>6} {'protokol':9} {'d_pdr':>9} "
          f"{'band':>8} {'birebir':>8}  karar")
    for ad in PARAMETRELER:
        hepsi = True
        for c in D.CARPANLAR:
            for p in PROTOKOLLER:
                v = degerler[(ad, c)]
                ciftler = [(sonuc[(p, ad, v, t)], sonuc[(p, None, None, t)])
                           for t in TOHUMLAR
                           if (p, ad, v, t) in sonuc and (p, None, None, t) in sonuc]
                if len(ciftler) < len(TOHUMLAR):
                    print(f"{ad:22} {c:>6} {p:9}  eksik tohum → GECERSIZ")
                    hepsi = False
                    continue
                d = [a[0] - b[0] for a, b in ciftler]
                ayni = all(a[2] == b[2] for a, b in ciftler)
                ort, band = ist.mean(d), 2 * ist.stdev(d) / len(d) ** 0.5
                if ayni:
                    karar = "BAGLAMIYOR"
                elif abs(ort) < D.R_ESLESTIRILMIS and abs(ort) <= band:
                    karar = "DUYARSIZ"
                else:
                    karar, hepsi = "DUYARLI", False
                print(f"{ad:22} {c:>6} {p:9} {ort:+9.4f} {band:8.4f} "
                      f"{str(ayni):>8}  {karar}")
        print(f"  → {ad}: {'DUYARSIZ' if hepsi else 'DUYARLI / GECERSIZ'}\n")
    taban = sonuc.get(("desparete", None, None, 1003))
    birebir = taban is not None and all(
        sonuc.get(("desparete", ad, degerler[(ad, 2.0)], 1003), (None, None, None))[2]
        == taban[2] for ad in BIREBIR)
    print(f"BIREBIRLIK (DESPARETE, gps/rssi x2): {'🟢 BIREBIR' if birebir else '🔴 FARKLI'}")


if __name__ == "__main__":
    main()
