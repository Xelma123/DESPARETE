# 08 — FAZ 0 KAPSAM BEYANI

> ⚠️ **DOSYA ADI TARİHSELDİR** — `AILE0` yazıyor, içerik **Faz 0**'dır.
> Ad değiştirilmedi çünkü depoda ona yapılan atıflar kırılırdı.

> ⚠️ **1 Eylül 2026'da güncellendi** *(K-081)*. Belge eskiden *"Faz 0"*
> diyordu; proje artık **FAZ** *(iş aşaması)* ile **AİLE** *(Holm düzeltme
> birimi)* ayrımını kullanıyor. İçerik aynı, ad değişti.

> # 🟡 FAZ 0 — KAPI 13/13 GEÇTİ, AMA **KAPALI DEĞİL**
>
> **Son kapı koşusu: 27 Ağustos 2026 · 13/13 · 185,6 dk.**
>
> ~~🟢 VE SONUCU BAYAT DEĞİL~~ → 🔴 **BAYAT** — `sim/` B0/B0.7/B0.8'de değişti *(`89587a19…` → `fc73905b…`)*. Bu **bilerek**: kapı `12` §2.3 gereği **B0 ve B1 birlikte bittikten sonra TEK KEZ** koşar. **B-129**.
>
> ⚠️ **Davranış değişmedi, ölçüldü:** `89587a19…` ↔ `0a1a94e5…` arasında
> **120 iş bit-birebir**; kapının yeniden koşma gerekçesi sonuçların
> değişmesi **değil**, mutasyon havuzunun ve test sayısının büyümesidir.
> Yani 13/13 **bugünkü koda** aittir.
>
> 🟢 **B0 KOŞULDU** *(K-086)* — sekiz kalemin **dördü kapandı**
> *(D-13 · koşul 2 · koşul 3 · F-4)*, biri **denetlendi** *(A-14)*.
> 🔴 **AMA BU BELGE HÂLÂ MÜHÜRLENMEDİ** — kalan kalemler:
> D-13 · B-57 · Li seviye 4 · `06` koşul 1 · koşul 2 · koşul 3 · A-14 · F-4.
> 📄 Tam kanıt envanteri: **`13-AILE0-KAPANIS-KANITI.md`**
>
> 🔴 **Bu belge okunmadan "Faz 0 geçti" denemez.** Aşağıdaki KAPSAMAZ
> tabloları ve **33** maddelik sınır listesi, kapının **neyi iddia
> etmediğini** söyler.

> 🔴 **BU BELGE, PROJENİN EN ÖNEMLİ TEK BELGESİ OLABİLİR.**
>
> Geçmiş projelerdeki hata örüntüsü şuydu: bir kapı geçilir, **neyi
> kapsamadığı hiçbir yerde yazılmaz**, kapsamadığı yol aylar sonra
> kullanılmaya başlanır, ve ortaya çıkan hata artık kapıya değil
> "sonradan eklenen şeye" atfedilir.
>
> Panzehir tek cümle: **bir kapı, "neyi KAPSAMIYOR" listesi yazılmadan
> kapanmaz.**

**Üretici komut:** `python dogrulama/aile0_kapi_raporu.py`

---

## Ç1 — KORUNUM

### ✅ KAPSAR

| | |
|---|---|
| Ölçek | **540 koşu** — 6 senaryo × 3 trafik × 30 ayarlama tohumu |
| Yol | **Gerçek MAC**: yeniden iletim, onay kaybı, kopya, kuyruk taşması, TTL |
| Düşme sebepleri | Dördü de **fiilen tetiklendi** *(üçü uç durum yapılandırmalarında)* |
| Uç durumlar | Kuyruk kapasitesi 1 · TTL 2 *(döngü yapan aktarıcı)* · **rota yok** *(ölü aktarıcı)* · yeniden deneme 0 |
| | ⚠️ 20 Ağustos'a kadar burada *"karıştırıcı +11 dBm (ağ bölünmüş)"* yazıyordu; kodda **öyle bir uç durum yok** (B-34). Dördüncüsü `rota_yok`tur |
| Doğrulama | **Mutasyonla** — üç ayrı bozma, üç ayrı dedektör |

### 🔴 KAPSAMAZ

| Kapsanmayan | Neden önemli |
|---|---|
| **"Hiçbir paket kaybolmuyor" DEMEZ** | Korunum denklemi **kayıp geçişi göremez**: bir `dus()` çağrısı silinince paket "uçuşta" asılı kalır ve eşitlik hâlâ tutar *(K-029)*. Kayıp geçişi yakalayan şey **boşaltma kontrolüdür** |
| 🔴 **Ana matris tek bir KÂHİN aktarıcıyla koşuldu** | 540 koşunun tamamı `en_kisa_yol` iledir ve o aktarıcı **açıkça kâhindir**. Saf gözlem aktarıcısıyla (`gurultuden_kacan`, 60 koşu) korunum yine 60/60 tutuyor **ama boruda kalan %0,031 → %0,531 (17 kat)** çıkıyor ve dört düşme sebebinin dördü de **doğal olarak** tetikleniyor. Ana matriste `kuyruk_tasmasi`, `ttl` ve `hedef_yok` **hiç koşulmamıştır**; Ç1.2'nin 4/4'ü tamamen 20 uç-durum koşusundan gelir |
| **Beacon çerçeveleri deftere girmez** | Defter **veri paketlerini** izler. Yayın çerçeveleri kontrol düzlemidir, ayrı sayılır. Bir beacon kaybolursa korunum bunu görmez — görmesi de gerekmez, ama bilinmeli |
| Ana deney tohumları | 2000–2029 aralığı **bilerek koşulmadı** *(K-025)* |
| Mobilite | Modellenmediği için sınanmadı |

---

## Ç2 — BELİRLENİMCİLİK

### ✅ KAPSAR
Tam koşu, 4 senaryo, **birebir** aynı sonuç sözlüğü · 3 farklı
`PYTHONHASHSEED` ayrı süreçlerde · iki farklı kol **tam koşuda** aynı kanal
gerçeklemesini görüyor.

### 🔴 KAPSAMAZ

| Kapsanmayan | Not |
|---|---|
| Farklı Python sürümü | Yalnızca 3.11.8'de sınandı |
| Farklı işletim sistemi | Yalnızca Windows'ta sınandı |
| Farklı donanım | Kayan nokta davranışı farklı bir CPU'da değişebilir |

> ⚠️ Sonuçlar başka bir makinede yeniden üretilecekse, önce `Ç2` testleri
> orada koşulmalıdır.

---

## Ç3 — ANALİTİK KONTROLLER

### ✅ KAPSAR
Termal gürültü *(kTB = −114 dBm)* · Friis yol kaybı *(1 m'de birebir)* ·
dekat başına 10α · menzil sınırında SINR **tanım gereği** eşik · türetilmiş
verici gücü *(15,5 dBm)* · türetilmiş girişim oranı *(β^(1/α))* · çerçeve
süreleri · tek atlama verimi *(932 vs analitik 933 kbps)* · **toplamsal
girişim** · **parça parça SINR = tek parça** · **darbeli ortalama güç koşan
sistemde, DÖRT görev çevriminde** · onay airtime'ı verimde görünüyor ·
**karıştırıcının alıcıda yarattığı güç, kapalı formla birebir**.

> 🔴 **BU LİSTENİN ÜÇ MADDESİ 19 AĞUSTOS'A KADAR HİÇBİR ŞEY ÖLÇMÜYORDU.**
> *Toplamsal girişim*, *parça parça SINR* ve *darbeli ortalama güç*
> iddiaları `pytest.approx(..., rel=…)` ile watt mertebesinde (~1e−14)
> karşılaştırma yapıyordu; aracın varsayılan **mutlak** toleransı (1e−12)
> her farkı yutuyordu. Üçü de **karşılaştırdıkları büyüklük ne olursa olsun
> geçiyordu** (B-22, K-037). Düzeltildi ve mutasyonla doğrulandı.
>
> ⚠️ *Karıştırıcı gücünün mutlak kontrolü* de yoktu: gücü 2 katına çıkaran
> bir mutasyon **216 testin 216'sından** sağ çıkıyordu (B-23).

### 🔴 KAPSAMAZ

| Kapsanmayan | Sonucu |
|---|---|
| Modülasyon/kodlama | DBPSK yaklaşımı; kodlama kazancı yok |
| Çoklu yol yayılımı | Yok — sönümleme modellenmiyor |
| Doppler | Yok |
| Anten yönlülüğü | İzotropik varsayım |
| Bit hataları | **Bağımsız** varsayılıyor; patlamalı hata yok. Gerçek kanallarda hatalar kümelenir ve aynı ortalama BER'de PER **daha düşük** olur |

---

## Ç4 — Lİ REPLİKASYONU

> ## 🔴 ÇALIŞMA NOKTASI — 27 Ağustos 2026'da BEYAN EDİLDİ (B-109)
>
> `v2/kaynak_doğrulama.txt` Li vd.'nin cümlesini birebir taşıyor:
> *"…they approach a utilization of 0.25 Mbps for 1500-byte packets, or
> **1/7 of the maximum of 1.7 Mbps**."*
>
> 🔴 **"1,7 Mbps" BİR ÇALIŞMA NOKTASIDIR:** 1500 baytta 1,7 Mbps tek atlama
> tavanı **2 Mbit/s'lik 802.11** demektir. Depo **1 Mbit/s**'te koşuyor
> *(`Konfig.bit_hizi_bps = 1e6`)* ve bu **hiçbir yerde yazılı değildi** —
> ne burada, ne Ç4.3'ün dört eksenli duyarlılık taramasında.
>
> 🟢 **VE ÖLÇÜM İYİ HABER VERDİ.** Li'nin kendi noktasında koşulduğunda araç
> **iki MUTLAK sayıyı da** üretiyor *(30 tohum × 2 uzunluk)*:
>
> | büyüklük | Li vd. | bu araç @ 2 Mbit/s | fark |
> |---|---|---|---|
> | tek atlama tavanı | **1,7 Mbps** | **1,761 Mbps** | **%3,6** |
> | uzun zincir verimi | **0,25 Mbps** | **0,277 Mbps** | **%10,8** |
> | plato oranı | 1/7 | 1/6,36 *(GA %1,54)* | %10 |
>
> **Depo bugüne kadar yalnızca ORANI karşılaştırdı**; iki mutlak sayının da
> tuttuğu hiç yazılmadı, yani replikasyon **olduğundan zayıf** sunuldu.
> 🔴 **ÜRETİCİ ÖLÜYDÜ, YENİDEN YAZILDI (B0.6 · F-4)** — `scratchpad/` yok.
> 🟢 **Dört sayının dördü de yeniden üretildi** *(30 tohum)*: 2 Mbit/s'te tek
> atlama **1,761 Mbps** *(+%3,6)* · uzun zincir **0,277 Mbps** *(+%10,8)* ·
> plato **1/6,36** *(GA %1,54)*; 1 Mbit/s'te **0,932 / 0,148 / 1/6,29**
> *(GA %2,04)*. Hiçbiri değişmedi.
> **Üretici:** `python dogrulama/li_calisma_noktasi.py`

### ✅ KAPSAR

| | Bizim @ 1 Mbit/s | Bizim @ 2 Mbit/s | Li vd. |
|---|---|---|---|
| Uzun zincir platosu | **1/6,29** *(GA %2,04)* | **1/6,36** *(GA %1,54)* | 1/7 |
| İdeal zincir bölgesi | **1/3,87** *(4 atlama)* | — | 1/4 |
| Tek atlama tavanı | 0,932 Mbps | **1,761 Mbps** | **1,7 Mbps** |
| Uzun zincir verimi | 0,148 Mbps | **0,277 Mbps** | **0,25 Mbps** |
| Nitel eğilim | ✅ Düşüş + plato | ✅ | ✅ |

Duyarlılık dört eksende tarandı; plato 1/5,7–1/12,6 bandında kaldı.
**Üç aday ölçümle elendi**: onay modellemesi *(açığın ~%30'u)*, yeniden
deneme sınırı *(%0,71, GA'lar örtüşüyor)* ve **bit hızı** *(%1,1 — B-110)*.

### 🔴 KAPSAMAZ

| Kapsanmayan | Not |
|---|---|
| **1/7 birebir üretilmedi** | Ölçülen 1/6,29 · gereken kayma **%10,2** |
| 🔴 **AÇIĞIN GEREKÇESİ SAĞLANMADI** | Aşağıya bak — adayların **ölçülmüş üst sınırları YETMİYOR** |
| **RTS/CTS** | Modellenmiyor. Analitik üst sınır **≤%7,71** *(1 Mbit/s)* |
| **EIFS** | Modellenmiyor. Üst sınır **≤%0,31** *(altıncı denetimin ölçümü; bu oturumda yeniden doğrulanmadı)* |
| **Bit hızı** | Ç4.3'ün dört ekseninden biri **değil**; replikasyonun kaynaktan 2 kat ayrıldığı tek eksen buydu |
| Topoloji çeşitliliği | Yalnızca **zincirde** doğrulandı. Izgara/rastgele topolojide kapasite doğrulanmadı |
| Li'nin diğer sonuçları | TCP davranışı, farklı paket boyutlarında kapasite eğrisinin tamamı replike edilmedi |

> ## 🔴 %10'LUK AÇIK — "ATFEDİLDİ"DEN "ÖLÇÜLDÜ VE YETMİYOR"A (B-110)
>
> `03` Bölüm D'nin şartı: *"birebir çakışma gerekmez; **nitel eğilimin aynı
> olması ve farkın GEREKÇELENDİRİLMESİ** yeterlidir."* Bu belge şimdiye
> kadar *"kalan fark modellenmeyen RTS/CTS ve EIFS'e **atfedilmektedir**"*
> diyordu. `03` B4: **bir kusuru ölçmek onu SEBEP yapmaz** — burada kusur
> **hiç ölçülmemişti.**
>
> **27 Ağustos 2026'da üç adayın da üst sınırı ölçüldü/hesaplandı:**
>
> | aday | üst sınır *(1 Mbit/s)* | yöntem |
> |---|---|---|
> | bit hızı | **%1,1** | 30 tohum × 2 uzunluk, ölçüm |
> | EIFS | ≤ **%0,31** | çözülemeyen alım oranı × `EIFS − DIFS` *(altıncı denetim)* |
> | RTS/CTS | ≤ **%7,71** | `cerceve_suresi_s(20) + cerceve_suresi_s(14) + 2·SIFS` / döngü |
> | **EN CÖMERT TOPLAM** | **≤ %9,1** | etkileşimsiz varsayılarak |
> | 🔴 **GEREKEN** | **%10,2** | |
>
> 🔴 **YETMİYOR.** Üstelik bu bir gerçek üst sınır bile değil: RTS/CTS'in
> **ikinci etkisi ters yönlüdür** *(gizli terminal çakışmalarını AZALTIR)*
> ve o etki **ölçülmedi**.
>
> ⚠️ **Payda tanımı yazılmalı:** RTS/CTS üst sınırı paydaya neyin girdiğine
> duyarlı. Geri çekilmesiz döngü *(8 768 µs)* **%7,71**, geri çekilmeli
> döngü *(12 866 µs)* **%4,99** verir. Üst sınır için cömert olan seçildi;
> ikisi de açığı kapatmıyor.
>
> ⚖️ **KARAR — `03` Bölüm D iki şart koyuyor:**
>
> | şart | durum |
> |---|---|
> | nitel eğilimin aynı olması | 🟢 **SAĞLANDI** *(düşüş + plato + 4 atlamada 1/3,87 ≈ Li'nin 1/4'ü)* |
> | farkın gerekçelendirilmesi | 🔴 **SAĞLANMADI** |
>
> Rapora giren cümle bunu taşımak zorunda. **Doğru cümle şudur:**
> *"Kalan %10'luk fark için üç aday ölçüldü; üçünün üst sınırları toplamı
> en cömert varsayımla bile açığı kapatmıyor. Fark bugün
> **AÇIKLANAMAMIŞTIR**."* — *"atfedilmektedir"* de artık yetmez, çünkü
> atfedilen şey **ölçüldü ve yetmedi**.
>
> 🟢 Bu bir kayıp değil: `03` Bölüm D'nin kendi cümlesi — *"bir replikasyon
> ilk denemede başarısız olursa bu raporun en güçlü bölümlerinden biri
> olabilir, **eğer sebebi bulunup yazılırsa**"*. Sebep bulunamadı; **arama
> ve sonucu** yazıldı.
---

## Ç5 — GÖZLEM SÖZLEŞMESİ

### ✅ KAPSAR
Yüzey izinli listeyle **birebir** · özyinelemeli tarama yasak tiplere
ulaşamıyor · tarama **mutasyonla** doğrulandı · t=0'da komşu tablosu **boş** ·
komşuluk menzil tablosundan **türetilmiyor** *(hem iç tabloda hem
**protokolün gördüğü yüzeyde**)* · saat senkronu yok *(paket doğum
zamanı görünmüyor)* · karıştırma altında beacon kayboluyor · bayt
sayaçları **düğümün kendi** sayaçları.

> ⚠️ *"Komşuluk menzilden türetilmiyor"* testi 19 Ağustos'a kadar **yanlış
> nesneyi** denetliyordu: protokolün gördüğü `Gozlem.komsular` yerine iç
> tabloya bakıyordu ve ilgili mutasyonu hiç kırmıyordu (K-037).

> 🔴 **Ç5 bugün 55 test.** ⚠️ *(27 Ağu — B-114: burada **18** yazıyordu;
> ara değerler 39 · 47 · 52'ydi. Kapının beklediği sayı `KAPI_SECIMLERI`de
> tek kaynakta ve `test_kapi_secimleri.py` onu 17 saniyede sınıyor.)*
> Eski hâliyle: 20 Ağustos'a kadar kapı **14** bekliyordu ve
> B-27b'nin dört içerik testi eklendiğinde bu sayı güncellenmedi; kapı
> `!!SEÇİM 18≠14` ile düştü *(K-046)*. Sayı düzeltildi, **tek kaynağa**
> taşındı ve `tests/test_kapi_secimleri.py` ile her suite koşusunda
> denetleniyor.

### 🔴 KAPSAMAZ

| Kapsanmayan | Neden önemli |
|---|---|
| **Gerçek protokolle sınanmadı** | Sözleşme yalnızca doğrulama aktarıcılarıyla test edildi. Aile 1'in protokolleri yazıldığında **yeniden** sınanmalı |
| **Dil düzeyinde mutlak değil** | Python'da bir protokol modül seviyesinde global duruma erişip kâhinlik yapabilir. Koruma **yapısaldır ve denetlenebilirdir**, ama zorlayıcı değildir. ⚠️ 20 Ağustos'a kadar burada **ikinci ve çok daha ucuz** bir kanal vardı: `protokol_fabrikasi` koşu başına **tek bir çağrılabilir** üretiyor ve 40 düğümün hepsi onu kullanıyordu — bir protokol kendi kapanışında düğümler arası bilgi taşıyabilirdi. Üçüncü denetim işaretledi *(A-4)*; **kapatıldı**: her düğüm kendi protokol örneğini alıyor ve `test_a4_her_dugum_KENDI_protokol_ornegini_aliyor` bunu mutasyonla doğruluyor. 🔴 **21 Ağustos'ta DÜZELTİLDİ (B-69):** *"kalan kanal yalnızca modül global'leridir"* beyanı **YANLIŞTI** ve riski olduğundan dar gösteriyordu. Dördüncü bağımsız denetim ölçtü: fabrikayı **saran bir kapsamda** yaratılan durum ne modül globalidir ne örneğe aittir — ve 40 örneğin hepsi onu paylaşır *(ölçüldü: 14 düğümün kendi anteninde ölçtüğü gürültü paylaşılan bir sözlükte biriktir ve komşu seçimi oradan yapıldı)*. Doğrusu: **kalan kanal, protokol nesnelerinin PAYLAŞTIĞI her yazılabilir durumdur** — modül global'i · fabrikayı saran kapsam · sınıf özniteliği · fabrikanın kendi `__dict__`i. `test_b69_…` artık örnekler arası paylaşımı **kapanış hücrelerinden** ölçüyor |
| Kontrol yükü eşitliği | Beacon aralığı eşit; ama farklı protokoller farklı beacon **içeriği** taşırsa bayt eşitliği ayrıca kontrol edilmeli |

---

## Ç6 — KOD DENETİMİ

### ✅ KAPSAR

**Gerçek değişmez (TEST):** kanal dilimi marjı — `test_rng.py -k test_dilim_`

**Kaynak denetimi (grep):** onay gerçek iletim · `Iletim` **kimlikle**
karşılaştırılıyor · `skeleton.py` **silindi** · geri çağrı adı yazım hatası
`__setattr__` ile yakalanıyor.

> 🔴 Ç6.2 19 Ağustos'a kadar *"marj **değişmezi**"* diye etiketlenmiş bir
> **dizgi aramasıydı** ve ölçtüğünü iddia ettiği şeyle **ters**
> korelasyonluydu: `0.0001` yazılsa (davranış birebir aynı) GEÇMEZ,
> zamanlama bozulup marj kaybolsa GEÇERDİ (B-09, K-040).
>
> ⚠️ Ç6.1/6.3/6.4 artık **"kaynak denetimi"** diye adlandırılıyor. Bir grep
> meşrudur; *"değişmez"* diye etiketlenmesi değildir.

### 🔴 KAPSAMAZ
Statik tip kontrolü *(mypy)* koşulmadı · kod kapsamı ölçülmedi — **ve
ölçülmesi de doğruluk kanıtı olmazdı** · üçüncü parti bağımlılık denetimi yok
*(yalnızca stdlib + numpy/scipy)*.

---

# BU ARAÇ NELERİ YAPMAZ

**Sonuçlar bu sınırlar içinde okunmalıdır.**

> **Madde sayısı: 37** — ölçüldü, elle sayılmadı. Numaralar **1–37**,
> boşluk ve tekrar yok.
> ⚠️ **2 Eylül 2026'da 33 → 37** *(B-132 · B-133 · B-134 · B-140,
> yedinci bağımsız denetim)*. Dördü de **beyandır**, davranış
> değişikliği değil — biri hariç: **madde 35** bir davranış
> değişikliğini *(K-088 kararı)* taşıyor ve etkisi aşağıdaki
> tabloda yazılı.
> ⚠️ **27 Ağustos 2026'da 25 → 30 düzeltildi (B-114).** Liste 26 Ağustos'ta
> beş madde büyümüştü *(B-83 · B-87 · B-91 · B-93 · A-10)*; bu satır
> güncellenmemişti. Belgenin KENDİ üretici komutu o gün `30 True` veriyordu
> ve kimse koşturmamıştı — `03` kural 1'in tam tarifi.
>
> **Üretici** *(depo kökünden)*:
> ```bash
> python -c "import re,pathlib; t=pathlib.Path('v2/08-AILE0-KAPSAM.md').read_text(encoding='utf-8'); g=re.split(r'(?m)^# BU ARAÇ NELERİ YAPMAZ$', t)[1]; g=re.split(r'(?m)^# ', g)[0]; n=sorted(int(m) for m in re.findall(r'(?m)^\|\s*\*{0,2}(\d+)\*{0,2}\s*\|', g)); print(len(n), n==list(range(1, len(n)+1)))"
> ```
> Beklenen çıktı: `37 True`
>
> ⚠️ **İki tuzak, ikisi de yaşandı:**
>
> 1. Desen **kalın numaraları da** saymak zorunda — 1–11 `| 1 |`, 12–25
>    `| **12** |` biçiminde yazılmış. Yalnızca ilkini arayan tarama **11**
>    der ve sessizce yanlış olur.
> 2. 🔴 Başlık **satır başına sabitlenmek** zorunda. İlk yazılan sürüm
>    `t.split('# BU ARAÇ...')` kullanıyordu ve **komutun kendi metnindeki**
>    başlık kopyasını yakalayıp **0** döndürdü — `B-68`in birebir ikizi.
>    Yakalandı çünkü komut, belgeye yazıldıktan **sonra belgeden çıkarılıp
>    koşuldu.**

> ⚠️ **Liste 26 Ağustos 2026'da 25 → 30 maddeye çıktı** *(B-83: beacon yükündeki `float` tek duyarlığa kırpılır · B-87: `teshis` sözleşmesi)*; madde **24 ve 25 aynı gün DÜZELTİLDİ** *(B-81 · B-80 — ikisi de B-66 öncesi modeli beyan ediyordu)*.
>
> ⚠️ **Liste 25 Ağustos 2026'da 24 → 25 maddeye çıktı** *(B-77: kontrol
> düzlemi bütçesi kollar arasında sınırsız farklılaşabilir)* — **dördüncü**
> bağımsız denetim. Ölçüldü *(26 Ağu, B-80)*: mesafe-vektörü kolu **%13,71–33,25**, gözlem kolu
> **%1,65–1,87** *(K-056)*.
> ⚠️ **Liste 21 Ağustos 2026'da 22 → 24 maddeye çıktı** *(B-55: beacon bayt maliyeti içeriğe duyarsız · yük tel biçiminde dolgu yok)*.
> ⚠️ **Liste 20 Ağustos 2026'da 16 → 22 maddeye çıktı.** İkinci bağımsız
> denetim, kodda modellenmemiş ama listede olmayan **dört** sınır buldu
> *(2B geometri · tek/merkezî karıştırıcı · enerji · kuyruk disiplini)*,
> artı yazılmamış istatistik katmanı ve tüketicisiz gözlem alanları.
> `08`in kendi kuralı: *"bir kapı, 'neyi KAPSAMIYOR' listesi yazılmadan
> kapanmaz."*

| # | Yapılmayan | Etkinin yönü |
|---|---|---|
| 1 | **Gölgeleme / sönümleme** | Bağ geçişleri gerçeğe göre **keskin**. Tazelik gerektiren yaklaşımların kazancını **azaltır** *(bizim hipotezimizin aleyhine)*. 🆕 *31 Ağu 2026:* literatürün log-mesafe modeli **X_σ gölgeleme terimi içeriyor** — K-077 |
| 2 | **RTS/CTS** | Gizli terminal çakışmaları gerçeğe göre **fazla** |
| 3 | **EIFS** | Çözülemeyen çerçeve sonrası bekleme yok |
| 4 | **Tepkisel karıştırıcı** | Yalnızca geniş bantlı gürültü |
| 5 | 🔴 **Karıştırıcı taşıyıcı dinlemeyi tetiklemez** | Karıştırmayı gerçeğe göre **hafifletir**: gerçekte güçlü bir karıştırıcı düğümleri hiç konuşturmaz |
| 6 | ~~**OLSR** — MPR seçimi kapsam dışı~~ | 🔄 **1 Eyl 2026'da KALDIRILDI:** OLSR artık Faz 1'in rakiplerinden biri ve **MPR seçimiyle birlikte** kurulacak *(`06` §4.2)*. Madde numarası korunuyor |
| **33** | 🆕 **GPSR modellenmiyor** *(1 Eyl 2026)* | Kapsam dışı: konum `05` §B gereği beacon'a konup **bayt ödenmeli**; ve asıl zafiyeti **GPS spoofing** zaten `01` §5.1'de kapsam dışı |
| 7 | **Mobilite** | Sabit topoloji — karıştırmayı izole etmek için bilinçli. 🔴 🆕 *31 Ağu 2026:* literatürde **3B Gauss-Markov mobilite standart**, ve *"3B mobilite + jamming bir arada"* boşluğu **bunu şart koşuyor** — 17. maddeyle **birlikte** okunur, karar öğrencinin *(K-077 §3, Boşluk B)* |
| 8 | **Patlamalı bit hatası** | Bağımsız varsayım; PER'i gerçeğe göre **yüksek** gösterir |
| 9 | **Frekans çevikliği** | Tek kanal. SPIDERMAN'in çözdüğü şey modellenmiyor |
| 10 | **Çok radyolu / tam çift yönlü düğüm** | Tek radyo, yarı çift yönlü |
| 11 | **Kopya önbelleği sınırı** | Sınırsız; gerçek 802.11 küçük pencere tutar |
| **12** | 🆕 **Alıcı kilidi (preamble capture)** — alıcının "şu an bir çerçeveye kilitli" durumu yok; zamanda çakışan iki çerçeveyi de başarıyla alabiliyor | Modeli gerçeğe göre **iyimser** yapar. **Ölçüldü: %0,028** *(S2/yoğun, 106 694 başarılı alımda 30 çakışan çift)* |
| **13** | 🆕 **Saat kayması/sapması (clock offset & drift)** — kodda **tek küresel saat** var; *"düğümler senkron değil"* yalnızca **disiplinle** sağlanıyor, yapısal değil | Bugün sızıntı yok *(hiçbir çerçeve zaman damgası taşımıyor)*. Ama `05` §A2 protokollere "başlığa alan koyup bedelini ödeyerek" bilgi taşıma hakkı veriyor: **bir protokol beacon'a zaman damgası koyarsa bedava ve kusursuz zaman senkronu kazanır** ve hiçbir test bunu görmez |
| **14** | 🆕 **Sanal taşıyıcı dinleme (NAV / süre alanı)** — RTS/CTS ayrı madde, ama 802.11 **veri** çerçevelerinin NAV kurması da modellenmiyor | Çakışmaları gerçeğe göre **fazla** gösterir *(2 numaralı maddeyle aynı yön)* |
| **15** | 🆕 **S0 kontrol kolunun tabanı %100 DEĞİL** | Ölçüldü *(90 koşu)*: ortalama **0,9938**, aralık **[0,8996 · 1,0000]**, std 0,0122; yalnızca **21/90** koşu tam %100. Kaynak: menzil sınırındaki PER *(1024 B için %16,97)* ve MAC çakışmaları — ikisi de topolojiden ve karıştırmadan **bağımsız**. 🔴 Aile 1'de *"S0'a göre kayıp"* hesaplanacaksa **bu taban raporlanmalıdır**; yoksa küçük etkiler taban gürültüsüyle karışır |
| **16** | 🆕 **Gecikmede seçilim yanlılığı — ŞEMA DÜZELTİLDİ, yanlılık DURUYOR** | Gecikme yalnızca **teslim edilenden** ölçülür. Ölçüldü: PDR 0,99 → 0,50 inerken gecikme yalnızca **+%2** artıyor. **Sonuç şeması artık paket bazlı teslim bilgisi taşıyor** *(`teslim_kimlikleri`, `teslim_gecikmeleri_s`)* ve `sim/karsilastirma.py` ortak alt küme karşılaştırması yapıyor. 🔴 **Ham gecikme farkı yine de yanlıdır:** S0↔S2 karşılaştırmasında ham fark +15,45 ms, ortak alt küme farkı +10,14 ms — ham sayı **1,52 kat abartıyor**. Rapora giren her gecikme karşılaştırması **kesişim oranıyla birlikte** yazılır |

| **17** | 🆕 **Geometri İKİ BOYUTLU** — düğümler tek düzlemde, irtifa yok | Bir **İHA** ağı için irtifa bir serbestlik derecesidir. Düzlemde karıştırıcıya uzaklık yalnızca yatay; irtifa farkı hem bağ geometrisini hem karıştırıcının aydınlatma desenini değiştirir. Model gerçeğe göre **basit**. 🔴 🆕 *31 Ağu 2026:* literatürde **3B geometri standart**; 7. maddeyle birlikte *Boşluk B*'yi kapatıyor. 🔴 🆕 *1 Eyl 2026:* literatür **2B mobilite modelini bir YAYGIN HATA** olarak listeliyor *(`Baseline…md` §12)* — beyan doğru ama **çerçeve değişti**: nötr bir tercih değil, adlandırılmış bir hata. 🔒 Öğrenci kararı: **gelecek çalışma** *(K-079)*. 🟢 **Ama *Boşluk A* (SJR↔PDR/E2E) bunu İSTEMİYOR** — `sim/topology.py` bugünkü hâliyle o boşluğu hedefleyebilir *(K-077 §3)* |
| **18** | 🆕 **TEK karıştırıcı** — çoklu ya da grup karıştırma yok. ⚠️ **1 Eyl 2026: KONUM ARTIK BİR EKSEN** *(J-merkez · J-kenar · J-hedef — `06` §2.1)*; eski *herzaman-merkezde* beyanı **kalktı**, kod maliyeti sıfır *(`karistirici_konum` zaten `Konfig` alanı)*. 🔴 Çoklu karıştırıcı hâlâ **yok** | 🔴 **İyimser VE hipotezin lehine.** Tek merkezî karıştırıcı, etrafından dolaşılabilir **simetrik bir zehirli bölge** üretir. H1.1'in mekanizması *(yarı ölü bağdan kaçmak)* tam olarak "kaçacak yer olmasına" dayanıyor; çoklu ya da kenar karıştırıcıda o yer kalmayabilir. **Bu, sonucu bizim lehimize çevirebilecek en büyük tek modelleme sınırıdır** |
| **19** | 🆕 **Enerji / pil kısıtı modellenmiyor** | `03` kural 9 SWaP kısıtını gerçek sayıyor; araç enerji maliyeti ölçmüyor. Kontrol düzlemi bütçesi yalnızca **bayt** ve **airtime** cinsinden |
| **20** | 🆕 **Kuyruk tek sınıf, önceliksiz FIFO** | Trafik sınıfı ayrımı yok; gecikme dağılımı kuyruk disiplinine duyarlıdır *(FIFO→LIFO mutasyonu iki testi kırıyor, yani etki büyük)* |
| **21** | 🆕 **İSTATİSTİKSEL TEST KATMANI YAZILMADI** — Wilcoxon · Holm–Bonferroni · güç analizi · NaN koruması | `06` Bölüm 3 planı henüz **koda dönmedi**: `wilcoxon`, `holm`, `scipy` deponun hiçbir yerinde geçmiyor. Ön-kaydın *"ZORUNLU"* dediği NaN kontrolü ve *"gerçek örneklem boyutuyla"* regresyon testi yok. 🔴 **Aile 1'in ilk sonucundan önce yazılmalı**; güç analizi 26 Eylül mührüne bağlı. 🟢 🆕 *31 Ağu 2026:* `v2/yeni_detaylı_arastırma/02_proje/Yöntem Ön-Kayıt Tohum ve Eşleştirilmiş Testler.md` bu katmanın **nasıl olması gerektiğini** anlatıyor ve `06`nın yöntemini doğruluyor *(K-077)* |
| **22** | 🆕 **Gözlem penceresinin ON DÖRT alanı HİÇ OKUNMUYOR** — `Gozlem` **9** *(`saat_s` · `olculen_gurultu_w` · `kanal_mesgul_mu` · `kuyruk_uzunlugu` · `kuyruk_kapasitesi` · `son_iletim_sonucu` · `son_iletim_hedefi` · `gonderilen_bayt` · `alinan_bayt`)* · `KomsuKaydi` **1** *(`bildirdigi_kuyruk`)* · 🔴 `PaketGorunumu` **4** *(`atlama_sayisi` · `bayt` · `kaynak` · `ttl`)* — **Üretici:** `python dogrulama/gozlem_tuketim.py` *(5 kol × 4 yapılandırma = 20 tam koşu)* | ⚠️ **27 Ağustos 2026'da 9 → 14 VE YÖNTEM DEĞİŞTİ (B-102 · D-12).** Önceki üretici DÜZYAZIYDI *("`g.<alan>` deseni taraması")* ve yeniden üretilemiyordu: üç farklı statik okuyuş **8 · 9 · 11** verdi, hiçbiri doğru değildi. Sebep yapısal — `PaketGorunumu.bayt` ile gerçek `Paket.bayt`, `Gozlem.kuyruk_kapasitesi` ile `Konfig.kuyruk_kapasitesi` **aynı adı taşıyor**; isimden tüketici çıkarmak bir TAHMİNDİR *(`03` kural 1)*. Ölçüt artık **çalışma anı**: üç sınıfın `__getattribute__`i sarmalanıp hangi alanın OKUNDUĞU kaydediliyor. ⚖️ **Altıncı denetimin bir iddiası ÇÜRÜDÜ:** B-102 `duyulan_beacon`ı da tüketicisiz saymıştı — çalışma anında OKUNUYOR *(`onceki.duyulan_beacon + 1`)*. 🔴 **Ve ikisinin de kaçırdığı boşluk çıktı (D-12):** `PaketGorunumu`nun beş alanından **dördü** taşınıyor ama hiç okunmuyor; ne `08` ne denetim anıyordu. ⚠️ **21 Ağustos'ta 4 → 9 düzeltilmişti (B-53)** — sayı o gün de elle yazılmış ve eksikti. 🔴 **KAPSAMI (Y11):** ölçüm yalnızca **koşulan** yolları görür. Aile 1'in protokolleri bu alanları okumaya başlayınca sayı DÜŞER — amaç budur. `05` bunlardan birine *"⭐ EN ÖNEMLİ ALAN"* diyor *(`son_iletim_sonucu`)* ve B-02 tam onun için yazıldı — ama okuyan kimse yok | Faz 0'ın doğrulama aktarıcılarının hiçbiri onları okumuyor. ⚠️ **İÇERİK testleri 20 Ağustos'ta yazıldı** (B-27b): her alanın değeri bağımsız hesapla karşılaştırılıyor, yani ilk okuyan protokol **doğrulanmış** bir sayı alacak. 🔴 Ama bu güvence `PaketGorunumu`nun dört alanı için **hiç sınanmadı** (D-12). *"Gerçek bir protokolle sınandı"* hâlâ **denemez**. 🟢 🆕 *31 Ağu 2026:* literatür bu alanların **ne işe yarayacağını söylüyor** — jamming-farkındalıklı yönlendirme, `son_iletim_sonucu`ndan **ACK/NACK → PER tahmini** ve `olculen_gurultu_w`den **girişim dinleme → SINR tahmini** yapıyor. 🔴 **Beyan değişmiyor, gerekçesi değişiyor:** okunmayan alan hâlâ okunmayan alandır — ama **ölü ağırlık değil, Aile 3'ün sensör takımıdır** *(K-077 §4)* |
| **23** | 🆕 **Simülatörün KENDİ beacon alanlarının bayt maliyeti içeriğe DUYARSIZ** — `kon.beacon_bayt` sabittir; `gurultu_w`/`kuyruk`/`konum` alanları eklense de çıkarılsa da kontrol yükü değişmez *(B-55)* | Modeli gerçeğe göre **basit** yapar. ⚠️ **Protokolün KENDİ koyduğu alanlar bu maddenin DIŞINDADIR**: `beacon_yuku` kancasıyla eklenen her alan gerçek serileştirme boyutundan hesaplanıp `kontrol_bayt` ve `kontrol_airtime_s`e yazılır *(B-47, K-049)*. Yani `05` §A2 kural 1 **protokol alanları için zorlanır**, simülatörün sabit alanları için zorlanmaz |
| **24** | 🆕 **Yük tel biçiminde hizalama/dolgu yok; İŞARET BEDELSİZDİR** — alan kimliği **UTF-8 bayt uzunluğu** · bool **1 B** · `int` **max(1, ⌈bit_length/8⌉)** *(BÜYÜKLÜK; işaret sayılmaz)* · `float` **4 B (tek duyarlık)** · sayı demeti **elemanların toplamı** | ⚠️ **26 Ağustos 2026'da DÜZELTİLDİ (B-81).** Önceki beyan *("alan kimliği 1 B · int/float 4 B · demet 4 B × eleman")* **B-66 ÖNCESİ** biçimdi: dört hükmünün **üçü yanlıştı** ve yön iddiası **tersti**. 🔴 Ölçülen yön **eksene göre değişir**: *(a)* alan adı ekseninde maliyeti gerçeğe göre **FAZLA** gösterir — gerçek bir uygulama 1 baytlık **kimlik tablosu** kullanırdı, burada tablonun varlığı doğrulanamadığı için adın kendisi faturalanır; *(b)* **işaret** ekseninde **AZ** gösterir — `−129` ile `129` aynı fiyatı öder *(sınır: ≤1 B, bu yüzden küçük)*. Hizalama/dolgu yok. **Üretici:** `python -c "import sys;sys.path.insert(0,'.');from sim.gozlem import yuk_bayt as y;print(y({'a'*10:1})-y({'a':1}), y({'x':2**8192})-1, y({'t':(1,2,3)})-1, y({'f':1.5})-1, y({'x':-129})-y({'x':129}))"` → `9 1025 3 4 0` |

| **25** | 🆕 **Kontrol düzlemi bütçesi kollar arasında SINIRSIZ farklılaşabilir** — K-009'un *"eşit kontrol düzlemi bütçesi"* adalet şartını zorlayan hiçbir mekanizma yok *(B-77)* | 🔴 Ölçüldü *(3 tohum, kâhinsiz mesafe-vektörü kolu vs `gurultuden_kacan`)*: kontrol payı **%13,71–33,25** vs **%1,65–1,87** — **eşleştirilmiş oran 8,3–17,8 kat** *(aynı senaryo, aynı tohum)*. İki kol bu hâliyle karşılaştırılırsa fark, mekanizmadan değil **bütçeden** gelebilir. 🔒 **Aile 1'in ilk karşılaştırmasından önce** ya bir tavan konur ya da her karşılaştırma **kontrol payıyla birlikte** raporlanır. ⚠️ **26 Ağustos 2026'da YENİDEN ÖLÇÜLDÜ (B-80, Y14).** Önceki değer *(%14,9–35,6 · "14–20 kat")* **B-66 ÖNCESİ** maliyet modelinden geliyordu ve **aynı oturumun kendi düzeltmesi** onu bayatlatmıştı — üretici satırı olmasına rağmen. 🔴 Eski oran ayrıca **eşleştirilmemişti** *(bir kolun en küçüğü ile diğerinin en büyüğü farklı senaryolardan oranlanıyordu — `03` B2)*. 🔴 **1 Eylül SONRASI YENİDEN ÖLÇÜLDÜ (B0.4) — ESKİ SAYI ÜÇ TOHUMDANDI.** `03` kural 2 ≥30 tohum şart koşuyor; **8,3–17,8 kat** değeri **3 tohumdan** geliyordu. 30 tohumla *(2 senaryo × 30 tohum × 2 kol = 120 tam koşu)* ölçülen: | okuma | DV kolu | gözlem kolu | eşleştirilmiş oran | |---|---|---|---| | tüm koşu · bayt *(eski okuma)* | %7,80–65,04 | %1,65–2,10 | **4,3–38,1 kat** *(ortanca **13,1**)* | | 🔒 **pencere · bayt** *(md 31'in şartı)* | %7,15–62,88 | %1,61–2,02 | **4,0–38,0 kat** *(ortanca **12,6**)* | | **pencere · airtime** | %10,33–72,07 | %3,74–4,51 | **2,6–18,9 kat** *(ortanca **7,5**)* | 🔴 **Üç bulgu:** *(a)* gerçek açıklık ilan edilenden **çok daha geniş** — eski aralık üç tohumla dar görünüyordu; *(b)* **airtime bayttan DAHA DAR** oran veriyor, yani bayt okuması asimetriyi **abartıyor** ve gerçek kıt kaynak kanal zamanıdır; *(c)* 30 tohumda **2 dejenere hücre** çıktı *(DV, tohum 25)* — 3 tohumla görünmezdi *(D-11)*. ⚠️ **F-5:** `kontrol_payi()` **tüm koşu** baytını okuyordu; md 31 pencereyi şart koşuyor. Artık ikisi de ölçülüyor ve pencere okuması `sim/karsilastirma.py` içinden **tek kaynaktan** geliyor. ⚠️ **B-135 · F-12 (2 Eylül):** *ortanca* artık `statistics.median` *(önceden `sorted[n//2]` — çift n'de ÜST ORTA)*; aynı veriden iki araç iki ortanca bastığı için fark edildi. 🔒 **Koşul 3'ün BAĞLAYICI çifti bu çifttir** *(DV ↔ gözlem)*; `dogrulama/gecerlilik.py` de artık aynı çifti ölçüyor ve **aynı aralığı** veriyor. 🔴 **B-153 (sekizinci denetim) — AYNI ADIN İKİ YÜKLEMİ VARDI:** `kontrol_payi.py` **`a / b`** *(YÖNLÜ, < 1 olabilir)*, `gecerlilik.py` **`max/min`** *(YÖNSÜZ, ≥ 1)*. Bugün **58/58 hücrede aynı çıkıyorlar — çünkü DV her hücrede gözlemden büyük**, yani çakışma **verinin bir özelliğidir, yüklemin değil**. Bir Faz 1 kolu gözlem kolundan **az** kontrol baytı üretir üretmez *(sessiz senaryoda reaktif AODV bunun doğal adayıdır)* iki araç iki farklı sayı basar. 🔒 `gecerlilik.py` artık **ikisini de** basıyor, **yön değişimini sayıyor** *(bugün 0/58)* ve ayrıştıklarında bağırıyor. **Üretici:** `python dogrulama/kontrol_payi.py` *(120 tam koşu, **12,9 dk** ölçüldü; tohum 1–30)* |

| **26** | 🆕 **Beacon yükündeki `float` TEK DUYARLIĞA KIRPILIR** — gözlem penceresine 4 baytın taşıyabildiği değer girer, çift duyarlıklı hâli değil; tek duyarlığa **sığmayan** bir değer *(|v| > ~3,4e38)* taşınamaz, `YukHatasi` ile reddedilir | ⚠️ **26 Ağustos 2026'da EKLENDİ (B-83).** Önceden `float` **4 bayta** faturalanıyor ama pencereye **8 bayt (çift duyarlık) hâliyle kırpılmadan** giriyordu: ölçüldü — 8 keyfi bayt bir `float`a konup **birebir** geri okundu, **2,00× kaçak**. Aynı 8 bayt `int` olarak 8 bayt öderken `float` olarak 4 ödüyordu, yani K-009'un *"eşit kontrol düzlemi bütçesi"* şartı **kodlamaya bağımlıydı**. 🔴 Kalan modelleme sınırı: kırpma **sessiz bir hassasiyet kaybıdır** — `1/3` pencereye `0.3333333432674408` olarak ulaşır. Yön: bu, gerçek bir telemetri başlığının **yaptığı** şeydir; model burada gerçeğe **yaklaşır**, uzaklaşmaz. **Üretici:** `python -m pytest tests/test_gozlem.py -q -k "b82 or b83"` *(6 test)* |

| **27** | 🆕 **`protokol.teshis(dugum)` sözleşmesi ELLE TUTULAN sınırlar taşır** — ad ≤ 64 B · dizgi değer ≤ 256 B · düğüm başına ≤ 32 alan · dizi ≤ 64 eleman; izinli tipler `bool · int · float · str` ve bunların **düz** dizisi *(iç içe dizi yok)*; **sonlu olmayan sayı yasak** | ⚠️ **26 Ağustos 2026'da EKLENDİ (B-87).** Öncesinde kancanın **hiçbir sözleşmesi yoktu**: beşinci denetim 8 sözleşme dışı yük denedi, **8'i de kabul edildi**, **4'ü** sonuç yazıcısını **koşu bittikten SONRA** ham `TypeError`/`ValueError` ile düşürdü *(o noktada koşu harcanmıştır)*, biri **`YASAK_TIPLER`den bir `Konfig`** taşıdı. Kardeşi `beacon_yuku` **anında** ve **tipli** reddediyordu; *"birebir aynı desen"* iddiası yanlıştı. 🔴 **Sınırın sınırı:** dört sayı **elle** seçildi ve ölçümden türetilmedi — bugün hiçbir kol onlara yaklaşmıyor, ama bir Aile 1 kolu 32 alandan fazlasına ihtiyaç duyarsa sözleşme **yeniden ölçülmeden** gevşetilemez. Sözleşme teşhisin **anlamlı** olduğunu da denetlemez; yalnızca **taşınabilir** olduğunu. **Üretici:** `python -m pytest tests/test_gozlem.py -q -k b87` *(2 test)* |

| **28** | 🆕 **Yayılma gecikmesi modellenmiyor** — bir çerçeve gönderende bittiği anda alıcıda da bitmiş sayılır | ⚠️ **26 Ağustos 2026'da EKLENDİ (B-91).** 🔴 Bu maddeyi **dördüncü denetim önermişti** *(§7, madde 25)* ve `08`e **hiç girmedi**; elenmesi de kayda geçmedi. Beşinci denetim bunu bulgu olarak açtı. Ölçülen büyüklük *(dördüncü denetimin ölçümü; bağımsız olarak yeniden ölçülmedi)*: **280 m'de 0,93 µs**, girişim menzilinde **2,01 µs** — `cca_s = 4 µs`in **%23–50'si**. Yön: çarpışma zamanlamasını gerçeğe göre **keskinleştirir** *(iki düğüm birbirini olduğundan hızlı duyar)*. ⚠️ Bu, `08`e giren maddelerin **önerildiği yerden takip edilmediğinin** de kanıtıdır; K-056'nın *"NE ELENDİ"* tablosu bu öneriyi hiç anmamıştı |

| **29** | 🆕 **`sim/` içindeki SEKİZ değişmez `assert` ile yazılmıştır ve `python -O` altında SESSİZCE kalkar** — `events.py` *(olay zamanı geriye gitmez)* · `traffic.py` *(üretim ölçüm penceresini aşmaz)* · `kosucu.py` *(koşu bitişi · pencere üst sınırı)* · `mac.py` *(PER hesaplandı · alıcı kendi gücünü girişime eklemez · **BER doyma varsayımı, B-116**)* · `gozlem.py` *(**kırpılmamış float ölçüm yoluna ulaşmaz, B-112**)* | ⚠️ **26 Ağustos 2026'da EKLENDİ (B-93).** 🟢 **Bugün zararsız — ölçüldü:** `-O` ile ve `-O`suz tam sonuç sözlüğünün blake2b'si **aynı** *(`aecc804b06cfa177b8e1460b`)*; altısı da sağlam koşuda zaten tetiklenmiyor. 🔴 **Ama kalktıklarında dördü SESSİZ yanlış cevap verir:** olay zamanı geriye gider · pencere dışı paket ölçüme girer · koşu sonrası beacon görünmez · alıcı kendi gücünü girişime ekler. Biri `TypeError` ile **gürültülü** patlar. 🔒 **Her ölçüm koşusu `-O`SUZ yapılır.** ⚠️ Denetçi **beş** saymıştı; altıncısı B-98'in düzeltmesiyle eklendi *(pencere üst sınırı)*. ⚠️ **27 Ağustos 2026'da ALTI → SEKİZ:** B-116 ve B-112'nin ölü dalları `assert`e çevrildi *(ölçüldü: 540 021 çağrıda 0 · 149 212 float değerinde 0)*. 🔴 **SATIR NUMARALARI KALDIRILDI (D-7):** hiçbir test onları kilitlemiyordu ve `test_b93` satır tabanlıyken 35 mutasyonun **7'sinde bedava yakalama** üretiyordu. Beyan artık DOSYA ve DEĞİŞMEZİN KONUSU üzerinden; test `assert` **ifadesini** bağlıyor. **Üretici:** `python -m pytest tests/test_kapi_secimleri.py -q -k b93` |

| **30** | 🆕 **Mutant zaman aşımı, süreyi test SAYISIYLA DOĞRUSAL ölçekler — ama testler eşit maliyetli DEĞİLDİR** | ⚠️ **26 Ağustos 2026'da EKLENDİ (A-10).** Ölçüldü: en pahalı tek test **254,51 sn** *(`test_b65_mekanizma_kapisi_ESLESTIRILMIS_ablasyona_karsi`, 16 tam koşu)*, ortalama test **≈2,09–4,39 sn** — **58–122 kat.** ⚠️ **27 Ağustos 2026'da DÜZELTİLDİ (B-114).** Önceki sayı *(45,7 sn · 17,8 kat)* hem yanlış testi gösteriyordu hem bayattı; ölçüm `--durations` ile yapıldı. 🔴 Oran bandının GENİŞ olmasının sebebi ayrı bir bulgudur: makine koşudan koşuya **2,10 kat** oynuyor *(K-073 · K-074)*. `_gereken_zaman_asimi_s` bunu **görmez**: tek bir pahalı test eklemek, korumanın öngördüğünden çok daha fazla süre ekleyebilir. 🟡 **Bugün karşılanıyor** çünkü *(a)* emniyet payı **1,50**, *(b)* çekişme çarpanı ölçülen maksimumun üstünde **1,80**, *(c)* test başına maliyet **en kötü gözlenen** koşudan alınıyor *(K-067)*. 🔴 **Kalan risk:** paketin bileşimi ağırlaşırsa doğrusal model **iyimser** kalır. Bunu ancak `--durations` ile tam bir koşu ölçer; bugüne kadar ölçülmedi |

| **31** | 🆕 **Sonuç sözlüğü İKİ PENCERE birden raporlar — hangisinin okunacağı OKUYANIN sorumluluğudur** — teslim/gecikme/atlama `[isinma_s, olcum_bitis_s]`; **26 kümülatif sayacın hem TÜM KOŞU hâli hem `*_pencere` ikizi** taşınır | ⚠️ **27 Ağustos 2026'da EKLENDİ (B-105'in kapanışıyla birlikte).** Öncesinde yalnızca tüm koşu hâli vardı ve `03` sözleşme 4 *("tüm sayaçlar aynı pencereden")* **ihlal ediliyordu**. Ölçüldü *(5 kol × 8 yapılandırma = 40 tam koşu)*: kontrol baytının **%17,63–22,84'ü** ölçüm penceresi dışında üretiliyor ve **çarpıklık KOLA GÖRE değişiyor** *(`gurultuden_kacan`·`dongu_yapan` 1,004–1,047 · `hedefe_en_yakin`·`en_kisa_yol` 1,054–1,079)* — yani eşleştirilmiş bir kol karşılaştırması **yanlıdır**. 🔴 **Aile 1'in her karşılaştırması `*_pencere` alanlarını kullanmak zorundadır**; tüm koşu hâli teşhis içindir. ⚠️ `en_yuksek_doluluk` bir MAKSİMUMDUR ve farkla türetilemez — ayrı izlenir. 🔴 **ÜRETİCİ ÖLÜYDÜ, YENİDEN YAZILDI (B0.6 · F-4).** `scratchpad/` dizini depoda **yok**. Kayıp betiğin *"8 yapılandırma"*sının ne olduğu hiçbir belgede yazılı değil ve **uydurulmadı** *(K-053)*; matris açıkça yeniden ilan edildi: **5 kol × 2 senaryo × 3 trafik = 30 tam koşu**. ⚠️ **B0.7'DE İKİ KEZ DÜZELTİLDİ (B-120 · B-123, yedinci bağımsız denetim).** 🔴 B0 önce **tek tohumdan** ölçtü *(%18,17–22,86)* ve çıkan bandı bir *"analitik sınır"* sanıp bir `assert`e çevirdi; araç **tohum 4'te çöküyordu**. 🔒 **30 TOHUMLA YENİDEN ÖLÇÜLDÜ** *(~~5 kol~~ → **6 kol** × 2 senaryo × 3 trafik × 30 tohum = ~~900~~ → **1 080 tam koşu**, korunum **1 080/1 080**)*: | büyüklük | ölçülen | |---|---| | pencere dışı kontrol baytı | **%16,62 – %23,03** *(ortanca **%21,50**, **1 080** hücre · korunum 1 080/1 080)* | | çarpıklık *(tüm koşu / pencere)* | **1,1993 – 1,2993** | 🟢 İlan edilen **%17,63–22,84** bandıyla uyumlu; tek tohumluk band gerçek bandı **iki uçtan da dar** gösteriyordu. Ortanca kararlı *(%21,06 → %21,12)*. 🔴 **ÇARPIKLIK BANDI ANALİTİK DEĞİL, AMPİRİKTİR.** B0 *"1,004–1,079 bir tüm koşu/pencere oranı **olamaz**, o oran [1,1852 · 1,2963] bandına hapistir"* demişti; **bu yanlıştı** ve üç yoldan kırılıyor: *(a)* aracın kendi sayaçlarından üçü bandın dışında *(`beacon_gonderilen` 1,3398 üstten; `veri_bayt`/`mac_deneme` 1,1786 alttan)*, *(b)* `hedefe_en_yakin` **tohum 4'te** 1,2993 ile üst çapayı aşıyor *(30 tohumda yeniden doğrulandı)*, *(c)* `isinma_s` = 5/15/25'te çarpıklık 1,0144/1,0446/1,0766 **doğrudan üretiliyor**. 🔒 **Doğru ifade:** ilan edilmiş 1,004–1,079, **bugünkü çalışma noktasında üretilemiyor**; hangi çalışma noktasından geldiği **bilinmiyor** ve **uydurulmadı** *(K-053)*. 🟢 **TEK GERÇEKTEN ANALİTİK ÇAPA KORUNDU:** `olu` kolu hiç veri göndermez, yalnız beacon üretir ve oranı **1,2963 = 350/270**'e oturmak zorundadır — **180 hücrede en büyük sapma 0,000000**. Bu `assert` kalır; diğer kolları banda hapseden `assert` **gözleme** dönüştürüldü. 🔴 **B-168 (SEKİZİNCİ DENETİM) — BAĞLAYICI KOL BU MADDEDE YOKTU.**
B-135 `DV`yi *"koşul 3'ün **BAĞLAYICI** çifti"* ilan etti ve
`gecerlilik.py`ye ekledi; bu maddeyi üreten `pencere_kapsami.py`
**güncellenmedi**. Depoda **üç ayrı kol kaydı** vardı ve ikisi DV'yi
görmüyordu *(`AKTARICILAR` 5 · `gecerlilik.KOLLAR` 3 **DV var** ·
`pencere_kapsami.KOLLAR` 5 **DV yok**)*. Sonucu: **bağlayıcı ilan edilen
kolun pencere kapsamı hiç ölçülmemişti.**

🟢 **3 Eylül 2026'da ÖLÇÜLDÜ** *(1 080 tam koşu · korunum 1 080/1 080)*:

| kol | çarpıklık *(tüm koşu / pencere)* | pencere dışı % |
|---|---|---|
| `dongu_yapan` | 1,1993 – 1,2958 | %16,62 – %22,83 |
| `gurultuden_kacan` | 1,2129 – 1,2865 | %17,56 – %22,27 |
| `hedefe_en_yakin` | 1,2289 – **1,2993** | %18,63 – **%23,03** |
| `en_kisa_yol` | 1,2404 – 1,2958 | %19,38 – %22,83 |
| 🔒 **`DV`** *(bağlayıcı)* | **1,2653 – 1,2974** | **%20,97 – %22,92** |
| `olu` *(analitik çapa)* | **1,2963** *(sapma 0,000000, 180 hücre)* | %22,86 |

> ## 🔴 DV BANDIN ÜST UCUNDA — ve analitik üst çapayı AŞIYOR
> DV'nin alt sınırı **1,2653**, altı kolun **en yükseği**; üst sınırı
> **1,2974**, düzgün beacon beklentisi olan **1,2963'ün ÜSTÜNDE.**
> Yani DV kontrol baytını zamanda **düzgün üretmiyor** — ve DV, Faz 1'in
> **AODV'sine en yakın** koldur *(kontrol düzlemi ağır, kâhinsiz)*.
>
> ⚖️ **Bu bir hata değil, maddenin bağlayıcı cümlesinin kanıtıdır:**
> *"Aile 1'in her karşılaştırması `*_pencere` alanlarını kullanmak
> **zorundadır**."* En çok çarpıtan kolun, karşılaştırılacak kola en
> yakın olması bu şartı **zayıflatmıyor, güçlendiriyor**.
>
> 🔴 **Ve `08` md 31 bunu 2 Eylül'e kadar GÖREMİYORDU** — çünkü ölçen
> araçta o kol yoktu. **Üretici:** `python dogrulama/pencere_kapsami.py`
> *(1 080 koşu · tahmin bandı 8,7–18,3 dk · ölçülen ~13 dk)*.

🟢 **Bağlayıcı cümle AYAKTA:** çarpıklık kola göre değişiyor, dolayısıyla tüm koşu hâliyle yapılan eşleştirilmiş bir kol karşılaştırması **yanlıdır**. **Üretici:** `python dogrulama/pencere_kapsami.py` *(900 tam koşu, ~8–17 dk)* |

| **32** | 🆕 **Ön-kayıtlı H1.1 kapısının NULL MODELİ `Akislar` DIŞINDA bir rastgelelik kaynağı kullanır** — `dogrulama/aktaricilar.py::kalite_ablasyonu`, `random.Random((hash(anahtar) & 0xFFFFFFFF) ^ tuz)` | ⚠️ **27 Ağustos 2026'da EKLENDİ (B-103).** `07`nin akış tablosu *"bu liste kapalıdır"* diyor ve bu istisna **hiçbir belgede yazılı değildi**; yalnızca bir test docstring'inde geçiyordu. 🟢 **Bugün zararsız — üç ölçüm:** `hash()` **tamsayı demetinde** üç `PYTHONHASHSEED` değerinde birebir aynı · `tuz` XOR'u çekimleri bağımsız yapıyor *(200 000 anahtar × 5 çekim, 1/k! referansıyla ayırt edilemez)* · tohumlar arası anahtar örtüşmesi **%0,000**. 🔴 **KIRILGANLIK:** güvence anahtarın **tamsayı demeti** olmasına dayanır; bir gün **dizgi** taşırsa `PYTHONHASHSEED`e bağlanır. Zorlayan koruma: `test_c2_2_pythonhashseed_den_bagimsiz` *(B-94 ile ablasyon kolu da kapsamda)*. 🔴 **İkinci sınır:** ablasyon `k ≤ 3` olan kararlarda `m = 5`in çoğu çekimi çakışır; kapının yapılandırmasında bu kararların payı **%11,73**. Tam beyan: `07` §BEYAN EDİLMİŞ TEK İSTİSNA |

| **34** | 🆕 **ORTAK ALT KÜME OKUMASININ KESİŞİM ALT SINIRI YOKTUR** — `ortak_alt_kume` yalnızca `ortak_paket == 0`ı reddeder | ⚠️ **2 Eylül 2026'da EKLENDİ (B-140, yedinci denetim).** Ölçüldü *(30 tohum, S0→S2)*: kesişim `en_kisa_yol`da **%51,1** *(min %20,0)*, `DV`de **%25,6** *(min %6,0)*, `gurultuden_kacan`da **%20,7** *(min **%5,6**)*. 🔴 `03` B3'ün kendi mantığı: seçilim yanlılığı ortak alt kümede *"ortadan kalkmaz"*, **taşınır** — %5,6'lık bir kesişim, iki kolun da teslim edebildiği **en kolay** paketlerdir ve o alt kümede ölçülen fark **genellenemez**. 🔴 **Faz 1'de bağlayıcı olacak:** AODV ↔ OLSR teslim oranları ayrıştıkça kesişim daralır. 🔒 **Alt sınır UYDURULMADI** *(`03` kural 2: bir sabit ancak GA'dan türetilirse yazılabilir)*; **B4'te ölçülerek** konacak — kesişimi yapay olarak daraltıp gecikme farkının ne zaman kaymaya başladığı ölçülür. **Üretici:** `python dogrulama/gecerlilik.py` |

| **35** | 🆕 **KONTROL PAYI TANIMSIZKEN KARŞILAŞTIRMA YİNE ÜRETİLİR** — `kontrol_payi_yuzde` `None` döner, `ozet()` **"🔴TANIMSIZ(D-11)"** basar | ⚠️ **2 Eylül 2026'da EKLENDİ (B-134, yedinci denetim + K-088 kararı).** Önceki hâl tüm karşılaştırmayı `KarsilastirmaHatasi` ile düşürüyordu; ölçüldü: **801 ortak paket** üzerinden hesaplanmış, tamamen geçerli bir gecikme farkı *(+10,140 ms)* **gecikmeyle hiç ilgisi olmayan** bir payda yüzünden üretilemiyordu. 🔒 Gerekçe: `06` koşul 3 kontrol payının **RAPORLANMASINI** istiyor ve *"TANIMSIZ (D-11)"* bir rapordur; `03` B3 *"iki çakışmayan olgu tek metriğe sıkışırsa metriği **İKİYE AYIR**"* diyor. 🔴 **BEDELİ:** artık kontrol payı bilinmeyen bir gecikme farkı **üretilebilir** — okuyan, `ozet()`in TANIMSIZ etiketini görmek zorundadır. Ölçek: 120 hücrenin **2'si** dejenere *(DV, tohum 25)*. **Üretici:** `python dogrulama/kontrol_payi.py` |

| **36** | 🆕 **SONUÇ SATIRI KOŞUYU TANIMLAMAZ *(ve ARACI DA AYIRMAZ)*** — `kaynak_hash` **kod sürümünü** ayırır, **koşuyu ayırmaz**; ne zaman damgası ne koşu kimliği vardır. 🔴 **B-164 (sekizinci denetim) — MADDE GENİŞLETİLDİ:** `kaynak_hash` **yalnızca `sim/`i** kapsıyor *(`sim/results.py:39`)*; `dogrulama/` **araç sürümü hiçbir sonuç satırında taşınmıyor**, yani bir sayının hangi ANALİZ koduyla üretildiği yeniden kurulamıyor. Bu oturum onu birinci elden yaşadı: `sim/karsilastirma.py`ye tek **yorum** eklendi, hash `fc73905b…` → `01cedf62…` oldu ve `dogrulama/` hiç değişmemesine rağmen tüm çapa verisi *"bayat"* sayıldı. 🔒 İkisi de **B1.5'te** eklenir *(`12` §2.2)*: `kosu_kimligi` · `arac_hash`; şema orada **son kez** genişliyor | ⚠️ **2 Eylül 2026'da EKLENDİ (B-133, yedinci denetim).** Aynı kod sürümünde **iki kez** koşan bir araç `.jsonl`de **ayırt edilemez**; dosyalar `append` modunda büyür. Bugün ölçülen: `pencere_kapsami.jsonl` **üç koşu**, `gecerlilik.jsonl` **üç kod sürümü** taşıyor. 🟢 Bugün zararsız — araçlar `veri` sözlüğünü **kendi bellek içi koşularından** kuruyor, dosyayı okumuyorlar. 🔴 **Zarar, dosyayı SONRADAN okuyan her analizdedir ve Faz 1'de tam olarak öyle okunacak.** 🔒 **Şema alanıdır: B1.5'te eklenmezse bir daha eklenemez** — `12` §5.1'in B1.5 kontrol listesinde |

| **37** | 🆕 **`08` Ç4'ÜN SAYILARI SÖZLEŞME 5'İN DIŞINDADIR** — `dogrulama/li_zincir.py` `sim/kosucu.py::Kosu`yu **kullanmaz**; kendi MAC seviyesi doymuş-zincir düzeneğini kurar | ⚠️ **2 Eylül 2026'da EKLENDİ (B-132, yedinci denetim).** Sonucu: Li replikasyonunun dört sayısı *(1,761 / 0,277 Mbps · 1/6,36 · GA %1,54)* `kaynak_hash` taşıyan **hiçbir sonuç satırı bırakmaz** ve `03` Bölüm C **sözleşme 5**'in kapsamı dışındadır. 🟢 Bu bilinçlidir: Li düzeneği bir **protokol deneyi değil**, MAC fiziğinin analitik doğrulamasıdır *(zincir topolojisi, doymuş kaynak, yönlendirme yok)*. 🔴 **Ama beyan edilmesi gerekiyordu:** o dört sayı, üretildikleri kod durumunu **satır düzeyinde** taşımıyor — yalnızca üretici komutun o an koştuğu koda güvenilir. **Üretici:** `python dogrulama/li_calisma_noktasi.py` |

### Ayrıca — iki birimli kontrol yükü

Kontrol yükü **hem bayt hem airtime** cinsinden raporlanır
*(`kontrol_bayt` · `kontrol_airtime_s`)*. Ölçüldü: kontrol payı bayt
cinsinden **%2,84**, airtime cinsinden **%5,12** — **1,80 kat**. Sebep
önbelge: her çerçeveye sabit 192 µs ekleniyor, yani 14 baytlık bir onay
112 µs veri taşırken 192 µs önbelge harcıyor.

🔴 **Aynı baytı farklı sayıda çerçeveye bölen iki protokol, bayt
metriğinde eşit görünür ve airtime'da 2 kat farklı olur.** K-009'un
*"eşit kontrol düzlemi bütçesi"* adalet şartı bayt üzerinden kurulmuştu;
her iki birim raporlanmadan o şart doğrulanamaz.

---

# 🔴 BU LİSTEYE SONRADAN MADDE EKLENİRSE

Ekleme tarihi yazılır ve şu soru **ayrıca** sorulur:

> *"Bu maddenin eklendiği tarihten ÖNCE üretilmiş sonuçlar hâlâ geçerli mi?"*

Cevap "hayır" ise, o sonuçlar **yeniden koşulur** ya da **geçersiz işaretlenir**.
Sessizce bırakılmaz.

| Tarih | Eklenen madde | Önceki sonuçlar geçerli mi |
|---|---|---|
| **19 Ağu 2026** | 12 · Alıcı kilidi | ✅ **Evet.** Araç her zaman böyleydi; eklenen şey **beyandır**, davranış değil. Etkisi ölçüldü ve %0,03 |
| **19 Ağu 2026** | 13 · Saat kayması | ✅ **Evet** — bugüne kadar hiçbir çerçeve zaman damgası taşımadı. ⚠️ Aile 1'de bir protokol taşırsa **o kolun sonucu geçersizdir** |
| **19 Ağu 2026** | 14 · NAV | ✅ **Evet.** Beyan eksikliğiydi |
| **19 Ağu 2026** | 15 · S0 tabanı %100 değil | ⚠️ **Kısmen.** Hiçbir ölçüm geçersiz değil, ama `06-ON-KAYIT.md`nin *"teslim tavanı %100'dür"* cümlesi **yanlıştı ve düzeltildi**. S0'a göre normalize edilen gelecek sonuçlar bu tabanı yazmak zorunda |
| **19 Ağu 2026** | 16 · Gecikme ortak alt kümesi | 🔴 **HAYIR — şema değişti.** B-19 öncesi üretilmiş satırlar `teslim_kimlikleri` taşımaz ve **ortak alt küme karşılaştırmasını desteklemez**. `sim/karsilastirma.py` böyle bir satırı sessizce kabul etmez, `KarsilastirmaHatasi` fırlatır. Faz 0'ın tüm sayıları kapanış koşusunda zaten yeniden üretilecek |
| **20 Ağu 2026** | 17 · 2B geometri | ✅ **Evet.** Araç her zaman böyleydi; eklenen **beyandır** |
| **20 Ağu 2026** | 18 · tek/merkezî karıştırıcı | ✅ **Evet** — ama 🔴 **yorumu değiştirir:** H1.1 lehine bir sınır olduğu artık yazılı. Rapora giren cümle bu sınırı taşımak zorunda |
| **20 Ağu 2026** | 19 · enerji kısıtı | ✅ **Evet.** Beyan eksikliğiydi |
| **20 Ağu 2026** | 20 · kuyruk disiplini | ✅ **Evet.** Beyan eksikliğiydi |
| **20 Ağu 2026** | 21 · istatistik katmanı yok | ✅ **Evet** — Faz 0 sonucu üretmiyor. ⚠️ Aile 1'in ilk sonucundan önce yazılmalı |
| **20 Ağu 2026** | 22 · tüketicisiz gözlem alanları | ⚠️ **Kısmen.** İçerik testleri eklendi (B-27b); `kanal_mesgul_mu`→`False` ve `kuyruk_uzunlugu`→`0` mutasyonları **artık yakalanıyor** *(önceden 240/240 geçiyorlardı)* |
| **2 Eyl 2026** | 34 · kesişim alt sınırı yok | ✅ **Evet.** Beyan eksikliğiydi; `ortak_alt_kume` her zaman böyleydi ve kesişim oranı zaten raporlanıyordu |
| **2 Eyl 2026** | 35 · kontrol payı TANIMSIZ olabilir | 🔴 **DAVRANIŞ DEĞİŞTİ.** Önceden dejenere payda **tüm karşılaştırmayı** reddediyordu; şimdi karşılaştırma üretiliyor ve pay `None` dönüyor. ⚠️ **Önceki sonuçlar geçerli** — reddedilen bir karşılaştırma **sayı üretmemişti**, yani geriye dönük değişen bir sayı yok. 🔴 Bundan sonraki her karşılaştırma `ozet()`in TANIMSIZ etiketini taşımak zorunda |
| **2 Eyl 2026** | 36 · sonuç satırı koşuyu tanımlamıyor | ✅ **Evet.** Araç her zaman böyleydi; eklenen **beyandır**. 🔴 Ama **B1.5'te şema alanı eklenmezse** bir daha eklenemez |
| **2 Eyl 2026** | 37 · Ç4 sözleşme 5 dışında | ✅ **Evet.** `li_zincir` her zaman `Kosu` kullanmıyordu; eklenen **beyandır** |
| **19 Ağu 2026** | Ç1 · kâhin aktarıcı notu | ⚠️ **Kısmen.** Sayılar doğru ama **kapsamları dar**: Ç1.4'ün %0,156'sı aracın değil, kâhin aktarıcının özelliğidir |

---

---

# 🔍 DENETİMİN "ANLAŞILMAYANLARI" — YEDİSİ DE KAPATILDI

`aile0_audit.md` §7, denetçinin **anlayamadığı yedi mekanizmayı** listeliyor
ve şunu diyor: *"Bu bölüm boş değil — anlamadığım bir mekanizma,
denetlenmemiş bir mekanizmadır."* Hiçbiri bulguya çevrilmemişti; kapanıştan
önce yedisi de ölçüldü.

| # | Denetçinin anlamadığı | Ölçüm / karar |
|---|---|---|
| **1** | K-019'un *"sapma gereken çift"* metriğinin kod karşılığı | 🔴 **Kurtarılamadı.** Tanım yeniden ilan edildi, tablo yeniden üretildi, **seçim ölçütü değişti** *(K-039)*. S2 = +2 dBm değişmedi |
| **2** | `UC_DURUMLAR` sözlüğü çağrı sırasında **kalıcı olarak** değiştiriliyor — *"bilinçli mi, fark edilmemiş mi belirleyemedim"* | 🔴 **Fark edilmemişti.** `uc_durum_matrisi()` artık **kopya** üzerinde çalışıyor. Bugün zararsızdı *(çıkarılan değer varsayılanla aynıydı)*, ama bir uç durumun senaryosu "S2"den farklı yazılsaydı ikinci çağrı sessizce başka senaryo koşardı |
| **3** | S2/seyrek/tohum=30'un **tam %0 teslim** vermesi tesadüf mü, topolojik özellik mi | ✅ **Ölçüldü: 30 tohumun yalnızca 1'i** (tohum 30). Teslim < 0,10 olan başka tohum **yok**. Tek tohumluk bir kuyruk durumu, sistematik değil. ⚠️ Ve o koşu artık `yakinsadi: None` + `dejenere` ile işaretleniyor *(B-11)* — *"hiçbir şey teslim edilmedi"* ile *"mükemmel yakınsadı"* aynı sayıya eşlenmiyor |
| **4** | `_bekleyeni_kostur` ↔ `_uyandir` öncelik sırası; **beacon açlığa düşüyor mu** | ✅ **Ölçüldü.** Kaçırılan beacon oranı: S0'da **%0,00** *(üç trafik seviyesinde de)*, S2'de %0,10 → %0,37 → **%0,65** *(seyrek → yoğun)*. Açlık **yok**; kayıp karıştırmadan geliyor ve %1'in altında |
| **5** | Kanal dilimi MAC slotunun **tam 5 katı** — bir sonucu var mı | ✅ **Ölçüldü, sonucu yok.** Slot ızgarasındaki anların dilim içi dağılımı düzgün *(40006/39981/39996/39976/40041)*; ardışık slotta çekim değişme oranı **2000/10000 = tam 1/5**, yani beklenen. Gerçek yeniden deneme aralığı ≥ 9528 µs = **95 dilim**; 5 slotluk ızgara o mesafede anlamsız |
| **6** | `gurultuden_kacan`da kayan nokta **beraberliği** oluyor mu | ✅ **Ölçüldü.** Beraberlik içeren karar oranı: S0 **%0,08** *(72 749 kararda 56)*, S2 **%0,00**. Beraberlik nadir ve `min(sorted(…))` deseniyle **belirlenimci** çözülüyor |
| **7** | Tek makine, tek Python sürümü | ⚠️ **Aşılamadı** — Ç2 KAPSAMAZ tablosunda zaten yazılı |

---

# 🔍 KÖR MUTASYON TARAYICISININ KAPSAMI

`dogrulama/kor_mutasyon.py` mutant havuzunu **koddan üretir**; havuz kodla
birlikte büyür. Bir koşuda havuzdan **24 mutant** örneklenir.

| tarih | havuz | taban | skor | sağ kalan |
|---|---|---|---|---|
| 19 Ağu | 185 | 220 test | %47,8 (11/23) | 12 → ayıklandı *(K-038)* |
| **20 Ağu** | **203** | **271 test** | **%55,6 (10/18)** | **8** → ayıklandı *(K-044)* |

⚠️ O taramadan sonra test paketi **271 → 284**'e çıktı *(B-27b içerik
testleri, KM1–KM6, ve K-046'nın 12 kapı seçimi testi)*. Skor bir **kod
durumu fotoğrafıdır**; bu satır 20 Ağustos öğleden önceki koda aittir ve
bugün yeniden koşulsa **başka bir örneklem** seçilir.

🔴 **SKOR İKİ ŞEYE BİRDEN BAĞLIDIR: havuza ve test paketine.**
`random.Random(tohum).sample(havuz, 24)` havuzun **uzunluğuna ve sırasına**
bağlı olduğu için havuz büyüyünce örneklem tamamen değişir — 19 ve 20 Ağustos
örneklemlerinin **yalnızca 1 mutantı ortaktı**. Yani iki skor
**karşılaştırılamaz**; ilerleme ölçüsü değildir.

⚠️ 20 Ağustos'a kadar bu belge *"185 mutant · 161 sınanmadı · %47,8"* diyordu
ve o sayı **artık üretilemiyordu** (B-25). Üretici komut beyan edilmişti ve
o sayıyı vermiyordu — kural 1 ihlali.

Sağ kalanların **hepsi ölçümle ayıklandı**: `dogrulama/sag_kalan_ayikla.py`
her birini sabit bir matriste koşup tam sonuç sözlüğünü tabanla karşılaştırır.
Davranışı değiştirenler regresyon testine bağlanır ve mutasyon paketine girer.

### 🔴 KAPSAMAZ

| Kapsanmayan | Not |
|---|---|
| **239 mutant hiç sınanmadı** | 🔴 **B-151 (sekizinci denetim): 231 → 239.** Örneklem sayısı `08`in kendi denkleminde **24** olarak geçiyordu ve o sayı **kodda yoktu** — `kor_mutasyon.py`nin varsayılanı **16**. 24'ün tek kaynağı, başlığında *"🔴 DURUM: BAYAT … Bir sayıyı buradan OKUMA"* yazan `ciktilar/kor_cikti.txt` idi; yani bayatlamayı önlemek için yazılan Y12 koruması **ikinci bir elle tutulan sabit** getirmişti. 🔒 Artık `kor_mutasyon.VARSAYILAN_ORNEKLEM`den türüyor: **255 − 16 = 239**. ⚖️ Yön muhafazakâr — *"sınanmamış"* sayısı **artıyor**, yani beyan genişliyor. ⚠️ **B-139 (yedinci denetim): 229 → 231.** Havuz **253 → 255** büyüdü *(B0/B0.7/B0.8'de `sim/karsilastirma.py` genişledi)*. 🔒 **Bu satır artık ELLE TUTULMUYOR:** `tests/test_kapi_secimleri.py::test_b139_kor_havuz_sayisi_08_ILE_AYNI` onu ölçülen havuzla bağlıyor ve saniyeler içinde konuşuyor. Sayı **iki kez** bayatlamıştı *(B-114 · B-139)*; üçüncüsü olmayacak *(Y12)*. ⚠️ **27 Ağu — B-114: 179 → 229.** Havuz **203 → 253** büyüdü *(havuz koddan üretilir ve kodla büyür)*; bu satır 203'te kalmıştı. **Üretici:** `python -c "import sys;sys.path.insert(0,'.');from dogrulama.kor_mutasyon import mutantlari_uret;print(len(mutantlari_uret()))"` ~~Örneklem 24/253~~ → **örneklem 16/255** *(B-151)*. Skor bu örneklem üzerinden okunur; *"kodun %55,6'sı korunuyor"* **demez** |
| Mutasyon operatörleri sınırlı | Yalnızca karşılaştırma/işaret/bool çevirmeleri. Silme, sıra değiştirme, sınır kaydırma yok |
| **Bu bir KAPI DEĞİLDİR** | Eşdeğer mutantlar sağ çıkar ve bu normaldir. Kapı ölçütü `mutasyon_paketi.py`nin **41 hedefli** mutasyonudur *(2 Eylül: 35 → 41, B-131 — `sim/karsilastirma.py` 1 → 7)* |

# 🔒 KAPANIŞ ÖN KOŞULLARI — YEDİSİ DE SAĞLANDI

1. ✅ 23 denetim bulgusunun tamamı kapalı
2. ✅ Bu belge yeniden yazıldı, 5 madde ve kâhin notu eklendi
3. ✅ Denetimin **§7 "anlaşılmayanları"** — yedisi de ölçüldü/karara bağlandı
4. ✅ **Kapı kriterlerinin kendisi denetlendi:** Ç1.1 boş kümede geçiyordu
   *(`0 == 0`)*, eşiği veriden türetiliyordu — beklenen koşu sayısı **540**
   sabit yazıldı. Ç1.4 boş kümede açıkça düşüyor
5. ✅ `mutasyon_on_kontrol.py` — **30/30** *(pahalı koşudan önce, 0,3 dk)*
6. ✅ **`python dogrulama/aile0_kapi_raporu.py` koşuldu — 13/13**, 35,6 dk
7. ✅ Kapanış **K-043** olarak kayda geçti
8. ✅ **İkinci bağımsız denetim** — 17 bulgu, hepsi kapalı *(K-044)*
9. ✅ **Kapı raporu şema değişikliğinden sonra koşuldu** — 20 Ağustos,
   **13/13**, 73,9 dk *(K-046)*. ⚠️ İlk koşu **12/13** verdi; düşen Ç5'in
   sebebi ölçüldü, düzeltildi ve **ucuz bir testle** kalıcılaştırıldı
10. ✅ **ÜÇÜNCÜ bağımsız denetim yapıldı** — **24 bulgu** *(B-41…B-64)*
    artı §ANLAŞILMAYANLAR'dan çıkan **A-4**. Biri ölçümle **çürütüldü**
    *(B-58 — K-052)*; kalan **23'ün 23'ü kapatıldı** *(K-047…K-053)*.
    🔴 **Sağ kalan oranı: 10/15 = %66,7** — nominal olarak 7/10'un altında,
    **ama denetçi *"örüntü kapandı"* demeyi REDDETTİ**: n=15'te binom SH
    ≈ 12,2 puan *(fark 0,3 SH)*, aynı ölçekte oran birebir **%70**, ve iki
    örneklem de amaçlı seçildi. **Örüntü üçüncü kez kapanmadı.**
    ⚠️ **Bir bulgu açık:** B-57 *(karar kayıtlarında üretici satırı oranı —
    ölçüldü: 52 kaydın 16'sı)*; Aile 1'in ilk sonucundan önce yapılacak
11. ✅ ~~**`sim/kosucu.py::_kurulum_hash`'in ayraç hatası**~~ — 🔴 **BÖYLE
    BİR HATA YOK, iddia çürütüldü (K-052).** Ham baytlar ölçüldü:
    `h.update(b"\x1f")`. *(Eski metin: `h.update(b"")`
    hiçbir şey yapmıyor)* — bilerek açık bırakıldı; düzeltmesi üçüncü
    denetimden sonra *(K-046)*

12. ✅ **Kapı raporu üçüncü kez koşuldu — 13/13**, 98,2 dk
    *(21 Ağustos 2026, K-054)*. Şema bu denetimde **beş alan** büyümüştü
    *(`bildirdigi_yuk` · `yuk_bayt_toplam` · `secim_avantaji_ortalama` ·
    `secim_avantaji_karar` · `kaynak_hash`)*
13. ⬜ **B-57 — karar kayıtlarında üretici satırı** *(ölçüldü: 55 kaydın
    25'inde)*. Kapatılmadı: eski bir kayda üretici komut **uydurmak** kural 1'in
    daha ağır ihlalidir. 🔒 Taraması **26 Eylül mühründen önce** *(K-053)*

> 🔴 **Bu belge, 13 kapanmadan MÜHÜRLENMEZ.**

> ⚠️ **Bir kapı, koşulmadığı sürece geçmiş sayılmaz.** Bu oturumda tam
> olarak bu sınıftan **iki** vaka bulundu: Ç1.3'ün `17/17`si kirli bir
> tabandan üretilmişti *(B-21)* ve Ç5'in beklenen test sayısı bayattı
> *(K-040)*. İkisi de "araç doğru, çıktısı bayat" örüntüsüydü.
