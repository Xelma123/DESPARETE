# 12 — YOL HARİTASI · TÜBİTAK'A KADAR

> ## 🔴 §0.0 GÜNCEL HARİTA — 9 Eylül 2026. AŞAĞISI TARİHTİR.
> §0'dan itibaren gelen her şey emekli `sim/` planına aittir ve **süreleri
> geçersizdir**. Kritik yolu ve *"Kat 4 yetenek boşluğu"* bulgusunu tarih
> olarak koruyoruz — çünkü o bulgu **hâlâ geçerli çıktı** (K-111).

---

## 0.0 · GÜNCEL YOL HARİTASI

**Bugün 9 Eylül 2026 · Teslim 19 Aralık 2026 · kalan 101 gün.**

⚠️ Aşağıdaki süreler **ÖLÇÜM DEĞİL, TAHMİNDİR** ve BANT olarak verilir.
Bu projede ölçülmemiş sayı raporlanmaz; bunlar rapora değil **plana**
girer ve öyle etiketlenir.

### Nerede duruyoruz

| faz | konu | durum |
|---|---|---|
| **0** | simülatörü karara bağlama *(6 adım)* | 🟢 **6/6 bitti** · 475 test · yapısal ihlal yok |
| **1** | duyarlılık denetimi + Li replikasyonu | 🟢 **bitti** · borç 48 → 33 · dış çapa koşuldu |
| **2** | **dikey dilim** — tek protokol uçtan uca | 🔒 **başlamadı** · bugünkü yüzeyle YAZILABİLİR |
| **2,5** | 🔴 **kontrol düzlemi yeteneği** *(YENİ — K-111)* | 🔒 başlamadı · **Faz 3'ün ön koşulu** |
| **3** | taban çizgileri (AODV · OLSR · AOMDV) + **ön-kayıt mührü** | 🔒 Faz 2,5'e bağımlı |
| **4** | öğrencinin protokolü | 🔒 tasarım henüz boş (`06` §5.1) |
| **5** | tam deney | 🔒 mühre bağımlı |
| **6** | yazım | 🔒 |

### 🔴 KRİTİK YOL — ve üzerindeki TEK yeni engel

```
Faz 2 (dikey dilim)  ──┐
                       ├──> Faz 3 (taban çizgileri) ──> MÜHÜR ──> Faz 5 ──> Faz 6
Faz 2,5 (kontrol) ─────┘                                  ▲
                                                          │
                                            Faz 4 (özgün protokol)
```

🔒 **Faz 2 ile Faz 2,5 BİRBİRİNİ BEKLEMEZ.** Dikey dilim beacon taşıyan
proaktif bir protokolle bugünkü yüzeyde yazılabilir; kontrol düzlemi
yalnız **RFC'ye sadık taban çizgileri** için gerekli. İkisi paralel
gidebilir ve bu, kritik yolu kısaltan tek yapısal fırsattır.

### Mührün ÖN KOŞULLARI — hepsi sayılabilir

| ön koşul | bugün | kim kapatır |
|---|---|---|
| `SINANMAMIS` = 0 | **33** *(4'ü protokol olmadan kapanmaz)* | ajan + Faz 3 |
| duyarlılık borcu = 0 | **5** *(dördü DUYARLI çıktı)* | ajan / ön-kayıtta eksen ilanı |
| güç analizi kararı | ölçüldü: 30 tohum yalnız **3,6 PDR puanını** görüyor | 🔴 **öğrenci** |
| keşifsel yüksek çalkantı kolu (Θ = 1,78) | kapının altında | 🔴 **öğrenci** |
| `dugum_sayisi = 40` kapsam onayı | ölçülen band 20–80 | 🔴 **öğrenci** |
| U2 · U3 uygunluk testleri | 🔴 bugün **sınanamaz** (`06` §4.2 notu) | Faz 2,5 ya da 🔴 **öğrenci** |
| görev kolu yarıçapı | ölçüt sınanamıyor (2SE > tolerans) | 🔴 **öğrenci** |

### Kaba fiyatlandırma — ⚠️ TAHMİN, ölçüm değil

| iş | BANT | not |
|---|---|---|
| Faz 2 · dikey dilim | **2–4 oturum** | tasarım + protokol + uçtan uca doğrulama; simülatöre dokunmaz |
| Faz 2,5 · kontrol düzlemi | **3–5 oturum** | yapı onayı → uygulama → testler; şema genişlemiyor |
| Faz 3 · üç taban çizgisi | **4–8 oturum** | RFC sadakati + dört uygunluk testi × 3 protokol |
| mühür hazırlığı | **1–2 oturum** | borç sıfırlama + öğrenci kararları |
| Faz 4 · özgün protokol | **3–6 oturum** | 🔴 tasarım henüz yok |
| Faz 5 · tam deney | **koşum: BANT 20–60 saat** | 360 koşu çekirdek; ⭐ öğrencinin fikri: parça parça koş, birleştir |
| Faz 6 · yazım | **2–4 oturum** | |

🔴 **En büyük takvim riski Faz 4'ün tasarımının HENÜZ BOŞ olmasıdır**
(`06` §5.1). Ölçüm altyapısı hazır, ölçülecek fikir değil.

⭐ **Faz 4 için bir tasarım kısıtı zaten ölçüldü** (K-110 EK-4): gürültünün
MUTLAK değeri bu simülatörde anlamlı bir büyüklük değil, dolayısıyla
protokol karıştırmayı **mutlak eşikle sezemez** — oranla ya da değişimle
sezmelidir.

---


> **Tarih:** 1 Eylül 2026 · **Teslim:** 19 Aralık 2026 · **Kalan: 109 gün**
> **Durum:** 🔴 **ÖĞRENCİ ONAYI BEKLİYOR** — bu belge karar vermez, fiyatlandırır.
>
> ⚠️ **1 Eylül 2026'da BAŞTAN YAZILDI** *(K-083)*. Önceki sürüm *"Faz 0
> kapalı"* varsayıyordu ve **Kat 4 altyapı boşluğunu görmüyordu**.

---

# 0 · 🔴 BU BELGENİN EN ÖNEMLİ BULGUSU

Öğrencinin talebi netti: *"ileride sorun yaşayıp geriye dönmek
istemiyorum — bütüncül düşün."* Bunun için **Faz 1'in simülatörden ne
isteyeceği ölçüldü**, varsayılmadı. Sonuç:

> ## 🔴 ÜÇ RAKİP PROTOKOLÜN ÜÇÜ DE BUGÜNKÜ ARAYÜZLE **YAZILAMAZ**.

**Ölçüldü** *(üretici komutlar §2.1'de)*: protokolün simülatörle temas
yüzeyi **tek çağrı** *(`self.protokol(gozlem)` — sıradaki atlama)* ve
**iki kanca** *(`beacon_yuku` · `teshis`)*. Yayın gönderimi
*(`yayin_gonder`)* deponun **tamamında tek yerden** çağrılıyor: periyodik
beacon.

| protokolün ihtiyacı | bugün | sebep |
|---|---|---|
| **AODV RREQ** — talep üzerine selleme | 🔴 **YOK** | yalnız **periyodik** yayın var |
| **AODV RREP** — ters yol boyunca **unicast** kontrol | 🔴 **YOK** | unicast kontrol çerçevesi yok |
| **AODV RERR** — kopmada tetiklenen yayın | 🔴 **YOK** | olay-tetiklemeli yayın yok |
| **OLSR HELLO (2 s) + TC (5 s)** | 🔴 **YOK** | tek `beacon_araligi_s` |
| **ACTIVE_ROUTE_TIMEOUT** vb. | 🔴 **YOK** | protokol zamanlayıcı kuramıyor |

🔴 **Bu, sekiz açık kalemin HİÇBİRİNDE yok.** Onlar *geçerlilik*
kalemleri; bu bir *yetenek* boşluğu — ve **daha büyük**.

## 0.1 ⚖️ Ve tam olarak "geriye dönme" riski budur

| ne | neden geri dönülür |
|---|---|
| **Şema donmuş** *(79 alan)* | Faz 1 yeni sayaç istiyor *(PSR · kopma sayaçları · Δ · COR)*. Faz 1 başladıktan sonra eklenirse **eski satırlar karşılaştırılamaz** |
| **Arayüz** | Protokoller yazıldıktan sonra arayüz değişirse **üçü de yeniden yazılır** |
| **Kapı** | `sim/` değişince `kaynak_hash` değişir → 13/13 **bayatlar** |

🔒 **Sonuç: Kat 4 altyapısı Faz 0'ın İÇİNDE, Faz 1'den ÖNCE yapılmalıdır.**

## 0.2 🟢 İYİ HABER — üç şey riski düşürüyor, üçü de ölçüldü

| bulgu | sonucu |
|---|---|
| Kontrol çerçeveleri **deftere girmiyor** *(`sim/ledger.py`de `yayin`/`beacon` geçmiyor)* | 🟢 Korunum denklemi **bozulmaz** *(sözleşme 3 güvende)* |
| **`yuk_bayt` faturalama zinciri zaten var** *(`mac.yayin_gonder(..., yuk_bayt)`)* | 🟢 Yeni kontrol paketleri **aynı yoldan** faturalanır |
| **`05` §A2 hakkı zaten veriyor** — *"protokol paketin başlığında yazan her şeyi okuyabilir"* | 🟢 Bu bir **uygulama boşluğu**, kilitli sözleşmenin genişletilmesi **değil** |

⚖️ Yani yapılacak iş **yeni bir sözleşme kurmak değil, var olan sözleşmenin
mekanizmasını tamamlamak**. Bu, maliyeti ve riski ciddi biçimde düşürür.

---

# 1 · BUGÜNKÜ KONUM — ölçüldü

| | |
|---|---|
| Kapı | **13/13** *(27 Ağu, 185,6 dk)* · 🔴 **BAYAT** — `sim/` B0/B0.7/B0.8'de değişti *(`89587a19…` → `fc73905b…`)*. Bu **bilerek**: kapı `12` §2.3 gereği **B0 ve B1 birlikte bittikten sonra TEK KEZ** koşar. **B-129** |
| Test | **492/492** *(3 Eylül · B0.9'da +19)* |
| Karar kaydı | **89** |
| Kapsam maddesi | **37** *(2 Eyl: 33 → 37)* |
| Faz 0 | 🔴 **KAPALI DEĞİL** — 8 geçerlilik kalemi **+ Kat 4 altyapısı** |
| Faz 1 | 🔒 başlamadı — üç protokolün hiçbiri yazılmadı |
| Faz 2 | 🔒 **özgün protokol tasarımı öğrenciden bekleniyor** |

---

# 2 · İŞ BLOKLARI — her adımın DOĞRULAMA ÖLÇÜTÜ var

> 🔴 **Ölçüt olmayan adım yoktur.** *"Yapıldı"* demek yetmez; her blok
> **koşulabilir bir kontrolle** kapanır.

## 2.1 🟢 B0 · FAZ 0 — GEÇERLİLİK KAPANIŞI · **KOŞULDU** *(K-086)*

**Tahmin: 4–5 efektif gün** · **gerçekleşen: tek oturum**
*(koşu toplamı < 25 dk; en uzun tek iş A-14'ün mutasyon kapsamı, 43 dk)*

| # | doğrulama ölçütü | sonuç |
|---|---|---|
| B0.1 | `.jsonl` satır sayısı = koşu sayısı | 🟢 `ana_matris` **2/2** · `uc_durum_matrisi` **20/20** · 3 mutasyon yakalandı |
| B0.2 | eşleştirilmiş fark + **işaret testi** | 🟢 ölçüt **koşmadan önce** ilan edildi, **360 koşu**, **18 çiftin 3'ü** ayak 1'i geçmiyor *(B-147: ~~240 koşu · 12 çiftin 2'si~~ bayattı)* |
| B0.3 | `06` Bölüm 8 güncel; analiz türetiyor | 🟢 §8.1b eklendi — 🔴 **reçete ölçümle değişti** |
| B0.4 | karşılaştırma **tipli hatayla** reddediyor | 🟢 `_PAY_ALANLARI` zorunlu; md 25 **30 tohumla** yeniden ölçüldü |
| B0.5 | bulgular **mutasyonla** doğrulanmış | 🟢 skor **10/16** ölçüldü → 6 boşluk kapatıldı → **16/16** |
| B0.6 | üretici komutlar **koşuyor** | 🟢 ikisi de `dogrulama/` altında, `08`in 4 sayısı **birebir** |

🔴 **Dört yeni bulgu:** F-5 *(kontrol payı yanlış pencereden + 3 tohum)* ·
F-6 *(`li_zincir` geri alınmış cümleyi basıyordu)* · F-7 *(bir test tek
tohumluk gözlemi yasa sanmıştı)* · **F-8** *(çıktı politikası kendi dosyasında ihlal ediliyordu)*.

🔒 **Kapı artık BAYAT** — ölçüldü: `89587a19…` → `0a1a94e5…`. Bu bilerek;
kapı **B0 ve B1 birlikte bittikten sonra tek kez** koşar *(§2.3)*.

⏭️ **Sıradaki: B1** — tasarım taslağını bekliyor.

### Özgün tahmin *(karşılaştırma için korunuyor)*

**Süre: 4–5 efektif gün** *(8 kalemin 2'si zaten "beyanlı kapalı")*

| # | iş | doğrulama ölçütü |
|---|---|---|
| **B0.1** | **D-13** — `kapi_korunum` işçileri sonucu döndürür, ebeveyn yazar | `aile0_kapi_raporu.jsonl` **satır sayısı = koşu sayısı** *(0 bayt değil)* |
| **B0.2** | **`06` koşul 1** — koşu uzunluğu bağımsızlığını **kol başına** ölçen araç | Her kol için 200 s ↔ 350 s eşleştirilmiş fark + **işaret testi**; sonuç `04`e yazılır |
| **B0.3** | **`06` koşul 2** — gecikme **p50/p95/p99** her sonuçta *(R-13)* | `06` Bölüm 8 güncellenmiş; analiz `teslim_gecikmeleri_s`den türetiyor |
| **B0.4** | **`06` koşul 3** — kontrol payı **zorunlu raporlama** yüklemi | `karsilastirma.py` kontrol payı olmadan karşılaştırma **reddediyor** *(tipli hata)* |
| **B0.5** | **A-14** — `karsilastirma.py` bağımsız denetimi | Bulgu listesi + her düzeltme **mutasyonla** doğrulanmış |
| **B0.6** | **F-4** — `08`in iki sayısı yeniden ölçülür | `08` md 31 ve Ç4'ün üretici komutları **koşuyor** |
| — | **B-57** | 🟢 **beyanlı kapalı** — K-053 komut uydurmayı yasaklıyor; iş yok |
| — | **Li seviye 4** | 🟢 **beyanlı kapalı** — *"açıklanamamıştır"* zaten yazılı; iş yok |

🔒 **B0 kapanış ölçütü:** `13-AILE0-KAPANIS-KANITI.md`'nin dört kanıt
tablosunda **kırmızı satır kalmaması** *(beyanlı olanlar hariç)*.

## 2.2 🔴 B1 · KAT 4 ALTYAPISI — **YENİ BLOK, en kritik**

**Süre: 4,5–8 efektif gün**

🔴 **Kod yazılmadan önce yapı anlatılıp onay alınacak** *(kural 8)*.
Aşağıdaki **taslak** arayüzdür, karar değil:

| # | iş | taslak | doğrulama ölçütü |
|---|---|---|---|
| **B1.1** | **Protokol-kaynaklı kontrol çerçevesi** — yayın **ve** unicast | `gonder_kontrol(hedef \| None, tip, yuk)` | Gönderilen her kontrol çerçevesi `kontrol_bayt` **ve** `kontrol_airtime_s`e yazılıyor; **deftere girmiyor** |
| **B1.2** | **Protokol zamanlayıcısı** | `zamanlayici_kur(gecikme_s, etiket)` + `zamanlayici_calindi` kancası | Zamanlayıcı olayı `Olaylar`a giriyor; **ölçüm penceresi dışında tetiklenmiyor** |
| **B1.3** | **Kontrol paketi alımı** | `kontrol_alindi(gonderen, tip, yuk)` kancası + `KontrolGorunumu` | 🔴 Gözlem sözleşmesi taraması **yasak tipe ulaşamıyor** *(Ç5 yeniden koşar)* |
| **B1.4** | **Çoklu periyot** — HELLO ≠ TC | protokol kendi zamanlayıcısını kurar *(B1.2 ile çözülür)* | OLSR 2 s HELLO + 5 s TC üretebiliyor |
| **B1.5** | 🔴 **ŞEMA GENİŞLETME — son kez** | kontrol paketi sayaçları *(tip başına)* · **PSR** · **üç kopma sayacı** · **Δ** · **COR** · 🆕 **`kosu_kimligi`** *(B-133)* · 🆕 **`arac_hash`** *(B-164)* | `test_b105_pencere_aynasi_*` yeni alanlar için de geçiyor **ve** aynı kod sürümünde iki kez koşan bir araç `.jsonl`de ayırt edilebiliyor |
| **B1.6** | Testler | mutasyon + gözlem sözleşmesi | Her yeni kanca için **en az bir mutasyon yakalanıyor** *(Y2)* |

🔒 **B1 kapanış ölçütü:** *"kontrol paketi gönderen ve zamanlayıcı kuran
bir oyuncak protokol yazıldı, gözlem sözleşmesini geçti, kontrol baytı
faturalandı, korunum 540/540 tuttu."*

⚠️ **B1.5 ŞEMANIN SON GENİŞLEMESİDİR.** Bundan sonra donar — Faz 1
başladıktan sonra eklenen alan eski satırları karşılaştırılamaz yapar.
🔴 **Bu yüzden Faz 1'in ve Faz 2'nin isteyeceği HER sayaç burada
düşünülmeli.** Bu belgenin varlık sebebi budur.

## 🔒 B1.5'İN İKİ KİMLİK ALANI — **B-133 · B-164**

Bunlar metrik değil **kimlik** alanlarıdır ve bir daha eklenemezler.

| alan | ne çözer | ölçülmüş kanıt |
|---|---|---|
| **`kosu_kimligi`** | Sonuç satırı **koşuyu tanımlamıyor** *(B-133, `08` md 36)*: `kaynak_hash` **kod sürümünü** ayırır, koşuyu ayırmaz. Aynı kod sürümünde iki kez koşan bir araç `.jsonl`de **ayırt edilemez** ve dosyalar `append` ile büyür | `pencere_kapsami.jsonl` **üç** hash taşıyor; `gecerlilik.jsonl`de `0a1a94e5…` altında **480 satır ama 240 eşsiz anahtar** — aynı anahtar **2×** |
| 🆕 **`arac_hash`** | `kaynak_hash` **yalnızca `sim/`i** kapsıyor *(B-164)*; `dogrulama/` **araç sürümü hiçbir sonuç satırında yok**. Bir sonucun hangi analiz koduyla üretildiği yeniden kurulamıyor | Bu oturum onu **birinci elden yaşadı**: `sim/karsilastirma.py`ye tek yorum eklendi, hash `fc73905b…` → `01cedf62…` oldu ve `sim/` dışındaki her şey aynı kalmasına rağmen bütün çapa verisi *"bayat"* sayıldı |

🔴 **Yanlış okumanın büyüklüğü ölçüldü:** aynı satırlar 2× okunursa
`8/30 · p = 0,0161` → `16/60 · p = 0,000394` — **41 kat**. Üçüncü kopyada
`p = 0,0000109`. Yani koşu kimliği olmayan bir dosya, **anlamlılığı
uydurabilir**.

⚖️ **Neden B1.5, daha erken değil:** ikisi de **şema alanıdır** ve şema
B1.5'te son kez genişliyor. Şimdi eklenirse tüm mevcut `.jsonl` satırları
alansız kalır ama **karşılaştırılabilir** olmaya devam eder *(alan
`None`)*; B1.5'ten sonra eklenirse eski satırlar **karşılaştırılamaz**
olur.

## 2.3 B2 · KAPI 7. KOŞUSU

**Süre: koşu 3,2–7,3 saat** *(**194–435 dk**)* + 0,5 gün hazırlık

> ## 🔴 BAND YENİDEN YAZILDI — **B-167** *(sekizinci denetim, B0.9)*
> İlan edilen **165–330 dk** üst uçta tutmuyordu. Deponun **kendi**
> sabitleriyle hesaplandı *(`CEKISME_CARPANI = 1,80` ·
> `TEST_BASINA_EN_KOTU_S = 4,3854` · `Pool(8)` · ⌈41/8⌉ = 6 dalga)*:
>
> | taban | Ç1.3 | + Ç1/Ç2…Ç6 *(~11 dk)* |
> |---|---|---|
> | **929 sn** *(3 Eyl · 492 test)* | 183 dk | **~194 dk** |
> | **2 158 sn** *(492 × 4,3854 — en kötü)* | 424 dk | 🔴 **~435 dk** |
>
> ⚖️ Bu bir *"eşiği gevşetme"* değil *(`03` kural 3)*: eşik değil
> **maliyet tahmini**, ve düzeltme onu **büyütüyor** — kural 7'nin
> *"30 dk'yı aşarsa SOR"* kapısını **güçlendiriyor**.

| doğrulama ölçütü |
|---|
| 13/13 · **ve `aile0_kapi_raporu.jsonl` boş değil** *(D-13'ün kanıtı)* |
| Yeni `kaynak_hash` `04`e yazılır — bundan sonraki her sonuç ona bağlanır |

🔴 **Kapı, B0 **ve** B1 bittikten sonra TEK KEZ koşulur.** İkisini ayrı
koşturmak 6–11 saat eder ve kazancı yoktur.

## 2.4 B3 · FAZ 1 — ÜÇ RAKİP PROTOKOL

**Süre: 10,5–16,5 efektif gün**

| # | protokol | süre | doğrulama ölçütü |
|---|---|---|---|
| **B3.1** | **AODV** *(RFC 3561)* | 3–5 | **U1–U4** *(`06` §4.2)* |
| **B3.2** | **OLSR** *(RFC 3626, MPR dâhil)* | 4–6 | **U1–U4** |
| **B3.3** | **AOMDV** *(AODV uzantısı)* | 1,5–2,5 | **U1–U4** + yedek yolun **fiilen devreye girdiği** ölçülüyor |
| **B3.4** | Uygunluk test paketi | 2–3 | Üç protokol × dört test **geçiyor** |

🔒 **Bir protokol U1–U4'ü geçmeden "kuruldu" sayılmaz** *(kural 4 revizyonu:
sadakat, ayarlama değil)*.

⚠️ **Ölçülmüş referansımız yok:** MPR seçimi ve protokol uygunluk testleri
bu depoda **hiç yapılmadı**. Bantlar geniş ve **güven aralığım dar değil.**

## 2.5 B4 · MÜHÜR HAZIRLIĞI

**Süre: 2,5–3,5 efektif gün**

| # | iş | doğrulama ölçütü |
|---|---|---|
| **B4.1** | **İstatistik katmanı** *(R-2)* — Wilcoxon · Holm · Clopper–Pearson · **NaN açık kontrolü** | Regresyon testi **n=30 gerçek örneklemle** yazılmış |
| **B4.2** | **Gürültü ölçümü** — yalnız rakip kollar, tohum 1–30 | Tohumlar arası std **ölçüldü ve yazıldı** |
| **B4.3** | **Güç analizi + eşikler** | *"30 tohumda %80 güçle görülebilen en küçük etki"* hesaplandı |
| **B4.4** | **Karıştırıcı konum kararı** *(J-merkez/kenar/hedef)* | Üç konumun ölçülmüş etkisi tabloda; birincil nokta seçildi |
| **B4.5** | 🔒 **`06` ve `08` MÜHÜRLENİR** | Aile 1/2/3 eşikleri yazıldı; `08`in **37** maddesi donduruldu |

## 2.6 B5 · FAZ 2 — ÖZGÜN PROTOKOL

**Süre: 🔴 TASARIM GELMEDEN FİYATLANAMAZ.** Kaba bant: **6–10 efektif gün**
*(protokol 5–8 + ablasyon kolu 1–2)*.

| # | iş | doğrulama ölçütü |
|---|---|---|
| **B5.1** | Tasarım `06` §5.1'e yazılır | 🔴 **Öğrenciden gelir** — danışman doldurmaz |
| **B5.2** | Uygulama | Kâhin yasağı taraması geçiyor · parametreler **mühürden önce sabit** |
| **B5.3** | **Ablasyon kolu** — bilgi kanalı permüte | Bayrakla üretiliyor, kod düzenlemesiyle değil |
| **B5.4** | **Mekanizma kapısı** | ≥7/8 pozitif · %95 GA sıfırı dışlıyor |

🔴 **Mekanizma kapısı geçmezse Aile 2'nin sonucuna BAKILMAZ** — ve o
noktada süre öngörülemez. **Takvimin tek gerçek belirsizliği budur.**

## 2.7 B6 · DENEY VE ANALİZ

**Süre: 3–4 efektif gün** · koşu **~1–2 saat**

| matris | koşu | tahmin |
|---|---|---|
| Ana deney *(4 kol × 6 senaryo × 3 trafik × 30 tohum)* | 2 160 | **33–69 dk** |
| H1.2 dirsek taraması | 960 | 15–31 dk |
| Karıştırıcı konum ekseni *(3 konum × 4 kol × 30 tohum)* | 360 | 6–13 dk |
| Mekanizma kapısı *(kol başına)* | 48 | 13–27 dk |

🟢 **Koşu takvimin darboğazı DEĞİL** — ölçülmüş taban: 300 koşu **4,3 dk**.

## 2.8 B7 · FAZ 3 — YAZIM

**Süre: 4–6 hafta takvim.** 🔒 **Yeni deney yok.**

---

# 3 · 🔴 TAKVİM ÇAKIŞMASI — dürüst hesap

## 3.1 Toplam

| blok | efektif gün |
|---|---|
| B0 · Faz 0 geçerlilik | 4–5 |
| **B1 · Kat 4 altyapısı** | **4,5–8** |
| B2 · Kapı *(koşu)* | 0,5 |
| B3 · Üç protokol | 10,5–16,5 |
| B4 · Mühür hazırlığı | 2,5–3,5 |
| **Mühre kadar ARA TOPLAM** | **22–33,5** |
| B5 · Özgün protokol | 6–10 *(tahmini)* |
| B6 · Deney + analiz | 3–4 |
| **GENEL TOPLAM** | **31–47,5 efektif gün** |

## 3.2 🔴 26 EYLÜL MÜHRÜ **TUTMUYOR**

26 Eylül'e **25 takvim günü** var; mühre kadar gereken **22–33,5 efektif
gün**. Bu, günde **~1 efektif gün** çalışmayı gerektirir — tam zamanlı
çalışan biri için gerçekçi değil.

| çalışma temposu | mühre kadar takvim günü | mühür tarihi |
|---|---|---|
| 0,7 efektif gün/gün *(çok yoğun)* | 31–48 | **2 Ekim – 19 Ekim** |
| 0,5 efektif gün/gün *(gerçekçi)* | 44–67 | **15 Ekim – 7 Kasım** |
| 0,35 efektif gün/gün *(rahat)* | 63–96 | 3 Kasım – 6 Aralık 🔴 |

🔴 **Ve mühür, işin sonu değil ortası:** B5+B6 için **9–14 efektif gün**
daha gerekiyor, ve yazım **4–6 hafta** istiyor.

⚖️ **19 Aralık − 5 hafta = 14 Kasım.** Yani B6, **14 Kasım'a kadar**
bitmiş olmalı. 0,5 tempoda genel toplam *(31–47,5)* **62–95 takvim günü**
eder → **2 Kasım – 5 Aralık**. **İyimser uçta sığıyor, kötümser uçta
sığmıyor.**

🔴 **Bu bir tahmin değil, bir uyarıdır: mevcut kapsam takvime PAYSIZ
oturuyor.**

---

# 4 · 🔒 KAPSAM SEÇENEKLERİ — ölçülmüş kazançla

Karar öğrencinindir. Dördü birleştirilebilir.

| # | seçenek | kazanç | bedel |
|---|---|---|---|
| **S1** | 🟢 **Yazımı PARALEL başlat** — yöntem · araç doğrulama · literatür bölümleri **sonuç gerektirmiyor** | **2–3 hafta takvim** | yok — 31 Ekim zaten *"yeni deney yok"* demek |
| **S2** | 🟢 **Kat 4 altyapısını MİNİMAL tut** — genel mesajlaşma çerçevesi değil, yalnız AODV/OLSR'ın istediği | **1–2 efektif gün** | ileride yeni protokol eklenirse arayüz büyür |
| **S3** | 🔒 **Mühür tarihini taşı** — 26 Eylül → **~20 Ekim** | takvim gerçekçi olur | ⚠️ `06` Bölüm 10'a **gerekçesiyle** yazılır |
| **S4** | 🟡 **AOMDV'yi düşür** *(2 protokol)* | 1,5–2,5 efektif gün | Boşluk A daha dar doldurulur; çok-yollu hipotez düşer |

## 4.1 🟢 ÖNERİM: **S1 + S2 + S3**, S4 yedekte

**Gerekçe:**

1. **S1 bedava.** Raporun üç bölümü *(yöntem · araç doğrulama · literatür
   boşluğu)* bugün yazılabilir — `10` ve `13` zaten o bölümlerin ham
   malzemesi. Bu, en büyük tek kazanç ve **hiçbir riski yok**.
2. **S2 ucuz ve doğru.** Genel bir mesajlaşma çerçevesi yazmak, `03`ün
   *"istenmeyen soyutlama"* uyarısına girer. AODV/OLSR ne istiyorsa o.
3. **S3 kaçınılmaz.** Mühür tarihi **bizim koyduğumuz** bir tarih, TÜBİTAK'ın
   değil. Tutmayacak bir tarihi tutuyormuş gibi yapmak, `03` kural 3'ün
   *("eşiği geriye dönük gevşetme")* ters yönü olur — **şimdi taşımak
   dürüst, sonra kaçırmak değil.**
4. **S4 yedekte kalsın.** AOMDV en ucuz protokol *(1,5–2,5 gün)* ve
   **ön-kayıtlı bir öngörüyü** sınıyor *(`06` §4.1: tek karıştırıcıda
   çok-yolluluğun avantajı kaybolmalı)*. Erken atılmamalı; **15 Ekim'de
   B3.3 başlamamışsa** düşürülür.

---

# 5 · 🔒 "GERİYE DÖNMEME" SÖZLEŞMESİ

Öğrencinin asıl talebi buydu. Geriye dönüşü zorunlu kılan **üç olay** var
ve üçü de **önlenebilir**:

| # | geri dönüş sebebi | önlemi | ne zaman |
|---|---|---|---|
| **1** | Şemaya sonradan alan eklemek | 🔒 **B1.5 şemanın SON genişlemesi** — Faz 1 ve Faz 2'nin isteyeceği her sayaç orada düşünülür | B1 |
| **2** | Arayüz protokoller yazıldıktan sonra değişmek | 🔒 **B1 önce, B3 sonra** — ve B1 bir **oyuncak protokolle** doğrulanır | B1→B3 |
| **3** | `06`nın mühürlenmesinden sonra hipotez/eşik değiştirmek | 🔒 **Mühür, rakipler ölçüldükten SONRA** — bu yüzden S3 gerekli | B4 |

## 5.1 🔴 B1.5'İN KONTROL LİSTESİ — şema son kez genişlerken

Faz 1 ve Faz 2'nin isteyeceği **her** sayaç burada olmalı:

| sayaç | kim ister | kaynak |
|---|---|---|
| **PSR** *(MAC'te gönderilebilen / istenen)* | Aile 1 | literatürün **asgari** metrik kümesi |
| Kontrol paketi **tip başına** sayaç *(RREQ/RREP/RERR/HELLO/TC)* | Aile 1 | NRL ve proaktif-reaktif asimetrisi |
| **Üç kopma sayacı** *(fiziksel · protokol-algılamalı · rota geçersizleşme)* | Aile 1 | protokolün **algılama duyarlılığı** |
| **Δ** *(rota kurtarma gecikmesi)* | Aile 1 | 🔴 literatürün **ikinci boşluğu** |
| **COR** *(kurtarılan/etkilenen yol)* | Aile 1 | Δ'nın tamamlayıcısı |
| Ablasyon karar sayaçları | Aile 3 | mekanizma kapısı |
| 🔴 **`teslim_dogum_s`** | Aile 1 | 🔴 **IPDV türetilemiyor**: varış = doğum + gecikme ve `dogum_s` satırda YOK *(K-085, ölçüldü)* |
| 🔴 **"MAC'e verilen paket" sayacı** | Aile 1 | 🔴 **PSR türetilemiyor**: `mac_gonderilen` **=** `mac_deneme` *(7214 = 7214)* — ikisi de DENEME sayıyor *(K-085, ölçüldü)* |
| 🔴 **koşu kimliği / zaman damgası** | hepsi | 🆕 **B-133** *(yedinci denetim)*: sonuç satırı **koşuyu tanımlamıyor**. `kaynak_hash` kod sürümünü ayırır, **koşuyu ayırmaz** — aynı kod sürümünde iki kez koşan bir araç `.jsonl`de **ayırt edilemez** *(bugün `pencere_kapsami.jsonl`de birden çok koşu üst üste duruyor)*. 🔴 Şema donduktan sonra **eklenemez** |
| 🔴 **Özgün protokolün isteyeceği** | Faz 2 | **tasarım gelmeden bilinemez** |

🔴 **SON SATIR EN RİSKLİ OLANI.** Özgün protokolün tasarımı gelmeden şema
donarsa, tasarım yeni bir sayaç isterse **geriye dönülür.**

🔒 **Bu yüzden tek bir şart var:** **B1.5, özgün protokolün tasarım
taslağı geldikten SONRA kapatılır.** Tasarımın tamamlanmış olması gerekmez
— *hangi büyüklükleri ölçmek isteyeceğinin* bilinmesi yeter.

⚖️ **Bu, takvimde bir bağımlılık yaratıyor:** B1 → B3 → B4 zinciri,
öğrencinin tasarım taslağını **B1 bitmeden** vermesini gerektiriyor.

---

# 6 · ÖNERİLEN SIRA — bağımlılıklarla

```
  🔒 ONAY 1  (bu plan)
      │
      ├─ S1: YAZIM PARALEL BAŞLAR ────────────────────────► (sürekli)
      │      yöntem · araç doğrulama · literatür boşluğu
      │
      ├─ B0  Faz 0 geçerlilik (4–5 g)
      │        │
      │        └─ 🔴 ÖĞRENCİ: özgün protokol TASARIM TASLAĞI
      │             (hangi büyüklükleri ölçecek?)
      │                    │
      ├─────────────────── ▼
      ├─ B1  Kat 4 altyapısı + ŞEMA SON GENİŞLEME (4,5–8 g)
      │        └─ 🔒 ONAY 2 (arayüz yapısı — kural 8)
      │
      ├─ B2  KAPI 7. koşusu (3–5,5 sa)   ← B0 ve B1 birlikte
      │
      ├─ B3  Üç protokol + U1–U4 (10,5–16,5 g)
      │
      ├─ B4  İstatistik + gürültü + güç + eşikler (2,5–3,5 g)
      │        └─ 🔒 `06` ve `08` MÜHÜRLENİR (~20 Ekim)
      │
      ├─ B5  Özgün protokol + ablasyon (6–10 g)
      │        └─ 🔒 Mekanizma kapısı — geçmezse sonuca BAKILMAZ
      │
      ├─ B6  Ana deney + analiz (3–4 g · koşu 1–2 sa)
      │
      └─ B7  Yazımın tamamlanması (S1 sayesinde kısalmış)
              → 19 Aralık
```

---

# 7 · ERKEN UYARI GÖSTERGELERİ

| gösterge | eşik | tetiklenirse |
|---|---|---|
| **Özgün protokol tasarım taslağı** | **10 Eylül**'de gelmemişse | 🔴 B1.5 şemayı **eksik** dondurur → geri dönüş riski |
| **B1 (Kat 4)** | 25 Eylül'de bitmemişse | S2'ye geç *(minimal arayüz)* |
| **B3.1+B3.2 (AODV+OLSR)** | 15 Ekim'de bitmemişse | 🔴 **S4** — AOMDV düşer |
| **Mekanizma kapısı** | Aile 3'te geçmezse | 🔴 sonuca bakılmaz — süre öngörülemez |
| **B6 (ana deney)** | **14 Kasım**'da bitmemişse | 🔴 yazım süresi 5 haftanın altına iner |
| **TÜBİTAK rehberi** | 10 Ekim'de indirilmemişse | `01` §4 matrisi doğrulanmamış kalır |

---

# 8 · 🔴 KAYMA PLANI — ne, hangi sırayla düşer

| sıra | düşen | kaybedilen | korunan |
|---|---|---|---|
| **1** | **AOMDV** *(S4)* | çok-yollu hipotez · Boşluk A daralır | AODV+OLSR karşılaştırması tam |
| **2** | **Δ ve COR ölçümü** | literatürün ikinci boşluğu | PDR/E2E/NRL üçlüsü tam |
| **3** | **Karıştırıcı konum ekseni** *(J-kenar/J-hedef)* | gerçekçilik argümanı zayıflar | J-merkez + **beyan** kalır |
| **4** | **H1.2'nin tarama çözünürlüğü** *(8 → 5 nokta)* | dirseğin keskinliği | dirseğin varlığı |
| **5** | 🔴 **HİÇBİR ZAMAN:** ≥30 tohum · Holm · ön-kayıtlı eşikler · kapsam beyanı · korunum · **kâhin yasağı** · **sadakat kuralı** | — | — |

🔴 **Beşinci satır pazarlığa kapalıdır.** Bir kural takvim yüzünden ihlal
edilirse projenin tek gerçek varlığı kaybolur.

---

# 9 · ÖZET — üç cümle

1. 🔴 **Faz 0, sanılandan büyük:** 8 geçerlilik kalemine ek olarak
   **Kat 4 altyapısı** var, ve o olmadan üç protokolün hiçbiri yazılamaz.
2. 🔴 **26 Eylül mührü tutmuyor.** Ölçülmüş gereksinim 22–33,5 efektif gün;
   kalan 25 takvim günü. **Öneri: ~20 Ekim'e taşı ve yazımı paralel başlat.**
3. 🔒 **Geriye dönmemenin tek şartı:** şema **B1.5'te son kez** genişler ve
   o an özgün protokolün **hangi büyüklükleri ölçeceği bilinmelidir** —
   bu yüzden tasarım taslağı **10 Eylül'e kadar** gerekli.

> **Bir şeyi büyütmek istiyorsan önce ölç.** Bu belge, büyütmeden önce
> ölçtü — ve ölçüm takvimin tutmadığını söyledi.
