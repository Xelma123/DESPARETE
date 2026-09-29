"""Uzun koşu için DONDURULMUŞ kod kopyası (Faz 4, ajan, 26 Eylül 2026).

Neden: kimlik özetleri (`arac_hash` → `sim2/`, `protokol_hash` →
`protokoller/`) satır başına okunur ve havuz işçileri modülleri ilk
kullanımda içe aktarır. Uzun bir koşu sürerken ana depoda kod değişirse
satırların kimliği ve davranışı karışır. Kopyadan koşulan iş ana depodaki
çalışmadan yalıtılır.

Kopyalanan: `sim2/`, `protokoller/`, `kalibrasyon/`, `analiz/`, `tests2/` (varsa) —
`__pycache__` hariç. Kopyanın `arac_hash`i basılır; koşu satırlarındakiyle
aynı olmalı. Ana depoda hiçbir şey silinmez ya da değiştirilmez.

    PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
        python arsiv/teshis/faz4_2026-09-26/dondur.py <hedef_dizin>
"""
import shutil
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
# `tests2/` 28 Eylül'de eklendi: regresyonun `yuklu` ve `kontrol_sinav`
# vakaları sınav protokollerini oradan alır (k196'da eksik kalmıştı).
PAKETLER = ("sim2", "protokoller", "kalibrasyon", "analiz", "tests2")


def main() -> None:
    hedef = Path(sys.argv[1]).resolve()
    if hedef.exists():
        raise SystemExit(f"hedef zaten var (silinmez, yeni ad ver): {hedef}")
    hedef.mkdir(parents=True)
    for ad in PAKETLER:
        kaynak = KOK / ad
        if kaynak.is_dir():
            shutil.copytree(kaynak, hedef / ad,
                            ignore=shutil.ignore_patterns("__pycache__"))
    (hedef / "ciktilar2").mkdir()
    sys.path.insert(0, str(hedef))
    from sim2.cekirdek.kimlik import arac_hash
    print(f"kopya: {hedef}")
    print(f"arac_hash (kopya): {arac_hash(hedef / 'sim2')}")


if __name__ == "__main__":
    main()
