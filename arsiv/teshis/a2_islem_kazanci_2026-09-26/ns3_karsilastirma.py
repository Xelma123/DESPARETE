"""A2 (K-173) kapısı — PER–SINR eğrisi ns-3 `DsssErrorRateModel` ile.

ns-3 formülleri depodaki kopyadan (`protokol_kaynaklari/uygulama_kaynaklari/
ns-3/dsss-error-rate-model.cc`, satır 34–57) birebir yazıldı:
  DBPSK 1 Mb/s : EbN0 = SINR·22 ; BER = ½·e^(−EbN0)
  DQPSK 2 Mb/s : EbN0 = SINR·11 ; BER = (√2+1)/√(8π√2) · x^(−½) · e^(−(2−√2)x)
Bizimki: `Kanal.per`/`onbelge_per`, işlem kazancı AÇIK, B = 22 MHz.

Kullanım:
    PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python \
        arsiv/teshis/a2_islem_kazanci_2026-09-26/ns3_karsilastirma.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.cekirdek.rng import Akislar  # noqa: E402
from sim2.dunya.topoloji import topoloji_kur  # noqa: E402
from sim2.kanal.cerceve import cerceve_kur  # noqa: E402
from sim2.kanal.kanal import Kanal  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402


def ns3_dqpsk_ber(x: float) -> float:
    return ((math.sqrt(2) + 1.0) / math.sqrt(8.0 * math.pi * math.sqrt(2))
            * (1.0 / math.sqrt(x)) * math.exp(-(2.0 - math.sqrt(2)) * x))


def ns3_per_govde(sinr: float, nbit: int) -> float:
    ber = min(ns3_dqpsk_ber(sinr * 22e6 / 1e6 / 2.0), 1.0)
    return 1.0 - (1.0 - ber) ** nbit


def ns3_per_onbelge(sinr: float, nbit: int) -> float:
    ber = 0.5 * math.exp(-sinr * 22e6 / 1e6)
    return 1.0 - (1.0 - ber) ** nbit


def esik_db(per_fn, hedef: float) -> float:
    """PER = hedef olan SINR (dB) — ikiye bölme (PER SINR'da azalan)."""
    alt, ust = -20.0, 30.0
    for _ in range(80):
        orta = 0.5 * (alt + ust)
        if per_fn(10.0 ** (orta / 10.0)) > hedef:
            alt = orta
        else:
            ust = orta
    return 0.5 * (alt + ust)


def main() -> None:
    k = Konfig(kol="a2", senaryo="statik-yok", islem_kazanci=True,
               bant_genisligi_hz=22e6, gurultu_figuru_db=7.0)
    kanal = Kanal(k, topoloji_kur(k, Akislar(1)))
    kapali = Konfig(kol="a2", senaryo="statik-yok")
    kanal0 = Kanal(kapali, topoloji_kur(kapali, Akislar(1)))
    c = cerceve_kur(k, "veri")
    c0 = cerceve_kur(kapali, "veri")
    n, nb = c.hataya_acik_bit, c.onbelge_bit
    print(f"veri çerçevesi: gövde {n} bit (DQPSK 2 Mb/s) · önbelge {nb} bit "
          f"(DBPSK 1 Mb/s) · çarpan gövde ×{c.govde_ebn0_carpani:g} · "
          f"önbelge ×{c.onbelge_ebn0_carpani:g}")
    gurultu_dbm = 10 * math.log10(kanal.yayilim.gurultu_w * 1e3)
    print(f"gürültü tabanı (22 MHz, NF 7, 290 K): {gurultu_dbm:.2f} dBm")
    print("\nPER hedefi → SINR eşiği (dB):  bizim (açık) · ns-3 · fark · "
          "bizim (KAPALI)")
    for hedef in (0.9, 0.5, 0.1, 0.01):
        b = esik_db(lambda s: kanal.kahin_per(c, s), hedef)
        n3 = esik_db(lambda s: ns3_per_govde(s, n), hedef)
        b0 = esik_db(lambda s: kanal0.kahin_per(c0, s), hedef)
        print(f"  gövde   PER {hedef:<5} {b:7.3f} · {n3:7.3f} · {b - n3:+.3f} "
              f"· {b0:7.3f}")
    for hedef in (0.5, 0.1, 0.01):
        b = esik_db(lambda s: kanal.onbelge_per(c, ((float(nb), s),)), hedef)
        n3 = esik_db(lambda s: ns3_per_onbelge(s, nb), hedef)
        print(f"  önbelge PER {hedef:<5} {b:7.3f} · {n3:7.3f} · {b - n3:+.3f}")
    # 2 Mb/s duyarlılığı: PER %10'daki alınan güç = gürültü + eşik
    s10 = esik_db(lambda s: kanal.kahin_per(c, s), 0.1)
    print(f"\n2 Mb/s duyarlılığı (PER %10, {c.bayt} B): "
          f"{gurultu_dbm + s10:.1f} dBm")


if __name__ == "__main__":
    main()
