"""
Yer–hava (A2G) kanalı — yerdeki karıştırıcı ↔ İHA bağının ek kaybı.

Kaynak: Al-Hourani, Kandeepan, Lardner, "Optimal LAP Altitude for Maximum
Coverage", IEEE WCL 2014 (`v2/02` G6). `v2/15` A6 · K-176.

    PL = FSPL + η_ξ ,  ξ ∈ {LoS, NLoS}
    P(LoS, θ) = 1 / (1 + a·exp(−b[θ − a]))       θ yükseklik açısı, DERECE

FSPL simülatörün yol kaybıdır (α = 2); bu modül yalnız η'yı ekler. Görüş
hattı durumu bağ ve zaman dilimi başına HASH'ten çekilir (`kanal_karar`
alanı, `a2g` anahtarı — yeni alan açılmaz): dilimin ortalaması makalenin
beklenen kaybını (denklem 9) verir, dilimler arası değişim binaların
arasından geçişi temsil eder.

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
           "YerHavaKanali"]

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


class YerHavaKanali:
    """Bir yer karıştırıcısının İHA'lara bağı için ek kayıp η."""

    __slots__ = ("_tohum", "_dilim_s", "_a", "_b", "_eta_los", "_eta_nlos")

    def __init__(self, tohum: int, ortam: str, dilim_s: float) -> None:
        dogrula(dilim_s > 0.0, "yer–hava durum dilimi pozitif olmalı")
        self._tohum = tohum
        self._dilim_s = dilim_s
        self._a, self._b = s_egrisi(ortam)
        self._eta_los, self._eta_nlos = A2G_ORTAMLARI[ortam][3:]

    def gorus_hatti_mi(self, kimlik: int, dugum: int, yer: Nokta3,
                       hava: Nokta3, t_s: float) -> bool:
        yatay = math.hypot(hava.x - yer.x, hava.y - yer.y)
        teta = math.degrees(math.atan2(hava.z - yer.z, yatay))
        p = gorus_hatti_olasiligi(self._a, self._b, teta)
        return hash_cekimi("kanal_karar", self._tohum, "a2g", kimlik, dugum,
                           int(t_s / self._dilim_s)) < p

    def ek_kayip_db(self, kimlik: int, dugum: int, yer: Nokta3, hava: Nokta3,
                    t_s: float) -> float:
        return (self._eta_los if self.gorus_hatti_mi(kimlik, dugum, yer, hava,
                                                    t_s)
                else self._eta_nlos)
