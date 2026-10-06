"""`ttl_baslangic` taban protokollerde — birincil hücre, kısa pencere (Faz 4.4, K-213).

    TESHIS_KOK=<kopya> PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
        py -3.11 -u arsiv/teshis/faz4_4_birincil_2026-10-02/ttl_olcum.py

Neden kâhinle değil: duyarlılık aracı kâhin ikilisiyle ölçer ve kâhin döngü
yapmaz; TTL yalnız VERİ paketinin ömrünü belirler (kontrol paketlerinin TTL'i
yüktedir, `atlama_sayisi` TTL'den bağımsız türetilir), yani etkisi döngüye
giren paketlerdedir. Döngüsüz en uzun yol 9 atlama (`ttl_cap.txt`), ölçüt
≤ 8 aşıldı → doğrudan ölçülür.

Koşular: AODV · AOMDV · OLSR × TTL 16 · 32 · 64 × tohum 1000–1004 (45) +
kablo denetimi: sınav protokolü (bilerek döngülü) tohum 1004'te TTL 16 · 32 (2).
DESPARETE yok: Faz 5'te değişecek; mühürden önce regresyon satırlarının
`ttl_olumu`'ndan yeniden okunur.

Ölçüt ölçmeden (`arsiv/teshis/faz4_4_2026-09-30/beklenti.md` Sonuç 4 öncesi):
  · protokol ve çarpan başına Δ = tohum başına (PDR_ttl − PDR_32) ortalaması,
    band = 2·SD/√5;
  · BAĞLAMIYOR: beş tohumda parmak izi birebir aynı VE kablo denetiminde
    sınav protokolünün izi değişiyor → DUYARSIZ (birebir);
  · DUYARSIZ: |Δ| < R (0,0188) ve |Δ| ≤ band;
  · aksi DUYARLI → öğrenciye eksen listesi.
"""
import os
import pathlib
import statistics as ist
import sys
import time
from multiprocessing import Pool

KOK = pathlib.Path(os.environ.get("TESHIS_KOK")
                   or pathlib.Path(__file__).resolve().parents[3])
for yol in (KOK, KOK / "tests2"):
    if str(yol) not in sys.path:
        sys.path.insert(0, str(yol))
os.environ["DESPARETE_DUNYA"] = "referans_2026"

from kalibrasyon import dunya_secimi as DS  # noqa: E402
from kalibrasyon.duyarlilik import HUCRE_EKLERI, PENCERE, R_ESLESTIRILMIS  # noqa: E402
from kalibrasyon.regresyon_satirlari import _fabrika  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.olcum.metrikler import metrik_sozlugu  # noqa: E402

TOHUMLAR = (1000, 1001, 1002, 1003, 1004)
PROTOKOLLER = ("aodv", "aomdv", "olsr")
TTL = (16, 32, 64)


def _is(gorev):
    protokol, ttl, tohum = gorev
    try:
        kfg = DS.konfig(kol="ttl_olcum", senaryo="formasyon-surekli",
                        tohum=tohum, ttl_baslangic=ttl,
                        **{**PENCERE, **HUCRE_EKLERI["birincil"]})
        kur = kurulum_yap(kfg)
        Kosu(kur, _fabrika(protokol, kur)).kostur()
        s = metrik_sozlugu(kur.sayaclar.disa_ver(), kur.paket_defteri,
                           kur.rota_defteri)
        say = kur.sayaclar
        izi = (int(say.oku("teslim_paket")), int(say.oku("mac_deneme")),
               int(say.oku("kontrol_cerceve")),
               repr(s["gecikme_ort_s_pencere"]))
        return gorev, (s["pdr_pencere"], int(say.oku("ttl_olumu")), izi), None
    except Exception as hata:                       # noqa: BLE001
        return gorev, None, f"{type(hata).__name__}: {hata}"


def main() -> None:
    DS.secimi_oku(["--dunya", "referans_2026"])
    gorevler = [(p, t, s) for p in PROTOKOLLER for t in TTL for s in TOHUMLAR]
    gorevler += [("kontrol_sinav", 16, 1004), ("kontrol_sinav", 32, 1004)]
    print(f"kopya: {KOK}\ntoplam kosu {len(gorevler)} · 8 isci · R {R_ESLESTIRILMIS}")
    t0 = time.perf_counter()
    with Pool(8) as havuz:
        ham = havuz.map(_is, gorevler, chunksize=1)
    print(f"sure {(time.perf_counter() - t0) / 60:.1f} dk\n")
    sonuc = {}
    for gorev, deger, hata in ham:
        if hata:
            print("  HATA", gorev, hata)
            continue
        sonuc[gorev] = deger
        print(f"  {gorev[0]:14} ttl {gorev[1]:2} tohum {gorev[2]}  "
              f"pdr {deger[0]:.4f}  ttl_olumu {deger[1]}  iz {deger[2][:3]}")
    k16, k32 = sonuc.get(("kontrol_sinav", 16, 1004)), sonuc.get(("kontrol_sinav", 32, 1004))
    kablo = k16 is not None and k32 is not None and k16[2] != k32[2]
    print(f"\nKABLO DENETIMI (sinav protokolu 16 ↔ 32 izi farkli): {'🟢' if kablo else '🔴'}")
    print(f"{'protokol':10} {'ttl':>4} {'d_pdr':>9} {'band':>8} {'birebir':>8}  karar")
    for p in PROTOKOLLER:
        for t in (16, 64):
            d = [sonuc[(p, t, s)][0] - sonuc[(p, 32, s)][0] for s in TOHUMLAR
                 if (p, t, s) in sonuc and (p, 32, s) in sonuc]
            ayni = all(sonuc[(p, t, s)][2] == sonuc[(p, 32, s)][2] for s in TOHUMLAR
                       if (p, t, s) in sonuc and (p, 32, s) in sonuc)
            if len(d) < len(TOHUMLAR):
                print(f"{p:10} {t:>4}  eksik tohum → GECERSIZ")
                continue
            ort = ist.mean(d)
            band = 2 * ist.stdev(d) / len(d) ** 0.5
            if ayni and kablo:
                karar = "BAGLAMIYOR (DUYARSIZ, birebir)"
            elif ayni:
                karar = "OLCULEMEDI (kablo denetimi yok)"
            elif abs(ort) < R_ESLESTIRILMIS and abs(ort) <= band:
                karar = "DUYARSIZ"
            else:
                karar = "DUYARLI"
            print(f"{p:10} {t:>4} {ort:+9.4f} {band:8.4f} {str(ayni):>8}  {karar}")


if __name__ == "__main__":
    main()
