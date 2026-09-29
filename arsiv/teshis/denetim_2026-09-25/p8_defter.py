"""K-166 — P8'in totolojik iddiası yerine ne sınanabilir: defter değerleri."""
import sys
KOK = "."                    # depo kökünden koşulur
sys.path.insert(0, KOK)
sys.path.insert(0, KOK + r"\tests2")
from test_kontrol_duzlemi import _kos, KAYIPLI
from sim2.kosum.sonuc import sonuc_satiri
kur, kosu, _ = _kos(**KAYIPLI)
d = sonuc_satiri(kur, kosu.dugumler, "kontrol_sinav")["teshis"]["kontrol_duzlemi"]["defter"]
print({k: v for k, v in d.items()})
