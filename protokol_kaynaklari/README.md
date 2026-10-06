# Protokol kaynakları — birincil belgeler

Taban protokollerin tanımlandığı **birincil belgeler**. TÜBİTAK proje yazımında
atıf ve alıntı için buradan kullanılır. Her belgenin künyesi, nereden
alındığı, özeti (SHA-256) ve hangi denetimlerden geçtiği aşağıda. Doğrulanmış
kaynakların tam listesi ve projedeki kullanımları: `v2/02-DOGRULANMIS-KAYNAKLAR.md`.

🔒 **Kural (öğrenci, 19 Eylül 2026):** bir belge buraya ancak **tamamı
okunduktan** ve gerçek olduğu, içinde yapay zekâya yönelik talimat benzeri bir
şey olmadığı denetlendikten sonra girer.

**Bu klasördeki iki DIŞ KAYNAK OLMAYAN klasör** — öğrencinin kendi çalışmasıdır,
yukarıdaki indirme kuralına tabi değildir:

| klasör | içerik |
|---|---|
| `DESPARETE_TASARIM_PAKETI/` | öğrencinin protokol tasarımı, v0.1 (40 dosya: dizin + 39 tasarım belgesi — 23 Eylül'de sayıldı, önceki "41" yanlıştı; tek okuma `36`). İnceleme ve kararlar `v2/04` K-150 |
| `literatur_taramasi_2026-08-31/` | öğrencinin ikinci literatür taraması (20 dosya) — 23 Eylül'de `v2/`den taşındı. ⚠️ İçindeki atıflar kullanılmadan önce birincil kaynaktan doğrulanır (`v2/02`) |

---

## marina_das_2001_aomdv_icnp.pdf — AOMDV

| | |
|---|---|
| **künye** | M. K. Marina, S. R. Das, *"On-demand Multipath Distance Vector Routing in Ad Hoc Networks"*, Proceedings of the IEEE International Conference on Network Protocols (ICNP), s. 14–23, 2001 |
| **genişletilmiş dergi sürümü** | M. K. Marina, S. R. Das, *"Ad hoc on-demand multipath distance vector routing"*, Wireless Communications and Mobile Computing 6(7):969–988, Kasım 2006 · DOI 10.1002/wcm.432 (ücretli; künye Edinburgh Üniversitesi kurum sayfasından doğrulandı) |
| **alındığı yer** | `https://www3.cs.stonybrook.edu/~samir/Pubs/icnp-01.pdf` — ortak yazar Samir R. Das'ın kendi üniversite sayfası |
| **alınma tarihi** | 19 Eylül 2026 (öğrenci izniyle) |
| **boyut · SHA-256** | 127 110 bayt · `e41c5df42170b723180867ba9a72d37ec7a4ca1923b0921503ed77a350f123e6` |

**Gerçeklik denetimi:**

- Dosya türü `application/pdf`, imza `%PDF-1.2` (2001 dönemine uygun)
- 10 sayfa — atıftaki *"s. 14–23"* ile tutarlı
- Başlık, yazarlar, yazarların 2001'deki kurumu (Cincinnati Üniversitesi),
  özet ve 35 maddelik kaynakça AOMDV hakkında bilinenlerle tutarlı
- Metin kaynakçayla bitiyor; sonrasında hiçbir şey yok

**Güvenlik denetimi (öğrencinin isteği — istem enjeksiyonuna karşı):**

- Metinde yapay zekâya yönelik talimat kalıbı taraması: **eşleşme yok**
  (yalnız kaynakçadaki iki ns-2 ve IETF bağlantısı)
- PDF yapısında etkin içerik (`/JavaScript`, `/OpenAction`, `/Launch`,
  `/URI`, `/EmbeddedFile`, `/AA`): **sıfır**
- Görünmez metin (render kipi 3): **sıfır**

⚠️ **Bilinen sınır:** makale 2001 dönemi dvips çıktısıdır; matematik simgeleri
**Type 3 bit eşlem yazı tiplerinde** (`/a0 … /a255`) ve metin olarak
çıkarılamıyor. Etkilenen kısımlar: Şekil 1 (AODV güncelleme kuralı), Şekil 3
(**AOMDV rota güncelleme kuralı**) ve bölüm 3.2'deki `k` değeri.

🟢 **Görsel olarak okundu (19 Eylül 2026):** öğrenci PDF'i açıp iki bölgenin
ekran görüntüsünü verdi; ikisi de bu klasörde:

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

⚠️ **Bu sürümde OLMAYANLAR:** ICNP makalesinin 3. bölümü `k` paragrafıyla
biter. Rota bakımı (bir yol kopunca ne yapılır, RERR), verinin hangi yoldan
gönderileceği ve yol başına zaman aşımları ayrı bir bölüm olarak YOK —
büyük olasılıkla dergi sürümünde (ücretli). ns-2.35'teki AOMDV kodu yazarların DEĞİL (Marcello Caleffi, 2008) —
boşluklar öğrenci kararıyla (22 Eylül) makale + RFC 3561'den doldurulur,
belirtilmemiş seçimler `protokoller/aomdv.py` başlığında beyanlı
(`v2/02-DOGRULANMIS-KAYNAKLAR.md` §R4.1).

⚠️ **Dağıtım:** yazarın kendi sayfasında yayımladığı kopyadır ve bu depoda
özel araştırma kullanımı içindir. Depo herkese açık yapılacaksa yeniden
dağıtım hakkı ayrıca denetlenmelidir.

---

## rfc3561_aodv.txt — AODV

| | |
|---|---|
| **künye** | C. Perkins, E. Belding-Royer, S. Das, *"Ad hoc On-Demand Distance Vector (AODV) Routing"*, RFC 3561, Temmuz 2003, kategori: Experimental |
| **alındığı yer** | `https://www.rfc-editor.org/rfc/rfc3561.txt` — RFC Editor, kanonik metin |
| **alınma tarihi** | 19 Eylül 2026 (öğrenci izniyle) |
| **boyut · SHA-256** | 90 356 bayt · `b3294169ed3e0cf87c1acc1d99ac8b428eec279c563d64fb10cc1c902a60d579` |

## rfc3626_olsr.txt — OLSR

| | |
|---|---|
| **künye** | T. Clausen, P. Jacquet (ed.), *"Optimized Link State Routing Protocol (OLSR)"*, RFC 3626, Ekim 2003, kategori: Experimental |
| **alındığı yer** | `https://www.rfc-editor.org/rfc/rfc3626.txt` — RFC Editor, kanonik metin |
| **alınma tarihi** | 19 Eylül 2026 (öğrenci izniyle) |
| **boyut · SHA-256** | 161 265 bayt · `722a7b5838ac29fe71aa48fa91ae619ab1ef8c128a754a84a98d705cefe17580` |

**İki RFC için denetim — ne yapıldığı TAM OLARAK:**

- Başlık, yazarlar, tarih, kategori ve sayfa sayısı (37 · 75) doğru.
- RFC 3626'nın boyutu (161 265), aynı gün tarayıcıda okunan metnin karakter
  sayısıyla BİREBİR aynı.
- Projede bugüne kadar alıntılanan cümleler indirilen metinlerde kelimesi
  kelimesine geçiyor: §6.9 *"Hello messages or otherwise"* · §6.11 *"have a
  non-empty precursor list"* · §18.9 *"MAXJITTER = HELLO_INTERVAL / 4"*.
- Tam metin taramasında yapay zekâya yönelik talimat kalıbı: **yok**.

⚠️ **Dürüst sınır:** RFC'lerin HER satırı okunmadı. Protokolle ilgili bölümler
okundu (AODV §5, §6, §10 · OLSR §3–§10, §13–§14, §18–§19) ve metnin tamamı
kalıp taramasından geçti. Kaynak RFC Editor'ün kendisi olduğu için risk
çok düşük; yine de "tamamı okundu" demek doğru olmazdı.

🔒 RFC metinleri IETF Trust'ın lisansıyla serbestçe dağıtılabilir.

---

## Gerçekçilik kaynakları — 25 Eylül 2026 (öğrenci izniyle, her biri ayrı; K-168, `v2/12` Faz 0)

Hepsi önce geçici alana indirildi, denetlendi, sonra buraya alındı. **Ortak denetim** (`pdftotext` ile metin + ham PDF taraması):
- etkin içerik (`/JavaScript`, `/Launch`, `/EmbeddedFile`, `/AA`, `/XFA` …) yok. İki arXiv dosyasında birer `/OpenAction` var; ikisi de yalnız `/GoTo … /Fit` (ilk sayfayı sığdırarak aç).
- yapay zekâya yönelik talimat kalıbı yok. Tek eşleşme RFC 8966'da, protokol metni: *"receiver MUST ignore any TLV"*.

| dosya | künye | alındığı yer | boyut · SHA-256 | okunan |
|---|---|---|---|---|
| `pei_henderson_2009_ns3_80211b_dogrulama.pdf` | G. Pei, T. Henderson, *"Validation of ns-3 802.11b PHY model"*, Boeing Research & Technology, Mayıs 2009 (21 s.) | `https://www.nsnam.org/~pei/80211b.pdf` (ns-3 projesi) | 148 982 B · `74d87ea8c318a7b9e9de2315866b2a316977aeb5a2d00ff1231c593cdf288e80` | **tamamı** |
| `boer_1996_ieee80211_dsss_phy.pdf` | J. Boer, *"Direct Sequence Spread Spectrum Physical Layer Specification IEEE 802.11"*, doc. IEEE P802.11-96/49E, Mart 1996 (taslaktan parçalar içerir) | `https://grouper.ieee.org/groups/802/11/Tutorial/ds.pdf` (IEEE 802.11 çalışma grubu) | 56 148 B · `49d8af18f445144fb0152c52e6ceda642008bd2baed000b9f06f8c4624f7ff61` | **tamamı** |
| `rfc8966_babel.txt` | J. Chroboczek, D. Schinazi, *"The Babel Routing Protocol"*, RFC 8966, Ocak 2021, Standards Track | `https://www.rfc-editor.org/rfc/rfc8966.txt` | 141 512 B · `592fe69e208f6c3f1ac5d8e673eb309a9f6323a4c471de9284385c0005db1f2f` | §1–§2 (kavramsal, uygulanabilirlik ve sıra numarası) tamamı; kalanı kalıp taramasında |
| `koubaa_2019_mavlink_survey.pdf` | A. Koubâa vd., *"Micro Air Vehicle Link (MAVLink) in a Nutshell: A Survey"*, arXiv:1906.10641v1, 2019 (9 s.) | `https://arxiv.org/pdf/1906.10641` | 856 711 B · `f0ffa9f95675e29280b6c87b2d07d82349c4646562d9cace6bcd85fa2cc0e41e` | başlık yapısı, mesaj boyları, yaşam sinyali, telemetri telsizleri tablosu; kalanı taramada |
| `pirayesh_zeng_2021_jamming_survey.pdf` | H. Pirayesh, H. Zeng, *"Jamming Attacks and Anti-Jamming Strategies in Wireless Networks: A Comprehensive Survey"*, arXiv:2101.00292v1, 2021 (16 s.) | `https://arxiv.org/pdf/2101.00292` | 1 827 418 B · `a1c943d03e52d7781d432e1d678894f2feda6e0b620e956bf2cf2fb5cfa193c9` | WLAN karıştırma saldırıları, hız uyarlaması/güç kontrolü ve karıştırma tespiti bölümleri; kalanı taramada |

**Projeye taşıdıkları** (ayrıntı `v2/02` · `v2/14`):
- **802.11b hata modeli** (Pei & Henderson): gürültü 22 MHz'de; Eb/N0 = SINR · 22/1 (1 Mb/s DBPSK) · SINR · 22/1/2 (2 Mb/s DQPSK) · CCK 5,5 ve 11 Mb/s için ·4 ve ·2. CMU ölçümleriyle (Prism 2.5) karşılaştırılmış.
- **Barker kodu:** kodlama kazancı 10,4 dB, *"girişime ve gürültüye karşı ~10 dB bastırma"* (Boer).
- **CCA:** modlar 1–3; ED eşiği verici gücüne bağlı (>100 mW −80 dBm · >50 mW −76 dBm · ≤50 mW −70 dBm); enerji sezme 15 µs.
- **Zamanlama ve alıcı:** slot 20 µs · Tx→Rx dönüşü 10 µs, Rx→Tx 5 µs · duyarlılık −80 dBm (FER 0,08, 1024 B) (Boer).
- **Babel:** uygulanabilirlik mesafesi (§2.4) ve sıra numaralı rotalar (§2.5–2.6) — DESPARETE'nin döngüsüzlük ailesi; README'deki atıf doğrulandı (`02` S6).
- **MAVLink:** mesaj 8–263 B (v1), yaşam sinyali ~1 Hz.
- **Karıştırma tespiti:** gürültü gücü, kanal meşgul oranı, çerçeveler arası süre, sinyal gücü ve teslim oranı birlikte kullanılıyor (Puñal vd., taramanın [83]'ü). Hız uyarlaması düşük güçlü girişimde etkili, yüksek güçlü sürekli karıştırmada etkisiz (Pelechrinis vd., [79]–[80]).

⚠️ **Dağıtım:** arXiv ve ns-3 belgeleri yazarların herkese açık kopyalarıdır; depo herkese açık yapılacaksa yeniden dağıtım hakkı ayrıca denetlenmelidir. IEEE 802.11-2016'nın kendisi burada yok — yalnız IEEE GET programından, IEEE hesabıyla (öğrenci) alınabilir.

### Öğrencinin indirdikleri — 25 Eylül 2026 akşamı (ajan denetledi)

Aynı ortak denetim; geçici kopyalar üzerinde. Etkin içerik yok. İki yanlış alarm çözüldü: Goddemeier dosyasındaki `/JS` bir DOI'nin parçası (`…/JSAC.2012.120610`); NATO belgesindeki `/AA` sıkıştırılmış akışta rastgele bayt. Gömülü tek dosya IEEE'nin PDF üretim ayarı (`CMW_Acr8_V1.joboptions`). Talimat kalıbı yok; Al-Hourani'deki "disregard" teknik cümle (*"we can disregard hRX"*).

| dosya | künye | boyut · SHA-256 | okunan | not |
|---|---|---|---|---|
| `al_hourani_2014_optimal_lap_altitude.pdf` | A. Al-Hourani, S. Kandeepan, S. Lardner, *"Optimal LAP Altitude for Maximum Coverage"*, IEEE Wireless Communications Letters, 2014 (4 s.) | 667 334 B · `657c893e7840749967599974f4c19bd54d61323a8d2c14f2bacf49bb2bee40ee` | **tamamı** | yer–hava modeli: PL = FSPL + η; P(LoS, θ) = 1 / (1 + a·exp(−b[θ − a])); (η_LoS, η_NLoS) banliyö (0,1; 21) · kentsel (1,0; 20) · yoğun kentsel (1,6; 23) · yüksek yapılı (2,3; 34) dB; a, b Tablo I–II polinomlarından |
| `doodlelabs_rm2450_veri_sayfasi_2021.pdf` | Doodle Labs, *Smart Radio RM-2450 Datasheet* (2×2 MIMO Mesh Rider, 2 400–2 482 MHz), 20 Aralık 2021 (10 s.) | 354 100 B · `1c4a76b492e1eccf955f602a5bc5c6ab0c63b14f5fa45af665a826e8f47b178c` | **tamamı** | çıkış Pro 27 dBm · Xtreme 33 dBm (MCS 0) · ABD 4 W EIRP, **Avrupa 100 mW EIRP** · DC güç Tx ≤ 10,6 W (Pro) / 14 W (Xtreme), Rx 2 W, uyku 1,2 W · tümleşik GPS **1,5 m CEP** · duyarlılık OFDM MCS 0: 3 MHz −100, 5 MHz −98 dBm · 802.11b/g/n uyumlu |
| `goddemeier_daniel_wietfeld_2012_jsac_a2g.pdf` | N. Goddemeier, K. Daniel, C. Wietfeld, *"Role-Based Connectivity Management with Realistic Air-to-Ground Channels for Cooperative UAVs"*, IEEE JSAC 30(5):951–963, Haziran 2012 (13 s.) | 1 648 920 B · `1d80f6c8ae0dc45fe6335743d6a1e06cf3cd87ed70a4b432bf51485582c034a3` | kanal bölümü (V) | ⚠️ **istenen makale değil** (istenen: Goddemeier & Wietfeld, GLOBECOM Wi-UAV 2015, hava–hava Rice modeli). Hava–hava için "basit serbest uzay" varsayar; yer–hava için yüksekliğe bağlı yol kaybı üsteli. ⚠️ Kopyada *"Authorized licensed use limited to: Universitaetsbibliothek der RWTH Aachen"* damgası var — yalnız araştırma kopyası, yeniden dağıtılmaz |

**Depoya alınmayanlar:**
- **NATO SPCoE kitabı:** Yzb. (TUR GEND) Yüksel Kütük, *"UAS (Unmanned Aircraft Systems): The Force Multiplier for Law Enforcement Agencies and the Potential Contributor to Stability Policing"*, NATO SPCoE, 2025, ISBN 979-12-5539-066-4. Kaynak: `https://nllp.jallc.nato.int/iks/sharing%20public/uas-unmanned-aircraft-systems.pdf`. 3 639 808 B · `160b3e547ccddb228f6a24b1f87c94b97ed386291428e6a55bfca0f7bd6404e3` (63 s.). Yalnız §1.4.3 okundu: NATO sınıflandırması, NATO ATP-3.3.8.1 Ed. B v1, 2019'dan — **Sınıf I "küçük" (>15 kg): taktik birlik, ≤ 5 000 ft AGL, görev yarıçapı 50 km (görüş hattı), ör. ScanEagle**. Web okumasında araç tarafından kendiliğinden kaydedildi, öğrencinin izniyle kullanıldı. Yayıncının izinsiz elektronik saklama yasağı nedeniyle kopyası depoya alınmadı.
### Ücretli iki kaynağın açık alternatifleri — 25 Eylül 2026 gecesi (öğrenci seçimi ajana bıraktı: *"hangilerinin kaliteli ve güvenilir olduğunu düşünüyorsan onları indir"*)

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
| `ns-3/arf-wifi-manager.cc` · `.h` | ARF hız uyarlaması (Kamerman & Monteban 1997'ye atıflı; zaman sayacı yerine paket sayacı): en düşük hızdan başla · **10** art arda başarı ya da **15** iletimlik sayaç → bir hız yukarı ve kurtarma kipi · kurtarmada ilk başarısızlık, normalde art arda **2** başarısızlık → bir hız aşağı. 26 Eylül 2026 indirildi (öğrenci izniyle, 8 353 B + 2 621 B), tamamı okundu | `723572f3502109ca4cf8d17950ddae78a1f74c6f297d60af7e7c614704fa86c0` · `d52e373873f0b29676f37621c0d85d2c18605b1cb98ea85ee687c9eb6e811d78` |
| `ns-3/aodv-routing-protocol.cc` · `aodv-rqueue.cc` · `.h` | AODV rota tamponu: `MaxQueueLen` **64**, `MaxQueueTime` **30 s**; kuyruk dolunca *"Drop the most aged packet"*, süresi dolan `Purge`da düşer. Başlık: *"Based on NS-2 AODV model developed by the CMU/MONARCH group and optimized and tuned by Samir Das and Mahesh Marina"*. 28 Eylül 2026 indirildi (öğrenci izniyle, 86 436 B · 3 405 B · 6 649 B), ilgili kısımlar okundu — `rota_tamponu_*` köken kaydı (K-198) | `104dbf6352b70949a114f4db3d3e21c6deb176082cc0b3138ff8025848eeb6b0` · `c66643b64d8131f9194f26b8192752f6c1923399a3f534a3ed7beec45a3aa678` · `d9651df51f082472bab64752617d2939d24cc3b09d8945e81f7e764e80a7eb1e` |
| `ns-3/wifi-mac-header.cc` | çerçeve başlık boyları: veri **2 + 2 + 6 + 6 + 6 + 2 = 24 B**, onay (ACK) **2 + 2 + 6 = 10 B** (FCS hariç; FCS **4 B** `wifi-standard-constants.h`de `WIFI_MAC_FCS_LENGTH`) → onay çerçevesi 14 B. 30 Eylül 2026 (öğrenci izniyle, K-203), 29 777 B, `GetSize` okundu | `cbe9061a40a65ae4467a7df8cbfa44f95c05125e8f7d68ef6dfc3d45cfc13f6e` |
| `ns-3/llc-snap-header.cc` | LLC/SNAP başlığı `LLC_SNAP_HEADER_LENGTH` (değeri RFC 1042: 8 oktet). 30 Eylül, 1 767 B, tamamı | `6a89e53e5b3bce433056a72a45d1c65226d2847f6a8a008a3c7a542a47ae93cd` |
| `ns-3/wifi-mac-queue.cc` | MAC kuyruğu varsayılanı **`MaxSize` 500 paket · `MaxDelay` 500 ms** (bizde 50 paket, süre sınırı yok — NS-2 `ifqlen` geleneği; değer farklı → duyarlılık ölçülür, Faz 4.4). 30 Eylül, 15 544 B, öznitelikler okundu | `dc5c27e1343510d027ae01bc90aef4d267ff0c81ff963df1f2270b53b68ca2f0` |
| `ns-3/simple-frame-capture-model.cc` · `frame-capture-model.cc` | yakalama: yeni çerçeve süren çerçeveden **5 dB** güçlüyse ve önbelge sezildikten sonraki **16 µs**'lik pencerede ise alım yeni çerçeveye geçer (bizde 10 dB · 192 µs; model ayrıntısı farklı → duyarlılık ölçülür, Faz 4.4). 30 Eylül, 1 823 B · 1 046 B, tamamı | `06a33f211d82f2c271cfb0bc82ab78e63156ae43ce5d94e79c0ba6b46e95c170` · `17909434a659c3899420bedc2fce4f6bf22c52d3f7791fca24bdd732caae0573` |
| `ns-3/wifi-utils.h` | yardımcı bildirimler (ACK boyu "FCS dâhil" hesaplanır). 30 Eylül, 8 584 B, taramada | `76454b3f2d9f0de839c8fb838a6bf3cdc1e0ad621ae11372cdb8a52e623720b2` |

30 Eylül'de indirilen `wifi-mac-trailer.h` FCS sabitini taşımadığı için `arsiv/kaynak_elenen/`e taşındı (sabit zaten `wifi-standard-constants.h`de). Denetim: talimat kalıbı yok; dosyalar GPL-2.0-only başlığını taşıyor.

### RFC'ler — kontrol kapsüllemesi (30 Eylül 2026, öğrenci izniyle, K-203)

| dosya | künye | alındığı yer | boyut · SHA-256 | okunan |
|---|---|---|---|---|
| `rfc791.txt` | J. Postel, *"Internet Protocol"*, RFC 791, Eylül 1981 | `https://www.rfc-editor.org/rfc/rfc791.txt` | 94 892 B · `6cfb387fcecfc1b72f2f69343c5b6951b5d263d708162e2b5c66ab8f394f6265` | §3.1 başlık biçimi: IHL en az 5 × 32 bit → **20 oktet** |
| `rfc768.txt` | J. Postel, *"User Datagram Protocol"*, RFC 768, Ağustos 1980 | `https://www.rfc-editor.org/rfc/rfc768.txt` | 5 896 B · `7dc8880e1ecef9c3f9da0db4b876a16e96bfa4f0953cc9d977d414f8f680c2f0` | tamamı: başlık kaynak/hedef kapısı, uzunluk, sağlama — **8 oktet** |
| `rfc1042.txt` | J. Postel, J. Reynolds, *"A Standard for the Transmission of IP Datagrams over IEEE 802 Networks"*, RFC 1042, Şubat 1988 | `https://www.rfc-editor.org/rfc/rfc1042.txt` | 34 359 B · `e8737abe7f7b80ae2e84b8cada0ea02d8cc3c4ad2414e902cc055e6953a01c55` | başlık bölümü: *"The total length of the LLC Header and the SNAP header is 8-octets"* |

### RFC 1700 ve ns-3 IPv4 — veri paketinin varsayılan TTL'i (6 Ekim 2026, öğrenci izniyle, K-215)

| dosya | künye | alındığı yer | boyut · SHA-256 | okunan |
|---|---|---|---|---|
| `rfc1700_assigned_numbers.txt` | J. Reynolds, J. Postel, *"Assigned Numbers"*, RFC 1700 (STD 2), Ekim 1994 — RFC 3232 (2002) ile tarihsel; kayıtlar IANA'nın çevrimiçi veritabanına taşındı | `https://www.rfc-editor.org/rfc/rfc1700.txt` | 458 860 B · `77de0532a5b4b6bef3d233795b5a87aae1838358b98e7da82676e0c6455eb03e` | "IP TIME TO LIVE PARAMETER": *"The current recommended default time to live (TTL) for the Internet Protocol (IP) [45,105] is 64."* |
| `uygulama_kaynaklari/ns-3/ipv4-l3-protocol.cc` | ns-3-dev `src/internet/model/ipv4-l3-protocol.cc` (GPL-2.0-only) | `https://gitlab.com/nsnam/ns-3-dev/-/raw/master/src/internet/model/ipv4-l3-protocol.cc` | 58 517 B · `faa5c2a9c5fdb800fda076bab33cb42b8b5dec5b208d46cd10a13d10e5b146ef` | öznitelik `DefaultTtl`: *"The TTL value set by default on all outgoing packets generated on this node"*, **64** |

Denetim: talimat kalıbı yok (RFC 1700'deki "Claude" geçişleri kayıt sahibi adları).
| `linux/net_wireless_core.c` | *"Initialize wiphy parameters to IEEE 802.11 MIB default values"*: `retry_short = 7`, `retry_long = 4`, RTS kapalı | `a1e6ebc52f7634585e5c7e8cb29b2e106de5af12da68cf9e5ed0794ad94fcb9a` |

- **`arsiv/kaynak_elenen/ieee_80211_2016_kesit_madde21_IPR2023-01414.pdf`:** IEEE Std 802.11-2016'nın yalnız 9 sayfası, madde 21 (VHT/802.11ac, s. 2538–2580). Bir ABD patent davasının delil dosyası (*"IPR2023-01414 · Patent Owner · EX 2003"*), üçüncü kişinin lisans damgasıyla. İhtiyaç duyulan 802.11b maddeleri (15–16) ve MAC zamanlaması (madde 10) yok → kaynak olarak kullanılmadı, arşive taşındı.
