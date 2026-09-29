# ⚠️ K-166 (bağımsız denetim Y-6): bu betik DESPARETE'nin profilini TAM
# vermez; kayıttaki sayılar O GÜNÜN varsayılanıyla üretildi. O gün seçenek
# yoktu (bugünkü karşılığı `secenekler=SECENEK_YOK`); bayraklar ve komut
# alanları kaydın tarihine göre (K-159'a kadar v0.1 = `PROFIL_V01` ve
# `komut_alanlari=True`; K-160 §12'den sonra `komut_alanlari=False`; K-161'den
# sonra `PROFIL_V02`; postür K-158'den önce yoktu). Bugünkü varsayılan v0.3:
# betik DEĞİŞTİRİLMEDEN koşulursa kayıttaki sayıyı ÜRETMEZ (denetçi ölçtü:
# K-157 §6'nın bir satırı bugün 0,766 · 0,380; o günün profiliyle 0,829 ·
# 2,168 birebir). Yeniden üretmek için profili açıkça ver.
"""K-158 — DESPARETE 3.6 postürler, küçük dünyada.

Üretici: PYTHONIOENCODING=utf-8 python arsiv/teshis/desparete_postur_2026-09-23/ayna.py
Küçük dünya (14 düğüm), yere toplama, 30 s, tohum 1000 — K-156 §5 ve K-157
§6 ile aynı koşu. HER KANCADAN SONRA döngü ve FD denetimi
(`tests2/test_desparete.py::_desparete_kos_denetimli`). Bir SONUÇ değil:
postürün ne sıklıkla ve neden değiştiğine, bedeline bakar.
"""
import sys
import time
from multiprocessing import Pool

sys.path.insert(0, ".")
sys.path.insert(0, "tests2")


def kos(senaryo):
    from test_desparete import _desparete_kos_denetimli
    from protokoller.desparete_alan import FORWARDABLE
    from protokoller.desparete_politika import CAUTION
    t0 = time.perf_counter()
    _kfg, kosu, satir, ihlal = _desparete_kos_denetimli(senaryo, 30.0)
    m = satir["metrikler"]
    p = [d.protokol for d in kosu.dugumler]
    pol = {ad: sum(q.politika.sayac[ad] for q in p)
           for ad in p[0].politika.sayac}
    kom = {ad: sum(q.komsular.sayac[ad] for q in p)
           for ad in ("probe_dogrulama", "dogrulama_acik_oturum",
                      "probe_bosta", "probe_hata")}
    iletilebilir = caution = 0
    for q in p:
        for h, a in q.alanlar.alanlar.items():
            if a.kendi or a.durum != FORWARDABLE:
                continue
            iletilebilir += 1
            caution += q.politika.durum(h) == CAUTION
    return (senaryo, satir["korunum"]["gecerli"], ihlal, m["pdr_pencere"],
            m["nrl_bayt_pencere"], m["kontrol_cerceve"], pol, kom,
            iletilebilir, caution, time.perf_counter() - t0)


if __name__ == "__main__":
    with Pool(2) as havuz:
        for r in havuz.map(kos, ("statik-yok", "bagimsiz-surekli")):
            (senaryo, gecerli, ihlal, pdr, nrl, kc, pol, kom, il, ca,
             sure) = r
            print(f"{senaryo:17} gecerli {gecerli} · pdr_pencere {pdr:.3f} · "
                  f"nrl_bayt_pencere {nrl:.3f} · kontrol_cerceve {kc:.0f} · "
                  f"{sure:.0f} s", flush=True)
            print(f"  denetim {ihlal['denetim']} · dongu {ihlal['dongu']} · "
                  f"fd_artti {ihlal['fd_artti']}")
            print("  politika " + " · ".join(f"{k} {v}"
                                              for k, v in pol.items()))
            print("  komsu " + " · ".join(f"{k} {v}" for k, v in kom.items()))
            print(f"  sonda iletilebilir alan {il} · CAUTION'da {ca}")
