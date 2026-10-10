# 01 · PROBLEM, AMAÇ VE İŞ AKIŞI

> Projenin ne olduğu ve neyi başarı sayacağı. Durum ve takvim `12` · kararlar `04`. Güncel: 10 Ekim 2026; önceki sürümler `arsiv/01-PROBLEM-VE-AMAC-*.md` (10 Eylül sürümünde TÜBİTAK kriter matrisi).

---

## 1 · Proje kartı

| | |
|---|---|
| yarışma | TÜBİTAK 2204-A Lise Öğrencileri Araştırma Projeleri · Yazılım / Bilgisayar Bilimleri |
| son teslim | **19 Aralık 2026** |
| konu | karıştırma (jamming) altındaki taktik İHA mesh ağlarında yönlendirme |
| ürün | **önerilen protokol DESPARETE**; AODV · OLSR · AOMDV kıyas tabanı |
| ölçüm ortamı | projenin kendi kesikli-olay simülatörü `sim2/` (K-001, K-090) |
| yürütücü | Xelma123 (lise öğrencisi); kapsam, gerçekçilik ve ön-kayıt kararları yürütücüye aittir. Yapay zekâ araçları danışman ve kod uygulayıcısı olarak kullanılmıştır (`README` · *Yapay zekâ kullanımı*) |

Resmî TÜBİTAK rehberi bu aşamada iş planına alınmamıştır; odak projenin kendisidir (10 Eylül).

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

**Literatürdeki iki boşluk** (tarama `protokol_kaynaklari/literatur_taramasi_2026-08-31/`): **A** — değişen karıştırma şiddetinde AODV/OLSR'nin raporlanmış PDR ve gecikme düşüşü · **B** — RF karıştırmada saniye ölçeğinde rota kurtarma gecikmesi. İkisini de bu proje ölçer; taban protokolleri bu eksende ölçmek tek başına bir katkıdır.

**Alan kalabalık:** bir derleme 13 Q-öğrenme tabanlı FANET protokolü sayıyor → "ilk", "eşi yok" savunulamaz; savunulabilir olan "hangi koşulda ne olduğunu ölçtük". Ödüllerde karıştırma terimi yok iddiası taramanın matrisine dayanır: 11 protokolün 9'unda "açık jamming: hayır" (1 Eylül; `02` §B). Küçük ağlarda (N ≤ ~40) tablo tabanlı yöntem uygun; büyük ağdaki boyut sorunu raporda yazılır.

## 3 · Kapsam

> **"Kontrollü bir deney ortamında routing protokolünün jamming karşısındaki davranışını izole etmek."** — kapsam tanımı, 8 Eylül 2026

- Karıştırma tedavidir; geri kalan her şey kontrol değişkeni.
- Gerçekçilik esastır (K-168, 25 Eylül): 1:1 kaynaklı taktik sürü, gerçek telsizin verdiği gözlem (`14`). Kurulum bir taban protokolü haksız zayıflatmamalı; tehdit modeli sahaya paralel olmalı — karıştırıcılar birden fazla ve hareketli olabilir.
- Tam harp senaryosu (arazi, manevra, kara–hava harekâtı) kapsam dışı.

| dışarıda | neden |
|---|---|
| gerçek RF, SDR, uçuş testi | yasal engel, bütçe |
| sembol düzeyinde PHY | SINR → PER soyutlaması yeterli |
| kriptografi, GPS spoofing, video kodlama | ayrı alanlar |
| frekans çevikliği / çoklu kanal | öncül: çözüm yönlendirme katmanında aranıyor |
| GPSR | komşu konumunu ister (bedava verilmez); asıl zafiyeti GPS spoofing (1 Eylül) |
| derin öğrenme (DQN vb.) | SWaP kısıtı; tablo tabanlı öğrenme bu kapsamda değil |
| çok-etmenli oyun kuramı / MARL | kararsızlık riski |

## 4 · Amaç ve özgünlük

Bir **tasarım projesi**: çözüm kurulur ve kontrollü ortamda ölçülerek savunulur. Sıralı hedefler: (1) bilimsel olarak dürüst ve savunulabilir · (2) olağanüstü yöntem olgunluğu · (3) mümkünse çalışan çözüm, değilse **iyi teşhis edilmiş negatif sonuç** — önceden ilan edilmiş bir yanlışlanmayı dürüstçe raporlamak taklidi en zor şeylerden biridir.

**Özgünlük** protokolün kendisinden; taban protokollerin karıştırma altındaki ölçümü ikinci, bağımsız katkı. Dürüst çerçeve: "ns-3 bunu yapamaz" değil — taktik İHA karıştırmasına özel, sızıntısız gözlem sözleşmeli, kâhin referanslı, ön-kayıtlı ve doğrulanmış bir deney düzeneği + protokol + taban protokollerin ölçümü (K-168). Bir mekanizmanın katkısı **ablasyonla** ölçülür. **Yerli/milli bağlam:** elektronik harp altında çalışabilen, açık kaynak, Türkçe belgelenmiş bir kavram kanıtı; hiçbir kurumla temas ya da onay iddiası yok.

## 5 · İş akışı

Tek geçerli plan **Faz 0–7** (`12`): 0 referans dünya · 1–3 simülatörün gerçekçiliği · 4 yeniden kalibrasyon ve taban protokoller · 5 DESPARETE'nin karıştırma mekanizmaları · 6 ön-kayıt ve mühür · 7 ana deney ve yazım. Eski kayıtlardaki "Aşama 1–5" 25 Eylül öncesinin numaralamasıdır: Aşama 1 simülasyon ve 2 taban protokoller (eski dünyada bitti) · 3 özgün protokol ≈ Faz 5 · 4 veri ≈ Faz 6–7 · 5 rapor ≈ Faz 7.

## 6 · Kısıtlar

| kısıt | değer |
|---|---|
| süre | 19 Aralık 2026; yazıma ~5 hafta, kısaltılmaz (`12` §2, Faz 7) |
| platform | Windows, kişisel bilgisayar |
| işlemci | deneyler çekirdeklerin yaklaşık yarısıyla (havuz 8 işçi); makine kullanılabilir kalmalı |
| donanım | yok |
| anlaşılabilirlik | jüri önünde savunulamayacak hiçbir yöntem ya da iddia kullanılmaz |
| doğrulama | kendi simülatörünün bedeli: dört seviyeli doğrulama (`03` §4, `07` §1) |

Kısıt, gerekçesi ayakta olduğu sürece geçerli; ölçüm gerekçeyi çürütürse tarihiyle revize edilir — "sonuç beğenilmedi" gerekçe değildir.

## 7 · Başarı ölçütü

| seviye | ölçüt |
|---|---|
| en az | doğrulanmış ölçüm ortamı + güçlü taban protokoller + istatistiksel olarak anlamlı herhangi bir bulgu |
| dürüst başarısızlık | ana hipotez reddedilir; hangi koşulda ne kadar başarısız olduğu nicel gösterilir |
| hedef | ön-kayıtlı eşiği geçen, ablasyonla ayrıştırılmış kazanç |
| üstün | kazanç + hangi bilgi kanalından geldiğinin ölçülmesi |

Raporlanabilirlik için dört koşul birden (`06` §8): koşu uzunluğundan bağımsızlık · metriğin ne ölçtüğü doğrulanmış · taraflar arasında gizli asimetri yok · üreten kodun regresyon testi var.

## 8 · Simülasyon–gerçeklik beyanı (rapora aynen girer)

> Bu çalışma bir kavram kanıtıdır. Kullanılan yayılım ve karıştırma modelleri gerçek RF ortamının basitleştirilmiş temsilleridir. Elde edilen sayısal sonuçlar saha performansı öngörüsü olarak yorumlanmamalıdır; bulgular yalnızca modellenen koşullar altında **göreli** karşılaştırma olarak geçerlidir.
