"""
Topoloji — ZAMANA BAĞLI. Eski simülatörün en büyük kusuru buradaydı.

🔴 NE DEĞİŞTİ
=============
Eski `Topoloji` dondurulmuş bir nesneydi: konumlar bir kez çekiliyor ve koşu
boyunca hiç değişmiyordu. Proje ise *"karıştırma altındaki taktik İHA mesh
ağları"* iddiasını taşıyor. Sabit topolojili bir İHA ağı, İHA ağı değildir.

Burada topoloji bir **fonksiyondur**: `konum(dugum, t)`. Kanal katmanı onu
parça başına, sıra dışı zamanlarda çağırır; bu yüzden **saf** olmak zorunda —
çağrı sırası sonucu değiştiremez.

🔴 BU MODÜL BİR KÂHİN YÜZEYİDİR
===============================
Buradaki graf **geometriktir**: iki düğüm menzil içindeyse "bağ" vardır.
Protokolün gördüğü şey bu değildir — protokol yalnız `gozlem/` üzerinden
komşu görür ve orada bağ, kanalın verdiği gerçek alım başarısıyla tanımlıdır.
Buradaki graf ölçüme, kalibrasyona ve teşhise aittir.

⚠️ AÇIK TAAHHÜT — `kopma_fiziksel` HENÜZ BURADAN TANIMLANMADI
=============================================================
Sayaç kaydı `kopma_fiziksel`i *"SINR eşiği altına inen bağ"* diye tanımlıyor.
Gölgeleme ve sönümleme eklendikten sonra bu, **saf menzilden farklıdır**:
gölgeleme σ = 3 dB iken menzil sınırı ±3 dB'lik bir bulanıklık kazanır ve
ölçüldü — PER'in 0,01'den 0,99'a düştüğü bant yalnızca 3,02 dB, yani tek bir
σ'dan dar. Bu yüzden `kopma_fiziksel` Adım 4'te **kanalın yavaş SINR'i**
(yol kaybı + gölgeleme + anten deseni, hızlı sönümleme HARİÇ) üzerinden
tanımlanacak. Buradaki geometrik graf o tanımın yerine geçmez; çalışma
noktasını ölçmek ve bölünmeyi izlemek içindir.
Üretici: `python kalibrasyon/adim3_oncesi.py`
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
        """Bir zaman serisinin bağlantılılık özeti.

        🔴 `tam_bagli_zaman_orani` BU GRAFİKTE ÖLÇÜLÜR, yani 280 m'lik
        TEŞHİS DİSKİNDE — ve modül başlığının söylediği gibi o disk veri
        yolunda hiçbir yeri kapamaz (K-096). Bu sayıyı bir bağlantılılık
        SONUCU diye okumak, kimsenin kullanmadığı bir ağı raporlamaktır.

        Bugün ölçülen (30 tohum × 350 s, üretici:
        `python kalibrasyon/adim3_kapanis.py`): statik **%0,0** · hareketli
        **%0,0** — derece 2,53 ↔ 2,49. Veri taşıyan KANAL grafiğinde ise
        statik kol 270/270 anda tek parça, derece 8,76 (üretici:
        `python kalibrasyon/denetim_ornekleme.py d`).

        ⚠️ Buradaki eski yorum (*"statik %73,3 · mobil %82,4"*) iki kere
        çürüdü — üreticisi aylardır koşmuyordu ve terk edilmiş bir çalışma
        noktasından geliyordu. Tam kayıt `yapilandirma/senaryolar.py`de.
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
    return Topoloji(mobilite=mobilite, menzil_m=konfig.iletim_menzili_m,
                    dugum_sayisi=konfig.dugum_sayisi)
