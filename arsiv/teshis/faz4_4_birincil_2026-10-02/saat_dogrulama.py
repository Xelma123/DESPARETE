"""Yamalı AODV saat ofsetine karşı değişmez mi? (K-214 önerisinin sınaması)

    TESHIS_KOK=<yamali kopya> PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
        py -3.11 -u arsiv/teshis/faz4_4_birincil_2026-10-02/saat_dogrulama.py

`protokol_tarama.txt`te ofset AODV ve AOMDV'yi bazı tohumlarda oynattı
(1001 · 1003 · 1000), OLSR'ı hiç oynatmadı. Aday sebep: başlangıç durumunun
yerel saatin 0 anına çapalı olması (`saat_cekirdegi_yama.py`).
Ölçüt (ölçmeden): yamalı kopyada AODV ve AOMDV, tohum 1001 ve 1003'te, ofset
aralığı 0,25 · 0,5 · 1,0 s için İZ BİREBİR aynı → sebep bulundu. Değilse
başka bir yerel saat bağımlılığı var, aranır.
"""
import os
import pathlib
import sys
from multiprocessing import Pool

KOK = pathlib.Path(os.environ["TESHIS_KOK"])
for yol in (KOK, KOK / "tests2"):
    sys.path.insert(0, str(yol))
os.environ["DESPARETE_DUNYA"] = "referans_2026"

from kalibrasyon import dunya_secimi as DS  # noqa: E402
from kalibrasyon import duyarlilik as D  # noqa: E402
from kalibrasyon.regresyon_satirlari import _fabrika  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.olcum.metrikler import metrik_sozlugu  # noqa: E402

GOREVLER = [(p, o, t) for p in ("aodv", "aomdv") for t in (1001, 1003)
            for o in (0.25, 0.5, 1.0)]


def _is(gorev):
    protokol, ofset, tohum = gorev
    kfg = DS.konfig(kol="saat_dogrulama", senaryo="formasyon-surekli",
                    tohum=tohum, saat_ofset_araligi_s=ofset,
                    **{**D.PENCERE, **D.HUCRE_EKLERI["birincil"]})
    kur = kurulum_yap(kfg)
    Kosu(kur, _fabrika(protokol, kur)).kostur()
    s = metrik_sozlugu(kur.sayaclar.disa_ver(), kur.paket_defteri,
                       kur.rota_defteri)
    say = kur.sayaclar
    return gorev, s["pdr_pencere"], (int(say.oku("teslim_paket")),
                                     int(say.oku("mac_deneme")),
                                     int(say.oku("kontrol_cerceve")),
                                     repr(s["gecikme_ort_s_pencere"]))


def main() -> None:
    print(f"kopya: {KOK}")
    with Pool(8) as havuz:
        ham = havuz.map(_is, GOREVLER, chunksize=1)
    iz = {}
    for gorev, pdr, z in ham:
        iz[gorev] = z
        print(f"  {gorev[0]:6} ofset {gorev[1]:4} tohum {gorev[2]}  pdr {pdr:.4f}  iz {z[:3]}")
    hepsi = True
    for p in ("aodv", "aomdv"):
        for t in (1001, 1003):
            ayni = len({iz[(p, o, t)] for o in (0.25, 0.5, 1.0)}) == 1
            hepsi &= ayni
            print(f"  {p:6} {t}: {'BIREBIR' if ayni else 'FARKLI'}")
    print("🟢 sebep bulundu — ofsete degismez" if hepsi
          else "🔴 baska bir yerel saat bagimliligi var")


if __name__ == "__main__":
    main()
