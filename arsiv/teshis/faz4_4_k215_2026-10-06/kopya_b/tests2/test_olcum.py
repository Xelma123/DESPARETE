"""
ADIM 8 — `sim2/olcum/` kapanış ölçütleri.

Yol haritası:
    🔒 7 metriğin 7'si BİR koşudan üretiliyor; her metriğin **bağımsız
    hesapla** eşleştiği içerik testi var.

Eski simülatör 7 metrikten yalnız 2'sini üretiyordu. Eksikler: PSR · p95
gecikme · NRL · üç kopma sayacı · Δ · COR.

🔴 Bu dosyanın en önemli testleri RİSK 3'e ait: hiç beyan etmeyen bir
protokolün kopma sayacı 0 çıkar ve "iyi" görünür. Etiketlenmesi gerekiyor.
"""

from __future__ import annotations

import ast
import math
import pathlib
import statistics as ist
import sys

import pytest

KOK = pathlib.Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))
SIM2 = KOK / "sim2"

from sim2.cekirdek.degismezler import DegismezHatasi  # noqa: E402
from sim2.cekirdek.sayaclar import Sayaclar  # noqa: E402
from sim2.gozlem.karar import Beyan  # noqa: E402
from sim2.olcum.kahin import Kahin, kahin  # noqa: E402
from sim2.olcum.metrikler import (YUZDELIKLER, metrik_sozlugu,  # noqa: E402
                                  ozet_istatistik, yuzdelik)
from sim2.olcum.paket_defteri import PaketDefteri  # noqa: E402
from sim2.olcum.rota_olaylari import RotaDefteri  # noqa: E402


# ==========================================================================
# KÂHİN SARMALAYICI
# ==========================================================================

def test_kahin_YALNIZ_raporla_okunuyor():
    k = kahin(42)
    assert k.rapora() == 42
    assert "42" not in repr(k) and "42" not in str(k)
    assert repr(k) == "Kahin<int>"


def test_kahin_DONDURULMUS():
    import dataclasses
    k = kahin(1)
    with pytest.raises(dataclasses.FrozenInstanceError):
        k._deger = 2  # type: ignore[misc]


def test_olcum_kahin_PROTOKOL_grafiginde_YOK():
    """🔒 `gozlem/` ve (ileride) `protokoller/` kâhini içe aktaramaz."""
    ihlal: list[str] = []
    for kok in ("gozlem", "kanal", "mac", "ag", "dunya"):
        dizin = SIM2 / kok
        if not dizin.exists():
            continue
        for yol in sorted(dizin.rglob("*.py")):
            if "__pycache__" in yol.parts:
                continue
            agac = ast.parse(yol.read_text(encoding="utf-8"))
            for n in ast.walk(agac):
                if isinstance(n, ast.ImportFrom) and n.module \
                        and n.module.startswith("sim2.olcum"):
                    ihlal.append(f"{kok}/{yol.name}:{n.lineno} → {n.module}")
    assert not ihlal, f"🔴 `olcum/` yukarı katmanlara sızmış: {ihlal}"


def test_BEYAN_yalniz_olcumde_ice_aktariliyor():
    """🔴 Risk 3 (c): `olcum/` dışında hiçbir modül `Beyan`ı içe aktaramaz."""
    ihlal: list[str] = []
    for yol in sorted(SIM2.rglob("*.py")):
        if "__pycache__" in yol.parts:
            continue
        goreli = yol.relative_to(SIM2).as_posix()
        if goreli.startswith(("olcum/", "gozlem/")):
            continue
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        for n in ast.walk(agac):
            if isinstance(n, ast.ImportFrom) and n.module == "sim2.gozlem.karar":
                for a in n.names:
                    if a.name == "Beyan":
                        ihlal.append(f"{goreli}:{n.lineno}")
    assert not ihlal, f"🔴 `Beyan` yetkisiz modülde: {ihlal}"


# ==========================================================================
# PAKET DEFTERİ
# ==========================================================================

def _defter(pencere=(50.0, 320.0)) -> PaketDefteri:
    return PaketDefteri(pencere_bas_s=pencere[0], pencere_bitis_s=pencere[1])


def test_pdr_BAGIMSIZ_hesapla_eslesiyor():
    d = _defter()
    for n in range(100):
        d.dogdu(n, akis_kimligi=n % 5, dogum_s=100.0 + n)
    for n in range(0, 100, 2):
        d.teslim_edildi(n, 100.0 + n + 0.05)
    assert d.uretilen == 100 and d.teslim == 50
    assert d.teslim / d.uretilen == pytest.approx(0.5)


def test_KOPYA_teslim_REDDEDILIYOR():
    """🔴 Kopya teslim PDR'yi 1'in üstüne çıkarır ve hata sessiz kalır."""
    d = _defter()
    d.dogdu(1, 0, 100.0)
    d.teslim_edildi(1, 100.1)
    with pytest.raises(DegismezHatasi):
        d.teslim_edildi(1, 100.2)


def test_dogmamis_paket_ve_GERIYE_teslim_reddediliyor():
    d = _defter()
    with pytest.raises(DegismezHatasi):
        d.teslim_edildi(7, 100.0)
    d.dogdu(7, 0, 100.0)
    with pytest.raises(DegismezHatasi):
        d.teslim_edildi(7, 99.0)
    with pytest.raises(DegismezHatasi):
        d.dogdu(7, 0, 101.0)          # aynı kimlik iki kez


def test_PENCERE_DOGUMA_gore():
    """🔴 Teslime göre sayılsaydı pay ile payda farklı kümelerden gelir ve
    oran 1'i aşabilirdi."""
    d = _defter((50.0, 320.0))
    d.dogdu(1, 0, 10.0)      # pencere ÖNCESİ
    d.dogdu(2, 0, 100.0)     # pencere İÇİ
    d.dogdu(3, 0, 400.0)     # pencere SONRASI
    for k in (1, 2, 3):
        d.teslim_edildi(k, 500.0)     # üçü de pencere DIŞINDA teslim
    assert d.uretilen == 3 and d.pencerede_uretilen == 1
    assert d.teslim == 3 and d.pencerede_teslim == 1
    assert d.pencere_kimlik_araligi() == (2, 2)


def test_gecikme_DOGUMDAN_teslime():
    d = _defter()
    d.dogdu(1, 0, 100.0)
    d.teslim_edildi(1, 100.25)
    assert d.gecikmeler() == (pytest.approx(0.25),)


def test_IPDV_AKIS_ICI_ve_DOGUM_sirasina_gore():
    """🔒 Akış kimliği olmasaydı iki akışın paketleri karışır ve ölçülen
    titreşim trafiğin değil, akışların kaymasının titreşimi olurdu."""
    d = _defter()
    # akış 0: gecikmeler 0,10 → 0,30 → 0,15   → |Δ| = 0,20 ve 0,15
    for n, (dogum, gecikme) in enumerate([(100.0, 0.10), (101.0, 0.30),
                                          (102.0, 0.15)]):
        d.dogdu(n, 0, dogum)
        d.teslim_edildi(n, dogum + gecikme)
    # akış 1: tek paket → IPDV üretmez
    d.dogdu(10, 1, 100.0)
    d.teslim_edildi(10, 100.9)
    olculen = sorted(d.ipdv())
    assert olculen == [pytest.approx(0.15), pytest.approx(0.20)]


def test_IPDV_teslim_sirasina_gore_DEGIL():
    """Teslim sırası yeniden sıralamayı da içerir; ölçülen şey titreşim
    yerine sıra bozulması olurdu."""
    d = _defter()
    d.dogdu(0, 0, 100.0)
    d.dogdu(1, 0, 101.0)
    d.teslim_edildi(1, 101.1)     # ikinci paket ÖNCE teslim edildi
    d.teslim_edildi(0, 102.0)
    # doğum sırası: gecikmeler 2,0 sonra 0,1 → |Δ| = 1,9
    assert d.ipdv() == (pytest.approx(1.9),)


def test_HAM_sozluk_uc_SEMA_TAAHHUDUNU_tasiyor():
    d = _defter()
    d.dogdu(5, 2, 100.0)
    d.teslim_edildi(5, 100.4)
    ham = d.ham_sozluk()
    for anahtar in ("teslim_kimlikleri", "teslim_gecikmeleri_s",
                    "teslim_akis_kimlikleri", "teslim_dogum_s",
                    "pencere_kimlik_araligi", "pencerede_uretilen"):
        assert anahtar in ham
    assert ham["teslim_akis_kimlikleri"] == (2,)
    assert ham["teslim_dogum_s"] == (100.0,)


# ==========================================================================
# YÜZDELİK — bağımsız hesapla eşleşme
# ==========================================================================

def test_yuzdelik_BAGIMSIZ_hesapla_eslesiyor():
    """Bağımsız hesap: `statistics.quantiles(method='inclusive')` aynı
    doğrusal aradeğerlemeli tanımı kullanır."""
    ornek = [0.05, 0.11, 0.13, 0.22, 0.31, 0.47, 0.52, 0.61, 0.78, 0.95]
    bagimsiz = ist.quantiles(ornek, n=100, method="inclusive")
    for p in YUZDELIKLER:
        assert yuzdelik(ornek, p) == pytest.approx(bagimsiz[p - 1], abs=1e-12)


def test_yuzdelik_sinirlar():
    assert yuzdelik([], 95) is None
    assert yuzdelik([3.0], 95) == 3.0
    assert yuzdelik([1.0, 2.0], 0) == 1.0
    assert yuzdelik([1.0, 2.0], 100) == 2.0
    assert yuzdelik([1.0, 2.0], 50) == pytest.approx(1.5)
    with pytest.raises(DegismezHatasi):
        yuzdelik([1.0], 101)


def test_BOS_ornekte_None_SIFIR_DEGIL():
    """🔴 `0.0` döndürmek ölçülmemiş bir hücreyi ortalamaya sokardı."""
    ozet = ozet_istatistik([], "gecikme")
    assert all(v is None for v in ozet.values())
    assert set(ozet) == {"gecikme_ort_s"} | {f"gecikme_p{p}_s"
                                             for p in YUZDELIKLER}


# ==========================================================================
# 🔴 ROTA OLAYLARI — RİSK 3
# ==========================================================================

def test_delta_BEYANDAN_beyana():
    r = RotaDefteri()
    r.beyan_isle(3, Beyan("kopma", 9), 100.0)
    r.beyan_isle(3, Beyan("rota_kuruldu", 9), 100.8)
    assert r.delta_ler() == (pytest.approx(0.8),)
    assert r.rota_kurtarildi == 1 and r.rota_etkilendi == 1
    assert r.cor() == pytest.approx(1.0)


def test_IKINCI_kopma_beyani_ILKINI_ezmiyor():
    """Protokol tekrar beyan ederse ölçülen şey İLK kesintinin süresi olmalı."""
    r = RotaDefteri()
    r.beyan_isle(3, Beyan("kopma", 9), 100.0)
    r.beyan_isle(3, Beyan("kopma", 9), 100.5)
    r.beyan_isle(3, Beyan("rota_kuruldu", 9), 101.0)
    assert r.delta_ler() == (pytest.approx(1.0),)


def test_KAPANMAMIS_kopma_ortalamaya_GIRMIYOR_ama_sayiliyor():
    """⚠️ Girmediklerini bilmeden Δ okumak, kurtarılamayan kopmaları yok
    saymak olur."""
    r = RotaDefteri()
    r.beyan_isle(1, Beyan("kopma", 2), 10.0)
    r.beyan_isle(1, Beyan("rota_kuruldu", 2), 10.5)
    r.beyan_isle(1, Beyan("kopma", 3), 20.0)      # hiç kurtarılmadı
    assert r.delta_ler() == (pytest.approx(0.5),)
    assert r.kapanmamis_kopma() == 1
    assert r.rota_etkilendi == 2 and r.rota_kurtarildi == 1
    assert r.cor() == pytest.approx(0.5)


def test_HIC_BEYAN_ETMEYEN_kol_ETIKETLENIYOR():
    """🔴 RİSK 3'ÜN KALBİ.

    Hiç beyan etmeyen protokolün kopma sayacı 0 çıkar ve tabloda *"hiç kopma
    yaşamadı"* gibi görünür. Oysa yalnızca susmuştur.
    """
    r = RotaDefteri()
    r.fiziksel_kopma(120)                  # gerçekte 120 bağ koptu
    assert r.kopma_algilanan == 0
    assert r.beyan_etmiyor is True
    assert r.algilama_duyarliligi() == 0.0
    assert r.delta_ler() == ()
    assert r.cor() is None, "COR beyan yoksa TANIMSIZ, sıfır değil"


def test_algilama_duyarliligi_KAHIN_paydayla():
    r = RotaDefteri()
    r.fiziksel_kopma(100)
    for n in range(30):
        r.beyan_isle(n, Beyan("kopma", n + 1), 10.0 + n)
    assert r.algilama_duyarliligi() == pytest.approx(0.30)
    assert r.beyan_etmiyor is False


def test_fiziksel_kopma_KAHIN_sarmalayiciyla_donuyor():
    r = RotaDefteri()
    r.fiziksel_kopma(7)
    k = r.kopma_fiziksel()
    assert isinstance(k, Kahin)
    assert k.rapora() == 7
    assert "7" not in repr(k)


def test_fiziksel_kopma_YOKSA_duyarlilik_None():
    r = RotaDefteri()
    r.beyan_isle(1, Beyan("kopma", 2), 5.0)
    assert r.algilama_duyarliligi() is None, "payda 0 → oran TANIMSIZ"


def test_kurtarma_kopmadan_ONCE_olamaz():
    r = RotaDefteri()
    r.beyan_isle(1, Beyan("kopma", 2), 100.0)
    with pytest.raises(DegismezHatasi):
        r.beyan_isle(1, Beyan("rota_kuruldu", 2), 99.0)


# ==========================================================================
# 🔒 KAPANIŞ ÖLÇÜTÜ — YEDİ METRİĞİN YEDİSİ, BİR KOŞUDAN
# ==========================================================================

def _dolu_kosum():
    """Sayaçlar + paket defteri + rota defteri: bir koşunun ölçüm tarafı."""
    s = Sayaclar()
    d = _defter((50.0, 320.0))
    r = RotaDefteri()
    r.fiziksel_kopma(40)

    s.pencere_baslat()
    for n in range(200):
        dogum = 60.0 + n
        d.dogdu(n, akis_kimligi=n % 10, dogum_s=dogum)
        s.artir("uretilen_paket")
        s.artir("mac_gonderim_istegi", 3)
        # 🔴 PSR'nin PAYDASI `mac_deneme` — yeniden denemeler DÂHİL.
        # 5 Eylül 2026'da düzeltildi; kayıt defteri `mac_gonderim_istegi`
        # kullanıyordu ve o sayaç paket-atlama başına bir kez artıyor.
        s.artir("mac_deneme", 4)
        s.artir("veri_alim_hedefte", 3)     # PSR'nin payı — alıcı tarafı
        s.artir("mac_gonderim_basarili", 2)
        s.ekle("veri_bayt", 512 * 3)
        s.ekle("veri_airtime_s", 0.00224 * 3)
        if n % 4 != 3:                      # dörtte üçü teslim
            d.teslim_edildi(n, dogum + 0.02 + 0.001 * (n % 17))
            s.artir("teslim_paket")
    for n in range(150):
        s.artir("kontrol_cerceve")
        s.ekle("kontrol_bayt", 32)
        s.ekle("kontrol_airtime_s", 0.00032)
    for n in range(24):
        r.beyan_isle(n % 8, Beyan("kopma", n % 5 + 10), 100.0 + n)
        s.artir("kopma_algilanan")
        if n % 3 == 0:
            r.beyan_isle(n % 8, Beyan("rota_kuruldu", n % 5 + 10), 100.4 + n)
            s.artir("rota_kurtarildi")
    s.artir("kopma_fiziksel", 40)
    s.artir("rota_etkilendi", r.rota_etkilendi)
    s.pencere_bitir()
    return s, d, r


def test_YEDI_METRIK_bir_kosudan():
    """🔒 Kapanış ölçütü. Yedisi de üretiliyor ve `None` değil."""
    s, d, r = _dolu_kosum()
    m = metrik_sozlugu(s.disa_ver(), d, r)

    yedi = {
        "1 PDR": "pdr",
        "2 PSR": "psr",
        "3 gecikme p95": "gecikme_p95_s",
        "4 NRL (çerçeve)": "nrl_cerceve",
        "5 kopma (algılanan)": "kopma_algilanan",
        "6 Δ (rota kurtarma)": "rota_kurtarma_delta_ort_s",
        "7 COR": "cor",
    }
    eksik = [ad for ad, anahtar in yedi.items()
             if anahtar not in m or m[anahtar] is None]
    assert not eksik, f"🔴 üretilmeyen metrik: {eksik}"

    # NRL'nin üç sürümü de olmalı — ölçüldü, 1,80 kat ayrışabiliyorlar
    for ad in ("nrl_cerceve", "nrl_bayt", "nrl_airtime"):
        assert m[ad] is not None
    # üç kopma sayacının üçü de
    for ad in ("kopma_fiziksel", "kopma_algilanan", "kopma_rota_gecersiz"):
        assert ad in m


def test_HER_METRIGIN_pencere_ikizi_VAR():
    s, d, r = _dolu_kosum()
    m = metrik_sozlugu(s.disa_ver(), d, r)
    for ad in ("pdr", "psr", "mac_basari_orani", "nrl_cerceve", "nrl_bayt",
               "nrl_airtime", "cor", "gecikme_ort_s", "gecikme_p95_s",
               "ipdv_ort_s"):
        assert f"{ad}_pencere" in m, f"🔴 {ad} pencere ikizi yok"


def test_PDR_bagimsiz_hesapla_esitleniyor():
    s, d, r = _dolu_kosum()
    m = metrik_sozlugu(s.disa_ver(), d, r)
    bagimsiz = d.teslim / d.uretilen
    assert m["pdr"] == pytest.approx(bagimsiz, rel=1e-12)


def test_GECIKME_yuzdelikleri_ham_listeden_YENIDEN_URETILEBILIYOR():
    """🔒 `analiz/`in doğrulama kapılarından biri tam olarak bu olacak.

    Ham liste satırda olmasaydı iki gerçekleme sessizce ayrışırdı.
    """
    s, d, r = _dolu_kosum()
    m = metrik_sozlugu(s.disa_ver(), d, r)
    ham = d.ham_sozluk()["teslim_gecikmeleri_s"]
    assert m["gecikme_ort_s"] == pytest.approx(ist.mean(ham), rel=1e-12)
    for p in YUZDELIKLER:
        assert m[f"gecikme_p{p}_s"] == pytest.approx(yuzdelik(ham, p),
                                                     rel=1e-12)


def test_NRL_UC_SURUMU_ayrisabiliyor():
    """Ölçüldü: çerçeve, bayt ve airtime sürümleri 1,80 kat ayrışabiliyor.
    Üçünü de raporlamanın sebebi bu."""
    s, d, r = _dolu_kosum()
    m = metrik_sozlugu(s.disa_ver(), d, r)
    degerler = {m["nrl_cerceve"], m["nrl_bayt"], m["nrl_airtime"]}
    assert len(degerler) == 3, "üç sürüm aynı sayıyı veriyorsa biri gereksiz"


def test_SAYACLARDAKI_oran_YENIDEN_hesaplanmiyor():
    """🔒 Kusur 6: bir oranı iki yerde hesaplamak sessiz ayrışma demektir.

    `metrik_sozlugu` sayaçlardan gelen anahtarları DEĞİŞTİRMEDEN geçirmeli.
    """
    s, d, r = _dolu_kosum()
    sayac = s.disa_ver()
    m = metrik_sozlugu(sayac, d, r)
    for ad, deger in sayac.items():
        assert m[ad] == deger or (deger is None and m[ad] is None), (
            f"🔴 {ad} ölçüm katmanında yeniden hesaplanmış")


def test_delta_HIC_BEYAN_yoksa_None():
    s = Sayaclar()
    d = _defter()
    d.dogdu(0, 0, 100.0)
    d.teslim_edildi(0, 100.1)
    r = RotaDefteri()
    r.fiziksel_kopma(50)
    m = metrik_sozlugu(s.disa_ver(), d, r)
    assert m["rota_kurtarma_delta_ort_s"] is None
    assert m["rota_kurtarma_delta_p95_s"] is None
    assert m["beyan_etmiyor"] is True
    assert m["algilama_duyarliligi_olcum"] == 0.0
    assert m["cor_olcum"] is None


def test_metrik_sozlugu_KAHINI_acikca_raporluyor():
    """Kâhin sayaç rapora GİRER (raporlanmalı), karara giremez."""
    s, d, r = _dolu_kosum()
    m = metrik_sozlugu(s.disa_ver(), d, r)
    assert m["kopma_fiziksel_olcum"] == 40
    assert isinstance(m["kopma_fiziksel_olcum"], int)


def test_olcum_YUKARI_katmani_ice_aktarmiyor():
    """Katman yönü: `olcum` `kosum`dan öncedir."""
    ihlal: list[str] = []
    for yol in sorted((SIM2 / "olcum").rglob("*.py")):
        if "__pycache__" in yol.parts:
            continue
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        for n in ast.walk(agac):
            if isinstance(n, ast.ImportFrom) and n.module \
                    and n.module.startswith("sim2.kosum"):
                ihlal.append(f"{yol.name}:{n.lineno} → {n.module}")
    assert not ihlal, f"🔴 katman yönü kırıldı: {ihlal}"


def test_COR_ayni_bag_IKI_KEZ_kopup_kurtarilinca_BIR_kalir():
    """🔴 K-141 — COR'un pay ve paydası AYNI birimi sayar: kopma döngüsü.

    Önceden pay döngü, payda FARKLI BAĞ sayıyordu ve bu dizide COR = 2,0
    çıkardı — "kurtarılan / etkilenen" diye tanımlı bir oran. AODV'nin beyan
    anahtarları düzelince gerçek bir koşuda ölçüldü: `bagimsiz-yok` 3,26.
    """
    r = RotaDefteri()
    r.beyan_isle(3, Beyan("kopma", 9), 100.0)
    r.beyan_isle(3, Beyan("rota_kuruldu", 9), 101.0)
    r.beyan_isle(3, Beyan("kopma", 9), 200.0)          # AYNI bağ, yeni döngü
    r.beyan_isle(3, Beyan("rota_kuruldu", 9), 201.0)
    assert r.rota_etkilendi == 2 and r.rota_kurtarildi == 2
    assert r.cor() == pytest.approx(1.0), "aynı bağın iki döngüsü COR'u şişirdi"


def test_COR_DEGISMEZI_kapanan_arti_bekleyen_ACILANA_esit():
    """🔒 Her açılan döngü ya kapandı ya hâlâ bekliyor; COR ∈ [0, 1]."""
    import random
    rng = random.Random(11)
    r = RotaDefteri()
    t = 0.0
    for _ in range(400):
        t += 0.1
        tip = rng.choice(("kopma", "kopma", "rota_kuruldu"))
        r.beyan_isle(rng.randrange(5), Beyan(tip, rng.randrange(6)), t)
    assert r.rota_kurtarildi + r.kapanmamis_kopma() == r.rota_etkilendi
    assert r.cor() is not None and 0.0 <= r.cor() <= 1.0


def test_beyan_isle_DONGU_ETIKETI_donduruyor():
    """🔒 Sayaç kütüğü COR'un ikizini bu dönüşten besler (`kosum/dugum.py`)."""
    r = RotaDefteri()
    assert r.beyan_isle(1, Beyan("kopma", 2), 1.0) == "acildi"
    assert r.beyan_isle(1, Beyan("kopma", 2), 1.5) is None     # zaten açık
    assert r.beyan_isle(1, Beyan("rota_kuruldu", 2), 2.0) == "kapandi"
    assert r.beyan_isle(1, Beyan("rota_kuruldu", 2), 2.5) is None  # kapanmıştı


def test_KRE_PDR_kohortu_YASAYAN_uclar_gorev_orani_PLANLANAN():
    """🔒 KR-E (K-182): ölü hedefe doğan paket PDR'ye girmez, ölü kaynağın
    doğuramadığı paket de; ikisi görev teslim oranının paydasında."""
    from sim2.olcum.metrikler import metrik_sozlugu
    from sim2.olcum.rota_olaylari import RotaDefteri
    d = PaketDefteri(pencere_bas_s=0.0, pencere_bitis_s=100.0)
    d.dogdu(1, 0, 10.0, hedef=5)
    d.dogdu(2, 0, 20.0, hedef=5)
    d.teslim_edildi(1, 11.0)
    d.olu_dugumler.add(5)
    d.dogdu(3, 0, 30.0, hedef=5)          # hedef ölü → kohort dışı
    d.uretilmedi(40.0)                    # kaynak ölü → doğmadı
    d.uretilmedi(200.0)                   # pencere dışı
    assert d.uretilen == 2 and d.teslim == 1
    assert d.planlanan() == 5 and d.planlanan(True) == 4
    m = metrik_sozlugu({}, d, RotaDefteri())
    assert m["pdr"] == pytest.approx(0.5)
    assert m["gorev_teslim_orani"] == pytest.approx(1 / 5)
    assert m["gorev_teslim_orani_pencere"] == pytest.approx(1 / 4)
    ham = d.ham_sozluk()
    assert ham["olu_hedefe_dogum_s"] == (30.0,)
    assert ham["uretilmeyen_dogum_s"] == (40.0, 200.0)
