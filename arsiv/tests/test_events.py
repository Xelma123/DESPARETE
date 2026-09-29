"""
Olay kuyruğu testleri.

Kritik nokta: aynı tohum → birebir aynı sonuç (06-ON-KAYIT.md, K2).
Bunu bozan en sinsi şey, eşit zamanlı olayların sırasının belirsiz olmasıdır.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sim.events import GecmisZamanHatasi, OlayKuyrugu  # noqa: E402


def test_zaman_sirasinda_calisiyor():
    k = OlayKuyrugu()
    izler: list[float] = []
    for t in (5.0, 1.0, 3.0, 2.0, 4.0):
        k.ekle(t, izler.append, t)
    k.kostur(10.0)
    assert izler == [1.0, 2.0, 3.0, 4.0, 5.0]


def test_esit_zamanli_olaylar_ekleme_sirasinda():
    """Eşit zamanlı olaylar EKLENME sırasında çalışmalı.

    Bu keyfi ama belirlenimci bir kural. Kural olmasaydı sıra bellek
    adresine bağlı olabilirdi — sessiz belirlenimsizlik.
    """
    k = OlayKuyrugu()
    izler: list[str] = []
    for etiket in "abcdef":
        k.ekle(1.0, izler.append, etiket)
    k.kostur(2.0)
    assert izler == list("abcdef")


def test_olay_nesneleri_karsilastirilmiyor():
    """Karşılaştırılamayan nesneler bile olay olarak taşınabilmeli.

    Kuyruk anahtarı (zaman, sıra) olduğu için geri çağrı ve argümanlar
    asla karşılaştırılmaz. Karşılaştırılsaydı bu test TypeError verirdi.
    """
    class Karsilastirilamaz:
        __lt__ = __gt__ = __le__ = __ge__ = None  # type: ignore

    k = OlayKuyrugu()
    alinanlar = []
    for _ in range(5):
        k.ekle(1.0, alinanlar.append, Karsilastirilamaz())
    k.kostur(2.0)
    assert len(alinanlar) == 5


def test_gecmise_olay_eklenemez():
    k = OlayKuyrugu()
    k.ekle(5.0, lambda: None)
    k.kostur(5.0)
    with pytest.raises(GecmisZamanHatasi):
        k.ekle(4.9, lambda: None)


def test_negatif_gecikme_hata_verir():
    k = OlayKuyrugu()
    with pytest.raises(GecmisZamanHatasi):
        k.gecikmeyle_ekle(-0.1, lambda: None)


def test_olay_yeni_olay_doguruyor():
    """Zincirleme: her olay bir sonrakini eklesin."""
    k = OlayKuyrugu()
    izler: list[float] = []

    def adim(kalan: int) -> None:
        izler.append(k.simdi)
        if kalan > 0:
            k.gecikmeyle_ekle(1.0, adim, kalan - 1)

    k.ekle(0.0, adim, 4)
    k.kostur(100.0)
    assert izler == [0.0, 1.0, 2.0, 3.0, 4.0]


def test_bitisten_sonraki_olaylar_islenmiyor():
    """Koşu bitişinden sonraki olaylar kuyrukta kalmalı — silinmemeli.

    Kuyrukta kalan olaylar boşaltma penceresinin doğru çalıştığını
    kontrol etmek için gerekli.
    """
    k = OlayKuyrugu()
    izler: list[float] = []
    for t in (1.0, 2.0, 9.0, 12.0):
        k.ekle(t, izler.append, t)
    k.kostur(5.0)
    assert izler == [1.0, 2.0]
    assert k.bekleyen_olay_sayisi() == 2
    assert k.simdi == 5.0


def test_kostur_simdiyi_tam_bitise_ayarliyor():
    """Koşu sonu sayımları her kolda AYNI ana denk gelmeli.

    Simdi son olayın zamanında kalsaydı, farklı kollar koşuyu farklı
    anlarda bitirir ve son sayımlar kıyaslanamaz olurdu.
    """
    k = OlayKuyrugu()
    k.ekle(1.0, lambda: None)
    k.kostur(350.0)
    assert k.simdi == 350.0


def test_belirlenimcilik_ayni_dizi():
    def kosuyu_uret() -> list[tuple[float, str]]:
        k = OlayKuyrugu()
        izler: list[tuple[float, str]] = []

        def olay(etiket: str, derinlik: int) -> None:
            izler.append((k.simdi, etiket))
            if derinlik > 0:
                k.gecikmeyle_ekle(0.5, olay, etiket + "L", derinlik - 1)
                k.gecikmeyle_ekle(0.5, olay, etiket + "R", derinlik - 1)

        k.ekle(0.0, olay, "x", 6)
        k.kostur(50.0)
        return izler

    assert kosuyu_uret() == kosuyu_uret()
