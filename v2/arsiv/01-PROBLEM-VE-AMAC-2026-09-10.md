# 01 — PROBLEM, AMAÇ VE SINIRLAR

> ## ✅ GÜNCEL — 5 Eylül 2026
> Bu belge **çözümden bağımsızdır**: problem, özgünlük ve kısıtlar
> simülatörün hangi sürümüyle çalışıldığına bağlı değil. `sim2/` ile
> çelişen tek bir iddia taşımadığı denetlendi *(K-093)*.


> ⚠️ **BU BELGE ÇÖZÜM İÇERMEZ VE İÇERMEYECEKTİR.** Burada yalnızca *neyin
> çözülmeye çalışıldığı*, *hangi kısıtlar altında* ve *neyin başarı sayılacağı*
> yazılıdır. **Nasıl** çözüleceği öğrenciyle birlikte sıfırdan kurgulanacaktır.

---

## 1. YARIŞMA VE TAKVİM

| | |
|---|---|
| **Yarışma** | TÜBİTAK 2204-A — Lise Öğrencileri Araştırma Projeleri Yarışması |
| **Alan** | Yazılım / Bilgisayar Bilimleri |
| 🎯 **Son teslim** | **19 Aralık 2026** |
| Başvuru açılışı | 13 Ekim 2026 |
| Ön değerlendirme | Aralık 2026 – Ocak 2027 · Bölge sergisi seçimi ~28 Ocak 2027 |
| **Kim yapıyor** | Bir lise öğrencisi, tam zamanlı çalışıyor, acele etmiyor |

> ⚠️ **Resmî 2204-A proje rehberi sonbaharda yayımlanacak.** Değerlendirme
> kriterleri ve ağırlıkları çıktığında `tubitak.gov.tr`den indirilip §4
> güncellenmelidir. Bu, planın ilk maddesidir.

---

## 2. PROBLEM ALANI

**Elektronik harp (karıştırma) altında çalışan taktik İHA mesh ağlarında
haberleşmenin ayakta kalması.**

Bir İHA sürüsü, tek bir merkeze değil **birbirine** bağlıdır: düğümler
birbirinin paketini taşır. Bir karıştırıcı devreye girdiğinde bağlantı
kalitesi rastgele değil **yapılı** biçimde bozulur — karıştırıcı sabit bir
noktadadır, darbelidir, ya da hareket eder. Ağın bu bozulmaya nasıl tepki
verdiği, sürünün görevini sürdürüp sürdüremeyeceğini belirler.

### 2.1 Doğrulanmış saha gerçekliği

> ⚠️ **Kanıt gücü sütunu bağlayıcıdır.** Her iddia, kaynağının gerçekte
> desteklediği kadar güçlü sunulur — daha fazlası değil. Ayrıntı ve künyeler:
> `v2/02-DOGRULANMIS-KAYNAKLAR.md`.

| İddia | Kanıt gücü | Nasıl kullanılabilir |
|---|---|---|
| Ukrayna'da aylık ~10.000 İHA kaybı; her 10 km cepheye ≥1 büyük EH sistemi | 🟡 **Tahmin** (RUSI, üç isimsiz subay mülakatı) | Yalnızca **büyüklük mertebesi** göstergesi |
| 2024'te operasyona sokulan FPV'lerin %60–80'i **karıştırmaya maruz kaldı** | 🟡 Tahmin | ⚠️ "hedefe ulaşamadı" **değil** — anlam kayması var |
| Yüksek mobiliteli VANET'lerde AODV varyantları PDR < %50 | 🟢 Yayınlanmış | **Mobilite** için geçerli, **karıştırma için değil** |
| Tek kanallı mesh (BATMAN-adv) karıştırma altında bağlantıyı tamamen yitiriyor | 🟢 Deneysel (SPIDERMAN) | Tek kanal kırılganlığına doğrudan kanıt |
| Çok atlamalı zincirde verim düşüşü: ideal 1/4, 802.11 gerçekte 1/7 | 🟢 Yayınlanmış (Li vd.) | Kesin sayılar — ölçüm ortamını doğrulamak için **replikasyon hedefi** olabilir |
| ~~"AODV/OLSR/BATMAN karıştırma altında <%50 PDR"~~ | 🔴 **Birincil kaynak YOK** | ❌ **İDDİA EDİLMEZ.** Bu boşluk, projenin **ölçeceği şeydir** |

> ⭐ Son satır bir zayıflık değil **varlık gerekçesidir**: literatürde bu
> protokollerin karıştırma altındaki karşılaştırmalı davranışı için doğrudan
> birincil kaynak bulunamamıştır. Kontrollü bir ortamda bunu ölçmek başlı
> başına bir katkıdır.
>
> 🟢 **31 Ağustos 2026 — BAĞIMSIZ OLARAK DOĞRULANDI.** 20 dosyalık bir
> literatür taraması *(`v2/yeni_detaylı_arastırma/`)* aynı sonuca ulaştı:
> *"2022–2026 FANET literatüründe OLSR, AODV ve GPSR için değişen SJR
> altında doğrudan raporlanmış PDR ve E2E gecikme düşüş yüzdeleri
> **bulunamamıştır. Bu, bir eksik arama değil, doğrulanmış bir literatür
> boşluğudur.**"*
>
> ⭐ **VE İKİNCİ BİR BOŞLUK DAHA BULUNDU:** aynı protokollerin RF karıştırma
> altında **saniye ölçeğinde rota kurtarma gecikmesini** bildiren birincil
> kaynak da yok. İkisi de bu projenin ölçeceği şeydir.
> Ayrıntı: `10-LITERATUR-KOD-KARSILASTIRMA.md` §5.

### 2.2 Literatürün durumu — alan KALABALIK

Taranan bir derleme (*Mathematics* 2022, 10, 3017) **on üç** Q-öğrenme tabanlı
FANET yönlendirme protokolü sayıyor: QTAR · QMR · QGeo · QSRP · QLGR ·
FEQ-routing-SA · Q-FANET · PPMAC+RLSRP · PARRoT · QFL-MOR · 3DQ · ICRA ·
TARRAQ.

**Bunun iki sonucu var ve ikisi de bağlayıcıdır:**

1. ❌ *"İlk"*, *"eşi yok"*, *"literatürde bulunmuyor"* iddiaları **yasaktır.**
2. ⭐ Aynı derlemenin Table 26'sı mevcut ödül fonksiyonlarını listeliyor ve
   **hiçbirinde girişim/karıştırma terimi yok.**

> 🔴 **1 EYLÜL 2026 — İKİNCİ MADDE ZAYIFLATILDI (dürüstlük düzeltmesi).**
> Buradaki cümle eskiden *"doğrulanmış bir tablodan okunan somut bir
> boşluk"* diyordu. 20 dosyalık yeni tarama Table 26'yı **yeniden
> doğrulayamadı**: *"MDPI tam metnine erişim kısıtlı olduğundan … protokol
> listesi **arama özeti ve metadata üzerinden** doğrulanmıştır."* Protokol
> sayısı da uyuşmuyor *(`02` B6 **13** diyor, yeni tarama **14** listeliyor)*.
>
> 🔒 **KARAR (öğrenci, 1 Eylül 2026):** iddia artık Table 26'ya değil,
> yeni taramanın **kendi matrisine** dayandırılır — 11 protokol × 6 sütun,
> *"Açık Jamming"* sütunu **9 protokolde `Hayır`**, 1'inde *kısmen*,
> 1'inde *(RLGM)* yalnızca **jammer tespiti**, yönlendirme ödülü değil.
> Daha zayıf görünür ama **yeniden üretilebilir** — ve `03` kural 1 için
> belirleyici olan budur.
> Ayrıntı: `10-LITERATUR-KOD-KARSILASTIRMA.md` §7c Y-2.

### 2.3 Kabul edilmiş sınır

> *"if the flying ad hoc network is large, these routing methods deal with the
> curse of the dimensionality problem"* — aynı derleme.

Küçük ağlar (N ≤ 40) için tablo tabanlı yaklaşımlar uygundur; büyük ağlarda
boyut laneti doğar. Bu sınır **raporda açıkça yazılır.**

---

## 3. AMAÇ

Bu proje bir **tasarım** projesidir: bir çözüm kurgulanır, inşa edilir ve
kontrollü bir ortamda **ölçülerek** savunulur.

> 🔑 **Çerçeve (öğrencinin kararı):** *Ürün çözümün kendisidir; ölçüm onun
> kanıtıdır.* Bu proje pasif bir "şunları test ettik" değerlendirmesi
> **değildir.**

**Sıralı hedefler:**

1. **Bilimsel olarak dürüst ve savunulabilir** bir çalışma üretmek
2. Jürinin *"bu bir lise projesi için olağanüstü"* diyeceği bir **yöntem
   olgunluğu** göstermek
3. Mümkünse **çalışan bir çözüm**, mümkün değilse **iyi teşhis edilmiş bir
   negatif sonuç**

> ⚠️ Üçüncü madde teselli ödülü değildir. Bir hipotezi **deney öncesi ilan
> edilmiş** bir yanlışlanma koşuluyla test etmek ve koşul tetiklendiğinde onu
> dürüstçe raporlamak, jüri karşısında çalışan bir çözümden **daha zor taklit
> edilen** bir şeydir.

### 3.1 🔒 DÖRT FAZ — iş planı *(1 Eylül 2026, öğrenci kararı)*

🔴 **"FAZ" bir iş aşamasıdır; "AİLE" istatistiksel düzeltme birimidir**
*(Holm aile içinde uygulanır)*. İkisi ayrı kavramdır ve karıştırılmaz.

| Faz | Ne yapılır | Hipotez ailesi |
|---|---|---|
| **Faz 0** | Ölçüm aracının kurulması ve **dört seviyede doğrulanması** | — *(kapı, hipotez yok)* |
| **Faz 1** | **Rakip protokollerin kurulması** + gerçekçi veri ürettiklerinin **kanıtlanması** | **Aile 1** — karakterizasyon |
| **Faz 2** | **Özgün protokolün kurulması** + rakiplerle karşılaştırma, veri toplama | **Aile 2** *(üstünlük)* · **Aile 3** *(mekanizma ablasyonu)* |
| **Faz 3** | Pürüz temizleme, görselleştirme, rapor yazımı | — |

### 3.2 🔒 ÖZGÜNLÜK NEREDEN GELİYOR

> **Özgünlük, kurulan protokolün kendisinden gelir.** Proje pasif bir
> *"şu protokolleri test ettik"* değerlendirmesi değildir: standart
> protokoller **kıyas tabanıdır**, ölçülen şey **öğrencinin kendi
> tasarımının** onlara göre nasıl davrandığıdır.

🟢 **Ve Faz 1 tek başına da bir katkıdır:** rakipleri kurup SJR ekseninde
ölçmek, §2.1'de doğrulanan literatür boşluğunu **doldurur**. İki katkı
birbirini besler — biri olmadan diğeri de zayıflar.

---

## 4. TÜBİTAK KRİTER MATRİSİ

⚠️ Resmî rehber çıkınca doğrulanacak. Her kriterin bu proje için ne gerektirdiği:

| Kriter | Bu projede ne gerektirir |
|---|---|
| **Özgün Değer** | Dar ve **çürütülemez** bir iddia. Alan kalabalık (§2.2) — *"ilk"* demek yerine *"hangi koşulda ne olduğunu ölçtük"* demek |
| **Fikir sahipliği / ÜYZ etiği** | 🔴 **En kırılgan alan — aşağıda ayrıca** |
| **Yöntem / Bilimsel Kurgu** | Ön-kayıtlı yanlışlanma koşulu · birden çok **ayarlanmış** karşılaştırma noktası · ≥30 tohum · eşleştirilmiş test + çoklu karşılaştırma düzeltmesi · **literatür replikasyonu** |
| **Fizibilite** | Sıfır donanım, sıfır yasal risk, öğrencinin makinesinde koşabilen hesap |
| **Yerli / Milli Katkı** | ⚠️ **Muhtemelen en zayıf halka.** Bilinçli olarak güçlendirilmeli (§4.2) |
| **Yaygın Etki** | Açık kaynak + Türkçe teknik doküman + tekrarlanabilir veri |
| **Sunum / Poster** | Kararların **açıklanabilir** olması; stant demosu potansiyeli |

### 4.1 🔴 Fikir sahipliği — yapısal risk ve tek panzehiri

Bir yapay zekâ danışmanla çalışıldığında, mimarinin büyük kısmını yapay zekâ
önerirse **TÜBİTAK'ın en çok önem verdiği kriterde yapısal bir kırılganlık**
doğar. Bilimsel içerik sağlam olsa bile.

> **Panzehir iki parçalıdır ve ikisi de BAŞTAN kurulmalıdır:**
>
> 1. **Tarihli karar kaydı** — her tasarım kararı: *kim önerdi · hangi
>    alternatifler değerlendirildi · neden bu · bunu ne değiştirirdi*
> 2. **Katkıyı ÖLÇMEK, tahmin etmemek** — bir mekanizmanın katkısı
>    ablasyonla ayrıştırılabiliyorsa ayrıştırılır
>
> ⭐ **Ölçülmüş bir ayrım, ölçülmemiş bir bütün iddiadan güçlüdür.** Jüri
> *"bu sayının ne kadarı size ait?"* diye sorduğunda, ölçülmüş bir yüzde
> vermek en güçlü cevaptır.

🔴 **Bu mekanizma sonradan eklenemez.** Karar kaydı tutulmadan verilen bir
karar, sonradan kime ait olduğu belirlenemeyecek bir karardır.

### 4.2 Yerli / milli katkı çerçevesi

Türkiye taktik İHA üretiminde önde gelen ülkelerden biridir (Bayraktar
TB2/Akıncı, TAI Anka/Aksungur, Kızılelma; sürü tarafında STM Kargu, KEMANKEŞ).
Sürü operasyonu tek İHA'dan farklı olarak **düğümler arası mesh haberleşmeye**
bağımlıdır ve bu katman büyük ölçüde tescilli/yabancı veri bağı IP'si üzerine
kuruludur.

**Savunulabilir iddia:** *milli sürü platformlarının ihtiyaç duyduğu alanda,
elektronik harp altında çalışabilen, açık kaynak ve Türkçe belgelenmiş bir
kavram kanıtı.*

> ⚠️ **Dürüstlük sınırı:** hiçbir savunma sanayii kurumuyla temas, veri
> paylaşımı veya onay iddiası yapılamaz. İddia *"kavram kanıtı"* düzeyinde
> kalmalıdır.

---

## 5. KISITLAR — bunlar tasarımı sınırlar

| Kısıt | Değer | Neden |
|---|---|---|
| **Süre** | 19 Aralık 2026'ya kadar. **Son ~7 hafta yazıma kilitlidir** | Rapor, koddan çok daha yavaş yazılır |
| **Platform** | **Windows.** Ötesi AÇIK KARAR | Öğrencinin makinesi Windows. Hangi ortamda ölçüleceği (hazır bir ağ simülatörü mü, kendi yazılan mı) **verilmemiş bir karardır** — ödünleşimi §5.3'te |
| **Donanım** | **Yok.** Gerçek RF, SDR, uçuş testi kapsam dışı | Yasal engel + bütçe |
| **İşlemci** | Öğrencinin kişisel makinesi. Deneyler çekirdeğin **yarısıyla** koşar | Makine deney sırasında kullanılabilir kalmalı |
| **Anlaşılabilirlik** | 🔴 **Öğrenci savunamadığı hiçbir şeyi projede tutmaz** | Jüri karşısında anlatan öğrencidir |

### 5.1 Kapsam dışı — ve bu kararlar gerekçelidir

| Dışlanan | Gerekçe |
|---|---|
| Gerçek RF karıştırıcı / SDR / uçuş testi | Yasal + bütçe |
| Sembol seviyesi PHY (OFDM, modülasyon) | Kapsam patlaması; SINR→PER soyutlaması yeterli |
| Kriptografi, GPS spoofing, video kodlama | Ayrı proje alanları |
| 🆕 **GPSR** *(coğrafi yönlendirme)* | 🔴 **1 Eylül 2026'da kapsam dışına alındı.** İki gerekçe: *(a)* GPSR komşu **konumunu** ister; `05` §B konumu bedava vermiyor — beacon'a konup **bayt ödenmesi** gerekir, bu da kontrol düzlemi bütçesini değiştirir. *(b)* GPSR'nin asıl zafiyeti **GPS spoofing**'dir ve o zaten yukarıda kapsam dışı — yani GPSR konsa bile **en ilginç kırılganlığı ölçülemezdi** |
| Çok-etmenli oyun teorisi / MARL formalizmi | Kararsızlık riski yüksek |

> ⚠️ **Bu liste ÇÖZÜM KISITI DEĞİLDİR** — hangi çözümün kurulacağını
> söylemez, yalnızca hangi *alanların* kapsam dışı olduğunu söyler.

### 5.3 ⚠️ ÖLÇÜM ORTAMI — verilmemiş, ağır bir karar

Bu **çözüm kararı değil altyapı kararıdır**, ama sonuçları ağırdır ve
takvimin tamamını belirleyebilir. İlk oturumlarda açıkça ele alınmalıdır.

| Seçenek | Kazanç | 🔴 Başarısızlık modu |
|---|---|---|
| **Hazır ağ simülatörü** (NS-3, OMNeT++/INET) | Yerleşik protokoller · akademik saygınlık · hız | **Araç zinciri projeyi öldürür.** Windows'ta yerel destek sorunlu; öğrenme eğrisi tek başına pencerenin yarısını yiyebilir |
| **Kendi ölçüm ortamını yazmak** | Tam enstrümantasyon · her değişken senin · düşük öğrenme eğrisi | *"Kendi oyuncağını yazdı"* itirazı · yanlış modellenmiş bir ayrıntı |

> ⚖️ **Karar verirken RİSK ASİMETRİSİNE bak, ortalama sonuca değil.** Bir
> tarafın riski *"modelim biraz kaba"* (düzeltilebilir, dürüstçe
> raporlanabilir); diğerininki *"araç zinciri yüzünden aylar kaybedildi"*
> (kurtarılamaz).
>
> 🔴 **İkinci yol seçilirse `03` Bölüm D'deki dört seviyeli doğrulama
> yükümlülüğü ZORUNLU hâle gelir ve pazarlık konusu değildir.** Kendi ortamını
> yazmanın bedeli budur ve peşinen kabul edilmelidir.

### 5.2 ⚠️ Bir kısıt kutsal değildir

Bir kısıt ancak **gerekçesi ayakta olduğu sürece** bağlayıcıdır. Ölçüm bir
gerekçeyi çürütürse **kısıt değil gerekçe kazanır** ve revizyon karar kaydına
tarihiyle yazılır.

🔴 **Bunun kötüye kullanımı** *"sonuç beğenilmedi, kısıtı değiştir"*tir ve
yasaktır: revizyonu tetikleyen şey **ölçüm** olmalıdır.

---

## 6. BAŞARI ÖLÇÜTÜ — çözüm seçilmeden önce yazılır

| Seviye | Ölçüt |
|---|---|
| **Minimum kabul** | Doğrulanmış bir ölçüm ortamı + güçlü temel çizgiler + istatistiksel olarak anlamlı **herhangi** bir bulgu |
| **Dürüst başarısızlık** | Ana hipotez reddedilir, **ancak hangi koşulda ve ne kadar** başarısız olduğu **nicel olarak** gösterilir (üst sınırlarıyla) |
| **Hedef** | Ön-kayıtlı eşiği geçen, ablasyonla ayrıştırılmış bir kazanç |
| **Üstün** | Kazanç + o kazancın **hangi bilgi kanalından** geldiğinin ölçülerek gösterilmesi |

### 6.1 Her sonucun geçerlilik ön koşulu

Aşağıdaki dördü sağlanmayan hiçbir sonuç raporlanmaz:

1. Sonuç **koşu uzunluğundan bağımsız**
2. **Metriğin ne ölçtüğü** doğrulanmış
3. Karşılaştırılan taraflar arasında **gizli asimetri yok**
4. Sonucu üreten kodun **regresyon testi var**

---

## 7. SİMÜLASYON–GERÇEKLİK BEYANI *(rapora aynen girer)*

> Bu çalışma bir **kavram kanıtıdır**. Kullanılan yayılım ve karıştırma
> modelleri gerçek RF ortamının basitleştirilmiş temsilleridir. Elde edilen
> sayısal sonuçlar saha performansı öngörüsü olarak yorumlanmamalıdır;
> bulgular yalnızca modellenen koşullar altında **göreli** karşılaştırma
> olarak geçerlidir.

---

## 8. BU BELGENİN SÖYLEMEDİĞİ

Bilerek yazılmayanlar:

- Hangi algoritma, mekanizma veya mimari kurulacağı
- Hangi hipotezin test edileceği
- Hangi metriklerin öne çıkarılacağı
- Protokolün adı, başlığı, çerçevelemesi

**Bunların hepsi öğrenciyle birlikte, sıfırdan kurgulanacaktır.**
