# 09 — DEVİR TESLİM

> ## ⚫ EMEKLİ — yerini [`../DEVIR.md`](../DEVIR.md) aldı · 5 Eylül 2026
> Bu belge emekli `sim/` simülatörünün durumunu anlatır. Tarihsel kayıt
> olarak duruyor; **devralan ajan bunu değil `DEVIR.md`yi okur**.


> **Sıfır bağlamlı bir ajanın projeyi devralması içindir.**
> **Tarih: 1 Eylül 2026** · Teslim: **19 Aralık 2026** · Kalan: **109 gün**
>
> ⚠️ **Bu belge 1 Eylül 2026'da baştan yazıldı** *(K-081)*. Önceki sürümü
> *"Aile 3 ertelendi"*, *"ürün bir protokol değil"* ve *"Faz 0 kapandı"*
> diyordu — **üçü de artık yanlış**. Eski sürüm `v2/arsiv/` altında yok;
> içeriği `04`ün K-077…K-081 kayıtlarında yaşıyor.

---

# 1 · TEK CÜMLEYLE NEREDEYİZ

> Ölçüm aracı yazıldı ve altı bağımsız denetimden geçti; kapı **13/13**
> verdi. 🟢 **B0 koşuldu:** sekiz geçerlilik kaleminin **dördü kapandı**,
> biri denetlendi, üçü beyanlı/ölçütlü kaldı *(K-086)*.
> 🔴 **Kapı sonucu artık BAYAT** — `sim/` B0'da değişti *(bilerek: kapı
> `12` §2.3 gereği B0 **ve** B1'den sonra **tek kez** koşacak)*.
> Rakip protokoller *(AODV · OLSR · AOMDV)* **henüz yazılmadı**, özgün
> protokolün tasarımı **öğrenciden bekleniyor** *(hedef 10 Eylül)*.

---

# 2 · PROJE NEDİR — üç cümle

**Problem:** elektronik harp (RF karıştırma) altında çalışan taktik İHA
mesh ağlarında haberleşmenin ayakta kalması.

**Boşluk:** 2022–2026 literatüründe adlandırılmış FANET yönlendirme
protokolleri için **SJR'ye bağlı PDR/E2E bozunumu** ve **karıştırma
altında rota kurtarma gecikmesi** raporlayan birincil kaynak **yok**
*(20 dosyalık tarama ile doğrulandı)*.

**Özgünlük:** 🔴 **kurulan protokolün kendisinden gelir.** Standart
protokoller **kıyas tabanıdır**; ölçülen şey öğrencinin kendi tasarımının
onlara göre nasıl davrandığıdır.

---

# 3 · 🔒 DÖRT FAZ — ve FAZ ≠ AİLE

| Faz | Ne yapılır | Aile | Durum |
|---|---|---|---|
| **Faz 0** | Araç + doğrulama **+ 🆕 Kat 4 altyapısı** | — *(kapı)* | 🟡 **B0 bitti** · 🔴 **B1 + 3 kalem** |
| **Faz 1** | **AODV · OLSR · AOMDV** kurulur + gerçekçilik kanıtlanır | **Aile 1** | 🔒 başlamadı |
| **Faz 2** | **Özgün protokol** + karşılaştırma | **Aile 2** · **Aile 3** | 🔒 tasarım bekleniyor |
| **Faz 3** | Görselleştirme, rapor | — | — |

🔴 **"FAZ" bir iş aşamasıdır; "AİLE" bir Holm düzeltme birimidir.**
İkisi karıştırılırsa istatistik bozulur. `04`teki tarihi *"Aile 1/Aile 2"*
referansları **eski anlamıyla** okunmalıdır *(hipotez ailesi)*.

---

# 4 · 🟡 FAZ 0 — B0 KOŞULDU, KAPALI DEĞİL

**Kapı 13/13 geçti** *(27 Ağustos, 185,6 dk)* ve 🔴 **BAYAT** — `sim/` B0/B0.7/B0.8'de değişti *(`89587a19…` → `fc73905b…`)*. Bu **bilerek**: kapı `12` §2.3 gereği **B0 ve B1 birlikte bittikten sonra TEK KEZ** koşar. **B-129** —
`sim/` hash'i o günden beri birebir aynı:

```bash
PYTHONIOENCODING=utf-8 python -c "import sys;sys.path.insert(0,'.');import json;from sim.results import kaynak_hash;e=json.loads(open('ciktilar/sonuclar/deneme_araliklari.jsonl',encoding='utf-8').readline());print(e['kaynak_hash'], kaynak_hash(), e['kaynak_hash']==kaynak_hash())"
```
🔴 **Beklenen çıktı artık `False`** *(B-129)*: `89587a19… fc73905b… False`.
Bu komut kapının **bayat olup olmadığını** ölçer; bugün **bayattır** ve
bu bilinçlidir.

> ## 🟢 B0 KOŞULDU — 8 KALEM **3'E** İNDİ *(K-086)*
> Altı işin altısı da yapıldı; **dört yeni bulgu** çıktı
> *(F-5 · F-6 · F-7 · F-8)*.
>
> 🔴 **VE 7. BAĞIMSIZ DENETİM KOŞTU** *(2 Eylül · 23 bulgu · K-087)*:
> B0'ın **dört iddiası çürüdü**. Üçü **B0.7'de kapatıldı**, biri
> *(B-133, şema alanı)* **B1.5'e** taşındı, **19'u B2 öncesine**.
> Denetimin yargısı: *"ölçümleri sağlam, gerekçeleri değil."*

> ## 🟢 B0.9 KOŞULDU *(K-089, 3 Eylül)* — SEKİZİNCİ DENETİMİN 27 BULGUSU
>
> **26 bulgu** *(B-143 … B-168)* yargılandı: **26'sının 26'sı gerçek**,
> 22'si birebir yeniden üretildi. Denetçi **dört yerde yanıldı**.
> **+1 bulgu danışmandan** *(B-169: `08` md 25'in geri aldığı oran üç
> yerde güncelmiş gibi duruyordu — biri **üretim kodunda**)*.
>
> 🔒 **B1'in altı bloke edici kalemi kapandı.** En ağırı: üç üreticinin
> tek koruması `sim/` değişir değişmez **9 testinin 5'ini** atlıyordu ve
> **B1'in ilk işi `sim/`e Kat 4 eklemektir**. Ölçüldü ve düzeltildi:
> `9 → 4 passed, 5 skipped` idi, şimdi **18 passed, 0 skipped**;
> yakalama **8/8**, iki durumda da, eşleştirilmiş fark **0**.
>
> 🔴 **Kapı süresi bandı yeniden yazıldı: 165–330 → 194–435 dk** *(B-167,
> deponun **kendi** sabitleriyle)*.



| # | açık kalem | tür | durum |
|---|---|---|---|
| 1 | **D-13** — kapının Ç1 yolu sonuç satırı yazmıyor | sözleşme 5 | 🟢 **KAPANDI** — 2/2 · 20/20 satır, 3 mutasyon yakalandı |
| 2 | **B-57** — 27 karar kaydı ölçüm taşıyıp üreticisiz | sözleşme 6 | 🟡 **beyanlı kapalı** *(K-053)* |
| 3 | **Li seviye 4** — %10,2'lik açık açıklanamadı | doğrulama | 🟡 **beyanlı açık** · üretici onarıldı, 4 sayı birebir üretildi |
| 4 | **`06` koşul 1** — koşu uzunluğu bağımsızlığı | geçerlilik | 🟡 **ölçüt ilan edildi · kol başına ölçüldü** — **18 çiftin 3'ü** ayak 1'i geçmiyor *(B-147)*; ayak 2 eksik olduğu için hiçbir kol *"sağlandı"* sayılamaz |
| 5 | **`06` koşul 2** — gecikme metriği | geçerlilik | 🟢 **KAPANDI** — 🔴 reçete ölçümle **değişti** |
| 6 | **`06` koşul 3** — kontrol payı asimetrisi | geçerlilik | 🟢 **KAPANDI** — 30 tohumla yeniden ölçüldü |
| 7 | **A-14** — `karsilastirma.py` denetlenmedi | denetim | 🟢 **DENETLENDİ** — bulgu F-7 |
| 8 | **F-4** — `08`in iki üretici komutu çalışmıyor | kural 1 | 🟢 **KAPANDI** — ikisi de `dogrulama/` altında |

### 🔴 B0'ın en önemli sonucu — koşul 2'nin REÇETESİ yanlıştı

`06` §8.1 *"her gecikme cümlesi **p95 ile** yazılır"* diyordu. Ölçüldü
*(30 tohum, eşleştirilmiş, kesin işaret testi)*: **ham p95 bile anlamlı
değil** *(p = 0,58)*; **ortak alt kümede ortalama bile anlamlı**
*(+5,40 ms, p = 0,0003)* ve p95 **+28,15 ms** *(p = 0,0000)*.

⚖️ Sorun *"ortalama yerine p95"* değil, **karşılaştırılan KÜME**ydi —
ham ortalamanın **işareti yanlış**. Üçü de artık **kodda zorunlu**:
ortak alt küme · yüzdelikler · kesişim oranı.

📄 **Tam kanıt envanteri: `13-AILE0-KAPANIS-KANITI.md`** · karar: **K-086**

## 4.1 🔴 VE DOKUZUNCU KALEM — KAT 4 ALTYAPISI *(K-083)*

Sekiz kalem **geçerlilik** kalemidir. Dokuzuncusu bir **yetenek** boşluğu
ve daha büyük:

> **Üç rakip protokolün ÜÇÜ DE bugünkü arayüzle YAZILAMAZ.**

**Ölçüldü:** protokolün temas yüzeyi **tek çağrı** *(`self.protokol(gozlem)`)*
ve **iki kanca** *(`beacon_yuku` · `teshis`)*. `yayin_gonder` deponun
tamamında **tek yerden** çağrılıyor: periyodik beacon.

| eksik | kim ister |
|---|---|
| Talep üzerine **selleme** *(RREQ)* | AODV · AOMDV |
| **Unicast** kontrol paketi *(RREP)* | AODV · AOMDV |
| Olay-tetiklemeli yayın *(RERR)* | AODV · AOMDV |
| **İki farklı periyot** *(HELLO 2 s · TC 5 s)* | OLSR |
| **Protokol zamanlayıcısı** | üçü de |

🟢 **Riski düşüren üç ölçüm:** kontrol çerçeveleri **deftere girmiyor**
*(korunum güvende)* · `yuk_bayt` faturalama **zaten var** · `05` §A2
başlık okuma hakkını **zaten veriyor** → bu bir **uygulama boşluğu**,
sözleşme genişletmesi **değil**.

🔒 **Faz 1'e, kalan kalemler VE Kat 4 altyapısı bitmeden geçilmez.**
📄 İş blokları ve doğrulama ölçütleri: **`12-YOL-HARITASI.md` §2**

---

# 5 · 🔴 ÖNCE OKUNACAKLAR — sırayla

| # | belge | neden |
|---|---|---|
| 1 | `v2/03-YONTEM-KURALLARI.md` | ⭐⭐ **15 kural + hata sınıfları.** Her denetimin ölçütü. ⚠️ **Kural 4, 1 Eylül'de revize edildi** |
| 2 | `v2/01-PROBLEM-VE-AMAC.md` | Problem · özgünlük · **dört faz** · kısıtlar |
| 3 | `v2/06-ON-KAYIT.md` | ⭐ **Yeniden kuruldu.** Aileler · hipotezler · senaryolar · metrikler · 🔒 **26 Eylül'de mühürlenir** |
| 4 | `v2/13-AILE0-KAPANIS-KANITI.md` | Faz 0 neden kapalı değil — dört kanıt tablosu |
| 5 | `v2/08-AILE0-KAPSAM.md` | Aracın **NE YAPMADIĞI** — **37** maddelik sınır listesi *(2 Eylül: 33 → 37, yedinci denetim)* |
| 6 | `v2/10-LITERATUR-KOD-KARSILASTIRMA.md` | Literatür ↔ kod, 68 yargı satırı + 7 bulgu |
| 7 | `v2/11` · `v2/12` | Refactoring kalemleri · yol haritası |
| 8 | `v2/05` · `v2/07` | Gözlem penceresi *(kilitli)* · simülatör arayüzü |
| 9 | `v2/04-NEDEN-BOYLE.md` | Karar kaydı — en az **K-076 … K-083** |

---

# 6 · 🔴 ÇALIŞMA ORTAMI — ilk komuttan önce oku

### 6.1 Windows + Türkçe/emoji → `PYTHONIOENCODING`

Depodaki araçların hepsi Türkçe ve emoji basıyor; Windows konsolu varsayılan
`cp1254` kullanır ve **`UnicodeEncodeError`** verir.

🔒 **Her Python çağrısında `PYTHONIOENCODING=utf-8` verilir.** Unutulursa
hata **aracın değil terminalin** hatasıdır — koda dokunma.

### 6.2 Windows `spawn` → `if __name__ == "__main__":` ZORUNLU

`multiprocessing` Windows'ta **fork değil spawn** kullanır; koruma bloğu
olmayan bir betik kendini sonsuz çoğaltır.

🔴 **Ve `Pool` kullanan bir ölçüm betiğinde YAZICI EBEVEYNDE KALIR:**
işçiler `olc()` sonucunu **döndürür**, ebeveyn `SonucYazici` ile **yazar**.
Yazıcı dosya tanıtıcısı taşıdığı için alt sürece geçirilemez — **D-13'ün
sebebi tam olarak budur.** Çalışan örnek:
`dogrulama/literatur_eksenleri.py`.

### 6.3 Makine — 10 çekirdek, **2,10× oynuyor**

🔴 **İki sonucu var:**
1. **Uzun koşudan ÖNCE süre tahmini yazdır; 30 dk'yı aşıyorsa SOR**
   *(kural 7)*. Tahmin **tek sayı değil, BANT**.
2. 🔴 **İki durum ancak İÇ İÇE koşturularak karşılaştırılabilir.** Ardışık
   ölçüm bu depoda *"+819 sn"* dedi; iç içe ölçümde gerçek fark **+45 sn**
   çıktı.

**Ölçülmüş taban:** 300 tam koşu, `Pool(10)`, **4,3 dk** *(tek koşu 9,1 sn)*.

---

# 7 · KOMUTLAR

Ucuz ön kontrol *(~20 sn)*:
```bash
PYTHONIOENCODING=utf-8 python -m pytest tests/test_kapi_secimleri.py -q
```

Tam test paketi *(14–30 dk)*:
```bash
PYTHONIOENCODING=utf-8 python -m pytest tests -q
```

Karar kaydı denetimi *(~2 sn)*:
```bash
PYTHONIOENCODING=utf-8 python dogrulama/karar_kaydi_denetimi.py
```

SJR/JSR dönüşüm tablosu *(~1 dk)*:
```bash
PYTHONIOENCODING=utf-8 python dogrulama/sjr_donusumu.py
```

🔴 **Kapı — ~194–435 dk** *(B-167: ilan edilen 165–330 üst uçta tutmuyordu; deponun kendi sabitleriyle yeniden hesaplandı)*. **Kural 7 gereği ÖNCE SOR:**
```bash
PYTHONIOENCODING=utf-8 python dogrulama/aile0_kapi_raporu.py
```

⚠️ **ÖN KONTROLÜN GEÇMESİ KAPININ GEÇTİĞİ ANLAMINA GELMEZ** — bu depoda
*"ön kontrol geçti, kapı düştü"* **dört kez** yaşandı.

---

# 8 · 🔒 DEĞİŞMEYEN KURALLAR

| kural | not |
|---|---|
| `03`ün 15 kuralı ve **Y1–Y14** | Bu depo onları **yaşayarak** öğrendi |
| 🔴 **Ölçmeden iddia etme** | Literatürden gelen bir sayı da **bu araçta ölçülmeden** projeye giremez |
| 🔴 **Kâhin yasağı** *(kural 5)* | Simülatörde olup gerçek telsizin ölçemeyeceği hiçbir şey karara giremez |
| 🔄 **Sadakat, ayarlama değil** *(kural 4, revize)* | Rakip RFC'ye sadık kurulur; **hiçbir kol — bizimki dâhil — senaryo başına ayarlanmaz** |
| 🔴 **Derin öğrenme yok** *(kural 9)* | SWaP kısıtı gerçek |
| 🔴 **Ana deney tohumları 2000–2029** | Mühürden önce **hiçbir amaçla** koşulmaz |
| 🔴 **Hiçbir git komutu yok** — `status` dahil | Depo öğrencinin |
| 🔴 **Kod yazmadan önce yapıyı anlat, onay al** | kural 8 |
| 🔴 **Bir bulguyu *"düşük öncelik"* deyip bırakma** | kural 10 |
| 🔒 **Faz 1 öğrenci onayı olmadan başlamaz** | — |

---

# 9 · TAKVİM

| tarih | ne |
|---|---|
| **1 Eylül 2026** | 🔴 **BUGÜN** — çerçeve netleşti *(K-081)*, `06` yeniden kuruldu |
| *sırada* | 🟢 **B0 bitti** → **B1 · Kat 4 altyapısı** *(tasarım taslağını bekliyor)* → kapı 7. koşu |
| ~~26 Eylül 2026~~ | 🔴 **MÜHÜR TUTMUYOR** — ölçüldü: mühre kadar **22–33,5 efektif gün** gerekiyor, **25 takvim günü** var |
| **~20 Ekim 2026** | 🔒 **ÖNERİLEN MÜHÜR** *(K-083 · öğrenci onayı bekliyor)* — eşikler · güç analizi · Aile 2/3 hipotezleri · karıştırıcı konumu |
| **13 Ekim 2026** | TÜBİTAK başvurusu açılır |
| **31 Ekim 2026** | 🔒 **Yazım kilidi** — yeni deney yok |
| **19 Aralık 2026** | Teslim |

**Tohum kümeleri:** kurulum/doğrulama **1–30** · ana deney **2000–2029**

---

# 10 · ÖĞRENCİ HAKKINDA

- TÜBİTAK 2204-A'ya hazırlanan bir **lise öğrencisi**; tam zamanlı çalışıyor,
  acele yok ama **takvim disiplini var**
- 🔴 **Doğrulama konusunda ısrarcı ve bu ısrar SEKİZ kez haklı çıktı.**
  Sonuncusu: *"araştırmaların hepsini okuduğuna emin misin?"* — %62 çıktı
  ve beş bulgu o eksikte saklıydı *(K-080)*
- **Savunamadığı hiçbir şeyi projede tutmaz**
- **Kararlar onundur.** Danışman **seçenekleri ve ölçüm yöntemini** sunar
- **Kısa, anlaşılır özet ister** — kod referansı değil, **ne olduğu ve neden**

---

# 11 · BU PROJENİN KÜLTÜRÜ

> Bir hipotezi **deney öncesi ilan edilmiş** bir yanlışlanma koşuluyla test
> etmek ve koşul tetiklendiğinde onu dürüstçe raporlamak, jüri karşısında
> çalışan bir çözümden **daha zor taklit edilen** bir şeydir.

Bu proje şunları yaptı ve **hepsi kayıtta**: bir bandı koşmadan önce ilan
etti ve **tutmadı** · kendi hata iddiasını ölçüp **çürüttü** · kendi kuralını
ihlal edip **yakaladı ve tohumları yaktı** · kapanmış bir kapıyı bağımsız
denetimle **beş kez yeniden açtı** · bir denetçinin altı iddiasını **ölçümle
çürüttü** · ve **kendi ajanlarının hatalarını kayda geçirdi.**

🔴 En önemli iki cümle:

> **"492 test geçiyor" ile "Faz 0 kapalı" AYNI ŞEY DEĞİLDİR.**
>
> **Bir şeyi büyütmek istiyorsan önce ölç.**
