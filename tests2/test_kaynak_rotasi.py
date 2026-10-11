"""Kaynak rotası — K-232 (DSR ailesi, RFC 4728 §6.7; JarmRout).

Protokol `Karar.rota` ile paketin başlığına ara düğümleri yazar; başlıkta
yazdığı için gözlem penceresinde görünür, adres başına bayt çerçeveyi uzatır
ve yönlendirme ek yüküne (`veri_baslik_bayt`) sayılır. Rota taşımayan
protokolde hiçbir şey değişmez.
"""

from __future__ import annotations

import pytest

from protokoller.kosum_kosumu import EnYakinKimlik
from sim2.ag.paket import Paket
from sim2.cekirdek.degismezler import DegismezHatasi
from sim2.gozlem.karar import Karar
from sim2.kosum import gonderim
from sim2.kosum.kosu import Kosu
from sim2.kosum.kurulum import kurulum_yap
from sim2.kosum.sonuc import korunum_bolumu
from sim2.yapilandirma.konfig import Konfig

_V = Konfig(kol="t")
_N = 14
_EN = _V.alan_en_m * (_N / _V.dugum_sayisi) ** 0.5
_ADRES = 4


def _konfig(bitis: float = 6.0) -> Konfig:
    return Konfig(kol="test", senaryo="statik-yok", tohum=1000,
                  isinma_s=0.2 * bitis, olcum_bitis_s=0.8 * bitis,
                  kosu_bitis_s=bitis, dugum_sayisi=_N, akis_sayisi=4,
                  alan_en_m=_EN, alan_boy_m=_EN, gorev_grup_sayisi=2,
                  gorev_grup_yaricapi_m=(_V.gorev_grup_yaricapi_m * _EN
                                         / _V.alan_en_m))


class RotaYazan(EnYakinKimlik):
    """Sınav aleti: kaynak, seçtiği sonraki atlamayı ve bir sahte ara düğümü
    rota olarak yazar; bir eşi başka komşuya kendi rotasıyla yollar. Ara
    düğümler başlıkta gördüğü rotayı kaydeder (yönlendirme EnYakin'inki)."""

    ad = "rota_yazan"
    rota_adres_bayt = _ADRES
    __slots__ = ("gorulen",)

    def __init__(self) -> None:
        self.gorulen: list[tuple[int, ...]] = []

    def sonraki_atlama(self, gozlem):
        karar = EnYakinKimlik.sonraki_atlama(self, gozlem)
        p = gozlem.paket
        if p is not None and p.kaynak != gozlem.dugum:
            self.gorulen.append(p.rota)
        if karar.sonraki is None or p is None or p.kaynak != gozlem.dugum:
            return karar
        rota = (karar.sonraki, 99)
        diger = [k.dugum for k in gozlem.komsular
                 if k.dugum != karar.sonraki]
        if not diger:
            return Karar(sonraki=karar.sonraki, rota=rota)
        k = min(diger)
        return Karar(sonraki=karar.sonraki, rota=rota, kopyalar=(k,),
                     kopya_rotalari=((k,),))


def test_KARAR_ve_PAKET_rota_kurallari():
    Karar(sonraki=1, rota=(1, 2))
    with pytest.raises(DegismezHatasi):
        Karar(rota=(1,))                                 # gönderilmeyen
    with pytest.raises(DegismezHatasi):
        Karar(sonraki=1, kopyalar=(2,), kopya_rotalari=((2,), (3,)))
    with pytest.raises(DegismezHatasi):
        Paket(kimlik=1, akis_kimligi=0, kaynak=0, hedef=5, dogum_s=0.0,
              boyut_bayt=512, ttl_kalan=64, rota=(2, 3, 2))   # döngü


def test_ROTA_baslikta_gorunur_ve_baytina_gore_cerceve_uzar(monkeypatch):
    beklenen: list[int] = []
    asil = gonderim.veri_gonder

    def izle(kosu, d, paket, hedef):
        beklenen.append(_ADRES * len(paket.rota))
        return asil(kosu, d, paket, hedef)

    monkeypatch.setattr(gonderim, "veri_gonder", izle)
    kur = kurulum_yap(_konfig())
    protokoller = []

    def fabrika(i):
        p = RotaYazan()
        protokoller.append(p)
        return p

    kosu = Kosu(kur, fabrika)
    kosu.kostur()
    r = korunum_bolumu(kur, kosu.dugumler)
    assert r["korunum_tamam"] and r["mutabakat_tamam"], r
    # Ara düğümler başlıktaki rotayı gördü (asıl: (j, 99) · eş: (k,)).
    gorulen = [g for p in protokoller for g in p.gorulen]
    assert any(len(g) == 2 and g[1] == 99 for g in gorulen)
    assert any(len(g) == 1 for g in gorulen)
    # Yönlendirme ek yükü: her veri iletiminin (yeniden denemeler dâhil)
    # başlığı adres başına 4 bayt — sayaç birebir.
    sayac = kur.sayaclar.disa_ver()
    assert sum(beklenen) > 0
    assert sayac["veri_baslik_bayt"] == sum(beklenen)


def test_ROTA_cercevesi_hizda_uzar():
    kur = kurulum_yap(_konfig(bitis=1.0))
    kosu = Kosu(kur, lambda i: RotaYazan())
    hiz = 1e6
    rotali, yuk = gonderim._hizda_veri_cerceveleri(kosu, hiz, 3 * _ADRES)
    duz, yuk2 = gonderim._hizda_veri_cerceveleri(kosu, hiz)
    assert yuk == yuk2 and duz == yuk
    assert rotali.bayt == yuk.bayt + 3 * _ADRES
    assert rotali.sure_s > yuk.sure_s


def test_ROTASIZ_protokolde_baslik_sayaci_yok():
    kur = kurulum_yap(_konfig())
    kosu = Kosu(kur, lambda i: EnYakinKimlik())
    kosu.kostur()
    assert kosu.rota_adres_bayt == 0
    assert not kur.sayaclar.disa_ver().get("veri_baslik_bayt")
