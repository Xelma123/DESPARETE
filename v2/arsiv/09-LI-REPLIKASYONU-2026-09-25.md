# 09 · Lİ vd. REPLİKASYONU — aletin TEK dış çapası

> **Durum: 🟢 TAMAMLANDI** — ön-kayıt 8 Eylül 2026'da ölçümden önce yazıldı,
> sonuç 9 Eylül'de altına eklendi, **10 Eylül 2026'da yeniden ölçüldü (K-113)**.
> Şartname karşılığı: `07-SIMULATOR-TASARIMI.md` §10, seviye 3.
> Kaynak: `02-DOGRULANMIS-KAYNAKLAR.md` **A5b** ✅
>
> **10 Eylül yeniden ölçümü** (`python -u kalibrasyon/li_replikasyonu.py`):
> eğrinin on noktası ve duyma menzili taraması 9 Eylül kaydıyla **birebir
> aynı**. H1 = **0,0861** (band [0,10; 0,20] → tutmadı) · H2 ve H3 tuttu ·
> B bölümünün koşum süresi 1,8 dk.
>
> ⚠️ **H1'in sayısı 0,0861'dir.** Betikteki ön-kayıtlı tanım: "uzun zincir =
> 8–11 düğümlü zincirlerin oranlarının ortalaması". **0,0739** yalnız 11
> düğümün değeridir ve §SONUÇ'taki mekanizma öngörüsüyle (0,0714)
> karşılaştırılan sayıdır; bazı eski belgeler onu H1 değeri diye yazmıştı.
>
> ⚠️ §03.1b'deki açık kanal ortalaması (0,94–0,98) 200 m'lik ilk denemenin
> bağlamında verilmiştir. 280 m aralıkta açık kanalın ortalaması **0,8800**,
> en kötü bağı **0,0000** (aynı komutun A bölümü, 10 Eylül).

> 🔴 **BU BELGE ÖLÇÜMDEN ÖNCE YAZILDI VE ÖYLE KALACAK.** Replikasyonun bütün
> değeri, beklentinin ölçümden **önce** ilan edilmiş olmasındadır. Sonuç
> tutmazsa bu belge değiştirilmez; altına *"tutmadı ve sebebi şu"* yazılır.

---

## 00 · NEDEN BU ÖLÇÜM HER ŞEYDEN ÖNEMLİ

Şartname §01.2'nin üç sınavı:

| sınav | durum |
|---|---|
| iç tutarlılık — sayaçlar birbirini tutuyor mu | ✅ korunum + mutabakat |
| analitik — bilinen formüllerle uyuşuyor mu | ✅ Bianchi · sönümleme varyansı · yol kaybı |
| **dış çapa — yayımlanmış bir sonucu yeniden üretiyor mu** | 🔴 **HİÇ YAPILMADI** |

🔒 **Üçüncüsü olmadan alet, kendi içinde tutarlı ve tamamen yanlış olabilir.**
Bianchi doğrulaması MAC'in *tek çarpışma alanındaki* davranışını sınıyor;
bu projenin ölçtüğü şey ise **çok atlamalı** teslim. İkisinin arasındaki
boşluk — uzamsal yeniden kullanım, kendi kendine girişim, zincir boyunca
çarpışma — bugüne kadar **hiç sınanmadı**.

---

## 01 · REPLİKE EDİLEN SONUÇ

**Li, Blake, De Couto, Lee, Morris — *"Capacity of Ad Hoc Wireless
Networks"*, §3.2** *(`02` A5b, ✅ doğrulanmış)*

Üç sayı veriyor ve üçü de ayrı şeyler söylüyor:

| # | ne | değer |
|---|---|---|
| L1 | **ideal MAC** ile zincir kullanımı | **1/3** |
| L2 | **ideal** zincirin uçtan uca verimi, tek atlamanın kaçta kaçı | **1/4** |
| L3 | **802.11**'in gerçekte verdiği | **1/7** |

🔒 **Mekanizma — ve replikasyonun sınadığı şey budur.** Bir zincirde düğüm
*i* iletirken *i±1*, *i±2* ve *i±3* susmak zorundadır: *i±1* alıcı ya da
verici, *i±2* taşıyıcı dinlemeyle duyar, *i±3* alıcıyı bozar. Dolayısıyla
zincirin ancak dörtte biri aynı anda konuşabilir → **L2 = 1/4**. 802.11'in
geri çekilmesi, çarpışmaları ve onay yükü bunu **1/7**'ye indirir.

⭐ Yani **L3/L2 ≈ 0,57 = 802.11'in kendi verimsizliği**, ve L2 = 1/4 saf
uzamsal yeniden kullanım. İkisini ayrı ayrı ölçmek, tek bir sayıya bakmaktan
çok daha güçlü bir sınavdır.

---

## 02 · KURULUM — ve neden `kalibrasyon/` altında

🔒 Zincir bir **deney kolu değil, bir ÖLÇÜM ALETİDİR** — kâhinlerle aynı
gerekçe. Deney matrisine girmez, ön-kayıtta bir aile değildir, `senaryolar.py`
büyümez. `kalibrasyon/` altında kendi dünyasını kurar.

| parça | nasıl |
|---|---|
| yerleşim | `Sabit` mobilite, düğümler tek eksende eşit aralıklı |
| yönlendirme | zincir yönlendiricisi: sonraki atlama = hedefe doğru komşu |
| trafik | **tek** akış, `0 → N−1`, **doygun** |
| kanal | 🔒 **hiçbir şey değişmez** — aynı yayılım, aynı MAC, aynı girişim |

🔴 **Kanalın değişmemesi şart.** Replikasyon, deneyde kullanılan aletin
kendisini sınamalıdır; zincir için ayarlanmış bir kanal hiçbir şey
doğrulamaz.

---

## 03 · ÖLÇÜMDEN ÖNCE KARARA BAĞLANAN ÜÇ SAYI

### 03.1 · Düğüm aralığı — GÜÇ ÇAPASI, ve iki ölçüt de onu gösteriyor

> 🔴 **BU BÖLÜM 8 EYLÜL 2026'DA, İLK ÖLÇÜMDEN SONRA DEĞİŞTİ.** Değişikliğin
> kendisi ve sebebi burada duruyor; ilk hâli silinmedi.

**İlk hâli şuydu:** *"aralık, tek atlama PDR'si ≥ 0,99 olan EN BÜYÜK
aralıktır — en büyük seçilir çünkü aralık küçüldükçe i±2 ve i±3 girişimi
artar ve zincir YAPAY olarak kötüleşir."*

🔴 **Gerekçenin fiziği yanlıştı.** i±2 ve i±3 girişimi bir artefakt DEĞİL,
Li'nin ölçtüğü **mekanizmanın ta kendisidir**: 1/4 oranı, taşıyıcı dinlemenin
iletim menzilinin ~2 katına ulaşmasından doğar. Aralığı büyütmek o girişimi
zayıflatır ve oranı **yapay olarak yükseltir** — yani ilk ölçüt, replikasyonu
tutturmaya değil, kaçırmaya ayarlıydı.

🔒 **YENİ ÇAPA — TÜRETİLMİŞ, SEÇİLMEMİŞ:** aralık = `iletim_menzili_m`
(280 m), yani **verici gücünün çapası**. Bu mesafede girişimsiz SINR tam
olarak eşiğe eşittir. Böylece *"bir atlama = bir iletim menzili"* **yapı
gereği** doğrudur ve zincir geometrisi Li'nin varsayımıyla örtüşür.

🔒 Eski ölçüt bir KAPI olarak KALIR: seçilen aralık, her bağda atlama başarısı
≥ 0,99 sınavını geçmek zorundadır. Ölçüldü — geçiyor (§03.1b).

### 03.1b · 🔴 ÖLÇÜM BİR SETUP KUSURU ORTAYA ÇIKARDI — ve ön-kayıtlı kapı onu yakaladı
İlk deneme 200 m aralıkla koşuldu ve **N ≥ 3 zincirlerde teslim SIFIR** çıktı.
Sebep contention değildi: tek paketli koşuda bile sıfırdı. Ölçüldü —
11 düğümlük zincirin **her bağı**, 5 tohum, atlama başarısı:

| kurulum | en kötü bağ | ortalama |
|---|---|---|
| gölgeleme + sönümleme AÇIK | **0,0000** | 0,94–0,98 |
| yalnız gölgeleme kapalı | **0,0000** | 0,94–0,98 |
| ikisi de kapalı | **1,0000** | 1,0000 |

⭐ **Bağları öldüren şey gölgeleme değil, SÖNÜMLEME.** Statik kolda sönümleme
dondurulmuştur: her bağ **tek bir** Rician çekimi alır ve bağ PER uçurumunun
kenarında olduğu için derin bir çekim onu tamamen öldürür. Ölçülen ölü bağ
oranı **%2–6**.

🔒 **BU BİR KUSUR DEĞİL, ALETİN BİLİNEN VE İSTENEN ÖZELLİĞİDİR** (K-096:
sönümleme kâhin grafiğine tam da "hayalet bağ" üretmesin diye eklendi). Ama
Li'nin kurulumunda **ne gölgeleme ne sönümleme vardır**; onları açık
bırakmak, replikasyonu MAC verimliliği yerine **bağ kesintisi** ölçmeye
çevirirdi — zincirin beşte biri tek bir ölü bağ yüzünden sıfır teslim eder.

🔒 **KARAR: replikasyon gölgeleme ve sönümleme KAPALI koşar.** Bu bir
gevşetme değil, ön-kayıtlı ≥ 0,99 kapısının **kendi işini yapmasıdır**: kapı,
ilan edilen kurulumun sorulan soruya uygun olmadığını söyledi. Verdikt temiz
kurulumda verilir.

⚠️ Bedeli beyan edilir: replikasyon, deneyde kullanılan **kanalın tamamını**
doğrulamaz — MAC + girişim + uzamsal yeniden kullanımı doğrular. Gölgeleme ve
sönümleme ayrı ayrı doğrulanmıştır (σ kaynaktan, K-096 ölçümleri).

### 03.2 · Zincir uzunluğu — TEK SAYI DEĞİL, EĞRİ
🔴 Tek bir N'de tek bir oran ölçmek zayıf bir sınavdır: bir sayı tesadüfen
tutabilir. Li'nin asıl iddiası bir **şekildir** — kullanım N ile düşer ve
düzleşir.

🔒 **N = 1 … 10 taranır ve eğri raporlanır.** Replikasyon eğrinin şeklini de
sınar: düşüş olmalı ve N ≳ 7'de düzleşmeli.

### 03.3 · Doygunluk — ölçülerek kurulur
Kaynak her zaman gönderecek paketi bulmalı. 🔒 Sunulan yük, **tek atlama
kapasitesinin iki katı** seçilir; tek atlama kapasitesi N = 1 koşumundan
**ölçülür**. Doygunluğun kanıtı raporlanır: kuyruk boş kalmamalı.

---

## 04 · 🔴 ÖN-KAYIT: NE BEKLİYORUZ, NE ÇÜRÜTÜR

| # | hipotez | beklenen | **başarısızlık** |
|---|---|---|---|
| **H1** | uzun zincir verimi / tek atlama verimi | **1/7 ≈ 0,143**, band **[0,10; 0,20]** | band dışı |
| **H2** | eğrinin şekli | N arttıkça düşer, N ≳ 7'de düzleşir | monoton düşmüyor ya da düzleşmiyor |
| **H3** | ideal-MAC tavanı ile ilişki | ölçülen oran, 1/4'ün **altında** | 1/4'ün ÜSTÜNE çıkarsa uzamsal yeniden kullanım fazla iyimser |

🔒 **Band [0,10; 0,20] ölçümden ÖNCE ilan edildi** ve şuradan geliyor: L3 =
1/7 = 0,143, ve Li'nin kendi ölçümü de bir noktadır — ±%40'lık bir band, iki
farklı 802.11 uygulaması arasında beklenen ayrımın mertebesidir. Band
sonradan genişletilmeyecek.

### 04.1 · ⚠️ ÖNCEDEN İLAN EDİLEN MODEL FARKLARI
Bunlar **sapmayı mazur göstermek için sonradan bulunan sebepler değildir** —
ölçümden önce yazıldılar. Sonuç bandın dışına düşerse, önce bunların
büyüklüğü ölçülür; hiçbiri açıklamıyorsa **kusur aletindedir**.

| fark | yönü |
|---|---|
| **Taşıyıcı dinleme menzili sert değil.** Li'nin 1/4'ü *"duyma menzili ≈ 2 × iletim menzili"* varsayar; burada duyma bir GÜÇ eşiğidir ve mesafeyle sürekli değişir. | Uzamsal yeniden kullanım Li'ninkinden **farklı** çıkabilir — iki yöne de |
| **RTS/CTS yok.** Li'nin 1/7'si temel erişim içindir. | ✅ aynı — fark yok |
| **Hız uyarlaması yok.** | ✅ aynı |
| ~~**Gölgeleme ve sönümleme AÇIK.**~~ → **KAPALI koşulacak**, gerekçesi §03.1b | Ölçüldü: açık bırakmak zincirin beşte birini tek bir ölü bağ yüzünden sıfırlıyordu |
| **Yayılma kazancı yok** (Barker ~10 dB). | Girişim olduğundan **güçlü** → oran **düşük** tarafa çeker |

🔴 **Sapmanın kabul edilebilir açıklaması, ölçülen bir büyüklük olmak
zorundadır.** *"Herhalde gölgeleme yüzündendir"* bir açıklama değildir;
gölgelemeyi kapatıp yeniden ölçmek bir açıklamadır.

---

## 05 · BU ÖLÇÜM NEYİ SINAMAZ
- Yönlendirme protokollerini — zincirde yönlendirme **yoktur**, rota sabittir.
- Karıştırmayı — zincir **karıştırıcısız** koşar.
- Mobiliteyi — zincir **durgundur**.

🔒 Sınadığı tek şey: **MAC + girişim + uzamsal yeniden kullanımın birlikte
davranışı**, yani bu projenin bütün çok atlamalı sonuçlarının altındaki
katman.

---

## 06 · ÇÜRÜTÜLÜRSE NE OLUR
Şartname §10: *"Tutmazsa MAC ya da girişim modelinde bir şey yanlıştır ve
**bulmadan devam edilmez**."*

🔴 Bu, ön-kayıt mührünün önündeki bir **engeldir**, bir not değil. Faz 0'ın
bütün kalibrasyonu — çalışma noktası, ρ, evre metrikleri — çok atlamalı
teslimin doğru modellendiği varsayımına dayanıyor. O varsayım burada sınanır.

---

# 🔴 SONUÇ — 9 Eylül 2026: **H1 TUTMADI**, H2 ve H3 TUTTU

> Yukarıdaki ön-kayıt **değiştirilmedi**. Sonuç buraya, altına yazılıyor.
> Üretici: `python -u kalibrasyon/li_replikasyonu.py`

## Ölçülen eğri (aralık 280 m · temiz kanal · 5 tohum · doygun)

| düğüm | atlama | verim (pkt/s) | tek atlamaya oran | **oran × atlama** |
|---|---|---|---|---|
| 2 | 1 | 356,07 | 1,0000 | 1,000 |
| 3 | 2 | 101,23 | 0,2843 | 0,569 |
| 4 | 3 | 72,98 | 0,2050 | 0,615 |
| 5 | 4 | 61,08 | 0,1715 | 0,686 |
| 6 | 5 | 50,59 | **0,1421** | 0,711 |
| 7 | 6 | 44,46 | 0,1249 | 0,749 |
| 8 | 7 | 35,07 | 0,0985 | 0,690 |
| 9 | 8 | 31,97 | 0,0898 | 0,718 |
| 10 | 9 | 29,34 | 0,0824 | 0,742 |
| 11 | 10 | 26,32 | 0,0739 | 0,739 |

| hipotez | sonuç |
|---|---|
| **H1** — uzun zincir / tek atlama ∈ [0,10; 0,20] | 🔴 **TUTMADI** — ölçülen **0,086** |
| **H2** — eğri düşüyor ve düzleşiyor | 🟢 TUTTU |
| **H3** — ideal MAC tavanının (1/4) altında | 🟢 TUTTU |

---

## 🔍 SEBEP ARANDI — iki hipotez kuruldu, **ikisi de ÇÜRÜTÜLDÜ**

Şartname §10: *"Tutmazsa MAC ya da girişim modelinde bir şey yanlıştır ve
**bulmadan devam edilmez**."* §04.1'in kuralı da netti: sapmanın kabul
edilebilir açıklaması **ölçülen bir büyüklük** olmak zorunda.

**Eğrinin şekli soruyu daralttı:** `oran × atlama ≈ 0,74` ve N ≥ 5'ten sonra
**sabit**. Yani verim atlama sayısıyla ters orantılı — **uzamsal yeniden
kullanım yok gibi davranıyor.**

### ❌ Hipotez 1: taşıyıcı dinleme menzili çok geniş
Duyma menzili / iletim menzili = **6,31**; Li ~2 varsayar. Sınandı — duyma
menzili taranarak:

| duyma/iletim | 280 | 420 | 560 | 840 | 1260 | 1767 |
|---|---|---|---|---|---|---|
| oran | 0,031 | 0,031 | 0,073 | **0,091** | 0,079 | 0,074 |

🔴 **ÇÜRÜDÜ.** Menzili daraltmak düzeltmiyor, **kötüleştiriyor** (gizli
terminal çarpışmaları). Hiçbir değerde band'a girmiyor.

### ❌ Hipotez 2: 280 m'de bağ marjı sıfır
Güç çapası tanımı gereği o mesafede SINR **tam eşikte**; en küçük girişim
bile bağı kırar. Sınandı — aralık taranarak (100 → 280 m): oran **0,074 –
0,081** arasında, `oran × atlama` her aralıkta ≈ 0,74–0,81.
🔴 **ÇÜRÜDÜ.**

---

## 🟢 MEKANİZMA BULUNDU — ve sayısal olarak KAPANIYOR

Tahmin etmeyi bırakıp mekanizma doğrudan ölçüldü.

### Ölçüm 1 — uzamsal yeniden kullanım VAR
Birbirinden çok uzak K bağımsız çift, her biri kendi doygun akışıyla:

| çift | toplam verim | K × tek? |
|---|---|---|
| 1 | 356,1 | 1,000 |
| 2 | 711,9 | **1,000** |
| 4 | 1 423,9 | **1,000** |

🔒 Alet **serileştirmiyor**. Dört uzak çift tam dört katı veriyor.

### Ölçüm 2 — yeniden kullanım MESAFESİ
İki çift, aralarındaki mesafe taranarak (bağ uzunluğu 280 m):

| ayrım | 560 | 840 | 1120 | 1680 | **2240** | 3360 | 5000 |
|---|---|---|---|---|---|---|---|
| atlama | 2 | 3 | 4 | 6 | **8** | 12 | 18 |
| tek çifte oran | 1,05 | 1,05 | 1,05 | 1,07 | **2,00** | 2,00 | 2,00 |

🔒 **Yeniden kullanım mesafesi ≈ 8 atlama.** Li'nin modelinde 4.

### Türetme — ve tam sayısal kapanış
Girişim menzili, alınan gücün gürültü tabanına eşit olduğu mesafedir; iletim
menzili ise SINR'in eşiğe eşit olduğu mesafe. İkisinin oranı **kapalı formda**:

    girişim menzili / iletim menzili = 10^(SINR_eşiği / (10·α))
                                     = 10^(16 / 20) = **6,31**   (α = 2,0)

Ölçülen oran: **6,31** — birebir. Yeniden kullanım, girişimcinin alıcının
girişim menzilinin dışında olmasını gerektirdiği için ≈ 6,3 + 1 ≈ **7–8
atlama** — ölçülen 8.

**Zincir oranının öngörüsü:**

    Li:    yeniden kullanım 4 atlama → ideal 1/4 → 802.11 ile 1/7
           ⇒ 802.11 verimlilik çarpanı = (1/7)/(1/4) = 0,571
    Bizde: yeniden kullanım 8 atlama → 0,571 / 8 = **0,0714**

**Ölçülen: 0,0739.** Öngörüyle uyum **%4**.

---

## 🔒 KARAR: SAYI TUTMADI, **MEKANİZMA TUTTU** — ve sebep BEYAN EDİLMİŞ BİR TASARIM KARARI

Fark tek bir parametreden geliyor: **yol kaybı üsteli α**.

| | Li (yer tabanlı, ns-2) | bu proje |
|---|---|---|
| α | ~4 *(iki-ışın)* | **2,0** *(hava-hava serbest uzay)* |
| girişim/iletim oranı | 10^(16/40) = 2,5 | 10^(16/20) = **6,31** |
| yeniden kullanım | ~4 atlama | **8 atlama** |
| zincir oranı | 1/7 = 0,143 | **0,074** |

🔒 **α = 2,0 bu projede GEREKÇELİ bir karardır** (`07` §04: hava-hava serbest
uzay; iki-ışın kırılma mesafesi bağ mesafesinin çok üstünde) ve §04.1'de
*"taşıyıcı dinleme menzili sert değil"* diye **ölçümden önce** ilan edilen
farkın nicel hâlidir.

⭐ **Replikasyonun asıl sınadığı şey — MAC + girişim + uzamsal yeniden
kullanımın birlikte davranışı — DOĞRU ÇIKTI:** eğri Li'nin öngördüğü şekilde
düşüyor ve düzleşiyor (H2 ✅), ideal tavanın altında kalıyor (H3 ✅), ve
mutlak değer **yeniden kullanım mesafesinden %4 hatayla türetilebiliyor**.
Alet Li'nin fiziğini yeniden üretiyor; farklı bir yayılım rejiminde.

## 🔴 BU SONUCUN PROJEYE ETKİSİ — ve devredilen iş

1. **Çok atlamalı sonuçlar bu projede Li'ninkinden DAHA KÖTÜ olacak** ve
   sebebi bilinen bir fizik: α = 2'de girişim iletimden 6,3 kat uzağa
   gidiyor. Bu, sonuç bölümünde **beyan edilmesi gereken** bir bağlamdır.
2. 🔴 **AÇIK SINAV — öngörü henüz doğrulanmadı.** α = 3 ve α = 4 ile zincir
   koşusu denendi; α ≠ 2'de bağlar bozulup yeniden deneme fırtınası çıktığı
   için koşumlar bitmedi. Öngörü şu ve **sınanmayı bekliyor**:

       α = 3 → oran 3,41 → yeniden kullanım ~4–5 atlama
       α = 4 → oran 2,51 → yeniden kullanım ~3–4 atlama → zincir oranı BAND İÇİNDE

   🔒 Daha ucuz ve daha temiz yol: zincir yerine **iki çift probunu** α ile
   koşturmak — yeniden kullanım mesafesi doğrudan ölçülür.
3. **Ön-kayıtlı band GENİŞLETİLMEDİ** ve genişletilmeyecek. H1 tutmadı
   yazıyor ve öyle kalıyor.

---

# 🟢 EK — 9 Eylül 2026: **AÇIK SINAV KAPANDI**, mekanizma üç α'da doğrulandı

> Üretici: `python -u kalibrasyon/yeniden_kullanim.py`

Yukarıdaki açıklama tek bir α değerinde (2,0) kuruldu ve *"tesadüf olabilir"*
diye açık bırakılmıştı. Üç α değerinde ölçüldü.

## Yeniden kullanım mesafesi — iki çift probu, 280 m bağ

| ayrım / atlama | 2 | 3 | 4 | 6 | 8 | 12 | 16 |
|---|---|---|---|---|---|---|---|
| **α = 2,0** | 1,05 | 1,05 | 1,05 | 1,07 | **2,00** | 2,00 | 2,00 |
| **α = 3,0** | 1,05 | 1,07 | **1,96** | 2,00 | 2,00 | 2,00 | 2,00 |
| **α = 4,0** | 1,07 | 1,56 | **2,00** | 2,00 | 2,00 | 2,00 | 2,00 |

*(2,00 = iki çift tam paralel · 1,00 = tamamen serileştirilmiş)*

| α | girişim/iletim | **ölçülen mesafe** | ölçülen / oran |
|---|---|---|---|
| 2,0 | 6,31 | 8 atlama | 1,268 |
| 3,0 | 3,41 | 4 atlama | 1,171 |
| 4,0 | 2,51 | 3 atlama | 1,194 |
| | | ortalama | **1,211** · saçılma **%8** |

## 🔴 BİR ÖLÇÜT HATASI DAHA — ve kayda geçer
İlk yazdığım sınav *"mesafe ≈ oran **+ 1** atlama"* sezgisini kullanıyordu ve
α = 2'de tuttuğu için doğru sanılmıştı. Üç α'da ölçülünce **toplamsal sabitin
tutmadığı, ORANTININ tuttuğu** görüldü. Sınav, çarpanın DEĞERİNİ değil —
o ölçülüyor — **α'dan BAĞIMSIZLIĞINI** sınayacak biçimde yeniden yazıldı.

⚠️ Bu bir eşik gevşetmesi değil: kayda geçmiş öngörü (K-108 ve bu belgenin §SONUÇ 2. maddesi)
zaten *"α = 3 → ~4–5 atlama, α = 4 → ~3–4 atlama"* diyordu ve ölçülen 4 ile 3
**o bandların içinde**. Betikteki kapı, kayda geçmiş öngörüden daha katıydı;
düzeltilen şey kapıydı, öngörü değil.

## 🔒 SONUÇ
`yeniden kullanım mesafesi ≈ 1,21 × 10^(SINR_eşiği / (10·α))` — çarpan
2,5 katlık bir oran aralığında **%8 saçılmayla sabit**. Çarpanın 1'den büyük
olmasının sebebi de açık: PER eğrisi sert bir basamak değil, eşiğin biraz
altında da teslim var.

⭐ **Li ile aradaki fark bir kusur DEĞİL, yayılım rejimi farkıdır** — ve artık
üç ayrı α'da ölçülmüş, kapalı formda türetilmiş bir açıklamaya dayanıyor.
Aletin MAC + girişim + uzamsal yeniden kullanım katmanı **doğrulanmıştır**.

🔒 **H1 hâlâ "tutmadı" yazıyor ve öyle kalıyor.** Doğrulanan şey sayı değil,
sayının nereden geldiğidir.
