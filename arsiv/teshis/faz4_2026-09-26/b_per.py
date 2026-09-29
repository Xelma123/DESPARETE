"""4.2 · PER eğrileri referans dünyada — yayımlanmış değerlerle karşılaştırma.

Hız başına duyarlılık (PER %8 ve %10; 1024 B ve simülatörün veri çerçevesi),
referans gürültüsüyle dBm'e çevrilir ve iki dış çapayla karşılaştırılır:
  · G2 (Boer 1996, IEEE 802.11 DSSS): alt sınır −80 dBm, FER %8, 1024 B
  · G1 (Pei & Henderson 2009): CMU Prism 2.5 ölçümü ≈ −94 … −100 dBm;
    modelin 1 Mb/s eğrisi ölçümden ~2 dB sağda (kötümser)
Kod değiştirmez; yalnız okur.

    PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
        python arsiv/teshis/faz4_2026-09-26/b_per.py
"""
import pathlib
import sys
from dataclasses import replace

KOK = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KOK))

from sim2.kanal.cerceve import cerceve_kur  # noqa: E402
from sim2.kanal.dunya import referans_2026, snr_esigi_db  # noqa: E402
from sim2.kanal.kanal import cerceve_per  # noqa: E402
from sim2.kanal.yayilim import Yayilim, lin_to_db  # noqa: E402
from sim2.yapilandirma.konfig import HIZLAR_BPS  # noqa: E402

if __name__ == "__main__":
    k = referans_2026(kol="per")
    gurultu_dbm = lin_to_db(Yayilim(k).gurultu_w * 1e3)
    print(f"gurultu {gurultu_dbm:.2f} dBm (22 MHz, NF {k.gurultu_figuru_db} dB)")
    print(f"{'hiz':>6} {'bayt':>5} {'SNR PER8%':>10} {'duyarlilik':>11} "
          f"{'SNR PER10%':>11} {'duyarlilik':>11}")
    for hiz in HIZLAR_BPS:
        for bayt in (1024, k.paket_bayt):
            kb = replace(k, paket_bayt=bayt)
            c = cerceve_kur(kb, "veri", hiz_bps=hiz)
            s8 = snr_esigi_db(lambda s: cerceve_per(c, s), 0.08)
            s10 = snr_esigi_db(lambda s: cerceve_per(c, s), 0.10)
            print(f"{hiz / 1e6:>5.1f}M {bayt:>5} {s8:>9.2f}dB "
                  f"{gurultu_dbm + s8:>9.1f}dBm {s10:>10.2f}dB "
                  f"{gurultu_dbm + s10:>9.1f}dBm")
    print("dis capalar: G2 alt sinir -80 dBm (FER %8, 1024 B) · "
          "G1 CMU Prism 2.5 ~ -94 ... -100 dBm")
