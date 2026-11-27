"""
Faz 5-3 · B7 (bekletme ve komut) için hesap: bugünkü bekletmenin ve komutun
sayıları. Yeni koşu yok; B5 teşhisinin kayıtlarından okur (`eğim0` kolu,
ikiz ve birincil, 8 tohum, tam koşu). Bugünkü kodda bekletme atlama başına en
çok 1 s (`TUTMA_EN_COK_S`), tampon 0,5 s'de bir yeniden sorulur, komut geri
izle gider (`kural/KK-05`).

    PYTHONIOENCODING=utf-8 py -3.11 <bu dosya> > bekletme_komut.txt

Babel-a'nın gecikmesi ve rota yokluğu kaybı karşılaştırma için teşhis (c)'nin
kayıtlarından (`arsiv/teshis/faz5_2_rakip_cizgisi_2026-11-15/`, aynı
tohumlar).
"""

from __future__ import annotations

import json
import statistics as ist
import sys
from pathlib import Path

D = Path(__file__).resolve().parent
B5 = D.parent / "faz5_3_b5_iletim_kaybi_2026-11-26"
sys.path.insert(0, str(B5))

import sonuc_hesap as SH  # noqa: E402

EVRELER = ("once", "acik", "sessiz")


def aralik(v: list[float], fmt: str = "{:.0f}") -> str:
    return (f"{fmt.format(ist.mean(v))} ({fmt.format(min(v))}–"
            f"{fmt.format(max(v))})")


def pay_sebep(r: dict, sebep: str, evre: str) -> float:
    n = r["karistirici_evresi"][evre]["dogan"]
    if not n:
        return float("nan")
    k = sum(v for a, v in r["dogum_evre_dusen"].items()
            if a.startswith(f"{sebep}|{evre}|"))
    return k / n


def yaz(a: dict[str, list[float]]) -> None:
    for ad, v in a.items():
        v = [x for x in v if x == x]                 # nan'ları at
        if not v:
            continue
        if "pay" in ad:
            print(f"  {ad:<58} {aralik([100 * x for x in v], '%{:.2f}')}")
        elif ad.endswith(", s"):
            print(f"  {ad:<58} {aralik(v, '{:.2f}')}")
        else:
            print(f"  {ad:<58} {aralik(v)}")
    print()


def main() -> None:
    kayit = SH.oku(B5)
    for h, rs in kayit.items():
        a: dict[str, list[float]] = {}

        def ekle(ad: str, x: float) -> None:
            a.setdefault(ad, []).append(x)

        for r in rs:
            t = r["teshis_toplam"]
            ac = t["rota.aclik"]
            ekle("açlık bölümü", ac)
            ekle("açlığın toplam süresi, s", t["rota.aclik_sure_ms"] / 1000)
            ekle("açlık bölümünün ortalama süresi, s",
                 t["rota.aclik_sure_ms"] / 1000 / ac if ac else float("nan"))
            bek = t["bekletme.bekletilen"]
            ekle("bekletilen paket (ayrı paket)", bek)
            ekle("  bekledikten sonra giden payı",
                 t["bekletme.bekletmeden_giden"] / bek if bek else float("nan"))
            ekle("  süresi dolup düşen payı (1 s)",
                 t["bekletme.suresi_dolan"] / bek if bek else float("nan"))
            pen = r["ikincil"]["pencere"]
            ekle("bekledikten sonra gidenin penceredeki teslime payı",
                 t["bekletme.bekletmeden_giden"] / pen["teslim"])
            ekle("gecikme p50, s", r["gecikme_s"]["p50"])
            ekle("gecikme p95, s", r["gecikme_s"]["p95"])
            ekle("gecikme p99, s", r["gecikme_s"]["p99"])
            for e in EVRELER:
                ekle(f"rota yokluğu kaybının payı, {e} doğumlu",
                     pay_sebep(r, "rota_gecersiz", e))
                ekle(f"iletim kaybının payı, {e} doğumlu",
                     pay_sebep(r, "iletim_basarisiz", e))
            ciz = r["ikincil"]["cizelge"]
            acik = next(iter(ciz.values()))["acik"]
            if acik["dogan"]:
                ekle("açıkta doğup 5 s'den geç teslim edilenin payı",
                     (acik["teslim"] - acik["teslim_tavan"]["5"])
                     / acik["dogan"])
            ekle("komut: gönderilen karar", t["protokol.komut_gonderilen"])
            ekle("komut: bekletilen karar", t["protokol.komut_bekletilen"])
            ekle("komut: düşürülen", t["protokol.komut_dusen"])
            kd = r["kaydedici"]
            ka = kd["dogan_acik"]["komut"]
            if ka:
                ekle("komut: açıkta doğan", ka)
                ekle("komut: açıkta doğup iletimde kaybolan payı",
                     sum(kd["komut_kayip"].values()) / ka)
                ekle("telemetri: açıkta doğup iletimde kaybolan payı",
                     len(kd["kayip"]) / kd["dogan_acik"]["telemetri"])
            ekle("geri iz: öğrenilen", t["iz.iz_ogrenilen"])
            ekle("geri iz: eski sırayla yok sayılan", t["iz.iz_eski_sira"])
        print(f"== {h} · koşu başına, 8 tohumun ortalaması (en az–en çok) ==")
        yaz(a)

    rc = D.parent / "faz5_2_rakip_cizgisi_2026-11-15"
    for h in ("ikiz", "birincil"):
        with open(rc / f"kayit_{h}.json", encoding="utf-8") as f:
            rs = [r for r in json.load(f)["sonuc"] if r["protokol"] == "babel"]
        a = {}
        for r in rs:
            for x, ad in (("p50", "gecikme p50, s"), ("p95", "gecikme p95, s"),
                          ("p99", "gecikme p99, s")):
                a.setdefault(ad, []).append(r["gecikme_s"][x])
            for e in EVRELER:
                if r["karistirici_evresi"][e]["dogan"]:
                    a.setdefault(f"rota yokluğu kaybının payı, {e} doğumlu",
                                 []).append(pay_sebep(r, "rota_gecersiz", e))
        print(f"== Babel-a · {h} · koşu başına, {len(rs)} tohumun ortalaması "
              f"(teşhis (c)'nin kayıtları) ==")
        yaz(a)


if __name__ == "__main__":
    main()
