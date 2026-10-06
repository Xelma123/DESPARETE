"""
DESPARETE — gerçeklemenin kapıları. Aşama 3, parça parça (`v2/04` K-150 · K-152).

Bölümler: M0.1 metrik profili (`35` §8'in test vektörleri) · mesaj biçimleri
(`19` §14'ün bayt sayıları). M0.1 vektörleri iki biçimde sınanır:

  · SOYUT — belgenin verdiği Q · H · N_Q · yaş değerleri doğrudan saf
    fonksiyonlara girer. Belgenin kendi hesabının kurallarla tutarlı olup
    olmadığını sınar.
  · UÇTAN UCA — aynı durum, düğümün MAC'inden gelecek gerçek sonuç dizisiyle
    (`BagOlcumu`) kurulur. Gerçeklemenin kuralları uyguladığını sınar.

🔴 Belgenin iki vektörü (TV-02 · TV-03) uçtan uca KURULAMAZ: verdikleri Q ya
da epoch değerleri, gerçek bağ sonuçlarının skor kümesinden (255 · 127 ·
85 · 63 · …) elde edilemiyor. Onlar için aynı yolu sınayan, gerçeklenebilir
bir dizi kullanılır — neden, testin yanında yazılı.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from protokoller.desparete_metrik import (  # noqa: E402
    SONLU_UST, SONSUZ, T_EPOCH_S, BagOlcumu, Olcum, c_kalite, c_risk, hazard,
    maliyet, sat_add, skor, u_ornek, u_yas)


def _epochlar(*gruplar: tuple[int, ...], bas_s: float = 0.0) -> Olcum:
    """Her grup bir epoch: sonuçlar epoch içine eşit aralıkla yerleşir.

    Grup öğesi bir TEKRAR sayısıdır; `None` başarısız sonuç demektir.
    Dönen: son epoch işleminin ölçümü.
    """
    b = BagOlcumu()
    olcum = None
    for k, grup in enumerate(gruplar):
        t0 = bas_s + k * T_EPOCH_S
        for m, tekrar in enumerate(grup, start=1):
            t = t0 + m * T_EPOCH_S / (len(grup) + 1)
            b.sonuc(t, tekrar is not None, tekrar or 0)
        olcum = b.epoch(t0 + T_EPOCH_S)
    return olcum


# ==========================================================================
# Tablolar ve saf fonksiyonlar — `35` §3–§4
# ==========================================================================
def test_skor_BELGENIN_formulu():
    assert [skor(r) for r in range(5)] == [255, 127, 85, 63, 51]
    with pytest.raises(ValueError):
        skor(-1)


@pytest.mark.parametrize("q, ceza", [(255, 0), (224, 0), (223, 2), (192, 2),
                                     (191, 4), (160, 4), (159, 8), (128, 8),
                                     (127, 16), (96, 16), (95, 32), (64, 32),
                                     (63, 64), (32, 64), (31, 128), (0, 128)])
def test_KALITE_cezasi_tablonun_HER_sinirinda(q, ceza):
    assert c_kalite(q) == ceza


@pytest.mark.parametrize("r, ceza", [(0, 0), (31, 0), (32, 2), (63, 2),
                                     (64, 4), (95, 4), (96, 8), (127, 8),
                                     (128, 16), (159, 16), (160, 32),
                                     (191, 32), (192, 64), (223, 64),
                                     (224, 128), (255, 128)])
def test_RISK_cezasi_tablonun_HER_sinirinda(r, ceza):
    assert c_risk(r) == ceza


def test_tablo_DISI_deger_REDDEDILIR():
    """`35` §4.2: tablo dışı değer geçersizdir — sessizce kırpılmaz."""
    for kotu in (-1, 256, 1.5):
        with pytest.raises(ValueError):
            c_kalite(kotu)
        with pytest.raises(ValueError):
            c_risk(kotu)


@pytest.mark.parametrize("yas, u", [(None, 255), (0.0, 0), (0.4999, 0),
                                    (0.5, 32), (0.9999, 32), (1.0, 64),
                                    (1.5, 128), (1.9999, 128), (2.0, 192),
                                    (2.9999, 192), (3.0, 255), (9.0, 255)])
def test_U_YAS_yari_acik_araliklar(yas, u):
    assert u_yas(yas) == u


@pytest.mark.parametrize("n, u", [(16, 0), (12, 0), (11, 32), (8, 32),
                                  (7, 64), (4, 64), (3, 128), (1, 128),
                                  (0, 255)])
def test_U_ORNEK_tablosu(n, u):
    assert u_ornek(n) == u


def test_HAZARD_yalniz_SUREKLI_kotulesmede():
    """`35` §3.3: tek düşüş, yetersiz örnek ya da düz epoch H yükseltmez."""
    assert hazard([(224, 4), (176, 4), (112, 4)]) == 112
    assert hazard([(224, 4), (176, 3), (112, 4)]) == 0     # bir epoch < 4
    assert hazard([(224, 4), (224, 4), (112, 4)]) == 0     # ilk düşüş 0
    assert hazard([(112, 4), (176, 4), (112, 4)]) == 0     # önce yükseliş
    assert hazard([(176, 4), (112, 4)]) == 0               # iki epoch
    assert hazard([(255, 9), (127, 9), (0, 9)]) == 255     # doygunluk


# ==========================================================================
# `35` §8 — test vektörleri
# ==========================================================================
def test_TV01_uctan_uca():
    """Dört sonuç: r=0 · r=1 · r=3 başarılı, bir başarısız → Q 111, ceza 16."""
    o = _epochlar((0, 1, 3, None))
    assert o.q == 111 and c_kalite(o.q) == 16 and o.n_q == 4


def test_TV02_BELGEDEKI_hali_KURALLARLA_40_DEGIL_28_verir():
    """🔴 K-152 §4 — belgenin vektörü kendi kurallarıyla çelişiyor.

    Vektör: üç epoch, her birinde N ≥ 4, q = 224 · 176 · 112, N_Q = 12,
    beklenen C = 40 (kalite cezası 16). N_Q = 12 ve her epochta en az dört
    sonuç → her epochta TAM dört sonuç; Q (§3.2) on iki sonucun ortalaması,
    yani epoch toplamlarının `[4q ; 4q + 3]` aralığından 170 ya da 171.
    İkisi de ceza 4 verir → C = 28. 40, Q'yu yalnız son epochtan (112)
    hesaplamaktan çıkar — Q'yu tanımlayan metinle (`35` §3.2 · `36` §4)
    çelişen tek yer bu vektör.
    """
    h = hazard([(224, 4), (176, 4), (112, 4)])
    assert h == 112
    alt = 4 * (224 + 176 + 112)
    q_olasi = {t // 12 for t in range(alt, alt + 10)}
    assert q_olasi == {170, 171}
    assert {maliyet(q, h) for q in q_olasi} == {28}      # U = 0 → R = H
    assert maliyet(112, h) == 40, "belgenin 40'ı yalnız Q = son epoch ise"


def test_TV02_224_ve_176_DORT_sonucla_KURULAMAZ():
    """Skor kümesi 255 · 127 · 85 · … — dört sonucun ortalaması 224 ya da
    176'ya düşemez; vektör bu yüzden uçtan uca sınanamazdı. Tekrar üst sınırı
    burada 63 alındı: iddia simülatörün yeniden deneme sınırına (4) bağlı
    değildir. (112 ise tekrarı 6 ve 7 olan sonuçlarla kurulabiliyor.)"""
    from itertools import combinations_with_replacement as kombinasyon
    kume = sorted({skor(r) for r in range(64)} | {0})
    ortalamalar = {sum(c) // 4 for c in kombinasyon(kume, 4)}
    assert 224 not in ortalamalar and 176 not in ortalamalar
    assert 111 in ortalamalar


def test_TV02_DUZELTILMIS_uctan_uca():
    """Aynı yol, gerçek sonuçlarla: q = 223 · 175 · 111 → H = 112 (belgeyle
    aynı), N_Q = 12, U = 0, Q = floor(2037 / 12) = 169 → ceza 4 → C = 28."""
    o = _epochlar((0, 0, 0, 1), (0, 0, 1, 3), (0, 1, 3, None))
    assert (o.h, o.u, o.r, o.n_q) == (112, 0, 112, 12)
    assert o.q == 169 and c_kalite(o.q) == 4 and c_risk(o.r) == 8
    assert o.c == 28


def test_TV03_soyut():
    """Q = 240, N_Q = 2, yaş 0,6 s → U = max(32, 128) = 128, C = 32."""
    u = max(u_yas(0.6), u_ornek(2))                      # H = 0 → R = U
    assert u == 128
    assert c_kalite(240) == 0 and c_risk(128) == 16 and maliyet(240, 128) == 32


def test_TV03_uctan_uca_GERCEKLENEBILIR_hali():
    """İki sonuçla Q = 240 KURULAMAZ (iki skorun ortalaması 255, 191, 170 …).
    Aynı yol — az örnek + taze olmayan son sonuç, kalite cezası 0 — iki ilk
    denemede başarıyla: Q = 255, U = 128, C = 32. Epoch başına iki sonuç
    olduğundan H yükselemez (yalnız CautionEvidence, belgedeki gibi)."""
    b = BagOlcumu()
    b.sonuc(0.1, True, 0)
    b.sonuc(0.4, True, 0)
    o = b.epoch(1.0)                       # son sonuç yaşı 0,6 s
    assert (o.q, o.h, o.u, o.r, o.c, o.n_q) == (255, 0, 128, 128, 32, 2)


def test_TV04_soyut():
    """Son Q = 200, N_Q = 0, yaş 2,2 s → U = 255, C = 16 + 2 + 128 = 146."""
    assert max(u_yas(2.2), u_ornek(0)) == 255
    assert maliyet(200, 255) == 146


def test_TV04_uctan_uca_SESSIZLIK_iyi_kalite_SAYILMAZ():
    """`35` §3.2: N_Q = 0 iken eski Q korunur ama U = 255 olur. Q = 223
    (dört sonuç) aynı ceza bandında (2): 2,1 s sessizlikten sonra C = 146."""
    b = BagOlcumu()
    for t, r in ((0.1, 0), (0.2, 0), (0.3, 0), (0.4, 1)):
        b.sonuc(t, True, r)
    assert b.epoch(0.5).q == 223
    for t in (1.0, 1.5, 2.0):
        b.epoch(t)
    o = b.epoch(2.5)                       # yaş 2,1 s · pencerede sonuç yok
    assert (o.q, o.u, o.r, o.c, o.n_q) == (223, 255, 255, 146, 0)


def test_TV05_doygunluk_SONSUZ_verir():
    assert sat_add(0xFFFFFFE0, 40) == SONSUZ
    assert sat_add(SONLU_UST - 40, 40) == SONLU_UST     # sınır sonlu
    assert sat_add(SONSUZ, 0) == SONSUZ


def test_TV06_simulasyonda_KAPSAM_DISI():
    """Profil ön-kabulü (preflight) görev öncesi bir işlemdir; simülasyonda
    bütün düğümler aynı profili YAPI GEREĞİ taşır (K-150 §2: roster ve profil
    kabulü kabul edilmiş sayılır). Burada sınanacak bir yol yok — beyan."""


# ==========================================================================
# Kuralların kenarları
# ==========================================================================
def test_ILK_sonuctan_once_METRIK_KAYNAGI_OLAMAZ():
    """`35` §3.2: ilk uygun sonuç yoksa Q tanımsız — maliyet yok."""
    o = BagOlcumu().epoch(0.5)
    assert o.q is None and o.c is None and o.u == 255


def test_pencerede_EN_YENI_16_sonuc():
    """20 sonuçtan en yeni 16'sı: 4 başarısız (eski) dışarıda kalır."""
    b = BagOlcumu()
    for k in range(4):
        b.sonuc(0.01 * (k + 1), False, 0)
    for k in range(16):
        b.sonuc(0.1 + 0.01 * k, True, 0)
    o = b.epoch(0.5)
    assert o.n_q == 16 and o.q == 255


def test_pencere_YARI_ACIK_eski_sonuc_DUSER():
    """`(şimdi − 2,0 ; şimdi]` — tam 2,0 s önceki sonuç pencerede değil."""
    b = BagOlcumu()
    b.sonuc(0.5, True, 0)
    b.epoch(0.5)
    assert b.epoch(2.0).n_q == 1
    assert b.epoch(2.5).n_q == 0


# ==========================================================================
# Biçimler — `19` §2–§11 · §14: bayt sayıları ALANLARDAN türer
# ==========================================================================
def test_BICIM_boylari_belgenin_en_kucuk_baslik_tablosuyla_ayni():
    """`19` §14'ün uzantısız sütunu — DFSN_REQUEST dışında birebir.

    DFSN_REQUEST: belge 72 yazıyor, kendi alan diyagramı 76 ediyor; burada
    diyagram izlendi (`desparete_bicim.py` başlığı · K-152 §6).
    """
    from protokoller.desparete_bicim import (DATA, DFSN_REQUEST,
                                             FAILURE_REPORT, FIELD_SOLICIT,
                                             FIELD_UPDATE, PROBE, PROBE_REPLY)
    beklenen = ((DATA, 36), (FIELD_UPDATE, 60), (FIELD_SOLICIT, 52),
                (DFSN_REQUEST, 76), (PROBE, 40), (PROBE_REPLY, 52),
                (FAILURE_REPORT, 84))
    for bicim, bayt in beklenen:
        assert bicim.sabit_bit % 8 == 0, f"{bicim.ad}: bayta oturmuyor"
        assert bicim.bayt({}) == bayt, f"{bicim.ad}: {bicim.bayt({})} ≠ {bayt}"


def test_BICIM_ortak_bloklar_ve_turler():
    """Her kontrol biçimi 4 bayt taban + 24 bayt gönderen bloğuyla başlar;
    tür numaraları `19` §3'teki gibi ve birbirinden ayrı."""
    from protokoller.desparete_bicim import (
        KONTROL_BICIMLERI, SURUM, TIP_DATA, TIP_DFSN_REQUEST,
        TIP_FAILURE_REPORT, TIP_FIELD_SOLICIT, TIP_FIELD_UPDATE, TIP_PROBE,
        TIP_PROBE_REPLY)
    assert SURUM == 1
    tipler = (TIP_DATA, TIP_FIELD_UPDATE, TIP_FIELD_SOLICIT, TIP_DFSN_REQUEST,
              TIP_PROBE, TIP_PROBE_REPLY, TIP_FAILURE_REPORT)
    assert tipler == tuple(range(7))
    ilk = [a for a, _ in KONTROL_BICIMLERI[0].alanlar[:9]]
    for bicim in KONTROL_BICIMLERI:
        assert [a for a, _ in bicim.alanlar[:9]] == ilk
        assert sum(b for _, b in bicim.alanlar[:9]) == (4 + 24) * 8
    assert len({b.ad for b in KONTROL_BICIMLERI}) == 6


def test_VERI_BASLIGI_alanlardan_36_ve_K151_Y2_ile_odenir():
    """Protokolün simülatöre bildireceği başlık baytı elle yazılmaz."""
    from protokoller.desparete_bicim import DATA, VERI_BASLIK_BAYT
    assert VERI_BASLIK_BAYT == DATA.bayt({}) == 36


def test_KONTROL_ISTEGI_bicimle_kurulur_ve_boyut_ODENIR():
    """Simülatörün sözleşmesi: yük alanları biçimle aynı, değer alana sığar,
    boyut biçimden. Potansiyelin ∞ kodu (0xFFFFFFFF) 32 bite sığmalı."""
    from sim2.gozlem.kontrol import KontrolHatasi, KontrolIstegi
    from protokoller.desparete_bicim import FIELD_UPDATE
    yuk = {a: 0 for a, _ in FIELD_UPDATE.alanlar}
    yuk.update(surum=1, tip=1, baslik_uzunlugu=60, hop_siniri=1,
               potansiyel=SONSUZ, durum=1)
    istek = KontrolIstegi.kur(None, FIELD_UPDATE, yuk)
    assert istek.mesaj_bayt == 60 and istek.yayin_mi
    with pytest.raises(KontrolHatasi):
        KontrolIstegi.kur(None, FIELD_UPDATE, dict(yuk, potansiyel=1 << 32))


def test_TEL_KIMLIGI_sifir_GECERSIZ_oldugu_icin_bir_kayar():
    from protokoller.desparete_bicim import tel_kimligi
    assert [tel_kimligi(n) for n in (0, 1, 39)] == [1, 2, 40]
    with pytest.raises(ValueError):
        tel_kimligi(-1)


# ==========================================================================
# Komşu yaşamı — `22` §4 · `23` §3 · `21` §2.1 (saf tablo, zaman dışarıdan)
# ==========================================================================
def _tablo(gerekli: bool = False):
    from protokoller.desparete_komsu import KomsuTablosu
    sayac = iter(range(1, 10_000))
    return KomsuTablosu(lambda: next(sayac), lambda j: gerekli)


def test_KOMSU_zaman_iliskileri_TR01_TR02_TR12():
    """`20` §4'ün koşulları `21`'in sayılarıyla — biri bozulursa yanar."""
    from protokoller.desparete_bicim import (
        J_PROBE_S, N_PROBE, T_FRESH_S, T_IDLE_PROBE_S, T_PROBE_ARA_S,
        T_PROBE_REPLY_S, T_PROBE_SESSION_S, T_PROBE_START_S, T_RETENTION_S)
    d_probe = 0.1                                          # `21` §2.1
    assert T_RETENTION_S >= T_FRESH_S + T_PROBE_SESSION_S           # TR-01
    assert T_PROBE_SESSION_S >= N_PROBE * T_PROBE_REPLY_S           # TR-02
    assert T_IDLE_PROBE_S + T_PROBE_REPLY_S + J_PROBE_S + d_probe < T_FRESH_S
    assert T_PROBE_SESSION_S == pytest.approx(
        T_PROBE_START_S + T_PROBE_REPLY_S + T_PROBE_ARA_S + T_PROBE_REPLY_S)


def test_ADAY_niteliksiz_acar_ve_TITRESIMLI_nitelik_PROBE_ister():
    from protokoller.desparete_komsu import UNQUALIFIED, ProbeIstegi
    k = _tablo()
    assert k.aday(7, 10.0) == [ProbeIstegi(7, 1, 0.1, "nitelik")]
    assert k.durum(7) == UNQUALIFIED and k.aktifler() == ()
    assert k.aday(7, 10.2) == [], "kayıt varken ikinci oturum açılmaz"


def test_NITELIK_oturumu_IKI_denemede_1_3_s_icinde_EXPIRED():
    """0,1 + 0,5 → ikinci deneme 0,2 sonra → 0,5 → toplam 1,3 s (`21`)."""
    from protokoller.desparete_komsu import EXPIRED, UNQUALIFIED
    k = _tablo()
    k.aday(7, 0.0)
    assert k.uyandirmalar(0.0) == [(7, pytest.approx(0.6))]
    assert k.zaman(7, 0.6) == [] and k.durum(7) == UNQUALIFIED
    assert k.uyandirmalar(0.6) == [(7, pytest.approx(0.2))]
    ikinci = k.zaman(7, 0.8)
    assert [(p.sira, p.jitter_s) for p in ikinci] == [(2, 0.0)]
    assert k.uyandirmalar(0.8) == [(7, pytest.approx(0.5))]
    assert k.zaman(7, 1.3) == [] and k.durum(7) == EXPIRED
    assert k.sayac["probe_nitelik"] == 2 and len(k) == 0


def test_ADAYIN_HIZ_SINIRI_bes_saniyede_bir_nitelik_oturumu():
    """K-154: `23` §3.1'in *"rate-limited"*ı — `T_retention` ile."""
    k = _tablo()
    k.aday(7, 0.0)
    for t in (0.6, 0.8, 1.3):
        k.zaman(7, t)
    assert k.aday(7, 2.0) == [] and k.sayac["aday_hiz_siniri"] == 1
    assert len(k.aday(7, 5.0)) == 1


def test_MAC_ONAYI_ileri_yonlu_KANIT_ve_tazelik_sureleri():
    """`23` §3.1: *"confirmed local unicast/ACK to j"* ACTIVE kurar.
    Nitelik PROBE'unun onayı M0.1 örneği DEĞİLDİR — komşu o an ACTIVE
    değildi (`35` §3.1)."""
    from protokoller.desparete_komsu import ACTIVE
    k = _tablo()
    k.aday(7, 0.0)
    k.sonuc(7, 0.05, True, 0)
    kay = k.kayit(7)
    assert k.durum(7) == ACTIVE and k.aktifler() == (7,)
    assert (kay.taze_son, kay.bosta_son, kay.saklama_son) == pytest.approx(
        (3.05, 2.05, 5.05))
    assert kay.oturum is None, "kanıt oturumu kapatır"
    assert k.sayac["olcum_sonuc"] == 0 and k.sayac["olcum_disi_sonuc"] == 1


def test_YALNIZ_ESLESEN_PROBE_YANITI_kanittir():
    from protokoller.desparete_komsu import ACTIVE, UNQUALIFIED
    k = _tablo()
    k.aday(7, 0.0)                                         # sıra 1
    assert not k.probe_yaniti(7, 99, 0.2) and k.durum(7) == UNQUALIFIED
    assert k.probe_yaniti(7, 1, 0.3) and k.durum(7) == ACTIVE
    assert not k.probe_yaniti(8, 1, 0.3), "kaydı olmayan komşu"


def test_BOSTA_tek_PROBE_sonra_T_fresh_STALE_sonra_T_retention_EXPIRED():
    """Sessiz ACTIVE komşu: 2 s'de BİR boşta PROBE (N_probe tüketmez);
    yanıtsızsa 3 s'de STALE, 5 s'de EXPIRED. Alan ihtiyacı yoksa STALE'de
    hata oturumu AÇILMAZ (`23` §3.2)."""
    from protokoller.desparete_komsu import ACTIVE, EXPIRED, STALE
    k = _tablo()
    k.kanit(7, 0.0)
    bosta = k.zaman(7, 2.0)
    assert [p.tur for p in bosta] == ["bosta"] and k.durum(7) == ACTIVE
    assert k.zaman(7, 2.6) == [] and k.durum(7) == ACTIVE
    assert k.zaman(7, 3.0) == [] and k.durum(7) == STALE
    assert k.aktifler() == ()
    assert k.zaman(7, 5.0) == [] and k.durum(7) == EXPIRED
    assert k.sayac["probe_bosta"] == 1 and k.sayac["probe_hata"] == 0


def test_BOSTA_PROBE_onayi_tazeler_STALE_olmaz():
    from protokoller.desparete_komsu import ACTIVE
    k = _tablo()
    k.kanit(7, 0.0)
    k.zaman(7, 2.0)
    k.sonuc(7, 2.05, True, 0)                  # boşta PROBE'un MAC onayı
    assert k.zaman(7, 3.0) == [] and k.durum(7) == ACTIVE
    assert k.kayit(7).taze_son == pytest.approx(5.05)
    assert k.sayac["olcum_sonuc"] == 1, "ACTIVE komşuya giden → örnek"


def test_BAG_HATASI_SUSPECT_ve_alan_ihtiyaci_yoksa_PROBE_YOK():
    from protokoller.desparete_komsu import EXPIRED, SUSPECT
    k = _tablo()
    k.kanit(7, 0.0)
    assert k.bag_hatasi(7, 1.0) == [] and k.durum(7) == SUSPECT
    assert k.aktifler() == (), "SUSPECT komşu HEMEN aday dışı"
    assert k.zaman(7, 5.0) == [] and k.durum(7) == EXPIRED


def test_BAG_HATASI_alan_gerekliyse_HATA_oturumu_ve_KANITLA_geri_ACTIVE():
    from protokoller.desparete_komsu import ACTIVE, EXPIRED, SUSPECT
    k = _tablo(gerekli=True)
    k.kanit(7, 0.0)
    assert [p.tur for p in k.bag_hatasi(7, 1.0)] == ["hata"]
    k.sonuc(7, 1.05, True, 2)
    assert k.durum(7) == ACTIVE, "SUSPECT → ACTIVE: yeni ileri yönlü kanıt"
    # Kanıtsız hâli: iki deneme, sonra EXPIRED
    k2 = _tablo(gerekli=True)
    k2.kanit(7, 0.0)
    k2.bag_hatasi(7, 1.0)
    k2.zaman(7, 1.6)
    assert [p.tur for p in k2.zaman(7, 1.8)] == ["hata"]
    assert k2.durum(7) == SUSPECT
    k2.zaman(7, 2.3)
    assert k2.durum(7) == EXPIRED and k2.sayac["probe_hata"] == 2


def test_STALE_komsu_alan_gerekliyse_SUSPECT_ve_HATA_oturumu():
    """`22` §4.2: STALE + *"field için komşu gerekli"* → SUSPECT."""
    from protokoller.desparete_komsu import SUSPECT
    k = _tablo(gerekli=True)
    k.kanit(7, 0.0)
    k.zaman(7, 2.0)                                        # boşta PROBE
    k.zaman(7, 2.6)
    assert [p.tur for p in k.zaman(7, 3.0)] == ["hata"]
    assert k.durum(7) == SUSPECT


def test_M01_olcumu_ACTIVE_komsuda_ve_EXPIRED_kayitla_SILINIR():
    k = _tablo()
    k.kanit(7, 0.0)
    k.sonuc(7, 0.1, True, 1)                               # skor 127
    k.epoch(0.5)
    assert k.kayit(7).son_olcum.q == 127
    for t in (2.1, 2.7, 3.1, 5.1):             # 0,1'deki onay süreleri kaydırdı
        k.zaman(7, t)
    assert k.kayit(7) is None
    k.aday(7, 5.1)
    k.epoch(5.5)
    assert k.kayit(7).son_olcum.q is None, "eski ölçüm canlanmaz"


def test_UYANDIRMA_ayni_komsu_icin_TEKRARLANMAZ():
    """Bekleyen uyandırma sayısı sınırlı kalmalı (simülatör tavanı 256)."""
    k = _tablo()
    k.kanit(7, 0.0)
    assert k.uyandirmalar(0.0) == [(7, pytest.approx(2.0))]
    k.sonuc(7, 0.5, True, 0)                   # son tarihler İLERİ kaydı
    assert k.uyandirmalar(0.5) == [], "daha erken uyandırma zaten kurulu"
    k.zaman(7, 2.0)                            # erken uyandırma: işi yok
    assert k.uyandirmalar(2.0) == [(7, pytest.approx(0.5))]


# ==========================================================================
# Simülatörde — DESPARETE'nin İLK koşuları (K-153'ten sonra, K-154)
# ==========================================================================
def _desparete_kos(senaryo: str, bitis: float, bayraklar=None,
                   komut_alanlari: bool = False, secenekler=None):
    """Koşu + HER KANCADAN SONRA döngüsüzlük denetimi (sonuç önbellekte)."""
    anahtar = (senaryo, bitis, bayraklar, komut_alanlari, secenekler)
    if anahtar not in _SIM_ONBELLEK:
        _SIM_ONBELLEK[anahtar] = _desparete_kos_denetimli(
            senaryo, bitis, bayraklar, komut_alanlari, secenekler)
    return _SIM_ONBELLEK[anahtar]


_SIM_ONBELLEK: dict = {}
_KANCALAR = ("sonraki_atlama", "zamanlayici_doldu", "uyandi",
             "kontrol_alindi", "iletim_basarisiz", "iletim_sonucu")


def _desparete_kos_denetimli(senaryo: str, bitis: float, bayraklar=None,
                             komut_alanlari: bool = False, secenekler=None):
    """🔒 `36` §3.3'ün iddiası — veri döngüsü YOK — her olaydan sonra.

    İki şey sayılır: (1) geçide giden alanda ardıl grafiğinde döngü;
    (2) bir düğümün uygulanabilirlik mesafesinin AYNI turda artması.
    Denetim yalnız GÖZLER; protokolün davranışını değiştirmez.
    `bayraklar=None` · `secenekler=None`: DESPARETE'nin varsayılanı — v0.4
    (`PROFIL_V02` + `SECENEK_V04`, K-167) — K-172'den beri v0.4.1
    (`SECENEK_V041`). Hepsi açık = v0.1 = `PROFIL_V01`.
    """
    sys.path.insert(0, str(KOK / "tests2"))
    from test_kosum import _konfig
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_alan import FORWARDABLE
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.kurulum import kurulum_yap
    from sim2.kosum.sonuc import sonuc_satiri
    kayit: list = []
    ihlal = {"dongu": 0, "fd_artti": 0, "denetim": 0}
    son_fd: dict = {}

    def denetle():
        """BÜTÜN hedeflerin alanları — geçit ve istek üzerine doğan hedefler."""
        ihlal["denetim"] += 1
        ardil: dict = {}
        for p in kayit:
            for h, a in p.alanlar.alanlar.items():
                if a.kendi:
                    continue
                if a.durum == FORWARDABLE:
                    ardil.setdefault(h, {})[p.kimlik] = a.ardil
                if a.fd is not None:
                    once = son_fd.get((p.kimlik, h))
                    if once and once[0] == a.fd[0] and a.fd[1] > once[1]:
                        ihlal["fd_artti"] += 1
                    son_fd[(p.kimlik, h)] = a.fd
        for h, harita in ardil.items():
            ihlal["hedef"] = max(ihlal.get("hedef", 0), len(ardil))
            for bas in harita:
                gorulen, n = set(), bas
                while n in harita:
                    if n in gorulen:
                        ihlal["dongu"] += 1
                        break
                    gorulen.add(n)
                    n = harita[n]

    class Denetimli(DESPARETE):
        __slots__ = ()

        def __init__(self, i, sink):
            ek = {} if bayraklar is None else {"bayraklar": bayraklar}
            if komut_alanlari:
                ek["komut_alanlari"] = True
            if secenekler is not None:
                ek["secenekler"] = secenekler
            super().__init__(i, sink, **ek)
            kayit.append(self)

    for ad in _KANCALAR:
        def sar(asil=getattr(DESPARETE, ad)):
            def kanca(self, *a):
                sonuc = asil(self, *a)
                denetle()
                return sonuc
            return kanca
        setattr(Denetimli, ad, sar())
    kfg = _konfig(senaryo, 1000, bitis, trafik_deseni="yere_toplama")
    kur = kurulum_yap(kfg)
    kosu = Kosu(kur, lambda i: Denetimli(i, kfg.gecit))
    kosu.kostur()
    return kfg, kosu, sonuc_satiri(kur, kosu.dugumler, "desparete"), ihlal


def test_SIM_statik_KOMSULAR_NITELENIR_ve_BOSTA_PROBE_siniri():
    """3.3: geçidi duyan her düğüm en az bir kez nitelenir; karşılıklı
    ACTIVE bağ var; boşta PROBE kayıt başına `T_idle`da en çok bir.
    Komşu yaşam döngüsünün sınavıdır → seçeneksiz (v0.2) koşar: v0.3'te
    V5 gereği geçit kimseyi nitelendirmez (ayrı kapı aşağıda)."""
    from protokoller.desparete_bayrak import SECENEK_YOK
    from protokoller.desparete_bicim import T_IDLE_PROBE_S
    from protokoller.desparete_komsu import ACTIVE
    kfg, kosu, satir, _ihlal = _desparete_kos("statik-yok", 12.0,
                                              secenekler=SECENEK_YOK)
    assert satir["korunum"]["gecerli"]
    gecit = kfg.gecit
    p = [d.protokol for d in kosu.dugumler]
    geciti_duyan = [n for n in range(len(p))
                    if n != gecit and gecit in p[n].komsular._kayit]
    assert geciti_duyan, "sınav boş geçti"
    karsilikli = [n for n in p[gecit].komsular.aktifler()
                  if p[n].komsular.durum(gecit) == ACTIVE]
    assert karsilikli, "karşılıklı ACTIVE bağ yok"
    for n in range(len(p)):
        t = p[n].komsular.sayac
        ust = -(-kfg.kosu_bitis_s // T_IDLE_PROBE_S) * max(t["aday_acilan"], 1)
        assert t["probe_bosta"] <= ust, f"{n}: {t['probe_bosta']} > {ust}"
    kd = satir["teshis"]["kontrol_duzlemi"]
    assert kd["tepe_bekleyen_uyandirma"] < 32, "uyandırmalar birikiyor"


def test_SIM_statik_VERI_ALAN_uzerinden_TESLIM_ve_DONGU_YOK():
    """3.4: veri alanın ardılı üzerinden geçide ulaşıyor; her olaydan sonra
    döngü 0 ve aynı turda artan uygulanabilirlik mesafesi 0."""
    _kfg, kosu, satir, ihlal = _desparete_kos("statik-yok", 12.0)
    assert ihlal["denetim"] > 1000, "denetim boş geçti"
    assert ihlal["dongu"] == 0 and ihlal["fd_artti"] == 0, ihlal
    assert satir["metrikler"]["pdr_pencere"] > 0.0, "veri hiç teslim edilmedi"
    toplam = sum(d.protokol._sayac["veri_iletilen"] for d in kosu.dugumler)
    assert toplam > 0


def test_SIM_hareketli_karistiricili_DONGU_YOK_SUSPECT_ve_BEYANLAR():
    """Gerçek MAC vazgeçmeleri SUSPECT yapar; ardılı kopan alan KOPMA beyan
    eder; kurtarılan hiçbir zaman açılandan fazla değil; döngü yok."""
    from protokoller.desparete_komsu import SUSPECT
    _kfg, kosu, satir, ihlal = _desparete_kos("bagimsiz-surekli", 10.0)
    assert satir["korunum"]["gecerli"]
    assert ihlal["dongu"] == 0 and ihlal["fd_artti"] == 0, ihlal
    p = [d.protokol for d in kosu.dugumler]
    assert sum(q.komsular.sayac["gecis_suspect"] for q in p) > 0, (
        "sınav boş geçti: hiç sert bağ hatası görülmedi")
    for q in p:
        for j in q.komsular._kayit:
            if q.komsular.durum(j) == SUSPECT:
                assert j not in q.komsular.aktifler()
    m = satir["metrikler"]
    assert m["kopma_algilanan"] > 0, "ardılı kopan alan kopma beyan etmedi"
    assert m["rota_kurtarildi"] <= m["rota_etkilendi"]


def test_SIM_komut_hedefleri_ALANINI_ISTEKLE_acar_ve_ONARIM_calisir():
    """3.5 · K-150 §4 A (`komut_alanlari=True`; v0.1'in varsayılanı DEĞİL,
    K-160 §10): geçidin komutları bilinmeyen hedeflere edinim başlatır;
    hedefler kendi alanını açar ve alan geçide kadar yayılır. Bütün
    hedeflerin alanlarında döngü yok (denetim bütün hedefleri kapsar)."""
    from protokoller.desparete_alan import FORWARDABLE
    kfg, kosu, satir, ihlal = _desparete_kos("statik-yok", 12.0,
                                             komut_alanlari=True)
    assert ihlal["dongu"] == 0 and ihlal["fd_artti"] == 0, ihlal
    p = [d.protokol for d in kosu.dugumler]
    acilan = [q.kimlik for q in p if q._sayac["hedef_alani_acildi"]]
    assert acilan, "hiçbir komut hedefi alanını açmadı"
    gecit = p[kfg.gecit]
    assert any(gecit.alanlar.durum(h) == FORWARDABLE for h in acilan), (
        "açılan hedef alanlarının hiçbiri geçide ulaşmadı")
    assert sum(q.edinim.sayac["istek_dalgasi"] for q in p) > 0


def test_SIM_POSTUR_CAUTION_dogrular_PROTECT_YOK():
    """3.6 (K-158): gerçek koşuda alanlar CAUTION'a giriyor; her giriş en çok
    iki doğrulama PROBE'u; koruma izni olmadığından PROTECT yok."""
    _kfg, kosu, satir, ihlal = _desparete_kos("statik-yok", 12.0)
    assert ihlal["dongu"] == 0 and ihlal["fd_artti"] == 0, ihlal
    p = [d.protokol for d in kosu.dugumler]
    girdi = sum(q.politika.sayac["caution_girdi"] for q in p)
    assert girdi > 0, "sınav boş geçti: hiç CAUTION girişi yok"
    assert sum(q.politika.sayac["protect_girdi"] for q in p) == 0
    for q in p:
        assert (q.komsular.sayac["probe_dogrulama"]
                <= 2 * q.politika.sayac["caution_girdi"])


# ==========================================================================
# Alan, uygulanabilirlik ve ardıl — `23` §4 · `22` §5 (saf tablo)
# ==========================================================================
_R, _W = 0, 1                                    # REACHABLE · WITHDRAWAL


def _alan(aktif=(1, 2, 3), maliyet=None):
    from protokoller.desparete_alan import AlanTablosu
    aktifler = set(aktif)
    c = maliyet or {}
    return AlanTablosu(lambda j: j in aktifler,
                       lambda j: c.get(j, 16)), aktifler


def test_SERI_KARSILASTIRMA_RFC1982():
    from protokoller.desparete_alan import (BELIRSIZ, ESIT, ESKI, YENI,
                                            seri_karsilastir as s)
    assert (s(5, 5), s(6, 5), s(5, 6)) == (ESIT, YENI, ESKI)
    assert s(0, (1 << 32) - 1) == YENI, "sarma"
    assert s(1 << 31, 0) == BELIRSIZ


def test_ILK_ILAN_alani_kurar_ardil_FD_ve_ACIL_tetik():
    from protokoller.desparete_alan import FORWARDABLE
    t, _ = _alan()
    t.ilan_al(1, 9, 1, 1, _R, 32, 30, 0.0)
    a = t.alanlar[9]
    assert (a.durum, a.ardil, a.potansiyel, a.fd) == (FORWARDABLE, 1, 48,
                                                      (1, 48))
    assert [r.pencere_s for r in t.istekler] == [0.1], "ardıl değişimi → acil"


def test_ACTIVE_OLMAYAN_komsunun_ilani_ADAY_OLAMAZ():
    t, _ = _alan()
    t.ilan_al(7, 9, 1, 1, _R, 32, 30, 0.0)
    assert 9 not in t.alanlar and t.sayac["ilan_aktif_disi"] == 1


def test_ESIT_POTANSIYEL_uygulanabilir_DEGIL_ve_FD_ARTMAZ():
    """`36` §3.3: `P_j < M_FD` şart; eşitlik YETMEZ. Yeni ardılın potansiyeli
    FD'den büyük olsa da FD aynı turda yükselmez."""
    from protokoller.desparete_alan import FORWARDABLE, REPAIRING
    from protokoller.desparete_metrik import SONSUZ
    t, _ = _alan()
    t.ilan_al(1, 9, 1, 1, _R, 32, 30, 0.0)            # FD = 48
    t.ilan_al(2, 9, 1, 1, _R, 48, 30, 0.1)            # 48 < 48 değil
    t.ilan_al(1, 9, 1, 2, _W, SONSUZ, 0, 0.2)         # ardıl çekildi
    assert t.alanlar[9].durum == REPAIRING, "2 uygulanabilir DEĞİL"
    t.ilan_al(3, 9, 1, 1, _R, 47, 30, 0.3)
    a = t.alanlar[9]
    assert (a.durum, a.ardil, a.potansiyel) == (FORWARDABLE, 3, 63)
    assert a.fd == (1, 48), "FD aynı turda yükselmez"


def test_ARDILIN_POTANSIYELI_YUKSELINCE_ACLIK_ve_ONARIM():
    from protokoller.desparete_alan import FORWARDABLE, REPAIRING
    t, _ = _alan()
    t.ilan_al(1, 9, 1, 1, _R, 32, 30, 0.0)            # FD 48
    t.ilan_al(1, 9, 1, 2, _R, 40, 30, 0.5)            # 40 < 48: hâlâ olur
    a = t.alanlar[9]
    assert (a.durum, a.potansiyel, a.fd) == (FORWARDABLE, 56, (1, 48))
    t.ilan_al(1, 9, 1, 3, _R, 48, 30, 1.0)            # açlık
    assert a.durum == REPAIRING and a.onarim_son == pytest.approx(7.0)
    assert a.fd == (1, 48), "onarım FD'yi sıfırlamaz (`23` §4.4)"


def test_ESKI_ya_da_ESIT_ADS_REDDEDILIR_ve_OMUR_UZATAMAZ():
    t, _ = _alan()
    t.ilan_al(1, 9, 1, 5, _R, 32, 30, 0.0)
    t.ilan_al(1, 9, 1, 5, _R, 32, 30, 1.0)
    t.ilan_al(1, 9, 1, 4, _R, 32, 30, 1.0)
    assert t.sayac["ilan_eski"] == 2
    assert t.alanlar[9].ilanlar[1].bitis == pytest.approx(3.0)
    t.ilan_al(1, 9, 1, 6, _R, 32, 30, 1.0)
    assert t.alanlar[9].ilanlar[1].bitis == pytest.approx(4.0)


def test_OMUR_alicida_L_ADV_MAX_ile_SINIRLANIR():
    t, _ = _alan()
    t.ilan_al(1, 9, 1, 1, _R, 32, 65535, 0.0)
    assert t.alanlar[9].ilanlar[1].bitis == pytest.approx(3.0)


def test_YENI_DFSN_FD_SIFIRLANIR_yuksek_potansiyel_kabul():
    from protokoller.desparete_alan import FORWARDABLE
    t, _ = _alan()
    t.ilan_al(1, 9, 1, 1, _R, 32, 30, 0.0)
    t.ilan_al(2, 9, 2, 1, _R, 100, 30, 0.1)
    a = t.alanlar[9]
    assert (a.durum, a.dfsn, a.ardil, a.fd) == (FORWARDABLE, 2, 2, (2, 116))


def test_ONARIM_SURESI_UNREACHABLE_ayni_turda_UYGULANABILIR_ilan_GERI_ACAR():
    """K-152 §2(a): `23` §4.3 ve `36` §6 gibi."""
    from protokoller.desparete_alan import FORWARDABLE, REPAIRING, UNREACHABLE
    from protokoller.desparete_metrik import SONSUZ
    t, _ = _alan()
    t.ilan_al(1, 9, 1, 1, _R, 32, 30, 0.0)
    t.ilan_al(1, 9, 1, 2, _W, SONSUZ, 0, 1.0)
    assert t.durum(9) == REPAIRING and t.son_tarih(9) == pytest.approx(7.0)
    t.zaman(9, 7.0, 1e-3)
    assert t.durum(9) == UNREACHABLE
    t.ilan_al(2, 9, 1, 1, _R, 40, 30, 8.0)
    assert t.durum(9) == FORWARDABLE and t.ardil(9) == 2


def test_ARDILIN_ILANI_SURESI_DOLUNCA_ONARIMA():
    from protokoller.desparete_alan import REPAIRING
    t, _ = _alan()
    t.ilan_al(1, 9, 1, 1, _R, 32, 30, 0.0)
    assert t.son_tarih(9) == pytest.approx(1.5), "önce koruma (`20` §6.2)"
    t.zaman(9, 1.5, 1e-3)
    assert t.olaylar[-1] == ("koruma", 9) and t.son_tarih(9) == pytest.approx(3.0)
    t.zaman(9, 3.0, 1e-3)
    assert t.durum(9) == REPAIRING and ("onarim", 9) in t.olaylar


def test_ESIT_MALIYETTE_KUCUK_KIMLIK():
    t, _ = _alan()
    t.ilan_al(3, 9, 1, 1, _R, 32, 30, 0.0)
    t.ilan_al(2, 9, 1, 1, _R, 32, 30, 0.0)
    assert t.ardil(9) == 2


def test_YASAK_BIRLESIMLER_REDDEDILIR():
    from protokoller.desparete_metrik import SONSUZ
    t, _ = _alan()
    t.ilan_al(1, 9, 1, 1, _R, SONSUZ, 30, 0.0)        # sonlu değil
    t.ilan_al(1, 9, 1, 1, _R, 32, 0, 0.0)             # ömürsüz
    t.ilan_al(1, 9, 1, 1, _W, 32, 0, 0.0)             # withdrawal sonlu
    t.ilan_al(1, 9, 1, 1, _R, 0, 30, 0.0)             # P = 0 hedef değil
    assert t.sayac["ilan_gecersiz"] == 4 and 9 not in t.alanlar


def test_ILAN_ICERIGI_withdrawal_BIR_KEZ_ve_periyodik_YALNIZ_FORWARDABLE():
    from protokoller.desparete_metrik import SONSUZ
    t, _ = _alan()
    t.ilan_al(1, 9, 1, 1, _R, 32, 30, 0.0)
    assert t.ilan_icerigi(9, tetik=False) == (1, 1, _R, 48)
    assert t.ilan_icerigi(9, tetik=True) is None, "periyodik tetiği söyledi"
    t.ilan_al(1, 9, 1, 2, _W, SONSUZ, 0, 0.5)
    assert t.ilan_icerigi(9, tetik=True) == (1, 2, _W, SONSUZ)
    t.yeniden_hesapla(9, 0.6)
    assert t.ilan_icerigi(9, tetik=True) is None, "withdrawal bir kez"
    assert t.ilan_icerigi(9, tetik=False) is None, "REPAIRING tazelenmez"


def test_TETIK_BIRLESIR_ve_ALAN_BASINA_HIZ_SINIRI():
    """Bekleyen acil tetik varken olağan değişim yeni istek doğurmaz;
    gönderimden sonraki tetik en erken `T_coalesce` sonra (5/s)."""
    t, _ = _alan()
    t.ilan_al(1, 9, 1, 1, _R, 32, 30, 0.0)            # acil
    t.ilan_al(1, 9, 1, 2, _R, 30, 30, 0.05)           # azalış → birleşir
    assert len(t.istekler) == 1
    assert t.ilan_icerigi(9, tetik=True) == (1, 1, _R, 46), "SON durum"
    t.tetik_gonderildi(9, 0.08)
    t.ilan_al(1, 9, 1, 3, _R, 28, 30, 0.1)
    son = t.istekler[-1]
    assert son.en_erken_s == pytest.approx(0.28) and son.pencere_s == 0.2


def test_KOMSU_EXPIRED_ilanlari_SILINIR_ve_ONARIM():
    from protokoller.desparete_alan import REPAIRING
    t, aktif = _alan()
    t.ilan_al(1, 9, 1, 1, _R, 32, 30, 0.0)
    aktif.discard(1)
    t.komsu_degisti(1, 0.5, silindi=True)
    assert 1 not in t.alanlar[9].ilanlar and t.durum(9) == REPAIRING


def test_KENDI_ALANI_P_SIFIR_ve_komsu_ilani_YOK_SAYILIR():
    t, _ = _alan()
    t.kendi_alani(9, 1)
    t.ilan_al(1, 9, 1, 1, _R, 32, 30, 0.0)
    assert 1 not in t.alanlar[9].ilanlar
    assert t.ilan_icerigi(9, tetik=False) == (1, 1, _R, 0)


def test_BELIRSIZ_DFSN_fail_closed():
    """`23` §4.3: sıra karşılaştırması tanımsızsa alan iletime KAPANIR."""
    from protokoller.desparete_alan import REPAIRING
    t, _ = _alan()
    t.ilan_al(1, 9, 5, 1, _R, 32, 30, 0.0)
    t.ilan_al(2, 9, 5 + (1 << 31), 1, _R, 32, 30, 0.1)
    assert t.durum(9) == REPAIRING


def test_ACLIK_ayni_turda_UYGULANAMAZ_ilan_varsa():
    """`23` §5.4 FEASIBLE_STARVATION'ın yerel tanımı (K-156)."""
    t, _ = _alan()
    t.ilan_al(1, 9, 1, 1, _R, 32, 30, 0.0)            # FD 48
    t.ilan_al(1, 9, 1, 2, _R, 48, 30, 0.5)            # uygulanamaz → onarım
    assert t.aclik_mi(9, 0.6)
    bos, _ = _alan()
    assert not bos.aclik_mi(9, 0.0), "alan yok → açlık değil, edinim"


def test_HEDEF_TUR_ARTIRIR_FD_SIFIRLANIR_ve_ACIL_ilan():
    t, _ = _alan()
    t.kendi_alani(9, 1)
    t.tur_artir(9, 0.0)
    a = t.alanlar[9]
    assert (a.dfsn, a.fd) == (2, (2, 0))
    assert [r.pencere_s for r in t.istekler] == [0.1]
    assert t.ilan_icerigi(9, tetik=True)[:1] == (2,)


def test_YANIT_ICERIGI_bekleyen_TETIGI_TEMIZLEMEZ():
    """Tek alıcılı yanıtı bir komşu duyar; öbürlerine gidecek tetik durur."""
    t, _ = _alan()
    t.ilan_al(1, 9, 1, 1, _R, 32, 30, 0.0)
    assert t.yanit_icerigi(9) == (1, 1, _R, 48)
    assert t.alanlar[9].tetik_bekliyor
    assert t.ilan_icerigi(9, tetik=True) == (1, 2, _R, 48), "ADS yine artar"


# ==========================================================================
# Edinim ve onarım — `22` §6 · `23` §5.1 (saf denetçi)
# ==========================================================================
def test_EDINIM_iki_SOLICIT_sonra_iki_DALGALI_4_s_istek_oturumu():
    """0 · 0,6: solicit · 1,0: istek (sıra 1) · 2,0: istek (sıra 2) ·
    5,0: oturum biter — `21` §2.3'ün sayıları birebir."""
    from protokoller.desparete_edinim import (QUIESCENT, REQUESTING,
                                              EdinimDenetcisi)
    e = EdinimDenetcisi()
    assert [x.tur for x in e.baslat(9, 0.0)] == ["solicit"]
    assert e.baslat(9, 0.1) == [] and e.sayac["birlesen"] == 1
    assert e.zaman(9, 0.4, 1e-3, True) == []
    assert e.son_tarih(9) == pytest.approx(0.6)
    assert [x.tur for x in e.zaman(9, 0.6, 1e-3, True)] == ["solicit"]
    ilk = e.zaman(9, 1.0, 1e-3, True)
    assert [(x.tur, x.sira) for x in ilk] == [("istek", 1)]
    assert e.durum(9) == REQUESTING
    assert [(x.tur, x.sira) for x in e.zaman(9, 2.0, 1e-3, True)] == [
        ("istek", 2)], "ikinci dalga YENİ Request-ID"
    assert e.zaman(9, 3.0, 1e-3, True) == [], "N_req = 2"
    assert [x.tur for x in e.zaman(9, 5.0, 1e-3, True)] == ["bitti"]
    assert e.durum(9) == QUIESCENT and e.sayac["istek_dalgasi"] == 2


def test_EDINIM_alan_hala_iletilebilirse_ISTEK_ACILMAZ():
    """Koruma solicit'i: ardılın ilanı tazelendiyse DFSN_REQUEST gereksiz."""
    from protokoller.desparete_edinim import QUIESCENT, EdinimDenetcisi
    e = EdinimDenetcisi()
    e.baslat(9, 0.0)
    e.zaman(9, 0.4, 1e-3, False)
    e.zaman(9, 0.6, 1e-3, False)
    assert e.zaman(9, 1.0, 1e-3, False) == [] and e.durum(9) == QUIESCENT
    assert e.sayac["gereksiz_kapandi"] == 1 and e.sayac["istek_dalgasi"] == 0


def test_EDINIM_basari_IPTAL_ve_YENIDEN_EDINIM_6_s_kurali():
    """K-152 §2: son bölümün bitişinden en az `T_repair_max` sonra."""
    from protokoller.desparete_edinim import QUIESCENT, EdinimDenetcisi
    e = EdinimDenetcisi()
    e.baslat(9, 0.0)
    e.basarili(9, 0.5)
    assert e.durum(9) == QUIESCENT
    assert e.yeniden_edinim(9, 3.0) == []
    assert e.sayac["yeniden_edinim_bekledi"] == 1
    assert [x.tur for x in e.yeniden_edinim(9, 6.5)] == ["solicit"]
    e.zaman_asimi_bitir(9, 7.0)
    assert e.durum(9) == QUIESCENT, "T_repair_max oturumu da bitirir"


# ==========================================================================
# Protokol — istek, solicit ve hedef (`23` §5.2–§5.4)
# ==========================================================================
def _kontrol(p, t, gonderen, istek):
    """`istek` bir `KontrolIstegi` — başka bir düğümün ürettiği çerçeve."""
    from test_aodv import _gozlem
    return p.kontrol_alindi(_gozlem(p.kimlik, t), gonderen, istek.bicim.ad,
                            istek.yuk, istek.hedef is None)


def _istekler_of(niyet, ad):
    from sim2.gozlem.kontrol import KontrolIstegi
    return [n for n in niyet if isinstance(n, KontrolIstegi)
            and n.bicim.ad == ad]


def _duzenle(istek, **alanlar):
    from sim2.gozlem.kontrol import KontrolIstegi
    y = dict(istek.yuk)
    y.update(alanlar)
    return KontrolIstegi.kur(istek.hedef, istek.bicim, y)


def test_ISTEK_ACTIVE_komsudan_BIR_KEZ_iletilir_Hop_Limit_azalir():
    sys.path.insert(0, str(KOK / "tests2"))
    from protokoller.desparete import DESPARETE
    q, r = DESPARETE(2, sink=0), DESPARETE(4, sink=0)
    istek = q._istek(9, 1, 0.0)
    assert _istekler_of(_kontrol(r, 0.1, 2, istek), "DFSN_REQUEST") == []
    assert r._sayac["istek_aktif_disi"] == 1, "ACTIVE olmayandan kabul yok"
    r.komsular.kanit(2, 0.2)
    ilet = _istekler_of(_kontrol(r, 0.3, 2, istek), "DFSN_REQUEST")
    assert len(ilet) == 1 and ilet[0].hedef is None, "tek yayın (K-150)"
    y = dict(ilet[0].yuk)
    assert (y["hop_siniri"], y["istek_sira"]) == (15, 1)
    assert y["gonderen"] == 5, "gönderen bloğu iletende değişir"
    tekrar = _istekler_of(_kontrol(r, 0.4, 2, istek), "DFSN_REQUEST")
    assert tekrar == [] and r._sayac["istek_tekrar"] == 1, "Request-ID bir kez"


def test_HEDEF_baglamsiz_istekte_KENDI_ALANINI_ACAR():
    """K-150 §4 A (`komut_alanlari=True`) — komut alacak düğüm alanını ilk
    istekte üretir. v0.1'in varsayılanı (C) bunu YAPMAZ — ayrı test."""
    sys.path.insert(0, str(KOK / "tests2"))
    from protokoller.desparete import DESPARETE
    from sim2.gozlem.kontrol import Uyandirma
    q, h = DESPARETE(2, sink=0), DESPARETE(9, sink=0, komut_alanlari=True)
    h.komsular.kanit(2, 0.0)
    niyet = _kontrol(h, 0.1, 2, q._istek(9, 1, 0.0))
    assert h.alanlar.alanlar[9].kendi and h._sayac["hedef_alani_acildi"] == 1
    assert any(isinstance(n, Uyandirma) and n.etiket == "ilan:9"
               for n in niyet), "başlangıç ilanı tetiklenmeli"


def test_HEDEF_yalniz_ACLIK_isteginde_ve_BIR_KEZ_tur_artirir():
    """`23` §5.4'ün dar yetkisi: bağlam tam eşleşmeli, neden açlık, istenen
    = güncel + 1. İkinci istek aynı eski tura dayanıyorsa artış olmaz."""
    sys.path.insert(0, str(KOK / "tests2"))
    from protokoller.desparete import DESPARETE
    q, h = DESPARETE(2, sink=0), DESPARETE(9, sink=0)
    h.alanlar.kendi_alani(9, 1)
    h.komsular.kanit(2, 0.0)
    temel = q._istek(9, 1, 0.0)
    aclik = dict(rbayraklar=1, bilinen_oiid=1, istenen_en_az_dfsn=2, sebep=1)
    _kontrol(h, 0.1, 2, _duzenle(temel, **aclik))
    assert h.alanlar.alanlar[9].dfsn == 2
    _kontrol(h, 0.2, 2, _duzenle(temel, istek_sira=2, **aclik))
    assert h.alanlar.alanlar[9].dfsn == 2, "eşdeğer istek tek artışta birleşir"
    _kontrol(h, 0.3, 2, _duzenle(temel, istek_sira=3, rbayraklar=1,
                                 bilinen_oiid=1, istenen_en_az_dfsn=3,
                                 sebep=0))
    assert h.alanlar.alanlar[9].dfsn == 2, "edinim nedeni tur üretmez"
    assert h.alanlar.sayac["tur_artirildi"] == 1


def test_SOLICIT_ACTIVE_komsuya_TEK_ALICILI_guncel_ilanla_yanitlanir():
    sys.path.insert(0, str(KOK / "tests2"))
    from protokoller.desparete import DESPARETE
    q, r = DESPARETE(2, sink=0), DESPARETE(4, sink=0)
    r.komsular.kanit(5, 0.0)
    r.komsular.sonuc(5, 0.1, True, 0)
    r.komsular.epoch(0.5)
    r.alanlar.ilan_al(5, 0, 1, 1, _R, 0, 30, 0.6)      # 5 geçit değil ama
    solicit = q._solicit(0)                             # P = 0 yalnız hedefte
    assert r.alanlar.durum(0) is None, "P = 0 hedef olmayandan reddedildi"
    r.alanlar.ilan_al(5, 0, 1, 1, _R, 16, 30, 0.6)
    assert _istekler_of(_kontrol(r, 0.7, 2, solicit), "FIELD_UPDATE") == []
    r.komsular.kanit(2, 0.8)
    yanit = _istekler_of(_kontrol(r, 0.9, 2, solicit), "FIELD_UPDATE")
    assert len(yanit) == 1 and yanit[0].hedef == 2
    assert dict(yanit[0].yuk)["potansiyel"] == r.alanlar.alanlar[0].potansiyel


# ==========================================================================
# K-157 · ALAN BAŞINA TAMPON KOTASI — `21` §2.4
# ==========================================================================
def test_KOTA_yuzde_on_ve_32nin_KUCUGU_yerel_tampon_SIMULATORLE_ayni():
    from protokoller.desparete_bicim import (TAMPON_KOTASI, YEREL_TAMPON,
                                             tampon_kotasi)
    from sim2.yapilandirma.konfig import Konfig
    assert YEREL_TAMPON == Konfig(kol="test").rota_tamponu_kapasitesi
    assert TAMPON_KOTASI == tampon_kotasi(64) == 6
    assert (tampon_kotasi(319), tampon_kotasi(320), tampon_kotasi(1000)) == (
        31, 32, 32)


def _onarimda(kota=None, bayraklar=None):
    """Düğüm 4, hedef 0 ve 9'un alanlarını tek komşusu 5'ten öğrenir; 5 ikisini
    de çekince iki alan REPAIRING olur (onarım bölümü 0,7 s'de başlar).
    İki alan yalnız K-150 §4 A'da (`komut_alanlari=True`) anlamlıdır; alan
    başına kota ve ayrılık onunla sınanır. v0.1'in C'si tek alanlıdır."""
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_alan import FORWARDABLE, REPAIRING
    from protokoller.desparete_metrik import SONSUZ
    ek = {"komut_alanlari": True}
    if kota is not None:
        ek["tampon_kotasi"] = kota
    if bayraklar is not None:
        ek["bayraklar"] = bayraklar
    r = DESPARETE(4, sink=0, **ek)
    r.komsular.kanit(5, 0.0)
    r.komsular.sonuc(5, 0.1, True, 0)
    r.komsular.epoch(0.5)
    for h in (0, 9):
        r.alanlar.ilan_al(5, h, 1, 1, _R, 16, 30, 0.6)
        assert r.alanlar.durum(h) == FORWARDABLE
        r.alanlar.ilan_al(5, h, 1, 2, _W, SONSUZ, 0, 0.7)
        assert r.alanlar.durum(h) == REPAIRING
    return r


def _veri(p, t, kaynak, sira, hedef=0):
    """Röledeki bir veri paketi: kimliği `(kaynak, sira)`."""
    sys.path.insert(0, str(KOK / "tests2"))
    from test_aodv import _gozlem
    return p.sonraki_atlama(_gozlem(p.kimlik, t, paket_hedefi=hedef,
                                    paket_kaynagi=kaynak, paket_sira=sira))


def test_KOTA_alti_AYRI_paket_YEDINCISI_duser_YENIDEN_SORULAN_sayilmaz():
    """Simülatör her uyandırmada bütün tamponu yeniden sorar; kimlik
    olmasaydı aynı altı paket kotayı ikinci soruşta kendisi doldururdu."""
    r = _onarimda()
    assert all(_veri(r, 1.0, 7, k).beklet for k in range(6))
    fazla = _veri(r, 1.1, 7, 6)
    assert not fazla.beklet and fazla.sonraki is None
    assert fazla.beyanlar("rota_gecersiz"), "alan bilinir → rota_gecersiz"
    assert all(_veri(r, 1.2, 7, k).beklet for k in range(6)), "yeniden soruş"
    s = r._sayac
    assert (s["tampon_alinan"], s["tampon_kota_disi"], s["tampon_tepe"],
            s["veri_bekletilen"]) == (6, 1, 6, 12)


def test_KOTA_kimlik_KAYNAKLA_birlikte_ve_ALAN_BASINA_ayri():
    r = _onarimda(kota=2)
    assert _veri(r, 1.0, 7, 0).beklet and _veri(r, 1.0, 8, 0).beklet, (
        "aynı sıra, başka kaynak: başka paket")
    assert not _veri(r, 1.0, 7, 1).beklet
    assert _veri(r, 1.0, 7, 1, hedef=9).beklet, "hedef 9'un kendi kotası"
    assert r._tutulan == {0: {(7, 0), (8, 0)}, 9: {(7, 1)}}


def test_KOTA_bolum_BITINCE_bosalir_iletilebilir_ve_ulasilamaz():
    """Tek kural: küme bölüm sonunda boşalır. Kalan paket yeniden sorulunca
    ya iletilir ya düşer; yeni bölüm kotaya BOŞ başlar."""
    sys.path.insert(0, str(KOK / "tests2"))
    from test_aodv import _gozlem
    from protokoller.desparete_alan import UNREACHABLE
    from protokoller.desparete_metrik import SONSUZ
    r = _onarimda(kota=2)
    assert _veri(r, 1.0, 7, 0).beklet and _veri(r, 1.0, 7, 1).beklet
    assert _veri(r, 1.0, 7, 0, hedef=9).beklet
    r.alanlar.ilan_al(5, 0, 1, 3, _R, 16, 30, 1.5)       # 0 onarıldı
    assert _veri(r, 1.6, 7, 0).sonraki == 5
    assert 0 not in r._tutulan and 9 in r._tutulan
    r.alanlar.ilan_al(5, 0, 1, 4, _W, SONSUZ, 0, 1.7)    # yeni bölüm
    assert _veri(r, 1.8, 7, 1).beklet and _veri(r, 1.8, 7, 2).beklet
    assert not _veri(r, 1.8, 7, 3).beklet
    r.uyandi(_gozlem(4, 6.8), "alan:9")                  # 0,7 + 6 s doldu
    assert r.alanlar.durum(9) == UNREACHABLE and 9 not in r._tutulan
    dus = _veri(r, 6.9, 7, 0, hedef=9)
    assert not dus.beklet and dus.beyanlar("rota_gecersiz")


# ==========================================================================
# 3.6 · POSTÜR — `22` §7 · `35` §5 · `21` §2.5 (K-158)
# ==========================================================================
def test_POLITIKA_sureleri_ve_TR09():
    from protokoller.desparete_bicim import (
        T_CAUTION_EVIDENCE_S, T_PROTECT_EVIDENCE_S, T_PROTECT_MIN_S,
        T_RECOVERY_EVIDENCE_S)
    assert (T_CAUTION_EVIDENCE_S, T_PROTECT_EVIDENCE_S, T_RECOVERY_EVIDENCE_S,
            T_PROTECT_MIN_S) == (1.5, 2.5, 4.0, 2.0)
    assert T_RECOVERY_EVIDENCE_S >= max(T_CAUTION_EVIDENCE_S,     # TR-09
                                        T_PROTECT_EVIDENCE_S)


def _o(h=0, u=0):
    from protokoller.desparete_metrik import Olcum
    return Olcum(q=255, h=h, u=u, r=max(h, u), c=16, n_q=12)


def test_M01_POLITIKA_YUKLEMLERI_esikleri():
    from protokoller.desparete_metrik import (koruma_kaniti,
                                              toparlanma_kaniti, uyari_kaniti)
    assert not uyari_kaniti(_o(63, 127)) and toparlanma_kaniti(_o(63, 127))
    assert uyari_kaniti(_o(64, 0)) and not toparlanma_kaniti(_o(64, 0))
    assert uyari_kaniti(_o(0, 128)) and not koruma_kaniti(_o(0, 255)), (
        "yüksek U tek başına PROTECT kanıtı değil")
    assert koruma_kaniti(_o(128, 0)) and not koruma_kaniti(_o(127, 0))


def _politika_kos(p, adimlar, h=0, ardil=5, ek=False):
    """`adimlar`: (t, Olcum) — her biri bir epoch değerlendirmesi. Doğrulama
    istenen anları döndürür."""
    return [t for t, o in adimlar if p.degerlendir(h, t, ardil, o, ek)]


def test_POSTUR_CAUTION_1_5_s_KESINTISIZ_kanitla_ve_kesinti_SIFIRLAR():
    from protokoller.desparete_politika import (CAUTION, STEADY,
                                                PolitikaTablosu)
    p = PolitikaTablosu()
    kotu, iyi = _o(0, 128), _o(0, 0)
    adim = [(0.0, kotu), (0.5, kotu), (1.0, iyi), (1.5, kotu), (2.0, kotu),
            (2.5, kotu)]
    assert _politika_kos(p, adim) == [] and p.durum(0) == STEADY
    assert _politika_kos(p, [(3.0, kotu)]) == [3.0], "1,5 → 3,0: 1,5 s"
    assert p.durum(0) == CAUTION and p.sayac["caution_girdi"] == 1
    assert (p.sayac["caution_belirsizlik"], p.sayac["caution_hazard"]) == (
        1, 0), "H = 0, U = 128: yalnız belirsizlik"


def test_POSTUR_STEADYe_donus_4_s_toparlanma_POSTUR_ICINDE_olculur():
    from protokoller.desparete_politika import (CAUTION, STEADY,
                                                PolitikaTablosu)
    p = PolitikaTablosu()
    _politika_kos(p, [(t / 2, _o(64, 0)) for t in range(4)])   # CAUTION 1,5
    assert p.durum(0) == CAUTION and p.sayac["caution_hazard"] == 1
    _politika_kos(p, [(2.0 + t / 2, _o(0, 0)) for t in range(8)])  # 2,0…5,5
    assert p.durum(0) == CAUTION, "2,0 → 5,5 yalnız 3,5 s"
    _politika_kos(p, [(6.0, _o(0, 0))])
    assert p.durum(0) == STEADY and p.sayac["steady_dondu"] == 1


def test_POSTUR_PROTECT_IZINLE_ve_izinsiz_BIR_KEZ_sayilir():
    from protokoller.desparete_politika import (CAUTION, PROTECT,
                                                PolitikaTablosu)
    adim = [(t / 2, _o(128, 0)) for t in range(10)]              # 0,0 … 4,5
    izinli = PolitikaTablosu(koruma_izni=True)
    _politika_kos(izinli, adim[:8], ek=True)                     # … 3,5
    assert izinli.durum(0) == CAUTION, "CAUTION 1,5'te; +2,5 = 4,0"
    _politika_kos(izinli, adim[8:9], ek=True)
    assert izinli.durum(0) == PROTECT
    izinsiz = PolitikaTablosu()
    _politika_kos(izinsiz, adim, ek=True)
    assert izinsiz.durum(0) == CAUTION
    assert izinsiz.sayac["protect_izinsiz"] == 1, "bölüm başına bir kez"
    tek = PolitikaTablosu(koruma_izni=True)
    _politika_kos(tek, adim, ek=False)
    assert tek.durum(0) == CAUTION, "ek güvenli ardıl yoksa PROTECT yok"


def test_POSTUR_PROTECT_ek_ardil_kaybinda_HEMEN_iner_STEADYe_DOGRUDAN_donmez():
    from protokoller.desparete_politika import (CAUTION, PROTECT, STEADY,
                                                PolitikaTablosu)
    p = PolitikaTablosu(koruma_izni=True)
    _politika_kos(p, [(t / 2, _o(128, 0)) for t in range(9)], ek=True)
    assert p.durum(0) == PROTECT                                  # 4,0
    _politika_kos(p, [(4.5, _o(128, 0))], ek=False)
    assert p.durum(0) == CAUTION and p.sayac["protect_zorunlu_cikis"] == 1
    q = PolitikaTablosu(koruma_izni=True)
    _politika_kos(q, [(t / 2, _o(128, 0)) for t in range(9)], ek=True)
    _politika_kos(q, [(4.5 + t / 2, _o(0, 0)) for t in range(8)], ek=True)
    assert q.durum(0) == PROTECT, "4,5 → 8,0: 3,5 s"
    _politika_kos(q, [(8.5, _o(0, 0))], ek=True)
    assert q.durum(0) == CAUTION and q.sayac["protect_cikti"] == 1
    _politika_kos(q, [(9.0, _o(0, 0))], ek=True)
    assert q.durum(0) == CAUTION, "toparlanma CAUTION'da YENİDEN başlar"
    _politika_kos(q, [(9.0 + t / 2, _o(0, 0)) for t in range(1, 8)], ek=True)
    assert q.durum(0) == STEADY                                   # 12,5


def test_POSTUR_ARDIL_degisince_KANIT_sifirlanir_ONARIMDA_etkisiz_sonra_STEADY():
    from protokoller.desparete_politika import (CAUTION, STEADY,
                                                PolitikaTablosu)
    p = PolitikaTablosu()
    kotu = _o(0, 128)
    _politika_kos(p, [(0.0, kotu), (0.5, kotu), (1.0, kotu)], ardil=5)
    _politika_kos(p, [(1.5, kotu)], ardil=6)
    assert p.durum(0) == STEADY and p.sayac["ardil_degisti_kanit"] == 1
    _politika_kos(p, [(2.0, kotu), (2.5, kotu), (3.0, kotu)], ardil=6)
    assert p.durum(0) == CAUTION, "6'nın kanıtı 1,5'ten"
    p.etkisiz(0)
    p.yeniden(0)
    assert p.durum(0) == STEADY and p.sayac["etkisiz_kaldi"] == 1


def test_DOGRULAMA_oturumu_ACTIVE_komsuya_iki_PROBE_yanitsizsa_DUSURMEZ():
    from protokoller.desparete_komsu import ACTIVE, ProbeIstegi
    k = _tablo()
    k.kanit(7, 0.0)
    assert k.dogrula(7, 0.5) == [ProbeIstegi(7, 1, 0.1, "dogrulama")]
    assert k.dogrula(7, 0.6) == [] and k.sayac["dogrulama_acik_oturum"] == 1
    assert k.zaman(7, 1.1) == []                        # 0,5 + 0,1 + 0,5
    assert [p.tur for p in k.zaman(7, 1.3)] == ["dogrulama"]
    assert k.zaman(7, 1.8) == [] and k.durum(7) == ACTIVE, (
        "yanıtsız doğrulama ACTIVE'i düşürmez; T_fresh karar verir")
    assert k.kayit(7).oturum is None and k.sayac["probe_dogrulama"] == 2
    assert k.dogrula(8, 2.0) == [], "kayıtsız komşu"


def test_EK_ARDIL_yalniz_BASKA_guvenli_aday_varsa():
    t, _ = _alan()
    t.ilan_al(1, 9, 1, 1, _R, 32, 30, 0.0)            # FD 48
    assert not t.ek_ardil_var(9, 0.1)
    t.ilan_al(2, 9, 1, 1, _R, 48, 30, 0.1)            # 48 < 48 değil
    assert not t.ek_ardil_var(9, 0.2), "uygulanabilir olmayan sayılmaz"
    t.ilan_al(3, 9, 1, 1, _R, 40, 30, 0.2)
    assert t.ek_ardil_var(9, 0.3) and t.ardil(9) == 1


def test_DESPARETE_bosta_ardil_CAUTIONa_girer_ve_DOGRULAR():
    """Tek başarı → pencerede 1 örnek → U = 128 (K-150 §3'ün yapısal
    belirsizliği): 1,0'dan kesintisiz → 2,5'te CAUTION ve ardıla PROBE."""
    sys.path.insert(0, str(KOK / "tests2"))
    from test_aodv import _gozlem
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_politika import CAUTION, STEADY
    r = DESPARETE(4, sink=0)
    r.komsular.kanit(5, 0.0)
    r.komsular.sonuc(5, 0.1, True, 0)
    r.komsular.epoch(0.5)
    r.alanlar.ilan_al(5, 0, 1, 1, _R, 16, 30, 0.6)
    probelar = {}
    for t in (1.0, 1.5, 2.0, 2.5):
        niyet = r.zamanlayici_doldu(_gozlem(4, t), "metrik")
        probelar[t] = _istekler_of(niyet, "PROBE")
        if t < 2.5:
            assert r.politika.durum(0) == STEADY
    assert r.politika.durum(0) == CAUTION
    assert [p.hedef for p in probelar[2.5]] == [5]
    assert r.komsular.sayac["probe_dogrulama"] == 1
    assert r.teshis(4)["politika_sayac"][0] == 1              # caution_girdi


# ==========================================================================
# 3.7 · ABLASYON BAYRAKLARI (K-159) — her biri: kapalıyken mekanizma İŞLEMEZ,
# açıkken işler. Varsayılan hepsi açık = v0.1.
# ==========================================================================
def test_BAYRAKLAR_sekiz_mekanizma_VARSAYILAN_acik():
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_bayrak import TUMU_ACIK, TUMU_KAPALI, Bayraklar
    assert Bayraklar.adlar() == (
        "risk_maliyeti", "kalite_maliyeti", "postur", "bosta_sondalama",
        "onarim_tamponu", "onarim_edinimi", "ilan_korumasi", "yeniden_edinim")
    from protokoller.desparete_bayrak import PROFIL_V01, PROFIL_V02
    assert Bayraklar() == TUMU_ACIK and TUMU_ACIK.kapali() == ()
    assert TUMU_KAPALI.kapali() == Bayraklar.adlar()
    assert Bayraklar(postur=False).kapali() == ("postur",)
    # K-161: v0.1 = hepsi açık; DESPARETE'nin varsayılanı v0.2 yalın profil.
    assert PROFIL_V01 == TUMU_ACIK
    assert PROFIL_V02.kapali() == ("bosta_sondalama", "onarim_edinimi",
                                   "ilan_korumasi")
    assert DESPARETE(1, sink=0).bayraklar == PROFIL_V02


def test_BAYRAKLAR_TESHISTE_duz_ve_sozlesmeye_uygun():
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_bayrak import Bayraklar
    from sim2.gozlem.teshis import teshis_dogrula
    te = teshis_dogrula(4, DESPARETE(4, sink=0, bayraklar=Bayraklar(
        postur=False)).teshis(4))
    b = dict(zip(te["bayraklar_adlari"], te["bayraklar"]))
    assert b["postur"] is False and sum(b.values()) == 7


def test_MALIYET_TERIM_bayraklari():
    from protokoller.desparete_metrik import maliyet
    assert maliyet(100, 150) == 48                      # 16 + 16 + 16
    assert maliyet(100, 150, risk=False) == 32
    assert maliyet(100, 150, kalite=False) == 32
    assert maliyet(100, 150, False, False) == 16, "atlama sayısı"


def test_RISK_ve_KALITE_bayragi_MALIYETE_ve_SAYACA():
    """Tek başarı, bir tekrarla: Q = 127 (kalite +16) · U = 128 (risk +16)."""
    sys.path.insert(0, str(KOK / "tests2"))
    from test_aodv import _gozlem
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_bayrak import Bayraklar
    for b, c, sayac in ((None, 48, (1, 1)),
                        (Bayraklar(risk_maliyeti=False), 32, (0, 1)),
                        (Bayraklar(kalite_maliyeti=False), 32, (1, 0)),
                        (Bayraklar(risk_maliyeti=False,
                                   kalite_maliyeti=False), 16, (0, 0))):
        r = (DESPARETE(4, sink=0) if b is None
             else DESPARETE(4, sink=0, bayraklar=b))
        r.komsular.kanit(5, 0.0)
        r.komsular.sonuc(5, 0.1, True, 1)
        r.zamanlayici_doldu(_gozlem(4, 1.0), "metrik")
        assert r._maliyet(5) == c, b
        assert (r._sayac["epoch_risk_cezali"],
                r._sayac["epoch_kalite_cezali"]) == sayac, b


def test_BOSTA_SONDALAMA_kapali_PROBE_yok_T_fresh_karar_verir():
    from protokoller.desparete_komsu import STALE, KomsuTablosu
    sayac = iter(range(1, 100))
    k = KomsuTablosu(lambda: next(sayac), lambda j: False,
                     bosta_sondalama=False)
    k.kanit(7, 0.0)
    assert k.kayit(7).bosta_son is None
    assert k.zaman(7, 2.0) == [] and k.sayac["probe_bosta"] == 0
    k.zaman(7, 3.0)
    assert k.durum(7) == STALE
    acik = _tablo()
    acik.kanit(7, 0.0)
    assert [p.tur for p in acik.zaman(7, 2.0)] == ["bosta"]


def test_POSTUR_kapali_CAUTION_ve_DOGRULAMA_yok():
    sys.path.insert(0, str(KOK / "tests2"))
    from test_aodv import _gozlem
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_bayrak import Bayraklar
    from protokoller.desparete_politika import STEADY
    r = DESPARETE(4, sink=0, bayraklar=Bayraklar(postur=False))
    r.komsular.kanit(5, 0.0)
    r.komsular.sonuc(5, 0.1, True, 0)
    r.komsular.epoch(0.5)
    r.alanlar.ilan_al(5, 0, 1, 1, _R, 16, 30, 0.6)
    for t in (1.0, 1.5, 2.0, 2.5, 3.0):
        assert _istekler_of(r.zamanlayici_doldu(_gozlem(4, t), "metrik"),
                            "PROBE") == []
    assert r.politika.durum(0) == STEADY
    assert r.politika.sayac["caution_girdi"] == 0
    assert r.komsular.sayac["probe_dogrulama"] == 0


def test_ONARIM_TAMPONU_kapali_REPAIRINGde_DUSURUR():
    from protokoller.desparete_bayrak import Bayraklar
    r = _onarimda(bayraklar=Bayraklar(onarim_tamponu=False))
    k = _veri(r, 1.0, 7, 0)
    assert not k.beklet and k.beyanlar("rota_gecersiz")
    assert r._sayac["tampon_alinan"] == 0 and r._sayac["veri_ardilsiz"] == 1


def test_ONARIM_EDINIMI_kapali_SOLICIT_yok():
    from protokoller.desparete_bayrak import PROFIL_V01, Bayraklar
    acik = _onarimda(bayraklar=PROFIL_V01)
    assert _istekler_of(_veri(acik, 1.0, 7, 0).niyetler, "FIELD_SOLICIT")
    assert acik._sayac["edinim_onarim"] == 2, "iki alan onarımda"
    kapali = _onarimda(bayraklar=Bayraklar(onarim_edinimi=False))
    assert _istekler_of(_veri(kapali, 1.0, 7, 0).niyetler,
                        "FIELD_SOLICIT") == []
    assert kapali._sayac["edinim_onarim"] == 0
    assert kapali.edinim.sayac["baslatilan"] == 0


def test_ILAN_KORUMASI_kapali_bitmeden_SOLICIT_yok():
    """İlan 0,6'da 3 s ömürle → bitiş 3,6 → koruma 3,6 − 1,5 = 2,1."""
    sys.path.insert(0, str(KOK / "tests2"))
    from test_aodv import _gozlem
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_bayrak import PROFIL_V01, Bayraklar
    for b, beklenen in ((PROFIL_V01, 1), (Bayraklar(ilan_korumasi=False), 0)):
        r = DESPARETE(4, sink=0, bayraklar=b)
        r.komsular.kanit(5, 0.0)
        r.komsular.sonuc(5, 0.1, True, 0)
        r.komsular.epoch(0.5)
        r.alanlar.ilan_al(5, 0, 1, 1, _R, 16, 30, 0.6)
        niyet = r.uyandi(_gozlem(4, 2.1), "alan:0")
        assert r.alanlar.sayac["koruma"] == 1, "koruma olayı her iki kolda"
        assert len(_istekler_of(niyet, "FIELD_SOLICIT")) == beklenen, b
        assert r._sayac["edinim_koruma"] == beklenen, b


def test_YENIDEN_EDINIM_kapali_ULASILAMAZa_yok_ILK_edinim_SURER():
    """0 ve 9 onarımda 0,7'den → 6,8'de 0 ULAŞILAMAZ, bölüm biter →
    kendi paketim 12,9'da (≥ 6 s sonra). Geçit alanı hiç olmayan bir düğüm
    için ilk edinim bayraktan bağımsız sürer."""
    sys.path.insert(0, str(KOK / "tests2"))
    from test_aodv import _gozlem
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_alan import UNREACHABLE
    from protokoller.desparete_bayrak import Bayraklar
    for b, beklenen in ((None, 1), (Bayraklar(yeniden_edinim=False), 0)):
        r = _onarimda(bayraklar=b)
        _veri(r, 1.0, 7, 0)                              # onarım edinimi
        r.uyandi(_gozlem(4, 6.8), "alan:0")
        assert r.alanlar.durum(0) == UNREACHABLE
        dus = _veri(r, 12.9, 4, 0)
        assert not dus.beklet and dus.beyanlar("rota_gecersiz")
        assert r._sayac["edinim_yeniden"] == beklenen, b
        yeni = (DESPARETE(7, sink=0) if b is None
                else DESPARETE(7, sink=0, bayraklar=b))
        _veri(yeni, 0.5, 7, 0)
        assert yeni._sayac["edinim_ilk"] == 1, "ilk edinim bayrakla kapanmaz"


def test_SIM_BUTUN_BAYRAKLAR_KAPALI_dongu_YOK_ve_SATIRDA():
    """Güvenlik değişmezleri bayraklardan bağımsız: hepsi kapalıyken de döngü
    0 ve FD artışı 0; satırdaki her düğüm kapalı bayraklarını taşıyor."""
    from protokoller.desparete_bayrak import TUMU_KAPALI
    _kfg, kosu, satir, ihlal = _desparete_kos("statik-yok", 12.0, TUMU_KAPALI)
    assert satir["korunum"]["gecerli"]
    assert ihlal["denetim"] > 1000, "denetim boş geçti"
    assert ihlal["dongu"] == 0 and ihlal["fd_artti"] == 0, ihlal
    for te in satir["teshis"]["dugum"]:
        assert tuple(te["bayraklar"]) == TUMU_KAPALI.degerler()
    p = [d.protokol for d in kosu.dugumler]
    assert sum(q._sayac["veri_iletilen"] for q in p) > 0, (
        "sınav boş geçti: hiç veri iletilmedi")
    for q in p:
        assert q.komsular.sayac["probe_bosta"] == 0
        assert q.politika.sayac["caution_girdi"] == 0
        assert (q._sayac["edinim_onarim"], q._sayac["edinim_koruma"],
                q._sayac["edinim_yeniden"], q._sayac["tampon_alinan"],
                q._sayac["epoch_risk_cezali"],
                q._sayac["epoch_kalite_cezali"]) == (0, 0, 0, 0, 0, 0)


# ==========================================================================
# 3.8 · KABUL KAPISI (K-160) — U1'in YAPI yarısı · U2 · U4'ün eksik satırları.
# U1'in sayısal yarısı `kalibrasyon/aodv_uygunluk.py --protokol desparete`.
# ==========================================================================
def test_U1_YAPI_teslim_COK_ATLAMALI_defter_kapali_KAHINI_GECMEZ():
    """`06` §4.4 U1-U, DESPARETE'nin işletme profilinde (yere toplama).
    Eşiksiz: kâhini GEÇMEK bir kaçaktır — AYNI dünyada koşan kâhinle."""
    sys.path.insert(0, str(KOK / "tests2"))
    from test_kosum import _konfig
    from kalibrasyon.kahin import EnGuvenilirKahin, KanalGrafigi
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.kurulum import kurulum_yap
    from sim2.kosum.sonuc import sonuc_satiri
    _kfg, _kosu, satir, _ihlal = _desparete_kos("statik-yok", 12.0)
    m, kor = satir["metrikler"], satir["korunum"]
    assert kor["gecerli"] and kor["uretilen"] > 0
    assert m["pdr"] is not None and m["pdr"] > 0.0, "hiç teslim yok"
    assert m["aktarilan_paket"] > 0, "teslimlerin hepsi tek atlamalı"
    kfg = _konfig("statik-yok", 1000, 12.0, trafik_deseni="yere_toplama")
    kur = kurulum_yap(kfg)
    grafik = KanalGrafigi(kur)
    kosu = Kosu(kur, lambda i: EnGuvenilirKahin(i, grafik))
    kosu.kostur()
    kahin = sonuc_satiri(kur, kosu.dugumler, "u1")["metrikler"]["pdr"]
    assert kahin is not None and kahin > 0.0, "kâhin BOŞ koştu"
    assert m["pdr"] <= kahin, (
        f"DESPARETE kâhini GEÇTİ: {m['pdr']:.4f} > {kahin:.4f}")


def _iki_komsulu(komsular=(5, 6), potansiyel=(16, 20), bayraklar=None):
    """Düğüm 4, geçit 0'ın alanını komşulardan öğrenir; hepsi C = 32."""
    from protokoller.desparete import DESPARETE
    r = (DESPARETE(4, sink=0) if bayraklar is None
         else DESPARETE(4, sink=0, bayraklar=bayraklar))
    for j in komsular:
        r.komsular.kanit(j, 0.0)
        r.komsular.sonuc(j, 0.1, True, 0)
    r.komsular.epoch(0.5)
    for j, p in zip(komsular, potansiyel):
        r.alanlar.ilan_al(j, 0, 1, 1, _R, p, 30, 0.6)
    return r


def test_U2_ARDIL_kopunca_GUVENLI_ALTERNATIFE_gecer_ve_KOPMA_beyan_eder():
    """`06` §4.3 U2'nin karşılığı (`36` §6): ardılın bağı koptu, uygulanabilir
    bir alternatif var → yerel geçiş; onarım ve edinim YOK."""
    sys.path.insert(0, str(KOK / "tests2"))
    from test_aodv import _gozlem
    from protokoller.desparete_alan import FORWARDABLE
    from sim2.gozlem.karar import Beyan
    r = _iki_komsulu()
    assert r.alanlar.ardil(0) == 5                      # 48 < 52
    niyet = r.iletim_basarisiz(_gozlem(4, 1.0), 5, "veri")
    assert Beyan("kopma", komsu=5) in niyet
    assert (r.alanlar.durum(0), r.alanlar.ardil(0)) == (FORWARDABLE, 6)
    assert _istekler_of(niyet, "FIELD_SOLICIT") == [], "alternatif varken"
    assert [p.hedef for p in _istekler_of(niyet, "PROBE")] == [5], (
        "kopan ardıl hâlâ gerekliydi: hata oturumu")


def test_U2_TEK_ARDIL_kopunca_ONARIM_WITHDRAWAL_EDINIM_sonra_KURULDU():
    """Alternatif yok → REPAIRING ve geri çekme ilanı; onarım edinimi YALNIZ
    v0.1'de (v0.2 yalın profilde kapalı, K-161). Ardıl yeniden kanıtlanınca
    alan iletilebilir olur ve `rota_kuruldu` beyan edilir — iki profilde."""
    sys.path.insert(0, str(KOK / "tests2"))
    from test_aodv import _gozlem
    from protokoller.desparete_alan import REPAIRING
    from protokoller.desparete_bayrak import PROFIL_V01, PROFIL_V02
    from sim2.gozlem.karar import Beyan
    from sim2.gozlem.kontrol import Uyandirma
    for b, edinim in ((PROFIL_V02, False), (PROFIL_V01, True)):
        r = _iki_komsulu(komsular=(5,), potansiyel=(16,), bayraklar=b)
        niyet = r.iletim_basarisiz(_gozlem(4, 1.0), 5, "veri")
        assert Beyan("kopma", komsu=5) in niyet
        assert r.alanlar.durum(0) == REPAIRING
        assert bool(_istekler_of(niyet, "FIELD_SOLICIT")) == edinim, b
        assert any(isinstance(n, Uyandirma) and n.etiket == "ilan:0"
                   for n in niyet), "geri çekme ilanı acil tetikte"
        r.komsular.kanit(5, 1.2)                         # PROBE onaylandı
        k = _veri(r, 1.4, 7, 0)
        assert k.sonraki == 5 and k.beyanlar("rota_kuruldu")


def test_U4_TEK_ILAN_KAYBI_alani_DUSURMEZ():
    """`21` §4 satır 3: olağan bir FIELD_UPDATE kaybolur → 3 s'lik ömür bir
    sonrakine yeter, alan onarıma düşmez."""
    from protokoller.desparete_alan import FORWARDABLE
    t, _ = _alan()
    t.ilan_al(1, 9, 1, 1, _R, 32, 30, 0.0)            # bitiş 3,0
    # 1,0'daki ilan KAYBOLDU
    t.ilan_al(1, 9, 1, 3, _R, 32, 30, 2.0)            # bitiş 5,0
    t.zaman(9, 3.5, 1e-3)
    assert t.durum(9) == FORWARDABLE and ("onarim", 9) not in t.olaylar


def test_U4_WITHDRAWALdan_sonra_ESKI_SONLU_ilan_ARDIL_OLAMAZ():
    """`21` §4 satır 5: geri çekmeden sonra gecikmiş eski sonlu ilan gelir →
    ADS / withdrawal önbelleği yüzünden sonlu ardıl olmaz."""
    from protokoller.desparete_alan import REPAIRING
    from protokoller.desparete_metrik import SONSUZ
    t, _ = _alan()
    t.ilan_al(1, 9, 1, 2, _R, 32, 30, 0.0)
    t.ilan_al(1, 9, 1, 3, _W, SONSUZ, 0, 0.5)
    assert t.durum(9) == REPAIRING
    t.ilan_al(1, 9, 1, 2, _R, 32, 30, 0.6)            # gecikmiş eski ilan
    assert t.durum(9) == REPAIRING and t.ardil(9) is None
    assert t.sayac["ilan_eski"] == 1


# --------------------------------------------------------------------------
# K-160 §10 · C — v0.1 yalnız geçit alanıyla çalışır (`23` §7)
# --------------------------------------------------------------------------
def test_C_GECIT_DISI_veri_POLITIKA_HATASI_politika_beyaniyla_duser():
    """Geçitte kendi komut paketi de, rölede başka bir paket de: düşer, tek
    beyan `politika` (→ düşme sebebi `politika`, K-171; eskiden beyansızdı
    ve `hedef_yok`a yazılıyordu), edinim başlamaz, kontrol çerçevesi doğmaz."""
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_bayrak import SECENEK_V04
    from sim2.gozlem.karar import Beyan
    for kimlik, kaynak in ((0, 0), (4, 7)):
        # 🔒 v0.4'e sabit: v0.4.1'de (K-172) komut geri izle taşınır.
        r = DESPARETE(kimlik, sink=0, secenekler=SECENEK_V04)
        assert r.komut_alanlari is False
        k = _veri(r, 1.0, kaynak, 0, hedef=9)
        assert k.sonraki is None and not k.beklet
        assert k.beyan == (Beyan("politika"),)
        assert r._sayac["veri_sink_disi"] == 1
        assert r.edinim.sayac["baslatilan"] == 0
        assert _istekler_of(k.niyetler, "FIELD_SOLICIT") == []


def test_C_HEDEF_istekte_ALAN_ACMAZ():
    sys.path.insert(0, str(KOK / "tests2"))
    from protokoller.desparete import DESPARETE
    q, h = DESPARETE(2, sink=0), DESPARETE(9, sink=0)
    h.komsular.kanit(2, 0.0)
    _kontrol(h, 0.1, 2, q._istek(9, 1, 0.0))
    assert 9 not in h.alanlar.alanlar
    assert h._sayac["hedef_alani_acildi"] == 0
    assert h.teshis(9)["komut_alanlari"] is False


def test_SIM_C_yalniz_GECIT_ALANI_komutlar_POLITIKA_ile_duser():
    """Simülatörde (küçük dünya, yere toplama): hiçbir düğümde geçit dışı alan
    yok; geçidin komut paketleri politika hatasıyla düşüyor ve defterde
    TAM OLARAK `politika`ya yazılıyor (K-171); döngü 0. v0.4'e sabit —
    v0.4.1'de komut geri izle taşınır (K-172)."""
    from protokoller.desparete_bayrak import SECENEK_V04
    kfg, kosu, satir, ihlal = _desparete_kos("statik-yok", 12.0,
                                             secenekler=SECENEK_V04)
    assert ihlal["dongu"] == 0 and ihlal["fd_artti"] == 0, ihlal
    p = [d.protokol for d in kosu.dugumler]
    assert all(set(q.alanlar.alanlar) <= {kfg.gecit} for q in p)
    sink_disi = sum(q._sayac["veri_sink_disi"] for q in p)
    assert sink_disi > 0, "sınav boş geçti: hiç komut paketi sorulmadı"
    assert p[kfg.gecit]._sayac["veri_sink_disi"] == sink_disi, (
        "komut paketi geçitten çıkmamalı")
    assert satir["korunum"]["dusen"]["politika"] == sink_disi
    assert satir["metrikler"]["politika_dusen"] == sink_disi
    assert satir["metrikler"]["pdr_komut"] == 0.0, (
        "v0.1 komut taşımaz — yön ayrımı bunu görünür kılmalı")


# --------------------------------------------------------------------------
# K-163 · aday iyileştirmeler V1 · V5 — varsayılan KAPALI
# --------------------------------------------------------------------------
def test_SECENEKLER_varsayilan_V04_ve_TESHISTE():
    """K-167: DESPARETE'nin varsayılanı v0.4 = v0.3 (V1 + V5 + V7, K-164)
    + V8 + V10."""
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_bayrak import (SECENEK_V03, SECENEK_V04,
                                              SECENEK_V041, SECENEK_YOK,
                                              Secenekler)
    assert Secenekler.adlar() == ("yanit_yalniz_onaysiz", "ihtiyac_nitelik",
                                  "nitelik_olcumu", "ilan_sakla",
                                  "hedefli_canlilik", "istek_tanidik",
                                  "soru_nitelik", "aclik_nitelik",
                                  "komut_ters_yol")
    assert not any(SECENEK_YOK.degerler())
    # K-172: V11 (`komut_ters_yol`) eklendi — v0.3 ve v0.4'te KAPALI.
    v03 = (True, True, True, False, False, False, False, False, False)
    v04 = (True, True, True, False, False, True, False, True, False)
    assert SECENEK_V03.degerler() == v03
    assert SECENEK_V04.degerler() == v04
    v041 = v04[:-1] + (True,)                  # K-172: v0.4.1 = v0.4 + V11
    assert SECENEK_V041.degerler() == v041
    r = DESPARETE(4, sink=0)
    assert r.secenekler == SECENEK_V041
    assert r.teshis(4)["secenekler"] == v041
    assert DESPARETE(4, sink=0, secenekler=SECENEK_YOK).teshis(4)[
        "secenekler"] == (False,) * 9


def test_SIM_V03_GECIT_kimseyi_NITELENDIRMEZ_dugumler_GECIDI_nitelendirir():
    """v0.3 ve v0.4'te (varsayılan) V5: geçidin kendi alanı var, hiçbir ilan
    onun için uygulanabilir değil → komşu nitelendirmez (V10 kendi alanına
    uygulanmaz); düğümler geçidi nitelendirir ve veri geçide ulaşır."""
    from protokoller.desparete_komsu import ACTIVE
    kfg, kosu, satir, _ihlal = _desparete_kos("statik-yok", 12.0)
    p = [d.protokol for d in kosu.dugumler]
    g = kfg.gecit
    assert p[g].komsular.sayac["aday_acilan"] == 0
    assert any(q.komsular.durum(g) == ACTIVE or q.komsular.sayac["gecis_active"]
               for q in p if q.kimlik != g)
    assert satir["metrikler"]["pdr"] > 0


def test_V1_ILK_denemede_YANIT_istenmez_TEKRARDA_istenir_ALICI_bite_uyar():
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_bayrak import Secenekler
    from protokoller.desparete_komsu import ProbeIstegi
    s = Secenekler(yanit_yalniz_onaysiz=True)
    q = DESPARETE(2, sink=0, secenekler=s)
    ilk = q._probe(ProbeIstegi(4, 1, 0.1, "nitelik"))
    tekrar = q._probe(ProbeIstegi(4, 2, 0.0, "nitelik", 2))
    assert dict(ilk.yuk)["probe_bayraklar"] == 0
    assert dict(tekrar.yuk)["probe_bayraklar"] == 1
    r = DESPARETE(4, sink=0, secenekler=s)
    assert _istekler_of(_kontrol(r, 0.2, 2, ilk), "PROBE_REPLY") == []
    assert r._sayac["probe_yanitsiz"] == 1
    assert len(_istekler_of(_kontrol(r, 0.3, 2, tekrar), "PROBE_REPLY")) == 1
    # kapalıyken: bayrak hep 0, alıcı hep yanıtlar (v0.2 birebir)
    from protokoller.desparete_bayrak import SECENEK_YOK
    q0 = DESPARETE(2, sink=0, secenekler=SECENEK_YOK)
    r0 = DESPARETE(4, sink=0, secenekler=SECENEK_YOK)
    assert dict(q0._probe(ProbeIstegi(4, 2, 0.0, "nitelik", 2)).yuk)[
        "probe_bayraklar"] == 0
    assert len(_istekler_of(_kontrol(r0, 0.3, 2, q0._probe(
        ProbeIstegi(4, 1, 0.1, "nitelik"))), "PROBE_REPLY")) == 1


def test_V1_TEKRAR_denemesi_numarasini_TASIR():
    k = _tablo()
    k.aday(7, 0.0)
    assert k.zaman(7, 0.6) == []
    ikinci = k.zaman(7, 0.8)
    assert [p.deneme for p in ikinci] == [2]


def test_V5_yalniz_UYGULANABILIR_ilanin_sahibi_NITELENIR():
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_bayrak import Secenekler
    from protokoller.desparete_bicim import DURUM_REACHABLE
    from protokoller.desparete_komsu import ProbeIstegi

    def ilan(kimlik, dfsn, potansiyel):
        return DESPARETE(kimlik, sink=0)._field_update(
            0, (dfsn, 1, DURUM_REACHABLE, potansiyel), None, 0.0)

    def nitelik(niyet):
        return [p.hedef for p in _istekler_of(niyet, "PROBE")]

    s = Secenekler(ihtiyac_nitelik=True)
    r = DESPARETE(4, sink=0, secenekler=s)
    assert nitelik(_kontrol(r, 0.1, 5, ilan(5, 1, 16))) == [5], "alan yok"
    p6 = DESPARETE(6, sink=0)._probe(ProbeIstegi(4, 1, 0.1, "nitelik"))
    assert nitelik(_kontrol(r, 0.2, 6, p6)) == [], "PROBE nitelik açmaz"
    assert r.komsular.kayit(6) is None and r._sayac["nitelik_ertelendi"] == 1
    r.komsular.kanit(5, 0.3)
    r.komsular.sonuc(5, 0.3, True, 0)
    r.komsular.epoch(0.5)
    r.alanlar.ilan_al(5, 0, 1, 1, _R, 16, 30, 0.6)            # FD (1, 48)
    assert r.alanlar.alanlar[0].fd == (1, 48)
    assert nitelik(_kontrol(r, 0.7, 7, ilan(7, 1, 48))) == [], "48 < 48 değil"
    assert nitelik(_kontrol(r, 0.8, 8, ilan(8, 1, 40))) == [8]
    assert nitelik(_kontrol(r, 0.9, 9, ilan(9, 2, 100))) == [9], "yeni tur"
    from protokoller.desparete_bayrak import SECENEK_YOK
    kapali = DESPARETE(4, sink=0, secenekler=SECENEK_YOK)
    assert nitelik(_kontrol(kapali, 0.2, 6, p6)) == [6], "v0.2: her duyulan"


def test_V7_ILK_ORNEK_olmadan_MALIYET_YOK_olcum_PROBEu_onu_uretir():
    """K-163 §2'nin içgörüsü: nitelik onayı komşuyu ACTIVE yapar ama M0.1
    örneği DEĞİLDİR → maliyet yok, aday olamaz. v0.2'de ilk örneği karşı
    yönün PROBE yanıtı sağlıyordu; V1/V5 onu kaldırınca ağ kilitlenir.
    V7'nin ölçüm PROBE'u ACTIVE iken onaylanır → ilk örnek."""
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_komsu import ProbeIstegi
    r = DESPARETE(4, sink=0)
    r.komsular.aday(5, 0.0)
    r.komsular.sonuc(5, 0.1, True, 0)                  # nitelik onayı
    r.komsular.epoch(0.5)
    assert r._aktif_mi(5) and r._maliyet(5) is None, "onay örnek değil"
    assert r.komsular.olcum(5, 0.6) == [ProbeIstegi(5, 2, 0.1, "olcum")]
    assert r.komsular.olcum(5, 0.61) == [], "açık oturum varken yok"
    r.komsular.sonuc(5, 0.7, True, 0)                  # ölçüm onayı
    r.komsular.epoch(1.0)
    assert r._maliyet(5) == 32, "ilk örnek → maliyet"
    assert r.komsular.olcum(5, 1.1) == [], "örneği olana ölçüm yok"


def test_V7_yeni_ACTIVE_komsuya_KANCADA_olcum_PROBEu():
    sys.path.insert(0, str(KOK / "tests2"))
    from test_aodv import _gozlem
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_bayrak import Secenekler
    for s, beklenen in ((Secenekler(nitelik_olcumu=True), [5]),
                        (Secenekler(), [])):
        r = DESPARETE(4, sink=0, secenekler=s)
        r.komsular.aday(5, 0.0)
        r.komsular.sonuc(5, 0.1, True, 0)
        niyet = r.zamanlayici_doldu(_gozlem(4, 0.5), "ilan")
        assert [p.hedef for p in _istekler_of(niyet, "PROBE")] == beklenen, s


def test_V5a_ACTIVE_olmayanin_ilani_SAKLANIR_ACTIVE_olunca_KALAN_omurle():
    """K-164 V5a: reddedilecek ilan saklanır; komşu ACTIVE olunca olağan
    yoldan, ORİJİNAL bitiş anıyla uygulanır. Kapalıyken reddedilir."""
    sys.path.insert(0, str(KOK / "tests2"))
    from test_aodv import _gozlem
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_bayrak import SECENEK_V03, Secenekler
    from protokoller.desparete_bicim import DURUM_REACHABLE
    ilan = DESPARETE(5, sink=0)._field_update(
        0, (1, 1, DURUM_REACHABLE, 16), None, 0.0)       # ömür 30 kuanta
    acik = Secenekler(True, True, True, ilan_sakla=True)
    r = DESPARETE(4, sink=0, secenekler=acik)
    _kontrol(r, 1.0, 5, ilan)
    assert r._sayac["ilan_saklandi"] == 1 and 0 not in r.alanlar.alanlar
    r.komsular.kanit(5, 1.2)
    r.zamanlayici_doldu(_gozlem(4, 1.4), "ilan")
    assert r._sayac["saklanan_uygulandi"] == 1
    assert r.alanlar.alanlar[0].ilanlar[5].bitis == pytest.approx(4.0), (
        "orijinal bitiş: varış 1,0 + 3,0")
    eski = DESPARETE(4, sink=0, secenekler=acik)
    _kontrol(eski, 1.0, 5, ilan)
    eski.komsular.kanit(5, 4.5)
    eski.zamanlayici_doldu(_gozlem(4, 4.6), "ilan")
    assert eski._sayac["saklanan_eskidi"] == 1 and 0 not in eski.alanlar.alanlar
    kapali = DESPARETE(4, sink=0, secenekler=SECENEK_V03)
    _kontrol(kapali, 1.0, 5, ilan)
    assert kapali._sayac["ilan_saklandi"] == 0
    assert kapali.alanlar.sayac["ilan_aktif_disi"] == 1


def test_SIM_SECENEKLER_V1_V5_V7_ISLIYOR_dongu_YOK():
    """Üçü birlikte (V1 · V5 yalnız V7'yle işler, K-163 §2)."""
    from protokoller.desparete_bayrak import Secenekler
    s = Secenekler(yanit_yalniz_onaysiz=True, ihtiyac_nitelik=True,
                   nitelik_olcumu=True)
    _kfg, kosu, satir, ihlal = _desparete_kos("statik-yok", 12.0,
                                              secenekler=s)
    assert satir["korunum"]["gecerli"]
    assert ihlal["denetim"] > 1000
    assert ihlal["dongu"] == 0 and ihlal["fd_artti"] == 0, ihlal
    p = [d.protokol for d in kosu.dugumler]
    assert sum(q._sayac["probe_yanitsiz"] for q in p) > 0
    assert sum(q._sayac["nitelik_ertelendi"] for q in p) > 0
    assert sum(q._sayac["veri_iletilen"] for q in p) > 0
    assert sum(q.komsular.sayac["probe_olcum"] for q in p) > 0
    for te in satir["teshis"]["dugum"]:
        assert tuple(te["secenekler"]) == (True, True, True, False, False,
                                           False, False, False, False)


def test_V2p_FILTRE_bosta_PROBEu_yalniz_GEREKLI_komsuya():
    from protokoller.desparete_komsu import KomsuTablosu
    sayac = iter(range(1, 100))
    gerekli = {7}
    k = KomsuTablosu(lambda: next(sayac), lambda j: False, True,
                     lambda j, t: j in gerekli)
    k.kanit(7, 0.0)
    k.kanit(8, 0.0)
    assert [p.tur for p in k.zaman(7, 2.0)] == ["bosta"]
    assert k.zaman(8, 2.0) == [] and k.sayac["bosta_atlandi"] == 1


def test_V2p_CANLI_TUT_ardil_ve_en_iyi_IKI_yedek():
    """Geçit alanının 4 uygulanabilir adayı: ardıl + en ucuz 2 yedek canlı
    tutulur, dördüncü tutulmaz; alan onarımdayken kimse (uygulanabilir aday
    yok)."""
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_bayrak import Secenekler
    r = DESPARETE(4, sink=0, secenekler=Secenekler(hedefli_canlilik=True))
    for j in (5, 6, 7, 8):
        r.komsular.kanit(j, 0.0)
        r.komsular.sonuc(j, 0.1, True, 0)
    r.komsular.epoch(0.5)
    for j, p in ((5, 16), (6, 20), (7, 24), (8, 28)):     # hepsi C = 32
        r.alanlar.ilan_al(j, 0, 1, 1, _R, p, 30, 0.6)
    assert r.alanlar.ardil(0) == 5
    assert [j for j in (5, 6, 7, 8) if r._canli_tut(j, 0.7)] == [5, 6, 7]


def test_SIM_V2p_ISLIYOR_dongu_YOK():
    from protokoller.desparete_bayrak import Secenekler
    s = Secenekler(True, True, True, hedefli_canlilik=True)
    _kfg, kosu, satir, ihlal = _desparete_kos("statik-yok", 12.0,
                                              secenekler=s)
    assert satir["korunum"]["gecerli"]
    assert ihlal["dongu"] == 0 and ihlal["fd_artti"] == 0, ihlal
    p = [d.protokol for d in kosu.dugumler]
    assert sum(q.komsular.sayac["probe_bosta"] for q in p) > 0
    assert sum(q.komsular.sayac["bosta_atlandi"] for q in p) > 0
    assert satir["metrikler"]["pdr"] > 0


# --------------------------------------------------------------------------
# K-166 · denetim K-1 — edinim yolu UÇTAN UCA: ön koşulu (gönderen ACTIVE)
# protokol KENDİSİ kurar. Yukarıdaki istek ve solicit testleri onu elle
# kuruyordu (`komsular.kanit`) ve V5'in yolu kapattığını göremedi.
# --------------------------------------------------------------------------
def _edinim_sayaclari(kosu) -> dict:
    p = [d.protokol for d in kosu.dugumler]
    return {ad: sum(q._sayac[ad] for q in p)
            for ad in ("solicit_gonderilen", "solicit_yanitlanan",
                       "istek_gonderilen", "istek_iletilen", "hedefte_istek",
                       "istek_aktif_disi")}


def test_SIM_v02_ALAN_SORUSU_komsularca_YANITLANIR():
    """Başlangıçta alanı olmayan düğüm FIELD_SOLICIT gönderir (`23` §5.2);
    alanı olan komşu, soranı ACTIVE görüyorsa yanıtlar. Ölçüldü (K-166):
    statik 12 s, v0.2 — 9 soru, 5 yanıt."""
    from protokoller.desparete_bayrak import SECENEK_YOK
    _kfg, kosu, _satir, _ihlal = _desparete_kos("statik-yok", 12.0,
                                                secenekler=SECENEK_YOK)
    s = _edinim_sayaclari(kosu)
    assert s["solicit_gonderilen"] > 0, "sınav boş geçti: soru yok"
    assert s["solicit_yanitlanan"] > 0, s


def test_SIM_v03_K1_BULGUSU_soru_ve_istek_yolu_KAPALI():
    """🔎 TESPİT testi — K-166'nın K-1 bulgusu v0.3'te yeniden üretilir.
    v0.3 yalnız yeniden üretilebilirlik için kodda (varsayılan v0.4, K-167).
    Ölçüldü: statik 12 s — 25 soru → 0 yanıt; 14 istek → 0 iletim, 50
    ACTIVE-dışı ret. (K-166'da bu test v0.3 varsayılanken katı xfail'di.)"""
    from protokoller.desparete_bayrak import SECENEK_V03
    _kfg, kosu, _satir, _ihlal = _desparete_kos("statik-yok", 12.0,
                                                secenekler=SECENEK_V03)
    s = _edinim_sayaclari(kosu)
    assert s["solicit_gonderilen"] > 0 and s["istek_gonderilen"] > 0, s
    assert s["solicit_yanitlanan"] == 0, s
    assert s["istek_iletilen"] + s["hedefte_istek"] == 0, s


def test_SIM_VARSAYILAN_v04_ISTEK_yolu_ACIK():
    """v0.4 (varsayılan, K-167): V8 ile istek, gönderenin PROBE'uyla tanıdık
    olan komşuda kabul edilir ve geçide ulaşır. Ölçüldü: statik 12 s — 10
    istek, 38 iletim, 54 tanıdık kabulü, geçitte 5.
    🔎 Soru (FIELD_SOLICIT) yanıtı v0.4'te de ~0: `23` §5.2 ACTIVE ister ve
    V5 aşağıdakini nitelendirmez; V9 bunu açıyordu ama zararlı çıktı
    (K-167 §5). Edinim, isteğe rölelerin verdiği tek alıcılı yanıtla sürer."""
    kfg, kosu, _satir, _ihlal = _desparete_kos("statik-yok", 12.0)
    s = _edinim_sayaclari(kosu)
    p = [d.protokol for d in kosu.dugumler]
    assert s["istek_gonderilen"] > 0 and s["istek_iletilen"] > 0, s
    assert sum(q._sayac["istek_tanidik_kabul"] for q in p) > 0
    assert p[kfg.gecit]._sayac["hedefte_istek"] > 0, s


def test_SIM_UCTAN_UCA_ACLIK_istegi_HEDEFTE_TUR_ARTIRIR_dongu_YOK():
    """`23` §5.4'ün uçtan uca yolu, v0.2: hareketli ağda uygulanabilirlik
    açlığı → DFSN_REQUEST → röleler iletir → geçit turu BİR artırır → FD'ler
    yeni turda sıfırlanır; her kancadan sonra döngü ve aynı turda FD artışı
    YOK. Senaryo ölçülerek seçildi (K-166): formasyon, tohum 1000, 60 s —
    geçit 50,9 s'de bir açlık isteği işliyor ve turu artırıyor (bağımsız
    ve görev kollarında 60 s içinde tur artışı yok)."""
    from protokoller.desparete_bayrak import SECENEK_YOK
    kfg, kosu, satir, ihlal = _desparete_kos("formasyon-yok", 60.0,
                                             secenekler=SECENEK_YOK)
    assert satir["korunum"]["gecerli"]
    assert ihlal["dongu"] == 0 and ihlal["fd_artti"] == 0, ihlal
    s = _edinim_sayaclari(kosu)
    assert s["istek_iletilen"] > 0, s
    g = kosu.dugumler[kfg.gecit].protokol
    assert g._sayac["hedefte_istek"] >= 1, s
    assert g.alanlar.sayac["tur_artirildi"] >= 1
    assert g.alanlar.alanlar[kfg.gecit].dfsn >= 2, "tur 1'den başlar"


# --------------------------------------------------------------------------
# K-167 · K-1'in düzeltme adayı — V8 (istek: `23` §2'nin ilk kabul kuralı) ·
# V9 (soru nitelik açar). Seçenek; varsayılan DEĞİL (ölçülüyor).
# --------------------------------------------------------------------------
def test_V8_ISTEK_TANIDIKTAN_kabul_ACTIVE_olmasa_da():
    """`23` §2: bana hedefli PROBE göndermiş komşunun isteği ACTIVE olmasa
    da kabul edilir ve iletilir. PROBE gelmeden ve seçenek kapalıyken
    (v0.3) reddedilir."""
    sys.path.insert(0, str(KOK / "tests2"))
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_bayrak import SECENEK_V03, SECENEK_V03_EDINIM
    from protokoller.desparete_komsu import ACTIVE, ProbeIstegi
    for sec, beklenen in ((SECENEK_V03, 0), (SECENEK_V03_EDINIM, 1)):
        q = DESPARETE(2, sink=0, secenekler=sec)
        r = DESPARETE(4, sink=0, secenekler=sec)
        assert _istekler_of(_kontrol(r, 0.1, 2, q._istek(0, 1, 0.0)),
                            "DFSN_REQUEST") == [], "PROBE yok → ret"
        _kontrol(r, 0.2, 2, q._probe(ProbeIstegi(4, 1, 0.0, "nitelik")))
        assert r.komsular.durum(2) != ACTIVE, "V5: PROBE nitelik açmaz"
        ilet = _istekler_of(_kontrol(r, 0.3, 2, q._istek(0, 2, 0.3)),
                            "DFSN_REQUEST")
        assert len(ilet) == beklenen
        assert r._sayac["istek_tanidik_kabul"] == beklenen
        assert r._sayac["istek_aktif_disi"] == 2 - beklenen


def test_V9_SORU_NITELIK_acar_YANIT_yalniz_ACTIVE_olunca():
    """Alanı iletilebilir düğüm, ACTIVE olmayan komşunun sorusuyla onu
    nitelendirir; yanıt ancak ACTIVE olunca (`23` §5.2). Alanı olmayan
    düğüm ve seçenek kapalıyken (v0.3) nitelik açılmaz."""
    sys.path.insert(0, str(KOK / "tests2"))
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_bayrak import SECENEK_V03, SECENEK_V03_EDINIM
    for sec, nitelik in ((SECENEK_V03, 0), (SECENEK_V03_EDINIM, 1)):
        q = DESPARETE(2, sink=0, secenekler=sec)
        g = DESPARETE(0, sink=0, secenekler=sec)     # geçit: kendi alanı
        r = DESPARETE(4, sink=0, secenekler=sec)     # alanı yok
        niyet = _kontrol(g, 0.1, 2, q._solicit(0))
        assert _istekler_of(niyet, "FIELD_UPDATE") == [], "ACTIVE değil"
        assert g._sayac["soru_nitelik"] == nitelik
        assert (g.komsular.kayit(2) is not None) == bool(nitelik)
        _kontrol(r, 0.1, 2, q._solicit(0))
        assert r._sayac["soru_nitelik"] == 0 and r.komsular.kayit(2) is None
        g.komsular.kanit(2, 0.2)
        yanit = _istekler_of(_kontrol(g, 0.3, 2, q._solicit(0)),
                             "FIELD_UPDATE")
        assert len(yanit) == 1 and yanit[0].hedef == 2


def test_V10_ALAN_ILETILEMEZKEN_AYNI_TURUN_SONLU_ilani_NITELIK_acar():
    """V5 yalnız uygulanabilir ilanın sahibini nitelendirir. V10: alan
    onarımdayken aynı turdan uygulanabilir OLMAYAN sonlu ilanın sahibi de —
    yeni turdan sonra ardıl adayıdır ve açlık (`23` §5.4) ancak ACTIVE bir
    komşuyla görünür. Alan iletilebilirken ve eski turda açılmaz."""
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_alan import REPAIRING
    from protokoller.desparete_bayrak import SECENEK_V03, SECENEK_V04
    for sec, beklenen in ((SECENEK_V03, False), (SECENEK_V04, True)):
        r = DESPARETE(4, sink=0, secenekler=sec)
        r.komsular.kanit(5, 0.0)
        r.komsular.sonuc(5, 0.1, True, 0)
        r.komsular.epoch(0.5)
        r.alanlar.ilan_al(5, 0, 1, 1, _R, 16, 30, 0.6)
        a = r.alanlar.alanlar[0]
        uzak = {"durum": _R, "potansiyel": a.fd[1] + 50, "hedef": 1, "dfsn": 1}
        assert not r._nitelige_deger("FIELD_UPDATE", uzak), "iletilebilir"
        a.durum = REPAIRING
        assert r._nitelige_deger("FIELD_UPDATE", uzak) is beklenen
        assert not r._nitelige_deger("FIELD_UPDATE", dict(uzak, dfsn=0)), \
            "eski tur aday değil"
        assert not r._nitelige_deger(
            "FIELD_UPDATE", dict(uzak, potansiyel=SONSUZ)), "sonsuz aday değil"


def test_SIM_v04_UCTAN_UCA_ACLIK_TUR_ARTISI_dongu_YOK():
    """`23` §5.4 uçtan uca, v0.4 (varsayılan): V10 açlığı görünür kılar →
    açlık nedenli istek → V8 ile geçide ulaşır → tur BİR artar; her
    kancadan sonra döngü ve aynı turda FD artışı YOK. Senaryo ölçülerek
    seçildi (`v04_senaryo.py`): bağımsız, tohum 1000 — ilk artış 41,6 s.
    🔒 v0.4'e SABİT (K-172): senaryo bu profil için ölçülerek seçildi. V11
    alan ve edinim mantığına dokunmaz ama komut trafiğini açar; MAC
    zamanlaması değişince bu tohumdaki açlık olayı doğmuyor (yörünge farkı)."""
    from protokoller.desparete_bayrak import SECENEK_V04
    kfg, kosu, satir, ihlal = _desparete_kos("bagimsiz-yok", 50.0,
                                             secenekler=SECENEK_V04)
    assert satir["korunum"]["gecerli"]
    assert ihlal["dongu"] == 0 and ihlal["fd_artti"] == 0, ihlal
    p = [d.protokol for d in kosu.dugumler]
    g = p[kfg.gecit]
    assert sum(q._sayac["istek_aclik"] for q in p) >= 1
    assert g._sayac["hedefte_aclik"] >= 1
    assert g.alanlar.sayac["tur_artirildi"] >= 1
    assert g.alanlar.alanlar[kfg.gecit].dfsn >= 2


def test_SIM_V03_EDINIM_SORU_ve_ISTEK_yolu_ACIK_dongu_YOK():
    """K-167: v0.3 + V8 · V9 — K-166'nın katı xfail'indeki kapı bu profilde
    geçer; her kancadan sonra döngü ve aynı turda FD artışı yok."""
    from protokoller.desparete_bayrak import SECENEK_V03_EDINIM
    _kfg, kosu, satir, ihlal = _desparete_kos("statik-yok", 12.0,
                                              secenekler=SECENEK_V03_EDINIM)
    assert satir["korunum"]["gecerli"]
    assert ihlal["dongu"] == 0 and ihlal["fd_artti"] == 0, ihlal
    s = _edinim_sayaclari(kosu)
    assert s["solicit_gonderilen"] > 0 and s["istek_gonderilen"] > 0, s
    assert s["solicit_yanitlanan"] > 0, s
    assert s["istek_iletilen"] + s["hedefte_istek"] > 0, s
    assert satir["metrikler"]["pdr"] > 0


# --------------------------------------------------------------------------
# K-172 · V11 — komut GERİ İZİ (telemetriden öğrenilir, ek kontrol mesajı yok)
# --------------------------------------------------------------------------
def _v11():
    from dataclasses import replace
    from protokoller.desparete_bayrak import SECENEK_V04
    return replace(SECENEK_V04, komut_ters_yol=True)


def _duy(p, t, gonderen, kaynak, sira, hedef=None, paket_hedefi=0,
         tur="veri"):
    sys.path.insert(0, str(KOK / "tests2"))
    from test_aodv import _gozlem
    from sim2.gozlem.pencere import PaketGorunumu
    paket = PaketGorunumu(hedef=paket_hedefi, kaynak=kaynak, ttl=30,
                          atlama_sayisi=1, bayt=512, kaynak_sira=sira)
    return p.cerceve_duyuldu(_gozlem(p.kimlik, t), gonderen, tur,
                             p.kimlik if hedef is None else hedef, -60, paket)


def test_V11_KAPALIYKEN_kanca_YOK_komut_POLITIKA():
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_bayrak import SECENEK_V04
    r = DESPARETE(4, sink=0, secenekler=SECENEK_V04)
    assert getattr(r, "cerceve_duyuldu", None) is None, (
        "kapalıyken kanca sunulursa her çerçevede çağrılır, v0.4 birebir kalmaz")
    assert _veri(r, 1.0, 0, 1, hedef=9).beyanlar("politika")


def test_V11_iz_YALNIZ_DAHA_YENI_sirayla_ve_YALNIZ_uygun_cerceveden():
    from protokoller.desparete import DESPARETE
    r = DESPARETE(4, sink=0, secenekler=_v11())
    _duy(r, 1.0, 7, kaynak=9, sira=5)
    assert r._geri_iz[9] == (7, 5, 1.0)
    _duy(r, 1.1, 8, kaynak=9, sira=4)            # eski sıra
    _duy(r, 1.2, 8, kaynak=9, sira=5)            # aynı sıra (tekrar)
    assert r._geri_iz[9][0] == 7
    _duy(r, 1.3, 8, kaynak=9, sira=6, hedef=3)   # başkasına adresli
    _duy(r, 1.4, 8, kaynak=9, sira=6, paket_hedefi=5)   # geçide gitmiyor
    _duy(r, 1.5, 8, kaynak=9, sira=6, tur="beacon")
    _duy(r, 1.6, 8, kaynak=4, sira=9)            # kendi paketim
    assert r._geri_iz == {9: (7, 5, 1.0)}
    _duy(r, 2.0, 8, kaynak=9, sira=6)
    assert r._geri_iz[9] == (8, 6, 2.0)
    assert r._sayac["geri_iz_ogrenilen"] == 2


def test_V11_komut_IZI_izler_BAYAT_iz_ve_MAC_hatasi_DUSURUR():
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_bicim import T_GERI_IZ_S
    sys.path.insert(0, str(KOK / "tests2"))
    from test_aodv import _gozlem
    r = DESPARETE(4, sink=0, secenekler=_v11())
    _duy(r, 1.0, 7, kaynak=9, sira=1)
    k = _veri(r, 1.5, 0, 1, hedef=9)
    assert k.sonraki == 7 and not k.beyan
    k = _veri(r, 1.0 + T_GERI_IZ_S + 0.01, 0, 2, hedef=9)
    assert k.sonraki is None and not k.beyan, "bayat iz → hedef_yok"
    _duy(r, 10.0, 7, kaynak=9, sira=2)
    r.iletim_basarisiz(_gozlem(4, 10.1), 7, "veri")
    assert 9 not in r._geri_iz and r._sayac["geri_iz_silinen"] == 1
    assert _veri(r, 10.2, 0, 3, hedef=9).sonraki is None
    assert _veri(r, 10.3, 0, 4, hedef=11).sonraki is None   # hiç iz yok
    s = r._sayac
    assert (s["komut_iz_iletilen"], s["komut_izsiz"],
            s["veri_sink_disi"]) == (1, 3, 0)


def test_SIM_V11_komutlar_TESLIM_dongu_YOK_politika_YOK():
    """Küçük dünya, yere toplama: komutlar geri izle teslim ediliyor; komut
    Hop Limit'e takılmıyor (izde döngü yok); politika düşüşü kalmadı."""
    kfg, kosu, satir, ihlal = _desparete_kos("statik-yok", 12.0,
                                             secenekler=_v11())
    assert satir["korunum"]["gecerli"]
    assert ihlal["dongu"] == 0 and ihlal["fd_artti"] == 0, ihlal
    p = [d.protokol for d in kosu.dugumler]
    s = {a: sum(q._sayac[a] for q in p) for a in
         ("komut_iz_iletilen", "geri_iz_ogrenilen", "veri_hop_siniri")}
    assert s["geri_iz_ogrenilen"] > 0 and s["komut_iz_iletilen"] > 0, s
    assert s["veri_hop_siniri"] == 0, s
    m, d = satir["metrikler"], satir["korunum"]["dusen"]
    assert d["politika"] == 0 and d["ttl"] == 0
    assert m["pdr_komut"] > 0.5, m["pdr_komut"]
    assert m["duyma_bildirimi"] > 0
