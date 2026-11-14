# Protokol kaynakları — birincil belgeler

Taban protokollerin ve simülatörün dayandığı **birincil belgeler** ve uygulama kaynakları. Her belgenin künyesi, nereden alındığı, özeti (SHA-256) ve hangi denetimlerden geçtiği aşağıdadır. Doğrulanmış kaynakların listesi ve projedeki kullanımları `v2/02-DOGRULANMIS-KAYNAKLAR.md`de, rapor künyeleri `v2/16-KAYNAKCA.md`dedir. Güncel: 21 Ekim 2026.

**Kural:** bir belge buraya, gerçek olduğu ve içinde gömülü talimat benzeri bir metin ya da etkin içerik olmadığı denetlendikten sonra girer. Okunan kapsam (tamamı ya da kullanılan bölümler) kaynak başına `v2/02`de yazılır.

**Faz 4'ün rakipleri:** AOMDV (Marina & Das 2001) ve OLSR (RFC 3626) K-229'dan beri kıyas tabanı değildir; kopyaları ve denetimleri tarihçe ve eski regresyon vakaları için kalır.

**Dış kaynak olmayan klasör:** `literatur_taramasi_2026-08-31/` — ikinci el literatür taraması (20 dosya). İçindeki atıflar kullanılmadan önce birincil kaynaktan doğrulanır (`v2/02`). DESPARETE'nin v0.1 tasarım taslağı `arsiv/DESPARETE_TASARIM_PAKETI_v0.1_2026-09-22/`e taşındı (bayat; bağlayıcı olan kod).

---

## marina_das_2001_aomdv_icnp.pdf — AOMDV

| | |
|---|---|
| **künye** | M. K. Marina, S. R. Das, *"On-demand Multipath Distance Vector Routing in Ad Hoc Networks"*, Proceedings of the IEEE International Conference on Network Protocols (ICNP), s. 14–23, 2001 |
| **genişletilmiş dergi sürümü** | M. K. Marina, S. R. Das, *"Ad hoc on-demand multipath distance vector routing"*, Wireless Communications and Mobile Computing 6(7):969–988, Kasım 2006 · DOI 10.1002/wcm.432 (ücretli; künye Edinburgh Üniversitesi kurum sayfasından doğrulandı) |
| **alındığı yer** | `https://www3.cs.stonybrook.edu/~samir/Pubs/icnp-01.pdf` — ortak yazar Samir R. Das'ın kendi üniversite sayfası |
| **alınma tarihi** | 19 Eylül 2026 |
| **boyut · SHA-256** | 127 110 bayt · `e41c5df42170b723180867ba9a72d37ec7a4ca1923b0921503ed77a350f123e6` |

**Gerçeklik denetimi:**

- Dosya türü `application/pdf`, imza `%PDF-1.2` (2001 dönemine uygun)
- 10 sayfa — atıftaki *"s. 14–23"* ile tutarlı
- Başlık, yazarlar, yazarların 2001'deki kurumu (Cincinnati Üniversitesi),
  özet ve 35 maddelik kaynakça AOMDV hakkında bilinenlerle tutarlı
- Metin kaynakçayla bitiyor; sonrasında hiçbir şey yok

**Güvenlik denetimi (gömülü talimat ve etkin içerik taraması):**

- Metinde gömülü talimat kalıbı taraması: **eşleşme yok**
  (yalnız kaynakçadaki iki ns-2 ve IETF bağlantısı)
- PDF yapısında etkin içerik (`/JavaScript`, `/OpenAction`, `/Launch`,
  `/URI`, `/EmbeddedFile`, `/AA`): **sıfır**
- Görünmez metin (render kipi 3): **sıfır**

**Bilinen sınır:** makale 2001 dönemi dvips çıktısıdır; matematik simgeleri
**Type 3 bit eşlem yazı tiplerinde** (`/a0 … /a255`) ve metin olarak
çıkarılamıyor. Etkilenen kısımlar: Şekil 1 (AODV güncelleme kuralı), Şekil 3
(**AOMDV rota güncelleme kuralı**) ve bölüm 3.2'deki `k` değeri.

**Görsel olarak okundu (19 Eylül 2026):** PDF açılıp iki bölgenin ekran
görüntüsü alındı; ikisi de bu klasörde:

| dosya | içerik | SHA-256 |
|---|---|---|
| `marina_das_2001_sekil3_guncelleme_kurali.png` | Şekil 3 | `9e2878ce8527d9f4782e4f3c5c40c2ee51fafeebaac11de56632d8deffdaa950` |
| `marina_das_2001_k3_ve_sekil6.png` | Şekil 6 ve bölüm 3.2'nin `k` paragrafı | `f4c2b0b7c3cf5ef156a7e3aeed3ca6f86529071c4046713187c493d20032c08a` |

**Şekil 3 — AOMDV rota güncelleme kuralı**, birebir döküm. Düğüm *i*,
komşu *j*'den hedef *d* için bir rota ilanı (RREQ ya da RREP) aldığında:

```
if (seqnum_i^d < seqnum_j^d) then                                     (1)
    seqnum_i^d := seqnum_j^d                                          (2)
    if (i ≠ d) then                                                   (3)
        advertised_hopcount_i^d := ∞                                  (4)
        route_list_i^d := NULL                                        (5)
        insert (j, advertised_hopcount_j^d + 1) into route_list_i^d   (6)
    else                                                              (7)
        advertised_hopcount_i^d := 0                                  (8)
    endif
elseif (seqnum_i^d = seqnum_j^d) and
       ((advertised_hopcount_i^d, i) > (advertised_hopcount_j^d, j))  (9)
    insert (j, advertised_hopcount_j^d + 1) into route_list_i^d       (10)
endif
```

Karşılaştırma (9) sözlük sırasındadır. Makalenin kendi cümlesi: satır (1)
ile (9)–(10) döngüsüzlüğü sağlar; ispat ekte.

**Reklam edilen atlama sayısı** — düz yazıdan (bölüm 3.1): *i*'nin *d* için
ilan ettiği atlama sayısı, elindeki yolların atlama sayılarının **en
büyüğüdür** ve *i* *d* için bir ilan GÖNDERDİĞİNDE güncellenir. (Formül
metinde bozuk; tanım düz yazıda açık.)

**k = 3** — bölüm 3.2: hedef, *"benzersiz komşulardan gelen en fazla k RREQ
kopyasına, ilk atlamalarından bağımsız olarak"* cevap verir; *"deneylerimizde
k = 3 kullandık"*.

**Bu sürümde OLMAYANLAR:** ICNP makalesinin 3. bölümü `k` paragrafıyla
biter. Rota bakımı (bir yol kopunca ne yapılır, RERR), verinin hangi yoldan
gönderileceği ve yol başına zaman aşımları ayrı bir bölüm olarak YOK —
büyük olasılıkla dergi sürümünde (ücretli). ns-2.35'teki AOMDV kodu yazarların DEĞİL (Marcello Caleffi, 2008) —
boşluklar karar gereği (22 Eylül) makale + RFC 3561'den doldurulur,
belirtilmemiş seçimler `protokoller/aomdv.py` başlığında beyanlı
(`v2/02-DOGRULANMIS-KAYNAKLAR.md` §R4.1).

**Dağıtım:** yazarın kendi sayfasında yayımladığı kopyadır ve bu depoda
özel araştırma kullanımı içindir. Depo herkese açık yapılacaksa yeniden
dağıtım hakkı ayrıca denetlenmelidir.

---

## rfc3561_aodv.txt — AODV

| | |
|---|---|
| **künye** | C. Perkins, E. Belding-Royer, S. Das, *"Ad hoc On-Demand Distance Vector (AODV) Routing"*, RFC 3561, Temmuz 2003, kategori: Experimental |
| **alındığı yer** | `https://www.rfc-editor.org/rfc/rfc3561.txt` — RFC Editor, kanonik metin |
| **alınma tarihi** | 19 Eylül 2026 |
| **boyut · SHA-256** | 90 356 bayt · `b3294169ed3e0cf87c1acc1d99ac8b428eec279c563d64fb10cc1c902a60d579` |

## rfc3626_olsr.txt — OLSR

| | |
|---|---|
| **künye** | T. Clausen, P. Jacquet (ed.), *"Optimized Link State Routing Protocol (OLSR)"*, RFC 3626, Ekim 2003, kategori: Experimental |
| **alındığı yer** | `https://www.rfc-editor.org/rfc/rfc3626.txt` — RFC Editor, kanonik metin |
| **alınma tarihi** | 19 Eylül 2026 |
| **boyut · SHA-256** | 161 265 bayt · `722a7b5838ac29fe71aa48fa91ae619ab1ef8c128a754a84a98d705cefe17580` |

**İki RFC için denetim — ne yapıldığı TAM OLARAK:**

- Başlık, yazarlar, tarih, kategori ve sayfa sayısı (37 · 75) doğru.
- RFC 3626'nın boyutu (161 265), aynı gün tarayıcıda okunan metnin karakter
  sayısıyla BİREBİR aynı.
- Projede bugüne kadar alıntılanan cümleler indirilen metinlerde kelimesi
  kelimesine geçiyor: §6.9 *"Hello messages or otherwise"* · §6.11 *"have a
  non-empty precursor list"* · §18.9 *"MAXJITTER = HELLO_INTERVAL / 4"*.
- Tam metin taramasında gömülü talimat kalıbı: **yok**.

**Dürüst sınır:** RFC'lerin HER satırı okunmadı. Protokolle ilgili bölümler
okundu (AODV §5, §6, §10 · OLSR §3–§10, §13–§14, §18–§19) ve metnin tamamı
kalıp taramasından geçti. Kaynak RFC Editor'ün kendisi olduğu için risk
çok düşük; yine de "tamamı okundu" demek doğru olmazdı.

RFC metinleri IETF Trust'ın lisansıyla serbestçe dağıtılabilir.

---

## Gerçekçilik kaynakları — 25 Eylül 2026 (her biri ayrı; K-168, `v2/12` Faz 0)

Hepsi önce geçici alana indirildi, denetlendi, sonra buraya alındı. **Ortak denetim** (`pdftotext` ile metin + ham PDF taraması):
- etkin içerik (`/JavaScript`, `/Launch`, `/EmbeddedFile`, `/AA`, `/XFA` …) yok. İki arXiv dosyasında birer `/OpenAction` var; ikisi de yalnız `/GoTo … /Fit` (ilk sayfayı sığdırarak aç).
- gömülü talimat kalıbı yok. Tek eşleşme RFC 8966'da, protokol metni: *"receiver MUST ignore any TLV"*.

| dosya | künye | alındığı yer | boyut · SHA-256 | okunan |
|---|---|---|---|---|
| `pei_henderson_2009_ns3_80211b_dogrulama.pdf` | G. Pei, T. Henderson, *"Validation of ns-3 802.11b PHY model"*, Boeing Research & Technology, Mayıs 2009 (21 s.) | `https://www.nsnam.org/~pei/80211b.pdf` (ns-3 projesi) | 148 982 B · `74d87ea8c318a7b9e9de2315866b2a316977aeb5a2d00ff1231c593cdf288e80` | **tamamı** |
| `boer_1996_ieee80211_dsss_phy.pdf` | J. Boer, *"Direct Sequence Spread Spectrum Physical Layer Specification IEEE 802.11"*, doc. IEEE P802.11-96/49E, Mart 1996 (taslaktan parçalar içerir) | `https://grouper.ieee.org/groups/802/11/Tutorial/ds.pdf` (IEEE 802.11 çalışma grubu) | 56 148 B · `49d8af18f445144fb0152c52e6ceda642008bd2baed000b9f06f8c4624f7ff61` | **tamamı** |
| `rfc8966_babel.txt` | J. Chroboczek, D. Schinazi, *"The Babel Routing Protocol"*, RFC 8966, Ocak 2021, Standards Track | `https://www.rfc-editor.org/rfc/rfc8966.txt` | 141 512 B · `592fe69e208f6c3f1ac5d8e673eb309a9f6323a4c471de9284385c0005db1f2f` | §1–§4 ve Ek A–B tamamı (14 Ekim 2026, Babel'in gerçeklemesi, K-242); kalanı (güvenlik, IANA, Ek C–F) kalıp taramasında |
| `koubaa_2019_mavlink_survey.pdf` | A. Koubâa vd., *"Micro Air Vehicle Link (MAVLink) in a Nutshell: A Survey"*, arXiv:1906.10641v1, 2019 (9 s.) | `https://arxiv.org/pdf/1906.10641` | 856 711 B · `f0ffa9f95675e29280b6c87b2d07d82349c4646562d9cace6bcd85fa2cc0e41e` | başlık yapısı, mesaj boyları, yaşam sinyali, telemetri telsizleri tablosu; kalanı taramada |
| `pirayesh_zeng_2021_jamming_survey.pdf` | H. Pirayesh, H. Zeng, *"Jamming Attacks and Anti-Jamming Strategies in Wireless Networks: A Comprehensive Survey"*, arXiv:2101.00292v1, 2021 (16 s.) | `https://arxiv.org/pdf/2101.00292` | 1 827 418 B · `a1c943d03e52d7781d432e1d678894f2feda6e0b620e956bf2cf2fb5cfa193c9` | WLAN karıştırma saldırıları, hız uyarlaması/güç kontrolü ve karıştırma tespiti bölümleri; kalanı taramada |

**Projeye taşıdıkları** (ayrıntı `v2/02` · `v2/14`):
- **802.11b hata modeli** (Pei & Henderson): gürültü 22 MHz'de; Eb/N0 = SINR · 22/1 (1 Mb/s DBPSK) · SINR · 22/1/2 (2 Mb/s DQPSK) · CCK 5,5 ve 11 Mb/s için ·4 ve ·2. CMU ölçümleriyle (Prism 2.5) karşılaştırılmış.
- **Barker kodu:** kodlama kazancı 10,4 dB, *"girişime ve gürültüye karşı ~10 dB bastırma"* (Boer).
- **CCA:** modlar 1–3; ED eşiği verici gücüne bağlı (>100 mW −80 dBm · >50 mW −76 dBm · ≤50 mW −70 dBm); enerji sezme 15 µs.
- **Zamanlama ve alıcı:** slot 20 µs · Tx→Rx dönüşü 10 µs, Rx→Tx 5 µs · duyarlılık −80 dBm (FER 0,08, 1024 B) (Boer).
- **Babel:** uygulanabilirlik mesafesi (§2.4) ve sıra numaralı rotalar (§2.5–2.6) — DESPARETE'nin döngüsüzlük ailesi; README'deki atıf doğrulandı (`02` S6). Üçüncü rakip (K-242); gerçeklemesi `protokoller/babel.py`, hakemi babeld (aşağıda).
- **MAVLink:** mesaj 8–263 B (v1), yaşam sinyali ~1 Hz.
- **Karıştırma tespiti:** gürültü gücü, kanal meşgul oranı, çerçeveler arası süre, sinyal gücü ve teslim oranı birlikte kullanılıyor (Puñal vd., taramanın [83]'ü). Hız uyarlaması düşük güçlü girişimde etkili, yüksek güçlü sürekli karıştırmada etkisiz (Pelechrinis vd., [79]–[80]).

**Dağıtım:** arXiv ve ns-3 belgeleri yazarların herkese açık kopyalarıdır; depo herkese açık yapılacaksa yeniden dağıtım hakkı ayrıca denetlenmelidir. IEEE 802.11-2016'nın kendisi burada yok — yalnız IEEE GET programından, IEEE hesabıyla alınabilir.

### Elle indirilenler — 25 Eylül 2026 akşamı (denetlendi)

Aynı ortak denetim; geçici kopyalar üzerinde. Etkin içerik yok. İki yanlış alarm çözüldü: Goddemeier dosyasındaki `/JS` bir DOI'nin parçası (`…/JSAC.2012.120610`); NATO belgesindeki `/AA` sıkıştırılmış akışta rastgele bayt. Gömülü tek dosya IEEE'nin PDF üretim ayarı (`CMW_Acr8_V1.joboptions`). Talimat kalıbı yok; Al-Hourani'deki "disregard" teknik cümle (*"we can disregard hRX"*).

| dosya | künye | boyut · SHA-256 | okunan | not |
|---|---|---|---|---|
| `al_hourani_2014_optimal_lap_altitude.pdf` | A. Al-Hourani, S. Kandeepan, S. Lardner, *"Optimal LAP Altitude for Maximum Coverage"*, IEEE Wireless Communications Letters, 2014 (4 s.) | 667 334 B · `657c893e7840749967599974f4c19bd54d61323a8d2c14f2bacf49bb2bee40ee` | **tamamı** | yer–hava modeli: PL = FSPL + η; P(LoS, θ) = 1 / (1 + a·exp(−b[θ − a])); (η_LoS, η_NLoS) banliyö (0,1; 21) · kentsel (1,0; 20) · yoğun kentsel (1,6; 23) · yüksek yapılı (2,3; 34) dB; a, b Tablo I–II polinomlarından |
| `doodlelabs_rm2450_veri_sayfasi_2021.pdf` | Doodle Labs, *Smart Radio RM-2450 Datasheet* (2×2 MIMO Mesh Rider, 2 400–2 482 MHz), 20 Aralık 2021 (10 s.) | 354 100 B · `1c4a76b492e1eccf955f602a5bc5c6ab0c63b14f5fa45af665a826e8f47b178c` | **tamamı** | çıkış Pro 27 dBm · Xtreme 33 dBm (MCS 0) · ABD 4 W EIRP, **Avrupa 100 mW EIRP** · DC güç Tx ≤ 10,6 W (Pro) / 14 W (Xtreme), Rx 2 W, uyku 1,2 W · tümleşik GPS **1,5 m CEP** · duyarlılık OFDM MCS 0: 3 MHz −100, 5 MHz −98 dBm · 802.11b/g/n uyumlu |
| `goddemeier_daniel_wietfeld_2012_jsac_a2g.pdf` | N. Goddemeier, K. Daniel, C. Wietfeld, *"Role-Based Connectivity Management with Realistic Air-to-Ground Channels for Cooperative UAVs"*, IEEE JSAC 30(5):951–963, Haziran 2012 (13 s.) | 1 648 920 B · `1d80f6c8ae0dc45fe6335743d6a1e06cf3cd87ed70a4b432bf51485582c034a3` | kanal bölümü (V) | **istenen makale değil** (istenen: Goddemeier & Wietfeld, GLOBECOM Wi-UAV 2015, hava–hava Rice modeli). Hava–hava için "basit serbest uzay" varsayar; yer–hava için yüksekliğe bağlı yol kaybı üsteli. Kopyada *"Authorized licensed use limited to: Universitaetsbibliothek der RWTH Aachen"* damgası var — yalnız araştırma kopyası, yeniden dağıtılmaz |

**Depoya alınmayanlar:**
- **NATO SPCoE kitabı:** Yzb. (TUR GEND) Yüksel Kütük, *"UAS (Unmanned Aircraft Systems): The Force Multiplier for Law Enforcement Agencies and the Potential Contributor to Stability Policing"*, NATO SPCoE, 2025, ISBN 979-12-5539-066-4. Kaynak: `https://nllp.jallc.nato.int/iks/sharing%20public/uas-unmanned-aircraft-systems.pdf`. 3 639 808 B · `160b3e547ccddb228f6a24b1f87c94b97ed386291428e6a55bfca0f7bd6404e3` (63 s.). Yalnız §1.4.3 okundu: NATO sınıflandırması, NATO ATP-3.3.8.1 Ed. B v1, 2019'dan — **Sınıf I "küçük" (>15 kg): taktik birlik, ≤ 5 000 ft AGL, görev yarıçapı 50 km (görüş hattı), ör. ScanEagle**. Web okuması sırasında kaydedildi. Yayıncının izinsiz elektronik saklama yasağı nedeniyle kopyası depoya alınmadı.
### Ücretli iki kaynağın açık alternatifleri — 25 Eylül 2026 gecesi

Ortak denetim; etkin içerik yok (1801.01656'daki `/JS` sıkıştırılmış akışta rastgele bayt, `/OpenAction` yalnız `/GoTo … /Fit`), talimat kalıbı yok.

| dosya | künye | alındığı yer | boyut · SHA-256 | okunan · sağladığı |
|---|---|---|---|---|
| `khuwaja_2018_uav_kanal_taramasi.pdf` | A. A. Khuwaja, Y. Chen, N. Zhao, M.-S. Alouini, P. Dobbins, *"A Survey of Channel Modeling for UAV Communications"*, arXiv:1801.07359v1, 2018 (IEEE COMST 2018'in açık sürümü; 35 s.) | `https://arxiv.org/pdf/1801.07359` | 354 043 B · `20640418d222600b0e8aa453fbafea86ca745940e6eef81255ca48a0dc1279f3` | hava–hava bölümü, Tablo I–II, küçük ölçekli sönümleme · **hava–hava yol kaybı üsteli 1,92 · 0,93 · 2,05 (802.15.4), 2,6 (Goddemeier & Wietfeld 2015, 802.11, 2,4 GHz, Pt 20 dBm, 5 dBi), 2,03 (802.11a)**; hava–hava Rician K "yüksekliğe bağlı", sayı vermiyor |
| `khawaja_2019_uav_yer_hava_kanal_taramasi.pdf` | W. Khawaja, I. Guvenc, D. W. Matolak, U.-C. Fiebig, N. Schneckenburger, *"A Survey of Air-to-Ground Propagation Channel Modeling for Unmanned Aerial Vehicles"*, arXiv:1801.01656v1, 2018 (IEEE COMST 2019'un açık sürümü; 25 s.) | `https://arxiv.org/pdf/1801.01656` | 2 997 614 B · `be0292197ac77cd80655aae84f5eb0ba589a172aa59fc0ac2f126a4a0fc23fb3` | §C "Ricean K-factor" ve özet tablosu · **K: alçak irtifa yer–hava 2–5 dB, (−5)–10 dB, ağaçlıkta 2–10 dB; güçlü görüş hattında ortalama L bandı ~12 dB, C bandı 27,4–31,3 dB** |

**Uygulama kaynakları** (`uygulama_kaynaklari/`, GPL-2.0-only — dosya başlarındaki lisans korunur): standardı uygulayan açık kodlar. Standardın kendisi değil; kayıtta **"uygulama kaynağı"** diye işaretlenir. İkisi bağımsızdır, aynı değerlerde birleşir. `gitlab.com/nsnam/ns-3-dev` (master, 25 Eylül 2026) ve `github.com/torvalds/linux` (master, 25 Eylül 2026):

| dosya | sağladığı (dosyadaki standart atfıyla) | SHA-256 |
|---|---|---|
| `ns-3/wifi-standard-constants.h` | DSSS SIFS **10 µs**, slot **20 µs** (*"Table 16-4 HR/DSSS PHY characteristics of 802.11-2020"*) · RTS eşiği varsayılanı en büyük değer (*"C.3 MIB detail in IEEE Std 802.11-2020"*) | `87c6e3c6391fa0c7cbe849e2d2d36f73f8637465208a15abc9c0a97a639baf18` |
| `ns-3/wifi-remote-station-manager.cc` | kısa yeniden deneme sınırı (MaxSsrc) **7**, uzun (MaxSlrc) **4** | `858fae5df7f0fe04c662cf1311403ea50af73e584d37c02e7f09ee8c412ad705` |
| `ns-3/wifi-mac.cc` | 802.11b CWmin **31**, CWmax **1023** | `4c42711c92e315e549f8c4c488b1ea73e0433beea284750284320949ac1dbff9` |
| `ns-3/wifi-phy.cc` | 802.11b yapılandırması (SIFS, slot, PIFS = SIFS + slot) | `27425b912e3dd322ea35b8d24082548c91683f6282492ae8ef6ee8a773b5c924` |
| `ns-3/dsss-phy.cc` | 1 / 2 / 5,5 / 11 Mb/s · uzun önbelge 144 µs + başlık 48 µs (kısa: 72 + 24 µs) | `d5239ede9c5793808db4541beebf62602dc1d2227bf2cb2355b89bc6053f196d` |
| `ns-3/dsss-error-rate-model.cc` | G1'in (Pei & Henderson) BER formüllerinin güncel kodu · CCK 5,5/11 Mb/s: Pursley–Royster sembol hatası (GSL sürümü) — A4'ün hata modeli | `e7274c4a98eb7be8e5732f4b4ce51cbadcf8a9ea3f777777a903dca86659f66f` |
| `ns-3/arf-wifi-manager.cc` · `.h` | ARF hız uyarlaması (Kamerman & Monteban 1997'ye atıflı; zaman sayacı yerine paket sayacı): en düşük hızdan başla · **10** art arda başarı ya da **15** iletimlik sayaç → bir hız yukarı ve kurtarma kipi · kurtarmada ilk başarısızlık, normalde art arda **2** başarısızlık → bir hız aşağı. 26 Eylül 2026 indirildi (8 353 B + 2 621 B), tamamı okundu | `723572f3502109ca4cf8d17950ddae78a1f74c6f297d60af7e7c614704fa86c0` · `d52e373873f0b29676f37621c0d85d2c18605b1cb98ea85ee687c9eb6e811d78` |
| `ns-3/aodv-routing-protocol.cc` · `aodv-rqueue.cc` · `.h` | AODV rota tamponu: `MaxQueueLen` **64**, `MaxQueueTime` **30 s**; kuyruk dolunca *"Drop the most aged packet"*, süresi dolan `Purge`da düşer. Başlık: *"Based on NS-2 AODV model developed by the CMU/MONARCH group and optimized and tuned by Samir Das and Mahesh Marina"*. 28 Eylül 2026 indirildi (86 436 B · 3 405 B · 6 649 B), ilgili kısımlar okundu — `rota_tamponu_*` köken kaydı (K-198) | `104dbf6352b70949a114f4db3d3e21c6deb176082cc0b3138ff8025848eeb6b0` · `c66643b64d8131f9194f26b8192752f6c1923399a3f534a3ed7beec45a3aa678` · `d9651df51f082472bab64752617d2939d24cc3b09d8945e81f7e764e80a7eb1e` |
| `ns-3/wifi-mac-header.cc` | çerçeve başlık boyları: veri **2 + 2 + 6 + 6 + 6 + 2 = 24 B**, onay (ACK) **2 + 2 + 6 = 10 B** (FCS hariç; FCS **4 B** `wifi-standard-constants.h`de `WIFI_MAC_FCS_LENGTH`) → onay çerçevesi 14 B. 30 Eylül 2026 (K-203), 29 777 B, `GetSize` okundu | `cbe9061a40a65ae4467a7df8cbfa44f95c05125e8f7d68ef6dfc3d45cfc13f6e` |
| `ns-3/llc-snap-header.cc` | LLC/SNAP başlığı `LLC_SNAP_HEADER_LENGTH` (değeri RFC 1042: 8 oktet). 30 Eylül, 1 767 B, tamamı | `6a89e53e5b3bce433056a72a45d1c65226d2847f6a8a008a3c7a542a47ae93cd` |
| `ns-3/wifi-mac-queue.cc` | MAC kuyruğu varsayılanı **`MaxSize` 500 paket · `MaxDelay` 500 ms** (bizde 50 paket, süre sınırı yok — NS-2 `ifqlen` geleneği; değer farklı → duyarlılık ölçülür, Faz 4.4). 30 Eylül, 15 544 B, öznitelikler okundu | `dc5c27e1343510d027ae01bc90aef4d267ff0c81ff963df1f2270b53b68ca2f0` |
| `ns-3/simple-frame-capture-model.cc` · `frame-capture-model.cc` | yakalama: yeni çerçeve süren çerçeveden **5 dB** güçlüyse ve önbelge sezildikten sonraki **16 µs**'lik pencerede ise alım yeni çerçeveye geçer (bizde 10 dB · 192 µs; model ayrıntısı farklı → duyarlılık ölçülür, Faz 4.4). 30 Eylül, 1 823 B · 1 046 B, tamamı | `06a33f211d82f2c271cfb0bc82ab78e63156ae43ce5d94e79c0ba6b46e95c170` · `17909434a659c3899420bedc2fce4f6bf22c52d3f7791fca24bdd732caae0573` |
| `linux/net_wireless_core.c` | *"Initialize wiphy parameters to IEEE 802.11 MIB default values"*: `retry_short = 7`, `retry_long = 4`, RTS kapalı | `a1e6ebc52f7634585e5c7e8cb29b2e106de5af12da68cf9e5ed0794ad94fcb9a` |
| `ns-3/wifi-utils.h` | yardımcı bildirimler (ACK boyu "FCS dâhil" hesaplanır). 30 Eylül, 8 584 B, taramada | `76454b3f2d9f0de839c8fb838a6bf3cdc1e0ad621ae11372cdb8a52e623720b2` |

30 Eylül'de indirilen `wifi-mac-trailer.h` FCS sabitini taşımadığı için `arsiv/kaynak_elenen/`e taşındı (sabit zaten `wifi-standard-constants.h`de). Denetim: talimat kalıbı yok; dosyalar GPL-2.0-only başlığını taşıyor.

### RFC'ler — kontrol kapsüllemesi (30 Eylül 2026, K-203)

| dosya | künye | alındığı yer | boyut · SHA-256 | okunan |
|---|---|---|---|---|
| `rfc791.txt` | J. Postel, *"Internet Protocol"*, RFC 791, Eylül 1981 | `https://www.rfc-editor.org/rfc/rfc791.txt` | 94 892 B · `6cfb387fcecfc1b72f2f69343c5b6951b5d263d708162e2b5c66ab8f394f6265` | §3.1 başlık biçimi: IHL en az 5 × 32 bit → **20 oktet** |
| `rfc768.txt` | J. Postel, *"User Datagram Protocol"*, RFC 768, Ağustos 1980 | `https://www.rfc-editor.org/rfc/rfc768.txt` | 5 896 B · `7dc8880e1ecef9c3f9da0db4b876a16e96bfa4f0953cc9d977d414f8f680c2f0` | tamamı: başlık kaynak/hedef kapısı, uzunluk, sağlama — **8 oktet** |
| `rfc1042.txt` | J. Postel, J. Reynolds, *"A Standard for the Transmission of IP Datagrams over IEEE 802 Networks"*, RFC 1042, Şubat 1988 | `https://www.rfc-editor.org/rfc/rfc1042.txt` | 34 359 B · `e8737abe7f7b80ae2e84b8cada0ea02d8cc3c4ad2414e902cc055e6953a01c55` | başlık bölümü: *"The total length of the LLC Header and the SNAP header is 8-octets"* |

### RFC 1700 ve ns-3 IPv4 — veri paketinin varsayılan TTL'i (6 Ekim 2026, K-215)

| dosya | künye | alındığı yer | boyut · SHA-256 | okunan |
|---|---|---|---|---|
| `rfc1700_assigned_numbers.txt` | J. Reynolds, J. Postel, *"Assigned Numbers"*, RFC 1700 (STD 2), Ekim 1994 — RFC 3232 (2002) ile tarihsel; kayıtlar IANA'nın çevrimiçi veritabanına taşındı | `https://www.rfc-editor.org/rfc/rfc1700.txt` | 458 860 B · `77de0532a5b4b6bef3d233795b5a87aae1838358b98e7da82676e0c6455eb03e` | "IP TIME TO LIVE PARAMETER": *"The current recommended default time to live (TTL) for the Internet Protocol (IP) [45,105] is 64."* |
| `uygulama_kaynaklari/ns-3/ipv4-l3-protocol.cc` | ns-3-dev `src/internet/model/ipv4-l3-protocol.cc` (GPL-2.0-only) | `https://gitlab.com/nsnam/ns-3-dev/-/raw/master/src/internet/model/ipv4-l3-protocol.cc` | 58 517 B · `faa5c2a9c5fdb800fda076bab33cb42b8b5dec5b208d46cd10a13d10e5b146ef` | öznitelik `DefaultTtl`: *"The TTL value set by default on all outgoing packets generated on this node"*, **64** |

Denetim: talimat kalıbı yok (RFC 1700'deki "Claude" geçişleri kayıt sahibi adları).

### Linux ath9k — sürücünün gürültü tabanı raporu (10 Ekim 2026, Faz 5.1 önkoşulu, denetim D-04)

`uygulama_kaynaklari/linux/ath9k/` — Linux v6.6 (LTS) etiketi, `https://raw.githubusercontent.com/torvalds/linux/v6.6/drivers/net/wireless/ath/ath9k/<dosya>`. Lisans **ISC** (Atheros Communications / Qualcomm Atheros; dosya başlıklarında), GPL değil. Atheros 802.11a/b/g/n yonga ailesinin açık sürücüsü; gerçek bir telsizin protokole verebileceği gürültü bilgisinin örneği (standart değil, uygulama kaynağı). Denetim: talimat kalıbı yok.

| dosya | sağladığı | boyut · SHA-256 |
|---|---|---|
| `calib.c` | gürültü tabanı (NF) işleme: her okuma çipin sınırlarına kırpılır (`ath9k_hw_nf_sanitize`: üstte **max**, altta nominale) · son **5** okumanın ortancası (`ath9k_hw_get_nf_hist_mid`) · ortanca da **max**'a kırpılır (çip "takılı beacon" girişim kipinde değilse) · bildirilen gürültü `ath9k_hw_getchan_noise`: **−95 dBm + max(0, NF − 6 − nominal)**, tamsayı | 12 936 B · `f4ae3ffbada0ea19a19cd88dec90ab592fb793fcd16bbabfbf1dbc6aba9674e6` |
| `calib.h` | `ATH9K_NF_CAL_HIST_MAX` **5** · `ATH9K_NF_CAL_NOISE_THRESH` **6** | 3 619 B · `f4316b58727cb50f7ce6d7c2ad827700a899cb329857c0d44b0e9f5e69d2121d` |
| `hw.h` | `ATH_DEFAULT_NOISE_FLOOR` **−95** · `struct ath_nf_limits` (max · min · nominal) | 36 270 B · `e8d59af29f0e60ecdf59c4e02b81b42e61794bbcd718ca8ce68b9b34b556808c` |
| `ath9k.h` | kalibrasyon aralıkları: uzun **30 s** (`ATH_LONG_CALINTERVAL`), girişim kipinde **1 s** (`_INT`); kısa 1 s (istasyon) · 100 ms (erişim noktası) | 31 766 B · `253bd71ae31a4867529dfb40c0a0aff174402151aaa0e34e1076593000d6cd4e` |
| `link.c` | `ath_ani_calibrate`: uzun kalibrasyon zamanlayıcısı; girişim bayrağı (`NFCAL_INTF`) varken 1 s | 14 315 B · `5c4d3a73da811688fd2762d758147a278d1df41fa642beb4306324e23f334a48` |
| `ar9003_calib.c` | *"Do NF cal only at longer intervals"*: NF yalnız uzun kalibrasyonda okunur | 47 135 B · `84421fd00033bd692ea0626dd489e877ba895d0c5b834e270e49fdb21b4ef034` |
| `ar9003_phy.c` · `ar9003_phy.h` | AR9300 sınırları, 2 GHz: nominal **−110** · min −125 · max **−60** (iç ölçek) | 62 977 B · `f7b1dd55d778578726128536bc2744f3058e9e7aa45908eb0b94ba275ecfc7b9` · 59 573 B · `52ad4dbd3d8b317ee0f397a5d541858f23e9203634c335e08892464767671f66` |
| `ar9002_phy.c` · `ar9002_phy.h` | AR9280 sınırları, 2 GHz: nominal **−112** · min −127 · max **−97**; AR5416 −90 · −100 · −80 | 17 430 B · `a4fe2b040163d5700607657d9c14d200d046b90ca20a39eeda1c0ba6838abe5b` · 23 901 B · `d2cceaa4340087d8bd961f9704d4361d9e22e737d038076294f1b172deb8f5fd` |

Sonuç: bildirilen gürültü ısıl tabanın üstündeki artışı yalnız nominalin 6 dB üstünden itibaren, çipe göre en çok +44 dB (AR9300) ya da +9 dB (AR9280) gösterir ve olağan kipte 30 s'de bir okunan 5 ölçümün ortancasıdır.

- **`arsiv/kaynak_elenen/ieee_80211_2016_kesit_madde21_IPR2023-01414.pdf`:** IEEE Std 802.11-2016'nın yalnız 9 sayfası, madde 21 (VHT/802.11ac, s. 2538–2580). Bir ABD patent davasının delil dosyası (*"IPR2023-01414 · Patent Owner · EX 2003"*), üçüncü kişinin lisans damgasıyla. İhtiyaç duyulan 802.11b maddeleri (15–16) ve MAC zamanlaması (madde 10) yok → kaynak olarak kullanılmadı, arşive taşındı.

### OLSRv2 · DSR · JarmRout — yeni rakiplerin kaynakları (11 Ekim 2026, K-229 · K-230)

İndirme yürütücünün izniyle. RFC'ler rfc-editor.org'un kanonik metinleri; RFC 7181 ve 6130'u güncelleyen dört RFC (7183 · 7187 · 7188 · 7466) davranışı etkileyebileceği için alındı; RFC 5444'ün güncellemeleri (7631 · 8245) yalnız adlandırma ve tasarım kuralı olduğu için alınmadı. Denetim: talimat kalıbı yok.

| dosya | künye | alındığı yer | boyut · SHA-256 | sağladığı |
|---|---|---|---|---|
| `rfc7181_olsrv2.txt` | T. Clausen, C. Dearlove, P. Jacquet, U. Herberg, *"The Optimized Link State Routing Protocol Version 2"*, RFC 7181, Nisan 2014, Standards Track | `https://www.rfc-editor.org/rfc/rfc7181.txt` | 253 538 B · `a5eaa55facce5496a0aabf1dc583fc69d831b93c95bba56114922ebd40a197fc` | OLSRv2'nin kendisi: MPR (yayın ve rota ayrı), TC, rota hesabı, bağ metriği çerçevesi (metrik tanımlamaz), parametreler §5 |
| `rfc6130_nhdp.txt` | T. Clausen, C. Dearlove, J. Dean, *"Mobile Ad Hoc Network (MANET) Neighborhood Discovery Protocol (NHDP)"*, RFC 6130, Nisan 2011 | `https://www.rfc-editor.org/rfc/rfc6130.txt` | 190 678 B · `7555e7aaafdccd36088082e798ab87deda5fa772e72b287979788165246c473a` | komşuluk keşfi (HELLO), bağ durumu, 2-atlama komşuluğu; OLSRv2'nin altındaki katman |
| `rfc5444_paket_bicimi.txt` | T. Clausen, C. Dearlove, J. Dean, C. Adjih, *"Generalized Mobile Ad Hoc Network (MANET) Packet/Message Format"*, RFC 5444, Şubat 2009 | `https://www.rfc-editor.org/rfc/rfc5444.txt` | 139 048 B · `07097bf766b0197c4b8f110bba3cd90d3d8319a8869f0f1a9ccafc15b73639cd` | paket/mesaj/TLV biçimi — kontrol mesajlarının bayt boyu buradan |
| `rfc5497_zaman_tlv.txt` | T. Clausen, C. Dearlove, *"Representing Multi-Value Time in MANETs"*, RFC 5497, Mart 2009 | `https://www.rfc-editor.org/rfc/rfc5497.txt` | 30 653 B · `5c4d63d8029095106a7f2dba09531287688efeb2623e341231f5510b779d52c6` | VALIDITY_TIME · INTERVAL_TIME TLV'lerinin 8 bitlik kodlaması |
| `rfc5148_titresim.txt` | T. Clausen, C. Dearlove, B. Adamson, *"Jitter Considerations in MANETs"*, RFC 5148, Şubat 2008 | `https://www.rfc-editor.org/rfc/rfc5148.txt` | 26 379 B · `d09c66dd0060a5684cb639d2c9fc257ed8cb4d7314fc0182c30d9767b5afd36a` | kontrol mesajı titreşimi (MAXJITTER) |
| `rfc7779_dat_metrigi.txt` | H. Rogge, E. Baccelli, *"Directional Airtime Metric Based on Packet Sequence Numbers for OLSRv2"*, RFC 7779, Nisan 2016, Experimental | `https://www.rfc-editor.org/rfc/rfc7779.txt` | 43 953 B · `055d0d84633fbe88f7105d1cf2320ac3f6b083cd672f7e60ce66c61a029632a9` | OLSRv2'nin bağ metriği (DAT): paket sıra numarasından kayıp, hızla yayın süresi |
| `rfc7183_butunluk.txt` | U. Herberg, C. Dearlove, T. Clausen, *"Integrity Protection for NHDP and OLSRv2"*, RFC 7183, Nisan 2014 | `https://www.rfc-editor.org/rfc/rfc7183.txt` | 32 730 B · `8279d878ba11726d4b1fd9ff770a2d1ca70234568b8764d20da6f80cd8761534` | 7181 · 6130'u günceller: bütünlük koruması (ICV TLV) — güvenlik, kapsam dışı (beyan) |
| `rfc7187_rota_mpr.txt` | C. Dearlove, T. Clausen, *"Routing Multipoint Relay Optimization for OLSRv2"*, RFC 7187, Nisan 2014 | `https://www.rfc-editor.org/rfc/rfc7187.txt` | 9 341 B · `9b9b16cbd310432bd512a13d9919a5b3d5a815dd749ce90c1b88a73d95098264` | 7181'i günceller: rota MPR'si seçimi |
| `rfc7188_uzanti_tlv.txt` | C. Dearlove, T. Clausen, *"OLSRv2 and NHDP Extension TLVs"*, RFC 7188, Nisan 2014 | `https://www.rfc-editor.org/rfc/rfc7188.txt` | 36 174 B · `d2f5239548f6b2b1c03d70f594029a39d3e105b5177f696666d492815f79b97e` | 7181 · 6130'u günceller: TLV genişletmeleri |
| `rfc7466_nhdp_iyilestirme.txt` | C. Dearlove, T. Clausen, *"An Optimization for the MANET Neighborhood Discovery Protocol (NHDP)"*, RFC 7466, Mart 2015 | `https://www.rfc-editor.org/rfc/rfc7466.txt` | 17 949 B · `b6375b33eaf5642a1448ed0e176e9d87b65a38e47ee9b979944e628db97e945e` | 6130'u (dolayısıyla 7181'i) günceller: 2-atlama kümesinin bakımı |
| `rfc4728_dsr.txt` | D. Johnson, Y. Hu, D. Maltz, *"The Dynamic Source Routing Protocol (DSR) for Mobile Ad Hoc Networks for IPv4"*, RFC 4728, Şubat 2007, Experimental | `https://www.rfc-editor.org/rfc/rfc4728.txt` | 265 706 B · `e848d726866f3ec6b1b67c80f2e97a211ab97d469454b63036d200a28b993abd` | JarmRout'un temeli: rota keşfi, kaynak rotası başlığı, rota hatası — makalenin sustuğu yerde hakem |
| `pu_2018_jarmrout_ieee_access.pdf` | C. Pu, *"Jamming-Resilient Multipath Routing Protocol for Flying Ad Hoc Networks"*, IEEE Access 6:68472–68486, 2018, DOI 10.1109/ACCESS.2018.2879758 (açık erişim; IEEE Xplore 8523684) | `https://congpu.github.io/document/paper/ieee_access_2018.pdf` (yazarın sayfası; yayıncı sürümüyle aynı) | 6 504 878 B · `828f08118160d8544761e93e5061464367a16d582a01417a1d980e1fbfa446a8` | §III bağ kalitesi (RSSI varyansı, Eş. 1–5) · trafik yükü (NAV + kuyruk, Eş. 6–8) · mekânsal uzaklık (Eş. 9–12) · çift önceliği (Eş. 13; ağırlıklar 0,2 · 0,2 · 0,6) · Şekil 4 sözde kod · §VI.B: aynı veri paketi iki yoldan gönderilir. Tablo 4 (yayıncı sayfasında görüntü, okundu): 1000 × 1000 m², 50–100 düğüm, 30 m/s rastgele yol noktası, menzil 300 m, karıştırıcı 1–6, kanal hata oranı %10, 2 Mb/s, 1–3 pkt/s × 512 B, 3 000 s. **Protokolün iç parametreleri (Eş. 6–8'in filtre sabitleri, RSSI örnek sayısı, hedefin bekleme süresi `t_wait`) makalede yok.** |

**Uygulama kaynağı — olsrd2 (OONF)** (`uygulama_kaynaklari/olsrd2/`, BSD-3 — `LICENSE`): olsr.org'un OLSRv2 başvuru gerçeklemesi, `github.com/OLSR/OONF` commit `477e716110ee210f9ce03a75ecacd55a06fd600f` (6 Ağustos 2026). NHDP, MPR seçimi, OLSRv2 (TC, rota) ve DAT metriği dosyaları; RFC'nin sustuğu yerde hakem (AODV'de ns-3'ün rolü).

| dosya | boyut · SHA-256 |
|---|---|
| `include/oonf/nhdp/ff_dat_metric/ff_dat_metric.h` | 2 536 B · `69b44b938dd2fc8a8bdb202c62a92e3bc4c39b7572feed0146624d9b0189a120` |
| `include/oonf/nhdp/mpr/neighbor-graph.h` | 4 552 B · `ad8b5b51a9e44f4b12f2850109851024924fcb12acf6ac766f4043e508c35093` |
| `include/oonf/nhdp/nhdp/nhdp.h` | 3 433 B · `3bb73d0bdd478ba73f75c239ae0cc14cc9b8ce7f293883af35498e35d0768133` |
| `include/oonf/nhdp/nhdp/nhdp_db.h` | 17 830 B · `d3e418b9efede4a41c138b82e625bb0ab5ed3ac7a46700b19b6b2b3b4d3922bb` |
| `include/oonf/nhdp/nhdp/nhdp_domain.h` | 13 666 B · `a0bf69bb7502b9d1f054ce7d64a12cf8e8b53776191d73f8c2680e285fff60e4` |
| `include/oonf/nhdp/nhdp/nhdp_interfaces.h` | 10 587 B · `50e15e79af6e6ad75a1d7d5669eb0a142fa5db3036824833616929cfbe3d6a46` |
| `include/oonf/olsrv2/olsrv2/olsrv2.h` | 3 536 B · `047bef8a5ef0d78b36ba44941149b04e244339e8f3f967168f7daa83924056ad` |
| `include/oonf/olsrv2/olsrv2/olsrv2_routing.h` | 6 757 B · `2d62e808483bee79cb22ca4720ddb75c76f398663badc423e631266ae1826c52` |
| `include/oonf/olsrv2/olsrv2/olsrv2_tc.h` | 8 054 B · `7368459d075676a9b95eee5d19403b98ccb2641838edf6047e12d4063d43a19a` |
| `LICENSE` | 1 750 B · `0d77f73d23a4fabcda9d32429ba28040f1259fe2575dbd9b21be16906ea83e9d` |
| `src/nhdp/ff_dat_metric/ff_dat_metric.c` | 38 794 B · `680d29d97e108bdaf70bafaa8b9186f73b8571679d96ab47e927140253674793` |
| `src/nhdp/mpr/mpr.c` | 9 324 B · `5ec9f571a4d47cdd4e719c30f43adb1771527e797c006a6449f83681982f10ee` |
| `src/nhdp/mpr/neighbor-graph-flooding.c` | 10 243 B · `c013bdbf28844a9a150a8971cb6ec16b11cf6febfb7f1f33471a6115f7339d9b` |
| `src/nhdp/mpr/neighbor-graph-routing.c` | 11 777 B · `ca135bdf6dc322aef76db1d2d70faa431cdb6cc30178f5cc204e2ed1d1a1a0e7` |
| `src/nhdp/mpr/neighbor-graph.c` | 9 169 B · `bb3c2f6e9828a90457a568dca82833ad165347bccab7f7637a109d246b910a85` |
| `src/nhdp/mpr/selection-rfc7181.c` | 14 951 B · `d999a1991c908b8872877f07817e21b8e378364a41088df8ddc06e6e8a9c2bd1` |
| `src/nhdp/nhdp/nhdp.c` | 14 942 B · `d62dc938844a35795b7ea953eabafd7bf0da843cd83b30f11cdb2fd348a35ef7` |
| `src/nhdp/nhdp/nhdp_db.c` | 30 092 B · `68a7d255b62ba3f2bb4ee325bd15c332ba547147e093d1a426a765f97dfa4951` |
| `src/nhdp/nhdp/nhdp_domain.c` | 40 672 B · `6a30f09a88ddeab1c44182b902af44f5503eaf54129e6b7061c36cc7369a386c` |
| `src/nhdp/nhdp/nhdp_hysteresis.c` | 4 250 B · `56ce0f9f02847d826acc142d02ec4281d9b6f48a2fcc60fab71fc0f032d8010c` |
| `src/nhdp/nhdp/nhdp_interfaces.c` | 18 808 B · `1e2398a403ee50d5e39adb44f8a6598f90bdcd7aa9186aaea3390f6a74af2f2c` |
| `src/nhdp/nhdp/nhdp_reader.c` | 33 064 B · `acd880f2cf3969d37624d3898085d57ef882f20aa16e170140b0f2ba9810a9d1` |
| `src/nhdp/nhdp/nhdp_writer.c` | 19 055 B · `796aa8d6ebe6aa9acbeea4f71fa76892abd05da0b910ae5a360e19d6b559d0e3` |
| `src/olsrv2/olsrv2/olsrv2.c` | 22 144 B · `65ddf86b834ca15613278aedabadbdbd2875267d20b78d4dd328bcc53718af93` |
| `src/olsrv2/olsrv2/olsrv2_originator.c` | 7 920 B · `e7514fca9c63b9134fada77a21ae772178acd6f67d6216cca17320b56b04c5cc` |
| `src/olsrv2/olsrv2/olsrv2_reader.c` | 19 815 B · `140cd57491cf2f85398fd286ae70cfeaa8d7be677f9e7d422e95a45843e7d4ae` |
| `src/olsrv2/olsrv2/olsrv2_routing.c` | 38 260 B · `595859cb7a4f0bd4d178f74ddf08a9a9230f5936c537691d205a0ed75f78cbc8` |
| `src/olsrv2/olsrv2/olsrv2_tc.c` | 15 877 B · `e95fe36ba8e97a5784b043710f623d3bca9a92ddf69cb6e5add84a49059e91b6` |
| `src/olsrv2/olsrv2/olsrv2_writer.c` | 19 635 B · `23484f9a3c0f219035e91fd1561fde649baa0c9489991547b1c3ab8ca7a5c3c2` |

### Babel — üçüncü rakibin hakemi (14 Ekim 2026, K-242 · K-244)

**Uygulama kaynağı — babeld** (`uygulama_kaynaklari/babeld/`, MIT — `LICENCE`): RFC 8966'nın yazarı J. Chroboczek'in Babel başvuru gerçeklemesi, sürüm **1.14** (20 Haziran 2026; `CHANGES`). `https://github.com/jech/babeld/archive/refs/tags/babeld-1.14.tar.gz`, 14 Ekim 2026 indirildi (yürütücünün izniyle), arşiv 109 976 B · `fe7e2df4f29e2da4eba511492fe62b405e5ac75d2048d1df69c52f6cc78218ff`. Arşivden yalnız protokol mantığının dosyaları alındı (yapılandırma ayrıştırıcısı, HMAC, BSD çekirdek arayüzü, testler alınmadı). Gömülü talimat kalıbı taraması temiz. RFC'nin seçeneğe ya da MAY'e bıraktığı yerde hakem (AODV'de ns-3, OLSRv2'de olsrd2'nin rolü); seçimler `protokoller/babel_bicim.py`nin beyan tablosunda.

Okunanlar: `neighbour.c` (Hello geçmişi, rxcost, maliyet, IHU süresi) · `route.c` (uygulanabilirlik, seçim, düzgünleştirme, tetiklenen güncelleme, kayıp, süre dolumu) · `message.c` (TLV ayrıştırma, istek işleme, Hello/IHU gönderimi, joker istek) · `resend.c` (yinelemeler, istek listesi) · `interface.c` · `babeld.c` (açılış, varsayılanlar) · `util.c/.h` (sıra aritmetiği, titreşim) · `kernel_netlink.c` (∞ rotanın "unreachable" kurulması). Öteki dosyalar bildirimler için.

| dosya | boyut · SHA-256 |
|---|---|
| `LICENCE` | 1 072 B · `b415c41292cedef6c97b243609e50552887c29343566c639f23282d31efd2afd` |
| `README` | 3 310 B · `827deaa14ba1f05cf0a8ca459c795e6dd1445e50ee4530b5e34083741718603c` |
| `babeld.c` | 31 190 B · `e882ea247006d2129ecfb6309d3eb861a72a7e6b75a2543565b1a03b66565638` |
| `babeld.h` | 3 358 B · `594129afefeb87493f6600a1801838186b19d9793406501c904ef59f41929911` |
| `interface.c` | 17 639 B · `3eaf449c2d5606a3c8d3955699a09372fb3477d39e2906a652807f75cd08d434` |
| `interface.h` | 5 287 B · `7aceee9f083162fd7df5941324369624ad702eb2886a6403ffa2c6d1e894c244` |
| `kernel.h` | 3 626 B · `8c3a1ed32ae5abc3ac0c02845b80a387d807008ad00bf3b49083316b4e480009` |
| `kernel_netlink.c` | 41 118 B · `e4bd552e4582d4ce87e3bd2bfce41823d41bffcb00c360fbb9f8f7fff3a5b947` |
| `message.c` | 77 150 B · `f0b79bddcdba0c89ff62a632628ef84e8dfa4f0017ad9317f994167f263731e1` |
| `message.h` | 5 329 B · `c276068c69878c57737e0e60782ae8029333c82182020b532113a86040d51b25` |
| `neighbour.c` | 10 764 B · `ac62baf9e9cf71d9cc2b82c704ec8e412342008508c5c5f3d39a82f894f9bb94` |
| `neighbour.h` | 3 013 B · `cbcc64b7412d618c472fa8df6c222bd181dc7a3d91054484be9b0f044e66ddd5` |
| `resend.c` | 9 979 B · `673dfb387ff94b26c5eeeb9216ed6b7bb7ff375f4640f2a3125d61899516bfcb` |
| `resend.h` | 2 700 B · `e76b584f15d87259e1f9c1ad255b0a222ff17444ecde11bd1c453a80598f956e` |
| `route.c` | 36 204 B · `220452122e99334958d2299da0084091e57aa42543f58fa08ea31baac45664ea` |
| `route.h` | 5 554 B · `0e886983b0083234e7c8544805f21354ee4d756af0727f5e9bbed4fb15b8b163` |
| `source.c` | 6 295 B · `21ae2b411eac5a46c9384e555ebf60e13d7b8bb0d2605dec1cdb1af2159d2a15` |
| `source.h` | 1 955 B · `780fec7cebd1ea8313987cbd2babdec32b6280ebb6462f0b3b5138ee6769462e` |
| `util.c` | 12 466 B · `9e7ec0f8a7206b4c315c8a245858a07118f55bb614865894ecd72923cf45cff1` |
| `util.h` | 5 725 B · `26cd5b5d6386f2afeef8951295920311ad54fb2765244cb3291e38a5b3f703b8` |
| `xroute.c` | 15 577 B · `d7fda76f675458135dd92b51e37e26a859464a07b059b9ea26844c75dd8e867e` |
| `xroute.h` | 2 137 B · `a32f90e692a718d98d2d0ee2a023b7ff78f84d502dd31d7bbbb3a7aae82f05aa` |

### Otopilot ve yer istasyonu — bağ kopması zaman aşımları (15 Ekim 2026, K-246)

**Uygulama kaynakları** (`uygulama_kaynaklari/otopilot/`): gecikme tavanlı `PDR_açık`ın eşikleri (5 s ana; 3,5 s ve 10 s duyarlılık). Her dosya indirildiği anın commit'ine sabitlendi (`master` değişir), yürütücünün izniyle indirildi, gömülü talimat taraması temiz; değerler dosyaların kendisinden doğrulandı.

| dosya | künye | alındığı yer | boyut · SHA-256 | sağladığı |
|---|---|---|---|---|
| `ardupilot_ArduCopter_Parameters.cpp` | ArduPilot `ArduCopter/Parameters.cpp` (GPL-3.0) | `https://raw.githubusercontent.com/ArduPilot/ardupilot/eb8b5180a1b81e11eb022bcee10a54068ed109de/ArduCopter/Parameters.cpp` | 56 272 B · `e074f4ecbba5f23517ba1ade1a622c6c8e5a8c37de435ee171fbd7459e312383` | `FS_GCS_TIMEOUT` = 5 s |
| `ardupilot_ArduPlane_Parameters.cpp` | ArduPilot `ArduPlane/Parameters.cpp` (GPL-3.0) | `https://raw.githubusercontent.com/ArduPilot/ardupilot/eb8b5180a1b81e11eb022bcee10a54068ed109de/ArduPlane/Parameters.cpp` | 79 047 B · `d45fc6dc9238c3165e03e07b7bd3866b2d1b48ef5fcc8cadd8dd135d7b77c2b9` | `FS_LONG_TIMEOUT` = 5 s; `FS_GCS_ENABL` bu süreyi kullanır |
| `px4_commander_params.c` | PX4-Autopilot v1.14.0 `src/modules/commander/commander_params.c` (BSD-3) | `https://raw.githubusercontent.com/PX4/PX4-Autopilot/b8c541dd7277ed735139d7d1bfb829d61fbe29fb/src/modules/commander/commander_params.c` | 27 088 B · `2d8d82aa5e521864e71e36af0cf30fe53e2b28923c156e211d3c399ab716223b` | `COM_DL_LOSS_T` = 10 s (en az 5, en çok 300) |
| `qgc_VehicleLinkManager.h` | QGroundControl `src/Vehicle/VehicleLinkManager.h` (Apache-2.0 / GPL-3.0) | `https://raw.githubusercontent.com/mavlink/qgroundcontrol/136960f304cf8cb9e82633eb06a188108a974b34/src/Vehicle/VehicleLinkManager.h` | 4 225 B · `523c649b4a00634684b1359b46c6a76c8e153b9e4e5508e460c4ef093f7e7f90` | `_heartbeatMaxElpasedMSecs` = 3 500 ms |
| `mavlink_heartbeat.md` | MAVLink Developer Guide `en/services/heartbeat.md` (CC BY 4.0) | `https://raw.githubusercontent.com/mavlink/mavlink-devguide/27cdc2d9d6671290b5b10a123e51f8a2749ebe2e/en/services/heartbeat.md` | 7 720 B · `e536a1c16ac7807bb273419d33812eb8c783b042e06d1f678d439427bae7f697` | RF telemetride 1 Hz heartbeat; 4–5 mesaj kaçarsa kopma |

## Faz 5-2 araştırma kaynakları — 21 Ekim 2026 (`faz5_arastirma_2026-10-21/`)

Faz 5'in araştırma aşamasında (`v2/12` §1.2, K-252) indirilen 15 dosya. Notlar ve konu konu kullanım aynı klasörde `NOTLAR.md`; doğrulama durumu ve okunan bölümler `v2/02` §F; künyeler `v2/16`. Hepsi açık erişim (arXiv, IETF, yazarların ya da yayıncının sayfası); alınma tarihi 21 Ekim 2026.

| dosya | künye (kısa) | alındığı yer | boyut (bayt) · SHA-256 |
|---|---|---|---|
| `an_weber_2018_reactive_jamming.pdf` | N. An, S. Weber, arXiv:1809.04263v1, 2018 | `https://arxiv.org/pdf/1809.04263` | 1 693 583 · `5a08494e299c2cd38d44183008f16779c44aa63bb3679140761b75dc7c978cb6` |
| `cerar_2021_lqe_survey.pdf` | G. Cerar vd., arXiv:1812.08856v10, 2021 | `https://arxiv.org/pdf/1812.08856` | 1 146 860 · `faad463dbf3a0fedfd8255b93074a0f784d6d64d7798d3eff73b6c397d6bdecf` |
| `decouto_2003_etx.pdf` | D. S. J. De Couto vd., ACM MobiCom 2003 | `https://pdos.csail.mit.edu/papers/grid:mobicom03/paper.pdf (yazarların laboratuvarı)` | 284 493 · `7811ff8dac1a2e3fea6a85715c8c2426af8588f9e40e4a69e83bb68f840bb480` |
| `jonglez_chroboczek_2014_delay_metric.pdf` | B. Jonglez, M. Boutier, J. Chroboczek, arXiv:1403.3488v1, 2014 | `https://arxiv.org/pdf/1403.3488` | 228 041 · `d114baaea5964d6e38cd0dff7aeb5dc5cf0a6f4ac76796266ca0ca2464ea2b88` |
| `punal_2014_wifi_jamming_detection.pdf` | O. Puñal vd., IEEE WoWMoM 2014 | `https://www.comsys.rwth-aachen.de/fileadmin/papers/2014/2014-aktas-wowmom-jammingdetection.pdf (yazarların bölümü)` | 1 203 506 · `115f659567fe0aca201a93bcc755564fbcf71e83e76ef2d83ac884ddb0c0e12b` |
| `ramachandran_2007_routing_stability.pdf` | K. Ramachandran vd., PAM 2007 | `https://ebelding.cs.ucsb.edu/sites/default/files/publications/pam07.pdf (ortak yazarın sayfası)` | 1 929 084 · `d3d5d0976a8698ca2f2693ff51574c3f8663548f8d6069a3a60d26b6f6ae3310` |
| `tague_2011_jamming_aware_traffic_allocation.pdf` | P. Tague vd., IEEE/ACM ToN 2011 | `https://labs.ece.uw.edu/nsl/papers/ToN_11.pdf (yazarların laboratuvarı)` | 425 389 · `ec5e9bcd53bb449a93b0a016ad1d6adda0bf9587ae24fb3a1d4315d4f8cf33df` |
| `telecom_2024_olsr_batman_babel.pdf` | D. Turlykozhayeva vd., Telecom 5(4), 2024 | `https://mdpi-res.com/d_attachment/telecom/telecom-05-00051/article_deploy/telecom-05-00051.pdf (yayıncı)` | 1 564 386 · `fd57f390b2be55c36bf200ab58a94e6e363ee4ac83f524f4558c7e35b450fbf8` |
| `yang_2025_uav_antijamming_survey.pdf` | J. Yang vd., arXiv:2508.11687v1, 2025 | `https://arxiv.org/pdf/2508.11687` | 632 026 · `dc298d8473ddd715803696128f1a53ee359eea53314b14a2f3ea72fa35b9113e` |
| `zhao_2026_perhop_multipath_uav.pdf` | Z. Zhao vd., arXiv:2608.25383v1, 2026 | `https://arxiv.org/pdf/2608.25383` | 4 669 463 · `56eed1401dc60360fb1fc92668b8e0b310388b9e7dfe50cdf5d021ec8f297a27` |
| `rfc5286_lfa.txt` | RFC 5286, Eylül 2008 | `https://www.rfc-editor.org/rfc/rfc5286.txt` | 71 027 · `7c612d458dbe0e6730ee38b43b75205acd24c967a2ec209cb8f40f5bc2b72c8b` |
| `rfc6206_trickle.txt` | RFC 6206, Mart 2011 | `https://www.rfc-editor.org/rfc/rfc6206.txt` | 30 283 · `a38faf4084395f992b8fd2f7e07d5da22184f7251a55287a387a3c9a25337d47` |
| `rfc6550_rpl.txt` | RFC 6550, Mart 2012 | `https://www.rfc-editor.org/rfc/rfc6550.txt` | 360 651 · `2c09f5945d6dbba4b69203a826121150c0cff1748d10f22c5a75060e53f5cb82` |
| `rfc6719_mrhof.txt` | RFC 6719, Eylül 2012 | `https://www.rfc-editor.org/rfc/rfc6719.txt` | 29 637 · `e0d71ba04db12930533b94ac5a420d7a33661a31016d19c31d1261851e9852ad` |
| `rfc7868_eigrp_dual.txt` | RFC 7868, Mayıs 2016 | `https://www.rfc-editor.org/rfc/rfc7868.txt` | 179 677 · `960af059ab0f2ee3a9c3adf930ad1036866cade0b5761298ee8bb978a9cee3b1` |

**Gerçeklik denetimi:** PDF imzası, sayfa sayısı, ilk sayfanın başlık ve yazarları künyeyle tutarlı; RFC'lerin başlıkları ve tarihleri rfc-editor kaydıyla tutarlı.

**Güvenlik denetimi:**
- Ham PDF baytlarında etkin içerik anahtarları: `/JavaScript`, `/Launch`, `/EmbeddedFile`, `/AA` **yok**. `/OpenAction` (iki arXiv dosyasında) yalnız açılış görünümünü gösteriyor; `/URI` bağlantıları kaynakça ve DOI bağlantıları.
- Metinde gömülü talimat kalıbı taraması: eşleşmelerin hepsi yanlış alarm ("Bellman" sözcüğü, kaynakçadaki bir kişi adı, bir makale başlığı, bir makalenin dil düzeltmesi beyanı).
- Dosyalar önce ayrı geçici klasörlerde denetlendi, sonra buraya kopyalandı.

**Alınamayanlar** (`NOTLAR.md` §10): Xu vd. 2005 (ACM, açık kopya yok) · Greco vd. 2021 (yazar sayfasının sertifikası geçersiz; TLS denetimi atlanmadı) · Mahmud & Cho 2019 · PMC 2021 · ExOR (sunucuya ulaşılamadı).
