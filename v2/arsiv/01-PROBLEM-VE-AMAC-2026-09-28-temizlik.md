# 01 · PROBLEM, AMAÇ VE İŞ AKIŞI

> **Güncel:** 25 Eylül 2026 (öz sürüm) · **Türü:** bilgi belgesi, çözüm içermez — *nasıl* (protokol tasarımı) öğrencinindir. Durum ve takvim `12` · kararlar `04` · önceki sürümler `v2/arsiv/01-PROBLEM-VE-AMAC-2026-09-10.md` (TÜBİTAK kriter matrisi) ve `…-2026-09-25.md`.

---

## 1 · Proje kartı

| | |
|---|---|
| yarışma | TÜBİTAK 2204-A Lise Öğrencileri Araştırma Projeleri · Yazılım / Bilgisayar Bilimleri |
| son teslim | **19 Aralık 2026** |
| konu | karıştırma (jamming) altındaki taktik İHA mesh ağlarında yönlendirme |
| ürün | **öğrencinin kendi protokolü (DESPARETE)**; AODV · OLSR · AOMDV kıyas tabanı |
| ölçüm ortamı | projenin kendi kesikli-olay simülatörü `sim2/` (K-001, K-090) |
| kim | tam zamanlı çalışan bir lise öğrencisi; fikirler ve kararlar onun. Yapay zekâ danışman ve uygulayıcı |

Resmî TÜBİTAK rehberi şimdilik iş planına girmiyor (öğrenci, 10 Eylül): odak projenin kendisi.

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

**Alan kalabalık:** bir derleme 13 Q-öğrenme tabanlı FANET protokolü sayıyor → "ilk", "eşi yok" savunulamaz; savunulabilir olan "hangi koşulda ne olduğunu ölçtük". Ödüllerde karıştırma terimi yok iddiası taramanın matrisine dayanır: 11 protokolün 9'unda "açık jamming: hayır" (öğrenci, 1 Eylül; `02` §B). Küçük ağlarda (N ≤ ~40) tablo tabanlı yöntem uygun; büyük ağdaki boyut sorunu raporda yazılır.

## 3 · Kapsam

> **"Kontrollü bir deney ortamında routing protokolünün jamming karşısındaki davranışını izole etmek."** — öğrenci, 8 Eylül 2026

- Karıştırma tedavidir; geri kalan her şey kontrol değişkeni.
- Gerçekçilik iki yerde gerekir: kurulum bir taban protokolü haksız zayıflatmamalı; tehdit modeli sahaya paralel olmalı — karıştırıcılar **birden fazla ve hareketli** (öğrenci, `07` §05).
- Tam harp senaryosu (arazi, manevra, kara–hava harekâtı) kapsam dışı.

| dışarıda | neden |
|---|---|
| gerçek RF, SDR, uçuş testi | yasal engel, bütçe |
| sembol düzeyinde PHY | SINR → PER soyutlaması yeterli |
| kriptografi, GPS spoofing, video kodlama | ayrı alanlar |
| frekans çevikliği / çoklu kanal | öncül: çözüm yönlendirme katmanında aranıyor |
| GPSR | komşu konumunu ister (bedava verilmez); asıl zafiyeti GPS spoofing (1 Eylül) |
| derin öğrenme (DQN vb.) | öğrenci kararı, SWaP; tablo tabanlı öğrenme bu kapsamda değil |
| çok-etmenli oyun kuramı / MARL | kararsızlık riski |

## 4 · Amaç ve özgünlük

Bir **tasarım projesi**: çözüm kurulur ve kontrollü ortamda ölçülerek savunulur. Sıralı hedefler: (1) bilimsel olarak dürüst ve savunulabilir · (2) olağanüstü yöntem olgunluğu · (3) mümkünse çalışan çözüm, değilse **iyi teşhis edilmiş negatif sonuç** — önceden ilan edilmiş bir yanlışlanmayı dürüstçe raporlamak taklidi en zor şeylerden biridir.

**Özgünlük** protokolün kendisinden; taban protokollerin karıştırma altındaki ölçümü ikinci, bağımsız katkı. **Fikir sahipliği:** her önemli kararın tarihli kaydı (`04`: kim önerdi, alternatifler, neden; ajan katkısı "ajan" diye etiketli) ve mekanizma katkısının **ablasyonla** ölçülmesi — "bu sayının ne kadarı size ait?" sorusunun en güçlü cevabı. **Yerli/milli bağlam:** EH altında çalışabilen, açık kaynak, Türkçe belgelenmiş bir kavram kanıtı; hiçbir kurumla temas, veri paylaşımı ya da onay iddiası yok.

## 5 · İş akışı — tek geçerli aşama numaralaması (öğrenci, 10 Eylül)

| aşama | ne | çıktı | durum (`12` §1 · §11) |
|---|---|---|---|
| 1 · Simülasyon | ölçüm ortamı, doğrulama, kontrol düzlemi, yere toplama, çoklu hareketli karıştırıcı, kalibrasyon | kalibre simülatör | 🟢 16 Eylül |
| 2 · Taban protokoller | AODV · OLSR · AOMDV RFC'ye sadık; U1–U4 | kabul edilmiş üç taban | 🟢 22 Eylül |
| 3 · Özgün protokol | öğrencinin tasarımı; her mekanizma ayrı bayrakla; geliştirme tohumlarında deneme | parametreleri sabit protokol | 🟡 sürüyor |
| 4 · Pürüz ve veri | ön-kaydın kesinleşmesi (hipotez · eşik · güç analizi); ana deney 40 tohum; istatistik; keşifsel eksenler | sonuç tabloları, GA | ⏳ |
| 5 · Rapor ve sunum | yazım; simülasyonun görselleştirilmesi (`07` §13) | rapor, poster, canlı gösterim | ⏳ |

"Aşama" bir iş dönemi, "aile" çoklu karşılaştırma düzeltmesinin birimi (`06`). Eski kayıtlardaki "Faz N" o günün numarasıdır: Faz 0 / Faz 1 duyarlılık + Li / Faz 2,5 kontrol düzlemi → Aşama 1 · Faz 1 rakip protokoller / Faz 2 dikey dilim / Faz 3 taban çizgileri → Aşama 2 · Faz 2 özgün / Faz 4 öğrencinin protokolü → Aşama 3 · mühür + Faz 5 tam deney → Aşama 4 · Faz 3 rapor / Faz 6 yazım → Aşama 5.

## 6 · Kısıtlar

| kısıt | değer |
|---|---|
| süre | 19 Aralık 2026; yazıma ~5 hafta, kısaltılmaz (`12` §11) |
| platform | Windows, öğrencinin kişisel makinesi |
| işlemci | deneyler çekirdeklerin yaklaşık yarısıyla (havuz 8 işçi); makine kullanılabilir kalmalı |
| donanım | yok |
| anlaşılabilirlik | öğrenci jüri önünde savunamadığı hiçbir şeyi tutmaz |
| doğrulama | kendi simülatörünün bedeli: dört seviyeli doğrulama (`03` §5, `07` §10) |

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
