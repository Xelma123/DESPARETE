# 03 — YÖNTEM KURALLARI

> ## ✅ GÜNCEL ve BAYATLAMAZ — 5 Eylül 2026
> ⭐⭐ Projenin en değerli belgesi. Sayı içermez, çözümden bağımsızdır ve
> `sim2/` yeniden yazımı da **bu kuralları uygulamak için** yapıldı.
> Yeni ajan `DEVIR.md`den sonra ilk bunu okur.


> ⭐⭐ **BU BELGE PROJENİN EN DEĞERLİ VARLIĞIDIR.**
>
> Aşağıdakiler bu alanda — karıştırma altındaki kablosuz ağ simülasyonu ve
> protokol karşılaştırması — çalışırken karşılaşılan **hata sınıflarıdır.**
> Her biri, "makul görünen" bir uygulamanın sessizce yanlış sonuç ürettiği bir
> durumu tarif eder.
>
> 🔴 **Bu belge ÇÖZÜMDEN BAĞIMSIZDIR.** Hangi çözüm kurulursa kurulsun,
> hangi metrik seçilirse seçilsin geçerlidir. **Sayı içermez** — sayılar bu
> projenin kendi ölçümlerinden gelecektir.

---

# BÖLÜM A — ASLA İHLAL EDİLMEYECEK KURALLAR

| # | Kural | Neden |
|---|---|---|
| **1** | **Ölçülmemiş bir şeyi ölçülmüş gibi sunma.** Her sayının yanında **üretici komut** ve **kaynak dosya** yazılır | Bir sayı bir kez yayımlandıktan sonra, onu üreten kod değişince sessizce bayatlar |
| **2** | **Tek/az tohumlu sonuç raporlama.** ≥30 tohum + güven aralığı | Simülasyonda tohumlar arası std, çoğu etkiden büyüktür |
| **3** | **Negatif sonucu gizleme.** Senaryoyu sonuç lehine değiştirme. **Eşiği geriye dönük gevşetme** | Ön-kayıtlı bir koşulun tek değeri, tetiklendiğinde ona uyulmasıdır |
| **4** | 🔄 **Straw-man rakip kurma.** Rakip, **mimarisine SADIK** kurulur: RFC'de ne varsa o, ne eksik ne fazla. 🔴 **Ve hiçbir kol — bizimki dâhil — senaryo başına ayarlanmaz** | Bir rakibi zayıflatmak, ona fazla cömert davranmaktan **daha kötü** bir hatadır. ⚠️ **1 Eylül 2026'da revize edildi — gerekçesi Bölüm A altında** |
| **5** | **Kâhin (oracle) özelliği kullanma** — simülatörün belleğinde olup gerçek donanımda ölçülemeyecek hiçbir şey karara giremez | Sinyal işleme bilen bir jüri üyesi bunu görür ve **tüm sonuçları geçersiz sayar** |
| **6** | **Git komutu çalıştırma.** `status` dahil | Depo öğrencinin; commit geçmişi fikir sahipliğinin kanıtıdır |
| **7** | **İşlemci bütçesi.** Çekirdeğin **yarısı** · süre tahminini **önce** yazdır · **30 dk'yı aşarsa SOR** | Makine öğrencinin; deney koşarken kullanılabilir kalmalı |
| **8** | **Kod yazmadan önce yapıyı anlat ve onay al** | Öğrenci anlamadığı kodu jüri karşısında savunamaz |
| **9** | **Derin öğrenme (DQN/PyTorch) önerme** | SWaP (boyut-ağırlık-güç) kısıtı gerçek; bağımlılık listesinde DL olmaması bir **özelliktir** |
| **10** | **Bir bulguyu "düşük öncelik" deyip düzeltmeden bırakma** | Bulmak ile düzeltmek arasındaki fark sıfır değildir |
| **11** | ⭐ **Bir ÖZGÜNLÜK İDDİASINI, onu üreten kod satırını ve ablasyon kolunu gösteremeden yazma** | Bir özellik tasarlanmış, belgelenmiş, hatta borulanmış olabilir — **ve hiç uygulanmamış** |
| **12** | **Sonuç beklentiyi tutmayınca parametre ayarlayıp tutturma.** Önce SEBEBİ ölç | Beklenmedik bir eğri, ayarlanacak bir hata değil, metriğin yanlış eksende olduğunun kanıtı olabilir |
| **13** | **Fiziksel sezgiyle çelişen bir sonucu, KURULUMU denetlemeden açıklamaya çalışma** | Literatürden makul bir hikâye uydurmak, kurulumu denetlemekten çok daha kolaydır |
| **14** | **Durum tutan yeni bir bileşeni BAŞLANGIÇ KOŞULUNU sormadan ekleme:** *t=0'da durağan mı, keyfi bir noktada mı?* | Isınma hataları bu alanın en sık ve en sinsi hata sınıfıdır |
| **15** | **Kod değişikliğini "başarılı" yazan bir betiğin çıktısına güvenme.** Değişikliği **kodda** doğrula | Eşleşmeyen bir `replace` sessizce hiçbir şey yapmaz ve betik yine "güncellendi" yazar |


## 🔄 KURAL 4'ÜN REVİZYONU — *"ayarlama"* değil *"sadakat"* *(1 Eylül 2026)*

**Eski hâli:** *"Rakip, ayarlanabildiği kadar iyi ayarlanır."*
**Yeni hâli:** *"Rakip, mimarisine sadık kurulur; hiçbir kol senaryo başına
ayarlanmaz."*

🔴 **Kuralın AMACI değişmedi** — rakibi zayıflatmamak. Değişen, o amaca
hangi yolla ulaşıldığı. Üç gerekçe:

| # | gerekçe |
|---|---|
| 1 | **Literatür bunu şart koşuyor:** *"RFC varsayılan değerlerini kullanın — özel optimize edilmiş değerler karşılaştırmayı bozar"* · *"Hello aralıklarını yapay olarak eşitlemeyin; bu protokollerin doğal davranışıdır"* |
| 2 | 🔴 **Senaryo başına ayarlamak bir KÂHİNLİKTİR.** Sahada AODV hangi senaryoda olduğunu bilmez. Her senaryoya ayrı ayarlanmış bir rakip, gerçekte var olmayan bir bilgiyle donatılmıştır — kural 5'in ihlali |
| 3 | **Ayarlama tartışılır, sadakat DENETLENEBİLİR.** *"Yeterince mi ayarladın?"* sorusunun sonu yoktur; *"RFC 3561 §6.3'e uyuyor mu?"* sorusunun cevabı vardır |

🔒 **VE KURAL SİMETRİKTİR — bu, revizyonun bedelidir:**

> **Kendi protokolümüz de ayarlanmaz.** Parametreleri mühürden **önce**
> sabitlenir ve ilan edilir. Rakip RFC varsayılanındayken bizimkini 50
> noktada taramak, kuralın yasakladığı şeyin ta kendisidir — yalnızca
> yönü ters.

⚠️ **Straw-man riski KAYBOLMADI, YER DEĞİŞTİRDİ.** Artık risk *"az
ayarladık"* değil, ***"eksik uyguladık"***. Panzehiri ayarlama taraması
değil, **uygunluk testleridir**: her rakip protokol, kabul edilmeden önce
davranışsal doğrulama testlerini geçmek zorundadır *(bağlı ağda teslim
oranı ≈ 1 · kopmada beklenen kontrol mesajının üretilmesi · yük deseninin
protokol ailesine uyması · olay izlerinin RFC ile karşılaştırılması)*.
Bir rakip *"kuruldu"* sayılmadan önce bu testleri geçer.

---

# BÖLÜM B — HATA SINIFLARI

## B1 · Ölçüm tasarımı

| Tuzak | Kaçınma |
|---|---|
| **Kontrol kolu olmadan etki ölçmek** | Etkinin **sıfır olması gereken** bir kol koymadan hiçbir etki ölçülmez |
| **"Mekanizma aktif" ile "mekanizma bilgi taşıyor"u karıştırmak** | Bir mekanizmanın çalıştığını göstermek, bilgi taşıdığını **göstermez.** Aynı yapısal etkiyi üreten ama bilgi taşımayan bir **null model** kur |
| **Null modeli fazla eşleştirmek** | *"Ne kadar çok eşleşirse o kadar iyi"* **yanlıştır**: yapıyı birebir eşleyen bir kontrol, bozması gereken kanalı da koruyabilir |
| **Ayarın kamuflaj olması** | Bir parametreyi metriğe göre ayarlarken, **mekanizmanın hâlâ çalıştığını ayrıca ölç.** "İyileşme", mekanizmayı fiilen kapatmaktan geliyor olabilir |
| **Mekanizma kapısını atlamak** | Önce *"mekanizma çalışıyor mu"* ölçülür; çalışmıyorsa sonuca **bakılmaz** |
| **Ablasyon kolunu kod düzenleyerek üretmek** | Bir ablasyon kolu **her zaman** bir konfigürasyon bayrağıdır. Kod düzenlemesiyle üretilen kol, kaynağından ayırt edilemez — **kaybolmuş bir deneydir** |
| **Ablasyonu yanlış yerden bölmek** | Tasarım metninin cümlelerinden değil, **mekanizma sınırlarından** böl |
| **Ayrıştırmanın gücü bölmesi** | *"Paket kaç tohumda anlamlı"* değil, ***"en küçük yarısı** kaç tohumda anlamlı"* diye sor |

## B2 · İstatistik

| Tuzak | Kaçınma |
|---|---|
| **Eşleştirmeyi yok saymak** | Ayrık RNG akışları kullanılıyorsa her protokol aynı tohumda **aynı senaryoyu** görür → örneklemler eşleştirilmiştir. Eşleştirmemek gücü boşa harcar |
| **Tek yönlü test** | Ters yöndeki bir bulguyu **tanım gereği göremez** — ve o bulgu en değerlisi olabilir |
| **Çoklu karşılaştırma düzeltmesi yapmamak** | Çok senaryolu bir ailede düzeltmesiz test, aile bazında yüksek yanlış pozitif oranı demektir (Holm-Bonferroni) |
| 🔴 **NaN'ın sessizce zehirlemesi** | `scipy.stats.wilcoxon` tüm farklar sıfırken **hata fırlatmaz, NaN döndürür**; `try/except ValueError` bunu **yakalamaz**. Tek bir NaN, düzeltilmiş p'lerin tümünü 1,00 yapar. ⚠️ Ve davranış **örneklem boyutuna bağlıdır** — küçük bir birim test geçer ve **yanlış güven verir** |
| **`nan`ı "etki yok" sanmak** | `nan` = *"ölçüm yok"*. Üst sınır verirken **kaç gözlemle** hesaplandığını da yaz |
| ⭐ **"Anlamsız çıktı" deyip bırakmak** | *"p > 0,05"* ile *"etki yok"* aynı şey değildir. **Negatif sonucun gücü, dışladığı etki büyüklüğündedir.** *"Bulamadık"* zayıf; *"şu büyüklükten fazlasını dışlıyoruz"* güçlüdür |
| **Gürültüden dar tarama** | Bir zayıflığın **yokluğunu** göstermek, aracın onu **görebilecek** kadar güçlü olmasını gerektirir. Taramanın genişliği tohum std'sinin altındaysa *"düz"* ile *"hiçbir şey söylemiyor"* ayırt edilemez |

## B3 · Metrikler

| Tuzak | Kaçınma |
|---|---|
| **Metrik gerçekten onu mu ölçüyor?** | Bir metrik tanım gereği sabit olabilir ve hiçbir bilgi taşımayabilir. **Yüke duyarlılığını ayrıca test et** |
| **Bir metrik, bir protokol sınıfı için geçersiz olabilir** | Tamponlayan bir protokol, tamponlamayanla aynı metrikte ölçülemeyebilir. İki çakışmayan olgu tek metriğe sıkışırsa **metriği ikiye ayır** |
| **Tek metrikle protokol sıralamak** | Bir protokol teslim oranında kazanıp gecikmede büyük fark kaybedebilir. **Üçlü sun:** teslim · gecikme · kontrol yükü |
| ⭐ **Seçilim yanlılığı (survivorship)** | Gecikme yalnızca **teslim edilenden** ölçülür; farklı başarı oranlı protokollerde bu tuzaktır. **Ortak alt küme** üzerinden karşılaştır ve kesişim oranını raporla |
| **Ölçüm penceresini koşu uzunluğuyla eşitlemek** | Isınma **asimetriktir** — protokoller farklı hızda yakınsar. Sonuç raporlarken **ölçüm penceresini** yaz |
| **Çalışma noktasını yazmamak** | Bir bulgu, ölçüldüğü çalışma noktasıyla birlikte yazılır; yoksa parametre değişince **sessizce yanlış olur** |
| ⚠️ **Yalnızca zorlayıcı noktada ölçmek** | Mobilite, tıkanıklık ve girişim protokoller arası farkı **bastırır** ve farkı **küçük gösterir.** Karşılaştırmanın **durağan bir referans noktası** da olmalı |
| **Kontrol yükünü paketle saymak** | **Bayt** cinsinden say; yoksa küçük çerçevelerle metrik manipüle edilir. Ve bir çerçeve doğuyorsa **çift faturalama** riskine dikkat |

## B4 · Teşhis

| Tuzak | Kaçınma |
|---|---|
| ⭐⭐⭐ **Bir kusuru ölçmek, onu SEBEP yapmaz** | Ölçülebilen her kusur, gözlenen sonucun sebebi değildir. **Kusur ile sonuç arasında nedensel bir kol kur** |
| **Kusurların birbirini dengelediğini görmemek** | Bir "patoloji"yi düzeltmek **zarar verebilir** — o patoloji sessizce başka bir işi görüyor olabilir. **Düzeltmeden önce ne işe yaradığını sor** |
| ⭐ **Düzeltmenin bedelinin kusurdan büyük olabilmesi** | Ders kitabına göre doğru bir düzeltme, bağlayıcı kısıt başka olduğu için zarar verebilir |
| **Ablasyona yalnızca sonucu sormak** | Hem **sonucu** hem **mekanizmayı** sor. İkisinin ayrıştığı yer bilginin bulunduğu yerdir |
| **Kör mekanizma ölçütü** | Bir yol tamamen değişip aynı atlama sayısını koruyabilir. **Ölçütün, sorduğun soruya duyarlı olduğunu ayrıca doğrula** |
| **Daraltmayan deney** | Bir eleme bir sonrakini daraltmalı. Neyi eleyeceğini önceden söyleyemiyorsan **koşma** |
| ⭐ **Kodun kendisini denetlememek** | Açıklamalar tükendiyse **kod ile tasarım belgesini yan yana koy.** Belgede olan bir özellik kodda olmayabilir |

## B5 · Kod ve belge

| Tuzak | Kaçınma |
|---|---|
| 🔴 **Bildirim ≠ kullanım** | Bir bileşen bildirilmiş, parametre olarak geçirilmiş ve belgelenmiş olabilir — **ve hiç çağrılmamış.** Bildirilen her şeyin gerçekten tüketildiğini **test et** |
| 🔴 **Yorumun kodla çelişmesi** | İkisinden de kötüdür. **Belge, kodun kanıtı değildir; kod, belgenin kanıtıdır** |
| **Şemanın kaybolması** | Bir sonuç dosyasının **şeması**, onu hangi kodun ürettiğini söyleyen tek kanıttır. Bayrak yoksa o satır **yeniden üretilemez** |
| ⭐ **Etiketi elle taşımak** | Yeni bir mekanizma varsayılan açıldığında, onu **kullanan** her ayrıştırmanın etiketi de değişmiş olabilir. Elle yazılan etiket **sessizce yanlışlaşır** |
| ⭐ **Yargıyı elle yazmak** | Yargı ve sayı **veriden çıkmalı.** Beklenen sonucu basan bir analiz fonksiyonu, ölçümü süsleme aracına çevirir |
| **Analiz kodunu hafife almak** | **Yanlış sayı, çalışmayan koddan daha tehlikelidir çünkü sessizdir.** Analiz kodunu üretim kodu kadar ciddiye al ve karar üreten yüklemlerini **ayrı ve test edilebilir** yaz |
| **Kapsam yüzdesine güvenmek** | Kapsam, doğruluğun ölçüsü **değildir** |
| **Göreli sonuç yolu** | Çağıranın çalışma dizinine yazar. Yolları **depo köküne** mutlakla |
| **Geçersizlik iddiasını varsaymak** | *"Her şeyi yeniden koş"* demek kolaydır ve saatlere mal olur. **Geçersizlik de ölçülür** |
| **Ara kayıt tutmamak** | Uzun bir matris yarıda kesilirse tamamlanan koşular kaybolur. Her satırı **anında** diske yaz |

## B6 · Kurulum hataları — en sinsi sınıf

| Tuzak | Kaçınma |
|---|---|
| ⭐⭐⭐ **Kod doğru, testler geçiyor, kapsam yüksek — ve kurulum yanlış** | Bu sınıf sıradan kod incelemesiyle **bulunamaz.** Bir mobilite modelinin durağan dağılımı düzgün değilken başlangıç konumları düzgün çekilirse, her koşu bir geçiş rejiminde başlar ve o geçişin ilerlemesi **taranan parametreye bağlı** olur → tarama **sessizce başka bir şeyi ölçer** |
| **Rezonans** | İki periyodik süreç aynı periyottaysa biri diğerini **hep aynı fazda** görür. Periyotları eşit bırakma ya da faz rastgeleleştir |
| **Örtüşme (aliasing)** | Örnekleme aralığı bir periyodu **tam bölerse** örnekler kilitlenir ve tohumlar arası varyans yapay olarak sıfıra iner |
| **Düzeltmenin yönünü tahmin etmek** | Bir hatayı düzeltince etkisi tahmin ettiğin yönde olmayabilir. **Bozuk bir kurulumun içinden yapılan ekstrapolasyon da bozuktur** |
| **Sahte host / mock'un ölçüleni yutması** | Bir test ikizi, tam da ölçmek istediğin şeyi devre dışı bırakabilir. **Entegrasyon değişmezleri gerçek sistemle sınanır** |

---

# BÖLÜM C — ZORUNLU ALTYAPI SÖZLEŞMELERİ

Hangi çözüm kurulursa kurulsun bunlar kurulmalıdır — **sonradan eklenemezler.**

| Sözleşme | Ne | Neden sonradan eklenemez |
|---|---|---|
| **Gözlem sözleşmesi** | Karar katmanının görebileceği alanlar **açıkça listelenir** ve simülatöre geri referans **taşımaz** | Sonradan daraltmak, tüm önceki ölçümleri geçersiz kılar |
| **Ayrık RNG akışları** | Her rastgelelik kaynağı **kendi akışını** kullanır | Tek akış, protokolleri farklı senaryolarda ölçer; 30 tohum bunu kurtarmaz |
| **Korunum denklemi** | `üretilen = teslim + düşen + kuyrukta + uçuşta`, **her koşuda otomatik** | Sessiz paket kaybı en zor bulunan hata sınıfıdır |
| **Ölçüm penceresi** | Isınma ayrı, ölçüm ayrı; **tüm sayaçlar aynı pencereden** | Asimetrik ısınma, sonucu koşu uzunluğuna bağımlı kılar |
| **Sonuç + konfigürasyon birlikte** | Her sonuç **kendi tam konfigürasyonuyla** saklanır | Aylar sonra *"bu sayı hangi parametrelerle çıktı"* sorusu cevapsız kalır |
| **Karar kaydı** | Her önemli karar: *tarih · alternatifler · neden bu · neden diğerleri elendi · bunu ne değiştirirdi* | Fikir sahipliği ancak tarihli kayıtla kanıtlanır |

---

# BÖLÜM D — SİMÜLATÖR DOĞRULAMA YÜKÜMLÜLÜĞÜ

Kendi ölçüm ortamını yazmanın **tek gerçek zayıflığı** şudur:

> *"Öğrenci kendi oyuncağını yazdı; sonuçlarına nasıl güveneceğiz?"*

Bu itiraz **meşrudur ve önlenebilir.** Önleme yolu dört seviyelidir ve
**pazarlık konusu değildir:**

| # | Seviye | Ne yapar |
|---|---|---|
| 1 | **Analitik doğrulama** | Bilinen kapalı-form sonuçlarla karşılaştırma (yol kaybı, gürültü tabanı, çerçeve süreleri, sönümleme momentleri) |
| 2 | **Korunum kontrolleri** | Hiçbir birim sessizce kaybolmuyor — her koşuda otomatik |
| 3 | **İç tutarlılık** | Uç durumlarda beklenen davranış; aynı tohum → bit-birebir aynı sonuç |
| 4 | ⭐ **Literatür replikasyonu** | **Yayınlanmış bir sonucu yeniden üret.** Birebir çakışma gerekmez; **nitel eğilimin aynı olması** ve farkın gerekçelendirilmesi yeterlidir |

> ⭐ Dördüncüsü, projeyi *"bir öğrenci simülasyon yazdı"*dan *"bir öğrenci bir
> araştırma aracı geliştirdi ve doğruladı"*ya taşıyan adımdır.
>
> ⚠️ Ve bir replikasyon **ilk denemede başarısız olursa** bu bir kayıp değil,
> raporun en güçlü bölümlerinden biri olabilir — **eğer sebebi bulunup
> yazılırsa.** Eğriye parametre ayarıyla uydurmak yerine nedenini bulmak,
> yöntem olgunluğunun en görünür kanıtıdır.

---

# BÖLÜM E — ÇALIŞMA BİÇİMİ

### Oturum şablonu
```
1. KONUM      : Neredeyiz, takvim durumu
2. HEDEF      : Bu oturumda ne bitecek (tek, net çıktı)
3. YAPI       : Ne yazılacak, neden, arayüzü ne — ONAY BEKLENİR
4. UYGULAMA   : Kod (yalnızca onaydan sonra)
5. DOĞRULAMA  : Nasıl test edildi, korunum geçti mi
6. RAPOR BAĞI : Raporun neresine giriyor
7. SONRAKİ    : Sonraki adım + yeni risk
```

### Bir modül ne zaman "bitmiş" sayılır — dördü birden gerekir
1. Hata geri gelirse yakalayacak **regresyon testi**
2. **Başlangıç koşulu** açıkça sorulmuş
3. **Metriğin ne ölçtüğü** doğrulanmış
4. Değişiklik **kodda** doğrulanmış (betik çıktısına güvenilmez)

### Danışmanın reddedeceği şeyler
Talep edilirse **önce itiraz edilir**; ısrar edilirse karara uyulur ve itiraz
kayda geçer:

- Simülatörden sızan bir bilgiyi karara koymak
- Tek tohumlu sonuç raporlamak
- Bir rakibi **eksik uygulayıp** *"geçtik"* demek *(uygunluk testleri geçilmeden)*
- Kendi kolumuza rakibe verilmeyen bir **ayarlama bütçesi** vermek
- Tek metriğe bakıp protokol sıralamak
- Negatif sonucu gizlemek
- Yazım döneminde yeni deney başlatmak
- Bir bulguyu *"düşük öncelik"* deyip bırakmak

### Öğrenci hakkında
- **Tam zamanlı çalışıyor.** Acele yok ama takvim disiplini var
- **Pasif bir proje istemiyor:** *"şunları test ettik"* değil, *"şunu tasarladık"*
- ⭐ **Doğrulama konusunda ısrarcı** ve bu ısrar defalarca haklı çıktı
- **Kararlar onundur.** Danışman **seçenekleri ve ölçüm yöntemini** sunar. Bir
  kararı sana devrederse, kararı ver **ama devredildiğini açıkça kaydet**

---

> **Bir şeyi büyütmek istiyorsan önce ölç.**
