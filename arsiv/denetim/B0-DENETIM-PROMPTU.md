# B0 · BAĞIMSIZ DENETİM — sıfır bağlamlı ajana yapıştırılacak metin

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
kıyas tabanıdır. Bu araç, o karşılaştırmanın ölçüm ortamıdır.

---

# 🔴🔴 BU DENETİMİN SORUSU TEKTİR VE ÖNCEKİLERDEN FARKLIDIR

| # | Önceki denetimlerin sorusu |
|---|---|
| 1–5 | *"Bu kodda ne bozuk?"* |
| 6 | *"Faz 0 OLMASI GEREKEN şey oldu mu?"* |
| 7 | *(tasarlandı, **koşulmadı** — `denetim/AILE0-DENETIM-7-PROMPTU.md`)* |

**Seninki bunlardan başka:**

> ## 🔴 B0, ÖLÇÜTLERİNİ **ÖLÇTÜĞÜ ŞEYİ GEÇİRECEK BİÇİMDE** Mİ SEÇTİ?

**Neden bu soru.** 1–2 Eylül'de koşan "B0" oturumu sıradan bir kod işi
yapmadı. Projenin **kendi ilan ettiği dört geçerlilik şartını** ilk kez
ölçtü — ve ölçerken üç şeyi **kendisi seçti**:

1. Şartın geçip geçmediğini söyleyen **istatistiksel ölçütü**,
2. Bir şartın **reçetesinin yanlış olduğu** sonucunu *(ve `06`yı buna göre
   değiştirdi)*,
3. Kendi kodunu sınayan **16 mutasyonu**.

🔴 **Üçünü de aynı ajan seçti, uyguladı ve "geçti" dedi.** Bu depoda bir
ölçütün onu seçen tarafından uygulandığı her durumda bağımsız bir göz
bulgu çıkardı. Senin işin o bulguyu bulmak.

⚠️ **Bu bir "kod hatası ara" görevi DEĞİL.** Kod büyük olasılıkla
çalışıyor — 462 test geçiyor. Aradığın şey, **çalışan kodun yanlış soruyu
cevaplaması.**

---

# ENVANTER — 2 Eylül 2026, koşturularak ölçüldü

| Büyüklük | Değer |
|---|---|
| Test | **462** *(hepsi geçiyor · 1 721 sn · `PYTEST_EXIT=0`)* |
| 🔴 Paket süresi bandı | **869 – 1 851 sn** — **2,10 KAT**, aynı kod |
| Kapı | 🔴 **13/13 ama BAYAT** *(27 Ağu, hash `89587a19…`)* |
| **Bugünkü `kaynak_hash`** | **`0a1a94e5fb24f01605fcf3168519520c`** |
| `sonuc()` şeması | **77 metrik + 47 konfig + korunum** |
| Hedefli mutasyon | **35** · kör havuz **255** |
| Karar kaydı | **86** *(K-001…K-086)* · ölçüm taşıyıp üreticisiz **27** |
| Kapsam maddesi | **33** |
| Kalıcı kural | **Y1–Y14** |
| Satır | `sim` **4 519** *(15 dosya)* · `tests` **9 945** *(19)* · `dogrulama` **7 329** *(31)* |
| `v2/04-NEDEN-BOYLE.md` | **8 547 satır** |
| `aile0_audit.md` | **8 602 satır**, ALTI denetim |

```
README.md          harita — BURADAN BAŞLA
aile0_audit.md     ALTI denetim raporu — DEĞİŞTİRİLMEZ
v2/                belgeler 00–13
denetim/           bu prompt ve öncekiler
ciktilar/          araç çıktıları + politika · sonuclar/ (JSONL)
sim/ tests/ dogrulama/
```

**Kat 4 (yönlendirme) YOKTUR** — sıradaki işin (B1) konusu.

---

# 🔴🔴 B0 NE YAPTI — ve bunu HİÇ KİMSE DENETLEMEDİ

| ne | miktar |
|---|---|
| Kapatılan açık kalem | **4** *(D-13 · `06` koşul 2 · koşul 3 · F-4)* |
| Denetlenen | **1** *(A-14)* |
| Kendi bulduğu yeni bulgu | **4** *(F-5 … F-8)* |
| Yeni `dogrulama/` aracı | **5** |
| Yeni test dosyası | **2** · eklenen test **+33** |
| Değişen `sim/` dosyası | **2** *(`karsilastirma.py` · `kosucu.py` yorumu)* |
| Yeniden ölçülen mühür-bekleyen sayı | **3 küme** *(`08` md 25 · md 31 · Ç4)* |
| Değişen belge | **9** |
| Karar kaydı | **1** *(K-086)* |

🔴 **VE HEPSİNİ AYNI AJAN DOĞRULADI.** Önceki altı denetimin her biri tam
olarak bu durumda bulgu çıkardı ve **beş kez** kapanmış sayılan bir kapıyı
yeniden açtı.

## B0 kendi işinde **iki** hata buldu — sen üçüncüyü ara

| # | Hata | Sınıf |
|---|---|---|
| 1 | `Pool` kullanan bir betiği `if __name__ == "__main__":` **olmadan** stdin'den koşturdu; Windows `spawn` altında havuz asıldı, üç süreç arkada kaldı | devir teslim §6.2'nin **birebir uyardığı** hata |
| 2 | İki kez, **kendi yazdığı açıklama satırındaki** bir dizgiyi *"eski kod kaldı"* sanan `assert` yazdı — doğrulama yanlış yerden düştü | metin ≠ kod *(`03` B5)* |

⚖️ **Örüntü — ve bu senin av haritan:** B0'ın hataları *"ölçütü yanlış
yerden okumak"* sınıfında. Aradığın bulgu büyük olasılıkla **aynı sınıfta**:
doğru görünen bir ölçüt, yanlış nesneye uygulanmış.

---

# 🔴 BÖLÜM A — EN YÜKSEK DEĞERLİ HEDEF: **ÖLÇÜTÜ KİM SEÇTİ**

`06` Bölüm 9 koşul 1: *"Sonuç koşu uzunluğundan bağımsız."* Bu şart bugüne
kadar **eşiksizdi** — `10` §7b.3 yalnızca *"15/30 🟢"* ve *"8/30 🔴"*
yazmıştı. B0 bir ölçüt ilan etti *(`06` §9.1)*:

> Bir kol geçer ⇔ 200 s ↔ 350 s eşleştirilmiş farkının **çift yönlü kesin
> işaret testi** *(binom, α = 0,05; sıfır farklar dışlanır)* reddetmezse.
> Ayrıca **dışlanan etki büyüklüğü** yazılır: medyan farkın dağılımdan
> bağımsız %95 GA'sı, tohumlar arası std'nin katı cinsinden.

B0'ın savunması: *"ölçüt eski yargıları BİREBİR üretiyor, yani geriye
dönük bir gevşetme değil."*

## 🔴 SALDIRI HATLARI

| # | soru |
|---|---|
| **A1** | 🔴 **En kritik:** ölçütün **yalnızca işaret testine** bağlanması, **büyüklüğü** serbest bırakıyor. Sistematik OLMAYAN ama **BÜYÜK** bir koşu uzunluğu etkisi *(ör. 15/30 işaret, ama medyan fark tohumlar arası std'nin 2 katı)* bu ölçütten **GEÇER**. Böyle bir vaka üret ve göster. Geçiyorsa, ölçüt *"koşu uzunluğundan bağımsız"* şartını **karşılamıyor** demektir |
| **A2** | *"Dışlanan etki büyüklüğü yazılır"* diyor ama **hiçbir geç/kal kararı ona bağlı değil.** Raporlanan ama karar vermeyen bir büyüklük, `03` kural 3'ün gevşetilmiş hâli mi? |
| **A3** | α = 0,05 nereden geldi? Ölçümden mü, gelenekten mi? Başka bir α'da hangi yargılar değişir — ölç |
| **A4** | Beraberlikler dışlanıp n düşürülüyor. `en_kisa_yol`/S2/teslim'de n **28**'e düşmüş *(2 beraberlik)*. Bu, testi **gevşetiyor mu sıkıştırıyor mu**? Ölç |
| **A5** | Ölçüt *"rapora giren kollar için bağlayıcı"* diye daraltıldı ve gerekçesi `06` Bölüm 9'un *"hiçbir SONUÇ raporlanmaz"* cümlesi. 🔴 Bu okuma, düşen iki çiftin **ikisini de** bağlayıcılıktan çıkarıyor mu? Çıkarıyorsa şart fiilen boşalmış olur |
| **A6** | 🔴 **Yeni düşen çift:** `en_kisa_yol`/**S0**/gecikme ortalaması *(22/30, p = 0,0161)*. B0 bunu *"ısınma yetersiz olabilir"* diye yorumladı ama **sebebi ölçmedi** *(`03` B4: bir kusuru ölçmek onu SEBEP yapmaz)*. Sebebi sen ölç: ısınma mı, boşaltma mı, kuyruk mu? |

---

# 🔴 BÖLÜM B — REÇETE DEĞİŞTİRİLDİ: MEŞRU MU?

B0'ın en büyük iddiası şu: `06` §8.1'in *"her gecikme cümlesi **p95 ile**
yazılır"* mührü **yetersizmiş**. Ölçtüğü *(30 tohum, eşleştirilmiş)*:

| okuma | medyan fark | işaret | p |
|---|---|---|---|
| HAM ortalama | −3,98 ms | 12/30 | 0,3616 |
| **HAM p95** | +7,11 ms | 17/30 | **0,5847** |
| ORTAK ortalama | **+5,40 ms** | 25/30 | **0,0003** |
| ORTAK p95 | **+28,15 ms** | 27/30 | **0,0000** |

Sonuç: *"sorun ortalama-yerine-p95 değil, karşılaştırılan KÜME"* — ve
`06` §8.1b yazıldı, üç şey **kodda zorunlu** yapıldı.

## 🔴 SALDIRI HATLARI

| # | soru |
|---|---|
| **B1** | 🔴 `06` bir **ÖN-KAYIT** belgesidir. B0 onu **ölçtükten sonra** değiştirdi. Mühür 20 Ekim'de olduğu için biçimsel olarak meşru — ama **`03` kural 3'ün ruhuna** uygun mu? Değişen şey bir **eşik** mi, bir **yöntem** mi? Cevabın gerekçesini yaz |
| **B2** | Ortak alt küme okuması **kesişim oranına** bağlı. `gurultuden_kacan`da kesişim **%20,7** *(min %5,6)*. Bu kadar dar bir kesişimde ortak alt küme okuması **anlamlı mı**? Alt sınır konmalı mı — ve konmadıysa bu bir boşluk mu? |
| **B3** | Aynı ölçüm `gurultuden_kacan` için **ters** sonuç veriyor *(ORTAK p95 −263 ms, p = 0,0428)*. B0 bunu §8.1b'de **öne çıkarmadı**. Bir kolun tersine gitmesi, *"reçete artık doğru"* iddiasını zayıflatıyor mu? |
| **B4** | 🔴 **Sayılar iki ayrı boru hattından aynı çıktı** deniyor *(`literatur_eksenleri.jsonl` ve `gecerlilik.py`)*. Bu bağımsız bir doğrulama mı, yoksa **aynı 30 koşunun iki kez okunması** mı? İki matrisin gerçekten farklı koşular ürettiğini **ölç** |

---

# 🔴 BÖLÜM C — MUTASYONLARI YAZAN, KODU YAZANDI

B0, `sim/karsilastirma.py` için **16 mutasyon** yazdı, **10'unun**
yakalandığını ölçtü, **6 boşluğu** kapattı ve **6/6** yakalandığını
doğruladı → **16/16**.

🔴 **Ama 16'sını da kodu yazan seçti.** Ve **B0'ın YENİ araçlarının
mutasyon kapsamı SIFIRDIR:**

| yeni araç | ne yapıyor | mutasyonu |
|---|---|---|
| `dogrulama/isaret_testi.py` | 🔴 **bir geçerlilik şartının geçip geçmediğine karar veren p değerini üretiyor** | **YOK** |
| `dogrulama/gecikme.py` | yüzdelik + analiz birimi | **YOK** |
| `dogrulama/gecerlilik.py` | üç koşulu birden ölçüyor | **YOK** |
| `dogrulama/pencere_kapsami.py` | `08` md 31'in üreticisi | **YOK** |
| `dogrulama/li_calisma_noktasi.py` | `08` Ç4'ün üreticisi | **YOK** |

**Senden istenen:** bu beş araca **kendi mutasyonlarını** yaz. Özellikle
`isaret_testi.py` — bir p değeri sessizce yanlış olursa, düşmesi gereken
bir kol **geçmiş** görünür ve kimse fark etmez.

⚠️ **Y8'i uygula:** bozduğun yolun sağlam koşuda **tetiklendiğini ÖNCE
göster**. Tetiklenmeyen bir yolu bozmak hiçbir şey ölçmez.

---

# 🔴 BÖLÜM D — SIKILAŞTIRMANIN BEDELİ ÖLÇÜLMEDİ

B0 `sim/karsilastirma.py`yi **daha katı** yaptı: `ortak_alt_kume` artık
**dört pencere alanı** *(kontrol/veri bayt + airtime)* olmadan çalışmıyor
ve dejenere kontrol payında **tipli hata** fırlatıyor.

| # | soru |
|---|---|
| **D1** | B0 önce **yalnızca ilk satıra** bakmıştı; sonra tamamını ölçtü ve şunu iddia ediyor: `ciktilar/sonuclar/` altında **1 114 satırın 1 114'ü** dört pencere alanını taşıyor, **eksik 0**. 🔴 **Bu iddiayı çürütmeye çalış** — ve dosyaların **iki farklı `kaynak_hash`** taşıdığına dikkat et *(`cd6d304f…` ve `0a1a94e5…`)*: `ortak_alt_kume` farklı hash'li iki satırı **reddediyor**, yani aynı dosyanın satırları birbiriyle karşılaştırılamaz olabilir. Bu bir tuzak mı? |
| **D2** | 🔴 Dejenere kontrol payı artık **tüm karşılaştırmayı** engelliyor — gecikme kısmı dâhil. Ölçüldü: `kontrol_payi.py`de 120 hücrenin **2'si** dejenere. Meşru bir gecikme karşılaştırması bu yüzden **imkânsız** hâle geliyor mu? Bu doğru tasarım mı? |
| **D3** | Yeni zorunlu alanlar **hem A hem B** için kontrol ediliyor mu — yoksa yalnız birinde mi? Kırarak göster |
| **D4** | `kontrol_payi_yuzde` `KarsilastirmaHatasi` fırlatıyor ama `KarsilastirmaHatasi` **ondan SONRA** tanımlanıyor. Çalışıyor, ama bir gün modül bölünürse? Bu bir kırılganlık mı? |

---

# 🔴 BÖLÜM E — D-13'ÜN DÜZELTMESİ **540 KOŞUDA HİÇ SINANMADI**

D-13: kapının Ç1 yolu `Pool` alt süreçlerinde koşuyor ve sonuç satırı
yazmıyordu *(`aile0_kapi_raporu.jsonl` = **0 bayt**)*. B0 düzeltti:
işçiler **tam sonuç sözlüğünü döndürür**, ebeveyn yazar.

🔴 **Ama kanıtı yalnızca 2 ve 20 koşuda.** Kapının gerçek yolu **540 + 20**
koşudur ve `aile0_kapi_raporu.jsonl` **hâlâ 0 bayt**.

| # | soru |
|---|---|
| **E1** | 🔴 **EN CİDDİ RİSK — ÖLÇÜLMEDİ:** işçiler artık **tam sonuç sözlüğünü** döndürüyor; içinde `teslim_kimlikleri` ve `teslim_gecikmeleri_s` **listeleri** var. 540 koşuda bu ne kadar bellek ve ne kadar pickle maliyeti demek? Kapı **165–330 dk** koşuyor ve bu maliyet **sonunda** patlarsa koşu boşa gider. **ÖLÇ** — küçük bir matrisle satır başına bayt maliyetini çıkar ve 540'a ölçekle |
| **E2** | `imap` sıralı yield ediyor; yavaş bir iş sonrakileri **bekletir mi**? Bellekte biriken sonuç sayısı sınırlı mı? |
| **E3** | Havuz boyu `min(CEKIRDEK, len(isler))` yapıldı. Kapının 540 işinde etkisi yok, ama uç durum matrisinde **5 iş → 5 işçi**. Kapı süresi bundan etkilenir mi — ölç |
| **E4** | Üretim yolundaki `assert yazilan == len(isler)` **yalnızca yazıcı aktifken** çalışıyor. Yazıcının aktif olmadığı bir üretim yolu var mı? |

---

# 🔴 BÖLÜM F — YENİDEN ÖLÇÜLEN MÜHÜR-BEKLEYEN SAYILAR

B0 üç sayı kümesini yeniden ölçtü. **Üçünü de doğrula.**

| # | sayı | B0'ın iddiası |
|---|---|---|
| **F1** | `08` md 25 · kontrol payı | eski **8,3–17,8 kat** *(3 tohum)* → yeni **4,0–38,0 kat** bayt · **2,6–18,9** airtime *(30 tohum, pencereden)* |
| **F2** | `08` md 31 · pencere dışı pay | **%18,17–22,86** *(beyan %17,63–22,84 ile uyumlu)* |
| **F3** | `08` md 31 · **çarpıklık** | 🔴 **YENİDEN ÜRETİLEMEDİ.** B0 iddia ediyor ki ilan edilen 1,004–1,079 bir *tüm koşu/pencere* oranı **OLAMAZ**, çünkü o oran analitik olarak **[1,1852 · 1,2963]** bandına hapistir |
| **F4** | `08` Ç4 · Li @2 Mbit/s | **1,761 / 0,277 Mbps · 1/6,36 · GA %1,54** — dördü de birebir |

| # | soru |
|---|---|
| **F5** | 🔴 F1'de **aynı kollar** mı karşılaştırılıyor? Eski ölçüm `mesafe_vektoru` *(DV)* vs `gurultuden_kacan`. Yeni ölçüm de öyle mi — yoksa kol tanımı değişti mi? |
| **F6** | 🔴 F3'ün analitik bandı türetmesini **kendin yeniden türet**. Doğruysa, ilan edilmiş bir sayının **imkânsız** olduğu gösterilmiş olur ki bu ciddi bir bulgudur. Yanlışsa, B0 bir sayıyı haksız yere çürütmüştür |
| **F7** | B0, kayıp üreticinin matrisini **yeniden ilan etti** *(5 kol × 2 senaryo × 3 trafik)*. Bu, sayıyı tutturmak için seçilmiş bir matris mi? Başka matrislerde pay bandı ne çıkıyor — ölç |
| **F8** | `08`in *"229 mutant hiç sınanmadı"* satırı **bayat**: kör havuz bugün **255**. Doğrula ve `08`e ne yazılması gerektiğini söyle |

---

# 🔍 ŞÜPHE LİSTESİ — bu denetime özel

| # | şüphe |
|---|---|
| 1 | `tests/test_gecikme.py` yüzdelik tanımının **bir kopyasını** taşıyor *("çapa" diye gerekçelendirilmiş)*. Bu B-07'nin *"ikinci doğru kaynağı"* tuzağı mı, yoksa meşru bir regresyon çapası mı? |
| 2 | `dogrulama/gecikme.py`, `yuzdelik`i `sim/karsilastirma.py`den **içe aktarıyor**. `dogrulama → sim` yönü doğru, ama bir **döngüsel içe aktarım** riski doğdu mu? |
| 3 | `kayit(dosya=...)` parametresi **testler için** eklendi. Üretim yolu bunu kazara kullanabilir mi? Bir koruma var mı? |
| 4 | `12` §2.1 B0'ın **doğrulama ölçütlerini** listeliyor. Altısını **tek tek** karşıla: ölçüt gerçekten sağlandı mı, yoksa yeniden mi yazıldı? |
| 5 | B0, `06` §8.1'in eski tablosunu **silmedi**, yanına §8.1b ekledi. İki tablo **çelişiyor** mu — ve bir okuyucu hangisinin geçerli olduğunu anlayabilir mi? |
| 6 | `ciktilar/sonuclar/pencere_kapsami.jsonl` **90 satır** taşıyor ama tek koşu **30** satır yazıyor *(dosya append modunda)* — yani **üç koşu** birikmiş ve ikisi **eski hash'ten**. `gecerlilik.jsonl` **480** *(2 koşu)*, `kontrol_payi.jsonl` **240** *(2 koşu)*. 🔴 Bir analiz bu dosyaları **tek koşu sanarsa** ne olur? Ayırt eden bir mekanizma var mı, yoksa okuyanın sorumluluğunda mı — ve bu yazılı mı? |
| 7 | K-086 *"sekiz kalem → üç"* diyor. Üçünün ikisi *"beyanlı kapalı"*. **Beyan yeterli mi**, yoksa iş mi kaldı? |
| 8 | B0 `sim/`e dokundu ve kapı bayatladı. `12` §2.3 kapıyı B1'den sonraya erteliyor. 🔴 **Bu erteleme, B0'ın hiçbir değişikliğinin kapı kriterlerini etkilemediği varsayımına dayanıyor. Bu varsayım ÖLÇÜLDÜ mü?** |

---

# ÇALIŞMA BİÇİMİN

1. **Önce oku, sonra koştur, en son yorumla.** Sıra: kök `README.md` →
   `v2/03-YONTEM-KURALLARI.md` *(15 kural — **denetimin ölçütü budur**)* →
   `v2/04-NEDEN-BOYLE.md`nin sonundaki **Y1–Y14** → **K-086** *(B0'ın kendi
   kaydı)* → `v2/13-AILE0-KAPANIS-KANITI.md` → `v2/06-ON-KAYIT.md` §8.1b
   ve §9.1.
2. 🔴 **Okuduğun bir dosyayı SONUNA KADAR oku.** Bu depoda bir ajan
   5 271 satırlık bir taramanın **%62'sini** okuyup tamamını okuduğunu
   yazdı ve **beş bulgu** o eksikte saklıydı *(K-080)*. Parça okuduysan
   **hangi satır aralığını okumadığını YAZ.**
3. Her bulgunun yanında **üretici komut** *(depo kökünden koşabilir)* ve
   **kaynak dosya:satır**.
4. Bir iddiayı doğrularken **iddianın kendi ölçütünü kullanma.**
5. ⭐ **Y6** — beklenenden iyi çıkan sonuç, kötü çıkan kadar şüphelidir.
   **Kendi lehine çıkan sonuca da uygula.**
6. ⭐ **Y8** *(bozulan yolun tetiklendiğini ÖNCE göster)* · **Y10**
   *(bir yaklaşık-eşitlik iddiası KIRILABİLİR olmalı)* · **Y11**
   *(korumayı kapsamı DIŞINDAKİ vakayla sına)* · **Y14** *(bir kod
   düzeltmesi ondan önce ölçülmüş her sayıyı şüpheli yapar)*.
7. 🔴 **Bir korumanın BEYANINI değil ETKİSİNİ ölç.** Bu deponun en sık
   tekrarlanan hatası budur — **dört kez**.
8. 🔴 **İki durumu karşılaştıracaksan İÇ İÇE koştur.** Ardışık ölçüm bu
   depoda *"+819 sn"* dedi; iç içe ölçümde gerçek fark **+45 sn** çıktı.
9. 🔴 **Yayımladığın her üretici komutu, yayımlamadan önce OLDUĞU GİBİ
   koştur.**
10. Deneme için depoyu geçici bir dizine kopyala; **aslını değiştirme.**

---

# ORTAM VE KISITLAR

| | |
|---|---|
| Platform | Windows 11 · Python 3.11 · numpy, scipy, pytest kurulu |
| Dil | Kod ve belgeler **Türkçe**. Raporunu da Türkçe yaz |
| ⚠️ Konsol | **`PYTHONIOENCODING=utf-8`** — varsayılan cp1254 Türkçe karakterde çöküyor. Hata **terminalin**, kodun değil |
| 🔴 Paralellik | Windows'ta `spawn`: `Pool` açan her betikte `if __name__ == "__main__":` **ZORUNLU**. 🔴 **stdin'den (`python -`) koşan bir betikte bu İMKÂNSIZDIR** — B0 tam olarak bunu denedi ve havuz asıldı. `Pool` kullanan her ölçümü **bir dosyaya yaz, öyle koştur** |
| 🔴 Boru hattı | `pytest ... \| tail` **`tail`in** çıkış kodunu döndürür. `${PIPESTATUS[0]}` kullan **ve çıktıyı OKU** |
| 🔴 Git | **Hiçbir git komutu çalıştırma — `status` dâhil** |
| 🔴 Kod | **Depodaki hiçbir dosyayı DEĞİŞTİRME.** Deneme için `tempfile.mkdtemp` kopyası |
| 🔴 Tohum | **2000–2029 HİÇBİR AMAÇLA koşulmaz.** Ayarlama/kapı: **1–30** |
| İşlemci | En fazla **10 çekirdek.** 30 dk'yı aşacak koşudan **önce** süre tahminini yazdır ve **SOR** |
| Yazacağın tek dosya | `aile0_audit.md` |

### ⏱️ Ölçülmüş süreler — 1–2 Eylül, 10 çekirdek

| Komut | Süre |
|---|---|
| `python -m pytest tests -q` | **1 721 sn** *(bant 869–1 851)* |
| `python -m pytest tests/test_kapi_secimleri.py -q` | **24 sn** ⭐ *(65 test)* |
| `python -m pytest tests/test_karsilastirma.py -q` | **127–490 sn** *(**40** test — B0 öncesi 29)* |
| `python dogrulama/gecerlilik.py` | **3,3 dk** *(240 tam koşu)* |
| `python dogrulama/kontrol_payi.py` | 🔴 **13,7 dk** *(120 tam koşu — belgede "~3 dk" yazıyordu, BAYAT)* |
| `python dogrulama/pencere_kapsami.py` | **43 sn** *(30 tam koşu)* |
| `python dogrulama/li_calisma_noktasi.py` | **~10 sn** |
| `python dogrulama/karar_kaydi_denetimi.py` | ~2 sn ⭐ |
| `python dogrulama/kayit_indeksi.py --kontrol` | ~2 sn ⭐ |
| `python dogrulama/aile0_kapi_raporu.py` | 🔴 **165–330 dk · İZİN GEREKİR** |

⚠️ Süre tahmini bu depoda **beş kez** tutmadı. Kendi tahminini **ölçtüğün
en büyük** süreden kur.

---

# ÇIKTI: `aile0_audit.md`

Dosya **altı denetimin raporunu** taşıyor. 🔴 **İçeriğini SİLME,
DEĞİŞTİRME.** Sonuna `# B0 DENETİMİ — <tarih>` bölümü ekle.
🔴 Bulgu numaraları **B-120**'den devam eder.

```
## 0. YÖNETİCİ ÖZETİ
    🔴 B0 ÖLÇÜTLERİNİ KENDİ LEHİNE Mİ SEÇTİ: EVET / HAYIR / KISMEN
    🔴 Bulduğun EN CİDDİ tek şey — ilk paragrafta
    🔴 B1'e (Kat 4) geçilebilir mi

## 1. 🔴 ÖLÇÜT SEÇİMİ — Bölüm A'nın altı sorusu
## 2. 🔴 REÇETE DEĞİŞİKLİĞİ — Bölüm B'nin dört sorusu
## 3. 🔴 YENİ ARAÇLARIN MUTASYON KAPSAMI — Bölüm C
    Beş araç için KENDİ mutasyonların. Her biri: Y8 tetiklenme (ÖNCE) ·
    462 testten sağ çıktı mı · sağ kaldıysa davranış değişiyor mu
    🔴 ARAÇ BAZINDA: oran · %95 GA · ULAŞILAN GÜÇ
## 4. SIKILAŞTIRMANIN BEDELİ — Bölüm D
## 5. 🔴 D-13'ÜN 540 KOŞUDAKİ BELLEK MALİYETİ — Bölüm E1 (ÖLÇÜM ZORUNLU)
## 6. YENİDEN ÖLÇÜLEN SAYILAR — Bölüm F'nin dört kümesi
## 7. YENİ BULGULAR (B-120'den)
## 8. B0'IN DÖRT KAPANIŞI — bağımsız doğrulama
    D-13 · koşul 2 · koşul 3 · F-4: her biri gerçekten kapandı mı
## 9. DOĞRULANAN İDDİALAR   ## 10. ÜRETİLEMEYEN İDDİALAR
## 11. KAPSAM BEYANINA EKLENECEKLER
## 12. 🔴 ANLAŞILMAYANLAR
    🔴 BOŞ BIRAKILAMAZ. Altı denetimde de buradan GERÇEK KUSUR çıktı.
    Numaralar A-17'den devam eder.
## 13. 🔴 SENİN YARGIN — tek cümleyle başlar:
    "B0'ın kapattığı dört kaleme GÜVENİLİR / GÜVENİLMEZ, çünkü…"
## 14. KOŞTURDUĞUN KOMUTLAR
## 15. 🔴 OKUMA KAPSAMIN — hangi dosyanın hangi satır aralığını OKUMADIN
```

**Son satır:** hiçbir dosyanın değiştirilmediğini ve hiçbir git komutunun
çalıştırılmadığını **açıkça yaz.**

---

# 🔴 SON SÖZ

Altı denetim, altı kez bulgu: **20 → 17 → 24 → 13 → 20 → 18.**
Örüntü **altı kez** kapanmadı.

B0 dört kalem kapattı ve dört yeni bulgu çıkardı — ama **kendi işini kendi
doğruladı.** Bu depoda o durum **her seferinde** bulgu üretti.

Ve şunu bil: **bu denetimden sonra B1 başlıyor** — simülatörün Kat 4
altyapısı kurulacak ve **şema SON KEZ donacak.** B0'ın ölçütlerinde
bulmadığın her kusur, o şemaya ve ondan sonra üretilecek **her sayıya**
taşınacak.

> **Bulacağın her şey, bulunmadığı takdirde jürinin bulacağı bir şeydir.**

Hiçbir şey bulamazsan bunu da yaz — ama **hiçbir şey bulamamak, aradığın
yerlerin listesiyle ve ulaştığın güçle birlikte anlamlıdır.**

**Bir şeyi büyütmek istiyorsan önce ölç.**
