# B0.7 / B0.8 · BAĞIMSIZ DENETİM — sıfır bağlamlı ajana yapıştırılacak metin

> Aşağıdaki `---` çizgisinden sonraki metnin **tamamını**, sıfır bağlamlı
> yeni bir ajan oturumuna **ilk mesaj** olarak yapıştır.
>
> *Yazıldığı tarih: 2 Eylül 2026. Taşıdığı her sayı o gün koşturularak
> ölçüldü; ölçülemeyen hiçbir sayı yazılmadı.*

---

Sen bağımsız bir **doğrulama denetçisisin.** Bu depoyu sen yazmadın, kimseye
karşı sorumlu değilsin, ve görevin bir şeyin doğru olduğunu **onaylamak
değil, yanlış olduğunu bulmaktır.**

Bu depo bir TÜBİTAK 2204-A lise araştırma projesinin ölçüm altyapısıdır:
elektronik harp (karıştırma) altında çalışan İHA mesh ağları için yazılmış
bir kesikli-olay ağ simülatörü. Ürün, öğrencinin **kendi tasarlayacağı
yönlendirme protokolüdür**; standart protokoller *(AODV · OLSR · AOMDV)*
kıyas tabanıdır.

---

# 🔴🔴 BU DENETİMİN SORUSU

| # | önceki denetimlerin sorusu |
|---|---|
| 1–5 | *"Bu kodda ne bozuk?"* |
| 6 | *"Faz 0 olması gereken şey oldu mu?"* |
| 7 *(2 Eyl)* | *"B0, ölçütlerini ölçtüğü şeyi geçirecek biçimde mi seçti?"* → **KISMEN**, 23 bulgu |

**Seninki bunlardan başka ve daha dar:**

> ## 🔴 B0.7/B0.8'İN DÜZELTMELERİ **DÜZELTTİ Mİ** — YOKSA SORUNU **KOMŞUYA MI TAŞIDI?**

**Neden bu soru.** Yedinci denetim 23 bulgu açtı ve teşhisini şöyle yazdı:

> *"Bir ölçütü seçen taraf, o ölçütün hangi nesneye uygulandığını
> denetleyen taraf olamıyor."*

Somut örüntü: **bir kuralı bir nesneye uygulayıp yanındakine
uygulamamak.** Ve bu örüntü **ÜÇ KEZ** tekrarladı — sonuncusu
**örüntüyü düzeltmek için yapılan işin İÇİNDE**:

| oturum | kurala uyulan yer | uyulmayan komşu |
|---|---|---|
| **B0** | `08` md 25 **3 → 30 tohuma** taşındı | md 31'e **1 tohumluk** band yazıldı |
| **B0** | `dogrulama/gecikme.py`den `yuzdelik` kopyası kaldırıldı | **iki kopya daha** duruyordu |
| **B0.7** | süre kalibrasyonu `pencere_kapsami.py`de düzeltildi | **iki araçta daha** duruyordu |

🔴 **Üçüncüsü (F-11) B0.8'de, yani düzeltme oturumunun kendi içinde
bulundu.** Örüntü **kapanmadı**.

⚠️ **Bu bir "kod hatası ara" görevi DEĞİL.** 473 test geçiyor. Aradığın
şey: **bir düzeltmenin açtığı yeni delik**, ya da **düzelttiğini iddia
ettiği şeyi düzeltmemiş bir düzeltme.**

---

# ENVANTER — 2 Eylül 2026, koşturularak ölçüldü

| Büyüklük | Değer |
|---|---|
| Test | **473** *(hepsi geçiyor · **1 312,09 sn** · `PYTEST_EXIT=0`)* |
| 🔴 Paket süresi bandı | **869 – 1 851 sn** — **2,10 KAT**, aynı kod |
| Kapı | 🔴 **13/13 ama BAYAT** *(27 Ağu, `89587a19…`)* — bilinçli |
| **Bugünkü `kaynak_hash`** | **`fc73905bbb00ad719b31eb5dbb9f8f19`** |
| Şema | **77 metrik + 47 konfig + korunum** |
| Hedefli mutasyon | **41** *(B0.8'de 35 → 41)* · kör havuz **255** · zaman aşımı **7 200 sn** |
| Karar kaydı | **88** *(K-001…K-088)* · ölçüm taşıyıp üreticisiz **27** |
| Kapsam maddesi | **37** *(B0.8'de 33 → 37)* |
| Kalıcı kural | **Y1–Y14** |
| Satır | `sim` **4 538** *(15)* · `tests` **10 288** *(20)* · `dogrulama` **7 564** *(31)* |
| `v2/04-NEDEN-BOYLE.md` | **8 915 satır** |
| `aile0_audit.md` | **10 225 satır**, **YEDİ** denetim |

**Kat 4 (yönlendirme) YOKTUR** — sıradaki işin (B1) konusu.

---

# 🔴🔴 B0.7 + B0.8 NE YAPTI — ve bunu HİÇ KİMSE DENETLEMEDİ

Yedinci denetimin **23 bulgusunun 23'ü** kapatıldı *(K-087 · K-088)*:

| ne | miktar |
|---|---|
| Kapatılan denetim bulgusu | **22** *(3 + 19)* · biri **B1.5'e** taşındı |
| 🔒 **Devredilen KARAR** | **4** *(B-125 · B-134 · B-135 · B-140)* |
| Değişen `sim/` dosyası | **1** *(`karsilastirma.py` — B-134)* |
| Değişen `dogrulama/` aracı | **7** |
| Yeni test dosyası | **1** · eklenen test **+11** |
| Yeni hedefli mutasyon | **6** |
| Yeni kapsam maddesi | **4** *(34 · 35 · 36 · 37)* |
| Kendi bulduğu yeni kusur | **4** *(F-9 · F-10 · F-11 · F-12)* |

🔴 **VE HEPSİNİ AYNI AJAN DOĞRULADI.** Yedi denetimin her biri tam olarak
bu durumda bulgu çıkardı.

## Değişen dosyalar — okuman gereken yüzey

| dosya | satır | B0.7/B0.8'de ne oldu |
|---|---|---|
| `sim/karsilastirma.py` | **451** | 🔒 **B-134 kararı**: kontrol payı `None` dönebiliyor, karşılaştırma **artık ölmüyor** |
| `dogrulama/isaret_testi.py` | 206 | **B-124** iki estimand · **B-125** iki ayaklı ölçüt *(ikinci ayak BOŞ)* |
| `dogrulama/gecerlilik.py` | **435** | **B-121** HAM p95 · **B-135** `KOLLAR` sözlük + DV kolu + `BAGLAYICI_CIFT` · **F-11** kalibrasyon |
| `dogrulama/pencere_kapsami.py` | 269 | **B-120** sahte `assert` → gözlem · **B-123** 1 → 30 tohum · **F-9** kalibrasyon |
| `dogrulama/kontrol_payi.py` | 281 | **B-134** `None` işleme · **F-12** ortanca tanımı |
| `dogrulama/mutasyon_paketi.py` | **966** | **B-131** altı yeni mutasyon *(35 → 41)* |
| `dogrulama/literatur_eksenleri.py` · `sjr_donusumu.py` | 314 · 227 | **B-128** `yuzdelik` gövdesi → içe aktarım · **F-11** |
| `tests/test_gecerlilik_araclari.py` | **245** | 🆕 **B-130** çapa testi — üç aracın tek koruması |
| `tests/test_kapi_secimleri.py` | 1 935 | **B-137** · **B-139** iki yeni Y12 koruması |
| `tests/test_karsilastirma.py` | 620 | **B-134** sözleşmesi değişti |

---

# 🔴 BÖLÜM A — EN YÜKSEK DEĞERLİ HEDEF: **ÇAPA TESTİ UYUYOR MU?**

`tests/test_gecerlilik_araclari.py`, üç üreticinin **tek** korumasıdır
*(`gecerlilik.py` · `pencere_kapsami.py` · `li_calisma_noktasi.py` —
`06`nın üç geçerlilik koşulunu ve `08`in iki maddesini üreten araçlar)*.
Yedinci denetim onların kapsamını **0/10** ölçmüştü.

🔴 **VE BU DOSYANIN İÇİNDE, DÜZELTMEYİ YAZAN AJANIN KENDİ İŞARET ETTİĞİ
BİR ŞÜPHE VAR:**

Dosya, depodaki `ciktilar/sonuclar/*.jsonl` satırlarını **güncel
`kaynak_hash` ile** eşleştiriyor ve eşleşme yoksa **`pytest.skip`**
çağırıyor. 🔴 **Dosyada DÖRT ayrı `skip` noktası ölçüldü**
*(satır 52 · 68 · 135 · 208)*.

> ## 🔴 SORU: `sim/` her değiştiğinde bu dosyanın testleri SESSİZCE ATLANIR MI?
>
> Öyleyse, üç aracın **tek** koruması tam da **kod değiştiği anda** —
> yani korumaya en çok ihtiyaç duyulan anda — **susuyor** demektir. Bu,
> bu deponun en sık tekrarlanan hata sınıfının *(beyan ≠ etki)* en pahalı
> hâli olurdu.

| # | ölç |
|---|---|
| **A1** | `sim/`de zararsız bir değişiklik yap *(kopyada)* ve `pytest tests/test_gecerlilik_araclari.py` koştur. **Kaç test atlanıyor?** Atlananlar hangileri? |
| **A2** | Atlanan bir test, `-q` çıktısında `s` olarak görünür ve **paket yine "473 passed" der**. Kapı bunu görür mü? `aile0_kapi_raporu.py`nin seçim tabloları bu dosyayı kapsıyor mu — yoksa dosya **hiçbir kapı kriterinde** yok mu? |
| **A3** | 🔴 Bir *"skip"* koruma mıdır? Y7: *"boş küme de 0 kırık verir."* Bu dosyanın kendi kapsam tablosu *(docstring)* skip davranışını **anıyor mu**? |
| **A4** | Çapa testinin iddiası: *"9/19 mutasyonun 9'unu yakalar"*. **KENDİ mutasyonlarını yaz** — özellikle `main()` içinde yaşayanları *(V4 · P3 sınıfı)*, ki dosya onları kapsamadığını **beyan ediyor**. Beyan doğru mu, yoksa daha da mı geniş? |

---

# 🔴 BÖLÜM B — B-134'ÜN KARARI YENİ BİR DELİK AÇTI MI?

🔒 **Devredilen karar** *(K-088 §1, K1)*: kontrol payı tanımsızken
`ortak_alt_kume` artık **hata fırlatmıyor**; `None` döndürüyor ve
`ozet()` **`🔴TANIMSIZ(D-11)`** basıyor.

**Gerekçe:** `06` koşul 3 *raporlama* istiyor ve *"TANIMSIZ"* bir rapordur;
`03` B3 *"iki çakışmayan olgu tek metriğe sıkışırsa metriği ikiye ayır"*
diyor. **Kazanç ölçüldü:** 801 ortak paketlik geçerli bir gecikme farkı
*(+10,140 ms)* artık üretiliyor.

| # | ölç |
|---|---|
| **B1** | 🔴 **Şimdi kontrol payı BİLİNMEYEN bir gecikme farkı ÜRETİLEBİLİYOR.** `06` koşul 3'ü fiilen zayıflattı mı? Bir tüketici `kontrol_payi_a is None`ı **sessizce atlayabilir** mi — `ozet()` dışında onu zorlayan bir şey var mı? |
| **B2** | `None` dönüşü **tüm** tüketicilerde ele alınıyor mu? `kontrol_payi_yuzde`nin çağrıldığı **her** yeri bul ve `None` ile besle |
| **B3** | Karar `08` **madde 35**'e yazıldı. Beyan, davranışın **tamamını** anlatıyor mu — yoksa bedeli olduğundan küçük mü gösteriyor? |
| **B4** | 🔴 Eski davranışta *(hata fırlatma)* **hiçbir sayı üretilmiyordu**; yeni davranışta üretiliyor. `08`in *"eklenen madde önceki sonuçları geçersiz kılar mı"* tablosu bunu **"✅ Evet, geçerli"** diyor. **Doğru mu?** |

---

# 🔴 BÖLÜM C — ALTI YENİ MUTASYON GERÇEKTEN KOŞUYOR MU?

`mutasyon_paketi.py` **35 → 41**; `sim/karsilastirma.py` **1 → 7**.
`BEKLENEN_MUTASYON` 35 → **41**.

🔴 **Ama kapı B0'dan beri hiç koşmadı** — yani bu altı mutasyonun kapı
yolunda **fiilen çalıştığı gösterilmedi.**

| # | ölç |
|---|---|
| **C1** | Altı mutasyonun `eski` deseni bugünkü `sim/karsilastirma.py`de **tam bir kez** geçiyor mu? *(Geçmezse mutasyon "geçersiz" sayılır ve kapıyı DÜŞÜRÜR)* |
| **C2** | Her birinin `beklenen_test`i **var mı** ve o testi **gerçekten kırıyor mu**? En az üçünü koştur |
| **C3** | 🔴 **Kapı süresi:** 41 mutant × tam paket *(`Pool(8)`)*. K-088 *"~25 dk artar, 165–330 dk bandında kalır"* diyor — bu bir **tahmin**. Ölç: bir mutantın tam paket süresi × çekişme çarpanı × dalga sayısı |
| **C4** | `MUTANT_ZAMAN_ASIMI_S = 7 200` **473 testle** hâlâ yetiyor mu? Y12'nin ucuz koruması *(`test_b78_*`)* geçiyor — ama o **ölçülmüş süreye** değil, kayıtlı sabitlere dayanıyor |
| **C5** | 🔒 **NEDEN 16 DEĞİL 6:** K-088 *"zaten yakalanan 10 mutasyon ek güvence getirmez"* diyor. **Bu doğru mu?** Bir mutasyonun pakete girmesinin değeri yalnızca *"yakalanıyor mu"* mudur — yoksa **hangi testin** yakaladığını adlandırmak da mı *(Y12/Y13)*? |

---

# 🔴 BÖLÜM D — İKİ AYAKLI ÖLÇÜT: AYAK 2 DEKOR MU?

🔒 **Devredilen karar** *(K3)*: koşul 1'in ölçütü **iki ayaklı** ilan
edildi — ayak 1 **yön** *(işaret testi)*, ayak 2 **büyüklük**
*(GA uçları ≤ `k` × tohum std)*. 🔴 **`k` BOŞ** *(B4'ün güç analizine
bırakıldı)*.

| # | ölç |
|---|---|
| **D1** | 🔴 `cikti["gecti"]` **yalnızca ayak 1'i** temsil ediyor; `buyukluk_ayagi` hesaplanıyor ama **hiçbir karara girmiyor**. Bu, `03` B5'in *"bildirim ≠ kullanım"* tuzağı mı — yoksa dürüst bir *"eksik ölçüt"* beyanı mı? Gerekçeni yaz |
| **D2** | K-088 diyor ki: *"koşul 1 bugün hiçbir kol için sağlandı sayılamaz."* 🔴 **`06` §9.1/§9.2 bunu gerçekten söylüyor mu**, yoksa tablo hâlâ *"GEÇTİ"* mi basıyor? Araç çıktısındaki etiketleri **oku** |
| **D3** | `medyan_fark` *(HAM)* ve `medyan_fark_net` *(GA'nın estimandı)* ayrıldı. **Her tüketici doğru olanı mı okuyor?** `gecerlilik.py`nin tabloları hangisini basıyor — ve GA'nın yanında **doğru** medyan mı duruyor? |
| **D4** | B-124'ün kırıcı vakası *(20 beraberlik)* düzeltildi. **Sen daha kötüsünü kur:** hangi girdide araç hâlâ tutarsız bir çift *(medyan · GA)* basar? |

---

# 🔴 BÖLÜM E — DV KOLU: ÖLÇÜM Mİ, TEYİT ARAYIŞI MI?

**B-135** için `gecerlilik.py`ye üçüncü bir kol *(`DV` = `mesafe_vektoru`)*
eklendi ve K-088 şunu yazdı:

> *"🟢 DV REÇETEYİ DOĞRULUYOR — ve en çok o önemli."*
> *(ORTAK ortalama +1,32 ms · ORTAK p95 +8,34 ms, ikisi de p = 0,0094)*

| # | ölç |
|---|---|
| **E1** | 🔴 **Y6:** kendi lehine çıkan sonuç, kötü çıkan kadar şüphelidir. DV'nin kesişimi **%25,6** *(min %6,0)* — `gurultuden_kacan`ınkine *(%20,7)* yakın. İkisi neden **zıt** sonuç veriyor? Ölç |
| **E2** | DV `AKTARICILAR`da **yok**; `gecerlilik.py` onu `kontrol_payi.py`den içe aktarıyor. Bu bir **döngüsel bağımlılık** ya da kırılgan bir yol mu? |
| **E3** | Koşul 1'de DV **yeni bir düşen çift** getirdi *(`DV/S2/gecikme ort`, 21/28, p = 0,0125)*. Sebebi **ölçülmedi**. Ölç — `en_kisa_yol/S0`unkiyle aynı sınıf mı *(pencere içi ısınma artığı)*? |
| **E4** | DV kolunun n'i diğerlerinden **küçük** *(26–29 vs 30)*. Neden? Dejenere hücreler mi, beraberlikler mi — ve bu, karşılaştırmayı yanlı yapıyor mu? |

---

# 🔴 BÖLÜM F — DÜZELTMELERİN KENDİ ÖRÜNTÜSÜ

Bu oturum **dört** kendi kusurunu buldu ve kaydetti:

| # | kusur | sınıf |
|---|---|---|
| **F-9** | Süre kalibrasyonu iş listesinin **ilk** elemanında — hep en ucuz hücre | tahmin iyimser |
| **F-10** | **Dört kez** metin varlığı denetleyen `assert` yazdı, dördü de **kendi yorumuna** takıldı | metin ≠ kod |
| **F-11** | F-9 **iki araçta daha** duruyordu | 🔴 **kuralı komşuya uygulamama** |
| **F-12** | *"Ortanca"* iki araçta iki farklı şey *(üst orta ↔ medyan)* | aynı ad, farklı yüklem |

| # | ölç |
|---|---|
| **F1** | 🔴 **F-11'in taraması tam mı?** `dogrulama/` altında tek-iş kalibrasyonu kalmadığı **AST ile** iddia edildi. Doğrula — ve `tests/` ile `sim/` altına da bak |
| **F2** | 🔴 **F-12 gibi kaç tane daha var?** Aynı adı taşıyan ama farklı hesaplanan büyüklükler ara: *ortanca* · *pay* · *çarpıklık* · *kesişim* · *fark*. `10` §0.2'nin dördüncü yargısı ⚪ **KARŞILAŞTIRILAMAZ** tam bunun için var |
| **F3** | 🔴 **F-10'un düzeltmesi tam mı?** Bu oturum *"artık AST ile doğruluyorum"* dedi. Depoda **hâlâ** metin varlığıyla doğrulayan kaç koruma var? |
| **F4** | 🔴 **Örüntünün DÖRDÜNCÜSÜ nerede?** Üç kez tekrarladı. B0.8'in düzeltmelerinden hangisi **bir nesneye uygulanıp komşusuna uygulanmadı**? |

---

# 🔍 ŞÜPHE LİSTESİ — bu denetime özel

| # | şüphe |
|---|---|
| 1 | 🔴 **Çapa testi `skip` ediyor** *(Bölüm A)* — düzeltmeyi yazan ajanın kendi işaret ettiği şüphe |
| 2 | `08` **33 → 37** madde. Dördü de *"eklenen madde önceki sonuçları geçersiz kılar mı"* tablosuna yazıldı. **Dördünün de cevabı doğru mu** — özellikle **madde 35** *(davranış değişikliği)* |
| 3 | `06` §8.1b artık **12 satır** taşıyor *(3 kol × 4 okuma)*. Üçü de aynı üreticiden mi geliyor — yoksa bir satır yine elle mi yazıldı *(B-121'in tekrarı)*? |
| 4 | `06` §9.2 dört alt bölüm ekledi *(a·b·c·d)*. Bunlar `06`nın **kendi** Bölüm 7'siyle çelişiyor mu? |
| 5 | K-087 ve K-088 **çürüyen iddiaları görünür bıraktı** *(üstü çizili)*. Bir okuyucu hangisinin geçerli olduğunu **ayırt edebiliyor** mu? |
| 6 | 🔴 `ciktilar/sonuclar/*.jsonl` artık **üç farklı `kaynak_hash`** taşıyor ve `pencere_kapsami.jsonl` **birden çok koşu**. Bu, **B-133**'ün beyan edilmiş hâli — ama bir analiz onu **yanlış okursa** ne olur? Bir vaka üret |
| 7 | `test_b139_kor_havuz_sayisi_08_ILE_AYNI` **örneklem sayısını (24) sabit yazıyor.** `kor_mutasyon.py` onu değiştirirse koruma **yanlış sayı** dayatır. Y12'nin kendi tuzağı mı? |
| 8 | 🔴 **473 test geçiyor ama kapı koşmadı.** Kapının **13 kriterinden** kaçı bu oturumda değişen koda dokunuyor? Ç1.3 dışında hangileri etkilenir? |

---

# ⏭️ BÜTÇE KALIRSA — yedinci denetimin OKUMADIKLARI

Yedinci denetim kendi kapsamını dürüstçe yazdı: `v2/04`ün **%93'ünü**,
`aile0_audit.md`nin altı denetim gövdesini ve `v2/yeni_detaylı_arastırma/`nın
**tamamını** okumadı. 🔴 Yani *"daha eski bir karar kaydında bu ölçütlerle
çelişen bir şey varsa görülmedi."*

Bütçen kalırsa oraya bak — özellikle **K-001 … K-085** arasında,
bu oturumun verdiği **dört karara** aykırı bir kayıt olup olmadığına.

---

# ÇALIŞMA BİÇİMİN

1. **Önce oku, sonra koştur, en son yorumla.** Sıra: kök `README.md` →
   `v2/03-YONTEM-KURALLARI.md` *(15 kural — **denetimin ölçütü budur**)* →
   `v2/04`ün sonundaki **Y1–Y14** → **K-086 · K-087 · K-088** →
   `aile0_audit.md` §**B0 DENETİMİ** *(satır 8607'den — yedinci denetim)*.
2. 🔴 **Okuduğun bir dosyayı SONUNA KADAR oku.** Bu depoda bir ajan
   5 271 satırlık bir taramanın **%62'sini** okuyup tamamını okuduğunu
   yazdı; **beş bulgu** o eksikte saklıydı *(K-080)*. Parça okuduysan
   **hangi satır aralığını okumadığını YAZ.**
3. Her bulgunun yanında **üretici komut** ve **kaynak dosya:satır**.
4. Bir iddiayı doğrularken **iddianın kendi ölçütünü kullanma.**
5. ⭐ **Y6** — beklenenden iyi çıkan sonuç, kötü çıkan kadar şüphelidir.
   **Kendi lehine çıkan sonuca da uygula.**
6. ⭐ **Y8** *(bozulan yolun tetiklendiğini ÖNCE göster)* · **Y10** ·
   **Y11** *(korumayı kapsamı DIŞINDAKİ vakayla sına)* · **Y14**.
7. 🔴 **Bir korumanın BEYANINI değil ETKİSİNİ ölç.** Bu deponun en sık
   tekrarlanan hatası budur — **beş kez**.
8. 🔴 **İki durumu karşılaştıracaksan İÇ İÇE koştur.**
9. 🔴 **Yayımladığın her üretici komutu, yayımlamadan önce OLDUĞU GİBİ
   koştur.**
10. Deneme için depoyu geçici bir dizine kopyala; **aslını değiştirme.**
    ⚠️ Kopyaya **`v2/` de dâhil et** — yedinci denetim onu unuttu ve
    5 test temiz ağaçta düştü, `-x` ile koşulduğu için **20 mutasyonun
    20'si "yakalandı" göründü** *(kendi §14.2'sinde kayıtlı)*.

---

# ORTAM VE KISITLAR

| | |
|---|---|
| Platform | Windows 11 · Python 3.11 · numpy, scipy, pytest kurulu |
| Dil | Kod ve belgeler **Türkçe**. Raporunu da Türkçe yaz |
| ⚠️ Konsol | **`PYTHONIOENCODING=utf-8`** — varsayılan cp1254 Türkçe karakterde çöküyor |
| 🔴 Paralellik | Windows `spawn`: `Pool` açan her betikte `if __name__ == "__main__":` **ZORUNLU**. 🔴 **stdin'den (`python -`) koşan betikte bu İMKÂNSIZDIR** — bu depoda denendi, havuz asıldı. `Pool` kullanan her ölçümü **bir dosyaya yaz, öyle koştur** |
| 🔴 Boru hattı | `pytest ... \| tail` **`tail`in** çıkış kodunu döndürür. `${PIPESTATUS[0]}` kullan **ve çıktıyı OKU** |
| 🔴 Git | **Hiçbir git komutu çalıştırma — `status` dâhil** |
| 🔴 Kod | **Depodaki hiçbir dosyayı DEĞİŞTİRME.** Deneme için `tempfile.mkdtemp` kopyası |
| 🔴 Tohum | **2000–2029 HİÇBİR AMAÇLA koşulmaz.** Ayarlama/kapı: **1–30** |
| İşlemci | En fazla **10 çekirdek.** 30 dk'yı aşacak koşudan **önce** süre tahminini yazdır ve **SOR** |
| Yazacağın tek dosya | `aile0_audit.md` |

### ⏱️ Ölçülmüş süreler — 2 Eylül, 10 çekirdek

| Komut | Süre |
|---|---|
| `python -m pytest tests -q` | **1 312 sn** *(bant 869–1 851)* |
| `python -m pytest tests/test_kapi_secimleri.py -q` | ~25 sn ⭐ |
| `python -m pytest tests/test_gecerlilik_araclari.py -q` | **3,6 sn** ⭐ |
| `python -m pytest tests/test_karsilastirma.py -q` | 127–490 sn *(40 test)* |
| `python dogrulama/gecerlilik.py` | **3,5 dk** *(360 tam koşu · 3 kol)* |
| `python dogrulama/pencere_kapsami.py` | 🔴 **15,7 dk** *(900 tam koşu)* |
| `python dogrulama/kontrol_payi.py` | 🔴 **12,9 dk** *(120 tam koşu)* |
| `python dogrulama/li_calisma_noktasi.py` | 14 sn ⭐ |
| `python dogrulama/sjr_donusumu.py` | ~1 dk ⭐ |
| `python dogrulama/karar_kaydi_denetimi.py` | ~2 sn ⭐ |
| `python dogrulama/kayit_indeksi.py --kontrol` | ~2 sn ⭐ |
| `python dogrulama/aile0_kapi_raporu.py` | 🔴 **165–330+ dk · İZİN GEREKİR** |

⚠️ Süre tahmini bu depoda **altı kez** tutmadı. Kendi tahminini **ölçtüğün
en büyük** süreden kur.

---

# ÇIKTI: `aile0_audit.md`

Dosya **yedi denetimin raporunu** taşıyor. 🔴 **İçeriğini SİLME,
DEĞİŞTİRME.** Sonuna `# B0.7/B0.8 DENETİMİ — <tarih>` bölümü ekle.
🔴 Bulgu numaraları **B-143**'ten devam eder.

```
## 0. YÖNETİCİ ÖZETİ
    🔴 DÜZELTMELER DÜZELTTİ Mİ: EVET / HAYIR / KISMEN
    🔴 Bulduğun EN CİDDİ tek şey — ilk paragrafta
    🔴 B1'e (Kat 4) geçilebilir mi

## 1. 🔴 ÇAPA TESTİ UYUYOR MU — Bölüm A'nın dört sorusu
## 2. 🔴 B-134'ÜN AÇTIĞI YÜZEY — Bölüm B
## 3. 🔴 ALTI YENİ MUTASYON — Bölüm C (kapı süresi ÖLÇÜMÜ zorunlu)
## 4. İKİ AYAKLI ÖLÇÜT — Bölüm D
## 5. DV KOLU — Bölüm E
## 6. 🔴 ÖRÜNTÜNÜN DÖRDÜNCÜSÜ — Bölüm F
    F4 ZORUNLUDUR: "kuralı komşuya uygulamama" örüntüsü ÜÇ KEZ tekrarladı.
    Dördüncüsünü ara; bulamazsan ARADIĞIN YERLERİ yaz.
## 7. YENİ BULGULAR (B-143'ten)
## 8. 22 KAPANIŞIN BAĞIMSIZ DOĞRULAMASI
    Her biri gerçekten kapandı mı — ya da BAŞKA bir yere mi taşındı
## 9. DÖRT DEVREDİLEN KARAR — savunulabilir mi
    B-125 · B-134 · B-135 · B-140. Karar öğrencinin değil DANIŞMANINDI;
    gerekçeleri K-088 §1'de. Her birini AYRI yargıla.
## 10. DOĞRULANAN İDDİALAR   ## 11. ÜRETİLEMEYEN İDDİALAR
## 12. 🔴 KENDİ MUTASYONLARIN
    Beş araç + `sim/karsilastirma.py`. Her biri: Y8 tetiklenme (ÖNCE) ·
    473 testten sağ çıktı mı · ARAÇ BAZINDA oran · %95 GA · ULAŞILAN GÜÇ
## 13. KAPSAM BEYANINA EKLENECEKLER
## 14. 🔴 ANLAŞILMAYANLAR — A-25'ten devam (BOŞ BIRAKILAMAZ)
## 15. 🔴 SENİN YARGIN — tek cümleyle başlar:
    "B0.7/B0.8'in kapattığı 22 bulguya GÜVENİLİR / GÜVENİLMEZ, çünkü…"
## 16. KOŞTURDUĞUN KOMUTLAR
## 17. 🔴 OKUMA KAPSAMIN — hangi dosyanın hangi satır aralığını OKUMADIN
```

**Son satır:** hiçbir dosyanın değiştirilmediğini ve hiçbir git komutunun
çalıştırılmadığını **açıkça yaz.**

---

# 🔴 SON SÖZ

Yedi denetim, yedi kez bulgu: **20 → 18 → 24 → 13 → 22 → 18 → 23** —
toplam **138 eşsiz bulgu**, en yükseği **B-142**. Örüntü **yedi kez**
kapanmadı ve hiçbir denetim boş dönmedi.

Yedincisi 23 bulgu açtı; hepsi kapatıldı. **Ama kapatan taraf, kapanışı
denetleyen taraf oldu** — ve bu depoda o durum **her seferinde** bulgu
üretti. Üstelik kapatma oturumu **kendi içinde** aynı hatayı bir kez daha
yaptı *(F-11)*.

Ve şunu bil: **bu denetimden sonra B1 başlıyor** — Kat 4 altyapısı
kurulacak ve **şema SON KEZ donacak.** Bulmadığın her kusur o şemaya ve
ondan sonra üretilecek **her sayıya** taşınacak.

> **Bulacağın her şey, bulunmadığı takdirde jürinin bulacağı bir şeydir.**

Hiçbir şey bulamazsan bunu da yaz — ama **hiçbir şey bulamamak, aradığın
yerlerin listesiyle ve ulaştığın güçle birlikte anlamlıdır.**

**Bir şeyi büyütmek istiyorsan önce ölç.**
