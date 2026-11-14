"""Faz 5-2 · beklentinin karar kuralını `kayit_*.json`a uygular (simülasyon yok).

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz5_2_anatomi_2026-11-14/sonuc_hesap.py [dizin]

`dizin` verilirse kayıtlar oradan okunur (duman koşusunun denemesi için);
verilmezse bu dosyanın dizininden.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

D = Path(__file__).resolve().parent
KOK = D.parents[2]
KAYIT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else D
KOLLAR = ("desparete", "babel", "en_guvenilir_kahin")
EVRELER = ("once", "acik", "sessiz")
GRUP = {"rota_gecersiz": "R", "hedef_yok": "R", "tampon_asimi": "R",
        "iletim_basarisiz": "I", "kuyruk_tasmasi": "K", "ttl": "T"}
SAYACLAR = {
    "desparete": ("alan.onarima_girdi", "alan.ulasilamaz",
                  "alan.tur_artirildi", "alan.ardil_degisti",
                  "komsu.gecis_expired", "komsu.gecis_suspect",
                  "protokol.tampon_kota_disi", "protokol.veri_bekletilen",
                  "protokol.istek_gonderilen", "protokol.istek_aclik"),
    "babel": ("secim_degisti", "geri_cekme", "sira_istegi_uretilen",
              "uygulanamaz_alinan", "uygulanamaz_yoksayilan",
              "sira_artirildi", "komsu_silindi"),
}


def oku(ad):
    yol = KAYIT / f"kayit_{ad}.json"
    if not yol.exists():
        return None
    sonuc = json.loads(yol.read_text(encoding="utf-8"))["sonuc"]
    return {p: sorted((r for r in sonuc if r["protokol"] == p),
                      key=lambda r: r["tohum"]) for p in KOLLAR}


def oranlar(rs, evreler):
    """Pencerede doğan paketlerin akıbeti, doğana oran (havuzlanmış)."""
    dogan = sum(r["karistirici_evresi"][e]["dogan"] for r in rs
                for e in evreler)
    teslim = sum(r["karistirici_evresi"][e]["teslim"] for r in rs
                 for e in evreler)
    sebep = Counter()
    for r in rs:
        for k, v in r["dogum_evre_dusen"].items():
            s, e, _alan = k.split("|")
            if e in evreler:
                sebep[s] += v
    if not dogan:
        return None
    o = {s: v / dogan for s, v in sebep.items()}
    o["teslim"] = teslim / dogan
    o["kalan"] = (dogan - teslim - sum(sebep.values())) / dogan
    o["_dogan"] = dogan
    return o


def gruplar(o):
    g = Counter()
    for s, v in o.items():
        if s in GRUP:
            g[GRUP[s]] += v
    return g


def gecerlilik(ad, kol):
    print(f"== 0 · GEÇERLİLİK — {ad} ==")
    for p, rs in kol.items():
        for r in rs:
            satir = (f"  {p:<20} {r['tohum']} korunum {r['gecerli']} · "
                     f"çelişki {r['dogum_celiski']} · atfsız "
                     f"{r['dogum_atfsiz'] or 0}")
            a = r["karistirici_evresi"]["acik"]["pdr"]
            b = r.get("pdr_acik_satir")
            if a is not None and b is not None:
                satir += (f" · açık PDR {a:.4f} satır {b:.4f} "
                          f"{'birebir' if abs(a - b) < 1e-12 else 'UYUŞMUYOR'}")
            print(satir)


def g2c_denetimi(kol):
    yol = KOK / "arsiv/teshis/rakipler_k244_2026-10-14/G2c.txt"
    g2c = {}
    for m in re.finditer(r"KAYIT (\[.*\])", yol.read_text(encoding="utf-8")):
        for r in json.loads(m.group(1)):
            if r["senaryo"] == "formasyon-surekli" and not r.get("hayalet"):
                g2c[(r["protokol"], r["tohum"])] = r["pdr_acik"]
    print("  K-244 G2ç ile (1003 · 1004):")
    for p, rs in kol.items():
        for r in rs:
            if (p, r["tohum"]) in g2c and r.get("pdr_acik_satir") is not None:
                x, y = r["pdr_acik_satir"], g2c[(p, r["tohum"])]
                print(f"    {p:<20} {r['tohum']} {x:.6f} ↔ {y:.6f} "
                      f"{'birebir' if abs(x - y) < 1e-12 else 'FARKLI'}")


def acik_tablosu(baslik, kol, evreler):
    """G = PDR(Babel) − PDR(DESPARETE) ve grup payları."""
    print(f"\n== {baslik} ==")
    O = {p: oranlar(rs, evreler) for p, rs in kol.items() if rs}
    for p, o in O.items():
        if o is None:
            continue
        g = gruplar(o)
        print(f"  {p:<20} PDR {o['teslim']:.4f} · " + " · ".join(
            f"{k} {g[k]:.4f}" for k in "RIKT")
            + f" · kalan {o['kalan']:.4f} · doğan {o['_dogan']}")
        print("      sebepler: " + " · ".join(
            f"{s} {v:.4f}" for s, v in sorted(o.items(), key=lambda x: -x[1])
            if s in GRUP))
    d, b = O.get("desparete"), O.get("babel")
    if not d or not b:
        return
    G = b["teslim"] - d["teslim"]
    gd, gb = gruplar(d), gruplar(b)
    E = {k: gd[k] - gb[k] for k in "RIKT"}
    pozitif = sum(max(v, 0.0) for v in E.values()) or float("nan")
    print(f"  G = PDR(Babel) − PDR(DESPARETE) = {G:+.4f}")
    print("  E_g ve pay: " + " · ".join(
        f"{k} {E[k]:+.4f} (pay {max(E[k], 0) / pozitif:.0%})" for k in "RIKT")
        + f" · kalan farkı {d['kalan'] - b['kalan']:+.4f}")
    k = O.get("en_guvenilir_kahin")
    if k:
        print(f"  kâhine oran: DESPARETE {d['teslim'] / k['teslim']:.3f} · "
              f"Babel {b['teslim'] / k['teslim']:.3f}")
    print("  tohum başına PDR ve G:")
    for rd, rb in zip(kol["desparete"], kol["babel"]):
        od, ob = oranlar([rd], evreler), oranlar([rb], evreler)
        if od and ob:
            ed = {x: gruplar(od)[x] - gruplar(ob)[x] for x in "RI"}
            print(f"    {rd['tohum']}: D {od['teslim']:.4f} · B "
                  f"{ob['teslim']:.4f} · G {ob['teslim'] - od['teslim']:+.4f}"
                  f" (R {ed['R']:+.4f} · İ {ed['I']:+.4f})")


def ozgu_kayip(kol):
    print("\n== Birincil · karıştırmaya özgü kayıp Δ = açık − önce ==")
    D_ = {}
    for p, rs in kol.items():
        a, o = oranlar(rs, ("acik",)), oranlar(rs, ("once",))
        if not a or not o:
            continue
        ga, go = gruplar(a), gruplar(o)
        D_[p] = a["teslim"] - o["teslim"]
        print(f"  {p:<20} Δ {D_[p]:+.4f} (önce {o['teslim']:.4f} → açık "
              f"{a['teslim']:.4f}) · " + " · ".join(
                  f"{k} {ga[k] - go[k]:+.4f}" for k in "RIKT"))
        s = oranlar(rs, ("sessiz",))
        if s:
            print(f"      sessiz evre PDR {s['teslim']:.4f}")
    if "desparete" in D_ and "babel" in D_:
        f = D_["desparete"] - D_["babel"]
        print(f"  Δ(DESPARETE) − Δ(Babel) = {f:+.4f} → "
              + ("4 tohumda ayırt edilemedi (|fark| < 0,03)"
                 if abs(f) < 0.03 else "fark ≥ 0,03"))
        for rd, rb in zip(kol["desparete"], kol["babel"]):
            x = [oranlar([r], (e,)) for r in (rd, rb) for e in ("acik", "once")]
            if all(x):
                print(f"    {rd['tohum']}: Δ(D) "
                      f"{x[0]['teslim'] - x[1]['teslim']:+.4f} · Δ(B) "
                      f"{x[2]['teslim'] - x[3]['teslim']:+.4f}")


def baglar(ad, kol):
    print(f"\n== Bağ seçimi — {ad} ==")
    for p, rs in kol.items():
        if not rs:
            continue
        for anahtar, ad2 in (("karar_bant", "karar"),
                             ("karar_bant_tek", "karar (tek deneme)"),
                             ("basarisiz_bant", "başarısız")):
            c = Counter()
            for r in rs:
                c.update(r.get(anahtar) or {})
            t = sum(c.values())
            if t:
                print(f"  {p:<20} {ad2:<19} iyi {c['iyi'] / t:.1%} · orta "
                      f"{c['orta'] / t:.1%} · kötü {c['kotu'] / t:.1%} "
                      f"(n {t})")
        print(f"  {p:<20} karar mesafesi km, tohum başına: " + " | ".join(
            f"{r['tohum']}: {r['karar_mesafe_km']}" for r in rs))
        print(f"  {p:<20} başarısız mesafe km: " + " | ".join(
            f"{r['tohum']}: {r['basarisiz_mesafe_km']}" for r in rs))


def onarim(ad, kol):
    rs = kol.get("desparete") or []
    if not any(r.get("desparete_onarim") for r in rs):
        return
    print(f"\n== DESPARETE onarım bölümleri — {ad} ==")
    sayim, durum = Counter(), Counter()
    for r in rs:
        o = r["desparete_onarim"]
        sayim.update(o["sayim"])
        durum.update(o["rota_gecersiz_durum"])
        print(f"  {r['tohum']}: bölüm {sum(o['sayim'].values())} · süre "
              f"(evre|son: p50/p90/toplam) " + " · ".join(
                  f"{k} {v[0]}/{v[1]}/{v[2]}"
                  for k, v in sorted(o["sure"].items())))
    for e in EVRELER:
        alt = {k: v for k, v in sayim.items() if k.startswith(e + "|")}
        t = sum(alt.values())
        if not t:
            continue
        giris, son = Counter(), Counter()
        for k, v in alt.items():
            _e, g, s = k.split("|")
            giris[g] += v
            son[s] += v
        print(f"  evre {e}: bölüm {t} · giriş " + " · ".join(
            f"{g} {v / t:.0%}" for g, v in giris.most_common())
            + " · son " + " · ".join(
                f"{s} {v / t:.0%}" for s, v in son.most_common()))
        dalt = {k: v for k, v in durum.items() if k.startswith(e + "|")}
        dt = sum(dalt.values())
        if dt:
            print(f"      rota_gecersiz anında alan: " + " · ".join(
                f"{k.split('|')[1]} {v / dt:.0%}" for k, v in
                sorted(dalt.items(), key=lambda x: -x[1])) + f" (n {dt})")


def sayaclar(ad, kol):
    print(f"\n== Sayaçlar (ağ toplamı, tohum başına) — {ad} ==")
    for p, adlar in SAYACLAR.items():
        for r in kol.get(p) or []:
            t = r.get("teshis_toplam") or {}
            print(f"  {p:<10} {r['tohum']}: " + " · ".join(
                f"{a} {t.get(a, 0):.0f}" for a in adlar))


def main():
    ikiz, birincil = oku("ikiz"), oku("birincil")
    if ikiz:
        gecerlilik("ikiz", ikiz)
        acik_tablosu("İkiz · bütün pencere", ikiz, EVRELER)
        baglar("ikiz", ikiz)
        onarim("ikiz", ikiz)
        sayaclar("ikiz", ikiz)
    if birincil:
        print()
        gecerlilik("birincil", birincil)
        g2c_denetimi(birincil)
        acik_tablosu("Birincil · açık evre", birincil, ("acik",))
        acik_tablosu("Birincil · önce evresi (karıştırıcı açılmadan)",
                     birincil, ("once",))
        ozgu_kayip(birincil)
        baglar("birincil", birincil)
        onarim("birincil", birincil)
        sayaclar("birincil", birincil)
    if not ikiz and not birincil:
        print("kayıt yok")


if __name__ == "__main__":
    main()
