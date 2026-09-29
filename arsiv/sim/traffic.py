"""
Kat 0 — Trafik üretimi.

Kaynak–hedef çiftleri seçilir, her çift sabit aralıkla (CBR) paket üretir.

ÜÇ KURULUM KARARI VE GEREKÇELERİ
=================================

1) ÇİFTLER YALNIZCA ULAŞILABİLİR DÜĞÜMLERDEN SEÇİLİR
   Ulaşılamayan bir hedefe giden paketin kaybı protokolün değil topolojinin
   suçudur. Bu çiftler dışlanmazsa karıştırıcısız kontrol kolunda bile teslim
   oranı %100'ün altında kalır ve "etkinin sıfır olması gereken kol" anlamını
   yitirir.

2) HER KAYNAK RASTGELE BİR FAZDA BAŞLAR
   Tüm kaynaklar t=ısınma anında aynı anda başlasaydı, periyodik süreçler
   kilitlenir; her CBR darbesi aynı anda gelir; ağ periyodik olarak dolup
   boşalır. Bu, tohumlar arası varyansı YAPAY olarak düşürür ve gerçekte
   olmayan bir düzenlilik yaratır. (03-YONTEM-KURALLARI.md, B6 "rezonans")

   ⭐ Bu, "durum tutan yeni bir bileşeni başlangıç koşulunu sormadan ekleme"
   kuralının (kural 14) somut hâli: CBR kaynağı durum tutar, ve t=0'daki
   fazı sorulmak zorundadır.

3) TRAFİK ÜRETİMİ ÖLÇÜM PENCERESİ BİTİMİNDE DURUR — BORU BOŞALIR
   Koşu, kuyruklarda ve havada paket varken kesilirse bu paketler "teslim
   edilmedi" sayılır. Uzun rota kullanan protokolün borusu daha doludur;
   yani haksız yere cezalandırılır. (07-SIMULATOR-ARAYUZ.md, boşaltma)
"""

from __future__ import annotations

from dataclasses import dataclass

from .config import Konfig
from .events import OlayKuyrugu
from .packet import Paket
from .queues import Kuyruk
from .rng import Akislar
from .topology import Topoloji


@dataclass(frozen=True)
class Akis:
    """Bir kaynak–hedef çifti ve onun CBR takvimi."""
    kaynak: int
    hedef: int
    ilk_gonderim_s: float


class TrafikUreteci:
    def __init__(
        self,
        kon: Konfig,
        topo: Topoloji,
        akislar: Akislar,
        olay_kuyrugu: OlayKuyrugu,
        kuyruklar: dict[int, Kuyruk],
    ) -> None:
        self.kon = kon
        self.olaylar = olay_kuyrugu
        self.kuyruklar = kuyruklar
        self._rnd_cift = akislar["trafik_ciftleri"]
        self._rnd_zaman = akislar["trafik_zamani"]
        self._sonraki_kimlik = 0
        self.uretilen_paketler: list[Paket] = []

        self.akislar_listesi = self._ciftleri_sec(topo)

    # ------------------------------------------------------------ çift seçimi
    def _ciftleri_sec(self, topo: Topoloji) -> list[Akis]:
        aday = topo.ulasilabilir_ciftler()
        istenen = self.kon.aktif_cift
        if len(aday) < istenen:
            raise RuntimeError(
                f"ulaşılabilir çift sayısı yetersiz: {len(aday)} < {istenen}. "
                f"Topoloji çok seyrek — parametreler ölçülmeden değiştirilmemeli."
            )
        secilen = self._rnd_cift.sample(aday, istenen)

        # Her akış [0, cbr_araligi) aralığında rastgele bir fazda başlar.
        return [
            Akis(
                kaynak=k,
                hedef=h,
                ilk_gonderim_s=self._rnd_zaman.uniform(0.0, self.kon.cbr_araligi_s),
            )
            for (k, h) in secilen
        ]

    # ------------------------------------------------------------- başlat
    def basla(self) -> None:
        """Tüm akışların ilk gönderimlerini olay kuyruğuna koyar.

        Trafik t=0'da başlar (ısınma dahil). Isınma boyunca üretilen
        paketler METRİKLERE girmez ama korunum defterine GİRER — ikisi
        ayrı defterdir.
        """
        for akis in self.akislar_listesi:
            self.olaylar.ekle(akis.ilk_gonderim_s, self._uret, akis)

    # --------------------------------------------------------------- üretim
    def _uret(self, akis: Akis) -> None:
        simdi = self.olaylar.simdi

        # Üretim ölçüm penceresi bitiminde DURUR; kalan süre boşaltmadır.
        #
        # 🔴 B-13: bu bir ERKEN DÖNÜŞ değil, DEĞİŞMEZ. Ölçüldü: 10 869 çağrının
        # 0'ında tetiklendi — çünkü olay ekleme tarafı (`_uret` sonundaki
        # `if simdi + sonraki <= olcum_bitis_s`) zaten engelliyor. Erken dönüş
        # olarak bırakmak, koruma sağlamadan koruma izlenimi verirdi.
        # Assert olarak, zamanlama mantığı bozulursa SESSİZ kalmaz.
        assert simdi <= self.kon.olcum_bitis_s, (
            f"ölçüm penceresi dışında paket üretildi: {simdi} > "
            f"{self.kon.olcum_bitis_s} — olay planlama mantığı bozuk"
        )

        paket = Paket(
            kimlik=self._sonraki_kimlik,
            kaynak=akis.kaynak,
            hedef=akis.hedef,
            bayt=self.kon.paket_bayt,
            dogum_s=simdi,
            ttl=self.kon.ttl_baslangic,
        )
        self._sonraki_kimlik += 1
        self.uretilen_paketler.append(paket)
        self.kuyruklar[akis.kaynak].ekle(paket, yeni_uretilen=True)

        # Bir sonraki gönderim: sabit aralık + titreşim.
        # Titreşim simetriktir (ortalama aralığı kaydırmaz), böylece
        # "seyrek trafik" gerçekten seyrek kalır.
        sonraki = self.kon.cbr_araligi_s + self._rnd_zaman.uniform(
            -self.kon.cbr_titresim_s, self.kon.cbr_titresim_s
        )
        if simdi + sonraki <= self.kon.olcum_bitis_s:
            self.olaylar.ekle(simdi + sonraki, self._uret, akis)

    # ---------------------------------------------------------------- teşhis
    def ozet(self) -> dict[str, object]:
        return {
            "akis_sayisi": len(self.akislar_listesi),
            "uretilen_paket": len(self.uretilen_paketler),
            "farkli_hedef": len({a.hedef for a in self.akislar_listesi}),
            "farkli_kaynak": len({a.kaynak for a in self.akislar_listesi}),
        }
