"""G1-P kaldı (K-244 kuyruğu): M4 yanlış tespiti 2/8 — sebep ölçülür.

17 Ekim 2026 · tetik: `arsiv/teshis/rakipler_k244_2026-10-14/G1p.txt`.
OLSRv2 ve Babel tohum 1001'de, ikisi de hayalet açılmadan 47 s sonra
"tespit" ediyor. Babel'in temiz evresinde hiç kopma beyanı yok (ortalama ve
varyans 0). Kuyruğun kuralı (`rakipler_k244_2026-10-14/beklenti.md` §3):
*"yeni bir protokol yüzünden kalırsa sebep ölçülür ve yürütücüye
bildirilir."* Ölçüt `beklenti.md`de.

G1-P'nin yapılandırmasıyla (`evre_metrikleri_kapilari._g1p_is`: kol
`evre_kapi_p`, `statik-yok`, yere toplama, tam pencere) dört protokol tohum
1001'de koşar; her kopma beyanı düğüm, komşu ve zamanla yazılır, M4'ün iç
sayıları (temiz ortalama ve varyans, eşik, tespit penceresindeki sayı)
yeniden hesaplanır.

    KOK=<donmuş kopya> py -3.11 -u arsiv/teshis/g1p_k244_2026-10-17/teshis.py
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

PROTOKOLLER = ("aodv", "olsrv2", "babel", "desparete")
TOHUM = 1001
# G1-P kaydı (`G1p.txt`): tespit (açılmadan sonra, s), temiz ortalama, varyans.
KAYIT = {"aodv": (None, 22.25), "olsrv2": (47.0, 3.54),
         "babel": (47.0, 0.0), "desparete": (None, 2.35)}


def _kos(protokol: str) -> dict:
    t0 = time.perf_counter()
    from kalibrasyon import dunya_secimi as DS
    from kalibrasyon.aodv_uygunluk import _fabrika
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.kurulum import kurulum_yap
    from sim2.olcum.evre import ALFA, Evreler, _negatif_binom_esigi
    kfg = DS.konfig(kol="evre_kapi_p", senaryo="statik-yok", tohum=TOHUM,
                    trafik_deseni="yere_toplama")
    kur = kurulum_yap(kfg)
    Kosu(kur, _fabrika(protokol, kfg)).kostur()
    bas, bitis = kfg.olcum_penceresi
    acilma = kfg.karistirici_baslangic_s
    e = Evreler(kur.paket_defteri, bas, acilma, bitis)
    rd = kur.rota_defteri
    sirali = sorted(rd.beyan_anlari("kopma"))
    ort, var = e._kova_momentleri(sirali)
    son = e.bitis_s if e.cizelge is None else min(
        e.acilma_s + e.cizelge[0], e.bitis_s)
    taranan = max(int((son - e.acilma_s) / e.izgara_s), 1)
    esik = _negatif_binom_esigi(ort, var, ALFA / taranan)
    tespit = e.tespit_gecikmesi(rd)
    kopmalar = [(o.t_s, o.dugum, o.komsu) for o in rd._olaylar
                if o.tip == "kopma"]
    return {"protokol": protokol, "bas": bas, "acilma": acilma,
            "bitis": bitis, "izgara": e.izgara_s, "taranan": taranan,
            "ort": ort, "var": var, "esik": esik, "tespit": tespit,
            "beyan_etmiyor": rd.beyan_etmiyor, "kopmalar": kopmalar,
            "fiziksel_kopma": rd._fiziksel_kopma,
            "sure_s": time.perf_counter() - t0}


def _analiz(kayitlar: dict) -> None:
    print()
    hata = False
    for p in PROTOKOLLER:
        x = kayitlar[p]
        k_tespit, k_ort = KAYIT[p]
        ayni = (x["tespit"] == k_tespit and abs(x["ort"] - k_ort) < 0.01)
        hata |= not ayni
        temiz = [k for k in x["kopmalar"] if x["bas"] <= k[0] < x["acilma"]]
        print(f"  {p:<10} açılma {x['acilma']:.0f} s · tespit {x['tespit']} "
              f"(kayıt {k_tespit}, {'aynı' if ayni else 'FARKLI'}) · temiz "
              f"ort {x['ort']:.2f} var {x['var']:.2f} · eşik {x['esik']} "
              f"(taranan {x['taranan']}) · temizde kopma {len(temiz)} · "
              f"toplam kopma {len(x['kopmalar'])} · fiziksel kopma "
              f"{x['fiziksel_kopma']}")
        if x["tespit"] is not None:
            t = x["acilma"] + x["tespit"]
            pencere = [k for k in x["kopmalar"] if t - 1 <= k[0] < t]
            print(f"      tespit penceresi [{t - 1:.0f}; {t:.0f}) s: "
                  f"{len(pencere)} beyan > eşik {x['esik']} · "
                  + ", ".join(f"{d}→{n} @{s:.3f}" for s, d, n in pencere))
    # Ortak olay: OLSRv2 ve Babel'in tespit penceresi çevresinde (±2 s)
    # beyan ettiği bağlar, yönsüz çift olarak.
    o, b = kayitlar["olsrv2"], kayitlar["babel"]
    if o["tespit"] is not None and b["tespit"] is not None:
        t = o["acilma"] + o["tespit"]

        def baglar(x):
            return {frozenset((d, n)) for s, d, n in x["kopmalar"]
                    if n is not None and t - 3 <= s < t + 1}
        ob, bb = baglar(o), baglar(b)
        print(f"\n  [{t - 3:.0f}; {t + 1:.0f}) s yönsüz bağlar · OLSRv2 "
              f"{sorted(tuple(sorted(x)) for x in ob)} · Babel "
              f"{sorted(tuple(sorted(x)) for x in bb)} · ortak "
              f"{sorted(tuple(sorted(x)) for x in ob & bb)}")
        for p in ("aodv", "desparete"):
            x = kayitlar[p]
            yakin = [(round(s, 3), d, n) for s, d, n in x["kopmalar"]
                     if t - 3 <= s < t + 1]
            print(f"  {p:<10} aynı aralıkta kopma beyanı: {len(yakin)} · "
                  f"ortak bağlar "
                  f"{sorted(tuple(sorted((d, n))) for _s, d, n in yakin if n is not None and frozenset((d, n)) in ob | bb)}")
    print("\nKİMLİK: " + ("tuttu" if not hata else "TUTMADI"))


def main() -> int:
    kayit = BURA / "teshis.jsonl"
    with Pool(len(PROTOKOLLER)) as havuz:
        sonuc = havuz.map(_kos, PROTOKOLLER, chunksize=1)
    with kayit.open("w", encoding="utf-8") as f:
        for x in sonuc:
            f.write(json.dumps(x) + "\n")
    for x in sonuc:
        print(f"  {x['protokol']:<10} {x['sure_s'] / 60:.0f} dk", flush=True)
    _analiz({x["protokol"]: x for x in sonuc})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
