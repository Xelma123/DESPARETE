"""
Y5b — tehdit senaryosu aileleri (`v2/07` §05.3.1 · §18 Y5).

Öğrenci kararları: `v2/04` K-119 (11 Eylül 2026) — beş aile ve üye sayıları ·
çekirdek süreler 15 s açık / 15 s sessiz / %50 görev çevrimi 30 s · derin
sızma aracı yalnız susarken taşınır · yerleşim türetme kuralları. Uygulama
kaydı: K-120.

🔒 HİÇBİR KAPI BOŞ GEÇMEZ (K-110): hareket sınanan her yerde hareket, güç
sınanan her yerde sıfırdan büyük güç bulunmuş olmalı.
"""

from __future__ import annotations

import math
import pathlib
import sys

import pytest

KOK = pathlib.Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.cekirdek.degismezler import DegismezHatasi  # noqa: E402
from sim2.cekirdek.rng import Akislar  # noqa: E402
from sim2.dunya.topoloji import topoloji_kur  # noqa: E402
from sim2.kanal.kanal import Kanal  # noqa: E402
from sim2.kanal.karistirici import (KaristiriciKumesi,  # noqa: E402
                                    KaristiriciTanimi, Surekli, Yayin,
                                    Yorunge, karistirici_kur)
from sim2.kanal.tehdit import en_buyuk_hiz_ms, tehdit_tanimlari  # noqa: E402
from sim2.yapilandirma.kapsam import kapsam_bolumu  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402
from sim2.yapilandirma.senaryolar import TEHDIT_SENARYOLARI  # noqa: E402

GUC_DBM = 5.0          # ölçülmemiş; testler için açıkça verilen çalışma gücü
UYE_SAYISI = {"cephe_hatti": 3, "derin_sizma": 1, "hedef_koruma": 2,
              "hava_eslik": 1}


def _konfig(aile: str = "tekli_merkez", senaryo: str = "statik-surekli",
            **ek) -> Konfig:
    return Konfig(kol="t", senaryo=senaryo, tehdit_senaryosu=aile,
                  karistirici_guc_override_dbm=GUC_DBM, **ek)


def _kanal(aile: str = "tekli_merkez", **ek) -> Kanal:
    k = _konfig(aile, **ek)
    return Kanal(k, topoloji_kur(k, Akislar(1)))


def _acik_orani(t: KaristiriciTanimi) -> float:
    y = t.yayin
    return 1.0 if y.duzen == "surekli" else y.acik_s / (y.acik_s + y.sessiz_s)


# ==========================================================================
def test_Y5b_bes_AILE_ve_varsayilan_TEKLI_MERKEZ():
    assert TEHDIT_SENARYOLARI == ("tekli_merkez", "cephe_hatti", "derin_sizma",
                                  "hedef_koruma", "hava_eslik")
    assert Konfig(kol="t").tehdit_senaryosu == "tekli_merkez"
    with pytest.raises(ValueError):
        Konfig(kol="t", tehdit_senaryosu="uzay_istasyonu")


def test_Y5b_tekli_merkez_TANIMSIZ_bugunku_nesne_BIREBIR():
    """Varsayılan aile tanım üretmez; kanal bugünkü tek merkez nesnesini kurar."""
    assert tehdit_tanimlari(_konfig()) is None
    assert type(_kanal().karistirici) is Surekli
    assert en_buyuk_hiz_ms(_konfig()) == 0.0
    # Senaryo adında karıştırıcı yoksa aile ne olursa olsun karıştırıcı yok.
    k = Konfig(kol="t", senaryo="statik-yok", tehdit_senaryosu="cephe_hatti")
    assert Kanal(k, topoloji_kur(k, Akislar(1))).karistirici is None


def test_Y5b_uye_SAYILARI_ve_ORTALAMA_GUC_ESITLEMESI():
    """Her ailede Σ (güç payı × açık oranı) = 1 — toplam ORTALAMA güç eşit."""
    for aile, k_uye in UYE_SAYISI.items():
        tanimlar = tehdit_tanimlari(_konfig(aile))
        assert len(tanimlar) == k_uye, aile
        assert math.fsum(t.guc_payi * _acik_orani(t) for t in tanimlar) == \
            pytest.approx(1.0, rel=1e-12), aile


def test_Y5b_YERLESIM_KURALLARI():
    cephe = tehdit_tanimlari(_konfig("cephe_hatti"))
    assert [t.yorunge.baslangic for t in cephe] == [
        (1.0, 1 / 6), (1.0, 3 / 6), (1.0, 5 / 6)]
    assert all(t.platform == "sabit_yer" and t.yayin.duzen == "surekli"
               for t in cephe)
    koruma = tehdit_tanimlari(_konfig("hedef_koruma"))
    assert [t.yorunge.baslangic for t in koruma] == [(0.75, 0.25),
                                                     (0.75, 0.75)]
    # 🔒 K-127: görev çevrimi KALDIRILDI; iki üye sürekli yayar ve payları
    # 1/(2×1) = 0,5, yani açıkken toplam TEPE güç tabanı AŞMAZ.
    assert all(t.yayin.duzen == "surekli" and t.guc_payi == 0.5
               for t in koruma)
    (sizma,) = tehdit_tanimlari(_konfig("derin_sizma"))
    assert sizma.platform == "arac" and sizma.yorunge.baslangic == (0.5, 0.5)
    assert sizma.yorunge.tur == "sessizde"
    assert sizma.yorunge.yon_rad == pytest.approx(math.pi)     # geçide, batıya
    assert sizma.yayin.duzen == "yay_sus_tasin"
    (hava,) = tehdit_tanimlari(_konfig("hava_eslik"))
    assert hava.platform == "hava" and hava.yayin.duzen == "surekli"
    assert hava.yorunge.yon_rad == pytest.approx(math.pi / 2)  # kuzeye


def test_Y5b_hava_eslik_KARISTIRILMIS_EVRENIN_ORTASINDA_merkezden_gecer():
    kanal = _kanal("hava_eslik")
    j, k = kanal.karistirici, kanal.konfig
    t_orta = 0.5 * (k.karistirici_baslangic_s + k.olcum_bitis_s)
    p = j.konum_t(t_orta)
    assert p.x == pytest.approx(k.alan_en_m / 2.0)
    assert p.y == pytest.approx(k.alan_boy_m / 2.0, abs=1e-6)
    hiz = k.tehdit_hava_hiz_kmh / 3.6 / k.olcek
    assert j.konum_t(t_orta + 10.0).y - p.y == pytest.approx(10.0 * hiz)


def test_Y5b_derin_sizma_YALNIZ_SUSARKEN_TASINIR():
    kanal = _kanal("derin_sizma")
    j, k = kanal.karistirici, kanal.konfig
    hiz = k.tehdit_arac_hiz_kmh / 3.6 / k.olcek
    t0, acik, sessiz = (k.karistirici_baslangic_s, k.tehdit_acik_s,
                        k.tehdit_sessiz_s)
    assert j.konum_t(0.0) == j.konum_t(t0), "açılmadan önce yerinde"
    assert j.konum_t(t0 + 1.0) == j.konum_t(t0 + acik - 1.0), \
        "açık dönemde durur"
    a, b = j.konum_t(t0 + acik + 1.0), j.konum_t(t0 + acik + sessiz - 1.0)
    assert a.x - b.x == pytest.approx(hiz * (sessiz - 2.0), rel=1e-9)
    assert b.x < a.x and a.y == b.y
    son = k.kosu_bitis_s
    n, faz = divmod(son - t0, acik + sessiz)
    toplam_sessiz = n * sessiz + max(0.0, faz - acik)
    yol = j.konum_t(0.0).x - j.konum_t(son).x
    assert yol > 0.0
    assert yol == pytest.approx(hiz * toplam_sessiz, rel=1e-9)


def test_Y5b_KUME_kurulur_ve_ACIK_DONEMDE_guc_verir():
    kanal = _kanal("cephe_hatti")
    assert isinstance(kanal.karistirici, KaristiriciKumesi)
    assert len(kanal.karistirici.uyeler) == 3
    t = kanal.konfig.karistirici_baslangic_s + 1.0
    assert kanal.karistirici.alinan_guc_w(
        0, kanal.topoloji.konum(0, t), t) > 0.0


def test_Y5b_hedef_koruma_SUREKLI_ve_TEPE_GUC_TABANI_ASMAZ():
    """🔒 K-127 KAPISI — çevrimin geri gelmesini yasaklar.

    Çevrimli hâlde açık oranı %50 olduğu için eşit ORTALAMA güç payı
    1/(2×0,5) = 1,0'a çıkıyordu ve açıkken toplam TEPE güç tabanın iki
    katıydı; 30 tohumun 2'sinde ağ bölünüyordu (açık evre 15 s, AODV'nin
    3 s'lik rota geçersizlemesinin çok üstünde).

    ⚠️ Kapı AİLEYE ÖZELDİR, genel bir "tepe ≤ taban" kuralı değildir:
    `derin_sizma` payı 2,0 ile yayar (tek üye, %50 açık) ve açık evreye
    kilitlenmiş ölçümde 30 tohumun HİÇBİRİNDE bölünme vermedi (ρ 0,382).
    Bölünmeyi üreten şey tepe gücü değil, tepe gücü + iki noktalı duvar.
    """
    kanal = _kanal("hedef_koruma")
    k = kanal.konfig
    t0 = k.karistirici_baslangic_s
    konum = kanal.topoloji.konum(0, t0)
    # Sürekli: hem erken hem geç anda güç VAR (eskiden geç anda 0 idi).
    assert kanal.karistirici.alinan_guc_w(0, konum, t0 + 1.0) > 0.0
    assert kanal.karistirici.alinan_guc_w(0, konum, t0 + 16.0) > 0.0
    tanimlar = tehdit_tanimlari(k)
    assert sum(t.guc_payi for t in tanimlar) == pytest.approx(1.0)


def test_Y5b_KONFIG_ve_YORUNGE_DOGRULAMALARI():
    for alan in ("tehdit_acik_s", "tehdit_sessiz_s",
                 "tehdit_arac_hiz_kmh", "tehdit_hava_hiz_kmh"):
        with pytest.raises(DegismezHatasi):
            Konfig(kol="t", **{alan: 0.0})
    kanal = _kanal()
    # "Yalnız susarken taşınma" çevrimsiz yayında anlamsızdır.
    with pytest.raises(DegismezHatasi):
        karistirici_kur(kanal.konfig, kanal.yayilim, kanal.topoloji,
                        kanal.ortam, tanimlar=(KaristiriciTanimi(
                            platform="arac",
                            yorunge=Yorunge(baslangic=(0.5, 0.5),
                                            tur="sessizde", hiz_ms=0.3),
                            yayin=Yayin(duzen="surekli")),))


def test_Y5b_kahin_tazelemesi_KARISTIRICI_HIZINI_katar():
    from kalibrasyon.kahin import dilim_suresi_s
    tekli = _konfig(golgeleme_hucre_m=1.0)
    hava = _konfig("hava_eslik", golgeleme_hucre_m=1.0)
    assert en_buyuk_hiz_ms(hava) == pytest.approx(
        hava.tehdit_hava_hiz_kmh / 3.6 / hava.olcek)
    assert dilim_suresi_s(tekli) == pytest.approx(
        1.0 / (2.0 * tekli.gm_hiz_maks_ms))
    assert dilim_suresi_s(hava) < dilim_suresi_s(tekli)


def test_Y5b_KAPSAM_tehdit_senaryosunu_ve_sinirlarini_yazar():
    tekli = kapsam_bolumu(_konfig())
    assert tekli["tehdit_senaryosu"] == "tekli_merkez"
    assert "tehdit_sinirlari" not in tekli
    sizma = kapsam_bolumu(_konfig("derin_sizma"))
    assert sizma["tehdit_senaryosu"] == "derin_sizma"
    assert sizma["tehdit_sinirlari"]
