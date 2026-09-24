# 06 · ÖN-KAYIT TASLAĞI

> **Güncel:** 10 Eylül 2026 · **Durum:** taslak — mühürlenmedi.
> Sabit bir mühür tarihi yok (öğrenci kararı). Ön-kayıt Aşama 4'ün başında,
> ana deney koşulmadan önce kesinleşir.
> Bu belge hangi soruların hangi istatistikle sınanacağını anlatır; sayısal
> eşikler ve kesin hücreler henüz yok.
> Önceki sürümler emekli `sim/` kollarıyla yazılmıştı:
> `arsiv/06-ON-KAYIT-2026-09-10.md` · `arsiv/06-ON-KAYIT-2026-08-27.md`.

---

## 0 · Temel kavramlar

### 0.1 · Aşama ≠ aile

| | aşama | aile |
|---|---|---|
| ne | bir iş dönemi (`01` §5) | bir çoklu karşılaştırma düzeltme birimi |
| ne işe yarar | takvim, sıra, bağımlılık | Holm–Bonferroni aile **içinde** uygulanır |
| sonradan değişebilir mi | evet | mühürden sonra hayır |

### 0.2 · Mühür neyi korur

Ön-kaydın değeri, hipotezin, eşiğin ve analiz planının sonuç görülmeden
yazılmasıdır. Korunacak üç şey:

1. **Ana deney tohumları (2000–2039) mühürden önce hiçbir kolda koşulmaz.**
2. **Eşikler rakiplerin gürültüsünden türer.** Eşiklerin *türetme formülü*
   özgün protokolün ilk koşusundan önce yazılır; sayısal değerleri taban
   protokollerin geliştirme tohumlarındaki ölçümünden hesaplanır.
3. **Parametreler mühürde sabitlenir.** Rakipler RFC varsayılanındadır; özgün
   protokol mühür anındaki değerlerindedir; hiçbir kol senaryoya göre
   ayarlanmaz.

### 0.3 · Sıra — 10 Eylül 2026'da gevşetildi 🟢 öğrenci onayladı (aynı gün)

**Eski sıra:** *"özgün protokol mühürden sonra İLK KEZ koşulur"*. Öğrencinin iş
akışında özgün protokolün tasarımı (Aşama 3) veri toplamadan (Aşama 4) önce
gelir; bir protokol denenmeden tasarlanamaz. Yeni sıra:

```
1. Simülatör doğrulanır                                        (Aşama 1)
2. Taban protokoller yazılır, uygunluk testlerini geçer,
   geliştirme tohumlarında gürültüleri ölçülür                  (Aşama 2)
3. Eşiklerin türetme formülleri, güç analizi yöntemi ve
   aday birincil hücre yazılır  ← özgün protokolün ilk koşusundan önce
4. Özgün protokol tasarlanır, geliştirme tohumlarında denenir   (Aşama 3)
5. MÜHÜR: hipotezler · eşik değerleri · parametreler ·
   tohum sayısı · birincil hücre                                (Aşama 4 başı)
6. Ana deney tohumlarında bütün kollar koşulur                  (Aşama 4)
```

- **Neden güvenli:** geliştirme sırasında özgün protokolün sonucu görülse bile
  eşik ona göre seçilemez. Formül önceden yazılıdır, değeri rakiplerin
  gürültüsünden gelir ve ana deney tohumları hiç görülmemiştir.
- **Kalan risk:** hipotezin *hangi hücrede* sınanacağı geliştirme sonuçlarından
  etkilenebilir. Bu yüzden aday birincil hücre adım 3'te yazılır. Adım 5'te
  değişirse gerekçesiyle kaydedilir ve değişen hipotez keşifsel etiketlenir.
- Öğrenci bu sırayı 10 Eylül 2026'da onayladı.

### 0.4 · Adım 3 — özgün protokolün İLK KOŞUSUNDAN ÖNCE yazıldı (23 Eylül 2026)

> **Karar kaydı:** `04` K-153. **Durum:** formüller ve yöntem BAĞLAYICI —
> DESPARETE'nin hiçbir simülasyon sonucu görülmeden yazıldı. Üç seçim
> öğrenci tarafından aynı gün verildi (§0.4.4) — adım 3 TAMAM.
> Bu bölüm yalnız **Aile 2 (üstünlük)** ve **Aile 3 (mekanizma)** içindir:
> Aile 1 yalnız taban protokolleri kapsar ve özgün protokolün sonucundan
> etkilenemez; hücreleri mühürde yazılır.

#### 0.4.1 · Birincil testler

Aile 2'nin birincil testi rakip başına BİR tanedir: **H2.a** DESPARETE ↔
AODV · **H2.b** ↔ OLSR · **H2.c** ↔ AOMDV — `m = 3`, Holm–Bonferroni aile
içinde (§7). Her biri birincil hücrede, birincil metrikte, 40 ana deney
tohumunda eşleştirilmiş, çift yönlü Wilcoxon. Gecikme ve kontrol yükü
betimleyicidir (güven aralığıyla, §3'ün üçlü sunumu) — birincil test
değildir; test sayısını artırmak her hipotezin eşiğini yükseltirdi (§1).

#### 0.4.2 · Eşiğin türetme formülü — serbest sabit YOK

Birincil hücrede, **yalnız taban protokollerle**, geliştirme tohumlarında
(`G` = 1100–1119, 20 tohum; ana deney tohumlarıyla kesişmez):

    d_XY(s) = M_X(s) − M_Y(s)          X, Y ∈ {AODV, OLSR, AOMDV}, s ∈ G
    SD_ref  = max( SD(d_AODV,OLSR) , SD(d_AODV,AOMDV) , SD(d_OLSR,AOMDV) )
    δ       = 2 · SD_ref / √n          n = ana deney tohum sayısı (40)

`M` birincil metriktir. δ, projenin çözünürlük tanımının (`kalibrasyon/
cozunurluk.py`: `R = 2 · SD / √n`) eşleştirilmiş hâlidir — kâhin kolları
yerine gerçek rakiplerle: *deneyin iki protokol arasında görebileceği en
küçük fark.* En gürültülü taban çifti alınır (muhafazakâr). Özgün protokolün
hiçbir koşusu δ'ya GİRMEZ.

**H2.x'in hükmü** (rakip Y için; §5.2'nin biçimi sayıya bağlandı):

| hüküm | koşul |
|---|---|
| **üstün** | Holm'dan sonra p < α = 0,05 **ve** eşleştirilmiş ortalama fark ≥ δ, yönü DESPARETE lehine **ve** mekanizma kapısı geçer (Aile 3 — kapı tanımı mühürde, ablasyon bayraklarıyla) |
| **aşağı** | aynı iki sayısal koşul, ters yönde — negatif sonuç olarak raporlanır |
| **ayırt edilemedi** | geri kalan her durum; dışlanan etki büyüklüğü (%95 GA'nın uçları) ve ulaşılan güç yazılır (`03` §B2) |

⚠️ δ koşulu Wilcoxon'un anlamlılığından AYRI bir koşuldur: sıra testi,
çarpık bir dağılımda ortalaması küçük bir farkı da anlamlı bulabilir.

#### 0.4.3 · Güç analizi yöntemi — Aşama 4'ün başında, bu yöntemle

1. **Gürültü dağılımı:** §0.4.2'nin `d_XY(s)` farkları, her çift kendi
   ortalamasından arındırılarak (sıfır merkezli). Aşama 4 başında
   DESPARETE'nin geliştirme tohumlarındaki `d_D,Y(s)` farkları da varsa,
   SADECE YAYILIMLARI (ortalamaları çıkarılarak) havuza girer — hangisinin SD'si
   büyükse güç onunla hesaplanır. Özgün protokolün ORTALAMA farkı hiçbir
   yerde kullanılmaz.
2. **Benzetim:** her Δ için `B = 2 000` örneklem: gürültü dağılımından
   yerine koyarak `n` fark çekilir, Δ eklenir, çift yönlü Wilcoxon;
   ret ölçütü `p < α / m` (Holm'un ilk adımı — en kötü durum, muhafazakâr).
   `güç(Δ)` = ret oranı.
3. **Çıktı:** `MDE₈₀` = gücün 0,80'i geçtiği en küçük Δ; ve δ'daki güç.
4. **Tohum kuralı:** `MDE₈₀ > Δ_hedef` ise mühürden ÖNCE tohum sayısı
   artırılır — `n' = ⌈n · (MDE₈₀ / Δ_hedef)²⌉`, sonra 1–3 yeni `n` ile
   yeniden (§7: *"mühürden önce artırılır, sonra artırılamaz"*). `Δ_hedef`
   öğrenci kararıdır (§0.4.4).
5. Tümü sıfır farklar için NaN tuzağı (§7) benzetimde de açıkça denetlenir.

*Ön tahmin (gerçek gürültüyle ölçüm değil):* yöntem NORMAL gürültüyle
denendi — `n = 40`, `α / m = 0,05 / 3`, `B = 2 000`: güç δ'da **0,31**,
1,6·δ'da 0,72, **1,7·δ'da 0,81** → `MDE₈₀ ≈ 1,7 · δ` (normal yaklaşımın
1,62'si Wilcoxon'da biraz büyüyor). Kâhin kollarının eşleştirilmiş
çözünürlüğü ~0,023 ile (`07` §09.3): `MDE₈₀ ≈ 0,039 < Δ_hedef = 0,05`
(önerilen). Taban protokollerin gürültüsü kâhininkinden büyükse bu büyür —
o yüzden ölçülür. Üretici: `python arsiv/teshis/guc_on_tahmin_2026-09-23/guc.py`
(tohum 20260923).

#### 0.4.4 · Aday birincil hücre ve öğrenci kararları

**Önceki kararlardan sabit:** N = 40 · alan 1800 m · **yere toplama**
(8 Eylül: birincil desen) · **formasyon + istasyon tutma** (10 Eylül:
çekirdek mobilite) · 40 tohum. ⚠️ Formasyon kolunda ana deney tohumlarının
2'sinde ağ ölçüm penceresi içinde bölünüyor (K-132); bölünmüş tohum
atılmaz, satır onu söyler.

**Seçilecek üç şey:**

1. **Karıştırma koşulu** (aile · sinyal sınıfı). ρ = karıştırıcının
   engellediği bağ oranı (`07` §05.3.1, K-127):

   | aday | ρ | ne sınar | bedeli |
   |---|---|---|---|
   | `tekli_merkez` · sürekli | 0,258 | referans kurgu; en temiz yorum; evre metriklerinin kapıları bu karıştırıcıyla koşuldu (statik kolda — `kalibrasyon/evre_metrikleri_kapilari.py`) | sahaya en az paralel olan (tek, sabit, merkezde) |
   | `hava_eslik` · sürekli | 0,260 | en güçlü etki + **hareketli** kötü bölge: rota, bozulan bağlardan yerel ölçümle kaçabiliyor mu — DESPARETE'nin tasarım gerekçesinin tam karşılığı | şok yavaş gelir; evre metriklerinin bu kurguda ne ölçtüğü ayrıca sınanmalı (`07` §05.3) |
   | `derin_sizma` · sürekli (yay–sus–taşın 15/15 s) | 0,170 (açık evrede 0,382) | tekrarlanan şok ve toparlanma — onarım hızı, literatür boşluğu B (`01` §2.2) | ortalama etki en zayıf; pencere ortalaması açık/sessiz dönemleri karıştırır |

2. **Birincil metrik:** **PDR** (ölçüm penceresinde teslim; çözünürlüğü
   ölçülü, en sağlam) · ya da **toparlanma süresi** (M3, `08`; projenin *"ne
   kadar hızlı toparlandım"* iddiası, ama tek şoklu kurguda anlamlı).
3. **`Δ_hedef`** — tohum kuralının hedef etkisi (§0.4.3).

✅ **ÖĞRENCİ KARARI (23 Eylül 2026): öneri olduğu gibi** — *"önerdiğin gibi
olsun"*. **Aday birincil hücre: `formasyon · yere_toplama · hava_eslik ·
sürekli` · birincil metrik PDR (ölçüm penceresi) · `Δ_hedef = 0,05`.**
DESPARETE'nin simülatörde hiçbir koşusu yokken verildi. Mühürde (adım 5)
değişirse gerekçesiyle kaydedilir ve değişen hipotez keşifsel etiketlenir
(§0.3).

**Ajanın önerisi (kararın dayanağı):** `formasyon · yere_toplama ·
hava_eslik · sürekli · PDR` ve `Δ_hedef = 0,05` (5 PDR puanı). Gerekçe: aday hücre, protokolün
iddiasının SINANABİLDİĞİ yer olmalı ve bu, DESPARETE'nin hiçbir sonucu
görülmeden, yalnız tasarım gerekçesinden seçiliyor — adım 3'ün koruduğu şey
tam olarak bu. `tekli_merkez` Aile 1'in referansı ve keşifsel eksen olarak
çekirdekte kalır. 0,05, üç taban protokolün karıştırıcısız hareketli
kollarda birbirinden ayrıldığı farkların mertebesi: kol ortalamalarının çift
farkları 0,01–0,17 (U1 oranları, PDR değil — K-149 §2).

---

## 1 · Aileler

| aile | soru | veri | birincil test |
|---|---|---|---|
| **1 · karakterizasyon** | taban protokoller karıştırma altında nasıl bozuluyor | Aşama 2 (geliştirme) + Aşama 4 (ana deney) | mühürde |
| **2 · üstünlük** | özgün protokol rakiplere göre ne yapıyor | Aşama 4 | mühürde |
| **3 · mekanizma** | kazanç hangi bilgi kanalından geliyor | Aşama 4 | mühürde |

- Her hipotezin **tek bir birincil testi** (birincil hücresi) vardır. Diğer
  hücreler betimleyicidir ve güven aralıklarıyla tam olarak raporlanır.
- Aile içinde Holm–Bonferroni uygulanır. Her yeni hipotez diğerlerinin eşiğini
  yükseltir; liste kısa tutulur.
- Bir hipotez sonuç görüldükten sonra aileler arasında taşınamaz.

---

## 2 · Tohumlar

| küme | tohumlar | ne için |
|---|---|---|
| kalibrasyon ve geliştirme | 2000–2039 dışındaki her tohum (bugünkü kalibrasyon ölçümleri 1000'den başlar) | simülatör kalibrasyonu · uygunluk testleri · gürültü ölçümü · özgün protokol geliştirme |
| **ana deney** | **2000–2039** — 40 tohum (öğrenci, 10 Eylül 2026) | rapora giren sonuçlar; mühürden önce hiçbir kolda koşulmaz |

- 40 tohumlu bir hücrenin çözünürlüğü kâhin kollarında ~3,2 PDR puanı,
  eşleştirilmiş karşılaştırmada ~2,3 puandır (`07` §09.3).
- 1000–1029 aralığı eski simülatörde ana deney için bir kez görüldüğünden ana
  deney tohumu olarak kullanılmaz; kalibrasyonda kullanılabilir.

---

## 3 · Metrikler

**Sunum üçlüdür:** teslim · gecikme · kontrol yükü. Tek metrikle sıralama
yapılmaz.

| metrik | tanım | durum |
|---|---|---|
| PDR | ölçüm penceresinde doğan paketlerin teslim oranı (doğum kohortu) | 🟢 |
| PSR | bağ düzeyi: hedef alıcının hatasız (CRC) çözdüğü veri iletimi / veri iletim denemesi — öğrenci tanımı (`07` §08.2) | 🟡 kod değişecek |
| gecikme | ortak alt küme üzerinden; p50 · p95 · p99; kesişim oranıyla | 🟢 ham veri satırda; analiz Aşama 4 |
| kontrol yükü | bayt ve kanal süresi; NRL (çerçeve · bayt · airtime), pencere ikizleriyle — ikiz `[pencere başı, pencere sonu)` sayar (K-130) | 🟢 · kontrol istatistikleri 🟢 (`13` R8 uygulandı) |
| üç kopma sayacı | fiziksel · protokolün algıladığı · rota geçersizleşmesi; algılama duyarlılığı | 🟢 (fiziksel sayım topoloji çalkantısını ölçer, karıştırmayı değil) · 🟢 **16 Eylül 2026 (K-134): beyan kanalı kancalara açıldı.** Öncesinde protokol yalnız VERİ GÖNDERİRKEN bildirebiliyordu; kuyruğu boş bir düğüm hiç bildiremiyor ve `algilama_duyarliligi` proaktif aileyi sistematik düşük gösteriyordu |
| rota kurtarma gecikmesi Δ · COR | kopmadan kurtarmaya süre · kurtarılan / etkilenen yol | 🟢 sayaçlar; protokol beyanı gerekir |
| evre metrikleri | şok derinliği · toparlanma tamlığı · toparlanma süresi · tespit gecikmesi | 🟢 (`08`) |

**Eski simülatörde ölçülerek bulunan ve geçerliliğini koruyan kurallar:**

- **Gecikme karşılaştırması ortak alt küme üzerinden yapılır.** Ham ortalama
  karıştırma altında *"gecikme azaldı"* diyebiliyordu; aynı veride ortak alt
  küme artışı gösterdi (hayatta kalan yanlılığı; `arsiv/06-ON-KAYIT-2026-09-10.md`
  §8.1b). p95 ortalamanın yanında yazılır; kesişim oranı her zaman raporlanır.
- **Kümülatif sayaçların pencere ikizi kullanılır.** Pencere dışında üretilen
  kontrol baytı payı kola göre değişiyordu.
- 🔒 **İkizin tanımı: `[pencere başı, pencere SONU)`.** Sayaçlar pencere
  kapanınca DONAR (16 Eylül 2026, `04` K-130). Önceki tanım `[pencere başı,
  KOŞU SONU)` idi ve boşalma aralığını içeriyordu; ölçüldü — boşalmadan gelen
  pay kontrol tarafında %7,6–10,7, veri tarafında **%0,0**, çünkü trafik
  çizelgesi pencerede biter. Pay büyüyüp payda büyümediği için `nrl_*_pencere`
  ~%10 şişiyordu ve şişme **protokol ailesine göre farklıydı** (periyodik
  kontrol boşalmada akar, keşif trafiği susar) — yani H1.1'in mekanizma
  kontrolünün baktığı yerde sistematik bir yanlılık. Tanım hiçbir protokol
  yazılmadan ve hiçbir sonuç görülmeden yazıldı.
- 🔒 **`nrl_bayt` ve `nrl_airtime`in payı = kontrol + protokolün VERİ
  BAŞLIĞI** (22 Eylül 2026, `04` K-151 — ölçümden ÖNCE). Veri paketine
  yönlendirme başlığı ekleyen protokolün (DESPARETE, 36 B) başlık bedeli veri
  değil yönlendirme ek yüküdür; başlık taşımayan protokolde (AODV · OLSR ·
  AOMDV) oran eskisiyle BİREBİR.
- **Analiz birimi tohumdur.** Havuzlanmış okuma yalnız betimleyicidir.

---

## 4 · Taban protokoller ve uygunluk

### 4.1 · Hangileri

| protokol | aile | neden |
|---|---|---|
| AODV | reaktif, mesafe vektörü | literatürün evrensel taban çizgisi; talep üzerine tek yol |
| OLSR | proaktif, bağ durumu | reaktifin karşı kutbu; periyodik HELLO/TC, MPR |
| AOMDV | reaktif, çok yollu | "yedek yol" sorusunu doğrudan sınar |

GPSR kapsam dışıdır (`01` §3.1).

**AOMDV öngörüsü yeniden yazılacak.** Eski öngörü, "tek karıştırıcılı sabit
topolojide AOMDV'nin AODV'ye üstünlüğünün kaybolması beklenir" diyordu ve
koşulmadan önce yazılmıştı. Öğrencinin yeni kararları (çoklu, hareketli
karıştırıcı; hareketli sürü; yere toplama) öngörünün öncüllerini değiştirdi.
Mühürden önce yeni tehdit modeline göre yeniden yazılır; eski hâli arşivde
kalır.

### 4.2 · Parametreler — RFC varsayılanı

| AODV (RFC 3561) | değer | OLSR (RFC 3626) | değer |
|---|---|---|---|
| HELLO_INTERVAL | 1,0 s | HELLO_INTERVAL | 2,0 s |
| ALLOWED_HELLO_LOSS | 2 | NEIGHB_HOLD_TIME | 6,0 s |
| ACTIVE_ROUTE_TIMEOUT | 3,0 s | TC_INTERVAL | 5,0 s |
| RREQ_RETRIES | 2 | TOP_HOLD_TIME | 15,0 s |
| NODE_TRAVERSAL_TIME | 40 ms | WILLINGNESS | 3 |
| NET_DIAMETER | 35 | MAXJITTER | HELLO_INTERVAL / 4 |

Künyeler `02` §R'dedir (WILLINGNESS ve MAXJITTER henüz oraya işlenmedi).

- **HELLO aralıkları yapay olarak eşitlenmez;** kontrol yükü farkı her
  karşılaştırmayla birlikte raporlanır.
- Bu simülatörde koşum düzeyindeki 1 s'lik beacon OLSR'ı zayıflatabilir; öneri
  `13` §06.1 R2.

### 4.3 · Dört uygunluk testi

| # | test | beklenen |
|---|---|---|
| U1 | karıştırıcısız, bağlı ağ | teslim oranı kâhin referansına yakın (yakınsama sonrası) |
| U2 | tek bağ koptuğunda | AODV RERR üretir ve yeni RREQ başlatır; OLSR NEIGHB_HOLD_TIME dolunca tabloyu günceller |
| U3 | karıştırma ve hareket yok | OLSR yükü periyodik ve sabit; AODV yükü yalnız keşif anında |
| U4 | olay izleri | RFC'nin öngördüğü mesaj sırası ve zamanlayıcı davranışı |

**🔴 U3'ÜN AODV BEKLENTİSİ TUTMADI — BULGU olarak raporlanır (19 Eylül 2026,
K-144 · öğrenci kararı).**

*"AODV yükü yalnız keşif anında"* beklentisi bu simülatörde ölçüldü ve
**tutmadı**. Kayıplı bir kablosuz ağda sürekli trafik altında bağlar çarpışma
ve sönümlemeyle düşüyor, MAC vazgeçiyor ve AODV her seferinde yeniden
keşfediyor; yük süreyle neredeyse doğrusal büyüyor:

| küçük dünya, statik | 60 s → 120 s kontrol çerçevesi oranı |
|---|---|
| AODV | **2,070** |
| OLSR | **2,130** (§13 sonrası, K-147; öncesi 2,200) |
| AOMDV | **2,310** (K-149) |

Üretici: `python -u kalibrasyon/aodv_uygunluk.py u3`. RFC 3561'e uygun
davranış; beklenti literatürden gelen idealleştirilmiş bir tablo, ölçüm ise
bu ağın gerçeği. 🔒 **Bu, H1.1 için bir bulgudur:** tepkisel ailenin
*"rotayı bulunca susar"* avantajı, kayıplı ve yüklü bir taktik ağda büyük
ölçüde kayboluyor.

⚠️ Ölçüm iki kusur temizlendikten SONRA yapıldı: RFC §6.9'un yarım
uygulanması (K-136) ve §6.11'in öncül kuralının hiç uygulanmaması (K-143).
İkincisi düzeltilmeden oran 1,854'tü ve sürekliliğin bir kısmı gereksiz
RERR'lerden geliyordu — bulgu, bir kusurla karışmamış hâliyle raporlanıyor.

**🟢 U1 ARTIK BİR ÖLÇÜ — oran, mutlak değer değil (17 Eylül 2026, K-136).**

*"Kâhin referansına yakın"* cümlesi 10 Eylül'den beri bir ölçü değildi; ilk
gerçekleme onu `PDR ≥ 0,95` diye MUTLAK bir eşiğe çevirdi ve **yanlış oldu** —
o referans tam ölçekte ölçülmüştü, eşik 14 düğümlük test dünyasında
uygulanıyordu. Ölçütün işlemsel hâli:

    oran = PDR(protokol) / PDR(EnGuvenilirKahin)        ← AYNI konfigürasyon

    🔒 statik kol     oran ≥ 0,90
    🔒 hareketli kol  oran ≥ 0,60

Oran biçiminin üçüncü kazancı bu maddenin *"bağlı ağ"* ön koşulunu **kendi
kendine nötrler**: kâhinin geçemediği bir bölünme paydayı da düşürür, yani
topolojinin kusuru protokolün hanesine yazılmaz.

⚠️ **Eşik, ölçüm GÖRÜLDÜKTEN SONRA seçildi** (öğrenci kararı) ve bu ön-kayıt
disiplininin zayıf tarafıdır. Taşınmasının sebebi: U1 bir **kabul kapısıdır**,
bir hipotez testi değil (§4.4 madde 3) ve hiçbir sonuç iddiası ona dayanmaz.
Eşik üç taban protokolü de bağlar; AODV'ye göre ayarlanmış olması OLSR ve
AOMDV'ye avantaj sağlamaz. Gerekçenin tamamı
`kalibrasyon/aodv_uygunluk.py`nin başlığında.

🔒 **KAPININ İKİ YARISI — nerede durduğu bağlayıcıdır.** Desen P1–P8'inkinin
aynısıdır: yapı kapısı testlerde, tam ölçek kanıtı kalibrasyonda.

| yarı | yer | ne sınar |
|---|---|---|
| yapı | `tests2/test_aodv.py` | keşif tamamlanıyor · teslim var · defter kapanıyor · **kâhin aşılmıyor** — eşiksiz |
| sayısal | `kalibrasyon/aodv_uygunluk.py` | dört `-yok` kolu × üç geliştirme tohumu, TAM pencerede; verdikt **çıkış koduna** bağlı |

**Durum (10 Eylül):**

- Kontrol düzlemi eklendi; U2 ve U3 mekanik olarak ifade edilebilir.
- 🟢 **U2'nin ikinci ön koşulu da karşılandı (16 Eylül 2026, K-131):** AODV
  rota keşfi sırasında paketi tamponlayabiliyor. Öncesinde U2 koşulabilirdi
  ama ölçtüğü şey protokolün kurtarma davranışı değil, keşif süresince
  kaybettiği paketler olurdu.
- ~~U2'deki RERR'in tetiklenmesi için bağ kopması geri bildirimi gerekir~~ —
  🟢 **ÖN KOŞUL KARŞILANDI (14 Eylül 2026, K-121):** iletim başarısızlığı
  kancası uygulandı (`13` §03.6). U2 artık mekanik olarak ifade edilebilir.
- **U1'in referansı:** kâhinle karıştırıcısız PDR statik kolda 0,996–1,000,
  hareketli kolda 0,83–0,92 (`python -u kalibrasyon/pdr_tavani.py 1`). "≈ 1"
  yalnız statik kolda anlamlıdır; hareketli kolda referans kâhin değeridir.
- M4'ün boş kol kapısı Aşama 2'de, kopma beyan eden ilk protokolle koşulur
  (`08`).

### 4.4 · Sadakat protokolü

1. Protokolün RFC parametreleri önceden yazılır (§4.2).
2. Uygulama yazılır; hiçbir parametre senaryoya göre değiştirilmez.
3. U1–U4 koşulur; geçilmeden protokol kabul edilmez.
   🔴 **BU MADDE U1 İÇİN YENİDEN YAZILDI (17 Eylül 2026, K-137 · öğrenci
   kararı).** Sebebi bir kavram karışıklığıydı, bir gevşetme değil: U1 iki
   ayrı soruyu tek kapıya bağlamıştı — *"gerçekleme RFC'ye sadık mı"* ve
   *"protokol iyi teslim ediyor mu"*. İkincisi bir **kabul ölçütü değil,
   deneyin kendi sonucudur.** AODV'nin zayıf bağlı bir topolojide kötü
   teslim vermesi, gerçeklemenin bozuk olduğu anlamına gelmez — RFC 3561
   atlama sayısıyla yönlendirir ve bağ kalitesi eşiği yoktur; yani bu, tam
   olarak §5.1 H1.1'in ölçmek istediği şeydir. Eski hâliyle madde 3, kendi
   deneyinin bulgusunu bir "başarısızlık" sayıp protokolü reddederdi.

   🔒 **U1 artık İKİ PARÇADIR ve ikisi de bağlayıcıdır:**

   | parça | ne sorar | kaldığında |
   |---|---|---|
   | **U1-U · uygunluk** | Gerçekleme RFC gibi mi davranıyor: keşif tamamlanıyor mu · teslim çok atlamalı mı · korunum defteri kapanıyor mu · protokol **kâhini geçiyor mu** (geçiyorsa kâhin bilgisi sızmıştır) | 🔴 **Protokol KABUL EDİLMEZ.** Bu bir kusur kapısıdır ve gevşetilemez |
   | **U1-B · başarım profili** | Protokolün PDR'sinin, AYNI konfigürasyonda koşan ETX kâhinine oranı (statik ≥ 0,90 · hareketli ≥ 0,60) | 🟡 **Protokol reddedilmez, ama hücre AÇIKLANMADAN geçilemez** |

   🔴 **"Açıklanmadan geçilemez" kapının dişidir** — ve `12` §4'te seçilen A
   seçeneğinin bedeli budur. Eşiğin altında kalan her (kol, tohum) hücresi
   için, **ÖLÇÜMLE**, şu gösterilmek zorunda: kayıp bir yazılım kusurundan
   değil, protokolün kendi mekanizmasından geliyor. Açıklaması kayda
   geçmemiş bir düşük hücre kapıyı **kırmızı yakar** (çıkış kodu 1). Yani
   yeni bir düşük hücre asla sessizce geçemez; ancak açıklaması yazıldıktan
   sonra bir BULGU'ya dönüşür.

   ⚠️ Aynı disiplin OLSR ve AOMDV'ye de uygulanacak. Bir protokolün düşük
   hücresini açıklamak, onu başka protokollerle karşılaştırmaktan MUAF
   tutmaz: karşılaştırma ana deneyin işidir, U1'in değil.

   ⚠️ **Bir açıklamanın sınırı (19 Eylül 2026, K-145).** Açıklama, bir
   hücrenin neden kolunun **en düşüğü** olduğunu gösterir; hücrede kusur
   olmadığını kanıtlamaz. `statik-yok/1002`nin açıklaması doğruydu, ama
   hücre eşiğin altında kalıyordu çünkü o yapıya bir RFC kusuru (§6.11)
   ekleniyordu — kusur düzeltilince hücre geçti ve kapı açıklamayı ölü
   kayıt olarak yakaladı. Açıklanmış hücreler bu sınırla okunur: *"bilinen
   kusurlar düzeltildikten sonra hâlâ düşük"*. Kural değişmedi; yalnız
   okunuşunun sınırı yazıldı.
4. Modellenmeyen özellikler sapma olarak yazılır.
   🟢 **AODV için yazıldı** (17 Eylül 2026) — dört sapma,
   `protokoller/aodv_bicim.py` başlığında tabloyla:

   | özellik | RFC | neden yok | AODV'yi zayıflatır mı |
   |---|---|---|---|
   | yerel onarım | §6.12 | RFC'de OPSİYONEL; üç yeni parametre getirir ve üçü de ölçülmemiş olurdu | ⚠️ **EVET** — karıştırma altında kopma sıktır ve yerel onarım tam orada iş görür. Sonuç raporlanırken bu sapma yanında anılır |
   | RREP-ACK · kara liste | §5.4 · §6.8 | yalnız TEK YÖNLÜ bağlar için gerekli; bu simülatörde bağ SİMETRİKTİR | hayır |
   | karşılıksız RREP (G) | §6.6.3 | kaynağa geri yol zaten RREQ'in ters rotasından kuruluyor | hayır |
   | çok arayüz · alt ağ öneki | §5.2 | tek arayüz, düz adresleme | hayır |

   ⚠️ **Bir sapma TERS yönde:** RREQ'te bir bayt FAZLA ödeniyor (RFC 24 →
   25). RFC'de TTL IP başlığındadır ve o başlık `KONTROL_KAPSULLEME`de zaten
   faturalanıyor, ama simülatörde bir çerçeveye "IP TTL" koymanın yolu yok.
   Yönü AODV'yi olduğundan **pahalı** gösterir — yani `nrl_*`
   karşılaştırmasında AODV'nin lehine bir sapma yoktur.

   🟢 **OLSR için yazıldı** (19 Eylül 2026, K-142) — `protokoller/olsr_bicim.py`
   başlığında. Kural *"SHOULD uygulanır, MAY beyan edilir"*; ölçülmüş
   gerekçeli tek istisna §13 bağ katmanı bildirimi (K-146 · K-147).
   🟢 **AOMDV için yazıldı** (22 Eylül 2026, K-148) — makale + RFC 3561;
   AODV'nin sapmaları aynen, artı ne makalede ne RFC'de olan on BEYANLI SEÇİM
   `protokoller/aomdv.py` başlığında (S1–S10), her biri gerekçe ve yönüyle.
5. Ana deneyde parametreler sabittir.

Aynı disiplin özgün protokole de uygulanır.

---

## 5 · Hipotezler — taslak

### 5.1 · Aile 1 · karakterizasyon

Soru biçimleri korunur; hücreler, eşikler ve birincil testler mühürde yazılır.

- **H1.1 · Protokol ailesi bozunumu belirler.** Reaktif ve proaktif
  protokoller aynı karıştırma altında farklı büyüklükte teslim kaybı yaşar.
  - **Mekanizma kontrolü:** fark teslimde görünüyorsa kontrol düzleminin
    davranışı ayrıca gösterilir (AODV'de karıştırma altında kontrol baytı
    artar, OLSR'da periyodik kalır). Desen yoksa sonuca bakılmaz.
  - **Yanlışlanma:** eşleştirilmiş farkın %95 GA'sı sıfırı içerir ya da
    mekanizma kontrolü geçmez.
- **H1.2 · Çöküş dirseklidir.** Karıştırma şiddeti tarandığında teslim oranı
  bir dirsekle düşer.
  - **Genişlik kontrolü:** tarama aralığı tohum SD'sinin en az 3 katı değilse
    hipotez test edilmemiş sayılır.
  - **Mekanizma kontrolü:** bağ düzeyi PER eğrisi ile ağ PDR eğrisinin
    dirsekleri karşılaştırılır; çakışırlarsa dirsek radyo modelinin
    özelliğidir. Çoklu karıştırıcıda şiddet ekseni senaryonun toplam
    gücüdür.
- **H1.3 · Yapı güçten önemlidir.** Aynı ortalama güçte darbeli ve sürekli
  karıştırma farklı kayıp üretir.
  - Bu simülatörde ölçülmüş iki eşleştirilmiş kontrast var: darbeli ↔ sürekli
    (ortalama güç eşit) ve aldatıcı ↔ sürekli (bağ hasarı aynı; fark CSMA
    görünürlüğü ile en çok 0,008'lik bir PER artığı, `07` §05.2).

**Ön-kayda girecek ölçülmüş tahminler:**

1. Taramalı sınıfın konak süresi (100 ms) en hızlı protokol zamanlayıcısından
   kısa; protokoller onu seyreltilmiş bir sürekli karıştırıcı gibi görebilir.
2. Taramalı sınıfın ortalama gücü 4,77 dB düşük; "taramalı zayıf çıktı"
   bulgusu tek başına mekanizmaya yazılamaz.
3. Aldatıcı ↔ sürekli farkı saf CSMA etkisi değildir.

**Yeni kararlarla açılan soru adayları 🔵**

- Hareketli karıştırıcıda rota kurtarma gecikmesi (Δ) protokol ailesine göre
  farklı mı? (Literatür boşluğu B.)
- Geçide yakınsayan trafikte, karıştırıcı geçit çevresindeyken çok yollu
  protokolün yedek yolları aynı anda mı kesiliyor?

### 5.2 · Aile 2 · üstünlük — biçim

> **H2.x:** Özgün protokol, [AODV | OLSR | AOMDV] ile karşılaştırıldığında,
> birincil hücrede **[metrik]** bakımından ön-kayıtlı eşiği geçen bir fark
> üretir.
>
> **Yanlışlanma:** eşleştirilmiş farkın %95 GA'sı sıfırı içerir, **ya da** fark
> ters yöndedir, **ya da** mekanizma kapısı geçmez.

### 5.3 · Aile 3 · mekanizma ayrımı

**Soru:** kazanç varsa hangi bilgi kanalından geliyor?

**Ölçüt** (tasarımdan bağımsız, eski sürümden taşındı): kol **kendi
ablasyonuna** karşı okunur. Aynı protokol ve aynı kalıcılık kullanılır;
komşuların bildirdiği bilgi alanı düğümler arasında permüte edilir
(permütasyon düğüm başına sabit, komşu sırası korunur). Tek fark bilgidir.

- Eşleştirilmiş fark tohumların büyük çoğunluğunda pozitif olmalı ve %95 GA
  sıfırı dışlamalıdır. Oranlar mühürde yazılır.
- Sayaçlar karar başına oran olarak raporlanır.
- Basit bir null yetmez; kalıcılık tek başına avantaj satın alabilir (eski
  simülatörde ölçüldü).

**Null çekim sayısı:** 26 Ağustos 2026'da m = 5 ilan edilmişti; eski
simülatörde tek bir çekimin varyansı farkın %46,4'üydü. Ablasyonun kendisi
özgün protokolün tasarımına bağlı olduğu için tasarım bitince yeniden
değerlendirilir; değişirse gerekçesiyle kaydedilir.

---

## 6 · Özgün protokol — tasarım öğrenciden

🔄 **23 Eylül 2026:** tasarım geldi — **DESPARETE v0.1**
(`protokol_kaynaklari/DESPARETE_TASARIM_PAKETI/`, tek okuma `36`). İnceleme
ve öğrencinin kararları `04` K-150; gerçeklemenin ilk kararları K-152.
Hipotezler (§5.2 · §5.3) ve ablasyon kolları mühürde bu tasarıma göre
yazılır.

**Tasarım doldurulduğunda geçerli olacaklar:**

- kâhin bilgisi yok (`05`)
- derin öğrenme yok
- parametreler mühürde sabit
- her mekanizma ayrı bir konfigürasyon bayrağı — 🟢 **yazıldı** (K-159: sekiz
  bayrak, varsayılan hepsi açık = v0.1; güvenlik değişmezleri bayrakla
  kapanmaz). Hangilerinin Aile 3'te KOL olacağı mühürde seçilir.
- durum tutan her bileşende başlangıç koşulu sorulur

**Bilinen iki tuzak:**

- Literatürdeki bir karıştırma-farkındalıklı ödül kodu karıştırıcı mesafesini
  doğrudan simülatörden okuyor (`10` §7c Y-1); o kod kopyalanmaz.
- Gürültünün mutlak değeri bu simülatörde anlamlı değildir; karıştırma sezimi
  oranla ya da değişimle yapılır (K-110 EK-4).

---

## 7 · İstatistik planı

| konu | plan |
|---|---|
| tohum | 40, tüm kollarda aynı küme (2000–2039) |
| eşleştirme | ayrık rastgelelik → aynı tohum aynı senaryo → eşleştirilmiş test |
| test | Wilcoxon işaretli sıralar, çift yönlü |
| düzeltme | Holm–Bonferroni, aile içinde, yalnız birincil testlere |
| α | tek bir α (öneri: 0,05); evre metriklerinin iki anlamlılık sabiti de buradan türetilir (`08` §05.3) |
| raporlama | etki büyüklüğü + güven aralığı; negatif sonuçta dışlanan etki büyüklüğü ve ulaşılan güç |
| güç analizi | Aşama 4 başında, taban protokollerin geliştirme tohumlarındaki gürültüsüyle; 40 tohum yetmiyorsa mühürden önce artırılır, sonra artırılamaz |
| durdurma kuralı | eski "göreli GA yarı genişliği ≤ %10" kuralı sıfıra yakın farklarda tanımsızlaşıyordu (`arsiv/06-ON-KAYIT-2026-09-10.md` §9.2); mühürde mutlak birimle yeniden yazılır |

**NaN tuzağı.** `scipy.stats.wilcoxon` tüm farklar sıfırken NaN döndürür ve
hata fırlatmaz; tek bir NaN Holm'dan sonra bütün p'leri 1,00 yapar. Test
çağrılmadan önce farkların tümünün sıfır olup olmadığı açıkça kontrol edilir;
regresyon testi gerçek örneklem boyutuyla yazılır.

**Kanal rastgeleliği** sıralı akıştan değil hash'ten gelir. Aynı anda aynı
çift arasındaki iletim, hangi protokol koşarsa koşsun aynı gerçeklemeyi görür
(`03` §4).

---

## 8 · Bir sonucun geçerlilik koşulları

Dördü birden sağlanmayan hiçbir sonuç raporlanmaz:

| # | koşul | nasıl |
|---|---|---|
| 1 | koşu uzunluğundan bağımsızlık | iki ayaklı ölçüt: **yön** (kesin işaret testi) ve **büyüklük** (GA uçları ≤ k × tohum SD; k güç analizinde belirlenir); kol başına, rapora giren kollar için bağlayıcı. Öğrenci kararıyla ısınma ve ölçüm penceresi birlikte taranacak — eski simülatörde gecikmede pencere içi bir ısınma artığı görülmüştü |
| 2 | metriğin ne ölçtüğü doğrulanmış | evre metrikleri kapıları (`08`); PSR'nin yeni tanımı için bir kapı 🔵 |
| 3 | gizli asimetri yok | HELLO aralıkları · koşum düzeyindeki beacon (`13` R2) · kapsülleme asimetrisi (R5) · veri onayı semantiği (R1) · 🟢 **beyan kanalı (K-134):** kopma bildirimi artık veri trafiğine bağlı değil — öncesinde proaktif aile düşük ölçülürdü · 🟢 **tamponlama (K-131):** rota yokken paket artık düşmek zorunda değil — eksik, RFC 3561 §6.3 gereği tamponlayan REAKTİF aileyi haksız zayıflatıyordu ve OLSR'a hiç uğramıyordu |
| 4 | regresyon testi | sonucu üreten kodun testi |

---

## 9 · Mühürden önce kapanması gerekenler

- [ ] Aşama 1 işleri (`12` §3)
- [ ] SINANMAMIŞ = 0 ve duyarlılık borcu = 0 — ya da borçlu sabitler eksen olarak ilan edilir
- [ ] U1–U4 üç taban protokolde geçti — 🟢 **U1 üçünde de** (K-145 · K-147 · K-149) · U2–U4 AODV ve OLSR'da adıyla kapı · AOMDV'de U3 ölçüldü (K-149), U2'nin karşılığı bakım kapıları (K-148) — ⚠️ mühürden önce AOMDV'nin U2 ve U4 karşılıkları adıyla eşlenmeli
- [ ] §0.3 adım 3 — eşik türetme formülleri · güç analizi yöntemi · aday birincil hücre — **özgün protokolün ilk koşusundan ÖNCE** — 🟢 **§0.4'te yazıldı (23 Eylül 2026, K-153)**: formüller ve yöntem bağlayıcı; aday hücre `formasyon · yere_toplama · hava_eslik · sürekli`, birincil metrik PDR, `Δ_hedef = 0,05` (öğrenci kararı, aynı gün)
- [ ] birincil hücre: mobilite kolu · karıştırıcı senaryosu · trafik deseni · düğüm sayısı
- [ ] α · eşik formülleri · güç analizi · tohum sayısı
- [ ] özgün protokolün parametreleri ve ablasyon bayrakları
- [ ] evre metriklerinin anlamlılık sabitleri · pencere taraması · koşul 1'in k değeri
- [ ] veri onayı semantiği kararı
- [ ] AOMDV öngörüsünün yeni tehdit modeline göre yazılması
- [ ] mühür sırasının öğrenci onayı (§0.3)

---

## 10 · Kayıt tablosu

| tarih | ne | sonuç |
|---|---|---|
| 17 Ağu 2026 | Ç4.4 bandı — eski simülatör, koşulmadan önce ilan edildi | tutmadı; sonuç kayıtta |
| 26 Ağu 2026 | Aile 3 null çekim sayısı m = 5 | yeniden değerlendirilecek (§5.3) |
| 1 Eyl 2026 | belge yeniden kurgulandı (K-081): faz/aile ayrımı · üç rakip · sadakat protokolü | — |
| 8–9 Eyl 2026 | Li replikasyonu ön-kaydı (`09`) | H1 tutmadı, H2/H3 tuttu |
| 10 Eyl 2026 | `sim2`ye göre yeniden yazıldı · tohum 40 · PSR tanımı · sabit mühür tarihi kaldırıldı · mühür sırası gevşetildi (onay bekliyor) · Li yeniden ölçüldü, aynı (K-113) | taslak |

Mühürden sonra yapılan her değişiklik tarihiyle bu tabloya yazılır ve ilgili
hipotez keşifsel etiketlenir.
