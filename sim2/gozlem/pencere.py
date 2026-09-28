"""
Gözlem penceresi — bir düğümün karar anında görebildiği HER ŞEY.

🔒 ÜÇ KURAL, ÜÇÜ DE YAPISAL
===========================
  1. **Dondurulmuş.** Protokol gördüğünü değiştiremez.
  2. **Geri referans yok.** Pencerede simülatöre giden hiçbir nesne yoktur;
     `Topoloji`, `Kanal`, `Konfig`, `Paket` gibi tipler buradan
     ULAŞILAMAZ. Bir yüzey taraması testi bunu gezerek denetler.
  3. **İzin listesi.** Alanlar burada sayılıdır; yeni bir alan eklemek testi
     kırar ve gözlem sözleşmesi belgesi güncellenmeden geçilemez.

🔴 SAAT KENDİ SAATİDİR
======================
`saat_s` tipi `YerelZaman`dır, küresel zaman değil. Düğümlerin saatleri
ofset (±0,5 s) ve sapma (20 ppm) ile ayrışır; ölçüldü — 40 düğümde en büyük
ayrışma **915 ms**. Bir protokol beacon'a zaman damgası koyabilir ama alıcı
onu kendi saatiyle karşılaştırdığında bu farkı görür. Bedava kusursuz
senkron yasaklanmıyor, **imkânsız** hâle geliyor.

🔴 MOBİLİTE HİÇBİR BEDAVA ALAN EKLEMEZ
======================================
Ağ artık hareketli ama gözlem penceresine "hız", "yön" ya da "komşunun
yörüngesi" diye bir alan GELMEDİ. Hareket bilgisi isteyen protokol onu
`bildirdigi_yuk` ile taşımak ve **bayt bedelini ödemek** zorundadır.

🔴 `bildirdigi_konum` KALDIRILDI — 16 Eylül 2026 (denetim B4, `04` K-131)
========================================================================
Alan bu sözleşmede *"3B, bedeli otomatik faturalanır"* diye duruyordu ama
koşucu onu HİÇ DOLDURMUYORDU: ölçüldü, 110 605 komşu kaydının **%100'ünde**
`None`. Yani belge bir yetenek anlatıyor, kod onu vermiyordu — ve arada
kalan boşluk, okuyanın kodda olmayan bir şeye güvenmesiydi (`03` §B5:
*"belge kodun kanıtı değildir; kod belgenin kanıtıdır"*).

Doldurmak yerine KALDIRILDI ve gerekçesi sözleşmenin kendi ilkesidir: konum
isteyen protokol onu `beacon_yuku`na koyar, `bildirdigi_yuk`tan okur ve BAYT
BEDELİNİ ÖDER. Alanı simülatörün doldurması, *"konum beacon'da taşınır"*
kararını protokol adına simülatörün vermesi olurdu.

🔒 Daraltma hiçbir ölçümü bayatlatmaz: alan protokolden BAĞIMSIZ olarak hep
boştu ve hiçbir ölçüm aleti onu okumuyordu (`05` §7'nin gerektirdiği kontrol).
Yüzey 24 → **23 alan** (12 gözlem + 6 komşu + 5 paket).

🔴 BİLGİ YOKLUĞU SIFIR DEĞİLDİR — 16 Eylül 2026
===============================================
`bildirdigi_gurultu_w` ve `bildirdigi_kuyruk`, protokol beacon'a koymazsa
`0.0` / `0` dönüyordu: *"bilgi yok"* ile *"ölçülen değer sıfır"* ayrışmıyordu.
Projenin her yerinde (türev oranları, Δ, algılama duyarlılığı, pencere ikizi)
titizlikle uygulanan `None ≠ 0` kuralının TEK istisnası burasıydı. Kapandı:
koymayan protokolde alan `None` döner. Sıfır gürültü bildiren bir komşu ile
gürültü bildirmeyen bir komşu artık ayırt edilebilir.

🔴 `dogum_s` YOKTUR ve olamaz
=============================
Paketin doğum anı ölçüm tarafının bilgisidir. Pencereye konsaydı, farklı
saatlerdeki iki düğüm onu karşılaştırarak saat farkını sıfır maliyetle
öğrenirdi — kusur 9'un arka kapısı.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sim2.cekirdek.saat import YerelZaman

__all__ = [
    "KomsuKaydi", "PaketGorunumu", "Gozlem",
    "IZINLI_GOZLEM_ALANLARI", "IZINLI_KOMSU_ALANLARI",
    "IZINLI_PAKET_ALANLARI", "YASAK_TIPLER",
]


@dataclass(frozen=True, slots=True)
class KomsuKaydi:
    """Bir komşu hakkında YALNIZCA beacon'dan öğrenilenler.

    ⚠️ Bu kaydın var olması komşunun ŞU AN hayatta olduğunu göstermez.
    `son_duyulma_s` bayattır ve karıştırma altında bayatlar. Tazelik kararı
    protokole aittir; `yas_s()` ham yaşı verir, eşiği koymaz.
    """

    dugum: int
    son_duyulma_s: YerelZaman     # 🔴 ALICININ kendi saatine göre
    duyulan_beacon: int
    # Beacon'ın taşıdığı alanlar — her biri BAYTA mal olur.
    # 🔴 `None` = KOMŞU BUNU BİLDİRMEDİ. `0.0` değil: *"ölçtü ve sıfır buldu"*
    # ile *"hiç koymadı"* aynı şey değildir ve ikincisini birincisi sanan bir
    # protokol, olmayan bir ölçüme dayanarak karar verir.
    bildirdigi_gurultu_w: float | None
    bildirdigi_kuyruk: int | None
    # 🔒 PROTOKOLÜN KENDİ KOYDUĞU ALANLAR. Komşusunun girişim seviyesini ya
    # da kuyruk durumunu kullanmak isteyen protokol, o alanları başlığa
    # KOYMAK ve bedelini ÖDEMEK zorundadır. Donmuş sıralı demet: simülatöre
    # geri referans taşımaz.
    bildirdigi_yuk: tuple[tuple[str, object], ...] = ()

    def yas_s(self, simdi_s: YerelZaman) -> float:
        """Bilginin yaşı — KENDİ saatine göre."""
        return float(simdi_s) - float(self.son_duyulma_s)


@dataclass(frozen=True, slots=True)
class PaketGorunumu:
    """Paketin başlığında YAZAN alanlar. Başka bir şey görünmez.

    `kaynak_sira` kaynağın kendi paket sırasıdır; `(kaynak, kaynak_sira)`
    paketi tanır. Küresel paket kimliği bilerek YOK: iki paketin küresel
    kimlik farkı bütün ağın ürettiğini söylerdi (`v2/05` §3.3, K-157).
    """

    hedef: int
    kaynak: int
    ttl: int
    atlama_sayisi: int
    bayt: int
    kaynak_sira: int


@dataclass(frozen=True, slots=True)
class Gozlem:
    """Bir düğümün bir karar anında görebildiği HER ŞEY."""

    # --- kimlik ve zaman ---------------------------------------------
    dugum: int
    saat_s: YerelZaman            # 🔴 KENDİ saati. Senkron DEĞİL.

    # --- kendi donanımından ölçtükleri -------------------------------
    olculen_gurultu_w: float
    kanal_mesgul_mu: bool
    kuyruk_uzunlugu: int
    kuyruk_kapasitesi: int

    # --- iletim geçmişi ----------------------------------------------
    # ⭐ En ucuz ve en önemli bilgi. Sıfır bayt: kendi denemesinin sonucu.
    son_iletim_sonucu: str | None      # "onay" | "zaman_asimi" | None
    son_iletim_hedefi: int | None
    gonderilen_bayt: int
    alinan_bayt: int

    # --- komşular: YALNIZCA beacon'dan -------------------------------
    komsular: tuple[KomsuKaydi, ...] = field(default_factory=tuple)

    # --- taşınan paket -----------------------------------------------
    paket: PaketGorunumu | None = None

    # --- kendi GPS/INS'i ve telsiz sayaçları — `v2/15` B3 (K-179) ----
    # 🔒 Gerçek bir otopilotun ve telsizin verdiği şeyler (`v2/05` §3.1a):
    # kendi konumu ve hızı (GPS/INS, hatalı) · CCA'nın meşgul kaldığı toplam
    # süre (sürücülerin "channel busy time" sayacı; protokol oranı kendi
    # penceresinde hesaplar — yalnız `kanal_dolulugu_ister` diyen protokole,
    # ötekinde `None` = ölçülmedi) · kilitlenip gövdesi çözülemeyen çerçeve
    # sayısı · başarıyla çözülen çerçeve sayısı. Komşunun hareketi YOK.
    kendi_konum: tuple[float, float, float] | None = None
    kendi_hiz: tuple[float, float, float] | None = None
    mesgul_sure_s: float | None = None
    phy_hata: int = 0
    alinan_cerceve: int = 0

    def komsu(self, dugum: int) -> KomsuKaydi | None:
        for k in self.komsular:
            if k.dugum == dugum:
                return k
        return None

    @property
    def kuyruk_doluluk(self) -> float:
        return self.kuyruk_uzunlugu / self.kuyruk_kapasitesi


# ==========================================================================
# İZİN VERİLEN YÜZEY — testin dayandığı listeler
#
# Listede olmayan bir alan eklenirse yüzey testi KIRILIR ve gözlem
# sözleşmesi belgesi güncellenmeden geçilemez.
# ==========================================================================
IZINLI_GOZLEM_ALANLARI: frozenset[str] = frozenset({
    "dugum", "saat_s",
    "olculen_gurultu_w", "kanal_mesgul_mu",
    "kuyruk_uzunlugu", "kuyruk_kapasitesi",
    "son_iletim_sonucu", "son_iletim_hedefi",
    "gonderilen_bayt", "alinan_bayt",
    "komsular", "paket",
    # `v2/15` B3 (K-179) — kendi GPS/INS'i ve telsiz sayaçları
    "kendi_konum", "kendi_hiz", "mesgul_sure_s", "phy_hata", "alinan_cerceve",
})

IZINLI_KOMSU_ALANLARI: frozenset[str] = frozenset({
    "dugum", "son_duyulma_s", "duyulan_beacon",
    "bildirdigi_gurultu_w", "bildirdigi_kuyruk",
    "bildirdigi_yuk",
})

IZINLI_PAKET_ALANLARI: frozenset[str] = frozenset({
    "hedef", "kaynak", "ttl", "atlama_sayisi", "bayt", "kaynak_sira",
})

# 🔴 Bu tiplerden birine gözlem penceresinden ULAŞILABİLİYORSA sözleşme
# kırılmıştır. Liste yeni katmanlarla GENİŞLEDİ: `Kanal`, `Yayilim`,
# `Sonumleme`, `Karistirici`, `Saatler`, `AliciZinciri`, `Dcf` — hepsi
# kâhin bilgi taşır ve hiçbirine ulaşılmamalı.
YASAK_TIPLER: tuple[str, ...] = (
    # dünya ve yapılandırma
    "Konfig", "Topoloji", "Anlik", "Mobilite", "GaussMarkov3B",
    "GorevTabanli3B", "Kutu",
    # kanal — kâhin fiziğin tamamı
    "Kanal", "Yayilim", "Sonumleme", "Girisim", "Ortam", "Iletim",
    "Karistirici", "Cerceve",
    # MAC
    "AliciZinciri", "AlimSonucu", "Dcf", "DcfZamanlari",
    # çekirdek ve ölçüm
    "Saatler", "Akislar", "OlayKuyrugu", "KorunumDefteri", "Sayaclar",
    "Kahin", "Paket", "Kuyruk", "TrafikUreteci",
)
