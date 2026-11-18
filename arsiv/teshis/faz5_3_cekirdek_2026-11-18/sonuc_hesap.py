"""Faz 5-3 · yeni sürümün çekirdeği ↔ Babel — beklentinin karar kuralını
kayıtlara uygular (simülasyon yok). Koşudan önce yazıldı.

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz5_3_cekirdek_2026-11-18/sonuc_hesap.py [kayıt dizini]

Argümansız: bu dizinin `kayit_cekirdek_*.json` dosyaları ve Babel, kâhin,
v0.4.1 için teşhis (c)'nin kayıtları (`../faz5_2_rakip_cizgisi_2026-11-15/`).
Bir dizin verilirse (duman koşusu) bütün kollar oradan okunur; Babel'in
kısa pencere satırları teşhis (c)'nin duman koşusuyla karşılaştırılır.
"""
import json
import math
import statistics as ist
import sys
from collections import Counter
from pathlib import Path

D = Path(__file__).resolve().parent
C = D.parent / "faz5_2_rakip_cizgisi_2026-11-15"
CEK, BABEL, KAHIN, V041 = ("desparete5_cekirdek", "babel",
                           "en_guvenilir_kahin", "desparete")
KOLLAR = (KAHIN, BABEL, CEK, V041)
AD = {KAHIN: "kâhin", BABEL: "Babel", CEK: "çekirdek", V041: "v0.4.1"}
HUCRE = ("ikiz", "birincil")
HAD = {"ikiz": "İ · karıştırıcısız ikiz (pencere PDR)",
       "birincil": "B · birincil, 15/15 (PDR_açık)"}
CIZELGE = {"birincil": "15/15"}
TOHUMLAR = tuple(range(1003, 1011))
GRUP = {"rota_gecersiz": "R", "hedef_yok": "R", "tampon_asimi": "R",
        "iletim_basarisiz": "I", "kuyruk_tasmasi": "K", "ttl": "T"}
COZUNURLUK = 0.0126                 # eşleştirilmiş R (K-224)
TAVAN = "5"                         # ana gecikme tavanı, saniye (K-246)
EK = "@tehdit_acik_s=10+tehdit_sessiz_s=20"
# Teşhis (c)'nin duman koşusu (`duman_kisa.txt`): Babel, tohum 1003, kısa
# pencere — (tüm koşu PDR'si, pencere PDR'si, üretilen).
DUMAN_BABEL = {"ikiz": (0.8109, 0.8631, 1597),
               "birincil": (0.5842, 0.6260, 1597)}


# ------------------------------------------------------------------ okuma
def _ekle(kayit, dosya: Path, kollar) -> bool:
    if not dosya.exists():
        return False
    k = json.loads(dosya.read_text(encoding="utf-8"))
    h = "ikiz" if k["sinif"] == "yok" else "birincil"
    for r in k["sonuc"]:
        if r["protokol"] not in kollar:
            continue                         # (c)'nin öteki kolları, D hücresi
        assert r["tohum"] not in kayit[h][r["protokol"]], (h, r["protokol"])
        kayit[h][r["protokol"]][r["tohum"]] = r
    return bool(k.get("kisa"))


def oku(dizin: Path, duman: bool):
    kayit = {h: {k: {} for k in KOLLAR} for h in HUCRE}
    kisa = False
    for ad in ("kayit_cekirdek_ikiz.json", "kayit_cekirdek_birincil.json"):
        kisa |= _ekle(kayit, dizin / ad, (CEK, BABEL) if duman else (CEK,))
    if not duman:
        for ad in ("kayit_ikiz.json", "kayit_birincil.json"):
            _ekle(kayit, C / ad, (BABEL, KAHIN))
        for ad in ("kayit_v041_ikiz.json", "kayit_v041_karistirma.json"):
            _ekle(kayit, C / ad, (V041,))
    return kayit, kisa


# ----------------------------------------------------------------- ölçüler
def oran(o: dict, tavan: str | None = None):
    t = o["teslim"] if tavan is None else o["teslim_tavan"][tavan]
    return t / o["dogan"] if o["dogan"] else None


def donem(h: str, r: dict, evre: str = "acik") -> dict:
    return r["ikincil"]["cizelge"][CIZELGE[h]][evre]


def olcu(h: str, r: dict, tavan: str | None = None):
    """Hücrenin birincil ölçüsü: İ'de pencere PDR'si, B'de PDR_açık."""
    if h == "ikiz":
        return oran(r["ikincil"]["pencere"], tavan)
    return oran(donem(h, r), tavan)


def dizi(kayit, h: str, kol: str, f) -> dict:
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
def gecerlilik(kayit, kisa: bool, duman: bool, tohumlar) -> None:
    print("== 0 · GEÇERLİLİK ==")
    for kol in ((CEK, BABEL) if duman else KOLLAR):
        eksik, kusurlu, tutarsiz = [], [], []
        for h in HUCRE:
            for t in tohumlar:
                r = kayit[h][kol].get(t)
                if r is None:
                    eksik.append(f"{h}/{t}")
                    continue
                if (not r["gecerli"] or r["dogum_celiski"]
                        or r["dogum_atfsiz"]):
                    kusurlu.append(f"{h}/{t}")
                p = oran(r["ikincil"]["pencere"])
                if p is None or abs(p - r["pdr_pencere"]) > 1e-12:
                    tutarsiz.append(f"{h}/{t}")
        print(f"  {AD[kol]:<9} koşu {2 * len(tohumlar) - len(eksik)}/"
              f"{2 * len(tohumlar)} · korunum, çelişki ya da atfsız düşüş "
              f"kusuru {len(kusurlu)} · ikincil sayımın pencere PDR'siyle "
              f"tutarsızlığı {len(tutarsiz)}"
              + (f" · eksik: {' '.join(eksik)}" if eksik else "")
              + (f" · kusurlu: {' '.join(kusurlu)}" if kusurlu else ""))
    if duman:
        print("  Babel ↔ teşhis (c)'nin duman koşusu (tohum 1003, kısa "
              "pencere; dört basamak):")
        for h in HUCRE:
            r = kayit[h][BABEL].get(1003)
            if r is None:
                print(f"      {h}: Babel satırı yok")
                continue
            simdi = (round(r["pdr"], 4), round(r["pdr_pencere"], 4),
                     r["uretilen"])
            print(f"      {h}: {simdi} ↔ {DUMAN_BABEL[h]} → "
                  + ("BİREBİR" if simdi == DUMAN_BABEL[h] else "FARKLI"))


# ------------------------------------------------------------------ tablolar
def hucre_tablolari(kayit, tohumlar) -> None:
    print("\n== 1 · HÜCRE TABLOLARI (tohum ortalaması ± ölçüt sapması) ==")
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
            print(f"    {AD[kol]:<9} {f3(ort(d))} ± {f3(ss(d))} "
                  f"[{min(d.values()):.3f} … {max(d.values()):.3f}] · "
                  f"5 s tavanlı {f3(tv)}{ek} · p99 {f3(p99)} s · kâhine oran "
                  f"{f3(ort(d) / kahin if kahin else None)}")
            print("              " + " · ".join(
                f"{t} {f3(d.get(t))}" for t in tohumlar))


def s1(kayit) -> None:
    print("\n== 2 · S1 — genel düzey, İ: G = Babel − çekirdek (eşik 0,02) ==")
    h = "ikiz"
    cek = dizi(kayit, h, CEK, lambda r: olcu(h, r))
    bab = dizi(kayit, h, BABEL, lambda r: olcu(h, r))
    e = esli(bab, cek)
    hukum = ayris(e, 0.02)
    print(f"  G {esli_metni(e)} → {hukum}")
    if hukum.endswith("(+)"):
        print("  → ÇEKİRDEK GERİDE: sıradaki iş genel açığın teşhisi "
              "(kayıp grupları, atlama, kontrol payı, veri tetiği), "
              "karıştırma katmanının A/B'leri ondan sonra")
    elif hukum.endswith("(−)"):
        print("  → ÇEKİRDEK İLERİDE: sıradaki iş karıştırma katmanı")
    elif e[0] is not None:
        print("  → AYIRT EDİLEMEDİ: sıradaki iş karıştırma katmanı")
    v = dizi(kayit, h, V041, lambda r: olcu(h, r))
    if v:
        e = esli(cek, v)
        print(f"  çekirdek − v0.4.1: {esli_metni(e)} → {ayris(e, 0.02)}")


def s2(kayit) -> None:
    print("\n== 3 · S2 — başlangıç çizgisi, B (betimleyici) ==")
    h = "birincil"
    cek = dizi(kayit, h, CEK, lambda r: olcu(h, r))
    for kol in (BABEL, V041):
        a = dizi(kayit, h, kol, lambda r: olcu(h, r))
        if a:
            e = esli(a, cek)
            print(f"  {AD[kol]} − çekirdek: {esli_metni(e)} → "
                  f"{ayris(e, 0.02)}")
    print("  Δ_k = PDR_açık(B) − hayalet PDR_açık(İ, 15/15):")
    dk = {}
    for kol in KOLLAR:
        a = dizi(kayit, h, kol, lambda r: olcu(h, r))
        b = dizi(kayit, "ikiz", kol, lambda r: oran(
            r["ikincil"]["cizelge"]["15/15"]["acik"]))
        e = esli(a, b)
        if e[0] is None:
            continue
        dk[kol] = e[4]
        print(f"    {AD[kol]:<9} Δ_k {e[0]:+.3f} ± {f3(ss(e[4]))} (hayalet "
              f"{f3(ort({t: b[t] for t in e[4]}))} → hücre "
              f"{f3(ort({t: a[t] for t in e[4]}))}) · "
              + " · ".join(f"{t} {v:+.3f}" for t, v in e[4].items()))
    if CEK in dk and BABEL in dk:
        e = esli(dk[CEK], dk[BABEL])
        print(f"  Δ_k(çekirdek) − Δ_k(Babel): {esli_metni(e)} → "
              f"{ayris(e, 0.03)}")


def s3(kayit) -> None:
    print("\n== 4 · S3 — kontrol yükü ve gecikme (T-19) ==")
    for h in HUCRE:
        print(f"  {HAD[h]}")
        for kol in KOLLAR:
            rs = list(kayit[h][kol].values())
            if not rs:
                continue
            n = len(rs)
            kon = sum(r["sayaclar"]["kontrol_airtime_s"] for r in rs) / n
            top = sum(r["enerji_s"]["enerji_gonderim_s"] for r in rs) / n
            b = {s: ort(dizi(kayit, h, kol, lambda r: (
                None if olcu(h, r) is None else olcu(h, r) - olcu(h, r, s))))
                for s in ("3.5", "5", "10")}
            gec = {p: ort(dizi(kayit, h, kol, lambda r: r["gecikme_s"][p]))
                   for p in ("p50", "p95", "p99")}
            print(f"    {AD[kol]:<9} kontrol kanal süresi {kon:.1f} s · "
                  f"toplam gönderim {top:.0f} s · kontrol payı "
                  f"{kon / top:.1%} | tavan bedeli 3,5 s {f3(b['3.5'])} · "
                  f"5 s {f3(b['5'])} · 10 s {f3(b['10'])}"
                  + ("  → TAVAN BAĞLAYICI" if (b["5"] or 0) >= 0.02 else "")
                  + f" | gecikme p50 {f3(gec['p50'])} · p95 "
                  f"{f3(gec['p95'])} · p99 {f3(gec['p99'])} s")


TANI = ("bag.veri_kotu", "bag.askida_giris", "bag.kotu_selam",
        "bag.kotu_donus", "bag.yeni_komsu", "bag.komsu_silindi",
        "bag.df_bayat", "rota.ardil_degisti", "rota.zorunlu_gecis",
        "rota.istege_bagli_gecis", "rota.aclik", "rota.aclik_bitti",
        "rota.aclik_istegi", "rota.tur_artirildi", "rota.istek_iletilen",
        "rota.istek_karsilandi", "rota.uygulanamaz_yoksayilan",
        "rota.geri_cekme_alinan", "selam.selam", "selam.ara_ilan",
        "bekletme.bekletilen", "bekletme.suresi_dolan",
        "protokol.komut_gonderilen", "protokol.komut_bekletilen",
        "protokol.komut_dusen", "iz.iz_eski_sira")


def s4(kayit) -> None:
    print("\n== 5 · S4 — tanı (betimleyici; kanal yükü bütün koşu, ağ "
          "toplamı, tohum ortalaması) ==")
    for h in HUCRE:
        print(f"  {HAD[h]}")
        for kol in KOLLAR:
            rs = list(kayit[h][kol].values())
            if not rs:
                continue
            g = gruplar(h, rs)
            d = sum(r["veri_deneme"] for r in rs)
            basari = sum(r["sayaclar"]["mac_gonderim_basarili"] for r in rs)
            karar = sum(r["karar_sayisi"] for r in rs)
            dusus = sum(sum(r["basarisiz_bant"].values()) for r in rs)
            print(f"    {AD[kol]:<9} kayıp R {f3(g['R'])} · İ {f3(g['I'])} · "
                  f"K {f3(g['K'])} · T {f3(g['T'])}"
                  + (f" · ? {f3(g['?'])}" if g["?"] else "")
                  + f" | karar/paket "
                  f"{karar / sum(r['uretilen'] for r in rs):.2f} · atlama "
                  f"başarısızlığı {dusus / karar:.2%} · deneme başarısı g "
                  f"{basari / d:.3f}")
        rs = list(kayit[h][CEK].values())
        if rs:
            n = len(rs)
            top = {k: sum(r["teshis_toplam"].get(k, 0) for r in rs) / n
                   for k in TANI}
            print("    çekirdeğin sayaçları (koşu başına, ağ toplamı): "
                  + " · ".join(f"{k} {v:.1f}" for k, v in top.items()))
            bitti = sum(r["teshis_toplam"].get("rota.aclik_bitti", 0)
                        for r in rs)
            sure = sum(r["teshis_toplam"].get("rota.aclik_sure_ms", 0)
                       for r in rs)
            print(f"    açlığın ortalama süresi "
                  f"{(sure / bitti / 1000.0) if bitti else float('nan'):.2f}"
                  f" s ({bitti} açlık)")


def kahin(kayit) -> None:
    print(f"\n== 6 · KÂHİN — tohum başına aşım (kol − kâhin > R = "
          f"{COZUNURLUK}) ==")
    for h in HUCRE:
        k = dizi(kayit, h, KAHIN, lambda r: olcu(h, r))
        for kol in (BABEL, CEK, V041):
            e = esli(dizi(kayit, h, kol, lambda r: olcu(h, r)), k)
            if e[0] is None:
                continue
            asan = {t: v for t, v in e[4].items() if v > COZUNURLUK}
            print(f"  {h:<9} {AD[kol]:<9} ortalama fark {e[0]:+.3f} · aşan "
                  f"tohum {len(asan)}/{e[3]}"
                  + (": " + " · ".join(f"{t} {v:+.3f}"
                                       for t, v in asan.items())
                     if asan else ""))


def main() -> None:
    duman = len(sys.argv) > 1
    dizin = Path(sys.argv[1]).resolve() if duman else D
    kayit, kisa = oku(dizin, duman)
    gorulen = sorted({t for h in HUCRE for k in KOLLAR for t in kayit[h][k]})
    if not gorulen:
        print("kayıt yok")
        return
    tohumlar = tuple(gorulen) if duman else TOHUMLAR
    gecerlilik(kayit, kisa, duman, tohumlar)
    hucre_tablolari(kayit, tohumlar)
    s1(kayit)
    s2(kayit)
    s3(kayit)
    s4(kayit)
    kahin(kayit)


if __name__ == "__main__":
    main()
