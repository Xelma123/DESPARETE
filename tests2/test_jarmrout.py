"""JarmRout (Pu 2018) — biçimler, denklemler ve uçtan uca koşu.

Sadakatin ölçüsü (`arsiv/teshis/jarmrout_2026-10-11/tasarim.md`): mesaj
boyutları kaynakların bastığı baytlarla, denklemler makalenin çözümlü
örnekleriyle birebir tutmalı.
"""

from __future__ import annotations

import math

import pytest

from protokoller.jarmrout import (JarmRout, bag_kalitesi, cift_onceligi,
                                  trafik_yuku, yol_uzakligi)
from protokoller.jarmrout_bicim import (AGIRLIK_BAG, AGIRLIK_UZAKLIK,
                                        AGIRLIK_YUK, RERR, RREP, RREQ,
                                        ROTA_ADRES_BAYT, VERI_BASLIK_BAYT)
from sim2.kosum.kosu import Kosu
from sim2.kosum.kurulum import kurulum_yap
from sim2.kosum.sonuc import korunum_bolumu
from sim2.yapilandirma.konfig import Konfig


# ---------------------------------------------------------------- biçimler
@pytest.mark.parametrize("n", [0, 1, 4, 9])
def test_RREQ_boyutu_makalenin_sekil_2si(n):
    """S_id 4 · D_id 4 · pkt_seq 2 · C_hop 1 · H_route 4n · P_coord 4n ·
    L_qt 4 · T_ld 4 = 19 + 8n bayt."""
    yuk = {"kaynak": 1, "hedef": 2, "pkt_seq": 3, "c_hop": n, "l_qt": 0.0,
           "t_ld": 0.0, "h_route": tuple(range(n)), "x": (0,) * n,
           "y": (0,) * n}
    assert RREQ.bayt(yuk) == 19 + 8 * n


@pytest.mark.parametrize("n,m", [(1, 0), (3, 2), (5, 4)])
def test_RREP_ve_RERR_boyutu_RFC_4728(n, m):
    """RREP: DSR başlığı 4 + Route Reply 3 + 4n + Source Route 4 + 4m +
    IP hedef 4 · RERR: 4 + 16 + 4 + 4m (§6.1 · §6.3 · §6.4 · §6.7)."""
    rrep = {"dsr_baslik": 0, "rrep_secenek": 0, "kaynak_rota_secenek": 0,
            "ip_hedef": 1, "yol": tuple(range(n)), "donus": tuple(range(m))}
    assert RREP.bayt(rrep) == 15 + 4 * n + 4 * m
    rerr = {"dsr_baslik": 0, "rerr_secenek": 0, "hata_kaynagi": 1,
            "hata_hedefi": 2, "ulasilamaz": 3, "kaynak_rota_secenek": 0,
            "donus": tuple(range(m))}
    assert RERR.bayt(rerr) == 24 + 4 * m
    assert (VERI_BASLIK_BAYT, ROTA_ADRES_BAYT) == (8, 4)


# ---------------------------------------------------------------- denklemler
def test_BAG_KALITESI_es_5_makalenin_tablo_1i():
    """Tablo 1 (Pu 2018): komşudan en son dört paketin RSSI'ı → LQ."""
    assert bag_kalitesi([-55, -56, -58, -62]) == pytest.approx(7.1875)   # n_a
    assert bag_kalitesi([-65, -70, -68, -63]) == pytest.approx(7.25)     # n_b
    assert bag_kalitesi([-60, -65, -63, -58]) == pytest.approx(7.25)     # n_c
    assert bag_kalitesi([-55, -55, -55, -55]) == 0.0     # kararlı bağ
    assert bag_kalitesi([]) == 0.0


def test_YOL_UZAKLIGI_sekil_1_ve_tablo_3():
    """Şekil 1'in koordinatları → Tablo 3 (Pu 2018): Υ(p, r) 10,0 ·
    Υ(p, q) 6,4 · Υ(q, r) 6,4 (tablo bir ondalıkla basıyor)."""
    p = ((10, 15), (20, 15), (30, 15), (40, 15))
    q = ((18, 10), (32, 10))
    r = ((10, 5), (20, 5), (30, 5), (40, 5))
    assert round(yol_uzakligi(p, r), 1) == 10.0
    assert round(yol_uzakligi(p, q), 1) == 6.4
    assert round(yol_uzakligi(q, r), 1) == 6.4
    assert yol_uzakligi(p, q) == pytest.approx(yol_uzakligi(q, p))
    assert yol_uzakligi((), p) is None


def test_CIFT_ONCELIGI_es_13_sekil_3_ornegi():
    """Şekil 3 (Pu 2018): X (L 7,19 · T 7,75), Y (7,25 · 11,63), Z (7,25 ·
    8,91); Υ(X,Y) 6,5 · Υ(X,Z) 10,0 · Υ(Y,Z) 6,4 → P 7,4638 · 6,8831 ·
    7,7095 ve seçilen çift X–Z (en küçük)."""
    assert (AGIRLIK_BAG, AGIRLIK_YUK, AGIRLIK_UZAKLIK) == (0.2, 0.2, 0.6)
    xy = cift_onceligi(7.19, 7.25, 7.75, 11.63, 6.5)
    xz = cift_onceligi(7.19, 7.25, 7.75, 8.91, 10.0)
    yz = cift_onceligi(7.25, 7.25, 11.63, 8.91, 6.4)
    assert (round(xy, 4), round(xz, 4), round(yz, 4)) == (7.4638, 6.8831,
                                                          7.7095)
    assert xz < xy < yz
    assert cift_onceligi(0.0, 0.0, 0.0, 0.0, None) == pytest.approx(0.6)
    assert cift_onceligi(0.0, 0.0, 0.0, 0.0, 0.0) == math.inf


def test_TRAFIK_YUKU_es_8_tablo_2():
    """Tablo 2 (Pu 2018): T_busy ms · Q_buf paket → TL; γ 0,5 · ε 0,02."""
    assert round(trafik_yuku(7.3619, 15), 4) == 11.6282               # n_a
    assert round(trafik_yuku(6.8976, 8), 4) == 7.7468                 # n_b
    assert round(trafik_yuku(7.1257, 10), 4) == 8.9054                # n_c


def test_YUK_SUZGECI_yalniz_kendi_erisiminde():
    """Eş. 6 · 7 — ölçüm "son ortama erişimden" (K-234). Atılan RREQ
    erişim değildir, süzgeci güncellemez; yeniden yayın günceller. Taşınan
    T_ld süzgeçlerin yayından önceki hâlinden (makale: "current traffic
    load")."""
    from types import SimpleNamespace

    def gozlem(t, mesgul_s, kuyruk):
        return SimpleNamespace(saat_s=t, mesgul_sure_s=mesgul_s,
                               kuyruk_uzunlugu=kuyruk, paket=None,
                               kendi_konum=(100.0, 200.0, 50.0))

    def rreq(sira, ara):
        return tuple({"kaynak": 1, "hedef": 9, "pkt_seq": sira,
                      "c_hop": len(ara), "l_qt": 0.0, "t_ld": 0.0,
                      "h_route": ara, "x": (0,) * len(ara),
                      "y": (0,) * len(ara)}.items())

    def t_ld(niyet):
        assert len(niyet) == 1
        return dict(niyet[0].yuk)["t_ld"]

    j = JarmRout(5)
    # İlk erişim: süzgeçler boş → T_ld 0; ölçümün başlangıcı (meşgul 100 ms).
    assert t_ld(j.kontrol_alindi(gozlem(1.0, 0.100, 4), 2, "RREQ",
                                 rreq(7, (2,)), True)) == 0.0
    # Yinelenen, C_hop'u büyük RREQ atılır — erişim yok, süzgeç aynı.
    assert j.kontrol_alindi(gozlem(1.002, 0.101, 4), 6, "RREQ",
                            rreq(7, (3, 4, 6)), True) == ()
    # İkinci erişim: T_ld bugünkü süzgeçten (T 0 · Q 2) → 1,04; sonra ölçüm
    # önceki erişimden bu yana 10 ms (atılan RREQ araya girmedi).
    assert t_ld(j.kontrol_alindi(gozlem(2.0, 0.110, 0), 2, "RREQ",
                                 rreq(8, (2,)), True)) == pytest.approx(1.04)
    # Üçüncü: T 0,5·10 = 5 ms · Q 0,5·2 = 1 → TL 3,12.
    assert t_ld(j.kontrol_alindi(gozlem(3.0, 0.120, 0), 2, "RREQ",
                                 rreq(9, (2,)), True)) == pytest.approx(3.12)


# ---------------------------------------------------------------- uçtan uca
_V = Konfig(kol="t")
_N = 14
_EN = _V.alan_en_m * (_N / _V.dugum_sayisi) ** 0.5


def test_JARMROUT_uctan_uca_defter_kopya_ve_kaynak_rotasi():
    kur = kurulum_yap(Konfig(
        kol="test", senaryo="statik-yok", tohum=1000, isinma_s=1.2,
        olcum_bitis_s=4.8, kosu_bitis_s=6.0, dugum_sayisi=_N, akis_sayisi=4,
        alan_en_m=_EN, alan_boy_m=_EN, gorev_grup_sayisi=2,
        gorev_grup_yaricapi_m=(_V.gorev_grup_yaricapi_m * _EN
                               / _V.alan_en_m)))
    protokoller: list[JarmRout] = []

    def fabrika(i):
        p = JarmRout(i)
        protokoller.append(p)
        return p

    kosu = Kosu(kur, fabrika)
    kosu.kostur()
    r = korunum_bolumu(kur, kosu.dugumler)
    assert r["korunum_tamam"] and r["mutabakat_tamam"], r
    assert r["teslim"] > 0
    toplam = {}
    for p in protokoller:
        for k, v in p.teshis(0).items():
            toplam[k] = toplam.get(k, 0) + v
    assert toplam["rreq_uretilen"] > 0 and toplam["rrep_uretilen"] > 0
    assert toplam["rotasiz_paket"] == 0
    # J8: iki yol bulunan oturumda aynı paket ikinci yoldan da gider.
    if toplam["iki_yol"]:
        assert r.get("kopya_uretilen", 0) > 0
    # J13: kaynak rotası başlıkta — yönlendirme ek yükü sayıldı.
    assert kur.sayaclar.disa_ver().get("veri_baslik_bayt", 0) > 0
