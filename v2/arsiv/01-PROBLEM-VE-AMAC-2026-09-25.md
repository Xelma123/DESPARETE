# 01 · PROBLEM, AMAÇ VE İŞ AKIŞI

> **Güncel:** 10 Eylül 2026 · **Türü:** bilgi belgesi — çözüm içermez.
> Durum ve iş planı: `12-YOL-HARITASI.md` · karar geçmişi: `04-NEDEN-BOYLE.md`.
> Önceki sürüm (TÜBİTAK kriter matrisi dâhil): `arsiv/01-PROBLEM-VE-AMAC-2026-09-10.md`.

Bu belge *neyin* çözülmeye çalışıldığını, *hangi sınırlar içinde* ve *neyin
başarı sayılacağını* anlatır. *Nasıl* çözüleceği — özgün protokolün tasarımı —
öğrencinindir ve burada yoktur.

---

## 1 · Proje kartı

| | |
|---|---|
| Yarışma | TÜBİTAK 2204-A Lise Öğrencileri Araştırma Projeleri · Yazılım / Bilgisayar Bilimleri |
| Son teslim | **19 Aralık 2026** |
| Konu | Karıştırma (jamming) altındaki taktik İHA mesh ağlarında yönlendirme |
| Ürün | **Öğrencinin kendi yönlendirme protokolü.** AODV · OLSR · AOMDV kıyas tabanıdır |
| Ölçüm ortamı | Projenin kendi kesikli-olay simülatörü (`sim2/`) — K-001, K-090 |
| Kim | Tam zamanlı çalışan bir lise öğrencisi; fikirler ve kararlar onundur. Yapay zekâ danışman ve uygulayıcıdır |

Resmî TÜBİTAK rehberi şimdilik iş planına girmiyor (öğrenci, 10 Eylül 2026):
odak, projenin kendisi.

---

## 2 · Problem

Bir İHA sürüsü tek bir merkeze değil birbirine bağlıdır: düğümler birbirinin
paketini taşır. Karıştırıcı devreye girdiğinde bağlantı kalitesi rastgele
değil **yapılı** biçimde bozulur — karıştırıcı bir yerde durur ya da hareket
eder, sürekli ya da darbeli yayın yapar, birden fazla olabilir. Ağın bu
bozulmaya nasıl tepki verdiği, sürünün haberleşmesini sürdürüp
sürdüremeyeceğini belirler.

### 2.1 Saha gerçekliği — kaynağın desteklediği kadar

| iddia | kanıt gücü | kullanım |
|---|---|---|
| Ukrayna'da aylık ~10 000 İHA kaybı; her 10 km cepheye ≥ 1 büyük EH sistemi | tahmin (RUSI; yazarlar kesin olmadığını belirtiyor) | yalnız büyüklük mertebesi |
| 2024'te FPV'lerin %60–80'i karıştırıldı | tahmin | "karıştırıldı" demek; "hedefe ulaşamadı" değil |
| Tek kanallı mesh (BATMAN-adv) karıştırma altında bağlantıyı tamamen yitiriyor | deneysel (SPIDERMAN) | tek kanal kırılganlığı |
| Çok atlamalı 802.11 zincirinde verim tek atlamanın ~1/7'si | yayımlanmış (Li vd.) | aletin dış çapası — `09` |
| "AODV/OLSR karıştırma altında < %50 PDR" | birincil kaynak yok | iddia edilmez; projenin ölçeceği şeydir |

Künyeler ve doğrulama durumu: `02-DOGRULANMIS-KAYNAKLAR.md`.

### 2.2 Literatürdeki iki boşluk

İkinci literatür taraması (`protokol_kaynaklari/literatur_taramasi_2026-08-31/`, 31 Ağustos 2026)
şunları bulamadı:

- **A:** AODV, OLSR gibi protokoller için değişen karıştırma şiddeti altında
  raporlanmış PDR ve uçtan uca gecikme düşüşleri.
- **B:** RF karıştırma altında saniye ölçeğinde **rota kurtarma gecikmesi**.

İkisi de bu projenin ölçeceği şeydir. Taban protokolleri bu eksende ölçmek
tek başına bir katkıdır.

### 2.3 Alan kalabalık

Bir derleme 13 Q-öğrenme tabanlı FANET yönlendirme protokolü sayıyor.
Dolayısıyla *"ilk"*, *"eşi yok"* gibi iddialar savunulamaz; savunulabilir olan
*"hangi koşulda ne olduğunu ölçtük"*tür. Ödül fonksiyonlarında karıştırma
terimi bulunmadığı iddiası yeni taramanın kendi matrisine dayanır: 11
protokolün 9'unda "açık jamming: hayır" (öğrenci kararı, 1 Eylül 2026;
ayrıntı `02` §B). Küçük ağlarda (N ≤ ~40) tablo tabanlı yöntemler uygundur;
büyük ağlardaki boyut sorunu raporda yazılır.

---

## 3 · Kapsam

> **"Kontrollü bir deney ortamında routing protokolünün jamming karşısındaki
> davranışını izole etmek."** — öğrenci, 8 Eylül 2026

- **Karıştırma tedavidir; geri kalan her şey kontrol değişkenidir.** Kontrol
  değişkenleri ne kadar iyi sabitlenirse izolasyon o kadar temizdir.
- **Gerçekçilik iki yerde gereklidir:** (1) kurulumun bir taban protokolü
  haksız biçimde zayıflatmaması; (2) tehdit modelinin sahadaki karıştırıcı
  davranışına paralel olması — öğrenci kararıyla karıştırıcılar **birden
  fazla ve hareketli** olacak (`07` §05).
- **Tam bir harp senaryosu kapsam dışıdır:** arazi, taktik manevra planı ya
  da kara–hava bütünleşik harekât modellenmez.

### 3.1 Kapsam dışı olanlar

| dışarıda | neden |
|---|---|
| gerçek RF, SDR, uçuş testi | yasal engel ve bütçe |
| sembol düzeyinde PHY (OFDM, modülasyon ayrıntısı) | SINR → PER soyutlaması yeterli |
| kriptografi, GPS spoofing, video kodlama | ayrı proje alanları |
| frekans çevikliği / çoklu kanal | projenin öncülü: çözüm yönlendirme katmanında aranıyor |
| GPSR | komşu konumunu ister (bedava verilmez) ve asıl zafiyeti kapsam dışı olan GPS spoofing (1 Eylül 2026) |
| derin öğrenme (DQN vb.) | öğrenci kararı — SWaP kısıtı; tablo tabanlı öğrenme bu kapsamda değil |
| çok-etmenli oyun kuramı / MARL | kararsızlık riski |

---

## 4 · Amaç ve özgünlük

Bu bir **tasarım projesidir**: bir çözüm kurulur ve kontrollü bir ortamda
**ölçülerek** savunulur. Pasif bir *"şunları test ettik"* çalışması değildir.

Sıralı hedefler:

1. Bilimsel olarak dürüst ve savunulabilir bir çalışma.
2. Olağanüstü bir yöntem olgunluğu.
3. Mümkünse çalışan bir çözüm; değilse **iyi teşhis edilmiş bir negatif
   sonuç**. Önceden ilan edilmiş bir yanlışlanma koşulunu dürüstçe
   raporlamak, jüri önünde taklidi en zor şeylerden biridir.

**Özgünlük** protokolün kendisinden gelir. Taban protokollerin karıştırma
altındaki ölçümü (§2.2) ikinci, bağımsız bir katkıdır.

**Fikir sahipliği.** Yapay zekâyla çalışıldığı için iki alışkanlık baştan
tutulur: her önemli kararın tarihli kaydı (`04`: kim önerdi, alternatifler,
neden bu) ve bir mekanizmanın katkısının **ablasyonla ölçülmesi**. Ölçülmüş
bir katkı payı, *"bu sayının ne kadarı size ait?"* sorusuna en güçlü cevaptır.

**Yerli/milli bağlam.** Milli sürü platformlarının ihtiyaç duyduğu alanda,
elektronik harp altında çalışabilen, açık kaynak ve Türkçe belgelenmiş bir
*kavram kanıtı*. Hiçbir kurumla temas, veri paylaşımı ya da onay iddiası
yapılmaz.

---

## 5 · İş akışı — öğrencinin taslağı, ayrıntılandırılmış

Öğrencinin 10 Eylül 2026'da tarif ettiği akış beş aşamadır. Bu numaralama
projedeki **tek geçerli** aşama numaralamasıdır; eski "Faz" numaralamaları
emeklidir (eşleşme aşağıda).

| aşama | ne yapılır | çıktı |
|---|---|---|
| **1 · Simülasyon** | Ölçüm ortamının kurulması, doğrulanması ve eksik yeteneklerin eklenmesi: kontrol düzlemi (bitti), yere toplama trafiği, çoklu hareketli karıştırıcı, mobilite kararı, açık doğruluk soruları, yeniden kalibrasyon. **Hedef: 26 Eylül 2026'ya kadar bitirmeye çalışmak** — kilitli bir tarih değil | Protokol yazmaya hazır, kalibre edilmiş simülatör |
| **2 · Protokollerin yapımı ve denenmesi** | AODV, OLSR, AOMDV'nin RFC'ye sadık yazılması; önce biri uçtan uca; uygunluk testleri (U1–U4); protokol olmadan kapanamayan borçlar | Kabul edilmiş üç taban protokol |
| **3 · Özgün protokolün tasarımı** | Öğrencinin tasarımı ve gerçeklemesi; her mekanizmanın ayrı bir bayrakla açılıp kapanabilmesi; geliştirme tohumlarında deneme | Parametreleri sabitlenmiş özgün protokol |
| **4 · Pürüz temizleme ve veri toplama** | Ön-kaydın kesinleştirilmesi (hipotez · eşik · güç analizi); ana deney (40 tohum); istatistik; keşifsel eksenler | Sonuç tabloları ve güven aralıkları |
| **5 · Rapor ve sunum** | Rapor yazımı; sunumda **simülasyonun işleyişinin görselleştirilmesi** (`07` §13) | Rapor, poster, canlı gösterim |

"Aşama" bir iş dönemidir; "aile" ise istatistikte çoklu karşılaştırma
düzeltmesinin birimidir (`06`). İkisi ayrı kavramlardır.

**Eski numaralamaların karşılığı:**

| eski ad | yeni karşılığı |
|---|---|
| Faz 0 ölçüm aracı (`01`, 1 Eylül) · Faz 0 simülatör, Faz 1 duyarlılık + Li, Faz 2,5 kontrol düzlemi (`DEVIR`/`12`, 9 Eylül) | Aşama 1 |
| Faz 1 rakip protokoller · Faz 2 dikey dilim, Faz 3 taban çizgileri | Aşama 2 |
| Faz 2 özgün protokol · Faz 4 öğrencinin protokolü | Aşama 3 |
| ön-kayıt mührü + Faz 5 tam deney | Aşama 4 |
| Faz 3 rapor · Faz 6 yazım | Aşama 5 |

Eski kayıtlarda geçen "Faz N" ifadesi o günün numaralamasıdır; anlamı kaydın
tarihine göre okunur.

---

## 6 · Kısıtlar

| kısıt | değer |
|---|---|
| süre | 19 Aralık 2026; rapor yazımına son haftalar ayrılır (`12` §6) |
| platform | Windows, öğrencinin kişisel makinesi |
| işlemci | deneyler çekirdeklerin yaklaşık yarısıyla koşar; makine kullanılabilir kalmalı |
| donanım | yok — gerçek RF, SDR, uçuş testi kapsam dışı |
| anlaşılabilirlik | öğrenci jüri önünde savunamadığı hiçbir şeyi projede tutmaz |
| doğrulama | kendi simülatörünü yazmanın bedeli: dört seviyeli doğrulama (`03` §5, `07` §10) |

Bir kısıt, gerekçesi ayakta olduğu sürece geçerlidir. Ölçüm gerekçeyi
çürütürse kısıt tarihiyle revize edilir; *"sonuç beğenilmedi"* bir revizyon
gerekçesi değildir.

---

## 7 · Başarı ölçütü

| seviye | ölçüt |
|---|---|
| en az | doğrulanmış ölçüm ortamı + güçlü taban protokoller + istatistiksel olarak anlamlı herhangi bir bulgu |
| dürüst başarısızlık | ana hipotez reddedilir, ama hangi koşulda ve ne kadar başarısız olduğu nicel olarak gösterilir |
| hedef | ön-kayıtlı eşiği geçen, ablasyonla ayrıştırılmış bir kazanç |
| üstün | kazanç + o kazancın hangi bilgi kanalından geldiğinin ölçülmesi |

Bir sonucun raporlanabilmesi için dört koşul gerekir: (1) koşu uzunluğundan
bağımsız olması, (2) metriğin ne ölçtüğünün doğrulanmış olması, (3)
karşılaştırılan taraflar arasında gizli asimetri olmaması, (4) sonucu üreten
kodun regresyon testinin olması. Ayrıntı `06` §8.

---

## 8 · Simülasyon–gerçeklik beyanı (rapora aynen girer)

> Bu çalışma bir kavram kanıtıdır. Kullanılan yayılım ve karıştırma
> modelleri gerçek RF ortamının basitleştirilmiş temsilleridir. Elde edilen
> sayısal sonuçlar saha performansı öngörüsü olarak yorumlanmamalıdır;
> bulgular yalnızca modellenen koşullar altında **göreli** karşılaştırma
> olarak geçerlidir.
