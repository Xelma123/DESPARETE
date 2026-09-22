# 07 · SİMÜLATÖR TASARIMI

> **Güncel:** 10 Eylül 2026 · **Türü:** bilgi belgesi — simülatörün ne olduğu,
> neden böyle olduğu, neyin uygulandığı ve Aşama 1'de neyin değişeceği.
> Karar geçmişi: `04` (K-090…K-113) · iş listesi: `12` §3 · önceki sürüm:
> `arsiv/07-SIMULATOR-TASARIMI-2026-09-10.md`.
>
> İşaretler: 🟢 uygulandı · 🟡 öğrenci kararı verildi, uygulanacak ·
> 🔵 ajan önerisi, öğrenci kararı ya da yapı onayı bekliyor · ⚪ açık soru.

---

## 00 · Bu belge neden var

Simülatör aşağıdan yukarı kuruldu ve her katmanın kendi kapanış ölçütü vardı;
ama o ölçütler *"bu katman kendi içinde doğru mu"* diye soruyordu. Bu belge
simülatörü **yapılacak ölçüme göre** tarif eder. İddianın savunulabilmesi
için beş şey gerekir: tehdit modeli · ağ modeli · sadık taban protokoller ·
iddiayı ölçebilen metrikler · ön-kayıtlı istatistik.

---

## 01 · Ne ölçüyoruz

### 01.1 · İddia yapısı

*Karıştırma altında, önerilen yönlendirme protokolü AODV / OLSR / AOMDV'ye
göre [şu metriklerde] [şu kadar] farklı davranır.*

### 01.2 · Aletin geçmesi gereken üç sınav

| sınav | soru | durum |
|---|---|---|
| iç tutarlılık | sayaçlar birbirini tutuyor mu | 🟢 korunum + mutabakat |
| analitik | bilinen formüllerle uyuşuyor mu | 🟢 Bianchi · sönümleme varyansı · yol kaybı |
| dış çapa | yayımlanmış bir sonucu yeniden üretiyor mu | 🟢 Li vd.: mekanizma doğrulandı, sayı farkı yol kaybı üsteliyle açıklandı (§10, `09`) |

---

## 02 · Dünya modeli

- Simülasyon hacmi, sürünün kütle merkezine bağlı **hareketli bir gözlem
  çerçevesidir**; modellenen hızlar göreli hızlardır. Sürünün ortak hareketi
  ağa görünmez (Galileo değişmezliği).
- Yer referanslı varlıklar (karıştırıcılar, yer istasyonu) bu çerçevede
  **hareket eder**. Öğrencinin hareketli karıştırıcı kararı (§05.3) bu modelle
  doğal olarak örtüşür.
- **Ölçek modeli:** 1:50; kutu yaklaşık 90 km'ye, hızlar 45–135 km/h'e,
  verici gücü 2,5 W'a karşılık gelir (K-101). Ölçeklenemeyen tek büyüklük dalga
  boyudur: Doppler tam ölçek hızından hesaplanır (K-102).
- **Ölçek tutarlılığı bir kapıdır:** tam ölçekteki verici fiziksel olarak var
  olabilmelidir (bu kapı α = 3'ü eledi).

---

## 03 · Mobilite

### 03.1 · Ölçüt: çalkantı sayısı Θ — bir kapı

```
Θ = ortalama rota ömrü / 15 s        (OLSR TOP_HOLD_TIME, RFC 3626)
kapı: Θ ≥ 3
```

Θ'nın altında OLSR'ın topoloji bilgisi kullanılmadan bayatlar; bu bir kurulum
straw-man'i olurdu (K-101). Rota ömrü, yavaş SINR bağ tanımı ve Kaplan–Meier
kestiricisiyle ölçülür (K-110 EK-3).

### 03.2 · Bugünkü kollar 🟢

| kol | model | hız (1:50'de) | Θ | not |
|---|---|---|---|---|
| statik | sabit konum | 0 | ∞ | U1 için referans |
| çekirdek (bağımsız) | Gauss-Markov 3B | 0,25–0,75 m/s (45–135 km/h) | **3,25** | kapının %8 üstünde |
| keşifsel yüksek çalkantı | Gauss-Markov 3B | 0,5–1,5 m/s (90–270 km/h) | **1,78** | kapının altında — §03.3 |
| görev (müfreze) | müfreze tabanlı | çekirdekle aynı | ölçülmedi | `gorev_grup_sayisi` (10 × 4) · `gorev_grup_yaricapi_m` (650 m, ölçüm bayat) · `gorev_jitter_hiz_ms` |

Üretici (Θ): `python -u kalibrasyon/bag_kumesi.py f g h`. Hız korelasyonu ve
dönüş hızı araç dinamiğinden türetildi ve ölçeklenmedi (K-101).

### 03.3 · Yüksek çalkantı kolu deneyden saklanmaz 🟡

**Öğrenci kararı (10 Eylül 2026):** kapının altında kalan bir kol saklanmaz ya
da halının altına süpürülmez; bir sorun varsa düzeltilir.

**Kapının anlamı yeniden okundu.** Θ, en yavaş taban protokolün (OLSR) topoloji
zaman sabitine göre tanımlı. Aynı rota ömürleri AODV'nin zaman sabitine
(`ACTIVE_ROUTE_TIMEOUT` = 3 s) bölününce:

| kol | rota ömrü τ | Θ_OLSR = τ / 15 s | Θ_AODV = τ / 3 s |
|---|---|---|---|
| çekirdek | 48,8 s | 3,25 | 16,3 |
| yüksek çalkantı | 26,7 s | 1,78 | 8,9 |

*(τ: K-110 EK-3, `bag_kumesi.py f g h`; bölmeler hesaptır.)*

Yani yüksek çalkantı kolu **yalnız OLSR'ın** tasarım zarfının dışındadır;
reaktif protokollerin zarfının içindedir. Bu bir kurulum hatası değil, bir
**bulgu üretebilecek stres koludur**: *"proaktif bir protokolün topoloji
zamanı bu çalkantıda yetmiyor"* gözlenebilir ve raporlanabilir bir sonuçtur.

Straw-man'e dönüşmemesi için:

- Kolun sonuçları her zaman **iki Θ değeriyle** ve *"OLSR tasarım zarfının
  dışında"* etiketiyle raporlanır.
- Kol çekirdek hipotez ailelerine girmez; keşifsel eksende **tam olarak**
  raporlanır.
- 🟢 **Tek-sayılı Θ düzeltildi** (14 Eylül 2026, Y7 · `04` K-122): Θ her
  taban protokol için ayrı ölçülür ve her sonuç satırının kapsam bölümüne
  `theta_olsr` ile `theta_aodv` olarak yazılır. Ölçüm dört mobilite kolunu
  birden kapsar (`python -u kalibrasyon/theta_kollari.py`).

### 03.4 · Mobilite modeli — ajan önerisi 🔵

Öğrenci sordu: daha mantıklı bir tercih var mı? Öneri (ölçümle doğrulanacak):

1. **Çekirdek kol: formasyon + istasyon tutma.** Her düğümün formasyon içinde
   bir istasyonu olur. Düğüm istasyonunu manevra gürültüsüyle tutar; gürültünün
   zaman sabiti araç dinamiğidir (~30 s, K-101) ve istasyonlar yavaşça yeniden
   düzenlenir. Gerekçe:
   - **Kapsam:** mobilite bir kontrol değişkenidir; karıştırmayı izole etmek
     için çalkantı kontrollü olmalıdır.
   - **Gerçekçilik:** bir sürü formasyonla uçar, düğümler rastgele yürümez.
     Sürünün ortak hareketi ağa zaten görünmez (§02).
   - **Kapı marjı:** bugün %8; istasyon tutmada çalkantı azalır ve marj büyür.
   - **Hareketin asıl kaynağı değişir:** yer referanslı varlıklar
     (karıştırıcılar, geçit) sürü çerçevesinden geçer. Gerçek bir sürüde
     bağların bozulma sebebi büyük ölçüde budur.
   - **Bedeli:** çekirdek statik kola yaklaşır. Çalkantı ekseni bu yüzden
     keşifsel kollarda korunur.
2. **Keşifsel kollar:** bugünkü Gauss-Markov kolları (Θ 3,25 ve 1,78, §03.3
   etiketiyle).
3. **Görev kolu:** öğrenci kararıyla yarıçap daha büyük örneklemle yeniden
   ölçülecek. İstasyon tutma kabul edilirse müfreze yapısı istasyon düzeninin
   bir parametresi olur; o durumda ölçüm yeni modelde yapılır (`12` §3).
4. **Duvar yansıması:** bugünkü hızlarda duvara erişilmediği kayıtlıdır
   (`arsiv/07` §17.0 A4; üretici komut kayıtta yok). İstasyon tutmada duvar
   gerekmez.

Karar öğrencinin; uygulama bir `sim2/dunya` değişikliğidir ve yapı onayı
ister.

---

## 04 · Kanal ve fizik 🟢

| bileşen | karar | durum |
|---|---|---|
| yol kaybı | log-mesafe, **α = 2,0** (hava-hava serbest uzay) | 🟢 |
| gölgeleme | log-normal, korelasyonlu; σ = 3 dB PER geçiş bandıyla aynı mertebede (K-109); hücre boyu DUYARSIZ | 🟢 |
| sönümleme | Rician, FIR ile durumsuz, marjinal varyans tam 1; **K = 6 dB** | 🟢 · ⚪ K'nin kaynağı doğrulanacak (öğrenci; `02` §S1) |
| anten | yarım dalga dipol, kapalı form | 🟢 |
| girişim | toplamsal, parça başına SINR | 🟢 |
| PER | önbelge (DBPSK) + gövde (DQPSK) ayrı | 🟢 |
| MAC | 802.11b DCF temel erişim; Bianchi ile ±%15 | 🟢 · ⚪ sabitlerin kaynağı (`02` §S2) |
| bağlantı bütçesi | gürültü tabanı ve menzil çapası **birim seçimidir**; kenar kümesi değişmiyor (K-110 EK-4) | 🟢 |

- "Menzil" bir bağlantı yarıçapı değil, **verici gücünün çapasıdır**; bağ
  kümesi kanaldan ölçülür. Komşuluk grafiği bir teşhistir.
- **Ablasyon bayrakları:** `golgeleme_acik` · `sonumleme_acik` ·
  `anten_deseni_acik` · `yakalama_etkisi_acik` · `saat_senkron`. Her biri bir
  fiziği ayrı ayrı kapatabilir. Li replikasyonu gölgeleme ve sönümleme kapalı
  koşar (`09` §03.1b).

---

## 05 · Tehdit modeli

### 05.1 · Yönlendirici bir savunmanın işe yarayabilmesinin şartı

> **Karıştırılan bölge alanın bir parçası olmalıdır.**

Alanın tamamı kapanırsa etrafından dolaşılacak yer yoktur, bütün protokoller
eşit çöker ve deney *"fark yok"* der — ama bu farkın değil, sorunun
yokluğudur.

### 05.2 · Bugünkü uygulama 🟢

- **Tek karıştırıcı**, alan merkezinde sabit; açılma anı 150 s (**parametre**
  olarak kalır, öğrenci 10 Eylül).
- Beş sınıf: sürekli · darbeli · reaktif · aldatıcı · taramalı.
- **Çalışma noktası −15,0 dBm · ρ = 0,258.** ρ engellenen bağ oranıdır. Nokta
  referans sınıfta (sürekli) seçildi; ölçüt: 30 tohumun hiçbirinde birden fazla
  çok üyeli bileşen yokken en büyük ρ.
  Üretici: `python kalibrasyon/karistirici_gucu.py tarama`.
- Sınıflar arası eşitleme karıştırıcının **harcadığı** şey (yayılan ortalama
  güç) üzerinden yapılır, **başardığı** şey (ρ) üzerinden değil — ρ bağımlı
  değişkendir (K-103). Taramalı sınıf tepe gücü eşit tutar; bu beyan edilmiş
  bir asimetridir.

| sınıf | açık oranı | ort. dBm | ρ | ayrılan tohum |
|---|---|---|---|---|
| sürekli | 1,000 | −15,0 | 0,258 | 0/30 |
| darbeli | 0,499 | −15,0 | 0,169 | 1/30 |
| reaktif | 0,000 | −∞ | 0,000 | 0/30 |
| aldatıcı | 0,978 | −15,1 | 0,258 | 0/30 |
| taramalı | 0,325 | −19,9 | 0,081 | 0/30 |

*(Üretici: `python kalibrasyon/karistirici_gucu.py`, K-103.)* Reaktif sınıfın
ρ'su trafiksiz ölçümde tanım gereği sıfırdır; şiddeti trafikle ölçülür.
Aldatıcı ↔ sürekli, kanal grafiğinde aynı olan eşleştirilmiş bir kontrasttır;
aralarındaki fark CSMA görünürlüğü ile en çok 0,008'lik bir PER artığıdır
(`python kalibrasyon/denetim_ornekleme.py c f`).

**Duyarlılık borcu:** darbe periyodu, görev çevrimi, taramalı konak süresi ve
konak sayısı DUYARLI; karıştırıcı konumu kararsız (K-107). Çoklu karıştırıcı
tasarımında bunlar eksen olarak ilan edilebilir.

### 05.3 · Çoklu ve hareketli karıştırıcı — saha davranışına paralel 🟡

**Öğrenci kararı (10 Eylül 2026):** birden fazla karıştırıcı olacak ve
hareketli olacak; model, bu karıştırıcıların sahada nasıl davrandığına paralel
kurulacak. Birincil konum kararı bu tasarımla birlikte verilecek.

**Tasarım önerisi 🔵** (saha davranışının kaynakları: `02` §S3). Model üç
eksenden oluşur:

| eksen | seçenekler | not |
|---|---|---|
| sinyal sınıfı | bugünkü beş sınıf | var |
| platform ve hareket | **sabit yer konuşlu** (sürü çerçevesinde yavaşça geçer) · **yer aracı** (yol hızında doğrusal geçiş ya da devriye) · **havadan** (kendi yörüngesiyle) | yörüngeler kurulumda önceden hesaplanır — mobilitedeki gibi; kollar arası eşleştirme korunur |
| yayın düzeni | sürekli · görev çevrimli · **yay–sus–taşın** (konum tespitinden kaçmak için yayını kesip yer değiştirme) | açılma anları parametredir |

**Senaryo = karıştırıcı kümesi** (K adet × platform × sınıf × yayın düzeni).
Aday senaryo aileleri ve saha karşılıkları:

| aile | kurgu | karşılığı |
|---|---|---|
| cephe hattı | alan kenarı boyunca K adet sabit yer karıştırıcısı | cephe gerisindeki EH sistemleri |
| derin sızma | alanı kesen yolda 1–2 hareketli yer aracı karıştırıcısı | araç üstü karıştırıcı |
| hedef koruma | geçidin (§06.2) yakınında konuşlu karıştırıcı | savunanın kritik varlığı koruması |
| hava eşlik | sürüyle kesişen yörüngede havadan karıştırıcı | havadan EH |

**Açık tasarım soruları ⚪**

- **Hareket yeterli mi?** Bugünkü koşu süresinde sürünün ölçekli transit
  hızıyla sabit bir karıştırıcının kat ettiği yol kutunun küçük bir parçasıdır
  (karıştırıcı modülünün başlığındaki hesap: ~225 m, kutunun %12,5'i).
  Hareketli karıştırıcının etkisi için ya kendi hızı (araç, hava) ya da daha
  uzun bir geçiş gerekir. Seçim ölçümle yapılır.
- **Güç eşitlemesi:** çoklu karıştırıcıda eşitleme **toplam harcanan ortalama
  güç** üzerinden yapılır. Çalışma noktası ölçütü (bağlantılılık kısıtı altında
  en büyük ρ) senaryo kümesi için yeniden koşulur.
- **Evre metrikleri:** "açılma anı" senaryonun ilk yayını olarak parametre
  kalır. Hareketli karıştırıcıda şok yavaş gelir; M1–M3'ün bu durumda ne
  ölçtüğü kendi kapılarıyla yeniden sınanır (`08`).

Uygulama: `sim2/kanal` (karıştırıcı kümesi, yörüngeler) ve
`sim2/yapilandirma` (senaryolar) — yapı onayı ister.

**11 Eylül 2026 — iki parçaya ayrıldı.**

- **Y5a · mekanizma** (onaylı yapının kodu): tanım, küme, önceden hesaplanan
  yörünge ve yayın çizelgesi, üye başına gölgeleme kimliği ve CSMA
  görünürlüğü. Varsayılan `tekli_merkez` bugünkü satırları birebir üretir.
  🟢 **Uygulandı (11 Eylül, `04` K-117):** regresyon 37/37 birebir · 524 test.
- **Y5b · ailelerin sayıları:** gerçekçilik kararıdır. 🟢 **Öğrenci 11 Eylül'de
  aşağıdaki öneriyi olduğu gibi kabul etti** (`04` K-119); uygulama sırada.

#### 05.3.1 · Aile parametreleri 🟢 — öğrenci kararı verildi (11 Eylül 2026)

**Önce bir hesap: gerçekçi hızlarla bir koşuda ne kadar yol alınır?** Ölçek
1:50; zaman ölçeklenmez (`Konfig.olcek`).

| platform | gerçek hız (varsayım) | ölçekli hız | 270 s'lik ölçüm penceresinde yol | kutunun (1 800 m) payı |
|---|---|---|---|---|
| yer aracı | 60 km/h | 0,33 m/s | ~90 m | %5 |
| hava | 200 km/h | 1,1 m/s | ~300 m | %17 |

*(hesap; hızlar kaynak değil, mertebe için)*

Gerçekçi hızlarda bir yer aracı bir koşu içinde neredeyse durur; hava
platformu anlamlı ama küçük bir yol alır. Hareketli karıştırıcının koşu
içindeki asıl etkisi bu yüzden iki yerden gelir: **yayın düzeni** (yay–sus–taşın;
açık ve sessiz dönemler protokol zaman sabitleriyle karşılaştırılabilir) ve
**hava platformunun geçişi**.

**Öneri — aileler**

| aile | K | platform ve yerleşim | yayın düzeni | koşu içi hareket |
|---|---|---|---|---|
| `tekli_merkez` (bugünkü, referans) | 1 | sabit yer, alan merkezi | sürekli | yok |
| `cephe_hatti` | 3 | sabit yer, geçidin karşı kenarı boyunca eşit aralıklı | sürekli | yok |
| `derin_sizma` | 1 | yer aracı; alanı geçide doğru kesen yolun ortasından başlar | yay–sus–taşın | yalnız susarken, gerçek hızla (~32 m; K-119 düzeltmesi) |
| `hedef_koruma` | 2 | sabit yer; görev bölgesinde, geçide uzak yarıda | **sürekli** (görev çevrimi 15 Eylül 2026'da KALDIRILDI, K-127) | yok |
| `hava_eslik` | 1 | hava; alanı kesen doğrusal geçiş, irtifa bandın ortası | sürekli | gerçek hızla (~300 m) |

Sinyal sınıfı her ailede senaryo adından gelir (bugünkü beş sınıf).

**Öneri — süreler protokol zaman sabitleri cinsinden** (tek bir "gerçek değer"
iddiası yok; Θ'daki yöntem):

| eksen | çekirdek | keşifsel | neden bu sabit |
|---|---|---|---|
| yay–sus–taşın açık süresi | 15 s (OLSR `TOP_HOLD_TIME`) | 3 s (AODV `ACTIVE_ROUTE_TIMEOUT`) · 45 s | açık dönem protokolün topoloji bilgisinin bayatlama süresinden kısa mı, uzun mu |
| sessiz süre | 15 s | 5 s (OLSR `TC_INTERVAL`) · 45 s | rota onarımına zaman kalıyor mu |
| ~~görev çevrimi (`hedef_koruma`)~~ | ~~%50, periyot 30 s~~ | ~~periyot 6 s~~ | 🔴 **EKSEN KALDIRILDI (15 Eylül 2026, K-127).** Sert kısıtı çiğniyordu: açık oranı %50 olunca eşit ORTALAMA güç payı 1/(2×0,5) = 1,0'a çıkıyor, açıkken toplam TEPE güç tabanın iki katı oluyor ve 30 tohumun 2'sinde ağ bölünüyordu (açık evre 15 s, AODV'nin 3 s'lik rota geçersizlemesinin çok üstünde). ⚠️ Buradaki *"görev düzeyi deseni, `surekli_darbeli` sınıfından ayrıdır"* gerekçesi ÇÜRÜTÜLMEDİ — sert kısıtın önceliği altında kaldı. `tehdit_cevrim_periyodu_s` de `Konfig`den silindi |
| taşınma mesafesi | gerçek hız × sessiz süre | — | serbest sayı yok |

**Güç:** her ailede toplam ortalama yayılan güç referans sınıfınkine eşit; üye
başına ortalama güç = referans / K. ρ her ailede bir sonuçtur. Referans güç yeni
küme ve yere toplamayla C2'de yeniden seçilir.

**Uzun koşu (keşifsel seçenek):** gerçek hızlı geçişi gözlemek için
`derin_sizma` ve `hava_eslik` ~2 000 s'lik koşuyla da ölçülebilir; maliyeti
~6 kat.

**Önerilmeyen:** hareketi görünür kılmak için hızı gerçekçi olmayan değerlere
çıkarmak. Stres ekseni olarak bile gerçekçilik iddiasını bozar.

**Düzeltme önerisi:** yukarıdaki eski tablo `hedef_koruma`yı "geçidin yakınında"
tanımlıyordu. Sentezde hedef koruma, düşmanın **kendi** yüksek değerli
hedefinin çevresindeki reddetme alanıdır; sürünün geçidine yaklaşmak daha çok
`derin_sizma`dır. Öneri bu yüzden onu görev bölgesine yerleştiriyor.

**Öğrenci kararları (11 Eylül 2026, `04` K-119):**

1. aile tablosu ve K değerleri — 🟢 öneri olduğu gibi
2. süre eksenlerinin çekirdek noktaları — 🟢 öneri olduğu gibi, keşifsel
   noktalar dâhil
3. uzun koşunun keşifsel eksene girip girmeyeceği — 🟢 şimdilik hayır; beyan
   edilir
4. derin sızma aracının hareketi — 🟢 **yalnız susarken taşınır.** Tablodaki
   "~90 m" sürekli hareketle hesaplanmıştı; 15 s açık / 15 s sessiz düzeninde
   araç koşu sonuna kadar ~32 m ilerler
5. yerleşim türetme kuralları — 🟢 kabul: cephe hattı doğu kenarında
   y = 1/6 · 1/2 · 5/6 · hedef koruma x = 0,75, y = 1/4 · 3/4 · derin sızma
   alan merkezinden batıya (geçide) · hava eşlik kuzeye uçar ve karıştırılmış
   evrenin ortasında (açılma anı ile ölçüm sonunun ortası) alan merkezinden
   geçer. Geçit merkezdeyse ve eşler arası desende de aynı yerler

**Güç eşitlemesinin sayıya çevrilmesi.** "Toplam ortalama yayılan güç eşit"
kuralı, görev çevrimli ya da yay–sus–taşın düzenindeki üyede tepe gücünü açık
oranına böler: üye güç payı = 1 / (K × açık oranı). `tekli_merkez` ve
`cephe_hatti` sürekli yayında 1/K · `derin_sizma` 1 / 0,5 = 2 ·
`hedef_koruma` **1 / (2 × 1) = 0,5** (görev çevrimi kaldırıldı, K-127;
eski çevrimli hâlde 1 / (2 × 0,5) = 1 idi). Sınıf içindeki darbe
telafisinden (sürekli darbeli) ayrı ve onun üstüne uygulanır.

🔴 **ÖLÇÜLDÜ — eşit ORTALAMA güç, eşit TEPE güç DEĞİLDİR ve bu kısıt
kırabilir.** Açık oranı 1'in altındaki bir üyenin payı 1'i aşar; açıkken
yaydığı tepe güç tabanı aşar. `hedef_koruma`da iki üye bunu birlikte
yapıyordu (toplam tepe = 2 × taban) ve 30 tohumun 2'sinde ağı bölüyordu.
`derin_sizma` da 2,0 payla yayar ama BÖLMEZ (açık evreye kilitlenmiş
ölçümde 0/30, ρ 0,382): bölünmeyi üreten şey tepe gücü ile iki noktalı
duvarın BİRLEŞİMİDİR. Bu yüzden kapı aileye özeldir, genel değil.

**Uygulama (14 Eylül 2026, `04` K-120).** Aileler `kanal/tehdit.py`de; eksen
`tehdit_senaryosu` (TEDAVİ, varsayılan `tekli_merkez` ve bugünkü satırlar
birebir). Süre ve hız alanları `Konfig`e girdi; yeni `sessizde` yörünge türü
aracı yalnız sessiz dönemlerde taşıyor. Kâhin grafiğinin tazeleme süresi
karıştırıcı hızını da hesaba katıyor. Regresyona beş vaka eklendi.

### 05.4 · Protokol karıştırıcıyı görmez

Karıştırıcının konumu, gücü ve açık olup olmadığı protokole hiçbir koşulda
verilmez (`05` §4). Karıştırıcının akıllı hedef takibi (reaktif sınıfın
dışında) ⚪ saha kaynaklarına göre değerlendirilir.

---

## 06 · Trafik

### 06.1 · Bugün 🟢

10 akış × 4 pkt/s × 512 B, rastgele eşler arası çiftler, CBR + titreşim; her
düğüm en çok bir akışta. Yük eski çalışma noktasında tek çarpışma alanının
%36,9'u olarak ölçülmüştü; bugünkü noktada bayat (köken defterinde
`SINANMAMIS`).

### 06.2 · Yere toplama — birincil desen 🟢 uygulandı (Y4, `04` K-116)

**Öğrenci kararı:** yere toplama deseni kabul edildi (8 Eylül'de birincil
desen seçilmişti) ve en iyi tasarımın düşünülmesi istendi (10 Eylül).

**Neden değerli:** yollar uzar ve geçide yakınsar (derinlik); geçit çevresi
doğal bir darboğaz olur; karıştırıcı için anlamlı bir hedef doğar.

**Tasarım önerisi 🔵**

| soru | seçenekler | öneri ve gerekçe |
|---|---|---|
| geçit ne | yerde sabit istasyon · sürünün kenarında konum tutan röle İHA | **röle İHA.** Hava-hava kanalı doğrulanmıştır; yer–hava bağı (iki-ışın, farklı α) yeni ve doğrulanmamış bir fizik getirir. Röle İHA'nın yere uzun menzilli bağı kapsam dışı (ideal) sayılır ve beyan edilir |
| kaç geçit | 1 · 2 | **çekirdekte 1.** RFC'ye sadık protokoller belirli bir hedef adrese yönlendirir; "herhangi bir geçide" yönlendirme yeni bir protokol yeteneği ister ve rakiplere haksızlık olur. 2 geçit, sabit atamayla keşifsel eksende |
| geçit nerede | merkez · kenar | **kenar.** Derinliği artırır; yer istasyonları cephe gerisinde durur. Derinlik ölçülerek doğrulanır |
| kim gönderir | tüm düğümler · bir alt küme | **tüm düğümler düşük hızlı telemetri gönderir.** ⚪ Birkaç yüksek hızlı sensör akışı keşifsel eksende |
| ters yön | yok · düşük hızlı komut akışı | **düşük hızlı komut akışı** (geçit → düğümler): çift yönlü yolları ve AODV'nin ters rota davranışını sınar; yükteki payı küçüktür |
| toplam yük | — | **ölçütle seçilir:** karıştırıcısız kolda kâhin yönlendirmenin PDR tavanını ve geçit çevresindeki kanal doluluğunu bozmayan en büyük yük — projenin öteki ölçütleriyle aynı biçim |
| eşler arası desen | — | keşifsel eksende kalır |

**Bedeli:** "her düğüm en çok bir akışta" değişmezi geçit için gevşer. Tek
geçitte darboğaz protokolden bağımsız bir sınır koyabilir; yük kalibrasyonu bu
yüzden şarttır. Kaynak soruları: `02` §S4. Uygulama: `sim2/ag` ve
`sim2/yapilandirma` — yapı onayı ister.

CBR bir basitleştirmedir; gerçek telemetri patlamalı olabilir ve bu beyan
edilir.

---

## 07 · Protokol yüzeyi

- **Görebilecekleri:** `05` — değişmez.
- **Yapabilecekleri:** `13` — kontrol düzlemi 🟢. Aşama 1'de beacon'ın protokol
  başına kapatılması (R2), iletim sonucu kancası (R3) ve protokol rastgelelik
  alt akışı (R4) 🔵 (`13` §06.1).
- **Beacon:** koşum düzeyinde, 1 s (AODV `HELLO_INTERVAL`). OLSR'ın 2 s'si ile
  ayrışıyor; R2 önerisiyle her protokol kendi HELLO'sunu yönetir.

### 07.1 · Kâhinler — ölçüm aleti ve referans, protokol değil

| kâhin | ne yapar | durum |
|---|---|---|
| en güvenilir (ETX) | beklenen iletim sayısını küçültür | 🟢 — **kesin tavan değil:** atlama kâhini, bağ eşiği 0,99'da 15 tohumun 6'sında, bugünkü eşikte 2'sinde onu geçiyor; kol ortalamasında önde (`python -u kalibrasyon/bag_kumesi.py d`) |
| en kısa yol | en az atlama | 🟢 — ölçütün bedelini ölçmek için |

```
ETX kâhini − atlama kâhini = ölçütün bedeli
kâhin − protokol          = protokolün körlüğünün bedeli
```

### 07.2 · Üst referans — 🟢 onaylandı (10 Eylül, ikinci tur)

**Öğrenci:** bu iddia önemli; istatistik sunulurken bir üst referans vermek
değerli olur.

- **Sorun:** ETX beklenen iletim sayısını küçültür, teslim olasılığını değil.
  Yeniden deneme sınırı sonlu olduğu için toplam ETX'i düşük bir yol, beş
  denemede de geçemeyen bir bağ taşıyabilir (K-110).
- **Öneri — teslim olasılığı kâhini:** her bağın deneme sınırı içinde geçme
  olasılığı `s = 1 − (1 − p)^(sınır + 1)`, yol ölçütü `Σ −ln s`; yani uçtan uca
  teslim olasılığı en büyük yol. Bağ başarı olasılığı kâhin grafiğinde zaten
  var (K-110'daki geri türetme).
- **Raporlama:** 40 tohumda üç kâhin karşılaştırılır. Üst referans olarak tohum
  başına üç kâhinin en iyisi (**kâhin zarfı**) ve onu geçen kol sayısı
  raporlanır.
- **Dürüst adı:** "üst referans (kâhin)" — kesin bir sınır değil. MAC
  çekişmesi, kuyruk ve girişim dinamiği kâhin grafiğinde yoktur; bir protokolün
  referansı geçmesi bir kusur işareti değildir.
- **Ölçülen bedel** (tek tohum teşhis, `04` K-114 §4.3): teslim olasılığı kâhini
  iyi bağlı uzun yolları seçiyor. Paket başına ~2,4 kat atlama, PDR +0,057,
  ortalama gecikme ~3 kat. Zarf **PDR için** üst referanstır, gecikme için
  değil; raporda zarfın gecikmesi yanında yazılır.

Uygulama `kalibrasyon/ust_referans.py` (ölçüm aleti; karar ölçütü ölçümden önce
aletin başına yazıldı). Sonuç: `04` K-114 §4.3.

---

## 08 · Metrikler

### 08.1 · Var olanlar 🟢

- PDR (doğum kohortuna göre) · gecikme ve yüzdelikleri · `nrl_cerceve`,
  `nrl_bayt`, `nrl_airtime` · COR · rota kurtarma gecikmesi Δ.
- Üç kopma sayacı ve **algılama duyarlılığı**. Fiziksel kopma sayımı topoloji
  çalkantısını ölçer, karıştırmayı değil (K-110 EK-2).
- Evre metrikleri M1–M4 ve dört doğrulama kapısı (`08`).

### 08.2 · PSR — öğrencinin tanımı 🟢 ağ geneli oran uygulandı (Y1, K-115)

**Tanım (öğrenci, 10 Eylül 2026):** PSR ağ genelindeki uçtan uca durumu değil,
**bağ düzeyinde** — tek atlamada, iki komşu İHA arasında — veri iletiminin
başarısını ifade eder. Gönderilen bir paketin havada bozulmadan, gürültüye
kurban gitmeden ve bit hata sınırlarını aşmadan karşı taraftaki alıcı
tarafından CRC testinden geçerek alınma oranıdır.

Simülatördeki karşılığı:

```
          hedef alıcının gövdesini hatasız çözdüğü veri iletimleri
PSR  =  ───────────────────────────────────────────────────────────
          veri iletimi denemeleri (yeniden denemeler dâhil)
```

- "CRC'den geçti" = alıcı zincirinde önbelge kilidi kuruldu ve gövde PER
  çekimi başarılı.
- Yalnız veri çerçeveleri; kontrol çerçevelerinin PSR'si ayrı raporlanır 🔵
  (henüz yok).
- Ağ geneli oran 🟢 (`psr`, pencere ikiziyle); bağ başına dağılım 🔵 henüz yok.

**Onaya dayalı eski orandan farkı.** 11 Eylül 2026'ya kadar `psr` adını taşıyan
oran **gönderen tarafındadır ve onaya dayanır** (onay geldi / deneme). Artık
`mac_basari_orani` adıyla korunuyor. İki durumda ayrışırlar:

1. Veri ulaştı, onay kayboldu: onaya dayalı oranda başarısız, PSR'de başarılı.
   İkisinin farkı onay kaybının kendisidir.
2. Seyirci onay kusuru (`13` R1): onaya dayalı oranı doğrudan şişiriyordu. PSR
   onaya bakmaz; yalnız deneme sayısı üzerinden dolaylı etkilenir. Kusurun
   düzeltmesi §18 Y2.

### 08.3 · Kontrol istatistikleri 🟢 uygulandı (Y1, K-115)

Kontrol defterinin toplamları sayaç kütüğüne ve pencere ikizlerine; mesaj
biçimi başına döküm teşhise. Öneri ve gerekçe: `13` §06.1 R8.

---

## 09 · Senaryo matrisi ve istatistik

### 09.1 · Çekirdek + keşifsel

Çok hücreli bir matris üzerinden çoklu karşılaştırma düzeltmesi istatistiksel
gücü eritir. Bu yüzden **ön-kayıt yalnız çekirdeği** mühürler; geri kalan
hücreler keşifseldir, doğrulayıcı iddia taşımaz ama **tam olarak**
raporlanır.

### 09.2 · Çekirdek taslağı

```
1 mobilite kolu (§03.4 kararına göre)
× karıştırma koşulları (yok + §05.3 senaryo ailelerinden seçilecek birkaç)
× 4 protokol (AODV · OLSR · AOMDV · özgün)
× yere toplama trafiği (§06.2)
× 40 tohum
```

Kesin hücreler Aşama 1 sonunda belirlenir ve mühürde yazılır (`06` §9).
**Keşifsel eksenler:** yüksek çalkantı (Θ etiketli) · görev kolu · eşler arası
trafik · kalan karıştırıcı sınıfları ve senaryoları · ρ taraması · derinlik ·
2 geçit.

### 09.3 · Güç analizi ve tohum sayısı

**Öğrenci kararı (10 Eylül 2026): ana deney 40 tohum.** Çözünürlük (kolun
2 SE'si; deneyin görebileceği en küçük fark) ölçüldü:

| çıktı | 30 tohum: SD / R | 40 tohum: SD / R |
|---|---|---|
| ETX kâhini PDR | 0,0693 / 0,0253 | 0,0767 / 0,0243 |
| atlama kâhini PDR | 0,0988 / **0,0361** | 0,1005 / **0,0318** |
| ölçütün bedeli (eşleştirilmiş) | 0,0706 / 0,0258 | 0,0729 / 0,0231 |

*Üreticiler: `python -u kalibrasyon/cozunurluk.py` (30 tohum, K-107) ·
`python -u kalibrasyon/cozunurluk.py --tohum 40` (10 Eylül). Kol:
`statik-surekli`, tohumlar 1000'den başlayarak.*

- **Okuma:** 40 tohumlu bir hücre ~3,2 PDR puanından büyük farkları görebiliyor
  (30'da ~3,6). Eşleştirilmiş karşılaştırmalar daha keskin (~2,3 puan); sonuçlar
  mümkün olduğunca eşleştirilmiş kontrastlarla okunur.
- Bunlar kâhin kollarından bir **ön tahmindir**. Asıl güç analizi (hangi etkiyi
  %80 güçle görebiliyoruz) Aşama 4'ün başında taban protokollerin gürültüsüyle
  yapılır. 40 tohum yetmiyorsa mühürden önce artırılır.

### 09.4 · Derinlik bir eksendir; düğüm sayısı

Sonuç bir derinliğin artefaktı olabilir: 2 atlamada kazanan bir protokol 5
atlamada kaybedebilir. Derinlik keşifsel eksende tek bir soruyla incelenir:
**protokol sıralaması derinliğe göre değişiyor mu?**

**Düğüm sayısı 🟡 — öğrenci:** 30–50 aralığında düşünülecek; en uygun ve
gerekli değeri ajan ölçerek bulacak. Önerilen ölçüt:

1. Bağlantılılık kısıtı: 40 tohumda kopukluk %0.
2. Geçide yeterli derinlik ve alternatif yol sayısı (yönlendirmenin seçeneği
   olması).
3. Maliyet: sabit bir çözünürlüğe ulaşmak için gereken toplam hesap süresi
   (tohum SD'si² × koşu süresi).

Derinlik yere toplama desenine bağlı olduğu için ölçüm o desen uygulandıktan
sonra yapılır (`12` §3). Mevcut ölçüm (eşler arası trafik, eşitlenmiş
derecede): N = 20 / 40 / 80 için ortalama atlama 1,64 / 2,22 / 3,12 ve koşu
süresi 60,8 / 126,9 / 297,2 s (`python -u kalibrasyon/bag_kumesi.py i j`,
K-110 EK-4).

### 09.5 · Karıştırıcısız kol

Kâhinle karıştırıcısız PDR, statik kolda 1,000 · 0,999 · 0,996, hareketli
kolda 0,917 · 0,831 (`python -u kalibrasyon/pdr_tavani.py 1`). Statik kolda
karıştırıcısız kol bir kontroldür; hareketli kolda protokollerin ayrışabileceği
17 puanlık bir alan vardır.

### 09.6 · "Simülatör protokolü kısıtlamaz" — ön koşullu kapı

Kuyruk ve TTL yalnız aktarmada bağlar. Bu yüzden kapı üç durumludur:
**aktarma yoksa KOŞULMADI** · aktarma var ve marj geniş → geçti · aktarma var ve
marj dar → kısıtlıyor. Sayım değil **marj** raporlanır (`python -u
kalibrasyon/bag_kumesi.py k`).

- **TTL:** yapısal bir alt sınırı var (en uzak çift 5 atlama, TTL 32), ama
  değeri sonucu oynatıyor (K-110 EK-6).
- **Kuyruk kapasitesi:** verdikt Aşama 2'de, gerçek taban protokollerle
  verilecek.

---

## 10 · Doğrulama planı

| seviye | ne | durum |
|---|---|---|
| 1 · değişmez | korunum · mutabakat · test takımı | 🟢 `503 passed` (`python -m pytest tests2 -q`, 10 Eylül) |
| 2 · analitik | Bianchi · sönümleme varyansı · yol kaybı | 🟢 |
| 3 · literatür replikasyonu | Li vd. zincir kapasitesi | 🟢 mekanizma doğrulandı · H1 = 0,0861 tutmadı (band [0,10; 0,20]) · 10 Eylül'de yeniden ölçüldü, birebir aynı (`python -u kalibrasyon/li_replikasyonu.py`, `09`) |
| 4 · gerçekçilik kapısı | karıştırıcısız + kâhin → PDR ≈ 1 | 🟢 statik kolda; hareketli kolda 0,83–0,92 (§09.5) |
| 5 · ölçek tutarlılığı | tam ölçek verici var olabilir mi | 🟢 |
| 6 · duyarlılık | sonucu belirleyen sayılar gerekçeli mi | 🟢 koşuldu (K-107); kalan borç §11 |
| 7 · üreticiler | köken defterinin andığı komutlar koşuyor mu | 🟢 duman kapısı (K-111) |
| 8 · kontrol düzlemi | P1–P8 | 🟢 (K-112) |

Aşama 1 değişikliklerinden (yere toplama, çoklu karıştırıcı, mobilite)
sonra 1, 4 ve 6 yeniden koşulur. Seviye 3, kanala ve MAC'e dokunulmadıkça
değişmez.

---

## 11 · Parametre disiplini

### 11.1 · Yedi kova — esas (öğrenci, 10 Eylül 2026)

| kova | anlamı |
|---|---|
| TÜRETİLMİŞ | başka parametrelerden hesaplanıyor, serbest değil |
| ÖLÇÜLMÜŞ | bir kalibrasyon betiği üretti; üretici komut yazılı |
| KAYNAK | doğrulanmış dış kaynak; `02`de var |
| DUYARSIZ | oynatıldı, sonuç değişmedi — ölçümle hak edilir |
| TEDAVİ | deneyin ekseni; iki kolun meşru olarak ayrıldığı alan |
| KOL TANIMI | bir kolun ne olduğunu tanımlayan sabit; duyarlılık borcu taşır |
| SINANMAMIŞ | gerekçesi yok ya da yetersiz — görünür bir borç |

`Konfig`in her alanı bir kovada olmak zorundadır; kayıtsız alan içe aktarmada
patlar. Modül ve kalibrasyon sabitlerini mimari denetimi tarar (D12, D13).
Ön-kayıt kesinleşmeden önce hedef: **SINANMAMIŞ = 0** ve **duyarlılık borcu =
0** — ya da borçlu sabitler eksen olarak ilan edilir.

### 11.2 · Bugünkü dağılım (10 Eylül 2026)

**131 parametre:** TÜRETİLMİŞ 43 · ÖLÇÜLMÜŞ 12 · KAYNAK 6 · DUYARSIZ 18 ·
TEDAVİ 11 · KOL TANIMI 6 · SINANMAMIŞ 35 · duyarlılık borcu 5. *(İkinci tur:
onay semantiği ölçümünün karar eşiği ÖLÇÜLMÜŞ kovasına eklendi.)*
Üretici: `python kalibrasyon/mimari_denetimi.py`. *(TEDAVİ 11 = Konfig'in 4
tedavi alanı + kalibrasyon betiklerinin 7 tarama ekseni.)*

**SINANMAMIŞ öbekleri:**

- 802.11b sabitleri (`02` §S2)
- yük üçlüsü (ölçüm bayat; yere toplamayla yeniden seçilecek)
- saat çifti
- kontrol düzleminin iki sabiti
- Rician K (`02` §S1)
- evre metriklerinin iki anlamlılık sabiti (`08` §05.3)
- protokol olmadan kapanmayan dört parametre: kuyruk kapasitesi, TTL, beacon
  aralığı, komşu ömrü

**Kâhin tazeleme süresinin üst sınırı (10 s):** öğrenci kabul etti (10
Eylül). Tek tohumda 10 s ↔ 1 s farkı 0,003 PDR ölçülmüştü (K-104; üretici komut
kayıtta yok). Kova kaydının bu kararla güncellenmesi bir sonraki kod
değişikliğiyle birlikte yapılır.

### 11.3 · Duyarlılık denetimi 🟢

49 aday · 5 tohum · ×2 ve ×0,5 · iki kâhin · altı kol (K-107). Üretici:
`python -u kalibrasyon/duyarlilik.py <kol> [parametre…]`.

- **Baskın grup** bağlantı bütçesiydi. Menzil çapası ve gürültü tabanının
  aslında birim seçimi olduğu sonradan gösterildi (K-110 EK-4).
- **Beyan edilen sınırlar:** tek tek oynatma (OAT) · yalnız çalışma noktası
  çıktıları · kâhin kolları — kuyruk, TTL ve yakalama ancak kötü yönlendirmede
  bağlar (K-110 EK-6).
- **Isınma ve ölçüm penceresi** OAT ile taranamaz. Öğrenci kararı: ikisi
  birlikte taranacak, karıştırıcı açılma anı parametre kalacak (`12` §3).

---

## 12 · Kapsam dışı — beyan edilir

| modellenmeyen | sonucu |
|---|---|
| hız uyarlaması | kötü bağda 1 Mb/s'ye düşme yok; gerçek bir savunma eksik |
| yayılma kazancı | 11 çipli Barker'ın ~10 dB'i yok → karıştırıcı gerçekte olduğundan ~10 dB etkili görünür |
| enerji sezmeli CCA | güçlü gürültü karıştırıcısı ertelemeye yol açmıyor; yalnız aldatıcı sınıf CSMA'yı tetikler |
| çoklu kanal / frekans çevikliği | projenin öncülü — çözüm yönlendirme katmanında aranıyor |
| RTS/CTS | temel erişim; Bianchi doğrulaması da temel erişim için |
| yayılım gecikmesi | slotun küçük bir kesri |
| arazi / engel | 3B var, engel yok |
| patlamalı trafik | CBR |
| geçidin yere uzun menzilli bağı | 🔵 yere toplama önerisinde ideal kabul edilir (§06.2) |
| karıştırıcının akıllı hedef takibi | ⚪ saha kaynaklarına göre (§05.4) |

Önceki listede yer alan "havadan karıştırıcı yok" satırı kaldırıldı: çoklu
karıştırıcı önerisinde havadan platform var (§05.3). Kodun kendi kapsam listesi
buna göre güncellenecek (§17 A23).

---

## 13 · Gösterim

**Öğrenci:** sunumda simülasyonun işleyişi görselleştirilecek (Aşama 5).

- **İz kanalı ayrıdır ve ölçüme dokunamaz.** Kapısı: iz açıkken ve kapalıyken
  sonuç satırı birebir aynı olmalı.
- **Gösterilecekler:** düğümler ve bağlar · karıştırıcıların etki alanı ve
  hareketi · geçide giden rotalar · rota kopması ve kurtarma anları · evre
  çizgisiyle (temiz–şok–toparlanma) PDR eğrisi · ölçek eşlemesi (*"1 m = 50 m
  · kutu ~90 km"*, konfigürasyondan okunur).
- **Durum:** ⚪ henüz yazılmadı. 🔵 İz kanalının Aşama 1–2'de eklenmesi,
  sonradan eklenmesinden ucuzdur.

---

## 14 · Uygulama durumu

| paket | bugün | Aşama 1'de |
|---|---|---|
| `cekirdek` | 🟢 | değişmez |
| `yapilandirma` | 🟢 yedi kova | senaryolar: yere toplama, karıştırıcı kümesi, mobilite kolu |
| `dunya` | 🟢 Gauss-Markov 3B · görev · sabit | 🔵 istasyon tutma (§03.4) |
| `kanal` | 🟢 tek karıştırıcı, beş sınıf | 🟡 çoklu hareketli karıştırıcı (§05.3) |
| `mac` | 🟢 · veri onayı yalnız göndericinin kendisi çözdüğünde işlenir (Y2) | — |
| `ag` | 🟢 eşler arası CBR · yere toplama (Y4) | çekirdekte hangi desenin varsayılan olacağı C1/C3'ten sonra |
| `gozlem` | 🟢 pencere + kontrol niyetleri | 🔵 iletim sonucu kancası (R3) |
| `olcum` | 🟢 evre metrikleri · kopma · PSR alıcı tarafında (Y1) | 🔵 anlamlılık sabitleri (`08` §05.3) · bağ başına PSR |
| `kosum` | 🟢 kontrol düzlemi · kontrol istatistikleri sayaç kütüğünde (R8, Y1) | 🔵 beacon'ın protokol başına kapatılması (R2) · rastgelelik alt akışı (R4) |
| `kalibrasyon` | 🟢 | onay etkisi ölçümü · teslim olasılığı kâhini · düğüm sayısı · görev yarıçapı · pencere taraması |
| `protokoller` | koşum aletleri | Aşama 2 |
| `analiz` | yok | Aşama 4 — istatistik katmanı |

---

## 15 · Öğrenci kararları — tek yerde

### 8 Eylül 2026

1. Kapsam cümlesi (`01` §3).
2. Trafik: yere toplama birincil, eşler arası keşifsel.
3. Mobilite yapısı ile çalkantı ayrı eksenler; çekirdekte düzgün istasyon.
   *(Hedeflenen Θ ≈ 10 ulaşılamaz bulundu; Θ bir kapıya çevrildi, K-101 ve
   K-110.)*
4. Li vd. replikasyonu yapılacak.

### 9 Eylül 2026

- Beacon yükü çerçeveyi uzatır (K-111).
- O gün için simülatör fazında kalınması (K-111).

### 10 Eylül 2026 (K-112, K-113)

- Kontrol düzleminin beş kararı (`13` §01).
- Keşifsel yüksek çalkantı kolu saklanmaz; sorun varsa düzeltilir (§03.3).
- Ana deney 40 tohum (§09.3).
- Mobilite: ajan daha mantıklı tercihini belirtecek (§03.4).
- Görev kolu yarıçapı daha büyük örneklemle yeniden ölçülecek.
- Düğüm sayısı 30–50 aralığında; en uygun değeri ajan ölçerek bulacak (§09.4).
- Veri onayı kusuru: önce etkisi ayrı ölçülecek, sonra karar verilecek.
- Yere toplama kabul; en iyi tasarım düşünülecek (§06.2).
- Karıştırıcılar çoklu ve hareketli, saha davranışına paralel (§05.3).
- Sabit mühür tarihi yok; simülasyon işleri 26 Eylül'e kadar bitirilmeye
  çalışılacak.
- İş akışı beş aşama (`01` §5).
- Birincil karıştırıcı konumu çoklu karıştırıcı tasarımıyla belirlenecek.
  Özgün protokol tasarımını öğrenci, simülasyon oturduğunda gösterecek.
- PSR tanımı (§08.2).
- Tespit gecikmesinin boş kol kapısı protokol yazım aşamasına bırakıldı.
- Rician K'nin kaynağı doğrulanacak.
- İki anlamlılık sabiti: ajan ölçerek seçecek (`08` §05.3).
- Isınma ve ölçüm penceresi birlikte taranacak; açılma anı parametre kalacak.
- Kâhin tazeleme süresinin üst sınırı kabul edildi.
- Tavan kâhini kontrol edilip mantıklı olan yapılacak; üst referans isteniyor
  (§07.2).
- Kontrol istatistikleri: projenin faydasına göre ajan önerecek (`13` §06.1).
- Yedi kova esas.
- Li H1 yeniden ölçülecek — yapıldı (§10).
- Belgeler bilgi kaynağına çevrilecek; aşırı katı kurallar gevşetilecek.

### 10 Eylül 2026 — ikinci tur (K-114)

- Mobilite önerisi onaylandı: çekirdekte formasyon + istasyon tutma (§03.4,
  §18 Y6).
- Yere toplama önerileri kabul edildi — *"projede dürüstlük ve gerçekçiliğe
  sıkıntı çıkarmayacaksa"*; değerlendirme §18 Y4.
- Çoklu hareketli karıştırıcı modeli onaylandı; saha davranışı sentezi
  öğrenciden geldi (`02` §S3, §18 Y5).
- Üst referans (teslim olasılığı kâhini + kâhin zarfı) onaylandı (§07.2,
  §18 Y9).
- Kontrol istatistikleri önerisi onaylandı (`13` R8, §18 Y1).
- Mühür sırasının gevşetilmesi onaylandı (`06` §0.3).

### 11 Eylül 2026 — üçüncü tur (K-114)

- Veri onayı kusuru düzeltilecek: onay yalnız göndericinin kendisi çözdüyse
  sayılır (`04` K-114 §4.2, §18 Y2).
- Üst referansın tohumlu ölçümü yeni çekirdek hücrede, çözünürlük ölçümüyle
  (C7) birlikte koşulacak (`04` K-114 §4.3).
- §18'in yapısı onaylandı: Y1, Y3, Y4, Y5, Y6, Y7, Y10.

### 11 Eylül 2026 — dördüncü tur (K-119)

- Karıştırıcı senaryo aileleri ve üye sayıları öneri olduğu gibi:
  `tekli_merkez` · `cephe_hatti` (3) · `derin_sizma` (1) · `hedef_koruma` (2)
  · `hava_eslik` (1); toplam ortalama yayılan güç her ailede EŞİT (`05` §3.1).
- Süre eksenlerinin çekirdek noktaları: açık 15 s · sessiz 15 s · hedef
  korumada %50 görev çevrimi, periyot 30 s.
- ~2 000 s'lik uzun koşu **şimdilik keşifsel eksene girmez**; çekirdek 350 s.
- Formasyon kolundaki duvar teması **nadir kabul edilir, sayılır ve beyan
  edilir**; istasyonlar değişmez.
- Derin sızma aracı **yalnız susarken taşınır** (yayın yaparken durur).
- Ailelerin alan içindeki yerleşim kuralları kabul edildi.

### 15 Eylül 2026 (K-124)

🔒 Üçü de **tarama koşulmadan ÖNCE** ilan edildi — bu listenin bir kuralı.

- C1 · düğüm sayısı: adaylar 30–50 · alan `1800 × √(N/40)` (yoğunluk sabit) ·
  **sert kısıt 1** statik kolda hiçbir tohumda ulaşılamaz çift yok · **sert
  kısıt 2** geçide düğüm-ayrık ikinci yolu olan kaynak oranı **≥ 0,90** ·
  amaç: iki kısıtı da geçenler arasında koşu maliyeti en küçük N.
- Maliyet **ölçülür**, varsayılmaz.
- C3 · yere toplama yükü: ölçüt, karıştırıcısız kolda KÂHİN yönlendirmeyle
  uçtan uca teslimin **≥ 0,95** tuttuğu en büyük telemetri hızı.

### 15 Eylül 2026 (K-129)

- Doğrulama listesinin tamamı koşulsun — *"şimdi koşsun, temiz girelim"*.

### 16 Eylül 2026 (K-130 · K-131 · K-133 · K-134)

- Bağımsız denetimin bulguları işlensin (`arsiv/DENETIM-2026-09-16.md`).
- **Tamponlama:** rota beklenirken paket ayrı bir **bekleme tamponuna** alınır;
  arayüz kuyruğunda kalmaz, arkasındaki paketler akar (A24).
- **Pencere ikizi** pencerede **dondurulur** (kontrol yükü metriği ~%9
  şişiyordu ve şişme protokol ailesine göre farklıydı).
- **Gözlem yüzeyi:** kancalara da gözlem verilir · `bildirdigi_konum`
  yüzeyden çıkar · bilgi yokluğunda `0` değil **`None`** döner —
  `None ≠ 0` kuralının projedeki tek istisnası kapanır (A25).
- **Θ yeniden ölçümü (C4) şimdi değil.**
- Ağ bölünmesi bulununca: *"gerekeni yap, beyan ederek hiçbir şey çözülmez"* —
  ölçüm kalibrasyon tarafına, kâhin grafiğiyle alındı (K-132).
- Duyarlılık aklamaları **20 tohumla** yeniden ölçülsün (ikisi çöktü).
- Doğrulama listesinin tamamı yeniden koşulsun — *"evet, tamamını koş"*.
- **Kancalar beyan döndürsün**; `rota_gecersiz` düşme sebebinin **yolu
  uygulansın** (K-134).

### 17 Eylül 2026 (K-136)

- **U1'in eşiği:** AODV'nin PDR'si, AYNI konfigürasyonda koşan ETX kâhininin
  PDR'sine oranlanır; **statik ≥ 0,90 · hareketli ≥ 0,60**.
  ⚠️ Eşik ölçüm görüldükten SONRA seçildi; gerekçe ve sınırı `06` §4.3'te
  ve `kalibrasyon/aodv_uygunluk.py` başlığında açık yazıyor.
- **AODV yerel onarımı (RFC 3561 §6.12) uygulanmaz, beyan edilir** — RFC'de
  opsiyonel, üç yeni ölçülmemiş parametre getirirdi. ⚠️ AODV'yi karıştırma
  altında zayıflatabilir ve sonuç raporlanırken bu sapma yanında anılır.

### 17 Eylül 2026 (K-137 · `03` §1)

- **U1 için A seçeneği:** eşik yerinde kalır; eşiğin altındaki hücre
  ölçülmüş açıklamasıyla **bulgu** olarak raporlanır. U1 ikiye ayrıldı —
  U1-U uygunluk (kapı) · U1-B başarım (bulgu), `06` §4.4 madde 3.
- **Çalışma ritmi** (`03` §1): *bir iş bitirilir, sonra ölçülür* — uzun
  kapılar yalnız kapanışta, bir kez · protokoller sırayla kapatılır · ağır
  koşumda havuz varsayılanı **4 işçi**.

### 18 Eylül 2026 (K-138)

- *"Sen en mantıklı bulduğun şeyi yap"* — hız araştırması (parça parça veri ·
  ekran kartı) ve devam etmeden önce düzeltilebilecek sorunlar **ajana
  devredildi**. Philox üreteci seçeneği ölçüldü ve alınmadı; karar yine
  öğrencinin.

### 19 Eylül 2026 (K-140 … K-145)

- **AODV kapatılsın** — *"aodvyi kapatalım, devam edelim"* (K-140). K-143
  kapanışı geçersiz kıldı; yeniden kapanış K-145.
- **COR düzeltmesi kapanıştan sonra** yapılsın (K-141).
- **OLSR: RFC 3626'nın SHOULD maddeleri uygulanır, MAY maddeleri beyan
  edilir** (K-142).
- **Sıra:** *"ilk önce aodv bitsin sonradan olsryi koşacağız"* — OLSR'ın
  kapanış ölçümü AODV kapandıktan sonra.
- **AODV'nin U3'ü bulgu olarak raporlanır** (K-144).
- **Birincil kaynaklar depoya girer** — `protokol_kaynaklari/`; bir belge
  ancak **tamamı okunup** gerçekliği ve istem enjeksiyonuna karşı
  denetlendikten sonra (öğrencinin şartı). AOMDV makalesi ve iki RFC
  alındı (`02` §R4).
- AOMDV'nin boşluklarını ns-2 ile çapraz kontrol önerisi kabul edildi →
  kontrol edilince ns-2 kodunun yazarlara ait OLMADIĞI çıktı; boşluk kararı
  açık (`02` §R4.1: a · b · c).

### 21 Eylül 2026

- **Ağır koşumlar 8 çekirdek kullanabilir** (4 yerine) — *"işlemcimin 8
  çekirdeğini kullanabilirsin"* (`03` §1).
- OLSR'ın kapanış ölçümü başlasın — *"devam edebiliriz"*.

### 22 Eylül 2026 (K-146 · K-147)

- **OLSR'da RFC 3626 §13 (bağ katmanı bildirimi) uygulanır** — *"MAY beyan
  edilir"* kuralına ölçülmüş gerekçeli **tek istisna**. Beyanlı sapmayken
  statik kolun iki hücresini eşiğin altına itiyordu (0,859 · 0,866; §13 ile
  0,926 · 0,908) ve OLSR'ı bağ katmanı bilgisinden yoksun tek taban
  bırakıyordu (K-146 §5).
- §13 hareketli kolların yedisinde OLSR'ı düşürdü (K-147 §3) — **karar
  kalır**, OLSR'ın §13'e duyarlılığı **bulgu** olarak raporlanır; mekanizma
  ölçülmeden hipotez olarak kalır.
- **AOMDV'nin boşlukları: makale + RFC 3561** (`02` §R4.1 seçenek a) —
  makalenin değiştirmediği her şey AODV'nin RFC'sinden; belirtilmemiş
  seçimler beyanla.
- **DESPARETE değerlendirmesinde güvenlik:** ana karşılaştırmada dört
  protokol de güvenliksiz; Güvenlik Profili 1'in bayt bedeli ayrı bir
  duyarlılık kolunda ölçülür (K-150).
- **DESPARETE'nin yedekli gönderimi** ilk gerçeklemede yok; kopyalama ve
  tekil teslim sayımı sonraya (K-150).
- **Ters yön (komut) trafiği: A · isteğe bağlı hedef alanı** — komut alacak
  düğüm kendi alanını üretir; edinim mekanizması her hedef için çalışır
  (K-150 §4).
- **`sim2/` yapısı Y1 ve Y2 onaylandı:** her unicast sonucunun tekrar
  sayısıyla bildirimi · protokolün veri başlığı baytı, yönlendirme ek yüküne
  sayılır (K-150 §4 · K-151).
- Hedef alanı simülasyonda emekliye ayrılmaz (K-150 §4).
- DESPARETE v0.1 yazıldığı gibi gerçeklenir; açık iki tasarım sorusu önce
  ölçülür, değişiklik v0.2'de (K-150 §4).
- CAUTION'a girişte seçili ardıla bir kez sınırlı doğrulama oturumu
  (tasarımın mevcut kuralı; yeni sabit yok) (K-150 §4).

### 23 Eylül 2026

- **Temizlik — bağlam kirliliğini önlemek için; SİLME YOK, arşive taşıma:**
  karar defterinin K-001…K-089'u ayrı arşiv dosyasına · eski denetim raporu,
  eski teknik referans, eski kaynak listesi ve 19 eski regresyon tabanı
  arşive · literatür taraması `protokol_kaynaklari/`na. Devir istemi
  güncellendi (`DEVIR-PROMPT.md`).

---

## 16 · Bu belgenin statüsü

Bilgi belgesidir. Kodla çelişirse hangi tarafın yanlış olduğu **ölçülerek**
bulunur ve §17'ye yazılır. Bir tasarım değişikliği önce burada tarif edilir,
sonra koda geçer; `sim2` değişiklikleri yapı onayı ister.

---

## 17 · Şartname–kod ayrışma defteri — açık satırlar

Kapanmış satırlar ve eski tablolar: `arsiv/07-SIMULATOR-TASARIMI-2026-09-10.md` §17.

| # | belge | kod | durum |
|---|---|---|---|
| A4 | istasyon tutma, duvarsız hareket (§03.4) | Gauss-Markov + duvar yansıması | 🔵 öğrenci kararı |
| A6 | menzil yalnız verici gücünün çapası; adı bunu söylemeli | ad hâlâ "iletim menzili" | ⚪ kozmetik ama ad yanlış bir iddia taşıyor |
| A8 | yere toplama birincil (§06.2) | 🟢 desen uygulandı (Y4, `04` K-116); varsayılan hâlâ `esler_arasi` | 🟡 çekirdekte varsayılan desenin seçimi C1/C3'ten sonra |
| A14 | OLSR HELLO 2 s | koşum düzeyinde tek 1 s beacon | 🟢 **kapandı** (K-142, 19 Eylül): OLSR de `kosum_beaconi = False` bildiriyor ve RFC 3626'nın `HELLO_INTERVAL` 2 s'ini kendi HELLO'suyla kullanıyor; AODV aynı yoldan RFC 3561'in 1 s'ini (17 Eylül). Koşum düzeyindeki 1 s'lik beacon iki taban protokolde de hiç yayılmıyor |
| A19 | kontrol düzlemi | 🟢 uygulandı | R1–R4, R8 kapandı; R5–R7 beyanlı (`13` §06) |
| A24 | protokol rota ararken paketi bekletebilmeli (RFC 3561 §6.3) | 🟢 uygulandı (K-131): `Karar.beklet` + düğüm başına tampon, iki tavan | 🟢 kapandı; tamponun iki parametresi `SINANMAMIS` ve Aşama 2'de kapanacak |
| A25 | gözlem penceresi yalnız veri gönderme kararında sunuluyordu | 🟢 uygulandı (K-131): yedi kanca gözlem alıyor | 🟢 kapandı; yüzey 24 → 23 alan (`05` §5) |
| A20 | çoklu hareketli karıştırıcı (§05.3) | tek karıştırıcı, merkezde sabit | 🟡 Aşama 1 |
| A21 | PSR alıcı tarafında (§08.2) | 🟢 uygulandı (Y1, `04` K-115) | 🟢 kapandı; bağ başına dağılım §08.2'de 🔵 açık |
| A22 | Θ protokol başına raporlanır (§03.3) | tek Θ | 🔵 |
| A23 | kapsam dışı listesi güncellendi (§12) | kodun kapsam listesi eski hâlde olabilir | ⚪ kontrol edilecek |
| A26 | sözleşme *"protokol niyet döndürür"* diyor (§13 §03) | niyet doğrulayıcı yalnız iki tipi tanıyordu; `Beyan` yalnız `Karar` içinden geçebiliyordu | 🟢 kapandı (K-134): kancalar da beyan döndürüyor, `Dugum.beyan_isle` tek kaynak. Öncesinde U2 ifade EDİLEMEZDİ — protokol kopmayı biliyor ama söyleyemiyordu |
| A27 | `rota_gecersiz` düşme sebebi şemada taahhüt edildi (K-131) | onu üreten kod yolu YOKTU; rota geçersizken de `hedef_yok` yazılıyordu | 🟢 kapandı (K-134): `gonderim.py` kararın beyanına bakıyor. Ayrım ölçüm için gerçek — *"hedefi hiç bilmiyorum"* ile *"biliyordum, bağ koptu"* aynı şey değil |

Ters taramada (kodda olup belgede adıyla geçmeyen) beş ablasyon bayrağı ve
görev kolunun üç parametresi artık bu belgede adıyla anılıyor (§03.2, §04).
Taramanın sınırı: ad arar, kavram aramaz.

---

## 18 · Aşama 1 yapı planı — 🟢 yapı onaylandı (11 Eylül 2026)

**Yapı onayı (öğrenci, 11 Eylül 2026 — üçüncü tur):**

- Y1, Y3, Y4, Y5, Y6, Y7, Y10
- veri onayı düzeltmesi (Y2)
- üst referansın tohumlu ölçümü: yeni çekirdek hücrede, C7 ile birlikte
- Y8'in (iz kanalı) yapısı ayrıca anlatılacak

**Onaylananlar (öğrenci, 10 Eylül 2026 — ikinci tur):**

- mobilite önerisi (§03.4)
- çoklu hareketli karıştırıcı (§05.3)
- üst referans (§07.2)
- kontrol istatistikleri (§08.3, `13` R8)
- mühür sırasının gevşetilmesi (`06` §0.3)
- yere toplama önerileri (§06.2) — *"projede dürüstlük ve gerçekçiliğe sıkıntı
  çıkarmayacaksa"* şartıyla; değerlendirme Y4'te.

Bu bölüm onaylanan tasarımların **kodda nasıl kurulacağını** anlatır. `sim2/`
değişiklikleri bu yapı onaylandıktan sonra yazılır. Ölçüm aletleri (Y0, Y9)
onay beklemez.

### 18.0 · Bütün adımlar için geçerli kurallar

| kural | nasıl |
|---|---|
| varsayılan = bugünkü davranış | Her yeni alanın varsayılanı bugünkü kolu birebir üretir. Her adımdan sonra regresyon matrisi (Y0) ve test takımı koşulur. Değişmesine izin verilen alanlar önceden yazılır: kimlik özetleri, yeni şema alanları, tanımı bilerek değişen metrik |
| yeni parametre | köken defterine kovasıyla; kol farkı yaratan alan TEDAVİ, kolun tanımı KOL TANIMI |
| yeni rastgelelik | önce hash alanı; kurulumda tüketilen sıralı akış yalnız gerekiyorsa. Kullanılmayan kolda akış yaratılmaz |
| yeni sayaç | sayaç kütüğünde; pencere ikizi otomatik |
| her mekanizmanın kapısı | boş geçmeyen bir test: mekanizma devredeyken kanıt sayısı > 0 |

### Y0 · Regresyon aleti — ölçüm aleti

- **Neden:** K-112'nin 35 satırlık "önce/sonra birebir" karşılaştırmasının
  betiği depoda kalmamıştı. Bu kez depoya yazılır.
- `kalibrasyon/regresyon_satirlari.py uret <etiket>`: aynı matrisi koşup
  satırları `ciktilar2/regresyon/<etiket>.jsonl`e yazar. Matris (35 vaka):
  - 3 statik kol × döngülü koşum aleti
  - 12 hareketli kol × doğrudan komşu
  - 6 karıştırıcı × doğrudan komşu
  - 3 kol × iki kâhin
  - yüklü beacon · kontrol sınavı
  - 4 tam uzunluk

  İlk matris (38 vaka) 32,4 dk sürdü ve süreye göre küçültüldü (`04` K-114
  §3, §4.4). Alet vaka başına süreyi basar.

  🟢 Geçerli taban: `y2b_2026-09-11` (Y1 + Y2 sonrası, `04` K-115). İlk taban
  `taban_2026-09-11b` idi; önceki üretimle ortak 23 vaka alan alan birebir
  aynıydı.
- `karsilastir <a> <b>`: alan alan farkı ve izin verilen farkların listesini
  basar.
- **İlk iş:** bugünkü koddan taban satırlarının üretilmesi.

### Y1 · PSR ve kontrol istatistikleri

| parça | yapı |
|---|---|
| sayaç kütüğü | Yeni sayaç `veri_alim_hedefte`: hedef alıcının gövdesini hatasız çözdüğü veri iletimi, tekrarlar dâhil. Veri teslim işleyicisinde, tekrar kontrolünden önce artar |
| PSR | `psr = veri_alim_hedefte / mac_deneme` (öğrenci tanımı). Bugünkü oran `mac_basari_orani` adıyla kalır |
| kontrol toplamları | Kontrol defterinin toplam alanları sayaç kütüğüne girer: yayın gönderilen · unicast onaylanan ve vazgeçilen · kontrol kuyruk taşması · yayın ve unicast teslim · tekrar bastırılan · başkasına adresli · dinamik ve periyodik ateş. Her biri düğüm defterinin arttığı **aynı** çağrı noktasında artar |
| mesaj biçimi dökümü | teşhiste `{biçim: {çerçeve, bayt, airtime}}`, tüm koşu ve ölçüm penceresi için |
| kapılar | PSR: onayı kaybolan bir iletimde yeni PSR başarı, eski oran başarısızlık sayar · kontrol: koşu sonunda her alanda Σ düğüm defteri = sayaç |
| beklenen etki | Sayaç şeması özeti değişir. `psr` değerleri değişir; tanım bilerek değişti. Diğer bütün metrikler birebir aynı kalır |

### Y2 · Veri onayı semantiği — 🟢 uygulandı (11 Eylül, `04` K-115)

Düzeltme seçilirse tek değişiklik şu olur: veri onayı işleyicisi onayı çözen
düğümü alır ve onayı yalnız gönderenin kendisi çözdüyse işler. Bu, kontrol
düzleminin kuralıyla aynıdır.

| parça | yapı |
|---|---|
| ölçüm | `04` K-114 §4.2: PDR'de çözünürlük üstünde etki yok. Kusur göndericiye fiziksel olarak alamayacağı bir başarı bilgisi veriyor ve karıştırıcı altında büyüyor. 🟢 **Öğrenci onayladı (11 Eylül): düzeltilecek** |
| kapı | Ölçüm aletinin `duzeltilmis` kipi başvuru uygulamasıdır. Değişiklikten sonra `sim2`nin varsayılan koşusu, aynı tohum ve kolda o kipin sonucuyla **birebir** aynı olmalıdır |
| beklenen etki | Unicast veri taşıyan her satır değişir, çünkü davranış ilk farklı onayda ayrışır. Regresyon karşılaştırması bu adımda birebirlik aramaz; yukarıdaki kapı onun yerini tutar. Adımdan sonra regresyon tabanı yeniden üretilir |

### Y3 · Kontrol düzlemi eksikleri — `13` R2 · R3 · R4 — 🟢 uygulandı (`04` K-121)

| # | yapı | neden bu biçim |
|---|---|---|
| R2 | Kontrol düzlemini kullanan protokol isteğe bağlı `kosum_beaconi = False` bildirebilir. O protokolün düğümlerinde koşum düzeyindeki beacon hiç çizelgelenmez; gözlemdeki komşu listesi boş kalır ve bu beyan edilir | protokol komşuluğunu kendi HELLO'sundan kurar; gözlem penceresi değişmez |
| R3 | Yeni kontrol kancası `iletim_basarisiz(dugum, hedef, tur, saat_s) → niyetler`. MAC bir unicast veri ya da kontrol çerçevesinden **vazgeçtiği anda** çağrılır. Kanca sayısı 4'ten 5'e çıkar; hepsi-ya-hiç kuralı sürer | Gönderenin kendi MAC'inin bildiği bir olaydır (`05` §3.1'deki "zaman aşımı"). Başarı için ayrı kanca yok: `son_iletim_sonucu` bunu zaten veriyor ve her onayda olay üretmek maliyetli · 🔄 **22 Eylül 2026 (K-151 · Y1):** başarıyı ve tekrar sayısını isteyen protokol için İSTEĞE BAĞLI `iletim_sonucu` eklendi — taşımayan protokol çağrılmaz |
| R4 | `KontrolIstegi` ve `Uyandirma` isteğe bağlı `jitter_s` taşır. Simülatör `U(0, jitter_s)` gecikmesini `protokol_kesif` akışının **düğüm alt akışından** çeker | Protokol rastgelelik nesnesi görmez; geri referans yasağı sürer. Jitter kullanmayan protokolde akış yaratılmaz, satırlar değişmez |

**Uygulama (14 Eylül 2026, `04` K-121) — yapıdan farklar**

- **Beacon'ı yalnız kontrol düzlemli protokol kapatabilir.** Yapı metni bunu
  söylemiyordu; kancasız ve beacon'sız bir protokol kalıcı olarak kör olurdu
  ve ölçülen şey kararı değil körlüğü olurdu. İhlal kurulumda durur.
- **Titreşimli istek kuyruğa girmeyi geciktirir** ve o ana kadar deftere
  `istenen` yazılmaz. Bekleyen isteğin sessizce kaybolmaması için
  uyandırmanınkiyle aynı biçimde kapalı bir denklem eklendi.
- **Üç yeni sayaç** (`basarisiz_bildirim`, `jitter_istenen`, `jitter_ates`)
  kontrol defterine girdi; `sayac_semasi_hash` bu yüzden değişti.

### Y4 · Yere toplama — yapı ve dürüstlük/gerçekçilik değerlendirmesi

**Yapı**

| parça | yapı |
|---|---|
| konfigürasyon | `trafik_deseni ∈ {esler_arasi, yere_toplama}` — **TEDAVİ**, varsayılan `esler_arasi` · `gecit_sayisi` (1) ve `gecit_konumu` (`kenar`) — KOL TANIMI · `telemetri_paket_hizi_hz` — C3 ile ÖLÇÜLMÜŞ · `komut_akis_sayisi`, `komut_paket_hizi_hz` |
| geçit | Düğüm 0 geçittir. Yerleşimde onun için çekilen konumun yerine alanın kenar ortasında sabit bir istasyon alır: sürü çerçevesinde konum tutan röle İHA. Öteki düğümlerin çekimleri **değişmez**; eşler arası kolla eşleştirme korunur |
| trafik | `yere_toplama`: geçit dışındaki her düğümden geçide bir telemetri akışı; geçitten `komut_akis_sayisi` düğüme komut akışı. Doğum çizelgesi aynı faz + titreşim yöntemiyle kurulur. İki geçit varsa her düğüm başlangıçta en yakın geçide sabit atanır |
| kapsam | satırın kapsam bölümüne "geçidin yere bağı ideal" yazılır; yönü: uçtan uca teslimi olduğundan iyi gösterir, bütün kollarda ortaktır |
| teşhis | **Kayıp yeri:** düşen paketlerin, düştükleri düğümün geçide mesafesine göre dağılımı (0–R · R–2R · >2R). Darboğaz kaybını yönlendirme kaybından ayırmak için |
| kapılar | `esler_arasi` birebir regresyon · bütün telemetri akışlarının hedefi geçit · geçit konumu koşu boyunca sabit · korunum |

**Dürüstlük ve gerçekçilik değerlendirmesi (öğrencinin şartı)**

| risk | değerlendirme | karşılığı |
|---|---|---|
| geçidin yere bağı modellenmiyor | Uçtan uca teslimi olduğundan iyi gösterir; ama bütün protokollerde aynıdır (ortak mod) ve sıralamayı değiştirmez | kapsam bölümünde yönüyle beyan |
| tek geçit darboğazı | Kayıpların bir kısmı yönlendirmeden bağımsız olabilir ve "protokol kötü" diye yanlış okunabilir | yük ölçütle seçilir (C3) + kayıp yeri raporu |
| yer istasyonlu mimari yok | Hava–yer kanalı doğrulanmadı; sonuçlar "röle İHA geçitli sürü" için geçerlidir | beyan |
| telemetri hızı ve paket boyu kaynaksız | "Gerçek telemetri" iddiası yapılmaz; yük ölçütle seçilir | `02` §S4 |
| literatürle kıyas | Literatür çoğunlukla rastgele çift kullanır | eşler arası desen keşifsel eksende korunur |

**Sonuç:** bu beş beyanla bir dürüstlük sorunu görünmüyor. Gerçekçilikteki tek
sınır yer istasyonlu mimarinin dışarıda kalmasıdır ve açıkça yazılır.

**Uygulama (11 Eylül 2026, `04` K-116) — onaylı yapıdan farklar**

- **İki geçit uygulanmadı.** Keşifsel eksendi. `gecit_sayisi` alanı da
  eklenmedi: tek değer alan bir alan hiçbir şeyi etkilemezdi. Geçit düğüm 0'dır.
- **Geçit noktası dünya katmanında türetilir** (`dunya/yerlesim.gecit_noktasi`):
  kenar = batı kenarının ortası, merkez = alan merkezi; irtifa bandın ortası.
- **Varsayılan hızlar sunulan yükü korur:** 40 düğümde 39 × 1,0 + 4 × 0,25 =
  40 pkt/s, bugünkü eşler arası yükle aynı. Üç değer de C3'e kadar SINANMAMIŞ.
- **Hız akış başına tutulur.** `Akis` tanımına dokunulmadı, çünkü iki
  kalibrasyon aleti onu doğrudan kuruyor.
- **Kayıp yeri** (`teshis.kayip_yeri`): düşüş sebebi × geçide mesafe bandı,
  0–R · R–2R · 2R+ (R = iletim menzili). Toplamı düşen paket sayısına eşit.
- **Kapsam:** `kapsam.trafik_deseni` her satırda; yere toplamada dört sınır
  `kapsam.desen_sinirlari` altında.
- **Parametre:** 5 yeni (TEDAVİ 1 · KOL TANIMI 1 · SINANMAMIŞ 3); duyarlılık
  borcu 5 → 6 (`gecit_konumu`).

### Y5 · Çoklu hareketli karıştırıcı — 🟢 Y5a uygulandı (`04` K-117) · Y5b öğrenci kararında

**Saha davranışı kaynağı:** öğrencinin sağladığı sentez,
`protokol_kaynaklari/literatur_taramasi_2026-08-31/02_proje_özeli_literatür/taktik-iha-mesh-karistirici-saha-davranislari.md`.
Verdiği çerçeve: sinyal sınıfı × platform × yayın düzeni, dört senaryo ailesi
ve *gözlemle → karıştır → sus → yer değiştir → yeniden karıştır* durum makinesi.

⚠️ Dosyanın kendi beyanına göre gerçek çatışma sahasına ait nicel veri (güç,
hız, süreler, koordinasyon) açık literatürde sınırlıdır; senaryo aileleri
askerî sınıflar değil, deney tasarımı kategorileridir. Bu yüzden zaman ve hız
parametreleri tek bir "gerçek değer" olarak sunulmaz. Bunun yerine **protokol
zaman sabitleri cinsinden ilan edilen eksenler** olarak tanımlanır; Θ'daki
yöntemin aynısı.

**Sentezdeki sinyal sınıflarının simülatördeki karşılığı**

| sentez | simülatör | not |
|---|---|---|
| geniş bant / barrage | `surekli` | tek kanal modelinde bant içi güç |
| aralıklı / darbeli | `surekli_darbeli` | ortalama güç eşit |
| süpürmeli / frekans çevik | `taramali` | tepe eşit, beyanlı asimetri |
| aldatıcı / paket benzeri | `aldatici` | CSMA'ya görünür |
| reaktif | `reaktif` | kanalı dinler, patlar |
| dar bant / spot | temsil edilmez | tek kanal SINR soyutlamasında spot ile barrage arasındaki fark yalnız bant içi güçtür; beyan edilir |
| ton / taşıyıcı | temsil edilmez | PER modeli tonun DQPSK üzerindeki özel etkisini ayırmaz |
| protokol farkında (ACK/önbelge hedefli) | şimdilik yok | 🔵 reaktif sınıfın bir türevi olarak keşifsel eksende eklenebilir |
| hedef korumada anten yönelimi, arazi | temsil edilmez | §12 |

**Yapı**

| parça | yapı |
|---|---|
| tanım | `KaristiriciTanimi(sinif, platform, yorunge, yayin)` donmuş veri. `sinif` boş bırakılırsa senaryo adındaki sınıf uygulanır · `platform ∈ {sabit_yer, arac, hava}` · `yorunge`: başlangıç (alan oranı), tür (`sabit`, `dogrusal`, `devriye`), hız, yön, irtifa · `yayin`: açılma ofseti, düzen (`surekli`, `gorev_cevrimli`, `yay_sus_tasin`), açık ve sessiz süreler, taşınma mesafesi |
| tehdit senaryosu | `TEHDIT_SENARYOLARI: {ad: (KaristiriciTanimi, …)}`. Aileler: `tekli_merkez` (bugünkü tek, merkezde sabit karıştırıcı) · `cephe_hatti` · `derin_sizma` · `hedef_koruma` · `hava_eslik`. Konfigürasyonda `tehdit_senaryosu` — **TEDAVİ**, varsayılan `tekli_merkez`. Senaryo adındaki sınıf `yok` ise karıştırıcı yoktur |
| hareket ve yayın | Yörünge ve yayın çizelgesi **kurulumda önceden hesaplanır**, mobilitedeki gibi. Rastgele parçalar bugün tanımlı ama kullanılmayan `karistirici_yerlesim` ve `karistirici_faz` akışlarından çekilir. `konum(t)` ve `devrede_mi(t)` zamanın saf fonksiyonudur; açılma ve kapanma anları parça sınırlarına eklenir |
| küme | `KaristiriciKumesi` bugünkü karıştırıcı arayüzünü aynen sunar: alınan güç üyelerin toplamı, geçiş anları birleşimleri. **Tek bir çağrı noktası değişir:** taşıyıcı dinleme artık yalnız CSMA'ya görünen üyelerin gücüne bakar; tek karıştırıcıda sonuç birebir aynıdır |
| gölgeleme kimliği | üye k için `−(k+1)`; ilk üye bugünkü `−1`i korur |
| güç eşitlemesi | Aileler **toplam ortalama yayılan güçte** (harcanan girdi) eşitlenir; ρ her ailede bir sonuçtur. Referans güç, çalışma noktası ölçütüyle (bağlantılılık kısıtı altında en büyük ρ) yeniden seçilir — C2 |
| evre metrikleri | açılma anı = senaryonun ilk yayını; parametre olarak kalır |
| kâhin grafiği | tazeleme süresi türetmesine karıştırıcıların en büyük hızı katılır |
| kapılar | `tekli_merkez` birebir regresyon · küme gücü = üyelerin toplamı · hareketli karıştırıcının konumu sürekli, çizelgesi ilan edildiği gibi · karıştırıcı kapalıyken kanal karıştırıcısız kanalla birebir aynı (K-104 kapısının genellemesi) · kâhin hareketli karıştırıcıyı görüyor (grafiğin zamanla değiştiği ölçülür) · her ailede korunum |

### Y6 · Mobilite — formasyon + istasyon tutma — 🟢 uygulandı (`04` K-118)

| parça | yapı |
|---|---|
| model | Yeni kol `formasyon`. İstasyonlar yerleşim çekimlerinin **aynısıdır**; yoğunluk statik ve bağımsız kollarla birebir eşit olduğu için derece eşitlemesi gerekmez. Düğüm istasyonunu mevcut `ISTASYON_TUTMA_S` zaman sabitiyle tutar. Manevra gürültüsü mevcut, türetilmiş araç dinamiği parametrelerinden gelir (`gm_alfa`, `gm_hiz_sigma_ms`) |
| yeni serbest parametre | Çekirdekte yok. İstasyonların yavaş yeniden düzenlenmesi `istasyon_kayma_hiz_ms` ile keşifsel eksende (çekirdekte 0, KOL TANIMI) |
| rastgelelik | yeni `formasyon_jitter` akışı, kurulumda tüketilir. `akis_listesi_hash` değişir; bedeli beyan edilir |
| senaryolar | `MOBILITE_KOLLARI`na `formasyon` eklenir → `formasyon-yok`, `formasyon-surekli`, … |
| Θ | C4 ile ölçülür; §03.3 gereği hem Θ_OLSR hem Θ_AODV raporlanır |
| kapılar | t = 0 konumları statik kolla aynı · sapma sınırlı · duvar teması nadir ve sayılıyor (onaylı hâli "temas 0" idi; öğrenci kararı 11 Eylül, `04` K-119) · aynı tohumda birebir aynı sonuç |

**Uygulama (11 Eylül 2026, `04` K-118) — onaylı yapıdan farklar**

- **Duvar teması sıfır değil:** düğüm-tiklerin %0,021'i (10 tohum). İstasyonu
  tabana ya da tavana birkaç metre yakın düşen düğümler gürültüyle sınıra
  değiyor. Öğrenci "nadir, sayılır ve beyan edilir" kapısını seçti.
- **Ortak fizik:** istasyon tutma döngüsü görev kolundan tek fonksiyona
  taşındı; görev kolu satırları regresyonla birebir sınanır.
- **Kayma ekseni:** her istasyon düğüm başına çekilen yatay bir yönde kayar ve
  kenarda geri döner. Yön çekimi kayma sıfırken de yapılır; gürültü dizisi
  kaymadan bağımsızdır.
- **Regresyon matrisi:** formasyon çapraz çarpıma girmez; iki vaka.
- **Ölçüm:** istasyondan sapma ortalaması 0,86 m · komşu çiftlerin bağıl hızı
  0,17 m/s (bağımsız 0,68 · görev 0,58). Üretici:
  `python -u kalibrasyon/formasyon_olcumu.py`.

### Y7 · Θ'nın protokol başına raporlanması

`senaryolar`da ölçülmüş bir `MOBILITE_THETA` tablosu tutulur (ÖLÇÜLMÜŞ köken).
Satırın kapsam bölümüne kolun Θ_OLSR ve Θ_AODV değerleri yazılır.

### Y8 · İz kanalı — sıra 3

Gösterim içindir ve ölçüme dokunmaz. Kapısı: iz açıkken ve kapalıyken sonuç
satırı birebir aynı (§13). Yapısı Aşama 1 sonunda ayrıca anlatılır.

### Y9 · Teslim olasılığı kâhini — ölçüm aleti

- Kâhin grafiği her bağ için `−ln(1 − (1 − p)^(sınır+1))` ağırlığını saklar.
  Yeni `EnOlasiTeslimKahin` bu ağırlıklarla en kısa yolu seçer.
- Bir karşılaştırma betiği üç kâhini aynı tohumlarda koşar. Tohum başına kâhin
  zarfını ve onu geçen kolları raporlar.
- Kapı: mevcut iki kâhinin sonuçları birebir aynı kalır.

### Y10 · Evre metriklerinin anlamlılık sabitleri — `08` §05.3 — 🟢 uygulandı (`04` K-123)

| parça | yapı |
|---|---|
| tek α | evre metrikleri modülünde tek sabit `ALFA = 0,05`; kökeni ön-kayıt (`06` §7). Bugünkü iki ayrı sabitin yerini alır |
| M4 eşiği | pencere başına `ALFA / taranan pencere sayısı` (Bonferroni). Sentetik boş hipotezde ölçülen yanlış alarm %2,2–3,4; bugünkü kuralda %37–70 (`python -u kalibrasyon/anlamlilik_sabitleri.py`) |
| M3 bandı | `z(1 − ALFA/2)` = 1,96 standart hata; bugünkü 2,0 ile pratikte aynı |
| kapılar | sentetik ölçüm bir kapıya çevrilir: boş hipotezde yanlış alarm ≤ ALFA · G1–G4 yeniden koşulur |
| beklenen etki | Bugünkü satırlarda `tespit_gecikmesi_s` hep boştur (koşum aletleri kopma beyan etmiyor), yani değişmez. `toparlanma_suresi_s` 2,0 → 1,96 yüzünden çok az değişebilir; regresyonla ölçülür |

### 18.1 · Önerilen sıra

```
Y0 regresyon tabanı → Y1 PSR + kontrol istatistikleri → Y2 (A1 sonucuna göre)
→ Y4 yere toplama → Y5 çoklu karıştırıcı → Y6 formasyon → Y3 kontrol eksikleri
→ Y7 → Y10 anlamlılık sabitleri → yeniden kalibrasyon (C1–C7)
→ doğrulama listesi (D1)
```

Her adım ayrı bir regresyon + test koşusuyla kapanır.
