# DEVİR — sıfır bağlamlı ajan için tek giriş noktası

**Tarih:** 8 Eylül 2026 · **Teslim:** 19 Aralık 2026
**Durum:** Faz 0 adım ①–④ bitti · adım ⑤–⑥ açık · **451 test geçiyor**

> Bu belge, projeyi hiç görmemiş bir ajanın **kod yazmadan önce** okuması
> içindir. §2'de bir doğrulama listesi, §3'te bir **denetim görevi** var.
> İkisi bitmeden tek satır yeni özellik yazılmaz.
>
> 📁 Bir önceki devir (5 Eylül) `arsiv/DEVIR-2026-09-05.md`dedir. Oradaki
> sayılar **bayattır**; çelişki olursa bu belge ve `v2/04-NEDEN-BOYLE.md`nin
> K-099 – K-103 kayıtları geçerlidir.

---

## 0 · TEK CÜMLEYLE

Karıştırma (jamming) altındaki taktik İHA mesh ağlarında yönlendirme
protokollerini karşılaştıran bir **kesikli olay simülatörü** yazılıyor.
Ürün **öğrencinin kendi tasarladığı protokoldür**; AODV · OLSR · AOMDV
**kıyas tabanıdır**. Şu an simülatör kalibre ediliyor; protokollerin
hiçbiri henüz yazılmadı.

🔒 **KAPSAM — öğrenci tarafından kesinleştirildi:**
> *"Kontrollü bir deney ortamında routing protokolünün jamming karşısındaki
> davranışını izole etmek."*

Bu cümle bir sınırdır. "Gerçekçi bir harp senaryosu kurmak" **kapsam dışıdır**;
gerçekçilik yalnız *"kurulum protokolü zayıflatmıyor mu"* sorusunu cevaplamak
için gereklidir. Li ve ark. replikasyonu **onaylandı** (Faz 1).

---

## 1 · 🔴 ÇALIŞMA KURALLARI — pazarlığa kapalı

Bunlar öğrencinin koyduğu kurallardır, tercih değil.

| # | Kural |
|---|---|
| 1 | **Hiçbir `git` komutu çalıştırma** — `status` dâhil. |
| 2 | Simülatör kodu yazmadan önce **yapıyı anlat ve onay al**. |
| 3 | 30 dakikayı aşacak koşumlar için **önce sor**. Süre tahminleri her zaman **BANT** olarak verilir. |
| 4 | Her çağrıda `PYTHONIOENCODING=utf-8` — konsol Türkçe karakterde çöküyor. |
| 5 | Uzun heredoc'lar Bash'te bozuluyor — uzun metin için **dosya yazma aracını** kullan. |
| 6 | Doğrulama **AST ile** yapılır, metin eşleştirmeyle değil. |
| 7 | Raporlanan her sayı **üretici komutunu** taşır. |
| 8 | ≥30 tohum · protokole kâhin erişim yok · eşiği sonradan gevşetme yok · olumsuz sonucu gizleme yok · ölçmeden iddia etme yok · ön-kayıt · korunum denklemi · ayrık RNG akışları · ölçüm penceresi. |
| 9 | Biçim: **KONUM → HEDEF → YAPI (onay) → UYGULAMA → DOĞRULAMA → SONRAKİ** |
| 10 | **Türkçe konuş.** Özet kısa ve net: *ne oldu · neden önemli · sırada ne var*. **Kod referansı verme** — öğrenci kararları okuyor, kodu değil. |
| 11 | Windows `spawn`: `Pool` kullanan her betikte `if __name__ == "__main__":` şart. **Asla `python -` ile stdin'den çalıştırma** — havuz kilitlenir. |

🔴 **12 · Öğrencinin verdiği sayıları mutlak gerçek sayma.** Onlar fikir ve
yaklaşık değerdir; nihai mantığı ve kararı **sen** verirsin. Ama kapsam ve
gerçekçilik kararları öğrenciye gider.

🔴 **13 · Ölçtüğünü sandığın şey yanlış olabilir.** Testin ya da ölçümün
amacını tam karşılamıyor olabilir. Bir sonuç beklentine uyuyorsa, *"bu ölçüm
gerçekten bunu mu ölçüyor"* diye bir kez daha sor.

---

## 2 · 🔴 BİRİNCİ İŞ — DOĞRULAMA LİSTESİ

Sırayla koştur. Hepsi geçmeden hiçbir şeye dokunma.

```bash
cd C:/Users/Xelma123/Desktop/desparete_pls && PYTHONIOENCODING=utf-8 python -m pytest tests2 -q
```
**Beklenen:** `451 passed` · ~7 dakika.
*(Üretici: 8 Eylül 2026, bu komut.)*

```bash
cd C:/Users/Xelma123/Desktop/desparete_pls && PYTHONIOENCODING=utf-8 python kalibrasyon/mimari_denetimi.py
```
**Beklenen:** `Yapisal ihlal YOK` · D12'de `kokeni yazilmamis 0` ·
`olu koken kaydi 0` · kova dağılımı `SINANMAMIS 46`.
*(Sondaki "33 not" hata değildir.)*

```bash
cd C:/Users/Xelma123/Desktop/desparete_pls && PYTHONIOENCODING=utf-8 python kalibrasyon/adim9_kapanis.py
```
**Beklenen:** 6 tam uzunlukta koşu, hepsinde `korunum + mutabakat : HEPSI TAMAM`.
⏱️ **25–40 dakika** — arka planda koştur.
⚠️ **Bu komut 8 Eylül değişikliklerinden sonra KOŞULMADI.** Karıştırıcı güç
tablosu doldu; daha önce açık güç vermeden koşamayan kollar artık koşuyor.
Sonucu bilinmiyor — bir sürprizle karşılaşırsan bu beklenen bir durumdur.

```bash
cd C:/Users/Xelma123/Desktop/desparete_pls && PYTHONIOENCODING=utf-8 python -u kalibrasyon/pdr_tavani.py
```
**Beklenen:** karıştırıcısız kolda **PDR ≈ 1,000**. ⏱️ **20–40 dakika**.
⚠️ Bu da 8 Eylül'den sonra koşulmadı.

---

## 3 · 🔴 İKİNCİ İŞ — SON OTURUMUN DENETİMİ

> Doğrulama listesi *"kod çalışıyor mu"* diye sorar. Bu bölüm **"son oturumda
> verilen kararlar doğru mu"** diye sorar. Öğrencinin talebi budur ve
> yeni bir şey yapmadan önce gelir.

Son oturum (8 Eylül) Faz 0'ın ③ ve ④ adımlarını kapattı. Kayıtları
`v2/04-NEDEN-BOYLE.md` → **K-101, K-102, K-103**. Aşağıdakiler o oturumun
**bilinen zayıf noktalarıdır**; her biri düşülmüş, gizlenmemiştir.

### 3.1 · 🔴 ρ taraması YENİ örnekleme anlarıyla tekrarlanmadı
Çalışma noktası (**−15,0 dBm · ρ = 0,258**) üç sabit anla (200/260/310 s)
koşulan bir taramadan çıktı. **Sonra** o örneklemenin darbeli sınıfta
örtüştüğü (aliasing) fark edildi ve anlar dokuz taneye çıkarıldı — ama
**tarama yeniden koşulmadı.**

Gerekçem şuydu: `surekli` zamanla değişmez, dolayısıyla anların sayısı
sonucu değiştirmez. **Bu bir iddia, ölçüm değil** — sönümleme zamanla
değişiyor, yani dokuz an dokuz farklı sönümleme gerçeklemesi demek.

```bash
cd C:/Users/Xelma123/Desktop/desparete_pls && PYTHONIOENCODING=utf-8 python kalibrasyon/karistirici_gucu.py tarama
```
**Kontrol:** seçilen güç yine **−15,0 dBm** mi? Değilse çalışma noktası
değişir ve K-103'ün bütün alt kararları yeniden bakılır. ⏱️ **10–25 dakika**.

### 3.2 · ⚠️ Kâhin tavanı (0,959) yalnız 3 TOHUMLA ölçüldü
*"Karıştırma altında ulaşılabilir tavan %95,9"* sayısı üç tohumdan geliyor ve
tohumlar arası yayılım büyük (0,989 · 0,994 · **0,894**). Kural 8 ≥30 tohum
diyor. Bu sayı bir **çapraz kontroldü**, sonuç satırına girmiyor — ama üç
belgeye yazıldı ve orada kesinmiş gibi duruyor.

**Kontrol:** ya ≥30 tohumla tekrarla, ya da geçtiği üç yerde *"3 tohum,
geçici"* olarak işaretle. İkisinden biri yapılmalı.

### 3.3 · ⚠️ ρ'nun paydası tek anda örnekleniyor
ρ = 1 − (karıştırılmış derece / temiz derece). Karıştırılmış derece dokuz
anda ölçülüyor ama **temiz derece yalnız birinde** (t = 200,0 s). Payda
sönümleme gürültüsü taşıyor ve pay taşımıyor — asimetrik.

**Kontrol:** temiz dereceyi de dokuz anda ölçüp ρ değişiyor mu bak. Değişmiyorsa
mesele yok, değişiyorsa ρ'nun bütün rakamları etkilenir.

### 3.4 · ⚠️ `aldatici` ile `surekli` neden TIPATIP aynı çıktı
İkisi de ρ = 0,258, boğulan 0,13, ayrılan 0/30 verdi. Bu *"eşleştirilmiş
kontrast"* diye yorumlandı (bağ hasarı sabit, tek fark CSMA). Ama aldatıcının
açık oranı 0,978, sürekliki 1,000 — **birebir aynılık beklenmezdi**.

**Kontrol:** aldatıcı, dokuz örnek anının hepsinde AÇIK mı? Öyleyse aynılık
beklenen sonuçtur ve yorum doğrudur. Değilse aynılık bir tesadüftür ya da
bir kusurdur, ve *"eşleştirilmiş kontrast"* iddiası çöker.

### 3.5 · 🔴 Dört sabit `SINANMAMIS`'tan `TEDAVI`ye taşındı — bu aklama mı?
`darbe_periyodu_s` · `darbe_gorev_cevrimi` · `taramali_konak_suresi_s` ·
`taramali_konak_sayisi`. Gerekçe: bunlar bir donanımın fiziğini iddia
etmiyor, **kolun tanımı**. Köken borcu 50 → 46 oldu — **yeni ölçüm
yapılmadan**.

🔴 Bu, borcu ölçmeden azaltmanın klasik yoludur. Bağımsız yargını ver:
gerçekten tedavi değişkeni mi, yoksa gerekçesizliği başka bir kovaya mı
taşındı? Taşındıysa geri al. Kaldıysa **ön-kayıtta kol tanımı olarak ilan
edilmeleri ve duyarlılık denetiminde oynatılmaları** şarttır — devredilen
yükümlülük budur.

### 3.6 · ⚠️ Sert kısıtın zaman anlamı SONUÇ GÖRÜLDÜKTEN SONRA netleşti
Darbeli kol *"hiçbir tohumda ağ ikiye ayrılmayacak"* kısıtını 1/30 tohumda
çiğnedi. Kısıt eğilmedi; **zaman anlamı** netleştirildi: *bölünme, en hızlı
taban çizgisinin rota geçersizleme süresinden (AODV 3 s) uzun sürmeyecek.*
Dayanağı iki ölçüm: temiz grafik 30/30 tohumda tek parça, ve ayrılmaların
dördü de darbenin AÇIK evresinde.

⚠️ Ama netleştirme **sonucu gördükten sonra** yazıldı ve bu K-103'te
düşülmüştür. Bağımsız yargını ver: yapıdan önce de sorulabilir bir soru
muydu, yoksa hoşa gitmeyen bir sonucun etrafından dolaşma mı?
🔒 Temiz grafiğin tek parçalılığı da **tek anda** (t = 200,0) ölçüldü, dokuz
anda değil — istersen sıkılaştır.

### 3.7 · ⚠️ Testlere gerekçesiz bir eşik girdi
Karıştırıcı PER testi artık `kirli − taban > 1e-6` istiyor. Sebep meşru:
eski hâli bir ULP farkıyla (3,1e-16) karıştırıcı **kapalıyken** geçiyordu.
Ama `1e-6` seçilmiş bir sayıdır ve köken defterinde değildir (defter test
sabitlerini kapsamıyor). Kapsaması gerekip gerekmediğine karar ver.

### 3.8 · ⚠️ `karistirici_baslangic_s = 150 s` başka nereleri sessizleştirdi?
Bu kapı testlerde **yedi kırık + iki boş yere yeşil** üretti; hepsi düzeltildi.
Ama denetim yalnız `tests2/` içinde yapıldı. **Kalibrasyon betikleri
taranmadı.** t < 150 s'de örnekleme yapan bir betik, karıştırıcıyı kapalı
ölçüyor ve bunu söylemiyor olabilir.

**Kontrol:** karıştırıcıya dokunan her kalibrasyon betiğinde örnekleme anı
`karistirici_baslangic_s`in üstünde mi?

### 3.9 · ⚠️ Şartname ile kod başka nerede ayrışıyor?
`07-SIMULATOR-TASARIMI.md` §05.4 karıştırıcının **çerçeveden geçtiğini**
söylüyor; kod onu **alan merkezinde sabit** tutuyor. Bu ayrışma §05.6'da
açıkça yazıldı — ama yalnız bu bölüm için arandı.

**Kontrol:** şartnamenin diğer bölümleri kodla uyuşuyor mu? Uyuşmayan her
yer ya koda ya belgeye yazılmalı; sessiz kalan bir ayrışma en tehlikelisidir.

---

## 4 · NEREDEYİZ

### Faz 0 — simülatörü karara bağlama
| adım | konu | durum |
|---|---|---|
| ① | ölçüm penceresi ve evreler | 🟢 bitti |
| ② | çalışma noktası (alan · yoğunluk · derinlik) | 🟢 **1800 m** · derece 8,67 · çiftlerin %31'i 3+ atlama |
| ③ | mobilite (Θ kapısı) · Doppler ayrımı | 🟢 **Θ = 5,93** · hız 0,25–0,75 m/s |
| ④ | tehdit modeli — güç kalibrasyonu | 🟢 **−15,0 dBm · ρ = 0,258** |
| ⑤ | evre metrikleri | ⏳ **SIRADA** |
| ⑥ | sonuç satırında `ham` bölümü · kapsam sınırlarının beyanı | ⏳ |

### Adım ⑤ — sıradaki iş
Dört metrik tanımlanacak ve uygulanacak. Anti-jamming bir protokolün asıl
iddiası *"ne kadar bozuldum"* değil **"ne kadar hızlı toparlandım"**dır:

| metrik | ne ölçer |
|---|---|
| şok derinliği | karıştırıcı açıldıktan sonra en dip nokta |
| toparlanma süresi | dipten kararlı hâle dönüş süresi |
| toparlanma tamlığı | dönülen seviye / temiz evre seviyesi |
| tespit gecikmesi | karıştırma başlangıcı ↔ protokolün ilk tepkisi |

🔴 Dördü de **tanımlanmadan** kod yazılmaz: "kararlı hâl" ve "ilk tepki"
ölçütleri sayıya bağlanmalı, yoksa sonradan sonuca göre seçilirler.

### Sonraki fazlar
| faz | konu |
|---|---|
| 1 | duyarlılık denetimi + **Li ve ark. zincir replikasyonu** |
| 2 | dikey dilim — tek protokol uçtan uca |
| 3 | taban çizgileri (AODV · OLSR · AOMDV) + **ön-kayıt mührü** |
| 4 | öğrencinin protokolü |
| 5 | tam deney — 💡 öğrencinin fikri: *parça parça koşup sonuçları birleştirmek* |
| 6 | yazım |

---

## 5 · AÇIK BORÇLAR

| borç | durum |
|---|---|
| **46 parametre `SINANMAMIS`** | 🔴 ön-kayıt mühürlenmeden sıfırlanmalı; D12 her koşumda sayıyor |
| `reaktif_sezme_s` · `reaktif_patlama_s` | 🔴 donanım iddiası, kaynak yok — `02-DOGRULANMIS-KAYNAKLAR.md`e girmeli |
| `isinma_s` | ölçülmedi, eski depodan devir |
| `olcum_bitis_s` · `kosu_bitis_s` | seçilmedi, devralındı |
| `dugum_sayisi = 40` | gerekçesi doğrulanmamış kaynakta |
| `BAGIL_HIZ_TABANI_MS` · `KOSE_ONBELLEK_SINIRI` | değer türetilmedi |
| `yeniden_deneme_siniri = 4` | 802.11'in kısa çerçeve sınırıyla (7) uyuşmuyor; etkisi ölçüldü, yok |
| `06-ON-KAYIT.md` | ⚠️ `sim2/`ye göre **revize edilmedi** |
| hareketli karıştırıcı | şartnamede var, kodda yok (§05.6) |

### Ön-kayıta girmesi gereken iki tahmin *(K-103'te yazıldı)*
1. **`taramali` gereksiz olabilir:** 100 ms konak, AODV'nin 1 s'lik
   zamanlayıcısından 10 kat hızlı — protokoller onu *seyreltilmiş sürekli*
   karıştırıcı gibi görebilir.
2. **`taramali` şiddet farkı taşıyor:** ortalaması −4,77 dB düşük. *"Taramalı
   zayıf çıktı"* bulgusu mekanizmaya tek başına yazılamaz.

---

## 6 · MİMARİ — bilinmesi zorunlu dört yapı

| yapı | ne yapar |
|---|---|
| **korunum defteri** | `üretilen = teslim + düşen + kuyrukta + uçuşta`. Ayrıca `mutabakat()` ayrı bir kapıdır. |
| **sayaç kütüğü** | Sayaçlar tek yerde tanımlı; pencere ikizleri ve kapalı kümeler otomatik türer. |
| **gözlem penceresi** | Protokolün görebildiği her şey — **genişletilemez** izin listesi. `Kahin[T]` tipi kazara kâhin erişimini engeller. |
| **köken defteri** | Her parametre beş kovadan birinde: türetilmiş · ölçülmüş · kaynak · tedavi · sınanmamış. D12 kapısı denetler. |

🔒 **Rastgelelik iki türlü:** kanal için hash tabanlı (durumsuz, protokolden
bağımsız), olay akışı için sıralı akışlar. Reaktif karıştırıcının sezmesi
hash'ten gelir — sıralı olsaydı çok iletim yapan protokol akışı kaydırır ve
kollar desenkronize olurdu.

---

## 7 · OKUMA SIRASI

| # | Dosya | Neden |
|---|---|---|
| 1 | **bu dosya** | durum · kurallar · denetim görevi |
| 2 | [`v2/07-SIMULATOR-TASARIMI.md`](v2/07-SIMULATOR-TASARIMI.md) | ⭐⭐⭐ **şartname** — simülatörün ne olduğu burada karara bağlandı |
| 3 | [`v2/03-YONTEM-KURALLARI.md`](v2/03-YONTEM-KURALLARI.md) | ⭐⭐ 15 kural — bu alanın hata sınıfları, bayatlamaz |
| 4 | [`v2/04-NEDEN-BOYLE.md`](v2/04-NEDEN-BOYLE.md) | 103 karar kaydı. ⚠️ 10 000 satır — **baştan okuma**, K-095'ten sonrasını oku |
| 5 | [`v2/01-PROBLEM-VE-AMAC.md`](v2/01-PROBLEM-VE-AMAC.md) | problem · özgünlük · kısıtlar |
| 6 | [`v2/05-GOZLEM-PENCERESI.md`](v2/05-GOZLEM-PENCERESI.md) | protokolün görebildiği her şey |
| 7 | [`v2/06-ON-KAYIT.md`](v2/06-ON-KAYIT.md) | aileler · hipotezler — ⚠️ revize edilmedi |

🔒 **Kodun kendisi belgedir.** Her modülün başlığında *"neden böyle,
alternatifi neden elendi, hangi ölçüm bunu söyledi"* yazılıdır. Bir davranışı
merak ediyorsan önce dosya başlığını oku.

---

## 8 · KOMUTLAR

```bash
cd C:/Users/Xelma123/Desktop/desparete_pls && PYTHONIOENCODING=utf-8 python -m pytest tests2 -q
```
```bash
cd C:/Users/Xelma123/Desktop/desparete_pls && PYTHONIOENCODING=utf-8 python kalibrasyon/mimari_denetimi.py
```
```bash
cd C:/Users/Xelma123/Desktop/desparete_pls && PYTHONIOENCODING=utf-8 python kalibrasyon/karistirici_gucu.py tarama
```
```bash
cd C:/Users/Xelma123/Desktop/desparete_pls && PYTHONIOENCODING=utf-8 python kalibrasyon/karistirici_gucu.py sinif
```
```bash
cd C:/Users/Xelma123/Desktop/desparete_pls && PYTHONIOENCODING=utf-8 python kalibrasyon/calkanti.py
```
```bash
cd C:/Users/Xelma123/Desktop/desparete_pls && PYTHONIOENCODING=utf-8 python kalibrasyon/calisma_noktasi.py
```
```bash
cd C:/Users/Xelma123/Desktop/desparete_pls && PYTHONIOENCODING=utf-8 python kalibrasyon/adim9_kapanis.py
```
```bash
cd C:/Users/Xelma123/Desktop/desparete_pls && PYTHONIOENCODING=utf-8 python -u kalibrasyon/pdr_tavani.py
```

---

## 9 · İLK TESLİMİN — soru değil, RAPOR

1. **Doğrulama listesinin sonucu** — dört komut, dört sonuç.
2. **§3'ün denetimi** — dokuz maddenin her biri için: ne ölçtün, ne buldun,
   son oturumun kararı **ayakta mı yoksa düştü mü**. Düşen varsa neyin
   değişmesi gerektiğini söyle.
3. **Adım ⑤'in yapısı** — dört metriğin tanımı, onay için.

🔴 *"Şunu mu yapalım, bunu mu?"* diye sormak bir teslim değildir. Ölçütü
zaten ilan edilmiş bir kararı vermek **senin işin**; öğrenciye yalnızca
kapsam ve gerçekçilik kararları gider.

⚠️ **Bir sayıyı rapor etmeden önce kendin üret.** Bu belgedeki her sayı bir
komuttan geldi; komutu koşturmadan sayıyı tekrarlama.

---

## 10 · SON UYARI

Bu projede **en tehlikeli hata sınıfı sessiz olanıdır**: makul görünen bir
sayı üreten yanlış model. Bugüne kadar bulunanların hepsi ölçülerek bulundu,
hiçbiri gözle görülmedi — duvara yapışan düğümler, hiç gövdeye değmeyen
reaktif karıştırıcı, geçmeyen bağın üstünde tanımlı menzil, çerçeve boyunca
donan kanal, beş kat uzun ömürlü topoloji bilgisi.

🔴 Son oturumun en pahalı dersi de bu sınıftandı: yeni bir **kapı** eklemek,
o kapıdan geçen bütün testleri sessizce boşaltabilir. Bir kapı eklerken
sorulacak soru *"ne kırıldı"* değil, **"ne hâlâ geçiyor ama artık hiçbir şey
doğrulamıyor"**dur. Bir testin geçmesi, doğru sebeple geçtiği anlamına gelmez.

> **Bir şeyi iddia etmeden önce ölç. Ölçemiyorsan iddia etme.**
