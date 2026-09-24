# 12 · YOL HARİTASI — durum ve plan

> **Güncel:** 23 Eylül 2026 · **Türü:** durum ve plan.
> Buradaki süreler ölçüm değil **tahmindir** ve bant olarak verilir; rapora
> değil plana girer. Ölçülmüş sayıların yanında üretici komutları yazılıdır.
> Önceki sürüm (emekli `sim/` planı dâhil): `arsiv/12-YOL-HARITASI-2026-09-10.md`.

---

## 1 · Nerede duruyoruz

| | |
|---|---|
| aşama | **3 · Özgün protokol** (`01` §5) — DESPARETE v0.1'in gerçeklenmesi, 23 Eylül 2026'da başladı. Aşama 1 ve 2 bitti (üç taban protokolün sonuncusu 22 Eylül'de kapandı — plandaki "Ekim ortası"nın önünde) |
| yazılmış yönlendirme protokolü | 🟢 **AODV — KAPANDI** (`AODV-e`, 19 Eylül, K-145; K-140'ın kapanışı K-143'te geçersizleşmişti) · 🟢 **OLSR — KAPANDI** (`OLSR-b`, 22 Eylül, K-147; RFC 3626 §13 öğrenci kararıyla uygulandı, K-146) · 🟢 **AOMDV — KAPANDI** (`AOMDV-a`, 22 Eylül, K-149; makale + RFC 3561, öğrenci seçeneği a). 🟢 **Üç taban protokol de kapandı.** 🟡 **DESPARETE** (23 Eylül): biçimler ve M0.1 (K-152) · komşu yaşamı (K-154) · alan ve ardıl (K-155) · edinim ve onarım (K-156) · paket kimliği ve alan kotası (K-157) · postürler (K-158) · ablasyon bayrakları (K-159) yazıldı — veri ve komutlar DESPARETE'yle taşınıyor · 🔴 kabul kapısında tam ölçekte çöküş ölçüldü (K-160): sebep komut hedeflerinin alanları → 🟢 öğrenci C'yi seçti (v0.1 yalnız geçit alanı, komutlar düşer); U1 sırada (§5) |
| trafik yükü | yere toplama 39×1,0 + 4×0,25 = 40,0 pkt/s · eşler arası 10×4,0 = 40,0 pkt/s (İKİ DESEN EŞİT YÜKTE) — `python -u kalibrasyon/yere_toplama_yuku.py` (15 Eylül, C3) |
| test takımı | **`643 passed`** — `python -m pytest tests2 -q` (23 Eylül, K-151 kapanışı; 626 s) · DESPARETE'nin ilk iki parçasıyla (M0.1 · biçimler, K-152) `tests2/test_desparete.py` **118 passed** (3.5 dâhil, K-156); tam takım **`761 passed`** (23 Eylül, 3.5 sonrası; 701 s; beklentiyle birebir) → **`768 passed`** (23 Eylül, K-157 sonrası; 1 513 s; `test_desparete.py` 122; beklentiyle birebir) → **`779 passed`** (23 Eylül, K-158 sonrası; 717 s; `test_desparete.py` 133; beklentiyle birebir) → **`790 passed`** (23 Eylül, K-159 sonrası; 653 s; `test_desparete.py` 144; beklentiyle birebir) → **`795 passed`** (24 Eylül, K-160; 754 s; `test_desparete.py` 149; beklentiyle birebir) → **`798 passed`** (24 Eylül, K-160 §12 C; 630 s; `test_desparete.py` 152; beklentiyle birebir) → **`810 passed`** (24 Eylül, K-165 sonrası, v0.3 varsayılanıyla; 799 s; `test_desparete.py` 164) |
| regresyon tabanı | **`k151`** · 45 vaka, 45/45 geçerli — `python -u kalibrasyon/regresyon_satirlari.py uret <etiket>` (23 Eylül, K-151 §7; 23,5 dk / 8 işçi; `k144` ile önceden yazılan beklentiyle BİREBİR, çıkış 0 — yeni vaka `j-` K-151'in iki yolunu sınar) |
| yapısal denetim | ihlal yok · **169** parametre · **SINANMAMIŞ 40** · duyarlılık borcu **9** · **130** modül · tekrarlı tanım **0** · ölü köken kaydı **0** · `DUYARSIZ` |Δ| **13/13** — `python kalibrasyon/mimari_denetimi.py` (23 Eylül, K-155) |
| U1 uygunluk kapısı | `python -u kalibrasyon/aodv_uygunluk.py` — dört `-yok` kolu × üç tohum, TAM pencerede; ölçüt **statik ≥ 0,90 · hareketli ≥ 0,60** (protokol/ETX kâhini oranı, K-136) · 🟢 **AODV (`AODV-e`): U1-U geçti · U1-B temiz · 2 açıklanmış düşük hücre** (bulgu) — `python -u kalibrasyon/aodv_uygunluk.py hukum` (19 Eylül, K-145) · 🟢 **AOMDV (`AOMDV-a`): U1-U geçti · U1-B temiz · 1 açıklanmış düşük hücre** (22 Eylül, K-149) · 🟢 **OLSR (`OLSR-b`): U1-U geçti · U1-B temiz · 0 açıklanmış düşük hücre** — `… aodv_uygunluk.py hukum ciktilar2/aodv_uygunluk/olsr_20260922_073356.json` (22 Eylül, K-147; §13 öncesi K-146) |
| çalışma noktası | tek karıştırıcı −15,0 dBm, ρ = 0,258 · alan 1800 m, 40 düğüm, derece 8,67 — ikisi de 15 Eylül'de BİREBİR doğrulandı (K-128) · beş tehdit ailesinin beşi de sert kısıtı geçiyor (K-127) · 🔴 **ana deney tohumlarının 15 (kol, tohum) çiftinde ağ ölçüm penceresi içinde BÖLÜNÜYOR** (`--bolunme`, K-132); satır bunu `kapsam.bolunme_payi` ile beyan ediyor |
| mobilite | çekirdek Θ = 3,25 · yüksek çalkantı Θ = 1,78 — `python -u kalibrasyon/bag_kumesi.py f g h` |
| dış çapa | Li: mekanizma doğrulandı · H1 = **0,0871** tutmadı — `python -u kalibrasyon/li_replikasyonu.py` (15 Eylül; 🔴 alet 10 Eylül'den beri çöküyordu, düzeltildi — K-129) |
| çözünürlük | 40 tohum: **kullanılacak eşik R = 0,0230** (eşleştirilmiş — birincil testin çözünürlüğü). Tek kol: `pdr_atlama` 0,0316 · `pdr_etx` 0,0244 — `python -u kalibrasyon/cozunurluk.py --tohum 40` (15 Eylül C7; eşik 16 Eylül'de düzeltildi, K-132) |
| kontrol düzlemi | uygulandı; P1–P8 **15 Eylül'de yeniden geçti** — Y3'ün beş kancasından SONRA ilk kez (1007 s) |

**Aşama 1'de tamamlananlar:** ölçüm penceresi ve evreler · çalışma noktası
(alan, yoğunluk, derinlik) · Θ kapısı ve Doppler ayrımı · karıştırıcı gücü ·
evre metrikleri ve kapıları · sonuç satırının ham ve kapsam bölümleri ·
duyarlılık denetimi · Li replikasyonu · mimari denetiminin ölçüm katmanına
genişletilmesi · üretici duman kapısı · beacon yükünün kanalda ödenmesi ·
kontrol düzlemi mekanizması.

🟢 **15 Eylül 2026: doğrulama listesi (D1) uçtan uca koşuldu** — dokuz yapı
adımından sonra ilk kez. İki ölü kapı bulundu ve düzeltildi, üç beklenen
değer Y2 öncesinden kalmış olduğu için güncellendi (`04` K-129).

🟢 **16 Eylül 2026: bağımsız denetimin bulguları işlendi** (`arsiv/DENETIM-2026-09-16.md`,
`04` K-130). Altı bulgunun beşine katılındı, biri ölçümle çürütüldü, üç yeni
bulgu eklendi. Kapanan: dört aletin verdikti **çıkış koduna bağlandı** ·
pencere ikizi **pencerede donduruldu** (kontrol yükü metriği ~%9 şişiyordu ve
şişme protokol ailesine göre farklıydı) · çift tanım silinip mimari denetimine
`D16` taraması eklendi.

🟢 **16 Eylül 2026: protokol arayüzü son hâlini aldı** (`04` K-131). Rota
bekleme tamponu (`Karar.beklet`, iki tavan, yeni düşme sebebi) ve yedi kancaya
gözlem; gözlem yüzeyi 24 → 23 alana **indi** ve `None ≠ 0` kuralının tek
istisnası kapandı. Regresyon: **141 metriğin hiçbiri değişmedi**.
🟢 **Aşama 2'nin arayüz ön koşulu KAPANDI** — AODV yazılabilir.

🟢 **16 Eylül 2026: doğrulama listesi 18/18 koşuldu** (`04` K-133) ve
duyarlılık borcu denetlendi (`04` K-132). **Aşama 1'in zemini sınandı;
sırada Aşama 2 · AODV dikey dilimi.**

🟢 **17–19 Eylül 2026: iki taban protokol.** AODV yazıldı (K-136), U1 ikiye
ayrıldı (K-137), ölçüm katmanında iki kusur düzeltildi (K-139 · K-141) ve
OLSR yazıldı (K-142). OLSR'ın ölçümüyle yan yana konunca AODV'de yarım
uygulanmış bir RFC maddesi bulundu (K-143); düzeltilmiş hâl `AODV-e`
kapanıştan geçti (K-145). OLSR §13 kararıyla kapandı (K-146 · K-147) ve
AOMDV makale + RFC 3561'le yazılıp kapandı (K-148 · K-149). 🟢 **Üç taban
protokol de kapalı; sırada Aşama 3 · özgün protokol.**

---

## 2 · Aşamalar

| aşama | içerik | takvim hedefi (tahmin) |
|---|---|---|
| **1 · Simülasyon** | §3 | 26 Eylül 2026'ya kadar |
| **2 · Protokollerin yapımı ve denenmesi** | AODV · OLSR · AOMDV; önce biri uçtan uca; U1–U4 | Eylül sonu – Ekim ortası |
| **3 · Özgün protokolün tasarımı** | öğrencinin tasarımı; gerçekleme; geliştirme tohumlarında deneme | Ekim (öğrencinin tasarım hızına bağlı) |
| **4 · Pürüz temizleme ve veri toplama** | mühür; ana deney (40 tohum); istatistik; keşifsel eksenler | Kasım başı – ortası |
| **5 · Rapor ve sunum** | yazım (~5 hafta); görselleştirme | Kasım ortası – 19 Aralık |

~~En büyük takvim riski, özgün protokol tasarımının henüz başlamamış olmasıdır.~~
🔄 23 Eylül 2026: tasarım (v0.1) hazır, gerçekleme başladı. Bugünkü en büyük
risk DESPARETE'nin **kanal yükü** — beş alanın ilanı ve boşta sondalama
birlikte ölçülmedi (K-150 §3; `04` K-152) — ve gerçeklemenin süresi (ilk iki
parçadan sonra ölçülerek bantlanacak).

---

## 3 · Aşama 1 iş listesi

**Sıra sütunu:** 1 = Aşama 2'nin ön koşulu, önce yapılır · 2 = Aşama 1'de
yapılmaya çalışılır · 3 = Aşama 4'ten önce yeter.
**Onay sütunu:** yapı = `sim2` değişikliği, önce yapı anlatılır ·
süre = 30 dk'yı aşan koşum, önce sorulur.

### A · Doğruluk ve tanımlar

| # | iş | karar / kaynak | onay | koşum (tahmin) | sıra |
|---|---|---|---|---|---|
| A1 | **Veri onayı kusurunun etkisinin ayrı ölçümü** — `kalibrasyon/onay_semantigi.py`: bugünkü onay semantiği ↔ "yalnız gönderenin kendisi çözerse", aynı tohum ve kollarda eşleştirilmiş | öğrenci: önce ölç, sonra karar · `13` R1 | süre | 🟢 **Ölçüldü (11 Eylül):** kısa pencere, 8 tohum, 128 koşu, 45 dk (`… olc kisa_2026-09-11 --tohum 5`, ardından `--tohum 8 --devam`). PDR: çözünürlük üstünde 0 · altında 5 · karar yok 3 (hareketli kollar). Sonuç ve öneri `04` K-114 §4.2; ilk tasarımın süre tahmini çökmüştü (K-114 §3). Öğrenci düzeltmeyi seçti; **düzeltme uygulandı** (Y2, K-115): düz koşu, kayıtlı `duzeltilmis` parmak izleriyle 16/16 birebir | 1 |
| A2 | **PSR'nin öğrenci tanımıyla uygulanması** (alıcı tarafında, CRC) | 🟢 tanım öğrencinin · `07` §08.2 · §18 Y1 | yapı | 🟢 **Uygulandı (11 Eylül, K-115):** ağ geneli PSR; bağ başına dağılım henüz yok | 1 |
| A3 | Kontrol istatistiklerinin sayaç kütüğüne alınması (R8) | 🟢 öğrenci onayladı · `13` §06.1 · `07` §18 Y1 | yapı | 🟢 **Uygulandı (11 Eylül, K-115)** | 2 |
| A4 | **Teslim olasılığı kâhini ve kâhin zarfı** (üst referans) — `kalibrasyon/ust_referans.py` | 🟢 öğrenci onayladı · `07` §07.2 · §18 Y9 | süre | Kapı geçti (11 Eylül). 10 tohumun bandı 59–105 dk basıldı; ölçüm başlatılmadı. Teşhis: teslim kâhini uzun yol seçiyor, PDR artıyor ama gecikme ~3 kat (`04` K-114 §4.3). **Öneri:** yeni çekirdek hücrede C7 ile birlikte koşmak; öğrenci kararı | 2 |
| A9 | **Rota bekleme tamponu** — protokol rota ararken paketi bekletebilsin (denetim B1). Bugün `Karar` iki şıklıydı ve rota yoksa paket ANINDA düşüyordu; RFC 3561 §6.3 tamponlamayı şart koşar, yani eksik yalnız REAKTİF aileyi vuruyordu | bağımsız denetim (16 Eylül) · öğrenci: ayrı bekleme tamponu | yapı | 🟢 **Uygulandı (16 Eylül, K-131):** `Karar.beklet`, düğüm başına tampon, iki tavan, yeni düşme sebebi, yedi kapı | 1 |
| A10 | **Kancalara gözlem** — gözlem TEK bir yerde (veri gönderme kararı) üretiliyordu; kontrol kancaları, `beacon_yuku` ve `beacon_alindi` hiç almıyordu (denetim B4) | bağımsız denetim (16 Eylül) · öğrenci onayladı | yapı | 🟢 **Uygulandı (16 Eylül, K-131):** yedi kanca gözlem alıyor · `bildirdigi_konum` yüzeyden çıktı (24 → 23 alan) · bilgi yokluğunda `None` | 1 |
| A5 | İki anlamlılık sabiti: tek α + tarama düzeltmesi | öğrenci: ajan ölçerek seçsin · `08` §05.3 · `07` §18 Y10 | yapı (Y10) | 🟢 **Uygulandı (14 Eylül, K-123):** tek `ALFA = 0,05`; band `z(1 − α/2)`, M4 eşiği Bonferroni. Ölçüm artık KAPI: eski kural %37–70, bugünkü %2,2–3,4 — `python -u kalibrasyon/anlamlilik_sabitleri.py` | 3 |
| A6 | Rician K kaynak doğrulaması | öğrenci · `02` §S1 | — | literatür | 2 |
| A7 | 802.11b sabitleri kaynak doğrulaması | `02` §S2 | — | literatür | 3 |
| A8 | ~~Pencere ikizinin boşalma payı~~ | Y1'de fark edildi (K-115), bağımsız denetimde B2 diye yükseltildi | yapı | 🟢 **KAPANDI (16 Eylül, K-130).** Ölçüldü: kontrol tarafı %7,6–10,7 · veri tarafı **%0,0** · `nrl_bayt_pencere` +%10,0 şişmeydi. Bir büyüklük değil **karşılaştırma geçerliliği** sorunuydu: boşalmadaki kontrol trafiği periyodiktir, yani OLSR şişer AODV şişmez. 🔒 Öğrenci kararı: ikiz **pencerede dondurulur**; tanım sonuç görülmeden yazıldı. Naif dondurmanın `algilama_duyarliligi_pencere`i öldüren tuzağı ölçülerek bulundu ve kapatıldı | 1 |

### B · Yeni yetenekler

| # | iş | karar / kaynak | onay | büyüklük | sıra |
|---|---|---|---|---|---|
| B1 | **Yere toplama deseni** — önerilen: röle İHA geçit · 1 geçit · kenarda · tüm düğümler telemetri · düşük hızlı komut akışı | öğrenci: kabul, en iyi tasarım düşünülsün · `07` §06.2 | yapı + öğrenci tasarım onayı | 🟢 **Uygulandı (11 Eylül, K-116)** — iki geçit keşifsel eksende, henüz yok | 1 |
| B2 | **Çoklu hareketli karıştırıcı** — platform × hareket × yayın düzeni; senaryo aileleri | öğrenci: çoklu, hareketli, saha davranışına paralel · `07` §05.3 · kaynaklar `02` §S3 | yapı + öğrenci tasarım onayı | büyük — 🟡 **Y5a mekanizması uygulandı (11 Eylül, K-117)**, regresyon 37/37 birebir; 🟢 Y5b kararları verildi (11 Eylül, K-119): beş aile ve K değerleri önerildiği gibi · çekirdek süreler 15 s açık / 15 s sessiz / %50 görev çevrimi 30 s, keşifsel noktalar önerildiği gibi · uzun koşu şimdilik yok. 🟢 **Uygulandı (14 Eylül, K-120):** beş aile, güç payı 1/(K × açık oranı), yalnız susarken taşınan araç, beş regresyon vakası (`07` §05.3.1) | 1 |
| B3 | **Mobilite: istasyon tutma** — formasyon kolu | öğrenci: öneri onaylandı (10–11 Eylül) · `07` §03.4 · §18 Y6 | yapı | orta — 🟢 **Uygulandı (11 Eylül, K-118):** 531 test; regresyon 37/37 birebir (ilan edilmiş dört alan dışında) + 2 yeni vaka. Duvar teması nadir, sayılır ve beyan edilir (öğrenci kararı, K-119) | 2 |
| B4 | Kontrol düzlemi eksikleri: beacon'ın protokol başına kapatılması (R2) · iletim sonucu kancası (R3) · protokol rastgelelik alt akışı (R4) | `13` §06.1 | yapı | orta — 🟢 **Uygulandı (14 Eylül, K-121):** beş kanca, üç yeni defter sayacı, `protokol_kesif` akışı açıldı | 1 |
| B5 | Θ'nın protokol başına raporlanması; yüksek çalkantı kolunun etiketi | öğrenci: kol saklanmaz · `07` §03.3 | yapı | küçük — 🟢 **Uygulandı (14 Eylül, K-122):** dört kolda ölçüldü, her satır iki Θ ve temsil oranını taşıyor. 🔴 Formasyonun Θ'sı aşağı yanlı (çiftlerin %92'si hiç kopmuyor) | 2 |
| B6 | İz kanalı (gösterim için; ölçüme dokunmaz, kapısı "birebir aynı satır") | öğrenci: sunumda görselleştirme · `07` §13 | yapı | orta | 3 |

### C · Yeniden kalibrasyon — B'den sonra

| # | iş | bağımlılık | koşum (tahmin) | sıra |
|---|---|---|---|---|
| C1 | **Düğüm sayısı 30–50** — ölçüt: bağlantılılık · geçide derinlik ve alternatif yol · çözünürlük başına maliyet (`07` §09.4) | B1 | 🟢 **Koştu (15 Eylül, K-125):** adaylar ayrılamadı; öğrenci N = 40'ta kaldı. Ölçüm N'i seçmedi, doğruladı | 1 |
| C2 | Çalışma noktası: alan ve karıştırıcı gücü, yeni karıştırıcı kümesiyle. 🔴 *"yeni trafikle"* ifadesi KALDIRILDI — iki ölçüt de trafiksiz kanal grafiğinde tanımlı (K-127 EK) | B1, B2, C1 | 🟡 **Aile kapısı koştu (15 Eylül, K-127):** `hedef_koruma` sert kısıtı çiğnedi, görev çevrimi kaldırıldı; öteki dört aile geçti. 🟢 **Çapalar da doğrulandı (15 Eylül, K-128):** alan 1800 m ve güç −15,0 dBm (ρ 0,258) bugünkü kodla BİREBİR yeniden çıktı; Y1–Y10 ve tehdit kümesi onları oynatmadı. 🔒 Alete bölüm seçimi eklendi — dosya dört bölümü birlikte koşturuyor ve C2'yi C5'in faturasıyla ödetiyordu | 1 |
| C3 | Yere toplama yük kalibrasyonu | B1, C1 | 🟢 **Koştu (15 Eylül, K-126):** ölçüt harfiyen 2,0 seçiyordu ama eksen dengesini (40 = 40 pkt/s) bozuyordu; öğrenci 1,0'da kaldı. Ölçüm hızı seçmedi, doğruladı; uçurum 2,5–3,0'da ölçüldü. `esler_arasi` de ilk kez sınandı ve geçti | 1 |
| C4 | Θ yeniden (seçilen mobilite modeliyle) — 🟡 dört kolda ölçüldü (14 Eylül, K-122). **Kalan:** formasyon kolunda kopmayan çift oranı %92 olduğu için kestirici az örnekle çalışıyor; daha çok tohumla yeniden ölçülmeli | B3 | 10–30 dk | 2 |
| C5 | **Görev kolu yarıçapı, büyük örneklemle** (~140 tohum gerektiği hesaplanmıştı, K-111 EK-1) — artık ayrı koşulabilir: `calisma_noktasi.py --bolum gorev_kolu` | öğrenci kararı; B3 kararına bağlı | 1–3 saat | 2 |
| C6 | Isınma × ölçüm penceresi birleşik taraması; açılma anı parametre | öğrenci kararı; B1, B2 | 1–3 saat | 3 |
| C7 | Çözünürlüğün yeni çekirdek hücrede ölçülmesi | C2, C3 | 🟢 **Koştu (15 Eylül, K-128):** R = 0,0316 (40 tohum). 🔴 Ölçüm bir kusur buldu: köken defterindeki aklamalar 30 tohumluk R = 0,036'ya karşı yazılmıştı, yani deneyin gerçekte görebileceğinden %14 gevşek. Sınıflandırma değişmedi (en büyük |Δ| = 0,027) ama eşik alıntıları düzeltildi. ✅ **16 Eylül: "8 kayıtta |Δ| yok" borcu ölçüldü ve zaten kapalıydı** — 15 kaydın 15'i de sayı taşıyor (`python kalibrasyon/mimari_denetimi.py`, D12; sayı artık her koşumda sayılıyor, düzyazıda değil). 🔴 **Yerine gerçek borç:** aklamalar **tek kol** çözünürlüğüne (R = 0,0316) karşı yazılı. Oysa duyarlılık aleti tohum başına FARK ölçüyor (eşleştirilmiş) ve ön-kayıttaki birincil test de eşleştirilmiş (Wilcoxon, `06` §7); doğru eşik **0,0230**. Çözünürlük aleti bunu kendi çıktısında söylüyor ama sonra en gevşek çıktıyı seçiyor. O eşikte üç kayıt aklanamıyor: `gm_pitch_sigma_rad` 0,030 · `golgeleme_hucre_m` 0,027 · `onay_bayt` 0,025 → daha çok tohumla yeniden ölçülecek | 2 |

### D · Kapanış

| # | iş | koşum (tahmin) | sıra |
|---|---|---|---|
| D1 | Doğrulama listesinin tamamı yeni kodla (`DEVIR.md` §2) | 🟢 **YENİDEN KOŞTU (16 Eylül, K-133): 18/18**, Adım 0–3'ün hepsinden sonra. İki şey yakalandı: duman kapısı K-130'da değiştirilip koşulmamış bir aletin çöktüğünü buldu; üst referansın beklenen değerleri DÖRDÜNCÜ bayat değer olarak çıktı (bugünden gelmediği ölçüldü — kâhin PDR'si 15 Eylül'le 10/10 birebir). Önceki koşum: 🟢 **KOŞTU (15 Eylül, K-129):** 18 maddenin hepsi, dokuz yapı adımından sonra ilk kez. İki ÖLÜ KAPI bulundu ve düzeltildi (Li replikasyonu çöküyordu; duman kapsam kapısı sessizdi), üç beklenen değer Y2 öncesinden kalmış olduğu için tazelendi. Ölçülen toplam ~3,5 saat (yüklü makine) | 1 |
| D2 | SINANMAMIŞ ve duyarlılık borcu: kaynakla, ölçümle ya da eksen ilanıyla. Protokolsüz kapanmayan dört parametre Aşama 2'ye | — | 3 |

**26 Eylül'e sığar mı?** Dürüst tahmin: sıra-1 işler (A1, A2, B1, B2, B4, C1–C3,
D1) sığabilir, ama B2'nin tasarımı ve kalibrasyon koşumları uzun. Sığmazsa
önce sıra-1 işler biter; sıra-2 ve sıra-3 işler Aşama 2 ile paralel yürür
(ölçüm betikleri ve literatür soruları protokol yazımını beklemez).

---

## 4 · Öğrenci kararları ve bekleyen onaylar

**Onaylandı (10 Eylül 2026, ikinci tur):**

- mobilite önerisi (formasyon + istasyon tutma)
- çoklu hareketli karıştırıcı; saha davranışı sentezi öğrenciden geldi (`02` §S3)
- üst referans (teslim olasılığı kâhini)
- kontrol istatistikleri
- mühür sırasının gevşetilmesi
- yere toplama önerileri — dürüstlük ve gerçekçilik şartıyla; değerlendirme
  `07` §18 Y4

**Onaylandı (11 Eylül 2026, üçüncü tur):**

- yapı: `07` §18 Y1, Y3, Y4, Y5, Y6, Y7, Y10 (`sim2` değişiklikleri)
- veri onayı düzeltmesi: `07` §18 Y2 (`04` K-114 §4.2)
- üst referansın tohumlu ölçümü yeni çekirdek hücrede, C7 ile birlikte
  (`04` K-114 §4.3)

**Bekleyenler:**

1. **Uzun koşumlar** — C grubu; yeni yetenekler yazıldıktan sonra. 30 dk'yı
   aşanlar önce sorulur.
2. **İz kanalı (Y8)** — yapısı Aşama 1 sonunda ayrıca anlatılır.
3. ✅ **KARAR VERİLDİ: A** (17 Eylül, K-137) — aşağıdaki metin o günün
   hâlidir ve tarihsel olarak duruyor. 🔴 **19 Eylül düzeltmesi (K-145):**
   RFC §6.11 düzeltmesinden sonra `statik-yok/1002` **0,932** ile eşiği
   geçiyor. Aşağıdaki *"yazılım kusuru değil"* hükmü yarı yarıya yanlıştı:
   hücrenin statik kolun en düşüğü olması yapıdan geliyor ve hâlâ öyle,
   ama eşiğin altında kalmasının bir kısmı kusurdu.

   🔴 **U1 statik kolda `statik-yok/1002`de KALIYOR** (17 Eylül, K-136) ve
   sebebi ölçüldü: **yazılım kusuru değil.** AODV'nin bağ kalitesi kabul
   eşiği yoktur (RFC 3561 atlama sayısıyla yönlendirir) ve 1002, deponun
   zaten bildiği en zayıf bağlı tohum — o dünyada akışların **7/10**'unun
   en kısa yolu 0,90'ın altında teslim veriyor (1000'de 3/10).
   ⚠️ Ajan eşiği DEĞİŞTİRMEDİ ve kapının biçimini (çift-başına sınama)
   DEĞİŞTİRMEDİ. Karar öğrenciye ait; dört seçenek ve bedelleri:

   | # | seçenek | bedeli |
   |---|---|---|
   | A | **Eşik yerinde kalsın, AODV bu tohumda kapıyı geçmedi diye raporlansın** | En dürüst seçenek ve `06` §5.1 H1.1'in ölçmek istediği bulguyu doğrudan besler. Bedeli: `06` §4.4 madde 3 *"geçilmeden protokol kabul edilmez"* diyor — o cümlenin **U1 için** yeniden yazılması gerekir, yoksa AODV'yi taban protokol olarak kullanamayız |
   | B | **Kapı kol ORTALAMASINA bakar** | Dört kolun dördü de geçer (0,944 · 0,666 · 0,615 · 0,758). Bedeli: sonucu gördükten sonra biçim değiştirmek, eşiği gevşetmenin kılık değiştirmiş hâli; ayrıca bir tohumun çökmesini (0,32) iki iyi tohum örter ve kapı körleşir. 🔴 Ajanın önerisi DEĞİL |
   | C | **Eşik düşürülsün** | Aynı itiraz (A'nın dürüstlüğünü kaybeder) ve ek bir zarar: eşik üç taban protokolü birden bağlıyor, AODV'ye göre indirilmiş bir eşik OLSR ve AOMDV için de gevşer |
   | D | **U1 "bağlı ağ" ön koşulunu bağ KALİTESİNE de genişletsin** | `06` §4.3 zaten *"bağlı ağ"* diyor; 1002'nin bağlarının yarıya yakını 0,90'ın altında, yani o dünya "bağlı" sayılabilir ama "sağlam" değil. Bedeli: yeni bir kapsam ölçütü demek ve **taramadan önce ilan edilmesi** gerekir; ayrıca ana deney tohumlarının ne kadarını eleyeceği ÖLÇÜLMEDEN seçilemez |

   🔒 Ajanın görüşü: **A**. Sebebi, D'nin gizli bedeli — zayıf bağlı
   topolojileri kapsam dışı bırakmak, karıştırma altındaki bir tatbikat
   ağında tam da ölçülmek istenen zorluğu deneyden çıkarmak olur.

---

## 5 · Tam yol haritası — 23 Eylül 2026

> 🟢 bitti · 🟡 sürüyor · ⏳ sırada · ⚪ açık, zamanı gelince. Her adım bir
> kapıyla kapanır; kapının adı ve kararın kaydı yanında. Süreler tahmindir.

**📍 ŞU AN BURADAYIZ: Aşama 3, adım 3.8** — kabul kapısı. Tam ölçekte
(N = 40) A seçeneğiyle DESPARETE çöküyordu (PDR 0,08–0,09; sebep ölçüldü:
komut hedeflerinin alanları). 🟢 **Öğrenci C'yi seçti** (24 Eylül, K-160
§12): v0.1 yalnız geçit alanıyla, komutlar düşer. C ile statik oran ~0,82
(eşik 0,90), 🔴 hareketli oranlar 0,12–0,34 (eşik 0,60) — sebep kontrol
yükü ve bağ çalkantısı, tek mekanizmaya bağlı değil (K-160 §13).
🟢 **Öğrenci: v0.2'ye geç** (K-160 §14) → **yalın profil** (K-161 §4):
boşta sondalama · onarım edinimi · ilan koruması kapalı; DESPARETE'nin
varsayılanı. Tam ölçek doğrulaması (40 s, U1'in tohumları): hareketli 9/9
hücre oran ≥ 0,60 (0,72–0,92), statik 3/3 hücre 0,87–0,89 (eşik 0,90).
🔄 **Öğrenci: test öncesi protokolü iyileştir** (K-162) — resmi U1 bekler.
Analiz: kontrol yükünün %76–86'sı komşu çalkantısının PROBE'ları; ACTIVE
komşu bilgisi bayat (kapsam ~0,62); ardıl kopunca yedek ACTIVE değil →
sık kısa onarım, gecikme p95 1–4 s. Adaylar V5 · V1 · V2+ · V6 (K-162 §5).
K-163: V1 + V5 + V7 tam ölçekte kontrol yükünü ~yarıya, hareketli gecikme
p95'i 2,5–4 s'den 0,1–0,8 s'ye indirdi → 🟢 **v0.3 = v0.2 + V1 + V5 + V7**,
DESPARETE'nin varsayılanı (K-164). V5a (ilanı sakla) ve V2+ (hedefli
canlılık) denendi, **benimsenmedi** (kararlı durumda zararlı; K-164 · K-165).
Yöntem dersi: 3 tohumluk 40 s hücrelerinde ±0,03'lük PDR farkı gürültü
düzeyinde (K-165 §4). Önceki: ablasyon bayrakları (K-159).

### Aşama 1 · Simülasyon — 🟢 BİTTİ (10–16 Eylül)

- 🟢 Ölçüm ortamı: dünya, kanal, MAC, beş karıştırıcı sınıfı ve beş tehdit
  ailesi, yere toplama, dört mobilite kolu, kontrol düzlemi, rota bekleme
  tamponu, evre metrikleri (§3; K-112…K-135).
- 🟢 Kalibrasyonlar C1–C3, C7 · doğrulama listesi 18/18 (K-133).
- ⚪ Kalan küçük işler (Aşama 4'ten önce yeter): C4 formasyonda Θ daha çok
  tohumla · C5 görev kolu yarıçapı · C6 ısınma × ölçüm penceresi taraması ·
  A6–A7 kaynak doğrulamaları · B6 iz kanalı (görselleştirme — Aşama 5 onu
  ister).

### Aşama 2 · Taban protokoller — 🟢 BİTTİ (17–22 Eylül)

- 🟢 AODV (`AODV-e`, K-145) · OLSR (`OLSR-b`, §13 ile, K-147) · AOMDV
  (`AOMDV-a`, K-149) — üçü de aynı 12 hücrede U1'den geçti.
- ⚪ Açık kalanlar: M4'ün boş kol kapısı · AOMDV'nin U2/U4 karşılıklarının
  adıyla eşlenmesi (`06` §9) · OLSR §13'ün hareketli kolda mekanizması
  (hipotez, K-147) · AOMDV'nin bayat yedek yolu (S2) · rota tamponunun iki
  parametresi (64 paket · 30 s — ölçülmedi).

### Aşama 3 · Özgün protokol DESPARETE — 🟡 SÜRÜYOR (23 Eylül →)

- 🟢 **3.0 · Hazırlık** — tasarım paketi okundu, kararlar (K-150) ·
  simülatöre iki eklenti: her unicast sonucunun bildirimi ve veri başlığı
  (K-151, 23 Eylül'de kapandı) · öğrencinin 23 Eylül yanıtları (K-152).
- 🟢 **3.1 · Mesaj biçimleri** — yedi biçim, boyutlar alanlardan; belgenin
  DFSN_REQUEST boyu hatası bulundu (K-152 §6).
- 🟢 **3.2 · M0.1 metrik profili** — bağ kalitesi, risk, maliyet; belgenin
  TV-02 hatası ölçüldü (K-152 §4). Ara toplam: `717 passed`.
- 🟢 **3.2b · Ön-kaydın adım 3'ü** — eşik formülü, güç yöntemi, aday
  birincil hücre `formasyon · yere_toplama · hava_eslik · sürekli · PDR`,
  `Δ_hedef = 0,05` (`06` §0.4, K-153).
- 🟢 **3.3 · Komşu yaşamı** (K-154) — UNQUALIFIED → ACTIVE → STALE /
  SUSPECT → EXPIRED; PROBE / PROBE_REPLY; boşta sondalama; M0.1 simülatörün
  sonuç bildirimine bağlı; protokol iskeleti. DESPARETE simülatörde ilk kez
  koştu. İlk ölçüm: yalnız boşta sondalanan bağlarda belirsizlik U = 128
  (K-150'nin tahmini tuttu). Ara toplam: `test_desparete.py` 89 passed.
- 🟢 **3.4 · Alan, uygulanabilirlik ve sıra numarası** (K-155) — veri ilk
  kez DESPARETE'yle taşındı; her kancadan sonra döngü denetimi, ihlal 0.
  Küçük dünyada teslim taban protokollerle aynı mertebede, **ek yük 4–9
  kat** (3.9'un ölçeceği ilk soru). Ara toplam: `test_desparete.py` 107.
  Tasarımın dökümü: FIELD_UPDATE (yayın),
  ardıl seçimi, uygulanabilirlik mesafesi; veri ilk kez DESPARETE'yle
  taşınır. 🔒 Döngüsüzlük değişmezleri her olaydan sonra denetlenir.
- 🟢 **3.5 · Edinim ve onarım** (K-156) — solicit ve iki dalgalı istek
  oturumu, hedefin dar tur yetkisi, isteğe bağlı hedef alanları, onarım
  tamponu, yeniden edinim. Alan başına tampon kotası paket kimliği
  olmadan uygulanamıyordu (K-156 §3) → 🟢 öğrenci A'yı seçti: kimlik
  `(kaynak, kaynak_sira)` gözlem yüzeyinde, kota 6 yazıldı, `k151 ↔ k157`
  birebir (K-157). Ara toplam: `test_desparete.py` 122. Tasarımın dökümü: FIELD_SOLICIT, DFSN_REQUEST (tek yayın),
  REPAIRING / UNREACHABLE, 6 s'lik onarım tamponu ve alan başına kota,
  yeniden edinim kuralı (K-152 §2), komut trafiği için hedef alanları
  (K-150).
- 🟢 **3.6 · Postürler** (K-158) — alan başına STEADY / CAUTION / PROTECT;
  CAUTION'a girişte bir doğrulama oturumu (K-150). Yedeklilik yok → koruma
  izni yok → PROTECT'e girilmez (koşulların izinsiz sağlandığı anlar
  sayılıyor: küçük dünyada 0). CAUTION'ın %100'ü belirsizlikten; A/B, 5
  tohum: statikte etki yok, karıştırıcılıda ek yük +%4,4 (5/5), PDR −0,021
  (4/5, anlamlı değil). Ara toplam: `test_desparete.py` 133.
- 🟢 **3.7 · Ablasyon bayrakları** (K-159) — sekiz mekanizma (risk ve
  kalite terimi · postür · boşta sondalama · onarım tamponu · onarım
  edinimi · ilan koruması · yeniden edinim); güvenlik değişmezleri bayrakla
  kapanmaz. Kullanılan bayraklar her düğümün teşhisinde, satırda. ⚠️ Koşu
  kimliği protokol parametresi içermez: her kol kendi `kol` etiketini
  taşımalı (Aşama 4'ün koşum aletine). Hangi bayrak KOL olur → mühürde
  (öğrenci). Ara toplam: `test_desparete.py` 144.
- 🔴 **3.8 · Kabul kapısı** ← BURADAYIZ (K-160) — U1 yapı · U2 · U4 testleri
  yazıldı (U2 bir kopma beyanı kusuru yakaladı, düzeltildi; ölçülen etkisi
  0). Tam ölçekte çöküş ölçüldü, sebebi komut alanları → **öğrenci kararı
  C** (K-160 §12: yalnız geçit alanı, komutlar düşer). U1'in sayısal
  koşumu ve U3 sırada. Ara toplam: `test_desparete.py` 152. Asıl plan: DESPARETE'nin U1'i yere toplama deseninde
  (K-150); U2–U4 karşılıkları. Tam kapanış paketi: test takımı + U1 (bant
  2,5–4,5 sa) + regresyon.
- ⏳ **3.9 · İlk ölçümler (geliştirme tohumları)** — boşta sondalama yükü ·
  belirsizlik eşiği ↔ sondalama hızı (küçük dünyada CAUTION'ın %100'ü
  belirsizlikten, K-158 §6) · beş alanın ilan yükü (K-150 §3) ·
  tampon kotası 6 ↔ 32 (K-152 §3; küçük dünyada alan başına tepe 1 —
  ancak daha yoğun trafikte bir şey gösterebilir, K-157 §6) · yeniden
  edinim sayısı (K-152 §2).
- ⏳ **3.10 · v0.2 kararları** (öğrenci) — ölçümlerin gösterdiği tasarım
  değişiklikleri, kanıtla; parametreler sabitlenir. Tasarım paketinin asıl
  kaynağına düzeltmelerin işlenmesi (TV-02 · durum makinesindeki eksik satır
  · DFSN_REQUEST boyu — öğrenci).
- ⚪ Kapsam kararı bekleyenler: güvenlik kolunun bayt bedeli (ayrı
  duyarlılık kolu, K-150) · yedekli gönderim (simülatör yapısı ister —
  gelecek çalışma olabilir).

### Aşama 4 · Pürüz temizleme ve veri — ⏳ (tahmin: Kasım başı–ortası)

- ⏳ **4.1 · Gürültü ölçümü** — üç taban protokol × 20 geliştirme tohumu
  (1100–1119), birincil hücrede, tam pencere → δ ve güç → tohum sayısı
  (40 yeterli mi) (`06` §0.4). Koşum bandı hücre sabitlenince ölçülür.
- ⏳ **4.2 · Ön-kaydın tamamlanması** — Aile 1'in hipotez ve hücreleri ·
  Aile 3'ün mekanizma kapısı ve ablasyon kolları · AOMDV öngörüsünün yeni
  tehdit modeline göre yazılması · çekirdek matris (karıştırma koşulları
  listesi) · koşu uzunluğu ölçütünün k değeri · durdurma kuralı (`06` §9).
- ⏳ **4.3 · Borçlar** — 40 `SINANMAMIŞ` parametre ve 9 duyarlılık borcu:
  kaynakla, ölçümle ya da eksen ilanıyla sıfırlanır · `algilama_duyarliligi`
  ikiye bölünür · doğrulama listesinin tamamı yeni kodla bir kez (~3,5+ sa).
- ⏳ **4.4 · İstatistik katmanı** (`analiz/` — henüz yazılmadı): eşleştirilmiş
  Wilcoxon, Holm, güven aralıkları, NaN tuzağının kapısı; satırdaki
  yüzdeliklerin ham listeden yeniden üretilmesi.
- ⏳ **4.5 · 🔒 MÜHÜR** (öğrenci onayı) — hipotezler, eşik değerleri,
  parametreler, tohum sayısı, birincil hücre.
- ⏳ **4.6 · Ana deney** — 4 protokol × çekirdek hücreler × 40 tohum
  (2000–2039, mühürden önce hiç koşulmaz). Parça parça koşup birleştirmek
  mümkün: her satır kendi konfigürasyonunu taşır. Koşum bütçesi mühürde.
- ⏳ **4.7 · Keşifsel eksenler** — yüksek çalkantı · görev kolu · eşler
  arası trafik · kalan aileler ve sınıflar · ρ taraması · derinlik · 2 geçit ·
  güvenlik kolu. Takvim sıkışırsa ilk düşenler bunlar (§7).

### Aşama 5 · Rapor ve sunum — ⏳ (tahmin: ~15 Kasım – 19 Aralık)

- ⏳ Rapor yazımı (~5 hafta; kısaltılmaz — §6) · sonuç tabloları ve güven
  aralıkları · negatif sonuçlar dürüstçe.
- ⏳ Görselleştirme: iz kanalı (B6) ve simülasyonun işleyişinin gösterimi
  (`07` §13).
- ⏳ Simülasyon–gerçeklik beyanı (`01` §8) · fikir sahipliği: karar defteri
  ve ablasyonla ölçülmüş katkı payı (`01` §4).
- ⏳ Poster, sunum, jüri savunması hazırlığı.

---

## 6 · Takvim — kaba

| dönem | hedef |
|---|---|
| 10–26 Eylül | Aşama 1 |
| 27 Eylül – ~15 Ekim | Aşama 2 |
| Ekim | Aşama 3 |
| Kasım başı – ortası | Aşama 4 |
| ~15 Kasım – 19 Aralık | Aşama 5 |

Hepsi tahmindir. Bir aşama kayarsa sonraki aşamanın başlangıcı kayar;
yazım süresi (Aşama 5) kısaltılmaz.

🔄 **Gerçekleşen (23 Eylül 2026):** Aşama 1 ve 2 22 Eylül'de bitti (Aşama 2'nin
hedef bitişi ~15 Ekim'di); Aşama 3 23 Eylül'de başladı. Aşama 4 ve 5'in
tarihleri değişmedi; kazanılan süre Aşama 3'ün ölçümlerine (kanal yükü,
geliştirme tohumları) ayrılıyor.

---

## 7 · Kayma planı — öneri

Kapsam kararı öğrencinindir. Takvim sıkışırsa önerilen düşme sırası:

1. Keşifsel eksenlerin bir kısmı (görev kolu, derinlik, 2 geçit, bazı
   karıştırıcı senaryoları).
2. İz kanalının zengin gösterimi (temel gösterim kalır).
3. Çekirdek hücre sayısının azaltılması.

Çekirdek deney, üç taban protokol ve özgün protokol korunur.
