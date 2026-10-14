# 01 · PROBLEM, AMAÇ VE KAPSAM

> Projenin ne olduğu ve neyi başarı sayacağı. Durum ve takvim `12` · kararlar `04`. Güncel: 14 Ekim 2026; önceki sürümler `arsiv/01-PROBLEM-VE-AMAC-*.md`.

---

## 1 · Proje kartı

| | |
|---|---|
| yarışma | TÜBİTAK 2204-A Lise Öğrencileri Araştırma Projeleri · Yazılım / Bilgisayar Bilimleri |
| teslim | proje hedefi **19 Aralık 2026** · resmî son başvuru 4 Ocak 2027, 17:30 (TÜBİTAK 2204-A sayfası) |
| konu | karıştırma (jamming) altındaki taktik İHA mesh ağlarında yönlendirme |
| ürün | bu çalışmada önerilen protokol **DESPARETE** |
| kıyas tabanı | AODV · OLSRv2 (K-229) · Babel (K-242): reaktif, bağ durumu ve DESPARETE'yle aynı ailedeki uzaklık-vektörü protokolü |
| ölçüm ortamı | projenin kendi kesikli-olay simülatörü `sim2/` (K-001, K-090) |
| yürütücü | Xelma123 (lise öğrencisi); kapsam, gerçekçilik ve ön-kayıt kararları yürütücüye aittir. Yapay zekâ araçları danışman ve kod uygulayıcısı olarak kullanılmıştır (`README` · *Yapay zekâ kullanımı*) |

## 2 · Problem

Sürüde düğümler birbirinin paketini taşır. Karıştırıcı bağ kalitesini rastgele değil **yapılı** bozar: bir yerde durur ya da hareket eder, sürekli ya da darbeli yayın yapar, birden fazla olabilir. Ağın buna tepkisi sürünün haberleşmesini sürdürüp sürdüremeyeceğini belirler.

**Saha gerçekliği — kaynağın desteklediği kadar** (künyeler `02`):

| iddia | kanıt gücü | kullanım |
|---|---|---|
| Ukrayna'da aylık ~10 000 İHA kaybı; her 10 km cepheye ≥ 1 büyük EH sistemi | tahmin (RUSI; yazarlar kesin değil diyor) | yalnız mertebe |
| 2024'te FPV'lerin %60–80'i karıştırıldı | tahmin | "karıştırıldı", "hedefe ulaşamadı" değil |
| tek kanallı mesh (BATMAN-adv) karıştırmada bağlantıyı tamamen yitiriyor | deneysel (SPIDERMAN) | tek kanal kırılganlığı |
| çok atlamalı 802.11 zincirinde verim tek atlamanın ~1/7'si | yayımlanmış (Li vd.) | aletin dış çapası (`09`) |
| "AODV/OLSR karıştırmada < %50 PDR" | birincil kaynak yok | iddia edilmez; projenin ölçeceği şey |

**Literatürdeki iki boşluk** (tarama `protokol_kaynaklari/literatur_taramasi_2026-08-31/`, ikinci el):
- **A** — değişen karıştırma şiddetinde taban protokollerin PDR ve gecikme düşüşü, gerçekçi kanalda ve taktik ölçekte. En yakın çalışma Pu 2018 (JarmRout), OLSR ve DSR'nin PDR'sini karıştırıcı sayısına göre raporluyor; ama 1 km²'lik alanda, sönümlemesiz iki-ışın kanalla, sabit ve sürekli karıştırıcılarla (OMNeT++). Gerçekçi kanal, taktik ölçek, hareketli ve çizelgeli karıştırıcı yok.
- **B** — RF karıştırmada saniye ölçeğinde rota kurtarma gecikmesi.

Bu çalışma ikisini de ölçer.

**Alan kalabalık:** bir derleme 13 Q-öğrenme tabanlı FANET protokolü sayıyor; "ilk" ya da "eşi yok" iddiası kurulmaz. Ödül fonksiyonlarında karıştırma terimi bulunmadığı bilgisi taramanın matrisine dayanır: 11 protokolün 9'unda "açık jamming: hayır" (`02` §B).

## 3 · Kapsam

**Kapsam tanımı** (8 Eylül 2026): kontrollü bir deney ortamında yönlendirme protokolünün karıştırma karşısındaki davranışını izole etmek.

- Karıştırma tedavidir; geri kalan her şey kontrol değişkeni.
- Gerçekçilik esastır (K-168): 1:1 kaynaklı taktik sürü, gerçek telsizin verdiği gözlem (`14`). Kurulum bir taban protokolü haksız zayıflatmamalı; tehdit modeli sahaya paralel olmalı — karıştırıcılar birden fazla ve hareketli olabilir.
- Tam harp senaryosu (arazi, manevra, kara–hava harekâtı) kapsam dışı.

| dışarıda | neden |
|---|---|
| gerçek RF, SDR, uçuş testi | yasal engel, bütçe |
| sembol düzeyinde PHY | SINR → PER soyutlaması yeterli |
| kriptografi, GPS spoofing, video kodlama | ayrı alanlar |
| frekans çevikliği / çoklu kanal | öncül: çözüm yönlendirme katmanında aranıyor |
| GPSR | komşu konumunu ister (bedava verilmez); asıl zafiyeti GPS spoofing |
| içeriden saldırılar (seçici iletim, kara delik, sahte rota) | ele geçirilmiş düğüm; güven ve kimlik doğrulama alanı (K-230) |
| derin öğrenme (DQN vb.) | SWaP kısıtı |
| çok-etmenli oyun kuramı / MARL | kararsızlık riski |

## 4 · Amaç ve özgünlük

Bir **tasarım projesi**: çözüm kurulur ve kontrollü ortamda ölçülür. Hedef sırası:
1. bilimsel olarak savunulabilir bir yöntem;
2. önceden ilan edilmiş hipotezlerle ölçülmüş sonuç;
3. çalışan bir çözüm. Çözüm çalışmazsa sonuç, önceden ilan edilmiş yanlışlanma koşulu altında teşhis edilmiş bir negatif sonuçtur.

**Özgünlük** protokolün kendisinden gelir; taban protokollerin karıştırma altındaki ölçümü ikinci, bağımsız katkıdır. Katkının çerçevesi "ns-3 bunu yapamaz" değildir. Katkı üç parçadır (K-168):
- taktik İHA karıştırmasına özel, sızıntısız gözlem sözleşmeli, kâhin referanslı, ön-kayıtlı ve doğrulanmış bir deney düzeneği;
- protokolün kendisi;
- taban protokollerin bu düzenekteki ölçümü.

Bir mekanizmanın katkısı **ablasyonla** ölçülür.

**Yerli/milli bağlam:** elektronik harp altında çalışabilen, açık kaynak, Türkçe belgelenmiş bir kavram kanıtı; hiçbir kurumla temas ya da onay iddiası yok.

## 5 · İş akışı

Tek geçerli plan **Faz 0–7** (`12`):

| faz | iş |
|---|---|
| 0 | referans dünya |
| 1–3 | simülatörün gerçekçiliği |
| 4 | yeniden kalibrasyon ve taban protokoller |
| 5 | DESPARETE'nin karıştırma mekanizmaları |
| 6 | ön-kayıt ve mühür |
| 7 | ana deney ve yazım |

## 6 · Kısıtlar

| kısıt | değer |
|---|---|
| süre | hedef 19 Aralık 2026 (resmî son başvuru 4 Ocak 2027); yazıma ~5 hafta (`12` Faz 7) |
| platform | Windows, kişisel bilgisayar, tek makine |
| donanım | yok |
| anlaşılabilirlik | jüri önünde savunulamayacak hiçbir yöntem ya da iddia kullanılmaz |
| doğrulama | kendi simülatörünün bedeli: dört seviyeli doğrulama (`03` §4, `07` §1) |

Bir kısıt, gerekçesi ölçümle çürütülürse tarihli bir kararla değiştirilir; sonucun beklentiye uymaması gerekçe sayılmaz.

## 7 · Başarı ölçütü

| seviye | ölçüt |
|---|---|
| en az | doğrulanmış ölçüm ortamı + kaynağına sadık taban protokoller + istatistiksel olarak anlamlı herhangi bir bulgu |
| negatif sonuç | ana hipotez reddedilir; hangi koşulda ne kadar başarısız olduğu nicel gösterilir |
| hedef | ön-kayıtlı eşiği geçen, ablasyonla ayrıştırılmış kazanç |
| üstün | kazanç + hangi bilgi kanalından geldiğinin ölçülmesi |

Raporlanabilirlik için dört koşul birden (`06` §8): koşu uzunluğundan bağımsızlık · metriğin ne ölçtüğü doğrulanmış · taraflar arasında gizli asimetri yok · üreten kodun regresyon testi var.

## 8 · Simülasyon–gerçeklik beyanı (rapora aynen girer)

> Bu çalışma bir kavram kanıtıdır. Kullanılan yayılım ve karıştırma modelleri gerçek RF ortamının basitleştirilmiş temsilleridir. Elde edilen sayısal sonuçlar saha performansı öngörüsü olarak yorumlanmamalıdır; bulgular yalnızca modellenen koşullar altında **göreli** karşılaştırma olarak geçerlidir.
