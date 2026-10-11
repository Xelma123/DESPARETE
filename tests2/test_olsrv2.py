"""OLSRv2 (RFC 7181 · NHDP 6130 · RFC 5444 · DAT 7779) — tel biçimi,
algoritmalar ve uçtan uca koşu.

Sadakatin ölçüsü (`arsiv/teshis/olsrv2_2026-10-11/tasarim.md`): kodlayıcı
RFC 6130 Ek B'nin örnek HELLO'larını bayt bayt üretmeli; MPR kümesi RFC 7181
§18.3'ün özelliklerini, DAT metriği RFC 7779 §10.2'nin formülünü tutmalı.
"""

from __future__ import annotations

import random
from collections import deque
from types import SimpleNamespace

import pytest

from protokoller.olsrv2 import OLSRv2, mpr_sec
from protokoller.olsrv2_bicim import (
    ADRES_TABANI, HELLO, MAXIMUM_METRIC, TC, WILL_ALWAYS, WILL_DEFAULT)
from protokoller.olsrv2_rfc5444 import (
    iletim_icin, mesaj_kodla, metrik_coz, metrik_kodla, paket_coz,
    paket_kodla, zaman_coz, zaman_kodla)
from sim2.kosum.kosu import Kosu
from sim2.kosum.kurulum import kurulum_yap
from sim2.kosum.sonuc import korunum_bolumu
from sim2.yapilandirma.konfig import Konfig

_H = 0x0A000000


# ---------------------------------------------------------------- RFC 5444
def test_RFC6130_EK_B_iki_ornek_HELLO_bayt_bayt():
    """RFC 6130 Ek B: 5 adresli HELLO 45 bayt, kısa biçimi 29 bayt."""
    adres = [_H + 1, _H + 2, _H + 3, _H + 4, _H + 5]
    durum = {_H + 2: b"\x02", _H + 3: b"\x02", _H + 4: b"\x01",
             _H + 5: b"\x00"}                    # HEARD HEARD SYMMETRIC LOST
    it = zaman_kodla(2.0)
    uzun = mesaj_kodla(0, hop_limit=1, hop_count=0, sira=0x1234,
                       mesaj_tlv=[(1, 0, b"\x64"), (0, 0, bytes([it]))],
                       adresler=adres,
                       adres_tlv=[(2, 0, {_H + 1: b"\x00"}), (3, 0, durum)])
    assert uzun == bytes([
        0, 0x73, 0, 45, 1, 0, 0x12, 0x34,              # MF=7 · MAL=3 · 45
        0, 8, 1, 16, 1, 0x64, 0, 16, 1, it,            # VALIDITY · INTERVAL
        5, 128, 3, 0x0A, 0, 0, 1, 2, 3, 4, 5,          # 5 adres, baş 3
        0, 14, 2, 80, 0, 1, 0,                         # LOCAL_IF, indeks 0
        3, 52, 1, 4, 4, 2, 2, 1, 0])                   # LINK_STATUS 1..4
    kisa = mesaj_kodla(0, mesaj_tlv=[(1, 0, b"\x64")], adresler=adres[1:],
                       adres_tlv=[(3, 0, durum)])
    assert kisa == bytes([
        0, 0x03, 0, 29, 0, 4, 1, 0x10, 1, 0x64, 4, 0x80, 3, 0x0A, 0, 0,
        2, 3, 4, 5, 0, 7, 3, 0x14, 4, 2, 2, 1, 0])


def test_ZAMAN_KODU_RFC5497():
    """§5: 6 s (C = 1/1024) → 100 (RFC 6130 Ek B'nin örneği)."""
    assert zaman_kodla(6.0) == 100 and zaman_coz(100) == 6.0
    for t in (0.001, 0.5, 1.25, 2.0, 5.0, 6.0, 15.0, 30.0, 300.0):
        k = zaman_kodla(t)
        assert zaman_coz(k) >= t - 1e-12
        assert k == 0 or zaman_coz(k - 1) < t


def test_METRIK_KODU_RFC7181_6_2():
    """§6.2: (257 + a)·2^b − 256; v'den küçük olmayan en küçük değer."""
    assert metrik_coz(metrik_kodla(1)) == 1
    assert metrik_coz(0x0FFF) == MAXIMUM_METRIC
    for v in (1, 2, 255, 256, 257, 1000, 2097, 2104, 5000, 65535, 10 ** 6,
              MAXIMUM_METRIC):
        k = metrik_kodla(v)
        assert metrik_coz(k) >= v
        assert k == 0 or metrik_coz(k - 1) < v
    kodlar = [metrik_kodla(v) for v in range(1, 50000, 37)]
    assert kodlar == sorted(kodlar)


def test_GIDIS_DONUS_ve_iletme_yalniz_hop_alanlari():
    adres = [_H + i for i in (1, 3, 4, 7, 9, 12)]
    m1 = {_H + 3: b"\x80\x10", _H + 4: b"\x80\x20", _H + 9: b"\xa0\x30"}
    m2 = {_H + 4: b"\x50\x40"}
    kanal = [(3, 0, {a: b"\x01" for a in adres[1:]}),
             (7, 0, m1), (7, 0, m2), (8, 0, {_H + 7: b"\x03"})]
    ham = mesaj_kodla(1, kaynak=_H + 1, hop_limit=255, hop_count=0, sira=9,
                      mesaj_tlv=[(1, 0, b"\x6f"), (8, 0, b"\x00\x05")],
                      adresler=adres, adres_tlv=kanal)
    psn, [m] = paket_coz(paket_kodla([ham], sira=77))
    assert psn == 77 and m.kaynak == _H + 1 and m.sira == 9
    assert m.adresler == tuple(adres)
    assert m.adres_degerleri(_H + 4, 7) == [b"\x80\x20", b"\x50\x40"]
    assert m.adres_degerleri(_H + 9, 7) == [b"\xa0\x30"]
    assert m.adres_degerleri(_H + 7, 8) == [b"\x03"]
    assert m.adres_degerleri(_H + 1, 3) == []
    ilet = iletim_icin(m)
    assert ilet[:8] == ham[:8] and ilet[10:] == ham[10:]
    assert (ilet[8], ilet[9]) == (254, 1)


# ---------------------------------------------------------------- §18 MPR
def _d(y, s, n1, n2_d1, d2):
    adaylar = [n2_d1[y]] if n2_d1[y] is not None else []
    adaylar += [n1[x][1] + d2[(x, y)] for x in s if (x, y) in d2]
    return min(adaylar) if adaylar else None


@pytest.mark.parametrize("tohum", range(40))
def test_MPR_KUMESI_RFC7181_18_3_ozellikleri(tohum):
    """Ek B'nin çıktısı §18.3'ü tutar: WILL_ALWAYS içinde; her y için
    d(y, M) = d(y, N1)."""
    r = random.Random(tohum)
    x_say, y_say = r.randint(1, 9), r.randint(1, 14)
    n1 = {x: (r.choice((1, WILL_DEFAULT, WILL_DEFAULT, WILL_ALWAYS)),
              r.randint(1, 9)) for x in range(x_say)}
    ys = range(100, 100 + y_say)
    d2 = {(x, y): r.randint(1, 9) for x in n1 for y in ys
          if r.random() < 0.35}
    n2 = {y: (r.randint(1, 20) if r.random() < 0.3 else None)
          for (_x, y) in d2}
    m = mpr_sec(n1, n2, d2)
    assert {x for x, (w, _d1) in n1.items() if w == WILL_ALWAYS} <= m
    for y in n2:
        assert _d(y, m, n1, n2, d2) == _d(y, n1, n1, n2, d2)


def test_MPR_tek_kapsayan_ve_kisa_yol_korunur():
    """y1'e yalnız a erişir (adım 2); y2'ye b'den (1 + 1) c'den (1 + 5)
    ucuz — en kısa uzaklık korunur; c gereksiz."""
    n1 = {1: (WILL_DEFAULT, 1), 2: (WILL_DEFAULT, 1), 3: (WILL_DEFAULT, 1)}
    d2 = {(1, 101): 1, (2, 102): 1, (3, 102): 5}
    assert mpr_sec(n1, {101: None, 102: None}, d2) == {1, 2}


# ---------------------------------------------------------------- DAT
def test_DAT_METRIGI_RFC7779_10_2():
    """L_in_metric = (2^24/8)·min(toplam/alınan, 8)/(hız/1000); kayıp HELLO
    aralıkları alınanı ölçekler; alınan < 1 → MAXIMUM_METRIC."""
    p = OLSRv2(0)

    def bag(alinan, toplam, kayip=0, aralik=None):
        return SimpleNamespace(
            alinan=deque([0] * 63 + [alinan], maxlen=64),
            toplam=deque([0] * 63 + [toplam], maxlen=64),
            hello_araligi=aralik, paket_zamani=float("-inf"),
            kayip_aralik=kayip, son_psn=1, in_metrik=None)

    p._bag = {1: bag(10, 12), 2: bag(10, 12, kayip=4, aralik=2.0),
              3: bag(0, 5), 4: bag(1, 100)}
    p._dat_yenile(0.0)
    assert p._bag[1].in_metrik == int((1 << 24) / 8 * 1.2 / 1000)   # 2516
    assert p._bag[2].in_metrik == int((1 << 24) / 8 * (12 / 8.75) / 1000)
    assert p._bag[3].in_metrik == MAXIMUM_METRIC
    assert p._bag[4].in_metrik == int((1 << 24) / 8 * 8.0 / 1000)  # tavan
    assert list(p._bag[1].alinan)[-1] == 0                  # kuyruk kaydı


# ---------------------------------------------------------------- NHDP
def _gozlem(t):
    return SimpleNamespace(saat_s=t, paket=None)


def _hello(p, t):
    return p._hello_kur(t).yuk


def test_IKI_DUGUM_HELLO_ile_simetrik_bag_ve_metrikler():
    """A'nın HELLO'su B'de bağı HEARD yapar; B'nin HELLO'su A'yı HEARD
    ilan eder → A'da SYMMETRIC, L_out_metric B'nin ilan ettiği gelen
    metrik; A'nın sonraki HELLO'su B'de SYMMETRIC (§12.5 · §15.3.2.1)."""
    a, b = OLSRv2(0), OLSRv2(1)
    b.kontrol_alindi(_gozlem(0.1), 0, "HELLO", _hello(a, 0.1), True)
    assert b._durum(b._bag[0], 0.1) == 2                    # HEARD
    assert b._bag[0].in_metrik == MAXIMUM_METRIC           # §15.3.2.1
    a.kontrol_alindi(_gozlem(0.2), 1, "HELLO", _hello(b, 0.2), True)
    assert a._durum(a._bag[1], 0.2) == 1                    # SYMMETRIC
    assert a._bag[1].out_metrik == metrik_coz(metrik_kodla(MAXIMUM_METRIC))
    assert a._komsu[1].simetrik
    b.kontrol_alindi(_gozlem(0.3), 0, "HELLO", _hello(a, 0.3), True)
    assert b._durum(b._bag[0], 0.3) == 1 and b._komsu[0].simetrik
    # Rota: tek atlama, metrik N_out_metric.
    b._guncelle(0.3)
    assert b._rota[0][0] == 0 and b._rota[0][2] == 1
    # H_HOLD_TIME (6 s) boyunca HELLO gelmezse bağ düşer, komşu silinir.
    b._guncelle(6.31)
    assert 0 not in b._komsu and 0 not in b._rota


def test_TC_ANSN_eski_atilir_COMPLETE_eskileri_temizler():
    """§16.3.3.1: AR_seq > ANSN → at · §16.3.4.1: ANSN'i eski demetler
    silinir."""
    p = OLSRv2(0)

    def tc(ansn, komsular, sira):
        adres = sorted(ADRES_TABANI + k + 1 for k in komsular)
        ham = mesaj_kodla(
            1, kaynak=ADRES_TABANI + 5 + 1, hop_limit=255, hop_count=0,
            sira=sira,
            mesaj_tlv=[(1, 0, bytes([zaman_kodla(15.0)])),
                       (8, 0, ansn.to_bytes(2, "big"))],
            adresler=adres,
            adres_tlv=[(9, 0, {x: b"\x03" for x in adres}),
                       (7, 0, {x: (0x1000 | metrik_kodla(3000)).to_bytes(
                           2, "big") for x in adres})])
        return paket_coz(paket_kodla([ham], sira=1))[1][0]

    p._tc_isle(tc(10, (7, 8), 1), 1.0)
    assert set(p._tr) == {(5, 7), (5, 8)}
    p._tc_isle(tc(9, (9,), 2), 1.1)                          # eski ANSN
    assert set(p._tr) == {(5, 7), (5, 8)} and p._sayac["tc_eski"] == 1
    p._tc_isle(tc(11, (8,), 3), 1.2)                         # yeni, COMPLETE
    assert set(p._tr) == {(5, 8)} and p._tr[(5, 8)][0] == 11


# ---------------------------------------------------------------- uçtan uca
_V = Konfig(kol="t")
_N = 14
_EN = _V.alan_en_m * (_N / _V.dugum_sayisi) ** 0.5


def test_OLSRv2_uctan_uca_defter_ve_tam_rota():
    kur = kurulum_yap(Konfig(
        kol="test", senaryo="statik-yok", tohum=1000, isinma_s=8.0,
        olcum_bitis_s=18.0, kosu_bitis_s=20.0, dugum_sayisi=_N,
        akis_sayisi=4, alan_en_m=_EN, alan_boy_m=_EN, gorev_grup_sayisi=2,
        gorev_grup_yaricapi_m=(_V.gorev_grup_yaricapi_m * _EN
                               / _V.alan_en_m)))
    protokoller: list[OLSRv2] = []

    def fabrika(i):
        p = OLSRv2(i)
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
    assert toplam["hello_uretilen"] > 0 and toplam["tc_uretilen"] > 0
    assert toplam["tc_iletilen"] > 0 and toplam["gecersiz_mesaj"] == 0
    # Durağan, bağlı ağ: her düğüm herkese rota bilir.
    assert all(len(p._rota) == _N - 1 for p in protokoller), \
        [len(p._rota) for p in protokoller]
    assert {HELLO.ad, TC.ad} == {"HELLO", "TC"}
