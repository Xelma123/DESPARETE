"""DESPARETE 5 · selam ve ara ilan (KK-02): ileti boyutu, kodlama,
uyarlanır aralık, sıklık sınırı, gönderemezken kurulmama."""

from __future__ import annotations

import pytest

from protokoller.desparete5_bicim import (
    SELAM, SELAM_E, SONSUZ, TAM, TUR_ISTEGI, Bayraklar, Degerler)
from protokoller.desparete5_selam import (
    SelamZamanlayici, onemli_degisim, selam_coz, selam_yuku)
from sim2.gozlem.kontrol import KontrolIstegi, Uyandirma

D = Degerler()


def test_BOYUT_9_bayt_arti_komsu_basina_2_bayt():
    bos = KontrolIstegi.kur(None, SELAM, selam_yuku(0, 2.2, 1, 0, False,
                                                     (), ()))
    assert bos.mesaj_bayt == 9
    on_bes = KontrolIstegi.kur(None, SELAM, selam_yuku(
        65535, 655.0, 65535, SONSUZ, True, tuple(range(15)),
        tuple([255] * 15)))
    assert on_bes.mesaj_bayt == 39                # KK-02: 15 komşuyla 39 B
    assert KontrolIstegi.kur(3, TUR_ISTEGI, {"istenen": 9, "kalan": 64}
                             ).mesaj_bayt == 3


def test_KODLAMA_gidis_donus_ve_listede_olmayan():
    y = selam_yuku(12, 0.55, 7, 150, True, (3, 7, 20), (255, 229, 10))
    istek = KontrolIstegi.kur(None, SELAM, y)
    sira, aralik, tur, maliyet, bit, bildirilen = selam_coz(istek.yuk, 7)
    assert (sira, tur, maliyet, bit) == (12, 7, 150, True)
    assert aralik == pytest.approx(0.55)
    assert bildirilen == pytest.approx(229 / 255)
    assert selam_coz(istek.yuk, 99)[5] is None    # Y-12: bilinmiyor


def test_ARALIK_olaydan_sonra_0_5_1_2_ve_ilan_edilen_ust_sinir():
    """KK-02'nin örneği: aralık 0,5 → 1 → 2 s; ilan edilen üst sınır
    0,55 → 1,1 → 2,2 → 2,2 s."""
    z = SelamZamanlayici(D, TAM)
    u = z.olay(10.0)
    assert isinstance(u, Uyandirma) and u.jitter_s == pytest.approx(0.05)
    t, ilan, ara = 10.0, [], []
    for _ in range(4):
        (sira, aralik), u = z.kur(t, False)
        ilan.append(round(aralik, 3))
        ara.append(round(u.gecikme_s, 3))
        assert z.guncel_mi(u.etiket)
        assert u.jitter_s == pytest.approx(0.1 * u.gecikme_s)
        t += u.gecikme_s
    assert ilan == [0.55, 1.1, 2.2, 2.2]
    assert ara == [0.5, 1.0, 2.0, 2.0]
    assert z.sira == 4


def test_SIKLIK_SINIRI_olaylar_birlesir_eski_nesil_yok_sayilir():
    z = SelamZamanlayici(D, TAM)
    z.olay(0.0)
    _, plan = z.kur(0.0, False)                   # sonraki 0,5'te
    for t in (0.5, 1.5):
        _, plan = z.kur(t, False)
    eski = plan                                   # 3,5'te planlı
    u = z.olay(1.6)
    assert u.gecikme_s == pytest.approx(0.4)      # en az I_MIN arayla
    assert z.olay(1.8) is None                    # birleşti
    assert not z.guncel_mi(eski.etiket) and z.guncel_mi(u.etiket)


def test_UYARLANIR_ARALIK_kapaliyken_ara_ilan_I_yi_degistirmez_Y5():
    z = SelamZamanlayici(D, Bayraklar(uyarlanir_aralik=False))
    u = z.olay(5.0)
    assert u.jitter_s == pytest.approx(0.2)
    (_, aralik), u = z.kur(5.0, False)
    assert aralik == pytest.approx(2.2) and u.gecikme_s == pytest.approx(2.0)
    (_, aralik), _ = z.kur(7.0, False)
    assert aralik == pytest.approx(2.2) and z.I == 2.0


def test_GONDEREMEZKEN_selam_kurulmaz_bitince_hemen_KK02_5():
    z = SelamZamanlayici(D, TAM)
    z.baslat(0.0)
    z.kur(0.0, False)
    selam, plan = z.kur(2.0, True)
    assert selam is None and plan is None and z.ed_bekliyor
    u = z.ed_bitti(15.0)
    assert u.gecikme_s == pytest.approx(1e-3) and not z.ed_bekliyor
    (sira, aralik), _ = z.kur(15.0, False)
    assert sira == 1 and aralik == pytest.approx(0.55)


@pytest.mark.parametrize("yeni,ilan,beklenen", [
    (100, None, True), (100, 100, False), (115, 100, True),
    (114, 100, False), (86, 100, False), (85, 100, True),
    (SONSUZ, 100, True), (100, SONSUZ, True), (SONSUZ, SONSUZ, False),
    (0, 0, False)])
def test_ONEMLI_DEGISIM_yuzde_15_ve_sonsuz(yeni, ilan, beklenen):
    assert onemli_degisim(yeni, ilan, D.ILAN_ESIGI) is beklenen


def test_EGIM_BICIMI_tur_yok_7_bayt_arti_komsu_basina_2_bayt():
    """KK-02 (19 Kasım): eğimde tur alanı yok; sabit 49 bit → 7 bayt."""
    bos = KontrolIstegi.kur(None, SELAM_E, selam_yuku(0, 2.2, None, 0, False,
                                                       (), ()))
    assert bos.mesaj_bayt == 7
    on_bes = KontrolIstegi.kur(None, SELAM_E, selam_yuku(
        65535, 655.0, None, SONSUZ, True, tuple(range(15)),
        tuple([255] * 15)))
    assert on_bes.mesaj_bayt == 37                # KK-02: 15 komşuyla 37 B
    sira, aralik, tur, C, bit, bildirilen = selam_coz(
        selam_yuku(7, 1.1, None, 640, True, (3, 5), (255, 128)), 5)
    assert (sira, tur, C, bit) == (7, None, 640, True)
    assert aralik == pytest.approx(1.1) and bildirilen == pytest.approx(128 / 255)
