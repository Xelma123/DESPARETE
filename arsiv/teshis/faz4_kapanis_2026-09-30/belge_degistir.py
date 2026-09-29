"""Bir Python dosyasının belge dizgisini (modül ya da `sinif.fonksiyon`)
verilen metinle değiştirir; satır sonları (CRLF/LF) korunur.

    py -3.11 belge_degistir.py <dosya> <yeni_metin_dosyasi> [nitelikli_ad]

Yeni metin dosyası belge dizgisinin İÇERİĞİDİR (üç tırnak olmadan); girinti
hedefin girintisine göre eklenir.
"""
import ast
import sys
from pathlib import Path


def main() -> None:
    yol, metin_yolu = Path(sys.argv[1]), Path(sys.argv[2])
    ad = sys.argv[3] if len(sys.argv) > 3 else None
    ham = yol.read_bytes()
    crlf = b"\r\n" in ham
    kaynak = ham.decode("utf-8").replace("\r\n", "\n")
    agac = ast.parse(kaynak)
    hedef = agac
    if ad:
        for parca in ad.split("."):
            hedef = next(d for d in hedef.body
                         if isinstance(d, (ast.ClassDef, ast.FunctionDef))
                         and d.name == parca)
    belge = hedef.body[0]
    assert isinstance(belge, ast.Expr) and isinstance(belge.value, ast.Constant)
    satirlar = kaynak.split("\n")
    bas, son = belge.lineno - 1, belge.end_lineno
    girinti = satirlar[bas][:len(satirlar[bas]) - len(satirlar[bas].lstrip())]
    yeni = metin_yolu.read_text(encoding="utf-8").rstrip("\n").split("\n")
    govde = [girinti + '"""' + yeni[0]] + [
        (girinti + s) if s.strip() else "" for s in yeni[1:]] + [girinti + '"""']
    sonuc = "\n".join(satirlar[:bas] + govde + satirlar[son:])
    ast.parse(sonuc)
    yol.write_bytes((sonuc.replace("\n", "\r\n") if crlf else sonuc)
                    .encode("utf-8"))
    print(f"{yol}: {son - bas} → {len(govde)} satır")


if __name__ == "__main__":
    main()
