# 05 — GÖZLEM PENCERESİ

> ## ✅ GÜNCEL — 5 Eylül 2026
> Sözleşme, `sim2/gozlem/pencere.py` ile **birebir karşılaştırıldı**:
> komşu listesi yalnız beacon'dan geliyor, tek yönlü gecikme yok, konum
> yalnız komşunun BİLDİRDİĞİ kadar *(bedeli baytla ödenir)*. Uyumlu.


> 🔴 **Bu belge kod yazılmadan önce kilitlenir ve GENİŞLETİLMEZ.**
>
> Sonradan daraltmak, o zamana kadar yapılan **her ölçümü** geçersiz kılar.
> Sonradan genişletmek ise, önceki sonuçları yeni sonuçlarla karşılaştırılamaz hâle getirir.

---

## Neden bu belge var

Bir jüri üyesi şunu sorabilir:

> *"Protokolünüz karıştırıcının nerede olduğunu nereden biliyordu?"*

Cevap *"bilmiyordu"* olmak zorunda. Ve bu cevabın kanıtı bir cümle değil, **bir test** olmalı.

Önceki uygulamada (v1) şu soru cevapsız kaldı: *rakip protokol tazelik bilgisini kendi paketlerinden mi alıyordu, yoksa simülatörden bedava mı okuyordu?* Bilinmiyor. Eğer bedava okuyorduysa, ölçülen açığın bir kısmı gerçek değildi.

**Bu belirsizlik bir daha oluşamaz.**

---

# TEMEL KURAL

> ## Bir protokolün bildiği her şey, ya **aldığı bir paketten** gelmiş, ya da **kendi donanımının fiziksel olarak yapabileceği bir ölçümden** gelmiş olmak zorundadır.
>
> Simülatörden bedava okuma yoktur.

Bu tek cümle, aşağıdaki tüm listelerin kaynağıdır. Bir şeyin listede olup olmadığından emin değilsen, şu soruyu sor:

> **"Gerçek bir İHA'nın üstündeki gerçek bir telsiz bunu ölçebilir mi?"**

Ölçemiyorsa, karara giremez.

---

# A · GÖREBİLECEKLERİ

## A1 · Kendi donanımından ölçebildikleri

| Alan | Gerçek karşılığı |
|---|---|
| **Kendi anteninde ölçülen toplam gürültü + girişim gücü** | Gürültü tabanı ölçümü. Her telsiz yapar |
| **Kanal meşgul oranı** | Taşıyıcı dinlemenin ne kadar süre "meşgul" gördüğü |
| **Kendi kuyruğundaki paket sayısı** | Kendi belleği |
| **Kendi saati** | ⚠️ Düğümler arası **senkron değildir** → aşağıya bak |
| **Bir iletimin sonucu** | ✅ onay geldi · ❌ **zaman aşımı** |
| **Kendi gönderdiği/aldığı bayt sayısı** | Kendi sayaçları |

> ⭐ **"Zaman aşımı" bu listenin en önemli satırıdır.**
> *"Cevap gelmedi"* bir bilgi yokluğu değil, **bir gözlemdir.** Ve hiçbir bayta mal olmaz.

### 🔴 Saat senkronu yok — gecikme nasıl ölçülüyor

*(17 Ağustos'ta eklendi. Bu, sessizce bir kâhin yaratabilecek bir boşluktu.)*

Düğümlerin saatleri **senkron değildir.** Gerçek bir taktik ağda da değildir
(GPS senkronu varsayılamaz — GPS zaten karıştırma hedefidir).

**Sonucu:** bir düğüm, komşusuna giden **tek yönlü** gecikmeyi ölçemez. Çünkü
tek yönlü gecikme = `varış_saati(y) − gönderim_saati(x)` ve bu iki saat farklı.

| | |
|---|---|
| ❌ | Tek yönlü gecikme *(saat senkronu gerektirir)* |
| ✅ | **Gidiş-dönüş süresi** — gönderim ile onayın gelişi arasındaki fark, **tek saatle** ölçülür |
| ✅ | Kendi kuyruğunda bekleme süresi — kendi saatiyle |

**Bir maliyet fonksiyonunda gecikme terimi kullanan her protokol, gidiş-dönüş
süresini kullanmak zorundadır.** Tek yönlü gecikme kullanan bir tasarım, gerçek
donanımda ölçülemeyecek bir şeyi karara sokmuş olur.

⚠️ v1'in maliyet fonksiyonundaki `τ̂(x,y)` terimi tam olarak bu soruyu
soruyordu ve cevabı yazılı değildi.

## A2 · Aldığı paketlerden öğrenebildikleri

Bir paket alındığında, protokol o paketin **başlığında yazan** her şeyi okuyabilir.

**Ama üç kural geçerlidir:**

| # | Kural |
|---|---|
| **1** | Başlıktaki her alan **bayt olarak sayılır** ve kontrol yüküne yazılır |
| **2** | Bilgi **bayattır** — gönderildiği andaki hâline aittir, şu ankine değil |
| **3** | Paket **kaybolabilir** — bilginin ulaşacağı garanti değil |

Komşusunun girişim seviyesini veya kuyruk durumunu kullanmak isteyen bir protokol, o alanları başlığa **koymak** ve bedelini **ödemek** zorundadır.

## A3 · Kendi geçmişinden hesaplayabildikleri

Yukarıdaki iki kaynaktan gelen verilerin herhangi bir işlenmiş hâli: ortalamalar, sayaçlar, tahminler, tablolar.

---

## A4 · 🔴 KOMŞU LİSTESİ — ayrıca yazılıyor, çünkü en kolay kaçırılan kâhin

*(17 Ağustos 2026'da eklendi.)*

**Bir düğüm komşularını nereden bilir?**

| | |
|---|---|
| ❌ | Simülatörün menzil hesabından |
| ❌ | Konumlardan türetilmiş hazır bir listeden |
| ✅ | **Yalnızca yakın geçmişte beacon'ı alınan düğümlerden** |

**Üç sonucu var ve üçü de ölçüme girer:**

1. Beacon **bayta sayılır** — komşu bilmek bedavaya gelmez
2. Karıştırma altında **beacon da kaybolur** → komşu görünmez olur. *Gerçek bir telsizde tam olarak böyledir*
3. ⚠️ **t=0 başlangıç koşulu: hiçbir düğüm hiçbir komşusunu bilmez.** Komşu tablosu boştur ve beacon'larla dolar

> 🔴 **Neden ayrı başlık:** komşu listesi bedava verilirse, bir protokol karıştırma altında *"o düğüm hâlâ orada"* bilgisini **ücretsiz** almış olur. Bu, karıştırmanın en temel etkisini — bağlantının görünmez olmasını — iptal eder. Ölçtüğümüz şey artık karıştırma değildir.
>
> ⚠️ v1'de cevabı bilinmeyen *"rakip bilgiyi nereden alıyordu"* sorusu tam olarak buraya işaret ediyordu.

---

# B · 🔴 GÖREMEYECEKLERİ

| Yasak | Neden |
|---|---|
| **Karıştırıcının konumu, gücü, açık olup olmadığı** | Hiçbir telsiz bunu bilmez. Gürültüyü *hisseder*, kaynağını görmez |
| **Diğer düğümlerin konumu** | Ancak bir pakette geldiyse — ve bayt maliyeti ödendiyse |
| **Ağın gerçek topolojisi** | Hiçbir düğümde bütünsel görüntü yoktur |
| **Bir bağın gerçek kalitesi** | Yalnızca **kendi denemelerinden** çıkardığı tahmin kullanılabilir |
| **Gerçek en kısa yol** | Bu simülatörün bilgisi |
| **Bir paketin ileride teslim edilip edilmeyeceği** | Geleceğe bakmak |
| **Başka bir düğümün tablosu / durumu** | Ancak paketle geldiyse |
| **Simülatörün olay kuyruğu, tohumu, iç durumu** | Hiçbir koşulda |
| **Menzil içindeki düğümlerin listesi** | Komşuluk **ölçülür**, verilmez → §A4 |
| **Bir komşunun hâlâ hayatta olduğu** | Beacon gelmiyorsa komşu **yoktur**. Karıştırmanın en temel etkisi budur |

> ⚠️ **Dördüncü satıra dikkat.** *"Gerçek ETX"* diye bir şey simülatörün belleğinde vardır (biz üretiyoruz). Bir protokol ona **asla** dokunamaz. Yalnızca teşhis/analiz kodu okuyabilir — ve okuduğu şey karara giremez, sadece rapora girer.

---

> ## 🔴 1 EYLÜL 2026 — BU SÖZLEŞME HENÜZ GERÇEK PROTOKOLLE SINANMADI
>
> `08` Ç5 KAPSAMAZ tablosu: *"Sözleşme yalnızca **doğrulama
> aktarıcılarıyla** test edildi. Faz 1'in protokolleri yazıldığında
> **yeniden** sınanmalı."*
>
> 🔴 **Ve Faz 1'in üç protokolü bu sözleşmeye somut biçimde basacak:**
>
> | protokol | riskli yer | kural |
> |---|---|---|
> | **AODV / AOMDV** | RREQ/RREP **ağ çapında** dolaşır. Bir ara düğüm, paketin taşıdığı bilgiden fazlasını **çıkarmamalı** | §A2 — başlıktaki her alan **bayta sayılır** |
> | **OLSR** | MPR seçimi **iki-atlamalık komşuluk** ister; bu bilgi **yalnızca HELLO'lardan** gelmeli, topolojiden değil | §A4 — komşuluk **ölçülür, verilmez** |
> | **hepsi** | Rota tablosu **kendi geçmişinden** kurulur | §A3 |
>
> 🔴 **Sözleşme 37 maddelik kapsam listesinde madde 22'yle birlikte
> okunur:** gözlem penceresinin **14 alanı** bugün hiç okunmuyor. Faz 1
> protokolleri okumaya başladığında o sayı **düşecek** — amaç budur.
> ⚠️ Ama içerik güvencesi `PaketGorunumu`nun dört alanı için **hiç
> sınanmadı** *(D-12)*.
>
> ## 🔴 9 EYLÜL 2026 — SAYI YENİDEN ÖLÇÜLDÜ: **24 ALANIN 19'U OKUNMUYOR**
> *(Yukarıdaki "14" emekli `sim/` deposundan; bugünkü yüzey 12 + 7 + 5 = 24
> alan. Üretici: `protokoller/*.py` + `kalibrasyon/kahin.py` AST nitelik
> taraması. ⚠️ Yöntem nitelik ADI eşler, tipini doğrulamaz — okunan sayı
> için bir ÜST SINIRDIR.)*
>
> Okunan **5**: `dugum` · `komsular` · `paket` · komşunun `dugum`u ·
> paketin `hedef`i.
> 🔴 Bir anti-jamming protokolünün ihtiyaç duyacağı alanların **hiçbiri**
> okunmuyor: `olculen_gurultu_w` · `son_iletim_sonucu` · `kanal_mesgul_mu` ·
> `duyulan_beacon` · `son_duyulma_s` · `kuyruk_uzunlugu`.
>
> 🔒 Bu bir kusur değil, **projenin nerede durduğunun sayısıdır**: alet,
> ölçmek için var olduğu şeye henüz hiç dokunmadı.
>
> ## 🔴 VE BU BELGENİN KAPSAMADIĞI BİR EKSEN VAR — K-111, `07` §17.2
> Bu sözleşme protokolün ne **GÖRECEĞİNİ** kısıtlar. Protokolün ne
> **YAPABİLECEĞİ** — kendi çerçevesini gönderebilmesi, zamanlayıcı
> kurabilmesi — burada hiç geçmiyor, ve simülatörde de **yok**. Ölçüldü:
> temas yüzeyi dört kanca, tek periyodik beacon, üç canlı çerçeve tipi.
> Dolayısıyla `06` §4.2'nin istediği RREQ/RREP/RERR bugün **ifade
> edilemiyor**. ⚠️ Bu boşluğu kapatmak bu sözleşmeyi **genişletmez**:
> §A2 zaten *"başlıktaki her alan bayta sayılır"* diyor.
>
> 🔒 **Bu belge GENİŞLETİLMEZ.** Bir protokol yeni bir alana ihtiyaç
> duyarsa, alan eklenmeden önce **bu belgeye yazılır**, `04`e kayıt düşer
> ve **önceki sonuçların hâlâ geçerli olup olmadığı ayrıca sorulur**.

---

# C · NASIL ZORLANIYOR

Belge yeterli değil. Üç katmanlı koruma:

### 1 · Yapısal ayrım
Protokoller simülatör nesnesini **hiç görmez.** Yalnızca kısıtlı bir görünüm nesnesi alır. Görünüm nesnesinde simülatöre geri referans **yoktur.**

### 2 · Otomatik test
Bir test, görünüm nesnesinin yüzeyini tarar ve A bölümündeki listenin dışında bir şey bulursa **kırılır.**

### 3 · Yeni alan eklenirse
Bu belgeye yazılmadan hiçbir alan görünüme eklenemez. Eklendiğinde:
- Bu belge güncellenir
- `04-NEDEN-BOYLE.md`ye kayıt düşülür
- ⚠️ **Önceki sonuçların hâlâ geçerli olup olmadığı ayrıca sorulur**

---

# D · TEŞHİS SAYAÇLARI — ayrı bir kategori

Bunlar simülatörün **her şeyi bilen** tarafından okunur ve **rapora** girer. Protokolün kararına **girmez.**

| Sayaç | Ne söyler |
|---|---|
| Karar anında kullanılan bilginin **yaşı** | v1'de 3,95 s vs rakip 1,00 s |
| **Kaydın hiç olmadığı** karar oranı | v1'de %18,4 |
| Yalnızca **başarılardan** öğrenilen karar oranı | v1'de %13,65 |
| **Gerçek** kalitesi çok kötü olan bağdan geçen karar oranı | v1'de %24 (karıştırıcısız %14) |
| Protokolün o bağa dair **kendi kestirimi** | v1'de 52–64 (tipik bağ 2,5) |

> 🔴 **Bu ayrım hayatidir.** Aynı büyüklük iki farklı yerden okunuyor:
> - **Gerçek değer** → yalnızca teşhis ve rapor
> - **Protokolün tahmini** → yalnızca karar
>
> Kod incelemesinde ilk bakılacak yer burasıdır. Bu iki kanalın karışması, tüm sonuçları geçersiz kılar.

---

# E · SONUÇ SÖZLEŞMESİ

Her koşu, sonucunun yanında **tam konfigürasyonunu** taşır. Bayrağı olmayan bir satır yeniden üretilemez.

| Alan | Neden |
|---|---|
| Tüm konfigürasyon bayrakları | Hangi kolun sonucu olduğu |
| Tohum | Tekrar üretilebilirlik |
| Kod sürümü | Sayının hangi koddan geldiği |
| **Korunum denklemi sonucu** | Tutmadıysa satır **geçersiz** işaretlenir |
| Ölçüm penceresi (başlangıç–bitiş) | Isınma asimetrik; pencere yazılmazsa sonuç koşu uzunluğuna bağımlı olur |

Her satır **anında** diske yazılır. Uzun bir matris yarıda kesilirse tamamlanan koşular kaybolmaz.
