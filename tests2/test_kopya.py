"""Uçtan uca kopya defteri — D-23 · K-231 (`v2/13` §07).

Protokol `Karar.kopyalar` ile gönderdiği paketin eşlerini başka komşulara
da yollayabilir (JarmRout her paketi iki düğüm-ayrık yoldan gönderir).
Hedefte ilk varan teslim sayılır, sonrakiler bastırılır; korunum eşleri de
kapatır; kopya istemeyen protokolün satırı birebir aynı kalır.
"""

from __future__ import annotations

import pytest

from protokoller.kosum_kosumu import EnYakinKimlik
from sim2.cekirdek.degismezler import DegismezHatasi
from sim2.cekirdek.korunum import KorunumDefteri
from sim2.gozlem.karar import Karar
from sim2.kosum.dugum import Dugum
from sim2.kosum.kosu import Kosu
from sim2.kosum.kurulum import kurulum_yap
from sim2.kosum.sonuc import korunum_bolumu
from sim2.yapilandirma.konfig import Konfig

_V = Konfig(kol="t")
_N = 14
_EN = _V.alan_en_m * (_N / _V.dugum_sayisi) ** 0.5


def _konfig(bitis: float = 6.0, tohum: int = 1000) -> Konfig:
    return Konfig(kol="test", senaryo="statik-yok", tohum=tohum,
                  isinma_s=0.2 * bitis, olcum_bitis_s=0.8 * bitis,
                  kosu_bitis_s=bitis, dugum_sayisi=_N, akis_sayisi=4,
                  alan_en_m=_EN, alan_boy_m=_EN, gorev_grup_sayisi=2,
                  gorev_grup_yaricapi_m=(_V.gorev_grup_yaricapi_m * _EN
                                         / _V.alan_en_m))


class KaynaktaKopyalayan(EnYakinKimlik):
    """Sınav aleti: kaynak düğüm her paketin bir eşini, seçilen sonraki
    atlamadan farklı en küçük kimlikli komşuya da yollar."""

    ad = "kaynakta_kopyalayan"
    __slots__ = ()

    def sonraki_atlama(self, gozlem):
        karar = EnYakinKimlik.sonraki_atlama(self, gozlem)
        p = gozlem.paket
        if karar.sonraki is None or p is None or p.kaynak != gozlem.dugum:
            return karar
        diger = [k.dugum for k in gozlem.komsular
                 if k.dugum != karar.sonraki]
        if not diger:
            return karar
        return Karar(sonraki=karar.sonraki, kopyalar=(min(diger),))


def _kos(protokol, bitis: float = 6.0):
    kur = kurulum_yap(_konfig(bitis))
    kosu = Kosu(kur, lambda i: protokol())
    kosu.kostur()
    return kur, kosu


def test_KARAR_kopya_kurallari():
    Karar(sonraki=1, kopyalar=(2, 3))
    with pytest.raises(DegismezHatasi):
        Karar(kopyalar=(2,))                        # gönderilmeyen paket
    with pytest.raises(DegismezHatasi):
        Karar(sonraki=1, kopyalar=(1,))             # sonraki'nin aynısı
    with pytest.raises(DegismezHatasi):
        Karar(sonraki=1, kopyalar=(2, 2))           # tekil değil
    with pytest.raises(DegismezHatasi):
        Karar(beklet=True, kopyalar=(2,))           # bekletilen paket


def test_KORUNUM_kopya_gecisleri_ve_rapor():
    d = KorunumDefteri()
    d.uret()
    d.kopya_uret()
    d.kuyruktan_al()
    d.kuyruktan_al()
    d.teslim_et()                                   # ilk varan eş
    d.kopya_bastir()                                # ikinci varan eş
    assert d.denklem_tutuyor_mu()
    r = d.kontrol()
    assert r["korunum_tamam"] and r["fark"] == 0
    assert (r["kopya_uretilen"], r["kopya_bastirilan"]) == (1, 1)
    bos = KorunumDefteri().kontrol()
    assert "kopya_uretilen" not in bos and "kopya_bastirilan" not in bos


def test_KOPYA_uctan_uca_defter_kapanir_ve_es_protokole_sorulmaz(
        monkeypatch):
    zorunlu: list[tuple[int, int, int]] = []
    asil = Dugum.kopya_sonraki_al

    def izle(self, paket):
        sonraki = asil(self, paket)
        if sonraki is not None:
            zorunlu.append((paket.kimlik, paket.kopya, sonraki))
        return sonraki

    monkeypatch.setattr(Dugum, "kopya_sonraki_al", izle)
    kur, kosu = _kos(KaynaktaKopyalayan)
    r = korunum_bolumu(kur, kosu.dugumler)
    assert r["korunum_tamam"] and r["mutabakat_tamam"], r
    assert r["kopya_uretilen"] > 0 and r["kopya_bastirilan"] > 0, r
    # Paket düzeyi: her paket en çok bir kez teslim; teslim sayısı defterle.
    kayitlar = kur.paket_defteri.kayitlar()
    assert len({k.kimlik for k in kayitlar}) == len(kayitlar) == r["teslim"]
    assert r["teslim"] <= r["uretilen"]
    # Eş kuyruk başında protokole sorulmadan kopya anındaki komşuya gitti.
    assert zorunlu and all(kopya >= 1 for _, kopya, _ in zorunlu)
    assert len(zorunlu) <= r["kopya_uretilen"]


def test_KOPYASIZ_kosuda_satira_alan_girmez():
    kur, kosu = _kos(EnYakinKimlik)
    r = korunum_bolumu(kur, kosu.dugumler)
    assert r["korunum_tamam"] and r["mutabakat_tamam"]
    assert "kopya_uretilen" not in r and "kopya_bastirilan" not in r
    assert kosu.kopya_no == {}
    assert all(not d._kopya_sonraki for d in kosu.dugumler)
