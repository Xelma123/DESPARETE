"""DESPARETE 5 · rota seçimi ve döngü bekçisi (KK-04, 19 Kasım; `egim`).
Senaryolar kâğıdın kurallarından ve örneğinden. Simülatörsüz: bağ tablosunun
rota için gereken yüzü elle kurulur."""

from __future__ import annotations

import math
from types import SimpleNamespace

import pytest

from protokoller.desparete5_bicim import (
    SONSUZ, TAM, Bayraklar, Degerler, maliyet_birimi)
from protokoller.desparete5_egim import Egim

D = Degerler()
GECIT = 0


class Baglar:
    """KK-01'in tablosunun eğim için gereken yüzü: durum, ETX, işaret."""

    def __init__(self) -> None:
        self.k: dict[int, list] = {}            # j → [durum, etx, vud_bitis]

    def ekle(self, j, durum="olagan", etx=1.0, vud=-math.inf):
        self.k[j] = [durum, etx, vud]

    def kullanilir_mi(self, j):
        return j in self.k and self.k[j][0] == "olagan"

    def durum(self, j):
        return self.k[j][0] if j in self.k else None

    def etx(self, j):
        return self.k[j][1]

    def maliyet(self, j):
        return maliyet_birimi(self.k[j][1])

    def veriye_uygun(self, j, t):
        return j not in self.k or t >= self.k[j][2]


def E(x: float) -> int:
    return maliyet_birimi(x)


def kur(bayraklar=TAM, ilan_C=None):
    e = Egim(5, GECIT, D, bayraklar)
    if ilan_C is not None:
        e.ilan_edildi(0, E(ilan_C))
    return e, Baglar()


def ilan(e, j, C, t=0.0):
    e.ilan_al(j, t, None, SONSUZ if C is None else E(C))


def paket(kaynak, sira, atlama):
    return SimpleNamespace(kaynak=kaynak, kaynak_sira=sira,
                           atlama_sayisi=atlama, hedef=GECIT)


# ==========================================================================
# KK-04/1–4 · seçim
# ==========================================================================
def test_ILK_SECIM_en_ucuz_ve_esitlikte_dusuk_ETX():
    e, b = kur()
    for j, etx, C in ((1, 1.0, 2.0), (2, 1.0, 1.5), (3, 2.0, 0.5)):
        b.ekle(j, etx=etx)
        ilan(e, j, C)
    # 2 ile 3 eşit (1,0 + 1,5 = 2,0 + 0,5 = 2,5); 1 3,0. Hiç ilan etmedim
    # (D = A); eşitlikte düşük ETX'li 2.
    e.sec(0.0, b, False)
    assert e.ardil == 2 and e.C == E(1.0) + E(1.5)
    assert e.ilan() == (0, e.C)
    # 2 kaybolunca en ucuz yokuş aşağı aday 3 (2,5 < 3,0).
    e.ilan_edildi(0, e.C)
    b.ekle(2, durum="kotu")
    e.sec(1.0, b, False)
    assert e.ardil == 3 and e.sayac["zorunlu_gecis"] == 1


def test_ZORUNLU_GECIS_grup_sirasi_ve_son_care():
    """G1 yokuş aşağı uygun · G2 yokuş aşağı veriye uygun değil · G3 yokuş
    yukarı uygun · G4. Yokuş yukarı seçim son çaredir: olay ve sayaç."""
    e, b = kur(ilan_C=2.5)
    b.ekle(1)
    ilan(e, 1, 1.0)                             # ardıl
    b.ekle(2, vud=100.0)
    ilan(e, 2, 2.0)                             # yokuş aşağı, veriye uygun değil
    b.ekle(3)
    ilan(e, 3, 3.0)                             # yokuş yukarı
    e.sec(0.0, b, False)
    assert e.ardil == 1
    e.olay_oku()
    b.ekle(1, durum="kotu")
    e.sec(1.0, b, False)
    assert e.ardil == 2 and e.sayac["son_care"] == 0 and not e.olay_oku()
    b.ekle(2, durum="kotu")
    e.sec(2.0, b, False)
    assert e.ardil == 3 and e.C == E(1.0) + E(3.0)
    assert e.sayac["son_care"] == 1 and e.olay_oku()


def test_VERIYE_UYGUN_DEGIL_ardil_yalniz_yokus_asagi_uygun_yedege_gecer():
    e, b = kur(ilan_C=2.5)
    b.ekle(1)
    ilan(e, 1, 1.0)
    b.ekle(3)
    ilan(e, 3, 3.0)                             # yalnız yokuş yukarı yedek
    e.sec(0.0, b, False)
    assert e.ardil == 1
    b.k[1][2] = 10.0                            # 1 veriye uygun değil
    e.sec(1.0, b, False)
    assert e.ardil == 1                         # yedek yok: bağ kalır (T-2)
    b.ekle(2)
    ilan(e, 2, 2.0)                             # yokuş aşağı, uygun
    e.sec(2.0, b, False)
    assert e.ardil == 2 and e.sayac["veri_gecis"] == 1
    assert e.C == E(1.0) + E(2.0)


def test_YOL_YOK_ve_suresi_tur_istegi_yok():
    e, b = kur(ilan_C=2.0)
    b.ekle(1)
    ilan(e, 1, 1.0)
    e.sec(0.0, b, False)
    ilan(e, 1, None)                            # ardıl ∞ ilan etti
    e.sec(1.0, b, False)
    assert e.ardil is None and e.C == SONSUZ and e.sayac["yol_yok"] == 1
    assert e.istekleri_al() == []
    ilan(e, 1, 1.0)
    e.sec(3.5, b, False)
    assert e.ardil == 1 and e.sayac["yol_yok_bitti"] == 1
    assert e.sayac["yol_yok_sure_ms"] == 2500


def test_MALIYET_TAVANI_32_ETX():
    e, b = kur()
    b.ekle(1)
    ilan(e, 1, 30.0)
    e.sec(0.0, b, False)
    assert e.ardil == 1 and e.C == E(31.0)      # 31 ≤ 32
    ilan(e, 1, 31.5)                            # 32,5 > 32
    e.sec(1.0, b, False)
    assert e.ardil is None and e.sayac["tavan_asimi"] == 1
    assert D.maliyet_tavani == 32 * 64


def test_SILINEN_komsunun_ilani_silinir():
    e, b = kur()
    b.ekle(1)
    ilan(e, 1, 1.0)
    e.sec(0.0, b, False)
    del b.k[1]
    e.sec(1.0, b, False)
    assert e.ardil is None and 1 not in e.ilanlar


def test_GECIT_secmez_maliyeti_0():
    g = Egim(GECIT, GECIT, D, TAM)
    b = Baglar()
    b.ekle(1)
    ilan(g, 1, 1.0)
    g.sec(0.0, b, False)
    assert g.ardil is None and g.C == 0 and g.ilan() == (0, 0)


# ==========================================================================
# KK-04/5–6 · isteğe bağlı geçiş
# ==========================================================================
def test_ISTEGE_BAGLI_iki_olcu_duzgunlestirme_bekletir():
    """Ardıl 3,0; x uzun süre 5,0, sonra 2,0. Anlık maliyet hemen daha iyi,
    düzgünleştirilmiş maliyet `2 + 3·e^(−Δ/6)` ancak Δ > 6·ln 3 ≈ 6,6 s'de
    3'ün altına iner."""
    e, b = kur(ilan_C=3.0)
    b.ekle(1)
    ilan(e, 1, 2.0)                             # m = 3,0
    b.ekle(2)
    ilan(e, 2, 4.0)                             # m = 5,0 (yokuş yukarı)
    for t in range(0, 31, 2):
        e.sec(float(t), b, False)
    assert e.ardil == 1 and e.ms[2][0] == pytest.approx(E(5.0))
    ilan(e, 2, 1.0, t=30.0)                     # m = 2,0, yokuş aşağı
    e.sec(30.0, b, False)
    e.sec(36.0, b, False)
    assert e.ardil == 1                         # ms 2 + 3/e ≈ 3,10 > 3
    e.sec(37.0, b, False)
    assert e.ardil == 2 and e.sayac["istege_bagli_gecis"] == 1


def test_ISTEGE_BAGLI_duzgun_gecis_kapali_yuzde_10_ikisi_kapali_en_ucuz():
    for bay, m_gecmez, m_gecer in (
            (Bayraklar(duzgun_gecis=False), 2.8, 2.6),
            (Bayraklar(duzgun_gecis=False, istege_bagli_esik=False), 3.0,
             2.95)):
        e, b = kur(bay, ilan_C=3.0)
        b.ekle(1)
        ilan(e, 1, 2.0)                         # m = 3,0
        e.sec(0.0, b, False)
        b.ekle(2)
        ilan(e, 2, m_gecmez - 1.0)
        e.sec(1.0, b, False)
        assert e.ardil == 1
        ilan(e, 2, m_gecer - 1.0)
        e.sec(2.0, b, False)
        assert e.ardil == 2


# ==========================================================================
# KK-04/8–9 · döngü bekçisi
# ==========================================================================
def test_BAYAT_BILGI_veri_getirenin_ilani_benimkinden_buyuk_degil():
    e, b = kur(ilan_C=2.0)
    b.ekle(1)
    ilan(e, 1, 1.0)
    e.sec(0.0, b, False)                        # C = 2,0
    e.olay_oku()
    b.ekle(7)
    ilan(e, 7, 3.0)                             # 7'nin ilanı 3,0 > 2,0
    e.veri_duyuldu(7, paket(9, 1, 2), 0.5)
    assert not e.olay_oku() and e.sayac["bayat_bilgi"] == 0
    ilan(e, 7, 2.0)                             # 2,0 ≤ 2,0: bayat
    e.veri_duyuldu(7, paket(9, 2, 2), 1.0)
    e.veri_duyuldu(7, paket(9, 3, 2), 1.1)
    assert e.olay_oku() and e.sayac["bayat_bilgi"] == 1   # selam başına bir
    e.ilan_edildi(0, e.C)
    e.veri_duyuldu(7, paket(9, 4, 2), 1.5)
    assert e.sayac["bayat_bilgi"] == 2
    ilan(e, 1, None)                            # yolum yok: her veri bayat
    e.sec(2.0, b, False)
    e.ilan_edildi(0, e.C)
    e.olay_oku()
    e.veri_duyuldu(7, paket(9, 5, 2), 2.1)
    assert e.olay_oku()


def test_KESIN_DONGU_iki_komsu_dislanir_MAC_tekrari_dongu_degil():
    e, b = kur(ilan_C=3.0)
    for j, C in ((1, 1.0), (2, 2.5), (3, 1.5)):
        b.ekle(j)
        ilan(e, j, C)
    e.sec(10.0, b, False)
    assert e.ardil == 1
    p3 = paket(9, 4, 3)
    e.gonderildi(p3, 1, 10.0)                   # 1'e gönderdim
    e.veri_duyuldu(2, paket(9, 4, 6), 10.3)     # 2 geri getirdi
    e.dongu_denetle(paket(9, 4, 3), 10.3)       # aynı atlama: MAC tekrarı
    assert e.sayac["dongu"] == 0
    e.olay_oku()
    e.dongu_denetle(paket(9, 4, 6), 10.3)
    assert e.sayac["dongu"] == 1 and e.sayac["dislama"] == 2
    assert e.disla == {1: pytest.approx(12.3), 2: pytest.approx(12.3)}
    e.sec(10.3, b, False)
    assert e.ardil == 3 and e.olay_oku()
    e.sec(12.3, b, False)                       # dışlama bitti
    assert 1 not in e.disla and 2 not in e.disla
    assert e.ardil == 1 or e.ardil == 3


def test_DONGU_KAYDI_5_s_sonra_unutulur_kendi_paketim_0_atlamayla():
    e, b = kur(ilan_C=3.0)
    b.ekle(1)
    ilan(e, 1, 1.0)
    e.sec(0.0, b, False)
    benim = paket(5, 1, 0)
    e.gonderildi(benim, 1, 0.0)
    e.dongu_denetle(paket(5, 1, 4), 1.0)        # kendi paketim geri geldi
    assert e.sayac["dongu"] == 1
    e.gonderildi(paket(5, 2, 0), 1, 2.0)
    e.zaman_isle(7.1, b, False)                 # 5 s'den yaşlı kayıt silinir
    e.dongu_denetle(paket(5, 2, 4), 7.1)
    assert e.sayac["dongu"] == 1 and (5, 2) not in e.gonderilen.kayit
