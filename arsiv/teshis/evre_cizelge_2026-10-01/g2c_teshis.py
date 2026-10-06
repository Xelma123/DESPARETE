"""G2ç kaldı — kâhin sessizde neden önceki düzeye dönmüyor? (tohum 1004)

    PYTHONIOENCODING=utf-8 py -3.11 -u arsiv/teshis/evre_cizelge_2026-10-01/g2c_teshis.py <senaryo> [tehdit]

Kâhinle bir koşu; çizelgeli evre sözlüğünün TAMAMI basılır (çevrim başına
açık/sessiz PDR, katlanmış 1 s profili, sızıntı). Karıştırıcısız kolda çizelge
hayalettir. Ayırt edilecek: sessizin başında geçici bir çukur (kuyruk
birikimi) mi, yoksa bütün sessiz dönemlerde düz bir kayma (zaman kayması) mı.
"""
import json
import os
import pathlib
import sys

KOK = pathlib.Path(os.environ.get("TESHIS_KOK")
                   or pathlib.Path(__file__).resolve().parents[3])
sys.path.insert(0, str(KOK))
os.environ["DESPARETE_DUNYA"] = "referans_2026"

from kalibrasyon import dunya_secimi as DS  # noqa: E402
from kalibrasyon.kahin import EnGuvenilirKahin, KanalGrafigi  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.kosum.sonuc import karistirici_cizelgesi  # noqa: E402
from sim2.olcum.evre import evre_sozlugu  # noqa: E402
from sim2.olcum.metrikler import yuzdelik  # noqa: E402

SENARYO = sys.argv[1]
EK = {"tehdit_senaryosu": sys.argv[2]} if len(sys.argv) > 2 else {}
kfg = DS.konfig(kol="evre_kapi_c", senaryo=SENARYO, tohum=1004,
                trafik_deseni="yere_toplama", **EK)
kur = kurulum_yap(kfg)
grafik = KanalGrafigi(kur)
Kosu(kur, lambda i: EnGuvenilirKahin(i, grafik)).kostur()
cizelge = karistirici_cizelgesi(kur) or (kfg.tehdit_acik_s, kfg.tehdit_sessiz_s)
bas, bitis = kfg.olcum_penceresi
s = evre_sozlugu(kur.paket_defteri, kur.rota_defteri, bas_s=bas,
                 acilma_s=kfg.karistirici_baslangic_s, bitis_s=bitis,
                 gecikme_p99_s=yuzdelik(kur.paket_defteri.gecikmeler(True), 99),
                 cizelge=cizelge)
print(f"{SENARYO} {EK} · cizelge {cizelge} · hayalet {karistirici_cizelgesi(kur) is None}")
for k in ("pdr_temiz", "pdr_acik", "pdr_sessiz", "sok_derinligi",
          "toparlanma_tamligi", "evre_sizinti", "bulaniklik_orani_evre"):
    print(f"  {k}: {s.get(k)}")
print("  cevrim [acik, sessiz]:", json.dumps([[None if x is None else round(x, 3) for x in c]
                                               for c in s["evre_cevrim_pdr"]]))
print("  katli profil (0-14 acik, 15-29 sessiz):",
      json.dumps([None if x is None else round(x, 3) for x in s["evre_katli_profil"]]))
