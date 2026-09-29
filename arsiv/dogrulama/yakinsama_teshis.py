"""
Yakınsama kapısının (K5) senaryo bazında kırılımı.

Ç1 koşusunda 77/540 koşu "yakınsamadı" işaretlendi. Bu betik hangi
senaryodan geldiğini ve sebebinin öğrenme mi ortam mı olduğunu ayırır.

⚠️ Windows'ta multiprocessing yalnızca gerçek bir dosyadan çalışır; çocuk
süreçler `__main__`i yeniden içe aktarır. Bu yüzden ayrı dosya.
"""

from __future__ import annotations

import math
import statistics as ist
import sys
from multiprocessing import Pool
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dogrulama.kapi_korunum import KAPI_TOHUMLARI, _kosu  # noqa: E402
from sim.config import SENARYOLAR, Konfig  # noqa: E402


def main() -> None:
    isler = [(s, "orta", t, "en_kisa_yol", {})
             for s in SENARYOLAR for t in KAPI_TOHUMLARI]
    with Pool(10) as p:
        r = p.map(_kosu, isler)

    print("Yakınsama, senaryo bazında (orta trafik, 30 tohum):")
    print(f"{'senaryo':>8} {'yakınsamayan':>14} {'ort dilim farkı':>17} "
          f"{'teslim ort':>11} {'teslim std':>11}")
    print("-" * 68)
    for s in SENARYOLAR:
        g = [x for x in r if x["senaryo"] == s]
        yk = sum(1 for x in g if x["yakinsadi"] is False)
        print(f"{s:>8} {yk:>9}/{len(g):<4} "
              f"{ist.mean(x['en_buyuk_fark'] for x in g):>17.4f} "
              f"{ist.mean(x['teslim_orani'] for x in g):>11.4f} "
              f"{ist.stdev(x['teslim_orani'] for x in g):>11.4f}")

    kon = Konfig(kol="x", senaryo="S5")
    cevre = 2 * math.pi * kon.karistirici_yorunge_yaricap_m
    periyot = cevre / kon.karistirici_hiz_ms
    pencere = kon.olcum_bitis_s - kon.isinma_s
    print()
    print("S5 (hareketli karıştırıcı) geometrisi:")
    print(f"  yörünge periyodu       : {periyot:.1f} s")
    print(f"  ölçüm penceresi        : {pencere:.0f} s")
    print(f"  pencere / periyot      : {pencere / periyot:.3f}  "
          f"{'← TAM SAYI DEĞİL' if abs(pencere/periyot - round(pencere/periyot)) > 0.05 else ''}")
    print(f"  bir dilim (pencere/3)  : {pencere/3:.0f} s = "
          f"{pencere/3/periyot:.3f} yörünge")
    print()
    print("  Yorum: dilimler farklı yörünge fazlarını görüyorsa dilim farkı")
    print("  ÖĞRENME yakınsamasından değil ORTAMDAN gelir.")

    print()
    print("S3/S4 (darbeli) geometrisi:")
    print(f"  darbe periyodu         : {kon.darbe_periyodu_s:.2f} s")
    print(f"  pencere / periyot      : {pencere / kon.darbe_periyodu_s:.1f} periyot")
    print(f"  bir dilim              : {pencere/3/kon.darbe_periyodu_s:.1f} periyot"
          f"  → çok sayıda periyot, ortalama kararlı olmalı")


if __name__ == "__main__":
    main()
