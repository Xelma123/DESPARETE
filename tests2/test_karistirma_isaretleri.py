"""Karıştırmanın yerel işaretleri — kaydedicinin saf yardımcıları (Faz 5-2
teşhis (d), 16 Kasım 2026). Simülasyon yok; davranışın değişmediği duman
koşusunda teşhis (c)'nin Babel satırıyla birebirlik olarak denetlenir.
"""
from collections import defaultdict

import pytest


def test_DAGIT_araligi_dilimlere_oranla_boler():
    from kalibrasyon.karistirma_isaretleri import dagit
    t = defaultdict(float)
    dagit(t, 7, 2.25, 4.5)
    assert t == {(7, 2): pytest.approx(0.75), (7, 3): pytest.approx(1.0),
                 (7, 4): pytest.approx(0.5)}
    dagit(t, 7, 3.0, 3.0)                       # boş aralık bir şey yazmaz
    assert sum(t.values()) == pytest.approx(2.25)


def test_KUTU_sinirlar_ve_tavan():
    from kalibrasyon.karistirma_isaretleri import KUTULAR, kutu, rssi_kutusu
    assert kutu("mesgul", 0.0) == 0
    assert kutu("mesgul", 1.0) == KUTULAR["mesgul"][2] - 1
    assert kutu("mesgul", 1.0000001) == KUTULAR["mesgul"][2] - 1
    assert kutu("phy", 0) == 0 and kutu("phy", 7) == 7
    assert kutu("phy", 10_000) == 99
    assert kutu("sessizlik", 0.05) == 0 and kutu("sessizlik", 0.15) == 1
    assert kutu("sessizlik", 30.0) == 299
    assert rssi_kutusu(None) == "yok"
    assert rssi_kutusu(-110.0) == "0" and rssi_kutusu(-108.5) == "0"
    assert rssi_kutusu(-200.0) == "0" and rssi_kutusu(0.0) == "39"


def test_VAZGECME_DIZILERI_baslangic_ve_uzunluk():
    from kalibrasyon.karistirma_isaretleri import vazgecme_dizileri
    assert vazgecme_dizileri([]) == []
    assert vazgecme_dizileri([True, True]) == []
    assert vazgecme_dizileri([False]) == [(0, 1)]
    s = [True, False, False, True, False, True, False, False, False]
    assert vazgecme_dizileri(s) == [(1, 2), (4, 1), (6, 3)]


def test_NCI_VAZGECME_basari_sifirlar_ve_oncesi_sayilmaz():
    from kalibrasyon.karistirma_isaretleri import nci_vazgecme
    olay = [(9.0, False), (10.5, False), (11.0, True), (12.0, False),
            (12.5, False), (13.0, False), (20.0, False)]
    # 10'dan önceki vazgeçme sayılmaz; 11'deki başarı sayacı sıfırlar.
    assert nci_vazgecme(olay, 10.0, 25.0, 1) == pytest.approx(0.5)
    assert nci_vazgecme(olay, 10.0, 25.0, 2) == pytest.approx(2.5)
    assert nci_vazgecme(olay, 10.0, 25.0, 3) == pytest.approx(3.0)
    assert nci_vazgecme(olay, 10.0, 25.0, 4) == pytest.approx(10.0)
    assert nci_vazgecme(olay, 10.0, 25.0, 5) is None
    # Dönemin sonu (dışarıda kalan olay sayılmaz).
    assert nci_vazgecme(olay, 10.0, 19.0, 4) is None
