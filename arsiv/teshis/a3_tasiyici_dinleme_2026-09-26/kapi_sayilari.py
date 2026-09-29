"""A3 (K-174) kapı sınavlarının sayıları — `tests2/test_kosum.py` A3 bölümüyle
aynı kurulum (küçük dünya). Kullanım:
    PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python \
        arsiv/teshis/a3_tasiyici_dinleme_2026-09-26/kapi_sayilari.py
"""
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
for y in (KOK, KOK / "tests2"):
    if str(y) not in sys.path:
        sys.path.insert(0, str(y))

from test_kosum import _kos  # noqa: E402

if __name__ == "__main__":
    print("1) tek çarpışma alanı (statik-yok, 6 s): geometrik ↔ güç (ED −200 dBm)")
    for ad, ek in (("geometrik", {}),
                   ("guc", {"tasiyici_dinleme": "guc",
                            "ed_esigi_dbm": -200.0})):
        kur, _ = _kos("statik-yok", "enyakin", bitis=6.0, **ek)
        s = kur.sayaclar.disa_ver()
        print(f"   {ad:<9} mac_deneme {s['mac_deneme']:>6.0f} · alim_red_mesgul "
              f"{s['alim_red_mesgul']:>6.0f} · teslim {s['teslim_paket']:>5.0f}")
    print("2) sürekli karıştırıcı 40 dBm, 1 s'de açılır (5 s; pencere 1–4 s)")
    ortak = dict(karistirici_baslangic_s=1.0, karistirici_guc_override_dbm=40.0)
    for ad, ek in (("geometrik", {}), ("guc", {"tasiyici_dinleme": "guc"})):
        kur, _ = _kos("statik-surekli", "enyakin", bitis=5.0, **ek, **ortak)
        s = kur.sayaclar.disa_ver()
        print(f"   {ad:<9} pencerede mac_deneme {s['mac_deneme_pencere']:>5.0f} · "
              f"beacon {s['beacon_gonderilen_pencere']:>4.0f} · tüm koşu "
              f"mac_deneme {s['mac_deneme']:>5.0f}")
