# Faz 5-3 · döngü kuralları: geri gönderme yasağı ve sınırlı yükselme, karıştırıcısız ikizde ve birincil hücrede — beklenti ve karar kuralı (ölçmeden önce)

> 24 Kasım 2026 · `v2/12` §1.2 · tasarım `v2/17` T-12'nin 20 Kasım eki · kurallar `v2/kural/KK-04` kural 13–14 (20 Kasım), kod `protokoller/desparete5*.py` (commit `a79f104`) · karşılaştırma tabanı: yeni çekirdeğin ölçümü (`../faz5_3_yeni_cekirdek_2026-11-19/`: 19 Kasım çekirdeği ve eğim0), teşhis (c) (Babel, kâhin). Sonuçlar ayrı `sonuc.md`ye yazılır; bu dosyaya dokunulmaz. Öngörüler duman koşusundan önce yazıldı ve commit'lendi. İki kural referans dünyada henüz hiç koşmadı; küçük test dünyasındaki davranışı aşağıda (karar girdisi değil).

## Neden bu ölçüm

Yeni çekirdeğin ölçümünde (`../faz5_3_yeni_cekirdek_2026-11-19/sonuc.md`) birincil hücrede eğimli kollar koşu başına binlerce döngü dönüşü yaşadı (19 Kasım çekirdeği 3620). Döngüler zor tohumlarda toplanıyor ve son çareyle birlikte artıyor (48 koşuda r = 0,95). Ortalama teslimde bedel görünmüyor (0,663 ↔ eğim0 0,665), ama:
- en kötü tohum 0,314 (eğim0 0,470);
- sessiz dönem 0,854 (eğim0 0,911);
- gecikmenin p99'u 1,77 s (eğim0 1,08 · Babel 1,31).

Döngüsüz eğim0 (18 Kasım'ın uygulanabilirlik koşulu) iki hücrede eğimle aynı teslim düzeyinde. İki kural eğimi döngüden kurtarabilir mi diye bakıyorum: kurtaramazsa yol seçiminde uygulanabilirlik koşuluna dönüş konuşulur. Sonuç, bu işten sonra yapılacak yeniden tasarımın (`v2/12`) girdisidir.

## Sorular

- **S1 · geri gönderme yasağı** (KK-04 kural 13): yalnız bu kural eklenince teslim ve döngü 19 Kasım çekirdeğine göre ne değişir?
- **S2 · sınırlı yükselme** (KK-04 kural 14): geri gönderme yasağının üstüne eklenince ne değişir?
- **S3 · eğim0 düzeyi** (karar): iki koldan biri birincil hücrede en kötü tohumda, sessiz dönemde, gecikmede ve döngüde eğim0'ın düzeyine geliyor mu, ikizde zarar vermeden?
- **S4 · tanı:** döngü, son çare, yol yok, tavan, kuralların kendi sayaçları (başka adaya yönlendirilen ve bekletilen paket, yükselme kopması), kaynak maliyeti, atlama sayısı.

## Düzen

    # bir adım = bir kol × bir hücre (dört adım)
    PYTHONIOENCODING=utf-8 py -3.11 -u <bu dizin>/olcum.py --dunya referans_2026 \
        --hucre ikiz|birincil --kollar <kol> \
        --tohumlar 1003,1004,1005,1006,1007,1008,1009,1010 --isci 8 --kayit <bu dizin>/kayit_<kol>_<hücre>.json

- **Hücreler** yeni çekirdeğin ölçümüyle aynı: İ (karıştırıcısız ikiz, hayalet çizelge 10:20; ölçü pencere PDR'si) ve B (`derin_sizma`, 15 s açık · 15 s sessiz; ölçü `PDR_açık`).
- **Kollar** (tohum 1003–1010; 2 kol × 2 hücre × 8 tohum = 32 koşu; değerler `KK-00`, `YUKSELME_PAYI` 4 ETX, `YUKSELME_UNUT_S` 4 s):

  | kol | `geri_yasagi` | `sinirli_yukselme` | ne ölçer |
  |---|---|---|---|
  | geri (`desparete5_geri`) | açık | kapalı | S1: geri − 19 Kasım |
  | **geri+sınır** (`desparete5_cekirdek`, 20 Kasım'ın varsayılanı) | açık | açık | S2: geri+sınır − geri |

  Öteki bayraklar 19 Kasım çekirdeği gibi: eğim, vazgeçme tetiği, iki ölçülü geçiş açık; karıştırmaya karşı mekanizmalar kapalı. `geri` kolu ölçüm aletinin içinde, koşu süresince profillere eklenir (`olcum.py`).
- **Karşılaştırılanlar yeniden koşulmaz:** 19 Kasım çekirdeği ve eğim0 yeni çekirdeğin ölçümünün, Babel ve kâhin teşhis (c)'nin kayıtlarından okunur.
  - Gerekçe: o ölçümün kopyasından (`63f9a45`) bu yana simülatörde, kayıp anatomisi aletinde, kâhinde ve Babel'de değişiklik yok (`git diff --stat 63f9a45 a79f104 -- sim2 kalibrasyon protokoller/babel* analiz`: yalnız `kalibrasyon/aodv_uygunluk.py`, profil eklendi).
  - Protokolün kodunda iki bayrak kapalıyken 19 Kasım'ın kodu birebir üretiliyor (küçük test dünyasında 12 koşu: `../faz5_3_kod_2026-11-20/esdegerlik.txt`).
  - Denetim (kural 0): duman koşusunda 19 Kasım çekirdeği (`desparete5_cekirdek_19k`) iki hücrede yeni çekirdeğin ölçümünün `cekirdek` duman satırıyla birebir olmalı (referans dünyada da).
- **Alet** (`olcum.py`): yeni çekirdeğin ölçümünün aleti, kaydedicisi aynı; yalnız kollar değişti. Kuralların sayaçları (`rota.geri_yasagi` · `rota.geri_bekletme` · `rota.yukselme_kopma`) protokolün tanısından gelir. İki sayaç karar başınadır: bekletilen bir paket her yeniden soruluşunda yeniden sayılır.
  - Denetim (kural 0): duman koşusunda geri+sınır kolu kaydediciyle ve doğrudan kayıp anatomisi aletiyle koşulur; iki satır bütün alanlarda birebir olmalı.
- **Küçük test dünyasındaki davranış** (karar girdisi değil; `sinama/kucuk_dunya.py` → `sinama/kucuk_dunya.txt`; 12 düğüm, tek tohum):
  - Karıştırıcılı senaryoda teslim 19 Kasım 656 · yalnız geri 657 · yalnız sınır 627 · ikisi 617 (839 paketten). Döngü dönüşü 4 · 4 · 26 · 32. Karıştırıcısız senaryoda dördü de birebir aynı.
  - Altı yükselme kopmasının ikisi gerçek iki düğümlü döngüyü kesti. Ötekiler karıştırma yüzünden maliyeti 4 saniye içinde yasal olarak yükselen düğümlerin yolunu kopardı (ör. düğüm 2: L 3,0, maliyeti 5,3'ten 7,1'e; ardılının ardılı başka düğüm); ardından gelen yol değişiklikleri yeni döngüler doğurdu.
  - Bu dünyada 19 Kasım çekirdeği hiç son çare yapmıyor (referans dünyanın birincil hücresinde koşu başına 141); döngünün kaynağı orada başka olabilir. Sayılar öngörüler yazılırken görüldü.
- **Yürütme:**
  - Koşu dondurulmuş kopyadan (`kopya/`, duman notunun commit'iyle dosya özeti birebir: `kopya_ozet.txt`), `kosu.sh` ile dört adımda; saatler `zaman.txt`e. Yanında başka ağır iş yok.
  - Sıra: bu beklenti commit'lenir → duman → duman notu bu dosyanın son bölümüne yazılır ve ikinci commit'le girer → o commit'ten dondurulmuş kopya → ölçüm. Adım sırası: geri+sınır (İ, B) → geri (İ, B).
  - Duman: `sh kosu.sh duman` (kısa pencere, tohum 1003; iki kol ve 19 Kasım çekirdeği iki hücrede, ayrıca geri+sınır kaydedicisiz; çalışma ağacından) → `duman_kisa.txt`. Ölçüm değil, hiçbir karara girmez.
  - Karar kuralının hesabı `sonuc_hesap.py` (koşudan önce yazıldı; ölçüler, eşli fark ve ayrışma kuralı yeni çekirdeğin ölçümünün betiğinden aynen alınır). Sınandı: 19 Kasım çekirdeğinin kayıtları sahte iki kol olarak verilince bütün bölümler çalıştı, farklar 0 çıktı, 19 Kasım çekirdeği K3–K6'yı geçmedi.
- **Süre tahmini ~4,5 sa (4–5,5):** adım başına İ'de 50–60 dk, B'de 70–85 dk. Dayanak: yeni çekirdeğin ölçümünde eğimli kolların adımları İ'de 51–60 dk, B'de 71–83 dk sürdü (`../faz5_3_yeni_cekirdek_2026-11-19/zaman.txt`). Duman ~25 dk.

## Tanımlar

Yeni çekirdeğin ölçümündeki gibi (`PDR_açık`, eşli fark, ayrışma kuralı: |ortalama| ≥ eşik ve 8 tohumun en az 6'sında aynı yön; kayıp grupları; kontrol payı; `R` = 0,0126). Bu ölçümde ayrıca:
- **Döngü dönüşü:** `rota.dongu`, bir paketin daha büyük atlama sayısıyla geri gelişi (KK-04 kural 9); paket başına değil, dönüş başına sayılır.
- **Sessiz dönem teslimi:** B'de karıştırıcının sessiz dönemlerinde doğan paketlerin teslim oranı.
- **En kötü tohum:** B'de 8 tohumun en düşük `PDR_açık`ı.

## Karar kuralı (8 tohum)

0. **Geçerlilik.**
   - 32 koşunun hepsi kayıtta; korunum geçerli, doğum çelişkisi 0, atfsız düşüş yok, kaydedicinin iç denetimleri geçmiş.
   - Karşılaştırma satırları 16'şar (19 Kasım çekirdeği, eğim0, Babel, kâhin).
   - Duman: geri+sınırın kaydedicili ve kaydedicisiz satırı iki hücrede bütün alanlarda birebir; 19 Kasım çekirdeği iki hücrede yeni çekirdeğin ölçümünün duman satırıyla birebir (ortak alanlar ve sayaçlar eşit, yeni sayaçlar sıfır).
   - Biri tutmazsa önce sebebi aranır; tablolar o zamana kadar kullanılmaz.
1. **S1 · geri gönderme yasağı:** `geri − 19 Kasım`, iki hücrede, eşli, eşik 0,02, ayrışma kuralıyla; ayrıca döngü dönüşü. Betimleyici; karar 3. maddededir.
2. **S2 · sınırlı yükselme:** `geri+sınır − geri`, aynı biçimde. Betimleyici.
3. **S3 · eğim0 düzeyi (karar).** Her kol için altı ölçüt; hepsi tutarsa kol "eğim0 düzeyinde"dir:
   - **K1:** B'de `PDR_açık(kol) − PDR_açık(eğim0)` eksi yönde ayrışmıyor (eşik 0,02).
   - **K2:** İ'de kol − eğim0 ve kol − 19 Kasım eksi yönde ayrışmıyor (ikizde zarar yok).
   - **K3:** B'de en kötü tohum ≥ eğim0'ın en kötü tohumu − 0,02 (0,470 − 0,02 = 0,450).
   - **K4:** B'de sessiz dönem teslimi, kol − eğim0, eksi yönde ayrışmıyor (eşik 0,02).
   - **K5:** B'de gecikmenin p99'u (tohum ortalaması) Babel'inkinden büyük değil (1,313 s).
   - **K6:** B'de döngü dönüşü (koşu başına) 19 Kasım çekirdeğininkinin en çok %10'u (≤ 362).

   Hüküm:
   - **Hiçbir kol eğim0 düzeyinde değil:** iki kural eğimi döngüden kurtarmadı. Yol seçiminde uygulanabilirlik koşuluna dönüş konuşulur; bu, yeniden tasarımın girdisidir.
   - **Bir kol eğim0 düzeyinde:** eğim o kuralla yeniden tasarımda aday kalır.
   - **İki kol da eğim0 düzeyinde:** B'de geri+sınır − geri artı yönde ayrışıyorsa geri+sınır, değilse daha az mekanizmalı olan geri aday kalır.
   - Kural hiçbir mekanizmayı kendiliğinden çıkarmaz; yeniden tasarımda neyin kalacağına bu sonuçla karar veririm.
4. **S4 · tanı** (betimleyici; sayaçlar bütün koşu, ağ toplamı, koşu başına): kayıp grupları (R · İ · K · T), kontrol payı ve bütün gönderim; döngü dönüşü, dışlama, bayat bilgi, son çare, zorunlu ve isteğe bağlı geçiş, veriye uygunsuzlukla geçiş, yol yok ve ortalama süresi, tavan aşımı, geri gönderme yasağının başka adaya yönlendirdiği ve beklettiği kararlar, yükselme kopması, vazgeçme tetiği, ara ilan, bekletme; kaynak maliyetinin p50 · p99'u, en büyüğü ve ∞ payı; teslimde 12 ve daha çok atlamalıların payı, kararlarda en büyük atlama; B'de tohum başına döngü dönüşü.
5. **Kâhin** yalnız referanstır (K-248).

## Öngörü

Düzeyler (8 tohum ortalaması; 19 Kasım çekirdeği, eğim0, Babel ve kâhin biliniyor):

| kol | İ · pencere PDR | B · `PDR_açık` | B · en kötü tohum | B · sessiz | B · p99 | B · döngü dönüşü / koşu |
|---|---|---|---|---|---|---|
| Babel | 0,930 | 0,663 | 0,485 | 0,916 | 1,31 s | — |
| eğim0 | 0,943 | 0,665 | 0,470 | 0,911 | 1,08 s | 0 |
| 19 Kasım | 0,954 | 0,663 | 0,314 | 0,854 | 1,77 s | 3620 |
| **geri** | **0,95–0,96** | **0,66–0,69** | **0,31–0,42** | **0,85–0,88** | **1,4–1,9 s** | **2000–3000** |
| **geri+sınır** | **0,94–0,955** | **0,60–0,69** | **0,28–0,45** | **0,83–0,90** | **1,2–2,0 s** | **500–3000** |

S1 (güven orta):
- İ'de geri − 19 Kasım −0,005 … +0,005 → ayırt edilemedi; döngü dönüşü 40–73.
- B'de +0,00 … +0,03 → en olası ayırt edilemedi.
- Dayanak: birincilde döngü dönüşlerinin en çok %45'i iki düğümlü (yeni çekirdeğin ölçümü, dışlama/döngü oranından üst sınır). Kural bunları paket dönmeden keser, ama paket bekletilir ya da başka adaya gider; üç ve daha çok düğümlü döngü sürer. Küçük dünyada yalnız geri 19 Kasım'la aynı düzeydeydi.

S2 (güven düşük):
- İ'de geri+sınır − geri −0,01 … +0,005 → ayırt edilemedi.
- B'de −0,06 … +0,03 → en olası ayırt edilemedi; ikinci olası eksi yönde ayrışma.
- Sınırın iki yönlü etkisi:
  - tavana tırmanmayı keser: B'de tavan aşımı 26,5'ten ~0'a iner;
  - maliyeti karıştırma yüzünden yasal olarak yükselen yolları da koparır: yükselme kopması B'de koşu başına 200–1500, yol yok 117'den 200–600'e çıkar, rota yokluğu kaybı 0,042'den 0,05–0,12'ye çıkar.
- Küçük dünyada sınır döngüyü artırdı (4 → 26).

S3 (güven orta):
- En olası hüküm "hiçbir kol eğim0 düzeyinde değil".
- K1 ve K2 iki kolda da büyük olasılıkla tutar. K6'yı (≤ 362) iki kolun da tutturması olası değil. K3, K4 ve K5'ten en az biri her kolda tutmaz.

S4 (güven düşük; koşu başına, B):
- geri: başka adaya yönlendirilen 200–2000 karar, bekletilen 300–3000 karar; son çare 100–160; tavan aşımı 15–30.
- geri+sınır: yükselme kopması 200–1500, son çare 100–300 (∞ ilanından sonra yokuş yukarı seçim artık son çare sayılır; KK-04 kural 3), tavan aşımı 0–5.
- İki kolda da TTL kaybı 0; kontrol payı %5–7; teslimde ≥ 12 atlama payı ≤ %1.

Kâhin: İ'de iki kol da kâhini 5–8 tohumda `R`'den fazla aşar; B'de en çok bir tohumda.

## Duman koşusundan sonra (ölçümden önce)

(Duman koşusundan sonra yazılır.)
