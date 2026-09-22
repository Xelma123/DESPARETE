"""GÖREV TABANLI KOLUN PARAMETRE TARAMASI.

Üretici:  PYTHONIOENCODING=utf-8 python kalibrasyon/gorev_kalibrasyonu.py

🔒 ÖLÇÜT — `sim2/yapilandirma/senaryolar.py`de, BU TARAMADAN ÖNCE ilan edildi:

    GEÇERLİLİK KOŞULU : müfreze başına en az 4 üye (40 düğüm → grup ≤ 10)
    SEÇİM             : ortalama dereceyi bağımsız kolunkiyle eşitleyen
                        (|Δderece| ≤ 0,3) adaylar arasından, tam bağlı zaman
                        oranı bağımsız kola en yakın olan

🔴 BAĞIL HIZ ve ROTA ÖMRÜ ÖLÇÜT DEĞİL, SONUÇTUR. Onlara göre ayarlamak, kolun
var oluş sebebi olan sayıyı seçmek — yani cevabı seçmek — olurdu. Bu yüzden
tabloda RAPORLANIRLAR ama seçime GİRMEZLER.
"""
from __future__ import annotations

import pathlib
import statistics as ist
import sys

KOK = pathlib.Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))
if str(KOK / "kalibrasyon") not in sys.path:
    sys.path.insert(0, str(KOK / "kalibrasyon"))

from mobilite_gercekcilik import (ADIM_S, BITIS_S, N, bagil_hizlar,  # noqa: E402
                                  bag_omurleri, rota_omurleri)
from sim2.cekirdek.rng import Akislar  # noqa: E402
from sim2.dunya.topoloji import Topoloji, topoloji_kur  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402

TOHUMLAR = range(1, 11)
DERECE_TOLERANSI = 0.3
UYE_TABANI = 4          # müfreze başına en az bu kadar üye


def _izler(top):
    adet = int(BITIS_S / ADIM_S) + 1
    return [[top.konum(i, k * ADIM_S) for k in range(adet)] for i in range(N)]


def olc(senaryo: str, **ek) -> dict:
    derece, bagli, hiz, bagomur, rotaomur, olay = [], [], [], [], [], []
    for tohum in TOHUMLAR:
        top = topoloji_kur(
            Konfig(kol="kalib", senaryo=senaryo, tohum=tohum, **ek),
            Akislar(tohum))
        seri = top.zaman_serisi(0.0, BITIS_S, 2.0)
        oz = Topoloji.baglantililik_ozeti(seri)
        derece.append(oz["ortalama_derece"])
        bagli.append(oz["tam_bagli_zaman_orani"])
        olay.append(Topoloji.bag_olaylari(seri)["kapanan"])
        iz = _izler(top)
        h = bagil_hizlar(iz)
        o = bag_omurleri(iz)
        r, _ = rota_omurleri(iz)
        hiz.append(ist.median(h) if h else float("nan"))
        bagomur.append(ist.median(o) if o else float("nan"))
        rotaomur.append(ist.median(r) if r else float("nan"))
    return dict(
        derece=ist.mean(derece),
        bagli=ist.mean(bagli),
        bagil_hiz=ist.mean(hiz),
        bag_omru=ist.mean(bagomur),
        rota_omru=(ist.mean([x for x in rotaomur if x == x])
                   if any(x == x for x in rotaomur) else float("nan")),
        rota_olculen=sum(1 for x in rotaomur if x == x),
        kapanan=ist.mean(olay),
    )


def main() -> None:
    print("=" * 78)
    print("REFERANS — BAGIMSIZ KOL  (esitlenecek hedef)")
    print("=" * 78)
    ref = olc("bagimsiz-yok")
    print(f"  ortalama derece      : {ref['derece']:.3f}   <- ESITLENECEK")
    print(f"  tam bagli zaman      : %{100*ref['bagli']:.1f}   <- YAKIN OLACAK")
    print(f"  bagil hiz (ortanca)  : {ref['bagil_hiz']:.1f} m/s   (SONUC)")
    print(f"  bag omru (ortanca)   : {ref['bag_omru']:.1f} s     (SONUC)")
    print(f"  rota omru (ortanca)  : {ref['rota_omru']:.1f} s     (SONUC)")

    print()
    print("=" * 78)
    print("TARAMA — gorev kolu")
    print("=" * 78)
    print(f"{'G':>3s} {'uye':>4s} {'rho':>5s} {'derece':>7s} {'d-fark':>7s} "
          f"{'bagli':>7s} {'bagil_hiz':>10s} {'bag_omru':>9s} {'rota':>7s} "
          f"{'gecerli':>8s}")
    adaylar = []
    for G in (4, 5, 8, 9, 10):
        for rho in (100.0, 150.0, 200.0, 250.0, 300.0):
            uye = N / G
            s = olc("gorev-yok", gorev_grup_sayisi=G,
                    gorev_grup_yaricapi_m=rho)
            fark = s["derece"] - ref["derece"]
            gecerli = (uye >= UYE_TABANI) and abs(fark) <= DERECE_TOLERANSI
            if uye >= UYE_TABANI and abs(fark) <= DERECE_TOLERANSI:
                adaylar.append((G, rho, s))
            etiket = ("ADAY" if gecerli
                      else ("uye<4" if uye < UYE_TABANI else "derece"))
            print(f"{G:3d} {uye:4.1f} {rho:5.0f} {s['derece']:7.2f} "
                  f"{fark:+7.2f} {100*s['bagli']:6.1f}% {s['bagil_hiz']:10.1f} "
                  f"{s['bag_omru']:9.1f} {s['rota_omru']:7.1f} {etiket:>8s}")

    print()
    print("=" * 78)
    print("SECIM  (ilan edilmis olcut uygulanir)")
    print("=" * 78)
    if not adaylar:
        print("  🔴 HIC ADAY YOK — olcut hicbir (G, rho) ciftini gecirmiyor.")
        print("     Bu bir SONUCTUR: bu yogunlukta koordineli hareket,")
        print("     bagimsiz kolun derecesini tutturamiyor demektir.")
        return
    G, rho, s = min(adaylar, key=lambda a: abs(a[2]["bagli"] - ref["bagli"]))
    print(f"  {len(adaylar)} aday geçerlilik koşulunu ve derece kısıtını geçti.")
    print(f"  SECILEN : grup_sayisi={G} · grup_yaricapi={rho:.0f} m "
          f"({N/G:.0f} uye/mufreze)")
    print()
    print(f"{'':22s} {'bagimsiz':>12s} {'gorev':>12s} {'oran':>8s}")
    for ad, anahtar, birim in (("ortalama derece", "derece", ""),
                               ("tam bagli zaman", "bagli", ""),
                               ("bagil hiz", "bagil_hiz", " m/s"),
                               ("bag omru", "bag_omru", " s"),
                               ("ROTA omru", "rota_omru", " s")):
        a, b = ref[anahtar], s[anahtar]
        oran = (b / a) if a else float("nan")
        print(f"  {ad:20s} {a:12.2f} {b:12.2f} {oran:7.2f}x{birim}")
    print()
    print("  🔒 Bagil hiz, bag omru ve rota omru SECIME GIRMEDI —")
    print("     ilan edilmis olcut yalniz derece ve bagliligi kullanir.")


if __name__ == "__main__":
    main()
