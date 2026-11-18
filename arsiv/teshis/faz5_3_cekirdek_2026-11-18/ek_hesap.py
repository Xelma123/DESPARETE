"""Faz 5-3 çekirdek ölçümü · ek sayılar (koşudan SONRA yazıldı; karar girdisi
değil). Tohum başına teslim, rota yokluğu kaybı ve çekirdeğin tanı sayaçları;
çöken tohumlar ile tur artışı ve açlık arasındaki ilişkiye bakmak için.

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz5_3_cekirdek_2026-11-18/ek_hesap.py
"""
import json
import statistics as ist
from pathlib import Path

D = Path(__file__).resolve().parent
SAYAC = ("rota.tur_artirildi", "rota.aclik", "rota.aclik_istegi",
         "rota.istek_iletilen", "rota.ardil_degisti", "rota.zorunlu_gecis",
         "rota.geri_cekme_alinan", "bag.veri_kotu", "bag.kotu_selam",
         "bag.kotu_donus", "bag.df_bayat", "bag.komsu_silindi",
         "selam.ara_ilan", "bekletme.suresi_dolan")
KISA = {k: k.split(".")[1][:10] for k in SAYAC}


def rgrubu(r, ikiz: bool) -> float:
    paydas = (r["ikincil"]["pencere"] if ikiz
              else r["ikincil"]["cizelge"]["15/15"]["acik"])["dogan"]
    n = 0
    for k, v in r["dogum_evre_dusen"].items():
        sebep, evre, _ = k.split("|")
        if sebep in ("rota_gecersiz", "hedef_yok", "tampon_asimi") and (
                ikiz or evre == "acik"):
            n += v
    return n / paydas


for ad, ikiz in (("ikiz", True), ("birincil", False)):
    k = json.loads((D / f"kayit_cekirdek_{ad}.json").read_text(
        encoding="utf-8"))
    rs = sorted(k["sonuc"], key=lambda r: r["tohum"])
    print(f"== {ad} ==")
    print("tohum  ölçü    R     " + " ".join(f"{KISA[s]:>10}" for s in SAYAC))
    satirlar = []
    for r in rs:
        o = r["ikincil"]["pencere"] if ikiz else (
            r["ikincil"]["cizelge"]["15/15"]["acik"])
        olcu = o["teslim"] / o["dogan"]
        t = r["teshis_toplam"]
        satirlar.append((olcu, t.get("rota.tur_artirildi", 0),
                         t.get("rota.aclik", 0), t.get("bag.df_bayat", 0),
                         t.get("bag.kotu_selam", 0),
                         t.get("rota.ardil_degisti", 0)))
        print(f"{r['tohum']}  {olcu:.3f}  {rgrubu(r, ikiz):.3f} "
              + " ".join(f"{t.get(s, 0):>10.0f}" for s in SAYAC))
    olcu = [s[0] for s in satirlar]
    for i, ad2 in ((1, "tur artışı"), (2, "açlık"), (3, "d_f bayatladı"),
                   (4, "selamdan KÖTÜ"), (5, "ardıl değişimi")):
        x = [s[i] for s in satirlar]
        print(f"  ölçü ↔ {ad2}: Pearson r = {ist.correlation(olcu, x):+.2f}")
