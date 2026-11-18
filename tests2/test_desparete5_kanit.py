"""DESPARETE 5 · kendi "karıştırılıyorum" durumum (KK-03 A; Y-3, Y-6).
Simülatörsüz: sayaçlar elle verilir."""

from __future__ import annotations

from protokoller.desparete5_bicim import CEKIRDEK, TAM, Degerler
from protokoller.desparete5_kanit import ED, GIRISIM, KendiDurum

D = Degerler()


class Telsiz:
    """Saniyede bir: meşgul payı m, çözülen çerçeve c, selam kaybı s."""

    def __init__(self, k: KendiDurum) -> None:
        self.k, self.t, self.mesgul, self.cozulen = k, 0.0, 0.0, 0
        k.saniye(0.0, 0.0, 0, None)                 # ilk okuma: olay yok

    def saniye(self, m=0.1, c=100, s=0.1):
        self.t += 1.0
        self.mesgul += m
        self.cozulen += c
        return self.k.saniye(self.t, self.mesgul, self.cozulen, s)


def isinmis(bayraklar=TAM, n=5):
    tel = Telsiz(KendiDurum(D, bayraklar))
    for _ in range(n):
        assert tel.saniye() == set()
    return tel


def test_ED_tek_saniyede_girer_tek_isaretsiz_saniyede_cikar():
    tel = isinmis()
    olay = tel.saniye(m=0.9, c=5, s=1.0)
    k = tel.k
    assert olay == {"basladi"} and k.kaynak == ED and k.gonderemez
    assert k.dondurma
    assert tel.saniye(m=0.95, c=3, s=1.0) == set()
    olay = tel.saniye()
    assert olay == {"bitti", "dondurma_bitti", "ed_bitti"}
    assert not k.karistiriliyorum and not k.gonderemez


def test_GIRISIM_iki_ardisik_isaretle_girer_uc_isaretsizle_cikar():
    tel = isinmis()
    assert tel.saniye(c=40, s=0.7) == set()          # 40 < 0,5 × 100
    assert tel.saniye(c=45, s=0.65) == {"basladi"}
    k = tel.k
    assert k.kaynak == GIRISIM and not k.gonderemez
    assert tel.saniye() == set() and tel.saniye() == set()
    assert tel.saniye() == {"bitti", "dondurma_bitti"}


def test_GIRISIM_ISARETI_iki_kosul_birden_ve_ardisiklik():
    tel = isinmis()
    assert tel.saniye(c=40, s=0.3) == set()          # kayıp eşiğin altında
    assert tel.saniye(c=60, s=0.9) == set()          # düşüş yok
    assert tel.saniye(c=40, s=0.7) == set()
    assert tel.saniye(c=60, s=0.7) == set()          # ardışıklık bozuldu
    assert tel.saniye(c=40, s=None) == set()         # s tanımsız: işaret yok
    assert not tel.k.karistiriliyorum


def test_ORTALAMA_yalniz_isaretsiz_saniyelerden():
    tel = isinmis()
    assert tel.k.c_ort == 100
    tel.saniye(m=0.9, c=5, s=1.0)                    # işaretli: girmez
    assert tel.k.c_ort == 100
    tel.saniye(c=70)                                 # işaretsiz: girer
    assert tel.k.c_ort == (5 * 100 + 70) / 6


def test_KAYNAK_ED_isareti_gorulen_saniyede_ED_kalir_Y3():
    """ED alanında girişim işareti de çıkar; aynı saniyede ED görülürse
    kaynak ED kalır. Girişime yalnız ED'siz bir saniyede geçilir; o an
    gönderebilirim, selam hemen gider."""
    tel = isinmis()
    tel.saniye(m=0.9, c=5, s=1.0)
    for _ in range(5):
        assert tel.saniye(m=0.9, c=5, s=1.0) == set()
        assert tel.k.kaynak == ED
    olay = tel.saniye(m=0.3, c=20, s=0.9)            # yalnız girişim
    assert olay == {"ed_bitti"} and tel.k.kaynak == GIRISIM
    assert tel.k.karistiriliyorum and not tel.k.gonderemez
    # Kaynak girişimken çıkış üç işaretsiz saniye ister.
    assert tel.saniye() == set() and tel.saniye() == set()
    assert "bitti" in tel.saniye()


def test_UST_SURE_30_s_dondurma_biter_bit_surer_Y6():
    tel = isinmis()
    tel.saniye(c=40, s=0.7)
    tel.saniye(c=40, s=0.7)                          # giriş
    giris = tel.k.giris_t
    olaylar = []
    while tel.t < giris + 31:
        olaylar.append(tel.saniye(c=40, s=0.7))
    k = tel.k
    assert sum("dondurma_bitti" in o for o in olaylar) == 1
    assert k.karistiriliyorum and not k.dondurma and k.sayac["ust_sure"] == 1
    for _ in range(2):
        tel.saniye()
    assert tel.saniye() == {"bitti"}                 # dondurma zaten bitmişti


def test_KARISTIRMA_KAPALIYKEN_calismaz():
    tel = Telsiz(KendiDurum(D, CEKIRDEK))
    for _ in range(5):
        assert tel.saniye(m=0.99, c=0, s=1.0) == set()
    assert not tel.k.karistiriliyorum
