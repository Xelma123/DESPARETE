# 07 — SİMÜLATÖR ARAYÜZÜ

> **Bu belge kod değildir.** Kutular, oklar ve sorumluluklar.
> Onay alınmadan tek satır kod yazılmaz.

---

> ## 🟡 FAZ 0 — KAPI 13/13, AMA **KAPALI DEĞİL** *(1 Eylül 2026)*
>
> ⚠️ Burada eskiden *"AİLE 0 KAPANDI — 19 Ağustos 2026"* yazıyordu ve
> **üç kez bayatladı**: kapı o günden sonra 21, 25 ve **27 Ağustos**'ta
> yeniden koştu; kapsam listesi 24 → **33** maddeye çıktı; ve 1 Eylül'de
> Faz 0'ın **kapalı olmadığı** ölçüldü.
>
> **Bugünkü durum:** kapı **13/13** *(27 Ağustos, 185,6 dk)* ve sonucu
> ~~bayat değil~~ → 🔴 **BAYAT** — `sim/` B0/B0.7/B0.8'de değişti *(`89587a19…` → `fc73905b…`)*. Bu **bilerek**: kapı `12` §2.3 gereği **B0 ve B1 birlikte bittikten sonra TEK KEZ** koşar. **B-129**.
> 🟢 **B0 koşuldu** *(K-086)*: sekiz kalemin dördü kapandı, biri
> denetlendi. 🔴 Kalan üç kalem + **Kat 4 altyapısı** →
> `13-AILE0-KAPANIS-KANITI.md`.
> ⚠️ **Kapı sonucu artık BAYAT:** `sim/` B0'da değişti
> *(`89587a19…` → `0a1a94e5…`)*; kapı B0 **ve** B1'den sonra tek kez koşar.
>
> ⚠️ **Şema DONDU** *(79 alan)*. Faz 1 başladıktan sonra değişemez —
> değişirse eski satırlar karşılaştırılamaz hâle gelir.
>
> 🔴 **Neyi kapsamadığı:** `08-AILE0-KAPSAM.md` — **33** maddelik sınır
> listesi. O belge okunmadan bu kapının geçtiği söylenemez.
>
> **Sıradaki adımlar Faz 1'e aittir:** Kat 4, üç rakip protokol *(§4.1)*.

---

# GENEL GÖRÜNÜM

```
        ┌─────────────────────────────────────────────┐
        │  KONFİGÜRASYON                              │
        │  Tek nesne. Tüm bayraklar burada.           │
        │  Ablasyon kolları = bayrak değişimi.        │
        └──────────────────┬──────────────────────────┘
                           │
        ┌──────────────────▼──────────────────────────┐
        │  KAT 0 · TRAFİK                             │
        │  Kaynak–hedef çiftleri · CBR üretimi        │
        │  Doz–yanıt ekseni burada yaşar              │
        └──────────────────┬──────────────────────────┘
                           │
        ┌──────────────────▼──────────────────────────┐
        │  KAT 1 · ZAMAN                              │
        │  Olay kuyruğu. Kesikli olay döngüsü.        │
        └──────────────────┬──────────────────────────┘
                           │
        ┌──────────────────▼──────────────────────────┐
        │  KAT 2 · RADYO                              │
        │  Mesafe → sinyal · karıştırıcı → gürültü    │
        │  SINR → paket hata olasılığı                │
        └──────────────────┬──────────────────────────┘
                           │
        ┌──────────────────▼──────────────────────────┐
        │  KAT 3 · KANAL ERİŞİMİ (MAC)                │
        │  Taşıyıcı dinleme · geri çekilme            │
        │  Onay / zaman aşımı · gizli terminal        │
        └──────────────────┬──────────────────────────┘
                           │
        ┌──────────────────▼──────────────────────────┐
        │  KAT 5 · GÖZLEM PENCERESİ  🔴   gozlem.py   │
        │  Gozlem · KomsuKaydi · PaketGorunumu        │
        │  Geri referans YOK — özyinelemeli test var  │
        └──────────────────┬──────────────────────────┘
                           │        ▲
                           ▼        │ yalnızca "paket gönder"
        ┌─────────────────────────────────────────────┐
        │  KAT 4 · YÖNLENDİRME                        │
        │  Tüm protokoller ve tüm kollar burada.      │
        │  Kat 1–3'ü GÖREMEZ.                         │
        └─────────────────────────────────────────────┘

        ┌─────────────────────────────────────────────┐
        │  TEŞHİS  (her şeyi görür, karara giremez)   │
        │  Korunum · sayaçlar · gerçek değerler       │
        └─────────────────────────────────────────────┘
```

🔴 **Dikkat:** Kat 4, Kat 5'in **altında** çizilmiştir. Yönlendirme katmanı
simülatörün içine bakmaz; simülatör ona kısıtlı bir görünüm **verir.**

---

# KAT 0 · TRAFİK

**Sorumluluk** — Paketleri doğurmak. *(İlk taslakta eksikti — 17 Ağustos'ta eklendi.)*

**Ne yapar**
- Sabit sayıda **kaynak–hedef çifti** seçer *(kendi RNG akışından)*
- Her çift için CBR üretir: sabit aralık + küçük rastgele titreşim
- **Doz–yanıt ekseni burada:** aktif çift sayısı üç seviyede *(yoğun / orta / seyrek)*

**🔴 Çiftler nasıl seçilir — teslim tavanı %100 olmalı**

Rastgele yerleştirilmiş 30 düğüm her zaman bağlı bir graf üretmez. Bir hedef
zaten ulaşılamazsa, o paketin kaybı protokolün değil **topolojinin** suçudur.

**Kural:** kaynak–hedef çiftleri yalnızca **karıştırıcısız topolojide birbirine
ulaşabilen** düğümler arasından seçilir.

⚠️ **DÜZELTME (B-18, 19 Ağustos 2026):** burada önce teslim tavanının
**%100** olduğu yazıyordu. Ölçüldü *(90 koşu, güncel kod)*: ortalama
**0,9938**, aralık **[0,8996 · 1,0000]**, yalnızca **21/90** koşu tam %100. Kalan kayıp menzil sınırındaki PER'den
ve MAC çakışmalarından geliyor.

Sonucu: S0 senaryosunda teslim tavanı **~%99'dur** ve oradaki her kayıp
protokole ya da MAC'e atfedilebilir. Kontrol kolunun anlamlı olması buna bağlı.

⚠️ Bu seçim **senaryo kurulumudur**, protokol kararı değil. Topoloji bilgisini
kurulum kullanabilir; protokol kullanamaz.

**⚠️ Neden titreşim var** — Tüm kaynaklar tam olarak aynı aralıkta üretirse
periyodik süreçler kilitlenir; bu, tohumlar arası varyansı **yapay olarak**
düşürür. Titreşim kendi RNG akışından çekilir.

**⚠️ Neden aynı çiftler her kolda kullanılır** — Kaynak–hedef çiftleri
**tohumdan** üretilir, koldan değil. Aynı tohum → aynı çiftler → gerçek
eşleştirme.

### 🔴 Boşaltma (drain) politikası

```
0 ────── 50 ──────────────────────── 320 ─── 350
  ısınma        trafik üretiliyor      boru
                                     boşalıyor
  └────────── ÖLÇÜM PENCERESİ: 50–320 ──────────┘
```

Trafik üretimi koşu bitiminden **30 s önce** durur. Boru boşalır.

**Neden** — Koşu, kuyruklarda ve havada paket varken kesilirse, bu paketler
"teslim edilmedi" sayılır. Uzun rota kullanan protokolün borusu daha doludur —
yani **haksız yere cezalandırılır.** Bu, ölçüm penceresini koşu uzunluğuyla
eşitleme tuzağının somut hâli.

**Boşaltma sonunda hâlâ boruda kalan paket varsa** → ayrı sayaç, raporlanır.

---

# KAT 1 · ZAMAN

**Sorumluluk** — Olayları zaman sırasına göre işlemek.

**Ne yapar**
- Öncelik kuyruğu: `(zaman, sıra_no, olay)`
- En erken olayı çıkar, çalıştır, doğan yeni olayları ekle
- Gerçek zaman yok, kare yok, sabit adım yok

**Neden sıra numarası var** — Aynı zamana denk gelen iki olayın sırası
belirlenimci olmalı. Yoksa aynı tohum farklı sonuç verir.

**Değişmez** — İşlenen olayların zamanı **asla azalmaz.**

---

## 🔴 RASTGELELİK AKIŞLARI

*(İlk taslakta ilke yazılıydı ama akışlar sayılmamıştı — 17 Ağustos'ta eklendi.)*

**YEDİ ayrı akış + kanal.** Her biri `(ana_tohum, akış_adı)`dan türetilir.

| # | Akış | Ne çeker |
|---|---|---|
| 1 | `yerlesim` | Düğüm konumları |
| 2 | `trafik_ciftleri` | Kaynak–hedef seçimi |
| 3 | `trafik_zamani` | CBR titreşimi |
| 4 | 🆕 `beacon_faz` | Beacon başlangıç fazı — **B-10/K-040'ta eklendi** |
| 5 | `mac_geri_cekilme` | Çakışma sonrası bekleme |
| 6 | `karistirici_faz` | Darbeli karıştırıcının başlangıç fazı |
| 7 | ⭐ `protokol_kesif` | Keşif kararları — **her protokol için ayrı**. Faz 0'da hiç çekim almadı; 🆕 **Faz 1 ile kullanıma girecek** *(OLSR `MAXJITTER` · AODV RREQ geri çekilmesi)* — §4.4 |
| — | `kanal` | ⚠️ **Aşağıya bak — bu bir akış değil** |

> ⚠️ **`beacon_faz` 20 Ağustos'a kadar bu tabloda yoktu (B-33).** `rng.py`
> başlığı bu tabloya atıf yapıyor ve *"bu liste kapalıdır"* diyor; akış
> koda ve karar defterine eklenmiş, **belgeye eklenmemişti.** Kapalı bir
> listenin tek kopyası olmalı.

> ## 🔴 BEYAN EDİLMİŞ TEK İSTİSNA — `kalite_ablasyonu` *(B-103, 27 Ağu 2026)*
>
> Yukarıdaki liste **`sim/` altındaki** rastgelelik kaynakları için kapalıdır
> ve öyle kalır. Ama `dogrulama/` altında **bir istisna vardır ve bugüne
> kadar hiçbir belgede yazılı değildi:**
>
> ```python
> # dogrulama/aktaricilar.py::kalite_ablasyonu
> random.Random((hash(anahtar) & 0xFFFFFFFF) ^ tuz).shuffle(idx)
> ```
>
> 🔴 **Bu, ön-kayıtlı H1.1 kapısının NULL MODELİDİR** — yani `06`nın
> mühürlediği ölçütün bir parçası. `Akislar` dışında bir kaynak kullanıyor ve
> `rng.py`nin kendi uyarısıyla çelişiyor: *"`hash()` çalışmalar arasında
> tuzlanır ve BELİRLENİMCİ DEĞİLDİR."*
>
> **Altıncı denetim üç ölçümle bugün ZARARSIZ olduğunu gösterdi:**
>
> | soru | ölçüm |
> |---|---|
> | `hash()` belirlenimci mi | ✅ **tamsayı demeti** üç `PYTHONHASHSEED` değerinde **birebir aynı** *(dizgi demeti üç FARKLI değer verir)* |
> | `tuz` XOR'u çekimleri bağımsız yapıyor mu | ✅ 200 000 anahtar × 5 çekim; çift-eşitlik oranı **1/k! referansıyla ayırt edilemez** |
> | tohumlar arası anahtar örtüşmesi | ✅ 959 ayrık anahtar, 28 tohum çiftinin hepsinde **%0,000** |
>
> 🔴 **AMA İSTİSNA BEYAN EDİLMEK ZORUNDADIR** ve bu blok o beyandır.
> Gerekçe: bir istisna yalnızca bir test docstring'inde yazılıysa, `08`in
> kapsam beyanı onu **taşımıyor** demektir *(B-103)*.
>
> ⚠️ **KIRILGANLIK NOKTASI — ölçülmüş:** güvence `anahtar`ın bir **tamsayı
> demeti** olmasına dayanıyor. Anahtar bir gün **dizgi** taşırsa
> `PYTHONHASHSEED`e bağlı hâle gelir ve Ç2 sessizce kırılır. Bunu zorlayan
> koruma: `tests/test_kapi_aile0.py::test_c2_2_pythonhashseed_den_bagimsiz`
> *(B-94 ile ablasyon kolu da kapsamda)*.
>
> 🔴 **İKİNCİ ÖLÇÜLMÜŞ SINIR:** ablasyon **k ≤ 3** olan kararlarda `m = 5`in
> çoğu çekimi çakışır — `k = 1`de permütasyon **birim**, `k = 2`de yalnızca
> iki permütasyon var. Kapının kendi yapılandırmasında bu kararların payı
> **%11,73** *(52 744 / 449 498)*. K-064'ün *"çekim varyansın %46,4'ü"*
> ayrıştırması **tek havuzlanmış sayıdır**; karar başına kazanç `k`ya bağlıdır.

### Neden 6 numara ayrı olmak zorunda

Keşif yapan bir protokol, keşif yapmayandan **daha çok rastgele sayı çeker.**
Ortak akışta bu, sonraki tüm çekimleri kaydırır → protokoller farklı senaryo
görür → eşleştirme kırılır. 30 tohum bunu **kurtarmaz.**

### 🔴 Neden 7 numara bir akış DEĞİL

Kanal hatası her iletim denemesinde bir sayı çeker. Protokol A, B'den daha çok
deneme yaparsa sıralı akış kayar ve **aynı tohumda farklı kanal gerçeklemesi**
oluşur.

**Çözüm — sayaç tabanlı (durumsuz) rastgelelik:**

```
kanal_rastgele = hash(ana_tohum, gönderen, alan, zaman_dilimi)
```

Sıralı durum yok. Aynı anda aynı çift arasındaki iletim, **hangi protokol
koşarsa koşsun** aynı gerçeklemeyi görür.

> ⭐ Bu tek karar, eşleştirilmiş testin gücünü ciddi biçimde artırır: iki kol
> arasındaki fark artık kanal gürültüsünün farklı çekilmesinden değil, yalnızca
> **protokol davranışından** gelir.

**Regresyon testi** — İki farklı protokol aynı tohumda koşulur; kanal hata
kayıtları, ortak (gönderen, alan, zaman) üçlüleri için **birebir** aynı olmalıdır.

---

# KAT 2 · RADYO

**Sorumluluk** — İki düğüm arasındaki iletimin başarılı olup olmadığına karar
vermek.

**Zincir**

```
mesafe ──► yol kaybı ──► alınan sinyal gücü ─┐
                                              ├──► SINR ──► hata olasılığı ──► ✅/❌
gürültü tabanı + karıştırıcı + diğer iletimler┘
```

**Karıştırıcı modeli**

| Tip | Davranış |
|---|---|
| **Sabit** | Konumu sabit, gücü sabit, sürekli açık |
| **Darbeli** | Görev çevrimiyle açılıp kapanır. ⚠️ **Fazı her tohumda rastgelelenir** |
| **Hareketli** | Belirlenimci yörünge, sürekli açık |

**Kapsam dışı** — Modülasyon, OFDM, sembol seviyesi, kodlama.
*Gerekçe: SINR→hata soyutlaması yeterli (`01` §5.1).*

### 🔴 GÖLGELEME: ilk sürümde YOK — ve bu bilinçli

*(İlk taslakta "eklenirse" diye açık bırakılmıştı — 17 Ağustos'ta karara bağlandı.)*

| | Karar |
|---|---|
| Yol kaybı | **Belirlenimci** *(log-mesafe)* |
| Gölgeleme / sönümleme | ❌ **İlk sürümde yok** |

**Üç gerekçe:**

1. **Durağan dağılım tuzağından kaçınmak.** Gölgeleme durum tutan bir süreçtir.
   t=0'da durağan dağılımdan çekilmezse her koşu bir geçiş rejiminde başlar, ve o
   geçişin ilerlemesi **taranan parametreye bağlı** olur → tarama sessizce başka
   bir şeyi ölçer. Bu, `03` Bölüm B6'nın ⭐⭐⭐ satırıdır.
2. **Li replikasyonu gölgeleme gerektirmiyor.**
3. ⭐ **İzolasyon:** gölgeleme yoksa, sabit topolojide **zamanla değişen tek şey
   karıştırıcıdır.** Zamana bağlı senaryolarda ortaya çıkan her protokol farkı,
   tanım gereği karıştırıcıya atfedilebilir. Bu bir eksiklik değil, **deney
   tasarımıdır.**

**⚠️ Bunun bedeli ve rapora girecek cümlesi** — *"Bağ kalitesi, karıştırıcı
dışında zamanla değişmez. Bu, gerçek RF ortamına göre bir basitleştirmedir ve
tepkisel protokollerin lehinedir: gerçekte bağ kalitesi kendiliğinden de
dalgalanır ve bu, tazelik gerektiren her yaklaşımın kazancını artırırdı."*

> Yani bu basitleştirme **kendi hipotezimizin aleyhine** çalışıyor. Bu iyi:
> hipotez bu koşulda bile geçerse, gerçekte daha da güçlü olması beklenir.

**Sonraki sürüm için** — Gölgeleme eklenirse, t=0'da **durağan dağılımdan**
çekilmesi zorunludur ve `04-NEDEN-BOYLE.md`ye kayıt düşülür.

---

# KAT 3 · KANAL ERİŞİMİ (MAC)

**Sorumluluk** — Aynı anda konuşmayı yönetmek.

**Ne yapar**
- **Taşıyıcı dinleme:** göndermeden önce kanalı dinle, meşgulse bekle
- **Geri çekilme:** çakışma sonrası rastgele bekleme
- **Onay:** başarılı alım onaylanır; onay gelmezse **zaman aşımı**
- **Yeniden deneme:** sınırlı sayıda

**🔴 Bu kat neden pazarlık dışı**

Li replikasyonundaki 1/7 sayısı ancak şunlar modellenirse çıkar:
- taşıyıcı dinleme
- **girişim menzili > iletim menzili**
- gizli terminal etkisi

Bunlar olmadan zincir kapasitesi 1/7 değil, çok daha iyi çıkar — ve araç
doğrulanmamış olur.

**⭐ Yönlendirme katmanına verdiği tek şey**

```
iletim sonucu = ✅ onaylandı   |   ❌ zaman aşımı
```

Bu iki değer, gözlem penceresindeki **en ucuz ve en önemli** bilgidir.
Sıfır bayta mal olur.

---

## KUYRUKLAR

*(İlk taslakta tanımsızdı — 17 Ağustos'ta eklendi.)*

| Konu | Karar |
|---|---|
| Kapasite | **Sonlu**, paket cinsinden, parametre |
| Dolduğunda | **Kuyruk sonu atma** — gelen paket düşer |
| Sayaç | Kuyruk taşması ayrı bir düşme sebebi olarak sayılır |

**🔴 Neden sonsuz kuyruk olmaz** — Sonsuz kuyrukta karıştırma altında paketler
atılmaz, sadece **bekler.** Teslim oranı yapay olarak yüksek çıkar, gecikme
sınırsız büyür ve **gecikme metriği anlamını yitirir.** Ölçtüğümüz şey ağın
dayanıklılığı değil, belleğin büyüklüğü olur.

**⚠️ Başlangıç koşulu** — t=0'da tüm kuyruklar **boştur.**

## TTL VE DÖNGÜ

*(İlk taslakta yoktu — 17 Ağustos'ta eklendi.)*

Öğrenen bir protokol rota döngüsü üretebilir. TTL olmazsa paket sonsuza kadar
dolaşır ve korunum denkleminde *"uçuşta"* olarak **sonsuza dek asılı kalır.**

| Konu | Karar |
|---|---|
| TTL | Her pakette, her atlamada azalır |
| Sıfırlandığında | Paket **düşer**, ayrı sebep olarak sayılır |
| Teşhis | TTL ile ölen paket oranı · aynı düğümü ikinci kez ziyaret oranı |

> ⚠️ TTL ile ölen paket oranı yüksekse, teslim oranındaki fark protokolün
> kalitesinden değil **döngü üretiminden** geliyor olabilir. Bu sayaç her koşuda
> raporlanır.

---

# KAT 5 · GÖZLEM PENCERESİ 🔴

> ℹ️ **Kat 5, Kat 4'ten önce anlatılıyor — bu bir yazım hatası değil.**
> Şemadaki sıra fizikseldir: gözlem penceresi, simülatör ile yönlendirme
> katmanının **arasında** durur. Yönlendirme, simülatöre pencereden bakar.

**Sorumluluk** — Yönlendirme katmanının **ne göremeyeceğini** garanti etmek.

Tam içerik: `05-GOZLEM-PENCERESI.md`

**Yapısal kural**

```
Yönlendirme  ──►  Görünüm nesnesi   (simülatöre geri referans YOK)
Yönlendirme  ──►  "şu paketi şu komşuya gönder"   (tek eylem)
```

**Zorlama** — Bir test, görünüm nesnesinin yüzeyini tarar. `05`teki listenin
dışında bir alan bulursa **kırılır.**

**Yönlendirmenin yapabileceği tek eylem:** bir paketi bir komşuya vermek.
Başka hiçbir şey.

---

# KAT 4 · YÖNLENDİRME

**Sorumluluk** — Sıradaki atlamayı seçmek.

**Ortak arayüz** — Her protokol aynı **dört** soruyu cevaplar:

| Olay | Protokolün işi |
|---|---|
| Bu düğüm bir paket **üretti** *(kaynak)* | Kime vereyim? |
| Bir paket **geldi**, hedefi ben değilim | Kime vereyim? |
| Bir iletim **sonuçlandı** (✅ onay / ❌ zaman aşımı) | Durumumu nasıl güncelleyeyim? |
| **Zamanlayıcı** çaldı | Ne yayınlayayım? *(kontrol düzlemi)* |

⚠️ İlk iki olay ayrıdır: kaynak düğüm ile aktaran düğüm aynı kararı verse de,
**farklı sayaçlara** yazılır. Karıştırılırsa teslim oranının paydası bozulur.

**Kollar** — Hepsi aynı arayüzü uygular, hepsi **konfigürasyon bayrağıyla**
seçilir.

> ⚠️ **1 Eylül 2026'da YENİDEN YAZILDI** *(K-081)*. Önceki tablo altı
> "Q-Routing / null model / BATMAN-benzeri" kolu sayıyordu; o kurgu
> **artık geçerli değil**.

## 4.1 Faz 1 · rakip protokoller — RFC'ye SADIK

| Kol | Protokol | Aile | Ne gerektirir |
|---|---|---|---|
| **R1** | **AODV** *(RFC 3561)* | reaktif, mesafe-vektör | RREQ / RREP / RERR · hedef sıra numarası · genişleyen halka · yerel onarım |
| **R2** | **OLSR** *(RFC 3626)* | proaktif, bağ-durumu | HELLO / TC · **MPR seçimi** · topoloji tablosu · SPF |
| **R3** | **AOMDV** | reaktif, çok yollu | AODV + `advertised hopcount` · bağ-ayrık yedek yollar |

## 4.2 Faz 2 · özgün protokol

| Kol | | |
|---|---|---|
| **Ö1** | **Özgün protokol** | 🔴 **TASARIM BOŞ — öğrenciden gelecek** *(`06` §5.1)* |
| **Ö1-abl** | Aynı protokol, **bilgi kanalı ablasyonlu** | Aile 3'ün mekanizma kapısı |

🔴 **Ablasyon kolu her zaman bir bayraktır.** Kod düzenlemesiyle üretilen kol,
kaynağından ayırt edilemez — kaybolmuş bir deneydir.

## 4.3 🔄 KONTROL BÜTÇESİ — *"eşit"* DEĞİL, *"raporlanan"*

> ⚠️ **BU MADDE 1 EYLÜL 2026'DA TERSİNE DÖNDÜ.** Eskiden şöyleydi:
> *"Eşit kontrol bütçesi — tüm kollar **aynı beacon aralığı** ve aynı
> bayt/saniye ile koşar (K-009)."*

🔴 **O kural artık geçerli DEĞİL** ve sebebi `03` kural 4'ün revizyonudur:

| | |
|---|---|
| **neden eşitlenemez** | AODV'nin HELLO aralığı **1 s**, OLSR'ınki **2 s** — bu protokollerin **doğasıdır**. Eşitlemek, ölçmek istediğimiz farkı **siler** |
| **literatür ne diyor** | *"Hello aralıklarını aynı tutmayın … yapay olarak eşitlemeyin"* |
| 🔒 **yerine ne var** | Kontrol düzlemi yükü **eşitlenmez, HER KARŞILAŞTIRMAYLA BİRLİKTE RAPORLANIR** — bayt **ve** airtime cinsinden |

⚠️ **Ölçülmüş büyüklük:** kollar arasında kontrol payı **4,0–38,0 kat**
farklılaşabiliyor *(`08` md 25 · pencere · bayt · ortanca **12,6** ·
30 tohum · n = 58)*. Bu fark **bir haksızlık değil, bir bulgudur** — ama
raporlanmadan hiçbir karşılaştırma geçerli değildir *(`06` Bölüm 9,
koşul 3)*.

> 🔴 **B-169** *(2 Eylül 2026, B0.9)*: burada **8,3–17,8 kat** yazıyordu.
> O sayı **3 tohumdan** geliyordu ve `08` md 25 onu **B0.4'te kendisi
> geri aldı** *(`03` kural 2: ≥30 tohum)* — ama bu satır kaynağına atıf
> yapmaya devam ederken **geri alınan değeri** taşıyordu. Üst uç
> **yarıdan fazla** eksik görünüyordu *(17,8 ↔ 38,0)* ve `07`, Faz 1'in
> protokol yazarının okuyacağı belgedir. **Üretici:**
> `python dogrulama/kontrol_payi.py` · `python dogrulama/gecerlilik.py`

## 4.4 🆕 `protokol_kesif` AKIŞI ARTIK KULLANILACAK

Akış **7** *(`protokol_kesif`)* bugüne kadar hiç çekim almadı ve
`rng.HENUZ_KULLANILMAYAN`da beyan edildi. **Faz 1 ile birlikte kullanıma
girecek:**

| protokol | ne çeker |
|---|---|
| **OLSR** | `MAXJITTER` — HELLO/TC yayınlarının anti-çakışma gecikmesi *(HELLO_INTERVAL / 4)* |
| **AODV** | RREQ yeniden deneme geri çekilmesi · genişleyen halka zamanlaması |
| **AOMDV** | AODV ile aynı |

🔴 **Akış PROTOKOL BAŞINA ayrıdır** ve bu zorunludur: bir protokolün kaç
rastgele sayı çektiği diğerini **etkilemez**. Kanal gerçeklemesi zaten
akıştan değil hash'ten geldiği için, eşleştirme **yapısal olarak** korunur.

🔒 **Kullanıma girdiğinde `rng.HENUZ_KULLANILMAYAN`dan ÇIKARILIR** — o liste
*"bildirim ≠ kullanım"* tuzağını zorlayan korumadır ve bayatlarsa boşalır.

---

## 🔴 KOMŞU KEŞFİ — kâhin olma riski buradaydı

*(İlk taslakta belirsizdi — 17 Ağustos'ta netleştirildi.)*

**Bir düğüm komşularını nereden bilir?**

> ❌ Simülatörden okuyarak **değil.**
> ✅ Yalnızca **aldığı beacon paketlerinden.**

| Konu | Karar |
|---|---|
| Beacon | Düzenli aralıkla yayınlanır, **bayta sayılır** |
| Komşuluk | Yakın geçmişte beacon'ı alınan düğüm |
| Beacon kaybı | Karıştırma altında beacon da kaybolur — komşu **görünmez** olur |
| **t=0 başlangıç koşulu** | 🔴 **Hiçbir düğüm hiçbir komşusunu bilmez.** Komşu tablosu boş |

**Neden bu kritik** — Komşu listesi bedava verilirse, karıştırma altında bir
protokol *"o düğüm hâlâ orada"* bilgisini **ücretsiz** almış olur. Gerçek bir
telsizde böyle bir şey yoktur: karıştırma altında komşu **kaybolur.**

⚠️ Bu, v1'de cevabı bilinmeyen *"rakip bilgiyi nereden alıyordu"* sorusunun tam
olarak geçtiği yerdir.

## 🔴 BAYRAK GERÇEKTEN BİR ŞEY YAPIYOR MU

`03` Bölüm B5: *"bildirim ≠ kullanım."* Bir bileşen bildirilmiş, parametre olarak
geçirilmiş, belgelenmiş — **ve hiç çağrılmamış** olabilir.

**Zorunlu test:** her ablasyon bayrağı için, sabit bir senaryoda bayrağın
çevrilmesinin **en az bir kararı değiştirdiğini** gösteren bir test.

> Bu test olmadan yazılan bir ablasyon tablosu, hiç var olmamış bir mekanizmanın
> katkısını raporlayabilir.

---

# TEŞHİS KATMANI

**Sorumluluk** — Her şeyi görmek, hiçbir şeye karışmamak.

| Ne | Ne zaman |
|---|---|
| **Korunum denklemi** | Her koşu sonunda, otomatik |
| Karar yaşı · kayıt eksikliği · ölü bağa gidiş | Sürekli |
| Gerçek bağ kalitesi *(protokolün tahmini değil)* | Sürekli |
| TTL ölümü · döngü oranı · kuyruk taşması | Sürekli |
| Yakınsama kontrolü *(pencere üçe bölünür)* | Koşu sonunda |

### 🔴 Korunum ile ölçüm penceresi AYRI defterlerdir

*(İlk taslakta çakışıyorlardı — 17 Ağustos'ta ayrıldı.)*

| Defter | Kapsam |
|---|---|
| **Korunum denklemi** | 🔵 **Tüm koşu** (0 → 350 s) |
| **Metrikler** | 🟢 **Ölçüm penceresi** (50 → 320 s) |

**Neden ayrı olmak zorunda** — Isınmada üretilip pencerede teslim edilen bir
paket, pencere bazlı bir korunum denklemini **kırar.** Ama ortada hata yoktur.
Korunumu pencereye sıkıştırırsak, her koşuda sahte alarm alırız ve bir süre sonra
alarma bakmayı bırakırız — ki gerçek hata tam o zaman kaçar.

🔴 **Mutlak kural:** teşhis katmanının okuduğu hiçbir değer, yönlendirme
katmanının kararına giremez. Bu iki kanalın karışması tüm sonuçları geçersiz
kılar.

---

# KONFİGÜRASYON VE SONUÇ SÖZLEŞMESİ

```
Konfigürasyon ──► Koşu ──► Sonuç satırı (kendi tam konfigürasyonuyla)
                              │
                              └──► ANINDA diske yaz
```

**Her sonuç satırı taşır:** tüm bayraklar · tohum · **kaynak hash'i** · korunum
sonucu · ölçüm penceresi · yakınsama kontrolü sonucu.

### Kod sürümü nasıl kaydediliyor — git yerine hash

Git komutu çalıştırılmıyor *(`03` Bölüm A, kural 6)*. Bunun yerine koşu anında
**tüm kaynak dosyaların içerik hash'i** hesaplanır ve sonuç satırına yazılır.

> ⭐ Bu aslında git'ten **daha iyi**: git, kaydedilmemiş yerel değişiklikleri
> göremez. Hash görür. *"Bu sayı hangi koddan çıktı"* sorusu, kaydedilmemiş bir
> değişiklik varken bile cevaplanabilir olur.

**Kontrol:** aynı hash'e sahip iki sonuç satırı, aynı tohumda **birebir aynı**
sayıları taşımalıdır. Taşımıyorsa belirlenimcilik kırılmıştır.

**Neden anında yazılır** — Uzun bir matris yarıda kesilirse tamamlanan koşular
kaybolmasın.

**Yollar** depo köküne göre mutlaklanır. Göreli yol, çağıranın çalışma dizinine
yazar.

---

# YAZIM SIRASI

| # | Ne | Bitince ne doğrulanır |
|---|---|---|
| # | Ne | Bitince ne doğrulanır | Durum |
|---|---|---|---|
| 1 | Olay kuyruğu + RNG akışları + konfigürasyon + sonuç yazıcı + **korunum defteri** | Aynı tohum → birebir aynı sonuç · iki protokol aynı kanalı görüyor · kaynak hash'i yazılıyor | ✅ **17 Ağu** |
| 2 | **Topoloji** — konumlar · menzil · bağlantılı bileşen | S0'da her kaynak–hedef çifti ulaşılabilir | ✅ **17 Ağu** |
| 3 | Trafik katmanı + kuyruklar + TTL + boşaltma | Boşaltma çalışıyor · TTL ölümü sayılıyor · korunum tutuyor | ✅ **17 Ağu** |
| 4 | Radyo katmanı *(SINR · karıştırıcı · hata olasılığı)* | Analitik kontroller ✅ · karıştırıcı kalibrasyonu ✅ | ✅ **17 Ağu** |
| 5 | MAC katmanı | ⭐ **Li replikasyonu 1/6,29 vs Li 1/7** 🚪 | ✅ **17 Ağu** |
| 6 | Gözlem penceresi + testi + komşu keşfi | Pencere dışına uzanma kırılıyor ✅ · t=0'da komşu tablosu boş ✅ | ✅ **18 Ağu** |
| 7 | Rakip kollar | Ayarlama *(ayrılmış tohumlarda)* | ⬜ **Aile 1** |
| 8 | Öğrenen kollar + null model + bayrak testleri | Mekanizma kapısı · her bayrak bir kararı değiştiriyor | ⬜ **Aile 2** |

> ⚠️ **2. adım sonradan eklendi.** İlk sırada trafik katmanı radyodan önce
> geliyordu — ama kaynak–hedef çiftleri yalnızca *bağlı* düğümlerden seçildiği
> için trafik, menzil bilgisine muhtaç. Bu hata ancak kod yazarken görüldü.
> *(K-016)*

> ⚠️ **Korunum denklemi ikinci sırada, tesadüf değil.** Onsuz yazılan her katman,
> sessizce paket kaybediyor olabilir ve bunu haftalar sonra fark ederiz.

---

# HESAP BÜTÇESİ

**Ana matris** *(Aile 1 + 2)*

```
6 kol × 6 senaryo × 3 trafik seviyesi × 30 tohum = 3240 koşu
```

Koşu başına ~15 s tahmini → 10 çekirdekte **~81 dakika**

**Ayarlama koşuları** *(mühürden önce, ayrılmış tohumlarda)*

```
rakip parametreleri × 6 senaryo × 10 ayarlama tohumu  ≈  300–500 koşu  →  ~10 dk
```

🔴 **30 dakikayı aştığı için, koşmadan önce süre tahmini yazdırılacak ve izin
istenecektir** *(`03` Bölüm A, kural 7)*.

**Karakterizasyon taraması** *(H1.2 — dirsek)*

```
2 rakip kol × 8 güç seviyesi × 30 tohum = 480 koşu  →  ~12 dakika
```

> Hesap bu projenin darboğazı **değil.** Darboğaz, kodu yazma ve sonucu anlama
> süresidir.
