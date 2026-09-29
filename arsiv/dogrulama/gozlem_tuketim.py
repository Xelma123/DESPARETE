"""
GÖZLEM PENCERESİNİN HANGİ ALANI FİİLEN OKUNUYOR — çalışma anında.

🔴 NEDEN BU ARAÇ VAR — B-102 (ALTINCI DENETİM) VE D-12
=======================================================
`08` madde 22 *"gözlem penceresinin DOKUZ alanının hiçbir tüketicisi yok"*
diyor ve üreticisini **düzyazıyla** tarif ediyor: *"`sim/` + `dogrulama/`
altında `g.<alan>` deseni taraması"*.

Bu tarif **yeniden üretilebilir değil.** 27 Ağustos 2026'da üç farklı statik
okuyuş denendi ve **üç farklı sayı** verdi:

    naif `<önek>.<alan>`            ->  8
    yerel değişken filtresi         ->  9
    altıncı denetimin taraması      -> 11

Sebep yapısal: **isimler çakışıyor.** `PaketGorunumu.bayt` ile gerçek
`Paket.bayt`, `Gozlem.kuyruk_kapasitesi` ile `Konfig.kuyruk_kapasitesi`
aynı adı taşıyor. İsimden tüketici çıkarmak bir TAHMİNDİR ve `03` kural 1
tahmini sayı olarak sunmayı yasaklıyor.

🔒 YÖNTEM — TAHMİN DEĞİL, GÖZLEM
=================================
Üç sınıfın `__getattribute__`i sarmalanır ve GERÇEK koşularda hangi alanın
**okunduğu** kaydedilir. Nesnenin kurulması okuma değildir (`__init__`
alanları yazar). Ölçüm, adların birbirine benzemesinden etkilenmez.

🔴 ÖLÇÜLDÜ (27 Ağustos 2026, 5 kol × 4 yapılandırma = 20 tam koşu):

    Gozlem         12 alan · hiç okunmayan  9   <- `08`in listesiyle BİREBİR
    KomsuKaydi      7 alan · hiç okunmayan  1
    PaketGorunumu   5 alan · hiç okunmayan  4   🔴 ne `08` ne denetim anıyor
    ------------------------------------------
    TOPLAM                   hiç okunmayan 14

⚖️ **ALTINCI DENETİMİN BİR İDDİASI ÇÜRÜDÜ:** B-102 `duyulan_beacon`ı da
tüketicisiz saymıştı. Çalışma anında **okunuyor** — `kosucu.py`de
`onceki.duyulan_beacon + 1`. Statik tarama onu kaçırmış, çünkü okuma bir
ÜRETİM ifadesinin içinde geçiyor.

⚠️ KAPSAMI (Y11 — koruma kendi sınırıyla birlikte yazılır)
============================================================
| vaka                                                    | görülür mü |
| Aile 0'ın kollarının okumadığı bir alan                 | ✅ evet    |
| Koşucunun kendi okuduğu alan                            | ✅ okunmuş sayılır |
| 🔴 Yalnızca KOŞULMAYAN bir dalda okunan alan            | ❌ **HAYIR** |
| 🔴 Aile 1'in protokollerinin okuyacağı alanlar          | ❌ **HAYIR** |

Sonuncusu bir kusur değil, **amaç**: bu alanlar Aile 1 için var. Sayının
düşmesi, pencerenin kullanılmaya başlandığı anlamına gelir.

Kullanım:
    python dogrulama/gozlem_tuketim.py
"""

from __future__ import annotations

import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK))

import sim.gozlem as G                                          # noqa: E402
from sim.config import Konfig                                   # noqa: E402
from dogrulama.aktaricilar import AKTARICILAR                   # noqa: E402
from dogrulama.kontrol_payi import mesafe_vektoru               # noqa: E402
from dogrulama.olcum import olc as _olc                         # noqa: E402

# Ölçüm matrisi — açıkça yazılı (`03` B3: çalışma noktasını yazmayan bulgu
# sessizce yanlış olur). Tohumlar AYARLAMA kümesinden (1–30).
KOLLAR = ("gurultuden_kacan", "en_kisa_yol", "hedefe_en_yakin", "dongu_yapan")
YAPILANDIRMALAR = (("S0", 3), ("S2", 1), ("S4", 9), ("S5", 4))

# 🔒 ÖLÇÜLDÜ 27 Ağustos 2026 — yukarıdaki matriste HİÇ OKUNMAYAN alanlar.
# Bu liste `08` madde 22'nin tek kaynağıdır ve elle yazılmaz: araç koşulur,
# çıktısı buraya ve `08`e geçer.
HIC_OKUNMAYAN: dict[str, frozenset[str]] = {
    "Gozlem": frozenset({
        "alinan_bayt", "gonderilen_bayt", "kanal_mesgul_mu",
        "kuyruk_kapasitesi", "kuyruk_uzunlugu", "olculen_gurultu_w",
        "saat_s", "son_iletim_hedefi", "son_iletim_sonucu",
    }),
    "KomsuKaydi": frozenset({"bildirdigi_kuyruk"}),
    "PaketGorunumu": frozenset({"atlama_sayisi", "bayt", "kaynak", "ttl"}),
}

_KUMELER = {
    "Gozlem": (G.Gozlem, frozenset(G.IZINLI_GOZLEM_ALANLARI)),
    "KomsuKaydi": (G.KomsuKaydi, frozenset(G.IZINLI_KOMSU_ALANLARI)),
    "PaketGorunumu": (G.PaketGorunumu, frozenset(G.IZINLI_PAKET_ALANLARI)),
}


def tuketimi_olc(kollar=KOLLAR, yapilandirmalar=YAPILANDIRMALAR) -> dict[str, set[str]]:
    """Matrisi koşar ve HİÇ OKUNMAYAN alanları döndürür.

    ⚠️ ADI `olc` DEĞİL, ve bu bilerek: kanonik `dogrulama/olcum.py::olc`
    modül kapsamında gölgelenirse çağrılar sessizce YEREL fonksiyona
    gider. Bu tam olarak `kontrol_payi.py`de yaşandı (K-072) ve
    `test_b106_KANONIK_olc_GOLGELENEMEZ` onu bir daha yakaladı.

    🔴 Sarmalama `try/finally` ile geri alınır: bu araç içe aktarıldığında
    süreçte kalıcı bir değişiklik BIRAKMAZ (bir doğrulama aracı ölçtüğü
    şeyi bozamaz — Y7).
    """
    okunan: dict[str, set[str]] = {k: set() for k in _KUMELER}
    asillar = {}
    try:
        for ad, (sinif, alanlar) in _KUMELER.items():
            asillar[ad] = sinif.__getattribute__

            def yap(ad=ad, alanlar=alanlar, asil=asillar[ad]):
                def izle(self, nitelik):
                    if nitelik in alanlar:
                        okunan[ad].add(nitelik)
                    return asil(self, nitelik)
                return izle

            sinif.__getattribute__ = yap()

        fabrikalar = [(k, AKTARICILAR[k]) for k in kollar]
        fabrikalar.append(("DV", mesafe_vektoru))
        for _kol_ad, fab in fabrikalar:
            for sen, toh in yapilandirmalar:
                _olc(Konfig(kol="t", senaryo=sen, tohum=toh), fab)
    finally:
        for ad, asil in asillar.items():
            _KUMELER[ad][0].__getattribute__ = asil

    return {ad: set(alanlar) - okunan[ad]
            for ad, (_s, alanlar) in _KUMELER.items()}


def main() -> int:
    print("=" * 78)
    print("GÖZLEM PENCERESİ — HANGİ ALAN FİİLEN OKUNUYOR (`08` madde 22)")
    print("=" * 78)
    print(f"{len(KOLLAR) + 1} kol × {len(YAPILANDIRMALAR)} yapılandırma = "
          f"{(len(KOLLAR) + 1) * len(YAPILANDIRMALAR)} tam koşu\n")

    olculen = tuketimi_olc()
    toplam = 0
    ayrisan = []
    for ad, (_s, alanlar) in _KUMELER.items():
        yok = olculen[ad]
        toplam += len(yok)
        print(f"  {ad:<14} {len(alanlar):>2} alan · okunan "
              f"{len(alanlar) - len(yok):>2} · HİÇ OKUNMAYAN {len(yok):>2}")
        for a in sorted(yok):
            print(f"                   → {a}")
        if yok != set(HIC_OKUNMAYAN[ad]):
            ayrisan.append(ad)

    print()
    print(f"  TOPLAM HİÇ OKUNMAYAN: {toplam}")
    if ayrisan:
        print()
        print(f"  🔴 BEYAN AYRIŞTI: {ayrisan}")
        print("     `HIC_OKUNMAYAN` ve `08` madde 22 GÜNCELLENMELİ (Y14).")
        return 1
    print("  ✅ beyan (`HIC_OKUNMAYAN`) ölçümle birebir")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
