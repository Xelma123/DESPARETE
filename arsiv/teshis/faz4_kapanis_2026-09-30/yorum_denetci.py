"""Yorum temizliği denetçisi — kod DEĞİŞMEDİ mi? (Faz 4 kapanışı, K-203)

Taban kopyadaki ve çalışma ağacındaki her `.py` dosyasının sözdizim ağacını
belge dizgileri çıkarılmış hâlde karşılaştırır. Yorumlar ağaçta yer almaz;
yani yorum ve belge dizgisi dışında TEK bir kod değişikliği bile fark olarak
çıkar. Satır sonu farkı da raporlanır (CRLF/LF korunmalı).

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz4_kapanis_2026-09-30/yorum_denetci.py <taban_dizini> [paket ...]
"""
import ast
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]


def _belgesiz(agac: ast.AST) -> str:
    for dugum in ast.walk(agac):
        govde = getattr(dugum, "body", None)
        if (isinstance(dugum, (ast.Module, ast.ClassDef, ast.FunctionDef,
                               ast.AsyncFunctionDef))
                and govde and isinstance(govde[0], ast.Expr)
                and isinstance(govde[0].value, ast.Constant)
                and isinstance(govde[0].value.value, str)):
            dugum.body = govde[1:] or [ast.Pass()]
    return ast.dump(agac, include_attributes=False)


def main() -> int:
    taban = Path(sys.argv[1]).resolve()
    paketler = sys.argv[2:] or ["sim2", "protokoller"]
    fark = ayni = 0
    for paket in paketler:
        for yeni in sorted((KOK / paket).rglob("*.py")):
            if "__pycache__" in yeni.parts:
                continue
            eski = taban / yeni.relative_to(KOK)
            if not eski.exists():
                print(f"YENİ DOSYA  {yeni.relative_to(KOK)}")
                continue
            be, by = eski.read_bytes(), yeni.read_bytes()
            if be == by:
                ayni += 1
                continue
            if _belgesiz(ast.parse(be)) != _belgesiz(ast.parse(by)):
                print(f"🔴 KOD FARKI  {yeni.relative_to(KOK)}")
                fark += 1
            crlf_e, crlf_y = b"\r\n" in be, b"\r\n" in by
            if crlf_e != crlf_y:
                print(f"⚠️ SATIR SONU  {yeni.relative_to(KOK)} "
                      f"({'CRLF' if crlf_e else 'LF'} → "
                      f"{'CRLF' if crlf_y else 'LF'})")
            if be != by and _belgesiz(ast.parse(be)) == _belgesiz(ast.parse(by)):
                print(f"   yalnız yorum  {yeni.relative_to(KOK)}  "
                      f"{len(be.splitlines())} → {len(by.splitlines())} satır")
    print(f"değişmeyen {ayni} · kod farkı {fark}")
    return 1 if fark else 0


if __name__ == "__main__":
    raise SystemExit(main())
