"""
Yer–hava (A2G) kanalı — yerdeki karıştırıcı ↔ İHA bağının ek kaybı.

Kaynak: Al-Hourani, Kandeepan, Lardner, "Optimal LAP Altitude for Maximum
Coverage", IEEE WCL 2014 (`v2/02` G6). `v2/15` A6 · K-176.

    PL = FSPL + η_ξ ,  ξ ∈ {LoS, NLoS}
    P(LoS, θ) = 1 / (1 + a·exp(−b[θ − a]))       θ yükseklik açısı, DERECE

FSPL simülatörün yol kaybıdır (α = 2); bu modül yalnız η'yı ekler.

🔒 GÖRÜŞ HATTI GEOMETRİDEN, KALICI (denetim DD-01, K-242)
=======================================================
Alçak yükselme açısında ışını kesen engeller karıştırıcının yakınındadır:
ışın tipik bina yüksekliğine (γ, ortamın Rayleigh ölçeği) karıştırıcıdan
d = (γ − h_k) / tan θ uzakta iner. O noktanın yerdeki konumu "engel
noktası"dır. Yer, ortamın ortalama bina genişliğinde (w = √(α/β) km;
banliyöde ≈ 11,5 m) hücrelere bölünür; her hücrenin durumsuz bir çekimi
u vardır (`kanal_karar` alanı, `a2g` anahtarı). Işın görüş hattıdır ⇔
u < P(LoS, θ). Yani hücreler üzerinden ortalama makalenin olasılığını
verir; durum ise engel noktası bir bina genişliği kaymadıkça ve açı
değişmedikçe AYNI kalır. Formasyondaki İHA'nın küçük yer değiştirmesi
engel noktasını metrenin altında kaydırır; karıştırıcı taşınınca engel
noktaları yeni binalara düşer. Yeni serbest parametre yok: w ve γ
makalenin ortam parametreleridir.
Önceki model durumu her (karıştırıcı, düğüm) çifti için her SANİYE
bağımsız çekiyordu (`a2g_durum_dilimi_s`); istasyon tutan İHA'da bile
1–3 s'lik parlamalar üretiyordu.

🔴 S-EĞRİSİ KATSAYILARI ELLE YAZILMADI — makalenin Tablo I–II polinomundan
(denklem 6) ortam parametreleriyle (α, β, γ; Şekil 2 metni) HESAPLANIR.
İndeks okuması: metin z = Σ C_ij (αβ)^i γ^j diyor, ama o okuma b'yi negatif,
P(LoS)'u açıyla AZALAN verir (imkânsız; Şekil 2'nin bütün eğrileri artan).
Tablonun sütun indeksi γ'nın, satır indeksi αβ'nın üssü okunduğunda banliyö
a = 4,880, b = 0,429 çıkar ve Şekil 2 ile tutarlıdır. Karşılaştırma:
`arsiv/teshis/a6_karistirici_2026-09-26/al_hourani_ab.py`.

⚠️ Makale η'nın ORTALAMASINI verir; etrafındaki Gauss yayılımı
simülatörün gölgelemesiyle temsil edilir (beyan). Açık kırsal ortam
makalede yok; en yakını banliyö (`v2/14`).
"""

from __future__ import annotations

import math

from sim2.cekirdek.degismezler import dogrula
from sim2.cekirdek.rng import hash_cekimi
from sim2.dunya.geometri import Nokta3

__all__ = ["A2G_ORTAMLARI", "s_egrisi", "gorus_hatti_olasiligi",
           "bina_genisligi_m", "YerHavaKanali"]

# ortam → (α, β, γ, η_LoS dB, η_NLoS dB) — Şekil 2 metni ve §III (G6)
A2G_ORTAMLARI: dict[str, tuple[float, float, float, float, float]] = {
    "banliyo": (0.1, 750.0, 8.0, 0.1, 21.0),
    "kentsel": (0.3, 500.0, 15.0, 1.0, 20.0),
    "yogun": (0.5, 300.0, 20.0, 1.6, 23.0),
    "yuksek": (0.5, 300.0, 50.0, 2.3, 34.0),
}

# Tablo I (a) · Tablo II (b): anahtar (sütun, satır) — okuma yukarıda.
_C_A = {(0, 0): 9.34e-01, (1, 0): 2.30e-01, (2, 0): -2.25e-03,
        (3, 0): 1.86e-05, (0, 1): 1.97e-02, (1, 1): 2.44e-03,
        (2, 1): 6.58e-06, (0, 2): -1.24e-04, (1, 2): -3.34e-06,
        (0, 3): 2.73e-07}
_C_B = {(0, 0): 1.17e+00, (1, 0): -7.56e-02, (2, 0): 1.98e-03,
        (3, 0): -1.78e-05, (0, 1): -5.79e-03, (1, 1): 1.81e-04,
        (2, 1): -1.65e-06, (0, 2): 1.73e-05, (1, 2): -2.02e-07,
        (0, 3): -2.00e-08}


def s_egrisi(ortam: str) -> tuple[float, float]:
    """`(a, b)` — Tablo I–II polinomu, sütun γ, satır αβ."""
    dogrula(ortam in A2G_ORTAMLARI, f"bilinmeyen yer–hava ortamı: {ortam!r}")
    alfa, beta, gama, _, _ = A2G_ORTAMLARI[ortam]
    ab = alfa * beta

    def poli(c):
        return sum(v * gama ** i * ab ** j for (i, j), v in c.items())
    return poli(_C_A), poli(_C_B)


def gorus_hatti_olasiligi(a: float, b: float, teta_derece: float) -> float:
    return 1.0 / (1.0 + a * math.exp(-b * (teta_derece - a)))


def bina_genisligi_m(ortam: str) -> float:
    """Ortalama bina genişliği √(α/β) km — α yapılı alan oranı, β km² başına
    bina sayısı (makalenin ortam parametreleri, ITU-R P.1410)."""
    alfa, beta, _, _, _ = A2G_ORTAMLARI[ortam]
    return 1000.0 * math.sqrt(alfa / beta)


class YerHavaKanali:
    """Bir yer karıştırıcısının İHA'lara bağı için ek kayıp η."""

    __slots__ = ("_tohum", "_a", "_b", "_gama_m", "_w_m", "_eta_los",
                 "_eta_nlos")

    def __init__(self, tohum: int, ortam: str) -> None:
        self._tohum = tohum
        self._a, self._b = s_egrisi(ortam)
        self._gama_m = A2G_ORTAMLARI[ortam][2]
        self._w_m = bina_genisligi_m(ortam)
        self._eta_los, self._eta_nlos = A2G_ORTAMLARI[ortam][3:]

    def engel_noktasi(self, yer: Nokta3, hava: Nokta3) -> tuple[float, float]:
        """Işının tipik bina yüksekliğine indiği yer noktası (x, y)."""
        dx, dy = hava.x - yer.x, hava.y - yer.y
        yatay = math.hypot(dx, dy)
        if yatay == 0.0:
            return yer.x, yer.y
        dogrula(hava.z > yer.z, "İHA karıştırıcının üstünde olmalı")
        d = min(yatay, max(self._gama_m - yer.z, 0.0) * yatay / (hava.z - yer.z))
        return yer.x + d * dx / yatay, yer.y + d * dy / yatay

    def gorus_hatti_mi(self, yer: Nokta3, hava: Nokta3) -> bool:
        yatay = math.hypot(hava.x - yer.x, hava.y - yer.y)
        teta = math.degrees(math.atan2(hava.z - yer.z, yatay))
        p = gorus_hatti_olasiligi(self._a, self._b, teta)
        x, y = self.engel_noktasi(yer, hava)
        return hash_cekimi("kanal_karar", self._tohum, "a2g",
                           math.floor(x / self._w_m),
                           math.floor(y / self._w_m)) < p

    def ek_kayip_db(self, yer: Nokta3, hava: Nokta3) -> float:
        return (self._eta_los if self.gorus_hatti_mi(yer, hava)
                else self._eta_nlos)
