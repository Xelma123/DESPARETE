"""
Beacon ve komşu tablosu teşhisi + koşu maliyeti.

İki soru:
  1. Beacon mekanizması gerçekten çalışıyor mu — komşu tabloları doluyor mu,
     ve karıştırma altında KOMŞU KAYBOLUYOR mu?
  2. Beacon'ların getirdiği olay yükü koşu süresini ne kadar artırdı?

İkincisi önemli: ana matris 6 senaryo × 3 trafik × 30 tohum = 540 koşu.
Koşu başına süre birkaç kat artarsa matris 30 dakikayı aşar ve izin gerekir.
"""

from __future__ import annotations

import statistics as ist
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dogrulama.aktaricilar import en_kisa_yol, gurultuden_kacan  # noqa: E402
from sim.config import SENARYOLAR, Konfig  # noqa: E402
from dogrulama.olcum import kayit, olc  # noqa: E402


def main() -> None:
    print("=" * 78)
    print("BEACON MEKANİZMASI — komşuluk gerçekten öğreniliyor mu?")
    print("=" * 78)
    print(f"{'senaryo':>8} {'beacon gön.':>12} {'alınan':>9} {'kaçırılan':>10} "
          f"{'ort komşu':>10} {'geometrik':>10} {'süre s':>8}")
    print("-" * 78)

    sureler = []
    for sen in SENARYOLAR:
        t0 = time.perf_counter()
        s = olc(Konfig(kol="teshis", senaryo=sen, tohum=1), en_kisa_yol,
                adim="beacon", senaryo=sen)
        sure = time.perf_counter() - t0
        sureler.append(sure)
        print(f"{sen:>8} {s['beacon_gonderilen']:>12} {s['beacon_alinan']:>9} "
              f"{s['beacon_kacirilan']:>10} {s['ort_komsu_sayisi']:>10.2f} "
              f"{s['topoloji']['ortalama_derece']:>10.2f} {sure:>8.2f}")

    print()
    print("  Beklenen: S0'da öğrenilen komşu ≈ geometrik derece.")
    print("  Karıştırma arttıkça öğrenilen komşu DÜŞMELİ — beacon da kaybolur.")

    print()
    print("=" * 78)
    print("KOŞU MALİYETİ")
    print("=" * 78)
    ort = ist.mean(sureler)
    n = 6 * 3 * 30
    dk10 = n * ort / 10 / 60
    print(f"  koşu başına ortalama  : {ort:.2f} s")
    print(f"  540 koşu, tek çekirdek: {n*ort/60:.1f} dk")
    print(f"  540 koşu, 10 çekirdek : {dk10:.1f} dk"
          f"   {'⚠️ 30 dk sınırı aşılıyor — izin gerek' if dk10 > 30 else '✅'}")

    print()
    print("=" * 78)
    print("SAF GÖZLEM PROTOKOLÜ ÇALIŞIYOR MU?")
    print("=" * 78)
    print("  (kâhin bilgi kullanmayan `gurultuden_kacan` ile)")
    for sen in ("S0", "S2"):
        s = olc(Konfig(kol="teshis", senaryo=sen, tohum=1),
                gurultuden_kacan, adim="gozlem",
                senaryo=sen)
        print(f"  {sen}: teslim {s['teslim_orani']:.4f}  "
              f"hedef_yok {s['hedef_yok']:6d}  ttl {s['ttl_olumu']:5d}  "
              f"korunum {s['korunum_tamam']}")
    print()
    print("  Not: bu protokol kötü olabilir — önemli olan KOŞABİLMESİ,")
    print("       yani gözlem penceresinin bir protokol yazmaya YETMESİ.")


if __name__ == "__main__":
    with kayit("beacon_teshis"):
        main()
