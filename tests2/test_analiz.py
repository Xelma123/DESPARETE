"""
`analiz/` — ön-kaydın analiz planı (`v2/06` §0.4, §7) · K-184.

Sınanan: Wilcoxon (kesin/yaklaşık, NaN tuzağı), Holm, δ, GA, hüküm, güç,
eşleştirme kimlik denetimi ve ham ikinci gerçekleme — sonuncusu GERÇEK bir
koşu satırında simülatörün kendi sayılarına karşı.
"""

from __future__ import annotations

import ast
import copy
import math
import pathlib
import sys

import pytest

KOK = pathlib.Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from analiz.istatistik import (AnalizHatasi, delta_esigi, guc_egrisi,  # noqa: E402
                               holm, hukum, mde80, ortalama_fark_ga,
                               wilcoxon_eslestirilmis)
from analiz.satir import eslestir, gecerli_suz, ham_denetimi, yuzdelik  # noqa: E402


# --------------------------------------------------------------- mimari
def test_analiz_SIMULATORDEN_HICBIR_SEY_ice_aktarmaz():
    """`olcum/metrikler.py` başlığı: `analiz/` JSONL üzerinde çalışır."""
    for dosya in (KOK / "analiz").glob("*.py"):
        agac = ast.parse(dosya.read_text(encoding="utf-8"))
        for dugum in ast.walk(agac):
            if isinstance(dugum, ast.Import):
                adlar = [a.name for a in dugum.names]
            elif isinstance(dugum, ast.ImportFrom):
                adlar = [dugum.module or ""]
            else:
                continue
            for ad in adlar:
                assert not ad.split(".")[0] in ("sim2", "protokoller",
                                                "kalibrasyon"), (dosya, ad)


# ------------------------------------------------------------ Wilcoxon
def test_wilcoxon_KESIN_dagilim_bilinen_deger():
    """On pozitif fark, bağsız: çift yönlü kesin p = 2 / 2¹⁰."""
    s = wilcoxon_eslestirilmis([float(i) for i in range(1, 11)], [0.0] * 10)
    assert s.yontem == "kesin" and s.p == pytest.approx(2 / 2 ** 10)
    assert s.ort_fark == pytest.approx(5.5)


def test_wilcoxon_BAGDA_yaklasik():
    s = wilcoxon_eslestirilmis([1.0, 1.0, 2.0, -1.0, 3.0], [0.0] * 5)
    assert s.yontem == "yaklasik" and 0.0 < s.p <= 1.0


def test_NAN_TUZAGI_tum_sifir_farklar_p_BIR_ve_holm_NAN_ALMAZ():
    s = wilcoxon_eslestirilmis([0.5] * 40, [0.5] * 40)
    assert s.tum_sifir and s.p == 1.0 and s.yontem == "tum_sifir"
    with pytest.raises(AnalizHatasi):
        holm([0.01, float("nan"), 0.2])
    with pytest.raises(AnalizHatasi):
        wilcoxon_eslestirilmis([1.0, float("nan")], [0.0, 0.0])


# ---------------------------------------------------------------- Holm
def test_holm_BILINEN_ornek_ve_MONOTON():
    assert holm([0.01, 0.04, 0.03]) == pytest.approx([0.03, 0.06, 0.06])
    assert holm([0.5, 0.9]) == pytest.approx([1.0, 1.0])
    d = holm([0.001, 0.2, 0.01, 0.04])
    sirali = sorted(zip([0.001, 0.2, 0.01, 0.04], d))
    assert all(a[1] <= b[1] for a, b in zip(sirali, sirali[1:]))


# ------------------------------------------------------- δ · GA · hüküm
def test_delta_EN_GURULTULU_cift_ve_formul():
    d = {"a": [0.0, 0.02], "b": [0.0, 0.10]}
    sd = math.sqrt(((0.05) ** 2 + (0.05) ** 2) / 1)
    assert delta_esigi(d, 40) == pytest.approx(2 * sd / math.sqrt(40))


def test_GA_TOHUMLA_belirlenimci_ve_ORTALAMAYI_kapsar():
    x = [0.8 + 0.01 * (i % 7) for i in range(40)]
    y = [0.75 + 0.01 * (i % 5) for i in range(40)]
    a = ortalama_fark_ga(x, y, tohum=3)
    assert a == ortalama_fark_ga(x, y, tohum=3)
    assert a[1] <= a[0] <= a[2]


@pytest.mark.parametrize("p, fark, kapi, beklenen", [
    (0.01, 0.06, True, "ustun"), (0.01, 0.06, False, "ayirt_edilemedi"),
    (0.01, 0.02, True, "ayirt_edilemedi"), (0.01, -0.06, True, "asagi"),
    (0.20, 0.06, True, "ayirt_edilemedi")])
def test_HUKUM_tablosu(p, fark, kapi, beklenen):
    assert hukum(p, fark, 0.05, kapi) == beklenen


# ----------------------------------------------------------------- güç
def test_GUC_merkezlenmemis_gurultuyu_REDDEDER_ve_egri_ARTAR():
    with pytest.raises(AnalizHatasi):
        guc_egrisi([0.1, 0.2, 0.3], 10, [0.0])
    g = [(-1) ** i * 0.01 * (1 + i % 3) for i in range(20)]
    ort = sum(g) / len(g)
    g = [v - ort for v in g]
    egri = guc_egrisi(g, 40, [0.0, 0.01, 0.05], b=300, tohum=1)
    assert egri[0.0] <= 0.05 and egri[0.05] == 1.0
    assert egri[0.0] <= egri[0.01] <= egri[0.05]
    assert mde80({0.0: 0.0, 0.02: 0.6, 0.04: 1.0}) == pytest.approx(0.03)
    assert mde80({0.0: 0.0, 0.02: 0.5}) is None


# ----------------------------------------------------------- eşleştirme
def _satir(tohum, deger, arac="a", kurulum="k", evren=None, gecerli=True):
    return {"kimlik": {"tohum": tohum, "protokol": "p", "arac_hash": arac,
                       "kurulum_hash": kurulum,
                       "evren_hash": evren or f"e{tohum}"},
            "konfig": {"senaryo": "s", "tehdit_senaryosu": "t",
                       "trafik_deseni": "d"},
            "korunum": {"gecerli": gecerli, "korunum_tamam": gecerli},
            "metrikler": {"pdr_pencere": deger}}


def test_ESLESTIRME_kimlik_denetimi_SESSIZ_GECMEZ():
    a = [_satir(t, 0.9) for t in range(3)]
    b = [_satir(t, 0.8) for t in range(3)]
    t, x, y, dusen = eslestir(a, b, "metrikler.pdr_pencere")
    assert t == [0, 1, 2] and x == [0.9] * 3 and dusen == []
    with pytest.raises(AnalizHatasi):
        eslestir(a, [_satir(0, 0.8, arac="b")], "metrikler.pdr_pencere")
    with pytest.raises(AnalizHatasi):
        eslestir(a, [_satir(0, 0.8, evren="baska")], "metrikler.pdr_pencere")
    with pytest.raises(AnalizHatasi):
        eslestir(a, [_satir(0, None)], "metrikler.pdr_pencere")
    g, d = gecerli_suz([_satir(0, 0.9), _satir(1, 0.9, gecerli=False)])
    assert len(g) == 1 and d[0]["tohum"] == 1


# ---------------------------------------------- ham — İKİNCİ GERÇEKLEME
def test_HAM_denetimi_GERCEK_satirda_SIMULATORLE_birebir():
    """Kısa bir gerçek koşu: `ham`dan yeniden üretilen pencere PDR'si,
    gecikme yüzdelikleri ve görev teslim oranı satırdakiyle TAM eşit."""
    sys.path.insert(0, str(KOK / "tests2"))
    from test_kosum import _kos                       # noqa: E402
    from sim2.kosum.sonuc import sonuc_satiri         # noqa: E402
    kur, kosu = _kos("bagimsiz-yok", "enyakin", bitis=5.0,
                     kayip_dugum_sayisi=4, kayip_bas_s=1.5, kayip_bitis_s=3.5)
    satir = sonuc_satiri(kur, kosu.dugumler, "en_yakin_kimlik")
    sonuc = ham_denetimi(satir)
    assert set(sonuc) >= {"pdr_pencere", "gecikme_p95_s_pencere",
                          "gorev_teslim_orani_pencere"}
    for ad, (sat, ham, tutuyor) in sonuc.items():
        assert tutuyor, (ad, sat, ham)
    assert satir["metrikler"]["pdr_pencere"] > 0.0, "test boş değil"
    bozuk = copy.deepcopy(satir)
    bozuk["ham"]["teslim_dogum_s"] = []
    assert not ham_denetimi(bozuk)["pdr_pencere"][2]


def test_yuzdelik_IKINCI_gerceklemesi_metriklerle_AYNI():
    from sim2.olcum.metrikler import yuzdelik as asil
    ornek = [0.3, 0.1, 0.7, 0.2, 0.9, 0.4, 0.05]
    for p in (0, 50, 95, 99, 100):
        assert yuzdelik(ornek, p) == asil(ornek, p)
    assert yuzdelik([], 50) is None


# ------------------------------------------------------ hücre koşucusu
def test_HUCRE_aile2_tablosu_HUKUM_ve_HOLM():
    """K-189: özgün her rakipten tutarlı biçimde iyiyse üstün; mekanizma
    kapısı kapalıysa ayırt edilemedi; δ geliştirme farklarından."""
    from analiz.hucre import aile2_tablosu, delta_gelistirme
    tohumlar = range(2000, 2040)

    def kol(taban, egim):
        return [_satir(t, taban + egim * ((t * 7) % 5) / 100.0)
                for t in tohumlar]
    ozgun = kol(0.80, 1.0)
    rakip = {"aodv": kol(0.70, 1.0), "olsr": kol(0.72, 1.0),
             "aomdv": kol(0.69, 1.0)}
    gelistirme = {ad: [_satir(t, 0.70 + ((t * 3 + i) % 4) / 100.0)
                       for t in range(1100, 1120)]
                  for i, ad in enumerate(("aodv", "olsr", "aomdv"))}
    delta = delta_gelistirme(gelistirme, "metrikler.pdr_pencere", 40)
    assert 0.0 < delta < 0.05
    tablo = aile2_tablosu(ozgun, rakip, "metrikler.pdr_pencere", delta, True)
    assert [s.rakip for s in tablo] == ["aodv", "aomdv", "olsr"]
    assert all(s.hukum == "ustun" and s.p_holm >= s.p for s in tablo)
    kapisiz = aile2_tablosu(ozgun, rakip, "metrikler.pdr_pencere", delta,
                            False)
    assert all(s.hukum == "ayirt_edilemedi" for s in kapisiz)
