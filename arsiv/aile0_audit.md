# AİLE 0 — DENETİM DOSYASI

> 🔴 **BU DOSYADA BEŞ AYRI DENETİM VAR. BEŞİ DE OLDUĞU GİBİ DURUYOR.**
>
> *(Bu satırın **tek** değişikliği sayının dörtten beşe çıkmasıdır — beşinci denetim, 25 Ağustos 2026. Önceki dört raporun metnine dokunulmamıştır.)*
> *(27 Ağustos 2026 — **altıncı denetim** eklendi. Yine tek değişiklik sayının beşten altıya çıkmasıdır; önceki beş raporun metnine dokunulmamıştır.)*

| | Tarih | Denetlenen | Sonuç |
|---|---|---|---|
| **Birinci denetim** | 19 Ağustos 2026 | K-034'teki **birinci** kapanış *(13/13)* | **20 bulgu.** Kapanış **iptal edildi**; kapatma sırasında 3 bulgu daha çıktı → toplam 23 |
| **İkinci denetim** | 20 Ağustos 2026 | K-043'teki **ikinci** kapanış *(13/13)* + 23 bulgunun kapatıldığı iddiası | **17 yeni bulgu** *(B-24 … B-39, artı B-27b)*. Kapanış **KOŞULLU geçerli** |
| **Üçüncü denetim** | 20 Ağustos 2026 | K-046'daki **üçüncü** kapanış *(13/13)* + 17 bulgunun kapatıldığı iddiası (K-044) | **24 yeni bulgu** *(B-41 … B-64)*. Kapanış **KOŞULLU geçerli**; 17 bulgunun **2'si kapanmamış** *(B-27b · B-32)* |
| **Dördüncü denetim** | 25 Ağustos 2026 | K-054'teki **dördüncü** kapanış *(13/13, 98,2 dk)* + 23 bulgunun kapatıldığı iddiası (K-047…K-055) | **13 yeni bulgu** *(B-65 … B-77)*. Kapanış **KOŞULLU geçerli**. 🔴 **Sağ kalan oranı 6/24 = %25,0** *(güç: n=24, TAM binom, 0,886@p=0,40)* — ama örüntü **kapanmadı, DARALDI**: sayaç/raporlama katmanında oran hâlâ **%45,5** ve H0=0,70 **reddedilemiyor** |
| **Beşinci denetim** | 25 Ağustos 2026 | K-059'daki **beşinci** kapanış *(13/13, 150,2 dk)* + 13 bulgunun kapatıldığı iddiası (K-056) + B-78/B-79 (K-058) | **20 yeni bulgu** *(B-80 … B-99)*. Kapanış **KOŞULLU geçerli**. 🔴 **KATMANLI ölçüm:** sayaç/raporlama **10/26 = %38,5** *(güç **0,892**, H0=0,70 **REDDEDİLDİ** — dördüncüde reddedilemiyordu)* · mekanizma **1/9 = %11,1** *(güç 0,483, n<19 → "kapandı" yazılamaz)* · **`sim/kosucu.py` 10/27 = %37,0** *(4. denetimin kör noktası, ilk kez ölçüldü — örneklemin **en kötü** katmanı)* · genel **11/35 = %31,4** |
| **Altıncı denetim** | 26 Ağustos 2026 | K-070'in TAMLIK denetimi: `03` Bölüm C'nin **altı sözleşmesi** + Bölüm D'nin **dört seviyesi** + 26 Ağustos oturumunun **21 kapanışı** | **18 yeni bulgu** *(B-100 … B-117)*. 🔴 **Kapanış KOŞULLU — ve kapı BUGÜN DÜŞER:** aracın kendi `taban_kontrolu()` koşuldu, **3 kırık / 385 geçen** → Ç1.3 `!!TABAN` *(B-100)*. 🔴 **Altı sözleşmenin ÜÇÜ sağlanmıyor** *(korunum «her koşuda» değil · sayaçlar İKİ pencereden · `SonucYazici` hiç kurulmuyor)*. 🟢 **KATMANLI ölçüm — mekanizma katmanı ALTI DENETİMDE İLK KEZ yeterli güçle:** mekanizma **7/22 = %31,8** *(GA [0,139 · 0,549], güç **0,879**, H0 **REDDEDİLDİ**)* · sayaç **3/20 = %15,0** *(güç 0,872, reddedildi)* · 26 Ağustos kodu **4/15 = %26,7** *(güç 0,610, n<19)* · genel **10/42 = %23,8**. 🔴 **Üç mekanizma boşluğu 388 testin hiçbirince görülmüyor** |

### İkinci denetimin özeti

13 çıkış kriterinin **13'ü de bağımsız olarak yeniden üretildi ve ilan edilen
değerlerle geçiyor** *(540/540 · %0,156 · 30/30 · 44/14/6/6/2 test · 1/6,29 ·
GA %2,04)*. Korunum defteri, defter hiç çağrılmadan **paket nesnesi sayılarak**
dört yapılandırmada doğrulandı. 23 bulgudan **16'sı** bağımsız olarak
sınandı: **13'ü tam kapanmış**, 3'ü kısmen *(B-03 · B-04 · B-08)*.

**Kapanış iptal edilmiyor. Ama üç iddiası ölçümle tutmuyor:**

1. **Örüntü kapanmadı.** Yeni yazılan **10 bağımsız mutasyonun 7'si** 240
   testten sağ çıktı *(birinci denetim: 8/10, 198 testle)*; dördünün davranışı
   fiilen değiştirdiği ayrıca ölçüldü. Kapanan şey **bulgular kümesiydi**,
   örüntü değil.
2. **Kapanış beyanının kendi sayıları bayat.** Birincil çalışma noktasını
   gerekçelendiren tablo *(0,5234 / 0,5087)* ve kör tarama skoru *(%47,8,
   185 mutant, 220 test tabanı)* bugünkü kodla üretilemiyor.
3. **Y7 iki yeni araçta tutmuyor.** `sag_kalan_ayikla.py` bir *araç hatasını*
   "korumasız kod yolu" diye raporluyor; `sim/karsilastirma.py` iki kolun
   **tek bir ortak paketi bile olmadığı hâlde** karşılaştırmayı kabul ediyor.

Ayrıca Aile 1'i doğrudan engelleyen iki şey: **H1.1'in ön-kayıtlı mekanizma
kapısı bu şemayla ölçülemiyor** ve gözlem penceresinin **dört alanının hiç
tüketicisi yok**.

Tam metin: **[İKİNCİ DENETİM](#i̇kinci-denetim--20-ağustos-2026)** *(dosyanın sonu)*.

### Üçüncü denetimin özeti

🔴 **SAĞ KALAN ORANI: 10/15 = %66,7** *(seri: %80,0 → %70,0 → %66,7)*. Nominal
olarak eşiğin altında, **ama örüntünün kapandığı söylenemez**: n=15'te binom
standart hatası ≈ 12,2 puan, ve aynı ölçekte *(ilk 10 mutasyon)* oran **birebir
%70**. Sağ kalan 10'un **4'ü davranışı fiilen değiştiriyor**, **5'i
tüketicisiz**, **1'i simülatörü değil KAPIYI bozuyor**.

Yeniden ürettiğim **her sayı tuttu** *(kalibrasyon · derece kayması · Li
platosu · mekanizma sayacı · K-020 bağ geçişi · sağ kalan ayıklaması ·
envanter · kapının beş beklenen test sayısı)*. **Ama üç şey doğru değil:**

1. **K-044'ün ilan ettiği bir düzeltme kodda YOK.** B-32 için yazılan
   `BEKLENEN_MUTASYON = 35` sabiti hiç eklenmemiş; Ç1.3'ün eşiği hâlâ
   `{toplam}/{toplam}`. Mutasyon listesi 35 → 5'e düşmüş gibi davrandığında
   kapı **"Ç1.3 · 5/5 · OK · 13/13"** diyor. **(B-41)**
2. **Kapının NE ölçtüğü sessizce daraltılabiliyor.** Ç5'in seçimi
   `-k "not test_b27b"` yapılıp beklenen sayı 18→14 indirildiğinde 284/284
   test, ucuz koruma ve kapının Ç5 kriteri **üçü de geçiyor**. **(B-42)**
3. **Aile 1'in iki rakip protokolü bu arayüzle yazılamıyor.** Protokolün
   hiçbir çerçeveye bilgi koyma kanalı yok, hedefin konumu gözlemde yok;
   yazdığım saf gözlem ETX protokolü karıştırıcısız S0'da **0,0997** teslim
   ve **1,00** ortalama atlama veriyor. **(B-47)**

Ayrıca B-27b'nin koruması **elle taşınan bir etikete** dayanıyor ve listesi
**bugün zaten yanlış** *(B-43)*; karıştırıcıyı görebilen tek gözlem alanı
sabitlendiğinde **284/284 geçiyor** *(B-44)*; ve H1.1'in mekanizma kapısı
**null model sınavını geçmiyor** — sıfır bilgi taşıyan bir kol *"gürültüden
kaçan"* koldan daha iyi skor alıyor *(B-45)*.

Tam metin: **[ÜÇÜNCÜ DENETİM](#üçüncü-denetim--20-ağustos-2026)** *(dosyanın sonu)*.

### Dördüncü denetimin özeti

🔴 **SAĞ KALAN ORANI: 6/24 = %25,0** *(taban temiz: 324 passed)*. **Seri:
%80,0 → %70,0 → %66,7 → %25,0.** **Ulaşılan güç**, K-055'in şart koştuğu
biçimde: tek örneklem binom, tek yönlü, α = 0,05, **TAM binom** — n = 24'te
red bölgesi X ≤ 12, gerçek α = 0,0314, **güç 0,886** *(gerçek oran 0,40 ise)*,
**0,581** *(0,50 ise)*. n ≥ 16 şartı **karşılandı**; H0: p = 0,70
**reddedildi** *(p = 7×10⁻⁶, %95 GA = [0,098 · 0,467])*.

🔴 **Ama *"örüntü kapandı"* yazmıyorum — örüntü KAPANMADI, DARALDI.**
Mutasyonları katmanlara ayırdığımda **mekanizma** katmanında oran **%9,1**
*(1/11 — ve o bir tane **gerçek eşdeğer** çıktı, yani korumasız mekanizma
yolu **0/11**)*, **sayaç/raporlama** katmanında **%45,5** *(5/11, %95 GA
[0,167 · 0,766], p = 0,078 — **H0: p = 0,70 REDDEDİLEMİYOR**)*. Önceki üç
denetimin 10 sağ kalanının **8'i** bu ikinci katmandaydı; genel düşüşün büyük
kısmı **örneklem karışımı** farkıdır. Ayrıca `sim/kosucu.py`ye **hiç mutasyon
koymadım** — bu, oranımın en büyük tek yanlılık kaynağı ve raporda yazılı.

**13 yeni bulgu (B-65 … B-77). En ağır üçü:**

1. **Ön-kayıtlı H1.1 mekanizma kapısı tek tohumda kalibre edilmiş** ve
   ayarlama tohumlarının **7/8'inde** kendi null model sınavını geçmiyor;
   null modelin tohumlar arası std'si **0,063**, kapının eşiği **0,02**.
   Sebep ölçüldü: ölçüt bilgiyi değil **seçimin kalıcılığını** ölçüyor —
   karar başına düzgün rastgeleleştirilmiş bir null **+0,00014** veriyor,
   projenin kendi null'ü **+0,054**. Hiçbir gözlem ALANI okumayan, yalnızca
   komşu tablosunun **sırasını** kullanan bir kol **+0,064** alıyor; hiç
   paket teslim etmeyen bir kol **+0,057**. **(B-65)**
2. **B-47'nin açtığı protokol→çerçeve kanalının bedeli kaçırılabiliyor.**
   `yuk_bayt` maliyeti **tipe** göre sayıyor: alan adı uzunluğundan,
   tamsayı büyüklüğünden bağımsız. Tam koşuda **10 bayt bedelle ≥1 236 bayt**
   taşıdım *(124×; sentetik tavan 20 205×)* ve yük **266 komşu kaydına**
   ulaştı. `05` §A2 kural 1 ve K-009'un *"eşit kontrol düzlemi bütçesi"*
   şartı bugün zorlanmıyor. **(B-66)**
3. **`ortak_alt_kume`nin dördüncü ekseni açık.** Üç parmak izi *(paket
   evreni · kurulum · kod sürümü)* **kollar arası** tutarlılığı denetliyor;
   **satır içi** yapı hiç denetlenmiyor. Yarıya kırpılmış bir gecikme
   listesi kabul edildi ve **846,7 ms'lik uydurma bir gecikme farkı** üretildi;
   tekrarlı kimlik, NaN ve negatif gecikme de kabul edildi. **(B-67)**

Ayrıca: `protokol_teshis` slotuna **meşru arayüzden yazılamıyor** ve
B-49'un kapanış testi bunu ancak simülatöre **geri referans** enjekte ederek
gösteriyor *(B-68)*; A-4'ün *"kalan kanal yalnızca modül global'leridir"*
beyanı **yanlış** — fabrikayı saran kapsam da kanal ve `test_a4_…` **geçiyor**
*(B-69)*; B-60'ın nöbetçisi **üç yoldan** atlanıyor, biri çalışma noktasını
**sessizce** değiştiriyor *(B-71)*.

**Yeniden ürettiğim 15 iddianın 15'i tuttu** — B-58'in çürütmesi ham baytla
doğrulandı *(`b"\x1f"` gerçek)*, seçim avantajının dört sayısı, yük bayt
muhasebesi, kanal kanıtı *(1,00 → 2,33)*, güç analizi ve dokuz tüketicisiz
alan dâhil.

Tam metin: **[DÖRDÜNCÜ DENETİM](#dördüncü-denetim--25-ağustos-2026)**
*(dosyanın sonu)*.

### Beşinci denetimin özeti

🔴 **KATMANLI ÖLÇÜM — ve sayaç katmanı ilk kez YETERLİ GÜÇLE ölçüldü.**
35 mutasyon, her biri **TAM 367 testlik paketle**, 72,7 dk:

| katman | sağ kalan | oran | %95 GA | **ULAŞILAN GÜÇ** | H0: p = 0,70 | n ≥ 19? |
|---|---|---|---|---|---|---|
| **sayaç / raporlama** | **10/26** | **%38,5** | [0,202 · 0,594] | **0,892** | **REDDEDİLDİ** *(p = 8,5×10⁻⁴)* | EVET |
| mekanizma | 1/9 | %11,1 | [0,003 · 0,482] | 0,483 | reddedildi | 🔴 **HAYIR** |
| **`sim/kosucu.py`** | **10/27** | **%37,0** | [0,194 · 0,576] | **0,926** | reddedildi | EVET |
| **GENEL** | **11/35** | **%31,4** | [0,169 · 0,493] | **0,970** | reddedildi *(p = 2,9×10⁻⁶)* | EVET |

**Seri %80,0 → %70,0 → %66,7 → %25,0 → %31,4** · **sayaç serisi %45,5 →
%38,5.** Sayaç katmanında H0 **artık reddediliyor** *(dördüncüde n = 11'de
güç yalnızca 0,533'tü)* — ama %95 GA hâlâ **[0,202 · 0,594]**: **daraldı,
kapanmadı.** 🔴 **Mekanizma katmanı için "kapandı" YAZILAMAZ** *(n = 9 < 19,
güç 0,483)*. 🔴 **Dördüncü denetimin beyan ettiği kör nokta ölçüldü ve
haklı çıktı:** `sim/kosucu.py` örneklemin **en kötü** katmanı.

**20 yeni bulgu (B-80 … B-99). En ağır üçü:**

1. **`08`in MÜHÜRLENMEYE HAZIR iki maddesi bugün yanlış — ikisini de aynı
   oturumun kendi düzeltmesi bayatlattı.** Madde 25'in kontrol payı sayıları
   *(%14,9–35,6)* **B-66 ÖNCESİ** maliyet modelinden; eski modelle **birebir**
   yeniden ürettim *(%26,04 · %35,63 · %14,88 · %25,41)*. Bugünkü doğru
   değer **%13,71–33,25**, oran **14–20 kat değil 8,3–17,8 kat**. Madde 24
   ise hâlâ *"alan kimliği 1 B · int/float 4 B"* diyor — kodun kendisi
   *"bu `08`de beyan edilir"* diye **istediği** beyanı almamış. **(B-80 · B-81)**
2. **Ön-kayıtlı H1.1 kapısının ablasyonu İKİ ekseni birden değiştiriyor.**
   `06` *"tek fark BİLGİ"* diyor; ölçüldü: sarmalayıcı komşu demetini
   **yeniden sıralıyor** ve sağlam koşuda demet **%92,8** oranında sırasız.
   Sıraya duyarlı bir sıfır-bilgi kolunda eşleştirilmiş farkın **%100'ü**
   sıralama artefaktı *(beş ondalığa kadar birebir)*, std **0,081** — kapının
   ayırt etmesi gereken sinyalin *(+0,0283)* **2,9 katı**. 🟢 Kapının bugünkü
   **kararı doğru**: yazdığım üç sıfır-bilgi kolunun **üçünü de reddetti**. **(B-84)**
3. **Kapının DÖRDÜNCÜ geçersizlik yolu, K-058'in kapattığı hatayı birebir
   tekrar edebiliyor.** `mutasyon_paketi.py:607` elle yazılmış bir etiket
   taşıyor, `gecersiz_sebebi`yi atlıyor ve 9 `test_b79_*` testinin
   **hiçbiri** oraya dokunmuyor. Etiketi *"mutasyon uygulanamadı"*ya
   çevirdim — **367/367 test geçti.** **(B-88)**

Ayrıca: `yuk_bayt`ın Y7 öz-denetimi **yapısal olarak ölü** *(105 943 kabul
edilen girdide **0** kez ateşlenebiliyor; iki hesap *"ayrı"* değil, birebir
aynı)* **(B-82)**; `float` ekseninde **2,00× kaçak** duruyor **(B-83)**;
`ortak_alt_kume`nin **beşinci ekseni** açık ve araç **%328,5 kesişim**
basıyor **(B-85)**; B-69'un kapanış-hücresi taraması `08`in **kendi beyan
ettiği dört kanaldan üçünü** göremiyor ve sınıf tabanlı protokolde
**çöküyor** **(B-86)**; `teshis` kancasının **hiçbir sözleşmesi yok** —
8/8 sözleşme dışı yük kabul edildi, biri `YASAK_TIPLER`den **(B-87)**.
🔴 **13 kapanışın 8'i bir sonraki bulguyu doğurdu.**

**Yeniden ürettiğim 20 iddiadan 17'si tuttu** — kapının kendi sayıları
*(+0,0283 · +0,0599 · +0,0876)*, K-050'nin **20 sayılık** tablosu, güç
tablosunun **10 hücresi**, `PYTHONHASHSEED` bağımsızlığı ve `-O` eşitliği
dâhil. Tutmayan üçü **aynı kökten** *(B-66'nın kendi düzeltmesi)*.

⚖️ **Y6 uygulandı:** sonuç kendi lehime çıktı *(%45,5 → %38,5)*; kendi
örneklemimde **üç yanlılık** buldum ve biri **kendi iddiamı geri
aldırdı** *(B-96)*.

Tam metin: **[BEŞİNCİ DENETİM](#beşinci-denetim--25-ağustos-2026)**
*(dosyanın sonu)*.


### Altıncı denetimin özeti

🔴 **Bu denetim bir bulgu avı değil, TAMLIK denetimidir** *(K-070)*. Sorulan
soru *"bu kodda ne bozuk"* değil, **"Aile 0'ın olması gereken şey oldu mu"**;
ölçüt `03` **Bölüm C**'nin altı sözleşmesi ve **Bölüm D**'nin dört seviyesidir.

# 🔴 CEVAP: KOŞULLU — ve `python dogrulama/aile0_kapi_raporu.py` BUGÜN DÜŞER.

**Ölçüldü, tahmin edilmedi.** Kapının kendi `taban_kontrolu()` fonksiyonu
koşturuldu: **3 kırık, 385 geçen** → Ç1.3 `!!TABAN`. Sebep:
`mutasyon_paketi.py` geçici kopyayı **`v2/` hariç** kuruyor ve **26 Ağustos
oturumunun yazdığı üç test** `v2/`yi okuyor *(B-100)*. Ucuz ön kontrol bunu
**yapısal olarak göremez** — bu, *"ön kontrol geçti, kapı düştü"* vakasının
**DÖRDÜNCÜSÜ** *(K-042 · K-046 · K-058)*, ve ilk kez **koşmadan önce** görüldü.

**Altı sözleşmenin üçü sağlanmıyor:**

| sözleşme | karar |
|---|---|
| 3 · korunum *"her koşuda otomatik"* | 🔴 `Kosu.kostur()` `defter.kontrol()`u **hiç çağırmıyor**; 47 alanlı sonuçta `korunum_tamam` yok. **Aile 1'in kapısı (48 koşu) korunum kontrol etmiyor** |
| 4 · *"tüm sayaçlar aynı pencereden"* | 🔴 Sayaçların yarısı **tüm koşudan**. Kontrol baytının **%17,89–22,79'u pencere dışında**; kontrol payı **1,010–1,094×** şişik ve **çarpıklık kola göre değişiyor** — `08` madde 25'in bağlayıcı oranı bundan etkileniyor |
| 5 · *"sonuç + konfigürasyon birlikte"* | 🔴 **Beş denetimde hiç bakılmamıştı.** `SonucYazici` **hiçbir ölçüm yolunda kurulmuyor**; `05` §E'nin **beş zorunlu alanından yalnızca biri** var — ve o bir tanesi B-46'da eklenmişti |

**Dördüncü doğrulama seviyesi — literatür replikasyonu:** 1/6,29 **birebir
yeniden üretildi**, ama replikasyon **Li'nin çalışma noktasında koşulmuyor**
*(Li 2 Mbit/s, depo 1 Mbit/s — hiçbir yerde beyan edilmiyor)*. %10'luk açığın
adaylarının **ölçülen üst sınırları yetmiyor**: EIFS ≤%0,49 · RTS/CTS ≤%4,99 ·
bit hızı %1,1 · **gereken %10,1**. 🟢 Buna karşılık Li'nin kendi çalışma
noktasında araç **iki mutlak sayıyı da** üretiyor *(1,761 vs 1,7 Mbps ·
0,277 vs 0,25 Mbps)* — bu hiç yazılmamış.

🔴 **Üç kapanış bir sonraki bulguyu doğurdu:** B-57+B-93 → **B-100** *(kapı)* ·
B-83 → **B-112** *(ölü dal)* · B-46 → **B-113** *(`sag_kalan_ayikla.py`
bugün hiçbir mutanta *"eşdeğer"* diyemiyor — karar kanalı `kaynak_hash` ile
satüre)*.

🟢 **Y13: 26 Ağustos'un 21 kapanışının 21'i de KODDA.** Yeniden ölçtüğüm
yedi sayının yedisi tuttu *(B-80 · B-82 · B-84 · B-94 · B-57 · A-5 · Ç4.2)*.
🔴 **Sekiz sayı bugün üretilemiyor** ve hepsi **mühürlenmeye hazır sayılan
`08`in içinde**.

| katman | sağ kalan | oran | %95 GA | **ULAŞILAN GÜÇ** *(p₁=0,40)* | n ≥ 19? | H0 = 0,70 |
|---|---|---|---|---|---|---|
| 🔴 **MEKANİZMA** | **7/22** | **%31,8** | **[0,139 · 0,549]** | **0,879** | ✅ **EVET** *(altı denetimde İLK KEZ)* | **REDDEDİLDİ** *(p = 2,5×10⁻⁴)* |
| **SAYAÇ / RAPORLAMA** | **3/20** | **%15,0** | [0,032 · 0,379] | **0,872** | ✅ EVET | **REDDEDİLDİ** *(p = 5,4×10⁻⁷)* |
| **26 AĞUSTOS KODU** *(çapraz kesen alt küme)* | **4/15** | %26,7 | [0,078 · 0,551] | 0,610 | 🔴 **HAYIR** | reddedildi *(p = 6,7×10⁻⁴)* |
| **GENEL** | **10/42** | **%23,8** | [0,121 · 0,395] | **0,982** | ✅ EVET | **REDDEDİLDİ** *(p = 8,8×10⁻¹⁰)* |

**AYRIKLIK:** M ∪ S = 22 + 20 = **42 = toplam** · **M ∩ S = 0** *(ayrık ve
tüketici)*. **A** ayrı bir katman değil, **çapraz kesen alt kümedir**:
A ∩ M = **2** · A ∩ S = **13**.

🔴 **"Kapandı" YAZILAMAZ.** Mekanizma katmanı ilk kez yeterli güçle ölçüldü
*(n = 22, güç 0,879)* ve H0 reddedildi — **ama %95 GA [0,139 · 0,549]:**
gerçek oran **%55'e kadar** olabilir. **Daraldı, kapanmadı.**
Seri: **%80,0 → %70,0 → %66,7 → %25,0 → %31,4 → %23,8** *(⚠️ altı örneklem
altı farklı yöntemle seçildi; seri **karşılaştırılabilir değil**)*.

Tam metin: **[ALTINCI DENETİM](#altıncı-denetim--26-ağustos-2026)** *(dosyanın sonu)*.


---

# BİRİNCİ DENETİM — 19 Ağustos 2026

> *(Aşağıdaki gövde, 19 Ağustos'ta yazıldığı hâliyle korunmuştur. Tek
> değişiklik bu başlıktır; içeriğe dokunulmamıştır.)*

## AİLE 0 BAĞIMSIZ DENETİM RAPORU

| | |
|---|---|
| **Tarih** | 19 Ağustos 2026 |
| **Denetçi** | Bağımsız doğrulama denetçisi (sıfır bağlamlı oturum) |
| **Depo** | `C:\Users\Xelma123\Desktop\desparete_pls` — **hiçbir dosyası değiştirilmedi** |
| **Ortam** | Windows 11 · Python 3.11.8 · numpy 1.26.4 · scipy 1.17.1 · pytest 8.2.2 · 12 çekirdek (en fazla 10 kullanıldı) |
| **Git** | Hiçbir git komutu çalıştırılmadı |
| **Toplam koşum süresi** | ~55 dk saf hesap (en uzun tek koşu 12 dk; 30 dk sınırı aşılmadı) |
| **Yazılan tek dosya** | `aile0_audit.md` |

Deneme betiklerinin tamamı geçici bir dizinde (`…\scratchpad\`) tutuldu;
mutasyonlar `tempfile.mkdtemp` kopyalarında uygulandı.

---

## 0. YÖNETİCİ ÖZETİ

> ### Aile 0 kapanmış sayılabilir mi: **KOŞULLU**

13 çıkış kriterinin 13'ünü de bağımsız olarak yeniden ürettim ve **hepsi
ilan edildiği sayılarla geçiyor** (540/540, %0,156, 1/6,29, GA %2,04, 39,
11, 6, 7/7). Korunum denklemini defteri hiç çağırmadan, paket **nesnesi
sayarak** doğruladım — defter dürüst. Fizik sayılarının hepsi (−114 dBm,
40,05 dB, 10,00 dB, 15,5 dBm, 2,1544, 932 kbps) elle formülden birebir
çıkıyor. Bu araç, gördüğüm lise projelerinin çok ötesinde.

**Ama üç şey Aile 1'e bu hâliyle taşınmamalı:**

1. **Gözlem penceresi sızdırıyor.** `Gozlem.gonderilen_bayt` ve
   `alinan_bayt`, düğümün kendi sayaçları değil **ağ genelindeki toplam
   sayaçlardır** — gerçek bir telsizin ölçemeyeceği bir büyüklük, doğrudan
   protokolün eline veriliyor. Kural 5 ve `05-GOZLEM-PENCERESI.md` §A1
   ("Kendi sayaçları") ihlal ediliyor. **(B-01)**

2. **Yakınsama kapısı (K5) S5'te örtüşmeyle körleştirildi.** K-026, kapı
   28/30 koşuda ateşlediği için karıştırıcı **hızını** değiştirdi ve yörünge
   periyodunu yakınsama dilimine **tam eşitledi**. Ölçtüm: bu ayarda dilim
   farkı 0,0089, herhangi bir yakın ayarda 0,060–0,097 ve 18–22/30 koşu
   "yakınsamadı" işaretleniyor. K-026'nın *"örtüşme riski DEĞİL"* savunması
   ölçümle çelişiyor. **(B-03)**

3. **Test paketi sanıldığı kadar koruma sağlamıyor.** Projenin 7 mutasyonu
   7/7 yakalanıyor — ama benim yazdığım 10 bağımsız mutasyonun **8'i tam
   198 testlik paketten sağ çıktı**; aralarında yakınsama eşiğinin
   0,05→0,99 yapılması, ölçüm penceresinin 10 s ısınmaya taşırılması ve
   gözlem penceresinin "en önemli alanı"nın tersine çevrilmesi var. **(B-04)**

Bu üçü düzeltilmeden Aile 1 başlarsa, sonuçlar **yanlış çıkmayabilir ama
savunulamaz** — ki bu proje için ikisi aynı şeydir.

---

## 1. BULGULAR

---

### B-01 · Gözlem penceresi ağ geneli sayaç sızdırıyor (kâhin)

**Ciddiyet:** 🔴 kritik
**Nerede:** `sim/kosucu.py:173-174` · sözleşme: `sim/gozlem.py:96-97` ve `:129`, `v2/05-GOZLEM-PENCERESI.md` §A1

**İddia:** `05-GOZLEM-PENCERESI.md` §A1 tablosu: *"Kendi gönderdiği/aldığı
bayt sayısı → **Kendi sayaçları**"*. `gozlem.py` başlığı: *"Bir düğümün bir
karar anında görebildiği HER ŞEY"*, bölüm başlığı *"kendi donanımından
ölçtükleri"*. Kural 5: *"simülatörün belleğinde olup gerçek donanımda
ölçülemeyecek hiçbir şey karara giremez."*

**Ölçtüğüm:** Alanlar düğüme ait değil, **ağ geneline** ait:

```python
gonderilen_bayt=self.mac.veri_bayt,      # TÜM düğümlerin toplam veri baytı
alinan_bayt=self.mac.kontrol_bayt,       # TÜM düğümlerin toplam kontrol baytı
```

`KanalErisimi._ilet` içinde `self.veri_bayt += …` global bir sayaçtır. Düğüm
başına gerçek değeri ayrıca sayıp karşılaştırdım (S2/orta/tohum=1, 7344 karar):

| t | düğüm | `gozlem.gonderilen_bayt` | düğümün KENDİ verisi | `gozlem.alinan_bayt` |
|---|---|---|---|---|
| 0,0785 | 38 | 1 024 | 0 | 32 |
| 160,11 | 4 | 8 811 520 | 1 074 176 | 237 576 |
| 319,92 | 38 | 17 599 488 | 6 548 480 | 475 252 |

**7344 kararın 7343'ünde gözlemdeki değer, düğümün kendi baytından büyüktü.**
Aynı düğümün ardışık iki kararı arasında kendi baytı hiç değişmezken gözlem
değeri artıyor — yani başka düğümlerin iletimlerini görüyor.

Ayrıca `alinan_bayt` alanı **adıyla da çelişiyor**: "alınan bayt" değil,
ağın toplam **kontrol düzlemi** baytı (beacon + onay) atanmış.

Sızıntının istismar edilebilirliğini de ölçtüm: tek bir düğümün ardışık
gözlemlerinden ağ bayt hızını türetip S3'te *"karıştırıcı şu an açık mı"*
tahmini yaptım — %53,7 doğruluk (şansın hafif üstünde). Yani sızıntı bu
kullanımda **zayıf**, ama alanın kendisi tanım gereği kâhindir.

**Üretici komut:**
```bash
python -c "import sys;sys.path.insert(0,r'C:\Users\Xelma123\Desktop\desparete_pls');from sim.config import Konfig;from sim.kosucu import Kosu;from dogrulama.aktaricilar import en_kisa_yol;k=Kosu(Konfig(kol='x',senaryo='S2',tohum=1),lambda kon:(lambda ic:(lambda g:(print(g.dugum,g.gonderilen_bayt,g.alinan_bayt),ic(g))[1]))(en_kisa_yol(kon)));k.kostur();print('mac.veri_bayt',k.mac.veri_bayt)"
```

**Neden önemli:** `05` §C'nin tüm savunması *"protokol simülatör nesnesini
hiç görmez"*e dayanıyor. Yapısal ayrım doğru kurulmuş ama **pencerenin
içine** ağ geneli bir sayaç konmuş. Jüri bu satırı görürse `05`'in
tamamının güvenilirliği tartışmaya açılır. Aile 1'in protokolleri bu alanı
kullanırsa, ölçülen fark protokolden değil kâhinlikten gelir. Ve `05`
açıkça diyor ki pencereyi **sonradan daraltmak, o zamana kadarki tüm
ölçümleri geçersiz kılar** — yani bu şimdi düzeltilmezse bedeli büyür.

**Öneri:** MAC'te düğüm başına `veri_bayt[d]` / `alinan_bayt[d]` sayaçları
tut; `_gozlem_uret` bunları versin. Testi: iki farklı düğümün gözlemi aynı
anda **farklı** değer vermeli. `05`'e satır eklenmesin — mevcut satır zaten
doğruyu söylüyor, kod ona uydurulsun.

---

### B-02 · `son_iletim_hedefi` sabit −1: bağ bazlı öğrenme yapısal olarak imkânsız

**Ciddiyet:** 🟠 önemli
**Nerede:** `sim/kosucu.py:232`, `sim/kosucu.py:239`

**İddia:** `gozlem.py`: *"⭐ EN ÖNEMLİ ALAN: `son_iletim_sonucu` … Karıştırma
altında en sık gerçekleşen olay budur."* `05` §B: *"Bir bağın gerçek
kalitesi → **Yalnızca kendi denemelerinden çıkardığı tahmin** kullanılabilir."*

**Ölçtüğüm:** Tam koşuda `son_iletim_hedefi`'nin aldığı **tüm** değerler:
`{None, -1}`. Kod her iki yolda da sabit yazıyor:

```python
self.son_sonuc[gonderen] = ("onay", -1)          # kosucu.py:232
self.son_sonuc[gonderen] = ("zaman_asimi", -1)   # kosucu.py:239
```

**Neden önemli:** Bir protokol *"onay geldi"* veya *"zaman aşımı"* bilgisini
alıyor ama **hangi komşuya** ait olduğunu asla öğrenemiyor. `05` §B'nin bağ
kalitesi için izin verdiği **tek** yol budur. Yani gözlem penceresi, kendi
belgesinin izin verdiği tek öğrenme kanalını fiilen kapatıyor. Aile 1'in
tüm hipotezi *"tazelik bilgisini kullanan protokol"* üzerine kurulu — o
protokol bu pencereyle yazılamaz. Gerçek bir telsiz hangi komşuya
gönderdiğini elbette bilir; bu bir kâhin sınırlaması değil, bir **eksik
uygulamadır**.

**Öneri:** `self.son_sonuc[gonderen] = ("onay", hedef)` — hedef zaten
`m.hedef` içinde mevcut, `_onay_geldi`/`_onay_zaman_asimi` sıfırlamadan önce
geri çağrıya taşınmalı. Regresyon testi: koşuda `son_iletim_hedefi` en az
iki farklı düğüm değeri almalı.

---

### B-03 · K5 yakınsama kapısı, S5'te örtüşmeyle körleştirildi

**Ciddiyet:** 🔴 kritik
**Nerede:** `sim/config.py:126-141` (K-026 gerekçesi; savunma cümlesi `:137-140`) · `v2/04-NEDEN-BOYLE.md:676-700` · `sim/kosucu.py:296-321`

**İddia:** K-026: *"⚠️ ÖRTÜŞME (ALIASING) RİSKİ DEĞİL — … yörünge fazı her
tohumda rastgelelenmeye devam ediyor, dolayısıyla varyans kaynağı duruyor.
Kaldırılan tek şey … **yanlılık**."* Aynı cümle `config.py:137-140`'ta.

**Ölçtüğüm (1):** Geometri tam olarak kilitli:

```
yörünge periyodu = 2π·300 / 20,943951… = 90,000000000 s
ölçüm penceresi   = 320 − 50 = 270 s
pencere / periyot = 3,000000000        bir dilim = 1,000000000 yörünge
```

**Ölçtüğüm (2):** S5/orta, 30 tohum, yalnızca karıştırıcı hızı değişerek:

| ayar | periyot | ort dilim farkı | max dilim farkı | yakınsamayan | teslim std |
|---|---|---|---|---|---|
| **HİZALI (sevk edilen)** | **90,0 s** | **0,0089** | **0,0193** | **0/30** | 0,0711 |
| eski (K-026 öncesi) | 125,7 s | 0,0965 | 0,2087 | 22/30 | 0,0716 |
| kaydırılmış | 70,0 s | 0,0598 | 0,1136 | 19/30 | 0,0734 |
| kaydırılmış | 115,0 s | 0,0689 | 0,1365 | 18/30 | 0,0719 |

**Ölçtüğüm (3) — K-026'nın savunmasını doğrudan sınadım.** Topolojiyi,
trafiği ve tohumu sabitleyip **yalnızca karıştırıcı fazını** 16 değere
taradım (tohum=1):

| ayar | teslim std (yalnız faz) | aralık genişliği | ort dilim farkı |
|---|---|---|---|
| HİZALI 90 s | **0,00256** | 0,0104 | **0,0094** |
| hizasız 115 s | 0,00846 | 0,0260 | 0,0560 |

**Faz kaynaklı varyans 3,3 kat, dilim farkı 6 kat bastırılıyor.** K-026'nın
*"varyans kaynağı duruyor"* iddiası ölçümle yanlış; kaldırılan şey yalnızca
yanlılık değil, varyansın kendisidir. `03` B6'nın örtüşme tanımı birebir
gerçekleşmiş: *"Örnekleme aralığı bir periyodu tam bölerse örnekler
kilitlenir."* Tohumlar arası toplam std'nin değişmemesi (0,0711 vs 0,0716)
yanıltıcıdır — o std'ye **topoloji** varyansı hâkimdir; kapının ölçtüğü
büyüklük ise koşu **içi** dilim farkıdır ve o çökmüştür.

**Ölçtüğüm (4) — hizalama kırılgan.** `isinma_s=0` yapınca dilim 106,67 s
olur ve hizalama 90 s'den 115 s'ye **geçer**: bu kez 115 s ayarı 0/30,
90 s ayarı 8/30 işaretler. Yani kapının verdiği sonuç, birbirinden bağımsız
üç konfigürasyon alanının (`isinma_s`, `olcum_bitis_s`, `karistirici_hiz_ms`)
gizli bir aritmetik ilişkisine bağlı. Bu ilişkiyi doğrulayan **hiçbir test
veya `__post_init__` kontrolü yok.**

**Üretici komut:** rapor ekindeki `ortusme_s5.py` / `ortusme_faz.py`
(§8'de tam liste).

**Neden önemli:** K-026 *"NE ELENDİ"* listesinde **"S5'i yakınsama
kapısından muaf tutmak (sorunu gizlerdi)"** yazıyor. Sevk edilen çözüm,
S5'i kapıdan fiilen muaf tutuyor — sadece görünmez biçimde. K5 ön-kaydı
*"Yakınsamamış bir kol, gizlenecek bir kusur değildir — kendisi bir
bulgudur"* diyor; kural 3 *"Senaryoyu sonuç lehine değiştirme"*, kural 12
*"Sonuç beklentiyi tutmayınca parametre ayarlayıp tutturma"* diyor.
Değiştirilen şey metrik değil, **fiziksel senaryo**: karıştırıcı 54 km/h'ten
75 km/h'e çıkarıldı ve bundan sonraki tüm S5 sonuçları, bir kapının
susması için seçilmiş bir hızda ölçülecek.

**Öneri:** Hızı ölçüm gerekçesiyle (senaryonun kendi fiziği) seç, kapıyı
tatmin etmek için değil. Ortam periyodikliğini metrikten çıkarmak
isteniyorsa doğru yer **metriktir**: dilimleri yörünge periyoduna göre tam
sayı katı seç ve bunu `yakinsama_kontrolu` içinde açıkça hesapla; ya da
S5 için dilim farkını faz-eşleştirilmiş bir null modele karşı ölç. Hangisi
seçilirse seçilsin, `03` B6'ya bir kayıt ve
`(olcum_bitis_s - isinma_s)/3` ile yörünge periyodu ilişkisini **kontrol
eden bir test** gerekli.

---

### B-04 · Test paketi sanılan korumayı sağlamıyor — 10 bağımsız mutasyonun 8'i yakalanmadı

**Ciddiyet:** 🔴 kritik
**Nerede:** `tests/` (198 test) · `dogrulama/mutasyon_paketi.py`

**İddia:** Ç1.3 — *"7 mutasyonun 7'si de en az bir testle yakalanıyor"*;
`mutasyon_paketi.py`: *"🔴 BAŞARISIZLIK ÖLÇÜTÜ: bir mutasyon HİÇBİR testi
kırmıyorsa, o kod yolu korumasızdır ve Aile 0 kapanamaz."*

**Ölçtüğüm:** Projenin 7 mutasyonunu yeniden koştum — 7/7 yakalanıyor,
doğru. Sonra **projeden bağımsız 10 mutasyon** yazdım; her biri geçici
kopyada uygulanıp tam 198 testlik paket koşuldu:

| # | Mutasyon | Sonuç |
|---|---|---|
| D1 | `Gozlem.gonderilen_bayt`/`alinan_bayt` → 0 | 🔴 **yakalanmadı** |
| D2 | `son_sonuc = ("onay",…)` → `("zaman_asimi",…)` | 🔴 **yakalanmadı** |
| D3 | Komşu tazelik filtresi kaldırıldı (komşu hiç bayatlamıyor) | 🔴 **yakalanmadı** |
| D4 | Ölçüm penceresi 10 s ısınmaya taşırıldı | 🔴 **yakalanmadı** |
| D5 | Beacon baytları `kontrol_bayt`'a yazılmıyor | 🔴 **yakalanmadı** |
| D6 | Karıştırıcı veri alımında girişim yapmıyor | ✅ yakalandı (6 test) |
| D7 | Kanal çekimi çerçeve başı yerine sonundan | ✅ yakalandı (1 test) |
| D8 | Kuyruk kapasitesi fiilen +1 | 🔴 **yakalanmadı** |
| D9 | Yakınsama eşiği `0,05` → `0,99` | 🔴 **yakalanmadı** |
| D10 | Beacon herkese `(0,0)` konumu bildiriyor | 🔴 **yakalanmadı** |

**8/10 mutasyon 198 testin tamamından sağ çıktı.**

**Üretici komut:** `kendi_mutasyonlarim.py` (§8).

**Neden önemli:** Her biri ayrı bir sözleşmeyi delik bırakıyor:

* **D9** — K5 yakınsama kapısının eşiği hiçbir regresyonla korunmuyor.
  Kapı, kendi eşiği anlamsızlaştırıldığında sessiz kalıyor.
* **D4** — `03` Bölüm C'nin *"Ölçüm penceresi … sonradan eklenemez"*
  sözleşmesi tamamen korumasız. Isınma sızıntısı hiçbir yerde sınanmıyor.
* **D2/D3** — v1'in tüm teşhisi *"karar anında kullanılan bilginin yaşı"*
  idi. Tazelik filtresi ve iletim sonucu semantiği korumasız.
* **D5** — `03` B3 *"Kontrol yükünü baytla say"*; sayaç bozulunca kimse
  görmüyor.

Bu, `03` B5'in *"Kapsam yüzdesine güvenmek"* uyarısının somut hâli. Ç1.3'ün
7/7'si, mutasyonların **zaten test edilmiş yollardan seçilmiş olmasından**
kaynaklanıyor — bir seçim yanlılığı.

**Öneri:** Mutasyon paketini "geçmesi beklenen 7 mutasyon" listesi olmaktan
çıkarıp, dosya başına en az bir **kör** mutasyon üretecek hâle getir (veya
`mutmut`/`cosmic-ray` gibi bir araçla `sim/` üzerinde tam tarama koş).
Yukarıdaki 8'i için önce doğrudan regresyon testi yaz.

---

### B-05 · `kanal_dilimi_s` gerekçesi, K-024'te ÇÜRÜTÜLMÜŞ iddiayı olgu olarak sunuyor

**Ciddiyet:** 🟠 önemli
**Nerede:** `sim/config.py:165-174` ↔ `v2/04-NEDEN-BOYLE.md:587-620` (K-024)

**İddia (kodda okunan):**
```
# 🔴 DEĞER 1 ms'DEN 100 µs'YE İNDİRİLDİ (K-024, B3).
# 1 ms iken başarısız bir iletimin yeniden denemesi çoğu zaman AYNI
# dilime düşüyor ve AYNI rastgele çekimi alıyordu:
#     yeniden deneme aralığı 384–1004 µs → 5 durumun 4'ünde aynı çekim
```

**Ölçtüğüm:** K-024 kaydı **tam tersini** söylüyor ve haklı: ölçülen ardışık
deneme araları 9528–18068 µs, *"1 ms dilimde bile çakışma hiç
olmuyordu"*. Ben de doğruladım: veri çerçevesi 1024 B'ta 8384 µs sürer ve
kanal çekimi çerçevenin **başlangıcına** anahtarlanır; ardışık başlangıçlar
arasında en az bir tam çerçeve süresi vardır. `04-NEDEN-BOYLE.md:1140` bunu
*"❌ Çürütüldü"* olarak listeliyor.

**Neden önemli:** `03` B5: *"🔴 Yorumun kodla çelişmesi — ikisinden de
kötüdür. Belge, kodun kanıtı değildir."* Burada kod yorumu, karar kaydının
çürüttüğü bir iddiayı **kaynak olarak K-024'ü göstererek** olgu gibi
sunuyor. Kodu okuyan biri (jüri, gelecekteki öğrenci, gelecekteki denetçi)
yanlış bilgiyi öğrenir ve *"neden 100 µs?"* sorusuna çürütülmüş cevabı
verir. Kural 1: *"onu üreten kod değişince sessizce bayatlar."*

**İkincil not:** K-024'ün *"marj"* gerekçesi de sınanabilir değil: örnek
olarak verilen 32 baytlık çerçeve **beacon**'dır ve beacon'lar 802.11 yayını
olduğu için **hiç yeniden iletilmez**. Yeniden iletilen en küçük çerçeve
veri paketidir; `paket_bayt=512`'de bile başlangıçlar arası ~4,7 ms'dir.
Marj gerçek bir yoldan değil, oluşamayan bir yoldan hesaplanmış.

**Öneri:** `config.py`deki yorumu K-024'ün sonucuyla değiştir: *"1 ms'te de
çakışma yoktu (ölçüldü: en kısa ara 9528 µs). 100 µs bir **marj kararıdır**;
çerçeve süresi küçüldüğünde güvenlik payının daralmaması için."*

---

### B-06 · İki ablasyon bayrağı hiç okunmuyor — ve her sonuç satırına yazılıyor

**Ciddiyet:** 🟠 önemli
**Nerede:** `sim/config.py:203-204`

**İddia:** Başlık: *"# ---- ablasyon bayrakları ---- Her mekanizma ayrı bir
bayrak."* `bayat_bilgi_null` yorumu: *"null model: aynı güncelleme sayısı,
sıfır bilgi"*.

**Ölçtüğüm:** Depo genelinde arama:

```bash
grep -rn "takvimli_tazeleme\|bayat_bilgi_null" --include="*.py" --include="*.md" .
```
→ **yalnızca tanımlandıkları iki satır.** Hiçbir kod okumuyor, hiçbir belge
anmıyor, hiçbir test kontrol etmiyor. `Konfig.sozluk()` `asdict()`
kullandığı için her sonuç satırına **yazılıyorlar**.

**Neden önemli:** `03` B5 🔴 *"Bildirim ≠ kullanım: Bir bileşen bildirilmiş,
parametre olarak geçirilmiş ve belgelenmiş olabilir — ve hiç çağrılmamış."*
ve Kural 11 ⭐ *"Bir ÖZGÜNLÜK İDDİASINI, onu üreten kod satırını … gösteremeden
yazma."* Somut risk: biri `bayat_bilgi_null=True` ile koştuğunda hiçbir şey
değişmeyecek, ama sonuç satırı *"null model kolu"* diye etiketlenmiş
olacak — `03` B5'in *"Etiketi elle taşımak"* tuzağının en kötü hâli, çünkü
etiket **otomatik** taşınıyor ve yalan söylüyor.

**Öneri:** Ya bayrakları şimdi sil (Aile 2/3'te tekrar eklenir), ya da
`__post_init__`'e *"bu bayraklar henüz uygulanmadı"* diye `NotImplementedError`
koy. Kalıcı çözüm: her `bool` bayrak için *"True yapınca en az bir metrik
değişiyor mu"* diye koşan otomatik bir test.

---

### B-07 · `darbe_gorev_cevrimi` ikinci bir "doğru" kaynağı — H1.3 sessizce kırılabiliyor

**Ciddiyet:** 🟠 önemli
**Nerede:** `sim/config.py:50-60` ve `sim/config.py:128`

**İddia:** `config.py:44-48`: *"⚠️ Darbeli senaryoların TEPE gücü, ORTALAMA
gücü karşılığı sabit senaryoya eşitleyecek şekilde yükseltilir. **H1.3'ün
'aynı ortalama güçte' koşulu budur.**"* Ç3.3 testi bunu *"koşan sistemde
örnekleyerek"* doğruluyor.

**Ölçtüğüm:** Tepe telafisi **modül sabitinden** türetiliyor
(`_TEPE_TELAFI_DB = 10·log10(1/_DARBE_GOREV)`, satır 53), görev çevrimi ise
bir **konfigürasyon alanı** (satır 128). İkisi bağımsız değiştirilebiliyor
ve `__post_init__` yalnızca `0 < d ≤ 1` kontrol ediyor:

| `darbe_gorev_cevrimi` | S1 ort. güç | S3 ort. güç | fark | Ç3.3 geçer mi |
|---|---|---|---|---|
| **0,50 (varsayılan)** | −113,083 dBm | −113,083 dBm | 0,000 dB | ✅ |
| 0,25 | −113,083 dBm | −116,093 dBm | **−3,010 dB** | ❌ |
| 0,10 | −113,083 dBm | −120,071 dBm | **−6,988 dB** | ❌ |
| 0,75 | −113,083 dBm | −111,322 dBm | **+1,761 dB** | ❌ |

Ç3.3 bunu yakalamıyor çünkü **yalnızca varsayılan görev çevriminde**
koşuyor.

**Üretici komut:** `ikinci_kaynak.py` (§8).

**Neden önemli:** Şüphe listesi #4'ün ta kendisi ve projenin bir kez
yaşadığını söylediği hata sınıfı (K-024: rng varsayılanı vs konfig). H1.3
*"aynı ortalama güçte sabit vs darbeli"* hipotezinin **tamamı** bu eşitliğe
dayanıyor; `darbe_gorev_cevrimi` bir tarama ekseni olarak kullanıldığı an
hipotez sessizce başka bir soruya dönüşür.

**Öneri:** `_TEPE_TELAFI_DB`'yi modül sabiti olmaktan çıkar; senaryo gücünü
`Konfig` üzerinden **türetilmiş bir property** yap
(`karistirici_guc_dbm` içinde `10·log10(1/self.darbe_gorev_cevrimi)`).
Ç3.3'ü `@pytest.mark.parametrize("duty", [0.1, 0.25, 0.5, 0.75])` ile koş.

---

### B-08 · K-017'nin "%0,9 derece önyargısı" yeniden üretilemedi (işaret ters) — ve K-017/K-019'un üretici komutu yok

**Ciddiyet:** 🟠 önemli
**Nerede:** `sim/config.py:99-100`, `sim/topology.py:51-53`, `v2/04-NEDEN-BOYLE.md:356-405` (K-017), `:427-464` (K-019)

**İddia:** *"doğal bağlantı oranı %82 · ortalama deneme 1,20 (en kötü 4) ·
ortalama derece kayması **%0,9** (gürültü mertebesinde)"*, 200 tohumla
ölçüldüğü belirtiliyor. Rapora girecek cümle olarak da yazılmış:
*"bunun derece dağılımına etkisi %1'in altında ölçülmüştür."*

**Ölçtüğüm:** 200 000 bağımsız çekim (numpy + `scipy.sparse.csgraph`):

| büyüklük | iddia | ölçtüğüm |
|---|---|---|
| doğal bağlantı oranı | %82 | **%82,93** ✅ |
| ortalama deneme | 1,20 | **1,2058** ✅ |
| gerçek `yerlesim` akışında (200 tohum) | 1,20 / en kötü 4 | **1,200 / en kötü 4** ✅ |
| 30 düğüm / 250 m bağlı tohum | 7/30 | **7/30** ✅ |
| en büyük bileşen aralığı | 10–30 | **10–30** ✅ |
| **ortalama derece kayması** | **+%0,9** | **−%0,362 ± 0,036** ❌ |

Yöntem doğrulaması: koşulsuz ortalama derece **7,44242**, kapalı-form
analitik değer **7,44258** — beşinci haneye kadar uyuşuyor. Koşullu
ortalama **7,41546**. Yani koşullama dereceyi **düşürüyor**, yükseltmiyor;
sapma 10σ ile sıfırdan farklı.

**Üretici komut:** `derece_onyargisi.py` (§8).

**Neden önemli:** Nitel sonuç değişmiyor (*"gürültü mertebesinde, %1'in
altında"* doğru kalıyor), ama:
1. Sayı **işaretiyle** yanlış ve iki ayrı kaynak dosyada (`config.py:100`,
   `topology.py:53`) bağlantı koşullamasını meşrulaştırmak için
   kullanılıyor.
2. **K-017 ve K-019'un hiçbirinde "Üretici:" satırı yok** ve depoda bu
   sayıları üreten hiçbir betik yok. K-022/K-030/K-032/K-034 kayıtlarında
   üretici komut var; bu ikisinde yok.
3. K-019'un tablosu (S2 = +2 dBm'i seçen tablo) **projenin birincil çalışma
   noktasını** belirliyor ve hiçbir şekilde yeniden üretilemez. Kural 1:
   *"Her sayının yanında üretici komut ve kaynak dosya yazılır."*
4. K-019 kendisi *"MAC'in yeniden iletimleri devreye girince kullanılabilir
   bağ tanımı değişir; kalibrasyon mühürden önce tekrarlanacak"* diyor.
   MAC/onay modellemesi 18 Ağustos'ta girdi (K-027); **tekrarlandığına dair
   kayıt yok.** Aynı şekilde K-017'nin *"MAC geldiğinde kanal doluluğu
   ölçülecek"* taahhüdünün karşılığı da yok.

**Öneri:** `dogrulama/kurulum_kalibrasyonu.py` yaz: (a) bağlantı oranı /
deneme / derece kayması, (b) K-019'un güç tablosu — *"yönlendirme kararının
fark ettiği çift oranı"*nın koddaki tanımıyla birlikte. K-017'deki %0,9'u
ölçülen değerle düzelt ve düzeltme tarihini kaydet. K-019'u MAC sonrası
tekrarla; sonuç değişirse S2 seçimi yeniden gerekçelendirilsin.

---

### B-09 · Ç6.2 "kanal dilimi marj değişmezi" bir dizgi eşleşmesi — ölçtüğünü iddia ettiği şeyi ölçmüyor

**Ciddiyet:** 🟠 önemli
**Nerede:** `dogrulama/aile0_kapi_raporu.py:148-151`

**İddia:** Çıkış kriteri Ç6.2'nin adı: *"kanal dilimi marj **değişmezi**"*.
K-024: *"Değişmez bir testle korunuyor."*

**Ölçtüğüm:** Kapının yaptığı tek şey:
```python
("Ç6.2", "kanal dilimi marj değişmezi",
 "kanal_dilimi_s: float = 1e-4" in (KOK/"sim"/"config.py").read_text(...)),
```
Bu bir **kaynak metni araması**. Sonuçları:
* `kanal_dilimi_s: float = 0.0001` yazılsa (davranış birebir aynı) → Ç6.2 **GEÇMEZ**.
* `slot_s`/`sifs_s`/`onay_bayt` değişip marj bozulsa → `1e-4` dizgisi
  durduğu için Ç6.2 **GEÇER**.

Yani kriter, ölçmesi gereken büyüklükle **ters** korelasyonlu.

Gerçek değişmez testi (`tests/test_rng.py:245`) mevcut ve doğru
(`dilim < en_kucuk_ara/3`) — ama Ç3 kapısı yalnızca
`tests/test_kapi_aile0.py` + `tests/test_radio.py` seçiyor, dolayısıyla
**bu test hiçbir kapıya dahil değil.**

**Neden önemli:** K-033'ün kendi dersi: *"bir doğrulama aracı, ne koştuğunu
kendisi doğrulamak zorunda."* Ç6.2 bunu sağlamıyor. `03` B5: *"⭐ Yargıyı
elle yazmak — yargı ve sayı veriden çıkmalı."*

**Öneri:** Ç6.2'yi `tests/test_rng.py::test_dilim_en_kucuk_cerceveyle_bile_guvenli`
+ `test_dilim_hala_protokol_zaman_farkini_yutuyor` dosya-yollu seçimine
bağla (`beklenen_sayi=2`). Ç6.1/Ç6.3'ün grep'leri kalabilir ama adları
*"kaynak denetimi"* olmalı, *"değişmez"* değil.

---

### B-10 · Beacon fazı, `AKIS_ADLARI`'nda olmayan bir rastgelelik kaynağı

**Ciddiyet:** 🟠 önemli
**Nerede:** `sim/kosucu.py:122-137` ↔ `sim/rng.py:38-46`

**İddia:** `rng.py`: *"Bu liste **kapalıdır**: yeni bir rastgelelik kaynağı
eklemek, bu listeye eklemeyi ve NEDEN-BOYLE.md'ye kayıt düşmeyi gerektirir."*
`Akislar.__getitem__` bilinmeyen akışta `KeyError` fırlatıyor: *"Sessizce
yeni akış yaratmıyoruz."* `03` Bölüm C: *"Ayrık RNG akışları — her
rastgelelik kaynağı kendi akışını kullanır … sonradan eklenemez."*

**Ölçtüğüm:** `_beaconlari_basla` beacon fazlarını **`trafik_zamani`**
akışından çekiyor:
```python
r = self.akislar["trafik_zamani"]          # kosucu.py:136
faz = r.uniform(0.0, self.kon.beacon_araligi_s)   # kosucu.py:137
```
`AKIS_ADLARI`'nda `trafik_zamani`'nin tanımı: *"# CBR titreşimi"*. Beacon
fazı için ayrı bir akış **yok** ve `04-NEDEN-BOYLE.md`'de kayıt yok.

Bugün için eşleştirme bozulmuyor — beacon çekim sayısı (`dugum_sayisi`) ve
akış çekim sayısı konfigürasyondan belirlenir, protokolden değil; iki kolun
aynı senaryoyu gördüğünü ayrıca ölçtüm (bkz. §2). **Ama sözleşme
ihlal edilmiş durumda** ve akış paylaşımı tam olarak `rng.py`'nin
önlemek için yazıldığı kuplajı geri getiriyor: akış üzerindeki çekim
sırasını değiştiren herhangi bir gelecek değişiklik (akış sayısı, ısınma
öncesi ek bir kaynak, beacon zamanlamasında titreşim) CBR titreşim dizisini
de kaydıracak.

**Öneri:** `AKIS_ADLARI`'na `"beacon_faz"` ekle, `_beaconlari_basla` onu
kullansın, `04`'e kayıt düş. `AKIS_ADLARI` dışında akış kullanılmadığını
sınayan mevcut testin yanına, **her akışın en az bir yerden çekim aldığını**
sınayan bir test ekle.

---

### B-11 · Yakınsama metriği PDR = 0'da dejenere: tamamen ölü koşu "yakınsadı" işaretleniyor

**Ciddiyet:** 🟡 küçük (ama kapının anlamına dair)
**Nerede:** `sim/kosucu.py:294-321` (`yakinsama_kontrolu`), eşik `:319`

**Ölçtüğüm:** 540 koşuluk ana matriste **bir koşu tamamen ölü**:

```
S2 / seyrek / tohum=30
  teslim_orani       = 0.0        (pencerede üretilen 1079, teslim 0)
  ortalama_gecikme_s = None       ortalama_atlama = None
  yakinsama          = {'dilim_oranlari': [0.0, 0.0, 0.0],
                        'en_buyuk_fark': 0.0, 'yakinsadi': True}
  korunum            = True       boruda kalan = 0
```

1280 paketin **1280'i** `iletim_basarisiz` ile düştü. K5 kapısı bu koşuya
mümkün olan **en iyi** yakınsama skorunu (`fark = 0,0`) veriyor. 13
kriterin hiçbiri bu koşuyu işaretlemiyor.

**Neden önemli:** `03` B3: *"Metrik gerçekten onu mu ölçüyor? Bir metrik
tanım gereği sabit olabilir ve hiçbir bilgi taşımayabilir."* "Hiçbir şey
teslim edilmedi" ile "mükemmel yakınsadı" aynı sayıya eşleniyor. Ayrıca
`ortalama_gecikme_s = None`, tohumlar arası ortalama alan herhangi bir
analiz kodunu patlatır (benim ilk analiz betiğim tam bu satırda çöktü) —
`03` B2'nin *"NaN'ın sessizce zehirlemesi"* uyarısının `None` sürümü.

**Öneri:** `yakinsama_kontrolu`'na `"yakinsadi": None` dönen bir dejenere
dal ekle (`max(gecerli) == 0` veya teslim sayısı eşiğin altında). Sonuç
sözlüğüne `gecikme_gozlem_sayisi` alanı ekle ki `None`'ın "ölçüm yok"
olduğu görülsün (`03` B2: *"üst sınır verirken kaç gözlemle hesaplandığını
da yaz"*).

---

### B-12 · `li_zincir.py` sonuç bölümünde elle yazılmış, bayatlamış sayılar

**Ciddiyet:** 🟡 küçük
**Nerede:** `dogrulama/li_zincir.py:174-188`

**Ölçtüğüm:** Betik ölçüyor, sonra **ölçmediği** sayıları basıyor:

| Betiğin bastığı (sabit) | Aynı koşuda ölçtüğü |
|---|---|
| `Bizim (kayipsiz bag) : 1/6.0` | **1/6,30** |
| `Bizim (menzil sinirinda) : 1/12` | **1/12,61** |
| `4 atlamada ideal zincir bolgesi (1/3.6)` | **1/3,87** |
| `Kalan %16 lik fark (1/6 vs 1/7)` | gerçek açık **%10** |

`06-ON-KAYIT.md` ve `08-AILE0-KAPSAM.md` doğru değerleri (1/6,29, 1/3,87,
%10) taşıyor — yani **betiğin kendi raporu, belgelerle çelişiyor.**

**Üretici komut:** `python dogrulama/li_zincir.py`

**Neden önemli:** `03` B5 ⭐ *"Yargıyı elle yazmak: Yargı ve sayı veriden
çıkmalı. Beklenen sonucu basan bir analiz fonksiyonu, ölçümü süsleme
aracına çevirir."* Bu, K4 kapısının **birincil üretici komutu**; jüriye
gösterilecek çıktı budur.

**Öneri:** Karşılaştırma bloğundaki dört sayıyı `rapor()` dönüşünden
biçimlendir; `%16` da `100*(1/7 − oran)/oran` olarak hesaplansın.

---

### B-13 · İki ölü kontrol

**Ciddiyet:** 🟡 küçük
**Nerede:** `sim/traffic.py:107`, `sim/kosucu.py:135`

**Ölçtüğüm:** Her iki erken-dönüş de asla tetiklenmiyor, çünkü olay ekleme
tarafındaki koşullar zaten engelliyor:

| kontrol | çağrı | tetiklenme |
|---|---|---|
| `TrafikUreteci._uret`: `if simdi > olcum_bitis_s: return` | 10 869 | **0** |
| `Kosu._beacon_at`: `if simdi > kosu_bitis_s: return` | 42 000 | **0** |

**Neden önemli:** Şüphe listesi #3. `config.py:222-227` projenin bu sınıfa
dair bilinçli tavrını gösteriyor: *"Tetiklenemeyen bir kontrol, koruma
sağlamadan koruma izlenimi verir."* Zararsız ama aynı ilke gereği ya
silinmeli ya `assert`'e çevrilmeli.

**Öneri:** Her ikisini `assert simdi <= …` yap; niyet korunur, yanlış
güven kalkar.

---

### B-14 · `Karistirici` dataclass varsayılanı, K-026'nın "yanlış" ilan ettiği hızı taşıyor

**Ciddiyet:** 🟡 küçük
**Nerede:** `sim/radio.py:216-223`

**Ölçtüğüm:**

| alan | `Karistirici` varsayılanı | `Konfig` değeri |
|---|---|---|
| `periyot_s` | 2,7 | 2,7 |
| `gorev_cevrimi` | 0,5 | 0,5 |
| **`hiz_ms`** | **15,0** | **20,943951…** ❌ |
| `yorunge_yaricap_m` | 300,0 | 300,0 |

Bugün zararsız (`senaryodan()` her alanı açıkça geçiyor, depoda başka
`Karistirici(...)` çağrısı yok). Ama `15,0`, K-026'nın *"eski değer …
yakınsama kapısını bozuyordu"* dediği değerdir ve dört alan da
`Konfig`'in ikinci kopyasıdır.

**Neden önemli:** `rng.kanal_cekimi` içinde aynı gerekçeyle
(*"🔴 VARSAYILAN DEĞER YOKTUR — bilerek"*) varsayılan kaldırılmış. Aynı
ilke burada uygulanmamış.

**Öneri:** Dördünü zorunlu alan yap (varsayılanı kaldır) — `senaryodan()`
zaten hepsini geçiyor, hiçbir çağrı kırılmaz.

---

### B-15 · Ç3 kapısında beklenen test sayısı yok — K-033'ün kendi kuralı eksik uygulanmış

**Ciddiyet:** 🟡 küçük
**Nerede:** `dogrulama/aile0_kapi_raporu.py:121-123`

**İddia:** K-033'ün yeni kuralı: *"Her kapı için beklenen test sayısı
yazılı; tutmuyorsa satır `!!SEÇİM n≠m` ile işaretlenip geçmiyor."*
K-033 tablosunda Ç3 satırı: *"Beklenen: —"*.

**Ölçtüğüm:** Ç3 çağrısında `adet=None` — sayı kontrolü **kapalı**. Ç2, Ç5,
Ç4.1'de açık (6/11/6). Oysa *"39 analitik kontrol geçiyor"* ilan edilen
sayı Ç3'ünkü.

**Öneri:** `("Ç3", …, "c3_ or test_radio", 39)` — `aile0_kapi_raporu.py:123`'teki `None` yerine.

---

### B-16 · Alıcı kilidi (preamble capture) modellenmiyor — kapsam listesinde yok

**Ciddiyet:** ℹ️ gözlem (kapsam beyanına eklenmeli)
**Nerede:** `sim/mac.py:531-556` (`_alim_basarili_mi` — yalnız yarı çift yönlü **gönderim** kontrolü var)

**Ölçtüğüm:** Her çerçevenin alım başarısı bağımsız hesaplanıyor; alıcının
"şu an bir çerçeveye kilitli" durumu yok. Sonucu: bir düğüm **zamanda
çakışan iki çerçeveyi de başarıyla alabiliyor.**

| senaryo | toplam başarılı alım | çakışan başarılı alım çifti | oran |
|---|---|---|---|
| S2/yoğun | 104 263 | 51 | %0,049 |
| S0/yoğun | 132 817 | 59 | %0,044 |

Örnek: alıcı 3, `[181,022568 … 181,030952]` veri (düğüm 9) **ve**
`[181,022570 … 181,023018]` yayın (düğüm 11) — beacon veri çerçevesinin
tam ortasında, ikisi de başarılı.

**Neden önemli:** Gerçek bir telsiz bir önbelgeye kilitlenir ve kilitliyken
gelen ikinci çerçeveyi SINR ne olursa olsun çözemez. Etki küçük (~%0,05)
ama **yönü** biliniyor: modelimiz gerçeğe göre biraz **iyimser**.
`08-AILE0-KAPSAM.md`'nin "BU ARAÇ NELERİ YAPMAZ" tablosunda 11 madde var,
bu yok.

---

### B-17 · Saatler kodda tek küresel saat; "senkron değil" yalnızca disiplinle sağlanıyor

**Ciddiyet:** ℹ️ gözlem
**Nerede:** `sim/kosucu.py:166` (`saat_s=simdi`)

**İddia:** `gozlem.py`: *"saat_s — 🔴 KENDİ saati. Düğümler arası SENKRON
DEĞİL."* `05` §A1: *"Düğümlerin saatleri senkron değildir … tek yönlü
gecikme ölçülemez."*

**Ölçtüğüm:** Her düğümün `saat_s`'i `olaylar.simdi` — **tek, kusursuz
senkron küresel saat**. Kayma (offset/drift) modellenmiyor. Senkronsuzluk
yalnızca *"paket başlığına zaman damgası koymama"* disipliniyle sağlanıyor,
yapısal değil.

**Neden önemli:** Bugün sızıntı yok (hiçbir çerçeve zaman damgası
taşımıyor). Ama `05` §A2 protokollere *"başlığa alan koyup bedelini
ödeyerek"* bilgi taşıma hakkı veriyor. Aile 1'de bir protokol beacon'a
zaman damgası koyarsa, **bedava ve kusursuz zaman senkronu** kazanır ve
hiçbir test bunu görmez. Kapsam beyanında da yok.

---

### B-18 · S0 kontrol kolunun tavanı %100 değil

**Ciddiyet:** ℹ️ gözlem
**Nerede:** `v2/06-ON-KAYIT.md:137-139`

**İddia:** *"Böylece karıştırıcısız senaryoda teslim tavanı %100'dür ve her
kayıp karıştırmaya ya da protokole atfedilebilir."*

**Ölçtüğüm (90 koşu, S0, 3 trafik × 30 tohum):** ortalama teslim **0,9935**,
aralık **[0,8701 · 1,0000]**, std 0,0148. Ana matriste S0'da 3137 paket
`iletim_basarisiz` ile düştü. Kaynak: menzil sınırında PER (1024 B için
%16,97) ve MAC çakışmaları — ikisi de topolojiden veya karıştırmadan
bağımsız.

**Neden önemli:** `03` B1 *"etkinin sıfır olması gereken bir kol"* fikri
sağlam ama taban %100 değil, ~%99 ve en kötü tohumda %87. Aile 1'de "S0'a
göre kayıp" hesaplanacaksa bu taban raporlanmalı, yoksa küçük etkiler taban
gürültüsüyle karışır.

---

### B-19 · Gecikme yalnızca teslim edilenden ölçülüyor — seçilim yanlılığı ölçüldü

**Ciddiyet:** ℹ️ gözlem (Aile 1 için kritik olacak)
**Nerede:** `sim/kosucu.py:245-248`

**Ölçtüğüm (540 koşu, senaryo bazında):**

| senaryo | teslim ort. | ort. gecikme |
|---|---|---|
| S0 | 0,9935 | 48,63 ms |
| S1 | 0,6806 | 48,97 ms |
| S2 | **0,5029** | **49,77 ms** |
| S3 | 0,8008 | 51,09 ms |
| S4 | 0,6973 | 52,25 ms |
| S5 | 0,6432 | 51,44 ms |

Teslim oranı **yarıya** düşerken gecikme yalnızca **%2** artıyor. Sebep
`03` B3'ün ⭐ uyarısı: gecikme yalnızca **hayatta kalanlardan** ölçülüyor;
zor paketler teslim edilmediği için gecikme dağılımına hiç girmiyor.

**Neden önemli:** `03` B3 çözümü de veriyor: *"Ortak alt küme üzerinden
karşılaştır ve kesişim oranını raporla."* Sonuç sözlüğünde bunu mümkün
kılacak hiçbir alan yok (paket kimliği bazında teslim listesi yok). Aile
1'de iki protokol gecikmede karşılaştırıldığında bu **şu anki şemayla
yapılamaz** — ve `03` B5 *"Şemanın kaybolması"* diyor: şema sonradan
değişirse eski satırlar karşılaştırılamaz.

---

### B-20 · `kontrol_bayt` önbelgeyi saymıyor: airtime payı bayt payının 1,8 katı

**Ciddiyet:** ℹ️ gözlem
**Nerede:** `sim/kosucu.py:260-261`, `sim/mac.py` (`kontrol_bayt`)

**Ölçtüğüm (S2/orta/tohum=1):**

| ölçüt | kontrol payı |
|---|---|
| **bayt** cinsinden | %2,84 |
| **airtime** cinsinden | %5,11 |

Önbelge tek başına onay çerçevesinin **%63'ü**, beacon çerçevesinin
**%43'ü** — ve `config.py:106-109` bunu zaten yazıyor: *"⚠️ Küçük gibi
görünür ama ONAY çerçevesi için baskın maliyettir."*

**Neden önemli:** `03` B3 *"Kontrol yükünü paketle sayma — bayt cinsinden
say"* diyor ve bu uygulanmış (doğru). Ama bu düzenekte gerçek kıt kaynak
**kanal zamanı**dır; aynı bayt sayısını farklı çerçeve sayısına bölen iki
protokol, bayt metriğinde eşit, airtime'da 2 kat farklı görünür. Aile 1'in
"eşit kontrol bütçesi" iddiası (K-009) bayt üzerinden kurulmuş.

**Öneri:** Sonuç sözlüğüne `kontrol_airtime_s` ve `veri_airtime_s` ekle;
üçlü sunumda (teslim · gecikme · kontrol yükü) kontrol yükünü her iki
birimde raporla.

---

## 2. DOĞRULANAN İDDİALAR

Bağımsız olarak yeniden ürettiğim ve **TUTAN** iddialar.

### A · 13 çıkış kriteri — hepsi ilan edilen sayılarla

`python dogrulama/aile0_kapi_raporu.py` (9,2 dk, benim koşumumda):

| # | ölçülen | eşik | sonuç |
|---|---|---|---|
| Ç1.1 | 540/540 | 540/540 | ✅ |
| Ç1.2 | 4/4 | 4/4 | ✅ |
| Ç1.4 | %0,156 | < %1 | ✅ |
| Ç1.3 | 7/7 | 7/7 | ✅ |
| Ç2 | 6 geçti, 0 kırıldı | 0 kırık | ✅ |
| Ç3 | 39 geçti, 0 kırıldı | 0 kırık | ✅ |
| Ç5 | 11 geçti, 0 kırıldı | 0 kırık | ✅ |
| Ç4.2 | 1/6,29 · GA %2,04 | GA < %5 | ✅ |
| Ç4.1 | 6 geçti, 0 kırıldı | 0 kırık | ✅ |
| Ç6.1–6.4 | evet · evet · evet · evet | evet | ✅ |

Tam test paketi ayrıca: **198 test, 198 geçti, 142,6 s.**

### B · Fiziksel sayılar — elle formülden, simülatör fonksiyonu kullanmadan

| iddia | ölçtüğüm | not |
|---|---|---|
| Termal gürültü −114 dBm | **−113,975 dBm** (kTB) | +6 dB NF ile −107,975 |
| Yol kaybı 1 m'de Friis'e birebir 40,05 dB | **40,0520 dB** | `20·log10(4π/λ)` ile birebir |
| Menzil sınırında SINR tanım gereği eşiğe eşit | **10,000000 dB** | tam eşitlik |
| Türetilen verici gücü 15,5 dBm | **15,4916 dBm** | elle `N+β+PL(R)` = 15,4916 |
| Girişim oranı β^(1/α) = 2,1544 | **2,154435** | `10^(1/3)` ile birebir; menzil 603,242 m |
| Tek atlama verimi 932 vs analitik 933 | **931,9 ölçülen / 932,7 analitik** | 12 866 µs döngü |
| Li ideal zincir bölgesi 1/3,87 (4 atlama) | **1/3,87** | |
| Li uzun zincir platosu 1/6,29 | **1/6,30** (5 tohum) · **1/6,29** (30 tohum) | |

Bonus: 4 atlamadaki `basarisiz` sıçraması (%0,9 → %15,3) mekanizmasıyla
anlaşıldı — 4 atlamada ilk kez düğüm 0 ile 3 arasındaki mesafe (714 m)
girişim menzilini (603 m) aşıyor ve **gizli terminal** doğuyor. Model
doğru davranıyor.

### C · Korunum — defteri çağırmadan, paket **nesnesi** sayarak

Her `Paket` nesnesinin koşu sonundaki fiziksel yerini (kuyruk / MAC eli /
havada / hiçbir yer) bağımsız sayıp deftere karşılaştırdım:

| senaryo | üretilen | teslim | kuyrukta | düşmüş | defterle uyum | aynı anda >1 yerde nesne |
|---|---|---|---|---|---|---|
| S2/orta | 3197 | 2197 | 0 | 1000 | ✅ tam | **0** |
| S4/yoğun | 6395 | 4420 | 0 | 1975 | ✅ tam | **0** |
| S0/seyrek | 1277 | 1276 | 0 | 1 | ✅ tam | **0** |

Defter dürüst; çift sayım veya askıda nesne yok.

### D · Eşleştirme (Ç2.3) — kapının kendi aracını kullanmadan

`mac.kanal_izi`'ne güvenmeden, aynı tohumda iki farklı kolun senaryosunu
bileşen bileşen karşılaştırdım:

| bileşen | aynı mı |
|---|---|
| düğüm konumları (40 nokta) | ✅ |
| trafik çiftleri + ilk gönderim fazları | ✅ |
| karıştırıcı fazı | ✅ |
| iki kol gerçekten farklı davranıyor mu | ✅ (11 139 vs 11 196 iletim; 0,7255 vs 0,6910 teslim) |

### E · Başlangıç koşulları (şüphe #6)

| bileşen | t = 0 durumu |
|---|---|
| komşu tablosu | ✅ boş (40/40 düğüm) |
| kuyruklar | ✅ boş |
| MAC durum makinesi | ✅ hepsi `bos` |
| MAC çekişme penceresi | ✅ hepsi `cw_min = 31` |
| karıştırıcı fazı | ✅ tohuma bağlı rastgele (0,785…) |
| CBR fazı | ✅ akış başına `U(0, 1)` |
| beacon fazı | ✅ düğüm başına `U(0, 1)` (ama bkz. B-10) |

### F · Kurulum kararları

| iddia | ölçtüğüm |
|---|---|
| %82 doğal bağlantı | **%82,93** (200 000 çekim) |
| ortalama 1,20 deneme (en kötü 4) | **1,2058** / gerçek akışta **1,200**, en kötü **4** |
| 30/250 elendi: 7/30 bağlı, bileşen 10–30 | **7/30**, **10–30** — birebir |
| Darbeli senaryoların ortalama gücü sabit karşılığına eşit | **S3 = −4,0000 dBm = S1**, **S4 = +2,0000 dBm = S2** (varsayılan görev çevriminde) |
| Yörünge periyodu = pencere/3 = 90 s | **90,000000000 s** |
| Ana deney tohumları (2000–2029) hiç koşulmadı | ✅ hiçbir betikte/testte geçmiyor |
| Komşuluk yalnızca beacon'dan, t=0'da boş | ✅ (D3/D10 mutasyonları menzil tablosundan türetilmediğini de gösterdi) |
| `skeleton.py` silindi | ✅ dosya yok |

### G · Rezonans — beacon/CBR aynı periyot ama etki YOK

Beacon aralığı (1,0 s) = CBR aralığı (1,0 s) ve beacon'da titreşim yok;
iki düğümün beacon fazı farkı koşu boyunca donuyor. Fazlar arası
sistematik beacon kaybı arandı — **bulunamadı**:

| faz farkı | çift | ort. alınan beacon (350 üzerinden) |
|---|---|---|
| 1–5 ms | 4 | 347,8 |
| 5–20 ms | 12 | 346,0 |
| 20–50 ms | 26 | 347,3 |
| 50–150 ms | 56 | 344,0 |
| 150–500 ms | 158 | 346,3 |

Sebebi anlaşıldı: `_yayin_ilet` her beacon için yeniden `randint(0, 31)`
geri çekilme çekiyor, bu da donmuş fazı her periyotta 0–620 µs
rastgeleleştiriyor. **Temiz.**

---

## 3. ÜRETİLEMEYEN İDDİALAR

| iddia | nerede | durum |
|---|---|---|
| **Bağlantı koşullamasının derece önyargısı %0,9** | `config.py:100`, `topology.py:53`, K-017 | ❌ **Üretilemedi.** Ölçtüğüm **−%0,362 ± 0,036** (200 000 çekim, 10σ). İşaret ters, büyüklük 2,5 kat farklı. Nitel sonuç (*"gürültü mertebesinde"*) değişmiyor. → **B-08** |
| **K-019 karıştırıcı gücü tablosu** (S2 = +2 dBm seçimi) | K-019, `config.py:33-39` | ❌ **Üretilemedi** — depoda bu tabloyu üreten hiçbir betik yok ve *"yönlendirme kararının fark ettiği çift oranı"* metriğinin kod karşılığı bulunamadı. Projenin **birincil çalışma noktası** yeniden üretilemez durumda. → **B-08** |
| K-017'nin diğer sayıları: ort. atlama 2,90 · çap 6,6 (5–12) · ort. derece 7,5 | K-017 | ⚠️ Kısmen: ort. derece **7,442** (analitikle uyumlu, 7,5'e yuvarlanmış). Atlama/çap için üretici komut yok, ölçmedim. |
| K-019'un *"kalibrasyon mühürden önce tekrarlanacak"* taahhüdü | K-019 son satır | ❌ **Karşılığı bulunamadı** — MAC/onay 18 Ağustos'ta girdi (K-027), tekrarlanan kalibrasyon kaydı yok. |
| K-017'nin *"MAC geldiğinde kanal doluluğu ölçülecek"* taahhüdü | K-017 son satır | ❌ Karşılığı bulunamadı. |
| `li_zincir.py`nin bastığı 1/6.0 · 1/12 · 1/3.6 · %16 | `li_zincir.py:174-188` | ❌ Aynı betiğin kendi ölçümü 1/6,30 · 1/12,61 · 1/3,87 · %10 veriyor. → **B-12** |
| K-026: *"varyans kaynağı duruyor"* | K-026, `config.py:138` | ❌ **Çürütüldü** — faz kaynaklı varyans 3,3 kat, dilim farkı 6 kat bastırılıyor. → **B-03** |
| `config.py`: *"1 ms iken … 5 durumun 4'ünde aynı çekim"* | `config.py:166-168` | ❌ Zaten K-024'te çürütülmüş; kod yorumu güncellenmemiş. → **B-05** |

---

## 4. KENDİ MUTASYONLARIM

10 mutasyon, her biri geçici kopyada, her biri **tam 198 testlik paketle**
sınandı. Asıl depo değişmedi.

| # | dosya:hedef | ne bozuyor | kırılan test | sonuç |
|---|---|---|---|---|
| D1 | `kosucu.py:173-174` | `Gozlem` bayt alanları → 0 | 0 | 🔴 **yakalanmadı** |
| D2 | `kosucu.py:232` | `("onay")` → `("zaman_asimi")` | 0 | 🔴 **yakalanmadı** |
| D3 | `kosucu.py:161-162` | komşu tazelik filtresi kaldırıldı | 0 | 🔴 **yakalanmadı** |
| D4 | `kosucu.py:245-246` | ölçüm penceresi 10 s ısınmaya taştı | 0 | 🔴 **yakalanmadı** |
| D5 | `mac.py:_yayin_geri_cekilme_bitti` | beacon baytı `kontrol_bayt`'a yazılmıyor | 0 | 🔴 **yakalanmadı** |
| D6 | `mac.py:_girisim_w` | karıştırıcı veri alımında girişim yapmıyor | **6** | ✅ yakalandı |
| D7 | `mac.py:_alim_basarili_mi` | kanal çekimi `bitis_s`'ten | **1** | ✅ yakalandı |
| D8 | `queues.py:60` | kapasite `>=` → `>` (fiilen +1) | 0 | 🔴 **yakalanmadı** |
| D9 | `kosucu.py:319` | yakınsama eşiği 0,05 → 0,99 | 0 | 🔴 **yakalanmadı** |
| D10 | `kosucu.py:141` | beacon herkese `(0,0)` konumu bildiriyor | 0 | 🔴 **yakalanmadı** |

**Yakalanma oranı: 2/10.** Karşılaştırma: projenin kendi 7 mutasyonu 7/7.

D6'yı yakalayan testler: `test_c5_3c_karistirma_beacon_kaybettiriyor`,
`test_c1_3_mutasyon_hangi_kontrol_yakaliyor`,
`test_c3_2_parca_parca_hesap_sabit_girisimde_tek_parcaya_esit`,
`test_karistiricinin_etkisi_var`,
`test_mac_dusurmesi_karistirici_altinda_artiyor`,
`test_karistirici_alimi_bozuyor`.
D7'yi yakalayan: `test_c2_3_iki_kol_ayni_kanali_goruyor`.

**Örüntü:** Radyo ve MAC fiziği iyi korunuyor. **Gözlem penceresi, ölçüm
penceresi, kontrol düzlemi muhasebesi ve kapı eşikleri hiç korunmuyor** —
yani sözleşme katmanı, fizik katmanının çok gerisinde. → **B-04**

---

## 5. ŞÜPHE LİSTESİ SONUÇLARI

| # | şüphe | sonuç |
|---|---|---|
| 1 | **Kâhin sızıntısı** | 🔴 **Bulgu var → B-01.** Ayrıca aktarıcılar hakkında: `en_kisa_yol` (açıkça KÂHİN) Ç1.1/Ç1.2/Ç1.4'ün **tüm** sayılarını üretiyor. Saf gözlem aktarıcısıyla (`gurultuden_kacan`) aynı matrisi koştum: korunum yine 60/60 ✅ ama **boruda kalan %0,031 → %0,531 (17 kat)** ve dört düşme sebebinin dördü de **doğal olarak** tetikleniyor (uç durum konfigürasyonu gerekmeden). Yani Ç1.4'ün %0,156'sı aracın değil, **kâhin aktarıcının** özelliği. → **B-04 eki**, §6 |
| 2 | **Bildirim ≠ kullanım** | 🔴 **Bulgu var → B-06** (2 ablasyon bayrağı hiç okunmuyor), **B-02** (`son_iletim_hedefi` sabit −1), **B-01/D1** (bayt alanları hiçbir yerde tüketilmiyor) |
| 3 | **Ölü kontrol** | 🟡 **Bulgu var → B-13.** İki ölü erken-dönüş (0/10 869 ve 0/42 000 tetiklenme). Ayrıca **B-09**: Ç6.2 kriteri, ölçtüğünü iddia ettiği değişmezle ters korelasyonlu |
| 4 | **İkinci "doğru" kaynağı** | 🟠 **Bulgu var → B-07** (`darbe_gorev_cevrimi` ↔ `_DARBE_GOREV`; H1.3 sessizce kırılıyor), **B-14** (`Karistirici.hiz_ms = 15,0`) |
| 5 | **Rezonans ve örtüşme** | 🔴 **Bulgu var → B-03** (yörünge periyodu = yakınsama dilimi, tam 1,000). Ayrıca: pencere / darbe periyodu = 270 / 2,7 = **tam 100**, kanal dilimi / MAC slotu = **tam 5**. Beacon/CBR aynı periyot (1,0 s) ama **etkisi ölçüldü ve yok** (§2-G) — temiz |
| 6 | **Isınma ve başlangıç koşulu** | ✅ **Temiz.** Yedi durum tutan bileşenin hepsi t=0'da açıkça tanımlı (§2-E). Kural 14 titizlikle uygulanmış |
| 7 | **Eşleştirmenin gerçekten eşleştirme olması** | ✅ **Temiz** — kapının kendi aracı kullanılmadan doğrulandı (§2-D). ⚠️ Tek uyarı **B-10**: beacon fazı `trafik_zamani` akışına biniyor; bugün bozmuyor, gelecekte bozabilir |
| 8 | **Korunum denkleminin körlüğü** | ✅ Nesne sayımıyla doğrulandı (§2-C). Beacon boşluğu **kapsam beyanında zaten yazılı**. Denklemi kıran başka bir yol **bulamadım** — aradığım yollar: paylaşılan `Paket` nesnesi (onay kaybında gönderen + alıcı aynı nesneye bakıyor → çift sayım yok, doğrulandı), kopya alımı, kuyruk taşması ile eşzamanlı kabul, koşu sonu kesintisi |
| 9 | **Metrik gerçekten onu mu ölçüyor** | 🟡 **Bulgu var → B-19** (gecikme seçilim yanlılığı, ölçüldü: PDR 0,99→0,50 iken gecikme +%2), **B-20** (kontrol yükü bayt vs airtime, 1,8 kat), **B-11** (yakınsama PDR=0'da dejenere). `teslim_orani`, `kontrol_bayt` (çift faturalama yok) tanımları **doğru** |
| 10 | **Sayılar üretilebilir mi** | 🟠 **Bulgu var → B-08, B-12.** Rastgele seçtiğim 8 fizik sayısının 8'i üretildi; kurulum sayılarından **%0,9 üretilemedi**, K-019 tablosu **hiç üretilemez**; `li_zincir.py`nin 4 sonuç sayısı bayat |
| 11 | **Testler bir şey ölçüyor mu** | 🔴 **Bulgu var → B-04.** 10 mutasyonun **8'i** yakalanmadı |
| 12 | **Sınırların dürüstlüğü** | 🟡 **Bulgu var → §6.** Beş eksik madde bulundu |

---

## 6. KAPSAM BEYANINA EKLENMESİ GEREKENLER

`08-AILE0-KAPSAM.md` "BU ARAÇ NELERİ YAPMAZ" tablosunda 11 madde var.
Kodda modellenmemiş ama listede olmayanlar:

| # | eksik madde | etkinin yönü | kanıt |
|---|---|---|---|
| 12 | **Alıcı kilidi (preamble capture / receiver lock)** — bir düğüm çakışan iki çerçeveyi de başarıyla alabiliyor | Modeli gerçeğe göre **iyimser** yapar | ölçüldü: %0,044–0,049 (B-16) |
| 13 | **Saat kayması/sapması (clock offset & drift)** — kodda tek küresel saat var; "senkron değil" yalnızca disiplinle sağlanıyor, yapısal değil | Gelecekte bir başlık alanı zaman damgası taşırsa **bedava kusursuz senkron** doğar | `kosucu.py:166` (B-17) |
| 14 | **Sanal taşıyıcı dinleme (NAV / süre alanı)** — RTS/CTS ayrı madde olarak var ama 802.11 veri çerçevelerinin NAV kurması da modellenmiyor | Çakışmaları gerçeğe göre **fazla** gösterir (RTS/CTS maddesiyle aynı yön) | `mac.kanal_mesgul` yalnız fiziksel taşıyıcı dinleme |
| 15 | **S0 kontrol kolunun tabanı %100 değil** — ön-kayıt "teslim tavanı %100" diyor; ölçülen ort. 0,9935, en kötü tohum 0,8701 | Küçük etkiler taban gürültüsüyle karışabilir | 90 koşu (B-18) |
| 16 | **Gecikme metriği ortak alt küme desteklemiyor** — sonuç şeması paket bazlı teslim bilgisi taşımadığı için `03` B3'ün istediği "ortak alt küme + kesişim oranı" karşılaştırması **yapılamaz** | Aile 1'de protokoller gecikmede karşılaştırılamaz | `kosucu.sonuc()` (B-19) |

Ayrıca **Ç1 KAPSAMAZ** tablosuna eklenmeli:

> **Ç1.1/Ç1.2/Ç1.4 tek bir kâhin aktarıcıyla ölçüldü.** Ana matrisin
> 540 koşusu `en_kisa_yol` (KÂHİN) ile koşulmuştur. Ölçtüğüm: saf gözlem
> aktarıcısıyla (`gurultuden_kacan`, 60 koşu) korunum yine 60/60 tutuyor
> ama boruda kalan oranı **%0,031 → %0,531** (17 kat) çıkıyor ve dört
> düşme sebebinin dördü de **doğal olarak** tetikleniyor. Ana matriste
> `kuyruk_tasmasi`, `ttl` ve `hedef_yok` yolları **hiç koşulmamıştır**
> (540 koşuda tümü sıfır); Ç1.2'nin 4/4'ü tamamen 20 uç-durum koşusundan
> gelmektedir.

---

## 7. ANLAŞILMAYANLAR

Bu bölüm boş değil — anlamadığım bir mekanizma, denetlenmemiş bir
mekanizmadır.

1. **K-019'un "sapma gereken çift oranı" metriğinin kod karşılığını
   bulamadım.** S2 = +2 dBm seçimi ve tüm senaryo güç merdiveni bu metriğe
   dayanıyor. `topology.ulasilabilir_ciftler` "ulaşılabilir çift"i veriyor
   ama "yönlendirme kararının fark ettiği çift" tanımının nasıl
   hesaplandığını çıkaramadım (en kısa yolun karıştırıcı bölgesinden geçip
   geçmediği mi? bağ PER eşiği mi? hangi eşik?). **Denetleyemedim.** → B-08

2. **Ç1.2'nin uç durum matrisinde `UC_DURUMLAR` sözlüğü çağrı sırasında
   `ek.pop("senaryo", "S2")` ile *kalıcı olarak* değiştiriliyor**
   (`kapi_korunum.py:83`). Tek çağrıda sorun yok; ama
   `uc_durum_matrisi()` iki kez çağrılırsa `denemesiz` durumu ikinci
   seferde S2 yerine varsayılan senaryoyla koşar. Bunun bilinçli mi yoksa
   fark edilmemiş mi olduğunu belirleyemedim; bugün tetiklenmiyor.

3. **S2/seyrek/tohum=30'un neden tam %0 teslim verdiğini kısmen anladım**
   (`en_kisa_yol` bağ kalitesine kör, 4 akışın hepsi karıştırıcının zehirli
   bölgesinden geçiyor; 7835 iletimin 6699'u başarısız alım) — ama 4/4
   akışın **hepsinin** tamamen ölmesinin tesadüf mü yoksa topolojik bir
   özellik mi olduğunu ayırt edemedim. Tek tohumluk bir gözlem olduğu için
   genellemedim.

4. **`_bekleyeni_kostur` ile `_uyandir` arasındaki öncelik sırasını tam
   çözemedim.** `_onay_geldi` önce `gonderim_bitti` (→ `_uyandir`, MAC'i
   yeniden meşgul edebilir) sonra `_bekleyeni_kostur` çağırıyor; bu sırada
   bekleyen beacon veri trafiğine karşı sistematik olarak açlığa düşebilir.
   `beacon_kacirilan` sayacı S0'da 0 çıktı, yoğun trafikte ölçmedim.
   **Denetlemedim.**

5. **Kanal diliminin MAC slotunun tam katı olmasının (100 µs / 20 µs = 5)
   bir sonucu olup olmadığını belirleyemedim.** Geri çekilme slot
   cinsinden çekiliyor, dolayısıyla iletim başlangıçları dilim sınırlarına
   göre düzgün dağılmayabilir. Çekim dağılımının düzgünlüğünü sınamadım.

6. **`hedefe_en_yakin` aktarıcısındaki `min(sorted(adaylar, key=…), key=…)`
   deseninin** (`aktaricilar.py:109`) neden iki kademeli olduğunu anladım
   (belirlenimci berabere bozma) ama `gurultuden_kacan`'da aynı desenin
   `bildirdigi_gurultu_w` üzerinde kullanılmasının, kayan nokta eşitliği
   nedeniyle beraberlik yaratıp yaratmadığını ölçmedim.

7. **Bu denetim tek bir makinede, tek Python sürümünde yapıldı.** Kapsam
   beyanı bunu zaten kabul ediyor; ben de aşamadım.

---

## 8. KOŞTURDUĞUM KOMUTLAR

Depoda çalıştırılanlar:

```bash
python -m pytest tests -q --tb=short -p no:cacheprovider
#  → 198 passed in 142.58s

python dogrulama/aile0_kapi_raporu.py
#  → 13/13 kriter geçti, 9.2 dk (§2-A tablosu)

python dogrulama/li_zincir.py
#  → 0.85R: plato 1/6.30, 4 atlama 1/3.87, tek atlama 931.9 kbps
#  → 1.00R: plato 1/12.61
#  → (elle yazılmış "1/6.0 · 1/12 · 1/3.6 · %16" satırları → B-12)
```

Geçici dizinde yazdığım denetim betikleri (`…\scratchpad\`):

| betik | ne ölçtü | özet çıktı |
|---|---|---|
| `b_fizik.py` | B grubu fizik sayıları, formülden bağımsız | §2-B tablosu; hepsi tuttu |
| `kahin_bayt2.py` | `Gozlem` bayt alanları düğüme mi ağa mı ait | 7343/7344 kararda ağ geneli → **B-01** |
| `kahin_sizinti.py` | bayt sayacından "karıştırıcı açık mı" çıkarımı | %53,7 doğruluk (zayıf sızıntı) |
| `eslestirme.py` | iki kol aynı senaryoyu mu görüyor + t=0 durumları | §2-D, §2-E; temiz |
| `bagimsiz_korunum.py` | korunum, **paket nesnesi sayarak** + ölü kontroller | §2-C tam uyum; 2 ölü kontrol → **B-13** |
| `ortusme_s5.py` | S5 dilim farkı, 4 farklı yörünge periyodunda, 30 tohum | 0,0089 (hizalı) vs 0,060–0,097 → **B-03** |
| `ortusme_faz.py` | topoloji sabit, yalnız faz taranarak varyans | std 0,00256 vs 0,00846 → **B-03** |
| `kendi_mutasyonlarim.py` | 10 bağımsız mutasyon × 198 test | 8'i yakalanmadı → **B-04** |
| `ikinci_kaynak.py` | görev çevrimi değişince H1.3 kırılıyor mu | 0,25'te −3,010 dB → **B-07** |
| `c_kurulum.py` + `derece_onyargisi.py` | bağlantı oranı / deneme / derece kayması, 200 000 çekim | %82,93 · 1,2058 · **−%0,362** → **B-08** |
| `rezonans.py` | beacon faz kilitlenmesi | etki yok → §2-G temiz |
| `alici_kilidi.py` | çakışan iki çerçevenin ikisi de başarılı mı | 51–59 olay (%0,05) → **B-16** |
| `matris_kirilim.py` | 540 koşunun senaryo bazlı kırılımı | §B-18, B-19, B-11 tabloları |
| `kahin_disi_matris.py` | Ç1 kriterleri kâhin olmayan aktarıcıyla | boru %0,031 → %0,531 → §6 |

**Depoda hiçbir dosya değiştirilmedi; hiçbir git komutu çalıştırılmadı.**

---

## KAPANIŞ NOTU

Bu araç ciddi. Korunum defteri nesne düzeyinde dürüst, fizik kapalı formla
birebir, eşleştirme gerçekten eşleştirme, başlangıç koşullarının hepsi
açıkça sorulmuş, ve K-024/K-029/K-033 kayıtları — kendi hatasını ölçüp
yazan kayıtlar — bu projenin en güçlü tarafı. **13/13'ün 13'ü gerçekten
geçiyor.**

Ama 13 kriterin hiçbiri şunları göremiyor: gözlem penceresinden sızan ağ
geneli sayaç, tersine çevrilebilen bir sözleşme alanı, ısınmaya taşan bir
ölçüm penceresi, anlamsızlaştırılabilen bir kapı eşiği, ve bir kapının
susması için değiştirilmiş bir fiziksel parametre. **Kapıların geçmesi,
kapıların doğru şeyleri ölçtüğünü göstermiyor** — K-033'ün kendi dersi
buydu ve o ders yalnızca kapı raporuna uygulandı, kapıların **kendisine**
uygulanmadı.

Kapanış için asgari koşul olarak şunu öneriyorum: **B-01, B-02, B-03 ve
B-04** kapatılsın (B-01/B-02 gözlem penceresi sonradan daraltılamayacağı
için **şimdi**), **B-05 ile B-10** arası düzeltilsin ve kayda geçsin, geri
kalanlar `08-AILE0-KAPSAM.md`'ye madde olarak eklensin. `03` kural 10:
*"Bir bulguyu 'düşük öncelik' deyip düzeltmeden bırakma."*

---

# İKİNCİ DENETİM — 20 Ağustos 2026

| | |
|---|---|
| **Denetçi** | Bağımsız doğrulama denetçisi (ikinci, sıfır bağlamlı oturum) |
| **Denetlenen** | Aile 0'ın **ikinci** kapanışı (K-043) + 23 bulgunun kapatıldığı iddiası |
| **Depo** | `C:\Users\Xelma123\Desktop\desparete_pls` — **hiçbir dosyası değiştirilmedi** |
| **Ortam** | Windows 11 · Python 3.11.8 · numpy 1.26.4 · scipy 1.17.1 · pytest 8.2.2 · en fazla 8 çekirdek |
| **Git** | Hiçbir git komutu çalıştırılmadı |
| **Tohumlar** | Yalnızca 1–30 ayarlama kümesi + betiklerin kendi sabit tohumları. **2000–2029 hiçbir amaçla koşulmadı** |
| **Yazılan tek dosya** | `aile0_audit.md` |

Bütün deneme betikleri geçici dizinde (`…\scratchpad\den2\`) tutuldu;
mutasyonlar `tempfile.mkdtemp` kopyalarına uygulandı.

---

## 0. YÖNETİCİ ÖZETİ

> ### Kapanış geçerli mi: **KOŞULLU**

Yeniden ürettiğim her kapı sayısı **tuttu** — 540/540 korunum, %0,156, 30/30
mutasyon, 44/14/6/6/2 test sayıları, Li platosu 1/6,29 · GA %2,04, S0 tavanı
0,9938 [0,8996 · 1,0000] 21/90, alıcı kilidi %0,028, kontrol yükü %2,84/%5,12,
gecikme yanlılığı 1,52 kat, derece kayması −%0,364 ± 0,026. Korunum defterini
**defteri hiç çağırmadan, paket nesnesi sayarak** dört yapılandırmada
doğruladım; dördünde de birebir tuttu. Bu araç gerçekten sağlam.

**Ama kapanışın kendisi hakkında üç şey doğru değil:**

1. **Örüntü kapanmadı, yalnızca fark edilen örnekleri kapandı.** Birinci
   denetimin 10 bağımsız mutasyonundan 8'i 198 testten sağ çıkmıştı. Bugün
   yazdığım **10 yeni bağımsız mutasyonun 7'si 240 testten sağ çıktı** — ve
   dördünün davranışı fiilen değiştirdiğini ayrıca ölçtüm. Test sayısı 198→240
   arttı, kör nokta yer değiştirdi. **(B-27, §5)**
2. **Kapanış beyanının kendi sayıları bayat.** Birincil çalışma noktasını
   (S2 = +2 dBm) gerekçelendiren tablo dört belgede duruyor ve üretici komut
   bugün başka sayı veriyor (0,5234 → **0,5252**); kör tarama skoru %47,8
   **185 mutantlık bir havuzdan ve 220 testlik bir tabandan** üretilmiş, bugün
   havuz 192, taban 240. **(B-25, B-28)**
3. **"Araç ne koşturduğunu kendisi doğrular" (Y7) iddiası iki yeni araçta
   tutmuyor.** `sag_kalan_ayikla.py` bugün koşturulduğunda bir *araç hatasını*
   "korumasız kod yolu" diye raporluyor; `sim/karsilastirma.py` iki kolun
   **tek bir ortak paketi bile olmadığı hâlde** karşılaştırmayı kabul ediyor.
   **(B-24, B-26)**

Buna Aile 1'i doğrudan engelleyen iki şey ekleniyor: H1.1'in ön-kayıtlı
**mekanizma kapısı bu şemayla ölçülemiyor** (B-30) ve şema "Aile 1 başlamadan
düzeltilir" kuralı altında donmuş sayılıyor.

**Kapanış iptal edilmeli mi: hayır.** 13 kriter gerçekten geçiyor ve kriterlerin
neyi ölçtüğü bu kez büyük ölçüde denetlenmiş. Ama kapanış metninin
*"örüntü kırıldı"* ve *"şema Aile 1'e hazır"* iddiaları **düzeltilmeli**, ve
aşağıdaki 17 bulgu Aile 1'in ilk koşusundan önce kapatılmalıdır.

---

## 1. YENİ BULGULAR

Ciddiyet: 🔴 kritik · 🟠 orta · ⚪ düşük.

---

### 🔴 B-24 · `sag_kalan_ayikla.py` bayat — bir ARAÇ HATASINI "korumasız kod yolu" diye raporluyor

**Nerede:** `dogrulama/sag_kalan_ayikla.py:88–94` (S02 girdisi) ↔ `sim/mac.py:588–601`

**İddia (K-038):** *"12 sağ kalan mutant ölçümle ayıklandı: 4'ü davranışı
gerçekten değiştiriyor, 8'i bu matriste eşdeğer."*

**ÖLÇTÜĞÜM** — Aracı bugün koşturdum:

```
🔴 DAVRANIŞI DEĞİŞTİREN : 5
⚪ bu matriste eşdeğer  : 7
     S02_alim_basarisiz_yerine_basarili   ← YENİ, ve GERÇEK DEĞİL
     S04 · S05 · S07 · S08
```

Beşincisinin sebebi kod değil, aracın kendisi:

```
⚠️ HATA     S02_alim_basarisiz_yerine_basarili
    detay : RuntimeError('mutasyon uygulanamadı: S02_alim_basarisiz_yerine_basarili')
```

S02'nin hedef aldığı `if per is None: return False` satırı **aynı oturumda**
(K-038, B-13 kapanışı) `assert per is not None`'a çevrildi. Mutasyon deseni
artık dosyada yok. `_kosu` istisnayı `durum="hata"` yapıyor, `main()` ise
`hata` ve `cokme` durumlarını **`degisen` listesine ekliyor** ve altına şunu
basıyor: *"Bunların her biri, hiçbir testin görmediği bir davranış
değişikliğidir — yani korumasız bir kod yolu."*

Yani araç, **kendi girdisinin bayatlığını korumasız kod yolu olarak
raporluyor.** Bu, Y7'nin ihlali ve bu depoda yedinci örneği.

**Ek:** 12 girdinin **10'unun satır numarası** da bayat *(mac.py:271 → gerçek
285, mac.py:435 → 451, config.py:294 → 325, results.py:85 → o satırdaki desen
artık yok)*. Satır numaraları çıktının içinde delil olarak basılıyor.

**Üretici:** `python dogrulama/sag_kalan_ayikla.py` *(6,5 dk)*
`python -c "…from dogrulama.sag_kalan_ayikla import SAG_KALANLAR…"` *(desen/satır kontrolü)*

**Neden önemli** — K-038'in tüm değeri *"yargı veriden çıkmalı"* idi. Veriden
çıkan yargı bugün yanlış: 5 diyor, 4 olmalı, ve fazladan olanın sebebi ölçüm
değil bakım eksikliği. Bir sonraki okuyucu bu çıktıyı yeni bir bulgu sanır.

**Öneri** — `_kopya`nın `RuntimeError`'ı ayrı bir `ARAÇ HATASI` kovasına
düşsün, `degisen`e **girmesin** ve kapıyı *"bulgu"* değil *"araç bakımı"*
olarak düşürsün. Satır numaraları ya üretimden alınsın ya kaldırılsın.

---

### 🔴 B-25 · Kör tarama skoru (%47,8) hem havuzu hem test paketi değişmiş bir kod durumundan — ve `08` bunu söylemiyor

**Nerede:** `kor_cikti.txt` ↔ `dogrulama/kor_mutasyon.py` ↔ `v2/08-AILE0-KAPSAM.md`

**İddia:** `08-AILE0-KAPSAM.md`: *"`kor_mutasyon.py` **185 mutant** üretiyor ve
bir koşuda **24'ünü** örnekliyor… **161 mutant hiç sınanmadı**… skor **%47,8
(11/23)**, 12 sağ kalan."* K-043 kapanış tablosu aynı sayıyı koşulsuz veriyor.

**ÖLÇTÜĞÜM**

| | kayıtta *(`kor_cikti.txt`)* | bugün |
|---|---|---|
| mutant havuzu | **185** | **192** |
| taban test paketi | **220 passed** | **240 passed** |
| aynı tohumla seçilen 24'lük örneklem | — | **24'ün yalnızca 1'i ortak** *(`packet.py:51`)* |

`random.Random(20260819).sample(havuz, 24)` havuzun **uzunluğuna ve sırasına**
bağlıdır; havuz 185 → 192 olunca örneklem tamamen değişti. Yani
`python dogrulama/kor_mutasyon.py 24` — beyan edilen üretici komut — o sayıyı
**bir daha üretmez.**

Dahası: skor bir **test paketi özelliğidir** ve o ölçüm 220 testlik bir paketle
yapıldı. K-039/K-040/K-041 sonrasında paket 240 test. Bu hiçbir belgede yazmıyor.

**Üretici:**
```
python -c "import sys;sys.path.insert(0,'.');from dogrulama.kor_mutasyon import mutantlari_uret;print(len(mutantlari_uret()))"   # 192
python -m pytest tests -q                                                                                                        # 240 passed
head -13 kor_cikti.txt                                                                                                           # 185 / 220 passed
```

**Neden önemli** — `09-DEVIR-TESLIM.md:167` havuz değişimini **kabul ediyor**
(*"Skor yanlış değil, ama güncel değil"*). Ama kapanışın kendi cümlesi şu:
*"🔴 Bu belge (`08`) okunmadan 'Aile 0 geçti' denemez."* `08` okuyan biri
185/161/%47,8'i güncel bir özellik olarak alır. İki belge çelişiyor ve
çelişkinin yanlış tarafı, kapanışın zorunlu belgesi.

**Öneri** — `08`'deki üç sayıyı düzelt ve kayıt notunu oraya taşı; skoru
*"20 test daha eklenmeden önceki kod durumunda ölçüldü"* diye tarihle.

---

### 🔴 B-26 · `sim/karsilastirma.py`'nin Y7 koruması iddia ettiği şeyi doğrulamıyor: hiç ortak paketi olmayan iki kol karşılaştırılabiliyor

**Nerede:** `sim/karsilastirma.py:118–135` (`ortak_alt_kume` girdi kontrolü)

**İddia (kod yorumu + K-041):** *"🔴 Y7 — ARAÇ NE KARŞILAŞTIRDIĞINI KENDİSİ
DOĞRULAR. İki sonucun aynı paket evreninden gelmesi ZORUNLUDUR; gelmiyorsa
… `KarsilastirmaHatasi` fırlatılır."*

**ÖLÇTÜĞÜM** — Aynı tohum, aynı trafik; tek fark `dugum_sayisi` 40 → 41:

| | A *(40 düğüm)* | B *(41 düğüm)* |
|---|---|---|
| üretilen paket | 3198 | 3198 |
| `pencerede_uretilen` | 2698 | 2698 |
| `pencere_kimlik_araligi` | [500, 3197] | [500, 3197] |
| aynı `dogum_s` taşıyan paket | — | **3198 / 3198** |
| **aynı `(kaynak, hedef)` taşıyan paket** | — | **0 / 3198** |

Yani **hiçbir kimlik aynı paketi göstermiyor** — ve araç karşılaştırmayı kabul
etti:

```
>>> GUARD KABUL ETTI: ortak 509 paket (kesişim %28.2 birleşim, %18.9 pencere)
                      gecikme A=66.77 ms B=98.33 ms
```

Aynı şey `iletim_menzili_m` 280→300 ve `alan_m` 1000→1010 için de oldu
*(o ikisinde çiftler tesadüfen aynı kaldı, ama koruma yine hiçbir şey
doğrulamadı)*.

**MEKANİZMA** — Koruma yalnızca iki şeye bakıyor: `pencerede_uretilen` ve
`pencere_kimlik_araligi`. İkisi de **yalnızca `trafik_zamani` akışından**
belirlenir; tohum dışında hiçbir konfigürasyon farkı bu ikisini değiştiremez.
Test edilen tek pozitif vaka (`test_b19_farkli_paket_evreni_reddediliyor`) de
tam olarak tohum farkını kullanıyor — yani koruma **yalnızca yakalayabildiği
tek durumla** sınanmış.

🔴 **Ve şema bu kontrolü mümkün kılmıyor:** sonuç sözlüğünde paket evrenini
tanımlayan hiçbir alan yok (`teslim_kimlikleri` yalnızca teslim edilenleri
taşır). `test_b19_paket_evreni_protokolden_bagimsiz` varsayımı doğrulamak için
`k.trafik.uretilen_paketler`e — yani **simülatör nesnesine** — bakıyor; kayıtlı
bir sonuç satırında o bilgi yok.

**Üretici:** yukarıdaki tablo, `sim.karsilastirma.ortak_alt_kume` üç ayrı
konfigürasyon çiftiyle çağrılarak *(scratchpad betiği)*.

**Neden önemli** — B-19 bu dosya için yazıldı ve `08`in 16. maddesi
*"her gecikme karşılaştırması `sim/karsilastirma.py` üzerinden"* diyor.
Aile 1'de S0↔S2, farklı protokol, farklı trafik kolları karşılaştırılacak;
koruma ilk gerçek yanlış kullanımı **sessizce geçirir**.

**Öneri** — Sonuç sözlüğüne paket evreni parmak izi ekle *(ör.
`blake2b((kimlik, dogum_s, kaynak, hedef) demetleri)` → `pencere_evren_hash`)*
ve `ortak_alt_kume` onu karşılaştırsın. `03` B5 ve K-041'in kendi kuralı
gereği bu **Aile 1 başlamadan** yapılmalı; sonra yapılırsa tüm önceki satırlar
karşılaştırılamaz olur.

---

### 🔴 B-27 · 10 bağımsız mutasyonun 7'si 240 testten sağ çıktı — B-04'ün örüntüsü kapanmadı

**Nerede:** test paketi geneli. Ayrıntı §5.

**İddia (K-043 kapanış tablosu):** *18 Ağustos'ta 198 test, 7 mutasyon
"seçim yanlılığıyla"; 19 Ağustos'ta 240 test, 30 mutasyon her biri kendi
testiyle.* B-04'ün kapanışı `tests/test_denetim_boslukları.py` ile ilan edildi.

**ÖLÇTÜĞÜM** — Depoyu hiç görmemiş bir gözle 10 yeni mutasyon yazdım ve her
birini **tam 240 testlik paketle** koşturdum: **7'si sağ çıktı.**
Sonra sağ kalanların davranışı gerçekten değiştirip değiştirmediğini
44/13/12 koşuluk matrislerde ölçtüm *(K-038'in ölçütü)*: **dördü fiilen
değiştiriyor**, üçü ise değiştirmiyor çünkü **o alanın hiçbir tüketicisi yok**
— ki asıl bulgu odur (B-27b).

| mutasyon | sonuç | davranış |
|---|---|---|
| `kesisim_orani_pencere` → 1.0 | sağ kaldı | 🔴 değişti *(rapora giren metrik)* |
| `komsu_omru_katsayisi` 10 → 1000 | sağ kaldı | 🔴 değişti *(12 koşunun 8'i; teslim ±0,10'a kadar)* |
| hareketli karıştırıcı yörünge **yönü** ters | sağ kaldı | 🔴 değişti *(S5 koşularının hepsi)* |
| yeniden deneme sınırı bir eksik *(5→4 iletim)* | sağ kaldı | 🔴 değişti *(13/13 koşu)* |
| `kanal_cekimi` alıcıya duyarsız | sağ kaldı | 🔴 değişti *(13/13 koşu)* |
| `kanal_mesgul_mu` → `False` | sağ kaldı | ⚪ tüketicisi yok → **B-27b** |
| `kuyruk_uzunlugu` → `0` | sağ kaldı | ⚪ tüketicisi yok → **B-27b** |
| ölçülen gürültü karıştırıcıyı görmüyor | yakalandı | — |
| CBR titreşimi tek yönlü | yakalandı *(ilgisiz testle)* | — |
| kuyruk FIFO → LIFO | yakalandı *(ilgisiz testlerle)* | — |

**Üretici:** `scratchpad/den2/kendi_mutasyonlarim.py` *(10,9 dk)* ·
`scratchpad/den2/etki_olc.py` · `scratchpad/den2/etki2.py`

**Neden önemli** — 42 yeni test ve 23 düzeltme, denetçinin **adını verdiği**
yolları kapattı. Yeni bir bağımsız örneklem hâlâ %70 sağ kalan veriyor.
Bu bir kusur değil, bir **ölçüdür**: kapanış *"test paketi artık koruyor"*
diyemez; *"denetimin bulduğu 10 yolu koruyor"* diyebilir.

---

### 🔴 B-27b · Gözlem penceresinin dört alanının ne tüketicisi ne içerik testi var

**Nerede:** `sim/gozlem.py` (`IZINLI_GOZLEM_ALANLARI`) ↔ `tests/test_gozlem.py` ↔ `dogrulama/aktaricilar.py`

**ÖLÇTÜĞÜM** — `Gozlem`in 12 alanı için "bir test içeriğini iddia ediyor mu"
ve "bir aktarıcı okuyor mu" taraması:

| alan | içerik testi | tüketici |
|---|---|---|
| `saat_s` | ❌ | ❌ |
| `kanal_mesgul_mu` | ❌ | ❌ |
| `kuyruk_uzunlugu` | ❌ | ❌ |
| `kuyruk_kapasitesi` | ❌ | ❌ |
| `olculen_gurultu_w` | ⚠️ dolaylı *(beacon içeriği üzerinden, `test_d10b`)* | ❌ |
| `gonderilen_bayt` · `alinan_bayt` | ✅ *(B-01)* | ❌ |
| `son_iletim_sonucu` · `son_iletim_hedefi` | ✅ *(B-02)* | ❌ |
| `komsular` · `paket` · `dugum` | ✅ | ✅ |

Doğrulama: `kanal_mesgul_mu`u sabit `False`, `kuyruk_uzunlugu`u sabit `0`
yapan mutasyonlar **240/240 test geçiyor**; gözlemi kullanan iki aktarıcıyla
12 koşuluk matriste de fark üretmiyorlar — çünkü **kimse okumuyor**.

Y8 gereği doğru okuma budur: *"eşdeğer"* değil, **"tüketicisiz"**. Alan
karar anında 7 342 kez üretiliyor *(S2/orta/tohum 1)*; `kanal_mesgul_mu`
bunların 1 417'sinde `True`, yani üretim yolu tetikleniyor — tüketim yolu yok.

**Neden önemli** — Bu, `03` B5'in *"bildirim ≠ kullanım"* tuzağının gözlem
sözleşmesindeki hâli. Proje bu tuzağa karşı iki koruma yazdı
(`UYGULANMAMIS_BAYRAKLAR` / `HENUZ_KULLANILMAYAN`) ama **gözlem penceresine
uygulamadı.** Aile 1'in ilk protokolü `kanal_mesgul_mu`yu okuduğunda, o alanın
doğru değeri taşıdığını gösteren hiçbir kayıt olmayacak.

**Öneri** — B-06/B-10 deseninin üçüncüsü: her `Gozlem` alanı **ya** değerinin
gerçek büyüklüğe eşit olduğunu gösteren bir teste bağlanır, **ya**
`gozlem.HENUZ_TUKETILMEYEN` gibi bir listede açıkça beyan edilir.

---

### 🔴 B-28 · S2 = +2 dBm'i gerekçelendiren sayılar dört belgede bayat; üretici komut bugün başka sayı veriyor

**Nerede:** `sim/config.py:60–64` · `v2/06-ON-KAYIT.md:131–136` ·
`v2/09-DEVIR-TESLIM.md:158` · `04-NEDEN-BOYLE.md` K-039

**İddia:** *"dinamik aralık [0,1198 · 0,8975] → orta **0,5087**; +2 dBm →
**0,5234**, ortadan 0,0147 uzakta ⇒ SEÇİLEN."*
**Üretici:** `python dogrulama/kurulum_kalibrasyonu.py`

**ÖLÇTÜĞÜM** — Aynı komut, aynı tohumlar *(1, 7, 13, 19, 23)*, belirlenimci:

| | mühürlü | bugün |
|---|---|---|
| +2 dBm teslim | 0,5234 | **0,5252** |
| dinamik aralık | [0,1198 · 0,8975] | **[0,1197 · 0,8955]** |
| orta | 0,5087 | **0,5076** |
| ortadan uzaklık | 0,0147 | **0,0176** |
| seçilen güç | +2 dBm | **+2 dBm** ✅ |

Tekrar koştum, birebir aynı çıktı — belirlenimsizlik değil, **kod durumu
farkı**. Bölüm B'nin graf tablosu *(97,0 ± 0,9 / 44,2 ± 1,5 …)* **birebir
tutuyor**, çünkü o yalnızca topolojiden hesaplanıyor; kayan tek şey uçtan uca
teslim. Sebep K-040'ın `beacon_faz` akışı: RNG çekim sırası kaydı. K-041
bu yüzden B-16 ve B-18'i yeniden ölçtü — **kalibrasyonu yeniden ölçmedi.**

**Üretici:** `python dogrulama/kurulum_kalibrasyonu.py` *(Bölüm A+B+C)*

**Neden önemli** — Sonuç değişmiyor (+2 dBm hâlâ seçiliyor), ama kural 1
ihlal ediliyor: *"her sayının yanında üretici komut yazılır"* — komut yazılı ve
**o sayıyı üretmiyor.** Bu, bu oturumda üçüncü *"araç doğru, çıktısı bayat"*
vakası; ilk ikisi (Ç1.3'ün 17/17'si ve Ç5'in 11'i) kapanışın en gururlu
bulguları.

---

### 🟠 B-29 · Yeni seçim ölçütünün *"ulaşılabilirlik ≥ %90"* kısıtı koda hiç girmemiş

**Nerede:** `dogrulama/kurulum_kalibrasyonu.py:373–383` (`yeni_olcut`) ·
`tests/test_kalibrasyon.py`

**İddia (K-039, koda yazıldığı iddiasıyla):** *"🔒 YENİ SEÇİM ÖLÇÜTÜ …
dinamik aralığın ortasına en yakın getiren güçtür; **ulaşılabilirlik (MAC
sonrası bağ tanımı) ≥ %90 kısıtı altında.** … **Uygulandığında (kod, proza
değil)**."*

**ÖLÇTÜĞÜM** — `yeni_olcut(egri)` yalnızca `(güç, teslim)` çiftleri alıyor;
ulaşılabilirlik **argüman olarak bile geçmiyor**:

```
yeni_olcut([(-10, 0.90), (0, 0.70), (6, 0.51), (11, 0.12)])  ->  (6.0, 0.51)
```

+6 dBm'in ölçülen ulaşılabilirliği **%84,8** — ilan edilen kısıtın altında,
ve ölçüt onu seçiyor. `bolum_c` de kısıtı hiçbir yerde uygulamıyor.
`tests/test_kalibrasyon.py`'nin 7 testinden hiçbiri bunu sormuyor; **eski**
ölçüt için soruyor (`test_eski_olcut_ulasilabilirlik_tabanina_uyuyor`).

**Üretici:** `python -c "from dogrulama.kurulum_kalibrasyonu import yeni_olcut; …"`

**Neden önemli** — Bugün bağlayıcı değil (S2'de ulaşılabilirlik %97,0). Ama
K-039'un *"BUNU NE DEĞİŞTİRİR"* satırı zaten yazıyor: radyo modeli, menzil
tanımı veya deneme sınırı değişirse tablo değişir ve betik yeniden koşulur.
O gün ölçüt, kısıtı sormadan bir nokta seçecek.

**⚖️ Ölçütün savunulabilirliği — ayrıca sınadım (şüphe #8).** Ölçütü zayıflatmak
için üç eksende zorladım; **üçünde de +2 dBm seçiliyor:**

| zorlama | sonuç |
|---|---|
| Taramayı iki yönde genişlet *(−16, −13, +14, +17 dBm ölçüldü: 0,8966 · 0,8967 · 0,0984 · 0,0800)* | taban 0,08'e insin, tavan 0,897'de doysun → orta 0,489; +2 (0,525) hâlâ en yakın. Taban **0'a** inse bile +2 kazanır |
| Kâhin olmayan yarı-gözlemsel aktarıcı `hedefe_en_yakin` *(3 tohum, 11 güç)* | aralık [0,0665 · 0,6932], orta 0,3798 → **+2 dBm** *(teslim 0,3836)* |
| `en_kisa_yol`, 3 tohum | aralık [0,0994 · 0,8621], orta 0,4807 → **+2 dBm** |

Yani ölçüt *"mevcut cevabı korumak için seçilmiş"* bir ölçüt gibi
davranmıyor — makul her varyantı aynı noktayı seçiyor. **Kusur ölçütün
kendisinde değil, kısıtın yarısının prozada kalmasında.**

---

### 🔴 B-30 · H1.1'in ön-kayıtlı mekanizma kapısı bu şemayla ÖLÇÜLEMİYOR

**Nerede:** `v2/06-ON-KAYIT.md` H1.1 ↔ `sim/kosucu.py::Kosu.sonuc`

**İddia (ön-kayıt):** *"🔴 Bu yüzden mekanizma kontrolü … **"seçilen rotalarda
ara bölge bağı (0,05 ≤ PER ≤ 0,9) kaç kez kullanıldı"** olacak. Bu sayaç
düşmüyorsa, teslimdeki fark başka bir sebepten geliyor demektir ve **sonuca
bakılmaz.**"*

**ÖLÇTÜĞÜM** — Sonuç sözlüğünde **34 anahtar** var; böyle bir sayaç yok:

```
beacon_alinan, beacon_gonderilen, beacon_kacirilan, boruda_kalan, donguyle_olen,
en_yuksek_doluluk, hedef_yok, islenen_olay, kontrol_airtime_s, kontrol_bayt,
kuyruk_tasmasi, mac_basarisiz_alim, mac_deneme, mac_dusurmesi, mac_gonderilen,
mac_kayip_onay, mac_kopya_alim, mac_onay, ort_komsu_sayisi, ortalama_atlama,
ortalama_gecikme_s, ortanca_gecikme_s, pencere_kimlik_araligi, pencerede_teslim,
pencerede_uretilen, teslim_gecikmeleri_s, teslim_kimlikleri, teslim_orani,
topoloji, trafik, ttl_olumu, veri_airtime_s, veri_bayt, yakinsama
```

`05-GOZLEM-PENCERESI.md` §D'nin **beş teşhis sayacının** *(karar anında
kullanılan bilginin yaşı · kaydın olmadığı karar oranı · yalnızca başarılardan
öğrenilen karar oranı · gerçek kalitesi kötü bağdan geçen karar oranı ·
protokolün kendi kestirimi)* hiçbiri de yok.

**Ek ölçüm — kapının paydası da üretilemiyor.** K-020 *"133 bağın yalnızca
11–17'si ara bölgede"* diyor ve **üretici komutu yok**. Ön-kaydın ilan ettiği
bantla (0,05 ≤ PER ≤ 0,9) yeniden ürettim:

| tohum | menzil içi bağ | ara bölge *(0,05–0,9)* |
|---|---|---|
| 1 | **133** ✅ | **6** |
| 2 | 165 | 7 |
| 3 | 147 | 12 |
| 4 | 151 | 14 |
| 5 | 128 | 8 |

10 tohumda 6–14. Bandı [0,01 · 0,99] alırsam 11–26 çıkıyor — yani "11–17"
**başka bir bantla** ölçülmüş ve bant yazılmamış. K-020'nin geri kalanı
birebir tutuyor *(0,85R→%0,03 · 1,00R→%16,97 · 1,05R→%51,60 · 1,20R→%100;
PER %1→%99 geçişi **2,79 dB**, iddia 2,8 dB)*.

**Üretici:** sonuç anahtarları — `Kosu(...).kostur().keys()`;
bağ sayımı — `Topoloji.uret` + `Radyo.paket_hata_olasiligi`, tohum 1–10.

**Neden önemli** — K-041 ve `03` B5 şemayı Aile 1 başlamadan dondurmayı
zorunlu kılıyor *(B-19'un kendi dersi)*. Kapanış *"sıradaki aile: Aile 1"*
diyor. Aile 1 koşulduktan sonra bu sayacı eklemek, o güne kadarki tüm
satırları karşılaştırılamaz yapar — ve sayaç olmadan H1.1'in kendi kuralı
gereği **sonuca bakılamaz**.

**Öneri** — Mekanizma sayacını (ve kararın kullandığı bağın gerçek PER'ini)
şemaya **şimdi** ekle; bandı ön-kayıtta tek bir yerde tanımla ve K-020'nin
"11–17"sini o bantla yeniden ölç ya da revizyonla düzelt.

---

### 🟠 B-31 · İstatistik planının (`06` Bölüm 3) hiçbir kod karşılığı yok; *"zorunlu"* denen NaN kontrolü ve regresyon testi yazılmamış

**Nerede:** `v2/06-ON-KAYIT.md` Bölüm 3 ↔ depo geneli

**İddia:** *"Test: Wilcoxon işaretli sıra, çift yönlü · Düzeltme:
Holm–Bonferroni · Güç analizi mühürde yapılır"* ve
*"**Zorunlu:** test çağrılmadan önce farkların tümünün sıfır olup olmadığı
açıkça kontrol edilir; regresyon testi **gerçek örneklem boyutuyla** yazılır."*

**ÖLÇTÜĞÜM**

```
grep -rn "wilcoxon\|holm\|Holm\|scipy" --include=*.py .   →   HİÇBİR EŞLEŞME
```

Depoda istatistik katmanı yok; `scipy` kurulu ama hiçbir dosyada import
edilmiyor. NaN tuzağına karşı ne bir kontrol ne bir test var.

**Neden önemli** — Bunun Aile 0 kapsamında olmaması savunulabilir. Sorun şu:
`08-AILE0-KAPSAM.md`'nin **hiçbir KAPSAMAZ tablosunda** *"istatistik katmanı
yazılmadı"* maddesi yok. Kapanış, eksik olduğunu beyan etmediği bir şeyi
eksik bırakıyor — ki `08`in var oluş sebebi tam olarak budur.
Ayrıca ön-kayıt *"güç analizi mühürde yapılır"* diyor ve mühür **26 Eylül**;
NaN tuzağı belgede iki kez 🔴 ile işaretlenmiş bir hata sınıfı.

**Öneri** — `08`e bir madde: *"İstatistiksel test katmanı (Wilcoxon · Holm ·
güç analizi · NaN koruması) YAZILMADI. Aile 1'in ilk sonucundan önce
yazılmalı ve NaN regresyonu gerçek örneklem boyutuyla kurulmalı."*

---

### 🟠 B-32 · Ç1.3'ün eşiği hâlâ VERİDEN türetiliyor — Ç1.1'de düzeltilen tuzağın ikizi

**Nerede:** `dogrulama/aile0_kapi_raporu.py:150–154`

**İddia (K-043, kapanış ön koşulu 4):** *"Kapı kriterlerinin kendisi
denetlendi: **Ç1.1 boş kümede geçiyordu (`0 == 0`), eşiği veriden
türetiliyordu** — beklenen koşu sayısı **540** sabit yazıldı."*

**ÖLÇTÜĞÜM** — Ç1.1 düzeltildi:

```python
BEKLENEN_KOSU = 6 * 3 * 30
... tutan == len(ana) == BEKLENEN_KOSU
```

Ç1.3 düzeltilmedi:

```python
K.append(Kriter("Ç1.3", "...",
                f"{mp['yakalanan']}/{mp['toplam']}",      # ölçülen
                f"{mp['toplam']}/{mp['toplam']}",         # EŞİK — aynı veriden
                mp["gecti"]))
```

`toplam = len(MUTASYONLAR)`. Liste kazayla küçülürse *(bir düzenleme, bir
`replace` kayması, bir yorum satırı)* kapı `"N/N"` ile geçer ve rapor 30
yerine N yazar. Ç2 · Ç3 · Ç5 · Ç4.1 · Ç6.2'nin hepsinde sabit beklenen sayı
var; Ç1.3'te yok. *(Liste tamamen boşalırsa `Pool(0)` ile çöker — sessiz
değil; asıl risk kısmi küçülme.)*

**Öneri** — `BEKLENEN_MUTASYON = 30` sabiti ve `mp["toplam"] == BEKLENEN_MUTASYON`
kontrolü.

---

### ⚪ B-33 · `07-SIMULATOR-ARAYUZ.md`'nin akış tablosu `beacon_faz`'ı içermiyor

**Nerede:** `v2/07-SIMULATOR-ARAYUZ.md:152–163` ↔ `sim/rng.py::AKIS_ADLARI`

`rng.py` başlığı: *"07-SIMULATOR-ARAYUZ.md, 'RASTGELELİK AKIŞLARI' tablosu.
**Bu liste kapalıdır**: yeni bir rastgelelik kaynağı eklemek, bu listeye
eklemeyi ve NEDEN-BOYLE.md'ye kayıt düşmeyi gerektirir."*

B-10/K-040 `beacon_faz` akışını **koda** ekledi, **kayda** düştü, ama
belgedeki tabloya eklemedi. Belge hâlâ *"Yedi ayrı akış"* diyor ve altı gerçek
akış + `kanal` sayıyor; kodda yedi gerçek akış var.

Aynı belgede ikinci bayat sayı: *"Li replikasyonu **1/6,0** vs Li 1/7"*
(satır 494) — B-12'nin `li_zincir.py`den sildiği elle yazılmış sayının belge
kopyası. Güncel değer **1/6,29**.

**Üretici:** `grep -n "beacon_faz" v2/07-SIMULATOR-ARAYUZ.md` → boş.

---

### ⚪ B-34 · `08-AILE0-KAPSAM.md`'nin Ç1 KAPSAR tablosu var olmayan bir uç durum sayıyor; mutasyon sayısı bayat

**Nerede:** `v2/08-AILE0-KAPSAM.md` (Ç1 KAPSAR) ↔ `dogrulama/kapi_korunum.py::UC_DURUMLAR`

| `08` diyor ki | kodda olan |
|---|---|
| Kuyruk kapasitesi 1 | `dar_kuyruk` ✅ |
| TTL 2 | `kisa_ttl` ✅ |
| yeniden deneme 0 | `denemesiz` ✅ |
| **karıştırıcı +11 dBm *(ağ bölünmüş)*** | ❌ **yok** — dördüncüsü `rota_yok` *(ölü aktarıcı)* |

Aynı belgede: *"Kapı ölçütü `mutasyon_paketi.py`nin **28 hedefli**
mutasyonudur"* — bugün **30**, ve kapanış tablosunun kendisi 30/30 yazıyor.

---

### ⚪ B-35 · Kalan bir Y10 vakası: `test_ber_kapali_form`'un ilan ettiği `rel` bağlayıcı değil

**Nerede:** `tests/test_radio.py:108–110`

```python
for gamma in (0.5, 1.0, 5.0, 10.0, 20.0):
    assert radyo.bit_hata_orani(gamma) == pytest.approx(0.5 * math.exp(-gamma))
```

**ÖLÇTÜĞÜM** — γ = 20'de beklenen değer 1,031e−9; `approx`ın varsayılan
toleransı `max(1e-6·1,031e−9, 1e-12) = 1e−12` → **etkin göreli tolerans
9,7e−4**, yani ilan edilen `rel=1e-6`'nın **970 katı**.

| iddia | `abs` varsayılan | `abs=0.0` |
|---|---|---|
| BER %0,05 hatalı | ✅ **geçiyor** | 🔴 kırılıyor |
| BER 2 kat hatalı | 🔴 kırılıyor | 🔴 kırılıyor |

Kırılamaz değil — ama **ilan edilen hassasiyette bağlayıcı değil.** B-22 beş
vakayı düzeltti; tarama tüm `approx` çağrılarına uygulanmadı, yalnızca
denetimin adını verdiklerine.

---

### ⚪ B-36 · `sag_kalan_ayikla` kendi Y8 uyarısını basıyor ama uygulamıyor; K-038 uyarıyı hiç kaydetmemiş

**Nerede:** `dogrulama/sag_kalan_ayikla.py:296–302`

Hem kayıtlı koşuda (`ayikla_cikti.txt`) hem bugünkü koşuda tetiklenme tablosu
`donguyle_olen = 0` gösteriyor ve araç şunu basıyor:

```
!! donguyle_olen      0
⚠️ Sıfır olan bir yol için 'eşdeğer' kararı GEÇERSİZDİR.
```

…sonra 7–8 *"eşdeğer"* kararını olduğu gibi veriyor. K-038 metni
*"araç … sıfır olan bir yol için verilen 'eşdeğer' kararını **geçersiz** ilan
ediyor"* diyor — kodda böyle bir bağ yok: hangi mutasyonun hangi yola
dokunduğu hiçbir yerde yazılı değil, dolayısıyla uyarı **hiçbir kararı
geçersizleştiremez.** Kayıt bu uyarıyı hiç anmıyor.

---

### 🟠 B-37 · Kapsam beyanında olmayan dört modelleme sınırı

**Nerede:** `sim/topology.py:33` · `sim/kosucu.py:78` · `sim/queues.py` ·
`v2/08-AILE0-KAPSAM.md` 16 maddelik liste

| # | Kodda | 16 maddede | Etkinin yönü |
|---|---|---|---|
| a | **Geometri 2 boyutlu** — `konumlar: tuple[tuple[float, float], ...]`, düğümler tek düzlemde | ❌ yok | Bir **İHA** ağı için irtifa bir serbestlik derecesidir. Düzlemde, karıştırıcıya olan uzaklık yalnızca yatay; irtifa farkı bağ geometrisini ve karıştırıcının aydınlatma desenini değiştirir |
| b | **Tek karıştırıcı, varsayılan konumu alanın MERKEZİ** — `Karistirici.senaryodan` tek nesne kurar | ❌ yok | 🔴 **Modeli iyimser yapar ve tam da hipotezin lehine:** tek merkezî karıştırıcı, etrafından dolaşılabilir simetrik bir zehirli bölge üretir. Çoklu ya da kenar karıştırıcıda "kaçacak yer" kalmayabilir — H1.1'in mekanizması *(yarı ölü bağdan kaçmak)* tam olarak buna dayanıyor |
| c | **Enerji / pil kısıtı yok** | ❌ yok | `03` kural 9 SWaP kısıtını gerçek sayıyor; araç enerji maliyeti ölçmüyor. Kontrol düzlemi bütçesi yalnızca bayt ve airtime cinsinden |
| d | **Kuyruk: tek sınıf, önceliksiz FIFO** | ❌ yok | Kontrol ve veri aynı kuyruğu paylaşmıyor *(beacon ayrı yol)*, ama trafik sınıfı ayrımı yok; gecikme dağılımı disipline duyarlıdır *(FIFO→LIFO mutasyonum iki testi kırdı, yani etki büyük)* |

`08`in kendi kuralı: *"bir kapı, 'neyi KAPSAMIYOR' listesi yazılmadan
kapanmaz."* Bu dördü listede yok.

---

### ⚪ B-38 · `Karistirici.faz_s` alanı saniye değil, birimsiz kesir

**Nerede:** `sim/radio.py:264–268` ve `:255–261` ↔ `sim/radio.py:293`

`senaryodan()` alana `akislar["karistirici_faz"].random()` (∈ [0,1)) atıyor.
Kullanıldığı iki yer de **tur/periyot kesri** bekliyor:

```python
evre = ((zaman_s / self.periyot_s) + self.faz_s) % 1.0        # acik_mi
aci  = 2π * ((hiz_ms * zaman_s) / cevre + self.faz_s)         # konum_t
```

Ad `_s` soneki taşıyor. B-14 bu alanı **zorunlu** yaptı çünkü varsayılanı
(`0.0`) rezonans korumasının kapalı hâliydi — yani alan artık her çağıranın
açıkça doldurduğu bir alan. `dogrulama/kurulum_kalibrasyonu.py` ve iki test
`faz_s=0.0` geçiyor; saniye cinsinden bir değer geçen bir çağıran
(ör. `faz_s=1.35`, "yarım periyot") sessizce yanlış fazı alır *(1,35 mod 1 =
0,35)*. Bugün hata yok, gelecekte sessiz.

---

### ⚪ B-39 · Depo kökünde kayıt dışı bir üretim betiği ve dört bayat çıktı dosyası

`_x.py` — docstring'siz, kayıtsız, `04`te geçmiyor; simülatörü dört senaryo ×
üç tohumda koşup teslim oranı basıyor. Kim, ne zaman, hangi soru için
çalıştırdı yazılı değil.

Kök dizindeki çıktı dosyalarının güncelliği:

| dosya | taşıdığı kod durumu | güncel mi |
|---|---|---|
| `kapi_cikti.txt` | 13/13, 35,6 dk | ✅ kapanış koşusu |
| `mut_cikti.txt` | **26/26**, taban **224 passed** | ❌ iki sürüm eski |
| `kor_cikti.txt` | havuz **185**, taban **220 passed** | ❌ → B-25 |
| `ayikla_cikti.txt` | S02 hâlâ uygulanabilirken | ❌ → B-24 |
| `kalibrasyon_cikti.txt` · `kalibrasyon_b.txt` | K-040 öncesi | ❌ → B-28 |

Beşi de sonuç gibi görünüyor ve dördü bugünkü koddan üretilemiyor.

---

## 2. BİRİNCİ DENETİMİN BULGULARI — kapanma doğrulaması

Rastgele seçtiğim **on altı** bulguyu bağımsız olarak sınadım *(istenen alt sınır 6)*.

| # | İddia edilen kapanış | Nasıl doğruladım | Sonuç |
|---|---|---|---|
| **B-01** | `Gozlem` bayt alanları düğümün kendi sayaçları | S2/orta koşusunda 7 342 kararın hepsinde `(gonderilen, alinan)` çifti kaydedildi: **7 341 farklı çift**; düğüm başı toplam = ağ toplamı (`veri_bayt + kontrol_bayt`) **birebir**; düğüm 0 ile düğüm 5 farklı değer görüyor | ✅ **kapandı** |
| **B-02** | `son_iletim_hedefi` gerçek komşuyu taşıyor | Aynı koşuda hedefi dolu **7 329** kararın **0'ında** hedef menzil dışında | ✅ **kapandı** |
| **B-03** | S5 örtüşmesi kalktı; hizalamayı fizik değil metrik yapıyor | Topoloji/trafik/tohum sabit, **yalnızca karıştırıcı fazı** 12 noktada tarandı; sevk edilen 15 m/s ile K-026'nın 20,944 m/s'si karşılaştırıldı → §3-D | ✅ **yön kapandı**, büyüklük üretilemedi *(§8-9)* |
| **B-04** | Test paketi boşlukları kapandı | **10 yeni bağımsız mutasyon** yazdım → **7'si sağ çıktı** | 🔴 **kısmen** → B-27 |
| **B-06** | Uygulanmamış bayraklar `True` yapılamıyor | `Konfig(takvimli_tazeleme=True)` ve `Konfig(bayat_bilgi_null=True)` → ikisi de `NotImplementedError` | ✅ **kapandı** |
| **B-08** | K-017/K-019 üretilebilir oldu | `kurulum_kalibrasyonu.py` koşuldu: Bölüm A **beşinci haneye kadar** tuttu; Bölüm B tablosu birebir; **Bölüm C bayat** | 🟠 **kısmen** → B-28 |
| **B-09** | Ç6.2 artık gerçek değişmez | Ç6.2 `tests/test_rng.py -k test_dilim_` → **2 test** toplanıyor; D20 mutasyonu *(dilim 100 µs → 1 ms)* o testi kırıyor | ✅ **kapandı** |
| **B-10** | Beacon fazı kendi akışında | `AKIS_ADLARI`'nda `beacon_faz` var, `_beaconlari_basla` onu kullanıyor, D21 mutasyonu yakalanıyor | ✅ **kodda kapandı**, belgede değil → B-33 |
| **B-11** | PDR = 0 dejenere işaretleniyor | Sahte paket kümesiyle: `yakinsadi=None`, `dejenere` alanı var, `teslim_gozlem=0` | ✅ **kapandı** |
| **B-12** | `li_zincir.py` elle yazılmış sayı basmıyor | Dosyada `1/6.0 · 1/12 · %16` yalnızca **yorumda**, tarihçe olarak geçiyor; basılan değerler ölçümden | ✅ **kapandı** |
| **B-13** | Üç ölü kontrol `assert`e çevrildi | `traffic.py:113`, `kosucu.py:143`, `mac.py:600` — üçü de `assert` | ✅ **kapandı** *(ama S02 mutasyonu güncellenmedi → B-24)* |
| **B-16/18/19/20** | Ölçülüp kapsam beyanına girdi | Dördü de bağımsız yeniden üretildi → §3 | ✅ **kapandı** |
| **B-22** | Beş kırılamaz iddia düzeltildi | Beş yerde `abs=0.0` var, `test_b22_…` regresyonu var | ✅ **kapandı** *(tarama tamamlanmadı → B-35)* |

---

## 3. DOĞRULANAN İDDİALAR

Hepsi **kendi koşturduğum komutların** çıktısı.

### A · Kapı sayıları

| kriter | iddia | ölçtüğüm | üretici |
|---|---|---|---|
| Ç1.3 | 30/30, her biri kendi testiyle | **30/30** *(0,3 dk)* | `python dogrulama/mutasyon_on_kontrol.py` |
| Ç2 | 6 test | **6/25 toplandı** | `pytest tests/test_kapi_aile0.py -k c2_ --collect-only` |
| Ç3 | 44 test | **44/59 toplandı** | `pytest tests/test_kapi_aile0.py tests/test_radio.py -k "c3_ or test_radio" --collect-only` |
| Ç5 | 14 test | **14 toplandı** | `pytest tests/test_gozlem.py --collect-only` |
| Ç4.1 | 6 test | **6 toplandı** | `pytest tests/test_li_regresyon.py --collect-only` |
| Ç6.2 | 2 test | **2/18 toplandı** | `pytest tests/test_rng.py -k test_dilim_ --collect-only` |
| — | 240 test geçiyor | **240 passed in 208,98 s** | `python -m pytest tests -q` |
| Ç1.1 | korunum 540/540 | **540/540** *(378 s)* | `python dogrulama/kapi_korunum.py` |
| Ç1.4 | boruda kalan < %1 | **%0,156** | aynı |
| Ç1.2 | dört düşme sebebi | **4/4** | aynı |

⚠️ Ç1.2'nin kırılımı `08`in KAPSAMAZ notunu **doğruluyor**: ana matriste
`hedef_yok = 0`, `kuyruk_tasmasi = 0`, `ttl = 0`; yalnızca `iletim_basarisiz`
(547 186) tetikleniyor. Dördün üçü tamamen 20 uç-durum koşusundan geliyor
*(611 368 · 11 655 · 16 001)* ve dördünde de korunum tutuyor.
Yakınsama kapısı bilgi amaçlı: **2/540** koşu yakınsamıyor, en büyük dilim
farkı 0,0513 *(S2/seyrek)*.

### B · Korunum — defteri hiç çağırmadan, paket NESNESİ sayarak

`uretilen − teslim − kuyrukta − ucusta` çıkarmasıyla bulunan düşen sayısı,
defterin `dusen_toplam`ıyla dört yapılandırmada **birebir** aynı:

| yapılandırma | üretilen | teslim | kuyrukta | uçuşta | düşen *(çıkarma)* | defter |
|---|---|---|---|---|---|---|
| S2 / `en_kisa_yol` | 3 198 | 952 | 0 | 0 | 2 246 | 2 246 ✅ |
| S2 / `dongu_yapan` / TTL 2 | 3 198 | 1 | 0 | 0 | 3 197 | 3 197 ✅ |
| S2 / `olu` *(rota yok)* | 3 198 | 0 | 0 | 0 | 3 198 | 3 198 ✅ |
| S2 / kuyruk 1 / yoğun | 127 896 | 505 | 14 | 0 | 127 377 | 127 377 ✅ |

### C · Bu oturumda üretilen yeni sayılar *(şüphe listesi C)*

| iddia | değer | ölçtüğüm | durum |
|---|---|---|---|
| Derece kayması | −%0,364 ± 0,026 | **−%0,364 ± 0,026** | ✅ birebir |
| doğal bağlantı oranı / ort. deneme | %82,93 · 1,2058 | **%82,93 · 1,2058** | ✅ |
| ort. derece koşulsuz / analitik / koşullu | 7,44242 · 7,44258 · 7,41546 | **birebir** | ✅ |
| gerçek akışta atlama/çap/derece | 2,934 · 6,80 [5·10] · 7,387 | **birebir** | ✅ |
| Bölüm B (MAC sonrası) tablosu | %97,0 ± 0,9 · %44,2 ± 1,5 … | **birebir** | ✅ |
| Eski ölçütün seçtiği güç | +4 dBm *(MAC sonrası)*, 0 dBm *(MAC öncesi)* | **+4 · 0** | ✅ |
| S0 kontrol kolu tavanı | 0,9938 · std 0,0122 · [0,8996 · 1,0000] · 21/90 | **birebir** | ✅ |
| Li platosu | 1/6,29 · GA %2,04 · tek atlama 932 kbps | **1/6,29 · %2,04 · 932,0 kbps** | ✅ |
| Kontrol yükü | bayt %2,84 · airtime %5,12 · 1,80 kat | **%2,84 · %5,12 · 1,80** | ✅ |
| Gecikme seçilim yanlılığı | ham fark 1,52 kat abartıyor | **1,52 kat** *(15,45 → 10,14 ms, kesişim %29,7)* | ✅ |
| Alıcı kilidi olmaması | S2/yoğun %0,028 · S0/yoğun %0,027 | **%0,028 (30 / 106 694)** · **%0,027 (35 / 131 597)** | ✅ |
| Beacon açlığı | en kötü %0,65 | **S0: %0,00 · %0,00 · %0,00 · S2: %0,10 · %0,37 · %0,65** | ✅ |
| S2 = +2 dBm gerekçesi | teslim 0,5234 · orta 0,5087 | **0,5252 · 0,5076** | 🔴 §4 |
| Kör mutasyon skoru | %47,8 (11/23), 12 sağ kalan | havuz artık 192, örneklem değişti | 🔴 §4 |

### D · B-03 — örtüşme, kendi ölçümümle

Topoloji, trafik ve tohum sabit; **yalnızca karıştırıcı fazı** 12 noktada
tarandı *(faz doğrudan `Karistirici` nesnesine yazıldı)*:

| kurulum | yörünge periyodu | dilim gerekçesi | **teslim oranının FAZ STD'si** | ort. dilim farkı |
|---|---|---|---|---|
| **sevk edilen** *(15 m/s)* | 125,7 s | yörünge-hizalı, 2 tam tur | **0,00620** | 0,0046 |
| **K-026 hızı** *(20,944 m/s)* | 90,0 s = pencere/3 | yörünge-hizalı, 3 tam tur | **0,00364** | 0,0086 |

**Yön doğrulandı:** K-026'nın hızı faz kaynaklı varyansı **1,7 kat**
bastırıyor; sevk edilen ayarda varyans geri gelmiş. B-03'ün iddiası
*(hizalama örtüşme yaratıyordu, düzeltme onu kaldırdı)* ölçümle tutuyor.

⚠️ **Ama büyüklükleri yeniden üretemedim.** K-036 *"0,00256 → 0,00811
(hizasız referans 0,00846)"* diyor, yani **3,2 kat**; ben 0,00364 → 0,00620,
yani **1,7 kat** ölçtüm. Kurulumum farklı *(tek tohum, 12 faz noktası)* ve
B-10'un RNG kayması araya girdi; hangisinin sebep olduğunu ayıramadım
**(§8-9)**. Sonuç niteliksel olarak aynı, sayılar karşılaştırılabilir değil.

### E · K-020 — üretici komutu olmayan bir kaydın sayıları

| büyüklük | K-020 | ölçtüğüm |
|---|---|---|
| PER @ 0,85R · 1,00R · 1,05R · 1,20R | %0,03 · %17 · %52 · %100 | **%0,03 · %16,97 · %51,60 · %100** ✅ |
| PER %1 → %99 geçişi | 2,8 dB | **2,79 dB** ✅ |
| menzil içi bağ *(tohum 1)* | 133 | **133** ✅ |
| ara bölge bağ sayısı | 11–17 | **6** *(ön-kayıt bandı 0,05–0,9)* 🔴 |
| uzamsal gradyan 300–400 m / 500–600 m | 0,27 / 0,08 | **0,05 / 0,01** 🔴 |

---

## 4. ÜRETİLEMEYEN İDDİALAR

| iddia | nerede | sorun |
|---|---|---|
| **teslim 0,5234 · dinamik aralık [0,1198 · 0,8975] · orta 0,5087** | `config.py` · `06` · `09` · K-039 | Üretici komut bugün 0,5252 · [0,1197 · 0,8955] · 0,5076 veriyor **(B-28)** |
| **Kör tarama %47,8 (11/23), 12 sağ kalan** | `08` · K-043 · `09` | Havuz 185→192, taban 220→240; aynı tohum artık başka 24 mutant seçiyor **(B-25)** |
| **"12 sağ kalanın 4'ü davranışı değiştiriyor, 8'i eşdeğer"** | K-038 | Araç bugün 5/7 diyor; beşincisi bir araç hatası **(B-24)** |
| **"133 bağın 11–17'si ara bölgede"** | K-020 | Ön-kaydın bandıyla 6 (10 tohumda 6–14). Bant yazılmamış; üretici komut yok **(B-30)** |
| **Uzamsal gradyan 0–100 m → 1,00 · 300–400 m → 0,27 · 500–600 m → 0,08** | K-020 | Ölçtüğüm: 1,00 · 0,05 · 0,01. Kova tanımı yazılmamış, üretici komut yok |
| **`08`: uç durumlardan biri "karıştırıcı +11 dBm"** | `08` Ç1 KAPSAR | Kodda öyle bir uç durum yok **(B-34)** |
| **`08`: "185 mutant", "161 sınanmadı", "28 hedefli mutasyon"** | `08` | 192 · 168 · 30 **(B-25, B-34)** |
| **`07`: "Li replikasyonu 1/6,0"** | `07` satır 494 | Güncel 1/6,29 **(B-33)** |
| **B-03 bastırma katsayısı: faz std 0,00256 → 0,00811 *(3,2 kat)*** | K-036 | Kendi ölçümüm 0,00364 → 0,00620 *(1,7 kat)*. **Yön aynı, büyüklük tutmuyor**; kayıtta üretici komut ve "hizasız referans"ın tanımı yok *(§8-9)* |

**Üretici komutu olmayan kayıt sayısı:** `04-NEDEN-BOYLE.md`'deki **43 kaydın
30'unda** *"Üretici"* satırı yok. Çoğu sayı içermeyen tasarım kararı; ama
**sayı taşıyan** ve üretici komutu olmayan kayıtlar arasında en az K-020,
K-024 ve K-029 var — K-020'ninkileri yeniden ürettim, ikisi tutmadı.

---

## 5. KENDİ MUTASYONLARIM

**10 mutasyon × tam 240 testlik paket** *(10,9 dk, 5 paralel)*. Y8 gereği her
mutasyonun bozduğu yolun sağlam koşuda tetiklendiğini **önce** ölçtüm
*(S2/orta/tohum 1, 7 342 karar)*:

| yol | tetiklenme |
|---|---|
| bayat komşu filtresi devrede | 250 karar |
| `kanal_mesgul_mu == True` | 1 417 karar |
| `kuyruk_uzunlugu > 0` | 7 342 karar |
| karıştırıcı, ölçülen gürültünün >%5'i | 6 358 karar |
| yeniden deneme / MAC düşürmesi | 17 377 deneme / 2 246 düşürme |
| yayın alıcı sayısı > 1 | ort. komşu 6,375 |
| S5 yörüngesi | `test_s5_de_yakinsiyor` + 4 S5 koşusu |
| kesişim oranı ≠ 1 | ölçülen %29,7 |

### Sonuçlar

| # | mutasyon | test paketi | davranış *(K-038 ölçütü)* |
|---|---|---|---|
| KM1 | `kesisim_orani_pencere` → `1.0` | 🔴 **sağ kaldı** | 🔴 değişti — rapora giren kesişim oranı sabitlenir |
| KM2 | `komsu_omru_katsayisi` 10 → 1000 | 🔴 **sağ kaldı** | 🔴 değişti — 12 koşunun **8'inde**, teslim 0,2867 → 0,1800'e kadar |
| KM3 | hareketli karıştırıcı yörünge **yönü** ters | 🔴 **sağ kaldı** | 🔴 değişti — bütün S5 koşuları |
| KM5 | `kanal_mesgul_mu` → `False` | 🔴 **sağ kaldı** | ⚪ tüketicisi yok *(B-27b)* |
| KM6 | `kuyruk_uzunlugu` → `0` | 🔴 **sağ kaldı** | ⚪ tüketicisi yok *(B-27b)* |
| KM7 | yeniden deneme sınırı `>` → `>=` *(5 → 4 iletim)* | 🔴 **sağ kaldı** | 🔴 değişti — **13/13** koşu |
| KM8 | `kanal_cekimi` alıcıya duyarsız | 🔴 **sağ kaldı** | 🔴 değişti — **13/13** koşu |
| KM4 | ölçülen gürültü karıştırıcıyı görmüyor | ✅ yakalandı | `test_d10b_beacon_gurultu_ve_kuyruk_bildiriyor` |
| KM9 | CBR titreşimi tek yönlü *(ortalama aralık kayar)* | ⚠️ yakalandı | `test_b19_ortak_alt_kume_…` — **ilgisiz test**; titreşim simetrisi için bir koruma yok |
| KM10 | kuyruk FIFO → LIFO | ⚠️ yakalandı | `test_bosaltma_…` + `test_s0_teslim_tavani_yuksek` — **ikisi de ilgisiz**; kuyruk disiplini için koruma yok |

**SAĞ KALAN: 7/10.** *(Birinci denetim: 8/10, 198 testle.)*

### Örüntü

1. **Fizik ve MAC korunuyor; kurulum parametreleri korunmuyor.**
   `komsu_omru_katsayisi`, `yeniden_deneme_siniri`'nin etkin değeri ve yörünge
   yönü — üçü de tek satırlık değişikliklerle sessizce kayıyor.
   `test_d3_bayat_komsu_gozlemden_dusuyor` ömrü **`kon.komsu_omru_s`'ye göreli**
   kullandığı için ömrün DEĞERİNE tanım gereği duyarsız — B-22'nin
   *"kırılamayan iddia"* sınıfının parametre hâli.
2. **Gözlem penceresi hâlâ zayıf halka**, ama artık farklı sebeple: alanlar
   doğru üretiliyor, **hiç tüketilmiyor** ve içerikleri sınanmıyor (B-27b).
3. **Eşleştirmenin kalbi korumasız.** `kanal_cekimi`den alıcıyı çıkarmak
   13/13 koşuda sonucu değiştiriyor ve hiçbir test görmüyor —
   `test_c2_3_iki_kol_ayni_kanali_goruyor` iki kolun **aynı** çekimi
   görmesini sınıyor, çekimin doğru **dörtlüden** üretildiğini değil.
4. **"Yakalandı" ≠ "korundu".** KM9 ve KM10 yakalandı, ama kıran testler
   bozulan mekanizmayla ilgisiz. B-21'in `beklenen_test` ölçütü mutasyon
   paketine uygulanıyor; kör/bağımsız mutasyonlarda böyle bir süzgeç yok,
   dolayısıyla "mutasyon skoru" olduğundan iyi görünür.

---

## 6. ŞÜPHE LİSTESİ SONUÇLARI

| # | Şüphe | Sonuç |
|---|---|---|
| **1** | Kırılamayan iddia | 240 testin `approx` çağrılarının tamamını taradım. B-22'nin beş vakası düzeltilmiş. **Bir kalıntı:** `test_ber_kapali_form` γ=20'de ilan ettiği `rel`in 970 katı toleransla çalışıyor **(B-35)**. Bunun **parametre hâli** daha ciddi: `test_d3` ömrü göreli kullandığı için ömrün değerine kırılamaz **(B-27/KM2)**. `assert all(...)`/`any(...)` taraması: dördü de boş kümede geçmiyor, hepsinin önünde doluluk kontrolü var ✅ |
| **2** | Aracın kendi çıktısını doğrulamaması | `mutasyon_paketi` taban kontrolü ✅ · `kor_mutasyon` taban kontrolü ✅ · `sag_kalan_ayikla` koşu sayısı kontrolü ✅ · `mutasyon_on_kontrol` rc=5 / "0 test" ayrımı ✅ · `_pytest` beklenen sayı kontrolü ✅ *(hepsini doğruladım)*. **Üç delik:** Ç1.3'ün eşiği veriden türetiliyor **(B-32)**; `sag_kalan_ayikla` araç hatasını bulgu sanıyor **(B-24)**; `karsilastirma` girdi kontrolü hiçbir şey doğrulamıyor **(B-26)** |
| **3** | Tetiklenmeyen yolda "eşdeğer" kararı | Araç tetiklenme sayaçlarını **basıyor** ama karara **bağlamıyor**; `donguyle_olen = 0` uyarısı iki koşuda da çıkmış, iki kayıtta da anılmamış **(B-36)**. Kendi mutasyonlarımda aynı tuzağa düştüm ve düzelttim: KM2/KM5/KM6 kâhin aktarıcıyla "eşdeğer" çıkıyor, gözlemi kullanan aktarıcıyla KM2 **8/12 koşuda değişiyor** |
| **4** | Düzeltmenin kendisi hata getirdi mi | RNG kayması **gerçek ve ölçülmemiş bir kalıntı bıraktı**: kalibrasyon tablosu **(B-28)**. `sag_kalan_ayikla` girdisi B-13 düzeltmesiyle bayatladı **(B-24)**. Kayan sayıların hepsi yeniden ölçülmedi: B-16 ve B-18 ölçüldü *(ve ikisini de birebir yeniden ürettim)*, Bölüm C ölçülmedi |
| **5** | Karar kayıtlarının sayıları | Beş kayıt sınadım: **K-017** ✅ *(beş hane)*, **K-019/K-039 Bölüm A–B** ✅, **K-039 Bölüm C** 🔴, **K-022/K-030 Li platosu** ✅, **K-020** 🔴 *(iki sayı)*, **K-041 B-16/18/19/20** ✅. 43 kaydın **30'unda** "Üretici" satırı yok |
| **6** | Kapsam beyanının doğruluğu, iki yönlü | **(a)** *"Yapmaz"* denen 16 maddeyi kodda kontrol ettim; **hiçbiri fiilen yapılmıyor** — RTS/CTS, EIFS, NAV, çoklu radyo, frekans çevikliği yok; `kanal_mesgul` karıştırıcıyı **gerçekten** dışlıyor *(satır 480)*; kopya önbelleği sınırsız; `Topoloji` sabit. ✅ **(b)** Listede **olmayan** dört sınır buldum: 2B geometri, tek/merkezî karıştırıcı, enerji kısıtı, kuyruk disiplini **(B-37)**. Etki yönleri: 15 maddenin yönü doğru; 5. maddenin *("karıştırıcı taşıyıcı dinlemeyi tetiklemez → karıştırmayı hafifletir")* yönünü kodla doğruladım ✅ |
| **7** | Yeni şema gerçekten işe yarıyor mu | 🔴 **Hayır — varsayımı kırdım.** `dugum_sayisi` 40↔41 ile iki kolun **hiçbir paketi ortak değil**, koruma kabul etti ve gecikme farkı üretti **(B-26)**. `iletim_menzili_m` ve `alan_m` varyantlarında da koruma hiçbir şey doğrulamadı |
| **8** | Çalışma noktasının gerekçesi | Ölçütü üç eksende zorladım *(tarama uçları · farklı aktarıcı · farklı tohum sayısı)*; **üçünde de +2 dBm** seçiliyor. Ölçüt "cevabı korumak için seçilmiş" gibi davranmıyor — **savunulabilir**. 🔴 Ama ilan edilen iki koşuldan biri *(ulaşılabilirlik ≥ %90)* koda hiç girmemiş **(B-29)**, ve sayıları bayat **(B-28)** |
| **9** | Aile 1 bu araçla yazılabilir mi | **Pencere karar için yeterli**, mekanizma kapısı için **değil.** Bağ kalitesi temelli bir protokol `son_iletim_sonucu` + `duyulan_beacon` + `son_duyulma_s`ten ETX benzeri bir kestirim kurabilir *(A3 "kendi geçmişinden hesaplama" izin veriyor)*. 🔴 **Ama** H1.1'in ön-kayıtlı mekanizma kapısı ölçülemiyor **(B-30)**, ve dört alan hiç tüketilmediği için ilk gerçek okuyucuda doğrulanmamış olacak **(B-27b)**. ⚠️ Ayrıca: protokol **yalnızca** düğümün paketi varken ve MAC boşken çağrılıyor; kuyruk boşken gerçekleşen iletim sonuçları protokole hiç görünmüyor — takvimli/periyodik davranış *(Aile 2'nin `takvimli_tazeleme` kolu)* bu arayüzle protokol tarafından **kurulamaz** |
| **10** | Depodaki bayat çıktılar | Altı dosyanın **beşi** bayat; dördü bugünkü koddan üretilemiyor **(B-39)**. Bayat çıktılara dayanan sayı: `08`in "185 / 161 / %47,8"i **(B-25)** |
| **11** | Ön-kaydın iç tutarlılığı | H1.1 ölçülemez *(mekanizma kapısı — B-30)*. H1.2 ölçülebilir; ön koşulunu *(taranan aralık ≥ 3 × tohum std)* kontrol ettim: aralık **0,776**, en büyük tohum std **0,2228** → 3× = 0,668 < 0,776 ✅ **ama yalnızca 1,16 kat marjla, ve KÂHİN aktarıcıyla ölçüldü**; ön-kayıt bunu "yalnızca rakip kollar" için istiyor. H1.3 ölçülebilir ✅ *(S1↔S3, S2↔S4 eşdeğer sabit güç kodda tek kaynaktan)*. Aile 2'nin dört kolu ve mekanizma kapısı için `takvimli_tazeleme` / `bayat_bilgi_null` **henüz uygulanmamış** *(açıkça beyan edilmiş)* |
| **12** | İstatistik planı | 🔴 **Kod karşılığı yok.** `wilcoxon` · `holm` · `scipy` deponun hiçbir yerinde geçmiyor; NaN tuzağına karşı ne kontrol ne regresyon testi var. Ve `08` bunu KAPSAMAZ listesine yazmamış **(B-31)** |

**Birinci denetimin 12 maddelik listesi** *(`AILE0-DENETIM-PROMPTU.md`)* de
uygulandı; oradaki maddeler bu tabloya dağıldı. Yeni bir bulgu çıkmadığı
maddeler: eşleştirme *(iki kol aynı kanalı görüyor — Ç2.3 geçiyor)*,
başlangıç koşulları *(komşu tablosu t=0'da boş, CBR fazı rastgele, karıştırıcı
fazı rastgele — üçü de doğrulandı)*, rezonans *(darbe periyodu 2,7 s, CBR 1,0 s;
`test_darbe_periyodu_cbr_araligiyla_olcusmuyor` bunu koruyor ve mutasyonla
kırılıyor)*.

---

## 7. KAPSAM BEYANINA EKLENMESİ GEREKENLER

`08-AILE0-KAPSAM.md`'ye, her biri **etki yönüyle**:

| # | Madde | Etkinin yönü |
|---|---|---|
| **17** | **Geometri 2 boyutlu** — düğümler tek düzlemde, irtifa yok | İHA ağı için bir serbestlik derecesi eksik; bağ geometrisi ve karıştırıcının aydınlatma deseni gerçeğe göre **basit** |
| **18** | **Tek karıştırıcı, alanın merkezinde** — çoklu/kenar/hareketli-grup karıştırma yok | 🔴 **İyimser ve hipotezin lehine:** simetrik bir zehirli bölge, etrafından dolaşılabilir. H1.1'in mekanizması buna dayanıyor |
| **19** | **Enerji / pil kısıtı modellenmiyor** | Kontrol düzlemi maliyeti yalnızca bayt ve airtime; SWaP kısıtı ölçülmüyor |
| **20** | **Kuyruk tek sınıf, önceliksiz FIFO** | Gecikme dağılımı disipline duyarlı *(FIFO→LIFO mutasyonu iki testi kırıyor)*; trafik sınıfı ayrımı yok |
| **21** | **İstatistiksel test katmanı YAZILMADI** *(Wilcoxon · Holm · güç analizi · NaN koruması)* | `06` Bölüm 3 planı henüz koda dönmedi; NaN tuzağının koruması yok |
| **22** | **Gözlem penceresinin dört alanının tüketicisi ve içerik testi yok** *(`saat_s`, `kanal_mesgul_mu`, `kuyruk_uzunlugu`, `kuyruk_kapasitesi`)* | Aile 1'in ilk protokolü bu alanları okuduğunda doğruluklarının kaydı olmayacak |
| **23** | **Ortak alt küme koruması paket evrenini doğrulamıyor** | Farklı konfigürasyonlu iki kol sessizce karşılaştırılabilir → gecikme farkı anlamsız olabilir |
| **24** | **H1.1'in mekanizma kapısı mevcut şemayla ölçülemez** | Sayaç eklenmeden Aile 1 koşulursa, ön-kayıt gereği sonuca bakılamaz |

Ayrıca **düzeltilmesi** gerekenler: Ç1 KAPSAR tablosundaki *"karıştırıcı
+11 dBm"* uç durumu **(B-34)**, *"185 mutant / 161 sınanmadı / 28 mutasyon"*
sayıları **(B-25, B-34)**.

---

## 8. ANLAŞILMAYANLAR

> Bu bölüm boş değil. Anlamadığım bir mekanizma, denetlenmemiş bir mekanizmadır.

1. **K-020'nin "ara bölge" bandını ve uzamsal gradyan kovalarını
   çıkaramadım.** Ön-kaydın bandıyla (0,05–0,9) 6, [0,01 · 0,99] ile 11–26
   çıkıyor; ikincisi K-020'nin aralığıyla örtüşüyor ama **bunu doğrulayamadım**
   — kayıtta bant yazmıyor ve üretici komut yok. Gradyan sayıları (0,27 / 0,08)
   hiçbir denemede çıkmadı; kova tanımının *(alıcı bazlı mı, bağ bazlı mı,
   hangi güçte)* ne olduğunu belirleyemedim. **Denetleyemedim.**

2. **`_uyandir` özyinelemesinin derinliği ve `hedef_yok` yolundaki
   `self._uyandir(dugum)` çağrısının sınırını çözemedim.** `olu` aktarıcıyla
   127 896 paketlik koşuda yığın taşması olmadı, ama neden olmadığını
   *(kuyruk uzunluğu sınırı mı, `bak()` sırası mı)* kesinleştiremedim.
   Bir protokol sürekli `None` döndürürse bu yol her paket için özyineliyor.

3. **`kanal_izi` mekanizmasının Ç2.3'te ne kadarını kapsadığını
   ölçemedim.** Varsayılan kapalı; açıkken hangi çekimlerin kaydedildiğini ve
   iki kolun karşılaştırmasının hangi alt kümede yapıldığını izlemedim.
   KM8 (çekimden alıcıyı çıkarmak) 240 testten sağ çıktığına göre, Ç2.3'ün
   kapsamı sandığımdan dar olabilir — ama **hangi kadar dar olduğunu
   ölçmedim.**

4. **`Gozlem.komsular` beşten uzun olduğunda Ç5.1'in yüzey taraması ne
   görüyor?** `_yuzeyi_gez` demet/listeleri **ilk 5 elemanla** kesiyor
   (`nesne[:5]`) ve derinliği 6 ile sınırlıyor. Ölçülen ortalama komşu sayısı
   **6,375**. Altıncı komşuda saklanan bir sızıntının görülüp görülmeyeceğini
   **sınamadım**; `test_c5_1b` yalnızca üst düzey bir alanla doğrulanmış.

5. **`hedefe_en_yakin` aktarıcısının "yarı kâhin" olmasının kalibrasyon
   çapraz kontrolüne etkisini ayırt edemedim.** Ölçütü onunla da sınadım ve
   +2 dBm çıktı, ama o aktarıcı hedefin **konumunu** kâhinden alıyor. Tamamen
   gözlemsel `gurultuden_kacan` ile eğri anlamlı değil *(teslim %10–29,
   döngüye giriyor)*, yani ölçütün **gerçek bir protokolün** eğrisinde ne
   seçeceğini bilmiyorum.

6. **KM7'nin (etkin deneme 5 → 4) K-039'un `PER⁵ ≤ eşik` bağ tanımıyla
   ilişkisini niceliksel olarak kapatamadım.** Deneme sayısı bağ
   kullanılabilirlik eşiğini *(0,7013)* tanımlıyor; mutasyon 13/13 koşuda
   sonucu değiştiriyor ama kalibrasyon tablosunun ne kadar kayacağını
   **ölçmedim.**

7. **`donguyle_olen` sayacının bu matrislerde neden hep 0 olduğunu
   anlamadım.** `dongu_yapan` aktarıcısı TTL ölümü üretiyor ve `dongude_mi`
   ziyaret listesinden hesaplanıyor; yine de hem kayıtlı hem bugünkü ayıklama
   matrisinde 0. Ya `_ziyaret` beklediğim gibi dolmuyor, ya TTL ölümü döngü
   tamamlanmadan gerçekleşiyor. **Ayırt edemedim** — ve araç bu sıfırı
   "eşdeğer kararı geçersizdir" uyarısına çeviriyor (B-36).

9. **B-03'ün bastırma katsayısını yeniden üretemedim.** K-036 3,2 kat
   *(0,00256 → 0,00811)* diyor; benim kurulumumda 1,7 kat *(0,00364 →
   0,00620)*. Yön aynı, büyüklük değil. Farkın kaynağı — kurulum farkı mı
   *(tek tohum · 12 faz noktası)*, B-10'un RNG kayması mı, yoksa "hizasız
   referans"ın nasıl kurulduğu mu — **ayırt edemedim**; K-036 o referansın
   nasıl üretildiğini yazmıyor ve kayıtta üretici komut yok.

10. **Tek makine, tek Python sürümü, tek işletim sistemi.** Birinci denetimin
    7. maddesi; ben de aşamadım.

---

## 9. KOŞTURDUĞUM KOMUTLAR

Depoda (yalnızca okuma/koşma; hiçbir dosya değiştirilmedi):

```bash
python -m pytest tests -q                      # 240 passed in 208.98s
python dogrulama/mutasyon_on_kontrol.py        # 30/30, 0.3 dk
python dogrulama/sag_kalan_ayikla.py           # 5 "DEĞİŞTİ" / 7 eşdeğer, 6.5 dk  -> B-24
python dogrulama/kurulum_kalibrasyonu.py       # Bölüm A+B+C                      -> B-28
python dogrulama/kapi_korunum.py               # Ç1.1 / Ç1.2 / Ç1.4
python -m pytest <kapı seçimleri> --collect-only -q      # 6 / 44 / 14 / 6 / 2
```

Geçici dizinde yazdığım denetim betikleri *(`…\scratchpad\den2\`)*:

| betik | ne ölçtü | özet çıktı |
|---|---|---|
| `kendi_mutasyonlarim.py` | 10 bağımsız mutasyon × 240 test | **7 sağ kaldı** → B-27 |
| `etki_olc.py` | sağ kalanlar davranışı değiştiriyor mu *(13 koşu)* | KM1/3/7/8 **değişti** |
| `etki2.py` | gözlem mutasyonları, gözlemi KULLANAN aktarıcılarla *(12 koşu)* | KM2 **8/12 değişti**; KM5/KM6 tüketicisiz → B-27b |
| `tavan_li.py` | S0 tavanı *(90 koşu)* + Li platosu *(30 tohum)* | 0,9938 · 1/6,29 — ikisi de **birebir** |
| `b03_dogrula.py` | faz taraması, hizalı vs K-026 hızı | §3-D |
| *(gömülü betikler)* | korunum nesne sayımı · alıcı kilidi · kontrol yükü · gecikme yanlılığı · beacon açlığı · K-020 · ölçüt zorlaması · paket evreni kırma · `approx` taraması | §3, §4, B-26, B-29, B-35 |

---

## KAPANIŞ NOTU

Bu depo, gördüğüm kadarıyla, kendi hatasını **ölçmeyi kural hâline getirmiş**
nadir projelerden biri. Birinci denetimin 23 bulgusunun 23'ü gerçekten
kapatılmış; 13 çıkış kriterinin **13'ünü de** bağımsız olarak yeniden ürettim
*(Ç6.1/6.3/6.4 dâhil — üçü de kaynak denetimi olarak doğrulandı)* ve hepsi
ilan edilen değerlerle geçiyor;
korunum defteri nesne düzeyinde dürüst; ve kapı kriterlerinin *kendisinin*
denetlenmesi — beş kusur çıkararak — bu projenin en değerli işi.

Ama kapanış metninin iki cümlesi ölçümle tutmuyor:

> *"Kör tarama gerçek skoru: %47,8, 12 sağ kalan ayıklandı"* — o skor artık
> üretilemez, ve ayıklama aracı bugün bir araç hatasını bulgu diye raporluyor.

> *"Şema Aile 1 başlamadan düzeltildi"* — düzeltilen şey gecikme seçilim
> yanlılığıydı ve o düzeltmenin **koruması boş**; ayrıca Aile 1'in kendi
> ön-kayıtlı mekanizma kapısı bu şemayla ölçülemiyor.

Ve en önemlisi: **7/10.** Birinci denetim 8/10 demişti; 42 yeni test ve 23
düzeltmeden sonra yeni bir bağımsız örneklem 7/10 veriyor. Bu, düzeltmelerin
işe yaramadığı anlamına gelmez — adı konmuş her yol gerçekten kapandı. Şu
anlama gelir: **kapanan şey bulgular kümesiydi, örüntü değil.** Örüntünün
kapandığını söyleyebilmenin tek yolu, bağımsız bir örneklemde sağ kalan
oranının düşmesidir; bugün düşmedi.

Kapanış iptal edilmemeli. Ama *"kapılar artık doğru şeyi ölçüyor"* cümlesi
**"kapıların ölçtüğü şey bir kez denetlendi ve beş kusur çıktı; ikinci
denetimde on yedi bulgu daha çıktı"** olarak yazılmalı — çünkü bulunmayan her
şey, jürinin bulacağı bir şeydir.

---

🔒 **Depoda hiçbir dosya değiştirilmedi; hiçbir git komutu çalıştırılmadı.**
Yazılan tek dosya bu rapordur (`aile0_audit.md`).

---

# ÜÇÜNCÜ DENETİM — 20 Ağustos 2026

| | |
|---|---|
| **Denetçi** | Bağımsız doğrulama denetçisi (üçüncü, sıfır bağlamlı oturum) |
| **Denetlenen** | K-046'daki **13/13** kapanış + K-044'ün *"17 bulgunun 17'si kapatıldı"* iddiası + 20 Ağustos'ta yazılan, hiç bağımsız denetlenmemiş kod |
| **Depo** | `C:\Users\Xelma123\Desktop\desparete_pls` — **hiçbir dosyası değiştirilmedi** |
| **Ortam** | Windows 11 · Python 3.11 · numpy 1.26.4 · scipy 1.17.1 · pytest 8.2.2 · 12 çekirdek (en fazla 5 eşzamanlı test paketi) |
| **Git** | Hiçbir git komutu çalıştırılmadı |
| **Tohumlar** | Yalnızca 1–30 ayarlama kümesi + araçların kendi sabit tohumları. **2000–2029 hiçbir amaçla koşulmadı** |
| **Yazılan tek dosya** | `aile0_audit.md` |
| ⚠️ **Bütçe aşımı** | Mutasyon partisi için *"~20–25 dk"* tahmini yazıldı; fiilen **~50 dk** sürdü (15 paket × ~8–9 dk, 5 paralel). Tahmin yanlıştı ve bu tahmin edilerek değil **ölçülerek** kaydedilmiştir |

Bütün deneme betikleri geçici dizinde (`…\scratchpad\den3\`) tutuldu; her
mutasyon `shutil.copytree` kopyasında uygulandı ve **uygulandıktan sonra kodda
yeniden okunarak doğrulandı** (`03` kural 15).

---

## 0. YÖNETİCİ ÖZETİ

> ### Kapanış geçerli mi: **KOŞULLU** — ve örüntü **üçüncü kez kapanmadı**

### 🔴 SAĞ KALAN ORANI

| denetim | bağımsız mutasyon | **sağ kalan** | test paketi | oran |
|---|---|---|---|---|
| Birinci *(19 Ağu)* | 10 | 8 | 198 | **%80,0** |
| İkinci *(20 Ağu)* | 10 | 7 | 240 | **%70,0** |
| **Üçüncü — bu rapor** | **15** | **10** | **284** | **%66,7** |

**%66,7 sayısal olarak 7/10'un altındadır — ama örüntünün kapandığı
söylenemez, ve bunun üç ölçülmüş sebebi var:**

1. **Fark gürültünün içinde.** n=15'te binom standart hatası ≈ **12,2 puan**;
   %70 → %66,7 farkı 0,3 SH'dir. İki oran ayırt edilemez.
2. **İlk on mutasyonum tam olarak 7/10 verdi** (U01–U10 arasında sağ kalan:
   U01 · U02 · U05 · U06 · U07 · U09 · U10). Karşılaştırılabilir örneklem
   boyutunda oran **birebir aynı**.
3. Her iki örneklem de **amaçlı** (purposive) seçildi, rastgele değil —
   ikisinin de hedefi *"en az denetlenmiş kod"*du. Aralarındaki farkı bir
   ilerleme ölçüsü saymak, `03` B2'nin *"gürültüden dar tarama"* tuzağıdır.

Sağ kalan 10'un **4'ü davranışı fiilen değiştiriyor** *(48 koşuluk sabit
matriste, `sag_kalan_ayikla.py` ölçütüyle)*, **5'i tüketicisiz**, **1'i de
simülatörü değil KAPININ KENDİSİNİ bozuyor.**

### Kapanışın tuttuğu yer

Yeniden ürettiğim **her sayı tuttu**: kalibrasyon *(+2 dBm 0,5252 · dinamik
aralık [0,1197 · 0,8955] · orta 0,5076 · elenen +6/+8/+10/+11)*, derece
kayması *(−%0,364 ± 0,026)*, Li platosu *(1/6,29 · GA %2,04)*, mekanizma
sayacı *(%8,68 vs %1,86 · 4,68 kat · 0,3282 vs 0,0055)*, K-020'nin bağ geçişi
*(%0,03 / %16,97 / %51,60 / %100 · 2,79 dB)*, sağ kalan ayıklaması *(7/7
eşdeğer · davranışı değiştiren 0 · araç hatası 0)*, envanter *(284 test · 35
mutasyon · 203 kör mutant · 46 karar · 22 kapsam maddesi)*. B-24'ün girdi
listesi bugün **bayat değil** (7/7 desen tam olarak bir kez bulunuyor);
B-29'un kısıtı **koda girmiş**; B-31 `08` madde 21 olarak **beyan edilmiş**;
B-33/B-34/B-38 **düzeltilmiş**; D10 kapanışı **gerçekten koruyor** (U15
yakalandı). Ön-kaydın 🔴 ile işaretlediği **NaN tuzağını** da doğruladım —
`wilcoxon` n=10'da p=1,0, **n=30'da p=nan**.

### Kapanışın tutmadığı üç yer

1. 🔴 **K-044'ün ilan ettiği bir düzeltme kodda YOK.** B-32 için
   *"`BEKLENEN_MUTASYON = 35` sabiti; liste küçülürse `!!LİSTE n≠35`"*
   yazılmış; depoda böyle bir sabit **hiç yok** ve Ç1.3'ün eşiği hâlâ
   `{toplam}/{toplam}`. Kapının gerçek kod yolunu koşturdum: mutasyon listesi
   35 → 5'e düşmüş gibi davrandığında kapı **"Ç1.3 · 5/5 · OK"** ve
   **"AİLE 0 KAPANMAYA HAZIR — 13/13"** yazıyor. *(B-41)*
2. 🔴 **Kapının ne ölçtüğü sessizce değiştirilebiliyor ve "kapının kapısı"
   görmüyor.** Ç5'in seçimini `-k "not test_b27b"` yapıp beklenen sayıyı
   18→14 indirdim: **284/284 test geçiyor**, `test_kapi_secimleri` geçiyor,
   ve kapının Ç5 kriteri **GEÇTİ** dönüyor — B-27b'nin dört içerik testi
   Ç5'in kapsamından tamamen çıkmışken. *(B-42)*
3. 🔴 **Aile 1'in iki rakip protokolü bu arayüzle yazılamıyor.** Protokolün
   herhangi bir çerçeveye bilgi koyma yolu **yok** (beacon içeriği
   `sim/kosucu.py`de sabit, `PaketGorunumu` donmuş 5 alan), hedefin konumu
   ya da uzaklığı gözlemde **yok**. Yazdığım saf gözlem ETX protokolü
   karıştırıcısız S0'da **0,0997** teslim ve **1,00** ortalama atlama
   veriyor — yani yalnızca komşusu olan hedeflere taşıyor. *(B-47)*

Buna, gözlem sözleşmesinin B-27b ile kapatıldığı iddiasının **elle taşınan
bir etikete** dayandığı *(B-43)*, karıştırıcıyı görebilen tek gözlem alanının
**hiç korunmadığı** *(B-44 — U14 284/284 geçiyor)* ve H1.1'in mekanizma
kapısının **null model sınavını geçmediği** *(B-45)* ekleniyor.

**Kapanış iptal edilmeli mi: hayır.** 13 kriterin ölçtüğü şeyler gerçekten
ölçülüyor ve ana sayıların hepsi tutuyor. Ama **kapanış metni üçüncü kez
düzeltilmelidir** ve `08-AILE0-KAPSAM.md` bu bulgular kapanmadan
**mühürlenemez.**

---

## 1. YENİ BULGULAR

Ciddiyet: 🔴 kritik · 🟠 orta · ⚪ düşük. Numaralar **B-41**'den devam eder.

---

### 🔴 B-41 · K-044'ün B-32 için ilan ettiği düzeltme KODA HİÇ GİRMEMİŞ — Ç1.3'ün eşiği hâlâ veriden türüyor

**Nerede:** `dogrulama/aile0_kapi_raporu.py:238–241` ↔ `v2/04-NEDEN-BOYLE.md` K-044 (B-32 satırı)

**İDDİA (K-044):** *"**B-32** | Ç1.3'ün eşiği hâlâ veriden türetiliyordu
(`{toplam}/{toplam}`) … | **`BEKLENEN_MUTASYON = 35` sabiti; liste küçülürse
`!!LİSTE n≠35`**"*

**ÖLÇTÜĞÜM** — Depoda `BEKLENEN_MUTASYON` diye bir isim **yok**, `!!LİSTE`
diye bir uyarı **yok**, ve kod ikinci denetimde bulunduğu hâliyle duruyor:

```python
K.append(Kriter(
    "Ç1.3", "mutasyon paketi (her mutasyon KENDİ testiyle)",
    f"{mp['yakalanan']}/{mp['toplam']}{notu}",
    f"{mp['toplam']}/{mp['toplam']}", mp["gecti"]))     # ← EŞİK = VERİNİN KENDİSİ
```

`mp["toplam"] = len(MUTASYONLAR)` ve `mp["gecti"] = (yakalanan == len(MUTASYONLAR) …)`
*(`dogrulama/mutasyon_paketi.py:534, 538`)*. Üstelik `tests/test_kapi_secimleri.py:46–48`
kendi yorumunda bu tuzağı **hâlâ açık bir tuzak olarak** anıyor:
*"Ç1.3'ün `{toplam}/{toplam}` tuzağının (B-32) bu dosyadaki hâli."*

Kapının **gerçek Ç1.3 kod yolunu** koşturdum *(pahalı kriterler taklit edildi;
Ç1.3 dalı DEĞİŞTİRİLMEDEN çalıştı)* ve listeyi 35 → 5'e düşmüş gibi gösterdim:

```
OK Ç1.3  mutasyon paketi (her mutasyon KENDİ testiyle)   5/5   5/5
OK AİLE 0 KAPANMAYA HAZIR — 13/13 kriter geçti.
```

**ÜRETİCİ KOMUT**
```bash
grep -rn "BEKLENEN_MUTASYON" dogrulama/ tests/ sim/
```
```bash
python scratchpad/den3/b32_kanit.py
```

**beklenen / görülen** — beklenen: `!!LİSTE 5≠35` ve Ç1.3'ün **düşmesi**.
görülen: `5/5`, kriter **geçiyor**, kapı **13/13** ilan ediyor.

**Neden önemli** — Bu, `03` **kural 15**'in *("kod değişikliğini 'başarılı'
yazan bir betiğin çıktısına güvenme; değişikliği KODDA doğrula")* karar
defterindeki hâli: kayıt bir düzeltmeyi tarif ediyor, kod onu içermiyor, ve
bunun üzerine **40/40 kapalı** ilan edildi. K-044 aynı hatanın o gün **bir kez**
yaşandığını kendisi yazıyor *(B-24 düzeltmesi ilk denemede landing etmemişti)*;
ikincisi yakalanmadı çünkü onu zorlayan bir test yok.

**Öneri** — `BEKLENEN_MUTASYON = 35` sabiti + `mp["toplam"] == BEKLENEN_MUTASYON`
kontrolü; ve `tests/test_kapi_secimleri.py`ye **Ç1.3'ü de kapsayan** ucuz bir
test *(`len(MUTASYONLAR) == 35`)*. Kapı 71 dakika sürdüğü için yalnızca orada
konuşan hiçbir sabit güvende değildir — K-046'nın kendi **Y12 adayı** budur.

---

### 🔴 B-42 · Kapının NE ÖLÇTÜĞÜ sessizce daraltılabiliyor; "kapının kapısı" yalnızca SAYI tutarlılığına bakıyor

**Nerede:** `dogrulama/aile0_kapi_raporu.py:72–86` (`KAPI_SECIMLERI`) ↔ `tests/test_kapi_secimleri.py:65–82`

**İDDİA (K-046):** *"Kapı seçimleri artık **tek kaynakta**… Kapının beklenen
sayıları **her suite koşusunda** denetleniyor — 71 dakika değil, **5,5 saniye**."*

**ÖLÇTÜĞÜM** — Ç5'in satırını **kendi içinde tutarlı** biçimde daralttım *(U10)*:

```python
"Ç5": ("gözlem sözleşmesi", ["tests/test_gozlem.py"], "not test_b27b", 14),
```

Bu, B-27b'nin **dört içerik testini** Ç5'in kapsamından tamamen çıkarır.
Üç katmanın üçü de sessiz kaldı:

| kontrol | sonuç |
|---|---|
| tam test paketi *(284)* | **284 passed** — hiçbir test kırılmadı |
| `toplanan_test_sayisi(yollar, secim)` *(ucuz koruma)* | **14**, beklenen **14** → **geçiyor** |
| kapının kendi `_pytest(...)` çağrısı | `gecen=14 kirilan=0 not=''` → **Ç5 GEÇTİ** |

**ÜRETİCİ KOMUT**
```bash
python scratchpad/den3/kostur.py
```
```bash
python -c "import sys;sys.path.insert(0,'.');from dogrulama.aile0_kapi_raporu import KAPI_SECIMLERI,_pytest,toplanan_test_sayisi;ad,y,s,a=KAPI_SECIMLERI['Ç5'];print(toplanan_test_sayisi(y,s),a);print(_pytest(y,s,a))"
```

**beklenen / görülen** — beklenen: bir kriterin kapsamı daralınca en az bir
koruma konuşur. görülen: **hiçbiri konuşmuyor**.

**Neden önemli** — `test_kapi_secimleri.py` tam olarak bu sürüklenme sınıfı
için yazıldı, ama ölçtüğü şey *"yazılı sayı = bugün toplanan sayı"*. İkisi
**birlikte** değiştirilirse koruma tanım gereği susar. Y11'in ta kendisi:
koruma yalnızca yakalayabildiği durumla (**sayı** sürüklenmesi) sınanmış;
kapsamı dışındaki durum (**seçim** sürüklenmesi) hiç sınanmamış. Ve
`KAPI_SECIMLERI`nin **yol + `-k` seçimi** kısmını hiçbir şey denetlemiyor —
`03` B5'in *"etiketi elle taşımak"* tuzağı.

**Öneri** — Kriterin kapsamını sayıdan değil **isim deseninden** türet
*(ör. `test_b27b_*` Ç5'te olmak ZORUNDA)*, ya da tek dosyalı kriterlerde `-k`
kullanımını kaynak denetimiyle yasakla.

---

### 🔴 B-43 · B-27b'nin koruması iki ELLE YAZILMIŞ kümeyi karşılaştırıyor; küme bugün zaten YANLIŞ

**Nerede:** `tests/test_gozlem.py:321–346` (`ICERIK_TESTI_OLAN`) ↔ `sim/gozlem.py::HENUZ_ICERIK_TESTI_OLMAYAN`

**İDDİA (K-044):** *"Dördü de **bağımsız hesapla** karşılaştıran içerik
testine bağlandı; `gozlem.HENUZ_ICERIK_TESTI_OLMAYAN` beyanı eklendi
(B-06/B-10 deseninin üçüncüsü)."*

**ÖLÇTÜĞÜM — iki ayrı kusur:**

**(a) Liste, testlerin varlığından TÜRETİLMİYOR.** `ICERIK_TESTI_OLAN` elle
yazılmış bir küme değişmezidir; `HENUZ_ICERIK_TESTI_OLMAYAN` boş olduğu için
kontrol şuna indirgeniyor: *"iki dosyadaki iki elle yazılmış küme eşit mi?"*
Bir içerik testini devre dışı bıraktım *(fonksiyon adını
`DEVRE_DISI_b27b_kanal_mesgul_mu_bagimsiz_hesapla_ayni` yaptım)*:

```
17 passed in 42.93s     ← test_b27b_her_gozlem_alaninin_icerik_testi_var GEÇTİ
```

**(b) Liste zaten yanlış.** İki alan, içerik testi olduğu iddiasıyla listede,
ama **hiçbir içerik testi yok**:

| alan | `ICERIK_TESTI_OLAN`da | fiilen içerik testi |
|---|---|---|
| `olculen_gurultu_w` | ✅ var | ❌ **YOK** — dizgi `tests/` altında **yalnızca** bu küme satırında geçiyor |
| `paket` | ✅ var | ❌ **YOK** — `test_c5_2b`/`test_c5_2c` yalnızca **alan adlarını** sınıyor, değerleri değil |

**ÜRETİCİ KOMUT**
```bash
grep -rn "olculen_gurultu_w" tests/
```
```bash
cd scratchpad/den3/b27b && python -m pytest tests/test_gozlem.py -q
```

**beklenen / görülen** — beklenen: silinen bir içerik testi korumayı kırar ve
liste yalnızca gerçekten test edilen alanları içerir. görülen: koruma susuyor;
listede iki yanlış girdi var.

**Neden önemli** — `03` B5 bu ⭐ tuzağı adıyla sayıyor: *"etiketi elle taşımak
— elle yazılan etiket sessizce yanlışlaşır."* B-06 (`UYGULANMAMIS_BAYRAKLAR`)
ve B-10 (`rng.HENUZ_KULLANILMAYAN`) korumaları **davranışa** bağlıdır
*(bayrağı `True` yapmak istisna fırlatır; bir akış fiilen çekim alır)*.
B-27b'nin koruması **hiçbir davranışa bağlı değil** — bu yüzden desenin
üçüncüsü değil, desenin **görünüşüdür.**

**Öneri** — Kapsamı kümeden değil **testlerin kendisinden** türet *(ör. her
içerik testine `@icerik_testi("kanal_mesgul_mu")` işaretleyicisi; kontrol
işaretleyicileri toplasın)*. `olculen_gurultu_w` ve `paket` ya gerçek içerik
testine bağlansın ya `HENUZ_ICERIK_TESTI_OLMAYAN`a yazılsın.

---

### 🔴 B-44 · Karıştırıcıyı görebilen TEK gözlem alanı korumasız: sabitlense 284/284 test geçiyor

**Nerede:** `sim/kosucu.py::_gozlem_uret` — `olculen_gurultu_w=self.mac.olculen_gurultu_w(dugum)`

**ÖLÇTÜĞÜM (U14)** — Yalnızca **gözlemdeki** değeri sabit gürültü tabanına
çevirdim; `mac.olculen_gurultu_w` **dokunulmadı**, dolayısıyla beacon'ın
taşıdığı `bildirdigi_gurultu_w` doğru kalıyor:

```python
olculen_gurultu_w=self.radyo.gurultu_gucu_w,
```

| | |
|---|---|
| **Y8 — yol tetikleniyor mu** | **7 342 / 7 342 karar** *(%100)* tabandan farklı değer görüyor; aralık **1,67e−14 … 2,59e−12**, taban **1,59e−14** |
| tam paket | **284 passed** — 🔴 **sağ kaldı** |
| davranış *(48 koşuluk matris)* | **eşdeğer** — çünkü alanın **hiçbir tüketicisi yok** |

⚠️ Bu, ikinci denetimin **KM4** mutasyonunun *(“ölçülen gürültü karıştırıcıyı
görmüyor”, **yakalandı**)* biraz değiştirilmiş hâlidir — şüphe listesi #3'ün
tam cevabı. KM4'ü yakalayan test `test_d10b_beacon_gurultu_ve_kuyruk_bildiriyor`
idi; o test **beacon içeriğini** ölçüyor, gözlem alanını değil. **Kapanan şey
mutasyondu, mekanizma değil.**

**ÜRETİCİ KOMUT**
```bash
python scratchpad/den3/kostur2.py
```

**beklenen / görülen** — beklenen: karıştırmayı hisseden tek alanın
sabitlenmesi en az bir testi kırar. görülen: **0 test kırıldı**.

**Neden önemli** — H1.1'in bütün hikâyesi *"protokol gürültüden / ölü bağdan
kaçar"*. Bir protokolün karıştırıcıyı **kendi anteninden** hissedebileceği tek
kanal budur; içeriğinin doğru olduğunu gösteren hiçbir kayıt yok, ve
`ICERIK_TESTI_OLAN` var olduğunu **söylüyor** (B-43).

**Öneri** — `test_b27b_kanal_mesgul_mu_bagimsiz_hesapla_ayni` deseniyle bir
içerik testi: gözlemdeki değeri `radyo.gurultu_gucu_w + Σ girişim + karıştırıcı`
olarak **bağımsız** hesapla; Y8 gereği karıştırıcı payının >%5 olduğu kararları
ayrıca say.

---

### 🔴 B-45 · H1.1 mekanizma kapısının duyarlılık testi NULL MODEL sınavını geçmiyor

**Nerede:** `tests/test_mekanizma_kapisi.py::test_b30_sayac_bag_kalitesine_DUYARLI`

**İDDİA (K-044):** *"⭐ Sayaç ilk koşuda mekanizmayı AYIRT ETTİ … **4,7 kat
fark.** H1.1'in mekanizması artık ölçülebilir."*

**ÖLÇTÜĞÜM** — İlan edilen sayılar **birebir tuttu** *(kör %8,68 · kaçan
%1,86 · **4,68 kat** · ort. karar PER 0,3282 vs 0,0055)*. Sonra `03` B1'in
istediği şeyi yaptım: **aynı yapısal etkiyi üreten ama SIFIR bilgi taşıyan bir
null model** *(komşulardan birini belirlenimci sözde-rastgele seçer)* ve bağ
kalitesiyle **ilgisiz** bir gözlem alanına *(`bildirdigi_kuyruk`)* bakan
ikinci bir kol:

| aktarıcı | karar | **ara bölge %** | ölü bağ | ort. karar PER | teslim | ort. atlama |
|---|---|---|---|---|---|---|
| `en_kisa_yol` *(kalite körü, kâhin)* | 7 342 | **8,68** | 2 236 | 0,3282 | 0,2973 | 2,66 |
| `gurultuden_kacan` *(gürültü okur)* | 72 775 | **1,86** | 140 | 0,0055 | 0,1045 | 1,57 |
| 🔴 **NULL — rastgele komşu (sıfır bilgi)** | 62 610 | **0,27** | 582 | 0,0114 | 0,1016 | 1,25 |
| **NULL — kuyruğa göre (ilgisiz alan)** | 46 040 | **7,12** | 754 | 0,0311 | 0,0997 | 1,00 |

**Sıfır bilgi taşıyan kol, "gürültüden kaçan" koldan DAHA İYİ skor alıyor**
*(%0,27 < %1,86)*. Testin ölçütü `p_kor > 2 * p_kacan` null modelde de
sağlanıyor *(8,68 > 2 × 0,27)* — yani ölçüt, *"bu kol bağ kalitesi bilgisi
kullanıyor"* ile *"bu kol yakın komşulara dolanıyor"*u **ayırt edemiyor.**

İkinci kusur: testin `assert kor["olu_bag_karar"] > kacan["olu_bag_karar"]`
satırı **mutlak sayıları** karşılaştırıyor, oysa iki kolun karar sayısı
**7 342'ye karşı 72 775** — 10 kat. Oran cinsinden kör %30,5, kaçan %0,19.

**ÜRETİCİ KOMUT** — `scratchpad/den3/` null-model betiği; dört aktarıcı,
S2 / orta trafik / tohum 1.

**beklenen / görülen** — beklenen: bilgi taşımayan bir kolun kör kolla **aynı**
kovaya düşmesi. görülen: bilgi taşımayan kol **daha iyi** çıkıyor.

**Neden önemli** — `03` B1 bu tuzağı iki satırda birden sayıyor
*("mekanizma aktif" ≠ "mekanizma bilgi taşıyor"; null model kur)* ve `03` B4
*"kör mekanizma ölçütü — ölçütün, sorduğun soruya duyarlı olduğunu AYRICA
doğrula"* diyor. Sayaç **ön-kayıtlı bir kapıyı** besliyor: *"bu sayaç
düşmüyorsa sonuca bakılmaz."* Bugünkü hâliyle sayaç, kolun **ne kadar uzağa
gönderdiğini** ölçüyor — ara bölge bağları uzak bağlardır.

**Öneri** — Kapının duyarlılık testine bir **null kol** ekle: aynı sayıda karar
veren, aynı komşu kümesinden seçen, ama bilgiyi **karıştırılmış** kullanan bir
aktarıcı. Sayacı **karar başına oran** olarak karşılaştır. `06` H1.1'e şu
sınırı yaz: *sayaç yalnızca ortalama atlama sayısı ve karar sayısı
eşleştirilmiş kollar arasında okunur.*

---

### 🔴 B-46 · Karşılaştırma koruması KOD SÜRÜMÜNÜ denetlemiyor: aynı konfigten, farklı koddan gelen iki satır kabul ediliyor

**Nerede:** `sim/karsilastirma.py::ortak_alt_kume` ↔ `sim/kosucu.py::sonuc()` ↔ `v2/05-GOZLEM-PENCERESI.md` §E

**İDDİA (K-044, B-26 düzeltmesi):** iki parmak izi — `pencere_evren_hash` ve
`kurulum_hash` — *"6 yanlış kullanım reddediliyor, 4 meşru tedavi farkı kabul
ediliyor."*

**ÖLÇTÜĞÜM (Y11 — korumanın KAPSAMI DIŞINDA bir vaka)** — İki koşu, **birebir
aynı konfigürasyon ve tohum**, tek fark **simülatör kodu**: B kopyasında
`mac._onay_zaman_asimi`'ndeki ikili üstel geri çekilme kaldırıldı.

| | A *(değişmemiş kod)* | B *(geri çekilmesiz kod)* |
|---|---|---|
| `pencere_evren_hash` | `fbbb694789090614…` | `fbbb694789090614…` **aynı** |
| `kurulum_hash` | `bea7234dcb71d9d4…` | `bea7234dcb71d9d4…` **aynı** |
| `teslim_orani` | 0,2973 | 0,2961 |
| `mac_deneme` | 17 377 | 17 454 |
| **koruma** | — | 🔴 **KABUL ETTİ** |

```
>>> GUARD KABUL ETTI: ortak 794 paket (kesişim %98,4 birleşim, %29,4 pencere)
                      gecikme A=65,58 ms  B=73,35 ms
>>> gecikme farkı   : +7,76 ms
```

`05` §E'nin sonuç sözleşmesi **"Kod sürümü"**nü zorunlu alan sayıyor ve
`sim/results.py::kaynak_hash()` onu üretiyor — ama `Kosu.sonuc()` onu
**taşımıyor**, `ortak_alt_kume` da **sormuyor**.

**ÜRETİCİ KOMUT** — `scratchpad/den3/y11/` *(iki depo kopyası, aynı üretici
betik, `sim.karsilastirma.ortak_alt_kume` ile karşılaştırma)*.

**beklenen / görülen** — beklenen: iki kol yalnızca **tedavide** ayrılabilir;
kod farkı tedavi değildir. görülen: 7,76 ms'lik bir *"gecikme farkı"* üretildi.

**Neden önemli** — B-26'nın dersi *"koruma yalnızca yakalayabildiği durumla
sınanamaz"* idi ve düzeltme **konfigürasyon** eksenine yazıldı; **kod ekseni**
açık kaldı. Bu deponun kendi geçmişi riskin gerçek olduğunu gösteriyor: şema
**bir günde iki kez** değişti, ikinci denetim **dört bayat çıktı dosyası**
buldu, ve K-041 B-16/B-18'i yeniden ölçüp kalibrasyonu ölçmedi *(B-28)*.

**Öneri** — `Kosu.sonuc()`a `kaynak_hash` ekle *(şema Aile 1 başlamadan
donmalı — B-19'un kendi dersi)*; `ortak_alt_kume` farkı **kesişim oranı gibi
daima raporlasın**, `sim/` içeriği farklıysa `KarsilastirmaHatasi` en güvenli
varsayılandır.

---

### 🔴 B-47 · Aile 1'in ön-kayıtlı iki rakip protokolü BU ARAYÜZLE YAZILAMAZ

**Nerede:** `sim/kosucu.py::_beacon_at` · `sim/gozlem.py::PaketGorunumu` · `v2/05-GOZLEM-PENCERESI.md` §A2

**İDDİA:** `05` §A2 — *"Komşusunun girişim seviyesini veya kuyruk durumunu
kullanmak isteyen bir protokol, o alanları başlığa **koymak** ve bedelini
**ödemek** zorundadır."* · `dogrulama/aktaricilar.py` — `gurultuden_kacan`
*"gözlem penceresinin yeterli olduğunun kanıtı"*.

**ÖLÇTÜĞÜM — üç ayrı ölçüm:**

**(a) Protokolün bir çerçeveye bilgi koyma yolu yok.** Beacon içeriği
`Kosu._beacon_at` içinde **simülatör tarafından** sabitlenmiş
*(`gurultu_w`, `kuyruk`, `konum`)*; `KomsuKaydi` donmuş 6 alan; `PaketGorunumu`
donmuş 5 alan; protokol arayüzü `Gozlem → int | None`. Protokolün yazabildiği
tek yer `protokol_teshis`, o da **iletilmiyor** — yalnızca rapora girer. Yani
`05` §A2'nin *"başlığa koy, bedelini öde"* hakkının **kod karşılığı yoktur.**

**(b) Hedefin nerede olduğu gözlemde yok.** `PaketGorunumu.hedef` yalnızca bir
**kimlik**tir. Komşuların konumu beacon'dan gelir, ama düğüm **kendi konumunu
bile** bilmez ve hedefin konumunu hiçbir yerden öğrenemez. `hedefe_en_yakin`
bunu **kâhinden** alır (`_KAHIN_topoloji`).

**(c) Yazdım ve koşturdum.** Yalnızca `son_iletim_sonucu` + `son_iletim_hedefi`
+ `komsular` kullanan, düğüm başına Laplace düzeltmeli başarı oranı tutan bir
**ETX benzeri saf gözlem protokolü**:

| protokol | kâhin | teslim (S2) | ort. atlama (S2) | teslim (S0) |
|---|---|---|---|---|
| `en_kisa_yol` | EVET | 0,2973 | 2,66 | **0,9996** |
| `hedefe_en_yakin` | yarı | 0,2876 | 2,62 | — |
| `gurultuden_kacan` | hayır | 0,1045 | 1,57 | **0,1657** *(1 922 TTL ölümü)* |
| 🔴 **ETX — saf gözlem (yazdığım)** | hayır | **0,0997** | **1,00** | **0,0997** |

ETX kolu **karıştırıcısız S0'da da 0,0997** veriyor ve ortalama atlaması
**tam 1,00** — yani hiçbir paketi bir atlamadan öteye taşımıyor. Karıştırmanın
etkisi bu kolda ölçülemez, çünkü kol zaten çok atlamalı çalışmıyor.

**ÜRETİCİ KOMUT** — `scratchpad/den3/` ETX betiği *(S0 ve S2, orta trafik,
tohum 1)*.

**beklenen / görülen** — beklenen: pencere, atlama-sayısı ve bağ-kalitesi
temelli **iki rakibi** beslemeye yetiyor. görülen: pencereyle kurulabilen en
iyi şey **yerel bir rastgele yürüyüş**; iki rakibin ikisi de kurulamıyor.

**Neden önemli** — Ön-kaydın mühür sırası: *"2. YALNIZCA rakip kollar koşulur
→ tohumlar arası std ölçülür · 3. Eşikler ve güç analizi BU ÖLÇÜMDEN
hesaplanır → 🔒 26 Eylül 2026."* Adım 2 bugün **kurulamıyor**, ve bu bir takvim
sorunu değil **yapısal** bir sorun. `08` madde 22 dört alanın tüketicisi
olmadığını beyan ediyor; beyan edilmeyen şey **pencerenin çok atlamalı
yönlendirmeye yetmediği**. `aktaricilar.py`nin *"gözlem penceresinin yeterli
olduğunun kanıtı"* cümlesi ölçümle **desteklenmiyor** *(`03` kural 11)*.

**Öneri** — Karar vermeden önce **ölç ve seç**: (i) protokolün beacon'a alan
ekleyebildiği ve baytının sayıldığı bir kanal aç — `05` §A2'nin kod karşılığı;
ya da (ii) `05`i daralt ve H1.1'i açıkça *"yerel kaçınma"* sorusu olarak
yeniden yaz. Üçüncü yol yok, ve seçim **Aile 1 başlamadan** yapılmalı çünkü
ikisi de şemayı değiştirir.

---

### 🟠 B-48 · Ön-kayıtlı bant sonuç satırında SABİTLENEBİLİYOR; test yalnızca varsayılan değeri sınıyor

**Nerede:** `sim/kosucu.py::sonuc()` — `"ara_bolge_per_bandi": list(self.kon.ara_bolge_per_bandi)` ↔ `tests/test_mekanizma_kapisi.py::test_b30_band_on_kayitla_ayni_ve_tek_kaynakta`

**İDDİA (K-044):** *"Bant `Konfig.ara_bolge_per_bandi`de **tek yerde**. …
aynı hata tekrarlanmasın diye bant **sonuç satırında da** taşınıyor."*

**ÖLÇTÜĞÜM (U01)** — Alanı sabit `[0.05, 0.9]` yaptım:

| | |
|---|---|
| **Y8 — yol tetikleniyor mu** | Evet: `ara_bolge_per_bandi=(0.2, 0.7)` ile sayaç **637 → 320** değişiyor |
| tam paket | **284 passed** — 🔴 sağ kaldı |
| davranış *(48 koşuluk matris)* | eşdeğer — çünkü matriste **varsayılan dışı bant kullanan koşu yok** |
| **gizli sonuç** | varsayılan dışı bir bantla koşulduğunda sonuç satırı `[0.05, 0.9]` yazıyor, sayaç ise `(0.2, 0.7)` ile sayılmış |

```
_taban   : {"bant_alani": [0.2, 0.7], "ara_bolge_karar": 320}
U01_mutant: {"bant_alani": [0.05, 0.9], "ara_bolge_karar": 320}   ← satır YALAN söylüyor
```

Testin ölçütü `_kos()["ara_bolge_per_bandi"] == [0.05, 0.9]` — yani **yalnızca
varsayılan değeri** sınıyor, alanın `Konfig`ten **türediğini** değil. Y11.

**ÜRETİCİ KOMUT** — `scratchpad/den3/calisma/{_taban,U01_*}/_kanit.py`

**Neden önemli** — Bu alan tam olarak *"K-020'nin sayısı bandı yazmadığı için
yeniden üretilemedi"* diye eklendi. Bugünkü koruma, o hatanın tekrarını
engellemiyor.

**Öneri** — Teste varsayılan **dışı** bir bant ekle:
`Kosu(Konfig(..., ara_bolge_per_bandi=(0.2,0.7))).kostur()["ara_bolge_per_bandi"] == [0.2,0.7]`.

---

### 🟠 B-49 · `protokol_teshis` slotunun boru hattı korumasız — yazılan teşhis sessizce düşüyor

**Nerede:** `sim/kosucu.py::sonuc()` — `"protokol_teshis": dict(self.protokol_teshis)` ↔ `tests/test_mekanizma_kapisi.py::test_b30_protokol_teshis_slotu_acik_ve_bos`

**ÖLÇTÜĞÜM (U02)** — Alanı sabit `{}` yaptım:

| | |
|---|---|
| **Y8 — yol tetikleniyor mu** | Evet: slota yazan bir protokol tabanda `{"karar_sayisi": 7342}` üretiyor |
| tam paket | **284 passed** — 🔴 sağ kaldı |
| mutantta aynı protokol | `{}` — teşhis **sessizce kayboluyor** |

Mevcut test `s["protokol_teshis"] == {}` diye bakıyor; Aile 0'da doğru cevap
zaten `{}` olduğu için test **boruyu değil boşluğu** sınıyor. Slot,
*"şema Aile 1 başlamadan dondurulsun"* gerekçesiyle açıldı — ama açıldığı
hâliyle **hiç taşımadığı** kanıtlanabilir değil.

**ÜRETİCİ KOMUT** — `scratchpad/den3/calisma/{_taban,U02_*}/_kanit.py` ·
`python scratchpad/den3/kostur.py`

**Öneri** — Teste, slota yazan bir sahte protokolle **taşındığını** gösteren
bir vaka ekle *(`03` B5: bildirim ≠ kullanım)*.

---

### 🟠 B-50 · Ç1.4 kapı ölçütünün payı sessizce eksiltilebiliyor

**Nerede:** `sim/kosucu.py::sonuc()` — `"boruda_kalan": self.defter.kuyrukta + self.defter.ucusta` ↔ `dogrulama/aile0_kapi_raporu.py` Ç1.4

**ÖLÇTÜĞÜM (U05)** — Payı yalnızca `ucusta` yaptım:

| | |
|---|---|
| **Y8 — yol tetikleniyor mu** | Evet: 30 kurulumluk taramada 3'ünde `defter.kuyrukta > 0` *(S2/yoğun/1 · S2/orta/5 · S4/orta/5)*; `dongu_yapan` aktarıcısıyla 2 |
| tam paket | **284 passed** — 🔴 sağ kaldı |
| davranış *(48 koşuluk matris)* | 🔴 **DEĞİŞTİ — 6/48 koşu**, tek alan: `boruda_kalan` |

Ç1.4 *"boruda kalan < %1"* diyor ve mutasyon payı **küçültüyor** — yani kapıyı
**kolaylaştırıyor**, hiçbir test görmeden. `tests/test_kosucu.py` `boruda_kalan`
adını anıyor ama toplamın iki bileşenden oluştuğunu doğrulayan bir değişmez yok.

**ÜRETİCİ KOMUT**
```bash
python scratchpad/den3/kostur.py
```
```bash
python scratchpad/den3/etki_olc.py U05_boruda_kalan_eksik
```

**Öneri** — `boruda_kalan == defter.kuyrukta + defter.ucusta` değişmezini,
`kuyrukta > 0` olan bir kurulumda *(Y8)* teste bağla.

---

### 🟠 B-51 · Darbeli karıştırıcının parça sınırı FAZI ters çevrildiğinde 284/284 test geçiyor

**Nerede:** `sim/mac.py::_parca_sinirlari` — `t = (k + kesir - kj.faz_kesri) * p`

**ÖLÇTÜĞÜM (U11)** — İşareti `+` yaptım *(darbe trenini yanlış fazda kesen
parça sınırları)*:

| | |
|---|---|
| **Y8 — yol tetikleniyor mu** | Evet: S4/orta/tohum 1'de `_parca_sinirlari` **116 556** kez çağrılıyor, **8 293**'ünde ikiden fazla sınır dönüyor *(yani darbe dalı fiilen çalışıyor)* |
| tam paket | **284 passed** — 🔴 sağ kaldı |
| davranış *(48 koşuluk matris)* | 🔴 **DEĞİŞTİ — 8/48 koşu** *(S3/S4 darbeli koşuların hepsi)*, değişen alanlar: `ara_bolge_karar` · `beacon_alinan` · `beacon_gonderilen` · `beacon_kacirilan` · `en_yuksek_doluluk` · `islenen_olay` · `iyi_bag_karar` · `karar_bag_per_ortalama` |

Ç3.2 *(parça parça hesabın sabit girişimde tek parçayla aynı sonucu vermesi)*
tam olarak **sabit** girişimde koşuyor; darbe fazının doğru yerde kesildiğini
sınayan hiçbir test yok. H1.3 *(darbeli ↔ sabit, eşit ortalama güç)* bu hesaba
dayanıyor.

**ÜRETİCİ KOMUT**
```bash
python scratchpad/den3/kostur.py
```
```bash
python scratchpad/den3/etki_olc.py U11_darbe_faz_isareti_ters
```

**Öneri** — `acik_mi()` ile `_parca_sinirlari()`nin **aynı** geçiş anlarını
verdiğini gösteren bir değişmez testi: her sınır anında `acik_mi` değeri
değişmeli, sınır olmayan anlarda değişmemeli.

---

### 🟠 B-52 · B-36'nın düzeltmesi 7 girdinin yalnızca 2'sini kapsıyor; kalan 5'i elle `yol=None` ile kontrolü atlıyor

**Nerede:** `dogrulama/sag_kalan_ayikla.py::SagKalan.yol` · `SAG_KALANLAR`

**İDDİA (K-044):** *"`SagKalan.yol` alanı: karar artık yola bağlı;
tetiklenmemiş yolda **`❓ KARAR YOK`** veriliyor, *"eşdeğer"* değil."*

**ÖLÇTÜĞÜM** — Aracı koşturdum *(5,3 dk)*: **7/7 eşdeğer · davranışı değiştiren 0
· araç hatası 0** — ilan edilen sonuç **birebir tuttu** ve 7 desenin 7'si de
bugün dosyada tam olarak bir kez bulunuyor *(B-24 kapanmış)*. Ama:

| girdi | `yol` | yol matriste tetikleniyor mu |
|---|---|---|
| T01 `parca_siniri_carpisma` | **None** | tetiklenebilir bir yol var *(parça sınırı)* — kontrol atlanıyor |
| T02 `parca_siniri_darbe` | **None** | tetiklenebilir *(S4'te 8 293 çağrı)* — kontrol atlanıyor |
| T03 `assert_mesaji_metni` | **None** | gerçekten yolsuz *(metin)* ✅ |
| T04 `sira_sayaci_isareti` | `mac_kopya_alim` | ✅ tetikleniyor *(S2/yoğun'da 693)* — karar geçerli |
| T05 `sonuc_dizini_olusturma` | **None** | 🔴 `SonucYazici.__init__` bu matriste **hiç çağrılmıyor** — karar **verilemez** |
| T06 `ilet_jetonu_isareti` | **None** | jeton tekilliği; eşdeğerlik savunulabilir |
| T07 `yari_cift_yonlu_siniri` | `mac_basarisiz_alim` | ✅ tetikleniyor — karar geçerli |

**5/7 girdi `yol=None`** ve `_tetiklendi()` kontrolü onlar için **hiç
çalışmıyor**. T05, B-36'nın yazıldığı vakanın ta kendisi: matris yalnızca
`Kosu(...).kostur()` koşuyor, `sim/results.py` hiç ithal edilse bile
`SonucYazici` **hiç kurulmuyor** — yani *"bu matriste eşdeğer"* değil,
**"bu matriste hiç koşmadı"**.

**ÜRETİCİ KOMUT**
```bash
python -c "import sys;sys.path.insert(0,'.');from dogrulama.sag_kalan_ayikla import SAG_KALANLAR;print([(m.ad,m.yol) for m in SAG_KALANLAR])"
```
```bash
python dogrulama/sag_kalan_ayikla.py
```

**Neden önemli** — `yol` alanı **elle** dolduruluyor ve `None` olması hiçbir
şeyle doğrulanmıyor: `03` B5'in *"etiketi elle taşımak"* tuzağı, B-36'nın
düzeltmesinin içinde. Düzeltme çalışıyor, ama kapsadığı 2 girdide çalışıyor.

**Öneri** — `yol=None`u yasakla; her girdi ya bir sayaç adı taşısın ya
`yol="__yolsuz__"` gibi **açık** bir beyanla gerekçesini yazsın. T05 için
matrise `SonucYazici` kullanan bir koşu ekle ya da girdiyi listeden çıkar.

---

### 🟠 B-53 · `08` madde 22 "dört alan" diyor; ölçülen **dokuz** alan + bir türetilmiş özellik

**Nerede:** `v2/08-AILE0-KAPSAM.md` madde 22 ↔ `sim/gozlem.py::IZINLI_GOZLEM_ALANLARI`

**İDDİA:** *"**22** · Gözlem penceresinin **dört** alanının hiçbir TÜKETİCİSİ
yok *(`saat_s`, `kanal_mesgul_mu`, `kuyruk_uzunlugu`, `kuyruk_kapasitesi`)*."*

**ÖLÇTÜĞÜM** — `sim/` ve `dogrulama/` altındaki **üretici olmayan** her dosyada
`g.<alan>` deseni taradım:

| gözlem üyesi | tüketici |
|---|---|
| `dugum` · `komsular` · `paket` | ✅ `dogrulama/aktaricilar.py` |
| `saat_s` · `olculen_gurultu_w` · `kanal_mesgul_mu` · `kuyruk_uzunlugu` · `kuyruk_kapasitesi` · `son_iletim_sonucu` · `son_iletim_hedefi` · `gonderilen_bayt` · `alinan_bayt` | ❌ **YOK (9 alan)** |
| `Gozlem.kuyruk_doluluk` *(özellik)* | ❌ **YOK** — üretim yolunda **0 çağrı** ölçüldü |
| `KomsuKaydi.yas_s()` | ❌ yalnızca testten çağrılıyor |

`05` bu alanlardan birine *"⭐ EN ÖNEMLİ ALAN"* diyor *(`son_iletim_sonucu`)* ve
B-02 tam olarak onun için yazıldı — ama okuyan kimse yok.

**ÜRETİCİ KOMUT**
```bash
python -c "import sys,io,re,pathlib;sys.path.insert(0,'.');from sim.gozlem import IZINLI_GOZLEM_ALANLARI;d=[p for p in list(pathlib.Path('sim').rglob('*.py'))+list(pathlib.Path('dogrulama').rglob('*.py')) if p.name not in ('gozlem.py','kosucu.py')];[print(a,[p.as_posix() for p in d if re.search(r'(?<![\w.])(g|gozlem)\.'+a, io.open(p,encoding='utf-8').read())]) for a in sorted(IZINLI_GOZLEM_ALANLARI)]"
```

**beklenen / görülen** — beklenen 4, görülen **9 (+2)**.

**Öneri** — Maddeyi düzelt ve sayıyı **koddan türet** *(`08` bir sayı
taşıyacaksa üreticisi olmalı — `03` kural 1)*.

---

### 🟠 B-54 · Kontrol düzlemi ve kuyruk muhasebesi tamamen korumasız

**Nerede:** `sim/mac.py::yayin_gonder` *(`kacirilan_yayin`)* · `sim/queues.py::Kuyruk.ekle` *(`en_yuksek_doluluk`)*

**ÖLÇTÜĞÜM (U06, U07)** — İkisi de **sağ kaldı** ve ikisi de davranışı
**değiştiriyor**:

| mutasyon | Y8 tetiklenme | tam paket | 48 koşuluk matris |
|---|---|---|---|
| U06 · `en_yuksek_doluluk` bir eksik | S2/orta'da 3, S2/yoğun'da 3 | **284 passed** | 🔴 **48/48 koşu değişti** |
| U07 · `kacirilan_yayin` hiç artmıyor | S2/orta 52, S2/yoğun 91 | **284 passed** | 🔴 **39/48 koşu değişti** |

`grep -rn "en_yuksek_doluluk\|beacon_kacirilan" tests/` → **hiçbir eşleşme**.

`08` Ç5 KAPSAMAZ tablosu *"kontrol yükü eşitliği … ayrıca kontrol edilmeli"*
diyor; `kacirilan_yayin` **tam olarak** kontrol düzlemi bütçesinin fiilen
harcanıp harcanmadığını gösteren sayaçtır ve K-046'nın *"anlaşılmayan #4"*
cevabı *(beacon açlığı %0,00–%0,65)* bu sayaca dayanıyor.

**ÜRETİCİ KOMUT**
```bash
grep -rn "en_yuksek_doluluk\|beacon_kacirilan" tests/
```
```bash
python scratchpad/den3/etki_olc.py U06_en_yuksek_doluluk_bir_eksik U07_kacirilan_beacon_sayilmiyor
```

**Öneri** — İkisine de bağımsız hesapla değişmez testi: tepe doluluk
kuyruğun gözlenen en büyük uzunluğuna eşit; kaçırılan beacon =
üretilen beacon − gönderilen beacon − bekleyen.

---

### 🟠 B-55 · Beacon'ın BAYT maliyeti içeriğinden bağımsız — `05` §A2 kural 1'in kod karşılığı yok

**Nerede:** `sim/kosucu.py::_beacon_at` — `self.mac.yayin_gonder(dugum, self.kon.beacon_bayt, icerik)`

**İDDİA:** `05` §A2, kural 1: *"Başlıktaki her alan **bayt olarak sayılır** ve
kontrol yüküne yazılır."*

**ÖLÇTÜĞÜM** — `icerik` keyfi bir sözlük; maliyet **sabit** `kon.beacon_bayt = 32`.
İçeriği tamamen boşalttım *(U15: `"konum": None`)*: `kontrol_bayt` **birebir
aynı** kaldı. Yani beacon'a alan eklemenin ya da çıkarmanın kontrol yükü
muhasebesinde **hiçbir karşılığı yok**.

Bugün zararsız *(içerik `sim/` tarafından sabitlenmiş)*, ama B-47 ile birlikte
okununca yönü belli: `05` §A2'nin verdiği hak uygulanırsa, bedeli **hiçbir yerde
tahsil edilmiyor** olacak — ve `08` madde 13 aynı riski yalnızca **zaman
damgası** için beyan ediyor.

**ÜRETİCİ KOMUT**
```bash
python -c "import sys;sys.path.insert(0,'.');from sim.config import Konfig;from sim.kosucu import Kosu;from dogrulama.aktaricilar import en_kisa_yol;s=Kosu(Konfig(kol='t',senaryo='S2',trafik='orta',tohum=1),en_kisa_yol).kostur();print(s['kontrol_bayt'], s['beacon_gonderilen'], Konfig(kol='t').beacon_bayt)"
```

**Öneri** — `beacon_bayt`ı içerikten **türet** *(alan başına sabit maliyet
tablosu)* ya da `08`e madde ekle: *"beacon bayt maliyeti sabittir ve içeriğe
duyarsızdır; `05` §A2'nin 'bedelini öde' kuralı kodda zorlanmaz."*

---

### ⚪ B-56 · K-020'nin *"133 bağın 11–17'si ara bölgede"* sayısı hâlâ üreticisiz ve bandsız; üç sayma kuralı üç farklı sayı veriyor

**Nerede:** `v2/04-NEDEN-BOYLE.md` K-020

**İDDİA:** *"133 bağın yalnızca 11–17'si ara bölgede."* Üretici komut **yok**,
bant **yazılı değil**, karıştırıcının açık olup olmadığı **yazılı değil**,
bağın yönlü sayılıp sayılmadığı **yazılı değil**.

**ÖLÇTÜĞÜM (tohum 1, ön-kayıtlı bant 0,05 ≤ PER ≤ 0,9):**

| sayma kuralı | menzil içi bağ | ara bölge |
|---|---|---|
| yönsüz · karıştırıcısız | **133** | **6** ← ikinci denetimin bulduğu |
| yönlü · karıştırıcısız | 266 | 12 |
| **yönsüz · karıştırıcı AÇIK (t=0)** | **133** | **13** ← *"11–17"* aralığına giren **tek** okuma |
| yönlü · karıştırıcı açık | 266 | 24 |

10 tohumda *(yönsüz, karıştırıcı açık)* aralık ≈ **13–30** — yani *"11–17"*
tohum 1'e özgü. İkinci denetim *"yeniden üretemedim"* demişti; **üretilebiliyor
— ama yazılmamış üç varsayımı doğru tahmin etmek şartıyla.**

**ÜRETİCİ KOMUT** — `Topoloji.uret` + `Radyo.paket_hata_olasiligi` +
`Karistirici.senaryodan`, tohum 1–10, dört sayma kuralı.

**Öneri** — K-020'yi revizyonla düzelt: bant · karıştırıcı durumu · yön
kuralı · tohum yazılsın; ya da sayıyı kaldır. B-30'un kendi önerisi buydu ve
**yapılmadı**.

---

### ⚪ B-57 · Karar kayıtlarında üretici komut oranı DÜZELMEDİ

**ÖLÇTÜĞÜM:** 46 kaydın **31'inde** *"Üretici"* satırı yok.
*(İkinci denetim 43 kaydın 30'unda yok demişti — %70 → %67, yani üç yeni
kaydın ikisi üreticiyle geldi ama eski 30 kaydın hiçbiri düzelmedi.)*

Üretici satırı olmayanlar: K-001…K-016, K-018, K-020, K-021, K-023…K-029,
K-031, K-033, K-036, K-041, K-045.

**ÜRETİCİ KOMUT**
```bash
python -c "import io,re;s=io.open('v2/04-NEDEN-BOYLE.md',encoding='utf-8').read();p=re.split(r'(?m)^# (K-\d+)',s);k=[(p[i],p[i+1]) for i in range(1,len(p),2)];print(len(k),sum('retici' not in b for _,b in k))"
```

**Öneri** — `03` kural 1 bir *"asla ihlal edilmeyecek kural"*. En azından
**sayı içeren** kayıtlar için üretici satırı zorunlu hâle getirilmeli; kalanlar
*"sayı içermez"* diye açıkça işaretlenmeli.

---

### ⚪ B-58 · `_kurulum_hash`'teki ayraç hiçbir şey yapmıyor — bağımsız olarak bulundu, ve bugün **sömürülemez** olduğu ölçüldü

**Nerede:** `sim/kosucu.py::_kurulum_hash` — `h.update(b"")`

Bunu K-046'nın *"açık bırakılan bulgu"* notunu okumadan önce koddan buldum;
örtüşmenin kendisi bir ölçüdür *(kayıt bunu açıkça istiyor)*.

**EKLEDİĞİM ÖLÇÜM** — Kayıt *"bugün çakışma üretmiyor"* diyor; bunun **neden**
böyle olduğunu ölçtüm: çakışma ancak bir alan değerinin bir sonraki **alan
adını** yutmasıyla olur. `Konfig`in serbest metin alanlarının **üçü de**
(`kol`, `not_`, ayrıca `senaryo`) `TEDAVI_ALANLARI` içinde olduğu için hash'e
hiç girmiyor; `trafik` `__post_init__`te kapalı bir kümeye kısıtlı; kalan tüm
alanlar sayısal/bool ve alan adları sabit ve sıralı. Yani bugün çakışma
**yapısal olarak imkânsız** — kayıt haklı, ama gerekçesi yazılı değil.

**Öneri** — Düzeltilirken gerekçe de yazılsın: *ayraç, ileride hash'e serbest
metin taşıyan bir alan girdiğinde gerekli olacak.*

---

### ⚪ B-59 · İki küçük kayıt hatası: *"6 yanlış kullanım"* aslında 7; `06`'nın durum bloğu bayat

**(a)** K-044: *"**6 yanlış kullanım** reddediliyor *(dugum_sayisi · menzil ·
alan · tohum · kuyruk · TTL · paket_bayt)*"* — parantez içinde **yedi** öğe var
ve `tests/test_karsilastirma.py::KIRILMASI_GEREKEN` **7** girdi taşıyor.

**(b)** `v2/06-ON-KAYIT.md`, Aile 0 durum bloğu: *"**40/40 kapalı**, kapı
raporu yeniden **koşulacak**."* Kapı 20 Ağustos'ta koşuldu ve **13/13** geçti
*(K-046, `09-DEVIR-TESLIM.md` da böyle yazıyor)*. İki belge çelişiyor.

**ÜRETİCİ KOMUT**
```bash
python -c "import sys;sys.path.insert(0,'.');sys.path.insert(0,'tests');import importlib.util as u;s=u.spec_from_file_location('t','tests/test_karsilastirma.py');m=u.module_from_spec(s);s.loader.exec_module(m);print(len(m.KIRILMASI_GEREKEN), len(m.KABUL_EDILMESI_GEREKEN))"
```

---

### ⚪ B-60 · `yeni_olcut(..., ulasilabilirlik=None)` kısıtı SESSİZCE atlıyor

**Nerede:** `dogrulama/kurulum_kalibrasyonu.py:375–408`

B-29 kapandı: kısıt koda girdi, `bolum_c` gerçek değerleri geçiyor
*(satır 524)* ve `tests/test_kalibrasyon.py::test_b29_*` iki yönlü sınıyor.
Ama varsayılan `None` **kısıtın tamamen atlanması** demek ve bunu zorlayan
hiçbir kaynak denetimi yok — B-29'un kendi hata sınıfının zayıflatılmış hâli.
Docstring *"YALNIZCA birim testleri için"* diyor; bu bir **yorum**, koruma değil.

**Öneri** — Argümanı zorunlu yap; birim testleri kısıtı devre dışı bırakmak
için açık bir `ULASILABILIRLIK_YOK` nöbetçisi geçsin.

---

### ⚪ B-61 · U12 *"yakalandı"* ama kıran iki test de İLGİSİZ — trafik çifti seçimi korumasız

**Nerede:** `sim/traffic.py::_ciftleri_sec` — `secilen = self._rnd_cift.sample(aday, istenen)`

Çift seçimini `sorted(aday)[:istenen]` yaptım *(kaynak-hedef çiftleri artık
en küçük numaralı düğümlerden — klasik bir `03` B6 kurulum hatası)*.
**3 test kırıldı**, ama bulabildiğim ikisi:

| kırılan test | ne ölçüyor |
|---|---|
| `test_b19_ortak_alt_kume_secilim_yanliligini_ortaya_cikariyor` | gecikme yanlılığı |
| `test_kosucu.py::test_bosaltma_boruyu_bosaltiyor` | boşaltma penceresi |

İkisi de **trafik çiftlerinin rastgele seçildiğiyle ilgisiz**. İkinci
denetimin KM9/KM10 için yazdığı *"yakalandı ≠ korundu"* uyarısının üçüncü
örneği: mutasyon skoru olduğundan iyi görünüyor.

**ÜRETİCİ KOMUT**
```bash
python scratchpad/den3/kiran.py
```

**Öneri** — `trafik.ozet()`in `farkli_kaynak`/`farkli_hedef` alanlarına
dayanan bir değişmez: seçilen çiftler tüm düğüm uzayına yayılmalı, ilk
N düğüme yığılmamalı.

---

### ⚪ B-62 · Kopya alımların baytları `alinan_bayt` gözlemine girmiyor — ve kimse fark etmiyor

**Nerede:** `sim/mac.py::_veri_bitti` — `self.dugum_alinan_bayt[alici] += il.paket.bayt`

**ÖLÇTÜĞÜM (U13)** — Satırı kopya olmayan dala taşıdım *(kopya alımlar
sayılmıyor)*:

| | |
|---|---|
| **Y8 — yol tetikleniyor mu** | Evet: S2/yoğun'da **693** kopya alım, S5/yoğun'da 1 393 |
| tam paket | **284 passed** — 🔴 sağ kaldı |
| davranış *(48 koşuluk matris)* | eşdeğer — çünkü `alinan_bayt`ın **tüketicisi yok** |

`test_b01_bayt_alanlari_dugume_ait_aga_degil` yalnızca **gönderilen** tarafa
değişmez kuruyor *(`sum(dugum_gonderilen_bayt) == veri_bayt + kontrol_bayt`)*;
**alınan** taraf için karşılık gelen bir değişmez yok.

**Öneri** — Alınan bayt için de bir değişmez: düğüm başına alınan bayt toplamı,
MAC'in kaydettiği başarılı alım sayılarıyla tutarlı olmalı.

---

### ⚪ B-63 · Aynı büyüklük iki farklı sayıyla: +6 dBm ulaşılabilirliği %84,8 mi %84,0 mı

**Nerede:** `sim/config.py` ana tablo ↔ `sim/config.py` K-039 bloğu ↔ `v2/06-ON-KAYIT.md`

| kaynak | +6 dBm ulaşılabilirlik | örneklem |
|---|---|---|
| `config.py` ana tablo | **%84,8 ± 2,6** | 30 ayarlama tohumu *(Bölüm B)* |
| `config.py` K-039 bloğu + `06` | **%84,0** | 5 tohum *(Bölüm C, 1·7·13·19·23)* |

İkisini de yeniden ürettim; ikisi de **doğru** — ama `06`'da aynı blokta
*"Ulaşılabilir çift %97,0"* *(30 tohum)* ile *"kısıtla elenen +6 dBm (%84,0)"*
*(5 tohum)* yan yana duruyor ve hangisinin hangi örneklemden geldiği
**yazılı değil**.

**ÜRETİCİ KOMUT**
```bash
python dogrulama/kurulum_kalibrasyonu.py
```

**Öneri** — Her iki sayının yanına tohum sayısını yaz; ya da kısıtı da
30 tohumluk tabloda değerlendir.

---

### ⚪ B-64 · `CIKTILAR.md`'nin kendi kuralını hayatta kalan üç çıktı dosyası ihlal ediyor

**Nerede:** `CIKTILAR.md` ↔ `ayikla_cikti.txt` · `kor_cikti.txt` · `kalibrasyon_c.txt`

B-39 kapandı: `_x.py` ve dört bayat çıktı **silinmiş**, politika belgesi
**yazılmış**. Politikanın kuralı şu: *"bir çıktı dosyası, üretildiği koşunun
tarihini ve o koştuğu kod durumunu taşımıyorsa **silinir**."*

**ÖLÇTÜĞÜM** — Kalan üç dosyanın hiçbiri tarih taşımıyor; biri zaten bayat:

| dosya | tarih | kod durumu | bugün geçerli mi |
|---|---|---|---|
| `ayikla_cikti.txt` | ❌ yok | ❌ yok | içerik bugünkü koşumla uyuşuyor *(7/7 eşdeğer)* |
| `kor_cikti.txt` | ❌ yok | **271 passed** | ❌ **bayat** — taban bugün **284** |
| `kalibrasyon_c.txt` | ❌ yok | ❌ yok | Bölüm C sayıları bugün tutuyor |

`kor_cikti.txt` tam olarak B-25'in örüntüsü: bir skor, ait olduğu **test paketi
büyüklüğüyle** birlikte anlamlı ve o büyüklük değişmiş.

**ÜRETİCİ KOMUT**
```bash
grep -niE "2026|passed" ayikla_cikti.txt kor_cikti.txt kalibrasyon_c.txt
```

**Öneri** — Üç dosyanın başına *"üretildiği tarih + `python -m pytest tests -q`
taban sayısı"* satırı; ya da politikanın gereği olarak silinsinler.

---

## 2. İKİNCİ DENETİMİN 17 BULGUSU — kapanma doğrulaması

İstenen alt sınır 8; **on yedisini de** tek tek sınadım. *"Mutasyonla sınadım"*
sütunu, kapanışın testine bağımsız bir mutasyon uygulayıp testin gerçekten
kırıldığını *(ya da kırılmadığını)* gösterdiğim yerdir.

| # | Kapanış iddiası | Nasıl doğruladım | Sonuç |
|---|---|---|---|
| **B-24** | `arac_hatasi` ayrı kovada; satır numaraları üretimden | 7 girdinin 7'sinin deseni bugün dosyada **tam bir kez** bulunuyor; `_satir_no` gerçek satırları veriyor; aracı koşturdum: **araç hatası 0** | ✅ **kapandı** |
| **B-25** | Kör tarama yeniden koşuldu; `08` tarihli tablo taşıyor | `mutantlari_uret()` → **203** *(kayıtla aynı)*; `08` iki satırlı tarihli tablo ve *"iki skor karşılaştırılamaz"* notu taşıyor | ✅ **kapandı** *(skorun kendisi yeniden koşulmadı — §4)* |
| **B-26** | İki parmak izi; 6 yanlış kullanım red, 4 tedavi kabul | `test_karsilastirma.py` **20/20** geçiyor; listede **7** red vakası var *(K-044 "6" diyor → B-59)*. 🔴 **Y11 ile KIRDIM:** aynı konfig + **farklı kod** çifti kabul ediliyor | ⚠️ **kısmen** → **B-46** |
| **B-27** | Örüntü kapanmadı; kapanış metni düzeltildi | 15 yeni bağımsız mutasyon; **10 sağ kaldı (%66,7)**; ilk 10'da **7/10** | ⚠️ **iddia doğru, örüntü hâlâ açık** |
| **B-27b** | Dört alan bağımsız hesapla içerik testine bağlandı | 🔴 Koruma **iki elle yazılmış kümeyi** karşılaştırıyor; içerik testini sildim → **17 passed**, koruma sustu. Liste **zaten yanlış** *(`olculen_gurultu_w`, `paket`)*. Ve KM4'ün türevi **U14 sağ kaldı** | 🔴 **KAPANMADI** → **B-43, B-44** |
| **B-28** | Kalibrasyon yeniden ölçüldü; +2 dBm değişmedi | `kurulum_kalibrasyonu.py` koşturuldu: **0,5252 · [0,1197 · 0,8955] · 0,5076 · 0,0176 · +2 dBm** — dördü de birebir | ✅ **kapandı** |
| **B-29** | Kısıt koda girdi; `bolum_c` ölçüp geçiriyor | `yeni_olcut(egri, ulasilabilirlik)` kısıtı uyguluyor *(satır 403–406)*; `bolum_c` gerçek değerleri geçiyor *(satır 524)*; koşuda **+6/+8/+10/+11 eleniyor**. ⚠️ Varsayılan `None` kısıtı sessizce atlıyor | ✅ **kapandı** *(kalıntı: B-60)* |
| **B-30** | Sayaç şemaya eklendi; bant tek yerde | Beş alan + bant + slot şemada; toplamlar paydayı tüketiyor. 🔴 **Duyarlılık testi null model sınavını geçmiyor**; bant alanı **sabitlenebiliyor**; K-020'nin sayısı **yeniden ölçülmedi** | ⚠️ **kısmen** → **B-45, B-48, B-56** |
| **B-31** | `08` madde 21 beyan edildi | Madde 21 var; `grep wilcoxon|holm|scipy` → **hiçbir eşleşme** *(beyan doğru)*. Ön-kaydın NaN tuzağını da doğruladım: n=10 → p=1,0; **n=30 → p=nan** | ✅ **kapandı** *(beyan olarak)* |
| **B-32** | `BEKLENEN_MUTASYON = 35` sabiti eklendi | 🔴 **Böyle bir sabit YOK.** Eşik hâlâ `{toplam}/{toplam}`; kapının gerçek kod yolu liste 5'e düştüğünde **"5/5 · OK · 13/13"** diyor | 🔴 **KAPANMADI** → **B-41** |
| **B-33** | `07`nin akış tablosuna `beacon_faz` eklendi; Li 1/6,29 | `grep beacon_faz v2/07-*` → **2 eşleşme**; `"1/6,0"` **kalmamış** | ✅ **kapandı** |
| **B-34** | `08` Ç1 tablosu düzeltildi; 35 hedefli | `08` dördüncü uç durumu `rota_yok` yazıyor ve düzeltmeyi kayda geçiriyor; *"35 hedefli"* güncel *(ölçüldü: 35)* | ✅ **kapandı** |
| **B-35** | `abs=0.0` eklendi | `tests/test_radio.py:116–117` → `pytest.approx(..., rel=1e-9, abs=0.0)` | ✅ **kapandı** |
| **B-36** | `SagKalan.yol`; tetiklenmemiş yolda `❓ KARAR YOK` | Mekanizma çalışıyor, ama **7 girdinin 5'i `yol=None`** ve kontrolü atlıyor; T05'in yolu bu matriste **kesinlikle** koşmuyor ve yine *"eşdeğer"* damgası alıyor | ⚠️ **kısmen** → **B-52** |
| **B-37** | `08` madde 17–20 eklendi | Dört madde de var; 18. madde *(tek/merkezî karıştırıcı)* **"hipotezin lehine"** yönüyle yazılmış. Kodla doğruladım: `Karistirici.senaryodan` **tek** nesne kuruyor, `karistirici_merkez` varsayılanı alanın merkezi | ✅ **kapandı** |
| **B-38** | `faz_s` → `faz_kesri` *(19 yerde)* | `grep -rn "faz_s" sim/ dogrulama/ tests/` → `faz_kesri` dışında **hiçbir eşleşme** | ✅ **kapandı** |
| **B-39** | `_x.py` ve beş bayat çıktı silindi; `CIKTILAR.md` yazıldı | `_x.py` ve dördü **yok**; politika belgesi var. ⚠️ Kalan üç dosya politikanın kendi kuralını ihlal ediyor | ⚠️ **kısmen** → **B-64** |

**Özet:** 17 bulgunun **10'u tam kapandı**, **5'i kısmen**, **2'si kapanmadı**
*(B-27b · B-32)*. Kapanmayan ikisi de aynı sınıftan: **düzeltme kodda yerini
almadı ya da davranışa bağlanmadı.**

### 🔴 Testleri mutasyonla sınadım — biri fazla dar çıktı

Şüphe listesi #3'ün istediği *"mutasyonu biraz değiştir"* denemesi:

| kapanışın testi | denetçinin mutasyonu | benim türevim | sonuç |
|---|---|---|---|
| `test_d10b_beacon_gurultu_ve_kuyruk_bildiriyor` | KM4: `mac.olculen_gurultu_w` karıştırıcıyı görmüyor → **yakalandı** | U14: **yalnızca `Gozlem.olculen_gurultu_w`** sabitleniyor, beacon bozulmuyor | 🔴 **SAĞ KALDI** — test beacon içeriğini koruyor, gözlem alanını değil |
| `test_d10_beacon_gercek_konum_bildiriyor` | D10: beacon herkese `(0,0)` bildiriyor | U15: beacon `konum=None` bildiriyor | ✅ **yakalandı** — koruma gerçek |
| `test_b30_*` *(mekanizma kapısı)* | — | U03: `bag_gercek_per` yönü ters | ✅ **yakalandı** *(`…monoton_kotulesiyor`)* |
| `test_km3_yorunge_yonu_kapali_formla_ayni` | KM3 | *(kod incelemesi)* — "bağımsız hesap" **üretici ifadenin birebir tekrarı**; testi bağlayan şey yalnızca sondaki **yön** iddiası | ⚠️ dar ama **yön** için bağlayıcı |

---

## 3. DOĞRULANAN İDDİALAR

Aşağıdakileri kendim koşturdum ve **tuttular**.

| iddia | ilan | ölçtüğüm | üretici komut |
|---|---|---|---|
| Test paketi | 284 *(17 dosya)* | **284 passed in 340,49 s** | `python -m pytest tests -q` |
| Hedefli mutasyon | 35 | **35** | `from dogrulama.mutasyon_paketi import MUTASYONLAR` |
| Kör mutant havuzu | 203 | **203** | `from dogrulama.kor_mutasyon import mutantlari_uret` |
| Karar kaydı | 46 | **46** | `grep -c "^# K-0" v2/04-NEDEN-BOYLE.md` |
| Kapsam maddesi | 22 | **22** | `08` numaralı liste taraması |
| Kapı beklenen test sayıları | 6 / 44 / 18 / 6 / 2 | **6 / 44 / 18 / 6 / 2** — beşi de **güncel** | `pytest <yol> -k <seçim> --collect-only -q` |
| S2 teslim | 0,5252 | **0,5252** | `python dogrulama/kurulum_kalibrasyonu.py` |
| Dinamik aralık · orta | [0,1197 · 0,8955] · 0,5076 | **birebir** | aynı |
| Kısıtla elenen güçler | +6 (%84,0) · +8 (%73,3) · +10 (%57,1) · +11 (%49,1) | **birebir** | aynı |
| Derece kayması | −%0,364 ± 0,026 | **−%0,364 ± 0,026** *(doğal bağlantı %82,93 · ort. deneme 1,2058 · analitik derece 7,44258 vs ölçülen 7,44242)* | `python dogrulama/kurulum_kalibrasyonu.py --a` |
| Li platosu · GA | 1/6,29 · %2,04 | **1/6,29 · %2,04** *(tek atlama 932,0 kbps)* | `plato_olc(TOHUM_TAM)` |
| Mekanizma sayacı | %8,68 vs %1,86 *(4,7 kat)* | **%8,68 vs %1,86 — 4,68 kat** | `Kosu(...).kostur()`, iki aktarıcı |
| Ort. karar PER'i | 0,3282 vs 0,0055 | **0,3282 vs 0,0055** | aynı |
| Sağ kalan ayıklaması | 7/7 eşdeğer · davranışı değiştiren 0 | **7/7 eşdeğer · 0 değişen · 0 araç hatası** *(5,3 dk)* | `python dogrulama/sag_kalan_ayikla.py` |
| Parmak izi koruması | 6 red · 4 kabul | **7 red · 4 kabul**, 20/20 test geçiyor | `pytest tests/test_karsilastirma.py -q` |
| K-020 bağ geçişi | %0,03 / %17 / %52 / %100 · 2,8 dB | **%0,03 / %16,97 / %51,60 / %100 · 2,79 dB** | `Radyo.menzilde_per` + `sinr_db` |
| Ön-kaydın NaN tuzağı | *"tüm farklar sıfırken NaN"* + *"örneklem boyutuna bağlı"* | **n=5 → 1,0 · n=10 → 1,0 · n=30 → nan** | `scipy.stats.wilcoxon([0.0]*n)` |
| `mutasyon_on_kontrol` seçim keskinliği | *(iddia yok)* | 35 mutasyonun **34'ü** `-k` ile **tam 1** test topluyor; biri parametrize *(4)* | 35 × `pytest --collect-only -k` |

**Ayrıca ölçtüğüm ve TEMİZ çıkan iki mekanizma:**

1. **Kâhin sayaç RNG çekmiyor.** `mac.bag_gercek_per` tamamen belirlenimci
   *(mesafe + karıştırıcı gücü)*; B-30'un şema değişikliği RNG çekim sırasını
   **kaydırmıyor** — bu, B-28'in *(`beacon_faz` kayması)* tekrarı olabilirdi.
2. **Yarı çift yönlü muhasebesi kaçak vermiyor.** `mac.gonderim_araligi`
   yalnızca **son** iletimi tutuyor; her alıcının **tüm** iletimlerini ayrıca
   kaydedip karşılaştırdım: **134 151** alım değerlendirmesinde *"gerçek
   örtüşme var ama `gonderim_araligi` görmedi"* vakası **0**.

---

## 4. ÜRETİLEMEYEN İDDİALAR

| iddia | durum |
|---|---|
| K-020 · *"133 bağın yalnızca **11–17**'si ara bölgede"* | Üretici komut **yok**, bant **yok**, karıştırıcı durumu **yok**, yön kuralı **yok**. Dört makul okumadan **yalnızca biri** (yönsüz · karıştırıcı açık · tohum 1) aralığa giriyor: **13**. Diğerleri 6 · 12 · 24. → **B-56** |
| Kör tarama skoru %55,6 *(10/18)*, taban **271 test** | **Yeniden koşulmadı** *(18 dk)* — ve `08` zaten *"iki skor karşılaştırılamaz, bu bir kod durumu fotoğrafıdır"* diyor. Taban bugün **284**, yani sayı tanım gereği bayat. `kor_cikti.txt` bunu hâlâ 271 ile taşıyor → **B-64** |
| K-044 · *"**6** yanlış kullanım reddediliyor"* | Kodda **7** vaka var → **B-59** |
| `08` madde 22 · *"**dört** alanın tüketicisi yok"* | Ölçüldü: **dokuz** alan + `kuyruk_doluluk` → **B-53** |
| `06` · *"kapı raporu yeniden **koşulacak**"* | Koşuldu ve geçti *(K-046)* → **B-59** |
| `aktaricilar.py` · `gurultuden_kacan` *"gözlem penceresinin yeterli olduğunun kanıtı"* | Ölçüldü: karıştırıcısız S0'da teslim **0,1657**, **1 922** TTL ölümü. Kanıt değil → **B-47** |
| Ç1.1 · 540/540 · Ç1.2 · 4/4 · Ç1.4 · %0,156 · Ç1.3 · 35/35 | **Koşturmadım** *(540 koşu + 35 mutasyon ≈ 45 dk)*. İkinci denetim bunları bağımsız olarak üretmişti; ben yalnızca **eşiklerinin** nasıl kurulduğunu denetledim → §8 |

---

## 5. 🔴 KENDİ MUTASYONLARIM

**15 yeni mutasyon**, her biri `shutil.copytree` kopyasında, her biri **tam
284 testlik paketle** *(5 paralel; toplam ~50 dk)*. Hiçbiri mevcut 35 hedefli
mutasyonun ya da 203 mutantlık kör havuzun tekrarı değil; hiçbiri birinci
denetimin D1–D10'u ya da ikinci denetimin KM1–KM10'u değil.

Her mutasyon için **Y8 önce uygulandı**: bozduğu yolun sağlam koşuda
tetiklendiği ölçüldü. Her mutasyon uygulandıktan sonra **kodda yeniden
okunarak** doğrulandı ve `ast.parse` ile sözdizimi denetlendi *(`03` kural 15)*.

| # | mutasyon | dosya | **Y8 · sağlam koşuda tetiklenme** | 284 test | davranış *(48 koşuluk matris)* |
|---|---|---|---|---|---|
| **U01** | `ara_bolge_per_bandi` sabit kodlanıyor | `kosucu.py` | özel bantla sayaç **637 → 320** | 🔴 **sağ kaldı** | ⚪ tüketicisiz — ama satır **yalan söylüyor** *(B-48)* |
| **U02** | `protokol_teshis` → `{}` | `kosucu.py` | yazan protokol tabanda **7 342** kayıt üretiyor | 🔴 **sağ kaldı** | ⚪ tüketicisiz *(B-49)* |
| **U03** | `bag_gercek_per` **yönü ters** | `kosucu.py` | **7 342/7 342** çağrı yön-asimetrik *(%100)* | ✅ yakalandı | `test_b30_karar_bag_kalitesi_…monoton_kotulesiyor` — **ilgili** |
| **U04** | gecikme yerine **mutlak teslim anı** | `kosucu.py` | `ortak_alt_kume` tüketiyor *(A = 55,41 ms)* | ✅ yakalandı | `test_b19_ortak_alt_kume_secilim_yanliligini_ortaya_cikariyor` — **ilgili** |
| **U05** | `boruda_kalan` = yalnızca `ucusta` | `kosucu.py` | 30 kurulumun **3'ünde** `kuyrukta > 0` | 🔴 **sağ kaldı** | 🔴 **DEĞİŞTİ 6/48** — Ç1.4 kolaylaşıyor *(B-50)* |
| **U06** | `en_yuksek_doluluk` bir eksik | `queues.py` | S2/orta **3**, S2/yoğun **3** | 🔴 **sağ kaldı** | 🔴 **DEĞİŞTİ 48/48** *(B-54)* |
| **U07** | `kacirilan_yayin` hiç artmıyor | `mac.py` | S2/orta **52**, S2/yoğun **91** | 🔴 **sağ kaldı** | 🔴 **DEĞİŞTİ 39/48** *(B-54)* |
| **U08** | ikili üstel geri çekilme yok | `mac.py` | **15 642** cw büyüme olayı | ✅ yakalandı | `test_cw_ikili_ustel_buyuyor` *(+1 test daha)* — **ilgili** |
| **U09** | `Gozlem.kuyruk_doluluk` iki kat yanlış | `gozlem.py` | 🔴 üretim yolunda **0 çağrı** | 🔴 **sağ kaldı** | ⚪ tüketicisiz — B-27b'nin **kapsamı dışında** *(B-53)* |
| **U10** | Ç5 seçimi sessizce daralıyor | `aile0_kapi_raporu.py` | kapı seçimi her koşuda okunuyor | 🔴 **sağ kaldı** | 🔴 **KAPIYI bozuyor** — Ç5 hâlâ *GEÇTİ* diyor *(B-42)* |
| **U11** | darbe parça sınırı **fazı ters** | `mac.py` | S4'te **116 556** çağrı, **8 293**'ü çok sınırlı | 🔴 **sağ kaldı** | 🔴 **DEĞİŞTİ 8/48** *(8 alan)* *(B-51)* |
| **U12** | trafik çiftleri rastgele değil | `traffic.py` | örneklem ≠ `sorted(aday)[:n]` | ⚠️ yakalandı | **2 İLGİSİZ test** — mekanizma korumasız *(B-61)* |
| **U13** | kopya alım baytı sayılmıyor | `mac.py` | S2/yoğun **693** kopya alım | 🔴 **sağ kaldı** | ⚪ tüketicisiz *(B-62)* |
| **U14** | gözlem gürültüsü sabit taban | `kosucu.py` | **7 342/7 342** karar tabandan farklı görüyor | 🔴 **sağ kaldı** | ⚪ tüketicisiz *(B-44)* |
| **U15** | beacon konum bildirmiyor | `kosucu.py` | **52 206** komşu kaydı konum taşıyor | ✅ yakalandı | `test_d10_beacon_gercek_konum_bildiriyor` — **ilgili** |

### 🔴 SAĞ KALAN ORANI VE SERİ

| denetim | mutasyon | sağ kalan | taban | oran |
|---|---|---|---|---|
| Birinci *(19 Ağu)* | 10 | 8 | 198 test | **%80,0** |
| İkinci *(20 Ağu)* | 10 | 7 | 240 test | **%70,0** |
| **Üçüncü *(bu rapor)*** | **15** | **10** | **284 test** | **%66,7** |
| — aynı ölçekte *(ilk 10'um)* | 10 | **7** | 284 test | **%70,0** |

🔴 **Örüntünün kapandığı SÖYLENEMEZ.** %66,7 nominal olarak eşiğin altında,
ama (i) n=15'te binom SH ≈ **12,2 puan** — fark **0,3 SH**; (ii) aynı ölçekte
oran **birebir %70**; (iii) iki örneklem de **amaçlı** seçildi, rastgele değil.
`03` B2'nin *"gürültüden dar tarama"* kuralı burada doğrudan uygulanır: bu
tarama, %70 ile %67'yi ayırt edecek güçte **değil**.

### Sağ kalanlar hangi sınıfta toplanıyor

| sınıf | mutasyon | sayı |
|---|---|---|
| 🔴 **Davranışı değiştiriyor, hiçbir test görmüyor** | U05 · U06 · U07 · U11 | **4** |
| ⚪ **Tüketicisiz** *(alan üretiliyor, kimse okumuyor)* | U01 · U02 · U09 · U13 · U14 | **5** |
| 🔴 **Simülatörü değil KAPIYI bozuyor** | U10 | **1** |

**Üç örüntü:**

1. **Muhasebe katmanı korumasız.** Dört *"davranışı değiştiren"* sağ kalanın
   dördü de bir **sayaç/metrik**: boru artığı, tepe doluluk, kaçırılan beacon,
   darbe fazı. Fizik ve MAC durum makinesi iyi korunuyor *(U03 · U08 · U15
   ilgili testlerle yakalandı)*; **rapora giren sayılar** korunmuyor. Bu,
   birinci denetimin B-04'te ve ikincisinin §5'te yazdığı örüntünün **aynısı**,
   yalnızca yeri kaydı: gözlem penceresi → sonuç muhasebesi.
2. **"Tüketicisiz" sınıfı büyüyor, küçülmüyor.** İkinci denetim 2 alan
   bulmuştu; ben 5 mutasyonla **9 alan + 1 özellik** ölçtüm. B-27b bu sınıfı
   *kapatmadı*, **isimlendirdi**.
3. 🔴 **Yeni sınıf: doğrulama aracının kendisi.** U10, bu üç denetimde
   ilk kez, simülatörü değil **kapıyı** hedefliyor ve sağ kalıyor. Kapı 71
   dakika sürdüğü için tüm koruması *"ucuz bir teste"* devredilmiş — ve o
   ucuz test yalnızca **sayıya** bakıyor.

---

## 6. ŞÜPHE LİSTESİ SONUÇLARI

| # | madde | sonuç |
|---|---|---|
| **1** | Y11 — korumanın kapsamı dışı | 🔴 **bulgu var: B-46 · B-42 · B-48 · B-52.** `karsilastirma`nın **konfig ekseni** temiz *(7 red / 4 kabul yeniden üretildi)*; **kod ekseni** kırıldı. `UYGULANMAMIS_BAYRAKLAR`, `rng.HENUZ_KULLANILMAYAN` ve `KanalErisimi.__setattr__` korumaları **davranışa bağlı** ve sağlam; `gozlem.HENUZ_ICERIK_TESTI_OLMAYAN` **değil** *(B-43)* |
| **2** | Kâhin sızıntısının yeni yüzeyi | ✅ **temiz — ölçüldü.** `bag_gercek_per` RNG çekmiyor *(belirlenimci)*; `Gozlem` donmuş, geri referans yok, alan adlarında iz yok; `protokol_teshis` **iletilmiyor**, yalnızca rapora giriyor; aktarıcıların kâhinliği `dogrulama/` altında ve `08` beyan ediyor. ⚠️ Ama sızıntı testi **ad tabanlı** — B-44 gösteriyor ki alanın **içeriği** denetlenmiyor |
| **3** | Denetçinin mutasyonuna göre yazılmış test fazla dar mı | 🔴 **bulgu var: B-44.** KM4'ün türevi *(U14)* **sağ kaldı**; kapanan şey mutasyondu, mekanizma değil. D10 için türev *(U15)* **yakalandı** — o koruma gerçek. KM3'ün *"bağımsız hesabı"* üretici ifadenin tekrarı, ama **yön** iddiası bağlayıcı |
| **4** | Y7'nin sekizinci örneği | ⚠️ **karışık.** `toplanan_test_sayisi` sağlam *(0 ≠ hata ayrımı üç testle sınanmış, biri Y11 vakası)*; `sag_kalan_ayikla`nın araç-hatası kovası **çalışıyor** *(0 araç hatası)*; `mutasyon_on_kontrol`ün `-k` seçimi **35/35 keskin**. Ama Y7'nin **sekizinci** *(B-41: eşik veriden)* ve **dokuzuncu** *(B-42: seçim daralması)* örnekleri var |
| **5** | Düzeltmenin kendisi hata getirdi mi | ✅ **büyük ölçüde temiz.** B-30'un şema değişikliği RNG çekim sırasını **kaydırmıyor** *(ölçüldü)*; kalibrasyon · Li · derece kayması bugün **tutuyor**. ⚠️ Kaymayan tek şey **yeniden ölçülmedi**: K-020 *(B-56)* |
| **6** | Gözlem içerik testleri ne ölçüyor | 🔴 **bulgu var: B-43 · B-44.** Beyan zinciri **elle taşınan bir etikete** dayanıyor; liste **bugün zaten yanlış**; boş `HENUZ_ICERIK_TESTI_OLMAYAN` kontrolü dejenere ediyor |
| **7** | Ön-kayıt ↔ kod | 🔴 **bulgu var: B-45 · B-48 · B-56.** Sayaç ölçülebilir **görünüyor** ama bilgi taşımayı ölçmüyor. Bant tek yerde tanımlı ✅ ama sonuç satırındaki kopyası korumasız. Monotonluk sınırı `test_b30_*`in docstring'inde yazılı, ama **`06`da değil** — Aile 1'de güçler arası okunma riski duruyor. `05` §D'nin **beş** sayacından **biri** şemada; dördü `protokol_teshis`e havale ve o slot **korumasız** *(B-49)* |
| **8** | Kapsam beyanı — iki yönlü | 🔴 **bulgu var: B-53 · B-55 · B-47.** (a) *"Yapmaz"* denen bir şeyin yapıldığı vaka **bulamadım** — madde 5 *(karıştırıcı CS tetiklemiyor)*, 11 *(sınırsız kopya önbelleği)*, 12 *(alıcı kilidi yok)*, 13 *(tek küresel saat)*, 18 *(tek merkezî karıştırıcı)*, 20 *(FIFO)* kodla **doğrulandı**. (b) Listede olmayan **beş** sınır buldum → §7 |
| **9** | Belge ↔ kod: her sayının üreticisi | 🔴 **bulgu var: B-57.** 46 kaydın **31'inde** üretici yok *(ikinci denetim: 43'te 30)*. Beş kayıt seçip sayılarını yeniden ürettim: **K-017/K-039** *(kalibrasyon + derece kayması)* ✅, **K-020** ❌ *(B-56)*, **K-038/K-044** *(sağ kalan ayıklaması)* ✅, **K-046** *(kapı seçimleri)* ✅ |
| **10** | Kapının kendisi | 🔴 **bulgu var: B-41 · B-42.** Ç1.3'ün eşiği hâlâ veriden; Ç5'in kapsamı sessizce daraltılabiliyor. ✅ **Beş kriterin beklenen test sayısı bugün GÜNCEL** *(6/44/18/6/2 — `--collect-only` ile kapıyı koşmadan doğruladım)*; kapı düşen kriteri **adıyla** söylüyor |
| **11** | Aile 1 bu araçla yazılabilir mi | 🔴 **HAYIR — B-47.** İkinci denetçinin sınırı **doğrulandı**: protokol yalnızca `_uyandir`dan, düğümün paketi varken **ve** MAC boşken çağrılıyor; başka çağıran yok, periyodik kanca yok → Aile 2'nin `takvimli_tazeleme` kolu bu arayüzle **kurulamaz**. ETX benzeri kestirim **kurulabiliyor ama işe yaramıyor**: hedefin nerede olduğu gözlemde yok, ve protokol hiçbir çerçeveye bilgi koyamıyor |
| **12** | İstatistik katmanı | ✅ **beyan yeterli, ama risk yerini değiştirdi.** `08` madde 21 katmanın yazılmadığını, NaN korumasının olmadığını ve Aile 1'in ilk sonucundan önce yazılması gerektiğini **açıkça** söylüyor; Aile 0 hipotez sonucu üretmiyor, dolayısıyla mühürden önce beyan savunulabilir. NaN tuzağını **ölçtüm ve doğruladım** *(n=30 → nan)* — regresyon testi bugün yazılabilir, hiçbir şey engellemiyor. 🔴 **Asıl risk B-47:** mühür sırasının 2. adımı *(“yalnızca rakip kollar koşulur”)* bugün **kurulamıyor**, yani 26 Eylül takvimi istatistik katmanı yüzünden değil **arayüz** yüzünden tehlikede |

---

## 7. KAPSAM BEYANINA EKLENMESİ GEREKENLER

`08`in 22 maddesinde **olmayan**, kodda modellenmemiş ya da yanlış sayılmış beş şey:

| # | Eksik beyan | Etkinin yönü |
|---|---|---|
| **23** | 🔴 **Protokolün ilettiği hiçbir çerçeveye bilgi koyma kanalı yok.** Beacon içeriği `sim/kosucu.py`de sabit; `PaketGorunumu` donmuş; protokolün yazabildiği tek yer `protokol_teshis` ve o **iletilmiyor** | **Ölçümü imkânsız kılar**, modeli iyimser/kötümser yapmaz: çok atlamalı yönlendirme *(H1.1'in iki rakibi de)* bu arayüzle kurulamaz. `05` §A2'nin *"başlığa koy, bedelini öde"* hakkının kod karşılığı yok |
| **24** | **Beacon'ın bayt maliyeti içeriğinden bağımsız** — `beacon_bayt` sabit 32, `icerik` keyfi | 23. madde uygulanırsa modeli **iyimser** yapar: bilgi bedava taşınır. `08` madde 13 aynı riski yalnızca zaman damgası için beyan ediyor |
| **25** | **Sonuç sözlüğü kod sürümünü taşımıyor** ve karşılaştırma onu denetlemiyor *(`05` §E zorunlu sayıyor, `results.py::kaynak_hash` üretiyor)* | Farklı kod sürümlerinden gelen iki satır **karşılaştırılabilir görünür**; ölçüldü: 7,76 ms'lik sahte bir *"gecikme farkı"* |
| **26** | **Madde 22 düzeltilmeli: dört değil DOKUZ alan** *(+ `Gozlem.kuyruk_doluluk` özelliği ve `KomsuKaydi.yas_s()`)* tüketicisiz | Beyanın kendisi eksik; `05`in *"⭐ EN ÖNEMLİ ALAN"* dediği `son_iletim_sonucu` da listede |
| **27** | **Trafik: tek paket boyu, tek CBR sınıfı, tıkanıklık geri beslemesi yok, ve kaynak–hedef çiftleri koşu boyunca SABİT** *(`_ciftleri_sec` bir kez çağrılıyor)* | Modeli gerçeğe göre **durağan** yapar. Sabit çift kümesi, bir kez öğrenilen rotanın hiç eskimemesi demek — **öğrenen protokollerin lehine** bir sınırdır ve H1.1 tam olarak öğrenme farkını soruyor |
| **28** | **Karıştırıcı yörüngesi belirlenimci daire, sabit hız ve yarıçap** *(S5)*; madde 7 yalnızca *düğüm* mobilitesinin yokluğunu beyan ediyor | Karıştırıcı hareketi **öngörülebilir**; gerçek bir hareketli karıştırıcı rastgele/manevralı olabilir. Öngörülebilirlik, tazelik temelli yaklaşımların işini **kolaylaştırır** — hipotezin lehine |

---

## 8. 🔴 ANLAŞILMAYANLAR

### A · Anlamadığım ve bu yüzden denetleyemediğim mekanizmalar

1. **`_kanal_mesgullesti`'deki geri sayım dondurma aritmetiği.**
   `gecen = simdi - sayac_basladi_s - difs_s` ve
   `kalan_slot = max(0, kalan_slot - int(gecen / slot_s))`. DIFS'in
   çıkarılması, geri sayım yeniden planlandığında `difs_s`in **tekrar**
   eklenmesiyle birlikte okununca (`_geri_cekilme_planla`) net etkisinin ne
   olduğunu çıkaramadım: donma–çözülme çevrimi başına bir DIFS **kazanılıyor**
   mu, kaybediliyor mu? 802.11'in kuralı *"DIFS boyunca boş kanaldan sonra
   geri sayım kaldığı yerden devam eder"*; kodun bunu mu yoksa her çözülmede
   tam bir DIFS daha mı beklediğini **ölçmedim**. Bu, çekişme altında verimi
   ve gecikmeyi doğrudan etkiler.

2. **Aynı ana denk gelen olayların sırası ile yarı çift yönlü kontrolü
   arasındaki ilişki.** `gonderim_araligi` yalnızca **son** iletimi tutuyor;
   134 151 alım değerlendirmesinde kaçak **ölçmedim (0)** — ama bunun neden
   **yapısal olarak** imkânsız olduğunu kanıtlayamadım. Kanıt, *"bir düğümün
   iki iletimi arasındaki boşluk her zaman en kısa çerçeveden uzundur"*
   biçiminde olmalı; `_onay_ilet`in SIFS önceliğiyle araya girdiği durumları
   tek tek çıkaramadım. Bugün kaçak yok; yarın çerçeve süreleri değişirse
   sessizce olabilir.

3. **`yakinsama_kontrolu`'nun yörünge-hizalı dilimlerinin kapsamı.**
   `tam_tur >= 2` sağlanmazsa fonksiyon boş dilim listesi ve
   *"pencere < 2 yörünge — kapı uygulanamaz"* döndürüyor. 540 koşuluk ana
   matriste bu dalın **kaç kez** tetiklendiğini ölçmedim; tetikleniyorsa
   Ç1'in yakınsama kolu o koşularda **sessizce uygulanmıyor** demektir ve bu
   `08`de yazılı değil.

4. **`en_kisa_yol` aktarıcısının `onbellek`i tüm düğümler arasında
   PAYLAŞILIYOR.** Protokol fabrikası koşu başına **tek bir çağrılabilir**
   üretiyor ve o çağrılabilir 40 düğümün hepsi için çalışıyor. Bugün zararsız
   *(anahtar `(dugum, hedef)`)*, ama bu, arayüzün düğüm başına durum izolasyonu
   **sağlamadığı** anlamına geliyor: Aile 1'in bir protokolü kazara ya da
   bilerek düğümler arası bedava bilgi paylaşabilir. `08` madde 190 bunu
   *"dil düzeyinde mutlak değil"* diye yalnızca **modül global'leri** için
   beyan ediyor; **arayüzün kendisinden** gelen bu kanalı beyan etmiyor.
   Bunun bir bulgu mu yoksa bilinçli bir tasarım mı olduğunu **belirleyemedim**.

### B · Denetleyemediğim eksenler — koşulmadı, dolayısıyla bu raporda kanıt yok

| eksen | neden koşulmadı |
|---|---|
| Ç1.1 / Ç1.2 / Ç1.4 · 540 koşuluk korunum matrisi | ~6 dk + kapı bağlamı; bütçe mutasyon serisine ayrıldı. **İkinci denetim bunları paket nesnesi sayarak bağımsız doğrulamıştı**; ben yalnızca eşiklerinin nasıl kurulduğunu denetledim |
| Ç1.3 · 35 mutasyonun tam koşusu | ~25 dk. **35/35'in bugün tuttuğunu doğrulamadım**; yalnızca eşiğin veriden türediğini gösterdim *(B-41)*. `mutasyon_on_kontrol` ile 35/35 seçim keskinliğini doğruladım, sonuçlarını değil |
| Kör tarama *(`kor_mutasyon.py 24`)* | ~18 dk, ve `08` skorun **karşılaştırılamaz** olduğunu zaten beyan ediyor. Üçüncü bir bayat sayı üretmek için koşmadım |
| Tam kapı raporu *(`aile0_kapi_raporu.py`)* | **71–74 dk**; 30 dk bütçe sınırının üstünde ve sormadan başlatılamazdı. Kapının **kod yolunu** taklit ederek denetledim *(B-41, B-42)* |
| `li_zincir.py` · `li_deneme_ekseni.py` iç mantığı | Okumadım; Ç4.2'nin çıktısını yeniden ürettim ama zincir kurulumunun kendisini denetlemedim |
| Ç6.1 / Ç6.3 / Ç6.4 kaynak denetimleri | Dizgi aramaları; adları bunu söylüyor ve **değişmez değiller**. Ç6.3'ün `".remove(il)" not in kaynak` koşulunun bir yeniden yazımda sessizce sağlanabileceğini gördüm ama sömürülebilir bir vaka üretmedim |

> ⚠️ İlk iki denetimde bu bölümdeki maddelerin birkaçı **gerçek kusur** çıktı.
> Yukarıdaki A-1 *(DIFS aritmetiği)* ve A-4 *(paylaşılan protokol durumu)*
> bence en güçlü adaylar.

---

## 9. KOŞTURDUĞUM KOMUTLAR

```bash
python -m pytest tests -q --collect-only          # 284 tests collected
python -m pytest tests -q                         # 284 passed in 340.49s  (TABAN)
python -m pytest tests/test_gozlem.py -q          # 18 passed  (B-27b kanıtı: 17 passed)
python -m pytest tests/test_karsilastirma.py -q   # 20 passed  (7 red + 4 kabul)
python -m pytest tests/test_mekanizma_kapisi.py -q
python -m pytest <yol> -k <seçim> --collect-only -q   # 6 / 44 / 18 / 6 / 2
python dogrulama/kurulum_kalibrasyonu.py          # 0,5252 · [0,1197·0,8955] · 0,5076
python dogrulama/kurulum_kalibrasyonu.py --a      # −%0,364 ± 0,026 · %82,93 · 1,2058
python dogrulama/sag_kalan_ayikla.py              # 7/7 eşdeğer · 0 değişen · 0 araç hatası · 5,3 dk
python -c "... plato_olc(TOHUM_TAM) ..."          # 1/6,29 · GA %2,04 · 932,0 kbps
python -c "... len(MUTASYONLAR), len(mutantlari_uret()) ..."   # 35 · 203
python -c "... scipy.stats.wilcoxon([0.0]*n) ..." # n=5→1,0 · n=10→1,0 · n=30→nan
```

**Denetim için yazdığım betikler** *(hepsi `…\scratchpad\den3\`, depoya
hiçbir şey yazılmadı)*:

```bash
python scratchpad/den3/y8_onkontrol.py        # Y8 ön koşulu: 12 yolun tetiklenmesi
python scratchpad/den3/u5_tetik.py            # U05/U13 için tetikleme noktası taraması
python scratchpad/den3/y8_u14_ve_yaricift.py  # U14 Y8 + yarı çift yönlü kaçak ölçümü (0/134151)
python scratchpad/den3/kostur.py              # 13 mutasyon × 284 test  (~40 dk, 5 paralel)
python scratchpad/den3/kostur2.py             # U14 · U15 × 284 test    (~10 dk)
python scratchpad/den3/etki_olc.py <mutant…>  # 48 koşuluk matriste davranış farkı
python scratchpad/den3/kiran.py               # yakalanan mutasyonların KIRAN testleri
python scratchpad/den3/b32_kanit.py           # B-41: kapının Ç1.3 kod yolu, liste 5'e düşmüş
```

**Özet çıktılar**

```
284 passed in 340.49s (0:05:40)                          ← taban
SAĞ KALAN: 10/15   (U01 U02 U05 U06 U07 U09 U10 U11 U13 U14)
davranışı DEĞİŞTİREN: U05 (6/48) · U06 (48/48) · U07 (39/48) · U11 (8/48)
tüketicisiz          : U01 · U02 · U09 · U13 · U14
kapıyı bozan         : U10  (Ç5 → gecen=14 kirilan=0 not='' → GEÇTİ)
🔴 DAVRANIŞI DEĞİŞTİREN : 0 / ⚪ eşdeğer : 7 / 🔧 ARAÇ HATASI : 0    ← sag_kalan_ayikla
OK Ç1.3  mutasyon paketi   5/5   5/5   →   OK AİLE 0 KAPANMAYA HAZIR — 13/13
```

---

## KAPANIŞ NOTU

Bu denetim **24 yeni bulgu** *(B-41 … B-64)* çıkardı ve ikinci denetimin
**17 bulgusunun 17'sini de** tek tek sınadı: 10'u tam kapanmış, 5'i kısmen,
**2'si kapanmamış**.

En değerli üç bulgu, projenin **kendi kurallarının** ihlal edildiği yerler:

| bulgu | ihlal edilen kural |
|---|---|
| **B-41** — ilan edilen düzeltme kodda yok, kapı 13/13 diyor | `03` **kural 15**: *"kod değişikliğini 'başarılı' yazan bir betiğin çıktısına güvenme; değişikliği KODDA doğrula"* |
| **B-43** — B-27b'nin koruması iki elle yazılmış kümeyi karşılaştırıyor ve küme zaten yanlış | `03` **B5** ⭐: *"etiketi elle taşımak — elle yazılan etiket sessizce yanlışlaşır"* |
| **B-45** — mekanizma kapısı null model sınavını geçmiyor: sıfır bilgi taşıyan kol daha iyi skor alıyor | `03` **B1**: *"'mekanizma aktif' ile 'mekanizma bilgi taşıyor'u karıştırmak"* + **B4**: *"kör mekanizma ölçütü"* |

Ve en ağır sonuç bir kural ihlali değil, bir **yapısal** engel: **B-47** —
ön-kaydın Aile 1 için ilan ettiği iki rakip protokol bu gözlem penceresiyle
yazılamıyor. Bu, 26 Eylül mührünü istatistik katmanından **önce** tehdit eder
ve kararı *(pencereyi genişletmek mi, hipotezi daraltmak mı)* **Aile 1
başlamadan** vermek gerekir; ikisi de şemayı değiştirir.

> **Örüntü üçüncü kez kapanmadı** — ve bu kez sağ kalanların **üçte biri**
> simülatörde değil, **doğrulama araçlarının kendisinde.** Kapı 71 dakika
> sürdüğü için korumasını ucuz bir teste devretti; o ucuz test yalnızca sayıya
> bakıyor, ölçülen şeye bakmıyor. K-046'nın **Y12 adayı** doğru teşhis, ama
> yazıldığı hâliyle eksik: *elle tutulan her kapı sabiti ucuz bir testle
> korunur* yetmiyor — **kapının NE ÖLÇTÜĞÜ de korunmalı.**

---

🔒 **Bu denetim sırasında depodaki hiçbir dosya değiştirilmemiştir.**
Yazılan tek dosya `aile0_audit.md`dir *(bu bölüm eklendi, mevcut iki denetim
raporuna dokunulmadı; baştaki durum bloğuna yalnızca üçüncü satır eklendi)*.
Bütün mutasyonlar ve deneme betikleri
`…\AppData\Local\Temp\…\scratchpad\den3\` altındaki geçici kopyalarda
çalıştırıldı. **Hiçbir git komutu çalıştırılmamıştır** — `status` dahil.
**2000–2029 tohum aralığı hiçbir amaçla koşulmamıştır.**

⚠️ **Tam şeffaflık — ve bir öz düzeltme.** Bu notun ilk hâli
*"`.pytest_cache` içeriği değişmemiştir"* diyordu; **yanlıştı** ve dizini
yalnızca üst seviyede kontrol etmiştim. Ölçtüğüm gerçek durum:

| ne | ne zaman | sebebi |
|---|---|---|
| `aile0_audit.md` | 21:02 | 🔴 **benim yazdığım tek dosya** |
| `sim/`, `dogrulama/`, `tests/` altındaki `__pycache__` | denetim boyunca | Python bayt kodu önbelleği — içe aktarma yan etkisi |
| `.pytest_cache/v/cache/nodeids` · `stepwise` | 18:37 | taban `pytest tests -q` koşusu *(`-p no:cacheprovider` vermemiştim)*. `nodeids` toplanan test kimlik listesi, `stepwise` boş; `lastfailed` **19 Ağustos'tan** kalma ve dokunulmadı — yani hiçbir başarısızlık kaydedilmedi |
| `AILE0-DENETIM-3-PROMPTU.md` · `dogrulama/aile0_kapi_raporu.py` · `v2/04-NEDEN-BOYLE.md` · `v2/08-AILE0-KAPSAM.md` · `v2/09-DEVIR-TESLIM.md` | **17:46–17:50** | ⚠️ Bu beşi **denetim başlamadan önceki** oturumun son yazımlarıdır *(K-046 + denetim promptu)*; ben hiçbirine yazmadım. İçerikleri, oturum boyunca okuduğum hâlleriyle aynıdır — nitekim B-41 tam olarak bu dosyalardaki **değişmemiş** koda dayanıyor |

Hiçbir kaynak dosyası, belge ya da test dosyası bu denetim tarafından
değiştirilmemiştir.

---

# DÖRDÜNCÜ DENETİM — 25 Ağustos 2026

> **Denetlenen:** K-054'teki **dördüncü kapanış** *(kapı 13/13, 98,2 dk,
> 21 Ağustos)* ve üçüncü denetimin **23 bulgusunun kapatıldığı iddiası**
> *(K-047 … K-055)*.
>
> **Bağlayıcı şart** *(K-055'in güç analizi)*: **en az 20 bağımsız mutasyon**
> ve **ulaşılan gücün raporlanması**. Koşulan: **24 mutasyon**, her biri
> **TAM 324 testlik paketle**, geçici kopyalarda, taban kontrolüyle birlikte
> *(58,0 dk)*.
>
> 🔴 **Bu rapor, önceki üç denetim raporuna DOKUNMADAN eklenmiştir.**
> Baştaki durum bloğuna yalnızca dördüncü satır ve dördüncü özet eklendi.

**Bu denetimin çalışma ilkesi — üç öncekinden devralınan üç kural:**

| kural | bu raporda nasıl uygulandı |
|---|---|
| **Y8** *(bozduğun yolun tetiklendiğini ÖNCE göster)* | 24 mutasyonun **24'ünün** tetiklenme sayısı, mutasyon yazılmadan **önce** ölçüldü *(§5 tablosu)* |
| **Y10 / Y11** *(iddia kırılabilir olmalı; koruma kapsamı DIŞINDA sınanmalı)* | Her önerdiğim değişmez **önce koşturuldu**; her koruma **kapsamı dışındaki** bir vakayla sınandı *(B-66 · B-67 · B-69 · B-71)* |
| 🔴 **Render kodun kanıtı değildir; BAYTLAR kodun kanıtıdır** *(B-58'in dersi)* | Şüphelenilen her satır `read_bytes()` ile okundu. **B-58'in çürütmesi doğrulandı:** `sim/kosucu.py`de ayraç gerçekten `b"\x1f"` |

⚠️ **Ve bir dördüncü kural, bu denetimin kendisinden çıktı:** *"Yayımladığın
her üretici komutu, yayımlamadan önce **olduğu gibi** koştur."* İki komutum
ilk yazımında **çalışmıyordu** *(Windows'ta `multiprocessing` + `python -`)*;
ikisi de düzeltilip verbatim koşturuldu *(§9)*.

---

## 0. YÖNETİCİ ÖZETİ

🔴 **SAĞ KALAN ORANI: 6/24 = %25,0** *(taban temiz: 324 passed)*. **Seri:
%80,0 → %70,0 → %66,7 → %25,0.** **Ulaşılan güç** *(tek örneklem binom, tek
yönlü, α = 0,05, TAM binom)*: n = 24'te red bölgesi X ≤ 12, gerçek α = 0,0314,
**güç 0,886** *(gerçek oran 0,40 ise)* ve **0,581** *(0,50 ise)*; %80 güce
ulaşılan eşik **p₁ ≤ 0,435**. K-055'in bağlayıcı şartı *(n ≥ 16)* ve aynı
hedefin TAM binomla hesaplanmış hâli *(n ≥ 19)* **karşılandı**; H0: p = 0,70
**reddedilir** *(tek yönlü p = 7×10⁻⁶, %95 GA = [0,098 · 0,467])*.

🔴 **Ama *"örüntü kapandı"* YAZMIYORUM — örüntü KAPANMADI, DARALDI.**
Katmanlara ayırdığımda: **mekanizma** mutasyonlarında oran **%9,1** *(1/11)*,
**sayaç/raporlama alanı** mutasyonlarında **%45,5** *(5/11, %95 GA
[0,167 · 0,766], p = 0,078 — **H0: p = 0,70 reddedilemiyor**)*. Önceki üç
denetimin 10 sağ kalanının **8'i** o ikinci katmandaydı. Genel orandaki
düşüşün büyük kısmı **örneklem karışımının değişmesinden** geliyor; ayrıca
`sim/kosucu.py`ye **hiç mutasyon koymadım** *(üçüncü denetimin 15'inin 7'si
oradaydı, 4'ü sağ kalmıştı)* — bu, oranımın en büyük tek yanlılık kaynağıdır
ve açıkça yazılmıştır.

🔴 **Sağ kalanların hepsi ayrıca ÖLÇÜLDÜ** *(iki ölçütle: tam sonuç sözlüğü
**ve** gözlem penceresi)*: **5'i *"tüketicisiz"*** — davranış/gözlem
değişiyor, **okuyan yok** *(`islenen_olay` 434 571 → 0 · `kuyruk_doluluk`
0,04 → 2,0 · `alinan_bayt` −%6,8 · yük alan sırası · demet bedeli)* —
**1'i gerçek eşdeğer** *(U4-17)*. **Davranışı değiştirip de korumasız kalan
tek bir MEKANİZMA yolu bulamadım: 0/11.**

**Kapanış geçerli mi: KOŞULLU — üç cümlede.** *(1)* Simülatörün **fiziği ve
mekanizmaları** bu denetimde de sağlam çıktı: 11 mekanizma mutasyonunun 10'u
anında yakalandı, korunum defteri, belirlenimcilik *(`PYTHONHASHSEED`ten
bağımsız, blake2b birebir)* ve analitik kontroller *(ortalama derece 7,44259,
girişim menzili 603,2417)* bağımsız olarak yeniden üretildi. *(2)* **Ama
ön-kayıtlı H1.1 mekanizma kapısı, ayarlama tohum kümesinin 8 üyesinin
7'sinde kendi null model sınavını geçmiyor** — K-050'nin B-45 için yazdığı
düzeltme, geometriye duyarlı bir ölçütü **kalıcılığa** duyarlı bir ölçütle
değiştirmiş ve tek tohumda kalibre edilmiş *(B-65)*; bu, Aile 1'in ilk
hipotezini bugün **ölçülemez** kılıyor. *(3)* Ve B-47'nin yeni açtığı
protokol→çerçeve kanalının **bedeli kaçırılabiliyor**: 10 bayt bedelle
1 236 bayt bilgi taşıdım *(124×; sentetik tavan 20 205×)*, yani `05` §A2
kural 1 ve K-009'un *"eşit kontrol düzlemi bütçesi"* şartı bugün
**zorlanmıyor** *(B-66)*.

**13 yeni bulgu: B-65 … B-77.** İkisi kritik *(B-65, B-66)*, ikisi yüksek
*(B-67, B-68)*, biri orta-yüksek *(B-69)*. **`08` kapsam listesine 6 madde**
öneriliyor *(madde 25–30)*; ikisi listede **hiç olmayan** modelleme sınırları
*(yayılma gecikmesi · sınırsız kopya önbelleği)*.

**Üçüncü denetimin 14 bulgusunun kapanışını doğruladım:** 7'si **tam kapalı**
*(B-48 · B-52 · B-53 · B-58 · B-64 ve iki tanesi mutasyonla)*, 2'si **kısmen**
*(B-43 · B-46)*, 3'ü **kapanmamış ya da yeni kusur doğurmuş** *(B-45 → B-65,
B-49 → B-68, B-60 → B-71)*, B-47'nin kapanışı **kanalı açtı ama bedelini
açık bıraktı** *(B-66, B-70)*, B-57 **açık ve kaydı iç çelişkili** *(B-74)*.

**Yeniden ürettiğim 15 iddiadan 15'i tuttu** — seçim avantajının dört sayısı
*(−0,167 · +0,037 · +0,008 · −0,012)*, yük bayt muhasebesi *(10,0)*, kanal
kanıtı *(1,00 → 2,33)*, kör havuz *(215)*, güç analizi *(9 · 16 · 35 · 136)*,
dokuz tüketicisiz alan, ve B-58'in çürütmesi **ham baytla** *(`b"\x1f"`
gerçek)* dâhil.

---

## 1. YENİ BULGULAR — B-65'ten

Her bulgunun **üretici komutu depo kökünden koşar** ve kendi kendine
yeterlidir *(scratchpad yoluna atıf yok — üçüncü denetimin `scratchpad/den3/…`
komutları yeniden üretilemedi)*.

---

### 🔴 B-65 · KRİTİK — Ön-kayıtlı H1.1 mekanizma kapısı TEK TOHUMDA kalibre edilmiş; ayarlama tohumlarının 7/8'inde düşüyor

| | |
|---|---|
| **Nerede** | `sim/kosucu.py:376-384` *(sayaç)* · `tests/test_mekanizma_kapisi.py:244, 261, 264` *(kapı yüklemleri)* · `v2/06-ON-KAYIT.md:365-384` *(ön-kayıt)* |
| **İDDİA** | *"Bilgi taşımayan her kol için beklenen değer **tanım gereği sıfırdır** — kaç atlama yaptığından, kaç karar verdiğinden bağımsız."* `06` H1.1 · `kosucu.py:363-371` |
| **ÖLÇTÜĞÜM** | İddia **yalnızca tohum 1'de** doğru. Ayarlama tohum kümesinin *(1–30)* ilk 8 üyesinde projenin **kendi** iki null modeli ortalama **+0,054** ve **+0,041** veriyor; eşik **0,02**. |

**Üretici komut** *(depo kökünden, kendi kendine yeter)*:

⚠️ **Seri koşar** *(ölçüldü: **3,1 dk**, 32 koşu)*. `multiprocessing` **bilerek
kullanılmadı**: Windows'ta `spawn` başlangıç yöntemi `__main__`i yeniden içe
aktarır ve `python - <<'PY'` ile verilen bir betikte bu **çöker**
*(`OSError: Invalid argument: '<stdin>'`)* — yani paralel bir üretici komut
depo kökünden **yeniden üretilemezdi.**

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import sys; sys.path.insert(0, ".")
from sim.config import Konfig
from sim.kosucu import Kosu
from dogrulama.aktaricilar import AKTARICILAR
def _null_rastgele(kon):                      # test dosyasindan BIREBIR
    def s(g):
        if not g.komsular: return None
        a = sorted(k.dugum for k in g.komsular)
        return a[(g.dugum*2654435761 + len(a)*40503) % len(a)]
    return s
def _null_kuyruk(kon):                        # test dosyasindan BIREBIR
    def s(g):
        if not g.komsular: return None
        return min(sorted(g.komsular, key=lambda k: k.dugum),
                   key=lambda k: k.bildirdigi_kuyruk).dugum
    return s
KOL = {"null_rastgele": _null_rastgele, "null_kuyruk": _null_kuyruk,
       "kacan": AKTARICILAR["gurultuden_kacan"], "kor": AKTARICILAR["en_kisa_yol"]}
d = {}
for ad, fab in KOL.items():
    for t in range(1, 9):
        d[(ad, t)] = Kosu(Konfig(kol="t", senaryo="S2", trafik="orta", tohum=t),
                          fab).kostur()["secim_avantaji_ortalama"]
for t in range(1, 9):
    nr, kq = d[("null_rastgele", t)], d[("null_kuyruk", t)]
    kc, ko = d[("kacan", t)], d[("kor", t)]
    print("tohum %d  null_rast=%+.5f null_kuy=%+.5f kacan=%+.5f kor=%+.5f | "
          "T1=%s T2=%s T3=%s" % (t, nr, kq, kc, ko,
          "GECTI" if abs(nr) < 0.02 and abs(kq) < 0.02 else "DUSTU",
          "GECTI" if kc > 3*abs(nr) else "DUSTU",
          "GECTI" if ko < -0.05 else "DUSTU"))
PY
```

**Beklenen / görülen** *(S2 · orta · `secim_avantaji_ortalama`)*:

| tohum | null_rastgele | null_kuyruk | kaçan *(bilgili)* | kör | T1 `abs(av)<0,02` | T2 `kacan>3·abs(nul)` | T3 `kor<−0,05` |
|---|---|---|---|---|---|---|---|
| **1** | +0,00809 | −0,01199 | +0,03695 | −0,16708 | ✅ | ✅ | ✅ |
| 2 | −0,02866 | +0,07719 | +0,07282 | −0,32441 | 🔴 | 🔴 | ✅ |
| 3 | +0,07456 | −0,03728 | +0,13037 | −0,05373 | 🔴 | 🔴 | ✅ |
| 4 | **+0,19886** | +0,14445 | +0,11936 | −0,33154 | 🔴 | 🔴 | ✅ |
| 5 | +0,05226 | +0,02453 | +0,04876 | −0,11304 | 🔴 | 🔴 | ✅ |
| 6 | +0,06861 | −0,03205 | +0,04165 | −0,04267 | 🔴 | 🔴 | 🔴 |
| 7 | +0,04106 | +0,11756 | +0,14645 | −0,05263 | 🔴 | ✅ | ✅ |
| 8 | +0,01745 | +0,04195 | +0,10425 | **+0,00930** | 🔴 | ✅ | 🔴 |
| **ort ± std** | **+0,054 ± 0,063** | **+0,041 ± 0,064** | +0,088 ± 0,040 | −0,134 ± 0,122 | **7/8 DÜŞTÜ** | **5/8 DÜŞTÜ** | **2/8 DÜŞTÜ** |

`06`'nın **yazılı** 3. koşulu *(«ikisinin **farkı**, null modelin büyüklüğünün
en az 3 katı»)* ile koşulduğunda da **3/8 tohumda düşüyor** *(tohum 3, 4, 6)*.

**Dört ayrı kanıt, aynı yöne:**

1. Null modelin **tohumlar arası std'si 0,063** — kapının eşiğinin **3 katı**.
   Tohum 1'de görülen +0,008/−0,012, eşiğin altındaki **tek** çekimdi.
2. Tohum 8'de *"tanım gereği kör"* kol **pozitif** avantaj alıyor (+0,009).
3. Bilgili kol ortalaması **+0,088**, bilgisiz kol ortalaması **+0,054** —
   ayrım 1,6 kat; kapı 3 kat istiyor.
4. **Yeni yazdığım üçüncü null model** *(hiçbir gözlem ALANI okumaz, yalnızca
   `g.komsular` demetinin SIRASINI kullanır)*: **+0,064**. Bir dördüncüsü
   *(`g.komsular[-1]`)* **hiçbir paket teslim etmiyor** *(teslim = 0,0000, üç
   tohumda da)* ve yine **+0,057** avantaj alıyor.

**SEBEP ÖLÇÜLDÜ** *(`03` B4 — kusuru ölçmek onu sebep yapmaz)*: kestirimin
beklenen değeri **yalnızca KARAR BAŞINA düzgün rastgeleleştirme altında**
sıfırdır. Her kararda bağımsız düzgün komşu seçen bir null yazdım:

| null | 8 tohumda ortalama | std | `abs(av)<0,02` |
|---|---|---|---|
| **karar başına düzgün rastgele** *(yeni)* | **+0,00014** | 0,00029 | **8/8 ✅** |
| projenin `_null_rastgele`'si *(düğüm başına SABİT seçim)* | +0,054 | 0,063 | 1/8 |

Yani ölçüt **bilgiyi** değil **seçimin KALICILIĞINI** ölçüyor: bir düğüm aynı
komşuyu binlerce kararda seçtiğinde fark ortalamada sönmüyor. Her gerçek
protokol *(ve projenin iki null'ü de)* kalıcı seçim yapar.

**Neden önemli:** B-45'in düzeltmesi *(K-050)*, **geometriye** duyarlı bir
ölçütü **kalıcılığa** duyarlı bir ölçütle değiştirdi. Ön-kayıtlı bir kapı
*(«bu ölçüt tutmuyorsa SONUCA BAKILMAZ»)* hâlâ *"bağ kalitesi bilgisi
kullanıyor"* ile *"ısrarla aynı komşuyu seçiyor"*u ayırt edemiyor — B-45'in
kendi cümlesiyle: *"Ayırt edemeyen bir kapı, kapı değildir."* Ve `03` kural 2
*(«tek/az tohumlu sonuç raporlama»)* ön-kaydın **kendi kapısında** ihlal
edilmiş.

**Öneri** *(önermeden önce koşturuldu)*:
- Ölçütü **karar başına** değil **düğüm-komşu çifti başına** ağırlıklandır
  ya da avantajı **eşleştirilmiş** hesapla *(aynı kararda seçilen ile
  seçilebilecek olanın farkı, düğüm bazında ortalanıp sonra düğümler
  arasında ortalanarak)*.
- Kapı eşiği **≥ 30 tohumun güven aralığından** türetilsin; tek tohumda
  yazılmış `0,02` sabiti null'un std'sinin **1/3'ü**.
- Kapı testleri `tohum` üzerinden **parametrize** edilsin *(en az 5 tohum)*.

---

### 🔴 B-66 · KRİTİK — `yuk_bayt` bedeli TİPE bağlı, taşınan BİLGİYE değil: 10 bayt bedelle 1 236 bayt taşındı

| | |
|---|---|
| **Nerede** | `sim/gozlem.py:216-244` *(`yuk_bayt`)* · özellikle `:221` *(alan adı kontrolü)* ve `:226-227` *(int/float → 4 bayt)* · `sim/kosucu.py:295-303` *(kanca)* |
| **İDDİA** | `05` §A2 kural 1: *"Başlıktaki her alan **bayt olarak sayılır** ve kontrol yüküne yazılır."* Ve `gozlem.py:210-214`: *"Maliyet **gerçek serileştirmeden** hesaplanır; protokolün kendi beyanına bırakılmaz. Beyan edilseydi, ucuz görünmek isteyen bir protokol az beyan ederdi."* |
| **ÖLÇTÜĞÜM** | Maliyet gerçek serileştirmeden **hesaplanmıyor**: `int` **büyüklüğünden bağımsız** 4 bayt, alan adı **uzunluğundan bağımsız** 1 bayt. İkisi de sınırsız. |

**Üretici komut** *(depo kökünden)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import sys; sys.path.insert(0, ".")
from sim.gozlem import yuk_bayt
from sim.config import Konfig
from sim.kosucu import Kosu
for ad, y in [("durust {'etx':1.5}", {"etx": 1.5}),
              ("BUYUK INT 2**8192", {"a": 2**8192}),
              ("100k karakterlik ALAN ADI", {"z"*100000: 0}),
              ("ikisi birden", {"z"*100000: 2**8192})]:
    b = yuk_bayt(y)
    bilgi = sum(len(k) for k in y) + sum((int(v).bit_length()+7)//8
               for v in y.values() if isinstance(v, int) and not isinstance(v, bool))
    print("%-28s odenen=%d bayt  tasinan>=%d bayt  kat=%d" % (ad, b, bilgi, bilgi//b))
GIZLI = "GIZLI-MESAJ-" + "X"*200
def fab(kon):
    def s(g): return min(k.dugum for k in g.komsular) if g.komsular else None
    s.beacon_yuku = lambda d: {GIZLI: d, "z": 2**8192}
    return s
k = Kosu(Konfig(kol="t", senaryo="S0", tohum=1), fab); s = k.kostur()
alan = sum(1 for t in k.komsu_tablosu.values() for r in t.values()
           if GIZLI in dict(r.bildirdigi_yuk))
print("beacon basina odenen: %.1f bayt · gizli yuku ALAN komsu kaydi: %d"
      % (s["yuk_bayt_toplam"]/s["beacon_gonderilen"], alan))
PY
```

**Beklenen / görülen:**

| yük | ödenen | taşınan *(en az)* | kat |
|---|---|---|---|
| `{"etx": 1.5}` *(dürüst)* | 5 bayt | 3 bayt | **0,6×** *(bedel bilgiden büyük — doğru yön)* |
| `{"a": 2**8192}` | **5 bayt** | 1 026 bayt | **205×** |
| `{"z"*100000: 0}` | **5 bayt** | 100 000 bayt | **20 000×** |
| tam koşu: `{212-karakterlik-ad: d, "z": 2**8192}` | **10 bayt/beacon** | ≥1 236 bayt | **124×** |

Tam koşuda gizli yük **266 komşu kaydına ulaştı** *(S0, tohum 1)* ve
`yuk_bayt_toplam` yalnızca 10,0 bayt/beacon saydı.

**Neden önemli:** Aile 1/2'nin rakip protokolleri bu kancayla yazılacak.
Bir protokol tüm yönlendirme tablosunu **tek bir alan adında** ya da **tek bir
büyük tamsayıda** taşıyıp kontrol düzlemi bütçesinin **%0,8'ini** ödeyebilir.
K-009'un *"eşit kontrol düzlemi bütçesi"* adalet şartı ve `03` B3'ün
*"kontrol yükünü BAYT cinsinden say"* kuralı **denetlenemez** hâle gelir —
ve `08` madde 24 yalnızca *"hizalama/dolgu yok"* diyor, bu ekseni **beyan
etmiyor**. `test_b47_SOZLESME_DISI_yuk_reddediliyor` sekiz kötü tip deniyor
*(metin, None, nesne, boş demet, karışık demet, boş ad, liste, sözlük değil)*
ama **uzunluk/büyüklük eksenini hiç denemiyor** — Y11'in tam tanımı.

**Öneri** *(önermeden önce koşturuldu — üstteki komut ölçümü basıyor)*:
`yuk_bayt` alan adını `len(ad.encode("utf-8"))` bayt, tamsayıyı
`max(4, (v.bit_length()+7)//8)` bayt saysın; ya da alan adları
**sabit uzunlukta bir kimlik havuzundan** seçilsin ve `int` için değer aralığı
`__post_init__` benzeri bir kontrolle sınırlansın.

---

### 🔴 B-67 · YÜKSEK — `ortak_alt_kume`nin DÖRDÜNCÜ EKSENİ: satır İÇİ yapısal doğrulama yok

| | |
|---|---|
| **Nerede** | `sim/karsilastirma.py:188-189` *(`dict(zip(...))`)* |
| **İDDİA** | *"🔴 Y7 — ARAÇ NE KARŞILAŞTIRDIĞINI KENDİSİ DOĞRULAR … sessizce yanlış bir sayı üretmek yerine `KarsilastirmaHatasi` fırlatılır."* `karsilastirma.py:97-101` |
| **ÖLÇTÜĞÜM** | Üç eksen *(paket evreni · kurulum · kod sürümü)* **kollar arası** tutarlılığı denetliyor. **Bir satırın kendi içindeki** tutarlılık hiç denetlenmiyor. |

**Üretici komut** *(depo kökünden)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import sys, copy; sys.path.insert(0, ".")
from sim.config import Konfig
from sim.kosucu import Kosu
from sim.karsilastirma import ortak_alt_kume, KarsilastirmaHatasi
from dogrulama.aktaricilar import en_kisa_yol, gurultuden_kacan
a = Kosu(Konfig(kol="a", senaryo="S2", trafik="orta", tohum=1), en_kisa_yol).kostur()
b = Kosu(Konfig(kol="b", senaryo="S2", trafik="orta", tohum=1), gurultuden_kacan).kostur()
def dene(ad, sb):
    try:
        r = ortak_alt_kume(a, sb)
        print("  KABUL ETTI  %-40s ortak=%d fark=%s" % (ad, r.ortak_paket,
              None if r.gecikme_farki_s is None else "%.3f ms" % (1000*r.gecikme_farki_s)))
    except KarsilastirmaHatasi as e:
        print("  reddetti    %-40s (%s)" % (ad, str(e)[:30]))
print("mesru cift:", ortak_alt_kume(a, b).ozet())
b1 = copy.deepcopy(b); b1["teslim_gecikmeleri_s"] = b1["teslim_gecikmeleri_s"][:len(b1["teslim_gecikmeleri_s"])//2]
dene("gecikme listesi YARIYA kirpik", b1)
b2 = copy.deepcopy(b); b2["teslim_kimlikleri"] = [b2["teslim_kimlikleri"][0]]*len(b2["teslim_kimlikleri"])
dene("TUM kimlikler ayni (tekrarli)", b2)
b3 = copy.deepcopy(b); b3["teslim_gecikmeleri_s"] = [float("nan")]*len(b3["teslim_gecikmeleri_s"])
dene("tum gecikmeler NaN", b3)
b4 = copy.deepcopy(b); b4["teslim_gecikmeleri_s"] = [-1.0]*len(b4["teslim_gecikmeleri_s"])
dene("tum gecikmeler NEGATIF", b4)
PY
```

**Beklenen / görülen** *(meşru çift: ortak 274 paket, kesişim %33,8)*:

| bozuk girdi | beklenen | görülen |
|---|---|---|
| `teslim_gecikmeleri_s` **yarıya kırpık** | `KarsilastirmaHatasi` | 🔴 **KABUL** — `ortak=139`, *"gecikme farkı **846,701 ms**"* |
| tüm `teslim_kimlikleri` **aynı** | hata | 🔴 **KABUL** — `ortak=1`, fark 551,345 ms |
| tüm gecikmeler **NaN** | hata *(`03` B2 🔴)* | 🔴 **KABUL** — fark `nan`, bayrak yok |
| tüm gecikmeler **negatif** | hata | 🔴 **KABUL** — fark −1 023,977 ms |

`tests/test_karsilastirma.py`in **14 testinin 14'ü de** üç eksenden birinde;
satır içi yapı sınayan **tek test yok**.

**Neden önemli:** `dict(zip(...))` sessizce **kırpar** ve tekrarlı kimliği
**ezer**. Araç, raporlamak için var olduğu tek büyüklüğü — *kaç paket ortak* —
sessizce yanlış üretiyor. NaN maddesi ayrıca `03` B2'nin 🔴 *"NaN'ın sessizce
zehirlemesi"* kuralına ve `08` madde 21'e doğrudan dokunuyor: istatistik
katmanı yazılmadı ama **NaN'ı taşıyan boru zaten çalışıyor**.

**Öneri** *(önermeden önce koşturuldu — üstteki komut dördünü de gösteriyor)*:
`ortak_alt_kume` başında dört değişmez:
`len(kimlikler) == len(gecikmeler)` · `len(set(kimlikler)) == len(kimlikler)` ·
`all(math.isfinite(x) for x in gecikmeler)` · `all(x >= 0 ...)`.
Dördü de bugünkü gerçek çıktıda **tutuyor** *(a ve b satırlarında ölçüldü)*,
yani değişmez **doğru** ve **kırılabilir**.

---

### 🔴 B-68 · YÜKSEK — `protokol_teshis` slotu meşru protokol arayüzünden YAZILAMAZ; tek gösterimi `05`'in yasakladığı geri referansla yapılıyor

| | |
|---|---|
| **Nerede** | `sim/kosucu.py:227` *(slot)* · `tests/test_mekanizma_kapisi.py:350-380` *(B-49'un kapanış testi)* |
| **İDDİA** | K-049/B-49: *"Slot açıldı ama taşıdığı hiç gösterilmedi… `test_b49_protokol_teshis_slotu_gercekten_TASIYOR`"*. `kosucu.py:222-226`: *"Aile 1/2'nin protokolleri … dört teşhis sayacını **buraya yazar**."* |
| **ÖLÇTÜĞÜM** | Protokol arayüzü `protokol_fabrikasi(kon) → protokol(gozlem) → int\|None`. `Gozlem` **donmuş** ve `YASAK_TIPLER` taraması simülatöre erişimi reddediyor. Slota giden **hiçbir meşru yol yok**. B-49'un testi slota yazabilmek için `yazan_fabrika._kosu = k` satırıyla **dışarıdan `Kosu` nesnesini enjekte ediyor** *(satır 373)*. |

**Üretici komut** *(depo kökünden)*:

```bash
grep -n "_kosu = k\|yazan_fabrika._kosu" tests/test_mekanizma_kapisi.py
grep -n "protokol_teshis" sim/*.py dogrulama/*.py
```

**Beklenen / görülen:** `sim/` + `dogrulama/` altında `protokol_teshis`e
**yazan tek satır yok**; okuyan tek satır `kosucu.py:542`. Testin yazma yolu
fabrikanın `__dict__`'ine iliştirilmiş bir `Kosu` referansı.

**Neden önemli:** İki yönlü hasar. *(a)* Şema *"Aile 1 başlamadan dondu"*
deniyor ama slot **doldurulamaz** — `05` §D'nin dört teşhis sayacının kod
karşılığı yok; bu `03` B5'in *"bildirim ≠ kullanım"* tuzağı, gözlem
sözleşmesinin **çıkış** tarafında. *(b)* Daha ağırı: testin gösterdiği yol bir
**şablon**. Aile 1 aynı deseni kullanırsa protokol `topo`, `karistirici`,
`mac.bag_gercek_per` dâhil her şeye ulaşır — `03` kural 5'in tam hedefi.
`test_c5_1b` sızıntı taraması **`Gozlem` nesnesinden** başlıyor; fabrikanın
özniteliğine bakmıyor, yani bu kanalı **göremez**.

**Öneri:** slot ya `Gozlem`e **salt-yazılır bir kanal** olarak açılsın
*(ör. protokolün döndürdüğü isteğe bağlı ikinci değer, ya da `beacon_yuku`
gibi isteğe bağlı bir `teshis(dugum) → dict` kancası — `_beacon_at`in
deseniyle birebir aynı)*, ya da `08`e *"slot bugün doldurulamaz"* maddesi
girsin. Kanca deseni zaten kanıtlanmış: `kosucu.py:295`.

---

### 🔴 B-69 · ORTA-YÜKSEK — A-4'ün *"kalan kanal yalnızca modül global'leridir"* beyanı YANLIŞ

| | |
|---|---|
| **Nerede** | `v2/08-AILE0-KAPSAM.md:194` *(beyan)* · `tests/test_gozlem.py:666-711` *(A-4 testi)* |
| **İDDİA** | *"…**kapatıldı**: her düğüm kendi protokol örneğini alıyor ve `test_a4_…` bunu mutasyonla doğruluyor. **Kalan kanal yalnızca modül global'leridir.**"* |
| **ÖLÇTÜĞÜM** | Fabrikayı **saran bir kapsamda** yaratılan durum ne modül globalidir ne örneğe aittir — ve 40 örneğin hepsi onu paylaşır. |

**Üretici komut** *(depo kökünden)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import sys; sys.path.insert(0, ".")
from sim.config import Konfig
from sim.kosucu import Kosu
def rakip_yap():
    ORTAK = {}                                  # modul globali DEGIL
    def fabrika(kon):
        def s(g):
            ORTAK[g.dugum] = g.olculen_gurultu_w         # A yazar
            if not g.komsular: return None
            gor = [k.dugum for k in g.komsular if k.dugum in ORTAK]
            return min(gor, key=lambda d: ORTAK[d]) if gor else min(k.dugum for k in g.komsular)
        return s
    fabrika._ORTAK = ORTAK
    return fabrika
fab = rakip_yap()
k = Kosu(Konfig(kol="t", senaryo="S2", tohum=1), fab); k.kostur()
print("paylasilan sozlukte biriken OZEL olcum sayisi:", len(fab._ORTAK), "/", k.kon.dugum_sayisi)
ornekler = []
def izole(kon):
    g_ = set(); ornekler.append(g_); ic = fab(kon)
    def s(g):
        g_.add(g.dugum); return ic(g)
    return s
Kosu(Konfig(kol="t", senaryo="S2", tohum=1), izole).kostur()
print("test_a4'un olctugu: birden cok dugum goren ornek =",
      len([x for x in ornekler if x and len(x) != 1]), "(0 ise test GECER)")
PY
```

**Beklenen / görülen:** `ORTAK` sözlüğünde **14 düğümün kendi anteninde
ölçtüğü gürültü** birikti ve komşu seçimi bu paylaşılan tablodan yapıldı;
`test_a4_…`ün ölçtüğü büyüklük **0** — yani test **geçiyor**, kanal **açık**.

**Neden önemli:** Beyan, kalan riski **olduğundan dar** gösteriyor. A-4'ün
kapattığı şey *"tek çağrılabilir, 40 düğüm"*tü; kapanmayan şey *"40
çağrılabilir, tek paylaşılan durum"*. Aile 1'in rakipleri bu arayüzle
yazılacak ve fabrika-saran kapsam en doğal Python deseni.

**Öneri:** `08:194`ün son cümlesi *"Kalan kanal, protokol nesnelerinin
PAYLAŞTIĞI her yazılabilir durumdur: modül global'i, fabrikayı saran kapsam,
sınıf özniteliği, fabrikanın kendi `__dict__`i."* olsun; ve `test_a4_…`e
**örnekler arası** bir kontrol eklensin *(her örneğin `__closure__`
hücrelerinin kimlik kümesi ayrık mı)*.

---

### B-70 · ORTA — Beacon yükünün bedeli gönderende ödeniyor, alıcıda kredilendirilmiyor

| | |
|---|---|
| **Nerede** | `sim/mac.py:276` *(alıcı: `+= self.kon.beacon_bayt`)* ↔ `sim/mac.py:262` *(gönderen: `+= bayt`)* |
| **İDDİA** | `gozlem.py` alan listesi `alinan_bayt`ı *"düğümün KENDİ sayacı"* olarak veriyor; B-47 yükün *"hem `kontrol_bayt`a hem `kontrol_airtime_s`e"* girdiğini yazıyor. |
| **ÖLÇTÜĞÜM** | 57 baytlık *(32 + 25)* bir beacon çerçevesi için alıcı **32 bayt** kredi alıyor. |

**Üretici komut** *(depo kökünden)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import sys; sys.path.insert(0, ".")
from sim.config import Konfig
from sim.kosucu import Kosu
kon = Konfig(kol="t", senaryo="S0", tohum=1)
def fab(k):
    def s(g): return min(x.dugum for x in g.komsular) if g.komsular else None
    s.beacon_yuku = lambda d: {"a":1,"b":2,"c":3,"d":4,"e":5}     # 5x5 = 25 bayt
    return s
k = Kosu(kon, fab); kayit = []
asil = k.mac._yayin_bitti
def izle(dugum, il):
    n0, a0 = k.mac.alinan_yayin, sum(k.mac.dugum_alinan_bayt)
    asil(dugum, il)
    if k.mac.alinan_yayin > n0 and len(kayit) < 3:
        kayit.append((sum(k.mac.dugum_alinan_bayt)-a0)/(k.mac.alinan_yayin-n0))
k.mac._yayin_bitti = izle
s = k.kostur()
print("cerceve = %d + %d = %d bayt" % (kon.beacon_bayt,
      s["yuk_bayt_toplam"]//s["beacon_gonderilen"],
      kon.beacon_bayt + s["yuk_bayt_toplam"]//s["beacon_gonderilen"]))
print("alici basina kredi:", kayit)
print("kosu boyunca kredilendirilmeyen: %d bayt" % (25*s["beacon_alinan"]))
PY
```

**Beklenen / görülen:** çerçeve 57 bayt; üç ayrı yayın olayında alıcı başına
kredi **32,0 · 32,0 · 32,0**. Bir koşuda toplam **1 668 050 bayt** *(66 722
alım × 25)* kredilendirilmiyor. Veri ve onay yollarında böyle bir asimetri
**yok** *(`mac.py:410`, `:449` gerçek boyutu kredilendiriyor)* — yani bu, B-47
kanalının **yeni** getirdiği tutarsızlık.

**Neden önemli:** `alinan_bayt` bir **gözlem penceresi alanıdır** — protokol
kararına girebilir *(bugün tüketicisi yok, `08` madde 22)*. Yük taşıyan bir
kolun komşuları, aldıkları baytı olduğundan **az** görür.

**Öneri:** `mac.py:276` → `+= il.bayt` benzeri gerçek çerçeve boyutu.
`Iletim` bugün `bayt` taşımıyor; `_yayin_geri_cekilme_bitti`de `bayt`ı
`Iletim`e ekleyip alıcıda kullanmak yeterli.

---

### B-71 · ORTA — B-60'ın `ULASILABILIRLIK_YOK` nöbetçisi üç yoldan atlanıyor; biri SESSİZCE çalışma noktasını değiştiriyor

| | |
|---|---|
| **Nerede** | `dogrulama/kurulum_kalibrasyonu.py:419-421` |
| **İDDİA** | K-053/B-60: *"Artık argüman **zorunlu**; atlamak isteyen `ULASILABILIRLIK_YOK` nöbetçisini **AÇIKÇA** geçmek zorunda."* |
| **ÖLÇTÜĞÜM** | Nöbetçi kimlik *(`is not`)* karşılaştırması; ve kısıt haritasının `egri`yi **kapsadığı hiç denetlenmiyor** — eksik anahtar `.get(r[0], 0.0)` ile **sessizce eleme** demek. |

**Üretici komut** *(depo kökünden)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import sys; sys.path.insert(0, ".")
from dogrulama.kurulum_kalibrasyonu import yeni_olcut, ULASILABILIRLIK_YOK
egri = [(-10, .90), (0, .70), (6, .51), (11, .12)]
print("A tam harita        ->", yeni_olcut(egri, {-10:99.,0:97.,6:84.8,11:60.})[3])
print("B '0' anahtari YOK  ->", yeni_olcut(egri, {-10:99.,6:84.8,11:60.})[3])
lit = "__ULASILABILIRLIK_YOK__"
print("C duz dizgi literali is-testi:", lit is ULASILABILIRLIK_YOK,
      "->", yeni_olcut(egri, lit)[3])
class HZI(dict):
    def get(self, k, d=None): return 100.0
print("D .get()'i ezen harita ->", yeni_olcut(egri, HZI())[3])
PY
```

**Beklenen / görülen:**

| girdi | beklenen | görülen |
|---|---|---|
| tam harita | `(0, 0.70)` | `(0, 0.70)` ✅ |
| **`0` anahtarı eksik** | hata *(veri yok)* | 🔴 **`(-10, 0.90)`** — çalışma noktası sessizce değişti |
| düz dizgi literali `"__ULASILABILIRLIK_YOK__"` | red | 🔴 `is` **True** *(CPython interning)* → `(6, 0.51)` — B-29'un engellemek için yazıldığı **+6 dBm** |
| `.get`'i ezen sözlük türevi | red | 🔴 `(6, 0.51)` |

**Neden önemli:** *(a)* Eksik anahtar sıradan bir hata ve **sessizce** başka
bir çalışma noktası seçtiriyor — `03` B5'in *"yanlış sayı, çalışmayan koddan
tehlikelidir çünkü sessizdir"*. *(b)* Nöbetçinin dizgi **kimliğine** dayanması
CPython interning'ine bağlı: `"__ULASILABILIRLIK_" + "YOK__"` çalışma anında
üretilirse `is` **False** döner ve `AttributeError` fırlar — yani aynı değer
iki farklı davranış üretir. Depo bu hata sınıfını `rng.py`de *(`hash()`
tuzlanması)* zaten adlandırmış.

**Öneri:** nöbetçi `object()` ya da bir `enum` üyesi olsun *(kimlik gerçekten
tekil olur)*; ve kısıt uygulanmadan önce
`eksik = {g for g,_ in egri} - set(ulasilabilirlik)` boş değilse `ValueError`.
*(Bugünkü tam haritada `eksik` boş — değişmez koşturuldu, tutuyor.)*

---

### B-72 · ORTA — `_girisim_w`de tetiklenemeyen dal: 246 378 çağrının 0'ında

| | |
|---|---|
| **Nerede** | `sim/mac.py:520` — `if baska is il or baska.gonderen == alici:` |
| **İDDİA** | Deponun kendi kuralı *(`config.py:329-332`, `mac.py:628-637`)*: *"Tetiklenemeyen bir kontrol, koruma sağlamadan koruma izlenimi verir."* Aynı gerekçeyle iki kontrol zaten `assert`e/`değişmez`e çevrilmiş. |
| **ÖLÇTÜĞÜM** | `baska.gonderen == alici` **hiç** tetiklenmiyor: `alim_per` zaten yarı çift yönlü örtüşmeyi *(mac.py:598-600)* kontrol edip `None` dönüyor, dolayısıyla alıcı çerçeve süresince gönderemiyor. |

**Üretici komut** *(depo kökünden)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import sys, collections; sys.path.insert(0, ".")
import sim.mac as mm
from sim.config import Konfig
from sim.kosucu import Kosu
from dogrulama.aktaricilar import en_kisa_yol
C = collections.Counter()
_g = mm.KanalErisimi._girisim_w
def g(self, alici, il, an_s):
    C["cagri"] += 1
    for b in self.aktif:
        if b is not il and b.gonderen == alici and b.baslangic_s <= an_s < b.bitis_s:
            C["tetiklendi"] += 1
    return _g(self, alici, il, an_s)
mm.KanalErisimi._girisim_w = g
for sen in ("S2", "S0"):
    C.clear()
    Kosu(Konfig(kol="t", senaryo=sen, trafik="orta", tohum=1), en_kisa_yol).kostur()
    print(sen, dict(C))
PY
```

**Beklenen / görülen:** S2 → `cagri=123407, tetiklendi=0`;
S0 → `cagri=122971, tetiklendi=0`. Toplam **246 378 çağrı, 0 tetiklenme**.

**Neden önemli:** Bu dal, deponun **kendi ölçütüne göre** koruma sağlamıyor.
Daha önemlisi: bir gün yarı çift yönlü kontrolü *(mac.py:598)* kaldırılırsa
bu dal **sessizce** doğru cevabı vermeye başlar ve hatayı **maskeler** —
`_alim_basarili_mi`de aynı durum için `assert` tercih edilmesinin sebebi
tam olarak buydu.

**Öneri:** ya `assert` ile değişmeze çevrilsin *(`mac.py:625-637`in birebir
deseni)*, ya `08`e *"bu dal tetiklenemez"* notu düşülsün.

---

### B-73 · DÜŞÜK-ORTA — `06`'nın H1.1 koşul 3'ü ile onu uygulayan test FARKLI YÜKLEM

| | |
|---|---|
| **Nerede** | `v2/06-ON-KAYIT.md:381` ↔ `tests/test_mekanizma_kapisi.py:261` |
| **İDDİA** | `06`: *"**İkisinin farkı**, null modelin büyüklüğünün en az 3 katı olmalı"*. Kayıt ayrıca *"Ölçüt `tests/test_mekanizma_kapisi.py`de teste bağlıdır"* diyor. |
| **ÖLÇTÜĞÜM** | Test `assert kacan > 3 * abs(nul)` yazıyor — **farkı değil, bilgili kolun kendi değerini** sınıyor. |

**Üretici komut:**

```bash
grep -n "İkisinin farkı" v2/06-ON-KAYIT.md
grep -n "kacan > 3 \* abs(nul)" tests/test_mekanizma_kapisi.py
```

**Beklenen / görülen:** İki yüklem farklı tohumlarda **farklı karar** veriyor
*(B-65 tablosu: `06` sürümü 3/8, test sürümü 5/8 tohumda düşüyor)* — yani fark
akademik değil, **bağlayıcı**. `03` B5: *"yorumun kodla çelişmesi ikisinden de
kötüdür."*

**Öneri:** Ön-kayıt mühürlenmeden *(26 Eylül)* ikisinden biri seçilsin ve
diğeri **aynı satırdan** türesin.

---

### B-74 · DÜŞÜK-ORTA — B-57'nin kendi kaydında aritmetik çelişki; ve bugünkü oran farklı

| | |
|---|---|
| **Nerede** | `v2/04-NEDEN-BOYLE.md:3628-3656` *(K-053 · B-57)* |
| **İDDİA** | *"sonra: toplam 53 üreticili 23 yok 30"* ve hemen ardından *"Kalan **30** kaydın **35'inde** sayı var ama üretici yok"*. |
| **ÖLÇTÜĞÜM** | **35 > 30.** 30 kaydın 35'inde bir şey olamaz. Kaydın kendi üretici satırıyla yeniden ölçtüm. |

**Üretici komut** *(kaydın kendi tarif ettiği tarama)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import re, pathlib
t = pathlib.Path("v2/04-NEDEN-BOYLE.md").read_text(encoding="utf-8")
p = re.split(r"(?m)^# (K-\d\d\d)", t)
kay = [(p[i], p[i+1]) for i in range(1, len(p), 2)]
uret = [k for k, g in kay if re.search(r"\*\*Üretici:?\*\*", g)]
sayi = re.compile(r"%\d|\d+,\d|\b\d{3,}\b")
tas  = [k for k, g in kay if sayi.search(g)]
print("toplam kayit          :", len(kay))
print("'**Üretici:**' satiri :", len(uret))
print("sayi tasiyan          :", len(tas))
print("sayi tasiyip uretici YOK:", len([k for k in tas if k not in uret]))
PY
```

**Beklenen / görülen:** toplam **55** kayıt · `**Üretici:**` satırı **18** ·
sayı taşıyan **55** · **sayı taşıyıp üretici satırı olmayan 37**
*(K-001…K-019, K-021, K-023…K-029, K-031, K-033, K-035, K-036, K-040, K-041,
K-044, K-045, K-046, **K-050**)*.

**Neden önemli:** B-57 *"ölçüldü ve tarihlendi"* diye **açık** bırakıldı; ama
bırakılırken yazılan sayı iç tutarsız ve bugün **37**. Bir bulgunun *"kısmen
açık"* durumu, ancak sınırı doğru ölçülmüşse bir taahhüttür. Ayrıca listede
**K-050** var — yani bu oturumda yazılan, `secim_avantaji` sayılarını taşıyan
kayıt üretici satırı taşımıyor *(B-65 tam o sayıların üzerine düştü)*.

**Öneri:** Kaydın çelişkili cümlesi revizyonla düzeltilsin *(K-020'de olduğu
gibi)* ve 26 Eylül taahhüdüne **37** yazılsın.

---

### B-75 · DÜŞÜK — `SAG_KALANLAR` listesi 203'lük havuzdan; bugün aynı komut 215'ten örnekliyor ve 7'nin yalnızca 1'i örnekte

| | |
|---|---|
| **Nerede** | `dogrulama/sag_kalan_ayikla.py:127-143` *(liste başlığı: "havuz 203 · taban 271")* · `v2/09-DEVIR-TESLIM.md:259` |
| **İDDİA** | `09:257-259`: *"**21 Ağustos itibarıyla — hepsi koşturularak ölçüldü:** … **215** kör mutant havuzu … **7 sağ kalan** *(hepsi eşdeğer)*."* |
| **ÖLÇTÜĞÜM** | Havuz bugün **215** *(doğru)*; ama 7 sağ kalan **203'lük havuzdan çekilmiş 24'lük bir örneklemin** ürünü. Bugün aynı tohumla çekilen 24'ün içinde **7'den yalnızca 1'i** var. |

**Üretici komut** *(depo kökünden)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import sys, random; sys.path.insert(0, ".")
from dogrulama.kor_mutasyon import mutantlari_uret, TOHUM
from dogrulama.sag_kalan_ayikla import SAG_KALANLAR
h = mutantlari_uret(); sec = random.Random(TOHUM).sample(h, 24)
print("bugunku havuz:", len(h))
for m in SAG_KALANLAR:
    e, y = m.eski.splitlines(), m.yeni.splitlines()
    ea, yb = [(a, b) for a, b in zip(e, y) if a != b][0]
    var = any(x.dosya == m.dosya and x.eski.strip() == ea.strip()
              and x.yeni.strip() == yb.strip() for x in sec)
    print("  %-38s bugunku 24'luk orneklemde: %s" % (m.ad, "EVET" if var else "hayir"))
PY
```

**Beklenen / görülen:** havuz **215**; `T06_ilet_jetonu_isareti` **EVET**,
diğer **6'sı hayır**. Yedisi de bugünkü **havuzda** var — ama örneklemde yok.

**Neden önemli:** `08:335-352` skor tablosunun *"iki tarama karşılaştırılamaz"*
uyarısını **doğru** yazıyor ve `09:261` havuz büyümesini **not ediyor**;
kapanmayan şey, **7 sağ kalan** kaleminin *"koşturularak ölçüldü"* envanterinin
içinde, kendi bayatlık notu olmadan durması. Üzerindeki tek testler
*(`test_b52_*`)* **yapısaldır** — her girdinin `yol` taşıdığına bakar,
girdilerin **bugünkü taramaya ait olup olmadığına** bakmaz. B-24'ün
*("araç doğru, girdisi bayat")* deseni, üçüncü kez.

**Öneri:** `sag_kalan_ayikla.py` başlığına, `kor_cikti.txt`teki gibi
**"KOD DURUMU / BAYAT"** satırı; ya da liste bugünkü örneklemden yeniden
türetilsin *(`kor_mutasyon.py 24` ≈ 18 dk)*.

---

### B-76 · DÜŞÜK — B-43'ün işaretleyicisi bir alanda YANLIŞ teste iliştirilmiş — hem de `05`'in *"EN ÖNEMLİ ALAN"*ına

| | |
|---|---|
| **Nerede** | `tests/test_gozlem.py:315` *(`@icerik_testi("son_iletim_sonucu")`)* |
| **İDDİA** | B-43'ün düzeltmesi: *"Artık kapsam, testlerin **kendisinden** türüyor"*; ve `test_b27b_her_gozlem_alaninin_icerik_testi_var` her alanın bir içerik testine bağlı olmasını zorluyor. |
| **ÖLÇTÜĞÜM** | `son_iletim_sonucu`u işaretleyen **tek** test `test_b02b_alici_kabul_etse_bile_gonderen_zaman_asimi_gorur` ve o test **`Gozlem.son_iletim_sonucu`u hiç okumuyor**: `k.mac.gonderim_bitti` geri çağrısını sarıp **MAC parametresini** inceliyor. Alanın gerçek içerik doğrulaması komşu testte *(`test_b02_…`, satır 303-305: `assert sonuclar == {"onay","zaman_asimi"}`)* ama o test yalnızca `son_iletim_hedefi` için işaretli. |

**Üretici komut** *(depo kökünden)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import sys, importlib.util; sys.path.insert(0, ".")
s = importlib.util.spec_from_file_location("tg", "tests/test_gozlem.py")
m = importlib.util.module_from_spec(s); s.loader.exec_module(m)
kay = {}
for ad in dir(m):
    for a in getattr(getattr(m, ad), "_gozlem_alanlari", frozenset()):
        kay.setdefault(a, []).append(ad)
for a in sorted(kay): print("%-20s %s" % (a, kay[a]))
PY
sed -n '315,338p' tests/test_gozlem.py    # govdede 'son_iletim_sonucu' GECMIYOR
```

**Beklenen / görülen:** `son_iletim_sonucu → ['test_b02b_alici_kabul_etse_bile_gonderen_zaman_asimi_gorur']`
ve o testin 36 satırlık gövdesinde `son_iletim_sonucu` **hiç geçmiyor**.

**Neden önemli:** Alan bugün **fiilen korunuyor** *(yanlış etiketli komşu test
sayesinde)* — yani bu bir güvenlik açığı değil, bir **muhasebe hatası**. Ama
sonucu şudur: `test_b02_…` silinse ya da adı değişse, `_icerik_testi_olan()`
`son_iletim_sonucu`u **hâlâ kapsanmış sayar** ve B-27b koruması **susar**.
B-43'ün kapattığı hata sınıfının *(«etiketi elle taşımak»)* düzeltmesinin
**içinde** kalmış bir örneği; `03` B5'in aynı satırı.

**Öneri:** işaretleyici `test_b02_…`e taşınsın *(gövdesi alanı gerçekten
okuyor)*; ve `icerik_testi` sarmalayıcısı, işaretlenen alan adının test
gövdesinde **geçtiğini** koşu anında doğrulasın — kaynağı zaten okunabilir
*(`inspect.getsource`)*, yani kontrol **davranışa** bağlanabilir.

---

### B-77 · DÜŞÜK — Aile 1 kontrol düzlemi bütçesi: bağımsız mesafe-vektörü kolu %15–36, gözlem kolu %1,7–1,9

| | |
|---|---|
| **Nerede** | K-009'un *"eşit kontrol düzlemi bütçesi"* adalet şartı · `sim/kosucu.py:295-305` |
| **ÖLÇTÜĞÜM** | Kendi yazdığım *(kâhinsiz)* mesafe-vektörü protokolü ile `gurultuden_kacan`ı aynı tohum/senaryoda koşturdum. |

**Üretici komut** *(depo kökünden, kendi kendine yeter)*:

⚠️ Seri koşar *(ölçüldü: **1,1 dk**, 12 koşu)* — gerekçe B-65'inkiyle aynı.

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import sys; sys.path.insert(0, ".")
from sim.config import Konfig
from sim.kosucu import Kosu
from dogrulama.aktaricilar import AKTARICILAR
def dv(kon):                       # KAHIN YOK: yalnizca Gozlem + beacon_yuku
    d = {"t": {}}
    def ogren(g):
        yeni = {g.dugum: (0, g.dugum)}
        for k in g.komsular:
            yeni.setdefault(k.dugum, (1, k.dugum))
            for ad, v in k.bildirdigi_yuk:
                if not ad.startswith("d"): continue
                try: h = int(ad[1:])
                except ValueError: continue
                if h == g.dugum: continue
                if h not in yeni or v + 1 < yeni[h][0]: yeni[h] = (v + 1, k.dugum)
        d["t"] = yeni; return yeni
    def s(g):
        t = ogren(g)
        if g.paket is None or not g.komsular: return None
        r = t.get(g.paket.hedef)
        if r is None or r[1] == g.dugum: return None
        return r[1] if any(k.dugum == r[1] for k in g.komsular) else None
    s.beacon_yuku = lambda dug: {("d%d" % h): m for h, (m, _) in
                                 (d["t"] or {dug: (0, dug)}).items() if m <= 8}
    return s
KOL = {"DV": dv, "gurultuden_kacan": AKTARICILAR["gurultuden_kacan"]}
for ad, fab in KOL.items():
    for sen in ("S0", "S2"):
        for t in (1, 2, 3):
            s = Kosu(Konfig(kol="t", senaryo=sen, trafik="orta", tohum=t), fab).kostur()
            print("%-18s %s t%d teslim=%.4f atlama=%s kontrol=%.2f%%"
                  % (ad, sen, t, s["teslim_orani"], s["ortalama_atlama"],
                     100.0*s["kontrol_bayt"]/(s["kontrol_bayt"]+s["veri_bayt"])))
PY
```

**Beklenen / görülen:**

| kol | senaryo | teslim *(3 tohum ort.)* | atlama | kontrol payı *(bayt)* |
|---|---|---|---|---|
| **DV** *(yük ilan eden)* | S0 | 0,2996 | **1,67** | **%26,0 – %35,6** |
| **DV** | S2 | 0,1949 | 1,12 | **%14,9 – %25,4** |
| `gurultuden_kacan` | S0 | 0,2928 | 4,61 | %1,68 – %1,87 |
| `gurultuden_kacan` | S2 | 0,2236 | 2,44 | %1,65 – %1,83 |

**Neden önemli:** İki kol **14–20 kat** farklı kontrol düzlemi bütçesi
harcıyor ve bunu **engelleyen ya da raporlayan bir mekanizma yok**. K-009'un
adalet şartı bugün yalnızca bir cümle. Ve B-66 nedeniyle DV'nin **gerçek**
maliyeti bu tablodakinden de büyük *(alan adı ve tamsayı büyüklüğü
sayılmıyor)*.

**Öneri:** `Konfig`e bir `kontrol_butce_bayt` tavanı ve `sonuc()`a
`kontrol_payi` alanı; ya da `06`ya *"iki kol kontrol payı %X içinde değilse
karşılaştırma yapılmaz"* ön-kaydı.

---

## 2. ÜÇÜNCÜ DENETİMİN BULGULARI — kapanma doğrulaması

**14 bulgu seçildi** *(istenen ≥10)*. Ölçüt: kapanma iddiasının **kendi
ölçütü kullanılmadı** — her biri ya bağımsız bir mutasyonla, ya bağımsız bir
ölçümle, ya ham baytla sınandı.

| # | kapanma iddiası | nasıl sınadım | sonuç |
|---|---|---|---|
| **B-41** | `BEKLENEN_MUTASYON = 35` sabiti eklendi | Sabiti **5'e düşüren** bağımsız mutasyon *(U4-24)* + `read_bytes()` ile satırın kodda olduğu doğrulandı | *(bkz. §5)* |
| **B-42** | Kapının kapsamı `zorunlu` desenleriyle korunuyor | Korumanın **kendisini** boşa çıkaran mutasyon *(U4-23: `eksik_zorunlu → set()`)* | *(bkz. §5)* |
| **B-43** | Kapsam artık işaretleyiciden **türüyor** | İşaretleyici→alan haritası çıkarıldı ve **her işaretin gövdesiyle** karşılaştırıldı | 🟡 **mekanizma kapandı, bir etiket yanlış** → **B-76** |
| **B-44** | `olculen_gurultu_w` içerik testi | Girişim terimini kaldıran bağımsız mutasyon *(U4-20)* — B-44'ün mutasyonundan **farklı** *(o sabit tabana çakıyordu, bu yalnızca komşu iletimlerini siliyor)* | *(bkz. §5)* |
| **B-45** | Kapı `secim_avantaji_ortalama`ya taşındı | **Üçüncü ve dördüncü null model** + 8 tohumluk tarama + sebep deneyi | 🔴 **KAPANMADI** → **B-65** |
| **B-46** | Sonuç satırı `kaynak_hash` taşıyor | Şemada var *(`kosucu.py:520`)*; `test_b46_*` üç vaka. **Dördüncü eksen** arandı | 🟢 eksen kapalı · ama satır **içi** eksen açık → **B-67** |
| **B-47** | Protokol→çerçeve kanalı açıldı | Kanalı **bağımsız yazdığım DV protokolüyle** kullandım; bedel modelini zorladım | 🟢 kanal çalışıyor · 🔴 **bedeli kaçırılabiliyor** → **B-66**, **B-70** |
| **B-48** | Bant `Konfig`ten türüyor | `_kos()` ile özel bantlı koşu; `ara_bolge_per_bandi` sonuç satırında | 🟢 **kapalı** *(bant `(0.05, 0.9)`, sonuçta `[0.05, 0.9]`)* |
| **B-49** | `protokol_teshis` slotu **taşıdığı gösterildi** | Slota giden **meşru** yol arandı | 🔴 **yok** → **B-68** |
| **B-52** | Her sağ kalan girdisi `yol` taşıyor; 3'ü `YOLSUZ` | Üç `YOLSUZ` mutasyonu geçici kopyaya uygulanıp **4 kurulumda tam sonuç sözlüğü** tabanla karşılaştırıldı | 🟢 **3/3 beyan doğru** *(ayrıntı §3)* |
| **B-53** | *"dört alan"* → **dokuz** | Kaydın **kendi tarama tarifi** bağımsız kodla yeniden yazıldı | 🟢 **dokuz** *(birebir)* |
| **B-54** | Kaçırılan beacon sayacı korumaya alındı | `kacirilan_yayin += 1` → `pass` *(U07'nin birebir tekrarı; bu yüzden §5'in oranına **girmiyor**, yalnızca kapanma kontrolü)* | *(bkz. §5)* |
| **B-57** | Ölçüldü ve **açık** bırakıldı | Kaydın kendi üretici tarifi yeniden koşuldu | 🔴 **kayıt iç çelişkili** → **B-74** |
| **B-58** | *"Ayraç hiçbir şey yapmıyor"* **çürütüldü** | `pathlib.Path("sim/kosucu.py").read_bytes()` | 🟢 **çürütme doğru**: bayt dizisi `b'h.update(b"\x1f")'` — gerçek 0x1F. Üçüncü denetimin öz düzeltmesi **haklı** |
| **B-60** | `ULASILABILIRLIK_YOK` nöbetçisi zorunlu | Nöbetçinin **kapsamı dışındaki** dört girdi denendi *(Y11)* | 🔴 **üç bypass** → **B-71** |
| **B-64** | `ciktilar/` üç dosyaya tarih + kod durumu | Üç dosyanın ilk 6 satırı okundu | 🟢 **kapalı** *(üçünde de başlık var; `kor_cikti.txt` açıkça **BAYAT**)* |

### 🔴 *"Test fazla dar mı"* — mutasyonu DEĞİŞTİRME denemesi

Üç kapanış testinin, denetçinin yazdığı **tek** mutasyonu değil, **komşu**
mutasyonu da yakalayıp yakalamadığını sınadım:

| kapanış | denetçinin mutasyonu | benim **komşu** mutasyonum | sonuç |
|---|---|---|---|
| B-44 | `olculen_gurultu_w` = sabit gürültü tabanı *(U14)* | **yalnızca komşu iletimlerinin katkısı** silindi; karıştırıcı terimi **duruyor** *(U4-20)* | §5 |
| B-50/B-54 | `en_yuksek_doluluk` **bir eksik** *(U06)* | `en_yuksek_doluluk` = **son değer** *(tepe değil)* *(U4-04)* | §5 |
| B-53 | `kuyruk_doluluk` **iki kat** *(U09)* | `kuyruk_doluluk` = **mutlak sayı** *(oransız)* *(U4-15)* | §5 |

---

## 3. DOĞRULANAN İDDİALAR

Hepsi **bağımsız olarak yeniden üretildi** *(iddianın kendi ölçütü
kullanılmadan)*. Üretici komutlar depo kökünden koşar.

| # | iddia | kaynak | ölçtüğüm | durum |
|---|---|---|---|---|
| 1 | Seçim avantajı: kör **−0,167** · bilgili **+0,037** · null **+0,008** ve **−0,012** | `06:355-359` | **−0,16708 · +0,03695 · +0,00809 · −0,01199** | ✅ **birebir** *(tohum 1)* |
| 2 | Yük bayt muhasebesi **10,0 bayt/beacon** *(2 alan)* | `test_gozlem.py:768` | `yuk_bayt_toplam / beacon_gonderilen = 10,0` | ✅ **birebir** |
| 3 | Kanal kanıtı: mesafe-vektörü kolu **S0'da atlama 1,00 → 2,33** | K-049 | **Kendi yazdığım** DV protokolü, S0/tohum 1: **2,33**; S2/tohum 1: **1,00** | ✅ **birebir** — ve projenin *"S2'de düşüyor, ayarlanmadı"* kaydı da doğru |
| 4 | Kör tarama havuzu **215** *(203'ten büyüdü)* | `09:258` | `len(mutantlari_uret()) = 215` | ✅ |
| 5 | Güç analizi: %70→%40 için **n = 16**, %70→%50 için **n = 35** | K-055 | Normal yaklaşımla **9 · 16 · 35 · 136** — **dördü de birebir** | ✅ *(⚠️ ama bkz. §6-13: TAM binom farklı söylüyor)* |
| 6 | `08` madde 22: gözlem penceresinin **DOKUZ** alanının tüketicisi yok | `08:260` | Bağımsız tarama: **dokuz** *(`saat_s`, `olculen_gurultu_w`, `kanal_mesgul_mu`, `kuyruk_uzunlugu`, `kuyruk_kapasitesi`, `son_iletim_sonucu`, `son_iletim_hedefi`, `gonderilen_bayt`, `alinan_bayt`)* | ✅ **birebir** |
| 7 | B-58 çürütmesi: ayraç `b"\x1f"` **gerçek** | K-052 | `read_bytes()` → `b'h.update(b"\x1f")'` | ✅ **çürütme haklı** |
| 8 | Analitik ortalama derece **7,44258** | `topology.py:66` | Kapalı formdan sayısal integral: **7,44259** | ✅ |
| 9 | Girişim menzili iletim menzilinin `β^(1/α)` katı | `03`/`config` | `2,154435 × 280 = 603,2417` = `kon.girisim_menzili_m` | ✅ **birebir** |
| 10 | Ç2.2 — sonuç `PYTHONHASHSEED`ten bağımsız | Ç2 | `PYTHONHASHSEED=0` ve `=12345` ile tam sonuç sözlüğünün blake2b'si **aynı** *(`32ce1a8137ede988`)* | ✅ |
| 11 | Ana deney tohumları *(2000–2029)* hiçbir yerde kullanılmıyor | K-025 | `tests/`, `dogrulama/`, `sim/` taraması: **0 eşleşme**; `TOHUM_TAM = range(1, 31)` | ✅ |
| 12 | B-52: üç `YOLSUZ` beyanı doğru | K-053 | T03 · T05 · T06 geçici kopyaya uygulandı, **4 kurulumda** *(S2/orta, S0/orta, `dongu_yapan`/S0, S4/yoğun)* tam sonuç sözlüğü tabanla karşılaştırıldı → **fark yok** | ✅ *(kapsam notu aşağıda)* |
| 13 | Envanter: 324 test · 35 hedefli mutasyon · 55 karar kaydı · 24 kapsam maddesi | `README`/`09` | `--collect-only` → **324**; `len(MUTASYONLAR)` → **35**; `# K-\d\d\d` → **55**; `08` madde listesi → **24** | ✅ |
| 14 | Testlerde mühürsüz rastgelelik yok | — | `tests/` içinde tek `random` kullanımı `random.Random(42)` | ✅ |
| 15 | Belge atıfları kırık değil | K-055 | 4 dosyadaki tüm markdown bağları + backtick yol atıfları tarandı: **kırık atıf yok** *(tek "kırık" görünen satır, K-055'in **düzeltilen** atıfları anlatan cümlesi)* | ✅ |

⚠️ **12 numaranın kapsam notu (Y9 — kendi hipotezimi geri alıyorum):**
T06'nın *(`m.jeton += 1` → `-= 1`)* `YOLSUZ` beyanına **itiraz edecektim**:
jeton başka yerlerde `+= 1` ile artıyor, dolayısıyla `-= 1` bir değeri
**yeniden ziyaret edebilir** ve iptal edilmiş bir olay canlanabilir. Dört
kurulumda **ölçtüm, olmadı** — tam sonuç sözlüğü birebir aynı. İddiam
çürüdü; beyan **bu dört kurulumda** doğru. *"Tetiklenebilir yol yok"*
kanıtlanmış değil, **desteklenmiş** durumda.

---

## 4. ÜRETİLEMEYEN / SINANAMAYAN İDDİALAR

| iddia | neden üretilemedi |
|---|---|
| **Kapı 13/13 · 98,2 dk** *(Ç1.1 540/540 · Ç1.4 %0,156 · Ç4.2 1/6,29 · GA %2,04)* | `aile0_kapi_raporu.py` **98 dk**; 30 dk bütçe sınırının çok üstünde ve mutasyon paketi *(zaten ~90 dk)* koşarken başlatılamazdı. **Kapıyı bu denetimde koşturmadım.** Kapının **girdilerini** ayrı ayrı denetledim *(mutasyon paketi eşiği, kapsam koruması, seçim listeleri, mutasyon listesi uzunluğu)*. |
| ⭐ *"Ç1.4 ve Ç4.2 üç koşuda birebir aynı ⇒ RNG çekim sırası kaymadı"* | Çıkarımın **kendisi** sınandı, sayılar değil — bkz. §6-7. Kalibrasyon tablosu *(B-28'in kaydığı yer)* bu denetimde de **yeniden ölçülmedi** *(~2 dk, ama kapının ölçtüğü şey değil)*. |
| K-020'nin revize sayıları *(ara bölge 6–14, ortalama 9,8; payda 145,4)* | 10 tohumluk yeniden ölçüm; mutasyon koşusuyla çakışırdı. **Sınamadım.** |
| `08` madde 12 *(alıcı kilidi %0,028)* · madde 15 *(S0 tabanı 0,9938, 90 koşu)* | Her biri onlarca koşu; bütçe mutasyon paketine gitti. **Sınamadım.** |
| Kör tarama skoru **%55,6 (10/18)** | Bugünkü kodla **tanım gereği** üretilemez *(havuz 203→215, örneklem tamamen değişir)*. `08` bunu **doğru** beyan ediyor; ölçtüğüm ek şey §1/B-75'te. |

---

## 5. 🔴 KENDİ MUTASYONLARIM — 24 mutasyon

**Kural 3 uyumu:** hiçbiri mevcut **35 hedefli** mutasyonun, **215 mutantlık
kör havuzun** ya da önceki denetimlerin **D1–D10 · KM1–KM10 · U01–U15**
mutasyonlarının tekrarı **değil** — **iki istisna dışında**, ve o ikisi
oranın paydasından **çıkarıldı** *(aşağıda)*.

**Yeni yol araması:** hedefli 35 mutasyonun **35'i de** `sim/` altında ve kör
tarayıcı **yalnızca `sim/`**e bakıyor *(`kor_mutasyon.py:56`)*. Bu yüzden
mutasyonlarımı, **hiç hedefli mutasyonu olmayan altı dosyaya** ve **hiç
mutasyon görmemiş `dogrulama/` dizinine** yaydım:
`events.py` · `ledger.py` · `topology.py` · `traffic.py` · `gozlem.py` ·
`queues.py` · `aile0_kapi_raporu.py`.

**Yöntem** *(üçüncü denetimin yöntemiyle aynı, `03` kural 15 dâhil)*:
her mutasyon **geçici bir kopyaya** uygulandı, uygulandıktan sonra dosya
**yeniden okunarak** hem eski desenin gittiği hem yeninin geldiği doğrulandı,
`ast.parse` ile sözdizimi denetlendi, sonra **TAM 324 testlik paket** o
kopyada koşuldu. **Taban (mutasyonsuz kopya) aynı yoldan koşuldu ve temiz
çıktı: `324 passed in 1034.00s`** *(Y7)*. Hiçbir mutasyon geçersiz olmadı
*(çökme/collect hatası yok, `err=0`)*.

**Üretici komut:** `scratchpad/mut4.py` *(betiğin tamamı bu raporun
dışında; ama her mutasyonun `dosya` + `eski` + `yeni` üçlüsü aşağıdaki
tabloda tam olarak yazılı, yani depo kökünden yeniden kurulabilir)*.
**Ölçülen süre: 58,0 dk** *(25 tam paket koşusu, 8 paralel; koşu sırasında
makinede başka ölçümler de vardı)*.

### Y8 ÖN KOŞULU — her mutasyonun bozduğu yolun SAĞLAM koşuda tetiklendiği ÖNCE ölçüldü

Ölçüm, depo değiştirilmeden çalışma zamanı sarmalayıcılarla yapıldı
*(S2/orta/tohum 1 ve S0/orta/tohum 1, `en_kisa_yol`)*.

| # | mutasyon | dosya | **Y8 · sağlam koşuda tetiklenme** | 324 test | sınıf |
|---|---|---|---|---|---|
| **U4-01** | olay eşitlik sırası ters *(`+sira` → `-sira`)* | `events.py` | **212** aynı-zamanlı ekleme | ✅ yakalandı **2** test | mekanizma |
| **U4-02** | `islenen_olay += 1` → `pass` | `events.py` | **434 571** olay işlendi | 🔴 **SAĞ KALDI** | sayaç |
| **U4-03** | kuyruk FIFO → **LIFO** | `queues.py` | **96** kez `len>1` iken `al()` | ✅ yakalandı **4** test | mekanizma |
| **U4-04** | `en_yuksek_doluluk` tepe → **son değer** | `queues.py` | **7 236** tepe-altı ekleme | ✅ yakalandı **1** test | sayaç |
| **U4-05** | `tasma_sayisi += 1` → `pass` | `queues.py` | **904** taşma *(`dongu_yapan`/S0)* | ✅ yakalandı **2** test | sayaç |
| **U4-06** | `dusen_toplam` bir kovayı saymıyor | `ledger.py` | **2 246** `iletim_basarisiz` düşme | ✅ yakalandı **26** test | mekanizma |
| **U4-07** | korunum raporunda `fark` → `0` | `ledger.py` | `kontrol()` her koşuda | ✅ yakalandı **2** test | sayaç |
| **U4-08** | mesafe Öklid → **Manhattan** | `topology.py` | **833 493** çağrı | ✅ yakalandı **7** test | mekanizma |
| **U4-09** | `ortalama_derece` → `max(derece)` | `topology.py` | `ozet()` her koşuda | ✅ yakalandı **1** test | sayaç |
| **U4-10** | girişim menzili = iletim menzili | `topology.py` | `cs_komsu` kurulumu | ✅ yakalandı **13** test | mekanizma |
| **U4-11** | CBR titreşimi **asimetrik** | `traffic.py` | **3 198** üretim | ✅ yakalandı **4** test | mekanizma |
| **U4-12** | tüm akışlar t=0'da başlıyor *(rezonans)* | `traffic.py` | akış başına 1 | ✅ yakalandı **4** test | mekanizma |
| **U4-13** | `YUK_ALAN_KIMLIK_BAYT` 1 → **0** | `gozlem.py` | kanca Aile 0 sim'inde 0, **test paketinde** tetikleniyor | ✅ yakalandı **1** test | sayaç |
| **U4-14** | demet yükü **eleman sayısından bağımsız** | `gozlem.py` | aynı | 🔴 **SAĞ KALDI** | sayaç |
| **U4-15** | `kuyruk_doluluk` oran → **mutlak** | `gozlem.py` | gözlem her kararda *(7 342)* | 🔴 **SAĞ KALDI** | sayaç |
| **U4-16** | `yuku_dondur` **sıralamasız** | `gozlem.py` | aynı | 🔴 **SAĞ KALDI** | sayaç |
| **U4-17** | kopya önbelleği **ağa ortak** | `mac.py` | **261** kopya alım | 🔴 **SAĞ KALDI** | **mekanizma** |
| **U4-18** | ikili üstel geri çekilme yok | `mac.py` | **10 035** cw büyüme | ✅ yakalandı **5** test | *(U08'in tekrarı)* |
| **U4-19** | taşıyıcı dinleme **CCA penceresini yok sayıyor** | `mac.py` | **258** CCA-içi gizli iletim | ✅ yakalandı **5** test | mekanizma |
| **U4-20** | `olculen_gurultu_w`den **komşu girişimi** silindi | `mac.py` | 21 342 çağrının **7 962**'sinde girişimci var | ✅ yakalandı **1** test | mekanizma |
| **U4-21** | `kacirilan_yayin += 1` → `pass` | `mac.py` | **52** kaçırılan | ✅ yakalandı **1** test | *(U07'nin tekrarı)* |
| **U4-22** | beacon alıcısına **yük kredisi yok** | `mac.py` | 66 722 beacon alımı | 🔴 **SAĞ KALDI** | sayaç |
| **U4-23** | `eksik_zorunlu()` → `set()` *(B-42'nin koruması)* | `aile0_kapi_raporu.py` | her kapı kriterinde çağrılıyor | ✅ yakalandı **1** test | araç |
| **U4-24** | `BEKLENEN_MUTASYON` 35 → **5** *(B-41'in sabiti)* | `aile0_kapi_raporu.py` | Ç1.3'te kullanılıyor | ✅ yakalandı **1** test | araç |

⚠️ **U4-18 ve U4-21, üçüncü denetimin U08 ve U07'sinin birebir tekrarıdır.**
Bunu mutasyonları yazdıktan **sonra** fark ettim *(`aile0_audit.md:3195-3199`)*.
İkisi de **yakalandı** — yani B-54'ün ve `test_cw_ikili_ustel_buyuyor`un
kapanışını doğruluyorlar *(§2)*. **Oranın paydasından çıkarılmış hâlleri de
aşağıda verilmiştir.**

---

### 🔴 SAĞ KALANLARIN DAVRANIŞI GERÇEKTEN DEĞİŞİYOR MU?

**İki ayrı ölçüm yapıldı** — çünkü *"eşdeğer"* ile *"o alanın hiç tüketicisi
yok"* **aynı çıktıyı verir** ve ikincisi asıl bulgudur:

1. **Sonuç sözlüğü ölçütü** *(`sag_kalan_ayikla.py`nin ölçütü)* — mutasyon
   geçici kopyaya uygulanıp **6 kurulumluk** matriste koşuldu *(S2/orta,
   S0/orta, `dongu_yapan`/S0, S4/yoğun, `gurultuden_kacan`/S2, **yük taşıyan
   kol**/S0)* ve tam `sonuc()` sözlüğü tabanla karşılaştırıldı.
2. 🔴 **Gözlem penceresi ölçütü** *(bu denetimin eklediği)* — aynı mutasyonlar
   için, protokolün karar anında **fiilen gördüğü** `alinan_bayt`,
   `kuyruk_doluluk` ve `bildirdigi_yuk` değerleri kaydedilip karşılaştırıldı.
   Sonuç sözlüğü bu alanları **taşımıyor**, dolayısıyla birinci ölçüt onları
   *"eşdeğer"* gösterir.

| sağ kalan | sonuç sözlüğü | gözlem penceresi | **karar** |
|---|---|---|---|
| **U4-02** `islenen_olay` | 🔴 **6/6 kurulumda değişti** *(434 571 → 0 · 340 515 → 0 · 8 479 981 → 0 · …)* | — | **TÜKETİCİSİZ** — şema alanı her satıra yazılıyor, **okuyan yok** |
| **U4-14** demet yükü bedeli | 🔴 **28 alan değişti** *(yalnızca yük taşıyan kolda: `kontrol_bayt` 925 526 → 812 784, `kontrol_airtime_s` 12,225 → 11,313 s, teslim 2 698 → 2 696)* | — | **KAPSANMAYAN YOL** — test paketinde **demet taşıyan tek bir kol yok** |
| **U4-15** `kuyruk_doluluk` | ⚪ değişmedi | 🔴 **`kuyruk_doluluk_max` 0,04 → 2,0** *(50 kat)*, toplam 212,78 → 10 639,0 | **TÜKETİCİSİZ** |
| **U4-16** `yuku_dondur` sırası | ⚪ değişmedi | 🔴 **alan sırası `(etx, kim, kom)` → `(etx, kom, kim)`** | **TÜKETİCİSİZ** — ve belirlenimcilik güvencesi kayboluyor |
| **U4-22** beacon alım kredisi | ⚪ değişmedi | 🔴 **`alinan_bayt` toplamı 5 681 479 150 → 5 292 348 910** *(−%6,8)*, tepe −%3,6 | **TÜKETİCİSİZ** → **B-70** |
| **U4-17** kopya önbelleği ortak | ⚪ değişmedi | ⚪ **değişmedi** | ✅ **GERÇEK EŞDEĞER** *(aşağıda)* |

⚠️ **U4-17 hakkında — kendi hipotezimi geri alıyorum (Y9).** Kopya
önbelleğini ağa ortak yapmanın **davranışı değiştireceğini** varsaymıştım.
Ölçtüm, değiştirmiyor — ve sebebi yapısal: anahtar `(gonderen, sira)` ve
`sira` her `gonder()` çağrısında gönderen tarafından **bir kez** atanıyor,
üstelik bir veri çerçevesini yalnızca **hedeflenen alıcı** işliyor
*(`_veri_bitti` → `alici = il.alan`)*. Dolayısıyla her anahtar **ağ genelinde
tekil** ve düğüm başına indeksleme bugün **fazlalıktır**. 🔴 Ama bu bir
**savunma fazlalığıdır**: karışık mod alım *(promiscuous)* ya da yayın
çerçevesi kopya bastırma eklendiği gün, ortak önbellek sessizce yanlış cevap
verir. **Bugün bir boşluk değil; bir bağımlılıktır ve `08`de yazılı değildir.**

🔴 **Sonuç: 6 sağ kalanın 5'i *"tüketicisiz"*, 1'i **gerçek eşdeğer**.
Davranışı değiştirip de KORUMASIZ kalan tek bir MEKANİZMA yolu bulamadım.**

---

### 🔴 SAĞ KALAN ORANI · SERİ · ULAŞILAN GÜÇ

| denetim | mutasyon | sağ kalan | taban | oran |
|---|---|---|---|---|
| Birinci | 10 | 8 | 198 test | %80,0 |
| İkinci | 10 | 7 | 240 test | %70,0 |
| Üçüncü | 15 | 10 | 284 test | %66,7 |
| **Dördüncü — bu denetim** | **24** | **6** | **324 test** | **%25,0** |

| payda | sağ kalan | oran | %95 GA *(Clopper–Pearson)* | tek yönlü p *(H0: p = 0,70)* |
|---|---|---|---|---|
| **24** *(hepsi)* | 6 | **%25,0** | **[0,098 · 0,467]** | **0,000007** |
| 22 *(2 birebir tekrar çıkarıldı)* | 6 | %27,3 | [0,107 · 0,502] | 0,000044 |
| 19 *(3 «varyant» da çıkarıldı)* | 5 | %26,3 | [0,091 · 0,512] | 0,000108 |

### 🔴 ULAŞILAN GÜÇ

**Tek örneklem binom · tek yönlü · α = 0,05 · H0: p = 0,70 · TAM binom**
*(normal yaklaşım değil — K-055 normal yaklaşım kullanmış, bkz. §6-13)*

| n | red bölgesi | gerçek α | güç *(p₁ = 0,40)* | güç *(p₁ = 0,50)* | %80 güç eşiği |
|---|---|---|---|---|---|
| 10 *(1. ve 2. denetim)* | X ≤ 4 | 0,0473 | 0,633 | 0,377 | p₁ ≤ 0,326 |
| 15 *(3. denetim)* | X ≤ 6 | 0,0152 | 0,610 | 0,304 | p₁ ≤ 0,332 |
| 16 *(K-055'in bağlayıcı eşiği)* | X ≤ 7 | 0,0257 | **0,716** | 0,402 | — |
| **24 *(bu denetim)*** | **X ≤ 12** | **0,0314** | **0,886** | **0,581** | **p₁ ≤ 0,435** |

**Şart karşılandı:** n = 24 ≥ 16 *(K-055'in bağlayıcı eşiği)* ve ≥ 19 *(aynı
hedefin TAM binomla hesaplanmış hâli)*. Gözlenen 6/24, red bölgesinin
*(X ≤ 12)* çok içinde; **H0: p = 0,70 reddedilir** *(p = 7×10⁻⁶)*.

---

### 🔴 AMA ÖRÜNTÜ KAPANMADI — **DARALDI.** *(Y6)*

⭐ **Y6: beklenenden iyi çıkan sonuç, kötü çıkan kadar şüphelidir.** %80 → %70
→ %66,7 serisinden sonra **%25,0** görmek, ilk bakılması gereken yerin
**örneklemim** olduğunu söyler. Baktım:

**(a) Katman analizi — asıl cevap burada.** Mutasyonlarımı üç katmana ayırdım
*(sınıflandırma tabloda; ölçüt: mutasyon bir **mekanizmayı** mı yoksa bir
**sayaç/raporlama alanını** mı bozuyor)*:

| katman | sağ kalan | oran | %95 GA | p *(H0: p = 0,70)* |
|---|---|---|---|---|
| **sayaç / raporlama alanı** | **5/11** | **%45,5** | **[0,167 · 0,766]** | **0,078 → H0 REDDEDİLEMEZ** |
| **mekanizma** | 1/11 | %9,1 | [0,002 · 0,413] | 0,00005 → reddedilir |
| doğrulama aracı | 0/2 | %0,0 | [0,000 · 0,842] | 0,090 |

⚠️ Mekanizma katmanındaki **tek** sağ kalan *(U4-17)* **gerçek eşdeğer**
çıktı; yani **korumasız mekanizma yolu sayısı 0/11**. Sayaç katmanındaki
**beşinin beşi de** tüketicisiz.

🔴 **Önceki üç denetimin mutasyonları ağırlıklı olarak SAYAÇ katmanındaydı**
*(U01 `ara_bolge_per_bandi`, U02 `protokol_teshis`, U05 `boruda_kalan`,
U06 `en_yuksek_doluluk`, U07 `kacirilan_yayin`, U09 `kuyruk_doluluk`,
U13 kopya baytı, U14 gözlem gürültüsü — 10 sağ kalanın **8'i**)*. O katmanda
oranım **%45,5** ve **%70 hipotezi reddedilemiyor.** Yani genel orandaki
düşüşün büyük kısmı, **örneklem karışımının değişmesinden** geliyor.

**(b) `sim/kosucu.py`ye HİÇ mutasyon koymadım.** Üçüncü denetimin 15
mutasyonunun **7'si** oradaydı ve **4'ü sağ kaldı** *(%57)*. Bu, oranımın
**en büyük tek yanlılık kaynağıdır** ve `03` B2'nin *"gürültüden dar tarama"*
kuralının bu rapordaki karşılığıdır — bir dosyayı örneklemden çıkarmak,
o dosyanın oranını **görünmez** yapar.

**(c) Yönü ters olan kanıt da var.** Doğrulama araçlarına *(`dogrulama/`,
3 664 satır, bugüne kadar **sıfır** mutasyon)* koyduğum iki mutasyonun
**ikisi de yakalandı** — B-41 ve B-42'nin korumaları **gerçekten ısırıyor**.
Ve mekanizma katmanında oran **%9,1**: FIFO→LIFO, Manhattan mesafe, girişim
menzili çökertme, rezonans, CCA penceresi — beşi de anında yakalandı.

**🔒 SONUÇ CÜMLESİ:** n = 24 ile *"örüntü kapandı"* demeye **yetkim var**
*(n ≥ 16 ve n ≥ 19)*, ve genel oran gerçekten düştü. Ama **öyle demiyorum**:
örüntü kapanmadı, **daraldı**. Simülatörün **mekanizma** yüzeyi artık
sağlam görünüyor *(%9,1)*; korumasız kalan yüzey **sayaç ve raporlama
alanlarıdır** *(%45,5, H0 reddedilemiyor)* — ve o yüzey Aile 1'in
**sonuç şemasıdır.**

---

## 6. ŞÜPHE LİSTESİ SONUÇLARI

| # | şüphe | sonuç |
|---|---|---|
| **1** | Ön-kayıtlı kapı değişti — meşru mu? | 🟡 **Değişiklik meşru, sonucu değil.** Eski ölçütün *(ara bölge oranı)* bilgiyi ölçmediği **ölçümle** gösterildi *(B-45)*, eşik geriye dönük **gevşetilmedi** — ölçüt **değiştirildi** ve gerekçesi `06`ya yazıldı; `03` kural 3'ün yasakladığı şey *"eşiği gevşetmek"*tir, *"ölçülemez olduğu kanıtlanan ölçütü değiştirmek"* değil. **Ama** yerine konan ölçüt de bilgiyi ölçmüyor *(kalıcılığı ölçüyor)* ve tek tohumda kalibre edilmiş → **B-65**. Yani `03` kural 3 ihlal edilmedi; **kural 2 ihlal edildi.** |
| **2** | Yeni ölçüt kendi null'ünü SENİN null'ünle geçiyor mu? | 🔴 **HAYIR.** Üçüncü null *(`g.komsular[0]` — hiçbir ALAN okumaz, yalnızca tablo sırası)*: **+0,064**. Dördüncü null *(`g.komsular[-1]`)*: **+0,057** — ve **hiç paket teslim etmiyor** *(3 tohumda da teslim = 0,0000)*. Beşinci null *(`duyulan_beacon` en çok olan)*: **+0,087**, bilgili koldan **yüksek**. → **B-65** |
| **3** | Protokol→çerçeve kanalı bedelsiz bilgi taşıyor mu? | 🔴 **EVET.** Bedel **tipe** bağlı: alan adı uzunluğundan, tamsayı büyüklüğünden bağımsız. Ölçüldü: **10 bayt bedelle ≥1 236 bayt** *(124×)*; sentetik tavan **20 205×**. Beacon dışı çerçevelere kanca yok *(kontrol edildi: yalnızca `_beacon_at`)*. → **B-66** |
| **4** | Y11'in dördüncü ekseni | 🔴 **BULUNDU.** Üç eksen *(paket evreni · kurulum · kod)* **kollar arası**; **satır içi** yapı hiç denetlenmiyor. Dört ayrı vaka kabul edildi: kırpık gecikme listesi *(846,7 ms uydurma fark)*, tekrarlı kimlik, NaN, negatif gecikme. → **B-67** |
| **5** | Kapının kapsam listesi elle yazılmış | 🟡 **Risk var ama zannedildiği kadar büyük değil.** `zorunlu` desenleri elle; ve desen **kimliğe** bakıyor, **içeriğe** değil — aynı önekli boş bir test korumayı susturur. **Ama** kapının Ç1.3 kolu `mutasyon_paketi.paketi_kostur()` → `taban_kontrolu()` üzerinden **324 testin tamamını** koşuyor ve taban kırıksa Ç1.3 düşüyor; yani hiçbir test kapının **tamamen** dışında değil. Ayrıca `test_kapi_secimleri.py` hem sayıyı hem kapsamı saniyeler içinde denetliyor *(12 sn)*. Kalan gerçek boşluk: **desenin içerik değil ad eşleşmesi** olması → §7'ye madde. |
| **6a** | `08`de *"yapmaz"* denen bir şey **yapılıyor** mu? | 🔴 **EVET, bir tane:** madde 24 yükün maliyet modelini *"alan kimliği 1 B · int/float 4 B"* diye ilan edip **yönünü** *"maliyeti gerçeğe göre AZ gösterir"* diyor — ama **ne kadar** az olabileceğini sınırlamıyor; ölçtüm: **20 000×**. Ve `gozlem.py:210` *"maliyet gerçek serileştirmeden hesaplanır"* diyor; hesaplanmıyor. → **B-66** |
| **6b** | Kodda modellenmemiş ama listede **olmayan** bir şey var mı? | 🔴 **DÖRT madde** → §7 |
| **7** | Şema donduruldu mu, gerçekten? | 🟡 **`protokol_teshis` keyfi anahtar kabul ediyor — ama kapı değil, ÇIKMAZ.** Slota **meşru** hiçbir yazma yolu yok *(B-68)*; yani şema *"açık bir slotla donduruldu"* değil, *"doldurulamaz bir slotla donduruldu"*. Şemayı değiştirmenin hâlâ açık yolu: `sonuc()` sözlüğüne alan eklemek — bunu engelleyen bir test **yok** *(`test_b30_…semada_var_ve_tam` yalnızca **varlığı** sınıyor, kümenin **sabitliğini** değil)*. → §7'ye madde |
| **8** | B-57 kapatılmadı — savunulabilir mi? | 🟡 **Gerekçe savunulabilir, sayısı değil.** *"Uydurmak daha ağır ihlal"* doğru bir gerekçe. Ama kaydın kendi sayısı iç çelişkili *(30 kaydın 35'i)* ve bugünkü doğru sayı **37**. Ayrıca **K-050** — bu oturumda yazılan ve B-65'in üzerine düştüğü kayıt — üretici satırı taşımıyor. → **B-74** |
| **9** | Belge rafineleştirmesi bir şey bozdu mu? | 🟢 **Hayır.** 4 dizindeki tüm markdown bağları ve backtick yol atıfları tarandı: **kırık atıf yok**. `ciktilar/` üç dosyasının üçünde de tarih + kod durumu başlığı var *(B-64 kapalı)*. Envanter sayılarının **hepsi** koşturularak doğrulandı. Tek kusur: `09:259`daki *"7 sağ kalan"* kalemi → **B-75** *(düşük)*. |
| **10** | Aile 1 gerçekten kurulabilir mi? | 🟢 **Evet, kurulabilir** — kendi DV protokolümü yazdım, koştu: S0/tohum 1'de atlama **2,33** *(projenin sayısıyla birebir)*. 🔴 **Ama savunma eksik:** S2'de 1,00'e düşmesi *"ayarlanmadı"* ile açıklanıyor; **ölçtüğüm ek şey**, kolun kontrol düzlemi payının **%15–36** olması *(gözlem kolu %1,7)*. Bu, `03` kural 4'ün *"rakibi ayarla"* sorunundan **başka** bir sorun: K-009'un eşit bütçe şartı **yapısal olarak** zorlanamıyor. → **B-77** |
| **11** | İstatistik katmanı hâlâ YOK | 🟢 **Beyan doğru, ama artık yetmiyor.** `grep -rn "wilcoxon\|holm\|scipy" --include=*.py .` → **0 eşleşme** *(doğrulandı)*. `08` madde 21 bunu beyan ediyor. **Ama** beyanın dayandığı varsayım *("Aile 0 sonuç üretmiyor, katman Aile 1'den önce yazılır")* artık tam doğru değil: `ortak_alt_kume` **bugün** NaN'ı sessizce taşıyor ve `gecikme_farki_s = nan` döndürüyor → **B-67**. Yani NaN riski istatistik katmanının **öncesine** taşınmış. |
| **12** | Bu promptun kendisi — neye bakmamı istemiyor olabilir? | Liste **on bir** yere bakmamı istedi; hepsine baktım. **Listede olmayan** dört yere de baktım ve üçünden bulgu çıktı: *(a)* `sim/events.py` · `sim/ledger.py` · `sim/topology.py` · `sim/traffic.py` — **hiç hedefli mutasyonu olmayan dört dosya** *(§5)*; *(b)* `mac.py`in **tetiklenemeyen dalı** → **B-72**; *(c)* `06` ↔ test yüklem uyuşmazlığı → **B-73**; *(d)* güç analizinin kendi yöntemi → **13**. Prompt beni **kapı raporunu koşturmaya** da çağırmadı *(98 dk)*; kapının **girdilerini** denetledim, kapının kendisini değil — bu bir **boşluk** ve §4'te yazılı. |
| **13** | ⭐ *(listede yoktu)* Güç analizinin kendisi | 🔴 **K-055 normal yaklaşım kullanıyor; küçük n'de TAM binom farklı söylüyor.** Ölçtüm *(tek yönlü, α=0,05, H0: p=0,70)*: %80 güç için gereken n — **p₁=0,40'ta 19** *(K-055: 16)*, **p₁=0,50'de 43** *(K-055: 35)*, p₁=0,30'da **12** *(9)*. **n=16'nın gerçek gücü p₁=0,40'ta 0,716** — ilan edilen 0,80'in altında. Yani K-055'in *bağlayıcı* eşiği *(n ≥ 16)* kendi ölçütüne göre **yetersiz**; n ≥ 19 olmalıydı. *(Benim örneklemim ikisini de aşıyor.)* |
| **14** | ⭐ *(listede yoktu)* *"İki sayı kaymadı ⇒ hepsi kaymadı"* çıkarımı | 🟢 **Bu vakada geçerli — ama iki sayı yüzünden değil.** Çıkarım genel olarak **geçersizdir**; burada **yapısal** olarak doğrulanabiliyor: K-050'nin eklediği `bag_gercek_per` çağrıları **hiç rastgele sayı çekmiyor** *(saf geometri + `radyo` kapalı formları)* ve K-049'un kancası kancasız kolda `ek_bayt = 0` bırakıp çerçeve boyutunu değiştirmiyor *(`test_b47_BOS_kanca_…` bunu zorluyor)*. Doğrudan ölçtüm: koşu boyunca `bag_gercek_per`i **fazladan 300 000 kez** çağırmak tam sonuç sözlüğünün blake2b'sini **değiştirmiyor** *(`bd437a331871b201` → `bd437a331871b201`)*. Yani doğru gerekçe *"iki sayı aynı çıktı"* değil, ***"eklenen yol RNG tüketmiyor"***; kayıt gerekçeyi zayıf biçimde yazmış. |

---

## 7. KAPSAM BEYANINA EKLENECEKLER — `08` madde 25…30

Dördü **modellenmiyor ve listede yok**; ikisi **var olan bir maddenin
sınırlanmamış ekseni**. Her birinin **yönü** ölçüldü.

| # | eklenecek madde | yön ve büyüklük *(ölçüldü)* |
|---|---|---|
| **25** | **Yayılma gecikmesi modellenmiyor.** Bir çerçeve `[t, t+süre]` aralığında alıcıya **anında** ulaşıyor; `Iletim.baslangic_s` gönderende ve alıcıda aynı. | 280 m'de **0,93 µs**, girişim menzilinde *(603 m)* **2,01 µs**. Karşılaştırma noktası: `cca_s = 4 µs`, `slot_s = 20 µs`. Yani ihmal edilen büyüklük, **aynı-slot çarpışmasını üreten mekanizmanın (CCA) %23–50'si** kadar. Yön: **çarpışma zamanlamasını gerçeğe göre keskinleştirir.** |
| **26** | **Kopya önbelleği sınırsız ve hiç yaşlandırılmıyor.** `mac.py:113` — `kopya_onbellegi[i]` bir `set` ve içinden hiçbir şey çıkarılmıyor. | Gerçek 802.11'de önbellek sonlu ve yaşlanır. Yön: kopya bastırma **kusursuz** → modeli gerçeğe göre **iyimser**. Ölçüldü: S2/orta/tohum 1'de **261**, S2/yoğun'da yüzlerce kopya alım bu yoldan geçiyor. |
| **27** | **Beacon yükünün bedeli, taşınan bilgi miktarından bağımsız.** Madde 24 yalnızca *"hizalama/dolgu yok"* diyor; alan adı uzunluğu ve tamsayı büyüklüğü **sınırsız**. | Ölçüldü: **124×** *(gerçek koşu)*, sentetik tavan **20 205×**. Yön: kontrol düzlemi maliyetini **sınırsız az** gösterebilir. → **B-66** |
| **28** | **Yayın çerçevesinin alıcı tarafı yalnızca `beacon_bayt` kredilendiriliyor.** Veri ve onay yollarında böyle bir asimetri yok. | Ölçüldü: 57 baytlık çerçeve → alıcıya **32 bayt**; bir koşuda **1 668 050 bayt** eksik. Yön: `alinan_bayt` gözlem alanını **az** gösterir. → **B-70** |
| **29** | **`protokol_teshis` slotu meşru arayüzden doldurulamaz.** Şema dondu ama slot yazılamıyor; `05` §D'nin dört teşhis sayacının kod karşılığı yok. | → **B-68** |
| **30** | **Kapının kapsam koruması test ADINA bakıyor, İÇERİĞİNE değil.** `zorunlu` desenleri önek eşleşmesi; aynı önekli boş bir test korumayı susturur. | Kalan net: Ç1.3'ün taban kontrolü 324 testin tamamını koşuyor, yani tek katman değil. → §6-5 |

⚠️ Ayrıca `08:194`ün *"Kalan kanal yalnızca modül global'leridir"* cümlesi
**düzeltilmeli** *(B-69)*: fabrikayı saran kapsam, sınıf özniteliği ve
fabrikanın `__dict__`i de kanaldır — üçüncüsünü deponun kendi testi
kullanıyor *(`test_b49_…`, `yazan_fabrika._kosu = k`)*.

---

## 8. 🔴 ANLAŞILMAYANLAR

Boş bırakılamaz; ve üç denetimde de bu bölümden gerçek kusur çıktı. Aşağıdaki
beşi **bulgu değil**: cevabını ölçemediğim ya da *"bilinçli tasarım mı, fark
edilmemiş mi"* ayrımını yapamadığım şeyler.

**A5 · `komsu_tablosu` sıralaması bir bilgi kanalı mı?**
`gozlem.komsular`, `dict.values()` sırasıyla — yani **ilk duyulma sırasıyla**
— geliyor. Karıştırma altında iyi bağlı komşu daha erken duyulur; ölçtüm:
hiçbir ALANI okumadan `komsular[0]`ı seçen bir kol **+0,064** seçim avantajı
alıyor *(B-65)*. **Anlayamadığım:** bu, protokolün *"meşru olarak sahip
olduğu"* bir bilgi mi *(gerçek bir telsiz de komşularını duyduğu sırayla
öğrenir)*, yoksa `05` §A4'ün kapatmak istediği kanalın sızıntısı mı?
Cevap ikisinden hangisiyse `06`nın null model tanımı ona göre yazılmalı —
**ve bugün yazılmamış.** Bu, B-65'in altında yatan asıl belirsizlik.

**A6 · `TEDAVI_ALANLARI`nda `not_` neden var?**
`kosucu.py:80-83` serbest metin alanı `not_`u **tedavi** sayıyor, yani
`kurulum_hash`ten çıkarıyor. İki kol farklı `not_` ile karşılaştırılabiliyor
*(ölçtüm: kabul ediliyor)*. Bir serbest metin alanının **tedavi** olması
mantıklı *(kurulumu değiştirmez)*, ama aynı gerekçeyle **hash'e girmesi de
zararsız** olurdu. **Anlayamadığım:** `not_` bilinçli mi listeye kondu, yoksa
`kol` ile birlikte *"etiket alanları"* diye toplandı mı? Bugün zararsız; ama
`not_` bir gün bir ablasyon bayrağının **yerine** kullanılırsa
*(«not_="null model kolu"»)* `03` B5'in *"etiketi elle taşımak"* tuzağının
tam hâli olur.

**A7 · `_bekleyeni_kostur` ↔ `_uyandir` arasında beacon önceliği**
Üçüncü denetimin §ANLAŞILMAYANLAR-4'ü *"beacon açlığa düşüyor mu"* diye
sormuş ve **ölçülmüş** *(kaçırılan oranı < %1)*. Benim anlamadığım farklı:
`yayin_gonder` MAC meşgulken beacon'ı **bekletiyor** ve bir sonraki beacon
gelirse eskisini **düşürüyor** *(`kacirilan_yayin`)*. Ama bekleyen beacon
`_bekleyeni_kostur` ile ancak **bir sonraki `_yayin_bitti` / `_onay_geldi`**
anında koşuyor — yani düğüm veri gönderirken beacon **kuyruklanmıyor**, tek
slotluk bir tampon var. **Anlayamadığım:** tek slotluk tampon bir modelleme
kararı mı, yoksa `bekleyen_yayin`in tek bir demet olmasının yan etkisi mi?
`08`de beyan yok. Yönü ölçtüm *(< %1)*, ama yoğun trafikte ve daha kısa
beacon aralığında oran nasıl davranır — bilmiyorum.

**A8 · Sonuç şemasının kendisi neden korumasız?**
`03` B5 *"şemanın kaybolması"* tuzağını sayıyor ve K-041 şemayı
*"Aile 1 başlamadan dondur"* diyor. Ama `sonuc()`un anahtar kümesini **sabit
tutan hiçbir test yok**: `test_b30_…semada_var_ve_tam` yalnızca **yedi
anahtarın varlığını** sınıyor. Yeni bir anahtar eklemek, bir anahtarı
yeniden adlandırmak ya da silmek **324 testin hiçbirini kırmaz** *(silme,
onu okuyan varsa kırar; okunmayanlar için kırmaz — §5'in U4-07'si tam bu
sınıf)*. **Anlayamadığım:** dondurma kararı **disiplinle** mi
sağlanacak *(A-4 öncesi durumu gibi)*, yoksa bir `BEKLENEN_SONUC_ANAHTARLARI`
frozenset'i mi eksik? İkincisi 10 satır; birincisi bu depoda **iki kez**
yetmedi *(K-041 ve B-30)*.

**A9 · `dogrulama/` neden kör taramanın dışında?**
`kor_mutasyon.py:56` — `HEDEF_DIZIN = KOK / "sim"`. Yani **3 664 satırlık
`dogrulama/`** — kapıyı, mutasyon paketini, ayıklamayı ve kalibrasyonu
üreten kod — kör taramaya **hiç girmiyor**; hedefli **35 mutasyonun da 35'i**
`sim/` altında *(`kosucu` · `mac` · `config` · `queues` · `radio` · `packet` ·
`rng` · `karsilastirma`)*. Üçüncü denetim sağ kalanlarının **üçte birinin** doğrulama araçlarında
olduğunu yazmıştı. **Anlayamadığım:** bu bilinçli bir kapsam kararı mı
*(«araçlar kapı değil»)*, yoksa `kor_mutasyon.py` yazılırken `sim/`
seçilmesinin fark edilmemiş sonucu mu? `08`de beyan yok. Ölçüm: bu denetimin
`dogrulama/` hedefli iki mutasyonu §5'te.

---

## 9. KOŞTURDUĞUM KOMUTLAR

Hepsi **depo kökünden** koştu. Uzun olanlar geçici dizinlerde
*(`tempfile.mkdtemp`)* çalıştı; depoda hiçbir dosya değiştirilmedi.

| # | komut / betik | ne ölçtü | süre |
|---|---|---|---|
| 1 | `python -m pytest tests -q --collect-only` | envanter: **324 test** | 0,3 sn |
| 2 | `python -c "…mutantlari_uret()…"` | kör havuz **215**, dosya dağılımı | 2 sn |
| 3 | `python -c "…len(MUTASYONLAR)…"` | hedefli mutasyon **35**, hepsi `sim/` altında | 1 sn |
| 4 | `pathlib.Path("sim/kosucu.py").read_bytes()` | 🔴 **B-58 doğrulaması**: `b'h.update(b"\x1f")'` — ayraç **gerçek** | anlık |
| 5 | Y8 sarmalayıcı betiği *(S2 ve S0, `en_kisa_yol`)* | 24 yolun tetiklenme sayısı *(§5 tablosu)*; ve `_girisim_w`in **0/246 378** dalı | 1,2 dk |
| 6 | üçüncü/dördüncü/beşinci **null model** *(S2, tohum 1–3)* | `komsular[0]` **+0,064** · `komsular[-1]` **+0,057** *(teslim 0,0000)* · `duyulan_beacon` **+0,087** | 0,6 dk |
| 7 | B-45 kapı yüklemleri × **8 tohum** *(4 kol)* | 🔴 **B-65**: T1 7/8 · T2 5/8 · T3 2/8 düştü | 13 dk *(seri)* |
| 8 | **karar başına düzgün** null × 8 tohum | sebep: **+0,00014 ± 0,00029**, 8/8 geçti | 4 dk |
| 9 | `yuk_bayt` bedel modeli + tam koşu | 🔴 **B-66**: 10 bayt bedelle **1 236 bayt**, **266** komşu kaydına ulaştı | 0,5 dk |
| 10 | `ortak_alt_kume` dördüncü eksen taraması *(8 aday)* | 🔴 **B-67**: kırpık liste · tekrarlı kimlik · NaN · negatif → **dördü de KABUL** | 2 dk |
| 11 | beacon alım kredisi izleme | 🔴 **B-70**: 57 baytlık çerçeve → **32 bayt** kredi; koşuda **1 668 050 bayt** | 0,4 dk |
| 12 | `yeni_olcut` nöbetçi taraması *(4 girdi)* | 🔴 **B-71**: eksik anahtar → çalışma noktası **0 → −10 dBm**; dizgi literali `is` **True** | anlık |
| 13 | A-4 kalan kanal denemesi | 🔴 **B-69**: **14 düğümün** özel ölçümü paylaşıldı, `test_a4_…` **geçiyor** | 0,4 dk |
| 14 | `@icerik_testi` haritası + gövde taraması | 🔴 **B-76**: `son_iletim_sonucu` **yanlış teste** iliştirilmiş | anlık |
| 15 | `# K-\d\d\d` üretici satırı taraması | 🔴 **B-74**: **55** kayıt · **18** üretici · **37** sayı taşıyıp üreticisiz | anlık |
| 16 | `SAG_KALANLAR` ↔ bugünkü 24'lük örneklem | 🔴 **B-75**: 7'nin **yalnızca 1'i** bugünkü örneklemde | 3 sn |
| 17 | üç `YOLSUZ` mutasyonu × 4 kurulum *(geçici kopya)* | ✅ **B-52 doğru**: T03 · T05 · T06 üçü de eşdeğer | 11 dk |
| 18 | bağımsız **mesafe-vektörü protokolü** *(S0/S2 × 3 tohum)* | ✅ atlama **2,33** *(S0/t1)*, **1,00** *(S2/t1)*; 🔴 kontrol payı **%15–36** *(B-77)* | 9 dk |
| 19 | `PYTHONHASHSEED=0` ve `=12345` ile tam sonuç blake2b | ✅ **Ç2.2**: `32ce1a8137ede988` = `32ce1a8137ede988` | 0,3 dk |
| 20 | `bag_gercek_per`e **300 000 ek çağrı** | ✅ RNG tüketmiyor: sonuç blake2b **birebir aynı** | 0,5 dk |
| 21 | analitik ortalama derece *(sayısal integral)* + girişim menzili | ✅ **7,44259** *(belge 7,44258)* · **603,2417** *(birebir)* | anlık |
| 22 | `scipy.stats` güç analizi *(normal + TAM binom)* | ✅ K-055'in **9 · 16 · 35 · 136**'sı birebir; 🔴 TAM binom **12 · 19 · 43 · 155** | anlık |
| 23 | markdown bağ + backtick yol taraması *(4 dizin)* | ✅ **kırık atıf yok** | anlık |
| 24 | `grep -rn "wilcoxon\|holm\|scipy" --include=*.py .` | ✅ **0 eşleşme** — istatistik katmanı gerçekten yok | anlık |
| 25 | 2000–2029 tohum taraması *(`tests/`, `dogrulama/`, `sim/`)* | ✅ **0 eşleşme**; `TOHUM_TAM = range(1, 31)` | anlık |
| 26 | 🔴 **`scratchpad/mut4.py`** — 24 mutasyon + taban, her biri **TAM 324 testlik paket**, geçici kopyalarda, 8 paralel | **taban 324 passed**; **6/24 sağ kaldı** | **58,0 dk** |
| 27 | 🔴 **`scratchpad/sagkalan4.py`** — 6 sağ kalan × **6 kurulumluk matris**, tam sonuç sözlüğü karşılaştırması | *(§5 sağ kalan tablosu)* | ~15 dk |

**Koşturmadığım:** `dogrulama/aile0_kapi_raporu.py` *(98 dk — 30 dk bütçe
sınırının üstünde ve mutasyon paketiyle çakışırdı)*, `kurulum_kalibrasyonu.py`,
`kor_mutasyon.py 24`, `mutasyon_paketi.py`. Kapının **girdilerini** ayrı
ayrı denetledim; **kapının kendisini koşturmadım** ve bu §4'te yazılıdır.

⚠️ **Bir üretici komut ilk yazımında ÇALIŞMIYORDU ve düzeltildi.** B-65 ve
B-77'nin komutları önce `multiprocessing.Pool` kullanıyordu; Windows'ta
`spawn` başlangıç yöntemi `__main__`i yeniden içe aktarmaya çalışır ve
`python - <<'PY'` ile verilen bir betikte bu **çöker**
*(`OSError: [Errno 22] Invalid argument: '<stdin>'`)* — üstelik `Pool`
işçileri **sonsuz yeniden doğar** ve makineyi doldurur *(ölçüldü: 4 MB hata
çıktısı, süreç öldürüldü)*. İkisi de **seri** hâle getirildi ve **verbatim
koşturularak** doğrulandı. Üçüncü denetimin komutlarının yeniden
üretilememesi bu raporda tekrarlanmasın diye, **§1'deki her üretici komut
olduğu gibi koşturuldu.**

---

## 🔴 SON SÖZ — dördüncü denetçiden

Üç denetim *"örüntü kapanmadı"* yazdı ve üçünde de haklıydı. Ben **daha
güçlü bir örneklemle** ölçtüm *(n = 24, güç 0,886)* ve oran **%25,0'e**
düştü. Bunun kolay okuması *"örüntü kapandı"*dır. **O okumayı
reddediyorum**, ve sebebi Y6:

> Katmanlara ayırdığımda, önceki üç denetimin fiilen örneklediği katmanda
> *(sayaç ve raporlama alanları)* oran **%45,5** ve **H0: p = 0,70
> reddedilemiyor** *(p = 0,078)*. Düşüşün büyük kısmı benim **başka bir
> yere baktığımdan** geliyor — ve baktığım yer *(mekanizmalar)* gerçekten
> sağlam: 11 mekanizma mutasyonunun **11'i de** ya yakalandı ya **gerçek
> eşdeğer** çıktı.

**Örüntü kapanmadı. Yer değiştirdi.** Simülatörün fiziği ve mekanizmaları
dört denetimden sonra sağlam duruyor. Korumasız kalan yüzey artık
**sayaçlar, raporlama alanları ve gözlem penceresidir** — yani tam olarak
**Aile 1'in sonuç şeması**. Bu denetimin beş *"tüketicisiz"* sağ kalanının
beşi de oradan çıktı, ve en ağır iki bulgusu *(B-65, B-66)* da oradan:
biri ön-kayıtlı bir kapının **ölçtüğü sayı**, diğeri bir kontrol düzlemi
bütçesinin **muhasebesi**.

⚖️ **Ve bir kez daha: iki bağımsız gözün aynı sonuca varması doğrulama
değildir.** Üçüncü denetim `b""` gördü, devralan ajan da `b""` gördü, ikisi
de yanıldı — bayt `0x1F`ti. Ben o satırı `read_bytes()` ile okudum ve
**çürütmenin haklı olduğunu** doğruladım. Ama aynı hataya kendim de düştüm:
**U4-17'nin davranışı değiştireceğini varsaydım, ölçtüm, değiştirmiyordu**
*(§5)*. Bu raporda bir tane geri alınmış iddia var ve **yazılıdır**.

**Jürinin bulacağı ama benim bulamadığım şeyler için** §4 *(kapı raporunu
koşturmadım — 98 dk)* ve §8 *(beş anlaşılmayan)* okunmalıdır. Özellikle
§8-A5: seçim avantajı ölçütünün altında yatan *"komşu tablosunun sırası bir
bilgi kanalı mı"* sorusunun cevabı **hâlâ yazılı değil**, ve B-65 tam
oradan doğdu.

---

🔒 **Bu denetim sırasında depodaki hiçbir dosya değiştirilmemiştir.**
Yazılan tek dosya `aile0_audit.md`dir — bu bölüm eklendi; **mevcut üç
denetim raporuna dokunulmadı**, baştaki durum bloğuna yalnızca dördüncü
satır ve dördüncü özet eklendi. Bütün mutasyonlar ve deneme betikleri
`…\AppData\Local\Temp\…\scratchpad\` altındaki **geçici kopyalarda**
*(`tempfile.mkdtemp`)* çalıştırıldı; hiçbiri depo ağacına yazmadı.
**Hiçbir git komutu çalıştırılmamıştır — `status` dâhil.**
**2000–2029 tohum aralığı hiçbir amaçla koşulmamıştır** *(ayrıca ölçüldü:
`tests/`, `dogrulama/` ve `sim/` altında o aralığa hiç atıf yok;
`TOHUM_TAM = range(1, 31)`)*. Koştuğum tohumlar: **1–8** *(ayarlama
kümesinden)*.

⚠️ **Tam şeffaflık.** Depo ağacında bu denetimden sonra değişmiş üç şey
var: **biri bilerek yazdığım rapor**, ikisi içe aktarma/pytest yan
etkisi. Hiçbiri kaynak, belge ya da test dosyası **değildir**:

| ne | ne zaman | sebebi |
|---|---|---|
| `aile0_audit.md` | **03:07** | 🔴 **benim yazdığım tek dosya** |
| `.pytest_cache/v/cache/nodeids` · `stepwise` | 22:42 | envanter için koştuğum `pytest tests -q --collect-only` *(`-p no:cacheprovider` vermemiştim)*. `lastfailed` **21 Ağustos 10:29'dan** kalma ve **dokunulmadı** — yani hiçbir başarısızlık kaydedilmedi |
| `tests/__pycache__/test_gozlem.cpython-311.pyc` | 23:29 | B-76 için `importlib` ile `test_gozlem.py` içe aktarıldı — bayt kodu önbelleği |

🔴 **BENİM OLMAYAN değişiklikler — ölçüldü ve ayırt edildi.** `find -newermt`
ile taradım: `README.md` · `denetim/AILE0-DENETIM-4-PROMPTU.md` ·
`v2/00` · `01` · `04` · `06` · `07` · `08` · `09` · `v2/README.md` ·
`v2/kaynak_doğrulama.txt` **22:20–22:43** arasında değişti. Bunlar
**denetim başlamadan önceki ve denetim promptunu yazan oturumun** son
yazımlarıdır *(K-055 + prompt)*; ben hiçbirine yazmadım. Üçüncü denetim de
aynı durumu yaşamış ve aynı şekilde kaydetmişti — **bu, denetçinin kendi
ayak izini ölçmesinin neden gerektiğinin örneğidir.** İçerikleri, oturum
boyunca okuduğum hâlleriyle aynıdır.

⚠️ Ayrıca bir kez **makineyi doldurdum ve düzelttim**: B-65'in üretici
komutunu `multiprocessing` ile koşturmaya çalıştım, Windows'ta `spawn`
işçileri sonsuz yeniden doğdu *(4 MB hata çıktısı)*; süreç ağacı
öldürüldü ve komut **seri** hâle getirildi. Bu, mutasyon paketinin
süresini de uzattı *(tahmin 40–50 dk, ölçülen 58,0 dk)* ve **kayda
geçiyor** — çünkü `03` kural 7'nin işlemci bütçesi kuralının ihlaline en
yakın olduğum an buydu.
---

# BEŞİNCİ DENETİM — 25 Ağustos 2026

> **Denetlenen:** K-059'daki **beşinci kapanış** *(kapı 13/13, 150,2 dk,
> 25 Ağustos)* ve dördüncü denetimin **13 bulgusunun kapatıldığı iddiası**
> *(K-056)*, artı kapının kendi düşüşünden çıkan **B-78 · B-79**'un
> kapatıldığı iddiası *(K-058)*.
>
> **Bağlayıcı şartlar** *(K-057'nin katmanlı güç analizi)*: **sayaç/raporlama
> katmanında ≥ 19 mutasyon** *(güç 0,814)* · **mekanizma katmanında ≥ 8** ·
> **`sim/kosucu.py`ye ≥ 5**. Koşulan: **35 mutasyon** — **26 sayaç · 9
> mekanizma · 27'si `sim/kosucu.py`de** — her biri **TAM 367 testlik
> paketle**, geçici kopyalarda, taban kontrolüyle birlikte *(**72,7 dk**)*.
>
> 🔴 **Bu rapor, önceki DÖRT denetim raporuna DOKUNMADAN eklenmiştir.**
> Baştaki durum bloğuna yalnızca beşinci satır ve beşinci özet eklendi.

**Bu denetimin çalışma ilkesi — dört öncekinden devralınan dört kural:**

| kural | bu raporda nasıl uygulandı |
|---|---|
| **Y8** *(bozduğun yolun tetiklendiğini ÖNCE göster)* | 35 mutasyonun **35'inin** bozduğu yol, mutasyon yazılmadan **önce**, dört sabit yapılandırmada ölçüldü. **Üçü tetiklenmedi** *(C15 · C18 · C20)*; üçü de 18 ek yapılandırmada sınandı ve **EŞDEĞER** ilan edildi *(§5)*. Bu, deponun *"mutasyon hatalı çıktı"* sınıfının **beşinci–yedinci** örneği ve ilk kez **rapordan önce** yakalandı |
| **Y10 / Y11** *(iddia kırılabilir olmalı; koruma kapsamı DIŞINDA sınanmalı)* | Dördüncü denetimin 13 bulgusunun **her biri** için kapsamı dışında bir vaka üretildi; **9'unda** kabul ettirildi. Önerdiğim her değişmez **önce koşturuldu** |
| **Y6** *(beklenenden iyi sonuç, kötü sonuç kadar şüphelidir)* | Sayaç oranım dördüncü denetiminkinden **iyi** çıktı; **kendi örneklemimde üç yanlılık** aradım ve buldum — biri kendi iddiamı **geri aldırdı** *(B-96)* |
| 🔴 **Yayımladığın her üretici komutu, yayımlamadan önce OLDUĞU GİBİ koştur** | 22 komut grubunun tamamı verbatim koşturuldu. **Biri ilk yazımında çalışmadı** *(B-89 — `inspect.getsource` stdin'den okuyamıyor)*; düzeltildi, yeniden koşuldu ve **düzeltilmiş hâli** yayımlandı |

⚠️ **Ve bir beşinci kural, bu denetimin kendisinden çıktı:** *"Bir SAYININ
üretici satırı olması, o sayının yeniden üretilebildiğini göstermez."*
`08` madde 25 üretici komut **taşıyor** ve yine de üretilemedi — çünkü onu
üreten kod **aynı oturumda** değişti *(**B-80**)*.

---

## 0. YÖNETİCİ ÖZETİ

🔴 **KATMAN BAZINDA SAĞ KALAN ORANI VE ULAŞILAN GÜÇ** *(tek örneklem binom ·
tek yönlü · α = 0,05 · **TAM binom** · H0: p = 0,70 · GA: Clopper–Pearson)*:

| katman | sağ kalan | oran | %95 GA | **ULAŞILAN GÜÇ** *(p₁=0,40)* | H0: p = 0,70 | n ≥ 19? |
|---|---|---|---|---|---|---|
| 🔴 **sayaç / raporlama** | **10/26** | **%38,5** | [0,202 · 0,594] | **0,892** | **REDDEDİLDİ** *(p = 8,5×10⁻⁴)* | **EVET** |
| **mekanizma** | 1/9 | %11,1 | [0,003 · 0,482] | 0,483 | reddedildi *(p = 4,3×10⁻⁴)* | 🔴 **HAYIR** |
| 🔴 **`sim/kosucu.py`** *(4. denetimin kör noktası)* | **10/27** | **%37,0** | [0,194 · 0,576] | **0,926** | reddedildi *(p = 4,0×10⁻⁴)* | **EVET** |
| **GENEL** | **11/35** | **%31,4** | [0,169 · 0,493] | **0,970** | reddedildi *(p = 2,9×10⁻⁶)* | **EVET** |

**Seri: %80,0 → %70,0 → %66,7 → %25,0 → %31,4.**
**Sayaç katmanı serisi: — → — → — → %45,5 → %38,5.**

🔴 **SAYAÇ KATMANI İÇİN İLK KEZ YETERLİ GÜÇLE ÖLÇÜLDÜ** *(n = 26 ≥ 19, güç
0,892)* ve H0 = 0,70 **bu kez reddedildi** *(dördüncüde reddedilemiyordu,
n = 11'de güç yalnızca 0,533'tü)*. **Ama %95 GA hâlâ [0,202 · 0,594]** —
gerçek oran %20 ile %59 arasında. **Bu katmanda da örüntü KAPANMADI,
DARALDI.** 🔴 **Mekanizma katmanı için "kapandı" YAZILAMAZ:** n = 9 < 19,
ulaşılan güç **0,483**.

🔴 **Dördüncü denetimin beyan ettiği kör nokta ölçüldü ve haklı çıktı:**
`sim/kosucu.py`ye 27 mutasyon kondu ve oran **%37,0** — örneklemin **en
kötü katmanı**. Üçüncü denetimde orada oran %57 *(4/7)*, dördüncüde
**hiç ölçülmemişti**.

**Kapanış geçerli mi: KOŞULLU — üç cümlede.** *(1)* Simülatörün **fiziği ve
mekanizmaları** beşinci kez de sağlam çıktı: 9 mekanizma mutasyonunun 8'i
yakalandı, ikisi doğrudan analitik değişmezlerle *(`test_ber_kapali_form` ·
`test_cw_ikili_ustel_buyuyor`)*, ve ön-kayıtlı H1.1 kapısı — iki kez yanlış
şey ölçtükten sonra — **üçüncü hâlinde doğru şeyi ölçüyor**: yazdığım üç
sıfır-bilgi kolunun **üçünü de reddetti**, `PYTHONHASHSEED`ten bağımsız,
ve kendi sayıları *(+0,0283 · +0,0599 · +0,0876)* **birebir** yeniden
üretildi. *(2)* **Ama `08` — B-57 kapanınca MÜHÜRLENECEK belge — bugün iki
yanlış madde taşıyor**, ve ikisini de **aynı oturumun kendi düzeltmesi**
bayatlattı: madde 25'in kontrol payı sayıları B-66 ÖNCESİ maliyet
modelinden *(eski modelle **birebir** yeniden ürettim: %26,04/%35,63/%14,88/
%25,41)*, madde 24 ise hâlâ *"alan kimliği 1 B · int/float 4 B"* diyor
oysa kodun kendisi *"bu `08`de beyan edilir"* diye **istediği** beyanı
almamış. *(3)* Ve **sonuç şeması** hâlâ Aile 1'in okuyacağı **korumasız
yüzeydir**: `pencerede_teslim` **802 → 2 698** yapılabiliyor,
`ortanca_gecikme_s` **ortalamaya** çevrilebiliyor *(S0'da 0,109 s →
2,450 s, 22×)*, `islenen_olay` · `mac_kayip_onay` · `mac_basarisiz_alim`
sıfırlanabiliyor — **367 test hiçbirini görmüyor.**

**20 yeni bulgu: B-80 … B-99.** Üçü yüksek-kritik sınırında *(B-80 · B-84 ·
B-88)*, altısı yüksek *(B-81 · B-82 · B-85 · B-86 · B-87 · B-95)*. 🔴 **13
kapanışın 8'i bir sonraki bulguyu doğurdu** — örüntü dördüncü kez
tekrarlandı. `08`e **bir düzeltme + beş madde** öneriliyor *(26…30)*; biri
dördüncü denetimin **kendi önerdiği** ve `08`e **hiç girmemiş** olan
madde *(yayılma gecikmesi)*.

**Dördüncü denetimin 13 bulgusunun 13'ünü de denetledim:** **4'ü tam
kapalı** *(B-70 · B-71 · B-72 · B-75)*, **9'u kısmen** — hepsinde düzeltme
**kodda** *(Y13 temiz: K-044/B-41'in *"ilan edildi, koda girmedi"* sınıfı
bu oturumda **tekrarlanmadı**)*, ama dokuzunun her birinde **korumanın
kapsamı dışında** bir vaka üretilip kabul ettirildi *(Y11)*.

**Yeniden ürettiğim 20 iddiadan 17'si tuttu**, üçü tutmadı — ve tutmayan
üçü de **aynı kökten** *(B-66'nın kendi düzeltmesi)*. İki iddia daha
**sınanamadı** *(§4)*.

⚖️ **Y6 — kendi lehime çıkan sonuca kendi ölçütümü uyguladım.** Sayaç
oranım dördüncü denetiminkinden daha iyi çıktı *(%45,5 → %38,5)*. Üç
yanlılık buldum, üçü de kendi örneklemimde: **(a)** 26 sayaç mutasyonunun
22'si tek bir fonksiyonda, ve şemanın **en korunan** alanlarına
*(parmak izleri)* hiç dokunmadım — oran muhtemelen **üst tahmin**;
**(b)** üç sağ kalanım **gerçekten eşdeğer** ve bunu **Y8'i mutasyondan
önce koşturarak ben yakaladım** *(eşdeğersiz oran: sayaç **%30,4**, genel
**%25,0**)*; **(c)** iki mekanizma mutasyonumun *"yanlış sebeple
yakalandığı"* iddiamı ölçtüm ve **geri aldım** — ikisi de doğrudan
değişmezlerle gerçekten korunuyor *(B-96)*.

**Ve bulamadıklarımı da yazıyorum** *(§6-11)*: gözlemden simülatöre geri
referans **yok**; `teshis` bir geri kanal **değil**; `yeni_olcut`un
dördüncü bir atlama yolu **yok**; ve kapıyı yanlışlıkla geçen bir
sıfır-bilgi kolu **bulamadım**.

---

## 1. YENİ BULGULAR — B-80'den

Her bulgunun **üretici komutu depo kökünden koşar**, kendi kendine yeterlidir
ve **yayımlanmadan önce olduğu gibi koşturulmuştur**. Hiçbiri `scratchpad/`
yoluna atıf yapmaz.

---

### 🔴 B-80 · YÜKSEK — `08` madde 25'in sayıları B-66 ÖNCESİ maliyet modelinden; aynı oturumun kendi düzeltmesi onları bayatlattı

| | |
|---|---|
| **Nerede** | `v2/08-AILE0-KAPSAM.md:289` *(madde 25)* · `README.md` *(Aile 1 uyarı 2)* · `aile0_audit.md` §B-77 |
| **İDDİA** | *"Ölçüldü (3 tohum, kâhinsiz mesafe-vektörü kolu vs `gurultuden_kacan`): kontrol payı **%14,9–35,6** vs **%1,65–1,87** — **14–20 kat**."* |
| **ÖLÇTÜĞÜM** | Kaydın **kendi üretici komutunu** olduğu gibi koşturdum. Teslim oranı ve atlama sayısı **birebir** çıktı *(DV S0 ort. 0,2996 · atlama 1,67)* — yani aynı koşu. Ama kontrol payı **tutmadı**. |

**Üretici komut** *(depo kökünden; seri koşar, **koşturuldu: 2,1 dk**, 12 tam koşu)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import sys; sys.path.insert(0, ".")
from sim.config import Konfig
from sim.kosucu import Kosu
from dogrulama.aktaricilar import AKTARICILAR
def dv(kon):                       # KAHIN YOK: yalnizca Gozlem + beacon_yuku
    d = {"t": {}}
    def ogren(g):
        yeni = {g.dugum: (0, g.dugum)}
        for k in g.komsular:
            yeni.setdefault(k.dugum, (1, k.dugum))
            for ad, v in k.bildirdigi_yuk:
                if not ad.startswith("d"): continue
                try: h = int(ad[1:])
                except ValueError: continue
                if h == g.dugum: continue
                if h not in yeni or v + 1 < yeni[h][0]: yeni[h] = (v + 1, k.dugum)
        d["t"] = yeni; return yeni
    def s(g):
        t = ogren(g)
        if g.paket is None or not g.komsular: return None
        r = t.get(g.paket.hedef)
        if r is None or r[1] == g.dugum: return None
        return r[1] if any(k.dugum == r[1] for k in g.komsular) else None
    s.beacon_yuku = lambda dug: {("d%d" % h): m for h, (m, _) in
                                 (d["t"] or {dug: (0, dug)}).items() if m <= 8}
    return s
for ad, fab in (("DV", dv), ("gurultuden_kacan", AKTARICILAR["gurultuden_kacan"])):
    for sen in ("S0", "S2"):
        for t in (1, 2, 3):
            s = Kosu(Konfig(kol="t", senaryo=sen, trafik="orta", tohum=t), fab).kostur()
            print("%-18s %s t%d teslim=%.4f atlama=%s kontrol=%.2f%%"
                  % (ad, sen, t, s["teslim_orani"], s["ortalama_atlama"],
                     100.0*s["kontrol_bayt"]/(s["kontrol_bayt"]+s["veri_bayt"])))
PY
```

**Beklenen / görülen:**

| büyüklük | `08` madde 25 | bugün ölçülen | tutuyor mu |
|---|---|---|---|
| DV teslim, S0 *(3 tohum ort.)* | 0,2996 | **0,2996** | ✅ birebir |
| DV atlama, S0 | 1,67 | **1,67** | ✅ birebir |
| **DV kontrol payı, S0** | **%26,0 – %35,6** | **%23,91 – %33,25** | 🔴 **HAYIR** |
| **DV kontrol payı, S2** | **%14,9 – %25,4** | **%13,71 – %23,50** | 🔴 **HAYIR** |
| gözlem kolu payı | %1,65 – %1,87 | **%1,65 – %1,87** | ✅ birebir |
| **oran** | **14 – 20 kat** | **8,3 – 17,8 kat** | 🔴 **HAYIR** |

🔴 **SEBEP ÖLÇÜLDÜ — tahmin değil.** Aynı koşuyu `yuk_bayt`ın **B-66 ÖNCESİ**
biçimiyle *(alan adı sabit 1 bayt, `int` sabit 4 bayt — dördüncü denetimin
kendi tarifi)* tekrarladım.

**İkinci üretici komut** *(geçici kopyaya yama uygular; **koşturuldu: 9,7 sn**)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import pathlib, shutil, subprocess, sys, tempfile
KOK = pathlib.Path(".").resolve()
d = pathlib.Path(tempfile.mkdtemp()) / "depo"
shutil.copytree(KOK, d, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.pyc"))
g = d / "sim" / "gozlem.py"
t = g.read_text(encoding="utf-8")
A = """        # 🔴 B-66: alan adı UZUNLUĞUYLA faturalanır, sabit 1 baytla değil.
        toplam += len(ad.encode("utf-8"))
        if isinstance(deger, bool):
            toplam += YUK_BOOL_BAYT
        elif isinstance(deger, int):
            toplam += _int_bayt(deger)          # 🔴 B-66: BÜYÜKLÜĞÜYLE"""
B = """        toplam += 1
        if isinstance(deger, bool):
            toplam += YUK_BOOL_BAYT
        elif isinstance(deger, int):
            toplam += 4"""
C = "    tasinan = _tasinan_bilgi_bayt(yuk)\n    if toplam < tasinan:"
D = "    tasinan = _tasinan_bilgi_bayt(yuk)\n    if False:"
assert t.count(A) == 1 and t.count(C) == 1
g.write_text(t.replace(A, B, 1).replace(C, D, 1), encoding="utf-8")
BETIK = r"""
import sys; sys.path.insert(0, ".")
from sim.config import Konfig
from sim.kosucu import Kosu
def dv(kon):
    d = {"t": {}}
    def ogren(g):
        yeni = {g.dugum: (0, g.dugum)}
        for k in g.komsular:
            yeni.setdefault(k.dugum, (1, k.dugum))
            for ad, v in k.bildirdigi_yuk:
                if not ad.startswith("d"): continue
                try: h = int(ad[1:])
                except ValueError: continue
                if h == g.dugum: continue
                if h not in yeni or v + 1 < yeni[h][0]: yeni[h] = (v + 1, k.dugum)
        d["t"] = yeni; return yeni
    def s(g):
        t = ogren(g)
        if g.paket is None or not g.komsular: return None
        r = t.get(g.paket.hedef)
        if r is None or r[1] == g.dugum: return None
        return r[1] if any(k.dugum == r[1] for k in g.komsular) else None
    s.beacon_yuku = lambda dug: {("d%d" % h): m for h, (m, _) in
                                 (d["t"] or {dug: (0, dug)}).items() if m <= 8}
    return s
for sen in ("S0", "S2"):
    satir = []
    for t in (1, 2, 3):
        s = Kosu(Konfig(kol="t", senaryo=sen, trafik="orta", tohum=t), dv).kostur()
        satir.append("t%d %.2f%%" % (t, 100.0*s["kontrol_bayt"]/(s["kontrol_bayt"]+s["veri_bayt"])))
    print("DV %s (B-66 ONCESI maliyet modeli): %s" % (sen, "   ".join(satir)))
"""
p = subprocess.run([sys.executable, "-c", BETIK], cwd=d, capture_output=True,
                   text=True, encoding="utf-8", errors="replace")
print(p.stdout.rstrip() or p.stderr[-600:])
shutil.rmtree(d.parent, ignore_errors=True)
PY
```

**Beklenen / görülen:**

```
DV S0 (B-66 ONCESI maliyet modeli): t1 26.04%   t2 34.77%   t3 35.63%
DV S2 (B-66 ONCESI maliyet modeli): t1 14.88%   t2 24.30%   t3 25.41%
```

Yazılan sayılar: **%26,0 – %35,6** *(S0)* ve **%14,9 – %25,4** *(S2)*.

**Dördü de yazılan sayının kendisi.** Yani madde 25, B-66'nın **düzelttiği**
maliyet modeliyle ölçülmüş ve **aynı oturumda** düzeltme yapıldıktan sonra
yeniden ölçülmemiş.

**Neden önemli:** `08` madde 25 bir **beyan değil, bağlayıcı bir kısıttır** —
*"🔒 Aile 1'in ilk karşılaştırmasından önce ya bir tavan konur ya da her
karşılaştırma kontrol payıyla birlikte raporlanır."* Tavanın kalibre
edileceği sayı bu. `08` **B-57 kapanınca mühürlenecek**; bu sayı mühürlenirse
yanlış mühürlenir. `03` kural 1'in tam tanımı: *"Bir sayı bir kez
yayımlandıktan sonra, onu üreten kod değişince sessizce bayatlar."*

⚖️ **Ve bu, B-57'nin ilacının yetmediğini gösteriyor:** madde 25'in sayısı
**üretici komut TAŞIYOR** — ve yine yeniden üretilemiyor. Eksik olan satır
değil, **yeniden koşudur**.

---

### 🔴 B-81 · YÜKSEK — `08` madde 24 hâlâ B-66 ÖNCESİ tel biçimini beyan ediyor; dört hükmünün üçü yanlış, yön iddiası ters

| | |
|---|---|
| **Nerede** | `v2/08-AILE0-KAPSAM.md:287` *(madde 24)* · `sim/gozlem.py:205-219, 222-304` |
| **İDDİA** | madde 24: *"Yük tel biçiminde hizalama/dolgu yok — **alan kimliği 1 B** · bool 1 B · **int/float 4 B** · **sayı demeti 4 B × eleman**"* · yön: *"maliyeti gerçeğe göre **AZ** gösterir"* |
| **ÖLÇTÜĞÜM** | `read_bytes()` ile okundu. Kodun bugünkü biçimi bunun **üçte üçünde** farklı. |

**Üretici komut:**

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import pathlib, sys; sys.path.insert(0, ".")
from sim.gozlem import yuk_bayt
b = pathlib.Path("v2/08-AILE0-KAPSAM.md").read_bytes().decode("utf-8")
print([s for s in b.splitlines() if s.startswith("| **24**")][0][:200])
print()
print("alan adi 1 B mi   :", yuk_bayt({"a"*10: 1}) - yuk_bayt({"a": 1}), "B fark (10 karakter icin)")
print("int 4 B mi        :", yuk_bayt({"x": 2**8192}) - 1, "B (2**8192 icin)")
print("demet 4 B/eleman  :", yuk_bayt({"t": (1, 2, 3)}) - 1, "B (uc kucuk int)")
print("float 4 B mi      :", yuk_bayt({"f": 1.5}) - 1, "B")
PY
```

**Beklenen / görülen:**

| madde 24'ün hükmü | bugünkü kod | tutuyor mu |
|---|---|---|
| alan kimliği **1 B** | **UTF-8 bayt uzunluğu** *(10 karakter → +9 B)* | 🔴 **HAYIR** |
| `int` **4 B** | `max(1, ⌈bit_length/8⌉)` *(2⁸¹⁹² → **1025 B**)* | 🔴 **HAYIR** |
| sayı demeti **4 B × eleman** | eleman başına `int` ise büyüklüğüyle *(3 küçük int → 3 B)* | 🔴 **HAYIR** |
| bool 1 B · float 4 B | 1 B · 4 B | ✅ |

🔴 **Yön iddiası da ters döndü.** Madde 24 *"maliyeti gerçeğe göre AZ
gösterir"* diyor. `sim/gozlem.py:215-219` bugün **tam tersini** yazıyor:
*"gerçek bir uygulama alan adları için 1 baytlık bir KİMLİK TABLOSU
kullanırdı; burada … adın kendisi faturalanır. Yön: dürüst bir protokolü
gerçeğe göre biraz **FAZLA** ücretlendirir."*

🔴 **Ve düzeltme kodun kendisi tarafından istenmişti:** `sim/gozlem.py:215`
aynen şöyle diyor: *"⚠️ MODELLEME KARARI, `08`de beyan edilir."* **O beyan
yapılmadı.** `03` B5: *"Yorumun kodla çelişmesi — ikisinden de kötüdür.
Belge, kodun kanıtı değildir; kod, belgenin kanıtıdır."*

---

### 🔴 B-82 · YÜKSEK — `yuk_bayt`ın Y7 öz-denetimi YAPISAL OLARAK ÖLÜ: 105 943 kabul edilen girdide 0 kez ateşlenebiliyor

| | |
|---|---|
| **Nerede** | `sim/gozlem.py:295-304` *(`if toplam < tasinan`)* · `sim/gozlem.py:232-251` *(`_tasinan_bilgi_bayt`)* · `tests/test_gozlem.py:951-957` |
| **İDDİA** | `sim/gozlem.py:235-237`: *"🔴 Y7: `yuk_bayt` kendi çıktısını buna karşı doğrular. **İki hesap ayrı hesaplanır ki, biri bozulduğunda diğeri konuşsun.**"* · K-056: *"`yuk_bayt` kendi çıktısını **ayrı yazılmış** bir taşınan bilgi hesabına karşı doğruluyor *(Y7)*"* |
| **ÖLÇTÜĞÜM** | İki hesap **ayrı değil**: `yuk_bayt`ın kabul ettiği HER girdi için ikisi **birebir aynı sayıyı** veriyor. Koruma dalı hiçbir girdide ateşlenemiyor. |

**Üretici komut** *(fuzz, **koşturuldu: 2,0 sn**)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import random, math, sys; sys.path.insert(0, ".")
from sim.gozlem import yuk_bayt, _tasinan_bilgi_bayt, YukHatasi
rnd = random.Random(7)
ALFABE = "abcXYZ0_çĞşİé中\U0001F600"
def deger():
    t = rnd.randrange(6)
    if t == 0: return rnd.choice([True, False])
    if t == 1: return rnd.randrange(-2**rnd.randrange(1,200), 2**rnd.randrange(1,200))
    if t == 2: return rnd.uniform(-1e30, 1e30)
    if t == 3: return rnd.choice([0.0, -0.0, math.inf, -math.inf, math.nan, 1e-320])
    if t == 4: return tuple(deger() for _ in range(rnd.randrange(0, 5)))
    return rnd.choice(["dizgi", b"bayt", None, [1,2], {"a":1}])
def ad(): return "".join(rnd.choice(ALFABE) for _ in range(rnd.randrange(0,6)))
kabul = red = farkli = ates = 0
for _ in range(200_000):
    y = {ad(): deger() for _ in range(rnd.randrange(0, 4))}
    try: a = yuk_bayt(y)
    except YukHatasi: red += 1; continue
    kabul += 1; b = _tasinan_bilgi_bayt(y)
    if a != b: farkli += 1
    if a < b: ates += 1
print("kabul edilen           :", kabul)
print("reddedilen             :", red)
print("iki hesap FARKLI olan  :", farkli)
print("'toplam < tasinan' ATES:", ates)
PY
```

**Beklenen / görülen:**

```
kabul edilen           : 105943
reddedilen             : 94057
iki hesap FARKLI olan  : 0
'toplam < tasinan' ATES: 0
```

**Neden yapısal:** iki fonksiyon aynı formülleri, aynı `_int_bayt()`
yardımcısını ve aynı `YUK_FLOAT_BAYT` sabitini kullanıyor. `yuk_bayt`ın
`raise` etmediği her dalda ikisi **tanım gereği** eşit. Bir *"kaçak"*
üretilemiyor.

🔴 **Sonuç iki katlı:**

1. `tests/test_gozlem.py:955`'in sekiz parametreli değişmezi
   `assert odenen >= tasinan` — ölçülen 8/8 vakada `odenen == tasinan`.
   Bu **`x >= x`**'tir; **Y10'un tam tanımı** *("bir yaklaşık-eşitlik iddiası,
   KIRILABİLİR olduğu gösterilmeden yazılmaz")*.
2. *"Biri bozulursa diğeri konuşur"* iddiası **paylaşılan** parçalar için
   yanlış: `_int_bayt` ya da `YUK_FLOAT_BAYT` bozulursa **ikisi birlikte**
   bozulur ve koruma susar. Bunu ayrıca mutasyonla ölçtüm — **§5, C22.**

⚖️ Depo bu hata sınıfını **kendisi adlandırmış** ve üç kez `assert`e
çevirmiş *(`mac.py:546`, `mac.py:666`, `kosucu.py:296` — hepsinin yanında
*"ölçüldü: N çağrının 0'ında tetiklendi"* notu var)*. Bu dördüncüsü, o
işlemden geçmemiş — üstelik **kaçağı bulan düzeltmenin kendi içinde.**

---

### 🟠 B-83 · ORTA-YÜKSEK — B-66'nın ÜÇÜNCÜ kaçak ekseni: `float` 4 bayta faturalanıyor, tele 8 bayt (64 bit) çıkıyor

| | |
|---|---|
| **Nerede** | `sim/gozlem.py:223` *(`YUK_FLOAT_BAYT = 4`)* · `sim/gozlem.py:307-309` *(`yuku_dondur` — kırpma YOK)* |
| **İDDİA** | K-056 / B-66: kaçak kapatıldı, *"tam koşu 124× → **1,00×**"* · `sim/gozlem.py:212`: *"🔒 DEĞİŞMEZ: **ödenen bayt ≥ taşınan bilgi**"* |
| **ÖLÇTÜĞÜM** | Ad ve `int` eksenlerinde kaçak gerçekten **1,00×**. Ama `float` ekseni açık: bir `float` **4 bayta** faturalanıyor ve gözlem penceresine **çift duyarlıklı (64 bit) hâliyle, kırpılmadan** giriyor. Kaçak **2,00×**, ve `int` ile `float` **aynı 8 baytlık bilgi için farklı fiyatlanıyor**. |

**Üretici komut** *(anlık)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import struct, sys; sys.path.insert(0, ".")
from sim.gozlem import yuk_bayt, yuku_dondur
ham = b"\xde\xad\xbe\xef\x01\x02\x03\x41"          # 8 KEYFI bayt
v = struct.unpack("<d", ham)[0]
print("odenen (float)      :", yuk_bayt({"a": v}), "bayt")
print("gozlem penceresine  :", yuku_dondur({"a": v}))
print("geri cozulen        :", struct.pack("<d", yuku_dondur({"a": v})[0][1]).hex())
print("giren               :", ham.hex())
print("BIREBIR AYNI MI     :", struct.pack("<d", yuku_dondur({"a": v})[0][1]) == ham)
i = int.from_bytes(ham, "little")
print()
print("AYNI 8 BAYT int olarak:", yuk_bayt({"a": i}), "bayt")
print("AYNI 8 BAYT float olarak:", yuk_bayt({"a": v}), "bayt")
print("ORAN:", (yuk_bayt({"a": i})-1)/(yuk_bayt({"a": v})-1), "x")
PY
```

**Beklenen / görülen:**

```
odenen (float)      : 5 bayt
gozlem penceresine  : (('a', 155712.2420629104),)
geri cozulen        : deadbeef01020341
giren               : deadbeef01020341
BIREBIR AYNI MI     : True

AYNI 8 BAYT int olarak: 9 bayt
AYNI 8 BAYT float olarak: 5 bayt
ORAN: 2.0 x
```

**Sınırı da ölçtüm:** kaçak **2,00× ile sınırlı** *(bir `float` en fazla 64
bit taşır)*; B-66'nın kapattığı eksenler **sınırsızdı** *(20 205×)*. Bu
yüzden **KRİTİK değil.** Ama iki şey söylüyor:

1. `05` §A2 kural 1 *("her alan BAYT OLARAK SAYILIR")* float ekseninde
   **hâlâ zorlanmıyor**; K-009'un eşit bütçe şartı **kodlamaya bağlı** —
   aynı bilgiyi `float` olarak taşıyan kol, `int` olarak taşıyandan
   **yarı fiyatına** ödüyor.
2. Bu ekseni B-82'deki öz-denetim **yapısal olarak göremez**: iki hesap da
   `YUK_FLOAT_BAYT = 4` kullanıyor.

⚠️ **Yön:** güvenli tarafa **değil**, kaçağa doğru — madde 24'ün *"maliyeti
AZ gösterir"* yönü float için doğru, ad için ters *(B-81)*.

---

### 🔴 B-84 · YÜKSEK — Ön-kayıtlı H1.1 kapısının ablasyonu İKİ ekseni birden değiştiriyor: bilgiyi yok ediyor **ve komşu demetini yeniden sıralıyor**

| | |
|---|---|
| **Nerede** | `dogrulama/aktaricilar.py:88, 96-98` *(`sorted(...)` → `zip(ks, degerler)`)* · `v2/06-ON-KAYIT.md:404-406` *(ön-kayıt metni)* |
| **İDDİA** | `06`: *"Kol, kendi ablasyonuna karşı okunur: aynı protokol, aynı kalıcılık, aynı topoloji … **Tek fark BİLGİ.**"* · `aktaricilar.py:67-69`: *"Dağılım, yapı ve kalıcılık korunur — **yok edilen tek şey** 'hangi değer hangi komşuya ait' bilgisidir."* |
| **ÖLÇTÜĞÜM** | Sarmalayıcı `komsular` demetini `sorted(..., key=dugum)` ile **yeniden sıralıyor**. Sağlam koşuda demet **%92,8 oranında sırasız** geliyor. Yani ablasyon kolu ile asıl kol arasında **ikinci bir fark** var ve o fark bilgi değil. |

**Üretici komut** *(seri koşar, 34 tam koşu; **koşturuldu: 10,0 dk** — 6 yollu mutasyon kampanyası eşzamanlı koşarken; boş makinede ~4 dk)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import dataclasses, statistics, sys; sys.path.insert(0, ".")
from sim.config import Konfig
from sim.kosucu import Kosu
from dogrulama.aktaricilar import AKTARICILAR, kalite_ablasyonu
sayac = {"cok": 0, "sirasiz": 0}
def olcen(kon):
    ic = AKTARICILAR["gurultuden_kacan"](kon)
    def s(g):
        d = [k.dugum for k in g.komsular]
        if len(d) > 1:
            sayac["cok"] += 1
            if d != sorted(d): sayac["sirasiz"] += 1
        return ic(g)
    return s
Kosu(Konfig(kol="t", senaryo="S2", tohum=1), olcen).kostur()
print("1) >1 komsulu karar : %d" % sayac["cok"])
print("   SIRASIZ gelen    : %d  (%%%.1f)" % (sayac["sirasiz"],
      100.0*sayac["sirasiz"]/sayac["cok"]))
def yalniz_sirala(fab):                 # ablasyonun IKINCI ekseni, TEK BASINA
    def sarma(kon):
        ic = fab(kon)
        def s(g):
            if not g.komsular: return ic(g)
            return ic(dataclasses.replace(
                g, komsular=tuple(sorted(g.komsular, key=lambda k: k.dugum))))
        return s
    return sarma
def sira_kolu(kon):                     # SIFIR kalite bilgisi, SIRAYA duyarli
    def s(g):
        if g.paket is None or not g.komsular: return None
        for k in g.komsular:
            if k.dugum == g.paket.hedef: return k.dugum
        return g.komsular[0].dugum
    return s
T = (1,2,3,4,5,6,7,8)
def kos(f,t): return Kosu(Konfig(kol="t",senaryo="S2",tohum=t),f).kostur()["secim_avantaji_ortalama"]
for ad, fab in (("gurultuden_kacan (sira-KOR)", AKTARICILAR["gurultuden_kacan"]),
                ("sira_kolu (sira-DUYARLI)", sira_kolu)):
    tam = [kos(fab,t) - kos(kalite_ablasyonu(fab),t) for t in T]
    yal = [kos(fab,t) - kos(yalniz_sirala(fab),t) for t in T]
    print("\n2) %s" % ad)
    print("   TAM ablasyon farki    : ort=%+.5f std=%.5f poz=%d/8"
          % (statistics.mean(tam), statistics.stdev(tam), sum(1 for x in tam if x>0)))
    print("   YALNIZCA SIRALAMA     : ort=%+.5f std=%.5f poz=%d/8"
          % (statistics.mean(yal), statistics.stdev(yal), sum(1 for x in yal if x>0)))
PY
```

**Beklenen / görülen:**

```
1) >1 komsulu karar : 72071
   SIRASIZ gelen    : 66863  (%92.8)

2) gurultuden_kacan (sira-KOR)
   TAM ablasyon farki    : ort=+0.02827 std=0.02298 poz=8/8
   YALNIZCA SIRALAMA     : ort=+0.00000 std=0.00000 poz=0/8

2) sira_kolu (sira-DUYARLI)
   TAM ablasyon farki    : ort=+0.01205 std=0.08091 poz=4/8
   YALNIZCA SIRALAMA     : ort=+0.01205 std=0.08091 poz=4/8
```

*(Komut ikinci başlığı da `2)` diye basıyor — çıktı burada **olduğu gibi**
verilmiştir; iki koşuda da birebir aynı çıktı.)*

🔴 **Sıraya duyarlı kolda TAM ablasyon farkı ile YALNIZCA-SIRALAMA farkı
BİREBİR aynı — beş ondalık basamağa kadar, sekiz tohumun sekizinde de.**
O kol `bildirdigi_gurultu_w`u **hiç okumuyor**; yani ablasyonun yok ettiği
bilgi miktarı **sıfır** ve ölçülen farkın **%100'ü** yeniden sıralama
artefaktı.

**Büyüklük:** artefaktın std'si **0,081**; kapının ayırt etmesi gereken
gerçek sinyal **+0,0283** *(std 0,0230)*. Yani sıraya duyarlı bir kol için
**gürültü tabanı, sinyalin 2,9 katı ve sinyalin std'sinin 3,5 katı.**
Artefaktın **ortalaması da sıfır değil**: +0,0120 — bilgi taşımayan bir kol
için kapının gerçek sinyalinin **%43'ü**.

**Bugün ateşliyor mu — HAYIR, ve bunu da ölçtüm.** Kendi yazdığım üç
sıfır-bilgi kolunun **üçü de kapıdan geçemedi**:

| kendi null kolum | poz | ort | %95 GA alt | kapı |
|---|---|---|---|---|
| `sira_kolu` *(`komsular[0]`)* | 4/8 | +0,01205 | −0,05561 | GEÇEMEDİ ✅ |
| `sira_kolu_tersten` *(`komsular[-1]`)* | 4/8 | +0,02555 | −0,07458 | GEÇEMEDİ ✅ |
| `yas_kolu` *(en taze komşu)* | 0/8 | **+0,00000** | +0,00000 | GEÇEMEDİ ✅ |

**Kapının bugünkü kararı DOĞRU.** Bulgu şu: `06`'nın *"tek fark BİLGİ"*
cümlesi **ölçümle yanlış**, ve tek Aile 0 kolunun *(kendi içinde
`sorted` yapan `gurultuden_kacan`)* artefakta **kör** olması bir tesadüf.
Aile 1'in kolları `g.komsular` sırasını kullanmakta serbest — ve o kolda
kapının gürültü tabanı 3,5 kat büyür.

⚖️ Bu tam olarak `03` B1'in adlandırdığı tuzak: *"Ablasyonu yanlış yerden
bölmek — tasarım metninin cümlelerinden değil, **mekanizma sınırlarından**
böl."* Sıralama bir mekanizma sınırı değil, bir uygulama ayrıntısı.

---

### 🔴 B-85 · YÜKSEK — `ortak_alt_kume`nin BEŞİNCİ ekseni: kardinalite/kapsama hiç denetlenmiyor; araç **%328,5 kesişim** basıyor

| | |
|---|---|
| **Nerede** | `sim/karsilastirma.py:206-227` *(B-67'nin dört değişmezi)* · `sim/karsilastirma.py:83-94` *(`ozet()`)* |
| **İDDİA** | B-67 *(K-056)*: satır **içi** yapı artık denetleniyor — *"Uzunluk · tekrar · finite · negatiflik değişmezleri"*, ve *"dördü de bugünkü gerçek çıktıda TUTUYOR — yani kırılabilir."* |
| **ÖLÇTÜĞÜM** | Dördü de yerinde. Ama **beşinci eksen açık**: teslim edilen kimliklerin sayısı ve kapsanması hiç denetlenmiyor. **Beş bozuk satır ürettim, beşi de kabul edildi** ve sayı üretti. |

**Üretici komut** *(**koşturuldu: 8,0 sn**)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import copy, sys; sys.path.insert(0, ".")
from sim.config import Konfig
from sim.kosucu import Kosu
from sim.karsilastirma import ortak_alt_kume, KarsilastirmaHatasi
from dogrulama.aktaricilar import AKTARICILAR
a = Kosu(Konfig(kol="A", senaryo="S2", tohum=1), AKTARICILAR["en_kisa_yol"]).kostur()
b = Kosu(Konfig(kol="B", senaryo="S2", tohum=1), AKTARICILAR["hedefe_en_yakin"]).kostur()
print("SAGLAM:", ortak_alt_kume(a, b).ozet())
def dene(ad, boz):
    aa, bb = copy.deepcopy(a), copy.deepcopy(b); boz(aa, bb)
    try: r = ortak_alt_kume(aa, bb)
    except KarsilastirmaHatasi as e: print("[RED]   ", ad, "->", str(e)[:60]); return
    print("[KABUL] ", ad); print("         ", r.ozet())
def e1(aa, bb):
    n = aa["pencerede_uretilen"]; ek = list(range(10**7, 10**7 + 3*n))
    for s, g in ((aa, 0.05), (bb, 0.90)):
        s["teslim_kimlikleri"] = s["teslim_kimlikleri"] + ek
        s["teslim_gecikmeleri_s"] = s["teslim_gecikmeleri_s"] + [g]*len(ek)
dene("E1 teslim sayisi > pencerede_uretilen", e1)
dene("E2 tum kimlikler pencere ARALIGI disinda",
     lambda aa, bb: [s.__setitem__("teslim_kimlikleri",
                     [k+10**9 for k in s["teslim_kimlikleri"]]) for s in (aa, bb)])
dene("E3 pencerede_teslim celiskili",
     lambda aa, bb: (aa.__setitem__("pencerede_teslim", 0),
                     bb.__setitem__("pencerede_teslim", 999999)))
dene("E4 teslim_orani celiskili",
     lambda aa, bb: (aa.__setitem__("teslim_orani", 0.0),
                     bb.__setitem__("teslim_orani", 1.0)))
dene("E5 gecikme kosu suresinin 1e6 kati",
     lambda aa, bb: aa.__setitem__("teslim_gecikmeleri_s",
                     [1e6]*len(aa["teslim_kimlikleri"])))
PY
```

**Beklenen / görülen:**

```
SAGLAM: ortak 770 paket (kesişim %95.3 birleşim, %28.5 pencere) · gecikme A=64.34 ms B=90.56 ms
[KABUL]  E1 teslim sayisi > pencerede_uretilen
          ortak 8864 paket (kesişim %99.6 birleşim, %328.5 pencere) · gecikme A=51.25 ms B=829.69 ms
[KABUL]  E2 tum kimlikler pencere ARALIGI disinda
[KABUL]  E3 pencerede_teslim celiskili
[KABUL]  E4 teslim_orani celiskili
[KABUL]  E5 gecikme kosu suresinin 1e6 kati
          ... gecikme A=1000000000.00 ms B=90.56 ms
```

🔴 **En keskini E1:** araç kendi rapor satırında **`kesişim %328.5 pencere`**
basıyor — bir kesişim oranı %100'ü aşamaz. `ozet()` `03` B3'ün
*"kesişim oranını raporla"* şartını yerine getiren tek satır; o satır
kendi kendini denetlemiyor *(Y7)*.

**Beşinci eksenin üç bileşeni** *(hiçbiri denetlenmiyor)*:

| değişmez | bugün | E-vakası |
|---|---|---|
| `len(teslim_kimlikleri) ≤ pencerede_uretilen` | ❌ yok | E1 → oran %328,5 |
| `teslim_kimlikleri ⊆ pencere_kimlik_araligi` | ❌ yok | E2 → hiç üretilmemiş paketlerden gecikme farkı |
| satır İÇİ tutarlılık *(`pencerede_teslim` ve `teslim_orani` ↔ `teslim_kimlikleri`)* | ❌ yok | E3 · E4 |

⚠️ E5 *(gecikme = 10⁶ sn)* bilinçli bir sınır olabilir — üst sınır için
koşu süresi gerekir ve o alan zorunlu şemada yok. **§8'e yazıldı.**

---

### 🔴 B-86 · YÜKSEK — B-69'un kapanış-hücresi taraması, `08`in **kendi beyan ettiği dört kanaldan üçünü** göremiyor; sınıf tabanlı protokolde **çöküyor**

| | |
|---|---|
| **Nerede** | `tests/test_gozlem.py:1008-1028` *(`_paylasilan_mutable`)* · `v2/08-AILE0-KAPSAM.md:194` |
| **İDDİA** | `08:194` *(B-69 ile düzeltilmiş hâli)*: *"kalan kanal, protokol nesnelerinin **PAYLAŞTIĞI her yazılabilir durumdur** — modül global'i · fabrikayı saran kapsam · **sınıf özniteliği** · fabrikanın kendi `__dict__`i. `test_b69_…` artık örnekler arası paylaşımı **kapanış hücrelerinden** ölçüyor."* |
| **ÖLÇTÜĞÜM** | Tarama yalnızca `prot.__closure__` içindeki `dict/list/set`e bakıyor. Beyan edilen dört kanaldan **birini** görüyor. Sınıf tabanlı bir protokolde ise `AttributeError` ile **çöküyor**. |

**Üretici komut** *(**koşturuldu: 1,7 dk**, 4 tam koşu)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import sys; sys.path.insert(0, "."); sys.path.insert(0, "tests")
from sim.config import Konfig
from sim.kosucu import Kosu
from tests.test_gozlem import _paylasilan_mutable
class SinifP:                       # protokol = SINIF ORNEGI (beacon_yuku/teshis
    ORTAK: dict = {}                # kancalari getattr ile okundugu icin dogal bicim)
    def __init__(self, kon): pass
    def __call__(self, g):
        SinifP.ORTAK[g.dugum] = g.olculen_gurultu_w              # A yazar
        if not g.komsular: return None
        gor = [k.dugum for k in g.komsular if k.dugum in self.ORTAK]
        return min(gor, key=lambda d: self.ORTAK[d]) if gor else min(k.dugum for k in g.komsular)
def bytearray_fab():
    ORTAK = bytearray(64)
    def fab(kon):
        def s(g):
            ORTAK[g.dugum % 64] = min(255, g.kuyruk_uzunlugu)
            if not g.komsular: return None
            return min((k.dugum for k in g.komsular), key=lambda d: ORTAK[d % 64])
        return s
    return fab
def oznitelik_fab():
    class Kutu: pass
    ORTAK = Kutu(); ORTAK.tablo = {}
    def fab(kon):
        def s(g):
            ORTAK.tablo[g.dugum] = g.olculen_gurultu_w
            if not g.komsular: return None
            gor = [k.dugum for k in g.komsular if k.dugum in ORTAK.tablo]
            return min(gor, key=lambda d: ORTAK.tablo[d]) if gor else min(k.dugum for k in g.komsular)
        return s
    return fab
def dict_fab():
    ORTAK = {}
    def fab(kon):
        def s(g):
            ORTAK[g.dugum] = g.olculen_gurultu_w
            if not g.komsular: return None
            gor = [k.dugum for k in g.komsular if k.dugum in ORTAK]
            return min(gor, key=lambda d: ORTAK[d]) if gor else min(k.dugum for k in g.komsular)
        return s
    return fab
kon = Konfig(kol="t", senaryo="S2", tohum=1)
for ad, fab in (("REFERANS · paylasilan dict", dict_fab()),
                ("A · SINIF DEGISKENI", SinifP),
                ("B · bytearray", bytearray_fab()),
                ("C · ORNEK OZNITELIGI", oznitelik_fab())):
    SinifP.ORTAK = {}
    k = Kosu(kon, fab)
    try: c, h = _paylasilan_mutable(k), None
    except Exception as e: c, h = [], "%s: %s" % (type(e).__name__, e)
    s = k.kostur()
    print("%-28s tarama=%2d cakisma %-12s teslim=%.8f" %
          (ad, len(c), "GORDU" if c else "GORMEDI", s["teslim_orani"]),
          ("[COKTU] " + h[:60]) if h else "")
PY
```

**Beklenen / görülen:**

```
REFERANS · paylasilan dict   tarama=39 cakisma GORDU        teslim=0.07857672
A · SINIF DEGISKENI          tarama= 0 cakisma GORMEDI      teslim=0.07857672 [COKTU] AttributeError: 'SinifP' object has no attribute '__closure_
B · bytearray                tarama= 0 cakisma GORMEDI      teslim=0.00000000
C · ORNEK OZNITELIGI         tarama= 0 cakisma GORMEDI      teslim=0.07857672
```

🔴 **C vakası kanıtın kendisi:** örnek özniteliğiyle kurulan kanal, referans
`dict` kanalıyla **birebir aynı teslim oranını** veriyor *(0,07857672…)* —
yani **aynı düğümler arası bilgi kanalı çalışıyor** — ve tarama **sıfır**
diyor.

🔴 **A vakası daha ağır:** protokolün **sınıf örneği** olması deponun kendi
davet ettiği biçim *(`kosucu.py:270, 322` kancaları `getattr(prot,
"beacon_yuku")` / `getattr(prot, "teshis")` ile okuyor — öznitelik taşıyan
bir nesne varsayıyor)*. O biçimde tarama **çalışmıyor bile**.

Bugün `test_b69_dogrulama_aktaricilari_YAZILABILIR_durum_PAYLASMIYOR`
yalnızca `AKTARICILAR`ı *(beşi de düz fonksiyon)* geziyor, bu yüzden
çökme görünmüyor.

---

### 🔴 B-87 · YÜKSEK — B-68'in açtığı `teshis` kancasının **hiçbir sözleşmesi yok**; kardeşi `beacon_yuku`nun sıkı sözleşmesi var

| | |
|---|---|
| **Nerede** | `sim/kosucu.py:266-274` *(`_protokol_teshislerini_topla`)* · karşılaştırma: `sim/kosucu.py:319-325` + `sim/gozlem.py:258-304` *(`yuk_bayt`)* |
| **İDDİA** | K-056/B-68: *"Kanca `beacon_yuku`nun deseniyle **birebir aynı**: isteğe bağlı, protokolün KENDİ örneğine ait, simülatöre referans taşımıyor. Şekil: `{sayaç_adı: {düğüm: değer}}`."* |
| **ÖLÇTÜĞÜM** | *"Simülatöre referans taşımıyor"* doğru. *"Birebir aynı desen"* **değil**: `beacon_yuku` `yuk_bayt()`ten geçip tipi, boyutu ve bedeli denetleniyor ve ihlalde **`YukHatasi`** fırlatıyor. `teshis` **hiçbir denetimden geçmiyor**. Sekiz sözleşme dışı yük denedim: **8'i de kabul edildi**, **4'ü sonuç yazıcısını** koşu bittikten sonra düşürdü. |

**Üretici komut** *(**koşturuldu: 4,0 dk**, 16 tam koşu)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import pathlib, sys, tempfile; sys.path.insert(0, ".")
from sim.config import Konfig
from sim.kosucu import Kosu
from sim.results import SonucYazici
def yap(fn):
    class P:
        def __init__(self, kon): pass
        def __call__(self, g): return min((k.dugum for k in g.komsular), default=None)
        def teshis(self, dugum): return fn(dugum)
    return P
D = [("dogru kullanim", lambda d: {"karar": d}),
     ("ANAHTAR int", lambda d: {12345: d}),
     ("ANAHTAR demet", lambda d: {(1, 2): d}),
     ("ANAHTAR 1 MB dizgi", lambda d: {"z"*1_000_000: d}),
     ("DEGER 100k liste", lambda d: {"buyuk": list(range(100_000))}),
     ("DEGER serilestirilemez", lambda d: {"nesne": object()}),
     ("DEGER Konfig (YASAK_TIPLER)", lambda d: {"kon": Konfig(kol="x")}),
     ("DEGER kendini iceren liste", lambda d: (lambda L: (L.append(L), {"d": L})[1])([]))]
for ad, fn in D:
    try: s = Kosu(Konfig(kol="t", senaryo="S0", tohum=1), yap(fn)).kostur()
    except Exception as e: print("KOSU RED  %-30s %s" % (ad, type(e).__name__)); continue
    yol = pathlib.Path(tempfile.mkdtemp()) / "s.jsonl"
    try:
        with SonucYazici(yol, "x") as w:
            w.yaz({"kol":"t"}, {"korunum_tamam":True}, {"protokol_teshis": s["protokol_teshis"]})
        print("KABUL + YAZDI  %-30s %d bayt" % (ad, yol.stat().st_size))
    except Exception as e:
        print("KABUL + YAZICI DUSTU  %-22s %s: %s" % (ad, type(e).__name__, str(e)[:44]))
PY
```

**Beklenen / görülen:**

```
KABUL + YAZDI  dogru kullanim                 509 bayt
KABUL + YAZDI  ANAHTAR int                    509 bayt
KABUL + YAZICI DUSTU  ANAHTAR demet          TypeError: keys must be str, int, float, bool or None,
KABUL + YAZDI  ANAHTAR 1 MB dizgi             1000504 bayt
KABUL + YAZDI  DEGER 100k liste               27556039 bayt
KABUL + YAZICI DUSTU  DEGER serilestirilemez TypeError: Object of type object is not JSON serializab
KABUL + YAZICI DUSTU  DEGER Konfig (YASAK_TIPLER) TypeError: Object of type Konfig is not JSON serializab
KABUL + YAZICI DUSTU  DEGER kendini iceren liste ValueError: Circular reference detected
```

🔴 **En ağırı `Konfig` vakası:** `sim/gozlem.py:313-317` `YASAK_TIPLER`
listesinde `"Konfig"` var ve *"Bu tiplerden birine ULAŞILABİLİYORSA
sözleşme kırılmıştır"* yazıyor. `teshis` yolu bir `Konfig` örneğini
**sonuç sözlüğüne** koyuyor ve hiçbir şey konuşmuyor. *(Karar kanalı
değil — rulo 5 ihlali **değil**; ama `test_c5_1b`in yüzey taraması
`Gozlem`den başlıyor ve **sonuç sözlüğünü hiç taramıyor**.)*

🔴 **Zamanlama da yanlış tarafta:** `beacon_yuku` ihlali **anında**,
tipli bir hatayla *(`YukHatasi`)* patlıyor. `teshis` ihlali koşu
**bittikten sonra**, ham bir `TypeError` ile ve **yazma anında** patlıyor —
o noktada koşu zaten harcanmıştır.

⚠️ Şema `05` §D için **donduruldu** *(`kosucu.py:225-227`: "SLOT ŞİMDİ
AÇILIYOR: şema Aile 1 başladıktan sonra değiştirilemez")*. Sözleşmesi
şimdi yazılmazsa sonra yazılamaz.

**`teshis` bir GERİ KANAL DEĞİL — bunu ayrıca ölçtüm ve doğrudur:**
`Kosu.kostur()` kancayı olay döngüsünden **sonra** çağırıyor
*(`kosucu.py:242-248`)* ve `self.protokol_teshis` yalnızca `sonuc()`ta
okunuyor *(satırlar 227, 242, 245, 248, 273, 573; başka okuyan yok)*.
Bir protokol yazdığını **sonraki kararda okuyamaz.**

---

### 🔴 B-88 · YÜKSEK — Mutasyon paketinin **DÖRDÜNCÜ** geçersizlik yolu elle yazılmış bir etiket taşıyor; B-79'un 9 testinin **hiçbiri** oraya dokunmuyor

| | |
|---|---|
| **Nerede** | `dogrulama/mutasyon_paketi.py:344` *(`cokme = "ERROR" in p.stdout …`)* · `:606-607` *(elle yazılmış etiket)* · `tests/test_kapi_secimleri.py::test_b79_*` ×9 *(K-058'in "13 yeni koruma"sı = `test_b78_*` ×4 + `test_b79_*` ×9)* |
| **İDDİA** | K-058: *"Sebep metinleri **test edilebilir fonksiyonlara** çıkarıldı"* · `gecersiz_sebebi` docstring'i: *"🔴 Y7 — ARAÇ, YAPMADIĞI TEŞHİSİ RAPOR EDEMEZ … yerinde duran tek satır ('mutasyon uygulanamadı') **üç ayrı olayı** aynı etikete indiriyordu"* |
| **ÖLÇTÜĞÜM** | Olay **üç değil DÖRT**. `_kosu` üç tipli olay üretiyor *(desen · zaman aşımı · istisna)* ve üçü de `gecersiz_sebebi`den geçiyor. **Dördüncüsü** toplama katmanında, `gecersiz_sebebi`yi **atlayarak**, sabit bir dizgiyle yazılıyor. 9 `test_b79_*` testinin **hiçbiri** o satırı çağırmıyor. |

**Üretici komut** *(anlık)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import ast, pathlib
src = pathlib.Path("dogrulama/mutasyon_paketi.py").read_bytes().decode("utf-8")
kosu = next(d for d in ast.walk(ast.parse(src))
            if isinstance(d, ast.FunctionDef) and d.name == "_kosu")
print("1) `_kosu`nun URETTIGI GECERSIZLIK OLAYLARI (hepsi tipli):")
for d in ast.walk(kosu):
    if isinstance(d, ast.Return) and isinstance(d.value, ast.Dict):
        a = [k.value for k in d.value.keys if isinstance(k, ast.Constant)]
        if "hata" in a: print("   satir %d: %s" % (d.lineno, a))
print("2) TOPLAMA KATMANINDAKI YOLLAR:")
for i, s in enumerate(src.splitlines(), 1):
    if "gecersiz.append" in s: print("   satir %d: %s" % (i, s.strip()))
print("3) `cokme` NASIL HESAPLANIYOR:")
for i, s in enumerate(src.splitlines(), 1):
    if "cokme =" in s or 'if r["cokme"]' in s: print("   satir %d: %s" % (i, s.strip()))
print("4) `test_b79_*` DORDUNCU YOLU TUTUYOR MU:")
t = pathlib.Path("tests/test_kapi_secimleri.py").read_text(encoding="utf-8")
for p in ("çökme/collect", "cokme", "koşturulamadı"):
    print("   %-16r test dosyasinda geciyor mu: %s" % (p, p in t))
PY
```

**Beklenen / görülen:**

```
1) `_kosu`nun URETTIGI GECERSIZLIK OLAYLARI (hepsi tipli):
   satir 329: ['ad', 'tur', 'hata']
   satir 359: ['ad', 'tur', 'hata']
   satir 362: ['ad', 'tur', 'hata']
2) TOPLAMA KATMANINDAKI YOLLAR:
   satir 598: gecersiz.append((r["ad"], gecersiz_sebebi(r)))
   satir 607: gecersiz.append((r["ad"], "mutant koşturulamadı (çökme/collect hatası)"))
3) `cokme` NASIL HESAPLANIYOR:
   satir 344: cokme = "ERROR" in p.stdout or p.returncode not in (0, 1)
   satir 606: if r["cokme"] and not r["sayi"]:
4) `test_b79_*` DORDUNCU YOLU TUTUYOR MU:
   'çökme/collect'  test dosyasinda geciyor mu: False
   'cokme'          test dosyasinda geciyor mu: False
   'koşturulamadı'  test dosyasinda geciyor mu: False
```

🔴 **MUTASYONLA SINANDI — SAĞ KALDI.** O satırdaki etiketi K-058'in
**yanlış olduğu ölçülen** etiketiyle değiştirdim:

```python
gecersiz.append((r["ad"], "mutasyon uygulanamadı"))
```

**367 testin 367'si geçti** *(§5, `C23`, 1 286 s)*. Yani kapı, K-058'in
kapattığı hatayı **birebir tekrar** yapabilir ve hiçbir test konuşmaz.

🔴 **İkinci kusur, aynı satırda:** `"ERROR" in p.stdout` bir **alt dizgi
aramasıdır**, bir teşhis değil. `p.returncode not in (0, 1)` ile birlikte
**üç ayrı olayı** *(gerçek collect hatası · standart dışı çıkış kodu ·
çıktıda "ERROR" geçen herhangi bir satır)* tek bir etikete indiriyor —
**K-058'in kapattığı hatanın tam olarak aynısı**, bir katman yukarıda.

**Y8 — yol tetiklenebilir mi:** evet, ve **bu depoda tetiklendi.** Kodun
kendi yorumu *(`mutasyon_paketi.py:603`)*: *"İlk koşuda tam olarak bu oldu:
D15, dataclass'ı kurulamaz yapıyordu."* `04:1466` D15'i kayıtta taşıyor.

⚖️ **Bu yol kapıyı DÜŞÜRÜR** *(`gecti` = … `and not gecersiz`)*. Yani
etiketin doğruluğu akademik değil: kapı bir daha o yoldan düşerse, teşhis
yine yanlış yöne sapar.

---

### 🟠 B-89 · ORTA — B-76'nın işaretleyicisi **prozayı koddan ayırt etmiyor**; bu, B-68'in **aynı oturumda** reddettiği desenin ta kendisi

| | |
|---|---|
| **Nerede** | `tests/test_gozlem.py:67-76` *(`inspect.getsource` + `in govde`)* · karşılaştırma: `tests/test_mekanizma_kapisi.py:538-546` *(B-68 · AST)* |
| **İDDİA** | K-056/B-76: *"İşaretleyici artık gövdeyi **çalışma anında** doğruluyor."* · Aynı oturum, B-68: *"Bir kaynak denetimi prozayı koddan ayırt edemiyorsa ölçüt değildir — **AST**'ye bağlandı."* |
| **ÖLÇTÜĞÜM** | B-76'nın denetimi `inspect.getsource(fn)` metninde **düz alt dizgi** arıyor ve yalnızca `@` ile başlayan satırları eliyor. **Docstring ve yorum satırları gövdeye dâhil.** |

**Üretici komut** *(**koşturuldu: 1,0 sn**)* — ⚠️ ilk yazımı **çalışmadı**:
`inspect.getsource` **stdin'den okuyamaz** *(`OSError: could not get source
code`)*, bu yüzden geçici bir **modül dosyası** gerekiyor:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import pathlib, sys, tempfile
sys.path.insert(0, "."); sys.path.insert(0, "tests")
gec = pathlib.Path(tempfile.mkdtemp()) / "b89_prova.py"
gec.write_text('''
from tests.test_gozlem import icerik_testi

def vaka_docstring():
    @icerik_testi("son_iletim_sonucu")
    def sahte():
        """Bu test `son_iletim_sonucu` alanini dogruladigini SOYLUYOR."""
        assert 1 == 1                      # alan adi GOVDEDE YOK
    return sorted(sahte._gozlem_alanlari)

def vaka_yorum():
    @icerik_testi("kanal_mesgul_mu")
    def sahte2():
        # kanal_mesgul_mu  <- yalnizca YORUM satirinda
        assert 1 == 1
    return sorted(sahte2._gozlem_alanlari)
''', encoding="utf-8")
sys.path.insert(0, str(gec.parent))
import b89_prova
for ad, fn in (("yalnizca DOCSTRING", b89_prova.vaka_docstring),
               ("yalnizca YORUM", b89_prova.vaka_yorum)):
    try:
        print("🔴 KABUL — %-20s -> isaretlendi: %s" % (ad, fn()))
    except AssertionError as e:
        print("REDDEDILDI — %-20s %s" % (ad, str(e)[:70]))
PY
```

**Beklenen / görülen:**

```
🔴 KABUL — yalnizca DOCSTRING   -> isaretlendi: ['son_iletim_sonucu']
🔴 KABUL — yalnizca YORUM       -> isaretlendi: ['kanal_mesgul_mu']
```

**Bugün canlı bir vaka VAR MI — HAYIR, ve bunu ayrıca ölçtüm.** 9
işaretli testin **9'unda** alan adı, docstring'ler AST ile çıkarıldıktan
sonra da gövdede geçiyor *(`icerik_testi` 11 yerde kullanılıyor; ikisi
`test_b76_*`in kendi iç içe kontrol fonksiyonları)*. Açık **yapısal**, sonuç **bugün doğru**.

🔴 **Ama B-76'nın kendi Y11 testi bu sınırı sınamıyor.** Negatif kontrol
*(`test_b76_isaretleyici_YANLIS_alani_reddediyor`)* gövdesi `return 42`
olan bir test kullanıyor — **ne docstring'i ne yorumu var.** Yani koruma
*"hiç geçmeyen"* vakayla sınanmış, *"yalnızca prozada geçen"* vakayla
sınanmamış. **Y11'in tam tanımı**, B-76'nın düzeltmesinin içinde.

---

### 🟠 B-90 · ORTA — `CEKISME_CARPANI = 1,60` ölçümle aşıldı: tam paketi **bitiren** 11 mutantta çarpan **1,55 – 1,78** *(ortanca 1,74)*

| | |
|---|---|
| **Nerede** | `dogrulama/mutasyon_paketi.py:96` · `tests/test_kapi_secimleri.py:418-424` *(`_gereken_zaman_asimi_s`)* |
| **İDDİA** | `mutasyon_paketi.py:92-96`: *"⚠️ **ALT SINIR.** 8 yollu koşuda biten TEK mutant 18,5 dk sürdü *(1,46×)*; diğer 7'si 20 dk'da HÂLÂ bitmemişti, yani gerçek çarpan ≥ 1,57. **Ölçülemeyen bir üst sınıra 'ölçüldü' denmez** — güvenli tarafa 1,60 alınıyor."* |
| **ÖLÇTÜĞÜM** | Üst sınır artık **ölçüldü**. 35 mutantlık kampanyamda **11 mutant tam paketi bitirdi** *(zaman aşımına uğramadan, `Pool(6)`)*. Çarpan **1,548 – 1,780**, **ortanca 1,744** — yazılı 1,60'ın **üstünde**. |

**Üretici komut** *(kampanyanın kendi kaydından; anlık)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import statistics
TABAN = 768.56          # bu makinede tek kosu, bos makine: 367 passed in 768.56s
SAG = [1354.2, 1361.2, 1364.4, 1329.4, 1326.3, 1335.0, 1340.4, 1342.1,
       1368.3, 1286.1, 1189.6]        # Pool(6), TAM paketi bitiren 11 mutant
o = sorted(s / TABAN for s in SAG)
print("olculen cekisme carpani : %.3f - %.3f  (ortanca %.3f)" % (o[0], o[-1], statistics.median(o)))
print("yazili CEKISME_CARPANI  : 1.60")
print("kodun ongordugu sure    : 828.3 * 1.60 = %.0f sn" % (828.3 * 1.60))
print("olculen ortanca sure    : %.0f sn" % statistics.median(SAG))
print("gereken zaman asimi     : 828.3 * 1.60 * 1.50 = %.0f sn" % (828.3 * 1.60 * 1.50))
print("olculen ortancaya gore  : 828.3 * %.3f * 1.50 = %.0f sn"
      % (statistics.median(o), 828.3 * statistics.median(o) * 1.50))
print("yazili MUTANT_ZAMAN_ASIMI_S = 3600 -> marj %.2fx (yazili) / %.2fx (olculen)"
      % (3600 / (828.3*1.60*1.50), 3600 / (828.3*statistics.median(o)*1.50)))
PY
```

**Beklenen / görülen:**

```
olculen cekisme carpani : 1.548 - 1.780  (ortanca 1.744)
yazili CEKISME_CARPANI  : 1.60
kodun ongordugu sure    : 828.3 * 1.60 = 1325 sn
olculen ortanca sure    : 1340 sn
gereken zaman asimi     : 828.3 * 1.60 * 1.50 = 1988 sn
olculen ortancaya gore  : 828.3 * 1.744 * 1.50 = 2167 sn
yazili MUTANT_ZAMAN_ASIMI_S = 3600 -> marj 1.81x (yazili) / 1.66x (olculen)
```

🔴 **Ve benim ölçümüm `Pool(6)`; kapı `Pool(8)` kullanıyor.** Yani gerçek
çarpan ölçtüğümden **daha büyüktür**; 1,60 iki kere birden düşük.

**Bugün kapıyı düşürür mü — HAYIR.** 3 600 sn sabiti ölçülen ihtiyaca göre
**1,66× marjla** hâlâ yeterli. Bulgu şudur: `test_b78_*`'in *"gereken zaman
aşımı"* hesabı **ölçülmüş bir çarpanın altındaki** bir sabitle yapılıyor, ve
o hesap kapının **tek** koruyucusu. Marj gerçekte ilan edilenden **%8 daha
dar**.

⚠️ **Kendi ölçümümün yanlılığı:** taban *(768,56 sn)* boş makinede,
mutantlar ise `Pool(6)` **artı** benim eşzamanlı tek koşuluk ölçüm
betiklerimle koştu. Yani 1,744 bir **üst tahmin** olabilir. Ama 1,60'ın
**altındaki tek gözlem yok** — 11 ölçümün **en küçüğü 1,548**, ortancası
1,744, ve 11'in **10'u** 1,60'ın üstünde.

---

### 🟠 B-91 · ORTA — Dördüncü denetimin önerdiği **6 kapsam maddesinin 1'i** eklendi; *"yayılma gecikmesi"* `08`e hiç girmedi ve elenmesi kayda geçmedi

| | |
|---|---|
| **Nerede** | `aile0_audit.md` §7 *(dördüncü denetim, madde 25…30)* · `v2/08-AILE0-KAPSAM.md` · `v2/04-NEDEN-BOYLE.md` K-056 *("NE ELENDİ")* |
| **İDDİA** | K-056 *"BUNU NE DEĞİŞTİRİR"*: *"`08` **24 → 25 madde**"* |
| **ÖLÇTÜĞÜM** | `08` gerçekten 24 → 25 oldu. **Ama eklenen madde 25, önerilen altısından HİÇBİRİ değil** — B-77'nin kontrol düzlemi bütçesi. Önerilen madde 25 *(yayılma gecikmesi)* `08`de **hiç geçmiyor**, ve K-056'nın *"NE ELENDİ"* tablosunda da yok. |

**Üretici komut** *(anlık)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import pathlib
k = pathlib.Path("v2/08-AILE0-KAPSAM.md").read_bytes().decode("utf-8")
for kelime in ("yayılma", "yayilma", "propagation", "yayılma gecikmesi"):
    print("08'de %-18r -> %d kez" % (kelime, k.lower().count(kelime.lower())))
print()
print("08 madde 25'in KONUSU:")
print([s for s in k.splitlines() if s.startswith("| **25**")][0][:150])
print()
n = pathlib.Path("v2/04-NEDEN-BOYLE.md").read_text(encoding="utf-8")
i = n.find("# K-056"); j = n.find("# K-057")
print("K-056'nin 'NE ELENDI' tablosunda 'yayilma' geciyor mu:",
      "yayılma" in n[i:j].lower())
PY
```

**Beklenen / görülen:**

```
08'de 'yayılma'          -> 0 kez
08'de 'yayilma'          -> 0 kez
08'de 'propagation'      -> 0 kez
08'de 'yayılma gecikmesi' -> 0 kez

08 madde 25'in KONUSU:
| **25** | 🆕 **Kontrol düzlemi bütçesi kollar arasında SINIRSIZ farklılaşabilir** — K-009'un *"eşit kontrol düzlemi bütçesi"* adalet şartını zorlayan 

K-056'nin 'NE ELENDI' tablosunda 'yayilma' geciyor mu: False
```

**Altı önerinin bugünkü durumu:**

| öneri | ne oldu | kayıtlı mı |
|---|---|---|
| 25 · **yayılma gecikmesi** *(280 m'de 0,93 µs, girişim menzilinde 2,01 µs; `cca_s = 4 µs`in **%23–50'si**)* | 🔴 **hiç girmedi** | ❌ elenmesi de yazılmadı |
| 26 · kopya önbelleği **yaşlandırılmıyor** | 🟡 kısmen — madde 11 *"sınırsız"* diyor, *"yaşlandırılmıyor"* demiyor | ⚠️ |
| 27 · yük bedeli bilgiden bağımsız | ✅ **koda** girdi *(B-66)* — beyan **eksik** *(**B-81**)* | ⚠️ |
| 28 · yayın alıcı kredisi | ✅ koda girdi *(B-70)* | ✅ |
| 29 · `protokol_teshis` doldurulamıyor | ✅ koda girdi *(B-68)* | ✅ |
| 30 · kapı kapsam koruması test **adına** bakıyor | 🔴 hiç girmedi | ❌ |

`08` **B-57 kapanınca mühürlenecek.** Mühür anında listede olmayan bir
modelleme sınırı, sonsuza kadar listede olmaz.

---

### 🟡 B-92 · DÜŞÜK-ORTA — `06`'nın revize H1.1 kapısı **ÜÇ** koşul sayıyor, onu uygulayan test **İKİ** koşul uyguluyor

| | |
|---|---|
| **Nerede** | `v2/06-ON-KAYIT.md:408-418` · `tests/test_mekanizma_kapisi.py:442-478` |
| **İDDİA** | B-73'ün düzeltmesi: *"İkisi de kaldırıldı; **yeni kapının metni ile testi aynı satırdan okunuyor.**"* |
| **ÖLÇTÜĞÜM** | `06` üç koşul listeliyor ve *"🔴 **Bu üçü** sağlanmıyorsa … sonuca bakılmaz"* diyor. Testin docstring'i *"KAPI **(iki koşul birden)**"* diyor ve **iki** `assert` içeriyor. Üçüncü koşul *(`ara_bolge_karar` ve `olu_bag_karar` **oran** cinsinden raporlanır)* hiçbir kapı testinde zorlanmıyor. |

**Üretici komut** *(anlık)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import ast, pathlib
t = pathlib.Path("v2/06-ON-KAYIT.md").read_bytes().decode("utf-8").splitlines()
i = next(k for k, s in enumerate(t) if "EŞLEŞTİRİLMİŞ ABLASYON" in s)
print("06'NIN KOSULLARI:")
for s in t[i:i+20]:
    if s.startswith("| 1 |") or s.startswith("| 2 |") or s.startswith("| 3 |"):
        print("  ", s[:120])
    if "Bu üçü" in s: print("  ->", s.strip()[:100])
src = pathlib.Path("tests/test_mekanizma_kapisi.py").read_text(encoding="utf-8")
fn = next(d for d in ast.walk(ast.parse(src)) if isinstance(d, ast.FunctionDef)
          and d.name == "test_b65_mekanizma_kapisi_ESLESTIRILMIS_ablasyona_karsi")
print()
print("TESTIN DOCSTRING'INDE:", [x.strip() for x in ast.get_docstring(fn).splitlines()
                                 if "koşul" in x][:2])
print("TESTTEKI assert SAYISI:", sum(1 for d in ast.walk(fn) if isinstance(d, ast.Assert)))
PY
```

**Beklenen / görülen:**

```
06'NIN KOSULLARI:
   | 1 | Eşleştirilmiş fark *(kol − kendi ablasyonu)* **≥ 8 tohumun 7'sinde pozitif** *(işaret testi, tek yönlü p ≤ 0,035)*
   | 2 | Farkın **%95 güven aralığı sıfırı dışlamalı** |
   | 3 | `ara_bolge_karar` ve `olu_bag_karar` **karar başına ORAN** cinsinden raporlanır; mutlak sayı **kullanılmaz** |
  -> 🔴 **Bu üçü sağlanmıyorsa teslimdeki farkın sebebi mekanizma değildir ve

TESTIN DOCSTRING'INDE: ['KAPI (iki koşul birden):']
TESTTEKI assert SAYISI: 2
```

Üçüncü koşul bir **raporlama** şartı olduğu için pass/fail yüklemine
çevrilmesi zor olabilir — ama `06` onu *"sağlanmıyorsa sonuca bakılmaz"*
diye **kapı koşulu** ilan ediyor. **Ya `06`nın sayısı ya testin sayısı
yanlış.** B-73 tam olarak *"metin ve test farklı yüklem"* için açılmıştı.

---

### 🟡 B-93 · DÜŞÜK — `sim/` altındaki **5 değişmezin 5'i** `assert`; `python -O` altında sessizce kalkar ve **4'ü sessiz yanlış cevap** verir. Hiçbir belgede beyan yok

| | |
|---|---|
| **Nerede** | `sim/events.py:71` · `sim/traffic.py:113` · `sim/kosucu.py:296` · `sim/mac.py:546` · `sim/mac.py:666` |
| **İDDİA** | `mac.py:546`: *"🔴 ASIL RİSK: yarı çift yönlü kontrolü bir gün kalkarsa bu dal **SESSİZCE** doğru cevabı vermeye başlar ve hatayı MASKELER"* → bu yüzden `assert`e çevrildi. `mac.py:666`: *"Assert olarak DURUYOR çünkü … sessizce yanlış cevap vermek yerine **PATLAR**."* |
| **ÖLÇTÜĞÜM** | `python -O` altında `assert` **derlenmiyor** — beşi de kaybolur ve *"patlar"* gerekçesi **tersine döner**. `08` *(kapsam listesi)*, `07` *(arayüz)* ve kapı raporu **hiçbiri** yorumlayıcı bayrağını beyan etmiyor. |

**Üretici komut** *(**koşturuldu: anlık**; alttaki iki `-O` koşusu 44 sn)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import ast, pathlib, subprocess, sys
for bayrak in ([], ["-O"]):
    p = subprocess.run([sys.executable, *bayrak, "-c",
                        "print('assert ETKIN' if __debug__ else 'assert SILINDI')"],
                       capture_output=True, text=True)
    print("python %-12s -> %s" % (" ".join(bayrak) or "(bayraksiz)", p.stdout.strip()))
sayim = {}
for y in sorted(pathlib.Path("sim").glob("*.py")):
    n = sum(1 for d in ast.walk(ast.parse(y.read_text(encoding="utf-8")))
            if isinstance(d, ast.Assert))
    if n: sayim[y.name] = n
print("sim/ altindaki assert degismezleri:", sayim, "toplam", sum(sayim.values()))
for d in ("v2/08-AILE0-KAPSAM.md", "v2/07-SIMULATOR-ARAYUZ.md",
          "dogrulama/aile0_kapi_raporu.py"):
    t = pathlib.Path(d).read_text(encoding="utf-8")
    print("%-38s 'python -O' / '__debug__' beyani: %s"
          % (d, "VAR" if ("python -O" in t or "__debug__" in t) else "YOK"))
PY
```
```bash
PYTHONIOENCODING=utf-8 python  -c "import hashlib,sys;sys.path.insert(0,'.');from sim.config import Konfig;from sim.kosucu import Kosu;from dogrulama.aktaricilar import en_kisa_yol;s=Kosu(Konfig(kol='t',senaryo='S2',tohum=3),en_kisa_yol).kostur();print(('O' if not __debug__ else '-'),hashlib.blake2b(repr(sorted(s.items())).encode(),digest_size=12).hexdigest())"
```
```bash
PYTHONIOENCODING=utf-8 python -O -c "import hashlib,sys;sys.path.insert(0,'.');from sim.config import Konfig;from sim.kosucu import Kosu;from dogrulama.aktaricilar import en_kisa_yol;s=Kosu(Konfig(kol='t',senaryo='S2',tohum=3),en_kisa_yol).kostur();print(('O' if not __debug__ else '-'),hashlib.blake2b(repr(sorted(s.items())).encode(),digest_size=12).hexdigest())"
```

**Beklenen / görülen:**

Birinci komut:

```
python (bayraksiz)  -> assert ETKIN
python -O           -> assert SILINDI
sim/ altindaki assert degismezleri: {'events.py': 1, 'kosucu.py': 1, 'mac.py': 2, 'traffic.py': 1} toplam 5
v2/08-AILE0-KAPSAM.md                  'python -O' / '__debug__' beyani: YOK
v2/07-SIMULATOR-ARAYUZ.md              'python -O' / '__debug__' beyani: YOK
dogrulama/aile0_kapi_raporu.py         'python -O' / '__debug__' beyani: YOK
```

İkinci ve üçüncü komut *(ayrı çıktılar; yan yana verilmiştir)*:

```
- aecc804b06cfa177b8e1460b
```
```
O aecc804b06cfa177b8e1460b
```

🟢 **BUGÜN ZARARSIZ — ölçüldü:** `-O` ile ve `-O`suz tam sonuç sözlüğünün
blake2b'si **aynı** *(`aecc804b06cfa177b8e1460b`)*. Beşi de sağlam koşuda
zaten tetiklenmiyor.

🔴 **Ama beşinin dördü, kalktığında SESSİZ yanlış cevap verir:**

| dosya:satır | `-O` altında ne olur |
|---|---|
| `events.py:71` *(olay zamanı geriye gitmez)* | 🔴 zaman geriye gider, **sessiz** |
| `traffic.py:113` *(pencere dışında üretim yok)* | 🔴 pencere dışı paket ölçüme girer, **sessiz** |
| `kosucu.py:296` *(koşu sonrası beacon yok)* | 🔴 **sessiz** |
| `mac.py:546` *(alıcı kendi iletimini girişim saymaz)* | 🔴 alıcının kendi gücü girişime eklenir, **sessiz** |
| `mac.py:666` *(`per is not None`)* | 🟢 `cekim >= None` → `TypeError`, **gürültülü** |

Bu bir **beyan eksikliğidir**: `08`e madde önerisi §7'de.

---

### 🟡 B-94 · DÜŞÜK-ORTA — Ç2.2 *(belirlenimcilik)* deponun **`hash()` kullanan tek karar yolunu** hiç koşmuyor ve **47 sonuç alanından 3'ünü** karşılaştırıyor

| | |
|---|---|
| **Nerede** | `tests/test_kapi_aile0.py:158-180` *(Ç2.2)* · `dogrulama/aktaricilar.py:93` |
| **İDDİA** | Ç2.2: *"Bir yerde yerleşik `hash()` kullanılsaydı aynı tohum farklı günlerde farklı sonuç verirdi ve sebebi asla bulunamazdı."* · `kosucu.py:91`: *"🔴 `hash()` DEĞİL blake2b: Python'un yerleşik hash'i çalışmalar arasında tuzlanır (PYTHONHASHSEED) ve Ç2'yi kırardı."* |
| **ÖLÇTÜĞÜM** | Depoda yerleşik `hash()` **bir yerde karar yolunda kullanılıyor**: `kalite_ablasyonu` permütasyonu `random.Random(hash(anahtar) & 0xFFFFFFFF)` ile tohumlanıyor — ve o, **ön-kayıtlı H1.1 kapısının null modelidir**. Ç2.2 yalnızca `en_kisa_yol` koluyla koşuyor *(o kolda `hash()` yok)* ve yalnızca **3 alanı** *(`teslim_orani`, `pencerede_teslim`, `mac_gonderilen`)* karşılaştırıyor. |

**Üretici komut** *(**koşturuldu: 2,7 dk**, 4 × 3 tam koşu)*:

```bash
for S in 0 1 42 random; do
PYTHONHASHSEED=$S PYTHONIOENCODING=utf-8 python - <<'PY'
import hashlib, json, os, sys; sys.path.insert(0, ".")
from dogrulama.aktaricilar import AKTARICILAR, kalite_ablasyonu
from sim.config import Konfig
from sim.kosucu import Kosu
abl = kalite_ablasyonu(AKTARICILAR["gurultuden_kacan"])
o = {}
for t in (1, 3, 5):
    s = Kosu(Konfig(kol="t", senaryo="S2", tohum=t), abl).kostur()
    o[str(t)] = hashlib.blake2b(repr(sorted(s.items())).encode(),
                                digest_size=12).hexdigest()
o["hash_int_demeti"] = hash((7, (1, 2, 3, 40)))
o["hash_dizgi"] = hash("ayni_dizgi")
print(os.environ.get("PYTHONHASHSEED"), json.dumps(o, sort_keys=True))
PY
done
```

**Beklenen / görülen:**

```
0 {"1": "9493cf8c4203347794315483", "3": "d0df9e44455d025e6770370c", "5": "58380307093f797db63e8152", "hash_dizgi": -2411182915114269216, "hash_int_demeti": 8679648302257419502}
1 {"1": "9493cf8c4203347794315483", "3": "d0df9e44455d025e6770370c", "5": "58380307093f797db63e8152", "hash_dizgi": -730943642425119680, "hash_int_demeti": 8679648302257419502}
42 {"1": "9493cf8c4203347794315483", "3": "d0df9e44455d025e6770370c", "5": "58380307093f797db63e8152", "hash_dizgi": 3808479939660462673, "hash_int_demeti": 8679648302257419502}
random {"1": "9493cf8c4203347794315483", "3": "d0df9e44455d025e6770370c", "5": "58380307093f797db63e8152", "hash_dizgi": 5898592604446463375, "hash_int_demeti": 8679648302257419502}
```

⚠️ **Son satırdaki `hash_dizgi` her koşuda DEĞİŞİR** *(`PYTHONHASHSEED=random`)*
— bulgunun kanıtı zaten budur. Üç sonuç hash'i ve `hash_int_demeti`
**dört koşuda da sabit**.

🟢 **BUGÜN TUTUYOR — ve sebebi ölçüldü:** `anahtar` bir **tamsayı demeti**
ve CPython tamsayı/demet hash'lerini **tuzlamaz**; `hash((7,(1,2,3,40)))`
dört tohum değerinde de **8679648302257419502**, oysa `hash("ayni_dizgi")`
dördünde de **farklı**. Kapının null modeli `PYTHONHASHSEED`ten bağımsız.

🔴 **Bulgu, sonucun kendisi değil, KAPSAM:** Ç2 belirlenimcilik kriteri
ön-kayıtlı bir çıkış koşulu; onu sağlayan şey, deponun **kendi yazılı
kuralının ihlal edildiği** tek satırda *(`hash()` kullanımı)*, **CPython'un
beyan edilmemiş bir uygulama ayrıntısıdır**. Ve Ç2.2 o satırı **hiç
koşmuyor**. Bir gün `anahtar`a bir dizgi eklenirse *(ör. `alan` adı —
`kalite_ablasyonu`nun **imzasında var**)*, kapının null modeli
`PYTHONHASHSEED`e bağlı olur ve **Ç2.2 bunu göremez**.

---

### 🔴 B-95 · YÜKSEK — B-50'nin koruması **indirgemenin yalnızca BİR yönünü** yakalıyor; ayna yönü 367 testten sağ çıkıyor

| | |
|---|---|
| **Nerede** | `tests/test_kosucu.py:237-256` · `sim/kosucu.py:601` · `dogrulama/aile0_kapi_raporu.py:328` *(Ç1.4'ün payı)* |
| **İDDİA** | B-50'nin testi: *"Ç1.4'ün payı sessizce eksiltilebiliyordu. `boruda_kalan` yalnızca `ucusta`ya indirgendiğinde 284/284 test geçiyordu … 🔴 **Y8:** `kuyrukta > 0` olan bir kurulum seçildi, yoksa iki biçim ayırt edilemezdi."* |
| **ÖLÇTÜĞÜM** | Test **`kuyrukta > 0`u zorluyor ama `ucusta > 0`u zorlamıyor** — ve `ucusta`, koşu sonunda **ölçtüğüm 18 yapılandırmanın 18'inde 0**. Yani değişmez fiilen `kuyrukta == kuyrukta + 0`. **Ayna indirgeme** *(`ucusta` terimini silmek)* 367 testten **sağ çıkıyor** *(§5, `C15`, 1 329 s)*. |

**Üretici komut** *(**koşturuldu: 48,5 sn**, 18 tam koşu)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import itertools, sys; sys.path.insert(0, ".")
from sim.config import Konfig
from sim.kosucu import Kosu
from dogrulama.aktaricilar import AKTARICILAR
print("%-22s %18s %9s %7s %22s" % ("senaryo/trafik/tohum",
      "deneme-gonderilen", "kuyrukta", "ucusta", "pencere USTUNDE dogan"))
s_d = s_u = s_p = 0
for sen, tr, t in itertools.product(("S0","S2","S5"), ("orta","yogun"), (1,2,3)):
    kon = Konfig(kol="t", senaryo=sen, trafik=tr, tohum=t)
    k = Kosu(kon, AKTARICILAR["en_kisa_yol"]); s = k.kostur()
    ust = sum(1 for p in k.trafik.uretilen_paketler if p.dogum_s > kon.olcum_penceresi[1])
    d = s["mac_deneme"] - s["mac_gonderilen"]
    s_d += (d != 0); s_u += (k.defter.ucusta != 0); s_p += (ust != 0)
    print("%-22s %18d %9d %7d %22d" % ("%s/%s/t%d" % (sen, tr, t), d,
          k.defter.kuyrukta, k.defter.ucusta, ust))
print()
print("18 yapilandirmanin:")
print("  mac_deneme != mac_gonderilen olan : %d      -> B-97" % s_d)
print("  defter.ucusta != 0 olan           : %d      -> B-95" % s_u)
print("  pencere USTUNDE paket dogan       : %d      -> B-98" % s_p)
PY
```

**Beklenen / görülen:** *(18 satırın tamamı `0 … 0`; özet)*

```
18 yapilandirmanin:
  mac_deneme != mac_gonderilen olan : 0      -> B-97
  defter.ucusta != 0 olan           : 0      -> B-95
  pencere USTUNDE paket dogan       : 0      -> B-98
```

🔴 **Bu üç sıfır, ÜÇ AYRI bulgunun ortak kanıtıdır** *(B-95 · B-97 · B-98)*
ve üçü de §5'te bir sağ kalana karşılık geliyor.

**Neden önemli:** Ç1.4 kapı kriteri **iki yerde** hesaplanıyor ve **farklı
kaynaklardan**:

| yer | formül | `C15`ten etkilenir mi |
|---|---|---|
| `tests/test_kapi_aile0.py:141` | `(k.defter.kuyrukta + k.defter.ucusta) / k.defter.uretilen` — **deftere doğrudan** | ❌ hayır |
| `dogrulama/aile0_kapi_raporu.py:328` | `r["boruda_kalan"] / r["uretilen"]` — **sonuç alanından** | 🔴 **EVET** |

Yani `C15` **birim testini değil, KAPININ KENDİ Ç1.4 sayısını** eksiltir ve
kapı ölçütünü **kolaylaştırır** — B-50'nin açılış cümlesinin tarif ettiği
şeyin aynısı, ayna yönde.

⚖️ **Bir hipotezimi de burada geri alıyorum *(Y9)*.** Önce *"C15, mutasyon
paketinin kendi M1'ini görünmez yapar"* diye ölçtüm; **yanlış çıktı.**
`M1 + C15` birlikte uygulandığında `test_c1_4_bosaltma_boruyu_bosaltiyor`
yine kırıldı *(aynı değerle: `('seyrek', 0.50234375)`)*, çünkü o test
`boruda_kalan`ı **kullanmıyor**, defterden yeniden hesaplıyor. İddiayı geri
alıyorum; yerine ölçülen doğru ifade yukarıdaki tablodur.

---

### 🟠 B-96 · ORTA — Bir testin **Y8 KURULUM NÖBETÇİSİ**, testin değişmezinden önce kırılıyor; test *"ölçemiyorum"* diyor ve bu *"yakaladım"* diye puanlanıyor

| | |
|---|---|
| **Nerede** | `tests/test_kosucu.py:251` *(Y8 nöbetçisi)* vs `:254` *(asıl değişmez)* |
| **İDDİA** | B-50'nin testi Y8'i uyguluyor: *"🔴 **Y8:** `kuyrukta > 0` olan bir kurulum seçildi, yoksa iki biçim ayırt edilemezdi."* |
| **ÖLÇTÜĞÜM** | İki mekanizma mutasyonumda *(`X05` ikili üstel geri çekilme kaldırıldı · `X06` BER yarılandı)* kırılan satır **`:251`** — yani **nöbetçi**. Asıl değişmez *(`:254`)* **hiç değerlendirilmedi.** Test kelimesi kelimesine *"bu koşuda iki biçim ayırt edilemez"* diyor. |

**Üretici komut** *(geçici kopyada; ölçüldü **8,7 sn**)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import pathlib, shutil, subprocess, sys, tempfile
KOK = pathlib.Path(".").resolve()
for ad, dosya, eski, yeni in [
  ("X05 ikili ustel geri cekilme YOK", "sim/mac.py",
   "        m.cw = min(self.kon.cw_max, 2 * m.cw + 1)   # ikili ustel geri cekilme",
   "        m.cw = self.kon.cw_min                      # ikili ustel geri cekilme"),
  ("X06 BER yarilandi", "sim/radio.py",
   "        return 0.5 * math.exp(-sinr_lineer)",
   "        return 0.25 * math.exp(-sinr_lineer)")]:
    d = pathlib.Path(tempfile.mkdtemp()) / "depo"
    shutil.copytree(KOK, d, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.pyc"))
    y = d / dosya; t = y.read_text(encoding="utf-8")
    assert t.count(eski) == 1
    y.write_text(t.replace(eski, yeni, 1), encoding="utf-8")
    p = subprocess.run([sys.executable, "-m", "pytest", "tests/test_kosucu.py",
                        "-q", "-k", "b50", "--tb=short", "-p", "no:cacheprovider"],
                       cwd=d, capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    print("=== %s ===" % ad)
    for s in p.stdout.splitlines():
        if s.startswith("E ") or "test_kosucu.py:2" in s: print("  ", s.strip()[:96])
    shutil.rmtree(d.parent, ignore_errors=True)
PY
```

**Beklenen / görülen:**

```
=== X05 ikili ustel geri cekilme YOK ===
   E   AssertionError: kurulum varsayımı tutmuyor: kuyrukta=0. Bu koşuda iki biçim ayırt edilemez.
   E   assert 0 > 0
   E    +  where 0 = KorunumDefteri(uretilen=6397, teslim=3192, kuyrukta=0, ucusta=0, …).kuyrukta
=== X06 BER yarilandi ===
   E   AssertionError: kurulum varsayımı tutmuyor: kuyrukta=0. Bu koşuda iki biçim ayırt edilemez.
   E   assert 0 > 0
   E    +  where 0 = KorunumDefteri(uretilen=6397, teslim=3392, kuyrukta=0, ucusta=0, …).kuyrukta
```

---

🔴 **BİR İDDİAMI ÖLÇÜP GERİ ALIYORUM — Y9.**

İlk yazdığım şey şuydu: *"mekanizma katmanı oranım bir miktar iyimser,
çünkü iki mutasyon yanlış sebeple yakalandı."* **Bunu ölçtüm ve YANLIŞ
çıktı.** Aynı iki mutantı, **yalnızca `test_b50` dışlanmış** tam paketle
yeniden koşturdum:

**Üretici komut** *(iki mutant paralel; **koşturuldu: 18,1 dk** ve
**18,6 dk** — mutasyon adımı dâhil, kendi kendine yeterli)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import pathlib, shutil, subprocess, sys, tempfile
from multiprocessing.pool import ThreadPool
KOK = pathlib.Path(".").resolve()
YAMA = [("X05 ikili ustel geri cekilme YOK", "sim/mac.py",
         "        m.cw = min(self.kon.cw_max, 2 * m.cw + 1)   # ikili ustel geri cekilme",
         "        m.cw = self.kon.cw_min                      # ikili ustel geri cekilme"),
        ("X06 BER yarilandi", "sim/radio.py",
         "        return 0.5 * math.exp(-sinr_lineer)",
         "        return 0.25 * math.exp(-sinr_lineer)")]
def kos(is_):
    ad, dosya, eski, yeni = is_
    d = pathlib.Path(tempfile.mkdtemp()) / "depo"
    shutil.copytree(KOK, d, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.pyc"))
    y = d / dosya; t = y.read_text(encoding="utf-8")
    assert t.count(eski) == 1
    y.write_text(t.replace(eski, yeni, 1), encoding="utf-8")
    p = subprocess.run([sys.executable, "-m", "pytest", "tests", "-q",
                        "--deselect",
                        "tests/test_kosucu.py::test_b50_boruda_kalan_IKI_BILESENIN_toplami",
                        "--tb=line", "-p", "no:cacheprovider"],
                       cwd=d, capture_output=True, text=True, encoding="utf-8",
                       errors="replace")
    shutil.rmtree(d.parent, ignore_errors=True)
    return ad, [s for s in p.stdout.splitlines() if s.startswith("FAILED")], \
           [s for s in p.stdout.splitlines() if " passed" in s]
for ad, kiran, ozet in ThreadPool(2).map(kos, YAMA):
    print("=== %s ===" % ad)
    for s in kiran: print("   ", s[:96])
    for s in ozet:  print("   ", s[:96])
PY
```

**Beklenen / görülen:**

```
=== X05 ikili ustel geri cekilme YOK ===
    FAILED tests/test_kosucu.py::test_b54_en_yuksek_doluluk_BAGIMSIZ_gozlemle_ayni
    FAILED tests/test_li_regresyon.py::test_bag_kaybi_platoyu_belirgin_kaydiriyor
    FAILED tests/test_mac.py::test_cw_ikili_ustel_buyuyor - AssertionError: asser...
    FAILED tests/test_mekanizma_kapisi.py::test_b45_secim_avantaji_ATLAMA_SAYISINDAN_bagimsiz
    4 failed, 362 passed, 1 deselected in 1086.65s (0:18:06)
=== X06 BER yarilandi ===
    FAILED tests/test_li_regresyon.py::test_uzun_zincir_platosu - AssertionError:...
    FAILED tests/test_li_regresyon.py::test_bag_kaybi_platoyu_belirgin_kaydiriyor
    FAILED tests/test_radio.py::test_ber_kapali_form - assert 0.15163266492815836...
    3 failed, 363 passed, 1 deselected in 1116.59s (0:18:36)
```

⚠️ **Son satırlardaki SÜRE koşudan koşuya değişir** *(öz-denetimde yeniden
koşuldu: 17,3 dk)*; **kırılan test kümeleri iki koşuda da birebir aynı.**

⚠️ **Bu komutun ilk yayımlanan hâli KENDİ KENDİNE YETERLİ DEĞİLDİ:**
yalnızca `pytest … --deselect …` satırını veriyordu, **mutasyon adımı
yoktu**; depo kökünden olduğu gibi koşulsaydı temiz depoyu koşturur ve
**366 passed** verirdi. Öz-denetimde yakalandı ve yukarıdaki hâliyle
değiştirildi *(yeni hâli koşturuldu — sonuç birebir aynı)*.

**Özet:**

| mutant | `test_b50` dışlandığında kıran testler | sonuç |
|---|---|---|
| **X05** *(ikili üstel geri çekilme)* | `test_mac.py::test_cw_ikili_ustel_buyuyor` ← **doğrudan değişmez** · `test_kosucu.py::test_b54_en_yuksek_doluluk_…` · `test_li_regresyon.py::test_bag_kaybi_platoyu_…` · `test_mekanizma_kapisi.py::test_b45_…` **(4 failed, 362 passed)** | 🟢 **gerçekten korunuyor** |
| **X06** *(BER yarılandı)* | `test_radio.py::test_ber_kapali_form` ← **doğrudan analitik değişmez** · `test_li_regresyon.py::test_uzun_zincir_platosu` · `…test_bag_kaybi_platoyu_…` **(3 failed, 363 passed)** | 🟢 **gerçekten korunuyor** |

**İkisi de doğru sebeple, doğru testle korunuyor.** Mekanizma katmanı
oranım **iyimser değil**; `1/9` olduğu gibi duruyor. **İddia geri alındı.**

🔴 **Kalan bulgu şudur ve dardır ama gerçektir:**

1. **Teşhis yanlış yöne sapıyor.** `test_kosucu.py` alfabetik olarak
   `test_mac.py`ten önce; `-x` ile koşan biri *(ben)* **yalnızca nöbetçiyi**
   görür ve *"geri çekilme korunuyor mu"* sorusunun cevabını **göremez.**
   Bu, K-058'in *"rapor teşhisi hiç orada olmayan bir hataya saptırdı"*
   sınıfının test tarafındaki hâli.
2. **`test_b50` kırılgan bir kanaryadır:** kuyruğu boşaltan **her**
   mekanizma değişikliği onu kırar, ve kırıldığında *"ölçemiyorum"* der.
   Mutasyon oracle'ı *(`if r["sayi"]: yakalanan += 1`)* bunu **koruma**
   sayar. *(`beklenen_test` eşleşmesi etkilenmez — paket `-x` kullanmıyor
   ve tüm kırılanları topluyor.)*
3. 🔴 **Deponun `evrensel_kiricilar` koruması bunu göremez:** o, **her**
   mutantta kırılan testleri işaretliyor *(`set.intersection`)*. Yalnızca
   **bazı** mutantlarda kırılan bir nöbetçi görünmez kalır.
4. **Aynı nöbetçi, kapsamadığı yönü de göremiyor** *(**B-95**)*: `kuyrukta`
   için var, `ucusta` için yok.

⚖️ Y8'in **ayna görüntüsü**: Y8 bir testin **yanlış sebeple geçmesini**
engellemek için yazıldı; bu nöbetçi bir testin **yanlış sebeple
kırılmasına** yol açıyor.

---

### 🟠 B-97 · ORTA — Sonuç şeması **aynı sayıyı iki alanla** taşıyor: `mac_deneme` ≡ `mac_gonderilen` *(18/18)*; koruyan değişmez `x ≥ x`

| | |
|---|---|
| **Nerede** | `sim/mac.py:306` *(`toplam_deneme += 1`)* · `:375` *(`gonderilen_veri += 1`)* · `sim/kosucu.py:626, 615` · `tests/test_denetim_boslukları.py:375-390` |
| **İDDİA** | `test_s05_toplam_deneme_iletim_sayisindan_az_olamaz`: *"DEĞİŞMEZ: her veri iletimi bir geri çekilmenin ardından başlar … **Yeniden denemeler de sayıldığı için** deneme sayısı iletim sayısından AZ OLAMAZ."* |
| **ÖLÇTÜĞÜM** | Değişmez doğru ama **hiçbir zaman katı değil**: iki sayı **18/18 yapılandırmada birebir eşit** *(17 377 · 64 566 · 53 645 · 50 157 …)*. Yani `assert s["mac_deneme"] >= s["mac_gonderilen"]` fiilen **`x >= x`**. |

**Üretici komut:** B-95'inkiyle **aynı** *(ilk sütun)*.

**Yapısal sebep — koddan okundu:** `toplam_deneme` yalnızca
`_geri_cekilme_basla()`de artıyor; o fonksiyon **iki yerden** çağrılıyor:
`gonder()` *(ilk deneme)* ve `mac.py:497` *(yeniden deneme)*. Her ikisi de
**tam olarak bir** veri iletimiyle sonuçlanıyor ve `gonderilen_veri` orada
artıyor. Yani **iki sayaç aynı olayı sayıyor.**

🔴 **Sonuçları:**

1. `mac_deneme` şemada **ayrı bir alan** ve Aile 1 için doğal bir
   *"yeniden deneme maliyeti"* metriği gibi duruyor. Değil:
   `mac_deneme / mac_gonderilen` **her koşuda tam 1,000**.
2. `C18` *(alanı `gonderilen_veri`den okumak)* **367 testten sağ çıktı** ve
   çıkmak zorundaydı — mutasyon **eşdeğer**.
3. `test_s05`'in Y10 durumu: iddia **kırılamaz**. Y10 *"bir yaklaşık-eşitlik
   iddiası, KIRILABİLİR olduğu gösterilmeden yazılmaz"* diyor; burada iddia
   **katı eşitsizlik hiç görülmediği** için boş.

⚠️ *Bu bir simülatör hatası olmayabilir* — geri çekilme başına bir iletim
tasarım gereği olabilir. **Bulgu, şemanın ve testin bunu söylememesidir.**

---

### 🟠 B-98 · ORTA — Ölçüm penceresinin **ÜST SINIRI yapısal olarak ulaşılamaz**; filtre hiçbir paketi dışlayamıyor

| | |
|---|---|
| **Nerede** | `sim/kosucu.py:477-478` *(`if bas <= p.dogum_s <= bit`)* · `sim/traffic.py:113` *(üretim `olcum_bitis_s`te durur)* · `sim/config.py` *(`olcum_penceresi = (50.0, 320.0)`, `olcum_bitis_s = 320.0`)* |
| **İDDİA** | `03` Bölüm C, zorunlu altyapı sözleşmesi: *"**Ölçüm penceresi** — Isınma ayrı, ölçüm ayrı; **tüm sayaçlar aynı pencereden**."* |
| **ÖLÇTÜĞÜM** | Pencerenin **alt** sınırı gerçek *(ısınma 0–50 s dışlanıyor)*. **Üst** sınırı ise hiçbir zaman bir şey dışlamıyor: `olcum_penceresi[1] == olcum_bitis_s == 320,0` ve trafik üretimi tam orada duruyor *(`traffic.py:113` bunu `assert` ile de koruyor)*. 18 yapılandırmada **`dogum_s > bit` olan paket sayısı 0**. |

**Üretici komut:** B-95'inkiyle **aynı** *(son sütun)*, artı:

```bash
PYTHONIOENCODING=utf-8 python -c "import sys;sys.path.insert(0,'.');from sim.config import Konfig;k=Konfig(kol='t',senaryo='S2',tohum=1);print('olcum_penceresi',k.olcum_penceresi,'olcum_bitis_s',k.olcum_bitis_s,'kosu_bitis_s',k.kosu_bitis_s)"
```

**Beklenen / görülen:**

```
olcum_penceresi (50.0, 320.0) olcum_bitis_s 320.0 kosu_bitis_s 350.0
```

…ve **B-95'in 18 yapılandırmalı taramasının son sütunu** *(ayrı komut, ayrı çıktı)*:

```
  pencere USTUNDE paket dogan       : 0      -> B-98
```

`C20` *(üst sınırı silmek)* bu yüzden **367 testten sağ çıktı ve çıkmak
zorundaydı** — **eşdeğer** bir mutasyon.

🔴 **Bulgu, deponun kendi kuralının uygulanmamasıdır.** `config.py` ve
`mac.py` şunu yazıyor: *"Tetiklenemeyen bir kontrol, koruma sağlamadan
koruma izlenimi verir."* Bu gerekçeyle **üç** kontrol `assert`e çevrildi ve
her birinin yanına *"ölçüldü: N çağrının 0'ında tetiklendi"* yazıldı
*(`kosucu.py:296`, `mac.py:546`, `mac.py:666`)*. **Bu dördüncüsü, sözleşme
düzeyinde bir kontrol** ve o işlemden geçmemiş.

⚠️ **Ve gerçek bir risk taşıyor:** üst sınır bugün `olcum_bitis_s`e
**eşit**. Biri `kosu_bitis_s`e kadar üretim yapan bir trafik modeli
eklerse *(ya da `olcum_penceresi`ni daraltırsa)*, filtre **anlam kazanır**
— ama bugün hiçbir test onun çalıştığını göstermiyor, çünkü hiç
çalışmadı.

---

### 🟠 B-99 · ORTA — B-27b'nin *"her alanın içerik testi olmak zorunda"* kuralı **yalnızca `Gozlem`e** uygulanıyor; `KomsuKaydi` ve `PaketGorunumu`nun **12 alanı** kural dışında

| | |
|---|---|
| **Nerede** | `sim/gozlem.py:160-164` *(kural)* · `tests/test_gozlem.py:405-422` *(zorlayan test)* · `sim/gozlem.py:166-177` *(`IZINLI_KOMSU_ALANLARI`, `IZINLI_PAKET_ALANLARI`)* |
| **İDDİA** | `sim/gozlem.py:160`: *"**KURAL:** `IZINLI_GOZLEM_ALANLARI`ndaki her alan **ya** değerinin bağımsız hesaplanmış gerçek büyüklüğe eşit olduğunu gösteren bir teste bağlanır, **ya** aşağıda açıkça beyan edilir. **Üçüncü seçenek yoktur.**"* |
| **ÖLÇTÜĞÜM** | Kural `IZINLI_GOZLEM_ALANLARI`nın **12 alanını** kapsıyor. `IZINLI_KOMSU_ALANLARI` *(7 alan)* ve `IZINLI_PAKET_ALANLARI` *(5 alan)* için **böyle bir kural yok**: o iki küme yalnızca bir **yüzey** testinde *(alan adları eşleşiyor mu)* kullanılıyor. |

**Üretici komut** *(anlık)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import pathlib, subprocess, sys; sys.path.insert(0, ".")
from sim.gozlem import (IZINLI_GOZLEM_ALANLARI, IZINLI_KOMSU_ALANLARI,
                        IZINLI_PAKET_ALANLARI)
print("IZINLI_GOZLEM_ALANLARI : %d alan  (B-27b kurali VAR)" % len(IZINLI_GOZLEM_ALANLARI))
print("IZINLI_KOMSU_ALANLARI  : %d alan" % len(IZINLI_KOMSU_ALANLARI))
print("IZINLI_PAKET_ALANLARI  : %d alan" % len(IZINLI_PAKET_ALANLARI))
t = pathlib.Path("tests/test_gozlem.py").read_text(encoding="utf-8")
for ad in ("IZINLI_GOZLEM_ALANLARI", "IZINLI_KOMSU_ALANLARI", "IZINLI_PAKET_ALANLARI"):
    satir = [i for i, s in enumerate(t.splitlines(), 1) if ad in s]
    print("%-24s testlerde gectigi satirlar: %s" % (ad, satir))
PY
```

**Beklenen / görülen:**

```
IZINLI_GOZLEM_ALANLARI : 12 alan  (B-27b kurali VAR)
IZINLI_KOMSU_ALANLARI  : 7 alan
IZINLI_PAKET_ALANLARI  : 5 alan
IZINLI_GOZLEM_ALANLARI   testlerde gectigi satirlar: [28, 154, 155, 156, 408, 412, 415, 421]
IZINLI_KOMSU_ALANLARI    testlerde gectigi satirlar: [28, 161]
IZINLI_PAKET_ALANLARI    testlerde gectigi satirlar: [28, 162, 170, 171]
```

`IZINLI_GOZLEM_ALANLARI` **içerik kuralının** içinde *(408–421)*. Diğer
ikisinin geçtiği satırlar **yalnızca yüzey testleridir**: `:161-162`
*(`{a.name for a in dataclasses.fields(KomsuKaydi)} == set(...)`)* ve
`:170-171` *(`"dogum_s" not in IZINLI_PAKET_ALANLARI` — bir **olumsuz**
yüzey kontrolü)*. **İçerik kuralı yok.**

🔴 **MUTASYONLA SINANDI — SAĞ KALDI.** `KomsuKaydi.duyulan_beacon`ı sabit
`1` yaptım *(`kosucu.py:344`)*: **gözlem penceresi parmak izi değişti**
*(`a17d7e3a…` → `1e975317…`)* ve **367 testin 367'si geçti**
*(§5, `X04`, 1 190 s)*.

⚖️ **`08` madde 22** dokuz tüketicisiz **`Gozlem`** alanı beyan ediyor.
`duyulan_beacon` **onuncu** tüketicisiz alandır ve `KomsuKaydi` seviyesinde
olduğu için o beyanın **dışında**. `05` bu alanı *"bilginin yaşı"*
teşhisinin *(`yas_s`)* kardeşi olarak taşıyor ve Aile 1'in tazelik temelli
kolları onu okuyacak.

---

## 2. DÖRDÜNCÜ DENETİMİN BULGULARI — kapanma doğrulaması

**13 bulgunun 13'ünü de bağımsız olarak denetledim** *(promptun istediği
en az 8)*. Her birinde iki soru ayrı soruldu: **(a)** düzeltme **kodda mı**
*(Y13 — K-044/B-41'de bir düzeltme ilan edildi ve koda hiç girmemişti)*, ve
**(b)** korumanın **kapsamı dışında** kalan bir vaka üretilip reddediliyor mu
*(Y11)*.

| # | kapanış iddiası | kodda mı | kapsamı dışı vaka | sonuç |
|---|---|---|---|---|
| **B-65** | kapı eşleştirilmiş ablasyona geçti; mutlak eşik kaldırıldı | ✅ `aktaricilar.py:63-103` + `test_b65_*` ×3 | 🔴 sıraya duyarlı kol | 🟡 **KISMEN** → **B-84** |
| **B-66** | bedel tipe değil **boyuta** bağlandı | ✅ `gozlem.py:227-304` | 🔴 `float` ekseni · 🔴 öz-denetim ölü | 🟡 **KISMEN** → **B-82 · B-83**; beyanı eksik → **B-80 · B-81** |
| **B-67** | dört satır-içi değişmez | ✅ `karsilastirma.py:206-227` | 🔴 kardinalite/kapsama | 🟡 **KISMEN** → **B-85** |
| **B-68** | `teshis(dugum)` kancası; test artık enjekte etmiyor | ✅ `kosucu.py:249-274`, AST denetimi var | 🔴 sözleşme yok | 🟡 **KISMEN** → **B-87** |
| **B-69** | paylaşım **kapanış hücrelerinden** ölçülüyor; `08` beyanı düzeltildi | ✅ `test_gozlem.py:1008-1028`, `08:194` | 🔴 3/4 kanal görünmüyor | 🟡 **KISMEN** → **B-86** |
| **B-70** | `Iletim.bayt` eklendi; alıcı gerçek boyutu alıyor | ✅ `mac.py:59, 262, 290` | ölçüldü, tutuyor | 🟢 **KAPALI** |
| **B-71** | nöbetçi tekil **nesne**; harita eğriyi kapsamak zorunda | ✅ `kurulum_kalibrasyonu.py:378-403, 442-455` | dördüncü yol aranıp **bulunamadı** | 🟢 **KAPALI** |
| **B-72** | ölü dal `assert`e çevrildi | ✅ `mac.py:546-550` | 🟡 `python -O` | 🟢 **KAPALI** *(uyarı: **B-93**)* |
| **B-73** | eski koşul 3 ve testi kaldırıldı; metin ve test **aynı satırdan** | ✅ `06:402-421` + `test_b65_*` | 🔴 `06` **üç** koşul, test **iki** | 🟡 **KISMEN** → **B-92** |
| **B-74** | sıkı desenle yeniden ölçüldü: 55 · 18 · 37 | ✅ kaydın kendi komutu | sayılar **kaydı**, bugün 60 · 23 · 37 | 🟡 **KISMEN** *(§4)* |
| **B-75** | başlığa **KOD DURUMU / BAYAT** bloğu | ✅ `sag_kalan_ayikla.py:144-158` | — | 🟢 **KAPALI** |
| **B-76** | işaretleyici gövdeyi **çalışma anında** doğruluyor | ✅ `test_gozlem.py:55-79` | 🔴 proza ≠ kod | 🟡 **KISMEN** → **B-89** |
| **B-77** | `08` **madde 25** olarak beyan edildi | ✅ `08:289` | 🔴 sayıları bayat | 🟡 **KISMEN** → **B-80** |

**Bilanço: 4 tam kapalı · 9 kısmen.** Hiçbiri *"ilan edildi, koda girmedi"*
sınıfından değil — **Y13 temiz: 13/13 düzeltme kodda.** K-044/B-41'in hata
sınıfı bu oturumda **tekrarlanmamış.**

---

### B-70 · 🟢 KAPALI — ölçüldü

**Üretici komut** *(**koşturuldu: 20,2 sn**)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import sys; sys.path.insert(0, ".")
from sim.config import Konfig
from sim.kosucu import Kosu
from sim.gozlem import yuk_bayt
import sim.mac as mm
class P:
    def __init__(self, kon): pass
    def __call__(self, g): return min((k.dugum for k in g.komsular), default=None)
    def beacon_yuku(self, dugum): return {"e": 1.5, "q": 7}
gor, asil = [], mm.KanalErisimi._yayin_bitti
def izle(self, dugum, il):
    if len(gor) < 5: gor.append(il.bayt)
    return asil(self, dugum, il)
mm.KanalErisimi._yayin_bitti = izle
kon = Konfig(kol="t", senaryo="S0", tohum=1)
s = Kosu(kon, P).kostur()
mm.KanalErisimi._yayin_bitti = asil
ek = yuk_bayt({"e": 1.5, "q": 7})
print("beacon_bayt        :", kon.beacon_bayt)
print("yuk_bayt           :", ek)
print("BEKLENEN cerceve   :", kon.beacon_bayt + ek)
print("Iletim.bayt (ilk 5):", gor)
print("ESIT MI            :", all(b == kon.beacon_bayt + ek for b in gor))
print("yuk_bayt_toplam/beacon:", s["yuk_bayt_toplam"] / s["beacon_gonderilen"])
PY
```

**Beklenen / görülen:**

```
beacon_bayt        : 32
yuk_bayt           : 7
BEKLENEN cerceve   : 39
Iletim.bayt (ilk 5): [39, 39, 39, 39, 39]
ESIT MI            : True
yuk_bayt_toplam/beacon: 7.0
```

Alıcı kredisi çerçeve boyutuna **eşit** *(39 = 32 + 7)*. K-056'nın
*(42 = 32 + 10)* örneğiyle aynı mekanizma, farklı yükle doğrulandı.

🔴 **Ama `il.bayt or self.kon.beacon_bayt` satırı ayrıca sınandı** *(promptun
sorusu: *"`bayt=0` olan bir çerçeve sessizce `beacon_bayt` alır — bu bir
kaçak mı?"*)*. **Kaçak değil, ama ölü:** `Iletim.bayt` yayın yolunda her
zaman `kon.beacon_bayt + ek_bayt ≥ kon.beacon_bayt` olarak yazılıyor;
`0` olabilmesi için `beacon_bayt == 0` **ve** `ek_bayt == 0` gerekir, o
durumda da `or` dalı **aynı sayıyı** verir. Mutasyonla ayrıca ölçtüm —
**§5, C26.**

---

### B-72 · 🟢 KAPALI — dal hâlâ tetiklenmiyor

**Üretici komut** *(**koşturuldu: 2,6 sn**)*:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import sys; sys.path.insert(0, ".")
from sim.config import Konfig
from sim.kosucu import Kosu
from dogrulama.aktaricilar import en_kisa_yol
import sim.mac as mm
sayac = {"cagri": 0, "tetik": 0}
asil = mm.KanalErisimi._girisim_w
def izle(self, alici, il, an_s):
    sayac["cagri"] += 1
    for b in self.aktif:
        if (b is not il and b.gonderen == alici
                and b.baslangic_s <= an_s < b.bitis_s):
            sayac["tetik"] += 1; break
    return asil(self, alici, il, an_s)
mm.KanalErisimi._girisim_w = izle
Kosu(Konfig(kol="t", senaryo="S2", tohum=1), en_kisa_yol).kostur()
print("_girisim_w cagrisi     :", sayac["cagri"])
print("dalin tetiklendigi     :", sayac["tetik"])
PY
```

**Beklenen / görülen:**

```
_girisim_w cagrisi     : 123407
dalin tetiklendigi     : 0
```

K-056 *"246 378 çağrının 0'ı"* demişti; bağımsız ölçüm **123 407 çağrının
0'ı** *(farklı tohum/kol karışımı, aynı sonuç)*. Değişmez doğru ve dal
gerçekten tetiklenemiyor. `mac.py:666`'nın *"yukarıdaki kontrol kalkarsa
PATLAR"* iddiası da **doğrulandı**: yarı çift yönlü kontrolü devre dışı
bırakan mutasyonum *(§5, X09)* tam olarak o `assert`i patlattı.

---

### B-74 · 🟡 KISMEN — "37" tuttu, "55 · 18" bugün "60 · 23"

Kaydın **kendi üretici komutunu** olduğu gibi koşturdum:

```bash
PYTHONIOENCODING=utf-8 python - <<'PY'
import re, pathlib
t = pathlib.Path("v2/04-NEDEN-BOYLE.md").read_text(encoding="utf-8")
p = re.split(r"(?m)^# (K-\d\d\d)", t)
kay = [(p[i], p[i+1]) for i in range(1, len(p), 2)]
uret = [k for k, g in kay if re.search(r"\*\*Üretici:?\*\*", g)]
sayi = re.compile(r"%\d|\d+,\d|\b\d{3,}\b")
tas  = [k for k, g in kay if sayi.search(g)]
print("toplam kayit          :", len(kay))
print("'**Üretici:**' satiri :", len(uret))
print("sayi tasiyan          :", len(tas))
print("sayi tasiyip uretici YOK:", len([k for k in tas if k not in uret]))
PY
```

```
toplam kayit          : 60
'**Üretici:**' satiri : 23
sayi tasiyan          : 60
sayi tasiyip uretici YOK: 37
```

**37 tuttu.** Ama `README.md` bugün *"**59** kaydın 37'si"*, `04`ün kendi
dizini *"**60** karar kaydı"*, `09-DEVIR-TESLIM.md` *"**60** kaydın 37'si"*
diyor — **aynı gün yazılmış üç belgede iki farklı taban.** B-74 tam olarak
bu sınıf için açılmıştı *("30 kaydın 35'inde" aritmetik çelişkisi)*. Sayının
**payı** doğru, **paydası** üç yerde iki türlü.

---

## 3. DOĞRULANAN İDDİALAR

Yeniden ürettiğim **20 iddianın 17'si tuttu** *(aşağıdaki tablo)*. **Üçü
tutmadı** ve §4'tedir; **ikisi de sınanamadı**.
🔴 **Y6 gereği: bunların çoğu benim tezimin ALEYHİNE çıktı** — özellikle
kapının kendi null sınavı, `PYTHONHASHSEED` bağımsızlığı ve `-O` eşitliği.
Hepsini de aynen yazıyorum.

| # | iddia | kaynak | ölçtüğüm | sonuç |
|---|---|---|---|---|
| 1 | Taban temiz: **367 test geçiyor** | `README` · `09` | `367 passed in 768.56s (0:12:48)`, RC=0 | ✅ *(süre yazılı 828,3 sn'nin **%7,2 altında** — boş makine)* |
| 2 | Ucuz koruma **39 test** | K-058 | `39 passed in 20.26s` | ✅ |
| 3 | Kapı **eşleştirilmiş fark +0,0283 ± 0,0230, 8/8 pozitif** | K-056 · `06:410` | **+0,02827**, std 0,02297, **8/8**, %95 GA alt **+0,00906** → kapı **GEÇİYOR** | ✅ birebir |
| 4 | Kalıcı ablasyon null'u **+0,0599 ± 0,0232** | K-056 · `06:394` | **+0,05931 ± 0,02383** | ✅ |
| 5 | `gurultuden_kacan` **+0,0876 ± 0,0431** | K-056 · `06:393` | **+0,08758 ± 0,04307** | ✅ birebir |
| 6 | 🔴 **Kapı sıfır-bilgi kollarını REDDEDİYOR** | `06` H1.1 | **Kendi yazdığım üç null kolun ÜÇÜ de geçemedi** *(4/8 · 4/8 · 0/8)* | ✅ **kapı doğru çalışıyor** |
| 7 | Ç2 belirlenimcilik `PYTHONHASHSEED`ten bağımsız | Ç2.2 | 4 tohum değeri *(0 · 1 · 42 · random)*, **tam sonuç sözlüğü hash'i aynı**; `hash((7,(1,2,3,40)))` dördünde de **8679648302257419502** | ✅ *(kapsam uyarısı: **B-94**)* |
| 8 | K-050'nin **20 sayılık tablosu** | `04` K-050 | karar · ara% · ölü% · atlama · avantaj — **20/20 birebir** | ✅ |
| 9 | Yük bedeli kaçağı düzeltmeden sonra **1,00×** *(ad ve int ekseni)* | K-056 · B-66 | 105 943 rastgele yükte **0 kaçak** | ✅ *(float ekseni açık: **B-83**)* |
| 10 | Alıcı kredisi çerçeve boyutuna **eşit** | K-056 · B-70 | **39 = 32 + 7**, 5/5 yayında | ✅ |
| 11 | `baska.gonderen == alici` dalı **tetiklenmiyor** | K-056 · B-72 | **123 407 çağrının 0'ı** *(K-056: 246 378'in 0'ı)* | ✅ |
| 12 | Gözlem kolu kontrol payı **%1,65–1,87** | `08` madde 25 | **%1,65 · %1,82 · %1,83** *(S2)* · **%1,68 · %1,84 · %1,87** *(S0)* | ✅ birebir |
| 13 | B-57'nin sınırı: **37 kayıt** sayı taşıyıp üretici satırı taşımıyor | `09` · B-74 | **37** *(60 kaydın 23'ünde üretici var)* | ✅ *(paydası §4)* |
| 14 | İstatistik katmanı **YOK** *(`08` madde 21)* | `08:283` | `grep -rn "wilcoxon\|holm\|scipy" --include=*.py .` → **0 satır** | ✅ |
| 15 | Promptun güç tablosu *(TAM binom, tek yönlü, α=0,05, H0: p=0,70)* | denetim promptu | n=11→X≤4 · 0,533/0,274 · n=15→X≤6 · 0,610/0,304 · **n=19→X≤9 · 0,814/0,500** · n=24→X≤12 · 0,886/0,581 · n=30→X≤16 · 0,952/0,708 — **10/10 birebir** | ✅ |
| 16 | B-73: `06`'nın koşul 3'ü ve `kacan > 3·abs(nul)` testi **kaldırıldı** | K-056 | `06:402-421` ve `test_b45_*` kaynakta doğrulandı | ✅ *(sayı uyuşmazlığı: **B-92**)* |
| 17 | `python -O` sonucu değiştirmiyor | *(ölçülmemişti — ben ölçtüm)* | S2/tohum 3 tam sonuç sözlüğü blake2b: `-O` ile ve `-O`suz **`aecc804b06cfa177b8e1460b`** | ✅ *(beyan eksikliği: **B-93**)* |

⚖️ **6 numaralı satır bu denetimin kendi lehine olmayan en önemli
bulgusudur.** Promptun şüphe listesi *"kendi null'ünü yaz ve kapının onu da
sıfırda tuttuğunu sına"* diyordu. Yazdım — **kapı üçünü de reddetti.** B-45
ve B-65'te iki kez yanlış şey ölçen kapı, üçüncü hâlinde **doğru şeyi
ölçüyor.** B-84 kapının *kararını* değil, *gürültü tabanını* ve
`06`'nın *"tek fark BİLGİ"* cümlesini çürütüyor.

---

## 4. ÜRETİLEMEYEN İDDİALAR

| # | iddia | nerede | bugün ölçülen | neden |
|---|---|---|---|---|
| **1** | 🔴 kontrol payı **%14,9 – %35,6** *(DV kolu)* | `08` **madde 25** · `README` · B-77 | **%13,71 – %33,25** | **B-80** — sayı B-66 ÖNCESİ maliyet modelinden; sebebi ölçüldü ve eski modelle **birebir** üretildi |
| **2** | 🔴 iki kol arasında **14–20 kat** fark | `README` Aile 1 uyarı 2 | **8,3 – 17,8 kat** | aynı sebep |
| **3** | B-74'ün **"55 kayıt · 18 üretici"** tabanı | `aile0_audit.md` §B-74 · `README` *("59 kaydın")* | **60 kayıt · 23 üretici** | K-059 ve K-060 sonradan eklendi; `README` **59**, `09` **60**, `04` dizini **60** diyor — **üç belge, iki taban** |
| 4 | `mutasyon_paketi.py` **~25 dk** | `README` süre tablosu | ölçmedim *(kapı koşulmadı — izin verilmedi)* | ⚪ **sınanamadı** |
| 5 | Kapı **13/13**, 150,2 dk | K-059 | **koşturmadım** *(öğrenci kararı: koşturma)* | ⚪ **sınanamadı** — §A'daki denetim **kod düzeyinde** yapıldı |

🔴 **1 ve 2 aynı kökten:** B-66'nın düzeltmesi, **aynı oturumda** ölçülmüş
iki sayıyı bayatlattı ve ikisi de `08`in **mühürlenmeye hazır** sayfasında
duruyor.

⚠️ **4 ve 5 için not:** *"sınanamadı"* ile *"yanlış"* aynı şey değildir.
Kapı raporunun 13/13'ünü **koşturmadım**; §A'da yaptığım şey, kapının
sayısına değil **ona giden yola** bakmaktı — ve o yolda **B-88** ile **B-90**
çıktı.

---

## 5. 🔴 KENDİ MUTASYONLARIM — KATMANLI

**35 mutasyon**, her biri **TAM 367 testlik paketle**, geçici kopyalarda,
`Pool(6)` ile, **72,7 dk**. Taban temiz: `367 passed in 768.56s`, RC=0.

**Şartların üçü de karşılandı:**

| şart | istenen | koşulan |
|---|---|---|
| 1 · sayaç/raporlama katmanı | **≥ 19** | **26** ✅ |
| 2 · mekanizma katmanı | ≥ 8 | **9** ✅ |
| 3 · `sim/kosucu.py` | ≥ 5 | **27** ✅ |

⚠️ **`-x` kullanıldı** *(ilk kırıkta dur)*. Bu, **verdicti değiştirmez** —
"sağ kaldı / yakalandı" sorusu her iki hâlde de *"en az bir test kırılıyor
mu"*dur; yalnızca yakalananların süresini kısaltır. Sağ kalanların hepsi
paketin **tamamını** koştu *(1 189–1 368 sn)*.

---

### 🔴 KATMAN BAZINDA ORAN · %95 GA · ULAŞILAN GÜÇ

*Tek örneklem binom · tek yönlü · α = 0,05 · **TAM binom** · H0: p = 0,70 ·
GA: Clopper–Pearson*

| katman | sağ kalan | oran | %95 GA | red bölgesi | **ULAŞILAN GÜÇ** *(p₁=0,40 / 0,50)* | H0: p = 0,70 | n ≥ 19? |
|---|---|---|---|---|---|---|---|
| 🔴 **sayaç / raporlama** | **10/26** | **%38,5** | [0,202 · 0,594] | X ≤ 13 *(α′=0,0255)* | **0,892** / 0,577 | **REDDEDİLDİ** *(p = 8,5×10⁻⁴)* | **EVET** |
| **mekanizma** | **1/9** | **%11,1** | [0,003 · 0,482] | X ≤ 3 *(α′=0,0253)* | **0,483** / 0,254 | reddedildi *(p = 4,3×10⁻⁴)* | 🔴 **HAYIR** |
| 🔴 **`sim/kosucu.py`** *(4. denetimin kör noktası)* | **10/27** | **%37,0** | [0,194 · 0,576] | X ≤ 14 | **0,926** / 0,649 | reddedildi *(p = 4,0×10⁻⁴)* | **EVET** |
| **GENEL** | **11/35** | **%31,4** | [0,169 · 0,493] | X ≤ 19 | **0,970** / 0,750 | reddedildi *(p = 2,9×10⁻⁶)* | **EVET** |

🔴 **MEKANİZMA KATMANI İÇİN "KAPANDI" YAZILAMAZ** — n = 9 < 19, ulaşılan
güç **0,483**. H0 reddedildi ama o red, dördüncü denetimin **bağımsız
örneklemle sınanması** şartını *(şart 2, n ≥ 8)* karşılar; **kapanış
kararını** karşılamaz. İki denetimin mekanizma oranı birlikte
*(1/9 + 1/11 = 2/20 = %10,0)* daha güçlüdür ama iki farklı örneklemin
birleştirilmesi ön-kayıtlı değildir ve **yapmıyorum.**

**SAYAÇ KATMANI İÇİN YAZILABİLİR** — n = 26 ≥ 19, güç **0,892**.
Ve sonuç şudur: **%45,5 → %38,5.** H0 = 0,70 bu kez **reddedildi**
*(dördüncüde reddedilemiyordu)*. **Ama %95 GA hâlâ [0,202 · 0,594]** — yani
*"gerçek oran %20 ile %59 arasında"*. **Örüntü bu katmanda da KAPANMADI,
DARALDI.**

---

### 🔴 Y6 — KENDİ LEHİME ÇIKAN SONUCA KENDİ ÖLÇÜTÜMÜ UYGULUYORUM

Dördüncü denetçi %25,0'i gördüğünde ilk baktığı yer kendi örneklemiydi.
Aynısını yapıyorum. **Üç yanlılık buldum, üçü de kendi örneklemimde:**

**1 · Sayaç örneklemim DAR.** 26 sayaç mutasyonunun **22'si** tek bir
fonksiyondaki *(`kosucu.py::sonuc()`)* tek satırlık alan değişimi
*(23'üncüsü, `C21`, komşusu `yakinsama_kontrolu()`de)*. Sonuç
şemasının **kimlik/parmak izi** alanlarına *(`pencere_evren_hash` ·
`kurulum_hash` · `kaynak_hash` · `teslim_kimlikleri`)* **hiç dokunmadım** —
ve onlar şemanın **en korunanları** *(B-19/B-26/B-46 üçü de oraya yazıldı)*.
Onları da koysaydım oran muhtemelen **DÜŞERDİ**. Yani %38,5 bir **üst
tahmin** olabilir ve yanlılık **benim aleyhime değil, lehime** çalışıyor —
bu yüzden *"kapandı"* demek daha da zor.

**2 · 🔴 Üç sağ kalanım GERÇEKTEN EŞDEĞER — ve bunu Y8 ile ben yakaladım.**
`C15` · `C18` · `C20`'nin dört yapılandırmalı davranış ölçümünde
**yalnızca `kaynak_hash` değişti**. Bu, promptun uyardığı tuzağın ta
kendisiydi *("bir mutasyon, bozduğunu iddia ettiği şeyi bozmuyordu ve
'sağ kaldı' diye raporlanacaktı")*. Üçünü de **18 yapılandırmada** *(3
senaryo × 2 trafik × 3 tohum)* ayrıca sınadım — üçünün de bozduğu yol
**hiç tetiklenmiyor**. Onları **sağ kalan sayıyorum** *(dördüncü denetim
kendi eşdeğerini —U4-17— saydığı için karşılaştırılabilirlik böyle korunur)*,
ama **duyarlılık analizini de veriyorum:**

| örneklem | sağ kalan | oran | %95 GA | güç |
|---|---|---|---|---|
| sayaç, eşdeğerler **dâhil** | 10/26 | %38,5 | [0,202 · 0,594] | 0,892 |
| sayaç, eşdeğerler **hariç** | 7/23 | **%30,4** | [0,132 · 0,529] | 0,836 |
| genel, eşdeğerler hariç | 8/32 | **%25,0** | [0,115 · 0,434] | 0,954 |

**3 · 🔴 Mekanizma katmanımın 9'undan 2'si YANLIŞ SEBEPLE yakalandı.**
`X05` *(ikili üstel geri çekilme kaldırıldı)* ve `X06` *(BER yarılandı)*
tek bir testte kırıldı — ve kırılan **testin değişmezi değil, Y8 KURULUM
NÖBETÇİSİYDİ:**

```
tests\test_kosucu.py:251: assert k.defter.kuyrukta > 0, (
E   AssertionError: kurulum varsayımı tutmuyor: kuyrukta=0.
E                   Bu koşuda iki biçim ayırt edilemez.
```

Test *"bu koşuda ölçemiyorum"* diyor — ve bu **"yakaladım" diye
puanlanıyor.** Ayrıntı ve sonucu: **B-96.**

---

### Sağ kalanların DAVRANIŞI — *"eşdeğer"* ile *"tüketicisiz"* ayrı ölçüldü

Her sağ kalan, **dört ayrı yapılandırmada** *(S2/`en_kisa_yol` ·
S0/`gurultuden_kacan` · S2/`dongu_yapan` + gözlem penceresi parmak izi ·
S0/yük+teşhis taşıyan protokol)* temiz koşuyla karşılaştırıldı.

| # | mutasyon | katman | değişen | **tanı** |
|---|---|---|---|---|
| C01 | `ortanca_gecikme_s`: **ortanca → ortalama** | sayaç | 4/4 koşuda değer *(0,109 s → **2,450 s**, 22×)* | 🔴 **TÜKETİCİSİZ** |
| C05 | `islenen_olay` → 0 | sayaç | 434 571 → 0 · 3 251 265 → 0 | 🔴 **TÜKETİCİSİZ** |
| C10 | `mac_kayip_onay` → 0 | sayaç | 270 → 0 · 1 436 → 0 | 🔴 **TÜKETİCİSİZ** |
| C15 | `boruda_kalan`: `ucusta` terimi silindi | sayaç | yalnızca `kaynak_hash` | 🟡 **EŞDEĞER** *(18/18'de `ucusta = 0`)* → ama **B-95** |
| C16 | `secim_avantaji_karar` → `yonlendirme_karari` | sayaç | 7 341 → 7 342 | 🔴 **TÜKETİCİSİZ** |
| C17 | `pencerede_teslim` → `len(pencere)` | sayaç | **802 → 2 698** *(teslim = üretilen)* | 🔴 **TÜKETİCİSİZ** |
| C18 | `mac_deneme` → `mac_gonderilen` | sayaç | yalnızca `kaynak_hash` | 🟡 **EŞDEĞER** → **B-97** *(iki alan AYNI SAYI)* |
| C19 | `mac_basarisiz_alim` → 0 | sayaç | 12 020 → 0 · 15 429 → 0 | 🔴 **TÜKETİCİSİZ** |
| C20 | ölçüm penceresinin **ÜST SINIRI** silindi | sayaç | yalnızca `kaynak_hash` | 🟡 **EŞDEĞER** → **B-98** *(ulaşılamaz kontrol)* |
| C23 | 4. geçersizlik yolunun etiketi → *"mutasyon uygulanamadı"* | sayaç | *(simülatör yolu yok)* | 🔴 **TÜKETİCİSİZ** → **B-88** |
| X04 | `duyulan_beacon` sabit 1 | mekanizma | **gözlem penceresi parmak izi değişti** | 🔴 **TÜKETİCİSİZ** → **B-99** |

**Bilanço: 8 tüketicisiz · 3 eşdeğer.** Dördüncü denetimde 5 tüketicisiz +
1 eşdeğerdi. **Tüketicisiz alan sayısı arttı, çünkü örneklem sonuç şemasına
odaklandı — ve şema Aile 1'in ölçtüğü şeydir.**

🔴 **En ağır ikisi:**

- **C17** — `pencerede_teslim` *(802)* yerine `pencerede_uretilen` *(2 698)*
  yazılıyor ve **367 test görmüyor.** `teslim_orani` ayrı hesaplandığı için
  tutarsızlık **satırın kendi içinde** kalıyor; ve `sim/karsilastirma.py`
  satır içi tutarlılığı denetlemiyor *(**B-85** E3)*. İki bulgu **birbirini
  besliyor**.
- **C01** — `ortanca_gecikme_s` **ortalamaya** dönüyor ve S0'da değer
  **0,109 s → 2,450 s** *(22×)* değişiyor. `03` B3 *"üçlü sun: teslim ·
  gecikme · kontrol yükü"* diyor; gecikmenin **ortanca** biçimi, uzun
  kuyruklu dağılımda ortalamadan **taban tabana** farklıdır ve hiçbir test
  hangisinin raporlandığını doğrulamıyor.

---

### Y8 — HER MUTASYONUN BOZDUĞU YOL, MUTASYON YAZILMADAN **ÖNCE** ÖLÇÜLDÜ

**Üretici komut** *(35 mutasyon × 4 yapılandırma, `Pool(5)`, ölçüldü
**3,8 dk**)* — betikler `dogrulama/` altında değil, denetim çalışma
dizinindedir; **yöntemi** aşağıda birebir veriyorum:

Her mutasyon geçici bir depo kopyasına uygulanır, ardından **dört sabit
koşu** yapılıp tam sonuç sözlükleri ve **gözlem penceresi parmak izi**
temiz koşuyla karşılaştırılır. Kabul ölçütü: `kaynak_hash` **dışında** en
az bir alan değişmeli.

| sonuç | sayı | ne demek |
|---|---|---|
| davranış değişti *(≥1 alan, `kaynak_hash` hariç)* | **28/35** | ✅ Y8 sağlandı |
| yalnızca `kaynak_hash` değişti | **4/35** *(C15 · C18 · C20 · **C26**)* | 🔴 Y8 bu bataryada **SAĞLANMADI** — aşağıya bkz. |
| simülatörü hiç çalıştırmıyor | **1/35** *(C23)* | ⚠️ Y8 **yapısal + tarihsel**: yol `mutasyon_paketi.py:606-607`, ve kodun kendi yorumu *"İlk koşuda tam olarak bu oldu: D15"* diyor |
| mutant anında çöküyor | **2/35** *(X01 · X09)* | ✅ Y8 sağlandı — simülatörün **kendi** `RuntimeError`ı / `assert`i fırlıyor |

**Dört *"yalnızca `kaynak_hash`"* vakası ikiye ayrılıyor:**

| mutasyon | ne yapıldı | sonuç |
|---|---|---|
| `C15` · `C18` · `C20` | **18 ek yapılandırmada** sınandı *(3 senaryo × 2 trafik × 3 tohum)* — bozdukları yol **hiçbirinde tetiklenmiyor** | 🟡 **EŞDEĞER** ilan edildi *(B-95 · B-97 · B-98)* |
| `C26` *(alıcı bayt kredisi)* | 🔴 **Bataryamın kendi kör noktası.** `alinan_bayt` bir **gözlem penceresi** alanıdır ve sonuç sözlüğünde yoktur; gözlem izini ürettiğim kol *(`dongu_yapan`)* **yük taşımıyor**, dolayısıyla `il.bayt == kon.beacon_bayt` ve mutasyon o kolda **tanım gereği** görünmez | ✅ Y8 **başka yoldan sağlandı**: B-70 ölçümüm `Iletim.bayt = 39 ≠ 32` diyor, ve mutant `test_b70_alici_GERCEK_cerceve_boyutunu_kredileniyor`u **kırdı** — yol canlı |

⚖️ **Üç eşdeğerimi ben yakaladım, çünkü Y8'i mutasyondan ÖNCE koştum.**
Bu, deponun *"üç mutasyon hatalı çıktı"* sınıfının **beşinci, altıncı ve
yedinci** örneği — ve ilk kez **rapordan önce** yakalandı.

🔴 **Ama bataryamın kendisi de eksik çıktı** *(Y6, dördüncü yanlılık)*:
dört sabit koşum **gözlem penceresini yalnızca yük taşımayan bir kolla**
örnekliyor, bu yüzden `C26`nın ekseni **yapısal olarak görünmez**. Y8'i o
mutasyon için sağlayan şey bataryam değil, **onu yakalayan testtir.**

---

### Katman ataması — ölçüt ve sınır vakaları

Dördüncü denetimin ölçütü kullanıldı: mutasyon bir **mekanizmayı** mı
*(fizik · MAC durum makinesi · yönlendirme kararı · zamanlama)* yoksa bir
**sayaç/raporlama alanını** mı *(sonuç sözlüğüne giren büyüklük · gözlem
penceresi alanı · kapı ölçütü)* bozuyor?

| sınır vakası | atandığı katman | gerekçe |
|---|---|---|
| `C21` *(yakınsama eşiği 0,05 → 0,5)* | **sayaç** | ölçütün tanımı *("kapı ölçütleri")* açıkça sayar |
| `C22` *(`YUK_FLOAT_BAYT` 4 → 1)* | **sayaç** | `kontrol_bayt`/`kontrol_airtime_s` muhasebesi |
| `C23` *(kapı raporu etiketi)* | **sayaç** | raporlama; dördüncü denetim bunu *"doğrulama aracı"* diye üçüncü bir katman saymıştı — **tek mutasyonla katman kurulmaz**, sayaç/raporlamaya kattım |
| `C26` *(alıcı bayt kredisi)* | **sayaç** | `alinan_bayt` bir **gözlem penceresi alanıdır** |
| `X04` *(`duyulan_beacon`)* | **mekanizma** | komşu kaydının **durumu**; sonuç sözlüğüne girmiyor |

🔴 **`C23`ü sayaç katmanına koymak kendi lehime bir seçim DEĞİL** — o
mutasyon **sağ kaldı**, yani sayaç oranımı **yükseltiyor.** Mekanizmaya
koysaydım sayaç oranı 9/25 = %36,0'a **düşerdi.**

---

## 6. ŞÜPHE LİSTESİ SONUÇLARI

| # | soru | cevap |
|---|---|---|
| **1** | 🔴 **Sayaç katmanı — bu denetimin ASIL HEDEFİ.** Sonuç sözlüğünün her alanını boz; hangileri sabitlenebiliyor? | **26 mutasyon · 10 sağ kalan · %38,5** *(GA [0,202 · 0,594], güç **0,892**, H0=0,70 **REDDEDİLDİ**)*. Sabitlenebilen ve **hiçbir testin görmediği** alanlar: `ortanca_gecikme_s` · `islenen_olay` · `mac_kayip_onay` · `mac_basarisiz_alim` · `pencerede_teslim` · `secim_avantaji_karar`. Görünen: `kuyruk_tasmasi` · `en_yuksek_doluluk` · `donguyle_olen` · `hedef_yok` · `ttl_olumu` · `beacon_kacirilan` · `beacon_alinan` · `mac_kopya_alim` · `veri_airtime_s` · `kontrol_airtime_s` · `yuk_bayt_toplam` · `ort_komsu_sayisi` · `ortalama_atlama` · `yakinsama` eşiği · `alinan_bayt` kredisi · `YUK_FLOAT_BAYT`. → **§5** |
| **2** | 🔴 **`sim/kosucu.py` — beyan edilmiş kör nokta.** | **27 mutasyon · 10 sağ kalan · %37,0** *(güç 0,926)*. Üçüncü denetimin oranı orada **%57** *(4/7)*, dördüncüde **ölçülmemişti**. Bugün **%37,0** — düştü, ama örneklemin **en kötü katmanı** hâlâ bu. |
| **3** | **Ön-kayıtlı kapı üçüncü hâlinde — dördüncü kez yanlış olabilir mi?** Kendi null'ünü yaz. `PYTHONHASHSEED` bağımsız mı? | 🟢 **Kapının KARARI doğru.** Yazdığım **üç** sıfır-bilgi kolunun **üçünü de reddetti** *(4/8 · 4/8 · 0/8; GA'ları sıfırı içeriyor)*. `PYTHONHASHSEED` **bağımsız** *(0 · 1 · 42 · random → aynı sonuç hash'i; sebebi ölçüldü: tamsayı demeti hash'i tuzlanmıyor)*. 🔴 **AMA** ablasyon **iki ekseni** birden değiştiriyor ve `06`'nın *"tek fark BİLGİ"* cümlesi ölçümle yanlış → **B-84**; ve Ç2.2 o yolu hiç koşmuyor → **B-94**. |
| **4** | **`assert` ile yazılmış değişmezler `python -O` altında SİLİNİR.** Kaç değişmez bağlı? Kapı `-O` ile koşulsa hangileri susardı? Beyan eksikliği mi? | `sim/` altında **5** değişmez, **5'i de** `assert`. `-O` ile **beşi de** silinir; **4'ü sessiz yanlış cevap** verir, 1'i `TypeError` ile patlar. 🟢 **Bugün zararsız — ölçüldü:** `-O` ile ve `-O`suz tam sonuç sözlüğünün blake2b'si **aynı**. 🔴 **Evet, beyan eksikliği** *(`08` · `07` · kapı raporu hiçbirinde yok)* → **B-93**, `08` madde önerisi §7. |
| **5** | **Yeni kancaların sızıntı yüzeyi.** `beacon_yuku` ve `teshis` — geriye bilgi sızıyor mu? Protokol `teshis` ile yazdığını sonraki kararda okuyabilir mi? | 🟢 **Geri kanal YOK — ölçüldü.** `_protokol_teshislerini_topla()` olay döngüsünden **sonra** çağrılıyor; `protokol_teshis` yalnızca `sonuc()`ta okunuyor *(`kosucu.py` satır 227 · 242 · 245 · 248 · 273 · 573; başka okuyan yok)*. 🔴 **Ama `teshis`in SÖZLEŞMESİ yok**: 8 sözleşme dışı yükün 8'i kabul edildi, 4'ü sonuç yazıcısını düşürdü, biri `YASAK_TIPLER`den bir `Konfig` taşıdı → **B-87**. `beacon_yuku` tarafında **üçüncü kaçak ekseni var**: `float` **2,00×** → **B-83**. |
| **6** | **Kontrol düzlemi bütçesi *(B-77 / `08` madde 25)*.** Beyan edildi ama zorlanmıyor. Aile 1 bu hâliyle koşarsa karşılaştırma geçerli olur mu? | 🔴 **HAYIR — ve beyanın SAYISI da yanlış.** Zorlayan mekanizma yok; iki kol arasındaki fark bugün **8,3–17,8 kat** *(beyan: 14–20)*. Sayı **B-66 öncesi** maliyet modelinden ve `08` mühürlenmeye hazır → **B-80**. Ayrıca `08` **madde 24**, B-66 öncesi tel biçimini hâlâ beyan ediyor → **B-81**. |
| **7** | **İstatistik katmanı hâlâ YOK.** Ön-kaydın *"ZORUNLU"* dediği NaN koruması yazılmadı — ama `karsilastirma.py` NaN'ı reddediyor *(B-67)*. Bu yeterli mi? | 🟡 **Kısmen — ve sınırı ölçtüm.** `grep -rn "wilcoxon\|holm\|scipy" --include=*.py .` → **0 satır** *(madde 21 doğru)*. `karsilastirma.py` NaN'ı **gerçekten** reddediyor *(E-vakalarında ölçüldü)*. **Ama NaN koruması `wilcoxon`un döndürdüğü NaN için değil, GİRDİ için**: `03` B2'nin uyardığı şey *"tüm farklar sıfırken `wilcoxon` **hata fırlatmaz, NaN döndürür**"*. O boru **hiç yok**, dolayısıyla o NaN **hiç korunmuyor**. `karsilastirma.py`nin koruması **farklı bir NaN'ı** yakalıyor. Yeterli **değil**; madde 21 yerinde duruyor. |
| **8** | **`08`in 25 maddesi — iki yönlü.** *(a)* *"Yapmaz"* denen bir şey yapılıyor mu? *(b)* Kodda modellenmemiş ama listede olmayan? | *(a)* 🔴 **Evet, biri:** madde 24 *"alan kimliği 1 B · int/float 4 B"* diyor; kod **UTF-8 uzunluğu** ve **büyüklük** kullanıyor, ve **yön iddiası ters** → **B-81**. *(b)* 🔴 **Evet, dördü:** `python -O` altında değişmezlerin silinmesi *(**B-93**)* · `teshis`in sözleşmesiz olması *(**B-87**)* · `float` bedelinin taşınan bilgiden **2×** küçük olması *(**B-83**)* · **yayılma gecikmesi** — dördüncü denetimin **kendi önerdiği** madde ve `08`e hiç girmemiş *(**B-91**)*. → §7'de dört madde önerisi. |
| **9** | 🔴 **B-57 hâlâ açık.** 37'nin kaçının sayısı bugün yeniden üretilebilir? | **Sayı doğrulandı: 60 kayıt · 23 üreticili · 37 eksik.** Üreticisiz bir kaydın *(K-050)* **20 sayılık tam tablosunu** bugünkü kodla **birebir** ürettim — konfigürasyonu **tahmin ederek** *(S2/orta/tohum 1, ilk denemede tuttu)*. 🔴 **Asıl bulgu ters yönde:** üretici satırı **TAŞIYAN** bir sayı *(`08` madde 25, B-77)* **yeniden üretilemedi**. Yani B-57'nin ilacı *(satır eklemek)* **yetmiyor**; eksik olan **yeniden koşudur** → **B-80**. |
| **10** | **Dört denetimin kapanışları birbirini bozdu mu? Bu oturumun 13 düzeltmesinden hangisi bir sonrakini doğuruyor?** | 🔴 **13'ün 8'i.** B-66 → **B-80 · B-81 · B-82 · B-83** *(dördü birden)* · B-65 → **B-84** · B-67 → **B-85** · B-68 → **B-87** · B-69 → **B-86** · B-73 → **B-92** · B-76 → **B-89** · B-77 → **B-80** *(madde 25'in sayıları; B-80'in iki ebeveyni var)*. Ayrıca **K-058'in kendi düzeltmesi** → **B-88** *(dördüncü geçersizlik yolu)* ve **B-90** *(çekişme çarpanı)*. Örüntü **dördüncü kez** tekrarlandı. |
| **11** | **Bu promptun kendisi.** Neye bakmanı istemiyor olabilir? Listede olmayan bir yere bak. | Aşağıda. |

---

### 11 · 🔴 PROMPTUN GÖSTERMEDİĞİ YER — ve orada bulduklarım

Prompt beni **sonuç şemasına** ve **`sim/kosucu.py`ye** yönlendirdi; ikisi
de haklıydı ve ikisi de sonuç verdi. **Bakmamı istemediği üç yer vardı:**

**(a) 🔴 TESTLERİN KENDİSİ — özellikle Y8 nöbetçileri.** Prompt Y8'i
*"benim mutasyonlarım için"* bir şart olarak yazdı; **deponun kendi
testlerindeki** Y8 nöbetçilerine hiç bakmamı istemedi. Baktım:
`test_b50`'nin Y8 nöbetçisi iki mekanizma mutasyonunu **testin
değişmezinden önce** kırıyor ve bu *"yakalandı"* diye puanlanıyor
*(**B-96**)*; aynı testin nöbetçisi indirgemenin **ayna yönünü** göremiyor
*(**B-95**)*.

**(b) 🔴 `dogrulama/` DIŞINDAKİ RAPORLAMA KATMANI.** Prompt §A'da
zaman aşımını ve sebep üreticilerini işaret etti — ikisi de **sağlam** çıktı
*(9 `test_b79_*` testinin hepsi gerçek koruma)*. Ama **onların yanındaki
dördüncü yol** listede yoktu: `mutasyon_paketi.py:606-607`. Orası
K-058'in kapattığı hatanın **birebir aynısını** taşıyor ve mutasyonla
**sağ kaldı** *(**B-88**)*.

**(c) 🔴 KAPSAM BELGESİNİN KENDİSİ — mühürlenmeden önce.** Prompt `08`in
25 maddesini *"iki yönlü"* denetlememi istedi ama **maddelerin sayılarının
bayat olabileceğini** sormadı. İki madde bugün yanlış *(**B-80 · B-81**)* ve
ikisi de **aynı oturumun kendi düzeltmesinden** bayatladı. `08` **B-57
kapanınca mühürlenecek** — yani bu iki yanlış sayı, **mührün içine
girecekti.**

⚖️ **Ve bir şey aradım, BULAMADIM** *(negatif sonuç, Y6 gereği yazılıyor)*:
- `Gozlem`den simülatöre **geri referans** aradım — `teshis`, `beacon_yuku`
  ve kapanış hücreleri üzerinden. **Yok.** Kancaların ikisi de tek yönlü.
- `protokol_teshis`in **karar anında okunabildiği** bir yol aradım. **Yok.**
- `kalite_ablasyonu`nun kapıyı **yanlış geçirdiği** bir sıfır-bilgi kolu
  aradım. **Bulamadım** — üç denemem de reddedildi.
- `yeni_olcut`un ulaşılabilirlik kısıtını atlayan **dördüncü bir yol**
  aradım *(B-71)*. **Yok** — nöbetçi tekil nesne ve `yeni_olcut` çalışma
  noktasını seçen **tek** yer *(tek çağrı yeri: `kurulum_kalibrasyonu.py:574`)*.

---

## 7. KAPSAM BEYANINA EKLENECEKLER — `08` madde 26…30

🔴 **Önce bir DÜZELTME, sonra beş EKLEME.** `08` **B-57 kapanınca
mühürlenecek**; aşağıdakiler mühürden önce girmeli.

### 🔴 ÖNCE: madde 24 ve madde 25 BUGÜN YANLIŞ

| madde | yazılı | doğrusu *(ölçüldü)* |
|---|---|---|
| **24** | *"alan kimliği **1 B** · bool 1 B · int/float **4 B** · sayı demeti **4 B × eleman**"* · yön: *"maliyeti gerçeğe göre **AZ** gösterir"* | alan kimliği **UTF-8 bayt uzunluğu** · bool 1 B · `int` **max(1, ⌈bit/8⌉)** · float 4 B · demet **elemanların toplamı**. Yön: **ad** ekseninde **FAZLA**, **float** ekseninde **AZ** *(2,00×)* → **B-81 · B-83** |
| **25** | kontrol payı *"**%14,9–35,6** vs %1,65–1,87 — **14–20 kat**"* | **%13,71–33,25** vs %1,65–1,87 — **8,3–17,8 kat** → **B-80** |

### SONRA: beş yeni madde

| # | eklenecek madde | yön ve büyüklük *(ölçüldü)* |
|---|---|---|
| **26** | 🔴 **Yayılma gecikmesi modellenmiyor.** *(Dördüncü denetimin önerdiği madde; `08`e hiç girmedi ve elenmesi de kayda geçmedi — **B-91**.)* | 280 m'de **0,93 µs**, girişim menzilinde **2,01 µs**; `cca_s = 4 µs`in **%23–50'si**. Yön: çarpışma zamanlamasını gerçeğe göre **keskinleştirir** *(dördüncü denetimin ölçümü; bağımsız olarak yeniden ölçmedim)* |
| **27** | 🔴 **`sim/` içindeki beş değişmez `assert` ile yazılmıştır ve `python -O` altında SESSİZCE kalkar.** *(`events.py:71` · `traffic.py:113` · `kosucu.py:296` · `mac.py:546` · `mac.py:666`)* | Ölçüldü: `-O` ile ve `-O`suz tam sonuç sözlüğü **birebir aynı** *(`aecc804b06cfa177b8e1460b`)* — bugün zararsız. Ama **4'ü** kalktığında **sessiz yanlış cevap** verir *(zaman geriye gider · pencere dışı paket ölçüme girer · alıcı kendi gücünü girişim sayar)*, 1'i `TypeError` ile patlar. 🔒 **Her ölçüm koşusu `-O`suz yapılır; kapı raporu bunu beyan etmeli** → **B-93** |
| **28** | 🔴 **`protokol.teshis(dugum)` kancasının hiçbir sözleşmesi yoktur.** Anahtar tipi, değer tipi, boyut ve serileştirilebilirlik denetlenmiyor. | Ölçüldü: 8 sözleşme dışı yükün **8'i** kabul edildi; **4'ü** `SonucYazici`yı **koşu bittikten sonra** ham `TypeError`/`ValueError` ile düşürdü; biri **`YASAK_TIPLER`den bir `Konfig`** taşıdı. Kardeşi `beacon_yuku` **anında** ve **tipli** *(`YukHatasi`)* reddediyor. Yön: sonuç şeması **doğrulanmamış** veri taşıyabilir → **B-87** |
| **29** | 🔴 **Beacon yükünde `float`, taşıdığı bilginin YARISINA faturalanır.** Tel biçimi `float` = 4 B, ama gözlem penceresine **çift duyarlıklı (8 B) hâliyle kırpılmadan** giriyor. | Ölçüldü: 8 keyfi bayt bir `float`a konup **birebir** geri okundu, bedel **4 B**. Aynı 8 bayt `int` olarak **8 B** ödüyor → **aynı bilgi, iki kodlama, 2,00× fiyat farkı**. Sınırlı *(≤2×; B-66'nın kapattığı eksenler sınırsızdı)* ama K-009'un *"eşit kontrol düzlemi bütçesi"* şartını **kodlamaya bağımlı** kılıyor → **B-83** |
| **30** | 🔴 **Sonuç şeması aynı büyüklüğü iki alanla taşıyor:** `mac_deneme` ≡ `mac_gonderilen`. | Ölçüldü: **18/18 yapılandırmada birebir eşit** *(3 senaryo × 2 trafik × 3 tohum)*. `mac_deneme / mac_gonderilen` her koşuda **tam 1,000**; *"yeniden deneme maliyeti"* diye okunamaz. Koruyan değişmez `assert mac_deneme >= mac_gonderilen` fiilen **`x ≥ x`** → **B-97** |

⚠️ **Ayrıca `08` madde 22'ye bir satır:** tüketicisiz alan sayısı **dokuz
değil, en az on** — `KomsuKaydi.duyulan_beacon` onuncusudur ve `Gozlem`
seviyesinde olmadığı için mevcut beyanın **dışında** kalıyor *(**B-99**)*.

---

## 8. 🔴 ANLAŞILMAYANLAR

Aşağıdaki altısı **bulgu değildir**: cevabını ölçemediğim ya da *"bilinçli
tasarım mı, fark edilmemiş mi"* ayrımını yapamadığım şeyler. Üç denetimde
bu bölümden gerçek kusur çıktı *(üçüncüde A-4 buradan geldi ve bir kâhin
kanalıydı)*.

**A-5 · `kalite_ablasyonu`nun permütasyonu TOHUMDAN bağımsız.**
`anahtar = (dugum, komşu demeti)` — **`kon.tohum` yok.** Yani aynı topoloji
ve aynı komşu kümesi, **hangi tohumda olursa olsun aynı permütasyonu** alır.
Bugün zararsız *(farklı tohum → farklı topoloji → farklı anahtar)*, ama iki
sonucu var ve hangisinin kastedildiğini **belirleyemedim**:
*(1)* Ablasyonun **kendi varyansı ölçülemiyor** — aynı tohumda ikinci bir
bağımsız null çekilemez, çünkü sarmalayıcının tohum/tuz parametresi yok.
Kapının %95 GA'sı **yalnızca tohumlar arası** varyansı taşıyor; ablasyon
çekiminin varyansı **hiç yok sayılıyor.**
*(2)* `03` Bölüm C *"Ayrık RNG akışları — her rastgelelik kaynağı kendi
akışını kullanır"* diyor; bu akış `Akislar` dışında, `random.Random` ile
kuruluyor. `dogrulama/` altında olduğu için kapsam dışı sayılmış olabilir —
ama **ön-kayıtlı kapının null modelidir.** Bilinçli mi, fark edilmemiş mi
bilmiyorum.

**A-6 · `il.bayt or self.kon.beacon_bayt` — `or` neden orada?**
`Iletim.bayt` yayın yolunda her zaman `kon.beacon_bayt + ek_bayt` yazılıyor,
yani `0` olabilmesi için `beacon_bayt == 0` **ve** `ek_bayt == 0` gerekir —
o durumda da `or` dalı **aynı sayıyı** verir. Yani dal **hiçbir girdide
farklı sonuç vermiyor.** Deponun deseni böyle dalları `assert`e çeviriyor
*(B-13 sınıfı, üç örnek)*; bu dördüncüsü çevrilmemiş. **Savunmacı bir
alışkanlık mı, `Iletim.bayt: int = 0` varsayılanına karşı bilinçli bir
kalkan mı** — belirleyemedim. *(Mutasyonla ölçtüm: `or` dalını tamamen
kaldıran `C26` **yakalanıyor**, yani `il.bayt` tarafı korunuyor.)*

**A-7 · Ölçüm penceresi iki ucunda FARKLI kapalılıkta.**
`sonuc()`: `bas <= p.dogum_s <= bit` *(iki uç da kapalı)*.
`yakinsama_kontrolu()`: `a <= p.dogum_s < b` *(sağ uç açık)*. Yani tam
`bit` anında doğan bir paket **pencereye girer ama hiçbir yakınsama
dilimine girmez**. Bugün ölçülemez *(**B-98**: `dogum_s > bit` olan paket
yok; `== bit` olanı da kayan noktada göremedim)*. **Bilinçli bir sınır
seçimi mi, iki ayrı yerde yazılmış iki ayrı alışkanlık mı** — belirleyemedim.

**A-8 · `sonuc()` içindeki `"topoloji"` ve `"trafik"` alt sözlükleri.**
Şema *"Aile 1 başladıktan sonra değiştirilemez"* ilan edildi *(B-19'un
dersi)*. Ama bu iki alan **iç içe sözlük** ve içeriklerini üreten
`topo.ozet()` / `trafik.ozet()`in **kendi** alanları hiçbir yerde
listelenmiyor — `IZINLI_*` kümelerinin karşılığı yok. **Bu iki alanın
şeması donmuş sayılıyor mu?** Hiçbir mutasyon koymadım *(örneklem
yanlılığım, §5'te yazılı)* ve belgede cevabını bulamadım.

**A-9 · `mutasyon_paketi.py:344`'teki `"ERROR" in p.stdout`.**
`--tb=no -q` ile koşan bir pytest, **her başarısız `assert` için** kısa
özet satırında `AssertionError` basar — içinde `"ERROR"` geçer. Yani bu
koşul, testleri kıran **her** mutantta `True`. Bugün zarar vermiyor, çünkü
ikinci koşul `not r["sayi"]` onu bastırıyor. **Alt dizgi araması bilinçli
bir ucuzluk mu, `ERROR` başlıklı pytest bölümünü hedefleyen ama yan etkisi
görülmemiş bir kontrol mü** — belirleyemedim. *(Etiketi ayrıca bir bulgu:
**B-88**.)*

**A-10 · `_gereken_zaman_asimi_s` süreyi test SAYISIYLA doğrusal ölçekliyor.**
Formül `PAKET_SURESI_S × (guncel / PAKET_TEST_SAYISI) × …`. Ama testler
**eşit maliyetli değil**: `test_b65_mekanizma_kapisi_ESLESTIRILMIS_…`
docstring'ine göre **16 tam koşu (~2 dk)** yapıyor, ortalama test ise
~2,3 sn. Yani **tek bir kapı testi eklemek**, korumanın öngördüğünden
~50 kat fazla süre ekleyebilir. **Doğrusal modelin bilinçli bir
basitleştirme mi olduğunu** *(ve emniyet payının bunu karşılamak için mi
konduğunu)* belirleyemedim; ölçmek için `--durations` ile tam bir koşu
gerekirdi ve bütçeye sığmadı.

---

## 9. KOŞTURDUĞUM KOMUTLAR

Hepsi **depo kökünden**, `PYTHONIOENCODING=utf-8` ile, **Windows 11 ·
Python 3.11.8 · numpy 1.26.4 · scipy 1.17.1 · pytest 8.2.2**, en fazla
**6 çekirdek** kullanılarak koşuldu. **Yayımladığım her üretici komut,
yayımlanmadan önce OLDUĞU GİBİ koşturuldu** — biri *(B-89)* ilk yazımında
çalışmadı *(`inspect.getsource` stdin'den okuyamıyor)*, düzeltilip yeniden
koşuldu ve **düzeltilmiş hâli** yayımlandı.

🔴 **26 Ağustos'ta bu bölümün kendisi denetlendi:** raporda yayımlanan
**26 `bash` bloğunun tamamı** metinden çıkarılıp yeniden koşuldu, ve her
*"Beklenen / görülen"* satırı gerçek `stdout`ta arandı. **On altı kusur
bulundu ve düzeltildi** — biri, üretici komutu **kendi sonucunu üretmeyen**
bir bulguydu *(B-96)*. Ayrıntı: **§10.**

| # | komut | süre | sonuç |
|---|---|---|---|
| 1 | `python -m pytest tests -q --collect-only` | 0,3 sn | **367 tests collected** |
| 2 | `python -m pytest tests -q` *(geçici kopyada, boş makine)* | **12,8 dk** | **367 passed in 768.56s**, RC=0 — **taban temiz** |
| 3 | `python -m pytest tests/test_kapi_secimleri.py -q` | 20,3 sn | **39 passed** |
| 4 | 🔴 **35 mutasyonluk kampanya** *(her biri TAM paketle, `Pool(6)`, geçici kopyalar, `-x`)* | **72,7 dk** | **11 sağ kalan / 35** — §5 |
| 5 | **Y8 ön ölçümü** *(35 mutasyon × 4 yapılandırma, `Pool(5)`)* | 3,8 dk | 30 tetiklendi · **3 tetiklenmedi** *(C15 · C18 · C20)* · 1 çökme · 1 yapısal |
| 6 | Kapı null sınavı: `gurultuden_kacan` + **3 kendi null kolum** × 8 tohum | 22 dk | kapı **GEÇTİ** *(8/8)*, üç null **REDDEDİLDİ** — §3-6 |
| 7 | Ablasyonun **ikinci ekseni** *(34 tam koşu)* | 10,0 dk | %92,8 sırasız · sıralama artefaktı **birebir** — **B-84** |
| 8 | B-77 yeniden üretimi *(12 koşu)* | 2,1 dk | kontrol payı **tutmadı** — **B-80** |
| 9 | B-77, **B-66 ÖNCESİ** maliyet modeliyle *(geçici kopya, 12 koşu)* | 2,3 dk | **%26,04 · %35,63 · %14,88 · %25,41** — yazılı sayının kendisi |
| 10 | `yuk_bayt` fuzz'u *(200 000 rastgele yük)* | 2,0 sn | 105 943 kabul · **0 kaçak** · Y7 dalı **0 kez ateşlenebilir** — **B-82** |
| 11 | `ortak_alt_kume` beşinci eksen *(5 bozuk satır)* | 8,0 sn | **5/5 kabul**, biri **%328,5 kesişim** — **B-85** |
| 12 | Kapanış hücresi taraması *(4 kanal tipi, 4 tam koşu)* | 1,7 dk | **3/4 görünmüyor**, biri **çöküyor** — **B-86** |
| 13 | `teshis` sözleşmesi *(8 sözleşme dışı yük, 16 tam koşu)* | 4,0 dk | **8/8 kabul**, **4/8** yazıcıyı düşürdü — **B-87** |
| 14 | `PYTHONHASHSEED` = 0 · 1 · 42 · random *(ablasyon kolu, 12 koşu)* | 2,7 dk | **dört tohumda da aynı sonuç hash'i** — §3-7 |
| 15 | `python -O` vs `python` tam sonuç sözlüğü | 44 sn | **`aecc804b06cfa177b8e1460b`** — ikisi de aynı |
| 16 | 18 yapılandırma taraması *(3 senaryo × 2 trafik × 3 tohum)* | 48,5 sn | üç sıfır: **B-95 · B-97 · B-98** |
| 17 | K-050'nin tam tablosu *(4 kol)* | 1,4 dk | **20/20 birebir** |
| 18 | B-74'ün kendi tarama komutu | anlık | **60 · 23 · 60 · 37** |
| 19 | B-70 *(alıcı kredisi)* · B-72 *(ölü dal)* | 20,2 sn · 2,6 sn | **39 = 32+7** · **123 407 çağrının 0'ı** |
| 20 | B-96 *(nöbetçi)* + `--deselect` ile iki tam paket | 8,7 sn + 13,3/13,6 dk | nöbetçi doğrulandı · **iddia geri alındı** |
| 21 | `M1` ve `M1 + C15` *(Ç1.4 hipotezi)* | 3,4 sn | **hipotez çürüdü** — §B-95 |
| 22 | B-81 · B-83 · B-88 · B-89 · B-90 · B-91 · B-92 · B-93 · B-99 | hepsi < 1 dk | §1 |

🔴 **KOŞTURMADIĞIM:** `python dogrulama/aile0_kapi_raporu.py` *(~150 dk)*.
Öğrenci *"koşturma"* dedi; §A'nın 13/13 denetimi bu yüzden **kod
düzeyinde** yapıldı — ve o yolda **B-88** *(kapının dördüncü geçersizlik
yolu)* ile **B-90** *(çekişme çarpanı)* çıktı.
Ayrıca `mutasyon_on_kontrol.py`, `sag_kalan_ayikla.py`, `kor_mutasyon.py`
ve `kurulum_kalibrasyonu.py` **koşturulmadı** — bütçe 35 mutasyona ayrıldı.

---

---

## 10. 🔴 ÖZ-DENETİM — bu raporun kendisi denetlendi *(26 Ağustos 2026)*

Rapor yazıldıktan sonra, **öğrencinin talebiyle**, bu denetimin kendisi aynı
ölçütlerle denetlendi. Yöntem, rapora uygulanan yöntemin aynısıdır:

| ne yapıldı | nasıl |
|---|---|
| **Sayımlar ham veriye karşı** yeniden hesaplandı | `mut_kayit.jsonl`den katman/sağ kalan/süre tabloları yeniden türetildi |
| **İstatistik BAĞIMSIZ yoldan** yeniden hesaplandı | `scipy.stats.binomtest` + `proportion_ci(method="exact")` — kendi `istatistik.py`m **kullanılmadı** |
| **Yayımlanan `bash` bloklarının tamamı** rapordan **çıkarılıp** yeniden koşuldu *(25 → düzeltmeden sonra 26)* | `aile0_audit.md`den regex ile alındı, Git Bash ile koşuldu |
| **Her "Beklenen / görülen" satırı** gerçek `stdout`ta aranıp bulundu | otomatik karşılaştırıcı |
| **67 `dosya:satır` atfının** hepsi açıldı ve içeriği okundu | 67/67 çözüldü, hiçbiri kırık değil |
| **Önceki dört raporun metni** bayt bayt karşılaştırıldı | **256 040 karakter birebir aynı** |

---

### 🔴 ON ALTI KUSUR BULUNDU VE DÜZELTİLDİ

**Hiçbiri bir bulgunun özünü, bir sağ kalan oranını ya da bir istatistiği
değiştirmiyor.** Yedisi **aritmetik/sayım**, yedisi **"birebir çıktı"
disiplini**, ikisi **yöntemsel** *(12 ve 13)*.

| # | kusur | eski | yeni |
|---|---|---|---|
| 1 | `sonuc()` içindeki sayaç mutasyonu sayısı | 21 | **22** *(23'üncüsü `C21`, `yakinsama_kontrolu()`de)* |
| 2 | Yeniden üretilen iddia sayısı *(3 yerde)* | *"17 iddiadan 14'ü"* | **"20 iddiadan 17'si"** — §3'te **17 satır ve 17'si ✅**, §4'te **3 tutmayan** |
| 3 | Bir sonraki bulguyu doğuran kapanış *(3 yerde)* | 13'ün **7'si** | 13'ün **8'i** — **B-77 → B-80** atlanmıştı *(§2 tablosu onu zaten yazıyordu; §6-10 yazmıyordu)* |
| 4 | `test_b79_*` test sayısı *(4 yerde)* | **13** | **9** *(K-058'in "13 yeni koruma"sı = `test_b78_*` ×4 + `test_b79_*` ×9)* |
| 5 | İşaretli test sayısı *(B-89)* | 11'in 11'i | **9'un 9'u** *(`icerik_testi` 11 yerde; ikisi `test_b76_*`in iç içe kontrolleri)* |
| 6 | Atıf *(B-99)* | `kosucu.py:341` | **`kosucu.py:344`** *(mutasyonun fiilen uygulandığı satır)* |
| 7 | 🔴 **Y8 künye tablosu** | 30 / 3 / 1 / **1** | **28 / 4 / 1 / 2** — `X09` çöken sayılmamış, **`C26` "yalnızca `kaynak_hash`" sayılmamıştı** |
| 8 | B-84'ün beklenen çıktısı | `3) sira_kolu` · `std=0.02297` | **`2) sira_kolu`** · **`std=0.02298`** *(komut ikinci başlığı da `2)` basıyor)* |
| 9 | B-83 · B-88 · B-91 · B-92'nin beklenen blokları | **açıklama eklenmiş / kısaltılmış** *(ör. `<- desen`, `…`)* | **birebir `stdout`** |
| 10 | B-86'nın beklenen çıktısı | eski betiğin sınıf adı `_SinifTabanliProtokol` | **`SinifP`** *(yayımlanan komutun ürettiği ad)* |
| 11 | B-93 · B-98'in tek `` ``` `` bloğu | **üç/iki ayrı komutun çıktısı tek fence'te** | komut başına ayrı fence, etiketli |
| 12 | 🔴 **B-96'nın üretici komutu** | `pytest … --deselect …` — **mutasyon adımı YOK**; depo kökünden olduğu gibi koşulsaydı temiz depoyu koşup **366 passed** verirdi | **kendi kendine yeterli hâle** getirildi *(kopya → yama → koşu)* ve **koşturuldu**: sonuç **birebir aynı** *(X05 4 failed/362 passed · X06 3 failed/363 passed)* |
| 13 | 🔴 **B-80'in İKİNCİ çıktı bloğu** *(B-66 öncesi maliyet modeliyle koşu)* | **üretici komutu YOKTU** — sayılar bir `` ``` `` bloğundaydı, onları üreten komut yayımlanmamıştı | komut yazıldı *(geçici kopya → yama → koşu)* ve **koşturuldu: 9,7 sn**; çıktı **birebir aynı** |
| 14 | B-87'nin beklenen bloğu | sütun genişlikleri elle düzeltilmiş, satırlar `…` ile kırpılmış | **birebir `stdout`** |
| 15 | B-94'ün beklenen bloğu | elle biçimlendirilmiş *(`{…ayni uc hash…}`)* | **birebir `stdout`** + `hash_dizgi`nin **her koşuda değiştiği** notu |
| 16 | B-96'nın özet satırındaki süre | sabit gibi sunuluyordu | **koşudan koşuya değişir** notu eklendi *(kırılan test kümeleri iki koşuda da aynı)* |

---

### ⚖️ 7 · 12 · 13 NUMARALI KUSURLAR NEDEN ÖNEMLİ

**7 — Y8 künyesi.** Bataryamın `C26`yı göremediğini **rapor yazılırken fark
etmemiştim**. Sebebi ölçüldü: `alinan_bayt` bir **gözlem penceresi** alanı,
sonuç sözlüğünde yok; gözlem izini ürettiğim kol *(`dongu_yapan`)* **yük
taşımıyor**, dolayısıyla `il.bayt == kon.beacon_bayt` ve mutasyon o kolda
**tanım gereği** görünmez. `C26` için Y8'i sağlayan şey bataryam değil,
**onu yakalayan testtir**. Bu, raporun kendi §5'inde *"Y6 · dördüncü
yanlılık"* olarak yazıldı.

🔴 **12 — kendi kendine yetmeyen üretici komut.** Bu, raporun **B-80'de
başkasında bulduğu kusurun aynısıdır**: *"bir sayının üretici satırı
olması, o sayının yeniden üretilebildiğini göstermez."* B-96'nın komutu
vardı ve **kendi sonucunu üretmiyordu.** Öz-denetim olmasaydı, jüri
karşısında koşulduğunda **"366 passed"** verecekti.

🔴 **13 — üretici komutu OLMAYAN bir çıktı bloğu.** B-80'in kendi bulgusu *"sayının üretici satırı var ama yeniden üretilemiyor"* idi; B-80'in **ikinci** sayı bloğunun ise **hiç komutu yoktu**. Bugün var, koşuyor ve aynı sayıları veriyor.

⚖️ **Ders, raporun kendi diline yazılıyor:** *"yayımladığın her üretici
komutu, yayımlamadan önce olduğu gibi koştur"* **yetmiyor** — komutun
**hangi dizinde ve hangi durumda** koşulduğunu da yayımlamak gerekiyor.
B-96'nın komutu **koşturulmuştu**, ama mutasyonlu bir kopyada; yayımlanan
metin o bağlamı taşımıyordu.

---

### Öz-denetimde DEĞİŞMEYENLER

| ne | sonuç |
|---|---|
| Katman oranları *(10/26 · 1/9 · 10/27 · 11/35)* | ham kayıttan **birebir** yeniden türetildi |
| %95 GA'lar *(Clopper–Pearson, iki yönlü)* | `scipy.binomtest` ile **birebir**; tek yönlü aralıkla karıştırılmadığı doğrulandı |
| Ulaşılan güçler *(0,892 · 0,483 · 0,926 · 0,970)* | **birebir** |
| Promptun güç tablosu *(10 hücre)* | **birebir** |
| 20 bulgunun **hiçbiri** | geri alınmadı, hiçbirinin şiddeti değişmedi |
| Önceki dört denetimin metni | **256 040 karakter birebir aynı** |
| `sim/` kaynak hash'i | denetimin başındaki ile **aynı**: `c5cdb9940ca599ef7939bf8595b89236` |
| Tohum uyumu | `sim/`+`tests/`+`dogrulama/` tarandı: **2000–2029 hiçbir yerde koşulmuyor**; benim kullandıklarım **1–8** |

🔴 **Ve öz-denetimin kendi sınırı:** bu tur **kapı raporunu koşturmadı**
*(~150 dk)* ve **35 mutasyonu yeniden koşturmadı** *(72,7 dk)*. Yeniden
koşulan şey **yayımlanan komutlar** ve **yayımlanan sayılar**dır; mutasyon
kampanyasının kendisi **ham kaydından** doğrulandı.

---

## 🔴 SON SÖZ — beşinci denetçiden

Dört denetim, dört kez bulgu: **20 → 17 → 24 → 13.** Beşincisi **20**.

Örüntü **beşinci kez de kapanmadı.** Ama bu kez ilk defa **doğru katmanda
ve yeterli güçte** ölçüldü, ve söylenebilecek şey şu:

- **Sayaç / raporlama katmanı** *(n = 26, güç 0,892)*: H0 = 0,70 **artık
  reddediliyor** — dördüncü denetimde n = 11'de güç 0,533'tü ve
  reddedilemiyordu. Oran **%45,5 → %38,5**. **Daraldı. Kapanmadı**
  *(%95 GA [0,202 · 0,594])*.
- **`sim/kosucu.py`** — dördüncü denetçinin **kendi beyan ettiği kör
  noktası** — ilk kez yeterli güçle ölçüldü *(n = 27, güç 0,926)* ve
  **örneklemin en kötü katmanı çıktı: %37,0**. Beyan haklıydı.
- **Mekanizma katmanı** *(n = 9, güç 0,483)*: **"kapandı" YAZILAMAZ.**

🔴 **Ve örüntünün asıl yüzü sayıda değil, TEKRARINDA:** dördüncü denetimin
13 kapanışının **7'si** bir sonraki bulguyu doğurdu. B-45 → B-65 → **B-84**
zinciri artık **üç halkalı**. B-66'nın tek bir düzeltmesi **dört** bulgu
doğurdu — ikisi *(B-80 · B-81)* **`08`in mühürlenmeye hazır sayfasında**,
biri *(B-82)* düzeltmenin **kendi Y7 korumasının** ölü olduğu, biri
*(B-83)* kapatılmamış üçüncü eksen.

**Bir şey öğrendim ve yazıyorum:** B-57'nin ilacı — *"her sayının yanına
üretici satır"* — **yetmiyor.** Bugün üretemediğim iki sayının **ikisinin
de** üretici komutu vardı. Eksik olan satır değil, **düzeltme sonrası
yeniden koşudur**. Bir kod düzeltmesi, ondan önce ölçülmüş her sayıyı
**otomatik olarak şüpheli** yapmalı; bugün böyle bir bağ yok.

**Ve bulamadıklarımı da yazıyorum**, çünkü *"hiçbir şey bulamamak, aradığın
yerlerin listesiyle birlikte anlamlıdır"*: gözlemden simülatöre **geri
referans yok** · `teshis` bir **geri kanal değil** · `yeni_olcut`un
**dördüncü atlama yolu yok** · ve ön-kayıtlı H1.1 kapısını **yanlışlıkla
geçen bir sıfır-bilgi kolu bulamadım** — üç denedim, üçü de reddedildi.
Kapı, iki kez yanlış şey ölçtükten sonra, **üçüncü hâlinde doğru şeyi
ölçüyor.**

**Kapanış: KOŞULLU.** Araç sağlam, kapı doğru, mekanizmalar korunuyor.
Korumasız kalan yüzey — dördüncü denetçinin dediği gibi — **SONUÇ
ŞEMASIDIR**, ve o yüzey Aile 1'in ölçtüğü şeydir. `08` mühürlenmeden önce
**madde 24 ve 25 düzeltilmeli**; düzeltilmezse iki yanlış sayı mührün
içine girer.

---

🔒 **BU OTURUMDA HİÇBİR DOSYA DEĞİŞTİRİLMEDİ.** `sim/`, `tests/`,
`dogrulama/`, `v2/`, `denetim/`, `ciktilar/` ve `README.md` **okundu,
yazılmadı**. Tüm mutasyonlar ve denemeler `tempfile.mkdtemp()` ile açılan
**geçici kopyalarda** koşturuldu ve koşu sonunda silindi. Bu oturumda
yazılan **tek dosya bu rapordur** *(`aile0_audit.md`)*; önceki dört
denetimin metnine **dokunulmamıştır**, yalnızca baştaki durum bloğuna
beşinci satır ve beşinci özet eklenmiştir.

🔒 **BU OTURUMDA HİÇBİR GİT KOMUTU ÇALIŞTIRILMADI — `status` dâhil.**

🔒 **Ana deney tohumları (2000–2029) hiçbir amaçla koşulmadı.** Kullanılan
tohumlar: **1, 2, 3, 4, 5, 6, 7, 8** *(ayarlama/kapı kümesi 1–30 içinde)*.

---
---

# ALTINCI DENETİM — 26 Ağustos 2026

> 🔴 **BU BÖLÜM ÖNCEKİ BEŞ RAPORUN METNİNE DOKUNMAZ.** Yalnızca dosyanın
> sonuna eklenmiştir; baştaki durum bloğuna altıncı satır ve altıncı özet
> eklenmiştir.
>
> **Soru bu kez başka:** *"bu kodda ne bozuk?"* değil —
> **"Aile 0'ın OLMASI GEREKEN şey oldu mu?"**
> Ölçüt `03` **Bölüm C**'nin altı zorunlu sözleşmesi ve **Bölüm D**'nin dört
> doğrulama seviyesidir.

---

## 0. YÖNETİCİ ÖZETİ

# 🔴 AİLE 0 OLMASI GEREKEN ŞEY OLDU MU: **KOŞULLU — ve bugün KAPI DÜŞER**

**Katman bazında sağ kalan oranı ve ULAŞILAN GÜÇ (ilk paragraf, şart 4):**

| katman | sağ kalan | oran | %95 GA | **ULAŞILAN GÜÇ** *(p₁=0,40)* | n ≥ 19? | H0 = 0,70 |
|---|---|---|---|---|---|---|
| 🔴 **MEKANİZMA** | **7/22** | **%31,8** | **[0,139 · 0,549]** | **0,879** | ✅ **EVET** *(altı denetimde İLK KEZ)* | **REDDEDİLDİ** *(p = 2,5×10⁻⁴)* |
| **SAYAÇ / RAPORLAMA** | **3/20** | **%15,0** | [0,032 · 0,379] | **0,872** | ✅ EVET | **REDDEDİLDİ** *(p = 5,4×10⁻⁷)* |
| **26 AĞUSTOS KODU** *(çapraz kesen alt küme)* | **4/15** | %26,7 | [0,078 · 0,551] | 0,610 | 🔴 **HAYIR** | reddedildi *(p = 6,7×10⁻⁴)* |
| **GENEL** | **10/42** | **%23,8** | [0,121 · 0,395] | **0,982** | ✅ EVET | **REDDEDİLDİ** *(p = 8,8×10⁻¹⁰)* |

**AYRIKLIK:** M ∪ S = 22 + 20 = **42 = toplam** · **M ∩ S = 0** *(ayrık ve
tüketici)*. **A** ayrı bir katman değil, **çapraz kesen alt kümedir**:
A ∩ M = **2** · A ∩ S = **13**.

🔴 **"Kapandı" YAZILAMAZ.** Mekanizma katmanı ilk kez yeterli güçle ölçüldü
*(n = 22, güç 0,879)* ve H0 reddedildi — **ama %95 GA [0,139 · 0,549]:**
gerçek oran **%55'e kadar** olabilir. **Daraldı, kapanmadı.**
Seri: **%80,0 → %70,0 → %66,7 → %25,0 → %31,4 → %23,8** *(⚠️ altı örneklem
altı farklı yöntemle seçildi; seri **karşılaştırılabilir değil**)*.

**Altı sözleşmenin durumu — tek tek ölçüldü:**

| # | Sözleşme | Karar | Ölçüm |
|---|---|---|---|
| 1 | Gözlem sözleşmesi | 🟡 **KISMEN** | Yüzey kapalı ve zorlanıyor; ama **derinlik ≥ 4'teki düğümler arası yazılabilir kanal taramadan KAÇIYOR** *(8/8 yapılandırmada görünmez, teslim farkı −0,0149…+0,2040)* · **11 alanın tüketicisi yok** *(`08` madde 22 **dokuz** diyor)* |
| 2 | Ayrık RNG akışları | 🟡 **KISMEN** | `Akislar` 7 akışla kapalı; **ama ön-kayıtlı kapının NULL MODELİ `Akislar` dışında `random.Random(hash(...))` kullanıyor** ve bu istisna `06`/`07`/`08`in **hiçbirinde beyan edilmiyor** *(`07`: "bu liste kapalıdır")*. 🟢 Ölçüldü: bugün belirlenimci ve çekimler bağımsız |
| 3 | Korunum denklemi | 🔴 **SAĞLANMADI** | `03`: *"her koşuda otomatik"*. Ölçüldü: `Kosu.kostur()` `defter.kontrol()`u **hiç çağırmıyor**; 47 anahtarlı sonuç sözlüğünde `korunum_tamam` **yok**. 113 `Kosu(` çağrı yerinin **15'i** korunumu kontrol ediyor; **`dogrulama/mekanizma_kapisi.py` (48 tam koşu, Aile 1'in kapısı) kontrol etmiyor** |
| 4 | Ölçüm penceresi | 🔴 **SAĞLANMADI** | `03`: *"tüm sayaçlar aynı pencereden"*. Ölçüldü *(5 kol × 8 yapılandırma = 40 tam koşu)*: `kontrol_bayt` · `veri_bayt` · `mac_*` · `beacon_*` · `islenen_olay` **tüm koşudan** sayılıyor, teslim/gecikme ise **penceresinden**. Kontrol baytının **%17,89–22,79'u pencere dışında**; raporlanan kontrol payı gerçeğin **1,010–1,094 katı** ve **çarpıklık kola göre değişiyor** |
| 5 | Sonuç + konfigürasyon | 🔴 **SAĞLANMADI** | **Beş denetimde hiç incelenmemişti.** `SonucYazici` **hiçbir ölçüm yolunda kurulmuyor** — tek kullanıcısı kendi birim testi. Fiilen kullanılan yük `Kosu.sonuc()` ve `05` §E'nin **beş zorunlu alanından yalnızca BİRİNİ** taşıyor *(kod sürümü)* |
| 6 | Karar kaydı | 🟡 **KISMEN** | 70 kayıt · 60'ı ölçüm taşıyor · **28'i üreticisiz** *(bağımsız olarak yeniden ölçüldü, B-57'nin sayısı **TUTTU**)*. 🔴 Ama üreticisiz kayıtlardan **K-024 bugün yeniden üretilemiyor** ve sayısı **iki kaynak dosyasında olgu gibi** duruyor |

**Dört doğrulama seviyesi:**

| # | Seviye | Karar | Ölçüm |
|---|---|---|---|
| 1 | Analitik doğrulama | 🟢 **SAĞLANDI** | Ç3 = 44 test. Y10 taraması: 51 `pytest.approx` çağrısının 12'si toleranssız; **hiçbirinde 1e-12 mutlak taban baskın değil** — B-22 sınıfı kapalı |
| 2 | Korunum kontrolleri | 🟡 **KISMEN** | Denklem doğru ve Ç1 matrisinde 540/540; **ama "her koşuda" değil** *(bkz. sözleşme 3)*. Kendi 40 koşumda korunum **40/40 tuttu** |
| 3 | İç tutarlılık | 🟢 **SAĞLANDI** | Ç2 = 6 test, üç eksen; B-94 ile `hash()` yolu da kapsamda *(bağımsız olarak doğrulandı: kodda)* |
| 4 | ⭐ Literatür replikasyonu | 🔴 **GEREKÇE ÖLÇÜLMEDİ** | 1/6,29 **birebir yeniden üretildi**. 🔴 Ama replikasyon **Li'nin çalışma noktasında koşulmuyor** *(Li 2 Mbit/s, depo 1 Mbit/s)* ve bu **hiçbir yerde beyan edilmiyor**. Açığın iki adayı **ölçülen üst sınırlarıyla YETERSİZ**: EIFS ≤ %0,49 · RTS/CTS ≤ %4,99 · gereken **%10,1** |

---

### 🔴 EN ÖNEMLİ TEK BULGU — B-100

> **`python dogrulama/aile0_kapi_raporu.py` bugün koşulsa Ç1.3 `!!TABAN` ile
> DÜŞER.** Ölçüldü, tahmin edilmedi.

`dogrulama/mutasyon_paketi.py` geçici kopyayı **`v2/` hariç** kuruyor
*(satır 458 ve 688–689)*. 26 Ağustos oturumunun yazdığı **üç test** `v2/`yi
okuyor ve kopyada `FileNotFoundError` alıyor:

```
tests/test_kapi_secimleri.py::test_b57_yeni_karar_kaydi_URETICI_satiri_TASIMAK_ZORUNDA   -> v2/04-NEDEN-BOYLE.md
tests/test_kapi_secimleri.py::test_b57_URETICILI_bir_kayit_muafiyet_listesinde_OLAMAZ    -> v2/04-NEDEN-BOYLE.md
tests/test_kapi_secimleri.py::test_b93_sim_altindaki_ASSERT_sayisi_BEYANLA_ayni          -> v2/08-AILE0-KAPSAM.md
```

**Aracın KENDİ fonksiyonu koşturuldu** *(yeniden yazılmadı)*:

```
taban_tamam : False
ozet        : 3 failed, 385 passed in 853.65s (0:14:13)
```

`paketi_kostur()` taban kırıkken **erken döner**; Ç1.3 `!!TABAN` yazar ve
kapı **kapanmaz.** Aynı kusur mutant kopyalarında da var — orada üç test
**evrensel kırıcı** olurdu.

🔴 **Ucuz ön kontrol bunu YAPISAL OLARAK göremez:** `mutasyon_on_kontrol.py`
her mutantı `-k <beklenen_test>` ile koşar; bu üç test hiç toplanmaz. Yani
bu, deponun *"ön kontrol geçti, kapı düştü"* vakasının **DÖRDÜNCÜSÜDÜR**
*(K-042 · K-046 · K-058)* — ve bu kez **koşmadan önce** görüldü.

**Üretici** *(depo kökünden, 19 sn — olduğu gibi koşuldu)*:

```bash
python -c "import os,shutil,subprocess,sys,tempfile;from pathlib import Path;K=Path('.').resolve();g=Path(tempfile.mkdtemp());h=g/'depo';shutil.copytree(K,h,ignore=shutil.ignore_patterns('__pycache__','.pytest_cache','*.pyc','v2','.git','*.txt'));p=subprocess.run([sys.executable,'-m','pytest','tests/test_kapi_secimleri.py','-q','--tb=no','-p','no:cacheprovider'],cwd=h,capture_output=True,text=True,encoding='utf-8',errors='replace');print(p.stdout[-800:]);shutil.rmtree(g,ignore_errors=True)"
```

**Düzeltme** *(uygulanmadı — depoya dokunulmadı)*: `ignore_patterns`
listelerinden `"v2"` çıkarılmalı *(üç yerde: `_kosu`, `taban_kontrolu`,
`mutasyon_on_kontrol._kos`)*, **ya da** üç test `v2/` yoksa `skip` etmeli.
🔴 Birincisi tercih edilmeli: ikincisi B-93 ve B-57'nin korumasını mutant
koşusunda sessizce kapatır.

⚠️ **Kendi tahminim tutmadı ve bunu yazıyorum:** *bir* test kırılacağını
öngörmüştüm, **üç** çıktı. `taban_kontrolu` ayrıca `*.txt`i de dışlıyor ve
`_kosu` dışlamıyor — yani **taban ile mutantlar aynı dosya ortamında
koşmuyor** *(Y7)*.

---

## 1. 🔴 ALTI ZORUNLU SÖZLEŞME — tek tek, ölçümle

Her sözleşme için `03`ün üç sorusu: **var mı · zorlanıyor mu · kapsamı ne.**

### Sözleşme 1 — GÖZLEM SÖZLEŞMESİ 🟡 KISMEN

| soru | cevap |
|---|---|
| **Var mı** | ✅ `sim/gozlem.py`de üç izinli küme *(`IZINLI_GOZLEM_ALANLARI` 12 · `IZINLI_KOMSU_ALANLARI` 7 · `IZINLI_PAKET_ALANLARI` 5)*; nesneler `frozen`; simülatöre geri referans yok |
| **Zorlanıyor mu** | ✅ Ç5 = **52 test** *(bugün ölçüldü; `08` hâlâ "18 test" yazıyor)*. B-99 ile içerik kuralı üç kümeye birden uygulanıyor |
| **Kapsamı ne** | 🔴 aşağıdaki iki delik |

#### 🔴 B-101 · Paylaşım taraması DERİNLİK 4'te KÖR — ve kanal sonucu değiştiriyor

`tests/test_gozlem.py::_ulasilan_yazilabilir` nesne grafiğini
`_TARAMA_DERINLIGI = 3` ile geziyor. **Elle seçilmiş bir sabit; ölçümden
türetilmemiş.**

Kurduğum kanal: her düğüm **kendi** sarmallarını kuruyor, paylaşılan tek şey
**en içteki sözlük**. Düğümler kendi ölçtükleri gürültüyü oraya yazıp
**başkalarınınkini okuyor** — gerçek bir telsizde karşılığı olmayan, bedava
ve kusursuz bir düğümler arası kanal *(`03` kural 5)*.

| gömme derinliği | tarama gördü | kaç düğüm yazıyor |
|---|---|---|
| 0 · 1 · 2 · 3 | **15** ✅ | 16 |
| **4** | 🔴 **0** | 16 |
| **5** | 🔴 **0** | 16 |

**Kanal etkisiz değil** *(Y8/Y11 — kontrol kolu: düğüm başına AYRI sözlük)*:

| yapılandırma | paylaşımlı | ayrı | fark |
|---|---|---|---|
| S2 t3 | 0,169154 | 0,139303 | **+0,029851** |
| S2 t7 | 0,314721 | 0,304569 | +0,010152 |
| S0 t3 | 0,238806 | 0,248756 | −0,009950 |
| **S1 t5** | **0,283582** | **0,079602** | 🔴 **+0,203980** *(3,6 kat)* |
| S2 t11 | 0,587940 | 0,597990 | −0,010050 |
| S3 t2 | 0,325000 | 0,295000 | +0,030000 |
| S4 t9 | 0,202970 | 0,217822 | −0,014851 |
| S5 t4 | 0,025000 | 0,020000 | +0,005000 |

**8/8 yapılandırmada tarama 0 diyor; 8/8'inde sonuç farklı.** `ortalama_atlama`
sekizinde de değişiyor *(ör. S4 t9: 1,878 vs 4,068)*.

⚠️ **Örneklem beyanı:** 1 **kasten kurulmuş** kol × 8 yapılandırma. Bu bir
*varlık* iddiasıdır *("böyle bir kanal kurulabiliyor")*, eşdeğerlik iddiası
değil — o yüzden tek kol yeterlidir ve genişliği burada yazılıdır.
Koşular kısaltılmış *(16 düğüm · 30 s)*; **etkinin büyüklüğü** tam koşuda
farklı olabilir, **görünmezliği** olmaz *(tarama zamandan bağımsız)*.

**Üretici:** `python scratchpad/b86_derinlik.py` · `python scratchpad/b86_kanal_etkisi.py`
*(ikisi de bu oturumda yazıldı; `tests/test_gozlem.py`nin KENDİ tarama
fonksiyonlarını import ediyor, yeniden yazmıyor)*

> ⚖️ **Kendi ilk denemem BAŞARISIZ oldu ve bunu yazıyorum:** sarmalları
> **ortak** kurmuştum; tarama onları derinlik 0'da gördü ve **KAZANDI**
> *(0→5 derinliğin hepsinde 15 çakışma)*. Sarmalların düğüm başına
> kurulması şart. `03` B1: *"null modeli fazla eşleştirmek"*in tersi —
> saldırıyı fazla eşleştirmek.

#### 🔴 B-102 · `08` madde 22 DOKUZ diyor, bugün ONBİR

`sim/` + `dogrulama/` altında `<önek>.<alan>` taraması *(K-053'ün tarifi)*:

| küme | alan | tüketicisi VAR | tüketicisi YOK |
|---|---|---|---|
| `Gozlem` | 12 | 3 | **9** *(madde 22 ile birebir aynı isimler)* ✅ |
| `KomsuKaydi` | 7 | 5 | 🔴 **2** — `bildirdigi_kuyruk` · `duyulan_beacon` |
| `PaketGorunumu` | 5 | 5 | 0 |

**Toplam 11.** B-99 `duyulan_beacon`ı *"ONUNCU"* diye kodda anıyor ama
`08` madde 22 **güncellenmedi**; `bildirdigi_kuyruk` **hiçbir yerde**
tüketicisiz diye anılmıyor *(yalnızca içerik testi yokluğu beyan edilmiş)*.

**Üretici:** `python scratchpad/madde22.py`

---

### Sözleşme 2 — AYRIK RNG AKIŞLARI 🟡 KISMEN

| soru | cevap |
|---|---|
| **Var mı** | ✅ `sim/rng.py::Akislar`, 7 adlı akış + durumsuz kanal çekimi. `AKIS_ADLARI` *"kapalı liste"* |
| **Zorlanıyor mu** | ✅ `test_b10_her_akis_ya_kullaniliyor_ya_beyan_edilmis` · Ç2.2 *(B-94 ile `hash()` yolu da kapsamda)* |
| **Kapsamı ne** | 🔴 **`Akislar` dışında bir rastgelelik kaynağı var ve BEYAN EDİLMEMİŞ** |

#### 🔴 B-103 · Ön-kayıtlı kapının null modeli `Akislar` dışında

`dogrulama/aktaricilar.py::kalite_ablasyonu`:

```python
random.Random((hash(anahtar) & 0xFFFFFFFF) ^ tuz).shuffle(idx)
```

`sim/rng.py` kendi başında şunu yazıyor:

> *"blake2b kullanılıyor çünkü Python'un yerleşik `hash()`'i çalışmalar
> arasında tuzlanır ve BELİRLENİMCİ DEĞİLDİR. `hash()` kullanmak bu projede
> sessiz bir belirlenimsizlik kaynağı olurdu."*

Ve `07` akış tablosunun altında: *"bu liste **kapalıdır**"*.

🟢 **Bugün zararsız — ÜÇÜ DE ÖLÇÜLDÜ:**

1. **Belirlenimci mi?** `hash((int, int demeti))` üç `PYTHONHASHSEED` değerinde
   **birebir aynı** *(`6286405454634030006`, permütasyon `[3,2,1,0,4]`)*;
   karşılaştırma için **dizgi** demeti üçünde **üç farklı** değer veriyor.
2. **`tuz` XOR'u çekimleri bağımsız yapıyor mu?** *(A-5'in `06`da yazılı
   açık uyarısı)* — 200 000 anahtar × 5 çekim:

   | k | XOR (depo) çift-eşitlik | BAĞIMSIZ referans | beklenen 1/k! |
   |---|---|---|---|
   | 3 | 0,166768 | 0,166044 | 0,166667 |
   | 6 | 0,001407 | 0,001419 | 0,001389 |
   | 8 | 0,000024 | 0,000029 | 0,000025 |

   İlk eleman ki-karesi her k'da %95 kritik değerin altında.
   🟢 **`06`nın uyarısı KAPATILABİLİR: çekimler bağımsız.**
3. **Tohum permütasyona girmiyor — tohumlar korele mi?** Kapının kendi
   yapılandırmasında *(S2, tohum 1–8, `gurultuden_kacan`)* **959 ayrık
   anahtar**; 28 tohum çiftinin **hepsinde ortak anahtar oranı %0,000**;
   toplam tekrar **0**. 🟢 **Korelasyon YOK.**

🔴 **Ama sözleşme yine de ihlal ediliyor ve ihlal BEYAN EDİLMEMİŞ.**
`06`, `07` ve `08`de `kalite_ablasyonu`nun RNG'si **hiç geçmiyor**; `07`
tersine *"liste kapalıdır"* diyor. İstisna yalnızca
`test_c2_2_...`in **docstring'inde** yazılı — ve bir docstring, `08`in
kapsam beyanı değildir.

🔴 **Ölçülmüş ikinci sınır:** ablasyon **k ≤ 3** olan kararlarda m=5'in
çoğu çekimi çakışır — `k=1`de permütasyon **birim**, `k=2`de yalnızca 2
permütasyon var. Kapının kendi yapılandırmasında:

| k | karar | pay |
|---|---|---|
| 1 | 5 439 | %1,21 *(ablasyon HİÇBİR ŞEY yapmıyor)* |
| 2 | 24 515 | %5,45 *(m=5 → en çok 2 ayrık çekim)* |
| 3 | 22 790 | %5,07 |
| **k ≤ 3 toplam** | **52 744 / 449 498** | 🔴 **%11,73** |

K-064'ün *"ablasyon çekimi varyansın %46,4'ü"* ayrıştırması **tek havuzlanmış
sayıdır**; m=5'in fiilen aldığı varyans azaltması karar başına **k'ya
bağlıdır** ve bu yazılı değil.

**Üretici:** `python scratchpad/a5_hashseed.py` · `python scratchpad/a5_tuz.py` · `python scratchpad/a5_anahtar.py`

---

### Sözleşme 3 — KORUNUM DENKLEMİ 🔴 SAĞLANMADI

`03` Bölüm C: *"`üretilen = teslim + düşen + kuyrukta + uçuşta`, **her koşuda
otomatik**"*. `05` §E: *"**Korunum denklemi sonucu** — tutmadıysa satır
geçersiz işaretlenir"* — **zorunlu sonuç alanı.**

#### 🔴 B-104 · `Kosu.kostur()` korunumu HİÇ ÇAĞIRMIYOR

```
sonuc anahtar sayisi: 47
'korunum' in r      : False
'korunum_tamam' in r: False
```

`KorunumDefteri.kontrol()` çağrı yerleri *(depo geneli, `__pycache__` hariç)*:

| yer | adet |
|---|---|
| `tests/` | 13 |
| `dogrulama/kapi_korunum.py` *(Ç1 matrisi)* | 1 |
| `dogrulama/beacon_teshis.py` | 1 |
| **`sim/` altında** | 🔴 **0** |

`Kosu(` çağrı yeri **113**. Yani korunum *"her koşuda otomatik"* değil,
**Ç1 matrisinde ve bazı testlerde elle** kontrol ediliyor.

🔴 **Somut sonuç:** `dogrulama/mekanizma_kapisi.py` — **Aile 1'in her kolunu
fiilen geçiren kapı** — kol başına **48 tam koşu** yapıyor ve **hiçbirinde**
korunumu kontrol etmiyor. Bir koşu sessizce korunumu kırarsa kapı o koşunun
sayısını okur ve fark etmez. `sim/ledger.py`nin kendi gerekçesi:
*"Sessiz paket kaybı bu alanın en zor bulunan hata sınıfıdır."*

🟢 **Ben ölçtüm ve bugün kırılmıyor:** kendi 40 koşumda *(5 kol × 8
yapılandırma)* korunum **40/40** tuttu. Yani bu bir *hata* değil, **eksik
bir sözleşmedir** — ve `03` tam olarak bunun *"sonradan eklenemez"*
olduğunu söylüyor: `sonuc()` şeması Aile 1 başladıktan sonra
değiştirilemez *(`kosucu.py`nin kendi beyanı, B-19'un dersi)*.

**Üretici:**

```bash
python -c "import sys;sys.path.insert(0,'.');from sim.config import Konfig;from sim.kosucu import Kosu;from dogrulama.aktaricilar import AKTARICILAR;r=Kosu(Konfig(kol='t',senaryo='S2',tohum=1),AKTARICILAR['gurultuden_kacan']).kostur();print(len(r),'korunum' in r,'korunum_tamam' in r)"
```

---

### Sözleşme 4 — ÖLÇÜM PENCERESİ 🔴 SAĞLANMADI

`03`: *"Isınma ayrı, ölçüm ayrı; **tüm sayaçlar aynı pencereden**."*

#### 🔴 B-105 · Sonuç sözlüğü İKİ AYRI PENCEREYİ karıştırıyor

| pencere | alanlar |
|---|---|
| **ölçüm penceresi** `[isinma_s, olcum_bitis_s]` = 270 s | `teslim_orani` · `pencerede_uretilen` · `pencerede_teslim` · gecikmeler · `ortalama_atlama` · `teslim_kimlikleri` |
| 🔴 **TÜM KOŞU** `[0, kosu_bitis_s]` = 350 s | `kontrol_bayt` · `veri_bayt` · `kontrol_airtime_s` · `veri_airtime_s` · `mac_gonderilen` · `mac_onay` · `mac_kayip_onay` · `mac_kopya_alim` · `mac_basarisiz_alim` · `mac_deneme` · `beacon_*` · `ttl_olumu` · `hedef_yok` · `mac_dusurmesi` · `kuyruk_tasmasi` · `en_yuksek_doluluk` · `islenen_olay` |

**Ölçüldü** — koşunun içine `t = isinma_s` ve `t = olcum_bitis_s` anlarında
iki gözlem olayı enjekte edildi *(hiçbir rastgelelik çekmiyorlar)*,
**5 kol × 8 yapılandırma = 40 tam koşu**:

| büyüklük | değer |
|---|---|
| Pencere DIŞINDA üretilen kontrol baytı | **%17,89 – %22,79** |
| Raporlanan kontrol payı / pencere içi kontrol payı | **1,010 – 1,094** *(ortanca 1,062)* |
| Korunum | 40/40 tuttu |

🔴 **Çarpıklık KOLA GÖRE DEĞİŞİYOR** — yani eşleştirilmiş bir kol
karşılaştırması **yanlıdır**:

| kol | oran aralığı |
|---|---|
| `gurultuden_kacan` | 1,012 – 1,049 |
| `dongu_yapan` | 1,010 – 1,069 |
| `hedefe_en_yakin` | 1,053 – 1,082 |
| `en_kisa_yol` | 1,066 – 1,083 |
| `DV (mesafe_vektoru)` | 1,030 – 1,094 |

**Bu, `08` madde 25'in BAĞLAYICI sayısını doğrudan vuruyor.**
`dogrulama/kontrol_payi.py::kontrol_payi()` tam olarak
`sonuc["kontrol_bayt"] / (kontrol_bayt + veri_bayt)` hesaplıyor — yani
**tüm koşudan**. Eşleştirilmiş oranı iki pencerede de hesapladım:

| çalışma noktası | raporlanan *(tüm koşu)* | pencere içi |
|---|---|---|
| S0 · orta · t1 | 14,26 kat | 13,59 kat |
| **S2 · orta · t1** | **8,29 kat** ← `08`in alt sınırı **%8,3** | **7,85 kat** |
| S2 · orta · t2 | 12,59 kat | 12,12 kat |

🟢 **B-80 bağımsız olarak DOĞRULANDI:** DV kolu S2/orta/t1'de **%13,710** —
`08` madde 25'in yazdığı **%13,71** ile birebir; gözlem kolu **%1,653**,
beyan edilen **%1,65–1,87** bandının içinde.

#### 🟡 A-7 — iki uçta farklı kapalılık *(devralınan, ölçüldü)*

`sonuc()`: `bas <= dogum_s` + `assert dogum_s <= bit` → **[bas, bit] kapalı**.
`yakinsama_kontrolu()`: dilim başına `a <= dogum_s < b` → **son uç açık**.
`traffic.py` üretimi `simdi + sonraki <= olcum_bitis_s` koşuluyla planlıyor,
yani `dogum_s == bit` **ölçü sıfır** bir olay: bugün fark üretmiyor.

🔴 **Ama S5'te pencere farkı ölçü sıfır DEĞİL:** hareketli karıştırıcıda
`_yakinsama_dilimleri` **tam yörünge** dilimleri kesiyor ve artanı
**dışlıyor**. Yörünge periyodu `2π·300/15 = 125,664 s`, pencere 270 s,
tam tur 2 → dilimler **251,33 s** kapsıyor, **18,67 s = %6,9** dışarıda.
Kodda yazılı, `08`de değil.

---

### Sözleşme 5 — SONUÇ + KONFİGÜRASYON BİRLİKTE 🔴 SAĞLANMADI

> **Beş denetimin hiçbiri bu sözleşmeye bakmadı.**

#### 🔴 B-106 · `SonucYazici` HİÇBİR ÖLÇÜM YOLUNDA KURULMUYOR

`SonucYazici` geçen tüm yerler *(depo geneli)*:

| yer | ne |
|---|---|
| `sim/results.py` | tanım |
| `sim/__init__.py` | dışa aktarım |
| `tests/test_results.py` | **tek kullanıcı** — 3 birim testi |
| `dogrulama/sag_kalan_ayikla.py:191` | bir **yorum**: *"`SonucYazici` bu matriste HİÇ kurulmuyor"* |

`dogrulama/` altındaki **hiçbir** ölçüm aracı *(kapı raporu · korunum
matrisi · kalibrasyon · mekanizma kapısı · kontrol payı · Li)* sonuç yazmıyor.
Yani `03`ün *"her sonuç kendi tam konfigürasyonuyla saklanır"* sözleşmesi
**bildirilmiş, test edilmiş ve hiç çağrılmamış** — `03` B5'in
*"bildirim ≠ kullanım"* tuzağının **dördüncü** örneği *(öncekiler:
`UYGULANMAMIS_BAYRAKLAR` · `rng.HENUZ_KULLANILMAYAN` · B-27b)*.

#### 🔴 B-107 · `05` §E'nin BEŞ zorunlu alanından yalnızca BİRİ var

Fiilen kullanılan yük `Kosu.sonuc()` *(47 alan)*:

| `05` §E zorunlu alan | `sonuc()`te | not |
|---|---|---|
| Tüm konfigürasyon bayrakları | 🔴 **YOK** | yalnızca `kurulum_hash` — **tek yönlü**, konfige geri çevrilemez |
| Tohum | 🔴 **YOK** | `kurulum_hash`in içinde, okunamaz |
| Kod sürümü | 🟢 **VAR** | `kaynak_hash` — **B-46/K-051'de eklendi** |
| Korunum denklemi sonucu | 🔴 **YOK** | bkz. B-104 |
| Ölçüm penceresi *(başlangıç–bitiş)* | 🔴 **YOK** | `pencere_kimlik_araligi` **paket kimliği**, zaman değil |

⚖️ **Bu, B-46'nın tam olarak yarım kalmış hâlidir.** Üçüncü denetim
`05` §E'yi okudu, **beş alandan birinin** eksik olduğunu gördü, onu ekletti
*(K-051)* — ve **kalan dördüne bakmadı.** Aynı paragraf, aynı liste.

#### 🟡 A-8 devamı — `topoloji` / `trafik` alt sözlük şemaları

Hiçbir yerde listelenmiyorlardı; ölçüldü:

```
topoloji -> bilesen_sayisi · dugum_sayisi · en_buyuk_bilesen · en_buyuk_derece
            en_kucuk_derece · ortalama_derece · yalniz_dugum
trafik   -> akis_sayisi · farkli_hedef · farkli_kaynak · uretilen_paket
```

⚠️ Ayrıca bir **ad çakışması**: `sonuc["trafik"]` bir **özet sözlüğü**,
`Konfig.trafik` ise `"orta"|"yogun"|"seyrek"`. Aynı ad, iki anlam.

---

### Sözleşme 6 — KARAR KAYDI 🟡 KISMEN

| soru | cevap |
|---|---|
| **Var mı** | ✅ `v2/04-NEDEN-BOYLE.md` · **70 kayıt** *(bugün ölçüldü)* |
| **Zorlanıyor mu** | ✅ `dogrulama/karar_kaydi_denetimi.py` + `test_b57_*` iki test |
| **Kapsamı ne** | 🔴 **28 kayıt üreticisiz**, ve en az biri bugün **üretilemiyor** |

🟢 **B-57'nin sayısı BAĞIMSIZ OLARAK DOĞRULANDI.** Aracı koşturdum
*(70 kayıt · 60 ölçüm taşıyan · 28 üreticisiz · yeni boşluk yok)* ve
ayrıca **ölçüm taşımayan 10 kaydın onunu da tek tek okudum**: dokuzu
gerçekten ölçüm taşımıyor *(tarih · adım numarası · öğrenci tahmini)*,
onuncusu **K-052 ölçüm taşıyor ama zaten `**Üretici:**` satırı var**, yani
`eksik` listesine hiç girmiyor. **`_OLCUM` deseni fazla dar değil.**

#### 🔴 B-108 · K-024'ün sayısı bugün ÜRETİLEMİYOR — ve iki kaynak dosyasında olgu gibi duruyor

K-024 *(üreticisiz)*: *"ardışık deneme başlangıçları arası **9528–18068 µs**"*.
Bu cümle `sim/config.py` ve `sim/rng.py` **yorumlarında** `kanal_dilimi_s`
seçimini savunmak için tekrarlanıyor.

Ölçüldü — **35 282 GERÇEK yeniden deneme çifti**, 4 yapılandırma, tam koşu
*(yalnızca `m.deneme` artan çiftler; ilk denemem fazla genişti ve döngüyle
geri gelen paketleri de sayıyordu — düzeltildi)*:

| büyüklük | değer |
|---|---|
| min | **8 768 µs** 🔴 *(iddia edilen alt sınır 9 528'in altında)* |
| 9 528'in altında | **5 698 = %16,15** |
| 18 068'in üstünde | **19 382 = %54,94** |
| ortanca | 18 660 µs |
| **AYNI 1 ms dilimine düşen çift** | 🟢 **0** |
| **AYNI 100 µs dilimine düşen çift** | 🟢 **0** |

⚖️ **Sayı bayat, KARAR sağlam.** K-024'ün *"1 ms dilimde de çakışma HİÇ
olmuyordu"* sonucu **birebir üretiliyor**; `kanal_dilimi_s = 1e-4` marj
kararı ayakta. Bayatlayan şey **aralık rakamı** — ve o rakam, üreticisi
olmadığı için **kimse fark etmeden iki kaynak dosyasına yayılmış**.

**Üretici:** `python scratchpad/k024b.py`

#### 🟢 K-017 bugün BİREBİR üretiliyor — ve artık üreticisi var

*(üreticisiz kayıtlardan ikinci örnek — Y6: kendi lehime çıkan sonuç da sınandı)*

| iddia *(K-017 / `config.py`)* | bugün ölçülen |
|---|---|
| 30 düğüm / 250 m'de "30 tohumun yalnızca **7**'si bağlıydı" | **7** ✅ |
| "en büyük bileşen **10–30** arasında geziniyordu" | **10–30** ✅ |

**Üretici:** `python scratchpad/k017.py`

---

## 2. 🔴 DÖRT SEVİYELİ DOĞRULAMA — tek tek, ölçümle

### Seviye 1 — ANALİTİK DOĞRULAMA 🟢 SAĞLANDI

Ç3 bugün **44 test** *(`KAPI_SECIMLERI["Ç3"].adet = 44`, bugün toplandı)*.

🔴 **Y10 taraması tüm pakete uygulandı** — `03`ün kendi kuralı Ç3 dışına hiç
uygulanmamıştı. `ast` ile 51 `pytest.approx` çağrısı bulundu; **12'si
toleranssız**. Her birinin karşılaştırdığı büyüklük ölçüldü:

| iddia | büyüklük | `rel=1e-6` toleransı | 1e-12 tabanı baskın mı |
|---|---|---|---|
| `difs_s` *(en küçüğü)* | 5,0e-05 | 5,0e-11 | **hayır** |
| `onay_suresi_s` | 3,04e-04 | 3,0e-10 | hayır |
| `cerceve_suresi_s(1024)` | 8,38e-03 | 8,4e-09 | hayır |
| diğer 9 | 0,5 … 603 | ≥ 5e-07 | hayır |

🟢 **1e-12 mutlak tabanının baskın olduğu iddia sayısı: 0.** B-22/Y10 sınıfı
**tüm pakette** kapalı — ölçüldü, varsayılmadı.

⚠️ **Kapsam beyanı:** bu iddiaların **beşi** kapalı formu değil, **kodun
kendi formülünü** yeniden yazıyor *(ör. `kon.difs_s == approx(kon.sifs_s +
2*kon.slot_s)`)*. Gövde değişikliğini yakalarlar, **sabit** değişikliğini
yakalamazlar. Bu bir kusur değil ama *"analitik doğrulama"* etiketinin
kapsamıdır.

**Üretici:** yukarıdaki `ast` taraması *(rapor §12)*

---

### Seviye 2 — KORUNUM KONTROLLERİ 🟡 KISMEN

Denklem doğru, defter tek geçiş noktası, Ç1.1 **540/540**. **Ama "her koşuda
otomatik" değil** — bkz. **B-104**. Kendi 40 koşumda korunum **40/40** tuttu;
yani bugün kırılmıyor, **kapsam eksik**.

Bilinen ve `08`de yazılı sınır duruyor: korunum denklemi **kayıp geçişi
göremez** *(K-029)*; onu yakalayan şey boşaltma kontrolüdür (Ç1.4).

---

### Seviye 3 — İÇ TUTARLILIK 🟢 SAĞLANDI

Ç2 = 6 test, üç eksen *(tam koşu · `PYTHONHASHSEED` · iki kol aynı kanal)*.
B-94'ün genişletmesi **kodda bulundu ve doğrulandı**:
`test_c2_2_pythonhashseed_den_bagimsiz` artık `kalite_ablasyonu` kolunu da
koşuyor, **tam sonuç sözlüğünün** parmak izini karşılaştırıyor ve
`hash("ayni_dizgi")` ile **aracın kendisinin canlı olduğunu** ölçüyor.

⚖️ Kendi ölçümüm de aynı yöne çıktı *(§1, sözleşme 2)*: tamsayı demeti hash'i
üç `PYTHONHASHSEED` değerinde birebir aynı, dizgi demeti üç farklı.

---

### Seviye 4 — ⭐ LİTERATÜR REPLİKASYONU 🔴 GEREKÇE ÖLÇÜLMEDİ

`03` Bölüm D'nin şartı: *"birebir çakışma gerekmez; **nitel eğilimin aynı
olması ve farkın gerekçelendirilmesi** yeterlidir."*
`08` kendi beyanı: *"Fark %10 ve **açıklaması ölçülmedi, atfedildi**."*

#### Önce: replikasyon NEYİ replike ediyor — kaynağa dönüldü

`v2/kaynak_doğrulama.txt` öğrencinin **birebir kopyaladığı** paragrafları
taşıyor *(Li, Blake, De Couto, Lee, Morris, §3.2, s.3)*:

> *"…they approach a utilization of 0.25 Mbps for 1500-byte packets, or
> **1/7 of the maximum of 1.7 Mbps**."*

🔴 **"1,7 Mbps" bir çalışma noktasıdır ve bu depoda hiçbir yerde yazılı
değil.** 1500 baytta 1,7 Mbps tek atlama tavanı **2 Mbit/s'lik 802.11**
demektir. Depo **1 Mbit/s**'te koşuyor *(`Konfig.bit_hizi_bps = 1e6`,
tek atlama 932 kbps)*.

#### 🟢 1/6,29 BİREBİR YENİDEN ÜRETİLDİ

30 tohum · 20 atlama · aralık 0,85R *(`li_duyarlilik.plato_olc` ile aynı
tanım, bağımsız yazıldı)*:

| bit hızı | tek atlama | plato | 1/x | %95 GA | GA genişliği |
|---|---|---|---|---|---|
| **1 Mbit/s** ← depo | 932,0 kbps | 0,1591 | **6,29** | [1/6,22 · 1/6,35] | **%2,04** |
| **2 Mbit/s** ← Li | **1 761,2 kbps** | 0,1573 | **6,36** | [1/6,31 · 1/6,40] | %1,54 |
| 4 Mbit/s | 3 171,3 kbps | 0,1515 | 6,60 | — | %1,27 |
| 0,5 Mbit/s | 480,0 kbps | 0,1591 | 6,28 | — | %3,17 |

`08`in yazdığı **1/6,29 · GA %2,04** ile **birebir** *(Y6: kendi lehime çıkan
sonucu da sınadım — tuttu)*.

#### 🔴 B-109 · Replikasyon Li'nin ÇALIŞMA NOKTASINDA koşulmuyor ve bu beyan edilmiyor

`08` Ç4 KAPSAMAZ tablosunda bit hızı **yok**; Ç4.3 duyarlılık taraması
**dört eksen** tarıyor *(paket boyutu · yeniden deneme sınırı · CW min ·
aralık çarpanı)* ve **bit hızı bunlardan biri değil** — oysa replikasyonun
kaynaktan **2 kat** ayrıldığı tek eksen budur.

🟢 **Ve ölçüm iyi haber veriyor:** Li'nin kendi çalışma noktasında
*(2 Mbit/s, 1500 B)* araç **iki mutlak sayıyı da** üretiyor:

| büyüklük | Li vd. | bu araç *(2 Mbit/s)* | fark |
|---|---|---|---|
| tek atlama tavanı | **1,7 Mbps** | **1,761 Mbps** | %3,6 |
| uzun zincir verimi | **0,25 Mbps** | **0,277 Mbps** | %10,8 |

Depo bugüne kadar yalnızca **oranı** karşılaştırdı. **İki mutlak sayının da
tuttuğu hiç yazılmadı** — replikasyon olduğundan **zayıf** sunuluyor.

#### 🔴 B-110 · %10'luk açığın iki adayı ÖLÇÜLEN ÜST SINIRLARIYLA YETERSİZ

`08`: *"kalan fark modellenmeyen RTS/CTS ve EIFS'e **atfedilmektedir**"*.
`03` B4: *"bir kusuru ölçmek, onu SEBEP yapmaz."* Burada kusur **hiç
ölçülmemiş**. Ölçtüm:

| aday | yöntem | üst sınır |
|---|---|---|
| **bit hızı** *(yeni aday)* | 30 tohum × 2 uzunluk, ölçüm | 1/6,29 → **1/6,36** = plato **%1,1** kayıyor 🔴 **AÇIĞI KAPATMIYOR** |
| **EIFS** | çözülemeyen alım oranı **ölçüldü** *(0,1253 · 20 atlama · 30 tohum)* × `EIFS − DIFS = 314 µs` / döngü 12 866 µs | **≤ %0,31** *(1 Mbit/s)* · **≤ %0,49** *(2 Mbit/s)* |
| **RTS/CTS** | analitik: `cerceve_suresi_s(20) + cerceve_suresi_s(14) + 2·SIFS = 676 µs` | **≤ %4,99** *(1 Mbit/s)* · ≤ %7,35 *(2 Mbit/s)* |
| **GEREKEN** | 1/6,29 → 1/7 | 🔴 **%10,1** |

**İkisi birlikte, EN CÖMERT yönde ve etkileşimsiz varsayılarak: ≤ %5,3.**
Gereken **%10,1**. Üstelik RTS/CTS'in **ikinci etkisi ters yönlüdür**
*(gizli terminal çakışmalarını AZALTIR)* ve o etki ölçülmedi — yani %4,99
bile bir **üst sınır değil, tek yönlü bir tahmindir**.

⚖️ **Karar:** `03` Bölüm D'nin *"farkın gerekçelendirilmesi"* şartı
**sağlanmıyor.** Sağlanan şey *"nitel eğilimin aynı olması"* — o kısım
sağlam *(düşüş + plato + 4 atlamada 1/3,87 ≈ Li'nin 1/4'ü)*. `08`in kendi
cümlesi (*"atfedilmektedir, kaynaklanmamaktadır"*) **doğru ama yetersiz**:
bugün elimizde adayların **ölçülmüş üst sınırları** var ve **yetmiyorlar**.

> ⚖️ **Kendi hipotezim ÇÜRÜDÜ ve bunu yazıyorum (Y9).** Bit hızının açığı
> kapatacağını öngörmüştüm *(sabit zamanlı çekişme ek yükleri 1 Mbit/s'te
> göreli olarak yarıya iner → çok atlamalı ceza küçülür)*. Ölçüm: plato
> yalnızca **%1,1** kayıyor. Yön doğru, **büyüklük yanlış**. Aday **elendi**
> — ve elenmesi bir kazançtır: onay modellemesi *(~%30)* ve yeniden deneme
> sınırı *(%0,71)* ile birlikte **ölçümle elenen üçüncü aday**.

**Üretici:** `python scratchpad/li_bithizi.py` · `python scratchpad/li_eifs.py` · `python scratchpad/li_rtscts.py`

---

## 3. ON ÜÇ ÇIKIŞ KRİTERİ — her biri ölçtüğünü mü ölçüyor

| kriter | ölçtüğünü ölçüyor mu | not |
|---|---|---|
| **Ç1.1** korunum 540/540 | 🟢 evet | `BEKLENEN_KOSU = 6*3*30` sabit; boş kümede `0==0` tuzağı kapalı. ⚠️ 540 koşunun **tamamı tek kâhin kolla** *(`08`de yazılı)* |
| **Ç1.2** dört düşme sebebi | 🟢 evet | dördü de uç durumlardan geliyor *(`08`de yazılı)* |
| **Ç1.3** mutasyon paketi 35/35 | 🔴 **BUGÜN DÜŞER** | **B-100** — taban kırık *(3 kırık test)*. Ölçüt doğru, **girdi ortamı bozuk** |
| **Ç1.4** boşaltma < %1 | 🟢 evet | boş kümede açıkça düşüyor |
| **Ç2** belirlenimcilik | 🟢 evet | üç eksen zorunlu kapsamda; B-94 ile `hash()` yolu da |
| **Ç3** analitik 44 test | 🟢 evet | Y10 taraması temiz *(bugün ölçüldü)* |
| **Ç4.1** Li regresyon 6 test | 🟢 evet | bant ±%10, kırılabilir |
| **Ç4.2** plato GA < %5 | 🟢 evet | bağımsız olarak **birebir** üretildi *(%2,04)* |
| **Ç5** gözlem sözleşmesi 52 test | 🟡 **kısmen** | sayı **ve** kapsam iki ayrı eksende korunuyor ✅ — ama koruduğu tarama **derinlik 4'te kör** *(B-101)* |
| **Ç6.1** onay gerçek iletim | 🔴 **HAYIR** | **B-111** aşağıda |
| **Ç6.2** kanal dilimi marjı | 🟢 evet | B-09'da dizgiden gerçek değişmeze çevrildi |
| **Ç6.3** `Iletim` kimlikle | 🔴 **HAYIR** | **B-111** aşağıda |
| **Ç6.4** `skeleton.py` silindi | 🟢 evet | `Path.exists()` — gerçek kontrol |

### 🔴 B-111 · Ç6.1 ve Ç6.3 İKİ YÖNDE DE KANDIRILABİLİR

Kapının yüklemleri *(`aile0_kapi_raporu.py`)* **tüm dosya üzerinde dizgi
araması** — yorum ve docstring dâhil:

```python
Ç6.1 : 'Iletim(alici, veri_gonderen' in kaynak_mac
Ç6.3 : "if x is il:" in kaynak_mac and ".remove(il)" not in kaynak_mac
```

Ölçüldü — her deneme geçici bir kopyada:

| deneme | Ç6.1 | Ç6.3 | olması gereken |
|---|---|---|---|
| (0) dokunulmamış | ✅ True | ✅ True | geçmeli |
| **(a1)** onay YÖNÜ ters çevrildi *(`Iletim(veri_gonderen, alici, …)`)* + aynı dizgi **YORUMDA** | 🔴 **True** | True | **düşmeli** |
| **(a2)** kimlik → **DEĞER** karşılaştırması + aynı dizgi **YORUMDA** | True | 🔴 **True** | **düşmeli** |
| **(b1)** `if x is il` → `if il is x` *(davranış **birebir aynı**)* | True | 🔴 **False** | geçmeli |
| **(b2)** yorumda `.remove(il)` geçiyor *(kod değişmedi)* | True | 🔴 **False** | geçmeli |

**Yanlış negatif ve yanlış pozitif, ikisi de ölçüldü.** Bu, B-09'un
Ç6.2'de kapattığı hata sınıfının **birebir aynısıdır** ve Ç6.1/Ç6.3'te
**açık bırakılmıştır**. 26 Ağustos oturumu bu sınıf için bir çözüm de
yazdı — **B-89'un PROZA/kod ayırt etme testi** — ama onu yalnızca gözlem
işaretleyicisine uyguladı, kapıya **uygulamadı**.

**Üretici:** `python scratchpad/c6_kandirma.py`

---

## 4. YENİ BULGULAR — B-100'den

| # | bulgu | sınıf | nerede |
|---|---|---|---|
| **B-100** | 🔴 **Kapı bugün Ç1.3'te `!!TABAN` ile düşer.** Mutasyon paketi geçici kopyayı `v2/` **hariç** kuruyor; 26 Ağustos'un yazdığı **üç test** `v2/`yi okuyor. Ölçüldü: **3 failed, 385 passed**. Ucuz ön kontrol bunu **yapısal olarak göremez** *(dördüncü "ön kontrol geçti, kapı düştü" vakası)* | `03` kural 15 · Y7 · Y14 | `dogrulama/mutasyon_paketi.py:458,688` |
| **B-101** | 🔴 **Paylaşım taraması derinlik ≥4'te kör.** `_TARAMA_DERINLIGI = 3` elle seçilmiş. Derinlik 4'te kurulan düğümler arası yazılabilir kanal **8/8 yapılandırmada görünmüyor** ve **sonucu değiştiriyor** *(teslim farkı −0,0149…+0,2040)* | `03` kural 5 · B-69'un bir katman altı | `tests/test_gozlem.py:1353` |
| **B-102** | 🟡 **`08` madde 22 DOKUZ diyor, bugün ONBİR.** `KomsuKaydi.bildirdigi_kuyruk` ve `duyulan_beacon` tüketicisiz; ikisi de madde 22'de yok | `03` B5 | `v2/08` madde 22 |
| **B-103** | 🔴 **Ön-kayıtlı kapının NULL MODELİ `Akislar` dışında `random.Random(hash(...))` kullanıyor** ve istisna `06`/`07`/`08`de **beyan edilmiyor** *(`07`: "bu liste kapalıdır")*. Üç ölçüm bugün zararsız olduğunu gösteriyor | `03` sözleşme 2 | `dogrulama/aktaricilar.py:103` |
| **B-104** | 🔴 **`Kosu.kostur()` korunum denklemini HİÇ kontrol etmiyor** ve sonuç sözlüğü taşımıyor. `sim/` altında `defter.kontrol()` çağrısı **0**. Aile 1'in kapısı 48 koşuda korunum kontrol etmiyor | `03` sözleşme 3 · `05` §E | `sim/kosucu.py:241` |
| **B-105** | 🔴 **Sonuç sözlüğü İKİ AYRI PENCEREDEN sayıyor.** Kontrol baytının **%17,89–22,79'u** ölçüm penceresi dışında; kontrol payı **1,010–1,094×** şişik ve **çarpıklık kola göre değişiyor**. `08` madde 25'in bağlayıcı oranını etkiliyor | `03` sözleşme 4 · B3 | `sim/kosucu.py:516-639` |
| **B-106** | 🔴 **`SonucYazici` hiçbir ölçüm yolunda kurulmuyor** — tek kullanıcısı kendi birim testi | `03` sözleşme 5 · B5 *(bildirim ≠ kullanım)* | `sim/results.py:54` |
| **B-107** | 🔴 **`05` §E'nin beş zorunlu sonuç alanından yalnızca biri var.** B-46 beşten birini ekletti; kalan dördü aynı paragrafta duruyor | `03` sözleşme 5 · B5 *(şemanın kaybolması)* | `sim/kosucu.py:516` |
| **B-108** | 🔴 **K-024'ün "9528–18068 µs"si bugün üretilemiyor** *(min 8 768 · %16,15 altında · %54,94 üstünde, 35 282 çift)* ve **iki kaynak dosyasında olgu gibi** duruyor. 🟢 Kararı *(1 ms dilimde çakışma yok)* **birebir tutuyor** | `03` kural 1 · Y14 | `sim/config.py` · `sim/rng.py` yorumları |
| **B-109** | 🔴 **Li replikasyonu Li'nin ÇALIŞMA NOKTASINDA koşulmuyor** *(Li 2 Mbit/s, depo 1 Mbit/s)* ve bit hızı ne `08` KAPSAMAZ'da ne Ç4.3 duyarlılık taramasında var. 🟢 Li'nin noktasında **iki mutlak sayı da tutuyor** *(1,761 vs 1,7 · 0,277 vs 0,25 Mbps)* — hiç yazılmamış | `03` Bölüm D · B3 *(çalışma noktasını yazmamak)* | `v2/08` Ç4 · `dogrulama/li_duyarlilik.py` |
| **B-110** | 🔴 **%10'luk açığın adaylarının ÖLÇÜLEN üst sınırları yetmiyor:** EIFS **≤%0,49** · RTS/CTS **≤%4,99** · bit hızı **%1,1** · gereken **%10,1**. Ve RTS/CTS'in ters yönlü ikinci etkisi ölçülmedi | `03` B4 *(kusuru ölçmek onu sebep yapmaz)* | `v2/08` Ç4 KAPSAMAZ |
| **B-111** | 🔴 **Ç6.1 ve Ç6.3 iki yönde de kandırılabilir.** Gerçek davranış bozulup aynı dizgi **yoruma** konunca kriter GEÇİYOR; davranışı birebir aynı bir yeniden yazım kriteri DÜŞÜRÜYOR. B-09'un Ç6.2'de kapattığı sınıfın aynısı; B-89'un çözümü kapıya uygulanmamış | Y7 · B-09 sınıfı | `dogrulama/aile0_kapi_raporu.py:440` |
| **B-112** | 🟡 **B-83'ün kırpması, B-82'nin ölçüm yolundaki 8-bayt dalını ÖLDÜRDÜ** — 750 180 çağrının **0**'ında tetikleniyor. Deponun üç kez `assert`e çevirdiği sınıfın dördüncüsü | Y8 · *"tetiklenemeyen kontrol"* | `sim/gozlem.py:262` |
| **B-113** | 🔴 **`sag_kalan_ayikla.py` bugün hiçbir `sim/` mutantına "eşdeğer" diyemiyor.** B-46'nın eklediği `kaynak_hash` **her** hücreyi farklılaştırıyor; `esdeger`/`karar_yok`/`yolsuz` dalları **ulaşılamaz**. Yayımlanan çıktı *(20 Ağu, "7/7 eşdeğer")* B-46'dan bir gün önceye ait. Koruyan test *(`test_b52_*`)* bir **grep** — dalın **varlığını** doğruluyor, **ulaşılabilirliğini** değil | Y7 · Y14 · B-24 sınıfı | `dogrulama/sag_kalan_ayikla.py:305` |
| **B-114** | 🔴 **`08`in SEKİZ sayısı bugün üretilemiyor** *(§7)* — ve `08` **B-57 kapandığı için mühürlenmeye hazır** sayılıyor. Bu hâliyle mühürlenirse sekiz bayat sayı mührün içine girer | `03` kural 1 · Y14 | `v2/08` |
| **B-115** | 🔴 **Ön-kayıtlı kapının İKİ MÜHÜRLÜ PARAMETRESİNİ hiçbir test korumuyor.** `NULL_CEKIM_SAYISI` ve `tuz` `tests/` altında **hiç geçmiyor**; `test_b65_*` m=1 kullanıyor *(bilerek)*. Ölçüldü: m=5 → m=1 kapının nokta kestirimini **0,03372 → 0,02506** *(−%26)*; tuzu yok saymak 5 çekimi **birebir aynı** yapar *(bugün 5/5 ayrık)* | **Y12** *(K-060, 25 Ağu)* — bir gün sonra mühürlenen sabite uygulanmamış | `dogrulama/mekanizma_kapisi.py:61-62` |
| **B-116** | 🟡 **`alim_per`in `if ber >= 0.5: return 1.0` dalı TETİKLENEMEZ** — 3 232 691 çağrının **0**'ında. `bit_hata_orani` yalnızca `sinr_lineer <= 0` iken 0,5 döner; alınan güç sonlu mesafede **daima pozitif** | Y8 · *"tetiklenemeyen kontrol"* | `sim/mac.py:628` |
| **B-117** | 🔴 **ÜÇ MEKANİZMA BOŞLUĞU — 388 testin hiçbiri görmüyor** *(§8'den)*: parça parça SINR'ın tek parçaya inmesi **39/40 hücre** · meşgul bildiriminin CCA gecikmesi **38/40** · kanal diliminin 10 kat kabalaşması **40/40** | `03` B6 · Y2 | `sim/mac.py` · `sim/rng.py` |

---

## 5. 26 AĞUSTOS OTURUMUNUN 21 KAPANIŞI — doğrulama

### Y13 · Değişiklik KODDA mı — **21/21**

Y13 dördüncü denetimin 13 düzeltmesine uygulanmış ve 13/13 tutmuştu
*(K-061)*. Aynı ölçütü 26 Ağustos'un 21 kapanışına uyguladım: her bulgu için
düzeltmenin **koddaki izi** arandı.

| B-80 | B-81 | B-82 | B-83 | B-84 | B-85 | B-86 | B-87 | B-88 | B-89 | B-90 |
|---|---|---|---|---|---|---|---|---|---|---|
| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

| B-91 | B-92 | B-93 | B-94 | B-95 | B-96 | B-97 | B-98 | B-99 | B-57 |
|---|---|---|---|---|---|---|---|---|---|
| ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

> ⚖️ **İlk koşumda ikisi "EKSİK" çıktı ve ikisi de BENİM hatamdı** *(Y5:
> test kırılınca önce testin varsayımı denetlenir)*. B-80'de desen
> `"ESLEŞTİRİLMİŞ"` yazılmıştı, doğrusu `"EŞLEŞTİRİLMİŞ"`; B-94'te
> `"b94"` aranmıştı ama düzeltme `test_c2_2_pythonhashseed_den_bagimsiz`in
> **genişletilmesi** biçiminde yapılmış. Düzeltildi; **21/21**.

**Üretici:** `python scratchpad/y13_kapanis.py`

### 🟢 Bağımsız olarak yeniden ölçülen kapanışlar

| kapanış | iddia | benim ölçümüm | karar |
|---|---|---|---|
| **B-80** | DV kolu S2/orta/t1 kontrol payı **%13,71** · gözlem kolu %1,65–1,87 | **%13,710** · **%1,653** | 🟢 **TUTTU** |
| **B-82** | 200 000 rastgele yükte iki hesap FARKLI: **0** | 200 000 yük · 132 816 kabul · **0** | 🟢 **TUTTU** |
| **B-84** | ablasyon komşu **sırasını** koruyor | kodda: `for k in g.komsular` | 🟢 **TUTTU** |
| **B-94** | Ç2.2 ablasyon (`hash`) kolunu da koşuyor + aracın canlılığı ölçülüyor | kodda + bağımsız `PYTHONHASHSEED` ölçümü | 🟢 **TUTTU** |
| **B-57** | 70 kayıt · 28 üreticisiz · yeni boşluk yok | **70 · 28 · yok** | 🟢 **TUTTU** |
| **A-5** *(m=5 mührü)* | `tuz` XOR'u ile bağımsız çekim | 200 000 anahtar × 5 çekim: bağımsız referansla ayırt edilemez | 🟢 **TUTTU** |
| **Ç4.2** | plato **1/6,29** · GA **%2,04** | **1/6,29** · **%2,04** | 🟢 **TUTTU** |

### 🔴 Bir kapanışın DOĞURDUĞU iki yeni bulgu

`09`in kendi uyarısı: *"dördüncü denetimin 13 kapanışının **8'i** bir
sonraki bulguyu doğurdu."* Bu oturumda **iki** tane ölçtüm:

1. **B-57 ve B-93'ün kapanışı → B-100.** İkisinin de zorlayan testi
   `v2/` altındaki bir belgeyi okuyor; mutasyon paketi `v2/`yi kopyaya
   almıyor. **Kapı bu yüzden düşer.**
2. **B-83'ün kapanışı → B-82'nin ölçüm yolunda ÖLÜ DAL** *(B-112, aşağıda)*.

### 🔴 B-112 · B-83'ün kırpması, B-82'nin float dalını ÖLDÜRDÜ

`_olculen_deger_bayt` float için iki dal taşıyor *(4 bayt / 8 bayt)*. Ama
`_tasinan_bilgi_bayt` değerleri `yuku_dondur`dan okuyor ve `yuku_dondur`
her float'ı **tek duyarlığa kırpıyor** *(B-83)*. Kırpılmış bir float her
zaman sığar.

Ölçüldü — 200 000 rastgele yük:

| büyüklük | değer |
|---|---|
| `_olculen_deger_bayt` çağrısı | 750 180 |
| float **4 bayt** dalı | 355 150 |
| float **8 bayt** dalı | 🔴 **0** |

Deponun kendi kuralı *(`config.py`, `mac.py`, B-13/B-72/B-98'de üç kez
uygulandı)*: *"tetiklenemeyen bir kontrol, koruma sağlamadan koruma
İZLENİMİ verir."* Üç kez `assert`e çevrildi; **dördüncüsü fark edilmedi.**

⚠️ **Kapsamı dar tutuyorum:** B-82'nin öz-denetimi **ölmedi** —
`YUK_FLOAT_BAYT` 4'ten 2'ye indirilse ölçüm yolu yine 4 döner ve koruma
**konuşur**. Ölen şey yalnızca *"tel biçimine sığmayan bir değeri
yakalama"* yeteneğidir; kırpmadan sonra öyle bir değer **pencereye
ulaşamaz**.

**Üretici:** `python scratchpad/b83_olu_dal.py`

### 🔴 B-113 · `sag_kalan_ayikla.py` bugün "EŞDEĞER" DİYEMİYOR — karar kanalı SATÜRE

Bu, **üçüncü** denetimin kapanışının doğurduğu bir bulgu ve **iki denetim
boyunca görülmedi**.

B-46/K-051 *(21 Ağustos)* `sonuc()`e `"kaynak_hash": kaynak_hash()` ekledi.
`kaynak_hash()` **`sim/` altındaki tüm `.py` dosyalarının içeriğini**
hash'liyor. `sag_kalan_ayikla.py` ise her koşunun **TAM sonuç sözlüğünü**
tabanla karşılaştırıyor.

⇒ `sim/` altındaki **her** mutasyon `kaynak_hash`i değiştirir ⇒ her matris
hücresi farklı çıkar ⇒ `durum = "degisti"`. **`"esdeger"`, `"karar_yok"` ve
`"yolsuz"` dalları `sim/` mutasyonları için ULAŞILAMAZ.**

Ölçüldü — **aracın KENDİ `_kosu` ve `_imza` fonksiyonları** çağrıldı
*(matris süre için 44 → 2 koşuya küçültüldü; karşılaştırma mantığı aynen)*:

| aracın kendi listesinden mutant | 20 Ağu yayımlanan | bugün | farklı ALANLAR |
|---|---|---|---|
| `T01_parca_siniri_carpisma_kapali` | ⚪ eşdeğer | 🔴 **degisti** | `['kaynak_hash']` |
| `T03_assert_mesaji_metni` | ⚪ eşdeğer | 🔴 **degisti** | `['kaynak_hash']` |
| `T05_sonuc_dizini_olusturma` | ⚪ eşdeğer *(`yolsuz` beyanlı)* | 🔴 **degisti** | `['kaynak_hash']` |

**Üçünde de tek fark `kaynak_hash`.** Yayımlanan çıktı
*(`ciktilar/ayikla_cikti.txt`, 20 Ağustos, "7/7 eşdeğer")* B-46'dan **bir
gün önceye** ait ve araç o günden beri **hiç koşulmadı**.

🔴 **Ve onu koruyan test bir GREP:**

```python
def test_b52_YOLSUZ_beyani_esdeger_sayilmiyor():
    assert 'durum = "yolsuz"' in kaynak
    assert "m.yol is YOLSUZ" in kaynak
```

Dalın **var olduğunu** doğruluyor, **ulaşılabilir olduğunu** değil.
`03`ün *"tetiklenemeyen kontrol"* kuralı, korumanın kendisinde.

⚖️ **Bu bulgu benim kendi ölçümümü de düzeltti:** sağ kalan davranış
matrisimden `kaynak_hash`i **çıkarmak zorunda kaldım**; çıkarmasaydım
42 mutasyonun 42'si *"davranış değişti"* çıkardı.

**Üretici:** `python scratchpad/ayikla_kaynak_hash.py`

---

## 6. DOĞRULANAN İDDİALAR

| iddia | kaynak | benim ölçümüm |
|---|---|---|
| Test paketi **388** test, hepsi geçiyor | envanter | **388 passed in 876,61 sn** *(temiz taban)* |
| Test başına maliyet bandı **2,2196–2,5694 sn** | `mutasyon_paketi.OLCULEN_KOSULAR` | **2,259 sn/test** — bandın içinde |
| Li platosu **1/6,29** · GA **%2,04** | `08` Ç4 | **birebir** |
| Kontrol payı DV **%13,71** · gözlem **%1,65–1,87** | `08` madde 25 | **%13,710** · **%1,653** |
| `08` madde 22'nin **dokuz** `Gozlem` alanı | `08` | **dokuz, aynı isimler** ✅ *(ama toplam 11 — B-102)* |
| B-57: **28** üreticisiz kayıt · yeni boşluk yok | K-069 | **28** · yok |
| `_OLCUM` deseni fazla dar değil | K-069 | ölçüm taşımayan 10 kaydın 10'u tek tek okundu — **doğru** |
| Kör mutant havuzu **253** | envanter | **253** |
| `BEKLENEN_MUTASYON = 35` = liste uzunluğu | B-41 | **35 = 35** |
| Y13: kapanışlar kodda | Y13 | **21/21** |
| B-82: iki hesap 200 000 yükte hiç ayrışmıyor | K-062 | **0** |
| A-5: `tuz` çekimleri bağımsız | K-064 uyarısı | **bağımsız** *(uyarı kapatılabilir)* |
| `08` madde 21: istatistik katmanı YOK | `08` | `wilcoxon|holm|scipy` → **0 eşleşme** |
| K-017: 30/250'de 7/30 bağlı, bileşen 10–30 | K-017 *(üreticisiz)* | **7/30 · 10–30** ✅ |
| K-024'ün KARARI: 1 ms dilimde çakışma yok | K-024 *(üreticisiz)* | **0/35 282** ✅ |
| Y10/B-22 sınıfı kapalı | K-037 | tüm pakette **0** kırılamaz iddia |

---

## 7. ÜRETİLEMEYEN İDDİALAR

| iddia | nerede | bugün ölçülen |
|---|---|---|
| 🔴 **"Ardışık deneme başlangıçları arası 9528–18068 µs"** | K-024 · `sim/config.py` yorumu · `sim/rng.py` yorumu | min **8 768** · **%16,15** altında · **%54,94** üstünde *(35 282 çift)* |
| 🔴 **`08` "Madde sayısı: **25**" · "Beklenen çıktı: `25 True`" · "Numaralar 1–25"** | `08` §BU ARAÇ NELERİ YAPMAZ | `08`in **kendi üretici komutu**: **`30 True`** |
| 🔴 **`08` "Ç5 bugün **18** test"** | `08` Ç5 | **52** |
| 🔴 **`08` "Son kapı koşusu: **21 Ağustos** · 98,2 dk (K-054)" · "üç denetim bitti" · "**22** maddelik sınır listesi"** | `08` başlık bloğu | son koşu **25 Ağu · 150,2 dk (K-059)** · **beş** denetim · **30** madde |
| 🔴 **`08` §KAPANIŞ ÖN KOŞULLARI: "B-57 … 55 kaydın 25'inde" (⬜ açık)** | `08` madde 13 | B-57 **26 Ağu kapandı**; sayı **70 kaydın 28'i** |
| 🔴 **`08` madde 30: "en pahalı tek test **45,7 sn** … **17,8 kat**"** | `08` madde 30 *(A-10)* | **118,23 sn** *(`test_b65_mekanizma_kapisi_ESLESTIRILMIS_ablasyona_karsi`)* — ortalamanın **~52 katı**; 45,7 sn'yi aşan **üç** test var |
| 🔴 **`08` §KÖR MUTASYON: "havuz **203** · 179 mutant hiç sınanmadı · örneklem 24/203"** | `08` | havuz **253** → sınanmayan **229** |
| 🔴 **README / envanter: "**69** karar kaydı"** | `README.md` · altıncı denetim promptu | aracın kendi çıktısı: **70** *(K-070 eklendi, sayı güncellenmedi)* |
| 🟡 **`08` madde 22: "DOKUZ alan"** | `08` | **onbir** *(9 `Gozlem` + 2 `KomsuKaydi`)* |
| 🟡 **`ciktilar/ayikla_cikti.txt`: "7/7 eşdeğer"** | 20 Ağu çıktısı | bugün araç **hiçbirine** "eşdeğer" diyemiyor *(B-113)* |

> ⚖️ Bunların **hiçbiri kod hatası değil.** Hepsi Y14'ün tarifi: *"bir kod
> düzeltmesi, ondan önce ölçülmüş HER SAYIYI şüpheli yapar."* Ve `08`
> **B-57 kapandığı için mühürlenmeye hazır** sayılıyor — bu hâliyle
> mühürlenirse **sekiz bayat sayı mührün içine girer.**

---

## 8. 🔴 KENDİ MUTASYONLARIM — KATMANLI

### Yöntem

**42 mutasyon**, iki fazlı, `Pool(8)`, **67,8 dk duvar süresi**. Her mutant
kendi `tempfile.mkdtemp()` kopyasında; **asıl depo hiç değişmedi.**

| faz | dosyalar | ölçülen süre |
|---|---|---|
| 1 | 12 **ucuz/orta** test dosyası | ~180 sn *(Pool(8) çekişmeli)* |
| 2 | 5 **pahalı** test dosyası | ~1 230 sn |

🔴 **Y7 — araç ne koştuğunu kendisi doğruluyor:** koşu başında
`faz1 ∪ faz2 == tests/ altındaki tüm dosyalar` **assert** ediliyor
*(çıktı: "faz1+faz2 = 17 dosya = tests/ TAMAMI ✅")*. İkisi de geçen bir
mutant **388 testin tamamından** sağ çıkmıştır.

**Taban temiz:** `388 passed in 876,61 sn` *(mutasyon kampanyasından önce,
asıl depoda)*.

**Katman tanımı** *(promptun tanımı birebir)*: **M** = fizik · MAC durum
makinesi · yönlendirme kararı · zamanlama · **S** = sonuç sözlüğüne giren
büyüklük · gözlem penceresi alanı · kapı ölçütü.

🔴 **AYRIKLIK (D-2 uyarısı):** **M ∪ S = 22 + 20 = 42 = toplam**, **M ∩ S = 0**.
İkisi **ayrık ve tüketici**; hiçbir mutasyon iki kez sayılmıyor.
**26 Ağustos kodu (A)** bir **çapraz kesen ALT KÜMEDİR**, ayrı bir katman
değil: **A ∩ M = 2 · A ∩ S = 13 · |A| = 15.** Örtüşme rakamla yazıldı.

### 🔴 KATMAN TABLOSU

*(Tek örneklem binom · **tek yönlü** · α = 0,05 · **TAM binom** · H0: p = 0,70 ·
%95 GA **Clopper–Pearson**. Promptun güç tablosu `scipy` ile **bağımsız
olarak yeniden üretildi: beş satırın beşi de birebir tuttu.**)*

| katman | sağ kalan | oran | %95 GA | red bölgesi | **ULAŞILAN GÜÇ** *(p₁=0,40)* | güç *(p₁=0,50)* | n ≥ 19? | H0 = 0,70 |
|---|---|---|---|---|---|---|---|---|
| 🔴 **MEKANİZMA** | **7/22** | **%31,8** | **[0,139 · 0,549]** | X ≤ 11 | **0,879** | 0,584 | ✅ **EVET** | **REDDEDİLDİ** *(p = 2,5×10⁻⁴)* |
| **SAYAÇ / RAPORLAMA** | **3/20** | **%15,0** | [0,032 · 0,379] | X ≤ 10 | **0,872** | 0,588 | ✅ EVET | **REDDEDİLDİ** *(p = 5,4×10⁻⁷)* |
| **26 AĞUSTOS KODU** *(alt küme)* | **4/15** | %26,7 | [0,078 · 0,551] | X ≤ 6 | 0,610 | 0,304 | 🔴 **HAYIR** | reddedildi *(p = 6,7×10⁻⁴)* |
| **GENEL** | **10/42** | **%23,8** | [0,121 · 0,395] | X ≤ 23 | **0,982** | 0,780 | ✅ EVET | **REDDEDİLDİ** *(p = 8,8×10⁻¹⁰)* |

🟢 **MEKANİZMA KATMANI ALTI DENETİMDE İLK KEZ YETERLİ GÜÇLE ÖLÇÜLDÜ**
*(n = 22 ≥ 19, güç 0,879; önceki en iyisi n = 9, güç 0,483)* ve H0 = 0,70
**reddedildi.**

🔴 **AMA "KAPANDI" YAZILAMAZ — ve sebebi eşik değil, GA:** mekanizma
katmanının %95 GA'sı **[0,139 · 0,549]**. Gerçek oran **%55'e kadar**
olabilir. Nokta kestirimi %31,8, dördüncü denetimin genel %25,0'ından
**yüksek**.

⚠️ **26 Ağustos alt kümesi için "kapandı" YAZILAMAZ** — n = 15 < 19,
güç 0,610 *(promptun 5. şartı)*. Promptun 3. şartı **≥10** mutasyondu:
**15** yazıldı, ama *"kapandı"* eşiği ayrı bir eşiktir.

### Seri

**%80,0 → %70,0 → %66,7 → %25,0 → %31,4 → %23,8**

⚠️ **Bu seri KARŞILAŞTIRILABİLİR DEĞİL ve bunu yazıyorum.** Altı örneklem
altı farklı yöntemle seçildi; benimki **kasten katmanlı** ve **kasten 26
Ağustos koduna ağırlıklı**. `08`in kör tarama için yazdığı uyarı burada da
geçerli: *"iki skor karşılaştırılamaz; ilerleme ölçüsü değildir."*
Söylenebilecek olan, **katman başına GA'nın daraldığıdır.**

### 🔴 Y8 ÖN KOŞULU — bozulan yol sağlam koşuda tetikleniyor mu

Katalogda her mutasyonun yanında **tetiklenme kanıtı** yazılı. Üç tanesini
**doğrudan ölçtüm**, çünkü sonuçları kararı değiştirdi:

| mutasyon | tetiklenme ölçümü | sonuç |
|---|---|---|
| **M06** | `bit_hata_orani` **3 232 691** çağrı · `ber == 0.5` **0** · `ber > 0.5` **0** | 🔴 **yol TETİKLENEMEZ** → B-116 |
| **M12** | `_iletim_bitir` **585 768** çağrı · aktif listede ≥2 iletim **481 758** *(%82)* · `==` ama `is` değil **0** | ✅ yol tetikleniyor, **fark noktası yok** |
| **A07** | B-98'in kendi ölçümü: `dogum_s > bit` olan paket **0/60** | ✅ beyan edilmiş, **beklenen sağ kalan** |

### 🔴 SAĞ KALANLARIN DAVRANIŞI — 5 KOL × 8 YAPILANDIRMA

**40 tam koşu × 47 alan/koşu**, taban dâhil **11 matris = 440 tam koşu**.
🔴 `kaynak_hash` karşılaştırma dışı — **B-113'ün tuzağı**; içeride
bırakılsaydı 42 mutasyonun 42'si *"davranış değişti"* çıkardı.

| # | sağ kalan | katman | farklı hücre | **karar** |
|---|---|---|---|---|
| 1 | **M07** parça parça SINR → tek parça | M | **39/40** | 🔴 **DAVRANIŞ DEĞİŞTİ** |
| 2 | **M14** meşgul bildirimi anında *(CCA = 0)* | M | **38/40** | 🔴 **DAVRANIŞ DEĞİŞTİ** |
| 3 | **M25** kanal dilimi 10 kat kaba | M | **40/40** | 🔴 **DAVRANIŞ DEĞİŞTİ** |
| 4 | **M06** BER doyma eşiği sınırda | M | 0/40 | ⚪ **EŞDEĞER** *(yol tetiklenemez — B-116)* |
| 5 | **M11** alım/iletim sırası ters | M | 0/40 | ⚪ **EŞDEĞER** *(kod yorumunun iddia ettiği etki gözlenmiyor)* |
| 6 | **M12** `is` → `==` | M | 0/40 | ⚪ **EŞDEĞER** *(481 758 çağrıda 0 fark noktası)* |
| 7 | **A02** ölçüm yolu hep 4 bayt | S/A | 0/40 | ⚪ **EŞDEĞER** *(dal ölü — 750 180 çağrıda 0, B-112)* |
| 8 | **A07** pencere üst sınır değişmezi | S/A | 0/40 | 🟡 **YOL TETİKLENMİYOR** *(0/60, B-98'in beyanı)* |
| 9 | **A09** ablasyon tuzu yok sayılıyor | M/A | 0/40 | 🔴 **TÜKETİCİSİ BU MATRİSTE YOK** ↓ |
| 10 | **A10** m = 5 → m = 1 | S/A | 0/40 | 🔴 **TÜKETİCİSİ BU MATRİSTE YOK** ↓ |

🔴 **A09 ve A10 için "EŞDEĞER" DEMEK YANLIŞ OLUR** *(B-36/B-52'nin kendi
kuralı)*. İkisinin de tek tüketicisi `dogrulama/mekanizma_kapisi.py`; o
tüketici **doğrudan ölçüldü** *(4 tohum × 6 koşu = 24 tam koşu)*:

| | m = 1 | m = 5 *(mühürlü)* |
|---|---|---|
| eşleştirilmiş fark *(ort)* | **0,02506** | **0,03372** |
| std *(tohumlar arası)* | 0,02012 | 0,02814 |

- **A10** kapının nokta kestirimini **%26 kaydırıyor** — ve hiçbir test görmüyor.
- **A09**: `tuz = 0…4` bugün **5/5 ayrık** çekim veriyor *(çekim std
  0,00705–0,02805)*; tuzu yok saymak beşini **birebir aynı** yapar, yani
  m = 5 ortalaması sessizce m = 1'e döner. Hiçbir test görmüyor.

⚠️ **4 tohum, kapının 8'i değil** — bu sayılar kapının sayıları DEĞİLDİR;
yönü ve büyüklük mertebesini gösterirler.

### 🔴 ÜÇ MEKANİZMA BOŞLUĞU — 388 test görmüyor *(B-117)*

| mutasyon | ne bozuyor | neden hiçbir test görmüyor |
|---|---|---|
| **M07** `noktalar = self._parca_sinirlari(il)` → `[baslangic, bitis]` | Girişim, çerçeve boyunca **sabit** varsayılıyor; darbeli karıştırıcının açma/kapama sınırları kayboluyor | **Ç3.2** *(parça parça SINR = tek parça)* tam olarak bu eşitliği test ediyor — ama **SABİT girişimde**. Darbeli senaryoda ikisi ayrışır ve o eksende test yok |
| **M14** `gecikmeyle_ekle(cca_s, …)` → `gecikmeyle_ekle(0.0, …)` | Aynı slotta geri sayımı biten iki düğüm **asla çarpışmaz** | `cca_s` sabitini koruyan test var *(`test_cca_ayni_slot_carpismasini_uretiyor`, mutasyon M3)*, ama o sabiti **sıfırlamayı** yakalıyor; **bildirim gecikmesi yolunu** değil |
| **M25** `int(zaman_s // dilim_s)` → `int(zaman_s // (dilim_s*10))` | Kanal dilimi 10 kat kabalaşıyor; ardışık denemeler aynı çekimi paylaşabilir | **Ç6.2**'nin marj değişmezi `Konfig.kanal_dilimi_s`ten **analitik** hesap yapıyor; `kanal_cekimi`in **içindeki bölene** bakmıyor. Konfig değeri değişmediği için değişmez susuyor |

⚖️ Üçü de `03` B6'nın *"kod doğru, testler geçiyor, kapsam yüksek — ve
kurulum yanlış"* sınıfında: hiçbiri sonuç sözlüğünü **kırmıyor**, hepsi
**kaydırıyor**.

### Örneklem seçimi — beyan

Mutasyonlar **kodu okuyarak** seçildi, mevcut testlerden değil; ama seçici
**benim** ve seçim yanlılığı sıfır değil. Somut yön: 26 Ağustos koduna
**kasten** ağırlık verdim *(15/42)*, çünkü prompt onu av sahası ilan etti.
Bu, genel oranı 26 Ağustos kodunun oranına *(%26,7)* doğru çeker.
**Katman oranları bu yanlılıktan bağımsızdır** — M ve S ayrı sayıldı.

### ⚠️ Bir yakalama SAHTE ÇIKABİLİRDİ — ölçtüm

**M10** ilk turda `test_b93_sim_altindaki_ASSERT_sayisi_BEYANLA_ayni` ile
"yakalandı" göründü. O test `sim/` altındaki `assert`lerin **(dosya, SATIR)**
kümesini beyanla karşılaştırıyor; M10 bir satırı ikiye böldüğü için
`mac.py:546` ve `:666` **kaydı** — yani yakalama **davranışsal değil,
defter tutmaydı** *(Y8'in tam tersi)*.

Ölçtüm: `sim/` satır sayısını değiştiren **5** mutasyon var; **yalnızca
M10** bu şekilde yakalanmıştı. M10 `test_b93` **hariç** tüm pakette yeniden
koşuldu *(18,7 dk)*:

```
1 failed, 385 passed, 1 skipped, 1 deselected
kirilan : tests/test_kosucu.py::test_b54_en_yuksek_doluluk_BAGIMSIZ_gozlemle_ayni
KARAR   : YAKALANDI
```

🟢 **M10 gerçek bir yakalamadır** ve katman tablosu değişmiyor.
🟡 **Ama gözlem duruyor:** `test_b93` `sim/` satır numaralarına duyarlıdır
ve satır kaydıran her mutasyonda **evrensel kırıcı** gibi davranır. Kapının
Ç1.3 ölçütü bundan korunuyor *(3. koşul `beklenen_test`in kırılmasını
istiyor)*; ama bir mutasyon kampanyasının ham *"yakalandı"* sayısı korunmuyor.

---

## 9. ŞÜPHE LİSTESİ SONUÇLARI

| # | şüphe | sonuç |
|---|---|---|
| **1** | Sözleşme 5 — *"sonuç + konfigürasyon birlikte"* | 🔴 **SAĞLANMIYOR.** `SonucYazici` hiç kurulmuyor *(B-106)*; `05` §E'nin beş alanından biri var *(B-107)*. A-8'in alt sözlük şemaları ölçüldü ve yazıldı |
| **2** | Literatür replikasyonu — %10 gerekçelendirildi mi | 🔴 **ATFEDİLDİ, ölçülmedi.** Üç adayın üst sınırı ölçüldü: bit hızı %1,1 · EIFS ≤%0,49 · RTS/CTS ≤%4,99; gereken **%10,1** *(B-109 · B-110)*. Ayrıca replikasyon **Li'nin çalışma noktasında koşulmuyor** ve bu beyan edilmiyor |
| **3** | Mekanizma katmanı — yeterli güç | 🟢 **İLK KEZ YETERLİ GÜÇLE ÖLÇÜLDÜ** — n = 22 ≥ 19, güç **0,879**, H0 = 0,70 **reddedildi** *(p = 2,5×10⁻⁴)*. 🔴 Ama GA **[0,139 · 0,549]** → *"kapandı"* yazılamaz. **Üç sağ kalan davranışı değiştiriyor ve 388 test görmüyor** *(B-117)* |
| **4** | A-5'in kalan yüzü — `Akislar` dışındaki RNG | 🔴 **İhlal var, BEYAN YOK** *(B-103)*. 🟢 Ama üç ölçümün üçü de zararsız çıktı: belirlenimci · çekimler bağımsız · tohumlar arası anahtar örtüşmesi **%0,000** |
| **5** | A-7 — pencerenin iki ucunda farklı kapalılık | 🟡 Bugün **ölçü sıfır**; 🔴 ama **S5'te dilimler pencerenin %6,9'unu dışlıyor** ve bu `08`de yok. Asıl mesele daha büyük: sayaçların yarısı **tüm koşudan** *(B-105)* |
| **6** | Kapı koşulmadı — koşarsa 13/13 gelir mi | 🔴 **GELMEZ.** Aracın kendi taban kontrolü koşuldu: **3 kırık** → Ç1.3 `!!TABAN` *(B-100)*. Kapının tamamı koşulmadı *(öğrenci kararı: sebep zaten ölçüldü)* |
| **7** | `06` 26 Eylül'de donuyor — hazır mı | 🟡 **m = 5 mührü sağlam** *(A-5'in uyarısı ölçümle kapatılabilir)*. 🔴 Ama `06`nın dayandığı iki şey eksik: **istatistik katmanı yok** *(`wilcoxon|holm|scipy` → 0 eşleşme)* ve **null modelin RNG'si beyan edilmemiş** *(B-103)* |
| **8** | `08`in 30 maddesi — iki yönlü | 🔴 **Sekiz bayat sayı** *(§7)*. 🔴 **Beş yeni madde önerisi** *(§10)*. *(a)* yönünde ihlal bulunamadı: *"yapmaz"* denen bir şeyin yapıldığı bir vaka çıkmadı |
| **9** | 28 üreticisiz kayıt — bugün üretilebilir mi | İkisi denendi: **K-017 birebir tuttu** · **K-024'ün SAYISI tutmadı, KARARI tuttu** *(B-108)*. Örneklem 2/28 — kalan 26 **ölçülmedi** ve bu bir eksikliktir |
| **10** | Beş denetimin kapanışları birbirini bozdu mu | 🔴 **EVET, üç kez ölçüldü:** B-57+B-93 → **B-100** · B-83 → **B-112** · B-46 → **B-113** |
| **11** | Bu promptun kendisi — neye bakmamı istemiyor | 🔴 **Aşağıda** |

### 🔴 11 · PROMPTUN LİSTESİNDE OLMAYAN YERLER

Prompt **`sim/`e ve beşinci denetimin bulgularına** odaklıyor. Listede
**olmayan** ve en pahalı üç bulgu oradan çıkmadı:

| bulgu | prompt onu istedi mi |
|---|---|
| **B-100** *(kapı bugün düşer — `v2/` kopyalanmıyor)* | ❌ Prompt *"kapı koşulmadı"* diyor ama **niçin düşeceğini** sormuyor; ucuz bir taban koşusuyla ölçülebileceğini de söylemiyor |
| **B-113** *(`sag_kalan_ayikla.py`nin karar kanalı satüre)* | ❌ Prompt `sag_kalan_ayikla.py`yi hiç anmıyor. Beşinci denetimin listesinde de yok |
| **B-105** *(sayaçların yarısı tüm koşudan)* | ❌ Prompt sözleşme 4 için **yalnızca A-7'yi** *(uç kapalılığı)* ve B-98'i işaret ediyor — ikisi de **ölçü sıfır** etkiler. Asıl ihlal **%17,89–22,79**'luk pencere dışı sayım |

⚖️ **Örüntü:** prompt **`sim/` altındaki mekanizmayı** denetletiyor;
üç bulgunun üçü de **`dogrulama/` altındaki ÖLÇÜM ARACINDA**. Aracın
kendisi, aracın denetlediği şeyden daha az denetlenmiş.

---

## 10. KAPSAM BEYANINA EKLENECEKLER

### `08`de DÜZELTİLECEK sekiz sayı *(§7)*

Madde sayısı **25 → 30** *(ve "Beklenen çıktı: `30 True`")* · Ç5 **18 → 52** ·
başlık bloğu *(üç → beş denetim; son kapı **25 Ağu, 150,2 dk, K-059**;
**22 → 30** maddelik liste)* · §KAPANIŞ ÖN KOŞULLARI madde 13 *(B-57
kapandı, **70 kaydın 28'i**)* · madde 30 *(en pahalı test **118,23 sn**)* ·
kör havuz **203 → 253** *(sınanmayan **229**)* · madde 22 *(**onbir** alan)* ·
`ciktilar/ayikla_cikti.txt` **BAYAT** işaretlenmeli *(B-113)*.

### Yeni madde önerileri — 31 … 35

| # | öneri | yön |
|---|---|---|
| **31** | 🆕 **Sonuç sözlüğü İKİ AYRI PENCEREDEN sayıyor.** Teslim/gecikme `[isinma_s, olcum_bitis_s]`; kontrol · veri · MAC · beacon · olay sayaçları **`[0, kosu_bitis_s]`**. Ölçüldü *(5 kol × 8 yapılandırma)*: kontrol baytının **%17,89–22,79'u** pencere dışında; kontrol payı **1,010–1,094×** şişik ve **çarpıklık kola göre değişiyor** | 🔴 `08` madde 25'in **bağlayıcı** oranını doğrudan etkiler. `03` Bölüm C sözleşme 4 ihlali |
| **32** | 🆕 **`Kosu.sonuc()` korunum denklemini TAŞIMIYOR** ve `kostur()` `defter.kontrol()`u hiç çağırmıyor. 113 `Kosu(` çağrı yerinin 15'i kontrol ediyor; **`mekanizma_kapisi.py`nin 48 koşusu etmiyor** | 🔴 `03` sözleşme 3 + `05` §E zorunlu alanı. **Sonradan eklenemez** — şema Aile 1 başlayınca donuyor |
| **33** | 🆕 **`05` §E'nin beş zorunlu sonuç alanından dördü yok** *(konfigürasyon · tohum · korunum · ölçüm penceresi)*; `SonucYazici` hiçbir ölçüm yolunda kurulmuyor | 🔴 Aylar sonra *"bu sayı hangi parametrelerle çıktı"* sorusu **hash'ten geri çözülemez** |
| **34** | 🆕 **Ön-kayıtlı kapının null modeli `Akislar` dışında `random.Random(hash(...))` kullanıyor.** Bugün belirlenimci *(tamsayı demeti)* ve çekimler bağımsız — **ölçüldü**; ama anahtar bir gün **dizgi** taşırsa `PYTHONHASHSEED`e bağlı olur | 🟡 `07`nin *"liste kapalıdır"* cümlesi bu hâliyle **yanlış**. İstisna yalnızca bir test docstring'inde yazılı |
| **35** | 🆕 **Paylaşım taraması `_TARAMA_DERINLIGI = 3`** — elle seçilmiş, ölçümden türetilmemiş. Derinlik ≥4'teki düğümler arası yazılabilir kanal **görünmüyor** *(8/8 yapılandırma)* ve **sonucu değiştiriyor** *(teslim farkı −0,0149…+0,2040)* | 🔴 `03` kural 5 · `08:194`ün dört kanal beyanının **derinlik ekseni** yazılı değil |

### `06`ya eklenecek *(26 Eylül mühründen ÖNCE)*

- 🟢 **A-5'in uyarısı kapatılabilir**: *"tuz düşük bitlere XOR'landı"* — ölçüldü, çekimler bağımsız. Yerine **ölçülmüş sınır** yazılmalı: ablasyon **k ≤ 3** olan kararların **%11,73'ünde** m=5'in çoğu çekimi çakışır *(k=1'de ablasyon birim permütasyon)*.
- 🔴 **Null modelin RNG'si `03` sözleşme 2'nin dışında** — beyan edilmeli.

---

## 11. 🔴 ANLAŞILMAYANLAR

> Bu bölüm boş bırakılamaz. Beş denetimde de buradan **gerçek kusur** çıktı
> *(A-4 bir kâhin kanalıydı; A-5 ön-kayıtlı kapının varyansını değiştirdi)*.
> Aşağıdakiler **bulgu değil**: ölçemediğim ya da niyetini
> çözemediğim şeyler. Numaralar **A-11**'den devam ediyor.

### 🔴 A-11 · `Konfig` "frozen" ama BİR ALANI DEĞİL

`sim/config.py` docstring'i: *"Nesne dondurulmuştur (frozen): bir koşu
başladıktan sonra konfigürasyon **değiştirilemez.** Bu kasıtlıdır — koşu
ortasında değişen bir parametre, sonuç satırındaki konfigürasyonu **yalancı**
yapar."*

Ölçüldü:

```
frozen mi                          : True
kon.tohum = 5                      : FrozenInstanceError   ✅
kon.aktif_cift_sayisi['orta'] = 999 : BAŞARILI             🔴
sozluk() değeri                     : {'yogun': 20, 'orta': 999, 'seyrek': 4}
```

`aktif_cift_sayisi` bir **`dict`** alanıdır; `frozen=True` yalnızca
**öznitelik atamasını** engeller, **içerik değişimini** engellemez. Ve
`sozluk()` → `kurulum_hash` → sonuç satırı zincirinin tamamı bu değere
bağlı.

🟢 **Sızıntı YOK:** `default_factory` her örneğe **yeni** bir sözlük veriyor
*(ölçüldü — yeni bir `Konfig` hâlâ 10 veriyor)* ve alan **tek yerde**
okunuyor *(`Konfig.aktif_cift`)*. Bugün hiçbir kod onu değiştirmiyor.

🔴 **Anlayamadığım:** bu bilinçli bir kabul mü, yoksa fark edilmemiş mi?
`Konfig`in **her diğer** demet alanı *(`karistirici_konum`,
`ara_bolge_per_bandi`)* değişmez tipte seçilmiş — yani desen biliniyor.
Bir `MappingProxyType` ya da demet-çifti bu deliği kapatırdı. Hiçbir test
donmuşluğu sınamıyor *(`FrozenInstanceError` depoda hiç geçmiyor)*.

> ⚖️ **Bulgu diye yazmadım** çünkü `03` B5'in ölçütü *"bildirim ≠ kullanım"*:
> burada bildirim var, **kötüye kullanım yok**. Ama `03` kural 14'ün
> *"durum tutan yeni bir bileşen"* uyarısı Aile 1'de bir protokol
> `kon.aktif_cift_sayisi`e dokunursa **hiçbir test konuşmaz**.

### 🔴 A-12 · `_T_975_7 = 2.365` — İKİ dosyada, hiçbir test bağlamıyor

Sabit **iki yerde** duruyor:

```
dogrulama/mekanizma_kapisi.py:62   _T_975_7 = 2.365
tests/test_mekanizma_kapisi.py:568 _T_975_7 = 2.365
```

Doğruluğunu ölçtüm: `scipy.stats.t.ppf(0.975, 7) = 2.3646` ✅.

🔴 **İki şeyi anlamadım:**

1. **Neden iki kopya?** Y12 *("elle tutulan her kapı sabiti ucuz bir testle
   korunur")* ve B-07'nin *"ikinci doğru kaynağı"* dersi tam olarak bunu
   yasaklıyor. `KAPI_TOHUMLARI` 8'den 10'a çıkarılırsa serbestlik derecesi
   9 olur *(t = 2,262)* ve **iki kopyanın biri güncellenip diğeri
   unutulabilir.** Hiçbir test ikisini bağlamıyor.
2. **Etiket ile istatistik uyuşmuyor.** Kapı **yalnızca alt sınıra** bakıyor
   *(`ga_alt > 0`)*, yani fiilen **tek yönlü** bir testtir; 2,365 kullanmak
   tek yönlü **α = 0,025** demektir. `06` ise *"%95 güven aralığı"* diyor.
   Tek yönlü %95 olsaydı sabit **1,895** olurdu. Yön **güvenli tarafta**
   *(daha sıkı)*, ama `06`nın cümlesi bu hâliyle testi **olduğundan gevşek**
   tarif ediyor. Bunun bilinçli bir muhafazakârlık mı yoksa bir etiket
   kayması mı olduğunu belirleyemedim.

### 🟡 A-13 · Ç1 matrisinin korunum kontrolü nereye kadar "otomatik"

`03` sözleşme 3'ün *"her koşuda otomatik"* ifadesini **iki türlü** okudum:
*(a)* her `Kosu` nesnesi kendi korunumunu doğrular, *(b)* her ÖLÇÜM
matrisinde doğrulanır. Kod *(b)*'yi bile tam yapmıyor *(B-104)*, ama
*(a)*'nın kastedildiğini **kesin olarak** söyleyemem. `05` §E'nin
*"korunum denklemi sonucu"*nu **zorunlu sonuç alanı** sayması *(a)*'ya
işaret ediyor; ben raporu ona göre yazdım. **Yanılıyorsam B-104'ün
şiddeti düşer, varlığı düşmez** — alan yine de `05` §E'de zorunlu.

### 🟡 A-14 · `sim/karsilastirma.py` denetlenmedi

Aile 1'in her gecikme karşılaştırması bu dosyadan geçecek *(`08` madde 16)*
ve bu denetimde **yalnızca `kaynak_hash` kontrolüne** baktım *(doğru
çalışıyor: iki farklı kod sürümü reddediliyor)*. 322 satırın geri kalanı —
ortak alt küme, kesişim oranı, NaN reddi — **açılmadı.** Beşinci denetim de
açmamıştı. Bu, Aile 1'e giden yolda **denetlenmemiş en büyük tek dosyadır.**

### 🟡 A-15 · Kör mutant havuzu 253 — 24'ü örnekleniyor, gerisi hakkında hiçbir şey bilinmiyor

`08` *"179 mutant hiç sınanmadı"* diyor *(203 havuza göre)*; bugün havuz
**253**, yani sınanmayan **229**. Havuzun büyümesi kodun büyümesiyle
otomatik. 🔴 **Anlamadığım:** `kor_mutasyon.py` bir kapı **değil** ve
öyle de yazılmış — ama o zaman **skorun ne işe yaradığı** yazılı değil.
İki tarih arasındaki skor `08`in kendi beyanıyla **karşılaştırılamaz**
*(örneklem tamamen değişiyor)*. Karşılaştırılamayan ve kapı olmayan bir
sayının rolünü çözemedim.

### 🟡 A-16 · S5'te dışlanan %6,9

`_yakinsama_dilimleri` hareketli karıştırıcıda **tam yörünge** dilimleri
kesip artanı dışlıyor — gerekçesi kodda yazılı ve ikna edici *(kısmi bir
yörünge tam yörüngelerle karşılaştırılamaz)*. 🔴 **Anlamadığım:** aynı
koşuda `teslim_orani` **tüm 270 s**'den hesaplanıyor. Yani S5'te
*"yakınsadı"* yargısı ile *"teslim oranı"* **farklı zaman aralıklarına**
ait. Bu bilinçli bir ayrım mı, yoksa `03`ün *"tüm sayaçlar aynı
pencereden"* şartının farkında olunmadan kırıldığı bir yer mi —
belirleyemedim. Ölçtüm: 270 s pencerenin **251,33 s**'si dilimlenmiş,
**18,67 s** dışarıda.

---

## 12. KOŞTURDUĞUM KOMUTLAR

Hepsi **depo kökünden** koşuldu. `PYTHONIOENCODING=utf-8` her koşuda ayarlı.
`scratchpad/…` yolları bu oturumda yazılan geçici betiklerdir; **depoya
hiçbiri kopyalanmadı** ve içerikleri raporun ilgili bölümlerinde tarif
edilmiştir.

### Depodaki araçlar — olduğu gibi

| komut | süre | sonuç |
|---|---|---|
| `python -m pytest tests -q --tb=short -p no:cacheprovider` | **876,61 sn** | **388 passed** *(temiz taban)* |
| `python -m pytest tests/test_gozlem.py --collect-only -q` | 0,1 sn | **52 tests collected** |
| `python dogrulama/karar_kaydi_denetimi.py` | anlık | 70 kayıt · 60 ölçüm · **28 üreticisiz** · yeni boşluk yok |
| `python -c "…from dogrulama.kor_mutasyon import mutantlari_uret…"` | anlık | havuz **253** |
| `python -c "…from dogrulama.mutasyon_paketi import taban_kontrolu…"` | **14,2 dk** | 🔴 **False — 3 failed, 385 passed** |
| `python -c "…from dogrulama.aile0_kapi_raporu import KAPI_SECIMLERI…"` | anlık | Ç2 6 · Ç3 44 · Ç5 52 · Ç4.1 6 · Ç6.2 2 · BEKLENEN_MUTASYON 35 = liste 35 |
| **`08`in kendi madde-sayısı komutu** *(belgeden kopyalandı)* | anlık | 🔴 **`30 True`** *(belge `25 True` bekliyor)* |
| **`08` madde 24'ün kendi üretici komutu** | anlık | 🟢 **`9 1025 3 4 0`** — beyanla birebir |
| **B-100 üreticisi** *(§0'da tam metin)* | **19 sn** | 🔴 3 failed, 42 passed |

### Bu oturumda yazılan ölçüm betikleri

| betik | ne ölçtü | süre |
|---|---|---|
| `scratchpad/pencere_sayaclari.py` | **Sözleşme 4** — pencere içi / tüm koşu, 5 kol × 8 yapılandırma = **40 tam koşu** | ~5 dk |
| `scratchpad/li_bithizi.py` | Li platosu, **4 bit hızı** × 30 tohum × 2 uzunluk = **240 zincir koşusu** | ~2 dk |
| `scratchpad/li_eifs.py` | EIFS üst sınırı *(çözülemeyen alım oranı ölçülerek)* | ~1 dk |
| `scratchpad/li_rtscts.py` | RTS/CTS ek yükü *(analitik, `Konfig` sabitlerinden)* | anlık |
| `scratchpad/kanit_v2.py` · `kanit_taban.py` · `kanit_taban3.py` | **B-100** — üç kırık testin adı ve sebebi | 19 sn + 14,2 dk |
| `scratchpad/dosya_sureleri.py` | **`08` madde 30 / A-10** — dosya başına süre + `--durations` | 7,3 dk |
| `scratchpad/y13_kapanis.py` | **Y13** — 21 kapanışın koddaki izi | anlık |
| `scratchpad/c6_kandirma.py` | **Ç6.1/Ç6.3** dört kandırma denemesi | anlık |
| `scratchpad/madde22.py` | **`08` madde 22** — tüketicisiz alan sayımı | anlık |
| `scratchpad/a5_hashseed.py` | `hash()` × 3 `PYTHONHASHSEED` | anlık |
| `scratchpad/a5_tuz.py` | `tuz` bağımsızlığı — 200 000 anahtar × 5 çekim × 6 k değeri | ~2 dk |
| `scratchpad/a5_anahtar.py` | ablasyon anahtar yapısı — **8 tam koşu**, 449 498 karar | ~2 dk |
| `scratchpad/b86_derinlik.py` · `b86_kanal_etkisi.py` | **B-101** — derinlik taraması + kontrol kolu, 8 yapılandırma × 2 kol | ~4 dk |
| `scratchpad/b83_olu_dal.py` | **B-112** — 200 000 yük, dal sayımı | ~1 dk |
| `scratchpad/ayikla_kaynak_hash.py` | **B-113** — aracın KENDİ `_kosu`/`_imza`sı | ~2 dk |
| `scratchpad/k017.py` · `k024b.py` | üreticisiz kayıtların yeniden üretimi | anlık + ~2 dk |
| `scratchpad/mut_katalog.py` + `mut_kostur.py` | **42 mutasyon**, iki fazlı, `Pool(8)` | **67,8 dk** |
| `scratchpad/matris_calis.py` + `sag_kalan_davranis.py` | sağ kalanların davranışı, **5 kol × 8 yapılandırma** | **21,3 dk** *(11 matris = 440 tam koşu)* |

### Ölçülen süreler — 26 Ağustos 2026, 10 çekirdek

| komut | bu oturumda ölçülen | depodaki yazılı |
|---|---|---|
| `python -m pytest tests -q` | **876,61 sn** *(2,259 sn/test)* | 908,69 sn *(2,342)* — bandın içinde |
| `taban_kontrolu()` *(v2'siz kopya)* | **853,65 sn** | — |
| `test_mekanizma_kapisi.py` tek başına *(Pool(8) çekişmeli)* | **403,9 sn** | — |
| en pahalı **tek** test *(çekişmeli)* | **118,23 sn** | `08` madde 30: **45,7 sn** 🔴 |

---

## SON SÖZ

`03` Bölüm C'nin **altı sözleşmesinden üçü sağlanmıyor** *(3 · 4 · 5)* ve
üçü de **"sonradan eklenemez"** diye işaretlenmiş olanlar. Bölüm D'nin
**dördüncü seviyesi** — projeyi *"bir öğrenci simülasyon yazdı"*dan
*"bir öğrenci bir araştırma aracı geliştirdi ve doğruladı"*ya taşıyacak
adım — **nitel olarak sağlanıyor, gerekçe olarak sağlanmıyor**; ve bu
denetimde açığın adaylarının **ölçülmüş üst sınırları** ilk kez yazıldı:
**yetmiyorlar.**

🟢 **Araç sağlam.** Yeniden ürettiğim on altı sayının **on beşi** birebir
tuttu; Y13 **21/21**; mekanizma katmanı altı denetimde ilk kez yeterli
güçle ölçüldü ve H0 reddedildi.

🔴 **Ama kapı bugün düşer**, ve düşme sebebi bu raporun yazıldığı sırada
**ölçülmüştü — koşulmadan.** Bu, deponun *"ön kontrol geçti, kapı düştü"*
örüntüsünün **dördüncüsüdür** ve ilk kez **önceden** görüldü.

🔴 **Ve örüntünün kendisi hakkında:** altı denetimin bulduğu şey artık
`sim/` altında değil. Bu denetimin en pahalı üç bulgusu — **B-100**,
**B-113**, **B-115** — **doğrulama araçlarının kendisinde.** Aracı
denetleyen araç, denetlediği araçtan daha az denetlenmiş.

> **Bir şeyi büyütmek istiyorsan önce ölç.** Bu denetimde büyütülmek istenen
> şey **güvendi**; ölçülen şey ise **aracın kendi ölçüm zinciriydi.**

---

🔒 **BU OTURUMDA HİÇBİR DOSYA DEĞİŞTİRİLMEDİ.** `sim/`, `tests/`,
`dogrulama/`, `v2/`, `denetim/`, `ciktilar/` ve `README.md` **okundu,
yazılmadı**. Tüm mutasyonlar, kandırma denemeleri ve matrisler
`tempfile.mkdtemp()` ile açılan **geçici kopyalarda** koşturuldu ve koşu
sonunda silindi. Ölçüm betikleri oturuma özel bir **scratchpad** dizininde
yazıldı ve depoya **kopyalanmadı**. Bu oturumda yazılan **tek depo dosyası
bu rapordur** *(`aile0_audit.md`)*; önceki beş denetimin metnine
**dokunulmamıştır** — yalnızca baştaki durum tablosuna **altıncı satır**,
beşinci özetten sonra **altıncı özet**, ve dosyanın sonuna **altıncı denetim
bölümü** eklenmiştir.

🔒 **BU OTURUMDA HİÇBİR GİT KOMUTU ÇALIŞTIRILMADI — `status` dâhil.**

🔒 **Ana deney tohumları (2000–2029) hiçbir amaçla koşulmadı.** Kullanılan
tohumlar **1–30** aralığındadır *(ayarlama/kapı kümesi)*: tekil ölçümlerde
**1 · 2 · 3 · 4 · 5 · 7 · 9 · 11 · 23**, Li ve topoloji taramalarında
**1–30**.

---
---

# B0 DENETİMİ — 2 Eylül 2026

> **Denetlenen:** K-086'nın B0 oturumu — dört kalemin kapatıldığı, bir
> kalemin denetlendiği, dört yeni bulgunun çıkarıldığı iddiası; ve
> **B0'ın kendi seçtiği üç şey:** koşul 1'in istatistiksel ölçütü,
> `06` §8.1'in reçetesinin değiştirilmesi kararı, `karsilastirma.py`nin
> 16 mutasyonu.
>
> **Soru:** *B0, ölçütlerini ölçtüğü şeyi geçirecek biçimde mi seçti?*
>
> **Yedinci bağımsız denetim** · bulgular **B-120 … B-142** *(23 bulgu)*.

---

## 0. YÖNETİCİ ÖZETİ

### 🔴 B0 ÖLÇÜTLERİNİ KENDİ LEHİNE Mİ SEÇTİ: **KISMEN** — ve en ağır kusur "lehine seçmek" değil, **ÖLÇÜTÜ YANLIŞ NESNEYE UYGULAMAK**

> ## 🔴 EN CİDDİ TEK BULGU — B-120
>
> B0, `08` md 31'de ilan edilmiş bir sayıyı *(çarpıklık **1,004–1,079**)*
> **"olamaz"** diye çürüttü. Gerekçesi: o oran **analitik olarak
> [1,1852 · 1,2963] bandına hapistir** *(320/270 ve 350/270)*.
>
> 🔴 **O band analitik DEĞİLDİR ve ÜÇ AYRI YOLDAN kırılıyor — üçü de bu
> denetimde ölçüldü:**
>
> | # | kanıt | ölçülen |
> |---|---|---|
> | 1 | Aracın **kendi çıktı dosyasında** üç sayaç bandın dışında | `beacon_gonderilen` **1,2942–1,3398** *(üstten)* · `veri_bayt` ve `mac_deneme` **1,1786–1,2573** *(alttan)* |
> | 2 | Bandın konuştuğu sayacın **kendisi**, başka bir tohumda dışarı çıkıyor | `hedefe_en_yakin`/S2/orta/**tohum 4** → **1,299260** > 1,296296 |
> | 3 | Başka bir **pencere yapılandırmasında** 1,004–1,079 doğrudan üretiliyor | `isinma_s` = 5 / 15 / 25 → **1,0144 · 1,0446 · 1,0766** |
>
> 🔴 **Bedeli iki katlı:** (2) numaralı kanıt aynı zamanda
> `dogrulama/pencere_kapsami.py`nin **tohum 4'te `AssertionError` ile
> ÇÖKTÜĞÜNÜ** gösteriyor. Yani `08` md 31'in yeni üreticisi, kendi ilan
> ettiği "analitik çapa" yüzünden **yalnızca B0'ın seçtiği tek tohumda
> koşuyor.**
>
> ⚖️ **Sınıf:** bu, B0'ın kendi kaydettiği iki hatasıyla *(kendi yazdığı
> açıklama satırındaki dizgiyi "eski kod" sanmak)* **aynı sınıftır** —
> doğru görünen bir ölçüt, **yanlış nesneye** uygulanmış. B0 bir sayıyı
> *"imkânsız"* ilan ederken imkânsızlığın **kendi çalışma noktasına bağlı**
> olduğunu ölçmedi; `03` kural 13'ün *"fiziksel sezgiyle çelişen bir sonucu
> KURULUMU denetlemeden açıklamaya çalışma"* uyarısının aynadaki hâli.

### İkinci ve üçüncü en ciddi

| # | bulgu | neden ciddi |
|---|---|---|
| **B-121** | `06` §8.1b'nin **taşıyıcı satırı** *(HAM p95, 17/30, p = 0,5847)* ilan edilen üreticiden **çıkmıyor** — `gecerlilik.py::kosul2` yalnızca üç okuma üretiyor | O satır olmadan *"sorun p95 değil, KÜME"* iddiası **kurulamaz**. `03` kural 1'in ihlali, mühre giden bir sayfada — B-80/B-81'in birebir tekrarı |
| **B-122** | K-086 §7.1'in *"iki farklı ölçüm hattı aynı sayıyı üretti"* kanıtı **tautoloji**: 120 işin metrikleri `kaynak_hash` dışında **bit-birebir aynı** — aynı tohum, aynı konfig, belirlenimci simülatör | Bağımsız doğrulama sanılan şey **determinizmin sonucu**. Y6: kendi lehine çıkan sonuç da şüphelidir |

### 🔴 B1'E (Kat 4) GEÇİLEBİLİR Mİ

> ## 🟡 EVET — AMA **B-120 · B-121 · B-123 · B-133** B1'DEN ÖNCE KAPANMALI

Gerekçe: B1 **şemayı SON KEZ donduracak** *(`12` §2.2 · B1.5)*. Bu dördünün
üçü doğrudan **şemanın nasıl okunacağıyla** ilgilidir:

| bulgu | B1'e taşınırsa |
|---|---|
| **B-120** | `08` md 31'in *"tüm koşu hâli teşhis içindir"* bağlayıcı cümlesi **yanlış bir analitik gerekçeyle** mühürlenir; üreticisi tek tohumda çalıştığı için Faz 1'de yeniden koşulamaz |
| **B-121** | Mühürlenen bir tablonun bir satırının üreticisi yok |
| **B-123** | md 31'in yeni bandı **tek tohumdan** — `03` kural 2'nin doğrudan ihlali, üstelik B0'ın md 25'te **düzelttiği** hatanın aynısı |
| **B-133** | Sonuç satırı **koşuyu tanımlamıyor**; şema donduktan sonra bu alan eklenemez *(`12` §2.2'nin kendi uyarısı)* |

Kalan 19 bulgu B1'i **bloke etmez** ama **B2 (kapı) öncesinde** kapanmalıdır.

---

## 1. 🔴 ÖLÇÜT SEÇİMİ — Bölüm A'nın altı sorusu

### A1 — Ölçüt işaretle sınırlı, **büyüklüğü serbest bırakıyor**. 🔴 DOĞRULANDI

`dogrulama/isaret_testi.py:139` — geçme kararının **tamamı**:

```python
cikti["gecti"] = cikti["p"] > alfa
```

GA hesaplanıyor ve yazdırılıyor — **hiçbir karara girmiyor**. Üretilen iki
karşı vaka:

| vaka | işaret | p | yargı | medyan fark |
|---|---|---|---|---|
| 16 tohumda +2σ, 14 tohumda −0,001σ | 16/30 | 0,8555 | 🟢 **GEÇTİ** | **+2,00 × tohumlar arası std** |
| 20 tohumda +5σ, 10 tohumda −0,1σ | 20/30 | 0,0987 | 🟢 **GEÇTİ** | **+5,00 × tohumlar arası std** |

🔴 İkincisi kritik: tohumların **%66,7'sinde aynı yönde** ve tohum
gürültüsünün **beş katı** olan bir koşu-uzunluğu bağımlılığı, ölçüte göre
*"sonuç koşu uzunluğundan bağımsız"* sayılır.

**ULAŞILAN GÜÇ** *(n = 30, α = 0,05, kesin binom — bu denetimde ilk kez
hesaplandı)*:

| tohumların şu oranında aynı yön | red olasılığı *(güç)* |
|---|---|
| %60 | **0,177** |
| %65 | **0,358** |
| %70 | **0,589** |
| %75 | 0,803 |
| %80 | 0,939 |

⚖️ **Yargı:** ölçüt **geriye dönük bir gevşetme DEĞİLDİR** — öncesinde
eşik zaten yoktu, `03` kural 3 ihlal edilmemiştir. Ama **eksiktir**:
koşul 1'in metni *"sonuç koşu uzunluğundan bağımsız"* diyor; ölçüt yalnızca
*"bağımlılığın YÖNÜ sistematik değil"* diyor. İkisi aynı şey değildir.

**Kapanış önerisi:** ölçüte ikinci ayak — *"…**ve** medyan farkın %95
GA'sının uçları tohumlar arası std'nin [k] katını aşmıyorsa"*. `k`, `06`
Bölüm 7 gereği **26 Eylül güç analizinden** türetilir; bugün bir sayı
yazmak `03` kural 2'nin ihlali olurdu.

### A2 — *"Dışlanan etki büyüklüğü yazılır"* ama `06`nın KENDİ iki şartı sağlanmıyor. 🔴 **B-126**

`06` Bölüm 7 negatif sonucun **biçimini** kendisi tanımlıyor:

> *"Şu büyüklükten daha büyük bir etkiyi **%__ güçle** dışlıyoruz (n = __)."*

🔴 §9.1 **gücü yazmıyor** — yalnızca GA yazıyor.

Ve `06` Bölüm 7'nin **durdurma kuralı** *(ε_rel = GA yarı genişliği /
nokta tahmini ≤ %10)* 12 çiftin **12'sinde de sağlanmıyor**:

| kol | sen | metrik | n+/n | p | **ε_rel** |
|---|---|---|---|---|---|
| en_kisa_yol | S0 | teslim_orani | 13/30 | 0,5847 | %238,0 |
| en_kisa_yol | S0 | **gecikme ort** | 22/30 | **0,0161** | **%77,9** |
| en_kisa_yol | S0 | gecikme p95 | 19/29 | 0,1360 | %242,9 |
| en_kisa_yol | S2 | teslim_orani | 15/28 | 0,8506 | %762,0 |
| en_kisa_yol | S2 | gecikme ort | 16/30 | 0,8555 | %248,3 |
| en_kisa_yol | S2 | gecikme p95 | 15/30 | 1,0000 | %4 397,4 |
| gurultuden_kacan | S0 | teslim_orani | 14/30 | 0,8555 | %950,6 |
| gurultuden_kacan | S0 | gecikme ort | 13/30 | 0,5847 | %170,1 |
| gurultuden_kacan | S0 | gecikme p95 | 12/30 | 0,3616 | %328,3 |
| gurultuden_kacan | S2 | **teslim_orani** | 8/30 | **0,0161** | %177,2 |
| gurultuden_kacan | S2 | gecikme ort | 10/30 | 0,0987 | %490,8 |
| gurultuden_kacan | S2 | gecikme p95 | 10/29 | 0,1360 | %589,5 |

⚖️ Bu **kolların suçu değil**: 30 tohum, sıfıra yakın bir medyan farkın
%10'luk göreli kesinliğine yetmez. Kusur şu: `06` kendi durdurma kuralını
koşul 1'e **hiç uygulamadı** ve uygulanmadığını da yazmadı. `03` kural 3'ün
*gevşetilmiş* hâli **değil** — **hiç uygulanmamış** hâli.

### A3 — α = 0,05 **gelenekten** geldi; α değişince üç yargı değişir

`06` Bölüm 7'de α **hiçbir yerde ilan edilmiyor**; tek geçtiği yer
*"p > 0,05 ile etki yok aynı şey değildir"* cümlesidir. Güç analizi
Bölüm 7'nin kendi ifadesiyle **26 Eylül'de** yapılacak — yani α ölçümden
değil, **konvansiyondan** geliyor. Ölçüldü:

| α | düşen çift | hangileri |
|---|---|---|
| 0,01 | **0** | — |
| **0,05** | **2** | `en_kisa_yol`/S0/gec ort · `gurultuden_kacan`/S2/teslim |
| 0,10 | **3** | + `gurultuden_kacan`/S2/gec ort |
| 0,20 | **5** | + `en_kisa_yol`/S0/gec p95 · `gurultuden_kacan`/S2/gec p95 |

🔴 **α = 0,01'de düşen çift KALMIYOR** — yani *"12 çiftin 2'si geçmiyor"*
cümlesi α'ya oynak. Hile değildir *(α koşmadan önce ilan edildi)*, ama
§9.1'e α'nın **nereden geldiği** yazılmalı.

### A4 — Beraberlikler: ne gevşetiyor ne sıkıştırıyor — **ESTİMANDI DEĞİŞTİRİYOR**. 🔴 **B-124**

**(a) Yön — iki ayrı cevap.** Sabit *pozitif oranda* beraberlik dışlamak
testi **gevşetir**; sabit *pozitif sayıda* beraberlik dışlamak
**sıkıştırır**:

| berabere | pozitif ORANI sabit (%60) | pozitif SAYISI sabit (18) |
|---|---|---|
| 0 | n=30 · p = 0,3616 | n=30 · p = 0,3616 |
| 2 | n=28 · p = 0,3449 | n=28 · p = 0,1849 |
| 5 | n=25 · p = 0,4244 | n=25 · **p = 0,0433 → REDDEDER** |
| 10 | n=20 · p = 0,5034 | n=20 · **p = 0,0004 → REDDEDER** |

Deponun gerçek vakasında *(`en_kisa_yol`/S2/teslim, 2 beraberlik)* etki
zararsız: dışlayarak **15/28 → p = 0,8506**; beraberlikleri pozitif sayarak
17/30 → 0,5847; negatif sayarak 15/30 → 1,0000. **Üçü de geçiyor.**

**(b) 🔴 ASIL KUSUR — iki farklı büyüklük tek satırda.**

- `medyan_fark` **HAM** farklardan *(sıfırlar dâhil)* — `isaret_testi.py:126`
- `ga` **NET** farklardan *(sıfırlar dışlanmış)* — `isaret_testi.py:143`

`06` §9.1 ise *"**medyan farkın** dağılımdan bağımsız %95 GA'sı"* diyor.
İkisi aynı büyüklüğün değil, **iki ayrı büyüklüğün** kestirimidir. Kırıcı
vaka *(20 tohumda fark tam sıfır, 10 tohumda +4/+5)*:

```
n_ham=30  berabere=20  n=10   p=0,001953   GECTI=False
raporlanan medyan_fark = +0,0000       (TÜM farklardan)
raporlanan GA          = [+4,00 , +5,00]  (SIFIRSIZ farklardan)
medyan KENDİ GA'sının içinde mi: HAYIR
```

🔴 Araç *"medyan fark 0,00 · dışlanan etki [+4,00 · +5,00] · GEÇMEDİ"*
basıyor — oysa farkların gerçek medyanı **tam sıfırdır**. Bugünkü veride
beraberlik 0–2 olduğu için zarar görünmüyor; Faz 1'in sayaç metrikleri
*(PSR · üç kopma sayacı · COR)* **çok daha fazla tam-sıfır fark** üretecek
ve orada bu satır **yanlış bir cümle** basar.

### A5 — 🔴 Bağlayıcılık daraltması şartı **BOŞALTIYOR**. **B-127**

§9.1: *"Koşul 1 **rapora giren kollar** için bağlayıcıdır; doğrulama
aktarıcıları ölçülür ve `08`e beyan edilir."* Ölçüldü — bugün ölçülebilen
kolların **hepsi** doğrulama aktarıcısıdır:

```
AKTARICILAR = ['en_kisa_yol', 'hedefe_en_yakin', 'dongu_yapan',
               'olu', 'gurultuden_kacan']
```

README, `07` ve `08` üçünü de *"doğrulama aktarıcısı"* diye tanımlıyor
*(`en_kisa_yol` **kâhindir**)*.

> 🔴 **Sonuç: koşul 1 bugün SIFIR kolu bağlıyor — ve düşen iki çiftin
> İKİSİ DE muaf.** Şart, tetiklendiği anda kapsamının dışına çıktı.

⚖️ **Ama bu bir hile DEĞİLDİR** ve öyle yazılmamalıdır: `06` Bölüm 9'un
başlığı gerçekten *"hiçbir **SONUÇ** raporlanmaz"* diyor ve doğrulama
aktarıcılarının hiçbir sonucu rapora girmiyor. Kusur **daraltmanın kendisi
değil, sessizliğidir**: bir okuyucu *"12 çiftin 2'si geçmiyor"* tablosunu
**bağlayıcı bir ölçüm** sanar.

**Kapanış önerisi:** §9.1'e tek cümle — *"Bugün ölçülen kolların hiçbiri
rapora girmez; koşul 1 ilk kez **Faz 1'de AODV/OLSR/AOMDV üzerinde**
bağlayıcı ölçülür. Bugünkü tablo bir **taban çizgisidir.**"*

### A6 — 🔴 SEBEP ÖLÇÜLDÜ: **pencere içi ısınma artığı** — "koşu uzunluğu" DEĞİL

B0 yeni düşen çifti *(`en_kisa_yol`/S0/gecikme ort, 22/30, p = 0,0161)*
*"`isinma_s = 50` yetersiz **olabilir**"* diye yorumladı ve **sebebi
ölçmedi** — `03` B4'ün tam olarak uyardığı şey.

Ölçüldü *(30 tohum, depodaki satırlardan, hiç yeni koşu açmadan)*: her
tohumda **tam** koşunun teslimleri, **kısa** koşunun pencere kimlik
aralığına göre erken/geç diye ikiye bölündü.

| karşılaştırma | işaret | p | medyan fark |
|---|---|---|---|
| KISA − TAM *(§9.1'in testi)* | 22/30 | **0,0161** | **+1,6497 ms** |
| **KISA − TAM_ERKEN** *(dinamik fark var mı)* | **0/1** | 1,0000 | **+0,0000** · berabere **29** |
| **TAM_ERKEN − TAM_GEÇ** *(pencere konumu)* | 22/30 | **0,0161** | **+2,9660 ms** |

🔴 **İki sonuç:**

1. **29/30 tohumda kısa koşunun paketleri, tam koşunun aynı kimlik
   aralığındaki paketleriyle BİT-BİREBİR AYNI.** Beklenmesi gereken buydu:
   simülatör nedensel ve belirlenimcidir; t = 170 s'den sonra doğan trafik
   daha önce doğmuş paketleri etkileyemez. Yani **"koşu uzunluğu" diye bir
   dinamik etki yok ve olamaz.**
2. Ölçülen etkinin **tamamı** pencere konumundan geliyor: penceredeki
   **erken paketler geç paketlerden sistematik olarak yavaş** *(aynı 22/30,
   aynı p = 0,0161, medyan **+2,97 ms**)*.

⚖️ **Sebep: kuyruk değil, boşaltma değil — ölçüm penceresinin İÇİNDE kalan
bir ısınma artığı.** B0'ın hipotezi doğru çıktı; ama hipotezdi, artık ölçüm.

🔴 **Ve daha önemli bir sonuç:** §9.1'in testi, adı *"koşu uzunluğundan
bağımsızlık"* olduğu hâlde **yapısal olarak yalnızca ısınma artığını
ölçebilir**. `06` §9.1 bunu yazmalı; yazmazsa Faz 1'de bir protokol bu
testten kaldığında **yanlış sebep aranır** *(`03` kural 12)*.

**Kapanış önerisi:** `isinma_s`ı gecikme metriği için **ölçerek** seç —
erken/geç fark testini `isinma_s ∈ {50, 80, 110, 140}` üzerinde koştur ve
farkın söndüğü noktayı yaz. B1'den önce yapılabilir, şemaya dokunmaz.

---

## 2. 🔴 REÇETE DEĞİŞİKLİĞİ — Bölüm B'nin dört sorusu

### B1 — Değişen şey bir **YÖNTEM**, bir eşik değil. Meşru — ama gerekçe eksik

`06` bir **ön-kayıt** belgesidir ve B0 onu **ölçtükten sonra** değiştirdi.
Biçimsel olarak meşru: mühür **26 Eylül** *(K-083 ile ~20 Ekim önerisi)*,
belge kendi başlığında *"o tarihe kadar yapısal değişiklik meşrudur"*
diyor.

⚖️ **`03` kural 3'ün ruhu açısından da meşru — ve gerekçesi ölçülebilir:**

| ne | eski §8.1 | yeni §8.1b | yön |
|---|---|---|---|
| ne yasaklandı | *"gecikme cümlesi p95 ile yazılır"* | *"ortak alt küme **+** p50/p95/p99 **+** kesişim oranı"* | 🟢 **SIKILAŞTI** |
| kodda zorunlu mu | ❌ hayır | 🟢 evet *(`ortak_alt_kume` tipli hata)* | 🟢 **SIKILAŞTI** |
| kaç şart | 1 | 3 | 🟢 **SIKILAŞTI** |

🔴 **Bir eşik gevşetilmedi; bir yöntem değiştirildi ve üç yeni şart eklendi.**
`03` kural 3'ün yasakladığı şey *"eşiği geriye dönük gevşetmek"*tir; burada
olan bunun tersidir. **Yargı: MEŞRU.**

⚠️ **Ama gerekçenin kendisi eksik yazılmış** — bkz. B-121 ve B3.

### B2 — 🔴 Ortak alt küme okuması **kesişim alt sınırı olmadan** ilan edildi. **B-140**

Ölçüldü *(30 tohum, S0→S2, `ortak_alt_kume`)*:

| kol | kesişim ortalaması | min | max |
|---|---|---|---|
| `en_kisa_yol` | **%51,1** | %20,0 | %77,7 |
| `gurultuden_kacan` | **%20,7** | **%5,6** | %37,9 |

🔴 `gurultuden_kacan`'ın **en dar hücresinde ortak alt küme, pencerede
üretilen paketlerin %5,6'sı.** `06` §8.1b bu sayıyı **yazıyor** ama bir
**alt sınır koymuyor**; `ortak_alt_kume` yalnızca `ortak_paket == 0`
durumunu reddediyor *(`karsilastirma.py:170`)*.

⚖️ **Bu bir boşluktur ve `03` B3'ün kendi mantığından çıkar:** seçilim
yanlılığı ortak alt kümede *"ortadan kalkmaz"*, **taşınır** — %5,6'lık bir
kesişim, iki kolun da teslim edebildiği **en kolay** paketlerdir. O alt
kümede ölçülen gecikme farkı, dağılımın **yalnızca en kolay ucunu**
temsil eder ve genellenemez.

🔴 **Ve B1'de bu bağlayıcı olacak:** AODV ↔ OLSR karşılaştırmasında
teslim oranları farklıysa kesişim daralır. `06` §8.1b bugün *"kesişim
oranını yaz"* diyor; **"şu oranın altında karşılaştırma yapılmaz"**
demiyor.

**Kapanış önerisi:** alt sınır **ölçülerek** konur *(kesişimi yapay olarak
daraltıp gecikme farkının ne zaman kaymaya başladığını ölçmek yeterli)*.
Bugün bir sayı yazmak `03` kural 2'ye aykırı olurdu; **ama boşluğun
kendisi `08`e madde olarak girmelidir.**

### B3 — 🔴 `gurultuden_kacan` TERSİ sonuç veriyor ve §8.1b'de **görünmüyor**. **B-136**

`gecerlilik.py::kosul2` bugün **altı satır** üretiyor; `06` §8.1b **yalnızca
`en_kisa_yol`'un üçünü** taşıyor. Ölçülen tam tablo:

| kol | okuma | işaret | p | medyan fark |
|---|---|---|---|---|
| en_kisa_yol | HAM ortalama | 12/30 | 0,3616 | −3,98 ms |
| en_kisa_yol | ORTAK ortalama | 25/30 | **0,0003** | **+5,40 ms** |
| en_kisa_yol | ORTAK p95 | 27/30 | **0,0000** | **+28,15 ms** |
| **gurultuden_kacan** | HAM ortalama | **4/30** | **0,0001** | **−414,51 ms** |
| **gurultuden_kacan** | ORTAK ortalama | 11/30 | 0,2005 | −61,69 ms |
| 🔴 **gurultuden_kacan** | **ORTAK p95** | **9/30** | **0,0428** | **−263,03 ms** |

🔴 **`gurultuden_kacan`da ortak alt küme p95'i S0 → S2'de DÜŞÜYOR
ve bu anlamlı *(p = 0,0428)*.** Yani reçetenin *"ortak alt kümede kuyruk
kötüleşir"* dediği yerde, ikinci kol **tersini** gösteriyor.

⚖️ **Bu, reçeteyi çürütmez** — reçete *"ortak alt küme kullan"* diyor,
*"sonuç şu yönde çıkar"* demiyor; ve `gurultuden_kacan`ın kesişimi
**%20,7** *(B2)*, yani ortak alt küme orada zaten dar ve seçilimli.
🔴 **Ama §8.1b'nin "ÜÇ SONUÇ" bölümü tek koldan yazılmış** ve ikinci kol
**hiç anılmıyor.** `03` kural 3: *"negatif sonucu gizleme"*. Gizlenmiş
değil — **yazılmamış**; ama araç onu her koşuda basıyor.

**Kapanış önerisi:** §8.1b'ye altı satırın **tamamı** girsin ve ters yön
`03` B3'ün kesişim uyarısıyla birlikte yorumlansın.

### B4 — 🔴 "İki ayrı boru hattı" **BAĞIMSIZ DEĞİL**. **B-122**

K-086 §7.1'in **üçüncü kanıtı**:

> *"`06` §8.1b'nin sayıları ilk kez `literatur_eksenleri.jsonl`den (hash
> `89587a19…`, B0 öncesi kod, farklı iş matrisi) türetilmişti.
> `gecerlilik.py` onları **bağımsız bir boru hattıyla** yeniden üretti."*

**Ölçüldü** — iki dosyanın **ortak 120 işi** karşılaştırıldı:

```
ortak is: 120 | metrik seti BIT-BIREBIR ayni: 0
farklilasan alan: {'kaynak_hash': 120}
```

🔴 **120 işin 120'sinde, 77 metriğin `kaynak_hash` DIŞINDAKİ hepsi
bit-birebir aynı.** Konfigürasyonlar da `kol` etiketi *(serbest metin)*
dışında birebir aynı.

⚖️ **Yani iki "boru hattı" aynı deterministik koşuları yeniden koştu.**
Aynı tohum + aynı konfig + belirlenimci simülatör = aynı sonuç, **tanım
gereği**. Bunu bir doğrulama saymak, bir hesap makinesini iki kez çalıştırıp
*"iki bağımsız hesap aynı çıktı"* demektir.

🟢 **Bunun DEĞERLİ bir yanı var ve o kaydedilmeli:** ölçüm, B0'ın `sim/`
değişikliklerinin **davranışsal olarak atıl** olduğunu kanıtlıyor —
hash `89587a19…` *(kapının koştuğu kod)* ile `0a1a94e5…` *(bugün)* arasında
**120 iş bit-birebir**. Bu, **şüphe 8'in** cevabıdır *(bkz. §8)*.
🔴 **Ama bu bir "denklik ölçümü"dür, bir "bağımsız doğrulama" değildir**
ve K-086 §7.1 ikisini karıştırıyor.

**Kapanış önerisi:** K-086 §7.1'in *"iki farklı ölçüm hattı"* cümlesi
*"aynı deterministik koşuların iki kod sürümündeki DENKLİĞİ"* olarak
düzeltilsin. Gerçek bir bağımsız doğrulama, **farklı bir tohum kümesi**
ya da **farklı bir kestirici** gerektirir.

---

## 3. 🔴 YENİ ARAÇLARIN MUTASYON KAPSAMI — Bölüm C

### 3.0 Önce: ULAŞILABİLİRLİK **ölçüldü**, varsayılmadı

Beş aracın her biri için modül başına `raise ImportError` sondası kondu ve
**tüm test paketi toplandı** *(`pytest --collect-only`)*:

| araç | onu içe aktaran test modülü | ölçülen |
|---|---|---|
| `isaret_testi.py` | `tests/test_isaret_testi.py` | 462 → **449** toplandı + 1 hata |
| `gecikme.py` | `tests/test_gecikme.py` | 462 → **455** toplandı + 1 hata |
| **`gecerlilik.py`** | 🔴 **HİÇBİRİ** | 462 toplandı, **hata yok** |
| **`pencere_kapsami.py`** | 🔴 **HİÇBİRİ** | 462 toplandı, **hata yok** |
| **`li_calisma_noktasi.py`** | 🔴 **HİÇBİRİ** | 462 toplandı, **hata yok** |

Metin/AST üzerinden dolaylı tek yol `tests/test_kapi_secimleri.py`
*(`dogrulama/*.py` üzerinde `glob` yapan iki B-106 testi)*. Bu üç dosya
**ölçülmüş ulaşılabilir küme**tir:

```
tests/test_isaret_testi.py  tests/test_gecikme.py  tests/test_kapi_secimleri.py
```

🔴 **Ve bu ölçüm bir kez YANLIŞ yapıldı — kayda geçer:** ilk mutasyon
koşusunda kopya `v2/` taşımıyordu; `test_kapi_secimleri.py`nin **5 testi
TEMİZ ağaçta da düşüyordu** ve `-x` ile koşulduğu için **20 mutasyonun
20'si "yakalandı" göründü**. Y7'nin kendisi: *bir ölçüt önce TEMİZ durumda
doğrulanır*. Düzeltildi; taban **85/85 GEÇİYOR** ve karşılaştırma
**düşen test kümesi** üzerinden yapılıyor.

### 3.1 Yirmi mutasyon — Y8 tetiklenmesi ÖNCE gösterildi

Y8 için bir **tetikleme harnessı** yazıldı: beş aracın karar yüklemleri
depodaki **gerçek** satırlarla koşturulup tek satırlık bir parmak izi
basılıyor. Temel çıktı, `08` md 31 ve `08` Ç4'ün ilan edilmiş sayılarını
**birebir** üretiyor *(pay %18,17–22,86 · çarpıklık 1,2221–1,2963 ·
1,761/0,277 Mbps · +%3,6/+%10,8)*, yani yol gerçekten koşuyor.

| kod | araç | ne bozar | Y8 tetik | test | yargı |
|---|---|---|---|---|---|
| I1 | isaret_testi | `p > alfa` → `p >= alfa` | DEĞİŞMEDİ | GEÇTİ | ⚪ **eşdeğer** |
| I2 | isaret_testi | varsayılan α 0,05 → 0,10 | DEĞİŞTİ | **GEÇTİ** | 🔴 **SAĞ KALDI** |
| I3 | isaret_testi | çift yönlü → tek yönlü | DEĞİŞTİ | DÜŞTÜ | 🟢 yakalandı |
| I4 | isaret_testi | beraberlikler dışlanmıyor | DEĞİŞTİ | DÜŞTÜ | 🟢 yakalandı |
| I5 | isaret_testi | binom kuyruğu bir eksik | DEĞİŞTİ | DÜŞTÜ | 🟢 yakalandı |
| I6 | isaret_testi | medyan GA'sı bir eleman daraltıldı | DEĞİŞTİ | DÜŞTÜ | 🟢 yakalandı |
| I7 | isaret_testi | GA/std yerine GA×std | DEĞİŞTİ | DÜŞTÜ | 🟢 yakalandı |
| G1 | gecikme | p95 → p90 | DEĞİŞTİ | DÜŞTÜ | 🟢 yakalandı |
| G2 | gecikme | boş tohumlar dışlanmıyor | ÇÖKTÜ | DÜŞTÜ | 🟢 yakalandı |
| G3 | gecikme | eşleştirilmiş diziye boş tohum giriyor | ÇÖKTÜ | DÜŞTÜ | 🟢 yakalandı |
| **V1** | **gecerlilik** | koşul 1'de farkın **işareti ters** | DEĞİŞTİ | **GEÇTİ** | 🔴 **SAĞ KALDI** |
| **V2** | **gecerlilik** | kısa koşu = tam koşu *(test boşalıyor)* | DEĞİŞTİ | **GEÇTİ** | 🔴 **SAĞ KALDI** |
| **V3** | **gecerlilik** | **ORTAK p95** aslında ORTAK ortalamayı basıyor | DEĞİŞTİ | **GEÇTİ** | 🔴 **SAĞ KALDI** |
| **V4** | **gecerlilik** | D-13'ün `assert yazilan == len(isler)`i etkisiz | *(main)* | **GEÇTİ** | 🔴 **SAĞ KALDI** |
| **V5** | **gecerlilik** | tohum std'si hiç hesaplanmıyor → GA/std daima boş | DEĞİŞTİ | **GEÇTİ** | 🔴 **SAĞ KALDI** |
| **P1** | **pencere_kapsami** | pencere dışı pay yanlış paydadan | DEĞİŞTİ | **GEÇTİ** | 🔴 **SAĞ KALDI** |
| **P2** | **pencere_kapsami** | çarpıklık **ters** | DEĞİŞTİ | **GEÇTİ** | 🔴 **SAĞ KALDI** |
| **P3** | **pencere_kapsami** | Y7 analitik çapa denetimi etkisiz | *(main)* | **GEÇTİ** | 🔴 **SAĞ KALDI** |
| **L1** | **li_calisma_noktasi** | Li farkı yanlış paydadan *(%10,8 → %9,7)* | DEĞİŞTİ | **GEÇTİ** | 🔴 **SAĞ KALDI** |
| **L2** | **li_calisma_noktasi** | literatürün hedefi ölçüme uyduruldu | DEĞİŞTİ | **GEÇTİ** | 🔴 **SAĞ KALDI** |

**Notlar.**
`I1` **eşdeğer mutanttır** ve skordan çıkarıldı: n = 1…60 aralığında kesin
binom **hiçbir zaman tam 0,05 vermiyor** *(ölçüldü)*, dolayısıyla
`>` ↔ `>=` davranışı değiştirmez.
`V4` ve `P3` yalnızca `main()` içinde yaşıyor; harness `main()`i çağırmadığı
için parmak izi değişmedi — **ama ikisi de üretim yolundadır** ve **hiçbir
test modülü bu iki dosyayı içe aktarmıyor** *(§3.0'da ölçüldü)*, yani
"ulaşılamaz" oldukları **kanıtlıdır**.
`V5` ilk parmak izinde görünmedi çünkü **benim harness'ım GA/std sütununu
basmıyordu**; genişletilmiş harness'ta *(`tetik2`)* mutasyon
`(-0,1965, 0,0533) → (None, None)` yaptı — **canlı**.

### 3.2 🔴 ARAÇ BAZINDA SKOR · %95 GA · ULAŞILAN GÜÇ

| araç | skor | oran | **%95 GA (Wilson)** |
|---|---|---|---|
| `isaret_testi.py` | **5/6** | %83,3 | [%43,6 · %97,0] |
| `gecikme.py` | **3/3** | %100,0 | [%43,9 · %100,0] |
| 🔴 `gecerlilik.py` | **0/5** | **%0,0** | [%0,0 · %43,4] |
| 🔴 `pencere_kapsami.py` | **0/3** | **%0,0** | [%0,0 · %56,1] |
| 🔴 `li_calisma_noktasi.py` | **0/2** | **%0,0** | [%0,0 · %65,8] |
| **BEŞ ARAÇ TOPLAM** | **8/19** | **%42,1** | **[%23,1 · %63,7]** |
| 🔴 **test dosyası OLMAYAN üç araç** | **0/10** | **%0,0** | **[%0,0 · %27,8]** |

**ULAŞILAN GÜÇ** *(0/n için kesin %95 üst sınır — 1 − 0,05^(1/n))*:

| n | *"gerçek yakalama oranı en fazla"* |
|---|---|
| 10 *(üç araç birlikte)* | **%25,9** |
| 5 *(`gecerlilik.py`)* | %45,1 |
| 3 *(`pencere_kapsami.py`)* | %63,2 |
| 2 *(`li_calisma_noktasi.py`)* | %77,6 |

⚖️ **Yorum — dürüstçe:** 10 mutasyonda 0 yakalama, *"bu üç aracın gerçek
mutasyon kapsamı %25,9'un altındadır"* demeye yeter; *"sıfırdır"* demeye
**yetmez**. Ama bu üç aracın kapsamı ölçülmeden önce zaten **yapısal olarak
sıfırdı**: hiçbir test modülü onları içe aktarmıyor.

### 3.3 🔴 Neden bu üç araç en tehlikeli olanı

| araç | ne üretiyor |
|---|---|
| `gecerlilik.py` | `06` **§8.1b'nin tablosu** · **§9.1'in 12 satırı** · koşul 3'ün sayıları |
| `pencere_kapsami.py` | `08` **md 31**'in pay bandı ve çarpıklık bandı |
| `li_calisma_noktasi.py` | `08` **Ç4**'ün dört mutlak sayısı |

🔴 **V3 özellikle pahalı:** `ortak_p95.append(o.p95_farki_s)` →
`o.gecikme_farki_s`. Bu tek satır, §8.1b'nin *"kuyruk merkezden ~5 kat
fazla kötüleşiyor (+28,15 ↔ +5,40 ms)"* cümlesini **+5,40 ↔ +5,40**
yapar — yani reçetenin **en güçlü gerekçesini** sessizce siler. 462 testin
hiçbiri kırılmaz.

🔴 **V2 ikinci pahalı:** `UZUNLUKLAR["kisa"]`ı `tam` ile aynı yapmak
koşul 1'i **kendi kendisiyle karşılaştıran** boş bir teste çevirir
*(tüm farklar sıfır → "TANIMSIZ")*. Y7'nin *"boş küme de 0 kırık verir"*
tuzağının koşul 1'deki hâli — ve hiçbir test görmüyor.

### 3.4 Önerilen ucuz koruma *(Y12 deseni)*

Üç araç için bir **birim test dosyası** yeter; koşu gerektirmez, çünkü
karar yüklemleri *(`kosul1` · `kosul2` · `kosul3` · `eslesmis_kol_orani` ·
`dis_pay` · `carpiklik` · `_satir`)* **saf fonksiyonlardır** ve depodaki
`ciktilar/sonuclar/*.jsonl` satırlarıyla beslenebilir. Bu denetimin
`tetik.py` harness'ı tam olarak bunu yapıyor ve **0,82–0,84 sn**'de
koşuyor *(3 tekrar ölçüldü: 844 · 828 · 824 ms)*.
Öneri: harness'ın parmak izi bir **çapa testi** olarak `tests/` altına
alınsın — V1, V2, V3, V5, P1, P2, L1, L2'nin **sekizini birden** yakalar.

---

## 4. SIKILAŞTIRMANIN BEDELİ — Bölüm D

### D1 — 🟢 İDDİA ÇÜRÜTÜLEMEDİ: **1 114 / 1 114**

B0 *"`ciktilar/sonuclar/` altında 1 114 satırın 1 114'ü dört pencere alanını
taşıyor, eksik 0"* diyor. Çürütmeye çalışıldı; **çürütülemedi** — ve
kontrol `_PAY_ALANLARI`nın ötesine, `ortak_alt_kume`nin **tam şema
listesine** genişletildi:

```
dosya satirlari: {'gecerlilik': 480, 'kontrol_payi': 240,
                  'pencere_kapsami': 90, 'literatur_eksenleri': 300,
                  'deneme_araliklari': 4}   TOPLAM: 1114
EKSIK alan tasiyan satir: YOK (0)
`ortak_alt_kume`nin TAM sema listesinde eksik: YOK (0)
```

### D1b — 🔴 İKİ HASH **gerçekten bir tuzak**, ve tuzağın adı yanlış

`ortak_alt_kume` farklı `kaynak_hash`li iki satırı **reddediyor**
*(`karsilastirma.py:254`)*. `gecerlilik.jsonl`de iki hash var
*(240 + 240)*, yani **aynı dosyanın satırları birbiriyle
karşılaştırılamıyor**. Ölçüldü:

```
CAPRAZ HASH: REDDEDILDI -> KOD SÜRÜMLERİ farklı: cd6d304f… vs 0a1a94e5…
...ama iki satirin metrikleri BIREBIR ayni mi: True
```

⚖️ **Koruma DOĞRU davranıyor** — kod farkının davranışa yansımadığını
`ortak_alt_kume` bilemez, bilmemeli de. 🔴 **Tuzak korumada değil,
dosyada:** bir okuyucu `gecerlilik.jsonl`i açtığında **iki farklı kod
sürümünden gelen 480 satır** görüyor ve hangisinin güncel olduğunu ancak
hash'e bakarak anlıyor. Bu, **B-133**'ün *(sonuç satırı koşuyu
tanımlamıyor)* bir yüzüdür.

**Pratikte bugün zarar yok:** `gecerlilik.py` `veri` sözlüğünü **kendi
bellek içi koşusundan** kuruyor, dosyayı okumuyor. Zarar, dosyayı
**sonradan** okuyan her analizdedir — ve Faz 1'de tam olarak öyle
okunacak.

### D2 — 🔴 EVET: dejenere kontrol payı **gecikme karşılaştırmasını da öldürüyor**. **B-134**

`ortak_alt_kume` kontrol payını **dönüş nesnesini kurmadan önce**
hesaplıyor *(`karsilastirma.py:412–413`)*; `kontrol_payi_yuzde` bir
`KarsilastirmaHatasi` fırlattığında **tüm fonksiyon** düşüyor. Ölçüldü:

```
SAGLAM : ortak=801 paket, gecikme farki=+10,140 ms, p95 farki=+29,270 ms
B'de dejenere kontrol payi -> TUM karsilastirma REDDEDILDI
```

🔴 **801 ortak paket üzerinden hesaplanmış, tamamen geçerli bir gecikme
farkı, GECİKMEYLE HİÇ İLGİSİ OLMAYAN bir payda yüzünden üretilemiyor.**

Ölçek: `kontrol_payi.py`nin 120 hücresinin **2'si** dejenere *(DV, tohum
25, S0 ve S2)* — %1,7. Küçük, ama **DV kolu** kontrol düzlemi ağır bir kol
ve Faz 1'in AODV'si de öyle olacak.

⚖️ **Bu doğru tasarım DEĞİLDİR ve `03` B3'ün kendi kuralına aykırıdır:**
*"İki çakışmayan olgu tek metriğe sıkışırsa **metriği ikiye ayır**."*
Gecikme karşılaştırması ile kontrol payı iki ayrı olgudur; birinin
tanımsızlığı diğerini geçersiz kılmaz.

**Kapanış önerisi:** `OrtakAltKume.kontrol_payi_a/b` alanları
`dict | None` olsun, `ozet()` **"kontrol payı TANIMSIZ (D-11)"** bassın ve
`06` koşul 3 *"raporlanmadan karşılaştırma yapılamaz"* şartını
**raporlamanın kendisiyle** karşılasın. Bugünkü hâl şartı *"ölçülemezse
hiçbir şey ölçme"*ye çeviriyor.

### D3 — 🟢 Yeni zorunlu alanlar **hem A hem B** için denetleniyor. Kırılarak gösterildi

Dört alanın her biri, önce A'dan sonra B'den silinerek **8 kez** kırıldı;
**8'i de reddedildi**:

```
a/kontrol_bayt_pencere         REDDEDILDI (sonuc_a bu şemayı taşımıyor…)
a/veri_bayt_pencere            REDDEDILDI
a/kontrol_airtime_s_pencere    REDDEDILDI
a/veri_airtime_s_pencere       REDDEDILDI
b/kontrol_bayt_pencere         REDDEDILDI (sonuc_b bu şemayı taşımıyor…)
b/veri_bayt_pencere            REDDEDILDI
b/kontrol_airtime_s_pencere    REDDEDILDI
b/veri_airtime_s_pencere       REDDEDILDI
```

### D4 — İleri referans **gerçek**, bugün zararsız, ama kırılganlık **beyanla değil testle** kapanmalı

`kontrol_payi_yuzde` **satır 67**'de tanımlı ve `KarsilastirmaHatasi`
**satır 94**'te — yani sınıf fonksiyondan **sonra**. Python adı **çağrı
anında** çözdüğü için çalışıyor *(ölçüldü)*.

⚠️ Risk gerçek ama küçük: modül bölünürse ya da `kontrol_payi_yuzde`
başka bir modüle taşınırsa `NameError`. **Kapanışı ucuz:** sınıf tanımını
fonksiyonun üstüne almak — davranış değişmez, `kaynak_hash` değişir
*(yani kapı zaten bayat olduğu için bedeli sıfır)*.

---

## 5. 🔴 D-13'ÜN 540 KOŞUDAKİ BELLEK MALİYETİ — Bölüm E1 *(ÖLÇÜM ZORUNLU)*

### E1 — 🟢 ÖLÇÜLDÜ: **en kötü 35,2 MB. Risk GERÇEK DEĞİL**

18 hücre koşuldu *(6 senaryo × 3 trafik, kapının `kol="kapi_en_kisa_yol"`
konfigürasyonu, tohum 1)* ve dönen **tam `sonuc` sözlüğü** en yüksek
protokolle picklelandı:

| sen | trafik | TAM pickle | liste payı | özet pickle | teslim | sn |
|---|---|---|---|---|---|---|
| S0 | yogun | **68 274 B** | 64 696 | 209 | 5 387 | 2,9 |
| S0 | orta | 35 973 | 32 404 | 209 | 2 697 | 3,3 |
| S0 | seyrek | 16 513 | 12 951 | 209 | 1 081 | 2,0 |
| S1 | yogun | 48 643 | 45 068 | 210 | 3 752 | 5,6 |
| S2 | yogun | 36 241 | 32 668 | 210 | 2 719 | 4,3 |
| S3 | yogun | 55 811 | 52 236 | 210 | 4 349 | 3,8 |
| S4 | yogun | 52 007 | 48 432 | 210 | 4 032 | 3,9 |
| S5 | yogun | 51 042 | 47 456 | 210 | 3 951 | 4,9 |
| *(kalan 10 hücre 10 054 – 26 412 B)* | | | | | | |

| büyüklük | ölçülen |
|---|---|
| satır başına pickle, **ortalama** | **28,8 KB** |
| satır başına pickle, **en büyük** | **66,7 KB** |
| **540 koşu · hepsi aynı anda bellekte (EN KÖTÜ)** | **35,2 MB** |
| 540 koşu · ortalama | 15,2 MB |
| Eski hâl *(yalnız özet)* 540 koşu | **110,7 KB** |
| **ARTIŞ** | **325 kat** |

🔴 **`teslim_kimlikleri` + `teslim_gecikmeleri_s` toplam boyutun
%78–95'ini oluşturuyor** — yani E1'in işaret ettiği yer doğruydu.
🟢 **Ama büyüklük yanlış tarafta:** 35,2 MB, 10 çekirdekli bir makinede
165–330 dakikalık bir koşu için **ihmal edilebilir**. Ayrıca `_havuzda_kos`
tam sonucu **tüketip atıyor** *(`_ozet` çıkarıp listeye onu koyuyor)*;
35,2 MB yalnızca **tüketici tamamen dursa** ulaşılacak teorik tavandır.

⚖️ **Yargı: D-13'ün düzeltmesi 540 koşuda güvenlidir. Ama B0 bunu
ÖLÇMEDİ** — `03` kural 1'in *"ölçmeden iddia etme"*si burada da geçerli;
riski *"yok"* saymak bir ölçüm değildi.

### E2 — `imap` sıralı; birikme **sınırlı ve ölçülü**

`multiprocessing.Pool`un sonuç kuyruğunda **üst sınır yoktur**: yavaş bir
iş sonrakileri bekletirse `IMapIterator` tamamlananları bellekte tutar.
🟢 **Ama tavan bellidir ve E1'de ölçüldü: 540 × 66,7 KB = 35,2 MB.**
Tüketici *(`yaz_sonuc` + `fsync`)* milisaniyeler sürerken üretici 2–6
saniye sürüyor, yani pratikte kuyruk boş kalır.

### E3 — Havuz boyu değişikliğinin bedeli **İÇ İÇE ölçüldü: −0,3 sn**

`Pool(min(CEKIRDEK, len(isler)))` değişikliği kapının **uç durum
matrisinde** *(havuz başına 5 iş)* etkili. 🔴 İki durum **dönüşümlü**
koşturuldu *(K-075: ardışık ölçüm makine oynaklığını koda atfeder)*,
6 tekrar:

| havuz | ortanca | bant |
|---|---|---|
| eski `Pool(10)` | **3,39 sn** | 3,36 – 3,43 |
| yeni `Pool(5)` | **3,31 sn** | 3,21 – 3,36 |

**Fark: −0,08 sn / havuz.** Kapıda böyle **4 havuz** var → toplam
**−0,3 sn**, kapının 9 900–19 800 sn'lik bandının **%0,0033'ü**.
🟢 **Kapı süresi bundan etkilenmez.**

### E4 — Yazıcının aktif olmadığı bir üretim yolu **var, ama küçük**

`_havuzda_kos`un `assert`i `aktif_yazici() is not None` koşuluna bağlı
*(`kapi_korunum.py:110`)*. Üretim yolları:

| yol | yazıcı | assert |
|---|---|---|
| `python dogrulama/aile0_kapi_raporu.py` | 🟢 `with kayit("aile0_kapi_raporu")` *(satır 615)* | çalışır |
| `python dogrulama/kapi_korunum.py` | 🟢 `with kayit("kapi_korunum")` *(satır 220)* | çalışır |
| 🔴 `aile0_kapi_raporu.main()`in **içe aktarılarak** çağrılması | ❌ yok | **sessizce atlanır** |

🟡 Bugün üçüncü yolu kullanan bir çağıran **yok** *(ölçüldü)*. Ama
`test_b106_URETIM_YOLLARI_sonuc_YAZIYOR` yalnızca *"dosyada `kayit(`
geçiyor mu"* diye bakıyor — **`__main__` bloğunun içinde mi, dışında mı
sormuyor.** Bu, `03` B5'in *"bildirim ≠ kullanım"* deseninin bir sonraki
adımıdır ve **B-132** ile aynı kökten gelir.

---

## 6. YENİDEN ÖLÇÜLEN SAYILAR — Bölüm F'nin dört kümesi

### F1 — 🟢 `08` md 25 · kontrol payı: **BİREBİR ÜRETİLDİ**

`ciktilar/sonuclar/kontrol_payi.jsonl`in yeni-hash 120 satırından bağımsız
olarak yeniden hesaplandı:

| okuma | DV kolu | gözlem kolu | eşleştirilmiş oran | `08` md 25 |
|---|---|---|---|---|
| tüm koşu · bayt | %7,80 – %65,04 | %1,65 – %2,10 | **4,3 – 38,1 kat** *(ortanca 13,4)* | 🟢 birebir |
| pencere · bayt | %7,15 – %62,88 | %1,61 – %2,02 | **4,0 – 38,0 kat** *(ortanca 12,9)* | 🟢 birebir |
| pencere · airtime | %10,33 – %72,07 | %3,74 – %4,51 | **2,6 – 18,9 kat** *(ortanca 7,6)* | 🟢 birebir |
| dejenere hücre | | | **2** — *(S0,25)* ve *(S2,25)* | 🟢 birebir |

### F2 — 🟢 `08` md 31 · pencere dışı pay: **BİREBİR ÜRETİLDİ**

**%18,17 – %22,86** *(ortanca **%21,06**)* · çarpıklık **1,2221 – 1,2963**.
Beyan edilen **%17,63 – %22,84** ile uyumlu.
🔴 **Ama tek tohumdan — bkz. B-123 ve F7.**

### F3 / F6 — 🔴 **B0 BİR SAYIYI HAKSIZ YERE ÇÜRÜTTÜ.** Analitik band yeniden türetildi

**B0'ın türetmesi.** Çarpıklık = tüm koşu / pencere. Sayaç zaman içinde
**düzgün** üretiliyorsa:

- yalnızca beacon *(0 → `kosu_bitis_s`)*: 350 / 270 = **1,296296**
- yalnızca onay *(0 → `olcum_bitis_s`)*: 320 / 270 = **1,185185**

🟢 **Aritmetik doğrudur** *(pencere = 320 − 50 = 270 s)*.
🔴 **Ama bu bir ANALİTİK SINIR DEĞİLDİR — üç varsayıma dayanır:**
*(i)* sayaç zamanda **düzgün** üretilir, *(ii)* üretim **[0, kosu_bitis]**
aralığındadır, *(iii)* pencere **[50, 320]**'dir. Üçü de kırılıyor:

**Kanıt 1 — aracın KENDİ çıktısında:**

| sayaç | çarpıklık | band [1,1852 · 1,2963] dışında mı |
|---|---|---|
| `kontrol_bayt` | 1,2221 – 1,2963 | hayır |
| `kontrol_airtime_s` | 1,2126 – 1,2963 | hayır |
| **`beacon_gonderilen`** | **1,2942 – 1,3398** | 🔴 **EVET (üstten)** |
| **`veri_bayt`** | **1,1786 – 1,2573** | 🔴 **EVET (alttan)** |
| **`mac_deneme`** | **1,1786 – 1,2573** | 🔴 **EVET (alttan)** |

Yani varsayım *(i)* deponun kendi sayaçlarında yanlış.

**Kanıt 2 — bandın konuştuğu sayacın kendisi, BAŞKA BİR TOHUMDA dışarı
çıkıyor:**

```
hedefe_en_yakin / S2 / orta / tohum 4
  carpiklik (tum kosu / pencere) = 1,299260
  analitik ust capa 350/270      = 1,296296
  BAND DISINDA MI: True
```

**Kanıt 3 — 1,004–1,079 doğrudan üretilebiliyor** *(varsayım (iii) kırılır)*:

| yapılandırma | çarpıklık | 1,004–1,079 içinde mi |
|---|---|---|
| deponun bugünkü noktası *(50/320/350)* | 1,2652 | hayır |
| `isinma_s` = 5, pencere = koşu | **1,0144** | 🔴 **EVET** |
| `isinma_s` = 15, pencere = koşu | **1,0446** | 🔴 **EVET** |
| `isinma_s` = 25, pencere = koşu | **1,0766** | 🔴 **EVET** |

⚖️ **Kayıp betiğin *"8 yapılandırma"*sının ne olduğu hiçbir belgede yazılı
değil** — ve `isinma_s` üzerinde 8 noktalı bir tarama, ilan edilmiş
1,004–1,079 bandını **neredeyse birebir** üretir *(1,0144 ↔ 1,0766)*.
Bu bir **kanıt değil**, ama *"olamaz"* iddiasını çürütmeye fazlasıyla
yeter.

🔴 **Ve F3'ün asıl bedeli:** aynı yanlış varsayım
`pencere_kapsami.py:207`de bir **`assert`e** dönüşmüş durumda. Tohum 4'te
araç **çöküyor** *(§0'daki çıktı)*. `08` md 31'in yeni üreticisi, bugün
**yalnızca tohum 1'de koşabilen** bir araçtır.

**Kapanış önerisi:**
1. `08` md 31'den *"olamaz / analitik olarak hapistir"* ifadesi çıkarılsın;
   yerine *"bugünkü çalışma noktasında **ölçülen** band 1,2221–1,2963'tür;
   ilan edilmiş 1,004–1,079 bu noktada üretilemiyor, **hangi çalışma
   noktasından geldiği bilinmiyor**"* yazılsın.
2. `pencere_kapsami.py`nin `assert`i **kaldırılmasın, gevşetilmesin** —
   **doğru büyüklüğe** bağlansın: `olu` kolunun *(yalnız beacon)* çapaya
   birebir oturması **korunur** *(o kontrol doğru ve değerli)*; diğer
   kolları bir banda hapseden ikinci `assert` **bir uyarıya** dönüşsün.

### F4 — 🟢 `08` Ç4 · Li @2 Mbit/s: **DÖRDÜ DE BİREBİR** *(koşularak)*

`python dogrulama/li_calisma_noktasi.py` — **11,1 sn**:

| büyüklük | Li vd. | bu araç | fark | `08` Ç4 |
|---|---|---|---|---|
| tek atlama tavanı | 1,700 | **1,761 Mbps** | +%3,6 | 🟢 birebir |
| uzun zincir | 0,250 | **0,277 Mbps** | +%10,8 | 🟢 birebir |
| plato | 1/7 | **1/6,355** *(→ 1/6,36)* | −%9,2 | 🟢 birebir |
| plato %95 GA genişliği | — | **%1,54** | — | 🟢 birebir |
| *(1 Mbit/s)* | — | 0,932 / 0,148 / **1/6,29** *(GA %2,04)* | — | 🟢 birebir |

⚠️ `06` Bölüm 10 aynı büyüklüğü **1/6,30** diye taşıyor, `08` **1/6,29**
diyor, araç **1/6,29** basıyor → **B-141**.

### F5 — 🟢 **AYNI KOLLAR** karşılaştırılıyor — ama kol tanımı bir yerde bulunmuyor

`kontrol_payi.py:193` — `("DV", mesafe_vektoru)` ve
`("gurultuden_kacan", AKTARICILAR["gurultuden_kacan"])`. Eski ölçümle
**aynı çift**. 🟢 F5 temiz.

🔴 **Ama bir yan bulgu çıktı — B-135:** `mesafe_vektoru`
`dogrulama/kontrol_payi.py:52`de tanımlı ve **`AKTARICILAR`da YOKTUR**:

```
AKTARICILAR: ['en_kisa_yol','hedefe_en_yakin','dongu_yapan','olu','gurultuden_kacan']
kontrol_payi.mesafe_vektoru AKTARICILAR icinde mi: False
```

Sonucu: `gecerlilik.py`nin `KOLLAR`ı yalnızca `AKTARICILAR`dan seçilebildiği
için **koşul 3'ü ölçen araç, `08` md 25'in bağlayıcı oranını üreten kolu
ÖLÇEMEZ.** İki araç koşul 3 için **iki farklı kol çiftinde** iki farklı
sayı basıyor:

| araç | kol çifti | eşleştirilmiş oran |
|---|---|---|
| `kontrol_payi.py` → `08` md 25 | **DV** ↔ `gurultuden_kacan` | **4,0 – 38,0 kat** |
| `gecerlilik.py` → koşul 3 çıktısı | `en_kisa_yol` ↔ `gurultuden_kacan` | **1,53 – 3,62 kat** *(ortanca 2,18)* |

Hangisinin *"koşul 3'ün bağlayıcı sayısı"* olduğu **hiçbir belgede
yazmıyor**.

### F7 — 🔴 Matris **sayıyı tutturmak için seçilmemiş** ama **TEK TOHUMLUK**. **B-123**

`dogrulama/pencere_kapsami.py:56` → `TOHUM = 1`.

🔴 **`03` kural 2:** *"Tek/az tohumlu sonuç raporlama. ≥30 tohum + güven
aralığı."* B0 aynı oturumda `08` md 25'i **3 tohumdan 30 tohuma** taşıdı
ve gerekçe olarak tam bu kuralı gösterdi — ve **md 31'e 1 tohumluk bir
band yazdı.**

**Ölçüldü** *(aynı matris, 5 tohum, 150 tam koşu, 147 sn)*:

| tohum | pay bandı | ortanca | çarpıklık bandı |
|---|---|---|---|
| **1** *(`08`in ilan ettiği)* | **%18,17 – %22,86** | %21,06 | 1,2221 – 1,2963 |
| 2 | %19,09 – %22,86 | %21,12 | 1,2359 – 1,2963 |
| 3 | **%16,62** – %22,86 | %21,21 | **1,1993** – 1,2963 |
| 4 | %18,93 – **%23,03** | %21,38 | 1,2335 – **1,2993** |
| 5 | %17,95 – %22,86 | %20,76 | 1,2188 – 1,2963 |
| **BEŞİ BİRDEN (n = 150)** | **%16,62 – %23,03** | **%21,09** | **1,1993 – 1,2993** |

🟢 **Ortanca kararlı** *(%21,06 → %21,09)* — matris sayıyı tutturmak için
seçilmiş **değil**.
🔴 **Ama band iki uçtan da genişliyor** *(%16,62 alt, %23,03 üst)* ve
**tohum 4'te araç çöküyor**. Tek tohumluk band, gerçek bandı **her iki
uçtan da dar gösteriyor**.

### F8 — 🔴 `08`in *"229 mutant hiç sınanmadı"* satırı **BAYAT**. **B-139**

```
kor havuz bugun: 255   (`08` md 30 satiri: 229, havuz 253)
```

`08` satırı 27 Ağustos'ta 179 → 229'a güncellenmişti *(havuz 203 → 253)*.
Havuz **koddan üretiliyor ve kodla büyüyor**; B0 `sim/karsilastirma.py`ye
dokununca **253 → 255** oldu.

**`08`e ne yazılmalı:** *"**231 mutant hiç sınanmadı**"* — havuz **255**,
örneklem **24**. Ve satırın yanına Y12 deseninde bir not: *"bu sayı `sim/`
her değiştiğinde bayatlar; üreticisi tek komuttur."*

⚠️ **Daha iyisi:** sayıyı belgeye yazmak yerine bir **ucuz teste** bağlamak
*(Y12)* — `08`in beyanı ile `mutantlari_uret()`in uzunluğu karşılaştırılsın.
Bu satır **iki denetimde iki kez** bayatladı; üçüncüsü olmasın.

---

## 7. YENİ BULGULAR — B-120 … B-142

> Her satırın **üretici komutu §14'tedir** ve **yayımlanmadan önce olduğu
> gibi koşturulmuştur.**

| # | bulgu | kaynak | ağırlık |
|---|---|---|---|
| **B-120** | 🔴 `08` md 31'in *"analitik band [1,1852 · 1,2963]"* iddiası **yanlış** — üç yoldan kırılıyor; ve `pencere_kapsami.py:207`deki `assert` yüzünden araç **tohum 4'te ÇÖKÜYOR** | `v2/08:363` · `dogrulama/pencere_kapsami.py:181–208` | 🔴🔴 **en ağır** |
| **B-121** | 🔴 `06` §8.1b'nin **HAM p95** satırı *(17/30, p = 0,5847)* ilan edilen üreticiden **çıkmıyor**; `kosul2` üç okuma üretiyor | `v2/06:541` · `dogrulama/gecerlilik.py:173` | 🔴🔴 |
| **B-122** | 🔴 K-086 §7.1'in *"iki bağımsız ölçüm hattı"* kanıtı **tautoloji**: 120 iş bit-birebir aynı | `v2/04` K-086 §7.1 | 🔴🔴 |
| **B-123** | 🔴 `08` md 31'in yeni bandı **TEK TOHUMDAN** *(`TOHUM = 1`)* — `03` kural 2'nin, B0'ın md 25'te düzelttiği ihlalin aynısı | `dogrulama/pencere_kapsami.py:56` | 🔴🔴 |
| **B-124** | 🔴 `isaret_testi`: `medyan_fark` **HAM**'dan, `ga` **NET**'ten — iki ayrı estimand; beraberlik varsa medyan **kendi GA'sının dışına** düşüyor | `dogrulama/isaret_testi.py:126,143` | 🔴 |
| **B-125** | 🔴 Ölçüt **büyüklüğü serbest bırakıyor**: 16/30 + 2σ **geçiyor**, 20/30 + 5σ **geçiyor** | `dogrulama/isaret_testi.py:139` | 🔴 |
| **B-126** | 🔴 §9.1, `06` Bölüm 7'nin **kendi iki şartını** sağlamıyor: güç yazılmıyor · ε_rel ≤ %10 **12/12 sağlanmıyor** | `v2/06:602–640` vs `v2/06:436–447` | 🔴 |
| **B-127** | 🔴 *"Rapora giren kollar için bağlayıcı"* daraltması koşul 1'i **fiilen boşaltıyor** — bugün bağlanan kol **sıfır**, düşen iki çift **muaf** | `v2/06:632–637` | 🔴 |
| **B-128** | 🔴 `yuzdelik` bugün **ÜÇ üretim gövdesi** taşıyor *(`sim/karsilastirma.py:63` · `literatur_eksenleri.py:137` · `sjr_donusumu.py:110`)*; K-086 *"tek gövde"* diyor ve `06` §8.1'in tablosunu üreten gövde **ikincisidir** | K-086 §5 | 🔴 |
| **B-129** | 🔴 Kapının bayatlığı **8 belgede** güncellenmemiş; `13` §3.1 bugün **`False`** basan bir komutu *"kriptografik kanıt"* diye taşıyor | `v2/13:96–111` · `README:33` · `06:152` · `07:16` · `08:14` · `09:58` · `12:63` · `04:7478` | 🔴 |
| **B-130** | 🔴 Üç yeni aracın *(gecerlilik · pencere_kapsami · li_calisma_noktasi)* mutasyon kapsamı **0/10**, `%95 GA [0 · %27,8]`; **hiçbir test modülü onları içe aktarmıyor** *(ölçüldü)* | §3 | 🔴 |
| **B-131** | 🔴 A-14'ün **16 mutasyonu** `mutasyon_paketi.py`ye **girmedi**; kapının hedefli havuzunda `sim/karsilastirma.py` hâlâ **1** mutasyon taşıyor *(Y13: kapanış kodda mı?)* | `dogrulama/mutasyon_paketi.py:695` | 🔴 |
| **B-132** | 🔴 `08` Ç4'ün dört sayısını üreten `li_calisma_noktasi.py` **hiçbir sonuç satırı yazmıyor** *(`kayit(` = 0)*; ve B-106 koruması onu **göremiyor** — `olc`u dolaylı kullanıyor, `li_zincir` ise `Kosu`yu hiç kullanmıyor | `dogrulama/li_calisma_noktasi.py` · `tests/test_kapi_secimleri.py:1360` | 🔴 |
| **B-133** | 🔴 Sonuç satırı **koşuyu tanımlamıyor**: ne zaman damgası ne koşu kimliği var. `pencere_kapsami.jsonl`de **aynı hash altında 30 iş İKİ KEZ** duruyor ve ayırt edilemiyor | `sim/results.py:78–84` | 🔴 |
| **B-134** | 🔴 Dejenere kontrol payı **gecikme karşılaştırmasını da** öldürüyor: 801 ortak paketlik geçerli bir fark *(+10,140 ms)* üretilemiyor | `sim/karsilastirma.py:412` | 🟡 |
| **B-135** | 🔴 `mesafe_vektoru` *(DV)* `AKTARICILAR`da **yok**; koşul 3 iki araçta **iki farklı kol çiftiyle** iki farklı sayı üretiyor *(4,0–38,0 kat ↔ 1,53–3,62 kat)* ve hangisinin bağlayıcı olduğu yazılı değil | `dogrulama/kontrol_payi.py:52` vs `dogrulama/gecerlilik.py:69` | 🟡 |
| **B-136** | 🔴 §8.1b **tek koldan** yazılmış; `gurultuden_kacan`ın **ters** sonucu *(ORTAK p95 −263,03 ms, p = 0,0428)* araç tarafından basılıyor ama belgede **yok** | `v2/06:529–573` | 🟡 |
| **B-137** | ⚠️ `kayit(dosya=…)` koruması yalnızca **yorumda** *("üretim aracı bu parametreyi HİÇ vermez")* — bir test onu zorlamıyor. **BEYAN ≠ ETKİ** | `dogrulama/olcum.py:107–113` | 🟡 |
| **B-138** | ⚠️ README'nin *"Kod — ölçüldü, 27 Ağustos"* bloğu **tamamen bayat**: 4 401/9 341/5 466 · 429 test · 25 araç · 79 alan → ölçülen **4 519/9 945/7 329** · **462** test · **31** araç · **77 metrik + 47 konfig** | `README:128–146` | 🟡 |
| **B-139** | ⚠️ `08`in *"229 mutant hiç sınanmadı"* satırı **bayat** — kör havuz bugün **255**, doğrusu **231** | `v2/08:463` | 🟡 |
| **B-140** | ⚠️ Ortak alt küme okumasının **kesişim ALT SINIRI yok**; ölçülen en dar hücre **%5,6** *(`gurultuden_kacan`)* | `v2/06:558` · `sim/karsilastirma.py:170` | 🟡 |
| **B-141** | ⚠️ Aynı büyüklük iki belgede iki değerde: `06` Bölüm 10 **1/6,30**, `08` Ç4 ve araç **1/6,29** | `v2/06:645` vs `v2/08:155` | 🟢 küçük |
| **B-142** | ⚠️ `06` §8.1'in eski tablosundaki *"p95 +%26,0 🟢 **gerçek**"* satırı §8.1b tarafından çürütüldü *(HAM p95 p = 0,5847)* ama **işareti geri alınmadı** | `v2/06:519` | 🟢 küçük |

---

## 8. B0'IN DÖRT KAPANIŞI — bağımsız doğrulama

| kalem | B0'ın iddiası | bu denetimin yargısı |
|---|---|---|
| **D-13** | 🟢 KAPANDI | 🟡 **KOŞULLU** — şekli doğru ve **540 koşuda güvenli** *(E1: 35,2 MB tavan, ölçüldü)*; ama kanıt hâlâ **2 + 20 koşu**, `aile0_kapi_raporu.jsonl` **0 bayt**, ve `12` §2.1'in ölçütü **değiştirildi** *(bkz. §8.1)* |
| **`06` koşul 2** | 🟢 KAPANDI | 🟡 **KOŞULLU** — reçete gerçekten **sıkılaştı** ve **kodda zorunlu** *(D3: 8/8 kırılarak doğrulandı)*; ama gerekçesinin taşıyıcı satırının üreticisi **yok** *(B-121)*, ikinci kolun ters sonucu **yazılmadı** *(B-136)*, kesişim alt sınırı **konmadı** *(B-140)* |
| **`06` koşul 3** | 🟢 KAPANDI | 🟢 **GEÇERLİ** — F1'in dokuz sayısı **birebir** yeniden üretildi, 30 tohum, 2 dejenere hücre dâhil. 🔴 Tek çekince: koşul 3'ün *"bağlayıcı sayısı"* iki araçta **iki farklı kol çiftinden** geliyor *(B-135)* |
| **F-4** | 🟢 KAPANDI | 🟡 **KOŞULLU** — Ç4'ün dört sayısı **koşularak birebir üretildi** 🟢; md 31'in pay bandı **birebir üretildi** 🟢; ama çarpıklık gerekçesi **yanlış** *(B-120)*, band **tek tohumluk** *(B-123)*, ve iki üreticiden biri **sonuç satırı yazmıyor** *(B-132)* |
| **A-14** *(denetlendi)* | 16/16 mutasyon | 🟡 **ÖLÇÜM DOĞRU, KALICILIĞI YOK** — 16 mutasyonun hiçbiri `mutasyon_paketi.py`ye girmedi; kapının 7. koşusu `karsilastirma.py`yi hâlâ **1 mutasyonla** sınayacak *(B-131)* |

### 8.1 🔴 B0.1'in ölçütü **değiştirildi** — `12` §2.1

| nerede | ölçüt |
|---|---|
| `12` §2.1 **özgün tahmin** tablosu *(planlama)* | *"`aile0_kapi_raporu.jsonl` **satır sayısı = koşu sayısı** (0 bayt değil)"* |
| `12` §2.1 **sonuç** tablosu *(B0 sonrası)* | *"`ana_matris` **2/2** · `uc_durum_matrisi` **20/20** · 3 mutasyon yakalandı"* |

`aile0_kapi_raporu.jsonl` bugün **0 bayttır** *(ölçüldü)*. Yani ilan edilen
ölçüt **sağlanmadı**; sağlanan başka bir ölçüttür.

⚖️ **Bu bir hile değildir** — `12` §2.3 gerekçeyi açıkça yazıyor
*(kapı B0+B1'den sonra tek kez koşacak; iki ayrı koşu 6–11 saat eder)* ve
gerekçe **sağlamdır**. 🔴 **Ama sonuç tablosunda "🟢 KAPANDI" yazıyor ve
ölçütün değiştiği yazmıyor.** `03` kural 3'ün ruhu: bir ölçüt
değiştirilecekse, değiştirildiği **yazılır**.

**Kapanış önerisi:** D-13'ün satırı *"🟡 **DÜZELTİLDİ, KANITI B2'DE**"*
olsun; *"KAPANDI"* ancak `aile0_kapi_raporu.jsonl` **560 satır** taşıdığında
yazılsın.

### 8.2 🟢 Şüphe 8'in cevabı: **erteleme varsayımı ÖLÇÜLDÜ ve TUTUYOR**

`12` §2.3 kapıyı B1'den sonraya erteliyor; bu, *"B0'ın hiçbir
değişikliğinin kapı kriterlerini etkilemediği"* varsayımına dayanıyor.
🔴 B0 bu varsayımı **ölçmedi**. Bu denetim ölçtü — iki ayrı yoldan:

| ölçüm | sonuç |
|---|---|
| `89587a19…` *(kapının koştuğu kod)* ↔ `0a1a94e5…` *(bugün)*, **120 ortak iş** | 🟢 **77 metriğin `kaynak_hash` dışındaki hepsi bit-birebir aynı** |
| `cd6d304f…` ↔ `0a1a94e5…`, **240 ortak iş** | 🟢 **bit-birebir aynı** |

🟢 **Simülatörün davranışı değişmedi** — B0'ın iki `sim/` dosyasına
dokunuşu *(karşılaştırma katmanı + bir yorum)* koşu sonuçlarına
yansımıyor. Ç1 *(korunum)*, Ç4 *(Li)* ve sayaç tabanlı kriterler
**etkilenmez.**

🔴 **AMA İKİ KRİTER ETKİLENİR ve bu ölçülmedi:**

| kriter | neden etkilenir |
|---|---|
| **Ç1.3** *(hedefli mutasyon)* | `sim/karsilastirma.py` **değişti** ve pakette o dosyaya ait **1 mutasyon** var; ayrıca test sayısı **429 → 462** ve `08` md 30 mutasyon kapısını paket süresine bağlıyor |
| **Ç3 / kör havuz** | havuz **koddan üretiliyor**: 253 → **255** *(B-139)* |

**Kapanış önerisi:** `12` §2.3'e tek satır — *"B0'ın `sim/` değişikliği
**davranışsal olarak atıldır** (120 + 240 iş bit-birebir, üretici §14);
kapının yeniden koşma gerekçesi **mutasyon havuzunun büyümesi ve test
sayısının artmasıdır**, sonuçların değişmesi değil."*

---

## 9. DOĞRULANAN İDDİALAR

| iddia | kaynak | doğrulama |
|---|---|---|
| `08` md 25 · üç okumanın **dokuz sayısı** | K-086 §3 F-5 | 🟢 **birebir** *(K-F1)* |
| `08` md 25 · **2 dejenere hücre** *(DV, tohum 25)* | K-086 §3 | 🟢 **birebir** — S0 ve S2 |
| `08` md 31 · pencere dışı pay **%18,17–22,86**, ortanca **%21,06** | `08` md 31 | 🟢 **birebir** |
| `08` md 31 · `olu` kolu çapaya **birebir** oturuyor *(sapma 0,000000)* | `08` md 31 | 🟢 **birebir** — 1,296296 = 350/270 |
| `08` Ç4 · **1,761 / 0,277 Mbps · 1/6,36 · GA %1,54** | `08` Ç4 | 🟢 **dördü de birebir**, koşularak *(11,1 sn)* |
| `06` §8.1b'nin **dört sayısı** *(−3,98 · +7,11 · +5,40 · +28,15 ms)* ve dört p'si | `06` §8.1b | 🟢 **birebir** — **iki ayrı dosyadan** *(ama bkz. B-122)* |
| `06` §9.1'in **12 satırı** ve GA/std sütunu | `06` §9.1 | 🟢 **birebir** — 22/30 ve 8/30, ikisi de p = 0,0161; GA/std [+0,045 · +0,253] |
| Ölçüt *"eski yargıları birebir üretiyor"* | `06` §9.1 | 🟢 **doğru** — 15/30 → p = 1,0000 · 8/30 → p = 0,016125 |
| `_PAY_ALANLARI` **hem A hem B** için zorunlu | K-086 §2 | 🟢 **8/8 kırılarak doğrulandı** |
| `ciktilar/sonuclar/` **1 114 satırın 1 114'ü** dört alanı taşıyor | B0 | 🟢 **çürütülemedi**; tam şema listesinde de eksik yok |
| Ortak alt küme **kesişim oranları** *(%51,1 ve %20,7)* | `06` §8.1b | 🟢 **birebir** |
| **462 test geçiyor** | K-086 §8 | 🟢 **462 passed in 1 030,81 sn** *(tam kopyada, 17 dk 10 sn)* |
| Paket süresi bandı **869–1 851 sn** | README | 🟢 **1 030,81 sn** ölçüldü — bandın içinde |
| `sim/` bugünkü hash `0a1a94e5fb24f01605fcf3168519520c` | envanter | 🟢 **birebir** |
| Kör havuz büyüdü | — | 🟢 **255** *(`08` 253 diyor)* |
| `dogrulama/gecikme.py` `yuzdelik`i **içe aktarıyor**, kopyalamıyor | K-086 §5 | 🟢 **doğru** — ama iki başka kopya var *(B-128)* |
| `dogrulama → sim` yönü doğru; **döngüsel içe aktarım yok** | şüphe 2 | 🟢 `sim/karsilastirma.py` yalnızca stdlib içe aktarıyor |
| `kayit(dosya=…)` **üretimde kullanılmıyor** | şüphe 3 | 🟢 tek kullanıcı `tests/test_kapi_secimleri.py:1487` — ama koruma yok *(B-137)* |

---

## 10. ÜRETİLEMEYEN İDDİALAR

| iddia | kaynak | ne oldu |
|---|---|---|
| 🔴 **HAM p95 = +7,11 ms · 17/30 · p = 0,5847** | `06` §8.1b · `04` K-086 §2 · `11` §229 · bu denetimin promptu | **İlan edilen üretici bu satırı basmıyor.** Sayı **doğru** *(bağımsız hesapla birebir çıktı)* ama `03` kural 1 anlamında **üretilemiyor** — **B-121** |
| 🔴 **Çarpıklık 1,004–1,079 "olamaz"** | `08` md 31 | **Çürütüldü.** Üç ayrı yoldan üretildi/kırıldı — **B-120** |
| 🔴 **`aile0_kapi_raporu.jsonl` satır sayısı = koşu sayısı** | `12` §2.1 planlama tablosu | Dosya **0 bayt**. Ölçüt **değiştirildi**, sağlanmadı — §8.1 |
| 🔴 **Kapı "bayat değil" · komut çıktısı `… True`** | `13` §3.1 · `README:33` · `06:152` · `07:16` · `08:14` · `09:58` · `12:63` | Bugün **`False`** basıyor — **B-129** |
| 🔴 **229 mutant hiç sınanmadı** | `08` md 30 | Havuz **255**; doğrusu **231** — **B-139** |
| ⚠️ **`yuzdelik`in tek gövdesi var** | K-086 §5 | **Üç** üretim gövdesi bulundu — **B-128** |
| ⚠️ **README'nin kod envanteri** *(4 401 / 9 341 / 5 466 · 429 · 25 · 79)* | `README:128–146` | Ölçülen: **4 519 / 9 945 / 7 329 · 462 · 31 · 77+47** — **B-138** |
| ⚠️ **1/6,30** | `06` Bölüm 10 | Araç **1/6,29** basıyor, `08` de öyle diyor — **B-141** |

---

## 11. KAPSAM BEYANINA EKLENECEKLER — `08`e madde önerisi

| # | önerilen madde |
|---|---|
| **K-1** | 🔴 **Çarpıklık bandı analitik değil ampiriktir.** `tüm koşu / pencere` oranı, sayacın zaman içindeki üretim profiline ve pencere yapılandırmasına bağlıdır; deponun kendi sayaçlarından **üçü** bugünkü `[1,1852 · 1,2963]` bandının dışındadır *(`beacon_gonderilen` 1,3398 · `veri_bayt`/`mac_deneme` 1,1786)* |
| **K-2** | 🔴 **md 31'in bandı TEK TOHUMDAN ölçülmüştür** *(`TOHUM = 1`)*. Beş tohumda band **%16,62 – %23,03**'e genişler ve **tohum 4'te üretici çöker**. `03` kural 2 gereği ya 30 tohuma çıkarılmalı ya da *"tek tohumluk"* olduğu maddede yazmalı |
| **K-3** | 🔴 **Ortak alt küme okumasının kesişim alt sınırı YOKTUR.** Ölçülen en dar hücre **%5,6**; `ortak_alt_kume` yalnızca `ortak_paket == 0`ı reddeder. Faz 1'de teslim oranları ayrıştıkça kesişim daralacaktır |
| **K-4** | 🔴 **Koşul 1'in testi, adı ne olursa olsun, "koşu uzunluğu" ölçmez.** Simülatör nedensel ve belirlenimcidir; kısa ve tam koşu ortak kimlik aralığında **bit-birebir aynıdır** *(29/30 tohum)*. Ölçülen şey **ölçüm penceresi içindeki ısınma artığıdır** |
| **K-5** | 🔴 **Koşul 1 bugün hiçbir kolu bağlamamaktadır** — ölçülen üç kol da doğrulama aktarıcısıdır. Bugünkü tablo bir **taban çizgisidir**, bir geçerlilik kanıtı değil |
| **K-6** | 🔴 **Dejenere kontrol payı, gecikme karşılaştırmasını da geçersiz kılar.** `ortak_alt_kume` kontrol payı tanımsızken **hiçbir sayı üretmez**; bu, `06` koşul 3'ün bilinçli bir yorumudur ve bedeli yazılmalıdır |
| **K-7** | 🔴 **Sonuç satırı koşuyu tanımlamaz.** `kaynak_hash` kod sürümünü ayırır, **koşuyu ayırmaz**; aynı kod sürümünde iki kez koşan bir araç `.jsonl`de ayırt edilemez *(bugün `pencere_kapsami.jsonl`de 30 tekrarlı iş var)*. Dosyaları okuyan her analiz bunu **kendi** ele almak zorundadır |
| **K-8** | 🔴 **`dogrulama/li_zincir.py` `sim/kosucu.py::Kosu`yu kullanmaz** — kendi MAC seviyesi doymuş-zincir harness'ını kurar. Dolayısıyla `08` Ç4'ün sayıları `kaynak_hash` taşıyan hiçbir satır bırakmaz ve `03` Bölüm C sözleşme 5'in dışındadır |
| **K-9** | ⚠️ **Koşul 3'ün bağlayıcı oranı iki farklı kol çiftinde iki farklı değerdir** *(DV ↔ gözlem: 4,0–38,0 kat · kâhin ↔ gözlem: 1,53–3,62 kat)*. Hangisinin bağlayıcı olduğu ilan edilmelidir |

---

## 12. 🔴 ANLAŞILMAYANLAR — A-17'den devam

| # | ne anlaşılmadı |
|---|---|
| **A-17** | 🔴 **`hedefe_en_yakin` neden analitik üst çapayı aşıyor?** Ölçüldü *(1,2993 > 1,2963)*, **sebebi ölçülmedi.** Aday: ısınma sırasında topoloji/komşuluk kararsızlığı kontrol baytını orantısız olarak `[0, 50]` aralığında üretiyor olabilir. `03` B4: bir kusuru ölçmek onu SEBEP yapmaz — **bu bir hipotezdir, ölçüm değil** |
| **A-18** | 🔴 **`beacon_gonderilen` çarpıklığı neden 1,3398'e kadar çıkıyor?** Beacon üretimi tanım gereği düzgün olmalıydı *(`olu` kolunda tam 1,2963 çıkıyor)*. Diğer kollarda neden sapıyor — beacon zamanlayıcısının jitter'ı mı, ilk beacon'ın ofseti mi? Ölçmedim |
| **A-19** | 🔴 **Koşul 3'ün bağlayıcı sayısı hangisi?** `08` md 25 DV ↔ gözlem *(4,0–38,0 kat)*, `gecerlilik.py` kâhin ↔ gözlem *(1,53–3,62 kat)*. İkisi de *"eşleştirilmiş kol oranı"* diye basılıyor. Hangisinin `06` koşul 3'ü karşıladığını **hiçbir belgeden çıkaramadım** |
| **A-20** | ⚠️ **`aile0_kapi_raporu.jsonl` 27 Ağustos 20:11'de neden oluşturuldu ve neden 0 bayt?** D-13 bunu *"işçiler yazmadı"* diye açıklıyor; ama dosya **var** ve boş — yani yazıcı **açıldı**, hiç satır yazmadı. Bu D-13'ün açıklamasıyla tutarlı, ama git komutu çalıştıramadığım için dosyanın o günden beri dokunulmadığını **doğrulayamadım** |
| **A-21** | ⚠️ **`I1` eşdeğer mutantı yalnızca n ≤ 60 için doğrulandı.** Kesin binom p değerinin tam 0,05'e eşit olamayacağını n = 1…60 aralığında ölçtüm; **genel bir kanıt vermedim**. Faz 1'de n değişirse yeniden bakılmalı |
| **A-22** | ⚠️ **`06` §8.1'in havuzlanmış tablosunun** *(45,83 → 44,29 ms · p95 92,04 → 115,95)* bugünkü kodla yeniden üretilebilirliğini **ölçmedim.** `literatur_eksenleri.jsonl` eski hash'te *(89587a19)* ve tablo havuzlanmış okumadan geliyor; §8.1b onu *"betimleyici"* ilan ettiği için önceliklendirmedim. 🔴 **Ama tablo hâlâ `06`da duruyor ve mühre gidiyor** |
| **A-23** | ⚠️ **Kapı 7. koşusunun süresine B0'ın etkisini ölçmedim.** `08` md 30 mutasyon kapısını paket süresine bağlıyor; test sayısı %7,7 arttı. K-086 *"165–330 dk bandının üst yarısına kayabilir"* diyor — bu bir tahmindir ve **doğrulamadım** *(kapıyı koşturmak izin gerektirirdi)* |
| **A-24** | ⚠️ **`gurultuden_kacan`ın ORTAK p95'inin neden TERSİNE gittiğini** *(−263 ms, p = 0,0428)* ölçmedim. Kesişimin **%20,7** olması *(min %5,6)* akla yatkın bir aday; ama bu bir hipotezdir — kesişimi yapay olarak daraltıp farkın nasıl kaydığını ölçmedim |

---

## 13. 🔴 SENİN YARGIN

> ## **B0'ın kapattığı dört kaleme KISMEN GÜVENİLİR, çünkü…**

…**ölçümleri sağlam, gerekçeleri değil.**

Somut olarak: F1'in dokuz sayısını, F2'nin bandını, F4'ün dördünü, §8.1b'nin
dördünü ve §9.1'in on ikisini **bağımsız olarak, farklı kodla, birebir
yeniden ürettim.** B0 hiçbir sayıyı uydurmadı, hiçbir sayıyı süslemedi,
kendi lehine hiçbir eşiği gevşetmedi — `03` kural 3 **ihlal edilmemiştir**
ve reçete değişikliği **sıkılaştırmadır**, gevşetme değil.

🔴 **Ama üç yerde ölçüt yanlış nesneye uygulanmış:**

1. **Bir sayıyı "imkânsız" ilan etti** — ve imkânsızlığın kendi çalışma
   noktasına bağlı olduğunu ölçmedi. Aynı iddia, aracın **kendi çıktı
   dosyasında** üç sayaç tarafından, **kendi tohum kümesinde** bir kol
   tarafından ve **başka bir pencere yapılandırmasında** doğrudan
   çürütülüyor. Üstelik iddia bir `assert`e dönüşüp aracı **tohum 4'te
   çökertiyor**.
2. **"İki bağımsız boru hattı"** dediği şey, aynı deterministik koşuların
   iki kez okunmasıydı. **Y6'nın tam olarak uyardığı şey:** kendi lehine
   çıkan sonuç, kötü çıkan kadar şüphelidir.
3. **`03` kural 2'yi bir maddede uygularken bir başkasında ihlal etti** —
   md 25'i 3 tohumdan 30'a taşıdı, md 31'e **1 tohumluk** bir band yazdı.

Ve bir yerde **kendi ölçütünü kendisi doğruladı ve doğrulama boştu:** üç
yeni aracın *(biri `06`nın üç geçerlilik koşulunun tamamını üreten araç)*
mutasyon kapsamı **0/10**, ve o üç dosyayı **hiçbir test modülü içe
aktarmıyor**. B0 `sim/karsilastirma.py`nin kapsamını **ölçtü ve 16/16'ya
çıkardı**; kendi yazdığı beş aracın kapsamını **hiç sormadı**.

⚖️ **Örüntü kapanmadı — ama yeri değişti.** Altıncı denetim şunu yazmıştı:
*"bu denetimin en pahalı üç bulgusu doğrulama araçlarının kendisinde."*
Yedincisinde **beş bulgunun beşi de** orada, ve artık **ölçütün kendisinde**:
bir ölçütü seçen taraf, o ölçütün **hangi nesneye uygulandığını** denetleyen
taraf olamıyor.

🟡 **B1'e geçilebilir** — ama B-120, B-121, B-123 ve B-133 kapanmadan
şema **dondurulmamalıdır.** Bunların dördü de birkaç saatlik iştir; şema
donduktan sonra hiçbiri düzeltilemez.

---

## 14. KOŞTURDUĞUM KOMUTLAR

> 🔒 **Aşağıdaki 16 komutun tamamı, yayımlanmadan önce depo kökünden
> OLDUĞU GİBİ koşturuldu** *(tek dosyada, `bash` ile, ardışık)*. Hepsi
> `PYTHONIOENCODING=utf-8` ve `PYTHONDONTWRITEBYTECODE=1` ile koşar ve
> **depoya hiçbir şey yazmaz**. Raporun her sayısı bu çıktılardan gelir.

### 14.0 Ortam

```bash
export PYTHONIOENCODING=utf-8
export PYTHONDONTWRITEBYTECODE=1
```

### K1 — B-120a · analitik band, aracın KENDİ verisiyle

```bash
python - <<'PY'
import sys, json; sys.path.insert(0, ".")
K = {}
for l in open("ciktilar/sonuclar/pencere_kapsami.jsonl", encoding="utf-8"):
    r = json.loads(l)
    if r["kaynak_hash"] != "0a1a94e5fb24f01605fcf3168519520c": continue
    K[(r["kol_adi"], r["senaryo_etiket"], r["trafik_etiket"])] = r["metrikler"]
ornek = next(iter(K.values())); bas, bit = ornek["olcum_penceresi_s"]
pen = bit - bas; alt = 320.0 / pen; ust = 350.0 / pen
print("analitik band (`08` md 31): [%.4f , %.4f]" % (alt, ust))
for sayac in ("kontrol_bayt", "veri_bayt", "kontrol_airtime_s",
              "beacon_gonderilen", "mac_deneme"):
    c = [s[sayac] / s[sayac + "_pencere"] for s in K.values()
         if s.get(sayac) and s.get(sayac + "_pencere")]
    print("  %-20s carpiklik [%.4f , %.4f]   BAND DISINDA: %s"
          % (sayac, min(c), max(c),
             "EVET" if (min(c) < alt - 1e-9 or max(c) > ust + 1e-9) else "hayir"))
PY
```

### K2 — B-120b · band tohum 4'te kendi sayacında kırılıyor *(~4 sn)*

```bash
python - <<'PY'
import sys; sys.path.insert(0, ".")
from sim.config import Konfig
from sim.kosucu import Kosu
from dogrulama.aktaricilar import AKTARICILAR
s = Kosu(Konfig(kol="x", senaryo="S2", trafik="orta", tohum=4),
         AKTARICILAR["hedefe_en_yakin"]).kostur()
c = s["kontrol_bayt"] / s["kontrol_bayt_pencere"]
print("hedefe_en_yakin / S2 / orta / tohum 4")
print("  carpiklik = %.6f" % c)
print("  analitik ust capa 350/270 = %.6f" % (350.0 / 270.0))
print("  BAND DISINDA MI: %s  -> `pencere_kapsami.py:207` bu tohumda COKER"
      % (c > 350.0 / 270.0))
PY
```

### K3 — B-120c · 1,004–1,079 başka pencerede ÜRETİLİYOR *(~12 sn)*

```bash
python - <<'PY'
import sys; sys.path.insert(0, ".")
from sim.config import Konfig
from sim.kosucu import Kosu
from dogrulama.aktaricilar import AKTARICILAR
print("%-34s %10s %8s" % ("yapilandirma", "carpiklik", "1,004-1,079?"))
for ad, i, o, k in (("deponun bugunku noktasi", 50.0, 320.0, 350.0),
                    ("isinma 5,  pencere = kosu",  5.0, 350.0, 350.0),
                    ("isinma 15, pencere = kosu", 15.0, 350.0, 350.0),
                    ("isinma 25, pencere = kosu", 25.0, 350.0, 350.0)):
    s = Kosu(Konfig(kol="x", senaryo="S0", trafik="orta", tohum=1,
                    isinma_s=i, olcum_bitis_s=o, kosu_bitis_s=k),
             AKTARICILAR["en_kisa_yol"]).kostur()
    c = s["kontrol_bayt"] / s["kontrol_bayt_pencere"]
    print("%-34s %10.4f %8s" % (ad, c, "EVET" if 1.004 <= c <= 1.079 else "hayir"))
PY
```

### K4 — B-121 · HAM p95'in üreticisi yok, sayı yine de doğru

```bash
python - <<'PY'
import sys, json, inspect; sys.path.insert(0, ".")
from sim.karsilastirma import ortak_alt_kume, yuzdelik
from dogrulama.isaret_testi import isaret_testi, satir
import dogrulama.gecerlilik as GV
kaynak = inspect.getsource(GV.kosul2)
print("`gecerlilik.py::kosul2`un URETTIGI okumalar:",
      [a for a in ("HAM ortalama", "HAM p95", "ORTAK ortalama", "ORTAK p95")
       if '"%s"' % a in kaynak])
V = {}
for l in open("ciktilar/sonuclar/gecerlilik.jsonl", encoding="utf-8"):
    r = json.loads(l)
    if r["kaynak_hash"] != "0a1a94e5fb24f01605fcf3168519520c" or r["uzunluk"] != "tam":
        continue
    V[(r["kol_adi"], r["senaryo_etiket"], r["konfig"]["tohum"])] = r["metrikler"]
ho, hp, oo, op = [], [], [], []
for t in range(1, 31):
    a, b = V[("en_kisa_yol", "S0", t)], V[("en_kisa_yol", "S2", t)]
    o = ortak_alt_kume(a, b)
    ho.append(1e3 * o.ham_fark_s); oo.append(1e3 * o.gecikme_farki_s)
    op.append(1e3 * o.p95_farki_s)
    hp.append(1e3 * (yuzdelik(b["teslim_gecikmeleri_s"], .95)
                     - yuzdelik(a["teslim_gecikmeleri_s"], .95)))
for ad, f in (("HAM ortalama", ho), ("HAM p95 (URETICISI YOK)", hp),
              ("ORTAK ortalama", oo), ("ORTAK p95", op)):
    print("  " + satir(ad, isaret_testi(f)))
PY
```

### K5 — B-122 · *"iki boru hattı"* bağımsız değil

```bash
python - <<'PY'
import json, collections
def yukle(ad, sec, anah):
    d = {}
    for l in open("ciktilar/sonuclar/%s.jsonl" % ad, encoding="utf-8"):
        r = json.loads(l)
        if sec(r): d[anah(r)] = r["metrikler"]
    return d
LE = yukle("literatur_eksenleri",
           lambda r: r.get("eksen") == "paket_boyutu" and r.get("paket_bayt") == 1024,
           lambda r: (r["kol_adi"], r["senaryo_etiket"], r["konfig"]["tohum"]))
GE = yukle("gecerlilik", lambda r: r["uzunluk"] == "tam"
           and r["kaynak_hash"] == "0a1a94e5fb24f01605fcf3168519520c",
           lambda r: (r["kol_adi"], r["senaryo_etiket"], r["konfig"]["tohum"]))
ortak = set(LE) & set(GE); fark = collections.Counter(); ayni = 0
for k in ortak:
    d = [a for a in set(LE[k]) | set(GE[k]) if LE[k].get(a) != GE[k].get(a)]
    if d:
        for a in d: fark[a] += 1
    else: ayni += 1
print("ortak is: %d | metrik seti BIT-BIREBIR ayni: %d" % (len(ortak), ayni))
print("farklilasan alan:", dict(fark))
PY
```

### K6 — B-124 · B-125 · ölçütün iki kusuru

```bash
python - <<'PY'
import sys; sys.path.insert(0, ".")
from dogrulama.isaret_testi import isaret_testi
r = isaret_testi([0.0] * 20 + [5.0] * 6 + [4.0] * 4, tohum_std=1.0)
print("B-124: n_ham=%d berabere=%d n=%d p=%.6f GECTI=%s"
      % (r["n_ham"], r["berabere"], r["n"], r["p"], r["gecti"]))
print("       medyan_fark=%+.4f (HAM)   GA=[%+.2f,%+.2f] (NET)"
      % (r["medyan_fark"], r["ga"][0], r["ga"][1]))
print("       medyan KENDI GA'sinin icinde mi: %s"
      % (r["ga"][0] <= r["medyan_fark"] <= r["ga"][1]))
for ad, f in (("B-125  16/30, +2 std", [+2.0] * 16 + [-0.001] * 14),
              ("B-125b 20/30, +5 std", [+5.0] * 20 + [-0.1] * 10)):
    x = isaret_testi(f, tohum_std=1.0)
    print("%s: %d/%d p=%.4f GECTI=%s medyan=%+.2f (= std x %+.2f)"
          % (ad, x["pozitif"], x["n"], x["p"], x["gecti"],
             x["medyan_fark"], x["medyan_fark"]))
PY
```

### K7 — B-126 · `06` Bölüm 7'nin durdurma kuralı

```bash
python - <<'PY'
import sys, json, statistics as ist; sys.path.insert(0, ".")
from sim.karsilastirma import yuzdelik
from dogrulama.isaret_testi import isaret_testi
V = {}
for l in open("ciktilar/sonuclar/gecerlilik.jsonl", encoding="utf-8"):
    r = json.loads(l)
    if r["kaynak_hash"] != "0a1a94e5fb24f01605fcf3168519520c": continue
    V[(r["kol_adi"], r["senaryo_etiket"], r["uzunluk"], r["konfig"]["tohum"])] = r["metrikler"]
def g(m, ne):
    x = m.get("teslim_gecikmeleri_s") or []
    return None if not x else (ist.mean(x) if ne == "ort" else yuzdelik(x, .95))
print("%-18s%-4s%-13s%8s%9s%12s  %s" % ("kol","sen","metrik","n+/n","p","eps_rel %","B7<=%10"))
for kol in ("en_kisa_yol", "gurultuden_kacan"):
    for sen in ("S0", "S2"):
        for ad, f in (("teslim_orani", lambda m: m["teslim_orani"]),
                      ("gecikme ort", lambda m: g(m, "ort")),
                      ("gecikme p95", lambda m: g(m, "p95"))):
            fark = [f(V[(kol,sen,"kisa",t)]) - f(V[(kol,sen,"tam",t)]) for t in range(1,31)]
            r = isaret_testi(fark)
            eps = 100 * ((r["ga"][1]-r["ga"][0])/2) / abs(r["medyan_fark"])
            print("%-18s%-4s%-13s%8s%9.4f%12.1f  %s"
                  % (kol, sen, ad, "%d/%d" % (r["pozitif"], r["n"]), r["p"], eps,
                     "SAGLANDI" if eps <= 10 else "SAGLANMADI"))
PY
```

### K8 — A6 · düşen çiftin SEBEBİ *(ısınma artığı mı, koşu uzunluğu mu)*

```bash
python - <<'PY'
import sys, json, statistics as ist; sys.path.insert(0, ".")
from dogrulama.isaret_testi import isaret_testi, satir
V = {}
for l in open("ciktilar/sonuclar/gecerlilik.jsonl", encoding="utf-8"):
    r = json.loads(l)
    if r["kaynak_hash"] != "0a1a94e5fb24f01605fcf3168519520c": continue
    V[(r["kol_adi"], r["senaryo_etiket"], r["uzunluk"], r["konfig"]["tohum"])] = r["metrikler"]
kol, sen = "en_kisa_yol", "S0"
d1, d2, d3 = [], [], []
for t in range(1, 31):
    a, b = V[(kol, sen, "kisa", t)], V[(kol, sen, "tam", t)]
    alt, ust = a["pencere_kimlik_araligi"]
    erken = [g for k, g in zip(b["teslim_kimlikleri"], b["teslim_gecikmeleri_s"]) if alt <= k <= ust]
    gec = [g for k, g in zip(b["teslim_kimlikleri"], b["teslim_gecikmeleri_s"]) if k > ust]
    d1.append(1e3 * (ist.mean(a["teslim_gecikmeleri_s"]) - ist.mean(b["teslim_gecikmeleri_s"])))
    d2.append(1e3 * (ist.mean(a["teslim_gecikmeleri_s"]) - ist.mean(erken)))
    d3.append(1e3 * (ist.mean(erken) - ist.mean(gec)))
print("  " + satir("KISA - TAM        (§9.1)", isaret_testi(d1)))
print("  " + satir("KISA - TAM_ERKEN  (dinamik)", isaret_testi(d2)))
print("  " + satir("TAM_ERKEN - TAM_GEC (konum)", isaret_testi(d3)))
PY
```

### K9 — B-128 · `yuzdelik`in ÜÇ üretim gövdesi

```bash
python - <<'PY'
import pathlib
kalip = "int(round(p * (len(s) - 1)))"
for yol in sorted(pathlib.Path(".").rglob("*.py")):
    if "__pycache__" in str(yol): continue
    t = yol.read_text(encoding="utf-8")
    if kalip in t:
        print("%-42s satir %s" % (yol.as_posix(),
              [i + 1 for i, l in enumerate(t.splitlines()) if kalip in l]))
PY
```

### K10 — B-131 · B-139 · mutasyon envanteri

```bash
python - <<'PY'
import ast, collections, sys; sys.path.insert(0, ".")
t = ast.parse(open("dogrulama/mutasyon_paketi.py", encoding="utf-8").read())
c = collections.Counter()
for d in ast.walk(t):
    if isinstance(d, ast.Call) and getattr(d.func, "id", None) == "Mutasyon":
        a = d.args
        c[a[1].value if len(a) > 1 and isinstance(a[1], ast.Constant) else "?"] += 1
print("hedefli mutasyon toplam:", sum(c.values()))
for k, v in c.most_common(): print("   %-24s %d" % (k, v))
from dogrulama.kor_mutasyon import mutantlari_uret
print("kor havuz bugun:", len(mutantlari_uret()), "(`08` md 30: 229, havuz 253)")
PY
```

### K11 — B-133 · sonuç satırı koşuyu tanımlamıyor

```bash
python - <<'PY'
import json, collections
for ad, an in (("pencere_kapsami", lambda r: (r["kol_adi"], r["senaryo_etiket"],
                                              r["trafik_etiket"], r["konfig"]["tohum"])),
               ("gecerlilik", lambda r: (r["kol_adi"], r["senaryo_etiket"],
                                         r["uzunluk"], r["konfig"]["tohum"])),
               ("kontrol_payi", lambda r: (r["kol"], r["konfig"]["senaryo"],
                                           r["konfig"]["tohum"]))):
    c = collections.Counter(); h = collections.Counter()
    for l in open("ciktilar/sonuclar/%s.jsonl" % ad, encoding="utf-8"):
        r = json.loads(l); c[(r["kaynak_hash"], an(r))] += 1; h[r["kaynak_hash"][:8]] += 1
    print("%-18s satir=%3d hash=%s AYNI hash icinde TEKRARLI is=%d"
          % (ad, sum(h.values()), dict(h), len({k: v for k, v in c.items() if v > 1})))
PY
```

### K12 — B-134 · dejenere pay gecikmeyi de öldürüyor

```bash
python - <<'PY'
import sys, json, copy; sys.path.insert(0, ".")
from sim.karsilastirma import ortak_alt_kume, KarsilastirmaHatasi
V = {}
for l in open("ciktilar/sonuclar/gecerlilik.jsonl", encoding="utf-8"):
    r = json.loads(l)
    if r["kaynak_hash"] != "0a1a94e5fb24f01605fcf3168519520c" or r["uzunluk"] != "tam":
        continue
    V[(r["kol_adi"], r["senaryo_etiket"], r["konfig"]["tohum"])] = r["metrikler"]
a, b = V[("en_kisa_yol", "S0", 1)], V[("en_kisa_yol", "S2", 1)]
o = ortak_alt_kume(a, b)
print("SAGLAM : ortak=%d paket, gecikme farki=%+.3f ms, p95 farki=%+.3f ms"
      % (o.ortak_paket, 1e3 * o.gecikme_farki_s, 1e3 * o.p95_farki_s))
b2 = copy.deepcopy(b); b2["veri_bayt_pencere"] = 0
try:
    ortak_alt_kume(a, b2); print("KABUL (!!)")
except KarsilastirmaHatasi as e:
    print("B'de dejenere kontrol payi -> TUM karsilastirma REDDEDILDI:")
    print("   ", str(e).splitlines()[0][:90])
PY
```

### K13 — D1 · D3 · şema tamlığı ve iki taraflı ret

```bash
python - <<'PY'
import sys, json, copy, collections; sys.path.insert(0, ".")
from sim.karsilastirma import ortak_alt_kume, KarsilastirmaHatasi, _PAY_ALANLARI
TAM = ("teslim_kimlikleri", "teslim_gecikmeleri_s", "pencere_kimlik_araligi",
       "pencerede_uretilen", "pencere_evren_hash", "kurulum_hash",
       "kaynak_hash", *_PAY_ALANLARI)
top = 0; eksik = collections.Counter(); say = {}
for ad in ("gecerlilik", "kontrol_payi", "pencere_kapsami",
           "literatur_eksenleri", "deneme_araliklari"):
    n = 0
    for l in open("ciktilar/sonuclar/%s.jsonl" % ad, encoding="utf-8"):
        m = json.loads(l)["metrikler"]; n += 1; top += 1
        for alan in TAM:
            if alan not in m: eksik[(ad, alan)] += 1
    say[ad] = n
print("D1: dosya satirlari:", say, "TOPLAM:", top)
print("D1: TAM semada eksik alan tasiyan satir:", dict(eksik) if eksik else "YOK (0)")
V = {}
for l in open("ciktilar/sonuclar/gecerlilik.jsonl", encoding="utf-8"):
    r = json.loads(l)
    if r["kaynak_hash"] != "0a1a94e5fb24f01605fcf3168519520c" or r["uzunluk"] != "tam":
        continue
    V[(r["kol_adi"], r["senaryo_etiket"], r["konfig"]["tohum"])] = r["metrikler"]
a, b = V[("en_kisa_yol", "S0", 1)], V[("en_kisa_yol", "S2", 1)]
for taraf in ("a", "b"):
    for alan in _PAY_ALANLARI:
        aa, bb = copy.deepcopy(a), copy.deepcopy(b)
        (aa if taraf == "a" else bb).pop(alan)
        try:
            ortak_alt_kume(aa, bb); print("D3: %s/%s KABUL (!!)" % (taraf, alan))
        except KarsilastirmaHatasi:
            print("D3: %s/%-28s REDDEDILDI" % (taraf, alan))
PY
```

### K14 — B-123 · B-129 · B-132 · B-138 · beyan ≠ etki

```bash
grep -n "^TOHUM = " dogrulama/pencere_kapsami.py
python -c "import sys;sys.path.insert(0,'.');import json;from sim.results import kaynak_hash;e=json.loads(open('ciktilar/sonuclar/deneme_araliklari.jsonl',encoding='utf-8').readline());print(e['kaynak_hash'], kaynak_hash(), e['kaynak_hash']==kaynak_hash())"
grep -c "kayit(" dogrulama/li_calisma_noktasi.py
grep -c "olc(" dogrulama/li_zincir.py
ls ciktilar/sonuclar/
for d in sim tests dogrulama; do echo "$d: $(ls $d/*.py | wc -l) dosya, $(cat $d/*.py | wc -l) satir"; done
```

### K15 — B-127 · B-135 · koşul 1 hangi kolları bağlıyor

```bash
python -c "import sys;sys.path.insert(0,'.');from dogrulama.aktaricilar import AKTARICILAR;import dogrulama.gecerlilik as G;print('AKTARICILAR:',list(AKTARICILAR));print('gecerlilik.KOLLAR:',G.KOLLAR);print('DV (mesafe_vektoru) AKTARICILAR icinde mi:', 'mesafe_vektoru' in AKTARICILAR)"
```

### K16 — E1 · 540 koşunun bellek/pickle maliyeti *(~60 sn, 18 tam koşu)*

```bash
python - <<'PY'
import sys, pickle; sys.path.insert(0, ".")
from sim.config import Konfig, SENARYOLAR, TRAFIK_SEVIYELERI
from sim.kosucu import Kosu
from dogrulama.aktaricilar import AKTARICILAR
b = lambda o: len(pickle.dumps(o, protocol=pickle.HIGHEST_PROTOCOL))
sat = []
print("%-4s %-8s %12s %12s %12s %8s" % ("sen","trafik","TAM pickle","liste payi","ozet","teslim"))
for sen in SENARYOLAR:
    for tr in TRAFIK_SEVIYELERI:
        s = Kosu(Konfig(kol="kapi_en_kisa_yol", senaryo=sen, trafik=tr, tohum=1),
                 AKTARICILAR["en_kisa_yol"]).kostur()
        tam = b(s)
        lis = b(s["teslim_kimlikleri"]) + b(s["teslim_gecikmeleri_s"])
        ozet = b({"korunum_tamam": s["korunum"]["korunum_tamam"],
                  "fark": s["korunum"]["fark"], "dusen": s["korunum"]["dusen"],
                  "uretilen": s["korunum"]["uretilen"],
                  "boruda_kalan": s["boruda_kalan"],
                  "teslim_orani": s["teslim_orani"],
                  "yakinsadi": s["yakinsama"]["yakinsadi"],
                  "en_buyuk_fark": s["yakinsama"]["en_buyuk_fark"]})
        print("%-4s %-8s %12d %12d %12d %8d" % (sen, tr, tam, lis, ozet,
                                                len(s["teslim_kimlikleri"])))
        sat.append((tam, ozet))
tmax = max(x[0] for x in sat); tort = sum(x[0] for x in sat) / len(sat)
omax = max(x[1] for x in sat)
print()
print("satir basina: ortalama %.1f KB, EN BUYUK %.1f KB" % (tort/1024, tmax/1024))
print("540 kosu EN KOTU (hepsi bellekte): %.1f MB | ortalama %.1f MB"
      % (540*tmax/1048576, 540*tort/1048576))
print("eski hal (yalniz ozet) 540 kosu  : %.1f KB   -> ARTIS %.0f kat"
      % (540*omax/1024, tmax/omax))
PY
```

### 14.1 Kopya üzerinde koşan işler *(depo değiştirilmedi)*

Aşağıdakiler `tempfile` sınıfı bir **geçici kopyada** koştu; depo kökü
**okundu, yazılmadı**.

| # | ne | süre / sonuç |
|---|---|---|
| **T1** | `python -m pytest tests -q -p no:cacheprovider` — **eksik kopyada** *(v2/ yok)* | 1 172,09 sn · **6 failed, 456 passed** *(altısı da eksik `v2/` dosyalarından)* |
| **T2** | Aynı komut, **tam kopyada** | **1 030,81 sn · 462 passed** *(17 dk 10 sn)* |
| **T3** | Ulaşılabilirlik sondası: her araca `raise ImportError` konup `pytest tests --collect-only -q` | `isaret_testi` → 449+1E · `gecikme` → 455+1E · **diğer üçü → 462, hata YOK** |
| **T4** | 20 mutasyon × *(tetikleme harness'ı + 3 test dosyası)* | 6 dk 56 sn · **8/19 yakalandı** *(I1 eşdeğer)* |
| **T5** | `python dogrulama/li_calisma_noktasi.py` | **11,1 sn** · dört sayı birebir |
| **T6** | `pencere_kapsami.py` **TOHUM = 4** ile | **35,8 sn** · `AssertionError` — bkz. B-120 |
| **T7** | F7: 5 kol × 2 senaryo × 3 trafik × **5 tohum** = 150 tam koşu | **147 sn** · band %16,62–23,03 |
| **T8** | E3: `Pool(10)` ↔ `Pool(5)`, **iç içe**, 6 tekrar × 5 iş | 40,3 sn · fark **−0,08 sn/havuz** |

**Mutasyon protokolü** *(T4)* — üretilebilir olması için sırası:

```bash
# 1) depoyu gecici bir dizine kopyala (sim tests dogrulama v2 ciktilar README)
# 2) TEMIZ TABANI DOGRULA — Y7:
python -m pytest tests/test_isaret_testi.py tests/test_gecikme.py \
                 tests/test_kapi_secimleri.py -q -p no:cacheprovider
#    -> 85 passed   (bu adim atlanirsa her mutasyon "yakalandi" gorunur)
# 3) her mutasyon: dosyayi IKILI oku, tek dizgiyi degistir, IKILI geri yaz
#    (metin modu CRLF'i LF'e cevirir ve butun agaci sessizce degistirir)
# 4) her mutasyonda: (a) tetikleme harness'inin parmak izi degisti mi,
#                    (b) yukaridaki uc test dosyasi DUSEN TEST KUMESI
#    -x KULLANMA: ilk dusen test digerlerini gizler
# 5) geri yukleme dogrulamasi: dogrulama/*.py blake2b = 4405b20bee9a2f73
```

### 14.2 🔴 Bu denetimin KENDİ hatası — kayda geçer

İlk mutasyon koşusunda kopya `v2/` taşımıyordu. `test_kapi_secimleri.py`nin
**5 testi temiz ağaçta da düşüyordu** ve koşu `-x` ile yapıldığı için
**20 mutasyonun 20'si "yakalandı" göründü** — yani skor **%100** çıktı.

⚖️ **Ders — ve bu deponun kendi kuralı:** Y7, *"bir doğrulama aracı ne
koştuğunu kendisi doğrulamak zorunda"*. Ölçütü **temiz durumda önce
doğrulamadan** koşturdum; sonuç *"beklenenden iyi"* çıktı ve **Y6 tam
olarak bunu söylüyor**: beklenenden iyi sonuç, kötü sonuç kadar şüphelidir.
Düzeltildikten sonra gerçek skor **8/19** çıktı.

---

## 15. 🔴 OKUMA KAPSAMIM — hangi dosyanın hangi satır aralığını OKUMADIM

### 🟢 TAMAMEN okuduklarım

| dosya | satır |
|---|---|
| `README.md` | 1–221 *(tamamı)* |
| `v2/03-YONTEM-KURALLARI.md` | tamamı |
| `v2/06-ON-KAYIT.md` | 1–661 *(tamamı)* |
| `dogrulama/isaret_testi.py` | tamamı |
| `dogrulama/gecikme.py` | tamamı |
| `dogrulama/gecerlilik.py` | tamamı |
| `dogrulama/pencere_kapsami.py` | 1–217 *(tamamı)* |
| `dogrulama/li_calisma_noktasi.py` | 1–128 *(tamamı)* |
| `dogrulama/olcum.py` | tamamı |
| `sim/karsilastirma.py` | 1–432 *(tamamı)* |
| `sim/results.py` | 1–117 *(tamamı)* |
| `tests/test_isaret_testi.py` | 1–145 *(tamamı)* |
| `tests/test_gecikme.py` | 1–119 *(tamamı)* |

### 🟡 KISMEN okuduklarım — OKUMADIĞIM ARALIKLAR

| dosya | okuduğum | 🔴 **OKUMADIĞIM** |
|---|---|---|
| `v2/04-NEDEN-BOYLE.md` *(8 547 satır)* | **8 102–8 547** *(K-086 + Y1–Y14 + bilanço)* + grep isabetleri *(213, 1399, 2422, 4207, 4556, 4895–4974, 5606, 5724, 5790, 5839, 5915, 6375, 7288, 7385, 7478–7513, 7708, 7932, 8020, 8152, 8391)* | 🔴 **1–8 101 aralığının tamamına yakını — yaklaşık 7 950 satır (%93)**. K-001…K-085'in gövdeleri okunmadı |
| `v2/08-AILE0-KAPSAM.md` *(510 satır)* | md **25**, md **28**, md **31**, md **30** *(satır 463)*, Ç4 bloğu *(120–175)*, başlık *(14)* | 🔴 **Kalan ~30 kapsam maddesi ve Ç1–Ç3, Ç5, Ç6 bölümleri** |
| `v2/12-YOL-HARITASI.md` *(402 satır)* | 1–40 · §2.1–§2.4 *(≈114–200)* | 🔴 **41–113 ve 201–402 — yaklaşık 275 satır (%68)** |
| `v2/13-AILE0-KAPANIS-KANITI.md` *(349 satır)* | **1–120** | 🔴 **121–349 — 229 satır (%66)**, dört kanıt tablosunun üçü |
| `dogrulama/kontrol_payi.py` *(276 satır)* | 1–276 *(tamamı)* | — |
| `dogrulama/kapi_korunum.py` *(221 satır)* | 1–221 *(tamamı)* | — |
| `dogrulama/aile0_kapi_raporu.py` *(616 satır)* | 440–480 · 595–616 + grep isabetleri | 🔴 **1–439 ve 481–594 — 553 satır (%90)** |
| `dogrulama/li_duyarlilik.py` *(139)* · `li_zincir.py` *(227)* | imza/akış düzeyinde *(grep + `li_zincir` 55–95)* | 🔴 **her ikisinin de gövdesinin çoğu — yaklaşık 300 satır** |
| `tests/test_kapi_secimleri.py` *(1 858 satır)* | **1 290–1 440** *(B-106 blokları)* + grep isabetleri | 🔴 **kalan 1 708 satır (%92)** |
| `tests/test_karsilastirma.py` *(599 satır)* | grep isabetleri | 🔴 **tamamı okunmadı** |
| `dogrulama/mutasyon_paketi.py` *(910 satır)* | AST ile sayıldı, gövde okunmadı | 🔴 **tamamı** |
| `v2/00,01,02,05,07,09,10,11` | grep isabetleri | 🔴 **tamamına yakını** |
| `v2/yeni_detaylı_arastırma/` *(20 dosya, 5 271 satır)* | ❌ hiç açılmadı | 🔴 **tamamı** |
| `aile0_audit.md` *(8 602 satır)* | baş *(1–20)* ve son *(30 satır)* | 🔴 **~8 550 satır** — altı denetimin gövdeleri |
| `denetim/` *(7 önceki prompt)* | ❌ hiç açılmadı | 🔴 **tamamı** |

### ⚠️ Bunun anlamı

🔴 **`v2/04`ün %93'ünü okumadım.** K-080'in dersi tam buydu: bir ajan
5 271 satırlık bir taramanın %62'sini okuyup tamamını okuduğunu yazdı ve
**beş bulgu o eksikte saklıydı.** Bu denetimin kapsamı **B0'ın çıktısıyla
sınırlıydı** *(K-086, `06` §8.1b/§9.1, `08` md 25/31/Ç4, beş yeni araç)*
ve daha eski karar kayıtlarında B0'ın ölçütleriyle çelişen bir şey varsa
**onu görmedim.**

🔴 **`aile0_audit.md`nin altı denetim gövdesini okumadım** — yani bu
raporun bir bulgusunun önceki bir denetimde **zaten açılmış** olma
ihtimalini eleyemedim. Numaralandırma B-120'den başladığı için çakışma
yok, ama **tekrar** olabilir.

🔴 **`v2/yeni_detaylı_arastırma/` hiç açılmadı.** Literatürün gecikme
yüzdelikleri, ısınma süresi ve pencere seçimi hakkında söyledikleri bu
denetimin ölçümlerine **girmedi**.

---

🔒 **BU OTURUMDA HİÇBİR DEPO DOSYASI DEĞİŞTİRİLMEDİ.** `sim/`, `tests/`,
`dogrulama/`, `v2/`, `denetim/`, `ciktilar/` ve `README.md` **okundu,
yazılmadı**. Bütünlük koşu sonunda ölçüldü:

```
sim kaynak_hash      : 0a1a94e5fb24f01605fcf3168519520c
dogrulama/ icerik    : 4405b20bee9a2f73      (mutasyonlardan ONCEKI ile AYNI)
tests/     icerik    : 0fd8e2462e85b6b1
v2/        icerik    : c1889d810af9df50
ciktilar/  icerik    : f94fef0d7f859c0c
```

**Ve bu bir beyan değil, bir ölçümdür** *(`03` kural 15 · bu deponun en
sık tekrarlanan hatası: korumanın BEYANI değil ETKİSİ ölçülür)*:

```bash
find . -newermt "2026-09-02 01:00" -type f
```

**Çıktı — bu rapor eklenmeden ÖNCE: BOŞ.** Oturum boyunca depoda
`__pycache__` dâhil **hiçbir dosyanın değiştirilme zamanı ilerlemedi**;
`PYTHONDONTWRITEBYTECODE=1` yüzünden tek bir `.pyc` bile tazelenmedi.
*(Rapor eklendikten sonra aynı komut yalnızca `./aile0_audit.md` döner —
bu oturumun yazdığı tek dosya odur.)*

Tüm mutasyonlar, kırma denemeleri, ek matrisler ve `pytest` koşuları
oturuma özel bir **scratchpad** dizinindeki **iki geçici kopyada**
koşturuldu. Depo kökünden koşan komutların hepsi `PYTHONDONTWRITEBYTECODE=1`
ile çalıştırıldı; hiçbiri `ciktilar/sonuclar/` altına satır yazmadı
*(hiçbiri `kayit(...)` bağlamı açmadı)*. Bu oturumda yazılan **tek depo
dosyası bu rapordur** *(`aile0_audit.md`)*; önceki **altı denetimin
metnine dokunulmamıştır** — yalnızca dosyanın **sonuna** yedinci denetim
bölümü eklenmiştir.

🔒 **BU OTURUMDA HİÇBİR GİT KOMUTU ÇALIŞTIRILMADI — `status` dâhil.**

🔒 **Ana deney tohumları (2000–2029) hiçbir amaçla koşulmadı.** Kullanılan
tohumlar **1–30** aralığındadır *(ayarlama/kapı kümesi)*: tekil ölçümlerde
**1 · 4**, F7 taramasında **1–5**, E1'de **1**, depodaki satırların
çözümlenmesinde **1–30**.

> **Bir şeyi büyütmek istiyorsan önce ölç.** Bu denetimde büyütülmek
> istenen şey bir **ölçütün kendisiydi**; ölçülen şey ise o ölçütün
> **hangi nesneye uygulandığıydı.**


---
---

# B0.7/B0.8 DENETİMİ — 2 Eylül 2026

> **Bu denetimin sorusu bir öncekilerden dar:** *"B0.7/B0.8'in düzeltmeleri
> düzeltti mi — yoksa sorunu komşuya mı taşıdı?"*
>
> 🔴 **Bağımsızlık beyanı:** bu oturum B0.7/B0.8'i yazan taraf değildir.
> Hiçbir depo dosyası değiştirilmemiş, hiçbir git komutu çalıştırılmamıştır.
> Bütün denemeler `tempfile.mkdtemp` kopyalarında yapılmıştır ve kopyalar
> **`v2/` dâhil** `dogrulama/kopya.py::depoyu_kopyala` ile kurulmuştur.

**Ortam:** Windows 11 · Python 3.11 · 12 çekirdek *(bütçe 10)* ·
`PYTHONIOENCODING=utf-8` · `kaynak_hash = fc73905bbb00ad719b31eb5dbb9f8f19`

---

## 0. YÖNETİCİ ÖZETİ

> # 🔴 DÜZELTMELER DÜZELTTİ Mİ: **KISMEN — VE ÖRÜNTÜ KAPANMADI**

### 🔴 EN CİDDİ TEK BULGU

**B0.7/B0.8'in en pahalı iki düzeltmesi — B-124 ve B-125 — ÖLÜ KODA
yazıldı.** İkisi de `dogrulama/isaret_testi.py::satir()` fonksiyonuna
uygulandı. Ölçüldü: **o fonksiyonun deposunda TEK bir çağıranı yoktur** —
ne üretim kodunda, ne testlerde, ne `tests/test_isaret_testi.py`nin içe
aktarma listesinde. `06` §9.1 ve §8.1b'nin tablolarını fiilen basan
üretici `dogrulama/gecerlilik.py::_yaz_kosul1/_yaz_kosul2`'dir ve o
**dokunulmamıştır**:

| B0.8'in yazdığı kural | `satir()` *(ölü)* | `_yaz_kosul1/2` *(canlı üretici)* |
|---|---|---|
| B-125: *"`gecti` yalnızca AYAK 1'dir; **etiket bunu söylemek zorunda**"* | `YON-OK`/`YON-RED` ✅ | 🔴 **`GECTI`/`GECMEDI`** — ve sütun başlığı **`yargi`** |
| B-124: *"ikisi ayrıştığında **İKİSİ DE basılır**, yoksa okuyucu GA'yı yanlış medyanla eşleştirir"* | `med_net=` basıyor ✅ | 🔴 **yalnızca HAM medyan** basıyor, GA'nın yanında |

**Ölçülen etki:** bugünkü veride koşul 1'in **18 satırının 15'i "GECTI"**
basıyor — K-088'in *"koşul 1 bugün hiçbir kol için sağlandı sayılamaz"*
cümlesinin tam tersi. Ve **18 satırın 7'sinde** basılan medyan, yanındaki
GA'nın estimandı **değil**; ikisinde işaret bile ters
*(`DV/S2/teslim_orani`: basılan `+0.00000`, GA'nın estimandı `−0.00005`)*.
`06` §8.1b'ye mühürlenmek üzere giren **DV kolunun dört satırının dördü de**
yanlış estimandı taşıyor — K-088'in manşet cümlesindeki *"+1,32 ms · +8,34 ms"*
dâhil *(doğrusu +1,61 · +9,01)*.

⚖️ Bu, deponun kendi en pahalı hata sınıfının *(beyan ≠ etki)* en saf
hâlidir ve **düzeltmenin kendi içindedir**: B-124/B-125 bir kusuru doğru
teşhis etti, doğru ilacı yazdı, ve **ilacı hastanın olmadığı odaya
bıraktı.**

### 🔴 ÖRÜNTÜNÜN DÖRDÜNCÜSÜ — ve beşincisi, altıncısı

Yedinci denetimin teşhisi *("bir kuralı bir nesneye uygulayıp yanındakine
uygulamamak")* **kapanmadı**; bu denetim **altı yeni örneğini ölçtü**
*(§6)*. En keskini:

> **B-135 DV kolunu araca ekledi. B-136 DV'nin satırlarını `06` §8.1b'ye
> *(koşul 2)* yazdı. `06` §9.1 *(koşul 1)* — aynı belgede, aynı araç
> koşusundan, 60 satır aşağıda — hâlâ *"12 çiftin 2'si geçmiyor"* diyor.
> Ölçülen: **18 çiftin 3'ü**. Ve bu bayat cümle `04` · `06` *(iki yerde)* ·
> `09` · `12` · `13` — **beş belgede, altı yerde** duruyor. `13`,
> jürinin okuyacağı KAPANIŞ KANITI belgesidir.**

### 🔴 ÇAPA TESTİ UYUYOR — düzeltmeyi yazan ajanın şüphesi doğrulandı

`sim/packet.py`ye **tek zararsız yorum satırı** eklendi *(kopyada)*:
`tests/test_gecerlilik_araclari.py`nin **9 testinin 5'i sessizce atlandı**.
Kendi yazdığım 26 mutasyonla ölçüldü *(iç içe, aynı mutasyon kümesi)*:

| durum | yakalanan | %95 GA | `gecerlilik.py` tek başına |
|---|---|---|---|
| **A · `sim/` temiz** | **13/26 · %50,0** | [%32,1 · %67,9] | 8/15 · %53,3 |
| **B · `sim/` değişmiş** | **7/26 · %26,9** | [%13,7 · %46,1] | **2/15 · %13,3** |

Eşleştirilmiş fark **6–0** *(McNemar kesin p = 0,031)*. Kaybolan altısının
içinde dosyanın **kendi docstring'inde varlık gerekçesi olarak yazdığı V3
mutasyonu** var. Ve dosya **hiçbir kapı kriterinde yoktur**.

### 🔴 BEŞ KAPANIŞIN REGRESYON TESTİ YOK

`03` Bölüm E: *"Bir modül 'bitmiş' sayılır — **dördü birden** gerekir:
1. Hata geri gelirse yakalayacak **regresyon testi**…"* Ölçüldü — şu beş
düzeltme geri alındığında **473 testin hiçbiri konuşmuyor**:

| düzeltme | geri alan mutasyonum | sonuç |
|---|---|---|
| **B-123** *(pencere_kapsami 1 → 30 tohum)* | `X18` | 🔴 sağ kaldı |
| **B-124** *(`medyan_fark_net`)* | `X24` | 🔴 sağ kaldı |
| **B-125** *(büyüklük ayağı)* | `X23` | 🔴 sağ kaldı |
| **F-9/F-11** *(kalibrasyon çok işten)* | `X10` · `X19` | 🔴 ikisi de sağ kaldı |
| **F-12** *(ortanca = `statistics.median`)* | `X25` | 🔴 sağ kaldı |

### 🟢 NE GERÇEKTEN DÜZELDİ — ve bir sabit ilk kez ölçüldü

🟢 **`Pool(8)` çekişme çarpanı bu depoda ilk kez ölçüldü: 1,795.** Depo
*"BUGÜNE KADAR HİÇ ÖLÇÜLMEDİ … 1,80 hâlâ bir alt sınır olabilir"* diye
yazıyordu; **değilmiş** — yazılı sabit **doğrulandı**. Bir dalga *(8 mutant,
`Pool(8)`)* **1 767,3 sn**; 35 → 41 artışı **29,5 dk** ve K-088'in *"~25 dk"*
tahmini **ölçülen 22–29,5 dk bandının içinde** — deponun altı kez tutmayan
süre tahmini **bu kez tuttu**. ⚠️ Ama ilan edilen **165–330 dk** bandının
üst ucu tutmuyor: en kötü gözlenen test maliyetiyle kapı **~418 dk**
*(B-167)*.


Hepsi kötü değil — **bağımsız olarak doğrulanan kapanışlar:** B-128
*(`yuzdelik` bugün **tek** gövde — AST ile sayıldı)* · B-129 *(kapının
bayatlığı 8 belgede yazılı; üretici komut bugün `False` basıyor —
koşturuldu)* · B-138 *(satır sayıları **birebir** tuttu: 4 538 / 10 288 /
7 564, 15/20/31 dosya, 473 test)* · B-136 *(§8.1b'nin 12 satırının 12'si
üreticiden **birebir** çıkıyor)* · B-121 *(HAM p95 artık üretiliyor)* ·
B-141 · B-137 · F-10 *(metin tabanlı korumalar gerçekten AST'ye çevrilmiş;
kalan `in` denetimleri **üretilen mesajlara** bakıyor, koda değil)* ·
**B-131'in altı mutasyonunun altısı da beklenen testini kırıyor** *(koştu)*.

### 🔴 B1'E (KAT 4) GEÇİLEBİLİR Mİ

> **HAYIR — ama iki günlük bir işle evet.**

Gerekçe tek cümlede: **şema SON KEZ donacak** ve bugün donacak şemanın
üstünde duran üç sayı yanlış estimanddan geliyor *(B-146)*, koşul 1'in
durumu altı belgede yanlış yazılı *(B-147)*, ve bunları koruyacak tek test
dosyası **`sim/` değişir değişmez susuyor** *(B-143)* — B1'in ilk işi
`sim/`e Kat 4 eklemektir, yani **çapa B1'in ilk saatinde uyur.**

🔒 **B1 öncesi zorunlu asgari** *(hiçbiri yeni ölçüm gerektirmiyor)*:
`_yaz_kosul1/2`nin etiket ve medyan basımını `satir()` ile aynı sözleşmeye
bağlamak *(B-145 · B-146)* · `06` §9.1 + 5 belgedeki *"12 çiftin 2'si"*
cümlesini üreticiden yeniden yazmak *(B-147)* · çapa testinin `skip`ini
`xfail`/`fail`e çevirmek ya da dosyayı bir kapı kriterine bağlamak
*(B-143 · B-144)* · `mutasyon_paketi.py`nin altı mutasyonunu `__main__`
bloğunun **üstüne** taşımak *(B-149)*.

---

## 1. 🔴 ÇAPA TESTİ UYUYOR MU — Bölüm A

`tests/test_gecerlilik_araclari.py`, üç üreticinin *(`gecerlilik.py` ·
`pencere_kapsami.py` · `li_calisma_noktasi.py`)* **tek** korumasıdır.

### A1 · `sim/` değişince kaç test atlanıyor — **ÖLÇÜLDÜ: 9'un 5'i**

Kopyada `sim/packet.py`ye tek satır yorum eklendi *(davranış değişmedi,
`kaynak_hash` `fc73905b…` → `16864c7b…` oldu)*:

```bash
cd <kopya> && echo "# zararsiz yorum" >> sim/packet.py
PYTHONIOENCODING=utf-8 python -m pytest tests/test_gecerlilik_araclari.py -q -rs
```

| | önce | sonra |
|---|---|---|
| çıktı | `9 passed in 3.20s` | 🔴 **`4 passed, 5 skipped in 1.97s`** |

**Atlanan beş test — ve neyi koruyorlardı:**

| test | koruduğu mutasyon sınıfı |
|---|---|
| `test_b130_kosul2_DORT_okumayi_da_uretiyor` | 🔴 **V3** — dosyanın docstring'inde *varlık gerekçesi* olarak yazılı olan |
| `test_b130_kosul1_KISA_ile_TAM_i_karsilastiriyor` | V2 |
| `test_b130_kosul1_farkin_ISARETI_kisa_eksi_tam` | V1 |
| `test_b130_kosul3_tohum_std_HESAPLANIYOR` | V5 |
| `test_b130_olu_kolunun_ANALITIK_capasi_hala_gecerli` | B-120'nin **kalan tek analitik çapası** |

**Mekanizma** *(`tests/test_gecerlilik_araclari.py:66-77` ve `:208-214`)*:
fixture `sim.results.kaynak_hash()` çağırıp `.jsonl` satırlarını ona göre
süzüyor; eşleşme yoksa `pytest.skip`. Ve `sim/results.py:44` —
`kaynak_hash` **`sim/` altındaki HER `.py` dosyasının içeriğini** hash'ler,
yorum dâhil.

🔴 **Sonuç:** üç aracın tek koruması, `sim/` her değiştiğinde — yani
**korumaya en çok ihtiyaç duyulan anda** — susuyor. Ve **B1'in ilk işi
`sim/`e Kat 4 eklemektir.**

### A2 · Kapı bunu görür mü — **HAYIR, dosya hiçbir kriterde yok**

```bash
grep -rn "gecerlilik_araclari" dogrulama/ tests/ v2/ --include=*.py --include=*.md
```
Tek eşleşme: `v2/04-NEDEN-BOYLE.md:8756` *(B-131 satırı)*. `dogrulama/`
altında **sıfır**.

`aile0_kapi_raporu.py::KAPI_SECIMLERI` beş seçim taşıyor — Ç2, Ç3, Ç5,
Ç4.1, Ç6.2 — ve dosyaları: `test_kapi_aile0.py` · `test_radio.py` ·
`test_gozlem.py` · `test_li_regresyon.py` · `test_rng.py`. **Çapa dosyası
hiçbirinde yok.** Ç1.1/Ç1.2/Ç1.4 korunum matrisidir, Ç6.1/6.3/6.4 AST
denetimidir. Dosyayı çalıştıran **tek** kapı yolu **Ç1.3**'tür — ve
Ç1.3'ün 41 mutasyonunun **41'i de `sim/` altındadır**, yani her mutantta
bu beş test **zaten atlanır**.

🔴 **Bir `skip` kırıklık sayılmıyor.** `_pytest()` *(`aile0_kapi_raporu.py:407-409`)*
yalnızca `" passed"` ve `" failed"` ayrıştırıyor:
`"468 passed, 5 skipped"` satırından `gecen=468, kirilan=0` çıkar. Ölçüt
`k == 0 and g > 0 and not notu` → **geçer**. Depoda toplam test sayısını
ya da `skipped` sayısını sabitleyen **hiçbir koruma yok** *(tarandı:
`grep -rn "473\|468\|skipped" tests/ dogrulama/` → boş)*.

### A3 · Bir *"skip"* koruma mıdır — **HAYIR, ve kapsam tablosu bunu anmıyor**

Dosyanın kendi kapsam tablosu **dört satır** taşıyor ve skip davranışı
**hiçbirinde yok**:

| dosyanın yazdığı vaka | yazdığı yargı | ölçülen |
|---|---|---|
| karar yükleminin **hesabı** bozulursa | ✅ | ⚠️ **yalnızca `sim/` değişmemişken** |
| okuma **etiketi** yanlış büyüklüğe bağlanırsa *(V3)* | ✅ | ⚠️ **yalnızca `sim/` değişmemişken** |
| `main()` içindeki akış bozulursa | ❌ HAYIR | 🟢 doğru *(§12'de ölçüldü)* |
| tam koşunun **fiziği** bozulursa | ❌ | 🟢 doğru |

Y7: *"boş küme de 0 kırık verir."* Bir `skip` tam olarak boş kümedir ve
`03` B5'in **bildirim ≠ kullanım** tuzağının bu dosyadaki hâlidir: iki
satır ✅ yazıyor, **koşulu yazmıyor**.

### A4 · Kendi mutasyonlarım — **beyan doğru, ama fazlasıyla dar**

26 mutasyon yazıldı *(15'i `gecerlilik.py`, 4'ü `pencere_kapsami.py`, 2'si
`li_calisma_noktasi.py`, 3'ü `isaret_testi.py`, 2'si `kontrol_payi.py`)* ve
**her biri iki durumda birden** koşuldu *(talimat 8 — iç içe)*.

**Üretici:** `scratchpad/olcum/a4.py` *(dosyadan koşuldu — Windows `spawn`)*

| durum | taban | yakalanan | %95 GA |
|---|---|---|---|
| **A · `sim/` temiz** | `89 passed in 22.20s` | **13/26 · %50,0** | [%32,1 · %67,9] |
| **B · `sim/` değişmiş** | `84 passed, 5 skipped` | **7/26 · %26,9** | [%13,7 · %46,1] |

**Eşleştirilmiş fark:** A'da yakalanıp B'de kaybolan **6**, tersi **0** →
McNemar kesin **p = 0,031**.

🔴 **`main()` beyanı DOĞRU ama sınırı daha geniş:** dosya *"`main()`
çağrılmıyor"* diyor ve `main()` mutasyonlarının **6/6'sı sağ kaldı** ✅
beyan doğru. **Ama `main()` DIŞINDA da yedi mutasyon sağ kaldı** *(durum
A'da)* — yani beyan, kapsamın dışını **olduğundan dar** gösteriyor:

| sağ kalan *(durum A)* | nerede | geri aldığı kapanış |
|---|---|---|
| `X7_kosul3_dejenere_sayilmiyor` | analiz | `03` B2 *(kaç gözlemle)* |
| `X8_kosul2_reddedilen_sayilmiyor` | analiz | `03` B2 |
| `X9_eslesmis_oran_YONLU_oldu` | analiz | 🔴 **F-12 sınıfı** |
| `X23_buyukluk_ayagi_BOSALDI` | analiz | 🔴 **B-125 / K3** |
| `X24_medyan_fark_net_HAMA_dondu` | analiz | 🔴 **B-124** |
| `X18_TOHUM_30_dan_1_e` | modül | 🔴 **B-123** |
| `X25_ortanca_UST_ORTAYA_dondu` | main | 🔴 **F-12** |

**Ulaşılan güç** *(n = 26, kesin binom)*: gerçek kapsam **%70** olsaydı
≤13/26 görme olasılığı **0,0255**; **%80** olsaydı **0,0006**. Yani
α = 0,05'te **gerçek kapsamın ≥%70 olduğu dışlanıyor** *(durum A'da)*.
B-130'un *"9/19 → 9/9"* ölçümü kendi ilan ettiği dar kapsamda doğrudur;
**bu ölçüm o kapsamın dışını ölçmüştür (Y11).**

---

## 2. 🔴 B-134'ÜN AÇTIĞI YÜZEY — Bölüm B

### B1 · Kontrol payı bilinmeyen bir gecikme farkı üretilebilir mi — **EVET, ve tek tüketici tam olarak onu yapıyor**

`ortak_alt_kume`ın **üretimdeki tek çağıranı** `dogrulama/gecerlilik.py:196`
*(`kosul2`)*'dir; kalan 18 çağrı test dosyalarındadır:
```bash
grep -rn "ortak_alt_kume(" --include=*.py . | grep -v tests/
```
Ve `kosul2` `o.ham_fark_s` · `o.gecikme_farki_s` · `o.p95_farki_s` ·
`o.kesisim_orani_pencere` · `o.ortak_paket` okuyor — **`kontrol_payi_a/b`yi
hiç okumuyor ve `ozet()`i hiç çağırmıyor**:
```bash
grep -rn "\.ozet()" --include=*.py . | grep -v tests/
```
→ yalnızca `sim/kosucu.py` *(topoloji/trafik özeti — başka bir `ozet`)* ve
`dogrulama/kurulum_kalibrasyonu.py`.

🔴 **Sonuç:** `08` madde 35'in güvencesi — *"okuyan, `ozet()`in TANIMSIZ
etiketini görmek zorundadır"* — **üretim yolunda değildir.** `ozet()`i
zorlayan tek şey `tests/test_karsilastirma.py:450`tir, yani bir testtir;
`06` §8.1b'nin 12 satırını basan yol onu hiç geçmez.

**Bugünkü ölçek:** `kosul2`nin ürettiği **88 karşılaştırmanın 0'ında**
kontrol payı `None`. Yani delik bugün **ateşlemiyor** — ama yapısaldır ve
Faz 1'in AODV'si D-11'in birebir profilidir *(kontrol düzlemi ağır)*.

### B2 · `None` her tüketicide ele alınıyor mu — **HAYIR, komşu vaka çöküyor**

`kontrol_payi_yuzde` dört yerde çağrılıyor:

| çağıran | `None` işleniyor mu |
|---|---|
| `sim/karsilastirma.py:431-432` | ✅ alana yazılıyor |
| `dogrulama/gecerlilik.py:241` *(`kosul3`)* | ✅ `dejenere += 1` |
| `dogrulama/gecerlilik.py:277` *(`eslesmis_kol_orani`)* | ✅ `continue` |
| `dogrulama/kontrol_payi.py:207` | ✅ `None` yazılıyor |

🔴 **Ama komşu dejenere vaka kapsanmıyor.** `kontrol_payi_yuzde` `vb == 0`
ve `va == 0`'ı `None`'a çeviriyor; **`kb == 0`** *(kolun pencerede hiç
kontrol baytı üretmemesi)* geçerli bir dönüş olan `bayt = 0.0`'ı veriyor ve
`gecerlilik.py:280-281`

```python
oranlar.append(max(pa["bayt"], pb["bayt"]) / min(pa["bayt"], pb["bayt"]))
```

**ZeroDivisionError** fırlatıyor — ölçüldü *(besleme: `{"bayt": 0.0,
"airtime": 1.0}`)*. `kontrol_payi.py::eslestirilmis_oranlar:160` aynı vakayı
`b == 0` ile **açıkça** eliyor. Yani D-11/B-134'ün dersi *(dejenere payda
tipli reddedilir)* iki araçtan birine uygulanmış, **komşusuna
uygulanmamıştır** — örüntünün bir örneği daha.

### B3 · `08` madde 35 davranışın tamamını anlatıyor mu — **HAYIR**

Madde 35 iki şey söylüyor ve ikisi de eksik:

| maddenin cümlesi | ölçülen |
|---|---|
| *"okuyan, `ozet()`in TANIMSIZ etiketini görmek **zorundadır**"* | 🔴 Üretim yolunda `ozet()` **çağrılmıyor** *(B1)*. "Zorunda" bir dilek, mekanizma değil |
| *"Ölçek: 120 hücrenin **2'si** dejenere *(DV, tohum 25)*"* | ⚠️ O 120 hücre `kontrol_payi.py`nindir. `06` §8.1b'yi üreten **88 karşılaştırmanın ölçeği yazılmamış** *(bugün 0)* |

### B4 · *"Önceki sonuçlar geçerli"* doğru mu — **BUGÜN EVET, GEREKÇE YANLIŞ**

Tablonun gerekçesi: *"reddedilen bir karşılaştırma **sayı üretmemişti**,
yani geriye dönük değişen bir sayı yok."*

🔴 Bu, **tekil** karşılaştırma için doğru, **toplu** istatistik için
yanlış. `kosul2` bir `KarsilastirmaHatasi` yakaladığında hücreyi
**örneklemden düşürüyordu** *(`reddedilen += 1; continue`)*. Yeni davranışta
o hücre örnekleme **giriyor** — yani `n`, `pozitif`, `p`, `ga`,
`kesisim_ort/min/max` ve medyan **hepsi değişir**. Reddedilen bir hücre
"sayı üretmez" ama **başka satırların sayısını değiştirir.**

🟢 **Bugün zararsız olduğu ölçüldü:** 88 karşılaştırmanın 0'ı dejenere, yani
eski ve yeni davranış aynı örneklemi veriyor. ⚠️ Ama tablonun yazdığı
gerekçe bu ölçüme değil, yanlış bir genellemeye dayanıyor — ve Faz 1'de
*(AODV ↔ OLSR)* dejenere hücre beklenen bir olaydır.

🔴 **Ve K-088'in *"ölçülen kazanç"*ı bugün gerçekleşmiş değil:** *"801 ortak
paket · +10,140 ms"* sayısı `aile0_audit.md:9175`teki **sentetik olarak
bozulmuş** bir girdiden gelir *("B'de dejenere kontrol payi")*, depodaki bir
hücreden değil. Ölçüldü: bugünkü **88 karşılaştırmanın 0'ında** eski
davranış bir fark öldürüyor olurdu. Kazanç **gösterilmiştir, gerçekleşmemiştir**;
K-088 onu 🔴 *"Ölçülen kazanç"* diye yazıyor *(B-156)*.

---

## 3. 🔴 ALTI YENİ MUTASYON — Bölüm C

### C1 · Desenler bugünkü kaynakta tutuyor mu — **41/41 TAM BİR KEZ**

```bash
PYTHONIOENCODING=utf-8 python scratchpad/olcum/c1.py
```
```
toplam mutasyon: 41
desen sayisi != 1 olan: 0
modul basina: config 6 · karsilastirma 7 · kosucu 11 · mac 11 ·
              packet 1 · queues 1 · radio 3 · rng 1
beklenen_test'i tests/ icinde BULUNMAYAN mutasyonlar: 0
```
🟢 **41 desenin 41'i de tam bir kez geçiyor** — hiçbiri "geçersiz" sayılmaz,
kapıyı düşürmez. `sim/karsilastirma.py` gerçekten **1 → 7**.

🔴 **AMA `_kosu` yalnızca varlığı denetliyor** *(`if m.eski not in metin`)*,
tekliği değil; `.replace(m.eski, m.yeni, 1)` çok geçen bir deseni **sessizce
ilkinde** değiştirirdi. Bugün sorun yok — **yarın için bir koruma yok**
*(beyan edilmemiş sınır)*.

🔴 **VE PAKET İKİ FARKLI SAYIYLA KOŞUYOR** *(B-149)*. Altı yeni mutasyon
`if __name__ == "__main__": main()` bloğunun **ALTINA** eklenmiş
*(`mutasyon_paketi.py:909-910` ↔ `:928-966`)*. Ölçüldü — kopyada `main()`e
tek satırlık sayaç yamalanarak:

| yol | `len(MUTASYONLAR)` |
|---|---|
| içe aktarma *(kapının yolu — `from … import paketi_kostur`)* | **41** ✅ |
| **betik** *(`python dogrulama/mutasyon_paketi.py` — aracın kendi belgelenmiş komutu)* | 🔴 **35** |

Ve `main()` `BEKLENEN_MUTASYON`u **hiç kontrol etmiyor** *(o kontrol yalnızca
`aile0_kapi_raporu.py:520`de)*: betik yolu **`✅ Ç1.3 GEÇTİ — 35/35`** basıp
çıkış kodu **0** verir. Y12'nin *"elle tutulan sabit"* dersinin ikizi —
bu kez sabit doğru, **kod yolu** yanlış.

🔴 **Numara çakışması** *(B-150)*: `D26`, `D27`, `D28` artık **ikişer**
mutasyon adlandırıyor *(`D26_yorunge_yonu_ters`/`radio.py` ↔
`D26_gecikme_farki_ISARET`/`karsilastirma.py` vb.)*. Tam adlar benzersiz
olduğu için araç çalışıyor, ama kayıtlardaki *"D26"* göndermesi artık
**tekil değil**.

### C2 · Her biri beklenen testini kırıyor mu — **6/6, İÇ İÇE ÖLÇÜLDÜ**

**Üretici:** `scratchpad/olcum/c2.py` — her mutasyon için **önce taban**
*(mutasyonsuz kopya)*, **sonra mutant**; ikisi de aynı test düğümünde.

| mutasyon | `beklenen_test` | TABAN | MUTANT |
|---|---|---|---|
| `D26_gecikme_farki_ISARET` | `test_b05_gecikme_ve_p95_farkinin_YONU_dogru` | `1 passed` | ✅ `1 failed` |
| `D27_p95_farki_ISARET` | *(aynı test)* | `1 passed` | ✅ `1 failed` |
| `D28_kontrol_payi_PAYDA` | `test_b05_kontrol_payi_paydasi_TOPLAM_pay_degil` | `1 passed` | ✅ `1 failed` |
| `D29_evren_hash_KONTROLU_YOK` | `test_b05_EVREN_hash_kontrolu_BAGIMSIZ_calisiyor` | `1 passed` | ✅ `1 failed` |
| `D30_uzunluk_KONTROLU_YOK` | `test_b67_SATIR_ICI_bozuk_yapi_reddediliyor` | `5 passed` | ✅ `1 failed, 4 passed` |
| `D31_kardinalite_KONTROLU_YOK` | `test_b05_KARDINALITE_kontrolu_calisiyor` | `1 passed` | ✅ `1 failed` |

🟢 **Altısı da geçerli ve altısı da kendi testini kırıyor.** Y8 sağlandı:
bozulan yolun sağlam koşuda **geçtiği önce gösterildi**.

⚠️ Kapsam sınırı: bu ölçüm `tests/test_karsilastirma.py`de yapıldı, tam
pakette değil. Gerekçe: kapının ölçütü *(a)* en az bir test kırılsın
*(b)* `beklenen_test` kırılanlar arasında olsun — **(b) doğrudan ölçüldü** ve
(a)'yı kapsıyor.

### C3 · 🔴 KAPI SÜRESİ — `Pool(8)` ÇARPANI BU DEPODA İLK KEZ ÖLÇÜLDÜ

Depo kendi kaydında yazıyordu *(`mutasyon_paketi.py:208-212`)*:

> *"Bu ölçüm `Pool(6)` altında … kapı `Pool(8)` kullanıyor.
> 🔴 **`Pool(8)` çarpanı BUGÜNE KADAR HİÇ ÖLÇÜLMEDİ** … 1,80 hâlâ bir ALT
> SINIR olabilir."*

**Ölçüldü** — kapının **kendi** `_kosu` fonksiyonu, kapının **kendi**
`Pool(8)`u, paketin ilk sekiz mutasyonu *(öğrenci onayı alındıktan sonra
koşuldu)*:

```bash
PYTHONIOENCODING=utf-8 python scratchpad/olcum/c3_pool8.py
```
```
DALGA SURESI (8 mutant, Pool(8)) : 1767.3 sn  (29.5 dk)
TEK KOSU TABANI                  :  984.37 sn (16.4 dk)   <- aynı gün, boş makine
OLCULEN CEKISME CARPANI          : 1.795
```
*(sekiz mutantın sekizi de en az bir test kırdı: 3 · 1 · 3 · 2 · 16 · 5 · 10 · 1)*

> 🟢 **YAZILI SABİT DOĞRULANDI.** `CEKISME_CARPANI = 1.80` — ölçülen
> **1,795**. `Pool(6)`da gözlenen maksimum 1,7803'tü ve K-066 *"1,80 hâlâ
> bir alt sınır olabilir"* demişti; **değilmiş.** Bu, bu denetimin
> doğruladığı en temiz sabittir.

**Kapı aritmetiği** *(`havuz.map(_kosu, MUTASYONLAR)` · `Pool(8)`)*:

| | mutasyon | dalga | Ç1.3 ≈ taban + dalga × süre |
|---|---|---|---|
| B0.8 **öncesi** | 35 | ⌈35/8⌉ = **5** | 984 + 5 × 1 767 = **9 821 sn · 164 dk** |
| **bugün** | 41 | ⌈41/8⌉ = **6** | 984 + 6 × 1 767 = **11 588 sn · 193 dk** |

🔴 **ARTIŞ = 29,5 dk** *(bir tam dalga)*. K-088 *"~25 dk"* yazdı.
⚖️ **Bu bir hata değil, bandın alt ucu:** `map` varsayılan `chunksize`ı
41 iş / 8 işçi için **2** hesaplıyor, yani son dalga eksik dolar ve gerçek
artış **⌈0,75 – 1,0⌉ dalga = 22–29,5 dk** aralığındadır. *"~25 dk"* bu
aralığın **içindedir** — 🟢 **deponun altı kez tutmayan süre tahmini bu kez
tuttu.**

🔴 **AMA İLAN EDİLEN 165–330 dk BANDI ÜST UÇTA TUTMUYOR.** Tahmin
**ölçülen en büyük** süreden kurulmalıdır *(deponun kendi kuralı)*.
`TEST_BASINA_EN_KOTU_S = 4,3854` ile:

| taban | dalga *(× 1,795)* | Ç1.3 | + Ç1/Ç2…Ç6 *(~11 dk)* |
|---|---|---|---|
| **984 sn** *(bugün — en iyi okuma)* | 1 767 sn | 193 dk | **~204 dk** |
| **2 074 sn** *(473 × 4,3854 — en kötü gözlem)* | 3 723 sn | **407 dk** | 🔴 **~418 dk** |

Yani üst uç ilan edilen **330 dk**'yı **%27** aşıyor *(B-167)*.

### C4 · `MUTANT_ZAMAN_ASIMI_S = 7 200` yetiyor mu — 🟢 **EVET, VE ARTIK ÖLÇÜLMÜŞ**

| | ölçülen mutant süresi | zaman aşımı | marj |
|---|---|---|---|
| bugünkü taban | ≤ **1 767 sn** *(ölçüldü)* | 7 200 | **×4,07** |
| en kötü gözlem | 3 723 sn *(2 074 × 1,795)* | 7 200 | **×1,93** |
| taban koşusu *(tek başına)* | 984 → 2 074 sn | 4 200 *(`TABAN_…`)* | ×4,27 → **×2,03** |

🟢 Y12'nin ucuz koruması *(`test_b78_*`)* geçiyor **ve bu kez ölçümle de
destekleniyor** — çünkü `_gereken_zaman_asimi_s(473) = 4,3854 × 473 × 1,80 ×
1,50 = 5 601 sn < 7 200`. Ölçülen gerçek en kötü *(3 723 sn)* bunun
**altında**; yani koruma **muhafazakâr** ve doğru yönde.

⚠️ **Yeni bir okuma bandı genişletti:** bugünkü koşu **2,081 sn/test**
*(984,37 / 473)* — `OLCULEN_KOSULAR`ın en iyisi **2,0906**'nın da altında.
Band artık **2,081 – 4,385 = ×2,11**. `OLCULEN_KOSULAR`a
`(473, 984.37)` eklenmelidir *(Y12)*.

### C5 · 🔒 **NEDEN 16 DEĞİL 6** — *"zaten yakalanan 10 ek güvence getirmez"* doğru mu?

> **HAYIR — ve bu, `Y12`/`Y13`in kendi mantığıyla çelişiyor.**

Bir mutasyonun pakete girmesinin değeri *"yakalanıyor mu"* **değildir**;
paket zaten *"yakalandı"* demiyor, **`beklenen_test` kırıldı mı** diyor
*(`paketi_kostur`ün 3. koşulu, B-21)*. Yani her mutasyon **hangi testin**
koruduğunu **adlandırır** — ve o adlandırma, mutasyon havuzunun asıl
ürünüdür:

| iddia | ölçülen |
|---|---|
| *"Zaten yakalanan 10 mutasyon ek güvence getirmez"* | 🔴 Yakalanıyor **bugünkü test kümesiyle**. Bir test silinince/daraltılınca hangi mutasyonun korumasız kaldığını söyleyecek olan **yine o mutasyondur.** Y12'nin *"kapsam sessizce daralır"* vakası tam olarak budur *(Ç5'te **iki kez** yaşandı)* |
| — | 🔴 Ve *"yakalandı"* ölçümü **A-14'ün kendi koşusundan** geliyor; kapı yolunda *(tam paket · `Pool(8)` · taban kontrolü)* **tekrarlanmadı**. B-131 bunu `karsilastirma.py` için düzeltti — kalan 10 için düzeltmedi |

⚖️ **Ama maliyet gerekçesi geçerli ve şimdi ölçülmüş:** 10 mutasyon daha
= ⌈51/8⌉ = **7 dalga** = +1 dalga = **+29,5 dk** *(en kötü gözlemde
+62 dk)*. 🔒 Yani karar *"ek güvence yok"* diye değil, **"+30 dk'ya değmez"**
diye savunulabilir — ve K-088 **birinci gerekçeyi** yazmış. Öneri: gerekçe
**maliyet** olarak yeniden yazılsın, ve o 10 mutasyon `mutasyon_paketi.py`ye
**yorum bloğu olarak** *(havuza değil)* adlarıyla kaydedilsin ki *"hangi test
neyi koruyor"* bilgisi kaybolmasın.

---

## 4. İKİ AYAKLI ÖLÇÜT — Bölüm D

### D1 · Ayak 2 dekor mu — **DEKORDAN DA AZ: hiç okunmuyor**

`buyukluk_ayagi` `isaret_testi.py:177-181`de hesaplanıyor. Deponun
tamamında tüketicisi:

```bash
grep -rn "buyukluk_ayagi" --include=*.py . | grep -v __pycache__
```
→ **yalnızca tanım satırları** *(`isaret_testi.py:140,177`)*. Ne
`gecerlilik.py` okuyor, ne bir test, ne `satir()`. Kendi mutasyonum `X23`
*(alanı sıfırlamak)* **473 testin hiçbirini kırmadı**.

🔴 **Ve daha ağırı — koşul 2'de yapısal olarak boş.** `buyukluk_ayagi`
ancak `tohum_std` verilirse hesaplanıyor. Ölçüldü:

| üretici | `isaret_testi` çağrısı | `ga_std_kati` dolu satır |
|---|---|---|
| `kosul1` *(`gecerlilik.py:162`)* | `isaret_testi(farklar, tohum_std=std)` | **18/18** ✅ |
| `kosul2` *(`gecerlilik.py:219`)* | `isaret_testi([1e3 * x for x in farklar])` | 🔴 **0/12** |

Yani `06` §8.1b'nin — **mühre giden** tablonun — 12 satırının **hiçbirinde**
dışlanan etki büyüklüğü σ cinsinden yok, ve K3'ün ayak 2'si oraya
**uygulanamıyor**. Kural koşul 1'e uygulanmış, **komşusu koşul 2'ye
uygulanmamıştır**. Ve çapa testinin V5 koruması
*(`test_b130_kosul3_tohum_std_HESAPLANIYOR`)* yalnızca `kosul1`e bakıyor —
koruma da aynı asimetriyi taşıyor.

**Yargım:** bu `03` B5'in *"bildirim ≠ kullanım"* tuzağıdır, dürüst bir
*"eksik ölçüt"* beyanı **değildir**. Dürüst beyan `06` §9.2(a)'da
**vardır** ve doğrudur; kusur, beyanın **aracın çıktısına inmemesidir**
*(D2)* ve alanın hiç okunmamasıdır.

### D2 · `06` bunu söylüyor mu — **§9.2 EVET, §9.1 ve ARAÇ HAYIR**

| yer | ne diyor |
|---|---|
| `06` §9.2(a) son cümle | 🟢 *"koşul 1 bugün **HİÇBİR KOL için 'sağlandı' sayılamaz**"* — doğru ve açık |
| `06` Bölüm 9 özet tablosu *(satır 648)* | 🔴 *"🟡 ÖLÇÜLDÜ — **12 kol/senaryo/metrik çiftinin 2'si** geçmiyor"* → 10'u geçiyor izlenimi |
| `06` §9.2(c) *(satır 752)* | 🔴 *"**12 çiftin 2'si geçmiyor** tablosunu"* |
| `06` §9.2(b) *(satır 726)* | 🔴 *"**12/12** çiftte sağlanmıyor"* |
| **Aracın kendi çıktısı** | 🔴 sütun başlığı **`yargi`**, değerler **`GECTI` / `GECMEDI`**; özet bloğu *"KOSUL 1 OZETI — hangi kol/metrik cifti **gecmedi**"* *(hiçbiri düşmese **"hepsi gecti"** basacak — `gecerlilik.py:424-429`)* |

**Koşturuldu** *(`dogrulama/gecerlilik._yaz_kosul1`, depodaki güncel 360
satırdan)*: 18 satırın **15'i `GECTI`**, 3'ü `GECMEDI`.

🔴 Ve tablo **bayat**: ölçülen **18 çift** *(3 kol × 2 senaryo × 3 metrik)*,
düşen **3**:

| kol | senaryo | metrik | işaret | p |
|---|---|---|---|---|
| `gurultuden_kacan` | S2 | teslim_orani | 8/30 | 0,0161 |
| `en_kisa_yol` | S0 | gecikme ort | 22/30 | 0,0161 |
| 🆕 **`DV`** | **S2** | **gecikme ort** | **21/28** | **0,0125** |

Üçüncüsü `06`da **yok**. Aynı bayat cümle **beş belgede, altı yerde**:
`04:8142` · `06:648` · `06:752` · `09:82` · `12:86` *(ayrıca "240 koşu" —
bugün **360**)* · `13:226` ve `13:256`.

### D3 · Her tüketici doğru medyanı mı okuyor — **HAYIR**

`isaret_testi` iki estimand üretiyor *(B-124)*: `medyan_fark` **HAM**,
`medyan_fark_net` **GA'nın estimandı**. Basan taraflar:

| basan | ne basıyor |
|---|---|
| `isaret_testi.satir()` | ✅ ayrıştıklarında **ikisini de** *(`med=` + `med_net=`)* |
| — çağıranı | 🔴 **YOK.** `grep -rn "\bsatir(" dogrulama tests` → sıfır. `tests/test_isaret_testi.py` onu **içe bile aktarmıyor** |
| `gecerlilik._yaz_kosul1` *(satır 309)* | 🔴 `r['medyan_fark']` — **HAM**, GA'nın yanında |
| `gecerlilik._yaz_kosul2` *(satır 333)* | 🔴 `r['medyan_fark']` — **HAM**, GA'nın yanında |

**Ölçülen ayrışma — koşul 1'de 18 satırın 7'si:**

| kol/sen/metrik | berabere | **basılan** | GA'nın estimandı |
|---|---|---|---|
| `DV`/S2/teslim_orani | 3 | **+0,00000** | 🔴 **−0,00005** *(işaret ters)* |
| `DV`/S0/teslim_orani | 2 | **+0,00000** | 🔴 **−0,00001** *(işaret ters)* |
| `en_kisa_yol`/S2/teslim_orani | 2 | +0,00021 | +0,00058 |
| `DV`/S2/gecikme p95 | 2 | +0,00012 | +0,00030 |
| `gurultuden_kacan`/S2/gecikme p95 | 1 | −0,12574 | −0,13049 |
| `en_kisa_yol`/S0/gecikme p95 | 1 | +0,00164 | +0,00166 |
| `DV`/S0/gecikme p95 | 1 | −0,00000 | −0,00001 |

**Ve `06` §8.1b'nin DV satırlarının 4'ü de** *(berabere = 2)*:

| §8.1b'nin yazdığı | GA'nın estimandı | oran |
|---|---|---|
| HAM ortalama **+0,10 ms** | +0,24 ms | ×2,42 |
| HAM p95 **+3,06 ms** | +5,59 ms | ×1,83 |
| 🟢 ORTAK ortalama **+1,32 ms** | **+1,61 ms** | ×1,22 |
| 🟢 ORTAK p95 **+8,34 ms** | **+9,01 ms** | ×1,08 |

🔴 K-088'in manşet cümlesi — *"🟢 DV REÇETEYİ DOĞRULUYOR: ORTAK ortalama
**+1,32 ms** · ORTAK p95 **+8,34 ms**, p = 0,0094"* — **HAM medyanı**
kullanıyor. B-124'ün yasakladığı şey tam olarak budur, ve B-124'ü
kapatan oturumun kendi manşetindedir.

### D4 · Daha kötüsünü kur — **20 beraberlik düzeltildi, ama araç hâlâ tutarsız çift basar**

B-124 `isaret_testi`nin **alanlarını** ayırdı; `satir()` ikisini de basıyor.
Ama `_yaz_kosul1/2` yalnızca HAM'ı bastığı için **kırıcı vaka aynen
duruyor**, sadece basan yer değişti:

**Üretici** *(koşuldu)*:
```bash
PYTHONIOENCODING=utf-8 python -c "import sys;sys.path.insert(0,'.');from dogrulama.isaret_testi import isaret_testi,satir;r=isaret_testi([0.0]*20+[4.0]*5+[5.0]*5);print(r['medyan_fark'],r['medyan_fark_net'],r['ga']);print(satir('ornek',r))"
```
```
0.0   4.5   (4.0, 5.0)
ornek   10/10  p=0.0020 YON-RED ort=+1.5000 med=+0.0000 med_net=+4.5000 GA=[+4.0000, +5.0000]  (berabere 20)
```

`satir()` doğru davranıyor ✅ — ama çağrılmıyor. `_yaz_kosul1`in biçimiyle
aynı satır şöyle basılır:

```
GECMEDI        0.00000       [+4.00000, +5.00000]
```

🔴 *Medyan kendi GA'sının **dışında*** — B-124'ün kırıcı vakasının birebir
aynısı, düzeltmeden **sonra**, canlı üreticide. Vaka kapanmamış,
**taşınmıştır**.

🔴 **Daha kötüsü — işaret çelişkisi bugünkü gerçek veride var:**
`DV/S2/teslim_orani` satırı **`GECTI · med fark +0.00000 · GA [−0,00064,
+0,00042]`** basıyor; GA'nın estimandı **−0,00005**. Okuyucu *"fark yok"*
okur; ölçülen şey *"küçük ama NEGATİF fark"*tır.

---

## 5. DV KOLU — Bölüm E

### E1 · Kesişim benzer, sonuç zıt — **çünkü kesişim yanlış eksen**

**Y6 uygulandı: kendi lehine çıkan sonuca da.** Üç kol ölçüldü *(30 tohum,
depodaki güncel satırlardan, yeni koşu yok)*:

| kol | ORTAK ort. gecikme *(S0)* | S0 **p95** | tohum std | ORTAK fark | **fark / std** |
|---|---|---|---|---|---|
| `en_kisa_yol` | 32,51 ms | 81,80 ms | 13,84 ms | +5,40 ms | **0,390 σ** |
| 🔒 **`DV`** | **14,94 ms** | **23,16 ms** | 5,93 ms | +1,32 ms | **0,223 σ** |
| `gurultuden_kacan` | **548,50 ms** | 🔴 **12 611,91 ms** | **1 732,75 ms** | −61,69 ms | **−0,036 σ** |

🔴 **Kesişim oranları yakın *(%25,6 ↔ %20,7)* ama kollar aynı rejimde
değil:** `gurultuden_kacan`ın p95'i **12,6 saniye**, DV'ninki **23 ms** —
**545 kat**. Ve `gurultuden_kacan`ın tohumlar arası std'si *(1 732 ms)*
kendi medyan farkının **28 katı**; o kolun *"ters sonucu"* gürültünün
içinde yüzüyor, bir bulgu değil.

🔴 **Y6'nın kendi lehine olan yüzü:** DV'nin *"doğrulaması"* σ cinsinden
**üçünün EN KÜÇÜĞÜDÜR** *(0,223 σ)* — `en_kisa_yol`ınkinin yarısından
az. K-088 onu *"ve **en çok o** önemli"* diye yazıyor. Ölçüm bunu
desteklemiyor: DV'nin p'si küçük *(0,0094)* çünkü **işaret tutarlı**
*(20/26)*, **etki büyük olduğu için değil**. Ve §8.1b bu σ bağlamını
**basmıyor** *(D1: `kosul2` `tohum_std` geçirmiyor)* — yani okuyucu bunu
tabloda göremez.

⚖️ Doğru okuma: `06` §8.1b'nin üç kolu, `10` §0.2'nin dördüncü yargısına
göre ⚪ **KARŞILAŞTIRILAMAZ** — aynı büyüklüğü değil, üç farklı çalışma
rejimindeki üç farklı büyüklüğü taşıyorlar.

### E2 · Döngüsel bağımlılık var mı — **HAYIR; ama kırılgan bir yol var**

`gecerlilik.py:52` → `from dogrulama.kontrol_payi import mesafe_vektoru`;
`kontrol_payi.py` `gecerlilik`i **hiç** içe aktarmıyor *(grep: 0)*. Döngü
yok, ve import başka bir `cwd`'den denendi — çalışıyor.

🔴 **Ama:** `dogrulama/` altındaki 20 aracın 18'i `sys.path.insert(0,
str(KOK))` *(mutlak)* kullanırken **`kontrol_payi.py:34` ve
`mekanizma_kapisi.py:52`** `sys.path.insert(0, ".")` *(göreli)* kullanıyor.
`03` B5: *"Göreli sonuç yolu — yolları **depo köküne** mutlakla."* Kural 18
nesneye uygulanmış, ikisine uygulanmamış; ve `gecerlilik.py` artık
**o ikisinden birini içe aktarıyor**, yani bir üretim aracı içe aktarıldığı
her yerde `sys.path`e `"."` enjekte ediyor.

### E3 · DV'nin düşen çifti — **ÖLÇÜLDÜ: `en_kisa_yol/S0` ile AYNI SINIF**

Yeni koşu açılmadan ölçüldü: `tam` koşunun paketleri `kisa`nın
`pencere_kimlik_araligi`na göre **ERKEN/GEÇ** diye bölündü *(denetimin
§9.2(d)'de kullandığı ayrıştırmanın aynısı)*.

| kol/sen | KISA − TAM | KISA − TAM_ERKEN | TAM_ERKEN − TAM_GEÇ |
|---|---|---|---|
| `en_kisa_yol`/S0 | 22/30 · p 0,0161 · **+1,650 ms** | 0/1 · **berabere 29** | 22/30 · p 0,0161 · **+2,966 ms** |
| 🆕 **`DV`/S2** | 21/28 · p **0,0125** · **+0,832 ms** | 🔴 **TANIMSIZ · berabere 28** | 21/28 · p **0,0125** · **+1,496 ms** |
| `DV`/S0 | 18/29 · p 0,2649 · +0,158 ms | TANIMSIZ · berabere 29 | 18/29 · p 0,2649 · +0,286 ms |

🟢 **Aynı sınıf, kanıtlanmış:** `DV/S2`de kısa koşu ile tam koşunun aynı
kimlik aralığındaki paketleri **28/28 tohumda BİT-BİREBİR AYNI** — dinamik
etki **sıfır**. Bütün fark **pencere konumundan** geliyor *(ERKEN−GEÇ
+1,496 ms, aynı p)*. Yani `isinma_s = 50`'nin gecikme metriği için
yetersizliği **ikinci bir kolda** doğrulanıyor — `06` §9.1'in *"Faz 1'de
her protokol için yeniden ölçülmelidir"* uyarısını güçlendiren bir bulgu.

🔴 **Ama aynı ölçüm §9.2(d)'nin bir cümlesini çürütüyor:**

> §9.2(d): *"29/30 tohumda … BİT-BİREBİR AYNI … **'Koşu uzunluğu' diye bir
> dinamik etki YOK ve OLAMAZ.**"*

Ölçüldü — `gurultuden_kacan`/S2: **KISA − TAM_ERKEN 5/19, berabere yalnız
11**. Yani 30 tohumun **19'unda** kısa koşu ile tam koşunun erken kısmı
**aynı değil**. Cümle **tek kolda** ölçülüp *"OLAMAZ"* diye evrenselleştirilmiş;
komşu kolda tutmuyor *(Y4: "tek noktada tutan sonuç doğrulama sayılmaz")*.
*(Sebep büyük olasılıkla pencere kenarı sansürüdür — `olcum_bitis_s` 170 ↔
320 — ama §9.2(d) bunu ölçmüyor, "olamaz" diyor.)*

### E4 · DV'nin n'i neden küçük — **2 boş kesişim + 2 beraberlik; ve SEBEP hiçbir yerde yazılı değil**

Ölçüldü:

| kol | 30 tohumdan karşılaştırılabilen | `ortak_paket == 0` | beraberlik | **basılan n** |
|---|---|---|---|---|
| `en_kisa_yol` | 30 | 0 | 0 | 30 |
| `gurultuden_kacan` | 30 | 0 | 0 | 30 |
| **`DV`** | **28** | 🔴 **2** | **2** | **26** |

Yanlılık yaratıyor mu: 🟡 **kısmen.** Düşen iki hücre *"iki kolun hiç ortak
paketi yok"* hücreleridir — yani **en zor** tohumlar; onları düşürmek
kalan örneklemi **kolaylaştırır** *(`03` B3'ün seçilim yanlılığı, bir
katman yukarıda)*. Etki küçüktür *(2/30)* ama **yönü bellidir**.

🔴 **Ve raporlanmıyor:** `kosul2` `reddedilen`i hesaplıyor
*(`gecerlilik.py:189,198,201,220`)* ama `_yaz_kosul2` onu **basmıyor**
*(gövdede sıfır geçiş)*. Komşusu `_yaz_kosul3` `dejenere` sütununu
**basıyor**. `03` B2: *"üst sınır verirken **kaç gözlemle** hesaplandığını
da yaz."* `06` §8.1b **`14/26`** yazıyor ama 26'nın neden 30 olmadığını
yazmıyor. Kural koşul 3'e uygulanmış, komşusu koşul 2'ye uygulanmamıştır.

---

## 6. 🔴 ÖRÜNTÜNÜN DÖRDÜNCÜSÜ — Bölüm F

### F4 · ARANAN: *"bir kuralı bir nesneye uygulayıp yanındakine uygulamamak"*

Örüntü **üç kez** tekrarlamıştı. Bu denetim **altı yeni örneğini ölçtü** —
dördü B0.7/B0.8'in **kendi düzeltmelerinin içinde**:

| # | kural | uygulandığı nesne | 🔴 uygulanmayan **komşu** | bulgu |
|---|---|---|---|---|
| **4** | B-125: *"`gecti` yalnızca ayak 1; etiket bunu söylemeli"* | `isaret_testi.satir()` *(çağıranı **yok**)* | `gecerlilik._yaz_kosul1` — `06` §9.1'i **fiilen basan** yer | **B-145** |
| **5** | B-124: *"ayrıştıklarında ikisi de basılır"* | `isaret_testi.satir()` | `_yaz_kosul1` **ve** `_yaz_kosul2` — §8.1b'yi basan yer | **B-146** |
| **6** | B-135/B-136: *"DV kolu eklendi, tablolar güncellensin"* | `06` **§8.1b** *(koşul 2)* | `06` **§9.1 + Bölüm 9 özeti** *(koşul 1)* — aynı belge, aynı koşu · ve `04` · `09` · `12` · `13` | **B-147** |
| **7** | `03` B2: *"dışlanan etki, tohum std'sinin katı cinsinden"* | `kosul1` *(18/18)* | `kosul2` *(0/12)* — ve **çapa testinin V5 koruması da yalnızca kosul1'e bakıyor** | **B-148** |
| **8** | `03` B2: *"kaç gözlemle hesaplandığını da yaz"* | `_yaz_kosul3` *(`dejenere` sütunu basılıyor)* | `_yaz_kosul2` *(`reddedilen` **hesaplanıyor, basılmıyor**)* | **B-166** |
| **9** | D-11/B-134: *"dejenere payda tipli reddedilir"* | `kontrol_payi.eslestirilmis_oranlar` *(`b == 0` eleniyor)* | `gecerlilik.eslesmis_kol_orani` *(`min(...) == 0` → **ZeroDivisionError**)* | **B-155** |
| **10** | B-131: *"paket 35 → 41"* | **içe aktarma** yolu *(kapı)* — 41 ✅ | **betik** yolu *(`python dogrulama/mutasyon_paketi.py`)* — **35** | **B-149** |
| **11** | F-9/F-11: *"kalibrasyon tek işten kurulmaz"* | `pencere_kapsami.py` — **KOL × TRAFİK**, iki eksen de | `gecerlilik.py` — yalnız **KOL**; kendi en büyük maliyet ekseni **UZUNLUK** ve **SENARYO** örneklenmiyor | **B-154** |
| **12** | B-138: *"envanter yeniden ölçüldü — 473 test"* | `README` · `09` · `12` · `04` | `13` §3.1 *(satır 120)* — **471** | **B-163** |

> ⚖️ **Örüntü kapanmadı — ve artık düzeltmenin İÇİNDE değil, düzeltmenin
> KENDİ YÖNTEMİNDE.** F-11 *"AST ile doğruladım, `dogrulama/` altında
> tek-iş kalibrasyonu kalmadı"* dedi. Bu **doğru** *(F1'de doğrulandı)*.
> Ama F-11 **eksen sayısını** değil **dosya sayısını** denetledi:
> `gecerlilik.py` artık üç iş koşuyor ama üçü de **aynı senaryodan (S0)** ve
> **üçte ikisi kısa koşudan**. Tarama, aradığı şeyin **adını** buldu,
> **kendisini** değil.

### F1 · F-11'in taraması tam mı — **`dogrulama/` altında EVET; ama eksen bazında HAYIR**

`dogrulama/` · `tests/` · `sim/` tarandı *(`scratchpad/olcum/f1.py`)*.
`isler[0]` / tek-iş kalibrasyonu **kalmamış** ✅. `tests/test_kapi_secimleri.py:1510`'daki
`_kosu(isler[0])` bir kalibrasyon değil, D-13 kaçak testidir *(bilinçli)*.

🔴 **Ama `gecerlilik.py`nin kalibrasyonu kendi maliyet eksenini kaçırıyor.**
`_isler()` sabit tohumla karıştırıyor *(`random.Random(20260901)`)*, yani
seçilen üç iş **belirlenimcidir**. Koşturuldu:

```bash
PYTHONIOENCODING=utf-8 python -c "import sys;sys.path.insert(0,'.');from dogrulama.gecerlilik import _isler,KOLLAR;i=_isler();o=[next(x for x in i if x[0]['kol_adi']==k) for k in KOLLAR];[print(x[0], x[1]['kosu_bitis_s']) for x in o]"
```
```
{'kol_adi': 'en_kisa_yol',      'senaryo_etiket': 'S0', 'uzunluk': 'tam'}  350.0
{'kol_adi': 'gurultuden_kacan', 'senaryo_etiket': 'S0', 'uzunluk': 'kisa'} 200.0
{'kol_adi': 'DV',               'senaryo_etiket': 'S0', 'uzunluk': 'kisa'} 200.0
```

| eksen | iş listesi | kalibrasyon örneği |
|---|---|---|
| senaryo | S0 %50 · **S2 %50** | 🔴 **S0 %100** — S2 hiç örneklenmiyor |
| uzunluk | kısa %50 · tam %50 | 🔴 kısa **%67** · tam %33 |
| ortalama `kosu_bitis_s` | **275,0 s** | 🔴 **250,0 s** *(−%9,1)* |

Yani tahmin **sistematik olarak iyimser** — F-9'un teşhisinin birebir
aynısı, F-11'in düzeltmesinin içinde. `03` kural 7'nin *"30 dk'yı aşarsa
SOR"* kapısı bu tahmine bağlıdır.

### F2 · F-12 gibi kaç tane daha var — **EN AZ BİR, ve tam da B-135'in büyüklüğünde**

*ortanca · pay · çarpıklık · kesişim · fark · yüzdelik* tarandı.

🟢 **`yuzdelik` — B-128 gerçekten kapandı:** tek gövde
*(`sim/karsilastirma.py:48`)*, diğer üçü içe aktarıyor.
🟢 **`ortanca` — F-12 gerçekten kapandı:** iki araç da `statistics.median`.
🟢 **`carpiklik`** tek gövde. **`kesisim`** iki adlandırılmış özellik
*(`_birlesim` / `_pencere`)*, ikisi de etiketiyle basılıyor.

🔴 **Ama `08` md 25'in *"eşleştirilmiş kol oranı"* İKİ FARKLI YÜKLEM:**

| araç | formül | tipi |
|---|---|---|
| `kontrol_payi.eslestirilmis_oranlar:163` | `a / b` | **YÖNLÜ** *(< 1 olabilir)* |
| `gecerlilik.eslesmis_kol_orani:280` | `max(a,b) / min(a,b)` | **YÖNSÜZ** *(≥ 1)* |

**Koşturuldu** *(depodaki `kontrol_payi.jsonl`, güncel hash, 120 hücre)*:

```
a/b      (YONLU)  : n=58  min=4.02  max=38.03  ortanca=12.60
max/min  (YONSUZ) : n=58  min=4.02  max=38.03  ortanca=12.60
AYRISAN hucre    : 0
```

🔴 **İkisi bugün aynı çıkıyor — ama tesadüfen:** 58 hücrenin 58'inde
DV > gözlem. K-088 bunu *"🟢 ambiguity kaldırıldı, papered over edilmedi:
iki araç **aynı sonucu** veriyor"* diye yazıyor. Ölçüm **sayıyı**
doğruluyor, **mekanizmayı** doğrulamıyor: bir Faz 1 kolu gözlem kolundan
**daha az** kontrol baytı üretir üretmez *(sessiz senaryoda reaktif AODV
bunun doğal adayıdır)* iki araç iki farklı sayı basar ve **hiçbir şey
konuşmaz** — kendi mutasyonum `X9` bunu birebir yaptı ve **473 testin
hiçbirini kırmadı.** F-12'nin sınıfı *(`10` §0.2'nin ⚪ KARŞILAŞTIRILAMAZ
yargısı)* **kapanmamıştır.**

⚠️ Bir ikinci aday, bilinçli ve etiketli olduğu için bulgu sayılmadı:
*"kontrol payı"* iki gövde taşıyor — `sim/karsilastirma.py:104`
**PENCERE** alanlarından, `dogrulama/kontrol_payi.py:132` **TÜM KOŞU**
alanlarından. İkisi de çıktıda etiketle ayrılıyor *(`TUM KOSU` / `PENCERE`)*
ve `08` md 31 farkı yazıyor. 🟢 Kabul.

### F3 · F-10'un düzeltmesi tam mı — **🟢 EVET**

Tarandı *(`scratchpad/olcum/f3.py`)*: bir `.py` **kaynağını** okuyup içinde
dizgi arayan beş test var, ama **beşi de AST'ye çevrilmiş** —
`test_b100_*` *(`ast.walk` + çağrı adları)*, `test_b105_*` *(`d.func.attr`
kümesi)*, `test_d13_*` *(`ast.Call` + `Name.id`)*. Kalan `in` denetimleri
*(`test_b79_*` · `test_b93_*`)* **kodu değil, aracın ÜRETTİĞİ MESAJI**
denetliyor — orada dizgi araması doğru araçtır.

🟢 **F-10 kapandı.** ⚠️ Y11 sınırı yazılmalı: `test_d13_*`'in
`assert "Pool" not in cagrilar` yüklemi yalnızca **`Name`** çağrılarına
bakar — `multiprocessing.Pool(...)` *(Attribute)* ya da
`from multiprocessing import Pool as P` bu denetimden **sağ çıkar**.
Bulgu değil, **beyan edilmemiş bir sınır**.

---

## 7. YENİ BULGULAR — B-143 … B-168 (26 bulgu)

> Her satırın üretici komutu **§16'dadır** ve **yayımlanmadan önce olduğu
> gibi koşturulmuştur.**

| # | bulgu | kaynak | ağırlık |
|---|---|---|---|
| **B-143** | 🔴 Çapa testi `sim/` her değiştiğinde **9 testin 5'ini** sessizce atlıyor; yakalama oranı **13/26 → 7/26** *(McNemar p = 0,031)*, `gecerlilik.py` tek başına **8/15 → 2/15**. Kaybolanların içinde dosyanın **kendi varlık gerekçesi** olan V3 var | `tests/test_gecerlilik_araclari.py:66-77,208-214` · `sim/results.py:44` | 🔴🔴 **en ağır** |
| **B-144** | 🔴 O dosya **hiçbir kapı kriterinde yok**; ve bir `skip` kapıyı düşürmez — `_pytest()` yalnızca `passed`/`failed` ayrıştırıyor, `skipped` sayısını hiçbir koruma sabitlemiyor | `dogrulama/aile0_kapi_raporu.py:172-283,407-409` | 🔴🔴 |
| **B-145** | 🔴 **B-125'in düzeltmesi ölü kodda:** `isaret_testi.satir()`in deposunda **sıfır çağıranı** var; canlı üretici `_yaz_kosul1` hâlâ `GECTI`/`GECMEDI` basıyor *(18 satırın 15'i `GECTI`)* ve sütun başlığı `yargi` | `dogrulama/isaret_testi.py:185-206` vs `gecerlilik.py:298-312` | 🔴🔴 |
| **B-146** | 🔴 **B-124'ün düzeltmesi de aynı ölü kodda:** `_yaz_kosul1/2` HAM medyanı NET medyanın GA'sının yanında basıyor. Koşul 1'de **18 satırın 7'si** ayrışıyor, **2'sinde işaret ters**; `06` §8.1b'nin **DV satırlarının 4'ü de** *(K-088'in manşetindeki +1,32/+8,34 dâhil — doğrusu +1,61/+9,01)* | `gecerlilik.py:309,333` · `v2/06:566-569` · `v2/04` K-088 §2 | 🔴🔴 |
| **B-147** | 🔴 **DV koşul 2'ye eklendi, koşul 1'e eklenmedi.** Ölçülen **18 çiftin 3'ü** geçmiyor; belgeler **beş yerde** *"12 çiftin 2'si"* diyor. Yeni düşen çift `DV/S2/gecikme ort` **21/28 · p = 0,0125** hiçbir belgede yok. `12` ayrıca *"240 koşu"* diyor — bugün **360** | `v2/06:648,726,752` · `04:8142` · `09:82` · `12:86` · `13:226,256` | 🔴🔴 |
| **B-158** | 🔴 `06` §9.2(b)'nin **ε_rel** satırı: *(1)* **üretici kodu YOK** — `grep -rn "eps_rel\|ε_rel" sim dogrulama tests` → **sıfır**, sayı elle hesaplanmış *(`03` kural 1)*; *(2)* **bayat** — *"12/12"* değil **18/18**; *(3)* **bandın üst ucu tanımsız** — elle yeniden hesaplandığında 18 çiftin **2'sinde** *(`DV/S0` ve `DV/S2` teslim oranı)* HAM medyan **tam sıfır**, yani ε_rel bölünemiyor; NET medyanla band **%77,9 – %2 803**, yazılı **%4 397** değil. Aynı büyüklüğün iki estimandla iki farklı değeri olması B-146'nın ta kendisi *(`DV/S0/gecikme p95`: HAM ile **%9,9 × 10¹¹**, NET ile **%1 776**)* | `v2/06:726` · `v2/06:444` | 🔴 |
| **B-148** | 🔴 `kosul2` `isaret_testi`ye `tohum_std` **geçirmiyor**: `06` §8.1b'nin 12 satırının **0'ında** dışlanan etki büyüklüğü var *(`kosul1`de 18/18 var)*. K3'ün **ayak 2'si koşul 2'ye yapısal olarak uygulanamıyor**; ve çapa testinin V5 koruması da yalnızca `kosul1`e bakıyor | `gecerlilik.py:162` vs `:219` · `tests/test_gecerlilik_araclari.py:159` | 🔴 |
| **B-149** | 🔴 Altı yeni mutasyon `if __name__ == "__main__": main()` bloğunun **ALTINA** eklenmiş. Ölçüldü: içe aktarma yolu **41**, belgelenmiş betik yolu `python dogrulama/mutasyon_paketi.py` **35** — ve `main()` `BEKLENEN_MUTASYON`u **hiç kontrol etmiyor**, `✅ Ç1.3 GEÇTİ — 35/35` basıp `0` ile çıkar | `dogrulama/mutasyon_paketi.py:909-966,904-906` | 🔴 |
| **B-150** | 🔴 Mutasyon numaraları **tekrarlı**: `D26`, `D27`, `D28` her biri **iki** mutasyon adlandırıyor *(radio/mac/rng ↔ karsilastirma)*. Kayıtlarda *"D26"* artık tekil bir gönderme değil | `dogrulama/mutasyon_paketi.py:930,936,942` | 🔴 |
| **B-151** | 🔴 `test_b139`in `ORNEKLEM = 24` sabiti **`kor_mutasyon.py`de yok**; aracın varsayılanı **16** *(`sys.argv[1] if … else 16`)*. 24'ün tek kaynağı, başlığında **"🔴 DURUM: BAYAT … Bir sayıyı buradan OKUMA"** yazan `ciktilar/kor_cikti.txt`. Bayatlamayı önlemek için yazılan Y12 koruması, **ikinci bir elle tutulan sabit** getirmiş | `tests/test_kapi_secimleri.py:1919` · `dogrulama/kor_mutasyon.py:181` · `ciktilar/kor_cikti.txt:3` | 🔴 |
| **B-152** | 🔴 `08` md 35'in güvencesi *("okuyan `ozet()`in TANIMSIZ etiketini görmek zorundadır")* **üretim yolunda yok**: `ortak_alt_kume`ın tek üretim çağıranı `kosul2`dir ve `kontrol_payi_a/b`yi hiç okumaz, `ozet()`i hiç çağırmaz | `gecerlilik.py:188-212` · `v2/08:378` | 🔴 |
| **B-153** | 🔴 `08` md 25'in *"eşleştirilmiş kol oranı"* **iki farklı yüklem**: `a/b` *(yönlü)* ↔ `max/min` *(yönsüz)*. Bugün 58/58 hücrede aynı çıkıyor **çünkü DV her hücrede gözlemden büyük**; mutasyonum `X9` ikisini ayrıştırdı ve **473 testin hiçbiri kırılmadı**. F-12'nin sınıfı kapanmamış | `kontrol_payi.py:163` vs `gecerlilik.py:280` | 🔴 |
| **B-154** | 🔴 F-11'in `gecerlilik.py` kalibrasyonu **KOL eksenini** örnekliyor, aracın kendi maliyet eksenleri **UZUNLUK ve SENARYO**'yu örneklemiyor: üç örneğin **3'ü de S0**, **2'si kısa** → ortalama `kosu_bitis_s` **250 s** *(iş listesi: 275 s, −%9,1)*. F-9'un teşhisi, F-11'in düzeltmesinin içinde | `gecerlilik.py:375-384` | 🔴 |
| **B-155** | 🔴 `eslesmis_kol_orani` `bayt == 0`da **ZeroDivisionError** *(ölçüldü)*; komşusu `kontrol_payi.eslestirilmis_oranlar` aynı vakayı `b == 0` ile **açıkça eliyor**. B-134'ün `None` işlemesi bu komşu dejenere vakayı kapsamıyor | `gecerlilik.py:280-281` vs `kontrol_payi.py:160` | 🟡 |
| **B-156** | ⚠️ K-088'in 🔴 *"**Ölçülen kazanç**: 801 ortak paket · +10,140 ms artık üretiliyor"* cümlesi **gerçekleşmiş bir kazancı** değil, **sentetik olarak bozulmuş** bir girdiyi tarif ediyor *(`aile0_audit.md:9175`)*. Ölçüldü: bugünkü **88 karşılaştırmanın 0'ında** kontrol payı tanımsız | `v2/04:8693` · `v2/08:378` | 🟡 |
| **B-157** | ⚠️ `08` md 35'in *"önceki sonuçlar geçerli — reddedilen karşılaştırma sayı üretmemişti"* gerekçesi **toplu istatistik için yanlış**: reddedilen hücre örneklemden düşüyordu, artık düşmüyor → `n`, `p`, `ga`, `kesisim_*` **hepsi değişir**. Bugün zararsız *(0 hücre)*, Faz 1'de değil | `v2/08:428` · `gecerlilik.py:195-202` | 🟡 |
| **B-159** | ⚠️ Kapının **13 kriterinin 12'si** bu oturumda değişen koda **hiç dokunmuyor**. `sim/karsilastirma.py`yi içe aktaran tek test dosyaları `test_karsilastirma.py` ve `test_denetim2_boslukları.py`; **ikisi de hiçbir kapı seçiminde yok**. Yalnız **Ç1.3** dokunuyor *(41 mutasyon tam paketi koştuğu için)* | `dogrulama/aile0_kapi_raporu.py:172-283` | 🟡 |
| **B-160** | ⚠️ `06` §9.2(d)'nin *"'Koşu uzunluğu' diye bir dinamik etki **YOK ve OLAMAZ**"* cümlesi **tek kolda** ölçülmüş. `gurultuden_kacan`/S2'de KISA − TAM_ERKEN **5/19, berabere yalnız 11** — 30 tohumun **19'unda** eşit değil. Y4 | `v2/06:770-776` | 🟡 |
| **B-161** | ⚠️ **Y6 — kendi lehine çıkan sonuca uygulandı.** DV'nin *"doğrulaması"* σ cinsinden üçünün **en küçüğü** *(0,223 σ; `en_kisa_yol` 0,390 σ)*. Ve DV *(p95 23 ms)* ile `gurultuden_kacan` *(p95 **12 612 ms**, tohum std **1 733 ms** = medyan farkının 28 katı)* aynı rejimde değil — kesişim oranı yanlış eksen. K-088'in *"ve **en çok o** önemli"* cümlesi ölçümle desteklenmiyor | `v2/04` K-088 §2 · `v2/06:571-575` | 🟡 |
| **B-162** | ⚠️ K-086'nın **378 satırlık** gövdesinde çürüme işareti **4 satırda**; **68 tablo satırının 0'ında**. Ör. satır **8409** hâlâ *"`olu` kolu **analitik** çapası — 1,2963"* diyor; B-120 tam olarak *"band analitik DEĞİL"* dedi. Kayıt görünür ama **okunduğu yerde işaretsiz** | `v2/04:8104-8481` | 🟡 |
| **B-163** | ⚠️ `13` §3.1'in **2 Eylül'de yazılmış** düzeltme bloğu *"test sayısının (429 → **471**)"* diyor; ölçülen **473**. B-138 aynı gün README/`09`/`12`/`04`ü 473'e güncelledi, `13`ü güncellemedi | `v2/13:120` | 🟢 küçük |
| **B-164** | ⚠️ `kaynak_hash` **yalnızca `sim/`i** kapsıyor; `dogrulama/` **araç sürümü hiçbir sonuç satırında yok**. `08` md 36 *"koşuyu ayırmaz"* diyor ama *"aracı da ayırmaz"* demiyor. Ölçüldü: `pencere_kapsami.jsonl`de **eski hash altında 775 anahtar 2×, 26 anahtar 3×** duruyor. Yanlış okuma vakası: aynı satırlar 2× okunursa `8/30 · p = 0,0161` → `16/60 · p = **0,000394**` *(41 kat)*, 3×'te `p = 0,0000109` | `sim/results.py:44,78-84` · `v2/08:380` | 🟡 |
| **B-165** | ⚠️ `dogrulama/` altındaki 20 aracın 18'i `sys.path.insert(0, str(KOK))` *(mutlak)*, **`kontrol_payi.py:34` ve `mekanizma_kapisi.py:52`** `sys.path.insert(0, ".")` *(göreli — `03` B5)*. `gecerlilik.py` artık o ikisinden birini içe aktarıyor | `dogrulama/kontrol_payi.py:34` · `mekanizma_kapisi.py:52` | 🟢 küçük |
| **B-166** | ⚠️ `kosul2` `reddedilen`i hesaplıyor, `_yaz_kosul2` onu **basmıyor**; komşusu `_yaz_kosul3` `dejenere`yi **basıyor**. `06` §8.1b **`14/26`** yazıyor ama 26'nın neden 30 olmadığını *(2 boş kesişim + 2 beraberlik)* yazmıyor. Düşen iki hücre **en zor tohumlardır** — yönü belli, küçük bir seçilim | `gecerlilik.py:220` vs `:350` · `v2/06:566` | 🟡 |

| **B-168** | 🔴 **DV *bağlayıcı kol* ilan edildi ama `08` md 31'i ölçen araca EKLENMEDİ.** Depoda artık **üç ayrı kol kaydı** var: `AKTARICILAR` *(5 kol, DV yok)* · `gecerlilik.KOLLAR` *(3 kol, **DV var**)* · `pencere_kapsami.KOLLAR` *(5 kol, **DV yok** — `AKTARICILAR`ın kendisi)*. Sonuç: `06` koşul 3 DV'yi ölçüyor, `08` md 31'in pencere çarpıklığı bandı **DV'yi hiç görmüyor** — yani **bağlayıcı ilan edilen kolun pencere kapsamı ölçülmemiş**. Örüntünün bir örneği daha *(B-135 bir sözlüğe uygulandı, komşusuna uygulanmadı)* | `dogrulama/gecerlilik.py:80-84` vs `dogrulama/pencere_kapsami.py:64` · `v2/08:363` | 🔴 |
| **B-167** | ⚠️ **Kapı süresinin ilan edilen 165–330 dk bandı üst uçta tutmuyor.** `Pool(8)` çekişme çarpanı ilk kez ölçüldü: **1,795** *(yazılı 1,80 — 🟢 doğrulandı)*; bir dalga **1 767,3 sn**. Ç1.3 = taban + 6 dalga → bugünkü en iyi tabanla **193 dk**, `TEST_BASINA_EN_KOTU_S` ile **407 dk**; kapının tamamı **~204 – ~418 dk**, yani üst uç **%27** aşıyor. 🟢 Buna karşılık K-088'in *"~25 dk artar"* tahmini **tuttu** *(ölçülen 22–29,5 dk bandı içinde)*. ⚠️ Ve bugünkü koşu **2,081 sn/test** ile `OLCULEN_KOSULAR`ın **en iyisinin altına** indi — band ×2,11; çift **(473, 984.37)** olarak eklenmeli *(Y12)* | `dogrulama/mutasyon_paketi.py:141-160,780` · `v2/04` K-088 §5 | 🟡 |

*(Kapı süresi ölçümünün ayrıntısı §3'tedir.)*

---

## 8. 22 KAPANIŞIN BAĞIMSIZ DOĞRULAMASI

> Ölçüt: *"kapandı"* demek **(a)** değişiklik kodda **ve (b)** geri
> alındığında bir test konuşuyor demektir *(`03` Bölüm E, madde 1 + Y13)*.

| # | B0.7/B0.8'in iddiası | (a) kodda mı | (b) regresyonu var mı | yargı |
|---|---|---|---|---|
| **B-120** | sahte `assert` → gözlem | 🟢 evet | 🟢 `test_b130_olu_*` *(ama `sim/` değişince **atlanır**)* | 🟡 **KOŞULLU** |
| **B-121** | HAM p95 üretiliyor | 🟢 evet — 4 okuma **birebir** üretildi | 🟢 `X6` yakalandı *(durum A)* · 🔴 durum B'de **sağ kaldı** | 🟡 **KOŞULLU** |
| **B-122** | çürüyen paragraf görünür bırakıldı | 🟢 evet | — | 🟡 **§5'e bkz** *(B-162)* |
| **B-123** | 1 → 30 tohum | 🟢 evet *(`TOHUMLAR = range(1,31)`)* | 🔴 **YOK** — `X18` sağ kaldı | 🔴 **YARIM** |
| **B-124** | iki estimand ayrıldı | 🟢 alanlar var, `satir()` doğru | 🔴 **YOK** *(`X24` sağ kaldı)* · **ve canlı üretici hâlâ HAM basıyor** | 🔴 **TAŞINDI** *(B-146)* |
| **B-125** | ölçüt iki ayaklı | 🟢 alan var | 🔴 **YOK** *(`X23` sağ kaldı)* · **ve etiket düzeltmesi ölü kodda** | 🔴 **TAŞINDI** *(B-145)* |
| **B-126** | §9.2(b) güç + ε_rel yazıldı | 🟢 evet | — *(belge)* | 🟢 **GEÇERLİ** ⚠️ *"12/12"* bayat *(bugün 18)* |
| **B-127** | §9.2(c) taban çizgisi | 🟢 evet ve **açık** | — | 🟢 **GEÇERLİ** ⚠️ komşusu §9.1 çelişiyor *(B-147)* |
| **B-128** | `yuzdelik` tek gövde | 🟢 **AST ile doğrulandı: 1 gövde** | 🟢 kimlik testi | 🟢 **GEÇERLİ** |
| **B-129** | 8 belgede bayatlık yazıldı | 🟢 evet | 🟢 **üretici bugün `False` basıyor** *(koşturuldu)* | 🟢 **GEÇERLİ** |
| **B-130** | çapa testi 9/19 → 9/9 | 🟢 dosya var | 🔴 **`sim/` değişince 5/9 susuyor**; ve kendi kapsam tablosu bunu anmıyor | 🔴 **KOŞULLU/AĞIR** *(B-143)* |
| **B-131** | 6 mutasyon pakete girdi | 🟢 41, desenler **tam bir kez**, **6/6 beklenen testini kırıyor** *(koşturuldu)* | 🟢 Ç1.3 | 🟡 **betik yolu 35** *(B-149)* · numara çakışması *(B-150)* |
| **B-132** | `08` md 37 | 🟢 evet | — | 🟢 **GEÇERLİ** |
| **B-134** | `None` + `ozet()` | 🟢 kod değişti · 🟢 `test_karsilastirma.py:442,450` var | 🔴 **üretim yolu `ozet()` çağırmıyor** | 🟡 **KOŞULLU** *(B-152)* |
| **B-135** | iki araç aynı çifti ölçüyor | 🟢 sayı **birebir** doğrulandı *(4,02–38,03 · 12,60)* | 🔴 **iki farklı yüklem**, bugün tesadüfen aynı | 🟡 **KOŞULLU** *(B-153)* |
| **B-136** | §8.1b'ye 12 satır | 🟢 **12/12 birebir üretiliyor** *(koşturuldu)* | 🟢 `X3` · `X6` | 🟢 **GEÇERLİ** ⚠️ DV'nin 4 satırı yanlış estimand *(B-146)* |
| **B-137** | `kayit(dosya=)` AST testi | 🟢 evet, gerçekten AST | 🟢 test var | 🟢 **GEÇERLİ** |
| **B-138** | envanter yeniden ölçüldü | 🟢 **4538/10288/7564 · 15/20/31 · 473 — birebir** | 🟢 kendi koşum | 🟢 **GEÇERLİ** ⚠️ `13` 471'de kaldı *(B-163)* |
| **B-139** | `08` md 30 + Y12 testi | 🟢 231 = 255 − 24 | 🔴 **24 kodda yok, araç varsayılanı 16** | 🔴 **YARIM** *(B-151)* |
| **B-140** | `08` md 34 | 🟢 evet | — | 🟢 **GEÇERLİ** |
| **B-141** | 1/6,30 → 1/6,29 | 🟢 `06:786` ve `08:158` **aynı** | — | 🟢 **GEÇERLİ** |
| **B-142** | §8.1'in p95 işareti geri alındı | 🟢 evet | — | 🟢 **GEÇERLİ** |

**Sayım:** 🟢 **11 geçerli** · 🟡 **6 koşullu** · 🔴 **5 yarım ya da taşınmış**
*(B-123 · B-124 · B-125 · B-130 · B-139)*.

🔴 **B-133 B1.5'e taşındı** — bu meşrudur *(şema alanı)*, ama taşınırken
**kapsamı daraltılmış**: `08` md 36 *"koşuyu ayırmaz"* diyor; ölçülen daha
geniş — `kaynak_hash` **`dogrulama/`yi hiç kapsamıyor** *(B-164)*.

---

## 9. DÖRT DEVREDİLEN KARAR — ayrı ayrı yargı

> Karar **danışmanındı** *(K-088 §1)*; `03` Bölüm E bunu meşru kılar. Soru
> kararın alınmış olması değil, **savunulabilirliği**.

### K1 · B-134 — kontrol payı `None` → 🟡 **KARAR DOĞRU, UYGULAMA EKSİK**

🟢 Gerekçe sağlam ve `03` B3'e birebir oturuyor *(iki olguyu ayır)*; eski
davranış *"ölçülemezse hiçbir şey ölçme"*ye dönüşmüştü ve bu gerçekten
yanlıştı.
🔴 Ama kararın **bedeli** *("okuyan TANIMSIZ etiketini görmek zorunda")*
bir mekanizmaya bağlanmadı: tek üretim tüketicisi `ozet()`i çağırmıyor
*(B-152)*, ve *"ölçülen kazanç"* diye yazılan sayı sentetik *(B-156)*.
**Öneri:** `kosul2` `o.kontrol_payi_a/b`yi okusun ve `None` olan hücreyi
**ayrı sütunda saysın** — `kosul3`ün `dejenere` sütunuyla aynı biçimde.

### K2 · B-135 — bağlayıcı çift **DV ↔ gözlem** → 🟢 **SAVUNULABİLİR**

🟢 Gerekçe güçlü ve `03` kural 5'e dayanıyor: `en_kisa_yol` bir **kâhindir**,
Faz 1'i temsil edemez; DV kontrol düzlemi ağır, AODV de öyle olacak.
Ambiguity gerçekten kaldırılmış ve sayı **birebir** doğrulandı.
🔴 Tek çekince yüklem düzeyinde *(B-153)*: iki araç aynı **adı** taşıyan
iki **farklı** oran hesaplıyor; bugün tesadüfen çakışıyorlar.
⚠️ Ve `mesafe_vektoru`nun `AKTARICILAR`a **eklenmemesi** bilinçli ve
gerekçeli *(kapının Ç1 uç durum matrisi o sözlüğü ada göre kullanıyor)* —
🟢 bu doğru bir karardır; bedeli `gecerlilik.py`nin ikinci bir kol kaydı
tutması ve `sys.path` yolunun kırılganlaşmasıdır *(B-165)*.

### K3 · B-125 — ölçüt iki ayaklı, `k` boş → 🔴 **KARAR DOĞRU, KAYDI YANLIŞ YERE DÜŞTÜ**

🟢 *"`k`yi bugün uydurmamak"* kararı **kesinlikle doğru** ve `03` kural 2/3
gereğidir. Bir sabit uydurmak, ölçütün engellemeye çalıştığı şey olurdu.
🟢 Ve *"koşul 1 bugün hiçbir kol için sağlandı sayılamaz"* beyanı `06`
§9.2(a)'da **açık ve dürüst** yazılmıştır.
🔴 **Ama karar üç yerde etkisiz kaldı:** *(1)* etiket düzeltmesi çağrılmayan
bir fonksiyona yazıldı, araç hâlâ `GECTI` basıyor *(B-145)*; *(2)*
`buyukluk_ayagi` hiçbir yerde okunmuyor ve boşaltılması hiçbir testi
kırmıyor *(B-148)*; *(3)* koşul 2'de `tohum_std` verilmediği için ayak 2
oraya **hiç uygulanamıyor**. Karar kayda geçti, **koda geçmedi**.

### K4 · B-140 — kesişim alt sınırı beyan edildi → 🟢 **SAVUNULABİLİR**

🟢 *"Türetilmemiş bir eşik yazmak `03` kural 2'nin doğrudan ihlali olurdu"*
— doğru. Ölçüm *(%51,1 / %25,6 / %20,7, en dar hücre %5,6)* yapılmış,
`08` md 34'e üreticisiyle yazılmış, B4'e ölçülerek bırakılmış. Örnek bir
*"eşiği geriye dönük gevşetme"* karşıtı davranış.
⚠️ Tek eksik: madde 34 kesişimi yazıyor ama **kesişimin yanlış eksen
olabileceğini** yazmıyor — `gurultuden_kacan`ın kesişimi DV'ninkine yakın
ama rejimi 545 kat farklı *(B-161)*. B4'te *"kesişimi daralt"* deneyi bunu
görmezse yine tek eksende ölçüm yapılmış olur.

---

### 9.1 · `08`in DÖRT YENİ MADDESİ — *"önceki sonuçları geçersiz kılar mı"* cevapları

| md | `08`in cevabı | bu denetimin yargısı |
|---|---|---|
| **34** *(kesişim alt sınırı yok)* | ✅ Evet, beyan eksikliğiydi | 🟢 **DOĞRU** — `ortak_alt_kume` yalnızca `ortak_paket == 0`ı reddediyor *(`karsilastirma.py:191`)*, alt sınır hiç yoktu |
| **35** *(kontrol payı TANIMSIZ olabilir)* | 🔴 Davranış değişti · ⚠️ önceki sonuçlar **geçerli** | 🟡 **BUGÜN DOĞRU, GEREKÇE YANLIŞ** — reddedilen hücre örneklemden **düşüyordu**; artık düşmüyor, yani toplam istatistik değişir. Bugün 0 hücre etkilendiği için zararsız *(ölçüldü)*, ama tabloda yazan gerekçe bu ölçüme değil yanlış bir genellemeye dayanıyor *(B-157)* |
| **36** *(sonuç satırı koşuyu tanımlamıyor)* | ✅ Evet, beyan | 🟡 **DOĞRU AMA EKSİK** — `kaynak_hash` yalnızca `sim/`i kapsıyor; `dogrulama/` **araç sürümü hiç kaydedilmiyor** ve madde bunu yazmıyor *(B-164)* |
| **37** *(Ç4 sözleşme 5 dışında)* | ✅ Evet, beyan | 🟢 **DOĞRU** — `li_zincir.py`de `Kosu`/`kosucu`/`kayit(` geçişi **sıfır**; `li_calisma_noktasi.py`de `kayit(` **sıfır** *(ölçüldü)* |

## 10. DOĞRULANAN İDDİALAR

> Bu denetim **kendi ölçümüyle** yeniden ürettiği iddialar. Hiçbirinde
> iddianın kendi ölçütü kullanılmadı *(çalışma biçimi, madde 4)*.

| iddia | kim | doğrulama |
|---|---|---|
| **473 test geçiyor** | README · `12` | 🟢 `473 passed in 984.37s`, RC = 0, temiz kopyada — **kendi koşum** |
| Satır envanteri **4 538 / 10 288 / 7 564**, 15/20/31 dosya | B-138 | 🟢 **birebir** |
| `yuzdelik` **tek gövde** | B-128 | 🟢 AST + grep: 1 tanım, 3 içe aktarma |
| Kapı **BAYAT**, `89587a19…` ≠ bugünkü | B-129 | 🟢 üretici komut koşturuldu, `False` |
| `06` §8.1b'nin **12 satırının 12'si** üreticiden çıkıyor | B-136 | 🟢 `_yaz_kosul2` çıktısı belge tablosuyla **birebir** |
| `06` §8.1b HAM p95 `17/30 · p = 0,5847 · +7,11 ms` | B-121 | 🟢 birebir |
| 41 mutasyonun **41'inin de** deseni bugünkü kaynakta **tam bir kez** geçiyor | B-131 | 🟢 ölçüldü |
| Altı yeni mutasyonun **altısı da** `beklenen_test`ini kırıyor | B-131 | 🟢 iç içe koşuldu *(taban: 6/6 geçiyor → mutant: 6/6 kırılıyor)* |
| 41 mutasyonun `beklenen_test`lerinin **41'i de** `tests/` altında var | — | 🟢 ölçüldü |
| `08` md 25 bağlayıcı oran **4,0–38,0 kat · ortanca 12,6** | B-135 | 🟢 birebir *(⚠️ yüklem farkı: B-153)* |
| `1/6,29` iki belgede aynı | B-141 | 🟢 |
| F-10: metin tabanlı korumalar **AST'ye çevrilmiş** | F-10 | 🟢 beş koruma da AST |
| F-12: *"ortanca"* iki araçta da `statistics.median` | F-12 | 🟢 |
| F-11: `dogrulama/` altında **tek-iş** kalibrasyonu kalmamış | F-11 | 🟢 *(⚠️ eksen bazında değil: B-154)* |
| Çapa testi kendi ilan ettiği kapsamda **`main()`ı kapsamıyor** | B-130 | 🟢 6/6 `main()` mutasyonu sağ kaldı — **beyan doğru** |
| `06` §9.2(d): düşen çift **pencere içi ısınma artığı** | 7. denetim | 🟢 **ve DV/S2'de de doğrulandı** *(28/28 bit-birebir · ERKEN−GEÇ +1,496 ms)* |

---

## 11. ÜRETİLEMEYEN İDDİALAR

| iddia | nerede | ne oldu |
|---|---|---|
| 🔴 *"Koşul 1 bugün hiçbir kol için sağlandı sayılamaz"* | K-088 §1 K3 | **Araç bunu söylemiyor** — sütun başlığı `yargi`, 18 satırın **15'i `GECTI`**. `06` §9.2(a) doğru yazıyor; **araç ve `06`nın kendi özet tablosu** yazmıyor *(B-145 · B-147)* |
| 🔴 *"12 kol/senaryo/metrik çiftinin 2'si geçmiyor"* | `06` · `04` · `09` · `12` · `13` | **Üretilemiyor** — bugün **18 çift, 3'ü** geçmiyor *(B-147)* |
| 🔴 *"12/12 çiftte ε_rel sağlanmıyor"* | `06` §9.2(b) | Sayı bayat *(bugün 18 çift)*; ε_rel'i **üreten kod yok** — hiçbir araç `ε_rel` hesaplamıyor *(grep: 0)* |
| 🔴 *"240 koşu"* | `12` §B0.2 | Bugün **360** *(3 kol × 2 sen × 2 uzunluk × 30 tohum)* |
| 🔴 *"Ölçülen kazanç: 801 ortak paket · +10,140 ms **artık üretiliyor**"* | K-088 §1 K1 · `08` md 35 | Sayı **sentetik girdiden**; bugünkü 88 karşılaştırmanın **0'ında** eski davranış bir fark öldürürdü *(B-156)* |
| 🔴 *"`kor_mutasyon.py`nin çektiği örneklem = 24"* | `test_b139` yorumu | **Kodda yok**; araç varsayılanı **16** *(B-151)* |
| 🔴 *"Kapı süresi ~25 dk artar"* | K-088 §5 | §3'e bkz — **ölçüldü** *(B-158)* |
| 🔴 *"test sayısının (429 → 471) büyümesi"* | `13` §3.1 | **473** *(B-163)* |
| ⚠️ *"🟢 DV REÇETEYİ DOĞRULUYOR — ve **en çok o** önemli"* | K-088 §2 B-136 | Yön doğru; **büyüklük iddiası desteklenmiyor** — DV'nin etkisi σ cinsinden üçünün **en küçüğü** *(B-161)* |
| ⚠️ *"D26 · D27 · D28"* mutasyon adları | K-088 · paket | **Tekil değil** — her numara iki mutasyon adlandırıyor *(B-150)* |

---

## 12. 🔴 KENDİ MUTASYONLARIM

**Üretici:** `scratchpad/olcum/a4.py` *(dosyadan koşuldu — Windows `spawn`)*
· hedef: `tests/test_gecerlilik_araclari.py` + `test_isaret_testi.py` +
`test_kapi_secimleri.py`

🔴 **Kapsanan test kümesinin gerekçesi** *(neden tam paket değil)*: içe
aktarma taraması yapıldı — `dogrulama.gecerlilik`, `dogrulama.pencere_kapsami`
ve `dogrulama.li_calisma_noktasi`'yı içe aktaran **tek** test dosyası
`test_gecerlilik_araclari.py`; `dogrulama.isaret_testi`'yi içe aktaran tek
dosya `test_isaret_testi.py`; `dogrulama.kontrol_payi`'yı içe aktaran tek
dosya `test_kapi_secimleri.py`. Üçü birlikte koşulduğunda 473 testlik paketin
**bu beş modüle erişebilen tamamı** koşmuş olur. *(Doğrulama: `X3`, `X5`,
`X16`, `X22` bu kümede kırıldı ve **taban 89 testin 89'u geçiyor**.)*

### Y8 — bozulan yolun ÖNCE tetiklendiği gösterildi

| durum | taban çıktısı |
|---|---|
| A · `sim/` temiz | `89 passed in 22.20s` — **hiçbir test atlanmıyor**, beş `gecerlilik` testi de canlı |
| B · `sim/` değişmiş | `84 passed, 5 skipped in 21.04s` |

Ve her mutasyon için desen sayısı **tam bir kez** doğrulandı; 26'sının
26'sında uygulandı *(geçersiz mutasyon yok)*.

### Sonuç — ARAÇ BAZINDA oran · %95 GA

| araç | durum A *(sim temiz)* | %95 GA | durum B *(sim değişmiş)* | %95 GA |
|---|---|---|---|---|
| `gecerlilik.py` | **8/15 · %53,3** | [%30,1 · %75,2] | 🔴 **2/15 · %13,3** | [%3,7 · %37,9] |
| `pencere_kapsami.py` | 2/4 · %50,0 | [%15,0 · %85,0] | 2/4 · %50,0 | [%15,0 · %85,0] |
| `li_calisma_noktasi.py` | 1/2 · %50,0 | [%9,5 · %90,5] | 1/2 · %50,0 | [%9,5 · %90,5] |
| `isaret_testi.py` | 1/3 · %33,3 | [%6,1 · %79,2] | 1/3 · %33,3 | [%6,1 · %79,2] |
| `kontrol_payi.py` | 1/2 · %50,0 | [%9,5 · %90,5] | 1/2 · %50,0 | [%9,5 · %90,5] |
| **TOPLAM** | **13/26 · %50,0** | **[%32,1 · %67,9]** | **7/26 · %26,9** | **[%13,7 · %46,1]** |

*(`sim/karsilastirma.py` ayrıca sınandı: paketin kendi altı yeni mutasyonu
**6/6** kendi `beklenen_test`ini kırdı — §3.)*

### ULAŞILAN GÜÇ

n = 26, kesin binom. Gerçek kapsam **p** iken ≤13/26 gözlemek:

| gerçek kapsam | P(≤13/26) |
|---|---|
| %50 | 0,577 |
| %60 | 0,199 |
| **%70** | **0,0255** |
| %80 | 0,0006 |

🔒 **Dışlanan:** α = 0,05'te **gerçek kapsamın ≥%70 olduğu dışlanıyor**
*(durum A)*. Durum B'de %95 GA'nın üst ucu **%46,1** — yani `sim/`
değiştikten sonra gerçek kapsam **en fazla %46**.

### 🔴 SAĞ KALANLAR — ve hangi kapanışı geri aldıkları

| mutasyon | durum A | geri aldığı |
|---|---|---|
| `X18_TOHUM_30_dan_1_e` | 🔴 sağ | **B-123** *(`03` kural 2)* |
| `X24_medyan_fark_net_HAMA_dondu` | 🔴 sağ | **B-124** |
| `X23_buyukluk_ayagi_BOSALDI` | 🔴 sağ | **B-125 / K3** |
| `X10` · `X19_MAIN_kalibrasyon_TEK_IS` | 🔴 sağ | **F-9 / F-11** |
| `X25_ortanca_UST_ORTAYA_dondu` | 🔴 sağ | **F-12** |
| `X9_eslesmis_oran_YONLU_oldu` | 🔴 sağ | **B-135'in yüklem tekliği** |
| `X7` · `X8` *(dejenere/reddedilen sayılmıyor)* | 🔴 sağ | `03` B2 |
| `X11_MAIN_30dk_SORMA_kapisi_yok` | 🔴 sağ | `03` kural 7 |
| `X12_MAIN_D13_kacak_asserti_yok` | 🔴 sağ | `03` Bölüm C sözleşme 5 |
| `X13_MAIN_baglayici_oran_basilmiyor` | 🔴 sağ | `08` md 25 |
| `X21_MAIN_tek_bit_hizi` | 🔴 sağ | `08` Ç4 |

🔴 **Durum B'de bunlara altısı daha katılıyor:** `X1` *(V1)* · `X2` *(V2)* ·
`X3` *(**V3**)* · `X4` *(V5)* · `X6` *(B-121)* · `X14` *(`03` kural 2)*.

---

## 13. KAPSAM BEYANINA EKLENECEKLER

Bu denetimin **kendi** kapsam sınırları — ve `08`e eklenmesi önerilenler:

| # | ne | nereye |
|---|---|---|
| 1 | 🔴 *"`tests/test_gecerlilik_araclari.py` `sim/` her değiştiğinde 9 testinin 5'ini atlar; yakalama oranı %50 → %27 düşer"* | dosyanın **kendi kapsam tablosuna** *(beşinci satır)* + `08` |
| 2 | 🔴 *"`kaynak_hash` yalnızca `sim/`i kapsar; `dogrulama/` araç sürümü hiçbir sonuç satırında taşınmaz"* | `08` md 36'nın **genişletilmesi** |
| 3 | 🔴 *"`06` §8.1b'nin 12 satırının hiçbirinde dışlanan etki büyüklüğü (σ katı) yoktur; ölçütün ayak 2'si koşul 2'ye uygulanmaz"* | `06` §8.1b + §9.2(a) |
| 4 | 🔴 *"`06` §9.1'in tablosu bugün üreticiden çıkmıyor: 18 çift, 3'ü geçmiyor"* | `06` §9.1 — **üreticiden yeniden yazılmalı** |
| 5 | ⚠️ *"`08` md 25'in oranı iki araçta iki farklı yüklemle hesaplanır; bugün çakışmaları verinin özelliğidir"* | `08` md 25 |
| 6 | ⚠️ *"`test_d13_*`'in `Pool` denetimi yalnızca `Name` çağrılarını görür"* | testin kendi docstring'ine *(Y11)* |
| 7 | ⚠️ *"`06` §8.1b'nin DV satırları n = 26'dır; 30'dan düşüşün sebebi 2 boş kesişim + 2 beraberliktir"* | `06` §8.1b |
| 8 | ⚠️ *"`06` §9.2(d)'nin 'dinamik etki olamaz' cümlesi tek kolda ölçülmüştür"* | `06` §9.2(d) |

---

## 14. 🔴 ANLAŞILMAYANLAR — A-25'ten devam

> *"Anlamadığım bir mekanizma, denetlenmemiş bir mekanizmadır."* Bu bölüm
> boş bırakılamaz.

| # | anlamadığım | ne ölçtüm · neden yetmedi |
|---|---|---|
| **A-25** | 🔴 `_yaz_kosul1/2` ile `satir()` **neden iki ayrı biçimlendirici**? `satir()` `06` §9.1'in ölçütünü **doğru** biçimlendiriyor ve hiç çağrılmıyor; `_yaz_kosul1` aynı sözlüğü **yanlış** biçimlendiriyor ve `06`yı üretiyor. Bu bilinçli bir ayrım mı *(tablo ↔ tek satır)*, yoksa `satir()` bir zamanlar çağrılıyor da mı düştü — **belirleyemedim.** Karar kayıtlarında ikisinin ilişkisine dair **hiçbir cümle yok** | grep + AST: `satir(` çağrısı **sıfır**; `test_isaret_testi.py` onu içe aktarmıyor. Hangi yönde düzeltileceği *(biçimlendiriciyi tekilleştirmek mi, `_yaz_*`i düzeltmek mi)* bir **karar**, ölçüm değil |
| **A-26** | 🔴 `gurultuden_kacan`ın S0'daki **p95'i 12 611,91 ms** — 12,6 **saniye**. Aynı senaryoda `DV` 23,16 ms, `en_kisa_yol` 81,80 ms. **545 kat.** Bu bir kuyruk çöküşü mü, bir yönlendirme döngüsü mü, yoksa metriğin o kolda **başka bir şey ölçmesi** mi *(`03` B3: "bir metrik bir protokol sınıfı için geçersiz olabilir")* — **ölçmedim** | Ölçtüğüm: teslim oranı S0'da **0,343** *(kâhin 0,996)*, ORTAK ortalama 548,50 ms, tohum std **1 732,75 ms**. Bu kolun sayıları `06` §8.1b'ye **girdi** ve *"reçeteyi çürütmüyor"* diye okundu. 🔴 Ama bir kol metriğin geçerlilik alanının dışındaysa, onun *"ters sonucu"* bir bulgu değil bir **artefakt**tır — ve bunu ayırt edecek ölçüm yapılmadı *(ne bu denetimde ne öncekilerde)* |
| **A-27** | 🔴 `gurultuden_kacan`/S2'de **KISA ile TAM_ERKEN neden aynı değil** *(30 tohumun 19'unda)*? `en_kisa_yol` ve `DV`de 28–29/30 **bit-birebir**. En olası açıklama pencere kenarı sansürüdür *(`olcum_bitis_s` 170 ↔ 320; kenarda doğup sonra teslim olan paketler)*, ama **ölçmedim** — kimlik kümelerinin farkını çıkarmak gerekirdi | `06` §9.2(d) bu ihtimali hiç anmadan *"dinamik etki **YOK ve OLAMAZ**"* diyor. Cümle tek kolda ölçülmüş; ben ikinci kolda **tutmadığını** gösterdim ama **sebebini gösteremedim** |
| **A-28** | `DV` kolunda **iki tohumda** *(30'un 2'si)* S0 ile S2'nin **hiç ortak paketi yok**. Dejenere bir topoloji mi, tam kopma mı, yoksa DV'nin yakınsamama durumu mu — **bakmadım** | Ölçtüğüm yalnızca sayı *(2)* ve yönü *(düşenler en zor tohumlar)*. `06` §8.1b n = 26 yazıyor, sebebini yazmıyor *(B-166)* |
| **A-29** | 🔴 **Aynı paket, aynı kod, 984 ↔ 1 851 sn *(×1,88)*.** Deponun kendi kaydı *(`04`:6614)* bunu *"sebep ne olursa olsun"* diye bırakmış. Ben bugün **en iyi okumayı** ölçtüm *(2,081 sn/test — yazılı bandın **altında**)*, yani band **2,081–4,385 = ×2,11**e genişledi. Sebebi **ölçmedim** | Bu, kapı süresi tahmininin *(§3)* ve `MUTANT_ZAMAN_ASIMI_S`in **tek girdisidir**. Sebep bilinmeden marj hesabı bir tahmin, ölçüm değil |
| **A-30** | `mesafe_vektoru` bir **yönlendirme kolu** ama `dogrulama/kontrol_payi.py`de tanımlı, `aktaricilar.py`de değil. K-088 bunu gerekçelendiriyor *(kapının Ç1 uç durum matrisi `AKTARICILAR`ı ada göre kullanıyor)* ve gerekçe geçerli — **ama** `gecerlilik.py` artık bir ölçüm aracından bir **deney kolu** içe aktarıyor. Bunun Faz 1'de AODV/OLSR eklenirken nasıl ölçekleneceğini **göremiyorum** | Ölçtüğüm: döngüsel bağımlılık **yok**; `sys.path` yolu kırılgan *(B-165)*. Ölçmediğim: `KOLLAR` sözlüğü üç yerde *(`AKTARICILAR`, `gecerlilik.KOLLAR`, `pencere_kapsami.KOLLAR`)* ayrı ayrı tutulduğunda Faz 1'de hangisinin bağlayıcı olacağı |
| **A-31** | `06` §9.2(b)'nin **ε_rel**'ini hiçbir kod hesaplamıyor *(B-158)*. Sayının **nasıl** üretildiğini — hangi medyanla, hangi çiftlerle — **bulamadım**; yalnızca alt ucun *(%77,9)* bugünkü `en_kisa_yol/S0/gecikme ort` çiftiyle uyuştuğunu gördüm | Üst uç *(%4 397)* bugün `en_kisa_yol/S2/gecikme p95`ten çıkıyor — yani sayı **iki kollu** dönemden. DV'li dünyada band **%77,9 – %2 803** *(NET)* ya da **tanımsız** *(HAM, 2 çift)* |

---

## 15. 🔴 SENİN YARGIN

> ## B0.7/B0.8'in kapattığı 22 bulguya **KISMEN GÜVENİLİR**, çünkü…

…**kapanışların 11'i bağımsız olarak yeniden üretildi ve tuttu**, ama
**5'i ya yarım ya da yalnızca yer değiştirdi** — ve yer değiştirenler tam
olarak oturumun **en pahalı** iki düzeltmesidir *(B-124 · B-125)*: doğru
teşhis, doğru ilaç, **hastanın olmadığı odaya bırakılmış**. `isaret_testi.satir()`
deposunda **sıfır çağıranı olan bir fonksiyondur**; `06` §9.1 ve §8.1b'yi
fiilen basan `_yaz_kosul1/_yaz_kosul2` dokunulmadan kalmıştır. Sonuç
ölçülebilir: koşul 1'in 18 satırının **15'i hâlâ `GECTI`** basıyor, 7'sinde
basılan medyan yanındaki GA'nın estimandı değil, ikisinde **işaret ters** —
ve K-088'in kendi manşet sayıları *(+1,32 / +8,34 ms)* yanlış estimanddan
geliyor.

Ve güvenin sınırını çizen şey bulguların sayısı değil, **korumanın
davranışıdır:** üç üreticinin tek koruması `sim/` değişir değişmez
9 testinin 5'ini atlıyor; kendi 26 mutasyonumla ölçüldü, yakalama
**%50,0 → %26,9** *(McNemar p = 0,031)*. B1'in **ilk işi `sim/`e Kat 4
eklemektir** — yani bu koruma, ihtiyaç duyulacağı ilk gün susacaktır. Buna
`03` Bölüm E'nin *"bitmiş modül"* ölçütü eklenince tablo netleşiyor:
**B-123 · B-124 · B-125 · F-9/F-11 · F-12** geri alındığında **473 testin
hiçbiri konuşmuyor.** Yani bu beş kapanış, deponun kendi tanımıyla
*"bitmiş"* değildir.

⚖️ **Ama güvensizlik de doğru kelime değil.** Bu oturum kendi **dört**
kusurunu *(F-9 … F-12)* buldu ve kaydetti — ve F-11'i düzeltirken aynı
sınıfın üçüncü tekrarını **kendi içinde** yakaladı; bu, denetlenmekten çok
denetlemeye benzeyen bir davranıştır. B-128, B-129, B-136,
B-138, B-131'in altı mutasyonu ve F-10'un AST dönüşümü **birebir tuttu**;
ε_rel ve kesişim alt sınırı için *"bir sayı uydurmamak"* kararı `03` kural
2'nin doğru uygulanmasıdır ve kolay olan yol değildi. Kusur **dikkatte**
değil, **kapsamdadır**: düzeltmeler nesne nesne yapılıyor, **sınıf sınıf**
değil. Örüntü yedi denetimdir kapanmıyor çünkü her seferinde *"bu nesneyi
düzelttim"* deniyor, *"bu kuralı hangi nesnelere uygulamam gerekir"*
sorulmuyor.

🔴 **B1'e geçilmemeli** — ama engel büyük değil: §0'daki dört maddelik asgari
liste, hiçbiri yeni ölçüm gerektirmeyen bir günlük iştir. **Şema son kez
donacaksa**, üstünde duran sayıların doğru estimanddan gelmesi ve koşul 1'in
durumunun altı belgede doğru yazılması, o donmadan **önce** olmalıdır.

---

## 16. KOŞTURDUĞUM KOMUTLAR

> Hepsi **yayımlanmadan önce olduğu gibi** koşturuldu. Depoyu değiştiren
> hiçbir komut yok; bütün denemeler `tempfile.mkdtemp` kopyalarında.

**Ölçüm ortamı:** `PYTHONIOENCODING=utf-8` · 12 çekirdek · kopyalar
`dogrulama/kopya.py::depoyu_kopyala` ile *(`v2/` **dâhil**)*.

### Taban ve envanter
```bash
PYTHONIOENCODING=utf-8 python -c "import sys;sys.path.insert(0,'.');from sim.results import kaynak_hash;print(kaynak_hash())"
```
→ `fc73905bbb00ad719b31eb5dbb9f8f19`

```bash
PYTHONIOENCODING=utf-8 python -m pytest tests -q --tb=no -p no:cacheprovider
```
→ **`473 passed in 984.37s (0:16:24)`** · RC = 0 · temiz kopyada
*(2,081 sn/test — deponun `OLCULEN_KOSULAR` bandının **altında**; band
2,081–4,385 = **×2,11**)*

```bash
for d in sim tests dogrulama; do find $d -name "*.py" -not -path "*__pycache__*" | wc -l; cat $d/*.py | wc -l; done
```
→ 15 / **4538** · 20 / **10288** · 31 / **7564** — B-138 **birebir**

### A1 — çapa testi uyuyor mu
```bash
cd <kopya> && echo "# zararsiz yorum" >> sim/packet.py
PYTHONIOENCODING=utf-8 python -m pytest tests/test_gecerlilik_araclari.py -q -rs
```
→ önce `9 passed in 3.20s` · sonra **`4 passed, 5 skipped in 1.97s`**

### A2 — kapı kapsamı
```bash
grep -rn "gecerlilik_araclari" dogrulama/ tests/ v2/ --include=*.py --include=*.md
grep -rn "473\|468\|skipped" tests/ dogrulama/
```
→ `dogrulama/` altında **0** · toplam sayıyı/`skipped`ı sabitleyen koruma **0**

### A4 · §12 — kendi mutasyon paketim *(26 mutasyon × 2 durum)*
```bash
PYTHONIOENCODING=utf-8 python scratchpad/olcum/a4.py
```
→ durum A `13/26` · durum B `7/26` · taban A `89 passed`, taban B
`84 passed, 5 skipped`

### C1/C2 — altı yeni mutasyon
```bash
PYTHONIOENCODING=utf-8 python -c "import sys;sys.path.insert(0,'.');from dogrulama.mutasyon_paketi import MUTASYONLAR;print(len(MUTASYONLAR))"
```
→ **41** *(içe aktarma yolu)* · aynı dosya **betik** olarak koşulduğunda
`main()` **35** görüyor *(B-149; kopyada `main()`e sayaç yamalanarak ölçüldü)*

```bash
PYTHONIOENCODING=utf-8 python scratchpad/olcum/c2.py
```
→ altı mutasyonun **6/6'sı** taban temizken geçen `beklenen_test`ini
mutantta **kırıyor**

### C3 — `Pool(8)` çekişme çarpanı
```bash
PYTHONIOENCODING=utf-8 python scratchpad/olcum/c3_pool8.py
```
*(kapının kendi `_kosu` fonksiyonu, kendi `Pool(8)`u, ilk sekiz mutasyon —
sonuç §3'te)*

### B · D · E — ölçüm betikleri *(hepsi depodaki `.jsonl`den; yeni koşu yok)*
```bash
PYTHONIOENCODING=utf-8 python scratchpad/olcum/d_olcum.py    # kosul1/kosul2 ham alanlar + basılan tablo
PYTHONIOENCODING=utf-8 python scratchpad/olcum/b_olcum.py    # 88 karşılaştırma, None kontrol payı, ZeroDivisionError
PYTHONIOENCODING=utf-8 python scratchpad/olcum/e.py          # E1 · E3 · E4
PYTHONIOENCODING=utf-8 python scratchpad/olcum/ga.py         # Wilson GA + güç + McNemar
```

### F — taramalar
```bash
PYTHONIOENCODING=utf-8 python scratchpad/olcum/f1.py   # tek-iş kalibrasyonu (dogrulama+tests+sim)
PYTHONIOENCODING=utf-8 python scratchpad/olcum/f3.py   # metin tabanlı korumalar
PYTHONIOENCODING=utf-8 python -c "import sys;sys.path.insert(0,'.');from dogrulama.gecerlilik import _isler,KOLLAR;i=_isler();o=[next(x for x in i if x[0]['kol_adi']==k) for k in KOLLAR];[print(x[0], x[1]['kosu_bitis_s']) for x in o]"
```

### Tekil doğrulamalar
```bash
PYTHONIOENCODING=utf-8 python -c "import sys;sys.path.insert(0,'.');from dogrulama.isaret_testi import isaret_testi,satir;r=isaret_testi([0.0]*20+[4.0]*5+[5.0]*5);print(r['medyan_fark'],r['medyan_fark_net'],r['ga']);print(satir('ornek',r))"
grep -rn "\bsatir(" --include=*.py dogrulama tests | grep -v "_satir\|def satir"
grep -rn "buyukluk_ayagi" --include=*.py . | grep -v __pycache__
grep -rn "eps_rel\|ε_rel" --include=*.py sim dogrulama tests
grep -rn "\.ozet()" --include=*.py . | grep -v tests/
grep -rn "sys.path.insert" dogrulama/*.py
grep -rn "def yuzdelik" --include=*.py . | grep -v __pycache__
```

**Süreler:** tam paket **984 sn** · çapa testi **3,2 sn** *(temiz)* / **2,0 sn**
*(`sim/` değişmiş)* · kendi mutasyon paketim **~35 dk** · C3 §3'te ·
jsonl analizleri **< 10 sn** her biri.

🔒 **Ana deney tohumları (2000–2029) hiçbir amaçla koşulmadı.** Kullanılan
tohumlar **1–30** *(ayarlama/kapı kümesi)*.

---

## 17. 🔴 OKUMA KAPSAMIM — hangi dosyanın hangi satır aralığını OKUMADIM

> `03` kural 1'in ruhu: okumadığım şeyi *"okudum"* diye yazmam. Aşağıdaki
> tablo **eksiklerimi** listeler, kapsamımı değil.

### SONUNA KADAR okuduklarım

`v2/03-YONTEM-KURALLARI.md` *(230)* · `tests/test_gecerlilik_araclari.py`
*(245)* · `dogrulama/gecerlilik.py` *(435)* · `dogrulama/isaret_testi.py`
*(206)* · `dogrulama/kontrol_payi.py` *(281)* · `sim/karsilastirma.py`
*(451)* · `sim/results.py` *(117)* · `dogrulama/kopya.py` *(91)*

### PARÇA okuduklarım — **okumadığım aralıklar**

| dosya | satır | **OKUMADIĞIM** |
|---|---|---|
| `v2/04-NEDEN-BOYLE.md` | 8 915 | 🔴 **1–235 · 239–8 021 · 8 131–8 408 · 8 410–8 481 · 8 531–8 651 · 8 842–8 915** — yani **~%93'ü**. Okuduğum: 236–238, 8 022–8 130, 8 409, 8 482–8 530, 8 652–8 841 *(K-086 banner · K-087 bulgu tablosu · **K-088 tamamı** · Y1–Y14)* + grep isabetleri |
| `aile0_audit.md` | 10 225 | 🔴 **1–9 149 · 9 196–9 479 · 9 531–10 210** — **~%98'i**. Okuduğum: 9 150–9 195 *(B-133/B-134 kanıtı)*, 9 480–9 530 *(B-120…B-142 tablosu + §8)*, son 15 satır |
| `v2/06-ON-KAYIT.md` | 802 | **1–508 · 629–641 · 783–802** — okuduğum 509–628 *(§8.1 · §8.1b)* ve 642–782 *(Bölüm 9 tamamı)* |
| `v2/08-AILE0-KAPSAM.md` | 530 | **1–279 · 321–375 · 383–395 · 451–530** — okuduğum 280–320, 376–382 *(md 34–37)*, 396–450 *(geçersizlik tablosu + anlaşılmayanlar)* |
| `v2/13-AILE0-KAPANIS-KANITI.md` | 396 | **1–89 · 131–396** — okuduğum 90–130 *(§3.1)* + grep isabetleri |
| `README.md` | 227 | **tamamı okunmadı** — yalnızca grep isabetleri *(8, 32, 33, 128–146, 227)* |
| `dogrulama/mutasyon_paketi.py` | 966 | **260–509 · 555–675 · 700–780** — okuduğum 1–260 *(sabitler)*, 510–554 *(`_kosu`)*, 780–966 *(`paketi_kostur` · `main` · B-131)* |
| `dogrulama/aile0_kapi_raporu.py` | 618 | **1–149 · 320–380** — okuduğum 150–319, 380–618 |
| `tests/test_kapi_secimleri.py` | 1 935 | 🔴 **~%85'i**. Okuduğum 430–470, 750–850, 925–960, 1 100–1 130, 1 495–1 545, 1 866–1 935 |
| `dogrulama/pencere_kapsami.py` | 269 | **1–89 · 146–199 · 250–269** — okuduğum 90–145, 200–249 |
| `dogrulama/li_calisma_noktasi.py` | 128 | **1–54 · 96–128** — okuduğum 55–95 |
| `dogrulama/kor_mutasyon.py` | 241 | **1–169 · 201–241** — okuduğum 170–200 |
| `tests/test_isaret_testi.py` | 145 | **41–145** — okuduğum 1–40 + grep |

### HİÇ AÇMADIKLARIM

🔴 `sim/` altında **12 dosya** *(`kosucu.py` 914 · `mac.py` 693 ·
`gozlem.py` 572 · `config.py` 510 · `radio.py` 325 · `topology.py` 180 ·
`rng.py` 156 · `traffic.py` 146 · `ledger.py` 140 · `queues.py` 132 ·
`events.py` 82 · `packet.py` 62 · `__init__.py` 58)* — **4 087 satır**
· `tests/` altında **15 dosya** *(~7 500 satır)* · `dogrulama/` altında
**22 araç** *(~4 800 satır)* · `v2/00 · 01 · 02 · 05 · 07 · 09 · 10 · 11 ·
12` *(**~4 400 satır**)* · `denetim/` altındaki dokuz prompt · `ciktilar/`
altındaki `.txt` dosyaları *(`kalibrasyon_c.txt` · `ayikla_cikti.txt` ·
`literatur_eksenleri_cikti.txt`)*

### 🔴 BÜTÇE YETMEDİ — yedinci denetimin okumadıkları

Yedinci denetim *"`04`ün %93'ünü, `aile0_audit.md`nin altı denetim
gövdesini okumadım"* diye yazmıştı. **Ben de okumadım** — ve
**K-001 … K-085** arasında bu oturumun dört kararına aykırı bir kayıt olup
olmadığına **bakılmadı.** Bu, önceki denetimin açık bıraktığı boşluğun
**aynen devam ettiği** anlamına gelir; bir sonraki denetimin ilk işi
olmalıdır.

⚠️ `v2/yeni_detaylı_arastırma/` **bu depoda yok** *(kök listelendi:
`README.md · aile0_audit.md · ciktilar/ · denetim/ · dogrulama/ · sim/ ·
tests/ · v2/`)*. Denetim promptunda anılan o dizin ya silinmiş ya da
başka bir konumdadır — **doğrulayamadım.**

---

---

## 🔒 KAPANIŞ BEYANI

**Bu oturumda depodaki hiçbir dosya DEĞİŞTİRİLMEDİ.** Yazılan tek depo
dosyası bu rapordur *(`aile0_audit.md`)*; önceki **yedi denetimin metnine
dokunulmamıştır** — yalnızca dosyanın **sonuna** sekizinci bölüm
eklenmiştir.

**Bütün denemeler geçici kopyalarda yapıldı** *(`tempfile.mkdtemp` +
`dogrulama/kopya.py::depoyu_kopyala`, **`v2/` dâhil**)*; kopyalar iş bitince
`shutil.rmtree` ile silindi. `sim/`, `tests/`, `dogrulama/`, `v2/` ve
`ciktilar/` altındaki hiçbir dosyaya yazılmadı.

🔒 **BU OTURUMDA HİÇBİR GİT KOMUTU ÇALIŞTIRILMADI — `status` dâhil.**

🔒 **Ana deney tohumları (2000–2029) hiçbir amaçla koşulmadı.** Kullanılan
bütün tohumlar **1–30** aralığındadır *(ayarlama/kapı kümesi, K-025)*.

🔒 **30 dakikayı aşan tek koşu** *(`Pool(8)` çekişme ölçümü, tahmin 30–56 dk,
ölçülen 29,5 dk)* **öncesinde süre tahmini yazdırıldı ve öğrenciye soruldu**
*(`03` kural 7)*; onay alındıktan sonra koşuldu.

> **Bir şeyi büyütmek istiyorsan önce ölç.** Bu denetimde ölçülen şey bir
> düzeltmenin **varlığı** değil, **etkisiydi** — ve iki düzeltme, doğru
> yazılmış olmalarına rağmen, hiç kimsenin okumadığı bir fonksiyonda
> duruyordu.
