"""
Sonuç yazıcı.

İKİ KURAL
---------
1) Her sonuç satırı KENDİ TAM KONFİGÜRASYONUNU taşır.
   Bayrağı olmayan bir satır yeniden üretilemez. Aylar sonra "bu sayı hangi
   parametrelerle çıktı" sorusu cevapsız kalırsa, o sayı raporlanamaz.

2) Her satır ANINDA diske yazılır ve flush edilir.
   Uzun bir matris yarıda kesilirse (elektrik, hata, Ctrl-C) tamamlanan
   koşular kaybolmaz.

KOD SÜRÜMÜ NEDEN GIT DEĞİL, HASH
---------------------------------
Bu projede git komutu çalıştırılmıyor (03-YONTEM-KURALLARI.md, kural 6).
Onun yerine koşu anında tüm kaynak dosyaların içerik hash'i hesaplanıyor.

Bu aslında git'ten daha iyi: git, kaydedilmemiş yerel değişiklikleri göremez.
Hash görür. "Bu sayı hangi koddan çıktı" sorusu, kaydedilmemiş bir değişiklik
varken bile cevaplanabilir olur.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Any, Iterable

# Yollar depo köküne göre mutlaklanır. Göreli yol, çağıranın çalışma dizinine
# yazar — ve sonuçlar bir gün "nereye kaydolduğu belli olmayan" dosyalarda
# kaybolur. (03-YONTEM-KURALLARI.md, Bölüm B5)
DEPO_KOKU = Path(__file__).resolve().parent.parent


def kaynak_hash(kok: Path | None = None) -> str:
    """sim/ altındaki tüm .py dosyalarının içeriğinden tek bir hash üretir.

    Dosya adları da hash'e girer: bir dosyanın yeniden adlandırılması da
    kod değişikliğidir.
    """
    kok = kok or (DEPO_KOKU / "sim")
    h = hashlib.blake2b(digest_size=16)
    for yol in sorted(kok.rglob("*.py")):
        h.update(yol.relative_to(kok).as_posix().encode())
        h.update(b"\x00")
        h.update(yol.read_bytes())
        h.update(b"\x00")
    return h.hexdigest()


class SonucYazici:
    """JSONL sonuç dosyası. Her satır bir koşu.

    JSONL seçildi çünkü: satır satır eklenebilir, yarıda kesilse bile okunan
    kısım geçerlidir, ve şeması satırın içinde taşınır.
    """

    def __init__(self, dosya: str | Path, kaynak_hash_degeri: str | None = None) -> None:
        self.dosya = Path(dosya)
        if not self.dosya.is_absolute():
            self.dosya = DEPO_KOKU / self.dosya
        self.dosya.parent.mkdir(parents=True, exist_ok=True)
        self.kaynak_hash = kaynak_hash_degeri or kaynak_hash()
        self._f = self.dosya.open("a", encoding="utf-8")
        self.yazilan = 0

    def yaz(self, konfig_sozluk: dict[str, Any], korunum: dict[str, Any],
            metrikler: dict[str, Any], **ek: Any) -> None:
        """Bir koşunun sonucunu yazar.

        `korunum["korunum_tamam"]` False ise satır yine de yazılır — silinmez.
        Analiz tarafı onu dışlar. Bozuk bir koşuyu silmek, kaç koşunun bozuk
        olduğunu da silmek demektir.
        """
        satir = {
            "kaynak_hash": self.kaynak_hash,
            "konfig": konfig_sozluk,
            "korunum": korunum,
            "metrikler": metrikler,
            **ek,
        }
        self._f.write(json.dumps(satir, ensure_ascii=False, sort_keys=True) + "\n")
        self._f.flush()
        os.fsync(self._f.fileno())   # işletim sistemi tamponunda kalmasın
        self.yazilan += 1

    def kapat(self) -> None:
        self._f.close()

    def __enter__(self) -> "SonucYazici":
        return self

    def __exit__(self, *_: object) -> None:
        self.kapat()


def satirlari_oku(dosya: str | Path) -> Iterable[dict[str, Any]]:
    """Sonuç dosyasını okur. Bozuk son satırı (yarıda kesilmiş yazım)
    sessizce atlamaz — uyarı olarak döndürür ki fark edilsin."""
    yol = Path(dosya)
    if not yol.is_absolute():
        yol = DEPO_KOKU / yol
    with yol.open(encoding="utf-8") as f:
        for i, satir in enumerate(f, start=1):
            satir = satir.strip()
            if not satir:
                continue
            try:
                yield json.loads(satir)
            except json.JSONDecodeError as e:
                raise ValueError(
                    f"{yol}:{i} bozuk JSON satırı — koşu yarıda kesilmiş "
                    f"olabilir. Satır silinmeden önce incelenmeli. ({e})"
                ) from e
