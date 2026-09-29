"""
Başlangıç yerleşimi — düğümler hacme nasıl dağıtılır.

🔒 BAĞLANTI KOŞULLAMASI YOK
===========================
Yerleşim bağlı olsun diye yeniden çekilmez: koşullama hareketin girdiği
rejimi değiştirmiyor, yalnız beyan edilmiş bir yanlılık ekliyordu; statik
kolda açılsaydı statik ve hareketli kollar farklı yerleşim dağılımlarından
örneklenir ve mobilite ekseni karşılaştırılamaz olurdu. Veri taşıyan kanal
grafiğinde statik kol zaten tek parçadır: alan "kopukluğun sıfır kaldığı en
büyük alan" ölçütüyle seçildi (referansta 33 km, K-188). Bölünme ana deney
tohumlarında ölçülüp satırda beyan edilir (`senaryolar.py`).

🔒 İRTİFA AYRI BİR AKIŞTAN ÇEKİLİR
==================================
`yerlesim` (x, y) ve `irtifa` (z) ayrı sıralı akışlardır. Tek akıştan
çekilselerdi irtifa bandını değiştirmek yatay yerleşimi de kaydırırdı ve
"yalnız irtifayı değiştirdim" diyen bir tarama aslında başka bir deney olurdu.
"""

from __future__ import annotations

from typing import Sequence

from sim2.cekirdek.degismezler import dogrula
from sim2.cekirdek.rng import Akislar
from sim2.dunya.geometri import Kutu, Nokta3, mesafe
from sim2.yapilandirma.konfig import Konfig

__all__ = ["kutu_kur", "gecit_noktasi", "yerlesim_kur", "komsuluk_listesi",
           "bilesenler"]


def kutu_kur(konfig: Konfig) -> Kutu:
    """Operasyon hacmi — `Konfig` alanlarından kurulur.

    Katman yönü gereği bu dönüşüm `dunya`da yapılır: `yapilandirma`nın
    `dunya`yı içe aktarması yönü tersine çevirirdi.

    🔒 Kutunun dikey sınırı **irtifa bandının kendisidir**. Ayrı bir yükseklik
    alanı olsaydı bandla ikinci bir doğru kaynağı doğardı.
    """
    return Kutu(konfig.alan_en_m, konfig.alan_boy_m,
                yukseklik_m=konfig.irtifa_maks_m,
                taban_m=konfig.irtifa_min_m)


def gecit_noktasi(konfig: Konfig) -> Nokta3 | None:
    """Yere toplamada geçidin sabit istasyonu — konfigden TÜRETİLİR (Y4).

    `kenar`: batı kenarının ortası · `merkez`: alan merkezi. İrtifa bandın
    ortasıdır; serbest bir sayı yok. Kenarda geçide giden yollar uzar
    (derinlik, `v2/07` §06.2). Katman yönü gereği `kutu_kur` gibi burada;
    eşler arası desende geçit yoktur.
    """
    if konfig.trafik_deseni != "yere_toplama":
        return None
    x = 0.0 if konfig.gecit_konumu == "kenar" else konfig.alan_en_m / 2.0
    return Nokta3(x, konfig.alan_boy_m / 2.0,
                  (konfig.irtifa_min_m + konfig.irtifa_maks_m) / 2.0)


def yerlesim_kur(konfig: Konfig, akislar: Akislar) -> tuple[Nokta3, ...]:
    """Düğümleri hacme düzgün dağıtır. Reddetme YOK — yukarıdaki nota bak."""
    yatay = akislar["yerlesim"]
    dikey = akislar["irtifa"]
    noktalar = tuple(
        Nokta3(yatay.uniform(0.0, konfig.alan_en_m),
               yatay.uniform(0.0, konfig.alan_boy_m),
               dikey.uniform(konfig.irtifa_min_m, konfig.irtifa_maks_m))
        for _ in range(konfig.dugum_sayisi))
    dogrula(len(noktalar) == konfig.dugum_sayisi, "yerleşim eksik düğüm üretti")
    return noktalar


# ==========================================================================
# Graf yardımcıları — KÂHİN yüzey (aşağıdaki nota bak)
# ==========================================================================
# 🔴 Bunlar GEOMETRİK graf üretir; protokolün gördüğü şey değildir. Protokol
# yalnız `gozlem/` üzerinden komşu görür ve orada bağ, kanalın verdiği alım
# başarısıyla tanımlıdır. Buradaki graf ölçüme ve kalibrasyona aittir.
def komsuluk_listesi(konumlar: Sequence[Nokta3], menzil_m: float
                     ) -> tuple[tuple[int, ...], ...]:
    n = len(konumlar)
    return tuple(
        tuple(j for j in range(n)
              if j != i and mesafe(konumlar[i], konumlar[j]) <= menzil_m)
        for i in range(n))


def bilesenler(komsular: Sequence[Sequence[int]]) -> tuple[tuple[int, ...], ...]:
    """Bağlı bileşenler, büyükten küçüğe."""
    n = len(komsular)
    gorulen = [False] * n
    cikti: list[tuple[int, ...]] = []
    for s in range(n):
        if gorulen[s]:
            continue
        yigin, uyeler = [s], []
        gorulen[s] = True
        while yigin:
            u = yigin.pop()
            uyeler.append(u)
            for v in komsular[u]:
                if not gorulen[v]:
                    gorulen[v] = True
                    yigin.append(v)
        cikti.append(tuple(sorted(uyeler)))
    cikti.sort(key=len, reverse=True)
    return tuple(cikti)
