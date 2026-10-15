# 02 — DOĞRULANMIŞ KAYNAKLAR

> Güncel: 13 Ekim 2026. Önceki sürümler `arsiv/02-DOGRULANMIS-KAYNAKLAR-*.md`, `arsiv/10-LITERATUR-KOD-KARSILASTIRMA-*.md`.
> Buradaki her kaynak açılıp okunmuş ve iddiayı destekleyip desteklemediği kontrol edilmiştir. **Kural:** bulunamayan bir atıf rapora giremez; yapay zekâ aracının verdiği hiçbir atıf, kaynak fiilen açılmadan kullanılmaz; rapora girecek her sayı için birincil kaynak açılır. İkinci el tarama (`protokol_kaynaklari/literatur_taramasi_2026-08-31/`) bunun yerini almaz (§L). Dosya kopyaları ve SHA-256'lar `protokol_kaynaklari/README.md`de, rapor künyeleri `16`da.
> **İşaretler:** ✓ doğrulandı · ~ kısmen ya da ilgili bölüm · ✗ bulunamadı / yeniden doğrulanamadı · ○ ertelendi.

---

## A · Problem motivasyonu

| # | iddia | kaynak | durum |
|---|---|---|---|
| A1 | Ukrayna'da aylık ~10 000 İHA kaybı; her 10 km cepheye ≥ 1 büyük EH sistemi | RUSI, *"Meatgrinder: Russian Tactics in the Second Year of Its Invasion of Ukraine"*, Watling & Reynolds, 19 Mayıs 2023, s.4 ¶2 | ✓ yalnız büyüklük mertebesi (yazarlar kesin değil diyor) |
| A2 | FPV %60–80 | Col. Vytis Andreika, *Military Review*, "Lessons from Ukraine", s.9 | ~ kaynak *"both sides jammed 60–80 percent of all FPVs"* diyor: "hedefe ulaşamadı" değil, "her iki taraf" |
| A5a | İHA hızları 30–400 km/h | Mahalakshmi & Ranjitha Kumari, IJRTE 8(5), s.1 | ✓ |
| A5b | çok atlamalı zincirde verim düşüşü | Li, Blake, De Couto, Lee, Morris, *"Capacity of Ad Hoc Wireless Networks"*, §3.2 | ✓ ideal MAC zincir kullanımı 1/3 · ideal zincir tek atlamanın 1/4'ü · 802.11 gerçekte 1/7'si (replikasyon `09`) |
| A6 | tek kanallı mesh (BATMAN-adv) karıştırma altında bağlantıyı tamamen yitiriyor | Deo, Schuß, Baddeley, Boano, *"Robust Wi-Fi Mesh Networking with SPIDERMAN"*, TU Graz | ✓ deneysel |

## B · Literatür boşluğu

| # | iddia | kaynak | durum |
|---|---|---|---|
| B5 | RL karıştırma önleme politikaları durağan ortama göre optimize olur; desen değişince yeniden eğitim gerekir | Hu, Shao, Qian, Du, Li, Lin, Wang, *"Meta-Reinforcement Learning in Time-Varying UAV Communications: Adaptive Anti-Jamming Channel Selection"*, Introduction | ✓ |
| B6 | 13 Q-öğrenme tabanlı FANET yönlendirme protokolü | *"Reinforcement Learning-Based Routing Protocols in Flying Ad Hoc Networks: A Survey"*, Mathematics 2022, 10, 3017, s.49 + Table 26 | ✓ (yeni taramada 14; üyelik farkı var) |
| B7 | Table 26: mevcut ödül fonksiyonlarının hiçbirinde girişim/karıştırma terimi yok | aynı derleme, Table 26 | ✗ yeniden doğrulanamadı (MDPI tam metni erişilemedi). Bu bilgi yerine taramanın kendi matrisi kullanılır: 11 protokolün 9'unda "açık karıştırma" yok (§L) |
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

## D · Öncül çalışma ve düzeltilmiş bir atıf

Vu Khanh Quy, Nguyen Tien Ban, Nguyen Dinh Han, *"A High-Performance Routing Protocol for Multimedia Applications in MANETs"*, Journal of Communications 14(4), Nisan 2019 — ✓.
- **Düzeltilen atıf:** bir yapay zekâ aracı, makalenin adındaki "Q"dan Q-learning kullandığı sonucunu çıkarmıştı.
- **Makalenin gerçek içeriği:** AODV'yi bant genişliği ve gecikme QoS'uyla genişletiyor (`Cost_Delay_Bandwidth`). Q-learning yok, karıştırıcı altında test yok.
- **Doğru konumlandırma:** *"QoS-aware AODV routing under varying mobility"*.
- **Table I:** 200 düğüm · 1500×1500 m · menzil 250 m · RWP 0…Vmax (2–20 m/s) · 50 CBR bağlantı, 1024 B, UDP · 1 Mb/s · 500 s · NS-2.34. AODV ~%98 (2 m/s) → ~%65 (20 m/s).

## E · Rapordan çıkarılmış iddialar — geri getirilmez

"AODV/OLSR/BATMAN karıştırma altında < %50 PDR" (birincil kaynak yok → araştırma sorusu oldu) · "Nature Scientific Reports 2026" RL boşluk analizi (bulunamadı) · "FedRoute PDR %6,5 / gecikme %14,5" (künye yok) · "Q-AODV bir Q-learning protokolüdür" (çürütüldü, §D).

## R · Protokol birincil kaynakları

**R1 · AODV — RFC 3561** ✓ Perkins, Belding-Royer, Das, *"Ad hoc On-Demand Distance Vector (AODV) Routing"*, Temmuz 2003, Experimental. §10 sabitleri:
- ACTIVE_ROUTE_TIMEOUT 3 000 ms · HELLO_INTERVAL 1 000 ms · ALLOWED_HELLO_LOSS 2;
- NET_DIAMETER 35 · NODE_TRAVERSAL_TIME 40 ms · RREQ_RETRIES 2;
- MY_ROUTE_TIMEOUT 2 × ACTIVE_ROUTE_TIMEOUT · DELETE_PERIOD K × max(ACTIVE_ROUTE_TIMEOUT, HELLO_INTERVAL), K = 5.

Kopya `protokol_kaynaklari/rfc3561_aodv.txt`.

**R5 · OLSRv2 — RFC 7181** ✓ Clausen, Dearlove, Jacquet, Herberg, Nisan 2014, Standards Track.
- **Altında:** NHDP (RFC 6130), paket biçimi (RFC 5444), zaman TLV'leri (RFC 5497), titreşim (RFC 5148).
- **Güncelleyenler:** RFC 7183 (bütünlük; kapsam dışı) · 7187 · 7188 · 7466.
- **Bağ metriği:** RFC 7779 (DAT, Experimental). RFC 7181 metrik çerçevesini tanımlar, metriği tanımlamaz.
- **Hakem uygulama:** olsrd2 (OONF, BSD-3, commit `477e716`).
- Gerçekleme için kural kural okundu; denetim `arsiv/teshis/olsrv2_sadakat_2026-10-11/denetim.md`.

**R6 · JarmRout** ✓ C. Pu, *"Jamming-Resilient Multipath Routing Protocol for Flying Ad Hoc Networks"*, IEEE Access 6:68472–68486, 2018. Tamamı okundu; Tablo 4 ve Şekil 4 yayıncı sayfasından (görüntü).
- **Yapı:** DSR tabanlı, iki düğüm-ayrık ve mekânsal olarak uzak yol. Bağ kalitesi RSSI varyansıyla, yük NAV ve kuyrukla ölçülür; çift önceliği ağırlıkları 0,2 · 0,2 · 0,6. Aynı veri paketi iki yoldan gönderilir (§VI.B).
- **Eksikler:** iç parametreler (filtre sabitleri, RSSI örnek sayısı, `t_wait`) makalede yok; kodu açık değil.
- **Makalenin kendi değerlendirmesi:** 1 km², iki-ışın kanal, 300 m menzil, tek CBR kaynağı, sürekli karıştırıcı, OMNeT++.

**R7 · DSR — RFC 4728** ~ Johnson, Hu, Maltz, Şubat 2007, Experimental. JarmRout'un temeli; makalenin sustuğu yerde (istek kimliği, zaman aşımları, rota hatası, kaynak rotası başlığı) hakem. İlgili bölümler okundu.

**Faz 4'ün rakipleri (K-229'dan beri kıyas tabanı değil; künyeleri tarihçe ve literatür bağlamı için kalır):**
- **R2 · OLSR — RFC 3626** ✓ Clausen, Jacquet (INRIA), Ekim 2003, Experimental. §18 sabitleri: HELLO_INTERVAL 2 s · TC_INTERVAL 5 s · NEIGHB_HOLD_TIME 6 s · **TOP_HOLD_TIME 15 s** (evre metriklerinin pencere sabiti `L`, `08` §02) · DUP_HOLD_TIME 30 s · WILL_DEFAULT 3. Kopya `protokol_kaynaklari/rfc3626_olsr.txt`.
- **R4 · AOMDV** ✓ M. K. Marina, S. R. Das, *"On-demand Multipath Distance Vector Routing in Ad Hoc Networks"*, Proc. IEEE ICNP, s. 14–23, 2001. ns-2.35'in AOMDV'si yazarların değildir (Caleffi, 2008).

## G · Gerçekçilik kaynakları (K-168, Faz 0) — kopyaları ve denetimleri `protokol_kaynaklari/README.md`

**G1 · 802.11b hata modeli** ✓ Pei & Henderson, *"Validation of ns-3 802.11b PHY model"*, Boeing, Mayıs 2009 — tamamı okundu.
- Gürültü 22 MHz'de alınır.
- Eb/N0 = SINR·22 (1 Mb/s DBPSK, `½e^−Eb/N0`) · SINR·11 (2 Mb/s DQPSK, Ferrari–Corazza yaklaşımı) · CCK 5,5 ve 11 Mb/s (Pursley–Royster).
- CMU ölçümleriyle (Judd & Steenkiste 2008; Prism 2.5, gürültü tabanı ≈ −99 dBm) karşılaştırılmış: kip sırası ve aralıkları tutuyor, 1 Mb/s eğrisi ölçümden ~2 dB sağda.

**G2 · 802.11 DSSS PHY** ✓ Boer, IEEE P802.11-96/49E, Mart 1996 (çalışma grubu eğitimi; taslaktan) — tamamı okundu.
- Barker 11 çip, kodlama kazancı 10,4 dB · CCA mod 1/2/3.
- ED eşiği: >100 mW −80 dBm, >50 mW −76, ≤50 mW −70 dBm; enerji sezme 15 µs.
- Slot 20 µs · Tx→Rx 10 µs, Rx→Tx 5 µs · duyarlılık −80 dBm (FER 0,08, 1024 B).
- Önbelge + başlık 192 bit, her zaman 1 Mb/s DBPSK.

**G3 · Babel — RFC 8966** ✓ Chroboczek & Schinazi, Ocak 2021, Standards Track — §1–§4 ve Ek A–B okundu (K-244; üçüncü rakip, hakemi babeld 1.14). Uygulanabilirlik mesafesi (§2.4: bildirilen metrik FD'den kesin küçükse kabul) · sıra numaralı rotalar (§2.5) · açlıkta hedefe sıra isteği (§2.6). DESPARETE'nin DFSN + FD'si bu ailededir.

**G4 · MAVLink** ✓ Koubâa vd., arXiv:1906.10641, 2019. Mesaj 8–263 B (v1; v2'de + 13 B imza), yaşam sinyali ~1 Hz; telemetri telsizleri +20…+30 dBm.

**G5 · Karıştırma taraması** ✓ Pirayesh & Zeng, arXiv:2101.00292v1, 2021 (dergi sürümü IEEE COMST 2022).
- Saldırı türleri: sürekli, aldatıcı, reaktif, taramalı. Reaktif karıştırıcı < 4 µs geçiş ister.
- Karıştırma tespiti gürültü, kanal meşgul oranı, çerçeveler arası süre, sinyal gücü ve teslim oranıyla yapılır (Puñal vd.).
- Hız uyarlaması düşük güçlü girişimde etkili, yüksek güçlü sürekli karıştırmada etkisizdir (Pelechrinis vd.).

**G6 · Yer–hava kanalı** ✓ Al-Hourani, Kandeepan, Lardner, *"Optimal LAP Altitude for Maximum Coverage"*, IEEE WCL 2014 — tamamı okundu.
- PL = FSPL + η. Görüş hattı olasılığı P(LoS, θ) = 1/(1 + a·exp(−b[θ − a])); θ yükseklik açısı (derece), a ve b ITU ortam parametrelerinden.
- Ortalama ek kayıp (η_LoS, η_NLoS): banliyö (0,1; 21) · kentsel (1,0; 20) · yoğun (1,6; 23) · yüksek yapılı (2,3; 34) dB.
- Simülatördeki kullanımı: yerdeki karıştırıcı → İHA bağı.

**G7 · Taktik İHA mesh telsizi** ✓ Doodle Labs, *Smart Radio RM-2450 Datasheet*, 20 Aralık 2021 — tamamı okundu.
- Çıkış 27 dBm (Pro) · 33 dBm (Xtreme). EIRP sınırı ABD 4 W, **Avrupa 100 mW**.
- DC güç: gönderimde ≤ 10,6 / 14 W, alımda 2 W, uykuda 1,2 W.
- Tümleşik GPS 1,5 m CEP · 802.11b/g/n uyumlu (kendi dalga biçimi COFDM).

**G8 · Hava–hava / yer–hava bağlantı yönetimi** ~ Goddemeier, Daniel, Wietfeld, *"Role-Based Connectivity Management with Realistic Air-to-Ground Channels for Cooperative UAVs"*, IEEE JSAC 30(5), 2012 — kanal bölümü okundu.
- Hava–hava için serbest uzay bir **varsayımdır**, ölçüm değil.
- Yer–hava için yüksekliğe bağlı yol kaybı üsteli ve anten yönlülüğü; 802.11g, 5–10 İHA, ≤ 50 km/h.

**G9 · NATO İHA sınıflandırması** ✓ Kütük, *"UAS … Stability Policing"*, NATO SPCoE, 2025, §1.4.3; NATO ATP-3.3.8.1 Ed. B (2019)'dan.
- **Sınıf I küçük (>15 kg):** taktik birlik · ≤ 5 000 ft AGL · görev yarıçapı 50 km (LOS) · ör. ScanEagle.
- Sınıf II: ≤ 18 000 ft AGL, 200 km.
- Kopya depoda değil (yayıncı notu); künye ve SHA-256 `protokol_kaynaklari/README.md`de.

**G10 · İHA kanal taraması** ✓ Khuwaja, Chen, Zhao, Alouini, Dobbins, *"A Survey of Channel Modeling for UAV Communications"*, arXiv:1801.07359 (IEEE COMST 2018) — hava–hava bölümü okundu.
- **Hava–hava yol kaybı üsteli ölçümleri:** 1,92 · 0,93 · 2,05 (802.15.4) · 2,6 (802.11, 2,4 GHz, 10–40 m) · 2,03 (802.11a, 15–110 m). α = 2 bu aralıkla uyumlu.
- Hava–hava Rician K için yalnız "yüksekliğe bağlı" deniyor, sayı yok.

**G11 · Yer–hava kanal taraması** ✓ Khawaja, Guvenc, Matolak, Fiebig, Schneckenburger, *"A Survey of Air-to-Ground Propagation Channel Modeling for Unmanned Aerial Vehicles"*, arXiv:1801.01656 (IEEE COMST 2019) — K faktörü bölümü okundu.
- Rician K: alçak irtifa yer–hava 2–5 dB, (−5)–10 dB, ağaçlıkta 2–10 dB.
- Güçlü görüş hattında ortalama L bandı ~12 dB, C bandı 27,4–31,3 dB. K yükseklik açısıyla artar.

**G12 · ns-3 (uygulama kaynağı)** ~ ns-3-dev `src/wifi` (GPL-2.0), 25 Eylül 2026. Dosyalar standarda atıf veriyor:
- DSSS SIFS 10 µs ve slot 20 µs (*"Table 16-4 … 802.11-2020"*) · 802.11b CWmin 31, CWmax 1023.
- Kısa yeniden deneme sınırı 7 (ns-3 `FrameRetryLimit`: toplam iletim denemesi; simülatörün alanı yeniden deneme sayısı, 6, K-223), uzun 4.
- RTS varsayılanda kapalı (*"C.3 MIB … 802.11-2020"*) · uzun önbelge 144 + 48 µs.

**G13 · Linux cfg80211 (uygulama kaynağı)** ~ `net/wireless/core.c` (GPL-2.0): *"IEEE 802.11 MIB default values"* — `retry_short = 7`, `retry_long = 4`, RTS kapalı. G12'den bağımsız, aynı değerler.

**G14 · ns-3 ARF (uygulama kaynağı)** ~ ns-3-dev `src/wifi/model/rate-control/arf-wifi-manager.{cc,h}` (GPL-2.0), tamamı okundu. Kamerman & Monteban 1997'nin ARF'si, paket sayaçlı:
- en düşük hızdan başlar;
- 10 art arda başarı ya da 15 iletim → bir hız yukarı (kurtarma kipi);
- kurtarmada ilk başarısızlık, normalde art arda 2 başarısızlık → bir hız aşağı.

Özgün makale açılmadı. K-177.

**G15 · ns-3 çerçeve başlıkları, MAC kuyruğu, yakalama (uygulama kaynağı)** ~ ns-3-dev (GPL-2.0), K-203.
- Veri başlığı **24 B** · onay başlığı **10 B** · FCS **4 B** → onay çerçevesi **14 B**.
- ns-3'ün MAC kuyruğu 500 paket, en çok 500 ms bekleme. Yakalama 5 dB fark, önbelge sezildikten sonraki 16 µs içinde.
- Bu iki değer simülatörünkünden farklıdır (50 paket, süresiz · 10 dB, 192 µs). Duyarlılıkları ölçüldü: ikisi de DUYARSIZ (K-214, K-217).

**G16 · IP/UDP/802.2 kapsüllemesi** ✓ RFC 791 (IPv4): başlık en az **20 oktet** · RFC 768 (UDP): başlık **8 oktet** · RFC 1042: LLC + SNAP **8 oktet** (K-203).

**G17 · IP veri paketinin varsayılan TTL'i** ✓ RFC 1700 (STD 2, Ekim 1994; RFC 3232 ile tarihsel, kayıtlar IANA'da): *"The current recommended default time to live (TTL) for the Internet Protocol (IP) is 64."* Bağımsız uygulama kaynağı: ns-3-dev `ipv4-l3-protocol.cc` `DefaultTtl` = **64** (K-215).

**G18 · Sürücünün gürültü tabanı raporu (uygulama kaynağı)** ~ Linux v6.6 ath9k (ISC). Gürültü işleme ve kalibrasyon zamanlaması okundu (`calib.c` · `ar9003_calib.c` · `link.c`; sınırlar `ar9003_phy.h` · `ar9002_phy.h`).
- Bildirilen gürültü **−95 dBm + max(0, NF − nominal − 6)**, tamsayı dBm.
- NF son **5** okumanın ortancasıdır ve çipin üst sınırına kırpılır: AR9300'de rapor en çok −51 dBm, AR9280'de en çok −86 dBm.
- NF yalnız uzun kalibrasyonda okunur: olağan kipte **30 s**'de bir.
- Bir sürücü örneğidir, standart değil. K-227'nin kaynağı.

**G19 · Bağ kopması zaman aşımları (uygulama kaynakları)** ~ dört açık kaynak yazılım ve bir protokol belgesi, sabitlenmiş commit'lerden (15 Ekim 2026, K-246):
- ArduPilot (GPL-3.0) Copter `FS_GCS_TIMEOUT` **5 s** (*"Timeout before triggering the GCS failsafe"*) · Plane `FS_LONG_TIMEOUT` **5 s**; `FS_GCS_ENABL`: *"Failsafe will trigger after FS_LONG_TIMEOUT seconds of no MAVLink heartbeat messages"*.
- PX4 v1.14.0 (BSD-3) `COM_DL_LOSS_T` **10 s** (en az 5): *"After this amount of seconds without datalink, the GCS connection lost mode triggers"*.
- QGroundControl `_heartbeatMaxElpasedMSecs` **3 500 ms**: *"No heartbeat for longer than this indicates comm loss"*.
- MAVLink heartbeat servisi: *"components typically publish their heartbeat at 1 Hz and consider another system to have disconnected if four or five messages are not received"*.
- Gecikme tavanlı `PDR_açık`ın eşikleri: 5 s ana, 3,5 s ve 10 s duyarlılık. Zaman aşımları heartbeat'ler arası boşluğu ölçer; veri yaşı tavanı olarak kullanılması modelleme seçimidir.

## S · Açık kaynak soruları

| # | soru | durum |
|---|---|---|
| S1 | hava–hava Rician K | doğrudan ölçüm (Goddemeier & Wietfeld, *"Investigation of Air-to-Air Channel Characteristics and a UAV Specific Extension to the Rice Model"*, IEEE GLOBECOM Workshops 2015) ücretli, açılmadı. Dolaylı kanıt G11 (2–12 dB). K aralık ve eksen olarak kullanılır (`14` §2) |
| S2 | IEEE 802.11 standardının kendisi | ücretli, açılmadı; değerler iki bağımsız uygulama kaynağından (G12, G13) |
| S3 | karıştırıcıların saha davranışı (platform, hız, yayın/sessizlik düzeni, sayı) | ~ nitel çerçeve literatür sentezinden (`…/02_proje_özeli_literatür/taktik-iha-mesh-karistirici-saha-davranislari.md`, ikinci el). Nicel saha verisi açık literatürde sınırlı; karıştırıcı güçleri için yalnız üretici sayfaları bulundu (10–200 W; kanıt gücü düşük) |
| S4 | yere toplama trafiği: telemetri akış hızı | kısmen (G4): mesaj boyları ve yaşam sinyali; akış hızları (ArduPilot varsayılanı 4 Hz) birincil kaynaktan doğrulanmadı |

## L · Literatür taramasından alınanlar (ikinci el, `protokol_kaynaklari/literatur_taramasi_2026-08-31/`)

Kural: "literatür şunu diyor" cümlesi, hangi dosyanın hangi örneklemden söylediği yazılmadan kurulmaz; hiçbir literatür sayısı projeye ölçülmeden alınmaz.

- **Literatür kendi içinde çelişiyor:**
  - koşu süresi medyan ~200 s ↔ 900–1000 s;
  - bit hızı 1–2 ↔ 2 Mb/s;
  - menzil 200–550 ↔ ~250 m.

  MobiHoc bildirilerinin %87,8'i güven aralığı raporlamamış.
- **Boşluk A** (K-081): değişen karıştırma şiddetinde AODV/OLSR'nin raporlanmış PDR ve gecikme düşüşü yok. Bu çalışma taban protokollerle ölçer; GPSR kapsam dışı olduğu için boşluk **kısmen** kapanır ve bu açıkça yazılır.
- **Doğruladıkları:**
  - soyutlama seviyesi SINR → PER → Bernoulli, parça başına;
  - kâhin yasağı ("karıştırıcı gücü, konumu, etki yarıçapı yalnız simülatörce bilinir");
  - "açık karıştırma" teriminin 11 protokolün 9'unda olmaması (dosya 17'nin matrisi);
  - ön-kayıt yönteminin ADEMP-PreReg (Siepe vd. 2024) ile örtüşmesi.
- **Uyarılar:**
  - literatürün kendi ödül formülü kâhin içeriyor (dosya 14 §5.7, §11.1); o kod kopyalanmaz;
  - "Table 26" iddiası yeniden doğrulanamadı (B7);
  - AODV'nin literatürdeki çöküş mekanizması (hareket → kopma → RREQ seli) statik kolda oluşmaz; statikte kopma yalnız karıştırmadan gelir;
  - kontrol kanalını hedefleyen karıştırma modellenmedi (kapsam dışı).
