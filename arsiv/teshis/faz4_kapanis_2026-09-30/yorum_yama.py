"""Yorum temizliği için satır aralığı yaması — her aralığın ilk satırı
beklenen metinle başlamazsa DURUR (yanlış numaraya karşı). Satır sonu korunur.

Kullanım (başka bir betikten):
    from yorum_yama import Yama
    y = Yama("sim2/..../dosya.py")
    y.yaz(bas, son, "beklenen ilk satır başı", "yeni satır", y.kod(n, ...), ...)
    y.uygula()
"""
from pathlib import Path


class Yama:
    def __init__(self, yol: str) -> None:
        self.yol = Path(yol)
        ham = self.yol.read_bytes()
        self.crlf = b"\r\n" in ham
        self.S = ham.decode("utf-8").replace("\r\n", "\n").split("\n")
        self.Y: list[tuple[int, int, list[str]]] = []

    def kod(self, *nler: int) -> list[str]:
        return [self.S[n - 1] for n in nler]

    def yaz(self, bas: int, son: int, beklenen: str, *parcalar) -> None:
        ilk = self.S[bas - 1].strip()
        assert ilk.startswith(beklenen), (self.yol, bas, ilk[:60], beklenen)
        satirlar: list[str] = []
        for p in parcalar:
            satirlar += p.split("\n") if isinstance(p, str) else list(p)
        self.Y.append((bas, son, satirlar))

    def uygula(self) -> None:
        self.Y.sort(reverse=True)
        onceki = None
        for bas, son, yeni in self.Y:
            assert onceki is None or son < onceki, (bas, son)
            onceki = bas
            self.S[bas - 1:son] = yeni
        metin = "\n".join(self.S)
        self.yol.write_bytes((metin.replace("\n", "\r\n") if self.crlf
                              else metin).encode("utf-8"))
        print(f"{self.yol}: {len(self.S)} satır")
