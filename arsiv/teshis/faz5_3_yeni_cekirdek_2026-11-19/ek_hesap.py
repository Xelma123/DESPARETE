"""Faz 5-3 · yeni çekirdek — kuraldan sonra bakılan ek sayılar (karar girdisi
değil; koşudan sonra yazıldı, 20 Kasım 2026).

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz5_3_yeni_cekirdek_2026-11-19/ek_hesap.py > .../ek_hesap.txt

Soru: eğim kollarındaki döngüler (birincilde koşu başına binlerce) tohumlara
nasıl dağılıyor, teslimle ve rota yokluğu kaybıyla ilişkili mi, teslim edilen
paketlerin ne kadarı döngüden geçmiş görünüyor?
"""
import importlib.util
import statistics as ist
from pathlib import Path

D = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("sh", D / "sonuc_hesap.py")
sh = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sh)

kayit, _ = sh.oku(D, False)
KOLLAR = (sh.CEK, sh.VAZ0, sh.DUZ0, sh.EGIM0)
SAYAC = ("rota.dongu", "rota.dislama", "rota.son_care", "rota.zorunlu_gecis",
         "rota.yol_yok", "rota.tavan_asimi", "rota.aclik")
UZUN = 12      # teslimde ≥ 12 atlama: p99'un (8–11) üstü, döngü izi


def pearson(x, y):
    if len(x) < 3 or ist.pstdev(x) == 0 or ist.pstdev(y) == 0:
        return None
    mx, my = ist.mean(x), ist.mean(y)
    return (sum((a - mx) * (b - my) for a, b in zip(x, y))
            / (len(x) * ist.pstdev(x) * ist.pstdev(y)))


def r_grubu(h, r):
    g = sh.gruplar(h, [r])
    return g["R"], g["I"]


for h in sh.HUCRE:
    print(f"== {sh.HAD[h]} — tohum başına ==")
    for kol in KOLLAR:
        rs = kayit[h][kol]
        print(f"  {sh.AD[kol]}")
        print("    tohum  ölçü   döngü  dışla  sonçare zorunlu yolyok tavan "
              "açlık  R      İ      uzun_teslim gönderim_s")
        x_d, y_o, y_r = [], [], []
        for t in sh.TOHUMLAR:
            r = rs[t]
            tt = r["teshis_toplam"]
            o = sh.olcu(h, r)
            R, I = r_grubu(h, r)
            at = {int(k): v for k, v in r["kaydedici"]["atlama"].items()}
            top = sum(at.values())
            uzun = sum(v for k, v in at.items() if k >= UZUN) / top
            v = [tt.get(k) for k in SAYAC]
            print(f"    {t}  {o:.3f}  " + "  ".join(
                f"{'—' if a is None else int(a):>5}" for a in v)
                + f"  {R:.3f}  {I:.3f}  {uzun:.4f}      "
                f"{r['enerji_s']['enerji_gonderim_s']:.0f}")
            if tt.get("rota.dongu") is not None:
                x_d.append(tt["rota.dongu"])
                y_o.append(o)
                y_r.append(R)
        rd = pearson(x_d, y_o)
        rr = pearson(x_d, y_r)
        if rd is not None:
            print(f"    Pearson r (döngü ↔ ölçü) {rd:+.2f} · (döngü ↔ R) "
                  f"{rr:+.2f}")
    print()

print("== birincil: eğimli kollar ↔ eğim0, tohum başına ölçü farkı ==")
h = "birincil"
e0 = {t: sh.olcu(h, r) for t, r in kayit[h][sh.EGIM0].items()}
for kol in (sh.CEK, sh.VAZ0, sh.DUZ0):
    d = {t: sh.olcu(h, r) - e0[t] for t, r in kayit[h][kol].items()}
    print(f"  {sh.AD[kol]} − eğim0: " + " · ".join(
        f"{t} {v:+.3f}" for t, v in sorted(d.items()))
        + f" · sapma {ist.stdev(d.values()):.3f}")
for kol in KOLLAR + (sh.BABEL,):
    v = [sh.olcu(h, r) for r in kayit[h][kol].values()]
    print(f"  {sh.AD[kol]:<9} tohumlar arası sapma {ist.stdev(v):.3f} · en "
          f"düşük {min(v):.3f}")
