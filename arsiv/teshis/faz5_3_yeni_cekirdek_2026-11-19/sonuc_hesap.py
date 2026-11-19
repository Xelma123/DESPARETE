"""Faz 5-3 · yeni çekirdek — beklentinin karar kuralını kayıtlara uygular
(simülasyon yok). Koşudan önce yazıldı.

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz5_3_yeni_cekirdek_2026-11-19/sonuc_hesap.py [duman dizini]

Argümansız: bu dizinin `kayit_<kol>_<hücre>.json` dosyaları (`olcum.py`);
Babel, kâhin ve v0.4.1 için teşhis (c)'nin kayıtları
(`../faz5_2_rakip_cizgisi_2026-11-15/`); 18 Kasım'ın çekirdeği için ilk
ölçümün kayıtları (`../faz5_3_cekirdek_2026-11-18/`); veri tetiği kapalı
18 Kasım çekirdeği (`vtk0`, yalnız ikiz) için açlık teşhisinin kaydı
(`../faz5_3_aclik_2026-11-18/`).

Bir dizin verilirse (duman) yeni kollar oradan okunur ve kural 0'ın duman
denetimleri yapılır: kaydedicili `cekirdek` ↔ doğrudan kayıp anatomisi
aletiyle koşulan `cekirdek` (`duz_<hücre>.json`), `eski` ↔ ilk ölçümün duman
kaydı.
"""
import json
import math
import statistics as ist
import sys
from collections import Counter
from pathlib import Path

D = Path(__file__).resolve().parent
C = D.parent / "faz5_2_rakip_cizgisi_2026-11-15"
ILK = D.parent / "faz5_3_cekirdek_2026-11-18"
ACLIK = D.parent / "faz5_3_aclik_2026-11-18"
KAHIN, BABEL, V041 = "en_guvenilir_kahin", "babel", "desparete"
ESKI, VTK0 = "eski", "vtk0"
CEK, VAZ0, DUZ0, EGIM0 = "cekirdek", "vaz0", "duz0", "egim0"
YENI = (CEK, VAZ0, DUZ0, EGIM0)
KOLLAR = (KAHIN, BABEL, V041, ESKI, VTK0) + YENI
AD = {KAHIN: "kâhin", BABEL: "Babel", V041: "v0.4.1", ESKI: "eski çek.",
      VTK0: "vtk0", CEK: "çekirdek", VAZ0: "vaz0", DUZ0: "düz0",
      EGIM0: "eğim0"}
DESPARETE5 = (ESKI, VTK0) + YENI
HUCRE = ("ikiz", "birincil")
HAD = {"ikiz": "İ · karıştırıcısız ikiz (pencere PDR)",
       "birincil": "B · birincil, 15/15 (PDR_açık)"}
CIZELGE = {"birincil": "15/15"}
TOHUMLAR = tuple(range(1003, 1011))
GRUP = {"rota_gecersiz": "R", "hedef_yok": "R", "tampon_asimi": "R",
        "iletim_basarisiz": "I", "kuyruk_tasmasi": "K", "ttl": "T"}
COZUNURLUK = 0.0126                 # eşleştirilmiş R (K-224)
TAVAN = "5"                         # ana gecikme tavanı, saniye (K-246)
ESIK = 0.02                         # düzey ve bileşen farkı (S1, S2, S4)
ESIK_DK = 0.03                      # Δ_k farkı
# Bileşenler (S4): (ad, açık kol, kapalı kol)
MEKANIZMA = (("vazgeçme tetiği", CEK, VAZ0),
             ("iki ölçülü geçiş", CEK, DUZ0),
             ("eğim (tetiksiz)", VAZ0, EGIM0))


# ------------------------------------------------------------------ okuma
def _ekle(kayit, dosya: Path, kollar: dict, hucre: str | None = None) -> bool:
    """`kollar`: kayıttaki anahtar → bu betiğin kolu. Anahtar `kol` alanı
    varsa odur, yoksa `protokol`."""
    if not dosya.exists():
        return False
    k = json.loads(dosya.read_text(encoding="utf-8"))
    h = hucre or k.get("hucre") or ("ikiz" if k["sinif"] == "yok"
                                    else "birincil")
    for r in k["sonuc"]:
        kol = kollar.get(r.get("kol") or r["protokol"])
        if kol is None:
            continue                         # (c)'nin öteki kolları, D hücresi
        assert r["tohum"] not in kayit[h][kol], (h, kol, r["tohum"])
        kayit[h][kol][r["tohum"]] = r
    return bool(k.get("kisa"))


def oku(dizin: Path, duman: bool):
    kayit = {h: {k: {} for k in KOLLAR} for h in HUCRE}
    kisa = False
    yeni = {k: k for k in YENI + ((ESKI,) if duman else ())}
    for dosya in sorted(dizin.glob("kayit_*.json")):
        kisa |= _ekle(kayit, dosya, yeni)
    if not duman:
        for ad in ("kayit_ikiz.json", "kayit_birincil.json"):
            _ekle(kayit, C / ad, {BABEL: BABEL, KAHIN: KAHIN})
        for ad in ("kayit_v041_ikiz.json", "kayit_v041_karistirma.json"):
            _ekle(kayit, C / ad, {V041: V041})
        for ad in ("kayit_cekirdek_ikiz.json", "kayit_cekirdek_birincil.json"):
            _ekle(kayit, ILK / ad, {"desparete5_cekirdek": ESKI})
        _ekle(kayit, ACLIK / "kayit_vtk0.json", {VTK0: VTK0}, "ikiz")
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


def ort(d):
    d = list(d.values()) if isinstance(d, dict) else list(d)
    return ist.mean(d) if d else None


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
def _fark(a: dict, b: dict, atla=(), yeni_sifir=()) -> list[str]:
    """İki sonuç satırının farklı alanları. `yeni_sifir`: yalnız `a`da olup
    sıfır olması gereken alt anahtarlar (sözlük alanlarında)."""
    fark = []
    for k in sorted(set(a) | set(b)):
        if k in atla:
            continue
        if k not in a or k not in b:
            fark.append(f"{k} (yalnız {'yeni' if k in a else 'eski'})")
            continue
        x, y = a[k], b[k]
        if isinstance(x, dict) and isinstance(y, dict) and k in yeni_sifir:
            for kk in sorted(set(x) | set(y)):
                if kk in x and kk in y:
                    if x[kk] != y[kk]:
                        fark.append(f"{k}.{kk}")
                elif kk in x:
                    if x[kk] != 0:
                        fark.append(f"{k}.{kk} (yeni, sıfır değil)")
                else:
                    fark.append(f"{k}.{kk} (yalnız eski)")
        elif x != y:
            fark.append(k)
    return fark


def gecerlilik(kayit, duman: bool, dizin: Path, tohumlar) -> None:
    print("== 0 · GEÇERLİLİK ==")
    kollar = (YENI + (ESKI,)) if duman else KOLLAR
    for kol in kollar:
        beklenen = [(h, t) for h in HUCRE for t in tohumlar
                    if not (kol == VTK0 and h == "birincil")]
        eksik, kusurlu, tutarsiz, denetim = [], [], [], []
        for h, t in beklenen:
            r = kayit[h][kol].get(t)
            if r is None:
                eksik.append(f"{h}/{t}")
                continue
            if not r["gecerli"] or r["dogum_celiski"] or r["dogum_atfsiz"]:
                kusurlu.append(f"{h}/{t}")
            p = oran(r["ikincil"]["pencere"])
            if p is None or abs(p - r["pdr_pencere"]) > 1e-12:
                tutarsiz.append(f"{h}/{t}")
            if r.get("kaydedici_denetim"):
                denetim.append(f"{h}/{t}: {r['kaydedici_denetim']}")
        print(f"  {AD[kol]:<9} koşu {len(beklenen) - len(eksik)}/"
              f"{len(beklenen)} · korunum, çelişki ya da atfsız düşüş kusuru "
              f"{len(kusurlu)} · ikincil sayımın tutarsızlığı {len(tutarsiz)}"
              + (" · kaydedicinin iç denetimi "
                 + ("tamam" if not denetim else "; ".join(denetim))
                 if kol in YENI or (duman and kol == ESKI) else "")
              + (f" · eksik: {' '.join(eksik)}" if eksik else "")
              + (f" · kusurlu: {' '.join(kusurlu)}" if kusurlu else ""))
    if not duman:
        return
    atla_k = ("sure_s", "kol", "hucre", "kaydedici", "kaydedici_denetim")
    print("  Kaydedici koşuyu değiştirmiyor — kaydedicili `cekirdek` ↔ "
          "doğrudan kayıp anatomisi aleti (tohum 1003, kısa pencere):")
    for h in HUCRE:
        a = kayit[h][CEK].get(1003)
        dosya = dizin / f"duz_{h}.json"
        if a is None or not dosya.exists():
            print(f"      {h}: satır yok")
            continue
        b = json.loads(dosya.read_text(encoding="utf-8"))["sonuc"][0]
        f = _fark(a, b, atla=atla_k)
        print(f"      {h}: " + ("BİREBİR (bütün alanlar)" if not f
                                else "FARKLI: " + ", ".join(f)))
    print("  `eski` ↔ ilk ölçümün duman kaydı (`desparete5_cekirdek`, tohum "
          "1003, kısa pencere; ortak sayaçlar eşit, yeni sayaçlar sıfır):")
    for h in HUCRE:
        a = kayit[h][ESKI].get(1003)
        dosya = ILK / "duman" / f"kayit_cekirdek_{h}.json"
        b = None
        if dosya.exists():
            b = next((r for r in json.loads(dosya.read_text(
                encoding="utf-8"))["sonuc"]
                if r["protokol"] == "desparete5_cekirdek"
                and r["tohum"] == 1003), None)
        if a is None or b is None:
            print(f"      {h}: satır yok")
            continue
        f = _fark(a, b, atla=atla_k + ("protokol",),
                  yeni_sifir=("teshis_toplam",))
        print(f"      {h}: " + ("BİREBİR" if not f
                                else "FARKLI: " + ", ".join(f)))


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
    print(f"\n== 2 · S1 — genel düzey, İ: G = Babel − çekirdek (eşik "
          f"{ESIK}) ==")
    h = "ikiz"
    cek = dizi(kayit, h, CEK, lambda r: olcu(h, r))
    bab = dizi(kayit, h, BABEL, lambda r: olcu(h, r))
    e = esli(bab, cek)
    hukum = ayris(e, ESIK)
    print(f"  G {esli_metni(e)} → {hukum}")
    if hukum.endswith("(+)"):
        print("  → ÇEKİRDEK GERİDE: sıradaki iş genel açığın teşhisi (S4'ün "
              "bileşenleri ve S5'in tanısı girdisi); karıştırma katmanı "
              "ondan sonra")
    elif hukum.endswith("(−)"):
        print("  → ÇEKİRDEK İLERİDE: S4'te zararlı bileşen yoksa sıradaki iş "
              "karıştırma katmanı")
    elif e[0] is not None:
        print("  → AYIRT EDİLEMEDİ: S4'te zararlı bileşen yoksa sıradaki iş "
              "karıştırma katmanı")
    for kol in (VTK0, ESKI, V041):
        a = dizi(kayit, h, kol, lambda r: olcu(h, r))
        if a:
            e = esli(cek, a)
            print(f"  çekirdek − {AD[kol]}: {esli_metni(e)} → "
                  f"{ayris(e, ESIK)}")


def s2(kayit) -> None:
    print("\n== 3 · S2 — başlangıç çizgisi, B (betimleyici) ==")
    h = "birincil"
    cek = dizi(kayit, h, CEK, lambda r: olcu(h, r))
    for kol in (BABEL, V041, ESKI):
        a = dizi(kayit, h, kol, lambda r: olcu(h, r))
        if a:
            e = esli(a, cek)
            print(f"  {AD[kol]} − çekirdek: {esli_metni(e)} → "
                  f"{ayris(e, ESIK)}")
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
              f"{ayris(e, ESIK_DK)}")


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
                  + ("  → TAVAN BAĞLAYICI" if (b["5"] or 0) >= ESIK else "")
                  + f" | gecikme p50 {f3(gec['p50'])} · p95 "
                  f"{f3(gec['p95'])} · p99 {f3(gec['p99'])} s")


def s4(kayit) -> None:
    print(f"\n== 5 · S4 — bileşenler: açık − kapalı, eşli (eşik {ESIK}) ==")
    zararli = []
    for ad, acik, kapali in MEKANIZMA:
        print(f"  {ad}: {AD[acik]} − {AD[kapali]}")
        for h in HUCRE:
            a = dizi(kayit, h, acik, lambda r: olcu(h, r))
            b = dizi(kayit, h, kapali, lambda r: olcu(h, r))
            e = esli(a, b)
            hukum = ayris(e, ESIK)
            if hukum.endswith("(+)"):
                anlam = "katkı var" if h == "ikiz" else "birincilde katkı"
            elif hukum.endswith("(−)"):
                anlam = "ZARARLI" if h == "ikiz" else "BİRİNCİLDE ZARAR"
                zararli.append(f"{ad} ({h})")
            elif e[0] is None:
                anlam = "veri yok"
            else:
                anlam = ("katkı ayırt edilemedi" if h == "ikiz"
                         else "zarar yok (ayırt edilemedi)")
            print(f"    {h:<9} {esli_metni(e)} → {hukum} → {anlam}")
    print("  → " + ("zararlı bileşen: " + ", ".join(zararli)
                    + " — karıştırma katmanından önce teşhisi"
                    if zararli else "zararlı bileşen yok"))
    print("  Betimleyici:")
    for ad, a_k, b_k, hucreler in (
            ("yeni yol seçimi bütünüyle", CEK, EGIM0, HUCRE),
            ("19 Kasım ↔ 18 Kasım çekirdeği", CEK, ESKI, HUCRE),
            ("bekletme 1 s ↔ 2 s (18 Kasım yol seçimi, tetiksiz)", EGIM0,
             VTK0, ("ikiz",))):
        for h in hucreler:
            e = esli(dizi(kayit, h, a_k, lambda r: olcu(h, r)),
                     dizi(kayit, h, b_k, lambda r: olcu(h, r)))
            print(f"    {ad}, {h}: {AD[a_k]} − {AD[b_k]} {esli_metni(e)} → "
                  f"{ayris(e, ESIK)}")


TANI = ("bag.vaz_tetik", "bag.vazgecme", "bag.vaz_katlama", "bag.kotu_selam",
        "bag.kotu_donus", "bag.komsu_silindi", "bag.df_bayat",
        "rota.ardil_degisti", "rota.zorunlu_gecis", "rota.istege_bagli_gecis",
        "rota.veri_gecis", "rota.son_care", "rota.yol_yok", "rota.tavan_asimi",
        "rota.bayat_bilgi", "rota.dongu", "rota.dislama", "rota.aclik",
        "rota.tur_artirildi", "selam.selam", "selam.ara_ilan",
        "bekletme.bekletilen", "bekletme.suresi_dolan",
        "protokol.komut_gonderilen", "protokol.komut_bekletilen",
        "protokol.komut_dusen")


def _yuzdelik(sayim: dict, q: float):
    """Tamsayı anahtarlı sayımın q yüzdeliği (anahtarın kendisi)."""
    top = sum(sayim.values())
    if not top:
        return None
    birikim = 0
    for k in sorted(sayim):
        birikim += sayim[k]
        if birikim >= q * top:
            return k
    return max(sayim)


def s5(kayit) -> None:
    print("\n== 6 · S5 — tanı (betimleyici; sayaçlar bütün koşu, ağ toplamı, "
          "koşu başına) ==")
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
        print("    vazgeçmelerin bağlara dağılımı (bütün koşu): vazgeçme · "
              "ayrı bağ · en kötü bağ · en kötü 5 bağın payı")
        for kol in DESPARETE5:
            rs = list(kayit[h][kol].values())
            if not rs:
                continue
            top = [sum(v for kk, v in r["tablo"].items()
                       if kk.startswith("iletim_basarisiz|")) for r in rs]
            b5 = [r["basarisiz_en_cok_5_bag"] for r in rs]
            en = [b[0][2] if b else 0 for b in b5]
            pay = [sum(x[2] for x in b) / t if t else 0.0
                   for b, t in zip(b5, top)]
            print(f"      {AD[kol]:<9} {ort(top):.0f} · "
                  f"{ort([r['basarisiz_bag_sayisi'] for r in rs]):.0f} · "
                  f"{ort(en):.0f} ({min(en)}–{max(en)}) · {ort(pay):.2f} "
                  f"({min(pay):.2f}–{max(pay):.2f})")
        print("    sayaçlar (koşu başına):")
        for kol in YENI:
            rs = list(kayit[h][kol].values())
            if not rs:
                continue
            n = len(rs)
            tt = [r["teshis_toplam"] for r in rs]
            parca = [f"{k.split('.', 1)[1]} {sum(t.get(k, 0) for t in tt) / n:.1f}"
                     for k in TANI if any(k in t for t in tt)]
            print(f"      {AD[kol]:<9} " + " · ".join(parca))
            bitti = sum(t.get("rota.yol_yok_bitti", 0) for t in tt)
            sure = sum(t.get("rota.yol_yok_sure_ms", 0) for t in tt)
            if bitti:
                print(f"                yol yok bölümünün ortalama süresi "
                      f"{sure / bitti / 1000.0:.2f} s ({bitti / n:.1f} biten "
                      f"bölüm)")
        print("    kaynağın geçide maliyeti (penceredeki telemetri, ETX; "
              "1 ETX'lik kutunun alt sınırı) · teslim edilenin atlama sayısı")
        for kol in YENI:
            rs = list(kayit[h][kol].values())
            if not rs:
                continue
            mal, atl = Counter(), Counter()
            for r in rs:
                z = r["kaydedici"]
                mal.update(z["maliyet"])
                atl.update({int(k): v for k, v in z["atlama"].items()})
            sonlu = {int(k): v for k, v in mal.items() if k.isdigit()}
            top = sum(mal.values())
            if not top:
                print(f"      {AD[kol]:<9} telemetri kaydı yok")
                continue
            ust16 = sum(v for k, v in sonlu.items() if k >= 16)
            print(f"      {AD[kol]:<9} maliyet p50 {_yuzdelik(sonlu, 0.5)} · "
                  f"p90 {_yuzdelik(sonlu, 0.9)} · p99 "
                  f"{_yuzdelik(sonlu, 0.99)} · en çok "
                  f"{max(r['kaydedici']['en_maliyet_etx'] for r in rs):.1f} · "
                  f"≥ 16 ETX {ust16 / top:.4f} · ∞ "
                  f"{mal.get('inf', 0) / top:.4f} | atlama p50 "
                  f"{_yuzdelik(atl, 0.5)} · p90 {_yuzdelik(atl, 0.9)} · p99 "
                  f"{_yuzdelik(atl, 0.99)} · en çok (teslim) "
                  f"{max(atl) if atl else None} · en çok (bütün kararlar) "
                  f"{max(r['kaydedici']['en_atlama'] for r in rs)}")
        print("    vazgeçme tetiği (penceredeki tetikler; kâhin bandı 7 "
              "denemelik atlama başarısından)")
        for kol in (CEK, DUZ0):
            rs = list(kayit[h][kol].values())
            if not rs:
                continue
            tet, bant = [], Counter()
            for r in rs:
                z = r["kaydedici"]
                bas, bit = z["pencere"]
                for c in z["tetik"]:
                    if bas <= c[2] < bit:
                        tet.append(c)
                        p = 1.0 - (1.0 - c[5]) ** z["deneme"]
                        bant["iyi" if p >= 0.90 else ("orta" if p >= 0.50
                                                      else "kotu")] += 1
            if not tet:
                print(f"      {AD[kol]:<9} tetik yok")
                continue
            ardil = [c for c in tet if c[3]]
            degisti = [c[6] for c in ardil if c[6] is not None]
            sure = Counter(c[4] for c in tet)
            print(f"      {AD[kol]:<9} tetik/koşu {len(tet) / len(rs):.1f} · "
                  f"kâhin iyi {bant['iyi'] / len(tet):.2f} · orta "
                  f"{bant['orta'] / len(tet):.2f} · kötü "
                  f"{bant['kotu'] / len(tet):.2f} · ardıl payı "
                  f"{len(ardil) / len(tet):.2f} · ardılın değiştiği pay "
                  f"{(len(degisti) / len(ardil)) if ardil else 0:.2f} "
                  f"(medyan {ist.median(degisti) if degisti else 0:.2f} s) · "
                  f"işaretliyken veri sonucu/tetik "
                  f"{sum(c[7] for c in tet) / len(tet):.2f} · vazgeçme/tetik "
                  f"{sum(c[8] for c in tet) / len(tet):.2f} · bekleme "
                  + " · ".join(f"{s:g} s {v / len(tet):.2f}"
                               for s, v in sorted(sure.items())))


def kahin(kayit) -> None:
    print(f"\n== 7 · KÂHİN — tohum başına aşım (kol − kâhin > R = "
          f"{COZUNURLUK}) ==")
    for h in HUCRE:
        k = dizi(kayit, h, KAHIN, lambda r: olcu(h, r))
        for kol in (BABEL,) + YENI:
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
    gorulen = sorted({t for h in HUCRE for k in YENI for t in kayit[h][k]})
    if not gorulen:
        print("kayıt yok")
        return
    tohumlar = tuple(gorulen) if duman else TOHUMLAR
    if kisa:
        print("KISA PENCERE — duman; ölçüm değil, hiçbir karara girmez\n")
    gecerlilik(kayit, duman, dizin, tohumlar)
    hucre_tablolari(kayit, tohumlar)
    s1(kayit)
    s2(kayit)
    s3(kayit)
    s4(kayit)
    s5(kayit)
    kahin(kayit)


if __name__ == "__main__":
    main()
