"""
Faz 5-3 · B3 teşhisinin karar hesabı (`beklenti.md` "Karar kuralı", K0–K6).
Kayıtlardan okur; simülasyon yok.

    PYTHONIOENCODING=utf-8 py -3.11 <bu dosya> [<klasör>] > sonuc_hesap.txt

<klasör> verilmezse bu dosyanın dizini (`kayit_<hücre>.json.gz`). Duman için
`duman/`: orada doğrulama yarısı yoktur, hüküm verilmez; yalnız geçerlilik
(K0) ve aletin çalıştığı denetlenir.
"""

from __future__ import annotations

import bisect
import gzip
import json
import math
import statistics as ist
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))

import bag as B  # noqa: E402

HUCRELER = ("ikiz", "birincil")
SECIM = (1003, 1004, 1005, 1006)
DOGRULAMA = (1007, 1008, 1009, 1010)
B2 = D.parent / "faz5_3_b2_isaretler_2026-11-24"

# --- karar kuralının eşikleri (`beklenti.md`) -----------------------------------
FARK_SECIM = 0.10             # bit: seçim yarısında "daha iyi"
FARK_DOGRULAMA = 0.05         # bit: doğrulama yarısında
AKTARIM = 0.5                 # bit: kullanılan ↔ kullanılmayan bağ farkı
YETER = 8                     # önceki kayıt (S1, K2, K4, K5)
F_EN_AZ = 4                   # sonraki bedel için en az kayıt
NLER = (1, 2, 3, 4, 6, 8, 12, 16)
YAS_DILIM = ((0.0, 2.0), (2.0, 5.0), (5.0, 10.0), (10.0, 20.0), (20.0, 30.0))
DILIM_EN_AZ = 30
OYNAMA_BIT, OYNAMA_PAY = 1.0, 0.10
OYNAMA_ARA = (9.0, 11.0)
D2_PENCERE_S, D2_EN_AZ = 60.0, 3
KAHIN_IYI = 0.28              # 7 denemelik başarının "iyi" bandının sınırı
ERKEN_S = 3.0
TEMIZ = "ios"                 # ikiz · önce · sessiz


def oku(klasor: Path) -> dict[str, list]:
    kayit: dict[str, list] = {}
    for h in HUCRELER:
        yol = klasor / f"kayit_{h}.json.gz"
        if yol.exists():
            with gzip.open(yol, "rt", encoding="utf-8") as f:
                k = json.load(f)
            kayit[h] = [r for r in k["sonuc"] if "hata" not in r]
    return kayit


def kap(x: float) -> float:
    return min(x, B.TAVAN)


def lg(x: float) -> float:
    return math.log2(kap(x))


def ev(once: str, n: int) -> float | None:
    """`E_veri`: en yeni n kayıt (varsa)."""
    nv, Dd, G = B.ozet(once, n)
    return B.e_veri(Dd, G, nv)


def omh(degerler: list[float]) -> float | None:
    return ist.median(degerler) if degerler else None


def fmt(x, ondalik=3) -> str:
    return "—" if x is None else f"{x:.{ondalik}f}"


# ==============================================================================
# Örnekler
# ==============================================================================
class Ornek:
    __slots__ = ("hucre", "tohum", "t", "i", "j", "Es", "once", "yas", "F",
                 "p", "yuk_i", "yuk_j", "evre", "alan")


def veri_ornekleri(kayit: dict) -> list[Ornek]:
    out: list[Ornek] = []
    for h, rs in kayit.items():
        for r in rs:
            for (t_ms, i, j, dr, ns, df, kayitli, once, yas, gel, p, yi, yj,
                 evre, alan) in r["kaydedici"]["veri"]:
                o = Ornek()
                o.hucre, o.tohum, o.t, o.i, o.j = h, r["tohum"], t_ms / 1000, i, j
                o.Es = B.e_selam(None if df < 0 else df / 1000,
                                 None if dr < 0 else dr / 1000)
                o.once, o.yas = once, (None if yas < 0 else yas / 1000)
                nf, Df, Gf = B.ozet(gel, len(gel), sondan=False)
                o.F = B.e_veri(Df, Gf, nf) if nf >= F_EN_AZ else None
                o.p, o.yuk_i, o.yuk_j = p / 1000, yi, yj
                o.evre, o.alan = evre, alan
                out.append(o)
    return out


# ==============================================================================
# K0 · geçerlilik
# ==============================================================================
ALANLAR = ("pdr", "pdr_pencere", "uretilen", "teslim", "sayaclar",
           "teshis_toplam")


def k0(kayit: dict, duman: bool) -> bool:
    print("== K0 · geçerlilik ==")
    tamam = True
    for h, rs in kayit.items():
        gecersiz = [r["tohum"] for r in rs if not r["gecerli"]]
        denetim = [(r["tohum"], r["kaydedici_denetim"]) for r in rs
                   if r["kaydedici_denetim"]]
        kd = [r["kaydedici"]["sayim"] for r in rs]
        print(f"  {h:<9} koşu {len(rs)} · geçersiz {gecersiz or 'yok'} · iç "
              f"denetim {denetim or 'tamam'} · veri örneği "
              f"{sum(len(r['kaydedici']['veri']) for r in rs)} · ızgara "
              f"{sum(len(r['kaydedici']['izgara']) for r in rs)} · kâhin "
              f"çağrısı {sum(z['kahin_cagri'] for z in kd)}")
        tamam &= not gecersiz and not denetim
    for h in kayit:
        yol = (B2 / "duman" / f"duz_{h}.json") if duman else (
            B2 / f"kayit_{h}.json")
        if not yol.exists():
            print(f"  birebirlik {h}: karşılaştırma dosyası yok ({yol})")
            tamam = False
            continue
        k = json.loads(yol.read_text(encoding="utf-8"))
        ote = {r["tohum"]: r for r in k["sonuc"] if "hata" not in r}
        farkli, eslesen = [], 0
        for r in kayit[h]:
            o = ote.get(r["tohum"])
            if o is None:
                continue
            eslesen += 1
            f = [x for x in ALANLAR if r.get(x) != o.get(x)]
            if f:
                farkli.append((r["tohum"], f))
        print(f"  birebirlik {h:<9} ↔ {yol.relative_to(D.parent)}: {eslesen} "
              f"eşleşen · {'birebir' if eslesen and not farkli else farkli}")
        tamam &= eslesen > 0 and not farkli
    print(f"  hüküm: {'geçerli' if tamam else 'GEÇERSİZ — tablolar kullanılmaz'}\n")
    return tamam


# ==============================================================================
# S1 · ayrışma (betimleyici)
# ==============================================================================
def s1(ornek: list[Ornek]) -> None:
    print("== S1 · ayrışma: log2(E_veri / E_selam), kullanılan bağ (temiz sınıf, "
          f"≥ {YETER} önceki kayıt, E_selam sonlu) ==")
    for h in HUCRELER:
        x = [lg(ev(o.once, 16)) - lg(o.Es) for o in ornek
             if o.hucre == h and o.evre in TEMIZ and len(o.once) >= YETER
             and math.isfinite(o.Es)]
        if x:
            q = np.quantile(x, [0.25, 0.5, 0.75])
            print(f"  {h:<9} n {len(x)} · ortanca {q[1]:+.3f} · çeyrekler "
                  f"{q[0]:+.3f} … {q[2]:+.3f} · E_veri > E_selam payı "
                  f"{np.mean(np.array(x) > 0):.3f}")
    print()


# ==============================================================================
# K1 · dönüşüm
# ==============================================================================
def d2_katsayilari(ornek: list[Ornek]) -> dict:
    """(hücre, tohum, i) → zaman sıralı [(t, j, log2(E_veri/E_selam))]."""
    g: defaultdict = defaultdict(list)
    for o in ornek:
        if len(o.once) >= YETER and math.isfinite(o.Es):
            g[(o.hucre, o.tohum, o.i)].append(
                (o.t, o.j, lg(ev(o.once, 16)) - lg(o.Es)))
    for v in g.values():
        v.sort()
    return g


def d2_tahmin(o: Ornek, g: dict) -> float:
    v = g.get((o.hucre, o.tohum, o.i), [])
    anlar = [x[0] for x in v]
    a = bisect.bisect_left(anlar, o.t - D2_PENCERE_S)
    b = bisect.bisect_left(anlar, o.t)
    oran = [x[2] for x in v[a:b] if x[1] != o.j]
    if len(oran) < D2_EN_AZ:
        return o.Es
    return o.Es * 2.0 ** ist.median(oran)


def k1(ornek: list[Ornek], kayit: dict, duman: bool) -> tuple:
    print("== K1 · selamın dönüşümü (S4) ==")
    kume = [o for o in ornek if o.evre in TEMIZ and math.isfinite(o.Es)
            and o.F is not None]
    sec = [o for o in kume if duman or o.tohum in SECIM]
    dog = [o for o in kume if o.tohum in DOGRULAMA]
    if not sec:
        print("  örnek yok\n")
        return "D0", 1.0, None
    log_k = ist.median([lg(o.F) - lg(o.Es) for o in sec])
    k_g = 2.0 ** log_k
    g = d2_katsayilari(ornek)

    def tahmin(ad: str, o: Ornek) -> float:
        if ad == "D0":
            return o.Es
        if ad == "D1":
            return o.Es * k_g
        return d2_tahmin(o, g)

    def olc(kume_: list[Ornek]) -> dict:
        return {ad: omh([B.hata(tahmin(ad, o), o.F) for o in kume_])
                for ad in ("D0", "D1", "D2")}

    s = olc(sec)
    print(f"  genel katsayı (seçim yarısı): log2 k = {log_k:+.3f} (k = {k_g:.3f})")
    print(f"  seçim yarısı (n {len(sec)}): OMH D0 {fmt(s['D0'])} · D1 "
          f"{fmt(s['D1'])} · D2 {fmt(s['D2'])} bit")
    en_iyi = min(("D0", "D1", "D2"), key=lambda a: s[a])
    secilen = en_iyi if (en_iyi == "D0"
                         or s[en_iyi] <= s["D0"] - FARK_SECIM) else "D0"
    print(f"  seçilen: {secilen}")
    # aktarılabilirlik: ızgara, kâhine göre selamın kötümserliği
    x_k, x_y = [], []
    for h, rs in kayit.items():
        for r in rs:
            for (_t, _i, _j, dr, _ns, df, once, p, evre, _a) in \
                    r["kaydedici"]["izgara"]:
                if evre not in TEMIZ or p <= 0:
                    continue
                Es = B.e_selam(None if df < 0 else df / 1000,
                               None if dr < 0 else dr / 1000)
                if not math.isfinite(Es):
                    continue
                x = lg(Es) + math.log2(p / 1000)
                (x_k if once else x_y).append(x)
    fark = (ist.median(x_y) - ist.median(x_k)) if x_k and x_y else None
    aktar = fark is not None and abs(fark) <= AKTARIM
    print(f"  aktarılabilirlik (ızgara, temiz sınıf): log2(E_selam · p) ortancası "
          f"kullanılan {fmt(omh(x_k))} (n {len(x_k)}) · kullanılmayan "
          f"{fmt(omh(x_y))} (n {len(x_y)}) · fark {fmt(fark)} bit → "
          f"{'aktarılabilir' if aktar else 'aktarılamaz'}")
    hukum = "D0"
    if not duman and dog:
        d = olc(dog)
        print(f"  doğrulama yarısı (n {len(dog)}): OMH D0 {fmt(d['D0'])} · D1 "
              f"{fmt(d['D1'])} · D2 {fmt(d['D2'])} bit")
        if secilen != "D0":
            iyi = d[secilen] <= d["D0"] - FARK_DOGRULAMA
            if iyi and aktar:
                hukum = secilen
                print(f"  hüküm K1: dönüşüm var ({secilen})")
            elif iyi:
                print(f"  hüküm K1: {secilen} kullanılan bağlarda iyi ama "
                      f"aktarılamaz → kullanılmayan bağlara uygulanmaz (D0); "
                      f"fark B4'ün geçiş kuralına not edilir")
            else:
                print(f"  hüküm K1: dönüşüm yok ({secilen} doğrulamada "
                      f"tutmadı)")
        else:
            print("  hüküm K1: dönüşüm yok (D0)")
    print()
    return hukum, k_g, g


def es_yildiz(o: Ornek, hukum: str, k_g: float, g: dict | None) -> float:
    if hukum == "D1":
        return o.Es * k_g
    if hukum == "D2" and g is not None:
        return d2_tahmin(o, g)
    return o.Es


# ==============================================================================
# K2 · verinin üstünlüğü · K3 · yeterli kayıt ve tazelik
# ==============================================================================
def k2(ornek, hukum, k_g, g, duman: bool) -> bool | None:
    print("== K2 · verinin üstünlüğü (S2): OMH(E_veri, ≤ 16 kayıt) ↔ OMH(Ês*) ==")
    kume = [o for o in ornek if o.evre in TEMIZ and math.isfinite(o.Es)
            and o.F is not None and len(o.once) >= YETER]
    sonuc = None
    for ad, tohum in (("seçim", SECIM), ("doğrulama", DOGRULAMA)):
        k = [o for o in kume if duman or o.tohum in tohum]
        if not k:
            continue
        a = omh([B.hata(ev(o.once, 16), o.F) for o in k])
        b = omh([B.hata(es_yildiz(o, hukum, k_g, g), o.F) for o in k])
        print(f"  {ad:<9} n {len(k)} · E_veri {fmt(a)} · Ês* {fmt(b)} bit")
        for h in HUCRELER:
            kh = [o for o in k if o.hucre == h]
            if kh:
                print(f"    {h:<9} n {len(kh)} · E_veri "
                      f"{fmt(omh([B.hata(ev(o.once, 16), o.F) for o in kh]))} · "
                      f"Ês* {fmt(omh([B.hata(es_yildiz(o, hukum, k_g, g), o.F) for o in kh]))}")
        if ad == "doğrulama" and not duman:
            sonuc = a <= b - FARK_SECIM
        if duman:
            break
    if sonuc is not None:
        print(f"  hüküm K2: {'veri üstün' if sonuc else 'veri üstün DEĞİL'}")
    print()
    return sonuc


def k3(ornek, hukum, k_g, g, duman: bool) -> None:
    print("== K3 · yeterli kayıt ve tazelik (S3) ==")
    kume = [o for o in ornek if o.evre in TEMIZ and math.isfinite(o.Es)
            and o.F is not None]
    yarilar = (("seçim", SECIM),) if duman else (("seçim", SECIM),
                                                 ("doğrulama", DOGRULAMA))
    tablo: dict = {}
    for ad, tohum in yarilar:
        k = [o for o in kume if duman or o.tohum in tohum]
        print(f"  {ad}: n · örnek · OMH E_veri(son n) · OMH Ês* (aynı örnekler)")
        for n in NLER:
            kn = [o for o in k if len(o.once) >= n]
            a = omh([B.hata(ev(o.once, n), o.F) for o in kn])
            b = omh([B.hata(es_yildiz(o, hukum, k_g, g), o.F) for o in kn])
            tablo[(ad, n)] = (a, b, len(kn))
            print(f"    {n:>2} · {len(kn):>6} · {fmt(a)} · {fmt(b)}")
    en_az = next((n for n in NLER
                  if tablo.get(("seçim", n), (None,))[0] is not None
                  and tablo[("seçim", n)][0] <= tablo[("seçim", n)][1]
                  - FARK_DOGRULAMA), None)
    print(f"  VERI_EN_AZ (seçim yarısı): {en_az if en_az is not None else 'yok'}")
    if not duman and en_az is not None:
        a, b, _ = tablo[("doğrulama", en_az)]
        if a is not None and a <= b:
            print(f"  doğrulama: n = {en_az}'de E_veri {fmt(a)} ≤ Ês* {fmt(b)} "
                  f"→ doğrulandı")
        else:
            n2 = next((n for n in NLER if tablo[("doğrulama", n)][0] is not None
                       and tablo[("doğrulama", n)][0]
                       <= tablo[("doğrulama", n)][1]), None)
            print(f"  doğrulama: n = {en_az}'de tutmadı; doğrulamada sağlayan en "
                  f"küçük n: {n2 if n2 is not None else 'yok'}")
    # tazelik
    if en_az is None:
        print()
        return
    for ad, tohum in yarilar:
        k = [o for o in kume if (duman or o.tohum in tohum)
             and len(o.once) >= en_az and o.yas is not None]
        dilimler, birikim, sinir_tam = [], [], None
        for alt, ust in YAS_DILIM:
            birikim += [o for o in k if alt <= o.yas < ust
                        or (ust == YAS_DILIM[-1][1] and o.yas == ust)]
            if len(birikim) >= DILIM_EN_AZ or ust == YAS_DILIM[-1][1]:
                a = omh([B.hata(ev(o.once, 16), o.F) for o in birikim])
                b = omh([B.hata(es_yildiz(o, hukum, k_g, g), o.F)
                         for o in birikim])
                dilimler.append((ust, len(birikim), a, b))
                birikim = []
        print(f"  tazelik, {ad}: üst sınır (s) · örnek · OMH E_veri · OMH Ês*")
        for ust, n, a, b in dilimler:
            print(f"    ≤ {ust:>4.0f} · {n:>6} · {fmt(a)} · {fmt(b)}")
        if ad == "seçim":
            for ust, n, a, b in dilimler:
                if a is None or b is None or a > b:
                    break
                sinir_tam = ust
            print(f"  VERI_TAZE_S (seçim yarısı): "
                  f"{sinir_tam if sinir_tam is not None else 0} s")
    print()


# ==============================================================================
# K4 · yükle oynama
# ==============================================================================
def siralama_korelasyonu(x: list[float], y: list[float]) -> float | None:
    if len(x) < 3:
        return None
    rx = np.argsort(np.argsort(x)).astype(float)
    ry = np.argsort(np.argsort(y)).astype(float)
    return float(np.corrcoef(rx, ry)[0, 1])


def k4(ornek: list[Ornek]) -> None:
    print("== K4 · yükle oynama (S5), ikiz, bütün tohumlar ==")
    bag: defaultdict = defaultdict(list)
    for o in ornek:
        if o.hucre == "ikiz" and len(o.once) >= YETER:
            bag[(o.tohum, o.i, o.j)].append(o)
    cift = buyuk = 0
    for v in bag.values():
        v.sort(key=lambda o: o.t)
        anlar = [o.t for o in v]
        for o in v:
            b = bisect.bisect_left(anlar, o.t + OYNAMA_ARA[0])
            if b < len(v) and v[b].t <= o.t + OYNAMA_ARA[1]:
                cift += 1
                d = abs(lg(ev(v[b].once, 16)) - lg(ev(o.once, 16)))
                buyuk += d >= OYNAMA_BIT
    pay = buyuk / cift if cift else None
    print(f"  çift {cift} · ≥ {OYNAMA_BIT:.0f} bit değişen {buyuk} · pay {fmt(pay)}"
          f" → {'oynama büyük' if pay is not None and pay > OYNAMA_PAY else 'oynama küçük'}")
    x = [o for o in ornek if o.hucre == "ikiz" and len(o.once) >= YETER
         and o.yuk_i >= 0 and o.yuk_j >= 0]
    e = [lg(ev(o.once, 16)) for o in x]
    print(f"  sıra korelasyonu log2 E_veri ↔ göndericinin yükü "
          f"{fmt(siralama_korelasyonu(e, [o.yuk_i for o in x]))} · ↔ alıcının "
          f"yükü {fmt(siralama_korelasyonu(e, [o.yuk_j for o in x]))} (n {len(x)})")
    print()


# ==============================================================================
# K5 · selamı geçen, veriyi taşımayan bağ
# ==============================================================================
def k5(ornek: list[Ornek]) -> None:
    print("== K5 · selamı geçen, veriyi taşımayan bağ (S6; betimleyici) ==")
    for h in HUCRELER:
        k = [o for o in ornek if o.hucre == h and o.evre in TEMIZ
             and len(o.once) >= YETER and math.isfinite(o.Es)]
        if not k:
            continue
        isaret = [o.Es <= 2.0 and (ev(o.once, 16) or 0) >= 4.0 for o in k]
        bag_hepsi = {(o.tohum, o.i, o.j) for o in k}
        bag_isaret = {(o.tohum, o.i, o.j) for o, s in zip(k, isaret) if s}
        sure = []
        grup: defaultdict = defaultdict(list)
        for o, s in zip(k, isaret):
            grup[(o.tohum, o.i, o.j)].append((o.t, s))
        for v in grup.values():
            v.sort()
            bas = onceki = None
            for t, s in v + [(math.inf, False)]:
                if s and bas is not None and t - onceki <= 2.0:
                    onceki = t
                    continue
                if bas is not None:
                    sure.append(onceki - bas + 1.0)
                    bas = onceki = None
                if s:
                    bas = onceki = t
        isaretli = [o for o, s in zip(k, isaret) if s]
        iyi = (np.mean([o.p >= KAHIN_IYI for o in isaretli])
               if isaretli else None)
        print(f"  {h:<9} örneklerin {np.mean(isaret):.4f}'ü (n {len(k)}) · "
              f"bağların {len(bag_isaret) / len(bag_hepsi):.3f}'i "
              f"({len(bag_isaret)}/{len(bag_hepsi)}) · süre ortancası "
              f"{fmt(omh(sure), 1)} s · kâhine göre iyi payı {fmt(iyi)}")
    print()


# ==============================================================================
# K6 · karıştırma altında
# ==============================================================================
def k6(ornek: list[Ornek], kayit: dict) -> None:
    print("== K6 · karıştırma altında (S7; betimleyici), birincil ==")
    if "birincil" not in kayit:
        print("  kayıt yok\n")
        return
    bag: defaultdict = defaultdict(list)
    for o in ornek:
        if o.hucre == "birincil":
            bag[(o.tohum, o.i, o.j)].append(o)
    for v in bag.values():
        v.sort(key=lambda o: o.t)
    sonuc = {"G": [], "E": []}         # (ev gecikmesi, es gecikmesi, dönemde örnek var)
    for r in kayit["birincil"]:
        kd = r["kaydedici"]
        S = kd["S"]
        for on, off in kd["donemler"]:
            orta = min(S - 1, int((on + off) / 2))
            for (tohum, i, j), v in bag.items():
                if tohum != r["tohum"] or kd["alan"][j][orta] not in "GE":
                    continue
                once = [o for o in v if on - 10.0 <= o.t < on and o.once
                        and math.isfinite(o.Es)]
                if not once:
                    continue
                son = once[-1]
                ev_once = ev(son.once, 16)
                if ev_once is None or not math.isfinite(ev_once):
                    continue
                icinde = [o for o in v if on <= o.t < off]
                g_ev = next((o.t - on for o in icinde if o.once and
                             (ev(o.once, 4) or 0) >= 2.0 * ev_once), None)
                g_es = next((o.t - on for o in icinde
                             if o.Es >= 2.0 * son.Es), None)
                sonuc[kd["alan"][j][orta]].append((g_ev, g_es, bool(icinde)))
    for alan, v in sonuc.items():
        if not v:
            continue
        n = len(v)

        def pay(f) -> float:
            return sum(1 for x in v if f(x)) / n
        print(f"  {alan} (bağ-dönem {n}; dönem içinde örneği olan "
              f"{pay(lambda x: x[2]):.3f}): E_veri 2 katına 3 s içinde "
              f"{pay(lambda x: x[0] is not None and x[0] <= ERKEN_S):.3f} · dönem "
              f"içinde {pay(lambda x: x[0] is not None):.3f} | E_selam 3 s içinde "
              f"{pay(lambda x: x[1] is not None and x[1] <= ERKEN_S):.3f} · dönem "
              f"içinde {pay(lambda x: x[1] is not None):.3f}")
    print()


# ==============================================================================
def main() -> int:
    klasor = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else D
    kayit = oku(klasor)
    duman = not any(r["tohum"] in DOGRULAMA for rs in kayit.values() for r in rs)
    print(f"B3 teşhisi · karar hesabı · {klasor}"
          f"{' · DUMAN (hüküm yok)' if duman else ''}\n")
    if not kayit:
        print("kayıt yok")
        return 1
    gecerli = k0(kayit, duman)
    ornek = veri_ornekleri(kayit)
    s1(ornek)
    hukum, k_g, g = k1(ornek, kayit, duman)
    k2(ornek, hukum, k_g, g, duman)
    k3(ornek, hukum, k_g, g, duman)
    k4(ornek)
    k5(ornek)
    k6(ornek, kayit)
    return 0 if gecerli else 1


if __name__ == "__main__":
    sys.exit(main())
