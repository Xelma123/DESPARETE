"""Faz 5-3 yeniden tasarım · Aşama 1.1 — hedef ve başarı ölçütünün sayıları
(`v2/18` §1.1). Simülasyon yok; kayıtlardan okunur.

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz5_3_tasarim_zemini_2026-11-24/hedef_sayilari.py > .../hedef_sayilari.txt

Kaynaklar:
- teşhis (c) (`arsiv/teshis/faz5_2_rakip_cizgisi_2026-11-15/`): AODV,
  OLSRv2, Babel, kâhin; ikiz, birincil (15/15) ve dayanıklılık (10/20)
  hücreleri, tohum 1003–1010;
- yeni çekirdeğin ölçümü (`../faz5_3_yeni_cekirdek_2026-11-19/`): 19 Kasım
  çekirdeği; döngü kuralları ölçümü (`../faz5_3_dongu_kurallari_2026-11-24/`):
  geri+sınır.
Ölçüler yeni çekirdeğin ölçümünün `sonuc_hesap.py`'sinden aynen alınır.
"""
import importlib.util
import json
import statistics as ist
from pathlib import Path

D = Path(__file__).resolve().parent
T = D.parent
_spec = importlib.util.spec_from_file_location(
    "sh", T / "faz5_3_yeni_cekirdek_2026-11-19" / "sonuc_hesap.py")
sh = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(sh)
C = T / "faz5_2_rakip_cizgisi_2026-11-15"
CIZ = {"ikiz": None, "birincil": "15/15", "dayaniklilik": "10/20"}


def satirlar(dosya: Path, anahtar: str, kol: str | None = None) -> list:
    k = json.loads(dosya.read_text(encoding="utf-8"))
    return sorted((r for r in k["sonuc"]
                   if (r.get("kol") or r["protokol"].split("@")[0]) == anahtar
                   or (kol and r.get("kol") == kol)),
                  key=lambda r: r["tohum"])


def ozet(h: str, rs: list) -> str:
    if h == "ikiz":
        v = [sh.oran(r["ikincil"]["pencere"]) for r in rs]
        ses = None
    else:
        c = r_c = CIZ[h]
        v = [sh.oran(r["ikincil"]["cizelge"][c]["acik"]) for r in rs]
        ses = ist.mean(sh.oran(r["ikincil"]["cizelge"][r_c]["sessiz"])
                       for r in rs)
    p99 = ist.mean(r["gecikme_s"]["p99"] for r in rs)
    kon = sum(r["sayaclar"]["kontrol_airtime_s"] for r in rs)
    top = sum(r["enerji_s"]["enerji_gonderim_s"] for r in rs)
    return (f"n {len(rs)} · ölçü {ist.mean(v):.3f} ± {ist.stdev(v):.3f} · en "
            f"kötü {min(v):.3f}"
            + (f" · sessiz {ses:.3f}" if ses is not None else "")
            + f" · p99 {p99:.2f} s · kontrol payı {kon / top:.1%}")


print("ölçü: ikizde pencere PDR'si, birincil ve dayanıklılıkta PDR_açık "
      "(8 tohum, 1003–1010)\n")
for h, dosya in (("ikiz", "kayit_ikiz.json"),
                 ("birincil", "kayit_birincil.json"),
                 ("dayaniklilik", "kayit_dayaniklilik.json")):
    print(f"== {h} ==")
    for p in ("aodv", "olsrv2", "babel", "en_guvenilir_kahin"):
        print(f"  {p:<20} {ozet(h, satirlar(C / dosya, p))}")
    if h != "dayaniklilik":
        rs = satirlar(T / "faz5_3_yeni_cekirdek_2026-11-19"
                      / f"kayit_cekirdek_{h}.json", "cekirdek")
        print(f"  {'19 Kasım çekirdeği':<20} {ozet(h, rs)}")
        rs = satirlar(T / "faz5_3_dongu_kurallari_2026-11-24"
                      / f"kayit_geri_sinir_{h}.json", "geri_sinir")
        print(f"  {'geri+sınır':<20} {ozet(h, rs)}")
    else:
        print("  (yeni sürümler bu hücrede ölçülmedi)")
    print()

kayit, _ = sh.oku(T / "faz5_3_yeni_cekirdek_2026-11-19", False)
b = sh.dizi(kayit, "birincil", sh.BABEL, lambda r: sh.olcu("birincil", r))
k = sh.dizi(kayit, "birincil", sh.KAHIN, lambda r: sh.olcu("birincil", r))
e = sh.esli(k, b)
print(f"birincilde kâhin − Babel: {e[0]:+.3f} (eşli farkın sapması "
      f"{ist.stdev(e[4].values()):.3f}); hedef Babel + 0,05 = "
      f"{ist.mean(b.values()) + 0.05:.3f}")
