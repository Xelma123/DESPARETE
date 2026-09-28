"""ADIM 6a KAPANIŞ — alıcı zinciri.

Üretici:  PYTHONIOENCODING=utf-8 python kalibrasyon/adim6a_kapanis.py

Kapanış ölçütü:
    🔴 Çakışan iki çerçeveden **yalnız biri** alınıyor (sıfır ihlal).
    Her başarısız alım bir **sebep** taşıyor, `Σ sebep = toplam`.

    A. Sebep dağılımı — beş sebebin de ateşlendiği görülüyor mu
    B. Çakışma denemesi — iki çerçeve, sıfır ihlal
    C. Capture effect'in ölçülen katkısı (ablasyon)
"""
from __future__ import annotations

import math
import pathlib
import random
import sys

KOK = pathlib.Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.cekirdek.rng import Akislar  # noqa: E402
from sim2.dunya.topoloji import topoloji_kur  # noqa: E402
from sim2.kanal.cerceve import cerceve_kur  # noqa: E402
from sim2.kanal.girisim import Iletim  # noqa: E402
from sim2.kanal.kanal import Kanal  # noqa: E402
from sim2.mac.alici import ALIM_SONUCLARI, AliciZinciri, sonuc_dogrula  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402
from kalibrasyon import dunya_secimi as DS  # noqa: E402  (K-183)


def kosum(senaryo="bagimsiz-yok", adim_sayisi=600, es_zamanli=3,
          tohum=1, **ek):
    """Rastgele eş zamanlı iletimler; her alıcı için sonuçları sayar."""
    k = DS.konfig(kol="kalib", senaryo=senaryo, tohum=tohum, **ek)
    kanal = Kanal(k, topoloji_kur(k, Akislar(tohum)))
    r = random.Random(90604 + tohum)
    zincirler = {n: AliciZinciri(n, k, kanal) for n in range(k.dugum_sayisi)}
    sayim = {s: 0 for s in ALIM_SONUCLARI}
    deneme = yakalama = 0

    for adim in range(adim_sayisi):
        t0 = 20.0 + 0.05 * adim
        a = kanal.topoloji.anlik(t0)
        adaylar = [n for n in range(k.dugum_sayisi) if a.komsular[n]]
        if len(adaylar) < 2:
            continue
        kanal.ortam.bitenleri_at(t0)
        iletimler = []
        for sira, g in enumerate(r.sample(adaylar,
                                          min(es_zamanli, len(adaylar)))):
            it = Iletim(gonderen=g, cerceve=cerceve_kur(k, "veri"),
                        baslangic_s=t0 + sira * 0.0004,
                        guc_w=kanal.yayilim.verici_gucu_w)
            kanal.ortam.ekle(it)
            iletimler.append(it)
        for it in iletimler:
            for alici in a.komsular[it.gonderen]:
                deneme += 1
                yeni, ezilen = zincirler[alici].cerceve_geldi(
                    it, it.baslangic_s)
                for s in (yeni, ezilen):
                    if s:
                        sayim[s.sebep] += 1
                        yakalama += s.yakalama
        for it in iletimler:
            for alici in a.komsular[it.gonderen]:
                s = zincirler[alici].cerceve_bitti(it, it.bitis_s)
                if s:
                    sayim[s.sebep] += 1
    return sayim, deneme, yakalama


def bolum_a():
    print("=" * 76)
    print("A - SEBEP DAGILIMI  (bes sebebin de atesledigi gorunuyor mu)")
    print("=" * 76)
    print(f"{'senaryo':22s}" + "".join(f"{s.replace('alim_', ''):>14s}"
                                       for s in ALIM_SONUCLARI))
    for senaryo, ek in (("statik-yok", {}), ("bagimsiz-yok", {}),
                        ("gorev-yok", {})):
        sayim, deneme, _ = kosum(senaryo, **ek)
        sonuc_dogrula(sayim, deneme)
        satir = "".join(f"{100*sayim[s]/deneme:13.1f}%" for s in ALIM_SONUCLARI)
        print(f"{senaryo:22s}{satir}")
    print()
    print("  Her satirda `Σ sebep = toplam deneme` denetlendi (sonuc_dogrula).")
    print("  `alim_red_yari_cift` bu kosumda 0: bu kosum GONDERIM yapmiyor,")
    print("  yarim ciftlik ancak DCF baglaninca (Adim 6b) atesler.")


def bolum_b():
    print()
    print("=" * 76)
    print("B - CAKISMA  (iki cerceve ayni alicida, kac kez IKISI DE alindi)")
    print("=" * 76)
    for yakalama_acik in (False, True):
        k = DS.konfig(kol="kalib", senaryo="statik-yok",
                   golgeleme_acik=False, sonumleme_acik=False,
                   yakalama_etkisi_acik=yakalama_acik)
        kanal = Kanal(k, topoloji_kur(k, Akislar(1)))
        a = kanal.topoloji.anlik(0.0)
        ucluler = [(i, j, m) for i, ks in enumerate(a.komsular) for j in ks
                   for m in a.komsular[j] if m not in (i, j)][:40]
        ihlal = toplam = 0
        for n, (i, j, m) in enumerate(ucluler):
            for kayma in (0.1, 0.3, 0.6, 0.9):
                z = AliciZinciri(j, k, kanal)
                t0 = 10.0 + 0.02 * (n * 4 + int(kayma * 10))
                ilk = Iletim(gonderen=i, cerceve=cerceve_kur(k, "veri"),
                             baslangic_s=t0,
                             guc_w=kanal.yayilim.verici_gucu_w)
                ikinci = Iletim(gonderen=m, cerceve=cerceve_kur(k, "veri"),
                                baslangic_s=t0 + kayma * ilk.cerceve.sure_s,
                                guc_w=kanal.yayilim.verici_gucu_w)
                kanal.ortam.ekle(ilk)
                kanal.ortam.ekle(ikinci)
                sonuclar = []
                for it in (ilk, ikinci):
                    yeni, ezilen = z.cerceve_geldi(it, it.baslangic_s)
                    sonuclar += [x for x in (yeni, ezilen) if x]
                for it in (ilk, ikinci):
                    s = z.cerceve_bitti(it, it.bitis_s)
                    if s:
                        sonuclar.append(s)
                toplam += 1
                if sum(s.basarili for s in sonuclar) > 1:
                    ihlal += 1
                kanal.ortam.bitenleri_at(1e9)
        etiket = "acik" if yakalama_acik else "kapali"
        print(f"  yakalama {etiket:7s} : {toplam} cakisma . "
              f"IKISI DE alinan: {ihlal}")
    print()
    print("  🔒 Eski simulatorde her alim BAGIMSIZ bir PER cekimiydi ve")
    print("  ikisi de basarili olabiliyordu. Burada yapisal olarak imkansiz.")


def bolum_c():
    """🔴 Bu bolum IKI KEZ yanlis olcuyordu ve ikisi de kosumun kendi hatasiydi.

      1. Cerceveler 400 us arayla baslatiliyordu, yakalama penceresi 192 us:
         yakalama dali HIC kosmuyordu.
      2. Duzeltildikten sonra da sifir cikti — bu kez ucluler rastgele
         seciliyordu ve guc farki 10 dB esigini asmiyordu.

    Dogru soru sudur: yakalama NE SIKLIKTA MUMKUN? Iki kosul birden gerekir —
    ikinci cerceve pencerede gelmeli VE guc farki esigi asmali. Asagida once
    guc farki dagilimi olculuyor, sonra ablasyon yalniz MUMKUN oldugu
    uclulerde kosuluyor.
    """
    print()
    print("=" * 76)
    print("C - CAPTURE EFFECT  (once: ne siklikta MUMKUN)")
    print("=" * 76)
    k0 = DS.konfig(kol="kalib", senaryo="statik-yok", golgeleme_acik=False,
                sonumleme_acik=False)
    kanal0 = Kanal(k0, topoloji_kur(k0, Akislar(1)))
    cerceve_s = cerceve_kur(k0, "veri").sure_s
    pencere_payi = k0.yakalama_penceresi_s / cerceve_s

    # Guc farki dagilimi: ayni aliciya menzil ici iki gonderen
    farklar = []
    guclu_ucluler = []
    for tohum in range(1, 11):
        kn = Kanal(DS.konfig(kol="k", senaryo="statik-yok", tohum=tohum,
                          golgeleme_acik=False, sonumleme_acik=False),
                   topoloji_kur(DS.konfig(kol="k", senaryo="statik-yok",
                                       tohum=tohum), Akislar(tohum)))
        a = kn.topoloji.anlik(0.0)
        for j in range(kn.konfig.dugum_sayisi):
            komsular = a.komsular[j]
            for x in range(len(komsular)):
                for y in range(x + 1, len(komsular)):
                    i, m = komsular[x], komsular[y]
                    pi = kn.girisim.sinyal_w(i, j, 0.0)
                    pm = kn.girisim.sinyal_w(m, j, 0.0)
                    fark = abs(10.0 * math.log10(pi / pm))
                    farklar.append(fark)
                    if fark >= k0.yakalama_esigi_db and tohum == 1:
                        guclu_ucluler.append((i, j, m) if pi > pm else (m, j, i))
    farklar.sort()
    asan = sum(f >= k0.yakalama_esigi_db for f in farklar) / len(farklar)
    print(f"  menzil ici gonderen cifti      : {len(farklar)}")
    print(f"  guc farki ortanca              : {farklar[len(farklar)//2]:.1f} dB")
    print(f"  guc farki p90                  : {farklar[int(.9*len(farklar))]:.1f} dB")
    print(f"  esigi ({k0.yakalama_esigi_db:.0f} dB) ASAN cift oranı   : %{100*asan:.1f}")
    print(f"  pencere payi ({k0.yakalama_penceresi_s*1e6:.0f}/{cerceve_s*1e6:.0f} us)"
          f"        : %{100*pencere_payi:.1f}")
    print(f"  IKISI BIRDEN (kaba tahmin)     : %{100*asan*pencere_payi:.1f}")
    print()
    print("  🔒 Yani yakalama, carpismalarin ancak kucuk bir kisminda")
    print("  devreye girer — ama sifir degildir ve kapali birakmak agin")
    print("  tasima kapasitesini sistematik olarak DUSUK olcerdi.")

    print()
    print("  ABLASYON — yalniz yakalamanin MUMKUN oldugu uclulerde:")
    print(f"{'yakalama':>10s} {'deneme':>8s} {'YAKALAMA':>10s} "
          f"{'basarili':>10s} {'ikisi de':>10s}")
    for acik in (False, True):
        k = DS.konfig(kol="kalib", senaryo="statik-yok", golgeleme_acik=False,
                   sonumleme_acik=False, yakalama_etkisi_acik=acik)
        kanal = Kanal(k, topoloji_kur(k, Akislar(1)))
        r = random.Random(6060)
        deneme = yakalanan = basarili = ihlal = 0
        for n, (guclu, j, zayif) in enumerate(guclu_ucluler[:40]):
            for tekrar in range(15):
                z = AliciZinciri(j, k, kanal)
                t0 = 10.0 + 0.02 * (n * 15 + tekrar)
                # zayif once baslar, guclu PENCERE ICINDE gelir
                gecikme = r.uniform(0.0, k.yakalama_penceresi_s)
                ilk = Iletim(gonderen=zayif, cerceve=cerceve_kur(k, "veri"),
                             baslangic_s=t0,
                             guc_w=kanal.yayilim.verici_gucu_w)
                ikinci = Iletim(gonderen=guclu, cerceve=cerceve_kur(k, "veri"),
                                baslangic_s=t0 + gecikme,
                                guc_w=kanal.yayilim.verici_gucu_w)
                kanal.ortam.ekle(ilk)
                kanal.ortam.ekle(ikinci)
                deneme += 1
                sonuclar = []
                for it in (ilk, ikinci):
                    yeni, ezilen = z.cerceve_geldi(it, it.baslangic_s)
                    sonuclar += [x for x in (yeni, ezilen) if x]
                for it in (ilk, ikinci):
                    sn = z.cerceve_bitti(it, it.bitis_s)
                    if sn:
                        sonuclar.append(sn)
                yakalanan += sum(x.yakalama for x in sonuclar)
                basarili += sum(x.basarili for x in sonuclar)
                ihlal += sum(x.basarili for x in sonuclar) > 1
                kanal.ortam.bitenleri_at(1e9)
        print(f"{str(acik):>10s} {deneme:8d} {yakalanan:10d} "
              f"{basarili:10d} {ihlal:10d}")
    print()
    print("  Kapaliyken guclu cerceve zayifin arkasinda sirada bekler ve")
    print("  KAYBEDILIR; acikken onu ezip alinir. Fark 'basarili' sutununda.")


def main() -> None:
    bolum_a()
    bolum_b()
    bolum_c()


if __name__ == "__main__":
    main()
