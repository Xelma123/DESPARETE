"""Tek bir döngünün RREQ geçmişi (statik-yok 1002, t 52–55 s, düğüm 15 · 36).

`dongu_g2_1002.txt`in ilk örneği: 15 geçide ters rotayı (RREQ sıra 92) 36'dan
kurmuş, ama 36'nın kendi rotası 89'da kalmış. Koşu 56 s'de kesilir; olaylar
kesimden önce birebir aynıdır (üretim hash tabanlı). Simülatöre dokunmaz.
"""
import os
import pathlib
import sys

KOK = pathlib.Path(__file__).resolve().parents[4]
sys.path.insert(0, str(KOK))
os.environ["DESPARETE_DUNYA"] = "referans_2026"

from kalibrasyon import dunya_secimi as DS  # noqa: E402
from kalibrasyon.aodv_uygunluk import _fabrika  # noqa: E402
from protokoller import aodv as A  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402

DUGUMLER, HEDEF, T0, T1 = {15, 36}, 0, 52.0, 55.0
kfg = DS.konfig(kol="anatomi", senaryo="statik-yok", tohum=1002,
                trafik_deseni="yere_toplama", isinma_s=50.0,
                olcum_bitis_s=55.5, kosu_bitis_s=56.0)
kur = kurulum_yap(kfg)
asil_kontrol = A.AODV.kontrol_alindi
asil_ters = A.AODV._ters_rota


def kontrol(self, gozlem, gonderen, bicim, yuk, yayin):
    t = float(gozlem.saat_s)
    y = dict(yuk)
    if (self.kimlik in DUGUMLER and T0 <= t <= T1 and bicim == "RREQ"
            and y.get("kaynak") == HEDEF):
        once = self._rota.get(HEDEF)
        gorulmus = (y["kaynak"], y["rreq_kimlik"]) in self._gorulen_rreq
        kara = self._kara_listede(gonderen, t)
        cikti = asil_kontrol(self, gozlem, gonderen, bicim, yuk, yayin)
        sonra = self._rota.get(HEDEF)
        ilet = any(getattr(i, "bicim", None) is not None
                   and getattr(i.bicim, "ad", "") == "RREQ" for i in cikti)
        print(f"{t:9.4f} dugum {self.kimlik:>2} ← {gonderen:>2} RREQ "
              f"id {y['rreq_kimlik']} sira {y['kaynak_sira']} atlama "
              f"{y['atlama']} | tekrar {gorulmus} kara {kara} ilet {ilet} | "
              f"rota {None if once is None else (once.sonraki, once.atlama, once.hedef_sira, once.gecerli)}"
              f" → {None if sonra is None else (sonra.sonraki, sonra.atlama, sonra.hedef_sira, sonra.gecerli)}")
        return cikti
    return asil_kontrol(self, gozlem, gonderen, bicim, yuk, yayin)


A.AODV.kontrol_alindi = kontrol
try:
    Kosu(kur, _fabrika("aodv", kfg)).kostur()
finally:
    A.AODV.kontrol_alindi = asil_kontrol
