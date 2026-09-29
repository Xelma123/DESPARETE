"""
BAĞ KALİTESİ — "menzil" dediğimiz mesafede bir çerçeve gerçekten geçiyor mu?

🔴 NEDEN BU ÖLÇÜM VAR
=====================
5 Eylül 2026: kâhin (mükemmel) yönlendirmeyle, KARIŞTIRICI YOKKEN, 2 akışlık
çok hafif yükte bile PDR %50 ve PSR %17 çıktı. Yani sorun ne yönlendirmede
ne çekişmede — **bağın kendisinde**.

Şüphe: `iletim_menzili_m`, "alınan güç = gürültü × SINR eşiği" olacak şekilde
tanımlı. Eşik 10 dB. Ama 10 dB SINR'de DQPSK ile 4096 bitlik bir gövdenin
hata olasılığı %75 civarındadır (Adım 4'te ölçülmüştü). Yani topolojinin
"bağ" dediği şey, fizik açısından **çoğunlukla geçmeyen** bir bağ.

Bu bir kod hatası DEĞİL, bir ÇALIŞMA NOKTASI seçimidir; ve seçimi öğrenci
yapar. Bu dosya seçeneği fiyatlandırır.

⚠️ LİTERATÜRDE BİLİNEN BİR OLGU
===============================
Atlama sayısına göre yönlendiren protokoller (AODV dâhil) en UZUN atlamayı
seçer, çünkü en az atlama odur; en uzun atlama da en kötü bağdır. ETX
metriği (De Couto ve ark., 2003) tam olarak bunun için icat edildi. Yani
düşük PDR gerçekçi bir davranıştır — ama öğrencinin beyanı şu: *"saldırı
yokken %95–100 olmalı."* İkisini uzlaştıran şey çalışma noktasıdır.
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.dunya.geometri import Nokta3  # noqa: E402
from sim2.kanal.cerceve import cerceve_kur  # noqa: E402
from sim2.kanal.kanal import Kanal, ber_dqpsk  # noqa: E402
from sim2.dunya.topoloji import topoloji_kur  # noqa: E402
from sim2.cekirdek.rng import Akislar  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402
from kalibrasyon import dunya_secimi as DS  # noqa: E402  (K-183)


def _kanal(konfig):
    return Kanal(konfig, topoloji_kur(konfig, Akislar(konfig.tohum)))


def per_mesafeye_gore(konfig, mesafeler):
    """Gölgeleme/sönümleme OLMADAN, saf yol kaybıyla PER.

    🔒 Ortalama davranışı görmek için: gölgeleme ve sönümleme bağa göre
    değişir ve tek bir sayı vermez. Buradaki eğri "tipik" bağdır.
    """
    k = _kanal(konfig)
    veri = cerceve_kur(konfig, "veri")
    onay = cerceve_kur(konfig, "onay")
    cikti = []
    for d in mesafeler:
        # saf yol kaybı + iki uç dipol (yatay bağ → kayıp ~0)
        kayip_db = k.yayilim.yol_kaybi_db(d)
        pr = k.yayilim.verici_gucu_w / (10.0 ** (kayip_db / 10.0))
        sinr = pr / k.yayilim.gurultu_w
        cikti.append((d, 10.0 * math.log10(sinr),
                      k.kahin_per(veri, sinr), k.kahin_per(onay, sinr)))
    return cikti


def basari_olasiligi(per_veri, per_onay, deneme_siniri):
    """Bir paket-atlamanın başarı olasılığı — yeniden denemeler dâhil.

    Bir denemenin başarısı: veri geçecek VE onay geri gelecek.
    """
    tek = (1.0 - per_veri) * (1.0 - per_onay)
    return 1.0 - (1.0 - tek) ** (deneme_siniri + 1)


def bolum(b):
    print("\n" + "=" * 78)
    print(b)
    print("=" * 78)


if __name__ == "__main__":
    k0 = DS.konfig(kol="kalib")
    menzil = k0.iletim_menzili_m
    print(f"varsayilan: sinr_esigi_db={k0.sinr_esigi_db}  "
          f"iletim_menzili_m={menzil}  paket_bayt={k0.paket_bayt}  "
          f"yeniden_deneme_siniri={k0.yeniden_deneme_siniri}")

    bolum("1 - PER MESAFEYE GORE  (varsayilan calisma noktasi)")
    print(f"  {'mesafe_m':>9} {'sinr_db':>8} {'per_veri':>9} {'per_onay':>9} "
          f"{'atlama_basari':>14}")
    for d, sinr, pv, po in per_mesafeye_gore(
            k0, [menzil * x for x in (0.3, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0)]):
        print(f"  {d:>9.0f} {sinr:>8.2f} {pv:>9.4f} {po:>9.4f} "
              f"{basari_olasiligi(pv, po, k0.yeniden_deneme_siniri):>14.4f}")

    bolum("2 - SINR ESIGI TARAMASI  (menzil SABIT 250 m, esik degisiyor)")
    print("  Esigi yukseltmek verici gucunu yukseltir: menzil tanimi")
    print("  'alinan guc = gurultu x esik' oldugu icin, ayni mesafede")
    print("  daha yuksek SINR elde edilir.\n")
    print(f"  {'esik_db':>8} {'menzilde_sinr':>14} {'per_veri':>9} "
          f"{'per_onay':>9} {'atlama_basari':>14} {'3 atlama':>9}")
    for esik in (10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 25.0):
        kx = DS.konfig(kol="kalib", sinr_esigi_db=esik)
        d, sinr, pv, po = per_mesafeye_gore(kx, [kx.iletim_menzili_m])[0]
        b = basari_olasiligi(pv, po, kx.yeniden_deneme_siniri)
        print(f"  {esik:>8.1f} {sinr:>14.2f} {pv:>9.4f} {po:>9.4f} "
              f"{b:>14.4f} {b ** 3:>9.4f}")

    bolum("3 - PAKET BOYUTU  (gövde biti azalirsa PER duser)")
    print(f"  {'paket_bayt':>11} {'per_veri@menzil':>16} "
          f"{'atlama_basari':>14}")
    for bayt in (128, 256, 512, 1024):
        kx = DS.konfig(kol="kalib", paket_bayt=bayt)
        d, sinr, pv, po = per_mesafeye_gore(kx, [kx.iletim_menzili_m])[0]
        print(f"  {bayt:>11} {pv:>16.4f} "
              f"{basari_olasiligi(pv, po, kx.yeniden_deneme_siniri):>14.4f}")

    bolum("4 - KAC dB'DE BIR ATLAMA %99 GECER?")
    for hedef in (0.90, 0.95, 0.99):
        bulunan = None
        for esik10 in range(100, 400):
            esik = esik10 / 10.0
            kx = DS.konfig(kol="kalib", sinr_esigi_db=esik)
            d, sinr, pv, po = per_mesafeye_gore(kx, [kx.iletim_menzili_m])[0]
            if basari_olasiligi(pv, po, kx.yeniden_deneme_siniri) >= hedef:
                bulunan = esik
                break
        print(f"  atlama basarisi >= {hedef:.2f}  ->  sinr_esigi_db = "
              f"{bulunan}")
