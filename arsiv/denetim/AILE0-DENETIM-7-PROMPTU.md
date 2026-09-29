# AİLE 0 · YEDİNCİ VE NİHAİ BAĞIMSIZ DENETİM — sıfır bağlamlı ajana yapıştırılacak metin

> Aşağıdaki `---` çizgisinden sonraki metnin **tamamını**, sıfır bağlamlı
> yeni bir ajan oturumuna **ilk mesaj** olarak yapıştır.
>
> *Yazıldığı tarih: 27 Ağustos 2026. Taşıdığı her sayı o gün koşturularak
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

# 🔴🔴 BU DENETİM SONUNCUSUDUR VE SORUSU TEKTİR

Önceki altı denetimin soruları şunlardı:

| # | Soru |
|---|---|
| 1–5 | *"Bu kodda ne bozuk?"* |
| 6 | *"Aile 0 OLMASI GEREKEN şey oldu mu?"* — `03`ün altı sözleşmesi + dört seviyesi |

**Yedincinin sorusu bunlardan başka ve daha basit:**

> ## 🔴 BU SİMÜLATÖR **SESSİZCE YANLIŞ SONUÇ VEREBİLİR Mİ?**

**Neden bu soru:** Aile 0 bugün kapandı *(kapı 13/13)*. Bundan sonraki her
adımda — Aile 1, 2, 3 — bu aracın ürettiği her sayı bir **araştırma
iddiasına** dönüşecek ve jüriye sunulacak. Araç gürültülü olabilir, eksik
olabilir, yavaş olabilir; bunların hepsi yönetilebilir.

🔴 **Yönetilemeyen tek şey, aracın YANLIŞ bir sayıyı DOĞRU gibi
üretmesidir** — çünkü o sayı, onu üreten kusurla birlikte rapora girer.

**Senden istenen: bu aracın sessizce yanlış cevap verebileceği bir yol
bulmak.** Bulamazsan, aradığın yerlerin listesiyle birlikte bunu yaz.

---

# ENVANTER — 27 Ağustos 2026, koşturularak ölçüldü

| Büyüklük | Değer |
|---|---|
| Test | **429** *(hepsi geçiyor)* |
| 🔴 Paket süresi | **892,66 – 1 850,63 sn** — **2,10 KAT**, aynı kod |
| Kapı | 🟢 **13/13 · 185,6 dk** *(27 Ağu, K-076)* |
| `sonuc()` şeması | **79 alan** *(bu oturumda 47'den çıktı)* |
| Hedefli mutasyon | **35** · kör havuz **253** |
| Karar kaydı | **76** *(K-001…K-076)* · üreticisiz **27** |
| Kapsam maddesi | **32** |
| Kalıcı kural | **Y1–Y14** *(+ Y15 adayı)* |
| Satır | `sim` **4 401** · `tests` **9 341** · `dogrulama` **5 466** |
| `aile0_audit.md` | **8 602 satır**, ALTI denetim |
| `v2/04-NEDEN-BOYLE.md` | **7 134 satır**, 76 karar kaydı |

```
README.md          harita — BURADAN BAŞLA
aile0_audit.md     ALTI denetim raporu — DEĞİŞTİRİLMEZ
v2/                belgeler 00–09
denetim/           bu prompt ve önceki altısı
ciktilar/          araç çıktıları + politika · sonuclar/ (JSONL)
sim/ tests/ dogrulama/
```

**Kat 4 (yönlendirme) YOKTUR** — Aile 1'in işi.
Protokol arayüzü: `protokol_fabrikasi(kon) → protokol(gozlem) → int | None`
*(fabrika **düğüm başına** çağrılır)* · iki isteğe bağlı kanca:
`beacon_yuku(dugum)` · `teshis(dugum)`

---

# 🔴🔴 EN ÖNEMLİ TEK OLGU: **BU İŞİ HİÇ KİMSE DENETLEMEDİ**

27 Ağustos oturumu şunları yaptı:

| ne | miktar |
|---|---|
| Altıncı denetimin bulgusu kapatıldı | **18/18** *(B-100 … B-117)* |
| Kendi bulduğu yeni bulgu | **8** *(D-6 … D-13)* |
| Yazılan mutasyon | **47** *(47'si de yakalandı)* |
| Yeni `dogrulama/` aracı | **4** |
| Sonuç şemasına eklenen alan | **32** |
| Yeniden yazılan belge | **2** *(`README` · `09`)* |
| Karar kaydı | **6** *(K-071 … K-076)* |

🔴 **VE HEPSİNİ AYNI AJAN DOĞRULADI.** Bağımsız hiçbir göz bu işin **hiçbir
parçasına** bakmadı. Önceki altı denetimin her biri tam olarak bu durumda
bulgu çıkardı — ve **beş kez** kapanmış sayılan bir kapıyı yeniden açtı.

## O oturum kendi işinde **on iki** hata buldu — sen on üçüncüyü ara

| # | Hata | Sınıf |
|---|---|---|
| 1 | `c63`ün `==` reddi **hiçbir testçe tetiklenmiyordu** | tetiklenemeyen kontrol |
| 2 | `kontrol_payi.olc` kanonik `olc`u **gölgeledi** | ikinci doğru kaynağı |
| 3 | D-11'in koruması `ast.unparse` **metninde** kelime arıyordu | metin ≠ davranış |
| 4 | Envantere **ölçmeden** sayı yazdı *("411" · gerçek 416)* | `03` kural 1 |
| 5 | `test_b52_*` bir **grep**'ti | beyan ≠ etki |
| 6 | B-101 testinin ölçütü yanlıştı *("ulaşılabilir" ≠ "paylaşılıyor")* | Y5 |
| 7 | Test `derinlik=None`ı **açıkça** geçiriyordu — üretimin varsayılanını sınamıyordu | Y11 |
| 8 | 🔴 **İki yanlış teşhis** *("tarama yavaşlattı" · "assert'ler yavaşlattı")* | `03` B4 |
| 9 | 🔴 **Yöntem:** iki kod durumunu **40 dk arayla** ölçüp karşılaştırdı | `03` B2 |
| 10 | Windows `spawn` uyarısını **okudu, uygulamadı** | — |
| 11 | 🔴 **Kanonik `olc`u YİNE gölgeledi** — kuralı yazdıktan **sonra** | 2'nin tekrarı |
| 12 | 🔴 **D-13:** yazıcı `Pool`'un ötesine geçmiyor; koruması `kayit()`ın **kurulduğunu** doğruluyor, satır **yazıldığını** değil | 5'in tekrarı |

⚖️ **ÖRÜNTÜ AÇIK VE SENİN EN İYİ AV HARİTAN BUDUR:**

> 🔴 **Bu oturumun yazdığı korumaların en sık hatası, BEYANI doğrulayıp
> ETKİYİ doğrulamamaktır.** 1, 3, 5, 7 ve 12 numaralı hatalar aynı sınıftır
> ve **üç kez tekrarlanmıştır.**

**Yani sorman gereken soru şudur: bu oturumun yazdığı ~50 korumadan kaçı,
korumak iddia ettiği şeyi FİİLEN ölçüyor?**

---

# 🔴 BÖLÜM A — EN YÜKSEK DEĞERLİ HEDEF: **PENCERE İKİZLERİ**

Bu oturum `sonuc()` şemasına **32 alan** ekledi. Bunların **25'i** kümülatif
sayaçların *"ölçüm penceresi"* ikizidir *(`kontrol_bayt_pencere`,
`mac_deneme_pencere`, …)* artı bir maksimum ve iki türev ortalama.

🔴 **BUNLAR NEDEN EN TEHLİKELİ YERDİR:**

1. **Aile 1'in HER karşılaştırması bunları kullanacak.** `08` madde 31:
   *"Aile 1'in her karşılaştırması `*_pencere` alanlarını kullanmak
   zorundadır."*
2. 🔴 **KAPININ HİÇBİR KRİTERİ ONLARI OKUMUYOR.** Ç1–Ç6'nın tamamı tüm koşu
   alanlarını ya da pytest seçimlerini ölçüyor. Yani bu 32 alan **kapı
   13/13 verdiği hâlde tamamen yanlış olabilir** ve kapı susardı.
3. Mekanizması ince: `Olaylar.kostur()` **üç kez** artan sınırla çağrılıyor
   ve sayaçlar iki uçta fotoğraflanıyor.

**Senden istenen:**

* `sim/kosucu.py::kostur()` ve `_sayac_anlik()` / `_pencere_alanlari()`
  yollarını **oku ve kır.** Üç fazlı koşu, tek fazlıyla **birebir** aynı mı?
  *(Oturum bunu 3 kol × 3 yapılandırmada ölçtü ve 0/9 fark buldu —
  **doğrula, ve daha geniş bir örneklemde**.)*
* 🔴 `_sayac_anlik()` **`sonuc()`in ifadelerini elle yansıtan bir İKİNCİ
  KAYNAKTIR.** Bir alan birinde değişip diğerinde değişmezse ikiz **yanlış
  alandan** hesaplanır. Bunu bağlayan test var mı, **kırılabilir mi**?
* `en_yuksek_doluluk_pencere` bir **maksimumdur** ve farkla türetilemez.
  `Kuyruk.pencere_baslat()` doğru anda mı çağrılıyor? Pencere başındaki
  doluluk doğru mu devralınıyor?
* 🔴 **İki türev ortalama** — `secim_avantaji_ortalama_pencere` ve
  `karar_bag_per_ortalama_pencere` — pay ve paydası ayrı ayrı
  fotoğraflanıyor. **Bölme doğru çiftten mi yapılıyor?**

⚠️ **VE BU EKSENDE BİR AÇIK KARAR VAR:** ön-kayıtlı H1.1 kapısı
*(`dogrulama/mekanizma_kapisi.py`)* hâlâ `secim_avantaji_ortalama`nın
**TÜM KOŞU** hâlini okuyor; ölçüldü ki kararlarının **%15,3–16,8'i pencere
dışında.** Hangisinin okunacağı `06` mühründen *(26 Eylül)* önce
kararlaştırılacak. **Sen hangisinin doğru olduğunu ÖLÇ.**

---

# 🔴 BÖLÜM B — KAPININ KENDİ KÖR NOKTASI

Kapı 13/13 verdi. **Kapının GÖREMEDİĞİ ne var?**

| ne | kapı görür mü |
|---|---|
| 25 pencere ikizi | 🔴 **HAYIR** |
| `konfig` · `korunum` · `olcum_penceresi_s` alanlarının **içeriği** | 🔴 kısmen *(Ç1 korunumu ayrı yoldan ölçüyor)* |
| Sonuç satırlarının yazılması | 🔴 **HAYIR** — D-13 tam bu yüzden kaçtı |
| `sim/karsilastirma.py`nin 322 satırı | 🔴 **HAYIR** *(A-14 — altı denetimde HİÇ açılmadı)* |
| `dogrulama/` altındaki 23 aracın çoğu | 🔴 kısmen |

🔴 **A-14 SENİN İÇİN AYRI BİR MADDEDİR.** `sim/karsilastirma.py` Aile 1'in
**her gecikme karşılaştırmasının** geçeceği dosyadır — ortak alt küme,
kesişim oranı, NaN reddi, iki parmak izi kontrolü. **Altı bağımsız denetimin
hiçbiri onu açmadı.** Beşinci ve altıncı denetim bunu **açıkça beyan etti**
ve yine açmadı.

---

# 🔴 BÖLÜM C — BU OTURUMUN DÖRT YENİ ARACI

Hiçbiri bağımsız bir gözle görülmedi:

| araç | ne yapıyor | neden şüpheli |
|---|---|---|
| `dogrulama/kopya.py` | depo kopyalama — **tek kaynak** | B-100'ün ilacı. Altı `copytree` buraya indi; **bir yer atlanmış olabilir mi**? |
| `dogrulama/olcum.py` | kanonik `olc(...)` + `kayit(...)` bağlamı | 🔴 **D-13 buradan çıktı.** `_AKTIF[0]` global bir listedir; **iç içe kullanım · thread · Pool** — başka hangi yolda sessizce boşalır? |
| `dogrulama/gozlem_tuketim.py` | `__getattribute__` sarmalayıp **okunan alanı** ölçer | Sarmalama `try/finally` ile geri alınıyor — **her yolda mı?** Ölçüm **yalnızca koşulan yolları** görür; beyan bunu söylüyor mu? |
| `dogrulama/deneme_araliklari.py` | ardışık iletim aralıkları | `_iletim_basla` sarmalanıyor. **Sarmalama ölçtüğü şeyi değiştiriyor mu?** |

🔴 **ORTAK ŞÜPHE:** dördü de **çalışan koda sarmalayıcı takıyor.** `03` B6:
*"sahte host / mock'un ölçüleni yutması — bir test ikizi, tam da ölçmek
istediğin şeyi devre dışı bırakabilir."*

---

# 🔴 BÖLÜM D — ÖLÇÜM ORTAMININ KENDİSİ

Bu oturum şunu ölçtü ve **kayda geçirdi**:

> **Aynı 429 testlik paket, aynı kodla, aynı gün: 892,66 · 1 832,95 ·
> 1 850,63 · 973,96 sn — 2,10 KAT salınım.**
> `test_gozlem.py` tek başına: **163,5 → 305 → 165,3 sn.**

Sonuçları:

1. `TEST_BASINA_EN_KOTU_S` **2,5694 → 4,3854** yapıldı *(en kötü okuma)*
2. `TABAN_ZAMAN_ASIMI_S` 1 800 → **4 200** · `MUTANT_ZAMAN_ASIMI_S`
   3 600 → **7 200**
3. 🔴 **Y12'nin duyarlılığı yarıya indi:** koruma artık gerçek bir iki
   katına çıkmayı **göremez**
4. **Y15 adayı:** *"İki kod durumu ancak İÇ İÇE koşturularak
   karşılaştırılabilir"*

**Senden istenen:**
* Salınımı **kendin ölç.** 2,10 kat doğru mu, yoksa o günkü makineye mi ait?
* 🔴 **Bu salınım BELİRLENİMCİLİĞİ etkiliyor mu?** Ç2 *"aynı tohum → bit
  birebir aynı sonuç"* diyor. Yavaş bir dönemde koşan bir ölçüm, hızlı
  dönemdekiyle **aynı sayıyı** veriyor mu? *(Vermeli — ama ölç.)*
* Zaman aşımı sabitleri **yavaş dönemden** mühürlendi. Bu, gereken zaman
  aşımını **abartıyor** — güvenli yön. Ama `_gereken_zaman_asimi_s`
  hesabının **kendisi** doğru mu?

---

# 🔴 BÖLÜM E — SENDEN İSTENEN KRİTİK ÖLÇÜM

**Tek örneklem binom · tek yönlü · α = 0,05 · TAM binom · H0: p = 0,70**

| n | red bölgesi | güç *(p₁=0,40)* | güç *(p₁=0,50)* |
|---|---|---|---|
| 15 | X ≤ 6 | 0,610 | 0,304 |
| **19** | X ≤ 9 | **0,814** | 0,500 |
| 24 | X ≤ 12 | 0,886 | 0,581 |
| 30 | X ≤ 16 | 0,952 | 0,708 |

**Altıncı denetimin katman tablosu** *(bağımsız olarak `scipy` ile yeniden
üretildi — dördü de birebir tuttu)*:

| katman | sağ kalan | oran | %95 GA | ulaşılan güç |
|---|---|---|---|---|
| 🔴 **mekanizma** | **7/22** | %31,8 | **[0,139 · 0,549]** | 0,879 |
| sayaç / raporlama | 3/20 | %15,0 | [0,032 · 0,379] | 0,872 |
| GENEL | 10/42 | %23,8 | [0,121 · 0,395] | 0,982 |

🔴 **Mekanizma katmanı ilk kez yeterli güçle ölçüldü ve H0 reddedildi — ama
GA [0,139 · 0,549] olduğu için *"kapandı"* YAZILAMADI.** Gerçek oran %55'e
kadar olabilir.

## 🔴 ŞARTLARIN

| # | Şart |
|---|---|
| 1 | 🔴 **BU OTURUMUN YAZDIĞI KODA en az 20 mutasyon.** 47 mutasyon yazıldı, 47'si yakalandı — **hepsi kendi yazarı tarafından**. Bağımsız bir örneklem şart |
| 2 | 🔴 **PENCERE İKİZLERİNE en az 8 mutasyon** *(Bölüm A)*. Kapının göremediği en büyük yüzey burası |
| 3 | **Mekanizma katmanında en az 19** — GA'yı daraltmak için; altıncı denetim 22 ile [0,139 · 0,549] aldı |
| 4 | Her katmanın **oranını, %95 GA'sını ve ULAŞILAN GÜCÜNÜ** ayrı raporla; katmanların **ayrık** olduğunu rakamla göster |
| 5 | 🔴 n < 19 olan katman için *"kapandı"* **YAZILAMAZ** |
| 6 | 🔴 *"Eşdeğer"* / *"tetiklenmiyor"* diyeceğin her iddia: **≥4 kol × ≥8 yapılandırma** |
| 7 | 🔴 **İki durumu karşılaştıracaksan İÇ İÇE koştur** — bu makine **2,10 kat** oynuyor ve ardışık ölçüm onu koda atfeder *(bu oturumun 9 numaralı hatası)* |

⏱️ **Bütçe:** ~50 mutasyon × tam paket. Paket **892–1 851 sn**;
`Pool(6)` ile **~2,5–5 saat**. 🔴 **30 dakikayı aşacak her koşudan önce SOR.**

---

# 🔴 BÖLÜM F — AÇIK BEYAN EDİLMİŞ ZAYIFLIKLAR

Bunlar **gizlenmiyor**; senden istenen, **yeterince açık beyan edilip
edilmediklerini** ve **başka bir şeyi gizleyip gizlemediklerini** ölçmen.

| # | Zayıflık | Nerede yazılı |
|---|---|---|
| 1 | 🔴 **D-13** — kapının Ç1 yolu *(540 koşu)* sonuç satırı **yazmıyor**; `Pool` alt süreçlerine yazıcı ulaşmıyor | K-076 · `09` |
| 2 | 🔴 **Li replikasyonundaki %10'luk fark AÇIKLANAMADI** — üç adayın üst sınırları toplamı **≤%9,1**, gereken **%10,2** | `08` Ç4 |
| 3 | 🔴 **Mekanizma katmanı *"kapandı"* değil** — GA [0,139 · 0,549] | `README` · `04` |
| 4 | **D-12** — `PaketGorunumu`nun 4 alanı taşınıyor, **hiç okunmuyor** | `08` madde 22 |
| 5 | **A-14** — `karsilastirma.py` hiç denetlenmedi | `09` §5 |
| 6 | **İstatistik katmanı YOK** — Wilcoxon · Holm · güç · NaN koruması | `08` madde 21 |
| 7 | **Y12'nin duyarlılık kaybı** | K-073 |
| 8 | Gözlem penceresinin **14 alanının** tüketicisi yok | `08` madde 22 |

🔴 **Her biri için tek soru:** *beyan, kusurun GERÇEK büyüklüğünü söylüyor
mu, yoksa küçültüyor mu?*

---

# 🔍 ŞÜPHE LİSTESİ — bu denetime özel

> Önceki altı listeyi de uygula *(`denetim/` altında)*.

**1 · 🔴 PENCERE İKİZLERİ.** Bölüm A. **En yüksek değerli hedef.**

**2 · 🔴 `sim/karsilastirma.py`.** 322 satır, **altı denetimde hiç
açılmadı**, Aile 1'in her gecikme karşılaştırması oradan geçecek.

**3 · 🔴 `dogrulama/olcum.py::_AKTIF`.** Global bir liste. D-13 `Pool`
yüzünden çıktı — **başka hangi yolda sessizce boşalır?** İç içe `kayit`
reddediliyor; ya istisna atılırsa? Ya `main()` erken dönerse?

**4 · KANONİK YOLUN KAPSAMI.** `dogrulama/` altında çıplak `Kosu(` yok —
**ama `tests/` altında 102 tane var** ve bu **bilerek** *(birim testler tek
koşuyu izole ölçer)*. Bu muafiyet gerçekten güvenli mi?

**5 · AST YÜKLEMLERİ.** Ç6.1/Ç6.3 dizgi aramasından AST'ye taşındı. Dört
kandırma denemesi kapatıldı. 🔴 **Beşincisini bul.**

**6 · SINIRSIZ TARAMA.** `_TARAMA_DERINLIGI` kaldırıldı, yerine **maliyet
tavanı** kondu *(`_TARAMA_TAVANI = 200 000`, aşılırsa PATLAR)*. Tavan
ölçümden türetilmiş mi? Aile 1'in bir protokolü onu aşar mı?

**7 · ZAMAN AŞIMI SABİTLERİ.** Yavaş dönemden mühürlendi. `test_b78_*` ve
`test_b90_*` onları bağlıyor — **kırılabilir mi**?

**8 · `06` 26 EYLÜL'DE DONUYOR.** Bugün mühürlenmeye hazır mı? İstatistik
katmanı yok, mekanizma kapısının penceresi kararsız, m=5 mührü sağlam mı?

**9 · 27 ÜRETİCİSİZ KARAR KAYDI.** K-024 bu oturumda üreticisine kavuştu
*(28 → 27)*. Kalan 27'nin kaçının sayısı bugün **yeniden üretilebilir**?
Üretilemeyen bir sayı `04`te olgu gibi duruyorsa, bu bir bulgudur.

**10 · KAPANIŞLAR BİRBİRİNİ BOZDU MU?** Bu depoda **dört kez** oldu
*(B-57+B-93 → B-100 · B-83 → B-112 · B-46 → B-113 · B-106 → D-13)*.
**Bu oturumun 26 kapanışından hangisi bir sonrakini doğuruyor?**

**11 · BU PROMPTUN KENDİSİ.** Bu metni **proje yazdı**, denetçi değil.
🔴 Neye bakmanı istemiyor olabilir? Listede **olmayan** bir yere bak.
*(Altıncı denetimin en pahalı üç bulgusu promptun listesinde YOKTU.)*

---

# ÇALIŞMA BİÇİMİN

1. **Önce oku, sonra koştur, en son yorumla.** İlk: kök `README.md` →
   `v2/03-YONTEM-KURALLARI.md` *(15 kural — **denetimin ölçütü budur**)* →
   `v2/04-NEDEN-BOYLE.md`nin sonundaki **Y1–Y14** → **K-071…K-076**.
2. Her bulgunun yanında **üretici komut** *(depo kökünden koşabilir)* ve
   **kaynak dosya:satır**.
3. Bir iddiayı doğrularken **iddianın kendi ölçütünü kullanma.**
4. ⭐ **Y6 — beklenenden iyi çıkan sonuç, kötü çıkan kadar şüphelidir.**
   Kendi lehine çıkan sonuca da uygula.
5. ⭐ **Y8** *(bozulan yolun tetiklendiğini ÖNCE göster)* · ⭐ **Y10** ·
   ⭐ **Y11** *(korumayı kapsamı DIŞINDAKİ vakayla sına)* · ⭐ **Y14**.
6. 🔴 **Şüphelendiğin satırı `read_bytes()` ile oku** — B-58 bunun
   yapılmamasından doğdu ve **iki bağımsız göz birden** yanıldı.
7. 🔴 **Yayımladığın her üretici komutu, yayımlamadan önce OLDUĞU GİBİ
   koştur** — ve **hangi dizinde, hangi durumda** koştuğunu da yaz.
8. 🔴 **İki durumu karşılaştıracaksan İÇ İÇE koştur** *(Bölüm D)*.
9. 🔴 **Bir korumanın BEYANINI değil ETKİSİNİ ölç.** Bu oturumun en sık
   hatası buydu ve **üç kez** tekrarlandı.
10. Deneme için depoyu geçici bir dizine kopyala; **aslını değiştirme.**

---

# ORTAM VE KISITLAR

| | |
|---|---|
| Platform | Windows 11 · Python 3.11 · numpy, scipy, pytest kurulu |
| Dil | Kod ve belgeler **Türkçe**. Raporunu da Türkçe yaz |
| ⚠️ Konsol | `PYTHONIOENCODING=utf-8` — varsayılan cp1254 Türkçe karakterde çöküyor |
| 🔴 Paralellik | Windows'ta `spawn`: `Pool` açan her betikte `if __name__ == "__main__":` **ZORUNLU** *(bu oturum bunu unuttu ve çöktü)* |
| 🔴 Git | **Hiçbir git komutu çalıştırma — `status` dâhil** |
| 🔴 Kod | **Depodaki hiçbir dosyayı DEĞİŞTİRME.** Deneme için `tempfile.mkdtemp` kopyası |
| 🔴 Tohum | **2000–2029 HİÇBİR AMAÇLA koşulmaz.** Ayarlama/kapı: **1–30** |
| İşlemci | En fazla **10 çekirdek.** 30 dk'yı aşacak koşudan **önce** süre tahminini yazdır ve **SOR** |
| Yazacağın tek dosya | `aile0_audit.md` |

### ⏱️ Ölçülmüş süreler — 27 Ağustos, 10 çekirdek

| Komut | Süre |
|---|---|
| `python -m pytest tests -q` | **892,66 – 1 850,63 sn** 🔴 *(2,10 kat)* |
| `python -m pytest tests/test_kapi_secimleri.py -q` | **17,3 sn** ⭐ *(63 test)* |
| `python dogrulama/mutasyon_on_kontrol.py` | **0,4 dk** ⭐ |
| `python dogrulama/gozlem_tuketim.py` | ~3 dk |
| `python dogrulama/deneme_araliklari.py` | ~2 dk |
| `python dogrulama/kontrol_payi.py` | ~3 dk |
| `python dogrulama/mekanizma_kapisi.py <kol>` | ~7 dk |
| `python dogrulama/aile0_kapi_raporu.py` | 🔴 **185,6 dk · izin gerekir** |

⚠️ Süre tahmini bu depoda **beş kez** tutmadı. Kendi tahminini **ölçtüğün en
büyük** süreden kur.

---

# ÇIKTI: `aile0_audit.md`

Dosya **altı denetimin raporunu** taşıyor. 🔴 **İçeriğini SİLME, DEĞİŞTİRME.**

1. Baştaki durum bloğunu yedinci denetimi de içerecek şekilde genişlet.
2. Sonuna `# YEDİNCİ DENETİM — <tarih>` bölümü ekle.
3. 🔴 Bulgu numaraları **B-120**'den devam eder. *(B-118/B-119 kasten boş —
   bu oturumun D-serisi bulguları `04`te.)*

```
## 0. YÖNETİCİ ÖZETİ
    🔴 BU SİMÜLATÖR SESSİZCE YANLIŞ SONUÇ VEREBİLİR Mİ: EVET / HAYIR / KOŞULLU
    🔴 Bulduğun EN CİDDİ tek yol — ilk paragrafta
    🔴 KATMAN BAZINDA sağ kalan oranı + ULAŞILAN GÜÇ

## 1. 🔴 PENCERE İKİZLERİ — kapının göremediği 32 alan
## 2. 🔴 `sim/karsilastirma.py` — altı denetimde hiç açılmadı
## 3. BU OTURUMUN DÖRT YENİ ARACI
## 4. KAPININ KÖR NOKTALARI
## 5. YENİ BULGULAR (B-120'den)
## 6. 27 AĞUSTOS OTURUMUNUN 26 KAPANIŞI — doğrulama (≥10)
## 7. DOĞRULANAN İDDİALAR   ## 8. ÜRETİLEMEYEN İDDİALAR

## 9. 🔴 KENDİ MUTASYONLARIN — KATMANLI
    ≥20 "27 Ağustos kodu" · ≥8 PENCERE İKİZİ · ≥19 mekanizma
    Her biri: Y8 tetiklenme (ÖNCE) · 429 testten sağ çıktı mı ·
    sağ kaldıysa davranış değişiyor mu (≥4 kol × ≥8 yapılandırma)
    🔴 HER KATMAN: oran · %95 GA · ULAŞILAN GÜÇ · katmanlar AYRIK mı

## 10. AÇIK BEYAN EDİLMİŞ ZAYIFLIKLAR — beyan yeterli mi
## 11. KAPSAM BEYANINA EKLENECEKLER

## 12. 🔴 ANLAŞILMAYANLAR
    🔴 BOŞ BIRAKILAMAZ. Altı denetimde de buradan GERÇEK KUSUR çıktı —
    A-4 bir kâhin kanalıydı; A-5 ön-kayıtlı kapının varyansını değiştirdi.
    Numaralar A-17'den devam eder.

## 13. 🔴 AİLE 1'E GEÇİLEBİLİR Mİ — senin yargın
    Bu bölüm ZORUNLUDUR ve tek cümleyle başlar:
    "Bu araçla üretilecek bir Aile 1 sonucuna GÜVENİLİR / GÜVENİLMEZ, çünkü…"

## 14. KOŞTURDUĞUN KOMUTLAR
```

4. **Son satır:** hiçbir dosyanın değiştirilmediğini ve hiçbir git komutunun
   çalıştırılmadığını **açıkça yaz.**

---

# 🔴 SON SÖZ

Altı denetim, altı kez bulgu: **20 → 17 → 24 → 13 → 20 → 18.**
Örüntü **altı kez** kapanmadı. Ve her seferinde bulgular, bir öncekinin
**kapanışından** doğdu.

Bu proje bir şeyi doğru yaptı: **kendi hatalarını sakladığı değil, kaydettiği
bir depo kurdu.** Son oturum kendi işinde **on iki** hata buldu ve on ikisini
de yazdı. Senin işin bunu **onaylamak değil** — on üçüncüyü bulmak.

Ve şunu bil: **bu denetimden sonra Aile 1 başlıyor.** Bulmadığın her kusur,
bundan sonra üretilecek **her sayıya** taşınacak ve raporun içine girecek.

> **Bulacağın her şey, bulunmadığı takdirde jürinin bulacağı bir şeydir.**

Hiçbir şey bulamazsan bunu da yaz — ama **hiçbir şey bulamamak, aradığın
yerlerin listesiyle birlikte anlamlıdır.**

**Bir şeyi büyütmek istiyorsan önce ölç.**
