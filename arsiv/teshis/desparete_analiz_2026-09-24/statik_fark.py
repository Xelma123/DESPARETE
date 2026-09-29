"""K-163 §4 — V1+V5+V7'nin statik koldaki PDR düşüşünün sebebi.

Üretici: PYTHONIOENCODING=utf-8 python arsiv/teshis/desparete_analiz_2026-09-24/statik_fark.py
Tam ölçek, `statik-yok`, 40 s (K-161 §6 penceresi), tohum 1000–1002;
v0.2 ve v0.2 + V1 + V5 + V7 — düşme sebepleri, gecikme, başlangıç kaybı
(ilk 5 s'de doğan paketlerin teslimi), kontrol çerçeveleri. Ayrıca
hareketli kollar için aynı pencerede v0.2'nin gecikmesi (tohum 1000).
"""
import sys
import time
from multiprocessing import Pool

sys.path.insert(0, ".")

PENCERE = {"isinma_s": 10.0, "olcum_bitis_s": 35.0, "kosu_bitis_s": 40.0}


def kos(is_):
    kol, tohum, secenekli = is_
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_bayrak import (PROFIL_V02, SECENEK_YOK,
                                              Secenekler)
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.kurulum import kurulum_yap
    from sim2.kosum.sonuc import sonuc_satiri
    from sim2.yapilandirma.konfig import Konfig
    s = (Secenekler(yanit_yalniz_onaysiz=True, ihtiyac_nitelik=True,
                    nitelik_olcumu=True) if secenekli else SECENEK_YOK)
    kfg = Konfig(kol="u1", senaryo=kol, tohum=tohum,
                 trafik_deseni="yere_toplama", **PENCERE)
    t0 = time.perf_counter()
    kur = kurulum_yap(kfg)
    kosu = Kosu(kur, lambda i: DESPARETE(i, kfg.gecit, bayraklar=PROFIL_V02,
                                         secenekler=s))
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "u1")
    m, kor = satir["metrikler"], satir["korunum"]
    p = [d.protokol for d in kosu.dugumler]
    bicim = satir["teshis"]["kontrol_duzlemi"]["bicim"]["tum"]
    return (kol, tohum, "V157" if secenekli else "v0.2", {
        "pdr": m["pdr"], "pdr_pencere": m["pdr_pencere"],
        "dusen": kor.get("dusen"),
        "gecikme_p50_s": m.get("gecikme_p50_s"),
        "gecikme_p95_s": m.get("gecikme_p95_s"),
        "cerceve": {a: b["cerceve"] for a, b in bicim.items()},
        "onarima_girdi": sum(q.alanlar.sayac["onarima_girdi"] for q in p),
        "ardil_degisti": sum(q.alanlar.sayac["ardil_degisti"] for q in p),
        "ort_active": round(sum(len(q.komsular.aktifler()) for q in p)
                            / len(p), 2)}, time.perf_counter() - t0)


if __name__ == "__main__":
    isler = [("statik-yok", t, v) for t in (1000, 1001, 1002)
             for v in (False, True)]
    isler += [(k, 1000, False) for k in ("bagimsiz-yok", "gorev-yok")]
    sira = sorted(isler, key=lambda g: g[0].startswith("statik"))
    with Pool(8) as havuz:
        sonuc = havuz.map(kos, sira, chunksize=1)
    for kol, tohum, ad, c, sure in sorted(sonuc, key=lambda r: r[:3]):
        print(f"== {kol} · {tohum} · {ad} · {sure:.0f} s", flush=True)
        for a, v in c.items():
            print(f"   {a}: {v}")
