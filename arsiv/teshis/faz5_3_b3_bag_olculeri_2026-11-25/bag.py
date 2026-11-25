"""
Faz 5-3 · B3 teşhisi — saf işlevler (`beklenti.md` "Tanımlar"). Simülatörü
bilmez; birim sınaması `sinama/saf.py`. Ölçüm aleti `olcum.py` ve karar hesabı
`sonuc_hesap.py` buradan içe aktarır.

1. `b1_selam`: B1'in selam sayımı ve `d_f`'si (`v2/bilesen/B1-KOMSU-VE-BAG.md`
   kural 1, 3–7, 11–12, 20), bir bağ için (i, j'nin selamlarını sayar). Sorgu
   anlarında NEDENSEL görünüm: yalnız sorgudan önceki olaylar işlenir.
2. `e_selam`, `e_veri`: B1 kural 13–14.
3. Veri kayıtlarının sıkıştırılmış biçimi (`kod`, `ozet`) ve tahmin hatası
   (`hata`).

Değerler B1'inkilerdir (`v2/bilesen/00-DIZIN.md`); teşhisin kendi değerleri
`beklenti.md`dedir.
"""

from __future__ import annotations

import bisect
import math

# --- B1'in değerleri (`v2/bilesen/00-DIZIN.md`) -------------------------------
N_SELAM = 16
SELAM_SAKLA = 128
ZAMAN_ASIMI_KATSAYI = 1.5
ARALIK_EN_AZ = 0.01
BOSLUK_EN_COK = 64
DF_UNUT_S = 30.0
T_SILME = 30.0
VERI_PENCERE = 16
VERI_PENCERE_S = 30.0
# --- teşhisin değerleri (`beklenti.md` "Tanımlar") ----------------------------
GELECEK_K = 16          # sonraki veri bedeli: en çok 16 kayıt …
GELECEK_S = 30.0        # … en çok 30 s ileri
TAVAN = 64.0            # hatada ∞ ve çok büyük maliyetin tavanı

INF = math.inf


def sira_farki(yeni: int, eski: int) -> int:
    """(yeni − eski) mod 2^16, [−32768, 32767] aralığına çevrilmiş."""
    f = (yeni - eski) & 0xFFFF
    return f - 0x10000 if f >= 0x8000 else f


def _ekle(o: list, ornek: tuple) -> None:
    """Zaman sıralı örnek listesine ekler; `SELAM_SAKLA`'yı aşan en eskisi
    atılır. Örnek: (an, 1 | 0, oran | None)."""
    if not o or o[-1][0] <= ornek[0]:
        o.append(ornek)
    else:
        anlar = [x[0] for x in o]
        o.insert(bisect.bisect_right(anlar, ornek[0]), ornek)
    if len(o) > SELAM_SAKLA:
        del o[0]


def b1_selam(gelisler: list, tazeler: list, sorgular: list) -> list:
    """Bir bağın (i ← j) B1 selam sayımı.

    `gelisler`: [(an, sıra, aralık s, j'nin benim için bildirdiği oran ya da
    None)], zaman sırasında. `tazeler`: [an], sıralı — j'nin selam dışındaki
    duyulma anları; yalnız silmeyi erteler (B1 kural 2–3). `sorgular`: [an],
    sıralı.

    Döner, her sorgu için `(d_r, n_s, d_f, kayitli)`: sorgudan ÖNCEKİ olaylarla
    (an < sorgu) güncel kayıt; `d_r` son `N_SELAM` örnekteki 1'lerin payı
    (n_s = 0 ise None); `d_f` oranı olan en yeni örneğin oranı, `DF_UNUT_S`'den
    eskiyse None. Aynı anda olaylar: önce zaman aşımı, sonra silme, sonra
    tazeleme, en son selam (kural 20).
    """
    o: list = []
    beklenen = son_t = a = None
    asim = sil = INF
    son_duyulma = None
    gi = ti = 0
    ng, nt = len(gelisler), len(tazeler)
    out: list = []
    for T in sorgular:
        while True:
            t_g = gelisler[gi][0] if gi < ng else INF
            t_z = tazeler[ti] if ti < nt else INF
            t_a = asim if beklenen is not None else INF
            t_s = sil if beklenen is not None else INF
            t_ev = min(t_g, t_z, t_a, t_s)
            if not t_ev < T:
                break
            if t_a == t_ev:                                  # zaman aşımı (5)
                _ekle(o, (asim, 0, None))
                beklenen = (beklenen + 1) & 0xFFFF
                asim += a
            elif t_s == t_ev:                                # silme (3)
                o = []
                beklenen = son_t = a = None
                asim = sil = INF
                son_duyulma = None
            elif t_z == t_ev:                                # duyulma (2)
                ti += 1
                if beklenen is not None:
                    son_duyulma = max(son_duyulma, t_z)
                    sil = son_duyulma + T_SILME
            else:                                            # selam (1, 4, 7)
                t, sira, aralik, oran = gelisler[gi]
                gi += 1
                aralik = max(float(aralik), ARALIK_EN_AZ)
                if beklenen is None:
                    o = [(t, 1, oran)]
                else:
                    fark = sira_farki(sira, beklenen)
                    if fark == 0:
                        _ekle(o, (t, 1, oran))
                    elif 0 < fark <= BOSLUK_EN_COK:
                        for k in range(1, fark + 1):
                            _ekle(o, (son_t + k * (t - son_t) / (fark + 1),
                                      0, None))
                        _ekle(o, (t, 1, oran))
                    elif -BOSLUK_EN_COK <= fark < 0:
                        del o[max(0, len(o) + fark):]
                        _ekle(o, (t, 1, oran))
                    else:
                        o = [(t, 1, oran)]
                beklenen = (sira + 1) & 0xFFFF
                son_t, a = t, aralik
                asim = t + ZAMAN_ASIMI_KATSAYI * a
                son_duyulma = t if son_duyulma is None else max(son_duyulma, t)
                sil = son_duyulma + T_SILME
        if beklenen is None:
            out.append((None, 0, None, False))
            continue
        son = o[-N_SELAM:]
        n_s = len(son)
        d_r = sum(x[1] for x in son) / n_s if n_s else None
        d_f = None
        for t, _, r in reversed(o):
            if r is not None:
                if T - t <= DF_UNUT_S:
                    d_f = r
                break
        out.append((d_r, n_s, d_f, True))
    return out


def e_selam(d_f: float | None, d_r: float | None) -> float:
    """B1 kural 13: 1 / (d_f · d_r); biri tanımsız ya da 0 ise ∞."""
    if d_f is None or d_r is None or d_f <= 0.0 or d_r <= 0.0:
        return INF
    return 1.0 / (d_f * d_r)


def e_veri(D: int, G: int, n: int) -> float | None:
    """B1 kural 14: D / G; G = 0 ve n > 0 ise ∞; n = 0 ise tanımsız."""
    if n == 0:
        return None
    return INF if G == 0 else D / G


# --- veri kayıtlarının sıkıştırılmış biçimi ----------------------------------
def kod(deneme: int, onay: bool) -> str:
    """Bir veri kaydı tek karakter: onay k'ıncı denemede geldiyse "k" (1–7),
    vazgeçildiyse "x" (7 deneme)."""
    if not onay:
        return "x"
    if not 1 <= deneme <= 7:
        raise ValueError(f"deneme {deneme}")
    return str(deneme)


def ozet(kodlar: str, n: int, sondan: bool = True) -> tuple[int, int, int]:
    """(n_v, D, G): `kodlar`ın en yeni (`sondan`) ya da en eski n kaydı."""
    parca = kodlar[-n:] if sondan else kodlar[:n]
    if n <= 0:
        parca = ""
    D = sum(7 if c == "x" else int(c) for c in parca)
    G = sum(c != "x" for c in parca)
    return len(parca), D, G


def hata(tahmin: float, gercek: float) -> float:
    """|log2(tahmin / gerçek)|, iki değer `TAVAN`'da kırpılarak (∞ = TAVAN).
    İkisi de ≥ 1 olmalı (beklenen deneme sayısı)."""
    a = min(tahmin, TAVAN)
    b = min(gercek, TAVAN)
    return abs(math.log2(a / b))
