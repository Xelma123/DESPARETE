"""
Kontrol düzlemi — P1–P8 doğrulama kapıları. K-112, `v2/13-KONTROL-DUZLEMI.md` §09.

🔒 KAPILAR KONTROL KODUNUN KENDİ SAYAÇLARINA GÜVENMEZ
=====================================================
Her kapı kanıtını mekanizmanın DIŞINDAN toplar: havaya çıkan her iletim
`Ortam.ekle`de, her alım kararı `AliciZinciri.cerceve_bitti`de, her olay
`OlayKuyrugu.ekle`de gözlenir. Kontrol defterinin söylediği, bu bağımsız
gözlemle birebir eşleşmek zorundadır — "ölçüm aletine, ölçtüğü şeyden az
güven" (K-109).

🔒 HİÇBİR KAPI BOŞ GEÇMEZ: her biri kanıt sayısının sıfırdan büyük olduğunu
da sınar (K-110'un `aktarilan_paket = 0` dersi).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parent.parent
for _y in (KOK, KOK / "tests2"):
    if str(_y) not in sys.path:
        sys.path.insert(0, str(_y))

from sim2.cekirdek.degismezler import DegismezHatasi  # noqa: E402
from sim2.cekirdek.olaylar import OlayKuyrugu  # noqa: E402
from sim2.gozlem.karar import Karar  # noqa: E402
from sim2.gozlem.kontrol import (KontrolHatasi, KontrolIstegi,  # noqa: E402
                                 MesajBicimi, Uyandirma)
from sim2.gozlem.kontrol import KONTROL_KANCALARI  # noqa: E402
from sim2.gozlem.protokol import KontrolluProtokol, Protokol  # noqa: E402
from sim2.gozlem.pencere import (IZINLI_GOZLEM_ALANLARI,  # noqa: E402
                                 IZINLI_KOMSU_ALANLARI, IZINLI_PAKET_ALANLARI,
                                 YASAK_TIPLER)
from sim2.kanal.cerceve import (cerceve_kur,  # noqa: E402
                                kontrol_kapsulleme_bayt)
from sim2.kanal.girisim import Ortam  # noqa: E402
from sim2.kosum import kontrol as KM  # noqa: E402
from sim2.kosum.kontrol_durum import (DEFTER_ALANLARI,  # noqa: E402
                                      KontrolDuzlemiHatasi,
                                      UyandirmaTavaniAsildi)
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.kosum.sonuc import sonuc_satiri  # noqa: E402
from sim2.mac.alici import AliciZinciri  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402
from test_kosum import _konfig  # noqa: E402

# ==========================================================================
# SINAV PROTOKOLÜ — taban çizgisi DEĞİL, mekanizmanın koşum aleti
# ==========================================================================
HELLO = MesajBicimi("SINAV_HELLO", (("tip", 8), ("kaynak", 8), ("sira", 32)))
ISTEK = MesajBicimi("SINAV_ISTEK", (("tip", 8), ("kaynak", 8), ("sira", 32)),
                    tekrarli=(("yol", 8),))
CEVAP = MesajBicimi("SINAV_CEVAP", (("tip", 8), ("kaynak", 8), ("sira", 32)))
GECIKME_S = 0.05


def yeni_kayit() -> dict:
    return {a: [] for a in ("periyodik", "dinamik_istek", "dinamik_ates",
                            "gonderilen", "teslim", "iletim_basarisiz")}


class SinavProtokolu:
    """Veriyi kimliği yakın komşuya iletir; kontrol düzleminin HER yolunu açar:
    periyodik yayın · karardan unicast istek + dinamik uyandırma · alımdan
    unicast cevap."""

    ad = "kontrol_sinav"
    __slots__ = ("kimlik", "kayit", "sira", "karar_no")

    def __init__(self, kimlik: int, kayit: dict) -> None:
        self.kimlik, self.kayit, self.sira, self.karar_no = kimlik, kayit, 0, 0

    def _mesaj(self, hedef, bicim, **ek):
        self.sira += 1
        yuk = {"tip": {"SINAV_HELLO": 1, "SINAV_ISTEK": 2,
                       "SINAV_CEVAP": 3}[bicim.ad],
               "kaynak": self.kimlik, "sira": self.sira, **ek}
        self.kayit["gonderilen"].append((self.kimlik, bicim.ad, self.sira,
                                         hedef))
        return KontrolIstegi.kur(hedef, bicim, yuk)

    def sonraki_atlama(self, gozlem):
        if gozlem.paket is None or not gozlem.komsular:
            return Karar()
        hedef = gozlem.paket.hedef
        adaylar = [k.dugum for k in gozlem.komsular]
        sonraki = hedef if hedef in adaylar else min(
            adaylar, key=lambda n: (abs(n - hedef), n))
        self.karar_no += 1
        if self.karar_no % 7:
            return Karar(sonraki=sonraki)
        self.kayit["dinamik_istek"].append((self.kimlik, "zaman_asimi",
                                            float(gozlem.saat_s), GECIKME_S))
        return Karar(sonraki=sonraki, niyetler=(
            self._mesaj(sonraki, ISTEK, yol=(self.kimlik, sonraki)),
            Uyandirma(GECIKME_S, "zaman_asimi")))

    def beacon_yuku(self, gozlem):
        return {}

    def beacon_alindi(self, gozlem, komsu, yuk):
        return None

    def teshis(self, dugum):
        return {}

    def zamanlayicilar(self):
        return {"hello": 1.0, "sessiz": 2.5}

    def zamanlayici_doldu(self, gozlem, etiket):
        self.kayit["periyodik"].append(
            (gozlem.dugum, etiket, float(gozlem.saat_s)))
        if etiket != "hello":
            return ()
        return (self._mesaj(None, HELLO),)

    def uyandi(self, gozlem, etiket):
        self.kayit["dinamik_ates"].append(
            (gozlem.dugum, etiket, float(gozlem.saat_s)))
        return ()

    def kontrol_alindi(self, gozlem, gonderen, bicim, yuk, yayin):
        y = dict(yuk)
        self.kayit["teslim"].append(
            (gozlem.dugum, gonderen, bicim, y["sira"], yayin))
        if bicim == "SINAV_ISTEK":
            return (self._mesaj(gonderen, CEVAP),)
        return ()

    def iletim_basarisiz(self, gozlem, hedef, tur):
        """Y3 · R3 — MAC vazgeçti. Sınav protokolü yalnız KAYDEDER."""
        self.kayit["iletim_basarisiz"].append(
            (gozlem.dugum, hedef, tur, float(gozlem.saat_s)))
        return ()


class VeriIkizi:
    """SinavProtokolu'nun veri kararlarının AYNISI, kontrol kancası YOK."""

    ad = "veri_ikizi"
    __slots__ = ("kimlik",)

    def __init__(self, kimlik: int) -> None:
        self.kimlik = kimlik

    def sonraki_atlama(self, gozlem):
        if gozlem.paket is None or not gozlem.komsular:
            return Karar()
        hedef = gozlem.paket.hedef
        adaylar = [k.dugum for k in gozlem.komsular]
        return Karar(sonraki=hedef if hedef in adaylar else min(
            adaylar, key=lambda n: (abs(n - hedef), n)))

    def beacon_yuku(self, gozlem):
        return {}

    def beacon_alindi(self, gozlem, komsu, yuk):
        return None

    def teshis(self, dugum):
        return {}


# ==========================================================================
# BAĞIMSIZ GÖZLEM — mekanizmanın dışından
# ==========================================================================
class Casus:
    def __init__(self, monkeypatch):
        self.iletimler: list = []            # (gönderen, tip, bayt, süre, baş)
        self.alim: dict = {}                 # (alıcı, id(iletim)) -> başarılı
        self.kontrol_alimlari: list = []     # (alıcı, gönderen, istek, no, başarılı)
        self.olaylar: list = []              # (zaman, geri_çağrı, args)
        o_ekle, a_bitti = Ortam.ekle, AliciZinciri.cerceve_bitti
        k_bitti, q_ekle = Kosu._cerceve_bitti, OlayKuyrugu.ekle
        casus = self

        def ortam_ekle(self, iletim):
            casus.iletimler.append((iletim.gonderen, iletim.cerceve.tip,
                                    iletim.cerceve.bayt, iletim.cerceve.sure_s,
                                    iletim.baslangic_s))
            return o_ekle(self, iletim)

        def alici_bitti(self, iletim, t_s):
            s = a_bitti(self, iletim, t_s)
            if s is not None:
                casus.alim[(self.dugum, id(iletim))] = s.basarili
            return s

        def kosu_bitti(self, n, iletim, yuk):
            # 🔴 `id()` yeniden kullanılabilir: önceki bir iletimin kaydı bu
            # alımda `cerceve_bitti` hiç sonuç döndürmezse (önbelgede reddedildi)
            # BAYAT bir "başarılı" okunabilirdi. Önce silinir.
            casus.alim.pop((n, id(iletim)), None)
            k_bitti(self, n, iletim, yuk)
            if yuk[0] == "kontrol":
                istek, no = yuk[1]
                casus.kontrol_alimlari.append(
                    (n, iletim.gonderen, istek, no,
                     casus.alim.get((n, id(iletim)), False)))

        def kuyruk_ekle(self, zaman, geri_cagri, *args):
            casus.olaylar.append((zaman, geri_cagri, args))
            return q_ekle(self, zaman, geri_cagri, *args)

        monkeypatch.setattr(Ortam, "ekle", ortam_ekle)
        monkeypatch.setattr(AliciZinciri, "cerceve_bitti", alici_bitti)
        monkeypatch.setattr(Kosu, "_cerceve_bitti", kosu_bitti)
        monkeypatch.setattr(OlayKuyrugu, "ekle", kuyruk_ekle)


def _kos(senaryo="statik-yok", tohum=1000, bitis=30.0, fabrika=None, **ek):
    kfg = _konfig(senaryo, tohum, bitis, **ek)
    kur = kurulum_yap(kfg)
    kayit = yeni_kayit()
    kosu = Kosu(kur, fabrika or (lambda i: SinavProtokolu(i, kayit)))
    kosu.kostur()
    return kur, kosu, kayit


KAYIPLI = dict(senaryo="statik-surekli", karistirici_baslangic_s=2.0)


# ==========================================================================
# P1 · BEDEL — tek kaynak, gerçek hava süresi, çift fatura yok
# ==========================================================================
def test_P1_boyut_RFC_alanlarindan_ve_kapsulleme_TEK_KAYNAKTAN():
    k = Konfig(kol="t")
    y = {"tip": 2, "kaynak": 3, "sira": 9, "yol": (1, 2, 3)}
    i = KontrolIstegi.kur(4, ISTEK, y)
    assert i.mesaj_bayt == (8 + 8 + 32 + 3 * 8 + 7) // 8 == 9
    c = cerceve_kur(k, "kontrol", mesaj_bayt=i.mesaj_bayt)
    assert c.bayt == 9 + kontrol_kapsulleme_bayt() == 9 + 64
    assert c.sure_s == pytest.approx(k.onbelge_s + c.bayt * 8 / k.bit_hizi_bps)
    for tip, beklenen in (("veri", k.paket_bayt), ("onay", k.onay_bayt),
                          ("beacon", k.beacon_bayt)):
        assert cerceve_kur(k, tip).bayt == beklenen, "mevcut çerçeve DEĞİŞTİ"
    with pytest.raises(DegismezHatasi):
        cerceve_kur(k, "kontrol", bayt=40)
    with pytest.raises(DegismezHatasi):
        cerceve_kur(k, "veri", mesaj_bayt=4)


@pytest.mark.parametrize("yuk", [
    {"tip": 256, "kaynak": 1, "sira": 1, "yol": ()},       # 8 bite sığmıyor
    {"tip": 1, "kaynak": 1, "sira": 1},                     # eksik alan
    {"tip": 1, "kaynak": 1, "sira": 1, "yol": (), "x": 1},  # fazla alan
    {"tip": 1.5, "kaynak": 1, "sira": 1, "yol": ()},        # 8 bitte float
    {"tip": 1, "kaynak": 1, "sira": -1, "yol": ()},         # negatif
])
def test_P1_sigmayan_deger_KACAK_TASIYAMAZ(yuk):
    with pytest.raises(KontrolHatasi):
        KontrolIstegi.kur(None, ISTEK, yuk)


def test_P1_sayac_HAVAYA_CIKANLA_birebir_cift_fatura_yok(monkeypatch):
    casus = Casus(monkeypatch)
    kur, kosu, _ = _kos()
    s = kur.sayaclar.disa_ver()
    kontrol_tipleri = ("beacon", "onay", "kontrol")
    kb = sum(b for _, t, b, _, _ in casus.iletimler if t in kontrol_tipleri)
    ka = sum(d for _, t, _, d, _ in casus.iletimler if t in kontrol_tipleri)
    kc = sum(1 for _, t, _, _, _ in casus.iletimler if t in kontrol_tipleri)
    n_kontrol = sum(1 for _, t, _, _, _ in casus.iletimler if t == "kontrol")
    assert n_kontrol > 0, "boş geçmemeli — kontrol çerçevesi havaya çıkmalı"
    assert s["kontrol_bayt"] == kb
    assert s["kontrol_airtime_s"] == pytest.approx(ka, rel=0, abs=1e-12)
    assert s["kontrol_cerceve"] == kc
    assert s["veri_bayt"] == sum(b for _, t, b, _, _ in casus.iletimler
                                 if t == "veri")
    defter = sonuc_satiri(kur, kosu.dugumler, "k")["teshis"]["kontrol_duzlemi"]
    assert defter["defter"]["iletim"] == n_kontrol


# ==========================================================================
# P2 · MAC ORTAKLIĞI — aynı DCF, aynı `gonder`, unicast onay + yeniden deneme
# ==========================================================================
def test_P2_kontrol_VERIYLE_AYNI_MACI_paylasiyor():
    """Aynı tohum, aynı veri kararları: kontrol trafiği eklenince veri
    zamanlaması DEĞİŞMELİ — ayrı bir kanal olsaydı değişmezdi."""
    kur_k, _, kayit = _kos()
    kur_v, _, _ = _kos(fabrika=lambda i: VeriIkizi(i))
    assert kayit["gonderilen"], "boş geçmemeli"
    sk, sv = kur_k.sayaclar.disa_ver(), kur_v.sayaclar.disa_ver()
    assert (sk["mac_deneme"], sk["teslim_paket"], sk["alim_red_mesgul"]) != \
           (sv["mac_deneme"], sv["teslim_paket"], sv["alim_red_mesgul"])


def test_P2_unicast_ONAYLANIR_yayin_ONAYLANMAZ(monkeypatch):
    casus = Casus(monkeypatch)
    kur, kosu, _ = _kos(**KAYIPLI)
    d = sonuc_satiri(kur, kosu.dugumler, "k")["teshis"]["kontrol_duzlemi"]["defter"]
    konay = [a for _, cb, a in casus.olaylar
             if cb.__name__ == "gonder" and a and a[-1][0] == "konay"]
    assert d["teslim_yayin"] > 0 and d["teslim_unicast"] > 0, "boş geçmemeli"
    assert len(konay) == d["teslim_unicast"] + d["tekrar_bastirilan"], \
        "onay yalnız unicast teslim/tekrar için üretilmeli"
    sonuc = (d["yayin_gonderilen"] + d["unicast_onaylanan"]
             + d["unicast_vazgecilen"])
    assert d["iletim"] > sonuc, "kayıplı kolda YENİDEN DENEME gözlenmeli"


# ==========================================================================
# P3 · TESLİM SEMANTİĞİ — yalnız başarıda; yayında alıcı başına; unicast hedefte
# ==========================================================================
def test_P3_teslim_FIZIKSEL_BASARIYLA_birebir(monkeypatch):
    casus = Casus(monkeypatch)
    kur, kosu, kayit = _kos(**KAYIPLI)
    beklenen, gorulen, basarisiz, baskasina = [], set(), 0, 0
    for n, g, istek, no, basarili in casus.kontrol_alimlari:
        if not basarili:
            basarisiz += 1
            continue
        if not istek.yayin_mi and istek.hedef != n:
            baskasina += 1
            continue
        if not istek.yayin_mi:
            if (n, g, no) in gorulen:
                continue
            gorulen.add((n, g, no))
        y = dict(istek.yuk)
        beklenen.append((n, g, istek.bicim.ad, y["sira"], istek.yayin_mi))
    assert basarisiz > 0 and beklenen, "boş geçmemeli — kayıp VE teslim olmalı"
    assert sorted(kayit["teslim"]) == sorted(beklenen)
    d = sonuc_satiri(kur, kosu.dugumler, "k")["teshis"]["kontrol_duzlemi"]["defter"]
    assert d["baskasina_adresli"] == baskasina
    assert all(t[0] != t[1] for t in kayit["teslim"]), "kendi çerçevesi teslim"


# ==========================================================================
# P4 · ZAMANLAYICILAR — iki AYRI mekanizma
# ==========================================================================
def test_P4_periyodik_ve_dinamik_AYRI_ve_DOGRU_ANLARDA(monkeypatch):
    casus = Casus(monkeypatch)
    kur, kosu, kayit = _kos()
    bitis = kur.konfig.kosu_bitis_s
    per = [(z, a) for z, cb, a in casus.olaylar if cb is KM._zamanlayici_ates]
    assert per and kayit["dinamik_istek"], "boş geçmemeli"
    zincir: dict = {}
    for z, (_k, n, etiket, periyot) in per:
        zincir.setdefault((n, etiket), []).append((z, periyot))
    for (n, etiket), anlar in zincir.items():
        faz, periyot = anlar[0]
        assert 0.0 <= faz < periyot
        for (a, _), (b, _) in zip(anlar, anlar[1:]):
            assert b == a + periyot, "periyodik zincir kaydı"
    ates = [x for x in kayit["periyodik"]]
    assert len(ates) == sum(1 for z, _ in per if z <= bitis)
    assert {e for _, e, _ in kayit["periyodik"]} == {"hello", "sessiz"}
    assert {e for _, e, _ in kayit["dinamik_ates"]} == {"zaman_asimi"}
    d = sonuc_satiri(kur, kosu.dugumler, "k")
    kd = d["teshis"]["kontrol_duzlemi"]["defter"]
    assert kd["periyodik_ates"] == len(kayit["periyodik"])
    assert kd["dinamik_istenen"] == len(kayit["dinamik_istek"])
    assert kd["dinamik_ates"] == len(kayit["dinamik_ates"])
    istekler: dict = {}
    for n, e, saat, g in kayit["dinamik_istek"]:
        istekler.setdefault(n, []).append(saat + g)
    for n, e, saat in kayit["dinamik_ates"]:
        assert any(abs(saat - x) <= 1e-5 for x in istekler[n]), \
            "uyandırma istenen anda ateşlenmedi"


@pytest.mark.parametrize("ilan", [{"hello": 1e-6}, {"": 1.0},
                                  {"x": float("inf")}, ["hello"]])
def test_P4_gecersiz_periyodik_ilan_REDDEDILIR(ilan):
    class Bozuk(SinavProtokolu):
        __slots__ = ()

        def zamanlayicilar(self):
            return ilan
    with pytest.raises(KontrolDuzlemiHatasi):
        _kos(bitis=5.0, fabrika=lambda i: Bozuk(i, yeni_kayit()))


def test_P4_slottan_kisa_uyandirma_DURDURUR():
    class Kisa(SinavProtokolu):
        __slots__ = ()

        def zamanlayici_doldu(self, gozlem, etiket):
            return (Uyandirma(1e-7, "kisa"),)
    with pytest.raises(KontrolDuzlemiHatasi):
        _kos(bitis=5.0, fabrika=lambda i: Kisa(i, yeni_kayit()))
    with pytest.raises(DegismezHatasi):
        Uyandirma(0.0, "sifir")


# ==========================================================================
# P5 · UYANDIRMA TAVANI — aşımda deterministik FAIL, sessiz düşürme yok
# ==========================================================================
class Tasan(SinavProtokolu):
    __slots__ = ()

    def zamanlayici_doldu(self, gozlem, etiket):
        return tuple(Uyandirma(100.0, "birikim")
                     for _ in range(KM.BEKLEYEN_UYANDIRMA_TAVANI + 1))


def _tavan_mesaji() -> str:
    with pytest.raises(UyandirmaTavaniAsildi) as h:
        _kos(bitis=5.0, fabrika=lambda i: Tasan(i, yeni_kayit()))
    return str(h.value)


def test_P5_tavan_asimi_KOSUYU_DURDURUR_ve_DETERMINISTIK():
    a, b = _tavan_mesaji(), _tavan_mesaji()
    assert a == b, "aynı tohumda aynı düğüm/an/sayıda durmalı"
    assert f"> tavan {KM.BEKLEYEN_UYANDIRMA_TAVANI}" in a


def test_P5_tavan_ALTINDA_hicbir_uyandirma_DUSMEZ():
    kur, kosu, kayit = _kos()
    kk = sonuc_satiri(kur, kosu.dugumler, "k")["korunum"]
    assert kayit["dinamik_istek"] and kk["kontrol_uyandirma_tamam"]


# ==========================================================================
# P6 · SÖZLEŞME YÜZEYİ — pencere büyümedi, geri referans yok, hepsi-ya-hiç
# ==========================================================================
def test_P6_gozlem_penceresi_BUYUMEDI():
    # 🔴 12 → 17: `v2/15` B3 (K-179, öğrenci onayı K-170) — kendi GPS/INS'i
    # (konum, hız) ve telsiz sayaçları (meşgul süre, PHY hatası, alınan
    # çerçeve). Hepsi gerçek telsizin ve otopilotun verdiği şeyler.
    assert len(IZINLI_GOZLEM_ALANLARI) == 17
    # 🔴 7 → 6: `bildirdigi_konum` kaldırıldı (16 Eylül 2026, K-131). Alan
    # protokolden bağımsız olarak HER ZAMAN boştu; konum isteyen protokol onu
    # `beacon_yuku`na koyar ve bedelini öder.
    assert len(IZINLI_KOMSU_ALANLARI) == 6
    # 🔴 5 → 6: `kaynak_sira` eklendi (23 Eylül 2026, K-157). Başlıkta yazar
    # ve bedeli ödenir; küresel paket kimliği bilerek açılmadı (`v2/05` §3.3).
    # 🔴 6 → 7: `rota` eklendi (11 Ekim 2026, K-232) — DSR ailesinin kaynak
    # rotası başlıkta yazar, bedeli adres başına bayt (JarmRout'un sadakati).
    assert len(IZINLI_PAKET_ALANLARI) == 7


def test_P6_niyet_tiplerinde_GERI_REFERANS_YOK():
    izinli = {"KontrolIstegi", "Uyandirma", "MesajBicimi", "int", "float",
              "str", "bool", "tuple", "NoneType"}

    def gez(nesne, derinlik=0):
        assert type(nesne).__name__ in izinli and \
            type(nesne).__name__ not in YASAK_TIPLER
        if derinlik > 6:
            return
        alanlar = getattr(type(nesne), "__slots__", ())
        if alanlar and not isinstance(nesne, tuple):
            for a in alanlar:
                gez(getattr(nesne, a), derinlik + 1)
        elif isinstance(nesne, tuple):
            for x in nesne:
                gez(x, derinlik + 1)
    gez(KontrolIstegi.kur(1, ISTEK, {"tip": 2, "kaynak": 0, "sira": 1,
                                      "yol": (0, 1)}))
    gez(Uyandirma(1.0, "x"))


def test_P6_ilan_edilen_tip_KANCA_LISTESIYLE_birebir():
    """`KontrolluProtokol` ile `KONTROL_KANCALARI` iki ayrı liste olamaz."""
    for kanca in KONTROL_KANCALARI:
        assert hasattr(KontrolluProtokol, kanca)
    assert isinstance(SinavProtokolu(0, yeni_kayit()), KontrolluProtokol)
    assert isinstance(VeriIkizi(0), Protokol)
    assert not isinstance(VeriIkizi(0), KontrolluProtokol)


def test_P6_kismi_kanca_REDDEDILIR_ve_eski_protokol_NIYET_DOLDURAMAZ():
    class Kismi(VeriIkizi):
        __slots__ = ()

        def zamanlayicilar(self):
            return {}
    with pytest.raises(KontrolDuzlemiHatasi):
        _kos(bitis=5.0, fabrika=lambda i: Kismi(i))

    class Sizinti(VeriIkizi):
        __slots__ = ()

        def sonraki_atlama(self, gozlem):
            k = super().sonraki_atlama(gozlem)
            return Karar(sonraki=k.sonraki, niyetler=(Uyandirma(1.0, "x"),))
    with pytest.raises(KontrolDuzlemiHatasi):
        _kos(bitis=5.0, fabrika=lambda i: Sizinti(i))
    with pytest.raises(DegismezHatasi):
        KontrolIstegi(hedef=None, bicim=HELLO, yuk=(("kaynak", 1),
                      ("sira", 1), ("tip", 1)), mesaj_bayt=99)


# ==========================================================================
# P7 · BELİRLENİMCİLİK — kontrol trafiği VARKEN
# ==========================================================================
_OYNAK = ("kosu_kimligi", "calisma_kimligi", "zaman_damgasi_utc")


def _satir_json(**ek) -> str:
    kur, kosu, _ = _kos(**ek)
    s = sonuc_satiri(kur, kosu.dugumler, "kontrol_sinav")
    for a in _OYNAK:
        s["kimlik"].pop(a)
    # 🔒 `ortam` koşum ORTAMINI kaydeder (Python sürümü, PYTHONHASHSEED…) —
    # değişmesi gereken şey odur; sonuç değil. Karşılaştırmadan çıkar.
    s.pop("ortam")
    return json.dumps(s, sort_keys=True, default=list)


def test_P7_ayni_tohum_BIREBIR_ayni_satir():
    a, b = _satir_json(**KAYIPLI), _satir_json(**KAYIPLI)
    assert '"kontrol_duzlemi"' in a, "boş geçmemeli"
    assert a == b


def test_P7_PYTHONHASHSEED_sonucu_DEGISTIRMIYOR():
    kod = ("import sys; sys.path[:0] = [r'%s', r'%s']\n"
           "import test_kontrol_duzlemi as T\n"
           "print(T._satir_json(bitis=12.0))") % (KOK, KOK / "tests2")
    cikti = []
    for tohum in ("0", "12345"):
        p = subprocess.run([sys.executable, "-c", kod], capture_output=True,
                           text=True, encoding="utf-8",
                           env={**os.environ, "PYTHONHASHSEED": tohum,
                                "PYTHONIOENCODING": "utf-8"}, check=True)
        cikti.append(p.stdout.strip().splitlines()[-1])
    assert cikti[0] == cikti[1]


# ==========================================================================
# P8 · UÇTAN UCA KANAL — kayıp gözlenir, iki defter de kapanır
# ==========================================================================
def test_P8_kayipli_kanalda_UCTAN_UCA(monkeypatch):
    casus = Casus(monkeypatch)
    kur, kosu, kayit = _kos(**KAYIPLI)
    satir = sonuc_satiri(kur, kosu.dugumler, "kontrol_sinav")
    k, d = satir["korunum"], satir["teshis"]["kontrol_duzlemi"]["defter"]
    kayip = sum(1 for *_, b in casus.kontrol_alimlari if not b)
    basari = sum(1 for *_, b in casus.kontrol_alimlari if b)
    assert kur.kanal.karistirici is not None
    assert kayip > 0 and basari > 0, "kanal gerçekten kayıplı olmalı"
    # K-166 (denetim O-3): eski iddia (`… >= 0`) tanım gereği doğruydu.
    # Kayıplı kanalda unicast vazgeçmesi GÖZLENMELİ — ölçüldü: 22 / 550.
    assert d["unicast_vazgecilen"] > 0, "kayıplı kanalda vazgeçme yok"
    assert k["korunum_tamam"] and k["mutabakat_tamam"] \
        and k["iletim_sonucu_tamam"], "VERİ defteri bozuldu"
    assert k["kontrol_mesaj_tamam"] and k["kontrol_uyandirma_tamam"]
    assert k["gecerli"]
    gonderilen = len(kayit["gonderilen"])
    assert d["istenen"] == gonderilen, "her niyet deftere girmeli"


# ==========================================================================
# Y1 · KONTROL İSTATİSTİKLERİ SAYAÇ KÜTÜĞÜNDE — `v2/07` §18 Y1 · `v2/13` R8
# ==========================================================================
def test_Y1_her_defter_alani_SAYACTA_ve_dugum_TOPLAMINA_ESIT():
    kur, kosu, _ = _kos(**KAYIPLI)
    s = kur.sayaclar.disa_ver()
    for alan in DEFTER_ALANLARI:
        toplam = sum(d.kontrol.defter[alan] for d in kosu.dugumler)
        assert s["kontrol_" + alan] == toplam, alan
        ikiz = s["kontrol_" + alan + "_pencere"]
        assert ikiz is not None and 0 <= ikiz <= s["kontrol_" + alan], alan
    for alan in ("istenen", "iletim", "yayin_gonderilen", "unicast_onaylanan",
                 "teslim_yayin", "teslim_unicast", "periyodik_ates",
                 "dinamik_istenen", "dinamik_ates"):
        assert s["kontrol_" + alan] > 0, f"boş geçmemeli: {alan}"


def test_Y1_kontrol_KULLANMAYAN_protokolde_sayaclar_SIFIR():
    kur, kosu, _ = _kos(fabrika=lambda i: VeriIkizi(i))
    s = kur.sayaclar.disa_ver()
    assert all(s["kontrol_" + a] == 0 for a in DEFTER_ALANLARI)
    satir = sonuc_satiri(kur, kosu.dugumler, "veri_ikizi")
    assert "kontrol_duzlemi" not in satir["teshis"]


def test_Y1_mesaj_bicimi_dokumu_HAVAYA_CIKANLA_birebir(monkeypatch):
    casus = Casus(monkeypatch)
    kur, kosu, _ = _kos(**KAYIPLI)
    t = sonuc_satiri(kur, kosu.dugumler, "k")["teshis"]["kontrol_duzlemi"]
    tum, pencere = t["bicim"]["tum"], t["bicim"]["pencere"]
    assert set(tum) == {"SINAV_HELLO", "SINAV_ISTEK", "SINAV_CEVAP"}
    havada = [(b, sure) for _, tip, b, sure, _ in casus.iletimler
              if tip == "kontrol"]
    assert sum(v["cerceve"] for v in tum.values()) == len(havada) \
        == t["defter"]["iletim"]
    assert sum(v["bayt"] for v in tum.values()) == sum(b for b, _ in havada)
    assert sum(v["airtime_s"] for v in tum.values()) == pytest.approx(
        sum(sure for _, sure in havada), rel=0, abs=1e-12)
    s = kur.sayaclar.disa_ver()
    assert sum(v["cerceve"] for v in pencere.values()) \
        == s["kontrol_iletim_pencere"] > 0
    for ad, v in pencere.items():
        assert 0 < v["cerceve"] <= tum[ad]["cerceve"]


# ==========================================================================
# P9 · Y3 · R2 — KOŞUM BEACON'I PROTOKOL BAŞINA KAPATILABİLİR
# ==========================================================================
class BeaconsuzSinav(SinavProtokolu):
    """Kontrol düzlemini kullanır ama koşum beacon'ını kapatır."""

    __slots__ = ()
    kosum_beaconi = False


def test_P9_kosum_beaconi_KAPATILABILIR_komsu_tablosu_BOS_kalir():
    """🔒 Kapatan protokolde beacon HİÇ çizelgelenmez; komşu listesi boş kalır.

    ⚠️ Kapı boş geçmesin: aynı koşu beacon AÇIKKEN de ölçülür — gönderilen
    beacon sayısı orada sıfırdan büyük olmalı, yoksa test hiçbir şey ölçmez.
    """
    kayit = yeni_kayit()
    kur, kosu, _ = _kos(bitis=8.0, fabrika=lambda i: BeaconsuzSinav(i, kayit))
    s = kur.sayaclar.disa_ver()
    assert s.get("beacon_gonderilen", 0) == 0
    assert s.get("beacon_alinan", 0) == 0
    assert all(not d.gozlem(8.0, None).komsular for d in kosu.dugumler)

    acik_kur, _acik_kosu, _acik_kayit = _kos(bitis=8.0)
    assert acik_kur.sayaclar.disa_ver()["beacon_gonderilen"] > 0

    teshis = KM.kontrol_teshisi(kosu.dugumler)
    assert teshis["kosum_beaconi_kapali_dugum"] == kur.dugum_sayisi


def test_P9_kontrol_duzlemsiz_protokol_beaconi_KAPATAMAZ():
    """Kancasız ve beacon'sız bir protokol kalıcı olarak KÖR olurdu."""
    class Kor(VeriIkizi):
        __slots__ = ()
        kosum_beaconi = False

    with pytest.raises(KontrolDuzlemiHatasi):
        _kos(bitis=5.0, fabrika=lambda i: Kor(i))


# ==========================================================================
# P10 · Y3 · R3 — MAC VAZGEÇİNCE PROTOKOL HABERDAR OLUR
# ==========================================================================
def test_P10_MAC_vazgecince_protokole_BILDIRILIR_ve_SAYILIR():
    """Karıştırıcı altında unicast vazgeçmeleri olur ve kanca her birinde çağrılır."""
    kayit = yeni_kayit()
    kur, kosu, _ = _kos(bitis=12.0, fabrika=lambda i: SinavProtokolu(i, kayit),
                        **KAYIPLI)
    bildirim = kayit["iletim_basarisiz"]
    assert bildirim, "kapı boş geçmesin: hiç vazgeçme olmadıysa kapı ölçmüyor"
    assert {t for _n, _h, t, _s in bildirim} <= {"veri", "kontrol"}
    assert all(h is None or 0 <= h < kur.dugum_sayisi
               for _n, h, _t, _s in bildirim)
    s = kur.sayaclar.disa_ver()
    assert s["kontrol_basarisiz_bildirim"] == len(bildirim)
    assert sum(d.kontrol.defter["basarisiz_bildirim"]
               for d in kosu.dugumler) == len(bildirim)


def test_P10_DORT_KANCA_YETMEZ_besincisi_ZORUNLU():
    """Kanca sayısı 4'ten 5'e çıktı; hepsi-ya-hiç kuralı sürüyor."""
    class Eksik(VeriIkizi):
        __slots__ = ()

        def zamanlayicilar(self):
            return {}

        def zamanlayici_doldu(self, gozlem, etiket):
            return ()

        def uyandi(self, gozlem, etiket):
            return ()

        def kontrol_alindi(self, gozlem, gonderen, bicim, yuk, yayin):
            return ()

    with pytest.raises(KontrolDuzlemiHatasi):
        _kos(bitis=5.0, fabrika=lambda i: Eksik(i))


# ==========================================================================
# P11 · Y3 · R4 — TİTREŞİMİ SİMÜLATÖR ÇEKER, DEFTER KAPALI KALIR
# ==========================================================================
class TitresimliSinav(SinavProtokolu):
    """Periyodik yayınını ve uyandırmasını TİTREŞİMLE ister."""

    __slots__ = ()

    def zamanlayici_doldu(self, gozlem, etiket):
        from dataclasses import replace
        self.kayit["periyodik"].append(
            (gozlem.dugum, etiket, float(gozlem.saat_s)))
        if etiket != "hello":
            return ()
        return (replace(self._mesaj(None, HELLO), jitter_s=0.5),
                Uyandirma(GECIKME_S, "titresimli", jitter_s=0.5))


def test_P11_titresim_DEFTERI_KAPALI_ve_kosu_GECERLI():
    kayit = yeni_kayit()
    kur, kosu, _ = _kos(bitis=10.0,
                        fabrika=lambda i: TitresimliSinav(i, kayit))
    s = kur.sayaclar.disa_ver()
    assert s["kontrol_jitter_istenen"] > 0, "kapı boş geçmesin"
    bekleyen = sum(d.kontrol.bekleyen_jitter for d in kosu.dugumler)
    assert (s["kontrol_jitter_istenen"]
            == s["kontrol_jitter_ates"] + bekleyen)
    assert all(d.kontrol.korunum()["jitter_tamam"] for d in kosu.dugumler)
    satir = sonuc_satiri(kur, kosu.dugumler, "titresimli")
    assert satir["korunum"]["kontrol_jitter_tamam"]
    assert satir["korunum"]["gecerli"]


def test_P11_titresim_AYNI_TOHUMDA_BIREBIR():
    """Titreşim düğüm alt akışından gelir: aynı tohum aynı sonucu verir."""
    a = _kos(bitis=10.0, fabrika=lambda i: TitresimliSinav(i, yeni_kayit()))[0]
    b = _kos(bitis=10.0, fabrika=lambda i: TitresimliSinav(i, yeni_kayit()))[0]
    sa, sb = a.sayaclar.disa_ver(), b.sayaclar.disa_ver()
    for ad in ("kontrol_jitter_istenen", "kontrol_jitter_ates",
               "kontrol_istenen", "kontrol_iletim", "kontrol_teslim_yayin"):
        assert sa[ad] == sb[ad], ad


@pytest.mark.parametrize("jitter", [-1e-9, float("nan"), float("inf")])
def test_P11_gecersiz_titresim_REDDEDILIR(jitter):
    with pytest.raises(DegismezHatasi):
        Uyandirma(1.0, "x", jitter_s=jitter)
    with pytest.raises(DegismezHatasi):
        KontrolIstegi.kur(None, HELLO, {"tip": 1, "kaynak": 1, "sira": 1},
                          jitter_s=jitter)


# ==========================================================================
# `v2/15` B1 (K-172) — kontrol ve kontrol onayı çerçeveleri de bildirilir
# ==========================================================================
def test_B1_KONTROL_ve_KONAY_cerceveleri_de_duyuluyor():
    duyulan: list = []

    class Duyan(SinavProtokolu):
        __slots__ = ()

        def cerceve_duyuldu(self, gozlem, gonderen, tur, hedef, rssi_dbm,
                            paket):
            duyulan.append((gozlem.dugum, tur, hedef))

    kayit = yeni_kayit()
    kur, _, _ = _kos(bitis=10.0, fabrika=lambda i: Duyan(i, kayit))
    s = kur.sayaclar.disa_ver()
    assert len(duyulan) == s["duyma_bildirimi"] == s["alim_basarili"]
    turler = {t for _, t, _ in duyulan}
    assert {"kontrol", "konay", "veri", "onay"} <= turler, turler
    # yayın kontrolünde hedef yok, unicast'ta var — ikisi de görülmeli
    kontrol_hedefleri = {h is None for _, t, h in duyulan if t == "kontrol"}
    assert kontrol_hedefleri == {True, False}


# ==========================================================================
# `v2/15` A4 (K-177) — kontrol unicast'ı ARF hızıyla, yayın temel hızda
# ==========================================================================
def test_A4_KONTROL_unicast_ARF_ile_defter_KAPANIR():
    kur, kosu, _ = _kos(bitis=10.0, islem_kazanci=True,
                        bant_genisligi_hz=22e6, hiz_uyarlamasi=True)
    komsular = sum(sum(d.hiz_denetcisi.dagilim().values())
                   for d in kosu.dugumler)
    assert komsular > 0, "ARF hiç bildirim almadı"
    from sim2.kosum.sonuc import korunum_bolumu
    assert korunum_bolumu(kur, kosu.dugumler)["gecerli"]
