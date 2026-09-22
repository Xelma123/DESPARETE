"""ADIM 4 KAPANIŞ — kanalın uçtan uca davranışı.

Üretici:  PYTHONIOENCODING=utf-8 python kalibrasyon/adim4_kapanis.py

Yol haritasının yedi kapanış ölçütü testlerde bağlı. Bu betik, testlerin
göstermediği şeyi gösterir: kanal **birlikte** nasıl davranıyor.

    A. PER–mesafe eğrisi ve her katmanın katkısı (ablasyon)
    B. Karıştırıcı sınıflarının etkisi, aynı güçte
    C. Maliyet — çerçeve başına ve koşu başına
"""
from __future__ import annotations

import math
import pathlib
import statistics as ist
import sys
import time

KOK = pathlib.Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.cekirdek.rng import Akislar  # noqa: E402
from sim2.dunya.geometri import Nokta3, mesafe  # noqa: E402
from sim2.dunya.topoloji import topoloji_kur  # noqa: E402
from sim2.kanal.cerceve import cerceve_kur  # noqa: E402
from sim2.kanal.girisim import Iletim  # noqa: E402
from sim2.kanal.kanal import Kanal  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402

TOHUMLAR = range(1, 21)


def _kanal(senaryo="statik-yok", **ek):
    k = Konfig(kol="kalib", senaryo=senaryo, **ek)
    return Kanal(k, topoloji_kur(k, Akislar(1)))


def ortalama_per_mesafede(kanal, d_m, ornek=200):
    """Verilen mesafede PER — gölgeleme/sönümleme üzerinden ortalanır."""
    c = cerceve_kur(kanal.konfig, "veri")
    degerler = []
    for n in range(ornek):
        # Bağ kimliğini değiştirerek gölgeleme alanını örnekle
        i, j = n % 39, (n % 39) + 1
        a = Nokta3(100.0, 100.0 + 3.0 * n, 70.0)
        b = Nokta3(100.0 + d_m, 100.0 + 3.0 * n, 70.0)
        yavas = kanal.yayilim.yavas_alinan_w(i, j, a, b)
        degerler.append(kanal.kahin_per(c, yavas / kanal.yayilim.gurultu_w))
    return ist.mean(degerler)


def bolum_a():
    print("=" * 76)
    print("A - PER-MESAFE ve ABLASYON  (kahin PER, girisimsiz)")
    print("=" * 76)
    kurulumlar = (
        ("cip lak yol kaybi", dict(golgeleme_acik=False, anten_deseni_acik=False)),
        ("+ anten deseni", dict(golgeleme_acik=False, anten_deseni_acik=True)),
        ("+ golgeleme", dict(golgeleme_acik=True, anten_deseni_acik=True)),
    )
    mesafeler = (100.0, 180.0, 240.0, 280.0, 320.0, 400.0)
    print(f"{'kurulum':22s}" + "".join(f"{d:>9.0f}m" for d in mesafeler))
    for ad, ek in kurulumlar:
        kanal = _kanal(**ek)
        satir = "".join(f"{ortalama_per_mesafede(kanal, d):>10.3f}"
                        for d in mesafeler)
        print(f"{ad:22s}{satir}")
    print()
    # ⚠️ ETIKET KONFIGDEN OKUNUR. Elle yazilmis "10 dB" burada duruyordu ve
    # esik 16 dB olunca sessizce yanlislasti — `03` B5, "etiketi elle tasima".
    kfg = Konfig(kol="kalib")
    print(f"  Not: menzil {kfg.iletim_menzili_m:.0f} m, orada girisimsiz "
          f"SINR tam olarak esik ({kfg.sinr_esigi_db:.0f} dB); "
          f"yol kaybi usteli {kfg.yol_kaybi_usteli:.1f}.")
    print("  Yatay bagda anten kaybi sifirdir; egriyi golgeleme yayar.")


def bolum_b():
    print()
    print("=" * 76)
    print("B - KARISTIRICI SINIFLARI  (ayni tepe guc, gercek topoloji)")
    print("=" * 76)
    temiz = _kanal(golgeleme_acik=False, sonumleme_acik=False)
    a = temiz.topoloji.anlik(0.0)
    # Karistiriciya en yakin baglardan biri secilir: etkinin gorunecegi yer
    merkez = Nokta3(500.0, 500.0, 70.0)
    en_iyi = None
    for i, komsular in enumerate(a.komsular):
        for j in komsular:
            d = mesafe(a.konumlar[j], merkez)
            if en_iyi is None or d < en_iyi[0]:
                en_iyi = (d, i, j)
    _, i, j = en_iyi
    c = cerceve_kur(temiz.konfig, "veri")
    print(f"  bag {i}->{j} . alicinin karistiriciya uzakligi "
          f"{mesafe(a.konumlar[j], merkez):.0f} m")
    # 🔴 ÖRNEKLEME ANI KONFİGDEN TÜRER — elle 10,0 s yazılmıştı ve
    # `karistirici_baslangic_s = 150 s` eklenince bu tablo SESSİZCE
    # BOŞALDI: `devrede_mi(10,0)` yanlış, `alinan_guc_w` sıfır, yani beş
    # sınıfın beşi de KAPALI bir karıştırıcıyla ölçülüyordu. Ölçüldü —
    # dört sınıfın dördü de PER 0,0000 (temiz tabanla aynı) veriyordu;
    # `acik_mi` sütunu ise SINIF zamanlamasını gösterdiği için tablo canlı
    # görünüyordu. Aynı kurulum t = 160 s'de PER 1,0000 veriyor.
    # Üretici: `python kalibrasyon/adim4_kapanis.py`
    bas = temiz.konfig.karistirici_baslangic_s + 10.0
    print(f"  ornekleme ani {bas:.1f} s "
          f"(karistirici_baslangic_s = "
          f"{temiz.konfig.karistirici_baslangic_s:.1f} s)")
    print(f"{'sinif':18s} {'PER':>8s} {'gorev cevrimi':>15s}")
    taban = temiz.alim_per(i, j, c, bas_s=bas)
    print(f"{'yok':18s} {taban:8.4f} {'-':>15s}")
    for sinif in ("surekli", "reaktif", "aldatici", "taramali"):
        kanal = _kanal(f"statik-{sinif}", karistirici_guc_override_dbm=15.0,
                       golgeleme_acik=False, sonumleme_acik=False)
        if sinif == "reaktif":
            kanal.ortam.ekle(Iletim(gonderen=i, cerceve=c, baslangic_s=bas,
                                    guc_w=kanal.yayilim.verici_gucu_w))
        n = 400
        cevrim = sum(kanal.karistirici.acik_mi(bas + c.sure_s * m / n)
                     for m in range(n)) / n
        per = kanal.alim_per(i, j, c, bas_s=bas)
        print(f"{sinif:18s} {per:8.4f} {100*cevrim:14.1f}%")
    print()
    print("  Taramali dusuk cikiyorsa o an baska konaktadir — tasarim geregi.")


def bolum_c():
    print()
    print("=" * 76)
    print("C - MALIYET")
    print("=" * 76)
    kanal = _kanal("bagimsiz-yok")
    c = cerceve_kur(kanal.konfig, "veri")
    a = kanal.topoloji.anlik(0.0)
    ciftler = [(i, ks[0]) for i, ks in enumerate(a.komsular) if ks][:20]

    # girisimli en kotu hal: 3 es zamanli iletim
    for n, (gi, _) in enumerate(ciftler[:3]):
        kanal.ortam.ekle(Iletim(gonderen=gi, cerceve=c,
                                baslangic_s=10.0 - 0.0003 * n,
                                guc_w=kanal.yayilim.verici_gucu_w))
    t0 = time.perf_counter()
    adet = 0
    for tur in range(200):
        for i, j in ciftler:
            kanal.alim_per(i, j, c, bas_s=10.0 + 0.01 * tur)
            adet += 1
    sure = time.perf_counter() - t0
    print(f"  parca/cerceve (girisimli) : "
          f"{len(kanal.girisim.parca_sinirlari(10.0, c.sure_s)) - 1}")
    print(f"  alim_per                  : {sure/adet*1e6:8.1f} us/cerceve")
    print(f"  42 000 cerceve            : {42000*sure/adet:8.1f} s/kosu")
    print()
    print("  Risk 1'in esigi: sonumleme maliyeti kosunun %15'ini asarsa memo")
    print("  zorunlu. Memo zaten yerinde; pay bu olcumde esigin altinda.")


def bolum_d():
    """PER geçiş bandı ↔ gölgeleme σ — `golgeleme_sigma_db`nin ÜRETİCİSİ.

    🔴 NEDEN BURADA. Bu ölçüm `adim3_oncesi.py`de yapılmıştı ve o betik
    TERK EDİLMİŞ bir çalışma noktasında koşuyor (yol kaybı üsteli 3,0,
    SINR eşiği 10 dB). Yani `golgeleme_sigma_db` `OLCULMUS` kovasındaydı
    ama üreticisi bugünkü fiziği hesaplamıyordu — sayıyı doğrulamak için
    onu koşturan biri başka bir cevap alırdı. Mimari denetimi D15 bunu
    9 Eylül 2026'da yakaladı.

    🔒 İDDİA: PER'in 0,99'dan 0,01'e düştüğü geçiş bandı, gölgeleme σ'sıyla
    AYNI MERTEBEDE. Yani "menzil" sert bir daire değil; σ kadarlık bir
    gölgeleme, bağı tamamen açıp kapatmaya yeter. σ = 3 dB seçimi buradan
    gerekçelenir: daha küçük bir σ bağları gerçeğe göre keskin yapardı.

    ⚠️ Gölgeleme ve sönümleme KAPALI ölçülür — ölçülen şey PER eğrisinin
    kendi dikliği; ikisi açıkken eğri zaten onlarla bulanıklaşır.
    """
    print()
    print("=" * 76)
    print("D - PER GECIS BANDI  (`golgeleme_sigma_db`nin ureticisi)")
    print("=" * 76)
    kanal = _kanal(golgeleme_acik=False, sonumleme_acik=False)
    kfg = kanal.konfig
    c = cerceve_kur(kfg, "veri")
    alt = ust = None
    x = -10.0
    while x < 50.0:
        per = kanal.kahin_per(c, 10.0 ** (x / 10.0))
        if alt is None and per <= 0.99:
            alt = x
        if per <= 0.01:
            ust = x
            break
        x += 0.01
    bant = ust - alt
    sigma = kfg.golgeleme_sigma_db
    print(f"  yol kaybi usteli {kfg.yol_kaybi_usteli:.1f} · "
          f"SINR esigi {kfg.sinr_esigi_db:.0f} dB")
    print(f"  PER 0,99 -> 0,01 gecis bandi : {bant:.2f} dB "
          f"({alt:.2f} -> {ust:.2f} dB)")
    print(f"  golgeleme sigma              : {sigma:.2f} dB")
    print(f"  bant / sigma                 : {bant / sigma:.2f}")
    print()
    if 0.5 <= bant / sigma <= 2.0:
        print("  🟢 IDDIA AYAKTA: gecis bandi sigma ile ayni mertebede.")
        print("     'Menzil' sert bir daire degil; sigma kadarlik bir")
        print("     golgeleme bagi tamamen acip kapatmaya yeter.")
    else:
        print("  🔴 IDDIA COKTU: bant ile sigma ayni mertebede degil.")
        print("     `golgeleme_sigma_db`nin gerekcesi yeniden bakilmali.")
    print()
    print("  ⚠️ ESKI OLCUM (terk edilmis calisma noktasi, alfa=3, esik=10 dB):")
    print("     bant 3,02 dB. Bugunku fizikte yeniden olculdu.")


def bolum_e():
    """Sönümleme örnek sayısı K — `SONUMLEME_ORNEGI`nin ÜRETİCİSİ.

    🔒 İDDİA (modül başlıklarında): donuk kolda sönümleme dondurulmuştur,
    dolayısıyla K sonucu DEĞİŞTİREMEZ; hareketli kolda doğru büyüklük
    ORTALAMADIR ve K = 6 yeterlidir.

    🔴 Bu iddia `OLCULMUS` diye etiketlenmişti ama ÜRETİCİSİ YOKTU — bir
    test (`test_OLCULMUS_kova_URETICI_gostermek_zorunda`) 9 Eylül 2026'da
    yakaladı. Üretici burada.
    """
    print()
    print("=" * 76)
    print("E - SONUMLEME ORNEK SAYISI K  (`SONUMLEME_ORNEGI`nin ureticisi)")
    print("=" * 76)
    from sim2.kosum.kurulum import kurulum_yap
    from kalibrasyon.kahin import KanalGrafigi
    for senaryo in ("statik-yok", "bagimsiz-yok"):
        kfg = Konfig(kol="kalib", senaryo=senaryo, tohum=1000)
        print(f"  --- {senaryo}  (donuk = {not kfg.hareketli})")
        dereceler = {}
        for K in (1, 2, 6, 16, 48):
            grafik = KanalGrafigi(kurulum_yap(kfg))
            grafik._ornek = K
            dereceler[K] = grafik.ozet(200.0)["derece"]
            print(f"      K={K:2d}   ortalama derece = {dereceler[K]:.6f}")
        yayilim = max(dereceler.values()) - min(dereceler.values())
        if yayilim == 0.0:
            print("      🟢 K SONUCU DEGISTIRMIYOR — dondurulmus sonumleme.")
            print("         Tek ornek yeterli; fazlasi ayni sayiyi tekrar")
            print("         hesaplamaktan ibaret.")
        else:
            altisi = dereceler[6]
            son = dereceler[48]
            print(f"      🔴 K SONUCU DEGISTIRIYOR — yayilim {yayilim:.4f}")
            print(f"         K=6 ile K=48 arasi fark: "
                  f"{abs(son - altisi):.4f} ({abs(son - altisi) / son:.1%})")
            print("         Yani K = 6 YAKINSAMAMIS. Deger secilmis, "
                  "turetilmemis.")


def main() -> None:
    bolum_a()
    bolum_b()
    bolum_c()
    bolum_d()
    bolum_e()


if __name__ == "__main__":
    main()
