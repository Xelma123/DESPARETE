"""Dondurulmuş kopyanın dosya özeti ve commit'le karşılaştırması.

    PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \n        py -3.11 arsiv/teshis/faz4_2026-09-26/kopya_ozet.py <kopya dizini> <commit> > <dizin>/kopya_ozet.txt

`dondur.py`'nin kopyasının commit'le birebir olduğunu gösterir (`DEVIR-PROMPT.md` §3 madde 6).
Faz 5'in teşhis ölçümlerindeki `kopya_ozet.txt` dosyaları bu betikle üretildi; 26 Kasım'da depoya alındı.

Her dosya için satır sonları LF'ye normalleştirilmiş içeriğin md5'i; aynı
yolun `git show <commit>:<yol>` içeriğiyle karşılaştırılır. Son satırlar
özet: birebir / farklı / kopyada fazla / commit'te eksik.
"""
import hashlib
import subprocess
import sys
from pathlib import Path

PAKETLER = ("sim2", "protokoller", "kalibrasyon", "analiz", "tests2")


def md5(b: bytes) -> str:
    return hashlib.md5(b.replace(b"\r\n", b"\n")).hexdigest()


def main() -> None:
    kopya = Path(sys.argv[1]).resolve()
    commit = sys.argv[2]
    kok = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"],
                                       text=True).strip())
    izli = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", commit, "--", *PAKETLER],
        cwd=kok, text=True).split()
    izli = {p for p in izli if "__pycache__" not in p}
    dosyalar = sorted(p.relative_to(kopya).as_posix()
                      for p in kopya.rglob("*") if p.is_file()
                      and "__pycache__" not in p.parts)
    birebir, farkli, fazla = 0, [], []
    for yol in dosyalar:
        ozet = md5((kopya / yol).read_bytes())
        print(f"{ozet} *{yol}")
        if yol not in izli:
            fazla.append(yol)
            continue
        asil = subprocess.check_output(["git", "show", f"{commit}:{yol}"],
                                       cwd=kok)
        if md5(asil) == ozet:
            birebir += 1
        else:
            farkli.append(yol)
    eksik = sorted(izli - set(dosyalar))
    print(f"# commit {commit} · kopya {len(dosyalar)} dosya · birebir "
          f"{birebir} · farklı {len(farkli)} · kopyada fazla {len(fazla)} · "
          f"commit'te olup kopyada eksik {len(eksik)} (satır sonları "
          f"normalleştirilerek)")
    for ad, liste in (("farklı", farkli), ("fazla", fazla), ("eksik", eksik)):
        for yol in liste:
            print(f"# {ad}: {yol}")


if __name__ == "__main__":
    main()
