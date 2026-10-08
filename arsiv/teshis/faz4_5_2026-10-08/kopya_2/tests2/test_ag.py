"""
ADIM 5 — `sim2/ag/` kapanış ölçütleri.

Yol haritası: *"Kayıpsız kanalda korunum tam. 10–15 akış × 4 pkt/s × 512 B."*

🔴 KORUNUM DENKLEMİ BU KATMANDA DOĞAR
=====================================
    üretilen = teslim + düşen + kuyrukta + uçuşta

Denklemin tutması *"hiçbir paket kaybolmuyor"* DEMEZ — bir geçişin kendisi
silinirse (paket "uçuşta" asılı kalırsa) eşitlik yine tutar. Onu yakalayan
şey koşu sonundaki boşalma kontrolüdür. Aşağıda ikisi de sınanır.
"""

from __future__ import annotations

import dataclasses
import pathlib
import sys

import pytest

KOK = pathlib.Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.ag.kuyruk import Kuyruk  # noqa: E402
from sim2.ag.paket import Paket, PaketSayaci  # noqa: E402
from sim2.ag.trafik import TrafikUreteci  # noqa: E402
from sim2.cekirdek.degismezler import DegismezHatasi  # noqa: E402
from sim2.cekirdek.korunum import (DUSME_SEBEPLERI, KorunumDefteri,  # noqa: E402
                                   KorunumHatasi)
from sim2.cekirdek.rng import Akislar  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402

K = Konfig(kol="test")


def _paket(kimlik=0, kaynak=1, hedef=2, dogum=0.0, ttl=32) -> Paket:
    return Paket(kimlik=kimlik, akis_kimligi=0, kaynak=kaynak, hedef=hedef,
                 dogum_s=dogum, boyut_bayt=512, ttl_kalan=ttl)


# ==========================================================================
# PAKET
# ==========================================================================

def test_paket_DONDURULMUS():
    p = _paket()
    with pytest.raises(dataclasses.FrozenInstanceError):
        p.ttl_kalan = 5  # type: ignore[misc]


def test_ttl_azaltmak_KIMLIGI_degistirmiyor():
    """🔒 "Aynı paket" sorusu her katmanda aynı cevabı vermeli."""
    p = _paket(kimlik=77, ttl=3)
    q = p.ttl_azalt()
    assert q.kimlik == p.kimlik == 77
    assert q.ttl_kalan == 2 and p.ttl_kalan == 3
    assert (q.akis_kimligi, q.kaynak, q.hedef, q.dogum_s) == \
           (p.akis_kimligi, p.kaynak, p.hedef, p.dogum_s)


def test_TTL_tukenince_azaltmak_REDDEDILIYOR():
    with pytest.raises(DegismezHatasi):
        _paket(ttl=0).ttl_azalt()
    assert _paket(ttl=0).ttl_tukendi_mi is True
    assert _paket(ttl=1).ttl_tukendi_mi is False


def test_gecikme_DOGUMDAN_olculuyor():
    """Kuyruğa giriş anından değil: kuyrukta beklemek gecikmenin parçasıdır
    ve onu dışarıda bırakmak yükü gizler."""
    p = _paket(dogum=10.0)
    assert p.gecikme_s(10.25) == pytest.approx(0.25)
    with pytest.raises(DegismezHatasi):
        p.gecikme_s(9.99)


def test_gecersiz_paket_REDDEDILIYOR():
    for ek in (dict(kaynak=3, hedef=3), dict(ttl=-1)):
        with pytest.raises(DegismezHatasi):
            _paket(**ek)
    with pytest.raises(DegismezHatasi):
        Paket(kimlik=0, akis_kimligi=0, kaynak=1, hedef=2, dogum_s=0.0,
              boyut_bayt=0, ttl_kalan=1)


def test_paket_sayaci_BENZERSIZ():
    s = PaketSayaci()
    kimlikler = [s.yeni() for _ in range(1000)]
    assert len(set(kimlikler)) == 1000
    assert s.uretilen_toplam == 1000


def test_SEMA_TAAHHUDU_uc_alan_yerinde():
    """🔴 Sonradan eklenemeyecek üç alan (`06` bölümü, sonuç şeması)."""
    adlar = {f.name for f in dataclasses.fields(Paket)}
    assert {"akis_kimligi", "dogum_s", "ttl_kalan"} <= adlar


# ==========================================================================
# KUYRUK
# ==========================================================================

def test_kuyruk_FIFO():
    k = Kuyruk(5)
    for n in range(3):
        assert k.ekle(_paket(kimlik=n)) is True
    assert len(k) == 3
    assert k.bak().kimlik == 0
    assert [k.al().kimlik for _ in range(3)] == [0, 1, 2]
    assert k.bos_mu


def test_kuyruk_DOLUNCA_reddediyor():
    """🔴 Sonsuz kuyruk gecikme metriğini anlamsızlaştırır: ağ ne kadar
    yüklenirse yüklensin paket düşmez ve PDR yapay olarak 1'e yakın kalır."""
    k = Kuyruk(3)
    assert all(k.ekle(_paket(kimlik=n)) for n in range(3))
    assert k.dolu_mu
    assert k.ekle(_paket(kimlik=99)) is False
    assert len(k) == 3
    assert [p.kimlik for p in k.tumu()] == [0, 1, 2], "reddedilen içeri girmemeli"


def test_bos_kuyruktan_almak_DEGISMEZ_ihlali():
    k = Kuyruk(2)
    with pytest.raises(DegismezHatasi):
        k.al()
    with pytest.raises(DegismezHatasi):
        k.bak()


def test_sifir_kapasite_REDDEDILIYOR():
    with pytest.raises(DegismezHatasi):
        Kuyruk(0)


# ==========================================================================
# TRAFİK
# ==========================================================================

def test_akis_sayisi_ve_AYRIK_dugumler():
    """Aynı düğüm iki akışın kaynağı olsaydı, ölçülen şey protokolün değil
    o düğümün darboğazının farkı olurdu."""
    t = TrafikUreteci(K, Akislar(1))
    assert len(t.akislar) == K.akis_sayisi == 10
    dugumler = [n for a in t.akislar for n in (a.kaynak, a.hedef)]
    assert len(set(dugumler)) == len(dugumler) == 2 * K.akis_sayisi
    assert all(a.kaynak != a.hedef for a in t.akislar)
    assert all(0 <= n < K.dugum_sayisi for n in dugumler)


def test_uretim_hizi_ILAN_EDILENE_esit():
    t = TrafikUreteci(K, Akislar(1))
    beklenen = K.akis_sayisi * K.akis_paket_hizi_hz
    assert t.sunulan_hiz_hz() == pytest.approx(beklenen, rel=0.02)
    assert K.sunulan_paket_hizi_hz == beklenen == 40.0


def test_dogum_OLCUM_BITISINDE_duruyor():
    t = TrafikUreteci(K, Akislar(1))
    assert all(d.t_s < K.olcum_bitis_s for d in t.cizelge)
    assert all(d.t_s >= 0.0 for d in t.cizelge)


def test_cizelge_SIRALI():
    t = TrafikUreteci(K, Akislar(1))
    anlar = [(d.t_s, d.akis_kimligi) for d in t.cizelge]
    assert anlar == sorted(anlar)


def test_AKIS_ICI_sira_korunuyor():
    """🔒 IPDV'nin ön koşulu: bir akışın paketleri doğum sırasını korumalı.

    Titreşim periyodun yarısını aşsaydı doğumlar akış içinde sıra değiştirir
    ve ölçülen titreşim trafiğin değil, çizelgenin yapaylığı olurdu.
    """
    t = TrafikUreteci(K, Akislar(1))
    for akis in t.akislar:
        anlar = [d.t_s for d in t.cizelge if d.akis_kimligi == akis.kimlik]
        assert anlar == sorted(anlar)
        assert len(anlar) > 100


def test_asiri_titresim_REDDEDILIYOR():
    with pytest.raises(DegismezHatasi):
        TrafikUreteci(Konfig(kol="t", cbr_titresim_s=0.2), Akislar(1))


def test_TRAFIK_protokolden_BAGIMSIZ():
    """🔒 Aynı tohumda her protokol birebir aynı paketleri, aynı anlarda görür.

    Koşu sırasında çekim yapılsaydı, çekim sayısı protokole göre değişir ve
    iki kol FARKLI TRAFİK görürdü — 30 tohum bunu kurtarmaz.
    """
    a = Akislar(7)
    ilk = TrafikUreteci(K, a)
    b = Akislar(7)
    # "öteki protokol" başka akışlardan bolca çekiyor
    for _ in range(5000):
        b["protokol_kesif"].random()
        b["mac_geri_cekilme"].random()
    ikinci = TrafikUreteci(K, b)
    assert ilk.akislar == ikinci.akislar
    assert ilk.cizelge == ikinci.cizelge


def test_farkli_tohum_farkli_trafik():
    assert (TrafikUreteci(K, Akislar(1)).akislar
            != TrafikUreteci(K, Akislar(2)).akislar)


def test_paket_kur_akistan_dogru_alanlari_aliyor():
    t = TrafikUreteci(K, Akislar(1))
    sayac = PaketSayaci()
    d = t.cizelge[0]
    p = t.paket_kur(d, sayac)
    akis = t.akis(d.akis_kimligi)
    assert (p.kaynak, p.hedef, p.akis_kimligi) == (akis.kaynak, akis.hedef,
                                                   akis.kimlik)
    assert p.dogum_s == d.t_s
    assert p.boyut_bayt == K.paket_bayt == 512
    assert p.ttl_kalan == K.ttl_baslangic


# --------------------------------------------------------------------------
# Y4 · YERE TOPLAMA — `v2/07` §06.2 · §18 Y4
# --------------------------------------------------------------------------
KY = Konfig(kol="t", trafik_deseni="yere_toplama")


def test_Y4_yere_toplama_HER_DUGUMDEN_GECIDE_telemetri_ve_KOMUT():
    t = TrafikUreteci(KY, Akislar(1))
    gecit = KY.gecit
    tele = [a for a in t.akislar if a.hedef == gecit]
    komut = [a for a in t.akislar if a.kaynak == gecit]
    assert sorted(a.kaynak for a in tele) == [
        i for i in range(KY.dugum_sayisi) if i != gecit]
    assert len(komut) == KY.komut_akis_sayisi
    hedefler = {a.hedef for a in komut}
    assert len(hedefler) == len(komut) and gecit not in hedefler
    assert len(t.akislar) == len(tele) + len(komut)
    assert [a.kimlik for a in t.akislar] == list(range(len(t.akislar)))


def test_Y4_yere_toplama_URETIM_HIZI_akis_basina_ILAN_EDILENE_esit():
    t = TrafikUreteci(KY, Akislar(1))
    assert KY.sunulan_paket_hizi_hz == pytest.approx(40.0)
    assert t.sunulan_hiz_hz() == pytest.approx(KY.sunulan_paket_hizi_hz,
                                               rel=0.02)
    for akis in t.akislar:
        n = sum(1 for d in t.cizelge if d.akis_kimligi == akis.kimlik)
        hiz = (KY.komut_paket_hizi_hz if akis.kaynak == KY.gecit
               else KY.telemetri_paket_hizi_hz)
        assert n == pytest.approx(hiz * KY.olcum_bitis_s, abs=2)


def test_K157_kaynak_sira_KAYNAK_BASINA_ardisik_ve_paketi_TANIR():
    """Her kaynağın paketleri 0, 1, 2, … sırası alır; `(kaynak, kaynak_sira)`
    bütün koşuda eşsizdir. Yere toplamada geçit birden çok komut akışının
    kaynağıdır ve TEK sayaç kullanır — sayaç akış başına olsaydı geçitin iki
    komut paketi aynı kimliği taşırdı."""
    for konfig in (K, KY):
        t = TrafikUreteci(konfig, Akislar(1))
        sayac = PaketSayaci()
        paketler = [t.paket_kur(d, sayac) for d in t.cizelge]
        kaynaklar = {p.kaynak for p in paketler}
        for kaynak in kaynaklar:
            siralar = [p.kaynak_sira for p in paketler if p.kaynak == kaynak]
            assert siralar == list(range(len(siralar)))
        assert len({(p.kaynak, p.kaynak_sira) for p in paketler}) == len(paketler)
    gecit_akislari = {a.kimlik for a in t.akislar if a.kaynak == KY.gecit}
    assert len(gecit_akislari) >= 2


def test_K157_kaynak_sira_TTL_azalinca_KORUNUR():
    p = _paket(1, 0, 2)
    p = dataclasses.replace(p, kaynak_sira=7)
    assert p.ttl_azalt().kaynak_sira == 7
    with pytest.raises(DegismezHatasi):
        dataclasses.replace(p, kaynak_sira=-1)


def test_Y4_varsayilan_ESLER_ARASI_ve_GECIT_YOK():
    assert K.trafik_deseni == "esler_arasi" and K.gecit is None
    assert not K.yere_toplama


# ==========================================================================
# 🔒 KAPANIŞ ÖLÇÜTÜ — KORUNUM
# ==========================================================================

def _kayipsiz_kosum(konfig: Konfig, tohum: int = 1):
    """İdeal aktarıcı: her paket doğar, kuyruğa girer, hedefine teslim edilir.

    ⚠️ MAC ve protokol henüz yok; bu koşum onların YERİNE geçmez. Ölçtüğü tek
    şey, `ag/` katmanının kendi geçişlerinin defteri tutup tutmadığıdır.
    """
    trafik = TrafikUreteci(konfig, Akislar(tohum))
    defter = KorunumDefteri()
    sayac = PaketSayaci()
    kuyruklar = {n: Kuyruk(konfig.kuyruk_kapasitesi)
                 for n in range(konfig.dugum_sayisi)}
    teslim: list[tuple[Paket, float]] = []

    for dogum in trafik.cizelge:
        paket = trafik.paket_kur(dogum, sayac)
        if kuyruklar[paket.kaynak].ekle(paket):
            defter.uret()
        else:
            defter.uret()
            defter.dus("kuyruk_tasmasi", nereden="kuyruk")
        # ideal aktarım: kuyruk hemen boşalır
        kuyruk = kuyruklar[paket.kaynak]
        while not kuyruk.bos_mu:
            p = kuyruk.al()
            defter.kuyruktan_al()
            defter.teslim_et()
            teslim.append((p, dogum.t_s))
    return defter, teslim, kuyruklar


def test_KORUNUM_kayipsiz_kanalda_TAM():
    """🔒 Adım 5'in kapanış ölçütü."""
    defter, teslim, kuyruklar = _kayipsiz_kosum(K)
    rapor = defter.kontrol()
    assert rapor["korunum_tamam"] is True, rapor
    assert rapor["fark"] == 0
    assert rapor["uretilen"] == len(teslim)
    assert rapor["dusen_toplam"] == 0
    # 🔒 Boşalma kontrolü: denklem tutuyor ama BOŞALDI MI?
    assert rapor["kuyrukta"] == 0 and rapor["ucusta"] == 0
    assert all(k.bos_mu for k in kuyruklar.values())
    # 🔒 Ve defterin MODELİ gerçekle uyuşuyor mu?
    m = defter.mutabakat(
        kuyrukta_gercek=sum(len(k) for k in kuyruklar.values()),
        ucusta_gercek=0)
    assert m["mutabakat_tamam"] is True, m


def test_KORUNUM_bes_dusme_sebebiyle_de_TAM():
    """Denklem yalnız kayıpsız hâlde değil, her düşme sebebiyle de tutmalı."""
    defter = KorunumDefteri()
    defter.uret(100)
    defter.kuyruktan_al(60)
    defter.teslim_et(20)
    defter.ucustan_kuyruga(10)
    # beş sebebin beşi de kullanılır
    defter.dus("kuyruk_tasmasi", nereden="kuyruk", adet=3)
    defter.dus("ttl", nereden="ucus", adet=4)
    defter.dus("iletim_basarisiz", nereden="ucus", adet=5)
    defter.dus("hedef_yok", nereden="kuyruk", adet=6)
    defter.dus("rota_gecersiz", nereden="kuyruk", adet=7)
    rapor = defter.kontrol()
    assert rapor["korunum_tamam"] is True, rapor
    assert rapor["dusen_toplam"] == 25
    assert set(rapor["dusen"]) == set(DUSME_SEBEPLERI)


def test_KORUNUM_DENKLEMININ_KOR_NOKTASI():
    """🔴 BU TEST BİR ŞEY BULDU ve `korunum.py`yi değiştirdi.

    Amacı denklemi kırmaktı: dolu kuyruk paketi reddediyor, çağıran
    `dus(...)` yapmayı unutuyor. Beklenti "denklem kırılır" idi.

    ÖLÇÜLEN: denklem **TUTUYOR**. `uret()` hem `uretilen`i hem `kuyrukta`yı
    artırdığı için defter paketin kuyrukta olduğunu sanıyor; gerçek kuyruk
    onu reddetmiş olsa bile `5 = 0 + 0 + 5 + 0`. Paket sessizce yok oldu ve
    korunum denklemi bunu GÖRMEDİ.

    Bu bir hata değil, denklemin tanımının sınırı: defterin kendi
    geçişlerinin tutarlılığını ölçer, gerçeği doğru modelleyip modellemediğini
    değil. Onu ölçen şey `mutabakat()` — bu testin doğurduğu metot.
    """
    defter = KorunumDefteri()
    kuyruk = Kuyruk(2)
    for n in range(5):
        defter.uret()
        if not kuyruk.ekle(_paket(kimlik=n)):
            pass                       # 🔴 KASITLI HATA: düşürülmüyor

    # 1) Denklem tutuyor — kör nokta budur.
    assert defter.denklem_tutuyor_mu() is True
    assert defter.kontrol()["fark"] == 0

    # 2) Mutabakat kırılıyor — kör noktayı gören kontrol.
    m = defter.mutabakat(kuyrukta_gercek=len(kuyruk), ucusta_gercek=0)
    assert m["mutabakat_tamam"] is False
    assert m["kuyruk_farki"] == 3, "defter 3 fazla paket olduğunu sanıyor"


def test_MUTABAKAT_dogru_kullanimda_tutuyor():
    defter = KorunumDefteri()
    kuyruk = Kuyruk(2)
    for n in range(5):
        defter.uret()
        if not kuyruk.ekle(_paket(kimlik=n)):
            defter.dus("kuyruk_tasmasi", nereden="kuyruk")
    assert defter.denklem_tutuyor_mu() is True
    m = defter.mutabakat(kuyrukta_gercek=len(kuyruk), ucusta_gercek=0)
    assert m["mutabakat_tamam"] is True
    assert m["kuyruk_farki"] == 0 and m["ucus_farki"] == 0


def test_negatif_gecis_ANINDA_patliyor():
    """Sessiz paket kaybı bu alanın en zor bulunan hata sınıfıdır; tek
    yapısal panzehiri geçişin anında patlamasıdır."""
    defter = KorunumDefteri()
    defter.uret(2)
    defter.kuyruktan_al(2)
    with pytest.raises(KorunumHatasi):
        defter.teslim_et(3)


def test_bilinmeyen_dusme_sebebi_REDDEDILIYOR():
    defter = KorunumDefteri()
    defter.uret(1)
    with pytest.raises(KorunumHatasi):
        defter.dus("kedi_yedi", nereden="kuyruk")
    with pytest.raises(KorunumHatasi):
        defter.dus("ttl", nereden="uzay")


def test_TASMA_kuyruk_kucukse_gercekten_oluyor():
    """Kapasite küçültülünce taşma ölçülebilir olmalı — yoksa kuyruğun
    sonluluğu hiçbir zaman sınanmamış demektir."""
    kucuk = Konfig(kol="t", kuyruk_kapasitesi=1)
    kuyruk = Kuyruk(kucuk.kuyruk_kapasitesi)
    kabul = sum(kuyruk.ekle(_paket(kimlik=n)) for n in range(10))
    assert kabul == 1


def test_pencerede_uretilen_TAM_KOSUDAN_az():
    """Ölçüm penceresi ile tüm koşu AYRI defterlerdir."""
    t = TrafikUreteci(K, Akislar(1))
    assert 0 < t.penceredeki_dogum() < t.toplam_dogum
    bas, bitis = K.olcum_penceresi
    beklenen = sum(1 for d in t.cizelge if bas <= d.t_s < bitis)
    assert t.penceredeki_dogum() == beklenen
