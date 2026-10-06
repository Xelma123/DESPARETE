"""
Değişmezler — `assert`in yerine geçen kontrol.

NEDEN `assert` DEĞİL
====================
`python -O` altında `assert` satırları **derleme sırasında silinir**. Eski
simülatörde yedi gerçek değişmez `assert` ile yazılmıştı ve dördü kalktığında
sessiz bir yanlış cevap üretiyordu: olay zamanı geriye gidebiliyor, ölçüm
penceresi dışında üretilen paket ölçüme girebiliyor, koşu bitiminden sonra
beacon görünmeyebiliyor, alıcı kendi gücünü girişime ekleyebiliyordu.

*"Ölçüm koşuları `-O`suz yapılır"* bir disiplindir, koruma değildir. Burada
disiplin yerine mekanizma var: `dogrula()` her zaman koşar.

MALİYET
=======
Sıcak yollarda (parça başına PER, girişim toplama) çağrı başına birkaç
nanosaniye. Ölçüldüğünde koşu süresinin %1'ini aşarsa, o çağrı **kaldırılmaz**
— `kritik=False` ile işaretlenir ve `AYRINTILI_DOGRULAMA` kapalıyken atlanır.
Kaldırmak yerine işaretlemek, kararın görünür kalmasını sağlar.
"""

from __future__ import annotations

import os
from typing import Any, Callable, NoReturn

__all__ = [
    "DegismezHatasi",
    "AYRINTILI_DOGRULAMA",
    "dogrula",
    "dogrula_ayrintili",
    "asla",
]


class DegismezHatasi(RuntimeError):
    """Bir değişmez kırıldı. Koşu geçersizdir."""


# Sıcak yoldaki pahalı kontroller yalnızca bu açıkken koşar.
# Varsayılan AÇIK: bir korumanın varsayılan olarak kapalı olması, kapalı
# olduğunu unutmanın en kolay yoludur.
AYRINTILI_DOGRULAMA: bool = os.environ.get("SIM2_AYRINTILI", "1") != "0"


def dogrula(kosul: Any, mesaj: str) -> None:
    """Değişmezi kontrol eder; kırıksa `DegismezHatasi` fırlatır.

    `mesaj` çağrı anında değil, **yalnızca kırıldığında** biçimlendirilmeli:
        dogrula(a >= b, f"...")     # f-string her çağrıda kurulur — YAVAŞ
        dogrula(a >= b, "a < b")    # sabit dizgi — ucuz
    Değişken içeren mesaj gerekiyorsa `asla()` kullan.
    """
    if not kosul:
        raise DegismezHatasi(mesaj)


def dogrula_ayrintili(kosul_uretici: Callable[[], Any], mesaj: str) -> None:
    """Pahalı değişmez — yalnızca `AYRINTILI_DOGRULAMA` açıkken koşar.

    Koşul bir **fonksiyon** olarak alınır ki kapalıyken hiç hesaplanmasın.
    """
    if AYRINTILI_DOGRULAMA and not kosul_uretici():
        raise DegismezHatasi(mesaj)


def asla(mesaj: str) -> NoReturn:
    """Ulaşılamaz olması gereken dal. Ulaşıldıysa değişmez kırılmıştır."""
    raise DegismezHatasi(f"ulaşılamaz dal: {mesaj}")
