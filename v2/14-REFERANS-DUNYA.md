# 14 · REFERANS GERÇEK DÜNYA — simülatörün 1:1 karşılığı

> **Durum: onaylandı** (K-169) ve uygulandı (`sim2/kanal/dunya.py::referans_2026`). Alan 33 km (K-188), karıştırıcı referans tabanı 10 W ve birincil hücre `derin_sizma` (K-186). Güncel: 14 Ekim 2026; eski dünyayla karşılaştırma ve öngörüler `arsiv/14-REFERANS-DUNYA-*.md`.
> **İlke:** simülatör ve gözlem sözleşmesi gerçek bir İHA sürüsünde olanı modeller. Her sayı ya **kaynaklı** (`02`), ya **betikle hesaplanmış**, ya da **onaylı karar**dır.
> **Üretici:** `python arsiv/teshis/referans_dunya_2026-09-25/bag_butcesi.py` (çıktı yanında) — yalnız aritmetik, simülasyon yok.

---

## 1 · Telsiz — 802.11b DSSS

| büyüklük | değer | köken |
|---|---|---|
| bant · kanal | 2,4 GHz ISM · kanal 6 (2 437 MHz) · 22 MHz | G2 |
| hızlar | 1 (DBPSK) · 2 (DQPSK) · 5,5 · 11 Mb/s (CCK); önbelge + başlık 192 bit, hep 1 Mb/s | G1, G2 |
| hata modeli | Eb/N0 = SNR·22 (1 Mb/s) · SNR·11 (2 Mb/s) · CCK Pursley–Royster; gürültü 22 MHz'de | G1 (CMU ölçümüyle karşılaştırılmış) |
| gürültü | NF 7 dB → **−93,6 dBm** | G1 · betik |
| duyarlılık (PER ≤ %10, 576 B) | **1 Mb/s −97,0 · 2 Mb/s −92,4 dBm** | betik · standardın alt sınırı −80 dBm (G2) · CMU Prism 2.5 ≈ −94…−100 (G1) |
| **verici** | **EIRP 20 dBm (100 mW)** — AB/Türkiye 2,4 GHz sınırı EIRP'dir (anten dâhil); dipolle iletilen ≈ 17,9 dBm (61 mW). Çalışma noktası bu sınıftaki telsizin erişim sınırına gerilmiş seyrek ağıdır; taktik telsiz gücünde aynı alan yoğun ağdır ve "ölçekli karşılık" gerekçesi tutmaz (hızlar, gölgeleme hücresi, yayılım gecikmesi ve yer–hava açıları ölçeklenmez; K-242) | G2 · G7 (*"In Europe, the max EIRP is 100mW"*) · onaylı |
| keşifsel verici | taktik mesh telsizi: 27 dBm (Doodle Labs Pro) · 33 dBm (Xtreme), MCS 0 | G7 |
| anten | yarım dalga dipol, 2,15 dBi, dikey | bugünkü model |
| ED eşiği | iletilen >100 mW → −80 · >50 mW → −76 · ≤50 mW → −70 dBm → 61 mW'ta **−76 dBm**; ED süresi 15 µs | G2 |
| hız uyarlaması | ARF (ns-3'ün gerçeklemesi, paket sayaçlı; K-181), bütün protokollerde aynı MAC | G14 · düşük güçlü girişimde etkili, güçlü karıştırmada etkisiz (G5) |

**Menzil (serbest uzay, 2 Mb/s, betik):**

| verici | sönümsüz | 10 dB payla | 20 dB payla |
|---|---|---|---|
| EIRP 20 dBm | 5,2 km | **1,65 km** | 0,52 km |
| Doodle Labs Pro (27 dBm + dipol) | 14,9 km | 4,7 km | 1,5 km |
| Doodle Labs Xtreme | 29,8 km | 9,4 km | 3,0 km |

## 2 · Kanal

| | değer | köken |
|---|---|---|
| hava–hava yol kaybı | serbest uzay, α = 2 (iki-ışın kırılma mesafesi 100 m irtifada ~325 km) | fizik · ölçümler 1,92–2,6, 802.11a'da 2,03 (G10) · G8 aynı varsayım |
| gölgeleme | log-normal, σ 3 dB, 2,5 km'lik hücrede korelasyonlu | σ ÖLÇÜLMÜŞ · hücre DÜNYA TANIMI, ölçülen duyarlılığıyla (K-220) |
| hızlı sönümleme | Rician, **K referans 10 dB, aralık 6–15 dB**. DUYARLI ölçüldü → **eksen** (K-215: birincil test 10 dB, 6 ve 15 dB keşifsel) · Doppler gerçek hızdan. Hava–hava için doğrudan ölçüm erişilemedi. Dolaylı kanıt: alçak irtifa yer–hava 2–10 dB, güçlü görüş hattı ~12 dB (L bandı) – ~30 dB (C bandı); hava–hava bağında yer saçılması daha azdır | G11 (dolaylı) · `02` S1 |
| **yer–hava** (yerdeki karıştırıcı → İHA) | Al-Hourani: PL = FSPL + η; P(LoS, θ) = 1/(1 + a·exp(−b[θ − a])); **banliyö** parametreleri (η_LoS 0,1 · η_NLoS 21 dB). Makalede açık kırsal yok; en yakını banliyö (beyan) | G6 |
| yayılım gecikmesi | d / c | fizik |

## 3 · Sürü

| | değer | köken |
|---|---|---|
| sınıf | NATO Sınıf I küçük: ≤ 5 000 ft AGL (~1 520 m), görev yarıçapı ≤ 50 km (LOS) | G9 |
| düğüm sayısı | **40** (çalışma noktasıyla doğrulandı, K-185…K-188) | onaylı |
| alan | **33 km kare**: gölgeleme birimi düzeltildikten sonra ağın kopmadığı en büyük alan (derece 9,67, derin çift %26,9; K-188). Referans telsizle bağ 1 Mb/s'te ~9–10 km; daha küçük alanda sürü tam örgüye yaklaşır (7 km'de derece 37,4). Gerçekçilik önceliğiyle seçildi (K-185); ölçüm `arsiv/teshis/faz4_2026-09-26/a_calisma_noktasi_sonuc.md` | ölçüldü · G9 zarfı (≤ 50 km) |
| irtifa | **50–300 m AGL** | onaylı (G9 zarfı içinde) |
| hız | **40–120 km/h** zarfı — bağımsız ve görev kollarında gerçek hızlarla. Formasyon kolunda sürü istasyon tutar, ortak transit modellenmez (`07` §4): yere göre hız yalnız manevra gürültüsü, ölçülen medyan 12 km/h, en çok 42 (birincil hücre, 1003; 15 Ekim 2026, DD-18). Statik kol durağan | onaylı |
| konum bilgisi | kendi konum ve hızı GPS/INS ile; yatay hata **1,5 m CEP** (σ ≈ 1,3 m/eksen); dikey σ 2 m (kaynaksız, SINANMAMIŞ — `05` §3.3b) · GPS karıştırması kapsam dışı | G7 · karar |

## 4 · Tehdit — karıştırıcılar

**Bağ bütçesi** (betik; serbest uzay, 2 Mb/s, işlem kazancı dâhil, düğüm EIRP 20 dBm): 1 km'lik bir bağı 1 W'lık karıştırıcı **3,7 km**'den, 10 W'lık **11,7 km**'den, 50 W'lık **26,1 km**'den keser. Yerdeki karıştırıcıda bu mesafeler geçerli değildir: yer–hava kanalı (banliyö) küçük yükselme açılarında çoğunlukla görüş hattı dışıdır ve ~21 dB ek kayıp getirir; birincil hücrenin kısmi karıştırma rejimi büyük ölçüde bu kayıptan doğar. Açık arazide aynı güç sürünün çoğunu karartır (denetim DD-01; ortam duyarlılığı Faz 6, K-242).

**Rejim sınırı:** onlarca watt'lık bir karıştırıcı birkaç kilometrelik sürünün tamamını karartır. Orada hiçbir yönlendirme protokolü teslimi kurtaramaz; kurtaran frekans çevikliği ya da hareket olur (ikisi kapsam dışı). Yönlendirmenin fark yaratabileceği rejim, etki alanı sürüden küçük karıştırıcılardır: düşük güçlü, İHA taşıyıcılı, uzaktaki ya da yer–hava kaybıyla zayıflayan. Birincil hücre bu rejimde kurulur ("kısmi karıştırma", ρ ölçütü). Güçlü uç, güç taramasıyla rejimin sınırını gösteren keşifsel eksendir (H1.2 dirseği).

| | değer | köken |
|---|---|---|
| sınıflar | sürekli · darbeli · reaktif (< 4 µs tepki, duyma menzilli) · aldatıcı (sahte çerçeve alıcıyı kilitler) · taramalı | G5 |
| güç | İHA taşıyıcılı 1–5 W · taşınabilir 10 W · araç 50 W. **Referans taban 10 W toplam ortalama, her ailede eşit; birincil hücre `derin_sizma` (hareketli araç), K-186.** Ölçüldü: 1–5 W'lık hava karıştırıcısı sürüyü her geometride böler (en büyük parça %5–20); yer/araç karıştırıcıları 10 W'ta kısmi (ρ 0,16–0,29) | onaylı · üretici sayfaları 10–200 W (kanıt gücü düşük, `02` S3) · `arsiv/teshis/faz4_2026-09-26/b_aile_guc.txt` |
| platformlar | yer (1,5–5 m, yer–hava kanalıyla) · araç · hava; beş tehdit ailesi | onaylı |
| etki | alıcıda SINR (işlem kazancıyla) **ve** vericide ED-CCA: yakınındaki düğüm kanalı meşgul görür, gönderemez | G2 |

## 5 · Trafik

Yere toplama (birincil): her düğümden geçide telemetri **1 pkt/s × 512 B ≈ 4,1 kb/s** (MAVLink ölçeğinde: mesaj 8–263 B, yaşam sinyali ~1 Hz — G4; akış hızı `02` S4) + geçitten 4 düğüme komut 0,25 pkt/s. Eşler arası keşifsel. Trafik yoğunluğu ayrı bir eksendir (tıkanıklık, karıştırmadan bağımsız).

## 6 · MAC zamanlaması

- **Standarttan ya da iki bağımsız uygulamadan (G12 ns-3, G13 Linux):**
  - slot 20 µs · SIFS 10 µs · CWmin 31, CWmax 1023 · uzun önbelge 144 + 48 µs = 192 µs;
  - **kısa yeniden deneme sınırı 7**: toplam iletim denemesidir (ns-3 `FrameRetryLimit`). Simülatörün alanı yeniden deneme sayısı olduğu için 6'dır (K-223).
  - RTS varsayılanda kapalı; 512 B'lık çerçeveler kısa sınıftadır.
- **Boer'den (G2):** Tx↔Rx dönüşleri 10 / 5 µs · ED süresi 15 µs.
- **Model:**
  - Yayılım gecikmesi modellenir: 33 km'lik alanda tipik bağ ~9 km → ~30 µs, slottan (20 µs) uzun. ACK zaman aşımı en büyük gecikmeyle genişletildi; slot ve kapsama sınıfı standart kaldı (beyan; duyarlılığı Faz 6).
  - ACK 14 B (alan toplamı; standardın metniyle doğrulanmadı).

## 7 · Gözlem

Gerçek telsiz ve otopilotun verdiği gözlem ve protokolün göremedikleri: `05` (sözleşme).

## 8 · Senaryo eksenleri

- **Düğüm kaybı:** vurulma, arıza; sayı ve anlar tedavidir.
- **Trafik yoğunluğu.**
- **Enerji:** telsiz gücü gönderimde ≤ 10,6 W, alım/dinlemede 2 W, uykuda 1,2 W (G7) × süreler. İHA'da itki enerjisinin yanında küçük kaldığı için raporlanır, tasarım ölçütü değildir.

## 9 · Açık

| ne | durum |
|---|---|
| hava–hava Rician K | doğrudan ölçüm erişilemedi; dolaylı aralık (G10, G11), eksen olarak kullanılır (K-214, K-215) |
| telemetri akış hızı | birincil kaynaktan doğrulanmadı (`02` S4) |
| slot ve kapsama sınıfının yayılım gecikmesine duyarlılığı | Faz 6 |
