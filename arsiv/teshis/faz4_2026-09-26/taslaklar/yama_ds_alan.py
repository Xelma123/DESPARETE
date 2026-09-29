"""dunya_secimi: `--alan` / DESPARETE_ALAN_M — Faz 4.1 alan × güç taraması (K-185)."""
import sys
from pathlib import Path
p = Path(sys.argv[1]) / "kalibrasyon" / "dunya_secimi.py"
b = p.read_text(encoding="utf-8")
def degis(eski, yeni):
    global b
    assert b.count(eski) == 1, eski[:50]
    b = b.replace(eski, yeni)
degis('''ORTAM = "DESPARETE_DUNYA"''', '''ORTAM = "DESPARETE_DUNYA"
# Faz 4.1 (K-185): alan × güç ortak taraması için referans alanını geçersiz
# kılar (yalnız referans dünyada; kare alan). Verilmezse `REFERANS_ALAN_M`.
ALAN_ORTAM = "DESPARETE_ALAN_M"''')
degis('''        del argv[i:i + 2]
        os.environ[ORTAM] = ad
    return secili()''', '''        del argv[i:i + 2]
        os.environ[ORTAM] = ad
    if "--alan" in argv:
        i = argv.index("--alan")
        dogrula(i + 1 < len(argv), "--alan bir metre değeri ister")
        alan = float(argv[i + 1])
        dogrula(alan > 0.0, "alan pozitif olmalı")
        del argv[i:i + 2]
        os.environ[ALAN_ORTAM] = repr(alan)
    return secili()''')
degis('''    if referans_mi():
        from sim2.kanal.dunya import referans_2026
        return referans_2026(**ek)''', '''    if referans_mi():
        from sim2.kanal.dunya import referans_2026
        alan = os.environ.get(ALAN_ORTAM)
        if alan is not None and "alan_en_m" not in ek:
            ek = {**ek, "alan_en_m": float(alan), "alan_boy_m": float(alan)}
        return referans_2026(**ek)''')
degis('''def etiket(ad: str) -> str:
    """Çıktı adı — referans dünyada sonek alır, eski çıktılar ezilmez."""
    return f"{ad}_referans_2026" if referans_mi() else ad''', '''def etiket(ad: str) -> str:
    """Çıktı adı — referans dünyada sonek alır, eski çıktılar ezilmez."""
    if not referans_mi():
        return ad
    alan = os.environ.get(ALAN_ORTAM)
    return (f"{ad}_referans_2026" if alan is None
            else f"{ad}_referans_2026_alan{float(alan):.0f}")''')
p.write_text(b, encoding="utf-8")
print("yamandi", p)
