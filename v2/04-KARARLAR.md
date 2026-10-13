# 04 · GEÇERLİ KARARLAR

> Bugün geçerli kararlar, konu konu. Yazılı değilse verilmemiştir. Bir kararın nasıl ve neden verildiği, kodda geçen `K-xxx` atıfları ve eski dünyanın (1:50) kararları: `kayit/KARAR-GUNLUGU.md`. Kod ile bu belge çelişirse hangisinin yanlış olduğu ölçülerek bulunur.
> Güncel: 13 Ekim 2026; önceki sürümler `arsiv/04-KARARLAR-*.md`.

## 1 · Proje ve kapsam

- **Soru:** karıştırma altındaki taktik İHA sürüsünde yönlendirme. Ürün, bu çalışmada önerilen DESPARETE protokolüdür. Taban protokollerin karıştırma altındaki ölçümü ikinci, bağımsız katkıdır (`01`).
- **Kıyas tabanı:** AODV ve OLSRv2 (K-229). Üçüncü rakip açık karar (K-240, §10): JarmRout kodlandı ve dondu, ama kesin taban protokol değildir.
- **Yön (K-168):** önce gerçekçilik (1:1, kaynaklı taktik sürü; gözlem = gerçek telsiz ve otopilotun verdiği), sonra DESPARETE'nin karıştırma altındaki başarımı. Bir ölçütle gerçekçilik çatışırsa gerçekçi olan seçilir (K-185).
- **Kapsam dışı:** gerçek RF/SDR/uçuş · frekans çevikliği ve çoklu kanal (öncül: çözüm yönlendirmede) · GPSR · derin öğrenme (SWaP) · GPS karıştırması · RTS/CTS · protokol farkında karıştırıcı · içeriden saldırılar (seçici iletim, kara delik, sahte rota; K-230) · ~2 000 s'lik uzun koşu (`12` §5).
- **Negatif sonuç** raporlanır; önceden ilan edilen bir yanlışlanma tetiklenirse sonuç teşhis edilmiş bir negatif sonuçtur.

## 2 · Referans dünya — deneylerin dünyası (`14`, K-169…K-181, K-185…K-188)

- `sim2/kanal/dunya.py::referans_2026()` bütün gerçekçilik anahtarlarını açar. **`Konfig()` varsayılanı eski 1:50 dünyadır** (eski regresyon vakaları onunla birebir). Araçlar dünyayı `kalibrasyon/dunya_secimi` üzerinden seçer (`--dunya referans_2026` ya da `DESPARETE_DUNYA`); bir AST testi bunu zorlar (K-183).
- **Telsiz:**
  - 802.11b DSSS, kanal 6, 22 MHz · EIRP 20 dBm (serbest uzayda güç yalnız mesafeyi ölçekler: taktik telsiz gücündeki daha geniş bir sürünün ölçekli karşılığı, K-230) · dipol 2,15 dBi.
  - İşlem kazancı (Eb/N0 = SNR·B/R) · ARF hız uyarlaması 1/2/5,5/11 Mb/s (ns-3) · güce dayalı taşıyıcı dinleme + ED-CCA −76 dBm, 15 µs · yayılım gecikmesi.
  - En çok 7 iletim denemesi (6 yeniden deneme; dot11ShortRetryLimit, K-223) · CW 31/1023 · veri onayı yalnız gönderen çözdüyse (K-115) · veri paketinin IP TTL'i 64 (RFC 1700, ns-3; K-215).
- **Kanal:**
  - Serbest uzay α = 2 · gölgeleme σ 3 dB, hücre 2,5 km · yer–hava kanalı Al-Hourani (banliyö).
  - Rician K 10 dB — **eksen** (K-215): birincil test 10 dB'de, 6 ve 15 dB'de keşifsel tekrar.
  - Sönümleme durumsuz FIR, referans dünyada blok üreteciyle (K-198); statik kolda bağ başına donuk tek çekim.
- **Sürü:** N = 40 · alan 33 km (K-188) · irtifa 50–300 m · 40–120 km/h · dört hareket kolu (statik · bağımsız · görev · formasyon) · kendi konumu GPS/INS 1,5 m CEP.
- **Trafik:** yere toplama birincildir: her düğümden geçide 1 pkt/s × 512 B telemetri + geçitten 4 düğüme 0,25 pkt/s komut (K-126). Eşler arası keşifseldir. Araç deseni açıkça vermeli (`Konfig` varsayılanı `esler_arasi`).
- **Senaryo eksenleri:** düğüm kaybı (birincil metrikte kohort: doğumda iki ucu yaşayan paketler, K-182) · trafik yoğunluğu · telsiz enerjisi (raporlanır, tasarım ölçütü değil).
- **Ölçüm penceresi:** ısınma 50 s · ölçüm bitişi 320 s (trafik üretimi burada durur) · koşu bitişi 350 s. Duyarlılığı Faz 6'da ölçülür (§10).

## 3 · Tehdit ve birincil hücre

- **Sınıflar:** sürekli · darbeli · reaktif · aldatıcı · taramalı.
- **Aileler:** tekli merkez · cephe hattı · derin sızma · hedef koruma · hava eşlik; her ailede toplam ortalama güç eşit, referans taban 10 W (K-186).
- **Rejim sınırı:** onlarca watt'lık karıştırıcı sürünün tamamını karartır; orada yönlendirme teslimi kurtaramaz. Birincil hücre, etki alanı sürüden küçük "kısmi karıştırma" rejiminde kurulur (`14` §4).
- **Birincil hücre (K-186, K-192):** `formasyon · yere_toplama · derin_sizma · sürekli`, 10 W.
  - Araç yalnız sessizken taşınır; ölçüm penceresinde ~1,3 km yol alır, fiilen merkezdedir.
  - Çizelge: 15 s açık · 15 s sessiz; açıkken 20 W.
  - Sınanan: periyodik açılıp kapanmaya zamansal uyum ve kısmi karıştırmada dolaşma.
- **Hava karıştırıcısı** (1–5 W) sürüyü böldüğü için birincil değil, keşifsel eksendir.

## 4 · Protokolün gördüğü ve yapabildiği

- **Gözlem sözleşmesi (`05`):** protokol yalnız gerçek bir telsizin ve otopilotun verebileceğini görür: RSSI, gürültü, kanal doluluğu, PHY hatası, kulak misafiri çerçeveler, kendi konum/hız. Karıştırıcıyı, gerçek bağ kalitesini ve topolojiyi göremez. Yüzey 30 alan; sızıntı testle kapalı.
- **Kontrol düzlemi (`13`):** protokol çağırmaz, niyet döndürür; her kontrol baytı kanalda ödenir; unicast sonucu ve iletim başarısızlığı kancalarla bildirilir.
- **Bekleme tamponu** simülatördedir ve herkes için ortaktır: 64 paket · 30 s, taşmada en eski düşer (ns-3 AODV ile aynı, K-198). Birincil hücrede bağlamıyor: 256 paket ve 60 s birebir aynı sonucu verdi (K-200).
- **Uçtan uca kopya (K-231):** protokol gönderdiği paketin eşlerini başka komşulara da yollayabilir (`13` §07). Hedefte ilk varan teslim sayılır; eşlerin yayın süresi veri yüküdür.
- **Kaynak rotası (K-232):** DSR ailesi için paket başlığında ara düğümler; adres başına 4 bayt çerçeveye ve yönlendirme ek yüküne sayılır (`13` §07).
- **Kâhin bilgisi hiçbir protokol kararına girmez.** Kâhinler yalnız ölçüm aleti ve referanstır.
- **Gürültü gözlemi protokol kararına girmez (K-227):** simülatörde anlık ve hatasızdır; gerçek sürücü onu 30 s'de bir, 5 ölçümün ortancasıyla ve kırparak verir (`02` G18). Mimari denetimi okunmasını engeller. Karıştırma kanıtı kanal doluluğu, PHY hatası, MAC sonucu ve RSSI'den kurulur.

## 5 · Taban protokoller — donmuş: `AODV-j` · `OLSRv2-b` · `JarmRout-b` (K-239)

**Ortak kurallar:**
- Kaynağına sadık kurulur; parametreler RFC ya da makale varsayılanıdır, hiçbiri senaryoya göre ayarlanmaz.
- Her protokol kendi HELLO'sunu kullanır; HELLO aralıkları eşitlenmez (`06` §4.2).
- SHOULD uygulanır, MAY beyan edilir. Sapmalar ve modellenmeyen özellikler her protokolün beyan tablosunda gerekçesiyle durur (`protokoller/*_bicim.py`); gerekçesiz sapma düzeltilir.
- Kod `tests2/test_donma.py`ye bağlıdır. Bir dosya değişirse yeni K kaydı, U1 ve regresyon gerekir. `OLSR-d` ve `AOMDV-f`nin dosyaları eski regresyon vakaları için bağlı kalır; rakip değildirler (K-229).

**AODV (RFC 3561), `AODV-j`:**
- Kural kural sadakat denetiminden geçti (K-208, `arsiv/teshis/aodv_sadakat_2026-09-30/denetim.md`). RFC birincil kaynaktır; ns-3 yalnız RFC'nin sustuğu ya da çeliştiği yerde hakemdir (§6.1–§6.6.1 çelişkisinde §6.6.1). ns-3'ün RFC dışı eklemeleri alınmadı.
- Başlangıç durumu −∞ (K-215).
- Beyanlı sapmalar: yerel onarım §6.12 (MAY) · RREP-ACK mesajı yerine bağ katmanı onaylı kara liste (K-194) · karşılıksız RREP · önceki atlama ömrü · RERR hep yayın · TTL yükte.
- RERR durum (ii) öncül süzmesizdir (RFC'nin süzme cümlesi normatif değil; ns-2/ns-3 ile aynı; K-210).
- RFC'nin kendi kurallarından doğan geçici döngüler protokolün mekanizmasıdır (K-207).

**OLSRv2 (RFC 7181), `OLSRv2-b`:**
- Kapsam: NHDP (RFC 6130) + bağ metriği DAT (RFC 7779); tel biçimi RFC 5444 bayt bayt (RFC 6130 Ek B'nin örnekleri birebir).
- olsrd2 yalnız RFC'nin seçeneğe bıraktığı yerde hakemdir.
- Sadakat denetimi `arsiv/teshis/olsrv2_sadakat_2026-10-11/denetim.md` (K-235, K-236): gerekçesiz sapma yok. RFC metninin iki iç tutarsızlığı (§18.5'in d2'si, Ek C.7'nin metriği) normatif bağlamla çözüldü.
- Bayrak MPR'leri atlama sayısıyla (§18.4 B), yönlendirme MPR'leri ve rotalar metrikle.
- Bütünlük koruması (RFC 7183) kullanılmaz: tehdit modelinde mesaj sahteciliği yok.
- DAT'ın gelen hızı sabittir (RFC 7779 §8).
- U1 iki desende temiz; evre kapılarını geçti.

**JarmRout (Pu 2018), `JarmRout-b` — kesin taban protokol değil (K-240):**
- Kaynak sırası: makale harfiyen → makalenin sustuğu yerde DSR (RFC 4728) → ikisinin de sustuğu yerde gerekçeli seçim. Makalenin dört çözümlü örneği (Tablo 1–3, Şekil 3) birim testinde birebir.
- Eş. 8'in katsayıları Tablo 2'den (γ 0,5 · ε 0,02); Eş. 13'ün mekânsal terimi e^(1/Υ).
- Beyanlı sapma: NAV yerine CCA meşgul süresi (RTS/CTS yok). Seçimler: `t_wait` 0,1 s ve Eş. 6–7 süzgeçleri 0,5; duyarlılıkları mühürden önce ölçülür.
- Kural kural sadakat denetimi: `arsiv/teshis/jarmrout_sadakat_2026-10-11/denetim.md` (K-234).
- **Ölçek sınırı (K-238):** makalenin yinelenen RREQ kuralı (Şekil 4, birebir) toplu akışta tıkanıklık çöküşü üretir. Aynı ağda 1–10 akışta PDR ≈ 1,00, 20 akışta 0,65; yere toplamada U1 oranı 0,30–0,55. Makale tek kaynakla değerlendirilmiş (`arsiv/teshis/jarmrout_sel_2026-10-12/inceleme.md`).
- U1'in 16 düşük hücresi bu mekanizmayla açıklandı; eşler arasındaki iki kâhin aşımı kayıtlı (K-239).
- **Evre metrikleri yorumlanamaz (K-239):** karıştırıcısız kolda PDR durağan değil (eğilim, pencere sonu boşalması). Gecikme kuyruğu rota beklemesidir (p99 28–30 s > açık süre 15 s). Evre kapılarında kayıtlı muafiyeti var; `PDR_açık`ı "bulanık" etiketiyle raporlanır.

**U1 — kabul kapısı (K-136, K-137, K-192, K-238):**
- Oran = PDR(protokol) / PDR(ETX kâhini), aynı konfig, tüm koşu PDR'si. Eşik: statik ≥ 0,90 · hareketli ≥ 0,60.
- **U1-U** uygunluk kapısıdır (keşif, çok atlamalı teslim, korunum, kâhin aşılmıyor); kalırsa protokol kabul edilmez.
- **U1-B** başarım bulgusudur: eşik altı hücre ölçümle açıklanır, kusur izleri dışlanır. Kaynağına sadık bir protokolün eşik altı kalması protokolün kendi sınırıdır (K-207).
- **Kâhin aşımı** otomatik ret değildir. Çözünürlükten (R) küçükse kayıt yeter. Büyükse üç kâhinin zarfına bakılır (K-192); kopya gönderen protokolde kopya kuralı uygulanır: yalnız kopyayla teslim edilenler çıkarılınca oran ≤ 1 + R (K-238). İkisi de tutmazsa sızıntı ya da yazılım hatası aranır.

## 6 · DESPARETE

- Bağlayıcı olan bugünkü koddur (`protokoller/desparete*.py`). İlk tasarım taslağı (v0.1, 22 Eylül) bayattır ve arşivdedir: `arsiv/DESPARETE_TASARIM_PAKETI_v0.1_2026-09-22/`. Kod yorumlarındaki `protokol_kaynaklari/DESPARETE_TASARIM_PAKETI/` yolları bu klasörü gösterir.
- **Bugünkü kod hâli v0.4.1:** bayrak profili `PROFIL_V02` (yalın) + `SECENEK_V041` (V1 · V5 · V7 · V8 · V10 · V11 komut geri izi). Sekiz ablasyon bayrağı; güvenlik değişmezleri bayrakla kapanmaz (K-159…K-172).
- **Komutlar:** DESPARETE yalnız geçit alanı kurar; komut V11 geri iziyle taşınır; trafik herkes için aynıdır (K-160, K-172).
- **Birincil hücrede ölçüm — Faz 5.0** (K-228; tohum 1003–1006, ana deney değil): `PDR_açık` DESPARETE 0,551 · AODV 0,444 · kâhin 0,780.
  - Karıştırmaya özgü kayıp (doğum evresine göre açık − önce): DESPARETE −0,204 · AODV −0,138 · kâhin −0,134.
  - v0.4.1'in AODV'ye üstünlüğü karıştırmadan bağımsızdır; karıştırıcı açılınca DESPARETE daha çok kaybeder.
  - Fazla kaybın tamamı "rota yok" (`rota_gecersiz`): ardılı karıştırılan alan onarıma girer. Paket kota (%52) ya da ulaşılamaz alan (%48, girişi çoğunlukla açlık) yüzünden düşer; çoğu karıştırıcıdan uzak rölelerdedir.
- **Faz 5'in sırası (K-228):**
  1. Yedek ardıl (5.4'ün çoğaltmasız kısmı): önceden doğrulanmış ikinci uygulanabilir ardıl; ardıl kopunca onarıma girmeden geçiş. Aynı A/B'de ayrı bayrakla açlıkta tur isteği.
  2. 5.1: karıştırma kanıtıyla erken geçiş.
  3. 5.3 (postür) ve 5.4'ün çoğaltması.
- **Faz 5'in konusu olan eksikler:** karıştırmaya özgü kanıt · öngörülü kaçınma · kanıta dayalı postür · PROTECT'in çok yolu ve çoğaltması · pasif dinleme (`12` Faz 5).

## 7 · Ölçüm

- **Metrikler üçlü sunulur:** teslim · gecikme · kontrol yükü; tek metrikle sıralama yok.
- **Birincil metrik `PDR_açık`** (K-222): karıştırıcının açık dönemlerinde doğan paketlerin teslim oranı. Pencere PDR'si (ölçüm penceresinde doğan paketler) betimleyicidir.
- **Gecikme** ortak alt küme üzerinden raporlanır. **Kontrol yükü** bayt ve kanal süresiyle ölçülür; protokolün veri başlığı dâhildir (K-151).
- **Evre metrikleri (`08`):** şok derinliği · toparlanma tamlığı · toparlanma süresi · tespit gecikmesi. Hata payı kümelenmeye dayanıklıdır; tespitin boş dağılımı negatif binomdur (K-196). Kapıları geçmeyen protokol kayıtlı muafiyetle etiketlenir (K-239).
- **Temas kaybı (betimleyici, K-230):** İHA başına telemetrinin T s'den uzun gelmediği aralıkların toplamı · temas kaybı yaşayan İHA sayısı. Tanımı ve T (otopilot kaynağından) mühürden önce yazılır.
- **Kâhinler:** ETX kâhini (U1 paydası) kesin tavan değildir; üst referans üç kâhinin tohum başına zarfıdır (K-110). Kâhin grafiği karıştırıcının açık/sessiz çizelgesini görür (K-195). Kâhin ile protokol arasındaki fark, protokolün gözlem kısıtının bedelidir.
- **Kayıp anatomisi** (`kalibrasyon/kayip_anatomisi.py`): düşüş sebebi × karıştırıcı bölgesi (alıcıda) × açık/sessiz evre × bağ kalitesi bandı; Faz 5 hedefleri buradan çıkar. Bölge anlık güçle ve etki alanıyla (karıştırıcı açık olsaydı alınacak ortalama güç) okunur (K-202).
- **Çözünürlük:** eşleştirilmiş R = 0,0126 (K-224; birincil hücre, yakınsamış kâhin, 50 s'lik kısa pencere kesiti). Ana deneyin penceresinde Faz 6'da δ ölçümüyle yenilenir.

## 8 · Deney tasarımı ve istatistik (`06`)

- **Tohumlar** (`06` §2 tek kaynak): ana deney **2000–2039** (40 tohum) mühürden önce hiçbir protokolle koşulmaz. Geri kalan tohumlar geliştirme ve kalibrasyon içindir: U1 1000–1002 · Faz 5 1003–1010 · R 1000–1039 · duyarlılık 1000–1019 · δ gürültüsü 1100–1119.
- **Aileler:**
  - 1 · karakterizasyon (taban protokoller);
  - 2 · üstünlük (H2.x: DESPARETE ↔ her rakip, birincil hücrede `PDR_açık`, çift yönlü eşleştirilmiş Wilcoxon, Holm aile içinde);
  - 3 · mekanizma (ablasyon).
- **İkincil testler (K-222):** karıştırıcısız ikiz hücreyle fark-içinde-fark · dayanıklılık hücresi (10 s açık · 20 s sessiz).
- **Eşik:** δ = 2·SD_ref/√n; SD_ref taban protokol çiftlerinin en gürültülüsünden. DESPARETE'nin hiçbir koşusu δ'ya girmez.
- **"Üstün"** = Holm'dan sonra p < 0,05 **ve** fark ≥ δ **ve** mekanizma kapısı: karıştırmaya özgü mekanizmalar kapatılınca `PDR_açık` anlamlı düşmeli (K-153, K-222).
- **"Karıştırmaya özgü kazanç"** ancak ayrıca fark-içinde-fark anlamlı pozitifse söylenir (`06` §0.4.5).
- **Mühür** ~20 Kasım (`12` Faz 6): hipotezler, eşik değerleri, parametreler, tohum sayısı (güç analiziyle), birincil metrik.

## 9 · Yazılım altyapısı

- **Rastgelelik:** durum tutan kaynaklar ayrı sıralı akışlardadır; kanal rastgeleliği protokolden bağımsız hash alanlarındadır. Aynı tohumda her protokol aynı dünyayı görür (eşleştirme yapısal).
- **Korunum:** `üretilen = teslim + düşen + kuyrukta + uçuşta` her koşuda denetlenir (kopyada `13` §07); düşme sebepleri kapalı kümedir.
- **Köken defteri** (`sim2/yapilandirma/kokenler.py`, K-203): her parametre sekiz kovadan birindedir: TÜRETİLMİŞ · ÖLÇÜLMÜŞ · KAYNAK · DUYARSIZ · TEDAVİ · KOL TANIMI · DÜNYA TANIMI · SINANMAMIŞ. Gerekçeler referans dünyanın değerini anlatır. Mühürden önce SINANMAMIŞ = 0 ve duyarlılık borcu boş olmalı (ya da eksen/kapsam ilanı).
  - **DÜNYA TANIMI:** onaylanmış referans dünya tanımları ve birincil hücre (33 km, N 40, 40–120 km/h, 10 W …). Projenin kapsamıdır, duyarlılık borcu taşımaz.
  - **Sayımın tek yeri burasıdır.** Bugün **SINANMAMIŞ 5**: pencere üçlüsü (Faz 6) · `rssi_olcum_sigma_db` ve `gps_dikey_sigma_m` (JarmRout RSSI ve konum okuyor; K-233) · duyarlılık borcu 0.
  - **DUYARSIZ 9** (ölçülen |Δ| defterde) · `gm_hiz_sigma_ms` DUYARLI → DÜNYA TANIMI, ölçülen duyarlılığı raporda (K-225) · Rician K eksen (§2).
  - **Kapsam ilanı 13** (K-204, K-215, K-222): darbeli · reaktif · taramalı sabitleri, tekli merkezin konumu, hava eşlik hızı, görev müfreze sayısı, GM eğimi, görev kolu jitter'ı. Birincil hücrenin kod yoluna girmezler; o kolların sonucu bu değerlere koşulludur; rapor kapsam bölümünde yazılır.
  - **Kaynaksız DÜNYA TANIMI'lar** (ölçülen duyarlılıklarıyla raporda): gölgeleme hücresi · CBR titreşimi · istasyon tutma (K-220) · formasyon manevra gürültüsü (K-225) · komut akış sayısı (K-223).
  - **KAYNAK'a bağlananlar:** TTL 64 · kâhinin beacon'ı = AODV HELLO (84 B, 1 s) (K-215). Kâhinin sönümleme örneği 48 (K-215).
- **Sonuç satırı** kendi konfigini, kimliğini (kod özetleri dâhil), kapsam sınırlarını ve metrikleri yeniden üretecek ham veriyi taşır.
- **Regresyon** (`kalibrasyon/regresyon_satirlari.py`, taban `k236`, K-237) ve **mimari denetimi** davranış değiştiren her simülatör değişikliğinden sonra koşulur.

## 10 · Açık kararlar

| konu | gereken | ne zaman |
|---|---|---|
| **Üçüncü rakip (K-240).** JarmRout kesin değil: toplu akışta makalenin kuralıyla çöküyor (K-238), evre metrikleri yorumlanamıyor (K-239). Aranan özellikler: tanımı eksiksiz ve birincil kaynağı açık (RFC ya da tam algoritmik tanım), bilimsel olarak güvenilir, karıştırma bağlamında anlamlı, straw-man eleştirisine açık değil. Aday yoksa JarmRout bulgularıyla kalır ya da rakip sayısı ikiye iner | aday araştırması, ardından karar | mühürden önce, KR-3 ile birlikte |
| KR-3 · rakiplerin rolü ön-kayıtta: hangi hücrede hangi test birincil (K-229) | karar | mühür, DESPARETE yeni rakiplere karşı koşulmadan önce |
| KR-2 · birincil metrikte komutlar (öneri: birincil telemetri, bütün trafik ikincil) | karar | Faz 6 |
| DESPARETE'nin güncel tasarım belgesi (v0.1 paketi arşivde; Faz 5 mekanizmalarıyla birlikte yeniden yazılır) | yazım | Faz 5.7 |
| temas kaybı metriğinin tanımı ve T eşiği (otopilot kaynağı, K-230) | kaynak, ardından karar | mühür |
| pencere üçlüsü (ısınma · ölçüm bitişi · koşu bitişi): koşu uzunluğundan bağımsızlık, birincil hücrede, taban protokollerle. Trafik ölçüm bitişinde durduğu için uzun bekleyişli protokolde son doğumlar boşalan ağda teslim edilir (JarmRout'ta son 5 s'nin PDR'si 0,53 · 0,59; K-239) | ölçüm, ardından karar | Faz 6 |
| `06` H1.3'ün aldatıcı ↔ sürekli kontrastı referansta (10 W aldatıcı ED'yle ağı susturuyor, K-219) · Rician K ekseninin keşifsel tekrarı (6 · 15 dB) | öneri, ardından karar | Faz 6 |
