"""
OLSR — RFC 3626 uygunluk kapıları (U1–U4) ve gerçekleme değişmezleri.

🔴 BU DOSYA BİR KABUL KAPISIDIR
===============================
`v2/06` §4.4: *"U1–U4 koşulur; geçilmeden protokol kabul edilmez"* —
K-137'nin iki parçalı hâliyle. Burası yapı yarısı; tam ölçek kanıtı
`kalibrasyon/`da koşar.

🔒 SINAV VEKTÖRLERİ BELGENİN KENDİSİNDEN
========================================
Biçim boyutları §3.3'ün *"Packet Length < 16"* kuralına, Vtime kodlaması
§18.3'ün dört çözülmüş örneğine bağlı — ikisi de ham metinden (`02` §R2.1).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from protokoller.olsr import OLSR, _Bag, _Hist  # noqa: E402
from protokoller.olsr_bicim import (  # noqa: E402
    ASYM_LINK, BASLIK_BAYT, HELLO, HELLO_INTERVAL_S, LOST_LINK,
    MAXJITTER_S, MPR_NEIGH, NEIGHB_HOLD_TIME_S, NOT_NEIGH,
    SYM_LINK, SYM_NEIGH, TC, TC_INTERVAL_S, TC_TTL, TIP_HELLO, TIP_TC,
    TOP_HOLD_TIME_S, WILL_DEFAULT, bag_kodu, zaman_coz, zaman_kodla)
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.kosum.sonuc import sonuc_satiri  # noqa: E402
from test_aodv import _gozlem, _istekler, _uyandirmalar  # noqa: E402
from test_kosum import _konfig  # noqa: E402


def _hello(kaynak: int, psn: int, bloklar: dict[int, list[int]]) -> tuple:
    """Bir HELLO yükü. `bloklar`: bağ kodu → adresler."""
    kodlar = sorted(bloklar)
    adresler = tuple(a for k in kodlar for a in bloklar[k])
    boy = 12 + 4 + 4 * len(kodlar) + 4 * len(adresler)
    return tuple({
        "paket_boyu": boy + 4, "paket_sira": psn, "mesaj_tipi": TIP_HELLO,
        "vtime": zaman_kodla(NEIGHB_HOLD_TIME_S), "mesaj_boyu": boy,
        "kaynak": kaynak, "ttl": 1, "atlama": 0, "mesaj_sira": psn,
        "ayrilmis": 0, "htime": zaman_kodla(HELLO_INTERVAL_S),
        "istek": WILL_DEFAULT, "blok_kodu": tuple(kodlar),
        "blok_ayrilmis": tuple(0 for _ in kodlar),
        "blok_boyu": tuple(4 + 4 * len(bloklar[k]) for k in kodlar),
        "komsu_adresi": adresler}.items())


def _tc(kaynak: int, psn: int, msn: int, ansn: int, adresler: tuple,
        ttl: int = TC_TTL) -> tuple:
    boy = 12 + 4 + 4 * len(adresler)
    return tuple({
        "paket_boyu": boy + 4, "paket_sira": psn, "mesaj_tipi": TIP_TC,
        "vtime": zaman_kodla(TOP_HOLD_TIME_S), "mesaj_boyu": boy,
        "kaynak": kaynak, "ttl": ttl, "atlama": 1, "mesaj_sira": msn,
        "ansn": ansn, "ayrilmis": 0, "komsu_adresi": adresler}.items())


def _simetrik_yap(p: OLSR, n: int, t: float = 0.0) -> None:
    """Sınav kurulumu: n'yi yerleşik ve simetrik bir komşu yap."""
    p._bag[n] = _Bag(sym_bitis=t + 100, asym_bitis=t + 100, bitis=t + 100)
    p._hist[n] = _Hist(kalite=0.95, bekleyen=False, kayip_bitis=t - 1,
                       son_psn=0, son_duyulma_s=t, htime_s=HELLO_INTERVAL_S,
                       sessiz_sayilan=0, sessiz_kredi=0, eksik={})
    p._kirli = True


# ==========================================================================
# BİÇİMLER — §3.3 · §6.1 · §9.1 · §18.3
# ==========================================================================
def test_RFC_BASLIK_16_bayt_ve_mesaj_boyutlari():
    """🔒 §3.4 adım 1: *"Packet Length < 16"* — 4 (paket) + 12 (mesaj)."""
    assert BASLIK_BAYT == 16
    bos_hello = dict(_hello(1, 1, {}))
    assert HELLO.bayt(bos_hello) == 20, "HELLO = 16 başlık + 4 gövde"
    y = dict(_hello(1, 1, {bag_kodu(SYM_NEIGH, SYM_LINK): [2, 3],
                           bag_kodu(MPR_NEIGH, SYM_LINK): [4, 5, 6]}))
    assert HELLO.bayt(y) == 20 + 2 * 4 + 5 * 4, "blok başına 4, adres başına 4"
    assert HELLO.bayt(y) == y["paket_boyu"], "Packet Length alanı tutarlı"
    assert TC.bayt(dict(_tc(1, 1, 1, 1, (2, 3, 4)))) == 20 + 3 * 4


def test_RFC_Vtime_ORNEKLERI_birebir():
    """🔒 §18.3'ün dört çözülmüş örneği — ham metinden."""
    for t, (a, b) in ((2, (0, 5)), (6, (8, 6)), (15, (14, 7)), (30, (14, 8))):
        k = zaman_kodla(t)
        assert (k >> 4, k & 0x0F) == (a, b), f"{t} s yanlış kodlandı"
        assert zaman_coz(k) == pytest.approx(t)


# ==========================================================================
# §7.1.1 · BAĞ ALGILAMA ve §14 · HİSTEREZİS
# ==========================================================================
def test_BAG_ALGILAMA_kendi_adresini_duyunca_SIMETRIK_olur():
    """Asimetrik → simetrik, ve histerezis bağı KURMADAN simetri yok."""
    p = OLSR(0)
    # 1, 0'ı henüz duymuyor: bağ asimetrik.
    p.kontrol_alindi(_gozlem(0, 1.0), 1, "HELLO", _hello(1, 1, {}), True)
    assert not p._simetrik_mi(1, 1.0), "kendi adresimi duymadan simetrik oldu"
    # 1, 0'ı ASYM olarak ilan ediyor → L_SYM_time kurulur. Histerezis:
    # 0,5 → 0,75 (bant, hâlâ bekleyen) → 0,875 (> 0,8, kuruldu).
    kod = bag_kodu(NOT_NEIGH, ASYM_LINK)
    p.kontrol_alindi(_gozlem(0, 2.0), 1, "HELLO", _hello(1, 2, {kod: [0]}), True)
    assert p._hist[1].bekleyen, "kalite 0,75'te bağ kurulmuş sayıldı"
    p.kontrol_alindi(_gozlem(0, 3.0), 1, "HELLO", _hello(1, 3, {kod: [0]}), True)
    assert p._hist[1].kalite == pytest.approx(0.875)
    assert p._simetrik_mi(1, 3.0)


def test_HISTEREZIS_iki_ardisik_kayip_bagi_KOPARIR():
    """§14.3: 0,875 → 0,4375 → 0,21875 < 0,3 — bağ bekleyen ve KAYIP."""
    p = OLSR(0)
    kod = bag_kodu(SYM_NEIGH, SYM_LINK)
    for i in range(1, 4):
        p.kontrol_alindi(_gozlem(0, float(i)), 1, "HELLO",
                         _hello(1, i, {kod: [0]}), True)
    assert p._simetrik_mi(1, 3.0)
    # PSN 4 ve 5 kayboldu, 6 geldi. Kayıp MAXJITTER sonra kesinleşir.
    p.kontrol_alindi(_gozlem(0, 4.0), 1, "HELLO", _hello(1, 6, {kod: [0]}), True)
    assert set(p._hist[1].eksik) == {4, 5}, "eksikler bekletilmedi"
    p.zamanlayici_doldu(_gozlem(0, 4.0 + MAXJITTER_S + 0.01), "bakim")
    assert p._hist[1].bekleyen, "iki kayıptan sonra bağ ayakta kaldı"
    assert not p._simetrik_mi(1, 4.6)


def test_HISTEREZIS_titresim_SIRA_DEGISIMI_KAYIP_DEGILDIR():
    """🔴 PSN titreşimden ÖNCE verildiği için havada sıra değişebilir.

    Düzeltilmeden ölçüldü: ~900 pakete karşı 2 563 sahte kayıp.
    """
    p = OLSR(0)
    kod = bag_kodu(SYM_NEIGH, SYM_LINK)
    for psn, t in ((1, 1.0), (3, 1.1), (2, 1.3)):      # 2, 3'ten sonra geldi
        p.kontrol_alindi(_gozlem(0, t), 1, "HELLO",
                         _hello(1, psn, {kod: [0]}), True)
    p.zamanlayici_doldu(_gozlem(0, 5.0), "bakim")
    assert p._sayac["hist_kayip_psn"] == 0, "geç gelen paket kayıp sayıldı"


# ==========================================================================
# §8.3.1 · MPR BULUŞSALI
# ==========================================================================
def test_MPR_TEK_ERISEN_komsu_secilir():
    """N2'deki bir düğüme TEK başına erişen komşu MPR olur (adım 3).

        1 → {10}   2 → {10, 11}   3 → {12}
    11 yalnız 2'den, 12 yalnız 3'ten → MPR {2, 3}; 10 zaten 2'den kapsanıyor.
    """
    p = OLSR(0)
    for n in (1, 2, 3):
        _simetrik_yap(p, n)
    for k in ((1, 10), (2, 10), (2, 11), (3, 12)):
        p._iki[k] = 100.0
    p._guncelle(1.0)
    assert p._mpr == frozenset({2, 3})


# ==========================================================================
# §9.2 · §9.3 · TC ÜRETİMİ ve §3.4.1 · İLETME
# ==========================================================================
def test_TC_yalniz_MPR_SECICISI_varken_uretilir_ve_bos_TC_SURER():
    p = OLSR(0)
    assert p._tc_kur(1.0) == (), "MPR seçicisi yokken TC üretildi"
    p._secici[5] = 100.0
    tc = p._tc_kur(2.0)
    y = dict(tc[0].yuk)
    assert y["komsu_adresi"] == (5,) and y["ttl"] == TC_TTL
    ansn = y["ansn"]
    del p._secici[5]
    # §9.3: küme boşaldı → boş TC geçerlilik süresi boyunca SÜRER, sonra DURUR.
    bos = p._tc_kur(3.0)
    assert bos and dict(bos[0].yuk)["komsu_adresi"] == ()
    assert dict(bos[0].yuk)["ansn"] != ansn, "§9.2: kaldırmada ANSN artmalı"
    assert p._tc_kur(2.0 + TOP_HOLD_TIME_S + 0.1) == ()


def test_TC_ILETME_yalniz_MPR_SECICISINDEN_ve_tekrar_BASTIRILIR():
    """§3.4.1: gönderen beni MPR seçtiyse ilet; aynı mesajı ikinci kez değil."""
    p = OLSR(0)
    _simetrik_yap(p, 1)
    _simetrik_yap(p, 2)
    p._secici[1] = 100.0                     # 1 beni MPR seçti, 2 seçmedi
    cikti = p.kontrol_alindi(_gozlem(0, 1.0), 1, "TC",
                             _tc(9, psn=1, msn=7, ansn=1, adresler=(8,), ttl=5),
                             True)
    ilet = [i for i in _istekler(cikti) if i.bicim is TC]
    assert len(ilet) == 1, "MPR seçicisinden gelen TC iletilmedi"
    y = dict(ilet[0].yuk)
    assert (y["ttl"], y["atlama"], y["kaynak"], y["mesaj_sira"]) == (4, 2, 9, 7)
    assert ilet[0].jitter_s == MAXJITTER_S, "§3.5 iletme titreşimi yok"
    tekrar = p.kontrol_alindi(_gozlem(0, 1.1), 2, "TC",
                              _tc(9, psn=1, msn=7, ansn=1, adresler=(8,), ttl=5),
                              True)
    assert not _istekler(tekrar), "aynı TC ikinci kez iletildi"
    baska = p.kontrol_alindi(_gozlem(0, 1.2), 2, "TC",
                             _tc(9, psn=2, msn=8, ansn=1, adresler=(8,), ttl=5),
                             True)
    assert not _istekler(baska), "MPR seçicisi olmayandan gelen TC iletildi"


def test_TC_SIMETRIK_OLMAYANDAN_islenmez_TEKRAR_kumesine_yazilmaz():
    """§9.5 adım 1 · §3.4.1 adım 1 — sonraki kopya işlenebilsin."""
    p = OLSR(0)
    _simetrik_yap(p, 2)
    p.kontrol_alindi(_gozlem(0, 1.0), 3, "TC",
                     _tc(9, psn=1, msn=7, ansn=1, adresler=(8,)), True)
    assert (8, 9) not in p._topoloji and (9, 7) not in p._tekrar
    p.kontrol_alindi(_gozlem(0, 1.1), 2, "TC",
                     _tc(9, psn=1, msn=7, ansn=1, adresler=(8,)), True)
    assert (8, 9) in p._topoloji, "simetrik komşudan gelen kopya işlenmedi"


# ==========================================================================
# §10 · YÖNLENDİRME TABLOSU
# ==========================================================================
def test_ROTA_TABLOSU_hat_topolojisinde_EN_KISA_YOL():
    """0 — 1 — 2 — 3 — 4 : 2-atlama kümesi + topoloji zinciri (h = 2'den)."""
    p = OLSR(0)
    _simetrik_yap(p, 1)
    p._iki[(1, 2)] = 100.0
    p._topoloji[(3, 2)] = (1, 100.0)
    p._topoloji[(4, 3)] = (1, 100.0)
    p._guncelle(1.0)
    assert p._rota == {1: (1, 1), 2: (1, 2), 3: (1, 3), 4: (1, 4)}


# ==========================================================================
# U2 · TEK BAĞ KOPTUĞUNDA — NEIGHB_HOLD_TIME dolunca tablo güncellenir
# ==========================================================================
def test_U2_bag_kopunca_tablo_guncellenir_ve_KOPMA_KURTARMA_ayni_anahtarda():
    """🔴 `06` §4.3 U2 + K-139'un beyan anlamı, gerçek `RotaDefteri` ile."""
    from sim2.olcum.rota_olaylari import RotaDefteri
    p = OLSR(0)
    defter = RotaDefteri()
    _simetrik_yap(p, 1)
    # 🔒 1'in simetrisi 1,5 s'de DOLACAK — baştan kurulur ve zamanın gerçekten
    # geçmesi beklenir. Böylece TEMBEL SÜZME de sınanır: protokol hiçbir olay
    # olmadan, en erken bitiş anı geçince kendiliğinden yeniden hesaplamalı.
    # (İlk yazımda bitiş hesaptan SONRA elle değiştiriliyordu; bu, gerçek
    # akışta hiç olmayan bir yolla "değişti" bayrağını atlıyordu.)
    p._bag[1].sym_bitis = 1.5
    p._iki[(1, 5)] = 100.0
    p._guncelle(1.0)
    assert p._rota[5] == (1, 2)
    beyan, _ = p._guncelle(2.0)
    assert 5 not in p._rota and 1 not in p._rota, "tablo güncellenmedi"
    assert [b.komsu for b in beyan if b.tip == "kopma"] == [1]
    for b in beyan:
        defter.beyan_isle(0, b, 2.0)
    # Başka bir komşu (2) hedef 5'e yol getirir.
    _simetrik_yap(p, 2, t=2.0)
    p._iki[(2, 5)] = 100.0
    beyan, _ = p._guncelle(2.8)
    assert p._rota[5] == (2, 2)
    assert [b.komsu for b in beyan if b.tip == "rota_kuruldu"] == [1]
    for b in beyan:
        defter.beyan_isle(0, b, 2.8)
    assert defter.delta_ler() == pytest.approx((0.8,))


# ==========================================================================
# §13 · BAĞ KATMANI BİLDİRİMİ — MAY, ama UYGULANIYOR (`04` K-147)
# ==========================================================================
def test_S13_bag_katmani_KOPTU_deyince_LOST_LINK_ve_KOPMA_histerezis_geri_acar():
    """🔴 §13'ün üç maddesi + §14.3 ile birlikte yaşaması.

    (2) `L_LOST_LINK_time = L_time = şimdi + NEIGHB_HOLD_TIME` · (1) bağ
    simetrik sayılmaz ve HELLO'da LOST_LINK ilan edilir · (3) §8.5 kaybı:
    rota düşer, kopma beyan edilir. Eski davranış (`return ()`) geri gelirse
    kapı yanar. Son iddia RFC'nin bileşimini belgeler: kalitesi eşiği aşan
    bir sonraki paket `L_LOST_LINK_time`ı geri alır.
    """
    p = OLSR(0)
    _simetrik_yap(p, 1)
    _simetrik_yap(p, 2)
    p._iki[(1, 5)] = 100.0
    p._guncelle(1.0)
    assert p._rota[5] == (1, 2)
    niyet = p.iletim_basarisiz(_gozlem(0, 2.0), 1, "veri")
    sinir = 2.0 + NEIGHB_HOLD_TIME_S
    assert p._bag[1].bitis == pytest.approx(sinir), "(2) L_time"
    assert p._hist[1].kayip_bitis == pytest.approx(sinir), "(2) L_LOST_LINK_time"
    assert not p._simetrik_mi(1, 2.0), "(1) bağ hâlâ simetrik"
    assert 1 not in p._rota and 5 not in p._rota, "(3) rota düşmedi"
    assert [b.komsu for b in niyet if getattr(b, "tip", None) == "kopma"] == [1]
    assert p._simetrik_mi(2, 2.0), "başka komşuya dokunuldu"
    y = dict(_istekler([p._hello_kur(2.1)])[0].yuk)
    blok, i = {}, 0
    for kod, boy in zip(y["blok_kodu"], y["blok_boyu"]):
        n = (boy - 4) // 4
        blok[kod] = y["komsu_adresi"][i:i + n]
        i += n
    assert 1 in blok.get(bag_kodu(NOT_NEIGH, LOST_LINK), ()), "(1) LOST_LINK ilanı"
    # §14.3 · kalitesi 0,95 olan bağda bir sonraki paket kaliteyi eşiğin
    # üstüne taşır → L_LOST_LINK_time = şimdi − 1, bağ geri açılır.
    p.kontrol_alindi(_gozlem(0, 2.5), 1, "HELLO",
                     _hello(1, 1, {bag_kodu(SYM_NEIGH, SYM_LINK): [0]}), True)
    assert p._simetrik_mi(1, 2.5)
    assert p.teshis(0)["bag_katmani_kopma"] == 1


# ==========================================================================
# U4 · ZAMANLAYICILAR — RFC'nin titreşim dağılımı
# ==========================================================================
def test_U4_HELLO_ve_TC_araligi_RFC_dagiliminda():
    """🔴 §3.5: *"Actual message interval = MESSAGE_INTERVAL − jitter"*.

    `Uyandirma(ARALIK − MAXJITTER, jitter=MAXJITTER)` → `ARALIK − U(0, MAXJ)`.
    Basit yol (sabit periyot + gecikme) HELLO aralığını 2,0 s tutardı; RFC
    1,75 s der ve fark kontrol yükünün %14'ü.
    """
    p = OLSR(0)
    ilk = _uyandirmalar(p.zamanlayici_doldu(_gozlem(0, 1.0), "bakim"))
    beklenen = {"hello": HELLO_INTERVAL_S, "tc": TC_INTERVAL_S}
    assert {u.etiket for u in ilk} == set(beklenen)
    for u in ilk + _uyandirmalar(p.uyandi(_gozlem(0, 3.0), "hello")):
        assert u.gecikme_s == pytest.approx(beklenen[u.etiket] - MAXJITTER_S)
        assert u.jitter_s == pytest.approx(MAXJITTER_S)
    cikti = p.uyandi(_gozlem(0, 3.0), "hello")
    hello = [i for i in _istekler(cikti) if i.bicim is HELLO]
    assert len(hello) == 1 and hello[0].jitter_s == 0.0, (
        "HELLO'ya ikinci bir gecikme eklendi — titreşim zaten aralıkta")


def test_kosum_beaconi_KAPALI():
    assert OLSR.kosum_beaconi is False


# ==========================================================================
# U3 · PROAKTİF YÜK — koşu süresiyle DOĞRUSAL ölçeklenir
# ==========================================================================
def test_U3_kontrol_yuku_PERIYODIK_ve_sure_ile_DOGRUSAL():
    """🔴 `06` §4.3 U3: *"OLSR yükü periyodik ve sabit"*.

    🔒 Ölçüt SONUÇ GÖRÜLMEDEN yazıldı: 120 s'lik koşunun kontrol çerçevesi,
    60 s'likin **[1,7 ; 2,3]** katı — periyodik bir yük süreyle doğrusal
    büyür, yani SABİT HIZDADIR. Ölçülen (19 Eylül): **2,200** — HELLO 2,02
    (tam periyodik), TC 2,26 (ilk dakikada yakınsama: TC'ler MPR seçicileri
    oluşunca başlıyor). §13'ten sonra (22 Eylül, K-147): **2,130**.

    🔴 İLK YAZIMDA BURADA ÇÜRÜMÜŞ BİR KARŞILAŞTIRMA VARDI: *"reaktif bir
    protokolün keşfi başta yığılır ve oran belirgin biçimde 2'nin altına
    düşerdi"*. ÖLÇÜLDÜ, düşmüyor: aynı dünyada AODV'nin oranı **1,854** —
    bu bandın İÇİNDE. Statik ağda bile AODV'nin keşfi susmuyor (boştaki
    komşu zaman aşımları ve MAC vazgeçmeleri sürekli RERR → yeniden keşif
    üretiyor). Yani bu kapı OLSR'ın KENDİ iddiasını — yük sabit hızda —
    sınar; OLSR'ı AODV'den AYIRT ETMEZ ve etmesi de gerekmiyor (`04` K-142).
    """
    cerceve = {}
    for bitis in (60.0, 120.0):
        kur = kurulum_yap(_konfig("statik-yok", 1000, bitis))
        kosu = Kosu(kur, OLSR)
        kosu.kostur()
        bicim = sonuc_satiri(kur, kosu.dugumler, "u3")[
            "teshis"]["kontrol_duzlemi"]["bicim"]["tum"]
        cerceve[bitis] = sum(b["cerceve"] for b in bicim.values())
    oran = cerceve[120.0] / cerceve[60.0]
    assert 1.7 <= oran <= 2.3, f"yük doğrusal ölçeklenmiyor: oran {oran:.3f}"


# ==========================================================================
# U1 · YAPI KAPISI — eşiksiz; sayısal yarısı kalibrasyonda
# ==========================================================================
def test_U1_YAPI_kapisi_teslim_COK_ATLAMALI_defter_kapali_kahin_asilmiyor():
    from kalibrasyon.kahin import EnGuvenilirKahin, KanalGrafigi

    kfg = _konfig("statik-yok", 1000, 60.0)
    kur = kurulum_yap(kfg)
    kosu = Kosu(kur, OLSR)
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "u1")
    m, kor = satir["metrikler"], satir["korunum"]
    assert kor["gecerli"], f"satır geçersiz: {kor}"
    assert kor["uretilen"] > 0 and m["pdr"] and m["pdr"] > 0.0
    assert m["aktarilan_paket"] > 0, "hiç çok atlamalı teslim yok"
    toplam = {}
    for d in satir["teshis"]["dugum"]:
        for k, v in d.items():
            toplam[k] = toplam.get(k, 0) + v
    assert toplam["mpr"] > 0 and toplam["tc_iletilen"] > 0, (
        f"MPR taşması çalışmıyor: {toplam}")
    kur_k = kurulum_yap(kfg)
    grafik = KanalGrafigi(kur_k)
    kosu_k = Kosu(kur_k, lambda i: EnGuvenilirKahin(i, grafik))
    kosu_k.kostur()
    kahin = sonuc_satiri(kur_k, kosu_k.dugumler, "u1")["metrikler"]["pdr"]
    assert m["pdr"] <= kahin, f"OLSR kâhini GEÇTİ: {m['pdr']} > {kahin}"


def test_korunum_ve_mutabakat_hareketli_kolda_kapaniyor():
    kur = kurulum_yap(_konfig("bagimsiz-yok", 1000, 30.0))
    kosu = Kosu(kur, OLSR)
    kosu.kostur()
    kor = sonuc_satiri(kur, kosu.dugumler, "k")["korunum"]
    assert kor["gecerli"], f"korunum/mutabakat kapanmadı: {kor}"
