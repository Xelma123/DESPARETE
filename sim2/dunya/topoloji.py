"""
Topoloji — zamana bağlı: `konum(dugum, t)` zamanın SAF fonksiyonudur. Kanal
katmanı onu parça başına, sıra dışı zamanlarda çağırır; çağrı sırası sonucu
değiştiremez.

🔴 BU MODÜL BİR KÂHİN YÜZEYİDİR
===============================
Buradaki graf geometriktir (menzil içi = bağ) ve ölçüme, kalibrasyona,
teşhise aittir. Protokol komşuyu yalnız `gozlem/` üzerinden, kanalın verdiği
gerçek alım başarısıyla görür. Fiziksel kopma buradan değil kanalın yavaş
SINR'inden tanımlanır (`olcum/kopma.py`).
"""

from __future__ import annotations

import statistics as ist
from dataclasses import dataclass

from sim2.cekirdek.degismezler import dogrula
from sim2.cekirdek.rng import Akislar
from sim2.dunya.geometri import Nokta3, mesafe
from sim2.dunya.mobilite import GecitliMobilite, Mobilite, mobilite_kur
from sim2.dunya.yerlesim import (
    bilesenler, gecit_noktasi, komsuluk_listesi, kutu_kur, yerlesim_kur)
from sim2.yapilandirma.konfig import Konfig

__all__ = ["Anlik", "Topoloji", "topoloji_kur"]


@dataclass(frozen=True, slots=True)
class Anlik:
    """Tek bir andaki geometrik graf. Dondurulmuş: kimse üzerine yazamaz."""
    t_s: float
    konumlar: tuple[Nokta3, ...]
    komsular: tuple[tuple[int, ...], ...]

    @property
    def ortalama_derece(self) -> float:
        return sum(len(k) for k in self.komsular) / len(self.komsular)

    @property
    def bilesenler(self) -> tuple[tuple[int, ...], ...]:
        return bilesenler(self.komsular)

    @property
    def bagli_mi(self) -> bool:
        return len(self.bilesenler) == 1

    @property
    def en_buyuk_bilesen(self) -> int:
        return len(self.bilesenler[0])

    @property
    def baglar(self) -> frozenset[tuple[int, int]]:
        """Yönsüz bağ kümesi — bağ olaylarını çıkarmak için."""
        return frozenset((i, j) for i, ks in enumerate(self.komsular)
                         for j in ks if i < j)


class Topoloji:
    """Zamana bağlı geometrik topoloji.

    `konum` sıcak yoldur (parça başına çağrılır) ve doğrudan mobiliteye iner.
    `anlik` O(n²)dir ve teşhis/kalibrasyon içindir; sıcak yolda çağrılmaz.
    """

    __slots__ = ("mobilite", "menzil_m", "dugum_sayisi")

    def __init__(self, *, mobilite: Mobilite, menzil_m: float,
                 dugum_sayisi: int) -> None:
        dogrula(menzil_m > 0.0, "iletim menzili pozitif olmalı")
        dogrula(dugum_sayisi >= 2, "en az iki düğüm gerekli")
        self.mobilite = mobilite
        self.menzil_m = menzil_m
        self.dugum_sayisi = dugum_sayisi

    # ------------------------------------------------------------ sıcak yol
    @property
    def hareketli(self) -> bool:
        return self.mobilite.hareketli

    def konum(self, dugum: int, t_s: float) -> Nokta3:
        return self.mobilite.konum(dugum, t_s)

    def mesafe(self, i: int, j: int, t_s: float) -> float:
        return mesafe(self.konum(i, t_s), self.konum(j, t_s))

    def menzilde_mi(self, i: int, j: int, t_s: float) -> bool:
        """🔴 GEOMETRİK bağ — kanalın verdiği gerçek bağ DEĞİL."""
        return self.mesafe(i, j, t_s) <= self.menzil_m

    # -------------------------------------------------------------- teşhis
    def anlik(self, t_s: float) -> Anlik:
        konumlar = tuple(self.konum(i, t_s) for i in range(self.dugum_sayisi))
        return Anlik(t_s, konumlar, komsuluk_listesi(konumlar, self.menzil_m))

    def zaman_serisi(self, bas_s: float, bitis_s: float, adim_s: float
                     ) -> tuple[Anlik, ...]:
        dogrula(adim_s > 0.0, "örnekleme adımı pozitif olmalı")
        dogrula(bas_s <= bitis_s, "zaman aralığı ters")
        n = int((bitis_s - bas_s) / adim_s) + 1
        return tuple(self.anlik(bas_s + k * adim_s) for k in range(n))

    @staticmethod
    def baglantililik_ozeti(seri: tuple[Anlik, ...]) -> dict[str, float]:
        """Geometrik grafiğin bağlantılılık özeti — TEŞHİS.

        🔴 Bu grafik veri yolunda hiçbir yeri kapamaz (K-096): kimin duyacağını
        alınan güç, alınıp alınmadığını SINR belirler. Buradaki
        `tam_bagli_zaman_orani`nı bir bağlantılılık SONUCU diye okumak, kimsenin
        kullanmadığı bir ağı raporlamaktır; veri taşıyan grafiğin bölünmesi
        `yapilandirma/senaryolar.py`nin tablolarında.
        """
        dogrula(len(seri) > 0, "boş zaman serisi özetlenemez")
        return {
            "ornek_sayisi": float(len(seri)),
            "tam_bagli_zaman_orani": sum(a.bagli_mi for a in seri) / len(seri),
            "ortalama_derece": ist.mean(a.ortalama_derece for a in seri),
            "en_kucuk_en_buyuk_bilesen": float(
                min(a.en_buyuk_bilesen for a in seri)),
            "ortalama_en_buyuk_bilesen": ist.mean(
                a.en_buyuk_bilesen for a in seri),
        }

    @staticmethod
    def bag_olaylari(seri: tuple[Anlik, ...]) -> dict[str, int]:
        """Ardışık anlar arasında açılan/kapanan geometrik bağ sayısı.

        ⚠️ Bu `kopma_fiziksel` DEĞİLDİR — modül başlığındaki açık taahhüde bak.
        Örnekleme adımından daha kısa süren bir kopma bu sayımda görünmez;
        adım küçüldükçe sayım artar ve bu, sayının bir ÖZELLİĞİDİR, hatası
        değil. Raporlanırken adım da yazılır.
        """
        acilan = kapanan = 0
        for onceki, simdi in zip(seri, seri[1:]):
            a, b = onceki.baglar, simdi.baglar
            acilan += len(b - a)
            kapanan += len(a - b)
        return {"acilan": acilan, "kapanan": kapanan}


# ==========================================================================
def topoloji_kur(konfig: Konfig, akislar: Akislar) -> Topoloji:
    """`Konfig` + tohum → dünya. Adım 3'ün tek giriş noktası."""
    baslangic = yerlesim_kur(konfig, akislar)
    mobilite = mobilite_kur(
        kol=konfig.mobilite_kolu,
        baslangic=baslangic,
        kutu=kutu_kur(konfig),
        akislar=akislar,
        kosu_bitis_s=konfig.kosu_bitis_s,
        alfa=konfig.gm_alfa,
        adim_s=konfig.gm_adim_s,
        hiz_min_ms=konfig.gm_hiz_min_ms,
        hiz_maks_ms=konfig.gm_hiz_maks_ms,
        hiz_sigma_ms=konfig.gm_hiz_sigma_ms,
        azimut_sigma_rad=konfig.gm_azimut_sigma_rad,
        pitch_ort_rad=konfig.gm_pitch_ort_rad,
        pitch_sigma_rad=konfig.gm_pitch_sigma_rad,
        grup_sayisi=konfig.gorev_grup_sayisi,
        grup_yaricapi_m=konfig.gorev_grup_yaricapi_m,
        jitter_hiz_ms=konfig.gorev_jitter_hiz_ms,
        istasyon_kayma_hiz_ms=konfig.istasyon_kayma_hiz_ms,
    )
    if konfig.yere_toplama:
        # 🔒 Geçit sabit istasyonda; iç modelin çekimleri değişmez (Y4).
        mobilite = GecitliMobilite(mobilite, konfig.gecit,
                                   gecit_noktasi(konfig))
    return Topoloji(mobilite=mobilite, menzil_m=konfig.nominal_bag_m,
                    dugum_sayisi=konfig.dugum_sayisi)
