"""
3B geometri — konum, mesafe, yükseliş açısı, sınır kutusu.

🔴 NEDEN 3B
===========
Eski simülatör 2B idi. Literatür 2B mobilite modelini **adlandırılmış bir
hata** olarak listeliyor: *"2D mobilite modeli kullanmak → 3D FANET
dinamiklerini kaçırmak"*. Bir İHA ağında irtifa bir serbestlik derecesidir ve
hem bağ geometrisini hem karıştırıcının aydınlatma desenini değiştirir.

🔒 YÜKSELİŞ AÇISI NEDEN BURADA
==============================
Anten deseni (yarım dalga dipol) yükseliş açısına bağlıdır ve 3B'de bu ihmal
edilebilir değildir. Ölçüldü — 1000×1000×120 m hacimde, menzil içi çiftler:

    yükseliş açısı : ortanca 11,1°   p95 40,6°
    dipol kaybı    : ortanca 0,24 dB  p95 3,27 dB

*(Aynı ölçüm 300 m irtifa bandında p95'te **9,70 dB** veriyor — gölgeleme
σ'sının çok üstünde. Çalışma noktası bu yüzden 120 m seçildi.)*
"""

from __future__ import annotations

import math
from dataclasses import dataclass

__all__ = ["Nokta3", "Kutu", "mesafe", "yatay_mesafe", "yukselis_acisi_rad"]


@dataclass(frozen=True, slots=True)
class Nokta3:
    x: float
    y: float
    z: float

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z


@dataclass(frozen=True, slots=True)
class Kutu:
    """Operasyon hacmi. Düğümler bunun dışına çıkamaz.

    🔒 SINIR KURALI: **yansıma** (`yansit`). Alternatifler ve neden elendiği:
      · *sarma (torus)* — fiziksel karşılığı yok; bir İHA alanın bir ucundan
        diğerine ışınlanmaz ve komşuluk grafiği anlamsızlaşır
      · *kelepçeleme (clamp)* — düğümler sınırda birikir, kenarda yapay
        yoğunlaşma yaratır ve derece dağılımını bozar
      · *yeniden çekim* — yörüngenin sürekliliğini kırar
    Yansıma üçünün de tuzağından uzak: konum sürekli, dağılım düzgün kalır.

    ⚠️ Yansıma TEK BAŞINA yetmez ve bu ölçüldü. Gauss-Markov düğümü kendi
    sabit ortalama yönüne geri çeker; o ortalama duvarı gösterdiği sürece
    düğüm duvara yapışır. Sınır kuralının ikinci yarısı `mobilite.py`dedir.

    🔒 DİKEY TABAN: `taban_m`. İrtifa bandı 20–120 m ise düğüm koşu boyunca
    da o bandın içinde kalmalı — yalnız başlangıçta değil. Tabansız bir kutu,
    öğrencinin verdiği "20–120 m" kararını yalnız yarım uygular: düğümler
    dakikalar içinde 0 m'ye, yani yere inerdi.
    """
    en_m: float
    boy_m: float
    yukseklik_m: float
    taban_m: float = 0.0

    def icinde_mi(self, p: Nokta3) -> bool:
        return (0.0 <= p.x <= self.en_m
                and 0.0 <= p.y <= self.boy_m
                and self.taban_m <= p.z <= self.yukseklik_m)

    def ayna_ekseni(self, p: Nokta3) -> tuple[bool, bool, bool]:
        """`yansit`in hangi eksenlerde aynalayacağı — `(x, y, z)`.

        🔒 Ayrı bir metot olmasının sebebi: yansıma yalnız ANLIK yönü değil,
        Gauss-Markov'un ORTALAMA yönünü de çevirmek zorunda. İkisi aynı
        dönüşümü uygulamalı, yoksa düğüm duvara yapışır (bkz. `mobilite.py`).
        Aynalama kuralı burada TEK yerde tanımlıdır.
        """
        return (p.x < 0.0 or p.x > self.en_m,
                p.y < 0.0 or p.y > self.boy_m,
                p.z < self.taban_m or p.z > self.yukseklik_m)

    @staticmethod
    def aci_aynala(azimut: float, x_ayna: bool, y_ayna: bool) -> float:
        """`yansit`in azimuta uyguladığı dönüşümün aynısı — tek tanım."""
        if x_ayna:
            azimut = math.pi - azimut
        if y_ayna:
            azimut = -azimut
        return (azimut + math.pi) % (2 * math.pi) - math.pi

    def yansit(self, p: Nokta3, azimut: float, pitch: float
               ) -> tuple[Nokta3, float, float]:
        """Kutudan taşan konumu içeri yansıtır; yönü de günceller.

        Döner: `(yeni_konum, yeni_azimut, yeni_pitch)`.
        """
        x, y, z = p.x, p.y, p.z
        if x < 0.0:
            x = -x
            azimut = math.pi - azimut
        elif x > self.en_m:
            x = 2.0 * self.en_m - x
            azimut = math.pi - azimut
        if y < 0.0:
            y = -y
            azimut = -azimut
        elif y > self.boy_m:
            y = 2.0 * self.boy_m - y
            azimut = -azimut
        if z < self.taban_m:
            z = 2.0 * self.taban_m - z
            pitch = -pitch
        elif z > self.yukseklik_m:
            z = 2.0 * self.yukseklik_m - z
            pitch = -pitch
        # Çok büyük bir adım iki kez taşırsa (patolojik) kutuya kelepçele.
        x = min(max(x, 0.0), self.en_m)
        y = min(max(y, 0.0), self.boy_m)
        z = min(max(z, self.taban_m), self.yukseklik_m)
        return Nokta3(x, y, z), (azimut + math.pi) % (2 * math.pi) - math.pi, pitch


def mesafe(a: Nokta3, b: Nokta3) -> float:
    """3B Öklid mesafesi — menzil ve yol kaybı bunu kullanır."""
    dx = a.x - b.x
    dy = a.y - b.y
    dz = a.z - b.z
    return math.sqrt(dx * dx + dy * dy + dz * dz)


def yatay_mesafe(a: Nokta3, b: Nokta3) -> float:
    return math.hypot(a.x - b.x, a.y - b.y)


def yukselis_acisi_rad(a: Nokta3, b: Nokta3) -> float:
    """`a`dan `b`ye bakış açısının yataya göre yükselişi, `[0, π/2]`.

    İşaret taşımaz: dipol deseni yukarı ve aşağı bakışta simetriktir.
    """
    return math.atan2(abs(a.z - b.z), yatay_mesafe(a, b))
