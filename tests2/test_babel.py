"""Babel (RFC 8966; hakem babeld 1.14) — tel biçimi, Ek A'nın maliyeti,
uygulanabilirlik, rota seçimi, tetikler, istekler ve uçtan uca koşu
(K-242)."""

from __future__ import annotations

import struct
from types import SimpleNamespace

import pytest

from protokoller.babel import Babel, maliyet, metrik, rxcost
from protokoller.babel_bicim import (
    ACIL_ZAMAN_ASIMI_S, ADRES_TABANI, BABEL, PAKET_UST_SINIRI_B, SONSUZ,
    Guncelleme, Hello, Ihu, RotaIstegi, SiraIstegi, adres, paket_coz,
    paket_kodla, sira_artir, sira_kucuk)
from sim2.gozlem.kontrol import KontrolIstegi, Uyandirma
from sim2.kosum.kosu import Kosu
from sim2.kosum.kurulum import kurulum_yap
from sim2.kosum.sonuc import korunum_bolumu
from sim2.yapilandirma.konfig import Konfig


def _g(t):
    return SimpleNamespace(saat_s=t, paket=None)


def _paketler(niyetler):
    """(hedef, jitter, TLV'ler) — niyetlerdeki Babel paketleri."""
    return [(n.hedef, n.jitter_s, paket_coz(bytes(dict(n.yuk)["babel"])))
            for n in niyetler if isinstance(n, KontrolIstegi)]


def _akit(p, niyetler, t):
    """Kancanın doğrudan paketleri ve tetiklediği tampon boşaltmaları:
    (hedef, acil, TLV'ler). Boşaltma acil olandan başlar; boşalmış tamponun
    eski uyandırması paket üretmez."""
    cikti = [(n.hedef, None, paket_coz(bytes(dict(n.yuk)["babel"])))
             for n in niyetler if isinstance(n, KontrolIstegi)]
    for u in sorted((n for n in niyetler if isinstance(n, Uyandirma)
                     and n.etiket.startswith("bosalt:")),
                    key=lambda u: u.jitter_s):
        acil = u.jitter_s == ACIL_ZAMAN_ASIMI_S
        cikti += [(n.hedef, acil, paket_coz(bytes(dict(n.yuk)["babel"])))
                  for n in p.uyandi(_g(t), u.etiket)
                  if isinstance(n, KontrolIstegi)]
    return cikti


def _yuk(tlvler):
    return (("babel", tuple(paket_kodla(tlvler))),)


# ---------------------------------------------------------------- §4
def test_TLV_BOYUTLARI_RFC8966_4_6():
    """§4.2 başlık 4 B · Hello 8 · IHU (AE 1) 12 · Update (AE 1, /32) tam
    önekle 16, ortak 3 bayt atlanınca 13 · Route Request 8, joker (AE 0) 4 ·
    Seqno Request 20."""
    assert len(paket_kodla([])) == 4
    assert len(paket_kodla([Hello(1, 400)])) == 4 + 8
    assert len(paket_kodla([Ihu(256, 1200, adres(3))])) == 4 + 12
    a, b = adres(1), adres(2)
    assert len(paket_kodla([Guncelleme(a, 32, 1600, 0, 0, a)])) == 4 + 16
    assert len(paket_kodla([Guncelleme(a, 32, 1600, 0, 0, a),
                            Guncelleme(b, 32, 1600, 7, 300, b)])) == 4 + 16 + 13
    assert len(paket_kodla([RotaIstegi(a, 32)])) == 4 + 8
    assert len(paket_kodla([RotaIstegi(0, 0)])) == 4 + 4
    assert len(paket_kodla([SiraIstegi(a, 32, 5, 64, a)])) == 4 + 20
    ham = paket_kodla([Hello(9, 400)])
    assert ham[:4] == bytes((42, 2, 0, 8))                 # Magic · Version
    assert struct.unpack(">BBHHH", ham[4:12]) == (4, 6, 0, 9, 400)
    assert paket_kodla([RotaIstegi(0, 0)])[4:] == bytes((9, 2, 0, 0))


def test_GIDIS_DONUS_ve_R_bayragi_router_id():
    a, b, c = adres(1), adres(2), adres(39)
    tlv = [Hello(65535, 400), Ihu(SONSUZ, 1200, a),
           Guncelleme(a, 32, 1600, 3, 0, a),
           Guncelleme(b, 32, 1600, 4, 512, b),
           Guncelleme(c, 32, 1600, 0, SONSUZ, 0),        # geri çekme
           RotaIstegi(b, 32), RotaIstegi(0, 0), SiraIstegi(c, 32, 9, 64, c)]
    assert paket_coz(paket_kodla(tlv)) == tlv
    # R bayrağı: router-id = 4 sıfır bayt + IPv4 (§4.6.9).
    g = paket_coz(paket_kodla([Guncelleme(a, 32, 1600, 3, 0, a)]))[0]
    assert g.router_id == a == ADRES_TABANI + 2


def test_SIRA_ARITMETIGI_3_2_1():
    assert sira_artir(0xFFFF) == 0
    assert sira_kucuk(0xFFFF, 0) and not sira_kucuk(0, 0xFFFF)
    assert sira_kucuk(1, 2) and not sira_kucuk(2, 2)
    assert not sira_kucuk(0, 0x8000) and not sira_kucuk(0x8000, 0)


def test_PAKET_MTU_ICINDE_BOLUNUR():
    p = Babel(0)
    tlv = [Guncelleme(adres(k), 32, 1600, 0, 0, adres(k)) for k in range(150)]
    paketler = p._paketle(tlv, None, 0.0)
    assert len(paketler) == 2
    boylar = [len(dict(x.yuk)["babel"]) for x in paketler]
    assert all(b <= PAKET_UST_SINIRI_B for b in boylar)
    cozulen = [t for x in paketler
               for t in paket_coz(bytes(dict(x.yuk)["babel"]))]
    assert cozulen == tlv


# ---------------------------------------------------------------- Ek A
def test_ETX_EK_A_2_2_babeld():
    """babeld `neighbour_rxcost` · `neighbour_cost`."""
    assert rxcost(0xFFFF) == 256
    assert rxcost(0xC000) == 0x800000 // 0x4001         # en yeni iki Hello
    assert rxcost(0x0F00) == 0x800000 // (0x0F00 + 1)
    assert rxcost(0x000F) == SONSUZ                     # son 12'de hiç yok
    assert rxcost(0xFFFF, 50.0) == (256 * 30000 + 10000) // 20000
    assert rxcost(0xFFFF, 180.0) == SONSUZ
    assert rxcost(0xFFFF, 39.9) == 256
    assert maliyet(256, 256) == 256 and maliyet(300, 512) == 600
    assert maliyet(256, 100) == 256
    assert maliyet(SONSUZ, 256) == SONSUZ == maliyet(256, SONSUZ)
    assert metrik(256, 0) == 256 and metrik(SONSUZ, 0) == SONSUZ
    assert metrik(40000, 40000) == SONSUZ


def test_HELLO_GECMISI_EK_A_1():
    p = Babel(0)
    p._hello_al(1, Hello(10, 400), 0.0)
    k = p._komsu[1]
    assert k.gecmis == 0x8000 and k.beklenen == 11 and k.hello_son == 6.0
    p._hello_al(1, Hello(13, 400), 1.0)          # 11 ve 12 kaçtı
    assert k.gecmis == 0b1001_0000_0000_0000 and k.beklenen == 14
    p._hello_al(1, Hello(12, 400), 1.5)          # geri: "undo history"
    assert k.beklenen == 13 and k.hello_t == 1.5
    p._hello_al(1, Hello(500, 400), 2.0)         # > 16 fark: yeniden başlamış
    assert p._komsu[1].gecmis == 0x8000
    # Zaman aşımı: 0 biti; 16 kaçırma geçmişi boşaltır, komşu silinir.
    p._zamanlari_isle(2.0 + 6.0)
    assert p._komsu[1].gecmis == 0x4000 and p._komsu[1].hello_t == 8.0
    p._zamanlari_isle(2.0 + 6.0 + 15 * 4.0)
    assert 1 not in p._komsu


def _komsu_hazir(p, n, t=0.0, rx=256):
    """Komşu n: son 16 Hello alındı (rxcost 256), IHU'su rxcost `rx`."""
    for i in range(16):
        p._hello_al(n, Hello(i, 400), t)
    p._ihu_al(n, Ihu(rx, 1200, p._adres), t)


def test_IHU_SIKLIGI_babeld_send_hello():
    """Sırası 3'e bölünen Hello'yla bütün komşulara; öteki Hello'larda son
    4 Hello'dan biri kaçmış ya da txcost ≥ 384 olan komşuya."""
    p = Babel(0)
    _komsu_hazir(p, 1)
    _komsu_hazir(p, 2)
    _komsu_hazir(p, 3, rx=400)                   # txcost ≥ 384
    p._komsu[2].gecmis = 0xBFFF                  # son 4'ün birini kaçırdı
    ihu = []
    for _ in range(3):
        tlv = p._hello_kur(0.0)
        ihu.append(sorted(t.adres for t in tlv if isinstance(t, Ihu)))
    assert ihu[0] == ihu[1] == [adres(2), adres(3)]
    assert ihu[2] == [adres(1), adres(2), adres(3)]     # Hello sırası 3


# ---------------------------------------------------------------- §3.5
def test_UYGULANABILIRLIK_3_5_1_ve_KAYNAK_TABLOSU_3_7_3():
    p = Babel(0)
    o = adres(5)
    assert p._uygulanabilir(o, o, 3, 1000)       # kayıt yok
    p._fd_guncelle(o, o, 3, 500, 0.0)
    assert p._uygulanabilir(o, o, 3, 499)
    assert not p._uygulanabilir(o, o, 3, 500)    # eşit uygulanabilir değil
    assert p._uygulanabilir(o, o, 4, 9999)       # daha yeni sıra
    assert not p._uygulanabilir(o, o, 2, 1)      # eski sıra
    assert p._uygulanabilir(o, o, 2, SONSUZ)     # geri çekme her zaman
    p._fd_guncelle(o, o, 3, 300, 1.0)
    assert p._kaynak[(o, o)][:2] == [3, 300]
    p._fd_guncelle(o, o, 3, 400, 1.0)            # büyük metrik FD'yi bozmaz
    assert p._kaynak[(o, o)][:2] == [3, 300]


def test_SECIM_EK_A_3_ve_YARI_OMUR_4_s():
    """Yeni rotanın ms'i max(m, ∞/2) (babeld): daha iyi yeni rota, ms'i
    seçiliyinkinin altına inene dek seçilmez (iki rota da 32767'den
    yarı ömür 4 s ile iner; hesapla t ≈ 7,75 s)."""
    p = Babel(0)
    o = adres(9)
    _komsu_hazir(p, 1)
    _komsu_hazir(p, 2)
    p._guncelleme_al(1, Guncelleme(o, 32, 1600, 1, 300, o), 0.0)
    p._sec(0.0)
    assert p._secili[o] == 1 and p._rota[o][1].yumusak == SONSUZ // 2
    p._guncelleme_al(2, Guncelleme(o, 32, 1600, 1, 100, o), 0.1)
    for t in (0.1, 4.0, 7.5):
        p._sec(t)
        assert p._secili[o] == 1, t
    p._sec(8.0)
    assert p._secili[o] == 2
    assert p._rota[o][2].yumusak == pytest.approx(
        356 + (32767 - 356) * 2 ** (-7.9 / 4), abs=1e-6)


def test_UYGULANAMAZ_GUNCELLEME_3_5_3_MAY_yok_sayilir_3_8_2_2_istek():
    """Seçili rotanın aynı router-id'li uygulanamaz güncellemesi yok sayılır
    (MAY; kayıt değişmez, rota seçili kalır), ilan edene tek-yayın sıra
    isteği gider (SHOULD); farklı router-id'li olanı seçimden çıkarır (MUST)
    ve kayıp yolu açlık isteğini çoklu-yayın gönderir."""
    p = Babel(0)
    o, x = adres(9), adres(30)
    _komsu_hazir(p, 1)
    p._guncelleme_al(1, Guncelleme(o, 32, 1600, 1, 100, o), 0.0)
    _akit(p, p._bitir(0.0), 0.0)                 # FD = (1, 356)
    assert p._kaynak[(o, o)][:2] == [1, 356]
    p._guncelleme_al(1, Guncelleme(o, 32, 1600, 1, 400, o), 1.0)
    r1 = p._rota[o][1]
    assert p._secili[o] == 1 and (r1.sira, r1.ilan_metrik) == (1, 100)
    istek = [x_ for x_ in p._giden if x_[0] == "tlv"]
    assert len(istek) == 1 and istek[0][2] == 1
    assert istek[0][1].sira == 2 and istek[0][1].router_id == o
    _akit(p, p._bitir(1.0), 1.0)
    assert p._secili[o] == 1                     # m 356, hâlâ seçili
    # Farklı router-id (FD'si olan) ile uygulanamaz → kayıp.
    p._fd_guncelle(o, x, 4, 100, 1.5)
    p._guncelleme_al(1, Guncelleme(o, 32, 1600, 4, 300, x), 2.0)
    assert o not in p._secili and p._kayip_sebebi[o] == "kaynak"
    paket = _akit(p, p._bitir(2.0), 2.0)
    acil = [t for h, a, ts in paket for t in ts if a]
    assert any(isinstance(t, Guncelleme) and t.metrik == SONSUZ for t in acil)
    sira = [t for h, a, ts in paket for t in ts if isinstance(t, SiraIstegi)]
    assert len(sira) == 1 and sira[0].router_id == o and sira[0].sira == 2
    assert p._yeniden[o] == [2.0, 0]


def test_ACLIK_3_8_2_1_ve_geri_cekme_yinelemesi():
    """Geri çekilen seçili rota: acil geri çekme 2 · 4 · 8 s sonra yinelenir,
    çoklu-yayın rota isteği (babeld); uygulanamaz rota varken çoklu-yayın
    sıra isteği (MUST), +2 · +6 · +14 s'de yinelenir (Ek B). Üçü aynı
    çoklu-yayın tamponunda, acil boşaltmayla tek pakette (§3.1)."""
    p = Babel(0)
    o = adres(9)
    _komsu_hazir(p, 1)
    _komsu_hazir(p, 2)
    p._guncelleme_al(1, Guncelleme(o, 32, 1600, 1, 100, o), 0.0)
    _akit(p, p._bitir(0.0), 0.0)                 # FD (1, 356)
    p._guncelleme_al(2, Guncelleme(o, 32, 1600, 1, 900, o), 0.2)
    assert not [x for x in p._giden if x[0] == "tlv"]  # seçili daha iyi
    _akit(p, p._bitir(0.2), 0.2)
    niyet = p.kontrol_alindi(_g(1.0), 1, "BABEL",
                             _yuk([Guncelleme(o, 32, 1600, 0, SONSUZ, 0)]),
                             True)
    paket = _akit(p, niyet, 1.0)
    assert len(paket) == 1
    hedef, acil, tlv = paket[0]
    assert hedef is None and acil
    assert tlv == [Guncelleme(o, 32, 1600, 0, SONSUZ, 0), RotaIstegi(o, 32),
                   SiraIstegi(o, 32, 2, 64, o)]
    # Yinelemeler.
    zaman = []
    for t in [x / 10 for x in range(11, 200)]:
        p._zamanlari_isle(t)
        for tur, veri, hedef, acil_ in p._giden:
            zaman.append((round(t, 1), type(veri).__name__ if tur == "tlv"
                          else "ilan"))
        p._giden.clear()
    assert [t for t, a in zaman if a == "ilan"] == [3.0, 5.0, 9.0]
    assert [t for t, a in zaman if a == "SiraIstegi"] == [3.0, 7.0, 15.0]


def test_SURE_DOLUMUNDA_KAYIP_route_lost_MAY_sira_istegi():
    """Seçili rotanın süresi dolup başka rota kalmayınca (babeld
    `route_lost`): ilk seçimde acil tetik; kayıpta yinelenen geri çekme ve
    eski metrik ≤ ∞/2 olduğu için çoklu-yayın sıra isteği (§3.8.2.1 MAY);
    rota isteği yok."""
    p = Babel(0)
    o = adres(9)
    _komsu_hazir(p, 1)
    p._guncelleme_al(1, Guncelleme(o, 32, 1600, 1, 100, o), 0.0)
    ilk = _akit(p, p._bitir(0.0), 0.0)
    assert ilk == [(None, True, [Guncelleme(o, 32, 1600, 1, 356, o)])]
    p._rota[o][1].bitis = 1.0
    paket = _akit(p, p._bitir(1.0), 1.0)
    assert p._sayac["rota_suresi_doldu"] == 1 and o not in p._secili
    tlv = [(a, t) for h, a, ts in paket for t in ts]
    assert (True, Guncelleme(o, 32, 1600, 0, SONSUZ, 0)) in tlv
    assert [t for a, t in tlv if isinstance(t, SiraIstegi)] == [
        SiraIstegi(o, 32, 2, 64, o)]
    assert not [t for a, t in tlv if isinstance(t, RotaIstegi)]
    assert p._yeniden[o] == [1.0, 0]


def test_TETIK_KURALLARI_babeld_send_triggered_update():
    p = Babel(0)
    o, x = adres(9), adres(30)

    def tetik(rid_eski, m_eski, rid, m):
        p._giden.clear()
        p._yeniden.clear()
        p._tetikle(o, rid_eski, m_eski, rid, 1, m)
        ilan = [a for t, v, h, a in p._giden if t == "ilan"]
        istek = [v for t, v, h, a in p._giden if t == "tlv"]
        tur = (None if not ilan else "yeniden" if o in p._yeniden
               else "acil" if ilan[0] else "normal")
        return tur, istek

    assert tetik(o, 500, x, 500) == ("yeniden", [])          # router-id
    assert tetik(o, 500, o, SONSUZ) == ("yeniden", [RotaIstegi(o, 32)])
    assert tetik(o, 1000, o, 1600) == ("acil", [RotaIstegi(o, 32)])
    assert tetik(o, 1600, o, 2200) == ("normal", [RotaIstegi(o, 32)])
    assert tetik(o, 1000, o, 1300) == (None, [])              # < 384
    assert tetik(o, 2000, o, 1200) == (None, [])              # iyileşme < 1024
    assert tetik(o, 3000, o, 1500) == ("normal", [])
    assert tetik(o, SONSUZ, o, 800) == ("normal", [])         # yeni rota
    p._istek[(o, o)] = SimpleNamespace(sira=1, bitis=99.0, acil_yanit=True)
    assert tetik(o, 800, o, 800) == ("acil", [])              # istek karşılandı


def test_SIRA_ISTEGI_3_8_1_2_kaynak_ve_ara_dugum():
    kaynak = Babel(9)
    o = kaynak._adres
    kaynak._sira_istegi_al(3, SiraIstegi(o, 32, 5, 64, o), 1.0)
    assert kaynak._sira == 1                      # en çok 1 (MUST)
    assert kaynak._giden == [("ilan", o, None, True)]
    ara = Babel(0)
    _komsu_hazir(ara, 1)
    _komsu_hazir(ara, 2)
    ara._guncelleme_al(1, Guncelleme(o, 32, 1600, 1, 100, o), 0.0)
    ara._guncelleme_al(2, Guncelleme(o, 32, 1600, 1, 50, o), 0.0)
    ara._bitir(0.0)
    assert ara._secili[o] == 2
    ara._giden.clear()
    # İstekçi seçili komşu: uygulanabilir öteki rotaya, acil tek-yayın.
    ara._sira_istegi_al(2, SiraIstegi(o, 32, 7, 10, o), 0.5)
    assert ara._giden == [("tlv", SiraIstegi(o, 32, 7, 9, o), 1, True)]
    ara._giden.clear()
    ara._sira_istegi_al(3, SiraIstegi(o, 32, 7, 10, o), 0.6)
    assert not ara._giden, "listede olan istek iletilmemeli"
    ara._sira_istegi_al(3, SiraIstegi(o, 32, 1, 10, o), 0.7)
    assert ara._giden == [("ilan", o, None, True)]   # sıra yetiyor: yanıt
    ara._giden.clear()
    # Liste 65 s sonra boşalır.
    ara._istek[(o, o)].bitis = 1.0
    ara._zamanlari_isle(1.0)
    assert (o, o) not in ara._istek


def test_ILETILEN_ISTEGIN_YANITI_acil_cok_yayin():
    ara = Babel(0)
    o = adres(9)
    _komsu_hazir(ara, 2)
    ara._guncelleme_al(2, Guncelleme(o, 32, 1600, 1, 50, o), 0.0)
    _akit(ara, ara._bitir(0.0), 0.0)
    ara._sira_istegi_al(3, SiraIstegi(o, 32, 7, 10, o), 0.5)
    _akit(ara, ara._bitir(0.5), 0.5)
    assert ara._istek[(o, o)].istekci == 3
    niyet = ara.kontrol_alindi(_g(0.8), 2, "BABEL",
                               _yuk([Guncelleme(o, 32, 1600, 7, 50, o)]), True)
    paket = _akit(ara, niyet, 0.8)
    assert (None, True, [Guncelleme(o, 32, 1600, 7, 306, o)]) in paket
    assert not ara._istek


def test_ROTA_ISTEGI_yanit_ve_SURE_DOLMADAN_istek_7_8():
    p = Babel(0)
    o = adres(9)
    _komsu_hazir(p, 1)
    p._rota_istegi_al(4, RotaIstegi(o, 32), 0.0)
    assert p._giden == [("ilan", o, None, False)]  # çoklu-yayın, acil değil
    assert p._ilan(o, 0.0).metrik == SONSUZ      # rota yok: geri çekme
    p._giden.clear()
    p._guncelleme_al(1, Guncelleme(o, 32, 1600, 1, 100, o), 0.0)
    p._sec(0.0)
    assert p._rota[o][1].bitis == pytest.approx(56.0)
    p._zamanlari_isle(48.9)
    assert not [x for x in p._giden if x[0] == "tlv"]
    p._zamanlari_isle(49.0)
    assert ("tlv", RotaIstegi(o, 32), 1, False) in p._giden
    p._giden.clear()
    p._zamanlari_isle(50.0)
    assert not p._giden                          # tazelenmeden bir kez


def test_JOKER_ISTEK_ve_ACILIS():
    p = Babel(0)
    _komsu_hazir(p, 1)
    p._rota_istegi_al(1, RotaIstegi(0, 0), 10.0)
    tur = [(t, type(v).__name__, h, a) for t, v, h, a in p._giden]
    assert ("tlv", "Ihu", None, False) in tur
    assert ("ilan", "int", None, False) in tur   # tam döküm
    p._giden.clear()
    p._rota_istegi_al(1, RotaIstegi(0, 0), 13.0)  # 4 s dolmadı: yalnız IHU
    assert [t for t, *_ in p._giden] == ["tlv"]
    p._giden.clear()
    p._rota_istegi_al(1, RotaIstegi(0, 0), 14.0)
    assert "ilan" in [t for t, *_ in p._giden]
    # Açılış: Hello, kendi önekim, joker istek bir pakette.
    q = Babel(5)
    ilk = q.zamanlayici_doldu(_g(1.0), "bakim")
    assert any(isinstance(n, Uyandirma) and n.etiket == "acilis" for n in ilk)
    paket = _paketler(q.uyandi(_g(1.3), "acilis"))
    assert len(paket) == 1
    tlv = paket[0][2]
    assert isinstance(tlv[0], Hello)
    assert Guncelleme(q._adres, 32, 1600, 0, 0, q._adres) in tlv
    assert RotaIstegi(0, 0) in tlv


# ---------------------------------------------------------------- uçtan uca
_V = Konfig(kol="t")
_N = 12
_EN = _V.alan_en_m * (_N / _V.dugum_sayisi) ** 0.5


def test_BABEL_uctan_uca_defter_ve_tam_rota():
    kur = kurulum_yap(Konfig(
        kol="test", senaryo="statik-yok", tohum=1000, isinma_s=50.0,
        olcum_bitis_s=70.0, kosu_bitis_s=75.0, dugum_sayisi=_N,
        akis_sayisi=4, alan_en_m=_EN, alan_boy_m=_EN, gorev_grup_sayisi=2,
        gorev_grup_yaricapi_m=(_V.gorev_grup_yaricapi_m * _EN
                               / _V.alan_en_m)))
    protokoller: list[Babel] = []

    def fabrika(i):
        p = Babel(i)
        protokoller.append(p)
        return p

    kosu = Kosu(kur, fabrika)
    kosu.kostur()
    r = korunum_bolumu(kur, kosu.dugumler)
    assert r["korunum_tamam"] and r["mutabakat_tamam"], r
    assert r["teslim"] > 0
    toplam: dict = {}
    for p in protokoller:
        for k, v in p.teshis(0).items():
            toplam[k] = toplam.get(k, 0) + v
    assert toplam["hello_gonderilen"] > 0 and toplam["dokum_gonderilen"] > 0
    assert toplam["joker_alinan"] > 0
    assert toplam["gecersiz_paket"] == 0
    # Durağan, bağlı ağ: her düğüm herkese rota seçmiş.
    assert all(len(p._secili) == _N - 1 for p in protokoller), \
        [len(p._secili) for p in protokoller]
    from sim2.gozlem.teshis import teshis_dogrula
    for p in protokoller:                       # en çok 32 alan
        teshis_dogrula(p.kimlik, p.teshis(p.kimlik))
    assert BABEL.ad == "BABEL"


def test_TAMPON_3_1_BIRLESTIRME_ve_HELLO_TASIR():
    """§3.1 · babeld'in tamponları: aynı kancalarda biriken aynı önekin
    duyuruları tek Update'e iner; acil TLV gelince tampon acil boşalır;
    Hello bekleyen çoklu-yayın tamponunu da taşır ve eski boşaltma
    uyandırması paket üretmez."""
    p = Babel(0)
    o, x = adres(9), adres(12)
    _komsu_hazir(p, 1)
    p._guncelleme_al(1, Guncelleme(o, 32, 1600, 1, 100, o), 0.0)
    p._guncelleme_al(1, Guncelleme(x, 32, 1600, 1, 100, x), 0.0)
    p._bitir(0.0)
    p._tampon.clear()
    for t in (1.0, 1.1, 1.2):                   # üç rota isteği, aynı önek
        p._rota_istegi_al(4, RotaIstegi(o, 32), t)
        normal = [u for u in p._bitir(t) if isinstance(u, Uyandirma)
                  and u.etiket.startswith("bosalt:")]
        assert len(normal) == (1 if t == 1.0 else 0)
    assert list(p._tampon[None].ilan) == [o]
    p._rota_istegi_al(4, RotaIstegi(x, 32), 1.3)
    hello = _paketler(p.uyandi(_g(1.4), "hello"))
    assert len(hello) == 1
    tlv = hello[0][2]
    assert isinstance(tlv[0], Hello)
    assert [t.onek for t in tlv if isinstance(t, Guncelleme)] == [o, x]
    assert None not in p._tampon
    eski = normal_etiket = f"bosalt:h:{p._tampon_nesil}"
    assert not _paketler(p.uyandi(_g(3.0), eski)), normal_etiket


def test_BEKLEYEN_ISTEKLER_TABLOSU_3_2_7_bastirma():
    """§3.2.7: üretilen istek tabloda; bekleyen eşdeğer istek varken aynı
    uygulanamaz güncelleme yeni istek üretmez, istek zaman aşımından
    (2 s) sonra üretir."""
    p = Babel(0)
    o = adres(9)
    _komsu_hazir(p, 1)
    p._guncelleme_al(1, Guncelleme(o, 32, 1600, 1, 100, o), 0.0)
    _akit(p, p._bitir(0.0), 0.0)                 # FD = (1, 356)

    def istekler(t):
        p._giden.clear()
        p._guncelleme_al(1, Guncelleme(o, 32, 1600, 1, 400, o), t)
        sonuc = [v for tur, v, h, a in p._giden if isinstance(v, SiraIstegi)]
        _akit(p, p._bitir(t), t)
        return sonuc

    assert len(istekler(1.0)) == 1
    assert istekler(1.5) == [] and istekler(2.9) == []
    assert p._sayac["sira_istegi_bastirilan"] == 2
    assert len(istekler(3.1)) == 1
    assert not p._istek[(o, o)].acil_yanit
