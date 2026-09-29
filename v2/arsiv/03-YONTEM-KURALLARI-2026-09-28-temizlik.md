# 03 · YÖNTEM İLKELERİ VE HATA SINIFLARI

> **Güncel:** 25 Eylül 2026 · **Türü:** bilgi belgesi — bu alanın hata
> sınıfları ve onlara karşı bu projede işe yarayan alışkanlıklar. Önceki
> sürümler `v2/arsiv/03-YONTEM-KURALLARI-*.md`.

## 0 · Nasıl okunur

Burada yazanlar, "makul görünen" bir uygulamanın **sessizce yanlış sonuç**
ürettiği durumlardır; çoğu bu projede yaşandı. Bir pusuladır, kural listesi
değil: ilke bir durumda yanlış görünüyorsa gerekçesi okunur, durum
**ölçülür**, sonuç `04`e yazılır (böyle düzeltilenler: rakip ayarlama ilkesi,
karıştırıcı eşitleme K-103, "tavan" kâhini K-110). Körü körüne uygulamak da
gerekçesini okumadan atmak da hatadır — önceki ajanların ortak kusuru fazla
itaatti (öğrenci, 9 Eylül). Sorgulama ölçümle biter.

---

## 1 · Çalışma anlaşmaları

Bunlar bilimsel ilke değildir; öğrencinin makinesinden, deposundan ve onunla
yapılan anlaşmalardan gelir.

| anlaşma | neden |
|---|---|
| `git` komutlarını **yalnız öğrenci** çalıştırır — salt-okur olanlar (`status`, `log`, `ls-files`) dâhil. Depoda 23 Eylül 2026'dan beri git var; kural değişmedi | depo ve commit geçmişi öğrencinin; fikir sahipliğinin kanıtı |
| Öğrenciyle Türkçe konuşulur; özetler kısa olur ve kod referansı içermez | öğrenci kararları okur, kodu değil |
| `sim2/` içinde yapısal bir değişiklikten önce yapı anlatılır ve onay alınır. Ölçüm betikleri ve belgeler bunun dışındadır | öğrenci anlamadığı kodu jüri önünde savunamaz |
| 30 dakikayı aşacağı tahmin edilen bir koşumdan önce sorulur; süreler bant olarak verilir | makine öğrencinin; deney koşarken kullanılabilir kalmalı |
| Kapsam ve gerçekçilik kararları öğrencinindir. Ajana devredilen bir karar, devredildiği yazılarak verilir | projenin yönü öğrencinin |
| Raporlanan her sayının yanında onu üreten komut yazılır | kod değişince sayı sessizce bayatlar; komut olmadan bu yakalanamaz |
| 🔴 **Sorunu ajan çözer:** bir kusur bulununca çözülür, ölçülür (beklenti ölçmeden önce yazılır), kaydedilir ve kanıtıyla getirilir — yalnız raporlanıp seçenek sunularak beklenmez. DESPARETE "yapım aşamasında"dır; geliştirilmesi ajana bırakıldı (25 Eylül). Öğrenciye yalnız fikrinin değiştiği yerlerde (kapsam, iddia, ön-kayıt metriği) öneriyle sorulur; ajan katkısı kayıtta "ajan" diye etiketlenir. Çözülemiyorsa ne denendiği ve nerede tıkanıldığı yazılır | öğrencinin açık beklentisi: *"sorunları çözmeyi ve protokolü neden geliştirmeye çalışmıyorsun"* |
| 🔴 **Öz yaz, kısa ölç:** aynı bilgi tek yerde, ötekiler atıf verir; belgelerin tam önceki hâli arşive gider. Bir koşu yalnız bir kararı değiştirecekse ve en az tohum/süre/kolla koşulur; tam test takımı iş sonunda bir kez (25 Eylül) | *"bağlam sorunu … testler ve ölçümler hem çok uzun hem de çoğu zaman gereksiz"* |
| 🔴 **Bir iş BİTİRİLİR, sonra ölçülür.** Uzun kapı koşumları iş sürerken tekrar tekrar koşulmaz; işin kapanışında **bir kez** koşulur (öğrenci kararı, 17 Eylül 2026) | ara koşumlar donanımı saatlerce meşgul eder ve sayıları havada bırakır: hangi tablonun hangi kod hâline ait olduğu kaybolur. Ayrıca kod değişmeye devam ettiği için o tablo zaten yeniden koşulacaktır |
| 🔴 **Protokoller sırayla kapatılır.** Bir protokol yazılır → entegre edilir → ölçülür → sorunları düzeltilir → *bitti* denir; ancak sonra sıradakine geçilir | paralel yürüyen iki yarım protokol, birinin kusurunu diğerinin ölçümüne karıştırır |
| 🔴 **Ağır koşumda makine kullanılabilir kalır:** havuz varsayılanı **8 işçi** (öğrenci, 21 Eylül 2026: *"8 çekirdeğini kullanabilirsin"*; 17 Eylül'de 4 idi). Makine i5-13420H — **8 fiziksel çekirdek** (4 performans + 4 verimlilik), 12 mantıksal iş parçacığı. 8'i aşan varsayılanlar (dört alette 10) 8'e indirildi | öğrencinin tek makinesi var ve koşum sırasında onu kullanabilmeli. ⚠️ Verimlilik çekirdekleri daha yavaş: 4 → 8 işçinin kazancı 2 kattan az |
| 🔴 **Dosya kalıcı olarak SİLİNMEZ; eskiyen belge arşive TAŞINIR** (öğrenci, 23 Eylül 2026 — temizliğin amacı bağlam kirliliğini önlemek) | tarih, bir kararın neden verildiğinin hafızasıdır. (Kural konduğunda depoda git yoktu ve silinen geri gelmezdi; git gelince de kural değişmedi — arşiv ve çıktılar git'in DIŞINDA tutuluyor) |

**Ortamın fiziği (Windows):** her Python çağrısında `PYTHONIOENCODING=utf-8`
ve `PYTHONDONTWRITEBYTECODE=1` (bazı `__pycache__/*.pyc` git'te izleniyor;
Python koşmak depoyu değiştirir); `Pool` kullanan betikte
`if __name__ == "__main__":`; iç içe havuz yok; depoda satır sonları
karışık (CRLF/LF) ve korunur — denetim bayt düzeyinde. 🔓 27 Eylül 2026
(öğrenci): sonucu etkilemeyen biçim tercihleri (`python -c`, stdin'den
Python, heredoc) serbesttir; *"çok önemli kurallar olmadıkça daha rahat
ol"*.

---

## 2 · Bilimsel ilkeler

| # | ilke | neden | nerede esner |
|---|---|---|---|
| 1 | **Ölçülmemiş bir şey ölçülmüş gibi sunulmaz.** Sayı, üretici komutu ve kaynak dosyasıyla yazılır | yayımlanan bir sayı, onu üreten kod değişince sessizce bayatlar | — |
| 2 | **Sonuç çok tohumla verilir.** Ana deney **40 tohum** (öğrenci, 10 Eylül 2026) + güven aralığı; tohum sayısının yeterliliği güç analiziyle sınanır | tohumlar arası yayılım çoğu etkiden büyüktür | keşif ve kalibrasyon ölçümleri daha az tohumla yapılabilir; kaç tohumla yapıldığı yazılır |
| 3 | **Negatif sonuç gizlenmez.** Senaryo sonuç lehine değiştirilmez; bir eşik sonuç görüldükten sonra gevşetilmez | ön-kayıtlı bir koşulun tek değeri, tetiklendiğinde ona uyulmasıdır | ölçüm bir ölçütün **sınanamaz** olduğunu gösterirse ölçüt düzeltilebilir: düzeltme tarihli yazılır, eski hâl silinmez, sonuç eskisiyle birlikte raporlanır (örnek: K-105 G2) |
| 4 | **Rakip mimarisine sadık kurulur; hiçbir kol senaryoya göre ayarlanmaz — kendi protokolümüz dâhil** | senaryo başına ayar bir kâhinliktir; sadakat denetlenebilir, "yeterince ayarlandı mı" denetlenemez | RFC'nin tanımlamadığı yerlerde (ör. MAC ile etkileşim) seçim yapılır ve gerekçesiyle yazılır. Straw-man riski artık "eksik uygulama"dadır; panzehiri uygunluk testleridir (`06` §4) |
| 5 | **Kâhin bilgisi karara girmez.** Simülatörün bildiği ama gerçek bir telsizin ölçemeyeceği hiçbir şey protokol kararına giremez | sinyal işleme bilen bir jüri üyesi bunu görür ve tüm sonuçları geçersiz sayar | kâhinler **ölçüm aleti ve referans** olarak kullanılır, protokolün girdisi olarak asla. Sınır `05`te |
| 6 | **Derin öğrenme kullanılmaz** (öğrenci kararı) | SWaP kısıtı gerçek; bağımlılık listesinde DL olmaması bir özelliktir | tablo tabanlı öğrenme bu kapsamda değildir |
| 7 | **Özgünlük iddiası, onu üreten kod ve ablasyon kolu gösterilerek yazılır** | bir özellik tasarlanmış, belgelenmiş, hatta borulanmış olup hiç uygulanmamış olabilir | — |
| 8 | **Beklenmeyen sonuçta önce sebep ölçülür;** parametre oynatılıp sonuç tutturulmaz. Fiziksel sezgiyle çelişen bir sonuçta önce kurulum denetlenir | beklenmedik bir eğri, metriğin yanlış eksende olduğunun kanıtı olabilir; literatürden hikâye uydurmak kurulumu denetlemekten kolaydır | — |
| 9 | **Durum tutan her bileşende başlangıç koşulu sorulur:** t = 0'da durağan mı, keyfî bir noktada mı? | ısınma hataları bu alanın en sık ve en sinsi hata sınıfıdır | — |
| 10 | **Bir değişiklik kodda ve çıktıda doğrulanır** | eşleşmeyen bir değiştirme sessizce hiçbir şey yapmaz ve betik yine "güncellendi" yazar | — |
| 11 | **Bulunan bir sorun "düşük öncelik" diye bırakılmaz;** ya düzeltilir ya tarihiyle ve sınıfıyla borç listesine yazılır | bulmak ile düzeltmek arasındaki fark sıfır değildir | — |

### 2.1 Bu projede işe yarayan düşünme alışkanlıkları

- **Bir ölçüm aletine, ölçtüğü şeye güvendiğinden daha az güven.** Bulunan
  kusurların çoğu modelde değil aletlerdeydi; hepsini yakalayan başka bir
  kapı oldu (K-109).
- **Tabloda değişmeyen sütuna bak.** 20 dB güç farkına rağmen aynı çıkan
  satırlar, kapalı bir karıştırıcıyı ölçüyordu (8 Eylül).
- **"Bu sayıyı ürettiği yazılan komut hâlâ koşuyor mu?"** Dört üretici
  kırıktı ve sayılar yine de doğruydu (K-111).
- **Muhasebede ödenen bedel kanalda da ödeniyor mu?** Beacon yükü sayaca
  yazılıyor ama çerçeveyi uzatmıyordu (K-111).
- **"Ölçtüm, etkisi yok" (DUYARSIZ) ile "bu kolda hesaba girmedi"
  (ÖLÇÜLEMEDİ) ayrıdır.** İkincisini birincisi sanmak gerekçesiz bir sayıyı
  aklar.
- **Bir alt sınır, bir değerin gerekçesi değildir** (K-110, TTL).
- **Gürültü üreten kapı bozuktur.** Doğru işi kırmızıya boyayan bir kapı
  insanları kapıyı görmezden gelmeye alıştırır.
- **Yeni bir kapı eklendiğinde "ne kırıldı" değil, "ne hâlâ geçiyor ama artık
  hiçbir şey doğrulamıyor" diye sorulur** (K-103).
- **Öğrencinin verdiği sayılar yaklaşık değerlerdir;** cevabı ölçüm verir.
  Kapsam ve gerçekçilik ise öğrencinindir.
- **Bir kapının "X yapmaz" sonucunu sınarken X'e bağlı kapıları da sor.**
  "Geçit kimseyi nitelendirmez" testi yazıldı; geçidin istek kabulünün
  nitelik istediği sorulmadı (K-166).
- **Kısa pencere zamanla biriken etkiyi göremez.** 40 s'de önde görünen
  profil 300 s'de geride çıktı (K-166); profil kararları uzun pencerede,
  geliştirme tohumlarında verilir.

---

## 3 · Hata sınıfları — bilgi bankası

### B1 · Ölçüm tasarımı

| tuzak | kaçınma |
|---|---|
| Kontrol kolu olmadan etki ölçmek | Etkinin sıfır olması gereken bir kol olmadan etki ölçülmez |
| "Mekanizma aktif" ile "mekanizma bilgi taşıyor"u karıştırmak | Aynı yapısal etkiyi üreten ama bilgi taşımayan bir null model kurulur |
| Null modeli fazla eşleştirmek | Yapıyı birebir eşleyen bir kontrol, bozması gereken kanalı da koruyabilir |
| Ayarın kamuflaj olması | Bir parametre metriğe göre ayarlanırken mekanizmanın hâlâ çalıştığı ayrıca ölçülür; "iyileşme" mekanizmayı kapatmaktan geliyor olabilir |
| Mekanizma kapısını atlamak | Önce "mekanizma çalışıyor mu" ölçülür; çalışmıyorsa sonuca bakılmaz |
| Ablasyon kolunu kod düzenleyerek üretmek | Ablasyon kolu bir konfigürasyon bayrağıdır; kod düzenlemesiyle üretilen kol kaynağından ayırt edilemez |
| Ablasyonu yanlış yerden bölmek | Tasarım metninin cümlelerinden değil, mekanizma sınırlarından bölünür |
| Ayrıştırmanın gücü bölmesi | "Paket kaç tohumda anlamlı" değil, "en küçük yarısı kaç tohumda anlamlı" diye sorulur |

### B2 · İstatistik

| tuzak | kaçınma |
|---|---|
| Eşleştirmeyi yok saymak | Ayrık rastgelelik akışları varsa aynı tohum = aynı senaryo; örneklemler eşleştirilmiştir |
| Tek yönlü test | Ters yöndeki bulguyu tanım gereği göremez — ve o bulgu en değerlisi olabilir |
| Çoklu karşılaştırma düzeltmesi yapmamak | Aile içinde Holm–Bonferroni |
| NaN'ın sessizce zehirlemesi | `scipy.stats.wilcoxon` tüm farklar sıfırken hata fırlatmaz, NaN döndürür; tek bir NaN düzeltilmiş p'lerin hepsini 1,00 yapar. Davranış örneklem boyutuna bağlıdır: açık kontrol ve gerçek n ile regresyon testi |
| `nan`ı "etki yok" sanmak | `nan` = ölçüm yok. Üst sınır verirken kaç gözlemle hesaplandığı yazılır |
| "Anlamsız çıktı" deyip bırakmak | *"p > 0,05"* ile *"etki yok"* aynı şey değildir; negatif sonucun gücü dışladığı etki büyüklüğündedir |
| Gürültüden dar tarama | Bir zayıflığın yokluğunu göstermek, aracın onu görebilecek güçte olmasını gerektirir |
| Sınanamaz ölçüt | Gerçek değeri eşit iki nokta gürültüyle yarı yarıya "düşüş" gösterir; "artış/azalış" hata payıyla okunur (K-105) |
| Sınırda çöken hata payı | Wald SE, p = 1'de sıfırdır ve bu projede p = 1 sık görülür; Agresti–Caffo (K-105) |
| Çok pencereli taramada yanlış alarm | Pencere başına α, pencere sayısı kadar tekrarlanınca toplam yanlış alarm oranı büyür (`08` §05.3) |

### B3 · Metrikler

| tuzak | kaçınma |
|---|---|
| Metrik gerçekten onu mu ölçüyor? | Bir metrik tanım gereği sabit olabilir; yüke duyarlılığı ayrıca test edilir |
| Bir metrik bir protokol sınıfı için geçersiz olabilir | Tamponlayan ve tamponlamayan protokol aynı metrikte ölçülemeyebilir; gerekirse metrik ikiye ayrılır |
| Tek metrikle protokol sıralamak | Üçlü sunulur: teslim · gecikme · kontrol yükü |
| Seçilim yanlılığı | Gecikme yalnız teslim edilenden ölçülür; karşılaştırma ortak alt küme üzerinden yapılır ve kesişim oranı yazılır |
| Ölçüm penceresini koşu uzunluğuyla eşitlemek | Isınma asimetriktir; ölçüm penceresi yazılır |
| Çalışma noktasını yazmamak | Bulgu, ölçüldüğü çalışma noktasıyla birlikte yazılır |
| Yalnız zorlayıcı noktada ölçmek | Mobilite, tıkanıklık ve girişim farkları bastırır; durağan bir referans nokta da olur |
| Kontrol yükünü paketle saymak | Bayt ve kanal süresi cinsinden sayılır; çift faturalamaya dikkat edilir |
| Bir kâhini kesin tavan sanmak | ETX beklenen iletim sayısını küçültür, teslimi değil; kâhin bir referanstır, sınırı ölçülerek beyan edilir (K-110) |

### B4 · Teşhis

| tuzak | kaçınma |
|---|---|
| Bir kusuru ölçmek onu sebep yapmaz | Kusur ile sonuç arasında nedensel bir kol kurulur |
| Kusurların birbirini dengelediğini görmemek | Bir "patolojiyi" düzeltmeden önce ne işe yaradığı sorulur |
| Düzeltmenin bedelinin kusurdan büyük olabilmesi | Bağlayıcı kısıt başka yerdeyse ders kitabı düzeltmesi zarar verebilir |
| Ablasyona yalnız sonucu sormak | Hem sonuç hem mekanizma sorulur; ayrıştıkları yer bilginin olduğu yerdir |
| Kör mekanizma ölçütü | Ölçütün sorulan soruya duyarlı olduğu ayrıca doğrulanır |
| Daraltmayan deney | Neyi eleyeceği önceden söylenemeyen deney koşulmaz |
| Kodun kendisini denetlememek | Kod ile tasarım belgesi yan yana konur; belgede olan kodda olmayabilir |

### B5 · Kod ve belge

| tuzak | kaçınma |
|---|---|
| Bildirim ≠ kullanım | Bildirilen her şeyin gerçekten tüketildiği test edilir |
| Yorumun kodla çelişmesi | Belge kodun kanıtı değildir; kod belgenin kanıtıdır |
| Şemanın kaybolması | Sonuç dosyasının şeması, hangi kodun ürettiğinin kanıtıdır |
| Etiketi elle taşımak | Yeni bir mekanizma varsayılan açıldığında onu kullanan her ayrıştırmanın etiketi değişmiş olabilir |
| Yargıyı elle yazmak | Yargı ve sayı veriden çıkar; beklenen sonucu basan analiz, ölçümü süsler |
| Analiz kodunu hafife almak | Yanlış sayı çalışmayan koddan tehlikelidir, çünkü sessizdir |
| Kapsam yüzdesine güvenmek | Kapsam doğruluğun ölçüsü değildir |
| Göreli sonuç yolu | Yollar depo köküne göre mutlaklanır |
| Geçersizlik iddiasını varsaymak | "Her şeyi yeniden koş" demek yerine geçersizlik de ölçülür |
| Ara kayıt tutmamak | Her satır anında diske yazılır |
| Aynı kuralı iki yerde yazmak | İki kopya bir gün ayrışır; kural tek kaynağa bağlanır (K-109, K-110) |

### B6 · Kurulum hataları — en sinsi sınıf

| tuzak | kaçınma |
|---|---|
| Kod doğru, testler geçiyor — kurulum yanlış | Durağan dağılımı düzgün olmayan bir modelde düzgün başlangıç gibi hatalar sıradan incelemeyle bulunmaz; tarama sessizce başka şeyi ölçer |
| Rezonans | İki periyodik süreç aynı periyottaysa biri diğerini hep aynı fazda görür |
| Örtüşme (aliasing) | Örnekleme aralığı bir periyodu tam bölerse örnekler kilitlenir |
| Düzeltmenin yönünü tahmin etmek | Bozuk bir kurulumun içinden yapılan ekstrapolasyon da bozuktur |
| Sahte host / mock'un ölçüleni yutması | Entegrasyon değişmezleri gerçek sistemle sınanır |
| Kapalı durumu ölçmek | Bir karıştırıcı ya da mekanizma ölçüm anında kapalıysa tablo canlı görünür ama hiçbir şey ölçmez; ön koşul kapıyla sınanır (K-104) |

---

## 4 · Altyapı sözleşmeleri — simülatörde nasıl uygulandıkları

| sözleşme | ne | nerede |
|---|---|---|
| gözlem sözleşmesi | protokolün görebileceği alanlar açıkça listelenir; simülatöre geri referans yoktur | `05` · yüzey taraması testi |
| protokolün yapabilecekleri | protokol çağırmaz, niyet döndürür; bedel kanalda ödenir | `13` · P1–P8 |
| ayrık rastgelelik | durum tutan kaynaklar için sıralı akışlar; kanal için protokolden bağımsız hash alanları | çekirdek rastgelelik modülü |
| korunum | `üretilen = teslim + düşen + kuyrukta + uçuşta`, her koşuda; ayrıca mutabakat | çekirdek korunum defteri |
| ölçüm penceresi | ısınma ayrı; sayaçların pencere ikizleri otomatik türer | çekirdek sayaç kütüğü |
| sonuç satırı | her satır kendi konfigini, kapsam sınırlarını ve metrikleri yeniden üretecek ham veriyi taşır | koşum sonuç modülü |
| köken defteri | her parametre yedi kovadan birinde: TÜRETİLMİŞ · ÖLÇÜLMÜŞ · KAYNAK · DUYARSIZ · TEDAVİ · KOL TANIMI · SINANMAMIŞ | `07` §11 |
| karar kaydı | tarih · alternatifler · neden bu · bunu ne değiştirir | `04` |

---

## 5 · Simülatör doğrulama seviyeleri

Kendi ölçüm ortamını yazmanın meşru itirazı şudur: *"Öğrenci kendi oyuncağını
yazdı; sonuçlarına nasıl güveneceğiz?"* Cevabı dört seviyedir:

| # | seviye | ne yapar |
|---|---|---|
| 1 | analitik doğrulama | kapalı-form sonuçlarla karşılaştırma (yol kaybı, gürültü tabanı, çerçeve süreleri, sönümleme momentleri, Bianchi) |
| 2 | korunum kontrolleri | hiçbir birim sessizce kaybolmaz — her koşuda otomatik |
| 3 | iç tutarlılık | uç durumlarda beklenen davranış; aynı tohum → birebir aynı sonuç |
| 4 | literatür replikasyonu | yayımlanmış bir sonucu yeniden üretmek; nitel eğilimin aynı olması ve farkın ölçülerek açıklanması yeterli |

Dördüncüsü, *"bir öğrenci simülasyon yazdı"*yı *"bir öğrenci bir araştırma
aracı geliştirdi ve doğruladı"*ya taşır. Bir replikasyonun tutmaması, sebebi
bulunup yazılırsa raporun en güçlü bölümlerinden biri olabilir (`09`).
Güncel durum: `07` §10.

---

## 6 · Oturum biçimi (öneri)

```
KONUM → HEDEF → YAPI (sim2 değişikliğinde onay) → UYGULAMA → DOĞRULAMA → SONRAKİ
```

Bir modülün "bitti" sayılması için: hatayı yakalayacak bir regresyon testi,
sorulmuş bir başlangıç koşulu, metriğin ne ölçtüğünün doğrulanması ve
değişikliğin kodda doğrulanması.

---

## 7 · Öğrenci hakkında

- **Tam zamanlı çalışıyor;** takvim disiplini var (Aşama 1–2 planın önünde
  bitti).
- **Pasif bir proje istemiyor:** *"şunları test ettik"* değil, *"şunu
  tasarladık"*.
- **Doğrulama konusunda ısrarcı** ve bu ısrar defalarca haklı çıktı.
- **Ajanlardan serbest düşünmelerini ve sorunları çözmelerini istiyor** —
  raporlayıp beklemelerini değil (25 Eylül).
- **Bağlam ve zaman ekonomisi istiyor:** öz belgeler, kısa ve gerekli
  ölçümler (25 Eylül).
- **Kapsam, iddia ve ön-kayıt kararları onundur.** Danışman bunlarda
  önerisini ve ölçümünü sunar.

> **Bir şeyi büyütmek istiyorsan önce ölç.**
