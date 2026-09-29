# 11 — REFACTORING ÖNERİSİ

> **Tarih:** 1 Eylül 2026 · **Girdi:** `10-LITERATUR-KOD-KARSILASTIRMA.md`
> **Durum:** 🔴 **PLAN — KOD DEĞİL.** Hiçbir kalem uygulanmadı.
> 🔒 **Öğrenci onayı olmadan tek satır yazılmaz** *(`03` kural 8)*.

---

# 0 · BU BELGE NASIL OKUNUR

Her kalem **altı alan** taşır:

| alan | ne |
|---|---|
| **NE DEĞİŞİR** | somut değişiklik |
| **DOSYA** | dokunulan yer |
| **KAPI** | Faz 0 kapısı yeniden koşulmalı mı *(165–330 dk)* |
| **ŞEMA** | sonuç şeması değişir mi *(değişirse eski satırlar karşılaştırılamaz)* |
| **Y14** | hangi belgedeki hangi sayı **bayatlar** |
| **ÖNERİ** | ve **neden** — 🔴 bu bir öneridir, karar öğrencinindir |

## 0.1 🔴 TEK BELİRLEYİCİ KURAL

> **`sim/` altında bir bayt değişirse `kaynak_hash` değişir, ve o andan
> itibaren kapının 13/13'ü ESKİ KODA aittir.**

Bu yüzden kalemler **`sim/`e dokunanlar** ve **dokunmayanlar** diye ikiye
ayrıldı. Dokunmayanlar kapıyı yeniden açmaz — ve bu, maliyetin tamamıdır.

## 0.2 Maliyet referansları — hepsi bu depoda ÖLÇÜLDÜ

| iş | süre | kaynak |
|---|---|---|
| Faz 0 kapısı, tam | **185,6 dk** *(bant 165–330)* | K-076 |
| Tam test paketi | **15–30 dk** | devir teslim |
| `test_kapi_secimleri.py` | **17 sn** | `08` |
| `mutasyon_on_kontrol.py` | **~0,3 dk** | K-042 |
| 300 tam koşu *(Pool 10)* | **4,3 dk** | `10` §7b |
| `kontrol_payi.py` *(12 koşu)* | **~3 dk** | `08` md 25 |

🔴 **Makine 2,10× oynuyor** *(K-075)* — aşağıdaki her tahmin **bant**tır.

---

# 1 · ÖNCELİK SIRASI — özet

> ## 🟢 B0'DA UYGULANANLAR *(K-086)* — dördü kapandı
> **R-1** *(D-13)* · **R-4** *(A-14 denetimi)* · **R-13** *(yüzdelikler,
> IPDV hariç)* · **R-16a** *(`08`in iki ölü üreticisi)*.
> 🔴 **R-13'ün gerekçesi ölçümle DEĞİŞTİ** — ayrıntı aşağıda.

| # | kalem | `sim/`? | kapı | öncelik |
|---|---|---|---|---|
| **R-1** | D-13 — `Pool` sonuç satırı yazmıyor | ❌ | ❌ | 🟢 **YAPILDI** *(B0.1)* |
| **R-2** | İstatistik katmanı | ❌ | ❌ | 🔴 **Aile 1'in İLK sonucundan önce** — B4. ⚠️ B0.2 yalnız **işaret testi** kullandı *(stdlib, Holm yok)* |
| **R-3** | Mekanizma kapısının penceresi | ❌ | ❌ | 🔒 mühre kadar — ⚠️ B0.4 aynı kararı **kontrol payı** için verdi: `*_pencere` |
| **R-4** | A-14 — `karsilastirma.py` denetlenmedi | ✅ | 🟡 | 🟢 **YAPILDI** *(B0.5)* — bulgu **F-7** |
| **R-13** | Gecikme yüzdelikleri + IPDV | ✅ | 🟡 | 🟢 **yüzdelikler YAPILDI** *(B0.3)* · 🟡 IPDV **B1.5'e** *(K-085: `teslim_dogum_s` gerekiyor)* |
| **R-7** | SJR raporlama ekseni | ❌ | ❌ | 🟢 ucuz, yüksek kazanç |
| **R-16** | Ölü üretici komutlar | 🟡 | 🟡 | 🟢 **(a) YAPILDI** *(B0.6)* — `08`in ikisi üretildi; kalanlar **beyan edildi** |
| **R-12** | PSR metriği | ❌ | ❌ | 🔴 **literatürün ASGARİSİ** *(Y-4)* · tanım kararı gerekir |
| **R-14** | Rota kurtarma Δ + COR | ❌ | ❌ | 🔴 **literatürün ASGARİSİ** *(Y-4)* · Aile 1'e bağlı |
| **R-11** | D-12 — 4 alanın içerik testi | ❌ | ❌ | 🟡 test boşluğu |
| **R-5** | Paket boyutu 512 B | ✅ *(bayrak)* | 🟡 | 🔒 **öğrenci kararı** |
| **R-10** | Bit hızı 2 Mb/s | ✅ *(bayrak)* | 🟡 | 🔒 öğrenci kararı |
| **R-6** | Gölgeleme X_σ | ✅ **model** | 🔴 **evet** | 🔒 öğrenci kararı |
| **R-15** | Karıştırıcı taksonomisi *(tepkisel/taramalı)* | ✅ **model** | 🔴 **evet** | 🔒 öğrenci kararı |
| **R-15b** | 🔒 **KARAR VERİLDİ** — karıştırıcı konumu bir eksen *(J-merkez · J-kenar · J-hedef)* | ❌ *(alan zaten var)* | ❌ | 🟢 **`06` §2.1'e girdi** |
| **R-17** | 🆕 Aile 3 için **kâhin uyarısı** *(literatürün §5.7/§11.1'i)* | ❌ | ❌ | 🔴 **Aile 3'e girilirse zorunlu** |
| **R-8** | 3B + mobilite | ✅ **model** | 🔴 **evet** | 🔒 **stratejik** |
| **R-9** | 🔒 **KARAR VERİLDİ** — adlandırılmış **AODV · OLSR · AOMDV** *(GPSR hariç)* | ✅ **yeni katman** | 🔴 **evet** | 🔴 **Faz 1'in TAMAMI** *(K-081)* |

---

# 2 · `sim/`E DOKUNMAYAN KALEMLER — kapı yeniden açılmaz

## R-1 · 🔴 D-13 — kapının Ç1 yolu sonuç satırı yazmıyor

| | |
|---|---|
| **NE DEĞİŞİR** | `kapi_korunum.ana_matris` ve `uc_durum_matrisi`'nin `Pool` işçileri `olc()` sonucunu **döndürür**, ebeveyn `SonucYazici` ile **yazar** |
| **DOSYA** | `dogrulama/kapi_korunum.py` *(161 satır)* |
| **KAPI** | ❌ kriterleri etkilemez — ama 🔴 **13/13 düzeltme ÖNCESİ koda ait kalır** |
| **ŞEMA** | ❌ değişmez |
| **Y14** | ❌ hiçbir sayı bayatlamaz *(`sim/` sabit)* |

🟢 **ŞEKLİ ARTIK KANITLI:** `dogrulama/literatur_eksenleri.py` bu oturumda
tam olarak bu şekli kullandı ve **300 işin 300'ü satır yazdı**
*(`10` §7b)*. Yani düzeltme bir tasarım tahmini değil, **çalıştığı ölçülmüş
bir desen**.

🔴 **KORUMA DAVRANIŞSAL OLMAK ZORUNDA.** D-13'ün gözden kaçma sebebi
`test_b106_URETIM_YOLLARI_sonuc_YAZIYOR`'un `kayit()`ın **kurulduğunu** AST
ile doğrulaması, satırın **yazıldığını** değil *(K-076 §2)*. Yeni test
küçük bir havuzlu matris koşup **satır sayısını** kontrol etmeli —
`literatur_eksenleri.py`nin `assert yazilan == len(isler)` satırının aynısı.

**MALİYET:** kod **~0,5–1 saat** · yeni test **2–5 dk koşar**
🔴 **artı kapının yeniden koşulması: 165–330 dk** *(13/13'ü düzeltilmiş koda
bağlamak için)*.

**NE ELENDİ:**
- *"Yazıcıyı alt sürece geçir"* — 🔴 imkânsız, dosya tanıtıcısı picklenmez.
- *"İşçiler kendi dosyalarına yazsın, sonra birleştir"* — satır sırası
  belirlenimci olmaz ve `03` B5'in *"her satır anında diske"* şartı
  havuz çöktüğünde sağlanmaz.
- *"Kapıyı yeniden koşturma, 13/13 geçerli say"* — 🔴 Y13: bir kapanış
  iddiası değişikliğin **kodda** bulunduğu gösterilmeden kayda geçmez.

**ÖNERİ:** 🟢 **YAP.** Öğrenci zaten karar verdi *(K-076)*. Kapının yeniden
koşulması R-5/R-6/R-8 kararlarıyla **birleştirilmeli** — üç ayrı kapı
koşusu 9–16 saat, tek koşu 3–5,5 saat.

---

## R-2 · 🔴 İSTATİSTİK KATMANI — Aile 1'in ilk sonucundan önce

| | |
|---|---|
| **NE DEĞİŞİR** | Yeni modül: eşleştirilmiş Wilcoxon *(çift yönlü)* · Holm–Bonferroni · Clopper–Pearson GA · etki büyüklüğü · **açık NaN kontrolü** · güç analizi |
| **DOSYA** | yeni `sim/istatistik.py` *(ya da `dogrulama/`)* — 🔴 **`sim/`e konursa `kaynak_hash` değişir** |
| **KAPI** | ❌ *(`dogrulama/` altına konursa)* · 🔴 **evet** *(`sim/` altına konursa)* |
| **ŞEMA** | ❌ |
| **Y14** | ❌ |

🔴 **YER KARARI ÖNEMLİ VE UCUZ DEĞİL:** `sim/istatistik.py` yazmak
`kaynak_hash`i değiştirir ve kapıyı yeniden açar. **Öneri:
`dogrulama/istatistik.py`** — analiz kodu ölçüm kodu değildir.

**Literatür şartnameyi veriyor** *(`Yöntem Ön-Kayıt…md`)*:
- test seçim tablosu §4.4 *(n≥30 + normal → t; çarpık → Wilcoxon; çok bağ → permütasyon)*
- eşleştirilmiş fark, GA ve etki büyüklüğü formülleri §4.1
- analiz birimi = **tohum** §4.4

🔴 **`06`nın kendi NaN tuzağı ZORUNLU kılıyor:** `scipy.stats.wilcoxon` tüm
farklar sıfırken **hata fırlatmaz, NaN döndürür**; tek NaN Holm'dan sonra
tüm p'leri 1,00 yapar. Ve davranış **örneklem boyutuna bağlıdır** — küçük
bir birim test geçer ve **yanlış güven verir** *(`06` Bölüm 3)*.
🔒 Regresyon testi **gerçek örneklem boyutuyla (n=30)** yazılmalı.

⚠️ **Bağımlılık:** `scipy` depoda **hiç geçmiyor** *(`08` md 21)*.
`03` kural 9 *derin öğrenme* yasaklıyor, `scipy`yi değil — ve
`02-DOGRULANMIS-KAYNAKLAR` zaten *"stdlib + numpy/scipy"* diyor. Serbest.

**MALİYET:** **1–2 gün** *(test dâhil)*. 🔴 **Güç analizinden ÖNCE bitmeli**
— `06` Bölüm 0'ın "kutsal sıra"sı buna bağlı.

**NE ELENDİ:** *"Aile 1'i koş, istatistiği sonra yaz"* — 🔴 `06` Bölüm 3
güç analizini **mühürde** istiyor; sonuç görülüp tohum eklenemez.

**ÖNERİ:** 🟢 **YAP, ve kritik yolun BAŞINA koy.**

---

## R-3 · 🔒 MEKANİZMA KAPISININ PENCERESİ — karar, kod değil

| | |
|---|---|
| **NE DEĞİŞİR** | Ön-kayıtlı H1.1 kapısı `secim_avantaji_ortalama`nın **tüm koşu** hâlini mi, `*_pencere` ikizini mi okuyacak |
| **DOSYA** | `06-ON-KAYIT.md` *(metin)* + `dogrulama/mekanizma_kapisi.py` |
| **KAPI** | ❌ |
| **ŞEMA** | ❌ — **ikiz alanlar zaten var** *(`08` md 31)* |
| **Y14** | mekanizma kapısının üç sayısı *(+0,02827 · +0,05931 · +0,08758)* |

**Ölçülmüş gerekçe:** `secim_avantaji_ortalama` kararlarının
**%15,3–16,8'i** ölçüm penceresi dışında *(K-072)*; ve kontrol baytının
**%17,63–22,84'ü** pencere dışında üretiliyor, **çarpıklık kola göre
değişiyor** *(`08` md 31)* — yani eşleştirilmiş bir kol karşılaştırması
**yanlıdır**.

**ÖNERİ:** 🟢 **`*_pencere` ikizi okunsun.** `08` madde 31 zaten
*"Aile 1'in her karşılaştırması `*_pencere` alanlarını kullanmak
zorundadır"* diyor; kapının kendisinin bunun dışında kalması **tutarsız**.
⚠️ Değişince üç sayı yeniden ölçülmeli *(~16 tam koşu, 5–15 dk)* ve
🔴 **kapı ölçütü GEVŞETİLMEMELİ** *(`03` kural 3)*: 7/8 pozitif ve GA
sıfırı dışlar koşulları aynen kalır. Kapı yeni pencerede geçmezse
**ölçüt değil, sonuç değişir.**

🔒 **26 Eylül mührüne kadar karara bağlanmalı.**

---

## R-4 · 🔴 A-14 — `sim/karsilastirma.py` altı denetimde hiç açılmadı

| | |
|---|---|
| **NE DEĞİŞİR** | 322 satırlık modül **denetlenir**; bulunursa düzeltilir |
| **DOSYA** | `sim/karsilastirma.py` — 🔴 **`sim/` altında** |
| **KAPI** | ❌ *okuma* · 🔴 **evet** *düzeltme çıkarsa* |
| **ŞEMA** | ❌ |
| **Y14** | `08` md 16'nın iki sayısı *(ham +15,45 ms · ortak alt küme +10,14 ms)* |

🔴 **Neden şimdi:** Aile 1'in **her gecikme karşılaştırması** buradan
geçecek, ve `10` §7b.4 az önce ölçtü ki gecikme karşılaştırması
**hayatta-kalan yanlılığının merkezinde**. Denetlenmemiş bir modülün
üstüne ön-kayıtlı bir hipotez kurulamaz.

⚠️ **Y11 uyarısı zaten bir kez ateşledi:** bu modülün girdi kontrolü
yalnızca tohum farkıyla test edilmişti ve `dugum_sayisi` 40→41'de iki kolun
tek ortak paketi yokken karşılaştırmayı **kabul etti** *(K-044/B-26)*.

**MALİYET:** denetim **3–6 saat** · düzeltme çıkarsa + kapı.

**ÖNERİ:** 🟢 **YAP, R-13 ile birlikte** *(ikisi de gecikme yolunda)*.

---

## R-13 · 🟢 GECİKME YÜZDELİKLERİ + IPDV — şema maliyeti SIFIR

| | |
|---|---|
| **NE DEĞİŞİR** | `06` Bölüm 4'e p50/p95/p99 ve IPDV eklenir; analiz `teslim_gecikmeleri_s`den türetir |
| **DOSYA** | `06-ON-KAYIT.md` + `dogrulama/` analiz katmanı |
| **KAPI** | ❌ |
| **ŞEMA** | ❌ — **alan zaten var** *(`kosucu.py:699`)* |
| **Y14** | ❌ *(ekleme; mevcut sayı bayatlamaz)* |

🔴 **GEREKÇE ÖLÇÜLDÜ** *(`10` §7b.4)*: S0→S2'de teslim 0,9962→0,5120
inerken **ortalama gecikme %3,4 DÜŞÜYOR** ama **p95 %26,0 ARTIYOR**.
Ortalama ters yönü gösteriyor. RFC 7679 ve `4:§3.2` tam bunu şart koşuyor.

> ## 🔴 B0.3'TE GEREKÇE DEĞİŞTİ — *"p95 kullan"* YETMİYOR *(K-086)*
> O tablo **havuzlanmış** ve **ham** okumadan geliyordu. 30 tohumla,
> eşleştirilmiş, kesin işaret testiyle ölçüldü:
>
> | okuma | medyan fark | p |
> |---|---|---|
> | HAM ortalama | −3,98 ms | 0,3616 |
> | **HAM p95** | +7,11 ms | **0,5847** 🔴 anlamsız |
> | ORTAK ortalama | **+5,40 ms** | **0,0003** |
> | ORTAK p95 | **+28,15 ms** | **0,0000** |
>
> ⚖️ Sorun *"ortalama yerine p95"* değil, **karşılaştırılan küme**.
> Yürürlükteki kural üç ayaklı ve **kodda zorunlu**: ortak alt küme ·
> p50/p95/p99 · kesişim oranı.

⚠️ **IPDV bir TANIM KARARI gerektirir:** `teslim_gecikmeleri_s` **üretim
sırasında**dır, varış sırasında değil. IPDV *"ardışık **alınan** paket"*
üzerinden tanımlı. İki seçenek: *(a)* tanımı üretim sırasına göre ilan et
*(basit, ama literatürün tanımı değil)*, *(b)* `teslim_kimlikleri` ile varış
sırasını yeniden kur. 🔴 **Karar verilmeden yazılmaz** — yoksa "IPDV" adı
taşıyan ama başka bir şey ölçen bir sayı doğar *(`03` B3)*.

**MALİYET:** yüzdelikler **~1 saat** · IPDV **karar + 2–3 saat**.

**ÖNERİ:** 🟢 **Yüzdelikleri YAP** *(ucuz, gerekçesi ölçülü)*.
🟡 **IPDV'yi ERTELE** — Aile 1'in darbeli senaryolarında *(S3/S4)* değeri
yüksek, ama tanım kararı 26 Eylül'e yetişmezse zorlamayın.

---

## R-7 · 🟢 SJR RAPORLAMA EKSENİ

| | |
|---|---|
| **NE DEĞİŞİR** | Her sonuç tablosuna SJR/JSR **sütunu** eklenir; H1.2 taraması dBm **ve** SJR ile raporlanır |
| **DOSYA** | `dogrulama/sjr_donusumu.py` **zaten yazıldı ve koştu** · `06` metni |
| **KAPI** | ❌ |
| **ŞEMA** | ❌ *(rapor katmanı)* |
| **Y14** | ❌ |

🔴 **Boşluk A'nın tablosu bu eksen olmadan literatüre bağlanamaz** —
boşluk *"değişen SJR altında"* diye tanımlı. Ölçüm `10` §4'te.

**ÖNERİ:** 🟢 **YAP.** Maliyeti neredeyse sıfır, kazancı büyük.
⚠️ Ve `10` §4.3(c)'nin gerekçesi **rapora aynen girmeli**: karıştırıcı
gücümüz literatürün bağ-seviyesi etkinlik eşiğinin *(J/S 10–15 dB)* altında
ve bu **bilinçli** — ağın dinamik aralığının ortası seçildi.

---

## R-16 · 🟢 ÖLÜ ÜRETİCİ KOMUTLAR

| | |
|---|---|
| **NE DEĞİŞİR** | `scratchpad/` altındaki **9 betiğe 14 referans** ya yeniden üretilir ya *"üretilemiyor"* diye işaretlenir |
| **DOSYA** | `04` *(6)* · `08` *(2)* · `sim/kosucu.py` *(1)* · `dogrulama/mutasyon_paketi.py` *(1)* · `tests/` *(4)* |
| **KAPI** | ❌ · ⚠️ `sim/kosucu.py`de **yalnızca yorum** değişir — 🔴 ama yorum da bayttır, `kaynak_hash` değişir |
| **ŞEMA** | ❌ |
| **Y14** | 🔴 `08` md 31 *(%17,63–22,84)* ve Ç4 çalışma noktası *(1,761 / 0,277 Mbps)* — **ikisi de mühür bekleyen sayfada** |

🔴 **`08` MÜHÜRLENMEDEN ÖNCE ÇÖZÜLMELİ.** Y14: *"mühürlenecek bir belgedeki
sayı, yeniden koşulmadan mühürlenemez."*

**Üç seçenek, üçü de dürüst:**

| # | ne | maliyet |
|---|---|---|
| a | Betikleri **`dogrulama/` altında yeniden yaz**, sayıları yeniden ölç | b105: 40 koşu ~2–5 dk · b109: 60 koşu ~3–8 dk |
| b | Sayıları **"üretilemiyor"** diye işaretle, üretici satırını sil | ~1 saat |
| c | 🔴 Sayıları **sil** | ⛔ bilgi kaybı |

**ÖNERİ:** 🟢 **(a) — ama yalnızca `08`in İKİ sayısı için.** Kalan 7 betik
`04` ve `tests/` içinde ve mühür beklemiyor; onlar için **(b)** yeterli.
🔴 `sim/kosucu.py:302`deki yorum düzeltmesi **kapı koşusuna denk
getirilmeli** *(tek başına 165–330 dk'ya değmez)*.

---

## R-12 · 🟡 PSR METRİĞİ — *"PDR tek başına yanıltıcıdır"*

| | |
|---|---|
| **NE DEĞİŞİR** | Xu vd.'nin PSR'si *(MAC'te başarıyla gönderilen / gönderilmek istenen)* raporlanır |
| **DOSYA** | analiz katmanı · muhtemelen `sim/kosucu.py` *(yeni sayaç gerekirse)* |
| **KAPI** | ❌ *(türetilebilirse)* · 🔴 **evet** *(yeni sayaç gerekirse)* |
| **ŞEMA** | 🔴 **yeni sayaç gerekirse EVET** — ve şema Aile 1 başlamadan donmuş olmalı |
| **Y14** | ❌ |

🔴 **GEREKÇE GÜÇLÜ:** literatürün ölçtüğü *(4:§2.2)* — **reaktif
karıştırıcıda gönderici PSR %99–100 kalırken alıcı PDR %0'a düşer**;
saldırı gönderici tarafından **görünmez**. PDR+PSR çifti karıştırıcı
sınıfının **imzasıdır**.

🔴 **AMA TANIM KARARI VERİLMEDİ.** Mevcut alanlar `mac_gonderilen` ·
`mac_deneme` · `mac_dusurmesi` · `kuyruk_tasmasi` *(kosucu.py:330-350)*.
Hangisinin pay, hangisinin payda olduğu **bir karardır** ve bu belge onu
vermez. 🔴 *"Türetilebilir"* demek *"türetildi"* demek değildir.

**ÖNERİ:** 🟡 **Önce ÖLÇ, sonra karar ver.** Yarım günlük bir çalışma:
dört sayaçtan PSR adayları kurulur, S0/S2'de koşulur, hangisinin Xu'nun
tanımına karşılık geldiği **gösterilir**. Şema değişikliği gerekiyorsa
🔒 **Aile 1'den önce** yapılmalı — sonradan eklenemez *(`03` B5)*.

---

## R-14 · 🟡 ROTA KURTARMA GECİKMESİ Δ + COR

| | |
|---|---|
| **NE DEĞİŞİR** | Δ = \|T_r − T_d\| *(4:§6.2)* ve COR *(4:§6.6)* ölçülür |
| **DOSYA** | analiz katmanı + protokol arayüzü |
| **KAPI** | ❌ · 🔴 evet *(sayaç `sim/`e girerse)* |
| **ŞEMA** | 🔴 muhtemelen **evet** |
| **Y14** | ❌ |

🔴 **BU, LİTERATÜRÜN İKİNCİ BOŞLUĞUDUR** *(dosya 9 §2)*:
*"OLSR, AODV, GPSR ve AOMDV'nin RF karıştırma altında **saniye ölçeğinde
rota kurtarma gecikmesi** bildiren doğrudan birincil kaynak literatürde
bulunamamıştır."* Ve dosya 4 §6.8 aynı boşluğu bağımsız olarak beyan
ediyor.

⚠️ **Ama bugünkü araçta bir sorun var:** Δ'nın tanımı *"arıza nedeniyle
düşürülen ilk veri paketi"* ile *"kaynağın tabloyu yeniden hesapladığı an"*
arasındaki farktır. **Sabit topolojide "arıza" yalnızca karıştırmadan
gelir** ve rota "kopmaz" — PER yükselir. Yani Δ bu araçta **tanımı gereği
farklı bir şeydir**.

**ÖNERİ:** 🟡 **Aile 1'in kolları yazılana kadar ERTELE.** Δ ölçülebilmesi
için protokolün *"rotam koptu"* diyebilmesi gerekir; bugünkü aktarıcılar
öyle bir olay üretmiyor. 🔴 Ama **`06`ya şimdiden yazılmalı** ki sonradan
eklenmiş görünmesin.

---

## R-11 · 🟡 D-12 — `PaketGorunumu`'nun dört alanı

| | |
|---|---|
| **NE DEĞİŞİR** | `atlama_sayisi` · `bayt` · `kaynak` · `ttl` için **içerik testi** yazılır |
| **DOSYA** | `tests/test_gozlem.py` |
| **KAPI** | ❌ · ⚠️ Ç5'in beklenen test sayısı **55'ten artar** *(`KAPI_SECIMLERI["Ç5"]`)* — kaç artacağı uygulayanın kararı, 🔴 **tahmin yazılmadı** |
| **ŞEMA** | ❌ |
| **Y14** | `08` md 22'nin **14** sayısı *(alan hâlâ okunmuyor — sayı DEĞİŞMEZ)* |

🔴 **BEYAN DEĞİŞMEZ, EKSİK OLAN TEST.** B-27b'nin içerik güvencesi
*(her alanın değeri bağımsız hesapla karşılaştırılır)* bu dört alan için
**hiç sınanmadı**. Aile 3 onları okumaya başladığında **doğrulanmamış** bir
sayı alacak.

🟢 Ve `10` §6.3 gerekçeyi güçlendiriyor: bu alanlar **ölü ağırlık değil,
Aile 3'ün sensör takımı**.

⚠️ **Y12:** `KAPI_SECIMLERI`deki Ç5 sayısı **elle tutulan bir sabittir** ve
bu depoda **iki kez** bayatladı. Test eklenirken sayı da güncellenmeli;
`test_kapi_secimleri.py` bunu 17 sn'de yakalar.

**MALİYET:** **2–4 saat.**

**ÖNERİ:** 🟢 **YAP** — ucuz ve `03` kural 10 *("bir bulguyu 'düşük
öncelik' deyip bırakma")* zaten zorunlu kılıyor.

---

# 3 · `sim/`E DOKUNAN KALEMLER — kapı yeniden açılır

## R-5 · 🔒 PAKET BOYUTU 512 B — ÖLÇÜLDÜ, "ucuz" DEĞİL

| | |
|---|---|
| **NE DEĞİŞİR** | `paket_bayt` 1024 → 512 *(ya da 512 bir tarama ekseni olur)* |
| **DOSYA** | `sim/config.py` — **tek sabit** |
| **KAPI** | 🟡 varsayılan değişirse **evet** · ❌ yalnızca eksen eklenirse |
| **ŞEMA** | ❌ *(`paket_bayt` zaten konfigde ve satıra yazılıyor)* |
| **Y14** | 🔴 **geniş** — aşağı bak |

### Ölçülen etki *(`10` §7b.2 · 30 tohum · eşleştirilmiş)*

| | 512 B | 1024 B | fark | işaret |
|---|---|---|---|---|
| S2 teslim | **0,5597** | 0,5120 | **+0,0477** | 28/30 |
| S2 gecikme | 0,0210 s | 0,0426 s | −0,0216 | 0/30 |
| menzilde PER | %8,88 | %16,97 | — | analitik |
| sunulan airtime | %4,288 | %8,384 | **yarıya** | analitik |

🔴 **BU BİR "LİTERATÜRE UYUM" DEĞİL, ÇALIŞMA NOKTASI TAŞIMASIDIR.**
K-039 çalışma noktasını *"dinamik aralığın ortası (0,5076)"* diye seçti;
512 B'da teslim **0,5597** olur ve ortadan uzaklık **0,0044 → 0,0521**
*(12 kat)* çıkar. Yani gerekçe **yeniden ölçülmeden geçersizdir**.

### Y14 — bayatlayacak sayılar *(varsayılan değişirse)*

| belge | sayı |
|---|---|
| `08` md 15 | S0 tabanı **0,9938** · menzil PER'i **%16,97 (1024 B için)** |
| `08` md 16 | ham fark **+15,45 ms** · ortak alt küme **+10,14 ms** |
| `08` md 12 | alıcı kilidi **%0,028** |
| `08` md 25 | kontrol payı **%13,71–33,25** vs **%1,65–1,87** |
| `08` md 31 | pencere dışı kontrol baytı **%17,63–22,84** |
| `config.py` | **kalibrasyon tablosunun TAMAMI** *(7 güç × 3 sütun)* |
| `06` §SENARYOLAR | ulaşılabilir çift oranları · **S2 = +2 dBm gerekçesi** |
| kapı | Ç1.4 **%0,156** · Ç4.2 **1/6,29** |

**NE ELENDİ:**
- *"512 B'a geç, literatür öyle diyor"* — 🔴 aynı literatür dosyası
  *(11:§4)* 1024'ü de listeliyor, ve normalize yükümüz baseline'la
  **birebir aynı** *(`10` §2.4)*.
- *"Paket boyutunu değiştir ama gönderim hızını da 4 pkt/s yap"* —
  bu **iki eksen birden** demektir; `03` B1: her seferinde bir değişken.

**ÖNERİ:** 🟢 **1024 B BİRİNCİL KALSIN + 512 B İLAN EDİLMİŞ DUYARLILIK
EKSENİ OLSUN.** Gerekçe üç ayaklı ve üçü de ölçülü: *(1)* normalize yük
baseline'la birebir, *(2)* 1024 literatürün kendi listesinde,
*(3)* 512'ye geçmek çalışma noktasını taşır ve kalibrasyonu geçersiz kılar.
🟢 **Ve duyarlılık ekseninin verisi ZATEN ÜRETİLDİ** — kapı koşusu
gerekmez, çünkü varsayılan değişmiyor.

---

## R-10 · 🟡 BİT HIZI 2 Mb/s — Li'nin kendi çalışma noktası

| | |
|---|---|
| **NE DEĞİŞİR** | `bit_hizi_bps` 1e6 → 2e6 |
| **DOSYA** | `sim/config.py` |
| **KAPI** | 🔴 **evet** |
| **ŞEMA** | ❌ |
| **Y14** | 🔴 **Faz 0'ın TÜM sayıları** — kapı dâhil |

🟢 **Kazanç ölçülmüş** *(B-109)*: Li'nin kendi noktasında araç **iki mutlak
sayıyı da** üretiyor — tek atlama tavanı **1,761** vs Li'nin **1,7 Mbps**
*(%3,6)*, uzun zincir verimi **0,277** vs **0,25 Mbps** *(%10,8)*.
Bugün depo yalnızca **oranı** karşılaştırıyor, yani replikasyon
**olduğundan zayıf** sunuluyor.

🔴 **Ama bedel çok büyük:** Faz 0'ın her sayısı yeniden koşulur, kapı
yeniden koşulur *(165–330 dk)*, `08` baştan yazılır.

**ÖNERİ:** 🔴 **VARSAYILANI DEĞİŞTİRME.** Onun yerine **R-16(a)** ile
`b109_li.py` yeniden yazılsın ve `08` Ç4 *"Li'nin kendi çalışma noktasında
ölçüldüğünde iki mutlak sayı da tutuyor"* cümlesini **üretilebilir bir
üreticiyle** taşısın. Kazancın tamamı **koşu noktasını değiştirmeden**
elde ediliyor. 🟢 Bu, en iyi maliyet/fayda oranına sahip kalem.

---

## R-6 · 🔒 GÖLGELEME X_σ

| | |
|---|---|
| **NE DEĞİŞİR** | `yol_kaybi_db_statik`e `X_σ ~ N(0, σ²)` eklenir |
| **DOSYA** | `sim/radio.py` + yeni RNG akışı + `sim/config.py` |
| **KAPI** | 🔴 **evet** |
| **ŞEMA** | 🟡 yeni konfig alanı |
| **Y14** | 🔴 **Faz 0'ın TÜM sayıları** |

🔴 **VE İKİ AĞIR YAN ETKİ:**

1. **Yeni bir RNG akışı** gerekir *(`07`nin akış listesi "kapalıdır")* ve
   akış eklemek **çekim sırasını kaydırır** — K-040'ta `beacon_faz`
   eklemesi tam bunu yapmış, **dört belgede bayat sayı** bırakmıştı *(B-28)*.
2. 🔴 **`03` kural 14:** durum tutan yeni bir bileşenin **başlangıç koşulu**
   sorulmalı. Gölgeleme bağ başına mı sabit, her iletimde mi yeniden
   çekilir? İkisi **tamamen farklı** modeller — ve literatür *(10:§2.2)*
   bunu söylemiyor.

⚖️ **Yön ölçülü ve hipotezin ALEYHİNE:** `08` md 1 — gölgelemesiz model bağ
geçişlerini **keskin** yapıyor, bu da *"tazelik gerektiren yaklaşımların
kazancını azaltır"*. Yani gölgeleme eklemek bizim lehimize çalışırdı ve
**tam bu yüzden** eklemenin gerekçesi ölçüm olmalı, tercih değil.

**ÖNERİ:** 🔴 **EKLEME. Beyanı GÜÇLENDİR.** `08` md 1 zaten yazılı;
eklenecek şey **ölçülmüş PER-mesafe eğrisi** *(d = R'de %16,97,
d = 1,2R'de ≈%100)*. Gerekçe: *(a)* kapı 165–330 dk, *(b)* RNG kayması riski
gerçek ve yaşanmış, *(c)* başlangıç koşulu kararı literatürde yok,
*(d)* etkisi **hipotezin aleyhine**, yani dışlanması **muhafazakâr**.
🟢 `12-YOL-HARITASI.md`de **gelecek çalışma** olarak yazılsın.

---

## R-15 · 🔒 KARIŞTIRICI TAKSONOMİSİ — 3 sınıf → 11 sınıf

| | |
|---|---|
| **NE DEĞİŞİR** | Tepkisel · taramalı · takipçi · **kontrol kanalı** · çoklu karıştırıcı |
| **DOSYA** | `sim/radio.py` · `sim/mac.py` *(tepkisel MAC'e girer)* · `sim/config.py` |
| **KAPI** | 🔴 **evet** |
| **ŞEMA** | 🔴 **evet** |
| **Y14** | 🔴 geniş |

Literatür **11 karıştırıcı sınıfı** sayıyor *(4:§7.1)*; depoda **3** var
*(sabit · darbeli · hareketli)*.

🔴 **En zararlısı modellenmemiş:** *kontrol kanalı karıştırması* —
HELLO/TC/beacon'ı seçici bastırıp **veri kanalını hiç bozmadan** topoloji
görüşünü çökertir; LTE'de barajdan **~20 dB daha J/S-verimli** olduğu
bildirilmiş.

⚠️ **Tepkisel karıştırıcı MAC'e girer** ve `08` md 4/5 onu **bilinçli**
dışlıyor: *"MAC ile iç içe geçmiş, ayrı bir araştırma"* *(K-008)*.

**ÖNERİ:** 🔴 **EKLEME.** Ama 🟢 **adlandır:** `06`daki S1–S5 senaryoları
literatürün taksonomisindeki adlarıyla etiketlensin
*(S1/S2 = **sürekli/baraj** · S3/S4 = **periyodik** · S5 = **mobil**)*.
Maliyeti sıfır, kazancı büyük: Boşluk A'nın iddiası
*"adlandırılmış karıştırıcı sınıfları altında"* diye kurulabilir hale gelir.

---

## R-8 · 🔒🔒 3B + MOBİLİTE — stratejik karar

| | |
|---|---|
| **NE DEĞİŞİR** | `konumlar` 2B → 3B; 3B Gauss-Markov mobilite *(α=0,85 · adım 0,5 s · 10–30 m/s)* |
| **DOSYA** | `sim/topology.py` · `sim/config.py` · `sim/radio.py` · muhtemelen `sim/mac.py` · yeni `sim/mobilite.py` · yeni RNG akışları |
| **KAPI** | 🔴 **evet** |
| **ŞEMA** | 🔴 **evet** *(konum 3 bileşen, mobilite alanları)* |
| **Y14** | 🔴 **HER ŞEY** |

### Ne kazanılır

🟢 **Boşluk B** *(`Açık Araştırma Alanları.md` A1: "mobilite ve jamming ayrı
modelleniyor; birleşik 3B model doğrulanamadı")* hedeflenebilir hale gelir.

### 🔴 Ne ödenir — ölçülmüş

| kalem | maliyet |
|---|---|
| 3B geometri + mobilite kodu | **1–2 hafta** |
| `03` kural 14 — mobilitenin **başlangıç koşulu** *(t=0'da durağan mı?)* | 🔴 `03` B6'nın ⭐⭐⭐ tuzağı: *"mobilite modelinin durağan dağılımı düzgün değilken başlangıç konumları düzgün çekilirse her koşu bir geçiş rejiminde başlar ve tarama SESSİZCE başka bir şeyi ölçer"* |
| Kalibrasyonun tamamı yeniden | 🔴 S2 = +2 dBm **yeniden seçilmeli** |
| Kapı yeniden | **165–330 dk** *(muhtemelen birkaç kez)* |
| `08`in 32 maddesi | md 7 ve md 17 kalkar, **yeni maddeler doğar** |
| Faz 0'ın **altıncı kapanışı** | — |

🔴 **VE ÖLÇÜLMÜŞ BİR EK RİSK:** `10` §7b.3 az önce gösterdi ki **gözlem
tabanlı kol 200 s'de henüz yakınsamamış** *(8/30)*. Mobilite eklenince
topoloji sürekli değişir ve yakınsama **hiç tamamlanmayabilir** — o zaman
`06` Bölüm 5 koşul 1 *("sonuç koşu uzunluğundan bağımsız")* **düşer** ve
koşu süresi 350 s'den yukarı çekilmek zorunda kalır, bu da her koşuyu
pahalılaştırır.

**ÖNERİ:** 🔴 **26 EYLÜL'DEN ÖNCE YAPMA.** Takvim analizi
`12-YOL-HARITASI.md`de; kısası: **~3,5 hafta kaldı ve arada iki onay kapısı
var.** 🟢 **Gelecek çalışma olarak yaz** — literatürle gerekçelendirilmiş
bir *"3B + mobilite"* bölümü, yapılmamış bir işten daha güçlüdür, çünkü
**neden yapılmadığı ölçülmüştür.**

---

## R-9 · 🔒🔒 ADLANDIRILMIŞ AODV / OLSR / GPSR — en büyük çatal

| | |
|---|---|
| **NE DEĞİŞİR** | Üç protokolün RFC uyumlu uygulaması |
| **DOSYA** | 🔴 **`sim/` DIŞINDA** — yeni `protokoller/` *(K-084)*. Deneyle doğrulandı: `sim/` dışı değişiklik `kaynak_hash`i **değiştirmiyor** → protokol eklemek kapıyı **yeniden açmıyor** |
| **KAPI** | 🔴 **evet** *(Ç5 gözlem sözleşmesi gerçek protokolle YENİDEN sınanmalı — `08` Ç5 KAPSAMAZ tablosu bunu zaten şart koşuyor)* |
| **ŞEMA** | 🟡 protokol teşhis alanları |
| **Y14** | `06` H1.1'in tamamı |

### İki dürüst iddia — `10` §5.4

| | iddia | maliyet |
|---|---|---|
| **A-dar** | *"…atlama-sayısı temelli ve bağ-kalitesi temelli yönlendirme **sınıflarının** SJR'ye bağlı PDR/E2E bozunumu"* | 🟢 **sıfır** |
| **A-tam** | *"**OLSR, AODV ve GPSR** için SJR'ye bağlı PDR/E2E"* | 🔴 **2–4 hafta** + kapı + ön-kayıt revizyonu |

🟢 **A-tam için literatür hazır:** RFC parametreleri `Baseline…md`
§8.1/§8.2'de tam tablo hâlinde *(AODV: HELLO 1 s, ALLOWED_HELLO_LOSS 2,
RREQ_RETRIES 2, NET_TRAVERSAL_TIME 2,8 s · OLSR: HELLO 2 s, TC 5 s,
NEIGHB_HOLD_TIME 6 s, TOP_HOLD_TIME 15 s)*.

🔴 **AMA ÜÇ SERT ENGEL:**

1. 🔄 **`03` kural 4 — REVİZE EDİLDİ, engel TERSİNE DÖNDÜ.** Eski hâli
   *"ayarlanabildiği kadar iyi ayarlanır"* idi ve tarama maliyeti
   getiriyordu. **Yeni hâli:** *"mimarisine sadık kurulur; hiçbir kol —
   bizimki dâhil — senaryo başına ayarlanmaz."*
   🟢 **Tarama maliyeti KALKTI.** 🔴 Yerine gelen: **uygunluk testleri**
   *(U1–U4, `06` §4.2)* — bir protokol onları geçmeden *"kuruldu"*
   sayılmaz. Risk *"az ayarladık"*tan ***"eksik uyguladık"***a taşındı.
2. **GPSR konum ister** — ve `05` §B *"diğer düğümlerin konumu"*nu yasaklıyor
   *("ancak bir pakette geldiyse ve bayt maliyeti ödendiyse")*. GPSR
   uygulanabilir ama **beacon'a konum koyup bedelini ödemek** zorunda;
   bu, kontrol düzlemi bütçesini değiştirir *(`08` md 25 **4,0–38,0 kat**
   fark ölçmüş — 🔴 **B-169:** burada **8,3–17,8** yazıyordu, o sayı 3
   tohumluk ve B0.4'te geri alınmıştı)*.
3. **OLSR'ın MPR'i** `08` md 6'da kapsam dışı; kaldırmak **yeni bir kapsam
   maddesi** değil, **bir mühür revizyonu** demektir.

**NE ELENDİ:**
- *"Sadece AODV yaz, o evrensel taban"* — 🔴 boşluk **üçünü birden** istiyor;
  biri eksik olursa iddia yine dar, ama maliyet üçte bir değil.
- *"`mesafe_vektoru`yu AODV diye adlandır"* — ⛔ **`03` kural 11'in ihlali**:
  bir iddiayı onu üreten kod satırını gösteremeden yazma. O 40 satır AODV
  değil; RREQ/RREP/RERR, sıra numarası, yerel onarım **yok**.

**🔒 KARAR (1 Eylül 2026, K-081):** **A-tam seçildi** — AODV · OLSR · AOMDV adlarıyla kurulacak, **GPSR hariç**. Aşağıdaki eski öneri kayıt için duruyor.

**ESKİ ÖNERİ *(geçersiz)*:** 🟢 *A-dar'ı seç, A-tam'ı gelecek çalışma yaz.*
Gerekçe: *(1)* `06` ve `08` zaten sınıf düzeyinde ön-kayıtlı ve mühür
yaklaşıyor; *(2)* dosya 9 §2'nin **ikinci boşluğu** *(rota kurtarma
gecikmesi)* de sınıf düzeyinde ölçülebilir; *(3)* `03` kural 4 gereği üç
protokolü **ayarlamadan** koşmak, onları straw-man yapar — ve bu, projenin
en ağır yasaklarından biri.
🔴 **Ama iddia cümlesi DÜRÜSTÇE DARALTILMALI** — `10` §5.4'teki A-dar
metni `06`ya ve rapora aynen girmeli.

---

## R-15b · 🟢 KENAR / DAĞITIK KARIŞTIRICI EKSENİ — kod değişikliği YOK

| | |
|---|---|
| **NE DEĞİŞİR** | Karıştırıcı konumu bir **tarama ekseni** olur: {merkez, kenar, 3 dağıtık} |
| **DOSYA** | 🟢 **hiçbiri** — `karistirici_konum` zaten `Konfig` alanı *(`config.py:186`)* |
| **KAPI** | ❌ |
| **ŞEMA** | ❌ — alan zaten sonuç satırına yazılıyor |
| **Y14** | ❌ *(varsayılan değişmiyor)* |

🔴 **GEREKÇE ÇİFT KAYNAKLI:**
- `08` madde 18 *(kendi beyanımız)*: tek merkezî karıştırıcı **"sonucu bizim
  lehimize çevirebilecek en büyük tek modelleme sınırıdır"** — H1.1'in
  mekanizması *"kaçacak yer olmasına"* dayanıyor.
- `FANET'te EH…md` §11 *(literatür)*: karıştırıcı sayısı/konumu
  **{1 merkezî, 1 kenar, 3 dağıtık}** bağımsız değişken.

⚠️ **Çoklu karıştırıcı `sim/radio.py` değişikliği ister** *(bugün tek
`Karistirici` nesnesi)* — o R-15'te kalır. **Kenar karıştırıcı istemez.**

**MALİYET:** tarama **0,5 gün** · koşu **15–31 dk** *(8 nokta × 30 tohum)*.

**ÖNERİ:** 🟢 **YAP.** `08` madde 18'in *"en büyük tek sınır"* beyanı, ölçülmüş
bir duyarlılık ekseniyle desteklenmeden rapora girerse zayıf kalır.

---

## R-17 · 🔴 AİLE 3 KÂHİN UYARISI — literatürün kendi kodunu kopyalama

| | |
|---|---|
| **NE DEĞİŞİR** | `06` Aile 3 bölümüne bir **yasak notu** girer |
| **DOSYA** | `06-ON-KAYIT.md` *(metin)* |
| **KAPI** | ❌ · **ŞEMA** ❌ · **Y14** ❌ |

🔴 **`10` §7c Y-1:** `Jamming-Aware Q-Learning Ödül Fonksiyonu.md` §7.1
*"ajan jammer parametrelerini bilemez"* diyor, ama **§5.7'nin formülü**
`1{d(j,J) ≤ R_J}` ve **§11.1'in referans kodu**
`link_metrics['in_jamming_radius'][j]` **doğrudan simülatörden okuyor**.

🔴 **Aile 3'e girilirse §11.1 KOPYALANAMAZ.** Kullanılacak olan §7'dir:
`ρ_j`, PER'in taban değerinden sapmasından **tahmin edilir**. Kaynaklar
`05`'te zaten var: `son_iletim_sonucu` *(ACK/NACK → PER)* ve
`olculen_gurultu_w` *(dinleme → SINR)*.

**ÖNERİ:** 🟢 **`06`ya şimdi yaz** — Aile 3 ertelenmiş olsa bile.
Ertelenmiş bir aileye girildiğinde ilk yapılacak şey literatürün referans
kodunu açmaktır; uyarı **o andan önce** yazılı olmalı.

---

# 4 · TOPLAM MALİYET — üç paket

| paket | kalemler | süre | kapı | 26 Eylül |
|---|---|---|---|---|
| 🟢 **ASGARİ** *(önerilen)* | R-1 · R-2 · R-3 · R-4 · R-7 · R-11 · R-13 · R-16 | **~5–8 gün** | **1 koşu** *(3–5,5 sa)* | 🟢 **tutar** |
| 🟡 **ORTA** | asgari + R-5 *(eksen)* · R-10 *(üretici)* · R-12 · R-15 *(adlandırma)* | **~8–12 gün** | 1 koşu | 🟡 **sıkışık** |
| 🔴 **GENİŞ** | orta + R-6 · R-8 · R-9 | **~5–8 hafta** | **3+ koşu** | 🔴 **TUTMAZ** |

🔴 **Bugün 1 Eylül; 26 Eylül'e 25 gün var ve arada İKİ ONAY KAPISI duruyor.**
Ayrıntı: `12-YOL-HARITASI.md`.

---

# 5 · 🔒 KARAR GEREKTİREN BEŞ SORU

Bu belge bunları **cevaplamaz**; ölçülmüş seçenekleri sunar.

| # | soru | önerilen | nerede |
|---|---|---|---|
| 1 | Mekanizma kapısı hangi pencereyi okuyacak? | `*_pencere` ikizi | R-3 |
| 2 | Paket boyutu: 512 birincil mi, duyarlılık ekseni mi? | **duyarlılık ekseni** | R-5 |
| 3 | Boşluk A: sınıf düzeyi *(A-dar)* mı, adlandırılmış *(A-tam)* mı? | **A-dar** | R-9 |
| 4 | 3B + mobilite: şimdi mi, gelecek çalışma mı? | **gelecek çalışma** | R-8 |
| 5 | `08` mühürlenmeden önce ölü üreticiler ne olacak? | iki sayı **yeniden ölçülsün** | R-16 |

⚖️ **Önerilerin hepsi aynı yöne bakıyor ve bu tesadüf değil:** kapsamı
korumak, ölçülmüş olanı sağlamlaştırmak ve **26 Eylül mührünü kurtarmak.**
🔴 Ama bu bir **tavsiyedir**, karar değil — ve karşı tercih de savunulabilir:
Boşluk B ve A-tam gerçek katkılardır, yalnızca **bu takvime sığmıyorlar.**
