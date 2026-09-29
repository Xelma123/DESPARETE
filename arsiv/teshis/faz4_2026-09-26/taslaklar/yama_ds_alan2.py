"""dunya_secimi alan geçersiz kılma: görev yarıçapı da alan oranıyla (K-185)."""
import sys
from pathlib import Path
p = Path(sys.argv[1]) / "kalibrasyon" / "dunya_secimi.py"
b = p.read_text(encoding="utf-8")
eski = '''        if alan is not None and "alan_en_m" not in ek:
            ek = {**ek, "alan_en_m": float(alan), "alan_boy_m": float(alan)}'''
yeni = '''        if alan is not None and "alan_en_m" not in ek:
            # Görev yarıçapı `referans_2026`daki gibi eski dünyanın alan
            # oranıyla (650/1800) ölçeklenir; yoksa küçük alana sığmaz.
            v = Konfig.__dataclass_fields__
            oran = (v["gorev_grup_yaricapi_m"].default
                    / v["alan_en_m"].default)
            ek = {"gorev_grup_yaricapi_m": oran * float(alan), **ek,
                  "alan_en_m": float(alan), "alan_boy_m": float(alan)}'''
assert b.count(eski) == 1
p.write_text(b.replace(eski, yeni), encoding="utf-8")
print("yamandi", p)
