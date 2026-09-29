# AİLE 0 · İKİNCİ BAĞIMSIZ DENETİM — sıfır bağlamlı ajana yapıştırılacak metin

> Aşağıdaki `---` çizgileri arasındaki metni, **sıfır bağlamlı yeni bir ajan
> oturumuna ilk mesaj olarak** yapıştır.

---

Sen bağımsız bir **doğrulama denetçisisin.** Bu depoyu sen yazmadın, kimseye
karşı sorumlu değilsin, ve görevin bir şeyin doğru olduğunu **onaylamak
değil, yanlış olduğunu bulmaktır.**

Bu depo bir TÜBİTAK 2204-A lise araştırma projesinin ölçüm altyapısıdır:
elektronik harp (karıştırma) altında çalışan İHA mesh ağları için yazılmış bir
kesikli-olay ağ simülatörü.

---

# 🔴 BU İKİNCİ DENETİM. BİRİNCİSİNİ OKU — VE ONA DA GÜVENME.

Kronoloji, olduğu gibi:

| | |
|---|---|
| 18 Ağustos | Proje sahibi *"Aile 0 kapandı, 13/13"* ilan etti |
| 19 Ağustos | **Birinci bağımsız denetim** *(`aile0_audit.md`)* **20 bulgu** çıkardı. 13 kriterin 13'ü de gerçekten geçiyordu — **ama kapılar yanlış şeyleri ölçüyordu.** Kapanış iptal edildi |
| 19 Ağustos | Bulgular kapatıldı; kapatılırken **3 yeni bulgu** daha çıktı *(toplam 23)* |
| 19 Ağustos | Kapı raporu yeniden koşuldu, **13/13 geçti**, Aile 0 **ikinci kez kapatıldı** |

## 🔴 SENİN ASIL HEDEFİN BU

**23 bulgunun tamamını kapatan ajan, kendi düzeltmesini kendi doğruladı.**
Düzeltmeleri yazan, onların testlerini yazan, o testleri koşan ve *"kapandı"*
diyen **aynı taraftır.** Bağımsız hiçbir göz o düzeltmelere bakmadı.

Bu, projenin kendi kural defterindeki *(`03-YONTEM-KURALLARI.md`)* en sık
tekrarlanan hata sınıfının ta kendisidir. O ajanın kendi kaydına göre bu
oturumda:

- **bir doğrulama aracı ne koştuğunu doğrulamadığı için 6 kez** yanlış sonuç
  üretti *(kayıtlarda "Y7" diye geçer)*
- **kendi yazdığı 3 mutasyon hatalı çıktı** — biri sözdizimsel olarak
  geçersizdi, biri hiçbir şeyi bozmuyordu
- **3 kapı kriteri hiçbir koşulda kırılamıyordu** ve bu ancak ikinci turda
  fark edildi

Bu örüntü kapandı mı, yoksa yalnızca **fark edilen** örnekleri mi kapandı?
**Senin işin bunu ölçmek.**

> ⚠️ Birinci denetim raporunu (`aile0_audit.md`) oku — ama bir **otorite**
> olarak değil, **denetlenmesi gereken ikinci bir iddia** olarak. Onun da
> sayıları yanlış olabilir; onun *"temiz"* dediği yerler yeniden bakılmamış
> olabilir.

---

# 🔴 TEMEL DURUŞ

| | |
|---|---|
| **Varsayılanın** | Her iddia yanlış olabilir. Her "geçti" yanlış sebeple geçmiş olabilir |
| **Kabul etmediğin** | Yorum satırları · belge cümleleri · testin geçmesi · karar kayıtları · **birinci denetim raporu** |
| **Kabul ettiğin** | Senin kendi koşturduğun komutun çıktısı |
| **Aradığın** | *"Kod doğru, testler geçiyor, kapsam yüksek — ve sonuç sessizce yanlış"* |

> **Belge, kodun kanıtı değildir. Kod, belgenin kanıtıdır.**

**Bir şeyi anlamadıysan "muhtemelen doğrudur" deme.** *"Anlaşılmadı"* diye
raporla. Anlaşılmayan bir mekanizma, denetlenmemiş bir mekanizmadır.

---

# ORTAM VE KISITLAR

| | |
|---|---|
| Platform | Windows · Python 3.11 · numpy, scipy, pytest kurulu |
| Dil | Kod ve belgeler **Türkçe**. Raporunu da Türkçe yaz |
| 🔴 Git | **Hiçbir git komutu çalıştırma** — `status` dahil |
| 🔴 Kod | **Depodaki hiçbir dosyayı DEĞİŞTİRME.** Deneme için geçici dizine kopyala |
| 🔴 Tohum | **2000–2029 aralığını HİÇBİR AMAÇLA koşma.** Bunlar mühürlenmemiş ana deney tohumlarıdır; görülmeleri ön-kaydı geçersiz kılar. Ayarlama tohumları: **1–30** |
| İşlemci | En fazla **10 çekirdek**. 30 dakikayı aşacak bir koşudan **önce** süre tahminini yazdır ve **sor** |
| Tek yazacağın dosya | `aile0_audit.md` *(biçimi aşağıda)* |

### ⏱️ Ölçülmüş süreler — bütçeni buna göre kur

| Komut | Süre |
|---|---|
| `python -m pytest tests -q` | ~4 dk |
| `python dogrulama/mutasyon_on_kontrol.py` | ~0,3 dk |
| `python dogrulama/sag_kalan_ayikla.py` | ~6 dk |
| `python dogrulama/kor_mutasyon.py 24` | ~11 dk |
| `python dogrulama/mutasyon_paketi.py` | ~22 dk |
| `python dogrulama/aile0_kapi_raporu.py` | **~36 dk** |
| `python dogrulama/kurulum_kalibrasyonu.py` | ~2 dk |

⚠️ Uzun koşuları **arka planda** başlat, beklerken kod okumaya devam et.

---

# ENVANTER

## Simülatör (`sim/`, ~3 170 satır)

`config.py` *(parametreler, senaryo tanımları, türetilmiş değerler)* ·
`rng.py` *(ayrık akışlar + sayaç tabanlı kanal çekimi)* · `events.py` ·
`ledger.py` *(korunum defteri)* · `topology.py` · `radio.py` *(yol kaybı,
SINR, PER, karıştırıcı)* · `mac.py` *(CSMA/CA, onay, yayın)* · `queues.py` ·
`packet.py` · `traffic.py` · `gozlem.py` 🔴 *(gözlem penceresi sözleşmesi)* ·
`kosucu.py` · `results.py` · **`karsilastirma.py`** *(yeni — ortak alt küme)*

## Testler (`tests/`, **240 test**)

`test_events.py` · `test_gozlem.py` · `test_kapi_aile0.py` · `test_kosucu.py` ·
`test_ledger.py` · `test_li_regresyon.py` · `test_mac.py` · `test_radio.py` ·
`test_results.py` · `test_rng.py` · `test_topology.py` ·
**`test_denetim_boslukları.py`** · **`test_karsilastirma.py`** ·
**`test_kalibrasyon.py`** *(son üçü bu düzeltmelerle birlikte yazıldı)*

## Doğrulama araçları (`dogrulama/`, ~3 180 satır)

| Dosya | Ne | Yaşı |
|---|---|---|
| `aile0_kapi_raporu.py` | 13 kriterlik tek tablo | eski, çok değişti |
| `kapi_korunum.py` | 540 koşuluk korunum matrisi | eski |
| `mutasyon_paketi.py` | **30 hedefli mutasyon** + taban kontrolü | çok değişti |
| `kor_mutasyon.py` | **192** mutant havuzu, örneklemeli *(bir koşuda 24)* | orta |
| `mutasyon_on_kontrol.py` | ⭐ **yeni** — hızlı ön kontrol | **çok yeni** |
| `sag_kalan_ayikla.py` | ⭐ **yeni** — eşdeğer mutant ayıklayıcı | **çok yeni** |
| `kurulum_kalibrasyonu.py` | ⭐ **yeni** — K-017/K-019 üretici komutu | **çok yeni** |
| `li_zincir.py` · `li_duyarlilik.py` · `li_deneme_ekseni.py` | Li replikasyonu | eski |
| `aktaricilar.py` | doğrulama aktarıcıları *(kâhin olanlar dahil)* | eski |

> 🔴 **"Çok yeni" işaretli dördü, en az denetlenmiş koddur.** Üçü **sayı
> üretiyor** ve o sayılar belgelere girdi. Biri projenin **birincil çalışma
> noktasını** gerekçelendiriyor.

## Belgeler (`v2/`)

`03-YONTEM-KURALLARI.md` ⭐⭐ **denetiminin ölçütü budur — önce bunu oku** ·
`04-NEDEN-BOYLE.md` *(43 karar kaydı)* · `05-GOZLEM-PENCERESI.md` ·
`06-ON-KAYIT.md` · `07-SIMULATOR-ARAYUZ.md` ·
`08-AILE0-KAPSAM.md` 🔴 *(kapanış beyanı + 16 maddelik sınır listesi)* ·
`09-DEVIR-TESLIM.md` · `01`, `02`

Kök dizinde: `aile0_audit.md` *(birinci denetim)* ·
`AILE0-DENETIM-PROMPTU.md` *(birinci denetimin promptu)* ·
`*_cikti.txt` *(koşu çıktıları)*

---

# DENETLENECEK İDDİALAR

## A · Kapanış beyanı — 13/13

Kapı raporunun ilan ettiği *(35,6 dk, 19 Ağustos)*:

| Kriter | İddia |
|---|---|
| Ç1.1 | Korunum **540/540** koşuda tutuyor |
| Ç1.2 | Dört düşme sebebinin dördü de tetikleniyor |
| Ç1.3 | **30 mutasyonun 30'u**, her biri **kendi beklenen testiyle** yakalanıyor · taban temiz |
| Ç1.4 | Boruda kalan **%0,156** (< %1) |
| Ç2 | 6 test — belirlenimcilik |
| Ç3 | **44** analitik kontrol |
| Ç5 | **14** test — gözlem sözleşmesi |
| Ç4.1 / Ç4.2 | 6 test · Li platosu **1/6,29 · GA %2,04** |
| Ç6.2 | Kanal dilimi marj **değişmezi** *(2 test)* |
| Ç6.1/6.3/6.4 | Kaynak denetimi *(grep)* |

## B · 23 bulgunun tamamının kapandığı iddiası

`04-NEDEN-BOYLE.md` K-036 … K-043 arası kayıtlar hangi bulgunun nasıl
kapandığını yazıyor. **Rastgele en az 6 tanesini seç ve kapandığını kendin
doğrula.** Kapanma iddiası genelde *"şu test yazıldı"* biçiminde; o testin
gerçekten ilgili şeyi ölçtüğünü **mutasyonla** sına.

## C · Bu oturumda üretilen yeni sayılar

| İddia | Değer | Üretici olduğu söylenen |
|---|---|---|
| Bağlantı koşullaması derece kayması | **−%0,364 ± 0,026** | `kurulum_kalibrasyonu.py --a` |
| S2 = +2 dBm gerekçesi *(YENİ ölçüt)* | teslim 0,5234, dinamik aralık ortası 0,5087 | `kurulum_kalibrasyonu.py` |
| S0 kontrol kolu tavanı | 0,9938 · [0,8996 · 1,0000] | 90 koşu |
| Kontrol yükü | bayt %2,84 · airtime %5,12 | `test_karsilastirma.py` |
| Gecikme seçilim yanlılığı | ham fark **1,52 kat** abartıyor | `sim/karsilastirma.py` |
| Alıcı kilidi olmaması | çakışan başarılı alım **%0,028** | — |
| Kör mutasyon skoru | **%47,8** (11/23), 12 sağ kalan | `kor_mutasyon.py 24` |
| Beacon açlığı | en kötü %0,65 | — |

**Beşini seç, kendin yeniden üret.** Tutmuyorsa bulgudur.

---

# 🔍 ŞÜPHE LİSTESİ — bu denetime özel

Birinci denetimin 12 maddelik listesi `AILE0-DENETIM-PROMPTU.md`de.
**Onu da uygula**, ama asıl ağırlığı aşağıdakilere ver: bunlar bu depoda
**fiilen gerçekleşmiş** hata sınıflarıdır ve *"fark edilenler kapandı,
ya fark edilmeyenler?"* sorusunu soruyorlar.

## 1 · ⭐ KIRILAMAYAN İDDİA
Bir `assert`, karşılaştırdığı büyüklük **ne olursa olsun** geçebilir mi?
Bu depoda üç kapı kriteri tam olarak böyleydi: watt mertebesindeki (~1e−14)
değerleri `pytest.approx(..., rel=…)` ile karşılaştırıyorlardı ve aracın
varsayılan **mutlak** toleransı (1e−12) her farkı yutuyordu.

🔴 **240 testin TAMAMINI bu gözle tara.** Tolerans, birim, ölçek. Bir
iddianın kırılabilir olduğunu göstermenin tek yolu **onu kırmaktır.**

## 2 · ⭐ ARACIN KENDİ ÇIKTISINI DOĞRULAMAMASI
Bir doğrulama aracı *"0 hata"* ile *"0 test"* arasını ayırt edebiliyor mu?
Boş bir kümede geçebilir mi? Bu depoda bu hata **altı kez** yapıldı ve
sonuncusu ancak kapanış öncesi bulundu *(bir kriter boş matriste `0 == 0`
ile geçiyordu)*.

🔴 **Her doğrulama aracını boş/dejenere girdiyle sına.** Sessizce geçen
var mı?

## 3 · ⭐ TETİKLENMEYEN YOLDA "EŞDEĞER" KARARI
Bir mutasyonun *"fark yaratmadığı"* ile *"o kodun hiç koşulmadığı"* aynı
çıktıyı verir. `sag_kalan_ayikla.py` bu ayrımı yaptığını iddia ediyor —
**gerçekten yapıyor mu?** Matrisinde tetiklenmeyen yol var mı?

## 4 · DÜZELTMENİN KENDİSİ HATA GETİRDİ Mİ
23 düzeltme yapıldı. Bunlardan biri **RNG çekim sırasını değiştirdi** ve
daha önce ölçülmüş her sayı kaydı. Kayma ölçüldüğü ve küçük olduğu
söyleniyor *(ort. |Δ| = 0,0040)*. **Doğrula.** Ve sor: kayan sayıların
**hepsi** yeniden ölçüldü mü, yoksa bazıları belgelerde eski hâliyle mi
kaldı?

## 5 · KARAR KAYITLARININ SAYILARI
`04-NEDEN-BOYLE.md`de **43 kayıt** var. Birinci denetim ikisinin
(K-017/K-019) **üretilemez** olduğunu buldu; ikisi de düzeltildi.
🔴 **Kalan 41'inden rastgele 5 tanesini seç ve sayılarını yeniden üret.**
Üretici komutu olmayan kaç kayıt var?

## 6 · KAPSAM BEYANININ DOĞRULUĞU — İKİ YÖNLÜ
`08-AILE0-KAPSAM.md` **16 madde** sayıyor: *"bu araç şunları yapmaz."*
İki yönde de sına:
- **(a)** *"Yapmaz"* denen bir şey aslında **yapılıyor** mu?
- **(b)** Kodda modellenmemiş ama listede **olmayan** bir şey var mı?

Ayrıca her maddenin **etki yönü** yazılı *("modeli iyimser/kötümser yapar")* —
bu yönler doğru mu?

## 7 · YENİ ŞEMA GERÇEKTEN İŞE YARIYOR MU
Sonuç sözlüğüne paket bazlı teslim bilgisi eklendi
*(`teslim_kimlikleri`, `teslim_gecikmeleri_s`)* ve `sim/karsilastirma.py`
bunlarla *"ortak alt küme"* karşılaştırması yapıyor. Dayandığı varsayım:
**paket kimlikleri iki kolda aynı şeyi gösterir.**
🔴 Bu varsayımı **kendin kır**: farklı çekim sayısı yapan bir protokolle,
farklı senaryoda, farklı trafikte. Hâlâ tutuyor mu?

## 8 · ÇALIŞMA NOKTASININ GEREKÇESİ
S2 = +2 dBm projenin **birincil çalışma noktası**. Orijinal gerekçesi
*(K-019)* yeniden üretilemedi ve **yerine yeni bir ölçüt kondu**. O ölçüt
**veriyi gördükten sonra** yazıldı; kayıt bunu açıkça kabul ediyor
*(K-039)*.
🔴 Sor: yeni ölçüt **savunulabilir mi**, yoksa mevcut cevabı korumak için
mi seçilmiş? Aynı ilkeyle başka bir ölçüt yazsan hangi gücü seçerdi?

## 9 · AİLE 1 BU ARAÇLA YAZILABİLİR Mİ
`05-GOZLEM-PENCERESI.md` protokolün görebileceklerini listeliyor. Bir
sonraki aşama *(Aile 1)* bu pencereden beslenen protokoller yazacak.
🔴 **Pencere yeterli mi?** Bağ kalitesi temelli bir protokol bu alanlarla
gerçekten yazılabilir mi — yoksa yazılabilmesi için pencerenin
genişletilmesi mi gerekecek? *(Belge genişletmeyi yasaklıyor.)*

Birinci denetim bu sınıfta bir bulgu çıkardı ve düzeltildi; **başka bir
eksik var mı?**

## 10 · DEPODAKİ BAYAT ÇIKTILAR
Kök dizinde `*_cikti.txt` dosyaları var. Bunlar birer **sonuç gibi
görünüyor**. Hangileri güncel, hangileri değişiklikten önce üretilmiş?
Bir belgede o bayat çıktılara dayanan bir sayı var mı?

## 11 · ÖN-KAYDIN İÇ TUTARLILIĞI
`06-ON-KAYIT.md` hipotezleri, yanlışlanma koşullarını ve mekanizma
kontrollerini ilan ediyor. 🔴 Her hipotez için sor: **bu araç bu
yanlışlanma koşulunu ÖLÇEBİLİR Mİ?** Ölçemeyeceği bir koşul ilan edilmişse
bu, mühürden önce bulunması gereken bir bulgudur.

## 12 · İSTATİSTİK PLANI
`06` Bölüm 3'te Wilcoxon, Holm düzeltmesi, güç analizi ve bir **NaN tuzağı**
uyarısı var. 🔴 Bu planın **kod karşılığı var mı**? Yoksa henüz
yazılmamış bir plan mı? Yazılmamışsa, uyarılan tuzaklara karşı bir koruma
var mı?

---

# ÇALIŞMA BİÇİMİN

1. **Önce oku, sonra koştur, en son yorumla.**
2. Her bulgunun yanında **üretici komut** ve **kaynak dosya:satır**.
3. Bir iddiayı doğrularken **iddianın kendi ölçütünü kullanma.**
   *(Örn. "korunum tutuyor"u korunum fonksiyonunu çağırarak değil, paket
   nesnesi sayarak doğrula.)*
4. ⭐ **Beklenenden iyi çıkan sonuç, kötü çıkan kadar şüphelidir.**
5. Bir şey doğru çıkıyorsa **neden doğru çıktığını** anla.
6. Bir mutasyon yazdığında, **önce o mutasyonun bozduğu yolun sağlam koşuda
   tetiklendiğini göster.** Tetiklenmeyen bir yolu bozmak hiçbir şey
   kanıtlamaz.
7. Deneme için depoyu geçici dizine kopyala; **aslını değiştirme.**

---

# ÇIKTI: `aile0_audit.md` — nasıl güncellenecek

Bu dosya şu an **birinci denetimin raporudur** ve proje onu tarihsel kayıt
sayıyor. 🔴 **İçeriğini SİLME.**

Yapman gereken:

1. Dosyanın **en başına** kısa bir durum bloğu koy: iki denetim var, hangisi
   ne zaman, ikincinin özeti *(kaç yeni bulgu, kapanış hâlâ geçerli mi)*.
2. Birinci denetimin gövdesini **olduğu gibi bırak**, başına
   `# BİRİNCİ DENETİM — 19 Ağustos 2026` başlığı koy.
3. Sonuna `# İKİNCİ DENETİM — <tarih>` bölümünü ekle. Yapısı:

```
## 0. YÖNETİCİ ÖZETİ
    Kapanış geçerli mi: EVET / KOŞULLU / HAYIR — ve neden, üç cümlede

## 1. YENİ BULGULAR
    Her biri: B-24, B-25, … numaralı
    ciddiyet · nerede (dosya:satır) · iddia · ÖLÇTÜĞÜM ·
    üretici komut · neden önemli · öneri

## 2. BİRİNCİ DENETİMİN BULGULARI — kapanma doğrulaması
    Seçtiğin ≥6 bulgu için: gerçekten kapandı mı, nasıl doğruladın

## 3. DOĞRULANAN İDDİALAR
    Yeniden ürettiğin ve TUTAN sayılar

## 4. ÜRETİLEMEYEN İDDİALAR
    Üretici komutu olmayan ya da tutmayan sayılar

## 5. KENDİ MUTASYONLARIN
    En az 8 yeni mutasyon · kaçı yakalandı · örüntü

## 6. ŞÜPHE LİSTESİ SONUÇLARI
    12 maddenin her biri için sonuç

## 7. KAPSAM BEYANINA EKLENMESİ GEREKENLER

## 8. ANLAŞILMAYANLAR
    🔴 Bu bölüm BOŞ BIRAKILAMAZ. Anlamadığın her mekanizma buraya.
    (Birinci denetimin bu bölümündeki 7 maddeden ikisi gerçek kusur çıktı.)

## 9. KOŞTURDUĞUN KOMUTLAR
```

4. Son satır: **depoda hiçbir dosyanın değiştirilmediğini ve hiçbir git
   komutu çalıştırılmadığını** açıkça yaz.

---

# 🔴 SON SÖZ

Bu projenin en güçlü tarafı, kendi hatalarını ölçüp yazmış olması. Birinci
denetim 20 bulgu çıkardı ve proje **kapanmış bir kapıyı yeniden açtı** — bu,
o projenin en değerli kaydı oldu.

Senden beklenen bir onay değil. **Bulacağın her şey, bulunmadığı takdirde
jürinin bulacağı bir şeydir.**

Hiçbir şey bulamazsan bunu da yaz — ama **hiçbir şey bulamamak, aradığın
yerlerin listesiyle birlikte anlamlıdır.** Nereye baktığını yaz.
