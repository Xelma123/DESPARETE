"""K-192 (b) · Babel'in kâhin aşımı, EŞLER ARASI — beş hücrede üç kâhinin zarfı.

K-244 kuyruğunun U1'i (eşler arası, 16 Ekim): Babel beş hareketli hücrede ETX
kâhinini R'den (0,0126) fazla aşıyor. Yere toplamanın betiğiyle
(`arsiv/teshis/babel_zarf_2026-10-15/zarf.py`) aynı; yalnız desen, hücreler
ve işçi sayısı (5; döngü izinin 3 işçisiyle toplam 8). Zarf = üç kâhinin PDR'lerinin en
büyüğü (`ust_referans.KAHINLER`). ETX kâhini U1'de aynı yapılandırmayla
ölçüldü (deterministik), burada öteki iki kâhin koşulur. Karar kuralı
kuyruğun beklentisinde (`arsiv/teshis/rakipler_k244_2026-10-14/beklenti.md`
§2): Babel ≤ zarf ise kayıt, zarfı da aşıyorsa yazılım hatası aranır.

    KOK=<donmuş kopya> py -3.11 -u arsiv/teshis/babel_zarf_esler_2026-10-16/zarf.py
"""
from __future__ import annotations

import json
import os
import pathlib
import sys
import time
from multiprocessing import Pool

KOK = pathlib.Path(os.environ.get("KOK")
                   or pathlib.Path(__file__).resolve().parents[3])
BURA = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(KOK))
os.environ["DESPARETE_DUNYA"] = "referans_2026"

DESEN = "esler_arasi"
# (kol, tohum): (Babel PDR, ETX kâhini PDR) — K-244 kuyruğunun U1 kaydı
# (`babel_referans_2026_esler_arasi_20261016_142910.json`).
HUCRELER = {("bagimsiz-yok", 1002): (0.8963, 0.8787),
            ("gorev-yok", 1000): (0.9755, 0.9612),
            ("gorev-yok", 1001): (0.8935, 0.8403),
            ("gorev-yok", 1002): (0.8638, 0.8392),
            ("formasyon-yok", 1001): (0.9636, 0.9424)}


def _kos(gorev):
    kol, tohum, kahin = gorev
    t0 = time.perf_counter()
    from kalibrasyon import dunya_secimi as DS
    from kalibrasyon.kahin import KanalGrafigi
    from kalibrasyon.ust_referans import KAHINLER, TeslimGrafigi
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.kurulum import kurulum_yap
    from sim2.kosum.sonuc import sonuc_satiri
    kfg = DS.konfig(kol="u1", senaryo=kol, tohum=tohum, trafik_deseni=DESEN)
    kur = kurulum_yap(kfg)
    tip = KAHINLER[kahin]
    grafik = (TeslimGrafigi(kur) if kahin == "en_olasi_teslim_kahin"
              else KanalGrafigi(kur))
    kosu = Kosu(kur, lambda i: tip(i, grafik))
    kosu.kostur()
    m = sonuc_satiri(kur, kosu.dugumler, "u1")["metrikler"]
    return {"kol": kol, "tohum": tohum, "kahin": kahin, "pdr": m["pdr"],
            "sure_s": time.perf_counter() - t0}


def main() -> int:
    from kalibrasyon.ust_referans import KAHINLER
    etx = "en_guvenilir_kahin"
    assert etx in KAHINLER
    isler = [(k, t, ad) for (k, t) in HUCRELER for ad in sorted(KAHINLER)
             if ad != etx]
    kayit = BURA / "zarf.jsonl"
    with Pool(5) as havuz:
        for r in havuz.imap_unordered(_kos, isler):
            with kayit.open("a", encoding="utf-8") as f:
                f.write(json.dumps(r) + "\n")
            print(f"  {r['kol']} {r['tohum']} {r['kahin']:<24} PDR "
                  f"{r['pdr']:.4f} · {r['sure_s'] / 60:.0f} dk", flush=True)
    sonuc = [json.loads(s) for s in kayit.read_text(encoding="utf-8").splitlines()]
    hepsi = True
    print()
    for (k, t), (babel, etx_pdr) in HUCRELER.items():
        pdrler = {r["kahin"]: r["pdr"] for r in sonuc
                  if r["kol"] == k and r["tohum"] == t}
        pdrler[etx] = etx_pdr
        zarf = max(pdrler.values())
        icinde = babel <= zarf
        hepsi &= icinde
        print(f"  {k} {t}: " + " · ".join(f"{a} {p:.4f}" for a, p in
                                          sorted(pdrler.items()))
              + f" → zarf {zarf:.4f} · Babel {babel:.4f} · "
              + ("🟢 zarfın içinde" if icinde else "🔴 zarfı da aşıyor"))
    print("\n  " + ("🟢 beş hücre de zarfın içinde — ETX kâhini bu hücrelerde "
                    "üst sınır değil, kayıt (K-192 b)" if hepsi else
                    "🔴 zarfı aşan hücre var — yazılım hatası aranır (K-192 b)"))
    return 0 if hepsi else 1


if __name__ == "__main__":
    raise SystemExit(main())
