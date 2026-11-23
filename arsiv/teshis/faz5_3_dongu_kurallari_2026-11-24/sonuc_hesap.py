"""Faz 5-3 · döngü kuralları — beklentinin karar kuralını kayıtlara uygular
(simülasyon yok). Koşudan önce yazıldı.

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz5_3_dongu_kurallari_2026-11-24/sonuc_hesap.py [duman dizini]

Argümansız: bu dizinin `kayit_<kol>_<hücre>.json` dosyaları (`olcum.py`);
19 Kasım çekirdeği (`c19`) ve eğim0 için yeni çekirdeğin ölçümünün kayıtları
(`../faz5_3_yeni_cekirdek_2026-11-19/`); Babel ve kâhin için teşhis (c)'nin
kayıtları. Ölçüler, eşli fark ve ayrışma kuralı yeni çekirdeğin ölçümünün
`sonuc_hesap.py`'sinden aynen alınır (içe aktarılır; o dosya donmuştur).

Bir dizin verilirse (duman) yeni kollar oradan okunur ve kural 0'ın duman
denetimleri yapılır: kaydedicili `geri_sinir` ↔ doğrudan kayıp anatomisi
aletiyle koşulan aynı kol (`duz_<hücre>.json`); `c19` ↔ yeni çekirdeğin
ölçümünün `cekirdek` duman satırı.
"""
import importlib.util
import json
import statistics as ist
import sys
from collections import Counter
from pathlib import Path

D = Path(__file__).resolve().parent
ONCEKI = D.parent / "faz5_3_yeni_cekirdek_2026-11-19"
_spec = importlib.util.spec_from_file_location("sh19",
                                               ONCEKI / "sonuc_hesap.py")
sh = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sh)

KAHIN, BABEL = sh.KAHIN, sh.BABEL
C19, EGIM0, GERI, GS = "c19", "egim0", "geri", "geri_sinir"
YENI = (GERI, GS)
KOLLAR = (KAHIN, BABEL, EGIM0, C19, GERI, GS)
AD = {KAHIN: "kâhin", BABEL: "Babel", EGIM0: "eğim0", C19: "19 Kasım",
      GERI: "geri", GS: "geri+sınır"}
HUCRE, HAD, TOHUMLAR = sh.HUCRE, sh.HAD, sh.TOHUMLAR
ESIK = sh.ESIK                      # 0,02
ESIK_DONGU = 0.10                   # K6: c19'un döngü dönüşünün en çok %10'u
olcu, oran, donem, dizi = sh.olcu, sh.oran, sh.donem, sh.dizi
ort, ss, f3 = sh.ort, sh.ss, sh.f3
esli, ayris, esli_metni = sh.esli, sh.ayris, sh.esli_metni


# ------------------------------------------------------------------ okuma
def oku(dizin: Path, duman: bool):
    kayit = {h: {k: {} for k in KOLLAR} for h in HUCRE}
    kisa = False
    yeni = {k: k for k in YENI + ((C19,) if duman else ())}
    for dosya in sorted(dizin.glob("kayit_*.json")):
        kisa |= sh._ekle(kayit, dosya, yeni)
    if not duman:
        for h in HUCRE:
            sh._ekle(kayit, ONCEKI / f"kayit_cekirdek_{h}.json",
                     {"cekirdek": C19})
            sh._ekle(kayit, ONCEKI / f"kayit_egim0_{h}.json",
                     {"egim0": EGIM0})
        for ad in ("kayit_ikiz.json", "kayit_birincil.json"):
            sh._ekle(kayit, sh.C / ad, {BABEL: BABEL, KAHIN: KAHIN})
    return kayit, kisa


def sayac(r: dict, ad: str) -> float:
    return r["teshis_toplam"].get(ad, 0)


# -------------------------------------------------------------- geçerlilik
def gecerlilik(kayit, duman: bool, dizin: Path, tohumlar) -> None:
    print("== 0 · GEÇERLİLİK ==")
    for kol in (YENI + (C19,)) if duman else KOLLAR:
        eksik, kusurlu, denetim = [], [], []
        for h in HUCRE:
            for t in tohumlar:
                r = kayit[h][kol].get(t)
                if r is None:
                    eksik.append(f"{h}/{t}")
                    continue
                if (not r["gecerli"] or r["dogum_celiski"]
                        or r["dogum_atfsiz"]
                        or abs(oran(r["ikincil"]["pencere"])
                               - r["pdr_pencere"]) > 1e-12):
                    kusurlu.append(f"{h}/{t}")
                if r.get("kaydedici_denetim"):
                    denetim.append(f"{h}/{t}: {r['kaydedici_denetim']}")
        n = 2 * len(tohumlar)
        print(f"  {AD[kol]:<10} koşu {n - len(eksik)}/{n} · kusur "
              f"{len(kusurlu)}"
              + (" · kaydedicinin iç denetimi "
                 + ("tamam" if not denetim else "; ".join(denetim))
                 if kol in YENI or duman else "")
              + (f" · eksik: {' '.join(eksik)}" if eksik else "")
              + (f" · kusurlu: {' '.join(kusurlu)}" if kusurlu else ""))
    if not duman:
        return
    atla = ("sure_s", "kol", "hucre", "kaydedici_denetim")
    print("  Kaydedici koşuyu değiştirmiyor — kaydedicili `geri_sinir` ↔ "
          "doğrudan kayıp anatomisi aleti (tohum 1003, kısa pencere):")
    for h in HUCRE:
        a = kayit[h][GS].get(1003)
        dosya = dizin / f"duz_{h}.json"
        if a is None or not dosya.exists():
            print(f"      {h}: satır yok")
            continue
        b = json.loads(dosya.read_text(encoding="utf-8"))["sonuc"][0]
        f = sh._fark(a, b, atla=atla + ("kaydedici",))
        print(f"      {h}: " + ("BİREBİR (bütün alanlar)" if not f
                                else "FARKLI: " + ", ".join(f)))
    print("  `c19` ↔ yeni çekirdeğin ölçümünün `cekirdek` duman satırı "
          "(tohum 1003, kısa pencere; ortak alanlar ve sayaçlar eşit, yeni "
          "sayaçlar sıfır; kaydedicinin özeti bayrak listesi dışında eşit):")
    for h in HUCRE:
        a = kayit[h][C19].get(1003)
        dosya = ONCEKI / "duman" / f"kayit_duman_{h}.json"
        b = None
        if dosya.exists():
            b = next((r for r in json.loads(dosya.read_text(
                encoding="utf-8"))["sonuc"]
                if r["kol"] == "cekirdek" and r["tohum"] == 1003), None)
        if a is None or b is None:
            print(f"      {h}: satır yok")
            continue
        ka = {k: v for k, v in a["kaydedici"].items() if k != "bayraklar"}
        kb = {k: v for k, v in b["kaydedici"].items() if k != "bayraklar"}
        f = sh._fark(a, b, atla=atla + ("protokol", "kaydedici"),
                     yeni_sifir=("teshis_toplam",))
        if ka != kb:
            f.append("kaydedici")
        print(f"      {h}: " + ("BİREBİR" if not f
                                else "FARKLI: " + ", ".join(f)))


# ------------------------------------------------------------------ tablolar
def tablolar(kayit, tohumlar) -> None:
    print("\n== 1 · DÜZEYLER (tohum ortalaması ± ölçüt sapması) ==")
    for h in HUCRE:
        print(f"  {HAD[h]}")
        for kol in KOLLAR:
            d = dizi(kayit, h, kol, lambda r: olcu(h, r))
            if not d:
                continue
            p99 = ort(dizi(kayit, h, kol, lambda r: r["gecikme_s"]["p99"]))
            ek = ""
            if h != "ikiz":
                ek = " · sessiz " + f3(ort(dizi(kayit, h, kol, lambda r: oran(
                    donem(h, r, "sessiz")))))
            dong = (ort([sayac(r, "rota.dongu")
                         for r in kayit[h][kol].values()])
                    if kol not in (KAHIN, BABEL, EGIM0) else None)
            print(f"    {AD[kol]:<10} {f3(ort(d))} ± {f3(ss(d))} · en düşük "
                  f"{min(d.values()):.3f}{ek} · p99 {f3(p99)} s"
                  + (f" · döngü dönüşü/koşu {dong:.0f}" if dong is not None
                     else ""))
            print("               " + " · ".join(
                f"{t} {f3(d.get(t))}" for t in tohumlar))


def fark_bolumu(kayit, baslik, a_k, b_k) -> dict:
    print(f"\n== {baslik}: {AD[a_k]} − {AD[b_k]}, eşli (eşik {ESIK}) ==")
    sonuc = {}
    for h in HUCRE:
        e = esli(dizi(kayit, h, a_k, lambda r: olcu(h, r)),
                 dizi(kayit, h, b_k, lambda r: olcu(h, r)))
        sonuc[h] = ayris(e, ESIK)
        print(f"  {h:<9} {esli_metni(e)} → {sonuc[h]}")
    if a_k not in (KAHIN, BABEL, EGIM0) and b_k not in (KAHIN, BABEL, EGIM0):
        for h in HUCRE:
            da = ort([sayac(r, "rota.dongu") for r in kayit[h][a_k].values()])
            db = ort([sayac(r, "rota.dongu") for r in kayit[h][b_k].values()])
            if da is not None and db is not None:
                print(f"  {h:<9} döngü dönüşü/koşu {AD[a_k]} {da:.0f} ↔ "
                      f"{AD[b_k]} {db:.0f}")
    return sonuc


def kabul(kayit, kol) -> tuple[bool, list[str]]:
    """S3: `kol` eğim0 düzeyinde mi? K1–K6 (beklenti, kural 3)."""
    B, I = "birincil", "ikiz"
    sat = []

    def y(h, k):
        return dizi(kayit, h, k, lambda r: olcu(h, r))

    e1 = esli(y(B, kol), y(B, EGIM0))
    k1 = not ayris(e1, ESIK).endswith("(−)")
    sat.append(f"K1 B'de {AD[kol]} − eğim0 {e1[0]:+.3f} → "
               f"{ayris(e1, ESIK)} → {'tamam' if k1 else 'TUTMADI'}")
    e2a = esli(y(I, kol), y(I, EGIM0))
    e2b = esli(y(I, kol), y(I, C19))
    k2 = (not ayris(e2a, ESIK).endswith("(−)")
          and not ayris(e2b, ESIK).endswith("(−)"))
    sat.append(f"K2 İ'de − eğim0 {e2a[0]:+.3f} ({ayris(e2a, ESIK)}) · − 19 "
               f"Kasım {e2b[0]:+.3f} ({ayris(e2b, ESIK)}) → "
               f"{'tamam' if k2 else 'TUTMADI'}")
    m_k, m_e = min(y(B, kol).values()), min(y(B, EGIM0).values())
    k3 = m_k >= m_e - ESIK
    sat.append(f"K3 B'de en düşük tohum {m_k:.3f} ≥ eğim0 {m_e:.3f} − "
               f"{ESIK} → {'tamam' if k3 else 'TUTMADI'}")
    s_k = dizi(kayit, B, kol, lambda r: oran(donem(B, r, "sessiz")))
    s_e = dizi(kayit, B, EGIM0, lambda r: oran(donem(B, r, "sessiz")))
    e4 = esli(s_k, s_e)
    k4 = not ayris(e4, ESIK).endswith("(−)")
    sat.append(f"K4 B'de sessiz dönem − eğim0 {e4[0]:+.3f} → "
               f"{ayris(e4, ESIK)} → {'tamam' if k4 else 'TUTMADI'}")
    p_k = ort(dizi(kayit, B, kol, lambda r: r["gecikme_s"]["p99"]))
    p_b = ort(dizi(kayit, B, BABEL, lambda r: r["gecikme_s"]["p99"]))
    k5 = p_k <= p_b
    sat.append(f"K5 B'de p99 {p_k:.2f} s ≤ Babel {p_b:.2f} s → "
               f"{'tamam' if k5 else 'TUTMADI'}")
    d_k = ort([sayac(r, "rota.dongu") for r in kayit[B][kol].values()])
    d_c = ort([sayac(r, "rota.dongu") for r in kayit[B][C19].values()])
    k6 = d_k <= ESIK_DONGU * d_c
    sat.append(f"K6 B'de döngü dönüşü/koşu {d_k:.0f} ≤ %10 × 19 Kasım "
               f"({d_c:.0f}) = {ESIK_DONGU * d_c:.0f} → "
               f"{'tamam' if k6 else 'TUTMADI'}")
    return all((k1, k2, k3, k4, k5, k6)), sat


def s3(kayit) -> None:
    print("\n== 4 · S3 — eğim0 düzeyi (karar; K1–K6 hepsi) ==")
    gecen = []
    for kol in YENI:
        tamam, sat = kabul(kayit, kol)
        print(f"  {AD[kol]}: " + ("EĞİM0 DÜZEYİNDE" if tamam
                                  else "eğim0 düzeyinde değil"))
        for s in sat:
            print(f"    {s}")
        if tamam:
            gecen.append(kol)
    if not gecen:
        print("  → HİÇBİR KOL eğim0 düzeyine gelmedi: yol seçiminde "
              "uygulanabilirlik koşuluna dönüş konuşulur (yeniden tasarımın "
              "girdisi)")
    elif len(gecen) == 1:
        print(f"  → {AD[gecen[0]]} eğim0 düzeyinde: eğim bu kuralla kalır "
              f"(aday)")
    else:
        e = esli(dizi(kayit, "birincil", GS,
                      lambda r: olcu("birincil", r)),
                 dizi(kayit, "birincil", GERI,
                      lambda r: olcu("birincil", r)))
        sec = GS if ayris(e, ESIK).endswith("(+)") else GERI
        print(f"  → ikisi de eğim0 düzeyinde; B'de geri+sınır − geri "
              f"{e[0]:+.3f} ({ayris(e, ESIK)}) → {AD[sec]} kalır (aday)")


TANI = ("rota.dongu", "rota.dislama", "rota.bayat_bilgi", "rota.son_care",
        "rota.zorunlu_gecis", "rota.istege_bagli_gecis", "rota.veri_gecis",
        "rota.yol_yok", "rota.tavan_asimi", "rota.geri_yasagi",
        "rota.geri_bekletme", "rota.yukselme_kopma", "bag.vaz_tetik",
        "selam.ara_ilan", "bekletme.bekletilen", "bekletme.suresi_dolan")


def s4(kayit) -> None:
    print("\n== 5 · S4 — tanı (betimleyici; sayaçlar bütün koşu, ağ "
          "toplamı, koşu başına) ==")
    for h in HUCRE:
        print(f"  {HAD[h]}")
        for kol in (BABEL, EGIM0, C19, GERI, GS):
            rs = list(kayit[h][kol].values())
            if not rs:
                continue
            g = sh.gruplar(h, rs)
            kon = sum(r["sayaclar"]["kontrol_airtime_s"] for r in rs) / len(rs)
            top = sum(r["enerji_s"]["enerji_gonderim_s"] for r in rs) / len(rs)
            print(f"    {AD[kol]:<10} kayıp R {f3(g['R'])} · İ {f3(g['I'])} · "
                  f"K {f3(g['K'])} · T {f3(g['T'])} | kontrol payı "
                  f"{kon / top:.1%} · bütün gönderim {top:.0f} s")
        for kol in (C19, GERI, GS):
            rs = list(kayit[h][kol].values())
            if not rs:
                continue
            n = len(rs)
            parca = [f"{k.split('.', 1)[1]} "
                     f"{sum(sayac(r, k) for r in rs) / n:.1f}" for k in TANI]
            print(f"    {AD[kol]:<10} " + " · ".join(parca))
            bitti = sum(sayac(r, "rota.yol_yok_bitti") for r in rs)
            sure = sum(sayac(r, "rota.yol_yok_sure_ms") for r in rs)
            if bitti:
                print(f"               yol yok bölümünün ortalama süresi "
                      f"{sure / bitti / 1000.0:.2f} s")
            mal, atl = Counter(), Counter()
            for r in rs:
                z = r["kaydedici"]
                mal.update(z["maliyet"])
                atl.update({int(k): v for k, v in z["atlama"].items()})
            sonlu = {int(k): v for k, v in mal.items() if k.isdigit()}
            tm = sum(mal.values())
            if tm:
                ta = sum(atl.values())
                uzun = sum(v for k, v in atl.items() if k >= 12)
                print(f"               maliyet p50 {sh._yuzdelik(sonlu, 0.5)}"
                      f" · p99 {sh._yuzdelik(sonlu, 0.99)} · en çok "
                      f"{max(r['kaydedici']['en_maliyet_etx'] for r in rs):.1f}"
                      f" · ∞ {mal.get('inf', 0) / tm:.4f} | teslimde ≥ 12 "
                      f"atlama {uzun / ta:.4f} · en çok (kararlar) "
                      f"{max(r['kaydedici']['en_atlama'] for r in rs)}")
        if h == "birincil":
            print("    tohum başına döngü dönüşü (B):")
            for kol in (C19, GERI, GS):
                rs = kayit[h][kol]
                if rs:
                    print(f"      {AD[kol]:<10} " + " · ".join(
                        f"{t} {sayac(r, 'rota.dongu'):.0f}"
                        for t, r in sorted(rs.items())))


def kahin(kayit) -> None:
    print(f"\n== 6 · KÂHİN — tohum başına aşım (kol − kâhin > R = "
          f"{sh.COZUNURLUK}) ==")
    for h in HUCRE:
        k = dizi(kayit, h, KAHIN, lambda r: olcu(h, r))
        for kol in (BABEL, EGIM0, C19, GERI, GS):
            e = esli(dizi(kayit, h, kol, lambda r: olcu(h, r)), k)
            if e[0] is None:
                continue
            asan = {t: v for t, v in e[4].items() if v > sh.COZUNURLUK}
            print(f"  {h:<9} {AD[kol]:<10} ortalama fark {e[0]:+.3f} · "
                  f"aşan tohum {len(asan)}/{e[3]}")


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
    tablolar(kayit, tohumlar)
    fark_bolumu(kayit, "2 · S1 — geri gönderme yasağı", GERI, C19)
    fark_bolumu(kayit, "3 · S2 — sınırlı yükselme", GS, GERI)
    if not duman:
        s3(kayit)
    s4(kayit)
    if not duman:
        kahin(kayit)


if __name__ == "__main__":
    main()
