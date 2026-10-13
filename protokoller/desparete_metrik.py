"""
DESPARETE · M0.1 metrik profili — bağ kalitesi, risk ve maliyet. TEK KAYNAK.

Kaynak: `arsiv/DESPARETE_TASARIM_PAKETI_v0.1_2026-09-22/35_DESPARETE_METRIC_PROFILE_M0.md`
§3–§4 (kurallar) ve §8 (test vektörleri). Kararlar: `v2/04` K-150 · K-152.

🔒 NEDEN AYRI VE SAF
====================
M0.1'in bütün kuralları tamsayı ve belirlenimci; komşu yaşamından, alandan
ve postürden bağımsız sınanabilmeli. Bu modül simülatörden HİÇBİR ŞEY içe
aktarmaz. Girdisi yalnız düğümün kendi MAC'inin bildiği şeydir — bir
unicast'in kesinleştiği yerel an, başarısı ve tekrar sayısı (`gozlem/
protokol.py::SonucBildirimliProtokol`, K-151 Y1). Kâhin bilgisi yapısal
olarak giremez.

🔒 SAYILAR BELGENİN ALINTISIDIR, BURADA SEÇİLMEDİ
=================================================
Pencere 2,0 s · en çok 16 sonuç · epoch 0,5 s · epoch başına en az 4 sonuç ·
`C_hop = 16` · U ve ceza tabloları — hepsi `35` §3–§4'ten, olduğu gibi.
Politika yüklemlerinin eşikleri (64 · 128 · 128) `35` §5'ten.
Kayan nokta yalnız ZAMAN içindir (simülatörün yerel saati saniye cinsinden);
Q, H, U, R ve C tamsayıdır, belgenin istediği gibi.

🔒 BELGENİN AÇIK BIRAKTIĞI, BURADA SEÇİLEN — beyan
==================================================
  · *"son W_Q = 2,0 s içindeki"* → yarı açık aralık `(şimdi − 2,0 ; şimdi]`.
  · Bir epoch, bir önceki epoch işleminden (hariç) bu işleme (dâhil) kadar
    kesinleşen sonuçlardır; epochlar düğümün 0,5 s'lik periyodik
    zamanlayıcısıyla işlenir.
  · `U_age` aralıkları belgedeki gibi `[alt ; üst)`.
  · Başarısız sonucun tekrar sayısı kullanılmaz (`35` §3.1).

🔴 TV-02 BELGENİN KENDİ KURALLARIYLA ÇELİŞİYORDU — ÖLÇÜLDÜ (K-152 §4)
=====================================================================
Vektör `q = 224 · 176 · 112` ve `N_Q = 12` verip `C = 40` (kalite cezası 16)
bekliyordu. §3.2'nin kuralıyla Q, 12 sonucun ortalamasıdır: 170 ya da 171 →
ceza 4 → **C = 28**. 40, Q'yu yalnız SON epochtan (112) hesaplamaktan çıkar
ve bu, Q'yu tanımlayan üç metinle (`35` §3.2 · `36` §4 · `27`) çelişir.
Ayrıca 224 ve 176, dört gerçek bağ sonucunun ortalaması OLAMAZ (skor kümesi
255 · 127 · 85 · 63 · …). Kurallar korundu; vektör, gerçeklenebilir ve
kurallarla tutarlı hâliyle testte duruyor.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass

__all__ = ["BagOlcumu", "Olcum", "SONSUZ", "SONLU_UST", "T_EPOCH_S",
           "H_UYARI", "U_UYARI", "H_KORUMA", "c_kalite", "c_risk", "hazard",
           "koruma_kaniti", "maliyet", "sat_add", "skor", "toparlanma_kaniti",
           "u_ornek", "u_yas", "uyari_kaniti"]

W_Q_S = 2.0                # `35` §3.2 — kalite penceresi
N_Q_UST = 16                # `35` §3.2 — pencerede en çok bu kadar sonuç
T_EPOCH_S = 0.5             # `35` §3.2 · `21` §2.5 — `T_metric_epoch`
EPOCH_MIN_ORNEK = 4         # `35` §3.3 — hazard için epoch başına en az
C_HOP = 16                  # `35` §4
SONLU_UST = 0xFFFFFFFE      # `19` §12.1 — en büyük sonlu potansiyel
SONSUZ = 0xFFFFFFFF         # `19` §12.1 — ∞
H_UYARI = 64                # `35` §5 — CautionEvidence: H ≥ 64 …
U_UYARI = 128               # … veya U ≥ 128; RecoveryEvidence ikisinin altı
H_KORUMA = 128              # `35` §5 — ProtectEvidence: H ≥ 128

# (üst sınır HARİÇ, değer) — `35` §3.4; ≥ 3,0 s ya da hiç sonuç yok → 255.
_U_YAS: tuple[tuple[float, int], ...] = (
    (0.5, 0), (1.0, 32), (1.5, 64), (2.0, 128), (3.0, 192))
# (alt sınır DÂHİL, değer) — `35` §3.4; N_Q = 0 → 255.
_U_ORNEK: tuple[tuple[int, int], ...] = ((12, 0), (8, 32), (4, 64), (1, 128))
# (alt sınır DÂHİL, ceza) — `35` §4.1 · §4.2.
_C_KALITE: tuple[tuple[int, int], ...] = (
    (224, 0), (192, 2), (160, 4), (128, 8), (96, 16), (64, 32), (32, 64),
    (0, 128))
_C_RISK: tuple[tuple[int, int], ...] = (
    (224, 128), (192, 64), (160, 32), (128, 16), (96, 8), (64, 4), (32, 2),
    (0, 0))


def _aralikta(deger: int, ad: str) -> int:
    if not (isinstance(deger, int) and 0 <= deger <= 255):
        raise ValueError(f"{ad} [0, 255] tamsayı olmalı: {deger!r}")
    return deger


def skor(tekrar: int) -> int:
    """`s(r) = floor(255 / (1 + r))` — başarılı bir sonucun katkısı (§3.1)."""
    if not (isinstance(tekrar, int) and tekrar >= 0):
        raise ValueError(f"tekrar negatif olmayan tamsayı olmalı: {tekrar!r}")
    return 255 // (1 + tekrar)


def u_yas(yas_s: float | None) -> int:
    """En son uygun sonucun yaşından belirsizlik (§3.4)."""
    if yas_s is None:
        return 255
    for ust, deger in _U_YAS:
        if yas_s < ust:
            return deger
    return 255


def u_ornek(n_q: int) -> int:
    """Penceredeki örnek sayısından belirsizlik (§3.4)."""
    for alt, deger in _U_ORNEK:
        if n_q >= alt:
            return deger
    return 255


def c_kalite(q: int) -> int:
    """Kalite cezası (§4.1). Tablonun son satırı 0'dan başlar: hep bulunur."""
    q = _aralikta(q, "Q")
    return next(ceza for alt, ceza in _C_KALITE if q >= alt)


def c_risk(r: int) -> int:
    """Risk cezası (§4.2)."""
    r = _aralikta(r, "R")
    return next(ceza for alt, ceza in _C_RISK if r >= alt)


def maliyet(q: int, r: int, kalite: bool = True, risk: bool = True) -> int:
    """`C(i,j) = 16 + C_quality(Q) + C_risk(R)` (§4).

    `kalite` / `risk` yalnız ABLASYON içindir (K-159): kapalı terim 0'dır;
    ikisi de kapalıyken maliyet atlama sayısıdır. Varsayılan M0.1'in kendisi.
    """
    return (C_HOP + (c_kalite(q) if kalite else 0)
            + (c_risk(r) if risk else 0))


def sat_add(potansiyel: int, c: int) -> int:
    """İlan edilen potansiyele bağ maliyeti — taşarsa ∞ (§4 · `19` §12.1)."""
    if potansiyel >= SONSUZ or potansiyel + c > SONLU_UST:
        return SONSUZ
    return potansiyel + c


def uyari_kaniti(o: "Olcum") -> bool:
    """`CautionEvidence` — `H ≥ 64` veya `U ≥ 128` (§5)."""
    return o.h >= H_UYARI or o.u >= U_UYARI


def koruma_kaniti(o: "Olcum") -> bool:
    """`ProtectEvidence` — `H ≥ 128` (§5). Yüksek U tek başına YETMEZ."""
    return o.h >= H_KORUMA


def toparlanma_kaniti(o: "Olcum") -> bool:
    """`RecoveryEvidence` — `H < 64` ve `U < 128` (§5)."""
    return o.h < H_UYARI and o.u < U_UYARI


def hazard(epochlar) -> int:
    """Son üç epochta SÜREKLİ kötüleşme (§3.3).

    `epochlar`: en eskiden en yeniye üç `(q_e, n_e)`. Her birinde en az dört
    sonuç yoksa ya da iki düşüşten biri pozitif değilse H = 0.
    """
    son = tuple(epochlar)[-3:]
    if len(son) < 3 or any(n < EPOCH_MIN_ORNEK for _q, n in son):
        return 0
    (q2, _), (q1, _), (q0, _) = son
    d1, d2 = q2 - q1, q1 - q0
    return min(255, d1 + d2) if d1 > 0 and d2 > 0 else 0


@dataclass(frozen=True, slots=True)
class Olcum:
    """Bir epoch işleminin sonucu. `q` ve `c` ilk sonuçtan önce `None`dur:
    kayıt o zamana kadar metrik kaynağı olamaz (§3.2)."""

    q: int | None
    h: int
    u: int
    r: int
    c: int | None
    n_q: int


class BagOlcumu:
    """Bir doğrudan komşuya giden bağın (`i → j`) M0.1 durumu.

    🔒 Kayıt `O(1)`: en çok 16 sonuç + üç epoch özeti (`27`'nin sınırı).
    Epoch içindeki sonuçlar liste olarak değil TOPLAM ve SAYI olarak tutulur.
    """

    __slots__ = ("_sonuclar", "_epoch_toplam", "_epoch_sayi", "_epochlar",
                 "_son_q", "_son_t")

    def __init__(self) -> None:
        # (an, skor) — en yeni sağda. En yeni 16'dan eskisi hiçbir kurala
        # girmediği için tutulmaz; yaş için yalnız `_son_t` gerekir.
        self._sonuclar: deque[tuple[float, int]] = deque(maxlen=N_Q_UST)
        self._epoch_toplam = 0
        self._epoch_sayi = 0
        self._epochlar: deque[tuple[int | None, int]] = deque(maxlen=3)
        self._son_q: int | None = None
        self._son_t: float | None = None

    def sonuc(self, t_s: float, basarili: bool, tekrar: int) -> None:
        """Bir unicast sonucu kesinleşti (yerel an)."""
        s = skor(tekrar) if basarili else 0
        self._sonuclar.append((t_s, s))
        self._epoch_toplam += s
        self._epoch_sayi += 1
        self._son_t = t_s

    def epoch(self, simdi_s: float) -> Olcum:
        """`T_metric_epoch` doldu: epochu kapat, Q · H · U · R · C'yi üret."""
        q_e = (self._epoch_toplam // self._epoch_sayi
               if self._epoch_sayi else None)
        self._epochlar.append((q_e, self._epoch_sayi))
        self._epoch_toplam = self._epoch_sayi = 0
        pencere = [s for t, s in self._sonuclar if t > simdi_s - W_Q_S]
        n_q = len(pencere)
        if n_q:
            self._son_q = sum(pencere) // n_q
        h = hazard(self._epochlar)
        yas = None if self._son_t is None else simdi_s - self._son_t
        u = max(u_yas(yas), u_ornek(n_q))
        r = max(h, u)
        c = None if self._son_q is None else maliyet(self._son_q, r)
        return Olcum(q=self._son_q, h=h, u=u, r=r, c=c, n_q=n_q)
