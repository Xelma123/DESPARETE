"""Faz 5-3 açlık teşhisi · ek sayılar (koşudan SONRA yazıldı; karar girdisi
değil). Veri tetiği kapalı kolun (vtk0) Babel ve kâhinle eşli farkı, kayıp
grupları, gecikme ve kontrol yükü; vtk0'da kalan açlıkların kökü. Babel ve
kâhin satırları teşhis (c)'nin kaydından (`kayit_ikiz.json`).

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz5_3_aclik_2026-11-18/ek_hesap.py
"""
import json
import statistics as ist
from collections import Counter
from pathlib import Path

D = Path(__file__).resolve().parent
C = D.parent / "faz5_2_rakip_cizgisi_2026-11-15"
TOHUM = list(range(1003, 1011))


def oku(yol, anahtar):
    return {r["tohum"]: r for r in json.loads(yol.read_text(
        encoding="utf-8"))["sonuc"] if anahtar(r)}


cek = oku(D / "kayit_cekirdek.json", lambda r: r["kol"] == "cekirdek")
vtk = oku(D / "kayit_vtk0.json", lambda r: r["kol"] == "vtk0")
bab = oku(C / "kayit_ikiz.json", lambda r: r["protokol"] == "babel")
kah = oku(C / "kayit_ikiz.json",
          lambda r: r["protokol"] == "en_guvenilir_kahin")
KOL = {"kâhin": kah, "Babel": bab, "çekirdek": cek, "vtk0": vtk}


def pdr(r):
    return r["pdr_pencere"]


def grup(r, sebepler):
    dogan = r["ikincil"]["pencere"]["dogan"]
    return sum(v for k, v in r["dogum_evre_dusen"].items()
               if k.split("|")[0] in sebepler) / dogan


def tavanli(r, s="5"):
    o = r["ikincil"]["pencere"]
    return o["teslim_tavan"][s] / o["dogan"]


print("== pencere PDR, tohum başına ==")
print("kol        ort    " + " ".join(f"{t:>6}" for t in TOHUM))
for ad, k in KOL.items():
    print(f"{ad:<9} {ist.mean(pdr(k[t]) for t in TOHUM):.3f}  "
          + " ".join(f"{pdr(k[t]):.3f}" for t in TOHUM))

print("\n== eşli farklar (eşik 0,02; ayrışma: ort ≥ eşik ve ≥ 6/8 aynı yön) ==")
for a, b in (("vtk0", "Babel"), ("vtk0", "kâhin"), ("vtk0", "çekirdek")):
    f = [pdr(KOL[a][t]) - pdr(KOL[b][t]) for t in TOHUM]
    arti = sum(x > 0 for x in f)
    eksi = sum(x < 0 for x in f)
    m = ist.mean(f)
    hk = ("ayrışıyor" if abs(m) >= 0.02 and max(arti, eksi) >= 6
          else "ayırt edilemedi")
    print(f"{a} − {b}: {m:+.3f} ({arti} artı · {eksi} eksi) → {hk} · "
          + " ".join(f"{x:+.3f}" for x in f))

print("\n== kayıp grupları, gecikme, kontrol yükü (8 tohum ortalaması) ==")
for ad, k in KOL.items():
    rs = [k[t] for t in TOHUM]
    kon = ist.mean(r["sayaclar"]["kontrol_airtime_s"] for r in rs)
    top = ist.mean(r["enerji_s"]["enerji_gonderim_s"] for r in rs)
    print(f"{ad:<9} R {ist.mean(grup(r, ('rota_gecersiz', 'hedef_yok', 'tampon_asimi')) for r in rs):.3f}"
          f" · İ {ist.mean(grup(r, ('iletim_basarisiz',)) for r in rs):.3f}"
          f" · K {ist.mean(grup(r, ('kuyruk_tasmasi',)) for r in rs):.3f}"
          f" · 5 s tavanın bedeli "
          f"{ist.mean(pdr(r) - tavanli(r) for r in rs):.3f}"
          f" · p50 {ist.mean(r['gecikme_s']['p50'] for r in rs):.2f}"
          f" · p99 {ist.mean(r['gecikme_s']['p99'] for r in rs):.2f} s"
          f" · kontrol {kon:.1f} s ({kon / top:.1%})")

print("\n== vtk0'da kalan açlıklar (pencerede başlayan) ==")
for t in TOHUM:
    a = vtk[t]["aclik"]
    bas, bit = a["pencere"]
    b = [x for x in a["bolum"] if bas <= x["t"] < bit]
    dusen = sum(1 for x in a["bolum"] for d in x["dusen"] if bas <= d < bit)
    print(f"{t}: bölüm {len(b)} · kök {sum(x['ust'] is None for x in b)} · "
          f"bölümde düşen {dusen} · sebep "
          f"{dict(Counter(x['sebep'] for x in b))}")

print("\n== çekirdekte veri tetiğinin çıkışları (pencerede) ==")
n = Counter()
for t in TOHUM:
    a = cek[t]["aclik"]
    bas, bit = a["pencere"]
    for c in a["cikis"]:
        if c[3] == "veri" and bas <= c[2] < bit:
            n["hepsi"] += 1
            n["ardil"] += c[6]
            n["dondu"] += c[7] is not None
print(f"koşu başına: çıkış {n['hepsi'] / 8:.0f} · ardıl bağında "
      f"{n['ardil'] / n['hepsi']:.1%} · OLAĞAN'a dönen {n['dondu'] / n['hepsi']:.1%}")

print("\n== bağ çıkışı anında selamın ölçtüğü ↔ kâhinin tek deneme başarısı "
      "(pencerede; tohum başına medyanların ortalaması) ==")
for ad, k in (("çekirdek", cek), ("vtk0", vtk)):
    for s in ("selam_asim", "selam_alim", "veri"):
        sel, kh = [], []
        for t in TOHUM:
            a = k[t]["aclik"]
            bas, bit = a["pencere"]
            cs = [c for c in a["cikis"] if c[3] == s and bas <= c[2] < bit]
            if cs:
                sel.append(ist.median((c[4] or 0) * (c[5] or 0) for c in cs))
                kh.append(ist.median(c[8] for c in cs))
        if sel:
            print(f"{ad:<9} {s:<11} d_f·d_r {ist.mean(sel):.2f} · kâhin p "
                  f"{ist.mean(kh):.2f}")

print("\n== vazgeçmelerin bağlara dağılımı (bütün koşu; `tablo`nun iletim_basarisiz"
      " satırları ve anatominin en çok vazgeçilen 5 bağı; 19 Kasım'da eklendi, "
      "`17` T-2'nin gerekçesi) ==")
for ad, k in (("çekirdek", cek), ("vtk0", vtk)):
    top, bag, en, pay = [], [], [], []
    for t in TOHUM:
        r = k[t]
        ib = sum(v for kk, v in r["tablo"].items()
                 if kk.startswith("iletim_basarisiz|"))
        b5 = r["basarisiz_en_cok_5_bag"]
        top.append(ib)
        bag.append(r["basarisiz_bag_sayisi"])
        en.append(b5[0][2])
        pay.append(sum(x[2] for x in b5) / ib)
    print(f"{ad:<9} vazgeçme/koşu {ist.mean(top):.0f} · ayrı bağ "
          f"{ist.mean(bag):.0f} · en kötü bağ {ist.mean(en):.0f} "
          f"({min(en)}–{max(en)}) · en kötü 5 bağın payı {ist.mean(pay):.2f} "
          f"({min(pay):.2f}–{max(pay):.2f})")
