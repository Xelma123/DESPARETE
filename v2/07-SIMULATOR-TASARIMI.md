# 07 · SİMÜLATÖR — `sim2/` ne, nasıl çalışır

> Bugünkü simülatörün anlatımı. Referans dünyanın sayıları ve kaynakları `14`de, kararlar `04`te. Güncel: 28 Eylül 2026. Önceki sürüm (eski dünyanın tabloları, yapım planı Y0–Y10, uygulama tarihçesi, öğrenci kararlarının tarihli listesi): `arsiv/07-SIMULATOR-TASARIMI-2026-09-28-temizlik.md` — koddaki eski `§` atıfları oraya gider.

## 1 · Ne ölçüyor, neden kendi simülatörü

*Karıştırma altında bir yönlendirme protokolü AODV, OLSR ve AOMDV'ye göre hangi metrikte ne kadar farklı davranır?* Hazır bir simülatör yerine proje kendi simülatörünü yazdı: her varsayım görünür, sınanabilir ve jüri önünde savunulabilir olsun diye. Karşılığı, aletin kendisinin doğrulanmasıdır:

| sınav | durum |
|---|---|
| iç tutarlılık — korunum, mutabakat, belirlenimcilik | her koşuda |
| analitik — yol kaybı, gürültü, çerçeve süreleri, sönümleme momentleri, Bianchi | ✅ |
| dış çapa — Li vd. çok atlamalı zincir kapasitesi | ✅ referans dünyada sabit hızda H1 = 0,127 bantta (`09`) |
| gerçekçilik — karıştırıcısız statik ağda kâhin PDR ≈ 1 | ✅ |

## 2 · İki dünya

- **Referans dünya** (`sim2/kanal/dunya.py::referans_2026()`): 1:1 gerçek birimler, bütün gerçekçilik mekanizmaları açık. **Deneyler burada koşar.**
- **Eski dünya** (`Konfig()` varsayılanı, 1:50 ölçek): Aşama 1–2'nin ölçümleri ve eski regresyon vakaları onunla birebir. Yeni ölçümde kullanılmaz.
- Araçlar dünyayı `kalibrasyon/dunya_secimi` üzerinden seçer; bir test bunu zorlar.

## 3 · Katmanlar

| paket | ne yapar |
|---|---|
| `cekirdek` | olay kuyruğu · rastgelelik (kaynak başına sıralı akışlar + durumsuz hash alanları) · korunum defteri · sayaç kütüğü · kimlik özetleri · düğüm saatleri |
| `dunya` | yerleşim · dört hareket kolu (statik · bağımsız Gauss-Markov 3B · görev/müfreze · formasyon) · topoloji (konum zamanın saf fonksiyonu) |
| `kanal` | yayılım (yol kaybı, gölgeleme, anten deseni) · sönümleme (Rician, durumsuz FIR) · girişim (parça başına SINR) · karıştırıcılar ve tehdit aileleri · yer–hava kanalı · çerçeve süreleri ve PER (tek fonksiyon) |
| `mac` | 802.11b DCF temel erişim · güce dayalı taşıyıcı dinleme + ED-CCA · onay ve yeniden deneme · ARF · tek radyolu alıcı zinciri, yakalama |
| `ag` | trafik (yere toplama, eşler arası) · kuyruk · paket |
| `gozlem` | protokolün gördüğü pencere, niyetler, kontrol düzlemi sözleşmesi, teşhis kanalı |
| `kosum` | düğüm, gönderim, alım, teslim, kontrol düzlemi, bekleme tamponu, düğüm kaybı, sonuç satırı |
| `olcum` | paket defteri · metrikler · evre metrikleri · rota olayları |
| `yapilandirma` | `Konfig` · senaryolar · kapsam beyanı · köken defteri |

Bir paketin yolu: trafik üretir → düğüm kuyruğa alır → protokol sonraki atlamayı seçer (yalnız gözlem penceresiyle) → MAC kanalı dinler, gönderir → kanal alıcıda parça parça SINR hesaplar, PER'den karar çıkar → alıcı onaylar ya da gönderici yeniden dener → teslim ya da kapalı bir düşme sebebiyle kayda geçer.

## 4 · Dünya, kanal ve MAC (referans dünyada)

- **Sürü:** 40 İHA · 33 km alan · 50–300 m irtifa · 40–120 km/h. Hacim sürüyle hareket eden bir gözlem çerçevesidir; yer referanslı varlıklar (karıştırıcılar) bu çerçevede hareket eder.
- **Hareket kolları:** statik (referans; sönümleme donuk) · bağımsız · görev (müfreze + istasyon tutma) · formasyon (istasyon = yerleşim; birincil hücrenin kolu). Kapı: Θ = rota ömrü / 15 s (OLSR `TOP_HOLD_TIME`) ≥ 3; her satır Θ_OLSR ve Θ_AODV'yi taşır.
- **Kanal:** serbest uzay α = 2 · log-normal gölgeleme σ 3 dB, 2,5 km'lik hücrede korelasyonlu · dipol anten deseni · Rician K 10 dB, Doppler gerçek bağıl hızdan; sönümleme 190 µs'lik parçalarda, durumsuz (her protokol aynı izi görür), referans dünyada blok üreteciyle (K-198) · girişim toplamsal, karıştırıcı alıcıda.
- **PHY/MAC:** EIRP 20 dBm · işlem kazancı · 1/2/5,5/11 Mb/s ARF · ED −76 dBm · slot 20 µs, SIFS 10 µs, CW 31–1023 · kısa yeniden deneme 7 · yayılım gecikmesi · yakalama. Veri onayı yalnız gönderen alıcı tarafından çözüldüyse sayılır.

## 5 · Tehdit

| sınıf | davranış |
|---|---|
| sürekli | hep açık gürültü |
| darbeli | periyot 2,7 s, görev çevrimi 0,5; tepe gücü ortalama eşit olacak biçimde |
| reaktif | çerçeveyi sezince (−90 dBm, 16 µs) kısa patlama |
| aldatıcı | sahte çerçeve; alıcıyı kilitler |
| taramalı | konaklar arasında atlar (3 konak × 0,1 s) |

| aile | üye | platform ve hareket |
|---|---|---|
| tekli merkez | 1 | alan merkezinde sabit |
| cephe hattı | 3 | doğu kenarında sabit, yer |
| derin sızma (**birincil**) | 1 | yer aracı, merkezden batıya 60 km/h, yalnız sessizken taşınır; 15 s açık · 15 s sessiz |
| hedef koruma | 2 | sabit, yer |
| hava eşlik | 1 | 200 km/h, kuzeye; karıştırılmış evrenin ortasında merkezden geçer |

Her ailede toplam ortalama güç eşit (referans taban 10 W). Yer karıştırıcısı 3 m'de, düğüme yer–hava kanalıyla ulaşır. İki etki: uzakta alıcı SINR'ı, yakında ED-CCA ile vericinin susması ("kanal erişim kilidi"). Karıştırıcı bir açılma anında (ölçüm penceresinin ortasında) devreye girer; evre metrikleri bu sayede tanımlıdır. **Protokol karıştırıcıyı görmez.**

## 6 · Trafik

Yere toplama (birincil): geçit düğüm 0, batı kenarının ortasında sabit röle İHA; her düğümden geçide telemetri 1 pkt/s × 512 B + geçitten 4 düğüme komut 0,25 pkt/s. Eşler arası (keşifsel): 10 akış CBR. Beyanlar: geçidin yere bağı ideal · tek geçit · CBR basitleştirmedir. Ana deney aleti deseni açıkça verir (`Konfig` varsayılanı eşler arası).

## 7 · Protokol yüzeyi ve kâhinler

- Protokol yalnız gözlem penceresini görür (`05`) ve niyet döndürür (`13`); her taban protokol kendi HELLO'sunu kullanır, simülatörün beacon'ı onlarda kapalıdır.
- **Kâhinler ölçüm aletidir,** protokol girdisi değil: ETX kâhini (U1'in paydası; kesin tavan değil), en kısa yol kâhini, teslim olasılığı kâhini; üst referans = tohum başına üçünün zarfı. Kâhin grafiği hareket diliminde ve karıştırıcının açık/sessiz geçişinde yenilenir. *ETX kâhini − atlama kâhini = ölçütün bedeli · kâhin − protokol = körlüğün bedeli.*

## 8 · Metrikler

PDR (doğum kohortu; tüm koşu ve ölçüm penceresi; telemetri/komut ayrı) · PSR (bağ düzeyi, öğrencinin tanımı) · gecikme yüzdelikleri (ortak alt küme) · kontrol yükü (çerçeve, bayt, kanal süresi; veri başlığı dâhil) · kopma sayaçları, rota kurtarma gecikmesi Δ ve COR · evre metrikleri (`08`) · Θ · enerji · kayıp yeri (düşüş sebebi × geçide mesafe).

## 9 · Parametre disiplini ve kapsam

- **Köken defteri** (`sim2/yapilandirma/kokenler.py`): her `Konfig` alanı ve modül sabiti yedi kovadan birinde; kayıtsız alan kurulumu durdurur, mimari denetimi sayar. Mühürden önce SINANMAMIŞ = 0 ya da eksen ilanı.
- **Kapsam beyanı** (`kapsam.py`): her sonuç satırı modellenmeyenleri ve sonucu hangi yöne çektiklerini kendi konfiginden yazar (çoklu kanal · RTS/CTS · arazi/engel · patlamalı trafik · hava–hava kanalının ayrı modeli · karıştırıcının akıllı hedef takibi).

## 10 · Simülatörü değiştirirken

| kural | nasıl |
|---|---|
| yeni davranış bir anahtarın arkasında | varsayılanı bugünkü davranışı birebir üretir; regresyonda değişmesi beklenen alanlar önceden yazılır |
| yeni parametre | köken defterine kovasıyla |
| yeni rastgelelik | önce hash alanı; sıralı akış yalnız durum gerekiyorsa |
| yeni sayaç | sayaç kütüğüne; pencere ikizi otomatik |
| yeni mekanizma | boş geçmeyen bir test: mekanizma devredeyken kanıt > 0 |
| büyük tasarım değişikliği | öğrenciye önce anlatılır |

## 11 · Açık

- **Görselleştirme** (sunum için; iz kanalı ölçüme dokunmaz — iz açık/kapalı sonuç satırı birebir olmalı): düğümler ve bağlar, karıştırıcı etki alanı ve hareketi, geçide rotalar, evre çizgili PDR eğrisi. Yazılmadı.
- `iletim_menzili_m` adı artık bir menzil değil, eski dünyanın güç çapası — ad yanıltıcı.
