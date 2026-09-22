# 08 · EVRE METRİKLERİ — adım ⑤

> **Durum: 🟢 UYGULANDI** — 8 Eylül 2026 (öğrenci onayı), kapılar K-105.
> Şartname karşılığı: `07-SIMULATOR-TASARIMI.md` §05 · §08.
> Üretici: `python -u kalibrasyon/evre_metrikleri_kapilari.py`
>
> **10 Eylül 2026 güncellemesi (öğrenci kararları, K-113):**
> - M4'ün boş kol kapısı protokol yazım aşamasında (Aşama 2) koşulacak.
> - Karıştırıcı açılma anı (`T_j`) bir **parametre** olarak kalır; ısınma
>   ve ölçüm penceresi birlikte taranacak (`12` §3).
> - İki anlamlılık sabiti ölçülerek tek bir α'ya bağlanacak; hesapla
>   görülen risk ve ölçüm planı §05.3'te.
> - Karıştırıcılar çoklu ve hareketli olacağı için "açılma anı" ve evre
>   sınırlarının tanımı Aşama 1 tasarımında yeniden ele alınır (`07` §05).
> - Belgedeki "Faz 2" ifadeleri eski numaralamadır (`01` §5).

---

## 00 · NEDEN BU BELGE VAR

Şartname §08.2 dört metriği **isimlendiriyor** ama ikisini tanımsız
bırakıyor:

> *"toparlanma süresi = açılma anından, PDR'nin temiz değerinin **%X**'ine
> dönmesine kadar"*

`%X` seçilmemiş. "Kararlı hâl", "ilk tepki", "en dip nokta" ifadelerinin
hiçbiri bir sayıya bağlı değil. Bunlar **sonuç görüldükten sonra** seçilirse
metrik, ölçmek istediği şeyi değil, hoşa giden cevabı ölçer.

🔒 Bu belgenin işi: dört metriği **sıfır serbest parametreyle**, sonucu
görmeden tanımlamak.

---

## 01 · 🔴 İLK TASARIMIMDAKİ HATA — kayda geçer

İlk hâlinde şok penceresi `[T_j; T_j+3)` idi ve gerekçesi şuydu:

> *"3 s = AODV `ACTIVE_ROUTE_TIMEOUT` (RFC 3561); en hızlı taban çizgisi
> bile bu süreden önce tepki veremez, dolayısıyla orada ölçülen şey saf
> darbedir."*

**Gerekçe yanlıştı.** `ACTIVE_ROUTE_TIMEOUT` bir rotanın *kullanılmadığı
için* geçersizleşme süresidir; **bağ arızası tespiti değildir**. AODV bir
bağ koptuğunda MAC yeniden deneme sınırı dolar dolmaz RERR üretir — yani
**milisaniyeler** mertebesinde. Dolayısıyla *"hiçbir protokolün tepki
veremeyeceği bir pencere"* diye bir şey **yoktur**; reaktif bir protokol
milisaniyede tepki verir.

🔒 **Bunun sonucu, tasarımın kendisini değiştirdi.** "Şok derinliği" ile
"toparlanma hızı"nı bir zaman penceresiyle tamamen ayırmak **imkânsızdır**:
hızlı toparlanan bir protokolün çukuru gerçekten daha sığdır ve bu bir
ölçüm kusuru değil, fiziktir. Doğru yol ayırmaya çalışmak değil, **neyin
ölçüldüğünü açıkça söylemektir** (§03, M1).

⚠️ 3 s hâlâ kullanılıyor mu? **Hayır.** Izgara adımı için de yanlış çapaydı;
yerine RFC 3561'in `HELLO_INTERVAL`ı (1 s) kondu — §02.

---

## 02 · ÖLÇÜM KAFESİ — iki sabit, ikisi de doğrulanmış dış kaynak

Dört metrik **tek bir zaman kafesi** paylaşır. Kafesin iki parametresi var
ve ikisi de RFC'den gelir; ikisi de bu projede zaten kullanılıyor.

| ne | değer | kaynak | ne işe yarar |
|---|---|---|---|
| **ızgara adımı** `S` | **1 s** | RFC 3561 · AODV `HELLO_INTERVAL` | **çözünürlük** — hiçbir taban çizgisi komşu bilgisini bundan hızlı tazeleyemez, dolayısıyla daha ince bir ızgara gürültü ölçer |
| **pencere** `L` | **15 s** | RFC 3626 · OLSR `TOP_HOLD_TIME` | **durağanlık** — "ağ artık kararlı" denebilecek en kısa süre; daha dar bir pencere geçici bir sıçramayı toparlanma sanar |

🔒 **ÇÖZÜNÜRLÜK EN HIZLI TABAN ÇİZGİSİNDEN, DURAĞANLIK EN YAVAŞTAN.** Bu bir
tutarsızlık değil, iki farklı sorudur: *"ne sıklıkta bakabilirim"* ile
*"ne kadar bakarsam kararlı bir sayı görürüm"*. Tek çapaya indirmek ikisinden
birini bozar ve nasıl bozduğu §06/1'de yazılı.

⚠️ `Konfig.beacon_araligi_s` de 1,0 s'dir ve RFC 3561'in `HELLO_INTERVAL`ı
ile **aynı sayıdır** — ama köken defterinde `SINANMAMIS` (*"hiçbir gerekçe
yazılmamış"*). Kafes, o parametreye değil **RFC'ye** çıpalanır; ikisi bir
gün ayrışırsa kafes yerinde kalır. *(Ve bu, `beacon_araligi_s`in RFC 3561
`02`ye eklendiğinde `KAYNAK` kovasına geçebileceğini gösteriyor — borç
azaltma fırsatı.)*

---

## 03 · ZEMİN VE EVRELER

| büyüklük | değer | üretici |
|---|---|---|
| ölçüm penceresi | `[50; 320)` s | `Konfig.olcum_penceresi` |
| karıştırıcı açılma anı `T_j` | **150,0 s** | `Konfig.karistirici_baslangic_s` |
| trafik | 10 akış × 4 pkt/s = **40 pkt/s** | ölçülerek seçildi |
| uçtan uca gecikme p99 | **5–6 ms** | `ciktilar2/adim9_kapanis.jsonl` |

```
   50 s                          150 s        165 s                   320 s
    |------------ TEMİZ -----------|--- ŞOK ---|----- TOPARLANMA -------|
                                  T_j        T_j+L
```

| evre | aralık | uzunluk | paket/tohum | arm düzeyi SE (30 tohum) |
|---|---|---|---|---|
| **TEMİZ** | `[50; 150)` | 100 s | 4 000 | 0,0014 |
| **ŞOK** | `[T_j; T_j+15)` | 15 s | 600 | 0,0037 |
| **TOPARLANMA** | `[T_j+15; 320)` | 155 s | 6 200 | 0,0012 |

🔒 **Bölümleme tam** — boşluk yok. İlk tasarımdaki "GEÇİŞ" boşluğu, §01'deki
hatalı 3 s penceresini kurtarmak için vardı; o pencere gidince gereği kalmadı.

🔒 **PDR paketin DOĞUM anına göre kovalanır** (`pdr_pencere`nin tanımıyla
aynı). Evre sınırı gecikme kadar bulanıklaşır: bugün **6 ms / 1 s = %0,6**.
🔴 Bu sayı protokole bağlıdır — bugünkü ölçüm rota beklemeyen bir koşum
aletiyle alındı; gerçek bir AODV rota keşfi sırasında paketi kuyrukta tutar.
Kapı **G4** bunu her kolda yeniden ölçtürür.

---

## 04 · DÖRT METRİK

Hepsi **tohum başına** hesaplanır, sonra kol içinde toplanır. Sayımlar
havuzlanır.

### M1 · ŞOK DERİNLİĞİ
```
sok_derinligi = PDR(TEMİZ) − PDR(ŞOK)
```
- Birim: PDR puanı. Pozitif = bozulma. Yansız; binom hata payı kapalı formda.
- `PDR(TEMİZ)` tanımsızsa (`0` paket) → **`None`**.

🔴 **NE ÖLÇTÜĞÜ AÇIKÇA YAZILIR — §01'in dersi.** Bu sayı *"darbe ne kadar
sertti"* ile *"ilk 15 s içinde ne kadar toparlandım"*ı **birlikte** ölçer.
Hızlı toparlanan bir protokolün şoku gerçekten daha sığdır; bu bir artefakt
değil, gerçek bir üstünlüktür. Ayrıştırmak isteyen M3'e bakar — ikisi
**birlikte** okunur, tek başına değil.

🔴 **"EN DİP NOKTA" BİR SONUÇ DEĞİL, TEŞHİSTİR.** Şartname *"şok evresinin
en düşük PDR'si"* diyor. Bir eğrinin minimumu **aşağı yanlı** bir
kestiricidir: pencere sayısı arttıkça düşer. `en_dip` yine de raporlanır
(ızgara üzerindeki en düşük pencere PDR'si) ama **pencere sayısıyla
birlikte** ve `teshis` bölümünde — sonuç satırında değil.

### M2 · TOPARLANMA TAMLIĞI
```
toparlanma_tamligi = PDR(TOPARLANMA) / PDR(TEMİZ)
```
- `1,0` = tam toparlanma. `> 1` **kırpılmaz** — kırpmak bozuk bir ölçümü
  gizlemek olurdu.
- `PDR(TEMİZ) = 0` ise `None`, sıfır değil.

### M3 · TOPARLANMA SÜRESİ
```
ızgara  t ∈ {T_j, T_j+1, T_j+2, …},  t + L ≤ 320
T_kur   = bu t'lerin EN KÜÇÜĞÜ öyle ki
          p̂([t; t+L))  ≥  p̂(TEMİZ) − 2·SE
          SE = √( p̂c(1−p̂c)/Nc + p̂w(1−p̂w)/Nw )

toparlanma_suresi = T_kur − T_j        (yoksa: SANSÜRLÜ = None)
```

🔴 **`%X` ÖLDÜRÜLDÜ.** Şartnamedeki *"temiz değerin %X'i"* serbest bir
parametredir ve serbest bir parametre, eğriler görüldükten sonra seçilir.
`2·SE` bandı **koşunun kendi paket sayımlarından** hesaplanır: seçilecek bir
şey yoktur.

🔒 **SANSÜR ASLA SAYIYA ÇEVRİLMEZ.** Toparlanmayan bir koşu *"170 s'de
toparlandı"* diye ortalamaya girmez; `None` döner ve **sansür oranı kol
başına raporlanır**. Aksi hâlde hiç toparlanmayan bir protokol, pencerenin
uzunluğu kadar iyi görünürdü. Bu, Δ için zaten kurulmuş olan kuralın aynısı.

⚠️ **BEYAN EDİLEN SINIR:** band, `p̂` 0 ya da 1'e yakın olmadığında genişler;
yani gürültülü bir kolda "toparlandı" demek daha kolaydır. Her istatistiksel
ölçütün özelliğidir. `SE` metrikle **birlikte** raporlanır.

### M4 · TESPİT GECİKMESİ
```
λ̂        = TEMİZ evrede ızgara kovası (1 s) başına kopma BEYANI sayısı
T_tespit = t > T_j ızgara anlarının EN KÜÇÜĞÜ öyle ki
           [t−1; t) aralığındaki beyan sayısı > Poisson(λ̂) %99 yüzdeliği

tespit_gecikmesi = T_tespit − T_j       (yoksa: SANSÜRLÜ = None)
```

🔒 **GÖZLEM PENCERESİ GENİŞLETİLMEZ.** Metrik, var olan beyan kanalını
kullanır; protokole yeni bir yüzey açılmaz.

🔴 **"AÇILMADAN SONRAKİ İLK BEYAN" YETMEZ.** Protokoller karıştırıcı olmadan
da sürekli kopma beyan eder (sönümleme, hareket). İlk beyanı almak çoğu zaman
karıştırıcıyla **ilgisi olmayan** bir olayı ölçmektir. Boş hipotez bu yüzden
**aynı koşunun kendi TEMİZ evresinden** kestirilir.

🔒 **SUSAN PROTOKOL HIZLI GÖRÜNEMEZ.** `beyan_etmiyor` ise metrik `None`
döner — sıfır değil.

---

## 05 · 🔴 METRİKLERİN KENDİ DOĞRULAMA KAPILARI

Bir ölçüm aleti, ölçtüğü şey kadar sınanır. Dört kapı, metrikler bir sonuç
için kullanılmadan **önce** geçilir.
Üretici: `python -u kalibrasyon/evre_metrikleri_kapilari.py`

| kapı | ne sınar | geçme ölçütü | sonuç |
|---|---|---|---|
| **G1 · BOŞ KOL** | karıştırıcısız kolda metrikler susuyor mu | **kol ortalaması** `sok_derinligi` 0'dan 2 SE içinde · her tohumda `toparlanma_suresi` = 0 · `tespit_gecikmesi` SANSÜRLÜ | 🟢 **GEÇTİ** — ortalama −0,00125 · 2 SE 0,00204 |
| **G2 · TEKDÜZELİK** | `sok_derinligi` şiddetle artıyor mu | hiçbir düşüş, iki noktanın **birleşik 2 SE**'sini aşmayacak | 🟢 **GEÇTİ** *(§05.2)* |
| **G3 · IZGARA FAZI** | sonuç örnekleme fazına bağlı mı | ızgara yarım adım kaydırılınca hiçbir karar kendi hata payından fazla değişmiyor | 🟢 **GEÇTİ** — en büyük fark 0,00187, band 0,00991 |
| **G4 · BULANIKLIK** | doğum-anına-göre kovalama geçerli mi | `gecikme_p99 / S < 1` — aşarsa atfetme kuralı **yeniden yazılır** | 🟢 **GEÇTİ** — 0,021 (temiz) · 0,029 (karıştırılmış) |

⚠️ **G1'in DÖRDÜNCÜ maddesi boş yere geçiyor ve bu beyan edilir:** tespit
gecikmesi bir protokolün kopma beyanını gerektiriyor, depodaki iki koşum
aleti de hiç beyan etmiyor. **M4'ün boş kol kapısı Faz 2'ye ertelenmiştir**;
bugünkü kapsamı `tests2/test_evre.py`in sentetik testleridir.

🔒 G3 doğrudan 8 Eylül dersinden geliyor: ρ'nun üç sabit örnekleme anı darbe
periyoduyla örtüşüyordu ve bu **sonradan** fark edildi. Aynı hatayı bu sefer
yapıdan önce sınadık — ve geçti.

### 05.1 · 🔴 G1 İLK KOŞUDA KALDI — ve kusur METRİKTE DEĞİL, HATA PAYINDAYDI
Tohum 1002: `sok_derinligi` −0,00375, band 2 SE = **0,00193**. Sebep, Wald
kestiricisidir: `SE² = p(1−p)/n`, ve `p = 1` olduğunda **tam olarak sıfır**.

🔴 Ve bu projede `p = 1` bir istisna değil **kuraldır**: karıştırıcısız kolda
kâhin PDR'si 1,000 ölçülüyor — §10/4 gerçekçilik kapısının talebi tam olarak
budur. Yani hata payı, en çok ihtiyaç duyulduğu yerde çöküyordu. Bu, yalnız
kapıyı değil **`toparlanma_suresi`nin bandını da** bozuyordu: sıfır genişlikte
bir band hiçbir zaman sağlanmaz.

🔒 Düzeltme **Agresti–Caffo**: iki oranın FARKI için belgelenmiş standart —
her örneğe bir başarı ve bir başarısızlık eklenir. Sınırda çökmez, serbest
parametre getirmez. Bedeli beyan edilir: band Wald'a göre biraz geniştir.
*(Aynı tohum düzeltmeden sonra tek başına da geçiyor: 0,00375 < 0,00387.)*

🔒 İkinci düzeltme **istatistikseldir**: verdikt tohum başına değil **kol
ortalamasında** verilir. Tohum başına bir 2 SE testi tanım gereği tohumların
~%5'inde kalır; üç tohumda en az birinin kalma olasılığı ~%14. Yani tohum
başına bir kapı, doğru bir metriği rastgele reddeder. Şok derinliği zaten
kol düzeyinde okunuyor (§06/2).

### 05.2 · 🔴 G2'NİN İLK ÖLÇÜTÜ DE YANLIŞTI — "kesin monoton artış"
İlk hâli *"güç arttıkça şok derinliği monoton artmalı"* idi. Ölçüldü:

| güç (dBm) | şok derinliği (3 tohum ort) | SE |
|---|---|---|
| −30 | −0,00069 | 0,00069 |
| −21 | −0,00125 | 0,00042 |
| −15 | **+0,03707** | 0,00618 |
| −9 | **+0,18742** | 0,01540 |

İlk iki nokta arasında bir "düşüş" var — ama ikisinin de gerçek değeri
**sıfır** (o güçlerde kâhin hiçbir şey kaybetmiyor) ve fark 0,00056, birleşik
2 SE'nin çok içinde.

🔴 Yani ölçüt **sınanamaz** bir şey istiyordu: gerçek değeri eşit olan iki
noktada gürültü ~%50 olasılıkla düşüş gösterir, dolayısıyla DOĞRU bir metrik
yarı yarıya kalırdı. Düzeltilen şey eşik değil **tanım**: *"artış"* bir
ölçümdür ve ölçülen her şey hata payıyla okunur. Yeni ölçütün de sıfır
serbest parametresi var — band verinin kendisinden geliyor.

⭐ **VE TABLO KENDİ BAŞINA BİR BULGU:** çalışma noktasında (−15 dBm)
**mükemmel yönlendirmeyle** şok derinliği yalnız **0,037**. Yani ayırt edici
gücün tamamı protokolün körlüğünden gelmek zorunda — K-103'ün argümanının
bağımsız bir doğrulaması.

---

### 05.3 · Tek α ve tarama düzeltmesi — 🟢 uygulandı (14 Eylül 2026, Y10)

**🟢 UYGULANDI (14 Eylül 2026, Y10 · `04` K-123).** Evre modülünde artık
TEK sabit var: `ALFA = 0,05`. M3'ün bandı `z(1 − α/2)` = 1,95996 olarak
ondan TÜRER (elle 1,96 yazılmaz); M4'ün eşiği pencere başına
`α / taranan pencere`dir (Bonferroni). Aşağıdaki ölçüm kararın gerekçesidir
ve artık bir KAPIDIR: `python -u kalibrasyon/anlamlilik_sabitleri.py`
bugünkü kuralın aile düzeyi yanlış alarmı `ALFA`yı aşarsa çıkış kodu 1
verir. 14 Eylül'de yeniden ölçüldü: eski kural 0,374–0,696, bugünkü kural
0,022–0,034.

Bugün iki ayrı sabit var:

| sabit | değer | kullanıldığı yer |
|---|---|---|
| toparlanma bandının genişliği | 2,0 SE (tek yanlı ~%97,5) | M3 |
| tespit eşiğinin yanlış alarm oranı | 0,01 — pencere başına Poisson kuyruğu | M4 |

İkisi de bir α'dır ve ayrı durmaları gerekçesizdir (köken defterinde
`SINANMAMIS`). Öğrenci kararı: ölçülerek en mantıklısı seçilecek.

**Hesapla görülen risk — ölçülmedi.** M4, açılma anından ölçüm penceresinin
sonuna kadar 1 s'lik pencereleri tek tek tarar ve eşiği aşan **ilk**
pencereyi alır. Varsayılan kafeste bu yaklaşık 170 pencere eder (151…320 s).
Pencere başına yanlış alarm en çok 0,01 ve pencereler bağımsız sayılırsa,
karıştırıcısız bir kolda en az bir yanlış tespit olasılığı en çok
`1 − 0,99^170 ≈ 0,82`dir. *(Üretici: hesap. Ayrık Poisson'da pencere başına
gerçek oran 0,01'in altında kalabilir; gerçek değer ölçülecek.)* Yani kopma
beyan eden bir protokolde G1'in "tespit gecikmesi SANSÜRLÜ" maddesi
tohumların çoğunda kalabilir. Bugün görünmüyor, çünkü depodaki koşum aletleri
hiç beyan etmiyor. M3'te benzer bir etki ters yönde çalışır: ilk başarılı
pencereyi aldığı için gürültü "erken toparlandı" demeyi kolaylaştırır (M3'ün
§04'te beyan edilmiş sınırı).

**Ölçüldü (11 Eylül 2026).** Üretici: `python -u kalibrasyon/anlamlilik_sabitleri.py`.
Sentetik boş hipotez: homojen Poisson beyanlar, açılmada değişiklik yok, hücre
başına 4 000 deneme, gerçek `tespit_gecikmesi` fonksiyonu. Değerler yanlış
alarm oranı ± 2 SE.

| beyan hızı (1/s) | bugünkü kural — pencere başına 0,01 | Bonferroni — 0,05 / 170 |
|---|---|---|
| 0,1 | 0,514 ± 0,016 | 0,022 ± 0,005 |
| 0,5 | 0,374 ± 0,015 | 0,024 ± 0,005 |
| 2,0 | 0,578 ± 0,016 | 0,034 ± 0,006 |
| 10,0 | 0,696 ± 0,015 | 0,030 ± 0,005 |

- **Bugünkü kural:** karıştırıcısız kolda yanlış tespit %37–70. Kopma beyan
  eden bir protokolde M4 çoğu zaman gerçek bir değişimi değil, taramanın
  kendisini ölçerdi. Hesaptaki üst sınır (0,82) ile tutarlı; ayrık Poisson
  eşiği yüzünden altında.
- **Bonferroni kuralı:** aile hedefi 0,05'in altında kalıyor.
- **M3'ün bandı:** `BANT_SE_KATI` = 2,0, tek α = 0,05 için çift yönlü
  z(0,975) = 1,96 ile zaten uyumlu. Değişmesi gereken asıl sabit
  `YANLIS_ALARM`dır.
- **Öneri** (yapı onayı — `07` §18 Y10): tek α = 0,05 (`06` §7). M4 eşiği
  pencere başına α / taranan pencere sayısı. M3 bandı aynı α'dan z olarak
  türetilir. M3'ün sentetik sınavı ayrıca yapılır.

**Plan (`12` §3):**

1. Tek α ön-kayıttan gelir (`06` §7).
2. M4 eşiği taranan pencere sayısı hesaba katılarak kurulur (ör. Bonferroni
   ya da sıralı bir test); seçim ölçümle yapılır.
3. Karıştırıcısız kolda gerçek yanlış alarm oranı ölçülür: önce sentetik
   Poisson beyanlarıyla (simülatörsüz, hızlı), sonra Aşama 2'de gerçek bir
   protokolle.
4. M3 bandı için aynı α ile boş kolda yanlış "toparlanmadı" oranı ve
   karıştırılmış kolda erken toparlanma yanlılığı ölçülür.

---

## 06 · İKİ SORU — karara bağlandı

### 1. Bir metrikte iki farklı taban çizgisi çapası
**Karar: İKİ ÇAPA KALIR.** Tek çapaya indirmek ikisinden birini bozuyor ve
nasıl bozduğu ölçülebilir:

- **Her şey 1 s olsaydı:** test penceresi 1 s = 40 pakete inerdi, tohum
  başına SE ≈ 0,08. Geçici bir sıçrama "toparlanma" diye okunurdu.
- **Her şey 15 s olsaydı:** toparlanma süresi 15 s'lik adımlara kuantalanırdı.
  155 s'lik toparlanma evresinde yalnız **10 ayırt edilebilir değer** kalırdı
  ve 15 s'den az farkla ayrışan protokoller **aynı** görünürdü — oysa
  şartname toparlanma süresini *"protokoller arası asıl ayırt edici"* diye
  tanımlıyor.

🔒 İkisi ayrı sorudur ve ayrı çapayı hak eder: **çözünürlük en hızlı taban
çizgisinden, durağanlık en yavaştan.**

### 2. Şok penceresinin gürültüsü
**Karar: PENCERE 15 s, ŞOK DERİNLİĞİ KOL DÜZEYİNDE OKUNUR.**
İlk tasarımdaki 3 s'lik pencere §01'de çürüdüğü için soru kendiliğinden
küçüldü: 15 s'de tohum başına 600 paket var, SE ≈ 0,020; 30 tohumluk kol
ortalamasında SE ≈ **0,0037**. Yük artırmaya ya da tohum sayısını değiştirmeye
gerek yok — ikisi de çalışma noktasını değiştirirdi.

⚠️ Yine de **tohum başına şok derinliği tek başına okunmaz** ve bu beyan
edilir: SE her koşuda metrikle birlikte raporlanır.

---

## 07 · UYGULAMA — çekirdeğe dokunmuyor

🔒 Dördü de **son işlemdir**: paket defteri zaten paket başına doğum ve teslim
anını, rota defteri zaten beyanları zaman damgasıyla tutuyor. Sıcak yolda
hiçbir değişiklik, hiçbir yeni sayaç yok.

Bu bir tercih değil **kısıttır**: metrikler sıcak yola sayaç eklemeyi
gerektirseydi, ölçümün maliyeti sonuca karışırdı.
