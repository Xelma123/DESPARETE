"""DESPARETE 5 · rota seçimi, döngüsüzlük, açlık (KK-04) ve bekletme ile
geri iz (KK-05). Senaryolar kâğıtların örneklerinden ve bağımsız denetimin
raporlarından (B-1 zinciri, yok sayma, istek yolu). Simülatörsüz."""

from __future__ import annotations

import pytest

from protokoller.desparete5_bekletme import (
    BEKLET, DUS, GONDER, Bekletme, GeriIz)
from protokoller.desparete5_bicim import (
    CEKIRDEK, DEGERLER_ESKI, SONSUZ, TAM, Bayraklar, Degerler,
    maliyet_birimi)
from protokoller.desparete5_rota import Rota

D = Degerler()
GECIT = 0


class Baglar:
    """KK-01'in tablosunun rota için gereken yüzü."""

    def __init__(self, **komsu) -> None:          # ad → (durum, etx)
        self.k = {int(a[1:]): v for a, v in komsu.items()}

    def kullanilir_mi(self, j):
        return self.k.get(j, (None,))[0] == "olagan"

    def durum(self, j):
        return self.k.get(j, (None,))[0]

    def etx(self, j):
        return self.k[j][1]

    def maliyet(self, j):
        return maliyet_birimi(self.k[j][1])

    def ayarla(self, j, durum, etx=1.0):
        self.k[j] = (durum, etx)


def rota(fd=None, bayraklar=TAM, kimlik=5):
    r = Rota(kimlik, GECIT, D, bayraklar)
    r.fd = fd
    return r


# ==========================================================================
# KK-04/1 · uygulanabilirlik
# ==========================================================================
def test_UYGULANABILIRLIK_KK04_1():
    r = rota()
    assert r.uygulanabilir(7, 500)                # FD yok: hepsi
    r.fd = (7, 128)
    assert r.uygulanabilir(7, 127) and not r.uygulanabilir(7, 128)
    assert r.uygulanabilir(8, 9000)               # daha yeni tur
    assert not r.uygulanabilir(6, 10)             # eski tur
    assert r.uygulanabilir(6, SONSUZ)             # geri çekme her zaman
    r.fd = (0xFFFF, 128)
    assert r.uygulanabilir(0, 500)                # 16 bit, modüler


# ==========================================================================
# KK-04/2–5 · zorunlu ve isteğe bağlı geçiş
# ==========================================================================
def test_KK04_ORNEGI_yedege_aninda_gecis_ya_da_aclik():
    """i'nin FD'si (tur 7, 2,0); ardıl k'nin bağı karıştırılıyor; j (7; 1,8)
    uygulanabilir, m (7; 2,5) değil. i anında j'ye geçer. Yalnız m kalsaydı
    açlık olurdu: tur 8 istenir, çok-yayınla, 0,5 s arayla 3 kez daha;
    açlık sürerse dizi 5 s'de bir yinelenir."""
    r = rota(fd=(7, 128))
    k, j, m = 1, 2, 3
    r.ilanlar = {k: (7, 64), j: (7, 115), m: (7, 160)}
    r.ardil, r.kabul = k, (7, 64)
    b = Baglar(n1=("karistiriliyor", 1.2), n2=("olagan", 1.2),
               n3=("olagan", 1.2))
    r.sec(10.0, b, False)
    assert r.ardil == j and r.C == 77 + 115
    assert r.sayac["zorunlu_gecis"] == 1 and r.istekleri_al() == []
    b.ayarla(j, "kotu", 1.2)
    r.sec(11.0, b, False)
    assert r.ardil is None and r.C == SONSUZ
    assert r.istekleri_al() == [(None, 8, 64)]
    gonderim = []
    for t in (11.5, 12.0, 12.5, 13.0, 15.9):
        r.zaman_isle(t, b, False)
        gonderim += [(t, x) for x in r.istekleri_al()]
    assert [t for t, _ in gonderim] == [11.5, 12.0, 12.5]   # 1 + 3 gönderim
    r.zaman_isle(16.0, b, False)
    assert r.istekleri_al() == [(None, 8, 64)]    # dizi yinelendi
    # Uygulanamaz ilanlı OLAĞAN komşu kalmazsa istek gitmez (B-8).
    b.ayarla(m, "kotu", 1.2)
    r.sec(16.5, b, False)
    assert r.aclik is None
    r.zaman_isle(30.0, b, False)
    assert r.istekleri_al() == []


def test_GERI_CEKME_yok_sayilmaz_ardil_hemen_birakilir_B1():
    """Zincirde X rotasını kaybedip ∞ ilan ederse X'i ardıl kullanan Y bunu
    yok saymaz: hemen yedeğine geçer ya da ∞ ilan eder."""
    r = rota(fd=(3, 200))
    x, z = 1, 2
    r.ilanlar = {x: (3, 100), z: (3, 150)}
    r.ardil, r.kabul = x, (3, 100)
    b = Baglar(n1=("olagan", 1.0), n2=("olagan", 1.0))
    r.sec(0.0, b, False)
    assert r.ardil == x
    r.ilan_al(x, 1.0, 3, SONSUZ)
    assert r.yoksay_bitis == float("inf") and r.istekleri_al() == []
    r.sec(1.0, b, False)
    assert r.ardil == z and r.C == 64 + 150
    r.ilan_al(z, 2.0, 3, SONSUZ)
    r.sec(2.0, b, False)
    assert r.ardil is None and r.ilan() == (3, SONSUZ)     # Y-8: FD'nin turu


def test_YOK_SAYMA_KK04_7_sure_yenilenmez_erken_biter_sonra_uygulanir():
    r = rota(fd=(7, 128))
    k = 1
    r.ilanlar = {k: (7, 64)}
    r.ardil, r.kabul = k, (7, 64)
    b = Baglar(n1=("olagan", 1.0))
    r.ilan_al(k, 10.0, 7, 200)                    # sonlu, uygulanamaz
    assert r.kabul == (7, 64) and r.yoksay_bitis == 15.0
    assert r.istekleri_al() == [(k, 8, 64)]       # tek alıcılı istek
    r.ilan_al(k, 12.0, 7, 210)
    assert r.yoksay_bitis == 15.0 and r.istekleri_al() == []
    r.sec(12.0, b, False)
    assert r.ardil == k and r.C == 64 + 64        # son kabul edilenle
    r.ilan_al(k, 13.0, 7, 100)                    # uygulanabilir → biter
    assert r.kabul == (7, 100) and r.yoksay_bitis == float("inf")
    # Süre dolunca son alınan ilan uygulanır; uygulanamıyorsa bırakılır.
    r.ilan_al(k, 20.0, 7, 300)
    r.zaman_isle(24.9, b, False)
    assert r.kabul == (7, 100)
    r.zaman_isle(25.0, b, False)
    r.sec(25.0, b, False)
    assert r.ardil is None and r.sayac["yoksay_doldu"] == 1


def test_ISTEGE_BAGLI_GECIS_yuzde_10_ve_bayrak_kapali():
    def kur(bayraklar, c_b):
        r = rota(bayraklar=bayraklar)
        r.ilanlar = {1: (1, 136), 2: (1, c_b - 64)}
        r.ardil, r.kabul = 1, (1, 136)
        return r, Baglar(n1=("olagan", 1.0), n2=("olagan", 1.0))
    r, b = kur(TAM, 185)                          # 185 ≥ 0,9 × 200
    r.sec(0.0, b, False)
    assert r.ardil == 1 and r.C == 200
    r, b = kur(TAM, 179)
    r.sec(0.0, b, False)
    assert r.ardil == 2 and r.sayac["istege_bagli_gecis"] == 1
    r, b = kur(Bayraklar(istege_bagli_esik=False), 199)
    r.sec(0.0, b, False)
    assert r.ardil == 2                           # her hesapta en ucuzu


def test_ESIT_MALIYET_mevcut_ardil_dusuk_ETX_kucuk_adres():
    r = rota()
    r.ilanlar = {4: (1, 100), 2: (1, 100), 3: (1, 120)}
    b = Baglar(n4=("olagan", 1.0), n2=("olagan", 1.0), n3=("olagan", 0.69))
    r.sec(0.0, b, False)
    # 3: 45 + 120 = 165 · 2 ve 4: 64 + 100 = 164 → eşit değil; küçük adres 2.
    assert r.ardil == 2
    r.ardil, r.kabul = 4, (1, 100)
    r.sec(1.0, b, False)
    assert r.ardil == 4                           # eşitte mevcut ardıl


# ==========================================================================
# KK-04/6 · ilan ve FD
# ==========================================================================
def test_FD_ilan_edilen_degerle_ve_gecidin_ilani():
    r = rota()
    r.ilan_edildi(7, 192)
    assert r.fd == (7, 192)
    r.ilan_edildi(7, 150)
    r.ilan_edildi(7, 170)
    assert r.fd == (7, 150)                       # aynı turda en küçüğü
    r.ilan_edildi(8, 300)
    assert r.fd == (8, 300)                       # yeni tur
    r.ilan_edildi(8, SONSUZ)
    assert r.fd == (8, 300) and r.son_ilan_C == SONSUZ
    assert r.ilan() == (8, SONSUZ)
    g = Rota(GECIT, GECIT, D, TAM)
    assert g.ilan() == (1, 0) and g.C == 0        # tur 1'den başlar


# ==========================================================================
# KK-04/8–11 · tur isteği
# ==========================================================================
def test_GECIT_turu_yalniz_istekle_ve_en_cok_bir_artirir():
    g = Rota(GECIT, GECIT, D, TAM)
    g.istek_al(3, 0.0, 2, 64)
    assert g.tur_gecit == 2 and g.olay_oku()
    g.istek_al(3, 0.1, 2, 64)
    assert g.tur_gecit == 2 and g.olay_oku()      # turum ≥ istenen: yanıt
    g.istek_al(3, 0.2, 9, 64)
    assert g.tur_gecit == 3                       # en çok 1


def test_ISTEK_yanitlanir_iletilir_bastirilir_ve_istek_yolundan_karsilanir():
    r = rota(fd=(7, 128))
    r.ilanlar = {1: (7, 64)}
    r.ardil, r.kabul, r.C = 1, (7, 64), 128
    b = Baglar(n1=("olagan", 1.0))
    r.istek_al(9, 0.0, 7, 64)
    assert r.olay_oku() and r.istekleri_al() == []        # turum ≥ 7
    r.istek_al(9, 1.0, 8, 64)
    assert r.istekleri_al() == [(1, 8, 63)] and not r.olay_oku()
    r.istek_al(9, 1.5, 8, 64)                     # 1 s içinde ikinci
    assert r.istekleri_al() == [] and r.iletilen[8][0] == 5.5   # Y-11
    r.istek_al(1, 3.0, 9, 64)                     # isteyen ardılım
    r.istek_al(9, 3.0, 9, 1)                      # kalan atlama biter
    assert r.istekleri_al() == []
    # Ardıl yeni turu ilan edince kayıt karşılanır: hemen selam.
    r.ilan_al(1, 4.0, 8, 64)
    r.sec(4.0, b, False)
    assert r.olay_oku() and 8 not in r.iletilen
    assert r.sayac["istek_karsilandi"] == 1
    # Kayıt ISTEK_ANIMSA sonra düşer.
    r.istek_al(9, 10.0, 9, 64)
    r.zaman_isle(13.99, b, False)
    assert 9 in r.iletilen
    r.zaman_isle(14.0, b, False)
    assert 9 not in r.iletilen


def test_ARDILSIZ_dugum_istegi_iletmez_B16():
    r = rota(fd=(7, 128))
    r.istek_al(9, 0.0, 8, 64)
    assert r.istekleri_al() == [] and not r.olay_oku()


def test_KENDIM_KARISTIRILIRKEN_istek_gitmez_cikinca_hemen():
    r = rota(fd=(7, 128))
    r.ilanlar = {3: (7, 160)}
    b = Baglar(n3=("olagan", 1.0))
    r.sec(0.0, b, True)
    assert r.istekleri_al() == [] and r.aclik is None
    r.kendi_bitti(5.0, b)
    assert r.istekleri_al() == [(None, 8, 64)]


def test_ZINCIR_aclik_istegi_gecide_gider_yanit_geri_yayilir():
    """geçit G ← X ← Y, ayrıca Z (Y'nin komşusu, X'i ardıl kullanır). Y'nin
    X bağı kötüleşir; Z'nin ilanı Y için uygulanamaz → açlık. İstek X'ten
    geçide iletilir, geçit turu bir artırır; yeni tur X'e, Z'ye ve Y'ye
    olağan ilanlarla ulaşır, Y yeniden yol bulur. Tur yalnız geçitte artar."""
    G, X, Y, Z = 0, 1, 2, 3
    g = Rota(G, G, D, TAM)
    x, y, z = (Rota(n, G, D, TAM) for n in (X, Y, Z))
    bx = Baglar(n0=("olagan", 1.0), n2=("olagan", 1.0), n3=("olagan", 1.0))
    by = Baglar(n1=("olagan", 1.0), n3=("olagan", 1.0))
    bz = Baglar(n1=("olagan", 2.0), n2=("olagan", 1.0))

    def ilan(gonderen, alicilar, t):
        tur, C = gonderen.ilan()
        gonderen.ilan_edildi(tur, C)
        for r, b in alicilar:
            r.ilan_al(gonderen.kimlik, t, tur, C)
            r.sec(t, b, False)

    ilan(g, [(x, bx)], 0.0)
    ilan(x, [(y, by), (z, bz)], 0.1)
    ilan(z, [(y, by)], 0.2)
    ilan(y, [], 0.3)
    assert (x.ardil, y.ardil, z.ardil) == (G, X, X)
    assert y.fd == (1, 128) and z.ilan() == (1, 192)   # Z: Y için uygulanamaz
    by.ayarla(X, "kotu", 5.0)
    y.sec(1.0, by, False)
    assert y.ardil is None
    (hedef, istenen, kalan), = y.istekleri_al()
    assert (hedef, istenen) == (None, 2)
    for r in (x, z):                               # çok-yayını duyanlar
        r.istek_al(Y, 1.0, istenen, kalan)
    (h, i, k), = x.istekleri_al()
    assert h == G and i == 2 and k == 63
    (h, i, _), = z.istekleri_al()
    assert h == X                                  # Z de ardılına iletir
    x.istek_al(Z, 1.01, i, 63)                     # 1 s içinde: bastırılır
    assert x.istekleri_al() == []
    g.istek_al(X, 1.05, 2, 63)
    assert g.tur_gecit == 2 and g.olay_oku()
    ilan(g, [(x, bx)], 1.1)
    assert x.olay_oku()                            # kaydı karşılandı: hemen selam
    ilan(x, [(z, bz)], 1.2)
    ilan(z, [(y, by)], 1.3)
    assert y.ardil == Z and y.ilan()[0] == 2
    # Tanı: açlık 1,0'da başladı, 1,3'te bitti (karara girmez).
    assert y.sayac["aclik_bitti"] == 1 and y.sayac["aclik_sure_ms"] == 300
    assert x.tur_gecit == 1 and g.tur_gecit == 2   # tur yalnız geçitte


# ==========================================================================
# KK-05 · bekletme ve geri iz
# ==========================================================================
def test_BEKLETME_atlama_basina_2_s_ve_kayit_temizligi():
    """18 Kasım'ın değeri (`DEGERLER_ESKI`, 2 s)."""
    bk = Bekletme(DEGERLER_ESKI, TAM)
    p = (4, 17)
    assert bk.karar(p, 10.0, False) == BEKLET and bk.bekleyen_var
    assert bk.karar(p, 11.99, False) == BEKLET
    assert bk.karar(p, 12.0, False) == DUS and not bk.bekleyen_var
    q = (4, 18)
    bk.karar(q, 20.0, False)
    assert bk.karar(q, 20.5, True) == GONDER and not bk.bekleyen_var
    bk.karar((5, 1), 30.0, False)
    bk.temizle(32.99)
    assert bk.bekleyen_var
    bk.temizle(33.0)                               # TUTMA_EN_COK + 1 s
    assert not bk.bekleyen_var
    kapali = Bekletme(D, Bayraklar(bekletme=False))
    assert kapali.karar(p, 0.0, False) == DUS


def test_BEKLETME_varsayilan_1_s_19_Kasim():
    """KK-00: `TUTMA_EN_COK` 19 Kasım'da 2 → 1 s (telemetri saniyede bir)."""
    assert D.TUTMA_EN_COK_S == 1.0 and DEGERLER_ESKI.TUTMA_EN_COK_S == 2.0
    bk = Bekletme(D, TAM)
    p = (4, 17)
    assert bk.karar(p, 10.0, False) == BEKLET
    assert bk.karar(p, 10.99, False) == BEKLET
    assert bk.karar(p, 11.0, False) == DUS


def test_GERI_IZ_yalniz_daha_yeni_sirayla_tazelik_ve_komsunun_durumu_G1():
    iz = GeriIz(D)
    iz.ogren(9, 2, 10, 100.0)
    assert iz.sonraki(9, 101.0, lambda j: True) == 2
    iz.ogren(9, 3, 9, 100.5)                       # eski sıra: yok sayılır
    assert iz.sonraki(9, 101.0, lambda j: True) == 2
    iz.ogren(9, 3, 11, 100.6)
    assert iz.sonraki(9, 103.6, lambda j: True) == 3
    assert iz.sonraki(9, 103.61, lambda j: True) is None   # bayat (3 s)
    assert iz.sonraki(9, 101.0, lambda j: j != 3) is None  # OLAĞAN değil
    assert iz.sonraki(8, 101.0, lambda j: True) is None    # iz yok
    assert iz.sayac == {"iz_ogrenilen": 2, "iz_eski_sira": 1}
