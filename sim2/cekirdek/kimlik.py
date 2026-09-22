"""
Kimlik — bir sonuç satırı hangi koşudan, hangi koddan, hangi araçtan geldi.

🔴 NEDEN BU DOSYA VAR
=====================
Eski simülatörde sonuç satırı **koşuyu tanımlamıyordu**: ne zaman damgası ne
koşu kimliği vardı ve `kaynak_hash` yalnız `sim/`i kapsıyordu. Sonucu ölçüldü:
aynı kod sürümünde iki kez koşan bir araç `.jsonl`de **ayırt edilemiyordu** ve
dosyalar `append` ile büyüdüğü için aynı anahtar iki kez okunabiliyordu. Bir
ölçümde aynı satırların 2× okunması `8/30 · p = 0,0161`i `16/60 · p = 0,000394`
yapıyordu — **41 kat**. Yani koşu kimliği olmayan bir dosya anlamlılığı
uydurabilir.

🔒 İKİ FARKLI KİMLİK — karıştırılmaz
====================================
`kosu_kimligi`   BELİRLENİMCİ. Aynı girdi → aynı kimlik. İki satır aynı
                 kimliği taşıyorsa **ikisi de aynı koşudur** (kopya).
`calisma_kimligi` FİZİKSEL çalıştırma. Her `python ...` çağrısında yeni.
                 🔴 Hiçbir parmak izine girmez — yoksa belirlenimcilik ölür.
"""

from __future__ import annotations

import hashlib
import os
import platform
import struct
import sys
import time
import uuid
from pathlib import Path
from typing import Iterable, Mapping, Sequence

__all__ = [
    "PAKET_KOKU", "arac_hash", "calisma_kimligi", "zaman_damgasi_utc",
    "kosu_kimligi", "kurulum_hash", "evren_hash", "ortam_ozeti",
]

PAKET_KOKU = Path(__file__).resolve().parent.parent   # .../sim2
_AYIRICI = b"\x1f"

# Süreç ömrü boyunca sabit; her `python` çağrısında yeni.
_CALISMA = uuid.uuid4().hex[:16]


def _ozet(*parcalar: bytes, bayt: int = 16) -> str:
    h = hashlib.blake2b(digest_size=bayt)
    for p in parcalar:
        h.update(p)
        h.update(_AYIRICI)          # 🔒 ayırıcı GERÇEK — b"" bir no-op'tur
    return h.hexdigest()


def arac_hash(kok: Path | None = None) -> str:
    """`sim2/` altındaki tüm `.py` dosyalarının içerik özeti.

    Dosya **adı da** özete girer: yeniden adlandırma da kod değişikliğidir.

    ⭐ Git'ten iyi: git kaydedilmemiş yerel değişikliği göremez, bu görür.
    🔒 Eski simülatörün aksine `protokoller/` ve `analiz/` bu özete GİRMEZ —
    onlar ayrı paketlerdir ve kendi özetlerini taşırlar; bir analiz aracını
    değiştirmek simülatör sonuçlarını bayatlatmamalı.
    """
    kok = kok or PAKET_KOKU
    h = hashlib.blake2b(digest_size=16)
    for yol in sorted(kok.rglob("*.py")):
        if "__pycache__" in yol.parts:
            continue
        h.update(yol.relative_to(kok).as_posix().encode())
        h.update(_AYIRICI)
        h.update(yol.read_bytes())
        h.update(_AYIRICI)
    return h.hexdigest()


def calisma_kimligi() -> str:
    """Bu Python sürecinin kimliği. Parmak izlerine GİRMEZ."""
    return _CALISMA


def zaman_damgasi_utc() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def ortam_ozeti() -> dict[str, str]:
    """Tekrarlanabilirlik için ortam — literatürün raporlama şartı."""
    ozet = {
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "islemci": platform.machine(),
        "hashseed": os.environ.get("PYTHONHASHSEED", "(ayarsız)"),
    }
    # 🔴 KÜTÜPHANE SÜRÜMLERİ DE YAZILIR. `kanal/kanal.py` DQPSK'nın kapalı
    # formunda `scipy`nin Marcum-Q ve Bessel gövdelerini kullanıyor; sürüm
    # değişirse PER'in son basamakları değişebilir. Sürümü kaydetmemek, sonuç
    # satırının "hangi araçla üretildi" sorusunu yarım cevaplaması olurdu —
    # `arac_hash` yalnız `sim2/`yi kapsar.
    for ad, modul in (("numpy", "numpy"), ("scipy", "scipy")):
        try:
            ozet[ad] = __import__(modul).__version__
        except Exception:
            ozet[ad] = "(yok)"
    return ozet


def kurulum_hash(konfig_sozlugu: Mapping[str, object],
                 tedavi_alanlari: Iterable[str]) -> str:
    """Deneyin KURULUMU — tedavi alanları hariç her şey.

    İki kol yalnızca **tedavide** ayrılabilir (kol adı, senaryo, ablasyon
    bayrakları). Başka bir alan farklıysa o ikisi aynı deneyin iki kolu
    değildir ve karşılaştırılamazlar.

    🔒 Konum BURAYA GİRMEZ (eski simülatörden fark): mobilite açıkken konum
    zamanın fonksiyonudur ve t=0 konumunu özetlemek yanıltıcı olurdu.
    Yerleşimi belirleyen şey tohum + alan boyutlarıdır, ikisi de konfigde.
    """
    haric = set(tedavi_alanlari)
    parcalar: list[bytes] = []
    for ad in sorted(konfig_sozlugu):
        if ad in haric:
            continue
        parcalar.append(f"{ad}={konfig_sozlugu[ad]!r}".encode())
    return _ozet(*parcalar)


def evren_hash(paketler: Sequence[tuple[int, float, int, int]]) -> str:
    """Ölçüm penceresindeki PAKET EVRENİNİN parmak izi.

    `(kimlik, doğum_s, kaynak, hedef)` dörtlüleri. İki kolun *"ortak alt
    kümesi"* ancak aynı evrenden gelirse anlamlıdır: aynı kimlik iki kolda
    aynı paketi göstermiyorsa *"ortak alt küme"* diye bir şey yoktur.

    🔒 Sabit genişlikli `struct` kullanılır — ayırıcı yeterli değil, çünkü
    kayan noktalı doğum anı metne çevrilirken sürüm bağımlı olabilir.
    """
    h = hashlib.blake2b(digest_size=16)
    for kimlik, dogum_s, kaynak, hedef in paketler:
        h.update(struct.pack("<qdii", int(kimlik), float(dogum_s),
                             int(kaynak), int(hedef)))
    return h.hexdigest()


def kosu_kimligi(*, arac: str, kurulum: str, kol: str, tohum: int,
                 sayac_semasi: str, akis_listesi: str) -> str:
    """Bu koşunun BELİRLENİMCİ kimliği.

    Aynı araç + aynı kurulum + aynı kol + aynı tohum → **aynı kimlik**.
    İki sonuç satırı aynı kimliği taşıyorsa ikisi de aynı koşudur; biri
    kopyadır ve analiz onu **dışlamak zorundadır**.

    🔴 `calisma_kimligi` ve zaman damgası buraya GİRMEZ — girseydi her
    çalıştırma yeni bir kimlik üretir ve kopya tespiti imkânsızlaşırdı.
    """
    return _ozet(arac.encode(), kurulum.encode(), kol.encode(),
                 struct.pack("<q", int(tohum)),
                 sayac_semasi.encode(), akis_listesi.encode(), bayt=12)
