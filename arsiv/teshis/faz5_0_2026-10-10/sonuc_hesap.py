"""Faz 5.0 · beklentinin karar kuralını `kayit.json`a uygular (simülasyon yok).

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz5_0_2026-10-10/sonuc_hesap.py
"""
import json
import re
from collections import Counter
from pathlib import Path

D = Path(__file__).resolve().parent
KOK = D.parents[2]
KOLLAR = ("desparete", "aodv", "aomdv", "olsr", "en_guvenilir_kahin")
EVRELER = ("once", "acik", "sessiz")
GRUP = {"rota_gecersiz": "R", "hedef_yok": "R", "tampon_asimi": "R",
        "iletim_basarisiz": "I", "kuyruk_tasmasi": "K", "ttl": "T"}


def oranlar(rs, e):
    dogan = sum(r["karistirici_evresi"][e]["dogan"] for r in rs)
    teslim = sum(r["karistirici_evresi"][e]["teslim"] for r in rs)
    sebep = Counter()
    for r in rs:
        for k, v in r["dogum_evre_dusen"].items():
            s, ee, _a = k.split("|")
            if ee == e:
                sebep[s] += v
    o = {s: v / dogan for s, v in sebep.items()}
    o["teslim"] = teslim / dogan
    o["kalan"] = (dogan - teslim - sum(sebep.values())) / dogan
    return o


def fark(rs):
    a, o = oranlar(rs, "acik"), oranlar(rs, "once")
    return {k: a.get(k, 0.0) - o.get(k, 0.0) for k in set(a) | set(o)}


def gruplar(f):
    g = Counter()
    for s, v in f.items():
        if s in GRUP:
            g[GRUP[s]] += v
    return g


def main():
    sonuc = json.loads((D / "kayit.json").read_text(encoding="utf-8"))["sonuc"]
    kol = {p: sorted((r for r in sonuc if r["protokol"] == p),
                     key=lambda r: r["tohum"]) for p in KOLLAR}

    print("== 0 · GEÇERLİLİK ==")
    for p, rs in kol.items():
        for r in rs:
            a = r["karistirici_evresi"]["acik"]["pdr"]
            b = r["pdr_acik_satir"]
            print(f"  {p:<20} {r['tohum']} korunum {r['gecerli']} · çelişki "
                  f"{r['dogum_celiski']} · atfsız {r['dogum_atfsiz'] or 0} · "
                  f"açık PDR {a:.4f} satır {b:.4f} "
                  f"{'birebir' if abs(a - b) < 1e-12 else 'UYUŞMUYOR'}")
    g2c = {}
    metin = (KOK / "arsiv/teshis/denetim_duzeltme_2026-10-09/B3_G2c.txt"
             ).read_text(encoding="utf-8")
    for m in re.finditer(r"KAYIT (\[.*\])", metin):
        for r in json.loads(m.group(1)):
            if r["senaryo"] == "formasyon-surekli":
                g2c[(r["protokol"], r["tohum"])] = r["pdr_acik"]
    print("  G2ç ile (1003 · 1004):")
    for p, rs in kol.items():
        for r in rs:
            if (p, r["tohum"]) in g2c:
                x, y = r["pdr_acik_satir"], g2c[(p, r["tohum"])]
                print(f"    {p:<20} {r['tohum']} {x:.6f} ↔ {y:.6f} "
                      f"{'birebir' if abs(x - y) < 1e-12 else 'FARKLI'}")

    print("\n== PDR_açık tohum başına (önce · açık · sessiz) ==")
    for p, rs in kol.items():
        print(f"  {p:<20} " + " | ".join(
            f"{r['tohum']}: " + " ".join(
                f"{r['karistirici_evresi'][e]['pdr']:.3f}" for e in EVRELER)
            for r in rs))

    print("  ortalama PDR_açık (tohum ortalaması) · DESPARETE − kol, tohum başına:")
    ort = {p: sum(r["pdr_acik_satir"] for r in rs) / len(rs)
           for p, rs in kol.items()}
    for p, rs in kol.items():
        print(f"    {p:<20} {ort[p]:.3f}" + ("" if p == "desparete" else
              " · D − kol " + " ".join(
                  f"{d['pdr_acik_satir'] - r['pdr_acik_satir']:+.3f}"
                  for d, r in zip(kol["desparete"], rs))))

    print("\n== Karıştırmaya özgü kayıp (açık − önce), havuzlanmış ==")
    F = {p: fark(rs) for p, rs in kol.items()}
    for p in KOLLAR:
        g = gruplar(F[p])
        print(f"  {p:<20} ΔPDR {F[p]['teslim']:+.3f} · " + " · ".join(
            f"{k} {g[k]:+.3f}" for k in "RIKT")
            + f" · kalan {F[p]['kalan']:+.3f}")

    print("\n== Karar kuralı: DESPARETE − kâhin (E) ve DESPARETE − AODV ==")
    for r_ad in ("en_guvenilir_kahin", "aodv"):
        E = -(F["desparete"]["teslim"] - F[r_ad]["teslim"])
        gd, gr = gruplar(F["desparete"]), gruplar(F[r_ad])
        eg = {k: gd[k] - gr[k] for k in "RIKT"}
        pozitif = sum(max(v, 0.0) for v in eg.values())
        print(f"  − {r_ad:<18} E {E:+.3f} · " + " · ".join(
            f"{k} {eg[k]:+.3f} (pay {max(eg[k], 0) / pozitif:.0%})"
            for k in "RIKT"))

    print("\n  tohum başına (DESPARETE − kâhin; açık − önce):")
    for i, r in enumerate(kol["desparete"]):
        k = kol["en_guvenilir_kahin"][i]
        a = kol["aodv"][i]
        fd, fk, fa = fark([r]), fark([k]), fark([a])
        gd, gk, ga = gruplar(fd), gruplar(fk), gruplar(fa)
        print(f"    {r['tohum']}: E_kâhin {-(fd['teslim'] - fk['teslim']):+.3f}"
              f" (R {gd['R'] - gk['R']:+.3f} · İ {gd['I'] - gk['I']:+.3f}) · "
              f"E_AODV {-(fd['teslim'] - fa['teslim']):+.3f} "
              f"(R {gd['R'] - ga['R']:+.3f} · İ {gd['I'] - ga['I']:+.3f})")

    print("\n== Güvenlik: T ve DESPARETE'nin hop sınırı ==")
    for r in kol["desparete"]:
        t = r["teshis_toplam"]
        print(f"  {r['tohum']}: veri_hop_siniri "
              f"{t.get('protokol.veri_hop_siniri', 'yok')} · ttl düşen "
              f"{sum(v for k, v in r['tablo'].items() if k.startswith('ttl|'))}")

    print("\n== R'nin alt ayrımı (DESPARETE) ==")
    rg, bol = Counter(), Counter()
    for r in kol["desparete"]:
        o = r["desparete_onarim"]
        rg.update(o["rota_gecersiz_durum"])
        bol.update(o["sayim"])
    print("  rota_gecersiz anında alan (evre|durum):", dict(sorted(rg.items())))
    for e in ("acik", "sessiz"):
        rep, unr = rg.get(f"{e}|REPAIRING", 0), rg.get(f"{e}|UNREACHABLE", 0)
        if rep + unr:
            print(f"    {e}: REPAIRING (kota dolu) {rep / (rep + unr):.0%} · "
                  f"UNREACHABLE {unr / (rep + unr):.0%}")
    giris = Counter()
    for k, v in bol.items():
        e, g, son = k.split("|")
        giris[(e, g, "+U" in son)] += v
    print("  onarım bölümleri (evre, giriş, ulaşılamaz oldu mu):",
          {f"{e}|{g}|{'U' if u else '-'}": v
           for (e, g, u), v in sorted(giris.items())})

    print("\n== Karar payı, etki alanına göre (açık evre; ed · girişim · uzak) ==")
    for p in ("desparete", "aodv", "aomdv", "olsr", "en_guvenilir_kahin"):
        c = Counter()
        for r in kol[p]:
            c.update(r["evre_alan_karar"])
        for e in ("once", "acik"):
            top = sum(c[f"{e}|{b}"] for b in ("ed", "girisim", "uzak"))
            print(f"  {p:<20} {e:<6} " + " · ".join(
                f"{b} {c[f'{e}|{b}'] / top:.1%}"
                for b in ("ed", "girisim", "uzak")))

    print("\n== Açık evrede doğan, düşen × etki alanı (doğana oran) ==")
    for p in ("desparete", "aodv", "en_guvenilir_kahin"):
        dogan = sum(r["karistirici_evresi"]["acik"]["dogan"] for r in kol[p])
        c = Counter()
        for r in kol[p]:
            c.update(r["dogum_evre_dusen"])
        for s in ("rota_gecersiz", "iletim_basarisiz"):
            v = [c[f"{s}|acik|{b}"] for b in ("ed", "girisim", "uzak")]
            w = [c[f"{s}|once|{b}"] for b in ("ed", "girisim", "uzak")]
            od = sum(r["karistirici_evresi"]["once"]["dogan"] for r in kol[p])
            if sum(v) or sum(w):
                print(f"  {p:<20} {s:<17} açık " + " / ".join(
                    f"{x / dogan:.3f}" for x in v) + " · önce " + " / ".join(
                    f"{x / od:.3f}" for x in w))


if __name__ == "__main__":
    main()
