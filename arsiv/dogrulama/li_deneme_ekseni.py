"""
K-028 adayı #1 — yeniden deneme sınırı, 30 tohumla.

Duyarlılık taraması 5 tohumla koşulmuştu ve yeniden deneme ekseninde gözlenen
fark (1/6,17 → 1/6,34) GÜVEN ARALIĞININ İÇİNDEYDİ. Yani "etkisiz" demek fazla
iddia olurdu; ölçüm ayırt edecek kadar keskin değildi.

Bu betik aynı ekseni 30 tohumla, EŞLEŞTİRİLMİŞ olarak koşar: aynı tohum her
üç ayarda da aynı topolojiyi ve aynı kanal gerçeklemesini görür, dolayısıyla
fark yalnızca yeniden deneme sınırından gelir.

Soru: ns-2'nin değeri (7) ile bizimki (4) arasındaki fark, Li ile aramızdaki
1/6,30 vs 1/7 açığını açıklayabilir mi?
"""

from __future__ import annotations

import statistics as ist
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dogrulama.li_duyarlilik import PLATO_ATLAMA, plato_olc  # noqa: E402

TOHUMLAR = range(1, 31)
DEGERLER = (2, 4, 7)


def main() -> None:
    print("=" * 72)
    print("K-028 ADAYI #1 — yeniden deneme sınırı, 30 tohum")
    print("=" * 72)
    print(f"{'sınır':>8} {'plato':>10} {'1/x':>8} {'%95 GA':>22} {'GA gen.%':>10}")
    print("-" * 72)

    sonuclar = {}
    for v in DEGERLER:
        s = plato_olc(TOHUMLAR, yeniden_deneme_siniri=v)
        sonuclar[v] = s
        not_ = "  ← bizim" if v == 4 else ("  ← ns-2" if v == 7 else "")
        print(f"{v:>8} {s['oran']:>10.4f} {s['ters']:>8.2f} "
              f"[{s['ga'][0]:.4f}, {s['ga'][1]:.4f}] {s['ga_genislik_yuzde']:>9.2f}"
              f"{not_}")

    a, b = sonuclar[4], sonuclar[7]
    ortusuyor = not (a["ga"][1] < b["ga"][0] or b["ga"][1] < a["ga"][0])
    fark_yuzde = 100 * (a["oran"] - b["oran"]) / a["oran"]

    print()
    print(f"  4 → 7 farkı        : {fark_yuzde:+.2f} %")
    print(f"  GA'lar örtüşüyor mu: {ortusuyor}")
    print()
    print("  Li açığı için gereken değişim:")
    hedef = 1 / 7
    gereken = 100 * (a["oran"] - hedef) / a["oran"]
    print(f"    1/{a['ters']:.2f} → 1/7 için {gereken:+.1f} % gerekiyor")
    print()
    if abs(fark_yuzde) < abs(gereken) / 2:
        print("  🔴 SONUÇ: yeniden deneme sınırı Li açığını AÇIKLAYAMAZ.")
        print("     Etkisi, gereken değişimin yarısından küçük.")
    else:
        print("  ⚠️ SONUÇ: yeniden deneme sınırı açığın kayda değer bir")
        print("     kısmını açıklıyor olabilir; rapora öyle yazılır.")


if __name__ == "__main__":
    main()
