"""
İSTATİSTİK — ön-kaydın analiz planının TEK gerçeklemesi (`v2/06` §0.4, §7).

🔒 NEYİ UYGULAR, NEREDEN
========================
  · Wilcoxon işaretli sıralar, EŞLEŞTİRİLMİŞ, ÇİFT YÖNLÜ (§7)
  · Holm–Bonferroni, aile içinde, yalnız birincil testlere (§7)
  · δ = 2 · SD_ref / √n — taban protokollerin en gürültülü çiftinden (§0.4.2)
  · hüküm: üstün · aşağı · ayırt edilemedi (§0.4.2 tablosu)
  · güç: gürültü farklarından yeniden örnekleme, B = 2 000, ret p < α/m
    (muhafazakâr), `MDE₈₀` (§0.4.3)
  · güven aralığı: eşleştirilmiş ORTALAMA farkın yüzdelik bootstrap'ı —
    §7 "etki büyüklüğü + güven aralığı" diyor, yöntemi söylemiyor; burada
    seçildi ve beyan edilir (ajan, 26 Eylül 2026, K-184)

🔴 NaN TUZAĞI (§7) KODDA KAPALI
===============================
`scipy.stats.wilcoxon` bütün farklar sıfırken NaN döndürür; Holm NaN'ı en
büyük p gibi sıralamaz ve ailenin bütün p'lerini bozar. Burada iki kapı var:
(1) bütün farklar sıfırsa test ÇAĞRILMAZ, `p = 1,0` ve `tum_sifir = True`
yazılır — "fark yok" ölçülmüştür, tanımsız değildir; (2) Holm'a sonlu
olmayan bir p girerse `DegismezHatasi`. Sessiz NaN yoktur.

🔒 YÖNTEM AÇIKÇA SEÇİLİR, `auto`YA BIRAKILMAZ: scipy'nin `auto` kuralı
sürümden sürüme değişti. Sıfır olmayan fark ≤ 50 ve bağ yoksa KESİN dağılım,
değilse normal yaklaşım (süreklilik düzeltmesi yok, bağ düzeltmeli).
Seçilen yöntem sonuca yazılır.

🔒 `analiz/` simülatörden HİÇBİR ŞEY içe aktarmaz (`olcum/metrikler.py`
başlığı; bir test bunu tarar) — hata sınıfı bile burada. Sonuç satırları
JSONL'den okunur (`analiz/satir.py`). Arac özeti (`arac_hash`) `analiz/`i kapsamaz: bir
analiz aracını değiştirmek simülatör sonuçlarını bayatlatmamalı.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Mapping, Sequence

import numpy as np
from scipy import stats

__all__ = ["AnalizHatasi", "ALFA", "WilcoxonSonucu", "wilcoxon_eslestirilmis", "holm",
           "delta_esigi", "ortalama_fark_ga", "hukum", "guc_egrisi",
           "mde80"]

ALFA: float = 0.05          # `v2/06` §7 — tek α
KESIN_TAVAN: int = 50       # bu kadar sıfır olmayan farka kadar kesin dağılım


class AnalizHatasi(ValueError):
    """Analiz girdisi sözleşmeyi çiğnedi — sessiz NaN yerine patlar."""


def dogrula(kosul: bool, mesaj: str) -> None:
    if not kosul:
        raise AnalizHatasi(mesaj)


@dataclass(frozen=True)
class WilcoxonSonucu:
    n: int                   # eşleştirilmiş çift sayısı
    n_sifir_disi: int        # teste giren (sıfır olmayan) fark sayısı
    istatistik: float | None
    p: float
    yontem: str              # "kesin" · "yaklasik" · "tum_sifir"
    ort_fark: float          # ortalama(x − y)
    tum_sifir: bool


def _farklar(x: Sequence[float], y: Sequence[float]) -> np.ndarray:
    dogrula(len(x) == len(y) and len(x) > 0,
            "eşleştirilmiş test aynı uzunlukta boş olmayan iki dizi ister")
    d = np.asarray(x, dtype=float) - np.asarray(y, dtype=float)
    dogrula(bool(np.all(np.isfinite(d))),
            "sonlu olmayan fark — geçersiz satır teste giremez (önce süz)")
    return d


def wilcoxon_eslestirilmis(x: Sequence[float],
                           y: Sequence[float]) -> WilcoxonSonucu:
    """Çift yönlü Wilcoxon işaretli sıralar testi, fark = x − y."""
    d = _farklar(x, y)
    ort = float(d.mean())
    sifir_disi = d[d != 0.0]
    if sifir_disi.size == 0:
        # 🔴 NaN TUZAĞI — test çağrılmaz; "fark yok" ölçüldü.
        return WilcoxonSonucu(n=int(d.size), n_sifir_disi=0, istatistik=None,
                              p=1.0, yontem="tum_sifir", ort_fark=ort,
                              tum_sifir=True)
    mutlak = np.abs(sifir_disi)
    bag_var = np.unique(mutlak).size < mutlak.size
    kesin = sifir_disi.size <= KESIN_TAVAN and not bag_var
    r = stats.wilcoxon(sifir_disi, alternative="two-sided",
                       zero_method="wilcox", correction=False,
                       method="exact" if kesin else "asymptotic")
    p = float(r.pvalue)
    dogrula(math.isfinite(p) and 0.0 <= p <= 1.0,
            f"Wilcoxon sonlu bir p döndürmedi: {p!r}")
    return WilcoxonSonucu(n=int(d.size), n_sifir_disi=int(sifir_disi.size),
                          istatistik=float(r.statistic), p=p,
                          yontem="kesin" if kesin else "yaklasik",
                          ort_fark=ort, tum_sifir=False)


def holm(p_degerleri: Sequence[float]) -> list[float]:
    """Holm–Bonferroni düzeltilmiş p'ler — adım adım aşağı, monoton, ≤ 1.

    p_(k)' = max_{j ≤ k} min(1, (m − j + 1) · p_(j)), özgün sırada döner."""
    m = len(p_degerleri)
    dogrula(m > 0, "Holm boş bir aile alamaz")
    for p in p_degerleri:
        dogrula(isinstance(p, (int, float)) and math.isfinite(p)
                and 0.0 <= p <= 1.0,
                f"Holm'a geçersiz p girdi: {p!r} — NaN tuzağı (§7)")
    sira = sorted(range(m), key=lambda i: p_degerleri[i])
    duzeltilmis = [0.0] * m
    onceki = 0.0
    for k, i in enumerate(sira):
        onceki = max(onceki, min(1.0, (m - k) * p_degerleri[i]))
        duzeltilmis[i] = onceki
    return duzeltilmis


def delta_esigi(farklar: Mapping[str, Sequence[float]], n: int) -> float:
    """§0.4.2: δ = 2 · SD_ref / √n, SD_ref = en gürültülü taban çiftinin
    eşleştirilmiş fark standart sapması (örneklem SD, n − 1)."""
    dogrula(n > 0 and len(farklar) > 0, "δ en az bir çift ve n > 0 ister")
    sd = []
    for ad, d in farklar.items():
        dogrula(len(d) >= 2, f"{ad}: SD için en az iki fark gerekir")
        sd.append(float(np.std(np.asarray(d, dtype=float), ddof=1)))
    return 2.0 * max(sd) / math.sqrt(n)


def ortalama_fark_ga(x: Sequence[float], y: Sequence[float], *,
                     duzey: float = 0.95, b: int = 10_000,
                     tohum: int = 0) -> tuple[float, float, float]:
    """Eşleştirilmiş ortalama fark ve yüzdelik bootstrap GA'sı —
    `(ortalama, alt, üst)`. Tohum sabit: aynı veri aynı aralığı verir."""
    d = _farklar(x, y)
    dogrula(0.0 < duzey < 1.0 and b > 0, "GA düzeyi (0, 1), b > 0")
    rng = np.random.default_rng(tohum)
    ornek = rng.choice(d, size=(b, d.size), replace=True).mean(axis=1)
    kuyruk = (1.0 - duzey) / 2.0
    return (float(d.mean()), float(np.quantile(ornek, kuyruk)),
            float(np.quantile(ornek, 1.0 - kuyruk)))


def hukum(p_holm: float, ort_fark: float, delta: float,
          mekanizma_kapisi: bool) -> str:
    """§0.4.2 tablosu. `ort_fark` = özgün − rakip (büyük iyi, ör. PDR).

      üstün           : p_holm < α ve fark ≥ δ ve mekanizma kapısı geçer
      aşağı           : p_holm < α ve fark ≤ −δ (kapı sorulmaz)
      ayırt edilemedi : geri kalan her durum
    """
    dogrula(math.isfinite(p_holm) and delta > 0.0, "geçersiz hüküm girdisi")
    if p_holm < ALFA and ort_fark >= delta and mekanizma_kapisi:
        return "ustun"
    if p_holm < ALFA and ort_fark <= -delta:
        return "asagi"
    return "ayirt_edilemedi"


def guc_egrisi(gurultu: Sequence[float], n: int,
               etkiler: Sequence[float], *, m: int = 3, b: int = 2_000,
               tohum: int = 0) -> dict[float, float]:
    """§0.4.3: gürültüden yerine koyarak `n` fark + Δ, çift yönlü Wilcoxon,
    ret `p < α/m`. Gürültü MERKEZLENMİŞ olmalı (her çift kendi
    ortalamasından arındırılmış) — burada denetlenir."""
    g = np.asarray(gurultu, dtype=float)
    dogrula(g.size >= 2 and abs(float(g.mean())) < 1e-9 * max(
        1.0, float(np.abs(g).max())) + 1e-12,
        "gürültü merkezlenmemiş — ortalama fark güce SIZAR (§0.4.3 (1))")
    rng = np.random.default_rng(tohum)
    sinir = ALFA / m
    cikti: dict[float, float] = {}
    for etki in etkiler:
        ret = 0
        for _ in range(b):
            d = rng.choice(g, size=n, replace=True) + etki
            ret += wilcoxon_eslestirilmis(d, np.zeros(n)).p < sinir
        cikti[float(etki)] = ret / b
    return cikti


def mde80(egri: Mapping[float, float]) -> float | None:
    """Gücün 0,80'i ilk geçtiği etki — ızgara üzerinde doğrusal ara
    değerleme. Hiçbir noktada geçilmiyorsa `None` (tohum kuralı, §0.4.3 (4))."""
    noktalar = sorted(egri.items())
    for (e0, g0), (e1, g1) in zip(noktalar, noktalar[1:]):
        if g0 < 0.80 <= g1:
            return e0 + (0.80 - g0) * (e1 - e0) / (g1 - g0)
    if noktalar and noktalar[0][1] >= 0.80:
        return noktalar[0][0]
    return None
