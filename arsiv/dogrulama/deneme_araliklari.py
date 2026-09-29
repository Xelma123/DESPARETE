"""
ARDIŞIK İLETİM ARALIKLARI — kanal dilimi yeterli mi (K-024 · B-108).

🔴 NEDEN BU ARAÇ VAR
====================
K-024 *(19 Ağustos 2026)* `kanal_dilimi_s = 100 µs` seçimini şu ölçümle
savundu: *"ardışık deneme başlangıçları arası 9528–18068 µs; 1 ms dilimde
bile çakışma HİÇ olmuyordu."*

Altıncı denetim (B-108) bu sayının **bugün üretilemediğini** ölçtü. Ve
kaydın kendisinde daha derin bir sorun vardı:

🔴 **ÖLÇÜM TEK BİR MESAJIN 7 DENEMESİNDEN, YANİ n = 6 ARALIKTAN ÇIKMIŞTI.**
`03` Y4: *"tek noktada tutan sonuç doğrulama sayılmaz."*

🔴 VE SORU DAR SORULMUŞTU
==========================
`kanal_cekimi` anahtarı `(gonderen, alan, dilim)`. Yani **aynı bağdaki
HERHANGİ İKİ İLETİM** aynı dilime düşerse **aynı çekimi paylaşır** —
yalnızca aynı mesajın yeniden denemeleri değil. K-024 yalnızca yeniden
denemeleri saymıştı; mekanizmanın kapsadığı popülasyon daha geniş.

ÖLÇÜLDÜ — 27 Ağustos 2026, 4 yapılandırma, **54 463 ardışık çift**:

    min 124 µs · ortanca 19 292 µs · maks 55 180 560 µs
    9 528 µs altında  : %14,96      18 068 µs üstünde : %52,93
    ------------------------------------------------------------
    100 µs dilimde çakışan çift : 🟢  0
      1 ms dilimde çakışan çift : 🔴 14

⚖️ **ARALIK RAKAMI BAYAT; KARAR DAHA GÜÇLÜ.** Seçilen 100 µs, K-024'ün
gerekçesinde yazdığından **daha gerekliydi**: geniş popülasyonda 1 ms
yetmiyor.

⚠️ KAPSAMI (Y11):
| vaka                                                | görülür mü |
| aynı bağdaki ardışık VERİ çerçeveleri               | ✅ evet    |
| onay / beacon çerçeveleri                           | ❌ hayır (yeniden deneme üretmezler) |
| 🔴 koşulmayan bir yapılandırmadaki aralıklar        | ❌ **HAYIR** |

Kullanım:
    python dogrulama/deneme_araliklari.py
"""

from __future__ import annotations

import statistics
import sys
from collections import defaultdict
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK))

import sim.mac as M                                             # noqa: E402
from sim.config import Konfig                                   # noqa: E402
from dogrulama.aktaricilar import AKTARICILAR                   # noqa: E402
from dogrulama.olcum import olc                                 # noqa: E402

YAPILANDIRMALAR = (("S2", 1), ("S2", 2), ("S4", 9), ("S5", 4))

# 🔒 ÖLÇÜLDÜ 27 Ağustos 2026 — yukarıdaki matriste.
#
# ⚠️ `min_us` bir ÖLÇÜLEN büyüklüktür ve **1 µs toleransla** karşılaştırılır.
# Bit-birebir pinlemek onu KIRILGAN yapardı: `sim/` altındaki ilgisiz her
# değişiklik aracı düşürür ve araç gürültüye dönerdi. Sayımlar (`cift`,
# `cakisma_*`) ise TAM karşılaştırılır — asıl iddiayı onlar taşıyor.
BEYAN = {"cift": 54_463, "min_us": 123.98, "cakisma_100us": 0,
         "cakisma_1ms": 14}
MIN_TOLERANS_US = 1.0


def olc_araliklar(yapilandirmalar=YAPILANDIRMALAR) -> list[float]:
    """Aynı `(gönderen, alan)` bağındaki ardışık VERİ başlangıçları (µs).

    🔴 Y7 — sarmalama `try/finally` ile geri alınır; araç ölçtüğü şeyi bozamaz.
    """
    denemeler: dict[tuple[int, int], list[float]] = defaultdict(list)
    asil = M.KanalErisimi._iletim_basla

    def izle(self, il):
        if il.tur == "veri":
            denemeler[(il.gonderen, il.alan)].append(il.baslangic_s)
        return asil(self, il)

    try:
        M.KanalErisimi._iletim_basla = izle
        for sen, toh in yapilandirmalar:
            olc(Konfig(kol="t", senaryo=sen, tohum=toh),
                AKTARICILAR["en_kisa_yol"])
    finally:
        M.KanalErisimi._iletim_basla = asil

    araliklar: list[float] = []
    for zamanlar in denemeler.values():
        zamanlar.sort()
        araliklar += [(b - a) * 1e6 for a, b in zip(zamanlar, zamanlar[1:])]
    return sorted(araliklar)


def main() -> int:
    print("=" * 78)
    print("ARDIŞIK İLETİM ARALIKLARI — kanal dilimi yeterli mi (K-024 · B-108)")
    print("=" * 78)
    a = olc_araliklar()
    n = len(a)
    if not n:
        print("🔴 hiç aralık ölçülmedi — kurulum bozuk (Y7)")
        return 1

    print(f"  ardışık çift              : {n}")
    print(f"  min / ortanca / maks (µs) : {a[0]:.0f} / "
          f"{statistics.median(a):.0f} / {a[-1]:.0f}")
    print(f"  K-024'ün 9 528'i altında  : {sum(1 for x in a if x < 9528)}"
          f"  (%{100*sum(1 for x in a if x < 9528)/n:.2f})")
    print(f"  K-024'ün 18 068'i üstünde : {sum(1 for x in a if x > 18068)}"
          f"  (%{100*sum(1 for x in a if x > 18068)/n:.2f})")
    print()
    kon = Konfig(kol="t")
    for dilim_us, ad in ((kon.kanal_dilimi_s * 1e6, "bugünkü dilim"),
                         (1000.0, "1 ms — K-024'ün elediği")):
        cak = sum(1 for x in a if x < dilim_us)
        isaret = "🟢" if cak == 0 else "🔴"
        print(f"  {isaret} {ad:<26} ({dilim_us:.0f} µs) çakışan çift: {cak}")

    print()
    olculen = {"cift": n, "min_us": a[0],
               "cakisma_100us": sum(1 for x in a if x < kon.kanal_dilimi_s * 1e6),
               "cakisma_1ms": sum(1 for x in a if x < 1000.0)}
    ayrik = {k: (BEYAN[k], v) for k, v in olculen.items()
             if k != "min_us" and BEYAN[k] != v}
    if abs(olculen["min_us"] - BEYAN["min_us"]) > MIN_TOLERANS_US:
        ayrik["min_us"] = (BEYAN["min_us"], olculen["min_us"])
    if ayrik:
        print(f"  🔴 BEYAN AYRIŞTI (beyan, ölçülen): {ayrik}")
        print("     `BEYAN`, `sim/config.py` yorumu ve `04` K-024 revizyonu "
              "GÜNCELLENMELİ (Y14).")
        return 1
    print("  ✅ beyan ölçümle birebir")
    return 0


if __name__ == "__main__":
    # Koşuları TEMİZ (yalnızca `_iletim_basla` sarmalanır, sonuç
    # sözlüğü etkilenmez) — satırlar yazılır.
    from dogrulama.olcum import kayit
    with kayit("deneme_araliklari"):
        raise SystemExit(main())
