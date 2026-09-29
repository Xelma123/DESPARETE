# ⚠️ K-166 (bağımsız denetim Y-6): bu betik DESPARETE'nin profilini TAM
# vermez; kayıttaki sayılar O GÜNÜN varsayılanıyla üretildi. O gün seçenek
# yoktu (bugünkü karşılığı `secenekler=SECENEK_YOK`); bayraklar ve komut
# alanları kaydın tarihine göre (K-159'a kadar v0.1 = `PROFIL_V01` ve
# `komut_alanlari=True`; K-160 §12'den sonra `komut_alanlari=False`; K-161'den
# sonra `PROFIL_V02`; postür K-158'den önce yoktu). Bugünkü varsayılan v0.3:
# betik DEĞİŞTİRİLMEDEN koşulursa kayıttaki sayıyı ÜRETMEZ (denetçi ölçtü:
# K-157 §6'nın bir satırı bugün 0,766 · 0,380; o günün profiliyle 0,829 ·
# 2,168 birebir). Yeniden üretmek için profili açıkça ver.
"""K-160 §7 — DESPARETE'nin tam ölçekteki çöküşünün sebebi.

Üretici: PYTHONIOENCODING=utf-8 python arsiv/teshis/desparete_kabul_2026-09-23/olcek.py
Tam ölçek (N = 40), yere toplama, `statik-yok`, 60 s (ısınma 10 · ölçüm 50),
tohum 1000. Yedi DESPARETE varyantı (ablasyon bayraklarıyla, K-159) + ETX
kâhini. Ön-kayıtlı iki hipotezi (kanal boğulması · alan kurulamaması)
ayıran ölçüler basılır. Bir SONUÇ değil: sebep teşhisi.
"""
import sys
import time
from multiprocessing import Pool

sys.path.insert(0, ".")

PENCERE = {"isinma_s": 10.0, "olcum_bitis_s": 50.0, "kosu_bitis_s": 60.0}
VARYANTLAR = (
    ("varsayilan", {}),
    ("sondalama_yok", {"bosta_sondalama": False}),
    ("koruma_yok", {"ilan_korumasi": False}),
    ("postur_yok", {"postur": False}),
    ("onarim_edinimi_yok", {"onarim_edinimi": False}),
    ("uclu_yok", {"bosta_sondalama": False, "ilan_korumasi": False,
                  "postur": False}),
    ("hepsi_kapali", "hepsi"),
    ("kahin", None),
)


def kos(is_):
    ad, bayrak = is_
    from kalibrasyon.kahin import EnGuvenilirKahin, KanalGrafigi
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_alan import FORWARDABLE
    from protokoller.desparete_bayrak import TUMU_KAPALI, Bayraklar
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.kurulum import kurulum_yap
    from sim2.kosum.sonuc import sonuc_satiri
    from sim2.yapilandirma.konfig import Konfig
    kfg = Konfig(kol="u1", senaryo="statik-yok", tohum=1000,
                 trafik_deseni="yere_toplama", **PENCERE)
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
    cikti = {
        "pdr_pencere": m["pdr_pencere"], "pdr": m["pdr"],
        "kontrol_airtime_s": m.get("kontrol_airtime_s"),
        "veri_airtime_s": m.get("veri_airtime_s"),
        "mac_deneme": m.get("mac_deneme"), "mac_vazgecme": m.get("mac_vazgecme"),
        "dusme": {k: v for k, v in kor.items() if "dus" in k},
        "uretilen": kor.get("uretilen"),
    }
    kd = satir["teshis"].get("kontrol_duzlemi")
    if kd is not None:
        cikti["bicim_cerceve"] = {a: b["cerceve"]
                                  for a, b in kd["bicim"]["tum"].items()}
    if bayrak is not None:
        p = [d.protokol for d in kosu.dugumler]
        gecit = kfg.gecit
        iletilebilir = sum(1 for q in p if q.kimlik != gecit
                           and q.alanlar.durum(gecit) == FORWARDABLE)
        cikti["gecit_alani_iletilebilir"] = f"{iletilebilir}/{len(p) - 1}"
        cikti["ort_active_komsu"] = round(
            sum(len(q.komsular.aktifler()) for q in p) / len(p), 2)
        for grup, anahtarlar in (
                ("edinim", ("baslatilan", "solicit", "istek_dalgasi",
                            "basarili", "sure_doldu")),
                ("komsu", ("gecis_active", "gecis_stale", "gecis_suspect",
                           "gecis_expired", "probe_bosta", "probe_hata",
                           "probe_nitelik")),
                ("alan", ("onarima_girdi", "ulasilamaz", "ardil_degisti"))):
            kaynak = {"edinim": lambda q: q.edinim.sayac,
                      "komsu": lambda q: q.komsular.sayac,
                      "alan": lambda q: q.alanlar.sayac}[grup]
            cikti[grup] = {a: sum(kaynak(q).get(a, 0) for q in p)
                           for a in anahtarlar}
    return ad, cikti, time.perf_counter() - t0


if __name__ == "__main__":
    with Pool(8) as havuz:
        sonuc = havuz.map(kos, VARYANTLAR, chunksize=1)
    for ad, c, sure in sonuc:
        print(f"== {ad} · {sure:.0f} s", flush=True)
        for k, v in c.items():
            print(f"   {k}: {v}")
