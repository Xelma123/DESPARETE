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
    rakip = {"aodv": kol(0.70, 1.0), "olsrv2": kol(0.72, 1.0),
             "jarmrout": kol(0.69, 1.0)}
    gelistirme = {ad: [_satir(t, 0.70 + ((t * 3 + i) % 4) / 100.0)
                       for t in range(1100, 1120)]
                  for i, ad in enumerate(("aodv", "olsrv2", "jarmrout"))}
    delta = delta_gelistirme(gelistirme, "metrikler.pdr_pencere", 40)
    assert 0.0 < delta < 0.05
    tablo = aile2_tablosu(ozgun, rakip, "metrikler.pdr_pencere", delta, True)
    assert [s.rakip for s in tablo] == ["aodv", "jarmrout", "olsrv2"]
    assert all(s.hukum == "ustun" and s.p_holm >= s.p for s in tablo)
    kapisiz = aile2_tablosu(ozgun, rakip, "metrikler.pdr_pencere", delta,
                            False)
    assert all(s.hukum == "ayirt_edilemedi" for s in kapisiz)


# --------------------------------- K-222 · açık evre PDR'si ve fark-içinde-fark
def test_K222_DONEM_PDR_evre_sozluguyle_BIREBIR():
    """Satırın `ham`ından açık/sessiz dönem PDR'si — simülatörün evre
    sözlüğüyle TAM eşit (ikinci gerçekleme); bozulunca ham denetimi konuşur."""
    sys.path.insert(0, str(KOK / "tests2"))
    from test_evre import _defter, _duzgun

    from sim2.olcum.evre import evre_sozlugu
    from sim2.olcum.rota_olaylari import RotaDefteri
    dogum = _duzgun(hiz_hz=10.0)
    acik_mi = lambda t: t >= 150.0 and ((t - 150.0) % 30.0) < 15.0
    teslim = [k for k, t in dogum if (k % 3 if acik_mi(t) else k % 10)]
    d = _defter(dogum, teslim)
    e = evre_sozlugu(d, RotaDefteri(), bas_s=50.0, acilma_s=150.0,
                     bitis_s=320.0, gecikme_p99_s=0.001, cizelge=(15.0, 15.0))
    ham = d.ham_sozluk()
    satir = {"kapsam": {"olcum_penceresi_s": [50.0, 320.0]},
             "konfig": {"karistirici_baslangic_s": 150.0},
             "metrikler": {"evre_cizelge_s": [15.0, 15.0],
                           "pdr_acik": e["pdr_acik"],
                           "pdr_sessiz": e["pdr_sessiz"],
                           "pdr_pencere": None},
             "ham": {k: list(v) if isinstance(v, tuple) else v
                     for k, v in ham.items()}}
    sonuc = ham_denetimi(satir)
    assert sonuc["pdr_acik"][2] and sonuc["pdr_sessiz"][2], sonuc
    assert sonuc["pdr_acik"][0] < sonuc["pdr_sessiz"][0]
    from analiz.satir import donem_pdr
    assert donem_pdr(satir, True, cizelge=(15.0, 15.0)) == e["pdr_acik"]


def test_DD03_GECIKME_TAVANLI_PDR_ACIK():
    """DD-03 (K-242): tavan verilince yalnız gecikmesi tavanı aşmayan
    teslimler sayılır; tavansız hâl birincil metrikle aynı."""
    from analiz.satir import donem_pdr, donem_sayim
    satir = {"kapsam": {"olcum_penceresi_s": [50.0, 320.0]},
             "konfig": {"karistirici_baslangic_s": 150.0},
             "metrikler": {"evre_cizelge_s": [15.0, 15.0]},
             "ham": {"dogum_s": [151.0, 152.0, 160.0, 170.0],
                     "teslim_dogum_s": [151.0, 152.0, 170.0],
                     "teslim_gecikmeleri_s": [0.5, 3.0, 1.0]}}
    assert donem_sayim(satir) == (2, 3)
    assert donem_sayim(satir, tavan_s=60.0) == (2, 3)
    assert donem_sayim(satir, tavan_s=2.0) == (1, 3)
    assert donem_pdr(satir, tavan_s=0.4) == 0.0
    assert donem_pdr(satir, acik=False, tavan_s=2.0) == 1.0
    with pytest.raises(AnalizHatasi):
        donem_sayim(satir, tavan_s=0.0)


def _did_satiri(tohum, sayim, cizelge=(15.0, 15.0), arac="a",
                acilma=150.0, evren=None, kurulum="k"):
    s = _satir(tohum, 0.5, arac=arac, kurulum=kurulum, evren=evren)
    s["konfig"]["karistirici_baslangic_s"] = acilma
    s["kapsam"] = {"olcum_penceresi_s": [50.0, 320.0]}
    if cizelge is not None:
        s["metrikler"]["evre_cizelge_s"] = list(cizelge)
    s["turetilen_sayim"] = sayim
    return s


def test_K222_FARK_ICINDE_FARK_karistirmaya_ozgu_kazanci_AYIRIR(monkeypatch):
    """Özgün protokol her hücrede rakipten 0,10 iyi (karıştırmadan bağımsız
    üstünlük) → DiD tam sıfır; birincilde ek kazanç → DiD > 0 ve anlamlı.
    DD-08 (K-242): DiD sayılardan kesirle — sıfır vaka tam sıfırdır."""
    from analiz import hucre as H
    from analiz.hucre import fark_icinde_fark_tablosu

    monkeypatch.setattr(H, "donem_sayim",
                        lambda s, acik=True, cizelge=None: s["turetilen_sayim"])
    monkeypatch.setattr(H, "donem_pdr", lambda s, acik=True, cizelge=None:
                        s["turetilen_sayim"][0] / s["turetilen_sayim"][1])
    tohumlar = range(2000, 2040)
    g = lambda t: (t * 7) % 5

    def kol(fn, ikiz=False):
        return [_did_satiri(t, (fn(t), 997),
                            cizelge=None if ikiz else (15.0, 15.0),
                            kurulum="ki" if ikiz else "kb")
                for t in tohumlar]
    D_b, R_b = kol(lambda t: 601 + g(t)), kol(lambda t: 501 + g(t))
    D_i = kol(lambda t: 901 + g(t), ikiz=True)
    R_i = kol(lambda t: 801 + g(t), ikiz=True)
    sifir = fark_icinde_fark_tablosu(D_b, {"aodv": R_b}, D_i, {"aodv": R_i})
    assert sifir[0].ort == 0.0 and sifir[0].yontem == "tum_sifir"
    assert sifir[0].p_holm == 1.0
    D_b2 = kol(lambda t: 651 + g(t) + (t * 3) % 4)
    ozgu = fark_icinde_fark_tablosu(D_b2, {"aodv": R_b}, D_i, {"aodv": R_i},
                                    (15.0, 15.0))
    assert ozgu[0].ort > 0.04 and ozgu[0].p_holm < 0.05


def test_DD08_FARK_ICINDE_FARK_birincil_ve_ikizin_UYUMUNU_denetler(
        monkeypatch):
    """DD-08 (K-242): farklı kod, açılma anı, çizelge ya da paket evreniyle
    koşulmuş ikiz kabul edilmez."""
    from analiz import hucre as H
    from analiz.hucre import fark_icinde_fark_tablosu

    monkeypatch.setattr(H, "donem_sayim",
                        lambda s, acik=True, cizelge=None: s["turetilen_sayim"])
    monkeypatch.setattr(H, "donem_pdr", lambda s, acik=True, cizelge=None:
                        s["turetilen_sayim"][0] / s["turetilen_sayim"][1])
    tohumlar = range(2000, 2010)

    def kol(n, ikiz=False, **ek):
        return [_did_satiri(t, (n + t % 3, 100),
                            cizelge=None if ikiz else (15.0, 15.0),
                            kurulum="ki" if ikiz else "kb", **ek)
                for t in tohumlar]
    D_b, R_b = kol(60), kol(50)
    D_i, R_i = kol(90, True), kol(80, True)
    assert fark_icinde_fark_tablosu(D_b, {"aodv": R_b}, D_i, {"aodv": R_i})
    for ikiz_D, ikiz_R in ((kol(90, True, arac="b"), kol(80, True, arac="b")),
                           (kol(90, True, acilma=100.0),
                            kol(80, True, acilma=100.0)),
                           (kol(90, True, evren="baska"),
                            kol(80, True, evren="baska"))):
        with pytest.raises(AnalizHatasi):
            fark_icinde_fark_tablosu(D_b, {"aodv": R_b}, ikiz_D,
                                     {"aodv": ikiz_R})
    with pytest.raises(AnalizHatasi):
        fark_icinde_fark_tablosu(D_b, {"aodv": R_b}, D_i, {"aodv": R_i},
                                 (20.0, 10.0))
