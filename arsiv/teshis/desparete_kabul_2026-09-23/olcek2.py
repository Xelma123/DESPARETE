# ⚠️ K-166 (bağımsız denetim Y-6): bu betik DESPARETE'nin profilini TAM
# vermez; kayıttaki sayılar O GÜNÜN varsayılanıyla üretildi. O gün seçenek
# yoktu (bugünkü karşılığı `secenekler=SECENEK_YOK`); bayraklar ve komut
# alanları kaydın tarihine göre (K-159'a kadar v0.1 = `PROFIL_V01` ve
# `komut_alanlari=True`; K-160 §12'den sonra `komut_alanlari=False`; K-161'den
# sonra `PROFIL_V02`; postür K-158'den önce yoktu). Bugünkü varsayılan v0.3:
# betik DEĞİŞTİRİLMEDEN koşulursa kayıttaki sayıyı ÜRETMEZ (denetçi ölçtü:
# K-157 §6'nın bir satırı bugün 0,766 · 0,380; o günün profiliyle 0,829 ·
# 2,168 birebir). Yeniden üretmek için profili açıkça ver.
"""K-160 §8 — maliyet bandı çalkantısı (c) ve komut alanları (d) hipotezleri.

Üretici: PYTHONIOENCODING=utf-8 python arsiv/teshis/desparete_kabul_2026-09-23/olcek2.py
`olcek.py` ile aynı dünya (N = 40, yere toplama, `statik-yok`, 60 s,
tohum 1000). Bir SONUÇ değil: iki yeni hipotezin sınaması.
"""
import sys
import time
from multiprocessing import Pool

sys.path.insert(0, ".")

PENCERE = {"isinma_s": 10.0, "olcum_bitis_s": 50.0, "kosu_bitis_s": 60.0}
KAPALI_MALIYET = {"risk_maliyeti": False, "kalite_maliyeti": False}
VARYANTLAR = (
    ("risk_kalite_yok", KAPALI_MALIYET, {}),
    ("risk_yok", {"risk_maliyeti": False}, {}),
    ("kalite_yok", {"kalite_maliyeti": False}, {}),
    ("risk_kalite_onarim_edinimi_yok",
     {**KAPALI_MALIYET, "onarim_edinimi": False}, {}),
    ("komut_yok", {}, {"komut_akis_sayisi": 0}),
    ("komut_yok_risk_kalite_yok", KAPALI_MALIYET, {"komut_akis_sayisi": 0}),
    ("komut_yok_hepsi_kapali", "hepsi", {"komut_akis_sayisi": 0}),
    ("komut_yok_kahin", None, {"komut_akis_sayisi": 0}),
)


def kos(is_):
    ad, bayrak, konfig_ek = is_
    from kalibrasyon.kahin import EnGuvenilirKahin, KanalGrafigi
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_alan import FORWARDABLE
    from protokoller.desparete_bayrak import TUMU_KAPALI, Bayraklar
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.kurulum import kurulum_yap
    from sim2.kosum.sonuc import sonuc_satiri
    from sim2.yapilandirma.konfig import Konfig
    kfg = Konfig(kol="u1", senaryo="statik-yok", tohum=1000,
                 trafik_deseni="yere_toplama", **konfig_ek, **PENCERE)
    t0 = time.perf_counter()
    kur = kurulum_yap(kfg)
    if bayrak is None:
        grafik = KanalGrafigi(kur)
        kosu = Kosu(kur, lambda i: EnGuvenilirKahin(i, grafik))
    else:
        b = TUMU_KAPALI if bayrak == "hepsi" else Bayraklar(**bayrak)
        kosu = Kosu(kur, lambda i: DESPARETE(i, kfg.gecit, bayraklar=b))
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "u1")
    m, kor = satir["metrikler"], satir["korunum"]
    cikti = {"pdr": m["pdr"], "uretilen": kor.get("uretilen"),
             "kontrol_airtime_s": round(m.get("kontrol_airtime_s") or 0, 1),
             "veri_airtime_s": round(m.get("veri_airtime_s") or 0, 1),
             "dusen": kor.get("dusen")}
    kd = satir["teshis"].get("kontrol_duzlemi")
    if kd is not None:
        cikti["bicim_cerceve"] = {a: b["cerceve"]
                                  for a, b in kd["bicim"]["tum"].items()}
    if bayrak is not None:
        p = [d.protokol for d in kosu.dugumler]
        g = kfg.gecit
        cikti["gecit_alani_iletilebilir"] = (
            f"{sum(1 for q in p if q.kimlik != g and q.alanlar.durum(g) == FORWARDABLE)}"
            f"/{len(p) - 1}")
        cikti["ardil_degisti"] = sum(q.alanlar.sayac["ardil_degisti"]
                                     for q in p)
        cikti["onarima_girdi"] = sum(q.alanlar.sayac["onarima_girdi"]
                                     for q in p)
        cikti["gecis_expired"] = sum(q.komsular.sayac["gecis_expired"]
                                     for q in p)
    return ad, cikti, time.perf_counter() - t0


if __name__ == "__main__":
    with Pool(8) as havuz:
        sonuc = havuz.map(kos, VARYANTLAR, chunksize=1)
    for ad, c, sure in sonuc:
        print(f"== {ad} · {sure:.0f} s", flush=True)
        for k, v in c.items():
            print(f"   {k}: {v}")
