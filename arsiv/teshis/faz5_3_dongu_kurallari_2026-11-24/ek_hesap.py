"""Faz 5-3 · döngü kuralları — kuraldan sonra bakılan ek sayılar (karar
girdisi değil; koşudan sonra yazıldı, 24 Kasım 2026).

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz5_3_dongu_kurallari_2026-11-24/ek_hesap.py > .../ek_hesap.txt

1. İkizde geri+sınır − Babel ve − eğim0, tohum başına.
2. Dumandaki varsayım (kural 13, kural 9'un iki düğümlü döngü kanıtını
   siliyor): tohum başına tavan aşımı ve döngü dönüşü, 19 Kasım ↔ geri;
   iki düğümlü dönüşlerin üst sınırı (2 − dışlama/döngü).
3. B'de evreler (önce · açık · sessiz) ve kayıp grupları, beş kol.
"""
import importlib.util
from pathlib import Path

D = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location("sh24", D / "sonuc_hesap.py")
m = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(m)
sh = m.sh
kayit, _ = m.oku(D, False)
I, B = "ikiz", "birincil"


def y(h, k):
    return m.dizi(kayit, h, k, lambda r: m.olcu(h, r))


print("== 1 · İkizde geri+sınır − Babel · − eğim0 · − 19 Kasım ==")
for k in (m.BABEL, m.EGIM0, m.C19):
    e = m.esli(y(I, m.GS), y(I, k))
    print(f"  − {m.AD[k]:<9} {m.esli_metni(e)} → {m.ayris(e, m.ESIK)}")

print("\n== 2 · Kural 13'ün kural 9'la etkileşimi (tohum başına) ==")
for h in (I, B):
    print(f"  {h}: tavan aşımı · döngü dönüşü (19 Kasım → geri → geri+sınır)")
    for t in m.TOHUMLAR:
        v = [kayit[h][k][t]["teshis_toplam"] for k in (m.C19, m.GERI, m.GS)]
        print(f"    {t}  tavan " + " → ".join(
            f"{x.get('rota.tavan_asimi', 0):.0f}" for x in v)
              + " · döngü " + " → ".join(
            f"{x.get('rota.dongu', 0):.0f}" for x in v))
    for k in (m.C19, m.GERI, m.GS):
        rs = kayit[h][k].values()
        d = sum(r["teshis_toplam"]["rota.dongu"] for r in rs)
        s = sum(r["teshis_toplam"]["rota.dislama"] for r in rs)
        print(f"    {m.AD[k]:<10} iki düğümlü dönüşlerin üst sınırı "
              f"{2 - s / d:.2f} (döngü {d / 8:.0f}/koşu)")

print("\n== 3 · B'de evreler ve açık dönemin kayıp grupları ==")
for k in (m.BABEL, m.EGIM0, m.C19, m.GERI, m.GS):
    ev = {e: m.ort(m.dizi(kayit, B, k, lambda r, e=e: (
        m.oran(r["ikincil"]["once"]) if e == "once"
        else m.oran(m.donem(B, r, e))))) for e in ("once", "acik", "sessiz")}
    g = sh.gruplar(B, list(kayit[B][k].values()))
    print(f"  {m.AD[k]:<10} önce {ev['once']:.3f} · açık {ev['acik']:.3f} · "
          f"sessiz {ev['sessiz']:.3f} | R {g['R']:.3f} · İ {g['I']:.3f} · "
          f"K {g['K']:.3f}")
