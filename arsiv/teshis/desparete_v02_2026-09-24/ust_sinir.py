# ⚠️ K-166 (bağımsız denetim Y-6): bu betik DESPARETE'nin profilini TAM
# vermez; kayıttaki sayılar O GÜNÜN varsayılanıyla üretildi. O gün seçenek
# yoktu (bugünkü karşılığı `secenekler=SECENEK_YOK`); bayraklar ve komut
# alanları kaydın tarihine göre (K-159'a kadar v0.1 = `PROFIL_V01` ve
# `komut_alanlari=True`; K-160 §12'den sonra `komut_alanlari=False`; K-161'den
# sonra `PROFIL_V02`; postür K-158'den önce yoktu). Bugünkü varsayılan v0.3:
# betik DEĞİŞTİRİLMEDEN koşulursa kayıttaki sayıyı ÜRETMEZ (denetçi ölçtü:
# K-157 §6'nın bir satırı bugün 0,766 · 0,380; o günün profiliyle 0,829 ·
# 2,168 birebir). Yeniden üretmek için profili açıkça ver.
"""K-161 §2 — yük azaltmanın üst sınırı ve PROBE_REPLY fazlalığı.

Üretici: PYTHONIOENCODING=utf-8 python arsiv/teshis/desparete_v02_2026-09-24/ust_sinir.py
Tam ölçek (N = 40), yere toplama, C (yalnız geçit alanı), 40 s (ısınma 10 ·
ölçüm 35), tohum 1000. Bir SONUÇ değil: v0.2 adaylarının beklentisini
kurmak için üst sınır ölçümü.
"""
import sys
import time
from multiprocessing import Pool

sys.path.insert(0, ".")

PENCERE = {"isinma_s": 10.0, "olcum_bitis_s": 35.0, "kosu_bitis_s": 40.0}
UCLU = {"bosta_sondalama": False, "onarim_edinimi": False,
        "ilan_korumasi": False}
DORTLU = {**UCLU, "postur": False}
ISLER = (
    ("bagimsiz-yok", "uclu", UCLU),
    ("bagimsiz-yok", "dortlu", DORTLU),
    ("formasyon-yok", "varsayilan", {}),
    ("formasyon-yok", "uclu", UCLU),
    ("gorev-yok", "uclu", UCLU),
    ("statik-yok", "varsayilan", {}),
    ("statik-yok", "uclu", UCLU),
    ("statik-yok", "dortlu", DORTLU),
)


def kos(is_):
    senaryo, ad, bayrak = is_
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_bayrak import Bayraklar
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.kurulum import kurulum_yap
    from sim2.kosum.sonuc import sonuc_satiri
    from sim2.yapilandirma.konfig import Konfig
    kfg = Konfig(kol="u1", senaryo=senaryo, tohum=1000,
                 trafik_deseni="yere_toplama", **PENCERE)
    t0 = time.perf_counter()
    kur = kurulum_yap(kfg)
    b = Bayraklar(**bayrak)
    kosu = Kosu(kur, lambda i: DESPARETE(i, kfg.gecit, bayraklar=b))
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "u1")
    m, kor = satir["metrikler"], satir["korunum"]
    p = [d.protokol for d in kosu.dugumler]
    kd = satir["teshis"]["kontrol_duzlemi"]
    komsu = {a: sum(q.komsular.sayac[a] for q in p) for a in (
        "yanit_eslesen", "yanit_fazla", "yanit_eslesmeyen", "probe_nitelik",
        "probe_bosta", "probe_hata", "probe_dogrulama", "gecis_expired")}
    return (senaryo, ad, {
        "pdr": m["pdr"],
        "kontrol_airtime_s": round(m.get("kontrol_airtime_s") or 0, 1),
        "veri_airtime_s": round(m.get("veri_airtime_s") or 0, 1),
        "dusen": kor.get("dusen"),
        "bicim_cerceve": {a: b["cerceve"]
                          for a, b in kd["bicim"]["tum"].items()},
        "komsu": komsu}, time.perf_counter() - t0)


if __name__ == "__main__":
    with Pool(8) as havuz:
        sonuc = havuz.map(kos, ISLER, chunksize=1)
    for senaryo, ad, c, sure in sonuc:
        print(f"== {senaryo} · {ad} · {sure:.0f} s", flush=True)
        for k, v in c.items():
            print(f"   {k}: {v}")
