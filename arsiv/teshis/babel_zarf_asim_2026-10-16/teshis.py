"""K-192 (b) · Babel zarfı aşıyor (eşler arası, üç hücre) — yazılım hatası aranır.

16 Ekim 2026 · tetik: `arsiv/teshis/babel_zarf_esler_2026-10-16/zarf.txt`.
Babel görev 1001 · görev 1002 · formasyon 1001'de üç kâhinin zarfını aşıyor.
Kural (`babel_zarf_esler_2026-10-16/beklenti.md`): *"yazılım hatası aranır
(kâhin sızıntısı, sayım, korunum); Babel donmaz."* Ölçüt ve okuma kuralı
`beklenti.md`de.

Her hücrede Babel ve iki kâhin (ETX · en olası teslim) U1'in yapılandırmasıyla
koşar; paket başına doğum anı ve teslim kaydı tutulur:
  - sayım/korunum: korunum, kopya, PDR'nin U1 ve zarf kayıtlarıyla kimliği;
  - Babel'in ulaştırıp zarf kâhininin ulaştıramadığı paketler ve kâhinin
    düşme sebepleri;
  - kâhin grafiğinin dilim içi yaşı: doğum anının dilim içindeki evresine
    göre teslim oranı (grafik `dilim_suresi_s`de bir yenilenir; karıştırıcısız
    kolda başka yenileme yok, K-195).

    KOK=<donmuş kopya> py -3.11 -u arsiv/teshis/babel_zarf_asim_2026-10-16/teshis.py
    (`TESHIS_KISA=1` yalnız duman sınaması: kısa pencere, tek hücre)
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
KISA = bool(os.environ.get("TESHIS_KISA"))
# (kol, tohum): U1 kaydındaki PDR'ler (Babel, ETX) ve zarf koşusundaki en
# olası teslim — kimlik denetimi için.
HUCRELER = {("gorev-yok", 1001): (0.8935, 0.8403, 0.8500),
            ("gorev-yok", 1002): (0.8638, 0.8392, 0.8632),
            ("formasyon-yok", 1001): (0.9636, 0.9424, 0.8891)}
KOLLAR = ("babel", "en_guvenilir_kahin", "en_olasi_teslim_kahin")
EVRE_KOVASI = 5


def _kos(gorev):
    kol, tohum, ad = gorev
    t0 = time.perf_counter()
    from kalibrasyon import dunya_secimi as DS
    from kalibrasyon.aodv_uygunluk import _fabrika
    from kalibrasyon.kahin import KanalGrafigi, dilim_suresi_s
    from kalibrasyon.ust_referans import KAHINLER, TeslimGrafigi
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.kurulum import kurulum_yap
    from sim2.kosum.sonuc import sonuc_satiri
    ek = (dict(karistirici_baslangic_s=5.0, isinma_s=10.0,
               olcum_bitis_s=40.0, kosu_bitis_s=50.0) if KISA else {})
    kfg = DS.konfig(kol="u1", senaryo=kol, tohum=tohum, trafik_deseni=DESEN,
                    **ek)
    kur = kurulum_yap(kfg)
    if ad == "babel":
        fabrika = _fabrika("babel", kfg)
    else:
        tip = KAHINLER[ad]
        grafik = (TeslimGrafigi(kur) if ad == "en_olasi_teslim_kahin"
                  else KanalGrafigi(kur))
        fabrika = (lambda i: tip(i, grafik))
    kosu = Kosu(kur, fabrika)
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "u1")
    pd = kur.paket_defteri
    return {"kol": kol, "tohum": tohum, "ad": ad,
            "pdr": satir["metrikler"]["pdr"], "korunum": satir["korunum"],
            "dilim_s": dilim_suresi_s(kfg),
            "dogum": {str(k): v[1] for k, v in pd._dogum.items()},
            "teslim": sorted(pd._teslim_kimlikleri),
            "sure_s": time.perf_counter() - t0}


def _analiz(kayitlar: list[dict]) -> int:
    hata = False
    for (kol, tohum), (u1_babel, u1_etx, zarf_eot) in HUCRELER.items():
        r = {x["ad"]: x for x in kayitlar
             if x["kol"] == kol and x["tohum"] == tohum}
        if len(r) < len(KOLLAR):
            continue
        b = r["babel"]
        print(f"\n=== {kol} {tohum}")
        # 1 · Sayım ve korunum
        beklenen = {"babel": u1_babel, "en_guvenilir_kahin": u1_etx,
                    "en_olasi_teslim_kahin": zarf_eot}
        for ad in KOLLAR:
            k = r[ad]["korunum"]
            kimlik = KISA or abs(r[ad]["pdr"] - beklenen[ad]) < 5e-5
            print(f"  {ad:<24} PDR {r[ad]['pdr']:.4f} (kayıt "
                  f"{beklenen[ad]:.4f}, {'aynı' if kimlik else 'FARKLI'}) · "
                  f"korunum {k.get('gecerli')} · kopya "
                  f"{k.get('kopya_uretilen', 0)} · düşen {k.get('dusen')}")
            if not (kimlik and k.get("gecerli")):
                hata = True
        if b["korunum"].get("kopya_uretilen", 0):
            hata = True
        # 2 · Zarf kâhini: Babel'in ulaştırıp onun ulaştıramadığı paketler
        z_ad = max(("en_guvenilir_kahin", "en_olasi_teslim_kahin"),
                   key=lambda a: r[a]["pdr"])
        z = r[z_ad]
        bt, zt = set(b["teslim"]), set(z["teslim"])
        print(f"  zarf kâhini {z_ad}: yalnız Babel {len(bt - zt)} · yalnız "
              f"kâhin {len(zt - bt)} · ikisi {len(bt & zt)} · doğan "
              f"{len(b['dogum'])} (kâhinde {len(z['dogum'])})")
        # 3 · Dilim içi evreye göre teslim oranı
        dilim = z["dilim_s"]
        for ad in ("babel", z_ad):
            x = r[ad]
            ts = set(x["teslim"])
            kova = [[0, 0] for _ in range(EVRE_KOVASI)]
            for k, t in x["dogum"].items():
                i = min(int((t % dilim) / dilim * EVRE_KOVASI),
                        EVRE_KOVASI - 1)
                kova[i][0] += 1
                kova[i][1] += int(k) in ts
            print(f"  evre ({dilim:.1f} s dilim, {EVRE_KOVASI} kova) "
                  f"{ad:<24} " + " · ".join(
                      f"{t / max(n, 1):.3f}" for n, t in kova))
    print("\n" + ("SAYIM/KORUNUM/KİMLİK: kusur izi VAR" if hata else
                  "SAYIM/KORUNUM/KİMLİK: kusur izi yok"))
    return 1 if hata else 0


def main() -> int:
    kayit = BURA / ("teshis_kisa.jsonl" if KISA else "teshis.jsonl")
    hucreler = list(HUCRELER)[:1] if KISA else list(HUCRELER)
    bitti = set()
    if kayit.exists():
        for s in kayit.read_text(encoding="utf-8").splitlines():
            x = json.loads(s)
            bitti.add((x["kol"], x["tohum"], x["ad"]))
    isler = [(k, t, a) for (k, t) in hucreler for a in KOLLAR
             if (k, t, a) not in bitti]
    print(f"kok {KOK} · {len(isler)} koşu kaldı{' · KISA' if KISA else ''}")
    with Pool(int(os.environ.get("TESHIS_ISCI", "5")),
              maxtasksperchild=1) as havuz:
        for x in havuz.imap_unordered(_kos, isler):
            with kayit.open("a", encoding="utf-8") as f:
                f.write(json.dumps(x) + "\n")
            print(f"  {x['kol']} {x['tohum']} {x['ad']:<24} PDR "
                  f"{x['pdr']:.4f} · {x['sure_s'] / 60:.0f} dk", flush=True)
    kayitlar = [json.loads(s) for s in
                kayit.read_text(encoding="utf-8").splitlines()]
    return _analiz(kayitlar)


if __name__ == "__main__":
    raise SystemExit(main())
