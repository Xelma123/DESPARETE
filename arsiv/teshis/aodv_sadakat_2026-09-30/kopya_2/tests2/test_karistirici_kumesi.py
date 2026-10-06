"""
Y5a — çoklu ve hareketli karıştırıcı MEKANİZMASI (`v2/07` §18 Y5, §05.3).

Ailelerin sayıları (Y5b) öğrenci kararını bekliyor; bu dosya yalnız mekanizmayı
bağlar ve tanımları doğrudan kurar. Varsayılan yolun (tek merkez karıştırıcı)
birebir kaldığını regresyon aleti sınar.

🔒 HİÇBİR KAPI BOŞ GEÇMEZ: güç sınanan her yerde güç sıfırdan büyük, görünür
üye sınanan her yerde görünür bir an bulunmuş olmalı (K-110 dersi).
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
from sim2.kanal.girisim import Girisim  # noqa: E402
from sim2.kanal.kanal import Kanal  # noqa: E402
from sim2.kanal.karistirici import (KaristiriciKumesi,  # noqa: E402
                                    KaristiriciTanimi, Yayin, Yorunge,
                                    karistirici_kur)
from sim2.yapilandirma.konfig import Konfig  # noqa: E402

GUC_DBM = 5.0          # ölçülmemiş; testler için açıkça verilen çalışma gücü

MERKEZ = KaristiriciTanimi(platform="sabit_yer",
                           yorunge=Yorunge(baslangic=(0.5, 0.5)))


def _kanal(sinif: str = "surekli", **ek) -> Kanal:
    k = Konfig(kol="t", senaryo=f"statik-{sinif}",
               karistirici_guc_override_dbm=GUC_DBM, **ek)
    return Kanal(k, topoloji_kur(k, Akislar(1)))


def _kur(kanal: Kanal, tanimlar):
    return karistirici_kur(kanal.konfig, kanal.yayilim, kanal.topoloji,
                           kanal.ortam, tanimlar=tanimlar)


def _devrede_an(kanal: Kanal, gecikme_s: float = 10.0) -> float:
    return kanal.konfig.karistirici_baslangic_s + gecikme_s


# ==========================================================================
def test_Y5a_TEK_TANIM_varsayilan_karistiriciyla_BIREBIR():
    """Merkezde sabit tek tanım = bugünkü varsayılan nesne: aynı sınıf, aynı güç."""
    kanal = _kanal()
    tek = _kur(kanal, (MERKEZ,))
    assert type(tek) is type(kanal.karistirici)
    t = _devrede_an(kanal)
    for alici in range(0, kanal.konfig.dugum_sayisi, 7):
        konum = kanal.topoloji.konum(alici, t)
        guc = kanal.karistirici.alinan_guc_w(alici, konum, t)
        assert guc > 0.0
        assert tek.alinan_guc_w(alici, konum, t) == guc


def test_Y5a_KUME_gucu_UYELERIN_TOPLAMI_ve_ARAYUZ_ayni():
    kanal = _kanal()
    kume = _kur(kanal, (MERKEZ, KaristiriciTanimi(
        platform="sabit_yer", yorunge=Yorunge(baslangic=(0.2, 0.8)))))
    assert isinstance(kume, KaristiriciKumesi) and len(kume.uyeler) == 2
    t = _devrede_an(kanal)
    konum = kanal.topoloji.konum(3, t)
    uyeler = [u.alinan_guc_w(3, konum, t) for u in kume.uyeler]
    assert all(g > 0.0 for g in uyeler)
    assert kume.alinan_guc_w(3, konum, t) == pytest.approx(sum(uyeler),
                                                           rel=1e-12)
    for ad in ("alinan_guc_w", "csma_guc_w", "csma_ya_gorunur",
               "gecis_anlari", "devrede_mi", "acik_mi"):
        assert callable(getattr(kume, ad)), ad


def test_Y5a_TASIYICI_DINLEME_yalniz_GORUNUR_uyelerin_gucune_bakar():
    """🔒 Tasarımın değişen TEK çağrı noktası: taşıyıcı dinleme yalnız CSMA'ya
    görünen üyelerin gücüne bakar. Tek karıştırıcıda sonuç bugünküyle aynıdır."""
    kanal = _kanal("surekli")
    kume = _kur(kanal, (MERKEZ, KaristiriciTanimi(
        platform="sabit_yer", sinif="aldatici",
        yorunge=Yorunge(baslangic=(0.3, 0.3)))))
    sur, ald = kume.uyeler
    assert not sur.csma_gorunur and ald.csma_gorunur and kume.csma_gorunur
    t = _devrede_an(kanal)
    for _ in range(100):
        if ald.csma_ya_gorunur(t):
            break
        t += 1e-4
    assert ald.csma_ya_gorunur(t), "boş geçmemeli — görünür bir an bulunmalı"
    konum = kanal.topoloji.konum(5, t)
    assert kume.csma_guc_w(5, konum, t) == pytest.approx(
        ald.alinan_guc_w(5, konum, t), rel=1e-12)
    assert kume.alinan_guc_w(5, konum, t) > kume.csma_guc_w(5, konum, t) > 0.0


def test_Y5a_HAREKETLI_uye_DOGRUSAL_ve_SUREKLI():
    kanal = _kanal()
    v, yon = 1.1, math.pi / 4
    j = _kur(kanal, (KaristiriciTanimi(
        platform="hava", yorunge=Yorunge(baslangic=(0.5, 0.5), tur="dogrusal",
                                         hiz_ms=v, yon_rad=yon)),))
    a, b = j.konum_t(100.0), j.konum_t(130.0)
    assert b.x - a.x == pytest.approx(v * 30.0 * math.cos(yon), rel=1e-9)
    assert b.y - a.y == pytest.approx(v * 30.0 * math.sin(yon), rel=1e-9)
    assert b.z == a.z
    t = _devrede_an(kanal)
    konum = kanal.topoloji.konum(0, t)
    assert j.alinan_guc_w(0, konum, t) != j.alinan_guc_w(0, konum, t + 60.0)


def test_Y5a_YAYIN_CIZELGESI_ilan_edildigi_gibi():
    kanal = _kanal()
    bas = kanal.konfig.karistirici_baslangic_s
    j = _kur(kanal, (KaristiriciTanimi(
        platform="arac", yorunge=Yorunge(baslangic=(0.5, 0.5)),
        yayin=Yayin(duzen="yay_sus_tasin", ofset_s=5.0, acik_s=15.0,
                    sessiz_s=10.0)),))
    t0 = bas + 5.0
    assert not j.devrede_mi(t0 - 1e-6)
    assert j.devrede_mi(t0 + 1e-6) and j.devrede_mi(t0 + 14.9)
    assert not j.devrede_mi(t0 + 15.1) and not j.devrede_mi(t0 + 24.9)
    assert j.devrede_mi(t0 + 25.1)
    konum = kanal.topoloji.konum(0, t0 + 20.0)
    assert j.alinan_guc_w(0, konum, t0 + 20.0) == 0.0
    assert j.alinan_guc_w(0, konum, t0 + 10.0) > 0.0
    with pytest.raises(DegismezHatasi):
        _kur(kanal, (KaristiriciTanimi(
            platform="arac", yorunge=Yorunge(baslangic=(0.5, 0.5)),
            yayin=Yayin(duzen="gorev_cevrimli", acik_s=0.0, sessiz_s=5.0)),))


def test_Y5a_GOLGELEME_KIMLIGI_uye_basina_AYRI(monkeypatch):
    """İlk üye bugünkü `-1`i korur; ikinci üye `-2`. Aynı kimlik olsaydı iki
    karıştırıcının gölgelemesi aynı konumda aynı çekimi paylaşırdı."""
    kanal = _kanal()
    gorulen: list[int] = []
    asil = type(kanal.yayilim).yavas_kayip_db

    def casus(self, i, j, a, b):
        gorulen.append(i)
        return asil(self, i, j, a, b)

    monkeypatch.setattr(type(kanal.yayilim), "yavas_kayip_db", casus)
    kume = _kur(kanal, (MERKEZ, MERKEZ))
    t = _devrede_an(kanal)
    kume.alinan_guc_w(2, kanal.topoloji.konum(2, t), t)
    assert sorted(set(gorulen)) == [-2, -1]


def test_Y5a_KAPALIYKEN_girisim_KARISTIRICISIZ_kanalla_BIREBIR():
    """K-104 kapısının genellemesi: açılmadan önce küme hiçbir şey eklemez."""
    kanal = _kanal()
    kume = _kur(kanal, (MERKEZ, KaristiriciTanimi(
        platform="sabit_yer", yorunge=Yorunge(baslangic=(0.1, 0.9)))))
    t = kanal.konfig.karistirici_baslangic_s - 1.0
    ile = Girisim(kanal.konfig, kanal.topoloji, kanal.yayilim,
                  kanal.sonumleme, kanal.ortam, kume)
    olmadan = Girisim(kanal.konfig, kanal.topoloji, kanal.yayilim,
                      kanal.sonumleme, kanal.ortam, None)
    for alici in (0, 4, 9):
        haric = (alici + 1) % 10
        assert ile.girisim_w(alici, t, haric=haric) == \
            olmadan.girisim_w(alici, t, haric=haric)
    assert not ile.kanal_mesgul_mu(3, t)


def test_Y5a_TANIM_DOGRULAMALARI():
    kanal = _kanal()
    with pytest.raises(DegismezHatasi):
        _kur(kanal, (KaristiriciTanimi(platform="uzay",
                                       yorunge=Yorunge(baslangic=(0.5, 0.5))),))
    with pytest.raises(DegismezHatasi):
        _kur(kanal, (KaristiriciTanimi(platform="sabit_yer",
                                       yorunge=Yorunge(baslangic=(1.5, 0.5))),))
    with pytest.raises(DegismezHatasi):
        _kur(kanal, ())
