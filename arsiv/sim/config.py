"""
Konfigürasyon nesnesi.

Bu projedeki HER deney kolu bir bayrak değişikliğidir. Kod düzenleyerek
üretilen bir kol, kaynağından ayırt edilemez ve kaybolmuş bir deneydir.
(03-YONTEM-KURALLARI.md, Bölüm B1)

Nesne dondurulmuştur (frozen): bir koşu başladıktan sonra konfigürasyon
değiştirilemez. Bu kasıtlıdır — koşu ortasında değişen bir parametre,
sonuç satırındaki konfigürasyonu yalancı yapar.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, asdict, field
from typing import Any, ClassVar


# --------------------------------------------------------------------------
# Senaryolar — 06-ON-KAYIT.md, "SENARYOLAR" tablosu
# --------------------------------------------------------------------------
SENARYOLAR = ("S0", "S1", "S2", "S3", "S4", "S5")

TRAFIK_SEVIYELERI = ("yogun", "orta", "seyrek")


# --------------------------------------------------------------------------
# SENARYO TANIMLARI — güçler ÖLÇÜMLE seçildi (K-019)
# --------------------------------------------------------------------------
# 🔴 TABLO 19 AĞUSTOS 2026'DA YENİDEN ÜRETİLDİ (B-08, K-039).
# Üretici: `python dogrulama/kurulum_kalibrasyonu.py`
#
# Önceki hâli üretici komutu OLMAYAN ve yeniden üretilemeyen bir tabloydu;
# "sapma gereken çift" metriğinin kod karşılığı bulunamadı (denetim §7-1).
# Aşağıdaki sayılar 30 ayarlama tohumuyla, açıkça ilan edilmiş tanımlarla
# üretilmiştir (tanımlar kalibrasyon betiğinin başında).
#
# BAĞ TANIMI: MAC SONRASI (5 deneme) — simülatörün fiilen uyguladığı hâl.
#
#   güç      ulaşılabilir çift    sapma gereken çift    uçtan uca teslim
#   -10 dBm      %99,8 ± 0,1           %11,9 ± 1,3          0,8975
#    -4 dBm      %99,3 ± 0,3           %25,5 ± 1,3          0,7467   <- S1
#     0 dBm      %97,9 ± 0,5           %37,4 ± 1,6          0,6614
#    +2 dBm      %97,0 ± 0,9           %44,2 ± 1,5          0,5252   <- S2
#    +4 dBm      %91,5 ± 1,9           %48,9 ± 1,9          0,3634
#    +6 dBm      %84,8 ± 2,6           %50,3 ± 2,4          0,2456
#   +11 dBm      %52,9 ± 3,2           %35,7 ± 3,0          0,1198
#
# 🔴 SEÇİM ÖLÇÜTÜ DEĞİŞTİ (K-039). Eski ölçüt ("sapma gereken çift oranını
# en büyükle, ulaşılabilirlik %90'ın altına düşmeden") YENİDEN UYGULANAMAZ:
# metriği kurtarılamadı. Üstelik mekanik olarak uygulandığında +4 dBm'i
# seçiyor — orada uçtan uca teslim zaten 0,363, yani hiçbir protokolün
# kazanamayacağı bir nokta. Tam da kaçınmak istediği tuzak.
#
# YENİ ÖLÇÜT: çalışma noktası, uçtan uca teslim oranını taramanın DİNAMİK
# ARALIĞININ ORTASINA en yakın getiren güçtür (ulaşılabilirlik ≥ %90).
# Metrik orada her iki yönde de en çok başlığa sahiptir; tabanda/tavanda
# protokol farkları sıkışır. (03-YONTEM-KURALLARI.md, B3)
#
#   dinamik aralık [0,1197 · 0,8955] → orta 0,5076
#   +2 dBm → 0,5252, ortadan 0,0176 uzakta  ⇒ SEÇİLEN
#   kısıtla elenen: +6 (%84,0) · +8 (%73,3) · +10 (%57,1) · +11 (%49,1)
#
# ⚠️ SAYILAR 20 AĞUSTOS'TA YENİDEN ÖLÇÜLDÜ (B-28). Öncekiler
# (0,5234 · [0,1198 · 0,8975] · 0,5087) B-10'un RNG kaymasından ÖNCE
# üretilmişti; K-041 B-16/B-18'i yeniden ölçtü ama kalibrasyonu ölçmedi —
# bu oturumun ÜÇÜNCÜ "araç doğru, çıktısı bayat" vakasıydı.
# 🔒 Seçilen güç DEĞİŞMEDİ.
#
# ⚠️ Bu ölçüt taramayı GÖRDÜKTEN SONRA yazıldı; ön-kayıtlı bir seçim değil,
# mevcut çalışma noktasının BETİMLEYİCİ gerekçesidir (K-039).
#
# ⚠️ "Etki yok" ile "ağ parçalandı" arasındaki dar pencere DURUYOR ve
# kendisi rapora giren bir bulgudur.
#
# ⚠️ Darbeli senaryoların TEPE gücü, ORTALAMA gücü karşılığı sabit senaryoya
# eşitleyecek şekilde yükseltilir. H1.3'ün "aynı ortalama güçte" koşulu budur.
#
# 🔴 B-07 DÜZELTMESİ (19 Ağustos 2026) — İKİNCİ "DOĞRU" KAYNAĞI KALDIRILDI
# ---------------------------------------------------------------------------
# Önceki hâlde bu tablo, `_TEPE_TELAFI_DB = 10·log10(1/_DARBE_GOREV)` modül
# sabitiyle ÖNCEDEN hesaplanmış TEPE güçleri taşıyordu. Görev çevrimi ise
# ayrı bir `Konfig` alanıydı (`darbe_gorev_cevrimi`) ve `__post_init__`
# yalnızca (0, 1] aralığını kontrol ediyordu. İkisi BAĞIMSIZ değişebiliyordu.
#
# Bağımsız denetimin ölçtüğü (aile0_audit.md, B-07):
#     görev çevrimi   S1 ort. güç   S3 ort. güç   fark
#     0,50 (varsayılan)  -113,083     -113,083     0,000 dB   ✅
#     0,25               -113,083     -116,093    -3,010 dB   ❌
#     0,10               -113,083     -120,071    -6,988 dB   ❌
# Yani `darbe_gorev_cevrimi` bir tarama ekseni olarak kullanıldığı an H1.3
# SESSİZCE başka bir soruya dönüşüyordu. Ç3.3 bunu göremiyordu çünkü yalnızca
# varsayılan görev çevriminde koşuyordu.
#
# Tablo artık TEPE değil, EŞDEĞER SABİT GÜCÜ taşır; tepe telafisi tek yerden,
# `Konfig.tepe_telafisi_db` üzerinden türetilir. Alan adı da değişti
# (`guc_dbm` → `esdeger_sabit_guc_dbm`): eski adı okuyan bayat bir kod artık
# yanlış sayı değil, `KeyError` alır.
#
# ⚖️ Varsayılan görev çevriminde (0,5) telafi 10·log10(2) = 3,0103 dB'dir —
# yani S3/S4 tepe güçleri bit-birebir DEĞİŞMEZ. Değişmemesi gereken şeyin
# değişmediği `test_b07_...` ile ayrıca ölçülür (Y6).

SENARYO_TANIMLARI: dict[str, dict] = {
    "S0": dict(esdeger_sabit_guc_dbm=None, darbeli=False, hareketli=False),
    "S1": dict(esdeger_sabit_guc_dbm=-4.0, darbeli=False, hareketli=False),
    "S2": dict(esdeger_sabit_guc_dbm=+2.0, darbeli=False, hareketli=False),
    "S3": dict(esdeger_sabit_guc_dbm=-4.0, darbeli=True,  hareketli=False),
    "S4": dict(esdeger_sabit_guc_dbm=+2.0, darbeli=True,  hareketli=False),
    "S5": dict(esdeger_sabit_guc_dbm=+2.0, darbeli=False, hareketli=True),
}

# H1.2 (dirsek) taraması: etkisizden bölünmeye kadar tüm pencereyi kapsar.
# Genişlik kontrolü ön-kayıtta: taranan teslim aralığı tohum std'sinin
# en az 3 katı olmalı, yoksa hipotez TEST EDİLMEMİŞ sayılır.
DIRSEK_TARAMASI_DBM = (-10.0, -7.0, -4.0, -1.0, 2.0, 5.0, 8.0, 11.0)


@dataclass(frozen=True)
class Konfig:
    """Bir koşuyu tam olarak belirleyen her şey.

    Kural: bu nesnede olmayan hiçbir şey koşunun davranışını etkilemez.
    Bir davranış bu nesneden okunmuyorsa, o davranış yeniden üretilemez.
    """

    # ---- kimlik -----------------------------------------------------------
    kol: str                      # hangi protokol kolu
    senaryo: str = "S2"           # S0..S5
    trafik: str = "orta"          # yogun | orta | seyrek
    tohum: int = 1000

    # ---- zaman (saniye) ---------------------------------------------------
    # 04-NEDEN-BOYLE.md K-008: 50 ısınma + 270 ölçüm + 30 boşaltma = 350
    isinma_s: float = 50.0
    olcum_bitis_s: float = 320.0      # trafik üretimi burada durur
    kosu_bitis_s: float = 350.0       # boru bu aralıkta boşalır

    # ---- ağ ---------------------------------------------------------------
    # 40 düğüm / 280 m: ölçümle seçildi, bkz. K-017.
    # 30/250 denendi ve ELENDİ: 30 tohumun yalnızca 7'si bağlıydı ve en büyük
    # bileşen 10–30 arasında geziniyordu — protokol farkını gömecek bir varyans.
    dugum_sayisi: int = 40
    alan_m: float = 1000.0
    iletim_menzili_m: float = 280.0

    # Bağlantı koşullaması — K-017, sayılar K-039'da DÜZELTİLDİ.
    # Üretici: `python dogrulama/kurulum_kalibrasyonu.py --a` (200 000 çekim)
    #   doğal bağlantı oranı : %82,93
    #   ortalama deneme      : 1,2058
    #   derece kayması       : −%0,364 ± 0,026
    #
    # 🔴 ÖNCEKİ YORUM "%0,9" YAZIYORDU VE İŞARETİ TERSTİ. Koşullama
    # dereceyi YÜKSELTMİYOR, DÜŞÜRÜYOR: bağlı yerleşimler daha seyrek
    # olanları değil, daha az yoğunlaşmış olanları içeriyor.
    # Nitel sonuç değişmiyor: |kayma| < %1, yani gürültü mertebesinde.
    baglanti_kosullamasi: bool = True
    topoloji_max_deneme: int = 500

    # ---- fiziksel katman --------------------------------------------------
    bit_hizi_bps: float = 1e6
    # PLCP önbelgesi + başlığı: 802.11b uzun önbelge, 1 Mbit/s'te 192 µs.
    # ⚠️ Küçük gibi görünür ama ONAY çerçevesi için baskın maliyettir:
    # 14 baytlık bir onay 112 µs sürerken önbelgesi 192 µs'dir.
    onbelge_s: float = 192e-6
    bant_genisligi_hz: float = 1e6
    frekans_hz: float = 2.4e9
    yol_kaybi_usteli: float = 3.0        # α — kentsel/engelli ortam
    sinr_esigi_db: float = 10.0          # β — bu SINR'de menzil sınırı tanımlı
    gurultu_figuru_db: float = 6.0
    sicaklik_k: float = 290.0

    # ---- karıştırıcı ------------------------------------------------------
    # 🔴 Güç ve tip SENARYODAN TÜRETİLİR — elle ayarlanmaz.
    # Elle ayarlanabilseydi "S2" etiketli iki koşu farklı karıştırıcı
    # taşıyabilirdi ve sonuç satırındaki etiket yalan söylerdi.
    #
    # Tek istisna: H1.2 dirsek taraması. O da açık bir alanla yapılır ki
    # sonuç satırında görünsün.
    # ⚠️ Bu değer NİHAİ güçtür: tepe telafisi UYGULANMAZ. Dirsek taraması
    # sabit senaryolarda koşulur; darbeli bir senaryoyla birleştirilmesi
    # `__post_init__`te reddedilir (B-07: ikinci doğru kaynağı).
    karistirici_guc_override_dbm: float | None = None

    karistirici_konum: tuple[float, float] | None = None   # None → alanın merkezi
    darbe_periyodu_s: float = 2.7        # ⚠️ CBR aralığının (1,0 s) tam katı DEĞİL
    # 🔴 TEK DOĞRU KAYNAĞI (B-07). Tepe telafisi bundan TÜRETİLİR;
    # `SENARYO_TANIMLARI` artık eşdeğer sabit gücü taşır.
    darbe_gorev_cevrimi: float = 0.5
    # 15 m/s (~54 km/h). K-026'da 20,944'e cikarilmisti, K-035'te GERI ALINDI.
    #
    # K-026'nin gerekcesi: yorunge periyodunu yakinsama dilimine (pencere/3
    # = 90 s) tam esitlemek, dilimlerin yorungenin farkli fazlarini gormesini
    # engeller. Savunma: "ortusme DEGIL, cunku faz her tohumda rastgelelenir;
    # kaldirilan yalnizca YANLILIK."
    #
    # 🔴 BU SAVUNMA OLCUMLE CURUTULDU (bagimsiz denetim + kendi tekrarim).
    # Topoloji ve trafik sabit, YALNIZCA faz tarandiginda:
    #     periyot  90 s (hizali) -> teslim std 0,00256 · dilim farki 0,0094
    #     periyot 115 s          -> teslim std 0,00846 · dilim farki 0,0560
    # Faz kaynakli varyans 3,3 kat, dilim farki 6 kat BASTIRILIYOR.
    # `03` B6'nin ortusme tanimi birebir gerceklesmis.
    #
    # ⚖️ Asil mesele sayi degil: bir KAPI atesledi diye bir FIZIKSEL parametre
    # degistirilmisti (kural 3 ve 12). Dogru cozum metrigi duzeltmekti;
    # `yakinsama_kontrolu` artik yorunge-hizali dilim kullaniyor.
    karistirici_hiz_ms: float = 15.0
    karistirici_yorunge_yaricap_m: float = 300.0

    # ---- trafik -----------------------------------------------------------
    paket_bayt: int = 1024
    cbr_araligi_s: float = 1.0
    cbr_titresim_s: float = 0.05      # periyodik süreçlerin kilitlenmesini kırar
    aktif_cift_sayisi: dict[str, int] = field(
        default_factory=lambda: {"yogun": 20, "orta": 10, "seyrek": 4}
    )

    # ---- kuyruk -----------------------------------------------------------
    # Sonsuz kuyruk yasak: gecikme metriğini anlamsızlaştırır.
    # (07-SIMULATOR-ARAYUZ.md, "KUYRUKLAR")
    kuyruk_kapasitesi: int = 50

    # ---- TTL --------------------------------------------------------------
    # TTL olmadan bir döngüye giren paket "uçuşta" olarak sonsuza dek asılı kalır.
    ttl_baslangic: int = 32

    # ---- kanal ------------------------------------------------------------
    # Kanal rastgeleliği sıralı akıştan DEĞİL, (tohum, gönderen, alan, dilim)
    # dörtlüsünün hash'inden gelir. Sebep: rng.py başındaki açıklama.
    #
    # DEĞER 1 ms'den 100 µs'ye indirildi — bir MARJ KARARI olarak.
    #
    # ⚠️ BU YORUM 19 AĞUSTOS 2026'DA DÜZELTİLDİ (B-05).
    # Önceki hâli, K-024'ün ÇÜRÜTTÜĞÜ bir iddiayı olgu gibi sunuyor ve
    # kaynak olarak K-024'ü gösteriyordu: "1 ms iken yeniden denemeler aynı
    # dilime düşüyordu." Bu YANLIŞTIR.
    #
    # 🔴 27 AĞUSTOS 2026 — B-108: BURADAKİ SAYI ÜRETİLEMİYORDU.
    # Eskiden şöyleydi: "K-024'te ölçülen: ardışık deneme başlangıçları arası
    # 9528–18068 µs ... 1 ms dilimde de çakışma HİÇ olmuyordu."
    #
    # K-024'ün ölçümü TEK BİR MESAJIN 7 denemesinden, yani n = 6 aralıktan
    # çıkmıştı (Y4: tek noktada tutan sonuç doğrulama sayılmaz). Bağımsız
    # olarak yeniden ölçüldü — 4 yapılandırma, 54 463 ardışık çift:
    #
    #     min 124 µs · ortanca 19 292 µs
    #     100 µs dilimde çakışma: 0   ·   1 ms dilimde çakışma: 14
    #
    # ⚖️ Aralık rakamı bayat; KARAR daha güçlü çıktı. `kanal_cekimi` anahtarı
    # (gonderen, alan, dilim) olduğu için aynı bağdaki HERHANGİ iki iletim
    # aynı dilimdeyse aynı çekimi paylaşır — yalnızca yeniden denemeler
    # değil. O popülasyonda 1 ms YETMİYOR, 100 µs yetiyor.
    #
    # Üretici: `python dogrulama/deneme_araliklari.py`
    #
    # 100 µs neden duruyor: güvenlik payı çerçeve süresine bağlı. Çerçeve
    # küçüldükçe pay daralır; 100 µs bu bağımlılığı ortadan kaldırır.
    # Değişmez `tests/test_rng.py::test_dilim_en_kucuk_cerceveyle_bile_guvenli`
    # ile korunuyor — dizgi eşleşmesiyle değil, gerçek hesapla.
    kanal_dilimi_s: float = 1e-4

    # ---- MAC (CSMA/CA) ----------------------------------------------------
    # 802.11b değerleri.
    slot_s: float = 20e-6
    sifs_s: float = 10e-6
    # Kanal degerlendirme (CCA) gecikmesi. 802.11 spesifikasyonu 4 us icinde
    # algilama ister. SIFIR OLAMAZ: sifir olsaydi bir dugum baskasinin
    # iletimini baslama aninda gorurdu ve geri sayimi ayni slotta biten iki
    # dugum ASLA carpismazdi. Ayni-slot carpismasi 802.11 in temel
    # cakisma kaynagidir; onu silmek verimi sessizce sisirir.
    cca_s: float = 4e-6
    cw_min: int = 31
    cw_max: int = 1023
    yeniden_deneme_siniri: int = 4
    onay_bayt: int = 14

    # ---- kontrol düzlemi --------------------------------------------------
    # K-009: tüm kollar EŞİT kontrol bütçesiyle koşar.
    beacon_araligi_s: float = 1.0
    beacon_bayt: int = 32
    # Komsu tablosunda bir kaydin tutulacagi ust sinir (beacon araliginin kati).
    # ⚠️ Bu bir PROTOKOL parametresi DEGIL, bellek sinirlamasidir. Tazelik
    # karari protokole aittir: `KomsuKaydi.yas_s()` ham yasi verir.
    # Genis tutuluyor ki protokol kararini kisitlamasin.
    komsu_omru_katsayisi: float = 10.0

    # ---- H1.1 mekanizma kapısı --------------------------------------------
    # 🔴 ÖN-KAYIT (`06`, H1.1) BU BANDI İLAN ETTİ:
    #   "mekanizma kontrolü 'seçilen rotalarda ARA BÖLGE BAĞI
    #    (0,05 ≤ PER ≤ 0,9) kaç kez kullanıldı' olacak. Bu sayaç düşmüyorsa
    #    teslimdeki fark başka bir sebepten geliyor demektir ve SONUCA
    #    BAKILMAZ."
    #
    # Bant BURADA, TEK YERDE tanımlıdır. K-020 "133 bağın 11–17'si ara
    # bölgede" diyor ama BANDI YAZMIYOR ve ikinci denetim onu yeniden
    # üretemedi (bu bantla 6, [0,01·0,99] ile 11–26 çıkıyor). Bandın iki
    # yerde olması ya da hiçbir yerde olmaması aynı sonucu verir: sayı
    # yeniden üretilemez.
    ara_bolge_per_bandi: tuple[float, float] = (0.05, 0.9)

    # ---- ablasyon bayrakları ---------------------------------------------
    # Her mekanizma ayrı bir bayrak. İleride Aile 2/3 kolları buraya eklenecek.
    #
    # 🔴 B-06: BU İKİSİ HENÜZ UYGULANMAMIŞTIR ve `True` yapılamaz.
    # Önceki hâlde hiçbir kod onları okumuyordu, ama `sozluk()` `asdict()`
    # kullandığı için HER SONUÇ SATIRINA yazılıyorlardı. Somut risk:
    # `bayat_bilgi_null=True` ile koşan biri hiçbir şeyin değişmediğini fark
    # etmez, ama sonuç satırı "null model kolu" diye etiketlenmiş olur —
    # `03` B5'in "etiketi elle taşımak" tuzağının en kötü hâli, çünkü etiket
    # OTOMATİK taşınıyor ve yalan söylüyor. (Kural 11: bir özgünlük iddiasını,
    # onu üreten kod satırını gösteremeden yazma.)
    #
    # Silinmediler çünkü `06-ON-KAYIT.md` bunları Aile 2'nin kolları olarak
    # ilan ediyor; silmek tasarım niyetini de silerdi. Uygulandıklarında
    # `UYGULANMAMIS_BAYRAKLAR` listesinden çıkarılacaklar ve
    # `test_b06_...` otomatik olarak "metrik değişiyor mu" sormaya başlayacak.
    takvimli_tazeleme: bool = False
    bayat_bilgi_null: bool = False     # null model: aynı güncelleme sayısı, sıfır bilgi

    # Bildirilmiş ama uygulanmamış bayraklar. ClassVar → alan DEĞİL,
    # `asdict()`e ve dolayısıyla sonuç satırına girmez.
    UYGULANMAMIS_BAYRAKLAR: ClassVar[tuple[str, ...]] = (
        "takvimli_tazeleme", "bayat_bilgi_null",
    )

    # ---- serbest not ------------------------------------------------------
    not_: str = ""

    def __post_init__(self) -> None:
        if self.senaryo not in SENARYOLAR:
            raise ValueError(f"bilinmeyen senaryo: {self.senaryo}")
        if self.trafik not in TRAFIK_SEVIYELERI:
            raise ValueError(f"bilinmeyen trafik seviyesi: {self.trafik}")
        if not (0 <= self.isinma_s < self.olcum_bitis_s <= self.kosu_bitis_s):
            raise ValueError("zaman sınırları tutarsız")
        if self.sinr_esigi_db <= 0 or self.yol_kaybi_usteli <= 0:
            # Bu kontrol Li replikasyonunu da korur: girisim_orani = β^(1/α)
            # olduğundan, β > 1 (yani eşik > 0 dB) ve α > 0 iken oran
            # ZORUNLU olarak 1'den büyüktür → girişim menzili iletim
            # menzilinden geniş olur → gizli terminal mümkün olur.
            #
            # ⚠️ Ayrıca bir "girisim_orani > 1" kontrolü YAZILMADI çünkü
            # yukarıdakinden matematiksel olarak çıkar ve asla tetiklenemez.
            # Tetiklenemeyen bir kontrol, koruma sağlamadan koruma izlenimi
            # verir. (03-YONTEM-KURALLARI.md, B5: yorumun kodla çelişmesi)
            raise ValueError("SINR eşiği ve yol kaybı üsteli pozitif olmalı")
        if not (0.0 < self.darbe_gorev_cevrimi <= 1.0):
            raise ValueError("darbe görev çevrimi (0, 1] aralığında olmalı")

        # 🔴 B-06 — bildirilmiş ama uygulanmamış bayrak açılamaz.
        # "Bildirim ≠ kullanım" (03 B5): bir bayrağın sonuç satırına yazılması,
        # onu OKUYAN bir kod olduğu anlamına gelmez. Sessizce etkisiz kalmak
        # yerine gürültülü biçimde durur.
        for _ad in self.UYGULANMAMIS_BAYRAKLAR:
            if getattr(self, _ad):
                raise NotImplementedError(
                    f"{_ad!r} bayrağı bildirilmiş ama HENÜZ UYGULANMADI. "
                    f"True yapmak hiçbir metriği değiştirmez; sonuç satırı "
                    f"yalan söylerdi. Uygulandığında Konfig."
                    f"UYGULANMAMIS_BAYRAKLAR listesinden çıkarılmalı."
                )

        # 🔴 B-07 — override NİHAİ güçtür, tepe telafisi uygulanmaz.
        # Darbeli bir senaryoyla birleştirilirse "aynı ortalama güç" koşulu
        # sessizce kırılır ve H1.3 başka bir soruya dönüşür.
        if (self.karistirici_guc_override_dbm is not None
                and SENARYO_TANIMLARI[self.senaryo]["darbeli"]):
            raise ValueError(
                "karistirici_guc_override_dbm darbeli bir senaryoyla "
                "birleştirilemez: override nihai güçtür, tepe telafisi "
                "uygulanmaz ve H1.3'ün 'aynı ortalama güç' koşulu kırılır. "
                "Darbeli bir güç taraması gerekiyorsa 04-NEDEN-BOYLE.md'ye "
                "kayıt düşülerek ayrı bir alan açılmalı."
            )
        if self.kuyruk_kapasitesi <= 0:
            raise ValueError("kuyruk kapasitesi sonlu ve pozitif olmalı")
        if self.ttl_baslangic <= 0:
            raise ValueError("TTL pozitif olmalı")

    # ---------------------------------------------------------------- yardım
    @property
    def girisim_orani(self) -> float:
        """Girişim menzilinin iletim menziline oranı — TÜRETİLMİŞ.

        Elle yazılmış bir sayı DEĞİL. Türetimi:

        Menzil sınırında (d = R) girişimsiz SINR tam olarak eşiğe (β) eşittir:
            P_sinyal(R) / N = β

        D mesafesindeki bir karıştırıcının/girişimcinin gücü gürültü tabanına
        eşit olduğunda, o girişimci "hissedilir" hâle gelir:
            P(D) = N
            Pt / (K·D^α) = Pt / (K·R^α·β)
            D^α = β·R^α
            D = β^(1/α) · R

        β = 10 dB, α = 3 için: 10^(1/3) ≈ 2,154

        ⭐ Bunu türetmenin bedeli sıfır, kazancı büyük: radyo modeliyle
        topolojinin girişim varsayımı artık ASLA çelişemez. Elle yazılmış
        2,2 değeri, β veya α değiştiğinde sessizce yanlış olurdu.
        """
        beta_lin = 10.0 ** (self.sinr_esigi_db / 10.0)
        return beta_lin ** (1.0 / self.yol_kaybi_usteli)

    @property
    def girisim_menzili_m(self) -> float:
        """Türetilmiş — bağımsız parametre değil. Tek doğru kaynağı."""
        return self.iletim_menzili_m * self.girisim_orani

    # ------------------------------------------------------- karıştırıcı
    @property
    def tepe_telafisi_db(self) -> float:
        """Darbeli karıştırıcının tepe gücüne eklenen telafi — TÜRETİLMİŞ.

        Ortalama güç = tepe × görev çevrimi. Ortalamayı sabit karşılığına
        eşitlemek için tepeyi 1/d kadar yükseltmek gerekir:
            +10·log10(1/d) dB
        d = 0,5 için 3,0103 dB.

        🔴 B-07: bu bir MODÜL SABİTİ DEĞİL. Sabit olduğunda `darbe_gorev_cevrimi`
        ile ikinci bir "doğru" kaynağı oluşuyordu ve ikisi bağımsız
        değişebiliyordu. Türetilmiş hâlinde ikisi ASLA çelişemez.
        """
        return 10.0 * math.log10(1.0 / self.darbe_gorev_cevrimi)

    @property
    def karistirici_guc_dbm(self) -> float | None:
        """Karıştırıcının TEPE gücü — senaryodan türetilir.

        Sabit senaryolarda tepe = ortalama. Darbeli senaryolarda tepe,
        eşdeğer sabit gücün üstüne `tepe_telafisi_db` eklenerek bulunur;
        böylece ORTALAMA güç sabit karşılığına eşit kalır (H1.3'ün koşulu).

        Override yalnızca dirsek taraması (H1.2) içindir ve NİHAİ güçtür;
        darbeli senaryoyla birleşimi `__post_init__`te reddedilir.
        """
        if self.karistirici_guc_override_dbm is not None:
            return self.karistirici_guc_override_dbm
        taban = SENARYO_TANIMLARI[self.senaryo]["esdeger_sabit_guc_dbm"]
        if taban is None:
            return None
        return taban + self.tepe_telafisi_db if self.karistirici_darbeli else taban

    @property
    def esdeger_sabit_guc_dbm(self) -> float | None:
        """Darbeli senaryonun eşitlendiği SABİT senaryo gücü (ortalama güç).

        H1.3 çiftleri bu değerle tanımlıdır: S1↔S3 ve S2↔S4 aynı eşdeğer
        sabit güce sahiptir. Rapora giren "aynı ortalama güçte" cümlesinin
        koddaki karşılığı budur.
        """
        return SENARYO_TANIMLARI[self.senaryo]["esdeger_sabit_guc_dbm"]

    @property
    def karistirici_darbeli(self) -> bool:
        return SENARYO_TANIMLARI[self.senaryo]["darbeli"]

    @property
    def karistirici_hareketli(self) -> bool:
        return SENARYO_TANIMLARI[self.senaryo]["hareketli"]

    @property
    def karistirici_var_mi(self) -> bool:
        return self.karistirici_guc_dbm is not None

    @property
    def karistirici_merkez(self) -> tuple[float, float]:
        """Varsayılan: alanın merkezi.

        Merkez seçildi çünkü tohumlar arasında KARŞILAŞTIRILABİLİR: rastgele
        bir karıştırıcı konumu, tohumlar arası varyansa karıştırıcının nereye
        düştüğünü de katardı ve protokol farkını gizlerdi.
        """
        return self.karistirici_konum or (self.alan_m / 2.0, self.alan_m / 2.0)

    def cerceve_suresi_s(self, bayt: int) -> float:
        """Önbelge + yük. Analitik doğrulama hedefi (Aile 0, K3)."""
        return self.onbelge_s + (bayt * 8) / self.bit_hizi_bps

    @property
    def paket_suresi_s(self) -> float:
        return self.cerceve_suresi_s(self.paket_bayt)

    @property
    def onay_suresi_s(self) -> float:
        return self.cerceve_suresi_s(self.onay_bayt)

    @property
    def komsu_omru_s(self) -> float:
        return self.beacon_araligi_s * self.komsu_omru_katsayisi

    @property
    def difs_s(self) -> float:
        return self.sifs_s + 2 * self.slot_s

    @property
    def olcum_penceresi(self) -> tuple[float, float]:
        """Metriklerin hesaplandığı aralık. Korunum denklemi BU aralıkta DEĞİL,
        tüm koşu üzerinden kontrol edilir — ikisi ayrı defterdir."""
        return (self.isinma_s, self.olcum_bitis_s)

    @property
    def aktif_cift(self) -> int:
        return self.aktif_cift_sayisi[self.trafik]

    def sozluk(self) -> dict[str, Any]:
        """Sonuç satırına yazılacak tam konfigürasyon."""
        return asdict(self)
