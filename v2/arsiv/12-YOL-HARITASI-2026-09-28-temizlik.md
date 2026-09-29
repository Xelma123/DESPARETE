# 12 · YOL HARİTASI — gerçekçilik ve karıştırmayı çözen DESPARETE (Faz 0–7)

> **Güncel:** 25 Eylül 2026 akşamı — öğrencinin yön değişikliği ve onayladığı plan (K-168). Önceki sürümler: ayrıntılı iş listesi (İ-1…İ-45, KR-1…KR-20) `v2/arsiv/12-YOL-HARITASI-2026-09-25-ayrintili.md` · öz `…-oz.md` · tam `…-2026-09-25.md`. Eski İ/KR numaraları aşağıda parantez içinde, hangi faza geçtiklerini göstermek için.
> **İşaretler:** 🟢 bitti · 🟡 sürüyor · ⏳ sırada · ⚪ zamanı gelince · 🟦 öğrenci kararı/onayı · **[yapı]** `sim2/` değişikliği: önce yapı anlatılır, onay alınır, regresyon koşulur · **[süre]** 30 dk'yı aşan koşum: önce sorulur · **[indirme]** her kaynak için ayrı izin. Süreler tahmin ve bant. Her ölçümün beklentisi ölçmeden önce yazılır.
> Kodda geçen eski atıflar: "`12` §3 C1…C7" = Aşama 1 kalibrasyonları (C1 · C2 · C3 · C7 kapandı, K-125…K-128; C4–C6 bugün Faz 4'te) · "`12` §5" = eski tam yol haritası (protokolsüz borçlar → Faz 4; DESPARETE'nin parça parça yazımı → bitti).

---

## 1 · Nerede duruyoruz

**📍 Faz 4 — yeniden kalibrasyon ve doğrulama (4.3: yere toplama bitti, eşler arası sırada; 27 Eylül).** Faz 0–3 kapandı (K-169…K-181). Aşama numaralaması (`01` §5) geçerli: Aşama 1–2 🟢, Aşama 3 🟡. Bu plan Aşama 3'ün içinde simülatöre geri dönüş, Aşama 4 (mühür, ana deney) ve 5'i (yazım) de kapsar.

| | |
|---|---|
| yön | **önce gerçekçilik, sonra DESPARETE'nin karıştırmayı gerçekten çözmesi** (öğrenci, 25 Eylül; K-168) |
| simülatör | **referans dünya `referans_2026`** (1:1, işlem kazancı, ED-CCA, hız uyarlaması, yayılım gecikmesi, gerçekçi karıştırıcı; alan 33 km, 10 W karıştırıcı — K-181…K-188). 25 Eylül öncesi ölçümler eski dünyanın (1:50) |
| taban protokoller | **`AODV-f` · `OLSR-c` · `AOMDV-b`** (28 Eylül: §6.8 kara liste K-194 · §13 varsayılan kapalı K-196); eski dünyada `AODV-e` · `OLSR-b` · `AOMDV-a` kapalı (K-145 · K-147 · K-149). Referans dünyada U1 yere toplama (K-190, K-191, eski kod hâlleriyle): üçü de U1-U 🟢 · U1-B 🔴. Eşik değişmez, tasarım bedeli açıklamadır (K-192); OLSR'ın düşüklüğü = geçide rotanın aralıklı boşalması, "açıklanmış, sıralamasız" (K-193, K-196). ✅ kara liste · AOMDV U1–U4 · M4 boş kol (G1-P). Kalan: rota tamponu (kaynak, 8c) · ⚠️ birincil hücrede `OLSR-b ↔ OLSR-c` (§13 karıştırma altında sınanmadı) · U1 yeni kod hâlleriyle — üçü de pahalı koşu, izinle. **Donmadı** |
| çalışma biçimi | 🔒 **önce yazılım** (öğrenci, 28 Eylül, K-192): karıştırıcılı ya da hareketli tam pencere koşuları yazılım tamamlanınca, izinle |
| DESPARETE | **v0.4.1** varsayılan (K-172: v0.4 + V11 komut geri izi — komut artık taşınıyor; tam ölçek kısa pencerede komut PDR 0,87 statik · 0,57 hareketli) · v0.4 (K-167); küçük dünyada v0.2'nin teslimi, yükünün %57'si. Tam ölçekte doğrulanmadı — eski dünyada doğrulanmayacak, yeni dünyada Faz 5.0'da |
| test takımı · regresyon | `941 passed` (`python -m pytest tests2 -q`) · taban `k198` (K-198) |
| hesap bütçesi | birincil hücre 350 s ~1 sa/koşu (tek süreç; blok üreteci K-198, önce ~4 sa), ana deney ~3 gün kesintisiz |
| mühür hedefi | ~12 Kasım · teslim 19 Aralık 2026 |

## 2 · Neden bu yön (K-168, koddan doğrulandı)

1. **Ölçek:** 1:50 ölçek modelinin gerçek karşılığı 90 km alan · 1–6 km irtifa · 2,5 W telsiz · ~80 mW karıştırıcı; yayılım gecikmesi ihmal edilmiş (gerçekte slottan uzun). Küçük bir taktik sürü değil, tutarlı bir 802.11 sistemi de değil.
2. **İşlem kazancı yok:** SINR doğrudan Eb/N0 → alım eşiği 16 dB (gerçek 802.11b birkaç dB) → girişim menzili iletimin 6,3 katı → 1800 m'lik alan tek çarpışma alanı. Li replikasyonundaki farkın bir kısmı bundan olabilir.
3. **ED-CCA yok:** taşıyıcı dinleme geometrik; sürekli gürültü karıştırıcısı vericiyi hiç durdurmuyor — sahadaki "kanal erişimini kilitleme" etkisi yok.
4. **Radyo:** sabit 2 Mb/s, hız uyarlaması yok; yeniden deneme sınırı 4 (standartta 7).
5. **Karıştırıcı:** hızlı sönümleme yok; "yer" karıştırıcıları 70 m'de, yer–hava kanalı yok; reaktif karıştırıcı menzilsiz duyuyor; aldatıcının sahte önbelgesi alıcıyı kilitlemiyor.
6. **Gözlem penceresi gerçek telsizden fakir:** RSSI, kulak misafiri dinleme, kendi konumu, PHY hatası, kanal doluluğu yok.
7. **Senaryolar:** enerji, düğüm kaybı, trafik yoğunluğu yok.
8. **DESPARETE:** karıştırmaya özgü kanıt yok (temkin yalnız kalite eğilimi ya da belirsizlikten); PROTECT (çok yol, çoğaltma) kapalı; taslaktaki C_jam, pasif dinleme, hızdan bağ ömrü uygulanmadı.
9. **Özgünlük:** "ns-3/OMNeT++ gerçek fiziği yapamaz" doğru değil. Doğru iddia: taktik İHA karıştırmasına özel, sızıntısız gözlem sözleşmeli, kâhin referanslı, ön-kayıtlı, doğrulanmış (Bianchi, Li, yayımlanmış PER eğrileri) açık bir deney düzeneği + protokol + taban protokollerin ölçümü.

**Öğrencinin kararları (25 Eylül):** 802.11b korunur, eksikleri kapatılır · 1:1 kaynaklı taktik sürü · kendi konumu küçük GPS/INS hatasıyla (GPS karıştırması kapsam dışı) · yazım paralel · dürüst özgünlük + yayın karşılaştırması · enerji, düğüm kaybı, tıkanıklık: mantıklı olan · tasarım paketinin üretimi belgelenir.

---

## 3 · Fazlar

### Faz 0 · Referans gerçek dünya — 26 Eyl–1 Eki ✅ (K-169, K-170)

| # | iş | çıktı / kapı |
|---|---|---|
| 0.1 | **Kaynaklar** [indirme]: IEEE 802.11-2016 DSSS/HR-DSSS PHY (CCA modları, ED eşiği, duyarlılık, zamanlama, kısa yeniden deneme 7) · ns-3 `DsssErrorRateModel` ve doğrulaması · taktik İHA mesh telsizlerinin veri sayfaları · hava–hava kanal ölçümleri (Rician K; `02` S1) · yer–hava kanalı (Al-Hourani 2014) · EH/karıştırıcı güçleri ve konuşlanması (S3) · telemetri hızı/boyu (S4) · Babel RFC 8966 (S6) | her kaynak `02`ye künyesiyle; indirilen belge depoya girmeden tamamı okunur · 🟡 25 Eylül: beşi alındı ve denetlendi (`02` G1–G5: ns-3 802.11b doğrulaması, IEEE DSSS eğitimi, RFC 8966, MAVLink, karıştırma taraması); bekleyenler `14` §10 d–h |
| 0.2 | **Referans dünya belgesi** `v2/14-REFERANS-DUNYA.md`: telsiz (güç, anten, duyarlılık, hızlar), sürü (N, alan, irtifa, hız, formasyon), karıştırıcı (EIRP, platform, mesafe, sınıf), trafik — gerçek birimlerle, her sayı kaynağıyla ya da gerekçesiyle | 🟢 **onaylandı** (25 Eylül, K-169; bağ bütçesi `arsiv/teshis/referans_dunya_2026-09-25/bag_butcesi.py`) · kaynaklar G1–G9; bekleyen: IEEE 802.11-2020 (S2) · Goddemeier & Wietfeld 2015 (S1) |
| 0.3 | **Yapı anlatımı** — Faz 1–3'ün `sim2/` değişiklikleri tek paket (kimlik ve PDR yönü dâhil; eski İ-1) | 🟢 onaylandı: `v2/15-GERCEKCILIK-YAPI-PAKETI.md` (K-170) → Faz 1 başlar |

### Faz 1 · Fizik ve MAC gerçekçiliği [yapı] — 2–9 Eki ✅ 26 Eylül (A1…A8: K-171…K-181)

| # | iş | kapı |
|---|---|---|
| 1a | **Ölçek 1:1** — geometri ve hızlar gerçek birimlerde; verici gücü kaynaktan, menzil sonuç; `iletim_menzili_m` adı düzelir (eski A6) | bağ bütçesi testi: veri sayfası duyarlılığıyla menzil |
| 1b | **DSSS işlem kazancı** — gürültü 22 MHz'de, Eb/N0 = SINR · (11 Mchip/s / bit hızı); tek PER gövdesi korunur | PER–SNR eğrileri yayımlanmış sonuçlarla ve ns-3'ün modeliyle örtüşür |
| 1c | **Güce dayalı taşıyıcı dinleme + ED-CCA** (CCA modu 3: önbelge sezme ya da enerji ≥ ED eşiği; karıştırıcı enerjisi dâhil) — mevcut `Girisim.kanal_mesgul_mu` çekirdek; `cca_s` kullanılır; karıştırıcı açılış anlarında donma | sürekli karıştırıcı yanında verici erteler (analitik sınav) · Bianchi ±%15 |
| 1d | **Hız uyarlaması** 1/2/5,5/11 Mb/s — kaynaklı basit kural, bütün protokollerde aynı MAC; hız hesabı yalnız `cerceve_kur`'da | tek bağda SINR'a göre hız |
| 1e | **Zamanlama** — yayılım gecikmesi · kısa yeniden deneme sınırı 7 (eski İ-8d) · ACK zaman aşımı | birim sınavları |
| 1f | **Karıştırıcı** — hızlı sönümleme · yer karıştırıcısı yerde + yer–hava kanalı · reaktif karıştırıcıya duyma menzili ve kayıtlı algılama olasılığı · aldatıcı çerçeve alıcıyı kilitler · güçler EIRP kaynaktan | sınıf başına birim sınavı |
| 1g | **Sonuç satırı** — `kosu_kimligi` (tedavi + protokol parmak izi) · PDR telemetri/komut ayrımı · politika düşme sebebi · regresyonda gerçek protokol vakaları ✅ K-171 · varsayılan desen kuralı (eski İ-1, A8 — dünya değişimi adımında) | "farklı koşu → farklı kimlik" testi ✅ |

Her yeni sabit köken defterine kovasıyla; `kapsam.py`nin modellenmeyenler listesi güncellenir (eski İ-19, A23).

### Faz 2 · Gözlem sözleşmesi v2 — gerçek telsiz ve otopilot ne veriyorsa [yapı] — 7–12 Eki ✅ 26 Eylül (B1…B4: K-172, K-179, K-180)

- Alınan her çerçevenin **RSSI**'ı (kaynaklı ölçüm hatasıyla) ve gürültü ölçümü.
- **PHY hata sayacı:** sezilen ama CRC'den geçmeyen çerçeveler.
- **Kanal doluluk oranı:** CCA'nın meşgul olduğu sürenin payı.
- **Kulak misafiri dinleme:** başkasına giden ama çözülen çerçevelerin başlığı ve protokol başlığı, isteğe bağlı yeni bir kancayla.
- **Kendi konumu, hızı, yönü** (GPS/INS, metre mertebesi hata). Komşunun konumu yine yalnız bedeli ödenmiş mesajla.
- `v2/05` yeniden yazılır: her alan için "gerçek telsiz/otopilot bunu verir mi" + kaynak. Yüzey testi yeni sayılara; sızıntı ve içe aktarma testleri korunur.

### Faz 3 · Senaryo eksenleri — Faz 2 ile paralel [yapı] ✅ 26 Eylül (C: K-180, K-182)

- **Düğüm kaybı** — İHA'lar belli anlarda düşer (vurulma, arıza); korunum defterine "ölü düğümde kalan" kalemi.
- **Trafik yoğunluğu ekseni** — tıkanıklık karıştırmadan ayrı ölçülür.
- **Enerji** — telsiz enerjisi = gönderim/alım/boşta süreleri × kaynaklı güçler. Raporlanır, tasarım ölçütü değil (İHA'da itki enerjisinin yanında küçük).
- **Mod metrikleri** — postür geçiş sayısı, karıştırıcısız kolda "yanlış kriz" süresi · `algilama_duyarliligi`nin ikiye bölünmesi (eski İ-23).

### Faz 4 · Yeniden kalibrasyon ve doğrulama [süre] — 12–19 Eki 🟡 26 Eylül'den beri: 4.1 ✅ · 4.2 ✅ · 4.3 yere toplama ✅ eşler arası ⏳ · 4.4–4.5 ⏳ (K-182…K-191)

| # | iş |
|---|---|
| 4.1 | **Çalışma noktası** — N, alan, derece, geçide derinlik (C1 ölçütleriyle) · karıştırıcı: güç kaynaktan, "kısmi karıştırma" rejimi konum/mesafeyle · yük (C3) · Θ kolları (C4) · görev kolu (C5, 🟦 ana deneye girecekse) · ısınma × pencere taraması (C6) · bölünme tablosu (eski İ-13…İ-15, İ-20) |
| 4.2 | **Doğrulama** — Bianchi · Li yeniden (öngörü önceden: işlem kazancıyla girişim/iletim oranı düşer, H1 banda yaklaşır) · PER eğrileri yayınla · ED-CCA sınavı · kâhin tavanı |
| 4.3 | **Taban protokoller** — U1 eşler arası + yere toplama (aletine `--desen`; eski İ-7) · adillik: RREP-ACK/kara liste (asimetri artık fiziksel), rota tamponu (eski İ-8) · AOMDV U2/U4 eşlemesi · M4 boş kol kapısı (eski İ-9, İ-10) → **taban protokoller DONAR** |
| 4.4 | **SINANMAMIŞ ve borç** — kaynağa bağlananlar kapanır; kalanlar ölçülür ya da eksen ilan edilir 🟦 (eski İ-16, İ-17) |
| 4.5 | Yeni regresyon tabanı · doğrulama listesinin tamamı bir kez · iş başına koşu süresi ölçülür (bütçe) |

### Faz 5 · DESPARETE — karıştırmayı gerçekten çözen protokol — 19 Eki–8 Kas

| # | mekanizma | ne çözer |
|---|---|---|
| 5.0 | **Kayıp anatomisi** — birincil hücre + yer karıştırıcılı bir aile; taban protokoller, kâhinler, v0.4: paket nerede, neden ölüyor (alıcı karıştırması, kanal erişim kilidi, bayat rota, tampon); kâhin − protokol = körlüğün bedeli | hedefleri ölçümle koyar |
| 5.1 | **Karıştırma kanıtı (taslaktaki C_jam)** — komşu başına RSSI eğilimi × teslim tutarlılığı (güçlü sinyal + düşük teslim = girişim), kendi kanal doluluğu, PHY hata oranı, gürültü; komşununki ilanda, bedeli ödenerek → risk terimi H. "Karıştırıcı tespiti" iddiası yok | karıştırılan bağdan kopmadan önce kaçmak |
| 5.2 | **Öngörülü kaçınma** — kendi ve komşu konum/hızı → bağ ömrü tahmini → komşu zaman aşımı ve maliyet (taslak §6) | hareketle kopan bağı önceden bırakmak |
| 5.3 | **Kanıta dayalı postür** — CAUTION/PROTECT karıştırma kanıtıyla; belirsizlik tek başına tetiklemez; histerezis; yanlış kriz oranı ölçülür (eski KR-6) | savunmacı modun doğru anda açılması |
| 5.4 | **PROTECT = seçici çok yol + çoğaltma** [yapı] — ilk atlaması farklı güvenli ardıllara sınırlı bütçeyle kopya; hedefte `(kaynak, kaynak_sira)` ile tekilleştirme; simülatörde kopya ve korunum kalemi | ani bağ kaybında paketi kurtarmak (taslağın CRISIS'i) |
| 5.5 | **Pasif bakım** — kulak misafiri + DATA'da potansiyel/DFSN (taslak §6); kanca `cerceve_duyuldu` hazır (K-172) | PROBE yükü ve bayat bilgi |
| 5.6 | **Canlılık ve yük** — periyodik DFSN (eski KR-5) · FIELD_SOLICIT'in akıbeti (KR-7) · nitelik PROBE'u = ilk M0.1 örneği (KR-8) · onarım kotası, belirsizlik eşiği (eski İ-3) · DESPARETE sabitleri köken defterine (D-5) | kontrol yükü, canlılık |
| 5.7 | **Kapanış** — profil v0.5 dondurulur · resmi U1 + U3 (eski İ-4, İ-6) · tasarım paketi güncellenir ve üretim süreci belgelenir 🟦 (eski İ-5) | Aşama 3'ün çıkışı |

Her mekanizma: ablasyon bayrağı · önceden yazılı beklenti · geliştirme tohumları 1003–1010 · 350 s · birincil hücre + bir yer karıştırıcılı aile · tam takım.

### Faz 6 · Ön-kayıt, analiz, mühür — 5–12 Kas

- δ için gürültü ölçümü (3 taban × 20 tohum 1100–1119, birincil hücre) [süre] · güç benzetimi üç koşulla (O-9) · tohum sayısı (eski İ-26, İ-27).
- Ön-kayıt: birincil metrik 🟦 KR-2 · Aile 1 hipotezleri ve AOMDV öngörüsü 🟦 · Aile 3 kolları (5.1–5.5 dâhil) 🟦 · çekirdek matris + bütçe 🟦 · durdurma kuralı · hareketli karıştırıcıda evre tanımı · PSR'nin yeri (eski İ-12, İ-21, İ-22, İ-28).
- `analiz/` katmanı: Wilcoxon, Holm, GA, NaN kapısı, kimlik denetimi (eski İ-29).
- Doğrulama listesi → 🔒 **mühür (~12 Kasım)** (eski İ-30 … İ-32).

### Faz 7 · Ana deney ve paralel yazım — 12 Kas–19 Ara

- **Ana deney** 12–26 Kasım: birincil hücre + Aile 1 hücreleri + Aile 3 kolları; keşifsel eksenler bütçeye göre, az tohumla (eski İ-33 … İ-35).
- **Yazım** Kasım başında başlar: giriş, literatür, yöntem, referans dünya, simülatör ve doğrulaması, taban protokoller, DESPARETE tasarımı. Sonuç bölümleri 26 Kasım–10 Aralık; son düzen 10–19 Aralık.
- Görselleştirme (iz kanalı, Y8) ana deney koşarken · beyanlar (sapmalar, R5–R7, kapsam dışı) · fikir sahipliği: kayıt + ablasyonla ölçülmüş katkı + tasarım paketinin üretim süreci · öğrenme rehberi ve jüri soru bankası · TÜBİTAK biçim gereklilikleri (eski İ-24, İ-25, İ-36 … İ-41).

### Sürekli

Kanıtın depoya alınması (teşhis betikleri, `kayit_indeksi.py` → `kalibrasyon/`) · git hijyeni [öğrenci]: izlenen `.pyc`'ler, `.gitattributes`, iş başına commit, beklentileri koşudan önce commit · README iddiaları · her işten sonra `12`, `DEVIR`, `04` (eski İ-42 … İ-45).

---

## 4 · Öğrenci kararları

| # | karar | ne zaman | durum |
|---|---|---|---|
| — | yön: önce gerçekçilik ve DESPARETE'nin karıştırmayı çözmesi · 802.11b + eksikler · 1:1 · kendi konumu · yazım paralel · dürüst özgünlük | 25 Eylül | 🟢 verildi (K-168) |
| KR-A | referans dünya belgesi (0.2) | Faz 0 sonu | 🟢 onaylandı (25 Eylül, K-169) |
| KR-B | `sim2/` yapı paketi (0.3) | Faz 0 sonu | 🟢 onaylandı (25 Eylül, K-170) — regresyon izni ve üç sayı dâhil |
| KR-C | kaynak indirmeleri (0.1) — her biri ayrı | Faz 0 | 🟢 G1–G13 (25 Eylül); ücretli iki kaynağın yerine açık taramalar ve uygulama kaynakları (K-170) |
| KR-1 | kâhin kuralının okuması (aşım = inceleme, otomatik ret değil) | Faz 4'ün U1'lerinden önce | ✅ K-192 (28 Eylül): zarf prosedürü (`06` §4.4) · U1 eşiği referans dünyada değişmez · tasarım bedeli açıklamadır |
| KR-2 | birincil metrikte komutlar (öneri: birincil telemetri, bütün trafik ikincil) — alanlar satırda (`pdr_telemetri` · `pdr_komut`, K-171); DESPARETE v0.1 komut taşımadığı için birleşik PDR'si telemetrininkinden düşük | Faz 6 | ⏳ |
| KR-D | 5.3 · 5.4 · 5.6'nın tasarım paketine yansıması (tasarım senin) | Faz 5 | ⏳ |
| KR-E | düğüm kaybı ekseninde birincil metrik — üretilen pakete göre PDR kaybı cezalandırmıyordu (K-180) | Faz 6 | ✅ K-182 (öğrenci ajana bıraktı): PDR kohortu doğumda iki ucu yaşayan paketler; `gorev_teslim_orani` ikincil |
| KR-12 … KR-20 | borçluların eksen ilanı · Aile 1 hipotezleri · Aile 3 kolları · çekirdek matris · keşifsel eksenler · görev kolu · PSR · kanıt dizini · mühür tarihi | Faz 4–6 | ⏳ (tam metin arşivdeki ayrıntılı sürüm §9) |

Eski KR-3 (v0.4'ün eski dünyada doğrulanması) ve KR-4 (yapı paketinin kapsamı) bu planla kapandı: doğrulama yeni dünyada (5.0), yapı paketi KR-B.

## 5 · Hesap bütçesi

Eski dünyanın iş süreleri (`python arsiv/teshis/belge_guncelleme_2026-09-25/u1_sureler.py`: hareketli iş 55–118 dk, kâhin 28–49 dk) yeni dünyada geçerli değil. Faz 4.5'te yeniden ölçülür; mühürde bütçe ve çekirdek matris buna göre yazılır. Kaba beklenti: mühürden önce ~50–80 sa, ana deney ~5–8 gün kesintisiz makine süresi.

## 6 · Riskler ve kayma

- **Faz 1–2 şişerse:** önce hız uyarlaması ve yer–hava kanalı ertelenir ve beyan edilir. 1:1 ölçek, işlem kazancı, ED-CCA, RSSI ve kulak misafiri korunur.
- **Yeni dünya yönlendirmeye iş bırakmazsa** (ağ tek atlamaya iner): alan ve N kaynaklı sürü geometrisi içinde ayarlanır, öğrenciye sorulur.
- **Mekanizmalar kazanç göstermezse:** dürüst negatif sonuç; neden çalışmadığı ölçülür.
- **Takvim:** Aralık başında ~1 hafta tampon. Düşme sırası: keşifsel eksenler → iz kanalının zengin gösterimi → Aile 3 kol sayısı → çekirdek hücre sayısı. Korunanlar: birincil hücre, üç taban protokol, DESPARETE, 40 tohum.

## 7 · Gelecek çalışma olarak beyan edilecekler

Komutların yönlendirilmesi (talep yolunda alan · ters ağaç) · hedef alanı emekliliği · iki geçit · ~2 000 s'lik uzun koşu · protokol farkında (kontrol kanalını hedefleyen) karıştırıcı · GPS karıştırması ve aldatması · RTS/CTS · OFDM telsizler · derin öğrenme · GPSR · gerçek RF/SDR/uçuş testi.
