# 13 — FAZ 0 KAPANIŞ KANITI

> ⚠️ **DOSYA ADI TARİHSELDİR** — `AILE0` yazıyor, içerik **Faz 0**'dır.
> Ad değiştirilmedi çünkü depoda ona yapılan atıflar kırılırdı.

> **Tarih:** 1 Eylül 2026
> **Soru (öğrenci):** *"Faz 0'ın tamamen kapandığına emin olmamız gerekiyor,
> kanıtlarıyla beraber — ve bunun ötesinde simülasyonun doğru ve güvenilir
> olması gerekir."*
>
> 🔴 Bu belge bir **kanıt envanteridir.** Her satır bir iddia, bir kanıt ve
> bir **üretici komut** taşır. Kanıtı olmayan satır 🔴 diye işaretlenir.

---

# 0 · 🔴 KISA CEVAP

> ## AİLE 0 **KAPALI DEĞİLDİR.**

Öğrenci haklı. Ve bunu ilk söyleyen **bu belge değil, deponun kendi
belgeleri:**

| kaynak | ne diyor |
|---|---|
| `08` §başlık | *"🔴 **AMA BU BELGE HENÜZ MÜHÜRLENMEDİ — D-13 AÇIK.**"* |
| `08` kapanış ön koşulu 13 | ⬜ **B-57 açık** · *"🔴 Bu belge, 13 kapanmadan MÜHÜRLENMEZ."* |
| `04` K-076 §3 | beş iddianın **üçü** tam yeşil değil |

🔴 **HATA BENDE:** `12-YOL-HARITASI.md` §0'a *"Faz 0 · 🟢 **KAPALI**"*
yazdım. K-076 bunu söylemiyor. **Düzeltildi** — bkz. §9.

⚖️ **Ama "kapalı değil" ile "geçersiz" aynı şey değildir.** Aşağıdaki dört
kanıt tablosu neyin kanıtlandığını, neyin kanıtlanmadığını **ayrı ayrı**
gösteriyor. Kapının **13/13'ü ayaktadır ama artık BAYATTIR** *(B-129)* — §4'te
kriptografik olarak kanıtlanıyor.

---

# 1 · 🔴 ÖNCE BİR AYRIM — yoksa yanlış şey düzeltilir

İki ayrı soru var ve **karıştırılırsa hem zaman hem güven kaybedilir:**

| | soru | kim cevaplar | bugünkü durum |
|---|---|---|---|
| **A** | **ARAÇ DOĞRU MU?** Hesapladığını söylediği şeyi hesaplıyor mu? | **Faz 0** *(kapı · `03` Bölüm C · Bölüm D)* | 🟡 **kısmen** — §4–§7 |
| **B** | **MODEL GERÇEKÇİ Mİ?** Modellenen dünya bir FANET'e benziyor mu? | **`08` kapsam beyanı** *(32 madde)* | 🟢 **beyan edilmiş sınırlar içinde** |

🔴 **Öğrencinin gerekçesi B'ye ait, sonucu A için doğru.** İkisi farklı
yollardan bağlanıyor ve bağlantı **tek bir yerde**: `03` Bölüm D **seviye 4
(literatür replikasyonu)**. Orası zaten **açık** *(§6)*.

⚖️ **Neden bu ayrım önemli:** *"literatür 512 bayt diyor, biz 1024
kullanıyoruz"* Faz 0'ı **açmaz** — o bir kapsam kararıdır ve `08`
onu taşır. Ama *"aracın kendi ilan ettiği geçerlilik ön koşulu ölçülmemiş"*
Faz 0'ı **açar** — ve bugün tam olarak öyle bir şey bulundu *(§7)*.

---

# 2 · ÖĞRENCİNİN GEREKÇESİ ÖLÇÜLDÜ

> *"Literatürde bu tarz simülasyonlar hakkında parametreler ve özellikler
> sunuluyor, bizim şu anki simülasyon bunlara uygun değil."*

**Ölçüldü** *(`10` §2, 68 yargı satırı)*. Sonuç iki parçalı:

## 2.1 🟢 GEREKÇENİN TUTMAYAN KISMI — ölçümle

| iddia | ölçülen | üretici |
|---|---|---|
| *"Parametrelerimiz literatüre uymuyor"* | **47 satır uyuyor**, 3 çelişiyor, 14 eksik, 3 karşılaştırılamaz | `10` §9 |
| *"Çalışma noktamız farklı"* | 🔴 **YANLIŞ** — normalize sunulan yük **%8,192**, literatür baseline'ıyla **BİREBİR** | `10` §2.4 |
| *"Soyutlama seviyemiz yetersiz"* | 🔴 **YANLIŞ** — literatürün *"en yaygın ve en titiz"* dediği **Seviye 3 (BER→PER)**; chunk bazlı PER **birebir** | `10` §6.1 |
| *"Kâhinlik riski var"* | 🔴 **YANLIŞ** — literatürün kâhin yasağı `03` kural 5'in **birebir aynısı** | `10` §6.2 |

⚖️ Yani *"simülasyon literatüre uygun değil"* cümlesi, **ölçüldüğünde
büyük ölçüde tutmuyor.** Uymayan üç şey var *(3B · mobilite · bit hızı)*
ve üçü de `08`'de **beyan edilmiş sınırlar**.

## 2.2 🔴 GEREKÇENİN TUTAN KISMI — ve beklenenden güçlü

Literatür taraması Faz 0'a **üç gerçek delik** açtı:

| # | ne | nasıl bulundu |
|---|---|---|
| **1** | `06` Bölüm 5 **koşul 1** hiç ölçülmemişti — ölçüldü, **kısmen düştü** | `10` §7b.3 |
| **2** | `06` Bölüm 5 **koşul 2** gecikme için sağlanmıyor: ortalama **ters yönü** gösteriyor | `10` §7b.4 |
| **3** | `08`'in **mühür bekleyen** sayfasında iki sayının üreticisi **çalışmıyor** | `10` §8 |

🔴 **Üçü de öğrencinin gerekçesinden DAHA GÜÇLÜ**, çünkü üçü de aracın
**kendi ilan ettiği** şartların ihlali — dış bir standarda uymama değil.

---

# 3 · KANIT TABLOSU A — 13 KAPI KRİTERİ

## 3.1 🟢 ÖNCE: KAPI SONUCU BAYAT DEĞİL — kriptografik kanıt

Kapı **27 Ağustos 2026, 20:11**'de koştu *(K-076)*. O günden bu yana `sim/`
değişti mi?

```bash
PYTHONIOENCODING=utf-8 python -c "import sys;sys.path.insert(0,'.');import json;from sim.results import kaynak_hash;e=json.loads(open('ciktilar/sonuclar/deneme_araliklari.jsonl',encoding='utf-8').readline());print(e['kaynak_hash'], kaynak_hash(), e['kaynak_hash']==kaynak_hash())"
```

**Çıktı — 27 Ağustos 2026:**
```
89587a191640a650f27bba12a253293e 89587a191640a650f27bba12a253293e True
```

> ## 🔴 BU BLOK ARTIK `False` BASIYOR — **B-129** *(2 Eylül 2026)*
> ```
> 89587a191640a650f27bba12a253293e fc73905bbb00ad719b31eb5dbb9f8f19 False
> ```
> `sim/` B0/B0.7/B0.8'de değişti *(`karsilastirma.py` + `kosucu.py` yorumu)*.
> 🔒 **Bilinçli:** kapı `12` §2.3 gereği **B0 ve B1 birlikte bittikten
> sonra TEK KEZ** koşar.
> 🟢 **Davranış değişmedi — ölçüldü:** `89587a19…` ↔ `0a1a94e5…` arasında
> **120 iş bit-birebir aynı**. Kapının yeniden koşma gerekçesi sonuçların
> değişmesi değil, **mutasyon havuzunun (253 → 255) ve test sayısının
> (429 → **473**) büyümesidir.** *(B-163: burada **471** yazıyordu; B-138 aynı gün README/`09`/`12`/`04`ü 473'e güncelledi, bu bloğu güncellemedi.)*

~~🟢 `sim/` altındaki tüm kaynak dosyaların blake2b içerik hash'i BİREBİR
AYNI … 13/13 bayat değildir.~~ 🔴 **2 Eylül'de bu artık DOĞRU DEĞİL** —
yukarıdaki bloğa bakınız *(B-129)*.

⚖️ Bu, `results.py`nin *"git'ten daha iyi: git kaydedilmemiş yerel
değişiklikleri göremez, hash görür"* iddiasının ilk fiilen kullanıldığı yer.

## 3.2 Kriterler ve ne KANITLADIKLARI

| kriter | ölçülen | 🔴 NE KANITLAMAZ |
|---|---|---|
| Ç1.1 korunum | 540/540 | *"hiçbir paket kaybolmuyor"* **DEMEZ** — `dus()` silinirse paket "uçuşta" asılı kalır ve eşitlik tutar *(K-029)* |
| Ç1.2 dört düşme sebebi | 4/4 | üçü **yalnızca uç durum** koşularında tetiklendi; ana matriste `kuyruk_tasmasi`/`ttl`/`hedef_yok` **hiç koşulmadı** *(`08` Ç1)* |
| Ç1.3 mutasyon paketi | 35/35 | 🔴 **253 mutantın 229'u hiç sınanmadı** *(`08` kör tarama)* |
| Ç1.4 boruda kalan | %0,156 | ana matris **tek bir KÂHİN aktarıcıyla** koşuldu; saf gözlemle **%0,531 (17 kat)** |
| Ç2 belirlenimcilik | 6 geçti | yalnız **Python 3.11.8 · Windows · tek CPU** |
| Ç3 analitik | 46 geçti | modülasyon · çoklu yol · Doppler · anten yönlülüğü **yok** |
| Ç4.1 Li regresyon | 6 geçti | — |
| Ç4.2 Li platosu | 1/6,29 · GA %2,04 | 🔴 **1/7 birebir üretilmedi**; %10,2'lik açık **AÇIKLANAMAMIŞTIR** *(§6)* |
| Ç5 gözlem sözleşmesi | 55 geçti | 🔴 **gerçek protokolle sınanmadı** — Aile 1'de yeniden sınanmalı |
| Ç6.1–6.4 kaynak denetimi | 4 geçti | grep/AST — **davranış değil** |

🔴 **KAPININ KENDİ KAPSAM BEYANI:** bu sütun `08`'in KAPSAMAZ tablolarından
**birebir** alındı. Yani kapı *"13/13"* derken **neyi iddia etmediğini**
zaten yazmış.

**Yargı:** 🟢 **13 kriter geçti, sonuç güncel, kapsamı yazılı.**
🔴 **Ama kapı "Faz 0 kapandı" demez** — bunu §5–§7 söyler.

---

# 4 · KANIT TABLOSU B — `03` BÖLÜM C · ALTI ZORUNLU SÖZLEŞME

| # | sözleşme | durum | kanıt |
|---|---|---|---|
| 1 | Gözlem sözleşmesi | 🟢 | Ç5 · 55 test · mutasyonla doğrulandı |
| 2 | Ayrık RNG akışları | 🟢 | `07` akış tablosu · `kanal_cekimi` hash'i · **1 beyan edilmiş istisna** *(`08` md 32)* |
| 3 | Korunum denklemi | 🟢 | `sonuc()["korunum_tamam"]` · bu oturumda **300/300** |
| 4 | Ölçüm penceresi | 🟢 | 25 pencere ikizi + maksimum + 2 türev |
| 5 | **Sonuç + konfigürasyon** | 🟢 **KAPANDI** *(B0.1)* | İşçiler tam sonucu **döndürür**, ebeveyn **yazar**. Ölçüldü: `ana_matris` **2/2**, `uc_durum_matrisi` **20/20** satır. Koruma DAVRANIŞSAL *(`test_d13_HAVUZLU_MATRIS_SATIR_SAYISI_KOSU_SAYISINA_ESIT`)* + üretim yolunda `assert`. **3 mutasyon, 3'ü de yakalandı.** 🔴 Kapının kendi `.jsonl`i **B2'de** dolacak |
| 6 | Karar kaydı | 🟡 **kısmen** | 78 kayıt · **27'si ölçüm taşıyıp üreticisiz** *(B-57 · `08` ön koşul 13 ⬜)* |

**Üretici:**
```bash
PYTHONIOENCODING=utf-8 python dogrulama/karar_kaydi_denetimi.py
```
```bash
ls -l ciktilar/sonuclar/aile0_kapi_raporu.jsonl
```

**Yargı:** 🔴 **6 sözleşmenin 4'ü tam, 1'i açık (D-13), 1'i kısmi (B-57).**

---

# 5 · KANIT TABLOSU C — `03` BÖLÜM D · DÖRT DOĞRULAMA SEVİYESİ

> `03` Bölüm D: *"Önleme yolu dört seviyelidir ve **pazarlık konusu
> değildir**."*

| # | seviye | durum | kanıt |
|---|---|---|---|
| 1 | **Analitik doğrulama** | 🟢 | Ç3 · 46 test · kTB −114 dBm · Friis · dekat başına 10α · β^(1/α) |
| 2 | **Korunum kontrolleri** | 🟢 | Ç1 · 540/540 · her koşuda otomatik |
| 3 | **İç tutarlılık** | 🟢 | Ç2 · aynı tohum → birebir · 3 `PYTHONHASHSEED` · bu oturumda SJR betiği için de doğrulandı |
| 4 | ⭐ **Literatür replikasyonu** | 🔴 **AÇIK** | Nitel eğilim 🟢 tuttu · **farkın gerekçesi 🔴 SAĞLANMADI** |

## 5.1 🔴 SEVİYE 4 — açığın tam hâli

`08` Ç4'ün kendi tablosu:

| aday | ölçülen üst sınır |
|---|---|
| bit hızı | %1,1 |
| EIFS | ≤ %0,31 |
| RTS/CTS | ≤ %7,71 |
| **en cömert toplam** | **≤ %9,1** |
| 🔴 **gereken** | **%10,2** |

> *"Kalan %10'luk fark için üç aday ölçüldü; üçünün üst sınırları toplamı en
> cömert varsayımla bile açığı kapatmıyor. Fark bugün **AÇIKLANAMAMIŞTIR**."*

🔴 **İŞTE ÖĞRENCİNİN GEREKÇESİNİN AİLE 0'A BAĞLANDIĞI TEK YER.** Literatür
replikasyonu, *"araç gerçek dünyayı temsil ediyor mu"* sorusunun Faz 0
içindeki karşılığıdır — ve **bugün sağlanmıyor.**

⚖️ **Ama `03` Bölüm D bunu bir başarısızlık saymıyor:** *"bir replikasyon
ilk denemede başarısız olursa bu bir kayıp değil, raporun en güçlü
bölümlerinden biri olabilir — **eğer sebebi bulunup yazılırsa**."*
Sebep bulunamadı; **arama ve sonucu yazıldı.** Bu, seviye 4'ü *"sağlandı"*
yapmaz ama *"gizlendi"* de yapmaz.

**Yargı:** 🔴 **4 seviyenin 3'ü tam, 4'ü açık ve bu YAZILI.**

---

# 6 · 🔴 KANIT TABLOSU D — `06` BÖLÜM 5 · DÖRT GEÇERLİLİK ÖN KOŞULU

> `06` Bölüm 5: *"**Dördü birden sağlanmayan** hiçbir sonuç raporlanmaz."*

🔴 **BU, BELGENİN EN SERT BÖLÜMÜDÜR** — ve bugüne kadar **hiç
denetlenmemişti.**

| # | ön koşul | durum | kanıt / eksik |
|---|---|---|---|
| **1** | Sonuç **koşu uzunluğundan bağımsız** | 🟡 **ÖLÇÜLDÜ · ÖLÇÜT İLAN EDİLDİ** | Ölçüt: çift yönlü **kesin işaret testi** *(α = 0,05)* + dışlanan etki büyüklüğü *(`06` §9.1)*. Ölçüt eski yargıları **birebir** üretiyor → gevşetme yok. 🔴 **B-147 (8. denetim): 18 çiftin 3'ü** ayak 1'i geçmiyor — `gurultuden_kacan`/S2/teslim *(8/30, p = 0,0161)* · `en_kisa_yol`/**S0**/gecikme ort. *(22/30, p = 0,0161)* · 🆕 **`DV`/S2/gecikme ort.** *(21/28, p = 0,0125)*. 🔒 Ayak 2'nin eşiği boş olduğu için geçen 15 çift de *"sağlandı"* **sayılamaz** |
| **2** | **Metriğin ne ölçtüğü** doğrulanmış | 🟢 **KAPANDI** *(B0.3)* | 🔴 Reçete ölçümle **değişti**: sorun *"ortalama yerine p95"* değil, **karşılaştırılan küme**. Ortak alt kümede ortalama **+5,40 ms** *(p = 0,0003)*, p95 **+28,15 ms** *(p = 0,0000)*; **ham** okumanın işareti kararsız *(12/30)*. Üçü — ortak alt küme · yüzdelikler · kesişim oranı — **kodda zorunlu** |
| **3** | Kollar arasında **gizli asimetri yok** | 🟢 **KAPANDI** *(B0.4)* | Asimetri **30 tohumla** ölçüldü *(eski sayı 3 tohumdandı — `03` kural 2 ihlali)*: **4,0–38,0 kat** bayt · **2,6–18,9 kat** airtime, **pencereden**. Raporlanması `ortak_alt_kume`de **tipli hatayla** zorunlu |
| **4** | Sonucu üreten kodun **regresyon testi var** | 🟡 **kısmen** | `karsilastirma.py` **B0.5'te denetlendi**. 🔴 A-14'ün nicel hâli: modül `mutasyon_paketi`nin 35 mutasyonunun **1'ini** taşıyordu *(kosucu 11 · mac 11)* ve 16 hedefli mutasyonun **6'sı sağ kaldı** *(skor 10/16)*. 🟢 Altısı da kapatıldı ve **her biri kendi mutasyonuyla doğrulandı** *(6/6)* → **16/16**. ⚠️ Kalan 🟡: paketin **geneli** için mutasyon skoru hâlâ ölçülmedi |

## 6.1 ⚖️ Bu tablo neden bu kadar önemli

`06` Bölüm 5 **Aile 1'in sonuçları için** yazılmış bir şart listesidir.
Ama şartların **üçü aracın kendisine** ait *(koşu uzunluğu · metrik
geçerliliği · kol simetrisi)* ve **hiçbiri Faz 0 kapısında ölçülmüyor.**

🔴 **Yani kapı 13/13 verirken, aracın kendi ilan ettiği dört geçerlilik
şartının ikisi ölçülmemişti ve ölçüldüklerinde tutmadılar.**

Bu, `03` B6'nın ⭐⭐⭐ tuzağının tarifidir:
> *"Kod doğru, testler geçiyor, kapsam yüksek — **ve kurulum yanlış.**
> Bu sınıf sıradan kod incelemesiyle **bulunamaz**."*

🟢 **Ve bulunma sebebi öğrencinin ısrarıdır** — literatür taraması olmasa
koşul 1 hiç ölçülmezdi. Bu, ısrarın **yedinci** kez haklı çıkışıdır.

---

# 7 · AÇIK KALEMLERİN TAM LİSTESİ — 8 kalem → 🟢 **B0 SONRASI 3**

| # | kalem | tür | durum *(B0 sonrası)* |
|---|---|---|---|
| **1** | **D-13** — sözleşme 5, Ç1 yolunda ihlal | 🔴 sözleşme | 🟢 **KAPANDI** *(B0.1)* — 3 mutasyon, 3'ü yakalandı. Kapının `.jsonl`i **B2'de** dolacak |
| **2** | **B-57** — 27 kayıt ölçüm taşıyıp üreticisiz | 🟡 sözleşme 6 | 🟡 **beyanlı kapalı** *(K-053: uydurma yasak)* — değişmedi |
| **3** | **Seviye 4** — Li açığı %10,2 açıklanamadı | 🔴 doğrulama | 🟡 **beyanlı açık** — ama üreticisi **onarıldı**, dört sayı **birebir üretildi** *(B0.6)*; ⚠️ **F-6** düzeltildi |
| **4** | **`06` koşul 1** — koşu uzunluğu bağımsızlığı | 🔴 | 🟡 **ÖLÇÜT İLAN EDİLDİ · KOL BAŞINA ÖLÇÜLDÜ** *(B0.2)* — **18 çiftin 3'ü** ayak 1'i geçmiyor *(B-147)*; ayak 2'nin eşiği **B4'te** |
| **5** | **`06` koşul 2** — gecikme metriği ters yön | 🔴 | 🟢 **KAPANDI** *(B0.3)* — reçete ölçümle düzeltildi, kodda zorunlu |
| **6** | **`06` koşul 3** — kontrol düzlemi asimetrisi | 🔴 | 🟢 **KAPANDI** *(B0.4)* — 30 tohumla yeniden ölçüldü, raporlama **tipli hatayla** zorunlu |
| **7** | **A-14** — `karsilastirma.py` denetlenmedi | 🟡 | 🟢 **KAPANDI** — mutasyon skoru **10/16** ölçüldü, **6 test boşluğu** kapatıldı → **16/16**; ve **B0.8'de kalıcı oldu**: altı kanıtlanmış boşluk `mutasyon_paketi.py`ye girdi *(modül **1 → 7** mutasyon, paket 35 → **41**)*. Bulgu **F-7** |
| **8** | **F-4** — mühür bekleyen 2 sayının üreticisi yok | 🔴 | 🟢 **KAPANDI** *(B0.6)* — ikisi de `dogrulama/` altına yazıldı ve üretildi |
| — | *(mekanizma katmanı GA [0,139 · 0,549])* | 🟡 | Aile 1'e ait, Faz 0'a değil |

## 7.0 🔴 YEDİNCİ BAĞIMSIZ DENETİM — B0'IN KAPANIŞLARI YENİDEN YARGILANDI

**2 Eylül 2026** · `aile0_audit.md` §B0 DENETİMİ · **23 bulgu**
*(B-120 … B-142)* · soru: *"B0, ölçütlerini ölçtüğü şeyi geçirecek biçimde
mi seçti?"* → **KISMEN**.

| B0'ın iddiası | denetimin yargısı |
|---|---|
| **D-13** 🟢 kapandı | 🟡 **KOŞULLU** — şekli doğru ve **540 koşuda güvenli** *(bellek tavanı **35,2 MB**, denetim ölçtü)*; ama kanıt hâlâ 2 + 20 koşu ve `12` §2.1'in ölçütü **değiştirildi**. *"KAPANDI"* ancak `.jsonl` **560 satır** taşıdığında yazılmalı — **B2** |
| **`06` koşul 2** 🟢 kapandı | 🟡 **KOŞULLU** — reçete gerçekten **sıkılaştı** ve kodda zorunlu *(8/8 kırılarak doğrulandı)*; taşıyıcı satırın üreticisi **yoktu** *(B-121 → 🟢 B0.7'de kapandı)* |
| **`06` koşul 3** 🟢 kapandı | 🟢 **GEÇERLİ** — dokuz sayı **birebir** yeniden üretildi, 2 dejenere hücre dâhil |
| **F-4** 🟢 kapandı | 🟡 **KOŞULLU** — Ç4'ün dördü ve md 31'in payı **birebir üretildi**; çarpıklık gerekçesi **yanlıştı** *(B-120 → 🟢 B0.7)*, band **tek tohumluktu** *(B-123 → 🟢 B0.7)* |
| **A-14** 16/16 | 🟡 **ÖLÇÜM DOĞRU, KALICILIĞI YOK** — 16 mutasyon `mutasyon_paketi.py`ye girmedi *(B-131, açık)* |

🟢 **DENETİMİN 23 BULGUSUNUN 23'Ü İŞLENDİ:**

| ne zaman | bulgular | sonuç |
|---|---|---|
| **B0.7** *(K-087)* | B-120 · B-121 · B-123 | 🟢 kapandı — B1'in şartıydı |
| **B0.8** *(K-088)* | kalan **19** | 🟢 kapandı · **dört karar devredildi** |
| **B1.5'e** | **B-133** | 🔒 **şema alanı** — başka türlü kapatılamaz |

🔒 **Dört devredilen karar** *(K-088 §1)*: kontrol payı TANIMSIZKEN
karşılaştırma **yaşar** *(B-134)* · koşul 3'ün bağlayıcı çifti **DV ↔
gözlem** *(B-135)* · ölçüt **iki ayaklı**, ikinci ayağın eşiği **B4'te**
*(B-125)* · kesişim alt sınırı **uydurulmadı**, beyan edildi *(B-140)*.

## 7.1 🔴 SEKİZİNCİ BAĞIMSIZ DENETİM — **B0.9'DA 27 BULGU KAPANDI**

**2–3 Eylül 2026** · `aile0_audit.md` §B0.7/B0.8 DENETİMİ · **26 bulgu**
*(B-143 … B-168)* · soru: *"B0.7/B0.8'in düzeltmeleri düzeltti mi —
yoksa sorunu **komşuya mı taşıdı**?"* → **KISMEN**.

🔒 **Danışmanın yargısı** *(K-089)*: **26'sının 26'sı gerçek.** 22'si
birebir yeniden üretildi; denetçi **dört yerde yanıldı** *(hepsi kapsam
hatası, teşhis hatası değil)*. **+1 bulgu danışmandan: B-169.**

| B0.7/B0.8'in iddiası | denetimin yargısı | B0.9'da ne oldu |
|---|---|---|
| **B-124** iki estimand ayrıldı | 🔴 **TAŞINDI** — düzeltme `satir()`e yazılmış, o fonksiyonun **sıfır çağıranı** var | 🟢 Sözleşme `isaret_testi.ga_estimandi`ye çıktı; **üç biçimlendirici de** çağırıyor |
| **B-125** ölçüt iki ayaklı | 🔴 **TAŞINDI** — araç hâlâ `GECTI` basıyor *(18'in 15'i)* | 🟢 `ayak1_etiketi()` → **`YON-OK`/`YON-RED`**; özet ayak 2'nin boşluğunu **koşulsuz** yazıyor |
| **B-130** çapa 9/19 → 9/9 | 🔴 **AĞIR** — `sim/` değişince **9'un 5'i** susuyor | 🟢 Çapa artık **en son koşu grubunu** okuyor: 18/18, yakalama **8/8** iki durumda da |
| **B-123 · F-12** | 🔴 *"regresyon testi yok"* | ⚠️ **Kısmen yanlış** — ikisi de yakalanıyor; korunmayan **komşu nesneleri** |
| **B-131** 6 mutasyon pakete girdi | 🔴 betik yolu **35** görüyor | 🟢 Blok `__main__`in **üstüne** taşındı, numaralar **D32–D37** |
| **B-135** iki araç aynı çifti ölçüyor | 🟡 **iki farklı yüklem** | 🟢 İkisi de basılıyor, **yön değişimi sayılıyor** *(0/58)* |
| — | 🔴 **B-168:** DV bağlayıcı ilan edildi, `08` md 31'i ölçen araçta **yoktu** | 🟢 Eklendi ve **koşuldu**: 900 → **1 080 koşu** |

> ## 🔴 B0.9'UN EN DEĞERLİ ÖLÇÜMÜ — DV bandın üst ucunda
> `08` md 31 ilk kez DV'yi gördü: çarpıklık **1,2653 – 1,2974** — altı
> kolun **en yüksek alt sınırı**, ve üst ucu düzgün beacon beklentisi
> **1,2963'ün ÜSTÜNDE.** Yani kontrol baytını zamanda en düzensiz üreten
> kollardan biri, tam da **Faz 1'in AODV'sine en yakın** kol.
> ⚖️ Bu, md 31'in bağlayıcı cümlesini *(*"her karşılaştırma `*_pencere`
> kullanmak zorundadır"*)* **zayıflatmıyor, güçlendiriyor** — ve o kol
> ölçülmeseydi görülmeyecekti.

🔒 **B1'in altı bloke edici kalemi kapandı** *(B-143 · B-144 · B-145 ·
B-146 · B-147 · B-149 + B-164/B-133 B1.5'e yazıldı + B-168 ölçüldü)*.
Kalan 20 bulgunun **13'ü kapatıldı**, **7'si gerekçesiyle kayda geçti**
*(B-156 · B-157 · B-159 · B-160 · B-161 · B-167 ve B-162'nin kalanı)* —
🔴 **hiçbiri *"düşük öncelik"* denip düşürülmedi** *(`03` kural 10)*.



⚠️ **Kapsam maddesi 33 → 37** — dördü de *"eklenen madde önceki sonuçları
geçersiz kılar mı"* tablosuna gerekçesiyle yazıldı.

⚖️ **Denetimin tek cümlelik yargısı:** *"B0'ın kapattığı dört kaleme
**KISMEN GÜVENİLİR** — ölçümleri sağlam, gerekçeleri değil."* Hiçbir sayı
uydurulmadı, hiçbir eşik gevşetilmedi *(`03` kural 3 ihlal edilmedi)*.

## 7.1 🔴 B0'DA ÇIKAN DÖRT YENİ BULGU

| # | bulgu | nasıl bulundu |
|---|---|---|
| **F-5** | `kontrol_payi()` **tüm koşu** baytını okuyordu; `08` md 31 **pencereyi** şart koşuyor. Üstelik bağlayıcı oran **3 tohumdan** geliyordu *(`03` kural 2: ≥30)* | B0.4 kod okuması |
| **F-6** | `li_zincir.main()` çıktısı, `08` Ç4'ün **B-110'da geri aldığı** *"RTS/CTS ve EIFS'e atfedilir"* cümlesini basıyordu — üstelik kendi yorumunda *"jüriye gösterilecek çıktı"* diye tanımlı bir betikte | B0.6 kod okuması |
| **F-7** | `test_b19_ortak_alt_kume_secilim_yanliligini_ortaya_cikariyor` bir **yasa** iddia ediyordu *(`ham > ortak > 0`)*; ölçüldü — **5/30** tohumda tutuyor. Tek tohumluk bir gözlem değişmez sanılmıştı | B0.5 denetimi |
| **F-8** | `ciktilar/literatur_eksenleri_cikti.txt`, `CIKTILAR.md`nin **kendi kuralını** ihlal ediyordu *(B-64: "tarih ve kod durumu taşımayan çıktı silinir")* — diğer üç çıktının taşıdığı zorunlu başlık onda yoktu | B0.6 kapsam kontrolü |

⚖️ **Üçü de aynı sınıf:** bir sayı ya da ilişki **doğru göründü** ama
üreticisi ya da örneklemi onu taşımıyordu — B-25 · B-80 · B-81 · F-4 ile
aynı aile.

---

# 8 · KAPANMASI İÇİN GEREKEN — kanıt üreten iş listesi

Her satır **kanıt üretir**; hiçbiri *"gözden geçirildi"* değildir.

| # | iş | kanıt | süre |
|---|---|---|---|
| **1** | **D-13 düzeltmesi** + davranışsal test | `aile0_kapi_raporu.jsonl` satır sayısı = koşu sayısı | 0,5–1 gün |
| **2** | **Koşul 1'i KOL BAŞINA ölçen araç** | her kol için 200 s ↔ 350 s eşleştirilmiş fark + işaret testi | 0,5 gün · 3–12 dk koşu |
| **3** | **Koşul 2 — gecikme yüzdelikleri** *(R-13)* | p50/p95/p99 her sonuçta; `06` Bölüm 4 güncellenir | 1 gün |
| **4** | **Koşul 3 — kontrol payı tavanı ya da zorunlu raporlama** | her karşılaştırma kontrol payıyla; `karsilastirma.py`ye yüklem | 1 gün |
| **5** | **A-14 denetimi** *(R-4)* | bulgu listesi + mutasyonla sınanmış düzeltme | 0,5–1 gün |
| **6** | **F-4** — `08`'in iki sayısı yeniden ölçülür *(R-16a)* | çalışan üretici komut | 0,5 gün · 5–15 dk koşu |
| **7** | **B-57** taraması | üreticisiz 27 kaydın taranması *(🔴 uydurma YASAK — K-053)* | 1 gün |
| **8** | 🔴 **KAPI 7. KOŞU** — hepsinden sonra | 13/13 **düzeltilmiş koda** bağlanır | **194–435 dk** *(B-167)* |
| **9** | **`08` MÜHÜRLENİR** | ön koşul 13 kapanır | 0,5 gün |

**TOPLAM: ~6–8 efektif gün + 1 kapı koşusu.**

⚖️ **`11`'in "ASGARİ paket"i (5–8 gün) bunun ZATEN İÇİNDE** — 1·3·5·6
oradaki R-1 · R-13 · R-4 · R-16. **Yeni eklenen: 2 · 4 · 7.**
🟢 **Yani takvim ~1–2 gün uzadı, dallanmadı.** `12` §2'nin kritik yolu
7,5–12 gün → **9–14 gün**; 26 Eylül'e **hâlâ payı var**.

## 8.1 🔴 SEVİYE 4 (Li açığı) NE OLACAK

Bu kalem **kapatılamaz** — `03` Bölüm D'nin kendi cümlesi izin veriyor:
farkın gerekçelendirilmesi gerekiyor, gerekçe **arandı ve bulunamadı**,
**arama yazıldı**.

🔒 **Karar gerektirir *(altıncı soru)*:**

| # | seçenek | sonuç |
|---|---|---|
| a | **Olduğu gibi bırak** — *"açıklanamamıştır"* raporda yazılı kalır | 🟢 dürüst · seviye 4 🟡 kalır |
| b | **Yeni aday ara** *(NAV · yayılma gecikmesi · alıcı kilidi)* | süre öngörülemez, üçü de üst sınırı **küçük** ölçülmüş |
| c | **Li'nin kendi noktasında raporla** *(R-16a ile 2 Mbit/s)* | 🟢 iki **mutlak** sayı da tutuyor *(%3,6 ve %10,8)* — replikasyon **güçlenir**, açık kapanmaz |

**Önerim: (a) + (c) birlikte.** (c) hiçbir şey değiştirmeden replikasyonu
güçlendiriyor *(zaten R-16a'da var)*; (b) `03` B4'ün *"bir kusuru ölçmek
onu sebep yapmaz"* tuzağına açık.

---

# 9 · DÜZELTİLEN İDDİALAR

| belge | eski | yeni |
|---|---|---|
| `12` §0 | *"Faz 0 · 🟢 **KAPALI**"* | 🟡 **kapı 13/13 geçti · 8 kalem açık · `08` MÜHÜRLENMEDİ** |
| `12` §3 | *"A/C dalı 7,5–12 efektif gün"* | **9–14 efektif gün** *(§8'in 3 yeni kalemi)* |

---

# 10 · "GÜVENİLİR SİMÜLASYON" — iki ayrı soru, iki ayrı cevap

Öğrencinin ikinci cümlesi: *"simülasyonun doğru ve güvenilir olması
gerekir."* Bu **iki** şey ister:

## 10.1 🟢 DOĞRU — büyük ölçüde kanıtlı

| kanıt | ölçüldü |
|---|---|
| Analitik kapalı formlarla uyum | Ç3 · 46 test |
| Korunum, her koşuda | 540/540 + bugün 300/300 |
| Belirlenimcilik | Ç2 · hash · `PYTHONHASHSEED`'den bağımsız |
| Yayınlanmış sonucun nitel replikasyonu | Li: düşüş + plato + 4 atlamada 1/3,87 ≈ 1/4 |
| **40 hedefli mutasyonun 40'ı yakalandı** | Ç1.3 |
| Kalibrasyon bağımsız olarak **birebir** üretildi | bugün: 0,5252 |

## 10.2 🔴 GÜVENİLİR — burada eksik var, ve eksiğin adı konuldu

**Güvenilirlik** = *"bu araçla üretilen bir sonuca dayanabilir miyim?"*
Cevabı `06` Bölüm 5 veriyor ve **dördünden ikisi bugün düştü** *(§6)*.

🔴 **Bu yüzden §8'in 2 ve 4 numaralı işleri PAZARLIĞA KAPALIDIR:**
onlar olmadan Aile 1'in **hiçbir sonucu** `06` Bölüm 5'i geçemez — ve
`06` *"dördü birden sağlanmayan hiçbir sonuç raporlanmaz"* diyor.

⚖️ **Tek cümleyle:**

> **Araç DOĞRU olduğunu büyük ölçüde kanıtladı; GÜVENİLİR olduğunu henüz
> kanıtlamadı — çünkü güvenilirliğin ölçütünü kendi yazdı ve o ölçütü
> bugüne kadar hiç koşmadı.**

🟢 Ve bunu bulan şey bir denetim değil, **öğrencinin bir literatür
taramasından sonra sorduğu tek soru** oldu.
