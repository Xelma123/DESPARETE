"""Duyarlılık aracı — modül sabiti oynatma (Faz 4.4, 2 Ekim 2026).

Simülasyon koşturmaz: yalnız oynatılan değer ve yamanın geri alınması.
"""
from __future__ import annotations

import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from kalibrasyon import duyarlilik as D


def test_MODUL_SABITI_turune_gore_oynatilir():
    assert D._oynat("sim2/dunya/mobilite.py::ISTASYON_TUTMA_S", 2.0) == 4.0
    assert D._oynat("kalibrasyon/kahin.py::SONUMLEME_ORNEGI", 0.5) == 24


def test_OLASILIK_ESIGI_kayip_payindan_oynatilir():
    """K-213: ×2 eşiği 1'in üstüne taşımaz; çarpılan (1 − p)."""
    import pytest
    ad = "kalibrasyon/kahin.py::ATLAMA_ESIGI"
    assert D._oynat(ad, 0.5) == pytest.approx(0.95)
    assert D._oynat(ad, 2.0) == pytest.approx(0.80)


def test_MODUL_SABITI_yamasi_GERI_ALINIR(monkeypatch):
    """`_kos` hata verse bile sabit eski değerine döner (try/finally)."""
    import kalibrasyon.kahin as K
    eski = K.ATLAMA_ESIGI
    monkeypatch.setattr(D, "kurulum_yap",
                        lambda kfg: (_ for _ in ()).throw(RuntimeError("dur")))
    try:
        D._kos("statik-yok", 1000, "en_guvenilir_kahin",
               {"kalibrasyon/kahin.py::ATLAMA_ESIGI": 0.5})
    except RuntimeError:
        pass
    assert K.ATLAMA_ESIGI == eski
