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
from analiz.satir import donem_pdr, eslestir, gecerli_suz

__all__ = ["KarsilastirmaSatiri", "delta_gelistirme", "aile2_tablosu",
           "FarkIcindeFark", "fark_icinde_fark_tablosu"]


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


@dataclass(frozen=True)
class FarkIcindeFark:
    rakip: str
    n: int
    ort: float
    ga_alt: float
    ga_ust: float
    p: float
    p_holm: float
    yontem: str
    esi_dusen: tuple


def _acik_pdr_ekle(satirlar: Sequence[dict],
                   cizelge: Sequence[float] | None) -> list[dict]:
    return [{**s, "turetilen": {"pdr_acik": donem_pdr(s, True, cizelge)}}
            for s in satirlar]


def fark_icinde_fark_tablosu(ozgun: Sequence[dict],
                             rakipler: Mapping[str, Sequence[dict]],
                             ozgun_ikiz: Sequence[dict],
                             rakipler_ikiz: Mapping[str, Sequence[dict]],
                             cizelge: Sequence[float]
                             ) -> list[FarkIcindeFark]:
    """K-222 (denetim D-01) · ön-kayıtlı İKİNCİL test — karıştırmaya özgü
    kazanç. Tohum başına

        DiD(s) = [PDR_açık(D) − PDR_açık(R)]_birincil
               − [PDR_açık(D) − PDR_açık(R)]_ikiz

    İkiz = aynı tohumlarda karıştırıcısız hücre; "açık" orada aynı çizelgenin
    HAYALET dönemleri. Eşleştirilmiş çift yönlü Wilcoxon (DiD ↔ 0), Holm rakip
    sayısı kadar testlik ailede. Bir tohum dört satırın hepsinde yoksa düşer
    ve yazılır."""
    dogrula(len(rakipler) >= 1 and set(rakipler) == set(rakipler_ikiz),
            "her rakibin birincil ve ikiz kolu olmalı")
    go = _acik_pdr_ekle(gecerli_suz(ozgun)[0], None)
    goi = _acik_pdr_ekle(gecerli_suz(ozgun_ikiz)[0], cizelge)
    ara = []
    for ad in sorted(rakipler):
        gr = _acik_pdr_ekle(gecerli_suz(rakipler[ad])[0], None)
        gri = _acik_pdr_ekle(gecerli_suz(rakipler_ikiz[ad])[0], cizelge)
        tb, xb, yb, db = eslestir(go, gr, "turetilen.pdr_acik")
        ti, xi, yi, di = eslestir(goi, gri, "turetilen.pdr_acik")
        fb = dict(zip(tb, (a - b for a, b in zip(xb, yb))))
        fi = dict(zip(ti, (a - b for a, b in zip(xi, yi))))
        ortak = sorted(set(fb) & set(fi))
        dogrula(len(ortak) > 0, f"{ad}: birincil ve ikizin ortak tohumu yok")
        x, y = [fb[t] for t in ortak], [fi[t] for t in ortak]
        w = wilcoxon_eslestirilmis(x, y)
        ort, alt, ust = ortalama_fark_ga(x, y)
        dusen = tuple(sorted(set(db) | set(di) | (set(fb) ^ set(fi))))
        ara.append((ad, len(ortak), ort, alt, ust, w, dusen))
    p_holm = holm([a[5].p for a in ara])
    return [FarkIcindeFark(rakip=ad, n=n, ort=ort, ga_alt=alt, ga_ust=ust,
                           p=w.p, p_holm=ph, yontem=w.yontem, esi_dusen=d)
            for (ad, n, ort, alt, ust, w, d), ph in zip(ara, p_holm)]
