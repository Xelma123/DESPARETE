"""K-172 · DESPARETE V11 (komut geri izi) A/B — tam ölçek, kısa pencere.

Kollar: v0.4 (`SECENEK_V04`) ↔ v0.4 + V11. Eşli tohum (1003–1007, geliştirme),
iki senaryo, yere toplama. Pencere regresyonunki: 50 s koşu, 10–40 s ölçüm,
karıştırıcı 5 s'de açılır. Beklenti önceden: `beklenti.md` §3.

Kullanım:
    PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python -u \
        arsiv/teshis/v11_komut_geri_izi_2026-09-26/ab.py
"""

from __future__ import annotations

import json
import statistics as ist
import sys
import time
from dataclasses import replace
from multiprocessing import Pool
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from protokoller.desparete import DESPARETE  # noqa: E402
from protokoller.desparete_bayrak import PROFIL_V02, SECENEK_V04  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.kosum.sonuc import sonuc_satiri  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402

DIZIN = Path(__file__).resolve().parent
KOLLAR = {"v04": SECENEK_V04,
          "v04_v11": replace(SECENEK_V04, komut_ters_yol=True)}
SENARYOLAR = ("statik-surekli", "bagimsiz-surekli")
TOHUMLAR = tuple(range(1003, 1008))
SAYACLAR = ("komut_iz_iletilen", "komut_izsiz", "geri_iz_ogrenilen",
            "geri_iz_silinen", "veri_hop_siniri", "veri_sink_disi")


def _is(is_):
    senaryo, tohum, kol = is_
    t0 = time.perf_counter()
    kfg = Konfig(kol=f"v11_ab_{kol}", senaryo=senaryo, tohum=tohum,
                 not_=f"{senaryo}-{tohum}-{kol}", trafik_deseni="yere_toplama",
                 karistirici_baslangic_s=5.0, isinma_s=10.0,
                 olcum_bitis_s=40.0, kosu_bitis_s=50.0)
    kur = kurulum_yap(kfg)
    sec = KOLLAR[kol]
    kosu = Kosu(kur, lambda i: DESPARETE(i, kfg.gecit, bayraklar=PROFIL_V02,
                                         secenekler=sec))
    kosu.kostur()
    s = sonuc_satiri(kur, kosu.dugumler, "desparete")
    m, k = s["metrikler"], s["korunum"]
    p = [d.protokol for d in kosu.dugumler]
    return {
        "senaryo": senaryo, "tohum": tohum, "kol": kol,
        "gecerli": k["gecerli"],
        "pdr_komut_pencere": m.get("pdr_komut_pencere"),
        "pdr_telemetri_pencere": m.get("pdr_telemetri_pencere"),
        "pdr_komut": m.get("pdr_komut"),
        "pdr_telemetri": m.get("pdr_telemetri"),
        "kontrol_bayt": m.get("kontrol_bayt"),
        "duyma_bildirimi": m.get("duyma_bildirimi"),
        "dusen": {a: v for a, v in k["dusen"].items() if v},
        "sayac": {a: sum(q._sayac[a] for q in p) for a in SAYACLAR},
        "sure_s": time.perf_counter() - t0,
    }


def _ozet(sonuclar: list[dict]) -> None:
    anahtar = {(r["senaryo"], r["tohum"], r["kol"]): r for r in sonuclar}
    print(f"gecerli: {sum(r['gecerli'] for r in sonuclar)}/{len(sonuclar)}")
    for sen in SENARYOLAR:
        print(f"\n== {sen}  (tohum {TOHUMLAR[0]}–{TOHUMLAR[-1]}, pencere)")
        print(f"  {'tohum':>5} {'komut A':>8} {'komut B':>8} {'tel A':>7} "
              f"{'tel B':>7} {'ΔTel':>7} {'kbayt B/A':>9} {'süre B/A':>8}")
        dk, dt, kb, sr = [], [], [], []
        for t in TOHUMLAR:
            a, b = anahtar[(sen, t, "v04")], anahtar[(sen, t, "v04_v11")]
            d_tel = b["pdr_telemetri_pencere"] - a["pdr_telemetri_pencere"]
            oran_k = b["kontrol_bayt"] / a["kontrol_bayt"]
            oran_s = b["sure_s"] / a["sure_s"]
            dk.append(b["pdr_komut_pencere"])
            dt.append(d_tel)
            kb.append(oran_k)
            sr.append(oran_s)
            print(f"  {t:>5} {a['pdr_komut_pencere']:>8.3f} "
                  f"{b['pdr_komut_pencere']:>8.3f} "
                  f"{a['pdr_telemetri_pencere']:>7.3f} "
                  f"{b['pdr_telemetri_pencere']:>7.3f} {d_tel:>+7.3f} "
                  f"{oran_k:>9.3f} {oran_s:>8.2f}")
        print(f"  ort   komut B {ist.mean(dk):.3f} · ΔTel {ist.mean(dt):+.4f} "
              f"(+{sum(x > 0 for x in dt)}/−{sum(x < 0 for x in dt)}) · "
              f"kbayt B/A {ist.mean(kb):.3f} · süre B/A {ist.mean(sr):.2f}")
        for kol in ("v04", "v04_v11"):
            toplam: dict[str, int] = {}
            for t in TOHUMLAR:
                r = anahtar[(sen, t, kol)]
                for a, v in {**r["dusen"], **r["sayac"]}.items():
                    toplam[a] = toplam.get(a, 0) + v
            print(f"  {kol:<8} toplam: " + " · ".join(
                f"{a}={v}" for a, v in sorted(toplam.items()) if v))


if __name__ == "__main__":
    isler = [(s, t, k) for s in SENARYOLAR for t in TOHUMLAR for k in KOLLAR]
    t0 = time.perf_counter()
    with Pool(8) as havuz:
        sonuclar = list(havuz.imap_unordered(_is, isler, chunksize=1))
    (DIZIN / "ab_sonuc.json").write_text(
        json.dumps(sorted(sonuclar, key=lambda r: (r["senaryo"], r["tohum"],
                                                   r["kol"])),
                   ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"V11 A/B — {len(isler)} koşu · "
          f"{(time.perf_counter() - t0) / 60:.1f} dk")
    _ozet(sonuclar)
