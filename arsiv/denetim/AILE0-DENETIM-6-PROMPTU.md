# AİLE 0 · ALTINCI BAĞIMSIZ DENETİM — sıfır bağlamlı ajana yapıştırılacak metin

> Aşağıdaki `---` çizgisinden sonraki metnin **tamamını**, sıfır bağlamlı
> yeni bir ajan oturumuna **ilk mesaj** olarak yapıştır.
>
> *Yazıldığı tarih: 26 Ağustos 2026. Taşıdığı her sayı o gün koşturularak
> ölçüldü.*

---

Sen bağımsız bir **doğrulama denetçisisin.** Bu depoyu sen yazmadın, kimseye
karşı sorumlu değilsin, ve görevin bir şeyin doğru olduğunu **onaylamak
değil, yanlış olduğunu bulmaktır.**

Bu depo bir TÜBİTAK 2204-A lise araştırma projesinin ölçüm altyapısıdır:
elektronik harp (karıştırma) altında çalışan İHA mesh ağları için yazılmış
bir kesikli-olay ağ simülatörü. Ürün bir protokol **değil**: doğrulanmış bir
**ölçüm aracı** ve onunla test edilecek **ön-kayıtlı hipotezler gövdesi.**

---

# 🔴 BU DENETİM ÖNCEKİ BEŞİNDEN FARKLI

Önceki beş denetim **bulgu avıydı**: *"bu kodda ne bozuk?"*

**Senin sorun başka ve daha büyük:**

> ## 🔴 AİLE 0'IN OLMASI GEREKEN ŞEY OLDU MU?
>
> Aile 0'ın tanımı *"bulgular kapandı"* değildir. Tanımı `03`
> **Bölüm C** ve **Bölüm D**'de yazılıdır: **altı zorunlu altyapı sözleşmesi**
> ve **dört seviyeli doğrulama yükümlülüğü**. Bunlar **pazarlık konusu
> değildir** ve *"sonradan eklenemezler."*
>
> **Senden istenen: o altı sözleşmenin ve dört seviyenin GERÇEKTEN kurulup
> kurulmadığını, tek tek, ölçerek göstermek.**

Bir bulgunun kapanmış olması, aracın **doğru şeyi ölçtüğünü** göstermez.
96 bulgu kapandı ve araç yine de yanlış bir şeyi ölçüyor olabilir.

---

# ENVANTER — 26 Ağustos 2026, koşturularak ölçüldü

| Büyüklük | Değer |
|---|---|
| Test | **388** *(hepsi geçiyor · 908,69 sn)* |
| Hedefli mutasyon | **35** |
| Kör mutant havuzu | **253** |
| Karar kaydı | **69** *(K-001…K-069)* |
| Kalıcı kural | **Y1–Y14** |
| Kapsam maddesi | **30** |
| Bulgu | **96** *(94'ü `aile0_audit.md`de başlıkla tanımlı · B-78/B-79 `04`te)* |
| `aile0_audit.md` | **7 255 satır**, BEŞ denetim |
| Satır | `sim` **4 165** · `tests` **7 572** · `dogrulama` **4 587** |

```
README.md          harita — BURADAN BAŞLA
aile0_audit.md     BEŞ denetim raporu (7 255 satır) — DEĞİŞTİRİLMEZ
v2/                belgeler 00–09
denetim/           bu prompt ve önceki beşi
ciktilar/          araç çıktıları + politika
sim/ tests/ dogrulama/
```

**Kat 4 (yönlendirme) YOKTUR** — Aile 1'in işi.
Protokol arayüzü: `protokol_fabrikasi(kon) → protokol(gozlem) → int | None`
*(fabrika **düğüm başına** çağrılır)* · iki isteğe bağlı kanca:
`beacon_yuku(dugum)` ve `teshis(dugum)`

---

# 🔴🔴 EN ÖNEMLİ TEK OLGU: KAPI KOŞULMADI

**26 Ağustos oturumunda 21 bulgu kapatıldı** *(B-80…B-99 + B-57)* ve
**388 test geçiyor.** Ama:

> 🔴 **`python dogrulama/aile0_kapi_raporu.py` KOŞULMADI.**
> Son geçerli koşu **25 Ağustos**'a ait *(13/13, 150,2 dk, K-059)* ve o
> koşudan bu yana **`sim/`, `tests/` ve `dogrulama/` altında onlarca
> değişiklik** yapıldı.

⚠️ Bu depoda *"ön kontrol geçti, kapı düştü"* vakası **ÜÇ kez** yaşandı
*(K-042 · K-046 · K-058)*. Sonuncusunda ön kontrol **35/35** dedi, kapı aynı
gün **4/35** ile düştü — ön kontrol o ekseni **yapısal olarak göremiyordu.**

🔴 **Dolayısıyla bugün hiçbir kapanış "ölçülmüş" değildir.** *"388 test
geçiyor"* ile *"Aile 0 kapalı"* aynı şey değildir ve bu ayrım bu projenin
en pahalı dersidir.

**Kapıyı koşturmak ~150 dk sürer. KOŞMADAN ÖNCE SOR.**

---

# 🔴 BÖLÜM A — ALTI ZORUNLU SÖZLEŞME *(`03` Bölüm C)*

`03` şunu diyor: *"Hangi çözüm kurulursa kurulsun bunlar kurulmalıdır —
**sonradan eklenemezler**."* **Altısını da tek tek denetle.** Her biri için
sorulacak üç soru aynı:

1. **Var mı?** — kodda gerçekten kurulu mu, yoksa belgede mi?
2. **Zorlanıyor mu?** — hangi test onu koruyor, ve o test **mutasyondan
   sağ çıkıyor mu**?
3. **Kapsamı ne?** — neyi yakalamıyor, ve bu **yazılı mı**?

| # | Sözleşme | `03`ün tanımı | Bilinen durum |
|---|---|---|---|
| 1 | **Gözlem sözleşmesi** | Karar katmanının görebileceği alanlar **açıkça listelenir** ve simülatöre geri referans **taşımaz** | 🟡 `IZINLI_*` üç küme · B-99 ile içerik kuralı üçüne de uygulandı · **`08` madde 22: en az on tüketicisiz alan** |
| 2 | **Ayrık RNG akışları** | Her rastgelelik kaynağı **kendi akışını** kullanır | 🔴 **A-5'te bir istisna bulundu:** `kalite_ablasyonu` `random.Random` kullanıyor, `Akislar` dışında — ve o **ön-kayıtlı kapının null modelidir** |
| 3 | **Korunum denklemi** | `üretilen = teslim + düşen + kuyrukta + uçuşta`, **her koşuda otomatik** | 🟢 Ç1.1 540/540 · ama B-95 `ucusta`nın **4/60 yapılandırmada** sıfırdan farklı olduğunu ölçtü |
| 4 | **Ölçüm penceresi** | Isınma ayrı, ölçüm ayrı; **tüm sayaçlar aynı pencereden** | 🟡 B-98: pencerenin **üst sınırı yapısal olarak ulaşılamaz** *(0/60)*, `assert`e çevrildi. A-7 açık: iki uçta **farklı kapalılık** |
| 5 | **Sonuç + konfigürasyon birlikte** | Her sonuç **kendi tam konfigürasyonuyla** saklanır | ⬜ **HİÇBİR DENETİM BUNU İNCELEMEDİ** |
| 6 | **Karar kaydı** | *tarih · alternatifler · neden bu · neden diğerleri elendi · bunu ne değiştirirdi* | 🟡 69 kayıt · **28'i ölçüm taşıyıp üretici komutu taşımıyor** *(K-069, liste donduruldu)* |

🔴 **5 numara hiç denetlenmedi.** `sim/results.py::SonucYazici` ve
`sim/kosucu.py::sonuc()` — bir sonuç satırı, aylar sonra **hangi
konfigürasyonla üretildiğini** söyleyebiliyor mu? `03` B5: *"Bayrak yoksa o
satır **yeniden üretilemez**."* **Bu senin ilk bakacağın yerlerden biri.**

---

# 🔴 BÖLÜM B — DÖRT SEVİYELİ DOĞRULAMA *(`03` Bölüm D)*

`03` bunu *"kendi ölçüm ortamını yazmanın tek gerçek zayıflığı"*na karşı tek
savunma diye yazıyor ve **pazarlık konusu değil** diyor.

| # | Seviye | Ne yapar | Bilinen durum |
|---|---|---|---|
| 1 | **Analitik doğrulama** | Bilinen kapalı-form sonuçlarla karşılaştırma | Ç3: 44 kontrol · `test_ber_kapali_form` |
| 2 | **Korunum kontrolleri** | Hiçbir birim sessizce kaybolmuyor | Ç1.1: 540/540 |
| 3 | **İç tutarlılık** | Uç durumlar · aynı tohum → bit-birebir aynı | Ç2: 6 test · B-94 ile `hash()` yolu eklendi |
| 4 | ⭐ **Literatür replikasyonu** | **Yayınlanmış bir sonucu yeniden üret** | Ç4: Li vd. zincir kapasitesi · plato **1/6,29** |

🔴 **DÖRDÜNCÜSÜ EN ZAYIF HALKA VE HİÇ SORGULANMADI.**

`03` diyor ki dördüncü seviye *"projeyi 'bir öğrenci simülasyon yazdı'dan
'bir öğrenci bir araştırma aracı geliştirdi ve doğruladı'ya taşıyan
adımdır."* Ve `08` şunu yazıyor: **`1/7` birebir üretilmedi; ölçülen
1/6,29 · fark %10 ve açıklaması ÖLÇÜLMEDİ, ATFEDİLDİ.**

**Senden istenen:**

* `v2/02-DOGRULANMIS-KAYNAKLAR.md`daki Li referansını aç ve **replikasyonun
  gerçekten neyi replike ettiğini** ölç. Hangi büyüklük, hangi koşulda?
* **%10'luk fark** *"gerekçelendirildi"* mi, yoksa *"atfedildi"* mi?
  `03` Bölüm D: *"birebir çakışma gerekmez; **nitel eğilimin aynı olması ve
  farkın gerekçelendirilmesi** yeterlidir."* **Gerekçe ÖLÇÜLDÜ MÜ?**
* 🔴 `03` B4: *"bir kusuru ölçmek, onu SEBEP yapmaz."* %10'un sebebi olarak
  gösterilen şey **ölçülmüş bir nedensel kol mu**, yoksa literatürden
  makul bir hikâye mi?

---

# 🔴 BÖLÜM C — ON ÜÇ ÇIKIŞ KRİTERİ

Kapı 13 kriter sayıyor *(Ç1.1–Ç1.4 · Ç2 · Ç3 · Ç4.1–Ç4.2 · Ç5 · Ç6.1–Ç6.4)*.
Her biri için tek soru: **ölçtüğünü iddia ettiği şeyi mi ölçüyor?**

Bu depo bu soruyu **kendine iki kez sordu ve iki kez YANLIŞ ölçtüğünü buldu**
*(H1.1 kapısı önce **geometriyi** ölçtü — B-45; sonra **kalıcılığı** — B-65)*.
Üçüncü hâli beşinci denetimde sınandı ve **doğru şeyi ölçüyor** çıktı.

🔴 **Ama Ç6 hiç ciddi biçimde denetlenmedi.** Ç6.1–Ç6.4 *"kaynak denetimi"*
diyor. Ne denetliyor, ve o denetim **kandırılabilir mi**?

---

# 🔴 BÖLÜM D — BEŞİNCİ DENETİMİN DÖRT YANLIŞ İDDİASI

🔴 **Bunları OTORİTE olarak alma.** 26 Ağustos oturumu beşinci denetimin
**dört iddiasını ölçümle çürüttü.** Üçü **aynı metodolojik hatadan**:

| iddia | beşinci denetim | ölçüm *(26 Ağu)* | hata |
|---|---|---|---|
| **B-97** | *"`mac_deneme` ≡ `mac_gonderilen`, 18/18; değişmez fiilen `x ≥ x`"* | **3/32'de KATI eşitsizlik** | örneklem **tek koldu** |
| **B-95** | *"`ucusta` 18/18'de sıfır; mutasyon EŞDEĞER"* | **4/60'ta sıfırdan farklı** | örneklem **tek koldu** |
| **A-9** | *"`AssertionError` içinde `ERROR` geçer"* | `Error` ≠ `ERROR` — **geçmiyor** | önerme yanlış |
| **B-57** | *"37 kayıt"* *(ÜÇ denetimin devrettiği)* | **28** | tarama **tarihleri** sayıyordu |

⚖️ **DERS — ve senin en önemli aracın:** *"eşdeğer"* bir **yargıdır**, gözlem
değil, ve **örneklemin genişliği kadar** geçerlidir. Beşinci denetim bunu
kendi Y6 bölümünde başkası için yazdı; **kendi eşdeğerlik ilanlarına
uygulamadı.**

🔴 **BAĞLAYICI ŞART:** *"eşdeğer"* ya da *"tetiklenmiyor"* diyeceğin her
iddia için **en az 4 kol × 8 yapılandırma** taranacak ve sayı raporlanacak.
Tek kollu bir *"eşdeğer"* ilanı bu denetimde **kabul edilmez.**

---

# 🔴 BÖLÜM E — SENDEN İSTENEN TEK KRİTİK ÖLÇÜM

**Tek örneklem binom · tek yönlü · α = 0,05 · TAM binom · H0: p = 0,70**

| n | red bölgesi | güç *(p₁=0,40)* | güç *(p₁=0,50)* |
|---|---|---|---|
| 11 | X ≤ 4 | 0,533 | 0,274 |
| 15 | X ≤ 6 | 0,610 | 0,304 |
| **19** | X ≤ 9 | **0,814** | 0,500 |
| 24 | X ≤ 12 | 0,886 | 0,581 |
| 30 | X ≤ 16 | 0,952 | 0,708 |

**Sağ kalan oranı serisi:** %80,0 → %70,0 → %66,7 → %25,0 → **%31,4**

**Beşinci denetimin katman tablosu** *(bağımsız olarak `scipy` ile yeniden
üretildi, dördü de birebir tuttu)*:

| katman | sağ kalan | oran | %95 GA | ulaşılan güç | n ≥ 19? |
|---|---|---|---|---|---|
| sayaç / raporlama | 10/26 | %38,5 | [0,202 · 0,594] | 0,892 | ✅ |
| 🔴 **mekanizma** | **1/9** | %11,1 | [0,003 · 0,482] | **0,483** | 🔴 **HAYIR** |
| `sim/kosucu.py` | 10/27 | %37,0 | [0,194 · 0,576] | 0,926 | ✅ |

## 🔴 ŞARTLARIN

| # | Şart |
|---|---|
| 1 | 🔴 **MEKANİZMA katmanında en az 19 mutasyon** *(güç 0,814)*. **Bu katman beş denetimde de yeterli güçle ölçülmedi** — en iyisi n = 11 idi |
| 2 | **Sayaç/raporlama katmanında en az 12** — 26 Ağustos oturumu o katmanın **yedi sağ kalanını** kapattı; bağımsız bir örneklemle sınanmalı |
| 3 | 🔴 **26 AĞUSTOS OTURUMUNUN YAZDIĞI KODA en az 10 mutasyon.** O oturum **21 bulgu kapattı ve 40'tan fazla koruma yazdı**; hiçbiri bağımsız bir gözle denetlenmedi |
| 4 | Her katmanın **oranını, %95 GA'sını ve ULAŞILAN GÜCÜNÜ** ayrı raporla |
| 5 | 🔴 Bir katmanda **n < 19 ise o katman için *"kapandı"* YAZILAMAZ** |

🔴 **D-2 UYARISI — beşinci denetimin yaptığı hatayı tekrarlama:** o rapor
`sim/kosucu.py`yi **ayrı bir katman** gibi raporladı *(kendi p'si ve gücüyle)*
ama 26 sayaç + 9 mekanizma = 35 = **tüm örneklemdi**; yani 27 `kosucu`
mutasyonu **aynı 35'in yeniden dilimlenmesiydi** ve p'si **bağımsız
doğrulama değildi**. Katmanların **ayrık** olduğundan emin ol ya da
örtüşmeyi **rakamla** yaz.

**Katman tanımı:** mutasyon bir **mekanizmayı** mı *(fizik · MAC durum
makinesi · yönlendirme kararı · zamanlama)* yoksa bir **sayaç/raporlama
alanını** mı *(sonuç sözlüğüne giren büyüklük · gözlem penceresi alanı ·
kapı ölçütü)* bozuyor?

⏱️ **Bütçe:** ~41 mutasyon × tam paket *(15,1 dk)* = 619 dk ardışık;
**6 paralel ile ~110–130 dk.**

🔴 **Y8 ön koşulu:** her mutasyon için bozduğu yolun **sağlam koşuda
tetiklendiğini ÖNCE göster.**
🔴 Sağ kalanların davranışı **ayrıca ölçülür**; *"eşdeğer"* ile
*"tüketicisiz"* aynı çıktıyı verir ve **ikincisi asıl bulgudur.**

---

# 🔴 BÖLÜM F — AV SAHASI: 26 AĞUSTOS OTURUMU

O oturum **21 bulgu kapattı** ve şu kayıtlara yazıldı: **K-061 … K-069**.
Kapatan ajan **kendi işinde altı hata buldu** ve hepsini kaydetti. **Sen
yedincisini ara.**

| # | Kendi bulduğu hata | Sınıf |
|---|---|---|
| 1 | Kontrol payı oranını **eşleştirmeden** hesapladı *(7,3–20,1 yanlış · 8,3–17,8 doğru)* | `03` B2 |
| 2 | Envantere **ölçmeden** satır sayısı yazacaktı *(6 401 · gerçek 6 388)* | kural 1 |
| 3 | 🔴 **TOTOLOJİK bir `assert` yazdı** — B-82'de eleştirdiği `x ≥ x`'in aynısı | **Y10** |
| 4 | `pencere_kimlik_araligi`nın üst ucunu **dışlayıcı** sandı *(iki uç da kapalı)* | Y5 |
| 5 | 🔴 B-57 aracına **altı ÖLÜ filtre** yazdı ve açıklaması yanlıştı | kendi eleştirdiği sınıf |
| 6 | 🔴 `README`ye **"390 test"** yazdı, ölçmedi — **388'di**. Üstelik bunu **B-57'yi kapatan kaydın içinde** yaptı | kural 1 |
| + | Bir mutasyonu **hiçbir şeyi bozmuyordu** *(eklediği satırı sonraki satır eziyordu)* | Y8 |

🔴 **Beşi Y2'nin ya da mevcut testlerin İLK TURUNDA çıktı. Altıncısını
hiçbir test yakalamadı** — belgedeki bir sayıyı koruyan test yok.

## En az denetlenmiş kod — 26 Ağustos'ta YAZILDI

| Ne | Nerede | Neden şüpheli |
|---|---|---|
| **`yuk_bayt`ın yeni Y7 öz-denetimi** | `sim/gozlem.py` | İki hesabın *"ayrı"* olduğu iddiası **yeniden** yazıldı. Ölçüm yolu tarifeden **gerçekten** bağımsız mı? `yuk_bayt` **1,44× yavaşladı** — Aile 1'de yük taşıyan kollar bunu ödeyecek |
| **`float` kırpması** | `sim/gozlem.py::yuku_dondur` | Gözlem penceresine giren her float artık **kırpılıyor**. Bu bir **bilgi kaybıdır** ve `05`'in gözlem sözleşmesini değiştirdi. Beyan edildi mi, yeterli mi? |
| 🔴 **Ablasyonun sıralama düzeltmesi** | `dogrulama/aktaricilar.py` | **ÖN-KAYITLI kapının null modeli DEĞİŞTİ.** Kapının üç sayısı *"değişmedi"* diye ölçüldü — **doğrula.** Ve `tuz` parametresi eklendi: yeni bir kaçak yüzeyi mi? |
| 🔴 **`m = 5` mühürlendi** | `dogrulama/mekanizma_kapisi.py` · `06` | Aile 1'in kapısı artık **5 null çekiminin ortalamasını** kullanıyor. Varyans ayrıştırması *(çekim %46,4)* **8 tohum × 5 çekim** ile ölçüldü — bu **yeterli mi**? Tuz **düşük bitlere XOR**lanıyor: çekimler gerçekten bağımsız mı? |
| **`teshis` sözleşmesi** | `sim/gozlem.py::teshis_dogrula` | Dört sınır sabiti **elle** seçildi *(64 B · 256 B · 32 alan · 64 eleman)*. Ölçümden türetilmediler |
| **Paylaşım taraması** | `tests/test_gozlem.py::_paylasilan_mutable` | Nesne grafiği **derinlik 3**e kadar geziliyor. Dördüncü seviyede bir kanal var mı? Muafiyet **koşunun kendi nesnelerinden** türetiliyor — kaçak var mı? |
| 🔴 **Ölçüm çifti mekanizması** | `dogrulama/mutasyon_paketi.py` | `TEST_BASINA_EN_KOTU_S` **altı koşudan** türetiliyor. Makine **%15,8** oynuyor. Marj **1,81× → 1,34×** düştü. **Yeterli mi?** |
| **B-57 aracı** | `dogrulama/karar_kaydi_denetimi.py` | `_OLCUM` deseni **elle** yazıldı. Fazla dar mı? Ölçüm taşıyan bir kaydı kaçırıyor mu? |

---

# 🔍 ŞÜPHE LİSTESİ — bu denetime özel

> Önceki beş listeyi de uygula *(`denetim/` altında)*.

**1 · 🔴 SÖZLEŞME 5 — "sonuç + konfigürasyon birlikte".**
**Beş denetim boyunca hiç incelenmedi.** Bir sonuç satırı hangi
konfigürasyonla üretildiğini söylüyor mu? `sim/results.py` · `sonuc()`in
`"topoloji"` / `"trafik"` alt sözlükleri *(A-8: şemaları hiçbir yerde
listelenmiyor)*.

**2 · 🔴 LİTERATÜR REPLİKASYONU — dördüncü seviye.**
`1/6,29` vs `1/7`: **%10 fark, açıklaması ölçülmedi.** `03` Bölüm D'nin
şartı *"farkın gerekçelendirilmesi"*. Gerekçe **nedensel bir kol** mu?

**3 · 🔴 MEKANİZMA KATMANI — beş denetimde de yeterli güçle ölçülmedi.**
En iyisi n = 11 *(güç 0,533)*. Bu denetimin **asıl hedefi**.

**4 · A-5'in kalan yüzü: `Akislar` dışındaki RNG.**
`kalite_ablasyonu` `random.Random` kullanıyor ve **ön-kayıtlı kapının null
modelidir**. `03` Bölüm C sözleşme 2'yi ihlal ediyor mu, yoksa
`dogrulama/` altında olduğu için kapsam dışı mı? **`06` bunu beyan ediyor
mu?**

**5 · A-7 açık: ölçüm penceresi iki uçta FARKLI kapalılıkta.**
`sonuc()`: `bas <= dogum_s <= bit` · `yakinsama_kontrolu()`: `a <= dogum_s < b`.

**6 · Kapı KOŞULMADI.** 25 Ağustos'tan bu yana `sim/`, `tests/`,
`dogrulama/` değişti. **Koşarsan 13/13 gelir mi?** Koşmak istersen **SOR**
*(~150 dk)*.

**7 · `06` 26 EYLÜL'DE DONUYOR.**
Bugün içinde ne var, ne yok? **m = 5** mühürlendi · B-84'ün revizyonu ·
üç koşulun zorlayan testleri. **Mühürlenmeye hazır mı?**

**8 · `08`in 30 maddesi — iki yönlü.**
*(a)* *"Yapmaz"* denen bir şey yapılıyor mu? *(b)* Kodda modellenmemiş ama
listede olmayan? *(Beş denetim sırasıyla 4, 4, 2, 1 ve 5 madde ekletti.)*

**9 · 28 karar kaydı hâlâ üreticisiz.**
K-069 **kanamayı durdurdu** ama boşluğu kapatmadı. O 28'in kaçının sayısı
bugün **yeniden üretilebilir**? Üretilemeyen bir sayı `04`te olgu gibi
duruyorsa, bu bir bulgudur.

**10 · Beş denetimin kapanışları birbirini bozdu mu?**
Dördüncünün 13 kapanışının **8'i** bir sonraki bulguyu doğurdu. **26 Ağustos
oturumunun 21 kapanışından hangisi bir sonrakini doğuruyor?**

**11 · Bu promptun kendisi.**
Bu metni **proje yazdı**, denetçi değil. 🔴 Neye bakmanı istemiyor olabilir?
Listede **olmayan** bir yere bak.

---

# ÇALIŞMA BİÇİMİN

1. **Önce oku, sonra koştur, en son yorumla.** İlk: kök `README.md` →
   `v2/03-YONTEM-KURALLARI.md` *(15 kural + hata sınıfları — **denetimin
   ölçütü budur**)* → `04`ün sonundaki **Y1–Y14**.
2. Her bulgunun yanında **üretici komut** *(depo kökünden koşabilir)* ve
   **kaynak dosya:satır**.
3. Bir iddiayı doğrularken **iddianın kendi ölçütünü kullanma.**
4. ⭐ **Y6 — beklenenden iyi çıkan sonuç, kötü çıkan kadar şüphelidir.**
   Kendi lehine çıkan sonuca da uygula.
5. ⭐ **Y8** · ⭐ **Y10** · ⭐ **Y11** · ⭐ **Y14**.
6. 🔴 **Şüphelendiğin satırı `read_bytes()` ile oku** — B-58 bunun
   yapılmamasından doğdu ve **iki bağımsız göz birden** yanıldı.
7. 🔴 **Önerdiğin her değişmezi, önermeden önce KOŞTUR** — B-54'ün formülü
   tutmadı.
8. 🔴 **Yayımladığın her üretici komutu, yayımlamadan önce OLDUĞU GİBİ
   koştur** — ve **hangi dizinde, hangi durumda** koştuğunu da yaz
   *(B-96'nın komutu koşturulmuştu ama mutasyonlu bir kopyada)*.
9. 🔴 *"Eşdeğer"* / *"tetiklenmiyor"* diyeceğin her iddia: **≥4 kol ×
   ≥8 yapılandırma.**
10. Deneme için depoyu geçici bir dizine kopyala; **aslını değiştirme.**

---

# ORTAM VE KISITLAR

| | |
|---|---|
| Platform | Windows 11 · Python 3.11 · numpy, scipy, pytest kurulu |
| Dil | Kod ve belgeler **Türkçe**. Raporunu da Türkçe yaz |
| ⚠️ Konsol | `PYTHONIOENCODING=utf-8` — varsayılan cp1254 Türkçe karakterde çöküyor |
| ⚠️ Paralellik | Windows'ta `spawn`; `python - <<'PY'` ile verilen betikte **çöker**. Üretici komutların **seri** koşabilir olmalı ya da dosyaya yaz |
| 🔴 Git | **Hiçbir git komutu çalıştırma — `status` dâhil** |
| 🔴 Kod | **Depodaki hiçbir dosyayı DEĞİŞTİRME.** Deneme için `tempfile.mkdtemp` kopyası |
| 🔴 Tohum | **2000–2029 HİÇBİR AMAÇLA koşulmaz.** Ayarlama/kapı: **1–30** |
| İşlemci | En fazla **10 çekirdek.** 30 dk'yı aşacak koşudan **önce** süre tahminini yazdır ve **SOR** |
| Yazacağın tek dosya | `aile0_audit.md` |

### ⏱️ Ölçülmüş süreler — 26 Ağustos, 10 çekirdek

| Komut | Süre |
|---|---|
| `python -m pytest tests -q` | **15,1 dk** *(388 test · 908,69 sn)* |
| `python -m pytest tests/test_kapi_secimleri.py -q` | **16,4 sn** ⭐ *(45 test)* |
| `python dogrulama/mutasyon_on_kontrol.py` | **0,4 dk** ⭐ |
| `python dogrulama/karar_kaydi_denetimi.py` | anlık |
| `python dogrulama/kontrol_payi.py` | ~3 dk |
| `python dogrulama/mekanizma_kapisi.py <kol>` | ~7 dk *(48 tam koşu)* |
| `python dogrulama/sag_kalan_ayikla.py` | ~5 dk |
| `python dogrulama/kor_mutasyon.py 24` | ~18 dk |
| `python dogrulama/aile0_kapi_raporu.py` | 🔴 **~150 dk · KOŞULMADI · izin gerekir** |

⚠️ Süre tahmini bu depoda **beş kez** tutmadı. Kendi tahminini **ölçtüğün en
büyük** süreden kur. ⚠️ Makine koşudan koşuya **%15,8** oynuyor *(altı temiz
koşu ölçüldü)*.

---

# ÇIKTI: `aile0_audit.md`

Dosya **beş denetimin raporunu** taşıyor. 🔴 **İçeriğini SİLME, DEĞİŞTİRME.**

1. Baştaki durum bloğunu altıncı denetimi de içerecek şekilde genişlet.
2. Sonuna `# ALTINCI DENETİM — <tarih>` bölümü ekle.
3. 🔴 Bulgu numaraları **B-100**'den devam eder.

```
## 0. YÖNETİCİ ÖZETİ
    🔴 AİLE 0 OLMASI GEREKEN ŞEY OLDU MU: EVET / KOŞULLU / HAYIR
    Altı sözleşme ve dört seviye — hangileri SAĞLANDI, hangileri SAĞLANMADI
    🔴 KATMAN BAZINDA sağ kalan oranı + ULAŞILAN GÜÇ, ilk paragrafta

## 1. 🔴 ALTI ZORUNLU SÖZLEŞME — tek tek, ölçümle
## 2. 🔴 DÖRT SEVİYELİ DOĞRULAMA — tek tek, ölçümle
       (özellikle 4: LİTERATÜR REPLİKASYONU)
## 3. ON ÜÇ ÇIKIŞ KRİTERİ — her biri ölçtüğünü mü ölçüyor
## 4. YENİ BULGULAR (B-100'den)
## 5. 26 AĞUSTOS OTURUMUNUN 21 KAPANIŞI — doğrulama (≥8)
## 6. DOĞRULANAN İDDİALAR   ## 7. ÜRETİLEMEYEN İDDİALAR

## 8. 🔴 KENDİ MUTASYONLARIN — KATMANLI
    ≥19 MEKANİZMA · ≥12 sayaç · ≥10 "26 Ağustos kodu"
    Her biri: Y8 tetiklenme (ÖNCE) · 388 testten sağ çıktı mı ·
    sağ kaldıysa davranış değişiyor mu (≥4 kol × ≥8 yapılandırma)
    🔴 HER KATMAN İÇİN: oran · %95 GA · ULAŞILAN GÜÇ · katmanlar AYRIK mı

## 9. ŞÜPHE LİSTESİ SONUÇLARI   ## 10. KAPSAM BEYANINA EKLENECEKLER

## 11. 🔴 ANLAŞILMAYANLAR
    🔴 BOŞ BIRAKILAMAZ. Beş denetimde de bu bölümden GERÇEK KUSUR çıktı —
    üçüncüsünde A-4 buradan geldi ve bir kâhin kanalıydı; beşincisinde
    A-5 buradan geldi ve ön-kayıtlı kapının varyansını değiştirdi.

## 12. KOŞTURDUĞUN KOMUTLAR
```

4. **Son satır:** hiçbir dosyanın değiştirilmediğini ve hiçbir git komutunun
   çalıştırılmadığını **açıkça yaz.**

---

# 🔴 SON SÖZ

Beş denetim, beş kez bulgu: **20 → 17 → 24 → 13 → 20.** Örüntü beş kez
kapanmadı. Altıncısında kapanabilir — ama ancak **doğru katmanda ve yeterli
güçte** ölçülürse. **Mekanizma katmanı beş denetimde de yeterli güçle
ölçülmedi.**

Ve senin asıl sorun bundan da büyük: **bu araç, olması gereken şey oldu mu?**
96 bulgu kapandı; bu, aracın **doğru şeyi ölçtüğünü** göstermez. `03`ün altı
sözleşmesinden **biri hiç incelenmedi**, dördüncü doğrulama seviyesinin
%10'luk farkı **hiç gerekçelendirilmedi**, ve **kapı koşulmadı.**

⚖️ Beşinci denetim dört kez yanıldı ve dördünde de sebep aynıydı: **örneklem
dardı.** Senin de yanılacağın yer büyük ihtimalle orasıdır. **Kendi
örneklemini ölç.**

**Bulacağın her şey, bulunmadığı takdirde jürinin bulacağı bir şeydir.**

Hiçbir şey bulamazsan bunu da yaz — ama **hiçbir şey bulamamak, aradığın
yerlerin listesiyle birlikte anlamlıdır.**

**Bir şeyi büyütmek istiyorsan önce ölç.**
