"""Performans değişikliğinin sonucu DEĞİŞTİRMEDİĞİNİ gösterir (ajan, 28 Eylül).

Kullanım (kod kökü argümanla — eski kod dondurulmuş kopyadan, yeni kod depodan):
    python birebir.py <kod_koku> <cikti.json> [kosu_s]

Birincil hücre (formasyon · derin_sizma 10 W · yere toplama), AODV ve
DESPARETE, tohum 1003, karıştırıcı 1 s'de açılır. Tam sonuç satırının
kimlik ve zaman alanları dışındaki HER bölümü JSON'a yazılır; iki JSON
bayt bayt karşılaştırılır. Süre de yazılır.
"""
import json
import os
import sys
import time

kok, cikti = sys.argv[1], sys.argv[2]
kosu_s = float(sys.argv[3]) if len(sys.argv) > 3 else 4.0
sys.path.insert(0, kok)
os.environ["DESPARETE_DUNYA"] = "referans_2026"

from kalibrasyon import dunya_secimi as DS  # noqa: E402
from kalibrasyon.aodv_uygunluk import _fabrika  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.kosum.sonuc import sonuc_satiri  # noqa: E402

sonuc = {}
for protokol in ("aodv", "desparete"):
    kfg = DS.konfig(kol="birebir", senaryo="formasyon-surekli", tohum=1003,
                    trafik_deseni="yere_toplama",
                    tehdit_senaryosu="derin_sizma",
                    karistirici_baslangic_s=1.0, isinma_s=0.5,
                    olcum_bitis_s=kosu_s - 0.5, kosu_bitis_s=kosu_s)
    kur = kurulum_yap(kfg)
    kosu = Kosu(kur, _fabrika(protokol, kfg))
    bas = time.perf_counter()
    kosu.kostur()
    sure = time.perf_counter() - bas
    satir = sonuc_satiri(kur, kosu.dugumler, protokol)
    ozet = {b: satir[b] for b in ("metrikler", "korunum", "ham")
            if b in satir}
    sonuc[protokol] = {"sure_s": round(sure, 1), "satir": ozet,
                       "onbellek": kur.kanal.sonumleme.onbellek_raporu()}
    print(f"{protokol}: {sure:.1f} s · onbellek {sonuc[protokol]['onbellek']}")
with open(cikti, "w", encoding="utf-8") as f:
    json.dump({p: v["satir"] for p, v in sonuc.items()}, f,
              ensure_ascii=False, sort_keys=True, default=str)
