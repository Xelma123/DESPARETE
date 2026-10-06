"""
Kurulum — bir koşunun bütün parçalarını `Konfig` + tohumdan kurar.

🔒 BÜTÜN RASTGELELİK BURADA TÜKENİR
===================================
Yerleşim, mobilite, saat, trafik ve beacon fazı **kurulumda** çekilir. Koşu
sırasında çekim yapan tek şey hash alanlarıdır (kanal kararı, gölgeleme,
sönümleme, karıştırıcı) ve onlar durumsuzdur. Sonuç: aynı tohumda her
protokol **birebir aynı dünyayı, aynı trafiği, aynı saatleri** görür.

🔴 KOŞU SIRASINDA SIRALI AKIŞTAN ÇEKİM YAPAN TEK YER
====================================================
`mac_geri_cekilme` — ve o da **düğüm başına alt akıştan**. Bir düğümün
kendi dizisi, protokol daha çok ilettiği için ilerler; bu düzeltilebilir bir
şey değil (iletim sayısı protokolün kendi davranışı). Düzeltilebilir olan
düğümler arası kuplajdı ve alt akışla kapatıldı.

🔒 KURULUM SIRASI SONUCU ETKİLEMEZ
==================================
Her akış kendi ADINDAN tohumlandığı için, hangi bileşenin önce kurulduğu
çekimleri kaydırmaz. Ölçüldü ve teste bağlandı (`test_yapilandirma.py`).
Yine de sıra sabit tutulur: değişmesi bir şeyi bozmasa da, sabit olması
hata ayıklamayı kolaylaştırır.
"""

from __future__ import annotations

from dataclasses import dataclass

from sim2.ag.kuyruk import Kuyruk
from sim2.ag.paket import PaketSayaci
from sim2.ag.trafik import TrafikUreteci
from sim2.cekirdek.degismezler import dogrula
from sim2.cekirdek.korunum import KorunumDefteri
from sim2.cekirdek.olaylar import OlayKuyrugu
from sim2.cekirdek.rng import Akislar
from sim2.cekirdek.saat import Saatler
from sim2.cekirdek.sayaclar import Sayaclar
from sim2.dunya.topoloji import Topoloji, topoloji_kur
from sim2.kanal.cerceve import Cerceve, cerceve_kur
from sim2.kanal.kanal import Kanal
from sim2.kanal.yayilim import ISIK_HIZI
from sim2.kosum.kayip import olum_anlari
from sim2.mac.dcf import DcfZamanlari
from sim2.olcum.kayip_yeri import KayipYeri
from sim2.olcum.paket_defteri import PaketDefteri
from sim2.olcum.rota_olaylari import RotaDefteri
from sim2.yapilandirma.konfig import Konfig

__all__ = ["Kurulum", "kurulum_yap", "duyma_turetimi"]


def duyma_turetimi(konfig: Konfig, beacon: Cerceve,
                   menzil_m: float | None = None) -> tuple[float, float]:
    """`(duyanlar_menzili_m, maks_gecikme_s)` — TEK türetim (K-183).

    🔴 NEDEN AYRI BİR İŞLEV: `Kurulum`u elle kuran iki kalibrasyon aracı (Li
    zinciri, iki çift) bu alanları KENDİLERİ hesaplıyordu ve A2/A5/C1'in
    eklediklerini almamıştı — ikisi de kurulamaz hâldeydi (Faz 4.0'da
    bulundu). Formül kopyalanırsa ayrışır; araçlar bunu çağırır.

    Duyma menzili girişim menzilinden türer; işlem kazancı açıkken önbelge
    Eb/N0 çarpanıyla `çarpan^(1/α)` genişler (kapalıyken çarpan 1 → birebir).
    `menzil_m` verilirse (araçların deneysel geçersiz kılması) o kullanılır.
    En uzak tek yön gecikmesi yalnız yayılım gecikmesi açıkken sıfırdan
    büyüktür.
    """
    if menzil_m is None:
        menzil_m = konfig.girisim_menzili_m * (
            beacon.onbelge_ebn0_carpani ** (1.0 / konfig.yol_kaybi_usteli))
    return menzil_m, (menzil_m / ISIK_HIZI if konfig.yayilim_gecikmesi
                      else 0.0)


@dataclass(frozen=True, slots=True)
class Kurulum:
    """Bir koşunun bütün parçaları. Dondurulmuş: koşu ortasında değişemez."""

    konfig: Konfig
    akislar: Akislar
    topoloji: Topoloji
    saatler: Saatler
    kanal: Kanal
    trafik: TrafikUreteci
    olaylar: OlayKuyrugu
    sayaclar: Sayaclar
    korunum: KorunumDefteri
    paket_defteri: PaketDefteri
    rota_defteri: RotaDefteri
    paket_sayaci: PaketSayaci
    kuyruklar: tuple[Kuyruk, ...]
    beacon_fazlari: tuple[float, ...]
    veri_cercevesi: Cerceve
    onay_cercevesi: Cerceve
    beacon_cercevesi: Cerceve
    zamanlar: DcfZamanlari
    # 🔒 Kimin kimi DUYDUĞU — geometrik girişim menzilinden.
    duyanlar_menzili_m: float
    # 🔒 A5 (K-175) — yayılım gecikmesi açık mı; en uzak duyma mesafesinin
    # tek yön gecikmesi (kapalıyken 0,0 — her toplama birebir).
    yayilim_gecikmeli: bool
    maks_gecikme_s: float
    # 🔒 C1 (K-180) — düğüm başına ölüm anı (`None` = ölmez).
    olum_anlari: tuple
    # Yere toplamada düşüşlerin geçide mesafesi (`v2/07` §18 Y4); eşler arası
    # desende `None` ve hiçbir yerde okunmaz.
    kayip_yeri: KayipYeri | None

    @property
    def dugum_sayisi(self) -> int:
        return self.konfig.dugum_sayisi


def kurulum_yap(konfig: Konfig, tohum: int | None = None) -> Kurulum:
    """`Konfig` + tohum → koşulmaya hazır bir dünya.

    🔴 `tohum` verilmezse `konfig.tohum` kullanılır. İki yerde tohum olması
    kafa karıştırıcı olurdu; `Konfig`teki tektir ve sonuç satırına o yazılır.
    """
    dogrula(tohum is None or tohum == konfig.tohum,
            "tohum `Konfig`ten gelir; ayrı bir tohum vermek sonuç satırındaki "
            "tohumu yalancı yapardı")
    akislar = Akislar(konfig.tohum)

    topoloji = topoloji_kur(konfig, akislar)
    saatler = Saatler(dugum_sayisi=konfig.dugum_sayisi,
                      ofset_araligi_s=konfig.saat_ofset_araligi_s,
                      sapma_ppm=konfig.saat_sapma_ppm,
                      senkron=konfig.saat_senkron, akislar=akislar)
    kanal = Kanal(konfig, topoloji)
    trafik = TrafikUreteci(konfig, akislar)

    # Beacon fazı düğüm başına: hepsi aynı anda yayın yapsaydı her beacon
    # aralığında bir çarpışma fırtınası olur ve ölçülen şey kontrol
    # düzleminin değil, fazın yapaylığı olurdu.
    r_faz = akislar["beacon_faz"]
    beacon_fazlari = tuple(r_faz.uniform(0.0, konfig.beacon_araligi_s)
                           for _ in range(konfig.dugum_sayisi))

    veri = cerceve_kur(konfig, "veri")
    onay = cerceve_kur(konfig, "onay")
    beacon = cerceve_kur(konfig, "beacon")
    duyanlar_menzili_m, maks_gecikme_s = duyma_turetimi(konfig, beacon)

    return Kurulum(
        konfig=konfig, akislar=akislar, topoloji=topoloji, saatler=saatler,
        kanal=kanal, trafik=trafik, olaylar=OlayKuyrugu(),
        sayaclar=Sayaclar(), korunum=KorunumDefteri(),
        paket_defteri=PaketDefteri(pencere_bas_s=konfig.olcum_penceresi[0],
                                   pencere_bitis_s=konfig.olcum_penceresi[1]),
        rota_defteri=RotaDefteri(), paket_sayaci=PaketSayaci(),
        kuyruklar=tuple(Kuyruk(konfig.kuyruk_kapasitesi)
                        for _ in range(konfig.dugum_sayisi)),
        beacon_fazlari=beacon_fazlari,
        veri_cercevesi=veri, onay_cercevesi=onay, beacon_cercevesi=beacon,
        zamanlar=DcfZamanlari.kur(konfig, veri, onay),
        # 🔒 KİM KİMİ DUYAR — geometrik girişim menzilinden.
        # Menzil tanımı gereği bu mesafede alınan güç tam olarak gürültü
        # tabanına eşittir; ötesinde SINR ≤ 0 dB ve önbelge PER'i ≈ 1. Yani
        # dışarıda bırakılanlar zaten çözemezdi. Gölgeleme sınırı ±3 dB
        # bulanıklaştırır (mesafede ±%26) ve bu KAPSAM BELGESİNE yazılır:
        # taşıyıcı dinleme ve alım denemesi kümesi geometrik seçilir, yavaş
        # kayıpla değil. Yönü belirsizdir, sistematik değil.
        # 🔒 İŞLEM KAZANCI (A2, K-173): önbelge Eb/N0 = SNR · çarpan (×22);
        # sınırdaki Eb/N0 eski dünyadakiyle aynı kalsın diye menzil
        # çarpan^(1/α) kadar genişler (α = 2'de ×4,69). Kazanç kapalıyken
        # çarpan tam 1 → menzil birebir.
        duyanlar_menzili_m=duyanlar_menzili_m,
        yayilim_gecikmeli=konfig.yayilim_gecikmesi,
        olum_anlari=olum_anlari(konfig),
        maks_gecikme_s=maks_gecikme_s,
        kayip_yeri=(KayipYeri(konfig.iletim_menzili_m)
                    if konfig.yere_toplama else None),
    )
