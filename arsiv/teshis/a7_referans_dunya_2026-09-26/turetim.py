"""A7 (K-178) — referans dünyanın türetilen değerleri.

Kullanım:
    PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python \
        arsiv/teshis/a7_referans_dunya_2026-09-26/turetim.py
"""
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.kanal.cerceve import cerceve_kur  # noqa: E402
from sim2.kanal.dunya import referans_2026, snr_esigi_db  # noqa: E402
from sim2.kanal.kanal import cerceve_per  # noqa: E402
from sim2.kanal.yayilim import Yayilim, lin_to_db  # noqa: E402

if __name__ == "__main__":
    k = referans_2026(kol="turetim")
    y = Yayilim(k)
    c = cerceve_kur(k, "veri")
    s10 = snr_esigi_db(lambda s: cerceve_per(c, s), 0.10)
    s50 = snr_esigi_db(lambda s: cerceve_per(c, s), 0.50)
    a = k.yol_kaybi_usteli
    print(f"EIRP {k.verici_eirp_dbm} dBm · alıcı dipol {k.alici_anten_kazanci_dbi}"
          f" dBi · gürültü {lin_to_db(y.gurultu_w * 1e3):.2f} dBm")
    print(f"SNR(PER %10) {s10:.2f} dB · SNR(PER %50) {s50:.2f} dB")
    print(f"menzil_snr_db {k.menzil_snr_db:.2f} (PER %10 + 10 dB) → "
          f"nominal bağ iletim_menzili_m {k.iletim_menzili_m:.0f} m")
    print(f"sinr_esigi_db β {k.sinr_esigi_db:.2f} (PER %50 + 2σ) → "
          f"β mesafesi {k.iletim_menzili_m * 10 ** ((k.menzil_snr_db - k.sinr_esigi_db) / (10 * a)):.0f} m")
    print(f"duyarlılık menzili (SNR = PER %10) "
          f"{k.iletim_menzili_m * 10 ** ((k.menzil_snr_db - s10) / (10 * a)):.0f} m"
          f" · girişim menzili (SNR 0 dB) {k.girisim_menzili_m:.0f} m")
    print(f"alan {k.alan_en_m:.0f} m · irtifa {k.irtifa_min_m:.0f}–{k.irtifa_maks_m:.0f}"
          f" m · hız {k.gm_hiz_min_ms * 3.6:.0f}–{k.gm_hiz_maks_ms * 3.6:.0f} km/h"
          f" (σ {k.gm_hiz_sigma_ms:.2f} m/s) · görev yarıçapı "
          f"{k.gorev_grup_yaricapi_m:.0f} m")
