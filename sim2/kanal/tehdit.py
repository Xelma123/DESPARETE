"""
Tehdit senaryosu aileleri — karıştırıcı KÜMESİNİN tanımı (Y5b).

Şartname: `v2/07-SIMULATOR-TASARIMI.md` §05.3.1 · §18 Y5. Öğrenci kararları:
`v2/04` K-119 (11 Eylül 2026). Mekanizma: `kanal/karistirici.py` (Y5a).

🔒 AİLE BİR TEDAVİ EKSENİDİR
============================
`Konfig.tehdit_senaryosu` senaryo adına girmez: sinyal sınıfı senaryo
adından, kümenin biçimi bu eksenden gelir. Varsayılan `tekli_merkez` hiçbir
tanım üretmez ve kanal bugünkü tek merkez karıştırıcıyı BİREBİR kurar.

🔒 YERLEŞİM EŞİT ARALIK VE SİMETRİDEN TÜRER — serbest sayı yok
==============================================================
    aile           K  platform   yer (alan oranı)                  yayın
    tekli_merkez   1  sabit yer  alan merkezi (bugünkü nesne)       sürekli
    cephe_hatti    3  sabit yer  x = 1 · y = (2i+1)/6               sürekli
    derin_sizma    1  araç       merkezden batıya, yalnız susarken  yay–sus–taşın
    hedef_koruma   2  sabit yer  x = 0,75 · y = (2i+1)/4            sürekli
    hava_eslik     1  hava       kuzeye; karıştırılmış evrenin       sürekli
                                 ortasında alan merkezinden geçer
Geçit batı kenarındadır; geçit merkezdeyse ve eşler arası desende de aynı
yerler kullanılır (öğrenci kararı, K-119).

🔒 GÜÇ — toplam ORTALAMA yayılan güç her ailede eşit
====================================================
Üye güç payı = 1 / (K × açık oranı): görev çevrimli ve yay–sus–taşın üyede
tepe gücü açık oranına bölünür. Sınıf içindeki darbe telafisinin üstüne
uygulanır. ρ her ailede bir SONUÇTUR.

⚠️ HIZLAR VARSAYIMDIR — araç 60 km/h, hava 200 km/h (`Konfig`, SINANMAMIŞ).
Gerçekçi hızlarda hareket bir koşu içinde küçüktür ve kapsam bölümünde beyan
edilir; ~2 000 s'lik uzun koşu şimdilik yok (K-119).
"""

from __future__ import annotations

import math

from sim2.kanal.karistirici import KaristiriciTanimi, Yayin, Yorunge
from sim2.yapilandirma.konfig import Konfig

__all__ = ["tehdit_tanimlari", "en_buyuk_hiz_ms"]


def _olcekli_hiz_ms(konfig: Konfig, gercek_kmh: float) -> float:
    """Gerçek hız (km/h) → ölçekli çerçevede m/s. Zaman ölçeklenmez."""
    return gercek_kmh / 3.6 / konfig.olcek


def _guc_payi(uye_sayisi: int, yayin: Yayin) -> float:
    """🔒 1 / (K × açık oranı) — ailenin toplam ORTALAMA gücü tek merkezinkine eşit."""
    oran = (1.0 if yayin.duzen == "surekli"
            else yayin.acik_s / (yayin.acik_s + yayin.sessiz_s))
    return 1.0 / (uye_sayisi * oran)


def tehdit_tanimlari(konfig: Konfig) -> tuple[KaristiriciTanimi, ...] | None:
    """Ailenin üye tanımları; `tekli_merkez` için `None` (bugünkü nesne)."""
    aile = konfig.tehdit_senaryosu
    if aile == "tekli_merkez":
        return None
    if aile == "cephe_hatti":
        yayin = Yayin()
        return tuple(KaristiriciTanimi(
            platform="sabit_yer",
            yorunge=Yorunge(baslangic=(1.0, (2 * i + 1) / 6)),
            yayin=yayin, guc_payi=_guc_payi(3, yayin)) for i in range(3))
    if aile == "hedef_koruma":
        # 🔴 GÖREV ÇEVRİMİ KALDIRILDI (15 Eylül 2026, K-127) — sert kısıtı
        # çiğniyordu. Açık oranı %50 olunca eşit ORTALAMA güç payı
        # 1/(2×0,5) = 1,0'a çıkıyor, yani açıkken toplam TEPE güç tabanın
        # İKİ KATI oluyordu ve 30 tohumun 2'sinde ağ BÖLÜNÜYORDU
        # (açık evre 15 s, AODV'nin 3 s'lik rota geçersizlemesinin çok
        # üstünde). Sebep ÖLÇÜLDÜ: aynı geometri sürekli yayında 0/30
        # (ρ 0,240); geometriyi batıya kaydırmak (x = 0,60) çevrim
        # kalırken yine 2/30 verdi. ⚠İ `07` §05.3 bu çevrimi *görev düzeyi
        # deseni* diye gerekçelendiriyordu; o gerekçe çürütülmedi, sert
        # kısıtın önceliği altında kaldı (öğrenci kararı, K-127).
        yayin = Yayin()
        return tuple(KaristiriciTanimi(
            platform="sabit_yer",
            yorunge=Yorunge(baslangic=(0.75, (2 * i + 1) / 4)),
            yayin=yayin, guc_payi=_guc_payi(2, yayin)) for i in range(2))
    if aile == "derin_sizma":
        yayin = Yayin(duzen="yay_sus_tasin", acik_s=konfig.tehdit_acik_s,
                      sessiz_s=konfig.tehdit_sessiz_s)
        return (KaristiriciTanimi(
            platform="arac",
            yorunge=Yorunge(baslangic=(0.5, 0.5), tur="sessizde",
                            hiz_ms=_olcekli_hiz_ms(
                                konfig, konfig.tehdit_arac_hiz_kmh),
                            yon_rad=math.pi),              # geçide, batıya
            yayin=yayin, guc_payi=_guc_payi(1, yayin)),)
    if aile == "hava_eslik":
        hiz = _olcekli_hiz_ms(konfig, konfig.tehdit_hava_hiz_kmh)
        # Karıştırılmış evrenin ortasında alan merkezinin üstünde olacak biçimde.
        t_orta = 0.5 * (konfig.karistirici_baslangic_s + konfig.olcum_bitis_s)
        yayin = Yayin()
        return (KaristiriciTanimi(
            platform="hava",
            yorunge=Yorunge(
                baslangic=(0.5, 0.5 - hiz * t_orta / konfig.alan_boy_m),
                tur="dogrusal", hiz_ms=hiz, yon_rad=math.pi / 2),  # kuzeye
            yayin=yayin, guc_payi=_guc_payi(1, yayin)),)
    raise ValueError(f"tanımı olmayan tehdit senaryosu: {aile!r}")


def en_buyuk_hiz_ms(konfig: Konfig) -> float:
    """En hızlı üyenin ölçekli hızı — kâhin tazelemesi için; sabit ailede 0."""
    if konfig.karistirici_sinifi == "yok":
        return 0.0
    tanimlar = tehdit_tanimlari(konfig)
    if tanimlar is None:
        return 0.0
    return max(t.yorunge.hiz_ms for t in tanimlar)
