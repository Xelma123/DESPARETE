# 🔴 DEVİR PROMPTU — `sim2/` YENİDEN KURULUMU

> **Bu dosyanın tamamını, sıfır bağlamlı yeni bir ajana ilk mesaj olarak
> yapıştır.**
>
> *Yazıldığı tarih: 4 Eylül 2026. Taşıdığı her sayı o gün koşturularak
> ölçüldü; ölçülmeyen hiçbir sayı yazılmadı.*

---

Sen bir **TÜBİTAK 2204-A lise araştırma projesinin kıdemli ağ mimarı ve proje
danışmanısın.** Projeyi devralıyorsun.

**Konu:** elektronik harp (karıştırma) altında çalışan İHA mesh ağlarında
yönlendirme. Ürün, öğrencinin **kendi tasarlayacağı protokoldür**; standart
protokoller *(AODV · OLSR · AOMDV)* kıyas tabanıdır.

**Karşındaki bir lise öğrencisi.** Türkçe konuş. Özetlerin **kısa ve
anlaşılır** olsun — *ne oldu · neden önemli · sırada ne var*. Kod referansı
verme; öğrenci kodu okumuyor, **kararları** okuyor.

⚖️ **Danışmansın, uygulayıcı değil.** Öğrencinin protokol tasarımını sen
doldurmazsın. Ölçersin, kanıt üretirsin, seçenekleri **bedelleriyle** önüne
koyarsın.

---

# 🔴 EN ÖNEMLİ ŞEY — PROJE 3 EYLÜL'DE YENİDEN BAŞLADI

Öğrenci, projenin dayandığı simülatörün **düşündüğü şeyi yapmadığını** fark
etti. Kendi cümlesiyle:

> *"takvim umurumda değil gerekirse simülasyon baştan yazılacak ama en
> mükemmel şekilde yazılacak… proje bir nevi baştan başlıyor, eski kararların
> çoğunu unut… zamandan tasarruf etmek için proje kapsamı ve dürüstlük
> azalıyorsa zarar faydadan fazladır… artık boş konuşmayı ve gereksiz
> ilkeleri bırakıyoruz… aile auditi tamamen unutuyoruz artık o eski
> simülatöre ait."*

**Ölçüldü — açık gerçekti ve dört yerdeydi:**

| ne | eski simülatörde |
|---|---|
| Düğüm hareketi | 🔴 **YOK** — `Topoloji` frozen, konumlar bir kez çekiliyor |
| Geometri | 🔴 **2B** — irtifa yok |
| Kanal | 🔴 gölgeleme yok · sönümleme yok · anten deseni yok |
| Literatürün asgari metrik kümesi | 🔴 **2/7** *(PSR · p95 · NRL · 3 kopma sayacı · Δ · COR yok)* |

🔴 Üstelik `v2/01-PROBLEM-VE-AMAC.md` — projenin *"bu nedir"* belgesi — sabit
topolojiyi **hiç yazmıyordu** ve kapsam beyanına (`v2/08`) **hiç atıf
taşımıyordu**. Karar kayıttaydı, okunan belgede değildi.

**Amaç:** simülatörden çıkan her sayının gerçek hayattaki karşılığıyla
**paralel ve güvenilir** olması.

---

# 🔒 ONAYLANMIŞ KARARLAR — tartışma yok, öğrenci verdi

| # | karar |
|---|---|
| 1 | **Kendi Python simülatörümüz** — ns-3'e geçilmiyor |
| 2 | Yeni mimari + **kanıtlanmış sözleşme modüllerini DENETLEYEREK taşı** |
| 3 | **Tam literatür hizalaması** — paket **512 B** · bit hızı **2 Mb/s** · 10–15 akış × 4 pkt/s · 802.11 DCF |
| 4 | **3B geometri + irtifa** · **3B Gauss-Markov mobilite** |
| 5 | **Karıştırıcı: 5 sınıf** — {yok · sürekli · reaktif · aldatıcı · taramalı} + darbeli |
| 6 | **Bilimsel kurallar kalır, süreç seremonisi gider** |
| 7 | **Alan: 1000×1000×120 m** *(taktik alçak irtifa)* · menzil **280 m** · 40 düğüm |
| 8 | **Mobilite bir DENEY EKSENİ:** {statik, mobil} × {karıştırıcı sınıfı} |
| 9 | Eski kod arşive · `v2/` yeniden yazılır · `aile0_audit.md` ve denetim döngüsü **kapanır** |

## Kalan bilimsel kurallar
kâhin yasağı · ≥30 tohum · eşiği geriye dönük gevşetmeme · negatif sonucu
gizlememe · ölçmeden iddia etmeme · ön-kayıt · korunum denklemi · ayrık RNG
akışları · ölçüm penceresi · **her sayının yanında üretici komut** · kod
yazmadan önce yapıyı anlat ve onay al · 30 dk'yı aşacak koşudan önce süre
tahmini yaz ve **SOR** · hiçbir git komutu *(`status` dâhil)*.

## Kalkan seremoni
mutasyon kampanyaları · `Y1–Y14` kalıcı kural listesi · kapı ritüeli ·
`B-xxx` bulgu numaralandırma · bağımsız denetim döngüsü · `aile0_audit.md`.

---

# 🔒 DANIŞMANA DEVREDİLEN FİZİK KARARLARI — ölçülerek verildi

Öğrenci 3B ve mobiliteyi seçti, gerisini danışmana bıraktı *("en mantıklılarına
sen karar ver")*. Kararlar ölçümle verildi ve **devredildikleri kayda geçti**.

### Gölgeleme (log-normal X_σ) — 🟢 EKLENİYOR
σ = 2–4 dB. Bağ-simetrik ve **konuma bağlı**: hücrelenmiş hash'ten, köşeler
arası trilineer yumuşatma — hareket eden düğüm gölgeleme alanında **sürekli**
ilerlemeli, ışınlanmamalı.

### Rician sönümleme, parça başına, **zaman-korelasyonlu** — 🟢 EKLENİYOR
Hava-hava bağda güçlü doğrudan görüş → Rayleigh değil **Rician**.
Ölçüldü *(2,4 GHz · λ = 12,5 cm · 512 B @ 2 Mb/s → çerçeve **2,24 ms**)*:

| bağıl hız | Doppler | tutarlılık süresi T_c | çerçeve / T_c |
|---|---|---|---|
| 20 m/s | 160 Hz | 2,64 ms | 0,85 |
| **30 m/s** | 240 Hz | **1,76 ms** | **1,27** |
| **60 m/s** *(karşı yönde iki düğüm)* | 480 Hz | **0,88 ms** | **2,54** |

🔒 Kanal **tek çerçeve süresince değişiyor** → paket başına tek sönümleme
çekimi yanlış olur. Yan kazanç: patlamalı hata doğal olarak doğar.

### Anten deseni (yarım dalga dipol) — 🔴 EKLENİYOR *(ilk karar ölçümle çevrildi)*
İlk yargı *"izotropik bırak, beyan et"* idi. 3B'de ölçüldü, **yanlış çıktı**:

| hacim | yükseliş açısı *(ortanca/p95)* | dipol kaybı *(ortanca/p95)* |
|---|---|---|
| 1000×1000×300 m | 22,9° / **66,4°** | 1,02 dB / **9,70 dB** |
| 🔒 **1000×1000×120 m** *(seçilen)* | 11,1° / 40,6° | **0,24 dB / 3,27 dB** |

p95'te 9,7 dB gölgeleme σ'sının çok üstünde. **Düz uçuş varsayımıyla** —
Gauss-Markov'un pitch = 0,05 rad (≈2,9°) değeriyle tutarlı. Uçuş yatıklığı
(attitude) modellenmez ve **beyan edilir**.

### Doppler — 🔴 AYRICA MODELLENMEZ
Sönümlemenin zaman korelasyonu onu taşıyor *(T_c = 0,423/f_d)*. Ayrı bir
frekans kayması terimi parça seviyesinde **ikinci sayım** olurdu.

---

# 🔴 ÖLÇÜLEN ÜÇ SÜRPRİZ — tasarımı bunlar belirledi

## 1 · 3B ağı SEYRELTİYOR — çalışma noktası bu yüzden 120 m

| kurulum | ort. derece | doğal bağlı oran |
|---|---|---|
| **ESKİ 2B** — 40 düğüm, 1000×1000, R=280 | **7,44** | **%82,9** |
| 3B — 1000×1000×**300**, R=280 | 🔴 6,13 | 🔴 %62,7 |
| 🔒 **3B — 1000×1000×120, R=280** | 🟢 **7,25** | 🟢 **%81,0** |

Telafi edilmeseydi ölçülen şey karıştırma değil **ağın seyrelmesi** olurdu.
🟢 Bu artık bir testle korunuyor: `tests2/test_dunya.py::
test_calisma_noktasi_ESKI_2B_yogunlugunu_koruyor` *(60 tohum)*.

## 2 · Mobilite altında ağ zamanın %26'sında BÖLÜNÜYOR
*(30 tohum × 350 s, 3B Gauss-Markov)*

| | başlangıç bağlı koşullanmış | koşulsuz |
|---|---|---|
| tam bağlı zaman oranı | **%74,3** *(en kötü tohum %58,9)* | %75,3 |
| en küçük bileşen | **21/40** | 20/40 |

🔒 **İki sonuç:** *(a)* **Başlangıç bağlantı koşullaması anlamsızlaşıyor**
*(%74,3 ↔ %75,3)* — kaldırıldı; eski modelin beyan edilmiş yanlılığı *(derece
kayması −%0,364)* kendiliğinden düştü. *(b)* Mobilite açıkken PDR ≈ 1
**olamaz** → literatürün **U1** sanity testi yalnız **statik** kolda koşar.

## 3 · Reaktif + aldatıcı karıştırıcı mimariyi değiştiriyor

| sonuç | ne demek |
|---|---|
| Karıştırıcı **zamanın saf fonksiyonu değil** | Reaktif *(16 µs sezme + 144 µs patlama)* durum tutar, **iletim-başladı olayına tepki verir** |
| **Aldatıcı karıştırıcı CSMA'ya görünür** | Geçerli görünümlü önbelge basıyor → taşıyıcı dinleme onu **meşgul görmek zorunda**; eski *"karıştırıcı CSMA'yı tetiklemez"* beyanı bu sınıf için kalkar |
| Parça sayısı | çerçeve başına ~2–4 → **~28**; sönümleme de parça başına çekilecek |

---

# 🔴 ESKİ SİMÜLATÖRÜN ON KUSURU — hepsi ölçüldü, tasarım bunları çözüyor

| # | kusur | durum |
|---|---|---|
| **1** | **İki farklı PER tanımı** — `radio.paket_hata_olasiligi` `8×bayt` (yalnız yük), `mac.alim_per` `süre×bit_hızı` (yük + 192 µs önbelge). 1024 B'da **8192 ↔ 8384 bit = %2,34**. Kâhin PER ile gerçek alım PER'i sistematik ayrışıyor | 🔴 **AÇIK** — Adım 4'te |
| **2** | **Alıcı zinciri kısıtı yok** — bir düğüm zamanda çakışan **iki** çerçeveyi de başarıyla alabiliyor. Tek radyolu telsizde imkânsız | 🔴 **AÇIK** — Adım 6a |
| **3** | **Capture effect / önbelge kilidi yok** | 🔴 **AÇIK** — Adım 6a |
| **4** | **`kosucu.py` tanrı nesnesi** (388 satır kod); `sonuc()` **191 satırlık tek dict literali** → alt parçaları birim test edilemiyor | 🔴 **AÇIK** — Adım 9 |
| **5** | **`mac.py` Kat 2 ile Kat 3'ü karıştırıyor** — `alim_per`, `_girisim_w`, `_parca_sinirlari` aslında kanal fiziği | 🔴 **AÇIK** — Adım 4/6 |
| **6** | **25 sayaç ifadesi iki yerde BİREBİR tekrarlı**; `*_pencere` ikizleri elle tutulan ikinci bir listeydi | 🟢 **KAPANDI** |
| **7** | **RNG akış listesi kapalı** — akış eklemek çekim sırasını kaydırıp önceki **tüm ölçümleri** bayatlatıyordu *(bu yaşandı)* | 🟢 **KAPANDI** |
| **8** | **Sonuç satırı koşuyu/aracı tanımlamıyor** — `kaynak_hash` yalnız `sim/`i kapsıyor, koşu kimliği/zaman damgası yok. Ölçüldü: aynı satırlar 2× okunursa `8/30 · p=0,0161` → `16/60 · p=0,000394` (**41 kat**) | 🟢 **KAPANDI** |
| **9** | **Tek küresel saat** → yapısal kâhin kanalı; bir protokol beacon'a zaman damgası koyarsa bedava kusursuz senkron kazanır ve hiçbir test görmez | 🔴 **AÇIK** — Adım 7 |
| **10** | **7 değişmez `assert` ile** → `python -O` altında sessizce kalkar; dördü sessiz yanlış cevap verir | 🟢 **KAPANDI** |

---

# ✅ BUGÜNE KADAR YAPILAN — ölçüldü, 4 Eylül 2026

## Dosyalar

```
sim2/  (11 dosya, 1 279 satır)
  __init__.py
  cekirdek/
    __init__.py
    degismezler.py    70   dogrula() · dogrula_ayrintili() · asla()  — `assert` yerine
    olaylar.py        93   OlayKuyrugu — (zaman, sıra_no) anahtarı
    korunum.py       149   KorunumDefteri — 5 düşme sebebi (rota_gecersiz DÂHİL)
    rng.py           239   🔒 İKİ LİSTE: AKIS_ADLARI (15) + HASH_ALANLARI (7)
    kimlik.py        146   arac_hash · kosu_kimligi · calisma_kimligi · kurulum_hash · evren_hash
    sayaclar.py      296   🔒 TEK KAYIT DEFTERİ — 31 sayaç + 7 türev
  dunya/
    __init__.py
    geometri.py      113   Nokta3 · Kutu (yansıma) · mesafe · yükseliş açısı
    mobilite.py      173   GaussMarkov3B · Sabit · mobilite_kur()

tests2/  (2 dosya, 759 satır) — 🟢 101 test, 2,15 sn
  test_cekirdek.py   521
  test_dunya.py      238
```

## Parmak izleri *(4 Eylül 2026)*

```
arac_hash          18249519e414b39c3bbdc8199e516ee4
akis_listesi_hash  b3753a98733bd203
sayac_semasi_hash  db49b3ee67bfcb9d
```

⚠️ Bunlar `sim2/` her değiştiğinde değişir; devraldığında **yeniden ölç**,
kopyalama.

## Kapanan üç kusurun kanıtı — hepsi test

| kusur | testi | ne kanıtlıyor |
|---|---|---|
| **7** | `test_YENI_HASH_ALANI_eski_cekimleri_KAYDIRMIYOR` | Hash alanı eklemek 300 eski çekimin hiçbirini değiştirmiyor |
| **10** | `test_degismezler_O_bayragi_altinda_HALA_atesliyor` | Alt süreçte `python -O` ile koşuluyor · `test_sim2_altinda_ciplak_assert_YOK` AST ile tarıyor |
| **6** | `test_IKINCI_bir_sayac_listesi_YOK` · `test_tepe_sayaci_FARKLA_turetilmiyor` | Sayaç adlarının ikinci bir listesi yok; `tepe` sayacı 7→4 veriyor, "7−4=3" değil |

🔒 **Risk 2 de yapısal olarak kapandı:** `pencere_ikizi=False` yazmak artık
`ikizsiz_gerekce` yazmayı **zorunlu** kılıyor *(modül yükleme anında
denetlenir)*. Unutmak imkânsız; kapatmak bilinçli bir eylem.

## Sayaç kayıt defteri — 31 sayaç + 7 türev

Literatürün **asgari metrik kümesinin 7'si de** şemada:
`pdr` · `psr` · gecikme yüzdelikleri *(ham listeden türetilecek)* ·
`nrl_cerceve/bayt/airtime` · `kopma_fiziksel/algilanan/rota_gecersiz` ·
`cor` · **`algilama_duyarliligi`** *(= kopma_algilanan / kopma_fiziksel — risk
3'ün ölçüsü)*.

---

# ⏭️ SIRADA — Adım 3'ten devam

Onaylı plan: `C:\Users\Xelma123\.claude\plans\takvim-umurumda-de-il-gerekirse-polymorphic-bengio.md`
**Onu önce oku.** Aşağısı yalnız özet.

| # | adım | kapanış ölçütü |
|---|---|---|
| **3** | `dunya/topoloji.py` *(zamana bağlı)* + `yapilandirma/konfig.py` | 1000×1000×120 · R=280'de ort. derece ve bağlı oran 30 tohumla raporlanmış, **7,25 / %81,0**'i doğruluyor. Hareket boyunca bağlantılılık zaman serisi ölçülmüş |
| **4** | `kanal/`: `cerceve` → `yayilim` *(+dipol)* → `sonumleme` → `girisim` → `karistirici` → `kanal` | *(a)* sabit girişimde parçalı PER == tek parça *(analitik)* · *(b)* σ=0'da gölgeleme kapalı hâle **birebir** · *(c)* K→∞'da Rician sabite gidiyor · *(d)* sönümleme otokorelasyonu `exp(−kΔt/T_c)` ile ±%10 · *(e)* paket başına ortalama parça ≥ 2 · *(f)* **TEK `per()`** *(AST)* · *(g)* aynı tohumda iki protokol → sönümleme izleri **birebir eşit** |
| **5** | `ag/`: `paket` · `kuyruk` · `trafik` | Kayıpsız kanalda korunum tam. 10–15 akış × 4 pkt/s × 512 B |
| **6a** | `mac/alici.py` | 🔴 Çakışan iki çerçeveden **yalnız biri** alınıyor *(sıfır ihlal)*. Her başarısız alım bir **sebep** taşıyor, `Σ sebep = toplam` |
| **6b** | `mac/dcf.py` | Doygunluk verimi **Bianchi** analitiğiyle ±%15 *(n=5…40)*. `dcf.py`de tek fizik formülü yok *(AST)* |
| **7** | `cekirdek/saat.py` bağlanır + `gozlem/` | Yüzey taraması yasak tipe ulaşamıyor · `olcum.kahin` protokol grafiğinde yok *(AST)* · `saat_senkron` ablasyonu ölçülebiliyor |
| **8** | `olcum/` | 7 metriğin 7'si bir koşudan üretiliyor; her metriğin **bağımsız hesapla** eşleştiği içerik testi var |
| **9** | `kosum/` | `kosu.py` ≤150 satır · `sonuc.py`de tek dict literali yok · satır anında `fsync` |
| **10** | `analiz/istatistik.py` | Wilcoxon · Holm–Bonferroni · GA · **NaN koruması n=30 gerçek örneklemle** |
| **11** | `protokoller/` — doğrulama kolları, sonra AODV · OLSR · AOMDV | 🔒 **U1–U4** *(U1 **statik** kolda)* |
| **12** | 🔒 Ön-kayıt yazılır ve **MÜHÜRLENİR** | Özgün protokol koşulmadan **önce** |
| **13** | `protokoller/ozgun.py` | 🔴 **Öğrencinin tasarım taslağını bekliyor** |

## Adım 3'ün ilk işi — `Konfig`

Öğrenciye son sorulan soru şuydu ve **cevap gelmedi**:

> *"Devam edeyim mi, yoksa `Konfig`in parametrelerini (512 B · 2 Mb/s ·
> menzil 280 m · ısınma/pencere süreleri · karıştırıcı güçleri) önce birlikte
> gözden geçirelim mi?"*

🔴 **Önce bunu sor.** Karıştırıcı güçleri özellikle önemli: eski depodaki
`S2 = +2 dBm` çalışma noktası **2B ve sönümlemesiz** bir dünyada seçilmişti;
yeni fizikte **yeniden türetilmesi** gerekiyor ve ölçütü koşmadan önce ilan
edilmeli.

---

# 🔒 MİMARİNİN BEŞ YAPISAL FİKRİ — bunlara dokunma

| fikir | neyi imkânsız kılıyor |
|---|---|
| **`kanal/cerceve.py::Cerceve`** — `sure_s` ve `hataya_acik_bit` **tek yerde**; `Kanal.per(cerceve, sinr_izi)` tek gövde, kâhin ve gerçek alım **aynı fonksiyon** | Kusur 1 — ikinci bir bit sayımı yazmak |
| **`mac/alici.py::AliciZinciri`** — düğüm başına `bos / onbelge_kilidi / govde_aliyor`; değişmez: **aynı anda en fazla bir kilitli çerçeve** | Kusur 2 ve 3 |
| **`cekirdek/sayaclar.py`** — `SayacTanimi` + `Turev` tek kayıt defteri; anlık görüntü, pencere ikizi ve sonuç **hepsi ondan türer** | Kusur 6 — ikinci bir sayaç listesi |
| **İki RNG listesi** — `AKIS_ADLARI` *(sıralı, kapalı, küçük)* ve `HASH_ALANLARI` *(durumsuz, serbestçe genişletilebilir)*. **Kural: yeni rastgelelik önce hash alanı olarak denenir** | Kusur 7 — akış eklemenin tüm ölçümleri bayatlatması |
| **`olcum/kahin.py::Kahin[T]`** — frozen sarmalayıcı, `.rapora()` dışında okunamaz; `olcum.kahin` protokol içe aktarma grafiğinde **yok** *(AST testi)* | Teşhis ↔ karar kanalının karışması |

## Sönümlemenin durumsuzluğu — 🔴 tasarımın kilit taşı
AR(1) doğal olarak durumludur; durumlu yazılırsa protokolden bağımsızlık ölür.
🔒 **Çözüm: hash'lenmiş yeniliklerin üzerinde FIR**

```
h_k = √(1−ρ²) · Σ_{m=0}^{M−1} ρ^m · w_{k−m}
ρ   = exp(−Δt_parça / T_c)
M   = ⌈ln(0,01) / ln ρ⌉
w   = normal_cekimi("sonumleme_i" | "sonumleme_q", tohum, i, j, k−m)
```

Rasgele erişimli, durumsuz, AR(1) ile aynı istatistik. **Ölçüm:** *(a)* aynı
tohum + iki farklı protokol → sönümleme izleri **birebir eşit** · *(b)* ölçülen
ρ(kΔt) beyanla ±%10 · *(c)* geri kestirilen K ±%10 · *(d)* maliyet payı %15'i
aşarsa `(i,j,k)` anahtarlı **saf memo** *(bağımsızlığı bozmaz)*.

## Saat modeli — kusur 9
Düğüm başına `ofset ~ U(−0,5, +0,5) s` + `sapma ~ N(0, 20) ppm`;
`YerelZaman = NewType(float)` **tip sınırı**.
🔒 **Yasak değil, fizik:** protokol beacon'a zaman damgası koyabilir ama alıcı
ofseti görür — bedava kusursuz senkron **imkânsız** hâle gelir, yasaklanmaz.
Ablasyon: `Konfig.saat_senkron`.

---

# 🔴 ÜÇ RİSK — her birinin ölçüm yöntemi belli

| # | risk | nasıl ölçülür |
|---|---|---|
| **1** | **Sönümlemenin durumsuzluğu** *(yukarıda)* | dört ölçüm, yukarıda |
| **2** | **Otomatik pencere ikizi sessizce eksik ikize dönebilir** | 🟢 **Yapısal olarak kapatıldı** — `pencere_ikizi=False` gerekçe zorunlu kılıyor. Ek olarak `Sayaclar.ikizsiz_rapor()` ısınmada artan ikizsiz sayaçları gerekçesiyle raporluyor |
| **3** | 🔴 **`Beyan` kanalı, kâhin sızıntısının YENİ kapısı** — hiç beyan etmeyen protokolün kopma sayacı 0 çıkar ve **iyi görünür** | *(a)* `algilama_duyarliligi` *(= algılanan/fiziksel)* her koşuda raporlanır; oran 0 ise kol *"beyan etmiyor"* diye **etiketlenir** ve Δ `None` döner · *(b)* 30 tohumda beyan sayısı ↔ PDR korelasyonu ölçülür · *(c)* `olcum/` dışında hiçbir modül `Beyan` içe aktaramaz *(AST)* |
| **4** | Çalışma noktası kayması *(3B + mobilite + sönümleme teslim oranını aralığın ucuna itebilir)* | Kalibrasyonda teslim oranı taranır, orta nokta **ölçütle** seçilir, tohumlar arası std raporlanır |
| **5** | Mobilite yakınsamayı engelleyebilir *(ağ zamanın %26'sında bölünüyor)* | Isınma **ölçülerek** seçilir: erken/geç pencere farkı `isinma_s ∈ {50,100,150,200}` üzerinde koşulur, farkın söndüğü nokta yazılır |

---

# ⚠️ HENÜZ YAPILMADI

| ne | durum |
|---|---|
| **Arşivleme** | 🔴 **YAPILMADI.** `sim/` · `tests/` · `dogrulama/` · `v2/` · `denetim/` · `ciktilar/` **hepsi yerinde**. `arsiv/` dizini yok |
| **Eski paket** | 🟢 Hâlâ çalışıyor: **492 test**, `kaynak_hash = 01cedf62deb99ca7f559861534e11d0a` |
| **`v2/` belgelerinin yeniden yazımı** | 🔴 **YAPILMADI** — 14 belge → 8 belge planı onaylı ama uygulanmadı |
| **`tests2/` → `tests/` adlandırması** | 🔴 Eski `tests/` yerinde olduğu için yeni testler `tests2/`de. Arşivleme yapılınca `tests/` olacak |

🔒 **Arşivleme ne zaman:** `sim2/` en az Adım 6'ya kadar geldiğinde. Şu an
eski `sim/` hâlâ tek çalışan referans; erken arşivlemek karşılaştırma
imkânını kaybettirir.

## Belge yeniden yapılandırma planı *(onaylı, uygulanmadı)*

| yeni | kaynağı |
|---|---|
| `00-PROBLEM.md` | eski `01` — 🔴 **modelin sınırları burada ve `05`e atıf** |
| `01-YONTEM.md` | eski `03`, seremoni çıkarılmış |
| `02-GOZLEM-SOZLESMESI.md` | eski `05` + **saat modeli** |
| `03-MIMARI.md` | eski `07` — katmanlar · RNG akışları · sayaç kaydı · sonuç şeması |
| `04-ON-KAYIT.md` | eski `06`, **yeniden** *(eski H1.1/H1.2/H1.3 sabit topolojiye dayanıyordu)* |
| `05-KAPSAM.md` | eski `08`, **yeniden** — her madde **yönüyle ve ölçülmüş büyüklüğüyle** |
| `06-KARARLAR.md` | eski `04` yerine, **sıfırdan** |
| `07-YOL-HARITASI.md` | eski `12` |

---

# 📚 ESKİ DEPODAN NE OKUNMALI

Eski `v2/` belgeleri **arşive gidecek** ama üçü hâlâ değerli:

| dosya | neden |
|---|---|
| `v2/10-LITERATUR-KOD-KARSILASTIRMA.md` *(1 066 satır)* | Literatürün ne istediği · 68 yargı satırı · **Boşluk A ve Boşluk B**'nin tanımı |
| `v2/yeni_detaylı_arastırma/` *(20 dosya, 5 271 satır)* | Ham literatür taraması. 🔴 8. denetim *"bu dizin depoda yok"* dedi — **YANLIŞ**, dizin var; kökü listeleyip `v2/` altına bakmamışlardı |
| `v2/08-AILE0-KAPSAM.md` *(530 satır)* | 37 maddelik *"neyi modellemiyoruz"* listesi — yeni `05-KAPSAM.md`in iskeleti |

🔴 **`aile0_audit.md` (11 595 satır) OKUNMAYACAK.** Öğrencinin kararı: *"aile
auditi tamamen unutuyoruz artık o eski simülatöre ait."*

---

# ⚠️ ORTAM TUZAKLARI — hepsi bu depoda yaşandı

| tuzak | çözüm |
|---|---|
| Konsol Türkçe karakterde çöküyor | Her çağrıda **`PYTHONIOENCODING=utf-8`** |
| Windows `spawn` | `Pool` açan her betikte `if __name__ == "__main__":`. 🔴 **stdin'den (`python -`) çalıştırma — havuz ASILIR.** Dosyaya yaz, öyle koştur. Ve **yazıcı EBEVEYNDE kalır** |
| 🔴 Uzun heredoc | Bash'te **parse hatası veriyor** — bu oturumda da oldu. Uzun metni **dosya yazma aracıyla** yaz |
| Metin varlığı denetleyen `assert` | 🔴 **Kendi yorumuna takılır.** Doğrulamayı **AST** ile yap. *(Bu oturumda `grep` üç göreli `sys.path` buldu, biri metin sabitinin içindeydi; AST iki dedi ve AST haklıydı.)* |
| Türkçe karakter eşleşmesi | `replace` deseninde `yon` ile `yön` farklıdır — bu oturumda bir kez tutmadı |
| Süre tahmini | 🔴 Eski depoda **altı kez** tutmadı. İş listesinin **ilk** elemanıyla kalibre etme — hep en ucuz hücredir. 🟢 Üç eksenli kalibrasyonla **iki kez tuttu** *(tahmin 8,7–18,3 dk ↔ ölçülen ~13 dk; 1,8–3,8 dk ↔ 3,7 dk)* |
| Makine oynaklığı | Aynı kod, aynı paket **2,32 kat** oynuyor *(1,888–4,385 sn/test)*. Her tahmin bir **BANT**tır |

---

# 🔴 ÇALIŞMA BİÇİMİ

```
1. KONUM      : Neredeyiz
2. HEDEF      : Bu oturumda ne bitecek (tek, net çıktı)
3. YAPI       : Ne yazılacak, neden, arayüzü ne — ONAY BEKLENİR
4. UYGULAMA   : Kod (yalnızca onaydan sonra)
5. DOĞRULAMA  : Nasıl test edildi, kapanış ölçütü geçti mi
6. SONRAKİ    : Sonraki adım + yeni risk
```

**Bir modül ne zaman "bitmiş" sayılır — üçü birden:**
1. Kapanış ölçütü **koşularak** geçildi
2. Değişiklik **kodda** doğrulandı *(betik çıktısına güvenilmez)*
3. Geri alındığında **konuşan bir test** var

**Öğrenci hakkında:** tam zamanlı çalışıyor · **doğrulama konusunda ısrarcı ve
bu ısrar defalarca haklı çıktı** · pasif bir proje istemiyor · **kararlar
onun**; danışman seçenekleri ve ölçüm yöntemini sunar. Bir kararı sana
devrederse, kararı ver **ama devredildiğini açıkça kaydet**.

---

# ✅ DEVRALDIĞINI GÖSTER — 6 soru

Okumayı bitirince **kendi cümlelerinle** cevapla. 🔴 Kopyalama.

1. Eski simülatörde **iki farklı PER tanımı** vardı. İkisi neyde ayrışıyordu,
   fark ne kadardı, ve yeni tasarım bunu neden **yapısal olarak** imkânsız
   kılıyor?
2. **`AKIS_ADLARI` ile `HASH_ALANLARI` arasındaki fark** ne, ve bu ayrım hangi
   somut felaketi önlüyor?
3. Sönümleme neden **paket başına değil parça başına** çekiliyor? Sayıyla
   açıkla.
4. **Anten deseni kararı ölçümle çevrildi.** Ne ölçüldü, hangi yönde çevirdi?
5. Mobilite açıkken **U1 sanity testi neden statik kolda koşmak zorunda**?
6. 🔴 **`Beyan` kanalı neden yeni bir kâhin kapısı**, ve hangi sayaç onu
   ölçüyor?

---

> **Bir şeyi büyütmek istiyorsan önce ölç.**
>
> Bu proje **kanıt üreterek** ilerliyor: hiçbir cümle *"gözden geçirildi"*
> demiyor, hepsi bir komutun çıktısına bağlı. Devraldığın şey bir kod tabanı
> değil — **savunulabilir bir ölçüm zinciri.** Halkayı sen de öyle ekle.
