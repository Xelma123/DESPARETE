"""SINANMAMIŞ parametrelerin ve duyarlılık borcunun adları (yalnız okur)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
from sim2.yapilandirma import kokenler as K  # noqa: E402

sin = sorted(ad for ad, (kova, _) in {**K.KOKENLER, **K.MODUL_KOKENLERI}.items()
             if kova == "SINANMAMIS")
print(f"SINANMAMIS {len(sin)}:")
for ad in sin:
    kayit = K.KOKENLER.get(ad) or K.MODUL_KOKENLERI.get(ad)
    print(f"  {ad:42s} {str(kayit[1])[:90]}")
borc = K.duyarlilik_borcu()
print(f"DUYARLILIK BORCU {len(borc)}: {', '.join(borc)}")
