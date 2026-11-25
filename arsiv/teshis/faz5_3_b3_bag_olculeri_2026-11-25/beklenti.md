# Faz 5-3 · B3 teşhisi — bağın iki ölçüsü aynı bağda, bizim çekirdeğimizin trafiğinde — beklenti

> 25 Kasım 2026 · `v2/18` §2.3'ün teşhis ölçümü. Kararım: çekirdekte seçenek 2 (kullanılan bağın maliyeti veriden, kullanılmayanınki selamdan, eşikle düşürme yok), karıştırma ekinde E1 (karıştırılan bağ son çare). Bu dosya koşudan ve dumandan önce commit'lenir; öngörüler referans dünyada hiçbir koşu yapılmadan yazıldı. Sonuç ayrı `sonuc.md`ye yazılır, bu dosyaya dokunulmaz.
>
> Alet: `olcum.py` (kaydedici) · `bag.py` (saf işlevler; sınaması `sinama/saf.py`) · `kosu.sh` · karar hesabı `sonuc_hesap.py` (bu kuralın kodu; koşudan önce yazıldı).

## Amaç

B3'ün kâğıdının dört girdisini ölçmek:
1. Kullanılan bağda veri ölçüsü (`E_veri`), bağın sonraki veri bedelini selam ölçüsünden (`E_selam`) daha iyi kestiriyor mu? Seçenek 2'nin dayanağı budur.
2. Kaç veri kaydı "yeterli"; kayıt ne kadar eskiyince selam daha iyi?
3. Kullanılmayan bağın selam ölçüsü veri cinsine çevrilmeli mi? İki kaynak aynı terazide karşılaştırılacak.
4. Veri ölçüsü yükle ne kadar oynuyor (salınım riski, `17` T-4)?

Ayrıca betimleyici: selamı geçen ama veriyi taşımayan bağların sıklığı; karıştırma altında iki ölçünün tepkisi.

Bunlar `18` §2.1'in "B3'e kalan riskler"i ve §2.3'ün açık bıraktıklarıdır. B1'in kâğıdı bu teşhisi "ölçümde sayılacak tanı" olarak öngörmüştü (B1 §13).

## Sorular

- **S1 · Ayrışma:** aynı kullanılan bağda `E_veri` ile `E_selam` ne kadar ve hangi yönde ayrışıyor?
- **S2 · Verinin üstünlüğü:** kullanılan bağın sonraki veri bedelini hangisi daha iyi kestiriyor?
- **S3 · Yeterli kayıt ve tazelik:** veri ölçüsü kaç önceki kayıtla ve kaç saniyelik kayıtla selamdan iyi?
- **S4 · Dönüşüm:** selamın ölçüsü veri cinsine çevrilirse (genel katsayı ya da düğümün kendi katsayısı) sonraki veri bedelini daha iyi kestiriyor mu; çevirme kullanılmayan bağlara aktarılabilir mi?
- **S5 · Yükle oynama:** veri ölçüsü 10 s'de ne kadar değişiyor; yükle ilişkisi ne?
- **S6 · Selamı geçen, veriyi taşımayan bağ:** ne sıklıkta görülüyor, ne kadar sürüyor, kâhine göre iyi mi?
- **S7 · Karıştırma altında:** alıcısı karıştırılan kullanılan bağda iki ölçü ne kadar hızlı tepki veriyor?

## Düzen

- **Kol:** `desparete5_cekirdek`, B2 teşhisindekinin aynısı: karıştırmaya karşı mekanizmalar kapalı, geri gönderme yasağı ve sınırlı yükselme açık. Sebep: ölçüler trafiğe bağlıdır ve yeni tasarımın selamı bugünkü selamla aynı biçimde ve aralıkta gidecek (B1 Ö-1…Ö-4); en yakın trafik bu kolun trafiği. Kod B2 teşhisinin koduyla aynı (`git diff e6b0bb6` simülatörde, protokollerde ve araçlarda boş).
- **Hücreler** (`formasyon · yere_toplama`, tam pencere, 350 s):
  - **ikiz:** karıştırıcısız, hayalet çizelge 10:20;
  - **birincil:** `derin_sizma`, 15 s açık · 15 s sessiz.

  Dayanıklılık ve cephe hattı yok: sorular bağın genel ölçüsüyle ilgili; karıştırma altındaki davranış birincilde betimlenir (S7).
- **Tohumlar:** 1003–1010. **Seçim yarısı 1003–1006, doğrulama yarısı 1007–1010** (B2 teşhisindeki gibi). Seçimler seçim yarısında yapılır, hüküm doğrulama yarısındaki sayılarla verilir.
- **Koşu:** dondurulmuş kopyadan, hücre başına bir adım (8 tohum, 8 işçi), kayıp anatomisi aletinin işçisiyle. Kaydedici yalnız okuyan sarmalayıcılar takar; tek ek kanal meşgul integralidir (B2 teşhisinde birebir).
- **Ölçüler protokolün dışında hesaplanır:** kayıtlardan, B1'in kurallarıyla (`bag.py`). Protokolün bugünkü bağ ölçüsü kullanılmaz.

## Tanımlar

**Bağ ve ölçüleri** (gönderen i → alıcı j):
- **`E_selam`:** i'nin j'den aldığı selamlar ve j'nin selamında i için bildirdiği oranla B1 kural 4–7, 11–13; hariç aralık yok. Silme yalnız selamla ve i'nin j'ye onaylanan çerçeveleriyle (veri ve kontrol) tazelenir. Bu B1 kural 2'nin yaklaşığıdır: j'den duyulan öteki çerçeveler kayda girmez.
- **`E_veri`:** i'nin j'ye veri kayıtlarından B1 kural 8–9, 14. Önceki en çok n kayıt, son 30 s içinde; `D / G`; G = 0 ise ∞. "En çok 16 kayıtla" B1'in penceresidir (`VERI_PENCERE`).
- **Sonraki veri bedeli F:** örneğin kaydı dâhil, sonraki en çok 16 kayıt (30 s içinde) üzerinden `D / G`; G = 0 ise ∞. En az 4 kayıt yoksa F tanımsızdır ve örnek tahmin hesaplarına girmez.

**Örnekler:**
- **Veri örneği:** her bağda, ölçüm penceresinin (50–320 s) her tam saniyesindeki ilk veri kaydı. Ölçüler o kayıttan hemen önceki görünümle alınır (nedensel).
- **Izgara örneği:** her 5 s'lik dilimin ortasında, B1'de kayıtlı her bağ. Önceki 30 s'de veri kaydı olan bağ "kullanılan", olmayan "kullanılmayan"dır.

**Kâhin:** kayıp anatomisinin ölçüsü. Bağın tek deneme başarısı p: sönümleme dâhil, ağın kendi girişimi hariç, 5 s'lik dilimin ortasında (`kalibrasyon/kahin.py`, `_tek_deneme_basarisi`). Yalnız değerlendirmede kullanılır (`05` §8).

**Evre ve sınıf:** B2 teşhisinin tanımı (önce · açık · sessiz · geçiş · ikiz). Temiz sınıf: ikiz, önce, sessiz. Alıcının alanı (E · G · U) da B2 teşhisindeki gibidir.

**Hata:** bir tahminin F'ye göre hatası |log2(tahmin / F)|; iki değer 64'te kırpılır (∞ = 64). Birimi "bit"tir: 1 bit iki kat demektir. **OMH** (ortanca mutlak hata), bir örnek kümesindeki hataların ortancasıdır.

**Selamın dönüşümleri:**
- **D0:** `E_selam`.
- **D1:** k · `E_selam`. log2 k, seçim yarısının örnek kümesinde (K1) log2(F / `E_selam`)'ın ortancasıdır.
- **D2:** düğümün kendi katsayısı. (i, j)'nin t anındaki örneği için k_i = 2^ortanca{log2(`E_veri` / `E_selam`)}. Ortanca, i'nin j dışındaki bağlarının (t − 60 s, t) aralığındaki veri örneklerinden alınır: sınıfına bakılmadan, en az 8 önceki kayıtlı ve `E_selam`'ı sonlu olanlardan. Böyle en az 3 örnek yoksa D0 kullanılır.

## Karar kuralı (`sonuc_hesap.py`)

**K0 · Geçerlilik.** 16 koşu kayıtta, hepsi geçerli, iç denetimler geçti. Birebirlik: satırlar B2 teşhisinin satırlarıyla (`arsiv/teshis/faz5_3_b2_isaretler_2026-11-24/kayit_{ikiz,birincil}.json`; aynı kod, aynı tohum) PDR, pencere PDR'si, üretilen, teslim, simülatör sayaçları ve protokol sayaçlarında aynı. Tutmazsa tablolar kullanılmaz, sebep ölçülür.

**Örnek kümesi** (K1–K3): temiz sınıftaki veri örnekleri, `E_selam` sonlu, F tanımlı.

**K1 · Dönüşüm (S4).**
- Seçim yarısında D0, D1 ve D2'nin OMH'si hesaplanır. En düşüğü seçilir; ama D1 ya da D2, D0'dan en az 0,10 bit iyi değilse D0 seçilir.
- **Aktarılabilirlik:** ızgara örneklerinde (temiz sınıf, iki yarı, `E_selam` sonlu, p > 0) x = log2(`E_selam` · p). Kullanılmayan bağların x ortancası ile kullanılanlarınki arasındaki fark ≤ 0,5 bit ise aktarılabilir.
- **Hüküm:**
  - seçilen D1 ya da D2, doğrulama yarısında D0'dan en az 0,05 bit iyi ve aktarılabilir ise "dönüşüm var";
  - doğrulamada iyi ama aktarılamaz ise "kullanılan bağlarda iyi, aktarılamaz";
  - öteki hâllerde "dönüşüm yok".

  Yalnız "dönüşüm var"da seçilen dönüşüm Ês* olur; öteki hâllerde Ês* = D0.

**K2 · Verinin üstünlüğü (S2).** Doğrulama yarısında, en az 8 önceki kaydı olan örneklerde, OMH(`E_veri`, en çok 16 kayıt) ≤ OMH(Ês*) − 0,10 ise "veri üstün".

**K3 · Yeterli kayıt ve tazelik (S3).**
- n ∈ {1, 2, 3, 4, 6, 8, 12, 16} için en az n önceki kaydı olan örneklerde OMH(`E_veri`, son n kayıt) ve aynı örneklerde OMH(Ês*) hesaplanır.
- Seçim yarısında `VERI_EN_AZ`, OMH(`E_veri`) ≤ OMH(Ês*) − 0,05 olan en küçük n'dir. Doğrulamada o n'de OMH(`E_veri`) ≤ OMH(Ês*) ise "doğrulandı"; değilse doğrulamada bunu sağlayan en küçük n bildirilir.
- **Tazelik:** en az `VERI_EN_AZ` önceki kaydı olan örnekler, en yeni önceki kaydın yaşına göre dilimlenir: [0, 2) · [2, 5) · [5, 10) · [10, 20) · [20, 30] s. 30'dan az örnekli dilim sonrakiyle birleşir. Seçim yarısında en genç dilimden başlanır; OMH(`E_veri`, en çok 16 kayıt) ≤ OMH(Ês*) ardışık sağlandığı sürece ilerlenir. Sağlanan son dilimin üst sınırı `VERI_TAZE_S` olur. Doğrulamada aynı dilimler raporlanır.

**K4 · Yükle oynama (S5).**
- İkizde, bütün tohumlarda, aynı bağda yaklaşık 10 s arayla iki veri örneği alınır: ikincisi, ilkinden 9–11 s sonra gelen ilk örnektir; ikisinde de en az 8 önceki kayıt olmalı.
- |log2(`E_veri`(t + 10) / `E_veri`(t))| ≥ 1 olan çiftlerin payı %10'u aşarsa "oynama büyük".
- Betimleyici: log2 `E_veri` ile göndericinin ve alıcının son 10 s'deki kanal meşgul payı arasındaki sıra korelasyonu.

**K5 · Selamı geçen, veriyi taşımayan bağ (S6), betimleyici.** Temiz sınıfta, en az 8 önceki kaydı olan ve `E_selam`'ı sonlu veri örneklerinde `E_selam` ≤ 2 ve `E_veri` ≥ 4 (∞ dâhil) olanlar sayılır. Raporlananlar:
- bu örneklerin payı;
- bu durumu en az bir kez gösteren bağların payı;
- aynı bağda kesintisiz sürmesinin ortancası (örnekler arası en çok 2 s);
- bu örneklerde kâhinin p ≥ 0,28 olanların payı (7 denemelik başarının "iyi" bandı).

**K6 · Karıştırma altında (S7), betimleyici.** Birincilde, dönemin ortasında alıcısı G ya da E alanında olan bağ-dönemlere bakılır. Dönemden önceki 10 s'de en az bir önceki kaydı olan ve `E_selam`'ı sonlu bir veri örneği bulunmalı; o örneğin `E_veri`'si (en çok 16 kayıt) sonlu olmalı.
- Dönem içinde `E_veri`'nin (son 4 kayıt) dönem öncesi değerin iki katına ilk ulaştığı an ölçülür; `E_selam` için de aynısı.
- Raporlanan: 3 s içinde ve dönem içinde ulaşanların payı (alana göre) ve dönem içinde örneği olan bağ-dönemlerin payı.

**Hükmün kâğıda etkisi:**
- **K2 "veri üstün":** seçenek 2'nin dayanağı tutar. Kâğıt kullanılan bağın maliyetini `E_veri`'den yazar; `VERI_EN_AZ` ve `VERI_TAZE_S` K3'ten gelir.
- **K2 "değil":** seçenek 2'nin dayanağı tutmaz. Karar `18` §2.3'te yeniden konuşulur, kâğıt yazılmaz.
- **K1 "dönüşüm var":** kullanılmayan bağın maliyeti Ês*'dan, "yok": `E_selam`'dan. "Kullanılan bağlarda iyi, aktarılamaz" ise dönüşüm kullanılmayan bağlara uygulanmaz; iki kaynağın farkı B4'ün geçiş kuralına not edilir.
- **K4 "büyük":** kâğıt kullanılan bağın maliyetine düzgünleştirme yazar ve B4'ten iki ölçülü geçiş bekler. "Küçük" ise düzgünleştirme yok.
- **K5 ve K6:** betimleyici; kâğıdın örneklerine ve B2 ile etkileşimine girdi.

**Eşiklerin gerekçesi:**
- **0,10 bit (~%7):** OMH farkının pratik anlamı; daha küçüğü örnekleme oynamasıyla karışır. Doğrulamada 0,05: yarım örneklemde pay.
- **0,5 bit (~%41):** aktarılabilirlik. Selamın kâhine göre kötümserliği kullanılan ve kullanılmayan bağlarda bundan fazla ayrışırsa tek katsayı iki gruba birden uymaz.
- **10 s'de 1 bit (iki kat):** bir bağın maliyetinin yol seçimini değiştirecek kadar oynaması. %10: on karardan biri.
- **8 kayıt** (S1, K2, K4, K5): `VERI_PENCERE`'nin yarısı; daha azında ölçü kabadır.
- **F için en az 4 kayıt:** sonraki bedel kaba da olsa ölçülsün.

## Öngörüler (referans dünyada hiçbir koşudan önce)

Gerekçe:
- **açlık teşhisi:** selam eşiğindeki bağlarda `d_f · d_r` ~0,23, kâhin 0,71–0,76;
- **seçenek-iletim teşhisi:** veride tek deneme başarısı 0,46–0,49, onay %94–96;
- **yeni çekirdek:** vazgeçmeler birkaç bağda toplanıyor;
- **teşhis (d):** karıştırılan alıcıya çerçeve başına 3,9 ve 6,3 deneme.

Ardıl bağları bugünkü selam ölçüsüyle seçildiği için selamın en iyi gördüğü bağlardır. Orada selam çok kötümser değildir; veri ise 512 baytlık çerçeveyi ve vazgeçmeleri sayar.

| # | öngörü |
|---|---|
| 1 | K0: birebirlik tutar, iç denetimler geçer |
| 2 | S1: ikizde log2(`E_veri` / `E_selam`)'ın ortancası −0,3 … +1,0, en olası artı (veri selamdan pahalı gösterir); çeyrekler arası genişlik ≥ 0,8 bit |
| 3 | K2: veri üstün; doğrulamada OMH(`E_veri`) 0,3–0,7 bit, OMH(Ês*) 0,6–1,4 bit |
| 4 | K1: seçimde en olası D1, ikinci D0; D2 gürültülü, en az olası. Aktarılabilirlik farkı (kullanılmayan − kullanılan) +0,5 … +1,5 bit: kullanılmayan bağlarda selam kâhine göre daha kötümser; en olası "aktarılamaz". Hüküm en olası "kullanılan bağlarda iyi, aktarılamaz" ya da "dönüşüm yok" |
| 5 | K3: `VERI_EN_AZ` 2–4; doğrulanır. `VERI_TAZE_S` 10–30 s, en olası 30 |
| 6 | K4: çiftlerin %2–10'u; en olası "oynama küçük". Sıra korelasyonları 0,0–0,3 |
| 7 | K5: örneklerin %0,5–5'i; bağların %3–20'si; süre ortancası 3–15 s; kâhine göre iyi payı ≥ 0,8 |
| 8 | K6: G alanında `E_veri` 3 s içinde %25–60, `E_selam` ≤ %15; E alanında `E_veri` %25–60, `E_selam` ≤ %25 |
| 9 | Koşu başına veri örneği 6 000–15 000, ızgara örneği 15 000–35 000 |

## Aletin denetimi

- **Saf işlevler:** `sinama/saf.py`. Denetlenenler:
  - B1 sayımı: düzenli selam ve `d_f`, zaman aşımı, ileri sarma, geri alma, yeniden başlama, silme ve tazeleme, `d_f`'nin 30 s'de unutulması, `N_SELAM` penceresi, aynı anda olaylar, sorgunun nedenselliği, kayıt yokken;
  - `E_selam`, `E_veri`, kodlama, özet, hata.
- **Mekanik denetim:** öngörüler yazıldıktan sonra yapılır; ölçülen tohumların dışındaki 1001 tohumuyla, kısa pencerede, iki hücrede bir kez koşulur. Bakılan tek şey iç denetimlerin geçmesi ve karar hesabının hatasız bitmesidir; sayılar okunmaz. Bu, kodun commit'ten önce çalıştığını gösterir.
- **Duman** (bu commit'ten sonra): kısa pencere, tohum 1003, iki hücre, kaydediciyle. Satırlar B2 teşhisinin duman koşusundaki kaydedicisiz satırlarla (`arsiv/teshis/faz5_3_b2_isaretler_2026-11-24/duman/duz_{ikiz,birincil}.json`) birebir olmalı. Duman notu ayrı commit'le girer; karar girdisi değildir.

## Süre ve kayıt

- **Adım başına** (bir hücre, 8 tohum, 8 işçi): ~1–1,5 saat. Dayanak: B2 teşhisinde aynı kolun adımları ikiz 52 dk, birincil 72 dk sürdü. Kâhin ve B1 hesabı kaydın özetine eklenir; payı mekanik denetimde görülür.
- **Toplam:** ~2–3 saat. İki ağır iş birlikte koşulmaz.
- **Kayıt:** `kayit_<hücre>.json.gz`, ara kayıt `kayit_<hücre>.jsonl.gz` (sıkıştırılmış).

## Sınırlar

- Ölçüler bugünkü çekirdeğin trafiğinde alınır. Yeni tasarımın yolu (B4) ve iletimi (B5) trafiği ve hangi bağların kullanıldığını değiştirir. Değerler başlangıçtır; Aşama 4'te yeniden bakılır.
- Kullanılmayan bağın gerçek veri bedeli ölçülemez, çünkü o bağa veri gönderilmiyor. Aktarılabilirlik kâhinle dolaylı sınanır; kâhin ağın kendi girişimini saymaz.
- F yalnız örnekten sonra da aynı bağ kullanıldıysa tanımlıdır; ardıl değişince kesilir (seçim yanlılığı).
- B1'in silmesi teşhiste yalnız selamla ve onaylanan çerçevelerle tazelenir; j'den duyulan öteki çerçeveler yok sayılır. Fark ancak 30 s'den uzun sessizlikte ortaya çıkar.
- Yalnız formasyon kolu ölçülür; hareketli kollar (bağımsız, görev) ölçülmez.

## Duman notu (25 Kasım; dumandan sonra yazıldı, karar girdisi değil)

**Koşu:**
- `kosu.sh duman`, beklentinin commit'inden (`08b180e`) sonra, çalışma ağacından; 23:01–23:12, toplam ~12 dk.
- Kısa pencere, tohum 1003, iki hücre kaydediciyle, yan yana: ikiz 443 s (özeti 19 s), birincil 704 s (özeti 30 s).
- Çıktılar `duman/`, karar hesabının raporu `duman_kisa.txt`. Kayıt koşu başına ~53 KB (sıkıştırılmış).

**Geçerlilik:**
- İki hücrede kaydedicinin iç denetimleri geçti: meşgul dilimleri düğümlerin toplamına, MAC sonucu sayısı sayaca eşit; selam alındı; veri örneği var.
- Satırlar B2 teşhisinin kaydedicisiz duman satırlarıyla (`duz_ikiz.json`, `duz_birincil.json`) bütün alanlarda birebir.
- Sonuç: kaydedici, kanal meşgul sayacını açmak dâhil, davranışı değiştirmiyor.

**Aletin çalışması:**
- Karar hesabının bütün bölümleri doldu (K0–K6 ve S1).
- Kâhin çağrısı ızgara örneği sayısına eşit (3475 · 3362): veri örneklerinin dilimleri ızgaranınkilerle aynı, önbellekten okunuyor.
- Kısa pencerede tazelik dilimleri az örnekli. 5–10 s dilimi 30'dan az örnekle sonrakiyle birleşti; son dilim (20–30 s) 3 örnekle kaldı ve kural onu kendi başına değerlendirdi, çünkü sonrası yok. Tam koşuda örnek sayısı kabaca 9 (pencere) × 8 (tohum) katıdır.

**Tek tohumda görülenler** (karar girdisi değil; tek tohum, 30 s'lik pencere):
- S1: veri selamdan pahalı gösteriyor. log2(`E_veri` / `E_selam`)'ın ortancası ikizde +0,33, birincilde +0,29; örneklerin %76–78'inde `E_veri` > `E_selam`.
- K1: D1, D0'dan 0,04 bit iyi (0,10 sınırının altında), seçim D0; aktarılabilirlik farkı 0,40 bit.
- K2: `E_veri` 0,24 ↔ Ês* 0,39 bit.
- K3: `E_veri`'nin OMH'si kayıt sayısıyla düşüyor (1 kayıtta 0,71, 16 kayıtta 0,22 bit); 0,05 bitlik farkı ilk 6 kayıtta sağlıyor.
- K4: 437 çiftin hiçbiri 10 s'de iki katına değişmedi. `E_veri` ile alıcının yükü arasında sıra korelasyonu 0,41, göndericininkiyle −0,07.
- K5: ikizde örneklerin %2,8'i, bağların 6/69'u; hepsi kâhine göre iyi bantta.
- K6: `E_selam` hiçbir bağ-dönemde iki katına çıkmadı; `E_veri` 3 s içinde G alanında %22, E alanında 4 bağ-dönemin 1'inde.

**Değişmeyenler:** öngörüler, karar kuralı ve alet değişmedi. Süre tahmini aynı: adım başına ~1–1,5 saat, toplam ~2–3 saat. Tam pencerede özet koşu başına birkaç dakika ekler; adımın süresi en uzun tohumunkidir.
