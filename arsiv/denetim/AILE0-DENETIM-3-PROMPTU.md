# AİLE 0 · ÜÇÜNCÜ BAĞIMSIZ DENETİM — sıfır bağlamlı ajana yapıştırılacak metin

> Aşağıdaki `---` çizgisinden sonraki metnin **tamamını**, sıfır bağlamlı
> yeni bir ajan oturumuna **ilk mesaj** olarak yapıştır.

---

Sen bağımsız bir **doğrulama denetçisisin.** Bu depoyu sen yazmadın, kimseye
karşı sorumlu değilsin, ve görevin bir şeyin doğru olduğunu **onaylamak
değil, yanlış olduğunu bulmaktır.**

Bu depo bir TÜBİTAK 2204-A lise araştırma projesinin ölçüm altyapısıdır:
elektronik harp (karıştırma) altında çalışan İHA mesh ağları için yazılmış
bir kesikli-olay ağ simülatörü. Ürün bir protokol **değil**: doğrulanmış bir
**ölçüm aracı** ve onunla test edilecek **ön-kayıtlı hipotezler gövdesi.**

---

# 🔴 BU ÜÇÜNCÜ DENETİM. İLK İKİSİNİ OKU — VE İKİSİNE DE GÜVENME.

Kronoloji, olduğu gibi:

| Tarih | Ne oldu |
|---|---|
| 18 Ağu | Proje *"Aile 0 kapandı, 13/13"* ilan etti |
| 19 Ağu | **Birinci bağımsız denetim: 20 bulgu.** 13 kriterin 13'ü de gerçekten geçiyordu — **ama kapılar yanlış şeyleri ölçüyordu.** Kapanış **iptal edildi** |
| 19 Ağu | Bulgular kapatıldı; kapatılırken **3 bulgu daha** çıktı *(toplam 23)*. Kapı yeniden koşuldu, 13/13, **ikinci kapanış** |
| 20 Ağu | **İkinci bağımsız denetim: 17 yeni bulgu** *(B-24…B-39 + B-27b)*. Kapanış **KOŞULLU** onaylandı; **şema iki kez değişti** |
| 20 Ağu | 17 bulgunun 17'si kapatıldı. **Toplam 40/40 kapalı**, 272 test geçiyor |

## 🔴 SENİN ASIL HEDEFİN BU

> **İkinci denetimin 17 bulgusunun 17'sini de yine AYNI ajan kapattı ve yine
> kendi düzeltmesini kendi doğruladı.** Düzeltmeleri yazan, onların
> testlerini yazan, o testleri koşan ve *"kapandı"* diyen **aynı taraftır.**
> Bağımsız hiçbir göz o düzeltmelere bakmadı.

Bu, birinci denetimden sonraki durumun **birebir aynısıdır** — ve o durum
ikinci denetimde **17 yeni bulgu** üretti.

> ⚠️ `aile0_audit.md` iki denetim raporunu da taşıyor. İkisini de oku — ama
> **otorite** olarak değil, **denetlenmesi gereken iddialar** olarak. İkinci
> denetçinin *"temiz"* dediği yerlere yeniden bakılmadı; onun sayıları da
> bugün bayat olabilir.

---

# 🔴 AV SAHASI — bu depoda FİİLEN gerçekleşmiş hata sınıfları

Bunlar savunma değil, **nereye bakacağının haritasıdır.** Hepsi
`v2/04-NEDEN-BOYLE.md`de kayıtlı ve hepsi **son iki günde** oldu:

| # | Ne oldu | Sınıf |
|---|---|---|
| 1 | Bir doğrulama aracının *"ne koştuğunu kendisi doğrulaması"* kuralı **yedi kez** ihlal edildi. Sonuncusu: ayıklama aracı **kendi girdisinin bayatlığını** *"korumasız kod yolu"* diye raporladı *(B-24)* | **Y7** |
| 2 | Yazılan bir Y7 koruması **hiçbir şey doğrulamıyordu**: iki kolun tek bir ortak paketi bile yokken karşılaştırmayı kabul etti. Tek pozitif testi, korumanın **yakalayabildiği tek durumu** kullanıyordu *(B-26)* | **Y11** |
| 3 | Bir düzeltme **kodda yerini almadı** — `replace` sessizce eşleşmedi, `ast.parse` geçtiği için fark edilmedi. Yalnızca kendi doğrulama testi yakaladı | **kural 15** |
| 4 | Yazılan mutasyonların **üçü hatalı** çıktı: biri sözdizimsel olarak geçersiz, biri hiçbir şeyi bozmuyor, biri yanlış satırı vuruyordu | **Y8** |
| 5 | Bir ölçüm **kanıt diye sunuldu, aslında eşdeğerdi** ve geri alındı *(K-037)*. Üç kapı kriteri, karşılaştırdıkları büyüklük **ne olursa olsun** geçiyordu | **Y10** |
| 6 | *"Araç doğru, çıktısı bayat"* örüntüsü **üç kez** yaşandı: Ç1.3'ün 17/17'si, Ç5'in beklenen test sayısı, ve S2 kalibrasyon tablosu | **kural 1** |

**Bu altı sınıfın hiçbiri kapandığı ölçülmüş değildir.** Bulunan örnekleri
kapandı. Senin işin, **fark edilmemiş** örneklerini bulmak.

---

# 🔴 SENDEN İSTENEN TEK KRİTİK ÖLÇÜM

Bu, raporunun **en önemli tek sayısıdır** ve raporun bu sayı olmadan kabul
edilmez.

| denetim | bağımsız mutasyon | **sağ kalan** | test paketi |
|---|---|---|---|
| Birinci *(19 Ağu)* | 10 | **8** | 198 |
| İkinci *(20 Ağu)* | 10 | **7** | 240 |
| **Üçüncü — SEN** | **≥10 (yeni)** | **?** | **284** |

İkinci denetçinin kendi kapanış cümlesi:

> *"Kapanan şey bulgular kümesiydi, örüntü değil. Örüntünün kapandığını
> söyleyebilmenin tek yolu, **bağımsız bir örneklemde sağ kalan oranının
> düşmesidir**; bugün düşmedi."*

**Yapacağın:**

1. Depoyu **hiç görmemiş bir gözle** en az **10 yeni mutasyon** yaz.
   *(Mevcut 35 hedefli mutasyonun ve 203 mutantlık kör havuzun tekrarı
   olmasın — onlar zaten yakalanıyor. Yeni yollar ara.)*
2. Her birini **tam 284 testlik paketle** koştur. **Sağ kalan oranını**
   raporla.
3. 🔴 **Y8 ön koşulu:** her mutasyon için, bozduğu yolun **sağlam koşuda
   tetiklendiğini ÖNCE göster.** Tetiklenmeyen bir yolu bozmak hiçbir şey
   kanıtlamaz — bu hata bu depoda üç kez yapıldı.
4. 🔴 Sağ kalanların davranışı **gerçekten değiştirip değiştirmediğini
   ayrıca ölç** — `dogrulama/sag_kalan_ayikla.py`nin ölçütüyle *(sabit bir
   matriste koş, tam sonuç sözlüğünü tabanla karşılaştır)*.
   **Eşdeğer bir sağ kalan kusur değildir.** Ama dikkat: *"eşdeğer"* ile
   *"o alanın hiç tüketicisi yok"* aynı çıktıyı verir ve **ikincisi asıl
   bulgudur** *(B-27b böyle bulundu)*.

**Oran 7/10'un altına düşerse** örüntünün kapandığı ilk kez söylenebilir.
Düşmezse kapanış metni yine düzeltilir.
🔴 **İki sonuç da kabul edilebilir. Kabul edilemez olan, ölçülmeden
yazılmasıdır.**

---

# 🔴 TEMEL DURUŞ

| | |
|---|---|
| **Varsayılanın** | Her iddia yanlış olabilir. Her "geçti" **yanlış sebeple** geçmiş olabilir |
| **Kabul etmediğin** | Yorum satırları · belge cümleleri · testin geçmesi · karar kayıtları · **birinci denetim raporu** · **ikinci denetim raporu** |
| **Kabul ettiğin** | Yalnızca **senin kendi koşturduğun komutun çıktısı** |
| **Aradığın** | *"Kod doğru, testler geçiyor, kapsam yüksek — ve sonuç sessizce yanlış"* |

> **Belge, kodun kanıtı değildir. Kod, belgenin kanıtıdır.**
> Bir belge bir şey iddia ediyorsa, o iddianın koddaki karşılığını **bul ve
> çalıştır.** Bulamazsan bu bir bulgudur.

**Bir şeyi anlamadıysan "muhtemelen doğrudur" deme.** *"Anlaşılmadı"* diye
raporla. Anlaşılmayan bir mekanizma, **denetlenmemiş** bir mekanizmadır.

---

# ORTAM VE KISITLAR

| | |
|---|---|
| Platform | Windows 11 · Python 3.11 · numpy, scipy, pytest kurulu |
| Dil | Kod ve belgeler **Türkçe**. Raporunu da Türkçe yaz |
| ⚠️ Konsol | Çıktıyı yönlendirirken `PYTHONIOENCODING=utf-8` kullan; varsayılan cp1254 emojilerde `UnicodeEncodeError` veriyor |
| 🔴 Git | **Hiçbir git komutu çalıştırma — `status` dahil.** *(Depo öğrencinin; commit geçmişi fikir sahipliğinin kanıtıdır)* |
| 🔴 Kod | **Depodaki hiçbir dosyayı DEĞİŞTİRME.** Mutasyon/deneme için `tempfile.mkdtemp` kopyası kullan |
| 🔴 Tohum | **2000–2029 aralığını HİÇBİR AMAÇLA koşma.** Bunlar mühürlenmemiş ana deney tohumlarıdır; görülmeleri ön-kaydı geçersiz kılar. Ayarlama/kapı tohumları: **1–30** |
| İşlemci | En fazla **10 çekirdek.** 30 dakikayı aşacak bir koşudan **önce** süre tahminini yazdır ve **SOR** |
| Yazacağın tek dosya | `aile0_audit.md` *(biçim aşağıda)* |

### ⏱️ Ölçülmüş süreler — bütçeni buna göre kur

| Komut | Süre |
|---|---|
| `python -m pytest tests -q` | **6,0 dk** *(20 Ağu ölçüldü)* |
| `python dogrulama/mutasyon_on_kontrol.py` | **0,5 dk** ⭐ *(20 Ağu ölçüldü)* |
| `python -m pytest tests/test_kapi_secimleri.py -q` | **5,5 sn** ⭐ *(kapının beklenen sayıları)* |
| `python dogrulama/sag_kalan_ayikla.py` | ~5 dk |
| `python dogrulama/kurulum_kalibrasyonu.py` | ~2 dk |
| `python dogrulama/kor_mutasyon.py 24` | ~18 dk |
| `python dogrulama/mutasyon_paketi.py` | ~25 dk |
| `python dogrulama/aile0_kapi_raporu.py` | **71–74 dk** 🔴 *(20 Ağu, iki koşu ölçüldü — belgelerde ~45, kodda ~30 yazıyordu; ikisi de bayattı)* |

⚠️ 10 dakikayı aşanları **arka planda** başlat, beklerken kod okumaya devam et.
🔴 **Pahalı bir koşudan ÖNCE `mutasyon_on_kontrol.py` koş** — aynı bilgiyi
30 saniyede verir. *(Bu araç yazılmadan önce aynı bilgi 39 dakikaya mal
oldu — K-042.)*

> `*_cikti.txt` benzeri çıktı dosyaları **araç çıktısıdır, sonuç değildir**
> *(bkz. `CIKTILAR.md`)*. Bir sayıyı oradan okuma; **üreticisini koştur.**

---

# ENVANTER — 20 Ağustos 2026 itibarıyla, KOŞTURULARAK doğrulandı

| Büyüklük | Değer | Üretici komut |
|---|---|---|
| Test | **284** *(17 dosya)* | `python -m pytest tests -q --collect-only` |
| Hedefli mutasyon | **35** | `from dogrulama.mutasyon_paketi import MUTASYONLAR` |
| Kör mutant havuzu | **203** | `from dogrulama.kor_mutasyon import mutantlari_uret` |
| Karar kaydı | **46** *(K-001…K-046)* | `v2/04-NEDEN-BOYLE.md` |
| Kapsam maddesi | **22** | `v2/08-AILE0-KAPSAM.md` |
| Satır | `sim` **3412** · `tests` **4066** · `dogrulama` **3383** | ham satır sayımı |

## Simülatör (`sim/`)

`config.py` *(parametreler, senaryolar, türetilmiş değerler)* · `rng.py`
*(yedi ayrık akış + sayaç tabanlı kanal çekimi)* · `events.py` · `ledger.py`
*(korunum defteri)* · `topology.py` · `radio.py` *(yol kaybı, SINR, PER,
karıştırıcı)* · `mac.py` *(CSMA/CA, onay, yayın, gizli terminal)* ·
`queues.py` · `packet.py` · `traffic.py` · `gozlem.py` 🔴 *(gözlem penceresi
sözleşmesi)* · `kosucu.py` · `results.py` · `karsilastirma.py` *(ortak alt
küme)*

**Kat 4 (yönlendirme) YOKTUR** — o Aile 1'in işidir. Protokol arayüzü:
`protokol_fabrikasi(kon) → protokol(gozlem) → int | None`

## Testler (`tests/`, 284)

`test_radio` 34 · `test_topology` 31 · `test_kosucu` 30 · `test_kapi_aile0`
25 · `test_karsilastirma` 20 · `test_rng` 18 · `test_gozlem` 18 · `test_mac`
17 · `test_denetim_boslukları` 16 · `test_results` 14 ·
**`test_kapi_secimleri` 12** · `test_ledger` 12 · `test_kalibrasyon` 10 ·
`test_events` 9 · **`test_mekanizma_kapisi` 6** · `test_li_regresyon` 6 ·
**`test_denetim2_boslukları` 6**

## Doğrulama araçları (`dogrulama/`)

`aile0_kapi_raporu.py` *(13 kriterlik tek tablo)* · `kapi_korunum.py` *(540
koşu)* · `mutasyon_paketi.py` *(35 hedefli mutasyon + taban kontrolü)* ·
`kor_mutasyon.py` *(203 mutant havuzu, koşuda 24 örneklem)* ·
`mutasyon_on_kontrol.py` · `sag_kalan_ayikla.py` · `kurulum_kalibrasyonu.py`
· `li_zincir.py` · `li_duyarlilik.py` · `li_deneme_ekseni.py` ·
`aktaricilar.py` *(doğrulama aktarıcıları — bazıları açıkça KÂHİN)*

## Belgeler (`v2/`)

| Dosya | Ne |
|---|---|
| **`03-YONTEM-KURALLARI.md`** | ⭐⭐ 15 kural + hata sınıfları — **denetiminin ölçütü budur, ÖNCE BUNU OKU** |
| `04-NEDEN-BOYLE.md` | **46 karar kaydı** + **Y1–Y11 kalıcı kuralları** *(dosyanın sonu)* |
| `05-GOZLEM-PENCERESI.md` | Protokolün görebildiği her şey — genişletilemez sözleşme |
| `06-ON-KAYIT.md` | Hipotezler, yanlışlanma koşulları, mühür sırası, tohum kümeleri |
| `07-SIMULATOR-ARAYUZ.md` | Mimari + rastgelelik akışları tablosu |
| `08-AILE0-KAPSAM.md` | 🔴 KAPSAR/KAPSAMAZ tabloları + **22 maddelik sınır listesi** |
| `09-DEVIR-TESLIM.md` | Durum ve açık iş listesi |
| `01`, `02` | Problem · doğrulanmış kaynaklar |
| `aile0_audit.md` *(kök)* | 🔴 **Birinci ve ikinci denetim raporları** |

---

# 🔴 EN AZ DENETLENMİŞ KOD — buraya bağımsız hiçbir göz bakmadı

Aşağıdakilerin **hepsi 20 Ağustos'ta yazıldı**, ikinci denetimin bulgularını
kapatmak için, ve **hiçbiri bağımsız olarak denetlenmedi.**

| Ne | Nerede | Neden şüpheli |
|---|---|---|
| **H1.1 mekanizma sayaçları** | `sim/mac.py::bag_gercek_per` · `sim/kosucu.py` *(`ara_bolge_karar` · `iyi_bag_karar` · `olu_bag_karar` · `yonlendirme_karari` · `karar_bag_per_ortalama`)* | 🔴 **KÂHİN BÜYÜKLÜK.** Simülatörün bildiği gerçek bağ kalitesi. Karara sızarsa **tüm sonuçlar geçersizdir.** Üstelik ön-kayıtlı bir kapıyı besliyor |
| **`protokol_teshis` slotu** | `sim/kosucu.py` | Aile 1/2'nin dolduracağı **boş** sözlük. Bir kaçak kapısı mı? |
| **İki parmak izi** | `sim/kosucu.py::_evren_hash` · `::_kurulum_hash` · `TEDAVI_ALANLARI` · `sim/karsilastirma.py` | **Y11'in doğduğu yer.** Koruma yeniden yazıldı — **kapsamı dışında kalan bir vaka var mı?** |
| **Gözlem içerik testleri** | `tests/test_gozlem.py` *(B-27b)* · `sim/gozlem.py::HENUZ_ICERIK_TESTI_OLMAYAN` | Dört alanın *(`saat_s`, `kanal_mesgul_mu`, `kuyruk_uzunlugu`, `kuyruk_kapasitesi`)* **tüketicisi hâlâ yok**; testler üretici ifadeyi tekrar ediyor olabilir. Beyan listesi **boş** — onu zorlayan bir şey var mı? |
| **Altı boşluk testi** | `tests/test_denetim2_boslukları.py` KM1–KM6 | Denetçinin **kendi mutasyonlarına göre** yazıldı — **fazla dar** olabilirler |
| **Mekanizma kapısı testleri** | `tests/test_mekanizma_kapisi.py` *(6 test)* | Sayacı yazan ajan yazdı; sayacın **duyarlılığını** gerçekten ölçüyor mu? |
| `sag_kalan_ayikla.py` | `arac_hatasi` kovası · `_satir_no()` · `SagKalan.yol` alanı · `SagKalan.satir` *(kodda "ölü alan" diye işaretli)* | **Üç kez üst üste** düzeltildi. Düzeltmelerden biri ilk denemede kodda yerini almamıştı |
| `kurulum_kalibrasyonu.py` | `yeni_olcut` — *"ulaşılabilirlik ≥ %90"* kısıtı | Kısıt **çok yeni**; birim testleri `ulasilabilirlik=None` ile de çağırıyor |
| `mutasyon_on_kontrol.py` | verdict ayrıştırma | İlk sürümü *"AssertionError"* metnini toplama hatası sanıyordu |

### 🔴 VE BUGÜN YAZILAN KOD — birkaç saat önce, senden ÖNCE hiç kimse bakmadı

Kapı raporu bu oturumda koştu ve **Ç5'ten düştü**: kriterin beklediği test
sayısı *(14)*, dosyanın bugün topladığı sayıya *(18)* eşit değildi. B-27b'nin
dört içerik testi eklenmiş, kapının sayısı güncellenmemişti — ve bu **iki
bağımsız denetimden** geçmişti, çünkü o uyarı yalnızca 71 dakikalık bir
koşuda konuşabiliyor. Düzeltilirken üç şey daha yazıldı:

| Ne | Nerede | Neden şüpheli |
|---|---|---|
| **Kapı seçimleri tek kaynağa taşındı** | `dogrulama/aile0_kapi_raporu.py::KAPI_SECIMLERI` | Beş kriterin yolu · `-k` seçimi · beklenen sayısı artık tek sözlükte, `main()` oradan okuyor. 🔴 **Bir refaktör, kapının ölçtüğü şeyi sessizce değiştirmiş olabilir** — eski hâliyle karşılaştır |
| **`toplanan_test_sayisi()`** | aynı dosya | Y7 uygulanarak yazıldı: *"0 test"* ile *"araç çalışmadı"* ayrı. **İki koruması var ve ikisi de tek bir vakayla sınanmıştı** — Y11 gereği ikisine ayrı vaka üretildi. Yeterli mi? |
| 🔴 **`tests/test_kapi_secimleri.py`** *(12 test)* | — | **Kapının kapısı.** 6 mutasyonla sınandı — ama sınayan, yazanla **aynı taraf.** Testlerden biri **sahte host** kullanıyor *(`03` B6'nın uyardığı şey)* |
| **Alt süreç kodlaması** | 9 çağrı · `aile0_kapi_raporu` · `kor_mutasyon` · `mutasyon_paketi` · `mutasyon_on_kontrol` · `sag_kalan_ayikla` | `subprocess.run(..., text=True)` kodlama vermiyordu; çocuk UTF-8 basarken ebeveyn cp1254 ile çözüyordu ve Türkçe **"Ş"** cp1254'te tanımsız. Ölçüldü: bir koşu tam olarak böyle çöktü. Dokuz çağrıya `encoding="utf-8", errors="replace"` eklendi — **her doğrulama aracının çıktı okuması bundan geçiyor** |

🔴 **Bu dört madde, deponun EN AZ denetlenmiş kodudur** ve tam olarak senin
denetlediğin örüntünün içinde doğdu: *düzeltmeyi yazan, testini yazan, testi
koşan ve "kapandı" diyen aynı taraf.* Tam metin: `04-NEDEN-BOYLE.md` **K-046**.

---

# DENETLENECEK İDDİALAR

## A · Kapı raporu — 13 çıkış kriteri

🔴 **Kapı raporu 20 Ağustos 2026'da İKİ KEZ koşturuldu** — şema
değişikliğinden *(B-30 mekanizma sayaçları · B-26 parmak izleri)* sonraki
ilk koşulardır:

| # | ne zaman | sonuç | süre |
|---|---|---|---|
| **1** | şema değişikliğinden sonra, **hiçbir şey düzeltilmeden** | 🔴 **12/13** — düşen: **Ç5** *(`!!SEÇİM 18≠14`)* | **71,0 dk** |
| **2** | Ç5'in beklenen test sayısı düzeltildikten sonra | ✅ **13/13** | **73,9 dk** |

Ç5'in düşme sebebi bir test kırılması **değildi** — 18 testin 18'i geçiyordu.
B-27b'nin dört içerik testi `test_gozlem.py`ye eklenmiş, kapının beklediği
sayı **14**'te kalmıştı. **Kapı haklıydı.** Ayrıntı: `04-NEDEN-BOYLE.md`
**K-046**.

> ⚠️ **Bu 13/13'ü bir otorite olarak alma.** İki koşuda da aynı araç, aynı
> ölçütlerle konuştu — ve o ölçütler iki bağımsız denetimde **sekiz kusur**
> verdi *(Ç1.1 boş kümede geçiyordu · Ç6.2 ölçtüğünün tersiyle korelasyonluydu
> · üç kriter kırılamazdı · Ç1.3'ün eşiği veriden türüyordu · Ç3'ün beklenen
> sayısı yoktu · Ç5'in beklenen sayısı iki kez bayatladı)*. Kapının **kendisi**
> hâlâ denetlenecek — şüphe listesi madde 10.


**Yeniden üretmen istenen ilan edilmiş değerler:**

| Kriter | İddia |
|---|---|
| Ç1.1 | Korunum **540/540** koşuda tutuyor *(6 senaryo × 3 trafik × 30 tohum)* |
| Ç1.2 | Dört düşme sebebinin dördü de tetikleniyor *(dördüncüsü `rota_yok`)* |
| Ç1.3 | **35 mutasyonun 35'i**, her biri **kendi beklenen testiyle** yakalanıyor · taban temiz |
| Ç1.4 | Boruda kalan **%0,156** *(< %1)* |
| Ç2 | 6 test — belirlenimcilik *(tam koşu · PYTHONHASHSEED · iki kol aynı kanal)* |
| Ç3 | **44** analitik kontrol |
| Ç5 | Gözlem sözleşmesi — **18 test** *(beklenen sayı 20 Ağu'da 14'ten düzeltildi)* |
| Ç4.1 / Ç4.2 | 6 test · Li platosu **1/6,29** · %95 GA genişliği **%2,04** |
| Ç6.2 | Kanal dilimi marj **değişmezi** *(2 test)* |
| Ç6.1/6.3/6.4 | **Kaynak denetimi** *(grep — "değişmez" DEĞİL)* |

🔴 Bir iddiayı doğrularken **iddianın kendi ölçütünü kullanma.**
*(Örn. "korunum tutuyor"u korunum fonksiyonunu çağırarak değil, paket
nesnesi sayarak doğrula — ilk iki denetçi de böyle yaptı.)*

## B · 40 bulgunun tamamının kapandığı iddiası

`v2/04-NEDEN-BOYLE.md` **K-044** ikinci denetimin 17 bulgusunun her birinin
nasıl kapandığını yazıyor.

🔴 **En az 8'ini seç ve kapandığını KENDİN doğrula.** Kapanma iddiası
genelde *"şu test yazıldı"* biçiminde; o testin gerçekten ilgili şeyi
ölçtüğünü **mutasyonla** sına — ve **mutasyonu biraz değiştirip** testin
hâlâ kırıldığını kontrol et *(fazla dar bir test, yalnızca denetçinin
yazdığı tek mutasyonu yakalar)*.

Öncelikli sekiz: **B-24 · B-26 · B-27 · B-27b · B-29 · B-30 · B-32 · B-36.**

## C · 20 Ağustos'ta üretilen yeni sayılar

| İddia | Değer | Üretici olduğu söylenen |
|---|---|---|
| **H1.1 mekanizma sayacı ayırt ediyor** | kör aktarıcı **%8,68** vs gürültüden kaçan **%1,86** *(4,7 kat)*; ort. karar PER'i 0,3282 vs 0,0055 | `tests/test_mekanizma_kapisi.py` |
| Kör tarama | havuz **203** · taban **271 test** · skor **%55,6 (10/18)** · **8 sağ kalan** — ⚠️ *taban o gün 271'di, bugün 284; skor bir **kod durumu fotoğrafıdır**, ilerleme ölçüsü değil* | `kor_mutasyon.py 24` |
| Sağ kalan ayıklama | **7/7 eşdeğer** · davranışı değiştiren **0** | `sag_kalan_ayikla.py` |
| S2 = +2 dBm gerekçesi | teslim **0,5252** · dinamik aralık **[0,1197 · 0,8955]** · orta **0,5076** · kısıt **ulaşılabilirlik ≥ %90** | `kurulum_kalibrasyonu.py` |
| Parmak izi koruması | **6 yanlış kullanım reddediliyor**, **4 meşru tedavi farkı kabul ediliyor** | `tests/test_karsilastirma.py` |
| Derece kayması | **−%0,364 ± 0,026** | `kurulum_kalibrasyonu.py --a` |

**En az beşini seç ve kendin yeniden üret.** Tutmuyorsa bulgudur —
bu depoda *"üretici komut yazılı ve o sayıyı üretmiyor"* vakası **üç kez**
yaşandı.

---

# 🔍 ŞÜPHE LİSTESİ — bu denetime özel 12 madde

> İlk iki denetimin şüphe listeleri `AILE0-DENETIM-PROMPTU.md` ve
> `AILE0-DENETIM-2-PROMPTU.md`de. **İkisini de uygula**, ama asıl ağırlığı
> aşağıdakilere ver: bunlar **son 24 saatte yazılmış koda** bakıyor.

## 1 · ⭐ Y11 — KORUMANIN KAPSAMI DIŞI

> **Bir koruma, yalnızca yakalayabildiği durumla sınanamaz.**

`sim/karsilastirma.py` iki parmak iziyle korunuyor: `pencere_evren_hash`
*(kimlik · doğum · kaynak · hedef)* ve `kurulum_hash` *(tedavi alanları
hariç tüm konfig + düğüm konumları)*.

🔴 **Bu korumayı KIR.** Reddetmesi gerekirken **kabul ettiği** bir çift üret.
Bakılacak yerler: `TEDAVI_ALANLARI` kümesi fazla geniş mi? `kon.sozluk()`
gerçekten **her** alanı taşıyor mu? Hash'e giren alanlar birbirinden
**gerçekten ayrılıyor** mu? Konfigürasyonda olmayan ama sonucu değiştiren
bir fark var mı?

Aynı soruyu **her** koruma için sor: `UYGULANMAMIS_BAYRAKLAR` ·
`rng.HENUZ_KULLANILMAYAN` · `gozlem.HENUZ_ICERIK_TESTI_OLMAYAN` ·
`KanalErisimi.__setattr__` yazım hatası koruması.

## 2 · 🔴 KÂHİN SIZINTISININ YENİ YÜZEYİ

`mac.bag_gercek_per()` simülatörün bildiği **gerçek** bağ kalitesidir.
`05-GOZLEM-PENCERESI.md` §D bunu açıkça ayırıyor: *"gerçek değer → yalnızca
teşhis ve rapor; protokolün tahmini → yalnızca karar."*

🔴 Sor: bu değer **karara girebilir mi?** `_gozlem_uret` yüzeyinde bir izi
var mı? `protokol_teshis` slotu protokolden yazılabilir bir kanal açıyor mu
— ve oraya yazılan bir şey **geri okunabilir mi?** Bir protokol
`Gozlem` nesnesi üzerinden simülatöre geri referans bulabilir mi?

`dogrulama/aktaricilar.py`daki aktarıcılar kendilerini kâhin ilan ediyor —
**gerçekten yalnızca doğrulama için mi kullanılıyorlar**, yoksa rapora giren
bir sayı üretiyorlar mı? *(`08`in kendi notu: 540 koşuluk korunum matrisinin
tamamı kâhin bir aktarıcıyla koşuldu.)*

## 3 · ⭐ DENETÇİNİN MUTASYONUNA GÖRE YAZILMIŞ TEST — FAZLA DAR MI?

`tests/test_denetim2_boslukları.py` **KM1–KM6** ve mutasyon paketinin
**D24–D28**'i, ikinci denetçinin yazdığı mutasyonlara **birebir** cevap
olarak yazıldı.

🔴 Her biri için sor: test **mutasyonu** mu yakalıyor, yoksa **mekanizmayı**
mı koruyor? Mutasyonu biraz değiştir *(farklı sabit, farklı yön, aynı
etkiyi başka satırdan üret)* — test hâlâ kırılıyor mu? Kırılmıyorsa,
kapanan şey bulgu değil **o tek mutasyondur.**

Kayıtlı bir uyarı var, sına: `test_d3_bayat_komsu_gozlemden_dusuyor` ömrü
`kon.komsu_omru_s`'ye **göreli** kullandığı için ömrün **değerine** tanım
gereği duyarsızdı. Aynı sınıftan başka test var mı?

## 4 · ⭐ Y7'NİN SEKİZİNCİ ÖRNEĞİ

> **Bir doğrulama aracı, ne koştuğunu kendisi doğrulamak zorundadır.**

🔴 **Değişen ya da yeni olan her aracı boş/dejenere girdiyle sına:**
`mutasyon_on_kontrol.py` · `sag_kalan_ayikla.py` · `kurulum_kalibrasyonu.py`
· `aile0_kapi_raporu.py` · `kor_mutasyon.py` · `mutasyon_paketi.py`.

- *"0 hata"* ile *"0 test"* ayırt ediliyor mu?
- Boş bir kümede `0 == 0` ile geçen bir kriter var mı?
- Bir alt süreç **çöktüğünde** sonuç ne oluyor — hata mı, "geçti" mi, bulgu mu?
- Bir aracın kendi girdisi **bayatlarsa** araç bunu söyleyebiliyor mu?
  *(B-24 tam olarak buydu.)*

## 5 · DÜZELTMENİN KENDİSİ HATA GETİRDİ Mİ

20 Ağustos'ta **şema iki kez değişti** *(B-30 mekanizma sayaçları, B-26
parmak izleri)* ve **17 düzeltme** yapıldı.

🔴 Sor: bir düzeltme **RNG çekim sırasını** değiştirdi mi? Daha önce
ölçülmüş bir sayı kaydı mı? Kayan sayıların **hepsi** yeniden ölçüldü mü,
yoksa bazıları belgelerde eski hâliyle mi kaldı?

*(Bu tam olarak B-28'di: bir önceki turda `beacon_faz` akışı eklendi, iki
sayı yeniden ölçüldü, **kalibrasyon tablosu ölçülmedi** ve dört belgede
bayat kaldı.)*

## 6 · GÖZLEM İÇERİK TESTLERİ NE ÖLÇÜYOR

B-27b'nin düzeltmesi, gözlem penceresinin dört alanını *"bağımsız hesapla
karşılaştıran"* içerik testlerine bağladı.

🔴 Sor: karşılaştırılan *"bağımsız hesap"* gerçekten bağımsız mı, yoksa
**üretici ifadenin tekrarı** mı? *(Aynı formülü iki yerde yazmak doğrulama
değildir.)*

Ve beyan zincirini sonuna kadar takip et: `test_gozlem.py`nin
`test_b27b_her_gozlem_alaninin_icerik_testi_var` testi
`IZINLI_GOZLEM_ALANLARI`nın her alanının **ya** bir içerik testine bağlı
**ya** `gozlem.HENUZ_ICERIK_TESTI_OLMAYAN`da beyan edilmiş olmasını
istiyor. 🔴 Bu zincirdeki her halkayı sına: içerik testi olan alanların
listesi **nereden geliyor**, ve o listeye girmek için gerçekten bir test
gerekiyor mu? *(`03` B5: **"etiketi elle taşımak"** — elle yazılan bir
etiket sessizce yanlışlaşır.)* Beyan listesinin bugün **boş** olması bu
kontrolü dejenere ediyor mu?

Dört alanın **hâlâ hiç tüketicisi yok**. İlk gerçek okuyucu Aile 1'in
protokolü olacak.

## 7 · ÖN-KAYIT ↔ KOD

`06-ON-KAYIT.md` H1.1 şunu ilan ediyor: *"seçilen rotalarda ara bölge bağı
(0,05 ≤ PER ≤ 0,9) kaç kez kullanıldı … **bu sayaç düşmüyorsa sonuca
bakılmaz.**"* Sayaç 20 Ağustos'ta eklendi.

🔴 Sor:
- Sayaç **gerçekten** ölçülebilir mi, yoksa ölçülebilir **görünüyor** mu?
- Bant *(`Konfig.ara_bolge_per_bandi`)* **tek yerde** mi tanımlı, sonuç
  satırında da taşınıyor mu?
- 🔴 Kaydedilmiş bir sınır var: **bant monoton değil**, çünkü ara bölge bir
  **orta dilim**. Sayaç *"yalnızca aynı çalışma noktasında iki kol
  arasında"* okunabilir. Bu sınır her yerde yazılı mı — yoksa Aile 1'de
  güçler arası okunacak bir yerde mi duruyor?
- K-020'nin *"133 bağın yalnızca **11–17**'si ara bölgede"* sayısı hangi
  bantla ölçülmüştü? İkinci denetçi bunu **yeniden üretemedi** *(ön-kaydın
  bandıyla 6–14 çıkıyor)*. Düzeldi mi, yoksa hâlâ orada mı?
- `05` §D **beş** teşhis sayacı sayıyor. Kaçı şemada var?

## 8 · KAPSAM BEYANI — İKİ YÖNLÜ

`08-AILE0-KAPSAM.md` **22 madde** sayıyor: *"bu araç şunları yapmaz."*

- **(a)** *"Yapmaz"* denen bir şey aslında **yapılıyor** mu?
- **(b)** Kodda modellenmemiş ama listede **olmayan** bir şey var mı?
  *(Birinci denetim 4, ikinci denetim 4 tane buldu. Üçüncüsü?)*
- Her maddenin **etki yönü** yazılı *("modeli iyimser/kötümser yapar")* —
  bu yönler doğru mu? Özellikle **18. madde** *(tek/merkezî karıştırıcı —
  "hipotezin lehine")*: bu yön kodla doğrulanabiliyor mu?

## 9 · BELGE ↔ KOD: HER SAYININ ÜRETİCİSİ

`03` kural 1: *"her sayının yanında üretici komut ve kaynak dosya yazılır."*

🔴 **45 karar kaydından rastgele 5 tanesini seç** ve sayılarını yeniden
üret. Kaç kayıtta *"Üretici"* satırı **yok**? *(İkinci denetim 43 kaydın
30'unda olmadığını ölçmüştü — bugün ne?)*

Aynı taramayı `08`, `06`, `07` ve `09`daki sayılara da uygula. Bu depoda
*"üretici komut yazılı ve o sayıyı vermiyor"* örüntüsü **üç kez** çıktı.

## 10 · KAPININ KENDİSİ

Kapı kriterleri **iki kez** denetlendi ve **sekiz kusur** çıktı. Üçüncüsünü
yap.

- Ç1.3'ün eşiği artık sabit mi *(`BEKLENEN_MUTASYON = 35`)*, yoksa hâlâ
  veriden mi türüyor?
- **Her kriter için beklenen test sayısı yazılı mı, ve o sayı GÜNCEL mi?**
  *(Bu depoda bir kriterin beklenen sayısı iki kez bayatladı: 11→14, sonra
  yine.)* Beklenen sayı ile fiilen toplanan test sayısını **kendin
  karşılaştır** — kapıyı koşmadan, `--collect-only` ile yapılabilir
- Bir kritere yeni test **eklendiğinde** kapı bunu görüyor mu; **çıkarıldığında**?
- Kapı raporu bir kriter düştüğünde **hangisinin** düştüğünü söylüyor mu?

## 11 · AİLE 1 BU ARAÇLA YAZILABİLİR Mİ

Sıradaki aşama, `05-GOZLEM-PENCERESI.md`nin penceresinden beslenen rakip
protokoller yazacak *(atlama-sayısı ve bağ-kalitesi temelli)*.
**Belge genişletmeyi yasaklıyor.**

🔴 İkinci denetçinin kaydettiği bir sınırı sına: **protokol yalnızca
düğümün paketi varken ve MAC boşken çağrılıyor.** Kuyruk boşken gerçekleşen
iletim sonuçları protokole **hiç görünmüyor**. Bu doğru mu? Doğruysa,
takvimli/periyodik davranış *(Aile 2'nin `takvimli_tazeleme` kolu)* bu
arayüzle **kurulabilir mi?**

Ve: bağ kalitesi temelli bir protokol `son_iletim_sonucu` +
`son_iletim_hedefi` + `komsular`dan ETX benzeri bir kestirim **gerçekten**
kurabilir mi? Bir tanesini **yaz ve koştur** — pencerenin yetip yetmediğini
ancak böyle öğrenirsin.

## 12 · İSTATİSTİK KATMANI

`06` Bölüm 3 Wilcoxon · Holm–Bonferroni · güç analizi ve 🔴 ile işaretlenmiş
bir **NaN tuzağı** ilan ediyor *(tüm farklar sıfırken `scipy.stats.wilcoxon`
hata fırlatmaz, **NaN döndürür**; `try/except ValueError` bunu yakalamaz;
tek bir NaN düzeltilmiş p'lerin tümünü 1,00 yapar — ve davranış **örneklem
boyutuna bağlıdır**)*.

Kod karşılığı **yok**; `08` madde 21 bunu beyan ediyor.
🔴 Sor: beyan **yeterli mi**? Ön-kaydın *"ZORUNLU"* dediği bir korumayı
*"yazılmadı"* diye beyan etmek, mühürden önce kabul edilebilir mi? Güç
analizi **26 Eylül mührüne** bağlı ve o tarihe kadar bu katman yazılmalı.

---

# ÇALIŞMA BİÇİMİN

1. **Önce oku, sonra koştur, en son yorumla.** İlk okunacak:
   `v2/03-YONTEM-KURALLARI.md`, sonra `v2/04-NEDEN-BOYLE.md`nin sonundaki
   **Y1–Y11** tablosu.
2. Her bulgunun yanında **üretici komut** ve **kaynak dosya:satır**.
3. Bir iddiayı doğrularken **iddianın kendi ölçütünü kullanma.**
4. ⭐ **Y6 — beklenenden iyi çıkan sonuç, kötü çıkan kadar şüphelidir.**
5. Bir şey doğru çıkıyorsa **neden doğru çıktığını** anla. Yanlış sebeple
   doğru çıkan sonuçlar en tehlikelileridir.
6. ⭐ **Y8 — bir mutasyon yazdığında, bozduğu yolun sağlam koşuda
   tetiklendiğini ÖNCE göster.**
7. ⭐ **Y10 — bir yaklaşık-eşitlik iddiasının kırılabilir olduğunu
   göstermenin tek yolu onu KIRMAKTIR.** Tolerans, birim, ölçek.
8. ⭐ **Y11 — bir korumayı sınamak, kapsamı DIŞINDA kalan bir vaka üretip
   reddedildiğini göstermektir.**
9. Deneme için depoyu geçici bir dizine kopyala; **aslını değiştirme.**

---

# ÇIKTI: `aile0_audit.md` — nasıl güncellenecek

Bu dosya şu an **iki denetimin raporunu** taşıyor ve proje ikisini de
tarihsel kayıt sayıyor. 🔴 **İçeriğini SİLME, DEĞİŞTİRME.**

Yapman gereken:

1. Dosyanın başındaki durum bloğunu **üçüncü denetimi de içerecek şekilde
   genişlet** *(mevcut iki satır durur, üçüncü satır eklenir)*.
2. Dosyanın **sonuna** `# ÜÇÜNCÜ DENETİM — <tarih>` bölümünü ekle.
3. 🔴 Bulgu numaraları **B-41**'den devam eder. *(B-01…B-40 kullanıldı.)*

```
## 0. YÖNETİCİ ÖZETİ
    Kapanış geçerli mi: EVET / KOŞULLU / HAYIR — ve neden, üç cümlede
    🔴 SAĞ KALAN ORANI burada, ilk paragrafta.

## 1. YENİ BULGULAR                     (B-41'den itibaren)
    Her biri: ciddiyet · nerede (dosya:satır) · İDDİA · ÖLÇTÜĞÜM ·
    ÜRETİCİ KOMUT · beklenen/görülen · neden önemli · öneri
    🔴 Üretici komut ve beklenen/görülen olmadan bulgu yazılamaz.

## 2. İKİNCİ DENETİMİN 17 BULGUSU — kapanma doğrulaması
    Seçtiğin ≥8 bulgu için: gerçekten kapandı mı, nasıl doğruladın,
    testi mutasyonla sınadın mı, test fazla dar mı

## 3. DOĞRULANAN İDDİALAR
    Yeniden ürettiğin ve TUTAN sayılar — üretici komutlarıyla

## 4. ÜRETİLEMEYEN İDDİALAR
    Üretici komutu olmayan ya da tutmayan sayılar

## 5. 🔴 KENDİ MUTASYONLARIN
    ≥10 yeni mutasyon. Her biri için:
      · bozduğu yolun tetiklenme sayısı (Y8, ÖNCE)
      · 272 testten sağ çıktı mı
      · sağ kaldıysa davranışı DEĞİŞTİRİYOR mu (eşdeğer / tüketicisiz / gerçek)
    🔴 SAĞ KALAN ORANI ve seri tablosu (8/10 → 7/10 → seninki)
    🔴 Örüntü: sağ kalanlar hangi sınıfta toplanıyor?

## 6. ŞÜPHE LİSTESİ SONUÇLARI
    12 maddenin her biri için: temiz / bulgu var (B-nn) / denetlenemedi

## 7. KAPSAM BEYANINA EKLENMESİ GEREKENLER
    Modellenmemiş ama 22 maddede olmayan şeyler — etki yönleriyle

## 8. 🔴 ANLAŞILMAYANLAR
    Anlamadığın ve bu yüzden denetleyemediğin mekanizmalar.
    🔴 BU BÖLÜM BOŞ BIRAKILAMAZ. Boşsa yeterince derine inmemişsindir.
    ⚠️ İlk iki denetimde bu bölümdeki maddelerin birkaçı GERÇEK KUSUR çıktı.

## 9. KOŞTURDUĞUN KOMUTLAR
    Tam liste, özet çıktılarıyla
```

4. **Son satır:** depoda hiçbir dosyanın değiştirilmediğini ve hiçbir git
   komutunun çalıştırılmadığını **açıkça yaz.**

---

# 🔴 SON SÖZ

Bu projenin en güçlü tarafı, kendi hatalarını **ölçüp yazmış** olması. Bir
bandı koşmadan önce ilan etti ve **tutmadı** · kendi hata iddiasını ölçüp
**çürüttü** · kendi kuralını ihlal edip **yakaladı ve tohumları yaktı** ·
kapanmış bir kapıyı bağımsız denetimle **iki kez yeniden açtı** · ve
*"örüntü kapanmadı"* cümlesini **kendi kapanış metnine yazdı.**

Senden beklenen bir onay değil.
**Bulacağın her şey, bulunmadığı takdirde jürinin bulacağı bir şeydir.**

*"Her şey yolunda görünüyor"* diyen bir rapor **işe yaramaz.** Hiçbir bulgu
bulamazsan bunu da yaz — ama **hiçbir şey bulamamak, aradığın yerlerin
listesiyle birlikte anlamlıdır.** Nereye baktığını yaz.

En değerli bulgun, **projenin kendi kurallarından birini ihlal ettiğini**
gösterdiğin yer olacak. `v2/03-YONTEM-KURALLARI.md`yi ve Y1–Y11'i yanında
tut.

**Bir şeyi büyütmek istiyorsan önce ölç.**
