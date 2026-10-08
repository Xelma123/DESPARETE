"""
Teşhis sözleşmesi — protokolün `teshis()` kancasından dönenin denetimi.

🔒 DENETLENEREK TAŞINDI (eski `sim/gozlem.py`den, 4 Eylül 2026)
==============================================================
🔴 NEDEN VAR: eski depoda `teshis` kancası açılırken *"`beacon_yuku`nun
deseniyle birebir aynı"* denmişti. Değildi — `beacon_yuku` `yuk_bayt`tan
geçiyordu, `teshis` **hiçbir denetimden geçmiyordu**. Bağımsız bir denetim
sekiz sözleşme dışı yük denedi: **sekizi de kabul edildi**, dördü sonuç
yazıcısını koşu BİTTİKTEN SONRA ham bir hatayla düşürdü — o noktada koşu
zaten harcanmıştır. Biri yasak tiplerden bir `Konfig` örneğini sonuç
sözlüğüne taşıdı.

🔴 NaN REDDİ AYRI BİR KAPIDIR
=============================
Tip denetimi NaN'ı KAÇIRIR: `nan` da bir `float`tır. Tek bir NaN ortalamayı
ve Holm–Bonferroni ile düzeltilmiş p'lerin tümünü bozar. Gecikme kanalında
zaten reddediliyordu; teşhis kanalı da reddetmeli, yoksa aynı zehir başka
kapıdan girer.
"""

from __future__ import annotations

import math

__all__ = ["TESHIS_EN_UZUN_AD_BAYT", "TESHIS_EN_UZUN_DIZGI_BAYT",
           "TESHIS_EN_COK_ALAN", "TESHIS_EN_COK_ELEMAN",
           "TeshisHatasi", "teshis_dogrula"]


TESHIS_EN_UZUN_AD_BAYT = 64      # sayaç adı; sonuç şemasında anahtar olur
TESHIS_EN_UZUN_DIZGI_BAYT = 256  # dizgi değerler
TESHIS_EN_COK_ALAN = 32          # düğüm başına sayaç
TESHIS_EN_COK_ELEMAN = 64        # demet/liste uzunluğu


class TeshisHatasi(ValueError):
    """Protokolün `teshis` kancasından dönen veri sözleşmeye uymuyor."""


def _teshis_deger_dogrula(ad: str, deger, derinlik: int = 0) -> None:
    if isinstance(deger, bool):
        return
    if isinstance(deger, (int, float)):
        # 🔴 Y11 — TİP denetimi bunu KAÇIRIR: `nan` da bir `float`tır.
        # `03` B2: *"NaN'ın sessizce zehirlemesi"* — tek bir NaN, ortalamayı
        # ve düzeltilmiş p'lerin tümünü bozar. `karsilastirma.py` gecikmelerde
        # zaten reddediyor (B-67); teşhis kanalı da reddetmeli, yoksa aynı
        # zehir başka kapıdan girer.
        if isinstance(deger, float) and not math.isfinite(deger):
            raise TeshisHatasi(
                f"{ad!r}: {deger!r} — sonlu olmayan sayı taşınamaz. "
                f"`03` B2: tek bir NaN düzeltilmiş p'lerin tümünü 1,00 yapar.")
        return
    if isinstance(deger, str):
        if len(deger.encode("utf-8")) > TESHIS_EN_UZUN_DIZGI_BAYT:
            raise TeshisHatasi(
                f"{ad!r}: dizgi değer {len(deger.encode('utf-8'))} bayt, "
                f"en çok {TESHIS_EN_UZUN_DIZGI_BAYT}")
        return
    if isinstance(deger, (tuple, list)) and derinlik == 0:
        if len(deger) > TESHIS_EN_COK_ELEMAN:
            raise TeshisHatasi(
                f"{ad!r}: {len(deger)} elemanlı dizi, en çok "
                f"{TESHIS_EN_COK_ELEMAN}. Sonuç şeması teşhis taşır, VERİ değil.")
        for x in deger:
            _teshis_deger_dogrula(ad, x, derinlik + 1)
        return
    raise TeshisHatasi(
        f"{ad!r}: taşınamaz tip {type(deger).__name__}. İzinli: "
        f"bool · int · float · str · bunların düz dizisi. "
        f"(Sonuç sözlüğü JSON'a yazılır; serileştirilemeyen bir değer koşu "
        f"BİTTİKTEN SONRA yazıcıyı düşürür ve koşu harcanmış olur.)")


def teshis_dogrula(dugum: int, veri) -> dict:
    """🔴 `protokol.teshis(dugum)` çıktısının sözleşmesi (B-87).

    `beacon_yuku`nun `yuk_bayt`ı gibi: ihlalde **anında** ve **tipli**
    fırlar. Boş/None kabul edilir ve atlanır.
    """
    if not veri:
        return {}
    if not isinstance(veri, dict):
        raise TeshisHatasi(
            f"düğüm {dugum}: `teshis` bir sözlük döndürmeli, "
            f"{type(veri).__name__} geldi")
    if len(veri) > TESHIS_EN_COK_ALAN:
        raise TeshisHatasi(
            f"düğüm {dugum}: {len(veri)} teşhis alanı, en çok "
            f"{TESHIS_EN_COK_ALAN}")
    for ad, deger in veri.items():
        if not isinstance(ad, str) or not ad:
            raise TeshisHatasi(
                f"düğüm {dugum}: teşhis adı boş olmayan bir DİZGİ olmalı, "
                f"{ad!r} ({type(ad).__name__}) geldi. Sonuç sözlüğü JSON'a "
                f"yazılır ve dizgi olmayan anahtar yazıcıyı düşürür.")
        if len(ad.encode("utf-8")) > TESHIS_EN_UZUN_AD_BAYT:
            raise TeshisHatasi(
                f"düğüm {dugum}: teşhis adı {len(ad.encode('utf-8'))} bayt, "
                f"en çok {TESHIS_EN_UZUN_AD_BAYT}")
        _teshis_deger_dogrula(ad, deger)
    return veri
