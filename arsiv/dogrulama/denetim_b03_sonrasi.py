"""
B-03 DÜZELTMESİ SONRASI — metrik fiziği ayarlamadan işini görüyor mu?

İki soru:
  1. Karıştırıcı hızı 15 m/s'ye döndü. Yörünge-hizalı metrik, S5'te kapıyı
     ateşletmeden çalışıyor mu?
  2. Faz kaynaklı varyans GERİ GELDİ mi? (K-026 onu bastırıyordu; düzeltme
     bastırmayı kaldırmalı, yani varyans eski seviyesine dönmeli.)

🔴 İkincisi kritik: eğer varyans hâlâ bastırılmışsa, metrik düzeltmesi de
örtüşme yaratıyor demektir ve düzeltme işe yaramamıştır.
"""

from __future__ import annotations

import math
import statistics as ist
import sys
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dogrulama.aktaricilar import en_kisa_yol  # noqa: E402
from sim.config import Konfig  # noqa: E402
from dogrulama.olcum import olc  # noqa: E402


def main() -> None:
    kon = Konfig(kol="b03s", senaryo="S5")
    periyot = (2 * math.pi * kon.karistirici_yorunge_yaricap_m
               / kon.karistirici_hiz_ms)
    pencere = kon.olcum_bitis_s - kon.isinma_s

    print("=" * 74)
    print("B-03 DÜZELTMESİ SONRASI")
    print("=" * 74)
    print(f"  karıştırıcı hızı : {kon.karistirici_hiz_ms:.1f} m/s  "
          f"(~{kon.karistirici_hiz_ms*3.6:.0f} km/h)")
    print(f"  yörünge periyodu : {periyot:.2f} s")
    print(f"  ölçüm penceresi  : {pencere:.0f} s = {pencere/periyot:.3f} yörünge")
    print(f"  → metrik {int(pencere//periyot)} TAM TUR kullanacak, "
          f"artan {pencere - int(pencere//periyot)*periyot:.1f} s dışlanacak\n")

    # --- 1) Kapı S5'te ateşliyor mu? -------------------------------------
    print("--- 30 tohum, S5/orta ---")
    yakinsamayan, farklar = 0, []
    for t in range(1, 31):
        s = olc(Konfig(kol="b03s", senaryo="S5", tohum=t), en_kisa_yol)
        y = s["yakinsama"]
        if y["yakinsadi"] is False:
            yakinsamayan += 1
        if y["en_buyuk_fark"] is not None:
            farklar.append(y["en_buyuk_fark"])
    print(f"  dilim gerekçesi   : {y['dilim_gerekcesi']}")
    print(f"  yakınsamayan koşu : {yakinsamayan}/30")
    print(f"  ort. dilim farkı  : {ist.mean(farklar):.4f}")

    # --- 2) Faz varyansı geri geldi mi? ----------------------------------
    print("\n--- faz taraması (topoloji/trafik sabit, yalnız faz) ---")
    teslimler = []
    for i in range(16):
        def _faz_sabitle(k, i=i):
            k.karistirici = replace(k.karistirici, faz_kesri=i / 16)
            k.mac.karistirici = k.karistirici
        teslimler.append(olc(Konfig(kol="b03s", senaryo="S5", tohum=1),
                             en_kisa_yol, hazirla=_faz_sabitle)["teslim_orani"])
    std = ist.stdev(teslimler)
    print(f"  teslim std (yalnız faz) : {std:.5f}")
    print(f"  K-026 hizalı ayarda     : 0,00256  (BASTIRILMIŞ)")
    print(f"  hizasız referans        : 0,00846")
    print()
    if std > 0.005:
        print("  ✅ Faz varyansı GERİ GELDİ — örtüşme kalktı.")
    else:
        print("  🔴 Faz varyansı hâlâ bastırılmış — düzeltme yetersiz.")


if __name__ == "__main__":
    main()
