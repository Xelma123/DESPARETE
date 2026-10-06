# 04 · GEÇERLİ KARARLAR

> Bugün geçerli olan her karar burada, konu konu. Yazılı değilse verilmemiştir. Bir kararın nasıl ve neden verildiği, kodda geçen `K-xxx` atıfları ve eski dünyanın (1:50) kararları: `kayit/KARAR-GUNLUGU.md`. Kod ile bu belge çelişirse hangisinin yanlış olduğu ölçülerek bulunur.
> Güncel: 29 Eylül 2026.

## 1 · Proje ve kapsam

- **Soru:** karıştırma altındaki taktik İHA sürüsünde yönlendirme. Ürün öğrencinin protokolü DESPARETE; AODV, OLSR, AOMDV kıyas tabanı. Taban protokollerin karıştırma altındaki ölçümü ikinci, bağımsız katkı (`01`).
- **Yön (K-168, öğrenci 25 Eylül):** önce gerçekçilik (1:1, kaynaklı taktik sürü; gözlem = gerçek telsiz ve otopilotun verdiği), sonra DESPARETE'nin karıştırmayı gerçekten çözmesi. Bir ölçütle gerçekçilik çatışırsa gerçekçi olan seçilir (K-185).
- **Kapsam dışı:** gerçek RF/SDR/uçuş · frekans çevikliği ve çoklu kanal (öncül: çözüm yönlendirmede) · GPSR · derin öğrenme (öğrenci) · GPS karıştırması · RTS/CTS · protokol farkında karıştırıcı · ~2 000 s'lik uzun koşu (`12` §7).
- **Negatif sonuç** raporlanır; önceden ilan edilen bir yanlışlanma tetiklenirse iyi teşhis edilmiş bir negatif sonuç olur.
- Fikir sahipliği analizi gündemde değil (öğrenci, 28 Eylül); kayıtlarda "kim" alanı normal bilgi olarak durur.

## 2 · Referans dünya — deneylerin dünyası (`14`, K-169…K-181, K-185…K-188)

- `sim2/kanal/dunya.py::referans_2026()` bütün gerçekçilik anahtarlarını açar. **`Konfig()` varsayılanı eski 1:50 dünyadır** (eski regresyon vakaları ve eski ölçümler onunla birebir); araçlar dünyayı `kalibrasyon/dunya_secimi` üzerinden seçer (`--dunya referans_2026` ya da `DESPARETE_DUNYA`), bir AST testi bunu zorlar (K-183).
- **Telsiz:** 802.11b DSSS, kanal 6, 22 MHz · EIRP 20 dBm · dipol 2,15 dBi · işlem kazancı (Eb/N0 = SNR·B/R) · ARF hız uyarlaması 1/2/5,5/11 Mb/s (ns-3) · güce dayalı taşıyıcı dinleme + ED-CCA −76 dBm, 15 µs · yayılım gecikmesi · kısa yeniden deneme 7 · CW 31/1023 · veri onayı yalnız gönderen çözdüyse (K-115) · veri paketinin IP TTL'i 64 (RFC 1700, ns-3; K-215).
- **Kanal:** serbest uzay α = 2 · gölgeleme σ 3 dB, hücre 2,5 km · Rician K 10 dB — **EKSEN** (K-215): birincil test 10 dB'de, 6 ve 15 dB'de keşifsel tekrar (Faz 4.4'te DUYARLI, K-214) · yer–hava kanalı Al-Hourani (banliyö) · sönümleme durumsuz FIR, referans dünyada blok üreteciyle (K-198; statikte bağ başına donuk tek çekim).
- **Sürü:** N = 40 · alan 33 km (K-188) · irtifa 50–300 m · 40–120 km/h · dört hareket kolu: statik · bağımsız · görev · formasyon · kendi konumu GPS/INS 1,5 m CEP.
- **Trafik:** yere toplama birincil — her düğümden geçide 1 pkt/s × 512 B telemetri + geçitten 4 düğüme 0,25 pkt/s komut (K-126); eşler arası keşifsel. Ana deney aleti deseni açıkça vermeli (`Konfig` varsayılanı `esler_arasi`).
- **Senaryo eksenleri:** düğüm kaybı (birincil metrikte kohort: doğumda iki ucu yaşayan paketler, K-182) · trafik yoğunluğu · telsiz enerjisi (raporlanır, tasarım ölçütü değil).

## 3 · Tehdit ve birincil hücre

- **Sınıflar:** sürekli · darbeli · reaktif · aldatıcı · taramalı. **Aileler:** tekli merkez · cephe hattı · derin sızma · hedef koruma · hava eşlik; her ailede toplam ortalama güç eşit, referans taban 10 W (K-186).
- **Rejim sınırı:** onlarca watt'lık karıştırıcı sürünün tamamını karartır, orada yönlendirme kurtaramaz. Birincil hücre, etki alanı sürüden küçük "kısmi karıştırma" rejiminde kurulur (`14` §4).
- **Birincil hücre (K-186, K-192):** `formasyon · yere_toplama · derin_sizma · sürekli`, 10 W. Araç yalnız sessizken taşınır; ölçüm penceresinde ~1,3 km → fiilen merkezde, 15 s açık · 15 s sessiz, açıkken 20 W. Sınanan: periyodik açılıp kapanmaya zamansal uyum ve kısmi karıştırmada dolaşma. Hava karıştırıcısı (1–5 W) sürüyü böldüğü için birincil değil, keşifsel eksen.

## 4 · Protokolün gördüğü ve yapabildiği

- **Gözlem sözleşmesi (`05`):** protokol yalnız gerçek bir telsizin ve otopilotun verebileceğini görür — RSSI, gürültü, kanal doluluğu, PHY hatası, kulak misafiri çerçeveler, kendi konum/hız; karıştırıcıyı, gerçek bağ kalitesini ve topolojiyi göremez. Yüzey 29 alan; sızıntı testle kapalı.
- **Kontrol düzlemi (`13`):** protokol çağırmaz, niyet döndürür; her kontrol baytı kanalda ödenir; unicast sonucu ve iletim başarısızlığı kancalarla bildirilir; bekleme tamponu simülatörde (64 paket · 30 s, taşmada en eski düşer — ns-3 AODV ile aynı, K-198; birincil hücrede bağlamıyor: 256 paket ve 60 s birebir aynı sonuç, K-200).
- **Kâhin bilgisi hiçbir protokol kararına girmez.** Kâhinler yalnız ölçüm aleti ve referanstır.

## 5 · Taban protokoller — DONDU: `AODV-j` · `OLSR-c` · `AOMDV-f` (K-211, K-215)

- Kaynağına sadık, parametreler RFC varsayılanı, hiçbiri senaryoya göre ayarlanmaz; her protokol kendi HELLO'sunu kullanır, HELLO aralıkları eşitlenmez (`06` §4.2).
- **Kural:** SHOULD uygulanır, MAY beyan edilir (öğrenci, 19 Eylül). Sapmalar her protokolün biçim dosyasında gerekçesiyle (`protokoller/*_bicim.py`, `aomdv.py`).
- **AODV (RFC 3561):** başlangıç durumu −∞ (`AODV-j`, K-215: yerel saatin sıfırına çapalı başlangıç sonucu saat ofsetine bağlıyordu; AOMDV miras alır → `AOMDV-f`). Kural kural sadakat denetiminden geçti (K-208, `arsiv/teshis/aodv_sadakat_2026-09-30/denetim.md`): RFC birincil, ns-3 yalnız RFC'nin sustuğu ya da çeliştiği yerde hakem (§6.1–§6.6.1 çelişkisinde §6.6.1), ns-3'ün RFC dışı eklemeleri alınmadı. Beyanlı sapmalar: yerel onarım §6.12 (MAY) · RREP-ACK mesajı (kara liste bağ katmanı onayıyla, K-194) · karşılıksız RREP · önceki atlama ömrü (gözlem yüzeyi) · RERR hep yayın · TTL yükte. RFC'nin kendi kurallarından doğan geçici döngüler mekanizmadır (K-207). RFC durum (ii)'nin RERR'i öncül süzmesiz (RFC'nin süzme cümlesi normatif değil; ns-2/ns-3 ile aynı; süzme ters yol rotalarıyla kara delik doğuruyordu, K-210).
- **OLSR (RFC 3626):** §14 histerezis var · §13 bağ katmanı bildirimi KAPALI (K-196): karıştırıcısız kolda ve birincil hücrede (karıştırma altında) zarar veriyor — kapalı sürüm 4/4 tohumda ort +0,052 iyi (K-200). `OLSR(i, s13=True)` eski `OLSR-b`.
- **AOMDV:** Marina–Das 2001 + RFC 3561; AODV'nin alt sınıfı, kara listeyi ve keşif/veri/bakım kısmını miras alır (K-148, K-149, K-194, K-208). Kendi yazdığı işleyicilerde RFC tabanı makalenin sustuğu yerlerde AODV-i'nin kurallarına getirildi ve eksik öncül adımları eklendi (K-210, `AOMDV-e`). Makaleye özgü: Şekil 3 güncelleme kuralı (zaman aşımı girdi başına, Şekil 2) · §3.2 çok RREP, k cevap · S10 (geçersiz girdide ilan kabulü, ölçülmüş sapma).
- **U1 (kabul, K-136/K-137/K-192):** oran = PDR(protokol) / PDR(ETX kâhini), aynı konfig, tüm koşu PDR'si; statik ≥ 0,90 · hareketli ≥ 0,60, referans dünyada da değişmez. **U1-U** uygunluk kapısı (keşif, çok atlamalı teslim, korunum, kâhin aşılmıyor) — kalırsa protokol kabul edilmez. **U1-B** başarım bulgusu — eşik altı hücre ölçümle açıklanır: kusur izleri dışlanır ve mekanizma hücreleri sıralar. OLSR'ın düşük hücreleri "açıklanmış, sıralamasız" (öğrenci onayı, K-196). **Kâhin aşımı** otomatik ret değil: çözünürlükten fazla aşarsa üç kâhinin zarfına bakılır; zarfı da aşıyorsa yazılım hatası aranır (K-192).
- **K-215 (6 Ekim):** `AODV-j` · `AOMDV-f` · ETX kâhini 48 sönümleme örneğiyle (6'da yakınsamamıştı, U1 oranları şişikti) · kâhinin beacon'ı AODV HELLO çerçevesi (84 B, 1 s) · TTL 64 → U1 iki desende yeniden (`12` §1.1/3e); aşağıdaki sayılar K-211'indir.
- **Durum: DONDU (K-211, 2 Ekim).** U1-U üç protokolde iki desende ✅ (AOMDV'nin eşler arası üç kâhin aşımı zarfta). Yere toplamada tek düşük hücre AODV statik 1002 (0,873), K-207 gereği bulgu. OLSR'ın düşük hücreleri K-196 atfıyla. Bundan sonra kod değişirse yeni K kaydı + U1 + regresyon.

## 6 · DESPARETE

- Öğrencinin ilk taslak fikirleri `protokol_kaynaklari/DESPARETE_TASARIM_PAKETI/`de duruyor; bağlayıcı olan bugünkü yapı, o da kodda (`protokoller/desparete*.py`). Geliştirilmesi ajana bırakıldı, "yapım aşamasında" (öğrenci, 23 ve 25 Eylül).
- **Bugünkü kod hâli v0.4.1:** bayrak profili `PROFIL_V02` (yalın) + `SECENEK_V041` (V1 · V5 · V7 · V8 · V10 · V11 komut geri izi). Sekiz ablasyon bayrağı; güvenlik değişmezleri bayrakla kapanmaz (K-159…K-172).
- **Komutlar:** DESPARETE yalnız geçit alanı kurar; komut V11 geri iziyle taşınır; trafik herkes için aynıdır (K-160, K-172).
- **Birincil hücrede ilk ölçüm** (K-200, 4 geliştirme tohumu — ana deney değil): PDR 0,700; AODV 0,556, AOMDV 0,569, OLSR 0,418, kâhin 0,813. Kazancın büyüğü rotasızlığın azalmasından; açık evrede 0,56 — iyileştirilecek yer.
- **Eksikler — Faz 5'in konusu:** karıştırmaya özgü kanıt (C_jam) · öngörülü kaçınma · kanıta dayalı postür · PROTECT'in çok yolu ve çoğaltması · pasif dinleme (`12` Faz 5).

## 7 · Ölçüm

- **Metrikler üçlü sunulur:** teslim · gecikme · kontrol yükü; tek metrikle sıralama yok. PDR = ölçüm penceresinde doğan paketlerin teslim oranı. Gecikme ortak alt küme üzerinden. Kontrol yükü bayt ve kanal süresiyle; protokolün veri başlığı dâhil (K-151).
- **Evre metrikleri (`08`):** şok derinliği · toparlanma tamlığı · toparlanma süresi · tespit gecikmesi. Hata payı kümelenmeye dayanıklı; tespitin boş dağılımı negatif binom (K-196). Boş kol kapısı gerçek protokollerle geçti (G1-P).
- **Kâhinler:** ETX kâhini (U1 paydası) kesin tavan değildir; üst referans = üç kâhinin tohum başına zarfı (K-110). Kâhin grafiği karıştırıcının açık/sessiz çizelgesini görür (K-195). *Kâhin − protokol = körlüğün bedeli.*
- **Kayıp anatomisi** (`kalibrasyon/kayip_anatomisi.py`): düşüş sebebi × karıştırıcı bölgesi (alıcıda) × açık/sessiz evre × bağ kalitesi bandı; Faz 5 hedefleri buradan çıkar. Bölge anlık güçle, ayrıca **etki alanı** (karıştırıcı açık olsaydı alınacak ortalama güç) evre × alan tablolarıyla (K-202).
- **Çözünürlük:** eşleştirilmiş R = 0,023 (eski dünyada ölçüldü; referans dünyada Faz 6'da yeniden).

## 8 · Deney tasarımı ve istatistik (`06`)

- **Tohumlar:** geliştirme 1000–1010 (U1 1000–1002, Faz 5 1003–1010) · δ gürültüsü 1100–1119 · **ana deney 2000–2039 (40 tohum) mühürden önce hiçbir protokolle koşulmaz.**
- **Aileler:** 1 karakterizasyon (taban protokoller) · 2 üstünlük (H2.a/b/c: DESPARETE ↔ AODV/OLSR/AOMDV, birincil hücrede, çift yönlü eşleştirilmiş Wilcoxon, Holm aile içinde) · 3 mekanizma (ablasyon).
- **Eşik:** δ = 2·SD_ref/√n, SD_ref taban protokol çiftlerinin en gürültülüsünden; DESPARETE'nin hiçbir koşusu δ'ya girmez. "Üstün" = Holm'dan sonra p < 0,05 **ve** fark ≥ δ **ve** mekanizma kapısı (K-153).
- **Mühür ~12 Kasım** (`12` Faz 6): hipotezler, eşik değerleri, parametreler, tohum sayısı (güç analiziyle), birincil metrik (KR-2 açık).

## 9 · Yazılım altyapısı

- **Rastgelelik:** durum tutan kaynaklar ayrı sıralı akışlarda; kanal rastgeleliği protokolden bağımsız hash alanlarında → aynı tohumda her protokol aynı dünyayı görür (eşleştirme yapısal).
- **Korunum:** `üretilen = teslim + düşen + kuyrukta + uçuşta`, her koşuda; düşme sebepleri kapalı kümedir.
- **Köken defteri** (K-203): gerekçeler REFERANS dünyanın değerini anlatır; her parametre sekiz kovadan birinde (TÜRETİLMİŞ · ÖLÇÜLMÜŞ · KAYNAK · DUYARSIZ · TEDAVİ · KOL TANIMI · DÜNYA TANIMI · SINANMAMIŞ). **DÜNYA TANIMI** = öğrencinin onayladığı referans dünya tanımları ve birincil hücre (33 km, N 40, 40–120 km/h, 10 W …) — projenin kapsamı, duyarlılık borcu taşımaz. Mühürden önce SINANMAMIŞ = 0 ve duyarlılık borcu boş (ya da eksen/kapsam ilanı). Bugün SINANMAMIŞ 25 · borç 0. **Kapsam ilanı** (K-204): 10 keşifsel kol tanımı (darbeli · reaktif · taramalı sabitleri, tekli merkezin konumu, hava eşlik hızı) ölçülmeden kapsam — o kolların sonucu bu değerlere koşullu, birincil hücrenin kod yoluna girmezler; defterde `KAPSAM_ILANI`, rapor kapsam bölümünde yazar (eski dünyada darbeli ve taramalı DUYARLI çıkmıştı).
- **Sonuç satırı** kendi konfigini, kimliğini (kod özetleri dâhil), kapsam sınırlarını ve metrikleri yeniden üretecek ham veriyi taşır.
- **Regresyon** (`kalibrasyon/regresyon_satirlari.py`, taban `k198`) ve **mimari denetimi** davranış değiştiren her simülatör değişikliğinden sonra.

## 10 · Açık kararlar

| konu | kimde | ne zaman |
|---|---|---|
| KR-2 · birincil metrikte komutlar (öneri: birincil telemetri, bütün trafik ikincil) | öğrenci | Faz 6 |
| KR-D · Faz 5 mekanizmalarının tasarım paketine yansıması | öğrenci | Faz 5 |
| çizelgeli (periyodik) karıştırıcıda evre metriklerinin tanımı | ajan önerir, öğrenci onaylar | Faz 6 |
| SINANMAMIŞ 25: referans dünyada duyarlılıkla ölç ya da eksen ilan et (liste defterde, gerekçelerinde) | ajan, öğrenciye eksen listesi | Faz 4.4 (kapanış) |
