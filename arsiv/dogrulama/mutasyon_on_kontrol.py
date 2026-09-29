"""
MUTASYON ÖN KONTROLÜ — pahalı koşudan ÖNCE, saniyeler içinde.

🔴 NEDEN BU DOSYA VAR
=====================
`mutasyon_paketi.py` her mutasyon için TAM test paketini koşar: 30 mutasyon
× ~200 s = **~25 dk**. Kapı raporunun içinde ise ~39 dk.

Bu sürenin sonunda öğrenilen şey çoğu zaman şu oluyor: *"bir mutasyonun
beklenen testi kırılmadı."* Ve bunun iki sebebi var —

  1. **Kod korumasız** *(gerçek bulgu)*
  2. **Mutasyon hatalı** *(benim hatam)*

İkisi de aynı çıktıyı verir, ama ikincisi 39 dakikaya değmez.

BU ARAÇ NE YAPAR
================
Her mutasyon için **yalnızca kendi `beklenen_test`ini** koşar. Tam paket
yerine tek test → **~30 kat hızlı**.

⚠️ BU BİR KAPI DEĞİLDİR ve `mutasyon_paketi.py`nin YERİNE GEÇMEZ.

🔴 KAPSAMI — NE SÖYLER, NE SÖYLEMEZ (25 Ağustos 2026, K-058)
=============================================================
Bu araç uzun süre *"kapının düşüp düşmeyeceğini önceden söyler"* diyordu.
**O cümle fazla genişti** ve üç kez yanlış çıktı: *"ön kontrol geçti, kapı
düştü"* vakası K-042, K-046 ve K-058'de yaşandı.

| soru | söyler mi |
|---|---|
| Beklenen test kırılıyor mu | ✅ **EVET** — tek işi bu |
| Mutasyon başka hangi testleri kırıyor | ❌ hayır |
| Taban temiz mi | ❌ hayır |
| 🔴 Tam paket zaman aşımına uğrar mı | ❌ **HAYIR — YAPISAL OLARAK GÖREMEZ** |

Sonuncusu K-058'in dersidir. Bu araç her mutantı `-k beklenen_test` ile
koşar; saniyeler sürer ve **tam paketin süresini hiç ölçmez.** 25 Ağustos'ta
35/35 dedi, kapı aynı gün 4/35 ile düştü — 31 mutant zaman aşımına uğramıştı.
Aradaki farkı bu araç göremezdi; ölçüsü o eksende yok.

O ekseni koruyan yer ayrı: `tests/test_kapi_secimleri.py::test_b78_*`
zaman aşımı sabitini GÜNCEL test sayısına karşı sınar (saniyeler sürer).

> Y11: bir korumanın kapsamı, kapsadığı kadar **kapsamadığıyla** da yazılır.

⚖️ NEDEN YAZILDI — 19 Ağustos 2026, K-042.
Kapı raporu 39,1 dk koştu ve `Ç1.3 → 30/30 !!YANLIŞ TEST x1` ile düştü.
Sebep D20 mutasyonunun kendisiydi: `slot_s`i 1 ns yapmak kanal dilimi
marjını BOZMUYOR (baskın terim önbelge, 192 µs). Bu araç aynı bilgiyi
**1,5 dakikada** verirdi.

Kullanım:
    python dogrulama/mutasyon_on_kontrol.py
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import time
from multiprocessing import Pool
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK))

from dogrulama.kopya import depoyu_kopyala          # noqa: E402
from dogrulama.mutasyon_paketi import MUTASYONLAR  # noqa: E402

# 🔴 ALT SÜREÇ ÇIKTISI UTF-8 OLARAK ÇÖZÜLÜR (20 Ağu 2026).
# `subprocess.run(..., text=True)` kodlama verilmezse çıktıyı YEREL KOD
# SAYFASIYLA çözer. Bu makinede o cp1254 ve çocuk süreç UTF-8 basıyor
# (PYTHONIOENCODING ayarlı). Türkçe "Ş" (U+015E → C5 9E) gibi karakterler
# cp1254'te TANIMSIZ olduğu için ebeveyn `UnicodeDecodeError` fırlatır ve
# araç, işini bitirmişken çöker. Ölçüldü: bir doğrulama koşusu tam olarak
# böyle düştü. `errors="replace"` ile ayrıştırma asla çökmez.


def _kos(m) -> tuple[str, str, str]:
    gecici = Path(tempfile.mkdtemp(prefix="on_kontrol_"))
    try:
        hedef = depoyu_kopyala(gecici / "depo")
        yol = hedef / m.dosya
        metin = yol.read_text(encoding="utf-8")
        if m.eski not in metin:
            return (m.ad, m.beklenen_test, "MUTASYON UYGULANAMADI")
        yol.write_text(metin.replace(m.eski, m.yeni, 1), encoding="utf-8")

        p = subprocess.run(
            [sys.executable, "-m", "pytest", "tests", "-q", "--tb=no",
             "-p", "no:cacheprovider", "-k", m.beklenen_test],
            cwd=hedef, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"})

        # 🔴 Y7 — "0 hata" ile "0 test" AYIRT EDİLMELİ (K-033'ün dersi).
        #
        # ⚠️ İlk yazımı `"error" in stdout` diye bakıyordu ve YANLIŞTI:
        # `--tb=no` ile bile pytest "FAILED … - AssertionError: …" basar,
        # yani GERÇEKTEN KIRILAN bir test "toplama hatası" sanılıyordu.
        # İki mutasyon böyle yanlış işaretlendi. Yargı, metin sezgisinden
        # değil pytest'in KENDİ özet satırından çıkarılmalı — bu dosyanın
        # var oluş sebebiyle aynı ders.
        if p.returncode == 5:                       # pytest: hiç test toplanmadı
            return (m.ad, m.beklenen_test, "TEST BULUNAMADI")
        if p.returncode not in (0, 1):
            return (m.ad, m.beklenen_test, f"PYTEST HATASI (rc={p.returncode})")

        son = [x for x in p.stdout.splitlines()
               if " passed" in x or " failed" in x or "no tests ran" in x]
        metin = son[-1] if son else ""
        gecen = (int(metin.split(" passed")[0].split()[-1])
                 if "passed" in metin else 0)
        kirilan = (int(metin.split(" failed")[0].split()[-1])
                   if "failed" in metin else 0)
        if gecen + kirilan == 0:
            return (m.ad, m.beklenen_test, "TEST BULUNAMADI")
        return (m.ad, m.beklenen_test, "kırıldı" if kirilan else "KIRILMADI")
    except Exception as e:                                   # noqa: BLE001
        return (m.ad, m.beklenen_test, f"HATA {e!r}"[:80])
    finally:
        shutil.rmtree(gecici, ignore_errors=True)


def main() -> None:
    t0 = time.perf_counter()
    print("=" * 78)
    print("MUTASYON ÖN KONTROLÜ — her mutasyon yalnızca KENDİ testiyle")
    print("=" * 78)
    print(f"{len(MUTASYONLAR)} mutasyon · tahmini ~2 dk")
    print()
    print("⚠️ Bu bir KAPI DEĞİLDİR. `mutasyon_paketi.py`nin yerine geçmez.")
    print("   Söylediği TEK şey: her mutasyonun beklenen testi kırılıyor mu.")
    print("   🔴 ZAMAN AŞIMINI GÖREMEZ — tam paketi hiç koşmaz (K-058).")
    print("   O ekseni koruyan: tests/test_kapi_secimleri.py::test_b78_*")
    print()

    with Pool(8) as havuz:
        sonuc = havuz.map(_kos, MUTASYONLAR)

    sorunlu = [r for r in sonuc if r[2] != "kırıldı"]
    for ad, test, durum in sonuc:
        if durum != "kırıldı":
            print(f"🔴 {ad}")
            print(f"     beklenen : {test}")
            print(f"     durum    : {durum}")

    print()
    print("=" * 78)
    print(f"Süre: {(time.perf_counter()-t0)/60:.1f} dk")
    if sorunlu:
        print(f"🔴 {len(sorunlu)}/{len(MUTASYONLAR)} mutasyonun beklenen testi "
              f"KIRILMIYOR.")
        print("   İki olasılık, ikisi de ayrı iş:")
        print("     · kod korumasız  → regresyon testi yaz")
        print("     · mutasyon hatalı → mutasyonu düzelt")
        print("   `mutasyon_paketi.py` bu hâliyle DÜŞER; koşmadan önce çöz.")
        sys.exit(1)
    print(f"✅ {len(MUTASYONLAR)}/{len(MUTASYONLAR)} mutasyonun beklenen testi "
          f"kırılıyor — tam koşu bu ölçütten geçmeli.")


if __name__ == "__main__":
    main()
