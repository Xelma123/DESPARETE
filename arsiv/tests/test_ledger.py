"""
Korunum defteri testleri.

    üretilen = teslim + düşen + kuyrukta + uçuşta

Bu eşitliğin her koşuda tutması, sessiz paket kaybına karşı tek savunmamız.
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sim.ledger import DUSME_SEBEPLERI, KorunumDefteri, KorunumHatasi  # noqa: E402


def test_bos_defter_tutuyor():
    d = KorunumDefteri()
    assert d.denklem_tutuyor_mu()
    assert d.kontrol()["korunum_tamam"] is True


def test_basit_yasam_dongusu():
    d = KorunumDefteri()
    d.uret()                       # kaynak kuyruğuna
    assert (d.uretilen, d.kuyrukta) == (1, 1)
    d.kuyruktan_al()               # iletiliyor
    assert (d.kuyrukta, d.ucusta) == (0, 1)
    d.ucustan_kuyruga()            # bir sonraki düğümde
    assert (d.kuyrukta, d.ucusta) == (1, 0)
    d.kuyruktan_al()
    d.teslim_et()                  # hedefte
    assert (d.teslim, d.ucusta) == (1, 0)
    assert d.denklem_tutuyor_mu()


@pytest.mark.parametrize("sebep", DUSME_SEBEPLERI)
def test_her_dusme_sebebi_korunumu_bozmaz(sebep):
    d = KorunumDefteri()
    d.uret()
    d.dus(sebep, nereden="kuyruk")
    assert d.denklem_tutuyor_mu()
    assert d.dusen[sebep] == 1


def test_ucustan_dusme():
    d = KorunumDefteri()
    d.uret()
    d.kuyruktan_al()
    d.dus("iletim_basarisiz", nereden="ucus")
    assert d.denklem_tutuyor_mu()


def test_bilinmeyen_sebep_hata_verir():
    """Sebepler kapalı bir kümedir. 'diğer' diye bir sebep yoktur —
    sebebi bilinmeyen bir düşüş, teşhis edilmemiş bir hatadır."""
    d = KorunumDefteri()
    d.uret()
    with pytest.raises(KorunumHatasi):
        d.dus("kim_bilir", nereden="kuyruk")


def test_gecersiz_nereden_hata_verir():
    d = KorunumDefteri()
    d.uret()
    with pytest.raises(KorunumHatasi):
        d.dus("ttl", nereden="hiclik")


def test_negatif_sayac_hemen_patlar():
    """Sayaç negatife düştüğü ANDA patlamalı, koşu sonunda değil.

    Koşu sonunda patlarsa, hatanın hangi geçişten geldiği bulunamaz.
    """
    d = KorunumDefteri()
    with pytest.raises(KorunumHatasi):
        d.kuyruktan_al()            # kuyrukta hiç paket yok


def test_rastgele_gecis_dizisi_korunumu_bozmuyor():
    """Kaba kuvvet: binlerce rastgele geçiş, denklem her adımda tutmalı."""
    rnd = random.Random(42)
    d = KorunumDefteri()
    for _ in range(20_000):
        secenekler = ["uret"]
        if d.kuyrukta > 0:
            secenekler += ["kuyruktan_al", "dus_kuyruk"]
        if d.ucusta > 0:
            secenekler += ["ucustan_kuyruga", "teslim", "dus_ucus"]
        eylem = rnd.choice(secenekler)

        if eylem == "uret":
            d.uret()
        elif eylem == "kuyruktan_al":
            d.kuyruktan_al()
        elif eylem == "ucustan_kuyruga":
            d.ucustan_kuyruga()
        elif eylem == "teslim":
            d.teslim_et()
        elif eylem == "dus_kuyruk":
            d.dus(rnd.choice(["kuyruk_tasmasi", "ttl"]), nereden="kuyruk")
        elif eylem == "dus_ucus":
            d.dus("iletim_basarisiz", nereden="ucus")

        assert d.denklem_tutuyor_mu(), d.kontrol()


def test_bozuk_defter_kontrolde_yakalanir():
    """Sayaç dışarıdan bozulursa kontrol() bunu bildirmeli.

    Defter tek geçiş noktası olsa da, birinin ileride alanı doğrudan
    değiştirmesine karşı kontrol() son savunma hattıdır.
    """
    d = KorunumDefteri()
    d.uret(5)
    d.teslim += 3                    # kasıtlı bozma: hiçbir geçişten geçmedi
    rapor = d.kontrol()
    assert rapor["korunum_tamam"] is False
    assert rapor["fark"] == -3
