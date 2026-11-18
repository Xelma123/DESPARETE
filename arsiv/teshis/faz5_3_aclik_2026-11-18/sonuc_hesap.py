"""Faz 5-3 · açlık teşhisi · karar kuralının hesabı (`beklenti.md`; koşudan
ÖNCE yazıldı).

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz5_3_aclik_2026-11-18/sonuc_hesap.py [kayıt dizini]

Argümansız: bu dizinin `kayit_*.json` dosyaları (satırlar `kol`a göre);
çekirdek kolu ilk ölçümün kaydıyla (`../faz5_3_cekirdek_2026-11-18/
kayit_cekirdek_ikiz.json`) karşılaştırılır. Kayıt dizini verilirse (duman)
kısa pencere satırları ilk ölçümün duman kaydıyla karşılaştırılır.
"""
from __future__ import annotations

import json
import statistics as ist
import sys
from collections import Counter
from pathlib import Path

D = Path(__file__).resolve().parent
ILK = D.parent / "faz5_3_cekirdek_2026-11-18"
R_GRUBU = ("rota_gecersiz", "hedef_yok", "tampon_asimi")
ESIK_PDR = 0.02
EN_AZ_YON = 6
IYI = 0.90                       # kâhin bandı (`kayip_anatomisi._bant`)

dizin = Path(sys.argv[1]) if len(sys.argv) > 1 else D
duman = len(sys.argv) > 1


def oku(yol: Path) -> list[dict]:
    if not yol.exists():
        return []
    return json.loads(yol.read_text(encoding="utf-8"))["sonuc"]


def ort(x):
    x = list(x)
    return ist.mean(x) if x else float("nan")


def medyan(x):
    x = list(x)
    return ist.median(x) if x else float("nan")


def yuzde(x, q):
    x = sorted(x)
    return x[int(q * (len(x) - 1))] if x else float("nan")


def pay(a, b):
    return a / b if b else float("nan")


def ayrisma(farklar: list[float], esik: float) -> str:
    m = ort(farklar)
    arti = sum(1 for f in farklar if f > 0)
    eksi = sum(1 for f in farklar if f < 0)
    yon = max(arti, eksi)
    karar = ("ayrışıyor" if abs(m) >= esik and yon >= EN_AZ_YON
             else "ayırt edilemedi")
    return f"{m:+.3f} ({arti} artı · {eksi} eksi) → {karar}"


def rgrubu(r) -> tuple[int, int]:
    dogan = r["ikincil"]["pencere"]["dogan"]
    n = sum(v for k, v in r["dogum_evre_dusen"].items()
            if k.split("|")[0] in R_GRUBU)
    return n, dogan


def igrubu(r) -> float:
    dogan = r["ikincil"]["pencere"]["dogan"]
    n = sum(v for k, v in r["dogum_evre_dusen"].items()
            if k.split("|")[0] == "iletim_basarisiz")
    return n / dogan


# --------------------------------------------------------------------------
# Bir koşunun ölçüleri
# --------------------------------------------------------------------------
def kok(bolum: list[dict], b: dict) -> dict:
    gorulen = set()
    while b["ust"] is not None and b["id"] not in gorulen:
        gorulen.add(b["id"])
        b = bolum[b["ust"]]
    return b


def kosu_olculeri(r: dict) -> dict:
    a = r["aclik"]
    bas, bit = a["pencere"]
    deneme = a["deneme"]
    bolum = a["bolum"]
    pencerede = [b for b in bolum if bas <= b["t"] < bit]
    # Bağ çıkışını bölümün köküne bağla: (düğüm, eski ardıl, aynı an)
    cikis_ani: dict[tuple[int, int], list] = {}
    for c in a["cikis"]:
        cikis_ani.setdefault((c[0], c[1]), []).append(c)

    def kok_cikisi(b: dict):
        aday = [c for c in cikis_ani.get((b["dugum"], b["eski"]), ())
                if c[2] <= b["t"] + 1e-9]
        return aday[-1] if aday else None

    def p_atlama(c) -> float:
        return 1.0 - (1.0 - c[8]) ** deneme

    def bag_kokenli(k: dict) -> bool:
        return k["sebep"].startswith("bag:")

    def yanlis_alarm(k: dict) -> bool | None:
        if not bag_kokenli(k):
            return None
        c = kok_cikisi(k)
        return None if c is None else p_atlama(c) >= IYI

    def tur_yardim(k: dict) -> bool:
        s = k["sayim"]
        return s.get("olagan_eski_tur", 0) + s.get("olagan_pahali", 0) > 0

    def yedek_bag(k: dict) -> bool:
        return k["sayim"].get("kotu_uygulanabilir", 0) > 0

    # Kayıp ağırlığı: penceredeki doğumlu, bölümde düşen telemetri paketleri
    dusen: list[tuple[dict, dict]] = []        # (bölüm, kök)
    for b in bolum:
        n = sum(1 for d in b["dusen"] if bas <= d < bit)
        k = kok(bolum, b)
        dusen.extend([(b, k)] * n)
    nd = len(dusen)
    bolumsuz = sum(1 for _, _, d in a["bolumsuz"] if bas <= d < bit)
    r_n, dogan = rgrubu(r)

    def agirlikli(f) -> float:
        return pay(sum(1 for b, k in dusen if f(b, k)), nd)

    kokler = [b for b in pencerede if b["ust"] is None]
    sure = [b["t_son"] - b["t"] for b in pencerede if b["t_son"] is not None]
    kapali = [b for b in pencerede if b["t_son"] is not None]
    # bağ çıkışları (pencerede başlayan)
    cik = [c for c in a["cikis"] if bas <= c[2] < bit]
    # tur yayılımı
    gt = [(t, tur) for t, tur in a["gecit_tur"] if bas <= t < bit]
    rota_tur = {int(d): v for d, v in a["rota_tur"].items()}
    tum_gt = a["gecit_tur"]
    yetisen, gecikme = [], []
    for i, (t, tur) in enumerate(tum_gt):
        if not bas <= t < bit:
            continue
        sonraki = tum_gt[i + 1][0] if i + 1 < len(tum_gt) else bit
        n_ulasan = 0
        for d, seri in rota_tur.items():
            if d == a["gecit"]:
                continue
            ilk = next((ts for ts, tr in seri if ts >= t and tr >= tur),
                       None)
            if ilk is not None:
                gecikme.append(ilk - t)
                if ilk < sonraki:
                    n_ulasan += 1
        yetisen.append(n_ulasan / max(1, len(rota_tur)
                                      - (a["gecit"] in rota_tur)))
    return {
        "tohum": r["tohum"], "pdr": r["pdr_pencere"],
        "r": r_n / dogan, "i": igrubu(r),
        "bolum": len(pencerede), "kok": len(kokler),
        "zincir_pay": pay(len(pencerede) - len(kokler), len(pencerede)),
        "dusen": nd, "bolumsuz": bolumsuz, "r_n": r_n,
        "kapsama": pay(nd + bolumsuz, r_n),
        # karar ölçüleri (kayıp ağırlıklı, köke göre)
        "M1": agirlikli(lambda b, k: bag_kokenli(k)),
        "M2": pay(sum(1 for b, k in dusen if yanlis_alarm(k)),
                  sum(1 for b, k in dusen if yanlis_alarm(k) is not None)),
        "M3": agirlikli(lambda b, k: tur_yardim(k)),
        "M3_eski_tur": agirlikli(
            lambda b, k: k["sayim"].get("olagan_eski_tur", 0) > 0),
        "M3b": agirlikli(lambda b, k: yedek_bag(k)),
        "M4": agirlikli(lambda b, k: b["ust"] is not None),
        "kok_sebep_agirlikli": Counter(k["sebep"] for b, k in dusen),
        "kok_sebep_sayi": Counter(b["sebep"] for b in kokler),
        "bolum_sebep_sayi": Counter(b["sebep"] for b in pencerede),
        "kok_cikis_bant": Counter(
            ("iyi" if p_atlama(c) >= IYI else
             "orta" if p_atlama(c) >= 0.5 else "kotu")
            for b in kokler if bag_kokenli(b)
            for c in [kok_cikisi(b)] if c is not None),
        # süre ve son
        "sure_medyan": medyan(sure), "sure_p90": yuzde(sure, 0.9),
        "sure_ort": ort(sure),
        "uzun_pay": pay(sum(1 for s in sure if s >= 2.0), len(sure)),
        "uzunda_dusen": agirlikli(
            lambda b, k: b["t_son"] is None or b["t_son"] - b["t"] >= 2.0),
        "acik_kalan": len(pencerede) - len(kapali),
        "ayni_komsu": pay(sum(1 for b in kapali if b["ayni_komsu"]),
                          len(kapali)),
        "yeni_tur": pay(sum(1 for b in kapali if b["yeni_tur"]),
                        sum(1 for b in kapali if b["yeni_tur"] is not None)),
        "istek": pay(sum(1 for b in pencerede if b["istek"]),
                     len(pencerede)),
        # bağ çıkışları
        "cikis": len(cik),
        "cikis_sebep": Counter(c[3] for c in cik),
        "cikis_ardil_sebep": Counter(c[3] for c in cik if c[6]),
        "cikis_ardil_iyi": pay(sum(1 for c in cik if c[6]
                                   and p_atlama(c) >= IYI),
                               sum(1 for c in cik if c[6])),
        "cikis_iyi_sebep": {
            s: pay(sum(1 for c in cik if c[3] == s and p_atlama(c) >= IYI),
                   sum(1 for c in cik if c[3] == s))
            for s in sorted({c[3] for c in cik})},
        "kotu_kalis_medyan": {
            s: medyan(c[7] - c[2] for c in cik
                      if c[3] == s and c[7] is not None)
            for s in sorted({c[3] for c in cik})},
        # tur yayılımı
        "tur_artisi": len(gt),
        "tur_ara_medyan": medyan(b[0] - a_[0] for a_, b in zip(gt, gt[1:])),
        "tur_yetisen": medyan(yetisen),
        "tur_gecikme_medyan": medyan(gecikme),
        "teshis": r["teshis_toplam"],
    }


# --------------------------------------------------------------------------
print("=" * 78)
print(f"AÇLIK TEŞHİSİ · karar kuralı · {dizin}")
print("=" * 78)
hepsi = [r for yol in sorted(dizin.glob("kayit_*.json")) for r in oku(yol)]
cek = [r for r in hepsi if r["kol"] == "cekirdek"]
vtk = [r for r in hepsi if r["kol"] == "vtk0"]
if duman:
    ilk = [r for r in oku(ILK / "duman" / "kayit_cekirdek_ikiz.json")
           if r["protokol"] == "desparete5_cekirdek"]
else:
    ilk = oku(ILK / "kayit_cekirdek_ikiz.json")
ilk = {r["tohum"]: r for r in ilk}

# --- 0 · geçerlilik ------------------------------------------------------
print("\n0 · GEÇERLİLİK")
beklenen = 1 if duman else 8
gecerli = True
for ad, rs in (("çekirdek", cek), ("vtk0", vtk)):
    tamam = (len(rs) == beklenen and all(
        r["gecerli"] and r["dogum_celiski"] == 0 and not r["dogum_atfsiz"]
        and not r["aclik_denetim"] and r["aclik"]["acik_kalan"] >= 0
        for r in rs))
    gecerli &= tamam
    print(f"  {ad}: {len(rs)} koşu · korunum, doğum, iç denetimler "
          f"{'tamam' if tamam else 'TUTMADI'}")
    for r in rs:
        if r["aclik_denetim"]:
            print(f"    {r['tohum']}: {r['aclik_denetim']}")
for r in vtk:
    b = dict(zip(r["aclik"]["bayrak_adlari"], r["aclik"]["bayraklar"]))
    if b.get("veri_kotu_tetigi") or r["teshis_toplam"].get("bag.veri_kotu"):
        gecerli = False
        print(f"  vtk0 {r['tohum']}: veri tetiği AÇIK görünüyor")
ayni = 0
for r in cek:
    o = ilk.get(r["tohum"])
    esit = o is not None and all(
        r[a] == o[a] for a in ("pdr", "pdr_pencere", "uretilen", "teslim",
                               "teshis_toplam", "dogum_evre_dusen"))
    ayni += esit
    if not esit:
        print(f"  çekirdek {r['tohum']}: ilk ölçümle AYNI DEĞİL "
              f"({r['pdr_pencere']} ↔ {o and o['pdr_pencere']})")
gecerli &= ayni == len(cek) == beklenen
print(f"  çekirdek kolu ilk ölçümle birebir: {ayni}/{len(cek)} "
      f"({'duman kaydı' if duman else 'kayit_cekirdek_ikiz.json'})")
print(f"  → {'GEÇERLİ' if gecerli else 'GEÇERSİZ: önce sebebi aranır'}")

if not cek:
    sys.exit(0)
O = [kosu_olculeri(r) for r in sorted(cek, key=lambda r: r["tohum"])]
V = [kosu_olculeri(r) for r in sorted(vtk, key=lambda r: r["tohum"])]


def satir(ad: str, anahtar: str, bicim: str = ".3f", olcu=None) -> None:
    olcu = O if olcu is None else olcu
    deger = [o[anahtar] for o in olcu]
    print(f"  {ad:<46} {ort(deger):{bicim}} · tohum "
          + " ".join(f"{v:{bicim}}" for v in deger))


def sayac_ort(anahtar: str, olcu=None) -> dict:
    olcu = O if olcu is None else olcu
    top: Counter = Counter()
    for o in olcu:
        top.update(o[anahtar])
    n = sum(top.values())
    return {k: f"{v / len(olcu):.1f} ({v / n:.0%})"
            for k, v in top.most_common()}


# --- 1 · açlık nereden başlıyor (karar) -----------------------------------
print("\n1 · AÇLIĞIN KÖKÜ (çekirdek; penceredeki doğumlu, bölümde düşen "
      "telemetri paketleriyle ağırlıklı)")
satir("düşen paket / koşu", "dusen", ".0f")
satir("kapsama (bölümde + bölümsüz) / R grubu", "kapsama")
satir("M1 bağ kökenli (kök sebep bag:*)", "M1")
satir("M2 yanlış alarm (bağ kökenlide kâhin ≥ 0,90)", "M2")
satir("M3 kökte OLAĞAN ama uygulanamaz komşu", "M3")
satir("   bunun eski turlu olanı", "M3_eski_tur")
satir("M3b kökte dışlanmış ama uygulanabilir komşu", "M3b")
satir("M4 zincir (yukarının ∞'undan) bölümde düşen", "M4")
print(f"  kök sebep (kayıp ağırlıklı, koşu başına): "
      f"{sayac_ort('kok_sebep_agirlikli')}")
m1, m2 = ort(o["M1"] for o in O), ort(o["M2"] for o in O)
m4 = ort(o["M4"] for o in O)
if m1 >= 0.5 and m2 >= 0.5:
    hukum = ("BAĞ KÖKENLİ, YANLIŞ ALARM: bağ çıkış kuralları iyi bağları "
             "düşürüyor → bağ çıkışı seçenekleri (T-2, T-3, Y-12)")
elif m1 >= 0.5:
    hukum = ("BAĞ KÖKENLİ, BAĞ GERÇEKTEN BOZULUYOR: açık yedeğin "
             "yokluğunda → yedek rota seçenekleri (T-12, T-13, tur yayılımı; "
             "kötü bağla sürdürme)")
else:
    enb = Counter()
    for o in O:
        enb.update({k: v for k, v in o["kok_sebep_agirlikli"].items()
                    if not k.startswith("bag:")})
    hukum = (f"BAĞ KÖKENLİ DEĞİL: en büyük kök sebep "
             f"{enb.most_common(1)[0][0] if enb else '—'} → onun seçenekleri")
print(f"  HÜKÜM: {hukum}")
if m4 >= 0.5:
    print("  ZİNCİR: kaybın çoğu yukarıdakinin ∞'undan gelen bölümlerde → "
          "∞'un yayılması seçenek listesine girer")

# --- 2 · bölümler (betimleyici) -------------------------------------------
print("\n2 · BÖLÜMLER (betimleyici)")
satir("pencere PDR", "pdr")
satir("R grubu kaybı", "r")
satir("bölüm / koşu", "bolum", ".0f")
satir("kök bölüm / koşu", "kok", ".0f")
satir("zincir bölüm payı (sayı)", "zincir_pay")
satir("süre medyanı (s)", "sure_medyan", ".2f")
satir("süre p90 (s)", "sure_p90", ".2f")
satir("süre ortalaması (s)", "sure_ort", ".2f")
satir("≥ 2 s süren bölüm payı", "uzun_pay")
satir("≥ 2 s süren bölümlerde düşen payı", "uzunda_dusen")
satir("eski ardılla biten pay", "ayni_komsu")
satir("yeni turla biten pay", "yeni_tur")
satir("istek dizisi başlayan pay", "istek")
print(f"  bölüm sebebi (sayı, koşu başına): {sayac_ort('bolum_sebep_sayi')}")
print(f"  kök sebebi (sayı, koşu başına): {sayac_ort('kok_sebep_sayi')}")
print(f"  bağ kökenli köklerde ardıl bağının kâhin bandı: "
      f"{sayac_ort('kok_cikis_bant')}")

# --- 3 · bağ çıkışları (betimleyici) --------------------------------------
print("\n3 · BAĞ ÇIKIŞLARI (OLAĞAN'dan; betimleyici)")
satir("çıkış / koşu", "cikis", ".0f")
print(f"  sebep: {sayac_ort('cikis_sebep')}")
print(f"  ardıl bağında sebep: {sayac_ort('cikis_ardil_sebep')}")
satir("ardıl bağı çıkışında kâhin ≥ 0,90 payı", "cikis_ardil_iyi")
for s in sorted({s for o in O for s in o["cikis_iyi_sebep"]}):
    print(f"  {s:<11} kâhin ≥ 0,90 payı "
          f"{ort(o['cikis_iyi_sebep'].get(s, float('nan')) for o in O):.3f}"
          f" · KÖTÜ'de kalış medyanı "
          f"{ort(o['kotu_kalis_medyan'].get(s, float('nan')) for o in O):.1f} s")

# --- 4 · tur yayılımı (betimleyici) ---------------------------------------
print("\n4 · TUR YAYILIMI (betimleyici)")
satir("geçidin tur artışı (pencerede)", "tur_artisi", ".0f")
satir("artışlar arası medyan (s)", "tur_ara_medyan", ".2f")
satir("sonraki artıştan önce yetişen düğüm payı", "tur_yetisen")
satir("yetişme gecikmesi medyanı (s)", "tur_gecikme_medyan", ".2f")

# --- 5 · veri tetiği kapalı kol (karar) -----------------------------------
print("\n5 · VERİ TETİĞİ KAPALI KOL (vtk0)")
if V:
    ortak = sorted({o["tohum"] for o in O} & {v["tohum"] for v in V})
    oo = {o["tohum"]: o for o in O}
    vv = {v["tohum"]: v for v in V}
    satir("pencere PDR (vtk0)", "pdr", olcu=V)
    satir("R grubu kaybı (vtk0)", "r", olcu=V)
    satir("İ grubu kaybı (vtk0)", "i", olcu=V)
    satir("İ grubu kaybı (çekirdek)", "i")
    satir("bölüm / koşu (vtk0)", "bolum", ".0f", olcu=V)
    satir("M1 (vtk0)", "M1", olcu=V)
    satir("M2 (vtk0)", "M2", olcu=V)
    print(f"  çıkış sebebi (vtk0): {sayac_ort('cikis_sebep', V)}")
    print(f"  PDR(vtk0) − PDR(çekirdek): "
          f"{ayrisma([vv[t]['pdr'] - oo[t]['pdr'] for t in ortak], ESIK_PDR)}")
    print(f"  bölüm sayısı oranı vtk0 / çekirdek: "
          f"{ort(vv[t]['bolum'] / oo[t]['bolum'] for t in ortak):.2f}")
