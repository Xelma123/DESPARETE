"""Faz 5-2 (c) · beklentinin karar kuralını kayıtlara uygular (simülasyon yok).

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz5_2_rakip_cizgisi_2026-11-15/sonuc_hesap.py [kayıt dizini]

Argümansız: bu dizinin `kayit_*.json` dosyaları. Bir dizin verilirse (duman
koşusunun denemesi) kayıtlar oradan okunur; kısa pencerede önceki kayıtlarla
birebirlik denetimi yapılmaz.
"""
import json
import math
import statistics as ist
import sys
from collections import Counter
from pathlib import Path

D = Path(__file__).resolve().parent
TESHIS = D.parent
ONCEKI_IKIZ = TESHIS / "faz5_2_secenek_iletim_2026-11-15" / "kayit_taban.json"
ONCEKI_BIRINCIL = TESHIS / "faz5_2_anatomi_2026-11-14" / "kayit_birincil.json"
K244 = TESHIS / "rakipler_k244_2026-10-14"
DOSYALAR = ("kayit_ikiz.json", "kayit_birincil.json",
            "kayit_dayaniklilik.json", "kayit_v041_ikiz.json",
            "kayit_v041_karistirma.json")
EK = "@tehdit_acik_s=10+tehdit_sessiz_s=20"
KAHIN, V041 = "en_guvenilir_kahin", "desparete"
RAKIP = ("babel", "olsrv2", "aodv")
KOLLAR = (KAHIN, *RAKIP, V041)
AD = {KAHIN: "kâhin", "babel": "Babel", "olsrv2": "OLSRv2", "aodv": "AODV-k",
      V041: "v0.4.1"}
HUCRE = ("ikiz", "birincil", "dayaniklilik")
HAD = {"ikiz": "İ · karıştırıcısız ikiz (pencere PDR)",
       "birincil": "B · birincil, 15/15 (PDR_açık)",
       "dayaniklilik": "D · dayanıklılık, 10/20 (PDR_açık)"}
CIZELGE = {"birincil": "15/15", "dayaniklilik": "10/20"}
TOHUMLAR = tuple(range(1003, 1011))
GRUP = {"rota_gecersiz": "R", "hedef_yok": "R", "tampon_asimi": "R",
        "iletim_basarisiz": "I", "kuyruk_tasmasi": "K", "ttl": "T"}
COZUNURLUK = 0.0126                 # eşleştirilmiş R (K-224)
TAVAN = "5"                         # ana gecikme tavanı, saniye (K-246)


# ------------------------------------------------------------------ okuma
def oku(dizin: Path):
    kayit = {h: {k: {} for k in KOLLAR} for h in HUCRE}
    kisa = False
    for ad in DOSYALAR:
        yol = dizin / ad
        if not yol.exists():
            continue
        k = json.loads(yol.read_text(encoding="utf-8"))
        kisa = kisa or bool(k.get("kisa"))
        for r in k["sonuc"]:
            etiket = r["protokol"]
            if k["sinif"] == "yok":
                h, kol = "ikiz", etiket
            elif etiket.endswith(EK):
                h, kol = "dayaniklilik", etiket[:-len(EK)]
            else:
                h, kol = "birincil", etiket
            assert kol in KOLLAR, etiket
            assert r["tohum"] not in kayit[h][kol], (h, kol, r["tohum"])
            kayit[h][kol][r["tohum"]] = r
    return kayit, kisa


# ----------------------------------------------------------------- ölçüler
def oran(o: dict, tavan: str | None = None):
    t = o["teslim"] if tavan is None else o["teslim_tavan"][tavan]
    return t / o["dogan"] if o["dogan"] else None


def donem(h: str, r: dict, evre: str = "acik") -> dict:
    return r["ikincil"]["cizelge"][CIZELGE[h]][evre]


def olcu(h: str, r: dict, tavan: str | None = None):
    """Hücrenin birincil ölçüsü: İ'de pencere PDR'si, B ve D'de PDR_açık."""
    if h == "ikiz":
        return oran(r["ikincil"]["pencere"], tavan)
    return oran(donem(h, r), tavan)


def dizi(kayit, h: str, kol: str, f) -> dict:
    """tohum → değer (tanımsızlar atılır)."""
    d = {t: f(r) for t, r in sorted(kayit[h][kol].items())}
    return {t: v for t, v in d.items() if v is not None}


def ort(d: dict):
    return ist.mean(d.values()) if d else None


def ss(d: dict):
    return ist.stdev(d.values()) if len(d) > 1 else None


def f3(x, isaret: bool = False) -> str:
    if x is None:
        return "  —  "
    return f"{x:+.3f}" if isaret else f"{x:.3f}"


def esli(a: dict, b: dict):
    """a − b, ortak tohumlarda: (ortalama, artı, eksi, n, farklar)."""
    ortak = sorted(set(a) & set(b))
    f = {t: a[t] - b[t] for t in ortak}
    if not f:
        return None, 0, 0, 0, f
    return (ist.mean(f.values()), sum(v > 0 for v in f.values()),
            sum(v < 0 for v in f.values()), len(f), f)


def ayris(e, esik: float) -> str:
    """Ayrışma kuralı: |ortalama| ≥ eşik ve tohumların ≥ 3/4'ünde aynı yön."""
    o, arti, eksi, n, _ = e
    if o is None:
        return "veri yok"
    gerek = math.ceil(0.75 * n)
    if o >= esik and arti >= gerek:
        return "AYRIŞIYOR (+)"
    if o <= -esik and eksi >= gerek:
        return "AYRIŞIYOR (−)"
    return f"{n} tohumda ayırt edilemedi"


def esli_metni(e) -> str:
    o, arti, eksi, n, f = e
    if o is None:
        return "veri yok"
    return (f"{o:+.3f} (artı {arti}/{n} · eksi {eksi}/{n}; "
            + " · ".join(f"{t} {v:+.3f}" for t, v in f.items()) + ")")


def gruplar(h: str, rs) -> dict:
    """Kayıp grupları, hücrenin birincil ölçüsünün paydasına oranla."""
    g, dogan = Counter(), 0
    for r in rs:
        dogan += (r["ikincil"]["pencere"] if h == "ikiz"
                  else donem(h, r))["dogan"]
        for k, v in r["dogum_evre_dusen"].items():
            sebep, evre, _ = k.split("|")
            if h == "ikiz" or evre == "acik":
                g[GRUP.get(sebep, "?")] += v
    return {k: (g[k] / dogan if dogan else None) for k in "RIKT?"}


# -------------------------------------------------------------- geçerlilik
def _k244(dosya: str) -> list[dict]:
    for satir in (K244 / dosya).read_text(encoding="utf-8").splitlines():
        if satir.strip().startswith("KAYIT "):
            return json.loads(satir.strip()[len("KAYIT "):])
    return []


def _birebir(baslik: str, ciftler: list[tuple[str, float | None, float | None]]):
    tutan = [c for c in ciftler if c[1] is not None and c[2] is not None
             and abs(c[1] - c[2]) < 5e-7]
    print(f"  {baslik}: {len(tutan)}/{len(ciftler)} birebir")
    for ad, a, b in ciftler:
        if (ad, a, b) not in tutan:
            print(f"      FARKLI {ad}: {a} ↔ {b}")


def gecerlilik(kayit, kisa: bool, tohumlar) -> None:
    print("== 0 · GEÇERLİLİK ==")
    eksik, kusurlu, tutarsiz, n = [], [], [], 0
    for h in HUCRE:
        for kol in KOLLAR:
            for t in tohumlar:
                r = kayit[h][kol].get(t)
                if r is None:
                    eksik.append(f"{h}/{AD[kol]}/{t}")
                    continue
                n += 1
                if (not r["gecerli"] or r["dogum_celiski"]
                        or r["dogum_atfsiz"]):
                    kusurlu.append(f"{h}/{AD[kol]}/{t}")
                p = oran(r["ikincil"]["pencere"])
                if p is None or abs(p - r["pdr_pencere"]) > 1e-12:
                    tutarsiz.append(f"{h}/{AD[kol]}/{t}")
    beklenen = len(HUCRE) * len(KOLLAR) * len(tohumlar)
    print(f"  koşu {n}/{beklenen} · eksik {len(eksik)} · korunum, çelişki ya "
          f"da atfsız düşüş kusuru {len(kusurlu)} · ikincil sayımın pencere "
          f"PDR'siyle tutarsızlığı {len(tutarsiz)}")
    for ad, liste in (("eksik", eksik), ("kusurlu", kusurlu),
                      ("tutarsız", tutarsiz)):
        if liste:
            print(f"      {ad}: " + " · ".join(liste))
    if kisa:
        print("  (kısa pencere: önceki kayıtlarla karşılaştırma yapılmaz)")
        return
    ilk4 = (1003, 1004, 1005, 1006)
    uc = ("babel", KAHIN, V041)
    onceki = {(r["protokol"], r["tohum"]): r for r in json.loads(
        ONCEKI_IKIZ.read_text(encoding="utf-8"))["sonuc"]}
    _birebir("İ pencere PDR'si ↔ ikinci teşhis", [
        (f"{AD[k]} {t}", (kayit["ikiz"][k].get(t) or {}).get("pdr_pencere"),
         (onceki.get((k, t)) or {}).get("pdr_pencere"))
        for k in uc for t in ilk4])
    onceki = {(r["protokol"], r["tohum"]): r for r in json.loads(
        ONCEKI_BIRINCIL.read_text(encoding="utf-8"))["sonuc"]}
    ciftler = []
    for k in uc:
        for t in ilk4:
            r, o = kayit["birincil"][k].get(t), onceki.get((k, t))
            ciftler.append((f"{AD[k]} {t} pencere",
                            r and r["pdr_pencere"], o and o["pdr_pencere"]))
            ciftler.append((f"{AD[k]} {t} açık",
                            r and olcu("birincil", r),
                            o and o["karistirici_evresi"]["acik"]["pdr"]))
    _birebir("B pencere PDR'si ve PDR_açık ↔ ilk teşhis (12 koşu, 24 değer)",
             ciftler)
    g2c = _k244("G2c.txt")
    _birebir("B PDR_açık ↔ K-244 G2ç (1003 · 1004)", [
        (f"{AD[k]} {t}",
         (lambda r: r and olcu("birincil", r))(kayit["birincil"][k].get(t)),
         next((x["pdr_acik"] for x in g2c
               if x["senaryo"] == "formasyon-surekli" and not x["hayalet"]
               and x["protokol"] == k and x["tohum"] == t), None))
        for k in KOLLAR for t in (1003, 1004)])
    bos = _k244("G1c.txt") + [x for x in g2c if x["hayalet"]]
    _birebir("İ hayalet PDR_açık (15/15) ↔ K-244 G1ç ve G2ç boş kol "
             "(1003 · 1004)", [
        (f"{AD[k]} {t}",
         (lambda r: r and oran(
             r["ikincil"]["cizelge"]["15/15"]["acik"]))(
                 kayit["ikiz"][k].get(t)),
         next((x["pdr_acik"] for x in bos
               if x["senaryo"] == "formasyon-yok" and x["hayalet"]
               and x["protokol"] == k and x["tohum"] == t), None))
        for k in KOLLAR for t in (1003, 1004)])


# ------------------------------------------------------------------ tablolar
def hucre_tablolari(kayit, tohumlar) -> None:
    print("\n== 1 · HÜCRE TABLOLARI (8 tohum ortalaması ± ölçüt sapması) ==")
    for h in HUCRE:
        print(f"  {HAD[h]}")
        kahin = ort(dizi(kayit, h, KAHIN, lambda r: olcu(h, r)))
        for kol in KOLLAR:
            d = dizi(kayit, h, kol, lambda r: olcu(h, r))
            if not d:
                continue
            tv = ort(dizi(kayit, h, kol, lambda r: olcu(h, r, TAVAN)))
            p99 = ort(dizi(kayit, h, kol, lambda r: r["gecikme_s"]["p99"]))
            ek = ""
            if h != "ikiz":
                ek = (" · sessiz "
                      + f3(ort(dizi(kayit, h, kol, lambda r: oran(
                          donem(h, r, "sessiz")))))
                      + " · önce "
                      + f3(ort(dizi(kayit, h, kol, lambda r: oran(
                          r["ikincil"]["once"])))))
            print(f"    {AD[kol]:<7} {f3(ort(d))} ± {f3(ss(d))} "
                  f"[{min(d.values()):.3f} … {max(d.values()):.3f}] · "
                  f"5 s tavanlı {f3(tv)}{ek} · p99 {f3(p99)} s · kâhine oran "
                  f"{f3(ort(d) / kahin if kahin else None)}")
            print("            " + " · ".join(
                f"{t} {f3(d.get(t))}" for t in tohumlar))


def s1(kayit) -> dict:
    print("\n== 2 · S1 — her hücrede en güçlü rakip (ayrışma eşiği 0,02) ==")
    guclu = {}
    for h in HUCRE:
        d = {k: dizi(kayit, h, k, lambda r: olcu(h, r)) for k in RAKIP}
        d = {k: v for k, v in d.items() if v}
        if not d:
            continue
        sira = sorted(d, key=lambda k: -ort(d[k]))
        guclu[h] = sira[0]
        print(f"  {HAD[h]}: sıra " + " > ".join(
            f"{AD[k]} {ort(d[k]):.3f}" for k in sira))
        for a, b in zip(sira, sira[1:]):
            e = esli(d[a], d[b])
            print(f"      {AD[a]} − {AD[b]}: {esli_metni(e)} → "
                  f"{ayris(e, 0.02)}")
    if guclu:
        print("  en güçlü rakip: " + " · ".join(
            f"{h} {AD[k]}" for h, k in guclu.items())
            + (" → üç hücrede de Babel" if set(guclu.values()) == {"babel"}
               else " → BABEL DIŞINDA RAKİP VAR (kural 1)"))
    return guclu


def s2(kayit, guclu: dict) -> None:
    print("\n== 3 · S2 — v0.4.1'in açığı (eşik 0,02; G = rakip − v0.4.1) ==")
    for h in HUCRE:
        v = dizi(kayit, h, V041, lambda r: olcu(h, r))
        if not v or h not in guclu:
            continue
        gv = gruplar(h, kayit[h][V041].values())
        for kol in dict.fromkeys((guclu[h], *RAKIP)):
            a = dizi(kayit, h, kol, lambda r: olcu(h, r))
            if not a:
                continue
            e = esli(a, v)
            ortak = [kayit[h][kol][t] for t in e[4]]
            ga = gruplar(h, ortak)
            gv_ = gruplar(h, [kayit[h][V041][t] for t in e[4]])
            hukum = ayris(e, 0.02).replace("(+)", "(v0.4.1 GERİDE)").replace(
                "(−)", "(v0.4.1 İLERİDE)")
            print(f"  {HAD[h]} · {AD[kol]}{' [en güçlü]' if kol == guclu[h] else ''}"
                  f": G {esli_metni(e)} → {hukum}")
            print("      açığın ayrımı (v0.4.1 − rakip): " + " · ".join(
                f"{k} {f3(None if gv_[k] is None or ga[k] is None else gv_[k] - ga[k], True)}"
                for k in "RIKT"))
        print(f"      v0.4.1'in kayıp grupları: " + " · ".join(
            f"{k} {f3(gv[k])}" for k in "RIKT"))


def s3(kayit) -> None:
    print("\n== 4 · S3 — karıştırmaya özgü kayıp, Δ_k = PDR_açık(hücre) − "
          "hayalet PDR_açık(ikiz) ==")
    for h in ("birincil", "dayaniklilik"):
        print(f"  {HAD[h]}")
        dk = {}
        for kol in KOLLAR:
            a = dizi(kayit, h, kol, lambda r: olcu(h, r))
            b = dizi(kayit, "ikiz", kol, lambda r: oran(
                r["ikincil"]["cizelge"][CIZELGE[h]]["acik"]))
            e = esli(a, b)
            if e[0] is None:
                continue
            dk[kol] = e[4]
            print(f"    {AD[kol]:<7} Δ_k {e[0]:+.3f} ± {f3(ss(e[4]))} "
                  f"(hayalet {f3(ort({t: b[t] for t in e[4]}))} → hücre "
                  f"{f3(ort({t: a[t] for t in e[4]}))}) · "
                  + " · ".join(f"{t} {v:+.3f}" for t, v in e[4].items()))
        if V041 in dk and "babel" in dk:
            e = esli(dk[V041], dk["babel"])
            print(f"    Δ_k(v0.4.1) − Δ_k(Babel): {esli_metni(e)} → "
                  f"{ayris(e, 0.03)}")
        if dk:
            enb = min(dk, key=lambda k: ort(dk[k]))
            print(f"    karıştırmaya özgü kaybı en büyük kol: {AD[enb]}")


def s4(kayit) -> None:
    print("\n== 5 · S4 — çizelgeye duyarlılık, PDR_açık(D) − PDR_açık(B) "
          "(eşik 0,03) ==")
    for kol in KOLLAR:
        e = esli(dizi(kayit, "dayaniklilik", kol,
                      lambda r: olcu("dayaniklilik", r)),
                 dizi(kayit, "birincil", kol, lambda r: olcu("birincil", r)))
        if e[0] is None:
            continue
        hukum = ayris(e, 0.03).replace("AYRIŞIYOR", "ÇİZELGEYE DUYARLI")
        s = esli(dizi(kayit, "dayaniklilik", kol, lambda r: oran(
                     donem("dayaniklilik", r, "sessiz"))),
                 dizi(kayit, "birincil", kol, lambda r: oran(
                     donem("birincil", r, "sessiz"))))
        print(f"  {AD[kol]:<7} {esli_metni(e)} → {hukum} | sessiz dönem "
              f"farkı {f3(s[0], True)}")


def tavan(kayit) -> None:
    print("\n== 6 · GECİKME TAVANI — bedel = ölçü − ölçü(tavan), 8 tohum "
          "ortalaması; 5 s'de ≥ 0,02 bağlayıcı ==")
    for h in HUCRE:
        print(f"  {HAD[h]}")
        for kol in KOLLAR:
            if not kayit[h][kol]:
                continue
            b = {s: ort(dizi(kayit, h, kol, lambda r: (
                None if olcu(h, r) is None else olcu(h, r) - olcu(h, r, s))))
                for s in ("3.5", "5", "10")}
            print(f"    {AD[kol]:<7} 3,5 s {f3(b['3.5'])} · 5 s {f3(b['5'])}"
                  f" · 10 s {f3(b['10'])}"
                  + ("  → TAVAN BAĞLAYICI" if (b["5"] or 0) >= 0.02 else ""))


def kahin(kayit) -> None:
    print(f"\n== 7 · KÂHİN — tohum başına aşım (kol − kâhin > R = "
          f"{COZUNURLUK}) ==")
    for h in HUCRE:
        k = dizi(kayit, h, KAHIN, lambda r: olcu(h, r))
        for kol in (*RAKIP, V041):
            e = esli(dizi(kayit, h, kol, lambda r: olcu(h, r)), k)
            if e[0] is None:
                continue
            asan = {t: v for t, v in e[4].items() if v > COZUNURLUK}
            print(f"  {h:<12} {AD[kol]:<7} ortalama fark {e[0]:+.3f} · aşan "
                  f"tohum {len(asan)}/{e[3]}"
                  + (": " + " · ".join(f"{t} {v:+.3f}"
                                       for t, v in asan.items())
                     if asan else ""))


def betimleyici(kayit) -> None:
    print("\n== 8 · BETİMLEYİCİLER (tohum ortalaması; kanal yükü bütün koşu, "
          "ağ toplamı) ==")
    for h in HUCRE:
        print(f"  {HAD[h]}")
        for kol in KOLLAR:
            rs = list(kayit[h][kol].values())
            if not rs:
                continue
            g = gruplar(h, rs)
            n = len(rs)
            d = sum(r["veri_deneme"] for r in rs)
            basari = sum(r["sayaclar"]["mac_gonderim_basarili"] for r in rs)
            g0 = 1.0 - sum(r["veri_deneme_beklenen_basarisiz"] for r in rs) / d
            karar = sum(r["karar_sayisi"] for r in rs)
            dusus = sum(sum(r["basarisiz_bant"].values()) for r in rs)
            gec = {p: ort(dizi(kayit, h, kol, lambda r: r["gecikme_s"][p]))
                   for p in ("p50", "p95", "p99")}
            print(f"    {AD[kol]:<7} kayıp R {f3(g['R'])} · İ {f3(g['I'])} · K "
                  f"{f3(g['K'])} · T {f3(g['T'])}"
                  + (f" · ? {f3(g['?'])}" if g["?"] else "")
                  + f" | karar/paket "
                  f"{karar / sum(r['uretilen'] for r in rs):.2f} · atlama "
                  f"başarısızlığı {dusus / karar:.2%} · deneme başarısı g "
                  f"{basari / d:.3f} = g0 {g0:.3f} × k {basari / d / g0:.3f}"
                  f" | kontrol kanal süresi "
                  f"{sum(r['sayaclar']['kontrol_airtime_s'] for r in rs) / n:.0f}"
                  f" s · toplam gönderim "
                  f"{sum(r['enerji_s']['enerji_gonderim_s'] for r in rs) / n:.0f}"
                  f" s | gecikme p50 {f3(gec['p50'])} · p95 {f3(gec['p95'])} "
                  f"· p99 {f3(gec['p99'])} s")


def main() -> None:
    dizin = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else D
    kayit, kisa = oku(dizin)
    gorulen = sorted({t for h in HUCRE for k in KOLLAR for t in kayit[h][k]})
    if not gorulen:
        print("kayıt yok")
        return
    tohumlar = tuple(gorulen) if kisa else TOHUMLAR
    gecerlilik(kayit, kisa, tohumlar)
    hucre_tablolari(kayit, tohumlar)
    guclu = s1(kayit)
    s2(kayit, guclu)
    s3(kayit)
    s4(kayit)
    tavan(kayit)
    kahin(kayit)
    betimleyici(kayit)


if __name__ == "__main__":
    main()
