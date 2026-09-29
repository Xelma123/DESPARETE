"""
B-03 DOĞRULAMASI — K-026 örtüşme yarattı mı?

Denetçi iddia ediyor: karıştırıcı yörünge periyodunu yakınsama dilimine tam
eşitlemek, faz kaynaklı varyansı BASTIRIYOR — yani K-026'nın "örtüşme riski
değil, yalnızca yanlılık kalkıyor" savunması yanlış.

Bunu bir başkasının raporundan kabul etmiyorum; kendim ölçüyorum.

DENEY: topoloji, trafik ve tohum SABİT; yalnızca karıştırıcı fazı taranıyor.
Faz kaynaklı varyans hizalı ve hizasız periyotta karşılaştırılıyor.

Eğer hizalı ayarda varyans belirgin biçimde küçükse, `03` B6'nın örtüşme
tanımı gerçekleşmiş demektir: "örnekler kilitlenir ve tohumlar arası varyans
YAPAY olarak sıfıra iner."
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
from sim.radio import Karistirici  # noqa: E402


def faz_taramasi(hiz_ms: float, fazlar: int = 16, tohum: int = 1) -> dict:
    """Aynı tohum, aynı topoloji, aynı trafik — yalnızca karıştırıcı fazı değişir."""
    teslimler, dilim_farklari = [], []
    for i in range(fazlar):
        faz = i / fazlar
        kon = Konfig(kol="b03", senaryo="S5", tohum=tohum,
                     karistirici_hiz_ms=hiz_ms)
        # Fazı elle sabitle — akıştan gelen rastgele fazı geçersiz kıl.
        # 🔴 `hazirla` kâhin kapısıdır ve `olcum.py`de beyan edilmiştir.
        def _faz_sabitle(k, faz=faz):
            k.karistirici = replace(k.karistirici, faz_kesri=faz)
            k.mac.karistirici = k.karistirici
        s = olc(kon, en_kisa_yol, hazirla=_faz_sabitle)
        teslimler.append(s["teslim_orani"])
        dilim_farklari.append(s["yakinsama"]["en_buyuk_fark"])
    return {
        "teslim_std": ist.stdev(teslimler),
        "teslim_aralik": max(teslimler) - min(teslimler),
        "ort_dilim_farki": ist.mean(dilim_farklari),
    }


def main() -> None:
    kon = Konfig(kol="b03", senaryo="S5")
    dilim = (kon.olcum_bitis_s - kon.isinma_s) / 3.0
    r = kon.karistirici_yorunge_yaricap_m

    print("=" * 74)
    print("B-03 DOĞRULAMASI — yörünge/dilim hizalaması örtüşme yaratıyor mu?")
    print("=" * 74)
    print(f"Yakınsama dilimi: {dilim:.1f} s")
    print(f"Sevk edilen hız : {kon.karistirici_hiz_ms:.4f} m/s "
          f"→ periyot {2*math.pi*r/kon.karistirici_hiz_ms:.2f} s\n")

    print(f"{'periyot':>9} {'hız m/s':>9} {'per/dilim':>10} "
          f"{'teslim std':>12} {'aralık':>9} {'dilim farkı':>12}")
    print("-" * 74)

    for periyot in (90.0, 70.0, 115.0, 125.66):
        hiz = 2 * math.pi * r / periyot
        s = faz_taramasi(hiz)
        oran = periyot / dilim
        isaret = "  ← SEVK EDİLEN" if abs(periyot - 90.0) < 0.1 else ""
        print(f"{periyot:>9.2f} {hiz:>9.3f} {oran:>10.4f} "
              f"{s['teslim_std']:>12.5f} {s['teslim_aralik']:>9.4f} "
              f"{s['ort_dilim_farki']:>12.4f}{isaret}")

    print()
    print("YORUM ÖLÇÜTÜ (sonuç görülmeden yazıldı):")
    print("  Hizalı ayarda teslim std belirgin KÜÇÜKSE → faz varyansı")
    print("  bastırılmış, yani `03` B6'nın örtüşmesi gerçekleşmiş.")
    print("  K-026'nın 'varyans kaynağı duruyor' savunması o durumda YANLIŞ.")


if __name__ == "__main__":
    main()
