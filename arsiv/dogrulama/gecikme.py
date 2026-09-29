"""
GECİKME YÜZDELİKLERİ — `06` Bölüm 9 koşul 2'nin aracı.

🔴 NEDEN BU DOSYA VAR
=====================
`06` Bölüm 9 koşul 2: *"metriğin ne ölçtüğü doğrulanmış"*. Gecikme için
**sağlanmıyor** ve sebebi ölçüldü (`10` §7b.4): S0 → S2'de teslim
0,9962 → 0,5120 düşerken

    ortalama  45,83 → 44,29 ms   (−%3,4)   🔴 "karıştırma İYİLEŞTİRDİ"
    p50       27,06 → 22,92 ms   (−%15,3)  🔴 aynı yalan
    p95       92,04 → 115,95 ms  (+%26,0)  🟢 GERÇEK
    p99      560,67 → 398,59 ms  (−%28,9)  🔴 en zor paketler hiç gelmiyor

Sebep hayatta-kalan yanlılığı: gecikme yalnızca TESLİM EDİLENDEN ölçülür.
`06` §8.1 bu yüzden mühürlü: *"rapora giren her gecikme cümlesi p95 ile
birlikte yazılır."*

🔒 YÜZDELİK TANIMI DEĞİŞMEZ — Y14
==================================
`06` §8.1'in tablosu (p95 = 115,95 ms) `literatur_eksenleri._yuzdelik` ile
üretildi. Buradaki `yuzdelik()` onun BİREBİR aynısıdır ve öyle kalmak
zorunda: farklı bir yüzdelik tanımı (doğrusal interpolasyon, R-7 tipi)
aynı veriden BAŞKA bir sayı üretir ve `06`nın tablosu sessizce bayatlar.
Regresyon: `tests/test_gecikme.py::test_yuzdelik_ESKI_UYGULAMAYLA_birebir`.

🔴 ANALİZ BİRİMİ — ÖLÇÜLECEK KARAR (B0.3)
==========================================
`06` Bölüm 7: *"analiz birimi = TOHUM, paket değil"* (literatür 12:§4.4).
Ama `10` §7b.4'ün tablosu tüm tohumların paketlerini HAVUZLAYARAK
hesaplandı — ve havuzlama, çok teslim eden tohuma fazla ağırlık verir.
İki okuma da burada hesaplanır; hangisinin BİRİNCİL olduğu ölçülüp
`04`e üreticisiyle yazılır. Sessiz bir tercih yapılmaz.
"""

from __future__ import annotations

import statistics as ist
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from typing import Iterable, Sequence

from sim.karsilastirma import yuzdelik  # noqa: F401  (yeniden dışa aktarılır)

# Rapora giren üçlü. p50 tek başına yanıltıcıdır (yukarıdaki tablo),
# bu yüzden hiçbir yerde tek başına raporlanmaz.
YUZDELIKLER = (0.50, 0.95, 0.99)


# 🔴 `yuzdelik` BURADA TANIMLANMAZ, `sim/karsilastirma.py`den İÇE AKTARILIR.
#
# İlk yazımda burada bir KOPYASI vardı ve bu, tam olarak B-07'nin
# *"ikinci doğru kaynağı"* tuzağıydı: aynı tanımın iki gövdesi bir gün
# ayrışır ve `06` §8.1'in tablosu ile `ortak_alt_kume`nin p95'i sessizce
# FARKLI yüzdelikler raporlamaya başlar. Tek gövde `sim/` altındadır
# çünkü `ortak_alt_kume` onu şemanın parçası olarak kullanıyor; bu modül
# `dogrulama/` katmanından ONU çağırır (dogrulama -> sim, doğru yön).


def havuzlanmis(gecikme_listeleri: Iterable[Sequence[float]]) -> dict:
    """TÜM tohumların paketleri tek havuzda — `10` §7b.4'ün yöntemi.

    ⚠️ Analiz birimi PAKETTİR. Çok teslim eden bir tohum dağılıma daha çok
    katkı verir; `06` Bölüm 7'nin *"birim = tohum"* şartıyla çelişir.
    Betimleyici olarak meşru, doğrulayıcı test için değil.
    """
    havuz = [d for liste in gecikme_listeleri for d in (liste or [])]
    if not havuz:
        return {"n_paket": 0, "n_tohum": 0, "ortalama": None,
                **{f"p{int(100*p)}": None for p in YUZDELIKLER}}
    return {
        "n_paket": len(havuz),
        "ortalama": ist.mean(havuz),
        **{f"p{int(100*p)}": yuzdelik(havuz, p) for p in YUZDELIKLER},
    }


def tohum_basina(gecikme_listeleri: Iterable[Sequence[float]]) -> dict:
    """Her tohum için ayrı yüzdelik, sonra tohumlar arası ortalama.

    🔒 `06` Bölüm 7'nin ilan ettiği analiz birimi budur: her tohum BİR
    gözlemdir. Eşleştirilmiş bir test ancak bu okumayla kurulabilir —
    havuzlanmış bir yüzdeliğin tohum başına eşleniği yoktur.

    Boş listeli tohumlar (hiç teslim yok) DIŞLANIR ve sayısı raporlanır:
    `03` B2 — kaç gözlemle hesaplandığı her zaman yazılır.
    """
    listeler = [list(x or []) for x in gecikme_listeleri]
    dolu = [x for x in listeler if x]
    if not dolu:
        return {"n_tohum": 0, "n_bos_tohum": len(listeler), "ortalama": None,
                **{f"p{int(100*p)}": None for p in YUZDELIKLER}}
    cikti = {
        "n_tohum": len(dolu),
        "n_bos_tohum": len(listeler) - len(dolu),
        "ortalama": ist.mean([ist.mean(x) for x in dolu]),
    }
    for p in YUZDELIKLER:
        cikti[f"p{int(100*p)}"] = ist.mean([yuzdelik(x, p) for x in dolu])
    return cikti


def tohum_yuzdelikleri(gecikme_listeleri: Iterable[Sequence[float]],
                       p: float) -> list[float]:
    """Tohum başına yüzdelik DİZİSİ — eşleştirilmiş test bunu ister."""
    return [yuzdelik(list(x), p) for x in gecikme_listeleri if x]


def ozet_satiri(ad: str, s: dict) -> str:
    """🔒 p95 DAİMA yanında — `06` §8.1 mühürlü cümlesi."""
    if s.get("ortalama") is None:
        return f"{ad:<26s} TESLİM YOK (ölçüm yok, 'gecikme düşük' DEĞİL)"
    return (f"{ad:<26s} ort={1e3*s['ortalama']:8.2f} "
            f"p50={1e3*s['p50']:8.2f} p95={1e3*s['p95']:9.2f} "
            f"p99={1e3*s['p99']:9.2f} ms")
