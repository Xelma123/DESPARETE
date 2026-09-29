"""
🔴 KURULUM KALİBRASYONUNUN KENDİ TESTLERİ (B-08 / K-039).

`dogrulama/kurulum_kalibrasyonu.py` projenin BİRİNCİL ÇALIŞMA NOKTASINI
seçen sayıyı üretiyor. Testi olmayan bir karar aracı, Y7'nin bu projede
beş kez tekrarlanan hatasıdır: *"bir doğrulama aracı ne koştuğunu kendisi
doğrulamak zorunda."*

Burada iki şey sınanıyor:
  1. KARAR ÜRETEN YÜKLEMLER — `eski_olcut` / `yeni_olcut` (03 B5: analiz
     kodunun karar yüklemleri ayrı ve test edilebilir yazılır)
  2. GRAF ÇEKİRDEĞİ — `_mesafe_matrisi` / `_bag_matrisi`
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dogrulama.kurulum_kalibrasyonu import (  # noqa: E402
    ULASILABILIRLIK_YOK,
    _bag_matrisi, _mesafe_matrisi, eski_olcut, yeni_olcut,
)
from sim.config import Konfig  # noqa: E402
from sim.radio import Karistirici, Radyo, dbm_to_w  # noqa: E402
from sim.topology import Topoloji  # noqa: E402


# ==========================================================================
# Karar üreten yüklemler
# ==========================================================================

def test_eski_olcut_ulasilabilirlik_tabanina_uyuyor():
    """%90 tabanını sağlamayan hiçbir güç seçilemez — sapma ne olursa olsun."""
    satirlar = [
        (0.0, 95.0, 1.0, 30.0, 1.0),
        (2.0, 92.0, 1.0, 40.0, 1.0),
        (4.0, 89.9, 1.0, 99.0, 1.0),   # en yüksek sapma AMA taban altında
    ]
    secim = eski_olcut(satirlar)
    assert secim[0] == 2.0, secim
    assert eski_olcut([(4.0, 50.0, 1.0, 99.0, 1.0)]) is None


def test_eski_olcut_sapma_en_buyugu_seciyor():
    satirlar = [(0.0, 99.0, 1.0, 30.0, 1.0), (2.0, 95.0, 1.0, 44.0, 1.0),
                (4.0, 91.0, 1.0, 49.0, 1.0)]
    assert eski_olcut(satirlar)[0] == 4.0


def test_yeni_olcut_dinamik_araligin_ortasini_seciyor():
    """K-039'un ölçütü: teslim, taban–tavan aralığının ortasına en yakın."""
    egri = [(-10.0, 0.90), (0.0, 0.70), (2.0, 0.52), (4.0, 0.36), (11.0, 0.12)]
    taban, tavan, orta, secim = yeni_olcut(egri, ULASILABILIRLIK_YOK)
    assert (taban, tavan) == (0.12, 0.90)
    assert orta == pytest.approx(0.51, abs=0.0, rel=1e-12)
    assert secim[0] == 2.0, secim


def test_yeni_olcut_tavana_yakini_secmiyor():
    """Y6 — ölçüt gerçekten ayırt ediyor mu? Eğriyi kaydırınca seçim kaymalı."""
    egri = [(-10.0, 0.90), (0.0, 0.51), (2.0, 0.20), (11.0, 0.12)]
    _, _, _, secim = yeni_olcut(egri, ULASILABILIRLIK_YOK)
    assert secim[0] == 0.0, "eğri kaydı ama seçim kaymadı — ölçüt duyarsız"


# ==========================================================================
# Graf çekirdeği
# ==========================================================================

def test_mesafe_matrisi_bilinen_zincirde_dogru():
    """0→1→2→3 zinciri: mesafeler 0,1,2,3; geri yön ulaşılamaz."""
    n = 4
    bag = np.zeros((n, n), bool)
    for i in range(n - 1):
        bag[i, i + 1] = True          # YALNIZ ileri yön
    d = _mesafe_matrisi(bag)
    assert list(d[0]) == [0, 1, 2, 3]
    assert list(d[3]) == [-1, -1, -1, 0]      # geriye gidilemez
    assert d[2, 0] == -1


def test_bag_matrisi_karistiriciyla_yonlu_hale_geliyor():
    """🔴 Karıştırıcı ALICIYI etkiler → u→v ile v→u ayrışabilir.

    Bu, tablonun yönlü grafla hesaplanmasının gerekçesidir. Simetrik bir
    graf kullanılsaydı, karıştırıcıya yakın bir düğümün HÂLÂ gönderebildiği
    ama ALAMADIĞI durum görünmezdi.
    """
    kon = Konfig(kol="t", senaryo="S2")
    radyo = Radyo.kur(kon)
    merkez = kon.karistirici_merkez
    # 0 karıştırıcının dibinde, 1 uzakta ama menzil içinde
    topo = Topoloji(
        konumlar=((merkez[0], merkez[1]), (merkez[0] + 200.0, merkez[1])),
        iletim_menzili_m=kon.iletim_menzili_m,
        girisim_menzili_m=kon.girisim_menzili_m)
    kj = Karistirici(
        guc_w=dbm_to_w(2.0), konum=merkez,
        yol_kaybi_usteli=kon.yol_kaybi_usteli, frekans_hz=kon.frekans_hz,
        darbeli=False, periyot_s=kon.darbe_periyodu_s,
        gorev_cevrimi=kon.darbe_gorev_cevrimi, faz_kesri=0.0,
        hareketli=False, hiz_ms=kon.karistirici_hiz_ms,
        yorunge_yaricap_m=kon.karistirici_yorunge_yaricap_m)

    esik = radyo.menzilde_per(kon.iletim_menzili_m, kon.paket_bayt)
    bag = _bag_matrisi(topo, radyo, kon, kj, esik)
    assert bag[0, 1] != bag[1, 0], (
        f"karıştırıcı yanındaki düğümde yön asimetrisi YOK: "
        f"0→1={bag[0,1]} 1→0={bag[1,0]} — graf yönlü hesaplanmıyor olabilir"
    )
    # Karıştırıcının dibindeki 0'a gönderim bozulmalı, 0'dan gönderim değil
    assert bag[1, 0] is np.False_ or not bag[1, 0]
    assert bag[0, 1]


def test_bag_matrisi_karistiricisiz_simetrik():
    """Kontrol kolu: karıştırıcı yokken graf simetrik olmalı."""
    kon = Konfig(kol="t", senaryo="S0", tohum=1)
    radyo = Radyo.kur(kon)
    from sim.rng import Akislar
    topo = Topoloji.uret(kon, Akislar(1))
    esik = radyo.menzilde_per(kon.iletim_menzili_m, kon.paket_bayt)
    bag = _bag_matrisi(topo, radyo, kon, None, esik)
    assert np.array_equal(bag, bag.T), "karıştırıcısız graf simetrik değil"


# ==========================================================================
# 🔴 B-29 — YENİ ÖLÇÜTÜN ULAŞILABİLİRLİK KISITI
#
# K-039 ölçütü İKİ koşulla ilan etti ve *"Uygulandığında (kod, proza değil)"*
# dedi — ama `yeni_olcut` ulaşılabilirliği **argüman olarak bile almıyordu**.
# İkinci bağımsız denetim kırdı:
#     yeni_olcut([(-10,.90),(0,.70),(6,.51),(11,.12)]) -> +6 dBm
# +6 dBm'in ölçülen ulaşılabilirliği %84,8 — ilan edilen tabanın altında.
#
# Ve `tests/test_kalibrasyon.py`nin 7 testinden hiçbiri bunu sormuyordu;
# yalnızca ESKİ ölçüt için soruyordu.
# ==========================================================================

def test_b29_yeni_olcut_ulasilabilirlik_tabanina_uyuyor():
    """Taban altındaki bir güç, ortaya en yakın olsa bile SEÇİLEMEZ."""
    from dogrulama.kurulum_kalibrasyonu import ULASILABILIRLIK_TABANI

    egri = [(-10.0, 0.90), (0.0, 0.70), (6.0, 0.51), (11.0, 0.12)]
    # Kısıtsız: +6 dBm (denetçinin kırdığı vaka)
    assert yeni_olcut(egri, ULASILABILIRLIK_YOK)[3][0] == 6.0

    # Kısıtlı: +6 elenmeli
    ulasim = {-10.0: 99.8, 0.0: 97.9, 6.0: 84.8, 11.0: 52.9}
    assert yeni_olcut(egri, ulasim)[3][0] == 0.0
    assert ULASILABILIRLIK_TABANI == 90.0


def test_b29_hicbir_guc_tabani_saglamazsa_HATA():
    """Y7 — sessizce bir nokta seçmektense açıkça patla."""
    egri = [(0.0, 0.70), (6.0, 0.51)]
    with pytest.raises(ValueError):
        yeni_olcut(egri, {0.0: 50.0, 6.0: 40.0})


def test_b29_dinamik_aralik_TARAMANIN_TAMAMINDAN_okunuyor():
    """Kısıt seçilebilirliği daraltır, ölçüm eksenini DEĞİL.

    Aralık yalnızca uygun alt kümeden okunsaydı, kısıt orta noktayı da
    kaydırırdı ve ölçüt kendi tanımını değiştirmiş olurdu.
    """
    egri = [(-10.0, 0.90), (0.0, 0.70), (6.0, 0.51), (11.0, 0.12)]
    taban_k, tavan_k, orta_k, _ = yeni_olcut(egri, ULASILABILIRLIK_YOK)
    taban_s, tavan_s, orta_s, _ = yeni_olcut(
        egri, {-10.0: 99.8, 0.0: 97.9, 6.0: 84.8, 11.0: 52.9})
    assert (taban_k, tavan_k, orta_k) == (taban_s, tavan_s, orta_s)
    assert taban_s == 0.12 and tavan_s == 0.90


# ==========================================================================
# 🔴 B-71 (K-056) — NÖBETÇİ VE HARİTA KAPSAMI
#
# B-60'ın nöbetçisi üç yoldan atlanıyordu; biri SESSİZCE çalışma noktasını
# değiştiriyordu (`0` anahtarı eksik → +(-10) dBm seçiliyordu).
# ==========================================================================

def test_b71_EKSIK_ulasilabilirlik_anahtari_reddediliyor():
    """Eksik anahtar `.get(g, 0.0)` ile SESSİZCE eleme demekti."""
    egri = [(-10, .90), (0, .70), (6, .51), (11, .12)]
    tam = {-10: 99., 0: 97., 6: 84.8, 11: 60.}
    assert yeni_olcut(egri, tam)[3] == (0, .70)

    eksik = {-10: 99., 6: 84.8, 11: 60.}          # `0` yok
    with pytest.raises(ValueError, match="kapsamıyor"):
        yeni_olcut(egri, eksik)


def test_b71_nobetci_DIZGI_DEGIL_tekil_nesne():
    """🔴 CPython interning: düz bir dizgi literali nöbetçi sayılamamalı.

    Önceki nöbetçi `"__ULASILABILIRLIK_YOK__"` dizgisiydi; aynı literal
    interning yüzünden `is` testini GEÇİYORDU ve kısıt sessizce atlanıp
    B-29'un engellemek için yazıldığı +6 dBm seçiliyordu.
    """
    assert not isinstance(ULASILABILIRLIK_YOK, str)
    egri = [(-10, .90), (0, .70), (6, .51), (11, .12)]
    with pytest.raises((ValueError, AttributeError, TypeError)):
        yeni_olcut(egri, "__ULASILABILIRLIK_YOK__")

    # ve gerçek nöbetçi hâlâ çalışıyor
    assert yeni_olcut(egri, ULASILABILIRLIK_YOK)[3] == (6, .51)
