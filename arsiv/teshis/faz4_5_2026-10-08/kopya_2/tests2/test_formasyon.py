"""
Y6 — formasyon kolu ve istasyon tutma.

Şartname: `v2/07-SIMULATOR-TASARIMI.md` §18 Y6 (öğrenci onayı 11 Eylül 2026).
Karar kaydı: `v2/04` K-118.

Onaylı yapının kapıları:
  · t = 0 konumları statik kolla AYNI — istasyonlar yerleşim çekimleridir
  · istasyondan sapma sınırlı, bütün konumlar kutuda
  · aynı tohumda birebir aynı yörünge

🔴 "DUVARA TEMAS 0" KAPISI KATI HÂLİYLE TUTMADI — ölçüldü.
Prototip (10 tohum × 350 s, gürültü akışı taklit): 280 400 düğüm-tikin 59'unda
temas (%0,021), 400 düğümün 12'sinde. İstasyonu tabana ya da tavana birkaç
metre yakın düşen düğüm, manevra gürültüsüyle arada bir sınıra değip yansıyor.
Kapı burada "temas nadir ve SAYILIYOR" biçiminde; sayaç ayrıca sınanıyor —
hep sıfır dönen bir sayaç "nadir" kapısını kendiliğinden geçerdi.
"""

from __future__ import annotations

import pathlib
import statistics as ist
import sys

import pytest

KOK = pathlib.Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.cekirdek.degismezler import DegismezHatasi  # noqa: E402
from sim2.cekirdek.rng import Akislar  # noqa: E402
from sim2.dunya.geometri import Kutu, Nokta3, mesafe  # noqa: E402
from sim2.dunya.mobilite import Formasyon3B  # noqa: E402
from sim2.dunya.topoloji import topoloji_kur  # noqa: E402
from sim2.dunya.yerlesim import kutu_kur  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402
from sim2.yapilandirma.senaryolar import (  # noqa: E402
    KARISTIRICI_SINIFLARI, SENARYOLAR)

TOHUMLAR = range(1000, 1005)


def _konfig(tohum: int = 1000, senaryo: str = "formasyon-yok", **ek) -> Konfig:
    return Konfig(kol="t", senaryo=senaryo, tohum=tohum, **ek)


def _top(tohum: int = 1000, senaryo: str = "formasyon-yok", **ek):
    return topoloji_kur(_konfig(tohum, senaryo, **ek), Akislar(tohum))


def _olcum(tohum: int) -> tuple[list[float], int, int]:
    """(istasyondan sapmalar, duvar teması, düğüm-tik) — konumların hepsi kutuda."""
    k = _konfig(tohum)
    m = topoloji_kur(k, Akislar(tohum)).mobilite
    kutu = kutu_kur(k)
    sapma: list[float] = []
    for i in range(k.dugum_sayisi):
        for j, p in enumerate(m.tik_konumlari(i)):
            assert kutu.icinde_mi(p), f"düğüm {i} tik {j} kutu dışında: {p}"
            sapma.append(mesafe(p, m.istasyon_konumu(i, j * k.gm_adim_s)))
    return sapma, m.duvar_temasi, k.dugum_sayisi * (m.tik_sayisi - 1)


def test_Y6_formasyon_bir_MOBILITE_KOLU():
    k = _konfig(senaryo="formasyon-surekli")
    assert k.mobilite_kolu == "formasyon" and k.hareketli
    assert {f"formasyon-{j}" for j in KARISTIRICI_SINIFLARI} <= set(SENARYOLAR)
    m = _top().mobilite
    assert isinstance(m, Formasyon3B)
    assert m.hareketli and m.mobilite_kolu == "formasyon"


def test_Y6_t0_konumlari_STATIK_KOLLA_AYNI():
    """İstasyonlar yerleşim çekimleridir; yoğunluk eşitlemesi bu yüzden gereksiz."""
    for t in TOHUMLAR:
        f, s = _top(t), _top(t, "statik-yok")
        for i in range(f.dugum_sayisi):
            assert f.konum(i, 0.0) == s.konum(i, 0.0)
            assert f.mobilite.istasyon_konumu(i, 0.0) == s.konum(i, 0.0)


def test_Y6_istasyondan_SAPMA_SINIRLI_ve_hepsi_KUTUDA():
    """Prototip: ortalama 0,87 m · p99 1,92 m · en büyük 2,83 m (10 tohum)."""
    tum: list[float] = []
    for t in TOHUMLAR:
        tum.extend(_olcum(t)[0])
    assert max(tum) < 10.0, f"en büyük sapma {max(tum):.2f} m"
    assert ist.mean(tum) < 2.0, f"ortalama sapma {ist.mean(tum):.2f} m"


def test_Y6_duvar_temasi_NADIR():
    temas = toplam = 0
    for t in TOHUMLAR:
        _, d, n = _olcum(t)
        temas += d
        toplam += n
    assert temas / toplam < 1e-3, f"temas payı %{100 * temas / toplam:.3f}"


def test_Y6_duvar_temasi_SAYACI_calisiyor():
    """İstasyonu tam tabanda olan düğüm sınıra değer; sayaç bunu görmeli."""
    kutu = Kutu(100.0, 100.0, 50.0)
    m = Formasyon3B(baslangic=[Nokta3(50.0, 50.0, 0.0)], kutu=kutu,
                    akislar=Akislar(1), kosu_bitis_s=50.0, alfa=0.85,
                    adim_s=0.5, hiz_maks_ms=5.0, hiz_sigma_ms=1.0)
    assert m.duvar_temasi > 0
    assert all(kutu.icinde_mi(p) for p in m.tik_konumlari(0))


def test_Y6_ayni_tohum_BIREBIR():
    a, b = _top(1003).mobilite, _top(1003).mobilite
    for i in range(_konfig().dugum_sayisi):
        assert a.tik_konumlari(i) == b.tik_konumlari(i)
    assert a.duvar_temasi == b.duvar_temasi


def test_Y6_istasyon_KAYMASI_sifirda_SABIT_pozitifte_KAYAR():
    """Keşifsel eksen. 🔒 Yön çekimi kaymadan bağımsız: gürültü dizisi aynı."""
    a0, a1 = Akislar(1000), Akislar(1000)
    m0 = topoloji_kur(_konfig(), a0).mobilite
    m1 = topoloji_kur(_konfig(istasyon_kayma_hiz_ms=0.05), a1).mobilite
    assert a0["formasyon_jitter"].random() == a1["formasyon_jitter"].random(), (
        "kayma hızı akıştan çekilen sayı adedini değiştirmemeli")
    kutu = kutu_kur(_konfig())
    kayan: list[float] = []
    for i in range(_konfig().dugum_sayisi):
        assert m0.istasyon_konumu(i, 0.0) == m0.istasyon_konumu(i, 350.0)
        assert m1.istasyon_konumu(i, 0.0) == m0.istasyon_konumu(i, 0.0)
        son = m1.istasyon_konumu(i, 350.0)
        assert kutu.icinde_mi(son)
        kayan.append(mesafe(m1.istasyon_konumu(i, 0.0), son))
    assert max(kayan) <= 0.05 * 350.0 + 1e-9
    assert max(kayan) > 10.0
    with pytest.raises(DegismezHatasi):
        _konfig(istasyon_kayma_hiz_ms=-0.1)
