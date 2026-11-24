"""
Faz 5-3 · B2 teşhisinin karar hesabı (`beklenti.md` "Karar kuralı", K0–K7).
Kayıtlardan okur; simülasyon yok.

    PYTHONIOENCODING=utf-8 py -3.11 <bu dosya> [<klasör>] > sonuc_hesap.txt

<klasör> verilmezse bu dosyanın dizini (`kayit_<hücre>.json`). Duman için
`duman/`: orada doğrulama yarısı yoktur, hüküm verilmez; yalnız geçerlilik
(K0) ve aletin çalıştığı denetlenir.
"""

from __future__ import annotations

import json
import math
import statistics as ist
import sys
from collections import Counter
from pathlib import Path

import numpy as np

D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))

import isaret as I  # noqa: E402

HUCRELER = ("ikiz", "birincil", "dayaniklilik", "cephe")
KARISTIRMA = ("birincil", "dayaniklilik")
SECIM = (1003, 1004, 1005, 1006)
DOGRULAMA = (1007, 1008, 1009, 1010)
DONGU = D.parent / "faz5_3_dongu_kurallari_2026-11-24"

# --- karar kuralının eşikleri (`beklenti.md`) -----------------------------------
ERKEN_S = 3.0                 # "erken yakalama": karıştırma başladıktan 3 s içinde
FA_ED, FA_ED_D = 0.0005, 0.001          # kanal kilidi: seçim · doğrulama
YAKALAMA_ED = 0.80
FA_G, FA_G_D = 0.001, 0.002             # girişim (kendi durumum): ikiz, önce
FA_UZAK, FA_UZAK_D = 0.01, 0.02         # ... açık dönemde uzak alandaki düğüm
YAKALAMA_G = 0.25
FA_BAG, FA_BAG_D = 1.0, 2.0             # bağ kuralları, 1000 birimde
YAKALAMA_BAG_E, YAKALAMA_BAG_G = 0.50, 0.30
ESIT = 0.005                  # amaç ölçüsünde eşitlik payı
YUK_KAT = 3.0                 # K5: en yüklü üçte birde yanlış alarm ≤ 3 × FA_G

SINIF = {"ikiz": 1, "once": 2, "sessiz": 3, "uzak": 4, "G": 5, "E": 6}
TEMIZ = ("ikiz", "once", "sessiz", "uzak")


# ==============================================================================
# Okuma
# ==============================================================================
def oku(klasor: Path) -> dict[str, list]:
    kayit: dict[str, list] = {}
    for h in HUCRELER:
        yol = klasor / f"kayit_{h}.json"
        if yol.exists():
            k = json.loads(yol.read_text(encoding="utf-8"))
            kayit[h] = [r for r in k["sonuc"] if "hata" not in r]
    return kayit


def yari(rs: list, tohumlar) -> list:
    return [r for r in rs if r["tohum"] in tohumlar]


# ==============================================================================
# K0 · geçerlilik
# ==============================================================================
ALANLAR = ("pdr", "pdr_pencere", "uretilen", "teslim", "sayaclar",
           "teshis_toplam")


def birebir(a: dict, b: dict) -> list[str]:
    return [x for x in ALANLAR if a.get(x) != b.get(x)]


def k0(kayit: dict, klasor: Path, duman: bool) -> bool:
    print("== K0 · geçerlilik ==")
    tamam = True
    for h, rs in kayit.items():
        gecersiz = [r["tohum"] for r in rs if not r["gecerli"]]
        denetim = [(r["tohum"], r["kaydedici_denetim"]) for r in rs
                   if r["kaydedici_denetim"]]
        print(f"  {h:<13} koşu {len(rs)} · geçersiz {gecersiz or 'yok'} · "
              f"iç denetim {denetim or 'tamam'}")
        tamam &= not gecersiz and not denetim
    # birebirlik: kaydedicisiz koşularla
    karsilar: list[tuple[str, Path, str | None]] = []
    if duman:
        for h in ("ikiz", "birincil"):
            karsilar.append((h, DONGU / "duman" / f"kayit_duman_{h}.json",
                             "geri_sinir"))
        for h in HUCRELER:
            karsilar.append((h, klasor / f"duz_{h}.json", None))
    else:
        for h in ("ikiz", "birincil"):
            karsilar.append((h, DONGU / f"kayit_geri_sinir_{h}.json",
                             "geri_sinir"))
    for h, yol, kol in karsilar:
        if h not in kayit or not yol.exists():
            continue
        k = json.loads(yol.read_text(encoding="utf-8"))
        ote = {r["tohum"]: r for r in k["sonuc"]
               if "hata" not in r and (kol is None or r.get("kol") == kol)}
        farkli, eslesen = [], 0
        for r in kayit[h]:
            o = ote.get(r["tohum"])
            if o is None:
                continue
            eslesen += 1
            f = birebir(r, o)
            if f:
                farkli.append((r["tohum"], f))
        print(f"  birebirlik {h:<13} ↔ {yol.relative_to(D.parent)}: "
              f"{eslesen} eşleşen · {'birebir' if not farkli else farkli}")
        tamam &= not farkli
    print(f"  hüküm: {'geçerli' if tamam else 'GEÇERSİZ — tablolar kullanılmaz'}\n")
    return tamam


# ==============================================================================
# Satırın hazırlanması
# ==============================================================================
def hazirla(r: dict) -> dict:
    k = r["kaydedici"]
    ilk, son = k["pencere"]
    S, N = k["S"], k["N"]
    ev = k["evre"]
    ds = k["ds"]
    z = ds["z"]
    kod = np.zeros((N, S), dtype=np.int8)
    harf = {"i": "ikiz", "o": "once", "s": "sessiz"}
    for n in range(N):
        for T in range(ilk, son):
            e = ev[T]
            if e == "g":
                continue
            ad = harf.get(e) or {"U": "uzak", "G": "G", "E": "E"}[z[n][T]]
            kod[n, T] = SINIF[ad]
    s = [[None if x < 0 else x / 1000.0 for x in sat] for sat in ds["s"]]
    donem = [tuple(x) for x in k["donemler"]]
    birim = []                    # (düğüm, dönem, alan, bas, bitis, sonraki)
    for q, (on, off) in enumerate(donem):
        orta = min(S - 1, int((on + off) / 2))
        sonraki = donem[q + 1][0] if q + 1 < len(donem) else None
        for n in range(N):
            if z[n][orta] in "GE":
                birim.append((n, q, z[n][orta], on, off, sonraki))
    return {"N": N, "S": S, "m": [[x / 1000.0 for x in sat] for sat in ds["m"]],
            "c": ds["c"], "s": s, "a": ds["a"], "f": ds["f"], "k": ds["k"],
            "kod": kod, "birim": birim,
            "payda": {ad: int((kod == SINIF[ad]).sum()) for ad in SINIF}}


class Birikim:
    """Bir kuralın bir hücrede bir tohum yarısındaki sayıları."""

    def __init__(self) -> None:
        self.ic = Counter()          # sınıf → durumdaki düğüm-saniye
        self.payda = Counter()
        self.birim = {"G": [], "E": []}     # (giriş, çıkış)

    def ekle(self, h: dict, dur: np.ndarray) -> None:
        for ad in SINIF:
            self.payda[ad] += h["payda"][ad]
            self.ic[ad] += int((dur & (h["kod"] == SINIF[ad])).sum())
        for n, _, alan, on, off, sonraki in h["birim"]:
            self.birim[alan].append(I.donem_olcusu(list(dur[n]), on, off,
                                                   sonraki))


def toplu(birikimler: list[Birikim]) -> Birikim:
    t = Birikim()
    for b in birikimler:
        t.ic.update(b.ic)
        t.payda.update(b.payda)
        for a in ("G", "E"):
            t.birim[a] += b.birim[a]
    return t


def olcu(b: Birikim, alan: str = "G") -> dict:
    def oran(ad):
        return b.ic[ad] / b.payda[ad] if b.payda[ad] else None
    u = b.birim[alan]
    gir = [g for g, _ in u if g is not None]
    cik = [c for g, c in u if g is not None and c is not None]
    return {"fa_ikiz": oran("ikiz"), "fa_once": oran("once"),
            "fa_sessiz": oran("sessiz"), "fa_uzak": oran("uzak"),
            "kapsama": oran(alan), "n": len(u),
            "erken": (sum(g <= ERKEN_S for g in gir) / len(u)) if u else None,
            "donemici": (len(gir) / len(u)) if u else None,
            "gecikme": ist.median(gir) if gir else None,
            "cikis": ist.median(cik) if cik else None,
            "cikis_yok": ((len(gir) - len(cik)) / len(gir)) if gir else None}


def kendi_degerlendir(hazir: dict[str, list], kurallar: list) -> dict:
    """kural → hücre → tohum → Birikim."""
    sonuc: dict = {kr: {h: {} for h in hazir} for kr in kurallar}
    gruplar: dict = {}
    for kr in kurallar:
        anahtar = ("ED",) if kr[0] == "ED" else (kr[0], kr[1], kr[2])
        gruplar.setdefault(anahtar, []).append(kr)
    for h, satirlar in hazir.items():
        for tohum, x in satirlar:
            N, S = x["N"], x["S"]
            for anahtar, krs in gruplar.items():
                if anahtar[0] == "ED":
                    m = np.array(x["m"])
                    for kr in krs:
                        b = Birikim()
                        b.ekle(x, m >= kr[1] - 1e-12)
                        sonuc[kr][h][tohum] = b
                    continue
                aile, al, be = anahtar
                isaret = [I.g_isareti(x["m"][n], x["c"][n], x["s"][n],
                                      x["a"][n], x["f"][n], x["k"][n],
                                      al, be, oy=(aile == "GM"))
                          for n in range(N)]
                for kr in krs:
                    dur = np.array([I.durum(isaret[n], kr[3], kr[4])
                                    for n in range(N)], dtype=bool)
                    b = Birikim()
                    b.ekle(x, dur)
                    sonuc[kr][h][tohum] = b
    return sonuc


def secim_olcusu(deg: dict, kr, hucreler, tohumlar, alan="G") -> dict:
    bs = [b for h in hucreler for t, b in deg[kr].get(h, {}).items()
          if t in tohumlar]
    return olcu(toplu(bs), alan)


def fmt(x, yuzde=False, ondalik=3) -> str:
    if x is None:
        return "—"
    return f"{100 * x:.{max(0, ondalik - 1)}f}%" if yuzde else f"{x:.{ondalik}f}"


def kural_adi(kr) -> str:
    if kr[0] == "ED":
        return f"ED(θ={kr[1]:.2f})"
    return f"{kr[0]}(α={kr[1]}, β={kr[2]}, giriş {kr[3]}, çıkış {kr[4]})"


def betimle(hazir: dict) -> None:
    """İşaretlerin sınıflara göre ortalaması (öngörü 3 için; karar dışı)."""
    print("== Betimleyici · işaretlerin ortalaması (bütün tohumlar) ==")
    print("  hücre · sınıf · düğüm-saniye · m · c (çerçeve/s) · s")
    for h, satirlar in hazir.items():
        for ad in SINIF:
            mm, cc, ss, n = [], [], [], 0
            for _, x in satirlar:
                maske = x["kod"] == SINIF[ad]
                if not maske.any():
                    continue
                n += int(maske.sum())
                mm.append(np.array(x["m"])[maske])
                cc.append(np.array(x["c"])[maske])
                s = np.array([[np.nan if v is None else v for v in sat]
                              for sat in x["s"]])[maske]
                ss.append(s[~np.isnan(s)])
            if n:
                m_, c_, s_ = (np.concatenate(v) for v in (mm, cc, ss))
                print(f"  {h:<13} {ad:<7} {n:>7} · {m_.mean():.3f} · "
                      f"{c_.mean():.1f} · "
                      f"{(f'{s_.mean():.3f}' if s_.size else '—')}")
    print()


# ==============================================================================
# K1 · K2 · kendi durumum
# ==============================================================================
def k1_k2(hazir: dict, kayit: dict, duman: bool) -> tuple:
    kurallar = I.izgara()
    hz = {h: v for h, v in hazir.items() if h in ("ikiz",) + KARISTIRMA}
    deg = kendi_degerlendir(hz, kurallar)
    sec = SECIM if not duman else tuple(sorted({t for h in hz
                                                for t, _ in hz[h]}))

    print("== K1 · kanal kilidi: kendi durumum (m ≥ θ) ==")
    print("  seçim yarısı: θ · ikizde yanlış alarm · önce · E alanında erken "
          "yakalama · dönem içinde · gecikme ortancası (s)")
    ed_ad = [kr for kr in kurallar if kr[0] == "ED"]
    secilen_ed = None
    for kr in ed_ad:
        fa = secim_olcusu(deg, kr, ("ikiz",), sec)["fa_ikiz"]
        o = secim_olcusu(deg, kr, KARISTIRMA, sec, "E")
        print(f"    {kr[1]:.2f} · {fmt(fa, True, 4)} · {fmt(o['fa_once'], True, 4)}"
              f" · {fmt(o['erken'])} (n {o['n']}) · {fmt(o['donemici'])} · "
              f"{fmt(o['gecikme'], ondalik=2)}")
        if secilen_ed is None and fa is not None and fa <= FA_ED:
            secilen_ed = kr
    print(f"  seçilen: {kural_adi(secilen_ed) if secilen_ed else 'yok'}")
    h1 = None
    if secilen_ed and not duman:
        fa = secim_olcusu(deg, secilen_ed, ("ikiz",), DOGRULAMA)["fa_ikiz"]
        o = secim_olcusu(deg, secilen_ed, KARISTIRMA, DOGRULAMA, "E")
        h1 = (fa is not None and fa <= FA_ED_D and o["erken"] is not None
              and o["erken"] >= YAKALAMA_ED)
        print(f"  doğrulama: ikizde yanlış alarm {fmt(fa, True, 4)} · erken "
              f"yakalama {fmt(o['erken'])} (n {o['n']}) · gecikme "
              f"{fmt(o['gecikme'], ondalik=2)} s")
        print(f"  hüküm K1: {'kanal kilidi kuralı tutar' if h1 else 'tutmaz'}")
    elif not duman:
        print("  hüküm K1: ikizde yanlış alarm sınırını geçen θ yok → tutmaz")
    print()

    print("== K2 · girişim: kendi durumum ==")
    gm = [kr for kr in kurallar if kr[0] in ("G", "GM")]
    tablo = []
    for kr in gm:
        fa = secim_olcusu(deg, kr, ("ikiz",), sec)["fa_ikiz"]
        o = secim_olcusu(deg, kr, KARISTIRMA, sec)
        tablo.append((kr, fa, o))
    uygun = [(kr, fa, o) for kr, fa, o in tablo
             if fa is not None and fa <= FA_G and o["fa_once"] is not None
             and o["fa_once"] <= FA_G and o["fa_uzak"] is not None
             and o["fa_uzak"] <= FA_UZAK and o["erken"] is not None]
    print(f"  ızgara {len(gm)} kural · seçim yarısında yanlış alarm sınırını "
          f"(ikiz ve önce ≤ {FA_G:.1%}, açık dönemde uzak ≤ {FA_UZAK:.0%}) "
          f"geçen {len(uygun)}")
    secilen = None
    if uygun:
        en = max(o["erken"] for _, _, o in uygun)
        aday = [x for x in uygun if x[2]["erken"] >= en - ESIT]
        aday.sort(key=lambda x: (-(x[2]["donemici"] or 0), x[1],
                                 0 if x[0][0] == "G" else 1, -x[0][3],
                                 x[0][4], x[0][1], x[0][2]))
        secilen = aday[0][0]
        print("  seçim yarısında en iyi 10 (erken yakalamaya göre):")
        for kr, fa, o in sorted(uygun, key=lambda x: -x[2]["erken"])[:10]:
            print(f"    {kural_adi(kr):<40} ikiz {fmt(fa, True, 4)} · önce "
                  f"{fmt(o['fa_once'], True, 4)} · erken {fmt(o['erken'])} · "
                  f"dönem içinde {fmt(o['donemici'])} · gecikme "
                  f"{fmt(o['gecikme'], ondalik=2)} s · kapsama "
                  f"{fmt(o['kapsama'])}")
    print(f"  seçilen: {kural_adi(secilen) if secilen else 'yok'}")
    eski = I.ESKI_KURAL
    for ad, kr in (("seçilen", secilen), ("önceki KK-03 kuralı", eski)):
        if kr is None:
            continue
        for yarisi, toh in (("seçim", sec), ("doğrulama", DOGRULAMA)):
            if yarisi == "doğrulama" and duman:
                continue
            fa = secim_olcusu(deg, kr, ("ikiz",), toh)["fa_ikiz"]
            for h in KARISTIRMA:
                o = secim_olcusu(deg, kr, (h,), toh)
                print(f"  {ad} · {yarisi} · {h:<12} ikiz {fmt(fa, True, 4)} · "
                      f"önce {fmt(o['fa_once'], True, 4)} · sessiz "
                      f"{fmt(o['fa_sessiz'], True, 4)} · uzak "
                      f"{fmt(o['fa_uzak'], True, 4)} · erken {fmt(o['erken'])}"
                      f" (n {o['n']}) · dönem içinde {fmt(o['donemici'])} · "
                      f"gecikme {fmt(o['gecikme'], ondalik=2)} s · kapsama "
                      f"{fmt(o['kapsama'])} · çıkış {fmt(o['cikis'], ondalik=2)}"
                      f" s (çıkılmayan {fmt(o['cikis_yok'])})")
    h2 = None
    if not duman:
        if secilen is None:
            h2 = False
        else:
            fa = secim_olcusu(deg, secilen, ("ikiz",), DOGRULAMA)["fa_ikiz"]
            uz = secim_olcusu(deg, secilen, KARISTIRMA, DOGRULAMA)["fa_uzak"]
            ok = (fa is not None and fa <= FA_G_D and uz is not None
                  and uz <= FA_UZAK_D)
            for h in KARISTIRMA:
                e = secim_olcusu(deg, secilen, (h,), DOGRULAMA)["erken"]
                ok &= e is not None and e >= YAKALAMA_G
            h2 = ok
        print(f"  hüküm K2: {'girişim kuralı var' if h2 else 'girişim kuralı yok'}")
    print()
    return deg, secilen_ed, secilen, h1, h2


# ==============================================================================
# K3 · K4 · göndericinin bağ kanıtı
# ==============================================================================
def bag_olcu(rs: list, ad: str, alan: str) -> dict:
    k0 = rs[0]["kaydedici"] if rs else None
    if k0 is None:
        return {"fa_ikiz": None, "fa_once": None, "erken": None, "n": 0,
                "donemici": None, "gecikme": None}
    adlar = k0["kural_veri"] + k0["kural_ses"]
    i = adlar.index(ad)
    ses = ad in k0["kural_ses"]
    ates, payda = Counter(), Counter()
    gec: list = []
    for r in rs:
        k = r["kaydedici"]
        for s in TEMIZ:
            ates[s] += k["fa"][ad][s]
            payda[s] += k["ses_payda"][s] if ses else k["veri_payda"][s][0]
        for u in k["veri_birim"]:
            if u[0] == alan:
                gec.append(u[3 + i])
    var = [g for g in gec if g is not None]

    def binde(s):
        return 1000.0 * ates[s] / payda[s] if payda[s] else None
    return {"fa_ikiz": binde("ikiz"), "fa_once": binde("once"),
            "fa_sessiz": binde("sessiz"), "fa_uzak": binde("uzak"),
            "n": len(gec),
            "erken": (sum(g <= ERKEN_S for g in var) / len(gec)) if gec else None,
            "donemici": (len(var) / len(gec)) if gec else None,
            "gecikme": ist.median(var) if var else None}


def k3_k4(kayit: dict, duman: bool) -> dict:
    secilenler = {}
    if not kayit.get("ikiz") or not any(kayit.get(h) for h in KARISTIRMA):
        return secilenler
    k0_ = kayit["ikiz"][0]["kaydedici"]
    adlar = k0_["kural_veri"] + k0_["kural_ses"]
    sec = SECIM if not duman else tuple(sorted({r["tohum"] for h in kayit
                                                for r in kayit[h]}))
    for etiket, alan, esik in (("K3 · kanal kilidindeki alıcı", "E",
                                YAKALAMA_BAG_E),
                               ("K4 · girişimdeki alıcı", "G", YAKALAMA_BAG_G)):
        print(f"== {etiket}: göndericinin bağ kanıtı (veri taşıyan bağlar) ==")
        print("  seçim yarısı: kural · ikizde ‰ · önce ‰ · erken · dönem içinde "
              "· gecikme ortancası (s) · birim")
        tablo = []
        for ad in adlar:
            fi = bag_olcu(yari(kayit["ikiz"], sec), ad, alan)["fa_ikiz"]
            o = bag_olcu([r for h in KARISTIRMA for r in
                          yari(kayit.get(h, []), sec)], ad, alan)
            tablo.append((ad, fi, o))
            print(f"    {ad:<10} {fmt(fi, ondalik=2):>7} · "
                  f"{fmt(o['fa_once'], ondalik=2):>7} · {fmt(o['erken'])} · "
                  f"{fmt(o['donemici'])} · {fmt(o['gecikme'], ondalik=2)} · "
                  f"{o['n']}")
        uygun = [x for x in tablo if x[1] is not None and x[1] <= FA_BAG
                 and x[2]["fa_once"] is not None and x[2]["fa_once"] <= FA_BAG
                 and x[2]["erken"] is not None]
        secilen = None
        if uygun:
            en = max(o["erken"] for _, _, o in uygun)
            aday = [x for x in uygun if x[2]["erken"] >= en - ESIT]
            aday.sort(key=lambda x: (-(x[2]["donemici"] or 0), x[1],
                                     adlar.index(x[0])))
            secilen = aday[0][0]
        print(f"  yanlış alarm sınırını (≤ {FA_BAG:.0f}‰) geçen {len(uygun)} · "
              f"seçilen: {secilen or 'yok'}")
        secilenler[alan] = secilen
        if not duman:
            hk = False
            if secilen:
                fi = bag_olcu(yari(kayit["ikiz"], DOGRULAMA), secilen,
                              alan)["fa_ikiz"]
                for h in KARISTIRMA:
                    o = bag_olcu(yari(kayit.get(h, []), DOGRULAMA), secilen,
                                 alan)
                    print(f"  doğrulama · {h:<12} ikiz {fmt(fi, ondalik=2)}‰ · "
                          f"önce {fmt(o['fa_once'], ondalik=2)}‰ · erken "
                          f"{fmt(o['erken'])} (n {o['n']}) · dönem içinde "
                          f"{fmt(o['donemici'])} · gecikme "
                          f"{fmt(o['gecikme'], ondalik=2)} s")
                o = bag_olcu([r for h in KARISTIRMA for r in
                              yari(kayit.get(h, []), DOGRULAMA)], secilen, alan)
                hk = (fi is not None and fi <= FA_BAG_D and o["erken"]
                      is not None and o["erken"] >= esik)
                # hız sınıfına göre (yaprak · röle)
                k0r = kayit["ikiz"][0]["kaydedici"]
                i = (k0r["kural_veri"] + k0r["kural_ses"]).index(secilen)
                for hiz, ad_ in (("y", "yaprak benzeri"), ("r", "röle")):
                    gec = [u[3 + i] for h in KARISTIRMA
                           for r in yari(kayit.get(h, []), DOGRULAMA)
                           for u in r["kaydedici"]["veri_birim"]
                           if u[0] == alan and u[1] == hiz]
                    var = [g for g in gec if g is not None]
                    print(f"    {ad_:<15} erken "
                          f"{fmt(sum(g <= ERKEN_S for g in var) / len(gec)) if gec else '—'}"
                          f" (n {len(gec)})")
            print(f"  hüküm {etiket.split(' ·')[0]}: "
                  f"{'göndericide tanınır' if hk else 'göndericide tanınmaz'}")
        print()
    return secilenler


# ==============================================================================
# K5 · K6 · K7
# ==============================================================================
def k5(hazir: dict, secilen) -> None:
    kr = secilen or I.ESKI_KURAL
    print(f"== K5 · kalabalık: {kural_adi(kr)} ikizde yükün üçte birlerine "
          f"göre yanlış alarm ==")
    if "ikiz" not in hazir:
        print("  ikiz yok\n")
        return
    mler, durlar = [], []
    for _, x in hazir["ikiz"]:
        isaret = [I.g_isareti(x["m"][n], x["c"][n], x["s"][n], x["a"][n],
                              x["f"][n], x["k"][n], kr[1], kr[2],
                              oy=(kr[0] == "GM")) for n in range(x["N"])]
        dur = np.array([I.durum(isaret[n], kr[3], kr[4])
                        for n in range(x["N"])], dtype=bool)
        maske = x["kod"] == SINIF["ikiz"]
        mler.append(np.array(x["m"])[maske])
        durlar.append(dur[maske])
    m = np.concatenate(mler)
    d = np.concatenate(durlar)
    s1, s2 = np.quantile(m, [1 / 3, 2 / 3])
    for ad, mk in (("düşük", m < s1), ("orta", (m >= s1) & (m < s2)),
                   ("yüksek", m >= s2)):
        print(f"  {ad:<7} meşgul payı {fmt(float(m[mk].min()), ondalik=2)}–"
              f"{fmt(float(m[mk].max()), ondalik=2)} · yanlış alarm "
              f"{fmt(float(d[mk].mean()), True, 4)} ({int(d[mk].sum())} / "
              f"{int(mk.sum())})")
    ust = float(d[m >= s2].mean())
    print(f"  hüküm K5: {'yük koruması gerekir' if ust > YUK_KAT * FA_G else 'yük koruması gerekmez'}"
          f" (en yüklü üçte birde {fmt(ust, True, 4)}, sınır "
          f"{fmt(YUK_KAT * FA_G, True, 4)})\n")


def k6(kayit: dict) -> None:
    print("== K6 · bitin ulaşması: G alanındaki düğümün açık dönemdeki "
          "selamlarından tanıdık komşulara ulaşan pay ==")
    for h in KARISTIRMA + ("cephe",):
        if h not in kayit:
            continue
        top = {a: [0, 0] for a in "EGU"}
        for r in kayit[h]:
            for a in "EGU":
                b = r["kaydedici"]["bit"][a]
                top[a][0] += b[0]
                top[a][1] += b[1]
        print(f"  {h:<13} " + " · ".join(
            f"alıcı {a}: {fmt(top[a][1] / top[a][0]) if top[a][0] else '—'}"
            f" ({top[a][0]})" for a in "UGE"))
    print()


def k7(kayit: dict, hazir: dict, deg_ed, secilen_g, secilen_bag) -> None:
    print("== K7 · genelleme: seçilen kurallar cephe hattında (bütün "
          "tohumlar) ve birincilde ==")
    if "cephe" not in hazir:
        print("  cephe yok\n")
        return
    for ad, kr, alan in (("kanal kilidi", deg_ed, "E"),
                         ("girişim", secilen_g, "G")):
        if kr is None:
            continue
        sonuc = {}
        for h in ("birincil", "cephe"):
            if h not in hazir:
                continue
            d = kendi_degerlendir({h: hazir[h]}, [kr])
            sonuc[h] = secim_olcusu(d, kr, (h,),
                                    tuple(t for t, _ in hazir[h]), alan)
        if len(sonuc) < 2:
            continue
        b, c = sonuc["birincil"], sonuc["cephe"]
        bayrak = (c["erken"] is not None and b["erken"] is not None
                  and c["erken"] < 0.5 * b["erken"])
        print(f"  {ad}: {kural_adi(kr)} · cephe önce yanlış alarm "
              f"{fmt(c['fa_once'], True, 4)} · erken {fmt(c['erken'])} (n "
              f"{c['n']}) · kapsama {fmt(c['kapsama'])} · çıkılmayan "
              f"{fmt(c['cikis_yok'])} ↔ birincil {fmt(b['erken'])} (n "
              f"{b['n']}){' · GENELLEMEDE DÜŞÜYOR' if bayrak else ''}")
    for alan, ad in secilen_bag.items():
        if ad is None:
            continue
        b = bag_olcu(kayit.get("birincil", []), ad, alan)
        c = bag_olcu(kayit["cephe"], ad, alan)
        bayrak = (c["erken"] is not None and b["erken"] is not None
                  and c["erken"] < 0.5 * b["erken"])
        print(f"  bağ ({alan}): {ad} · cephe önce {fmt(c['fa_once'], ondalik=2)}‰"
              f" · erken {fmt(c['erken'])} (n {c['n']}) ↔ birincil "
              f"{fmt(b['erken'])} (n {b['n']})"
              f"{' · GENELLEMEDE DÜŞÜYOR' if bayrak else ''}")
    print()


def main() -> int:
    klasor = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else D
    kayit = oku(klasor)
    duman = not any(r["tohum"] in DOGRULAMA for rs in kayit.values() for r in rs)
    print(f"B2 teşhisi · karar hesabı · {klasor} · hücreler "
          f"{ {h: len(v) for h, v in kayit.items()} }"
          f"{' · DUMAN: hüküm verilmez' if duman else ''}\n")
    gecerli = k0(kayit, klasor, duman)
    if not gecerli and not duman:
        return 1
    hazir = {h: [(r["tohum"], hazirla(r)) for r in rs]
             for h, rs in kayit.items()}
    betimle(hazir)
    _, secilen_ed, secilen_g, _, _ = k1_k2(hazir, kayit, duman)
    secilen_bag = k3_k4(kayit, duman)
    k5(hazir, secilen_g)
    k6(kayit)
    k7(kayit, hazir, secilen_ed, secilen_g, secilen_bag)
    return 0


if __name__ == "__main__":
    sys.exit(main())
