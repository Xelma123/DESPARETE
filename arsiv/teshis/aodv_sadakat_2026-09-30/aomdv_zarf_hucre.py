"""K-192 (b) · AOMDV kâhin aşımı — verilen hücrede üç kâhinin zarfı (genelleştirilmiş).

    PYTHONIOENCODING=utf-8 py -3.11 -u arsiv/teshis/aodv_sadakat_2026-09-30/aomdv_zarf_hucre.py <desen> <kol> <tohum> <aomdv_pdr> <etx_pdr>


Hücre: referans dünya · eşler arası · formasyon-yok · tohum 1000 · tam pencere,
U1'in konfigürasyonuyla birebir (`aodv_uygunluk._is`). AOMDV 0,9777 · ETX kâhini
0,9762 (+0,0015). Karar kuralı (ölçmeden önce, `beklenti.md`): AOMDV ≤ zarf ise
"ETX kâhini bu hücrede üst sınır değil" beyanı, U1-U geçer; AOMDV > zarf ise
yazılım hatası aranır. Kâhinler `ust_referans.py`deki üçlü.

    PYTHONIOENCODING=utf-8 py -3.11 -u arsiv/teshis/faz4_4_2026-09-30/aomdv_zarf.py
"""
import os
import pathlib
import sys
from multiprocessing import Pool

# Dondurulmuş kopyadan koşmak için `ZARF_KOK=<kopya>`.
KOK = pathlib.Path(os.environ.get("ZARF_KOK") or pathlib.Path(__file__).resolve().parents[3])
sys.path.insert(0, str(KOK))
os.environ["DESPARETE_DUNYA"] = "referans_2026"
DESEN, KOL, TOHUM = sys.argv[1], sys.argv[2], int(sys.argv[3])
AOMDV_PDR, ETX_PDR = float(sys.argv[4]), float(sys.argv[5])


def _kos(kahin: str):
    from kalibrasyon import dunya_secimi as DS
    from kalibrasyon.kahin import KanalGrafigi
    from kalibrasyon.ust_referans import KAHINLER, TeslimGrafigi
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.kurulum import kurulum_yap
    from sim2.kosum.sonuc import sonuc_satiri
    kfg = DS.konfig(kol="u1", senaryo=KOL, tohum=TOHUM, trafik_deseni=DESEN)
    kur = kurulum_yap(kfg)
    tip = KAHINLER[kahin]
    grafik = (TeslimGrafigi(kur) if kahin == "en_olasi_teslim_kahin"
              else KanalGrafigi(kur))
    kosu = Kosu(kur, lambda i: tip(i, grafik))
    kosu.kostur()
    m = sonuc_satiri(kur, kosu.dugumler, "u1")["metrikler"]
    return kahin, m["pdr"]


if __name__ == "__main__":
    from kalibrasyon.ust_referans import KAHINLER
    with Pool(3) as havuz:
        sonuc = dict(havuz.map(_kos, sorted(KAHINLER)))
    for k, p in sorted(sonuc.items()):
        print(f"  {k:<24} PDR {p:.4f}")
    zarf = max(sonuc.values())
    print(f"  {DESEN} {KOL} {TOHUM}")
    print(f"  zarf {zarf:.4f} · AOMDV {AOMDV_PDR:.4f} · ETX (U1) {ETX_PDR:.4f}")
    print("  🟢 AOMDV zarfın içinde — ETX kâhini bu hücrede üst sınır değil"
          if AOMDV_PDR <= zarf else
          "  🔴 AOMDV zarfı da aşıyor — yazılım hatası aranır (K-192 b)")
