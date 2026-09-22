# 02 — DOĞRULANMIŞ KAYNAKLAR

> ## ✅ GÜNCEL — 10 Eylül 2026
> Kaynak doğrulamaları koddan bağımsızdır. Rapora girecek yeni bir iddia önce
> buraya doğrulanmış kaynağıyla yazılır. **§S — doğrulanmayı bekleyen kaynak
> soruları** (Rician K, 802.11b sabitleri, karıştırıcıların saha davranışı,
> yere toplama trafiği) 10 Eylül'de eklendi.


> ⭐ **BU BELGE PROJENİN EN PAHALI VARLIKLARINDAN BİRİDİR.**
> Buradaki her kaynak **öğrenci tarafından tek tek açılıp okunmuş** ve
> iddianın gerçekten desteklenip desteklenmediği kontrol edilmiştir.
> Bu iş yeniden yapılmasın diye taşınıyor.

> 🔴 **KURAL:** bulunamayan bir atıf **rapora giremez.** İddia ya kaldırılır
> ya da doğrulanmış başka bir kaynakla değiştirilir.

**Durum işaretleri:** ✅ doğrulandı (kaynak var *ve* iddiayı destekliyor) ·
⚠️ kısmen (kaynak var, iddiayı tam desteklemiyor) · 🔴 bulunamadı

---

## A. PROBLEM MOTİVASYONU

| # | İddia | Kaynak | Durum | Not |
|---|---|---|---|---|
| **A1** | Ukrayna'da aylık ~10.000 İHA kaybı; her 10 km cepheye ≥1 büyük EH sistemi | RUSI, *"Meatgrinder: Russian Tactics in the Second Year of Its Invasion of Ukraine"*, Watling & Reynolds, 19 May 2023, s.4 ¶2 · `static.rusi.org/403-SR-Russian-Tactics-web-final.pdf` | ✅ | 🟡 Yazarlar kesin olmadığını **kendileri** belirtiyor. Yalnızca büyüklük mertebesi |
| **A2** | FPV %60–80 | Col. Vytis Andreika, *Military Review*, "Lessons from Ukraine", s.9 | ⚠️ | 🔴 **ANLAM KAYMASI:** kaynak *"both sides **jammed** 60–80 percent of all FPVs operated"* diyor. **"Hedefe ulaşamadı" DEĞİL**, ve "her iki taraf" |
| **A5a** | İHA hızları 30–400 km/h | Mahalakshmi & Ranjitha Kumari, IJRTE 8(5), s.1 | ✅ | arXiv 2108.13154 **doğrulanamadı**, bununla değiştirildi |
| **A5b** | ⭐ Çok atlamalı zincirde verim düşüşü | Li, Blake, De Couto, Lee, Morris, *"Capacity of Ad Hoc Wireless Networks"*, §3.2 | ✅ | **Kesin sayılar:** ideal MAC zincir kullanımı **1/3** · ideal zincir tek atlamanın **1/4**'ü · 802.11 gerçekte **1/7**'si |
| **A6** | ⭐ Tek kanallı mesh (BATMAN-adv) karıştırma altında bağlantıyı tamamen yitiriyor | Deo, Schuß, Baddeley, Boano, *"Robust Wi-Fi Mesh Networking with SPIDERMAN"*, TU Graz | ✅ | **Deneysel** kanıt |

---

## B. LİTERATÜR BOŞLUĞU

| # | İddia | Kaynak | Durum |
|---|---|---|---|
| **B5** | ⭐ RL anti-jamming politikaları durağan ortama göre optimize olur; ortam/karıştırma deseni değişince **yeniden eğitim gerekir** | Hu, Shao, Qian, Du, Li, Lin, Wang, *"Meta-Reinforcement Learning in Time-Varying UAV Communications: Adaptive Anti-Jamming Channel Selection"*, Introduction | ✅ |
| **B6** | ⭐ **13 Q-öğrenme tabanlı FANET yönlendirme protokolü**; tablo tabanlı yöntemler küçük FANET'ler için uygun, büyük ağlarda boyut laneti | *"Reinforcement Learning-Based Routing Protocols in Flying Ad Hoc Networks: A Survey"*, **Mathematics 2022, 10, 3017**, s.49 + Table 26 | ✅ |
| **B7** | ⭐⭐ **Table 26: mevcut ödül fonksiyonlarının HİÇBİRİNDE girişim/karıştırma terimi yok** | Aynı derleme, Table 26, s.49 | 🔴 **1 Eyl 2026: YENİDEN DOĞRULANAMADI** — aşağı bak |
| **B8** | FEQ-routing-SA öğrenme oranını **düğüm hızına**, PARRoT iskonto çarpanını **bağlantı ömrüne** göre uyarlıyor | Aynı derleme | ✅ |
| **B9** | DRL yaklaşımları yüksek hesaplama maliyeti gerektirir | Termehchi vd.; Jiao vd.; Hu vd. | ✅ |

### ⭐ Table 26'nın verdiği somut boşluk

| Protokol | Ödül fonksiyonu |
|---|---|
| QTAR | gecikme, enerji, hız |
| QMR | gecikme, enerji |
| QGeo | paket seyahat hızı |
| QLGR | yük kapasitesi, bağlantı kalitesi |
| FEQ-routing-SA | iletim (…) |

**Hiçbirinde girişim terimi yok.**

> ## 🔴 1 EYLÜL 2026 — B6/B7 YENİDEN DOĞRULANAMADI
>
> 20 dosyalık yeni literatür taraması aynı derlemeye ulaşmayı denedi ve
> **kapanış notuna şunu yazdı:**
>
> > *"**MDPI tam metnine erişim kısıtlı olduğundan** Lansky vd. (2022)
> > derlemesinin protokol listesi **arama özeti ve metadata üzerinden**
> > doğrulanmıştır."*
>
> Ayrıca **protokol sayısı uyuşmuyor:**
>
> | kaynak | sayı | üyelik farkı |
> |---|---|---|
> | B6 *(bu belge)* | **13** | TARRAQ var |
> | yeni tarama, dosya 17 §2 | **14** | DQN-VR + TQNGPSR var, TARRAQ yok |
>
> ⚖️ **BU, B7'Yİ ÇÜRÜTMEZ.** Yukarıdaki 5 satırlık tablo bir zaman
> erişildiğinin kanıtıdır — uydurulmuş olsaydı satırlar olmazdı.
> Doğru ifade: **iddia bugün yeniden üretilemiyor.** Y14: *"mühürlenecek
> bir belgedeki sayı, yeniden koşulmadan mühürlenemez."*
>
> 🔒 **KARAR (öğrenci, 1 Eylül 2026):** özgünlük iddiası artık Table 26'ya
> değil, yeni taramanın **kendi matrisine** dayandırılır — 11 protokol,
> *"Açık Jamming"* sütunu **9'unda `Hayır`**. Yeniden üretilebilir.
> 🔴 **B7 silinmiyor**, durumu *"✅"*den *"yeniden doğrulanamadı"*ya
> düşürülüyor. Bir kaynağı çıkarmak, çıkarıldığını yazmadan yapılmaz.

---

## C. YÖNTEM KAYNAKLARI

| # | Ne için | Kaynak | Durum |
|---|---|---|---|
| **C4** | Q-Routing (RL yönlendirmenin temeli) | **Boyan & Littman, 1994** | ✅ Öğrenci doğruladı |
| C3 | ETX metriği | De Couto vd. | ⬜ *(A5b'nin ortak yazarı — muhtemelen aynı grup)* |
| C2 | Gauss-Markov mobilite | Liang & Haas | ⬜ |
| C5 | Gölgeleme korelasyonu | Gudmundson, Electronics Letters | ⬜ |
| **C6** | ⭐ Random Waypoint hız çürümesi | **Yoon, Liu & Noble 2003, *"Random Waypoint Considered Harmful"*** | ✅ ⚠️ Bir mobilite modeli kullanılacaksa bu kaynak **önce okunmalıdır** — ortalama hız durağan bir değere yakınsamaz ve bu sessizce başka bir şeyi ölçtürür |

---

## D. ⭐ ÖNCÜL ÇALIŞMA — ve öğrencinin yakaladığı hata

| Kaynak | Durum |
|---|---|
| Vu Khanh Quy, Nguyen Tien Ban, Nguyen Dinh Han, *"A High-Performance Routing Protocol for Multimedia Applications in MANETs"*, **Journal of Communications 14(4), Nisan 2019** | ✅ |

### 🔴 Yapay zekânın hatası, öğrencinin düzeltmesi

Yapay zekâ, protokolün adındaki **"Q"** harfinden Q-learning çıkarımı yaptı ve
bunu *"doğrudan bizim alanımızda öncül çalışma"* diye sundu. **Yanlıştı.**
Öğrenci makaleyi açıp okudu:

> Makale AODV'yi multimedya için **bant genişliği ve gecikme** QoS ölçütleriyle
> genişletiyor. PDF'de Q-learning, Q-tablo, ödül fonksiyonu veya ε-greedy
> **yok**. Rota seçimi `Cost_Delay_Bandwidth` minimizasyonuna dayanıyor.

**Bu makaleden ÇIKARILMAMASI gerekenler:** Q-learning algoritmasıdır ❌ ·
Q-tablosu vardır ❌ · ödül fonksiyonu vardır ❌ · ε-greedy kullanır ❌ ·
karıştırıcı altında test edilmiştir ❌ · paket/saniye değeri verilmiştir ❌

**Doğru konumlandırma:** *"QoS-aware AODV routing under varying mobility"*.

> ⚖️ **Bu epizot rapora girer.** Yapay zekânın bir hatasını öğrencinin kaynağı
> açıp okuyarak düzeltmesi, fikir sahipliği kriterinin **doğrudan kanıtıdır.**

### D1 — Replikasyon parametreleri (Table I'den, doğrulanmış)

| Parametre | Değer |
|---|---|
| Düğüm sayısı | 200 · Alan 1500×1500 m · Menzil 250 m |
| Mobilite | Random Waypoint, hız ∈ [0, Vmax], Vmax = 2…20 m/s |
| Trafik | CBR, 50 bağlantı, 1024 B, UDP · Bant 1 Mbit/s · Süre 500 s |
| Ortam | NS-2 v2.34 · Karşılaştırılan: Q-AODV, AODV, DSR |
| AODV eğrisi | 2 m/s'de ~%98 → 20 m/s'de ~%65 |

⚠️ **Paket/saniye Table I'de YOK.** Öğrenci notu: *"PDF'nin desteklemediği bir
değer çıkarılmamalıdır."*

---

## E. 🔴 RAPORDAN ÇIKARILMIŞ İDDİALAR — geri getirilmez

| İddia | Neden çıkarıldı |
|---|---|
| "AODV/OLSR/BATMAN karıştırma altında <%50 PDR" | Birincil kaynak **yok**. Araştırma sorusuna çevrildi |
| "Nature Scientific Reports 2026" RL boşluk analizi | **Bulunamadı.** Yerine B5 + B6 geçti |
| "FedRoute PDR %6,5 / gecikme %14,5" | Künye **hiç verilmemişti** |
| "Q-AODV bir Q-learning protokolüdür" | ❌ Makale okundu, çürütüldü (§D) |

---

## F. ÖZET

| | Sayı |
|---|---|
| ✅ Doğrulandı | 10 |
| ⚠️ Anlam kayması | 1 (A2) |
| 🔴 Bulunamadı → iddia kaldırıldı | 3 |
| ⬜ Ertelendi (kritik değil) | 4 |
| ⭐ Beklenmedik yeni bulgu | 4 (Li vd. · SPIDERMAN · Hu vd. · Mathematics derlemesi) |

**Doğrulama üç iddiayı çıkardı ve dört yenisini getirdi.** ⭐ Ve getirilenlerin
ikisi doğrudan yeni imkân açtı: **Li vd.** ölçüm ortamını doğrulamak için kesin
sayılar veriyor, **Table 26** ise savunulabilir bir özgünlük boşluğu.

> ⚖️ **Bu tablo bir kayıp listesi değil, bir yöntem kanıtıdır.** Kaynaklarını
> tek tek açıp üçünü kendi raporundan çıkaran bir öğrenci, jüri karşısında
> hiç iddia çıkarmamış bir öğrenciden güçlüdür.

---

## G. ⚠️ `research.md` HAKKINDA

Bu tablonun kaynağı, bir **üretken yapay zekâ tarafından hazırlanmış** bir
fizibilite/literatür raporudur. O rapor **kısmen çürütülmüştür**: yukarıdaki
tablo onun *doğrulanmış alt kümesidir.*

> 🔴 **KURAL:** üretken yapay zekânın verdiği hiçbir atıf, kaynağı fiilen
> açılıp iddia görülmeden kullanılamaz. §E'deki dört madde tam olarak bu
> kontrolde düştü — biri (§D) **uydurma değil, yanlış okumaydı** ve yalnızca
> makaleyi açmakla yakalandı.

> ⭐ **Öğrencinin ham, düzenlenmemiş doğrulama notları saklanmalıdır.** Bir
> kaynağın gerçekten okunduğunun kanıtı, düzenlenmiş bir özet değil, o ham
> nottur — ve fikir sahipliği kriterinde doğrudan işe yarar.

---

# H. 🆕 İKİNCİ LİTERATÜR TARAMASI — 31 Ağustos 2026

Öğrenci ikinci ve çok daha geniş bir tarama tamamladı:
**`protokol_kaynaklari/literatur_taramasi_2026-08-31/` — 20 dosya, 5 271 satır.**

| ne getirdi | nerede işlendi |
|---|---|
| **Boşluk A** — SJR'ye bağlı PDR/E2E verisi yok *(doğrulanmış)* | `01` §2.2 · `10` §5 |
| **Boşluk B** — RF karıştırma altında rota kurtarma gecikmesi yok | `01` §2.2 · `10` §5 |
| Aracın soyutlama seviyesinin **bağımsız onayı** *(Seviye 3 BER→PER, chunk PER, toplamsal girişim)* | `10` §6.1 |
| **Kâhin yasağının** dış kaynaklı gerekçesi | `10` §6.2 |
| **Metrik asgarisi** — PDR+PSR, D̄+p95, O_pkt+NRL, üç kopma sayacı, Δ+COR | `10` §7c Y-4 |
| **RFC parametre tabloları** *(AODV 3561 · OLSR 3626)* | 🟢 **8 Eylül 2026: BİRİNCİL BELGELER AÇILDI → §R.** Artık ikinci el değil |
| **Deney tasarımı iskeleti** — faktöriyel eksenler | `06` |
| **Sanity doğrulama testleri** *(4 adet)* | Faz 1'in kabul ölçütü |
| 🔴 **Literatürün kendi ödül kodunda KÂHİN** | `10` §7c Y-1 |

⚠️ **Bu tarama `02`nin yerini almaz.** `02` *"tek tek açılıp okunmuş
kaynaklar"*dır; yeni tarama ikinci el derlemedir ve künyelerinin bir kısmı
kendi içinde *"doğrulanamadı"* diye işaretli. 🔴 **Rapora girecek her sayı
için birincil kaynak açılmalıdır.**

🔴 **Ve tarama okunurken bir ders çıktı** *(K-080)*: ilk okumada 5 271
satırın yalnızca **%62'si** okunmuştu ve okunmayan dosyalar için de
"iddia sayısı" yazılmıştı. **Bir okuma iddiası da bir ölçümdür ve
üreticisi vardır.**

---

## R. RFC PARAMETRE TABLOLARI — 8 Eylül 2026'da açıldı

> 🔴 **NEDEN GEÇ AÇILDILAR VE NEDEN ÖNEMLİ.** Bu iki RFC, 8 Eylül'e kadar
> yalnız §"yeni tarama"da *"Faz 1'in girdisi"* diye duruyordu — yani ikinci
> el bir derlemeden geliyorlardı, birincil belge açılmamıştı. Oysa aletin
> **üç ayrı kararı** onlara dayanıyordu:
>
> | karar | çapa | kayıt |
> |---|---|---|
> | çalkantı sayısı Θ'nın paydası | OLSR `TOP_HOLD_TIME` | K-101 |
> | bağlantılılık kısıtının zaman anlamı | AODV `ACTIVE_ROUTE_TIMEOUT` | K-103 |
> | evre metriklerinin ölçüm kafesi | AODV `HELLO_INTERVAL` + OLSR `TOP_HOLD_TIME` | K-105 |
>
> Üçü de doğrulanmamış bir kaynağa dayanıyordu. Artık dayanmıyor.

### R1 · AODV — RFC 3561 ✅

**Künye:** Perkins, C., Belding-Royer, E., Das, S., *"Ad hoc On-Demand
Distance Vector (AODV) Routing"*, RFC 3561, **Temmuz 2003**, kategori:
**Experimental**. · `https://www.rfc-editor.org/rfc/rfc3561.txt`

Bölüm 10, *"Configuration Parameters"* — belgenin bastığı değerler:

| parametre | değer (belgede yazdığı gibi) |
|---|---|
| `ACTIVE_ROUTE_TIMEOUT` | **3,000 Milliseconds** |
| `HELLO_INTERVAL` | **1,000 Milliseconds** |
| `ALLOWED_HELLO_LOSS` | 2 |
| `NET_DIAMETER` | 35 |
| `NODE_TRAVERSAL_TIME` | 40 milliseconds |
| `RREQ_RETRIES` | 2 |
| `MY_ROUTE_TIMEOUT` | 2 × `ACTIVE_ROUTE_TIMEOUT` |
| `DELETE_PERIOD` | K × max(`ACTIVE_ROUTE_TIMEOUT`, `HELLO_INTERVAL`), önerilen K = 5 |

### R2 · OLSR — RFC 3626 ✅

**Künye:** Clausen, T., Jacquet, P. (Project Hipercom, INRIA), *"Optimized
Link State Routing Protocol (OLSR)"*, RFC 3626, **Ekim 2003**, kategori:
**Experimental**. · `https://www.rfc-editor.org/rfc/rfc3626.txt`

Bölüm 18, *"Proposed Values for Constants"*:

| parametre | değer (belgede yazdığı gibi) |
|---|---|
| `HELLO_INTERVAL` | **2 seconds** |
| `REFRESH_INTERVAL` | 2 seconds |
| `TC_INTERVAL` | **5 seconds** |
| `NEIGHB_HOLD_TIME` | 3 × `REFRESH_INTERVAL` *(= 6 s)* |
| `TOP_HOLD_TIME` | **3 × `TC_INTERVAL`** *(= 15 s)* |
| `DUP_HOLD_TIME` | 30 seconds |
| `MID_HOLD_TIME` | 3 × `MID_INTERVAL` |

🔒 **Θ'nın paydası (15 s) doğrulandı** — türetme belgede açık: 3 × 5 s.
🔒 **Evre kafesinin iki sabiti doğrulandı**: 1 s ve 15 s.

#### R2.1 · Birincil belge İKİNCİ KEZ açıldı — biçimler ve kalan sabitler (19 Eylül 2026)

OLSR yazılmadan önce, AODV'de olduğu gibi *"RFC'ye sadık"* iddiasını bayt
bayt ölçülebilir kılmak için. Ham metin tarayıcıda okundu
(`https://www.rfc-editor.org/rfc/rfc3626.txt`, 161 265 karakter).

**Biçimler (§3.3 · §6.1 · §9.1)** — genişlikler bit olarak, 32 bitlik
kelimelere hizalı:

| yapı | alanlar | bayt |
|---|---|---|
| paket başlığı | Packet Length 16 · Packet Sequence Number 16 | **4** |
| mesaj başlığı | Message Type 8 · Vtime 8 · Message Size 16 · Originator Address 32 · Time To Live 8 · Hop Count 8 · Message Sequence Number 16 | **12** |
| HELLO gövdesi | Reserved **16** · Htime 8 · Willingness 8 — sonra her bağ kodu bloğu için: Link Code 8 · Reserved 8 · Link Message Size 16 · Neighbor Interface Address 32 × n | **4 + Σ(4 + 4n)** |
| TC gövdesi | ANSN 16 · Reserved 16 · Advertised Neighbor Main Address 32 × n | **4 + 4n** |

🔒 **Öz-sınama sayısı belgenin kendisinde:** §3.3.1 *"Packet Length < 16
olan paket sessizce atılır"* der — 16 = paket başlığı (4) + mesaj başlığı
(12). Biçim tabloları bu toplama oturmak zorunda.

**Kalan sabitler (§18)** — ön-kayıt `06` §4.2 bunları *"henüz işlenmedi"*
diye taşıyordu; artık birincil belgeden:

| sabit | değer |
|---|---|
| `C` (Vtime/Htime ölçeği) | 1/16 s |
| `MID_INTERVAL` · `HNA_INTERVAL` | `TC_INTERVAL` |
| `MID_HOLD_TIME` · `HNA_HOLD_TIME` | 3 × ilgili aralık |
| mesaj tipleri | HELLO 1 · TC 2 · MID 3 · HNA 4 |
| bağ tipleri | UNSPEC 0 · ASYM 1 · SYM 2 · LOST 3 |
| komşu tipleri | NOT 0 · SYM 1 · MPR 2 |
| **`WILL_DEFAULT`** | **3** (aralık 0–7; NEVER 0 · LOW 1 · HIGH 6 · ALWAYS 7) |
| `TC_REDUNDANCY` · `MPR_COVERAGE` | 0 · 1 |
| **`MAXJITTER`** | **`HELLO_INTERVAL / 4`** = 0,5 s |
| histerezis (§18.7) | HIGH 0,8 · LOW 0,3 · SCALING 0,5 |

**Vtime/Htime kodlaması (§18.3):** `değer = C·(1 + a/16)·2^b`, `a` üst dört
bit, `b` alt dört bit, yukarı yuvarlanır. 🔒 Belge **dört çözülmüş örnek**
veriyor ve bunlar kodlayıcının hazır sınav vektörleri: 2 s → (0, 5) ·
6 s → (8, 6) · 15 s → (14, 7) · 30 s → (14, 8). Dördü de formülle elle
doğrulandı.

**İsteğe bağlı iki özellik — anahtar sözcükleriyle:**

| özellik | bölüm | RFC'nin sözü | ne yapar |
|---|---|---|---|
| bağ histerezisi | §14 | *"SHOULD be considered"* | OLSR'ın **kendi bağ kalitesi süzgeci**: patlamalı kayba ve geçici bağlara karşı |
| bağ katmanı bildirimi | §13 | *"MAY"* | MAC onayı gelmezse bağı kayıp say |

#### R2.2 · 🔴 ÖZETLEYİCİ BİR ARAÇ BİRİNCİL KAYNAK DEĞİLDİR — üç hata

Belge önce bir web getirme aracıyla okundu. Araç birebir alıntıyı reddetti,
olguları özetledi — ve özetinde **üç hata** vardı; üçü de ham metinle
karşılaştırılınca yakalandı:

| özetin dediği | birincil belge |
|---|---|
| paket başlığı "16 bayt" | **4 bayt** (16, *en küçük geçerli paket*tir) |
| HELLO'nun Reserved alanı "13 bit" | **16 bit** — 13 + 8 + 8 = 29, kelimeye hizalanmaz |
| `MAXJITTER` "0,04 s" | **`HELLO_INTERVAL / 4` = 0,5 s** |

🔒 İlk ikisi iç tutarlılık sınavıyla bile yakalanıyordu. Ders: bayt bayt
sadakat iddia edilen bir şartname **ham metinden** okunur; bir özet ne kadar
düzgün görünürse görünsün birincil kaynak değildir. `03` §2 ilke 1'in
kaynak tarafındaki karşılığı.

### R3 · 🔴 AÇMANIN ORTAYA ÇIKARDIĞI ŞEY — bir STRAW-MAN RİSKİ

İki RFC yan yana konunca şu görüldü ve **kimse aramıyordu**:

| | AODV | OLSR |
|---|---|---|
| komşu yenileme aralığı | **1 s** | **2 s** |

Simülatörün beacon'ı **koşum düzeyinde sabittir** (`kosu.py` onu tek bir
konfig alanından çizelgeler) ve bugün **1 s**. Yani:

- **AODV** kendi RFC hızında koşuyor — sorun yok.
- 🔴 **OLSR, RFC'sinin iki katı hızda beacon yayınlıyor.** İki yönlü sonucu
  var ve ikisi zıt yöne çekiyor:
  · komşu bilgisi RFC'den **daha taze** → PDR'de **avantaj**
  · kontrol yükü **iki katı** → `nrl_*` metriklerinde **dezavantaj**

🔒 **Bu, `03` kural 4'ün yasakladığı şeyin adayıdır** *(taban çizgisi kurulum
yüzünden zayıflatılamaz)* — ve K-101'de OLSR için bulunan straw-man'in
**aynı sınıftan ikinci örneğidir**. Orada topoloji bilgisi kullanılmadan
bayatlıyordu; burada kontrol yükü şişiyor.

⚠️ **AMA HENÜZ ÖLÇÜLMEDİ, dolayısıyla iddia edilmiyor.** İki şey doğru
olabilir: (a) beacon ortak bir alt yapıdır, bütün kollarda aynıdır ve
karşılaştırmada ortak-mod olarak sadeleşir; (b) `nrl_*` bir SONUÇ metriğidir
ve OLSR'ın payını iki katına çıkarmak onu haksız yere kötü gösterir.

🔒 **Ayrıştıran ölçüm hazır:** `beacon_gonderilen` ayrı bir sayaçtır, yani
beacon'ın `nrl_*`e katkısı sonuç satırından **çıkarılabilir**. Faz 3'te
taban çizgileri koşarken bu ölçülür ve şu üçünden biri yapılır: beacon
aralığını protokole bıraktırmak · ortak-mod terimi raporda ayırmak · ya da
etkinin ölçülüp ihmal edilebilir çıktığını beyan etmek.

**Borç kaydı:** `beacon_araligi_s` bu yüzden `SINANMAMIS` kalıyor. Değerinin
kökeni artık belli (AODV `HELLO_INTERVAL`), ama *"bu değer hiçbir taban
çizgisini zayıflatmıyor"* iddiası ÖLÇÜLMEDİ — ve bu proje ölçülmemiş bir
şeye "kaynak" demiyor.

---

### R4 · AOMDV — Marina & Das, ICNP 2001 ✅ (19 Eylül 2026)

🔴 **Bu girdi 19 Eylül'e kadar HİÇ YOKTU** — üçüncü taban protokolün birincil
kaynağı defterde değildi. AOMDV'nin bir RFC'si yok; tanımı bir makalede.

**Künye:** M. K. Marina, S. R. Das, *"On-demand Multipath Distance Vector
Routing in Ad Hoc Networks"*, Proc. IEEE ICNP, s. 14–23, 2001. Genişletilmiş
dergi sürümü: *Wireless Communications and Mobile Computing* 6(7):969–988,
2006, DOI 10.1002/wcm.432 (ücretli; künyesi Edinburgh Üniversitesi kurum
sayfasından doğrulandı).

**Depodaki kopya ve denetimleri:** `protokol_kaynaklari/` — ortak yazarın
kendi sayfasından, öğrenci izniyle; tamamı okundu, gerçeklik ve istem
enjeksiyonu denetimleri `protokol_kaynaklari/README.md`de.

**Okunan — ve nasıl:**

| içerik | kaynak | nasıl okundu |
|---|---|---|
| rota güncelleme kuralı (10 satır) | Şekil 3 | 🔴 metinde BOZUK (Type 3 bit eşlem yazı tipi) → öğrencinin ekran görüntüsünden, birebir döküm README'de |
| reklam edilen atlama sayısı = yolların atlama sayısının EN BÜYÜĞÜ, ilan gönderilirken güncellenir | §3.1 düz yazı | metinden |
| RREQ'te `firsthop` alanı; tekrar kopyalar atılmaz, yeni bir düğüm-ayrık yol veriyorsa güncelleme kuralı çağrılır; yol yoksa yalnız ilk kopya iletilir | §3.2 düz yazı | metinden |
| hedef, farklı komşulardan gelen en fazla **k** RREQ kopyasına cevap verir, ilk atlamadan bağımsız | §3.2 | metinden |
| **k = 3** | §3.2 | 🔴 metinde BOZUK → öğrencinin ekran görüntüsünden |
| bağ-ayrık yol (düğüm-ayrık değil) seçildi; bir bayrakla düğüm-ayrığa çevrilebilir | §3.2 | metinden |
| bağ katmanı geri bildirimi kopmayı algılamada kullanıldı | §4.1 | metinden |

⚠️ **ICNP sürümünde OLMAYANLAR:** rota bakımı (bir yol kopunca ne yapılır ·
RERR), verinin hangi yoldan gönderileceği, yol başına zaman aşımları. Makale
*"yeni keşif yalnız BÜTÜN yollar kopunca gerekir"* der, ama mekanizmayı ayrı
bir bölümde vermez.

#### R4.1 · 🔴 ns-2'deki AOMDV YAZARLARIN KODU DEĞİL — bir varsayım çürüdü

Boşlukları doldurmak için *"yazarların ns-2 gerçeklemesi"* önerilmişti ve bu
**doğrulanmamış bir varsayımdı**. Kontrol edildi (19 Eylül 2026):

- ns-2.35'in `aomdv/aomdv.cc` başlığı: *"Copyright (c) 2008, Marcello Caleffi
  … developed at DIET, University of Naples Federico II"* (GPL v2).
- Caleffi'nin kendi sayfası: *"I've updated an old AOMDV … code for Ns-2"* —
  eski kodun kökeni belirtilmemiş.
- Kod, makalede OLMAYAN iki parametre getiriyor: `aomdv_max_paths_` ve
  `aomdv_prim_alt_path_len_diff_`.

🔒 **Sonuç:** ns-2'nin AOMDV'si bir **üçüncü taraf gerçeklemesidir**, AOMDV'nin
tanımı değil. Literatürdeki AOMDV karşılaştırmalarının çoğu onu kullandığı
için topluluğun "fiilî" AOMDV'si odur — ama ondan alınan her seçim BAŞKA
BİRİNİN seçimidir ve öyle beyan edilmelidir.

**Boşluklar için seçenekler — karar öğrencinin, AOMDV yazılmadan önce:**

| # | yol | bedeli |
|---|---|---|
| a | makale + makalenin değiştirmediği her şeyde **RFC 3561** (makalenin kendi ilkesi: *"altta yatan AODV'nin bilgisini mümkün olduğunca kullan"*) | birkaç belirtilmemiş seçim (veri hangi yoldan gider) beyanla yapılır; literatürdeki ns-2 sonuçlarından biraz farklı çıkabilir |
| b | makale + ns-2.35'in (Caleffi) seçimleri | üçüncü tarafın iki parametresini ithal eder |
| c | dergi sürümü (2006) — ücretli; okul/TÜBİTAK erişimiyle ya da yazardan istenerek | boşlukları yetkili kaynaktan kapatır; erişim belirsiz |

✅ **KARAR (öğrenci, 22 Eylül 2026): a** — makale + RFC 3561. ns-2'nin
seçimleri İTHAL EDİLMEZ; belirtilmemiş her seçim gerçeklemenin başlığında
beyan edilir.

⚠️ **AODV'den MİRAS:** AOMDV, AODV'nin bir uzantısıdır. Makalede açıkça
değiştirilmeyen her sabit ve kural için RFC 3561 geçerli sayılacak (R1).

## S. DOĞRULANMAYI BEKLEYEN KAYNAK SORULARI — 10 Eylül 2026

Bunlar henüz doğrulanmış kaynak değildir; her biri bir tasarım kararını ya da
bir köken kaydını taşıyor. Cevaplanan soru yukarıdaki bölümlere künyesiyle
işlenir.

| # | soru | neden önemli | bağlam |
|---|---|---|---|
| **S1** | Rician K = 6 dB, baskın saçılım yer yansımasıysa Γ ≈ 0,50 demektir (`K_dB = −20·log₁₀Γ`). Bu hava-hava geometride (2,4 GHz, ölçekli irtifa) yer yansıma katsayısı 0,50 mertebesinde mi? | K derece dağılımını belirgin biçimde oynatıyor; projenin kendi ölçütü K ≈ 8–10 dB'yi işaret ediyor. **Öğrenci kararı: kaynak doğrulanacak** | K-110 EK-7 · `07` §04 |
| **S2** | 802.11b MAC/PHY sabitleri: slot, SIFS, CW aralığı, önbelge süresi, bit hızları, ACK boyu — IEEE 802.11-2016 | tek bir doğrulama bu öbeği `SINANMAMIS`tan `KAYNAK`a taşır | köken defteri |
| **S3** | Karıştırıcıların saha davranışı: platform (sabit yer, araç, hava), hareket hızı ve düzeni, yayın/sessizlik düzeni, aynı bölgede eşzamanlı sayı, etki alanı | **öğrenci kararı:** çoklu ve hareketli karıştırıcı modeli saha davranışına paralel kurulacak. 🟡 **Kısmen cevaplandı (10 Eylül):** öğrencinin sağladığı sentez `protokol_kaynaklari/literatur_taramasi_2026-08-31/02_proje_özeli_literatür/taktik-iha-mesh-karistirici-saha-davranislari.md` nitel çerçeveyi veriyor — sinyal sınıfı × platform × yayın düzeni, dört senaryo ailesi, gözlemle–karıştır–sus–yer değiştir durum makinesi. Nicel saha verisi (hız, güç, süreler, koordinasyon) açık literatürde sınırlı; bu dosyanın kendi beyanı. Künyeleri (ör. Pirayesh & Zeng 2022; Xu, Trappe vd. 2005; Xu, Zhang & Lu 2023) burada tek tek açılıp doğrulanmadı. A1 (her 10 km cepheye ≥ 1 büyük EH sistemi) yalnız büyüklük mertebesi verir | `07` §05.3 · §18 Y5 |
| **S4** | Taktik İHA sürüsünde yere toplama trafiği: telemetri paket hızı ve boyu, sensör akışları, geçit mimarisi (yer istasyonu ↔ röle İHA) | yere toplama deseninin yük ve geçit kararları | `07` §06 |
| **S5** | Kontrol mesajı kapsülleme boyutları: 802.11 MAC başlığı 24 B + FCS 4 B (IEEE 802.11-2016 §9), LLC/SNAP 8 B (RFC 1042), IPv4 20 B (RFC 791), UDP 8 B (RFC 768) | `13` §03.1 künyeleri veriyor ama burada doğrulanmadı; kapsülleme sabiti `SINANMAMIS` | `13` §03.1 |
