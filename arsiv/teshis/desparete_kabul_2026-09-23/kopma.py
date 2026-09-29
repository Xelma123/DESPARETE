# ⚠️ K-166 (bağımsız denetim Y-6): bu betik DESPARETE'nin profilini TAM
# vermez; kayıttaki sayılar O GÜNÜN varsayılanıyla üretildi. O gün seçenek
# yoktu (bugünkü karşılığı `secenekler=SECENEK_YOK`); bayraklar ve komut
# alanları kaydın tarihine göre (K-159'a kadar v0.1 = `PROFIL_V01` ve
# `komut_alanlari=True`; K-160 §12'den sonra `komut_alanlari=False`; K-161'den
# sonra `PROFIL_V02`; postür K-158'den önce yoktu). Bugünkü varsayılan v0.3:
# betik DEĞİŞTİRİLMEDEN koşulursa kayıttaki sayıyı ÜRETMEZ (denetçi ölçtü:
# K-157 §6'nın bir satırı bugün 0,766 · 0,380; o günün profiliyle 0,829 ·
# 2,168 birebir). Yeniden üretmek için profili açıkça ver.
"""K-160 §2 — kopma beyanı düzeltmesinin önce/sonra ölçümü.

Üretici: PYTHONIOENCODING=utf-8 python arsiv/teshis/desparete_kabul_2026-09-23/kopma.py <etiket>
Küçük dünya (14 düğüm), yere toplama, 30 s, tohum 1000 — K-156…K-159 ile
aynı koşu. Beyan yönlendirmeyi değiştirmez; ölçülen: teslim ve ek yük
BİREBİR mi, kopma sayaçları ne kadar değişti.
"""
import sys
from multiprocessing import Pool

sys.path.insert(0, ".")
sys.path.insert(0, "tests2")


def kos(senaryo):
    from test_kosum import _konfig
    from protokoller.desparete import DESPARETE
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.kurulum import kurulum_yap
    from sim2.kosum.sonuc import sonuc_satiri
    kfg = _konfig(senaryo, 1000, 30.0, trafik_deseni="yere_toplama")
    kur = kurulum_yap(kfg)
    kosu = Kosu(kur, lambda i: DESPARETE(i, kfg.gecit))
    kosu.kostur()
    m = sonuc_satiri(kur, kosu.dugumler, "desparete")["metrikler"]
    return senaryo, {ad: m.get(ad) for ad in (
        "pdr_pencere", "nrl_bayt_pencere", "kontrol_cerceve",
        "kopma_algilanan", "rota_etkilendi", "rota_kurtarildi")}


if __name__ == "__main__":
    etiket = sys.argv[1] if len(sys.argv) > 1 else "?"
    with Pool(2) as havuz:
        for senaryo, m in havuz.map(kos, ("statik-yok", "bagimsiz-surekli")):
            print(f"{etiket} {senaryo:17} " + " · ".join(
                f"{k} {v:.4f}" if isinstance(v, float) else f"{k} {v}"
                for k, v in m.items()), flush=True)
