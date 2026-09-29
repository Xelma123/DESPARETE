# AİLE 0 · BEŞİNCİ BAĞIMSIZ DENETİM — sıfır bağlamlı ajana yapıştırılacak metin

> Aşağıdaki `---` çizgisinden sonraki metnin **tamamını**, sıfır bağlamlı
> yeni bir ajan oturumuna **ilk mesaj** olarak yapıştır.
>
> *Yazıldığı tarih: 25 Ağustos 2026. Taşıdığı her sayı o gün koşturularak
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

# 🔴 BU BEŞİNCİ DENETİM

| Tarih | Denetim | Bulgu | Sağ kalan |
|---|---|---|---|
| 19 Ağu | **Birinci** | 20 *(+3 kapatırken)* | 8/10 = %80,0 |
| 20 Ağu | **İkinci** | 17 | 7/10 = %70,0 |
| 20 Ağu | **Üçüncü** | 24 *(1'i çürütüldü)* | 10/15 = %66,7 |
| 25 Ağu | **Dördüncü** | 13 | **6/24 = %25,0** |

**Toplam 76 bulgu · 75'i kapatıldı · 1'i ölçümle çürütüldü** *(B-58)*.

## 🔴 SENİN ASIL HEDEFİN — dört denetimde de aynı

> **Dördüncü denetimin 13 bulgusunun 13'ünü de yine AYNI ajan kapattı ve
> yine kendi düzeltmesini kendi doğruladı.**

Ve o ajanın sicili şudur: **dördüncü denetimin iki KRİTİK bulgusu da onun
kendi düzeltmelerine çıktı** — B-45'i düzeltirken yazdığı kapı *(B-65)* ve
açtığı protokol→çerçeve kanalı *(B-66)*. Üçüncüsü onun A-4 beyanı *(B-69)*,
dördüncüsü B-49'un test yolu *(B-68)*, beşincisi B-43'ün işaretleyicisi
*(B-76)*.

> ⚠️ `aile0_audit.md` **dört denetim raporunu da** taşıyor *(4 812 satır)*.
> Haritası kök `README.md`de. Dördünü de oku — ama **otorite** olarak değil,
> **denetlenmesi gereken iddialar** olarak. Şimdiye kadar denetim
> raporlarında **üç hata** bulundu *(B-58 çürütüldü · B-54'ün formülü
> tutmadı · üçüncü denetimin üretici komutları yeniden üretilemedi)*.

---

# 🔴 SENDEN İSTENEN TEK KRİTİK ÖLÇÜM — bu kez KATMANLI

Dördüncü denetim oranı **%25,0**'e düşürdü ve H0 *(p = 0,70)* **reddedildi**
*(n = 24, tek yönlü p = 7×10⁻⁶, güç 0,886)*. Buna rağmen denetçi *"örüntü
kapandı"* **demedi** — *"daraldı"* dedi, ve gerekçesini kendi lehine olan
sonucun üzerine uyguladı *(Y6)*:

| katman | sağ kalan | oran | %95 GA | H0: p = 0,70 |
|---|---|---|---|---|
| **sayaç / raporlama** | 5/11 | **%45,5** | [0,167 · 0,766] | 🔴 **REDDEDİLEMEDİ** *(p = 0,078)* |
| mekanizma | 1/11 | %9,1 | [0,002 · 0,413] | reddedildi *(p = 0,00005)* |
| doğrulama aracı | 0/2 | %0,0 | — | — |

Ve iki **yanlılık** kendisi tarafından yazıldı:

1. Önceki üç denetimin 10 sağ kalanının **8'i** sayaç katmanındaydı — genel
   orandaki düşüşün büyük kısmı **örneklem karışımının değişmesinden** geliyor.
2. 🔴 **`sim/kosucu.py`ye HİÇ mutasyon konmadı.** Üçüncü denetimin 15'inin
   **7'si** oradaydı ve **4'ü sağ kalmıştı** *(%57)*.

> 🔴 **Korumasız kalan yüzey mekanizma değil, SONUÇ ŞEMASIDIR** — ve o yüzey
> Aile 1'in ölçtüğü şeydir.

## 🔒 BAĞLAYICI ŞARTLAR — güç analizi ÖNCEDEN yapıldı

**Tek örneklem binom · tek yönlü · α = 0,05 · TAM binom · H0: p = 0,70**

| n | red bölgesi | güç *(p₁ = 0,40)* | güç *(p₁ = 0,50)* |
|---|---|---|---|
| **11** *(4. denetimin sayaç katmanı)* | X ≤ 4 | **0,533** | 0,274 |
| 15 | X ≤ 6 | 0,610 | 0,304 |
| **19** | X ≤ 9 | **0,814** | 0,500 |
| 24 | X ≤ 12 | 0,886 | 0,581 |
| 30 | X ≤ 16 | 0,952 | 0,708 |

🔴 **Sayaç katmanı n = 11'de güç yalnızca 0,533'tü** — H0'ın reddedilememesi
bir sonuç değil, **yetersiz güç** olabilir. Ayırt edilemez.

**Bu denetimin şartları:**

| # | Şart |
|---|---|
| 1 | 🔴 **SAYAÇ / RAPORLAMA katmanında en az 19 mutasyon** *(güç 0,814)*. Bu katman **hedefin kendisidir** |
| 2 | **MEKANİZMA katmanında en az 8 mutasyon** — dördüncü denetimin %9,1'i bağımsız bir örneklemle sınanmalı |
| 3 | 🔴 **`sim/kosucu.py`ye en az 5 mutasyon.** Dördüncü denetimin **kendi beyan ettiği kör noktası**; üçüncü denetimde orada oran %57'ydi |
| 4 | **Her katmanın oranını, %95 GA'sını ve ULAŞILAN GÜCÜNÜ ayrı ayrı raporla.** Genel oran tek başına yanıltıcıdır — dördüncü denetim bunu kendi raporunda gösterdi |
| 5 | 🔴 Bir katmanda **n < 19 ise o katman için "kapandı" YAZILAMAZ** |

**Katman tanımı** *(dördüncü denetimin ölçütü)*: mutasyon bir **mekanizmayı**
mı *(fizik · MAC durum makinesi · yönlendirme kararı · zamanlama)* yoksa bir
**sayaç/raporlama alanını** mı *(sonuç sözlüğüne giren büyüklükler · gözlem
penceresi alanları · kapı ölçütleri)* bozuyor?

⏱️ **Bütçe:** ~32 mutasyon × tam paket *(13,8 dk)* = 442 dk ardışık;
**5 paralel ile ~85–100 dk.** Dördüncü denetçi 24 mutasyonu 58 dk'da
koşturdu *(324 test tabanıyla; bugün 367)*.

🔴 **Y8 ön koşulu:** her mutasyon için bozduğu yolun **sağlam koşuda
tetiklendiğini ÖNCE göster.**
🔴 Sağ kalanların davranışı **ayrıca ölçülür**; *"eşdeğer"* ile
*"tüketicisiz"* aynı çıktıyı verir ve **ikincisi asıl bulgudur.**

---

# 🔴 AV SAHASI — bu depoda FİİLEN gerçekleşmiş hata sınıfları

| # | Ne oldu | Sınıf |
|---|---|---|
| 1 | *"Ne koştuğunu kendisi doğrula"* kuralı **yedi kez** ihlal edildi | **Y7** |
| 2 | Bir koruma **hiçbir şey doğrulamıyordu**; tek testi korumanın yakalayabildiği tek durumu kullanıyordu | **Y11** |
| 3 | K-044 bir düzeltmeyi **ilan etti, koda girmedi** ve iddia iki oturum kayıtta doğru göründü | **kural 15** |
| 4 | Bir ön-kayıtlı kapı **iki kez** yanlış şey ölçtü: önce **geometri** *(B-45)*, sonra **kalıcılık** *(B-65)* — ikincisi **tek tohumda** kalibre edilmişti | **kural 2** |
| 5 | Açılan bir bilgi kanalının bedeli **tipe** bağlıydı: 10 bayt bedelle **1 236 bayt** taşındı *(B-66)* | **`05` §A2** |
| 6 | Bir mutasyon, bozduğunu iddia ettiği şeyi **bozmuyordu** ve *"sağ kaldı"* diye raporlanacaktı | **Y8** |
| 7 | Bir test **yanlış değişmez** tarafından geçiriliyordu *(`nan >= 0` zaten `False`)* | **Y11** |
| 8 | Bir kaynak denetimi **kendi docstring'ini** yakalayıp kırıldı | **`03` B5** |
| 9 | Bir işaretleyici, gövdesinde adı **hiç geçmeyen** bir teste iliştirilmişti | **`03` B5** |

🔴 **Bu dokuz sınıfın hiçbiri kapandığı ÖLÇÜLMÜŞ değildir.**

---

# 🔴 EN AZ DENETLENMİŞ KOD — 25 Ağustos'ta yazıldı

Dördüncü denetimin 13 bulgusunu kapatan ajan **15 yeni koruma** yazdı ve
şemaya iki alan ekledi. Hepsinin mutasyonla sınandığı iddia ediliyor
*(15/15)*. **Bunu doğrula.**

| Ne | Nerede | Neden şüpheli |
|---|---|---|
| **Eşleştirilmiş ablasyon kapısı** | `dogrulama/aktaricilar.py::kalite_ablasyonu` · `tests/test_mekanizma_kapisi.py::test_b65_*` | 🔴 **ÖN-KAYITLI KAPININ ÜÇÜNCÜ HÂLİ.** İlk ikisi yanlış şey ölçtü. Ablasyon permütasyonu `hash(anahtar)` ile tohumlanıyor — `PYTHONHASHSEED` bağımsız mı? *(Ç2'yi kırar mı?)* |
| **Yük bedeli** | `sim/gozlem.py::yuk_bayt` · `_tasinan_bilgi_bayt` | İki hesap **ayrı** yazıldı ki biri bozulunca diğeri konuşsun. **Üçüncü bir kaçak ekseni var mı?** *(float? demet derinliği? Unicode?)* |
| **Satır içi dört değişmez** | `sim/karsilastirma.py` | Dördüncü eksen. **Beşinci var mı?** |
| **Teşhis kancası** | `sim/kosucu.py::_protokol_teshislerini_topla` | Yeni bir yazma yolu. Slota **keyfi anahtar** yazılabiliyor mu? Sızıntı kapısı mı? |
| **Alıcı bayt kredisi** | `sim/mac.py` *(`il.bayt or ...`)* | `or` kısa devresi: `bayt=0` olan bir çerçeve sessizce `beacon_bayt` alır. Bu bir kaçak mı? |
| **Nöbetçi nesnesi** | `dogrulama/kurulum_kalibrasyonu.py` | Dördüncü yol var mı? |
| **Kapanış hücresi taraması** | `tests/test_gozlem.py::_paylasilan_mutable` | Yalnızca `dict/list/set` sayıyor. **Paylaşılabilir başka yazılabilir tip?** *(`bytearray`, örnek özniteliği, sınıf değişkeni)* |
| **`assert` ile değişmez** | `sim/mac.py` *(B-72)* | `python -O` ile `assert`ler **silinir**. Bu bir koruma mı, yoksa varsayım mı? |
| 🔴 **Zaman aşımı bütçesi** | `dogrulama/mutasyon_paketi.py` · `tests/test_kapi_secimleri.py::test_b78_*` | **DÜNKÜ kod.** Çekişme çarpanı 1,60 bir **ALT SINIR** — üst sınır ölçülmedi. Koruma paket büyümesini oranla yakalıyor, ama **ölçüm çiftinin kendisi elle tutuluyor**: biri güncellenip diğeri ölçülmezse sessizce boşalır |
| 🔴 **Sebep üreticileri** | `mutasyon_paketi.py::zaman_asimi_sebebi` · `desen_tutmadi_sebebi` · `gecersiz_sebebi` | **DÜNKÜ kod.** İlk yazımda iki mutasyon sağ kaldı *(M-C6, M-C7)*. Dördüncü bir sebep türü eklenirse ayırt ediliyor mu? |

---

# DENETLENECEK İDDİALAR

## A · Kapı raporu — AYNI GÜN ÖNCE DÜŞTÜ, SONRA GEÇTİ

**25 Ağustos 2026 · beşinci koşu · 150,2 dk · RC=0**

```
OK Ç1.3  mutasyon paketi (her mutasyon KENDİ testiyle)   35/35   35/35
OK AİLE 0 KAPANMAYA HAZIR — 13/13 kriter geçti.
```

🔴 **Ama aynı gün, aynı 35 mutasyonla, kapı ÖNCE DÜŞTÜ:**

| | düşen koşu | geçen koşu |
|---|---|---|
| mutant `timeout` | 1200 sn | **3600 sn** |
| Ç1.3 | **4/35** | **35/35** |
| süre | 127,8 dk | 150,2 dk |

Sebep: paket 324→354 teste büyümüştü, zaman aşımı sabiti **1200 sn'de
kalmıştı**, `Pool(8)` altında mutant başına süre 18,5–20+ dk'ya çıkmıştı ve
**31 mutant zaman aşımına uğradı.**

🔴 **VE KAPI DÜŞME SEBEBİNİ YANLIŞ RAPORLADI.** 31 mutant için *"mutasyon
uygulanamadı"* yazdı — bu, **desenin kaynakta bulunamadığı** iddiasıdır.
Desen üç ayrı ölçümde **35/35 tuttu.** Etiket, aracın hiç yapmadığı bir
teşhisti *(Y7)*. Ayrıntı: **K-058**, kapanış: **K-059**.

### 🔴 SENİN İŞİN — kapanış sayısını değil, ONA GİDEN YOLU denetle

1. **13/13'ü doğrula ama sayıya güvenme.** Bu depoda bir kapı, düşme
   sebebini **yanlış söyledi**. Aynı kapı geçtiğinde **doğru sebeple**
   geçtiğini ne gösteriyor?
2. **Y13 — düzeltmelerin KODDA olduğunu göster.** K-044'te bir düzeltme
   ilan edildi ve koda hiç girmemişti *(B-41)*.
3. **13 yeni koruma gerçekten koruyor mu** *(`test_b78_*` · `test_b79_*`)*?
   Mutasyonu biraz değiştir — test hâlâ kırılıyor mu?
4. 🔴 **Zaman aşımının YENİ değeri de yeterli mi?** Ölçüm çifti yazılı:
   **367 test / 828,3 sn**, çekişme **1,60**, emniyet **1,50**, sabit
   **3600 sn** *(marj 1,81×)*. Çekişme çarpanı bir **ALT SINIRDIR** —
   8 yollu koşuda **biten TEK mutant** ölçüldü *(1,46×)*; diğer 7'sinin
   gerçek süresi **hiç ölçülmedi**. Üst sınır bilinmiyor. **Bu bir bulgu mu?**
5. 🔴 **Ölçüm çifti elle tutuluyor.** `PAKET_TEST_SAYISI` ve
   `PAKET_SURESI_S` birlikte ölçülmezse koruma **sessizce boşalır** ve
   hiçbir test bunu göremez. Kodda uyarı yazılı — **uyarı bir koruma mıdır?**

Kapıyı kendin koşmak istersen **~150 dk** sürer — koşmadan önce **SOR**.
Ucuz ön kontroller *(~35 sn)*:

```bash
python dogrulama/mutasyon_on_kontrol.py
```
```bash
python -m pytest tests/test_kapi_secimleri.py -q
```

⚠️ *"Ön kontrol geçti, kapı düştü"* vakası **ÜÇ kez** yaşandı
*(K-042, K-046, K-058)*. Sonuncusunda ön kontrol **35/35** dedi, kapı aynı
gün **4/35** ile düştü — ön kontrol o ekseni **yapısal olarak göremiyordu**.

## B · 75 bulgunun kapandığı iddiası

`04-NEDEN-BOYLE.md` **K-056** dördüncü denetimin her bulgusunun nasıl
kapandığını yazıyor. 🔴 **En az 8'ini seç ve kapandığını KENDİN doğrula** —
ve testi **mutasyonu biraz değiştirerek** sına: fazla dar bir test yalnızca
denetçinin yazdığı tek mutasyonu yakalar.

Öncelikli: **B-65** *(kapı üçüncü hâlinde gerçekten bilgiyi mi ölçüyor?)* ·
**B-66** · **B-69** · **B-70** · **B-72** · **B-74** *(sayı doğru mu?)* ·
**B-57** *(hâlâ açık — sınırı doğru mu?)*

## C · 25 Ağustos'ta üretilen sayılar

| İddia | Değer |
|---|---|
| Kalıcı ablasyon null'u | **+0,0599 ± 0,0232** *(8 tohum)* |
| Karar-başına ablasyon | −0,0006 ± 0,0015 |
| Eşleştirilmiş fark *(kol − ablasyon)* | **+0,0283 ± 0,0230**, 8/8 pozitif |
| Yük bedeli kaçağı, düzeltmeden sonra | **1,00×** *(önce 20 205×)* |
| Alıcı kredisi | çerçeve boyutuna **eşit** *(42 = 32+10)* |
| Kontrol payı farkı *(B-77)* | DV %14,9–35,6 · gözlem %1,65–1,87 |
| Üretici satırı taşıyan kayıt | **57'nin 20'si**; sayı taşıyıp taşımayan **37** |

**En az beşini yeniden üret.**

---

# 🔍 ŞÜPHE LİSTESİ — bu denetime özel

> Önceki dört listeyi de uygula *(`denetim/` altında)*.

**1 · 🔴 SAYAÇ KATMANI — bu denetimin ASIL HEDEFİ.**
Dördüncü denetimde **%45,5** ve H0 reddedilemedi. Sonuç sözlüğünün **her
alanını** tek tek boz: `teslim_orani` · `ortalama_gecikme_s` ·
`ortanca_gecikme_s` · `kontrol_bayt` · `kontrol_airtime_s` · `veri_bayt` ·
`veri_airtime_s` · `mac_*` sayaçları · `beacon_*` · `ttl_olumu` ·
`donguyle_olen` · `hedef_yok` · `kuyruk_tasmasi` · `islenen_olay` ·
`ortalama_atlama` · `ort_komsu_sayisi` · `yakinsama` · `pencerede_*`.
**Hangileri sabitlenebiliyor ve hiçbir test görmüyor?**

**2 · 🔴 `sim/kosucu.py` — beyan edilmiş kör nokta.**
Dördüncü denetim oraya hiç dokunmadı; üçüncüde oran **%57**'ydi. En az 5
mutasyon.

**3 · Ön-kayıtlı kapı ÜÇÜNCÜ hâlinde — dördüncü kez yanlış olabilir mi?**
İlk hâli geometriyi ölçtü, ikincisi kalıcılığı. Üçüncüsü *"eşleştirilmiş
ablasyon"*. 🔴 **Kendi null'ünü yaz** ve kapının onu da sıfırda tuttuğunu
sına. Ablasyon `hash()` ile tohumlanıyor — `PYTHONHASHSEED=0` ve `=1` ile
sonuçlar aynı mı? *(Ç2 belirlenimcilik kriteri bunu şart koşuyor.)*

**4 · `assert` ile yazılmış değişmezler `python -O` altında SİLİNİR.**
Depoda kaç değişmez `assert`e bağlı? Kapı raporu `-O` ile koşulsa hangileri
susardı? Bu bir **beyan eksikliği** mi?

**5 · Yeni kancaların sızıntı yüzeyi.**
`beacon_yuku` ve `teshis` — protokolün simülatöre bilgi **yazdığı** iki yol.
🔴 Bunlardan geriye bilgi **sızıyor mu?** Bir protokol `teshis` ile yazdığını
sonraki kararda okuyabilir mi?

**6 · Kontrol düzlemi bütçesi *(B-77 / `08` madde 25)*.**
Beyan edildi ama **zorlanmıyor**. Aile 1 bu hâliyle koşarsa karşılaştırma
geçerli olur mu?

**7 · İstatistik katmanı HÂLÂ YOK.**
`grep -rn "wilcoxon\|holm" --include=*.py .` → yalnızca beyan. Ön-kaydın
*"ZORUNLU"* dediği NaN koruması yazılmadı — ama artık `karsilastirma.py`
NaN'ı **reddediyor** *(B-67)*. Bu yeterli mi?

**8 · `08`in 25 maddesi — iki yönlü.**
*(a)* *"Yapmaz"* denen bir şey yapılıyor mu? *(b)* Kodda modellenmemiş ama
listede olmayan? *(Dört denetim sırasıyla 4, 4, 2 ve 1 madde ekletti.)*

**9 · B-57 hâlâ açık.**
57 kaydın 37'si sayı taşıyıp üretici satırı taşımıyor. 🔴 O 37'nin kaçının
sayısı bugün **yeniden üretilebilir?** Üretilemeyen bir sayı `04`te olgu gibi
duruyorsa, bu bir bulgudur.

**10 · Dört denetimin kapanışları birbirini bozdu mu?**
B-45'in düzeltmesi B-65'i doğurdu, B-49'unki B-68'i, B-60'ınki B-71'i.
🔴 **Bu oturumun 13 düzeltmesinden hangisi bir sonrakini doğuruyor?**

**11 · Bu promptun kendisi.**
Bu metni **proje yazdı**, denetçi değil. 🔴 Neye bakmanı istemiyor olabilir?
Listede **olmayan** bir yere bak.

---

# ÇALIŞMA BİÇİMİN

1. **Önce oku, sonra koştur, en son yorumla.** İlk: kök `README.md` →
   `v2/03-YONTEM-KURALLARI.md` → `04`ün sonundaki **Y1–Y12**.
   🔴 **Y12 DÜNKÜ kuraldır** *(K-060)* ve kendi sınırı yazılı — o sınır
   senin av sahandır.
2. Her bulgunun yanında **üretici komut** *(depo kökünden koşabilir)* ve
   **kaynak dosya:satır**.
3. Bir iddiayı doğrularken **iddianın kendi ölçütünü kullanma.**
4. ⭐ **Y6 — beklenenden iyi çıkan sonuç, kötü çıkan kadar şüphelidir.**
   Dördüncü denetçi %25,0'i gördüğünde ilk baktığı yer **kendi örneklemiydi**;
   sen de öyle yap.
5. ⭐ **Y8** · ⭐ **Y10** *(`>` operatörü hiç tolerans almaz)* · ⭐ **Y11**.
6. 🔴 **Şüphelendiğin satırı `read_bytes()` ile oku** — B-58 bunun
   yapılmamasından doğdu ve **iki bağımsız göz birden** yanıldı.
7. 🔴 **Önerdiğin her değişmezi, önermeden önce KOŞTUR** — B-54'ün formülü
   tutmadı.
8. 🔴 **Yayımladığın her üretici komutu, yayımlamadan önce OLDUĞU GİBİ
   koştur** — üçüncü denetimin `scratchpad/den3/…` komutları yeniden
   üretilemedi.
9. Deneme için depoyu geçici bir dizine kopyala; **aslını değiştirme.**

---

# ORTAM VE KISITLAR

| | |
|---|---|
| Platform | Windows 11 · Python 3.11 · numpy, scipy, pytest kurulu |
| Dil | Kod ve belgeler **Türkçe**. Raporunu da Türkçe yaz |
| ⚠️ Konsol | `PYTHONIOENCODING=utf-8` — varsayılan cp1254 Türkçe karakterde çöküyor |
| ⚠️ Paralellik | Windows'ta `spawn`, `python - <<'PY'` ile verilen betikte **çöker**. Üretici komutların **seri** koşabilir olmalı ya da dosyaya yaz |
| 🔴 Git | **Hiçbir git komutu çalıştırma — `status` dahil** |
| 🔴 Kod | **Depodaki hiçbir dosyayı DEĞİŞTİRME.** Deneme için `tempfile.mkdtemp` kopyası |
| 🔴 Tohum | **2000–2029 HİÇBİR AMAÇLA koşulmaz.** Ayarlama: **1–30** |
| İşlemci | En fazla **10 çekirdek.** 30 dk'yı aşacak koşudan **önce** süre tahminini yazdır ve **SOR** |
| Yazacağın tek dosya | `aile0_audit.md` |

### ⏱️ Ölçülmüş süreler — 25 Ağustos, 10 çekirdek

| Komut | Süre |
|---|---|
| `python -m pytest tests -q` | **13,8 dk** *(367 test)* |
| `python -m pytest tests/test_kapi_secimleri.py -q` | **15,7 sn** ⭐ *(39 test)* |
| `python dogrulama/mutasyon_on_kontrol.py` | **0,4 dk** ⭐ |
| `python dogrulama/sag_kalan_ayikla.py` | ~5 dk |
| `python dogrulama/kurulum_kalibrasyonu.py` | ~2 dk |
| `python dogrulama/kor_mutasyon.py 24` | ~18 dk |
| `python dogrulama/mutasyon_paketi.py` | ~25 dk |
| `python dogrulama/aile0_kapi_raporu.py` | **150,2 dk** 🔴 *(beş koşu ölçüldü · izin gerekir)* |

⚠️ Süre tahmini bu depoda **üç kez** tutmadı. Kendi tahminini **ölçtüğün en
büyük** süreden kur.

---

# ENVANTER — 25 Ağustos 2026, koşturularak ölçüldü

| Büyüklük | Değer |
|---|---|
| Test | **367** |
| Hedefli mutasyon | **35** |
| Kör mutant havuzu | **227** |
| Karar kaydı | **60** *(K-001…K-060)* |
| Kapsam maddesi | **25** |
| Bulgu | **76** · 1 çürütüldü · **75 kapalı** · **1 açık (B-57)**
🔴 Ayrıca **B-78 · B-79** — kapının kendi düşüşünden çıktı *(K-058)* |
| Satır | `sim` **3 803** · `tests` **6 238** · `dogrulama` **3 899** |

```
README.md          harita — BURADAN BAŞLA
aile0_audit.md     DÖRT denetim raporu (4 812 satır)
v2/                belgeler 00–09
denetim/           bu prompt ve öncekiler
ciktilar/          araç çıktıları + politika
sim/ tests/ dogrulama/
```

**Kat 4 (yönlendirme) YOKTUR** — Aile 1'in işi.
Protokol arayüzü: `protokol_fabrikasi(kon) → protokol(gozlem) → int | None`
*(fabrika **düğüm başına** çağrılır)* · iki isteğe bağlı kanca:
`beacon_yuku(dugum)` ve `teshis(dugum)`

---

# ÇIKTI: `aile0_audit.md`

Dosya **dört denetimin raporunu** taşıyor. 🔴 **İçeriğini SİLME, DEĞİŞTİRME.**

1. Baştaki durum bloğunu beşinci denetimi de içerecek şekilde genişlet.
2. Sonuna `# BEŞİNCİ DENETİM — <tarih>` bölümü ekle.
3. 🔴 Bulgu numaraları **B-80**'den devam eder.
   ⚠️ **B-78 ve B-79 KULLANILMIŞTIR** — kapının 25 Ağustos'taki kendi
   düşüşünden çıktılar *(K-058)* ve `tests/test_kapi_secimleri.py`de
   `test_b78_*` / `test_b79_*` adlarıyla korunuyorlar.

```
## 0. YÖNETİCİ ÖZETİ
    Kapanış geçerli mi: EVET / KOŞULLU / HAYIR — üç cümlede
    🔴 KATMAN BAZINDA sağ kalan oranı + ULAŞILAN GÜÇ, ilk paragrafta

## 1. YENİ BULGULAR                       (B-80'den)
## 2. DÖRDÜNCÜ DENETİMİN BULGULARI — kapanma doğrulaması (≥8)
## 3. DOĞRULANAN İDDİALAR        ## 4. ÜRETİLEMEYEN İDDİALAR

## 5. 🔴 KENDİ MUTASYONLARIN — KATMANLI
    ≥19 sayaç · ≥8 mekanizma · ≥5 `sim/kosucu.py`
    Her biri: Y8 tetiklenme (ÖNCE) · 367 testten sağ çıktı mı ·
    sağ kaldıysa davranış değişiyor mu
    🔴 HER KATMAN İÇİN: oran · %95 GA · ULAŞILAN GÜÇ
    🔴 n < 19 olan katman için "kapandı" YAZILAMAZ

## 6. ŞÜPHE LİSTESİ SONUÇLARI    ## 7. KAPSAM BEYANINA EKLENECEKLER

## 8. 🔴 ANLAŞILMAYANLAR
    🔴 BOŞ BIRAKILAMAZ. Dört denetimde de bu bölümden GERÇEK KUSUR çıktı —
    üçüncüsünde A-4 buradan geldi ve bir kâhin kanalıydı.

## 9. KOŞTURDUĞUN KOMUTLAR
```

4. **Son satır:** hiçbir dosyanın değiştirilmediğini ve hiçbir git komutunun
   çalıştırılmadığını **açıkça yaz.**

---

# 🔴 SON SÖZ

Dört denetim, dört kez bulgu: **20 → 17 → 24 → 13.** Örüntü dört kez
kapanmadı. Beşincisinde kapanabilir — ama ancak **doğru katmanda ve yeterli
güçte** ölçülürse.

Dördüncü denetçi genel oranı %25,0'e düşürdü ve *"kapandı"* diyebilecekken
**demedi**, çünkü kendi örnekleminin karışımını ölçtü. Senden beklenen aynı
dürüstlüktür — **kendi lehine çıkan sonuca da Y6'yı uygula.**

**Bulacağın her şey, bulunmadığı takdirde jürinin bulacağı bir şeydir.**

Hiçbir şey bulamazsan bunu da yaz — ama **hiçbir şey bulamamak, aradığın
yerlerin listesiyle birlikte anlamlıdır.**

**Bir şeyi büyütmek istiyorsan önce ölç.**
