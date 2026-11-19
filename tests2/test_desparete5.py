"""DESPARETE 5 · simülatörde uçtan uca (küçük test dünyası; ölçüm değil):
paket ve kontrol defteri kapanır, rotalar kurulur, karıştırma yolları
işler, çekirdek profilde karıştırmaya karşı mekanizmalar çalışmaz, teşhis
sözleşmeye uyar, koşu belirlenimlidir, protokol yasak gözlem alanı okumaz.

Dünya `test_babel.py`ninkiyle aynı ölçekleme (12 düğüm, eski 1:50 dünyasının
alanı küçültülmüş); yere toplama deseni, karıştırıcı 20. saniyede açılır."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from protokoller.desparete5 import Desparete5
from protokoller.desparete5_bicim import (
    CEKIRDEK, DEGERLER_ESKI, ESKI_CEKIRDEK, TAM, Bayraklar)
from protokoller.desparete5_egim import Egim
from protokoller.desparete5_rota import Rota
from sim2.gozlem.teshis import teshis_dogrula
from sim2.kosum.kosu import Kosu
from sim2.kosum.kurulum import kurulum_yap
from sim2.kosum.sonuc import korunum_bolumu, sonuc_satiri
from sim2.yapilandirma.konfig import Konfig

KOK = Path(__file__).resolve().parent.parent
_V = Konfig(kol="t")
_N = 12
_EN = _V.alan_en_m * (_N / _V.dugum_sayisi) ** 0.5
# 18 Kasım'ın tam sürümü (eski veri tetiği, FD ve tur; 19 Kasım'da yeni
# sürümde kalktı, kodda bayrakla yeniden üretilir).
ESKI_TAM = Bayraklar(vazgecme_tetigi=False, egim=False, duzgun_gecis=False,
                     veri_kotu_tetigi=True)


def _kos(senaryo: str, bayraklar, degerler=None) -> dict:
    kfg = Konfig(kol="test", senaryo=senaryo, tohum=1000, isinma_s=50.0,
                 olcum_bitis_s=70.0, kosu_bitis_s=75.0, dugum_sayisi=_N,
                 trafik_deseni="yere_toplama", alan_en_m=_EN, alan_boy_m=_EN,
                 gorev_grup_sayisi=2, karistirici_baslangic_s=20.0,
                 gorev_grup_yaricapi_m=(_V.gorev_grup_yaricapi_m * _EN
                                        / _V.alan_en_m))
    kur = kurulum_yap(kfg)
    pr: list[Desparete5] = []

    def fabrika(i):
        p = Desparete5(i, kfg.gecit, bayraklar=bayraklar,
                       degerler=degerler)
        pr.append(p)
        return p

    kosu = Kosu(kur, fabrika)
    kosu.kostur()
    toplam: dict = {}
    for p in pr:
        t = p.teshis(p.kimlik)
        teshis_dogrula(p.kimlik, t)                 # en çok 32 alan
        for ad in ("protokol", "bag", "rota", "selam", "kendi", "bekletme",
                   "iz"):
            for k, v in zip(t[f"{ad}_adlari"], t[f"{ad}_sayac"]):
                toplam[f"{ad}.{k}"] = toplam.get(f"{ad}.{k}", 0) + v
    return {"korunum": korunum_bolumu(kur, kosu.dugumler),
            "satir": sonuc_satiri(kur, kosu.dugumler, "desparete5"),
            "protokoller": pr, "toplam": toplam}


@pytest.fixture(scope="module")
def sakin():
    return _kos("statik-yok", TAM)


@pytest.fixture(scope="module")
def karisik():
    return _kos("statik-surekli", TAM)


@pytest.fixture(scope="module")
def karisik_eski():
    return _kos("statik-surekli", ESKI_TAM, DEGERLER_ESKI)


def test_SAKIN_dunyada_defter_kapanir_rotalar_kurulur(sakin):
    r = sakin["korunum"]
    assert r["korunum_tamam"] and r["mutabakat_tamam"], r
    assert sakin["satir"]["korunum"]["gecerli"]
    assert r["teslim"] > 0.9 * r["uretilen"]
    pr = sakin["protokoller"]
    assert all(p.rota.ardil is not None for p in pr if p.kimlik != 0)
    assert pr[0].rota.ardil is None and pr[0].rota.C == 0
    t = sakin["toplam"]
    assert t["selam.selam"] > 0 and t["iz.iz_ogrenilen"] > 0
    assert t["protokol.komut_gonderilen"] > 0       # geri iz çalışıyor
    assert all(isinstance(p.rota, Egim) for p in pr)
    assert t["bag.vaz_kayit"] > 0                   # KK-01/6
    assert t["protokol.tur_istegi_gonderilen"] == 0  # T-13: tur yok


def test_KARISTIRMA_YOLLARI_isler_defter_kapanir(karisik):
    r = karisik["korunum"]
    assert r["korunum_tamam"] and r["mutabakat_tamam"], r
    t = karisik["toplam"]
    assert t["kendi.giris_girisim"] + t["kendi.giris_ed"] > 0     # KK-03 A
    assert t["bag.karisma_bit"] > 0 and t["bag.karisma_bitti"] > 0  # KK-01/9–10
    assert t["protokol.tur_istegi_gonderilen"] == 0  # T-13
    assert t["bag.askida_giris"] == 0 and t["bag.veri_kotu"] == 0  # T-2
    kd = karisik["satir"]["teshis"]["kontrol_duzlemi"]
    assert kd["tepe_bekleyen_uyandirma"] < 32       # niyet döngüsü yok


def test_ESKI_TASARIM_karistirma_ve_tur_yollari_isler(karisik_eski):
    """18 Kasım'ın uçtan uca kanıtı (`ESKI_TAM`, `DEGERLER_ESKI`): açlıkta
    istek, tur artışı, istek yolundan yanıt."""
    r = karisik_eski["korunum"]
    assert r["korunum_tamam"] and r["mutabakat_tamam"], r
    t = karisik_eski["toplam"]
    assert all(isinstance(p.rota, Rota) for p in karisik_eski["protokoller"])
    assert t["kendi.giris_girisim"] + t["kendi.giris_ed"] > 0
    assert t["bag.karisma_bit"] > 0 and t["bag.karisma_bitti"] > 0
    assert t["rota.aclik_istegi"] > 0 and t["rota.tur_artirildi"] > 0
    assert t["rota.istek_karsilandi"] > 0           # yanıt istek yolundan
    gecit = karisik_eski["protokoller"][0]
    assert gecit.rota.tur_gecit == 1 + t["rota.tur_artirildi"]
    assert t["bag.vaz_kayit"] == 0                  # vazgeçme tetiği kapalı


def test_CEKIRDEK_profilde_karistirmaya_karsi_mekanizma_calismaz():
    s = _kos("statik-surekli", CEKIRDEK)
    assert s["korunum"]["korunum_tamam"] and s["korunum"]["mutabakat_tamam"]
    t = s["toplam"]
    assert not any(v for k, v in t.items()
                   if k.startswith("kendi.") or k.startswith("bag.karisma"))
    assert t["bag.askida_giris"] == 0 and t["bag.veri_kotu"] == 0
    assert t["bag.vaz_kayit"] > 0


def test_ESKI_CEKIRDEK_profilinde_Y4():
    """18 Kasım'ın çekirdeği: veri tetiği bağı askıda beklemeden KÖTÜ'ye
    ve cezaya götürür (Y-4)."""
    s = _kos("statik-surekli", ESKI_CEKIRDEK, DEGERLER_ESKI)
    assert s["korunum"]["korunum_tamam"] and s["korunum"]["mutabakat_tamam"]
    t = s["toplam"]
    assert t["bag.askida_giris"] == t["bag.veri_kotu"] > 0    # Y-4


def test_BELIRLENIMCI_ayni_tohum_ayni_satir(sakin):
    ikinci = _kos("statik-yok", TAM)
    assert ikinci["toplam"] == sakin["toplam"]
    a, b = sakin["satir"]["metrikler"], ikinci["satir"]["metrikler"]
    assert a == b


def test_YASAK_GOZLEM_ALANI_okunmaz():
    """KK-00 "gözlemin kullanımı": RSSI, ölçülen gürültü, konum, hız ve
    simülatörün komşu listesi okunmaz (mimari denetiminin D17'si ile aynı
    tarama, yalnız bu sürümün dosyalarında; `komsular` da eklendi)."""
    yasak = {"rssi_dbm", "olculen_gurultu_w", "kendi_konum", "kendi_hiz",
             "komsular", "phy_hata"}
    bulunan = []
    for yol in sorted((KOK / "protokoller").glob("desparete5*.py")):
        for n in ast.walk(ast.parse(yol.read_text(encoding="utf-8"))):
            ad = (n.attr if isinstance(n, ast.Attribute)
                  else n.id if isinstance(n, ast.Name)
                  and isinstance(n.ctx, ast.Load) else None)
            if ad in yasak:
                bulunan.append(f"{yol.name}:{n.lineno} {ad}")
    assert not bulunan, bulunan


def test_GECITSIZ_desende_kurulmaz():
    with pytest.raises(ValueError):
        Desparete5(1, None)
