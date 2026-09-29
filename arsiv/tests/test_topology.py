"""
Topoloji testleri.

Bu modül SENARYO KURULUMUDUR. Buradaki bir hata, tüm koşuların hangi ağda
yapıldığını değiştirir — ve fark edilmesi çok zordur çünkü sonuçlar yine
makul görünür.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sim.config import Konfig  # noqa: E402
from sim.rng import Akislar  # noqa: E402
from sim.topology import Topoloji  # noqa: E402


def _topo(tohum: int = 1, **kw) -> tuple[Topoloji, Konfig]:
    kon = Konfig(kol="test", tohum=tohum, **kw)
    return Topoloji.uret(kon, Akislar(tohum)), kon


def test_ayni_tohum_ayni_topoloji():
    a, _ = _topo(7)
    b, _ = _topo(7)
    assert a.konumlar == b.konumlar


def test_farkli_tohum_farkli_topoloji():
    a, _ = _topo(7)
    b, _ = _topo(8)
    assert a.konumlar != b.konumlar


def test_topoloji_protokol_kesfinden_etkilenmiyor():
    """🔴 EŞLEŞTİRMENİN TEMELİ.

    Bir protokolün kaç rastgele sayı çektiği topolojiyi DEĞİŞTİRMEMELİ.
    Değiştirseydi, keşif yapan kol ile yapmayan kol farklı ağlarda ölçülürdü.
    """
    kon = Konfig(kol="test", tohum=1000)

    a1 = Akislar(1000)
    t1 = Topoloji.uret(kon, a1)

    a2 = Akislar(1000)
    for _ in range(10_000):
        a2["protokol_kesif"].random()
        a2["mac_geri_cekilme"].random()
    t2 = Topoloji.uret(kon, a2)

    assert t1.konumlar == t2.konumlar


@pytest.mark.parametrize("tohum", range(1, 21))
def test_kosullama_her_zaman_bagli_uretiyor(tohum):
    topo, _ = _topo(tohum)
    assert len(topo.bagli_bilesenler()) == 1, (
        f"tohum {tohum}: koşullamaya rağmen kopuk topoloji"
    )
    assert topo.ozet()["en_buyuk_bilesen"] == topo.dugum_sayisi


def test_kosullama_kapatilinca_kopuk_topoloji_kabul_ediliyor():
    """Koşullamanın gerçekten bir şey yaptığını göster.

    Bayrak kapatıldığında en az bir tohumda kopuk topoloji çıkmalı;
    çıkmıyorsa bayrak hiçbir işe yaramıyor demektir. (bildirim ≠ kullanım)
    """
    kopuk = 0
    for tohum in range(1, 31):
        kon = Konfig(kol="t", tohum=tohum, baglanti_kosullamasi=False)
        topo = Topoloji.uret(kon, Akislar(tohum))
        if len(topo.bagli_bilesenler()) > 1:
            kopuk += 1
    assert kopuk > 0, "bağlantı koşullaması bayrağı hiçbir şey değiştirmiyor"


def test_girisim_menzili_iletimden_genis():
    """Li replikasyonunun ön koşulu."""
    topo, kon = _topo(1)
    assert topo.girisim_menzili_m > topo.iletim_menzili_m
    assert kon.girisim_menzili_m == pytest.approx(
        kon.iletim_menzili_m * kon.girisim_orani
    )


def test_gizli_terminal_gecmisi_var():
    """En az bir üçlü (a,b,c) olmalı ki: a-b iletim menzilinde,
    a-c değil, ama a ile c girişim menzilinde.

    Bu, gizli terminalin GEOMETRİK olarak mümkün olduğunu gösterir.
    Mümkün değilse Li replikasyonundaki 1/7 asla çıkmaz.
    """
    topo, _ = _topo(1)
    n = topo.dugum_sayisi
    bulundu = any(
        topo.iletim_menzilinde_mi(a, b)
        and not topo.iletim_menzilinde_mi(a, c)
        and topo.girisim_menzilinde_mi(a, c)
        for a in range(n) for b in range(n) for c in range(n)
        if len({a, b, c}) == 3
    )
    assert bulundu, "gizli terminal geometrisi yok — 1/7 replikasyonu imkânsız"


def test_menzil_simetrik():
    topo, _ = _topo(3)
    n = topo.dugum_sayisi
    for i in range(n):
        for j in range(n):
            assert topo.iletim_menzilinde_mi(i, j) == topo.iletim_menzilinde_mi(j, i)


def test_dugum_kendi_komsusu_degil():
    topo, _ = _topo(3)
    for i in range(topo.dugum_sayisi):
        assert i not in topo.geometrik_komsular(i)


def test_ulasilabilir_ciftler_bagli_topolojide_tam():
    topo, kon = _topo(5)
    n = kon.dugum_sayisi
    assert len(topo.ulasilabilir_ciftler()) == n * (n - 1)


def test_ulasilabilir_ciftler_kopuk_topolojide_eksik():
    """Kopuk bir topolojide bileşenler arası çiftler DIŞLANMALI."""
    # Çok seyrek bir yerleşim kur: menzil küçük, alan büyük
    kon = Konfig(kol="t", tohum=1, dugum_sayisi=10, alan_m=5000.0,
                 iletim_menzili_m=300.0, baglanti_kosullamasi=False)
    topo = Topoloji.uret(kon, Akislar(1))
    assert len(topo.bagli_bilesenler()) > 1, "test kurulumu kopuk ağ üretmedi"
    assert len(topo.ulasilabilir_ciftler()) < 10 * 9


def test_yakinsamayan_topoloji_sessizce_gecmiyor():
    """İmkânsız yoğunlukta hata fırlatmalı — kopuk ağla devam etmemeli."""
    kon = Konfig(kol="t", tohum=1, dugum_sayisi=40, alan_m=100_000.0,
                 iletim_menzili_m=100.0, topoloji_max_deneme=5)
    with pytest.raises(RuntimeError, match="bağlı topoloji üretilemedi"):
        Topoloji.uret(kon, Akislar(1))
