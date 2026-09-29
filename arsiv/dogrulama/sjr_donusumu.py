"""
SJR / JSR DONUSUMU — senaryolarimizi LITERATURUN para biriminde ifade eder.

🔴 NEDEN BU DOSYA VAR
=====================
`v2/yeni_detaylı_arastırma/` taramasinin iki dosyasi, karistirma siddetini
**SJR/JSR (dB)** ekseninde raporluyor:

    01_genel/SJR PDR E2E Literatür Boşluğu.md   — bosluk "degisen SJR altinda"
                                                  diye tanimli; tarama araligi
                                                  -40…+40 dB, kesme esigi -3 dB
    01_genel/10-JAMMING-GPS-SPOOFING-...md §C.2 — SJR -5/-13/-14 dB

Bu depo ise karistiriciyi **mutlak dBm** ile tanimliyor (`SENARYO_TANIMLARI`,
`karistirici_guc_override_dbm`). Iki eksen arasindaki donusum HICBIR YERDE
YAZILI DEGIL — ve o donusum olmadan Bosluk A'nin hedefledigi tablo
literaturun eksenine oturtulamaz.

🔴 DONUSUM BIR SABIT DEGIL, BIR DAGILIMDIR
===========================================
SJR alici-merkezlidir (`RF Jamming SINR-PER Soyutlama Modeli.md` §5.3): ayni
karistirici, guclu sinyal alan bir aliciyi farkli, zayif alani farkli etkiler.
Bu yuzden tek bir sayi YAZILAMAZ; menzil ici her yonlu bag icin ayri hesaplanir
ve dagilim (ortanca + %5/%95) raporlanir.

TANIMLAR — literaturden birebir
--------------------------------
    SJR_dB  = 10*log10(S_r / J_r)          (Gao & Zhi: (P_r)dBm - (J_r)dBm)
    JSR_dB  = -SJR_dB
    SINR_dB = 10*log10(S_r / (N + J_r))    (`radio.py::sinr_db` ile ayni ifade)

⚠️ BU BIR SIMULASYON KOSUSU DEGILDIR. `Kosu` calistirmaz, paket uretmez;
yalnizca URETIM YOLUNUN KENDI nesnelerini (`Topoloji`, `Radyo`, `Karistirici`)
kullanarak geometri + yayilim hesabi yapar. Bu yuzden sonuc satiri yazmaz —
yazdigi sey bir kosu sonucu degil, bir EKSEN DONUSUM TABLOSUDUR.

🔴 KAPSAMI (Y11 — koruma kendi siniriyla yazilir)

    | ne olculuyor                                   | evet/hayir  |
    | menzil ici yonlu baglarin anlik SJR dagilimi   | evet        |
    | darbeli karistiricinin TEPE anindaki hali      | evet (b ayri)|
    | hareketli karistiricinin yorunge boyu dagilimi | evet (24 faz)|
    | 🔴 MAC/kuyruk/protokol etkisi                  | HAYIR       |
    | 🔴 gercek teslim orani                          | HAYIR       |

Yani bu tablo *"bizim S2'miz literaturun hangi SJR'sine denk"* sorusunu
cevaplar; *"o SJR'de PDR ne olur"* sorusunu **cevaplamaz** — onu ancak
gercek kosu olcer.

Kullanim:
    PYTHONIOENCODING=utf-8 python dogrulama/sjr_donusumu.py
"""

from __future__ import annotations

import math
import statistics as ist
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sim.config import DIRSEK_TARAMASI_DBM, SENARYOLAR, Konfig   # noqa: E402
from sim.radio import Karistirici, Radyo, lin_to_db, w_to_dbm    # noqa: E402
from sim.rng import Akislar                                      # noqa: E402
from sim.topology import Topoloji                                # noqa: E402

# 🔴 AYARLAMA TOHUMLARI (1-30). Ana deney tohumlari (2000-2029) muhurden
# once HICBIR amacla kosulmaz — bir eksen donusumu de bir "amac"tir (K-025).
TOHUMLAR = range(1, 31)

# Hareketli karistiricinin yorungesi kac fazda ornekleniyor.
# 24 secildi: yorunge periyodu 2*pi*R/v ~ 125,7 s, yani ~5,2 s'de bir ornek —
# beacon araligindan (1 s) kaba, ama dagilimin seklini vermeye yeter.
YORUNGE_FAZ_SAYISI = 24

# Literaturun haberlesme kesme esigi (`10-JAMMING...` §C.2, Huang 2026).
LIT_KESME_SINR_DB = -3.0


def _ornek_zamanlari(kar: Karistirici | None) -> list[float]:
    """Karistiricinin hangi anlarda ornekleneceği.

    🔴 Darbeli karistiricida ACIK an secilir (tepe gucu). Kapali ani da
    orneklemek dagilima sonsuz SJR'ler sokar ve ortancayi anlamsizlastirir;
    gorev cevrimi beta AYRI raporlanir — `RF Jamming...md` §2.4'un istedigi budur.
    """
    if kar is None:
        return [0.0]
    if kar.hareketli:
        cevre = 2.0 * math.pi * kar.yorunge_yaricap_m
        periyot = cevre / kar.hiz_ms
        return [periyot * i / YORUNGE_FAZ_SAYISI
                for i in range(YORUNGE_FAZ_SAYISI)]
    if kar.darbeli:
        # Faz tohumdan cekiliyor; acik olan ilk ani ara.
        adim = kar.periyot_s / 200.0
        for i in range(200):
            if kar.acik_mi(i * adim):
                return [i * adim]
        raise RuntimeError("darbeli karistiricinin ACIK ani bulunamadi")
    return [0.0]


# 🔴 B-128 (yedinci denetim) — `_yuzdelik` GOVDESI SILINDI.
# `yuzdelik` bu depoda UC ayri govdede tanimliydi ve K-086
# *"tek govde"* diyordu — YANLISTI. Ustelik `06` §8.1'in
# tablosunu ureten govde BURADAKIYDI. Tek govde artik
# `sim/karsilastirma.py`de; buradan ICE AKTARILIYOR
# (B-07'nin "ikinci dogru kaynagi" tuzagi).
from sim.karsilastirma import yuzdelik as _yuzdelik  # noqa: E402


def olc_senaryo(senaryo: str, override_dbm: float | None = None) -> dict:
    """Bir senaryonun (ya da tarama noktasinin) SJR/SINR dagilimi."""
    ek = {} if override_dbm is None else {
        "karistirici_guc_override_dbm": override_dbm}
    ornek_kon = Konfig(kol="sjr", senaryo=senaryo, **ek)
    radyo = Radyo.kur(ornek_kon)
    gurultu_w = radyo.gurultu_gucu_w

    sjr_db: list[float] = []
    sinr_db: list[float] = []
    bag_sayisi = 0

    for tohum in TOHUMLAR:
        kon = Konfig(kol="sjr", senaryo=senaryo, tohum=tohum, **ek)
        akislar = Akislar(ana_tohum=tohum)
        topo = Topoloji.uret(kon, akislar)
        kar = Karistirici.senaryodan(kon, akislar)
        zamanlar = _ornek_zamanlari(kar)

        for j in range(topo.dugum_sayisi):
            komsular = topo.geometrik_komsular(j)
            if not komsular:
                continue
            alici_konum = topo.konumlar[j]
            for i in komsular:
                s_w = radyo.alinan_guc_w(topo.mesafe(i, j))
                bag_sayisi += 1
                for t in zamanlar:
                    j_w = 0.0 if kar is None else kar.alinan_guc_w(alici_konum, t)
                    sinr_db.append(lin_to_db(s_w / (gurultu_w + j_w)))
                    if j_w > 0.0:
                        sjr_db.append(lin_to_db(s_w / j_w))

    return {
        "senaryo": senaryo,
        "override_dbm": override_dbm,
        "karistirici_tepe_dbm": ornek_kon.karistirici_guc_dbm,
        "esdeger_sabit_dbm": ornek_kon.esdeger_sabit_guc_dbm,
        "gorev_cevrimi": (ornek_kon.darbe_gorev_cevrimi
                          if ornek_kon.karistirici_darbeli else 1.0),
        "verici_dbm": w_to_dbm(radyo.verici_gucu_w),
        # 🔴 Literaturun "jammer/IHA guc orani" ekseni (`10-JAMMING` §C.1):
        # kaynaktaki guclerin farki — geometriden BAGIMSIZ tek sayi.
        "kaynak_js_db": (None if ornek_kon.karistirici_guc_dbm is None
                         else ornek_kon.karistirici_guc_dbm
                         - w_to_dbm(radyo.verici_gucu_w)),
        "bag_orneklemi": bag_sayisi,
        "sjr_ortanca_db": ist.median(sjr_db) if sjr_db else None,
        "sjr_p05_db": _yuzdelik(sjr_db, 0.05) if sjr_db else None,
        "sjr_p95_db": _yuzdelik(sjr_db, 0.95) if sjr_db else None,
        "sinr_ortanca_db": ist.median(sinr_db) if sinr_db else None,
        "sinr_p05_db": _yuzdelik(sinr_db, 0.05) if sinr_db else None,
        "sinr_p95_db": _yuzdelik(sinr_db, 0.95) if sinr_db else None,
        # Literaturun kesme esiginin (-3 dB) altina dusen bag orani
        "lit_kesme_orani": (sum(1 for v in sinr_db if v < LIT_KESME_SINR_DB)
                            / len(sinr_db)) if sinr_db else None,
        # Bizim KENDI menzil tanimimizin esigi (10 dB) altina dusen oran
        "bizim_esik_alti_orani": (
            sum(1 for v in sinr_db if v < ornek_kon.sinr_esigi_db)
            / len(sinr_db)) if sinr_db else None,
    }


def _satir(r: dict) -> str:
    def f(x, n=2):
        return "     -" if x is None else format(x, "6." + str(n) + "f")
    ad = (r["senaryo"] if r["override_dbm"] is None
          else format(r["override_dbm"], "+.0f") + "dBm")
    return (format(ad, ">8s") + " "
            + f(r["karistirici_tepe_dbm"]) + " " + f(r["kaynak_js_db"])
            + " | " + f(r["sjr_ortanca_db"]) + " " + f(r["sjr_p05_db"])
            + " " + f(r["sjr_p95_db"])
            + " | " + f(r["sinr_ortanca_db"]) + " " + f(r["sinr_p05_db"])
            + " " + f(r["sinr_p95_db"])
            + " | " + f(r["lit_kesme_orani"], 4)
            + " " + f(r["bizim_esik_alti_orani"], 4))


def main() -> int:
    print("SJR / JSR DONUSUM TABLOSU")
    print("tohumlar: " + str(TOHUMLAR.start) + "-" + str(TOHUMLAR.stop - 1)
          + " | yorunge fazi: " + str(YORUNGE_FAZ_SAYISI)
          + " | literatur kesme esigi: " + str(LIT_KESME_SINR_DB) + " dB")
    print()
    print("   nokta tepe_dBm kayn_JS |  SJR: ortan    p05    p95 "
          "|  SINR: ortan    p05    p95 |  <-3dB   <10dB")
    print("-" * 116)

    sonuclar = []
    for sen in SENARYOLAR:
        r = olc_senaryo(sen)
        sonuclar.append(r)
        print(_satir(r))

    print()
    print("H1.2 DIRSEK TARAMASI (S2 tabaninda override — sabit senaryo)")
    print("-" * 116)
    for guc in DIRSEK_TARAMASI_DBM:
        print(_satir(olc_senaryo("S2", override_dbm=guc)))

    print()
    print("bag orneklemi (S2, 30 tohum): " + str(sonuclar[2]["bag_orneklemi"]))
    print()
    print("🔴 OKUMA NOTU: SJR yalnizca karistirici ACIKKEN tanimlidir; S0'da")
    print("   sutun bostur ve bu bir eksiklik degil, tanimin kendisidir.")
    print("   Darbeli senaryolarda (S3/S4) degerler TEPE anina aittir;")
    print("   gorev cevrimi ayri raporlanir (S3: "
          + str(sonuclar[3]["gorev_cevrimi"]) + " | S4: "
          + str(sonuclar[4]["gorev_cevrimi"]) + ").")
    return 0


if __name__ == "__main__":        # 🔴 Windows `spawn` — devir teslim §0.2
    raise SystemExit(main())
