"""ADIM 5 KAPANIŞ — trafik ve korunum.

Üretici:  PYTHONIOENCODING=utf-8 python kalibrasyon/adim5_kapanis.py

    A. Trafiğin ölçülen hâli (ilan edilenle karşılaştırma)
    B. Korunum denklemi + MUTABAKAT, 30 tohumda
    C. Kuyruk kapasitesinin taşmaya etkisi
"""
from __future__ import annotations

import pathlib
import statistics as ist
import sys

KOK = pathlib.Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.ag.kuyruk import Kuyruk  # noqa: E402
from sim2.ag.paket import PaketSayaci  # noqa: E402
from sim2.ag.trafik import TrafikUreteci  # noqa: E402
from sim2.cekirdek.korunum import KorunumDefteri  # noqa: E402
from sim2.cekirdek.rng import Akislar  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402

TOHUMLAR = range(1, 31)


def bolum_a():
    k = Konfig(kol="kalib")
    print("=" * 74)
    print("A - TRAFIK  (ilan: 10 akis x 4 pkt/s x 512 B)")
    print("=" * 74)
    dogum, hiz, pencere = [], [], []
    for t in TOHUMLAR:
        tr = TrafikUreteci(k, Akislar(t))
        dogum.append(tr.toplam_dogum)
        hiz.append(tr.sunulan_hiz_hz())
        pencere.append(tr.penceredeki_dogum())
    print(f"  akis sayisi           : {k.akis_sayisi}")
    print(f"  akis basina hiz       : {k.akis_paket_hizi_hz} pkt/s")
    print(f"  paket boyutu          : {k.paket_bayt} B")
    print(f"  ILAN EDILEN toplam    : {k.sunulan_paket_hizi_hz:.1f} pkt/s")
    print(f"  OLCULEN toplam        : {ist.mean(hiz):.2f} +- "
          f"{ist.stdev(hiz):.2f} pkt/s")
    print(f"  kosu basina dogum     : {ist.mean(dogum):.0f} "
          f"(en az {min(dogum)} . en cok {max(dogum)})")
    print(f"  OLCUM PENCERESINDE    : {ist.mean(pencere):.0f} "
          f"(%{100*ist.mean(pencere)/ist.mean(dogum):.1f})")
    print(f"  pencere [{k.olcum_penceresi[0]:.0f}, "
          f"{k.olcum_penceresi[1]:.0f}) s . kosu {k.kosu_bitis_s:.0f} s")
    print()
    print("  Pencere disinda kalan paylar, sonuc satirinda AYRI sayaclarla")
    print("  raporlanir: tam kosu ve pencere ikizi ayri defterlerdir.")


def kosum(konfig, tohum, kapasite=None):
    """BOŞALTMAYAN koşum — paketler üretilir, kuyruğa girer, orada kalır.

    ⚠️ Adı önemli: bu bir "ideal aktarıcı" DEĞİLDİR, hiçbir paketi iletmez.
    Amacı `ag/` katmanının kendi geçişlerini ve taşma yolunu sınamak. MAC ve
    protokol yazılmadan gerçek bir aktarım zaten kurulamaz.
    """
    kapasite = konfig.kuyruk_kapasitesi if kapasite is None else kapasite
    trafik = TrafikUreteci(konfig, Akislar(tohum))
    defter = KorunumDefteri()
    sayac = PaketSayaci()
    kuyruklar = {n: Kuyruk(kapasite) for n in range(konfig.dugum_sayisi)}
    tasma = 0
    for dogum in trafik.cizelge:
        paket = trafik.paket_kur(dogum, sayac)
        defter.uret()
        if not kuyruklar[paket.kaynak].ekle(paket):
            defter.dus("kuyruk_tasmasi", nereden="kuyruk")
            tasma += 1
    return defter, kuyruklar, tasma


def bolum_b():
    k = Konfig(kol="kalib")
    print()
    print("=" * 74)
    print("B - KORUNUM + MUTABAKAT  (30 tohum, bosaltmayan kosum)")
    print("=" * 74)
    denklem = mutabik = 0
    for t in TOHUMLAR:
        defter, kuyruklar, _ = kosum(k, t)
        denklem += defter.kontrol()["korunum_tamam"]
        m = defter.mutabakat(
            kuyrukta_gercek=sum(len(q) for q in kuyruklar.values()),
            ucusta_gercek=0)
        mutabik += m["mutabakat_tamam"]
    print(f"  korunum denklemi tutan tohum : {denklem}/{len(TOHUMLAR)}")
    print(f"  MUTABAKAT tutan tohum        : {mutabik}/{len(TOHUMLAR)}")
    print()
    print("  🔴 Ikisi AYRI kontroldur. Denklem defterin kendi gecislerinin")
    print("  tutarliligini olcer; mutabakat defterin GERCEGI dogru")
    print("  modelleyip modellemedigini. Dolu kuyruk paketi reddedip cagiran")
    print("  `dus()` yapmayi unutursa denklem TUTAR, mutabakat KIRILIR.")


def bolum_c():
    print()
    print("=" * 74)
    print("C - KUYRUK KAPASITESI ve TASMA  (bosaltmayan kosum)")
    print("=" * 74)
    print(f"{'kapasite':>9s} {'tasma':>8s} {'tasma orani':>13s}")
    for kapasite in (1, 2, 5, 10, 50):
        k = Konfig(kol="kalib", kuyruk_kapasitesi=kapasite)
        oran, adet = [], []
        for t in range(1, 11):
            defter, _, tasma = kosum(k, t, kapasite)
            adet.append(tasma)
            oran.append(tasma / defter.uretilen)
        print(f"{kapasite:9d} {ist.mean(adet):8.1f} "
              f"{100*ist.mean(oran):12.2f}%")
    print()
    print("  Bu kosum hicbir paketi iletmez, yani tablodaki oranlar TASMA")
    print("  ORANI DEGIL: kuyrugun sonlulugunun OLCULEBILIR oldugunu")
    print("  gosterirler. Gercek tasma orani MAC ve protokol yazilinca,")
    print("  kuyruklar bosaldigi kosullarda olculecek.")


def main() -> None:
    bolum_a()
    bolum_b()
    bolum_c()


if __name__ == "__main__":
    main()
