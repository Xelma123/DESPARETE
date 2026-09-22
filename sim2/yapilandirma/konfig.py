"""
Konfigürasyon — bir koşuyu TAM olarak belirleyen her şey.

🔒 KURAL
========
Bu nesnede olmayan hiçbir şey koşunun davranışını etkilemez. Bir davranış
buradan okunmuyorsa, o davranış **yeniden üretilemez**. Her deney kolu bir
bayrak değişikliğidir; kod düzenleyerek üretilen bir kol kaynağından ayırt
edilemez ve kaybolmuş bir deneydir.

Nesne dondurulmuştur: koşu başladıktan sonra değişemez. Koşu ortasında değişen
bir parametre, sonuç satırındaki konfigürasyonu yalancı yapar.

🔴 BURADA OLMAYAN İKİ ŞEY — kasıtlı
===================================
1. **Çerçeve süresi yok.** Eski simülatörde iki farklı PER tanımı vardı ve
   ölçüldü: 1024 B @ 1 Mb/s'te %2,34 ayrışıyorlardı. Yeni parametrelerde
   (512 B @ 2 Mb/s) aynı ayrışma **%9,38** olurdu — önbelge sabit kalıp yük
   yarıya indiği için kusur 4 kat büyüyor. Çerçeve süresi ve hataya açık bit
   `kanal/cerceve.py`de **tek yerde** tanımlanır; buraya bir kolaylık
   fonksiyonu koymak ikinci bir bit sayımı doğururdu.
   Üretici: `python kalibrasyon/adim3_oncesi.py`

2. **Kutu nesnesi yok.** Katman yönü `yapilandirma → dunya`dır; bu modülün
   `dunya`yı içe aktarması yönü tersine çevirirdi. Kutuyu `dunya` katmanı
   bu alanlardan kurar.

⚠️ ISINMA SÜRESİ HENÜZ ÖLÇÜLMEDİ
================================
`isinma_s = 50` eski depodan gelen bir DEVİRDİR, yeni dünyada ölçülmedi.
Mobilite yakınsamayı geciktirebilir (mobil kolda ağ zamanın %17,6'sında
bölünmüş durumda).
Ön-kayıt mühürlenmeden önce `isinma_s ∈ {50, 100, 150, 200}` taranacak ve
erken/geç pencere farkının söndüğü nokta yazılacak (risk 5).
"""

from __future__ import annotations

import dataclasses as _dc
import math
from dataclasses import asdict, dataclass
from typing import Any, ClassVar

from sim2.cekirdek.degismezler import DegismezHatasi as _DegismezHatasi
from sim2.cekirdek.degismezler import dogrula
from sim2.yapilandirma import kokenler as _kokenler
from sim2.yapilandirma.senaryolar import (
    KARISTIRICI_GUCU_DBM, SENARYOLAR, TEHDIT_SENARYOLARI, TRAFIK_DESENLERI,
    UYGULANMAMIS_KARISTIRICI)

__all__ = ["Konfig", "HENUZ_OKUNMAYAN"]


# 🔒 `rng.HENUZ_KULLANILMAYAN`ın Konfig'deki karşılığı.
# Bir alan ya fiilen bir `sim2/` modülü tarafından OKUNUR ya BURADA yazılıdır.
# Üçüncü bir hâl yok: "bildirilmiş ama kimse okumuyor" durumu sonuç satırına
# yazılan ama hiçbir şeyi etkilemeyen bir parametre demektir ve satırı yalancı
# yapar. Liste, modüller indikçe KISALIR; testi iki yönlü çalışır.
HENUZ_OKUNMAYAN: frozenset[str] = frozenset({
    # 🔒 Adım 9 (`kosum/`) yazıldıktan sonra listeden ÇIKANLAR — 5 Eylül 2026:
    #   saat_senkron · saat_ofset_araligi_s · saat_sapma_ppm  → `kurulum.py`
    #   kuyruk_kapasitesi                                     → `kurulum.py`
    #   beacon_araligi_s                                      → `kosu.py`
    #   kol · not_ · senaryo                                  → `sonuc.py`
    # Liste, modüller indikçe KISALMAK zorunda ve bir test bunu bağlıyor.
    #
    # zaman — `isinma_s` yalnız `olcum_penceresi` özelliği üzerinden okunuyor;
    # bir alanın kendi türetilmiş özelliğince okunması onun bir DAVRANIŞI
    # etkilediğini kanıtlamaz, o yüzden listede kalıyor.
    "isinma_s",
    # kontrol düzlemi — `komsu_omru_katsayisi` de yalnız kendi türetilmiş
    # özelliği (`komsu_omru_s`) üzerinden okunuyor.
    "komsu_omru_katsayisi",
    # karıştırıcı — `karistirici_guc_override_dbm` ve `karistirici_konum`
    # yalnız `Konfig`in kendi türetilmiş özelliklerince okunuyor.
    "karistirici_guc_override_dbm", "karistirici_konum",
})


@dataclass(frozen=True)
class Konfig:
    # ==================================================================
    # KİMLİK
    # ==================================================================
    kol: str                          # hangi protokol kolu
    senaryo: str = "statik-yok"       # `senaryolar.SENARYOLAR` anahtarı
    tohum: int = 1000

    # ==================================================================
    # ZAMAN (saniye)
    # ==================================================================
    # 50 ısınma + 270 ölçüm + 30 boşaltma. ⚠️ Isınma henüz ÖLÇÜLMEDİ
    # (modül başlığındaki nota bak).
    isinma_s: float = 50.0
    olcum_bitis_s: float = 320.0      # trafik üretimi burada durur
    kosu_bitis_s: float = 350.0       # boru bu aralıkta boşalır

    # ==================================================================
    # DÜNYA
    # ==================================================================
    # ⚠️ AŞAĞIDAKİ ÖLÇÜM GEÇERSİZ — 4 Eylül 2026, `kalibrasyon/adim3_oncesi.py`
    #   eski 2B  1000×1000            : derece 7,412 · bağlı %80,4
    #   3B       1000×1000×300        : derece 6,101 · bağlı %58,4
    #   3B  1000×1000, irtifa 20–120  : derece 7,271 · bağlı %78,2
    # Bu sayılar 280 m'lik GEOMETRİK grafikte hesaplandı. O grafik veri
    # yolunda kullanılmıyor: kimin duyacağını girişim menzili, alınıp
    # alınmadığını SINR belirliyor (K-096). Yani kalibrasyon, kimsenin
    # kullanmadığı bir ağı kalibre etmişti. 3B'ye geçişin ağı seyrelttiği
    # gözlemi ayakta; sayıları değil.
    #
    # 🔒 ÇALIŞMA NOKTASI — YENİDEN ÖLÇÜLDÜ, 5 Eylül 2026.
    # Üretici: `python kalibrasyon/calisma_noktasi.py`
    # Ölçüm KULLANILABİLİR BAĞ grafiğinde: gölgeleme ve sönümleme dâhil,
    # yeniden denemelerle atlama başarısı ≥ 0,90 olan bağlar.
    #
    #   1000 m (eski) : derece 18,60 · çiftlerin %0,3'ü 3+ atlama
    #   1800 m (yeni) : derece  8,67 · çiftlerin %31,0'ı 3+ atlama
    #
    # 🔴 ALAN 1000 → 1800 m. Eski alanda çiftlerin %99,7'si bir ya da iki
    # atlamaydı: yönlendirmenin ifade edebileceği fark yoktu ve tarama
    # *"protokoller arasında fark yok"* derdi — oysa ölçülemeyen şey farkın
    # yokluğu değil, başlığın yokluğuydu.
    #
    # 🔒 1800 SEÇİLMİŞ DEĞİL, TÜRETİLMİŞTİR: statik kolda 30 tohumun
    # hiçbirinde ulaşılamaz çift kalmayan EN BÜYÜK alan. 1850'de kopukluk
    # açılıyor (%0,2). Sert kısıt bağlantılılık, amaç derinlik — ölçütün
    # sıfır serbest parametresi var. Gerekçesi ve ilk ölçütün neden
    # infeasible çıktığı `calisma_noktasi.py` başlığında.
    #
    # ⚠️ HAREKETLİ kolda kopukluk sıfırlanamaz ve bu bilinen bir şeydir
    # (`senaryolar.py`): 1700 m'de bile 10 tohumun 3'ü bir anda kopuyor.
    # Bağlantılılık koşulu statik kola aittir; U1 orada koşar.
    dugum_sayisi: int = 40
    alan_en_m: float = 1800.0
    alan_boy_m: float = 1800.0

    # 🔴 ÖLÇEK — bu simülatör bir 1:N GEOMETRİK ÖLÇEK MODELİDİR.
    # Kavanoza dünya sığmaz; ölçeği düşürüp yapıyı korursun. Ağın hissettiği
    # her şey (mesafe, bağıl hız, topoloji değişimi) GÖRELİ büyüklüklere
    # bağlı olduğu için sürünün ortak hareketi ağa görünmez — kutu, sürüyle
    # birlikte hareket eden bir GÖZLEM ÇERÇEVESİDİR.
    #
    # 🔒 `olcek` FİZİĞİ DEĞİŞTİRMEZ, yalnız gerçek dünya eşlemesini verir.
    # Değerini iki kısıt birlikte belirledi:
    #   · seçilen hızlar, ölçeklenince doğrulanmış İHA aralığına düşmeli
    #     (30–400 km/h, A5a): 0,25–1,5 m/s × 50 → 45–270 km/h ✔
    #   · türetilen verici gücü var olabilecek bir telsiz vermeli:
    #     0,03 dBm + 20·log₁₀(50) = 34 dBm = 2,5 W ✔
    #
    # ⚠️ ÖLÇEKLENEMEYEN İKİ ŞEY VAR ve ikisi de beyan edilir:
    #   · DALGA BOYU — o yüzden Doppler tam ölçek hızından hesaplanmalı
    #   · YERÇEKİMİ — o yüzden dönüş hızı gerçek hızdan türetildi
    olcek: float = 50.0

    # 🔒 İRTİFA BANDI 20–120 m — öğrenci kararı, 4 Eylül 2026.
    # U(0,120) bir İHA'nın 0 m'de, yani yerde olmasına izin veriyordu.
    # Bedeli ölçüldü ve gürültü içinde: derece 7,210 → 7,271, bağlı
    # %77,4 → %78,2 (her ikisi de ~1 standart hata).
    #
    # 🔴 AYRI BİR `alan_yukseklik_m` YOK — olsaydı `irtifa_maks_m` ile İKİNCİ
    # bir doğru kaynağı olurdu ve ikisi bağımsız değişebilirdi. Bant, hem
    # başlangıç yerleşiminin hem de kutunun dikey sınırıdır: düğüm koşu
    # boyunca da bandın içinde kalır. Aksi hâlde karar yalnız yarım
    # uygulanırdı — ölçüldü, tabansız kutuda düğümler dakikalar içinde yere
    # (0 m) iniyordu.
    irtifa_min_m: float = 20.0
    irtifa_maks_m: float = 120.0

    # Menzil, verici gücünün TÜRETİLDİĞİ tanımdır (bkz. `girisim_orani`).
    iletim_menzili_m: float = 280.0

    # ------------------------------------------------------- 3B Gauss-Markov
    # Literatürün FANET için standart saydığı model. Random Waypoint elendi:
    # sonsuz ivme üretiyor ve ortalama hızı durağan bir değere yakınsamıyor.
    # 🔴 HIZLAR 1/50 ÖLÇEĞE ÇEKİLDİ — 8 Eylül 2026, K-101.
    # Üretici: `python kalibrasyon/calkanti.py`
    #
    # Eski değerler 10–30 m/s idi ve HİÇBİR gerekçesi yoktu. Ölçüldü:
    # bağıl hız 26,4 m/s · rota ömrü 3,2 s · **Θ = 0,21**.
    # OLSR'ın TOP_HOLD_TIME'ı 15 s (RFC 3626), yani topoloji bilgisi
    # kullanılacağı rotadan BEŞ KAT uzun ömürlü — rota öğrenilmeden yok
    # oluyordu. Bu OLSR'ın tasarımının değil BİZİM KURULUMUMUZUN sonucuydu:
    # kurulum yüzünden zayıflatılmış bir taban çizgisi, yani straw-man.
    #
    # 🔒 Θ BİR HEDEF DEĞİL, BİR KAPIDIR: Θ = rota_ömrü / 15 s ≥ 3.
    # Altına düşen bir kol protokolü tasarım zarfının DIŞINDA koşturuyor
    # demektir ve bulgu olarak raporlanır, gizlenmez.
    #
    # ⚠️ İlk şartname "çekirdek Θ ≈ 10" diyordu; ULAŞILAMIYOR. Θ = 10 için
    # 0,12–0,36 m/s gerekiyor, o da 1:50 ölçekte 22–65 km/h — doğrulanmış
    # İHA aralığının (30–400 km/h, A5a) altında. Kapı + gerçekçilik birlikte
    # uygulanınca çözüm kendiliğinden çıkıyor:
    #
    #   0,25–0,75 m/s → Θ = 3,25 · 1:50'de 45–135 km/h   ← SEÇİLEN
    #   0,50–1,50 m/s → Θ = 1,78 · 1:50'de 90–270 km/h   🔴 KAPININ ALTINDA
    #
    # 🔴 Θ DEĞERLERİ 9 EYLÜL 2026'DA YENİDEN TÜRETİLDİ — hızlar DEĞİŞMEDİ,
    # gerekçeleri değişti. Üretici: `python -u kalibrasyon/bag_kumesi.py h`
    # Eski değerler (5,95 ve 3,33) üç ayrı yanlılık taşıyordu:
    #   1. bağ tanımı 400 m'lik SERT DİSKTİ — gölgelemeyi hiç görmüyor ve
    #      rota ömrünü İKİ KAT uzun gösteriyor (ölçüldü: 89 s ↔ 43 s)
    #   2. t = 0'da var olan rotanın yaşı bilinmediği hâlde sayılıyordu
    #      (soldan kesme) — artık her çiftin ilk ömrü atılıyor
    #   3. koşu bitince yaşayan rota "ölmüş" sayılıyordu (sağdan sansür) —
    #      artık Kaplan–Meier ile düzeltiliyor
    # 🔒 Sansür düzeltmesi TAŞIYICIDIR: ham ortalamayla Θ = 2,59 çıkar ve
    # çekirdek kol kapıyı GEÇEMEZDİ. Bugünkü bağ tanımı `kopma_fiziksel`in
    # tanımıyla AYNI (yavaş SINR ≥ eşik) — iki yerde iki tanım yok.
    #
    # 🔴 SEÇİM DEĞİŞMEDİ ama MARJ DARALDI: 5,93 yerine 3,25, yani kapının
    # (Θ ≥ 3) yalnız %8 üstünde. Çalışma noktasını değiştiren her şey —
    # alan, güç, gölgeleme σ'sı — bu marjı yeniden sınamayı gerektirir.
    #
    # 🔴 KEŞİFSEL YÜKSEK ÇALKANTI KOLU ARTIK KAPININ ALTINDA (1,78 < 3).
    # K-101'in kuralı net: kapının altına düşen bir kol protokolü tasarım
    # zarfının DIŞINDA koşturur ve **bulgu olarak raporlanır, gizlenmez**.
    # Bu kol ön-kayıtta ya böyle beyan edilir ya çıkarılır — öğrenci kararı.
    #
    # 🔒 `gm_alfa` ve `gm_azimut_sigma_rad` ARAÇ DİNAMİĞİDİR ve ÖLÇEKLENMEZ:
    #   · hız korelasyon süresi ~30 s → α = exp(−0,5/30) = 0,983.
    #     Eski 0,85, 3,1 s veriyordu; bir İHA için fazla titrek.
    #   · koordineli dönüşte ω = g·tan(φ)/v. Yerçekimi ölçeklenmediği için
    #     GERÇEK hızdan hesaplanır: 90 km/h'de 30° banka → 0,226 rad/s →
    #     0,5 s adımda 0,11 rad. Eski 0,3, saniyede 34°'lik dönüş demekti.
    # Ölçüldü: ikisi de Θ'yı DEĞİŞTİRMİYOR (5,95→5,93 · 3,33→3,27).
    gm_alfa: float = 0.983
    gm_adim_s: float = 0.5
    gm_hiz_min_ms: float = 0.25
    gm_hiz_maks_ms: float = 0.75
    gm_hiz_sigma_ms: float = 0.075
    gm_azimut_sigma_rad: float = 0.11
    # 🔴 ORTALAMA PİTCH 0 — 4 Eylül 2026.
    # Sıfırdan farklı bir ORTALAMA, KALICI bir tırmanış demektir. Tavan
    # etkisinden arınmış geniş bandda ölçüldü — 350 s'de irtifa sürüklenmesi
    # 0,00 rad'da +8 m, 0,05 rad'da +299 m. Sürüklenme, dipol anten kararının
    # dayandığı "düz uçuş" varsayımıyla çelişir. Ortalama 0 · σ = 0,05 ile
    # tipik |pitch| ≈ 2,3°: varsayım gerçekten sağlanıyor.
    # ⚠️ Bir ÇÖKÜŞ düzeltmesi değil: sınır aynalaması geldikten sonra +0,05
    # tek başına irtifayı çökertmiyor (bkz. `dunya/mobilite.py`).
    gm_pitch_ort_rad: float = 0.0
    gm_pitch_sigma_rad: float = 0.05

    # ------------------------------------------- gorev tabanli kol (RPGM)
    # 🔒 Parametreler, `senaryolar.py`de TARAMADAN ONCE ilan edilen olcutle
    # secilir: ortalama dereceyi bagimsiz kolla esitleyen adaylar arasindan
    # tam bagli zaman orani en yakin olani. Bagil hiz ve rota omru OLCUT
    # DEGIL, SONUCTUR — onlara gore ayarlamak cevabi secmek olurdu.
    # Uretici: `python kalibrasyon/gorev_kalibrasyonu.py`
    # 🔴 YARICAP 250 → 650 m, 5 Eylul 2026 (K-097). YENIDEN OLCULDU.
    # Uretici: `python kalibrasyon/calisma_noktasi.py`
    #
    # Eski deger 1000 m'lik alanda ve 280 m'lik TESHIS grafiginde kalibre
    # edilmisti. Alan 1800 m'ye cikinca bagimsiz kol seyreldi, mufrezeler ise
    # 250 m'de kumelenmis kaldi — derece esitligi bozuldu (2,60 ↔ 3,65).
    #
    # 🔒 YENI KALIBRASYON KULLANILABILIR BAG GRAFIGINDE. Kumelenmis bir
    # yerlesimde iki yaricap AYNI ORANDA olceklenmez: mufreze ici baglar
    # kucuk yaricapta zaten doygundur. 280 m'de esitlemek 530 m'de
    # esitledigini garanti etmez.
    #     yaricap 250 m → derece 8,133 (bagimsiz 7,406'nin 1,098 kati)
    #     yaricap 450 m → derece 7,704 (1,040 kat)
    #     yaricap 650 m → derece 7,281 (0,983 kat)  ← SECILEN
    #     yaricap 750 m → derece 6,998 (0,945 kat)
    #
    # ⚠️ 650 m, telsizin ~530 m'lik kullanilabilir yaricapindan GENIS: bir
    # mufreze artik kendi icinde tam bagli bir klik DEGIL. Bu kolu
    # anlamsizlastirmiyor, cunku koordinasyon klik olmaktan degil ORTAK
    # HIZDAN geliyor (bkz. `dunya/mobilite.py` GorevTabanli3B): uyeler gorev
    # merkeziyle birlikte hareket eder, bagil hizlari dusuktur.
    # 🔴 Yine de bu bir kapsam sorusudur ve ogrenciye acik durumdadir (6.5):
    # cok atlamali yonlendirmeye yer birakacak kadar buyuk bir alanda,
    # 40 dugumle yogunluk-esitlenmis mufrezeler KLIK OLAMAZ.
    gorev_grup_sayisi: int = 10
    gorev_grup_yaricapi_m: float = 650.0
    gorev_jitter_hiz_ms: float = 0.05

    # ----------------------------------------------- formasyon kolu (Y6)
    # 🔒 Öğrenci onayı 11 Eylül 2026 (`v2/07` §18 Y6). İstasyonlar yerleşim
    # çekimlerinin AYNISIDIR; tutma zaman sabiti `mobilite.ISTASYON_TUTMA_S`,
    # manevra gürültüsü `gm_alfa` ve `gm_hiz_sigma_ms`ten gelir. Çekirdekte
    # yeni serbest sayı yok. Bu alan keşifsel eksendir: istasyonların yavaş
    # yeniden düzenlenmesi — her istasyon düğüm başına çekilen yatay bir yönde
    # bu hızla kayar ve kutu kenarında geri döner. Çekirdekte 0.
    istasyon_kayma_hiz_ms: float = 0.0

    # 🔴 SINIR KURALININ AYARLANACAK PARAMETRESİ YOK — ve bu kasıtlı.
    # Yansıma tek başına yetmiyordu: anlık azimutu çeviriyor ama Gauss-Markov
    # düğümü duvarı gösteren sabit ORTALAMA yönüne geri çekiyordu. Ölçüldü —
    # kenardan ortanca uzaklık 170 m → 5 m, derece 7,2 → 11,2, tam bağlı
    # zaman oranı %11,1. Çözüm yansımada ORTALAMA YÖNÜ DE AYNALAMAK.
    # "Sınır marjı" alternatifi ölçümle elendi (bkz. `dunya/mobilite.py`):
    # bir marj parametresi olsaydı, onu seçerek ortalama dereceyi 6,8 ile
    # 11,9 arasında istenen yere koymak mümkün olurdu. O parametre yok.

    # ==================================================================
    # FİZİKSEL KATMAN
    # ==================================================================
    # 🔒 Literatür hizalaması: 512 B · 2 Mb/s · 802.11 DCF.
    bit_hizi_bps: float = 2e6
    # PLCP uzun önbelgesi + başlığı: 192 µs. 🔴 Önbelge 1 Mb/s'te gönderilir,
    # gövde 2 Mb/s'te. Bu yüzden önbelge GÖVDE HATASINA KATILMAZ — alıcı
    # zincirinin kilit aşamasına aittir. Süreyi bit hızıyla çarpmak 192 µs'lik
    # dayanıklı önbelgeyi 384 kırılgan gövde biti gibi saymak olurdu.
    onbelge_s: float = 192e-6
    # 🔒 Önbelge TEMEL HIZDA gönderilir (802.11b: 1 Mb/s DBPSK), gövde ise
    # `bit_hizi_bps`te. Önbelgenin bit sayısı bu ikisinden TÜRETİLİR
    # (`kanal/cerceve.py`), elle yazılmaz: 192 µs × 1 Mb/s = 192 bit.
    # Bu yüzden önbelge gövdeden DAHA DAYANIKLIDIR ve `alim_red_onbelge` ile
    # `alim_red_per` gerçekten farklı iki başarısızlık kipidir.
    temel_bit_hizi_bps: float = 1e6
    bant_genisligi_hz: float = 2e6
    frekans_hz: float = 2.4e9
    # 🔴 α = 2,0 — 3,0'DAN DÜŞÜRÜLDÜ, 5 Eylül 2026. HESAPLANARAK.
    # Eski değer 3,0 idi ve gerekçesi *"kentsel/engelli ortam"* yazıyordu.
    # Bu bir YER ağı değeridir; bu proje hava-hava bağları modelliyor.
    #
    # 🔒 İKİ BAĞIMSIZ HESAP AYNI YERE DÜŞÜYOR:
    #
    # 1) İKİ-IŞIN KIRILMA MESAFESİ  d_b = 4·h₁·h₂/λ
    #    simülasyonda (h = 70 m)  → d_b ≈ 157 km
    #    tam ölçekte  (h = 3 km)  → d_b ≈ 288 000 km
    #    Bağ mesafeleri ikisinde de bunun ÇOK altında. Kırılma mesafesinin
    #    altında yer yansıması yol kaybını α = 4'e çıkarmaz; rejim serbest
    #    uzaydır ve serbest uzayda α = 2. Yansımanın getirdiği dalgalanma
    #    zaten Rician sönümlemeyle modelleniyor.
    #
    # 2) ÖLÇEK TUTARLILIĞI. Bu simülatör bir 1:50 geometrik ölçek modelidir
    #    (bkz. `olcek` alanı). Aynı SINR'ı korumak için
    #        Pt_gerçek = Pt_sim + 10·α·log₁₀(50)
    #    α = 2 → 34 dBm = **2,5 W**   (makul bir taktik İHA veri bağı)
    #    α = 3 → 75,5 dBm = **35 kW** (fiziksel olarak imkânsız)
    #    Yani α = 3, kavanozun dışına çıkarıldığında VAR OLAMAYAN bir telsiz
    #    tarif ediyordu. Bağ bütçesi de kapanıyor: 2,5 W · 2,4 GHz · serbest
    #    uzay · 26,7 km → alınan −94,6 dBm, gürültü tabanı −105 dBm,
    #    SINR 10,4 dB — tam olarak çözülebilirlik eşiği.
    #
    # ⚠️ NE DEĞİŞİR:
    #    verici gücü        24,50 → 0,03 dBm  (menzilden TÜRETİLİR)
    #    girişim oranı       3,415 → 6,310    (β^(1/α))
    #    girişim menzili       956 → 1 767 m
    #    etkin/çapa yarıçapı  1,54 → 1,91
    #
    # 🔴 BEDELİ: girişim menzili alanı aşıyor, yani MEKÂNSAL YENİDEN KULLANIM
    # YOK. Bu bir kusur değil, gerçeğin kendisi: tam ölçekte girişim menzili
    # ~88 km ve operasyon kutusundan büyük — tek kanallı bir sürüde bütün ağ
    # tek bir çarpışma alanıdır. Beyan edilir, düzeltilmez.
    #
    # 🔴 BUNU NE GEÇERSİZ KILAR: Adım 4'ün kanal kalibrasyonu ve Adım 3'ün
    # yoğunluk kalibrasyonu yeniden koşulmalıdır (K-096).
    yol_kaybi_usteli: float = 2.0     # α — hava-hava, serbest uzay rejimi

    # 🔴 β = 16 dB — 10 dB'DEN YÜKSELTİLDİ, 5 Eylül 2026. ÖLÇÜLEREK.
    # Üretici: `python kalibrasyon/bag_kalitesi.py`
    #          `python kalibrasyon/pdr_tavani.py`
    #
    # Eski değer 10 dB, "çözülebilirlik eşiği" idi ve menzil TAM ORADA
    # tanımlıydı. Ölçüldü: menzil sınırında (280 m) 512 baytlık bir gövdenin
    # hata olasılığı **%75,5**. Yani topolojinin "bağ" dediği şey, fizik
    # açısından çoğunlukla GEÇMEYEN bir bağdı. Sonucu uçtan uca ölçüldü —
    # kâhin (mükemmel) yönlendirme, karıştırıcı YOK, hafif yük:
    #
    #     β = 10 dB → PDR 0,499 · PSR 0,298   ← gerçeğe aykırı
    #     β = 12 dB → PDR 0,603 · PSR 0,380
    #     β = 14 dB → PDR 0,976 · PSR 0,712
    #     β = 16 dB → PDR 1,000 · PSR 0,817   ← seçilen
    #     β = 20 dB → PDR 1,000 · PSR 0,822   (kazanç yok, maliyet var)
    #
    # 🔒 SEÇİM KEYFÎ DEĞİL, TÜRETİLMİŞ: 10 dB çözülebilirlik + **2σ**
    # gölgeleme marjı (σ = 3 dB) = 16 dB. Ölçüm ve türetme aynı yere düşüyor.
    # Telsiz mühendisliğinde bu standart uygulamadır: menzil, alıcının
    # duyarlılığında değil, duyarlılık + sönümleme marjında tanımlanır.
    #
    # 🔴 BU BLOKTA BİR İDDİA ÇÜRÜTÜLDÜ — 5 Eylül 2026, K-096.
    # Burada eskiden şu yazıyordu: *"`iletim_menzili_m` sabit kaldığı için
    # GEOMETRİ ve dolayısıyla Adım 3'ün yoğunluk kalibrasyonu (derece 7,271 ·
    # bağlı %78,2) aynen geçerli."* **Yanlış.**
    #
    # `iletim_menzili_m` veri yolunda hiçbir yeri kapamıyor: kimin duyacağını
    # girişim menzili, alınıp alınmadığını SINR belirliyor. 280 m yalnızca
    # verici gücünün türetildiği bir ÇAPA ve kalibrasyon betiklerinin
    # topoloji anlık görüntüsüdür. β yükselince çapa ile fiilen kullanılabilen
    # yarıçap AYRIŞTI ve Adım 3 kullanılmayan bir grafiği kalibre etmiş oldu.
    #
    # Ölçüldü (gölgeleme + sönümleme dâhil, β = 16 dB, α = 3, 1000 m alan):
    #     çapada (280 m)  derece 6,5  · ortalama atlama 3,15
    #     GERÇEKTE         derece 12,9 · ortalama atlama 1,81
    # Yani ağ tasarlandığından iki kat yoğun ve yarı derinlikte.
    # Adım 3 kullanılabilir bağ grafiğinde YENİDEN kalibre edilmelidir.
    #
    # ⚠️ Girişime karşı marj DEĞİŞMEZ (herkesin gücü aynı oranda arttı), bu
    # yüzden çarpışma davranışı korunur — o kısım ayakta.
    #
    # ⚠️ NE DEĞİŞİR: `girisim_orani` bundan TÜRETİLDİĞİ için 2,154 → 3,42.
    # Daha güçlü verici daha uzağa girişim yapar; bu fizik, yan etki değil.
    # Bedeli ölçüldü: koşu süresi ~%40 artıyor.
    #
    # 🔴 KARIŞTIRICI GÜCÜ BUNDAN SONRA KALİBRE EDİLMELİ. Karıştırıcının dBm
    # cinsinden mutlak gücü, artık 6 dB daha güçlü bir sinyale karşı
    # çalışacak. `senaryolar.KARISTIRICI_GUCU_DBM` zaten boş (ölçülmedi).
    sinr_esigi_db: float = 16.0       # β — menzil sınırının tanımlandığı SINR
    gurultu_figuru_db: float = 6.0
    sicaklik_k: float = 290.0

    # 🔒 2 Mb/s'te 802.11b DQPSK kullanır — DBPSK 1 Mb/s'in modülasyonudur.
    # Öğrenci kararı (4 Eylül 2026): kapalı formu yazılacak ve yayınlanmış
    # BER eğrileriyle analitik olarak doğrulanacak.
    modulasyon: str = "dqpsk"

    # Kanal rastgeleliği sıralı akıştan DEĞİL, hash'ten gelir.
    kanal_dilimi_s: float = 1e-4

    # ---------------------------------------------------------- gölgeleme
    # 🔴 NEDEN EKLENDİ — ölçüldü: PER'in 0,01'den 0,99'a düştüğü SINR bandı
    # yalnızca **3,02 dB**. Gölgeleme σ'sı 2–4 dB, yani geçiş bandı TEK bir
    # σ'dan dar. Gölgelemesiz bir modelde bağlar gerçeğe göre keskin açılıp
    # kapanır. Üretici: `python kalibrasyon/adim3_oncesi.py`
    golgeleme_acik: bool = True
    golgeleme_sigma_db: float = 3.0
    # Bağ-simetrik ve KONUMA BAĞLI: hücrelenmiş hash + trilineer yumuşatma.
    # Hareket eden düğüm gölgeleme alanında sürekli ilerler, ışınlanmaz.
    golgeleme_hucre_m: float = 50.0

    # ---------------------------------------------------------- sönümleme
    # Hava-hava bağda güçlü doğrudan görüş → Rayleigh değil **Rician**.
    sonumleme_acik: bool = True
    rician_k_db: float = 6.0
    # 🔒 PARÇA BAŞINA çekilir, paket başına DEĞİL — ve süresi ÖLÇÜLEREK
    # seçildi. Devir belgesi 30 m/s'lik bir VARSAYIMLA çalışıyordu; gerçek
    # bağıl hız dağılımı ölçülüyor ve Doppler K-102'den beri TAM ÖLÇEK
    # hızından hesaplanıyor (dalga boyu ölçeklenemez).
    #
    # 🔒 TÜRETME: parça süresi = T_c(p99)/4. Ölçüldü — 10 tohum × 350 s,
    # bağımsız kol. Üretici: `python kalibrasyon/adim4_sonumleme.py` §A/B
    #     ortanca 0,6 m/s → T_c 1,65 ms → çerçeve/T_c 1,36
    #     p95     1,2 m/s → T_c 0,90 ms → çerçeve/T_c 2,49
    #     p99     1,4 m/s → T_c 0,77 ms → parça = 193 µs  →  **190 µs**
    # Kanal bir çerçeve süresince ortancada ~1,4 kez değişiyor: paket başına
    # tek çekim yanlış olurdu. Çerçeve başına 12 parça. Eski varsayılan
    # 80 µs bir ölçüme değil bir varsayıma dayanıyordu (28 parça, 3 kat).
    #
    # 🔴 BURADAKİ ESKİ TABLO BAYATTI ve 9 Eylül 2026'da değiştirildi. Şunu
    # yazıyordu: *"ortanca 25,1 m/s → T_c 2,10 ms … parça = 243 µs → 240 µs,
    # çerçeve başına ~9,3 parça."* Üç sayı da K-101 ÖNCESİ hız rejiminden
    # (26 m/s) geliyordu ve türettiği değer (240) koddaki değerle (190)
    # çelişiyordu. ⚠️ Üreticinin kendisi de bozuktu: T_c'yi ölçekli hızdan
    # hesaplıyordu (K-102'yi kaçırmış) ve 9 666 µs veriyordu. Onarıldı;
    # bugün üretici 193 µs diyor, yani DEĞER AYAKTA — bayat olan gerekçeydi.
    sonumleme_parca_suresi_s: float = 190e-6

    # ------------------------------------------------------- anten deseni
    # 🔴 İlk yargı "izotropik bırak" idi, ÖLÇÜMLE ÇEVRİLDİ. 1000×1000×300 m'de
    # dipol kaybının p95'i 9,70 dB — gölgeleme σ'sının çok üstünde. Seçilen
    # 120 m bandında 3,27 dB; yine de ihmal edilemez ve tam da YAKIN
    # komşularda modeli iyimser yapardı.
    anten_deseni_acik: bool = True

    # ==================================================================
    # ALICI ZİNCİRİ (Adım 6a)
    # ==================================================================
    yakalama_etkisi_acik: bool = True
    yakalama_esigi_db: float = 10.0
    # 🔒 YAKALAMA PENCERESİ = önbelge süresi (192 µs). Gerçek bir alıcı hâlâ
    # senkronizasyon aşamasındayken daha güçlü bir çerçeveye geçebilir; gövde
    # çözümüne başladıktan sonra kilidi kolay bırakmaz. Pencere koşulu
    # olmasaydı alıcı neredeyse bitmiş bir gövdeyi bırakıp yeni bir önbelgeye
    # geçer ve gerçekte imkânsız bir davranış üretirdi.
    # ⚠️ Sayı BEYAN EDİLİR, `onbelge_s`ten türetilmez: türetilseydi önbelge
    # aritmetiği `cerceve.py` dışına çıkardı (kusur 1'in kuralı).
    yakalama_penceresi_s: float = 192e-6

    # ==================================================================
    # MAC — CSMA/CA, 802.11b değerleri
    # ==================================================================
    slot_s: float = 20e-6
    sifs_s: float = 10e-6
    # CCA gecikmesi SIFIR OLAMAZ: sıfır olsaydı geri sayımı aynı slotta biten
    # iki düğüm asla çarpışmazdı ve 802.11'in temel çakışma kaynağı silinirdi.
    cca_s: float = 4e-6
    cw_min: int = 31
    cw_max: int = 1023
    yeniden_deneme_siniri: int = 4
    onay_bayt: int = 14

    # ==================================================================
    # SAAT (Adım 7)
    # ==================================================================
    # 🔒 Yasak değil, FİZİK: protokol beacon'a zaman damgası koyabilir ama
    # alıcı ofseti görür. Bedava kusursuz senkron imkânsız hâle gelir.
    saat_senkron: bool = False        # ablasyon: True → tek küresel saat
    saat_ofset_araligi_s: float = 0.5  # ofset ~ U(−bu, +bu)
    saat_sapma_ppm: float = 20.0       # sapma ~ N(0, bu)

    # ==================================================================
    # TRAFİK
    # ==================================================================
    # 🔒 10 akış × 4 pkt/s — öğrenci kararı, 4 Eylül 2026. Ölçüldü:
    #   10 akış → tek çarpışma alanının %36,9'u   (SEÇİLEN)
    #   15 akış → %54,0
    #   eski kurulum (10 çift × 1 pkt/s × 1024 B @ 1 Mb/s) → %27,1
    # Gerekçe: karıştırıcı devreye girdiğinde ağın çökmeden bozulmasına yer
    # bırakır. %54'te tüm protokoller birlikte çöker ve fark bastırılır.
    paket_bayt: int = 512
    akis_sayisi: int = 10
    akis_paket_hizi_hz: float = 4.0
    cbr_titresim_s: float = 0.05      # periyodik süreçlerin kilitlenmesini kırar

    # 🔒 TRAFİK DESENİ — `v2/07` §06.2 · §18 Y4 (öğrenci onayı 10–11 Eylül 2026).
    # `esler_arasi` bugünkü rastgele çiftlerdir ve varsayılandır. `yere_toplama`:
    # geçit dışındaki her düğümden geçide telemetri, geçitten birkaç düğüme
    # düşük hızlı komut. Geçit düğüm 0'dır: konum tutan röle İHA.
    # ⚠️ Hızların kaynağı yok (`v2/02` §S4); C3 ölçütle seçecek. Varsayılanlar
    # 40 düğümde sunulan yükü bugünkü 40 pkt/s'de tutar: 39 × 1,0 + 4 × 0,25.
    # ⚠️ İki geçit (keşifsel eksen) henüz uygulanmadı.
    trafik_deseni: str = "esler_arasi"
    gecit_konumu: str = "kenar"        # kenar · merkez
    telemetri_paket_hizi_hz: float = 1.0
    komut_akis_sayisi: int = 4
    komut_paket_hizi_hz: float = 0.25

    # ==================================================================
    # KUYRUK ve TTL
    # ==================================================================
    # Sonsuz kuyruk yasak: gecikme metriğini anlamsızlaştırır.
    kuyruk_kapasitesi: int = 50
    # ==================================================================
    # ROTA BEKLEME TAMPONU — `Karar.beklet` (16 Eylül 2026, K-131)
    # ==================================================================
    # 🔒 İKİ TAVAN, İKİSİ DE İLAN EDİLMİŞ. Protokol rota ararken paketi
    # bekletebilir ama sonsuza kadar bekletemez: tampon hem PAKET SAYISIYLA
    # hem SÜREYLE sınırlıdır ve aşım `tampon_asimi` sebebiyle deftere yazılır.
    # Tavansız bir tampon, sonsuz kuyruğun ta kendisi olurdu — gecikme
    # metriğini anlamsızlaştırır ve PDR'yi yapay olarak yükseltirdi
    # (`ag/kuyruk.py`nin aynı gerekçesi).
    #
    # ⚠️ İkisi de `SINANMAMIS`: değerler NS-2'nin AODV gerçeklemesinin
    # geleneğinden alındı (64 paket · 30 s) ve BU PROJEDE ÖLÇÜLMEDİ. Protokol
    # olmadan kapanamayan parametrelerin (kuyruk kapasitesi, TTL, beacon
    # aralığı, komşu ömrü) yanına beşinci ve altıncı olarak yazılıyorlar;
    # Aşama 2'de gerçek taban protokolle kapanacaklar.
    rota_tamponu_kapasitesi: int = 64
    rota_tamponu_omru_s: float = 30.0
    # TTL olmadan döngüye giren paket "uçuşta" olarak sonsuza dek asılı kalır.
    ttl_baslangic: int = 32

    # ==================================================================
    # KONTROL DÜZLEMİ
    # ==================================================================
    beacon_araligi_s: float = 1.0
    beacon_bayt: int = 32
    # ⚠️ Bir PROTOKOL parametresi DEĞİL, bellek sınırlamasıdır. Tazelik kararı
    # protokole aittir. Geniş tutuluyor ki protokolün kararını kısıtlamasın.
    komsu_omru_katsayisi: float = 10.0

    # ==================================================================
    # KARIŞTIRICI — sınıf SENARYODAN gelir, parametreler burada
    # ==================================================================
    # Sınıf elle ayarlanabilseydi aynı etiketli iki koşu farklı karıştırıcı
    # taşıyabilir ve sonuç satırındaki etiket yalan söylerdi.
    karistirici_guc_override_dbm: float | None = None  # yalnız güç taraması
    karistirici_konum: tuple[float, float] | None = None  # None → alan merkezi

    # 🔴 AÇILMA ANI — projenin asıl iddiasını ÖLÇÜLEBİLİR yapan parametre.
    # Karıştırıcı eskiden koşunun başından sonuna açıktı; ölçüm penceresi
    # tamamen karıştırılmış dönemin içindeydi ve GEÇİCİ TEPKİ diye bir şey
    # yoktu. Oysa beyan edilmiş beklenti (*"ilk şokta %50 altı, mesh tepki
    # verince %70–80"*) bir geçici tepki tarifidir; bir anti-jamming
    # yönlendirme protokolünün asıl iddiası da *"ne kadar bozuluyor"* değil
    # **"ne kadar hızlı toparlanıyor"**dur.
    #
    # 🔒 DEĞER PENCEREDEN TÜRETİLDİ, elle seçilmedi:
    #   ölçüm penceresi [50, 320] = 270 s
    #   temiz evre        [50, 150) = 100 s → 4 000 paket, PDR SE ≈ 0,005
    #   karıştırılmış     [150, 320) = 170 s → 6 800 paket
    # Toparlanma rota ömrü (89 s) ve protokol zamanlayıcıları (AODV 3 s,
    # OLSR 15 s) mertebesinde beklendiği için 170 s bolca yeter.
    #
    # ⚠️ Karıştırıcısız kollarda anlamsızdır ve okunmaz.
    karistirici_baslangic_s: float = 150.0
    darbe_periyodu_s: float = 2.7     # ⚠️ trafik aralığının tam katı DEĞİL
    darbe_gorev_cevrimi: float = 0.5  # 🔒 tepe telafisi bundan TÜRETİLİR
    reaktif_sezme_s: float = 16e-6
    reaktif_patlama_s: float = 144e-6
    taramali_konak_suresi_s: float = 0.1
    taramali_konak_sayisi: int = 3

    # 🔒 TEHDİT SENARYOSU — Y5b, öğrenci kararları 11 Eylül 2026 (`v2/04`
    # K-119). Sinyal sınıfı senaryo adından, karıştırıcı kümesinin biçimi bu
    # eksenden gelir (`kanal/tehdit.py`). `tekli_merkez` bugünkü tek merkez
    # karıştırıcıyı birebir kurar.
    # Süreler protokol zaman sabitleri cinsinden ilan edilir; tek bir "gerçek
    # değer" iddiası yok. Çekirdek 15 s = OLSR TOP_HOLD_TIME. Keşifsel: açık
    # 3 s · 45 s, sessiz 5 s · 45 s, görev çevrimi periyodu 6 s. Hızlar
    # kaynaksız varsayımdır; ölçekli hız = km/h ÷ 3,6 ÷ `olcek`.
    tehdit_senaryosu: str = "tekli_merkez"
    tehdit_acik_s: float = 15.0             # yay–sus–taşın: yayın dönemi
    tehdit_sessiz_s: float = 15.0           # yay–sus–taşın: sessiz, taşınma
    tehdit_arac_hiz_kmh: float = 60.0
    tehdit_hava_hiz_kmh: float = 200.0

    # ==================================================================
    not_: str = ""

    UYGULANMAMIS_ALANLAR: ClassVar[frozenset[str]] = frozenset()

    # ------------------------------------------------------------------
    def __post_init__(self) -> None:
        dogrula(bool(self.kol.strip()), "kol adı boş olamaz")
        if self.senaryo not in SENARYOLAR:
            raise ValueError(
                f"bilinmeyen senaryo: {self.senaryo!r} — "
                f"seçenekler: {sorted(SENARYOLAR)}")

        dogrula(0.0 <= self.isinma_s < self.olcum_bitis_s <= self.kosu_bitis_s,
                "zaman sınırları tutarsız: 0 ≤ ısınma < ölçüm_bitiş ≤ koşu_bitiş")
        dogrula(self.dugum_sayisi >= 2, "en az iki düğüm gerekli")
        dogrula(self.alan_en_m > 0 and self.alan_boy_m > 0,
                "alan boyutları pozitif olmalı")
        dogrula(0.0 <= self.irtifa_min_m < self.irtifa_maks_m,
                "irtifa bandı artan ve negatif olmayan olmalı")
        dogrula(self.iletim_menzili_m > 0, "iletim menzili pozitif olmalı")
        dogrula(0.0 <= self.gm_alfa < 1.0, "gm_alfa [0, 1) aralığında olmalı")
        dogrula(self.gm_adim_s > 0.0, "mobilite adımı pozitif olmalı")
        dogrula(0.0 < self.gm_hiz_min_ms <= self.gm_hiz_maks_ms,
                "hız bandı tutarsız")

        # β > 1 ve α > 0 → girişim menzili iletim menzilinden GENİŞ olur, yani
        # gizli terminal mümkün kalır. Ayrı bir "oran > 1" kontrolü YAZILMADI:
        # bundan matematiksel olarak çıkar ve asla tetiklenemezdi. Tetiklenemeyen
        # bir kontrol, koruma sağlamadan koruma izlenimi verir.
        dogrula(self.sinr_esigi_db > 0 and self.yol_kaybi_usteli > 0,
                "SINR eşiği ve yol kaybı üsteli pozitif olmalı")
        dogrula(self.bit_hizi_bps > 0 and self.bant_genisligi_hz > 0,
                "bit hızı ve bant genişliği pozitif olmalı")
        dogrula(self.golgeleme_sigma_db >= 0.0, "gölgeleme σ negatif olamaz")
        dogrula(self.golgeleme_hucre_m > 0.0, "gölgeleme hücresi pozitif olmalı")
        dogrula(self.sonumleme_parca_suresi_s > 0.0, "parça süresi pozitif olmalı")
        dogrula(self.kanal_dilimi_s > 0.0, "kanal dilimi pozitif olmalı")
        dogrula(self.cca_s > 0.0,
                "CCA gecikmesi sıfır olamaz — aynı-slot çarpışması silinir")
        dogrula(1 <= self.cw_min <= self.cw_max, "çekişme penceresi tutarsız")
        dogrula(self.yeniden_deneme_siniri >= 0, "yeniden deneme sınırı negatif")
        dogrula(self.kuyruk_kapasitesi > 0, "kuyruk kapasitesi sonlu ve pozitif")
        dogrula(self.rota_tamponu_kapasitesi > 0,
                "rota bekleme tamponu kapasitesi sonlu ve pozitif olmalı — "
                "tavansız tampon sonsuz kuyruktur")
        dogrula(self.rota_tamponu_omru_s > 0.0,
                "rota bekleme tamponu ömrü pozitif olmalı")
        dogrula(self.ttl_baslangic > 0, "TTL pozitif olmalı")
        dogrula(self.akis_sayisi >= 1 and self.akis_paket_hizi_hz > 0,
                "trafik parametreleri pozitif olmalı")
        if self.trafik_deseni not in TRAFIK_DESENLERI:
            raise ValueError(
                f"bilinmeyen trafik deseni: {self.trafik_deseni!r} — "
                f"seçenekler: {TRAFIK_DESENLERI}")
        if self.trafik_deseni == "esler_arasi":
            dogrula(2 * self.akis_sayisi <= self.dugum_sayisi,
                    "akış sayısı düğüm sayısının yarısını aşamaz — "
                    "aynı düğüm birden çok akışın kaynağı olurdu")
        else:
            dogrula(self.gecit_konumu in ("kenar", "merkez"),
                    "geçit konumu `kenar` ya da `merkez` olmalı")
            dogrula(self.telemetri_paket_hizi_hz > 0
                    and self.komut_paket_hizi_hz > 0,
                    "telemetri ve komut hızı pozitif olmalı")
            dogrula(0 <= self.komut_akis_sayisi <= self.dugum_sayisi - 1,
                    "komut akışı sayısı geçit dışındaki düğüm sayısını aşamaz")
        dogrula(1 <= self.gorev_grup_sayisi <= self.dugum_sayisi,
                "mufreze sayisi 1 ile dugum sayisi arasinda olmali")
        dogrula(self.gorev_grup_yaricapi_m > 0.0
                and 2.0 * self.gorev_grup_yaricapi_m
                < min(self.alan_en_m, self.alan_boy_m),
                "grup capi alandan buyuk olamaz")
        dogrula(self.gorev_jitter_hiz_ms >= 0.0,
                "titresim hizi negatif olamaz")
        dogrula(self.istasyon_kayma_hiz_ms >= 0.0,
                "istasyon kayma hızı negatif olamaz")
        dogrula(0.0 < self.darbe_gorev_cevrimi <= 1.0,
                "darbe görev çevrimi (0, 1] aralığında olmalı")
        if self.tehdit_senaryosu not in TEHDIT_SENARYOLARI:
            raise ValueError(
                f"bilinmeyen tehdit senaryosu: {self.tehdit_senaryosu!r} — "
                f"seçenekler: {TEHDIT_SENARYOLARI}")
        dogrula(self.tehdit_acik_s > 0.0 and self.tehdit_sessiz_s > 0.0,
                "tehdit süreleri pozitif olmalı")
        dogrula(self.tehdit_arac_hiz_kmh > 0.0
                and self.tehdit_hava_hiz_kmh > 0.0,
                "tehdit platform hızları pozitif olmalı")
        dogrula(self.saat_ofset_araligi_s >= 0.0 and self.saat_sapma_ppm >= 0.0,
                "saat parametreleri negatif olamaz")

        # 🔴 Güç override yalnız güç taraması içindir ve NİHAİ güçtür: darbeli
        # bir senaryoyla birleşirse "aynı ortalama güç" koşulu sessizce kırılır.
        if (self.karistirici_guc_override_dbm is not None
                and SENARYOLAR[self.senaryo].darbeli):
            raise ValueError(
                "karistirici_guc_override_dbm darbeli senaryoyla "
                "birleştirilemez: override nihai güçtür, tepe telafisi "
                "uygulanmaz ve 'aynı ortalama güç' koşulu kırılır.")

        # ⚠️ Burada eskiden "uygulanmamış karıştırıcı sınıfı" kapısı vardı.
        # Beş sınıfın beşi de uygulanınca o kapı TETİKLENEMEZ hâle geldi ve
        # kaldırıldı: tetiklenemeyen bir kontrol, koruma sağlamadan koruma
        # izlenimi verir. Yerini alan kapı `kanal/karistirici.py`de ve farklı
        # bir şeyi koruyor — ÖLÇÜLMEMİŞ GÜÇLE koşmayı.

    # ==================================================================
    # TÜRETİLENLER — elle yazılmış sayı YOK
    # ==================================================================
    @property
    def mobilite_kolu(self) -> str:
        """🔒 Mobilite bir KONFİGÜRASYON BAYRAĞIDIR, kod düzenlemesi değil.

        Dort kol: `statik` (U1 sanity kolu) · `bagimsiz` (Gauss-Markov,
        literaturun standardi) · `gorev` (koordineli suru) · `formasyon`
        (istasyon tutma, Y6). Ucuncusu bir OLCUMUN sonucu olarak eklendi,
        dorduncusu ogrenci onayiyla — `yapilandirma/senaryolar.py`ye bak.
        """
        return SENARYOLAR[self.senaryo].mobilite_kolu

    @property
    def hareketli(self) -> bool:
        """Turetilmis: `statik` disindaki her kol hareketlidir."""
        return SENARYOLAR[self.senaryo].hareketli

    @property
    def karistirici_sinifi(self) -> str:
        return SENARYOLAR[self.senaryo].karistirici_sinifi

    @property
    def karistirici_darbeli(self) -> bool:
        return SENARYOLAR[self.senaryo].darbeli

    @property
    def karistirici_var_mi(self) -> bool:
        return SENARYOLAR[self.senaryo].karistirici_var_mi

    # ------------------------------------------------------ ölçek eşlemesi
    # 🔒 `olcek` bu özellikler üzerinden OKUNUR — uyuyan bir alan değildir.
    # Gösterim katmanı da ("1 m = N m · bu kutu X km") verisini buradan alır,
    # sonradan uydurmaz.
    @property
    def gercek_alan_km(self) -> float:
        """Kutunun gerçek dünyadaki kenar uzunluğu."""
        return self.alan_en_m * self.olcek / 1000.0

    @property
    def gercek_capa_km(self) -> float:
        """Güç çapasının gerçek karşılığı."""
        return self.iletim_menzili_m * self.olcek / 1000.0

    @property
    def gercek_hiz_araligi_kmh(self) -> tuple[float, float]:
        """Simüle edilen hızların gerçek karşılığı — A5a ile karşılaştırılır."""
        return (self.gm_hiz_min_ms * self.olcek * 3.6,
                self.gm_hiz_maks_ms * self.olcek * 3.6)

    @property
    def gercek_irtifa_km(self) -> tuple[float, float]:
        return (self.irtifa_min_m * self.olcek / 1000.0,
                self.irtifa_maks_m * self.olcek / 1000.0)

    @property
    def olcek_guc_farki_db(self) -> float:
        """`Pt_gerçek = Pt_sim + bu`. Aynı SINR'ı korumanın bedeli.

        🔴 Bu bir KAPIDIR: sonuç fiziksel olarak var olabilecek bir verici
        vermelidir. α = 3 iken 35 kW çıkıyordu ve α'yı bu hesap eledi.
        """
        return 10.0 * self.yol_kaybi_usteli * math.log10(self.olcek)

    @property
    def girisim_orani(self) -> float:
        """Girişim menzilinin iletim menziline oranı — TÜRETİLMİŞ.

        Menzil sınırında girişimsiz SINR tam olarak eşiğe eşittir:
            P(R)/N = β
        Bir girişimcinin gücü gürültü tabanına eşit olduğunda hissedilir olur:
            P(D) = N  →  D = β^(1/α) · R

        Güncel çalışma noktasında (β = 16 dB, α = 2) ≈ 6,310; girişim menzili
        1 767 m olur ve 1 000 m'lik alanı aşar — yani her düğüm her düğümü
        duyar. Bu beyan edilmiş bir sonuçtur, yan etki değil.

        ⚠️ Örnek değerler ÜRETİLMİŞTİR, elle yazılmamıştır: β = 10 dB, α = 3
        için 2,154 · β = 16 dB, α = 3 için 3,415. Elle yazılmış bir sabit,
        β ya da α değiştiğinde sessizce yanlış olurdu.
        """
        return (10.0 ** (self.sinr_esigi_db / 10.0)) ** (1.0 / self.yol_kaybi_usteli)

    @property
    def girisim_menzili_m(self) -> float:
        return self.iletim_menzili_m * self.girisim_orani

    @property
    def difs_s(self) -> float:
        return self.sifs_s + 2 * self.slot_s

    @property
    def komsu_omru_s(self) -> float:
        """Komşu kaydının BELLEKTE tutulduğu süre — TÜRETİLMİŞ.

        Beacon aralığının katı olarak yazılır ki beacon aralığı değişince
        ömür sessizce ayrışmasın. ⚠️ Bir tazelik eşiği DEĞİL: tazelik kararı
        protokolündür, bu yalnız komşu tablosunun sınırsız büyümesini önler.
        """
        return self.komsu_omru_katsayisi * self.beacon_araligi_s

    @property
    def olcum_penceresi(self) -> tuple[float, float]:
        """Metriklerin hesaplandığı aralık.

        ⚠️ Korunum denklemi BU aralıkta değil, TÜM koşu üzerinden kontrol
        edilir — ikisi ayrı defterdir.
        """
        return (self.isinma_s, self.olcum_bitis_s)

    @property
    def tepe_telafisi_db(self) -> float:
        """Darbeli karıştırıcının tepe gücüne eklenen telafi — TÜRETİLMİŞ.

        Ortalama = tepe × görev çevrimi; ortalamayı sabit karşılığına
        eşitlemek için tepeyi 1/d kadar yükseltmek gerekir. Bir modül sabiti
        OLARAK yazılsaydı görev çevrimiyle ikinci bir doğru kaynağı oluşur ve
        ikisi bağımsız değişebilirdi.
        """
        return 10.0 * math.log10(1.0 / self.darbe_gorev_cevrimi)

    @property
    def karistirici_guc_dbm(self) -> float | None:
        """Karıştırıcının TEPE gücü. `None` = ölçülmedi (0,0 DEĞİL)."""
        if self.karistirici_guc_override_dbm is not None:
            return self.karistirici_guc_override_dbm
        taban = KARISTIRICI_GUCU_DBM[self.karistirici_sinifi]
        if taban is None:
            return None
        return taban + self.tepe_telafisi_db if self.karistirici_darbeli else taban

    @property
    def karistirici_merkez(self) -> tuple[float, float]:
        """Varsayılan alanın merkezi — tohumlar arasında KARŞILAŞTIRILABİLİR.

        Rastgele bir karıştırıcı konumu, tohumlar arası varyansa karıştırıcının
        nereye düştüğünü de katardı ve protokol farkını gizlerdi.
        """
        return self.karistirici_konum or (self.alan_en_m / 2.0,
                                          self.alan_boy_m / 2.0)

    @property
    def yere_toplama(self) -> bool:
        return self.trafik_deseni == "yere_toplama"

    @property
    def gecit(self) -> int | None:
        """Geçit düğümü — yere toplamada düğüm 0; eşler arası desende yok."""
        return 0 if self.yere_toplama else None

    @property
    def sunulan_paket_hizi_hz(self) -> float:
        """Ağa sunulan toplam paket hızı — teşhis ve yük kontrolü için."""
        if self.yere_toplama:
            return ((self.dugum_sayisi - 1) * self.telemetri_paket_hizi_hz
                    + self.komut_akis_sayisi * self.komut_paket_hizi_hz)
        return self.akis_sayisi * self.akis_paket_hizi_hz

    # ------------------------------------------------------------------
    def sozluk(self) -> dict[str, Any]:
        """Sonuç satırına yazılacak TAM konfigürasyon."""
        return asdict(self)


# ===========================================================================
# 🔴 KÖKEN KAPSAMASI — GEREKÇESİZ PARAMETRE DEPOYA GİREMEZ
# ===========================================================================
# `Konfig`in her alanı `kokenler.KOKENLER`de bir kovaya yazılmak zorundadır.
# Bu denetim İÇE AKTARMA anında koşar: eksik bir alan varsa modül hiç
# yüklenmez ve hiçbir koşu başlamaz.
#
# 🔒 Neden burada ve neden import anında: bir sonraki geliştirici `Konfig`e
# alan eklediğinde, o alanın nereden geldiğini yazmayı UNUTAMASIN diye.
# Disiplin değil, mekanizma — `cekirdek/sayaclar.py`nin sayaçlar için
# yaptığının parametreler için yapılmış hâli.
_eksik, _fazla = _kokenler.eksik_alanlar(
    tuple(_a.name for _a in _dc.fields(Konfig)))
if _eksik:
    raise _DegismezHatasi(
        f"kökeni yazılmamış Konfig alanı: {_eksik}. Her parametre "
        f"sim2/yapilandirma/kokenler.py'de bir kovaya yazılmak zorundadır "
        f"(TURETILMIS · OLCULMUS · KAYNAK · DUYARSIZ · TEDAVI · KOL_TANIMI · SINANMAMIS).")
if _fazla:
    raise _DegismezHatasi(
        f"artık var olmayan alan için köken kaydı: {_fazla}. Kayıt "
        f"defterinde ölü giriş bırakmak, kaydın güvenilirliğini bitirir.")
