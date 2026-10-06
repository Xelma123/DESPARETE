"""K-215 sonrası protokol kontrolleri — birincil hücre, kısa pencere (Faz 4.4).

    TESHIS_KOK=<kopya> PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
        py -3.11 -u arsiv/teshis/faz4_4_k215_2026-10-06/protokol_kontrol.py

Neden:
  · `kuyruk_kapasitesi` ve `saat_sapma_ppm` K-214'te TTL 32'yle ölçüldü;
    TTL 64'te OLSR'ın döngüdeki paketi kuyruğu daha uzun doldurabilir →
    OLSR'da yeniden (AODV ve AOMDV'de ikisi de birebirdi, TTL ölümleri yok).
  · `saat_ofset_araligi_s` AODV ve AOMDV'de DUYARLI'ydı; sebep düzeltildi
    (`AODV-j`) ve 2 tohumda sınandı → beş tohumda yeniden.

Koşular: OLSR × {taban, kuyruk ×0,5 · ×2, sapma ×0,5 · ×2} × 5 tohum (25)
+ AODV · AOMDV × {taban, ofset ×0,5 · ×2} × 5 tohum (30) = 55.

Ölçüt ölçmeden (`protokol_tarama.py`yle aynı): protokol ve çarpan başına
Δ = tohum başına (PDR_oynatılmış − PDR_taban) ortalaması, band = 2·SD/√5;
beş tohumda iz birebir → BAĞLAMIYOR; |Δ| < R ve |Δ| ≤ band → DUYARSIZ; aksi
DUYARLI. Ofset için ayrıca: AODV ve AOMDV'de beş tohumda İZ BİREBİR bekleniyor
(sebep giderildiyse); değilse başka bir yerel saat bağımlılığı aranır.
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
PLAN = {"olsr": ("kuyruk_kapasitesi", "saat_sapma_ppm"),
        "aodv": ("saat_ofset_araligi_s",),
        "aomdv": ("saat_ofset_araligi_s",)}


def _is(gorev):
    protokol, ad, deger, tohum = gorev
    t0 = time.perf_counter()
    try:
        ek = {} if ad is None else {ad: deger}
        kfg = DS.konfig(kol="protokol_kontrol", senaryo="formasyon-surekli",
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
        return gorev, (s["pdr_pencere"], int(say.oku("kuyruk_tasmasi")),
                       int(say.oku("ttl_olumu")), izi), None, \
            time.perf_counter() - t0
    except Exception as hata:                       # noqa: BLE001
        return gorev, None, f"{type(hata).__name__}: {hata}", 0.0


def main() -> None:
    DS.secimi_oku(["--dunya", "referans_2026"])
    degerler = {(ad, c): D._oynat(ad, c) for ads in PLAN.values()
                for ad in ads for c in D.CARPANLAR}
    gorevler = [(p, None, None, t) for p in PLAN for t in TOHUMLAR]
    gorevler += [(p, ad, degerler[(ad, c)], t) for p, ads in PLAN.items()
                 for ad in ads for c in D.CARPANLAR for t in TOHUMLAR]
    print(f"kopya: {KOK}\ntoplam kosu {len(gorevler)} · 8 isci · "
          f"R {D.R_ESLESTIRILMIS}")
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
        print(f"  {gorev[0]:6} {str(gorev[1]):22} {str(gorev[2]):>8} {gorev[3]}  "
              f"pdr {deger[0]:.4f}  kuyruk_tasmasi {deger[1]:4}  "
              f"ttl_olumu {deger[2]:4}  iz {deger[3][:3]}  {s / 60:.1f} dk")
    print(f"\n{'parametre':22} {'carpan':>6} {'protokol':9} {'d_pdr':>9} "
          f"{'band':>8} {'birebir':>8}  karar")
    for p, ads in PLAN.items():
        for ad in ads:
            for c in D.CARPANLAR:
                v = degerler[(ad, c)]
                ciftler = [(sonuc[(p, ad, v, t)], sonuc[(p, None, None, t)])
                           for t in TOHUMLAR
                           if (p, ad, v, t) in sonuc and (p, None, None, t) in sonuc]
                if len(ciftler) < len(TOHUMLAR):
                    print(f"{ad:22} {c:>6} {p:9}  eksik tohum → GECERSIZ")
                    continue
                d = [a[0] - b[0] for a, b in ciftler]
                ayni = all(a[3] == b[3] for a, b in ciftler)
                ort, band = ist.mean(d), 2 * ist.stdev(d) / len(d) ** 0.5
                if ayni:
                    karar = "BAGLAMIYOR"
                elif abs(ort) < D.R_ESLESTIRILMIS and abs(ort) <= band:
                    karar = "DUYARSIZ"
                else:
                    karar = "DUYARLI"
                print(f"{ad:22} {c:>6} {p:9} {ort:+9.4f} {band:8.4f} "
                      f"{str(ayni):>8}  {karar}")


if __name__ == "__main__":
    main()
