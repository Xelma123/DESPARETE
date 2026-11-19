"""DESPARETE 5 · bağın durumu ve ölçüsü (KK-01) ve bağa ait karıştırma
kanıtı (KK-03 B). Senaryolar kural kâğıtlarının örneklerinden ve bağımsız
denetimin raporlarından (`arsiv/denetim/DENETIM-RAPORU-KURAL-2026-11-17*`).
Simülatörsüz: zaman ve olaylar elle verilir."""

from __future__ import annotations

import math

import pytest

from protokoller.desparete5_bag import (
    ASKIDA, KARISTIRILIYOR, KOTU, OLAGAN, SEBEP_BIT, SEBEP_SESSIZLIK,
    BagTablosu, k_sessizlik, sondaki_sifirsiz)
from protokoller.desparete5_bicim import (
    CEKIRDEK, ESKI_CEKIRDEK, SONSUZ, TAM, Bayraklar, Degerler,
    maliyet_birimi, maliyet_topla, sira_buyuk, sira_farki)

D = Degerler()
# 18 Kasım'ın tam sürümü: eski veri tetiği, askıda, veri cezası (19 Kasım'da
# yeni sürümde kalktı; kodda bayrakla yeniden üretilir).
ESKI_TAM = Bayraklar(vazgecme_tetigi=False, egim=False, duzgun_gecis=False,
                     veri_kotu_tetigi=True)
J = 7
# 16 selamdan 13'ü geldi (KK-01'in örneği): d_r = 13/16 ≈ 0,81.
DESEN_13 = [1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1]


class Komsu:
    """j'nin selamları: 2 s arayla, ilan edilen aralık 2,2 s."""

    def __init__(self, tab: BagTablosu, j: int = J, sira: int = 100,
                 bildirilen: float | None = 0.9) -> None:
        self.tab, self.j, self.sira = tab, j, sira
        self.bildirilen = bildirilen

    def selam(self, t: float, alindi: bool = True, bit: bool = False,
              bildirilen: object = "varsayilan", aralik: float = 2.2) -> None:
        self.tab.zaman_isle(t)
        b = self.bildirilen if bildirilen == "varsayilan" else bildirilen
        if alindi:
            self.tab.selam_al(self.j, t, self.sira, aralik, b, bit)
        self.sira = (self.sira + 1) & 0xFFFF


def kur(bayraklar: Bayraklar = TAM, desen=DESEN_13, t0: float = 0.0):
    """Deseni 2 s arayla besler; son selam t0 + 2·(len − 1)."""
    tab = BagTablosu(D, bayraklar)
    k = Komsu(tab)
    for i, v in enumerate(desen):
        k.selam(t0 + 2.0 * i, alindi=bool(v))
    return tab, k, t0 + 2.0 * (len(desen) - 1)


def bag(tab):
    return tab.baglar[J]


def basarisiz(tab, t, n=1, ara=0.5):
    for i in range(n):
        tab.zaman_isle(t + i * ara)
        tab.veri_sonucu(J, t + i * ara, False, 6, "veri")
    return t + (n - 1) * ara


# ==========================================================================
# Birimler ve yardımcılar
# ==========================================================================
def test_BIRIMLER_KK00_genel_kural_3():
    assert maliyet_birimi(1.5) == 96
    assert maliyet_birimi(1.367) == 88            # 87,49 → yukarı
    assert maliyet_birimi(math.inf) == SONSUZ
    assert maliyet_birimi(5000.0) == 0xFFFE       # sonlu tavan
    assert maliyet_topla(0xFFF0, 0x100) == 0xFFFE
    assert maliyet_topla(10, SONSUZ) == SONSUZ
    assert sira_farki(2, 0xFFFF) == 3 and sira_farki(0xFFFF, 2) == -3
    assert sira_buyuk(1, 0xFFFF) and not sira_buyuk(0xFFFF, 1)


@pytest.mark.parametrize("d_r,k", [(0.9, 3), (0.8, 3), (0.6, 6), (0.5, 7),
                                   (0.25, 16), (1.0, 3), (None, 16)])
def test_K_SESSIZLIK_KK03_6_ornekleri(d_r, k):
    assert k_sessizlik(d_r, 16) == k


def test_BAYRAK_BAGIMLILIKLARI():
    with pytest.raises(ValueError):
        Bayraklar(karistirma_durumu=False)        # bit ve hatıra ona bağlı
    with pytest.raises(ValueError):
        Bayraklar(cogaltma=True)
    with pytest.raises(ValueError):
        Bayraklar(veri_kotu_tetigi=True)          # vazgeçme tetiğiyle birlikte
    assert not CEKIRDEK.karistirma_durumu and CEKIRDEK.vazgecme_tetigi
    assert CEKIRDEK.egim and not CEKIRDEK.veri_kotu_tetigi
    assert ESKI_CEKIRDEK.veri_kotu_tetigi and not ESKI_CEKIRDEK.egim
    assert not ESKI_CEKIRDEK.vazgecme_tetigi and not ESKI_CEKIRDEK.duzgun_gecis


# ==========================================================================
# KK-01/1–5, 11–12 · ölçü ve iki eşik
# ==========================================================================
def test_YENI_KOMSU_KOTUDE_baslar_ORNEK_EN_AZ_ile_doner():
    tab = BagTablosu(D, TAM)
    k = Komsu(tab)
    for i in range(3):
        k.selam(2.0 * i)
        assert bag(tab).durum == KOTU
    k.selam(6.0)                                  # 4. örnek
    assert bag(tab).durum == OLAGAN
    assert tab.bayraklari_oku() == (True, True)


def test_ORNEK_ETX_KK01():
    tab, _, _ = kur()
    assert bag(tab).d_r == pytest.approx(13 / 16)
    assert tab.etx(J) == pytest.approx(1 / (0.8125 * 0.9))   # ≈ 1,37
    assert bag(tab).durum == OLAGAN


def test_ZAMAN_ASIMI_1_5_a_sonra_her_a():
    tab, k, t = kur(desen=[1] * 16)               # son selam t = 30
    tab.zaman_isle(t + 3.29)
    assert list(bag(tab).gecmis)[-1] == 1
    tab.zaman_isle(t + 3.3)
    assert sondaki_sifirsiz(bag(tab).gecmis) != tuple(bag(tab).gecmis)
    tab.zaman_isle(t + 5.5)
    assert list(bag(tab).gecmis)[-2:] == [0, 0]


def test_GERI_ALMA_fazla_sayilan_butun_sifirlar_G4():
    """Olaydan sonra ilan edilen aralık 0,55 s; komşunun gerçek aralığı
    büyüdüğü için zaman aşımları fazla 0 sayar. Geç gelen selam fazlanın
    hepsini geri alır (RFC 8966 Ek A), yalnız sonuncusunu değil.

    Karıştırma kapalı: açıkken üçüncü sıfır sessizlik kanıtı olur ve ölçü
    donar (bu da beklenen davranış; aşağıdaki testlerde)."""
    tab, k, t = kur(CEKIRDEK, desen=[1] * 16)
    k.selam(t + 0.5, aralik=0.55)                 # olay selamı
    n0 = len(bag(tab).gecmis)
    tab.zaman_isle(t + 0.5 + 0.825 + 0.55 * 3 + 1e-6)   # 4 zaman aşımı
    assert list(bag(tab).gecmis)[-4:] == [0, 0, 0, 0]
    # Komşunun gerçekte gönderdiği: bir kayıp, sonra bu selam (sıra +2).
    tab.selam_al(J, t + 3.5, k.sira + 1, 2.2, 0.9, False)
    assert list(bag(tab).gecmis)[-3:] == [1, 0, 1]
    # 4 sıfır en eski 4 kaydı dışarı itti; 3'ü geri alındı: 16 − 3 + 1.
    assert n0 == 16 and len(bag(tab).gecmis) == 14
    # Gölge geçmiş aynı sayımı yapar: 4 zaman aşımı, 3'ü geri alındı.
    assert [v for _, v in bag(tab).ham_olay][-3:] == [1, 0, 1]


def test_YENIDEN_BASLAMA_bosluk_N_den_buyuk():
    tab, k, t = kur(desen=[1] * 16)
    tab.selam_al(J, t + 2.0, k.sira + 40, 2.2, 0.9, False)
    assert list(bag(tab).gecmis) == [1]


def test_IKI_ESIK_OLAGAN_KOTU_ve_donus():
    tab, k, t = kur(desen=[1] * 16)
    # d_f 0,2 bildirilirse ETX = 5 > 4 → KÖTÜ (cezasız).
    k.selam(t + 2.0, bildirilen=0.2)
    assert bag(tab).durum == KOTU and not bag(tab).ceza_bekliyor
    # 0,3 → ETX 3,33: E_DON'un (3) altında değil, KÖTÜ kalır.
    k.selam(t + 4.0, bildirilen=0.3)
    assert bag(tab).durum == KOTU
    k.selam(t + 6.0, bildirilen=0.9)
    assert bag(tab).durum == OLAGAN


def test_KARISTIRMA_KAPALIYKEN_sessiz_komsu_ETXten_KOTU_G3():
    """`karistirma_durumu` kapalıyken "sondaki k sıfır hariç" istisnası
    yok: sessiz komşu silinmeden önce ETX'ten KÖTÜ olur."""
    tab, _, t = kur(CEKIRDEK, desen=[1] * 16)
    tab.zaman_isle(t + 3.3 + 2.2 * 11 - 0.01)     # 11 sıfır: d_r 5/16
    assert bag(tab).durum == OLAGAN
    tab.zaman_isle(t + 3.3 + 2.2 * 11 + 1e-6)     # 12. sıfır: d_r 4/16
    assert bag(tab).durum == KOTU
    assert tab.sayac["kotu_selam"] == 1


def test_SILME_30_s_ve_kendi_durumumda_duraklama():
    tab, _, t = kur(CEKIRDEK, desen=[1] * 16)
    tab.zaman_isle(t + 29.99)
    assert J in tab.baglar
    tab.zaman_isle(t + 30.0)
    assert J not in tab.baglar
    # Duraklama: 10 s'lik dondurma silmeyi 10 s öteler (KK-01/13).
    tab, _, t = kur(desen=[1] * 16)
    tab.kendi_basla(t + 5.0)
    tab.zaman_isle(t + 15.0)
    tab.kendi_bitir(t + 15.0)
    tab.zaman_isle(t + 39.99)
    assert J in tab.baglar
    tab.zaman_isle(t + 40.0)
    assert J not in tab.baglar


# ==========================================================================
# KK-01/6–11 · veri tetiği, ASKIDA, KARIŞTIRILIYOR, ceza
# ==========================================================================
def test_KARISTIRICIYA_COK_YAKIN_ALICI_ASKIDA_sonra_sessizlikle_KARISTIRILIYOR():
    """KK-01'in örneği: j hiç selam gönderemez; dördüncü başarısız
    çerçevede bağ ASKIDA'ya geçer, sessizlik kanıtı süre içinde gelir,
    hatıra ASKIDA'ya girişteki ölçüdür; j dönünce iki temiz selamla ceza-
    sız OLAĞAN. 18 Kasım'ın kuralı (`ESKI_TAM`)."""
    tab, k, t = kur(ESKI_TAM)                     # son selam 30
    snapshot = tuple(bag(tab).gecmis)
    basarisiz(tab, t + 0.5, n=3)
    assert bag(tab).durum == OLAGAN               # 3 çerçeve < VERI_EN_AZ
    basarisiz(tab, t + 2.0)
    b = bag(tab)
    assert b.durum == ASKIDA
    assert b.askida_bitis_t == pytest.approx(t + 2.0 + 4 * 2.2)   # (k+1)·a
    tab.zaman_isle(t + 3.3 + 2.2 * 2 - 0.01)      # iki sıfır
    assert b.durum == ASKIDA
    tab.zaman_isle(t + 3.3 + 2.2 * 2 + 1e-6)      # üçüncü sıfır: k = 3
    assert b.durum == KARISTIRILIYOR and b.sebepler == {SEBEP_SESSIZLIK}
    assert b.hatira == (snapshot, 0.9)            # Y-7
    n = len(b.gecmis)
    tab.zaman_isle(t + 20.0)                      # donuk: sıfır eklenmez
    assert len(b.gecmis) == n and list(b.gecmis)[-1] == 0
    k.sira += 5                                   # karıştırmada kaçanlar
    k.selam(t + 21.0)
    assert b.durum == KARISTIRILIYOR
    k.selam(t + 23.0)
    assert b.durum == OLAGAN
    assert tuple(b.gecmis) == snapshot and tab.etx(J) == pytest.approx(
        1 / (0.8125 * 0.9))
    assert not b.ceza_bekliyor and tab.sayac["veri_kotu"] == 0
    # Dondurmadan çıkıştan sonraki ilk selam: boşluk sayılmaz.
    k.sira += 3
    k.selam(t + 25.0)
    assert list(b.gecmis)[-2:] == [1, 1]


def test_GIRISIM_ALICISI_bitle_KARISTIRILIYOR_ve_iki_temiz_selamla_donus():
    tab, k, t = kur()
    onceki = tuple(bag(tab).gecmis)
    k.selam(t + 2.0, bit=True)
    b = bag(tab)
    assert b.durum == KARISTIRILIYOR and b.sebepler == {SEBEP_BIT}
    assert b.hatira[0] == sondaki_sifirsiz(onceki)   # selamdan önceki ölçü
    k.selam(t + 4.0, bit=True)
    k.selam(t + 6.0)
    k.selam(t + 8.0, bit=True)                    # ardışıklık bozuldu
    k.selam(t + 10.0)
    assert b.durum == KARISTIRILIYOR
    k.selam(t + 12.0)
    assert b.durum == OLAGAN and tuple(b.gecmis) == onceki


def test_ALICI_BILDIRIMI_kapaliyken_bit_okunmaz():
    tab, k, t = kur(Bayraklar(alici_bildirimi=False))
    k.selam(t + 2.0, bit=True)
    assert bag(tab).durum == OLAGAN


def test_HATIRLANAN_KALITE_kapaliyken_donuste_yeniden_olcum():
    tab, k, t = kur(Bayraklar(hatirlanan_kalite=False))
    k.selam(t + 2.0, bit=True)
    k.selam(t + 4.0)
    k.selam(t + 6.0)
    assert bag(tab).durum == KOTU and len(bag(tab).gecmis) == 0
    assert not bag(tab).ceza_bekliyor


def test_ASKIDA_kanitsiz_KOTU_ve_cezanin_katlanmasi():
    """Komşu duyuluyor (kanıt yok), veri bağı kötü: ASKIDA süresi dolunca
    veri sebepli KÖTÜ ve ceza; 60 s içinde yinelenirse 10 → 20 → 40 → 40
    (tavan); 60 s'den sonra yine 10. Eski çerçeveler ceza boyunca 10 s'lik
    veri penceresinden çıkar. 18 Kasım'ın kuralı (`ESKI_TAM`)."""
    tab, k, t = kur(ESKI_TAM, desen=[1] * 16)
    beklenen_ceza = [10.0, 20.0, 40.0, 40.0, 10.0]
    for tur in range(5):
        if tur == 4:                              # 60 s'den uzun sakin dönem
            for _ in range(31):
                t += 2.0
                k.selam(t)
        basarisiz(tab, t + 0.2, n=4, ara=0.2)
        b = bag(tab)
        assert b.durum == ASKIDA
        bitis = b.askida_bitis_t
        while t < bitis:
            t += 2.0
            k.selam(t)
        assert b.durum == KOTU and b.ceza_s == beklenen_ceza[tur]
        assert b.ceza_bitis_t == pytest.approx(bitis + beklenen_ceza[tur])
        while b.durum == KOTU:
            t += 2.0
            k.selam(t)
        assert b.durum == OLAGAN and t >= b.ceza_bitis_t
    assert tab.sayac["veri_kotu"] == 5


def test_KARISTIRMA_KAPALIYKEN_ASKIDA_beklemesi_yok_Y4():
    tab, k, t = kur(ESKI_CEKIRDEK, desen=[1] * 16)
    basarisiz(tab, t + 0.2, n=4, ara=0.2)
    b = bag(tab)
    assert b.durum == KOTU and b.ceza_bekliyor and b.ceza_s == 10.0


def test_AYNI_OLAYDA_SIRA_once_MAC_kaniti_sonra_veri_tetigi():
    """KK-01/15: dördüncü vazgeçme hem MAC kanıtını (3 ardışık, son 2·a'da
    selam yok) hem veri tetiğini sağlıyor; kanıt kazanır (`ESKI_TAM`)."""
    tab, k, t = kur(ESKI_TAM)
    basarisiz(tab, t + 1.0, n=3)
    assert bag(tab).durum == OLAGAN
    tab.zaman_isle(t + 4.5)
    tab.veri_sonucu(J, t + 4.5, False, 6, "veri")
    assert bag(tab).durum == KARISTIRILIYOR
    assert tab.sayac["karisma_mac"] == 1 and tab.sayac["askida_giris"] == 0


def test_KARISTIRILIYOR_ust_suresi_ve_KOTU_donuste_bit_Y8():
    """Komşu 30 s'den uzun karıştırılıyor: bit hep 1. Üst süre dolunca
    geçmiş boşalır, bağ KÖTÜ'den yeniden ölçülür; KÖTÜ'den OLAĞAN'a
    çıkaran selamın biti 1 olduğu için doğrudan KARIŞTIRILIYOR (Y-8)."""
    tab, k, t = kur(desen=[1] * 16)
    giris = t + 2.0
    for i in range(15):                           # giris … giris + 28
        k.selam(giris + 2.0 * i, bit=True)
    b = bag(tab)
    assert b.durum == KARISTIRILIYOR
    k.selam(giris + 30.0, bit=True)               # üst süre bu selamdan önce
    assert b.durum == KOTU and list(b.gecmis) == [1]
    assert tab.sayac["karisma_ust_sure"] == 1
    for i in range(1, 4):
        k.selam(giris + 30.0 + 2.0 * i, bit=True)
    assert b.durum == KARISTIRILIYOR and tab.sayac["karisma_kotuden"] == 1


# ==========================================================================
# KK-01/13 · kendim karıştırılıyorum (Y-2)
# ==========================================================================
def test_KENDI_KARISTIRILMAM_ASKIDAyi_cezasiz_OLAGANa_dondurur_Y2():
    tab, k, t = kur(ESKI_TAM, desen=[1] * 16)
    snapshot = tuple(bag(tab).gecmis)
    basarisiz(tab, t + 0.2, n=4, ara=0.2)
    assert bag(tab).durum == ASKIDA
    k.selam(t + 1.0)                              # ASKIDA'da ölçülür
    tab.kendi_basla(t + 1.5)
    b = bag(tab)
    assert b.durum == OLAGAN and tuple(b.gecmis) == snapshot
    assert len(b.veri) == 0 and not b.ceza_bekliyor
    assert tab.sayac["askida_kendi"] == 1
    # Dondurma: selam yazılmaz, veri sonucu ve zaman aşımı işlenmez.
    k.selam(t + 2.0)
    basarisiz(tab, t + 2.5, n=6, ara=0.2)
    tab.zaman_isle(t + 15.0)
    assert tuple(b.gecmis) == snapshot and b.durum == OLAGAN
    assert len(b.veri) == 0 and b.mac_ardisik == 0
    tab.kendi_bitir(t + 15.0)
    assert b.son_selam_t == t + 15.0
    k.sira += 6                                   # duyulmayan selamlar
    k.selam(t + 16.0)
    assert list(b.gecmis)[-1] == 1 and len(b.gecmis) == 16
    assert list(b.gecmis).count(0) == 0           # boşluk sayılmadı (B-5)


def test_KENDI_DURUMUMDA_yeni_komsunun_ilk_ornegi_yazilmaz():
    tab = BagTablosu(D, TAM)
    tab.kendi_basla(0.0)
    tab.selam_al(9, 1.0, 50, 2.2, 0.9, False)
    assert len(tab.baglar[9].gecmis) == 0 and tab.baglar[9].d_f is None
    tab.kendi_bitir(2.0)
    tab.selam_al(9, 3.0, 55, 2.2, 0.9, False)
    assert list(tab.baglar[9].gecmis) == [1]


# ==========================================================================
# Y-12 · komşu listesi ve "bilinmiyor"
# ==========================================================================
def test_LISTE_en_az_dort_ornekle_ve_bildirimsizlik_bilinmiyor_Y12():
    tab = BagTablosu(D, TAM)
    k = Komsu(tab)
    for i in range(3):
        k.selam(2.0 * i)
    assert tab.liste() == ((), ())
    k.selam(6.0, alindi=False)                    # zaman aşımı 7,7'de
    k.selam(8.0)
    assert tab.liste() == ((J,), (int(0.8 * 255),))
    # Bildirmemek d_f'yi değiştirmez; 30 s bildirmezse d_f tanımsız.
    t = 8.0
    while t < 36.0:
        t += 2.0
        k.selam(t, bildirilen=None)
    assert bag(tab).d_f == 0.9
    k.selam(38.0, bildirilen=None)
    assert bag(tab).d_f is None and tab.etx(J) == math.inf
    assert bag(tab).durum == KOTU and tab.sayac["df_bayat"] == 1


# ==========================================================================
# KK-03/2 · gölge geçmiş ve selam kaybı payı (Y-10)
# ==========================================================================
def test_GOLGE_GECMIS_dondurmadan_bagimsiz_sayar():
    tab, k, t = kur(desen=[1] * 16)               # son selam t = 30
    assert tab.selam_kaybi(t) == 0.0
    tab.kendi_basla(t + 0.5)
    tab.zaman_isle(t + 5.6)                       # 33,3 · 35,5'te ham kayıp
    assert tab.selam_kaybi(t + 5.6) == 1.0        # pencere (31,6; 35,6]
    assert list(bag(tab).gecmis).count(0) == 0    # asıl geçmiş donuk
    # Sıra boşluğu da kayıptır; geri alma gölgede de uygulanır.
    tab.kendi_bitir(t + 6.0)
    tab.selam_al(J, t + 7.0, k.sira + 4, 2.2, 0.9, False)
    olay = [v for _, v in bag(tab).ham_olay]
    assert olay[-1] == 1 and olay.count(0) == 4
    assert tab.selam_kaybi(t + 7.0) == pytest.approx(4 / 5)
    # Tanıdık komşu: son 16 s'de selamı alınmış.
    assert tab.selam_kaybi(t + 30.0) is None


def test_SON_TARIH_en_erken_olay():
    tab, k, t = kur(desen=[1] * 16)
    assert tab.son_tarih() == pytest.approx(t + 3.3)


# ==========================================================================
# KK-01/6–7 · vazgeçme tetiği (19 Kasım)
# ==========================================================================
def gonder(tab, t, sonuclar, ara=0.2, tekrar=6):
    """Veri çerçevesi sonuçları: True gitti (`tekrar` yeniden denemeyle),
    False vazgeçildi."""
    for i, ok in enumerate(sonuclar):
        tab.zaman_isle(t + i * ara)
        tab.veri_sonucu(J, t + i * ara, ok, tekrar if ok else 6, "veri")
    return t + (len(sonuclar) - 1) * ara


def test_VAZGECME_TETIGI_yalniz_vazgecme_sayilir_bag_OLAGAN_kalir():
    """Yeniden denemeyle giden çerçeve başarılıdır; üçüncü vazgeçmede bağ
    "veriye uygun değil" olur ama durumu, ölçüsü ve maliyeti değişmez."""
    tab, k, t = kur(CEKIRDEK, desen=[1] * 16)
    b = bag(tab)
    t = gonder(tab, t + 0.1, [True] * 20)            # hepsi 7. denemede
    assert tab.veriye_uygun(J, t) and tab.sayac["vaz_tetik"] == 0
    t = gonder(tab, t + 0.2, [False, True, False])    # 2 vazgeçme
    assert tab.veriye_uygun(J, t)
    tab.zaman_isle(t + 0.2)                           # aynı anda karşılaştır
    maliyet = tab.maliyet(J)
    t = gonder(tab, t + 0.2, [False])                 # 3. vazgeçme (16'da)
    assert not tab.veriye_uygun(J, t)
    assert b.durum == OLAGAN and tab.maliyet(J) == maliyet
    assert b.vud_bitis_t == pytest.approx(t + D.VAZ_BEKLE_S)
    assert len(b.vaz) == 0 and tab.sayac["vaz_tetik"] == 1
    assert tab.veriye_uygun(J, t + D.VAZ_BEKLE_S)    # bekleme doldu
    assert tab.sayac["vazgecme"] == 3 and tab.sayac["vaz_kayit"] == 24


def test_VAZGECME_PENCERESI_16_cerceve_ve_30_s():
    tab, k, t = kur(CEKIRDEK, desen=[1] * 16)
    # İki vazgeçme 16 çerçeveden eski kalır: tetik yok.
    t = gonder(tab, t + 0.1, [False, False] + [True] * 16 + [False])
    assert tab.veriye_uygun(J, t) and tab.sayac["vaz_tetik"] == 0
    # İki vazgeçme 30 s'den eski kalır: tetik yok.
    tab2, k2, t2 = kur(CEKIRDEK, desen=[1] * 16)
    gonder(tab2, t2 + 0.1, [False, False])
    for i in range(1, 17):                            # bağ OLAĞAN kalsın
        k2.selam(t2 + 2.0 * i)
    gonder(tab2, t2 + 31.0, [False])
    assert tab2.veriye_uygun(J, t2 + 31.0)
    assert tab2.sayac["vaz_tetik"] == 0


def test_VAZGECME_BEKLEMESI_60_s_icinde_katlanir_en_cok_40_s():
    tab, k, t = kur(CEKIRDEK, desen=[1] * 16)
    b = bag(tab)
    beklenen = [5.0, 10.0, 20.0, 40.0, 40.0, 5.0]
    for tur in range(6):
        if tur == 5:                                  # 60 s'den uzun sakin
            for _ in range(31):
                t += 2.0
                k.selam(t)
        t = gonder(tab, t + 0.1, [False, False, False], ara=0.1)
        assert b.vud_sure == beklenen[tur], tur
        t += 1.0
        k.selam(t)
    assert tab.sayac["vaz_tetik"] == 6 and tab.sayac["vaz_katlama"] == 4


def test_VAZGECME_kendi_durumumda_yazilmaz_ve_KARISTIRILIYOR_isareti_kaldirir():
    tab, k, t = kur(desen=[1] * 16)                   # TAM
    b = bag(tab)
    tab.kendi_basla(t + 0.1)
    gonder(tab, t + 0.2, [False] * 5)                 # dondurma: yazılmaz
    assert len(b.vaz) == 0 and tab.veriye_uygun(J, t + 2.0)
    tab.kendi_bitir(t + 2.0)
    k.selam(t + 2.0)
    t = gonder(tab, t + 2.1, [False] * 3, ara=0.1)
    assert not tab.veriye_uygun(J, t) and b.durum == OLAGAN
    k.selam(t + 0.5, bit=True)                        # alıcı: karıştırılıyorum
    assert b.durum == KARISTIRILIYOR
    assert tab.veriye_uygun(J, t + 0.5) and len(b.vaz) == 0
    assert b.son_vud_t == pytest.approx(t) and b.vud_sure == D.VAZ_BEKLE_S


def test_VAZGECME_once_MAC_kaniti_selam_yoksa_KARISTIRILIYOR():
    """KK-01/15: selam da gelmiyorsa vazgeçmeler karıştırma kanıtıdır
    (KK-03/7); selam geliyorsa vazgeçme tetiği."""
    tab, k, t = kur(desen=[1] * 16)                   # TAM; son selam 30
    t1 = gonder(tab, t + 1.0, [False] * 3, ara=0.5)   # 2·a = 4,4 s içinde
    assert bag(tab).durum == OLAGAN and not tab.veriye_uygun(J, t1)
    tab.zaman_isle(t + 4.5)
    tab.veri_sonucu(J, t + 4.5, False, 6, "veri")     # 2·a'dan sonra
    assert bag(tab).durum == KARISTIRILIYOR
    assert tab.sayac["karisma_mac"] == 1 and tab.veriye_uygun(J, t + 4.5)


def test_VAZGECME_TETIGI_kapaliyken_yok():
    tab, k, t = kur(Bayraklar(vazgecme_tetigi=False, karistirma_durumu=False,
                              alici_bildirimi=False, hatirlanan_kalite=False),
                    desen=[1] * 16)
    gonder(tab, t + 0.1, [False] * 6)
    assert tab.veriye_uygun(J, t + 2.0) and tab.sayac["vaz_kayit"] == 0
