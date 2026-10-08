"""
İKİ ÇİFT PROBU — uzamsal yeniden kullanımın SAF ölçümü.

K adet birbirinden uzak çift kurulur; her çift kendi doygun akışını koşar.

    toplam verim ≈ K × tek çift  →  yeniden kullanım VAR
    toplam verim ≈ tek çift      →  her şey SERİLEŞTİRİLİYOR

🔒 ZİNCİR YOK, YÖNLENDİRME YOK, ÇOK ATLAMA YOK — ve bu bilinçli. Zincir
kuyruk, uçtan uca gecikme ve çok atlamalı etkileri de taşır; burada sorulan
tek soru *"iki iletim ne kadar uzaktan itibaren aynı anda başarılı
olabiliyor"*. Bu prob o soruyu saf hâlde sorar.

Bağlam: `v2/09-LI-REPLIKASYONU.md` §SONUÇ · K-108. Koşan betik
`kalibrasyon/yeniden_kullanim.py`; burası kütüphanedir.

🔒 Kanal TEMİZ koşar (gölgeleme ve sönümleme kapalı) — `09` §03.1b'deki
gerekçenin aynısı: statik kolda donmuş derin Rician çekimi bağların %2–6'sını
öldürüyor ve ölçülen şey yeniden kullanım yerine bağ kesintisi olurdu.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.ag.kuyruk import Kuyruk  # noqa: E402
from sim2.ag.paket import Paket, PaketSayaci  # noqa: E402
from sim2.ag.trafik import Akis, Dogum  # noqa: E402
from sim2.cekirdek.korunum import KorunumDefteri  # noqa: E402
from sim2.cekirdek.olaylar import OlayKuyrugu  # noqa: E402
from sim2.cekirdek.rng import Akislar  # noqa: E402
from sim2.cekirdek.saat import Saatler  # noqa: E402
from sim2.cekirdek.sayaclar import Sayaclar  # noqa: E402
from sim2.dunya.geometri import Nokta3  # noqa: E402
from sim2.dunya.mobilite import Sabit  # noqa: E402
from sim2.dunya.topoloji import Topoloji  # noqa: E402
from sim2.gozlem.karar import Karar  # noqa: E402
from sim2.kanal.cerceve import cerceve_kur  # noqa: E402
from sim2.kanal.kanal import Kanal  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kayip import olum_anlari  # noqa: E402
from sim2.kosum.kurulum import Kurulum, duyma_turetimi  # noqa: E402
from sim2.mac.dcf import DcfZamanlari  # noqa: E402
from sim2.olcum.paket_defteri import PaketDefteri  # noqa: E402
from sim2.olcum.rota_olaylari import RotaDefteri  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402
from kalibrasyon import dunya_secimi as DS  # noqa: E402  (K-183)

__all__ = ["TOHUMLAR", "kos"]

TOHUMLAR = (1000, 1001, 1002)


class TekAtlama:
    """Hedef doğrudan komşudur; yönlendirme diye bir şey yok."""

    ad = "tek_atlama"
    __slots__ = ("kimlik",)

    def __init__(self, kimlik: int) -> None:
        self.kimlik = kimlik

    def sonraki_atlama(self, gozlem) -> Karar:
        if gozlem.paket is None or gozlem.paket.hedef == self.kimlik:
            return Karar()
        return Karar(sonraki=gozlem.paket.hedef)

    def beacon_yuku(self, gozlem) -> dict:
        return {}

    def beacon_alindi(self, gozlem, komsu, yuk) -> None:
        return None

    def teshis(self, dugum: int) -> dict:
        return {}


@dataclass(frozen=True, slots=True)
class CokAkis:
    """K akış, her biri kendi çiftine. `TrafikUreteci`nin yerine geçer."""

    _cizelge: tuple
    _akislar: tuple
    _paket_bayt: int
    _ttl: int
    _olcum_bitis_s: float
    _pencere: tuple

    @property
    def cizelge(self):
        return self._cizelge

    @property
    def toplam_dogum(self) -> int:
        return len(self._cizelge)

    def akis(self, kimlik: int) -> Akis:
        return self._akislar[kimlik]

    def paket_kur(self, dogum: Dogum, sayac) -> Paket:
        a = self._akislar[dogum.akis_kimligi]
        return Paket(kimlik=sayac.yeni(), akis_kimligi=a.kimlik,
                     kaynak=a.kaynak, hedef=a.hedef, dogum_s=dogum.t_s,
                     boyut_bayt=self._paket_bayt, ttl_kalan=self._ttl)

    def sunulan_hiz_hz(self) -> float:
        return self.toplam_dogum / max(self._olcum_bitis_s, 1e-9)

    def penceredeki_dogum(self) -> int:
        bas, bitis = self._pencere
        return sum(1 for d in self._cizelge if bas <= d.t_s < bitis)


def kos(cift: int, tohum: int, ayrim_m: float, bag_m: float = 280.0,
        alfa: float = 2.0, yuk_hz: float = 1200.0,
        bitis_s: float = 20.0) -> float:
    """K çift, `ayrim_m` aralıklarla dizili → pencere içi toplam verim (pkt/s).

    🔒 Verici gücü `alfa`dan TÜRETİLİR (`yayilim.py`: hedef alınan güç
    `nominal_bag_m`de eşiğe eşitlenir), dolayısıyla bağ her α'da çalışır
    ve α'lar arası karşılaştırma adildir.
    """
    temiz = dict(golgeleme_acik=False, sonumleme_acik=False,
                 yol_kaybi_usteli=alfa)
    n = 2 * cift
    kfg = DS.konfig(kol="yeniden_kullanim", senaryo="statik-yok", tohum=tohum,
                 dugum_sayisi=n, akis_sayisi=max(1, cift),
                 gorev_grup_sayisi=min(10, n),
                 isinma_s=0.2 * bitis_s, olcum_bitis_s=0.8 * bitis_s,
                 kosu_bitis_s=bitis_s, **temiz)
    akislar = Akislar(tohum)
    irtifa = 0.5 * (kfg.irtifa_min_m + kfg.irtifa_maks_m)
    konumlar = []
    for c in range(cift):
        konumlar.append(Nokta3(c * ayrim_m, 0.0, irtifa))
        konumlar.append(Nokta3(c * ayrim_m + bag_m, 0.0, irtifa))
    topoloji = Topoloji(mobilite=Sabit(tuple(konumlar)),
                        menzil_m=kfg.nominal_bag_m, dugum_sayisi=n)
    kanal = Kanal(kfg, topoloji)
    akis_listesi = tuple(Akis(kimlik=c, kaynak=2 * c, hedef=2 * c + 1)
                         for c in range(cift))
    periyot = 1.0 / yuk_hz
    adet = int(kfg.olcum_bitis_s / periyot)
    cizelge = tuple(sorted(
        (Dogum(k * periyot, c) for c in range(cift) for k in range(adet)),
        key=lambda d: (d.t_s, d.akis_kimligi)))
    veri = cerceve_kur(kfg, "veri")
    onay = cerceve_kur(kfg, "onay")
    beacon = cerceve_kur(kfg, "beacon")
    r_faz = akislar["beacon_faz"]
    kur = Kurulum(
        konfig=kfg, akislar=akislar, topoloji=topoloji,
        saatler=Saatler(dugum_sayisi=n,
                        ofset_araligi_s=kfg.saat_ofset_araligi_s,
                        sapma_ppm=kfg.saat_sapma_ppm,
                        senkron=kfg.saat_senkron, akislar=akislar),
        kanal=kanal,
        trafik=CokAkis(cizelge, akis_listesi, kfg.paket_bayt,
                       kfg.ttl_baslangic, kfg.olcum_bitis_s,
                       kfg.olcum_penceresi),
        olaylar=OlayKuyrugu(), sayaclar=Sayaclar(), korunum=KorunumDefteri(),
        paket_defteri=PaketDefteri(pencere_bas_s=kfg.olcum_penceresi[0],
                                   pencere_bitis_s=kfg.olcum_penceresi[1]),
        rota_defteri=RotaDefteri(), paket_sayaci=PaketSayaci(),
        kuyruklar=tuple(Kuyruk(kfg.kuyruk_kapasitesi) for _ in range(n)),
        beacon_fazlari=tuple(r_faz.uniform(0.0, kfg.beacon_araligi_s)
                             for _ in range(n)),
        veri_cercevesi=veri, onay_cercevesi=onay, beacon_cercevesi=beacon,
        zamanlar=DcfZamanlari.kur(kfg, veri, onay),
        # 🔴 K-183: yere toplama (kayıp yeri), A5 ve C1'in alanları eksikti;
        # araç KURULAMIYORDU. Türetim kurulumla TEK (`duyma_turetimi`).
        **dict(zip(("duyanlar_menzili_m", "maks_gecikme_s"),
                   duyma_turetimi(kfg, beacon))),
        yayilim_gecikmeli=kfg.yayilim_gecikmesi,
        olum_anlari=olum_anlari(kfg),
        kayip_yeri=None)
    Kosu(kur, TekAtlama).kostur()
    bas, bitis = kfg.olcum_penceresi
    return kur.paket_defteri.pencerede_teslim / (bitis - bas)
