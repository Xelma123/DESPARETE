# 07 · SİMÜLATÖR TASARIMI — nihai şartname

> **Tarih:** 8 Eylül 2026 · **Durum: TASLAK — öğrenci onayı bekliyor**
> Bu belge, simülatörün ne olacağını **kod yazılmadan önce** kararlaştırır.
> Mevcut `sim2/` bu belgeye göre **refactor edilecek**, baştan yazılmayacak.

---

## 00 · BU BELGE NEDEN VAR

Simülatör aşağıdan yukarı inşa edildi: çekirdek → konfig → dünya → kanal →
ağ → MAC → gözlem → ölçüm → koşum. Her adımın kapanış ölçütü vardı ve hepsi
geçti. Ama o ölçütlerin hepsi *"bu katman kendi içinde doğru mu"* diye
soruyordu.

🔴 **Hiçbiri "bu katman, yapacağımız ölçüm için doğru mu" diye sormadı —
çünkü o ölçüm hiçbir yerde yazılı değildi.**

5 Eylül 2026'da bulunan kusurların hepsi bunun türevidir: kalibrasyon
kimsenin kullanmadığı bir grafikte yapılmıştı, karıştırıcı koşunun başından
sonuna açıktı *(yani projenin asıl iddiası olan "toparlanma" ölçülemezdi)*,
kâhin sönümlemeyi görmüyordu, 18 senaryonun ayırt edip edemeyeceği hiç
sorulmamıştı.

Ve bir ölçüm daha yapıldı: **davranış belirleyen 108 sayısal parametrenin
çoğunun değeri gerekçesiz.** Yorumlar *"bu parametre neden VAR"* sorusunu
cevaplıyor, *"neden BU DEĞER"* sorusunu değil. `kuyruk_kapasitesi = 50`ın
yanında *"sonsuz kuyruk yasak"* yazıyor — neden 50 olduğu yazmıyor.

Bu belge o boşluğu kapatır ve bundan sonra **tek doğru kaynaktır**.

---

## 01 · NE ÖLÇÜYORUZ

### 01.1 · İddia yapısı
Proje şunu iddia edecek: *karıştırma altında, önerilen yönlendirme protokolü
AODV / OLSR / AOMDV'ye göre [şu metriklerde] [şu kadar] daha iyidir.*

Bu iddianın savunulabilir olması için beş şey gerekir ve **hepsi bu belgede
karara bağlanır**: tehdit modeli · ağ modeli · sadık taban çizgileri ·
iddiayı ölçebilen metrikler · ön-kayıtlı istatistik.

### 01.2 · Aletin karşılaması gereken üç sınav
| sınav | soru | bugün |
|---|---|---|
| **iç tutarlılık** | sayaçlar birbirini tutuyor mu | ✅ korunum + mutabakat |
| **analitik** | bilinen formüllerle uyuşuyor mu | ✅ Bianchi · sönümleme varyansı · yol kaybı |
| **dış çapa** | yayımlanmış bir sonucu yeniden üretiyor mu | 🟡 **KOŞULDU** — mekanizma tuttu, sayı α farkıyla açıklandı (K-108) |

Üçüncüsü olmadan alet, kendi içinde tutarlı ve tamamen yanlış olabilir.
**Bu belgenin en önemli maddesi §10'dur.**

---

## 02 · DÜNYA MODELİ — hareketli gözlem çerçevesi

### 02.1 · Karar
> **Simülasyon hacmi, sürünün kütle merkezine bağlı HAREKETLİ bir gözlem
> çerçevesidir. Modellenen bütün hızlar GÖRELİ hızlardır.**

**Gerekçe (Galileo değişmezliği):** ağın hissettiği her şey — mesafe, bağıl
hız, Doppler, topoloji değişimi — yalnız göreli büyüklüklere bağlıdır.
Sürünün ortak hareketi ağa **görünmez**. Bu bir yaklaşım değil, tam eşitlik.

### 02.2 · Bu neyi düzeltir
1. **Kutu duvarı bir yapaylıktı.** Gerçek İHA görünmez bir duvardan sekmez.
   Duvar yansıması, "atanmış sektörün kenarında geri dönme"nin kaba modeliydi
   ve bir kez de kusur üretmişti *(düğümlerin duvara yapışması)*.
2. **🔴 Merkeze çakılı karıştırıcı savunulamazdı.** Hareketli çerçevede o,
   *"karıştırıcı sürüyle formasyonda uçuyor"* demektir. Yer çerçevesinde de
   tuhaftır: sürü hiç ayrılmadan karıştırıcının etrafında dolanır.
3. **Hareketin yanlış bileşeni modelleniyordu.** Gerçek sürüde hareketin
   büyük kısmı ORTAK, küçük kısmı görelidir. Bizim modelimizde ortak bileşen
   sıfır, hareketin tamamı göreliydi — yani yönlendirmeyi zorlayan bileşen
   azami yapılmıştı. Tam tersi olmalıydı.

### 02.3 · Ne modellenir, ne modellenmez
| | |
|---|---|
| modellenir | düğümlerin **birbirine göre** konumu ve hızı |
| modellenir | yer referanslı varlıkların *(karıştırıcı, baz)* çerçeveden **geçişi** |
| modellenmez | sürünün ortak hızı — ağa görünmez |
| beyan edilir | çerçevenin ortak hızı, yalnız **raporlama** için: gerçek dünya eşlemesi |

### 02.4 · Ölçek
Simülatör bir **geometrik ölçek modelidir**. `olcek` konfigürasyona birinci
sınıf bir alan olarak girer ve kavanoz–gerçek eşlemesi tek bir yerde durur.

⚠️ **Ölçeklenemeyen tek şey dalga boyudur.** Dolayısıyla sönümlemenin
Doppler'i, ölçekli hızdan değil **tam ölçek hızından** hesaplanır. Korunması
gereken boyutsuz büyüklük *"kanal bir çerçeve boyunca kaç kez değişiyor"*dur
ve ancak böyle korunur. Bu bir hile değil, ölçek modellemesinin standart
uygulamasıdır ve **beyan edilir**.

**Ölçek tutarlılığı bir KAPIDIR:** `Pt_gerçek = Pt_sim + 10·α·log₁₀(ölçek)`
fiziksel olarak var olabilecek bir telsiz vermelidir. *(Bu kapı α = 3'ü
eledi: 35 kW'lık bir verici çıkıyordu.)*

---

## 03 · MOBİLİTE — m/s ile değil, ÇALKANTI SAYISIYLA tanımlı

### 03.1 · Sorun
Bugüne kadar mobilite `gm_hiz_min/maks_ms` ile tanımlıydı ve o sayıların
gerekçesi yoktu. Ölçüldü: bağıl hız **26,4 m/s**, rota ömrü **2,6 s**.
OLSR'ın `TOP_HOLD_TIME`ı 15 s. Yani **OLSR'ın topoloji bilgisi
kullanılmadan bayatlıyor** — kurulum yüzünden zayıflatılmış bir taban çizgisi,
yani straw-man.

### 03.2 · Karar
> **Mobilite, ÇALKANTI SAYISI Θ ile tanımlanır. Hızlar Θ'dan TÜRETİLİR.**
>
> ```
> Θ = ortalama rota ömrü / en yavaş taban çizgisinin topoloji zamanı
>   = τ_rota / 15 s        (OLSR TOP_HOLD_TIME, RFC 3626)
> ```

| kol | Θ | anlamı |
|---|---|---|
| **durgun** | ∞ | topoloji değişmez — referans nokta |
| **orta** | **≈ 10** | protokol bilgisi çoğu zaman taze — gerçekçi seyir |
| **yüksek** | **≈ 3** | bilgi zamanın üçte birinde bayat — zorlayıcı ama adil |
| *(yasak)* | < 1 | protokoller çalışamaz; karşılaştırma değil, kurulum hatası |

**Bugün Θ ≈ 0,17.** Yani yasak bölgedeyiz.

**Neden bu ölçüt:** taban çizgilerinin zayıflatılmadığını garanti eden tek
şey, onların kendi zaman sabitleridir. Θ, doğrulanmamış bir menzil ya da hız
sayısına değil, **RFC'nin kendi tablosuna** dayanır.

**Çapraz kontrol:** seçilen Θ'ya karşılık gelen hızlar, ölçek uygulanınca
doğrulanmış İHA hız aralığına *(30–400 km/h, A5a)* düşmelidir. Düşmezse ya
Θ ya ölçek yanlıştır.

### 03.3 · Hareket modeli
Hareketli çerçevede rastgele yürüyüş anlamsızdır — sürü dağılır. Doğru model
**istasyon tutma**dır:

- Her düğümün formasyona göre bir **istasyonu** vardır.
- Düğüm istasyonunu sınırlı hatayla tutar; hata süreci manevra gürültüsüdür.
- Manevra zaman sabiti bir **araç dinamiği** büyüklüğüdür ve **ölçeklenmez**:
  gerçek bir İHA onlarca saniye düz uçar. *(Bugünkü `gm_alfa = 0,85`, 0,5 s
  adımda 3,1 s korelasyon süresi veriyor — bir İHA için fazla titrek.)*
- **Görev kolu**: istasyonlar müfrezeler hâlinde gruplanır; müfreze merkezleri
  birbirine göre yavaş hareket eder.
- **Yüksek çalkantı kolu**: istasyonlar atanmış sektör içinde yavaşça yer
  değiştirir. Sektör sınırı **beyan edilen bir kısıttır**, fizik değil.

🔒 Duvar yansıması kaldırılır. Sınırlama formasyondan gelir, duvardan değil.

---

## 04 · KANAL VE FİZİK

Bu katman **büyük ölçüde korunur** — tek tek doğrulanmış durumda.

| bileşen | karar | durum |
|---|---|---|
| yol kaybı | log-mesafe, **α = 2,0** *(hava-hava serbest uzay; iki-ışın kırılma mesafesi her iki dünyada da bağ mesafesinin çok üstünde)* | ✅ |
| gölgeleme | log-normal, korelasyonlu, σ ve hücre boyu **ölçülerek** seçilir | ⚠️ σ ölçülmüş, hücre boyu değil |
| sönümleme | Rician, FIR ile durumsuz, marjinal varyans tam 1 | ✅ · K değeri gerekçesiz |
| anten | yarım dalga dipol, kapalı form | ✅ |
| girişim | toplamsal, parça başına SINR | ✅ |
| PER | önbelge *(DBPSK)* + gövde *(DQPSK)* ayrı | ✅ |
| MAC | 802.11b DCF, temel erişim, Bianchi ile ±%15 | ✅ |

**Değişecek:** `rician_k_db` ve `golgeleme_hucre_m` gerekçelendirilir ya da
duyarsız oldukları gösterilip beyan edilir *(§11)*.

**🔴 Menzil artık bir "yarıçap" değildir.** Ölçüldü: tek bir yarıçap gerçek
bağ kümesini temsil edemiyor — derece eşitlense bile kenarların yalnız yarısı
örtüşüyor *(Jaccard 0,53)*, çünkü gölgeleme σ = 3 dB, α = 2'de mesafede
±%41 demek. Dolayısıyla:

- `iletim_menzili_m` **yalnız verici gücünün çapasıdır**, bağlantılılık
  yarıçapı değil. Adı buna göre değişir: **`guc_capasi_m`**.
- Bağlantılılık ve derece **kanaldan** ölçülür, geometriden değil.
- `Topoloji`nin komşuluk grafiği bir **teşhistir** ve öyle etiketlenir.

---

## 05 · TEHDİT MODELİ

🔴 Bugüne kadar **tasarlanmadı** — kodlanan neyse o oldu: bir karıştırıcı,
alan merkezinde, koşu boyunca açık, gücü kalibre edilmemiş. Bu belgenin en
çok karar içeren bölümü budur.

### 05.1 · Yönlendirici bir savunmanın işe yarayabilmesinin şartı
> **Karıştırılan bölge alanın bir PARÇASI olmalıdır.**

Ölçüldü: düğüm gücü 0,03 dBm, girişim menzili **1 767 m**, alan **1 800 m**.
Yani düğümle aynı güçteki bir karıştırıcı alanın tamamını kapatır. Alanın
tamamı kapanırsa **etrafından dolaşılacak bir yer yoktur**, bütün protokoller
eşit çöker ve deney *"fark yok"* der — ama bu farkın yokluğu değil,
**sorunun yokluğudur**.

### 05.2 · Karar: çalışma noktası `ρ` ile seçilir — ama sınıflar ρ ile EŞİTLENMEZ
> **Çalışma noktası: −15,0 dBm · ρ = 0,258** (ölçüldü, 8 Eylül 2026)
> Üretici: `python kalibrasyon/karistirici_gucu.py`

ρ = engellenen bağ oranı, yani *ağın kaçta kaçı yok edildi*. Bir gücün ne
kadar ağ yok ettiği alana, yoğunluğa ve yayılım üsteline bağlı olduğu için
dBm tek başına anlamsızdır; **nokta seçerken** doğru birim ρ'dur.

🔒 Nokta bir kez ve **referans sınıfta** (`surekli`) seçilir — zaman yapısı
olmayan tek sınıf odur, dolayısıyla ρ orada örtüşmesiz okunur. Ölçüt: 30
tohumun hiçbirinde birden fazla çok üyeli bileşen yokken ρ en büyük.

🔴 **BU BÖLÜMÜN İLK HÂLİ YANLIŞTI ve düzeltildi.** Şöyle diyordu: *"her sınıf
aynı ρ'ya kalibre edilir; bu, darbelinin ortalama gücü / taramalının tepe
gücü eşitlemesinin yerine geçer."* İkisi de yanlış:

1. **ρ ile eşitlemek DÖNGÜSELDİR.** ρ bir *etkidir*, yani bağımlı değişken —
   deneyin ölçmek istediği şeyin ta kendisi. Her sınıfa aynı ρ'yu verdirmek,
   aramaya çıktığımız mekanizma farkını kalibrasyonla **silmek** olurdu.
2. **Yerine geçtiği söylenen karar aslında doğruydu.** Eşitleme,
   karıştırıcının *harcadığı* şey üzerinden yapılır: yayılan **ortalama güç**,
   bir verici özelliği, bir girdi. Kod bunu zaten böyle yapıyormuş; sapan
   şartnameydi.

🔒 Beş sınıf da **aynı tabanı** taşır (−15,0 dBm) ve tepe telafisi ortalamayı
eşitler. **Ölçülerek doğrulandı:** sürekli −15,00 · darbeli −15,00 · aldatıcı
−15,10 · taramalı −19,88 dBm.

⚠️ Son satır **beyan edilmiş tek asimetridir**: `taramali` tepesini eşit
tutar, ortalaması konak sayısına bölünür. *"Taramalı zayıf çıktı"* bulgusu
mekanizmaya tek başına yazılamaz.

### 05.2b · Ölçülen sınıf profilleri — ρ bir SONUÇ alanıdır
| sınıf | açık | ort_dBm | ρ | ayrılan |
|---|---|---|---|---|
| `surekli` | 1,000 | −15,0 | 0,258 | 0/30 |
| `surekli_darbeli` | 0,499 | −15,0 | 0,169 | 1/30 |
| `reaktif` | 0,000 | −∞ | 0,000 | 0/30 |
| `aldatici` | 0,978 | −15,1 | 0,258 | 0/30 |
| `taramali` | 0,325 | −19,9 | 0,081 | 0/30 |

⭐ **`aldatici` ↔ `surekli` EŞLEŞTİRİLMİŞ KONTRASTTIR:** kanal grafiğinde
tıpatıp aynılar. Bağ hasarı sabit tutulmuş, tek fark CSMA görünürlüğü — yani
ikisinin farkı **saf kanal-erişim etkisidir**. Tehdit modelindeki en temiz
karşılaştırma budur ve ön-kayıtta hipotez olarak yazılır.

> 🔒 **8 EYLÜL 2026 DENETİMİ — EŞLEŞME ÖLÇÜLDÜ, VE BİR ARTIK VAR.**
> *Üretici: `python kalibrasyon/denetim_ornekleme.py c f`*
>
> · Kanal grafiğinde eşleşme **birebirdir ve tesadüf değildir**: `aldatici`
>   dokuz örnek anının **9/9'unda AÇIK**, ve iki kolun kenar kümeleri
>   270/270 (30 tohum × 9 an) noktada **aynı**.
> · **AMA ÇERÇEVE DÜZEYİNDE TAM DEĞİL.** Aldatıcı zamanın %2,2'sinde
>   (DIFS boşlukları) kapalıdır ve `alim_per` çerçeveyi parça parça integre
>   eder. Ara PER bandındaki 61 bağda ölçüldü: `surekli − aldatici` PER
>   farkı ortalama **+0,0039**, en büyük **+0,0080**. İşaret beklendiği gibi
>   pozitif — aldatıcı biraz daha az hasar verir.
> · 🔴 Yani iki kolun farkı **saf CSMA değil, CSMA + bu artıktır**.
>   Ön-kayıtta hipotez böyle yazılır; artık 0,008 PER puanıyla sınırlıdır.

🔴 `reaktif` ρ = 0 bir kusur **değil, tanımdır**: trafiksiz bir grafik
probunda patlayacağı iletim yoktur. Şiddeti Faz 2'de trafikli ölçülür.

🔒 **Bağlantılılık kısıtının zaman anlamı netleşti** (darbeli 1/30 tohumda
çiğnedikten sonra): *hiçbir kolda bölünmüş topoloji, en hızlı taban
çizgisinin rota geçersizleme süresinden (AODV 3 s, RFC 3561) uzun
sürmeyecek.* Darbelinin ayrılması yapısal olarak ≤ 1,35 s'dir; temiz grafik
30/30 tohumda tek parça olduğu için kapanınca bütünleşme garantidir.

### 05.3 · Karar: karıştırıcının bir AÇILMA ANI vardır
> **Ölçüm penceresi üç evreye bölünür: TEMİZ → ŞOK → TOPARLANMA.**

**Gerekçe:** projenin beyan edilmiş beklentisi *"ilk şokta %50'nin altına
düşer, mesh tepki verince %70–80'e çıkar"* bir **geçici tepki** tarifidir.
Karıştırıcı baştan sona açıkken bu **yapısal olarak ölçülemez** — ölçülen tek
şey kararlı hâldeki bozulmadır. Ve bir anti-jamming yönlendirme protokolünün
asıl iddiası *"ne kadar bozuluyor"* değil, **"ne kadar hızlı toparlanıyor"**dur.

### 05.4 · Karar: karıştırıcı çerçeveden GEÇER
Yer referanslı bir karıştırıcı, hareketli çerçevede doğal olarak şu profili
üretir:

```
temiz → yaklaşma → şok → mesh tepkisi → uzaklaşma → temiz
```

Parametreleri **fiziksel ve anlamlı**: en yakın geçiş mesafesi, geçiş hızı
*(= sürünün transit hızı)*, ve ρ. "Merkeze çakılı karıştırıcı" tuhaflığı
ortadan kalkar.

### 05.5 · Tehdit ekseninin son hâli
| eksen | seçim | gerekçe |
|---|---|---|
| sayı | **1** | en basit ayırt edici; çoklu karıştırıcı keşifsel eksende |
| yer | **yer referanslı, çerçeveden geçen** | uçan karıştırıcı formasyonda uçmaz |
| zaman | **ölçüm penceresi içinde açılır** | toparlanma ölçülebilsin |
| şiddet | **−15,0 dBm** — nokta ρ ile, referans sınıfta seçildi | 🔒 ölçüldü |
| mekanizma | 5 sınıf *(sürekli · darbeli · reaktif · aldatıcı · taramalı)* | hepsi aynı TABAN güçte; ρ sonuç |
| bilgi | kör / reaktif / aldatıcı | mevcut sınıflar bunu zaten kapsıyor |

🔴 **Mekanizma kapısı:** bir sınıf, ilan edilen güçte ölçülebilir bir etki
üretmiyorsa **bulgu olarak raporlanır**, kolu sessizce güçlendirilmez.

### 05.6 · ⚠️ ŞARTNAME İLE KODUN AYRIŞTIĞI YER — açıkça yazılıyor
§05.4 karıştırıcının **çerçeveden geçtiğini** söylüyor. **Kod bunu yapmıyor:**
karıştırıcı alan merkezinde sabit duruyor ve `karistirici_baslangic_s = 150 s`
ile devreye giriyor. Yani üç evre (temiz → şok → toparlanma) **var**, ama
"yaklaşma / uzaklaşma" profili **yok**.

Bu bir eksiklik olarak durur ve kapatılana kadar §05.4 bir **tasarım niyeti**,
uygulanmış bir karar değildir. Sonuç satırında karıştırıcının sabit olduğu
etiketlenir; hareketli karıştırıcı Faz 1 sonrası değerlendirilir.

---

## 06 · TRAFİK

### 06.1 · Bugünkü hâl ve sorunu
10 akış × 4 pkt/s × 512 B, **rastgele düğüm çiftleri**. Yük ölçülerek
seçilmiş *(tek çarpışma alanının %36,9'u)* — bu iyi. Ama **desen** bir MANET
geleneği, İHA gerçeği değil.

### 06.2 · Karar
> **İki trafik deseni: eşler-arası *(mevcut)* ve YERE TOPLAMA.**

Gerçek bir taktik İHA sürüsünde baskın desen **yere toplamadır**: bütün
düğümler bir yer istasyonuna / geçide veri gönderir. Bunun üç sonucu var ve
üçü de deney için değerli:

1. Yollar **uzar** — trafik geçide yakınsar, ortalama atlama sayısı artar.
   *(Bugün 2,2 atlama; yönlendirmeye dar bir alan bırakıyor.)*
2. **Doğal darboğaz** oluşur — geçit çevresindeki düğümler kritik hâle gelir.
3. Karıştırıcı için **anlamlı bir hedef** doğar: geçidi kesmek.

🔒 Eşler-arası desen korunur *(genel yönlendirme stresi)*, yere toplama
**birincil desen** olur. Hangisinin birincil olacağı §15'te öğrenciye sorulur.

⚠️ **Beyan:** CBR bir basitleştirmedir; gerçek telemetri patlamalıdır.

---

## 07 · PROTOKOL YÜZEYİ

🔒 **`05-GOZLEM-PENCERESI.md` genişletilemez bir sözleşmedir ve aynen
korunur.** Protokol yalnızca şunları görür: kendi komşu tablosu · son
iletiminin sonucu · kuyruk doluluğu · **ölçtüğü gürültü** · duyduğu beacon'lar.

Konumları, gerçek topolojiyi, kanalın durumunu **göremez**.

**Bu yüzey bir anti-jamming protokolü için yeterlidir:** karıştırma sezimi
`olculen_gurultu_w` ve `son_iletim_sonucu`ndan yapılır; bağ kalitesi
`duyulan_beacon` sayısından kestirilir. Genişletmeye gerek yoktur ve
genişletmek o güne kadarki her ölçümü geçersiz kılar.

**Kâhinler** `kalibrasyon/` altındadır ve taban çizgisi değildir:
- `en_guvenilir_kahin` — beklenen iletim sayısını küçültür. **Gerçek tavan.**
- `en_kisa_yol_kahin` — en az atlama. Ölçütün bedelini ölçmek için.

```
ETX-kâhin − atlama-kâhin = ölçütün bedeli
atlama-kâhin − protokol  = protokolün körlüğünün bedeli
```

---

## 08 · METRİKLER — hipotezden türetilir, listeden değil

### 08.1 · Korunanlar
`pdr` · `psr` · `nrl_cerceve` · `nrl_bayt` · `nrl_airtime` · `cor` ·
`algilama_duyarliligi` · gecikme yüzdelikleri.

### 08.2 · 🔴 Eklenecekler — bugün ölçülemeyen şey
| metrik | tanım | neden |
|---|---|---|
| **şok derinliği** | temiz evre PDR'si − şok evresinin en düşük PDR'si | "ne kadar bozuldu" |
| **toparlanma süresi** | açılma anından, PDR'nin temiz değerinin %X'ine dönmesine kadar | 🔴 **protokoller arası asıl ayırt edici** |
| **toparlanma tamlığı** | toparlanma platosu / temiz PDR | tam mı, kısmi mi |
| **sezme gecikmesi** | gerçek açılma anı → protokolün ilk tepkisi | yüzeyde `olculen_gurultu_w` var; kullanılıyor mu |

⚠️ Bu dördü **açılma anı olmadan tanımsızdır**. §05.3 bu yüzden zorunludur.

`cor` bir **orandır**, süre değil — "toparlandı mı" der, "ne kadar sürede"
demez. Protokoller arasındaki fark en çok orada görünür.

---

## 09 · SENARYO MATRİSİ VE İSTATİSTİK

### 09.1 · Bugünkü tasarımın sorunu
3 mobilite × 6 karıştırıcı = **18 aile**. Holm–Bonferroni 18 aile üzerinden
düzeltince istatistiksel güç ciddi biçimde erir. Ve hiçbiri *"bu hücre ayırt
edebiliyor mu"* diye sorulmadan seçildi.

### 09.2 · Karar: ÇEKİRDEK + KEŞİFSEL
> **Ön-kayıt yalnız ÇEKİRDEĞİ mühürler. Gerisi keşifsel raporlanır ve
> doğrulayıcı iddia taşımaz.**

**ÇEKİRDEK DENEY** *(birincil hipotez burada sınanır)*
```
1 mobilite kolu (orta çalkantı, Θ ≈ 10)
× 3 karıştırma koşulu (yok · sürekli-açılan · reaktif-açılan)
× 4 protokol
× ≥30 tohum
= 360 koşu · Holm 3 karşılaştırma üzerinden
```

**KEŞİFSEL EKSENLER** *(betimsel; hipotez sınamaz)*
mobilite Θ ∈ {∞, 3} · kalan karıştırıcı sınıfları · ρ taraması · trafik deseni ·
🔴 **ağ derinliği**.

### 09.3 · Güç analizi ÖNCE yapılır
Tohum sayısı "30" diye kabul edilmez; beklenen etki büyüklüğü ve tohumlar
arası varyanstan **hesaplanır**. Varyans, çekirdek hücrenin taban
çizgileriyle ölçülür. 30 yetmiyorsa artırılır — mühürden önce.

> 🔴 **ÖLÇÜLDÜ — 9 Eylül 2026.** *Üretici: `python kalibrasyon/cozunurluk.py`*
> (`statik-surekli`, 30 tohum, kâhin kolları)
>
> | çıktı | ortalama | SD_tohum | **R = 2·SD/√30** |
> |---|---|---|---|
> | `pdr_etx` | 0,9379 | 0,0693 | 0,0253 |
> | `pdr_atlama` | 0,8896 | 0,0988 | **0,0361** |
> | `olcut_bedeli` *(eşleştirilmiş)* | 0,0483 | 0,0706 | 0,0258 |
>
> 🔴 **30 tohumlu bir hücre yalnızca ~3,6 PDR puanından büyük farkları
> görebiliyor.** Tohumlar arası SD 0,07–0,10 — çok yüksek. Protokoller
> bundan az ayrışıyorsa 30 tohum YETMEZ ve mühürden önce artırılmalıdır.
>
> ⭐ Eşleştirilmiş `olcut_bedeli` daha keskin (0,026): deneyin asıl ayırt
> edici ekseni de zaten odur. Sonuçlar mümkün olduğunca EŞLEŞTİRİLMİŞ
> kontrastlar üzerinden okunmalı, mutlak PDR üzerinden değil.

---

### 09.4 · 🔴 DERİNLİK BİR SABİT DEĞİL, BİR EKSEN — 8 Eylül 2026
Alan büyüklüğü, derinliği **amaç edinen** bir ölçütle seçildi *(§14 sırası)*.
Bu meşru bir deney tasarımıdır: eski alanda çiftlerin %99,7'si bir-iki
atlamaydı ve orada *"protokoller arasında fark yok"* çıkardı — ama bu farkın
yokluğu değil, **sorunun yokluğu** olurdu.

⚠️ **Ama iddiayı da daraltır.** Derinlik sabit tutulursa sonucun o derinliğin
artefaktı olup olmadığı bilinemez: 2 atlamada kazanan bir protokol 5 atlamada
kaybedebilir. Jüri *"bu sonuç sizin seçtiğiniz topolojiye mi özgü?"* diye
sorduğunda cevap olmaz.

**Karar:** derinlik keşifsel eksene girer *(2–3 seviye, alan büyüklüğüyle
ayarlanır)* ve tek bir soru sorulur:

> **Protokol SIRALAMASI derinliğe göre değişiyor mu?**

- Değişmiyorsa iddia **güçlenir** — sonuç topolojiye özgü değil.
- Değişiyorsa bu bir **bulgudur** ve raporun en ilginç kısmı olabilir:
  hangi protokol hangi rejimde işe yarıyor.

🔒 Çekirdek deney tek derinlikte kalır — istatistiksel güç orada, ve
ön-kayıt yalnız onu mühürler.

### 09.5 · ⚠️ KARIŞTIRICISIZ KOL BİR KONTROL, BİR KARŞILAŞTIRMA DEĞİL
Kâhin tavanı karıştırıcısız kolda **0,996–1,000** ölçüldü. Yani orada bütün
protokoller birbirine yakın çıkacak ve ayırt edici olmayacak. Bu bir kusur
değil, tanım: karıştırıcısız kol *"alet sağlam mı"* sorusunu cevaplar,
*"hangi protokol daha iyi"* sorusunu değil. Ayrım karıştırıcılı koldan
gelmek zorundadır.

### 09.6 · 🔴 "SİMÜLATÖR PROTOKOLÜ KISITLAMAZ" — KANIT BOŞTU (9 Eylül 2026)

> 🔴 **AŞAĞIDAKİ TABLONUN KANIT DEĞERİ YOKTUR.** Sayılar `dogrudan_komsu`
> koşum aletiyle üretildi ve o alet **`aktarilan_paket = 0`** veriyor: tek bir
> paketi bile ARA DÜĞÜMDE ileri iletmemiş (üretilen 12 799 · teslim 5 114 ·
> `hedef_yok` ile düşen 6 548 — hepsi tek atlamada).
>
> TTL yalnız **aktarmada** azalır; kuyruk yalnız **aktarmayla** dolar.
> Yani bu test, parametreler ne olursa olsun **sıfırdan başka bir şey
> üretemezdi**. Geçmiş görünen ama hiçbir şey sınamayan bir kapı.
>
> 🔒 Aynı ölçüm, çok atlamalı koşum aletiyle: **kuyruk 50/50 dolu · 226
> taşma · 162 TTL ölümü**. Yani mekanizmalar gerçekten bağlıyor — sadece o
> alet onlara hiç dokunmuyordu.
>
> **DÜZELTME BİR SAYI DEĞİL, BİR ÖN KOŞUL.** Verdikt artık üç durumlu:
> `aktarilan_paket = 0` → **KOŞULMADI** · aktarma var + marj geniş → GEÇTİ ·
> aktarma var + marj dar → **KISITLIYOR**. Ve **marj** raporlanır, sayım
> değil: *"TTL ölümü 0"* bir yokluk, *"en uzun yol 5 atlama, TTL 32,
> marj 6,4×"* bir kanıttır.
> Üretici: `python -u kalibrasyon/bag_kumesi.py k`
>
> 🟢 **TTL için yapısal kanıt BUGÜN VAR:** döngüsüz bir yönlendirmede yol
> uzunluğu ağ çapını aşamaz ve çap ölçüldü — N = 40'ta en uzak çift
> **5 atlama** (`bag_kumesi.py j`). TTL 32 ile marj 6,4×. TTL yalnızca
> **döngü** olduğunda bağlar; zaten var olma sebebi odur.
>
> 🔴 **Kuyruk kapasitesi için kanıt YOK.** İki koşum aleti soruyu
> **bracketliyor ama cevaplamıyor**: biri mekanizmaya hiç dokunmuyor, öteki
> kasten döngü üretip patolojik olarak zorluyor. Gerçek verdikt **Faz 3'te**,
> gerçek bir taban çizgisiyle verilecek — ve ön koşul artık boş geçmeyi
> yapısal olarak engelliyor.

Kontrol edildi (8 Eylül 2026, karıştırıcılı ve karıştırıcısız) —
⚠️ **yukarıdaki uyarıyla birlikte okunur:**

| | karıştırıcısız | karıştırıcılı |
|---|---|---|
| TTL ile düşen | 0 *(TTL 32, ağ çapı ~3)* | 0 |
| kuyruk taşması | 0 | 0 |
| en yüksek kuyruk | 3 / 50 | 2 / 50 |
| ulaşılamayan hedef | 0 | 0 |

Atlama sayısı **hiçbir yerde ayarlanmıyor**; geometriden, bağ kalitesinden ve
protokolün kendi seçiminden çıkıyor. Bir protokol isterse uzun yol kullanabilir.
Kısıt DÜNYAYA konuyor, protokole değil — ve kontrollü deneyin tanımı budur.

**Gerekçe:** az sayıda, iyi seçilmiş hücrede yüksek güç; çok sayıda hücrede
düşük güç. `03` "dar tarama" uyarısı iki yönlü çalışır — hem çok dar hem çok
geniş taramak yanıltır. Ve ön-kayıt, **sınanabilecek** kadar iddia
mühürlemelidir.

## 10 · 🔴 DOĞRULAMA PLANI — belgenin en önemli maddesi

Bugüne kadarki bütün doğrulama **iç tutarlılıktır**. Bir alet, kendi içinde
tutarlı ve tamamen yanlış olabilir.

| seviye | ne | durum |
|---|---|---|
| 1 · değişmez | korunum · mutabakat · 444 test | ✅ |
| 2 · analitik | Bianchi *(DCF)* · marjinal varyans *(sönümleme)* · yol kaybı | ✅ |
| 3 · **literatür replikasyonu** | **Li vd.: 802.11 zincirinde kapasite tek atlamanın 1/7'si** | 🟡 **KOŞULDU (K-108)** — sayı tutmadı (0,074 ↔ band [0,10;0,20]) ama **mekanizma tuttu**: fark yol kaybı üstelinden (α = 2 → girişim/iletim 6,31 → yeniden kullanım 8 atlama) ve öngörüyle **%4 uyum**. `09` §SONUÇ |
| 4 · gerçekçilik kapısı | karıştırıcısız + kâhin → PDR ≈ 1 | ✅ *(0,996–1,000)* |
| 5 · ölçek tutarlılığı | tam ölçek vericisi var olabilir mi | ✅ *(2,5 W)* |
| 6 · duyarlılık | sonucu belirleyen sayılar gerekçeli mi | 🔴 **YAPILACAK** |

**Seviye 3 nasıl yapılır:** ayrı bir zincir topolojisi senaryosu *(N düğüm
düz dizi, uçtan uca tek akış, doyurulmuş)*, ölçülen uçtan uca verim tek
atlamanın kaçta kaçı. Hedef: literatürdeki 1/7 ± bant. Tutmazsa MAC ya da
girişim modelinde bir şey yanlıştır ve **bulmadan devam edilmez**.

🔒 `03` Bölüm D bunu *"öğrenci bir simülatör yazdı"* ile *"öğrenci
doğrulanmış bir araştırma aleti kurdu"* arasındaki fark diye tarif ediyor.

---

## 11 · PARAMETRE DİSİPLİNİ

### 11.1 · Kural
> **Davranış belirleyen her sayı dört kovadan birinde olmak ZORUNDA:**
>
> | kova | anlamı |
> |---|---|
> | `TÜRETİLMİŞ` | başka bir şeyden hesaplanıyor, serbest değil |
> | `ÖLÇÜLMÜŞ` | bir kalibrasyon betiği üretti — üretici komut yazılı |
> | `KAYNAK` | doğrulanmış dış kaynak *(RFC, standart, makale)* |
> | `DUYARSIZ` | ölçüldü, sonuç ona duyarlı değil — **beyan edilir** |
>
> Beşinci kova yoktur. Bir sayı hiçbirine girmiyorsa **koşu başlamaz**.

### 11.2 · Nasıl uygulanır
- Her parametre kodda kovasıyla etiketlenir.
- **Mimari denetimine yeni kapı (D12):** etiketsiz parametre = bulgu.
- `DUYARSIZ` kovası **ölçümle hak edilir**, iddiayla değil.

### 11.3 · Duyarlılık denetimi — 🟢 KOŞULDU (9 Eylül 2026, K-107)
Her aday parametre için: değeri oynat, çekirdek hücrenin çıktısı ne kadar
oynuyor ölç, esnekliğe göre sırala.

> *Üretici: `python -u kalibrasyon/duyarlilik.py <kol> [parametre…]`*
> 49 aday · 5 tohum · ×2 ve ×0,5 · iki kâhin · altı kol · ~1 200 koşum.
> **Köken borcu 48 → 33 · `DUYARSIZ` kovası 0 → 15.**
>
> ⭐ **BASKIN OLAN ŞEY BAĞLANTI BÜTÇESİ:** `iletim_menzili_m` (−0,655) ·
> `frekans_hz` (−0,234) · `dugum_sayisi` (−0,183) · `bant_genisligi_hz` ·
> `sicaklik_k` · `gurultu_figuru_db` (üçü de −0,112) ·
> `karistirici_guc_override_dbm` · `darbe_periyodu_s` (−0,093) ·
> `darbe_gorev_cevrimi` · `rician_k_db` · `akis_sayisi`.
> Gerekçelendirilecek 33 sayı değil, esas olarak **bir avuç SINR sayısı** var.
>
> 🔴 **DUYARLILIK BORCU KAPANMADI, BÜYÜDÜ:** beş kol tanımı sabitinin dördü
> kendi canlı kollarında **DUYARLI** çıktı, biri kararsız. Sabit tutulan ve
> sonucu belirleyen bir sayı gerekçesiz kalamaz.
>
> ⚠️ Üç sınır beyan edilir: **OAT** *(birlikte etkiler görülmedi)* ·
> yalnız **çalışma noktası çıktıları** *(protokol sıralamasının duyarlılığı
> Faz 3'e ait)* · ölçüt **kasten asimetrik** *(yanlışlıkla "duyarsız" demek
> gerekçesiz bir sayıyı aklardı; ucuz hata seçildi)*.
>
> ⚠️ `isinma_s` ve `olcum_bitis_s` **OAT ile taranamıyor**: bir sıralama
> değişmeziyle birbirine bağlılar. Birleşik pencere taraması açık borç.

- **duyarlı + gerekçesiz** → 🔴 engel, çözülmeden ilerlenmez
- **duyarsız + gerekçesiz** → beyan et, geç

Maliyet: ~30 parametre × 3 değer × 3 tohum ≈ 6 işçiyle **~1 saat**.
Karşılığı: *"şu 8 sayı sonucu belirliyor, gerisi gürültü"* — ve o zaman 108
sayıyı değil 8 sayıyı gerekçelendirmek gerekir.

---

## 12 · KAPSAM DIŞI — beyan edilir, gizlenmez

| ne yok | sonucu |
|---|---|
| **hız uyarlaması** | kötü bağda 1 Mb/s'ye düşme yok; gerçek bir savunma eksik |
| **yayılma kazancı** | 11 çipli Barker'ın ~10 dB'i yok → **karıştırıcı gerçekte olduğundan ~10 dB etkili** |
| **enerji sezmeli CCA** | güçlü gürültü karıştırıcısı ertelemeye yol açmıyor; yalnız aldatıcı sınıf CSMA tetikler |
| **çoklu kanal / frekans çevikliği** | 🔒 **PROJENİN ÖNCÜLÜ** — çözüm yönlendirme katmanında aranıyor |
| RTS/CTS | temel erişim; Bianchi doğrulaması da temel erişim için |
| yayılım gecikmesi | 600 m'de 2 µs, slotun onda biri |
| arazi / engel | 3B var, engel yok |
| havadan karıştırıcı | yalnız yer referanslı |
| patlamalı trafik | CBR |

---

## 13 · GÖSTERİM

TÜBİTAK sunumunda simülatör bir **gösterim aracı** olacak.

- **İz kanalı ayrıdır ve ölçüme dokunamaz.** Konum + rota olayı + teslim
  olayı yazar; MAC seviyesindeki milyonlarca olayı değil.
- 🔒 **Kapısı:** iz açıkken ve kapalıyken sonuç satırı **bit-birebir aynı**
  olmalı. Testle bağlanır, beyanla değil.
- **Ölçek eşlemesi gösterimin en güçlü parçasıdır**: ekranda *"1 m = N m ·
  bu kutu X km"* yazması, kavanoz fikrini jüriye tek bakışta anlatır. Ve
  `olcek` konfigürasyonda birinci sınıf alan olduğu için o katman
  **veriden** gelir, sonradan uydurulmaz.

---

## 14 · REFACTOR HARİTASI — neyin kalacağı

🔒 **Baştan yazma yok.** 444 test, doğrulanmış DCF, doğrulanmış sönümleme,
çalışan korunum defteri — bunlar 9 haftalık teknik bütçenin yarısı eder.

| paket | karar |
|---|---|
| `cekirdek/` | **aynen kalır** — değişmezler, olay kuyruğu, korunum, RNG, sayaç kayıt defteri |
| `yapilandirma/` | parametreler **kovalarına göre yeniden düzenlenir**; senaryo tanımları yeniden yazılır |
| `dunya/` | 🔴 **mobilite yeniden yazılır** *(istasyon tutma, hareketli çerçeve, duvar yok)*; topoloji **teşhise indirilir** |
| `kanal/` | korunur; karıştırıcıya **yer referanslı konum + açılma zamanlaması** eklenir; ρ kalibrasyonu |
| `ag/` | korunur; **yere toplama trafik deseni** eklenir |
| `mac/` | **aynen kalır** |
| `gozlem/` | **aynen kalır** — sözleşme genişletilmez |
| `olcum/` | **dört evre metriği eklenir** *(şok · toparlanma · tamlık · sezme)* |
| `kosum/` | `ham` bölümü + iz kanalı |
| `kalibrasyon/` | kâhinler korunur; ρ kalibrasyonu, Θ kalibrasyonu, duyarlılık denetimi eklenir |
| `analiz/` | **yeni** — ama sırası en sonda |
| `protokoller/` | **yeni** |

### Sıra
| # | ne | neden burada |
|---|---|---|
| 1 | **Duyarlılık denetimi** | hangi sayılar önemli — geri kalan her şeyi önceliklendirir |
| 2 | **Θ kalibrasyonu + mobilite yeniden yazımı** | bugün yasak bölgedeyiz |
| 3 | **Tehdit modeli**: ρ kalibrasyonu + açılma anı | metrikler buna bağlı |
| 4 | **Dört evre metriği** | iddianın ölçülebilir hâli |
| 5 | 🔴 **Li replikasyonu** | dış çapa — güvenin tek kaynağı |
| 6 | **Dikey dilim**: 1 hücre, uçtan uca, tek cümleye kadar | tekrar etmeden önce bir kez doğru yap |
| 7 | Taban çizgileri · `analiz/` · ön-kayıt · özgün protokol | genişletme |

---

## 15 · KARARA BAĞLANDI — 8 Eylül 2026

Kapsam öğrenci tarafından kesinleştirildi:

> **"Kontrollü bir deney ortamında routing protokolünün jamming karşısındaki
> davranışını izole etmek."**

Bu cümle aşağıdaki dördünü belirledi. **Jamming TEDAVİ, geri kalan her şey
KONTROL değişkenidir** — bir kontrol değişkeni ne kadar sabitlenirse izolasyon
o kadar temiz olur.

| # | karar | gerekçe |
|---|---|---|
| 1 | **Trafik deseni: yere toplama birincil**, eşler-arası keşifsel | Gerçek taktik desen; yolları uzatır *(bugün 2,2 atlama)*, doğal darboğaz yaratır, karıştırıcıya anlamlı bir hedef verir |
| 2 | **Çekirdek Θ ≈ 10**, Θ ≈ 3 keşifsel | Taban çizgileri kurulum yüzünden zayıflatılmasın; Θ ≈ 3 zorlayıcı ama hâlâ adil |
| 3 | **Mobilite YAPISI ile ÇALKANTI ayrı eksenler.** Çekirdek: düzgün istasyon + Θ ≈ 10. Müfreze yapısı keşifsel eksene iner | Kapsam jamming'i izole etmek olduğuna göre mobilite bir kontrol değişkenidir; çekirdekte sabitlenir |
| 4 | **Li vd. replikasyonu yapılacak** | Aletin tek dış çapası; pazarlıksız |

🔒 **Eski 6.5 kapandı.** "Görev tabanlı mobilite"nin müfrezelerinin klik
olamaması artık bir sorun değil: müfreze yapısı çekirdek deneyden çıktı ve
keşifsel eksende, kendi sınırlarıyla birlikte raporlanacak.

---

## 16 · BU BELGENİN STATÜSÜ

- Onaylanınca **tek doğru kaynak** olur; `DEVIR.md` ve `04-NEDEN-BOYLE.md`
  ona atıf yapar.
- Değişiklik önerisi **belgeye** yapılır, koda değil.
- Kod, belgeye uymuyorsa **kod yanlıştır**.
- ⚠️ Ama belge de yanılabilir: §05.2 ölçümle **çürütüldü** ve düzeltildi.
  Belgeyi dokunulmaz saymak, koda dokunulmaz demekle aynı hatadır.

### 16.1 · FAZ 0 İLERLEME
| adım | konu | durum |
|---|---|---|
| ① | ölçüm penceresi ve evreler | 🟢 bitti |
| ② | çalışma noktası (alan · yoğunluk · derinlik) | 🟢 bitti — 1800 m |
| ③ | mobilite (Θ kapısı) ve Doppler ayrımı | 🟢 kapı geçildi — **Θ = 3,25** *(K-110; eski 5,93 sert diskten geliyordu)*. ⚠️ marj yalnız **%8** · ⚠️ keşifsel yüksek çalkantı kolu **Θ = 1,78, kapının ALTINDA** *(öğrenci kararı)* · ⚠️ mobilite YENİDEN YAZILMADI (§17 A4) |
| ④ | **tehdit modeli — güç kalibrasyonu** | 🟢 **bitti — −15,0 dBm · ρ = 0,258** |
| ⑤ | evre metrikleri (şok derinliği · toparlanma) | 🟢 **bitti — dört metrik + dört kapı, hepsi GEÇTİ (K-105)** |
| ⑥ | sonuç satırında `ham` bölümü · kapsam dışı sınırlar | 🟢 **bitti (K-106)** — satır sekiz bölüm, kendi kendine yetiyor |

🔒 Köken borcu **(9 Eylül 2026)**: **33** parametre `SINANMAMIS` **+ 5
parametre duyarlılık borcu**. Ön-kayıt mühürlenmeden önce ikisi de
sıfırlanmalı; D12 kapısı her koşumda ikisini de sayıyor.
*(Yol: 56 → 50 → 48 → 43 → 33. Bir ara 43'e ÇIKTI ve bu defterin
çalıştığının kanıtıdır — K-109'da 27 kalibrasyon sabiti deftere girdi.)*

⭐ Borcun ara ara ARTMASI defterin çalıştığının kanıtıdır: evre kafesinin
dört sabiti deftere girdi ve RFC 3561/3626 `02`de doğrulanmadığı için
`SINANMAMIS` oldular. **Tek bir bibliyografik doğrulama dördünü birden
`KAYNAK`a taşır** — ve aynı iki RFC K-101'in Θ paydasını, K-103'ün
bağlantılılık kısıtını da çıpalıyor. *(İkisi 8 Eylül'de açıldı; bugün
`KAYNAK` kovası 6.)*

> 🔴 **VE FAZ 0'IN BU TABLOSU BİR ŞEYİ HİÇ SORMUYOR — 9 Eylül 2026.**
> Altı adımın altısı *"simülatör kendi içinde doğru mu"* diye soruyor.
> **Hiçbiri *"protokoller bu yüzeyle YAZILABİLİR Mİ"* diye sormadı** —
> ve cevabı ölçüldüğünde **hayır** çıktı: §17.2 (A19). Kontrol düzlemi
> yeteneği Faz 0'ın içinde değil, ama Faz 3'ün ön koşulu.

---

## 17 · 🔴 ŞARTNAME–KOD AYRIŞMA DEFTERİ — 8 Eylül 2026 denetimi

§05.6 tek bir ayrışmayı açıkça yazmıştı *(sabit karıştırıcı)*. Ama yalnız o
bölüm için arandı. Bu defter, **belgenin bütünü kodla karşılaştırılarak**
dolduruldu. Her satır için ya kod ya belge hareket etmek zorundadır; hiçbiri
sessiz bırakılmaz.

🔒 **Bir ayrışmanın burada olması onu meşrulaştırmaz** — görünür kılar. §16
hâlâ geçerli: *kod belgeye uymuyorsa kod yanlıştır*, ama belge de ölçümle
çürütülebilir. Her satır hangisinin çürüdüğünü söylüyor.

| # | belge diyor | kod yapıyor | kim hareket etmeli |
|---|---|---|---|
| **A1** | §11.1: **dört kova** — `TÜRETİLMİŞ · ÖLÇÜLMÜŞ · KAYNAK · DUYARSIZ`. *"Beşinci kova yoktur. Bir sayı hiçbirine girmiyorsa koşu başlamaz."* | 🟢 **KISMEN KAPANDI (K-105):** `DUYARSIZ` eklendi, `TEDAVI` tam olarak `TEDAVI_ALANLARI` oldu, kol tanımı sabitleri `KOL_TANIMI`na ayrıldı. Kova sayısı **yedi**; `SINANMAMIS`taki 50 parametreyle koşu hâlâ **başlıyor**. | 🔴 **BELGE** — §11.1 yedi kovayı ve *"mühürden önce `SINANMAMIS` = 0 **ve** duyarlılık borcu = 0"* şartını yazmalı. Kovanın kendisi artık kodda. |
| **A2** | §11.3: duyarlılık denetiminin çıktısı `DUYARSIZ` etiketidir. | 🟢 **KAPANDI (K-105):** `DUYARSIZ` kovası var (bugün boş) ve borç `DUYARLILIK BORCU` sayacında duruyor — D12 her koşumda basıyor. | ✅ |
| **A3** | §05.3: ölçüm penceresi **ÜÇ** evreye bölünür — `TEMİZ → ŞOK → TOPARLANMA`. | 🟢 **KAPANDI (K-105):** `olcum/evre.py` üç evreyi tanımlıyor — `TEMİZ [50;150)` · `ŞOK [150;165)` · `TOPARLANMA [165;320)`, bölümleme tam. Sınır iki RFC sabitinden türüyor. | ✅ |
| **A4** | §03.3 + §14: mobilite **yeniden yazılır** — istasyon tutma, hareketli gözlem çerçevesi, **duvar yok**. | `dunya/mobilite.py` hâlâ `GaussMarkov3B` + `GorevTabanli3B`, ve **duvar yansıması canlı** *(`kutu.yansit`, iki çağrı yeri)*. Hareketli çerçeve yok. | 🔴 **AÇIK BORÇ** — ve §16.1'de adım ③ **🟢 bitti** görünüyor. Bitmiş olan Θ **kapısıdır**, mobilite yeniden yazımı değil. Satır ayrıştırılmalı. |
| **A5** | §09.2 + §15/2: **çekirdek Θ ≈ 10**. | Çekirdek kol Θ = **5,93**. | 🔴 **BELGE** — K-101 Θ ≈ 10'un *ulaşılamaz* olduğunu ölçtü *(doğrulanmış İHA hız aralığının altına düşüyor)* ve Θ'yı hedef değil **kapı (≥ 3)** yaptı. Karar kayıtta var, şartnameye **taşınmadı**. |
| **A6** | §04: `iletim_menzili_m` yalnız gücün çapasıdır, **adı `guc_capasi_m` olur**. | Ad hâlâ `iletim_menzili_m`. | ⚠️ **KOD** — kozmetik ama ad bir iddia taşıyor: "menzil" okuyan biri onu bağlantılılık yarıçapı sanır, ki §04 tam olarak bunu yasaklıyor. |
| **A7** | §05.4: karıştırıcı çerçeveden **geçer**. | Alan merkezinde sabit. | ✅ **ZATEN BEYAN EDİLDİ** — §05.6. Ayrıca `karistirici.py` başlığı geçişin bu zaman ölçeğinde 225 m *(kutunun %12,5'i)* olduğunu hesaplayıp yaklaşımı gerekçelendiriyor. |
| **A8** | §06.2 + §15/1: **yere toplama birincil** trafik deseni. | `ag/trafik.py`de yalnız eşler-arası desen var. | ⏳ **AÇIK BORÇ** — §14'te *"eklenecek"* diye duruyor, yani biliniyor. Ama §15/1 onu **öğrenci kararı** olarak kesinleştirdi; kesinleşmiş bir karar "eklenecek" listesinde beklerken çekirdek deney tanımı eksiktir. |
| **A13** | §12: kapsam dışı sınırlar **beyan edilir, gizlenmez**. | 🟢 **KAPANDI (K-106):** sınırlar artık HER SONUÇ SATIRINDA (`kapsam` bölümü) ve her biri sonucu hangi yöne çektiğini söylüyor; koşuma özgü olanlar konfigden **türüyor**, bayatlayamıyor. | ✅ |
| **A14** | *(şartnamede yok — açarken çıktı)* | 🔴 **YENİ STRAW-MAN ADAYI:** beacon koşum düzeyinde sabit ve **1 s** (AODV `HELLO_INTERVAL`). OLSR'ın kendi `HELLO_INTERVAL`ı **2 s** (RFC 3626 §18), yani OLSR bu simülatörde RFC'sinin iki katı hızda beacon yayınlıyor: komşu bilgisi daha taze (PDR'de avantaj), kontrol yükü iki katı (`nrl_*`de dezavantaj). | 🔴 **ÖLÇÜLECEK (Faz 3)** — `beacon_gonderilen` ayrı sayaç olduğu için katkı çıkarılabilir. Ayrıntı `02` §R3, K-106. |
| **A9** | §10: doğrulama seviye 1 — **444 test**. | **472 test** geçiyor. | ⚠️ **BELGE** — sayı bayat. *(Üretici: `python -m pytest tests2 -q`, 8 Eylül 2026, `472 passed in 402.71s`.)* |
| **A10** | §12: enerji sezmeli CCA yok; **yalnız aldatıcı sınıf CSMA tetikler**. | `kosum/dugum.py::karistirici_mesgul_mu` iki koşulu birlikte arıyor: `csma_ya_gorunur` *(yalnız `Aldatici` için True)* **ve** gücün gürültü tabanını aşması. | ✅ **AYRIŞMA YOK** — arandı, bulunmadı. Kod belgeyle uyuşuyor. |
| **A11** | §04: `Topoloji`nin komşuluk grafiği bir **teşhistir ve öyle etiketlenir**. | `dunya/topoloji.py` başlığı: *"Buradaki graf ölçüme, kalibrasyona ve teşhise aittir"* ve kâhin yüzeyi olduğunu ilan ediyor. | ✅ **AYRIŞMA YOK.** |
| **A12** | §09.5 + §10/4: karıştırıcısız kolda kâhin tavanı **0,996–1,000**, dolayısıyla o kol *"ayırt edici olmayacak"*. | Bu aralık **yalnız STATİK kolun** sayısıdır *(ölçüldü: 1,000 · 0,999 · 0,996)*. **Hareketli kolda 0,917 ve 0,831.** Yani çekirdek deneyin koşacağı kolda karıştırıcısız tavan 1,0 değil ~0,83–0,92. | 🔴 **BELGE** — §09.5'in gerekçesi hareketli kol için geçerli değil: orada protokollerin ayrışacağı **17 puanlık** bir alan var. §10/4 gerçekçilik kapısı da hangi kolda geçtiğini söylemeli. |

🔒 **A12 için bir kusur hipotezi kuruldu ve ÇÜRÜTÜLDÜ.** İlk şüphe şuydu:
*"0,83, ağın değil KÂHİNİN sınırı olabilir"* — çünkü K-101 hızları
düşürünce `dilim_suresi_s`in türetilmiş değeri 33,3 s'ye çıktı ve 10,0 s'lik
üst kelepçeye dayandı; yani kâhinin grafiği 10 s'ye kadar bayat. Ölçüldü
*(aynı tohum, aynı pencere, `bagimsiz-yok`)*:

| kâhin grafiği tazeleme | PDR |
|---|---|
| `dilim_s = 10,0` *(kelepçeli varsayılan)* | 0,831 |
| `dilim_s = 1,0` *(on kat sık)* | **0,834** |

Fark **0,003**. Tavan kâhinin bayatlığından gelmiyor; hareketli koldaki
kayıp gerçek *(677 iletim başarısızlığı / 4 078 paket)*. **Şüphe ölçüldü ve
düştü** — ama kelepçenin artık bağlayıcı olduğu ve değerin türetilmediği
kayda geçer.

### 17.0 · 🔴 9 EYLÜL 2026 DENETİMİ — yedi satır hareket etti

| # | ne | durum |
|---|---|---|
| **A4** | mobilite yeniden yazımı *(istasyon tutma · duvar yok)* | 🟢 **GEREKÇESİ ÖLÇÜMLE DÜŞTÜ.** Yeniden yazımı isteyen kusur *"düğümler duvara yapışıyor"*du ve **26 m/s** hızlarda ölçülmüştü. Hızlar 1/50 ölçeğe indikten sonra duvar **erişilemez**: 400 yörüngede **sıfır** temas, çünkü 0,75 m/s'te bir düğüm bütün koşuda en çok **262 m** gidiyor (kutu 1800 m). Hareketli çerçeve zaten çerçevenin kendisi. Geriye **istasyon tutma** kalıyor ki o bir gerçekçilik tercihi ve çalkantıyı **azaltır** — Θ zaten kapının %8 üstündeyken ekseni sönükleştirir. 🔴 **ÖĞRENCİ KARARI** |
| **A5** | çekirdek Θ ≈ 10 | 🟢 **KAPANDI.** K-101 Θ ≈ 10'u ulaşılamaz bulup 5,93'e indirmişti; K-110 bağ tanımını düzeltip **3,25**'e getirdi. Hızlar DEĞİŞMEDİ. ⚠️ Marj artık %98 değil **%8** |
| **A9** | doğrulama seviye 1 — 444 test | ⚠️ **474 test**. Sayı yine bayat; her oturumda değişiyor, belgeye SABİT yazılmamalı |
| **A15** | *(yeni)* §09.6 *"simülatör protokolü kısıtlamaz"* | 🔴 **KANIT BOŞTU** — `aktarilan_paket = 0`. Ön koşul eklendi, verdikt üç durumlu. §09.6'ya işlendi |
| **A16** | *(yeni)* `EnGuvenilirKahin` *"gerçek tavan"* | 🔴 **EVRENSEL İDDİA ÇÜRÜDÜ.** Atlama kâhini, eşik 0,99'da 15 tohumun 6'sında onu geçiyor. Sebep: ETX **beklenen iletim sayısını** küçültür, **teslimi** değil, ve yeniden deneme sınırı sonlu. Ortalamada hâlâ önde — *"daha kötü"* değil **üst sınır değil** |
| **A17** | *(yeni)* `kopma_fiziksel` sayacı | 🟢 **AÇIK TAAHHÜT KAPANDI.** Hiç sayılmıyordu, `algilama_duyarliligi` her koşuda `None` dönüyordu — Risk 3'ün nicel yarısı ölüydü. Son işlem olarak eklendi, koşunun %1'i |
| **A18** | *(yeni)* `yol_kaybi_usteli = 2` ile `rician_k_db = 6` tutarlılığı | 🔒 **ŞÜPHE KURULDU VE DÜŞTÜ.** Biri yer yansımasını önemsiz sayıyor, öteki onu %25'te tutuyordu. Çelişmiyorlar: kırılma mesafesinin altında alan serbest uzay etrafında **salınır** — α = 2 ortalamayı, Rician salınımı modelliyor. Geriye bir **denklik** kaldı: K_dB = −20·log₁₀(Γ), yani **K = 6 dB ⟺ Γ = 0,50**. Sayı artık belirsiz bir modelleme tercihi değil, TEK bir bibliyografik kontrol. ⚠️ Projenin kendi *'geçiş bandı mertebesi'* ölçütü K ≈ 8–10 dB'yi işaret ediyor — karar değil, kaynakla birlikte götürülen işaret. Kova `SINANMAMIS` KALIYOR |

### 17.1 · Bu defterin kendi sınırı
Karşılaştırma **belgenin iddialarından koda** doğru yapıldı: §00–§16'nın her
bölümü okundu ve karşılığı kodda arandı. **Ters yön taranmadı** — yani
*"kodda olup belgede hiç anılmayan"* davranışlar bu defterde yok. O tarama
ayrı bir iştir ve yapılmadığı burada yazılıdır.

> 🟢 **9 EYLÜL 2026: TERS TARAMANIN İLK GEÇİŞİ YAPILDI** — parametre
> düzeyinde §17.3, mekanizma düzeyinde ilk bulgu §17.2 (A19).
> ⚠️ Yukarıdaki *"taranmadı"* cümlesi TARİH olarak duruyor.

---

### 17.2 · 🔴 A19 — KONTROL DÜZLEMİ: ÖN-KAYIT, SİMÜLATÖRÜN YAPAMADIĞI ÜÇ ŞEYİ ŞART KOŞUYOR

> **Tarih:** 9 Eylül 2026 · **Bu, bu defterin EN AĞIR satırıdır.**
> Ölçüldü: `sim2/gozlem/protokol.py::KANCALAR` · `sim2/kosum/kosu.py` ·
> `sim2/kanal/cerceve.py::CERCEVE_TIPLERI` · AST taraması.

**Bugün protokolün simülatörle temas yüzeyinin TAMAMI:**

| ne | bugün |
|---|---|
| kanca | **4**: `sonraki_atlama` · `beacon_yuku` · `beacon_alindi` · `teshis` |
| gönderim | **tek yol** — koşum düzeyinde **periyodik** beacon (`kosu.py`), aralık tek bir `beacon_araligi_s` |
| çerçeve tipi | canlı **3**: `veri` · `onay` · `beacon` |
| zamanlayıcı | **yok** — protokolün olay kuyruğuna erişimi yok, olması da doğru değil *(geri referans yasağı)* |

**`06-ON-KAYIT.md` §4.2'nin ŞART KOŞTUĞU ve bugün İFADE EDİLEMEYEN şeyler:**

| gereken | protokol | bugün |
|---|---|---|
| **RREQ** — talep üzerine selleme | AODV · AOMDV | 🔴 yalnız periyodik yayın var |
| **RREP** — ters yol boyunca **unicast** kontrol | AODV · AOMDV | 🔴 unicast kontrol çerçevesi yok |
| **RERR** — kopmada **olay tetiklemeli** yayın | AODV · AOMDV | 🔴 olay tetiklemeli yayın yok |
| **HELLO 2 s + TC 5 s** — İKİ bağımsız periyot | OLSR | 🔴 tek `beacon_araligi_s` |
| `ACTIVE_ROUTE_TIMEOUT` · `RREQ_RETRIES` · `NET_DIAMETER` | AODV | 🔴 protokol zamanlayıcı kuramaz |

🔴 **Ve bu bir tercih değil, bir ÇELİŞKİDİR:** `06` §4.2'nin **U2 uygunluk
testi** aynen şunu istiyor — *"tek bağ koptuğunda AODV **RERR** üretir ve
yeni **RREQ** başlatır."* Yani ön-kayıt, kabul ölçütü olarak simülatörün
ifade edemediği bir davranışı yazmış. `03` kural 4 rakibi **eksik
uygulamayı** yasakladığına göre, bugünkü yüzeyle üç taban çizgisinin üçü de
**sadık biçimde yazılamaz**.

🔒 **NE OLMADIĞI DA ÖNEMLİ — bu bir gözlem sözleşmesi ihlali DEĞİL.**
`05-GOZLEM-PENCERESI.md` protokolün ne **GÖRECEĞİNİ** kısıtlar; buradaki
boşluk protokolün ne **YAPABİLECEĞİ** eksenindedir ve sözleşmede karşılığı
yoktur. Dahası `05` §A2 hakkı zaten veriyor: *"başlıktaki her alan bayta
sayılır."* Yani yapılacak iş **kilitli bir sözleşmeyi genişletmek değil, var
olan sözleşmenin mekanizmasını tamamlamaktır.**

⭐ **ÜÇ ŞEY MALİYETİ DÜŞÜRÜYOR ve üçü de ölçüldü:**
1. **Faturalama zinciri hazır** — `kontrol_cerceve` · `kontrol_bayt` ·
   `kontrol_airtime_s` · `beacon_gonderilen` sayaçları kayıt defterinde
   **var** ve `nrl_*` türevleri onlardan çıkıyor. Yeni kontrol çerçeveleri
   aynı yoldan faturalanır; **şema genişlemez**.
2. **`kontrol` çerçeve tipi ZATEN TANIMLI** (`CERCEVE_TIPLERI`) ve boyutu
   `beacon_bayt`ten geliyor — ⚠️ ama **hiçbir yerde kurulmuyor**: klasik
   *bildirim ≠ kullanım* (`03` B5). Yani yer ayrılmış, mekanizma yazılmamış.
3. Kontrol çerçeveleri korunum defterine **girmiyor** (defter yalnız veri
   paketlerini sayar), dolayısıyla korunum denklemi bozulmaz.

🔴 **BU SATIR NE ŞARTNAMEDE (§00–§16) NE `DEVIR.md`DE ANILIYOR.** Tek kaydı,
emekli `sim/` planına göre yazılmış ve *"süreleri geçersiz"* diye
işaretlenmiş `12-YOL-HARITASI.md` §0'dır. Yani proje, taban çizgilerini
yazamayacağını **bir kez ölçmüş ve sonra unutmuş.**

**Kim hareket etmeli:** 🔴 **KOD** — ve bu Faz 3'ün ön koşuludur, Faz 2'nin
değil.

> 🟢 **10 EYLÜL 2026 — KOD HAREKET ETTİ (K-112).** Mekanizma uygulandı;
> sözleşme `13-KONTROL-DUZLEMI.md`, kapılar P1–P8. Protokoller henüz yok.
> ⚠️ Kalan: bağ kopması geri bildirimi · beacon'ın protokol başına
> kapatılması · protokol rastgelelik kaynağı · veri onayı semantiği (§13 §06). Faz 2'nin dikey dilimi bugünkü yüzeyle yazılabilir *(beacon taşıyan
proaktif bir protokol)*; AODV/OLSR/AOMDV yazılamaz.

---

### 17.3 · 🟢 TERS TARAMA — ilk geçiş *(kodda var, belgede yok)*

*Üretici: köken defterinin 74 `Konfig` alanı + 21 `sim2/` modül sabiti,
`v2/*.md`nin tamamında adıyla arandı.*

| tarama | sonuç |
|---|---|
| `Konfig` alanı | 74 · şartnamede (07) anılmayan **52** · hiçbir `v2/` belgesinde anılmayan **10** |
| `sim2/` modül sabiti | 21 · şartnamede anılmayan **21** · hiçbir belgede anılmayan **10** |

🔴 **Anılmayan 20'nin içinde iki öbek önemli:**

1. **BEŞ ABLASYON BAYRAĞI hiçbir belgede geçmiyor:** `golgeleme_acik` ·
   `sonumleme_acik` · `anten_deseni_acik` · `yakalama_etkisi_acik` ·
   `saat_senkron`. `03` B1 *"bir ablasyon kolu HER ZAMAN bir konfigürasyon
   bayrağıdır"* diyor ve `06` bir ablasyon ailesi mühürlüyor — ama koddaki
   ablasyon eksenlerinin kendisi hiçbir yerde ilan edilmiş değil.
   ⚠️ Üstelik ikisi fiilen KULLANILIYOR: `09-LI-REPLIKASYONU.md` §03.1b
   replikasyonu gölgeleme ve sönümleme **kapalı** koşuyor.
2. **Görev kolunun tamamı:** `gorev_grup_sayisi` · `gorev_grup_yaricapi_m` ·
   `gorev_jitter_hiz_ms` — üçü de yalnız kodda. *(Ve yarıçapın bayat
   olduğu bu oturumda ayrıca ölçüldü.)*

⚠️ **YÖNTEMİN SINIRI BEYAN EDİLİR:** tarama **adı** arar, **kavramı** değil.
`saat_senkron` hiçbir belgede adıyla geçmiyor ama saat senkronsuzluğu `05`
§A1'de uzun uzun tartışılıyor. Yani bu liste *"belgede hiç yok"* değil,
***"belgede ADIYLA bağlanmamış"*** listesidir — ve bir ablasyon bayrağının
ön-kayıtta adıyla bağlanmamış olması yine de bir borçtur.

⚠️ Kalan 10 sabit büyük ölçüde masumdur *(Boltzmann sabiti, ışık hızı, bayt
muhasebesi tavanları)*. Tarama **parametre düzeyindedir**; *"kodda olup
belgede anılmayan MEKANİZMA"* taraması ayrı bir iştir ve A19 onun ilk
bulgusudur.
