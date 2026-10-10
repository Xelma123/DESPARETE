# 02 — DOĞRULANMIŞ KAYNAKLAR

> Güncel: 10 Ekim 2026 — literatür bulguları (eski `10`) §L'ye katıldı. Önceki sürümler `arsiv/02-DOGRULANMIS-KAYNAKLAR-*.md`, `arsiv/10-LITERATUR-KOD-KARSILASTIRMA-*.md`.
> Buradaki her kaynak **tek tek açılıp okunmuş** ve iddiayı gerçekten destekleyip desteklemediği kontrol edilmiştir — projenin en pahalı varlıklarından biri. **Kural:** bulunamayan bir atıf rapora giremez; üretken yapay zekânın verdiği hiçbir atıf kaynağı fiilen açılmadan kullanılamaz; rapora girecek her sayı için birincil kaynak açılır (ikinci el tarama `protokol_kaynaklari/literatur_taramasi_2026-08-31/` bunun yerini almaz — `10`). Ham doğrulama notları saklanır.
> **İşaretler:** ✓ doğrulandı · ~ kısmen · ✗ bulunamadı / yeniden doğrulanamadı · ○ ertelendi.

---

## A · Problem motivasyonu

| # | iddia | kaynak | durum |
|---|---|---|---|
| A1 | Ukrayna'da aylık ~10 000 İHA kaybı; her 10 km cepheye ≥ 1 büyük EH sistemi | RUSI, *"Meatgrinder: Russian Tactics in the Second Year of Its Invasion of Ukraine"*, Watling & Reynolds, 19 Mayıs 2023, s.4 ¶2 | ✓ yalnız büyüklük mertebesi (yazarlar kesin değil diyor) |
| A2 | FPV %60–80 | Col. Vytis Andreika, *Military Review*, "Lessons from Ukraine", s.9 | ~ anlam kayması: kaynak *"both sides jammed 60–80 percent of all FPVs"* diyor — "hedefe ulaşamadı" değil, "her iki taraf" |
| A5a | İHA hızları 30–400 km/h | Mahalakshmi & Ranjitha Kumari, IJRTE 8(5), s.1 | ✓ (arXiv 2108.13154 doğrulanamadı, değiştirildi) |
| A5b | çok atlamalı zincirde verim düşüşü | Li, Blake, De Couto, Lee, Morris, *"Capacity of Ad Hoc Wireless Networks"*, §3.2 | ✓ ideal MAC zincir kullanımı 1/3 · ideal zincir tek atlamanın 1/4'ü · 802.11 gerçekte 1/7'si (replikasyon `09`) |
| A6 | tek kanallı mesh (BATMAN-adv) karıştırma altında bağlantıyı tamamen yitiriyor | Deo, Schuß, Baddeley, Boano, *"Robust Wi-Fi Mesh Networking with SPIDERMAN"*, TU Graz | ✓ deneysel |

## B · Literatür boşluğu

| # | iddia | kaynak | durum |
|---|---|---|---|
| B5 | RL karıştırma önleme politikaları durağan ortama göre optimize olur; desen değişince yeniden eğitim gerekir | Hu, Shao, Qian, Du, Li, Lin, Wang, *"Meta-Reinforcement Learning in Time-Varying UAV Communications: Adaptive Anti-Jamming Channel Selection"*, Introduction | ✓ |
| B6 | 13 Q-öğrenme tabanlı FANET yönlendirme protokolü; tablo tabanlı yöntemler küçük FANET'e uygun | *"Reinforcement Learning-Based Routing Protocols in Flying Ad Hoc Networks: A Survey"*, Mathematics 2022, 10, 3017, s.49 + Table 26 | ✓ (sayı yeni taramada 14; üyelik farkı var) |
| B7 | Table 26: mevcut ödül fonksiyonlarının hiçbirinde girişim/karıştırma terimi yok (QTAR · QMR · QGeo · QLGR · FEQ-routing-SA satırları o zaman kopyalandı) | aynı derleme, Table 26 | ✗ **1 Eylül: yeniden doğrulanamadı** (MDPI tam metni erişilemedi). **Karar (1 Eylül):** özgünlük iddiası taramanın kendi yeniden üretilebilir matrisine dayanır — 11 protokol, "açık karıştırma" 9'unda yok (§L). B7 silinmez |
| B8 | FEQ-routing-SA öğrenme oranını düğüm hızına, PARRoT iskonto çarpanını bağ ömrüne göre uyarlıyor | aynı derleme | ✓ |
| B9 | DRL yaklaşımları yüksek hesaplama maliyeti ister | Termehchi vd.; Jiao vd.; Hu vd. | ✓ |

Taramanın getirdiği iki boşluk: **A** — SJR'ye bağlı PDR/E2E verisi yok (adlandırılmış protokollerle; §L) · **B** — RF karıştırma altında rota kurtarma gecikmesi yok.

## C · Yöntem kaynakları

| # | ne için | kaynak | durum |
|---|---|---|---|
| C4 | Q-Routing | Boyan & Littman, 1994 | ✓ |
| C6 | Random Waypoint hız çürümesi (ortalama hız durağan değere yakınsamaz) | Yoon, Liu & Noble 2003, *"Random Waypoint Considered Harmful"* | ✓ |
| C3 | ETX metriği | De Couto vd. | ○ |
| C2 | Gauss-Markov mobilite | Liang & Haas | ○ |
| C5 | gölgeleme korelasyonu | Gudmundson, Electronics Letters | ○ |

## D · Öncül çalışma — ve düzeltilen bir atıf hatası

Vu Khanh Quy, Nguyen Tien Ban, Nguyen Dinh Han, *"A High-Performance Routing Protocol for Multimedia Applications in MANETs"*, Journal of Communications 14(4), Nisan 2019 — ✓. Bir yapay zekâ aracı makalenin adındaki "Q"dan Q-learning kullandığı sonucunu çıkarmıştı; **makale okunarak düzeltildi**: AODV'yi bant genişliği ve gecikme QoS'uyla genişletiyor (`Cost_Delay_Bandwidth`), Q-learning/Q-tablo/ödül/ε-greedy yok, karıştırıcı altında test yok. Doğru konumlandırma: *"QoS-aware AODV routing under varying mobility"*. Bu örnek, ikinci el özetlerin neden birincil kaynakla doğrulanması gerektiğini gösterir. Table I: 200 düğüm · 1500×1500 m · menzil 250 m · RWP 0…Vmax (2–20 m/s) · 50 CBR bağlantı, 1024 B, UDP · 1 Mb/s · 500 s · NS-2.34; AODV ~%98 (2 m/s) → ~%65 (20 m/s). Paket/saniye Table I'de yok — çıkarılmaz.

## E · Rapordan çıkarılmış iddialar — geri getirilmez

"AODV/OLSR/BATMAN karıştırma altında < %50 PDR" (birincil kaynak yok → araştırma sorusu oldu) · "Nature Scientific Reports 2026" RL boşluk analizi (bulunamadı) · "FedRoute PDR %6,5 / gecikme %14,5" (künye yok) · "Q-AODV bir Q-learning protokolüdür" (çürütüldü, §D). Doğrulama üç iddiayı çıkardı, dört yenisini getirdi (Li vd. · SPIDERMAN · Hu vd. · Mathematics derlemesi).

## R · Protokol birincil kaynakları

**R1 · AODV — RFC 3561** ✓ Perkins, Belding-Royer, Das, *"Ad hoc On-Demand Distance Vector (AODV) Routing"*, Temmuz 2003, Experimental. §10: ACTIVE_ROUTE_TIMEOUT 3 000 ms · HELLO_INTERVAL 1 000 ms · ALLOWED_HELLO_LOSS 2 · NET_DIAMETER 35 · NODE_TRAVERSAL_TIME 40 ms · RREQ_RETRIES 2 · MY_ROUTE_TIMEOUT 2 × ACTIVE_ROUTE_TIMEOUT · DELETE_PERIOD K × max(ACTIVE_ROUTE_TIMEOUT, HELLO_INTERVAL), K = 5. Kopya `protokol_kaynaklari/rfc3561_aodv.txt`.

**R2 · OLSR — RFC 3626** ✓ Clausen, Jacquet (INRIA), *"Optimized Link State Routing Protocol (OLSR)"*, Ekim 2003, Experimental. §18: HELLO_INTERVAL 2 s · REFRESH_INTERVAL 2 s · TC_INTERVAL 5 s · NEIGHB_HOLD_TIME 6 s · **TOP_HOLD_TIME 15 s** (Θ'nın paydası) · DUP_HOLD_TIME 30 s · C = 1/16 s · WILL_DEFAULT 3 · MAXJITTER HELLO_INTERVAL/4 = 0,5 s · histerezis HIGH 0,8 · LOW 0,3 · SCALING 0,5. **R2.1** (19 Eylül, ham metin ikinci kez) biçimler (§3.3 · §6.1 · §9.1): paket başlığı 4 B · mesaj başlığı 12 B (§3.3.1 "Packet Length < 16 atılır" = 4 + 12) · HELLO 4 + Σ(4 + 4n) · TC 4 + 4n. Vtime kodlaması `C·(1 + a/16)·2^b`; belgenin dört örneği (2 s → (0,5) · 6 → (8,6) · 15 → (14,7) · 30 → (14,8)) kodlayıcının sınav vektörleri. İsteğe bağlı: bağ histerezisi §14 (SHOULD) · bağ katmanı bildirimi §13 (MAY; K-147'de uygulandı, K-196'da varsayılan kapalı — referans dünyada zarar veriyordu). ✗ Ders (19 Eylül): web özetleyicinin üç hatası (paket başlığı "16 B", Reserved "13 bit", MAXJITTER "0,04 s") ham metinle yakalandı — bayt bayt sadakat ham metinden okunur. Kopya `protokol_kaynaklari/rfc3626_olsr.txt`.

**R3 · Koşum beacon'ı straw-man riski** (8 Eylül): tek 1 s'lik koşum beacon'ı OLSR'ı RFC'sinin iki katı hızda yayınlatırdı. Çözüldü: her taban protokol kendi HELLO'sunu kullanır (`kosum_beaconi = False`; K-121 · K-136 · K-142).

**R4 · AOMDV** ✓ M. K. Marina, S. R. Das, *"On-demand Multipath Distance Vector Routing in Ad Hoc Networks"*, Proc. IEEE ICNP, s. 14–23, 2001 (dergi sürümü WCMC 6(7):969–988, 2006, DOI 10.1002/wcm.432, ücretli). Depodaki kopya ortak yazarın sayfasından, tamamı okundu; Şekil 3 (güncelleme kuralı) ve k = 3 metinde bozuk olduğu için ekran görüntüsünden (`protokol_kaynaklari/README.md`). ICNP sürümünde rota bakımı, veri yolu seçimi ve yol başına zaman aşımı yok. **R4.1** ns-2.35'in AOMDV'si yazarların değil (Caleffi, 2008; iki ek parametre) — üçüncü taraf gerçeklemesi. **Karar (22 Eylül): seçenek a — makale + RFC 3561** (b: ns-2 seçimleri, reddedildi); ns-2 seçimleri ithal edilmez, belirtilmemiş seçimler `protokoller/aomdv.py` başlığında beyanlı.

## G · Gerçekçilik kaynakları (25 Eylül; K-168, Faz 0) — kopyaları ve denetimleri `protokol_kaynaklari/README.md`

**G1 · 802.11b hata modeli** ✓ Pei & Henderson, *"Validation of ns-3 802.11b PHY model"*, Boeing, Mayıs 2009 — tamamı okundu. Gürültü 22 MHz'de; Eb/N0 = SINR·22 (1 Mb/s DBPSK, `½e^−Eb/N0`) · SINR·11 (2 Mb/s DQPSK, Ferrari–Corazza yaklaşımı) · CCK 5,5 ve 11 Mb/s (Pursley–Royster). CMU ölçümleriyle (Judd & Steenkiste 2008; Prism 2.5, gürültü tabanı ≈ −99 dBm) karşılaştırılmış: kip sırası ve aralıkları tutuyor, 1 Mb/s eğrisi ölçümden ~2 dB sağda. Sonuç: bu çalışmanın gövde modeli ısıl gürültüye karşı bununla eşdeğer (gürültü 2 MHz'de), ama **girişime ve karıştırmaya karşı işlem kazancı yok** (~10,4 dB fazla zarar); önbelge DBPSK'sı 3 dB eksik krediliyor (Faz 1b).

**G2 · 802.11 DSSS PHY** ✓ Boer, IEEE P802.11-96/49E, Mart 1996 (çalışma grubu eğitimi; taslaktan) — tamamı okundu. Barker 11 çip, kodlama kazancı 10,4 dB · CCA mod 1/2/3 · ED eşiği >100 mW −80 dBm, >50 mW −76, ≤50 mW −70 dBm; enerji sezme 15 µs · slot 20 µs · Tx→Rx 10 µs, Rx→Tx 5 µs · duyarlılık −80 dBm (FER 0,08, 1024 B) · önbelge + başlık 192 bit, her zaman 1 Mb/s DBPSK.

**G3 · Babel — RFC 8966** ✓ Chroboczek & Schinazi, Ocak 2021, Standards Track — §1–§2 okundu. Uygulanabilirlik mesafesi (§2.4: ilan, bildirilen metrik FD'den kesin küçükse kabul) · sıra numaralı rotalar (§2.5) · açlıkta hedefe sıra isteği, uygulanabilirliğe bakılmadan iletilir (§2.6). DESPARETE'nin DFSN + FD'si bu ailede.

**G4 · MAVLink** ✓ Koubâa vd., arXiv:1906.10641, 2019. Mesaj 8–263 B (v1; v2'de + 13 B imza), yaşam sinyali ~1 Hz; telemetri telsizleri +20…+30 dBm.

**G6 · Yer–hava kanalı** ✓ Al-Hourani, Kandeepan, Lardner, *"Optimal LAP Altitude for Maximum Coverage"*, IEEE WCL 2014 — tamamı okundu. PL = FSPL + η; görüş hattı olasılığı P(LoS, θ) = 1/(1 + a·exp(−b[θ − a])) (θ yükseklik açısı, derece; a, b ITU ortam parametrelerinden Tablo I–II polinomlarıyla); ortalama ek kayıp (η_LoS, η_NLoS): banliyö (0,1; 21) · kentsel (1,0; 20) · yoğun (1,6; 23) · yüksek yapılı (2,3; 34) dB. Yerdeki karıştırıcı → İHA bağının modeli.

**G7 · Taktik İHA mesh telsizi** ✓ Doodle Labs, *Smart Radio RM-2450 Datasheet*, 20 Aralık 2021 — tamamı okundu. Çıkış 27 dBm (Pro) · 33 dBm (Xtreme) · EIRP sınırı ABD 4 W, **Avrupa 100 mW** · DC güç gönderimde ≤ 10,6 / 14 W, alımda 2 W, uykuda 1,2 W · tümleşik GPS 1,5 m CEP · 802.11b/g/n uyumlu (kendi dalga biçimi COFDM).

**G8 · Hava–hava / yer–hava bağlantı yönetimi** ~ Goddemeier, Daniel, Wietfeld, *"Role-Based Connectivity Management with Realistic Air-to-Ground Channels for Cooperative UAVs"*, IEEE JSAC 30(5), 2012 — kanal bölümü okundu. Hava–hava için serbest uzay **varsayımı** (ölçüm değil) · yer–hava için yüksekliğe bağlı yol kaybı üsteli ve anten yönlülüğü; 802.11g, 5–10 İHA, ≤ 50 km/h. İstenen 2015 hava–hava Rice ölçümü değil (S1 açık).

**G9 · NATO İHA sınıflandırması** ✓ Kütük, *"UAS … Stability Policing"*, NATO SPCoE, 2025, §1.4.3, NATO ATP-3.3.8.1 Ed. B (2019)'dan: **Sınıf I küçük (>15 kg): taktik birlik · ≤ 5 000 ft AGL · görev yarıçapı 50 km (LOS) · ör. ScanEagle** · Sınıf II ≤ 18 000 ft AGL, 200 km. Kopya depoda değil (yayıncı notu), künye ve SHA-256 `protokol_kaynaklari/README.md`de.

**G10 · İHA kanal taraması** ✓ Khuwaja, Chen, Zhao, Alouini, Dobbins, *"A Survey of Channel Modeling for UAV Communications"*, arXiv:1801.07359 (IEEE COMST 2018) — hava–hava bölümü okundu. **Hava–hava yol kaybı üsteli ölçümleri:** 1,92 · 0,93 · 2,05 (802.15.4) · **2,6** (Goddemeier & Wietfeld 2015; 802.11, 2,4 GHz, 20 dBm, 5 dBi, 10–40 m) · 2,03 (802.11a, 15–110 m) → α = 2 destekleniyor. Hava–hava Rician K yalnız "yüksekliğe bağlı", sayı yok.

**G11 · Yer–hava kanal taraması** ✓ Khawaja, Guvenc, Matolak, Fiebig, Schneckenburger, *"A Survey of Air-to-Ground Propagation Channel Modeling for Unmanned Aerial Vehicles"*, arXiv:1801.01656 (IEEE COMST 2019) — K faktörü bölümü okundu. Rician K: alçak irtifa yer–hava 2–5 dB, (−5)–10 dB, ağaçlıkta 2–10 dB · güçlü görüş hattında ortalama L bandı ~12 dB, C bandı 27,4–31,3 dB; K yükseklik açısıyla artar.

**G12 · ns-3 (uygulama kaynağı)** ~ ns-3-dev `src/wifi` (GPL-2.0), 25 Eylül 2026 — dosyalar standarda atıf veriyor: DSSS SIFS 10 µs ve slot 20 µs (*"Table 16-4 … 802.11-2020"*) · 802.11b CWmin 31, CWmax 1023 · kısa yeniden deneme sınırı 7, uzun 4 · RTS varsayılanda kapalı (*"C.3 MIB … 802.11-2020"*) → 512 B'lık çerçeveler kısa sınıftadır · uzun önbelge 144 + 48 µs.

**G14 · ns-3 ARF (uygulama kaynağı)** ~ ns-3-dev `src/wifi/model/rate-control/arf-wifi-manager.{cc,h}` (GPL-2.0), 26 Eylül 2026, tamamı okundu — Kamerman & Monteban 1997'nin ARF'si (paket sayaçlı): en düşük hızdan başla · 10 art arda başarı ya da 15 iletim → bir hız yukarı (kurtarma kipi) · kurtarmada ilk başarısızlık, normalde art arda 2 başarısızlık → bir hız aşağı. Özgün makale (Bell Labs Tech. J. 1997) açılmadı → ↪. CCK 5,5/11 Mb/s hata modeli G12'nin `dsss-error-rate-model.cc`sinde (Pursley–Royster, G1). K-177.

**G13 · Linux cfg80211 (uygulama kaynağı)** ~ `net/wireless/core.c` (GPL-2.0): *"IEEE 802.11 MIB default values"* — `retry_short = 7`, `retry_long = 4`, RTS kapalı. G12'den bağımsız, aynı değerler.

**G15 · ns-3 çerçeve başlıkları, MAC kuyruğu, yakalama (uygulama kaynağı)** ~ ns-3-dev (GPL-2.0), 30 Eylül 2026 (K-203) — `wifi-mac-header.cc` `GetSize`: veri başlığı 2 + 2 + 6 + 6 + 6 + 2 = **24 B**, onay 2 + 2 + 6 = **10 B**; FCS **4 B** (`wifi-standard-constants.h` `WIFI_MAC_FCS_LENGTH`, G12) → onay çerçevesi **14 B** · `llc-snap-header.cc` LLC/SNAP (değeri G16) · `wifi-mac-queue.cc` MAC kuyruğu **500 paket, en çok 500 ms bekleme** · `simple-frame-capture-model.cc` + `frame-capture-model.cc` yakalama **5 dB** fark, önbelge sezildikten sonraki **16 µs** içinde. Son ikisi bugünkü modelden farklı (50 paket, süresiz · 10 dB, 192 µs) → değer değil, duyarlılık sorusu (Faz 4.4).

**G16 · IP/UDP/802.2 kapsüllemesi** ✓ RFC 791 (IPv4, 1981): başlık en az 5 × 32 bit = **20 oktet** · RFC 768 (UDP, 1980): başlık **8 oktet** · RFC 1042 (IP over IEEE 802, 1988): *"The total length of the LLC Header and the SNAP header is 8-octets"*. RFC Editor'ün kanonik metinleri, 30 Eylül 2026 (K-203).

**G17 · IP veri paketinin varsayılan TTL'i** ✓ RFC 1700 (Reynolds & Postel, *"Assigned Numbers"*, STD 2, Ekim 1994; RFC 3232 ile tarihsel, kayıtlar IANA'da çevrimiçi), "IP TIME TO LIVE PARAMETER": *"The current recommended default time to live (TTL) for the Internet Protocol (IP) is 64."* Bağımsız uygulama kaynağı: ns-3-dev `ipv4-l3-protocol.cc` `DefaultTtl` = **64**. RFC 791 (G16) TTL'in anlamını verir, değer vermez; RFC 3626 OLSR'ın TTL'i yalnız kendi kontrol mesajlarınındır. 6 Ekim 2026 (K-215).

**G5 · Karıştırma taraması** ✓ Pirayesh & Zeng, arXiv:2101.00292v1, 2021 (dergi sürümü IEEE COMST 2022). Sürekli, aldatıcı, reaktif, taramalı saldırılar; reaktif karıştırıcı < 4 µs geçiş ister · karıştırma tespiti gürültü, kanal meşgul oranı, çerçeveler arası süre, sinyal gücü, teslim oranıyla (Puñal vd.) · hız uyarlaması düşük güçlü girişimde etkili, yüksek güçlü sürekli karıştırmada etkisiz (Pelechrinis vd.).

## S · Doğrulanmayı bekleyen kaynak soruları

| # | soru | neden önemli |
|---|---|---|
| S1 | Rician K = 6 dB (yer yansımasıysa Γ ≈ 0,50) bu hava-hava geometride makul mü? | kısmen (25 Eylül): hava–hava için doğrudan ölçüm erişilemedi (Goddemeier & Wietfeld 2015 ücretli). Dolaylı kanıt G11: alçak irtifa yer–hava 2–10 dB, güçlü görüş hattı ~12 dB (L) – ~30 dB (C). 6 dB kötümser uçta → K **aralık olarak** kullanılır (`14` §2) |
| S2 | 802.11b MAC/PHY sabitleri (slot, SIFS, CW, önbelge, bit hızları, ACK boyu; yeniden deneme sınırı) — IEEE 802.11-2016 | uygulama kaynaklarıyla kapandı (G12, G13 + G1, G2): slot 20 · SIFS 10 µs · CW 31/1023 · önbelge 192 µs · **kısa yeniden deneme 7**. ACK boyu **14 B** G15 ile (başlık 10 B + FCS 4 B, 30 Eylül) |
| S3 | karıştırıcıların saha davranışı (platform, hız, yayın/sessizlik düzeni, sayı) | ~ nitel çerçeve literatür sentezinden (`…/02_proje_özeli_literatür/taktik-iha-mesh-karistirici-saha-davranislari.md`); nicel saha verisi açık literatürde sınırlı; Pirayesh & Zeng doğrulandı (G5), öteki künyeler (Xu, Trappe vd. 2005; Xu, Zhang & Lu 2023) tek tek doğrulanmadı · karıştırıcı güçleri için yalnız üretici sayfaları bulundu (10–200 W; kanıt gücü düşük) |
| S4 | yere toplama trafiği: telemetri hızı ve boyu, geçit mimarisi | kısmen (G4): mesaj boyları ve yaşam sinyali; akış hızları (ArduPilot varsayılanı 4 Hz) birincil kaynaktan doğrulanmadı |
| S5 | kontrol kapsülleme boyutları: 802.11 başlık 24 B + FCS 4 B · LLC/SNAP 8 B (RFC 1042) · IPv4 20 B (RFC 791) · UDP 8 B (RFC 768) | G15 + G16 ile kapandı (30 Eylül) |
| S6 | Babel — RFC 8966 (DESPARETE'nin döngüsüzlük koşulunun ailesi; kök README'de anılıyor) | doğrulandı (G3, 25 Eylül) |
| S7 | taktik telsiz · yer–hava kanalı · NATO sınıfı · GPS hatası · telsiz enerjisi | G6 · G7 · G9 ile kapandı (25 Eylül). Açık kalan: hava–hava Rician K (S1 — Goddemeier & Wietfeld, *"Investigation of Air-to-Air Channel Characteristics and a UAV Specific Extension to the Rice Model"*, IEEE GLOBECOM Workshops 2015; gelen dosya 2012 JSAC makalesiydi) · IEEE 802.11 standardının kendisi (S2; gelen dosya madde 21 kesitiydi) |

## L · Literatürün projeye verdikleri (eski `10`, tarama `protokol_kaynaklari/literatur_taramasi_2026-08-31/`)

Kural: "literatür şunu diyor" cümlesi hangi dosyanın hangi örneklemden söylediği yazılmadan kurulmaz; hiçbir literatür sayısı projeye ölçülmeden alınmaz.

- **Literatür kendi içinde çelişiyor:** koşu süresi medyan ~200 s ↔ 900–1000 s · bit hızı 1–2 ↔ 2 Mb/s · menzil 200–550 ↔ ~250 m; MobiHoc bildirilerinin %87,8'i güven aralığı raporlamamış. Kaynakların kendi varyansı projenin kaynaktan sapmasından büyük.
- **Boşluk A** (K-081): değişen karıştırma şiddetinde AODV/OLSR'nin raporlanmış PDR ve gecikme düşüşü yok → proje AODV · OLSR · AOMDV ile doldurur; GPSR kapsam dışı olduğu için **kısmen**, açıkça yazılır.
- **Doğruladıkları:** soyutlama seviyesi SINR → PER → Bernoulli, parça başına (en yaygın ve titiz seviye) · kâhin yasağı dış kaynaklı ("karıştırıcı gücü, konumu, etki yarıçapı yalnız simülatörce bilinir") · tablo tabanlı öğrenme yeni bağımlılık istemez · "açık karıştırma" teriminin 11 protokolün 9'unda olmaması (dosya 17'nin matrisi) · ön-kayıt yöntemi ADEMP-PreReg (Siepe vd. 2024) ile örtüşür.
- **Uyarılar:** literatürün kendi ödül formülü kâhin içeriyor (dosya 14 §5.7, §11.1) — o kod kopyalanmaz · `01`'in "Table 26" iddiası yeniden doğrulanamadı, özgünlük dosya 17'nin matrisine dayanır · asgari bağımlı değişken kümesi (PDR + PSR · gecikme ortalama ve p95 · yük ve NRL · kopma sayaçları · Δ ve COR; hücre başına ≥ 20 tekrar, %95 GA) `sim2/`de karşılanıyor · AODV'nin literatürdeki çöküş mekanizması (hareket → kopma → RREQ seli) statik kolda oluşmaz; statikte kopma yalnız karıştırmadan gelir — iddia bu sınırla yazılır · kontrol kanalını hedefleyen karıştırma (~20 dB daha verimli) modellenmedi (kapsam dışı).
