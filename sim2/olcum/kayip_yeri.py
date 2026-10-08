"""
Kayıp yeri — yere toplamada paketler NEREDE düşüyor?

Şartname karşılığı: `v2/07-SIMULATOR-TASARIMI.md` §18 Y4 (teşhis).

🔴 NEDEN VAR
============
Tek geçitli yere toplamada geçit çevresi doğal bir darboğazdır. Oradaki kayıp
yönlendirmeden BAĞIMSIZ olabilir (kuyruk, çekişme) ve "protokol kötü" diye
okunabilir. Düşen paketin, düştüğü düğümün geçide mesafesine göre dağılımı bu
iki kaybı ayırmaya yarar.

🔒 BANTLAR İLETİM MENZİLİNDEN TÜRER
===================================
    [0, R) · [R, 2R) · [2R, ∞)      R = `nominal_bag_m`

Serbest bir mesafe sayısı yok. Mesafe düşüş ANINDA geometrik konumdan ölçülür;
bu bir teşhistir, protokolün kararına girmez.

⚠️ Eşler arası desende geçit yoktur ve bu kayıt hiç kurulmaz.
"""

from __future__ import annotations

from sim2.cekirdek.degismezler import dogrula

__all__ = ["KayipYeri"]

_BANTLAR: tuple[str, ...] = ("0-R", "R-2R", "2R+")


class KayipYeri:
    """Düşüş sebebi × geçide mesafe bandı sayımı."""

    __slots__ = ("_menzil_m", "_sayim")

    def __init__(self, menzil_m: float) -> None:
        dogrula(menzil_m > 0.0, "iletim menzili pozitif olmalı")
        self._menzil_m = menzil_m
        self._sayim: dict[str, list[int]] = {}

    def kaydet(self, sebep: str, mesafe_m: float) -> None:
        dogrula(mesafe_m >= 0.0, "mesafe negatif olamaz")
        if mesafe_m < self._menzil_m:
            bant = 0
        elif mesafe_m < 2.0 * self._menzil_m:
            bant = 1
        else:
            bant = 2
        self._sayim.setdefault(sebep, [0, 0, 0])[bant] += 1

    @property
    def toplam(self) -> int:
        return sum(sum(v) for v in self._sayim.values())

    def rapor(self) -> dict[str, object]:
        """Sonuç satırının `teshis.kayip_yeri` alanı."""
        return {
            "bantlar": _BANTLAR,
            "sebep": {s: dict(zip(_BANTLAR, v))
                      for s, v in sorted(self._sayim.items())},
            "toplam": dict(zip(_BANTLAR, (sum(v[i] for v in self._sayim.values())
                                          for i in range(len(_BANTLAR))))),
        }
