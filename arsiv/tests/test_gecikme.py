"""
GECİKME YÜZDELİKLERİ — `06` Bölüm 9 koşul 2'nin aracı (B0.3).

🔴 BU DOSYANIN İKİ İŞİ VAR
===========================
1. **Yüzdelik TANIMINI dondurmak** (Y14). `06` §8.1'in dört sayısı
   (p95 = 115,95 ms vb.) belirli bir yüzdelik tanımıyla üretildi. Başka
   bir tanım (doğrusal interpolasyon, R-7/R-8 tipi) AYNI veriden BAŞKA
   sayı üretir ve tablo sessizce bayatlar.
2. **Analiz birimini ayırmak.** `06` Bölüm 7: *"analiz birimi = TOHUM,
   paket değil"*. Havuzlanmış okuma bunu ihlal eder ve ölçüldü: fark
   `gurultuden_kacan` p50'de **%577**.
"""

from __future__ import annotations

import random
import statistics as ist

import pytest

from dogrulama.gecikme import (havuzlanmis, tohum_basina,
                               tohum_yuzdelikleri, yuzdelik)


def _eski_yuzdelik(veri, p):
    """`literatur_eksenleri._yuzdelik`in 1 Eylül 2026'daki gövdesi.

    🔴 BU KOPYA BİLEREK BURADA: `06` §8.1'in tablosunu üreten tanım budur
    ve yeni gövdenin ondan ayrılmadığı ANCAK bir referansa karşı
    gösterilebilir. Testteki kopya bir "ikinci doğru kaynağı" değil, bir
    ÇAPADIR — üretim kodunda tek gövde var.
    """
    if not veri:
        return None
    s = sorted(veri)
    k = min(len(s) - 1, max(0, int(round(p * (len(s) - 1)))))
    return s[k]


def test_yuzdelik_ESKI_UYGULAMAYLA_birebir():
    """🔒 Y14 — tanım değişirse `06` §8.1'in dört sayısı bayatlar."""
    r = random.Random(20260901)
    for _ in range(2000):
        v = [r.random() for _ in range(r.randint(1, 60))]
        for p in (0.0, 0.25, 0.50, 0.95, 0.99, 1.0):
            assert yuzdelik(v, p) == _eski_yuzdelik(v, p)


def test_yuzdelik_BANKACI_yuvarlamasi_kullaniyor():
    """`int(round(x))` ile `int(x + 0.5)` AYNI DEĞİLDİR — ayrımı kilitle.

    n = 3, p = 0,25  ->  p*(n-1) = 0,5.
    Bankacı yuvarlama 0'a (çifte) gider; `int(x + 0.5)` 1 verirdi.
    """
    v = [10.0, 20.0, 30.0]
    assert yuzdelik(v, 0.25) == 10.0, (
        "yüzdelik tanımı değişmiş — `06` §8.1'in tablosu artık üretilemez")


def test_yuzdelik_bos_veride_None():
    """🔴 `03` B2 — 'ölçüm yok' bir SAYI olarak dönmemeli."""
    assert yuzdelik([], 0.95) is None
    assert havuzlanmis([])["p95"] is None
    assert tohum_basina([[], []])["p95"] is None


# ==========================================================================
# ANALİZ BİRİMİ — `06` Bölüm 7
# ==========================================================================

def test_havuzlanmis_ve_tohum_basina_AYRISIYOR():
    """🔴 İkisi aynı şey değildir; havuzlama teslim SAYISIYLA ağırlıklandırır.

    Kurulum ölçülen olguyu birebir taklit ediyor: bir tohum ÇOK paket ve
    DÜŞÜK gecikme, diğeri AZ paket ve YÜKSEK gecikme. Havuzlanmış medyan
    kalabalık tohuma kayar; tohum başına okuma ikisine EŞİT ağırlık verir.
    """
    kalabalik_hizli = [1.0] * 100
    seyrek_yavas = [100.0] * 2
    h = havuzlanmis([kalabalik_hizli, seyrek_yavas])
    t = tohum_basina([kalabalik_hizli, seyrek_yavas])

    assert h["p50"] == 1.0, "havuzlanmış medyan kalabalık tohuma kaymalıydı"
    assert t["p50"] == pytest.approx((1.0 + 100.0) / 2)
    assert t["p50"] > 10 * h["p50"], (
        "iki okuma ayrışmıyor — analiz birimi ayrımı ölçülemez hâle gelmiş")


def test_tohum_basina_BOS_tohumlari_sayiyor():
    """🔴 `03` B2 — kaç gözlemle hesaplandığı her zaman yazılır."""
    t = tohum_basina([[1.0, 2.0], [], [3.0], []])
    assert t["n_tohum"] == 2 and t["n_bos_tohum"] == 2


def test_tohum_yuzdelikleri_ESLESTIRILMIS_test_icin_dizi_veriyor():
    """Eşleştirilmiş bir test tohum BAŞINA tek sayı ister."""
    diziler = [[1.0, 2.0, 3.0], [10.0, 20.0, 30.0], []]
    p95 = tohum_yuzdelikleri(diziler, 0.95)
    assert p95 == [3.0, 30.0], "boş tohum diziye girmemeli"


# ==========================================================================
# 🔴 Y8 — ÖLÇÜLEN OLGU: ortalama YALAN SÖYLEYEBİLİR
# ==========================================================================

def test_y8_hayatta_kalan_yanliligi_SENTETIK_olarak_uretilebiliyor():
    """Aracın göstermesi gereken olgu, sentetik veride de görünmeli.

    S0: hem kolay hem zor paketler teslim ediliyor.
    S2: yalnızca KOLAY paketler teslim ediliyor (zorlar hiç gelmiyor).
    Ortalama DÜŞER — ve bu bir iyileşme değildir.
    """
    s0 = [10.0] * 50 + [200.0] * 50          # ortalama 105
    s2 = [12.0] * 50                          # ortalama 12, ama yarısı kayıp
    assert ist.mean(s2) < ist.mean(s0), (
        "kurulum olguyu üretmiyor — test hiçbir şey göstermiyor (Y7)")
    # Aynı paketler (ortak alt küme) üzerinden bakılınca gecikme ARTIYOR:
    assert ist.mean(s2) > ist.mean(s0[:50])
