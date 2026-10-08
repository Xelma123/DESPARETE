# 14 · REFERANS GERÇEK DÜNYA — simülatörün 1:1 karşılığı

> **Durum: 🟢 onaylandı** (öğrenci, 25 Eylül 2026; K-169) ve uygulandı (Faz 1–3, `sim2/kanal/dunya.py::referans_2026`). Alan sonradan 33 km (K-188), karıştırıcı referans tabanı 10 W ve birincil hücre `derin_sizma` (K-186).
> **İlke (öğrenci):** simülatör ve gözlem sözleşmesi gerçek bir İHA sürüsünde ne oluyorsa o. Her sayı ya **kaynaklı** (`02` G1–G9, R1–R4), ya **betikle hesaplanmış**, ya da **öneri (ajan, onaylı)**.
> **Üretici:** `python arsiv/teshis/referans_dunya_2026-09-25/bag_butcesi.py` (çıktı yanında) — yalnız aritmetik, simülasyon yok.

---

## 0 · Eski dünyadan ne değişiyor

| | eski (1:50 ölçek, K-101/K-102) | yeni (1:1) |
|---|---|---|
| birimler | simülatör metresi = 50 m | gerçek metre, gerçek dBm |
| verici gücü | menzilden türetiliyordu (0,03 dBm ≡ 2,5 W) | kaynaktan (§1); menzil sonuç |
| alım eşiği | SINR 16 dB, işlem kazancı yok | 2 Mb/s'te SNR +1,2 dB (22 MHz), işlem kazancı dâhil |
| girişim | karıştırıcı ve öteki çerçeveler ~10,4 dB fazla zararlı | gürültü gibi, işlem kazancıyla (G1, G2) |
| taşıyıcı dinleme | geometrik (1767 m = bütün alan) | güce dayalı önbelge sezme + enerji sezme (ED) |
| 802.11 zamanlaması | yayılım gecikmesi ihmal (gerçekte slottan uzundu) | modellenir; 33 km'lik alanda tipik bağ ~9 km → ~30 µs, slottan (20 µs) UZUN: ACK zaman aşımı en büyük gecikmeyle genişletildi, slot ve kapsama sınıfı standart kaldı (beyan; duyarlılığı Faz 6, denetim D-11) |

## 1 · Telsiz — 802.11b DSSS

| büyüklük | değer | köken |
|---|---|---|
| bant · kanal | 2,4 GHz ISM · kanal 6 (2 437 MHz) · 22 MHz | G2 |
| hızlar | 1 (DBPSK) · 2 (DQPSK) · 5,5 · 11 Mb/s (CCK); önbelge + başlık 192 bit, hep 1 Mb/s | G1, G2 |
| hata modeli | Eb/N0 = SNR·22 (1 Mb/s) · SNR·11 (2 Mb/s) · CCK Pursley–Royster; gürültü 22 MHz'de | G1 (CMU ölçümüyle karşılaştırılmış) |
| gürültü | NF 7 dB → **−93,6 dBm** | G1 · betik |
| duyarlılık (PER ≤ %10, 576 B) | **1 Mb/s −97,0 · 2 Mb/s −92,4 dBm** | betik · standardın alt sınırı −80 dBm (G2) · CMU Prism 2.5 ≈ −94…−100 (G1) |
| **verici** | **EIRP 20 dBm (100 mW)** — AB/Türkiye 2,4 GHz sınırı EIRP'dir (anten dâhil); dipolle iletilen ≈ 17,9 dBm (61 mW) | G2 · G7 (*"In Europe, the max EIRP is 100mW"*) · onaylı |
| keşifsel verici | taktik mesh telsizi: 27 dBm (Doodle Labs Pro) · 33 dBm (Xtreme), MCS 0 | G7 |
| anten | yarım dalga dipol, 2,15 dBi, dikey (bugünkü desen modeli) | bugünkü model |
| ED eşiği | iletilen >100 mW → −80 · >50 mW → −76 · ≤50 mW → −70 dBm → 61 mW'ta **−76 dBm**; ED süresi 15 µs | G2 |
| hız uyarlaması | basit kaynaklı kural (ARF benzeri), bütün protokollerde aynı MAC | onaylı öneri · düşük güçlü girişimde etkili, güçlü karıştırmada etkisiz (G5) |

**Menzil (serbest uzay, 2 Mb/s, betik):** EIRP 20 dBm'de sönümsüz 5,2 km · 10 dB payla **1,65 km** · 20 dB payla 0,52 km. Doodle Labs Pro'da (27 dBm + dipol) 14,9 · 4,7 · 1,5 km; Xtreme'de 29,8 · 9,4 · 3,0 km.

## 2 · Kanal

| | değer | köken |
|---|---|---|
| hava–hava yol kaybı | serbest uzay, α = 2 (iki-ışın kırılma mesafesi 100 m irtifada ~325 km) | fizik · **ölçümler 1,92–2,6, 802.11a'da 2,03** (G10) · G8 aynı varsayım |
| gölgeleme | log-normal, σ 3 dB, korelasyonlu | bugünkü (ÖLÇÜLMÜŞ) |
| hızlı sönümleme | Rician, **K referans 10 dB, aralık 6–15 dB** — Faz 4.4'te DUYARLI ölçüldü → **EKSEN** (K-215: birincil test 10 dB, 6 ve 15 dB keşifsel) · Doppler gerçek hızdan. Hava–hava için doğrudan ölçüm erişilemedi; dolaylı kanıt: alçak irtifa yer–hava 2–10 dB, güçlü görüş hattı ~12 dB (L bandı) – ~30 dB (C bandı). Hava–hava bağında yer saçılması daha az → alçak irtifa yer–hava değerlerinin altında olmamalı. **Faz 4'te 6 · 10 · 15 dB duyarlılığı ölçülür:** sonuca etkisi çözünürlüğün altındaysa DUYARSIZ, değilse eksen | G11 (dolaylı) · öneri (ajan) · S1 |
| **yer–hava** (yerdeki karıştırıcı → İHA) | Al-Hourani: PL = FSPL + η; P(LoS, θ) = 1/(1 + a·exp(−b[θ − a])); **banliyö** parametreleri (η_LoS 0,1 · η_NLoS 21 dB) — makalede açık kırsal yok, en yakını banliyö (beyan) | G6 |
| yayılım gecikmesi | d / c | fizik |

## 3 · Sürü

| | değer | köken |
|---|---|---|
| sınıf | NATO Sınıf I küçük: ≤ 5 000 ft AGL (~1 520 m), görev yarıçapı ≤ 50 km (LOS) | G9 |
| düğüm sayısı | **40**; Faz 4'te C1 ölçütleriyle yeniden doğrulanır | onaylı |
| alan | **33 km kare** (K-185 → K-188: gölgeleme birimi düzeltilince 35 km kopuyordu; altındaki her alanın geçtiği en büyük 33 km, derece 9,67, derin çift %26,9) — ilk öneri ~6–8 km'ydi ve 10 dB paylı nominal bağa (1,65 km) dayanıyordu; simülatörün kanalında bağ 1 Mb/s'te ~9–10 km, 7 km'lik sürü tam örgü (derece 37,4). 35 km ağın hiç kopmadığı en büyük alan (derece 8,82, derin çift %31,9). Öğrenci: gerçekçilik önce → ajan kararı | ölçüldü · G9 zarfı (≤ 50 km) |
| irtifa | **50–300 m AGL** | onaylı (G9 zarfı içinde) |
| hız | **40–120 km/h** — dört kol (statik, bağımsız, görev, formasyon) gerçek hızlarla | onaylı |
| konum bilgisi | kendi konum ve hızı GPS/INS ile; yatay hata **1,5 m CEP** (σ ≈ 1,3 m/eksen); dikey σ 2 m (öneri) · GPS karıştırması kapsam dışı | G7 · öğrenci kararı |

## 4 · Tehdit — karıştırıcılar

**Bağ bütçesi** (betik; 2 Mb/s, işlem kazancı dâhil, düğüm EIRP 20 dBm): 1 km'lik bir bağı 1 W'lık karıştırıcı **3,7 km**'den, 10 W'lık **11,7 km**'den, 50 W'lık **26,1 km**'den keser.

🔒 **Raporun temel sınır cümlesi:** onlarca watt'lık bir karıştırıcı birkaç kilometrelik sürünün tamamını karartır. Orada hiçbir yönlendirme protokolü teslimi kurtaramaz; kurtaran şey frekans çevikliği ya da hareket olur (ikisi kapsam dışı). **Yönlendirmenin fark yaratabileceği rejim, etki alanı sürüden küçük karıştırıcılardır:** düşük güçlü, İHA taşıyıcılı (hava eşlik), uzaktaki ya da yer–hava kaybıyla zayıflayan. Birincil hücre bu rejimde kurulur ("kısmi karıştırma", ρ ölçütü, Faz 4.1). Güçlü uç, güç taramasıyla rejimin sınırını gösteren keşifsel eksen olur (H1.2 dirseği).

| | değer | köken |
|---|---|---|
| sınıflar | sürekli · darbeli · reaktif (< 4 µs tepki, duyma menzilli) · aldatıcı (sahte çerçeve alıcıyı kilitler) · taramalı | G5 |
| güç | İHA taşıyıcılı 1–5 W · taşınabilir 10 W · araç 50 W. **Referans taban 10 W toplam ortalama, her ailede eşit; birincil hücre `derin_sizma` (hareketli araç) — öğrenci kararı K-186.** Ölçüldü (35 km): 1–5 W'lık hava karıştırıcısı sürüyü her geometride böler (en büyük parça %5–20); yer/araç karıştırıcıları 10 W'ta kısmi (ρ 0,16–0,29) | onaylı · üretici sayfaları 10–200 W (kanıt gücü düşük, S3) · `arsiv/teshis/faz4_2026-09-26/b_aile_guc.txt` |
| platformlar | yer (1,5–5 m, yer–hava kanalıyla) · araç · hava; beş tehdit ailesi korunur | onaylı |
| etki | alıcıda SINR (işlem kazancıyla) **ve** vericide ED-CCA: yakınındaki düğüm kanalı meşgul görür, gönderemez | G2 |

## 5 · Trafik

Yere toplama (birincil): her düğümden geçide telemetri **1 pkt/s × 512 B ≈ 4,1 kb/s** (MAVLink ölçeğinde: mesaj 8–263 B, yaşam sinyali ~1 Hz — G4; akış hızı S4) + geçitten 4 düğüme komut 0,25 pkt/s. Eşler arası keşifsel. **Yeni eksen:** trafik yoğunluğu (tıkanıklık, karıştırmadan ayrı).

## 6 · MAC zamanlaması

- **Standarttan ya da iki bağımsız uygulamadan (G12 ns-3, G13 Linux):** slot 20 µs · SIFS 10 µs · CWmin 31, CWmax 1023 · uzun önbelge 144 + 48 µs = 192 µs · **kısa yeniden deneme sınırı 7** — toplam İLETİM DENEMESİ (ns-3 `FrameRetryLimit`); simülatörün alanı yeniden deneme sayısı olduğu için 6 (K-223) (RTS varsayılanda kapalı, 512 B'lık çerçeveler kısa sınıfta; eski dünyanın 4'ü "uzun" sınırdı).
- **Boer'den (G2):** Tx↔Rx dönüşleri 10 / 5 µs · ED süresi 15 µs.
- **Model:** ACK zaman aşımı yayılım gecikmesini kapsar. ACK 14 B (alan toplamı; standardın metniyle doğrulanmadı).

## 7 · Gözlem penceresi v2 — gerçek telsiz ve otopilot ne verir (Faz 2)

| alan | gerçek karşılığı |
|---|---|
| alınan çerçevenin RSSI'ı | her 802.11 alıcısı raporlar; Doodle Labs önerilen aralık −25…−85 dBm (G7) |
| gürültü/girişim ölçümü | var (bugün de) |
| kanal doluluk oranı | CCA meşgul süresi / pencere (802.11k kanal yükü); karıştırma tespitinin girdisi (G5) |
| PHY hata sayısı | sezilen ama CRC'den geçmeyen çerçeve |
| kulak misafiri | başkasına giden, çözülen çerçeve (izleme kipi); havaya ek bayt yok |
| kendi konum · hız · yön | GPS/INS (G7: 1,5 m CEP) |
| komşu konumu | **yalnız** bedeli ödenmiş mesajla |
| görmez | karıştırıcının yeri, gücü, açık olup olmadığı · gerçek bağ kalitesi · topoloji |

## 8 · Senaryo eksenleri (Faz 3)

**Düğüm kaybı** (vurulma, arıza; sayı ve anlar tedavi) · **trafik yoğunluğu** · **enerji:** telsiz gücü gönderimde ≤ 10,6 W, alım/dinlemede 2 W, uykuda 1,2 W (G7, taktik mesh telsizi) × süreler. İHA'da itki enerjisinin yanında küçük kaldığı için raporlanır, tasarım ölçütü değildir.

## 9 · Öngörüler — ölçmeden önce yazıldı · sonuçları

Sonuç: 1 ✅ Li zinciri sabit hızda banda girdi, 0,127 (K-187) → 0,1188 (K-219, 84 B beacon) · 2 ✅ ED kilidi referans dünyada gözlendi (K-181; kayıp anatomisinde `ed` bölgesi) · 3 ✅ taban protokoller referans dünyada yeniden kabul edildi ve dondu (U1, K-218).

1. **Uzamsal yeniden kullanım artar.** 2 Mb/s'te gereken SIR 16 dB → +1,2 dB. Eşit güçlü bir girişimcinin bağı bozmadığı mesafe oranı 6,31 → ~1,15 (α = 2, `10^(β/20)`). Önbelge sezme / iletim menzili ≈ 10^((−92,4 + 97,0)/20) ≈ 1,7. → Li replikasyonunda oran 0,0871'den yukarı, bandına (0,10–0,20) doğru kayar.
2. **Karıştırıcının iki etkisi ayrışır:** uzakta alıcı SINR'ı, yakında ED-CCA ile vericinin susması. Karıştırıcı yakınındaki düğümlerin kuyruğu dolar; kayıp anatomisinde "kanal erişim kilidi" diye görünür.
3. **Taban protokollerin mutlak teslimi değişir** (U1 yeniden). Yönleri önceden söylenemez; yeniden kabul Faz 4.3'te.

## 10 · Açık

| # | ne | durum |
|---|---|---|
| a–c | verici gücü, sürü, tehdit rejimi | 🟢 onaylandı (25 Eylül) |
| d | 802.11 MAC sabitleri — standardın kendisi erişilemedi (ücretli); standarda atıf veren iki bağımsız açık uygulamadan alındı (G12, G13) | 🟢 25 Eylül |
| e | Doodle Labs veri sayfası | 🟢 G7 |
| f | Hava–hava Rician K — Goddemeier & Wietfeld 2015 ücretli, erişilemedi; açık taramalardan dolaylı aralık (G10, G11); Faz 4.4'te DUYARLI → eksen (K-214, K-215) | 🟡 aralık + eksen |
| g | NATO sınıflandırması | 🟢 G9 |
| h | GPS hatası (G7) · telsiz enerjisi (G7) | 🟢 · telemetri akış hızı (S4) ⏳ |
| i | **alan (§3)** — Faz 4.1a (26 Eylül): referans telsizle bağ 1 Mb/s'te ~9–10 km; 7 km'de derece 37,4, çiftlerin %96'sı tek atlama. Onaylı ölçüt (kopukluk %0, derinlik en büyük) **35 km** seçiyor: derece 8,82, derin çift %31,9 (eski dünyanın noktası 8,67 · %31,0). §3'ün ~6–8 km'si 10 dB paylı nominal bağa (1,65 km) dayanıyordu. `arsiv/teshis/faz4_2026-09-26/a_calisma_noktasi_sonuc.md` | 🟢 K-185/K-188: 33 km (öğrenci: gerçekçilik önce, karar ajanın) |
