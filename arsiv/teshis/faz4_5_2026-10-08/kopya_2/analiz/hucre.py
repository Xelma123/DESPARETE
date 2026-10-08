"""
HÜCRE KOŞUCUSU — ön-kaydın Aile 2 tablosu (`v2/06` §0.4.1–§0.4.2) · K-189.

    δ     : taban protokollerin GELİŞTİRME tohumlarındaki eşleştirilmiş
            farklarının en gürültülü çiftinden (§0.4.2) — özgün protokolün
            hiçbir koşusu δ'ya girmez
    H2.x  : özgün ↔ rakip, ANA DENEY tohumlarında eşleştirilmiş çift yönlü
            Wilcoxon; m = rakip sayısı, Holm aile içinde (§0.4.1)
    hüküm : üstün · aşağı · ayırt edilemedi (§0.4.2 tablosu); mekanizma
            kapısı (Aile 3) dışarıdan verilir

🔒 Girdi JSONL satırlarıdır (simülatör içe aktarılmaz). Her kol bir satır
listesidir; eşleştirme, kimlik denetimi ve geçerlilik süzgeci `satir.py`de.
Dışlanan satırlar ve eşi düşen tohumlar TABLOYA yazılır, gizlenmez.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Mapping, Sequence

from analiz.istatistik import (dogrula, delta_esigi, holm, hukum,
                               ortalama_fark_ga, wilcoxon_eslestirilmis)
from analiz.satir import eslestir, gecerli_suz

__all__ = ["KarsilastirmaSatiri", "delta_gelistirme", "aile2_tablosu"]


@dataclass(frozen=True)
class KarsilastirmaSatiri:
    rakip: str
    n: int
    ort_fark: float
    ga_alt: float
    ga_ust: float
    p: float
    p_holm: float
    yontem: str
    hukum: str
    dislanan: tuple
    esi_dusen: tuple


def delta_gelistirme(taban: Mapping[str, Sequence[dict]], metrik: str,
                     n_ana: int) -> float:
    """§0.4.2: δ = 2 · max SD(d_XY) / √n_ana — taban protokollerin
    geliştirme tohumlarındaki eşleştirilmiş farklarından."""
    dogrula(len(taban) >= 2, "δ en az iki taban protokol ister")
    farklar: dict[str, list[float]] = {}
    for a, b in combinations(sorted(taban), 2):
        ga, _ = gecerli_suz(taban[a])
        gb, _ = gecerli_suz(taban[b])
        _, x, y, _ = eslestir(ga, gb, metrik)
        farklar[f"{a}-{b}"] = [xi - yi for xi, yi in zip(x, y)]
    return delta_esigi(farklar, n_ana)


def aile2_tablosu(ozgun: Sequence[dict], rakipler: Mapping[str, Sequence[dict]],
                  metrik: str, delta: float,
                  mekanizma_kapisi: bool) -> list[KarsilastirmaSatiri]:
    """H2.a–c: özgün ↔ her rakip. Holm, rakip sayısı kadar testlik ailede."""
    dogrula(len(rakipler) >= 1 and delta > 0.0, "rakip ve δ > 0 gerekli")
    go, do = gecerli_suz(ozgun)
    ara = []
    for ad in sorted(rakipler):
        gr, dr = gecerli_suz(rakipler[ad])
        tohum, x, y, dusen = eslestir(go, gr, metrik)
        w = wilcoxon_eslestirilmis(x, y)
        ort, alt, ust = ortalama_fark_ga(x, y)
        ara.append((ad, len(tohum), ort, alt, ust, w, tuple(do + dr),
                    tuple(dusen)))
    p_holm = holm([s[5].p for s in ara])
    return [KarsilastirmaSatiri(
        rakip=ad, n=n, ort_fark=ort, ga_alt=alt, ga_ust=ust, p=w.p,
        p_holm=ph, yontem=w.yontem,
        hukum=hukum(ph, ort, delta, mekanizma_kapisi),
        dislanan=dis, esi_dusen=dusen)
        for (ad, n, ort, alt, ust, w, dis, dusen), ph in zip(ara, p_holm)]
