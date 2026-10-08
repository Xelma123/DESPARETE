"""
Kâhin sarmalayıcı — teşhis ile kararın arasındaki TİP SINIRI.

🔴 NEDEN BİR TİP, BİR KURAL DEĞİL
=================================
"Protokol kâhin bilgiye bakmasın" bir disiplindir ve disiplinler unutulur.
Burada aynı şey bir **tip** hâline getiriliyor: `Kahin[T]` sarılı değeri
yalnız `.rapora()` ile verir, ve `olcum.kahin` protokollerin içe aktarma
grafiğinde **yoktur** (AST testi). Yani bir protokol kâhin bir sayıyı
kazara okuyamaz — okuyabilmesi için önce bu modülü içe aktarması, sonra
`.rapora()` çağırması gerekir; ikisi de görünür ve ikisi de yasak.

🔒 `__repr__` DEĞERİ GİZLER
===========================
Sarmalayıcı kendini yazdırırken içeriğini göstermez. Bir teşhis günlüğüne
kazara düşen kâhin değer, oradan okunup bir karara dönüşemesin diye.

⚠️ NE DEĞİLDİR
==============
Bu bir güvenlik mekanizması değildir; kararlı bir saldırgan elbette aşar.
Amacı **kazayı** imkânsız kılmak: eski simülatörde kâhin bir sayıya erişmek
için hiçbir şey yapmak gerekmiyordu, çünkü aynı nesne üzerinde duruyordu.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar

__all__ = ["Kahin", "kahin"]

T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class Kahin(Generic[T]):
    """Simülatörün bildiği ama protokolün bilmemesi gereken bir değer."""

    _deger: T

    def rapora(self) -> T:
        """🔴 Değeri okumanın TEK yolu. Yalnız `olcum/` ve rapor çağırır."""
        return self._deger

    def __repr__(self) -> str:          # değeri GİZLER
        return f"Kahin<{type(self._deger).__name__}>"

    def __str__(self) -> str:
        return self.__repr__()


def kahin(deger: T) -> Kahin[T]:
    """Kısa kurucu."""
    return Kahin(deger)
