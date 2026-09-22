# 04 — NEDEN BÖYLE · Kayıt Defteri

> ## 📦 K-001…K-089 ARŞİVDE — 23 Eylül 2026 (öğrenci kararı)
> Emekli `sim/` simülatörünün kayıtları ve eski statik içindekiler
> `v2/arsiv/04-NEDEN-BOYLE-K001-K089.md`dedir — SİLİNMEDİ, bağlam
> kirliliğini önlemek için ayrıldı. Bu dosya `sim2/` dönemini (**K-090** ve
> sonrası) taşır; K-0xx'e yapılan her atıf o arşiv dosyasındadır.


> Bu defter **sahiplik** için değil **hafıza** için tutulur.
> Kasım ayında *"bu parametreyi neden böyle seçmiştik?"* sorusunun cevabı burada olacak.
>
> **Kural:** bir karar burada yazılı değilse, o karar verilmemiştir.
> Yeni kayıt **en alta** eklenir. Eski kayıt silinmez; değişirse **revizyon** olarak yazılır.

---

## Sütunlar

Her kaydın dört parçası var:

| Parça | Ne |
|---|---|
| **NE** | Karar tek cümleyle |
| **NEDEN** | Gerekçe |
| **NE ELENDİ** | Değerlendirilip seçilmeyen alternatifler |
| **BUNU NE DEĞİŞTİRİR** | Kararı geri aldıracak ölçüm |

---

---

# 📇 KAYIT İNDEKSİ — *(üretildi)*

> 🔴 **BU İNDEKS ELLE TUTULMAZ, ÜRETİLİR.** Bayatlarsa yeniden koşulur:
> ```bash
> PYTHONIOENCODING=utf-8 python arsiv/dogrulama/kayit_indeksi.py
> ```
> Değiştirmeden kontrol: `--kontrol` *(bayatsa 1 döner)*

🔴 **REVİZE EDİLMİŞ kayıtlar SİLİNMEDİ** — bir kararın sonradan
değiştiğini göstermek, hiç verilmemiş gibi görünmesinden **güçlüdür**.
Hangisinin geçerli olduğu **burada** yazılı.

| kayıt | konu | durum |
|---|---|---|
| K-090 | 🔴 SİMÜLATÖR SIFIRDAN YENİDEN YAZILDI — sim/ EMEKLİ, sim2/ DOĞDU | 🟢 geçerli |
| K-091 | 🔴 SINR EŞİĞİ 10 → 16 dB — MENZİL, GEÇMEYEN BİR BAĞIN ÜSTÜNDE TANIMLIYDI | 🟢 geçerli |
| K-092 | 🔴 KARIŞTIRICI, TAŞIYICI DİNLEMEYE MESAFEDEN BAĞIMSIZ GÖRÜNÜYORDU | 🟢 geçerli |
| K-093 | 🔒 DEPO SADELEŞTİRİLDİ — EMEKLİ HER ŞEY arsiv/ ALTINA | 🟢 geçerli |
| K-094 | 🔴 BULGU — BEACON MENZİLİ VERİ MENZİLİNDEN GENİŞ, "KOMŞU" TANIMI YETERSİZ | 🟢 geçerli |
| K-095 | 🔴 SÖNÜMLEME ÖNBELLEĞİ SINIRSIZDI — HAREKETLİ KOLLAR KOŞULAMIYORDU | 🟢 geçerli |
| K-096 | 🔴 ÇALIŞMA NOKTASI ÖLÇÜLDÜ — ÜÇ AYRI YARIÇAP, VE MACH 4'TE UÇAN İHA'LAR | 🟢 geçerli |
| K-097 | 🔴 ÇALIŞMA NOKTASI DEĞİŞTİ — α = 2,0 ve ALAN 1800 m · VE İLAN ETTİĞİM ÖLÇÜT INFEASIBLE ÇI | 🟢 geçerli |
| K-098 | 🔴 KÂHİN KANALDAN KURULUYOR — VE ÖLÇÜM ALETİM KENDİ HAYALET BAĞLARINI ÜRETİYORMUŞ | 🟢 geçerli |
| K-099 | 🔴 KODUN TAMAMI OKUNDU — ETİKET VE TANIM KUSURLARI | 🟢 geçerli |
| K-100 | 🔴 PARAMETRE KÖKEN KAYIT DEFTERİ — BORÇ ARTIK GÖRÜNÜR VE SAYILABİLİR | 🟢 geçerli |
| K-101 | 🔴 MOBİLİTE ARTIK m/s İLE DEĞİL, PROTOKOLÜN ZAMANIYLA TANIMLI — VE OLSR YAPISAL OLARAK KI | 🟢 geçerli |
| K-102 | 🔴 DOPPLER PLATFORM HIZINDAN AYRILDI — VE KENDİ HIZ DEĞİŞİKLİĞİM SESSİZ BİR KUSUR YARATMI | 🟢 geçerli |
| K-103 | 🔴 KARIŞTIRICI GÜCÜ ÖLÇÜLDÜ — VE "SINIFLARI AYNI ETKİDE EŞİTLE" DEDİĞİM ŞEY DÖNGÜSELMİŞ | 🟢 geçerli |
| K-104 | 🔴 SON OTURUMUN DENETİMİ — DÖRT ŞÜPHE DÜŞTÜ, ÜÇ GERÇEK KUSUR ÇIKTI | 🟢 geçerli |
| K-105 | 🟢 ADIM ⑤ KAPANDI — VE İKİ ÖLÇÜTÜMÜ KENDİ KAPILARIM ÇÜRÜTTÜ | 🟢 geçerli |
| K-106 | 🟢 SİMÜLATÖR FAZI KAPANDI — ve iki RFC açılınca İKİNCİ bir straw-man çıktı | 🟢 geçerli |
| K-107 | 🟢 DUYARLILIK DENETİMİ — 48 GEREKÇESİZ SAYI 34'E İNDİ, VE DÖRT ÖLÇÜT HATAM ÇIKTI | 🟢 geçerli |
| K-108 | 🔴 Lİ REPLİKASYONU: SAYI TUTMADI, MEKANİZMA TUTTU — sebep α | 🟢 geçerli |
| K-109 | 🔴 MİMARİ YARIMMIŞ — ölçüm katmanının hiçbir disiplini yoktu | 🟢 geçerli |
| K-110 | 🔴 ÜÇ BORÇ TEK ALETLE KAPANDI — ve dört şey daha çürüdü | 🟢 geçerli |
| K-111 | 🔴 DÖRT ÖLÇÜM ALETİ KOŞMUYORDU — ve ön-kayıtın şart koştuğu bir yetenek hiç yokmuş | 🟢 geçerli |
| K-112 | 🟢 KONTROL DÜZLEMİ MEKANİZMASI UYGULANDI — ve veri onayında gizli bir kusur ölçüldü | 🟢 geçerli |
| K-113 | 🟢 ÖĞRENCİNİN 10 EYLÜL KARARLARI — belgeler bilgi kaynağına çevrildi, iki ölçüm yenilendi | 🟢 geçerli |
| K-114 | 🟡 İKİNCİ TUR ONAYLARI — yapı planı yazıldı, dört ölçüm aleti kuruldu, bir süre tahmini ç | 🟢 geçerli |
| K-115 | 🟡 YAPI ADIMLARI — Y1 uygulandı: PSR alıcı tarafında, kontrol istatistikleri sayaç kütüğü | 🟢 geçerli |
| K-116 | 🟢 YAPI ADIMI Y4 — yere toplama deseni uygulandı | 🟢 geçerli |
| K-117 | 🟢 YAPI ADIMI Y5a — çoklu ve hareketli karıştırıcı mekanizması | 🟢 geçerli |
| K-118 | 🟢 YAPI ADIMI Y6 — formasyon kolu ve istasyon tutma | 🟢 geçerli |
| K-119 | 🟢 ÖĞRENCİ KARARLARI — Y5b aileleri, süreler, uzun koşu, derin sızma hareketi, yerleşim,  | 🟢 geçerli |
| K-120 | 🟢 YAPI ADIMI Y5b — tehdit senaryosu aileleri | 🟢 geçerli |
| K-121 | 🟢 YAPI ADIMI Y3 — kontrol düzlemi eksikleri (R2 · R3 · R4) | 🟢 geçerli |
| K-122 | 🟢 YAPI ADIMI Y7 — Θ'nın protokol başına raporlanması | 🟢 geçerli |
| K-123 | 🟢 YAPI ADIMI Y10 — evre metriklerinin TEK anlamlılık sabiti | 🟢 geçerli |
| K-124 | 🟢 ÖĞRENCİ KARARLARI — C1 ve C3'ün ölçütleri (taramadan ÖNCE ilan) | 🟢 geçerli |
| K-125 | 🟢 C1 — düğüm sayısı: ölçüm adayları AYIRAMADI, 40 doğrulandı | 🟢 geçerli |
| K-126 | 🟢 C3 — yere toplama yükü: ölçüm hızı SEÇMEDİ, 1,0'ı DOĞRULADI | 🟢 geçerli |
| K-127 | 🔴 C2 aile kapısı — hedef_koruma sert kısıtı ÇİĞNEDİ, çevrim kaldırıldı | 🟢 geçerli |
| K-128 | 🟢 C2 çapaları ve C7 — ikisi de doğrulandı, R eşiği DÜZELTİLDİ | 🟢 geçerli |
| K-129 | 🔴 D1 koştu ve İKİ ÖLÜ KAPI buldu — Aşama 2'nin zemini sınandı | 🟢 geçerli |
| K-130 | 🟢 DENETİM BULGULARI — kapılar çıkış koduna bağlandı, pencere ikizi DONDURULDU | 🟢 geçerli |
| K-131 | 🟢 PROTOKOL ARAYÜZÜ SON HÂLİNİ ALDI — tamponlama ve kancalara gözlem | 🟢 geçerli |
| K-132 | 🔴 İKİ AKLAMA ÇÖKTÜ, BİR AĞ BÖLÜNMESİ BULUNDU — ve iki ölçüm aleti kuralın yarısını uygul | 🟢 geçerli |
| K-133 | 🟢 DOĞRULAMA LİSTESİ UÇTAN UCA KOŞTU — 18/18, ve iki şey yakalandı | 🟢 geçerli |
| K-134 | 🟢 BEYAN KANALI KANCALARA AÇILDI — ve bir düşme sebebi nihayet yolunu buldu | 🟢 geçerli |
| K-135 | 🔴 TAMPON BİR YOKLAMA DÖNGÜSÜNE DÖNMÜŞTÜ — makul bir kural ölçümde çöktü | 🟢 geçerli |
| K-136 | 🟢 AŞAMA 2 AÇILDI — AODV yazıldı, U1–U4 geçti, ve U1'in kapısı YANLIŞ YERDEYDİ | 🟢 geçerli |
| K-137 | 🟢 U1 İKİYE AYRILDI — uygunluk bir KAPI, başarım bir BULGU | 🟢 geçerli |
| K-138 | 🟡 HIZ ARAŞTIRMASI — üç hipotez, üçü de ÖLÇÜMDE çöktü; bir borç kapandı | 🟢 geçerli |
| K-139 | 🔴 AODV'NİN ÖLÇÜM BEYANLARI YANLIŞ ANAHTARLANIYORDU — ve düzeltme ölçüm katmanında ikinci | 🟢 geçerli |
| **K-140** | 🟢 AODV KAPANDI — kapı yeni bir düşük hücreyi yakaladı, hüküm ölçülmüş tablodan yeniden ü | 🔄 **REVİZE → K-143 · K-145**<br>AODV kapanışının U1 tablosu `AODV-c` hâline aitti; RFC §6.11 öncül kuralı davranışı değiştirdi (K-143) ve kapanış `AODV-e` ile yeniden koşuldu (K-145). Açıklanmış düşük hücre 4 → **2** |
| K-141 | 🟢 COR ONARILDI — pay ve payda aynı birimi sayıyor, sayaç ikizi artık canlı | 🟢 geçerli |
| K-142 | 🟢 OLSR YAZILDI — üç özet hatası, bir straw-man tuzağı, çürüyen iki hipotez | 🟢 geçerli |
| K-143 | 🔴 AODV YENİDEN AÇILDI — RERR öncül kuralı uygulanmamıştı; AODV'yi hem pahalı hem kötü gö | 🟢 geçerli |
| K-144 | 🟢 AODV'NİN U3'Ü BULGU OLARAK RAPORLANDI — zayıf kapı ateş edebilen bir kapıyla değişti | 🟢 geçerli |
| K-145 | 🟢 AODV YENİDEN KAPANDI (AODV-e) — kapı iki ölü açıklama yakaladı ve biri benim kusurumu  | 🟢 geçerli |
| K-146 | 🟡 OLSR KAPANIŞ ÖLÇÜMÜ — hareketlide AODV'den iyi, statikte iki hücre düşük; sebep ÖLÇÜLD | 🟢 geçerli |
| K-147 | 🟢 OLSR KAPANDI (§13 ile) — statik öngörü BİREBİR tuttu; hareketli kolda öngörülmeyen bir | 🟢 geçerli |
| K-148 | 🟢 AOMDV YAZILDI — AODV'nin alt sınıfı; entegrasyonda Şekil 3'ün harfiyen uygulanmasının  | 🟢 geçerli |
| K-149 | 🟢 AOMDV KAPANDI — 12 hücrenin 12'sinde AODV'den iyi; düşük hücrenin sebebi ÖLÇÜLDÜ | 🟢 geçerli |
| K-150 | 🟡 AŞAMA 3 AÇILDI — DESPARETE v0.1 tasarım paketi okundu; simülatörle üç yapısal boşluk,  | 🟢 geçerli |
| K-151 | 🟢 sim2/ Y1 · Y2 — her unicast sonucunun bildirimi ve protokolün veri başlığı | 🟢 geçerli |

**62 kayıt · 1 revize · 61 geçerli**

<!-- INDEKS SONU -->

---

# K-090 · 🔴 SİMÜLATÖR SIFIRDAN YENİDEN YAZILDI — `sim/` EMEKLİ, `sim2/` DOĞDU

> **Tarih:** 3–5 Eylül 2026 · **Karar: öğrenci**

## NE
Eski simülatör (`sim/`) emekli edildi ve yerine `sim2/` sıfırdan yazıldı.
Eski kod, testleri ve çıktıları `arsiv/` altına taşındı.

## NEDEN
Eski simülatör iddia ettiği şeyi yapmıyordu. Ölçülen kusurlar:

| # | Kusur |
|---|---|
| 1 | Çerçeve süresi **birden çok yerde** hesaplanıyordu |
| 2 | **Alıcı zinciri kısıtı yoktu** — bir düğüm çakışan iki çerçeveyi de alabiliyordu |
| 3 | **Capture effect yoktu** |
| 4 | Topoloji **donuktu** — mobilite bağları güncellemiyordu |
| 5 | MAC, Kat 2 ile Kat 3'ü **karıştırıyordu** (PER hesabı MAC'in içindeydi) |
| 6 | Sayaç ifadeleri **iki yerde** tekrarlanıyordu ve ayrışabiliyordu |
| 7 | Geometri **2B**'ydi |
| 8 | **Gölgeleme ve sönümleme yoktu** |
| 9 | **Anten deseni yoktu** |
| 10 | Literatürün istediği **7 metrikten yalnız 2'si** üretiliyordu |

Öğrencinin gerekçesi aynen: *"takvim umurumda değil… proje bir nevi baştan
başlıyor… kapsam ve dürüstlük azalıyorsa zarar faydadan fazladır."*

## NE ELENDİ
**Kademeli düzeltme** *(`11-REFACTORING-ONERISI.md`)*. Elendi çünkü
kusurların çoğu **yapısaldı**: 2B geometri, donuk topoloji ve alıcı zinciri
kısıtının yokluğu birbirine bağlıydı; birini düzeltmek ötekini
düzeltmeden anlam taşımıyordu.

## NE TAŞINDI
Beş modül **denetlenerek** taşındı, kopyalanarak değil: olay kuyruğu,
gözlem yükü sözleşmesi, teşhis sözleşmesi ve iki yardımcı. Taşıma sırasında
`yuk.py` içinde çıplak bir `assert` bulundu ve `dogrula`ya çevrildi.

## SONUÇ (5 Eylül 2026)
`sim2/` 7 608 satır · 9 paket · **437 test** · Adım 0–9 bitti · uçtan uca
koşuyor, korunum denklemi ve mutabakat her koşuda denetleniyor · 7 metriğin
7'si tek koşudan çıkıyor.

## BUNU NE DEĞİŞTİRİR
Hiçbir şey — eski kod arşivde duruyor ve karşılaştırma gerekirse oradan
okunur. Ama `sim/`e geri dönmek, on kusuru geri almak demektir.

---

# K-091 · 🔴 SINR EŞİĞİ 10 → 16 dB — MENZİL, GEÇMEYEN BİR BAĞIN ÜSTÜNDE TANIMLIYDI

> **Tarih:** 5 Eylül 2026 · **Karar: danışman ölçtü, öğrencinin beyan ettiği
> gerçekçilik hedefi uygulandı**
> **Üretici:** `python kalibrasyon/bag_kalitesi.py` ·
> `python -u kalibrasyon/pdr_tavani.py`

## NE
`Konfig.sinr_esigi_db` 10,0 → **16,0**.

## NEDEN
Öğrencinin beyanı: *"normal şartlarda ortalıkta saldırı yoksa PDR %95–100
olmalı."* Ölçülen: **%10–30**. Arandı ve sebep bulundu.

Menzil, *"alınan güç = gürültü × β"* olacak şekilde tanımlıydı ve β = 10 dB
idi. Ölçüldü: menzil sınırında (280 m) 512 baytlık gövdenin hata olasılığı
**%75,5**. Yani topolojinin *"bağ"* dediği şey, fizik açısından çoğunlukla
**geçmeyen** bir bağdı.

Sorunun yönlendirme ya da tıkanıklık olmadığı iki ölçümle gösterildi:

1. **Kâhin (mükemmel) en-kısa-yol yönlendirmeyle** bile PDR 0,50.
2. PDR **yükten bağımsızdı**: 40 pkt/s'de 0,517 · 10 pkt/s'de 0,534.

Uçtan uca eşik taraması *(kâhin yönlendirme, karıştırıcı yok)*:

| β | PDR | PSR |
|---|---|---|
| 10 dB | 0,499 | 0,298 |
| 12 dB | 0,603 | 0,380 |
| 14 dB | 0,976 | 0,712 |
| **16 dB** | **1,000** | **0,817** |
| 20 dB | 1,000 | 0,822 |

## NE ELENDİ
- **Paket boyutunu küçültmek** — 128 bayta inince atlama başarısı 0,9965
  oluyor ama yük profili literatürden sapardı.
- **Yeniden deneme sınırını yükseltmek** — kök sebebi gizler, gecikmeyi şişirir.
- **20 dB ve üstü** — 16 dB'ye göre kazanç yok, girişim menzili ve maliyet var.

## NEDEN 16 — keyfî değil
10 dB çözülebilirlik + **2σ** gölgeleme marjı *(σ = 3 dB)* = 16 dB. Ölçüm ve
türetme aynı yere düşüyor. Telsiz mühendisliğinde menzil, alıcı
duyarlılığında değil, **duyarlılık + sönümleme marjında** tanımlanır.

## NE DEĞİŞMEZ
`iletim_menzili_m` sabit kaldı → geometri ve **Adım 3'ün yoğunluk
kalibrasyonu** *(derece 7,271 · bağlı %78,2)* aynen geçerli. Girişime karşı
marj da değişmedi: herkesin gücü aynı oranda arttı.

## NE DEĞİŞİR
Verici gücü 18,50 → **24,50 dBm** *(tam 6 dB)*. `girisim_orani` bundan
türetildiği için 2,154 → **3,415**; girişim menzili 603 → 956 m. Koşu süresi
~%40 arttı. 🔴 **Karıştırıcı gücü bundan SONRA kalibre edilmeli.**

## ⚠️ ÖDENEN BEDEL — ölçüldü, gizlenmiyor
Girişim menzili 603 → 956 m. Alan 1000 × 1000 m olduğu için artık neredeyse
her düğüm her düğümü duyuyor: bir çerçeve ~15 yerine ~39 alıcıda alım
denemesi doğuruyor ve **mekânsal yeniden kullanım pratikte kalmadı**.
Ölçüldü: tam uzunlukta bir koşu **35–62 s → 148–203 s** *(~3,5×)*;
iletim başına maliyet statik kolda 2 200 → **5 104 µs**, reaktif karıştırıcı
kolunda 21 968 → **29 065 µs**. Tarama bütçesi Adım 11'de yeniden ölçülmeli.

## BUNU NE DEĞİŞTİRİR
Gölgeleme σ'sı değişirse marj yeniden türetilmeli. Modülasyon ya da paket
boyutu değişirse eşik yeniden ölçülmeli — PER eğrisi kayar. Bütçe
kaldırılamaz olursa seçenekler: alanı büyütmek *(yoğunluğu koruyarak)*,
paralel koşum, ya da hedefli hızlandırma.

---

# K-092 · 🔴 KARIŞTIRICI, TAŞIYICI DİNLEMEYE MESAFEDEN BAĞIMSIZ GÖRÜNÜYORDU

> **Tarih:** 5 Eylül 2026 · **Karar: danışman** *(bu bir KUSUR düzeltmesidir,
> bir tercih değil)*

## NE
`Dugum.karistirici_mesgul_mu()` eklendi. Karıştırıcı artık taşıyıcı dinlemeyi
yalnız **alınan gücü gürültü tabanının üstünde olan** düğümlerde tetikliyor.

## NEDEN
`Karistirici.csma_ya_gorunur(t_s)` bir **alıcı argümanı almıyordu**. Sonuç:
aldatıcı karıştırıcı 1 km uzakta bile olsa alandaki **her** düğüm
erteliyordu. Ölçüldü: `aldatici` kolunda 320 pakete karşı **0 iletim
denemesi, 0 teslim** — bütün ağ, gücü ne olursa olsun kilitleniyordu.

Bu fiziksel olarak imkânsızdır: taşıyıcı dinleme bir **güç eşiğidir**,
küresel bir anahtar değil. Kusur, aldatıcı kolunun üç senaryosunu
*(statik · bağımsız · görev)* **tümüyle ölçülemez** yapıyordu: bütün
protokoller aynı sıfırı alırdı ve fark ölçümü anlamsızlaşırdı.

## NASIL BULUNDU
Öğrenci *"aldatıcı hakkında bir sıkıntımız var"* dedi. Adım 9 kapanış
betiğinin aldatıcı satırındaki `deneme = 0` sayısı zaten oradaydı ve
düzeltmeyi tetikleyen şey o oldu.

## EŞİK NEDEN GÜRÜLTÜ TABANI
`girisim.kanal_mesgul_mu`nun varsayılanıyla aynı olsun diye. İki yerde iki
farklı eşik olsaydı *"kanal meşgul mü"* sorusunun iki cevabı olurdu — ikinci
doğru kaynağı tuzağının ta kendisi.

## BUNU NE DEĞİŞTİRİR
CCA eşiği gürültü tabanından ayrı bir parametre yapılırsa burası da onu
kullanmalı.

---

# K-093 · 🔒 DEPO SADELEŞTİRİLDİ — EMEKLİ HER ŞEY `arsiv/` ALTINA

> **Tarih:** 5 Eylül 2026 · **Karar: öğrenci**

## NE
`sim/` · `tests/` · `dogrulama/` · `denetim/` · `ciktilar/` · `aile0_audit.md`
ve dört v2 belgesi *(`07` · `08` · `11` · `13`)* `arsiv/` altına taşındı.
Kök `README.md` ve yeni `DEVIR.md` baştan yazıldı.

## NEDEN
Yeni bir ajanın devralması gerekiyordu ve depoda **iki simülatör, iki test
paketi ve iki devir belgesi** vardı. Hangisinin güncel olduğu koddan
okunamıyordu — `03-YONTEM-KURALLARI`nin *"ikinci doğru kaynağı"*
tuzağının belge hâli.

## NE SİLİNDİ
**Hiçbir şey.** Taşındı, silinmedi. Arşiv karşılaştırma için duruyor.

## DOĞRULANDI
`sim2/` · `tests2/` · `kalibrasyon/` · `protokoller/` içinde emekli koda
**tek bir içe aktarım yok** — AST ile tarandı.

---

# K-094 · 🔴 BULGU — BEACON MENZİLİ VERİ MENZİLİNDEN GENİŞ, "KOMŞU" TANIMI YETERSİZ

> **Tarih:** 5 Eylül 2026 · **Durum: KARARA BAĞLANMADI** — devralan ajanın
> çözeceği açık madde *(`DEVIR.md` §6.4)*
> **Üretici:** `python kalibrasyon/adim9_kapanis.py` ·
> `python -u kalibrasyon/pdr_tavani.py`

## NE ÖLÇÜLDÜ
Aynı çalışma noktasında *(β = 16 dB, karıştırıcı yok)*:

| yönlendirme | PSR |
|---|---|
| kâhin en-kısa-yol | **0,817** |
| `DogrudanKomsu` *(komşu tablosundan seçiyor)* | **0,17 – 0,29** |

## NEDEN
Beacon **32 bayt** ve dayanıklı **temel hızda** *(DBPSK 1 Mb/s)*; veri
çerçevesi **512 bayt** ve **DQPSK 2 Mb/s**. Yani beacon'ın duyulduğu mesafe,
verinin geçtiği mesafeden **geniştir**. Komşu tablosu beacon'dan kurulduğu
için içinde **veriyi taşıyamayacak bağlar** var; atlama sayısına bakan bir
protokol bunlara körü körüne gönderir.

## 🔒 BU BİR SİMÜLATÖR KUSURU DEĞİL
Gerçek ağlarda da böyledir. Atlama sayısına göre yönlendiren protokoller en
uzun — yani en kötü — bağı seçer; ETX metriği *(De Couto ve ark., 2003)* tam
olarak bunun için icat edildi. ⚠️ **Bu atıf `02-DOGRULANMIS-KAYNAKLAR.md`de
doğrulanmadan rapora giremez.**

## NEDEN KARAR GEREKTİRİYOR
AODV atlama sayısıyla yönlendirir, yani bu tuzağa **tasarımı gereği** düşer.
Bu, özgün protokolün fark yaratabileceği yerlerden biri **olabilir** —
🔴 ama **ölçülmeden iddia edilmez**. Karara bağlanacak iki şey:

1. Taban çizgileri bağ kalitesi ölçütü kullanacak mı? Kullandırmak onları
   *"literatürdeki AODV"* olmaktan çıkarır ve kıyas tabanını yumuşatır.
2. Gözlem penceresi yeterli mi? Protokol; `son_iletim_sonucu`,
   `duyulan_beacon` sayısı ve `bildirdigi_*` alanlarıyla bağ kalitesini
   **kendisi tahmin edebilir** — pencereyi genişletmeye gerek yok.
   🔴 `05-GOZLEM-PENCERESI.md` genişletilemez bir sözleşmedir.

## BUNU NE DEĞİŞTİRİR
Beacon boyutu ya da hızı değişirse asimetri değişir. Beacon veri hızına
çekilirse asimetri kapanır ama beacon kaybı artar — ölçülmeden yapılmaz.


## 🔴 5 EYLÜL 2026 — MEKANİZMA DÜZELTMESİ *(sonuç değişmedi, GEREKÇE yanlıştı)*

Yukarıda *"beacon 32 bayt ve dayanıklı temel hızda (DBPSK 1 Mb/s); veri
çerçevesi 512 bayt ve DQPSK 2 Mb/s"* yazıyor. **Bu yanlış.**

`kanal.py` gövde PER'ini **her çerçeve tipi için** `Konfig.modulasyon`
(DQPSK, 2 Mb/s) ile hesaplıyor; temel hızda DBPSK ile gönderilen tek şey
**önbelge**, ve o veri çerçevesinde de öyle. Yani beacon ile veri arasında
**modülasyon farkı yok**.

**Asıl mekanizma UZUNLUK:** beacon gövdesi 256 bit, veri gövdesi 4 096 bit.
Aynı bit hata oranında 16 kat kısa bir çerçeve çok daha uzağa geçer.

**Ölçüldü** *(önbelge dâhil, saf yol kaybı, β = 16 dB)*:

| çerçeve | alım hatası 0,10 | alım hatası 0,50 |
|---|---|---|
| veri (512 B) | 395 m | 428 m |
| beacon (32 B) | 447 m | **500 m** |
| onay (14 B) | 465 m | 524 m |

beacon/veri yarıçap oranı **1,17** *(alan oranı 1,37)*.

⚠️ **Ve asıl büyük fark bu değil:** beacon yarıçapı, topolojinin "bağ" dediği
280 m'nin **1,79 katı**. Komşu tablosunu 280 m'ye hapseden hiçbir şey yok —
duyma kümesi girişim menziliyle (956 m) geometrik, alım ise SINR'la
belirleniyor. Ayrıntı ve sonuçları: **K-096**.

🔒 **Sonuç değişmedi**, gerekçe değişti: komşu tablosunda veriyi
taşıyamayacak bağlar var ve atlama sayısına bakan bir protokol onlara körü
körüne gönderiyor. Değişen şey, bunun *neden* böyle olduğu.

---

# K-095 · 🔴 SÖNÜMLEME ÖNBELLEĞİ SINIRSIZDI — HAREKETLİ KOLLAR KOŞULAMIYORDU

> **Tarih:** 5 Eylül 2026 · **Karar: ajan** *(öğrenci onayıyla)* · **Durum: UYGULANDI**
> **Üretici:** `python kalibrasyon/sonumleme_onbellegi.py`

## NE ÖLÇÜLDÜ
`Sonumleme._yenilik`in memo'su sınırsızdı. Hareketli bir kolda:

| büyüklük | ölçülen |
|---|---|
| büyüme hızı | **372 000 – 405 000 girdi / simüle edilen saniye** *(doğrusal)* |
| girdi başına | **190 – 193 bayt** |
| 350 s hareketli koşunun isteyeceği | **~25 GB** |
| makinede olan | 15,7 GB |

Yani **18 senaryonun 12'si — bütün hareketli kollar — tam uzunlukta
koşulamıyordu.**

## ⚠️ NEDEN BUGÜNE KADAR GÖRÜNMEDİ
Statik kolda sönümleme dondurulduğu için (`_donuk`) önbellek **1 530**
girdide kalıyor. `sim2/`de bugüne kadar yapılan bütün tam uzunluk ölçümleri
statik koldaydı; hiçbiri bu duvara çarpmadı. Kusur, ölçümün yanlış rejimde
koşmasıyla gizlenmişti — `03` B6'nın sınıfı.

🔴 Ve ilk teşhisim yanlıştı: kusur bir `MemoryError` ile ortaya çıktı, ama o
çöküş **üç ağır sürecin aynı anda koşturulmasından** kaynaklanıyordu. Tek
süreçte aynı komut sorunsuz tamamlanıyor. Kanıt çöküş değil, **büyüme hızı**.

## KARAR
Önbellek sınırlandı: `YENILIK_ONBELLEK_SINIRI = 250_000`, politika
**dolunca tamamen boşalt**. `kanal/yayilim.py`deki `KOSE_ONBELLEK_SINIRI`
ile aynı desen — aynı kusur o modülde daha önce teşhis edilip çözülmüş,
sönümleme tarafında atlanmıştı.

## NEDEN ZARARSIZ — bu ölçüm değil, YAPI
`_yenilik`, `normal_cekimi(alan, tohum, i, j, indeks)`in memo'sudur: değer
yalnız anahtara bağlıdır, çağrı sırasına değil. Bir girdiyi atmak onu
**yeniden hesaplatır**, başka bir sayı üretmez.

🔒 Yine de ölçüldü, çünkü kanıtlanan şey matematik değil **uygulamadır**.

## ALTERNATİFLER — ve neden elendiler
| aday | neden elendi |
|---|---|
| **Önbelleği tamamen kaldır** | İsabet oranı %86; kaldırmak çekim sayısını ~7 katına çıkarır |
| **İki kuşaklı önbellek** *(LRU yaklaşımı)* | İsabet oranına 0,1 puan katıyor ama iki sözlük tutuyor (iki kat bellek) ve tahliyede kopyaladığı için ~%8 daha yavaş |
| **Bağ başına halka tampon** | FIR erişimi neredeyse tek yönlü olduğu için cazip, ama ölçüm en basit politikanın zaten yettiğini gösterdi; karmaşıklığın karşılığı yok |
| **Sınırı `Konfig`e alan olarak koymak** | Bir performans parametresini tedavi gibi gösterirdi. `arac_hash` zaten `sim2/` kaynağının tamamını özetlediği için modül sabiti kökene otomatik giriyor |
| **Her çağrıda isabet sayacı** | %11 CPU ölçüldü; 100 saatlik bir taramada 11 saat. Tahliye sayacı (koşu başına ~30 artış) aynı bilgiyi %0,4 sapmayla veriyor |

## DOĞRULANDI — dört ayrı kapı
1. **Birebir aynılık.** Üç senaryo *(bagimsiz-yok · bagimsiz-surekli ·
   statik-yok)* × üç sınır *(1 000 000 · 250 000 · 100 000)*. Karşılaştırılan
   şey yalnız özet değil: **tam sonuç satırı** + **ham teslim dizisi**
   *(paket kimliği, akış kimliği, tam duyarlıkta gecikme)*. Hepsi aynı.
2. **Depo kodu ile referans farkı: 6 alan, hepsi `arac_hash` ve ondan türeyen
   `kosu_kimligi`** — yani kaynak değişince tanım gereği değişen köken
   damgaları. Başka hiçbir alan oynamadı.
3. **Mutasyon denemesi.** Üç bozuk uygulama *(tahliyede tohum kayması ·
   sınırın uygulanmaması · tahliyede yapışkan değer)* kuruldu; **üçü de
   yakalandı**, hiçbiri testlerden kaçamadı.
4. **Tam uzunluk kapısı.** 350 s hareketli koşu **1 262 s**'de tamamlandı,
   önbellek 250 000'i hiç aşmadı *(567 tahliye)*, `korunum + mutabakat TAMAM`.
   Bu, `sim2/`de yapılan **ilk tam uzunluk hareketli koşusudur**.

## ⚠️ MEVCUT TESTLER YETMİYORDU
`test_IZLER_cagri_sirasindan_BAGIMSIZ` ve kardeşleri 200–600 çağrı yapıyor;
üretim sınırı 250 000. Yani **sınırlı önbellek bozuk yazılsa o testler yine
geçerdi**. Eklenen altı test sınırı küçültüp tahliyeyi **zorluyor** ve
ölçtüğü şey *"önbellek çalışıyor mu"* değil, *"tahliye edilmiş bir girdi
geri geldiğinde aynı sayıyı mı veriyor"*.

Ayrıca `test_MODUL_SABITI_ornege_BAGLI` eklendi: sabit ilan edilip
kullanılmıyor olsaydı, değerini değiştirmek hiçbir şeyi değiştirmezdi ve
bunu kimse fark etmezdi.

## BUNU NE DEĞİŞTİRİR
- Sınır bir gün yetmezse bedeli **sessiz bir CPU kaybıdır**. Bu yüzden
  `teshis.sonumleme_onbellegi` her sonuç satırına yazılıyor: ıskalama ≈
  tahliye × sınır + kalan girdi.
- Çalışma noktası değişince *(yol kaybı üsteli, hızlar)* FIR uzar ve çalışma
  kümesi büyür. Sınır o gün yeniden ölçülmelidir; ölçüm **kendini raporlar**.
- `kalibrasyon/adim4_sonumleme.py`de önbellek boyutunu yazdıran satırın
  **etiketi düzeltildi**: sayı artık "toplam çekim" değil "şu an tutulan".
  Anlamı sessizce kaydırmak `03` B5'in *"etiketi elle taşımak"* tuzağıydı.

## 🔴 KOŞUM BAŞINA KALMALI
Önbellek anahtarı **tohumu içermez**. Modül düzeyine taşınır ya da koşumlar
arasında paylaşılırsa aynı anahtar farklı tohumda farklı değere karşılık
gelir ve **sessizce yanlış sonuç** üretir. Paylaştırmak isteyen önce anahtara
tohumu koymak zorundadır.

---

# K-096 · 🔴 ÇALIŞMA NOKTASI ÖLÇÜLDÜ — ÜÇ AYRI YARIÇAP, VE MACH 4'TE UÇAN İHA'LAR

> **Tarih:** 5 Eylül 2026 · **Karar: ajan** · **Durum: KARAR VERİLDİ, UYGULANMADI**
> **Üretici:** `scratchpad/gercek_yaricap.py` · `gercek_derece.py` ·
> `atlama_dagilimi.py` · `hiz_karari.py` *(kalibrasyona taşınacak)*

## NE ÖLÇÜLDÜ — 1: "menzil" tek bir sayı değil
`iletim_menzili_m = 280 m` **veri yolunda hiçbir yeri kapamıyor**: kimin
duyacağını girişim menzili (956 m), alınıp alınmadığını SINR belirliyor.
280 m yalnızca verici gücünün türetildiği bir çapa ve kalibrasyon
betiklerinin topoloji anlık görüntüsü.

| yarıçap | anlamı | değer |
|---|---|---|
| çapa | SINR tam eşiğe eşit *(2σ gölgeleme marjı dâhil)* | 280 m |
| kullanılabilir bağ | atlama başarısı ≥ 0,95, denemelerle | ~430 m |
| komşu tablosu | beacon'ın %50 alındığı mesafe | ~500 m |
| duyma / girişim | kimin kimi duyduğu | 956 m |

**Sonucu:** gölgeleme ve sönümleme dâhil ölçülen gerçek derece **12,9**
*(çapada 6,5)*, gerçek ortalama atlama **1,81** *(çapada 3,15)*.

## NE ÖLÇÜLDÜ — 2: yönlendirmenin yapacak işi yok
Kullanılabilir bağ grafiğinde, 1000 m alanda çiftlerin dağılımı:
**%33,1'i 1 atlama · %53,7'si 2 atlama · %13,1'i 3 atlama.** Yani
**%86,8'i ≤ 2 atlama.** Çok atlamalı mesh yönlendirme hakkında bir projede
yönlendirmenin ifade edebileceği fark büyük ölçüde kapalı.

## NE ÖLÇÜLDÜ — 3: hızlar ölçek dışı
Bağıl hız **26,4 m/s**, rota ömrü **4,0 s** *(1400 m alanda 2,6 s)*.
OLSR'ın `TOP_HOLD_TIME`ı 15 s: yani topoloji bilgisi **kullanılmadan
bayatlıyor** ve OLSR kurulum yüzünden zayıflatılmış oluyor — `03` kural 4'ün
yasakladığı straw-man, yalnızca kasıtsız.

🔴 **Ölçek tutarlılığı testi**: 1/50 ölçekte aynı SNR'ı korumak
`Pt_gerçek = Pt_sim + 10·α·log₁₀(50)` ister.
α = 2 → 34 dBm = **2,5 W** *(makul bir taktik İHA veri bağı)*.
α = 3 → 75,5 dBm = **35 kW** *(fiziksel olarak imkânsız)*.
Ayrıca iki-ışın kırılma mesafesi `4·h₁·h₂/λ` sim'de 157 km, tam ölçekte
288 000 km — bağ mesafeleri ikisinde de çok altında, yani **her iki dünya da
serbest uzay rejiminde**. α = 3,0 hava-hava bağ için savunulamıyor.

## KARARLAR — ölçütleri ölçümden ÖNCE ilan edilmiştir
1. **Yol kaybı üsteli 3,0 → 2,0.**
2. **Alan büyür**, kesin değeri α değiştikten sonra ölçülerek seçilir.
   İlan edilen ölçüt: **çiftlerin ≥ %45'i 3+ atlama · kopukluk %0 ·
   derece ≥ 7** *(karıştırma bağ sildiğinde ağın kolayca ikiye ayrılmaması
   için pay)*.
3. **Hızlar ölçeklenir.** İlan edilen ölçüt: **rota ömrü ≥ 3 × OLSR
   TOP_HOLD_TIME = 45 s**. Ölçüt doğrulanmamış bir menzil sayısına değil,
   doğrulanmış RFC tablosuna dayanıyor.
4. **`gm_alfa` 0,85 → 0,983.** Hız korelasyon süresi bir **araç dinamiği**
   zamanıdır ve ölçeklenmez; 3,1 s yerine ~30 s olmalı.
5. **Doppler platform hızından ayrılır.** Kavanoz geometriyi ölçekler,
   **dalga boyunu ölçekleyemez**. Korunması gereken boyutsuz büyüklük
   "kanal bir çerçeve boyunca kaç kez değişiyor"dur; bunun için sönümleme
   tam ölçek hızını kullanmalı. Konfigürasyona birinci sınıf bir `olcek`
   alanı girer, böylece kavanoz–gerçek eşlemesi tek ve denetlenebilir bir
   yerde durur.
6. **Düğüm sayısı 40 kalır** *(doğrulanmış derleme: tablo tabanlı
   yaklaşımlar küçük FANET'lere uygun)*.

## ⚠️ BU OTURUMDA GERİ ALINAN İDDİALAR
| iddia | neden düştü |
|---|---|
| *"Etkin yarıçap 320 m"* | Kenar etkisi ihmal edilmişti; doğrusu ~430 m |
| *"GM düğümleri merkeze topluyor"* | **6 tohumluk gürültü.** 25 tohumda sapma güven aralığının içinde |
| *"Alan 1600 m'ye çıksın, hedef derece 7"* | Hedef, kullanılmayan bir grafikten okunmuş artefakttı. Yeni gerekçe farklı ve ölçülü |
| *"Sürekli karıştırıcı CSMA'yı tetiklediği için tek yönlü değil"* | Gürültü karıştırıcıları CSMA'yı **hiç** tetiklemiyor |
| *"Reaktif karıştırıcı iş görmüyor"* | Tek tohum · 10 s · döngü üreten aletle alınmış tablodan çıkarılamaz |

🔒 Beşi de ölçüm genişletilerek düştü, tartışmayla değil.

## BEYAN EDİLMEMİŞ DÖRT KAPSAM SINIRI — rapora yazılacak
1. **Hız uyarlaması yok** *(sabit 2 Mb/s DQPSK)*. Gerçek 802.11b kötü bağda
   1 Mb/s DBPSK'ye düşer ve bu karıştırmaya karşı gerçek bir savunmadır.
2. **Yayılma kazancı yok.** 802.11b'nin 11 çipli Barker dizisi dar bantlı
   girişime ~10 dB kazanç verir; bant genişliği = bit hızı olduğu için
   burada yayma yok. Karıştırıcı gerçekte olduğundan **~10 dB etkili**.
3. **Enerji sezmeli taşıyıcı dinleme yok** — yalnız önbelge sezme var.
   Güçlü bir gürültü karıştırıcısı hiç ertelemeye yol açmıyor.
4. **Tek kanal, kanal değiştirme yok.** Bu projenin **öncülü**: çözüm
   yönlendirme katmanında aranıyor. Öncül olarak açıkça yazılmalı.

## BUNU NE DEĞİŞTİRİR
Adım 3 *(yoğunluk)* ve Adım 4 *(kanal)* kalibrasyonları **yeniden
yapılmalı** — ve bu sefer geometrik grafikte değil, **kullanılabilir bağ
grafiğinde**. Ön-kayıt bu liste kapanmadan mühürlenemez.

---

# K-097 · 🔴 ÇALIŞMA NOKTASI DEĞİŞTİ — α = 2,0 ve ALAN 1800 m · VE İLAN ETTİĞİM ÖLÇÜT INFEASIBLE ÇIKTI

> **Tarih:** 5 Eylül 2026 · **Karar: ajan** *(öğrenci kararları devretti)* ·
> **Durum: UYGULANDI**
> **Üretici:** `python kalibrasyon/calisma_noktasi.py`

## NE DEĞİŞTİ
| alan | eski | yeni |
|---|---|---|
| `yol_kaybi_usteli` (α) | 3,0 | **2,0** |
| `alan_en_m` / `alan_boy_m` | 1 000 m | **1 800 m** |

Türetilen sonuçlar: verici gücü 24,50 → **0,03 dBm** · girişim oranı 3,415 →
**6,310** · girişim menzili 956 → **1 767 m** · etkin/çapa yarıçap oranı
1,54 → **1,91**.

## NEDEN α = 2,0 — iki bağımsız hesap aynı yere düşüyor
**1 · İki-ışın kırılma mesafesi** `d_b = 4·h₁·h₂/λ`: simülasyonda (h = 70 m)
157 km, tam ölçekte (h = 3 km) 288 000 km. Bağ mesafeleri ikisinde de çok
altında → **her iki dünya da serbest uzay rejiminde**. Eski gerekçe
*"kentsel/engelli ortam"* yazıyordu; bu bir YER ağı değeridir.

**2 · Ölçek tutarlılığı.** 1:50 ölçekte `Pt_gerçek = Pt_sim + 10·α·log₁₀(50)`:
α = 2 → 34 dBm = **2,5 W** *(makul bir taktik İHA veri bağı)*;
α = 3 → 75,5 dBm = **35 kW** *(fiziksel olarak imkânsız)*.
Yani α = 3, kavanozun dışına çıkarıldığında **var olamayan bir telsiz** tarif
ediyordu. Bağ bütçesi de kapanıyor: 2,5 W · 2,4 GHz · serbest uzay · 26,7 km
→ alınan −94,6 dBm, gürültü tabanı −105 dBm, SINR 10,4 dB — tam olarak
çözülebilirlik eşiği.

## NEDEN ALAN 1800 m
Eski alanda ağ, yönlendirmeye **iş bırakmıyordu**. Kullanılabilir bağ
grafiğinde ölçülen atlama dağılımı *(20 tohum)*:

| alan | derece | 1 atl | 2 atl | ≥3 atl | kopukluk (statik, 30 tohum) |
|---|---|---|---|---|---|
| **1 000** *(eski)* | 18,60 | %47,7 | %52,0 | **%0,3** | %0,0 |
| 1 400 | 12,36 | %31,7 | %57,8 | %10,5 | %0,0 |
| 1 750 | 8,97 | %23,0 | %47,3 | %29,7 | %0,0 |
| **1 800** *(yeni)* | 8,67 | %22,2 | %46,8 | **%31,0** | **%0,0** |
| 1 850 | 8,23 | %21,1 | %44,2 | %34,5 | %0,2 |
| 2 000 | 6,88 | %17,6 | %37,0 | %44,9 | %0,5 |

Eski alanda çiftlerin **%99,7'si bir ya da iki atlama**. Bir yönlendirme
karşılaştırmasının orada söyleyebileceği pek bir şey yok: tarama
*"protokoller arasında fark yok"* derdi ve bu, farkın yokluğu değil
**başlığın yokluğu** olurdu.

## 🔴 İLAN ETTİĞİM ÖLÇÜT INFEASIBLE ÇIKTI — ve bunu saklamıyorum
Tarama koşulmadan önce şunu ilan etmiştim:
> çiftlerin ≥ %45'i 3+ atlama · kopukluk %0 · ortalama derece ≥ 7

**Hiçbir alan bunu sağlamadı.** Sebebi bir parametre seçimi değil, ölçütün
kendi iç yapısı:

- **(kopukluk %0) ile (derece ≥ 7) AYNI ŞEY.** Rastgele geometrik bir
  grafikte bağlantılılık, dereceyi eşiğin üstünde tutmaktan başka bir şey
  değildir. İki madde bir madde.
- **(≥%45 derin) ile (kopukluk %0) BİRBİRİNİ DIŞLAR.** Derece ≈ n·π/(L/r)²
  ve derinlik ≈ L/r olduğundan, n = 40 sabitken **derece × derinlik² sabit**.
  Ölçülen sınır: derece 7'de derin çift payı en çok ~%44,5. Ölçüt %45
  istiyordu — frontier'ın **bir puan** dışında.
- **"7" çürütülmüş bir sayıdan miras kalmıştı**: Adım 3'ün derece 7,45
  kalibrasyonundan, ki K-096 onu geçersiz ilan etmişti.
- **"%0" hareketli kola hiç uygulanamazdı**: `senaryolar.py` mobil kolda
  fasılalı bölünmeyi zaten belgeliyor. Ölçüldü: 1700 m'de bile 10 tohumun
  3'ü en az bir anda kopuyor, en kötü anda çiftlerin %9,7'si ulaşılamaz.
  Bağlantılılık koşulu **statik kola** aittir — U1 orada koşar.

🔒 **Bunların hepsi taramaya bakmadan görülebilirdi.** Ölçüt kötü koşulmadı;
**kötü yazıldı.**

## YENİDEN FORMÜLASYON — eşik gevşetilmedi, infeasible kısıt AMACA taşındı
    Sert kısıt : statik kolda 30 tohumun hiçbirinde ulaşılamaz çift yok
    Amaç       : bu kısıt altında atlama derinliğini EN BÜYÜK yapmak
    Sonuç      : 1 800 m — kopukluğun sıfır kaldığı EN BÜYÜK alan

⚠️ Bu bir eşik gevşetmesi **değildir** ve aradaki fark önemlidir: sağlanamayan
bir kısıt kısıt olmaktan çıkıp amaç olur, sağlanabilen kısıt **aynen kalır**.
Yeni ölçütün **sıfır serbest parametresi** var; 1800 sayısını ben koymadım,
veri koydu. Yine de bu bir yeniden formülasyondur ve öğrenci itiraz ederse
alan değişir.

## ⚠️ ÖLÇÜMÜN KENDİSİNDE DÜZELTİLEN İKİ KUSUR
1. **6 tohum yetmiyordu.** İlk tarama 1920–1950 m'de *"kopukluk %0"* gösterdi;
   20 tohumda aynı noktalar %0,5–0,8 çıktı. İyimser gürültüydü.
2. **Tek anlık görüntü yetmiyordu.** Alan taraması t = 100 s'de ölçüyordu.
   Ölçüt *"ağ kopmasın"* diyorsa zaman boyunca ve hareketli kolda da
   ölçülmeliydi; ölçülünce hareketli kolun hiçbir alanda %0 vermediği
   görüldü. Bu, ölçütün hangi kola ait olduğunu belirledi.

## BUNU NE GEÇERSİZ KILAR
- **Adım 3'ün yoğunluk kalibrasyonu** *(derece 7,271 · bağlı %78,2)* —
  zaten K-096 ile geçersizdi, şimdi alan da değişti. `konfig.py`deki blok
  düzeltildi ve eski sayılar "GEÇERSİZ" etiketiyle duruyor.
- **Adım 4'ün kanal kalibrasyonu** — α değiştiği için yeniden koşulmalı.
  `adim4_kapanis.py` yeni değerlerle koşuyor; içindeki elle yazılmış
  *"esik (10 dB)"* etiketi konfigden okunur hâle getirildi.
- **Karıştırıcı gücü** — çalışma noktası değiştiği için 6.1'in taraması
  bundan sonra yapılmalı.
- **Görev kolunun parametreleri** — yoğunluk eşitlemesi kullanılabilir bağ
  grafiğinde yeniden yapılmalı.

## SIRADA NE VAR
Hızların 1/50 ölçeğe çekilmesi · `gm_alfa` 0,85 → 0,983 · Doppler'in platform
hızından ayrılması · `olcek` alanının eklenmesi. Ölçütü ilan edildi: **rota
ömrü ≥ 3 × OLSR TOP_HOLD_TIME = 45 s** *(bugün 2,6 s)*.

---

# K-098 · 🔴 KÂHİN KANALDAN KURULUYOR — VE ÖLÇÜM ALETİM KENDİ HAYALET BAĞLARINI ÜRETİYORMUŞ

> **Tarih:** 5 Eylül 2026 · **Karar: ajan** · **Durum: UYGULANDI**
> **Üretici:** `python -u kalibrasyon/pdr_tavani.py` · `kalibrasyon/kahin.py`

## NE KIRILDI
Alan 1800 m'ye çıkınca (K-097) kâhin yönlendirici **kopuk bir grafikte**
kaldı: `Topoloji`nin 280 m'lik diski o alanda derece 2,57 veriyor. Kâhin
tabanlı bütün kalibrasyonlar — PDR tavanı, karıştırıcı gücü — koşamaz hâle
geldi.

## ⚠️ VE TEK BİR YARIÇAP ÇÖZÜM DEĞİLDİ
Önce "doğru yarıçapı bul" denendi. Ölçüldü: **hiçbir yarıçap işe yaramıyor.**
Derece eşitlense bile (r = 560 m'de 8,23 ↔ 8,25) kenarların yalnız yarısı
örtüşüyor — **Jaccard 0,53**; 51 gerçek bağ diskte yok, 51 disk bağı
gerçekte yok. Sebebi gölgeleme: σ = 3 dB, α = 2'de mesafede ±%41. "Menzil"
bir daire değil, kenarları 1,4 kat oynayan bulanık bir buluttur.

🔒 Sonuç: `Topoloji`nin komşuluk grafiği bir **TEŞHİStir**, bağlantılılık
modeli değil. Kâhin ve bağlantılılık ölçümü **kanaldan** beslenmelidir.

## ÜÇ HİPOTEZ — İKİSİ ÖLÇÜMLE ÖLDÜ
Yeni alanda kâhin tavanı statik kolda **0,511 – 0,911** çıktı; beklenen
0,95–1,00 idi. Üç aday sırayla sınandı:

| hipotez | sınama | sonuç |
|---|---|---|
| Yeniden deneme sınırı düşük (5 deneme, 802.11 kısa çerçeve 7 der) | sınır 4 → 6 | PDR 0,511 → 0,514. **ÖLÜ** |
| Tıkanıklık | yük 40 → 5 pkt/s | PDR 0,511 → 0,511; onaysız oranı %68,5 → %68,4. **ÖLÜ** |
| **Kâhinin kendi bağ modeli yanlış** | yavaş kanal ↔ sönümlemeli karşılaştırması | **DOĞRULANDI** |

## 🔴 ASIL KUSUR: KÂHİN SÖNÜMLEMEYİ GÖRMÜYORDU
Bağ kalitesini `yavas_alinan_w`den alıyordum — gölgeleme var, **sönümleme
yok**. Gerekçesini de yazmıştım: *"sönümleme saniyede yüzlerce kez değişir,
onu bağ kalitesine katmak anlık bir fadingi bağın kalıcı özelliği saymak
olurdu."* **Gerekçe yanlıştı.**

Ölçüldü *(statik-yok, tohum 1002, eşikli graftaki 161 bağ)*:

| büyüklük | yavaş kanal | sönümleme dâhil |
|---|---|---|
| tek deneme başarısı, ortalama | 0,881 | **0,710** |
| tek deneme başarısı, en kötü bağ | 0,374 | **0,000** |
| kâhinin "iyi" sandığı ama atlama < 0,90 olan bağ | — | **%26** |

Yani ölçüm aletim, K-094'te protokollere atfettiğim **hayalet bağ tuzağının
aynısına kendi düşmüştü** — ve bunu modül başlığına *"biraz iyimser"* diye
beyan etmiştim. "Biraz" değildi.

⚠️ Statik kolda sönümleme **dondurulmuştur**, yani orada ortalama alınacak
bir şey yok: her bağın tek bir donmuş kazancı vardır ve bağın kalıcı
kalitesi odur. Kâhin o kazancı hiç görmüyordu. *(Bu, "kaç örnek yeter"
sorusunu da anlamsız kıldı: K = 2, 4, 8, 16, 48 aynı sonucu veriyor.)*

## SONUÇ — TAVAN GERİ GELDİ
Düzeltilmiş kâhinle, statik kol, aynı üç tohum:

| tohum | ETX-kâhin | atlama-kâhin |
|---|---|---|
| 1000 | 0,911 → **1,000** | 0,983 |
| 1001 | 0,602 → **0,999** | 0,987 |
| 1002 | 0,511 → **0,996** | 0,988 |

Oynaklık tamamen kayboldu. Düşük tavan ne alandan ne fizikten kaynaklanıyordu.

🔒 Ve **ölçütün bedeli artık uçtan uca ölçülebiliyor**: mükemmel topoloji
bilgisi ve elenmiş iyi bağ kümesiyle bile atlama sayısıyla yönlendirmek
PDR'den ~1,2 puan, PSR'den 6–9 puan götürüyor (0,745–0,825 ↔ 0,681–0,737).

## İKİ KÂHİN, İKİ AYRI SORU
    ETX-kâhin − atlama-kâhin  = ölçütün bedeli, İYİ BİR BAĞ KÜMESİ VERİLMİŞKEN
    atlama-kâhin − protokol   = körlüğün bedeli (hayalet bağ + bayatlık)

⚠️ `EnKisaYolKahin` **korumalıdır** ve bu beyan edilir: eşiği geçen bağlardan
kurulu grafikte çalışır, yani kötü bağ seçmesi engellenmiştir. Gerçek AODV'nin
böyle bir koruması yoktur. İkinci fark bu yüzden atlama ölçütünün gerçek
dünyadaki asıl bedelini de içerir.

## YENİLEME ARALIĞI TÜRETİLDİ, ELLE YAZILMADI
Elle 0,5 s yazılmıştı ve o sayı **mobilite adımına** bakılarak seçilmişti —
yanlış büyüklük. Bağ kalitesini değiştiren şey gölgeleme hücresinin
değişmesidir:

    dilim = golgeleme_hucre_m / (2 · gm_hiz_maks_ms)

Bugün 0,83 s; hızlar 1/50 ölçeğe çekilince üst sınıra (10 s) oturuyor ve
sönümleme örneklemesinin maliyeti kendiliğinden eriyor.

## 🔴 AÇIK KALAN KUSUR — `mac_carpisma` YANLIŞ ETİKETLİ
Sayaç kayıt defterinde *"eşzamanlı iletim çakışması"* diye tanımlı, ama kod
onu **onay zaman aşımının her sebebinde** artırıyor: gerçek çarpışmada da,
veri çerçevesi PER'den düştüğünde de, onay çerçevesi kaybolduğunda da.
Yani adı bir MEKANİZMA iddia ediyor, kod bir BELİRTİ sayıyor.

⚠️ Pratik sonucu: karıştırma altında bu sayacın artması yanlışlıkla
"tıkanıklık" diye okunabilir. Bu oturumda tam olarak o hataya düşüldü ve
ancak yük taramasıyla ayırt edilebildi.

**Düzeltme seçenekleri:** (a) adı `mac_onaysiz` yapmak — ucuz ve dürüst;
(b) alıcının ret sebebini göndericiye bağlayıp sebebe göre bölmek — bilimsel
olarak daha değerli, katmanlar arası bir bağlantı gerektirir. Karar
verilmedi.

## 🔴 AÇIK KALAN İKİNCİ MADDE — `yeniden_deneme_siniri` GEREKÇESİZ
Değer 4 (yani 5 deneme) ve **hiçbir gerekçesi yazılı değil**; üstelik
"802.11b değerleri" başlığının altında duruyor. 802.11'in kısa çerçeve
sınırı 7'dir ve 512 baytlık çerçevemiz RTS eşiğinin altında olduğu için
geçerli olan odur.

⚠️ Değiştirilmedi. Tavanı yükselteceğini gördükten sonra değiştirmek sonucu
seçmek olurdu; üstelik ölçüldü ve **etkisi yok** çıktı. Doğru sıra: kaynağı
`02-DOGRULANMIS-KAYNAKLAR.md`de doğrulatmak, sonra karar vermek.

---

# K-099 · 🔴 KODUN TAMAMI OKUNDU — ETİKET VE TANIM KUSURLARI

> **Tarih:** 8 Eylül 2026 · **Karar: ajan** · **Durum: UYGULANDI**
> **Bağlam:** Faz 0, adım ①. Şartname `v2/07-SIMULATOR-TASARIMI.md`.

## NEDEN BU OKUMA YAPILDI
Öğrenci, ilerlemeden önce mevcut kodun **tamamının okunmasını, hâkim
olunmasını ve düzeltilmesini** istedi. Gerekçesi kendi ifadesiyle:
*"simülatörün verdiği verilere güvenilemez… daha ben simülatörün nasıl
çalışacağını bile bilmiyorum, hangi kararları verdik."*

🔒 **Genel kanaat: mimari sağlam, kırılgan olan altındaki sayılar ve
birkaç etiket.** Korunum defteri + mutabakat, sayaç kayıt defteri, gözlem
sözleşmesi, hash tabanlı kanal, `Kahin[T]` tip sınırı — bunlar bu alanın
bilinen hata sınıflarına karşı yazılmış gerçek panzehirler. Baştan yazmak
gerekmiyor; refactor yeter.

---

## D1 · `mac_carpisma` BİR MEKANİZMA İDDİA EDİYOR, BİR BELİRTİ SAYIYORDU

Kayıt defterindeki tanımı *"eşzamanlı iletim çakışması"* idi. Kod onu
`_onay_penceresi`de, **onay zaman aşımının HER sebebinde** artırıyordu:
gerçek çarpışmada da, gövde PER'den düştüğünde de, onay çerçevesi
kaybolduğunda da.

⚠️ **Pratik sonucu ölçüldü ve bu oturumda yaşandı:** karıştırma altında
sayacın artışı *"tıkanıklık"* diye okundu ve ancak bir yük taramasıyla
(yük 8 kat düşürüldü, PDR kılını kıpırdatmadı) yanlış olduğu anlaşıldı.

### Karar
İki sayaca bölündü ve ayrım **bedava** — `Dugum.devredildi` zaten paketin
el değiştirip değiştirmediğini biliyor:

| sayaç | anlamı |
|---|---|
| `mac_onaysiz_veri` | onay gelmedi ve veri **ulaşmadı** |
| `mac_onaysiz_onay` | onay gelmedi ama veri **ulaşmıştı** — kaybolan ONAYDI |

### 🔒 VE ÜÇÜNCÜ BİR KORUNUM KAPISI DOĞDU
Kimlik ölçüldü ve **tam** tutuyor:

    mac_deneme = mac_gonderim_basarili + mac_onaysiz_veri + mac_onaysiz_onay

Tuttuğu için kapalı küme (`kume="iletim_sonucu"`) yapıldı ve korunum
bölümüne **üçüncü kapı** olarak bağlandı. Artık bir MAC denemesi hiçbir
kovaya girmeden kaybolamaz — ve bu, korunum denklemini KIRMADAN olabilecek
bir kayıptı.

**Ölçülen yan fayda:** karıştırma altında başarısızlıkların **%1,9'u**
aslında ulaşmış paketler; yalnız onayları kaybolmuş. Eskiden hepsi
"çarpışma" diye okunuyordu.

---

## D2 · İKİ FARKLI PDR TANIMI VARDI VE AYRIŞIYORLARDI

`pdr` sayaç kayıt defterinde bir oran olarak tanımlıydı ve pencere ikizleri
**fark alarak** türetiliyor. Sonuç:

    pdr_pencere = [50,320] arasında TESLİM EDİLEN  /  [50,320] arasında DOĞAN

Pay ile payda **iki ayrı kümeden**. `PaketDefteri` ise doğrusunu yapıyordu:
kohort doğuma göre.

**Ölçüldü** *(statik-surekli, tohum 1000)*:

| karıştırıcı | sayaçlardan | defterden | fark |
|---|---|---|---|
| −25 dBm | 0,9995 | 0,9994 | +0,0001 |
| −20 dBm | 0,9988 | 0,9986 | +0,0002 |
| −15 dBm | 0,9184 | 0,9200 | −0,0016 |

⚠️ **Büyüklük küçük ama YÖNÜ tehlikeli:** gecikmesi uzun bir protokol
pencere kenarından daha çok paket kaçırır ve hem gecikmede hem PDR'de
cezalandırılır. Eşleştirilmiş bir karşılaştırmada bu doğrudan bir
confound'dur — ve karıştırma altında kuyruklar dolunca büyür.

### Karar
`Turev("pdr", ...)` sayaç kayıt defterinden **kaldırıldı**. PDR artık
yalnız `olcum/metrikler.py`de, paket defterinden, kohort **doğuma göre**:
pencerede doğan paket, ne zaman teslim edilirse edilsin sayılır. Boşalma
penceresi tam bunun için var.

🔒 Bir test bunu kilitler: `assert "pdr" not in d` — sayaç oranı olarak geri
gelirse iki tanım yeniden doğar.

---

## D3 · BOŞALMA PENCERESİ 400 KAT FAZLA — *(karar ertelendi)*
Ölçülen en kötü uçtan uca gecikme **71 ms**; boşalma penceresi **30 s**.
Her koşunun %8,5'i boşuna. ⚠️ Küçültülmedi: açılma anı eklenince şok
evresinde kuyruklar dolacak ve gecikme büyüyecek. Tehdit modeli kurulduktan
sonra yeniden ölçülüp karara bağlanacak.

## D4 · YEDİ METRİĞİN ÜÇÜNÜN DİNAMİK ARALIĞI YOK — *(tasarım girdisi)*
Kuyruk hiç taşmıyor, gecikme 7–8 ms'de sabit, IPDV neredeyse sıfır. Şu an
ayırt edebilecek tek şey PDR ve NRL. Açılma anı bunu düzeltir: şok evresinde
kuyruklar dolar ve gecikme anlamlı hâle gelir. **Tehdit modelinin bir
gerekçesi daha.**

## D5 · `adim3_oncesi.py` KENDİ SABİTLERİNİ TUTUYOR — *(sanıldığı gibi kusur değil)*
İlk teşhisim *"ikinci doğru kaynağı"* idi. **Yanlış:** o betik `Konfig` daha
yokken, hangi değerlerin seçileceğine karar vermek için koşulmuş **tarihsel
bir belgedir**. Sabitleri `Konfig`den okutmak, betiğin o günkü ölçümü değil
bugünkü çalışma noktasını ölçmesine yol açardı.

🔒 Ama bayatladıkları da doğru. Çözüm: betik **kendi bayatlığını raporluyor**.
Her koşumda hangi sabitin güncel `Konfig`den ayrıştığını yazıyor — ölçüldü,
üç tane: `EN` 1000↔1800 · `YOL_KAYBI_USTELI` 3,0↔2,0 · `SINR_ESIGI_DB` 10↔16.

## D6 · `yeniden_deneme_siniri = 4` GEREKÇESİZ — *(açık)*
"802.11b değerleri" başlığının altında ama 802.11'in **uzun çerçeve**
sınırıdır; 512 baytlık çerçevemiz RTS eşiğinin altında olduğu için geçerli
olan **kısa çerçeve** sınırıdır. ⚠️ Değiştirilmedi: ölçüldü ve mevcut çalışma
noktasında **etkisi yok** (5→7 deneme, PDR 0,511→0,514). Kaynak `02`de
doğrulanmadan değişmeyecek.

## D7 · `ATLAMA_ESIGI = 0.90` UYDURMA — *(açık, ajanın kendi eklediği)*
Bugün kâhine eklenen eşik. Hiçbir yerden türetilmedi. "Bağ nedir"i
tanımladığı için dereceyi, atlama derinliğini ve alan seçimini belirliyor.
Duyarlılık denetiminde (Faz 1) sınanacak.

## D8 · MOBİLİTEDE KUTU YANSIMASI BİR YAPAYLIK — *(Faz 0 adım ③)*
Gerçek İHA görünmez duvardan sekmez. ⭐ Ama **görev kolu zaten istasyon
tutma kullanıyor** — yani doğru model kodda mevcut, sadece tek bir kolda.
Yeniden yazım sıfırdan değil, **var olanı üç kola genelleme** olacak.

---

## DOĞRULANDI
- Tam test paketi ve mimari denetimi *(D11 içe aktarılabilirlik kapısı dâhil)*.
- Kırılan iki test **`pdr` örneğini kullanan türev makinesi testleriydi**;
  sınadıkları şey `pdr` değil mekanizma olduğu için hayatta kalan bir
  türevle (`psr`) yeniden yazıldı ve iddiaları aynen korundu. Üstüne
  `pdr`nin sayaç oranı olarak geri gelmesini yasaklayan bir iddia eklendi.

## BUNU NE DEĞİŞTİRİR
`sayac_semasi_hash` değişti — bu tarihten önceki sonuç satırları yeni
satırlarla **biçimsel olarak karşılaştırılamaz**. Hepsi kalibrasyon
koşusuydu; deney verisi yok.

---

# K-100 · 🔴 PARAMETRE KÖKEN KAYIT DEFTERİ — BORÇ ARTIK GÖRÜNÜR VE SAYILABİLİR

> **Tarih:** 8 Eylül 2026 · **Karar: ajan** · **Durum: UYGULANDI**
> **Bağlam:** Faz 0, adım ②. Şartname `v2/07-SIMULATOR-TASARIMI.md` §11.

## NE ÖLÇÜLDÜ
Davranış belirleyen **87 sayısal parametre** *(72 `Konfig` alanı + 15 modül
sabiti)* dört kovaya ayrıldı. Sonuç:

| kova | sayı | pay |
|---|---|---|
| TÜRETİLMİŞ | 17 | %20 |
| ÖLÇÜLMÜŞ | 6 | %7 |
| **KAYNAK** | **2** | **%2** |
| TEDAVİ | 6 | %7 |
| **SINANMAMIŞ** | **56** | **%64** |

🔴 **Doğrulanmış dış kaynağa dayanan tek şey Boltzmann sabiti ve ışık hızı.**
802.11b'nin MAC sabitlerinin *(slot · SIFS · CW · önbelge · bit hızları ·
ACK boyu)* hiçbiri `02-DOGRULANMIS-KAYNAKLAR.md`de yok. Bianchi doğrulaması
onları **dolaylı** kısıtlıyor (±%15) ama bibliyografik kaynak yok.

⭐ Ve bu iyi haber: **tek bir doğrulama on parametreyi birden temizler.**

## SORUN NEYDİ
Yorumlar *"bu parametre neden VAR"* sorusunu cevaplıyordu, *"neden BU DEĞER"*
sorusunu değil:

| sayı | yorumun söylediği | söylemediği |
|---|---|---|
| `kuyruk_kapasitesi = 50` | "sonsuz kuyruk yasak" | neden 50 |
| `ttl_baslangic = 32` | "TTL olmadan paket asılı kalır" | neden 32 |
| `rician_k_db = 6` | "Rayleigh değil Rician" | neden 6 dB |
| `beacon_araligi_s = 1` | *(hiçbir şey)* | *(hiçbir şey)* |

Sonucu: her şey belgelenmiş **görünüyordu**, hiçbiri doğrulanamıyordu. Ve
5 Eylül'de bulunan kusurların hepsi bu boşluktan çıktı.

## KARAR — YAPISAL, DİSİPLİN DEĞİL
`sim2/yapilandirma/kokenler.py` tek kayıt defteri. Beş kova, altıncısı yok.
`Konfig`in her alanı orada olmak **zorunda**: eksik alan varsa `konfig.py`
**içe aktarma anında patlar** ve hiçbir koşu başlamaz. Modül sabitleri için
aynı defter, mimari denetiminin **D12** kapısı tarıyor.

🔒 Bu, `cekirdek/sayaclar.py`nin sayaçlar için yaptığının parametreler için
yapılmış hâlidir: tek kaynak, yapısal zorunluluk, ikinci liste imkânsız.

## 🔴 `SINANMAMIS` BİR MAZERET DEĞİL, BİR BORÇ
Bugün 56 parametre orada ve bu **kasten**: duyarlılık denetimi yapılmadan
hiçbir şeye *"duyarsız"*, `02`de doğrulanmadan hiçbir şeye *"kaynak"*
denemez. Kova sistemi borcu ödemez, **görünür ve sayılabilir** kılar.

    🔒 ÖN-KAYIT MÜHÜRLENMEDEN ÖNCE `SINANMAMIS` SAYISI SIFIR OLMALIDIR.

Ve borç **her sonuç satırına yazılıyor** (`teshis.koken_kovalari`): bir koşu
kaç gerekçesiz parametreyle üretildiğini kendisi beyan ediyor.

## ⚠️ TEST, ETİKETİN KENDİSİNİ YAKALADI — SAYI ARTTI
`test_OLCULMUS_kova_URETICI_gostermek_zorunda`, `ÖLÇÜLMÜŞ` diyen ama üretici
betiği yazmayan beş kaydı yakaladı. Bakınca daha kötüsü çıktı: o ölçümler
**eski çalışma noktasında** yapılmıştı.

| parametre | ölçüm gerçek mi | ama |
|---|---|---|
| `irtifa_min_m` · `irtifa_maks_m` | evet | 1000 m alanda, α = 3'te |
| `paket_bayt` · `akis_sayisi` · `akis_paket_hizi_hz` | evet | kanal doluluğu %36,9 → 1000 m, α = 3, 1,8 atlama |

🔴 **Yük, karıştırıcının etkisini belirleyen ana eksenlerden biri.** Alan
1800 m, α = 2 ve yollar 2,2 atlama olunca doluluk değişti ve yeniden
ölçülmedi. Beşi de `SINANMAMIS`a indirildi.

🔒 Yani kova sistemi ilk gününde **borcu 51'den 56'ya çıkardı**. Mekanizmanın
işi tam olarak bu: tabloyu daha kötü ve daha dürüst yapmak.

## ⚠️ BAYATLAMAYA ADAY BİR ETİKET DAHA
`sonumleme_parca_suresi_s` bugün geçerli *(T_c(p99)/4)* ama Θ kalibrasyonu
hızları değiştirdiği anda bayatlayacak — T_c bağıl hızdan türüyor. Kayıtta
uyarısıyla duruyor.

## BUNU NE DEĞİŞTİRİR
- Yeni bir parametre **kökeni yazılmadan** eklenemez; `Konfig` yüklenmez.
- Modül sabiti **kökeni yazılmadan** eklenemez; D12 bulgu üretir.
- Bir ölçüm bayatladığında etiketi indirilir ve borç **artar** — bu bir
  başarısızlık değil, defterin çalıştığının kanıtıdır.
- Faz 1'in duyarlılık denetimi bu 56'yı ikiye ayıracak: sonucu belirleyenler
  *(gerekçelendirilecek)* ve belirlemeyenler *(`DUYARSIZ` olarak beyan
  edilecek)*.

---

# K-101 · 🔴 MOBİLİTE ARTIK m/s İLE DEĞİL, PROTOKOLÜN ZAMANIYLA TANIMLI — VE OLSR YAPISAL OLARAK KIRIKMIŞ

> **Tarih:** 8 Eylül 2026 · **Karar: ajan** · **Durum: UYGULANDI**
> **Üretici:** `python kalibrasyon/calkanti.py`
> **Bağlam:** Faz 0, adım ③. Şartname `v2/07-SIMULATOR-TASARIMI.md` §03.

## NE ÖLÇÜLDÜ
Hızlar `gm_hiz_min/maks_ms = 10–30 m/s` idi ve **hiçbir gerekçesi yoktu**.
Ölçüldü *(6 tohum, 350 s, etkin yarıçap 400 m)*:

| hız (m/s) | bağıl | rota ömrü | **Θ** | 1:50'de km/h |
|---|---|---|---|---|
| **10–30** *(eski)* | 26,4 | **3,2 s** | **0,21** 🔴 | 1 800–5 400 |
| 2–6 | 5,2 | 16,1 s | 1,07 | 360–1 080 |
| 1–3 | 2,7 | 28,6 s | 1,90 | 180–540 |
| 0,5–1,5 | 1,4 | 50,0 s | 3,33 | 90–270 |
| **0,25–0,75** | 0,7 | **89,3 s** | **5,95** | **45–135** ← SEÇİLEN |
| 0,12–0,36 | 0,3 | 155,1 s | 10,34 | 22–65 |

## 🔴 BU BİR STRAW-MAN'DI
OLSR'ın `TOP_HOLD_TIME`ı **15 s**tir (RFC 3626). Rota ömrü 3,2 s iken
topoloji bilgisi, kullanılacağı rotadan **beş kat uzun ömürlü** oluyordu:
OLSR bir rotayı öğrenip kullanamadan o rota çoktan yok oluyordu.

Bu OLSR'ın tasarımının değil **bizim kurulumumuzun** sonucuydu — yani
`03` kural 4'ün yasakladığı şey, kasıtsız hâliyle. Ve hiçbir kapı bunu
yakalamıyordu, çünkü mobilitenin ölçütü yoktu.

## 🔒 ÇALKANTI SAYISI Θ — hedef değil, KAPI
    Θ = ortalama rota ömrü / en yavaş taban çizgisinin topoloji zamanı
      = τ_rota / 15 s          (OLSR TOP_HOLD_TIME, RFC 3626)

    🔒 KAPI: Θ ≥ 3. Altına düşen bir kol, protokolü tasarım zarfının
       DIŞINDA koşturuyor demektir ve bulgu olarak raporlanır, gizlenmez.

Ölçüt doğrulanmamış bir menzil ya da hız sayısına değil, **taban çizgisinin
kendi zaman sabitine** dayanır. Zayıflatılmadığını garanti eden tek şey budur.

## ⚠️ ŞARTNAMEDEKİ HEDEFİM ÇÜRÜDÜ
`07-SIMULATOR-TASARIMI.md` *"çekirdek Θ ≈ 10"* diyordu. **Ulaşılamıyor:**
Θ = 10 için 0,12–0,36 m/s gerekiyor, o da 1:50 ölçekte **22–65 km/h** —
doğrulanmış İHA aralığının (30–400 km/h, A5a) altında.

🔒 Doğru çerçeve Θ'yı hedef değil **kapı** yapmaktı. Kapı + gerçekçilik
birlikte uygulanınca çözüm kendiliğinden çıktı ve iki kol da hem adil hem
gerçekçi oldu:

| kol | hız | Θ | 1:50'de |
|---|---|---|---|
| **çekirdek** | 0,25–0,75 m/s | **5,93** | 45–135 km/h |
| keşifsel, yüksek çalkantı | 0,5–1,5 m/s | 3,33 | 90–270 km/h |
| durgun | 0 | ∞ | — |

## ÖLÇEKLENEMEYEN İKİ BÜYÜKLÜKTEN TÜRETİLEN İKİ PARAMETRE
Bir ölçek modelinde geometri ölçeklenir ama bazı şeyler ölçeklenmez:

| parametre | eski | yeni | türetme |
|---|---|---|---|
| `gm_azimut_sigma_rad` | 0,3 | **0,11** | 🔴 **YERÇEKİMİ ölçeklenmez.** Koordineli dönüş ω = g·tan(φ)/v; GERÇEK hızdan: 90 km/h'de 30° banka → 0,226 rad/s → 0,5 s adımda 0,11 rad. Eski değer saniyede 34°'lik dönüş demekti |
| `gm_alfa` | 0,85 | **0,983** | Hız korelasyon süresi bir ARAÇ DİNAMİĞİ zamanıdır ve ölçeklenmez: ~30 s → α = exp(−0,5/30). Eski değer 3,1 s veriyordu — bir İHA için fazla titrek |

🔒 **Ölçüldü: ikisi de Θ'yı değiştirmiyor** (5,95 → 5,93 · 3,33 → 3,27).
Yani gerçekçiliğe geçmek kalibrasyonu bozmadı.

## `olcek` ARTIK BİRİNCİ SINIF BİR ALAN
Kavanoz–gerçek eşlemesi tek yerde ve **okunuyor** — türetilmiş özellikler
üzerinden, uyuyan bir alan olarak değil:

    1:50 · kutu 90 km · çapa 14 km · irtifa 1–6 km
    hız 45–135 km/h · verici 0,03 dBm → 2,5 W

Değerini **iki kısıt birlikte** belirledi: hızların doğrulanmış İHA
aralığına düşmesi VE türetilen vericinin var olabilmesi. Gösterim katmanı
da *"1 m = 50 m · bu kutu 90 km"* verisini buradan alacak, sonradan
uydurmayacak.

## ⚠️ KIRILAN ÜÇ TEST — ikisi yeni alan, biri EŞİK BAYATLIĞI
`test_gorev_kolu_STATIK_kolun_kopyasi_DEGIL` eşiği **50 bağ olayı** idi ve
Mach-4 hızlarına göre yazılmıştı. Ağ 28 kat yavaş çalkalanınca iddiası hâlâ
doğruyken kırıldı. Yeniden ölçüldü *(7 tohum, 200 s)*:

    statik-yok   :  0,0 kapanan   ← donmuş, tanım gereği
    gorev-yok    : 11,1 kapanan   ← DONMUŞ DEĞİL
    bagimsiz-yok : 14,6 kapanan

Eşik ölçülenin yarısına (5) çekildi ve statik kolun sıfırı ayrı bir iddia
olarak eklendi.

🔒 **"görev < bağımsız" BİLEREK test edilmedi.** `dunya/mobilite.py` bağıl
hızı ve rota ömrünü *"ÖLÇÜT DEĞİL, SONUÇ"* diye ilan ediyor; sonucu kapıya
çevirmek cevabı seçmek olurdu.

## BUNU NE DEĞİŞTİRİR
- **Taban çizgileri artık tasarım zarflarının içinde koşacak.** Bundan önce
  ölçülecek her OLSR sonucu geçersizdi.
- `sonumleme_parca_suresi_s` **bayatladı**: T_c bağıl hızdan türüyor ve bağıl
  hız 26,4 → 0,68 m/s oldu. Köken defterinde uyarısı vardı; yeniden ölçülmeli.
- Θ, mobilitenin **tek** ölçütü. Yeni bir mobilite kolu eklemek isteyen önce
  Θ'sını ölçmek zorunda.
- Köken borcu 56 → **50**: altı parametre `SINANMAMIS`tan çıktı.

---

# K-102 · 🔴 DOPPLER PLATFORM HIZINDAN AYRILDI — VE KENDİ HIZ DEĞİŞİKLİĞİM SESSİZ BİR KUSUR YARATMIŞ

> **Tarih:** 8 Eylül 2026 · **Karar: ajan** · **Durum: UYGULANDI**
> **Bağlam:** Faz 0, adım ③'ün ikinci yarısı. Şartname §02.4.

## 🔴 ÖNCE: KENDİ DEĞİŞİKLİĞİMİN YARATTIĞI KUSUR
K-101 hızları 26,4 → 0,68 m/s'ye indirdi. Sönümlemede `BAGIL_HIZ_TABANI_MS
= 1,0` diye bir taban vardı; sıfıra bölmeye (T_c → ∞) karşı bir korumaydı ve
26 m/s'lik hızlara göre konmuştu.

**Ölçüldü: çiftlerin %84,4'ünün geometrik bağıl hızı tabanın ALTINA indi.**
Yani sönümleme, bağların %84'ünde gerçek hızla değil **uydurma bir 1,0 m/s
ile** hesaplanmaya başlamıştı. Bir koruma, baskın belirleyici hâline gelmişti.

⚠️ Bu kusur bir kod hatasından değil, **bir parametrenin ölçeğinin
değişmesinden** doğdu ve hiçbir test yakalamazdı — çünkü hiçbir test
"tabanın kaç çiftte bağladığını" sormuyordu. Bulunma sebebi, değişikliğin
yan etkilerinin ARANMASIydı.

## ASIL KARAR: DOPPLER TAM ÖLÇEK HIZINDAN
Simülatör 1:50 geometrik bir ölçek modelidir. Mesafeler ve hızlar
ölçeklenir; **2,4 GHz'in dalga boyu ölçeklenemez.**

`f_d = v/λ` olduğuna göre ölçekli hızı kullanmak sönümlemeyi 50 kat
yavaşlatır. Korunması gereken boyutsuz büyüklük *"kanal bir çerçeve
süresince kaç kez değişiyor"*dur ve modülün kendi tasarım hedefi odur.

**Ölçüldü:**

| | v | T_c | çerçeve/T_c |
|---|---|---|---|
| ölçekli hız | 0,64 m/s | 83,1 ms | **0,03** 🔴 |
| **tam ölçek** | **31,8 m/s** | **1,66 ms** | **1,35** ✔ |
| *(tasarım hedefi)* | 25,1 m/s | 2,10 ms | *1,06* |

Ölçekli hız kullanılsaydı kanal çerçeve boyunca **donardı**: yeniden
denemeler aynı derin fade'i görür ve bağ olduğundan **kötü** ölçülürdü.

🔒 Bu bir hile değil, ölçek modellemesinin standart uygulaması: aynı anda
korunamayan iki benzerlikten önemli olan korunur ve **hangisinin feda
edildiği yazılır**. Feda edilen, sönümlemenin MUTLAK zaman ölçeği; korunan,
çerçeveye GÖRE değişim hızı.

⭐ Yan fayda: taban artık Doppler hızına uygulanıyor ve orada hız ~32 m/s
olduğu için bir daha baskın olmuyor — **%84,4 → %0,1**.

## PARÇA SÜRESİ YENİDEN TÜRETİLDİ: 240 → 190 µs
Kural değişmedi *(en hızlı %1'lik bağın T_c'sini dört örnekle çöz)*, T_c
dağılımı değişti:

    yeni ölçüm: T_c ortanca 1,663 ms · p95 0,887 ms · p99 0,764 ms
    dt = T_c(p99)/4 = 191 µs  →  190 µs

Çerçeve başına 11,8 parça (eskiden 9,3). FIR kapsaması 12,2 ms.

### 🔴 YAPISAL YAN ETKİ: PARÇA ARTIK ÖNBELGEDEN KISA
190 µs < 192 µs. Yani **ilk parça tamamen önbelgenin içinde kalıyor** ve hiç
gövde biti taşımıyor; bit taşıyan ilk parça ikincisidir. Kod bunu zaten doğru
yapıyor (`_iz` sıfır örtüşmeli parçayı atlıyor); yanlış olan, testin eski
yapıya göre yazılmış beklentisiydi.

## ⚠️ KIRILAN DÖRT TEST — DÖRDÜ DE AYNI SINIF
Hepsi **türetilmiş bir değeri elle yazmıştı**:

| test | elle yazılmış | artık |
|---|---|---|
| `test_ONBELGE_bit_tasimiyor` | `240e-6` | konfigden + önbelge sınırı hesabı |
| `test_hizli_bag_HIZLI_dekorele_oluyor` | `0,423·λ/v` | `olcek` dâhil, konfigden |
| `test_paket_basina_parca_sayisi_IKIDEN_COK` | `== 10` | `ceil(süre/dt)` |
| `test_HENUZ_OKUNMAYAN_bayatlayamaz` | — | 🔒 **iki yönlü test doğru çalıştı**: `olcek` artık okunuyor, listeden çıkarılmasını ZORLADI |

🔒 Sonuncusu bir kusur değil, **mekanizmanın kendisi**: `olcek`i listeye
koyarken *"Doppler ayrımı yapıldığında bu listeden ÇIKACAK"* diye not
düşmüştüm; ayrımı yaptım, çıkarmayı unuttum, test hatırlattı.

## BUNU NE DEĞİŞTİRİR
- `olcek` artık bir **raporlama parametresi değil**: fiziğe giriyor ve
  `kanal/sonumleme.py` tarafından okunuyor.
- Sönümleme ile mobilite **ayrık büyüklüklerden** besleniyor: geometri
  ölçekli hızdan, Doppler tam ölçek hızından. İkisinin ayrı olduğu
  `tutarlilik_suresi_s`in başlığında beyan edilmiştir.
- Bir parametrenin ölçeği değiştiğinde **koruma amaçlı tabanların** hâlâ
  koruma mı yoksa belirleyici mi olduğu ARANMALIDIR. Bu oturumda bir kez
  yaşandı; başka tabanlar da olabilir *(`FIR_EN_COK_KATSAYI`, capture eşiği,
  `cca_s`)* ve duyarlılık denetiminde sınanacak.

---

# K-103 · 🔴 KARIŞTIRICI GÜCÜ ÖLÇÜLDÜ — VE "SINIFLARI AYNI ETKİDE EŞİTLE" DEDİĞİM ŞEY DÖNGÜSELMİŞ

> **Tarih:** 8 Eylül 2026 · **Karar: ajan** · **Durum: UYGULANDI**
> **Üretici:** `python kalibrasyon/karistirici_gucu.py`
> **Bağlam:** Faz 0, adım ④. Şartname §05 (tehdit modeli).

## ÇALIŞMA NOKTASI: −15,0 dBm · ρ = 0,258
Ölçüt K-099'da ilan edildi ve **referans sınıfta** (`surekli`) koştu: 30
tohumun hiçbirinde birden fazla çok üyeli bileşen yokken ρ en büyük.
`senaryolar.KARISTIRICI_GUCU_DBM` beş sınıfta da bu tabanı taşır.

## 🔴 İLK BEYANIM YANLIŞTI: "SINIFLAR AYNI ETKİDE EŞİTLENMELİ"
Kalibrasyon başlığına böyle yazmıştım. Yanlış — ve yanlışlığı ilkeseldir:
**ρ bir ETKİDİR, yani bağımlı değişken.** Her sınıfa aynı ρ'yu verdirmek,
deneyin aramaya çıktığı mekanizma farkını kalibrasyonla **silmek** olurdu.

🔒 Doğru ilke: eşitleme karıştırıcının **HARCADIĞI** şey üzerinden yapılır
(yayılan ortalama güç — bir girdi), **BAŞARDIĞI** şey üzerinden değil.
`karistirici.py` bunu zaten böyle yapıyormuş; şartnamem koddan sapmıştı.

## PLANIMI BİR KAPI DURDURDU — VE HAKLIYDI
Her sınıfa `karistirici_guc_override_dbm` ile güç vermeyi deneyince `Konfig`
reddetti: *"override nihai güçtür, tepe telafisi uygulanmaz ve 'aynı ortalama
güç' koşulu kırılır."* Yani darbeli sınıfı override ile kalibre etmek yapısal
olarak mümkün değil. Kapı, az önce yazdığım ilkeyi bana zorladı.

## ⚠️ ρ HER SINIFTA OKUNAMIYOR — önce kod okundu, sonra ölçüldü
| sınıf | açık | ort_dBm | ρ | AYRILAN |
|---|---|---|---|---|
| `surekli` | 1,000 | −15,0 | 0,258 | 0/30 |
| `surekli_darbeli` | 0,499 | −15,0 | 0,169 | **1/30** 🔴 |
| `reaktif` | **0,000** | −∞ | **0,000** | 0/30 |
| `aldatici` | 0,978 | −15,1 | 0,258 | 0/30 |
| `taramali` | 0,325 | −19,9 | 0,081 | 0/30 |

🔒 Tepe telafisi **ölçülerek doğrulandı**: darbelinin yayılan ortalaması tam
−15,00 dBm'e oturuyor.

🔴 `reaktif` ρ = 0 bir kusur değil **tanımdır**: trafiksiz bir grafik probunda
patlayacağı iletim yoktur. Şiddeti ancak Faz 2'de, protokol koşarken ölçülür.

⭐ `aldatici` ile `surekli` kanal grafiğinde **tıpatıp aynı**. Bu, tehdit
modelindeki en temiz kontrast: bağ hasarı sabit, tek fark CSMA görünürlüğü —
yani ikisinin farkı **saf kanal-erişim etkisidir**.

## 🔴 DARBELİ KOL SERT KISITI 1/30 TOHUMDA ÇİĞNEDİ
Eşit ORTALAMA güç eşit TEPE güç değildir: darbeli tepesini +3,01 dB
yükseltir ve açıkken **0,380** bağ yok eder (sürekli 0,258).

Ölçütü sonuca göre eğmedim; **zaman anlamını netleştirdim** ve iki ölçüm
bunu iddia olmaktan çıkardı:
1. Temiz grafik **30/30 tohumda tek parça** → kapanınca bütünleşme garanti.
2. Ayrılan tek tohum (1028) ve dört örneğinin dördü de **açık evrede**.

Yani ayrılma süresi yapısal olarak **≤ 1,35 s**. AODV'nin
`ACTIVE_ROUTE_TIMEOUT`u **3 s** (RFC 3561); ayrılma ondan kısa olduğu için
hiçbir protokol KARARLI bölünmüş topoloji görmez — gördüğü bir bağ arızası
salvosudur.

🔒 Netleşmiş kısıt (sıfır serbest parametre, çıpası RFC 3561): *hiçbir kolda
bölünmüş topoloji, en hızlı taban çizgisinin rota geçersizleme süresinden
uzun sürmeyecek.* Sürekli sınıf için bu eskisiyle **aynı** şeydir; fark
yalnız zamanla değişen sınıflarda doğuyor — eski hâli onlar için hiç
tanımlanmamıştı.

⚠️ **Ne zaman yazıldığı kayda geçer:** 1/30 sonucu görüldükten SONRA. Yapıdan
önce de sorulabilirdi; dört sınıfın zaman yapısı olduğunu kod okumasıyla
zaten saptamıştım, *"karıştırıcı kapanıyorsa 'ayrılma yok' ne demek"*
sorusunu o an sormayı atladım.

> ## 🟢 8 EYLÜL 2026 DENETİMİ — ÇIKARIM KANITA DÖNDÜ
> *Üretici: `python kalibrasyon/denetim_ornekleme.py d g`*
>
> Yukarıdaki (2) numaralı dayanak bir **çıkarımdı**, kanıt değil: dört örnek
> bölünmenin açık evreyle *çakıştığını* gösterir, kapanınca *bittiğini*
> değil. 1,35 s sınırı ancak kapalı evrede ağın bütün olduğu gösterilirse
> geçerlidir. Denetimde bu ölçüldü:
>
> | ne sınandı | sonuç |
> |---|---|
> | darbeli kapalı evre grafiği ≡ `statik-yok` grafiği | **270/270** (30 tohum × 9 kapalı an) |
> | darbeli kapalı evrede tek parça | **270/270** |
> | temiz grafik dokuz anın hepsinde tek parça | **270/270** *(eskiden yalnız t = 200,0'da bakılmıştı)* |
>
> 🔒 Yani `acik_mi` yanlışken kanal, karıştırıcısız kanalın **birebir
> aynısıdır** — bölünme yapısal olarak açık evreyle sınırlıdır ve süresi
> ≤ 1,35 s'dir. **K-103'ün bu alt kararı ayakta ve artık kanıta dayanıyor.**
>
> ⚠️ Netleştirmenin sonucu gördükten sonra yazıldığı gerçeği DEĞİŞMEDİ ve
> silinmez. Değişen tek şey, gerekçenin artık dört örneğe değil bir yapısal
> özdeşliğe dayanmasıdır.

🔴 Yanlışlama koşulu: darbe süresi 3 s'yi aşarsa gerekçe çöker ve taban gücü
düşürülür. Duyarlılık denetiminde sınanacak.

## ⚠️ ÇAPRAZ KONTROL BEKLENTİYİ TUTMADI — ve iki şeyi karıştırdığımı gösterdi
Beklenti: *"ilk şokta %50 altı, mesh tepki verince %70–80."* Ölçülen kâhin
tavanı karıştırma altında **0,959**.

> 🔴 **8 EYLÜL 2026 DENETİMİ — BU SAYI GEÇİCİDİR.** Yalnız **3 tohumla**
> ölçüldü ve tohumlar arası yayılım büyük: 0,989 · 0,994 · **0,894**. Kural 8
> sonuç için ≥30 tohum istiyor; dolayısıyla 0,959 bir **çapraz kontroldür**,
> sonuç satırına giremez ve tek başına okunamaz.
>
> Ayrıca denetimde ortaya çıktı ki bu sayının **üreticisi yoktu** — kural 7
> çiğnenmişti: `pdr_tavani.py` üç bölümünde de yalnız `-yok` kolunu koşuyor,
> yani karıştırılmış tavanı üreten hiçbir betik depoda yoktu. Üretici eklendi:
> `python kalibrasyon/pdr_tavani.py 4` (3 tohum) · `4x30` (sonuç için).

Bağların dörtte birini yok etmek mükemmel yönlendirmeyle yalnız 4 puana mal
oluyor — ağın yedekliliği yetiyor. 🔒 Çelişki değil: %70–80 bir
**PROTOKOLÜN** performansını tarif ediyor, ulaşılabilir tavanı değil. Tavan
0,96 iken protokol 0,75'e ulaşıyorsa aradaki fark **protokolün körlüğüdür** —
ölçmek istediğimiz şey odur.

🔴 Ölçülmüş gerginlik: tavanı %70–80'e indirmek ~−9 dBm gerektirir, orada 30
tohumun **9'unda ağ ayrılıyor**. *"Tavan %70–80"* ile *"ağ bölünmesin"*
**aynı anda sağlanamaz**; sert kısıt bağlantılılık olduğu için tavan yüksek
kalır ve fark protokollerden gelir.

## İKİ SESSİZ KUSUR DAHA BULUNDU
- **Sınıf adı ayrışması:** kalibrasyon betiği `darbeli` yazıyordu, tablo
  `surekli_darbeli`. Yalnız `surekli` koştuğum için hiç ateşlenmemiş; sıra o
  sınıfa gelseydi `KeyError`. Liste artık **kaynağından türetiliyor**.
- **Örtüşme (aliasing):** üç sabit an (200/260/310) darbeliyi %50 yerine %67
  açık yakalıyordu. Anlar 15,6 s aralıklı seçildi; 15,6 mod 2,7 = 2,1 = 7×0,3
  ve gcd(7,9)=1 olduğu için dokuz an darbe fazını **düzgün** örtüyor. Ölçüt
  değil, ölçüm aracı düzeltildi.

## KÖKEN DEFTERİ: 50 → 46
Dört karıştırıcı sabiti `TEDAVI`ye taşındı *(`darbe_periyodu_s`,
`darbe_gorev_cevrimi`, `taramali_konak_suresi_s`, `taramali_konak_sayisi`)*:
bunlar bir donanımın fiziğini iddia etmiyor, **kolun tanımı**. 🔴 Borç
silinmedi, **yer değiştirdi** — TEDAVİ değişkenleri ön-kayıtta ilan edilir ve
duyarlılık denetiminde oynatılır.

İkisi `SINANMAMIS` **kaldı** *(`reaktif_sezme_s`, `reaktif_patlama_s`)*:
bunlar kol tanımı değil, bir alıcının zamanlamasını iddia ediyor ve
karıştırıcının çerçeve gövdesine değip değmediğini belirliyor. Kaynak gerekir.

🔒 `darbe_periyodu_s`in rezonans yasağı **ölçüldü**: beacon 1,0 s'ye oran 2,7
(10 ayrı faz), trafik 0,25 s'ye oran 10,8 (54 ayrı faz). Darbe hiçbir
periyodik olaya kilitlenmiyor.

## ⚠️ ÖN-KAYITLI İKİ TAHMİN
1. **`taramali` gereksiz olabilir:** 100 ms konak, en hızlı protokol
   zamanlayıcısından (AODV 1 s) 10 kat hızlı. Protokoller onu *seyreltilmiş
   sürekli* karıştırıcı gibi görürse sınıf yeni bir soru sormuyordur.
2. **`taramali` şiddet farkı taşıyor:** ortalaması −4,77 dB düşük. *"Taramalı
   zayıf çıktı"* bulgusu mekanizmaya tek başına yazılamaz.

## 🔴 EK BULGU: KENDİ DEĞİŞİKLİĞİM DOKUZ TESTİ BOZDU — VE İKİSİ *YEŞİL* KALARAK

Güç tablosu dolunca test takımı koşuldu: **7 kırık**. Ama asıl bulgu kırılan
yedi değil, kırılmayan ikisiydi.

Sebep tek: daha önce eklediğim `karistirici_baslangic_s = 150,0`. Karıştırıcı
artık t = 150 s'de devreye giriyor; oysa karıştırıcı testleri **t ≈ 0'da**
ölçüyordu, yani karıştırıcı tamamen kapalıyken.

| test | oldu |
|---|---|
| `PERi_YUKSELTIYOR[surekli/aldatici/taramali]` | kırıldı — doğru davranış |
| `aldatici_TASIYICI_DINLEMEYI_mesgul_ediyor` | kırıldı — doğru davranış |
| `PERi_YUKSELTIYOR[reaktif]` | 🔴 **GEÇTİ** — kayan nokta gürültüsüyle |
| `surekli_TASIYICI_DINLEMEYI_mesgul_ETMIYOR` | 🔴 **GEÇTİ** — boş yere |

### İkisi neden tehlikeli
**Reaktif kolu** `kirli > taban` diye bakıyordu. Ölçüldü:

    taban  1,0760491354011618e-64
    kirli  1,0760491354011621e-64
    fark   3,37e-80        bağıl fark  3,1e-16   ← bir ULP

Yani *"reaktif karıştırıcı PER'i yükseltiyor"* iddiası, karıştırıcı KAPALIYKEN
bir double'ın son bitiyle doğrulanıyordu. Eşik artık `1e-6` mutlak artış —
gerçek kirli PER 1,0'a çıktığı için fazlasıyla gevşek, ama ULP'yi eliyor.

**Sürekli CSMA kolu** *"gürültü karıştırıcısı kanalı meşgul göstermez"*
diyordu ve kapalı bir karıştırıcıyı doğruluyordu. Bir testin geçmesi, doğru
sebeple geçtiği anlamına gelmiyor — ve olumsuz iddialar (`not any(...)`) bu
kusura yapısal olarak açık.

### Üç yapısal düzeltme
1. Ölçüm anı artık `_devrede_an(konfig)` ile **konfigden türüyor**; elle
   yazılmış `10.0` aynı çürümeyi tekrar üretirdi.
2. Her karıştırıcı testine **ön koşul** eklendi: `devrede_mi(bas)` doğru mu.
   Kapalı bir karıştırıcıyı ölçüp geçmek artık mümkün değil.
3. 🔒 Kapının **kendisi** test edildi (`test_karistirici_BASLANGICTAN_ONCE_
   susuyor`): öncesinde `alinan_guc_w == 0`, sonrasında `> 0`. Kapı
   eklendiğinde bu test yazılsaydı, etkisi başka testlerin içinde sessizce
   keşfedilmezdi.

⚠️ `test_adim3_te_okunan_alanlar_GERCEKTEN_dunyayi_kuruyor` de kırıldı ve
haklıydı: `karistirici_baslangic_s`i ekleyip "hangi alan okunuyor" defterine
yazmamıştım.

🔒 **Genel ders:** yeni bir KAPI eklemek, o kapıdan geçen bütün testleri
sessizce boşaltabilir. Kapı eklendiğinde sorulacak soru *"ne kırıldı"* değil,
**"ne hâlâ geçiyor ama artık hiçbir şey doğrulamıyor"**dur.

## BUNU NE DEĞİŞTİRİR
- Karıştırıcı kolları artık **koşulabilir**: güç tablosu doldu, `override`
  zorunluluğu kalktı. Kapı kalkmadı — yeni bir sınıf `None` kalırsa yine durur.
- Tehdit modelinde **eşleştirilmiş bir kontrast** var (`surekli` ↔ `aldatici`)
  ve ön-kayıtta hipotez olarak yazılacak.
- ρ artık bir **hedef değil rapor alanı**: her kolun sonuç satırında yazılır.

# K-104 · 🔴 SON OTURUMUN DENETİMİ — DÖRT ŞÜPHE DÜŞTÜ, ÜÇ GERÇEK KUSUR ÇIKTI

> **Tarih:** 8 Eylül 2026 · **Karar: ajan** · **Durum: UYGULANDI**
> **Bağlam:** Faz 0, adım ④ sonrası denetim. `DEVIR.md` §3'ün dokuz maddesi.
> **Üreticiler:** `python kalibrasyon/denetim_ornekleme.py` ·
> `python kalibrasyon/karistirici_gucu.py tarama` ·
> `python kalibrasyon/adim4_kapanis.py` · `python kalibrasyon/adim9_kapanis.py`

## NE YAPILDI
Bir önceki oturum kendi zayıf noktalarını dokuz madde hâlinde düşmüştü.
Hepsi **ölçülerek** sınandı. Sonuç ikiye ayrıldı: şüphelerin çoğu düştü, ama
şüphe edilmeyen bir yerde üç gerçek kusur çıktı.

## 🟢 DÜŞEN ŞÜPHELER — ve neden düştükleri ÖNEMLİ

### Statik kolda kanal grafiği ZAMANDAN BAĞIMSIZ — ölçüldü
`statik-yok`, `statik-surekli` ve `statik-aldatici` için dokuz örnek anının
**kenar kümeleri birebir aynı** (30/30 tohum, en küçük Jaccard **1,0000**).
Sebebi yapısal ve üç yerden geliyor: sönümleme statik kolda dondurulmuş
(`_donuk` → k = 0, M = 1), karıştırıcı gücü yalnız **yavaş** kayıptan
geçiyor, ve `Surekli.acik_mi` her t'de doğru.

Bundan üç sonuç birden çıkıyor:
- **ρ taraması yeniden koşuldu ve aynı sonucu verdi: −15,0 dBm · ρ = 0,258.**
  Çalışma noktası ayakta; K-103'ün alt kararlarına dokunulmadı.
- **ρ'nun paydasındaki "asimetri" YOK.** Temiz dereceyi bir yerine dokuz
  anda örneklemek ρ'yu **0,00e+00** değiştiriyor (beş sınıfın beşinde de).
- Önceki oturumun *"`surekli` zamanla değişmez"* gerekçesi **doğruymuş** —
  ama o zaman bir iddiaydı, şimdi ölçüm.

### `aldatici` ↔ `surekli` aynılığı TESADÜF DEĞİL — ama tam da değil
`aldatici` dokuz örnek anının **9/9'unda açık**, ve iki kolun kenar kümeleri
**270/270** noktada aynı. Yani "eşleştirilmiş kontrast" yorumu doğru.

⚠️ **Ama çerçeve düzeyinde bir artık var ve şimdiye kadar ölçülmemişti.**
Aldatıcı zamanın %2,2'sinde (DIFS boşlukları) kapalı ve `alim_per` çerçeveyi
parça parça integre ediyor. Ara PER bandındaki 61 bağda: fark ortalama
**+0,0039**, en büyük **+0,0080** — işareti beklendiği gibi pozitif. İki
kolun farkı **saf CSMA değil, CSMA + bu artık**. Ön-kayıta böyle girer.

### Darbeli kolun 1,35 s sınırı: ÇIKARIM ARTIK KANIT
K-103 bunu dört örneğe dayandırıyordu. Ölçüldü: darbelinin **kapalı evre
grafiği**, `statik-yok` grafiğinin **270/270** noktada birebir aynısı ve
270/270 tek parça. Yani kapalı evrede ağ yapısal olarak bütün; bölünme açık
evreyle sınırlı, süresi ≤ 1,35 s < AODV'nin 3 s'si. **Alt karar ayakta.**

⚠️ Netleştirmenin sonucu gördükten sonra yazıldığı gerçeği silinmiyor.
Değişen tek şey, gerekçenin dört örneğe değil bir özdeşliğe dayanması.

## 🔴 ÜÇ GERÇEK KUSUR — hiçbiri şüphelenilen yerde değildi

### 1. Üç kalibrasyon tablosu KAPALI bir karıştırıcı ölçüyordu
`karistirici_baslangic_s = 150 s` kapısı `tests2/` içinde denetlenmişti;
**`kalibrasyon/` taranmamıştı.** Ölçüldü:

| yer | ne yapıyordu | kanıt |
|---|---|---|
| `adim4_kapanis.py` B | `bas_s = 10,0` — dört sınıfın dördü de **PER 0,0000** *(temiz tabanla aynı)*, `gorev cevrimi` sütunu ise canlı görünüyordu | aynı kurulum t = 160 s'de **PER 1,0000** |
| `adim9_kapanis.py` 2 | `bagimsiz-reaktif` satırı `bitis = 10 s` — **iletim sayısı `bagimsiz-yok` ile birebir aynı (6051)** | düzeltince 5958 |
| `adim9_kapanis.py` 3 | dokuz satırın dokuzu da `bitis = 10 s` — **üç sınıf × üç güç (0/10/20 dBm) hepsi birebir aynı: 4014 deneme · 59 teslim · PDR 0,184** | 20 dB güç farkı hiçbir şeyi değiştirmiyordu |

🔒 **`acik_mi` sütunu tabloyu canlı gösteriyordu** çünkü o SINIF zamanlamasını
söyler, `devrede_mi` kapısını değil. Bu, `DEVIR` §10'daki *"ne hâlâ geçiyor
ama artık hiçbir şey doğrulamıyor"* uyarısının tam örneğidir.

**Düzeltme yapısal:** örnekleme anı artık konfigden türüyor ve iki betikte de
bir **kapı** var — karıştırıcı devreye girmeden biten bir koşu istenirse
`dogrula` patlıyor.

### 2. `adim9_kapanis.py` bölüm 3, ÇÜRÜTÜLMÜŞ bir ölçütü ilan ediyordu
Bölümün başlığı *"karıştırıcı gücü kalibre edilmedi"* diyor ve ölçüt olarak
*"teslim oranını dinamik aralığın ortasına getiren güç; kısıt ulaşılabilirlik
≥ %90"* ilan ediyordu. O ölçüt K-103'te **açıkça çürütüldü** ve yerine
*"birden fazla çok üyeli bileşen yokken ρ en büyük"* geldi. Yani depoda aynı
sayı için **iki ayrı ölçüt** duruyordu ve biri koşulabilir hâldeydi.

🔒 Bölüm silinmedi, **gerçek bir kapıya çevrildi**: *"korunum defteri
karıştırıcı devredeyken de kapanıyor mu?"* Bu boşluk gerçekti — bölüm 1'in
altı koşusunun altısı da `statik-yok`. Ölçüldü, beş sınıfın beşinde de
**korunum + mutabakat TAMAM**.

### 3. `pdr_tavani.py` ölü bir varsayılan taşıyordu — ve bir sayının üreticisi YOKTU
`ek.setdefault("karistirici_guc_override_dbm", 0.0)` hiç ateşlenmiyordu
(üç bölüm de yalnız `-yok` koşuyor). Ateşlenseydi kalibre edilmiş −15,0 dBm'i
**15 dB ezerdi** — taramada −6 dBm'in bile 30 tohumun 19'unda ağı ayırdığı
bir yerde. Kaldırıldı.

🔴 Ve asıl mesele: *"karıştırma altında tavan 0,959"* sayısının **üreticisi
yoktu**. Üç belgede kesin bir sayı gibi duruyordu ama onu üreten hiçbir betik
depoda yoktu — kural 7 çiğnenmişti. Üretici eklendi (`pdr_tavani.py` bölüm 4,
ölçüm penceresi tamamen karıştırılmış evrede) ve sayı geçtiği yerlerde
**"3 tohum, geçici"** diye işaretlendi *(tohumlar arası yayılım
0,989 · 0,994 · 0,894)*.

🔒 Yeni üretici eski sayıyı **doğruladı**: tohum 1000'de temiz 1,000 →
karıştırılmış **0,988** (eski kayıtta 0,989). Kurulum eşleşiyor; yani
0,959'luk ortalama tek bir aykırı tohumun (0,894) eseri. Sorun sayının
kendisi değil, **yayılımı** — ve 3 tohum onu göstermeye yetmiyor.

## ⚠️ İKİ AÇIK YARGI

### Dört sabitin `TEDAVI`ye taşınması AKLANMADI
Depoda **iki ayrı "tedavi" tanımı** var ve biri yapısal olarak zorlanıyor:
`sonuc.py::TEDAVI_ALANLARI = ("kol", "senaryo", "tohum", "not_")` — iki kolun
meşru olarak ayrılabileceği alanlar; `kurulum_hash` bunları dışarıda bırakır.
`darbe_periyodu_s` ve arkadaşları bu listede **yok**, yani `kurulum_hash`in
İÇİNDE: onlarda ayrışan iki koşu, aletin kendi kuralına göre *"aynı deneyin
iki kolu değildir"*. Ayrıca ölçüldü — dördü de deneyde **hiç oynatılmıyor**,
yalnız birim testlerinde.

🔒 Yani bunlar tedavi *değişkeni* değil, bir tedavi *seviyesinin tanımıdır*.
Etiket savunulabilir ama **adı yanlış** ve borç sayacı o yanlış adla 50 → 46
düştü.

**Önerilen çözüm (onay bekliyor — `sim2/` değişikliği):**
1. Kovanın adı `TEDAVI` → **`KOL_TANIMI`**. Bu, `TEDAVI_ALANLARI` ile
   karışmaz ve iddiası doğrudur: bu sayılar bir karıştırıcı sınıfının NE
   OLDUĞUNU tanımlar.
2. Şartnamenin istediği ama kodda **hiç olmayan** `DUYARSIZ` kovası eklenir —
   Faz 1 duyarlılık denetiminin çıktısının yazılacak yeri bugün yok.
3. Borç düzyazıda değil **sayaçta** durur: `KOL_TANIMI`ndaki her parametre,
   duyarlılık denetimi onu `DUYARSIZ`a ya da `OLCULMUS`a taşıyana kadar bir
   `DUYARLILIK_BORCU` listesinde kalır ve D12 onu `SINANMAMIS` gibi **sayar**.
   Ön-kayıt mührü iki sayacın da sıfır olmasını ister.

### Şartname–kod ayrışması tarandı: 12 satır, 3'ü temiz
§05.6 tek bir ayrışmayı yazmıştı ama yalnız o bölüm için aranmıştı. Belgenin
bütünü tarandı ve `07-SIMULATOR-TASARIMI.md` §17'ye **ayrışma defteri**
olarak yazıldı. En ağır üçü: kova sisteminin şartnamedeki dört kovaya
uymaması (`DUYARSIZ` kodda yok, `TEDAVI`/`SINANMAMIS` şartnamede yok),
mobilite yeniden yazımının yapılmamış olmasına rağmen adım ③'ün 🟢 görünmesi
*(duvar yansıması hâlâ canlı, istasyon tutma yok)*, ve çekirdek Θ'nın belgede
hâlâ ≈ 10 yazması *(K-101 onu ulaşılamaz bulup 5,93'e indirdi)*.

⚠️ Tarama **tek yönlü**: belgeden koda. *"Kodda olup belgede anılmayan"*
tarama yapılmadı ve §17.1'de öyle yazıyor.

## ⭐ BONUS: BİR KUSUR HİPOTEZİ KURULDU VE ÇÜRÜTÜLDÜ
Karıştırıcısız kâhin tavanı hareketli kolda **0,831–0,917** çıkıyor, statik
kolda 0,996–1,000. Şüphe: K-101 hızları düşürünce `dilim_suresi_s`in
türetilmiş değeri 33,3 s'ye çıkıp **10 s'lik kelepçeye** dayandı — belki
tavan ağın değil **kâhinin** sınırıydı. Ölçüldü *(aynı tohum, aynı pencere)*:

| kâhin grafiği tazeleme | PDR |
|---|---|
| `dilim_s = 10,0` (kelepçeli varsayılan) | 0,831 |
| `dilim_s = 1,0` (on kat sık) | **0,834** |

Fark 0,003. **Şüphe düştü**, kayıp gerçek (677 iletim başarısızlığı /
4 078 paket). Ama iki şey kayda geçer: kelepçe artık **bağlayıcı** ve değer
türetilmiyor; ve şartnamenin §09.5'te ilan ettiği *"0,996–1,000"* aralığı
**yalnız statik kolun** sayısıdır — çekirdek deney hareketli kolda koşacak ve
orada karıştırıcısız kolda bile **17 puanlık** bir ayrışma alanı var.

## BUNU NE DEĞİŞTİRİR
- Çalışma noktası (−15,0 dBm · ρ = 0,258) **ölçülerek doğrulandı**; K-103 ve
  bütün alt kararları ayakta.
- Üç kalibrasyon tablosu artık gerçekten ölçüyor; ikisinde **kapı** var.
- Korunum defteri ilk kez **karıştırılmış kolda** kapandı (5 sınıf, TAMAM).
- Bir test eşiği (`1e-6`) **ölçülmüş bir brakete** dönüştü: temiz PER
  1,076e−64 ↔ kirli 1,000000, yani 64 mertebe ayrım; artık fark değil
  **mutlak değer** sınanıyor ve bir ULP bunu geçemez.
- Şartname ile kod arasındaki 12 ayrışma tek yerde ve sayılabilir.
- 451 test geçiyor · `Yapisal ihlal YOK` · köken borcu **46**.

---

# K-105 · 🟢 ADIM ⑤ KAPANDI — VE İKİ ÖLÇÜTÜMÜ KENDİ KAPILARIM ÇÜRÜTTÜ

> **Tarih:** 8 Eylül 2026 · **Karar: ajan** (öğrenci onayı: *"mantıklı
> gördüğünü yap"*) · **Durum: UYGULANDI**
> **Bağlam:** Faz 0, adım ⑤. Tasarım `v2/08-EVRE-METRIKLERI.md`.
> **Üreticiler:** `python -u kalibrasyon/evre_metrikleri_kapilari.py` ·
> `python -m pytest tests2 -q` · `python kalibrasyon/mimari_denetimi.py`

## NE YAPILDI
Dört evre metriği (şok derinliği · toparlanma tamlığı · toparlanma süresi ·
tespit gecikmesi) **sıfır serbest parametreyle** tanımlandı, uygulandı ve
**kendi doğrulama kapılarından geçirildi**. Ayrıca K-104'ün açık bıraktığı
köken defteri sorunu yapısal olarak kapatıldı.

🔒 Metrikler **son işlemdir**: paket defteri zaten doğum/teslim anlarını,
rota defteri zaten beyanları zaman damgasıyla tutuyordu. Sıcak yolda hiçbir
değişiklik, hiçbir yeni sayaç yok — bu bir tercih değil kısıt, çünkü ölçümün
maliyeti sonuca karışmamalı.

## 🔒 ÖLÇÜM KAFESİ — iki sabit, ikisi de dışarıdan
    ızgara adımı  S = 1 s   RFC 3561 · AODV HELLO_INTERVAL   → ÇÖZÜNÜRLÜK
    pencere       L = 15 s  RFC 3626 · OLSR TOP_HOLD_TIME    → DURAĞANLIK

Evreler: `TEMİZ [50;150)` · `ŞOK [150;165)` · `TOPARLANMA [165;320)`.
Bölümleme tam, boşluk yok.

Şartnamedeki serbest parametre — *"PDR'nin temiz değerinin **%X**'ine
dönmesi"* — **öldürüldü**. Yerine geçen band, koşunun KENDİ paket
sayımlarından hesaplanıyor; seçilecek bir yüzde yok.

## 🔴 ÜÇ ÖLÇÜT HATASI — üçünü de kendi yazdığım kapılar buldu

### 1. Şok penceresinin gerekçesi yanlıştı (yapıdan önce)
İlk hâli `[T_j; T_j+3)` idi: *"3 s = AODV ACTIVE_ROUTE_TIMEOUT, en hızlı
taban çizgisi bile bundan önce tepki veremez."* **Yanlış.** O sabit bir
rotanın KULLANILMADIĞI için geçersizleşme süresidir; bağ arızası tespiti
değildir — AODV, MAC yeniden deneme sınırı dolar dolmaz RERR üretir,
**milisaniyeler** mertebesinde.

🔒 Sonucu tasarımı değiştirdi: *"hiçbir protokolün tepki veremeyeceği
pencere"* diye bir şey **yoktur**, dolayısıyla şok derinliğini toparlanma
hızından bir zaman penceresiyle ayırmak **imkânsızdır**. Doğru yol ayırmaya
çalışmak değil, **ne ölçüldüğünü yazmaktır**: şok derinliği ikisini birlikte
ölçer ve hızlı toparlanan bir protokolün çukuru gerçekten daha sığdır.

### 2. Hata payı kestiricisi sınırda ÇÖKÜYORDU — G1 bunu yakaladı
G1 ilk koşuda kaldı: tohum 1002'de şok derinliği −0,00375, band 2 SE =
**0,00193**. Sebep Wald: `SE² = p(1−p)/n`, ve `p = 1`'de **tam olarak
sıfır**.

🔴 Bu projede `p = 1` istisna değil **kural**: karıştırıcısız kolda kâhin
PDR'si 1,000 ölçülüyor — §10/4 gerçekçilik kapısının talebi tam olarak bu.
Yani hata payı, en çok gerekli olduğu yerde çöküyordu. Ve yalnız kapıyı
değil, **`toparlanma_suresi`nin bandını da** bozuyordu: sıfır genişlikte bir
band hiçbir zaman sağlanmaz.

🔒 Düzeltme **Agresti–Caffo** — iki oranın FARKI için belgelenmiş standart,
sınırda çökmez, serbest parametre getirmez. Düzeltmeden sonra tohum 1002 tek
başına da geçiyor (0,00375 < 0,00387).

⚠️ İkinci düzeltme istatistikseldir: verdikt **kol ortalamasında** verilir.
Tohum başına bir 2 SE testi tanım gereği tohumların ~%5'inde kalır; üç
tohumda en az birinin kalma olasılığı ~%14. Yani tohum başına bir kapı,
DOĞRU bir metriği rastgele reddeder.

### 3. G2'nin ölçütü SINANAMAZ bir şey istiyordu
İlk hâli *"güç arttıkça şok derinliği monoton artmalı"*. Ölçüldü:

| güç (dBm) | şok derinliği (3 tohum ort) | SE | karar |
|---|---|---|---|
| −30 | −0,00069 | 0,00117 | — |
| −21 | −0,00125 | 0,00107 | fark YOK (gürültü) |
| −15 | **+0,03707** | 0,00375 | artış |
| −9 | **+0,18742** | 0,00891 | artış |

İlk iki noktanın **gerçek değeri de sıfır** (o güçlerde kâhin hiçbir şey
kaybetmiyor) ve aradaki fark 0,00056 — birleşik 2 SE'nin çok içinde. Gerçek
değeri eşit iki noktada gürültü ~%50 olasılıkla düşüş gösterir, yani DOĞRU
bir metrik yarı yarıya kalırdı.

🔒 Düzeltilen şey **eşik değil TANIM**: *"artış"* bir ölçümdür ve ölçülen her
şey hata payıyla okunur. Yeni ölçütün de sıfır serbest parametresi var —
band verinin kendisinden geliyor. *(Aynı sınıf hata: "ulaşılamaz çift"
ölçütü de boğulma ile bölünmeyi ayırmıyordu, K-103.)*

## 🟢 DÖRT KAPI DA GEÇTİ
| kapı | sonuç |
|---|---|
| **G1 · boş kol** | kol ortalaması **−0,00125**, 2 SE **0,00204** → içinde; her tohumda toparlanma süresi 0 |
| **G2 · tekdüzelik** | ölçüm hatasını aşan hiçbir düşüş yok |
| **G3 · ızgara fazı** | yarım adım kaydırmada en büyük fark **0,00187**, band **0,00991** |
| **G4 · bulanıklık** | gecikme p99 / ızgara = **0,021** (temiz) · **0,029** (karıştırılmış) |

⚠️ **G1'in dördüncü maddesi BOŞ YERE GEÇİYOR ve bu beyan edilir:** tespit
gecikmesi bir protokolün kopma beyanını gerektiriyor, depodaki iki koşum
aleti de hiç beyan etmiyor. **M4'ün boş kol kapısı Faz 2'ye ertelenmiştir**;
bugünkü kapsamı sentetik birim testleridir.

## ⭐ KAPI TABLOSU KENDİ BAŞINA BİR BULGU
Çalışma noktasında (−15 dBm) **mükemmel yönlendirmeyle** şok derinliği yalnız
**0,037**. Yani ayırt edici gücün tamamı protokolün körlüğünden gelmek
zorunda. Bu, K-103'ün *"tavan 0,96 iken protokol 0,75'e ulaşıyorsa aradaki
fark protokolün körlüğüdür"* argümanının **bağımsız bir doğrulamasıdır** —
ve bu sefer PDR tavanıyla değil, şok metriğiyle ölçüldü.

## 🔒 KÖKEN DEFTERİ — K-104'ün açık bıraktığı sorun kapandı
`TEDAVI` sözcüğünün iki anlamı vardı ve biri yapısal olarak zorlanıyordu
(`kosum/sonuc.py::TEDAVI_ALANLARI`, `kurulum_hash`in dışladığı dört alan).

| ne yapıldı | sonuç |
|---|---|
| `TEDAVI` kovası **tam olarak** `TEDAVI_ALANLARI` oldu | 10 → **4** alan; bir test ikisini **birbirine bağladı** — ayrışma artık kırmızı test |
| Kol tanımı sabitleri yeni **`KOL_TANIMI`** kovasına | 6 alan |
| Şartnamenin istediği ama kodda **hiç olmayan** `DUYARSIZ` eklendi | Faz 1'in çıktısının artık yazılacak yeri var |
| Borç düzyazıdan **sayaca** taşındı (`DUYARLILIK_BEKLEYEN`) | D12 artık **iki** sayaç basıyor; mühür ikisinin de sıfır olmasını ister |

🔴 **VE BORÇ ARTTI: 46 → 50.** Evre kafesinin dört sabiti deftere girdi ve
dördü de `SINANMAMIS`: RFC 3561/3626 **`02-DOGRULANMIS-KAYNAKLAR.md`de
YOK** — orada *"Faz 1'in girdisi"* diye, ikinci el bir taramadan geliyorlar.
Kova kuralı net: `KAYNAK` yalnız `02`de doğrulanmış olandır.

⭐ **Ve bu tek bir bibliyografik doğrulamayla kapanır, ÜÇ KARARI birden
taşıyarak:** aynı iki RFC, K-101'in Θ paydasını (OLSR TOP_HOLD_TIME) ve
K-103'ün bağlantılılık kısıtının zaman anlamını (AODV ACTIVE_ROUTE_TIMEOUT)
da çıpalıyor. Üçü de bugün **açılmamış** bir kaynağa dayanıyor.

⚠️ `BANT_SE_KATI` ve `YANLIS_ALARM` da `SINANMAMIS`: ikisi de α'dır ve
**ön-kayıttaki α'dan türetilmeli**. Bugün ayrı duruyorlar ve farklı olmaları
(0,025 ↔ 0,01) gerekçesiz — α için ikinci bir doğru kaynağı.

## BUNU NE DEĞİŞTİRİR
- Adım ⑤ **bitti**; sıradaki iş adım ⑥ (`ham` bölümü · kapsam beyanı).
- Evre metrikleri her sonuç satırında; açılma anı ölçüm penceresinin
  dışındaysa satır **sebebini kendi yazıyor** (sessiz atlama yok).
- 472 test geçiyor (21'i yeni) · `Yapisal ihlal YOK` · köken borcu **50** +
  duyarlılık borcu **5**.
- 🔴 Bir sonraki ajan için en yüksek getirili tek iş: **RFC 3561 ve 3626'yı
  açıp `02`ye işlemek.** Dört parametreyi `KAYNAK`a taşır ve üç ayrı kararın
  çapasını sağlamlaştırır.

---

# K-106 · 🟢 SİMÜLATÖR FAZI KAPANDI — ve iki RFC açılınca İKİNCİ bir straw-man çıktı

> **Tarih:** 8 Eylül 2026 · **Karar: ajan** · **Durum: UYGULANDI**
> **Bağlam:** Faz 0'ın son iki işi — dış çapaların doğrulanması ve sonuç
> satırının kendi kendine yeter hâle gelmesi.
> **Üreticiler:** `python kalibrasyon/adim9_kapanis.py 1` ·
> `python -m pytest tests2 -q` · `python kalibrasyon/mimari_denetimi.py`

## 1 · İKİ RFC AÇILDI — üç kararın çapası artık doğrulanmış

`02-DOGRULANMIS-KAYNAKLAR.md` RFC 3561/3626'yı *"Faz 1'in girdisi"* diye,
**ikinci el bir derlemeden** taşıyordu. Oysa aletin üç kararı onlara
dayanıyordu: Θ'nın paydası (K-101), bağlantılılık kısıtının zaman anlamı
(K-103), evre metriklerinin ölçüm kafesi (K-105).

Birincil belgeler açıldı ve `02` §R'ye işlendi:

| RFC | doğrulanan |
|---|---|
| **3561** *(Perkins, Belding-Royer, Das; Tem 2003; Experimental)* | `ACTIVE_ROUTE_TIMEOUT` = **3 000 ms** · `HELLO_INTERVAL` = **1 000 ms** |
| **3626** *(Clausen, Jacquet; Eki 2003; Experimental)* | `TC_INTERVAL` = **5 s** · `TOP_HOLD_TIME` = **3 × TC_INTERVAL** = **15 s** · `HELLO_INTERVAL` = **2 s** |

🔒 Θ'nın paydası (15 s) ve evre kafesinin iki sabiti (1 s · 15 s) **belgeden
okundu**. `IZGARA_ADIMI_S` ve `PENCERE_S` `SINANMAMIS` → **`KAYNAK`**.
Köken borcu **50 → 48**; `KAYNAK` kovası **2 → 4** *(daha önce yalnız
Boltzmann sabiti ve ışık hızı vardı)*.

## 2 · 🔴 AÇMANIN ORTAYA ÇIKARDIĞI ŞEY — kimse aramıyordu

İki RFC yan yana konunca görüldü:

| | AODV | OLSR |
|---|---|---|
| komşu yenileme aralığı | **1 s** | **2 s** |

Bu simülatörde beacon **koşum düzeyinde sabittir** — `kosu.py` onu tek bir
konfig alanından çizelgeler ve değeri **1 s**. Yani:

- **AODV** kendi RFC hızında koşuyor.
- 🔴 **OLSR, RFC'sinin İKİ KATI hızda beacon yayınlıyor.** Sonucu iki yönlü:
  komşu bilgisi RFC'den daha taze *(PDR'de avantaj)*, kontrol yükü iki katı
  *(`nrl_*` metriklerinde dezavantaj)*.

🔒 **Bu, K-101'de OLSR için bulunan straw-man'in AYNI SINIFTAN İKİNCİ
ÖRNEĞİDİR.** Orada topoloji bilgisi kullanılmadan bayatlıyordu; burada
kontrol yükü şişiyor. İkisi de `03` kural 4'ün yasakladığı şeyin adayı ve
ikisi de **kurulumun kendisinden** geliyor, kasıttan değil.

⚠️ **AMA ÖLÇÜLMEDİ, DOLAYISIYLA İDDİA EDİLMİYOR.** İki şey de doğru olabilir:
beacon ortak bir altyapıdır ve karşılaştırmada ortak-mod olarak sadeleşir;
ya da `nrl_*` bir sonuç metriğidir ve OLSR'ın payını iki katına çıkarmak onu
haksız yere kötü gösterir.

🔒 **Ayrıştıran ölçüm HAZIR:** `beacon_gonderilen` ayrı bir sayaç, yani
beacon'ın `nrl_*`e katkısı sonuç satırından çıkarılabilir. Faz 3'te taban
çizgileri koşarken ölçülür. `beacon_araligi_s` bu yüzden `SINANMAMIS`
kalıyor — değerinin kökeni artık belli ama *"hiçbir taban çizgisini
zayıflatmıyor"* iddiası ölçülmedi, ve bu proje ölçülmemiş bir şeye "kaynak"
demiyor.

## 3 · SONUÇ SATIRI ARTIK KENDİ KENDİNE YETİYOR

İki bölüm eklendi: **`kapsam`** ve **`ham`**.

### `kapsam` — her satır kendi sınırlarını taşıyor
Kapsam sınırları yalnız şartnamedeydi. Bir `.jsonl` satırı aylar sonra
açıldığında hangi sınırlarla üretildiği **satırdan okunamıyordu**; bir
sayının yanında kendi sınırı yoksa o sayı olduğundan geniş okunur.

İki liste var ve farkları önemli: `MODELLENMEYEN` **elle yazılır** (şartname
§12'nin aynası, bayatlayabilir), `bu_kosumda_kapali` **konfigden türer**
(bayatlayamaz — sönümlemesi kapalı bir koşu bunu kendi satırında söyler).

🔒 Her sınır, sonucu **hangi yöne** çektiğini de söylüyor. *"Yayılma kazancı
yok"* demek yetmez; okuyucunun bilmesi gereken, bunun karıştırıcıyı
olduğundan **~10 dB güçlü** gösterdiğidir. Bir test her satırın yönünü
yazmayı zorunlu kılıyor.

### `ham` — VARDI ama hiçbir yere yazılmıyordu
`PaketDefteri.ham_sozluk()` aylardır kodda duruyordu ve **hiçbir yerden
çağrılmıyordu**: `BOLUMLER` listesinde yoktu, yani satıra hiç girmiyordu.
`metrikler.py` başlığı bunu bir taahhüt olarak yazıyordu — *"`analiz/`in
doğrulama kapılarından biri satırdaki yüzdelikler ham listeden yeniden
üretilebiliyor mu olacak"* — taahhüt yerine getirilmemişti.

🔴 **Ve yazılsa bile yetmezdi: PAYDA defterde yoktu.** Evre metrikleri PDR'yi
zaman kovalarında hesaplıyor, yani pencerede doğan paketlerin **ANLARI**
gerekiyor; defter yalnız `pencerede_uretilen` **sayısını** veriyordu ve bir
sayıdan kova çıkmaz. `dogum_s` eklendi.

⚠️ **VE EKLERKEN BİR KUSUR DAHA ÇIKTI.** İlk yazımda `dogum_s` pencereye
kırpılmıştı, oysa `teslim_*` dizileri koşumun TAMAMINI kapsıyor: pay ile
payda **farklı kümelerden** geliyordu ve `teslim_dogum_s ⊄ dogum_s` oldu.
Bu, `pdr_pencere`de bir kez düzeltilmiş olan kusurun aynısıdır. Testin
alt-küme iddiası onu ilk koşuda yakaladı. İkisi de artık koşumun tamamını
kapsıyor; pencere `kapsam.olcum_penceresi_s` ile filtrelenerek elde ediliyor.

🔒 **Kapı artık koşuyor:** bir test, satırdaki `sok_derinligi`,
`pdr_temiz`, `pdr_sok` ve `toparlanma_tamligi`yi **yalnız `ham` + `kapsam`
bölümlerinden** yeniden hesaplayıp karşılaştırıyor.

### Bedeli ölçüldü ve beyan edildi
Tam uzunlukta statik bir koşuda satır **0,52 MB**, bunun **511 KB'ı (%98)**
`ham`. Çekirdek deney (360 koşu) ≈ **187 MB**, tam matris (2 160) ≈ **1,1 GB**.

🔒 `ham` **kapatılabilir yapılmadı** ve bu bilinçli: kapatılabilir olsaydı iki
koşum modu doğardı — birinde metrikler yeniden üretilebilir, diğerinde değil
— ve hangi modda koşulduğu bir gün unutulurdu. Boyut sorun olursa çözüm
sıkıştırmadır, atlama değil.

## BUNU NE DEĞİŞTİRİR
- **Faz 0 (simülatörü karara bağlama) BİTTİ.** Altı işin altısı kapalı.
- Sonuç satırı sekiz bölüm taşıyor ve **kendi kendine yetiyor**: metrikleri,
  sınırlarını ve onları yeniden üretecek ham veriyi birlikte.
- 474 test geçiyor · `Yapisal ihlal YOK` · köken borcu **48** + duyarlılık
  borcu **5** · korunum + mutabakat 6 tohumda TAMAM.
- 🔴 Faz 3'e devredilen ölçülebilir borç: **beacon aralığının OLSR'a etkisi**.

---

# K-107 · 🟢 DUYARLILIK DENETİMİ — 48 GEREKÇESİZ SAYI 34'E İNDİ, VE DÖRT ÖLÇÜT HATAM ÇIKTI

> **Tarih:** 8–9 Eylül 2026 · **Karar: ajan** · **Durum: UYGULANDI**
> **Bağlam:** Faz 1, ilk iş. Şartname `07-SIMULATOR-TASARIMI.md` §11.3.
> **Üreticiler:** `python -u kalibrasyon/duyarlilik.py <kol> [parametre…]` ·
> `python -u kalibrasyon/cozunurluk.py`

## NE YAPILDI
49 aday parametre (`SINANMAMIS` + `KOL_TANIMI`), 5 tohum, iki yönde (×2 ve
×0,5), iki kâhin aleti, altı ayrı kolda oynatıldı. Toplam ~1 200 koşum,
~4,5 saat. Sonuç: **köken borcu 48 → 33**, `DUYARSIZ` kovası 0 → **15**.

## 🔒 TASARIM — üç karar, üçü de sıfır serbest parametreli

### İki alet, ÜÇ çıktı — ve üçüncüsü asıl olan
    y1 = PDR(en_guvenilir_kahin)   mükemmel yönlendirme — TAVAN
    y2 = PDR(en_kisa_yol_kahin)    BAŞKA bir yönlendirme ölçütü
    y3 = y1 − y2                   ÖLÇÜTÜN BEDELİ

`y3`, protokol sıralamasının duyarlılığı için bugün ölçülebilen en iyi
**vekildir**: iki kâhin aynı dünyayı ve aynı trafiği görür, tek fark
yönlendirme ölçütüdür. Bir parametre `y3`ü oynatıyorsa stratejiler arası
dengeyi oynatıyordur. Tek çıktıya bakmak yetmezdi — `y1` ve `y2` birlikte
düşüp `y3`ü sabit bırakabilir.

### "DUYARSIZ" ile "ÖLÇÜLEMEDİ" — parmak iziyle ayrılıyor
🔴 Bir parametre o kolda **hiç devrede değilse** çıktıyı oynatmaz ve saf bir
tarama onu *"duyarsız"* diye aklar. Simülasyon belirlenimli olduğu için
hesaba gerçekten giren bir parametre çıktının bir yerini değiştirir — 15.
ondalığı bile olsa. Parmak izi birebir aynıysa **`OLCULEMEDI`**.

⭐ **Bu mekanizma işe yaradığını KANITLADI:** `darbe_periyodu_s` ve
`darbe_gorev_cevrimi` `statik-surekli` kolunda `OLCULEMEDI` çıktı; kendi
darbeli kollarında **DUYARLI** çıktılar. Tek kolda taramak dört sabiti
haksız yere aklardı.

### Eşik değil, DENEYİN KENDİ ÇÖZÜNÜRLÜĞÜ
Üretici: `python kalibrasyon/cozunurluk.py` — 30 tohum, `statik-surekli`.

| çıktı | ortalama | SD_tohum | **R = 2·SD/√30** |
|---|---|---|---|
| `pdr_etx` | 0,9379 | 0,0693 | 0,0253 |
| `pdr_atlama` | 0,8896 | 0,0988 | **0,0361** |
| `olcut_bedeli` | 0,0483 | 0,0706 | 0,0258 |

🔴 **BU KENDİ BAŞINA BİR BULGU VE ŞARTNAMENİN İSTEDİĞİ GÜÇ ANALİZİDİR**
(§09.3: *"Tohum sayısı 30 diye kabul edilmez; hesaplanır"*). **30 tohumlu bir
hücre yalnızca 3,6 PDR puanından büyük farkları görebiliyor.** Tohumlar arası
SD 0,07–0,10 — çok yüksek. Protokoller 5 puandan az ayrışıyorsa 30 tohum
YETMEZ ve bu mühürden önce karara bağlanmalı.

⭐ `olcut_bedeli` eşleştirilmiş olduğu için daha keskin (0,026): deneyin asıl
ayırt edici ekseni de zaten odur.

## 🔴 DÖRT ÖLÇÜT HATASI — hepsi ölçüm sırasında çıktı

### 1. Karşılaştırma EŞLEŞTİRİLMEMİŞTİ
İlk hâl, bozulmamış koşumun tohumlar arası yayılımını band olarak
kullanıyordu. Ölçüldü: o band `pdr_atlama` için **0,134**, ölçüt bedeli için
**0,196**. Hiçbir parametre duyarlı çıkamazdı ve tarama *"her şey duyarsız"*
diye makul görünen, tamamen gürültüden ibaret bir cevap üretecekti.

🔒 Oysa RNG mimarisi eşleştirmeyi zaten yapısal kılıyor. Doğru istatistik
**tohum başına fark**tır; tohumlar arası varyans ortak-mod olarak düşer.
Düzeltince tarama ayırt etmeye başladı.

### 2. Üç pencere alanı ÇÖKTÜ ve SESSİZCE AKLANDI
`isinma_s`, `olcum_bitis_s`, `kosu_bitis_s` `TypeError` verdi — tarama kendi
pencere ayarlarını iki kez geçiriyordu. Hata düşüldü **ama karar
`OLCULEMEDI` kaldı**: yani ölçülemeyen bir şey *"bu kolda etkisiz"* diye
raporlandı. 🔒 `GECERSIZ` artık en yüksek öncelikli karar; bir ölçüm aracının
kendi arızasını ölçtüğü şeyin özelliği gibi göstermesi bu projedeki en pahalı
hata sınıfıdır.

⚠️ Düzeltmeden sonra ortaya çıktı ki `isinma_s` ve `olcum_bitis_s`
**OAT ile taranamaz**: bir sıralama değişmeziyle (`ısınma < ölçüm < koşu`)
birbirine bağlılar, biri tek başına oynatılamıyor. Ayrı bir **birleşik
pencere taraması** gerekiyor ve bu borç olarak duruyor.

### 3. `modulasyon` HİÇ OYNATILMAMIŞTI
`str` tipi hiçbir dala girmiyordu, `None` dönüyordu, koşum hiç
çizelgelenmiyordu — ve parametre `OLCULEMEDI` diye raporlanıyordu. Yani
**sınanmadığı hâlde "bu kolda etkisiz" gibi göründü.** Artık geçerli diğer
modülasyona çevriliyor.

### 4. Ölçüt BÜYÜK AMA TUTARSIZ etkileri aklıyordu
`irtifa_maks_m` PDR'yi iki yönde de **8 puan** oynatıyor ama tohumlar arası
yayılımı büyük olduğu için band testini geçiyor — yani 8 puanlık bir etki
*"duyarsız"* etiketi alacaktı.

🔒 Düzeltme iki parçalı bir kural: bir parametre `DUYARSIZ` olabilmek için
**hem** kendi hata payı içinde olmalı **hem** etkisi deneyin çözünürlüğü
R = 0,036'nın altında kalmalı. Biri yetmez.

## 🟢 SONUÇ — hangi sayılar sonucu belirliyor

### BASKIN (|Δ| ≥ 0,05) — bunlar gerekçelendirilmeden mühür vurulamaz
| parametre | en büyük etki | ne |
|---|---|---|
| `iletim_menzili_m` | **−0,655** (bandın 10,3 katı) | güç çapası |
| `frekans_hz` | **−0,234** (6,2×) | yol kaybı |
| `dugum_sayisi` | **−0,183** | yoğunluk |
| `bant_genisligi_hz` | −0,112 | gürültü tabanı |
| `sicaklik_k` | −0,112 | gürültü tabanı |
| `gurultu_figuru_db` | −0,112 | gürültü tabanı |
| `karistirici_guc_override_dbm` | −0,112 | tehdit şiddeti |
| `darbe_periyodu_s` | −0,093 | darbeli kolun tanımı |
| `darbe_gorev_cevrimi` | +0,066 | darbeli kolun tanımı |
| `rician_k_db` | −0,060 | sönümleme derinliği |
| `akis_sayisi` | +0,052 | yük |

⭐ **Desen açık: BAĞLANTI BÜTÇESİ baskın.** Menzil çapası, frekans, bant
genişliği, sıcaklık, gürültü figürü — hepsi SINR'i belirliyor. Yani
gerekçelendirilecek 34 sayı değil, esas olarak **bir avuç bağlantı bütçesi
sayısı** var.

⭐ Ve `sicaklik_k` (290 K) ile 802.11b MAC sabitleri **tek bir bibliyografik
doğrulamayla** birlikte `KAYNAK`a geçebilir — RFC'lerde olduğu gibi.

### SAPTANABİLİR ama küçük (R'nin üstünde, 0,05'in altında)
`taramali_konak_suresi_s` · `taramali_konak_sayisi` · `yeniden_deneme_siniri` ·
`akis_paket_hizi_hz` · `beacon_araligi_s` · `beacon_bayt` · `bit_hizi_bps` ·
`kanal_dilimi_s` · `gm_adim_s`

### 🟢 DUYARSIZ — ölçümle hak edildi (15)
`cbr_titresim_s` · `cw_min` · `golgeleme_hucre_m` · `irtifa_min_m` ·
`onay_bayt` · `onbelge_s` · `paket_bayt` · `sifs_s` · `slot_s` ·
`temel_bit_hizi_bps` · `reaktif_sezme_s` · `reaktif_patlama_s` ·
`gm_pitch_sigma_rad` · `kosu_bitis_s` · `modulasyon`

⭐ `reaktif_sezme_s` ve `reaktif_patlama_s` — K-104'ün *"donanım iddiası,
kaynak yok"* diye işaretlediği iki sabit — kendi reaktif kollarında ölçüldü
ve **duyarsız** çıktı. Kaynak borcu ölçümle kapandı.

### ⚠️ KARAR YOK (2) — daha çok tohum gerekiyor
`irtifa_maks_m` (|Δ| 0,098) ve `karistirici_konum` (|Δ| 0,048): etkileri
R'nin üstünde ama kendi hata paylarının içinde. Ne aklanabilir ne mahkûm
edilebilir.

### OLCULEMEDI (yapısal olarak etkisiz)
`cca_s` · `cw_max` · `komsu_omru_katsayisi` · `kuyruk_kapasitesi` ·
`saat_ofset_araligi_s` · `saat_sapma_ppm` · `ttl_baslangic` ·
`yakalama_esigi_db` · `yakalama_penceresi_s`

⭐ İkisinin sebebi öğretici: **`cw_max` = 1023'e HİÇ ULAŞILAMIYOR** — yeniden
deneme sınırı 4 olduğu için CW en fazla 511'e çıkıyor. Ve `ttl_baslangic` =
32, ağ çapı ~3 olduğu için hiç bağlamıyor. İkisi de "gerekçesiz" değil,
**erişilemez**.

## 🔴 DUYARLILIK BORCU KAPANMADI — BÜYÜDÜ
K-104, dört kol tanımı sabitini `TEDAVI`den `KOL_TANIMI`na taşımış ve borcu
sayaca bağlamıştı. Şimdi beşi de kendi canlı kollarında oynatıldı:

    darbe_periyodu_s          🔴 DUYARLI  (R'nin 2,6 katı)
    darbe_gorev_cevrimi       🔴 DUYARLI
    taramali_konak_suresi_s   🔴 DUYARLI
    taramali_konak_sayisi     🔴 DUYARLI
    karistirici_konum         ⚠️ KARAR YOK

🔒 Yani bu beş sayı **sonucu belirliyor**. Borç artık *"ölçülmedi"* değil,
*"ölçüldü ve önemli çıktı"*: her biri ya gerekçelendirilecek ya da ön-kayıtta
bir EKSEN olarak ilan edilip deneyde oynatılacak. **Sabit tutulan ve sonucu
belirleyen bir sayı gerekçesiz kalamaz.**

⚠️ K-104'ün *"bunlar kol tanımıdır, tedavi değişkeni değil"* yargısı ölçümle
doğrulandı ama **aklanmadı**: kol tanımı olmak, sonucu belirlememek anlamına
gelmiyor.

## ⚠️ BU TARAMANIN BEYAN EDİLEN ÜÇ SINIRI
1. **OAT** — her parametre tek başına oynatıldı; birlikte etkiler görülmedi.
2. **Çalışma noktası çıktıları** — protokol SIRALAMASININ duyarlılığı
   ölçülmedi, o gerçek protokoller gerektiriyor (Faz 3).
3. **Ölçüt kasten asimetrik** — 5 tohumla `2 SE` katı bir %95 testi değil,
   duyarlılığı fazla çağırmaya meyilli. Yön bilinçli: yanlışlıkla `DUYARLI`
   demek parametreyi yığında tutar, yanlışlıkla `DUYARSIZ` demek gerekçesiz
   bir sayıyı **aklar**.

## BUNU NE DEĞİŞTİRİR
- Köken borcu **48 → 33**; `DUYARSIZ` kovası ölçümle dolmaya başladı.
- Gerekçelendirme yığını artık **öncelikli**: bağlantı bütçesi 5–6 sayı, yük
  3 sayı, kol tanımı 4 sayı. Geri kalanı gürültü.
- 🔴 Ön-kayıt mührünün önünde yeni bir engel: **30 tohum 3,6 puandan küçük
  farkları göremiyor.** Beklenen protokol farkı bunun altındaysa tohum
  sayısı artmak zorunda.
- Birleşik pencere taraması (`isinma_s` · `olcum_bitis_s`) açık borç.

---

# K-108 · 🔴 Lİ REPLİKASYONU: SAYI TUTMADI, MEKANİZMA TUTTU — sebep α

> **Tarih:** 9 Eylül 2026 · **Karar: ajan** · **Durum: UYGULANDI**
> **Ön-kayıt:** `v2/09-LI-REPLIKASYONU.md` — **ölçümden ÖNCE** yazıldı ve
> sonuç görüldükten sonra **değiştirilmedi**; sonuç altına eklendi.
> **Üretici:** `python -u kalibrasyon/li_replikasyonu.py`

## NE ÖLÇÜLDÜ
Aletin **tek dış çapası**. Bugüne kadarki bütün doğrulama iç tutarlılıktı;
Bianchi MAC'i tek çarpışma alanında sınıyor, oysa bu projenin ölçtüğü şey çok
atlamalı teslim. Aradaki boşluk — uzamsal yeniden kullanım — hiç sınanmamıştı.

| hipotez | sonuç |
|---|---|
| **H1** — uzun zincir / tek atlama ∈ [0,10; 0,20] | 🔴 **TUTMADI** — 0,086 |
| **H2** — eğri düşüyor ve düzleşiyor | 🟢 TUTTU |
| **H3** — ideal MAC tavanının (1/4) altında | 🟢 TUTTU |

## 🔴 İKİ HİPOTEZ KURDUM, İKİSİ DE ÇÜRÜDÜ
Eğrinin şekli soruyu daralttı: `oran × atlama ≈ 0,74` ve N ≥ 5'ten sonra
**sabit** — yani verim atlama sayısıyla ters orantılı, uzamsal yeniden
kullanım yokmuş gibi.

1. **"Taşıyıcı dinleme menzili çok geniş"** *(duyma/iletim = 6,31; Li ~2)*.
   Menzil tarandı: daraltmak **düzeltmiyor, kötüleştiriyor** (280 m'de oran
   0,031 — gizli terminal). Hiçbir değerde band'a girmiyor. ❌
2. **"280 m'de bağ marjı sıfır"** *(güç çapası = SINR tam eşikte)*. Aralık
   100 → 280 m tarandı: oran 0,074–0,081, `oran × atlama` her yerde ≈ 0,74–0,81. ❌

🔒 Tahmin etmeyi bırakıp **mekanizmayı doğrudan ölçtüm**.

## 🟢 MEKANİZMA — ve tam sayısal kapanış
**Yeniden kullanım VAR:** birbirinden çok uzak 4 çift tam **4 katı** veriyor
(1,000 · 1,000 · 1,000). Alet serileştirmiyor.

**Yeniden kullanım MESAFESİ ölçüldü:** iki çift arasındaki ayrım tarandı —
6 atlamada oran 1,07 *(yok)*, **8 atlamada 2,00** *(tam)*. Yani **8 atlama**;
Li'nin modelinde 4.

**Kapalı formda türedi ve birebir tuttu:**

    girişim menzili / iletim menzili = 10^(SINR_eşiği / (10·α)) = 10^(16/20) = 6,31

Ölçülen oran **6,31**. Yeniden kullanım ≈ 6,3 + 1 ≈ 7–8 atlama → ölçülen 8.

**Zincir oranının öngörüsü:** Li'de yeniden kullanım 4 atlama, ideal 1/4,
802.11 ile 1/7 ⇒ verimlilik çarpanı 0,571. Bizde 8 atlama ⇒ **0,571/8 =
0,0714**. **Ölçülen 0,0739 — uyum %4.**

## 🔒 SEBEP: YOL KAYBI ÜSTELİ α
| | Li *(yer tabanlı)* | bu proje |
|---|---|---|
| α | ~4 | **2,0** |
| girişim/iletim | 2,5 | **6,31** |
| yeniden kullanım | ~4 atlama | **8 atlama** |
| zincir oranı | 0,143 | **0,074** |

α = 2,0 **gerekçeli bir karardır** (`07` §04: hava-hava serbest uzay) ve
§04.1'de *"taşıyıcı dinleme menzili sert değil"* diye ölçümden önce ilan
edilen farkın nicel hâlidir. Sapma **sonradan bulunmuş bir mazeret değil**;
ilan edilmiş bir farkın büyüklüğü ölçüldü ve sayıyı %4 hatayla açıkladı.

⭐ **Replikasyonun asıl sınadığı şey DOĞRU ÇIKTI:** eğri Li'nin öngördüğü gibi
düşüp düzleşiyor, ideal tavanın altında kalıyor, ve mutlak değer yeniden
kullanım mesafesinden türetilebiliyor. Alet Li'nin fiziğini yeniden üretiyor —
farklı bir yayılım rejiminde.

## BUNU NE DEĞİŞTİRİR
- 🔴 **Çok atlamalı sonuçlar bu projede Li'ninkinden yapısal olarak daha kötü
  olacak** ve sebebi bilinen bir fizik. Sonuç bölümünde beyan edilmeli.
- 🟢 **ÖNGÖRÜ DOĞRULANDI (aynı gün, `kalibrasyon/yeniden_kullanim.py`).**
  Üç α değerinde yeniden kullanım mesafesi ölçüldü: 8 · 4 · 3 atlama;
  girişim/iletim oranları 6,31 · 3,41 · 2,51. Oran **1,268 · 1,171 · 1,194**
  — ortalama **1,211**, saçılma **%8**. Yani mesafe, oranla **ORANTILI** ve
  çarpan α'dan bağımsız.

  ⚠️ Zincirle denemek başarısız oldu — ama sebebi α değil, **kendi
  hatamdı**: `python -c` içinde iç içe `Pool` açmak kilitleniyor. Tek koşu
  2,7 saniye sürerken iş bir saat boyunca sıfır çıktı verdi. Ölçüm zincirle
  değil, **iki çift probuyla** yapıldı — zaten daha temizi: zincir kuyruk ve
  uçtan uca etkileri de taşıyor, iki çift soruyu saf hâlde soruyor.

  🔴 **VE BİR ÖLÇÜT HATASI DAHA ÇIKTI.** İlk sınav *"mesafe ≈ oran + 1
  atlama"* sezgisini kullanıyordu; α = 2'de tuttuğu için doğru sanılmıştı.
  Toplamsal sabit tutmuyor, **oran** tutuyor. Sınav, çarpanın DEĞERİNİ değil
  α'dan BAĞIMSIZLIĞINI sınayacak biçimde yeniden yazıldı. *(Kayda geçmiş
  öngörü — "α=3 → 4–5, α=4 → 3–4 atlama" — zaten tutuyordu; düzeltilen
  betikteki kapıydı, öngörü değil.)*

  🔒 **Nihai bağıntı:** `yeniden kullanım mesafesi ≈ 1,21 × 10^(eşik/(10α))`.
  Çarpan türetilmedi, ölçüldü; 1'den büyük olmasının sebebi PER eğrisinin
  sert bir basamak olmamasıdır.
- 🔒 **Ön-kayıtlı band genişletilmedi ve genişletilmeyecek.** H1 tutmadı
  yazıyor ve öyle kalıyor.
- ⚠️ Replikasyon gölgeleme ve sönümleme **kapalı** koşar (`09` §03.1b):
  açıkken donmuş derin Rician çekimi bağların %2–6'sını öldürüyor ve zincirin
  beşte biri sıfır teslim ediyor. Yani replikasyon kanalın tamamını değil,
  MAC + girişim + uzamsal yeniden kullanımı doğrular.

---

# K-109 · 🔴 MİMARİ YARIMMIŞ — ölçüm katmanının hiçbir disiplini yoktu

> **Tarih:** 9 Eylül 2026 · **Karar: öğrenci yönlendirdi, ajan uyguladı**
> **Bağlam:** Öğrenci, bağlantı bütçesi gibi işlerden ÖNCE alınan sonuçların
> gerçek olduğundan emin olunmasını ve mimarinin eksiksiz olmasını istedi.
> **Üretici:** `python kalibrasyon/mimari_denetimi.py`

## 🔴 ÖĞRENCİ HAKLIYDI — ve sebebi ölçüldü

Bir önceki iki oturumda bulunan kusurların **hepsi** `kalibrasyon/` altındaydı:
kapalı bir karıştırıcıyı ölçen üç tablo, eşleştirilmemiş bir istatistik,
sınırda çöken bir hata payı, hiç oynatılmamış bir parametre, kilitlenen bir
havuz. Bu tesadüf değilmiş:

| katman | dosya | kapı |
|---|---|---|
| `sim2/` — MODEL | 52 | **12** |
| `kalibrasyon/` — ÖLÇÜM ALETLERİ | 24 | **1** *(yalnız "import edilebiliyor mu")* |

🔒 Yani simülatör on iki yapısal sözleşmeyle korunuyordu, onu ölçen aletler
hiçbiriyle. **Kusurların korumasız yarıda toplanması bir tesadüf değil,
kapsam boşluğunun doğrudan sonucudur.**

## ÜÇ YENİ KAPI

### D13 · kalibrasyon sabitleri kökene bağlı mı
Tarandı: **41 davranış belirleyen sabit, hiçbiri köken defterinde yok.**
İçlerinden biri doğrudan sonucu belirliyor — `kahin.py::ATLAMA_ESIGI = 0,90`:
çalışma noktası **ρ = 0,258, o eşikle tanımlanmış bir grafikte ölçüldü** ve
eşik ne kayıtlı, ne türetilmiş, ne ölçülmüştü.

🔒 27'si deftere bağlandı. 14'ü `TARIHSEL_FIZIK` beyanlı modülde ve muaf —
donmuş bir anlık görüntü, canlı bir ölçüm parametresi değil.

### D14 · gölge fizik — ve KENDİ KAPIMIN YANLIŞ ALARMI
`adim3_oncesi.py` fizik sabitlerinin kendi kopyasını taşıyor ve **dördü
ayrışmış**: alan 1000 ↔ 1800 m, yol kaybı üsteli **3,0 ↔ 2,0**, SINR eşiği
**10 ↔ 16 dB**. Yani ölçek kapısının eleyip attığı α = 3 orada yaşıyor.

🔴 **Ama ilk yazdığım kapı YANLIŞ ALARM verdi.** Modül bu durumu ZATEN beyan
ediyordu ve her koşumda `bayatlik_raporu()` basarak hangi sabitin ayrıştığını
söylüyordu. Doğru yapılmış bir işi kusur diye işaretledim.

🔒 **Doğru çalışan işi kırmızıya boyayan bir kapı, kapısızlıktan KÖTÜDÜR:**
insanları kapıyı görmezden gelmeye alıştırır. Kural yasak değil **sözleşme**
oldu: fiziğin kopyasını tutan modül `TARIHSEL_FIZIK` beyan etmek ve
bayatlığını her koşumda raporlamak zorunda. Beyanlı kopya NOT, beyansız
kopya BULGU.

### D15 · bayat üretici
Muafiyetin bedeli: tarihsel bir betik **canlı bir sayının üreticisi**
gösterilemez. Kapı tam bir tane buldu: `golgeleme_sigma_db` `OLCULMUS`
kovasındaydı ve üreticisi `adim3_oncesi.py` idi — yani canlı bir kova
iddiası, **terk edilmiş bir çalışma noktasında** hesaplayan bir betiğe
dayanıyordu. Sayıyı doğrulamak için onu koşturan biri başka bir cevap alır ve
nedenini bilemezdi.

🔒 **İddia bugünkü fizikte YENİDEN ÖLÇÜLDÜ ve AYAKTA:** PER'in 0,99→0,01
geçiş bandı **3,44 dB**, σ = 3,00 dB, oran 1,15 — aynı mertebede. *(Terk
edilmiş noktada 3,02 dB idi.)* Üretici artık canlı: `adim4_kapanis.py` §D.

## 🔴 KAPILAR ÜÇ HATA DAHA BULDU — ikisi benim yeni kodumda

1. **Denetimin kapsamı defterinkinden dardı.** Defter iki ağacı kapsar hâle
   gelince D12 yeni 27 kaydı birden *"ölü kayıt"* ilan etti — çünkü yalnız
   `sim2/` tarıyordu. 🔒 Bir denetimin kapsamı, denetlediği defterin
   kapsamından dar olamaz.
2. **Aynı muafiyet iki kapıda ayrı yazılmıştı** ve ayrıştılar: D13'ün muaf
   tuttuğu 14 sabiti D12 *"kökeni yazılmamış"* saydı. Kural tek kaynağa
   bağlandı.
3. **Var olan bir test benim yeni kayıtlarımı yakaladı:**
   `test_OLCULMUS_kova_URETICI_gostermek_zorunda` — üç kaydı `OLCULMUS`
   yazmıştım ama üretici göstermiyorlardı.

## ⭐ VE O TEST BİR BULGU DAHA ÇIKARDI
`SONUMLEME_ORNEGI = 6` iddiası ölçüldü ve **ikiye ayrıldı**:

| kol | K = 1 · 2 · 6 · 16 · 48 | sonuç |
|---|---|---|
| **statik** (donuk) | 8,100000 · 8,100000 · 8,100000 · 8,100000 · 8,100000 | 🟢 K sonucu **hiç** değiştirmiyor — iddia KANITLI |
| **hareketli** | 7,20 · 8,05 · **7,90** · 7,90 · **8,10** | 🔴 K = 6 **YAKINSAMAMIŞ** (K=48'e göre %2,5 fark) |

🔒 Yani "ölçülmüş" görünen bir sayı, ihtiyaç duyulan yerde ölçülmemiş.
`OLCULMUS` → `SINANMAMIS`, üretici eklendi (`adim4_kapanis.py` §E).

⚠️ Ayrıca `duyarlilik.py::TOHUMLAR`ı `OLCULMUS` yazmıştım — yanlıştı:
`cozunurluk.py` 30 tohumun çözünürlüğünü ölçüyor, 5 tohumun YETERLİLİĞİNİ
değil. Düzeltildi.

## SONUÇ
- `sim2/` **12 kapı** · `kalibrasyon/` artık **4 kapı** *(D11 · D13 · D14 · D15)*.
- Köken defteri **iki ağacı** kapsıyor: 123 parametre, `kokeni yazilmamis 0`,
  `olu kayit 0`, `SESSIZ golge fizik 0`, `bayat uretici 0`.
- Borç **görünür oldu**: `SINANMAMIS` 33 → **43**. Bu bir gerileme değil —
  27 yeni sabit deftere girdi ve 10'u dürüstçe gerekçesiz çıktı.
- 🔴 Yeni ve önemli borç: **`ATLAMA_ESIGI = 0,90`** çalışma noktasını
  belirliyor ve gerekçesiz. **`ETKIN_YARICAP_M = 400`** Θ'yı belirliyor ve
  K-096 tam da tek yarıçapın bağ kümesini temsil edemediğini ölçmüştü.

## 🔒 BU OTURUMUN ASIL DERSİ
Bu oturumda dört kez, kendi yazdığım bir ölçüt ya da kapı, ölçtüğünü sandığı
şeyi ölçmedi. Hepsini yakalayan şey **başka bir kapı** oldu — parmak izi
mekanizması, boş kol kapısı, alt küme iddiası, üretici testi.

🔴 Bundan çıkan kural: **bir ölçüm aletine, ölçtüğü şeye güvendiğinden daha
az güvenme.** Aletin de kapısı olmalı.

---

# K-110 · 🔴 ÜÇ BORÇ TEK ALETLE KAPANDI — ve dört şey daha çürüdü

> **Tarih:** 9 Eylül 2026 · **Durum: UYGULANDI**
> 🔒 **KARAR DEVREDİLDİ VE BU KAYDA GEÇER.** Öğrenci şunu söyledi:
> *"tamam simülasyonu geliştirmek için gerekenleri yap sana bırakıyorum."*
> `03` Bölüm E: *"Bir kararı sana devrederse, kararı ver ama devredildiğini
> açıkça kaydet."* Aşağıdaki bütün seçimler ajana aittir; kapsam ve
> gerçekçilik kararları öğrenciye açık kalmaya devam ediyor.
> **Üreticiler:** `python -u kalibrasyon/bag_kumesi.py` ·
> `python kalibrasyon/adim3_kapanis.py` · `python kalibrasyon/mimari_denetimi.py`

## NE YAPILDI

Üç ayrı açık borç aynı eksik ölçüme dayanıyordu — hepsi *"bağ kümesini
KANALDAN oku"* diyordu:

| borç | kaynağı |
|---|---|
| `ATLAMA_ESIGI = 0,90` gerekçesiz ve **çalışma noktasını belirliyor** | K-109 |
| Θ'nın kanal tabanlı doğrulaması **taahhüt edilmiş ama yazılmamış** | `calkanti.py` başlığı |
| bağlantılılık sayılarının üreticisi **koşmuyor** | bu oturumda bulundu |

Tek bir alet yazıldı: `kalibrasyon/bag_kumesi.py`.

🔒 **KÂHİN GRAFİĞİ YENİDEN YAZILMADI** — ve bu bir tercih değil kısıt: ikinci
bir bağ-kalitesi gerçeklemesi, bu projenin defalarca yakalandığı hata
sınıfıdır. Onun yerine var olan grafiğin **ETX değerleri okunuyor** ve her
eşiğin bağ kümesi onlardan geri türetiliyor (`etx = 1/p`, `atlama = 1 −
(1−p)^5`). Tek geçişte bütün eşikler çıkıyor; modele sıfır dokunuş.

## 🔒 ALETİN KENDİ DÖRT KAPISI — bulgu üretmeden önce

| kapı | ne sınar | sonuç |
|---|---|---|
| **G-a** | türetilen derece == canlı grafiğin kendi derecesi | 🟢 6/6 tohum, 9 ondalık birebir |
| **G-b** | sönümleme KAPALIYKEN faz kaydırması grafiği değiştirmemeli | 🟢 yayılım **0,000e+00** |
| **G-c** | eşik sütunu gerçekten değişiyor mu | 🟢 derece 9,56 → 8,06 |
| **G-d** | ETX kâhini eşikten etkilenmemeli, atlama kâhini etkilenmeli | 🟢 **0,000e+00** ↔ **0,0739** |

⭐ G-d, iki kâhinin **ilan edilmiş tanımını** doğrudan sınıyor ve ikisi de
tanımlarına birebir uyuyor. G-b ise "faz kaydırması sönümlemeyi izole eder"
varsayımını bir iddia olmaktan çıkarıyor.

## 🟢 BAĞ EŞİĞİ — PLATO ÖLÇÜLDÜ

*Üretici: `python -u kalibrasyon/bag_kumesi.py b d`*

**ρ'nun kendisi eşiğe neredeyse duyarsız** (−15 dBm'de 0,252…0,259) — ve
sebebi yapısal: ρ bir ORANDIR, payı da paydası da aynı eşiği kullanır.

🔴 **Ama sert kısıt bir oran değil.** Seçilen karıştırıcı gücü eşiğe bağlı:

| eşik | 0,50 | 0,70 | **0,80** | **0,90** | **0,95** | **0,99** |
|---|---|---|---|---|---|---|
| seçilen güç (dBm) | −12,0 | −12,0 | **−15,0** | **−15,0** | **−15,0** | **−15,0** |
| ölçüt bedeli | — | +0,0850 | +0,0599 | **+0,0299** | +0,0202 | +0,0111 |
| tabandan fark | — | +0,055 🔴 | +0,030 🔴 | taban | −0,010 | −0,019 |

*(ölçüt bedeli: `statik-surekli`, **15 tohum**, eşleştirilmiş fark)*

🔒 **İki bağımsız ölçüt aynı sınırı gösteriyor:** çalışma noktası 0,80'in
altında kayıyor, ölçüt bedeli 0,80 ve 0,70'te DUYARLI çıkıyor. 0,90 · 0,95 ·
0,99 üçünde de hiçbir karar değişmiyor.

**Kova: `SINANMAMIS` → `OLCULMUS`.** Ölçüt: *kararların değişmediği platonun
EN KÜÇÜK değeri* — yani bağ kümesini en büyük yapan eşik, kararların sabit
kalması kısıtı altında. Bu, alan seçimi *(kopukluk sıfırken en büyük alan)*
ve karıştırıcı gücü *(ayrılma yokken en büyük ρ)* ölçütleriyle **aynı
biçimdedir**.

⚠️ **İki sınır beyan edilir.** (a) Ölçüt taramayı **gördükten sonra**
formüle edildi — plato ölçüldü, sonra *"platonun alt kenarı"* kuralı yazıldı;
K-103'ün kaydettiği aynı dürüstlük borcu. (b) Kenar yalnız taranan ızgarada
bilinir; gerçek kenar **(0,80; 0,90]** aralığındadır.

⚠️ Standart ×0,5 oynatması (0,45) bu platonun **dışındadır**. Yani sayı
`DUYARSIZ` **değildir**: bandıyla birlikte ölçülmüştür ve band **aşağı yönde
bağlayıcıdır**. Kova kaydı bandı taşıyor — yazılmasaydı biri bir gün eşiği
düşürür ve çalışma noktası sessizce kayardı.

## 🔴 KIRIK ÜRETİCİ — ve onun taşıdığı tablo iki kere çürüdü

`adim3_kapanis.py` bağlantılılık sayılarının üreticisiydi ve **koşmuyordu**:
kolların ESKİ adını (`mobil-yok`) kullanıyordu. Üçüncü kol eklenirken
(4 Eylül) kollar yeniden adlandırıldı, betik güncellenmedi, ve `Konfig`
bilinmeyen senaryoyu reddettiği için bölüm 3 **ilk çağrıda patlıyordu**.

🔴 **Kural 7'nin yeni bir ihlal biçimi:** üretici var, yazılı, ve *koşmuyor*.
Var olan kapılar bunu göremiyordu — D11 betiklerin **içe aktarılabildiğini**
sınıyor (bu betik içe aktarılabiliyordu; hata koşarken çıkıyor), D15 ise
**terk edilmiş** üreticileri arıyor (bu terk edilmiş değil, kırık).

**Ve tablo ikinci kez çürüdü:** ölçtüğü graf 280 m'lik **teşhis diskiydi** —
K-096 tam da o diskin veri yolunda hiçbir yeri kapamadığını ölçmüştü.

| | kodda yazan | **bugün, aynı disk** | **kanal grafiği** |
|---|---|---|---|
| statik, tam bağlı zaman | %73,3 | **%0,0** | 270/270 TEK PARÇA |
| hareketli, tam bağlı zaman | %82,4 | **%0,0** | — |
| derece | 7,41 | **2,53** | **8,76** |
| bağlı yerleşim (500 tohum) | %78,2 | **%0,0** | — |

Betik onarıldı, koşuyor, ve çıktısının her bölümü artık `TESHIS GRAFIGI`
etiketi taşıyor. Sayıları `sim2/`de dört yerde gerekçe olarak duruyordu;
dördü de düzeltildi.

### 🔴 Ve bir "zorunlu" mekanizmanın hem gerekçesi hem kendisi yokmuş
Tablo iki kararı taşıyordu. Biri **düştü**:

> *"Statik kolda tohumların %26,7'si tamamen kopuk; bu yüzden U1 **bağlı
> tohum süzgeci** kullanır — statik kolda bu süzgeç ZORUNLUDUR."*

· **Süzgeç hiçbir yerde uygulanmamış.** Beş dosyada beyan ediliyordu, kodda
  tohum eleyen tek satır yok. Klasik *"bildirim ≠ kullanım"*.
· **Gerekli de değil.** Kanal grafiğinde statik kol 270/270 anda tek parça,
  yalnız düğüm 0. Çalışma noktası (1800 m) zaten *"kopukluğun sıfır kaldığı
  en büyük alan"* ölçütüyle seçilmişti — kopukluğun sıfır olması o seçimin
  **sonucudur**, ayrıca sağlanması gereken bir koşul değil.

⭐ Öteki karar **ayakta ama gerekçesi değişti**: *"hareketli kolda PDR ≈ 1
imkânsız"* doğru, ancak dayanağı artık bu tablo değil, bugün ölçülen kâhin
tavanı (0,917 · 0,831 — `pdr_tavani.py 1`).

## 🔴 "TAVAN" KÂHİNİ BİR TAVAN DEĞİL

*Üretici: `python -u kalibrasyon/bag_kumesi.py d` (15 tohum)*

`pdr_tavani.py` `EnGuvenilirKahin` için şunu diyor: *"GERÇEK TAVAN BUDUR:
hiçbir protokol daha iyisini yapamaz."* **Evrensel bir cümle ve çürüdü.**

| eşik | atlama kâhininin ETX kâhinini GEÇTİĞİ tohum |
|---|---|
| 0,70 | 0/15 |
| 0,80 | 1/15 |
| **0,90** *(bugünkü)* | **2/15** |
| 0,95 | 1/15 |
| 0,99 | **6/15** |

🔒 **Sebep fiziksel:** ETX **beklenen iletim sayısını** küçültür, **teslimi**
değil. Yeniden deneme sınırı **sonlu** (5 deneme) olduğu için ikisi ayrışır —
toplam ETX'i düşük bir yol, içinde beş denemede de geçemeyen bir bağ
taşıyabilir. Karıştırma altında ayrışma büyüyor.

⚠️ **Kol ortalamasında ETX kâhini her eşikte önde** (ölçüt bedeli hiçbir
eşikte negatife dönmüyor: +0,085 … +0,011). Yani düzeltme *"daha kötü"*
değil, **"üst sınır değil"**. Aynı düzeltme K-096'da atlama kâhinine
yapılmıştı, farklı bir sebeple; şimdi sırası ETX kâhininde.

🔴 Sonucu: `pdr_tavani.py`nin ürettiği sayılar bir **tavan değil, bir kâhinin
performansı**. Faz 3'te bir protokol o sayıyı geçerse bu bir kusur işareti
DEĞİLDİR.

## 🔴 KAPININ KÖR NOKTASI — ve onu kendi kaydım ortaya çıkardı

Yeni aletin `GUCLER = (−30,0 … −6,0)` sabiti köken defterine yazıldı ve D12
onu **"ölü kayıt"** ilan etti — yani tarayıcı o sabiti **hiç görmüyordu**.

🔒 Sebep: `−15.0` AST'de bir `Constant` **değildir**, `UnaryOp(USub,
Constant)`tır. Kalibrasyon tarayıcısı tablo elemanlarına **doğrudan**
bakıyordu; D12'nin kendi yardımcısı ise `ast.walk` ile **iniyor**. Yani aynı
kural iki yerde ayrı yazılmış ve **yine ayrışmıştı** — bu dosyada **ikinci
kez** (birincisi muafiyet kuralıydı, K-109).

⚠️ **Ve kaçış SESSİZDİ:** kaydı yazmasaydım `GUCLER` defterin dışında kalır,
hiçbir kapı konuşmazdı. Yalnız negatif sayılardan oluşan her tablo ve her
negatif skaler aynı yoldan kaçabilirdi.

🔒 Düzeltme tek kaynağa bağlandı: `_skaler_sayi_mi` eklendi ve tablo denetimi
D12'nin yardımcısını çağırıyor. Tarama 32 → **33** sabit.

## 🔴 ÜÇ ÖLÇÜT HATAM — üçü de ölçüm sırasında çıktı

1. **Yanlış toleransı kullandım.** Sönümleme örnek sayısını, *kolların
   derecesini eşitlemek* için ilan edilmiş 0,3 toleransıyla karşılaştırdım.
   O tolerans o karara ait. K'nin beslediği asıl karar kâhin kollarının
   PDR'si ve onun toleransı R = 0,036. Bölüm C duruyor (grafik düzeyindeki
   resim), ama **karar bölüm E'den çıkıyor**.
2. **İki kova kullandım, üç olmalıydı.** *"Kendi bandının üstünde"* ile
   *"çözünürlüğün üstünde"* ayrı sorulardır. İlk yazımda çözünürlüğün
   üstünde ama kendi bandının içinde olan bir etkiyi `DUYARLI` sayıyordum —
   yani karar verilemeyen bir şeyi mahkûm ediyordum. K-107'nin `KARAR YOK`
   kovası eklendi.
3. **Bir türetme denedim ve dejenere çıktı.** *"Çapadaki bağ tanım gereği
   kullanılabilirdir"* diyerek eşiği güç çapasından türetmeyi denedim.
   Ölçüldü: çapada (280 m) atlama başarısı **tam 1,0000** — geçiş 476 m'de
   başlıyor, 588 m'de 0,30, 644 m'de sıfır. Ölçüt hiçbir eşik vermiyor.

⚠️ Ayrıca 5 tohumla koşulan ilk sınavda ölçüt bedeli 0,99'da **−0,020**
görünüyordu ve *"tavan kâhini daha az teslim ediyor"* diye rapor edildi.
15 tohumda **+0,011** çıktı: o negatif değer **gürültüydü**. Düzeltildi.

## BUNU NE DEĞİŞTİRİR

- `ATLAMA_ESIGI` **`OLCULMUS`** oldu; köken borcu **43 → 42**.
- Bağlantılılığın karar taşıyan ölçümü artık **kanal grafiğinde**; teşhis
  diskinin sayıları etiketlendi ve gerekçe olmaktan çıkarıldı.
- *"Bağlı tohum süzgeci"* beyanı **kaldırıldı** — ne vardı ne gerekiyor.
- `pdr_tavani.py`nin *"tavan"* iddiası **daraltılmalı** (bu kayıtla açık borç).
- Mimari denetiminin kalibrasyon tarayıcısı artık negatif sayıları görüyor.
- 🔴 Devreden iş: **Θ'nın kanal tabanlı çapraz kontrolü** — alet hazır,
  ölçüm henüz koşulmadı.

## 🔴 EK 1 — SÖNÜMLEME ÖRNEK SAYISI: ARA SONUCUM GERİ ALINDI

*Üretici: `python -u kalibrasyon/bag_kumesi.py c e`*

**Bölüm C (grafik düzeyi)** kestiricinin kendi gürültüsünü DERECE biriminde
ölçtü — aynı tohum, aynı dünya, yalnız örnekleme fazı kaydırılmış:

| K | 4 | 8 | 16 | 32 |
|---|---|---|---|---|
| derece yayılımı | 0,65 | 0,40 | 0,25 | 0,25 |

Bunu görev kolu eşitlemesinin 0,3 toleransıyla karşılaştırıp *"K = 6
yetersiz, 16 gerekli"* dedim. 🔴 **O tolerans BAŞKA bir karara aittir.**
K'nin beslediği asıl karar kâhin kollarının PDR'sidir ve onun kendi
toleransı deneyin çözünürlüğü R = 0,036'dır.

**Bölüm E (kararın kendi birimi)** aynı gürültüyü PDR'de ölçtü
(`bagimsiz-surekli`, 3 tohum, 4 faz):

| K | 4 | 8 | 16 |
|---|---|---|---|
| PDR yayılımı (ortalama) | 0,071 | 0,030 | 0,045 |

🔴 **TEKDÜZE DEĞİL** ve üçü de R mertebesinde. K = 16, K = 8'den KÖTÜ çıkıyor —
bu bir sıralama olamaz, üç tohumluk bir yayılım kestiricisinin gürültüsüdür.

🔒 **İKİ ÖLÇÜM BİRLİKTE OKUNUNCA MEKANİZMA ÇIKIYOR:** grafik kestirimi K ile
düzeliyor (0,65 → 0,25) ama **rota seçimi düzelmiyor**. Yani daha iyi bir bağ
kalitesi tahmini, daha KARARLI bir yol seçimi üretmiyor: yakın maliyetli
rotalar arasındaki eşitlikler küçük tahmin değişimleriyle yer değiştiriyor.
Tek başına hiçbiri bunu söylemezdi.

**KARAR: K = 6'da BIRAKILDI.** Gerekçe *"6 en iyisi"* değil, **"büyütmenin
ölçülebilir bir faydası yok"**. Kova `SINANMAMIS` → **`DUYARSIZ`**.

⚠️ Üç sınır beyan edilir: PDR ölçümü yalnız **3 tohum** (yayılım
kestiricisinin kendisi gürültülü, K eğrisi çözülmedi) · iddia yalnız taranan
aralık için (4…16) · fazlar örnekleme adımı oynatılarak üretildiği için ilk
örnek bütün fazlarda ortak, yani ölçülen gürültü ~1/K kadar **eksik**.

## 🔴 EK 2 — `kopma_fiziksel` HİÇ SAYILMIYORDU: RİSK 3'ÜN NİCEL YARISI ÖLÜYDÜ

Sayaç kaydı `kopma_fiziksel`i *"SINR eşiği altına inen bağ"* diye tanımlıyor
ve üstüne `algilama_duyarliligi = kopma_algilanan / kopma_fiziksel` türevini
kuruyor. `gozlem/karar.py` bunu **Risk 3'ün** panzehiri diye ilan ediyor:
hiç beyan etmeyen bir protokolün sayacı 0 çıkar ve *"hiç kopma yaşamadı"*
gibi görünür.

🔴 **O payda hiç sayılmıyordu.** Canlı bir sonuç satırında ölçüldü:
`kopma_fiziksel = 0`, dolayısıyla `algilama_duyarliligi = None`.
`RotaDefteri.fiziksel_kopma()` yalnız **testlerden** çağrılıyordu.
`dunya/topoloji.py` bunu bir *"AÇIK TAAHHÜT"* olarak yazmıştı — yani
biliniyordu, ama Faz 2/3'e girerken kapanmamış olacaktı.

🔒 **UYGULANDI** (`olcum/kopma.py`) ve dört karar sıfır serbest parametreyle:

| karar | gerekçe |
|---|---|
| **son işlem** — koşu bitince sayılır | konum ve gölgeleme zamanın SAF fonksiyonları; sıcak yola dokunmuyor. Ölçüldü: **1,4–1,7 s**, koşunun %1'i |
| **ızgara = evre ızgarası** (1 s, RFC 3561) | ikinci bir ızgara sabiti iki sabitin ayrışabilmesi demekti |
| **karıştırıcı HARİÇ** | `surekli_darbeli` 2,7 s periyotla salınıyor, `taramali` 100 ms konakla. 1 s ızgarada her salınım "kopma" sayılır, payda şişer ve **her protokol körmüş gibi** görünürdü |
| **ilk ızgara noktası kopma saymaz** | başlangıç koşulu (`03` kural 14) |

⚠️ **BEYAN EDİLEN BEDEL:** `algilama_duyarliligi` böylece bir **topoloji
çalkantısı algılama** ölçüsüdür, **karıştırma algılama** ölçüsü DEĞİL.
Karıştırmanın etkisi evre metrikleriyle ölçülüyor; orası onun yeri. Bu ayrım
sonuç bölümünde yazılmalıdır.

🔒 **KENDİ KAPISINI TAŞIYOR:** statik kolda sonuç **tam olarak sıfır** olmak
zorunda — konumlar değişmez, gölgeleme konuma bağlıdır, hızlı sönümleme
dışarıdadır. Ölçüldü: statik **0**, hareketli **8** (kısa koşu) / **49**
(tam pencere). Ve `algilama_duyarliligi` `None`'dan **0,000**'a döndü: koşum
aleti sekiz gerçek kopmanın sıfırını görüyor — Risk 3'ün kapısı artık nicel
olarak konuşuyor.

## SAYAÇ — bu oturumun sonu

- köken borcu **43 → 40** · `DUYARSIZ` 15 → **17** · `OLCULMUS` 10 → **11**
- **474 test geçiyor** · `Yapisal ihlal YOK` · ölü köken kaydı 0

## 🔴 EK 3 — Θ YENİDEN TÜRETİLDİ: HIZLAR AYNI, GEREKÇE DEĞİŞTİ, MARJ DARALDI

*Üretici: `python -u kalibrasyon/bag_kumesi.py f g h`*

### Önce bir artefaktı rapor etmekten döndüm

Kâhin grafiğinde ölçülen ilk sonuç **Θ = 0,20** idi — sert diskteki 5,93'ün
otuzda biri. Rapor edilseydi *"çekirdek mobilite kolu yasak bölgede"* denecek
ve hızlar boşuna düşürülecekti.

🔒 **ŞÜPHE ÖLÇÜLDÜ:** kâhin grafiği hızlı sönümlemeyi K örnekle ORTALIYOR ve o
ortalama her ızgara adımında BAĞIMSIZ yeniden çekiliyor (sönümleme ~1,7 ms'de
dekorele olur). Yani bağlar dünya değiştiği için değil, **kestirim titrediği
için** kopuyordu. Ayıran ölçüm sönümlemeyi kapatmaktı:

| bağ tanımı | atlama | τ | **Θ** |
|---|---|---|---|
| sert disk 400 m | 6,10 | 89,0 s | **5,93** |
| yavaş SINR *(geometri + gölgeleme + anten)* | 5,58 | 43,2 s | **2,88** |
| kâhin grafiği, sönümleme **KAPALI** | 2,79 | 78,1 s | **5,21** |
| kâhin grafiği, sönümleme **AÇIK** | 2,76 | **3,0 s** | **0,20** |

🔴 **Son iki satırın tek farkı sönümleme ve Θ 26 kat değişiyor.** Kâhin
grafiği bir ROTA SEÇME aletidir; bir ÖMÜR ölçme aleti değildir. Bu ayrım
kayda geçer: aynı grafik, iki farklı soru için aynı derecede geçerli değil.

⭐ Ve vaat edilen doğrulama sonuç verdi: sönümlemesiz kanal grafiği (5,21) ile
sert disk (5,93) %14 içinde — **disk yaklaşımı SIRALAMA için tutuyor.**

### İki kestirici yanlılığı da giderildi

`calkanti.py`nin kestiricisi iki yönden de AŞAĞI yanlıydı ve ikisi de Θ'yı
düşük gösteriyordu:

  · **soldan kesme** — t = 0'da zaten var olan rotanın geçmiş yaşı bilinmiyor
    ama ömür sayılıyordu. 🔒 Çözüm YAPISAL: her çiftin **ilk ömrü atılıyor**;
    sonrakiler gözlem içinde doğduğu için yaşları tam.
  · **sağdan sansür** — koşu bitince yaşayan rota "ölmüş" sayılıyordu ve
    sansürlenenler tam da UZUN ömürlüler. 🔒 Çözüm **Kaplan–Meier** (RMST);
    serbest parametre yok.

### Türetme yeniden koşuldu — ölçüt K-101'in biçiminde

    sert kısıt : Θ ≥ 3 (K-101 kapısı) VE ölçekli hız 30–400 km/h (`02` A5a)
    amaç       : bu kısıtlar altında ÇALKANTIYI EN BÜYÜK yapmak

| hız (m/s) | τ ham | **τ (KM)** | sansür | **Θ** | 1:50'de | kapı | ölçek |
|---|---|---|---|---|---|---|---|
| 1,0–3,0 | 12,7 | 13,6 | %3,9 | 0,91 | 180–540 | kalır | 🔴 |
| 0,5–1,5 | 22,4 | 26,7 | %8,8 | **1,78** | 90–270 | **kalır** | evet |
| **0,25–0,75** | 38,8 | **48,8** | %15,3 | **3,25** | **45–135** | **GEÇER** | **evet** |
| 0,12–0,36 | 62,3 | 86,2 | %28,5 | 5,75 | 22–65 | geçer | 🔴 |

🟢 **SEÇİM DEĞİŞMEDİ: 0,25–0,75 m/s.** İki sert kısıtı da geçen TEK aday —
bir üstü kapının altında, bir altı ölçek aralığının dışında.

🔒 **SANSÜR DÜZELTMESİ TAŞIYICIDIR:** ham ortalamayla Θ = 2,59 çıkar ve
çekirdek kol **kapıyı geçemezdi**. Kaplan–Meier burada süsleme değil,
kararın kendisidir.

⚠️ **MARJ DARALDI:** 5,93 yerine **3,25**, yani kapının yalnız **%8** üstünde.
Çalışma noktasını değiştiren her şey — alan, güç, gölgeleme σ'sı — bu marjı
yeniden sınamayı gerektirir. Eskiden marj %98'di ve bu yüzden kimse
sınamıyordu.

### 🔴 VE BİR KOL KAPININ ALTINA DÜŞTÜ

Keşifsel **yüksek çalkantı** kolu (0,5–1,5 m/s) kayıtta *"Θ = 3,33 · zorlayıcı
ama adil"* diye duruyordu. Doğru tanımla **Θ = 1,78**.

K-101'in kuralı net: *kapının altına düşen bir kol, protokolü tasarım
zarfının DIŞINDA koşturuyor demektir ve **bulgu olarak raporlanır,
gizlenmez***. Bu kol ön-kayıtta ya öyle beyan edilir ya çıkarılır —
🔴 **öğrenci kararı, açık bırakıldı.**

### Bunu ne değiştirir

- `gm_hiz_min_ms` · `gm_hiz_maks_ms` üreticisi `calkanti.py` → `bag_kumesi.py §H`.
- `ETKIN_YARICAP_M` bir KARAR taşımıyor artık → `SINANMAMIS` → **`DUYARSIZ`**.
  Θ bir yarıçap seçimine değil, kanalın kendi tanımına dayanıyor.
- `calkanti.py` bir HIZLI TARAMA aleti; ürettiği Θ bir **teşhis**.
- Köken borcu **43 → 39**.

## 🔴 EK 4 — BAĞLANTI BÜTÇESİ YEDİ SAYI DEĞİL: İKİ DEGENERASYON BULUNDU

*Üretici: `python -u kalibrasyon/bag_kumesi.py i j`*

Duyarlılık denetimi bağlantı bütçesini **baskın** ilan etmişti ve yedi sayı
gerekçe bekliyordu. Ama tabloda bir şey vardı: `sicaklik_k`,
`bant_genisligi_hz` ve `gurultu_figuru_db` **tam olarak aynı** etkiyi
veriyordu (−0,112). **Aynı sayının üç kez çıkması tesadüf değildir.**

### Degenerasyon 1 — gürültü tabanı bir BİRİM, bir parametre değil

🔒 AST taraması: üçü de `sim2/` içinde **yalnız gürültü tabanında** geçiyor.
Ve verici gücü gürültü tabanından TÜRETİLİYOR:

    Pt = N · β · PL(R)   ⟹   SINR(d) = Pt/PL(d)/N = β · PL(R)/PL(d)

**N tamamen sadeleşiyor.** Düğümler arası girişim de ∝ N olduğu için o da;
taşıyıcı dinleme eşiği N'dir ve karşılaştırdığı güçler ∝ N. Geriye **tek
kalıntı** kalıyor: karıştırıcının MUTLAK gücü, yani **J/N** — ve o ρ ile
kalibre ediliyor.

🔴 **Yanlışlanabilir tahmin:** gürültü tabanını X dB yükselt + karıştırıcıyı
X dB yükselt → sonuç **birebir aynı**.

| oynatma | derece | kenar | kenar kümesi |
|---|---|---|---|
| taban | 6,650000000 | 133 | — |
| gürültü figürü 6→9 dB | 6,650000000 | 133 | **BİREBİR AYNI** |
| sıcaklık 290→580 K | 6,650000000 | 133 | **BİREBİR AYNI** |
| bant 2→4 MHz | 6,650000000 | 133 | **BİREBİR AYNI** |
| frekans 2,4→4,8 GHz | 6,650000000 | 133 | **BİREBİR AYNI** |

🔒 Bunlar **fizik parametresi değil, birim seçimi**: değerleri yalnız
*−15 dBm ne demek* sorusunu tanımlıyor.

⭐ **Frekansın sadeleşmeyen yarısı ayrıldı:** yol kaybı yarısı sadeleşiyor,
**Doppler** yarısı sadeleşmiyor. Aynı oynatma statik kolda Jaccard **1,0000**,
hareketli kolda **0,9254** ve derece farkı **0,10** — ilan edilmiş derece
toleransının (0,3) altında. Yani −0,234'lük ölçülen etkinin ağırlıklı kısmı
karıştırıcı ölçeği artefaktıydı.

### Degenerasyon 2 — menzil çapası bir UZUNLUK BİRİMİ

Aynı cebir: `SINR(d) = β·(R/d)^α`, yani yalnız **R/d oranı** belirleyici.
Bütün uzunluklar λ ile ölçeklenip karıştırıcı `10α·log10(λ)` dB telafi
edilirse sonuç değişmemeli.

| ölçek λ | karıştırıcı | derece | kenar | Jaccard |
|---|---|---|---|---|
| 1,25 | +1,938 dB | 6,650000000 | 133 | **1,0000** |
| 2,00 | +6,021 dB | 6,650000000 | 133 | **1,0000** |

🔒 `iletim_menzili_m` bağımsız bir sayı **değil**; belirleyici büyüklük
`menzil/alan` oranıdır ve **alan zaten o oranı sabitleyen bir ölçütle
seçildi**. Duyarlılık denetiminin −0,655'i (en büyük etki) tam olarak bunun
sonucudur: R'yi tek başına oynatmak oranı oynatır.

### 🔒 Sonuç: yedi sayı → **iki** gerçek soru

    sicaklik_k · bant_genisligi_hz · gurultu_figuru_db · frekans_hz
    iletim_menzili_m                                    → TÜRETİLMİŞ (5)
    dugum_sayisi                                        → KAPSAM (aşağıda)
    rician_k_db                                         → hâlâ açık

### `dugum_sayisi` — fizik boşluğu değil, onaylanmamış bir kapsam kararı

N boyutsuzdur, ölçekle sadeleşmez. Ölçüldü, iki aşamada:

1. **Yoğunluk sabit tutulursa derece SABİT KALMIYOR** (6,23 → 7,92 → 9,98).
   Sebep sınır etkisi: kenardaki düğüm oranı ∝ 1/√N azalıyor.
2. **Derece eşitlenirse geriye TEK etki kalıyor: DERİNLİK.**

| N | alan | derece | ort. atlama | en uzak |
|---|---|---|---|---|
| 20 | 1100 m | 7,90 | **1,64** | 3 |
| **40** | **1800 m** | **7,92** | **2,22** | **5** |
| 80 | 3000 m | 7,35 | **3,12** | 8 |

🔒 **ALT SINIR ÖLÇÜLDÜ:** N = 20, eşitlenmiş derecede 1,64 atlama veriyor —
şartnamenin **açıkça reddettiği** sığ rejim (§09.4: *"bu farkın yokluğu
değil, SORUNUN yokluğu"*).
🔒 **ÜST SINIR ÖLÇÜLDÜ:** N = 80 koşu başına **2,34 kat** maliyet
(60,8 / 126,9 / 297,2 s).

⚠️ Ölçüm bir BAND verir, tek sayı vermez. 40 o bandın içinde ve incelenen
sürü büyüklüğüdür. `03` kural 12 gereği **öğrenci onayı bekliyor** — ve bu,
bir araştırma sorusu değil **tek satırlık bir karar**.

### Bunu ne değiştirir

- Köken borcu **43 → 34**. Beş baskın sayı **cebirle türetilip ölçümle
  birebir doğrulandı** — bir kaynak gösterilerek değil.
- 🔴 **FAZ 4 İÇİN TASARIM KISITI, burada doğdu:** gürültünün MUTLAK değeri
  bu simülatörde anlamlı bir büyüklük **değildir** (serbest bir ölçek). Gözlem
  penceresi `olculen_gurultu_w`u protokole veriyor; onu **mutlak bir eşikle**
  karşılaştıran bir protokol, fizikte karşılığı olmayan bir sayıya dayanmış
  olur. Karıştırma sezimi **oranla ya da değişimle** yapılmalıdır.
- ⚠️ Beyan edilen model sınırı: bu modelde bant genişliği ile bit hızı
  **bağımsız** parametrelerdir; gerçekte bağlıdırlar.

## 🔴 EK 5 — "SİMÜLATÖR PROTOKOLÜ KISITLAMAZ" GÜVENCESİNİN KANITI BOŞTU

*Üretici: `python -u kalibrasyon/bag_kumesi.py k l`*

Şartname §09.6 aletin protokollere haksız bir sınır koymadığını **güvence**
olarak veriyor ve kanıtı şu tabloydu:

    TTL ile düşen 0 · kuyruk taşması 0 · en yüksek kuyruk 3/50

🔴 O sayılar `dogrudan_komsu` koşum aletiyle üretilmiş ve o alette
**`aktarilan_paket = 0`** — tek bir paketi bile ara düğümde ileri
iletmemiş. Sonuç satırından okundu: üretilen 12 799 · teslim 5 114 ·
`hedef_yok` ile düşen **6 548** · tepe kuyruk doluluğu **1/50**.

🔒 **TTL yalnız aktarmada azalır; kuyruk yalnız aktarmayla dolar.** Yani o
test, parametreler ne olursa olsun **sıfırdan başka bir şey üretemezdi.**
Geçmiş görünen ama hiçbir şey sınamayan bir kapı — 8 Eylül'ün *"kapalı
karıştırıcıyı ölçen tablo"* hatasının aynı sınıfı.

⭐ Aynı ölçüm, çok atlama üreten koşum aletiyle: **kuyruk 50/50 DOLU ·
226 taşma · 162 TTL ölümü · 25 yakalama**. Mekanizmalar gerçekten bağlıyor;
sadece o alet onlara hiç dokunmuyordu.

### Düzeltme bir sayı değil, bir ÖN KOŞUL

Kapı üç durumlu yapıldı — *geçti/kaldı* değil:

| durum | verdikt |
|---|---|
| `aktarilan_paket = 0` | **KOŞULMADI** — test boş |
| aktarma var · marj geniş | GEÇTİ |
| aktarma var · marj dar | 🔴 KISITLIYOR |

Ve **marj raporlanır, sayım değil**: *"TTL ölümü 0"* bir yokluk;
*"en uzun yol 5 atlama, TTL 32, marj 6,4×"* bir kanıt.

### İki kayıt düzeltildi

- 🟢 **`ttl_baslangic` → `TURETILMIS`.** Yapısal kanıt: döngüsüz bir
  yönlendirmede yol uzunluğu ağ **çapını** aşamaz. Çap ölçüldü (§J):
  N = 40'ta en uzak çift **5 atlama**. TTL 32 → marj **6,4×**. TTL yalnızca
  DÖNGÜ olduğunda bağlar, ki var olma sebebi odur.
  ⚠️ Eski gerekçe İKİ kez yanlıştı: *"ağ çapı ~3"* **teşhis diskinden**
  geliyordu (K-096'da geçersiz ilan edilen graf), ve *"hiç bağlamıyor"*
  iddiası `aktarilan_paket = 0` olan koşumdan.
- 🔴 **`kuyruk_kapasitesi` açık kalıyor** ama gerekçesi düzeltildi. İki koşum
  aleti soruyu **bracketliyor ama cevaplamıyor**: biri mekanizmaya hiç
  dokunmuyor, öteki kasten döngü üretip patolojik olarak zorluyor. Verdikt
  **Faz 3'te**, gerçek bir taban çizgisiyle.

### ⚠️ VE DUYARLILIK DENETİMİNİN BEYAN EDİLMEMİŞ BİR SINIRI ÇIKTI

K-107 üç sınır beyan etmişti: OAT · yalnız çalışma noktası çıktıları · kasten
asimetrik ölçüt. **Dördüncü bir sınır vardı ve yazılmamıştı:**

🔴 **Denetim her şeyi KÂHİN kollarında ölçtü** — yönlendirmenin kusursuz
olduğu bir dünyada. Kuyruk kapasitesi, TTL ve yakalama eşiği ancak
yönlendirme KÖTÜ olduğunda bağlar. Kusursuz bir kolda tanım gereği
görünmezler ve parmak izi değişmez — yani `OLCULEMEDI` okunurlar.

🔒 K-107 bu tuzağı KENDİSİ tarif etmişti (*"OLCULEMEDI aklama değildir; canlı
olduğu bir kolda yeniden taranmalı"*) ama uyguladığı ayrım yalnız
**karıştırıcı sınıfı** ekseniydi — protokol kalitesi ekseni gözden kaçtı.
`bag_kumesi.py §L` o taramayı stres altında yapıyor.

## 🔴 EK 6 — STRES TARAMASI: DÖRT ETİKET YANLIŞ KOLDAN GELMİŞ

*Üretici: `python -u kalibrasyon/bag_kumesi.py l`*

K-107 dokuz parametreyi `OLCULEMEDI` işaretledi ve kendi uyarısını yazdı:
*"aklama değildir; canlı olduğu bir kolda yeniden taranmalı."* Uyguladığı
ayrım yalnız **karıştırıcı sınıfı** ekseniydi. **Protokol kalitesi ekseni
gözden kaçtı** — ve denetim her şeyi KÂHİN kollarında ölçtü, yani
yönlendirmenin kusursuz olduğu bir dünyada.

🔒 Kuyruk kapasitesi, TTL ve yakalama eşiği ancak yönlendirme **kötü**
olduğunda bağlar. Kusursuz bir kolda tanım gereği görünmezler.

| oynatma | PDR | fark | verdikt |
|---|---|---|---|
| TABAN | 0,18531 | — | |
| kuyruk_kapasitesi ×2 | 0,18531 | +0,00000 | 🔴 CANLI |
| kuyruk_kapasitesi ×0,5 | 0,16277 | −0,0225 | 🔴 CANLI |
| **ttl_baslangic ×0,5** | **0,39149** | **+0,206** | 🔴 **CANLI** |
| ttl_baslangic ×2 | 0,21285 | +0,0276 | 🔴 CANLI |
| yakalama_esigi_db ×2 | 0,18531 | +0,00000 | 🔴 CANLI |
| yakalama_penceresi ×2 | 0,18531 | +0,00000 | 🔴 CANLI |
| **cw_max ×0,5 (511)** | 0,18531 | +0,00000 | **ÖLÇÜLEMEDİ** |

### 🔴 Bir kaydımı AYNI GÜN İÇİNDE geri aldım — ve sebebi kayda geçer

Bu taramadan **saatler önce** `ttl_baslangic`i `TURETILMIS` yapmıştım.
Türetme şuydu: *döngüsüz bir yönlendirmede yol uzunluğu ağ çapını aşamaz;
çap 5 atlama ölçüldü, TTL 32 → marj 6,4×.*

🔒 **O türetme AYAKTA — ama yalnızca bir ALT SINIR veriyor (TTL > çap),
DEĞERİ vermiyor.** Ve değer önemli çıktı: TTL'i yarıya indirmek PDR'yi
**0,185'ten 0,391'e** çıkarıyor — deneyin çözünürlüğünün **5,7 katı**.
Mekanizma açık: döngüdeki paketler erken ölünce kapasite gerçek trafiğe
kalıyor.

⚠️ Kayıt `SINANMAMIS`a geri alındı. Bir alt sınırı değerin gerekçesi diye
sunmak, gerekçesiz bir sayıyı aklamaktır — bu projedeki en pahalı hata.

### 🟢 `cw_max` kapandı — aritmetik kanıt + stres altında doğrulama

Çekişme penceresi her başarısızlıkta `2c+1` oluyor; `cw_min = 31` ve yeniden
deneme sınırı 4 olduğundan dizi **31 → 63 → 127 → 255 → 511** ile duruyor ve
beşinci başarısızlıkta vazgeçiliyor. 1023 için **altı** katlanma gerekirdi.

Ölçüldü: 849 vazgeçme üreten bir koşumda `cw_max` 1023 → 511 değiştirildiğinde
parmak izi **birebir aynı**. Kova `SINANMAMIS` → **`TURETILMIS`**.

🔒 **KOŞULLU BİR ATALET ve koşulu bir KAPIYA bağlandı** (`mimari_denetimi`
D8): `en çok CW = 2^limit·(cw_min+1) − 1 < cw_max`. Yeniden deneme sınırı 5'in
üstüne çıkarsa kapı konuşur ve köken kaydı sessizce yanlışlaşmaz.

### Kalan üçü

`kuyruk_kapasitesi` · `yakalama_esigi_db` · `yakalama_penceresi_s` — üçü de
**CANLI** ama PDR etkileri tek tohumda 0,000–0,023. ⚠️ Bu bir DUYARLILIK
ölçümü DEĞİL, bir **CANLILIK** ölçümüdür: tek tohum, hata payı yok. Verdikt
Faz 3'te, gerçek taban çizgileriyle ve tohumlarla verilir.

## 🔒 EK 7 — RICIAN K: BİR TUTARSIZLIK ŞÜPHESİ, DÜŞÜŞÜ VE GERİYE BIRAKTIĞI DENKLİK

*Üretici: `python -u kalibrasyon/bag_kumesi.py m`*

### Şüphe

Sönümleme modelinin iki sayısı birbirine bakınca çelişir görünüyordu:

- `yol_kaybi_usteli = 2` — gerekçesi *"hava-hava, yer yansıması önemsiz"*.
- `rician_k_db = 6` — anlamı: **saçılan güç, doğrudan görüşün dörtte biri.**

🔴 Biri yansımayı yok sayıyor, öteki onu %25 seviyesinde tutuyordu. İki sayı
aynı fiziği farklı anlatıyorsa, en az biri yanlıştır.

### Şüphe düştü — ve çelişki değil, iş bölümü çıktı

İki-ışın geometrisinde **kırılma mesafesinin altında** alan, serbest uzay
değerinin **etrafında salınır**; üstünde α = 4'e döner. Bu bağlantılar
(≈ 280 m, irtifa 20–120 m, 2,4 GHz) kırılmanın **altında**.

🔒 Yani: **α = 2 salınımın ORTALAMASINI, Rician SALINIMIN KENDİSİNİ
modelliyor.** Aynı işi iki kere yapmıyorlar, birbirini tamamlıyorlar. Şüphe
haklıydı ama cevap "biri yanlış" değil, "ikisi farklı katman" çıktı.

### Geriye kalan: keyfî bir sayı değil, TEK bir bibliyografik kontrol

Baskın çok yol bileşeni yer yansımasıysa, güç oranı yansıma katsayısının
karesidir:

    P_yansıyan / P_doğrudan = Γ²   ⟹   K_dB = −20·log₁₀(Γ)

| K (dB) | Γ (denk) |
|---|---|
| 0 | 1,000 |
| 3 | 0,708 |
| **6** | **0,501** |
| 10 | 0,316 |
| 15 | 0,178 |

⭐ **K = 6 dB ⟺ Γ = 0,50.** Sayının statüsü değişti: *"hava-hava için K kaç
olmalı?"* gibi cevabı ölçüme bağlı belirsiz bir soru olmaktan çıkıp,
*"bu geometride yer yansıma katsayısı 0,50 mi?"* diye **tek ve net bir
literatür sorusu** oldu. Cevaplanınca kova `SINANMAMIS` → `KAYNAK` olur.

### Duyarlı mı? Evet — ve dejenere değil

| K (dB) | derece | Jaccard | p10 fade | p1 fade |
|---|---|---|---|---|
| 0 | 6,00 | 0,7448 | −8,57 | −18,86 |
| 3 | 6,20 | 0,8489 | −7,11 | −16,21 |
| **6** | **6,65** | **1,0000** | **−5,15** | **−11,61** |
| 10 | 7,10 | 0,8581 | −3,02 | −6,35 |
| 15 | 7,55 | 0,7317 | −1,57 | −3,12 |

Derece aralığı %26 — ilan edilmiş 0,3 derece toleransının çok üstünde.
🔴 Bu sayı **DUYARSIZ ilan edilemez**; gerekçesi gerçekten gerekiyor.

### ⚠️ VE BİR İŞARET ÇIKTI — KARAR DEĞİL

`golgeleme_sigma_db` şu ölçütle gerekçelenmişti: *sönümleme, PER'in
0,99 → 0,01 geçiş bandıyla (**3,44 dB**) aynı mertebede olmalı* — daha küçüğü
kozmetiktir, daha büyüğü fiziği bastırır.

Aynı ölçüt K'ya uygulandığında:

| K (dB) | p10 fade | geçiş bandına (3,44 dB) göre |
|---|---|---|
| 6 | 5,15 dB | 1,5× — bandın üstünde |
| 10 | 3,02 dB | ≈ 1,0× — banda oturuyor |
| 15 | 1,57 dB | 0,5× — kozmetik |

🔒 Yani projenin **kendi ölçütü** K ≈ 8–10 dB'yi işaret ediyor; 6 dB güçlü
sönümleme ucunda duruyor. ⚠️ Bunu **karar olarak yazmıyorum**: ölçüt σ için
kurulmuştu ve K'ya taşınması gerekçelendirilmedi. Bu bir **işaret**tir ve
`02`ye gidecek bibliyografik kontrole birlikte götürülür — kaynak 0,50'yi
onaylarsa 6 dB kalır, onaylamazsa işaret zaten yönü söylemiş olur.

🔒 Kayıt `SINANMAMIS` kalıyor. *"Artık sınanabilir"* ile *"sınandı"* aynı şey
değildir; ikincisini birincisi sanmak bu projedeki en pahalı hatadır.

---

# K-111 · 🔴 DÖRT ÖLÇÜM ALETİ KOŞMUYORDU — ve ön-kayıtın şart koştuğu bir yetenek hiç yokmuş

> **Tarih:** 9 Eylül 2026 (üçüncü oturum) · **Karar: ajan** · **Durum: UYGULANDI**
> 🔒 **Öğrenci kapsamı belirledi:** *"şu anlık simülatör fazında kalmaya
> devam etmek istiyorum."* Aşağıdaki teknik seçimler ajana aittir; kapsam
> ve gerçekçilik kararları öğrenciye açık kalmaya devam ediyor.
> **Üreticiler:** `python -u kalibrasyon/uretici_duman.py` ·
> `python kalibrasyon/calisma_noktasi.py` ·
> `python kalibrasyon/adim4_sonumleme.py` ·
> `python -u kalibrasyon/sonumleme_onbellegi.py 2`

## 0 · DEVRALINAN DOĞRULAMA LİSTESİ — SEKİZİ DE GEÇTİ

| ne | beklenen | ölçülen |
|---|---|---|
| test takımı | 474 passed | 🟢 `474 passed in 377.93s` |
| mimari denetimi | ihlal yok · borç 33 · duyarlılık 5 | 🟢 birebir |
| `bag_kumesi.py a` | G-a · G-b GEÇTİ | 🟢 |
| `karistirici_gucu.py tarama` | −15,0 dBm · ρ = 0,258 | 🟢 birebir |
| `denetim_ornekleme.py` | 30/30 · Jaccard 1,0000 · ρ farkı 0 · 270/270 | 🟢 birebir |
| `pdr_tavani.py 1` | 1,000·0,999·0,996 / 0,917·0,831 | 🟢 birebir |
| `adim9_kapanis.py` | korunum + mutabakat HEPSİ TAMAM | 🟢 6 tohum + 5 sınıf |
| `evre_metrikleri_kapilari.py` | dört kapı GEÇTİ | 🟢 G1·G2·G3·G4 |

Yani **devralınan sayıların hepsi ayakta** — sekiz maddenin sekizi de
bugün yeniden üretildi. Bulgular listenin *dışından*
çıktı — ve çıkış yolu, listenin kendisinin sormadığı bir soruydu:
*"defterin ANDIĞI üretici komutlar hâlâ koşuyor mu?"*

## 1 · 🔴 ASIL BULGU — dört üretici koşmuyordu, dördü de defterde ANILIYOR

K-110 bu sınıfı bir kez bulmuştu (`adim3_kapanis.py` — *"üretici var,
yazılı, ve koşmuyor"*), o betiği onarmış, **boşluğun kendisini açık
bırakmıştı**. Boşluk dört örnek daha verdi:

### 1.1 · `calisma_noktasi.py` — ÇALIŞMA NOKTASININ ÜRETİCİSİ, 4 gündür kırık

`Konfig` şunu istiyor: `2 × gorev_grup_yaricapi_m < alan`. K-097 (5 Eylül)
yarıçapı 250 → **650 m** yaptı; alan taramasının ilk ızgara noktası ise
**1000 m**. 2 × 650 = 1300 > 1000 → betik **bölüm 2'nin ilk çağrısında**
`DegismezHatasi` ile patlıyordu.

🔴 Bedeli: `alan_en_m` · `alan_boy_m` · `gorev_grup_yaricapi_m` — **üçü de
`OLCULMUS`** ve üçünün de gösterdiği üretici bu betik. Yani çalışma
noktasının kendisi dört gündür **yeniden üretilemiyordu**.

🔒 **ONARIM ÖLÇÜMÜ DEĞİŞTİRMEDİ, iki ayrı yoldan gösterildi.** Taranan
kollar `statik` ve `bagimsiz`; `mobilite_kur` müfreze yarıçapını YALNIZ
`gorev` kolunda okur. Ölçüldü: 6 tohum × 2 kol × 2 zamanda düğüm
konumlarının parmak izi, yarıçap 650 ↔ 400 m'de **BİREBİR AYNI**.

### 1.2 · `calisma_noktasi.py` — ikinci kusur: ölçüt 30 tohum diyor, varsayılan 6

Onarıldıktan sonra betik koştu ve **2000 m** dedi — kayıtta **1800 m**
yazıyor. Ölçüt satırı ise açıkça *"statik kolda kopukluk %0 (**30
tohum**)"* diyor; betiğin varsayılanı **6**'ydı ve defterin gösterdiği
üretici komut argümansız.

    6 tohum  → hiçbir alanda kopukluk görünmüyor → 2000 m
    30 tohum → 2000 m'de kopukluk %0,3 açılıyor  → **1800 m**

🔒 Sebep istatistikseldir, kod değil: kopukluk **nadir** bir olaydır ve
6 tohum onu göremez. **30 tohumla yeniden üretildi ve kayıt AYAKTA:**

| alan | kopukluk | derece | derin çift |
|---|---|---|---|
| 1600 | %0,0 | 10,42 | %19,7 |
| **1800** | **%0,0** | **8,67** | **%31,0** |
| 2000 | %0,3 | 7,15 | %42,8 |

⭐ `konfig.py`de yazan derece de tam olarak **8,67**. Sayı doğruymuş;
kırılan şey **yeniden üretilebilirliğiydi**. Varsayılan 30'a çekildi.

⚠️ Izgara yukarı da tarandı (2000…2800 m): kopukluk %0,3 → %1,6 → %2,4 →
%10,5. Yani 1800 m gerçekten bir **sınırdır**, ızgaranın kenarı değil.

### 1.3 · `adim4_sonumleme.py` — K-102'yi kaçırmış, 51 kat sapıyordu

`sonumleme_parca_suresi_s`in üreticisi. K-102 (8 Eylül) Doppler'i **tam
ölçek** hızına bağladı; betik **ölçekli** hızı kullanmaya devam etti:

    betigin ilan ettigi olcut : T_c(p99)/4
    betigin hesapladigi       : 38 666 µs / 4 = 9 666 µs
    KONFIGDEKI deger          :                  190 µs

İkisi yan yana basılıyor, fark **hiç açıklanmıyordu**. Ayrıca bölüm D
`KeyError: 'tavan'` ile çöküyordu *(önbellek raporunun şeması değişmiş,
betik güncellenmemiş)*. D15'in tarif ettiği tehlikenin tam kendisi:
*"sayıyı doğrulamak için onu koşturan biri başka bir cevap alır."*

🔒 **ÇÖZÜM İKİNCİ BİR FORMÜL DEĞİL, MODELİN KENDİSİ:** T_c artık
`Sonumleme.tutarlilik_suresi_s`ten okunuyor; ölçek dönüşümü tek yerde.
🟢 **Onarım sonrası: T_c(p99) = 773 µs → parça 193 µs ↔ koddaki 190 µs.**
Değer AYAKTA (%1,6 içinde), bayat olan gerekçesiydi.

⚠️ Bölüm C'nin saf formülü **kasten korundu**: orada ρ modelin çalışma
noktası değil, FIR'ı sınayan bir **girdi**dir. İkisi ayrı isimlendirildi.

### 1.4 · `sonumleme_onbellegi.py` — YANLIŞ ALARM, 8 Eylül'den beri

Bu betik önbellek sınırının zararsızlığını *"sonuç satırı birebir aynı mı"*
diye sınıyordu. K-106 sonuç satırına **önbelleğin KENDİ durumunu** ekledi
(`teshis.sonumleme_onbellegi`: sınır · tahliye · girdi · ıskalama). O alan
sınır değişince **tanım gereği** değişir → kapı o günden beri **her
satırda** `🔴 HAYIR` diyordu. Betik ~35 dk sürdüğü için kimse koşmamıştı.

🔒 Ölçüldü *(`bagimsiz-yok`, tohum 1000, 15 s, sınır 1e9 ↔ 100 000)*:

| ne | sonuç |
|---|---|
| ham teslim dizisi | **BİREBİR AYNI** |
| tam satır | farklı |
| `sonumleme_onbellegi` çıkarılınca | **BİREBİR AYNI** |

Yani önbellek gerçekten saf bir memo; **kırılan şey kapıydı.** K-109'un
kuralı burada geçerli: *doğru çalışan işi kırmızıya boyayan bir kapı,
kapısızlıktan kötüdür.* Alan karşılaştırmadan çıkarıldı, **rapordan değil**
— tahliye ve ıskalama sütunları sınırın fiilen devreye girdiğinin kanıtı.

🟢 **ONARIMDAN SONRA KAPI KOŞULDU ve artık BOŞ da geçmiyor:** dokuz
karşılaştırmanın dokuzu **EVET**, ve tahliye sayıları **7 · 31 · 78** —
yani sınır fiilen devreye girdi. *(Tahliye sıfır olsaydı kapı hiçbir şey
sınamamış olurdu; K-110'un `aktarilan_paket = 0` dersi.)*

## 2 · 🔒 BOŞLUK KAPATILDI — `kalibrasyon/uretici_duman.py`

Dört örnek bir sınıf yapar. Mevcut kapılar bu sınıfı **yapısal olarak**
göremiyor:

    D11  betiğin İÇE AKTARILABİLDİĞİNİ sınar — dördü de aktarılabiliyordu
    D15  TERK EDİLMİŞ üretici arar        — dördü de terk edilmiş değil, KIRIK

Yeni alet, defterin andığı **9 üreticinin** hepsini ucuz bir kesitle
koşturur ve çıkış kodunu raporlar. **Kapsam kapısı var:** defterde anılıp
kesiti tanımlanmamış bir betik bulgu üretir *(K-109: bir denetimin kapsamı,
denetlediği defterin kapsamından dar olamaz)*.

🔴 **İDDİA ETMEDİĞİ ŞEY BAŞLIKTA YAZILI:** duman koşusu *"betik koşuyor"*
der, *"sayıyı yeniden üretti"* **demez**. Örneğin `calisma_noktasi.py` 6
tohumla koşar ve 2000 m der; kayıttaki 1800 m 30 tohumun sonucudur. Her
satır kendi kesitini ve tam koşumun **bandını** taşır.

🔒 **VE ALETİN KENDİ KAPISI VAR** (`--kapi`, ~2 sn) — `bag_kumesi.py a` ile
aynı idiom. K-103'ün dersi gereği dört dalın dördü de sınanıyor ve dördü de
ateş ediyor: kırık bir koşum yakalanıyor *(ve SEBEBİ taşınıyor)*, sağlam
bir betik geçiyor *(yanlış alarm yok)*, kapsam kapısı konuşuyor, olmayan
dosya görülüyor. **Ateş etmeyen bir kapı, kapı değildir.**

## 3 · 🔴 A19 — ÖN-KAYIT, SİMÜLATÖRÜN YAPAMADIĞI BİR ŞEYİ ŞART KOŞUYOR

Tam kayıt: `07-SIMULATOR-TASARIMI.md` §17.2. Özeti:

Protokolün temas yüzeyinin **tamamı** dört kanca, **tek** periyodik beacon
ve üç canlı çerçeve tipidir. `06` §4.2 ise RREQ *(talep üzerine selleme)*,
RREP *(unicast kontrol)*, RERR *(olay tetiklemeli yayın)*, OLSR'ın iki ayrı
periyodu ve protokol zamanlayıcıları istiyor — ve **U2 uygunluk testi**
bunları kabul ölçütü yapıyor. `03` kural 4 eksik uygulamayı yasakladığına
göre, bugünkü yüzeyle **üç taban çizgisinin üçü de sadık yazılamaz.**

🔒 Bu bir **gözlem sözleşmesi ihlali değil**: `05` protokolün ne GÖRECEĞİNİ
kısıtlar, buradaki boşluk ne YAPABİLECEĞİ eksenindedir. `05` §A2 hakkı
zaten veriyor. Yapılacak iş sözleşmeyi genişletmek değil, **mekanizmasını
tamamlamak**.

⭐ Maliyeti düşüren üç ölçülmüş gerçek: faturalama sayaçları (`kontrol_*`,
`beacon_gonderilen`) **zaten var**; `kontrol` çerçeve tipi
`CERCEVE_TIPLERI`de **zaten tanımlı** *(ama hiçbir yerde kurulmuyor —
`bildirim ≠ kullanım`)*; kontrol çerçeveleri korunum defterine girmiyor.

🔴 **Bu boşluk ne şartnamede ne `DEVIR.md`de anılıyor.** Tek kaydı, emekli
`sim/` planına göre yazılmış ve *"süreleri geçersiz"* diye işaretlenmiş
`12-YOL-HARITASI.md` §0. Yani proje bunu **bir kez ölçmüş, sonra unutmuş**.

## 4 · 🟢 TERS TARAMA — ilk geçiş yapıldı

`07` §17.1 *"ters yön taranmadı"* diyordu. Yapıldı *(§17.3)*: 74 `Konfig`
alanı + 21 `sim2/` modül sabiti, bütün `v2/` belgelerinde adıyla arandı.
**20'si hiçbir belgede adıyla geçmiyor.** İki öbek önemli: **beş ablasyon
bayrağı** *(ikisi Li replikasyonunda fiilen kullanılıyor)* ve **görev
kolunun üç parametresi**. ⚠️ Yöntem **adı** arar, **kavramı** değil; liste
*"belgede yok"* değil *"belgede ADIYLA bağlanmamış"* listesidir.

## 5 · ⭐ GÖZLEM YÜZEYİNİN NE KADARI KULLANILIYOR — 24'te 5

*Üretici: `protokoller/*.py` + `kalibrasyon/kahin.py` AST nitelik taraması.*

Karar katmanı bugün gözlem penceresinin **24 alanından yalnız 5'ini**
okuyor *(`dugum` · `komsular` · `paket` · `hedef` ve komşunun `dugum`u)*.
🔴 Bir anti-jamming protokolünün ihtiyaç duyacağı alanların **hiçbiri**
okunmuyor: `olculen_gurultu_w` · `son_iletim_sonucu` · `kanal_mesgul_mu` ·
`duyulan_beacon` · `son_duyulma_s` · `kuyruk_uzunlugu`.

⚠️ Bu bir kusur değil, **projenin nerede durduğunun sayısıdır**: alet
ölçmek için var olduğu şeye henüz hiç dokunmadı. *(`05` belgesindeki
*"14 alan okunmuyor"* sayısı emekli depodan; bugünkü sayı 19/24.)*
⚠️ Yöntem üst sınır verir: tarama nitelik ADI eşler, tipini doğrulamaz.

## BUNU NE DEĞİŞTİRİR

- Dört üretici onarıldı; **hiçbir kayıtlı sayı değişmedi** — dördünde de
  ölçüm ayakta çıktı, bayat olan gerekçeler ve kapılardı.
- Yeni kapı: `uretici_duman.py`. Mühürden önce koşulması gereken listeye
  girer.
- 🔴 **Faz 3'ün önüne yeni ve büyük bir ön koşul yazıldı:** kontrol düzlemi
  yeteneği. Faz 2'nin dikey dilimi bundan **etkilenmez** — beacon taşıyan
  proaktif bir protokol bugünkü yüzeyle yazılabilir.
- Köken borcu **33** · duyarlılık borcu **5** · **474 test** · yapısal
  ihlal yok — hepsi değişmedi.

## 🔴 EK 1 — GÖREV KOLU: ÖLÇÜM BAYAT, VE ÖLÇÜTÜ SINAYAN ALET ÖLÇÜTTEN KABA

*Üretici: `python -u kalibrasyon/calisma_noktasi.py` §4 (8 tohum) +
genişletilmiş ızgara ve hata payıyla yeniden ölçüm (12 tohum).*

`gorev_grup_yaricapi_m = 650` **`OLCULMUS`** kovasında ve ölçütü şu:
*"ortalama dereceyi bağımsız kolunkiyle eşitleyen yarıçap, |Δderece| ≤ 0,3."*
Ölçüm 5 Eylül'de (K-097) yapıldı. **8 Eylül'de K-101 hızları ~40 kat
düşürdü** — ve bu kalibrasyonu üreten betik o tarihten beri kırıktı (§1.1),
yani **hiç yeniden koşulmadı**.

Bugün ölçüldü (12 tohum, t ∈ {50, 175, 320}):

| yarıçap | görev derecesi | fark | **birleşik 2SE** | verdikt |
|---|---|---|---|---|
| **650** *(kodda)* | 7,261 ± 0,305 | **0,557** | 0,689 | 🔴 toleransı aşıyor |
| 750 | 7,031 ± 0,261 | 0,326 | 0,612 | 🔴 aşıyor |
| 800 | 6,933 ± 0,247 | 0,229 | 0,589 | geçer |
| **850** | 6,688 ± 0,229 | **0,017** | 0,559 | geçer |

    bagimsiz-yok referans derecesi : 6,704 ± 0,161   (kayitta: 7,406)

🔴 **REFERANS BAYATLAMIŞ:** 7,406 → 6,704, yani **4,3 SE**lik bir düşüş.
Sebep K-101'in hız değişimi: hızlar 1/40'a inince düğümler başlangıç
yerleşiminin yakınında kalıyor ve derece dağılımı değişiyor. Kaydın
sayısı artık bugünün dünyasına ait değil.

## 🔴 VE ASIL BULGU: ÖLÇÜT, ONU SINAYAN ALETİN ÇÖZÜNÜRLÜĞÜNÜN ALTINDA

Tablodaki **birleşik 2SE sütunu 0,56–0,69** — yani ilan edilmiş toleransın
(**0,3**) **iki katı**. Bunun üç sonucu var ve üçü de yazılmalı:

1. **650'nin 0,557'lik sapması kendi hata payının İÇİNDE** (0,689). Yani
   *"650 yanlış"* denemez.
2. **850'nin 0,017'si de öyle.** Yani *"850 doğru"* da denemez — bu ızgarada
   yarıçaplar birbirinden **ayırt edilemiyor**.
3. 🔒 Dolayısıyla ölçüt **bu örneklem büyüklüğünde SINANAMAZ**. Bir eşik,
   onu ölçen aletin çözünürlüğünün altındaysa hiçbir şey söylemez —
   K-107'nin *"deneyin kendi çözünürlüğü"* dersinin aynısı, bu sefer
   derece biriminde.

⚠️ **Toleransı sınanabilir yapmak için gereken tohum sayısı ölçüldü:**
birleşik 2SE'yi 0,3'ün altına indirmek ~**3,5 kat** daha küçük SE ister,
yani **~140 tohum** *(bugünkü 12'nin ~12 katı)*. Görev kolu `07` §15/3'e
göre **keşifsel eksende** olduğuna göre bu, ölçülmüş bir maliyet–fayda
sorusudur ve **kapsam kararıdır** → 🔴 **öğrenciye açık.**

🔒 **YAPISAL BİR ÜST SINIR DA VAR:** `Konfig` `2r < alan` istiyor, yani
1800 m'lik alanda yarıçap **< 900 m**. Aranabilir aralığın tepesi ~850 m ve
bugünkü en iyi ızgara noktası tam orada — yani optimum, aramanın **kenarına
dayanmış** olabilir. *(Bu değişmez ölçüm sırasında bu ajanı da durdurdu:
r = 900 denemesi `DegismezHatasi` verdi.)*

🔒 **KOVA DEĞİŞMİYOR ama gerekçesi düzeltiliyor:** `OLCULMUS` etiketi
kalıyor çünkü bir ölçüm gerçekten yapıldı; ama kaydın yanına *"ölçüm
K-101 öncesi hız rejiminde yapıldı ve bugün referans derecesi 4,3 SE
kaymış durumda"* yazılmak zorunda. ⚠️ **Aksi hâlde bu, bir alt sınırı
değerin gerekçesi diye sunmakla aynı sınıfa girerdi** — K-110'un
`ttl_baslangic`te geri aldığı hata.

## 🔴 EK 2 — BEACON YÜKÜNÜN BEDELİ **SAYAÇTA ÖDENİYOR, KANALDA ÖDENMİYOR**

> **Durum: BULUNDU ve ÖLÇÜLDÜ · DÜZELTİLMEDİ** — düzeltme `sim2/` koduna
> dokunur ve çalışma kuralı 2 *"yapıyı anlat ve onay al"* diyor.
> **Üretici:** `sim2/kanal/cerceve.py` + `sim2/gozlem/yuk.py` ile doğrudan
> hesap; aşağıdaki tablo yeniden üretilebilir.

### Sözleşmenin merkezindeki vaat

`05-GOZLEM-PENCERESI.md` §A2 ve `gozlem/pencere.py` aynı şeyi söylüyor:

> *"Komşusunun girişim seviyesini ya da kuyruk durumunu kullanmak isteyen
> protokol, o alanları başlığa **KOYMAK** ve bedelini **ÖDEMEK**
> zorundadır."*

Bu, gözlem sözleşmesinin **yükü taşıyan** maddesidir: pencere dar tutuluyor
çünkü fazlası bayta mal oluyor.

### Ölçülen: bedelin yalnız YARISI ödeniyor

`Dugum.beacon_yuku()` yükün bayt maliyetini hesaplayıp `kontrol_bayt`
sayacına ekliyor — ✅ **muhasebe dürüst**. Ama `kosu.py::_beacon` havaya
**kurulumda bir kez kurulmuş, SABİT boyutlu** beacon çerçevesini veriyor:

| yük | `yuk_bayt` | bugün havada geçen süre | yük çerçeveye girseydi |
|---|---|---|---|
| `{"a": 1}` | 2 B | **320,0 µs** | 328,0 µs *(1,03×)* |
| 20 rota alanı | 250 B | **320,0 µs** | **1 320,0 µs** *(4,12×)* |

🔴 Yani 250 baytlık bir yük çerçeveyi **4,12 kat** uzatması gerekirken
**hiç uzatmıyor**. Sonuçları:

- `kontrol_airtime_s` sabit çerçevenin süresini sayıyor → **yükü görmüyor**
- uzun beacon **çarpışmaya daha çok maruz kalmıyor**
- daha çok bit **daha yüksek gövde hata olasılığı üretmiyor**

🔒 **Kısacası: yükü şişiren bir protokol, fizikte BEDAVA taze komşu bilgisi
alıyor ve yalnız `nrl_bayt` metriğinde pahalı görünüyor.**

### Bu neden şimdi önemli

Faz 4'ün özgün protokolü tam olarak **beacon'a alan koyan** sınıftandır
*(gürültü · kuyruk · bağ kalitesi)*. Bu boşluk kapatılmazsa, protokolün
kazancının bir kısmı ödenmemiş bir bedelden gelir ve `03` kural 11'in
yasakladığı şey olur: gösterilemeyen bir özgünlük iddiası.

### ⭐ DÜZELTMEK İÇİN EN İYİ AN TAM OLARAK ŞİMDİ — ölçüldü

Depodaki **üç** protokol gerçeklemesinin **üçü de** `beacon_yuku` olarak
`{}` döndürüyor *(`kosum_kosumu.py`de iki tane, `kahin.py`de bir tane)* ve
`yuk_bayt({}) = 0`. Yani düzeltme **bugün hiçbir ölçülmüş sayıyı
değiştirmez** — parmak izi birebir aynı kalır. Bir protokol yük taşımaya
başladıktan **sonra** yapılırsa, o güne kadarki her sayı bayatlar.

### ⚠️ VE BİR ÇİFT SAYIM TUZAĞI VAR — düzeltmede dikkat

Bugün `kontrol_bayt` İKİ yerden besleniyor: `Dugum.beacon_yuku` yükü,
`kosu.py::_beacon` çerçeveyi ekliyor. Çerçeve yükü içerecek biçimde
uzatılırsa **yük iki kez faturalanır**. Düzeltme tek kaynağa indirmeli:
çerçeve boyutu yükü içersin, sayaç yalnız çerçeveden okusun.

### 🔒 BEYAN EDİLMEMİŞ OLMASI AYRI BİR BULGU

Bu basitleştirme **hiçbir yerde yazılı değil**: `kapsam.py`nin
`MODELLENMEYEN` listesinde yok, `07` §12'de yok, `cerceve.py` başlığında
yok. Yani `03` B5'in tarif ettiği durum: **kod bir şey yapıyor, belge
başka bir şey vaat ediyor.** Düzeltilmezse bile **beyan edilmek zorunda**
ve yönü yazılmalı: *"beacon yükü taşıyan protokolü olduğundan UCUZ
gösterir."*

### 🟢 EK 2'NİN UYGULAMASI — öğrenci onayladı, ve regresyon KANITLANDI

> 🔒 **KARAR ÖĞRENCİNİN:** *"Düzelt — çerçeve yük kadar uzasın."*
> Çalışma kuralı 2 gereği yapı önce anlatıldı, sonra kod yazıldı.

**Ne değişti — tek kaynak ilkesiyle:**

| önce | sonra |
|---|---|
| `Dugum.beacon_yuku` yükü `kontrol_bayt`a ekliyor | 🔒 **eklemiyor** — yük çerçevenin BOYUTUNA giriyor |
| `kosu.py` sabit boyutlu beacon çerçevesini gönderiyor | 🔒 çerçeve `beacon_bayt + yuk_bayt` boyutunda kuruluyor |
| bedel iki yerden sayılıyor | 🔒 **tek yerden**: çerçeveden |

⚠️ Çift faturalama tuzağı gerçekti ve tasarımda karşılandı: çerçeve yükü
içerecek biçimde uzatılıp `Dugum` de saymaya devam etseydi yük **iki kez**
faturalanırdı. Bir test bunu bağlıyor.

**🟢 REGRESYON KANITI — iddia değil, ölçüm.**
`ciktilar2/adim9_kapanis.jsonl` bu değişiklikten **önce** (23:23) yazılmıştı.
Aynı konfig, aynı tohum, tam uzunlukta yeniden koşuldu ve sonuç satırı
**alan alan** karşılaştırıldı:

| bölüm | aynı mı |
|---|---|
| `metrikler` · `korunum` · `ham` · `teshis` | 🟢 **EVET** |
| `konfig` · `kapsam` · `ortam` | 🟢 **EVET** |
| `kimlik` | 🔴 tek fark: **`arac_hash`** |

🔒 **Ve o farkın olması GEREKİYOR:** `arac_hash` kaynak kodun özetidir;
kodu değiştirdim, özet değişti. **Sonuç değişmedi.** Yani mekanizma tam
olarak tasarlandığı gibi çalışıyor — kod değişikliği görünür, ölçüm sağlam.

**Üç yeni test eklendi:**
`test_BEACON_YUKU_cerceveyi_UZATIYOR` *(yük havada süre harcamak zorunda)* ·
`test_BEACON_YUKU_CIFT_FATURALANMIYOR` *(bedel tek kaynaktan)* ·
`test_BOS_YUKTE_sonuc_BIREBIR_AYNI` *(bugünkü kolların bozulmadığı)*.

⭐ Testlerin **kendi yüklü protokolü** var — çünkü depodaki üç gerçeklemenin
üçü de boş yük döndürüyordu ve kusurun 9 Eylül'e kadar görünmemesinin sebebi
tam olarak buydu: **hiçbir test yükü olan bir protokolü koşturmuyordu.**

### 🟢 EK 3 — DUMAN KOŞUCUSU UÇTAN UCA KOŞTU

*Üretici: `python -u kalibrasyon/uretici_duman.py` · 10 Eylül 2026*

Önce kapının kendi sınavı (`--kapi`, ~2 sn): **dört dalın dördü de ateş
etti** — kırık koşum yakalanıyor *(ve sebebi taşınıyor)*, sağlam betik
geçiyor, kapsam kapısı konuşuyor, olmayan dosya görülüyor.

Sonra dokuz üretici:

| betik | kesit | süre |
|---|---|---|
| `calisma_noktasi.py` | 6 tohum | 1 008 s |
| `cozunurluk.py` | tamamı | 539 s |
| `sonumleme_onbellegi.py` | bölüm 2 | 479 s |
| `karistirici_gucu.py` | tamamı | 341 s |
| `duyarlilik.py` | tek parametre | 264 s |
| `adim4_kapanis.py` | tamamı | 24 s |
| `adim4_sonumleme.py` · `calkanti.py` · `bag_kumesi.py a` | — | < 10 s |

🟢 **Dokuzunun dokuzu da `GECTI`.** Toplam **45,6 dk** — ilan edilen bandın
(*25–60 dk*) içinde, ama tahminimin üst yarısında. ⚠️ **Bandı ölçüme göre
düzelttim** *(40–60 dk)*: bir bandı sonuçtan sonra daraltmak değil,
gerçeğe uydurmaktır — ve `03` kural 1 zaten bunu istiyor.
⚠️ `calisma_noktasi.py`nin tam koşum bandı da **15–25 → 25–35 dk** yapıldı:
varsayılan tohum sayısı 6'dan 30'a çıktığı için bölüm 2 beş kat büyüdü.

---

# K-112 · 🟢 KONTROL DÜZLEMİ MEKANİZMASI UYGULANDI — ve veri onayında gizli bir kusur ölçüldü

> **Tarih:** 10 Eylül 2026 · **Karar: öğrenci** (beş sözleşme kararı) ·
> **Uygulama: ajan** · **Durum: UYGULANDI**
> **Sözleşme:** `v2/13-KONTROL-DUZLEMI.md` · **Kapılar:**
> `python -m pytest tests2/test_kontrol_duzlemi.py` ·
> `python -u kalibrasyon/kontrol_duzlemi_kapilari.py`

## 0 · ÖĞRENCİNİN GEREKÇESİ — kayda geçer
> *"Mevcut durum 'simülatör doğru' noktasında. Ama hâlâ 'bu simülatör
> gerçekten AODV/OLSR/AOMDV'yi ön-kayıtta tarif edildiği biçimde
> çalıştırabilir mi?' sorusunun mekanik cevabı eksik. Doğru hedef daha fazla
> kalibrasyon değil; ilk gerçek routing protokolünü bu doğrulanmış fizik
> üzerinde çalıştırabilecek mekanizmayı tamamlamak."*

Beş karar: (1) boyut RFC alanlarından, ek yük tek kaynak `cerceve_kur()`;
(2) uyandırma tavanı, aşımda deterministik FAIL; (3) aynı kanal/MAC/kayıp;
(4) teslim yalnız başarıda, yayında alıcı başına; (5) periyodik ve dinamik
zamanlayıcı ayrı. Protokol gerçeklemeleri **kapsam dışı** tutuldu.

## 1 · YAPI — üç ilke

- 🔒 **Protokol çağırmaz, niyet döndürür.** `KontrolIstegi` ve `Uyandirma`
  donmuş değerlerdir; `Karar.beyan` ile aynı biçim. Geri referans yapısal
  olarak imkânsız.
- 🔒 **Hepsi-ya-hiç kancalar.** Dört yeni kanca taşımayan protokol (bugünkü
  dört gerçekleme) hiçbir şey fark etmez; kısmi taşıyan kurulumda reddedilir.
- 🔒 **Yeni sayaç yok, yeni Konfig alanı yok.** Aksi hâlde sayaç şeması ya
  da kurulum özeti değişir ve **her mevcut satır** karşılaştırılamaz olurdu.
  Kontrol defteri sonuç satırına yalnız kontrol düzlemi kullanıldığında girer.

## 2 · İKİ TASARIM KARARI ÖLÇÜMLE VERİLDİ

**Zamanlayıcı: global tik değil, istek üzerine.** Bugünkü olay bütçesi
(tam uzunluk, statik, tohum 1000) **2 236 670** olay. Global 10 ms tik
**+1 400 000** olay (+%63) eklerdi — protokol hiçbir şey beklemese bile.

**Faz: yeni hash alanı değil, var olan akışın alt akışı.** `HASH_ALANLARI`na
ad eklemek `akis_listesi_hash`i, dolayısıyla her mevcut satırın kimliğini
değiştirirdi. Periyodik faz `beacon_faz`ın **düğüm alt akışından** çekiliyor;
kurulumdaki beacon fazları ana diziden çekildiği için hiçbiri kaymıyor.

## 3 · 🔴 UYGULARKEN BULUNAN: VERİ ONAYI YANLIŞ DÜĞÜMÜ KREDİLENDİRİYOR

Kontrol onayını yazarken veri yolunun onayına bakıldı: `teslim.onay_alindi`
onayı **çözen düğümün kim olduğunu sormuyor**. Aynı anda biten alımlar düğüm
sırasıyla işlendiği için, onayı ilk çözen **seyirci** göndereni
kredilendiriyor — gönderen onu çözemese bile.

*Üretici: değişiklik ÖNCESİ anlık kopyada `onay_seyirci.py` (40 s,
`EnYakinKimlik`); kod değiştirilmedi, iki metot sarıldı.*

| senaryo | tohum | gönderen kredilendirdi | seyirci kredilendirdi | **hayalet** |
|---|---|---|---|---|
| `statik-yok` | 1000 | 365 | 8 158 | **34** |
| `statik-surekli` | 1000 | 29 | 2 690 | **18** |
| `bagimsiz-surekli` | 1001 | 367 | 6 401 | **184** |

⚠️ **İlk ölçümüm yanlış anahtar kullanıyordu** ve sayıları şişirmişti (79 ·
37 · 231): alımları `id(iletim)` ile eşliyordum ve Python `id`leri yeniden
kullanıyor, yani bayat bir kayıt okunabiliyordu. Anahtar `(alıcı, gönderen,
başlangıç anı)` yapıldı ve ölçüm tekrarlandı; tablodaki sayılar ikincisidir.

🔒 **Hayalet kredi** = seyirci kredilendirdi **ve** gönderenin kendi alıcısı
o onayı çözemedi. Bu çerçeveler yeniden denenmesi gerekirken başarılı
sayıldı: `mac_gonderim_basarili`, PSR ve yeniden deneme davranışı
etkileniyor.

⚠️ **DÜZELTİLMEDİ ve bu bilinçli:** öğrencinin talimatı *"hiçbir mevcut sonucu
değiştirmemeli"* idi ve düzeltme veri yolunun sonuçlarını değiştirir. Kontrol
onayı **doğru** uygulandı (`n == gönderen`). İki onay semantiği bugün
ayrışık — bu açık bir risk ve öğrenci kararı.

## 4 · 🔴 BİR MEVCUT TEST ÇAKIŞTI — test gevşetilmedi, ad değişti

`test_TEK_per_govdesi_VAR` `kanal.py` dışında adında **"per"** geçen her
fonksiyonu ikinci bir PER gövdesi sayıyor. İlk kanca adı `periyot_doldu`
ve iç fonksiyon `_periyot` Türkçe **per**iyot yüzünden yakalandı. Test bir
ad eşleştirmesi — kaba ama işini yapıyor; gevşetmek yerine kanca
`zamanlayici_doldu`, iç fonksiyon `_zamanlayici_ates` oldu.

## 5 · SONUÇLAR

**Test takımı:** `503 passed` (478 mevcut + 25 kapı) ·
`Yapisal ihlal YOK` · köken borcu 35.

**P1–P8, 40 düğümde gerçek kontrol trafiğiyle** *(üretici:
`python -u kalibrasyon/kontrol_duzlemi_kapilari.py`, 60 s, karıştırıcı
20 s'de açılıyor)*:

| kapı | `statik-surekli` · 1000 | `bagimsiz-surekli` · 1001 |
|---|---|---|
| **P1** kontrol iletimi · sayaç ≡ havaya çıkan | 7 815 · EVET | 7 442 · EVET |
| **P2** kontrol onayı ≡ unicast teslim+tekrar · yeniden deneme | 3 634 ≡ 3 634 · 1 781 | 2 857 ≡ 2 857 · 2 223 |
| **P3** teslim ≡ fiziksel başarı (multiset) · kayıp alım · başkasına adresli | 22 249 · EVET · 237 552 · 36 288 ≡ 36 288 | 18 556 · EVET · 227 681 · 28 087 ≡ 28 087 |
| **P4** periyodik (zincir) · dinamik (en büyük anlık hata) | 3 360 kesin · 1 838 (2,6 µs) | 3 360 kesin · 1 449 (2,1 µs) |
| **P8** veri defteri · kontrol defteri · geçerli | TAMAM · TAMAM · True | TAMAM · TAMAM · True |
| kontrol defteri: istenen = yayın + onaylanan + vazgeçilen | 6 034 = 2 400 + 3 555 + 79 | 5 219 = 2 400 + 2 647 + 172 |
| tepe bekleyen uyandırma / tavan | 2 / 256 | 2 / 256 |

**Ortak:** P2 — kontrol trafiği eklenince aynı tohumdaki veri sayaçları
değişiyor (`mac_deneme` 14 883 → 22 819, `teslim_paket` 825 → 669): kontrol
aynı kanalı gerçekten paylaşıyor. P5 — iki koşuda aynı FAIL: *düğüm 7,
t = 0,068035…, 257 > 256*. P6 — pencere 12/7/5, kısmi kanca reddi. P7 — aynı
tohum, aynı satır.

⚠️ Dinamik uyandırma anlık hatası (µs) sıfır değil çünkü kanıt protokolün
YEREL saatinden okunuyor ve saatin sapması 20 ppm; olay kuyruğundaki anın
kendisi kesin.

**Regresyon — mevcut sonuç satırları birebir.** Kod değiştirilmeden ÖNCE
deponun anlık kopyası alındı; aynı 35 kolluk matris önce kopyada, sonra
değişmiş depoda koşuldu ve satırlar **alan alan** karşılaştırıldı.

| | |
|---|---|
| matris | 18 senaryo × `EnYakinKimlik` (kısa) · 6 karıştırıcı × `DogrudanKomsu` · 3 kol × iki kâhin · yüklü beacon · 4 tam uzunluk |
| **birebir aynı satır** | **35 / 35** · karşılaştırılan 7 145 091 bayt |
| değişen kimlik alanları | `arac_hash` (kaynak kodun özeti) · onu içeren `kosu_kimligi` · her koşuda değişen `calisma_kimligi`, `zaman_damgasi_utc` |
| beyanlı fark | `teshis.koken_kovalari.SINANMAMIS` **33 → 35** — iki yeni sabit deftere girdi; simülasyon sonucu değil |

🔒 **Temel üreticinin kendisi de sınandı:** tam uzunluktaki `statik-yok ·
DogrudanKomsu · 1000` satırı, dün başka bir aletin (`adim9_kapanis.py`)
yazdığı satırla `metrikler · korunum · ham · teshis` düzeyinde birebir aynı
çıktı — karşılaştırma bir alet hatasına dayanmıyor.
⚠️ Karşılaştırıcıda bir hata yakalandı: meşru kimlik alanlarını silindikten
SONRA okuyordu, yani "değişen alan yok" diyecekti. Düzeltildi ve yeniden
koşuldu.

## BUNU NE DEĞİŞTİRİR
- `06` §4.2'nin U2/U3 testleri artık **mekanik olarak ifade edilebilir**;
  sınanmaları için protokollerin yazılması gerekiyor.
- Köken borcu **33 → 35** (`KONTROL_KAPSULLEME`, `BEKLEYEN_UYANDIRMA_TAVANI`).
- Faz 3'ün önündeki kalan mekanik boşluklar: beacon'ın protokol başına
  kapatılması, bağ kopması geri bildirimi, protokol rastgelelik kaynağı,
  veri onayı semantiği (`13` §06).

---

# K-113 · 🟢 ÖĞRENCİNİN 10 EYLÜL KARARLARI — belgeler bilgi kaynağına çevrildi, iki ölçüm yenilendi

> **Tarih:** 10 Eylül 2026 · **Karar:** öğrenci (§1) · **Uygulama ve devredilen
> seçimler:** ajan · **Durum:** kararlar kayda geçti, belgeler güncellendi;
> `sim2` değişiklikleri yapı onayı, uzun koşumlar süre onayı bekliyor.
> **Üreticiler:** `python kalibrasyon/mimari_denetimi.py` ·
> `python -u kalibrasyon/li_replikasyonu.py` ·
> `python -u kalibrasyon/cozunurluk.py --tohum 40`

## 0 · Bağlam

Yeni bir ajan salt okuma turunda projeyi özetledi; açık soruları ve belgeler
arası çelişkileri listeledi. Öğrenci hepsine cevap verdi ve şunları istedi:
belgelerin güncellenmesi, gereksiz yerlerden arındırılması, ajanların özgür
düşünmesini kısıtlayan aşırı katı kural bölümlerinin gevşetilmesi ve
belgelerin bir bilgi kaynağına çevrilmesi. Belirsiz yerlerin ajan tarafından
ölçülerek çözülmesini de istedi.

## 1 · Öğrencinin kararları

| # | konu | karar | ajana devredilen |
|---|---|---|---|
| 1 | keşifsel yüksek çalkantı kolu (Θ = 1,78) | saklanmaz, halının altına süpürülmez; sorun varsa düzeltilir | sorunun teşhisi ve düzeltme önerisi |
| 2 | tohum sayısı | ana deney **40 tohum** | — |
| 3 | mobilite | ajan daha mantıklı tercihini belirtecek | öneri |
| 4 | görev kolu yarıçapı | daha büyük örneklemle yeniden ölçülecek | ölçüm tasarımı |
| 5 | düğüm sayısı | 30–50 aralığında; en uygun ve gerekli değer | ölçütle bulunması |
| 6 | veri onayı kusuru | önce etkisi ayrı ölçülecek, sonra karar | ölçüm tasarımı |
| 7 | yere toplama | kabul; en iyi tasarım düşünülecek | tasarım önerisi |
| 8 | karıştırıcı | birden fazla ve hareketli; saha davranışına paralel | model önerisi |
| 9 | mühür tarihi | sabit tarih yok; simülasyon işleri 26 Eylül'e kadar bitirilmeye çalışılacak | — |
| 10 | iş akışı | simülasyon → protokollerin yapımı ve denenmesi → özgün protokolün tasarımı → pürüz temizleme ve veri toplama → rapor ve sunum (görselleştirmeyle) | ayrıntılandırma |
| 11 | birincil karıştırıcı konumu | çoklu karıştırıcı tasarımıyla birlikte; özgün protokol tasarımını öğrenci simülasyon oturunca gösterecek | — |
| 12 | PSR | bağ düzeyinde, alıcının CRC'den geçirerek hatasız aldığı paketlerin gönderilen pakete oranı | simülatördeki tam tanım |
| 13 | tespit gecikmesinin boş kol kapısı | protokol yazım aşamasına | — |
| 14 | Rician K | kaynağı doğrulanacak | — |
| 15 | iki anlamlılık sabiti | ölçülerek en mantıklısı | seçim |
| 16 | ısınma ve ölçüm penceresi | birlikte taranacak; karıştırıcı açılma anı parametre kalacak | tarama tasarımı |
| 17 | kâhin tazeleme süresi | üst sınır kabul | — |
| 18 | tavan kâhini | kontrol edilip mantıklı olan yapılacak; istatistikte üst referans istenir | öneri |
| 19 | kontrol istatistikleri | projenin faydasına göre | öneri |
| 20 | belgeler | DEVIR yalnız devir içindir, çok referans alınmaz; belgeler eski olabilir, yedi kova esastır; düğüm sayısı 30–50 düşünülür; Li H1 yeniden ölçülür; TÜBİTAK belgesi şimdilik gerekmez | belge düzenlemesi |

## 2 · Bugünkü ölçümler

### 2.1 · Köken defteri — KAYNAK sayısındaki çelişki kapandı

`python kalibrasyon/mimari_denetimi.py`: **130 parametre** — TÜRETİLMİŞ 43 ·
ÖLÇÜLMÜŞ 11 · KAYNAK **6** · DUYARSIZ 18 · TEDAVİ 11 · KOL TANIMI 6 ·
SINANMAMIŞ 35 · duyarlılık borcu 5 · yapısal ihlal yok · 11 not.

- Belgelerde KAYNAK için hem 4 hem 6 yazıyordu; doğrusu 6.
- TEDAVİ 11 = `Konfig`in 4 tedavi alanı + kalibrasyon betiklerinin 7 tarama
  ekseni.

### 2.2 · Li H1 yeniden ölçüldü — değişmedi; iki farklı sayının kaynağı bulundu

`python -u kalibrasyon/li_replikasyonu.py`:

| düğüm | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|
| tek atlamaya oran | 1,0000 | 0,2843 | 0,2050 | 0,1715 | 0,1421 | 0,1249 | 0,0985 | 0,0898 | 0,0824 | 0,0739 |

- H1 = **0,0861** → band [0,10; 0,20] dışında, tutmadı · H2 tuttu · H3 tuttu ·
  B bölümü 1,8 dk.
- Duyma menzili taraması (1,0 · 1,5 · 2,0 · 3,0 · 4,5 · 6,31 kat): oranlar
  0,0305 · 0,0305 · 0,0729 · 0,0905 · 0,0791 · 0,0740; hiçbiri bandın içinde
  değil.
- 9 Eylül kaydıyla on noktanın onu da birebir aynı.
- **İki sayının kaynağı:** betikteki ön-kayıtlı H1 tanımı *"8–11 düğümlü
  zincirlerin oranlarının ortalaması"*dır, yani 0,0861. **0,0739** yalnız 11
  düğümün değeridir ve mekanizma öngörüsüyle (0,0714) karşılaştırılan sayıdır.
  Eski DEVIR §3.6 ve eski `07` §10 0,074'ü H1 değeri diye yazıyordu; bu sürüm
  düzeltildi.
- **Açık kanal:** 280 m aralıkta ortalama 0,8800, en kötü bağ 0,0000. `09`
  §03.1b'deki 0,94–0,98, 200 m'lik ilk denemenin bağlamında verilmişti.

### 2.3 · Çözünürlük 40 tohumda

`python -u kalibrasyon/cozunurluk.py --tohum 40` (`statik-surekli`, tohumlar
1000–1039):

| çıktı | ortalama | SD | R = 2·SD/√40 |
|---|---|---|---|
| ETX kâhini PDR | 0,9349 | 0,0767 | 0,0243 |
| atlama kâhini PDR | 0,8795 | 0,1005 | **0,0318** |
| ölçütün bedeli (eşleştirilmiş) | 0,0554 | 0,0729 | 0,0231 |

- 30 tohumda en gevşek R 0,0361 idi (K-107).
- Betiğe `--tohum N` argümanı eklendi. Varsayılan 30 kaldı, böylece köken
  defterindeki 0,036 kaydı argümansız komutla yeniden üretilebilir.
- Değişiklikten sonra mimari denetimi yeniden koşuldu: D13 taranan sabit 33,
  kökeni yazılmamış 0, yapısal ihlal yok.

## 3 · Ölçümle ya da hesapla bulunan yeni şeyler

- **M4'ün çok pencereli taraması** (`08` §05.3): pencere başına 0,01 yanlış
  alarm, ~170 pencerelik taramada karıştırıcısız kolda en çok ~%82 yanlış
  tespit olasılığı verir (hesap: `1 − 0,99^170`; ölçülmedi). Bugün görünmüyor,
  çünkü koşum aletleri kopma beyan etmiyor.
- **Yüksek çalkantı kolu yalnız OLSR'ın zarfı dışında** (`07` §03.3): aynı rota
  ömrü AODV'nin 3 s'lik zaman sabitine bölününce Θ_AODV çekirdekte 16,3,
  yüksek çalkantıda 8,9 (hesap; τ K-110 EK-3). Kol bir kurulum hatası değil,
  etiketiyle raporlanacak bir stres koludur.
- **Bugünkü PSR gönderen tarafında ve onaya dayalı;** öğrencinin tanımı alıcı
  tarafında. Seyirci onay kusuru bugünkü oranı doğrudan şişirir; yeni tanımı
  yalnız deneme sayısı üzerinden dolaylı etkiler (`07` §08.2).

## 4 · Belge düzenlemesi — ajan

- **Yeniden yazılanlar:** `01` · `03` · `05` · `06` · `07` · `12` ·
  `v2/README` · kök `README` · `DEVIR` · `DEVIR-PROMPT`. Önceki sürümler:
  `v2/arsiv/*-2026-09-10.md` · `arsiv/DEVIR-2026-09-10.md` ·
  `arsiv/DEVIR-PROMPT-2026-09-10.md` · `arsiv/README-2026-09-05.md`.
- **Düzenlenenler:** `02` (bant, §S) · `08` (bant, §05.3) · `09` (bant) · `10`
  (bant) · `13` (§06.1).
- **Arşive taşınanlar:** `v2/00-BASLATMA-PROMPTU.md` ve `v2/09-DEVIR-TESLIM.md`
  → `arsiv/v2-eski/`. Hiçbir dosya silinmedi.
- **Aşama numaralaması tekleştirildi** (`01` §5); eski iki "Faz"
  numaralamasının karşılığı orada.
- `03`ün kural listesi **ilke · gerekçe · nerede esner** biçimine çevrildi;
  çalışma anlaşmaları (git, yapı onayı, süre onayı, üretici komut) ayrıldı ve
  korundu.
- Güncel durum ve plan artık `12`de; öğrenci kararlarının tek listesi `07`
  §15'te.

## 5 · 🔵 Öğrenci onayına sunulan gevşetme — mühür sırası

- **Eski:** özgün protokol mühürden sonra ilk kez koşulur.
- **Yeni** (`06` §0.3): özgün protokol geliştirme tohumlarında tasarım
  sırasında koşulabilir. Korunanlar üçtür: ana deney tohumları mühürden önce
  hiçbir kolda koşulmaz · eşiklerin türetme formülleri özgün protokolün ilk
  koşusundan önce yazılır ve değerleri rakiplerin gürültüsünden gelir ·
  parametreler mühürde sabitlenir.
- **Gerekçe:** öğrencinin iş akışında tasarım veri toplamadan önce gelir; bir
  protokol denenmeden tasarlanamaz.
- **Kalan risk:** birincil hücre seçimi. Aday hücre önceden yazılır; değişirse
  gerekçesiyle kaydedilir ve hipotez keşifsel etiketlenir.
- Onaylanmazsa eski sıraya dönülür.

## 6 · Ajanın önerileri — öğrenci kararı ya da yapı onayı bekliyor

- **Mobilite:** çekirdekte formasyon + istasyon tutma (`07` §03.4).
- **Yere toplama:** röle İHA geçit, çekirdekte 1 geçit, kenarda; tüm düğümler
  telemetri; düşük hızlı komut akışı; yük ölçütle (`07` §06.2).
- **Çoklu hareketli karıştırıcı:** sinyal sınıfı × platform ve hareket × yayın
  düzeni; dört senaryo ailesi (`07` §05.3).
- **Üst referans:** teslim olasılığı kâhini ve kâhin zarfı (`07` §07.2).
- **Kontrol düzlemi:** R2, R3, R4, R8 (`13` §06.1).
- **PSR'nin uygulanması:** `07` §08.2.
- **Düğüm sayısı ölçütü:** `07` §09.4.
- **Anlamlılık sabitleri:** tek α ve tarama düzeltmesi (`08` §05.3).

## BUNU NE DEĞİŞTİRİR

- Ana deney 40 tohum, 2000–2039; 40 tohumluk çözünürlük ~3,2 PDR puanı.
- Sabit mühür tarihi yok; Aşama 1'in hedefi 26 Eylül.
- DEVIR bir devir notuna indi; proje bilgisi `v2/`de.
- Aşama 1 iş listesi (`12` §3) yapı ve süre onaylarını bekliyor; ilk öncelik
  veri onayı etkisinin ölçümü ve Aşama 2'nin ön koşulu olan yetenekler.

---

# K-114 · 🟡 İKİNCİ TUR ONAYLARI — yapı planı yazıldı, dört ölçüm aleti kuruldu, bir süre tahmini çöktü

> **Tarih:** 10–11 Eylül 2026 · **Karar:** öğrenci (§1) · **Uygulama:** ajan ·
> **Durum:** ölçüm aletleri ve regresyon tabanı hazır. 11 Eylül'de öğrenci
> yapıyı (`07` §18 Y1, Y3–Y7, Y10), veri onayı düzeltmesini (Y2) ve üst
> referansın yeni çekirdek hücrede ölçülmesini onayladı. Uygulama K-115'te.
> **Üreticiler:** `python -u kalibrasyon/anlamlilik_sabitleri.py` ·
> `python -u kalibrasyon/onay_semantigi.py olc kisa_2026-09-11 --tohum 5`, ardından `… --tohum 8 --devam` ·
> `python -u kalibrasyon/ust_referans.py --kapi` · `… teshis [--profil]` ·
> `python -u kalibrasyon/regresyon_satirlari.py karsilastir taban_2026-09-11 taban_2026-09-11b` ·
> `python -u kalibrasyon/regresyon_satirlari.py uret <etiket>` ·
> `python kalibrasyon/mimari_denetimi.py`

## 1 · Öğrencinin kararları

- **Mobilite:** öneri onaylandı — çekirdekte formasyon + istasyon tutma.
- **Yere toplama:** öneriler kabul edildi, bir şartla: *"projede dürüstlük ve
  gerçekçiliğe sıkıntı çıkarmayacaksa."*
- **Çoklu hareketli karıştırıcı:** model onaylandı. Saha davranışı sentezini
  öğrenci sağladı:
  `protokol_kaynaklari/literatur_taramasi_2026-08-31/02_proje_özeli_literatür/taktik-iha-mesh-karistirici-saha-davranislari.md`.
- **Üst referans:** teslim olasılığı kâhini ve kâhin zarfı onaylandı.
- **Kontrol istatistikleri:** öneri onaylandı.
- **Mühür sırası:** gevşetme onaylandı.
- *"Şimdi işe devam edebilirsin."*

## 2 · Ajanın yaptıkları

### 2.1 · Yapı planı — `07` §18

Onaylanan tasarımların kodda nasıl kurulacağı yazıldı ve `sim2`
değişikliğinden önce yapı onayına sunuldu:

- Y0 regresyon aleti · Y1 PSR + kontrol istatistikleri · Y2 veri onayı
  semantiği (ölçüme bağlı)
- Y3 kontrol düzlemi eksikleri (R2–R4) · Y4 yere toplama · Y5 çoklu
  karıştırıcı · Y6 formasyon mobilitesi
- Y7 protokol başına Θ · Y8 iz kanalı · Y9 teslim olasılığı kâhini · Y10
  anlamlılık sabitleri

**Ortak kural:** varsayılanlar bugünkü davranışı birebir üretir ve her adım
bir regresyon + test koşusuyla kapanır.

### 2.2 · Yere toplama şartının değerlendirmesi — `07` §18 Y4

Beş risk tartıldı:

1. Geçidin yere bağı modellenmiyor (ortak mod).
2. Tek geçit darboğazı (yük ölçütü + kayıp yeri raporu).
3. Yer istasyonlu mimari yok.
4. Telemetri hızının ve paket boyunun kaynağı yok.
5. Literatürle kıyas zorlaşıyor (eşler arası desen keşifsel eksende korunuyor).

**Sonuç:** beş beyanla bir dürüstlük sorunu görünmüyor. Gerçekçilikteki tek
sınır yer istasyonlu mimarinin dışarıda kalması; açıkça yazılır.

### 2.3 · Saha sentezinin simülatördeki karşılığı — `07` §18 Y5

- Sentezin yedi sinyal sınıfından beşinin karşılığı var.
- Karşılığı olmayanlar: dar bant/spot ile ton/taşıyıcı (tek kanal SINR
  soyutlaması onları ayırmıyor), protokol farkında karıştırıcı (keşifsel
  eklenebilir), anten yönelimi ve arazi. Hepsi beyan edilir.
- ⚠️ Sentez nicel saha verisinin açık literatürde sınırlı olduğunu kendisi
  söylüyor. Bu yüzden karıştırıcıların zaman ve hız parametreleri tek bir
  "gerçek değer" olarak değil, **protokol zaman sabitleri cinsinden eksenler**
  olarak tanımlanacak. Sentezin künyeleri `02`de tek tek açılıp
  doğrulanmadı.

### 2.4 · Yeni ölçüm aletleri — `sim2`ye dokunmadan

| alet | ne yapar |
|---|---|
| `regresyon_satirlari.py` | Y0 — sabit bir matrisin tam sonuç satırlarını yazar ve alan alan karşılaştırır. K-112'nin depoda kalmayan karşılaştırma betiğinin kalıcı hâli. Vaka başına duvar saati basılır, satıra yazılmaz. **Tam uzunluk vakaları ilk üretimden önce süreye göre yeniden seçildi, bir yanlış adımla:** önce hareketli kolun tam uzunluktaki kâhin vakasını (~20 dk) ölçmeden `en_yakin_kimlik`e çevirdim. Sonra ölçtüm: o protokol kasıtlı olarak döngü ürettiği için kısa pencerede 378,6 s sürüyor, yani tam uzunlukta ~44 dk; kâhinden de yavaş. Son matris: statik kolda ETX kâhini (kısa ~53 s), hareketli kollarda `dogrudan_komsu` (kısa 76,1 · 64,4 s). Süre tablosu `vakalar()` içinde |
| `anlamlilik_sabitleri.py` | M4'ün çok pencereli yanlış alarmını sentetik boş hipotezde, gerçek fonksiyonla ölçer |
| `onay_semantigi.py` | veri onayı semantiğinin etkisi. Karar eşiği `COZUNURLUK_R` köken defterine ÖLÇÜLMÜŞ olarak eklendi → 131 parametre, ÖLÇÜLMÜŞ 12 |
| `ust_referans.py` | Y9 — teslim olasılığı kâhini; kâhin modülüne dokunmadan alt sınıf olarak (geçici yer beyanlı) |

Mimari denetimi dört aletten sonra da temiz: 105 modül, içe aktarılamayan 0,
kökeni yazılmamış 0 (`python kalibrasyon/mimari_denetimi.py`, 11 Eylül).

## 3 · 🔴 Bir süre tahmini çöktü — ve ara kayıt hatası ajanın kendi betiğinde tekrarlandı

- **İlk tasarım:** veri onayı ölçümünün ilk sürümü 160 koşuyu tam uzunlukta
  koşuyor ve sonuçları yalnız sonda basıyordu. Süreyi başka koşum koşullarına
  ait bir sayıdan türetip koşu başına ~2 dk tahmin ettim ve bandı 25–45 dk
  verdim.
- **Gerçek:** kâhin kolunda tam uzunlukta bir koşu ~20–25 dk sürdü. 79
  dakikada 32/160'a gelmişti; toplam ~6 saat sürecekti.
- **Ne yapıldı:** 11 Eylül'de fark edildi ve süreç durduruldu; 1 saat 43
  dakikadır 10 işçiyle koşuyordu. Sonuçlar diske anında yazılmadığı için
  kayboldu. Bu, `03` B5'teki "ara kayıt tutmamak" hata sınıfının ta
  kendisi.
- **Düzeltme:** kısa pencere · her koşu anında diske ve `--devam` ile
  sürdürme · kapı koşu süresini ÖLÇÜP bandı basıyor. Kısa pencerede ölçülen:
  karıştırıcılı statik kol ~53 s, karıştırıcılı hareketli kol ~170 s.
- **Ders:** bir süre bandı başka bir koşumun sayısından türetilmez; aletin
  kendi kapısında ölçülür.
- **Aynı gün bir kez daha:** regresyon aletinin tam uzunluk vakasını ölçmeden
  daha yavaş bir protokole çevirdim; ilk üretimden önce ölçülünce yakalandı
  (§2.4). Üst referans aletinde de kısa koşu, veri onayı aletinin kapısındaki
  ~170 s yerine 326,8 s sürdü; sebebi teslim kâhininin uzun yolları (§4.3).
- **Üçüncü kez, ve 30 dk kuralı çiğnendi:** regresyon tabanını 12–25 dk
  tahminiyle başlattım; 32,4 dk sürdü. Tahmin iki şeyi atlamıştı:
  - Kısa sondaj yalnız `surekli` sınıfını ölçmüştü. En uzun vaka `reaktif`
    sınıfındaydı: 1330 s.
  - Sondaj tek süreçti. 10 işçi 8 fiziksel çekirdekte koşunca süreç başına
    ~2,1 kat yavaşlama oluyor (üç vakada 2,12–2,18).

  Matris küçültüldü (§4.4).
- **Bu makinede bant kuralı:** bant tek süreçli bir sondajdan verilecekse ×2,1
  yük katsayısı uygulanır ve matrisin **her** senaryo sınıfı sondajlanır.

## 4 · Ölçümler

### 4.1 · Evre metriklerinin anlamlılık sabitleri — sentetik boş hipotez

`python -u kalibrasyon/anlamlilik_sabitleri.py` · 4 000 deneme/hücre ·
yanlış alarm oranı ± 2 SE:

| beyan hızı (1/s) | bugünkü kural (pencere başına 0,01) | Bonferroni (0,05 / 170) |
|---|---|---|
| 0,1 | 0,514 ± 0,016 | 0,022 ± 0,005 |
| 0,5 | 0,374 ± 0,015 | 0,024 ± 0,005 |
| 2,0 | 0,578 ± 0,016 | 0,034 ± 0,006 |
| 10,0 | 0,696 ± 0,015 | 0,030 ± 0,005 |

`08` §05.3'teki hesapla gösterilen risk ölçümle doğrulandı. Öneri `07` §18
Y10'da.

### 4.2 · Veri onayı semantiğinin etkisi

`python -u kalibrasyon/onay_semantigi.py olc kisa_2026-09-11 --tohum 5`, ardından
önceden yazılmış kural gereği (karar yok → genişlet) `… --tohum 8 --devam`.
Analiz yeniden: `… analiz kisa_2026-09-11`.

**Kurulum**

- Kısa pencere: karıştırıcı 5 s'de açılır, ölçüm 10–40 s arası.
- 4 kol × 2 kâhin × 2 semantik × 8 tohum = 128 koşu.
- Geçersiz koşu 0 · süre 28,0 + 17,3 dk.
- "Düzeltilmiş" semantikte onay yalnız göndericinin kendisi çözdüyse sayılır.

**Karar metriği.** PDR farkı (düzeltilmiş − mevcut), eşleştirilmiş, ± 2 SE, R = 0,0318:

| kol | ETX kâhini | atlama kâhini |
|---|---|---|
| statik-yok | +0,0006 ± 0,0009 · altında | −0,0015 ± 0,0022 · altında |
| statik-surekli | −0,0023 ± 0,0030 · altında | +0,0016 ± 0,0043 · altında |
| bagimsiz-yok | +0,0052 ± 0,0165 · altında | −0,0106 ± 0,0339 · **karar yok** |
| bagimsiz-surekli | +0,0137 ± 0,0240 · **karar yok** | −0,0082 ± 0,0250 · **karar yok** |

- Çözünürlük üstünde 0 hücre · altında 5 · karar yok 3.
- 5 tohumda karar yok 1'di; genişletme ikisini daha ekledi. ETX'in
  `bagimsiz-surekli` farkı −0,003'ten +0,014'e döndü: gürültü.

**Mekanizma (kodla doğrulandı).**

- Onay yalnız alıcı veriyi çözdüyse gönderilir; `teslim.onay_alindi` bu
  değişmezi çalışma anında denetliyor.
- Dolayısıyla seyirci kredisi alan her iletimde veri bir sonraki atlamaya
  **zaten ulaşmıştır**.
- Kusur teslimi değiştirmez; göndericiye fiziksel olarak alamayacağı bir
  "başarılı" bilgisi verir.
- Beklenen iz: PDR'de küçük, MAC sayaçlarında büyük fark.

Ölçülen, tohum ortalamaları (ETX · atlama):

| | statik-yok | statik-surekli | bagimsiz-yok | bagimsiz-surekli |
|---|---|---|---|---|
| hayalet kredi / koşu (mevcut) | 8 · 18 | 27 · 45 | 78 · 80 | 100 · 102 |
| onaysız kalan onay, mevcut → düzeltilmiş | 59→72 · 59→90 | 72→121 · 68→154 | 80→223 · 77→252 | 85→297 · 92→290 |
| bugünkü `psr` farkı | −0,0003 · −0,0050 | −0,0031 · −0,0063 | −0,0016 · −0,0229 | −0,0106 · −0,0157 |
| teslim edilen paket farkı (koşu başına ~1100–1600) | +0,6 · −1,3 | −1,3 · +0,1 | +6,9 · −14,9 | +17,1 · −9,8 |

Terimler:

- **Hayalet kredi:** seyirci çözdüğü için sayılmış, ama göndericinin
  kendisinin hiç çözemediği onay.
- **Onaysız kalan onay** (`mac_onaysiz_onay`): veri ulaştığı halde onayın
  göndericiye gelmediği durum.
- **Bugünkü `psr`:** onaya dayalı MAC başarı oranı, `mac_gonderim_basarili /
  mac_deneme`. Y1'de `mac_basari_orani` adını alacak.

Teslim farklarının hepsi 2 SE içinde. Betimleyici satırlar çoklu
karşılaştırmadır; tek tek anlamlılık iddia edilmez.

**Karıştırıcı kusuru büyütüyor.** Karıştırıcı açıkken hayalet kredi statik kolda
2,5–3,3 katına, hareketli kolda 1,3 katına çıkıyor. *Yorum:* karıştırıcı
göndericinin onayı almasını bozuyor; ama uzaktaki bir seyirci onayı çözünce
gönderici bu bozulmayı hiç görmüyor. Bu, protokol gözlemindeki
`son_iletim_sonucu`nun ve `13` R3'teki iletim sonucu kancasının taşıyacağı
bilgidir. Yani tam da projenin konusu olan sinyal.

**Hareketli kollarda eşleştirme çözülüyor.**

- İki semantik ilk farklı onayda ayrışır; sonrası farklı çekişme ve farklı
  rastgele çekimlerdir.
- Statik kolda topoloji sabit olduğu için farkın 2 SE'si ≤ 0,004.
- Hareketli kolda 0,017–0,034, yani R ile aynı büyüklükte.
- Üç hücreyi çözmek için kabaca 10–20 tohum gerekir (tahmin: nokta tahmini ve
  yayılım aynı kalırsa).

**Öneri: düzeltmek (`07` §18 Y2). Karar öğrencinin.**

- Kusur fiziksel olarak mümkün olmayan bir bilgi veriyor ve karıştırmanın
  gönderici tarafındaki etkisini gizliyor.
- PDR'deki etkisi hiçbir hücrede çözünürlük üstünde görünmedi.
- Ana deney satırları Y1–Y10'dan sonra zaten yeniden üretilecek; düzeltmenin
  ek ölçüm bedeli yok.
- Düzeltme seçilmezse iki ölçüm daha gerekir: hareketli kollarda 10–20 tohum
  ve evre metrikleri için tam uzunluk. İkisi de 30 dk'yı aşar.

**Süre bandı**

- 5 tohum: kapının bastığı bant 14–30 dk · gerçek 28,0 dk.
- Genişletme: basılan 22–47 dk bütün koşular içindi; kalan 48 koşu 17,3 dk
  sürdü.
- Gerçek süre `n · en_uzun / işçi` değerinin 1,21 ve 1,27 katı çıktı.
- İki kâhin aletinin bant katsayıları bu ölçümle 0,9–1,6 yapıldı.

### 4.3 · Üst referans

**Kapı:** `python -u kalibrasyon/ust_referans.py --kapi` · 11 Eylül · üç kapı OK.

| kol (tohum 1000, kısa pencere) | ETX | atlama | teslim olasılığı |
|---|---|---|---|
| statik-surekli | 0,9891 | 0,9850 | 1,0000 |
| bagimsiz-surekli | 0,9065 | 0,8681 | 0,9633 |

En uzun kısa koşu 326,8 s sürdü; veri onayı aletinde ~170 s'ydi. 10 tohumluk
ölçümün bandı 59–105 dk basıldı. 30 dk'yı aştığı için ölçüm başlatılmadı.

**Teşhis: neden iki kat yavaş?**
`python -u kalibrasyon/ust_referans.py teshis --profil` · bagimsiz-surekli ·
tohum 1000 · kısa pencere.

| kâhin | PDR | teslim | atlama isteği / teslim | deneme / atlama isteği | gecikme ort · p95 (s) | süre |
|---|---|---|---|---|---|---|
| atlama | 0,8681 | 1339 | 2,00 | 2,15 | 0,013 · 0,040 | 165,7 s (profilsiz) |
| ETX | 0,9065 | 1434 | 1,97 | 1,93 | 0,012 · 0,037 | 483,1 s (profil altında) |
| teslim olasılığı | 0,9633 | 1532 | **4,65** | 1,60 | **0,040 · 0,102** | 839,9 s (profil altında) |

- **Hipotez doğrulandı.** `−ln s` ağırlığı iyi bağlarda neredeyse sıfır
  (p = 0,9 → ~10⁻⁵). Kâhin az atlamalı orta kaliteli yol yerine çok atlamalı,
  iyi bağlı yolu seçiyor: paket başına ~2,4 kat atlama, atlama başına daha az
  deneme.
- **Bedeli.** PDR +0,057, ama ortalama gecikme ~3,3 kat, p95 ~2,8 kat.
- **Süre nereye gidiyor.** Profilin ilk sıraları kanalın kendisi: sönümleme
  süzgeci, rastgele çekim, gölgeleme, konum. Dijkstra ilk 12'de yok. Fonksiyon
  çağrısı 1,12 → 2,04 milyar. Süre çerçeve sayısıyla büyüyor, bu yüzden bir
  yol önbelleği hızlandırmaz.
- **Profilsiz doğrulama.** `python -u kalibrasyon/ust_referans.py teshis`
  aynı sayaçları birebir verdi: PDR, teslim, iki oran, gecikme. Süreler ETX
  172,0 s · atlama 173,1 s · teslim 287,7 s; teslim/ETX 1,67 kat. Koşu test
  takımıyla eşzamanlıydı (4 süreç).
- Tek tohum: bu bir teşhis, ölçüm değil. Karar ölçütü uygulanmadı.

**Anlamı.** Teslim olasılığı kâhini tanımı gereği yalnız teslimi en büyütür;
çekişmeyi, kuyruğu ve gecikmeyi görmez. Bu yüzden kâhin zarfı **PDR için** bir
üst referanstır, gecikme için değil. Raporda zarfın gecikmesi yanında yazılır.
Tasarım değiştirilmedi: atlama cezası eklemek serbest bir parametre olurdu.

**Öneri (karar öğrencinin).** 10 tohumluk ölçümü şimdi koşmamak; yeni çekirdek
hücre kurulduktan sonra çözünürlük ölçümüyle (`12` §3 C7) birlikte koşmak.

- Bugünkü kollar (tek merkez karıştırıcı, eşler arası trafik) Y4–Y5 ile
  değişecek. Referans kararı eski hücrede verilirse yeniden verilmesi gerekir.
- Şimdi koşulursa süre tahmini (bant, ölçüm değil): 10 tohum 45–70 dk, 5 tohum
  22–35 dk. Dayanağı A1'in koşu hızı ve teşhisteki 1,7 kat süre oranı.

### 4.4 · Regresyon tabanı, test takımı ve mimari denetimi

**Regresyon tabanı (Y0).**
`python -u kalibrasyon/regresyon_satirlari.py uret taban_2026-09-11b`

| üretim | vaka | süre | en uzun vaka | hata |
|---|---|---|---|---|
| `taban_2026-09-11` (ilk matris) | 38 | 32,4 dk | `a-bagimsiz-reaktif-en_yakin_kimlik` 1330 s | 0 |
| `taban_2026-09-11b` (küçültülmüş, **geçerli taban**) | 35 | 19,2 dk | `e-bagimsiz-surekli-kontrol_sinav` 699 s | 0 |

- Bütün satırlarda korunum geçerli.
- **Belirlenimcilik:** `… karsilastir taban_2026-09-11 taban_2026-09-11b`
  - İki matrisin ortak 23 vakası alan alan birebir aynı.
  - Farklı olan yalnız her koşuda değişmesi gereken iki kimlik alanı.
  - Ortak vakalar tam uzunluğu, iki kâhini, yüklü beacon'ı ve kontrol sınavını
    kapsıyor.
  - Aletin çıkışı "FARK VAR" diyor, çünkü matris değişti (27 vaka yalnız bir
    dosyada). Alan farkı yok.
- Araç özeti iki üretimde aynı çıktı. Arada yalnız ölçüm aletleri değişti;
  demek ki özet onları kapsamıyor.
- Sonraki her `sim2` adımı `taban_2026-09-11b`ye karşı karşılaştırılır. Bandı
  bu makinede, 10 işçiyle 17–25 dk; ölçülen 19,2 dk.

**Test takımı.** `python -m pytest tests2 -q` → `503 passed` (478 s; kısmen 3
süreçli bir koşumla eşzamanlı).

**Mimari denetimi.** `python kalibrasyon/mimari_denetimi.py`

- Yapısal ihlal yok · 105 modül, içe aktarılamayan 0.
- 131 parametre: TÜRETİLMİŞ 43 · ÖLÇÜLMÜŞ 12 · KAYNAK 6 · DUYARSIZ 18 ·
  TEDAVİ 11 · KOL TANIMI 6 · SINANMAMIŞ 35.
- Duyarlılık borcu 5 · D13 taranan sabit 34 · 11 not.
- Bu turda `sim2`ye dokunulmadı.

## BUNU NE DEĞİŞTİRİR

- Öğrenci 11 Eylül'de yapıyı (Y1, Y3–Y7, Y10), veri onayı düzeltmesini (Y2) ve
  üst referansın yeni çekirdek hücrede ölçülmesini onayladı. `sim2`
  değişiklikleri `07` §18.1 sırasıyla yazılır; her adım regresyon ve test
  koşusuyla kapanır (K-115).
- M4'ün eşiği bugünkü hâliyle, kopma beyan eden bir protokol yazıldığında
  güvenilmez; düzeltmesi Y10.
- Uzun ölçümlerde süre artık kapıda ölçülüyor ve sonuçlar anında diske
  yazılıyor.
- Veri onayı kusurunun PDR'ye etkisi 8 hücrenin 5'inde çözünürlük altında, 3'ünde
  kararsız; hiçbirinde üstünde değil. Düzeltme kararı öğrencinin (§4.2).
  Düzeltilirse Y2'nin kapısı ölçüm aletinin `duzeltilmis` kipidir.

---

# K-115 · 🟡 YAPI ADIMLARI — Y1 uygulandı: PSR alıcı tarafında, kontrol istatistikleri sayaç kütüğünde

> **Tarih:** 11 Eylül 2026 · **Karar:** öğrenci (K-114 üçüncü tur: yapı Y1,
> Y3–Y7, Y10 ve veri onayı düzeltmesi) · **Uygulama:** ajan ·
> **Durum:** Y1 kodlandı; test takımı ve mimari denetimi geçti; regresyon
> karşılaştırması sürüyor.
> **Üreticiler:** `python -m pytest tests2 -q` ·
> `python kalibrasyon/mimari_denetimi.py` ·
> `python -u kalibrasyon/regresyon_satirlari.py uret y1_2026-09-11` ·
> `python -u kalibrasyon/regresyon_satirlari.py karsilastir taban_2026-09-11b y1_2026-09-11 --izin …`

## 1 · Y1 — ne değişti

**PSR (`07` §08.2, öğrencinin tanımı)**

- Yeni sayaç `veri_alim_hedefte`: adreslenen alıcının gövdeyi hatasız çözdüğü
  veri iletimi, tekrarlar dâhil. Veri teslim işleyicisinde, tekrar
  denetiminden önce artar.
- `psr = veri_alim_hedefte / mac_deneme`, tüm koşu ve pencere ikizi.
- Onaya dayalı eski oran silinmedi, adı `mac_basari_orani` oldu. İkisinin farkı
  onay kaybının kendisidir.
- ⚠️ 11 Eylül'den önce kaydedilmiş `psr` değerleri onaya dayalı tanımdır: K-114
  §4.2'deki "bugünkü `psr`" ve daha eski kayıtlardaki PSR aralıkları.

**Kontrol istatistikleri (`13` R8)**

- Kontrol defterinin 13 alanı sayaç kütüğünde `kontrol_<alan>` adıyla, pencere
  ikizleriyle duruyor ve satırın `metrikler` bölümüne giriyor.
- Defterin alan adları artık sayaç kütüğünden türüyor (`kume="kontrol_defteri"`;
  alıcı zincirinin `ALIM_SONUCLARI` deseni). Tek bir sayma yöntemi düğüm
  defterini ve sayacı aynı çağrıda artırıyor; ikisinin ayrışması yapısal olarak
  mümkün değil.
- Tasarımda 10 alan listelenmişti. Uygulanan, defterin bütün alanlarıdır (üst
  küme), çünkü ikinci bir ad listesi tutulmamalı.

**Mesaj biçimi dökümü**

- Teşhiste `kontrol_duzlemi.bicim`: biçim adı → çerçeve · bayt · airtime, tüm
  koşu ve pencere için.
- Pencere sütunu sayaç ikizleriyle aynı tanımı kullanır: pencere başladıktan
  sonraki artış. Bunun için sayaç kütüğüne `pencere_basladi` eklendi.

**Henüz yapılmayanlar** (`07` §08.2'de anılan): bağ başına PSR dağılımı ve
kontrol çerçevelerinin PSR'si.

## 2 · Kapılar

| kapı | test |
|---|---|
| onayı kaybolan iletimde yeni PSR başarı, onaya dayalı oran başarısızlık; tekrar sayılır, başkasına adresli sayılmaz | `test_kosum::test_Y1_PSR_ALICI_tarafinda_…` |
| onay kaybı gözlenen gerçek koşuda PSR > onaya dayalı oran | `test_kosum::test_Y1_PSR_gercek_trafikte_…` |
| her defter alanında Σ düğüm defteri = sayaç; pencere ikizi var; kanıt > 0 | `test_kontrol_duzlemi::test_Y1_her_defter_alani_…` |
| kontrol düzlemi kullanmayan protokolde sayaçlar sıfır, teşhis bölümü yok | `test_kontrol_duzlemi::test_Y1_kontrol_KULLANMAYAN_…` |
| biçim dökümü havaya çıkan kontrol çerçeveleriyle birebir: sayı, bayt, airtime | `test_kontrol_duzlemi::test_Y1_mesaj_bicimi_…` |

## 3 · Sonuçlar

- **Test takımı:** `508 passed` (503 + 5 yeni kapı; 877 s, regresyonla eşzamanlı).
- **Mimari denetimi:** yapısal ihlal yok · 105 modül · 131 parametre, kovalar
  değişmedi · D13 34 sabit.
- **Regresyon:** `y1_2026-09-11` (20,4 dk, hata 0) ↔ `taban_2026-09-11b` →
  `🟢 BIREBIR (izinli farklar disinda)`, **35/35 vaka bulgusuz**.
  - Farklı olanlar yalnız önceden yazılmış alanlar: sayaç şeması özeti,
    `psr`, `mac_basari_orani`, `veri_alim_hedefte`, 13 `kontrol_*` sayacı (hepsi
    pencere ikizleriyle) ve kontrol sınavı vakalarında biçim dökümü.
  - `psr` 35 vakanın 15'inde değişti. Değişmeyen 20 vakanın hepsinde onayı
    kaybolan iletim 0, alım = onaylı başarı; beklenen budur. Değişen 15 vakada
    alım − onaylı başarı ≤ `mac_onaysiz_onay` (ör. tam uzunluk kâhin vakasında
    370 ≤ 407).

## 4 · Fark edilen ve kayda geçen

- **Pencere ikizinin boşalma payı** (`12` §3 A8). Sayım ikizleri pencere
  başından koşu sonuna kadar sayıyor. Boşalma aralığında periyodik kontrol
  sürerken yeni veri doğmuyor, bu yüzden `nrl_*_pencere` şişebilir. Ölçülecek.
- **Araç özeti diskten okunur.** Satır yazılırken `sim2/` dosyalarının özeti o
  anda hesaplanıyor. Çalışan bir koşum bitmeden `sim2`ye dokunulursa sonraki
  satırlar çalıştırmadıkları kodun özetini taşır. **Kural:** koşum bitmeden
  `sim2` değişikliği yapılmaz.

## 5 · Y2 — veri onayı yalnız göndericinin kendisi çözdüğünde

**Karar:** öğrenci, 11 Eylül — K-114 §4.2'deki ölçümden sonra.

**Değişiklik**

- `teslim.onay_alindi` onayı çözen düğümü alıyor ve yalnız o düğüm
  göndericinin kendisiyse işliyor; seyircinin çözdüğü onay yok sayılıyor.
  Kontrol düzleminin onay kuralıyla aynı.
- Çözen düğümü koşu döngüsü veriyor; başka çağrı noktası yok.
- Ölçüm aleti (`onay_semantigi.py`) güncellendi:
  - `mevcut` kip eski kusuru BİLEREK yeniden üretiyor: seyircinin çözdüğü
    onayı gönderen çözmüş gibi işliyor.
  - Kapı 1 artık "düz koşu = düzeltilmiş kip".
  - Yeni `y2kapi` alt komutu.

**Kapılar**

| kapı | sonuç |
|---|---|
| düz koşu, Y2'den ÖNCE kaydedilmiş `duzeltilmis` parmak izleriyle birebir; 4 kol × 2 kâhin × 2 tohum (`python -u kalibrasyon/onay_semantigi.py y2kapi kisa_2026-09-11`) | 🟢 16/16 `BIREBIR` |
| aletin kendi kapısı (`… --kapi`): düz = düzeltilmiş · `mevcut` kusuru üretiyor · düzeltilmiş kipte seyirci kredisi 0 · korunum | 🟢 dördü OK; seyirci 2929 · 2393, hayalet 10 · 60 — Y2'den önceki kapıyla aynı sayılar |
| seyircinin çözdüğü onay göndereni serbest bırakmıyor | `test_kosum::test_Y2_SEYIRCININ_…` |

Parmak izi alanları (teslim, deneme, kontrol çerçevesi, onaylı başarı, gecikme,
PDR) Y1'den etkilenmiyor; Y1 regresyonu bunu 35/35 birebir gösterdi. Bu yüzden
Y2 öncesi kayıtla karşılaştırma geçerli.

**Sonuçlar**

- **Test takımı:** `509 passed` (508 + 1; 705,6 s, regresyon ve kapıyla
  eşzamanlı).
- **Mimari denetimi:** yapısal ihlal yok · 105 modül · 131 parametre · D13 34.
- **Regresyon** (`y2_2026-09-11`, 19,6 dk, hata 0) ↔ `y1_2026-09-11`: davranış
  bilerek değiştiği için birebirlik aranmadı. 35 vakanın 1'i birebir
  (`b-statik-aldatici-dogrudan_komsu`); 34'ünde metrikler ve ham listeler
  değişti.

**Y2'nin ortaya çıkardığı etki beklenenden büyük.** Tek atlamalı
`dogrudan_komsu` vakaları, Y1 → Y2:

| vaka | onaya dayalı oran | onayı kaybolan iletim | deneme |
|---|---|---|---|
| `b-statik-surekli` | 0,93 → 0,51 | 0 → 316 | 463 → 732 |
| `b-statik-reaktif` | 0,93 → 0,56 | 0 → 266 | 459 → 693 |
| `b-statik-surekli_darbeli` | 0,86 → 0,52 | 0 → 279 | 551 → 776 |
| `b-statik-yok` (karıştırıcısız) | 0,91 → 0,91 | 0 → 1 | 520 → 520 |

- Karıştırıcısız kolda neredeyse hiçbir şey değişmiyor. Karıştırıcılı kollarda
  onay kayıplarının hepsi seyirci kredisiyle gizleniyormuş.
- PDR bu vakalarda değişmedi (ör. 0,263 → 0,263); K-114 §4.2'deki "teslimi
  değil, göndericinin bilgisini bozuyor" teşhisiyle tutarlı.
- *Yorum:* tek atlamalı bağlar kısa; alıcı ve seyirciler onayı güçlü alıyor,
  karıştırıcı ise göndericinin onayı almasını bozuyor.

**🔴 Bir kapı kusuru bulundu ve düzeltildi**

- **Belirti:** Y2 regresyonunda `d-bagimsiz-surekli-yuklu` satırı geçersiz
  çıktı; deneme 23 864, sonuç toplamı 23 863.
- **Tanı:** vaka tek başına yeniden koşuldu ve aynı sayıları verdi. Koşu
  sonunda veri onayı bekleyen düğüm tam 1'di (düğüm 36). Olay kuyruğu
  bitişten sonraki olayları işlemiyor; son anda başlayan denemenin onay
  penceresi sınırı aşmıştı.
- **Kusurun yeri:** Y2'nin mantığında değil, iletim sonucu kapısında. Kapıda
  "koşu sonunda sonucu bekleyen deneme" terimi yoktu. Koşular şimdiye kadar
  bitmeden boşaldığı için hiç tetiklenmemişti.
- **Düzeltme:** `korunum.iletim_sonucu_askida` = koşu sonunda onay bayrağı
  kalkık düğüm sayısı; kapı artık `toplam + askıda = deneme`. Onay beklenirken
  düğümün sürümü değişmediği için bu terim orta yerde kaybolmuş bir sonucu
  örtemez.
- **Test:** askıda deneme kapıyı bozmuyor; gerçekten kaybolmuş bir sonuç satırı
  geçersiz yapıyor (`test_kosum::test_ILETIM_SONUCU_…`). Düzeltmeden sonra
  test takımı `510 passed` (801,8 s, regresyonla eşzamanlı).
- **Doğrulama:** regresyon `y2b_2026-09-11` (20,4 dk, hata 0, 35/35 geçerli) ↔
  `y2_2026-09-11` → `🟢 BIREBIR (izinli farklar disinda)`, 35/35 bulgusuz.
  Farklı olan yalnız yeni `iletim_sonucu_askida` alanı (35 vaka) ile o vakanın
  kapı ve geçerlilik alanı (1 vaka). Düzeltme davranışa dokunmadı.
- **`y2b_2026-09-11` yeni regresyon tabanıdır.**

## BUNU NE DEĞİŞTİRİR

- `psr` adı artık öğrencinin tanımıdır; eski oran `mac_basari_orani`.
- Kontrol yükü protokol karşılaştırmasında pencere içinde ve biçim biçim
  okunabilir.
- Veri onayı fiziksel olarak mümkün olanı yapıyor; karıştırmanın gönderici
  tarafındaki etkisi artık gizlenmiyor. Onaya bağlı MAC sayaçları (onaylı
  başarı, onayı kaybolan iletim, `mac_basari_orani`) Y2'den önceki satırlarla
  karşılaştırılamaz. `psr`nin tanımı onaya bağlı değil, ama davranış değiştiği
  için değerleri de değişir.
- Önceki kalibrasyon sayıları (ρ, kâhin PDR'si, Θ) K-114 §4.2'ye göre
  çözünürlük altında ya da kararsız etkilenir; Aşama 1'in yeniden kalibrasyonu
  (C grubu) onları zaten yeniden üretecek.
- Sıradaki adım Y4: yere toplama.

---

# K-116 · 🟢 YAPI ADIMI Y4 — yere toplama deseni uygulandı

> **Tarih:** 11 Eylül 2026 · **Karar:** öğrenci — yere toplama kabulü 10 Eylül;
> öneriler ve yapı onayı 10–11 Eylül; şart: *"projede dürüstlük ve
> gerçekçiliğe sıkıntı çıkarmayacaksa"* · **Uygulama:** ajan ·
> **Durum:** kapandı — test takımı `516 passed`, mimari denetimi temiz,
> regresyon ortak 35 vakada birebir; yeni taban `y4_2026-09-11`.
> **Üreticiler:** `python -m pytest tests2 -q` ·
> `python kalibrasyon/mimari_denetimi.py` ·
> `python -u kalibrasyon/regresyon_satirlari.py uret y4_2026-09-11` ·
> `python -u kalibrasyon/regresyon_satirlari.py karsilastir y2b_2026-09-11 y4_2026-09-11 --izin …`

## 1 · Ne değişti

| parça | uygulama |
|---|---|
| konfigürasyon | `trafik_deseni` (TEDAVİ; varsayılan `esler_arasi`; tedavi alanları kümesine girdi) · `gecit_konumu` (KOL TANIMI; `kenar` · `merkez`) · `telemetri_paket_hizi_hz` 1,0 · `komut_akis_sayisi` 4 · `komut_paket_hizi_hz` 0,25 — son üçü SINANMAMIŞ, C3 seçecek |
| geçit | Düğüm 0. Yörüngesi `GecitliMobilite` ile sabit istasyona bağlanır; iç modelin bütün çekimleri değişmeden tüketilir. Nokta dünya katmanında türetilir: kenar = batı kenarının ortası, merkez = alan merkezi, irtifa bandın ortası |
| trafik | Geçit dışındaki her düğümden geçide bir telemetri akışı; geçitten `komut_akis_sayisi` düğüme komut akışı (hedefler `trafik_ciftleri` akışından). Hız akış başına; faz + titreşim yöntemi aynı. Eşler arası dal birebir aynı |
| kayıp yeri | `teshis.kayip_yeri`: düşüş sebebi × geçide mesafe bandı (0–R · R–2R · 2R+, R = iletim menzili). Korunum defterine giden iki çağrı noktasının ikisinden de beslenir |
| kapsam | `kapsam.trafik_deseni` her satırda. Yere toplamada `kapsam.desen_sinirlari`: geçidin yere bağı ideal · yer istasyonlu mimari yok · tek geçit darboğazı · telemetri hızı kaynaksız |
| regresyon aleti | iki yere toplama vakası: `g-statik-surekli-en_guvenilir_kahin-yere_toplama` · `g-bagimsiz-surekli-dogrudan_komsu-yere_toplama` |

**Onaylı yapıdan farklar** (`07` §18 Y4 "Uygulama"):

- İki geçit uygulanmadı ve `gecit_sayisi` alanı eklenmedi.
- Varsayılan hızlar 40 düğümde bugünkü sunulan yükü (40 pkt/s) korur.

## 2 · Kapılar ve testler

| kapı | test |
|---|---|
| geçit dışındaki her düğümden geçide tam bir telemetri akışı; komutlar geçitten ayrık düğümlere | `test_ag::test_Y4_yere_toplama_HER_DUGUMDEN_…` |
| sunulan yük 40 pkt/s; akış başına doğum sayısı hızına uygun | `test_ag::test_Y4_yere_toplama_URETIM_HIZI_…` |
| bilinmeyen desen ve geçersiz değerler reddedilir; geçit noktası doğru | `test_yapilandirma::test_Y4_…` (2 test) |
| gerçek koşuda defter kapanır · kayıp yeri toplamı = düşen paket · geçit sabit · öteki düğümlerin konumu eşler arası kolla birebir · kapsam beyanı var | `test_kosum::test_Y4_yere_toplama_KORUNUM_…` |
| eşler arası desen birebir | regresyon (§3) |

**Yolda yakalanan.** "Okunan alanlar" sözleşmesi iki alanı yakaladı:

- `gecit_konumu` yalnız konfigürasyonun kendi özelliğinde okunuyordu. Kural,
  bunun davranışı etkilediğini kanıtlamadığını söyler. Geçit noktası dünya
  katmanına taşındı.
- `trafik_deseni`nin tek okuması kapsam raporundaydı. Trafik üretecinin dalı
  artık alanı doğrudan okuyor.

## 3 · Sonuçlar

- **Hedefli testler:** yapılandırma · ağ · topoloji · dünya `131 passed`;
  koşumda Y4 · korunum · iletim sonucu `9 passed`.
- **Duman:** yere toplamada 43 akış (39 telemetri + 4 komut), 12 798 doğum,
  sunulan yük 40,0 pkt/s, geçit (0, 900, 70).
- **Mimari denetimi:** yapısal ihlal yok · 106 modül · 136 parametre (TEDAVİ 12
  · KOL TANIMI 7 · SINANMAMIŞ 38) · duyarlılık borcu 6 · sahipsiz alan 0.
- **Tam test takımı:** `516 passed` (510 + 6 yeni Y4 testi; 857,5 s,
  regresyonla eşzamanlı).
- **Regresyon:** `y4_2026-09-11` (37 vaka, 20,6 dk, hata 0, 37/37 geçerli) ↔
  `y2b_2026-09-11` → ortak 35 vaka **35/35 bulgusuz**.
  - Farklı olan yalnız önceden yazılmış alanlar: kurulum özeti, beş yeni
    konfigürasyon alanı, `kapsam.trafik_deseni`, köken kova sayıları (TEDAVİ ·
    KOL TANIMI · SINANMAMIŞ).
  - Aletin "FARK VAR" çıkışı iki yeni vakanın yalnız yeni dosyada olmasından;
    alan farkı yok.
  - **`y4_2026-09-11` yeni regresyon tabanıdır.**
- **İki yeni vaka** (kısa pencere, betimleyici):

  | vaka | PDR (pencere) | düşen / üretilen | kayıp yeri 0–R · R–2R · 2R+ |
  |---|---|---|---|
  | `g-statik-surekli-en_guvenilir_kahin-yere_toplama` | 0,9925 | 55 / 1 600 | 1 · 0 · 54 |
  | `g-bagimsiz-surekli-dogrudan_komsu-yere_toplama` | 0,0917 | 1 450 / 1 600 | 30 · 40 · 1 380 |

  İkisinde de kayıp yeri toplamı düşen paket sayısına eşit ve kapsam beyanı
  var. Doğrudan komşu protokolü yalnız hedef komşuysa gönderdiği için çoğu
  paket geçide uzakta "hedef yok" sebebiyle düşüyor; beklenen bu.

## BUNU NE DEĞİŞTİRİR

- Yere toplama artık bir konfigürasyon bayrağı; C1 (düğüm sayısı) ve C3 (yük)
  bu desenle koşulabilir.
- Satırlar desenin sınırlarını kendileri beyan ediyor.
- Sıradaki adım Y5: çoklu hareketli karıştırıcı.

---

# K-117 · 🟢 YAPI ADIMI Y5a — çoklu ve hareketli karıştırıcı mekanizması

> **Tarih:** 11 Eylül 2026 · **Karar:** öğrenci — çoklu hareketli karıştırıcı
> modeli 10 Eylül, yapı onayı 11 Eylül · **Uygulama:** ajan ·
> **Durum:** 🟢 kapandı — hedefli testler, mimari denetimi, tam test takımı
> (524) ve regresyon (37/37 birebir) geçti. Y5b (ailelerin sayıları) öğrenci
> kararını bekliyor (`07` §05.3.1).
> **Üreticiler:** `python -m pytest tests2 -q` ·
> `python kalibrasyon/mimari_denetimi.py` ·
> `python -u kalibrasyon/regresyon_satirlari.py uret y5a_2026-09-11` ·
> `python -u kalibrasyon/regresyon_satirlari.py karsilastir y4_2026-09-11 y5a_2026-09-11`

## 1 · Neden ikiye ayrıldı

Öğrencinin verdiği saha sentezi aileleri, platformları ve yayın düzenlerini
tanımlıyor; ama güç, hız ve süreler için doğrulanabilir sayısal saha verisi
olmadığını kendisi söylüyor. Ailelerin sayıları bu yüzden bir gerçekçilik
kararıdır (Y5b). Mekanizma ise onaylı yapının kodudur ve sayılardan
bağımsızdır (Y5a).

## 2 · Ne değişti — `sim2/kanal/karistirici.py`

| parça | uygulama |
|---|---|
| tanım | `Yorunge(baslangic, tur, hiz_ms, yon_rad)` · `Yayin(duzen, ofset_s, acik_s, sessiz_s)` · `KaristiriciTanimi(platform, yorunge, yayin, sinif, guc_payi)`; hepsi donmuş veri, doğrulamalı |
| konum | `konum_t(t)` zamanın saf fonksiyonu: `sabit` · `dogrusal` (ölçekli hız, koşu başından). Devriye, Y5b'nin aileleri isterse eklenir |
| yayın | `devrede_mi(t)` tanımlı üyede çizelgeyi de uygular: `surekli` · `gorev_cevrimli` · `yay_sus_tasin`, açılma anına göre ofsetle. Geçişler parça sınırına eklenmez — açılma anıyla aynı beyan |
| güç | üye başına `guc_payi` çarpanı |
| gölgeleme | üye başına kimlik `-(indeks + 1)`; ilk üye bugünkü `-1` |
| rastgelelik | aynı sınıftan üyelerin hash çekimleri bağımsız: indeks > 0 anahtara eklenir, ilk üyenin anahtarı aynı kalır |
| küme | `KaristiriciKumesi`: güç toplamı · geçiş anları birleşimi · CSMA görünürlüğü herhangi bir üye |
| taşıyıcı dinleme | yeni `csma_guc_w`: yalnız CSMA'ya görünen üyelerin gücü. İki çağrı noktası (`girisim.kanal_mesgul_mu`, `Dugum.karistirici_mesgul_mu`) buna geçti; tek karıştırıcıda eski iki adımlı denetimle aynı |
| kurucu | `karistirici_kur(..., tanimlar=None)`: tanım yoksa bugünkü tek merkez karıştırıcı birebir; tek tanım doğrudan üye; birden çok tanım küme |

Konfigürasyona yeni alan eklenmedi: tek geçerli değeri olan bir tehdit
senaryosu ekseni yaratmamak için. Eksen, ailelerle birlikte (Y5b) gelecek.

## 3 · Kapılar — `tests2/test_karistirici_kumesi.py`

| kapı | test |
|---|---|
| merkezde tek tanım = varsayılan nesne: aynı sınıf, birebir aynı güç | `test_Y5a_TEK_TANIM_…` |
| küme gücü = üyelerin toplamı; arayüz aynı | `test_Y5a_KUME_gucu_…` |
| taşıyıcı dinleme yalnız görünür üyenin gücüne bakar | `test_Y5a_TASIYICI_DINLEME_…` |
| hareketli üyenin konumu doğrusal ve sürekli; güç zamanla değişir | `test_Y5a_HAREKETLI_…` |
| yayın çizelgesi ilan edildiği gibi; sessizken güç 0; geçersiz süre reddedilir | `test_Y5a_YAYIN_CIZELGESI_…` |
| gölgeleme kimliği üye başına ayrı (−1, −2) | `test_Y5a_GOLGELEME_KIMLIGI_…` |
| açılmadan önce girişim karıştırıcısız kanalla birebir | `test_Y5a_KAPALIYKEN_…` |
| geçersiz platform, alan dışı başlangıç, boş tanım reddedilir | `test_Y5a_TANIM_DOGRULAMALARI` |
| varsayılan yol birebir | regresyon (§4) |

## 4 · Sonuçlar

- **Hedefli testler:** karıştırıcı `31 passed` (8 yeni + mevcut) · kanal
  `100 passed` · koşumda korunum `8 passed`.
- **Mimari denetimi:** ilk koşuda bir not çıktı: `Karistirici` protokolü dışa
  açık ama okunmuyordu, çünkü kurucunun dönüş türü açıklaması yeniden yazımda
  düşmüştü. Açıklama geri kondu. İkinci koşu temiz: yapısal ihlal yok · 107
  modül · okunmayan ad 0 · 136 parametre.
- **Tam test takımı:** `524 passed in 862.22s` (516 + 8 yeni; regresyonla
  eşzamanlı koştu).
- **Regresyon:** `y5a_2026-09-11` üretimi 20,8 dk, 37/37 geçerli, hata 0.
  `karsilastir y4_2026-09-11 y5a_2026-09-11` → bulgusuz vaka 37/37; farklı
  alanlar yalnız `kimlik.arac_hash`, `kimlik.kosu_kimligi`,
  `kimlik.calisma_kimligi`, `kimlik.zaman_damgasi_utc` →
  `🟢 BIREBIR (izinli farklar disinda)`. İzinli önek verilmedi.

## BUNU NE DEĞİŞTİRİR

- Karıştırıcı kümesi ve hareketli üye artık kurulabiliyor. Y5b yalnız aileleri
  tanımlayacak ve konfigürasyona `tehdit_senaryosu` eksenini ekleyecek.
- Kâhin grafiğinin tazeleme süresine karıştırıcıların en büyük hızı, hareketli
  aileler gelince (Y5b) katılacak.
- C2 (çalışma noktası) Y5b'yi bekliyor.

---

# K-118 · 🟢 YAPI ADIMI Y6 — formasyon kolu ve istasyon tutma

> **Tarih:** 11 Eylül 2026 · **Karar:** öğrenci — mobilite önerisi 10 Eylül,
> yapı onayı 11 Eylül, duvar teması kapısı 11 Eylül dördüncü tur (K-119) ·
> **Uygulama:** ajan ·
> **Durum:** 🟢 kapandı — hedefli testler, mimari denetimi, tam test takımı
> (531) ve regresyon (37/37 birebir, ilan edilmiş dört alan dışında) geçti.
> **Üreticiler:** `python -m pytest tests2 -q` ·
> `python kalibrasyon/mimari_denetimi.py` ·
> `python -u kalibrasyon/formasyon_olcumu.py` ·
> `python -u kalibrasyon/regresyon_satirlari.py uret y6_2026-09-11` ·
> `python -u kalibrasyon/regresyon_satirlari.py karsilastir y5a_2026-09-11 y6_2026-09-11 --izin konfig.istasyon_kayma_hiz_ms,kimlik.kurulum_hash,kimlik.akis_listesi_hash,teshis.koken_kovalari --yeni h-`

## 1 · Ne değişti

| parça | uygulama |
|---|---|
| kol | `MOBILITE_KOLLARI`na `formasyon`; senaryo sayısı 18 → 24 |
| model | `dunya/mobilite.py::Formasyon3B`: istasyon = yerleşim çekimi, dolayısıyla t = 0 statik kolla aynı ve yoğunluk eşitlemesi gereksiz |
| ortak fizik | istasyon tutma döngüsü görev kolundan `_istasyonlari_izle`ye taşındı; iki kol aynı kodu kullanır. Görev kolunun satırları bu yüzden regresyonla birebir sınanır |
| gürültü | `gm_alfa` ve `gm_hiz_sigma_ms`ten; tutma zaman sabiti `ISTASYON_TUTMA_S`. Yeni serbest sayı yok |
| rastgelelik | yeni sıralı akış `formasyon_jitter`: önce düğüm başına kayma yönü (kayma sıfırken de çekilir), sonra tik → düğüm → eksen gürültüsü. `akis_listesi_hash` değişti |
| keşifsel eksen | `Konfig.istasyon_kayma_hiz_ms` — çekirdekte 0, KOL_TANIMI, duyarlılık borcu 6 → 7. Her istasyon düğüm başına bir yatay yönde bu hızla kayar ve kenarda geri döner |
| teşhis | `Formasyon3B.duvar_temasi`: yansıyan düğüm-tik sayısı |
| mimari denetimi | belirlenimcilik ve "t = 0 yerleşimi aynı" bölümlerine formasyon eklendi |
| regresyon aleti | formasyon çapraz çarpıma girmez; iki `h-` vakası (tek atlama + kâhin). `karsilastir --yeni`: bilerek eklenen vaka ayrı basılır, geçersizse bulgudur |

## 2 · Onaylı yapıdan farklar

- **Duvar teması kapısı.** Onaylı yapı "duvara temas 0" diyordu; tutmadı (§3).
  Öğrenci "nadir kabul et, say ve beyan et" seçeneğini seçti (K-119). Kapı:
  5 tohumda temas payı < %0,1 ve sayaç ayrıca sınanır.
- **Regresyon matrisi.** Formasyon tam çarpıma girseydi 8 vaka (~1 900
  işlemci-saniye) eklenir ve üretimin üst bandı 30 dk'yı aşardı. Kolun kendi
  yolu iki vakayla sınanır; mobilite × karıştırıcı etkileşimi öteki hareketli
  kollarda sınanıyor.
- **Θ** henüz ölçülmedi (C4, Y7).

## 3 · Ölçüm — 10 tohum (1000–1009) × 350 s

| büyüklük | değer |
|---|---|
| istasyondan sapma: ortalama · p99 ortalaması · en büyük | 0,86 m · 1,89 m · 2,73 m |
| ortalama yatay · dikey sapma | 0,67–0,71 m · 0,41–0,44 m (tohum aralığı) |
| duvar teması | 58 / 280 400 düğüm-tik (%0,021); tohum başına 0–16 |

İstasyonu tabana ya da tavana birkaç metre yakın düşen düğümler manevra
gürültüsüyle sınıra değip yansıyor.

**Komşu çiftlerin bağıl hızı** (teşhis, Θ değil; çift mesafesi ≤ 530 m,
pencere [50, 320] s, 5 s örnekleme):

| kol | ortalama m/s | p50 | p95 |
|---|---|---|---|
| statik | 0,000 | 0,000 | 0,000 |
| bağımsız | 0,677 | 0,676 | 1,195 |
| görev | 0,576 | 0,570 | 1,168 |
| formasyon | 0,168 | 0,161 | 0,294 |

Formasyon, hareketli kolların yaklaşık dörtte biri bağıl hızda; Θ'sının yüksek
çıkması beklenir.

⚠️ Sıra: önce taklit gürültü akışlı bir prototip ölçüldü (temas %0,021, sapma
ortalaması 0,87 m, en büyük 2,83 m). Test sınırları (en büyük < 10 m, ortalama
< 2 m, temas payı < %0,1) prototipe bakılarak ve gerçek ölçümden ÖNCE yazıldı;
gerçek ölçüm aynı yere düştü.

## 4 · Kapılar — `tests2/test_formasyon.py` (7 test)

| kapı | test |
|---|---|
| kol, senaryolar, sınıf | `test_Y6_formasyon_bir_MOBILITE_KOLU` |
| t = 0 statik kolla aynı (5 tohum) | `test_Y6_t0_konumlari_STATIK_KOLLA_AYNI` |
| sapma sınırlı, bütün konumlar kutuda | `test_Y6_istasyondan_SAPMA_SINIRLI_ve_hepsi_KUTUDA` |
| temas nadir | `test_Y6_duvar_temasi_NADIR` |
| temas sayacı çalışıyor | `test_Y6_duvar_temasi_SAYACI_calisiyor` |
| aynı tohumda birebir | `test_Y6_ayni_tohum_BIREBIR` |
| kayma sıfırda sabit, pozitifte kayar; çekim sayısı aynı | `test_Y6_istasyon_KAYMASI_sifirda_SABIT_pozitifte_KAYAR` |

## 5 · Sonuçlar

- **Hedefli testler:** `183 passed` (formasyon · dünya · topoloji ·
  yapılandırma · çekirdek).
- **Mimari denetimi:** yapısal ihlal yok · 108 modül · Konfig 80 alan (76
  okunan) · sıralı akış 19 · 137 parametre (KOL_TANIMI 8) · duyarlılık borcu 7
  · 11 not.
- **Tam test takımı:** `531 passed in 940.24s` (524 + 7 yeni; regresyonla
  eşzamanlı koştu).
- **Regresyon:** `y6_2026-09-11` üretimi 23,2 dk (bant 19–28), 39/39 geçerli,
  hata 0. Karşılaştırmadan ÖNCE ilan edilen beklenen farklar:
  `konfig.istasyon_kayma_hiz_ms` (yeni alan) · `kimlik.kurulum_hash` (konfig
  sözlüğü büyüdü) · `kimlik.akis_listesi_hash` (yeni akış) ·
  `teshis.koken_kovalari` (KOL_TANIMI 7 → 8). Sonuç: bulgusuz vaka 37/37;
  farklı çıkan alanlar tam olarak bu dördü (izinli, 37 vakada) ve her koşuda
  değişen dört kimlik alanı → `🟢 BIREBIR (izinli farklar disinda)`. İki `h-`
  vakası yeni ve geçerli. İstasyon tutma döngüsünün görev kolundan taşınması
  dokuz görev vakasında birebir doğrulandı.
  `h-formasyon-surekli-en_guvenilir_kahin` 585 s sürdü (tahmin ~430 s).

## BUNU NE DEĞİŞTİRİR

- Mobilite ekseni dört kol. C4 (Θ) formasyonu da ölçmeli; Y7 tablosu dört kolu
  taşır.
- `ISTASYON_TUTMA_S`in duyarlılık borcu artık iki kolu birden etkiliyor.

---

# K-119 · 🟢 ÖĞRENCİ KARARLARI — Y5b aileleri, süreler, uzun koşu, derin sızma hareketi, yerleşim, formasyonda duvar teması

> **Tarih:** 11 Eylül 2026 (dördüncü tur) · **Karar:** öğrenci · **Kayıt:** ajan

| # | soru | karar |
|---|---|---|
| 1 | Karıştırıcı senaryo aileleri ve üye sayıları (`07` §05.3.1) | **Öneri olduğu gibi:** `tekli_merkez` (1, referans) · `cephe_hatti` (3, geçidin karşı kenarı boyunca) · `derin_sizma` (1 yer aracı, yay–sus–taşın, gerçek hızla) · `hedef_koruma` (2, görev bölgesinde, görev çevrimli) · `hava_eslik` (1 hava platformu, doğrusal geçiş). Toplam ortalama yayılan güç her ailede eşit |
| 2 | Süre eksenlerinin çekirdek noktaları | **Öneri olduğu gibi:** açık 15 s · sessiz 15 s · hedef korumada %50 görev çevrimi, periyot 30 s. Keşifsel: açık 3 s ve 45 s · sessiz 5 s ve 45 s · periyot 6 s. Taşınma mesafesi = gerçek hız × sessiz süre |
| 3 | ~2 000 s'lik uzun koşu keşifsel eksene girsin mi | **Şimdilik hayır.** Çekirdek 350 s'de kalınır; hareketin koşu içi etkisinin yayın düzeni ve hava geçişiyle sınırlı ölçüldüğü beyan edilir. Aşama 2 ile paralel sonradan eklenebilir |
| 4 | Formasyon kolunda duvar teması sıfır değil (K-118 §3) | **Nadir kabul et, say ve beyan et.** İstasyonlar yerleşim noktalarının aynısı kalır |
| 5 | Derin sızma aracı nasıl hareket etsin? Tablodaki "~90 m" sürekli hareketle hesaplanmıştı; "taşınma = hız × sessiz süre" ise yalnız susarken yer değiştirmeyi söylüyor | **Yalnız susarken taşınsın.** Yayın yaparken durur; 15 s / 15 s düzeninde koşu sonuna kadar ~32 m ilerler. Tablodaki ~90 m düzeltildi |
| 6 | Ailelerin alan içindeki yerleşim kuralları | **Kabul:** cephe hattı doğu kenarında y = 1/6 · 1/2 · 5/6 · hedef koruma x = 0,75, y = 1/4 · 3/4 · derin sızma alan merkezinden batıya (geçide) · hava eşlik kuzeye uçar, karıştırılmış evrenin ortasında alan merkezinden geçer · tekli merkez bugünkü gibi. Geçit merkezdeyse ve eşler arası desende de aynı yerler |

## Sonuç

- Y5b'nin önündeki karar engeli kalktı; uygulama §18.1 sırasında Y6'dan sonra
  gelir. Onaylı yapının (`07` §18 Y5) sayıya çevrilmesinde gereken türetmeler
  (üyelerin alan içindeki noktaları, süre ve hız alanlarının kovaları)
  uygulama kaydında ayrıca yazılır ve öğrenciye raporlanır.
- C2 (çalışma noktası) Y5b uygulandıktan sonra koşabilir.

---

# K-120 · 🟢 YAPI ADIMI Y5b — tehdit senaryosu aileleri

> **Tarih:** 14 Eylül 2026 · **Karar:** öğrenci — aileler, süreler, uzun koşu,
> derin sızma hareketi ve yerleşim kuralları 11 Eylül (K-119) ·
> **Uygulama:** ajan ·
> **Durum:** 🟢 kapandı — hedefli testler, mimari denetimi, tam test takımı
> (542) ve regresyon (39/39 birebir, ilan edilmiş alanlar dışında) geçti.
> **Üreticiler:** `python -m pytest tests2 -q` ·
> `python kalibrasyon/mimari_denetimi.py` ·
> `python -u kalibrasyon/regresyon_satirlari.py uret y5b_2026-09-14` ·
> `python -u kalibrasyon/regresyon_satirlari.py karsilastir y6_2026-09-11 y5b_2026-09-14 --izin konfig.tehdit_*,kimlik.kurulum_hash,kapsam.tehdit_senaryosu,kapsam.modellenmeyen.hareketli_karistirici,kapsam.modellenmeyen.havadan_karistirici,teshis.koken_kovalari --yeni i-`

## 1 · Ne değişti

| parça | uygulama |
|---|---|
| eksen | `Konfig.tehdit_senaryosu` — TEDAVİ, beş değer, varsayılan `tekli_merkez`. Trafik deseni gibi senaryo adına girmez; `TEDAVI_ALANLARI`na eklendi |
| aileler | yeni `sim2/kanal/tehdit.py`: aileyi `KaristiriciTanimi` demetine çevirir. `tekli_merkez` tanım ÜRETMEZ → bugünkü tek merkez karıştırıcı birebir kurulur |
| yerleşim | eşit aralık ve simetriden türer (K-119): cephe hattı doğu kenarında y = (2i+1)/6 · hedef koruma x = 0,75, y = (2i+1)/4 · derin sızma merkezden batıya · hava eşlik kuzeye, karıştırılmış evrenin ortasında merkezden geçecek başlangıçla |
| hareket | yeni yörünge türü `sessizde`: hız YALNIZ sessiz dönemlerde işler (yay–sus–taşın); açılmadan önce ve yayın sırasında platform yerinde durur |
| süreler | üç yeni alan — açık 15 s · sessiz 15 s · görev çevrimi periyodu 30 s (KOL_TANIMI; duyarlılık borcu 7 → 10) |
| hızlar | iki yeni alan — araç 60 km/h · hava 200 km/h (SINANMAMIŞ; ölçekli hız = km/h ÷ 3,6 ÷ `olcek`) |
| güç | üye güç payı = 1 / (K × açık oranı): toplam ORTALAMA yayılan güç tek merkezinkine eşit. Sınıf içindeki darbe telafisinin ÜSTÜNE uygulanır |
| kâhin | grafiğin tazeleme süresi düğüm–karıştırıcı bağıl hızını da hesaba katar; sabit karıştırıcıda ifade bit bit aynı kalır |
| kapsam | her satır `kapsam.tehdit_senaryosu`nu taşır; aile koşarken `kapsam.tehdit_sinirlari` (yerleşim · güç · hızlar · uzun koşu yok). `modellenmeyen` içindeki "hareketli karıştırıcı" ve "havadan karıştırıcı" beyanları güncellendi |
| regresyon | beş yeni `i-` vakası: dört aile tek atlamayla, hava eşlik ayrıca kâhinle (matris 39 → 44) |

## 2 · Onaylı yapıdan farklar ve türetmeler

- **"~90 m" düzeltildi:** onaylı tabloda derin sızmanın koşu içi yolu SÜREKLİ
  hareketle hesaplanmıştı. Öğrenci "yalnız susarken taşınsın" dedi (K-119);
  15 s / 15 s düzeninde koşu sonuna kadar yol ~32 m'dir.
- **Yerleşim sayıya çevrildi:** onaylı tablo yerleri sözel tarif ediyordu.
  Eşit aralık ve simetri kuralı önerildi ve onaylandı; serbest sayı yok.
- **Güç eşitlemesinin formülü:** "toplam ortalama güç eşit" kuralı görev
  çevrimli üyede tepe gücü açık oranına böler — `derin_sizma` tepe payı 2 ·
  `hedef_koruma` üye başına 1 · `cephe_hatti` üye başına 1/3.
- **`sessizde` yeni bir mekanizmadır:** Y5a'nın yayın belgesi "sessizlikte yer
  değiştirme yörüngeden gelir" diyordu; yörünge türü şimdi eklendi ve
  çevrimsiz yayınla birleştirilmesi reddediliyor.
- **Uzun koşu yok** (K-119): hareketin koşu içi etkisi yayın düzeni ve hava
  geçişiyle sınırlı ölçülür; kapsam satırında beyan edilir.

## 3 · Kapılar — `tests2/test_tehdit_senaryolari.py`

| kapı | test |
|---|---|
| beş aile · varsayılan tekli merkez · bilinmeyen ad reddedilir | `test_Y5b_bes_AILE_…` |
| tekli merkez tanım üretmez, bugünkü nesne; karıştırıcısız senaryoda küme yok | `test_Y5b_tekli_merkez_…` |
| üye sayıları ve Σ (güç payı × açık oranı) = 1 | `test_Y5b_uye_SAYILARI_…` |
| yerleşim kuralları | `test_Y5b_YERLESIM_KURALLARI` |
| hava eşlik karıştırılmış evrenin ortasında merkezden geçer | `test_Y5b_hava_eslik_…` |
| derin sızma yalnız susarken taşınır; toplam yol = hız × sessiz süre | `test_Y5b_derin_sizma_…` |
| küme kurulur ve açık dönemde güç verir | `test_Y5b_KUME_…` |
| hedef koruma görev çevrimi ilan edildiği gibi | `test_Y5b_hedef_koruma_…` |
| konfig ve yörünge doğrulamaları | `test_Y5b_KONFIG_ve_YORUNGE_DOGRULAMALARI` |
| kâhin tazelemesi karıştırıcı hızını katar | `test_Y5b_kahin_tazelemesi_…` |
| kapsam satırı aileyi ve sınırlarını yazar | `test_Y5b_KAPSAM_…` |

## 4 · Sonuçlar

- **Hedefli testler:** `75 passed` (tehdit · karıştırıcı kümesi · yapılandırma
  · formasyon).
- **Mimari denetimi:** yapısal ihlal yok · 111 modül · Konfig 86 alan (82
  okunan) · 145 parametre (TEDAVI 13 · KOL_TANIMI 11 · SINANMAMIS 42) ·
  duyarlılık borcu 10 · 11 not.
- **Tam test takımı:** `542 passed in 894.81s` (531 + 11 yeni; regresyonla
  eşzamanlı koştu).
- **Regresyon:** `y5b_2026-09-14` üretimi 22,2 dk (bant 20–29), 44/44
  geçerli, hata 0. Karşılaştırmadan ÖNCE ilan edilen beklenen farklar:
  `konfig.tehdit_*` (altı yeni alan) · `kimlik.kurulum_hash` ·
  `kapsam.tehdit_senaryosu` · `kapsam.modellenmeyen.hareketli_karistirici`
  ve `…havadan_karistirici` (beyan metni) · `teshis.koken_kovalari`.
  Sonuç: bulgusuz vaka 39/39; farklı çıkan alanlar tam olarak bunlar ve her
  koşuda değişen dört kimlik alanı → `🟢 BIREBIR (izinli farklar disinda)`.
  Beş `i-` vakası yeni ve geçerli.
- **Aileler kanala ULAŞIYOR** — kapı boş geçmesin diye ayrıca bakıldı: beş
  yeni vakanın PDR'si 5/5 FARKLI. Aynı tohumda (1007), aynı kolda, yalnız
  aile değişiyor: cephe hattı 0,121 · derin sızma 0,138 · hedef koruma
  0,139 · hava eşlik 0,108 (doğrudan komşu) · hava eşlik kâhinle 0,962.

## BUNU NE DEĞİŞTİRİR

- C2 (çalışma noktası) artık koşabilir: referans güç yeni küme ve yere
  toplamayla yeniden seçilir; ρ her ailede bir SONUÇTUR.
- Evre metriklerinin kapıları hareketli karıştırıcıda yeniden sınanmalı
  (`08`): şok yavaş gelir.
- §18.1 sırasında kalanlar: Y3 → Y7 → Y10 → C1–C7 → D1.

---

# K-121 · 🟢 YAPI ADIMI Y3 — kontrol düzlemi eksikleri (R2 · R3 · R4)

> **Tarih:** 14 Eylül 2026 · **Karar:** öğrenci — yapı onayı 11 Eylül
> (`07` §18 Y3) · **Uygulama:** ajan ·
> **Durum:** 🟢 kapandı — hedefli kapılar, mimari denetimi, tam test takımı
> (551) ve regresyon (44/44 birebir, ilan edilmiş alanlar dışında) geçti.
> **Üreticiler:** `python -m pytest tests2 -q` ·
> `python kalibrasyon/mimari_denetimi.py` ·
> `python -u kalibrasyon/regresyon_satirlari.py uret y3_2026-09-14` ·
> `python -u kalibrasyon/regresyon_satirlari.py karsilastir y5b_2026-09-14 y3_2026-09-14 --izin kimlik.sayac_semasi_hash,metrikler.kontrol_basarisiz_bildirim*,metrikler.kontrol_jitter_*,korunum.kontrol_jitter_tamam,korunum.kontrol_bekleyen_jitter,teshis.kontrol_duzlemi.defter.basarisiz_bildirim,teshis.kontrol_duzlemi.defter.jitter_istenen,teshis.kontrol_duzlemi.defter.jitter_ates,teshis.kontrol_duzlemi.kosum_beaconi_kapali_dugum`

## 1 · Ne değişti

| # | uygulama |
|---|---|
| **R2** | Kontrol düzlemini KULLANAN protokol `kosum_beaconi = False` bildirebilir; o düğümlerde koşum beacon'ı hiç çizelgelenmez, gözlemdeki komşu listesi boş kalır. Beacon fazları yine KURULUMDA çekilir → çekim dizisi kaymaz. Satırda beyan: `kosum_beaconi_kapali_dugum` |
| **R3** | Beşinci kanca `iletim_basarisiz(dugum, hedef, tur, saat_s)`. MAC bir unicast VERİ ya da KONTROL çerçevesinden vazgeçtiği anda çağrılır; `hedef` uçuştan indirilmeden ÖNCE okunur. Çağrı sayılır (`basarisiz_bildirim`) |
| **R4** | `KontrolIstegi` ve `Uyandirma` isteğe bağlı `jitter_s` taşır. `U(0, jitter_s)` `protokol_kesif` akışının DÜĞÜM ALT AKIŞINDAN çekilir. İstekte kuyruğa girmeyi geciktirir, uyandırmada gecikmenin üstüne eklenir |
| defter | üç yeni sayaç: `basarisiz_bildirim` · `jitter_istenen` · `jitter_ates`. Titreşim için uyandırmanınkiyle aynı KAPALI denklem: `jitter_istenen = jitter_ates + bekleyen_jitter`; tutmazsa satır `gecerli=False` |
| akış | `protokol_kesif` "henüz kullanılmayan" listesinden ÇIKTI |
| sözleşme | `13` §02.2 · §02.3 · §02.5 · §03.6 · §03.7 · §03.8 |

## 2 · Yapıdan farklar ve türetmeler

- **Beacon'ı yalnız kontrol düzlemli protokol kapatabilir.** Yapı metninde
  yoktu. Kancasız ve beacon'sız bir protokol kalıcı olarak kördür; ölçülen şey
  onun kararı değil körlüğü olurdu. İhlal kurulumda durur.
- **Titreşimli istek `istenen` sayılmadan bekler.** Kuyruğa girmeyi
  geciktirdiği için defter denklemi bozulmaz; ama bekleyen isteğin sessizce
  kaybolmaması için ikinci bir kapalı denklem eklendi.
- **Kanca veri yolunda koşu döngüsünden bağlandı.** Gönderim modülünden
  bağlamak kontrol modülüyle döngüsel içe aktarma yaratırdı.
- **Başarı için ayrı kanca YOK** (yapı metnindeki gerekçe): `son_iletim_sonucu`
  bunu zaten veriyor ve her onayda olay üretmek maliyetli.

## 3 · Kapılar — `tests2/test_kontrol_duzlemi.py` (dokuz yeni test)

| kapı | test |
|---|---|
| beacon kapatılınca hiç beacon gönderilmez, komşu listesi boş; AÇIKKEN gönderiliyor (kapı boş geçmesin) | `test_P9_kosum_beaconi_KAPATILABILIR_…` |
| kancasız protokol beacon kapatamaz | `test_P9_kontrol_duzlemsiz_protokol_…` |
| MAC vazgeçince kanca çağrılır; sayaç ile düğüm defteri ve kayıt birebir | `test_P10_MAC_vazgecince_…` |
| dört kanca yetmez, beşincisi zorunlu | `test_P10_DORT_KANCA_YETMEZ_…` |
| titreşim defteri kapalı, koşu geçerli | `test_P11_titresim_DEFTERI_KAPALI_…` |
| titreşim aynı tohumda birebir | `test_P11_titresim_AYNI_TOHUMDA_BIREBIR` |
| geçersiz titreşim reddedilir (negatif · NaN · sonsuz) | `test_P11_gecersiz_titresim_REDDEDILIR` |

## 4 · Sonuçlar

- **Hedefli kapılar:** `9 passed` (P9 · P10 · P11); kontrol düzlemi, koşum,
  çekirdek ve ölçüm takımları birlikte `174 passed`.
- **Mimari denetimi:** yapısal ihlal yok · 111 modül · sıralı akış 19, çekim
  alan akış 16 (`protokol_kesif` eklendi) · 145 parametre · 11 not.
- **Tam test takımı:** `551 passed in 947.51s` (542 + 9 yeni; regresyonla
  eşzamanlı koştu).
- **Regresyon:** `y3_2026-09-14` üretimi 22,3 dk (bant 20–29), 44/44
  geçerli, hata 0. Karşılaştırmadan ÖNCE ilan edilen beklenen farklar:
  `kimlik.sayac_semasi_hash` (üç yeni sayaç) · üç yeni sayacın `metrikler`
  alanları ve pencere ikizleri · kontrol düzlemi kullanan satırlarda
  `korunum.kontrol_jitter_tamam`, `korunum.kontrol_bekleyen_jitter` ve
  `teshis.kontrol_duzlemi` altındaki üç defter alanı ile
  `kosum_beaconi_kapali_dugum`. Sonuç: bulgusuz vaka 44/44; farklı çıkan
  alanlar tam olarak bunlar (kontrol düzlemine ait olanlar yalnız İKİ sınav
  vakasında) ve her koşuda değişen dört kimlik alanı →
  `🟢 BIREBIR (izinli farklar disinda)`.

## BUNU NE DEĞİŞTİRİR

- Aşama 2'nin üç ön koşulu kapandı: AODV'nin RERR'i (R3), OLSR'ın
  `MAXJITTER`ı (R4) ve protokol başına beacon kararı (R2) artık YAZILABİLİR.
- §18.1'de kalanlar: Y7 (Θ tablosu) → Y10 (anlamlılık sabitleri) → C1–C7 → D1.

---

# K-122 · 🟢 YAPI ADIMI Y7 — Θ'nın protokol başına raporlanması

> **Tarih:** 14 Eylül 2026 · **Karar:** öğrenci — yapı onayı 11 Eylül
> (`07` §18 Y7); "kapının altındaki kol saklanmaz" kararı 10 Eylül
> (`07` §03.3) · **Uygulama:** ajan ·
> **Durum:** 🟢 kapandı — Θ dört kolda ölçüldü; hedefli kapılar, mimari
> denetimi, tam test takımı (554) ve regresyon (44/44 birebir, ilan
> edilmiş alanlar dışında) geçti.
> **Üreticiler:** `python -u kalibrasyon/theta_kollari.py` ·
> `python -m pytest tests2 -q` · `python kalibrasyon/mimari_denetimi.py` ·
> `python -u kalibrasyon/regresyon_satirlari.py uret y7_2026-09-14` ·
> `python -u kalibrasyon/regresyon_satirlari.py karsilastir y3_2026-09-14 y7_2026-09-14 --izin kapsam.theta_olsr,kapsam.theta_aodv,kapsam.theta_kopmayan_oran,teshis.koken_kovalari`

## 1 · Ölçüm — dört kol, iki payda

| kol | atlama | ölçülen ömür | hiç kopmayan çift | τ_ham | τ_KM | sansür | Θ_OLSR | Θ_AODV |
|---|---|---|---|---|---|---|---|---|
| statik | 3,71 | 0 | %100 | — | — | — | — | — |
| bagimsiz | 5,58 | 405 | %40,4 | 38,8 s | 48,8 s | %15,3 | **3,25** | 16,27 |
| gorev | 4,81 | 538 | %27,5 | 45,4 s | 59,8 s | %19,9 | **3,99** | 19,93 |
| formasyon | 5,06 | 104 | %92,1 | 32,0 s | 34,6 s | %6,7 | **2,31** | 11,53 |

6 tohum × 350 s × 40 çift · bağ tanımı **yavaş SINR ≥ 16 dB**
(`kopma_fiziksel` ile AYNI) · soldan kesme ve Kaplan–Meier düzeltmesi K-101'in
gövdesinden.

🟢 **ÇAPRAZ DOĞRULAMA:** bağımsız kolda Θ_OLSR = 3,25 BİREBİR yeniden üretildi
(K-101'in sayısı). Ölçüm gövdesini kola göre parametrelemek davranışı
değiştirmedi.

## 2 · BULGU — formasyonun Θ'sı AŞAĞI YANLI, ve bu her satırda yazılı

Formasyon kolu Θ_OLSR = 2,31 ile kapının (Θ ≥ 3) ALTINDA görünüyor. Sayı
olduğu gibi okunamaz; sebebi kestiricinin kendisidir:

- her çiftin İLK ömrü atılır (yaşı bilinmez — soldan kesme),
- koşu sonunda yaşayan rota SANSÜRLÜDÜR,
- formasyonda çiftlerin **%92,1'i hiç kopmuyor**; ölçüme yalnız eşiğin
  kıyısında titreyen %7,9 giriyor.

Yani 2,31 kolun tipik rota ömrü DEĞİL, kopan azınlığın ömrüdür — bir ALT
SINIR. Kapının altında görünmesi mobilitenin çalkantısından değil, örneklemin
KİM OLDUĞUNDAN geliyor. ⚠️ Karşılaştırma: kopmayan oranı bağımsızda %40,4,
görevde %27,5; oralarda Θ temsil edicidir.

**Ne yapıldı:** sayı tek başına dolaşmasın diye üçüncü sayı (hiç kopmayan çift
oranı) hem tabloya hem HER SONUÇ SATIRININ kapsam bölümüne kondu; ölçüm aleti
de aynı uyarıyı basıyor.

**Ne YAPILMADI ve neden:** kestirici "ilk ömrü de say" diye gevşetilmedi —
yaşı bilinmeyen bir ömrü saymak K-110'da düzeltilmiş bir yanlılığı geri
getirirdi. Statik kolda Θ tanımsız kalır; bu bir eksiklik değil, kolun
tanımıdır.

## 3 · Ne değişti

| parça | uygulama |
|---|---|
| tablo | `senaryolar.MOBILITE_THETA` — kol başına (Θ_OLSR, Θ_AODV, hiç kopmayan çift oranı); OLCULMUS köken, üretici komutuyla |
| kapsam | her sonuç satırı `theta_olsr` · `theta_aodv` · `theta_kopmayan_oran` taşır |
| ölçüm aleti | yeni `kalibrasyon/theta_kollari.py`. Ölçüm gövdesi `bag_kumesi.py::_is_theta_hiz`tir — İKİNCİ bir kestirici yazılmadı, gövde yalnız senaryoya göre parametreli hâle geldi (altı elemanlı eski çağrı birebir korunur) |
| kopmayan çift | ölçüm gövdesine eklendi: Θ'nın temsil oranı her koşumda basılıyor |
| paydalar | OLSR `TOP_HOLD_TIME` 15 s · AODV `ACTIVE_ROUTE_TIMEOUT` 3 s — ikisi de KAYNAK (RFC 3626 · RFC 3561, `02` §R1–R2) |

## 4 · Kapılar — `tests2/test_yapilandirma.py` (üç yeni test)

| kapı | test |
|---|---|
| tablo kollarla aynı; Θ_AODV = Θ_OLSR × 5; Θ yalnız hiç kopma olmayan kolda `None` | `test_Y7_THETA_tablosu_…` |
| kapsam bölümü üç sayıyı da yazıyor (dört kolda) | `test_Y7_kapsam_THETAYI_…` |
| formasyonun Θ'sı kapının altında AMA kopmayan oranı %90'ın üstünde; bağımsız kolda tersi | `test_Y7_formasyonun_THETASI_ASAGI_YANLI_…` |

## 5 · Sonuçlar

- **Hedefli testler:** `70 passed` (yapılandırma · formasyon · tehdit).
- **Mimari denetimi:** yapısal ihlal yok · 147 parametre (iki yeni modül
  sabiti: Θ tablosu ve AODV paydası) · kökeni yazılmamış 0 · ölü kayıt 0.
- **Tam test takımı:** `554 passed in 934.82s` (551 + 3 yeni; regresyonla
  eşzamanlı koştu).
- **Regresyon:** `y7_2026-09-14` üretimi 22,2 dk, 44/44 geçerli, hata 0.
  Karşılaştırmadan ÖNCE ilan edilen beklenen farklar: `kapsam.theta_olsr` ·
  `kapsam.theta_aodv` · `kapsam.theta_kopmayan_oran` ·
  `teshis.koken_kovalari` (OLCULMUS 12 → 13, KAYNAK 6 → 7). Sonuç:
  bulgusuz vaka 44/44; farklı çıkan alanlar tam olarak bunlar ve her koşuda
  değişen dört kimlik alanı → `🟢 BIREBIR (izinli farklar disinda)`.
  🟢 İLAN EDİLDİĞİ GİBİ `kimlik.kurulum_hash` ve `kimlik.sayac_semasi_hash`
  DEĞİŞMEDİ: Y7 ne `Konfig`e alan ne kütüğe sayaç ekledi.

## BUNU NE DEĞİŞTİRİR

- `07` §03.3'ün "tek sayılı Θ" borcu kapandı: yüksek çalkantı kolu iki Θ ile
  ve etiketiyle raporlanabiliyor.
- **Formasyon kolunun Θ'sı C4'te daha çok tohumla yeniden ölçülmeli:** kopmayan
  oranı yüksek olduğu için kestirici az örnekle çalışıyor. Bu, `12` §3 C4'e
  yazıldı.
- §18.1'de kalan: Y10 (anlamlılık sabitleri) → C1–C7 → D1.

---

# K-123 · 🟢 YAPI ADIMI Y10 — evre metriklerinin TEK anlamlılık sabiti

> **Tarih:** 14 Eylül 2026 · **Karar:** öğrenci — yapı onayı 11 Eylül
> (`07` §18 Y10); "ajan ölçerek en mantıklısını seçsin" 10 Eylül (K-113) ·
> **Uygulama:** ajan ·
> **Durum:** 🟢 kapandı — anlamlılık kapısı, evre testleri, mimari denetimi,
> tam test takımı (555), regresyon (44/44 birebir) ve evre kapıları
> (G1–G4, dördü de GEÇTİ) tamam.
> **Üreticiler:** `python -u kalibrasyon/anlamlilik_sabitleri.py` ·
> `python -m pytest tests2 -q` · `python kalibrasyon/mimari_denetimi.py` ·
> `python -u kalibrasyon/evre_metrikleri_kapilari.py` ·
> `python -u kalibrasyon/regresyon_satirlari.py uret y10_2026-09-14` ·
> `python -u kalibrasyon/regresyon_satirlari.py karsilastir y7_2026-09-14 y10_2026-09-14 --izin metrikler.toparlanma_suresi_s,teshis.koken_kovalari`

## 1 · Ne değişti

| parça | uygulama |
|---|---|
| tek sabit | `olcum/evre.py::ALFA = 0,05`. İki eski sabit (`BANT_SE_KATI = 2,0` · `YANLIS_ALARM = 0,01`) kalktı |
| M3 bandı | `BANT_SE_KATI` artık TÜRETİLMİŞ: `z(1 − α/2)` = 1,95996. Elle 1,96 yazmak α ile ikinci bir doğru kaynağı doğururdu |
| M4 eşiği | pencere BAŞINA `α / taranan pencere` (Bonferroni). Varsayılan kafeste taranan pencere 170, yani pencere başına 2,94e-4 |
| köken | iki SINANMAMIS kayıt bir kayda indi (`evre.py::ALFA`); `BANT_SE_KATI` türetilmiş olduğu için defterden ÇIKTI |
| ölçüm aleti | `anlamlilik_sabitleri.py` artık bir KAPI: bugünkü kuralın aile düzeyi yanlış alarmı `ALFA`yı aşarsa çıkış kodu 1. Eski kural karşılaştırma için AYNI gövdeden koşuyor (aile α'sı `0,01 × taranan pencere` verilerek) — ikinci bir eşik gerçeklemesi yazılmadı |

## 2 · Ölçüm — sentetik boş hipotez (14 Eylül 2026)

4 000 deneme / hücre · pencere [50; 320) · açılma 150 s · taranan pencere 170.

| beyan hızı (1/s) | eski kural (pencere başına 0,01) | bugünkü kural (Bonferroni) |
|---|---|---|
| 0,1 | 0,514 ± 0,016 | **0,022 ± 0,005** |
| 0,5 | 0,374 ± 0,015 | **0,024 ± 0,005** |
| 2,0 | 0,578 ± 0,016 | **0,034 ± 0,006** |
| 10,0 | 0,696 ± 0,015 | **0,030 ± 0,005** |

Hesap (bağımsız pencere varsayımıyla üst sınır): `1 − 0,99^170 = 0,819`.
🟢 **KAPI GEÇTİ:** bugünkü kuralın ölçülen yanlış alarmı aile hedefinin
(α = 0,05) altında, 2 SE marjıyla. 11 Eylül'de ölçülen sayılar birebir yeniden
üretildi (K-114 §A5).

## 3 · Kapılar

| kapı | yer |
|---|---|
| α = 0,05 ve band `z(1 − α/2)` — değerler dondurulmuş | `tests2/test_evre.py::test_evre_kafesi_…` |
| Poisson kuyruk sözleşmesi (iki farklı α'da) | `test_poisson_esigi_kuyruk_orani_TUTUYOR` |
| M4 eşiği Bonferroni ile: λ = 1,0'da eşik 6 (eski kuralda 4); bir pencereye düşen 5 beyan artık tespit DEĞİL, 7 beyan tespit | `test_Y10_M4_esigi_BONFERRONI_ile_kuruluyor` |
| sentetik boş hipotezde aile düzeyi yanlış alarm ≤ α | `kalibrasyon/anlamlilik_sabitleri.py` (çıkış kodu) |

## 4 · Sonuçlar

- **Anlamlılık kapısı:** 🟢 geçti (§2).
- **Evre ve ölçüm testleri:** `54 passed`.
- **Mimari denetimi:** yapısal ihlal yok · 112 modül · 146 parametre
  (SINANMAMIS 42 → **41**: iki kayıt gitti, `ALFA` geldi; `BANT_SE_KATI`
  türetilmiş olduğu için defterde yok) · ölü kayıt 0 · 11 not.
- **Tam test takımı:** `555 passed in 935.64s` (554 + 1 yeni; regresyonla
  eşzamanlı koştu).
- **Regresyon:** `y10_2026-09-14` üretimi 22,2 dk, 44/44 geçerli, hata 0.
  Karşılaştırmadan ÖNCE ilan edilen beklenen farklar:
  `metrikler.toparlanma_suresi_s` (band 2,0 → 1,95996) ·
  `teshis.koken_kovalari` (SINANMAMIS 42 → 41). Sonuç: bulgusuz vaka 44/44;
  farklı çıkan TEK alan `teshis.koken_kovalari.SINANMAMIS` ve her koşuda
  değişen dört kimlik alanı → `🟢 BIREBIR (izinli farklar disinda)`.
  🔒 ÖLÇÜLDÜ: bandın 2,0'dan 1,95996'ya inmesi 44 vakanın HİÇBİRİNDE
  `toparlanma_suresi_s`i oynatmadı — `07` §18 Y10 "çok az değişebilir"
  diyordu, ölçülen değişim SIFIR. `tespit_gecikmesi_s` ilan edildiği gibi
  `None` kaldı (koşum aletleri kopma beyan etmiyor).
- **Evre kapıları (G1–G4):** 🟢 **dördü de GEÇTİ** (15 Eylül 2026, öğrenci
  onayıyla Y10'dan hemen sonra koşuldu). G1 boş kol · G2 tekdüzelik ·
  G3 ızgara fazı · G4 bulanıklık (p99/ızgara 0,021 ve 0,030). Yani tek α'ya
  geçiş evre metriklerinin doğrulama kapılarını kırmadı.

## BUNU NE DEĞİŞTİRİR

- `08` §05.3'ün borcu kapandı: evre metriklerinde tek α var ve ikisi de ondan
  türüyor.
- Ön-kayıt mühürlenirken α tek yerde durur; değiştirilirse band ve eşik
  birlikte değişir.
- §18'in yapı adımları BİTTİ (Y1 · Y2 · Y3 · Y4 · Y5a · Y5b · Y6 · Y7 · Y10).
  Sırada kalibrasyonlar (C1–C7) ve doğrulama listesi (D1) var; Y8 (iz kanalı)
  ve Y9'un ölçüm koşumu keşifsel sırada.

---

# K-124 · 🟢 ÖĞRENCİ KARARLARI — C1 ve C3'ün ölçütleri (taramadan ÖNCE ilan)

> **Tarih:** 15 Eylül 2026 · **Karar:** öğrenci · **Kayıt:** ajan ·
> **Üreticiler:** `python -u kalibrasyon/dugum_sayisi.py` ·
> `python -u kalibrasyon/yere_toplama_yuku.py`

## 1 · Neden ÖNCE ilan

Bu depodaki kural: bir seçim ölçütü TARAMA KOŞULMADAN ÖNCE yazılır. Eski
depoda karıştırıcı gücü ölçütü taramayı gördükten SONRA yazılmıştı ve bu
kayda geçmişti — *"ön-kayıtlı bir seçim değil, betimleyici gerekçe"*. Aynı
tuzağa düşmemek için C1 ve C3'ün ölçütleri burada, ölçüm başlamadan duruyor.

## 2 · C1 · düğüm sayısı

| parça | karar |
|---|---|
| adaylar | 30 · 35 · 40 · 45 · 50 (`12` §3 C1'in aralığı) |
| alan | `1800 m × √(N/40)` — yoğunluk SABİT; 1800 m, N = 40 için ölçülmüş çapadır (`calisma_noktasi.py`). Alan N başına AYRICA taranmaz |
| sert kısıt 1 | statik kolda 30 tohumun HİÇBİRİNDE ulaşılamaz çift yok |
| sert kısıt 2 | yere toplama deseninde geçide DÜĞÜM-AYRIK ikinci yolu olan kaynak oranı ≥ %90 |
| amaç | iki kısıtı da geçen adaylar arasında KOŞU MALİYETİ en küçük N |
| maliyet | ÖLÇÜLÜR (kısa pencereli koşunun duvar saati), varsayılmaz |

**Gerekçe.** N boyutsuzdur ve ölçekle sadeleşmez; derece eşitlenince geriye
tek fiziksel etki DERİNLİK kalır (K-110 §J) ve derinlik zaten alan ölçütüyle
en büyük yapılıyor. Geriye iki şey kalır: yönlendirmeye YER (alternatif yol)
ve MALİYET. Ölçüt bu ikisini bağlar.

⚠️ İkinci kısıt YENİ bir ölçümdür ve tam cevap verir: düğüm bölmeli akışla
hesaplanır. Açgözlü *"bir yol bul, düğümlerini sil, tekrar ara"* yöntemi
ikinci yolu OLDUĞUNDAN AZ bulurdu ve bu bir kapıda kabul edilemez.

## 3 · C3 · yere toplama yükü

| parça | karar |
|---|---|
| eksen | telemetri paket hızı; komut hızı bugünkü oranıyla birlikte gider |
| ölçüt | karıştırıcısız kolda, KÂHİN yönlendirmeyle uçtan uca teslim ≥ 0,95 tutan EN BÜYÜK hız |
| gerekçe | karıştırıcı gücü ölçütünün kardeşi: yük tek başına ağı çökertirse karıştırıcının etkisi ÖLÇÜLEMEZ hâle gelir |

⚠️ Bugünkü varsayılan (telemetri 1,0 · komut 0,25 pkt/s) kaynaksız bir
varsayımdı (`02` §S4). Bu ölçüt onu ya doğrular ya değiştirir.

## 4 · Sıra

C1 → C3 → C2 (alan ve karıştırıcı gücü) → C7 (çözünürlük). Öğrenci 15 Eylül'de
dördünü sırayla koşmayı seçti; N değişirse alan, güç ve Θ onunla birlikte
yeniden seçilir.

---

# K-125 · 🟢 C1 — düğüm sayısı: ölçüm adayları AYIRAMADI, 40 doğrulandı

> **Tarih:** 15 Eylül 2026 · **Ölçüm:** ajan · **Karar:** öğrenci ·
> **Ölçüt:** K-124'te, taramadan ÖNCE ilan edildi.
> **Üretici:** `python -u kalibrasyon/dugum_sayisi.py` (tarama) ve aynı
> aletin işçisiyle koşulan iki teşhis: 120 tohumda kopukluk olasılığı, 30
> tohumda geçide derinlik.

## 1 · Tarama (30 tohum, ilan edilen ölçüt)

| N | alan | derece | kopuk tohum | geçide iki yollu | maliyet |
|---|---|---|---|---|---|
| 30 | 1559 m | 8,09 | 0 | %99,8 | 8,8 s |
| 35 | 1684 m | 8,29 | 1 | %99,6 | 12,1 s |
| 40 | 1800 m | 8,69 | 0 | %99,7 | 13,2 s |
| 45 | 1909 m | 8,93 | 2 | %99,6 | 13,2 s |
| 50 | 2012 m | 9,02 | 1 | %99,5 | 18,5 s |

Ölçüt harfiyen uygulanınca N = 30 çıkıyordu (iki kısıtı geçenler arasında en
ucuz). 🔴 **Ama bu seçim GÜRÜLTÜYE dayanıyordu ve kabul edilmedi.**

## 2 · Neden ayıramadı — iki ölçüm

**(a) Kopukluk gürültüsü.** 120 AYRI tohumla ölçülen kopukluk olasılığı:

| N | 30 | 35 | 40 | 45 | 50 |
|---|---|---|---|---|---|
| olasılık | %1,7 | %0,8 | %0,8 | %2,5 | %3,3 |
| 2·SE | ±2,3 | ±1,7 | ±1,7 | ±2,9 | ±3,3 |

Bütün bantlar çakışıyor: adaylar bu yoğunlukta AYRILAMAZ. Sebebi yapısal —
1800 m zaten *kopukluğun sıfır kaldığı EN BÜYÜK alan* ölçütüyle seçilmişti,
yani yoğunluk çapası uçurumun kenarında duruyor; o yoğunluğu öteki N'lere
taşıyınca hepsi aynı kenarda kalıyor.

🔴 **BU, ESKİ BİR SAYIYI DA TAMAMLIYOR:** 1800 m için kayıtlı *30 tohumda
kopukluk sıfır* gözlemi yanlış değil ama tam değil — aynı nokta 120 tohumla
%0,8 kopukluk veriyor. Çalışma noktası uçurumun kenarındadır ve bu artık
beyan edilmiştir.

**(b) Alternatif yol ayırmıyor.** Geçide düğüm-ayrık ikinci yolu olan kaynak
oranı beş adayda da %98,6–%99,8: kısıt sağlanıyor ama seçim yapmıyor.

## 3 · Ölçütün BULUNAN EKSİĞİ — derinlik korunmuyordu

Ölçüt *derinlik zaten alan seçimiyle en büyük yapılıyor* varsayıyordu. Yanlış:
yoğunluk sabitken derinlik N ile birlikte büyüyor. Ölçüldü (30 tohum, geçide):

| N | 30 | 35 | 40 | 45 | 50 |
|---|---|---|---|---|---|
| ortalama atlama | 2,01 | 2,15 | **2,21** | 2,29 | 2,38 |
| en uzak | 3,23 | 3,43 | 3,63 | 3,67 | 3,90 |

En ucuz aday (30) derinliği 2,21'den 2,01'e indiriyor, yani `07` §09.4'ün
açıkça reddettiği sığ rejime YAKLAŞIYOR. Ölçüt bunu koruyacak bir kısıt
taşımıyordu; eksik sonucu görünce fark edildi ve **ölçüt sonradan
DEĞİŞTİRİLMEDİ** — karar öğrenciye götürüldü.

## 4 · Karar (öğrenci, 15 Eylül 2026)

**N = 40'ta kalındı.** Gerekçe: adaylar iki sert kısıtta istatistiksel olarak
ayrılamıyor; 40, alanı kendi ilan edilmiş ölçütüyle seçilmiş TEK değer ve
derinliği en ucuz adaydan yüksek. Maliyet kazancı (%33) sığ rejime yaklaşma
pahasına alınmadı.

🔒 **Ölçüm N'i SEÇMEDİ, DOĞRULADI.** 40 iki sert kısıtı da geçiyor; seçim bir
KAPSAM kararıdır ve öyle beyan edilir.

## BUNU NE DEĞİŞTİRİR

- `dugum_sayisi` köken kaydı artık ölçüme ve karara dayanıyor.
- Alan, güç ve Θ çapaları DEĞİŞMEDİ; C2 ve C3 bugünkü N ile koşar.
- ⚠️ Çalışma noktasının uçurum kenarında olduğu artık yazılı: alanı büyütmek
  ya da gücü düşürmek kopukluğu hızla açar.

---

# K-126 · 🟢 C3 — yere toplama yükü: ölçüm hızı SEÇMEDİ, 1,0'ı DOĞRULADI

> **Tarih:** 15 Eylül 2026 · **Ölçüm:** ajan · **Karar:** öğrenci ·
> **Ölçüt:** K-124'te, taramadan ÖNCE ilan edildi.
> **Üreticiler:**
> `python -u kalibrasyon/yere_toplama_yuku.py` (tarama · yan gözlem) ·
> `python -u kalibrasyon/yere_toplama_yuku.py marj` (uçurum nerede) ·
> `python -u kalibrasyon/yere_toplama_yuku.py esler` (eksenin öteki yarısı)

## 1 · Ölçüt hangi kolda uygulandı — ve neden hareketli kolda DEĞİL

İlk tasarım taramayı `bagimsiz-yok`ta koşuracaktı. Koşmadan önce ölçülmüş bir
sayı bunu çürüttü: o kolda kâhinin YÜKSÜZ PDR tavanı zaten **0,917**. `≥ 0,95`
orada en düşük yükte bile sağlanamaz; tarama *"hiçbir aday geçmedi"* derdi ve
ölçülen şey yük değil MOBİLİTE olurdu. Ölçüt metni değişmedi; onu ölçen kol
`statik-yok` olarak adlandırıldı (kâhin tavanı ≈ 1,000: PDR'yi 1'den aşağı
çeken TEK şey yüktür).

## 2 · Tarama (3 tohum, statik-yok, kâhin yönlendirme)

| telemetri | komut | sunulan | PDR | 2·SE | ölçüt |
|---|---|---|---|---|---|
| 0,50 | 0,12 | 20 pkt/s | 0,9956 | ±0,0076 | geçer |
| 1,00 | 0,25 | 40 pkt/s | 0,9923 | ±0,0103 | geçer |
| 1,50 | 0,38 | 60 pkt/s | 0,9907 | ±0,0092 | geçer |
| **2,00** | **0,50** | **80 pkt/s** | **0,9841** | ±0,0180 | **geçer** |
| 3,00 | 0,75 | 120 pkt/s | 0,8294 | ±0,1405 | kalır |

Yan gözlem (`bagimsiz-yok`, kısa pencere, **KAPI DEĞİL**): PDR 0,7674. O
koldaki sayı yükün değil mobilitenin sınırını taşır.

🔒 Ölçüt harfiyen uygulanınca **2,00 pkt/s** seçiyordu.

## 3 · Ölçütün BULUNAN EKSİĞİ — eksen dengesi korunmuyordu

`trafik_deseni` bir TEDAVİ eksenidir ve iki seviyesi var. Bugünkü telemetri
hızı keyfi değil; köken kaydı bunu zaten yazıyordu:

> *"Varsayılan, 40 düğümde komutlarla birlikte sunulan yükü bugünkü
> 40 pkt/s'de tutar."*

Aritmetik tutuyor: 39 × 1,0 + 4 × 0,25 = **40,0 pkt/s**, ve `esler_arasi`
tam olarak 10 × 4,0 = **40,0 pkt/s** sunuyor. Telemetriyi 2,0'a çıkarmak o
kolu 80'e taşır, ötekini 40'ta bırakır — ve *"şu desen daha kötü"* bulgusu
İKİ KAT YÜKLE karışır. Ölçüt bu kısıtı taşımıyordu; eksik, sonucu görünce
fark edildi ve **ölçüt sonradan DEĞİŞTİRİLMEDİ** — karar öğrenciye götürüldü.

## 4 · Uçurum nerede — 2,0'ın marjı ölçüldü

| telemetri | sunulan | PDR | 2·SE | tohum tek tek |
|---|---|---|---|---|
| 2,25 | 90 pkt/s | 0,9787 | ±0,0149 | 0,9639 · 0,9849 · 0,9875 |
| 2,50 | 100 pkt/s | 0,9680 | ±0,0309 | **0,9386** · 0,9746 · 0,9909 |

2,50'de TEK TOHUMLAR eşiğin altına düşmeye başlıyor. Yani ölçütün seçtiği
2,0, kendi eşiğinin çiğnenmeye başladığı noktadan yalnız **%25** uzakta;
1,0 ise **%150** uzakta. C1'in dersi buydu: noktanın uçuruma uzaklığı,
noktanın kendisi kadar önemlidir.

⚠️ Sapma yükle büyüyor (2·SE: 0,0103 → 0,0180 → 0,0309 → 0,1405) ve
çözünürlük R = 2·SD/√n olduğu için aynı çözünürlük daha çok tohum ister.
Bu bir İŞARETTİR, ölçülmüş bir sonuç değil: 3 tohumla SD kestirimi zayıftır
ve kesin sayıyı C7 verir.

## 5 · Eksenin öteki yarısı — ilk kez ölçüldü

`esler_arasi` bu ölçütle HİÇ sınanmamıştı (`akis_sayisi` ve
`akis_paket_hizi_hz` kökende SINANMAMIS, gerekçeleri eski çalışma
noktasından kalma):

| akış hızı | sunulan | PDR | 2·SE | ölçüt |
|---|---|---|---|---|
| 4,0 (bugünkü) | 40 pkt/s | 0,9987 | ±0,0026 | geçer |
| 8,0 | 80 pkt/s | 0,9967 | ±0,0036 | geçer |

⭐ Aynı sunulan yükte iki desen çok farklı davranıyor (80 pkt/s'te 0,9967 ↔
0,9841). Sebep yapısal: yere toplama bütün trafiği tek geçide yığar, eşler
arası rastgele çiftlere dağıtır. Yani 40 = 40 eşitliği ZORLUĞU değil,
SUNULAN YÜKÜ eşitler — projenin karıştırıcılar için zaten benimsediği
ilkenin aynısı: *harcananı eşitle, başarılanı değil.*

## 6 · Karar (öğrenci, 15 Eylül 2026)

**Telemetri 1,0 · komut 0,25 pkt/s'te kalındı.** Gerekçe: eksen dengesi
(40 = 40) korunur; 2,0'ın marjı dar; yükü büyütmek çözünürlüğü pahalılaştırır
ve ayırt etme için zaten geniş alan var (karıştırılmış kolda kâhin tavanı
0,96, protokoller ~0,75).

🔒 **Ölçüm HIZI SEÇMEDİ, DOĞRULADI.** 1,0 ölçütü 0,9923 ile geçiyor ve
uçurumdan %150 uzakta. Seçim bir KAPSAM kararıdır ve öyle beyan edilir.

## BUNU NE DEĞİŞTİRİR

- `telemetri_paket_hizi_hz` · `komut_paket_hizi_hz` · `komut_akis_sayisi`
  artık kaynaksız varsayım değil: ölçütle sınandı, marjı ölçüldü.
- ⚠️ `02` §S4 kaynak boşluğu KAPANMADI — 1,0 hâlâ literatür çapası taşımıyor;
  değişen şey, artık ölçülmüş bir ÜST SINIRI ve beyan edilmiş bir GEREKÇESİ
  olması.
- `akis_sayisi` · `akis_paket_hizi_hz` ilk kez bu ölçütle sınandı ve geçti;
  duyarlılık borçları (eski çalışma noktası) DEVAM EDİYOR.
- C7 bugünkü yükte koşar.

---

# K-127 · 🔴 C2 aile kapısı — `hedef_koruma` sert kısıtı ÇİĞNEDİ, çevrim kaldırıldı

> **Tarih:** 15 Eylül 2026 · **Ölçüm:** ajan · **Karar:** öğrenci ·
> **Ölçüt:** DEĞİŞMEDİ — `karistirici_gucu.py`nin yeniden formülasyonu.
> **Üreticiler:**
> `python -u kalibrasyon/karistirici_gucu.py aile` (beş aile) ·
> `python -u kalibrasyon/karistirici_gucu.py acik_evre` (çevrimliler) ·
> `python -u kalibrasyon/karistirici_gucu.py hedef_teshis` (sebep)
>
> 🔒 **§2 ve §3'teki `hedef_koruma` satırları KALDIRILAN tasarımı ölçer.**
> Düzeltme uygulandıktan sonra `aile` ve `acik_evre` bölümleri artık bugünkü
> (sürekli) hâli okur — 0,240 · 0/30. Silinen tasarımın sayıları üreticisiz
> kalmasın diye o varyant `hedef_teshis` bölümünde **V0** olarak YAŞATILDI
> ve iki ızgarada birden koşar. Depodan silinen bir sayının üreticisi de
> silinmiş olurdu; kural 7 bunu kabul etmez.

## 1 · Bu kapı neden vardı ve neden bugüne kadar koşmamıştı

ρ ölçütü beş karıştırıcı **sınıfı** için ölçülmüştü. Y5b'de eklenen beş
tehdit **ailesi** (geometri/sayı ekseni) o ölçütte HİÇ sınanmadı. Sert kısıt
aynen geçerli:

    30 tohumun hiçbirinde BİRDEN FAZLA ÇOK ÜYELİ bileşen yok
    (tek tek boğulmuş düğümler serbest — olgunun kendisi)

⚠️ Ailelerde kısıt DAHA SERTTİR: keskinleşmiş hâli *"bölünme en hızlı tabanın
rota geçersizleme süresinden (3 s, RFC 3561) uzun sürmesin"* diyor.
`cephe_hatti` sürekli yayar (bölünme KALICI olurdu), çevrimli ailelerde açık
evre 15 s. Yani tek bir örnek anında görülen bölünme bile kısıtı çiğner.

## 2 · Sonuç (30 tohum × 9 an, hepsi −15,0 dBm TABAN toplam gücünde)

| aile | K | toplam ort. pay | ρ | ulaş | boğulan | ayrılan | ölçüt |
|---|---|---|---|---|---|---|---|
| tekli_merkez | 1 | 1,000 | 0,258 | 0,994 | 0,13 | 0/30 | geçer |
| cephe_hatti | 3 | 1,000 | 0,142 | 0,990 | 0,20 | 0/30 | geçer |
| derin_sizma | 1 | 1,000 | 0,170 | 0,991 | 0,19 | 0/30 | geçer |
| **hedef_koruma** | **2** | **1,000** | **0,156** | **0,983** | **0,30** | **2/30** | **🔴 kalır** |
| hava_eslik | 1 | 1,000 | 0,260 | 0,993 | 0,15 | 0/30 | geçer |

⭐ İki doğrulama birden:

1. **Eşitleme ÖLÇÜLDÜ, varsayılmadı:** toplam ortalama pay her ailede tam
   1,000 — `tehdit.py::_guc_payi`'nın 1/(K × açık oranı) iddiası tutuyor.
2. **`tekli_merkez` BİREBİR:** ρ 0,258 · boğulan 0,13 · 0/30 — sınıf
   raporundaki `surekli` satırının aynısı. `karistirici_kur`un *"tanım
   verilmezse bugünkü nesne birebir kurulur"* iddiası artık ölçülmüş.

## 2b · Düzeltmeden SONRA — kapı son hâliyle koştu

Düzeltme uygulandıktan sonra kapının tamamı yeniden koşuldu; bir kapının
YAMALI hâlde geçtiğini varsaymak, kapıyı hiç koşmamakla aynı şeydir:

| aile | K | toplam ort. pay | ρ | ulaş | boğulan | ayrılan | ölçüt |
|---|---|---|---|---|---|---|---|
| tekli_merkez | 1 | 1,000 | 0,258 | 0,994 | 0,13 | 0/30 | geçer |
| cephe_hatti | 3 | 1,000 | 0,142 | 0,990 | 0,20 | 0/30 | geçer |
| derin_sizma | 1 | 1,000 | 0,170 | 0,991 | 0,19 | 0/30 | geçer |
| **hedef_koruma** | 2 | 1,000 | **0,240** | 0,985 | 0,30 | **0/30** | **geçer** |
| hava_eslik | 1 | 1,000 | 0,260 | 0,993 | 0,15 | 0/30 | geçer |

🟢 **Beş ailenin beşi de sert kısıtı geçiyor** — çalışma noktası, tehdit
kümesi eklendikten SONRA da geçerli. ⭐ Düzelen ailenin ρ'su 0,156'dan
0,240'a ÇIKTI: karıştırıcı artık zamanın yarısında değil tamamında yayıyor,
yani daha az bölüyor ama daha çok bağ yok ediyor.

## 3 · Örnekleme kusuru bulundu ve giderildi

`ORNEK_ANLARI` (200,0 + k × 15,6) darbeli SINIFIN 2,7 s periyoduyla örtüşmeyi
kırmak için seçilmişti. Çevrimli AİLELERİN periyodu 30 s ve o ızgarada
9 anın yalnız **4'ü** açık evreye düşüyor — bölünme ise yalnız açık evrede
olabilir (kapalıyken karıştırıcı hiç yok, grafik temiz). Yani yukarıdaki
2/30 bir ALT SINIR, 0/30'lar da ZAYIF geçiş olabilirdi.

Dokuz anın dokuzu da açık evrede olacak biçimde yeniden ölçüldü:

| aile | açık evre ρ | ulaş | boğulan | ayrılan |
|---|---|---|---|---|
| hedef_koruma | 0,352 | 0,962 | 0,67 | **2/30 🔴** |
| derin_sizma | 0,382 | 0,979 | 0,43 | 0/30 ✓ |

Sayılar aritmetiği de doğruluyor (0,156 × 9/4 = 0,351 · 0,170 × 9/4 = 0,382),
yani çözümleme doğruydu. 🔒 `hedef_koruma`nın 2/30'u SAĞLAM; `derin_sizma`nın
geçişi artık GÜÇLÜ.

⭐ `derin_sizma` açık evrede DAHA YÜKSEK ρ'ya (0,382 ↔ 0,352) rağmen hiç
bölünmüyor: tek merkez düğüm boğar, ağı KESMEZ.

## 4 · Sebep ölçüldü — geometri değil, çevrimin ürettiği tepe gücü

| varyant | ızgara | ρ | ulaş | boğulan | ayrılan |
|---|---|---|---|---|---|
| V0 kaldırılan (çevrim, x = 0,75) | karma | 0,156 | 0,983 | 0,30 | **2/30** |
| V0 kaldırılan | açık | 0,352 | 0,962 | 0,67 | **2/30** |
| V1 sürekli yayın (tepe = taban) | karma | 0,240 | 0,985 | 0,30 | **0/30** |
| V1 sürekli yayın | açık | 0,240 | 0,985 | 0,30 | **0/30** |
| V2 çevrim kalır, x = 0,60 | karma | 0,182 | 0,981 | 0,33 | **2/30** |
| V2 çevrim kalır, x = 0,60 | açık | 0,410 | 0,957 | 0,73 | **2/30** |

⭐ Bölümün kendi iç kapısı tuttu: **sürekli varyantta iki ızgara AYNI sayıyı
verdi.** Hep açık olan bir karıştırıcıda *"açık evre"* diye ayrı bir evre
yoktur; vermeseydi ızgara mantığında bir hata olurdu.

⭐ V2'nin açık evre ρ'su (0,410) V0'ınkinden (0,352) YÜKSEK olmasına rağmen
ikisi de aynı 2/30'u veriyor — bölünmeyi üreten şey ρ'nun büyüklüğü değil,
gücün nereye yığıldığıdır.

Açık oranı %50 olunca eşit ORTALAMA güç payı 1/(2 × 0,5) = 1,0'a çıkıyor ve
açıkken toplam TEPE güç tabanın İKİ KATI oluyor — darbeli sınıfın sert kısıtı
1/30'da çiğneten fiziğinin aynısı. Ama darbelinin kaçış yolu burada yok:
orada bölünme en çok 1,35 s sürüyordu (3 s'in altında), burada açık evre 15 s.

🔒 V2 yalnız **x konumunu** değiştirdi, iki nokta yapısını değil. Doğru ifade:
duvarı batıya kaydırmak bölünmeyi engellemiyor, tepe gücünü tabana indirmek
engelliyor. Bölünmeyi üreten şey tepe gücü İLE iki noktalı duvarın
birleşimidir — nitekim `derin_sizma` da 2,0 payla yayar ve bölmez.

## 5 · Üçü birden tutulamaz — ve tasarımda buna karşı bir gerekçe vardı

    görev çevrimi + eşit ORTALAMA güç  ⇒  iki kat TEPE  ⇒  bölünme

Üç şeyden ikisi seçilebilir. ⚠️ `07` §05.3 bu çevrimi savunuyordu: *"Fiziksel
katmandaki `surekli_darbeli` sınıfından ayrı bir görev düzeyi desenidir"* ve
keşifsel periyodu OLSR `NEIGHB_HOLD_TIME`ına (6 s) bağlanmıştı. Bu gerekçe
ÇÜRÜTÜLMEDİ; sert kısıtın önceliği altında kaldı.

🔴 Bu kayda geçer: soru öğrenciye götürülürken bu gerekçe SUNULMADI, sonradan
fark edildi ve karardan sonra bildirildi. Karar geçerli, eksiklik kaydedildi.

## 6 · Karar (öğrenci, 15 Eylül 2026)

**`hedef_koruma`nın görev çevrimi kaldırıldı.** İki üye sürekli yayar, pay
1/(2 × 1) = 0,5, tepe = taban. Ölçüldü: 0/30, ρ 0,240.

Gerekçe: eksenleri dikleştirir — aileler GEOMETRİ/SAYI ekseni, zaman yapısı
ise SINIF ekseni (`surekli_darbeli` orada zaten var).

## BUNU NE DEĞİŞTİRİR

- `tehdit_cevrim_periyodu_s` artık HİÇBİR YERDE kullanılmıyor ve `Konfig`den
  SİLİNDİ. Ölü bir varsayılan, bir gün canlanan bir varsayılandır.
- Duyarlılık borcu 10 → 9 (`DUYARLILIK_BEKLEYEN`). Borç ölçülerek değil,
  parametre ortadan kalkarak kapandı — bu böyle beyan edilir.
- Yeni kapı: `test_Y5b_hedef_koruma_SUREKLI_ve_TEPE_GUC_TABANI_ASMAZ`.
  Boş değil: çevrimli hâlde toplam tepe pay 2,000 çıkıp kapıyı ısırıyor.
  ⚠️ Kapı AİLEYE ÖZELDİR — genel bir *"tepe ≤ taban"* kuralı `derin_sizma`yı
  haksız yere düşürürdü.
- ⚠️ `hedef_koruma` artık `cephe_hatti`ye daha yakın (ikisi de sabit ve
  sürekli); ayrımı üye sayısı, üye başına güç ve alana giriş derinliği
  taşıyor (ρ 0,240 ↔ 0,142).
- 🔒 C2'nin ALAN ve GÜÇ çapaları bu kararla DEĞİŞMEDİ.

## 7 · Kapanış — regresyon, testler, denetim

**Regresyon.** Taban `y10_2026-09-14` ↔ `k127` (44 vaka, 22,4 dk, hata 0).
Beklenen farklar KARŞILAŞTIRMADAN ÖNCE ilan edildi. Sonuç: **43/44 vaka
birebir**; bulgu taşıyan tek vaka `i-statik-surekli-dogrudan_komsu-hedef_koruma`
ve yönü doğru (PDR 0,139 → 0,109: karıştırıcı artık yarı zamanlı iki kat tepe
yerine tam zamanlı taban gücünde). `akis_listesi_hash` ve `sayac_semasi_hash`
44/44'te AYNI.

🔴 **BEYAN AŞILDI — ve bu kayda geçer.** İlan edilen listede
`teshis.koken_kovalari.*` YOKTU. *"Köken metin eklemeleri davranışı
etkilemez, yalnız `arac_hash`e girer"* demiştim; yanlış — kova sayıları HER
sonuç satırında taşınıyor ve C1/C3'ün köken eklemeleri onları 44 vakada
oynatmıştı. Fark tamamen hesaplanabildi:

| kova | taban | bugün | sebep |
|---|---|---|---|
| KOL_TANIMI | 11 | 10 | `tehdit_cevrim_periyodu_s` silindi (bugün) |
| SINANMAMIS | 41 | 40 | `dugum_sayisi` ölçüldü (C1) |
| OLCULMUS | 13 | 15 | `dugum_sayisi` + `ALAN_CAPASI_M` |
| TEDAVI | 13 | 17 | C1'den 2, C3'ten 2 ölçüt sabiti |
| TURETILMIS | 43 | 46 | C1'den 1, C3'ten 2 |
| **toplam** | **146** | **153** | +8 yeni kayıt − 1 silinen |

🔒 Ders alete YAZILDI (`regresyon_satirlari.py`): köken defteri tabandan beri
değiştiyse fark ilan edilirken HANGİ kayıtların değiştiği tek tek yazılır.
Sınıf bilerek otomatik yapılmadı — otomatik izin, bir parametrenin sessizce
TEDAVI'den DUYARSIZ'a kaymasını da görünmez kılardı.

**Testler.** 555/555 geçti (7 dk 58 s). Test sayısı değişmedi: bir kapı
yeniden adlandırıldı, silinmedi.

**Mimari denetim.** Yapısal ihlal YOK · köken defterinde eksik ya da ölü
kayıt 0. Kovalar: SINANMAMIS 40 → **37** (telemetri · komut hızı · komut
akış sayısı çıktı), OLCULMUS 15 → 16, TURETILMIS 46 → 51, toplam 153 → 156.
Duyarlılık borcu 10 → **9**.

## EK — C2'nin trafikten bağımsızlığı (yol haritası düzeltmesi)

`12` §3'te C2 *"yeni trafik ve karıştırıcı kümesiyle"* diye yazılıydı. Trafik
kısmı YANLIŞ bir bağımlılık iddiasıdır ve kaynak okunarak düzeltildi: alan
ölçütü *"girişim dâhil DEĞİLDİR"* (`calisma_noktasi.py`), ρ ölçütü de
TRAFİKSİZ kâhin grafiğinde tanımlı (`karistirici_gucu.py`). Yani C3'ün
seçtiği hız C2'ye girmez. C7'nin C3'e bağımlılığı ise GERÇEKTİR — çözünürlük
sapmadan türer, sapma da yükten.

---

# K-128 · 🟢 C2 çapaları ve C7 — ikisi de doğrulandı, R eşiği DÜZELTİLDİ

> **Tarih:** 15 Eylül 2026 · **Ölçüm:** ajan
> **Üreticiler:**
> `python -u kalibrasyon/calisma_noktasi.py --bolum yaricaplar,alan_taramasi` ·
> `python -u kalibrasyon/karistirici_gucu.py tarama` ·
> `python -u kalibrasyon/cozunurluk.py --tohum 40`

## 1 · C2 çapaları bugünkü kodla BİREBİR yeniden çıktı

**Alan** (sert kısıt: statik kolda kopukluk %0, 30 tohum · amaç: derinlik en
büyük):

| alan | derece | ≥3 atlama | kopuk | ölçüt |
|---|---|---|---|---|
| 1600 | 10,42 | %19,7 | %0,0 | geçer |
| **1800** | **8,67** | **%31,0** | **%0,0** | **geçer** |
| 2000 | 7,15 | %42,8 | %0,3 | kalır |

**Güç** (sert kısıt: birden fazla çok üyeli bileşen yok · amaç: ρ en büyük):

| güç | ρ | ulaş | ayrılan |
|---|---|---|---|
| −18,0 | 0,164 | 0,998 | 0/30 |
| **−15,0** | **0,258** | **0,994** | **0/30** |
| −12,0 | 0,379 | 0,974 | 1/30 |

🔒 İkisi de ELLE KONMADI: sert kısıt ile amacın kesiştiği noktalar. Y1–Y10
yapı adımları ve Y5b tehdit kümesi bu çapaları OYNATMADI.

⚠️ C1'in bulgusu burada da görünüyor: 1800 m'de 30 tohumla kopukluk %0,0
okunuyor, oysa 120 tohumla %0,8'dir (K-125). Çapa uçurumun kenarındadır.

## 2 · C7 — çözünürlük yeni çekirdek hücrede

| çıktı | ortalama | SD_tohum | R = 2·SD/√n (n = 40) |
|---|---|---|---|
| ETX kâhini PDR | 0,9350 | 0,0773 | 0,0244 |
| atlama kâhini PDR | 0,8809 | 0,0999 | **0,0316** |
| ölçüt bedeli | 0,0540 | 0,0729 | 0,0230 |

🟢 **Kullanılacak eşik R = 0,0316** (en gevşek çıktı). 10 Eylül'de aynı ölçüm
0,0318 vermişti; aradaki 0,0002 anlamsız. ⚠️ Birebir DEĞİL ve olması da
gerekmiyordu: o ölçüm Y1–Y10'dan ÖNCEYDİ ve o adımlar ilan edilmiş davranış
düzeltmeleri taşıyordu (Y2'nin veri onayı düzeltmesi gibi). *"Çözünürlüğün
YENİ çekirdek hücrede ölçülmesi"* maddesinin sebebi tam olarak buydu.

## 3 · 🔴 BULUNAN KUSUR — aklamalar GEVŞEK bir eşiğe karşı yazılmıştı

Köken defterindeki `DUYARSIZ` gerekçeleri *"etki R'nin altında"* diyor ve o R
**0,036** yazıyordu. Ama 0,036 **30 TOHUMLUK** bir ölçümdür; ana deney 10
Eylül'de 40 tohuma çıkarıldı (K-113) ve 40 tohumda çözünürlük DAHA KESKİNDİR
(R = 2·SD/√n, n büyüyünce R küçülür):

    30 tohum : R = 0,0361        40 tohum : R = 0,0316

🔒 Yani 18 kayıt, deneyin gerçekte görebileceğinden **%14 gevşek** bir eşiğe
karşı aklanmıştı. Yeniden denetlendi: deftere yazılı en büyük etki
|Δ| = 0,027 (`golgeleme_hucre_m`) ve o da 0,0316'nın altında — **hiçbir
sınıflandırma değişmiyor.** Eşik alıntıları yine de düzeltildi: bayat bir
eşik, bir gün yanlış aklayan bir eşiktir.

**İki kayıt ayrı ele alındı:**

- TTL kaydındaki *"çözünürlüğün 5,7 KATI"* bir ORANDIR, eşik değişince o da
  değişir: 0,206 / 0,0316 = **6,5 KATI**.
- Onay eşiği platosu kaydında farkın SAYISI yazılı değil, yalnız *"R'nin
  içinde"* deniyor. Denetlenemedi; eski eşiğiyle BIRAKILDI ve *"40 tohumluk
  R ile yeniden sınanmadı"* diye işaretlendi.

🔴 **AÇIK BORÇ:** 15 `DUYARSIZ` kaydının yalnız 7'sinde |Δ| sayısı yazılı.
Kalan 8'i bu denetimden geçirilemedi. Ön-kayıt mühürlenmeden önce ya sayıları
yazılmalı ya da yeniden ölçülmelidir.

> 🔴 **DÜZELTME — 16 Eylül 2026 (K-130).** Yukarıdaki cümle **YANLIŞTI** ve
> eski hâliyle bırakılıyor (`03` §2 ilke 3: eski hâl silinmez). Ölçüldü:
> 15 kaydın **15'i de** ölçülen |Δ| taşıyor. Aynı yanlış sayı `DEVIR` §1 ve
> `v2/12` §3 C7'de de duruyordu — **üç kopya birlikte bayatladı**, ki bu
> `03` §B5'in kendi hata sınıfıdır. Sayı artık düzyazıda değil, her koşumda
> sayılıyor: `python kalibrasyon/mimari_denetimi.py` → D12.
>
> Bu kaydın ASIL bulgusu (eşiğin bayatlığı) ise ayaktadır ve **daha da
> derinleşti:** K-128 eşiği 0,036'dan 0,0316'ya çekti, ama 0,0316 da **tek
> kol** çözünürlüğüdür. Duyarlılık aleti tohum başına FARK ölçer
> (eşleştirilmiş) ve ön-kayıttaki birincil test de eşleştirilmiştir; doğru
> eşik **0,0230**'dur ve o eşikte üç kayıt aklanamaz.

## BUNU NE DEĞİŞTİRİR

- C2 ve C7 kapandı; C1 ve C3 ile birlikte öğrencinin onayladığı dört
  kalibrasyonun dördü de koştu.
- Duyarlılık eşiği artık ana deneyin tohum sayısıyla TUTARLI.
- 🔒 Alete bölüm seçimi eklendi (`calisma_noktasi.py --bolum ...`): dosya
  dört bölümü birlikte koşturuyordu ve ölçüldü — 3 tohumla bile 15 dakikanın
  üstünde. Oysa `gorev_kolu` C5'in işidir; C2 onun faturasını ödüyordu.
  C2'nin kendi iki bölümü 30 tohumla ~15 dakika.

---

# K-129 · 🔴 D1 koştu ve İKİ ÖLÜ KAPI buldu — Aşama 2'nin zemini sınandı

> **Tarih:** 15 Eylül 2026 · **Koşum:** ajan · **Karar:** öğrenci
> (*"şimdi koşsun, temiz girelim"*)
> **Üretici:** doğrulama listesinin 18 maddesi, `DEVIR.md` §2'deki komutlarla.

## 1 · Neden şimdi

Öğrenci Aşama 2'ye (taban protokoller) geçmeden önce *"kapanması gereken bir
şey kaldı mı"* diye sordu. Doğrulama listesi dokuz yapı adımından SONRA hiç
uçtan uca koşulmamıştı; maddelerin çoğu 9–11 Eylül'dendi. Liste ikiye ayrıldı:

- **ZEMİN** — protokolün üstüne basacağı kapılar (kontrol düzlemi, tavanlar,
  teslim semantiği, dış çapa). Bunlar ENGELDİR.
- **ölçüm bütünlüğü** — Aşama 2 ile paralel yürüyebilir.

Öğrenci ikisini de şimdi koşturmayı seçti.

## 2 · 🔴 BULGU 1 — Li replikasyonu ÖLÜYDÜ

`kalibrasyon/li_replikasyonu.py` ilk saniyede çöküyordu:

    TypeError: Kurulum.__init__() missing 1 required positional argument:
               'kayip_yeri'

Bir yapı adımı `Kurulum`a yeni bir alan ekledi. Bu alet zincir topolojisini
KENDİ kurduğu için imza değişikliğini almadı. **10 Eylül'den beri hiç
koşulmadığı için kimse görmedi** — yani projenin TEK DIŞ DOĞRULAMA ÇAPASI
günlerdir kırıktı ve bunu ancak D1 ortaya çıkardı.

🔒 Düzeltildi; ifade `kosum/kurulum.py`dekiyle AYNI tutuldu (iki yerde iki
kural yazmak ayrışmayı davet etmek olurdu). Koşuyor: **H1 = 0,0871 TUTMADI ·
H2 EVET · H3 EVET** — hüküm kayıtlıyla aynı.

## 3 · 🔴 BULGU 2 — üretici duman kapısı KENDİ SINAVINDA kalıyordu

Kapı, kendi kendine *"kapsam kapım konuşuyor mu"* diye soruyor ve
**SESSİZ** cevabını aldı: defterin andığı dört betiğin duman kesiti
tanımlanmamıştı (`anlamlilik_sabitleri` · `theta_kollari` ·
`yere_toplama_yuku` · ve kapının kasten çıkardığı kontrol betiği). Üçü 14–15
Eylül'de eklenmiş, kesit listesine yazılmamıştı.

⭐ Kapı DOĞRU davrandı: boş geçmektense duman koşusunu REDDETTİ.

🔒 Dört kesit eklendi (13/13 kapsandı). Ek olarak `calisma_noktasi.py`nin
kesiti *"ucuz kesit"* sözleşmesini çiğniyordu — dört bölümü birden
koşturuyordu ve ölçüldü: `zaman_ve_kol` 2 tohumla bile 7 dk+, `gorev_kolu`
ise C5'in saatler süren ölçümü. Kesit iki ucuz bölüme daraltıldı ve
kapsanmayan ikisi BEYAN edildi.

## 4 · 🔴 BULGU 3 — beklenen değerlerin bir kısmı Y2 ÖNCESİNDENDİ

Üç madde kayıtlı değerinden saptı:

| madde | kayıtlı | bugün |
|---|---|---|
| PDR tavanı, hareketli kol | 0,917 · 0,831 | **0,915 · 0,844** |
| Li H1 | 0,0861 | **0,0871** |
| çözünürlük R (40 tohum) | 0,0318 | **0,0316** |

🔒 Bu bir SÜRÜKLENME DEĞİL. Üçünün de kayıtlı değeri 9–10 Eylül'den, yani
**veri onayı düzeltmesinden (Y2, 11 Eylül, K-115) ÖNCEDEN**. O düzeltme
teslim semantiğini BİLEREK değiştirdi; bu sayıların oynaması düzeltmenin yere
inmesidir. Kimse beklenen değerleri güncellememişti çünkü liste hiç
koşulmamıştı. Hepsi güncellendi.

## 5 · 🔴 BULGU 4 — C1'in üretici komutu köken kaydına yazılmamıştı

`dugum_sayisi` C1'den sonra ÖLÇÜLMÜŞ kovasına taşınmıştı ama gerekçe metni
C1 aletinin komutunu taşımıyordu (yalnız 9 Eylül'ün eski üreticisini). Kural
7'nin ihlali ve **bu oturumda ajanın kendi bıraktığı bir açık.** Yazıldı — ve
bunu ortaya çıkaran şey duman kapısının kapsam taraması oldu.

## 6 · Sonuç — 18 maddenin hepsi

| madde | sonuç | süre (yüklü makine) |
|---|---|---|
| test takımı | 555 passed | 478 s |
| mimari denetimi | ihlal YOK | < 1 dk |
| üretici duman (kapı + tam) | 🟢 **13/13 GECTI** (kapsam tamamlandıktan sonra) | 1979 s |
| bağ kümesi kapıları | G-a · G-b GECTI | 6,3 s |
| karıştırıcı gücü taraması | −15,0 dBm · ρ 0,258 | — |
| aile kapısı · açık evre | beş aile GECER | 8–12 dk |
| denetim örneklemesi | çıkış 0 | 680 s |
| adım 9 kapanışı | **HEPSİ TAMAM** | 3584 s |
| PDR tavanı | çıkış 0 | 1242 s |
| evre metrikleri kapıları | dört kapı GECTI | — |
| **kontrol düzlemi P1–P8** | **çıkış 0** | **1007 s** |
| Li replikasyonu | H1 tutmadı · H2 · H3 EVET | — |
| çözünürlük | R = 0,0316 | — |
| anlamlılık sabitleri | KAPI GECTI | 8,9 s |
| onay semantiği (kapı · Y2 · analiz) | çıkış 0 | 175 · 366 · 1,3 s |
| üst referans (kapı · teşhis) | çıkış 0 | 375 · 310 s |
| regresyon | 43/44 birebir | 22,4 dk |

🟢 **Kontrol düzlemi kapıları, Y3'ün beş kancası eklendikten SONRA İLK KEZ
koştu ve geçti.** Protokolün bağlanacağı arayüz artık bugünkü hâliyle
sınanmıştır — Aşama 2'nin asıl ön koşulu buydu.

## BUNU NE DEĞİŞTİRİR

- 🟢 **Aşama 2'nin zemini temiz.** D1 uçtan uca koştu; iki ölü kapı
  düzeltildi, üç beklenen değer tazelendi.
- ⚠️ D1'in kendisi de bir ders verdi: **koşulmayan kapı, kapı değildir.**
  İki kapı günlerce ölü kaldı ve ikisi de ancak listenin tamamı koşunca
  görüldü. Liste her yapı adımından sonra değil, en azından her AŞAMA
  geçişinde uçtan uca koşulmalıdır.
- ⚠️ Borçlar DEĞİŞMEDİ: 37 SINANMAMIŞ · 9 duyarlılık borcu · 8 sayısız
  DUYARSIZ kaydı. Bunlar ön-kayıt mühürlenmeden önce kapanır.

---

# K-130 · 🟢 DENETİM BULGULARI — kapılar çıkış koduna bağlandı, pencere ikizi DONDURULDU

> **Tarih:** 16 Eylül 2026 · **Ölçüm ve uygulama:** ajan · **Karar:** öğrenci
> **Kaynak:** `arsiv/DENETIM-2026-09-16.md` (bağımsız denetim, altı bulgu)
> **Üreticiler:** `python -m pytest tests2 -q` ·
> `python kalibrasyon/mimari_denetimi.py` ·
> `python -u kalibrasyon/regresyon_satirlari.py karsilastir k127 b2_2026-09-16`

## 1 · Öğrencinin kararları

| konu | karar |
|---|---|
| tamponlama (B1) | **ayrı bekleme tamponu** — paket arayüz kuyruğundan çıkar, arkasındakiler akar |
| pencere ikizi (B2) | **pencerede dondurulur** |
| gözlem yüzeyi (B4) | kancalara da gözlem verilir · `bildirdigi_konum` yüzeyden çıkar · **bilgi yokluğunda `0` değil `None`** |
| paralel işler | kapıların çıkış kodu (B3) · ana deney tohumlarının bağlantılılığı (B6) · duyarlılık eşiği (B5) |
| Θ yeniden ölçümü (C4) | şimdi değil |

**Ajana bırakılan teknik seçim (kayda geçiyor):** Aşama 2'nin dikey dilimi
**AODV** ile açılacak. AODV bu planın eklediği her yeni mekanizmayı yükler
(bekleme tamponu · dinamik uyandırma · titreşim · iletim başarısızlığı kancası ·
unicast + yayın kontrol mesajı); OLSR yalnız periyodik zamanlayıcıyı yükler ve
tamponlama yolunu hiç sınamaz.

## 2 · 🟢 B3 — dört alet artık ÇIKIŞ KODU üretiyor

`evre_metrikleri_kapilari` · `karistirici_gucu` (`aile`, `acik_evre`) ·
`denetim_ornekleme` (a · c · d · g) · `kontrol_duzlemi_kapilari` (P1–P8).

🔒 **Kırılabilirliği ÖLÇÜLDÜ, iddia edilmedi.** Ölçüm fonksiyonları bozuk
değer döndürecek biçimde değiştirildi; her kapı `False` döndü ve süreç
`SystemExit` fırlattı. *"Kırmızı yanamayan bir kapı kapı değildir"* —
K-129'un dersinin ikizi: **okunmayan kapı da kapı değildir.**

⚠️ **Θ kapısı KODA ALINMADI ve bu bilinçli.** Çekirdek kol adayı `formasyon`
bugün 2,31 ile eşiğin altında ve kestiricinin aşağı yanlı olduğu ölçülmüş
(çiftlerin %92,1'i hiç kopmuyor). Bugün bağlamak, doğru işi kırmızıya boyayan
bir kapı kurmak olurdu ve insanları kapıyı görmezden gelmeye alıştıran şey
tam olarak budur (`03` §2.1). Alet çıktısındaki *"KAPI"* sözcüğü
*"BEYAN EDİLEN EKSEN"*e çevrildi — ikisinin arasında durmak yanıltıcıydı.
Karar C4'ten sonra.

⚠️ Ölçüm olan bölümler (`tarama`, `sinif`, `hedef_teshis`, `b`, `e`, `f`)
verdikt DÖNDÜRMEZ. Bir ölçümü kapıya çevirmek, sayının kendisini sonradan
uydurulmuş bir eşik gibi okumak olurdu.

## 3 · 🔴 DENETÇİNİN GÖRMEDİĞİ ÜÇ BULGU

**D1 · `yuku_dondur` İKİ KEZ tanımlıydı** (`sim2/gozlem/yuk.py`). Gövdeler
birebir aynıydı ve ikincisi birincisini sessizce gölgeliyordu; silmeden önce
eşitlik programla doğrulandı, yani hiçbir ölçülmüş sayı bayatlamadı.
Zararsızlığı kusuru küçültmez — `03` §B5'in hata sınıfı tam olarak budur ve
ayrışsalardı Python İKİNCİSİNİ seçerdi, dosyayı okuyan BİRİNCİSİNİ okurdu, ve
o dosyada okunan şey BEDEL TARİFESİDİR.
🔒 Yapısal panzehir: mimari denetimine **D16 · TEKRARLI TANIM** eklendi
(`sim2` · `kalibrasyon` · `tests2` · `protokoller`; sınıf gövdeleri ayrı ad
uzayı sayılır). Bugün: **0 bulgu**.

**D2 · Mesaj biçimi dökümü B2'nin AYNI kaçağını taşıyordu.**
`bicim_say` pencere kipini `pencere_basladi` ile seçiyordu ve o özellik
pencere kapandıktan sonra da `True` döner. İkizler dondurulup bu
düzeltilmeseydi `Σ bicim["pencere"]` ile `kontrol_iletim_pencere` ayrışırdı ve
`13` §03.11'in taahhüdü kırılırdı. **Ölçüldü:** düzeltme geçici olarak geri
alındı ve mevcut test kırıldı — **411 ↔ 327** (%25,7 ayrışma). Yani kapı
zaten canlıydı; eksik olan `pencere_acik` kavramıydı ve eklendi.

**D3 · Θ aleti `MOBILITE_THETA` için EKSİK demet basıyordu** — iki eleman,
tablo üç tutuyor (üçüncüsü kopmayan oranı, satırın kapsam bölümüne girer).
Alet üçüncü sayıyı hesaplıyor ama basmıyordu; bir sonraki ölçümde elle
tamamlanacaktı. Düzeltildi.

## 4 · 🔴 B5 — DENETÇİ YANILDI, ama asıl bulgusu AYAKTA

Denetim *"15 `DUYARSIZ` kaydının 8'inde ölçülen |Δ| yazılı değil"* diyen üç
kaydı (`kokenler.py` başlığı · `DEVIR` §1 · `12` §3 C7) **yanlış** buldu ve
bunda haklıydı. **ÖLÇÜLDÜ: 15'in 15'i de sayı taşıyor.** Üç kopya birlikte
bayatlamıştı — `03` §B5'in kendi hata sınıfı.

🔒 Sayı artık düzyazıda DEĞİL: mimari denetimi D12 her koşumda sayıyor ve
sayısız bir kaydı isimle basar. Üç yerdeki cümle düzeltildi; K-128'in kaydına
tarihli bir düzeltme notu eklendi (eski hâl silinmedi, `03` §2 ilke 3).

🔴 **Denetimin İKİNCİ noktası ise doğru ve daha derin.** Aklamalar
`R = 0,0316`ya karşı yazılı, ama bu **TEK KOL** çözünürlüğüdür. Duyarlılık
aleti tohum başına FARK ölçer (`duyarlilik.py` — eşleştirilmiş, kendi 2 SE
bandıyla) ve ön-kayıttaki birincil test de eşleştirilmiştir (Wilcoxon,
`06` §7). Doğru eşik **0,0230**'dur. Çözünürlük aleti bunu kendi çıktısında
söylüyor (*"deneyin asıl ayırt edici ekseni de budur"*) ama sonra **en
gevşek** çıktıyı seçiyor — alet kendi kendisiyle çelişiyor.
O eşikte üç kayıt aklanamıyor: `gm_pitch_sigma_rad` 0,030 ·
`golgeleme_hucre_m` 0,027 · `onay_bayt` 0,025. **Adım 3'e.**

## 5 · 🟢 B2 — pencere ikizi DONDURULDU, ve bir TUZAK çıktı

### 5.1 · Ölçülen büyüklük (tanım yazılmadan ÖNCE)

`statik-yok` · `statik-surekli` · `DogrudanKomsu` · tohum 1000 · tam uzunluk:

| büyüklük | boşalmadan gelen pay |
|---|---|
| `kontrol_cerceve` · `kontrol_bayt` · `kontrol_airtime_s` | %7,6 · %9,1 · %8,1 |
| `beacon_gonderilen` · `beacon_alinan` | %10,7 · %10,7 |
| `veri_bayt` · `veri_airtime_s` · `teslim_paket` · `mac_deneme` | **%0,0** |
| `nrl_bayt_pencere` | 0,0867 → 0,0788 (**+%10,0** şişmeydi) |

Payda boşalmada HİÇ büyümüyor (trafik çizelgesi `olcum_bitis_s`te biter), pay
büyümeye devam ediyordu. O kontrol trafiği **periyodiktir**: OLSR'ın HELLO/TC'si
boşalmada da akar, AODV'nin keşif trafiği susar. Yani üç manşet metrikten biri
iki protokol ailesini **sistematik olarak farklı** cezalandırıyordu — tam da
H1.1'in mekanizma kontrolünün baktığı yerde. Bir büyüklük sorunu değil,
**karşılaştırma geçerliliği** sorunu.

### 5.2 · 🔴 TUZAK — naif dondurma bir ÖN-KAYITLI METRİĞİ öldürüyordu

`kopma_fiziksel` geometriden, koşu BİTTİKTEN sonra, ölçüm penceresi için
hesaplanır. Naif bir dondurma onu ikizde **0** yapardı. **Ölçüldü**
(`bagimsiz-surekli`, tohum 1000): ham 49 · ikiz 49 → **0**, ve
`algilama_duyarliligi_pencere` 0,0 yerine **`None`** dönerdi. Yani Risk 3'ün
(`gozlem/karar.py`) NİCEL YARISI sessizce ölürdü.

🔒 Yolu `Sayaclar.pencere_icinde_olculdu`: değeri hem ham sayaca hem pencere
anlık görüntüsüne AYNI çağrıda yazar. İkinci bir sayaç listesi DEĞİL — tek
çağrı yolu, gerekçesi çağrı yerinde. Dört yeni test bağlar.

### 5.3 · Regresyon — beklenen farklar karşılaştırmadan ÖNCE yazıldı

Taban `k127` ↔ `b2_2026-09-16` · 44/44 geçerli · üretim 23,3 dk · 0 hata.

🔒 **52 bulgunun 52'si de bir PENCERE İKİZİ.** Hiçbir ham sayaç, hiçbir
korunum alanı, PDR, gecikme, kapsam, konfig ya da şema özeti değişmedi.
`sayac_semasi_hash` birebir aynı kaldı (`9569371c7f96bbce`) — şema alanı
eklenmediği için, ve bu önceden ilan edilmişti.

- **691 ikiz azaldı · 8 arttı · 2073 alan-vaka değişmedi.**
- 🟡 Artan 8'in hepsi **oran** ikizi (`psr_pencere`, `mac_basari_orani_pencere`).
  Sınıf C'de *"değişebilir"* diye ilan edilmişti ama **yönü ilan edilmemişti**;
  bu bir eksikliktir ve olduğu gibi yazılıyor. Mekanizma: boşalmada yeni paket
  doğmaz, kuyrukta kalanların yeniden denemeleri sürer ve karıştırıcı altında
  başarı oranları düşüktür — onları çıkarmak pencere içi PSR'yi bir miktar
  YÜKSELTİR. En büyük oynama 0,546 → 0,557.
- Düşüşün büyüklüğü **boşalma/pencere oranıyla ölçekleniyor** ve bu mekanizmayı
  doğruluyor: tam uzunluk vakaları (boşalma = pencerenin %11,1'i) −%6,2…−%10,8 ·
  kısa vakalar (%33,3) −%12,3…−%29,3.
- 🟢 `kopma_fiziksel_pencere` ve `algilama_duyarliligi_pencere` **44 vakanın
  44'ünde de değişmedi** — tuzağın kapandığının kanıtı.

### 5.4 · 🔴 YAN BULGU — `k127` tabanı köken kovalarında BAYATMIŞ

Karşılaştırma `teshis.koken_kovalari`nde 44 vakada fark buldu ve bu **bu
değişikliğin eseri DEĞİL**:

| taban | üretildi | toplam | TÜRETİLMİŞ | ÖLÇÜLMÜŞ | SINANMAMIŞ |
|---|---|---|---|---|---|
| `y10_2026-09-14` | 15 Eyl 00:00 | 146 | 43 | 13 | 41 |
| `k127` | 15 Eyl **17:14** | 153 | 46 | 15 | 40 |
| bugünkü kod | — | **156** | **51** | **16** | **37** |

`kokenler.py` 15 Eylül **20:11**'de değişti (K-128'in eşik düzeltmesi), yani
`k127` üretildikten SONRA; ve o günden beri hiç karşılaştırma koşulmadı.
Bugünkü 156/51/16/37, `DEVIR` §2'de **15 Eylül (K-128 sonrası)** diye kayıtlı
değerle BİREBİR aynıdır — yani kod kendi kayıtlı durumunda, bayat olan taban.

⚠️ **Ders, K-129'unkinin bir başka yüzü:** karşılaştırılmayan bir ürün
sürüklenir. Köken defteri her değiştiğinde regresyon tabanı yenilenmeli;
yoksa bu alan her karşılaştırmada gürültü üretir ve *"gürültü üreten kapı
bozuktur"* (`03` §2.1).

🔒 **Yeni geçerli taban: `b2_2026-09-16`** — bugünkü köken defterini taşıyor.

## 6 · Kapılar

| kapı | sonuç |
|---|---|
| `python -m pytest tests2 -q` | **559 passed** (555 + 4 yeni), 480,5 s |
| `python kalibrasyon/mimari_denetimi.py` | ihlal YOK · 156 parametre · 114 modül · 11 not · **D16 tekrarlı tanım 0** · **D12 `DUYARSIZ` |Δ| 15/15** |
| regresyon `k127 ↔ b2_2026-09-16` | 52 bulgunun 52'si de pencere ikizi; korunması gerekenlerin hiçbiri değişmedi |
| kapıların kırılabilirliği | bozuk ölçümde dördü de `SystemExit` fırlattı |

## BUNU NE DEĞİŞTİRİR

- 🟢 Kontrol yükü metriği artık iki protokol ailesini aynı aralıkta ölçüyor.
  İlk NRL sayısı raporlanmadan kapandı ve tanım sonuç görülmeden yazıldı.
- 🟢 Dört kapı Aşama 2 boyunca gerçekten koruyacak.
- ⚠️ `DEVIR` §2'de **beklenen değerler tazelendi**: test takımı 559, regresyon
  tabanı `b2_2026-09-16`.
- ⏭️ Sırada **Adım 2**: bekleme tamponu + kancalara gözlem. `sim2`de yapısal
  değişikliktir ve koda geçmeden önce yapı ayrıca anlatılıp onay alınacak.
- 📌 **Açık bırakılan borç (yeni):** `04`ün kayıt indeksi K-088'de kalmış ve
  onu üreten betik `arsiv/dogrulama/kayit_indeksi.py`ye taşınmış — indeksin
  başında yazan komut artık o yolda yok. Bir ölçümü etkilemiyor, ama
  *"bu sayıyı üreten komut hâlâ koşuyor mu?"* sorusunun bir kırık örneği.
  Bilerek bugün kapatılmadı; kapsamı öğrenciye ait.

---

# K-131 · 🟢 PROTOKOL ARAYÜZÜ SON HÂLİNİ ALDI — tamponlama ve kancalara gözlem

> **Tarih:** 16 Eylül 2026 · **Yapı onayı:** öğrenci · **Uygulama:** ajan
> **Kaynak:** `arsiv/DENETIM-2026-09-16.md` B1 ve B4
> **Üreticiler:** `python -m pytest tests2 -q` ·
> `python kalibrasyon/mimari_denetimi.py` ·
> `python -u kalibrasyon/kontrol_duzlemi_kapilari.py` ·
> `python -u kalibrasyon/regresyon_satirlari.py karsilastir b2_2026-09-16 arayuz_2026-09-16`
>
> 🔒 Bu adım Aşama 2'yi BEKLETİYORDU: ikisi de arayüz değişikliğidir ve
> protokoller yazıldıktan sonra yapılsaydı o güne kadarki bütün taban
> ölçümleri bayatlardı.

## 1 · B1 — rota bekleme tamponu

**Sorun.** Protokolün paket başına verebileceği cevap İKİ şıklıydı: *"şu
komşuya gönder"* ya da *"gönderme"*. İkincisi paketi ANINDA düşürüyordu
(`gonderim.py`, `hedef_yok`). RFC 3561 §6.3 rota keşfi sırasında tamponlamayı
**şart koşar** ve NS-2'nin AODV'si 64 paketlik bir kuyruk tutar. Tamponsuz bir
AODV akış başlangıcında ve **her rota kopmasından sonra** keşif bitene kadar
doğan her paketi kaybederdi; OLSR proaktiftir, rotası neredeyse hep vardır ve
bu kayba uğramazdı.

🔴 Yani eksik, karşılaştırdığımız iki aileden **yalnız birine** biniyordu — ve
etkinin yoğunlaştığı yer kötüydü: karıştırma altında kopma sıktır, onarım
yavaştır, yani eksik iddianın yaşadığı rejimde en büyüktür. `06` §8'in üçüncü
geçerlilik koşulunun (*"gizli asimetri yok"*) doğrudan ihlali.

**Öğrenci kararı: ayrı bekleme tamponu.** Paket arayüz kuyruğundan ÇIKAR ve
düğümün tamponuna geçer; arkasındaki paketler akmaya devam eder. Alternatif
(kuyruk başında bekletmek) çok daha az koddu ama tek bir rotasız paket düğümün
bütün kuyruğunu tıkardı — gerçek AODV'de olmayan ve yalnız reaktif aileyi
vuran bir ceza.

| parça | uygulama |
|---|---|
| karar | `Karar.beklet: bool`. Değişmez: `beklet` ile `sonraki` birlikte verilemez |
| tampon | `Dugum.bekleyenler` · kapasite 64 · ömür 30,0 s (`Konfig`, ikisi de `SINANMAMIS`) |
| tavan | aşım `tampon_asimi` sebebiyle deftere; kapasitede **en eski** düşer (NS-2 `aodv_rqueue`) |
| defter | tampon ayrı bir havuz DEĞİL: paket hâlâ *"kuyrukta"*. `mutabakat` tamponu da sayar |
| yeniden sorma | `kontrol_alindi` · `uyandi` · `iletim_basarisiz` sonrası tampon kuyruğa dökülür |
| sayaçlar | `tampon_giris` · `tampon_dusen` · `en_yuksek_tampon` |

🔒 **`zamanlayici_doldu` sonrası yeniden SORULMAZ** ve bu bilinçli: periyodik
zamanlayıcı düğümün kendi ürettiği bir olaydır, dışarıdan bilgi taşımaz.
Ondan sonra sormak tamponu protokolün HELLO hızında dönen bir yoklama
döngüsüne çevirirdi. Yeniden sorulmak İSTEYEN protokol kendi `Uyandirma`sını
döndürür — sözleşmenin zaten istediği disiplin (`13` §03.5).

## 2 · B4 — kancalara gözlem

**Sorun.** Gözlem penceresi TEK bir yerde üretiliyordu: veri gönderme kararı
(`.gozlem(` çağrısı tüm depoda **bir** yerde). Üç ölçülmüş sonucu vardı:

| gözlem | ölçülen |
|---|---|
| `kanal_mesgul_mu = True` | **%2,17** (533 / 24 558 karar anı) |
| `bildirdigi_konum is None` | **%100,0** (110 605 komşu kaydı) |
| protokolün kendi gürültüsünü beacon'a koyması | imkânsız — koyarken ölçemiyordu |

`kanal_mesgul_mu` yapısal olarak neredeyse sabitti çünkü gözlem tam da düğümün
kanalı **boş bulduğu** anda üretiliyordu. `05` §6 karıştırma sezimi için
gereken altı alanı sayıyor; ikisi bu yüzden kullanılamaz durumdaydı ve
Aşama 3'ün tasarım uzayı farkında olmadan daraltılmıştı.

**Uygulama.** Yedi kanca gözlem alıyor: `beacon_yuku` · `beacon_alindi` ·
`zamanlayici_doldu` · `uyandi` · `kontrol_alindi` · `iletim_basarisiz`
(+ zaten alan `sonraki_atlama`). `Gozlem` düğüm kimliğini ve yerel saati zaten
taşıdığı için **hiçbir bilgi eksilmedi**; donanım ölçümleri eklendi.

⚠️ `beacon_alindi` yapı anlatımında YOKTU; ayrıca soruldu ve öğrenci ekledi.
Gerekçe: protokolün gördüğü en sık dış olay odur ve `05` §6 *"duyulan beacon"*
ile *"ölçülen gürültü"*yü birlikte sayıyor.

**Yüzey BÜYÜMEDİ, 24 → 23'e İNDİ.** `bildirdigi_konum` kaldırıldı: sözleşme
onu *"3B, bedeli faturalanır"* diye anlatıyordu ama koşucu hiç doldurmuyordu.
Doldurmak, *"konum beacon'da taşınır"* kararını protokol adına simülatörün
vermesi olurdu; konum isteyen protokol onu `beacon_yuku`na koyar ve öder.

🟢 **`None ≠ 0` (öğrenci kararı).** Protokolün beacon'a koymadığı alanlar `0`
değil `None` döner. Kuralın projedeki **tek istisnası** kapandı.

## 3 · Maliyet — ilan edilmiş ölçüt, ölçülen sonuç

Ölçüt taramadan ÖNCE ilan edilmişti: *"tam uzunlukta bir koşuda süre artışı
%15'i aşarsa gözlem üretimi belleklenir"*.

| kol | önce | sonra | değişim |
|---|---|---|---|
| `statik-yok` | 110,5 s | 100,4 s | **−%9,1** |
| `statik-surekli` | 112,6 s | 101,0 s | **−%10,3** |

🟢 Ölçüt geçti; bellekleme gerekmedi. ⚠️ Ama **azalma da açıklanmalı** ve tek
bir sebebe bağlanmadı: `KomsuKaydi` bir alan kaybetti (koşu başına ~140 000
kez kuruluyor) ve makine gürültüsü bu oturumda ±%5 ölçüldü (aynı test takımı
458–504 s). Asıl soru *"davranış değişti mi"* idi ve cevabı §4'te.

## 4 · Regresyon — beklenen farklar karşılaştırmadan ÖNCE yazıldı

`b2_2026-09-16` ↔ `arayuz_2026-09-16` · 44/44 geçerli · üretim 21,9 dk.

🟢 **141 METRİK ALANININ 44 VAKADA HİÇBİRİ DEĞİŞMEDİ.** Korunum, mutabakat,
`gecerli` ve `tampon_asimi` dışındaki bütün düşme sebepleri de birebir.
Üç yeni tampon sayacı 44 vakanın 44'ünde de **0** — mekanizma gerçekten
dormant ve bu ölçüldü, iddia edilmedi.

**İlan edilmiş ve gerçekleşen farklar:** `sayac_semasi_hash` (üç yeni sayaç) ·
`korunum.dusen.tampon_asimi` (yeni anahtar, 0) · `kapsam.rota_tamponu` ·
`konfig.rota_tamponu_*` · üç yeni sayaç ve ikizleri · `koken_kovalari.SINANMAMIS`
37 → 39.

### 🔴 İLAN ETMEDİĞİM İKİ FARK — ikisi de açıklandı

**1 · `kimlik.kurulum_hash` (44 vaka).** Beklenen farklar listesinde
*"değişmemeli"* yazmıştım ve **yanılmıştım**: `kurulum_hash`, tedavi alanları
hariç `Konfig`in TAMAMINI özetliyor (`cekirdek/kimlik.py`), yani iki yeni alan
eklemek onu zorunlu olarak değiştirir. Hata ilanda, kodda değil — ve anlamı
doğru: bu satırlar gerçekten farklı bir kurulumla üretildi.

**2 · `teshis.sonumleme_onbellegi.girdi` ve `iskalama_tahmini` (13 vaka).**
Sönümleme önbelleğinin İSTATİSTİĞİ. Kancalara gözlem vermek fazladan
`Gozlem` üretiyor, her `Gozlem` bir girişim hesabı yapıyor ve o hesap
sönümleme önbelleğine uğruyor. Ölçüldü: **13 vakanın 13'ünde de ARTMIŞ**
(2 … 16 084 girdi), hiçbirinde azalmamış, ve **tahliye sayısı 44 vakanın
44'ünde de aynı** kalmış.

🔒 Bu bir davranış değişikliği DEĞİLDİR: önbellek saf bir memo'dur ve
değerler sıralı akıştan değil **hash'ten** gelir (`06` §7), yani kaç kez
sorulduğu sonucu değiştiremez. Kanıtı da ayrıca ölçüldü — 141 metriğin
hiçbiri oynamadı. Ama kaydediliyor, çünkü *"tabloda değişmeyen sütuna bak"*ın
tersi de doğrudur: **beklenmedik biçimde değişen bir sütun da okunmalıdır.**

## 5 · 🔴 KENDİ KODUMDA BULDUĞUM İKİ KUSUR

**1 · Tamponu dökerken kuyruk dolarsa KALAN HER PAKET düşüyordu.** İlk yazımda
dökme döngüsü dolu kuyrukta da sürüyordu; geçici bir doluluk tamponun
tamamını yok ederdi — tamponun var olma sebebinin tam tersi. Düzeltildi: dökme
durur, kalanlar tamponda bekler ve süre tavanı işlemeye devam eder.
⚠️ Düzeltme regresyon üretiminden SONRA yapıldı; geçerliliği iddia edilmedi,
**ölçüldü**: 44 satırın 44'ünde de `tampon_giris = 0`, yani hiçbir regresyon
vakası bu yola hiç girmedi.

**2 · Yeniden sorma yolu HİÇ TEST EDİLMİYORDU.** Tamponun ilk yedi kapısı
kontrol kancası olmayan bir sınav protokolüyle koşuyordu; `tamponu_kuyruga_dok`
hiçbir testte çalışmıyordu — yani mekanizmanın en kritik yarısı (paketin
tampondan ÇIKIP teslim edilmesi) sınanmamıştı. İki kapı eklendi; birincisi
paketin tampona girip çıktığını ve **tamponun boşaldığını** ayrıca ölçüyor,
çünkü tamponlanan paketler ölse ve yalnız sonradan doğanlar teslim edilse
tablo aynı görünürdü.

## 6 · Bir testin haklı çıkması

`tampon_asimi` önce hem düşme sebebi hem sayaç adı olarak konmuştu ve
`test_IKINCI_bir_sayac_listesi_YOK` kırıldı: `DUSME_SEBEPLERI` demeti böylece
üç sayaç adı taşıyor hâle geliyordu. Test sezgiseldir (eşiği üç sabit) ve
koruduğu asıl değişmez fiilen çiğnenmemişti — ama **ölçüt sonuç görüldükten
sonra gevşetilmez** (`03` §2 ilke 3). Sayaç adı `tampon_dusen` oldu; zaten var
olan geleneğe uyuyor (`ttl` → `ttl_olumu`).

Aynı biçimde `Konfig` alan muhasebesi testi de kırıldı ve haklıydı: iki yeni
alanı deftere yazmamıştım.

## 7 · Kapılar

| kapı | sonuç |
|---|---|
| `python -m pytest tests2 -q` | **570 passed** (568 + 2 yeniden sorma kapısı), 476 s |
| `python kalibrasyon/mimari_denetimi.py` | ihlal YOK · **158** parametre · SINANMAMIŞ **39** · 114 modül · D16 tekrarlı tanım 0 |
| regresyon `b2 ↔ arayuz` | **141 metriğin hiçbiri değişmedi**; farkların hepsi ilan edilmiş ya da açıklanmış |
| tampon kapıları | 9 kapı, hepsi **boş geçmeye kapalı** |

## BUNU NE DEĞİŞTİRİR

- 🟢 **Aşama 2'nin arayüz ön koşulu kapandı.** AODV artık RFC'ye sadık
  yazılabilir: rota keşfi sırasında paketi tamponlar, kopmada RERR üretir,
  kendi gürültüsünü ölçüp beacon'a koyabilir.
- 🟢 `06` §8'in üçüncü geçerlilik koşulu (*gizli asimetri yok*) bu eksende
  kapandı; U2 artık protokolün kurtarma davranışını ölçer, keşif süresince
  kaybettiği paketleri değil.
- ⚠️ **Borç arttı ve bilerek:** `SINANMAMIS` 37 → **39**. Protokolsüz
  kapanamayan parametreler dörtten **altıya** çıktı. Tampon ömrü (30 s) ölçüm
  penceresinin %11'i kadar — PDR'yi ve gecikmeyi doğrudan oynatabilir, o
  yüzden AODV yazılır yazılmaz **ilk o** ölçülecek.
- 🔒 Yeni geçerli regresyon tabanı: **`arayuz_2026-09-16`**.

---

# K-132 · 🔴 İKİ AKLAMA ÇÖKTÜ, BİR AĞ BÖLÜNMESİ BULUNDU — ve iki ölçüm aleti kuralın yarısını uyguluyormuş

> **Tarih:** 16 Eylül 2026 · **Ölçüm ve uygulama:** ajan
> **Öğrenci kararı:** *"gerekeni yap; bir sorun varsa çözmek gerek, beyan
> ederek hiçbir şey çözülmez"* + 20 tohumla yeniden ölçüm
> **Kaynak:** `arsiv/DENETIM-2026-09-16.md` B5 ve B6
> **Üreticiler:** `python -u kalibrasyon/dugum_sayisi.py --bolunme` ·
> `python -u kalibrasyon/duyarlilik.py statik golgeleme_hucre_m onay_bayt --tohum 20` ·
> `python -u kalibrasyon/duyarlilik.py hareketli gm_pitch_sigma_rad --tohum 20` ·
> `python kalibrasyon/mimari_denetimi.py`

## 1 · B6 — ağ bölünmesi: İLK ÖLÇÜMÜM YANILTICIYDI

C1 (K-125) çalışma noktasının uçurumun kenarında olduğunu ölçmüştü (%0,8
kopukluk, 120 tohum) ve 40 tohumluk ana deneyde en az bir kopuk tohum görme
olasılığı ~%27'ydi.

🔴 **İlk ölçümüm dardı ve YANLIŞ GÜVEN VERDİ.** Ana deney tohumlarına t = 0'da,
statik kolda, karıştırıcısız bakıldı: **0/40**. Rapor edilen sonuç *"risk
gerçekleşmedi"* idi. Ama bölünme HAREKETTEN doğar ve tek bir ana bakmak onu
göremez. Ölçüm penceresinin tamamında (dokuz an) ve bütün mobilite kollarında
yeniden yapıldı:

| kol | bölünmüş tohum | bölünmüş an payı |
|---|---|---|
| `statik` | **0/40** | — |
| `bagimsiz` | **6/40** | %18,5 |
| `gorev` | **7/40** | %25,4 |
| `formasyon` | **2/40** | %44,4 |

**15 (kol, tohum) çiftinde** ağ ölçüm penceresi içinde bölünüyor. En kötüsü
**formasyon / 2011: dokuz anın YEDİSİNDE bölünmüş.** Bölünmelerin neredeyse
hepsinde 39 ulaşılamaz çift var — tek bir düğüm menzil dışına düşüyor;
`gorev`de iki tohumda 76 çift, yani iki düğüm.

🔒 `statik`in SIFIR çıkması bir **kontroldür**: konumlar değişmediği için
bölünme doğamaz ve orada sıfırdan farklı bir sayı ölçümün bozuk olduğunu
gösterirdi.

**Satır artık söylüyor.** `kapsam.bolunme_payi` — `None` ölçülmedi, `0.0`
ölçüldü ve bölünme yok, `> 0` bölünme var. Θ'nın deseni: ölçülmüş tablo
`senaryolar.py`de (ÖLÇÜLMÜŞ köken), her satıra `kapsam.py` yazıyor.

🔒 **Bölünmüş tohum ATILMAZ** — atmak seçilim yanlılığı olurdu. Satır onu
söyler; betimleyici tablolar ve evre metrikleri orada ayrıca okunur.

### 1.1 · 🔴 YANLIŞ BİR TASARIM YAZILDI, ÖLÇÜLDÜ ve GERİ ALINDI

Bölünme önce **koşunun içine**, `olcum/kopma.py`nin mevcut taramasına
bindirildi: tarama zaten her ızgara noktasında bağ kümesini kuruyordu ve
ikinci bir bağ tanımı doğmuyordu. Sayaçlar, türev, testler yazıldı.

Sonra *"bu sayaç hiç sıfırdan büyük çıkıyor mu"* diye soruldu ve cevap
**her kolda, her tohumda %100** çıktı — aynı tohumlarda C1 aleti *"hiç
bölünme yok"* derken. Sebep ölçüldü (`statik-yok`, t = 200 s):

    yavaş SINR grafiği  :  55 bağ · derece 2,75 · TEK PARÇA DEĞİL
    kâhin grafiği (C1)  : 162 bağ · derece 8,10 · TEK PARÇA

`kopma.py`nin bağ tanımı **tek denemelik** bir eşiktir ve o grafik zaten hep
bölünmüştür. O tanımla bir "bölünme" alanı her satıra %100 yazardı — ölçtüğü
şey ağın bölünmesi değil, bir eşiğin seyrekliği olurdu. **Tanım gereği sabit
çıkan metrik** `03` §B3'ün tuzak listesinde yazılı.

Doğru tanım kâhin grafiğidir ve o `kalibrasyon/`da yaşıyor; `sim2` onu içe
aktaramaz (katman kuralı) ve ikinci bir gerçeklemesini yazmak `03` §B5'in
hatası olurdu. Bu yüzden ölçüm kalibrasyon tarafında yapılıyor, tablo
`senaryolar.py`ye ÖLÇÜLMÜŞ olarak giriyor, satıra `kapsam.py` yazıyor.
Sayaçlar geri alındı ve `sayac_semasi_hash`in eski değerine BİREBİR döndüğü
doğrulandı.

⚠️ **Yan bulgu — `kopma_fiziksel` hakkında.** O sayaç derecesi **2,75** olan
bir grafikteki geçişleri sayıyor, derecesi **8,10** olan erişilebilir
grafiktekileri değil. Tanımına sadıktır ve tanımı kaydında yazılıdır; ama
*"ağın bağları koptu"* diye okunmamalıdır. Modül başlığına yazıldı.

## 2 · B5 — iki aklama ÇÖKTÜ

Eşik eşleştirilmiş çözünürlüğe bağlandıktan sonra (§3) eşiğin kıyısındaki üç
kayıt **20 tohumla** yeniden ölçüldü. Eskisi 5 tohumluktu.

| kayıt | 5 tohum | 20 tohum | sonuç |
|---|---|---|---|
| `gm_pitch_sigma_rad` | \|Δ\| = 0,030 | **0,0158** · band 0,6x | 🟢 **AKLANDI** — iki ölçütü de geçiyor |
| `golgeleme_hucre_m` | \|Δ\| = 0,027 | **0,0605** · band 0,7x | 🔴 **ÇÖKTÜ** — R'nin 2,6 katı |
| `onay_bayt` | \|Δ\| = 0,025 | **0,0226** · band **1,1x** | 🔴 **ÇÖKTÜ** — kendi bandını aşıyor |

İkisi de `DUYARSIZ` kovasından çıkıp **`SINANMAMIS`**a geçti; ikisinin de
değeri zaten gerekçesizdi (*"mekanizması gerekçeli ama DEĞERİ ölçülmedi"* ve
*"802.11 ACK 14 bayt — `02`de yok"*). **SINANMAMIŞ 39 → 41.**

🔒 `gm_pitch_sigma_rad`ın aklanması da bir ders: 5 tohumluk bir |Δ|
KESTİRİMİNİN kendi hata payı vardır ve bu kayıtta etki **yarıya indi**. Az
tohumlu bir tarama hem yanlış mahkûm eder hem yanlış aklar.

## 3 · 🔴 İKİ ALET KURALIN YARISINI UYGULUYORMUŞ

**3.1 · Çözünürlük aleti kendi kendisiyle çelişiyordu.** Çıktısında *"deneyin
asıl ayırt edici ekseni EŞLEŞTİRİLMİŞ olandır"* yazıyor, sonra **en gevşek**
çıktıyı seçiyordu (`max`). Oysa ön-kayıttaki birincil test eşleştirilmiştir
(Wilcoxon, `06` §7) ve duyarlılık aleti de eşleştirilmiş çalışır (tohum başına
FARK, `_esli_fark`). K-128 eşiği 0,036 → 0,0316'ya çekmişti; **0,0316 da tek
kol çözünürlüğüdür** ve aynı hatanın küçük hâliydi. Doğru eşik **0,0230**.

**3.2 · Duyarlılık aleti R'ye HİÇ BAKMIYORDU.** `cozunurluk.py` kuralı iki
ayaklı yazmıştı — *"etkisi R'DEN KÜÇÜK **ve** kendi hata payı içinde;
ikisinden biri yetmez"* — ama alet yalnız BAND ayağını uyguluyordu. R yalnız
köken defterinin DÜZYAZISINDAYDI, yani ikinci ayak insan hafızasına bağlıydı.

🔴 **Ve tam o boşluğa fiilen düşülmüştü:** `golgeleme_hucre_m`in ALTI PDR
PUANLIK etkisi, tohumlar arası yayılım büyük olduğu için band testini geçiyor
ve alet *"duyarsiz"* basıyordu. `cozunurluk.py`nin kendi başlığı bu senaryoyu
kelimesi kelimesine tarif ediyor ve *"aklamanın en kötü hâli"* diyor.

**Kapatıldı:**

- `duyarlilik.py::R_ESLESTIRILMIS` — çözünürlüğün **TEK KAYNAĞI**, köken
  defterinde ÖLÇÜLMÜŞ olarak kayıtlı. Sabit `duyarlilik.py`de durur çünkü
  `cozunurluk.py` onu içe aktarır; ters yön bir döngü olurdu.
- Karar mantığı artık **iki ayağı da** uygular; çıktıya `|Δ|/R` sütunu eklendi.
- 🔒 **BAYATLIK KAPISI:** `cozunurluk.py` R'yi her koşumda yeniden ölçüp
  sabitle karşılaştırır ve 0,0005'ten çok ayrışırsa kırmızı yanar. Bu sayının
  bayatlaması tam olarak K-128'in bulduğu hataydı; artık kodda tekrarlanamaz.

## 4 · Mimari denetimi iki kez itiraz etti, ikisinde de haklıydı

1. `R_ESLESTIRILMIS`in köken kaydı yazılmamıştı (D13).
2. Bölünme ölçümünün tohum aralığı `range(2000, 2040)` yazılmıştı; D12'nin
   tarayıcısı sayısal sabitleri ve sayı TABLOLARINI görür, bir **çağrıyı**
   değil. Kayıt yazılmış ama sabit görülmemişti: **ÖLÜ KAYIT**, denetimin
   kendi cümlesiyle *"defterin güvenilirliğini bitirir"*. Sayı demetine
   çevrildi (`BOLUNME_OLCULEN_ARALIK`).

## 5 · Kapılar

| kapı | sonuç |
|---|---|
| `python -m pytest tests2 -q` | **573 passed** |
| `python kalibrasyon/mimari_denetimi.py` | ihlal YOK · **161** parametre · SINANMAMIŞ **41** · ölü kayıt **0** · kökeni yazılmamış **0** · `DUYARSIZ` \|Δ\| **13/13** |
| `python -u kalibrasyon/dugum_sayisi.py --bolunme` | çıkış 0 · statik 0/40 (kontrol) · hareketli kollarda 15/120 |

## BUNU NE DEĞİŞTİRİR

- 🟢 Satır artık kendi tohumundaki ağ bölünmesini SÖYLÜYOR. Bölünmüş bir
  tohumda teslim kaybının bir kısmı yönlendirmeden bağımsızdır ve okuyucu
  bunu satırdan görür.
- 🟢 Duyarlılık aklamaları artık deneyin gerçekte kullanacağı eşiğe karşı
  ve **iki ölçüt birden** uygulanarak yapılıyor; eşik bayatlayamıyor.
- ⚠️ **SINANMAMIŞ 39 → 41.** Borç arttı çünkü iki aklama gerçekte hak
  edilmemişti. `golgeleme_hucre_m` mühürden önce ya kaynakla
  gerekçelendirilecek ya EKSEN ilan edilecek; `onay_bayt` `02` §S2'nin
  802.11b öbeğinde kapanır.
- ⚠️ **Dersin kendisi:** bu oturumda ÜÇ ölçüm aleti (çözünürlük, duyarlılık,
  bölünme) ilan ettikleri kuralı yarım uyguluyordu. `03` §2.1'in ilk
  maddesi: *"bir ölçüm aletine, ölçtüğü şeye güvendiğinden daha az güven."*

---

# K-133 · 🟢 DOĞRULAMA LİSTESİ UÇTAN UCA KOŞTU — 18/18, ve iki şey yakalandı

> **Tarih:** 16 Eylül 2026 · **Koşum:** ajan · **Karar:** öğrenci
> (*"evet, tamamını koş"*)
> **Üretici:** `DEVIR.md` §2'nin 18 maddesi, oradaki komutlarla.
> Aşama 2'ye geçmeden önce; Adım 0–3'ün (K-130 · K-131 · K-132) hepsinden
> SONRA.

## 1 · Neden şimdi

Bugün arayüz, sayaç şeması, gözlem yüzeyi, düşme sebepleri ve köken defteri
değişti. K-129'un dersi *"liste en azından her AŞAMA geçişinde bütün hâlinde
koşulmalıdır"* diyordu; öğrenci koşturmayı seçti.

## 2 · Sonuç — 18 maddenin 18'i

| # | madde | sonuç |
|---|---|---|
| 1 | test takımı | **573 passed** (439 s) |
| 2 | mimari denetimi | ihlal YOK · 161 parametre · ölü kayıt 0 |
| 3 | üretici duman | **13/13 GECTI** (45,6 dk) — 🔴 ilk koşumda KALDI, §3 |
| 4 | bağ kümesi | `G-a` · `G-b` GECTI |
| 5 | karıştırıcı — tarama | **`−15,0 dBm · rho = 0,258`** birebir |
| 5b | karıştırıcı — aile | beş aile GECER · ρ 0,258 · 0,142 · 0,170 · 0,240 · 0,260 birebir |
| 5c | karıştırıcı — açık evre | 0,240 · 0,382 GECER birebir |
| 6 | denetim örneklemesi | 270/270 · Jaccard 1,0000 · **`KAPI OZETI: 4/4`** |
| 7 | adım 9 kapanışı | **HEPSİ TAMAM** |
| 8 | PDR tavanı | 1,000 · 0,999 · 0,996 · **0,915 · 0,844** birebir |
| 9 | evre metrikleri kapıları | **dört kapı GECTI** |
| 10 | kontrol düzlemi | **`KAPI OZETI: 21/21`** · P6 yüzeyi **12/6/5** |
| 11 | Li replikasyonu | **H1 = 0,0871** TUTMADI · H2 · H3 EVET — birebir |
| 12 | çözünürlük | `olcut_bedeli` **0,0230** · **`saklanan sabit TAZE`** |
| 13 | anlamlılık sabitleri | KAPI GECTI |
| 14 | onay semantiği — kapı | dört kapı OK |
| 14b | onay semantiği — Y2 | **16/16 BIREBIR** |
| 15 | üst referans — kapı | üç kapı OK · 🔴 PDR üçlüsü bayat (§4) |
| 16 | regresyon | beş fark, beşi de **ilan edilmiş**; 141 metrik oynamadı |
| 17 | onay semantiği — analiz | çözünürlük üstünde 0 · karar yok 3 — birebir |
| 18 | üst referans — teşhis | 🔴 **kayıtlı değer BAYATMIŞ** (§4) |

🟢 **Bugün bağlanan dört çıkış kodunun üçü bu koşumda konuştu ve yeşil yandı**
(denetim örneklemesi 4/4 · kontrol düzlemi 21/21 · evre metrikleri dört kapı);
dördüncüsü (çözünürlüğün bayatlık kapısı) da ilk gerçek koşumunda `TAZE` bastı.

## 3 · 🔴 BULGU 1 — duman kapısı BENİ yakaladı

İlk koşumda madde 3 **çıkış 1** verdi: `theta_kollari.py` → `KeyError:
'kopmayan'`.

Sebep: K-130'da o alete üç elemanlı demet bastırmıştım (tablo üç tutuyor, alet
iki basıyordu) ama **kopma olmayan kolda** sözlüğe o anahtar hiç yazılmıyordu.
Ve asıl kusur şu: **aleti değiştirip KOŞMAMIŞTIM.** Gerekçem *"Θ ölçümü (C4)
öğrenci kararıyla ertelendi, nasılsa koşmayacak"* idi.

⚠️ K-129'un dersi bu kez bana uygulandı: *koşulmayan kapı kapı değildir.*
Düzeltildi ve **koşuldu**; alet kayıtlı tabloyu birebir yeniden üretiyor:
`statik (None, None, 1.000)` · `bagimsiz (3.25, 16.27, 0.404)` ·
`gorev (3.99, 19.93, 0.275)` · `formasyon (2.31, 11.53, 0.921)`.
Sonra duman koşusu tekrarlandı: **13/13 GECTI, çıkış 0.**

🔒 Bunu yakalayan şey K-129'da eklenen kapsam taramasıydı. Bir kapının değeri,
onu yazanın hatasını yakaladığında görülür.

## 4 · 🔴 BULGU 2 — DÖRDÜNCÜ bayat beklenen değer

Madde 18 (ve aynı üçlüyü taşıyan madde 15) kayıtlı değerinden saptı:

| büyüklük | kayıtlı | ölçülen |
|---|---|---|
| PDR (ETX · atlama · teslim) | 0,9065 · 0,8681 · 0,9633 | **0,9048 · 0,8623 · 0,9658** |
| gecikme ort | 0,0121 · 0,0129 · 0,0402 | **0,0129 · 0,0132 · 0,0506** |
| istek/teslim | 1,97 · 2,00 · 4,65 | 1,97 · 1,97 · **4,99** |

🔒 **Bugünden gelmediği İDDİA EDİLMEDİ, ÖLÇÜLDÜ:** kâhin vakalarının PDR'si
`k127` (15 Eylül 17:14) ile `b6_2026-09-16` arasında **10/10 BİREBİR** aynı.
Kâhin davranışı 15 Eylül'den beri kılı kıpırdamadı.

**Kaynak:** kayıtlı değerler `04` K-114 §4.3'ten, yani **11 Eylül'den — Y2'nin
veri onayı düzeltmesinden ÖNCE.** K-129 bu maddeyi koşturdu ama yalnız ÇIKIŞ
KODUNU kaydetti; alet sayıları basıyor, **kapı kurmuyor**, kimse
karşılaştırmadı.

⚠️ Sınıfı denetimin B3 bulgusunun ta kendisi: *okunmayan kapı da kapı
değildir*. K-129 üç bayat değer bulup düzeltmişti; bu dördüncüsü ve **aynı
sebepten** kaçtı. İki satır da tazelendi ve neden bayatladıkları, bugünden
gelmediğinin kanıtıyla birlikte yazıldı.

## BUNU NE DEĞİŞTİRİR

- 🟢 **Aşama 2'nin zemini temiz ve bu kez uçtan uca sınandı.** Arayüz, sayaç
  şeması, gözlem yüzeyi ve köken defteri bugün değişti; 18 maddenin hepsi
  o değişikliklerden SONRA koşuldu.
- ⚠️ **Kalan yapısal borç:** madde 15 ve 18 hâlâ **kapı değil, rapor**. Bugün
  dört alet çıkış koduna bağlandı; bu ikisi bağlanmadı çünkü bastıkları şey
  bir ölçüttün verdikti değil, bir ÖLÇÜM. Doğru çözüm beklenen değerleri
  koda gömmek değil — o ikinci bir kaynak olurdu — ama bu boşluk üçüncü kez
  bayat sayı üretirse bir kapıya çevrilmeli. Not olarak bırakılıyor.
- ⏭️ **Sırada Aşama 2: AODV.** Arayüz ön koşulu K-131'de, ölçüm bütünlüğü
  K-132'de, zemin sınaması burada kapandı.

---

# K-134 · 🟢 BEYAN KANALI KANCALARA AÇILDI — ve bir düşme sebebi nihayet yolunu buldu

> **Tarih:** 16 Eylül 2026 · **Koşum:** ajan · **Karar:** öğrenci
> (*"kancalar beyan döndürsün"* · *"düşme sebebinin yolunu uygula"*)
> **Üretici:** `python -m pytest tests2/test_kosum.py -q` (13 yeni kapı) ·
> `python -m pytest tests2/test_aodv.py -q`

## 1 · Bulunan boşluk — bir sözleşme yarım kalmıştı

`13` §03 kontrol düzlemini *niyet* üzerine kurdu: protokol çağrı yapmaz,
**niyet döndürür**. Ama niyet doğrulayıcı yalnız iki tipi tanıyordu —
`KontrolIstegi` ve `Uyandirma`. Üçüncü tip, `Beyan`, yalnız `Karar` içinden
geçebiliyordu; yani **veri paketi elde tutarken** bildirilebiliyordu.

Sonuç bir ölçüm boşluğuydu ve U2'yi ifade edilemez kılıyordu: bağ kopması
`iletim_basarisiz` kancasında öğrenilir, ama o kanca `Karar` döndürmez.
Protokol kopmayı **biliyor** ama söyleyemiyordu. Δ, COR ve algılama
duyarlılığı bu beyanlara bağlı (`08`); beyan edilemeyen bir kopma
ölçülemeyen bir kopmadır.

## 2 · Yapılan

| parça | yapı |
|---|---|
| doğrulayıcı | `niyetleri_dogrula(niyetler, beyan_izinli=False)` — kanca yolunda `True`, `Karar` yolunda değişmedi |
| dağıtım | `kosum/kontrol.py::_uygula` `KontrolIstegi`/`Uyandirma` dışındaki niyeti `d.beyan_isle`e verir |
| tek kaynak | `Dugum.beyan_isle(beyan, t_s)` — beyanı işleyen **tek** yer; `Karar` yolu da oraya çıkar |
| döngü kırma | `Beyan` ve `BEYAN_TIPLERI` `gozlem/karar.py`den `gozlem/kontrol.py`ye **taşındı**; `karar.py` onları yeniden dışa verir. Sebep: `kontrol.py` `karar.py`yi içe aktaramaz, döngü olurdu |

🔴 **Taşıma sırasında bir kusur doğdu ve kapı yakaladı.** İki yamadan biri
atomik olarak başarısız olurken diğeri geçti ve ortada **iki `Beyan` sınıfı**
kaldı; `isinstance` sessizce `False` dönmeye başladı. Bir sınıfın iki
tanımının bir gün ayrışması bu projenin kendi hata sınıfıdır (`03` §B5) ve
D16 taraması tam olarak bunun için eklenmişti (K-130).

## 3 · İkinci iş — `rota_gecersiz` nihayet bir yol buldu

`rota_gecersiz` düşme sebebi `DUSME_SEBEPLERI`ne K-131'de eklenmişti ama
**hiçbir kod yolu onu üretmiyordu**: rota yokken de, rota geçersizken de
`hedef_yok` yazılıyordu. Yani şema bir ayrımı taahhüt ediyor, ölçüm onu
yapmıyordu.

`kosum/gonderim.py` artık kararın beyanına bakar:

    sebep = "rota_gecersiz" if karar.beyanlar("rota_gecersiz") else "hedef_yok"

🔒 Ayrım ölçüm için gerçektir: *"hedefi hiç bilmiyorum"* ile *"biliyordum,
bağ koptu"* aynı şey değildir ve ikincisi protokolün kurtarma davranışını
ölçer. U2'nin ara-düğüm kapısı bu ayrımı sınar.

## 4 · Ders

Bir sözleşme *"protokol niyet döndürür"* diyorsa, **niyetlerin hepsi** her
kanaldan geçebilmelidir. Yarım açılmış bir kanal, kapalı bir kanaldan daha
tehlikelidir: protokol bildirdiğini sanır, ölçüm sessizce boş kalır.

---

# K-135 · 🔴 TAMPON BİR YOKLAMA DÖNGÜSÜNE DÖNMÜŞTÜ — makul bir kural ölçümde çöktü

> **Tarih:** 16 Eylül 2026 · **Koşum:** ajan · **Karar:** ajan (ölçümle)
> **Üretici:** ilk gerçek AODV koşumunun teşhis sayaçları
> (`tampon_giris` · `tampon_dusen`)

## 1 · İlk kural ve gerekçesi

K-131 tamponu şöyle kurmuştu: paket rota yokken beklesin; tampon
**`kontrol_alindi` · `uyandi` · `iletim_basarisiz`** kancalarından sonra
yeniden sorulsun. Gerekçe makuldü — üçü de DIŞARIDAN bir olay taşır (bir
cevap geldi, beklenen an doldu, bir bağ koptu), yani rota bilgisi değişmiş
**olabilir**.

Gerekçe makuldü ve **yanlıştı.** İlk gerçek protokol onu ilk günde kırdı.

## 2 · Ölçüm

    1 598 paket  →  146 678 tampon girişi        (ilk kural)
    1 598 paket  →    4 851 tampon girişi        (daraltılmış kural)

Sebep: AODV her RREQ selini **duyar**. Her alınan kontrol mesajı tamponun
tamamını kuyruğa döküyor, her paket yeniden soruluyor, rota hâlâ yok ve
hepsi tampona geri giriyordu. Yani kural, tamponu **kontrol trafiği hızında
dönen bir yoklama döngüsüne** çevirmişti. Bedeli yalnız sayaç değildi: her
tur DCF'yi yeniden çekişmeye sokup vazgeçiriyordu.

## 3 · Yeni kural — tek ve protokole ait

**Yeniden sorulmak isteyen protokol bir `Uyandirma` döndürür.** Simülatör
*"rota bulundu mu"* diye tahmin etmez; bilen taraf protokoldür. Sözleşmenin
zaten istediği disiplin budur (`13` §03.5) ve o yol `uyandi` üzerinden
tampona çıkar.

🔴 **`Beyan("rota_kuruldu")`ya BAĞLANMADI** — oysa anlamı tam oydu. `Beyan`
sözleşmede *"YALNIZ ÖLÇÜME GİDER, simülatörün davranışını değiştirmez"*
diye tanımlıdır. Ölçüm kanalını bir eyleme bağlamak o sözleşmeyi kırardı ve
beyan etmeyen bir protokol sessizce **farklı davranırdı** — yani ölçüm
aracının kendisi deneyi etkilerdi. Bir kolaylık için bir sözleşme
çiğnenmedi.

## 4 · Bir test kırıldı — ve kırılan şey doğru yerdi

`test_tampon_YENIDEN_SORULUP_teslim_ediliyor` daraltmadan sonra 56 paketle
kaldı. Düzeltilen şey **sınav protokolü** oldu (artık kendi `Uyandirma`sını
kuruyor); iddia (`kalan == 0`) **değişmedi**.

🔒 Ayrım bağlayıcıdır ve burada yazılı duruyor: *sınav düzeneğini yeni
sözleşmeye uydurmak* meşrudur, *iddiayı sonuca uydurmak* değildir.

## 5 · Ders

Bir davranış kuralının gerekçesi makul olabilir ve kural yine de yanlış
olabilir. Ayıran şey otorite değil, **üretici komutu olan bir sayıdır**.
146 678 sayısı bir tartışmayı bitirdi; hiçbir gerekçe bitiremezdi.

---

# K-136 · 🟢 AŞAMA 2 AÇILDI — AODV yazıldı, U1–U4 geçti, ve U1'in kapısı YANLIŞ YERDEYDİ

> **Tarih:** 16–17 Eylül 2026 · **Koşum:** ajan · **Karar:** öğrenci
> (U1 eşiği · yerel onarım) · **Kayıt:** ajan
> **Üreticiler:**
> `python -m pytest tests2 -q` (595) ·
> `python -u kalibrasyon/aodv_uygunluk.py` ·
> `python kalibrasyon/mimari_denetimi.py`

## 1 · Yazılan

| dosya | ne |
|---|---|
| `protokoller/aodv_bicim.py` | RFC 3561 §5 biçimleri ve §10 sabitleri — **tek kaynak**. Boyutlar alan tablosundan TÜRER; protokol bir bayt yazamaz |
| `protokoller/aodv.py` | Tam AODV: genişleyen halka araması · sıra numaraları · öncül listesi · RERR · rota tamponu · HELLO |
| `tests2/test_aodv.py` | **18 kapı** — RFC bayt sayıları · RFC türetmeleri · U1 (yapı) · U2 · U3 · U4 |
| `kalibrasyon/aodv_uygunluk.py` | U1'in **sayısal** yarısı, tam ölçekte; verdikt çıkış kodunda |

🔒 `kosum_beaconi = False` bildirip komşuluğu **kendi HELLO'sundan** kuruyor
(R2). Böylece A14 borcu (koşum düzeyinde tek 1 s beacon) AODV'yi etkilemiyor;
borç OLSR'ındır ve açık kaldı.

## 2 · İki kusur — ikisi de ÖLÇÜMLE bulundu, ikisi de benimdi

### 2.1 · HELLO ayıracı fazla genişti

    rrep_uretilen = 95   ·   rrep_iletilen = 0

RFC §6.9 HELLO'yu ayrı bir mesaj yapmaz: TTL = 1 olan, **hedefi kendisi olan**
bir RREP'tir. İlk ayıracım "TTL = 1" idi ve o, **gerçek** RREP'lerin son
atlamasını da HELLO sanıyordu; hiçbir RREP iletilmiyordu. Doğru ayıraç
`kaynak == hedef`.

    PDR 0,4005  →  0,9875        keşif başarısızlığı 12 → 0

⚠️ Bu kusuru bulan şey bir test değil, bir **teşhis sayacıydı** — üretilen ve
iletilen RREP'lerin ayrı sayılması. Sayaçlar olmasa PDR düşüklüğü
"karıştırma zaten böyle" diye okunabilirdi.

### 2.2 · Tampon bir yoklama döngüsüne dönmüştü

K-135'te ayrı yazıldı: 1 598 pakete karşı **146 678 tampon girişi**.

## 3 · 🔴 U1'İN KAPISI YANLIŞ YERDEYDİ — ve kırmızı yanması bir teşhis değildi

İlk yazımda U1'i teste **mutlak** bir eşik olarak koydum: `PDR ≥ 0,95`. Test
kırmızı yandı (0,851) ve ilk tepkim *"başlangıç geçişi olabilir"* oldu. Onu
ölçtüm ve **çürüttüm**: pencere uzadıkça 0,851 → 0,866 → 0,874, yani geçiş
vardı ama farkı kapatmıyordu.

Asıl sebep eşiğin **yanlış dünyada** durmasıydı. `06` §4.3'ün ölçütü *"teslim
oranı KÂHİN REFERANSINA yakın"*dır ve o referans konfigürasyona bağlıdır; ben
tam ölçekte ölçülmüş bir sayıyı (0,996–1,000) 14 düğümlük test dünyasına
uygulamıştım. Aynı dünyada ölçülünce:

    kâhin 0,9687   ·   AODV 0,8512   ·   oran 0,879

🔴 **Bu noktada neredeyse yeni bir ölçüt uydurdum.** *"AODV ≥ atlama kâhini"*
diye bir kapı önerecektim — kulağa doğru geliyordu. **Önce ölçtüm: 4/9.**
İddia dokuz (senaryo, tohum) çiftinin beşinde tutmuyordu; önerilmedi.

🔒 Ders, bu oturumun en pahalı dersi: *bir kapının kırmızı yanması, kapının
doğru olduğunun kanıtı değildir.* Önce kapının kendisi ölçülür.

## 4 · U1'in yeni hâli — oran, ve iki yarı

    oran = PDR(protokol) / PDR(EnGuvenilirKahin)      ← AYNI konfigürasyon

    🔒 statik kol     oran ≥ 0,90       ← öğrenci kararı, 17 Eylül
    🔒 hareketli kol  oran ≥ 0,60

Oran biçiminin üçüncü kazancı: §4.3'ün *"bağlı ağ"* ön koşulu **kendini
nötrler** — kâhinin geçemediği bir bölünme paydayı da düşürür, yani
topolojinin kusuru protokolün hanesine yazılmaz.

| yarı | yer | ne sınar |
|---|---|---|
| yapı | `tests2/test_aodv.py` | keşif tamamlanıyor · çok atlamalı teslim var · defter kapanıyor · **AODV kâhini GEÇMİYOR** — eşiksiz |
| sayısal | `kalibrasyon/aodv_uygunluk.py` | dört `-yok` kolu × üç tohum, TAM pencerede; verdikt çıkış kodunda |

### 4.1 · Ölçülen — TAM pencerede

🔒 **KOD HÂLİ: `AODV-a`** (ilk yazım). Bu tablo, aşağıdaki §9'un bulduğu iki
RFC kusuru düzeltilmeden ÖNCE ölçüldü ve bilerek burada duruyor — §9'un
"önce/sonra" karşılaştırması buna dayanıyor. Etiket tablosu: `DEVIR.md` §2.
⚠️ AODV'nin bugünkü hâli `AODV-c`; onun tablosunu **kapanış paketi** üretecek.

| kol | tohum | AODV | ETX kâhini | oran | eşik | karar |
|---|---|---|---|---|---|---|
| `statik-yok` | 1000 | 0,9777 | 1,0000 | **0,978** | 0,90 | GEÇTİ |
| `statik-yok` | 1001 | 0,9856 | 1,0000 | **0,986** | 0,90 | GEÇTİ |
| `statik-yok` | 1002 | 0,8644 | 0,9962 | **0,868** | 0,90 | 🔴 KALDI |
| `bagimsiz-yok` | 1000 | 0,7129 | 0,9123 | **0,781** | 0,60 | GEÇTİ |
| `bagimsiz-yok` | 1001 | 0,6036 | 0,8455 | **0,714** | 0,60 | GEÇTİ |
| `bagimsiz-yok` | 1002 | 0,4102 | 0,8165 | **0,502** | 0,60 | 🔴 KALDI |
| `gorev-yok` | 1000 | 0,7215 | 0,9115 | **0,792** | 0,60 | GEÇTİ |
| `gorev-yok` | 1001 | 0,3221 | 0,7394 | **0,436** | 0,60 | 🔴 KALDI |
| `gorev-yok` | 1002 | 0,4839 | 0,7826 | **0,618** | 0,60 | GEÇTİ |
| `formasyon-yok` | 1000 | 0,7960 | 0,8946 | **0,890** | 0,60 | GEÇTİ |
| `formasyon-yok` | 1001 | 0,6910 | 0,8967 | **0,771** | 0,60 | GEÇTİ |
| `formasyon-yok` | 1002 | 0,4979 | 0,8122 | **0,613** | 0,60 | GEÇTİ |

    kol ortalamaları :  statik 0,944 · bagimsiz 0,666 · gorev 0,615 · formasyon 0,758
    kol en düşükleri :  statik 0,868 · bagimsiz 0,502 · gorev 0,436 · formasyon 0,613
    24 koşum · 14 332 s (~4 saat, 6 işçi)

🔴 **U1 KALDI — 12 çiftin 3'ünde.** Çıkış kodu 1.

### 4.3 · Ölçülen desen — ve iki şey karıştırılmamalı

AODV'nin oranı, **kâhinin kendi PDR'si düştükçe** düşüyor:

    kâhin 1,000 → oran 0,978 · 0,986        (statik, kolay topoloji)
    kâhin 0,912 → oran 0,781 · 0,792
    kâhin 0,739 → oran 0,436                (en zor topoloji, en kötü oran)

Yani zorlaşan ağda AODV **orantısız** kaybediyor. Bu şaşırtıcı değil ve tam
olarak deneyin ölçmek istediği şey: tepkisel bir protokol rotayı önce
**bulmak** zorundadır ve ağ zorlaştıkça keşfin kendisi de zorlaşır. Ama bir
KABUL kapısı için bu bir açıklama değil, bir bulgudur.

### 4.4 · 🔴 KAPININ BİÇİMİNİ DEĞİŞTİRMEDİM — ve bunu yazıyorum

Alet her (kol, tohum) çiftini ayrı ayrı sınıyor ve **biri kalırsa kapı
kalıyor**. Çıktının alt tablosu kol ORTALAMALARINI da basıyor ve o
ortalamalarla **dört kolun dördü de geçerdi** (0,944 · 0,666 · 0,615 ·
0,758 — hepsi kendi eşiğinin üstünde).

🔒 **Biçimi değiştirmedim.** Çift-başına sınama, sonuçlar görülmeden önce
yazılmıştı; sonucu gördükten sonra ortalamaya geçmek, eşiği gevşetmenin
kılık değiştirmiş hâlidir ve `03` §2.1'in yasakladığı şeyin tam kendisidir.
Ortalamaların burada yazılı olmasının sebebi şeffaflık: öğrenci biçimi
değiştirmek isterse, bunu **bilerek** ve ayrı bir kayıtla yapmalı.

⚠️ Ayrıca ortalama biçimi tek başına daha zayıf bir kapıdır: üç tohumluk bir
ortalama, bir tohumun çökmesini ikisinin iyiliğiyle örter. `gorev-yok`
1001'de AODV'nin PDR'si **0,32** ve bunu bir ortalamanın arkasına saklamak,
kapının varlık sebebini ortadan kaldırır.

### 4.2 · 🔴 Eşik sayılar GÖRÜLDÜKTEN SONRA seçildi

Ön-kayıt disiplini ölçütün ölçümden ÖNCE yazılmasını ister (`03` §2) ve
burada öyle olmadı. Gizlenmiyor; üç hafifletici sebeple taşınıyor:

1. U1 bir **kabul kapısıdır**, hipotez testi değil (`06` §4.4 madde 3).
   Hiçbir sonuç iddiası bu eşiğe dayanmıyor ve dayanmayacak.
2. Eşik **üç taban protokolü de** bağlar; AODV'ye göre ayarlanmış olması
   OLSR ve AOMDV'ye avantaj sağlamaz — tersine, daha sıkıdır.
3. Seçenekler, hangisinin bugün geçtiği açıkça yazılarak sunuldu.

⚠️ **Ve kanıt tabanı seçimden sonra kaydı.** Öğrenciye gösterilen dört oran
KISA pencerede ölçülmüştü (`ısınma 10 · ölçüm 40 · koşu 50 s`); kapı GERÇEK
pencerede koşuyor. Aynı koşu tam pencerede 0,9875 değil **0,9777** verdi —
yön aşağı. **Eşik buna rağmen değiştirilmedi:** sonuç görüldükten sonra bir
ölçütü gevşetmek de sıkmak da aynı hatadır (`03` §2.1). OLSR ve AOMDV
yazıldığında eşik onların da karşısında sınanacak; gerekirse karar yeniden
alınır ve **ayrı bir kayda** geçer.

## 5 · Beyan edilen sapmalar (`06` §4.4 madde 4)

Dört RFC özelliği uygulanmadı; tablosu `06` §4.4'te ve
`protokoller/aodv_bicim.py` başlığında. **Yerel onarım (§6.12) öğrenci
kararıyla dışarıda** ve ⚠️ tek zayıflatıcı olan odur: karıştırma altında
kopma sıktır ve yerel onarım tam orada iş görür. Sonuç raporlanırken bu
sapma yanında anılacak.

⚠️ Bir sapma TERS yönde: RREQ'te bir bayt FAZLA ödeniyor (RFC 24 → 25),
çünkü RFC'de TTL IP başlığındadır ve simülatörde bir çerçeveye "IP TTL"
koymanın yolu yok. Yani `nrl_*` karşılaştırmasında AODV'nin **lehine** bir
sapma yok.

## 6 · Yol boyunca kapatılan üç borç

| borç | durum |
|---|---|
| `04`ün kayıt indeksi **K-088'de donmuştu** (47 kayıt görünmüyordu) | 🟢 üreticisi onarıldı: kök SABİT bir üst dizin sayısıyla türüyordu (`parent.parent`) ve betik `arsiv/`e taşınınca `arsiv/v2/04-...` diye var olmayan bir dosya arıyordu. Kök artık ARANAN DOSYADAN türer. İndeks yeniden üretildi: **135 kayıt** |
| `07` §15 *"öğrenci kararlarının tek listesi"* **11 Eylül'de donmuştu** | 🟢 beş günlük karar geri dolduruldu (11 Eylül dördüncü tur · 15 · 16 · 17 Eylül) |
| U1 yapı kapısının son iddiası `pdr <= 1.0` idi | 🔴 **hiç ateş edemeyecek bir kapıydı** — PDR tanımı gereği 1'i aşamaz, ama yorumu *"kâhini geçmek de bir hatadır"* diyordu. Yorum bir şey iddia ediyor, iddia başka bir şey sınıyordu. 🟢 Kâhin artık AYNI dünyada gerçekten koşuyor ve sıralama sınanıyor |

## 7 · Bir tarayıcı sınırı — kapatılmadı, YAZILDI

`KOLLAR` sabitini köken defterine yazdım ve D12 onu **ölü kayıt** ilan etti.
Sebep: tarayıcı yalnız **sayı** tablolarını görüyor, `KOLLAR` bir metin
demeti. Genişletmenin bedelini ölçtüm — depoda **48** salt-metin tablosu var
ve neredeyse tamamı SÖZLÜK (`DUSME_SEBEPLERI`, `DCF_DURUMLARI`, `KANCALAR`,
`KOVALAR`); *"neden BU DEĞER"* sorusu onlar için anlamsız.

🔒 Karar: tarayıcı **genişletilmedi**, kayıt geri alındı (emsal
`dugum_sayisi.py::BOLUNME_KOLLARI` de kayıtsız). Gerekçe kodun kendi
yorumunda duruyor.

⚠️ **Ama sınır gerçek:** bir metin tablosu bazen bir SÖZLÜK, bazen bir SEÇİM
olur (`KOLLAR` bir seçimdir) ve tarayıcı ikisini ayırt edemiyor. Ayırt edici
bir kural düşünülebilir — *başka bir ilan edilmiş kümenin alt kümesi olan
metin tablosu bir seçimdir* — ama bu, kendi doğrulamasını isteyen yeni bir
tarama olur. Not olarak bırakılıyor.

## 8 · Sırada

- ⏭️ **`rota_tamponu_omru_s` (30 s) ölçülecek** — ölçüm penceresinin %11'i ve
  değeri NS-2 geleneğinden, bu projede ölçülmedi. Artık gerçek bir protokol
  var, ölçülebilir.
- ⏭️ Protokolsüz kapanmayan diğer beş parametre.
- ⏭️ **OLSR** (A14 borcu orada ölçülür), sonra **AOMDV**.
- ⏭️ M4'ün boş kol kapısı (`08`) — AODV kopma beyan ediyor, koşulabilir.

## 9 · 🔴 U1 KALDI — ve öğrencinin sorduğu soru: kusur mu, bulgu mu?

> **Öğrenci (17 Eylül):** *"AODV'nin çalışmasında ve genel olarak
> simülasyonun çalışmasında herhangi bir sıkıntı yoksa … bağların
> konumundan dolayı AODV'nin çalışma prensibinin zayıf noktasını gösteriyor,
> bu araştırmada değerli bir şey. Öte yandan yazılımla ilgili bir problemden
> kaynaklıysa bu düzeltilmeli. Karar senin."*

Soru ölçüldü ve cevabı **ikisi birden**: bir yazılım kusuru VARDI, bulundu
ve düzeltildi; kalan fark ise AODV'nin kendi ölçütünün zayıflığı.

### 9.1 · Önce yazılım kusuru — RFC §6.9 yarım uygulanmıştı

`statik-yok/1002`in teşhis sayaçları imkânsız bir şey söylüyordu: topolojinin
hiç değişmediği bir koşuda **7 671 komşu zaman aşımı**, 11 961 RERR, 96 992
bastırılmış RREQ. Birincil belge açıldı (RFC 3561 §6.9, 17 Eylül):

> *"…does not receive any packets (**Hello messages or otherwise**) for more
> than ALLOWED_HELLO_LOSS \* HELLO_INTERVAL milliseconds, the node SHOULD
> assume that the link to this neighbor is currently lost."*

**"Any packets — or otherwise".** Bendeki gerçeklemede komşuluğu yalnız
kontrol mesajları tazeliyordu; veri taşıyan bir bağ, HELLO'su çakıştığı anda
ölü sayılıyordu. Doğan şey bir geri beslemeydi: sahte kopma → RERR → yeniden
keşif → RREQ seli → daha çok çarpışma → daha çok sahte kopma.

🔒 Düzeltme: paketi bir komşuya devretmek temas kanıtıdır. MAC ya onaylar
(yani o komşudan bir çerçeve gelir — §6.9'un saydığı şey) ya da vazgeçer, ve
vazgeçtiğinde `iletim_basarisiz` komşuyu **zaten aynı anda** düşürür. Yani
tazeleme ölü bir bağı ayakta tutamaz.

| `statik-yok` | 1000 önce | 1000 sonra | 1002 önce | 1002 sonra |
|---|---|---|---|---|
| PDR | 0,9777 | **0,9960** | 0,8644 | **0,8753** |
| keşif sayısı | 319 | **56** | 1 419 | 1 305 |
| bastırılan RREQ | 28 611 | **6 083** | 96 992 | 84 073 |
| iletim başarısızlığı | 237 | **40** | 1 450 | 1 398 |

🔴 **TAHMİNİMİN YARISI ÇÖKTÜ.** Ölçümden önce *"`komsu_zaman_asimi` sert
düşecek"* yazmıştım. **Düşmedi** (7 722 → 7 474). Sebebi sonradan ölçüldü:
§6.9 HELLO'yu yalnız etkin rotadaki düğümlere gönderttiği için boştaki
düğümler birbirinin tablosundan normal olarak düşüyor ve o kırpınma
zararsız. Zararlı olan altküme — **sonraki atlama olan** komşular —
düzeldi; PDR sıçraması oradan geliyor. Yani düzeltme doğruydu ama onu
doğrulayan sayaç, benim gösterdiğim sayaç değildi.

### 9.2 · Kalan fark yazılım değil — AODV'nin ÖLÇÜTÜ

AODV'nin bir **bağ kalitesi eşiği yoktur**; RFC 3561 atlama sayısıyla
yönlendirir. RREQ hangi bağdan geçtiyse rota oraya kilitlenir ve hedef,
**ilk ulaşan** RREQ kopyasının ters yoluna cevap verir — ilk ulaşan kopya da
genelde en az atlamalı, yani en uzun bağlı olandır.

Aynı iki dünyada, gerçek akış çiftleri üzerinden yol kalitesi *(simülasyon
yok, yalnız kanal grafiği)*:

| | ETX yolu | en az atlama (eşikli bağlar) | **en az atlama (bütün bağlar)** |
|---|---|---|---|
| tohum 1000 | 1,0000 | 0,9891 | **0,6993** · 3/10 akış < 0,90 |
| tohum 1002 | 0,9969 | 0,9884 | **0,3885** · **7/10 akış < 0,90** |

İki tohum arasındaki fark ETX yolunda yok (1,000 ↔ 0,997) ve eşikli atlama
yolunda da yok (0,989 ↔ 0,988). Fark **yalnız** eşiksiz atlama yolunda var —
yani tam olarak AODV'nin çalıştığı yerde.

🔒 Bağımsız doğrulama, **başka bir amaçla ve daha önce** ölçülmüş: kâhin
grafiğinin kendi belgesinde (`kahin.py::_tek_deneme_basarisi`) tam bu tohum
anılıyor — *"ölçüldü (statik-yok, t=1002): eşikli grafikteki bağların %26'sı
sönümleme hesaba katılınca %90 eşiğinin altındaydı; en kötü bağ 0,374 →
0,000."* 1002, deponun zaten bildiği **en zayıf bağlı** tohum.

⚠️ AODV'nin ölçülen 0,8753'ü, saf "eşiksiz en kısa yol" sınırından (0,3885)
çok daha iyi. Sebep mekanizmanın kendisinde: zayıf bağ RREQ'i de düşürür,
kopma RERR doğurur, yeniden keşif daha iyi bir yol bulabilir. Yani AODV
kendi patolojisini kısmen onarıyor — ama ETX kâhinine yetişemiyor.

### 9.3 · 🔴 İLAN ETTİĞİM AYIRT EDİCİ SINAV KARIŞTIRICI ÇIKTI

Ölçümden önce şunu yazmıştım: *"AODV'yi ATLAMA kâhini ile karşılaştır; fark
iki tohumda benzerse gerçek zayıflık, 1002'de büyükse yazılım kusuru."*

**Sınav kusurlu.** `EnKisaYolKahin` `_komsu` grafiği üzerinde koşuyor ve o
grafik yalnız `ATLAMA_ESIGI = 0,90`ı geçen bağları içeriyor. Yani o kâhin
*"mükemmel bilgiye sahip AODV"* değil, *"mükemmel bilgiye sahip **ve bağ
kalitesi süzgeci olan** AODV"* — oysa AODV'de eksik olan tam o süzgeç.
Kâhinin kendi belgesi bunu zaten söylüyordu ve ben sınavı yazarken
okumamıştım.

🔒 Sınav yine de koşuldu ve sonucu §9.4'te; ölçütü sonucu gördükten sonra
değiştirmemek için. Ama **ağırlık yapısal ölçümdedir** (§9.2): o ölçüm
kâhinlerin hiçbirine bağlı değil, doğrudan kanal grafiğinden okunuyor.

### 9.4 · Karar

Sınav koştu (`statik-yok`, §6.9 düzeltmesinden SONRA):

| tohum | AODV | atlama kâhini | ETX kâhini | fark (atlama − AODV) |
|---|---|---|---|---|
| 1000 | 0,9960 | 0,9845 | 1,0000 | **−0,0115** |
| 1002 | 0,8753 | 0,9858 | 0,9962 | **+0,1105** |

İlan ettiğim kuralın LAFZINA göre bu *"yazılım kusuru"* der: fark 1002'de
çok daha büyük. Kuralı değiştirmiyorum, sonucunu yazıyorum — ve §9.3'te
ölçümü görmeden ilan ettiğim karıştırıcı tam olarak burada görünüyor:
atlama kâhini 1002'de **0,9858** alıyor, yani *atlama-sayısı ölçütünün
kendisi* sorun değil; **süzgeçsiz bağlar üzerinde** atlama-sayısı sorun.
Kâhinin 0,9858'i ile yapısal tablonun eşikli atlama yolu (0,9884) birbirini
doğruluyor.

🔒 **VE HİÇBİR YORUMA İHTİYAÇ DUYMAYAN KANIT:** tohum 1000'de AODV atlama
kâhinini **GEÇİYOR** (0,9960 > 0,9845). Mükemmel topoloji bilgisine sahip
bir atlama yönlendiricisinden daha iyi iş çıkaran bir gerçekleme bozuk
değildir. Sebep mekanizmanın kendisinde ve `EnKisaYolKahin`in belgesinde
zaten yazılı (*"en az atlama, en uzun — yani en kötü — bağı seçer"*):
AODV'nin fiilî ölçütü **"ilk ulaşan RREQ"**tir — atlama sayısı ile bağ
güvenilirliğinin karışımı, çünkü zayıf bağ RREQ'i de düşürür. İyi
topolojide bu karışım kâhini geçiyor; zayıf bağların bol olduğu 1002'de
bozuluyor, çünkü bir bağ tek bir RREQ'i hızla geçirip sonra veriyi
taşıyamayabilir.

**Sonuç:** AODV 0,3885 (saf süzgeçsiz en kısa yol) ile 0,9858 (süzgeçli en
kısa yol) arasında, 0,8753'te duruyor. Ayıran değişken tek: **AODV'de bağ
kalitesi kabul eşiği YOKTUR.**

**Kusur düzeltildi, bulgu raporlanacak.** U1'in statik koldaki eşiği
(0,90) `statik-yok/1002`de tutmuyor ve sebebi bir yazılım hatası değil:
AODV'nin atlama-sayısı ölçütü, bağ kalitesi çok değişken bir topolojide
kötü yol seçiyor. Bu, `06` §5.1 H1.1'in *"protokol ailesi bozunumu
belirler"* hipotezinin tam da ölçmek istediği şey.

⚠️ **Eşiğe DOKUNULMADI ve kapının biçimi DEĞİŞTİRİLMEDİ.** Bir kabul
kapısının bir tohumda kırmızı yanması, o tohumu kapsam dışı bırakmanın
gerekçesi değildir. Kararı öğrenci verecek; seçenekler ve her birinin
bedeli `12` §4'e yazıldı.

### 9.5 · Düzeltmeden SONRA — üç kırmızı çift yeniden ölçüldü

🔒 Bu bir TANI koşumudur, kapı değil: yalnız kırmızı çiftleri koşar. Kapının
kendisi tam kümeyi koşar ve verdikt oradan gelir.

| vaka | önceki oran | sonraki oran | eşik | karar |
|---|---|---|---|---|
| `statik-yok/1002` | 0,868 | **0,879** | 0,90 | KALIR |
| `bagimsiz-yok/1002` | 0,502 | **0,497** | 0,60 | KALIR |
| `gorev-yok/1001` | 0,436 | **0,443** | 0,60 | KALIR |

**Üçü de kırmızı kaldı.** §6.9 düzeltmesi sağlıklı dünyaları kurtardı
(`statik-yok/1000`: 0,978 → **0,996**), zayıf bağlı dünyaları kurtarmadı.
Hareketli kollarda etkisi neredeyse sıfır ve bunun sebebi anlaşılır:
orada bağlar **gerçekten** kopuyor, yani komşu zaman aşımlarının çoğu
sahte değildi.

⚠️ Bu, §9.2'nin teşhisini bağımsız olarak doğruluyor: kusur giderilince
kusurun açıkladığı kadarı düzeldi, geri kalan durdu.

---

# K-137 · 🟢 U1 İKİYE AYRILDI — uygunluk bir KAPI, başarım bir BULGU

> **Tarih:** 17 Eylül 2026 · **Karar:** öğrenci (*"senin önerin olan A
> seçeneğini seçiyorum"*) · **Kayıt ve uygulama:** ajan
> **Üretici:** `python -u kalibrasyon/aodv_uygunluk.py`
> **Bağlam:** K-136 §9 — U1 ilk koşumunda 12 çiftin 3'ünde kaldı ve sebebi
> ölçüldü: yazılım kusuru DEĞİL.

## 1 · Karar

`12` §4'te dört seçenek bedelleriyle sunuldu. Seçilen **A**: *eşik yerinde
kalsın, AODV'nin o hücrelerde geçemediği bir BULGU olarak raporlansın.*

🔒 Reddedilenler ve sebepleri kayda geçiyor, çünkü bir seçimin değeri
neyin reddedildiğiyle ölçülür:

| seçenek | neden seçilmedi |
|---|---|
| B · kol ORTALAMASINA bak | Dört kolun dördü de geçerdi (0,944 · 0,666 · 0,615 · 0,758). Sonucu gördükten sonra biçim değiştirmek, eşiği gevşetmenin kılık değiştirmiş hâli; ayrıca bir tohumun çökmesini (0,32) iki iyi tohum örter ve kapı körleşir |
| C · eşiği düşür | Aynı itiraz, artı: eşik ÜÇ taban protokolü birden bağlıyor; AODV'ye göre indirilen bir eşik OLSR ve AOMDV için de gevşer |
| D · "bağlı ağ" ön koşulunu bağ KALİTESİNE genişlet | Gizli bedeli büyük: zayıf bağlı topolojileri kapsam dışı bırakmak, karıştırma altındaki bir tatbikat ağında tam da ölçülmek istenen zorluğu deneyden çıkarmak olur |

## 2 · A'nın bedeli ödendi — `06` §4.4 madde 3 yeniden yazıldı

A'nın tek bedeli ön-kayıttaki cümleydi: *"U1–U4 koşulur; geçilmeden protokol
kabul edilmez."* O cümle olduğu gibi kalsaydı AODV taban protokol olarak
kullanılamazdı.

🔴 Ama cümleyi **gevşetmek** yerine, altındaki kavram karışıklığı düzeltildi.
U1 iki ayrı soruyu tek kapıya bağlamıştı:

    "gerçekleme RFC'ye sadık mı?"     ← bir KABUL ölçütü
    "protokol iyi teslim ediyor mu?"  ← deneyin kendi SONUCU

İkincisi bir kabul ölçütü olamaz. AODV'nin zayıf bağlı bir topolojide kötü
teslim vermesi, gerçeklemenin bozuk olduğunu göstermez — RFC 3561 atlama
sayısıyla yönlendirir ve **bağ kalitesi eşiği yoktur**. Yani eski hâliyle
madde 3, kendi deneyinin bulgusunu bir "başarısızlık" sayıp protokolü
reddederdi.

| parça | ne sorar | kaldığında |
|---|---|---|
| **U1-U · uygunluk** | keşif tamamlanıyor · teslim çok atlamalı · defter kapanıyor · protokol **kâhini geçmiyor** | 🔴 protokol KABUL EDİLMEZ |
| **U1-B · başarım** | PDR / ETX kâhini oranı (statik ≥ 0,90 · hareketli ≥ 0,60) | 🟡 reddedilmez, ama hücre AÇIKLANMADAN geçilemez |

## 3 · 🔒 KAPININ DİŞİ — "açıklanmadan geçilemez" ne demek

Bu, A'yı bir gevşetme olmaktan çıkaran şeydir ve koda bağlıdır:

1. Eşiğin altındaki her (kol, tohum) hücresi için **ölçümle** gösterilmek
   zorunda: kayıp bir yazılım kusurundan değil, protokolün mekanizmasından
   geliyor.
2. Açıklaması kayda geçmemiş bir düşük hücre kapıyı **kırmızı yakar**
   (çıkış kodu 1). Yeni bir düşük hücre asla sessizce geçemez.
3. 🔴 **Ters yön de denetlenir:** açıklanmış listede olup ARTIK düşük
   OLMAYAN bir hücre **ölü kayıttır** ve kapı onu da kırmızı yakar. Köken
   defterinin D12 taramasıyla aynı disiplin — bir muafiyet listesi, kendi
   bayatlığını gizleyemez.

## 4 · Bugünkü üç hücrenin açıklaması — ÖLÇÜLDÜ

Ayıran değişken tek: **eşiksiz en kısa yolun uçtan uca teslimi.** AODV'nin
bağ kalitesi kabul eşiği yoktur; hedef, **ilk ulaşan** RREQ kopyasının ters
yoluna cevap verir ve o kopya genelde en az atlamalı, yani en uzun bağlı
olandır.

🔒 **BU TABLO AODV'NİN KODUNA BAĞLI DEĞİLDİR** ve bu onun en güçlü tarafı:
simülasyon koşmaz, doğrudan kanal grafiğinden okunur. `AODV-a`, `-b`, `-c`
hangisi olursa olsun aynı sayıları verir; yani AODV değiştikçe bayatlamaz.
(U1 sütunu `AODV-a`nın verdiktidir ve kapanışta tazelenecek.)

| kol | tohum | U1 | ETX yolu | eşikli atlama | **eşiksiz atlama** |
|---|---|---|---|---|---|
| `statik-yok` | 1000 | geçti | 1,0000 | 0,9891 | **0,6993** |
| `statik-yok` | 1002 | **kaldı** | 0,9969 | 0,9884 | **0,3885** |
| `bagimsiz-yok` | 1000 | geçti | 0,9922 | 0,9798 | **0,4589** |
| `bagimsiz-yok` | 1001 | geçti | 0,9861 | 0,9734 | **0,3718** |
| `bagimsiz-yok` | 1002 | **kaldı** | 0,9807 | 0,9642 | **0,2386** |
| `gorev-yok` | 1000 | geçti | 0,9887 | 0,9816 | **0,5519** |
| `gorev-yok` | 1001 | **kaldı** | 0,9826 | 0,9520 | **0,2502** |
| `gorev-yok` | 1002 | geçti | 0,9837 | 0,9634 | **0,2937** |

🔒 **Her kolda kırmızı hücre, kendi kolunun en kötü eşiksiz atlama yoluna
sahip.** ETX yolu (0,981–0,992) ve eşikli atlama yolu (0,952–0,989) hiçbir
şey ayırt etmiyor — aralıkları U1 oranının aralığını (0,44–0,79)
açıklayamayacak kadar dar. Ağ hiçbir anda bölünmüyor, yani bağlantı sorunu
değil.

⚠️ Üretici: yapısal ölçüm **simülasyon koşmaz**, doğrudan kanal grafiğinden
okur (hareketli kollarda ölçüm penceresi boyunca altı an). Yani kâhinlerin
hiçbirine bağlı değildir — K-136 §9.3'te bulunan karıştırıcıdan bağışıktır.

## 5 · Ders

Bir kapı kırmızı yandığında sorulacak ilk soru *"eşik yanlış mı"* değildir.
Sırası şudur ve bu sıra bu oturumda üç kez işe yaradı:

    1. Kapı DOĞRU ŞEYİ mi ölçüyor?      → U1 yanlış dünyadaydı (K-136 §3)
    2. GERÇEKLEME doğru mu?             → RFC §6.9 yarım uygulanmıştı (§9.1)
    3. Kalan fark NEREDEN geliyor?      → ölçüldü: protokolün ölçütü (§9.2)
    4. Ancak bundan SONRA eşik konuşulur.

🔴 Ve dördüncü adımda bile eşik **değişmedi**. Değişen şey, kapının neyi
reddetmesi gerektiğiydi.

---

# K-138 · 🟡 HIZ ARAŞTIRMASI — üç hipotez, üçü de ÖLÇÜMDE çöktü; bir borç kapandı

> **Tarih:** 18 Eylül 2026 · **Soru:** öğrenci (*"veriyi parça parça alsak ·
> koşumları CUDA ekran kartı üzerinden yapma ihtimalimiz var mı"*) ·
> **Ölçüm ve karar:** ajan
> **Üreticiler:** `cProfile` kesiti · çalışma anında sarmalama sayımı ·
> `python -u kalibrasyon/sonumleme_onbellegi.py 4`

## 1 · Ölçülen — zaman NEREYE gidiyor

Kısa pencere (50 s), AODV, tohum 1000, profilci altında:

| | `statik-yok` | `bagimsiz-yok` |
|---|---|---|
| toplam | 105 s | **863 s** |
| sönümleme güç kazancı | ~0 *(donuk)* | **600 s · %69** |
| FIR süzgeç çağrısı | — | 8,7 M |
| yenilik adımı | — | **229 M** |
| Gauss çekimi | — | 36 M |

🔒 Statik kolda sönümleme DONMUŞ olduğu için bu maliyet hiç yok. Gerçek
koşumlardaki **12 kat** statik–hareketli farkının tamamı buradan geliyor.
Olay kuyruğu, MAC, protokol ve gözlem katmanı gürültü seviyesinde — yani
hızlandırılacak tek bir yer var ve o yer fizik çekirdeği.

## 2 · 🔴 ÜÇ HİPOTEZ, ÜÇÜ DE ÇÖKTÜ

Üçünü de ölçümden ÖNCE yazdım; üçü de yanlış çıktı. Bu kaydın asıl değeri
bu — hız işinde sezgi neredeyse her zaman yanılıyor.

**(a) "Önbellek taşıyordur."** Sönümleme yenilik önbelleğinin sınırı
250 000 ve 50 saniyelik bir koşu **36 milyon FARKLI** yenilik istiyor; sınır
144 kat küçük görünüyordu. **Yanlış:** çağrı 229 M, farklı 36 M, gerçek
çekim 36 M — yani **her farklı değer tam bir kez çekiliyor**. Önbellek
zaten optimal; yerellik o kadar iyi ki tahliye hiçbir değeri erken
düşürmüyor. Sınırı büyütmek sıfır kazandırır *(ve zaten imkânsız: tam
pencerede ~250 milyon farklı değer gerekiyor)*.

**(b) "Bellekleme kazandırır."** Aynı argümanlarla tekrar çağrı oranı
ölçüldü: `guc_kazanci` **%15,2** · `_fir` **%17,6**. İş gerçekten yeni;
tam-doğru bir memo en fazla altıda bir kazandırır.

**(c) "Çekim başına marshalling pahalı."** Hızlı bir yol yazıldı — alan
kodlaması ve tohum paketlemesi önbelleğe alındı, sekiz `update` çağrısı
teke indi, `isinstance` dağıtımı atlandı. 🔒 **200 000 karşılaştırmada tek
bir bit farkı yok** (bütün alanlar, 1–4 anahtar). Ama kazanç **1,11 kat**.
Bileşenlere ayrıldığında sebep görüldü:

    paketleme 0,024 s · blake2b 0,131 s · Box-Muller 0,122 s   (300k çekim)

Maliyet marshalling'de değil, **kriptografik özetin ve Box-Muller'in
kendisinde**. 🔒 Belirlenimciliğin kalbindeki bir fonksiyona %11 için
dokunmak kötü bir takas — **uygulanmadı**.

## 3 · CUDA — ölçülmüş cevap: ana simülasyon için HAYIR

Öğrencinin sezgisi doğru yeri işaret etti (darboğaz gerçekten sayısal bir
iç döngü), ama üç ölçülebilir engel var:

1. **Tanecik boyutu.** `guc_kazanci` tek bir bağ ve tek bir an için
   çağrılıyor; çağrı başına iş ~2 µs. GPU'da bir çekirdek başlatmanın
   maliyeti tek başına bundan büyük. Kazanç için binlerce bağ-an'ı tek
   kernel'de toplamak gerekir — bu, zaman akışını değiştiren bir mimari
   değişiklik.
2. **Belirlenimcilik.** Proje tohum-tekrarlanabilirliğine dayanıyor
   (regresyon · korunum · 595 test). GPU'da kayan nokta indirgeme sırası
   garanti değildir; aynı tohum aynı sayıyı vermeyebilir. `rng.py` zaten
   Python'un kendi `hash()`ini bile bu yüzden reddediyor.
3. **Olay kuyruğu paralelleştirilemez.** Ve asıl paralellik ekseni zaten
   kullanılıyor: koşumlar arası, süreç havuzuyla.

⚠️ **Sayaç tabanlı bir üreteç (Philox) blake2b'den 13,8 kat hızlı ölçüldü**
ve belirlenimcidir — yani teknik seçenek GERÇEK. Ama her sönümleme
değerini değiştirir, dolayısıyla bugüne kadar ölçülmüş **her kalibre
sayıyı** (çalışma noktası, karıştırıcı gücü, çözünürlük, kâhin tavanları,
duyarlılık aklamaları) geçersiz kılar. Kaba hesap: kazanç ~1,7 kat, bedel
yeniden kalibrasyon + bütün regresyon tabanının yeniden kurulması. 🔒
**Alınmadı** — ama mühür öncesinde bir seçenek olarak burada duruyor ve
kararı öğrenciye aittir.

## 4 · Parça parça veri toplama — evet, ve KANITLANABİLİR biçimde güvenli

`12` §5 bunu zaten öğrencinin fikri olarak taşıyor. Buradaki ek şu: her
sonuç satırı `kurulum_hash` · `evren_hash` · `sayac_semasi_hash` taşıyor,
yani farklı günlerde alınmış parçaların **aynı koda ait olduğu sonradan
ispatlanabiliyor**. Kod arada değişmişse özet tutmaz ve birleştirme
reddedilir. "Kesintisiz koşmak" bir zorunluluk değil.

🔒 Ve "alınacak veriler önceden belirlensin" isteği zaten **mühürün
kendisidir**: birincil hücrenin seçimi `06` §9'un açık maddelerinden biri.

## 5 · 🟢 KAPANAN BORÇ — `KOSE_ONBELLEK_SINIRI` artık ölçülmüş

Kaydı şunu diyordu: *"saf memo olduğu için sonucu değiştiremez ama DEĞERİ
ölçülmedi — sönümleme önbelleğinin aksine birebir aynılık kanıtı yok."*

Ölçüt taramadan ÖNCE yazıldı: *sınır ne olursa olsun sonuç satırı VE ham
teslim imzası birebir aynı çıkmalı.* Hareketli kol, `bagimsiz-yok` 1000,
50 s:

| sınır | süre | teslim | satır + imza |
|---|---|---|---|
| 4 194 304 | 132,9 s | 1443 | taban |
| 524 288 *(varsayılan)* | 133,5 s | 1443 | **BİREBİR** |
| 16 384 | 135,0 s | 1443 | **BİREBİR** |
| 1 024 | 142,0 s | 1443 | **BİREBİR** |

**4 096 kat** aralıkta dördü de birebir. Bedel yalnız süre: en küçük
sınırda %7. 🟢 `SINANMAMIS` → `OLCULMUS`; borç **41 → 40**.
Üretici: `python -u kalibrasyon/sonumleme_onbellegi.py 4`.

## 6 · Asıl kaldıraç hız değil, BÜYÜKLÜK

Bugünkü ölçümün en önemli çıktısı bir hızlandırma değil, bir bütçe sayısı:
tam ölçekli **hareketli** bir koşum ~1 saat, statik ~5 dakika. Ana deney =
protokol × tohum × hücre. Hücre sayısı henüz seçilmedi (`06` §9 açık
maddesi) ve seçim doğrudan takvimi belirliyor:

    6 hücre  × 40 tohum × 4 protokol =   960 koşum ≈ 10 gün (4 işçi)
    24 hücre × 40 tohum × 4 protokol = 3 840 koşum ≈ 40 gün → SIĞMAZ

🔒 Yani 1,7 katlık bir hızlandırma yanlış hücre seçimini kurtarmaz, doğru
hücre seçimi ise hızlandırmaya ihtiyaç bırakmaz. **Mühürden önce yapılacak
en değerli iş, birincil hücreyi bu bütçeye göre seçmektir.**

## 7 · Ders

Bugün üç hız hipotezi kurdum, üçü de ölçümde çöktü — ve bir tanesi
(önbellek) tam tersi çıktı: suçlu sandığım bileşen zaten optimal
çalışıyordu. Hız sezgisi, fizik sezgisinden daha güvenilmez: `03` §2
ilke 8 *"beklenmeyen sonuçta önce sebep ölçülür"* der; bu kayıt onun hız
tarafındaki karşılığıdır. **Profilci olmadan tek satır eniyileme
yazılmamalı.**

---

# K-139 · 🔴 AODV'NİN ÖLÇÜM BEYANLARI YANLIŞ ANAHTARLANIYORDU — ve düzeltme ölçüm katmanında ikinci bir kusur açtı

> **Tarih:** 19 Eylül 2026 · **Bulan ve düzelten:** ajan (OLSR'ın beyanları
> tasarlanırken) · **Karar bekleyen:** öğrenci — §5
> **Üreticiler:** `tests2/test_aodv.py` (üç yeni kapı) · birebir imza
> karşılaştırması (aşağıda)

## 1 · Nasıl bulundu

OLSR'ın `kopma` ve `rota_kuruldu` beyanlarını tasarlarken, iki protokolün
Δ'yı AYNI anlamda ölçmesi için AODV'nin ne yaptığına bakıldı. Rota defteri
(`olcum/rota_olaylari.py`) anlamı açıkça yazıyor:

- `algilama_duyarliligi = kopma_algilanan / kopma_fiziksel` — payda fiziksel
  **BAĞ** kopmaları
- `rota_etkilendi` = *"kopma beyan edilen ayrı **BAĞ** sayısı"*
- Δ, aynı `(düğüm, komşu)` anahtarına düşen `kopma` ile ilk `rota_kuruldu`
  arasındaki süre

AODV ise `komsu` alanına iki farklı şey yazıyordu:

| beyan | nerede | `komsu` ne |
|---|---|---|
| `kopma` | yerel bağ koptu | kopan **komşu** ✓ |
| `kopma` | RERR alındı | her ulaşılamaz **HEDEF** ✗ |
| `rota_kuruldu` | RREP kaynağa ulaştı | rotanın **HEDEFİ** ✗ |

## 2 · Ölçüldü — önce

`bagimsiz-yok`, tohum 1000, 50 s:

| | değer |
|---|---|
| beyan edilen kopma | 3 441 |
| fiziksel (kâhin) kopma | 8 |
| **algılama duyarlılığı** | **430,1** *(0–1 olmalı)* |
| farklı kopma anahtarı / kurulum anahtarı / ortak | 789 / 9 / 6 |
| kapanmamış kopma | 785 |

`statik-yok`ta — topoloji hiç değişmezken — **1 082** kopma.

İki kaynak: (a) §6.9'un HELLO bastırması boştaki komşuları sürekli
tablodan düşürüyor ve her düşüş, **hiçbir rota etkilenmese bile**, kopma
beyan ediliyordu; (b) RERR'deki her uzak hedef kopma sayılıyordu.

## 3 · Düzeltme — RFC'nin kendi tanımı

RFC 3561 §6.11 bağ kopmasını *"etkin bir rotanın sonraki atlaması"* için
tanımlar. Üç kural:

1. `kopma(K)` yalnız K üzerinden **etkin rota geçen** bir bağ koptuğunda.
2. RERR bir kopma **değildir** — uzaktaki bir bağın haberidir.
3. `rota_kuruldu(K)` — K'nin kopmasının etkilediği hedeflerden birine rota
   yeniden kurulduğunda, **K anahtarıyla**. Rota kurulan üç yerin üçünde
   de (komşu rotası · ters rota · RREP ileri rotası).

🔒 **Davranış değişmedi — birebir kanıtlandı.** Beyan yalnız ölçüme gider;
yine de tahmin edilmedi, ölçüldü. Aynı iki koşu düzeltmeden önce ve sonra:

| | teslim imzası | korunum | PDR | kontrol çerçevesi |
|---|---|---|---|---|
| `statik-yok` | **BİREBİR** | **BİREBİR** | **BİREBİR** | **BİREBİR** |
| `bagimsiz-yok` | **BİREBİR** | **BİREBİR** | **BİREBİR** | **BİREBİR** |

Yani 19 Eylül'de koşan AODV kapanış ölçümünün U1 tablosu bu kod hâli için
de geçerlidir. Etiket: **`AODV-d`** = `AODV-c` + beyan anlamı.

## 4 · Sonra — ve düzeltmenin açığa çıkardığı şey

| `bagimsiz-yok` | önce | sonra |
|---|---|---|
| beyan edilen kopma | 3 441 | 2 565 |
| kapanan Δ | 198 | **2 207** |
| kapanmamış | 785 | 358 |
| **COR** | 0,25 | **3,26** |

🔴 **COR "kurtarılan / etkilenen" diye tanımlı ve 1'i AŞAMAZ.** Sebep ölçüm
katmanında: pay (`rota_kurtarildi = len(_delta)`) kopma→kurtarma
**döngülerini** sayıyor, payda (`rota_etkilendi`) **farklı bağları**. Aynı
bağ beş kez kopup beş kez kurtarılırsa 5/1 = 5. Düzeltmeden önce Δ neredeyse
hiç kapanmadığı için bu kusur görünmüyordu.

Aynı veriden, doğru birimle (döngü / döngü): statik **0,912** · hareketli
**0,860**.

## 5 · 🔴 Açık iki karar — `sim2/olcum/`, öğrenci onayı gerekir

| # | sorun | öneri | ne zaman |
|---|---|---|---|
| a | COR'un payı ve paydası farklı birim sayıyor | payda da **döngü** saysın: açılan bekleyen kayıt sayısı. Değişiklik tek bir özelliktir ve tanımın kendi cümlesini ("kurtarılan / etkilenen") gerçekleştirir | kapanış paketinin regresyonu bittikten SONRA (öncesinde `sim2/`ye dokunmak önceden yazılan beklentiyi kirletir) |
| b | `algilama_duyarliligi` bir **geri çağırma** ölçüsü diye tanımlı ama protokolün bütün beyanlarını sayıyor — yanlış pozitifler dâhil. Ayrıca paydasının grafiği, K-132'de ölçüldüğü gibi, kullanılan bağ grafiğinden ~3 kat seyrek | ikiye bölünsün: **geri çağırma** (fiziksel bir kopmayla eşleşen beyan / fiziksel kopma) ve **yanlış alarm oranı**. Eşleştirme için fiziksel kopmaların bağ ve zaman bilgisi gerekir — orta büyüklükte bir ölçüm katmanı değişikliği | mühürden önce; acil değil |

⚠️ (b)'nin bugünkü okuması şudur ve bir BULGU olarak saklanmalı: AODV,
fiziksel olarak 8 bağ koparken 2 565 kez "bağım koptu" diyor. Bunların
çoğu çarpışma kaynaklı MAC vazgeçmeleri ve boştaki rotaların zaman
aşımları. Literatürde bilinen bir AODV zaafı — **tıkanıklığı hareket
sanmak** — ve bu simülatör onu sayısal olarak gösteriyor.

## 6 · OLSR için sonuç

OLSR beyanlarını en baştan bu anlamla yazacak: `kopma(K)` K üzerinden rota
geçen simetrik bir bağ kaybedildiğinde (bekleme süresi ya da histerezis),
`rota_kuruldu(K)` o bağın etkilediği bir hedefe yeniden rota hesaplandığında.
İki protokolün Δ'sı böylece aynı şeyi ölçer.

## 7 · Ders

Bir ölçüm kusurunu düzeltmek, arkasında saklanan ikinci bir kusuru
açığa çıkarabilir. COR'un birim hatası ancak Δ gerçekten kapanmaya
başlayınca görünür oldu. **Düzeltilmiş bir sayının ilk işi, kendisinden
sonra gelen hesabı sınamaktır.**

---

# K-140 · 🟢 AODV KAPANDI — kapı yeni bir düşük hücreyi yakaladı, hüküm ölçülmüş tablodan yeniden üretildi

> **Tarih:** 19 Eylül 2026 · **Karar:** öğrenci (*"AODV'yi kapatalım"*) ·
> **Koşum ve kayıt:** ajan
> **Üreticiler:** `DEVIR.md` §2'nin kapanış paketi (dört adım, tek sefer) ·
> `python -u kalibrasyon/aodv_uygunluk.py hukum ciktilar2/aodv_uygunluk/u1_20260919_kapanis_tablodan.json`

## 1 · Kapanış paketi — dört adım

| # | adım | sonuç | süre |
|---|---|---|---|
| 1 | test takımı | **595 passed** | 8 dk 14 sn |
| 2 | U1 kapısı (24 koşum, 4 işçi) | U1-U **GEÇTİ** · U1-B 🔴 **KALDI** — §2 | **4 sa 9 dk** |
| 3 | regresyon üretimi `aodv_c` (4 işçi) | 44/44 geçerli | **30,9 dk** |
| 4 | `k135` ↔ `aodv_c` | yalnız dört köken kovası — **önceden yazılan beklentiyle BİREBİR** (§4) | < 1 dk |

⚠️ İki bant tahmini yine tutmadı ve ikisi de **iyi** yönde: regresyonu 4
işçiyle 50–75 dk tahmin etmiştim, **31 dk** sürdü; kapı 4 işçiyle 6 işçiden
yalnız **%4** yavaş (14 967 s ↔ 14 332 s). Yani makine çekirdek sayısıyla
değil başka bir şeyle (büyük olasılıkla bellek bant genişliğiyle) sınırlı ve
`03` §1'in 4 işçi kuralı neredeyse bedava.

## 2 · 🔴 Kapı tasarlandığı gibi çalıştı — yeni bir düşük hücre sessizce geçemedi

`formasyon-yok/1002`: AODV-a'da **0,613** (eşiğin 0,013 üstü), AODV-c'de
**0,572**. Kâhin aynı (0,8122), AODV 0,4979 → 0,4643. Hücre açıklanmış
listede olmadığı için kapı `🔴 ACIKLANMAMIS` bastı ve çıkış 1 verdi. K-137'nin
*"açıklanmadan geçilemez"* dişi ilk gerçek sınavında ısırdı.

**Hipotez ölçümden ÖNCE yazıldı ve ÇÜRÜDÜ.** Tahminim şuydu: AODV-a'nın
kusuru (veri akan komşuların sahte zaman aşımı) sık yeniden keşfe zorluyor
ve hareketli formasyonda **kazara periyodik bir rota tazelemesi** gibi
işliyordu. Ölçüldü — aynı hücre, kısa pencere, iki kod hâli:

| | AODV-a | AODV-d |
|---|---|---|
| keşif | 406 | 413 |
| RREQ | 907 | 909 |
| komşu zaman aşımı | 2 214 | 2 254 |
| MAC vazgeçmesi | 512 | 504 |
| PDR | 0,5344 | 0,5219 |

Mekanizma sayaçları neredeyse aynı. Kayma bir sistematik etki değil:
zamanlamayı birkaç milisaniye oynatan her kod değişikliği, deterministik bir
simülasyonda tek bir tohumu başka bir örneğe çevirir. Eşiğin 0,013 üstündeki
bir hücrenin öbür tarafa geçmesi bundan fazlasını söylemez.

Yapısal açıklama ise diğer üç hücreninkiyle AYNI: eşiksiz en kısa yolun
teslimi **0,2719** — kolunun en düşüğü (1000: 0,5466 · 1001: 0,3799). Hücre
bu ölçülmüş açıklamayla listeye eklendi.

## 3 · Hüküm, 4 saatlik koşum TEKRARLANMADAN yeniden üretildi

Liste değişince verdikti yeniden üretmenin tek yolu 4 saatlik koşumdu —
oysa simülasyon deterministik ve davranış AODV-c ↔ AODV-d birebir (K-139);
aynı tabloyu verirdi. Alete iki şey eklendi:

- **Tam koşum ölçtüğü hücreleri diske yazar** (`ciktilar2/aodv_uygunluk/`,
  `regresyon_satirlari.py` ile aynı gelenek).
- **`hukum` kipi** kayıtlı bir ölçüme BUGÜNKÜ hüküm kodunu uygular.
  🔒 İkinci bir hüküm gerçeklemesi YAZILMADI: tam koşum da `hukum` kipi de
  aynı `_degerlendir` fonksiyonundan geçer.

Bugünkü koşum bu özellikten ÖNCE yapıldığı için kaydı **yazdırılan
tablodan** kuruldu (4 basamak) ve kaynak alanı bunu açıkça söylüyor. Hiçbir
hücre eşiğe yuvarlamanın çevirebileceği kadar yakın değil.

**Sonuç: çıkış 0** — U1-U GEÇTİ · U1-B TEMİZ · 4 açıklanmış düşük hücre.

| kol | 1000 | 1001 | 1002 |
|---|---|---|---|
| statik | 0,996 | 0,982 | **0,897** 🟡 |
| bağımsız | 0,784 | 0,705 | **0,497** 🟡 |
| görev | 0,819 | **0,443** 🟡 | 0,612 |
| formasyon | 0,904 | 0,780 | **0,572** 🟡 |

*(AODV / ETX kâhini oranı, tam pencere · 🟡 = ölçülmüş açıklamasıyla bulgu)*

## 4 · Regresyon — önceden yazılan beklentiyle birebir

44 vakanın 44'ünde tek bir köken dağılımı ve tam olarak beklenen:
TURETILMIS 51 → **52** · OLCULMUS 18 → **19** · TEDAVI 17 → **23** ·
SINANMAMIS 41 → **40** · KAYNAK, DUYARSIZ, KOL_TANIMI aynı. Başka tek bir
alan değişmedi. Yeni taban **`aodv_c`**.

## 5 · İkinci bulgu — rota tamponu BOŞTA DEĞİL

| | değer |
|---|---|
| en yüksek doluluk | **64 / 64** — beş hareketli hücrede |
| süre tavanından düşen | toplam 81 paket |
| en kötü hücre | `gorev-yok/1001`: 30 335 giriş, 44 düşüş |

İki `SINANMAMIŞ` parametre (kapasite 64, ömür 30 s) **bağlıyor**. Etkilerinin
TEK YÖNLÜ bir üst sınırı var: sonsuz bir tampon en fazla düşürdüklerini
kurtarabilirdi — en kötü hücrede 44 / 12 799 ≈ **0,0034**, çözünürlüğün
(0,023) altında. Daha küçük bir tampon daha çok düşürebileceği için bu bir
aklama DEĞİLDİR; parametreler `SINANMAMIS`ta kalır, kanıt buraya yazılır.

## 6 · AODV'nin durumu

🟢 **AODV-d KABUL EDİLDİ** (`06` §4.4 madde 3, K-137'nin iki parçalı hâli):
uygunluk geçti, dört düşük hücre ölçülmüş açıklamalarıyla bulgu. Beş sapma
beyanlı (`aodv_bicim.py`). 

Açık kalan, AODV'nin değil ölçüm katmanının iki işi (K-139 §5): COR'un birim
düzeltmesi (öğrenci onayladı, sıradaki iş) ve `algilama_duyarliligi`nin
geri çağırma / yanlış alarm olarak bölünmesi (mühürden önce).

⏭️ **Sırada OLSR** — biçimleri ve algoritmaları birincil belgeden okundu
(`02` §R2.1), karar kuralı verildi (SHOULD uygulanır · MAY beyan edilir).

---

# K-141 · 🟢 COR ONARILDI — pay ve payda aynı birimi sayıyor, sayaç ikizi artık canlı

> **Tarih:** 19 Eylül 2026 · **Karar:** öğrenci (*"evet, kapanıştan
> sonra"* — K-139 §5a) · **Uygulama:** ajan
> **Üreticiler:** `tests2/test_olcum.py` (üç yeni kapı) ·
> `tests2/test_aodv.py::test_COR_SAYAC_IKIZI_ile_DEFTER_ayni_sayiyi_veriyor` ·
> `python -u kalibrasyon/regresyon_satirlari.py karsilastir aodv_c k141`

## 1 · İki kusur, aynı metrikte

**(a) Birim uyuşmazlığı.** Defterde pay (`rota_kurtarildi = len(_delta)`)
kopma→kurtarma **döngülerini**, payda (`rota_etkilendi`) **farklı bağları**
sayıyordu. Aynı bağ beş kez kopup beş kez kurtarılırsa 5/1 = 5. AODV'nin beyan
anahtarları düzelip Δ gerçekten kapanmaya başlayınca görünür oldu (K-139):
COR statikte **3,46**, hareketlide **3,26** — "kurtarılan / etkilenen" diye
tanımlı bir oran.

**(b) Ölü ikiz.** `rota_etkilendi` SAYACI tanımlıydı ama **hiçbir yerde
artırılmıyordu**. Sayaçtan türeyen `cor` ve onun analiz penceresindeki
ikizi `cor_pencere`, paydası hep sıfır olduğu için **her koşuda boştu**.
Pay tarafı (`rota_kurtarildi` sayacı) ise her `rota_kuruldu`yu sayıyordu —
bir Δ'yı kapatsın kapatmasın. Yani iki COR hesabı iki farklı tanımdı ve
biri hiç ateşlenmiyordu.

## 2 · Düzeltme — tanımın kendi cümlesi

| parça | önce | sonra |
|---|---|---|
| defter paydası | farklı bağ sayısı | **açılan döngü sayısı** |
| `beyan_isle` dönüşü | yok | `"acildi"` · `"kapandi"` · `None` |
| `rota_etkilendi` sayacı | hiç artmıyordu | döngü AÇILINCA artar |
| `rota_kurtarildi` sayacı | her `rota_kuruldu`da | döngü KAPANINCA artar |
| değişmez | yok | `kapanan + bekleyen == açılan` — `cor()` her çağrıda sınar |

İki COR hesabı artık aynı muhasebeden besleniyor; bir kapı bunu gerçek bir
AODV koşusunda sınıyor (`cor == cor_olcum`).

## 3 · Ölçülen

| `AODV-d`, 50 s | COR önce | COR sonra | teslim imzası | korunum |
|---|---|---|---|---|
| `statik-yok` | 3,457 | **0,912** | BİREBİR | BİREBİR |
| `bagimsiz-yok` | 3,255 | **0,860** | BİREBİR | BİREBİR |

Sonraki değerler K-139 §4'te düzeltmeden ÖNCE, aynı veriden elle
hesaplananla birebir aynı.

## 4 · Mevcut testler neden yakalamadı

Üç COR testi vardı ve hiçbiri yanlış tanımı KODLAMIYORDU — ama hiçbiri
*"aynı bağ iki kez kopar"* durumunu da sınamıyordu. Kusur tam o durumdaydı.
Testler değiştirilmedi; eksik durum eklendi.

## 5 · Regresyon

🔒 Beklenti karşılaştırmadan ÖNCE yazıldı: **44 vakanın hiçbirinde tek alan
değişmemeli** — hiçbir vaka beyan üreten bir protokol koşmuyor (mevcut
tabanda bütün COR alanları boş), sayaç şeması ve köken defteri değişmedi.

`python -u kalibrasyon/regresyon_satirlari.py karsilastir aodv_c k141` —
**🟢 BİREBİR, 44/44 bulgusuz**. Beklentiyle tam aynı. Üretim 33,6 dk
(4 işçi). Yeni taban **`k141`**.

Test takımı: **603 passed** (602 zincirde + ölü sayaç kapısı ayrıca).

## 6 · Ders — ve bu kez kapıya çevrildi

Sayacı TANIMLAYIP hiç ARTIRMAMAK bu depoda **üçüncü kez** yaşandı
(`kopma_fiziksel` 9 Eylül'e kadar hiç sayılmıyordu, `olcum/kopma.py`
başlığı). Kaydın ilk taslağı bunu *"dördüncüsü bulunursa kapıya
çevrilmeli"* diye bırakıyordu — tarama ucuz olduğu için bekletilmedi.

`tests2/test_cekirdek.py::test_her_ham_sayac_BIR_YERDE_ARTIRILIYOR`: her
ham sayacın adı `sim2/` içinde (kütük hariç) tırnaklı geçmeli; kontrol
düzlemi sayaçları için öneksiz ad da kabul edilir.

🔴 **İlk taraması 16 yanlış alarm verdi** — kontrol düzlemi sayaçları
`say("iletim")` diye önek eklenerek artırılıyor. Öneki hesaba katınca
bugün ölü sayaç **yok**. 🔒 Ve kapının ateş edebildiği gösterildi: düzeltme
öncesi hâl bellekte canlandırıldı, kapı **tam olarak `rota_etkilendi`yi**
yakaladı.

⚠️ Sınırı: ad bir belge dizesinde tırnaklı geçerse kandırılır. Yakaladığı
şey, yaşanan iki örneğin ortak hâlidir — adın HİÇ geçmemesi.

---

# K-142 · 🟢 OLSR YAZILDI — üç özet hatası, bir straw-man tuzağı, çürüyen iki hipotez

> **Tarih:** 19 Eylül 2026 · **Karar:** öğrenci (SHOULD uygulanır · MAY beyan
> edilir) · **Gerçekleme ve kayıt:** ajan
> **Üreticiler:** `tests2/test_olsr.py` (16 kapı) ·
> `python -u kalibrasyon/aodv_uygunluk.py --protokol olsr` (kapanış ölçümü —
> HENÜZ koşulmadı)

## 1 · Yazılan

| dosya | ne |
|---|---|
| `protokoller/olsr_bicim.py` | RFC 3626 §3.3 · §6.1 · §9.1 biçimleri ve §18 sabitleri — ham metinden. Vtime/Htime kodlayıcısı kesir aritmetiğiyle |
| `protokoller/olsr.py` | bağ algılama · histerezis · komşu ve 2-atlama kümeleri · MPR buluşsalı · MPR seçici kümesi · TC üretme/işleme/iletme · tekrar kümesi · yönlendirme tablosu · RFC'nin titreşim dağılımı |
| `tests2/test_olsr.py` | 16 kapı — biçim, RFC örnekleri, bağ algılama, histerezis, MPR, TC, rota tablosu, U1–U4, korunum |

`sim2/`de **hiçbir değişiklik** gerekmedi: kontrol düzlemi sözleşmesi OLSR'ı
zaten öngörmüş (tekrarlı alanlar bağımsız uzunlukta — HELLO'nun blok yapısı
bayt bayt oturuyor; belge örnek olarak doğrudan *"OLSR HELLO'nun komşu
listesi"*ni anıyor).

## 2 · Birincil belge — özetin üç hatası

Önce bir web getirme aracının özeti denendi. Üç hata taşıyordu; üçü de ham
metinle karşılaştırılınca yakalandı (`02` §R2.2): paket başlığı "16 bayt"
(4) · HELLO'nun Reserved alanı "13 bit" (16) · MAXJITTER "0,04 s"
(`HELLO_INTERVAL / 4` = 0,5 s). İlk ikisi iç tutarlılık sınavında bile
düşüyordu. Belgenin kendisi iki öz-sınama verdi: *"Packet Length < 16"*
kuralı (4 + 12) ve Vtime'ın dört çözülmüş örneği. İkisi de kapıya bağlı.

## 3 · Karar kuralı ve uygulandığı yerler

**Uygulanan SHOULD'lar:** bağ histerezisi (§14) · üretim ve iletme titreşimi
(§3.5) · ANSN'nin eklemede de artması (§9.2) · boş TC'nin `TOP_HOLD_TIME`
boyunca sürmesi ve bağ kaybına bağlı erken TC (§9.3).

**Beyan edilen MAY'ler:** bağ katmanı bildirimi (§13) · mesaj birleştirme ·
MPR buluşsalının 5. adımı · MPR değişince ek HELLO. Tablo ve yönleri
`olsr_bicim.py` başlığında.

## 4 · 🔴 RFC'nin titreşim dağılımı — basit yol %14 fark ederdi

§3.5: *"Actual message interval = MESSAGE_INTERVAL − jitter"* — titreşim
aralığı **kısaltır**. Sabit periyot + gecikme olarak yazılsaydı ortalama HELLO
aralığı 2,0 s kalırdı; RFC'ninki 1,75 s. OLSR'ın kontrol yükü %14 olduğundan
düşük ölçülürdü. Doğru dağılım sözleşmeyle birebir kuruldu:
`Uyandirma(ARALIK − MAXJITTER, jitter=MAXJITTER)` → `ARALIK − U(0, MAXJ)`.

## 5 · 🔴 Straw-man tuzağı: paket sıra numarası titreşimden ÖNCE veriliyordu

İlk koşu (14 düğüm, 30 s): ~900 paket gönderilmişken histerezis **2 563**
"kayıp" saydı, bağlar sahte kayıplarla "bekleyen"e düştü, PDR 0,577.

RFC'de paket sıra numarası paket **havaya çıkarken** verilir; titreşim
ondan önce uygulanır, dolayısıyla havada numaralar hep artan sırada gider.
Sözleşmede ise titreşim istek oluşturulduktan sonra uygulanıyor; numarası
önce verilen bir iletme, sonrakinin ardından çıkabiliyordu. Alıcı bu sıra
değişimini kayıp sanıyordu.

🔒 **Düzeltme parametresiz:** bir sıra boşluğu hemen kayıp sayılmaz, eksik
numara `MAXJITTER` kadar beklenir — titreşimin üst sınırı tam olarak budur ve
MAC kuyruğu FIFO'dur. RFC'nin kendi modelinde hiç sıra değişmediği için bu,
RFC'nin anlamını birebir geri kurar. Sahte kayıp 2 563 → 1 080.

## 6 · Çürüyen iki hipotez

**(a) "Düşük PDR'nin sebebi sahte kayıplar."** Sahte kayıp yarıya indi, PDR
kıpırdamadı (0,577 → 0,572) ve `hedef_yok` **tam aynı** kaldı (134).
Sebep yakınsamaydı: pencere uzadıkça PDR 0,572 → 0,715 → **0,788**,
`hedef_yok` ise mutlak olarak sabit (134 → 119 → 119) — rotasızlık
başlangıçta yığılıyor. Tam ölçekte 50 s'lik ısınma bu dönemi dışarıda bırakır.

**(b) "Beyan edilen §13 (MAY) OLSR'ı zayıflatıyor."** Kararlı durumda
kayıpların %12,6'sı MAC vazgeçmesiydi ve §13 tam bunu kullanırdı. Bir ölçüm
varyantıyla — protokole girmeden — ölçüldü, 14 düğüm, 120 s:

| | OLSR | OLSR + §13 |
|---|---|---|
| statik PDR | 0,7878 | **0,7754** |
| hareketli PDR | 0,5840 | **0,5189** |
| MAC vazgeçmesi (statik) | 194 | 98 |
| geçersiz rota (statik) | 13 | **128** |

§13 MAC kayıplarını yarıya indiriyor ama bağı 6 s "kayıp" işaretlediği için
o yöndeki hedefler **rotasız** kalıyor; OLSR'ın AODV gibi anında yeniden
keşfi yok. 🔒 **MAY kuralı OLSR'ı zayıflatmıyor — straw-man kaygısı yok.**
⚠️ Küçük dünya, tek tohum; yön göstergesi, tam ölçüm değil.

## 7 · 🔴 U3 — kapının gerekçesi çürüdü, ve AODV hakkında bir bulgu

OLSR'ın U3 kapısı ölçüt olarak **[1,7 ; 2,3]** aldı (120 s'lik koşunun
kontrol çerçevesi 60 s'likin kaç katı) ve **2,200** ile geçti: HELLO 2,02,
TC 2,26. Ama kapının belgesine *"reaktif bir protokolün oranı belirgin
biçimde 2'nin altına düşerdi"* diye yazmıştım. **Ölçüldü, düşmüyor:**

| AODV | 60 s | 120 s |
|---|---|---|
| RREQ · RREP · RERR | 1 026 · 690 · 409 | 1 918 · 1 253 · 769 |
| oran | | **1,854** |

Statik ağda bile AODV'nin keşfi susmuyor: boştaki komşuların zaman aşımı
(§6.9'un HELLO bastırması) ve MAC vazgeçmeleri sürekli RERR → yeniden keşif
üretiyor. RFC'ye uygun davranış — ama `06` §4.3'ün *"AODV yükü yalnız keşif
anında"* beklentisi bu dünyada **TUTMUYOR**.

🔴 **Ve AODV'nin U3 kapısı bunu hiç görmemişti, çünkü ZAYIFTI:**
`test_U3_kontrol_yuku_KESIFTE_yogunlasiyor` içinde `hello` değişkenine
yine RREP sayısı yazılmış ve iddia `kesif > 0 and hello > 0` — pratikte
ateş edemeyen bir kapı. İkinci U3 kapısı (*"keşif susuyor"*) yalnız koşunun
SON ANINDA süren keşif olup olmadığına bakıyor; keşfin sürekli yeniden
başlamasını görmüyor. Karar öğrenciye (§9).

## 8 · Kapılar — 16/16

biçim · Vtime örnekleri · bağ algılama · histerezis (iki kayıp bağı koparır ·
sıra değişimi kayıp değil) · MPR (tek erişen seçilir) · TC (yalnız MPR seçicisi
varken · boş TC sürer · ANSN) · TC iletme (yalnız MPR seçicisinden · tekrar
bastırılır · simetrik olmayandan işlenmez) · rota tablosu (h = 2'den
topoloji) · U2 (tablo güncellenir · kopma/kurtarma aynı anahtarda, Δ kapanır)
· U4 (RFC titreşim dağılımı) · U3 (doğrusal yük) · U1 yapı (çok atlamalı,
defter kapalı, kâhin aşılmıyor) · korunum hareketli kolda.

🔒 U2 kapısının ilk kurulumu bir bitiş süresini hesaptan SONRA elle
değiştiriyordu ve protokolün "değişti" bayrağını gerçek akışta hiç olmayan
bir yolla atlıyordu. İddia değişmeden kurulum güçlendirildi: bitiş baştan
kısa kurulur ve zamanın geçmesi beklenir — böylece **tembel süzme** de
sınanıyor.

## 9 · Açık

- ⏭️ **OLSR kapanış ölçümü** (`--protokol olsr`, 24 koşum, ~4 saat) —
  öğrencinin zamanlamasına bağlı.
- 🔴 **AODV U3** — beklenti tutmuyor ve kapı zayıftı. Seçenek: U1'deki A
  kararına benzer biçimde bulgu olarak raporlamak ve zayıf kapıyı ölçüye
  dayalı bir kapıyla değiştirmek. Öğrenci kararı.
- U1 aleti artık bütün taban protokollerin (`--protokol`); açıklanmış hücre
  listesi protokol başına. Dosya adı tarihsel.

---

# K-143 · 🔴 AODV YENİDEN AÇILDI — RERR öncül kuralı uygulanmamıştı; AODV'yi hem pahalı hem kötü gösteriyordu

> **Tarih:** 19 Eylül 2026 · **Bulan ve düzelten:** ajan (OLSR'ın U3
> ölçümünde AODV'nin karşılaştırma değeri incelenirken) · **Karar
> bekleyen:** öğrenci — §6
> **Üreticiler:** `tests2/test_aodv.py::test_RERR_ONCULU_OLMAYAN_hedef_icin_GONDERILMEZ`
> · önce/sonra imza karşılaştırması (aşağıda)

## 1 · Nasıl bulundu

K-142'de OLSR'ın U3 kapısının gerekçesi çürüdü: AODV'nin kontrol yükü de
süreyle neredeyse doğrusal büyüyordu (oran 1,854) — statik bir ağda keşif
susmuyordu. Bunu bir "AODV özelliği" diye kaydetmeden önce sürekliliğin
kaynağı sorgulandı: statik ağda bol RERR vardı (120 s'de 769).

## 2 · Birincil belge — RFC 3561 §6.11

> *"The RERR should contain those destinations that are part of the created
> list of unreachable destinations **and have a non-empty precursor
> list.**"*
>
> *"The neighboring node(s) that should receive the RERR are all those that
> belong to a precursor list of at least one of the unreachable
> destination(s) in the newly created RERR."*

Öncülü olmayan bir hedef için RERR **gönderilmez**. Bizim AODV'de öncül
listeleri tutuluyordu (RREP iletilirken kaydediliyor) ama RERR üreten
fonksiyon onları **kullanmıyordu**: etkilenen rota varsa her zaman yayın.

⚠️ `aodv_bicim.py`nin beyanlı sapması başka bir şeydi — *"tek öncül varsa
unicast yerine yayın"*. *"Öncül yoksa gönderme"* kuralı ne uygulanmış ne
beyan edilmişti.

## 3 · Düzeltme

`_rerr_kur` hedefleri öncülü olanlara süzer; hiçbiri kalmazsa RERR yok. 🔒
Süzme **hız sınırından önce**: öncülsüz bir aday `RERR_RATELIMIT`
penceresinden boşuna hak tüketmez. Yeni sayaç `rerr_onculsuz`.

⚠️ **Üç test eski davranışı kodluyordu** — RERR bekleyip kurulumlarında
öncül YOKTU. Senaryoları "başkalarının kullandığı bir rota"ydı ama kurulum
bunu söylemiyordu. İddialar AYNEN korundu, kurulumlara öncül açıkça
eklendi (K-135'in ayrımı: sınav düzeneğini sözleşmeye uydurmak meşrudur,
iddiayı sonuca uydurmak değil). RFC kuralının kendisi için yeni bir kapı.

## 4 · Tahmin ölçümden ÖNCE yazıldı — yarısı çöktü

*"Statik ağda RERR sert düşecek, yeniden keşif azalacak, U3 oranı 1,854'ün
belirgin biçimde altına inecek; PDR düşmeyecek."*

| 14 düğüm, statik | önce | sonra | tahmin |
|---|---|---|---|
| RERR (60 / 120 s) | 409 / 769 | **41 / 112** | ✓ |
| RREQ (60 / 120 s) | 1 026 / 1 918 | 1 094 / 2 213 | ✗ düşmedi |
| **U3 oranı** | 1,854 | **2,070** | ✗ yükseldi |
| bastırılan öncülsüz aday (120 s) | — | 853 | — |

RERR kuralı çalışıyor, ama keşif susmuyor — saniyede ~1,8 yeni keşif, sabit
hızda. Sürekliliğin asıl kaynağı RERR değil **MAC vazgeçmeleri**: kayıplı
kablosuz bir ağda sürekli trafik altında bağlar çarpışma ve sönümlemeyle
düşüyor ve AODV her seferinde yeniden keşfediyor. RFC'ye uygun davranış.

🔒 **Sonuç:** `06` §4.3'ün *"AODV yükü yalnız keşif anında"* beklentisi bu
dünyada tutmuyor — ve artık bir kusurla karışmamış hâliyle.

## 5 · Tam ölçekte etkisi — büyük

`AODV-d` ↔ `AODV-e`, 40 düğüm, 50 s:

| | PDR | kontrol çerçevesi |
|---|---|---|
| `statik-yok` | 0,9925 → **0,9981** | 5 582 → 4 789 (**−%14**) |
| `bagimsiz-yok` | 0,7328 → **0,7960** | 16 865 → 11 911 (**−%29**) |

Eksik kural AODV'yi hem **pahalı** hem **kötü** gösteriyordu — tersinden
bir straw-man. `nrl_*` karşılaştırmasında AODV'nin aleyhine bir sapmaydı.

🔴 **AODV'nin kapanışı (K-140) bu yüzden GEÇERSİZ.** U1 tablosu `AODV-c`
hâline aitti ve davranış değişti. Etiket: **`AODV-e`** = `AODV-d` + RFC
§6.11 öncül kuralı. Kapanış ölçümü yeniden koşulmalı. Açıklanmış hücrelerden
bazıları artık düşük olmayabilir — kapı onları **ölü kayıt** olarak
yakalayacak, tasarlandığı gibi.

## 6 · Açık iki karar

| # | konu | seçenekler |
|---|---|---|
| a | AODV + OLSR kapanış ölçümü (48 koşum, ~8 saat, 4 işçi) | öğrencinin zamanlaması |
| b | AODV'nin U3'ü: beklenti tutmuyor ve eski kapı zayıftı (`hello` değişkenine RREP sayısı yazılmış, iddia pratikte ateş edemiyordu) | U1'deki A kararına benzer biçimde: zayıf kapı kaldırılır, yerine ölçüme dayalı bir kapı (keşif tamamlanıyor · takılı keşif yok · yük ölçülüp bulgu olarak basılıyor) konur; beklenti "tutmadı" diye raporlanır |

## 7 · Ders

AODV'yi iki kez kapattığımı sandım. İkisinde de kapanıştan sonra bir RFC
maddesinin **yarım** uygulandığı çıktı (§6.9, şimdi §6.11). Ortak nokta:
ikisi de ancak başka bir protokolün ölçümüyle **karşılaştırılınca**
görüldü. Tek başına ölçülen bir protokol kendi kusurunu gizleyebilir;
iki protokolü aynı ölçüyle yan yana koymak, birinin sapmasını öbürünün
aynasında gösteriyor.

---

# K-144 · 🟢 AODV'NİN U3'Ü BULGU OLARAK RAPORLANDI — zayıf kapı ateş edebilen bir kapıyla değişti

> **Tarih:** 19 Eylül 2026 · **Karar:** öğrenci (*"bulgu olarak raporla"*) ·
> **Uygulama:** ajan
> **Üreticiler:** `python -u kalibrasyon/aodv_uygunluk.py u3` ·
> `tests2/test_aodv.py::test_U3_BULGU_onculsuz_RERR_GERCEK_kosuda_bastiriliyor`

## 1 · Karar

`06` §4.3'ün *"AODV yükü yalnız keşif anında"* beklentisi TUTMADI ve bu,
U1'deki A kararına benzer biçimde **bulgu olarak** raporlanır. Beklenti
literatürden gelen idealleştirilmiş bir tablo; kayıplı ve yüklü bir taktik
ağda tepkisel ailenin *"rotayı bulunca susar"* avantajı büyük ölçüde
kayboluyor. `06` §4.3'e yazıldı; H1.1 için bir bulgu.

## 2 · Üretici — sayılar artık bir komuttan

K-142 ve K-143'teki oranlar geçici betiklerle ölçülmüştü; projenin
*"raporlanan her sayının yanında onu üreten komut"* kuralına aykırıydı. U1
aletine bir `u3` kipi eklendi: iki protokolü aynı küçük dünyada 60 s ve
120 s koşar, oranı basar. Çıkış 0 — bir ÖLÇÜMDÜR, kapı değil.

| küçük dünya, statik | 60 s | 120 s | oran |
|---|---|---|---|
| AODV | RREQ 1 094 · RREP 697 · RERR 41 | RREQ 2 213 · RREP 1 468 · RERR 112 | **2,070** |
| OLSR | HELLO 470 · TC 1 547 | HELLO 949 · TC 3 489 | **2,200** |

Komut, K-143'te kaydedilen sayıları **birebir** yeniden üretti. K-142'deki
**1,854** yeniden üretilemez ve bu doğrudur: `AODV-d`nin (öncül kuralı
öncesi) sayısıdır, kod o hâlde değil.

## 3 · Kapı değişimi

Eski `test_U3_kontrol_yuku_KESIFTE_yogunlasiyor` hiç ateş edemiyordu
(`hello` değişkenine RREP sayısı, iddia `kesif > 0 and hello > 0`). Yerine
`test_U3_BULGU_onculsuz_RERR_GERCEK_kosuda_bastiriliyor`: bulunan kusurun
SINIFINI — RFC'nin istemediği kontrol trafiği — gerçek bir koşuda sınar.
§6.11 süzgeci kaldırılırsa `rerr_onculsuz` sıfır kalır ve kapı yanar.
İkinci U3 kapısı (*"keşif tamamlanıyor, takılı keşif yok"*) değişmedi.

## 4 · 🔒 Bir sonraki regresyonun beklenen farkı — ÖNCEDEN

Köken defterine bir girdi eklendi (`U3_SURELERI_S`, TEDAVI). `k141` ile
bir sonraki karşılaştırmada 44 vakada YALNIZ `teshis.koken_kovalari.TEDAVI`
**23 → 24** değişmeli; başka hiçbir alan.

---

# K-145 · 🟢 AODV YENİDEN KAPANDI (`AODV-e`) — kapı iki ölü açıklama yakaladı ve biri benim kusurumu örtüyordu

> **Tarih:** 19 Eylül 2026 · **Karar:** öğrenci (*"aodvyi kapatalım, devam
> edelim"* · sıra: *"ilk önce aodv bitsin sonradan olsryi koşacağız"*) ·
> **Uygulama:** ajan
> **Üreticiler:** `python -m pytest tests2 -q` ·
> `python -u kalibrasyon/aodv_uygunluk.py` ·
> `python -u kalibrasyon/aodv_uygunluk.py hukum ciktilar2/aodv_uygunluk/aodv_son.json` ·
> `python -u kalibrasyon/regresyon_satirlari.py uret k144` ·
> `python -u kalibrasyon/regresyon_satirlari.py karsilastir k141 k144`

## 1 · Kapanış paketi — tek seferde, `AODV-e` hâli

| adım | sonuç | süre |
|---|---|---|
| test takımı | **`620 passed`** | 533 s |
| U1 kapısı (24 koşum, 4 işçi) | U1-U 🟢 · U1-B 🔴 — **yalnız iki ÖLÜ açıklama yüzünden** (§3) | 15 021 s ≈ 4 sa 10 dk |
| regresyon üretimi `k144` | 44/44 geçerli | 38,2 dk |
| `k141` ↔ `k144` | yalnız `teshis.koken_kovalari.TEDAVI` **23 → 24** | < 1 dk |

Regresyon farkı K-144 §4'te karşılaştırmadan ÖNCE yazılan beklentiyle
**birebir**; başka hiçbir alan değişmedi. Karşılaştırma aletinin çıkışı 1'dir,
çünkü köken kovaları aletin izinli farklar listesinde yok — beklenti alette
değil, K-144 §4'te yazılıydı.

## 2 · U1 — `AODV-c` ↔ `AODV-e`

| kol | tohum | `AODV-c` (K-140) | **`AODV-e`** | eşik |
|---|---|---|---|---|
| `statik-yok` | 1000 | 0,996 | 0,995 | 0,90 |
| | 1001 | 0,982 | 0,999 | |
| | 1002 | **0,897** | 0,932 | |
| `bagimsiz-yok` | 1000 | 0,784 | 0,805 | 0,60 |
| | 1001 | 0,705 | 0,715 | |
| | 1002 | **0,497** | **0,549** | |
| `gorev-yok` | 1000 | 0,819 | 0,830 | 0,60 |
| | 1001 | **0,443** | **0,462** | |
| | 1002 | 0,612 | 0,636 | |
| `formasyon-yok` | 1000 | 0,904 | 0,931 | 0,60 |
| | 1001 | 0,780 | 0,811 | |
| | 1002 | **0,572** | 0,646 | |
| kol ortalaması | | 0,958 · 0,662 · 0,625 · 0,752 | **0,975 · 0,690 · 0,643 · 0,796** | |

Kalın = eşiğin altında. 12 hücrenin **11'i yükseldi**; tek düşen
`statik-yok/1000` (−0,001). K-143 §5'in 50 s'lik ölçümündeki yön (PDR
yükselir) tam pencerede de tuttu. ETX kâhininin 12 değeri iki kayıtta
**birebir** aynı — kâhin AODV'den bağımsız, beklenen buydu.

Eski tablonun üreticisi:
`python -u kalibrasyon/aodv_uygunluk.py hukum ciktilar2/aodv_uygunluk/u1_20260919_kapanis_tablodan.json`.
⚠️ Bugün **çıkış 1** verir ve bu doğrudur: açıklama listesi artık `AODV-e`ye
aittir, `AODV-c`nin iki düşük hücresi onda yok.

## 3 · Kapı iki ölü açıklamayı yakaladı — tasarlandığı gibi

`statik-yok/1002` (0,932 ≥ 0,90) ve `formasyon-yok/1002` (0,646 ≥ 0,60) artık
düşük değil. Açıklamaları kapıyı `OLU ACIKLAMA` diye kırmızı yaktı — K-137'nin
iki yönlü denetimi ilk kez bu yönden ateş etti. İki kayıt silindi; silinme
gerekçesi ve eski/yeni oranlar `aodv_uygunluk.py`de listenin başında yazılı.

Hüküm 4 saatlik koşum tekrarlanmadan `hukum` kipiyle yeniden üretildi:
**U1-U GEÇTİ · U1-B TEMİZ · çıkış 0** · açıklanmış düşük hücre **2**
(`bagimsiz-yok/1002` · `gorev-yok/1001`) — bulgu olarak raporlanır.

## 4 · 🔴 Bir düzeltme — `statik-yok/1002`

17 Eylül'de öğrenci şunu söyledi: bu hücre AODV'nin çalışma ilkesinin zayıf
noktasını gösteriyorsa değerli bir bulgudur, bir yazılım probleminden
geliyorsa düzeltilmelidir. K-137 §4 ölçtü ve **"yazılım kusuru değil"** dedi
(`12` §4 madde 3).

Bu cevap **yarı yarıya yanlıştı.** Ölçülen yapı doğru ve hâlâ geçerli: hücre
statik kolun hâlâ **en düşüğü** (0,932 ↔ 0,995 · 0,999) ve dört kolun
dördünde de en zayıf eşiksiz yola sahip hücre, en düşük U1 oranına sahip —
sıralama değişmedi. Ama hücrenin **eşiğin altında** kalması o yapıyla §6.11
kusurunun birleşimiydi; kusur gidince hücre geçti.

🔒 **Ders:** ölçülmüş açıklama bir hücrenin neden **en düşük** olduğunu
gösterdi, neden **eşiğin altında** olduğunu değil. Sıralamayı açıklayan bir
mekanizma, seviyeyi kaydıran bir kusurla yan yana yaşayabilir. Kalan iki
açıklama da aynı türden — sıralama açıklaması. Bugünkü bilgiyle doğrular,
ama *"bu hücrede kusur yok"* demenin kanıtı DEĞİLLER; yalnız *"bilinen
kusurlar düzeltildikten sonra hücre hâlâ düşük"* demenin kanıtıdırlar.

⏭️ **Bir ayna var:** OLSR kapanış ölçümü aynı 12 hücreyi aynı kâhinle
ölçecek. İki protokol aynı hücrede birlikte düşükse zorluk topolojidedir;
yalnız biri düşükse o protokole özgüdür — mekanizma ya da kusur. K-143 §7'nin
dersi (bir protokolün sapması öbürünün aynasında görünür) burada önceden
uygulanıyor. Bu bir tahmin değil, planlı bir karşılaştırmadır; sonucu
ölçülmeden yorumlanmayacak.

## 5 · Rota tamponu

Tepe **64/64** dört hücrede (`bagimsiz-yok/1001` · `gorev-yok/1001` ·
`formasyon-yok/1001` · `formasyon-yok/1002`) · süre tavanından düşen **89**.
Kapasite ve ömür hâlâ `SINANMAMIŞ` ve bağlayıcı — bilinen borç, kapanış onu
değiştirmedi.

## 6 · Durum

- 🟢 **`AODV-e` KAPANDI.** K-140'ın kapanışı K-143'te geçersiz olmuştu; o
  kayıt revize haritasına **K-140 → K-145** olarak girdi (silinmedi).
- Regresyon tabanı artık **`k144`**. Yapısal denetim: ihlal yok · **169**
  parametre · TEDAVI **24** · SINANMAMIŞ **40** · **121** modül
  (`python kalibrasyon/mimari_denetimi.py`).
- ⏭️ Sırada OLSR kapanış ölçümü (`--protokol olsr`, 24 koşum) — öğrencinin
  zamanlamasına bağlı. Ardından AOMDV; yazılmadan önce boşluk kararı
  (`02` §R4.1: a · b · c).

---

# K-146 · 🟡 OLSR KAPANIŞ ÖLÇÜMÜ — hareketlide AODV'den iyi, statikte iki hücre düşük; sebep ÖLÇÜLDÜ: beyanlı §13 sapması

> **Tarih:** 21–22 Eylül 2026 · **Koşum:** öğrenci (*"devam edebiliriz"*, 8
> çekirdek) · **Teşhis:** ajan · **Karar bekleyen:** öğrenci — §5
> **Üreticiler:** `python -u kalibrasyon/aodv_uygunluk.py --protokol olsr`
> (kayıt `ciktilar2/aodv_uygunluk/olsr_20260921_223536.json`; hüküm:
> `… aodv_uygunluk.py hukum ciktilar2/aodv_uygunluk/olsr_20260921_223536.json`) ·
> teşhis: `arsiv/teshis/olsr_statik_2026-09-22/` (ön-kayıt, üç betik, sonuçlar)

## 1 · Kapanış ölçümü

24 koşum, **8 işçi**, 11 117 s ≈ 3 sa 5 dk (bant 2,5–4,5 sa). U1-U **GEÇTİ** ·
U1-B **KALDI** — iki açıklanmamış düşük hücre, ikisi de statik.

| kol | tohum | `AODV-e` | **OLSR** | eşik |
|---|---|---|---|---|
| `statik-yok` | 1000 | 0,995 | 0,926 | 0,90 |
| | 1001 | 0,999 | **0,859** | |
| | 1002 | 0,932 | **0,866** | |
| `bagimsiz-yok` | 1000 | 0,805 | 0,912 | 0,60 |
| | 1001 | 0,715 | 0,912 | |
| | 1002 | **0,549** | 0,836 | |
| `gorev-yok` | 1000 | 0,830 | 0,934 | 0,60 |
| | 1001 | **0,462** | 0,751 | |
| | 1002 | 0,636 | 0,870 | |
| `formasyon-yok` | 1000 | 0,931 | 0,972 | 0,60 |
| | 1001 | 0,811 | 0,944 | |
| | 1002 | 0,646 | 0,867 | |
| kol ortalaması | | 0,975 · 0,690 · 0,643 · 0,796 | 0,884 · 0,887 · 0,851 · 0,928 | |

Kalın = eşiğin altında. OLSR hiç tamponlamıyor (proaktif, tasarım gereği).
⚠️ Bunlar bir **kabul kapısının** sayılarıdır, ana deneyin karşılaştırması
değil (`06` §4.4 madde 3) — tek pencere, üç geliştirme tohumu, karıştırıcısız.

## 2 · Ayna — K-145 §4'te önceden planlanan karşılaştırma

- AODV'nin iki düşük hücresi OLSR'da rahat geçiyor (0,836 · 0,751) → o
  zayıflık **AODV'ye özgü**, topolojinin değil.
- Ters yönde: OLSR'ın iki düşük hücresi AODV'de geçiyor (0,999 · 0,932) →
  **OLSR'a özgü**.
- AODV'nin yapısal açıklaması (eşiksiz en kısa yol; 1002 en zayıf) OLSR'ın
  sıralamasını açıklamıyor — OLSR'da en düşük hücre 1001. Açıklama
  taşınamazdı; ayrı teşhis gerekti.

## 3 · Teşhis — hipotezler ölçümden ÖNCE yazıldı

Protokolü yalnız SAYAN bir alt sınıfla koşuldu; beş koşunun PDR'si U1
kaydıyla **birebir** (sarmalayıcı davranışı değiştirmedi).

| # | hipotez | sonuç |
|---|---|---|
| H2 | rota tablosu boşluğu | ❌ `hedef_yok`un TAMAMI ısınmada (280 · 311 · 321), pencerede 0 |
| H3 | döngü | ❌ `ttl` 3–12 |
| H4 | kuyruk taşması | ❌ 0 |
| K1 | **bayat rota** (kusur adayı): seçilen sonraki atlama o anda simetrik mi | ❌ ihlal **0** — üç tohum, 71 572 karar |
| H1 | gri bölge — GÜÇLÜ biçim: kontrol ≥ 0,80 ve atlama < 0,90 | 🔴 **ÇÜRÜDÜ: %0.** Başarısız bağlarda kontrol çerçevesinin tek seferde geçme olasılığı 0,57–0,76. Tanım sonradan değiştirilmedi |

Kaybın ~%80'i `iletim_basarisiz` ve BİRKAÇ bağda yoğun. Görülen mekanizma:

- Bu bağlarda kısa kontrol çerçevesi, veri + onay çiftinden 3–5 kat sık
  geçiyor (örn. 1001'de `33→34`: kontrol 0,57 · veri 0,09).
- RFC histerezisi (`HYST_SCALING` 0,5 · eşikler 0,8 / 0,3) son birkaç pakete
  bakar: üç ardışık başarı bağı açar, iki ardışık kayıp kapatır. Kontrol
  başarısı 0,57 · 0,63 · 0,70 · 0,76 olan bir bağ zamanın **%53 · %64 · %77 ·
  %86**'sında açık sayılır (RFC sabitleriyle Markov hesabı).
- Atlama sayısıyla yönlendirme bağ açıkken onu tercih eder; verinin 5
  denemeyle teslimi o bağlarda 0,38–0,73.
- AODV aynı dünyada o bağları kullanmıyor: `33→34` OLSR'da 484 kez kullanıldı
  ve 297 kez başarısız oldu; AODV'de **1** kez. AODV'nin farkı bağ katmanı
  bildirimi — başarısızlıkta rotayı bırakıp yeniden keşfediyor.

## 4 · Nedensel sınama — RFC 3626 §13 HARFİYEN

§13 (MAY, `olsr_bicim.py`de beyanlı sapma): bağ katmanı *"koptu"* deyince
`L_LOST_LINK_time = L_time = şimdi + NEIGHB_HOLD_TIME`, §8.5 kaybı. Yalnız
teşhis alt sınıfında; repodaki OLSR değişmedi. Öngörü YAZILMADI (§13
histerezisle birlikte yaşar ve etkisi kısa sürebilirdi).

| tohum | PDR önce → §13 | kâhine oran | veri başarısızlığı | kontrol çerçevesi |
|---|---|---|---|---|
| 1000 | 0,9257 → 0,9434 | 0,926 → **0,943** | 714 → 435 | +%3,1 |
| 1001 | 0,8589 → 0,9263 | 0,859 → **0,926** | 1 594 → 664 | +%3,6 |
| 1002 | 0,8630 → 0,9048 | 0,866 → **0,908** | 1 518 → 943 | +%3,9 |

🔒 **Sonuç:** statik kolun iki düşük hücresi büyük ölçüde **beyanlı §13
sapmasından** geliyor — sapma kaldırılınca üç hücre de eşiği geçiyor.
Bedeli küçük: `ttl` düşmesi 10 → 47 · 3 → 8 · 12 → 32 (topoloji daha hızlı
değiştiği için geçici döngüler).

🔒 K-145'in dersi uygulandı: açıklama bu kez bir SIRALAMA değil, NEDENSEL —
sapma kaldırılınca hücre geçiyor; kusur dışlama da ayrıca yapıldı (K1).

## 5 · 🔴 Açık karar — öğrenci

| # | seçenek | bedeli |
|---|---|---|
| A | Kural yerinde (*"MAY beyan edilir"*). İki hücre açıklanmış düşük olarak OLSR listesine girer; açıklama §4'ün nedensel ölçümü | OLSR, bağ katmanı bilgisini kullanan tabanlarla o bilgiden yoksun karşılaştırılır; statik kolda aleyhine ölçülmüş bir sapma raporla birlikte taşınır |
| B | §13 uygulanır — öğrencinin kuralına ölçülmüş gerekçeli TEK istisna | OLSR kapanış ölçümü yeniden (~3 sa, 8 işçi) + §13 kapısı; hareketli kollardaki etkisi ölçülmedi |

Ajanın önerisi: **B.**
1. AODV bağ katmanı bildirimini RFC 3561'in çekirdeği olarak kullanıyor,
   AOMDV makalesi de kullandığını söylüyor (§4.1, `02` §R4). Simülatör bu
   bilgiyi her protokole aynı kancayla veriyor; §13'süz OLSR, bilgi yüzeyi
   daha dar TEK taban olur.
2. §13 RFC metninin kendisi; yeni parametre getirmiyor.
3. `03` kural 4 (*taban çizgisi kurulum yüzünden zayıflatılamaz*) ve aynı
   sınıfın iki önceki örneği (K-101 · `02` §R3): isteğe bağlı bir özelliğin
   yokluğuyla zayıflatılmış bir taban, özgün protokolün üstünlüğünü şişirir.

---

# K-147 · 🟢 OLSR KAPANDI (§13 ile) — statik öngörü BİREBİR tuttu; hareketli kolda öngörülmeyen bir bedel

> **Tarih:** 22 Eylül 2026 · **Karar:** öğrenci (§13 uygulansın — K-146 §5,
> seçenek B) · **Uygulama:** ajan
> **Üreticiler:** `python -m pytest tests2 -q` ·
> `python -u kalibrasyon/aodv_uygunluk.py --protokol olsr` (kayıt
> `ciktilar2/aodv_uygunluk/olsr_20260922_073356.json`) ·
> `… aodv_uygunluk.py hukum ciktilar2/aodv_uygunluk/olsr_20260922_073356.json` ·
> `python -u kalibrasyon/aodv_uygunluk.py u3`

## 1 · Uygulama

- `OLSR.iletim_basarisiz` RFC 3626 §13'ün (2). maddesini harfiyen uygular:
  `L_LOST_LINK_time = L_time = şimdi + NEIGHB_HOLD_TIME`. (1) LOST_LINK ilanı
  ve simetri dışı bırakma ile (3) §8.5 kaybı mevcut kod yollarında — §14 için
  zaten yazılıydı. Yeni sayaç `bag_katmani_kopma`.
- Kapı: `test_S13_bag_katmani_KOPTU_deyince_LOST_LINK_ve_KOPMA_histerezis_geri_acar`
  — üç madde ve §14.3 ile birlikte yaşama (kalitesi eşiği aşan bir sonraki
  paket bağı geri açar). Eski `return ()` geri gelirse yanar.
- `olsr_bicim.py` sapma tablosundan §13 satırı çıktı; yerine *"tek istisna"*
  notu, gerekçesi ve ölçümüyle.
- Kod hâli etiketleri: **`OLSR-a`** (K-142, §13 yok) · **`OLSR-b`** (K-147, §13).

## 2 · Kapanış paketi — beklenti ÖNCEDEN yazıldı (`DEVIR.md` §2, 22 Eylül)

| adım | önceden yazılan | sonuç |
|---|---|---|
| test takımı | `621 passed` | ✅ **621 passed** (535 s) |
| statik üç hücre | teşhisin §13 koşularıyla BİREBİR: 0,9434 · 0,9263 · 0,9048 | ✅ **BİREBİR** — üç tohumda son basamağa kadar (`0.9434330807094304` · `0.926322368935073` · `0.9047581842331432`) |
| hareketli dokuz hücre | tahmin yok | §3 |
| U3 OLSR oranı | tahmin yok | 2,200 → **2,130** |
| regresyon | yok — 44 vakanın hiçbiri OLSR koşmuyor | — |

U1: **U1-U GEÇTİ · U1-B TEMİZ** · açıklanmış düşük hücre **0**. 24 koşum,
8 işçi, 10 948 s. ETX kâhininin 12 değeri iki kayıtta birebir aynı.

🔒 Birebir tutması şunu kanıtlıyor: repodaki §13, teşhiste sınanan alt
sınıfla AYNI davranıyor — K-146'nın nedensel ölçümü bugünkü koda aittir.

## 3 · 🔴 Öngörülmeyen bedel — hareketli kollar

| kol | tohum | `OLSR-a` | **`OLSR-b`** | fark |
|---|---|---|---|---|
| `statik-yok` | 1000 · 1001 · 1002 | 0,926 · 0,859 · 0,866 | **0,943 · 0,926 · 0,908** | +0,018 · +0,067 · +0,042 |
| `bagimsiz-yok` | 1000 · 1001 · 1002 | 0,912 · 0,912 · 0,836 | 0,920 · 0,892 · 0,754 | +0,007 · −0,021 · **−0,082** |
| `gorev-yok` | 1000 · 1001 · 1002 | 0,934 · 0,751 · 0,870 | 0,923 · 0,628 · 0,806 | −0,010 · **−0,123** · −0,063 |
| `formasyon-yok` | 1000 · 1001 · 1002 | 0,972 · 0,944 · 0,867 | 0,975 · 0,923 · 0,690 | +0,003 · −0,021 · **−0,177** |
| kol ortalaması | | 0,884 · 0,887 · 0,851 · 0,928 | **0,926 · 0,855 · 0,786 · 0,863** | |

Hareketli dokuz hücrenin **yedisi düştü**; hepsi eşiğin üstünde ama ikisi
yakın (0,690 · 0,628). Kol ortalamasında OLSR hareketlide hâlâ AODV'nin
üstünde (0,855 · 0,786 · 0,863 ↔ 0,690 · 0,643 · 0,796).

⚠️ **Mekanizma ÖLÇÜLMEDİ.** Aday — hipotez, iddia değil: hareketli ve yüklü
kanalda MAC vazgeçmelerinin çoğu gerçek kopma değildir (K-139'un AODV
ölçümü: 8 fiziksel kopmaya karşı 2 565 *"koptu"* beyanı). §13 her birini
6 s'lik kayıp ilan eder; histerezisin bandındaki (0,3–0,8) bir bağ o süre
geri açılmaz, ve OLSR tamponlamadığı için başka rotası olmayan hedefe giden
paketler düşer. Sınaması: bir hareketli hücrede düşme sebepleri ve §13
bildirimi başına fiziksel kopma — bant ~2 saat.

## 4 · Bu bedel kararı geri aldırır mı — ajanın görüşü: HAYIR

Öğrencinin kararı bir ilkeye dayanıyordu (taban protokoller arasında bilgi
eşitliği: AODV bağ katmanı bildirimini kullanıyor, AOMDV makalesi de) ve
hareketli sonuç GÖRÜLMEDEN verildi. Hareketli sonucu görüp geri dönmek, bir
uygulama seçeneğini sonuca göre seçmek olurdu — bu kez ters yönde. İki ölçüm
de saklanıyor ve kendisi bir bulgu: **OLSR'ın §13'e duyarlılığı** statikte
+0,02…+0,07, hareketlide +0,01…−0,18. Rapor OLSR'ı §13'le verir ve bu
duyarlılığı yanında anar. Karar öğrencinindir.

✅ **Öğrenci (22 Eylül):** *"Karar kalsın, bulgu"* — §13 yerinde kalır,
duyarlılık bulgu olarak raporlanır, mekanizma ölçülmeden hipotez olarak
kalır.

## 5 · U3

OLSR 60 s → 120 s kontrol çerçevesi oranı **2,130** (§13 öncesi 2,200;
HELLO 470 → 948 · TC 1 572 → 3 402), AODV 2,070 (değişmedi). İkisi de
önceden yazılan [1,7 ; 2,3] bandında.

## 6 · Durum

- 🟢 **OLSR (`OLSR-b`) KAPANDI.** İki taban protokol kapalı.
- ⏭️ AOMDV — yazılmadan önce boşluk kararı (`02` §R4.1: a · b · c).
- İsteğe bağlı: hareketli kolda §13 mekanizmasının ölçümü (§3).

---

# K-148 · 🟢 AOMDV YAZILDI — AODV'nin alt sınıfı; entegrasyonda Şekil 3'ün harfiyen uygulanmasının bir KİLİDİ bulundu

> **Tarih:** 22 Eylül 2026 · **Karar:** öğrenci (*"Makale + RFC 3561"* —
> `02` §R4.1 seçenek a) · **Gerçekleme ve kayıt:** ajan
> **Üreticiler:** `tests2/test_aomdv.py` (16 kapı) ·
> `arsiv/teshis/aomdv_s10_2026-09-22/` (`aomdv_duman.py` · `aomdv_hata.py` ·
> `sonuc.md`)

## 1 · Yapı

`protokoller/aomdv.py` · `protokoller/aomdv_bicim.py` · `tests2/test_aomdv.py`.
U1 aletine `--protokol aomdv` eklendi (açıklanmış hücre listesi boş).

AOMDV **`AODV`nin alt sınıfıdır.** Makale onu AODV'nin uzantısı olarak
tanımlıyor ve ilkesi *"use of routing information already available in the
underlying AODV protocol as much as possible"*. Bu yüzden RFC 3561'in
makalenin değiştirmediği her parçası (HELLO · halka araması · tampon · hız
sınırları · RERR'in öncül kuralı · sıra numaraları · zaman aşımları) MİRAS
alınır ve yeniden yazılmaz — aynı kuralın iki kopyası bir gün ayrışır.
AODV'nin beyanlı sapmaları AOMDV için de aynen geçerli.

Yeniden yazılan yalnız makalenin değiştirdikleri: rota girdisi (Şekil 2b —
yol listesi, ilan edilen atlama) · güncelleme kuralı (Şekil 3, satır satır) ·
RREQ'in `ilk_atlama` alanı (+4 bayt) ve yinelenen kopyalar (§3.2) · hedefin
k = 3 benzersiz komşuya cevabı · RREP'in farklı ters yollardan dönmesi ·
bakım (*"yeni keşif yalnız bütün yollar kopunca"*). Girdinin `sonraki` ve
`atlama`sı BİRİNCİL yoldur, böylece AODV'nin veri gönderme kodu da miras.

## 2 · Beyanlı seçimler — ne makalede ne RFC'de

On seçim `aomdv.py`nin başlığında tabloyla, gerekçe ve yönüyle: S1 veri tek
yoldan (en az atlamalı) · S2 yol başına zaman aşımı yok (⚠️ bayat yedek yol
AOMDV'yi zayıflatabilir) · S3/S4 kopmada ve RERR'de yalnız o yol düşer, RERR
yalnız yolu kalmayan hedef için · S5 RREP'in ters yol seçimi · S6 alan
genişliği · S7 hedefte ters rota · S8 tek atlamalı komşu rotası · S9 ölçüm
beyanı (yalnız BİRİNCİL yol; yedeğe geçişte Δ = 0) · **S10** aşağıda.

## 3 · 🔴 S10 — Şekil 3'ü harfiyen uygulamak rotayı KİLİTLİYORDU

İlk entegrasyon koşusunda (küçük dünya, `bagimsiz-yok`, 60 s) AOMDV'nin
PDR'si **0,3233**'tü — AODV 0,5098 — ve 79 paket tampon tavanından
düşüyordu; AODV'de 0. Teşhis (`aomdv_hata.py`): kaynağa gelen **184** RREP
rotayı ne önce ne sonra kullanılır yapmamıştı.

**Kusur:** RFC 3561 §6.11 her geçersizleştirmede sıra numarasını YEREL
olarak bir artırır. Komşu rotası kopup (S8) yeniden kurulup yeniden kopunca
yerel sıra hedefin gerçek sırasını GEÇER. Şekil 3'ün (1) dalı `seq_i <
seq_j` ister; harfiyen uygulanınca hedefin kendi cevabı *"bayat"* diye
reddedildi, keşif *"başarılı"* sayılıp kapandı, paketler tamponda öldü.
AODV'miz geçersiz rotaya gelen her ilanı kabul ettiği için aynı şişmeden
etkilenmiyordu.

**Düzeltme:** geçersiz girdide (1) dalı işler — Şekil 3 geçersiz girdiyi ele
almıyor, dolayısıyla RFC 3561'in ve `AODV`nin kuralı geçerli.

| `bagimsiz-yok` | AODV-e | AOMDV S10 öncesi | AOMDV S10 sonrası |
|---|---|---|---|
| PDR | 0,5098 | 0,3233 | **0,5698** |
| `tampon_asimi` | 0 | 79 | **0** |
| rotayı kurmayan RREP (kaynakta) | 0 | 184 | 0 |

`statik-yok` birebir aynı kaldı (AOMDV 0,8644 · AODV 0,8488; AOMDV yarı
sayıda RREQ ve %14 az kontrol çerçevesi). Kapı:
`test_S10_GECERSIZ_girdiye_DUSUK_SIRALI_ilan_KABUL_edilir`.

🔒 **Ders:** bir makalenin şekli, altında yatan protokolün durum makinesini
VARSAYAR. *"Harfiyen"* uygulamak, varsayılan durumu (burada: geçersiz girdi
ve RFC'nin yerel sıra artırımı) dışarıda bırakınca yanlış olabilir. Bu kez
aynı dünyada AODV'yle yan yana koşmak yakaladı — K-143'ün dersinin
tekrarı.

## 4 · Kapılar — 16/16

biçim (+4 bayt, ad "RREQ", k = 3) · Şekil 3 (yeni sıra listeyi sıfırlar ·
eşit sırada yalnız küçük ilan · sözlük sırası) · ilan edilen atlama (en
büyük, ilan anında) · §3.2 (yeni ilk atlama yedek ters yol kurar ama
iletilmez · aynı ilk atlama bastırılır · kaynağın komşusu ilk atlama olarak
kendini yazar · hedef en çok k benzersiz komşuya) · RREP farklı ters yoldan ve
kendi ilanıyla · bakım (yedeğe geçiş, RERR yok, Δ = 0 · yedeğin kopması beyan
değil · son yol kopunca geçersiz + RERR · RERR yalnız gönderenden geçen yolu
siler) · S10 · U1 yapı (çok atlamalı teslim, defter kapalı, kâhin aşılmıyor,
yedek yol GERÇEKTEN kullanılıyor) · korunum hareketli kolda · koşum beacon'ı
kapalı.

Yapısal denetim: ihlal yok · **124** modül (121 + 3) · parametre sayısı
değişmedi (169) — `python kalibrasyon/mimari_denetimi.py`.

## 5 · Kapanıştan ÖNCE denetim — öğrencinin isteğiyle (*"4,5 saatimiz boşa gitmesin"*)

- **Kod incelemesi** (miras alınan her yöntemle birlikte): mantık hatası
  bulunmadı. Şüphelenilen tek nokta — ömrü dolmuş ama henüz geçersizleşmemiş
  rotaya gelen cevap tamponu yeniden sordurmuyor — kusur DEĞİL: tampon keşif
  zamanlayıcısının `uyandi`sında zaten yeniden soruluyor (`kosum/kontrol.py`,
  K-135); AODV de aynı.
- **Değişmez denetimi** (`arsiv/teshis/aomdv_s10_2026-09-22/degismez_denetimi.py`;
  her kancadan sonra: geçerli girdinin yolu var · geçersizin yok · her yolun
  sonraki atlaması komşu · hedefe doğrudan yol 1 atlama · kendine rota yok ·
  RREP döngüsü yok): **küçük dünya 2 kol · tam ölçek 4 kol, ihlal 0.** Tam
  ölçekte (kısa pencere 10/40/50 s) korunum dördünde de kapalı, `ttl` ve
  `tampon_asimi` 0, yedek yola geçiş 76 · 381 · 440 · 425.
- **U1 aleti** `--protokol aomdv duman` uçtan uca: çıkış 0.
- 🔧 Bulunan tek kusur KOZMETİK: U1 aleti *"kâhin aşıldı"* ve *"PDR yok"*
  iletilerinde protokolden bağımsız *"AODV"* basıyordu (OLSR koşumunda da).
  Sayıyı etkilemiyordu; artık ölçülen protokolün adı basılıyor.
- Kapanış betiği test takımı kalırsa uzun ölçüme GEÇMEZ.

## 6 · Açık

- ⏭️ **AOMDV kapanış ölçümü** — beklentisi ölçümden ÖNCE `DEVIR.md` §2'de.

---

# K-149 · 🟢 AOMDV KAPANDI — 12 hücrenin 12'sinde AODV'den iyi; düşük hücrenin sebebi ÖLÇÜLDÜ

> **Tarih:** 22 Eylül 2026 · **Kararlar:** öğrenci (kapanış paketi koşsun ·
> düşük hücre *"ölçerek açıklansın"*) · **Koşum ve kayıt:** ajan
> **Üreticiler:** `python -m pytest tests2 -q` ·
> `python -u kalibrasyon/aodv_uygunluk.py --protokol aomdv` (kayıt
> `ciktilar2/aodv_uygunluk/aomdv_son.json`) · `… hukum …` ·
> `python -u kalibrasyon/aodv_uygunluk.py u3` ·
> `python arsiv/teshis/aomdv_gorev1001_2026-09-22/teshis.py`

## 1 · Kapanış paketi — beklenti ÖNCEDEN yazıldı (`DEVIR.md` §2, K-148)

| adım | önceden yazılan | sonuç |
|---|---|---|
| test takımı | `637 passed` | ✅ **637 passed** (572 s) |
| U3 · AODV ve OLSR oranları | BİREBİR yeniden çıkmalı (kodları değişmedi) | ✅ **2,070** ve **2,130** birebir |
| U3 · AOMDV oranı | tahmin YOK | **2,310** |
| U1-U | GEÇMELİ | ✅ geçti |
| U1-B | tahmin YOK (liste boş başlıyor) | bir düşük hücre — §3'te ölçülüp açıklandı |
| regresyon | gerekmez (44 vakanın hiçbiri AOMDV koşmuyor) | — |

24 koşum, **8 işçi**, 8 890 s ≈ **2 sa 28 dk** (bant 2,5–4,5 sa).

## 2 · Üç taban protokol, AYNI 12 hücre (protokolün ETX kâhinine oranı)

| kol | tohum | `AODV-e` | `OLSR-b` | **`AOMDV-a`** |
|---|---|---|---|---|
| `statik-yok` | 1000 · 1001 · 1002 | 0,995 · 0,999 · 0,932 | 0,943 · 0,926 · 0,908 | 0,996 · 0,998 · 0,931 |
| `bagimsiz-yok` | 1000 · 1001 · 1002 | 0,805 · 0,715 · 0,549 | 0,920 · 0,892 · 0,754 | 0,869 · 0,786 · 0,657 |
| `gorev-yok` | 1000 · 1001 · 1002 | 0,830 · **0,462** · 0,636 | 0,923 · 0,628 · 0,806 | 0,839 · **0,512** · 0,643 |
| `formasyon-yok` | 1000 · 1001 · 1002 | 0,931 · 0,811 · 0,646 | 0,975 · 0,923 · 0,690 | 0,941 · 0,874 · 0,742 |
| kol ortalaması | | 0,975 · 0,690 · 0,643 · 0,796 | 0,926 · 0,855 · 0,786 · 0,863 | 0,975 · 0,771 · 0,665 · 0,852 |

- 🟢 **AOMDV, 12 hücrenin 12'sinde de AODV'nin üstünde.** Çoklu yolun kazancı
  bu ölçekte ÖLÇÜLDÜ; makalenin kendi iddiasının yönüyle aynı.
- Hareketli kollarda **OLSR önde**, statikte AOMDV ile AODV başa baş (kol
  ortalaması 0,975) ve OLSR geride.
- Rota tamponu: AOMDV tepe **32/64**, süre tavanından düşen **0** (AODV'de
  64/64 ve 89). Tamponun iki `SINANMAMIS` parametresi AOMDV'yi BAĞLAMIYOR.
- ⚠️ Bunlar bir **kabul kapısının** sayılarıdır, ana deneyin karşılaştırması
  değil (`06` §4.4 madde 3): tek pencere, üç geliştirme tohumu, karıştırıcısız.

## 3 · Düşük hücrenin (`gorev-yok/1001`) açıklaması — ön-kayıtlı teşhis

Ön-kayıt ölçümden ÖNCE yazıldı
(`arsiv/teshis/aomdv_gorev1001_2026-09-22/onkayit.md`). Tam pencerede, aynı
hücrede AOMDV ve AODV; PDR'ler kapanış ölçümüyle **birebir** (0,3786 ·
0,3418) — sarmalayıcı davranışı değiştirmedi.

| # | hipotez | öngörü | sonuç |
|---|---|---|---|
| M1 | atlama sayısıyla yönlendirme zayıf bağları seçiyor (bağ kalitesi eşiği YOK) | başarısızlıkların **> %60'ı** `p_atlama < 0,90` bağlarda | ✅ **%70** — ve o bağlar kullanımın yalnız **%23'ü** (AODV: %72 / %25) |
| M2 | rota boşluğu | `hedef_yok` baskın | ❌ `hedef_yok` **0** |
| M3 | döngü | `ttl` belirgin | ❌ 36 paket (%0,3) — §4 |
| M4 | tampon tavanı | `tampon_asimi` > 0 | ❌ ZATEN çürüktü: 14 234 giriş, **0** düşen |

Kayıp birkaç akışta yoğun: 10 akışın **3'ü** neredeyse hiç teslim etmiyor
(126 · 107 · 56 / 1 080), **2'si tam** teslim ediyor. Yani sorun ağ geneli
değil, yapısal olarak zayıf birkaç yol — K-137 §4'ün kanal grafiğinden
ölçtüğü sayıyla tutarlı: bu hücre görev kolunun **en zayıf eşiksiz en kısa
yoluna** sahip (0,2502; 1000'de 0,5519).

🔎 **Yorum (ayrıca ölçülmedi, iddia değil):** OLSR aynı hücrede geçiyor
(0,628) ve K-146 onun histerezisinin bağları kontrol paketi teslimine göre
süzdüğünü ölçmüştü. AODV ailesinde böyle bir süzgeç yok — hedef İLK ULAŞAN
RREQ kopyasına cevap verir. Bu farkı doğrudan sınamak ayrı bir ölçüm ister.

## 4 · Dürüst yan bulgu — AOMDV'de TTL düşmesi

Aynı hücrede AOMDV 36, AODV 0 paketi TTL tükenerek düşürdü (üretilenin
%0,3'ü). Çoklu yolun geçici tutarsızlığının bedeli; U1 oranını açıklamıyor
(hepsi teslim edilseydi oran 0,512 yerine ~0,517 olurdu). Kapanış öncesi değişmez denetimi dört kolda RREP
döngüsü BULMADI, yani kalıcı bir döngü değil.

## 5 · Durum

- 🟢 **ÜÇ TABAN PROTOKOLÜN ÜÇÜ DE KAPANDI:** `AODV-e` (K-145) · `OLSR-b`
  (K-147) · `AOMDV-a` (bu kayıt). Üçü de aynı 12 hücrede, aynı kâhine karşı,
  aynı kapıdan geçti.
- ⏭️ **Aşama 3 · özgün protokol** — tasarımı öğrencinin.
- Açık borçlar değişmedi: 40 `SINANMAMIS` · duyarlılık borcu 9 ·
  `algilama_duyarliligi`nin ikiye bölünmesi · ana deneyin koşum bütçesi.

---

# K-150 · 🟡 AŞAMA 3 AÇILDI — DESPARETE v0.1 tasarım paketi okundu; simülatörle üç yapısal boşluk, dört tasarım sorusu

> **Tarih:** 22 Eylül 2026 · **Tasarım:** öğrenci
> (`protokol_kaynaklari/DESPARETE_TASARIM_PAKETI/`, 41 belge, v0.1 aday) ·
> **İnceleme:** ajan · **Kararlar:** öğrenci — §4

## 1 · Tasarımın özü (incelemenin okuması)

Tek-sink, hedef-yönlü, yönlü bağ maliyetli bir uzaklık-vektörü alanı.
Döngüsüzlük TTL'ye DEĞİL, hedefin ürettiği sıra numarası (DFSN) ile
feasibility distance'a dayanır — Babel'in (RFC 8966) koşulunun ailesi.
Bağ maliyeti `C = 16 + C_quality(Q) + C_risk(R)`, `R = max(H, U)`; Q yerel
unicast sonuçlarından (son 2 s, en çok 16 sonuç, tekrar sayısıyla
ağırlıklı), H art arda üç 0,5 s'lik düşüşten, U örnek yaşı ve sayısından.
Postürler STEADY / CAUTION / PROTECT; PROTECT'te sınırlı ikinci kopya.
Güvenlik Profili 1: her pakette Ed25519.

🔒 Tasarımın kuralları bu projeninkilerle aynı disiplinde: yenilik iddiası
yeniden taramayla geri çekilmiş, "jamming tespiti" iddiası yok, TTL kanıt
sayılmıyor, her sabitin gerekçesi yazılı.

🔎 **Bağlantı:** üç taban protokolün düşük hücrelerinin ortak sebebi
ölçüldü — atlama sayısıyla yönlendirme zayıf bağları seçiyor (K-146 · K-149).
DESPARETE'nin maliyeti tam bu zayıflığı hedefliyor. ⚠️ Kaliteye dayalı
maliyetin kazancı literatürde bilinir (ETX); deney, kazancın kalite
metriğinden mi yoksa yeni parçalardan mı geldiğini **mekanizma
bayraklarıyla** ayırmalı (`12` §5, Aşama 3).

## 2 · Simülatörle uyum

**Hazır:** yerel saat · unicast ve yayın kontrol mesajları · titreşimli
zamanlayıcılar (düğüm başına 256 bekleyen uyandırma) · MAC vazgeçmesi
bildirimi · ölçüm beyanları · kâhinsiz gözlem (tasarım zaten yalnız yerel
gözlem istiyor) · tek-sink telemetri = yere toplama deseni.

**`sim2/`de değişiklik gerektiren (yapı onayı gerekir):**

| # | boşluk | kanıt | etkisi |
|---|---|---|---|
| Y1 | her unicast sonucunun TEK TEK bildirimi ve tekrar sayısı | gözlem yalnız `son_iletim_sonucu`nu taşıyor; başarı için ayrı kanca YOK (`gozlem/protokol.py`) | M0.1'in Q'su doğrudan buna dayanıyor |
| Y2 | veri paketine protokol başlığı baytı | veri çerçevesi `paket_bayt`la sabit; protokol bayt ekleyemiyor | DESPARETE başlığı 36 B (Profil 1 ile 194 B) — ödetilmezse ucuz görünür |
| Y3 | kopyalama + paket kimliği + tekil teslim sayımı | `Karar` tek `sonraki` taşıyor; paket görünümünde kimlik yok | PROTECT yedekliliği; korunum defterini etkiler |

**Beyanla çözülebilir:** tampon ömrü (tasarım 6 s ↔ ortak tampon 30 s) ·
hop sınırı (16 ↔ TTL 32) · trafik sınıfı/koruma biti · roster ve profil
kabulü (hepsi kabul edilmiş sayılır).

## 3 · Tasarım soruları — ölçüm perspektifinden, hüküm değil

1. **Güvenlik değerlendirmede açık mı** — Profil 1 paket başına 78–158 B;
   veri çerçevesi ~%38 büyür, taban protokollerde güvenlik yok.
2. **Ters yön trafik** — v0.1 yalnız sink'e yönlendirir (`23` §7:
   *"ApplicationDestinationID != SinkID → local policy failure"*). Yere
   toplamanın 4 komut akışı düşer; U1 kapısının eşler-arası deseni de
   çalışmaz.
3. **Boşta sondalama yükü** — her ACTIVE komşuya 2 s'de bir unicast PROBE.
   Kaba üst sınır (tek çarpışma alanı, N = 40, derece 8,7, değişim başına
   iki unicast + onay): kanal süresinin **%20–26**'sı. Uzamsal yeniden
   kullanım düşürür; gerçek değeri simülatör ölçecek.
4. **U eşiği ↔ sondalama hızı** — yalnız sondalanan bir bağın 2 s'lik
   penceresinde ~1 örnek olur → `U_sample = 128` → `R ≥ 128` → +16 risk
   cezası ve CAUTION kanıtı. Veri taşımayan her bağ kalıcı olarak
   "belirsiz" görünür; bu trafik yoğunluğundan bağımsız, YAPISAL.

## 4 · Öğrenci kararları (22 Eylül)

- ✅ **Güvenlik:** ana karşılaştırmada dört protokol de güvenliksiz;
  Profil 1'in bayt bedeli ayrı bir duyarlılık kolunda ölçülür.
- ✅ **Yedeklilik:** ilk gerçekleme yedekliliksiz; Y3 sonraya.
- ✅ **Ters yön trafik — A · isteğe bağlı hedef alanı** (tartışmadan sonra):
  komut alacak düğüm kendi alanını üretir; tasarımın edinim mekanizması
  (FIELD_SOLICIT · DFSN_REQUEST) yalnız sink için değil her hedef için
  çalışır. Döngüsüzlük kanıtı değişmez (kanıt alan başına; her alanın tek
  üreticisi var). Bedeli: alan sayısı 1 → 5, alan ilanı yükü ~5 kat; ilk
  komut paketi edinimde düşer (v0.1 kuralı); alan EMEKLİLİK kuralı tasarıma
  yazılmalı. Elenenler: B ters ağaç (RPL benzeri — yeni döngüsüzlük
  argümanı ister, gelecek çalışma) · C komutlar düşer · D komutlar ana
  deneyden çıkar.
- 🔒 DESPARETE'nin U1'i YERE TOPLAMADA koşulur (v0.1 eşler-arası deseni
  yönlendiremez); U1 her protokolün kendi işletme profilindeki kabul
  kapısıdır, taban protokollerin U1'i geçerli kalır. Beyan edilir.
- ✅ **Y1 ve Y2 onaylandı** (yapı anlatıldıktan sonra): Y1 — isteğe bağlı,
  niyet döndürmeyen bir bildirim; her unicast (veri ve kontrol) sonucunda
  hedef, başarı ve tekrar sayısı. Y2 — protokol sınıfı veri başlığı baytını
  bildirir (taban protokoller 0, DESPARETE 36; güvenlik kolunda 194); bu
  baytlar YÖNLENDİRME ek yüküne sayılır. Uygulaması K-151'de.
- ✅ **Hedef alanı emekliliği:** simülasyon profilinde YOK — kurulan alan
  koşu boyunca sürer; yeni sabit gerekmez. Emeklilik kuralı tasarımda
  gelecek çalışma olarak beyan edilir.
- ✅ **§3'ün 3. ve 4. soruları:** v0.1 YAZILDIĞI GİBİ gerçeklenir; boşta
  sondalama yükü ve belirsizlik eşiğinin etkisi geliştirme tohumlarında
  ÖLÇÜLÜR; tasarım değişikliği ölçümden sonra, v0.2'de ve kanıtla.
- ✅ **CAUTION'ın eylemi (yedeklilik kapalıyken):** tasarımda sayısal
  karşılığı YOKTU (`15` §3 *"sınırlı daha sık gözlem"*, `22` §5 *"probe
  yoğunluğunu artır"*; `21` bir değer vermiyor). Seçilen: CAUTION'a
  GİRİŞTE seçili ardıla bir kez sınırlı doğrulama oturumu — tasarımın
  kendi kuralıyla (`20`: `T_probe_start` tetikleyicileri arasında
  *"CAUTION/PROTECT'te ek doğrulama ihtiyacı"*; en çok 2 PROBE, 1,3 s).
  Yeni sabit yok. Elenenler: yeni sondalama aralığı (gerekçesiz sabit) ·
  postürün yalnız izlenmesi (politika bayrağı etkisiz kalırdı).
- ✅ **DFSN_REQUEST'in iletimi — TEK YAYIN çerçevesi.** Belge iki okumaya
  açıktı (`23` §5.1 *"broadcast/forward-control"* ↔ §5.3 *"one copy … to
  each ACTIVE neighbor"*). Yayında her düğüm isteği bir kez yayınlar,
  ACTIVE olmayan alıcı kabul kapısında reddeder; bir dalga ~40 çerçeve
  (komşu başına unicast ~350). Bedeli: yayında onay/tekrar yok.
- 🔎 **Yorum (beyan):** PROBE ve PROBE_REPLY MAC UNICAST olarak
  gerçeklenir — M0.1'in *"uygun sonuç"*u bağ sonucu ister ve `23` §3.1
  *"confirmed local unicast/ACK"*u kanıt sayar; yayın çerçevesinin bağ
  sonucu yoktur. FIELD_UPDATE yayındır; FIELD_SOLICIT'e cevap olan
  FIELD_UPDATE (`23` §5.2 *"once to j"*) unicast.

---

# K-151 · 🟢 `sim2/` Y1 · Y2 — her unicast sonucunun bildirimi ve protokolün veri başlığı

> **Tarih:** 22 Eylül 2026 · **Karar:** öğrenci (yapı anlatıldıktan sonra
> *"ikisi de onaylı"*, K-150 §4) · **Uygulama:** ajan
> **Üreticiler:** `tests2/test_kosum.py` (altı yeni kapı) ·
> `python -u kalibrasyon/regresyon_satirlari.py uret k151` ·
> `python -u kalibrasyon/regresyon_satirlari.py karsilastir k144 k151`

## 1 · Neden

DESPARETE'nin M0.1 profili bağ kalitesini son 2 s'nin en çok 16 unicast
sonucundan ve her başarının TEKRAR sayısından hesaplar. Simülatör yalnız
*"son iletimin sonucu"*nu veriyordu; başarı için olay yoktu, iki gözlem
arasındaki iletimler kayboluyordu. Ayrıca protokolün veri paketine eklediği
başlık (36 B) ödetilemiyordu — DESPARETE'yi olduğundan ucuz gösterirdi.

## 2 · Y1 — `iletim_sonucu(gozlem, hedef, basarili, tekrar, tur)`

- İsteğe bağlı `SonucBildirimliProtokol`; kontrol kancalarının hepsi-ya-hiç
  kuralına girmez. Taşımayan protokol HİÇ çağrılmaz (düğümde kurulumda bir
  kez okunan bayrak — iletim başına maliyet yok).
- Dört yerde çağrılır: veri onayı · veri vazgeçmesi · kontrol unicast onayı ·
  kontrol unicast vazgeçmesi. `tekrar` DCF sayacı sıfırlanmadan önce okunur
  (ilk denemede başarı → 0; vazgeçmede yeniden deneme sınırı).
- Başarısızlıkta `iletim_basarisiz`den ÖNCE: protokolün ölçümü onarım
  kararından önce güncellenir.
- 🔒 NİYET DÖNDÜRMEZ (dönerse koşu durur). Bilgi göndericinin KENDİ MAC'inin;
  `Gozlem` alanları değişmedi, yüzey büyümedi.
- Yeni sayaç `sonuc_bildirimi`.

## 3 · Y2 — protokol sınıfı `veri_baslik_bayt`

- Yoksa 0. Kurulum protokolden bağımsız kalır (`kurulum_hash` değişmez);
  başlıklı veri çerçevesi koşuda türer. Başlığın süresi iki çerçevenin
  FARKIDIR — bit hızı aritmetiği yalnız `kanal/cerceve.py`de.
- `veri_bayt` ve `veri_airtime_s` yalnız YÜKÜ sayar; başlık yeni
  `veri_baslik_bayt` · `veri_baslik_airtime_s`e gider.
- 🔒 **Ölçüm tanımı — ölçümden ÖNCE:** `nrl_bayt` ve `nrl_airtime`in payı
  artık *kontrol + veri başlığı*dır (`Turev.ek_pay`). Başlığı 0 olan
  protokolde oranlar BİREBİR eskisi.
- Çerçeve uzadıkça hataya açık bit de artar (fiziksel olarak doğru).
  Tepkisel karıştırıcının tipik veri çerçevesi süresi ve kâhin grafiğinin
  çerçevesi PROTOKOLDEN BAĞIMSIZ kalır: saldırgan protokolü bilmez, kâhin
  kendi protokolüdür. Beyan.

## 4 · Kapılar — altı yeni test

Y1: bildirimler simülatörün kendi sayaçlarıyla BİREBİR (veri başarısı =
`mac_gonderim_basarili` · vazgeçme = `kontrol_basarisiz_bildirim` · kontrol
başarısı = `kontrol_unicast_onaylanan` · toplam = `sonuc_bildirimi`),
vazgeçmede tekrar = sınır, tekrarlı başarı GÖRÜLÜYOR, sıra ihlali 0 ·
taşımayan protokol çağrılmaz · niyet döndüren reddedilir. Y2: çerçeve 548 B,
`veri_bayt` yalnız yük, başlık baytı ve süresi tam, NRL tanımı · başlıksızda
aynı çerçeve nesnesi ve sayaç 0 · negatif başlık reddedilir.

## 5 · 🔒 Regresyonun beklenen farkı — KARŞILAŞTIRMADAN ÖNCE yazıldı

`k144` ↔ `k151`, 44 vaka. Hiçbir vaka Y1'i taşımıyor ve hiçbirinin başlığı
yok. Beklenen:

- **Değişmemeli:** var olan bütün metrikler (`nrl_*` dâhil) · korunum ve
  mutabakat · kapsam · `kurulum_hash` · `evren_hash` · köken kovaları.
- **Değişmeli (ilan edilmiş):** `kimlik.sayac_semasi_hash` (üç yeni sayaç,
  iki türevde `ek_pay`) · yeni metrik alanları `veri_baslik_bayt`,
  `veri_baslik_airtime_s`, `sonuc_bildirimi` ve pencere ikizleri — 44
  vakanın HEPSİNDE 0 · `kimlik.arac_hash` (her zaman).

Bir tek var olan metrik değişirse düzeltme değil kusurdur ve sebebi
bulunmadan devam edilmez.
