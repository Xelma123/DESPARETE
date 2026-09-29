"""A4 (K-177) — dört hızın PER eşikleri ve tek bağda ARF'nin seçtiği hız.

1) PER %10 ve %50 için gereken SNR (22 MHz, NF 7, 576 B'lık veri çerçevesi)
   — bizim `Kanal.kahin_per`imiz (CCK: SEP₁₆ tablosu).
2) CCK SEP₁₆ tablosu ↔ doğrudan integral (ns-3 GSL formu).
3) Tek bağ, sabit SNR: ARF'ye her denemede Bernoulli(1 − PER(hız, SNR))
   sonucu verilir; 3000 denemede ortalama hız ve 11 Mb/s payı.

Kullanım:
    PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python \
        arsiv/teshis/a4_hiz_uyarlamasi_2026-09-26/esikler.py
"""
import math
import random
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.cekirdek.rng import Akislar  # noqa: E402
from sim2.dunya.topoloji import topoloji_kur  # noqa: E402
from sim2.kanal.cerceve import cerceve_kur  # noqa: E402
from sim2.kanal.kanal import Kanal, sep16  # noqa: E402
from sim2.mac.hiz import Arf  # noqa: E402
from sim2.yapilandirma.konfig import HIZLAR_BPS, Konfig  # noqa: E402


def esik_db(per_fn, hedef):
    alt, ust = -20.0, 40.0
    for _ in range(80):
        orta = 0.5 * (alt + ust)
        if per_fn(10.0 ** (orta / 10.0)) > hedef:
            alt = orta
        else:
            ust = orta
    return 0.5 * (alt + ust)


if __name__ == "__main__":
    k = Konfig(kol="a4", islem_kazanci=True, bant_genisligi_hz=22e6,
               gurultu_figuru_db=7.0, hiz_uyarlamasi=True)
    kanal = Kanal(k, topoloji_kur(k, Akislar(1)))
    cer = {h: cerceve_kur(k, "veri", bayt=k.paket_bayt + 64 - 64, hiz_bps=h)
           for h in HIZLAR_BPS}
    gurultu = 10 * math.log10(kanal.yayilim.gurultu_w * 1e3)
    print(f"1) PER eşikleri ({cer[1e6].bayt} B; gürültü {gurultu:.2f} dBm)")
    for h in HIZLAR_BPS:
        e10 = esik_db(lambda s: kanal.kahin_per(cer[h], s), 0.1)
        e50 = esik_db(lambda s: kanal.kahin_per(cer[h], s), 0.5)
        print(f"   {h / 1e6:>4} Mb/s ({cer[h].govde_modulasyonu:<5} ×"
              f"{cer[h].govde_ebn0_carpani:g}) PER %10: {e10:6.2f} dB → "
              f"duyarlılık {gurultu + e10:6.1f} dBm · PER %50: {e50:6.2f} dB")
    print("2) SEP₁₆ tablo ↔ doğrudan integral")
    from scipy.integrate import quad
    from scipy.special import ndtr
    import numpy as np
    for e in (0.01, 0.3, 1.0, 3.0, 8.0, 15.0):
        b = math.sqrt(2 * e)
        ic = quad(lambda x: (2 * ndtr(x + b) - 1) ** 7 * math.exp(-x * x / 2)
                  / math.sqrt(2 * math.pi), -b, math.inf)[0]
        print(f"   e={e:<5} tablo {float(sep16(np.array([e]))[0]):.6e} · "
              f"doğrudan {1 - ic:.6e}")
    print("3) tek bağ, ARF (3000 deneme)")
    for snr_db in (-2.0, 2.0, 6.0, 10.0, 14.0):
        s = 10 ** (snr_db / 10)
        a, r = Arf(HIZLAR_BPS, 10, 15), random.Random(1)
        toplam, en_ust = 0.0, 0
        for _ in range(3000):
            h = a.hiz(1)
            toplam += h
            en_ust += h == 11e6
            if r.random() >= kanal.kahin_per(cer[h], s):
                a.basarili(1)
            else:
                a.basarisiz(1)
        print(f"   SNR {snr_db:5.1f} dB → ortalama hız {toplam / 3000 / 1e6:5.2f}"
              f" Mb/s · 11 Mb/s payı {en_ust / 3000:.2f}")
