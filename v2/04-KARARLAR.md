# 04 · GEÇERLİ KARARLAR

> Bugün geçerli kararlar, konu konu. Yazılı değilse verilmemiştir. Bir kararın nasıl ve neden verildiği, kodda geçen `K-xxx` atıfları ve eski dünyanın (1:50) kararları: `kayit/KARAR-GUNLUGU.md`. Kod ile bu belge çelişirse hangisinin yanlış olduğu ölçülerek bulunur.
> Güncel: 14 Ekim 2026 (K-242); önceki sürümler `arsiv/04-KARARLAR-*.md`.

## 1 · Proje ve kapsam

- **Soru:** karıştırma altındaki taktik İHA sürüsünde yönlendirme. Ürün, bu çalışmada önerilen DESPARETE protokolüdür. Taban protokollerin karıştırma altındaki ölçümü ikinci, bağımsız katkıdır (`01`).
- **Kıyas tabanı:** AODV ve OLSRv2 (K-229) ve Babel (RFC 8966, K-242). Babel, DESPARETE'nin döngüsüzlük çekirdeğiyle aynı aileden (proaktif uzaklık-vektörü, uygulanabilirlik koşulu): DESPARETE'nin kazancının aile yapısından değil kendi mekanizmalarından gelip gelmediğini sınar. JarmRout rakiplikten çıktı (K-242); kodu ve kayıtları Faz 4b'nin kaydıdır.
- **Yön (K-168):** önce gerçekçilik (1:1, kaynaklı taktik sürü; gözlem = gerçek telsiz ve otopilotun verdiği), sonra DESPARETE'nin karıştırma altındaki başarımı. Bir ölçütle gerçekçilik çatışırsa gerçekçi olan seçilir (K-185).
- **Kapsam dışı:** gerçek RF/SDR/uçuş · frekans çevikliği ve çoklu kanal (öncül: çözüm yönlendirmede) · GPSR · derin öğrenme (SWaP) · GPS karıştırması · RTS/CTS · protokol farkında karıştırıcı · içeriden saldırılar (seçici iletim, kara delik, sahte rota; K-230) · ~2 000 s'lik uzun koşu (`12` §5).
- **Negatif sonuç** raporlanır; önceden ilan edilen bir yanlışlanma tetiklenirse sonuç teşhis edilmiş bir negatif sonuçtur.

## 2 · Referans dünya — deneylerin dünyası (`14`, K-169…K-181, K-185…K-188)

- `sim2/kanal/dunya.py::referans_2026()` bütün gerçekçilik anahtarlarını açar. **`Konfig()` varsayılanı eski 1:50 dünyadır** (eski regresyon vakaları onunla birebir). Araçlar dünyayı `kalibrasyon/dunya_secimi` üzerinden seçer (`--dunya referans_2026` ya da `DESPARETE_DUNYA`); bir AST testi bunu zorlar (K-183).
- **Telsiz:**
  - 802.11b DSSS, kanal 6, 22 MHz · EIRP 20 dBm · dipol 2,15 dBi. Çalışma noktası: AB/TR 2,4 GHz sınırındaki telsizin erişim sınırına gerilmiş seyrek ağı (1 Mb/s bağ ~8,9 km, geçide medyan 2 atlama). Taktik telsiz gücündeki (27–33 dBm) aynı alan yoğun ağdır (derece 32–33, en çok 2 atlama) ve keşifseldir. K-230'un "güç yalnız mesafeyi ölçekler, taktik sürünün ölçekli karşılığı" gerekçesi tutmaz: hızlar, gölgeleme hücresi, yayılım gecikmesi ve yer–hava açıları ölçeklenmez (denetim DD-02, K-242).
  - İşlem kazancı (Eb/N0 = SNR·B/R) · ARF hız uyarlaması 1/2/5,5/11 Mb/s (ns-3) · güce dayalı taşıyıcı dinleme + ED-CCA −76 dBm, 15 µs · yayılım gecikmesi.
  - En çok 7 iletim denemesi (6 yeniden deneme; dot11ShortRetryLimit, K-223) · CW 31/1023 · veri onayı yalnız gönderen çözdüyse (K-115) · veri paketinin IP TTL'i 64 (RFC 1700, ns-3; K-215).
- **Kanal:**
  - Serbest uzay α = 2 · gölgeleme σ 3 dB, hücre 2,5 km · yer–hava kanalı Al-Hourani (banliyö).
  - Rician K 10 dB — **eksen** (K-215): birincil test 10 dB'de, 6 ve 15 dB'de keşifsel tekrar.
  - Sönümleme durumsuz FIR, referans dünyada blok üreteciyle (K-198); statik kolda bağ başına donuk tek çekim.
- **Sürü:** N = 40 · alan 33 km (K-188) · irtifa 50–300 m · 40–120 km/h (bağımsız ve görev kolları; formasyonda istasyon tutma, ortak transit yok, `14` §3) · dört hareket kolu (statik · bağımsız · görev · formasyon) · kendi konumu GPS/INS 1,5 m CEP.
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
- **Bekleme tamponu** simülatördedir; kapasitesi herkes için aynıdır: 64 paket · 30 s, taşmada en eski düşer (ns-3 AODV ile aynı, K-198). Kullanımı protokole bağlıdır: AODV ve DESPARETE rotasız paketi bekletir, OLSRv2 ve Babel bekletmez (RFC'lerinde tampon yok). Bu yüzden `PDR_açık`ın gecikme tavanlı biçimi ikincil metriktir (§7, K-242). Birincil hücrede kapasite bağlamıyor: 256 paket ve 60 s birebir aynı sonucu verdi (K-200, Faz 4'ün rakipleriyle).
- **Uçtan uca kopya (K-231):** protokol gönderdiği paketin eşlerini başka komşulara da yollayabilir (`13` §07). Hedefte ilk varan teslim sayılır; eşlerin yayın süresi veri yüküdür.
- **Kaynak rotası (K-232):** DSR ailesi için paket başlığında ara düğümler; adres başına 4 bayt çerçeveye ve yönlendirme ek yüküne sayılır (`13` §07).
- **Kâhin bilgisi hiçbir protokol kararına girmez.** Kâhinler yalnız ölçüm aleti ve referanstır.
- **Gürültü gözlemi protokol kararına girmez (K-227):** simülatörde anlık ve hatasızdır; gerçek sürücü onu 30 s'de bir, 5 ölçümün ortancasıyla ve kırparak verir (`02` G18). Mimari denetimi okunmasını engeller. Karıştırma kanıtı kanal doluluğu, PHY hatası, MAC sonucu ve RSSI'den kurulur.

## 5 · Taban protokoller — AODV · OLSRv2 · Babel (K-242)

Donmuş: `AODV-k` (K-249; önceki `AODV-j`) · `OLSRv2-b` (K-239) · `Babel-a` (K-249). AODV-k ve Babel K-244 kuyruğunda regresyon, U1 (iki desen), evre kapıları ve G1-P'den geçti.

**Ortak kurallar:**
- Kaynağına sadık kurulur; parametreler RFC ya da makale varsayılanıdır, hiçbiri senaryoya göre ayarlanmaz.
- Her protokol kendi HELLO'sunu kullanır; HELLO aralıkları eşitlenmez (`06` §4.2).
- **Hakem ilkesi (K-244):** RFC'nin MUST ve SHOULD'u uygulanır; RFC açık bir değer ya da yordam veriyorsa o alınır. RFC'nin sustuğu, kendi içinde çeliştiği, seçeneğe ya da MAY'e bıraktığı yerde referans uygulamanın varsayılanı alınır (AODV'de ns-3, OLSRv2'de olsrd2, Babel'de babeld); referans uygulama yapmıyorsa alınmaz. Referans uygulamanın RFC'nin MUST ya da SHOULD'una uymadığı yerde RFC alınır. RFC'de olmayan eklemeleri alınmaz. Rakibi güçlendirir, DESPARETE açısından muhafazakârdır.
- Sapmalar ve modellenmeyen özellikler her protokolün beyan tablosunda gerekçesiyle durur (`protokoller/*_bicim.py`); gerekçesiz sapma düzeltilir.
- Kod `tests2/test_donma.py`ye bağlıdır. Bir dosya değişirse yeni K kaydı, U1 ve regresyon gerekir. `OLSR-d` ve `AOMDV-f`nin dosyaları eski regresyon vakaları için bağlı kalır; rakip değildirler (K-229).

**AODV (RFC 3561), donmuş `AODV-k` (K-243 · K-244 · K-249; önceki `AODV-j`):**
- Kural kural sadakat denetimi K-208 (`arsiv/teshis/aodv_sadakat_2026-09-30/denetim.md`), 42 kurala tamamlandı (K-244, `arsiv/teshis/aodv_sadakat_2026-10-14/denetim.md`). §6.1–§6.6.1 çelişkisinde §6.6.1 (ns-3). ns-3'ün RFC dışı eklemeleri alınmadı.
- Başlangıç durumu −∞ (K-215).
- K-242 (denetim DD-04): yayınlarda U(0, 10 ms) titreşim · §6.2'nin önceki atlama ömrü · MY_ROUTE_TIMEOUT 11,2 s · başarısız keşfin tamponu düşer.
- K-244 (ns-3'ün varsayılanları): her RREQ'te G bayrağı ve yanıt veren ara düğümden hedefe karşılıksız RREP (§6.6.3) · RERR tek öncüle tek-yayın, çok öncüle yayın; (ii)'de veri kaynağına rota varsa tek-yayın (§6.11) · kara liste yalnız RREP başarısızlığında (`iletim_sonucu` ile tür eşlemesi).
- Beyanlı sapmalar: yerel onarım §6.12 (MAY, ns-3'te yok) · RREP-ACK mesajı (tek-yayın RREP'in bağ katmanı onayı aynı tek yönlü bağı sezer, K-194) · TTL yükte · sıra karşılaştırması sarmasız.
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

**Babel (RFC 8966), gerçekleme K-244 (`protokoller/babel*.py`):**
- Hakem babeld 1.14 (`protokol_kaynaklari/uygulama_kaynaklari/babeld/`). Parametreler Ek B; bağ maliyeti babeld'in ETX'i (Ek A.2.2'nin seçeneği); histerezis Ek A.3, düzgünleştirme yarı ömrü 4 s; tetik eşikleri, IHU sıklığı, yinelemeler, joker istek ve kötüleşmede rota isteği babeld'in varsayılanları.
- Sadakat denetimi 55 kural (`arsiv/teshis/babel_sadakat_2026-10-14/denetim.md`). Giden TLV'ler hedef başına tamponda birleşir (§3.1); yerelde üretilen her sıra isteği bekleyen istekler tablosunda (§3.2.7). babeld'in RFC'den ayrıldığı üç yerde RFC alındı: seçili rotanın aynı router-id'li uygulanamaz güncellemesi (yok sayılır) · uygulanamaz güncellemede sıra isteği (her seferinde) · istek listesinin karşılaştırma yönü.
- Tel biçimi RFC 8966 §4 bayt bayt, IPv4 (AE 1); IPv6 yerine IPv4 beyanlı (simülatörün tek ağ katmanı).
- DESPARETE'yle aynı aileden: kazancın aile yapısından mı DESPARETE'nin kendi mekanizmalarından mı geldiğini ayırır.

**JarmRout (Pu 2018), `JarmRout-b` — rakiplikten çıktı (K-242):**
- Kodu (`protokoller/jarmrout*.py`), testleri, kural kural sadakat denetimi (K-234), U1 kayıtları ve iki regresyon vakası Faz 4b'nin kaydı olarak kalır. Regresyon vakaları kopya defteri (K-231) ve kaynak rotası (K-232) yollarının tek sınayıcısıdır.
- Çıkış gerekçesi rakibin kendi geçerliliğidir: makalenin yinelenen RREQ kuralı toplu akışta tıkanıklık çöküşü üretir (K-238; karıştırıcısız ikizde PDR ~0,38) ve evre metrikleri yorumlanamaz (K-239).

**U1 — kabul kapısı (K-136, K-137, K-192, K-238):**
- Oran = PDR(protokol) / PDR(ETX kâhini), aynı konfig, tüm koşu PDR'si. Eşik: statik ≥ 0,90 · hareketli ≥ 0,60.
- **U1-U** uygunluk kapısıdır (keşif, çok atlamalı teslim, korunum, kâhin aşılmıyor); kalırsa protokol kabul edilmez.
- **U1-B** başarım bulgusudur: eşik altı hücre ölçümle açıklanır, kusur izleri dışlanır. Kaynağına sadık bir protokolün eşik altı kalması protokolün kendi sınırıdır (K-207).
- **Kâhin aşımı** otomatik ret değildir. Çözünürlükten (R) küçükse kayıt yeter. Büyükse üç kâhinin zarfına bakılır (K-192); kopya gönderen protokolde kopya kuralı uygulanır: yalnız kopyayla teslim edilenler çıkarılınca oran ≤ 1 + R (K-238). İkisi de tutmazsa sızıntı ya da yazılım hatası aranır. Hata araması (sızıntı, sayım, korunum, kimlik) temiz çıkar ve kâhinin fazla kaybı ölçülürse hücre "kâhin bu hücrede üst sınır değil" beyanıyla kayda girer (K-248). Kâhinler bağ bilgisinin referansıdır, tavan değil: kanal modelinden yönlendirir, trafiğin yükünü ve çarpışmaları görmez.

## 6 · DESPARETE

- Bağlayıcı olan bugünkü koddur (`protokoller/desparete*.py`). İlk tasarım taslağı (v0.1, 22 Eylül) bayattır ve arşivdedir: `arsiv/DESPARETE_TASARIM_PAKETI_v0.1_2026-09-22/`. Kod yorumlarındaki `protokol_kaynaklari/DESPARETE_TASARIM_PAKETI/` yolları bu klasörü gösterir.
- v0.4.1 bir taslaktır. Faz 5'te yürütücünün tasarım kararlarıyla geliştirilir, gerekirse baştan yazılır; döngüsüzlük çekirdeğinin Babel ailesinden gelmesi tasarımı bağlamaz (yürütücü, 13 Ekim).
- **Bugünkü kod hâli v0.4.1:** bayrak profili `PROFIL_V02` (yalın) + `SECENEK_V041` (V1 · V5 · V7 · V8 · V10 · V11 komut geri izi). Sekiz ablasyon bayrağı; güvenlik değişmezleri bayrakla kapanmaz (K-159…K-172).
- **Komutlar:** DESPARETE yalnız geçit alanı kurar; komut V11 geri iziyle taşınır; trafik herkes için aynıdır (K-160, K-172).
- **Birincil hücrede ölçüm — Faz 5.0** (K-228; tohum 1003–1006, ana deney değil): `PDR_açık` DESPARETE 0,551 · AODV 0,444 · kâhin 0,780.
  - Karıştırmaya özgü kayıp (doğum evresine göre açık − önce): DESPARETE −0,204 · AODV −0,138 · kâhin −0,134.
  - v0.4.1'in AODV'ye üstünlüğü karıştırmadan bağımsızdır; karıştırıcı açılınca DESPARETE daha çok kaybeder.
  - Fazla kaybın tamamı "rota yok" (`rota_gecersiz`): ardılı karıştırılan alan onarıma girer; çoğu karıştırıcıdan uzak rölelerdedir. Fazla kayıp 4 tohumun 4'ünde pozitif ama anlamlı değil (t = 2,92 < 3,18). "Kota %52 / ulaşılamaz %48" ve "girişi %64 açlık" payları kanıt değildir: aletin açlık tanımı protokolünkiyle uyuşmuyor (denetim DD-11).
  - Aynı hücrede (1003 · 1004, G2ç) `PDR_açık` DESPARETE 0,476 · 0,538 ↔ OLSRv2 0,409 · 0,602; karıştırıcısız ikizde DESPARETE OLSRv2'nin gerisinde (0,757 · 0,786 ↔ 0,817 · 0,910). İki tohum, karar değil (K-242).
- **Faz 5'in sırası (K-228, K-242):**
  1. Yedek ardıl (5.4'ün çoğaltmasız kısmı): ardıl kopunca onarıma girmeden uygulanabilir ikinci ardıla geçiş zaten var; eksik olan yedeklerin canlı tutulması. İlk A/B mevcut `hedefli_canlilik` (V2+) seçeneğidir; K-165'teki reddi eski dünyada, karıştırıcısız, 3 tohum × 40 s'lik ölçüme dayanıyordu (denetim DD-28). Aynı A/B'de ayrı bayrakla açlıkta tur isteği.
  2. 5.1: karıştırma kanıtıyla erken geçiş.
  3. 5.3 (postür) ve 5.4'ün çoğaltması.
  - Hedefler 8 tohumla (1003–1010) ve OLSRv2'ye göre de okunur; anatomi aleti önce düzeltilir (DD-11).
- **Faz 5'in konusu olan eksikler:** karıştırmaya özgü kanıt · öngörülü kaçınma · kanıta dayalı postür · PROTECT'in çok yolu ve çoğaltması · pasif dinleme (`12` Faz 5).

## 7 · Ölçüm

- **Metrikler üçlü sunulur:** teslim · gecikme · kontrol yükü; tek metrikle sıralama yok.
- **Birincil metrik `PDR_açık`** (K-222): karıştırıcının açık dönemlerinde doğan paketlerin teslim oranı. Pencere PDR'si (ölçüm penceresinde doğan paketler) betimleyicidir.
- **Gecikme tavanlı `PDR_açık`** (ön-kayıtlı ikincil, K-242): aynı oran, yalnız tavan içinde teslim edilenler sayılır. Gerekçe: bekletme protokole göre değişir (§4) ve geç gelen telemetrinin sahada değeri azdır. Eşikler (K-246): **ana tavan 5 s** (ArduPilot'un GCS failsafe'i: Copter `FS_GCS_TIMEOUT`, Plane `FS_LONG_TIMEOUT`; MAVLink: 1 Hz heartbeat, 4–5 kaçan mesajda kopma) · duyarlılık **3,5 s** (QGroundControl'ün kopma ilanı) ve **10 s** (PX4 `COM_DL_LOSS_T`). Kaynaklar `protokol_kaynaklari/uygulama_kaynaklari/otopilot/`; sabitler `analiz/satir.py`. Zaman aşımları heartbeat'ler arası boşluğu ölçer; veri yaşı tavanı olarak kullanılması modelleme seçimidir.
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
  - 2 · üstünlük (H2.x: DESPARETE ↔ her rakip, birincil hücrede `PDR_açık`, çift yönlü eşleştirilmiş Wilcoxon, Holm aile içinde; üç rakip eşit rolde, m = 3, KR-3 · K-247);
  - 3 · mekanizma (ablasyon).
- **İkincil testler (K-222):** karıştırıcısız ikiz hücreyle fark-içinde-fark · dayanıklılık hücresi (10 s açık · 20 s sessiz).
- **Eşik:** δ = 2·SD_ref/√n; SD_ref taban protokol çiftlerinin en gürültülüsünden. DESPARETE'nin hiçbir koşusu δ'ya girmez.
- **"Üstün"** = Holm'dan sonra p < 0,05 **ve** fark ≥ δ **ve** mekanizma kapısı: karıştırmaya özgü mekanizmalar kapatılınca `PDR_açık` anlamlı düşmeli (K-153, K-222). Kapıya karıştırmaya karşı tasarlanan mekanizmalar girer, her zaman açık olsalar bile; amaç ölçmeden önce yazılır. Genel katkıları ikiz hücredeki geliştirme ablasyonuyla beyan edilir (K-247).
- **"Karıştırmaya özgü kazanç"** ancak ayrıca fark-içinde-fark anlamlı pozitifse söylenir (`06` §0.4.5).
- **Mühür** ~20 Kasım (`12` Faz 6): hipotezler, eşik değerleri, parametreler, tohum sayısı (güç analiziyle), birincil metrik.

## 9 · Yazılım altyapısı

- **Rastgelelik:** durum tutan kaynaklar ayrı sıralı akışlardadır; kanal rastgeleliği protokolden bağımsız hash alanlarındadır. Aynı tohumda her protokol aynı dünyayı görür (eşleştirme yapısal).
- **Korunum:** `üretilen = teslim + düşen + kuyrukta + uçuşta` her koşuda denetlenir (kopyada `13` §07); düşme sebepleri kapalı kümedir.
- **Köken defteri** (`sim2/yapilandirma/kokenler.py`, K-203): her parametre sekiz kovadan birindedir: TÜRETİLMİŞ · ÖLÇÜLMÜŞ · KAYNAK · DUYARSIZ · TEDAVİ · KOL TANIMI · DÜNYA TANIMI · SINANMAMIŞ. Gerekçeler referans dünyanın değerini anlatır. Mühürden önce SINANMAMIŞ = 0 ve duyarlılık borcu boş olmalı (ya da eksen/kapsam ilanı).
  - **DÜNYA TANIMI:** onaylanmış referans dünya tanımları ve birincil hücre (33 km, N 40, 40–120 km/h, 10 W …). Projenin kapsamıdır, duyarlılık borcu taşımaz.
  - **Sayımın tek yeri burasıdır.** Bugün **SINANMAMIŞ 5**: pencere üçlüsü (Faz 6) · `rssi_olcum_sigma_db` ve `gps_dikey_sigma_m` (JarmRout RSSI ve konum okuyor, K-233; JarmRout rakiplikten çıktı, iki kayıt DESPARETE'nin Faz 5'te bu alanları okuyup okumayacağı belli olunca kapanır, K-242) · duyarlılık borcu 0.
  - **DUYARSIZ 9** (ölçülen |Δ| defterde) · `gm_hiz_sigma_ms` DUYARLI → DÜNYA TANIMI, ölçülen duyarlılığı raporda (K-225) · Rician K eksen (§2).
  - **Kapsam ilanı 13** (K-204, K-215, K-222): darbeli · reaktif · taramalı sabitleri, tekli merkezin konumu, hava eşlik hızı, görev müfreze sayısı, GM eğimi, görev kolu jitter'ı. Birincil hücrenin kod yoluna girmezler; o kolların sonucu bu değerlere koşulludur; rapor kapsam bölümünde yazılır.
  - **Kaynaksız DÜNYA TANIMI'lar** (ölçülen duyarlılıklarıyla raporda): gölgeleme hücresi · CBR titreşimi · istasyon tutma (K-220) · formasyon manevra gürültüsü (K-225) · komut akış sayısı (K-223).
  - **KAYNAK'a bağlananlar:** TTL 64 · kâhinin beacon'ı = AODV HELLO (84 B, 1 s) (K-215). Kâhinin sönümleme örneği 48 (K-215).
- **Sonuç satırı** kendi konfigini, kimliğini (kod özetleri dâhil), kapsam sınırlarını ve metrikleri yeniden üretecek ham veriyi taşır.
- **Regresyon** (`kalibrasyon/regresyon_satirlari.py`, taban `k243`, K-243) ve **mimari denetimi** davranış değiştiren her simülatör değişikliğinden sonra koşulur.

## 10 · Açık kararlar

| konu | gereken | ne zaman |
|---|---|---|
| Yer–hava ortamının duyarlılığı: banliyö (birincil) ↔ açık arazi; açık arazide aynı güç sürüyü karartır, kısmi rejim için güç ya da konum ayarı gerekir (denetim DD-01, K-242) | ölçüm planı, ardından karar | Faz 6 |
| KR-2 · birincil metrikte komutlar (öneri: birincil telemetri, bütün trafik ikincil) | karar | Faz 6 |
| DESPARETE'nin güncel tasarım belgesi (v0.1 paketi arşivde; Faz 5 mekanizmalarıyla birlikte yeniden yazılır) | yazım | Faz 5.7 |
| temas kaybı metriğinin tanımı ve T eşiği (otopilot kaynağı, K-230) | kaynak, ardından karar | mühür |
| pencere üçlüsü (ısınma · ölçüm bitişi · koşu bitişi): koşu uzunluğundan bağımsızlık, birincil hücrede, taban protokollerle. Trafik ölçüm bitişinde durduğu için uzun bekleyişli protokolde son doğumlar boşalan ağda teslim edilir (JarmRout'ta son 5 s'nin PDR'si 0,53 · 0,59; K-239) | ölçüm, ardından karar | Faz 6 |
| `06` H1.3'ün aldatıcı ↔ sürekli kontrastı referansta (10 W aldatıcı ED'yle ağı susturuyor, K-219) · Rician K ekseninin keşifsel tekrarı (6 · 15 dB) | öneri, ardından karar | Faz 6 |
