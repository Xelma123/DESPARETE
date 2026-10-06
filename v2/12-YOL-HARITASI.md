# 12 · DURUM VE YOL HARİTASI

> Projenin durumu ve planı YALNIZ burada tutulur; başka belgeler buraya atıf verir. Güncel: 6 Ekim 2026. Onaylı plan Faz 0–7 (öğrenci, 25 Eylül, K-168). Kararlar `04`, tarihçe `kayit/KARAR-GUNLUGU.md`.

## 1 · Nerede duruyoruz

| | |
|---|---|
| **faz** | **4 · yeniden kalibrasyon ve doğrulama → KAPANIŞ** — 4.1 ✅ · 4.2 ✅ · 4.3'te yalnız U1 kaldı · 4.4–4.5 sırada · ardından kapanış denetimi (§1.1). Planın takviminden ~2 hafta önde |
| simülatör | referans dünya (`14`) tamam; birincil hücrede 350 s'lik koşu tek süreçte ~1 sa, 8 işçide koşu başına 1–2 sa (K-198, K-200) |
| taban protokoller | **DONDU (K-211), sadakat düzeltmesi K-215:** `AODV-j` · `OLSR-c` · `AOMDV-f`. AODV kural kural RFC'ye sadık (K-208, K-210), başlangıç durumu yerel saatten bağımsız (K-215) · AOMDV'nin RFC tabanı hizalandı, kara delik giderildi (K-210) · U1 K-215'ten sonra yeniden koşulacak |
| DESPARETE | v0.4.1; birincil hücrede ilk ölçüm PDR 0,700 (AODV 0,556, kâhin 0,813; 4 geliştirme tohumu, K-200) |
| doğrulama | `976 passed` (6 Ekim, K-215 kodu) · mimari denetimi ihlalsiz · regresyon tabanı **`k215`** (K-216) · R = **0,0142** (K-216) · SINANMAMIŞ 12 · duyarlılık borcu 0 · kapsam ilanı 12 |
| arkada koşan | **kuyruk B** (6 Ekim 22:32'den ~22 sa): sınırdaki 6 parametre 20 tohumla (3 parti) → protokol kontrolleri → U1 yere toplama → U1 eşler arası → evre kapıları 1c · 2c — `arsiv/teshis/faz4_4_k215_2026-10-06/` (`zaman.txt`, adım başına bir çıktı; ölçütler `beklenti.md`) |
| takvim | mühür ~12 Kasım · teslim 19 Aralık 2026 |

### 1.1 · Sıradaki iş — Faz 4 kapanışı (yeni ajan buradan başlar)

> **Kural (öğrenci, 29 Eylül):** Faz 5'e geride iş kalmadan, yazılım ve yapı denetiminden geçmiş bir simülatörle ve güncel, arınmış belgelerle geçilir. Faz 5'le paralel iş yok.

1. ✅ **U1 aracı:** kâhin desen başına bir kez, birden çok protokol tek çağrıda, ara kayıt ve kaldığı yerden sürme (K-202).
2. ✅ **U1 ve donma** (K-205…K-211): taban protokoller `AODV-i` · `OLSR-c` · `AOMDV-e` DONDU. Ayrıntı `arsiv/teshis/u1_2026-09-29/`, `aodv_sadakat_2026-09-30/`.
3. **Faz 4.4** — ✅ köken defteri (K-203) · kapsam ilanı (K-204) · R birincil hücrede **0,0188** (K-213) · 19 parametre kâhinle tarandı; TTL, kuyruk ve saat taban protokollerle; kâhinin sönümleme örneği yakınsaması; konum/RSSI birebirliği (K-214). Sonuçlar `arsiv/teshis/faz4_4_2026-09-30/beklenti.md` Sonuç 3–7. Kalan, SIRAYLA:
   - **a · Kararlar ✅ (öğrenci, K-215):** TTL kaynağa bağlandı → 64 (RFC 1700, ns-3; `02` G17) · kâhinin sönümleme örneği platoya (öneri 48; 6 örnekte yakınsamamış, U1 oranları şişik) · AODV başlangıç çapası düzeltmesi (yamalı kopyada sınandı: saat ofsetine birebir değişmez, Sonuç 8) · kâhin beacon'ı AODV HELLO'suna (1 s · 20 B, RFC 3561) · Rician K: eksen mi dünya tanımı mı · en kısa yol kâhininin eşiği aletin tanımı · görev müfreze sayısı ve GM eğimi kapsam ilanı · G2ç'nin D maddesi (boş kola eşleştirme).
   - **b · Kod tek partide** ✅ (K-215; 976 test, mimari temiz) · regresyon k215 58/58 birebir ✅ (K-216).
   - **c · R yeniden** ✅ 0,0142 (K-216).
   - **d · Sınırdaki 6 parametre 20 tohumla** (gölgeleme hücresi, mobilite adımı, kanal dilimi, yakalama eşiği, CBR titreşimi, istasyon tutma) — ~7–8 sa, partili.
   - **e · U1 yeniden** — üç taban protokol + kâhin, iki desen; açıklanmış düşük hücre kayıtları yeniden — ~10 sa.
   - **f · Evre kapıları** — G2ç düzeltmesiyle 2c yeniden (+ tohum 1003'ün boş kol koşusu) — ~3 sa.
   - **g · Köken defteri** — duyarlı çıkanlar eksen / kaynak / kapsam; SINANMAMIŞ yalnız pencere üçlüsü (Faz 6).
4. **Faz 4.5** — eski doğrulama listesinin referans dünyada anlamlı kısmını ayıkla ve bir kez koş.
5. **Yazılım ve yapı denetimi:** simülatör projenin kapsamına yetiyor mu — ön-kayıdın ve hipotezlerin ölçmek istediği her şey referans dünyada ölçülebiliyor mu (çizelgeli karıştırıcıda evre metrikleri: v1 eldeki veriyle sınanıp geri çekildi, **v2 öğrenci onayında** — `arsiv/teshis/faz4_kapanis_2026-09-30/evre_cizelgeli_oneri.md`); kod: ölü kod, eski dünyaya bağlı aletler, bayat yorum ve adlar (`iletim_menzili_m`); tam takım + regresyon (yeni taban) + mimari denetimi.
6. **Dosya ve belge temizliği:** bağlam zehirlenmesi yaratacak bayat anlatılar arşive; kod yorumlarındaki tarihçe anlatıları kısaltılır (davranış aynı, regresyonla); belgeler tek kaynak ve güncel; devir istemi.
7. **Faz 4 kapanış kaydı** (K) → Faz 5.

Faz 5.0'ın aleti hazır (K-202 ve 29 Eylül gecesi eki: onarım bölümleri, `rota_gecersiz` anında alan durumu); ölçümü Faz 5'in ilk işi — kopya, beklenti ve karar kuralı `arsiv/teshis/faz5_0_2026-09-30/` (koşulmadı).

## 2 · Fazlar

**Faz 0 · Referans dünya ✅** (25 Eylül): `14` onaylandı (K-169), yapı paketi onaylandı (K-170; artık `arsiv/`).
**Faz 1 · Fizik ve MAC gerçekçiliği ✅** (26 Eylül): işlem kazancı · ED-CCA · ARF · yayılım gecikmesi · gerçekçi karıştırıcı · 1:1 girdiler (K-171…K-181).
**Faz 2 · Gözlem sözleşmesi v2 ✅** (26 Eylül): RSSI · kulak misafiri · kanal doluluğu · PHY hatası · kendi GPS/INS (K-172, K-179, K-180).
**Faz 3 · Senaryo eksenleri ✅** (26 Eylül): düğüm kaybı · trafik yoğunluğu · enerji (K-180, K-182).

### Faz 4 · Yeniden kalibrasyon ve doğrulama 🟡

| # | iş | durum |
|---|---|---|
| 4.1 | çalışma noktası: alan 33 km, N 40, karıştırıcı rejimi ve birincil hücre, görev yarıçapı 16 km | ✅ K-185…K-188 |
| 4.2 | doğrulama: Li (sabit hızda tuttu), Bianchi, PER eğrileri, kâhin tavanı | ✅ K-187 |
| 4.3 | taban protokoller: kara liste ✅ · AOMDV U1–U4 ✅ · evre metriklerinin boş kol kapısı ✅ · OLSR teşhisi ✅ · birincil hücrede §13 (kapalı kalır) ve rota tamponu (bağlamıyor) ✅ K-200 → **U1 yeni kod hâlleriyle** (yere toplama + eşler arası) → **taban protokoller DONAR** | 🟡 |
| 4.4 | köken defteri referans dünyaya göre ✅ (K-203) · borç 0, 10 keşifsel kol tanımı kapsam ilanı ✅ (K-204) · R ✅ (K-213) · taramalar ✅ (K-214) → kararlar, kod, R, sınırdakiler, U1, evre kapıları (§1.1/3) | 🟡 |
| 4.5 | doğrulama listesinin referans dünyada anlamlı kısmı bir kez (`DEVIR-PROMPT.md` §5) · iş başına süre (bütçe) | ⏳ |

### Faz 5 · DESPARETE — karıştırmayı gerçekten çözen protokol ⏳

| # | mekanizma | ne çözer |
|---|---|---|
| 5.0 | **kayıp anatomisi** — birincil hücrede taban protokoller, kâhin, v0.4.1: paket nerede, neden ölüyor (ilk ölçüm K-200; etki alanı ve DESPARETE sayaçları K-202) | hedefleri ölçümle koyar |
| 5.1 | **karıştırma kanıtı** (taslaktaki C_jam) — komşu başına RSSI × teslim tutarlılığı, kanal doluluğu, PHY hatası; komşununki ilanda, bedeli ödenerek. "Karıştırıcı tespiti" iddiası yok | karıştırılan bağdan kopmadan önce kaçmak |
| 5.2 | **öngörülü kaçınma** — konum/hızdan bağ ömrü tahmini | hareketle kopan bağı önceden bırakmak |
| 5.3 | **kanıta dayalı postür** — CAUTION/PROTECT kanıtla, histerezisle; yanlış kriz oranı ölçülür | savunma modunun doğru anda açılması |
| 5.4 | **PROTECT = seçici çok yol + çoğaltma** — farklı ilk atlamalara sınırlı bütçeyle kopya, hedefte tekilleştirme (simülatöre kopya kalemi) | ani bağ kaybında paketi kurtarmak |
| 5.5 | **pasif bakım** — kulak misafiri + DATA'da potansiyel/DFSN | kontrol yükü ve bayat bilgi |
| 5.6 | **canlılık ve yük** — periyodik DFSN, onarım kotası, sabitler köken defterine | canlılık |
| 5.7 | **kapanış** — profil v0.5 donar · resmi U1 + U3 · tasarım paketi güncellenir 🟦 | protokolün çıkışı |

Her mekanizma: ablasyon bayrağı · önceden yazılı beklenti · geliştirme tohumları 1003–1010 · birincil hücre + bir yer karıştırıcılı aile.

### Faz 6 · Ön-kayıt ve mühür ⏳ (~5–12 Kasım)

δ için gürültü ölçümü (3 taban × 20 tohum 1100–1119, birincil hücre) · güç benzetimi ve tohum sayısı · ön-kayıdın kesinleşmesi (`06`): birincil metrik KR-2 🟦, hipotezler, Aile 3 kolları, çekirdek matris, durdurma kuralı · çözünürlük referans dünyada · **mühür**.

### Faz 7 · Ana deney ve yazım ⏳ (12 Kasım–19 Aralık)

Ana deney 40 tohum (birincil hücre + Aile 1 hücreleri + Aile 3 kolları; keşifsel eksenler az tohumla) · yazım Kasım başında başlar, sonuç bölümleri ana deneyden sonra · simülasyonun görselleştirilmesi · jüri soru bankası · TÜBİTAK biçim gereklilikleri.

## 3 · Hesap bütçesi

Ölçülen (K-200, birincil hücre, 350 s, 8 işçi aynı anda): kâhin 50–60 dk · OLSR 52–90 dk · AOMDV 95–130 dk · AODV 105–140 dk · DESPARETE 115–130 dk koşu başına; 32 koşu 7,1 sa. Tek süreçte bir koşu ~1 sa. Ana deney (40 tohum × ~5 kol ≈ 200 koşu) ~40–45 sa kesintisiz. Statik karıştırıcısız koşu ~15 dk.

## 4 · Riskler

- **Yeni dünya yönlendirmeye iş bırakmazsa** (ağ tek atlamaya iner ya da hep bölünür): geometri kaynaklı zarf içinde ayarlanır, öğrenciye sorulur.
- **Mekanizmalar kazanç göstermezse:** dürüst negatif sonuç; neden çalışmadığı ölçülür.
- **Takvim:** Aralık başında ~1 hafta tampon. Düşme sırası: keşifsel eksenler → görselleştirmenin zenginliği → Aile 3 kol sayısı → çekirdek hücre sayısı. Korunanlar: birincil hücre, üç taban protokol, DESPARETE, 40 tohum.

## 5 · Gelecek çalışma olarak beyan edilecekler

Komutların yönlendirilmesi · iki geçit · ~2 000 s'lik uzun koşu · protokol farkında karıştırıcı · GPS karıştırması ve aldatması · RTS/CTS · OFDM telsizler · derin öğrenme · GPSR · gerçek RF/SDR/uçuş testi.
