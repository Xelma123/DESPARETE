# AİLE 0 · DÖRDÜNCÜ BAĞIMSIZ DENETİM — sıfır bağlamlı ajana yapıştırılacak metin

> Aşağıdaki `---` çizgisinden sonraki metnin **tamamını**, sıfır bağlamlı
> yeni bir ajan oturumuna **ilk mesaj** olarak yapıştır.
>
> *Yazıldığı tarih: 21 Ağustos 2026. Taşıdığı her sayı o gün koşturularak
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

# 🔴 BU DÖRDÜNCÜ DENETİM. ÜÇÜNÜ DE OKU — VE ÜÇÜNE DE GÜVENME.

| Tarih | Ne oldu |
|---|---|
| 18 Ağu | Proje *"Aile 0 kapandı, 13/13"* ilan etti |
| 19 Ağu | **Birinci denetim: 20 bulgu.** 13 kriter gerçekten geçiyordu — **ama kapılar yanlış şeyleri ölçüyordu.** Kapanış **iptal** |
| 19 Ağu | 23 bulgu kapatıldı, kapı 13/13, **ikinci kapanış** |
| 20 Ağu | **İkinci denetim: 17 bulgu.** Kapanış **KOŞULLU**; şema iki kez değişti |
| 20 Ağu | Kapı yeniden koşuldu — önce **12/13** *(Ç5 düştü)*, düzeltildikten sonra 13/13 |
| 20 Ağu | **Üçüncü denetim: 24 bulgu** *(B-41…B-64)* + §ANLAŞILMAYANLAR'dan **A-4** |
| 21 Ağu | 23 bulgu kapatıldı, **1'i ölçümle çürütüldü**, kapı **13/13** *(98,2 dk)* |

## 🔴 SENİN ASIL HEDEFİN — üç denetimde de aynı

> **Üçüncü denetimin 23 bulgusunun 23'ünü de yine AYNI ajan kapattı ve yine
> kendi düzeltmesini kendi doğruladı.** Düzeltmeleri yazan, testlerini yazan,
> o testleri koşan ve *"kapandı"* diyen **aynı taraftır.**

Bu, birinci ve ikinci denetimden sonraki durumun **birebir aynısıdır** — ve
o durum her seferinde **yeni bulgular** üretti: 20 → 17 → 24.

> ⚠️ `aile0_audit.md` **üç denetim raporunu da** taşıyor *(3 434 satır)*.
> Haritası kök `README.md`de. Üçünü de oku — ama **otorite** olarak değil,
> **denetlenmesi gereken iddialar** olarak. Üçüncü denetimin iki iddiası
> zaten ölçümle çürütüldü *(aşağıda)*.

---

# 🔴 SENDEN İSTENEN TEK KRİTİK ÖLÇÜM — ve bu kez GÜÇ ANALİZİYLE

| denetim | mutasyon | sağ kalan | taban | oran |
|---|---|---|---|---|
| Birinci | 10 | 8 | 198 test | **%80,0** |
| İkinci | 10 | 7 | 240 test | **%70,0** |
| Üçüncü | 15 | 10 | 284 test | **%66,7** |
| — aynı ölçekte *(ilk 10'u)* | 10 | 7 | 284 | **%70,0** |
| **Dördüncü — SEN** | **≥20** | **?** | **324 test** | **?** |

## 🔴 NEDEN 20 — ve neden öncekiler yetersizdi

Üçüncü denetçi oranı **%66,7** ölçtü *(nominal olarak eşiğin altında)* ve
*"örüntü kapandı"* demeyi **REDDETTİ**: n=15'te binom standart hatası
≈ 12,2 puan, fark 0,3 SH. Aynı ölçekte oran birebir %70.

Proje bunun üzerine **güç analizini yaptı** *(K-055)*:

**Tek örneklem binom · tek yönlü · α = 0,05 · güç = 0,80 · H0: p = 0,70**

| gerçek oran | gereken n |
|---|---|
| 0,30 | **9** |
| 0,40 | **16** |
| 0,50 | **35** |
| 0,60 | **136** |

🔴 **Geçmiş üç denetimin örneklemi yalnızca %40'ın altına bir ÇÖKÜŞÜ
görebilirdi.** %70 → %50 gibi gerçek ama ılımlı bir iyileşme, o
örneklemlerde **tanım gereği görünmezdi.** Üç denetim boyunca aynı cümle
yazıldı ve cümlenin dayandığı eşik **ölçülemezdi.**

## 🔒 BAĞLAYICI ŞARTLAR

1. **En az 20 bağımsız mutasyon.** *(16'nın üstünde, güvenli marjla.)*
2. **Ulaştığın gücü raporla.** Oran düşse bile **n < 16 ise "örüntü kapandı"
   YAZILAMAZ** — bu, projenin kendi kuralıdır ve sana da uygulanır.
3. Mutasyonların **hiçbiri** mevcut **35 hedefli mutasyonun** ya da **215
   mutantlık kör havuzun** tekrarı olmasın; önceki denetimlerin D1–D10,
   KM1–KM10, U01–U15 mutasyonlarının da tekrarı olmasın. **Yeni yollar ara.**
4. 🔴 **Y8 ön koşulu:** her mutasyon için, bozduğu yolun **sağlam koşuda
   tetiklendiğini ÖNCE göster.** Tetiklenmeyen bir yolu bozmak hiçbir şey
   kanıtlamaz — bu hata bu depoda **üç kez** yapıldı.
5. 🔴 Sağ kalanların davranışı **gerçekten değiştirip değiştirmediğini
   ayrıca ölç** *(`dogrulama/sag_kalan_ayikla.py`nin ölçütü)*. Ama dikkat:
   *"eşdeğer"* ile *"o alanın hiç tüketicisi yok"* aynı çıktıyı verir ve
   **ikincisi asıl bulgudur.**

⏱️ **Bütçe:** 20 mutasyon × tam paket *(8,6–10,2 dk)* = 172–204 dk ardışık;
**5 paralel ile ~40–55 dk.** Üçüncü denetçi 15 mutasyonu ~50 dk'da koşturdu.
⚠️ Kendi tahminini **ölçtüğün en büyük** süreden kur — bu depoda süre
tahmini iki kez tutmadı *(K-054: %24 sapma)*.

---

# 🔴 AV SAHASI — bu depoda FİİLEN gerçekleşmiş hata sınıfları

Savunma değil, **nereye bakacağının haritası.** Hepsi `04-NEDEN-BOYLE.md`de:

| # | Ne oldu | Sınıf |
|---|---|---|
| 1 | *"Ne koştuğunu kendisi doğrula"* kuralı **yedi kez** ihlal edildi | **Y7** |
| 2 | Yazılan bir koruma **hiçbir şey doğrulamıyordu**; tek testi korumanın yakalayabildiği tek durumu kullanıyordu | **Y11** |
| 3 | Bir düzeltme **kodda yerini almadı**, `ast.parse` geçtiği için fark edilmedi | **kural 15** |
| 4 | **K-044 bir düzeltmeyi ilan etti, düzeltme koda hiç girmedi** ve iddia **iki oturum** boyunca kayıtta doğru göründü *(B-41)* | **kural 15** |
| 5 | Bir yaklaşık-eşitlik iddiası, tolerans tabanı yüzünden **kırılamazdı** | **Y10** |
| 6 | Bir **sıralama** iddiası (`>`), sabit bir alanda yuvarlama farkıyla **tesadüfen True** dönüyordu | **Y10** |
| 7 | Bir mekanizma sayacı **bilgiyi değil yol geometrisini** ölçüyordu; sıfır bilgi taşıyan null model bilgili koldan iyi skor alıyordu *(B-45)* | **`03` B1** |
| 8 | *"Araç doğru, çıktısı bayat"* örüntüsü **üç kez** yaşandı | **kural 1** |

🔴 **Bu sekiz sınıfın hiçbiri kapandığı ÖLÇÜLMÜŞ değildir.** Bulunan
örnekleri kapandı. Senin işin **fark edilmemiş** örneklerini bulmak.

---

# 🔴 ÜÇÜNCÜ DENETİMİN İKİ İDDİASI ÇÜRÜTÜLDÜ — sen de yanılabilirsin

Bu, bir denetim raporunun **otorite olmadığının** kanıtı ve senin için
doğrudan bir uyarı:

### 1 · B-58 — *"ayraç hiçbir şey yapmıyor"*

Denetçi `sim/kosucu.py::_kurulum_hash`'te `h.update(b"")` gördü ve *"ayraç
niyetiyle yazılmış, hiçbir şey yapmıyor"* dedi. **Devralan ajan da aynı
şeyi bağımsız olarak iddia etmişti.**

Düzeltme uygulanmadan önce desen arandı ve **bulunamadı.** Ham baytlar
okundu:

```
b'h.update(b"\\x1f")'
```

Satırda **gerçek bir 0x1F (UNIT SEPARATOR) baytı** var. Ayraç **çalışıyor**;
ortada kusur yok. 0x1F basılamayan bir kontrol karakteridir ve okuma
araçları onu **görünmez** render eder.

> ⚖️ **İki bağımsız gözün aynı sonuca varması burada bağımsız doğrulama
> DEĞİLDİ — ortak bir araç körlüğüydü.** İkisi de aynı render katmanının
> arkasından baktı.
>
> 🔴 **Sana kuralı:** *"belge kodun kanıtı değildir; kod belgenin
> kanıtıdır"*ın bir katman aşağısı — **render kodun kanıtı değildir;
> BAYTLAR kodun kanıtıdır.** Şüphelendiğin her satırı `read_bytes()` ile oku.

### 2 · B-54'ün önerdiği değişmez tutmadı

Denetçi *"kaçırılan beacon = üretilen − gönderilen − bekleyen"* önerdi.
Ölçüldü: `14 000 − 13 842 − 91 − 0 = 67` — **kapanmıyor.** Bulgu doğruydu
*(sayaç gerçekten korumasızdı)*, **önerilen formül yanlıştı.**

🔴 **Önerdiğin her değişmezi, önermeden önce KOŞTUR.**

---

# 🔴 EN AZ DENETLENMİŞ KOD — bu oturumda yazıldı, bağımsız hiçbir göz bakmadı

Üçüncü denetimin 23 bulgusunu kapatan ajan **20 yeni koruma** yazdı ve
**şemaya beş alan** ekledi. Hepsi mutasyonla sınandığını iddia ediyor
*(20/20 yakalandı)*. **Bunu doğrula.**

| Ne | Nerede | Neden şüpheli |
|---|---|---|
| **Seçim avantajı sayacı** | `sim/kosucu.py` *(`secim_avantaji_ortalama`)* · `tests/test_mekanizma_kapisi.py` | 🔴 **ÖN-KAYITLI BİR KAPIYI besliyor** *(`06` H1.1 revizyonu)*. Kâhin büyüklük kullanıyor. Ölçüt *"null modelde 0 olmalı"* diyor — **gerçekten öyle mi, yoksa 0'a yakın görünen başka bir şey mi?** |
| **Protokol→çerçeve kanalı** | `sim/gozlem.py` *(`yuk_bayt`, `yuku_dondur`)* · `sim/kosucu.py::_beacon_at` · `sim/mac.py::yayin_gonder` | Yeni bir **bilgi kanalı** açtı. `05` §A2'nin üç kuralı *(bayta sayılır · bayattır · kaybolabilir)* gerçekten zorlanıyor mu? Bedel **kaçırılabilir** mi? |
| **Kod sürümü parmak izi** | `sim/karsilastirma.py` *(üçüncü kontrol)* · `kosucu.sonuc()::kaynak_hash` | Y11'in üçüncü ekseni. **Kapsamı dışında kalan dördüncü bir eksen var mı?** |
| **Düğüm başına protokol** | `sim/kosucu.py::_protokoller` | A-4'ün düzeltmesi. Sevk edici (`self.protokol`) hâlâ sarmalanabiliyor — **bu bir kaçak kapısı mı?** |
| **Kapının kapsam kontrolü** | `dogrulama/aile0_kapi_raporu.py` *(`zorunlu`, `TAM_DOSYA_KRITERLERI`, `kapsam_notu`)* | Kapının kapsamı artık desenle korunuyor. **Desen listesi ELLE yazılmış** — `03` B5'in *"etiketi elle taşımak"* tuzağı |
| **İşaretleyiciden türeyen kapsam** | `tests/test_gozlem.py::icerik_testi` | B-43'ün düzeltmesi. İşaretleyici **doğru alanı** işaretliyor mu, yoksa etiket yine elle mi taşınıyor? |
| **`YOLSUZ` beyanı** | `dogrulama/sag_kalan_ayikla.py` | B-52'nin düzeltmesi. 7 girdinin **3'ü** `YOLSUZ` — beyanlar **doğru** mu? |
| **`ULASILABILIRLIK_YOK` nöbetçisi** | `dogrulama/kurulum_kalibrasyonu.py` | B-60'ın düzeltmesi. Kısıt artık zorunlu — **atlanabilecek başka bir yol var mı?** |

---

# DENETLENECEK İDDİALAR

## A · Kapı raporu — 13/13, 21 Ağustos, 98,2 dk

| Kriter | İddia |
|---|---|
| Ç1.1 | Korunum **540/540** *(6 senaryo × 3 trafik × 30 tohum)* |
| Ç1.2 | Dört düşme sebebi de tetikleniyor |
| Ç1.3 | **35/35** mutasyon, her biri **kendi** testiyle · taban temiz |
| Ç1.4 | Boruda kalan **%0,156** |
| Ç2 | 6 test · Ç3 **44** test · Ç5 **29** test · Ç4.1 6 test · Ç6.2 2 test |
| Ç4.2 | Li platosu **1/6,29** · GA **%2,04** |

⭐ **Ç1.4 ve Ç4.2 ÜÇ koşuda da birebir aynı** *(71,0 · 73,9 · 98,2 dk)* —
şemaya beş alan eklenmesine rağmen. Proje bunu *"RNG çekim sırası kaymadı"*
kanıtı sayıyor. 🔴 **Bu çıkarım geçerli mi?** İki sayının kaymaması,
hepsinin kaymadığını gösterir mi? Kalibrasyon tablosu *(B-28'in kaydığı yer)*
bu koşuda yeniden ölçülmedi.

## B · 62 bulgunun kapandığı iddiası

`04-NEDEN-BOYLE.md` **K-047 … K-054** üçüncü denetimin her bulgusunun nasıl
kapandığını yazıyor. 🔴 **En az 10'unu seç ve kapandığını KENDİN doğrula.**

Öncelikli: **B-41** *(kodda gerçekten var mı?)* · **B-42** · **B-43** ·
**B-45** · **B-47** · **B-52** · **B-57** *(kapatılmadı — sebebi savunulabilir mi?)*

🔴 Kapanma iddiası genelde *"şu test yazıldı"* biçiminde. O testin gerçekten
ilgili şeyi ölçtüğünü **mutasyonla** sına — ve **mutasyonu biraz değiştir**:
fazla dar bir test yalnızca denetçinin yazdığı tek mutasyonu yakalar.

## C · Bu oturumda üretilen sayılar

| İddia | Değer | Üretici |
|---|---|---|
| Seçim avantajı | kör **−0,167** · bilgili **+0,037** · null **+0,008** ve **−0,012** | `test_mekanizma_kapisi.py` |
| Kanal kanıtı | mesafe-vektörü kolu S0'da atlama **1,00 → 2,33** | kâhinsiz DV protokolü, S0/S2, tohum 1 |
| Yük bayt muhasebesi | **10,000 bayt/beacon** *(tam)* | `test_gozlem.py -k b47` |
| Kör tarama havuzu | **215** *(203'ten büyüdü)* | `kor_mutasyon.py` |
| Güç analizi | %70→%40 için **n=16** · %70→%50 için **n=35** | `scipy.stats.norm` |

**En az beşini yeniden üret.** Tutmuyorsa bulgudur.

---

# 🔍 ŞÜPHE LİSTESİ — bu denetime özel

> Önceki üç listeyi de uygula *(`denetim/` altında)*. Ağırlığı aşağıdakilere ver.

**1 · 🔴 ÖN-KAYITLI KAPI DEĞİŞTİ — meşru mu?**
`06` H1.1'in mekanizma kapısı **revize edildi** *(K-050)*: eski ölçüt
*(ara bölge kullanımı)* bilgiyi değil geometriyi ölçüyordu. Yeni ölçüt
`secim_avantaji_ortalama`. 🔴 Sor: bu bir **düzeltme** mi, yoksa aracın
hipotezi test edemediği görüldükten sonra **hipotezin ölçütünü değiştirmek**
mi? `03` kural 3 *(eşiği geriye dönük gevşetme)* ihlal edildi mi? Kayıt bunu
tartışıyor — **savunması yeterli mi?**

**2 · Yeni ölçüt kendi null modelini geçiyor mu — SENİN null'ünle?**
Proje iki null model kullandı *(rastgele komşu · kuyruğa göre)*. **Üçüncü
bir null yaz** ve avantajın yine ~0 çıktığını doğrula. Çıkmıyorsa ölçüt
bilgiyi değil başka bir şeyi ölçüyor.

**3 · Protokol→çerçeve kanalı bedelsiz bilgi taşıyor mu?**
`beacon_yuku` kancası. 🔴 Bedeli **atlatmanın** bir yolu var mı — çok büyük
bir yük, tip kontrolünü delen bir değer, ya da beacon yerine başka bir
çerçeve? `05` §A2'nin *"bayta sayılır"* kuralı **zorlanıyor** mu?

**4 · Y11'in dördüncü ekseni**
Karşılaştırma koruması üç eksende bakıyor: paket evreni · kurulum · kod.
🔴 **Dördüncü bir eksen bul** — reddetmesi gerekirken kabul ettiği bir çift.

**5 · Kapının kapsam listesi elle yazılmış**
`zorunlu` desen kümeleri elle tutuluyor. 🔴 Bir kriterin kapsamı, desen
listesi **de** güncellenerek daraltılabilir mi?

**6 · `08`in 24 maddesi — iki yönlü**
*(a)* *"Yapmaz"* denen bir şey **yapılıyor** mu? *(b)* Kodda modellenmemiş
ama listede **olmayan** bir şey var mı? *(Üç denetim sırasıyla 4, 4 ve 2
madde ekletti.)*

**7 · Şema donduruldu mu, gerçekten?**
Beş alan eklendi ve *"Aile 1 başlamadan donduruldu"* deniyor. 🔴 Şemayı
değiştirmenin **hâlâ açık** bir yolu var mı? `protokol_teshis` slotu keyfi
anahtar kabul ediyor — bu bir kapı mı?

**8 · B-57 kapatılmadı — bu savunulabilir mi?**
55 kaydın 25'inde üretici satırı var. Proje *"uydurmak daha ağır ihlal"*
diyerek kapatmadı. 🔴 Sor: **sayı taşıyan** kaç kayıt üreticisiz, ve
bunlardan kaçının sayısı bugün **yeniden üretilebilir**? Üretilemeyen bir
sayı `04`te hâlâ olgu gibi duruyorsa, bu bir bulgudur.

**9 · Belge rafineleştirmesi bir şey bozdu mu?**
21 Ağustos'ta dosyalar taşındı *(`denetim/`, `ciktilar/`)*, `v2/README.md`
inceltildi, `04`e içindekiler eklendi. 🔴 Kırık atıf, kaybolan bilgi ya da
**sessizce değişmiş bir sayı** var mı?

**10 · Aile 1 gerçekten kurulabilir mi?**
Proje bunu *"S0'da atlama 1,00 → 2,33"* ile kanıtladı. 🔴 O protokolü
**kendin yaz ve koştur.** S2'de 1,00'e düşüyor — proje bunu *"ayarlanmadı"*
diye sonuç saymadı. **Bu savunma yeterli mi, yoksa yapısal bir sınır mı?**

**11 · İstatistik katmanı hâlâ YOK**
`grep -rn "wilcoxon\\|holm\\|scipy" --include=*.py .` → yalnızca beyan.
🔴 Ön-kaydın *"ZORUNLU"* dediği NaN koruması yazılmadı. `08` madde 21 bunu
beyan ediyor — **beyan yeterli mi?**

**12 · Bu promptun kendisi**
Bu metni **proje yazdı**, denetçi değil. 🔴 Neye bakmanı istemiyor olabilir?
Listede **olmayan** bir yere bak.

---

# ÇALIŞMA BİÇİMİN

1. **Önce oku, sonra koştur, en son yorumla.** İlk: kök `README.md` →
   `v2/03-YONTEM-KURALLARI.md` → `04`ün sonundaki **Y1–Y11**.
2. Her bulgunun yanında **üretici komut** ve **kaynak dosya:satır**.
3. Bir iddiayı doğrularken **iddianın kendi ölçütünü kullanma.**
4. ⭐ **Y6 — beklenenden iyi çıkan sonuç, kötü çıkan kadar şüphelidir.**
5. ⭐ **Y8** — bozduğun yolun tetiklendiğini **önce** göster.
6. ⭐ **Y10** — bir yaklaşık-eşitlik ya da **sıralama** iddiasını kırılabilir
   olduğunu göstererek yaz. `>` operatörü hiçbir tolerans almaz.
7. ⭐ **Y11** — bir korumayı kapsamı **dışındaki** bir vakayla sına.
8. 🔴 **Şüphelendiğin satırı `read_bytes()` ile oku** — B-58 tam olarak
   bunun yapılmamasından doğdu.
9. **Önerdiğin her değişmezi, önermeden önce koştur** — B-54'ün formülü
   tutmadı.
10. Deneme için depoyu geçici bir dizine kopyala; **aslını değiştirme.**

---

# ORTAM VE KISITLAR

| | |
|---|---|
| Platform | Windows 11 · Python 3.11 · numpy, scipy, pytest kurulu |
| Dil | Kod ve belgeler **Türkçe**. Raporunu da Türkçe yaz |
| ⚠️ Konsol | Çıktı yönlendirirken `PYTHONIOENCODING=utf-8` — varsayılan cp1254 Türkçe karakterde çöküyor |
| 🔴 Git | **Hiçbir git komutu çalıştırma — `status` dahil** |
| 🔴 Kod | **Depodaki hiçbir dosyayı DEĞİŞTİRME.** Deneme için `tempfile.mkdtemp` kopyası |
| 🔴 Tohum | **2000–2029 HİÇBİR AMAÇLA koşulmaz** *(mühürlenmemiş ana deney)*. Ayarlama: **1–30** |
| İşlemci | En fazla **10 çekirdek.** 30 dk'yı aşacak koşudan **önce** süre tahminini yazdır ve **SOR** |
| Yazacağın tek dosya | `aile0_audit.md` |
| ⚠️ Yol | Betiklerinde **depo dışına** yazma; üretici komutların depo kökünden koşabilir olmalı *(üçüncü denetimin `scratchpad/den3/…` komutları yeniden üretilemedi)* |

### ⏱️ Ölçülmüş süreler — 21 Ağustos, 10 çekirdek

| Komut | Süre |
|---|---|
| `python -m pytest tests -q` | **8,6–10,2 dk** *(324 test · iki ölçüm; bütçeni ÜSTÜNE göre kur)* |
| `python -m pytest tests/test_kapi_secimleri.py -q` | **12 sn** ⭐ |
| `python dogrulama/mutasyon_on_kontrol.py` | **0,4 dk** ⭐ |
| `python dogrulama/sag_kalan_ayikla.py` | ~5 dk |
| `python dogrulama/kurulum_kalibrasyonu.py` | ~2 dk |
| `python dogrulama/kor_mutasyon.py 24` | ~18 dk |
| `python dogrulama/mutasyon_paketi.py` | ~25 dk |
| `python dogrulama/aile0_kapi_raporu.py` | **98 dk** 🔴 *(izin gerekir)* |

---

# ENVANTER — 21 Ağustos 2026, koşturularak ölçüldü

| Büyüklük | Değer |
|---|---|
| Test | **324** *(17 dosya)* |
| Hedefli mutasyon | **35** |
| Kör mutant havuzu | **215** |
| Karar kaydı | **55** *(K-001…K-055)* |
| Kapsam maddesi | **24** |
| Toplam bulgu | **63** · 1 çürütüldü · **62 kapalı** · **1 açık (B-57)** |
| Satır | `sim` **3 638** · `tests` **5 445** · `dogrulama` **3 664** |

```
README.md          harita — BURADAN BAŞLA
aile0_audit.md     üç denetim raporu (3 434 satır)
v2/                belgeler 00–09
denetim/           bu prompt ve öncekiler
ciktilar/          araç çıktıları + politika
sim/ tests/ dogrulama/
```

**Kat 4 (yönlendirme) YOKTUR** — Aile 1'in işi.
Protokol arayüzü: `protokol_fabrikasi(kon) → protokol(gozlem) → int | None`
*(fabrika **düğüm başına** çağrılır)* · isteğe bağlı `protokol.beacon_yuku(dugum)`

---

# ÇIKTI: `aile0_audit.md` — nasıl güncellenecek

Dosya **üç denetimin raporunu** taşıyor. 🔴 **İçeriğini SİLME, DEĞİŞTİRME.**

1. Baştaki durum bloğunu **dördüncü denetimi de içerecek** şekilde genişlet.
2. Sonuna `# DÖRDÜNCÜ DENETİM — <tarih>` bölümü ekle.
3. 🔴 Bulgu numaraları **B-65**'ten devam eder.

```
## 0. YÖNETİCİ ÖZETİ
    Kapanış geçerli mi: EVET / KOŞULLU / HAYIR — üç cümlede
    🔴 SAĞ KALAN ORANI + ULAŞILAN GÜÇ, ilk paragrafta

## 1. YENİ BULGULAR                       (B-65'ten)
    ciddiyet · nerede (dosya:satır) · İDDİA · ÖLÇTÜĞÜM ·
    ÜRETİCİ KOMUT (depo kökünden koşabilir) · beklenen/görülen ·
    neden önemli · öneri
    🔴 Önerdiğin her değişmezi ÖNCE koştur.

## 2. ÜÇÜNCÜ DENETİMİN BULGULARI — kapanma doğrulaması
    Seçtiğin ≥10 bulgu · mutasyonla sınadın mı · test fazla dar mı

## 3. DOĞRULANAN İDDİALAR          ## 4. ÜRETİLEMEYEN İDDİALAR

## 5. 🔴 KENDİ MUTASYONLARIN
    ≥20 mutasyon · her biri için Y8 tetiklenme sayısı (ÖNCE) ·
    324 testten sağ çıktı mı · sağ kaldıysa davranış değişiyor mu
    🔴 SAĞ KALAN ORANI · SERİ TABLOSU · **ULAŞILAN GÜÇ**
    🔴 n < 16 ise "örüntü kapandı" YAZILAMAZ

## 6. ŞÜPHE LİSTESİ SONUÇLARI      ## 7. KAPSAM BEYANINA EKLENECEKLER

## 8. 🔴 ANLAŞILMAYANLAR
    🔴 BOŞ BIRAKILAMAZ. Üç denetimde de bu bölümden GERÇEK KUSUR çıktı —
    üçüncüsünde A-4 buradan geldi ve bir kâhin kanalıydı.

## 9. KOŞTURDUĞUN KOMUTLAR
```

4. **Son satır:** hiçbir dosyanın değiştirilmediğini ve hiçbir git komutunun
   çalıştırılmadığını açıkça yaz.

---

# 🔴 SON SÖZ

Bu proje üç denetimden geçti ve her seferinde bulgu çıktı: **20 → 17 → 24.**
Örüntü **üç kez** kapanmadı. Dördüncüsünde kapanabilir — ama ancak
**yeterli güçte bir örneklemle** ölçülürse.

İki şeyi birden bil:

1. **Bu depo gerçekten sağlam.** 13 kriter üç koşuda da geçti, korunum
   defteri nesne düzeyinde dürüst, fizik analitik olarak doğrulanmış.
2. **Ve üç bağımsız göz üç kez yanıldığını gösterdi** — biri de kendi
   raporunda: `b"\\x1f"` bir kez `b""` sanıldı ve **iki kişi birden** yanıldı.

Senden beklenen bir onay değil.
**Bulacağın her şey, bulunmadığı takdirde jürinin bulacağı bir şeydir.**

Hiçbir şey bulamazsan bunu da yaz — ama **hiçbir şey bulamamak, aradığın
yerlerin listesiyle birlikte anlamlıdır.** Nereye baktığını yaz.

**Bir şeyi büyütmek istiyorsan önce ölç.**
