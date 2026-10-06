"""
ADIM 2 — `sim2/dunya/` kapanış ölçütleri.

Kapanış ölçütü: *"GM hız otokorelasyonu ölçülen ρ(k) = α^k ile ±%5
(10⁴ adım). Tüm konumlar kutu içinde; sınır kuralı beyan edilmiş."*
"""

from __future__ import annotations

import math
import pathlib
import statistics as ist
import sys

import pytest

KOK = pathlib.Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.cekirdek.degismezler import DegismezHatasi  # noqa: E402
from sim2.cekirdek.rng import Akislar  # noqa: E402
from sim2.dunya.geometri import (  # noqa: E402
    Kutu, Nokta3, mesafe, yatay_mesafe, yukselis_acisi_rad)
from sim2.dunya.mobilite import (  # noqa: E402
    GaussMarkov3B, Sabit, mobilite_kur)

KUTU = Kutu(1000.0, 1000.0, 120.0)
ADIM_S = 0.5
ALFA = 0.85


def _baslangic(n: int = 40, tohum: int = 1) -> list[Nokta3]:
    a = Akislar(tohum)
    return [Nokta3(a["yerlesim"].uniform(0.0, KUTU.en_m),
                   a["yerlesim"].uniform(0.0, KUTU.boy_m),
                   a["irtifa"].uniform(0.0, KUTU.yukseklik_m))
            for _ in range(n)]


def _gm(tohum: int = 1, n: int = 40, bitis: float = 350.0) -> GaussMarkov3B:
    return GaussMarkov3B(baslangic=_baslangic(n, tohum), kutu=KUTU,
                         akislar=Akislar(tohum), kosu_bitis_s=bitis)


# ==========================================================================
# GEOMETRİ
# ==========================================================================

def test_mesafe_3B_irtifayi_hesaba_katiyor():
    a, b = Nokta3(0.0, 0.0, 0.0), Nokta3(3.0, 4.0, 12.0)
    assert mesafe(a, b) == pytest.approx(13.0)
    assert yatay_mesafe(a, b) == pytest.approx(5.0)


def test_yukselis_acisi():
    assert yukselis_acisi_rad(Nokta3(0, 0, 0), Nokta3(100, 0, 100)) == \
        pytest.approx(math.pi / 4)
    assert yukselis_acisi_rad(Nokta3(0, 0, 0), Nokta3(100, 0, 0)) == \
        pytest.approx(0.0)
    # İşaretsiz: yukarı ve aşağı bakış simetrik (dipol deseni öyle).
    assert yukselis_acisi_rad(Nokta3(0, 0, 100), Nokta3(0, 100, 0)) == \
        pytest.approx(yukselis_acisi_rad(Nokta3(0, 0, 0), Nokta3(0, 100, 100)))


@pytest.mark.parametrize("p", [
    Nokta3(-5.0, 500.0, 60.0),
    Nokta3(1005.0, 500.0, 60.0),
    Nokta3(500.0, -5.0, 60.0),
    Nokta3(500.0, 1005.0, 60.0),
    Nokta3(500.0, 500.0, -5.0),
    Nokta3(500.0, 500.0, 125.0),
])
def test_yansima_konumu_KUTUYA_geri_getiriyor(p: Nokta3):
    yeni, _az, _pit = KUTU.yansit(p, 0.3, 0.05)
    assert KUTU.icinde_mi(yeni), f"{p} → {yeni} hâlâ dışarıda"


def test_yansima_YONU_de_ceviriyor():
    """Yalnız konumu geri itmek düğümü sınıra yapıştırırdı."""
    _p, az, _pit = KUTU.yansit(Nokta3(1005.0, 500.0, 60.0), 0.0, 0.0)
    assert abs(abs(az) - math.pi) < 1e-9, "x sınırında azimut π−az olmalı"
    _p, _az, pit = KUTU.yansit(Nokta3(500.0, 500.0, 125.0), 0.0, 0.1)
    assert pit == pytest.approx(-0.1), "z sınırında pitch işaret değiştirmeli"


# ==========================================================================
# MOBİLİTE — kapanış ölçütü
# ==========================================================================

def test_gauss_markov_hiz_otokorelasyonu_alfa_ussu():
    """🔴 ADIM 2'NİN KAPANIŞ ÖLÇÜTÜ — ρ(k) = α^k, ±%5, 10⁴ adım.

    Bu tutmuyorsa model Gauss-Markov değildir; adı öyle olsa bile.
    """
    tek = GaussMarkov3B(
        baslangic=[Nokta3(500.0, 500.0, 60.0)],
        kutu=Kutu(1e9, 1e9, 1e9),          # sınırsız: yansıma otokorelasyonu bozar
        akislar=Akislar(7), kosu_bitis_s=5000.0)
    iz = tek.tik_konumlari(0)
    hiz = [mesafe(iz[i], iz[i + 1]) / ADIM_S for i in range(len(iz) - 1)]
    assert len(hiz) >= 10_000, f"yalnız {len(hiz)} adım"

    ort = ist.mean(hiz)
    var = ist.pvariance(hiz)
    for k in (1, 2, 3, 5):
        n = len(hiz) - k
        olculen = sum((hiz[i] - ort) * (hiz[i + k] - ort)
                      for i in range(n)) / n / var
        beklenen = ALFA ** k
        assert abs(olculen - beklenen) / beklenen < 0.05, (
            f"ρ({k}) = {olculen:.4f}, beklenen {beklenen:.4f}")


def test_hiz_ilan_edilen_bandda():
    gm = _gm()
    h: list[float] = []
    for d in range(40):
        iz = gm.tik_konumlari(d)
        h += [mesafe(iz[i], iz[i + 1]) / ADIM_S for i in range(len(iz) - 1)]
    assert 15.0 < ist.mean(h) < 25.0, f"ortalama hız {ist.mean(h)}"
    assert min(h) >= 0.0


def test_TUM_konumlar_kutu_icinde():
    gm = _gm()
    for d in range(40):
        for adim in range(0, 3500, 7):
            assert KUTU.icinde_mi(gm.konum(d, adim * 0.1))


def test_aradegerleme_surekli_ve_tikte_TAM_oturuyor():
    gm = _gm()
    assert mesafe(gm.konum(0, 1.0), gm.konum(0, 1.0 + 1e-6)) < 0.01
    # t = 2,0 s → tik 4 (adım 0,5 s)
    assert mesafe(gm.konum(0, 2.0), gm.tik_konumlari(0)[4]) < 1e-9


def test_kosu_bitisinden_SONRA_da_konum_veriyor():
    """Boşalma penceresi koşu bitişini aşabilir; `konum` çökmemeli."""
    gm = _gm(bitis=350.0)
    assert KUTU.icinde_mi(gm.konum(0, 400.0))


@pytest.mark.parametrize("tohum", [1, 2, 3, 17, 30])
def test_ayni_tohum_BIREBIR_ayni_yorunge(tohum: int):
    a, b = _gm(tohum), _gm(tohum)
    for d in (0, 7, 39):
        for t in (0.0, 17.3, 120.0, 349.9):
            assert mesafe(a.konum(d, t), b.konum(d, t)) < 1e-12


def test_farkli_tohum_farkli_yorunge():
    assert mesafe(_gm(1).konum(0, 100.0), _gm(2).konum(0, 100.0)) > 1.0


def test_dugumler_AYNI_yone_gitmiyor():
    """Ortalama yön düğüm başına çekilmezse sürü tek blok hâlinde kayar."""
    gm = _gm()
    yonler = []
    for d in range(40):
        iz = gm.tik_konumlari(d)
        yonler.append(math.atan2(iz[20].y - iz[0].y, iz[20].x - iz[0].x))
    # Yönler dağılmış olmalı: dairesel ortalama vektörünün boyu küçük.
    cx = ist.mean(math.cos(a) for a in yonler)
    cy = ist.mean(math.sin(a) for a in yonler)
    assert math.hypot(cx, cy) < 0.6, "düğümler tek yöne akıyor"


# ==========================================================================
# MOBİLİTE BİR EKSENDİR
# ==========================================================================

def test_sabit_kol_gercekten_hareketsiz():
    bas = _baslangic()
    s = Sabit(bas)
    assert s.hareketli is False
    for d in (0, 13, 39):
        assert mesafe(s.konum(d, 0.0), s.konum(d, 349.0)) == 0.0


def test_mobilite_bir_KONFIGURASYON_BAYRAGI():
    """Ablasyon kod düzenlemesiyle değil, bayrakla üretilir."""
    ortak = dict(baslangic=_baslangic(), kutu=KUTU,
                 akislar=Akislar(1), kosu_bitis_s=350.0)
    assert mobilite_kur(kol="statik", **ortak).hareketli is False
    assert mobilite_kur(kol="bagimsiz", **ortak).hareketli is True


def test_gecersiz_alfa_ve_adim_reddediliyor():
    ortak = dict(baslangic=_baslangic(2), kutu=KUTU,
                 akislar=Akislar(1), kosu_bitis_s=10.0)
    with pytest.raises(DegismezHatasi):
        GaussMarkov3B(alfa=1.0, **ortak)
    with pytest.raises(DegismezHatasi):
        GaussMarkov3B(adim_s=0.0, **ortak)


# ==========================================================================
# ÇALIŞMA NOKTASI — ölçülerek seçildi, testle sabitlenir
# ==========================================================================

def _derece_ve_bagli(konumlar: list[Nokta3], menzil: float) -> tuple[float, bool]:
    n = len(konumlar)
    komsu = [[j for j in range(n) if j != i
              and mesafe(konumlar[i], konumlar[j]) <= menzil] for i in range(n)]
    gor = [False] * n
    yig, say = [0], 0
    gor[0] = True
    while yig:
        u = yig.pop()
        say += 1
        for v in komsu[u]:
            if not gor[v]:
                gor[v] = True
                yig.append(v)
    return sum(len(k) for k in komsu) / n, say == n


def test_calisma_noktasi_ESKI_2B_yogunlugunu_koruyor():
    """🔒 3B'ye geçmek ağı SEYRELTİYOR — çalışma noktası bu yüzden ölçüldü.

        eski 2B (1000×1000, R=280)      : derece 7,44 · bağlı %82,9
        3B 1000×1000×300, R=280         : derece 6,13 · bağlı %62,7   🔴
        3B 1000×1000×120, R=280 (seçilen): derece 7,25 · bağlı %81,0   🟢

    Telafi edilmeseydi ölçülen şey karıştırma değil **ağın seyrelmesi**
    olurdu.
    """
    dereceler, bagli = [], 0
    for tohum in range(1, 61):
        d, b = _derece_ve_bagli(_baslangic(40, tohum), 280.0)
        dereceler.append(d)
        bagli += b
    ort = ist.mean(dereceler)
    oran = bagli / 60
    assert 6.6 < ort < 7.9, f"ortalama derece {ort:.2f} — 7,25 bekleniyordu"
    assert 0.68 < oran < 0.93, f"bağlı oran {oran:.3f} — %81 bekleniyordu"
