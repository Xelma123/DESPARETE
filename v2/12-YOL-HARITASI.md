# 12 · DURUM VE YOL HARİTASI

> Projenin durumu ve planı YALNIZ burada tutulur; başka belgeler buraya atıf verir. Güncel: 10 Ekim 2026. Onaylı plan Faz 0–7 (25 Eylül, K-168). Kararlar `04`, tarihçe `kayit/KARAR-GUNLUGU.md`.

## 1 · Nerede duruyoruz

| | |
|---|---|
| **faz** | **5 · DESPARETE** — sıradaki iş 5.0 (§1.1). Faz 5'e geçiş kapısı KAPANDI (K-226, 10 Ekim): bağımsız denetimin (8 Ekim, `arsiv/denetim/DENETIM-RAPORU-2026-10-08.md`) kararları ve düzeltmeleri K-222…K-226. Faz 4 KAPANDI (K-221) |
| simülatör | referans dünya (`14`) tamam; birincil hücrede 350 s'lik koşu tek süreçte ~1 sa, 8 işçide koşu başına 1–2 sa (K-198, K-200) |
| taban protokoller | **DONDU (K-224, 10 Ekim):** `AODV-j` · `OLSR-d` · `AOMDV-f`, en çok 7 iletim denemesi — U1-U iki desende geçti, yere toplamada U1-B temiz (açıklanmış hücreler K-207 · K-196, anatomiyle) |
| DESPARETE | v0.4.1; birincil hücrede ilk ölçüm pencere PDR'si 0,700 (AODV 0,556, kâhin 0,813; 4 geliştirme tohumu, K-200 — eski kod, 5.0'da yeniden ölçülür); açık evrede AODV'ye üstünlüğü küçük (K-224) |
| doğrulama | `982 passed` (10 Ekim) · mimari denetimi ihlalsiz · regresyon tabanı **`k223`** (K-224) · R = **0,0126** (K-224, 7 deneme) · köken sayımı `04` §9 |
| arkada koşan | Faz 5.0 kayıp anatomisi — 10 Ekim 17:33'ten, ~5 sa (`arsiv/teshis/faz5_0_2026-10-10/`, beklenti commit `075ce8a`) |
| takvim | mühür ~12 Kasım · teslim 19 Aralık 2026 |

### 1.1 · Sıradaki iş — Faz 5.0

> **Kural (29 Eylül):** bir faza geride iş kalmadan, yazılım ve yapı denetiminden geçmiş bir simülatörle ve güncel belgelerle geçilir; fazlar paralel yürümez. Faz 4 bu kapıdan geçti (K-221); Faz 5'e geçiş bağımsız denetimden ve düzeltmelerinden sonra (K-226).

1. **Faz 5.0 · kayıp anatomisi** — birincil hücrede taban protokoller, kâhin ve DESPARETE v0.4.1: paket nerede ve neden ölüyor; Faz 5'in mekanizma hedefleri buradan çıkar. Alet hazır (`kalibrasyon/kayip_anatomisi.py`, K-202 + onarım bölümleri ve `rota_gecersiz` anında alan durumu). `arsiv/teshis/faz5_0_2026-09-30/`daki kopya ve beklenti K-215 öncesi koda ve pencere PDR'sine ait → beklenti `PDR_açık`a göre yeniden yazılır (önkoşullar §2), kopya bugünkü koddan (K-224) yeniden dondurulur, ölçüt ölçmeden önce commit'le girer, süre önce hesaplanır.
2. Sonra 5.1 → 5.7 (§2 tablosu); her mekanizma ablasyon bayrağıyla ve önceden yazılı beklentiyle.

## 2 · Fazlar

**Faz 0 · Referans dünya ✓** (25 Eylül): `14` onaylandı (K-169), yapı paketi onaylandı (K-170; artık `arsiv/`).
**Faz 1 · Fizik ve MAC gerçekçiliği ✓** (26 Eylül): işlem kazancı · ED-CCA · ARF · yayılım gecikmesi · gerçekçi karıştırıcı · 1:1 girdiler (K-171…K-181).
**Faz 2 · Gözlem sözleşmesi v2 ✓** (26 Eylül): RSSI · kulak misafiri · kanal doluluğu · PHY hatası · kendi GPS/INS (K-172, K-179, K-180).
**Faz 3 · Senaryo eksenleri ✓** (26 Eylül): düğüm kaybı · trafik yoğunluğu · enerji (K-180, K-182).

### Faz 4 · Yeniden kalibrasyon ve doğrulama ✓ (8 Ekim, K-221)

| # | iş | durum |
|---|---|---|
| 4.1 | çalışma noktası: alan 33 km, N 40, karıştırıcı rejimi ve birincil hücre, görev yarıçapı 16 km | ✓ K-185…K-188 |
| 4.2 | doğrulama: Li (sabit hızda tuttu), Bianchi, PER eğrileri, kâhin tavanı | ✓ K-187 |
| 4.3 | taban protokoller: kara liste ✓ · AOMDV U1–U4 ✓ · evre metriklerinin boş kol kapısı ✓ · OLSR teşhisi ✓ · birincil hücrede §13 (kapalı kalır) ve rota tamponu (bağlamıyor) ✓ K-200 → **U1 yeni kod hâlleriyle** (yere toplama + eşler arası) → **taban protokoller DONAR** | ✓ K-218 (denetimden sonra `OLSR-d` ve 7 denemeyle yeniden, K-224) |
| 4.4 | köken defteri referans dünyaya göre (K-203) · kapsam ilanı (K-204, K-215) · R (bugün 0,0126, K-224) · 22 parametre ölçümle ya da kararla kapandı · Rician K eksen · TTL 64 · kâhin 48 örnek · AODV-j | ✓ K-213…K-220 |
| 4.5 | doğrulama listesinin referans dünyada anlamlı kısmı bir kez · iş başına süre (bütçe) | ✓ K-219 (son kodla yeniden K-226) |

### Faz 5 · DESPARETE — karıştırmayı gerçekten çözen protokol (sıradaki faz)

| # | mekanizma | ne çözer |
|---|---|---|
| 5.0 | **kayıp anatomisi** — birincil hücrede taban protokoller, kâhin, v0.4.1: paket nerede, neden ölüyor (ilk ölçüm K-200; etki alanı ve DESPARETE sayaçları K-202) | hedefleri ölçümle koyar |
| 5.1 | **karıştırma kanıtı** (taslaktaki C_jam) — komşu başına RSSI × teslim tutarlılığı, kanal doluluğu, PHY hatası; komşununki ilanda, bedeli ödenerek. "Karıştırıcı tespiti" iddiası yok | karıştırılan bağdan kopmadan önce kaçmak |
| 5.2 | **öngörülü kaçınma** — konum/hızdan bağ ömrü tahmini | hareketle kopan bağı önceden bırakmak |
| 5.3 | **kanıta dayalı postür** — CAUTION/PROTECT kanıtla, histerezisle; yanlış kriz oranı ölçülür | savunma modunun doğru anda açılması |
| 5.4 | **PROTECT = seçici çok yol + çoğaltma** — farklı ilk atlamalara sınırlı bütçeyle kopya, hedefte tekilleştirme (simülatöre kopya kalemi) | ani bağ kaybında paketi kurtarmak |
| 5.5 | **pasif bakım** — kulak misafiri + DATA'da potansiyel/DFSN | kontrol yükü ve bayat bilgi |
| 5.6 | **canlılık ve yük** — periyodik DFSN, onarım kotası, sabitler köken defterine | canlılık |
| 5.7 | **kapanış** — profil v0.5 donar · resmi U1 + U3 · tasarım paketi güncellenir | protokolün çıkışı |

Her mekanizma: ablasyon bayrağı · önceden yazılı beklenti (iki ölçütle: birincil hücrede `PDR_açık` artışı **ve** karıştırıcısız kolda zarar yok) · geliştirme tohumları 1003–1010 · birincil hücre + **dayanıklılık hücresi** (10 s açık · 20 s sessiz; zaman sabitleri tek çizelgeye ayarlanmasın) + bir yer karıştırıcılı aile (K-222, denetim D-08).
**Öncelik (K-222):** karıştırmaya özgü olanlar önce — 5.1 → 5.3 → 5.4; **5.2 keşifsel** (formasyonda bağ hareketle kopmuyor, Θ tanımsız — birincil testte kazanç gösteremez; bağımsız/görev kollarında); 5.5 · 5.6 yalnız kontrol yükü ya da canlılık sorun çıkarırsa.
**Önkoşullar:** 5.0'ın beklentisi `PDR_açık`a göre yeniden yazılır (5 kol: AODV · AOMDV · OLSR · DESPARETE · kâhin; önce/açık/sessiz; açık evre kaybının bölgesi ve sebebi — denetim D-22) · gürültü gözlemi kilitli kalır, 5.1'in kanıtı kanal doluluğu, PHY hatası, MAC sonucu ve RSSI'den (K-227; D-04 kapandı) · 5.4'ten önce çoğaltmanın PDR, korunum ve fatura tanımları yazılır (D-23).

### Faz 6 · Ön-kayıt ve mühür (~5–12 Kasım)

δ için gürültü ölçümü (3 taban × 20 tohum 1100–1119, birincil hücre) · güç benzetimi ve tohum sayısı · ön-kayıdın kesinleşmesi (`06`): birincil metrik KR-2 (karar), hipotezler, Aile 3 kolları, çekirdek matris, durdurma kuralı, fark-içinde-fark eşiği · pencere üçlüsü (ısınma · ölçüm bitişi · koşu bitişi; SINANMAMIŞ 3) · ana deneyin penceresinde R ve DUYARSIZ hükümlerinin yeniden okunması (δ koşularından, denetim D-03) · uzun bağlarda slot zamanlamasının duyarlılığı (D-11) · kâhinin 96 sönümleme örneğiyle yakınsaması (D-15) · `06` H1.3'ün aldatıcı ↔ sürekli kontrastı referansta yeniden düşünülür (10 W aldatıcı ED'yle bütün ağı susturuyor, K-219) · Rician K ekseninin keşifsel tekrarı (6 · 15 dB, K-215) · **mühür**.

### Faz 7 · Ana deney ve yazım (12 Kasım–19 Aralık)

Ana deney 40 tohum (birincil hücre + Aile 1 hücreleri + Aile 3 kolları; keşifsel eksenler az tohumla) · yazım Kasım başında başlar, sonuç bölümleri ana deneyden sonra · simülasyonun görselleştirilmesi · jüri soru bankası · TÜBİTAK biçim gereklilikleri.

## 3 · Hesap bütçesi

Ölçülen (K-200, birincil hücre, 350 s, 8 işçi aynı anda): kâhin 50–60 dk · OLSR 52–90 dk · AOMDV 95–130 dk · AODV 105–140 dk · DESPARETE 115–130 dk koşu başına; 32 koşu 7,1 sa (≈ 4,5 koşu/sa). Statik karıştırıcısız koşu ~15 dk. Tek makine.

**Kaba plan** (denetim D-09; birim süreler yukarıdan):

| iş | koşu | süre |
|---|---|---|
| Faz 5: 5.0 (~20) · 5.1 · 5.3 · 5.4 × (açık/kapalı × 8 tohum × 3 hücre) × ~2 deneme · 5.7 (U1, U3) | ~350 | ~80 sa |
| Faz 6: δ gürültüsü (3 taban × 20) · pencere üçlüsü · tam pencere R ve DUYARSIZ'ların yeniden okunması · Rician 6 · 15 dB · kâhin 96 örnek | ~200 | ~45 sa |
| Faz 7: birincil 5 kol × 40 · karıştırıcısız ikiz 5 × 40 · dayanıklılık hücresi 5 × 40 · Aile 3 (≤ 3 kol × 40) · Aile 1 (≤ 2 hücre × 3 protokol × 40) | ~960 | ~210 sa |

Faz 7'nin hesabı tek başına ~9 gün kesintisiz → Faz 7 mühürden hemen sonra başlar, yazım hesapla paralel yürür.

## 4 · Riskler

- **Yeni dünya yönlendirmeye iş bırakmazsa** (ağ tek atlamaya iner ya da hep bölünür): geometri kaynaklı zarf içinde ayarlanır; karar kayda geçer.
- **Mekanizmalar kazanç göstermezse:** dürüst negatif sonuç; neden çalışmadığı ölçülür.
- **Takvim ve hesap:** Aralık başında ~1 hafta tampon. Düşme sırası (önceden yazıldı, K-222): keşifsel eksenler (20 tohumla yetinilir: Rician 6 · 15 dB, eşler arası, hava eşlik) → görselleştirmenin zenginliği → Aile 1 hücreleri (en çok 2) → Aile 3 kol sayısı (en çok 3) → dayanıklılık hücresi 20 tohuma. Güç benzetimi n > 40 isterse önce Aile 1 düşer, sonra dayanıklılık hücresi. Korunanlar: birincil hücre ve karıştırıcısız ikizi, üç taban protokol, DESPARETE, 40 tohum.
- **Tek makine:** her ölçümden sonra commit + push (denetim D-05); elektrik kesintisinde uzun kuyruk biten adımları atlayarak sürer.

## 5 · Gelecek çalışma olarak beyan edilecekler

Komutların yönlendirilmesi · iki geçit · ~2 000 s'lik uzun koşu · protokol farkında karıştırıcı · GPS karıştırması ve aldatması · RTS/CTS · OFDM telsizler · derin öğrenme · GPSR · gerçek RF/SDR/uçuş testi.
