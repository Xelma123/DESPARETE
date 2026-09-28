"""ADIM 3 KAPANIŞ ÖLÇÜTÜ.

Üretici:  PYTHONIOENCODING=utf-8 python kalibrasyon/adim3_kapanis.py

Kapanış ölçütü (yol haritası, Adım 3):
    "1000×1000×120 · R=280'de ort. derece ve bağlı oran raporlanmış.
     Hareket boyunca bağlantılılık zaman serisi ölçülmüş."

🔴 KAPI KURALI ÖLÇÜMLE DEĞİŞTİRİLDİ (4 Eylül 2026, danışmana devredilmiş
karar). Yol haritası "30 tohum" diyordu. Ölçüldü: bağlı oranın 30 tohumdaki
standart hatası ±8,4 puan — aynı kurulum 30 tohumda %70,0, 120 tohumda %69,2,
500 tohumda %77,4 veriyor. Derece 30 tohumda yeterli (±0,17), bağlı oran
DEĞİL. Bu yüzden derece 30 tohumla, bağlı oran 500 tohumla raporlanır.
Maliyeti saniyelerle ölçülür.

🔴 BU BETİK 9 EYLÜL 2026'YA KADAR **KOŞMUYORDU** — ve sayıları kullanılıyordu
=============================================================================
Bölüm 3 ve 4, mobilite kolunun ESKİ adını (`mobil-yok`) kullanıyordu. Üçüncü
kol eklenirken (4 Eylül, `senaryolar.py`) kollar `statik · bagimsiz · gorev`
diye yeniden adlandırıldı ve bu betik güncellenmedi. `Konfig` bilinmeyen bir
senaryoyu reddettiği için bölüm 3 **ilk çağrıda `ValueError` ile patlıyordu**.

🔴 Yani bu betiğin ürettiği bağlantılılık sayıları o tarihten beri **yeniden
üretilemiyordu** — ve `sim2/` içinde DÖRT yerde "üretici" olarak gösteriliyor
(`dunya/mobilite.py` · `dunya/topoloji.py` · `dunya/yerlesim.py` ·
`yapilandirma/senaryolar.py`). Dördünde de tablo hâlâ ESKİ kol adıyla yazılı;
yani sayılar da o tarihten kalma, yani **terk edilmiş bir çalışma
noktasından** (alan 1000 m · yol kaybı üsteli 3 · SINR eşiği 10 dB).

⚠️ VE ÖLÇTÜĞÜ GRAFİK ZATEN ÇÜRÜTÜLMÜŞTÜ. Buradaki graf `Topoloji.anlik`ten
gelir, yani `iletim_menzili_m` (280 m) yarıçaplı SERT DİSKTİR. K-096 tam da
o diskin veri yolunda hiçbir yeri kapamadığını ölçtü: kimin duyacağını
girişim menzili, alınıp alınmadığını SINR belirliyor. Alan 1800 m'ye çıkınca
o diskin derecesi 2,57'ye indi.

🔒 BU BETİĞİN SAYILARI ARTIK BİR TEŞHİSTİR, BİR ÖLÇÜM DEĞİL. Onarıldı
(kol adı düzeltildi) ve koşuyor; ama sonuç satırlarına `TESHIS GRAFIGI`
etiketi eklendi. Bağlantılılığın KARAR TAŞIYAN ölçümü kanal grafiğinde
yapılır: `kalibrasyon/bag_kumesi.py`.
"""
from __future__ import annotations

import pathlib
import statistics as ist
import sys
import time

KOK = pathlib.Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.cekirdek.rng import Akislar  # noqa: E402
from sim2.dunya.topoloji import Topoloji, topoloji_kur  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402
from kalibrasyon import dunya_secimi as DS  # noqa: E402  (K-183)

TOHUM_AZ = range(1, 31)     # derece için yeter
TOHUM_COK = range(1, 501)   # bağlı oran için gerekir


def _konfig(senaryo: str, tohum: int, **ek) -> Konfig:
    return DS.konfig(kol="kalibrasyon", senaryo=senaryo, tohum=tohum, **ek)


def _topoloji(senaryo: str, tohum: int, **ek) -> Topoloji:
    return topoloji_kur(_konfig(senaryo, tohum, **ek), Akislar(tohum))


# ==========================================================================
def baslangic_grafi(tohumlar, **ek):
    """t = 0 anındaki geometrik graf — çalışma noktası budur."""
    dereceler, bagli, en_buyuk = [], 0, []
    for t in tohumlar:
        a = _topoloji("statik-yok", t, **ek).anlik(0.0)
        dereceler.append(a.ortalama_derece)
        bagli += a.bagli_mi
        en_buyuk.append(a.en_buyuk_bilesen)
    n = len(tohumlar)
    p = bagli / n
    return dict(
        tohum=n,
        derece=ist.mean(dereceler),
        derece_se=ist.stdev(dereceler) / n ** 0.5,
        bagli=p,
        bagli_se=(p * (1 - p) / n) ** 0.5,
        en_buyuk=ist.mean(en_buyuk),
    )


def zaman_serisi_ozeti(senaryo: str, tohumlar, adim_s: float,
                       bitis_s: float = 350.0):
    ozetler, olaylar = [], []
    for t in tohumlar:
        top = _topoloji(senaryo, t)
        seri = top.zaman_serisi(0.0, bitis_s, adim_s)
        ozetler.append(Topoloji.baglantililik_ozeti(seri))
        olaylar.append(Topoloji.bag_olaylari(seri))
    return dict(
        tohum=len(tohumlar),
        adim_s=adim_s,
        tam_bagli=ist.mean(o["tam_bagli_zaman_orani"] for o in ozetler),
        tam_bagli_en_kotu=min(o["tam_bagli_zaman_orani"] for o in ozetler),
        derece=ist.mean(o["ortalama_derece"] for o in ozetler),
        en_kucuk_bilesen=min(o["en_kucuk_en_buyuk_bilesen"] for o in ozetler),
        kapanan=ist.mean(o["kapanan"] for o in olaylar),
        acilan=ist.mean(o["acilan"] for o in olaylar),
    )


# ==========================================================================
def main() -> None:
    baslangic = time.perf_counter()

    print("=" * 74)
    print("1 - CALISMA NOKTASI  (t = 0, statik-yok, irtifa 20-120 m)")
    print("    ⚠️ TESHIS GRAFIGI — 280 m sert disk. K-096: bu disk veri")
    print("       yolunda hicbir yeri kapamaz. Karar tasiyan baglantililik")
    print("       olcumu KANAL grafiginde: kalibrasyon/bag_kumesi.py")
    print("=" * 74)
    az = baslangic_grafi(TOHUM_AZ)
    cok = baslangic_grafi(TOHUM_COK)
    for ad, s in (("30 tohum", az), ("500 tohum", cok)):
        print(f"  {ad:10s} derece {s['derece']:.3f}+-{s['derece_se']:.3f}"
              f"  .  bagli %{100 * s['bagli']:.1f}+-{100 * s['bagli_se']:.1f}"
              f"  .  en buyuk bilesen {s['en_buyuk']:.2f}/40")
    print("  KAPI: derece 30 tohumla, bagli oran 500 tohumla raporlanir.")
    print("        30 tohumda bagli oranin standart hatasi +-"
          f"{100 * az['bagli_se']:.1f} puan — kapiyi tasiyamaz.")

    print()
    print("=" * 74)
    print("2 - IRTIFA TABANI KARARININ BEDELI")
    print("=" * 74)
    for zmin in (0.0, 20.0):
        s = baslangic_grafi(TOHUM_COK, irtifa_min_m=zmin)
        print(f"  irtifa {zmin:5.1f}-120 m : derece {s['derece']:.3f}"
              f"+-{s['derece_se']:.3f} . bagli %{100 * s['bagli']:.1f}"
              f"+-{100 * s['bagli_se']:.1f}")
    print("  Fark her iki olcumde de ~1 standart hata: bedelsiz.")

    print()
    print("=" * 74)
    print("3 - HAREKET BOYUNCA BAGLANTILILIK  (30 tohum x 350 s)")
    print("    ⚠️ TESHIS GRAFIGI (280 m sert disk) — bkz. modul basligi.")
    print("    🔴 Bu bolum 9 Eylul 2026'ya kadar ESKI kol adiyla PATLIYORDU.")
    print("=" * 74)
    for senaryo in ("statik-yok", "bagimsiz-yok"):
        s = zaman_serisi_ozeti(senaryo, TOHUM_AZ, adim_s=1.0)
        print(f"  {senaryo:12s} tam bagli zaman orani %{100 * s['tam_bagli']:.1f}"
              f"  (en kotu tohum %{100 * s['tam_bagli_en_kotu']:.1f})")
        print(f"  {'':12s} ort. derece {s['derece']:.3f}"
              f" . en kucuk 'en buyuk bilesen' {s['en_kucuk_bilesen']:.0f}/40")
        print(f"  {'':12s} bag olayi: {s['kapanan']:.1f} kapanan"
              f" . {s['acilan']:.1f} acilan  (adim 1,0 s)")
    print("  🔴 Hareketli kolda ag zamanin bir kismi BOLUNMUS —")
    print("     yani PDR = 1 tanim geregi imkansiz. U1 statik kolda kosar.")

    print()
    print("=" * 74)
    print("4 - BAG OLAYI SAYIMI ORNEKLEME ADIMINA BAGLI  (5 tohum)")
    print("    ⚠️ TESHIS GRAFIGI (280 m sert disk).")
    print("=" * 74)
    print("  Adimdan kisa suren kopma sayimda gorunmez. Bu sayinin bir")
    print("  OZELLIGIDIR, hatasi degil — raporlanirken adim da yazilir.")
    for adim in (2.0, 1.0, 0.5):
        s = zaman_serisi_ozeti("bagimsiz-yok", range(1, 6), adim_s=adim)
        print(f"  adim {adim:4.1f} s -> {s['kapanan']:7.1f} kapanan"
              f" . {s['acilan']:7.1f} acilan"
              f" . tam bagli %{100 * s['tam_bagli']:.1f}")

    print()
    print(f"toplam sure: {time.perf_counter() - baslangic:.1f} sn")


if __name__ == "__main__":
    main()
