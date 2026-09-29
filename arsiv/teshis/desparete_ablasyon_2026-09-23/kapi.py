# ⚠️ K-166 (bağımsız denetim Y-6): bu betik DESPARETE'nin profilini TAM
# vermez; kayıttaki sayılar O GÜNÜN varsayılanıyla üretildi. O gün seçenek
# yoktu (bugünkü karşılığı `secenekler=SECENEK_YOK`); bayraklar ve komut
# alanları kaydın tarihine göre (K-159'a kadar v0.1 = `PROFIL_V01` ve
# `komut_alanlari=True`; K-160 §12'den sonra `komut_alanlari=False`; K-161'den
# sonra `PROFIL_V02`; postür K-158'den önce yoktu). Bugünkü varsayılan v0.3:
# betik DEĞİŞTİRİLMEDEN koşulursa kayıttaki sayıyı ÜRETMEZ (denetçi ölçtü:
# K-157 §6'nın bir satırı bugün 0,766 · 0,380; o günün profiliyle 0,829 ·
# 2,168 birebir). Yeniden üretmek için profili açıkça ver.
"""K-159 §2 — ablasyon bayraklarının mekanizma kapısı.

Üretici: PYTHONIOENCODING=utf-8 python arsiv/teshis/desparete_ablasyon_2026-09-23/kapi.py
Küçük dünya (14 düğüm), yere toplama, 30 s, tohum 1000; her senaryoda
hepsi açık + sekiz tekli kapalı + hepsi kapalı. HER KANCADAN SONRA döngü ve
FD denetimi (`tests2/test_desparete.py::_desparete_kos_denetimli`).
Bir SONUÇ değil: bayrağın gerçekten kendi mekanizmasını kapattığını ve
açıkken mekanizmanın bu dünyada işleyip işlemediğini gösterir.
"""
import sys
import time
from multiprocessing import Pool

sys.path.insert(0, ".")
sys.path.insert(0, "tests2")

SENARYOLAR = ("statik-yok", "bagimsiz-surekli")
# bayrak → (sayaç grubu, sayaç adı)
SAYAC = {
    "risk_maliyeti": ("protokol", "epoch_risk_cezali"),
    "kalite_maliyeti": ("protokol", "epoch_kalite_cezali"),
    "postur": ("politika", "caution_girdi"),
    "bosta_sondalama": ("komsu", "probe_bosta"),
    "onarim_tamponu": ("protokol", "tampon_alinan"),
    "onarim_edinimi": ("protokol", "edinim_onarim"),
    "ilan_korumasi": ("protokol", "edinim_koruma"),
    "yeniden_edinim": ("protokol", "edinim_yeniden"),
}


def kos(is_):
    senaryo, kapali = is_
    from test_desparete import _desparete_kos_denetimli
    from protokoller.desparete_bayrak import TUMU_KAPALI, Bayraklar
    if kapali == "hepsi":
        b = TUMU_KAPALI
    elif kapali is None:
        b = None
    else:
        b = Bayraklar(**{kapali: False})
    t0 = time.perf_counter()
    _kfg, kosu, satir, ihlal = _desparete_kos_denetimli(senaryo, 30.0, b)
    m = satir["metrikler"]
    p = [d.protokol for d in kosu.dugumler]
    grup = {"protokol": lambda q: q._sayac,
            "politika": lambda q: q.politika.sayac,
            "komsu": lambda q: q.komsular.sayac}
    sayac = {bayrak: sum(grup[g](q)[ad] for q in p)
             for bayrak, (g, ad) in SAYAC.items()}
    bayrak_satir = {tuple(te["bayraklar"]) for te in satir["teshis"]["dugum"]}
    return (senaryo, kapali or "yok", satir["korunum"]["gecerli"], ihlal,
            m["pdr_pencere"], m["nrl_bayt_pencere"], sayac, bayrak_satir,
            time.perf_counter() - t0)


if __name__ == "__main__":
    from protokoller.desparete_bayrak import Bayraklar
    isler = [(s, k) for s in SENARYOLAR
             for k in (None, *Bayraklar.adlar(), "hepsi")]
    with Pool(8) as havuz:
        sonuc = havuz.map(kos, isler)
    for (s, k, gecerli, ihlal, pdr, nrl, sayac, bs, sure) in sonuc:
        print(f"{s:17} kapali={k:16} gecerli {gecerli} · pdr {pdr:.3f} · "
              f"nrl {nrl:.3f} · denetim {ihlal['denetim']} · dongu "
              f"{ihlal['dongu']} · fd_artti {ihlal['fd_artti']} · "
              f"satirdaki bayrak kumeleri {len(bs)} · {sure:.0f} s",
              flush=True)
        print("    " + " · ".join(f"{b} {v}" for b, v in sayac.items()))
