# FANET'te Elektronik Harp Şartları Altında Yönlendirme Protokollerinin Değerlendirilmesi: Spesifik Başarım Metrikleri

## Yönetici Özeti

Uçan Tasarsız Ağlarda (FANET) yönlendirme protokollerinin elektronik harp (EH) — özellikle karıştırma (jamming) — altında değerlendirilmesi, klasik MANET başarım ölçütlerinin doğrudan aktarılmasıyla yapılamaz. Bunun iki temel nedeni vardır. Birincisi, karıştırma altında bir bağlantının "kopması" fiziksel katmanda bir SINR eşiği ihlalidir; yönlendirme protokolü bunu yalnızca HELLO kaybı gibi dolaylı bir sinyalle, üstelik gecikmeli olarak algılar. İkincisi, karıştırıcı sınıfına göre başarım göstergelerinin ilişkisi tersine dönebilir: reaktif bir karıştırıcı altında gönderici tarafındaki Paket Gönderim Oranı (PSR) %99–100 seviyesinde kalırken alıcı tarafındaki Paket Teslim Oranı (PDR) %0'a düşebilir ([Xu, Trappe, Zhang & Wood](https://www.winlab.rutgers.edu/~trappe/Papers/JamDetect_Mobihoc.pdf)). Bu nedenle tek bir metrik üzerinden yapılan değerlendirme, saldırıyı tamamen görünmez kılabilir.

Bu rapor, kullanıcının odaklanılmasını istediği beş metriği — PDR, Uçtan Uca Gecikme, Yönlendirme Yükü, Bağlantı Kopma Sayısı ve Karıştırma Altında Rota Kurtarma Süresi — birincil kaynaklardaki formal tanımlarına, ölçüm protokollerine, tuzaklarına ve EH bağlamına özgü ek parametrelerine indirgeyerek ele almaktadır. Metodolojik çerçeve olarak IETF RFC 2501 temel alınmış, üzerine karıştırma literatüründen (J/S, SINR eşiği, görev döngüsü, spektral doluluk) gelen bağımsız değişkenler eklenmiştir.

Raporun en kritik bulgusu bir boşluk tespitidir: taranan literatürde OLSR, AODV, BATMAN-adv, DSDV veya GPSR için **RF karıştırma altında saniye ölçeğinde rota kurtarma gecikmesi** bildiren doğrudan bir çalışma bulunamamıştır. Saniye ölçeğindeki kurtarma sayıları düğüm-kapatma veya kanal-değiştirme ile arıza enjekte edilen MANET/mesh senaryolarından gelmekte (benzetimde 4,8–14,9 s; saha ölçümünde 2,2–7,3 s), karıştırmaya özgü FANET çalışmaları ise PDR, verim, bağlantısallık, ada sayısı ve COR bildirmektedir. Bu iki literatürün birleştirilmesi açıkça beyan edilmeli, ima edilmemelidir.

---

## 1. Metodolojik Temel: RFC 2501 ve EH Bağlamına Genişletilmesi

### 1.1 RFC 2501'in nicel metrik seti

MANET yönlendirme protokollerinin değerlendirilmesine ilişkin ilk standartlaştırılmış çerçeve olan RFC 2501, yalnızca dört nicel metrik tanımlar: uçtan uca veri iş hacmi ve gecikmesi, Rota Edinme Süresi (Route Acquisition Time), Sırasız Teslim Yüzdesi (Percentage Out-of-Order Delivery) ve Verimlilik (Efficiency) ([Corson & Macker, RFC 2501](https://www.rfc-editor.org/rfc/rfc2501)). Aynı doküman yönlendirme yükünün sınırını çok net çizer: veri olmayan her şey kontrol yüküdür. Bu kural, protokoller arası karşılaştırmalarda yükü tanımlamanın tek tutarlı yoludur, çünkü OLSR'ın periyodik HELLO/TC trafiği ile AODV'nin olay-tetiklemeli RREQ/RREP/RERR trafiği aksi halde aynı ölçekte kıyaslanamaz.

RFC 2501 ayrıca sonuçların yorumlanabilmesi için bildirilmesi zorunlu sekiz bağlamsal parametre listeler (ağ boyutu, bağlantısallık, topolojik değişim oranı, bağlantı kapasitesi, tek/çift yönlü bağlantı oranı, trafik deseni, uyku/uyanık düğüm oranı ve hareketlilik) ([RFC 2501](https://www.rfc-editor.org/rfc/rfc2501)). EH senaryolarında bu listeye karıştırıcıya özgü bir ikinci parametre bloğu eklenmesi gerekir; bu blok Bölüm 7'de tanımlanmıştır.

### 1.2 Neden EH'ye özgü genişletme zorunlu

Karıştırma, hareketliliğin yarattığı topoloji değişiminden bağımsız ve onunla karışabilen bir bağımsız değişkendir. Meşru düğümlerin hareket modeli ve kanal hata modeli bildirilmezse, gözlenen PDR düşüşünün karıştırmadan mı yoksa hızlı İHA hareketinden mi kaynaklandığı ayrıştırılamaz. Bu nedenle karıştırma çalışmalarında hareketlilik parametrelerinin karıştırıcı parametrelerinden ayrı raporlanması, temel bir geçerlilik koşuludur ([Won, Youn & Ali](https://dl.ifip.org/db/conf/euc/eucw2006/WonYA06.pdf)).

---

## 2. Metrik 1 — Paket Teslim Oranı (PDR)

### 2.1 Formal tanım

PDR, hedefe başarıyla ulaşan veri paketlerinin kaynaklarca üretilen veri paketlerine oranıdır:

\[
\mathrm{PDR}=\frac{\sum_{f}\left|\mathcal{R}_f\right|}{\sum_{f}\left|\mathcal{G}_f\right|}\times 100\%
\]

Burada \(\mathcal{G}_f\) akış \(f\) için uygulama katmanında üretilen paket kümesi, \(\mathcal{R}_f\) ise hedefte teslim edilen paket kümesidir. Bu tanım MANET protokol karşılaştırmalarının kanonik referansı olan Broch ve arkadaşlarının MobiCom çalışmasında "packet delivery fraction" adıyla kullanılmıştır ([Broch et al.](https://pages.cs.wisc.edu/~suman/courses/740/papers/broch98mobicom.pdf)). Karıştırma literatüründeki tanım da özünde aynıdır: "bir hedefe başarıyla teslim edilen paketlerin göndericinin gönderdiği paketlere oranı"; kritik ek kural, hiç paket alınmadığında PDR'nin tanım gereği 0 kabul edilmesidir ([Xu et al.](https://www.winlab.rutgers.edu/~trappe/Papers/JamDetect_Mobihoc.pdf)). ns-3 karıştırma modülü de PDR'yi "doğru alınan paketlerin gönderilen paketlere oranı" olarak aynı biçimde tanımlar ([Bout & Loscrì](https://hal.science/hal-03765858/file/WSNIMhal.pdf)).

### 2.2 PSR ile birlikte raporlama zorunluluğu

EH bağlamında PDR'nin tek başına raporlanması yanıltıcıdır. Paket Gönderim Oranı (PSR), "meşru bir trafik kaynağının MAC katmanında başarıyla gönderebildiği paketlerin göndermek istediği paketlere oranı", yani \(m/n\) olarak tanımlanır ([Xu et al.](https://www.winlab.rutgers.edu/~trappe/Papers/JamDetect_Mobihoc.pdf)). Bu iki metriğin birleşimi karıştırıcı sınıfının imzasını verir:

| Karıştırıcı sınıfı | PSR | PDR | Yorum |
|---|---|---|---|
| Sürekli (constant) | %74,37 → %99,57 | %0,43 (d=38,6 in) → %93,57 (d=72 in) | Mesafeye güçlü bağımlılık ([Xu et al.](https://www.winlab.rutgers.edu/~trappe/Papers/JamDetect_Mobihoc.pdf)) |
| Aldatıcı (deceptive) | %0,00 | %0,00 | Kanal tamamen meşgul; gönderici bile erişemez ([Xu et al.](https://www.winlab.rutgers.edu/~trappe/Papers/JamDetect_Mobihoc.pdf)) |
| Rastgele (random) | ≈%60,5 | %0,06 → %47,41 | Uyku süresi dağılımına duyarlı ([Xu et al.](https://www.winlab.rutgers.edu/~trappe/Papers/JamDetect_Mobihoc.pdf)) |
| Reaktif (reactive) | %99–100 | %0,00 | **Saldırı gönderici tarafından görünmez** ([Xu et al.](https://www.winlab.rutgers.edu/~trappe/Papers/JamDetect_Mobihoc.pdf)) |

Reaktif satır, EH değerlendirmesinde tek metrikli yaklaşımın neden reddedilmesi gerektiğinin ampirik kanıtıdır.

### 2.3 Ölçüm kuralları ve tuzaklar

PDR hesabında kontrol paketleri hem paya hem paydaya dahil edilmez; bu dışlama RFC 2501'in "veri olmayan her şey kontrol yüküdür" kuralının doğal sonucudur ([RFC 2501](https://www.rfc-editor.org/rfc/rfc2501)). Bunun yanında üç yapısal tuzak vardır:

- **Isınma (warm-up) dönemi.** Proaktif protokoller topoloji tablolarını doldurmadan önce üretilen paketler kaçınılmaz olarak düşer. Bu dönem PDR hesabından dışlanmazsa OLSR sistematik olarak cezalandırılır.
- **Kuyruk (cool-down) etkisi.** Benzetim bitiminde hâlâ yolda olan paketler teslim edilmemiş sayılır; uzun benzetimlerde etkisi küçük, kısa benzetimlerde ciddidir.
- **Üretilen paket sayımının yeri.** Uygulama katmanında üretilen paket ile ağ katmanına teslim edilen paket farklıysa (kuyruk taşması nedeniyle), payda seçimi sonucu değiştirir.

### 2.4 Karıştırma altında bildirilmiş PDR bozulmaları

| Ortam | Karıştırıcı yapılandırması | Bildirilen bozulma | Kaynak |
|---|---|---|---|
| ns-3 + gerçek 802.11 test yatağı, 1 saldırgan | Sürekli | PDR %100 → %0; gerçek ortamda bağlantı saniyeler içinde kayboluyor | [Bout & Loscrì](https://hal.science/hal-03765858/file/WSNIMhal.pdf) |
| Aynı | Reaktif | PDR %60–70 (benzetim) / %50–60 (gerçek) bandında salınıyor | [Bout & Loscrì](https://hal.science/hal-03765858/file/WSNIMhal.pdf) |
| 802.11p araç ağı | Sürekli / periyodik (%86 görev döngüsü, 74 µs) / reaktif | PDR sırasıyla SNJR 9 dB / 55 dB / 12 dB altında sıfırlanıyor | [Pirayesh & Zeng](https://inss.egr.msu.edu/papers/Hossein22_COMST_jamming_survey.pdf) |
| 200 düğümlü ızgara, AODV + GPSR, NS-2 | Hareketli karıştırıcı, 12 m yarıçap, 8 → 1 m/s | Teslim başarı oranı %10'a kadar düşüyor; GPSR, yönlendirme bilgisinin güncellenmesini beklediği için AODV'den daha hızlı bozuluyor | [Won, Youn & Ali](https://dl.ifip.org/db/conf/euc/eucw2006/WonYA06.pdf) |
| FANET, ns-3, AODV, 25 düğüm, 720 km/sa | *Yönlendirme* saldırıları (RF karıştırma değil) — kıyas tabanı | Temel PDR %91,43; %20 sinkhole → %56,60; %20 blackhole → %56,81 | [Ceviz, Sadioglu & Sen](https://web.cs.hacettepe.edu.tr/~ssen/files/papers/AdhocNets22.pdf) |
| FANET, CentAir vs çok-kanallı OLSR | Aldatıcı karıştırıcılar | PDR +%11,5; verim +%18,1; gecikme −%21,1; enerji verimliliği +%17,8 | [Sarı & Seçinti](https://research.itu.edu.tr/en/publications/using-centrality-based-topology-control-for-fanet-survivability-a/) |

Son satır, FANET'e özgü karıştırma-dayanıklı topoloji kontrolünün ölçülebilir kazanımını gösteren en doğrudan sayısal referanstır.

---

## 3. Metrik 2 — Uçtan Uca Gecikme (E2E Latency)

### 3.1 Formal tanım

Ortalama uçtan uca gecikme, yalnızca teslim edilen paketler kümesi \(S\) üzerinden hesaplanır:

\[
\bar{D}=\frac{1}{|S|}\sum_{k\in S}\left(t^{k}_{rx}-t^{k}_{tx}\right)
\]

Bu tanım güncel FANET/İHA başarım çalışmalarında standart biçimde kullanılmaktadır ([Ateya et al.](https://www.mdpi.com/1999-5903/17/10/473)). Gecikme bileşenleri klasik olarak rota keşfi bekleme süresi, arayüz kuyruğunda bekleme, MAC yarışma ve yeniden iletim süresi ile yayılma/iletim süresi olarak ayrıştırılır ([Das et al.](https://ebelding.cs.ucsb.edu/sites/default/files/publications/infocom00.pdf)).

### 3.2 Hayatta kalan yanlılığı (survivorship bias) — EH'de kritik

Formülün \(S\) kümesi üzerinden tanımlanması, karıştırma altında ciddi bir yorumlama hatasına yol açar: karıştırıcı en uzun ve en kırılgan yolları kestiğinde, teslim edilemeyen paketler ortalamadan çıkar ve **ortalama gecikme paradoksal biçimde iyileşmiş görünür**. Bu nedenle karıştırma altında ortalama gecikme, PDR ile birlikte ve tercihen yüzdelik değerlerle raporlanmalıdır.

IETF, kaybolan paketler için formal çözümü açıkça belirtir: tek yönlü gecikme ölçümünde kaybolan paketin gecikmesi "sonsuz büyük" (undefined) kabul edilir; yüzdelik hesabında bu değerler \(+\infty\) olarak sıralamaya dahil edilir ([RFC 7679](https://datatracker.ietf.org/doc/html/rfc7679)). Pratik sonuç: p50 anlamlı kalırken p95/p99 karıştırma altında tanımsız olabilir ve bu bilgi bizzat sonucun kendisidir.

### 3.3 Titreşim (jitter)

Ardışık paket gecikme farkının mutlak ortalaması olarak IPDV:

\[
J_{\mathrm{IPDV}}=\frac{1}{N-1}\sum_{i=2}^{N}\left|D_i-D_{i-1}\right|
\]

Bu form güncel sensör/İHA ağı çalışmalarında kullanılmaktadır ([Tu et al.](https://www.mdpi.com/1424-8220/25/24/7522)). RTP'nin düzleştirilmiş (smoothed) tahmin edicisi ise gerçek zamanlı akışlar için tanımlanmıştır:

\[
J(i)=J(i-1)+\frac{\left|D(i-1,i)\right|-J(i-1)}{16}
\]

([RFC 3550](https://www.rfc-editor.org/rfc/rfc3550)). EH senaryolarında titreşim, kesikli/darbeli karıştırıcıların (periyodik, taramalı) imzasını taşır: ortalama gecikme fazla değişmezken titreşim patlar.

### 3.4 Karıştırma altında bildirilmiş gecikme etkileri

Hareketli karıştırıcı senaryosunda gecikme artışı %55'e kadar çıkmıştır ([Won, Youn & Ali](https://dl.ifip.org/db/conf/euc/eucw2006/WonYA06.pdf)). Merkezî karıştırma altında çok yollu detour mekanizması kullanan DMP'nin gecikme avantajı, JAM'e kıyasla yaklaşık 30 kat olarak bildirilmiştir ([Kim & Chae](https://www.mdpi.com/1424-8220/10/4/3626)). CentAir ise aldatıcı karıştırıcı altında çok-kanallı OLSR'a göre gecikmeyi %21,1 azaltmıştır ([Sarı & Seçinti](https://research.itu.edu.tr/en/publications/using-centrality-based-topology-control-for-fanet-survivability-a/)).

---

## 4. Metrik 3 — Yönlendirme Yükü (Routing Overhead)

### 4.1 Dört ayrı operasyonelleştirme

Yönlendirme yükü tek bir metrik değildir; birbirinin yerine kullanılamayan dört varyantı vardır.

| Varyant | Formül | Birim | Ne ölçer | Kaynak |
|---|---|---|---|---|
| (a) Mutlak kontrol paketi sayısı | \(O_{\mathrm{pkt}}=\sum\) atlama-başına kontrol iletimi | paket | MAC yarışma baskısı | [Broch et al.](https://pages.cs.wisc.edu/~suman/courses/740/papers/broch98mobicom.pdf) |
| (b) Kontrol baytı | \(O_{\mathrm{byte}}=\sum \mathrm{size}(m)\) | bayt | Bant genişliği tüketimi | [Das et al.](https://ebelding.cs.ucsb.edu/sites/default/files/publications/infocom00.pdf); [RFC 2501](https://www.rfc-editor.org/rfc/rfc2501) |
| (c) Normalize Yönlendirme Yükü (NRL) | \(O_{\mathrm{pkt}}/N_{\mathrm{data,delivered}}\) | boyutsuz | Teslim edilen paket başına maliyet | [Ateya et al.](https://www.mdpi.com/1999-5903/17/10/473) |
| (d) Bant genişliği ek yük oranı | toplam bit / veri biti | boyutsuz | Toplam verimlilik | [Perkins & Royer](http://www.ronai.hu/library/AODV-Perkins.pdf) |

Atlama-başına sayım kritiktir: yayınlanan (broadcast) bir RREQ, ağdaki her yeniden iletiminde ayrı ayrı sayılmalıdır; yoksa reaktif protokollerin selleme maliyeti sistematik olarak eksik ölçülür ([Broch et al.](https://pages.cs.wisc.edu/~suman/courses/740/papers/broch98mobicom.pdf)).

### 4.2 NRL'nin EH'de neden yanıltıcı olduğu

NRL'nin paydası teslim edilen veri paketi sayısıdır. Karıştırma altında bu payda çökerken pay (kontrol trafiği) rota keşfi yeniden denemeleri nedeniyle artar. Sonuç, NRL'nin **çift taraflı** olarak şişmesidir; bu yüzden NRL karıştırma altında bozulma büyüklüğünü olduğundan fazla gösterir. FANET yönlendirme saldırısı çalışmasında %20 sinkhole altında yükün 111,14'e, blackhole altında 72,77'ye çıkması bu mekanizmanın somut örneğidir ([Ceviz, Sadioglu & Sen](https://web.cs.hacettepe.edu.tr/~ssen/files/papers/AdhocNets22.pdf)). Doğru yaklaşım, NRL ile birlikte mutlak kontrol baytını da raporlamaktır: birincisi verimliliği, ikincisi kanal üzerindeki gerçek yükü verir.

AODV için bildirilen bayt tabanlı ek yük oranı aralığı 1,14–1,49'dur ([Perkins & Royer](http://www.ronai.hu/library/AODV-Perkins.pdf)); bu, karıştırma olmayan koşullar için bir taban çizgisi olarak kullanılabilir.

### 4.3 Proaktif–reaktif asimetrisi

Proaktif protokollerin yükü büyük ölçüde zamanlayıcı-güdümlüdür ve trafikten bağımsızdır: OLSR varsayılan olarak 2 s HELLO ve 5 s TC aralığı kullanır ([RFC 3626](https://www.rfc-editor.org/rfc/rfc3626.html)). Bu, karıştırma altında yükün nispeten sabit kalması ancak kurtarmanın da zamanlayıcı sınırlarına takılması anlamına gelir. Reaktif protokollerde ise yük karıştırmayla birlikte patlar, çünkü her kopan rota yeni bir selleme turu tetikler; AODV bunu RREQ_RETRIES = 2 ve RREQ_RATELIMIT ile sınırlar ([RFC 3561](https://www.rfc-editor.org/rfc/rfc3561.html)). Bu asimetri, EH altında iki protokol ailesinin aynı metrikle karşılaştırılmasının neden dikkat gerektirdiğini açıklar.

---

## 5. Metrik 4 — Bağlantı Kopma Sayısı ve Bağlantı Dinamikleri

### 5.1 Bağlantı değişim sayısı

Kanonik tanım basittir: bir düğüm doğrudan iletişim menzilinin içine girdiğinde veya dışına çıktığında bir bağlantı bağlantısallık değişimi sayılır ([Broch et al.](https://pages.cs.wisc.edu/~suman/courses/740/papers/broch98mobicom.pdf)). Aynı çalışmada bu sayının senaryo bazında 898 ile 11.857 arasında değiştiği bildirilmiştir; bu geniş aralık, metriğin hareketlilik senaryosuna aşırı duyarlı olduğunu ve mutlak değerinin ancak senaryo parametreleriyle birlikte anlamlı olduğunu gösterir.

Bir düğümün bağlantı değişim oranı, kararlı durumda yeni bağlantı varış oranının iki katıdır (her bağlantı bir kurulma ve bir kopma olayı üretir) ([Samar & Wicker](https://www.sigmobile.org/mobihoc/2004/presentations/p145-samar.pdf)). Literatürde "bağlantı değişim oranı" için kapalı biçimli bir formül bulunamamıştır; yalnızca sayım tanımlıdır ve bu durum raporlanmalıdır.

### 5.2 Bağlantı Sona Erme Süresi (LET) ve Rota Sona Erme Süresi (RET)

Sabit hızlarla hareket eden iki düğüm arasındaki bağlantının ne kadar süre ayakta kalacağı kapalı biçimde hesaplanabilir:

\[
\Delta t=\frac{-(ab+cd)+\sqrt{(a^{2}+c^{2})r^{2}-(ad-bc)^{2}}}{a^{2}+c^{2}}
\]

Burada \(r\) iletişim menzili, \(a,b,c,d\) düğümlerin hız ve konum bileşenlerinden türetilen katsayılardır ([Su, Lee & Gerla](http://shiftleft.com/mirrors/www.hpl.hp.com/personal/Sung-Ju_Lee/abstracts/papers/ijnm2001.pdf)). Bir rotanın sona erme süresi, rotayı oluşturan bağlantıların en küçük LET değeridir:

\[
\mathrm{RET}=\min_{l\in R}\mathrm{LET}_{l}
\]

FANET'te bu metrik özellikle değerlidir, çünkü yüksek hız nedeniyle LET tipik olarak protokolün HELLO aralığıyla aynı mertebeye iner; yani hareketlilik-kaynaklı kopmalar zamanlayıcı-kaynaklı algılama gecikmesiyle örtüşür.

### 5.3 EH bağlamına uyarlama: "kopma" tanımının değişmesi

Hareketlilik temelli kopma tanımı menzil geçişine dayanır; karıştırma altında ise kopma bir SINR eşiği ihlalidir. Işın sıfırlama (beam nulling) literatüründeki tanım nettir: SINR bir eşiğin altına düştüğünde alıcı düğüm karıştırılmış kabul edilir ([Bhunia, Regis & Sengupta](https://sbhunia.me/publications/manuscripts/comnet2018.pdf)). İHA yol planlama çalışmasında bu eşik için somut bir referans değer verilmiştir: \(T_s=-3\) dB ([Jamming-Resilient Path Planning for Multiple UAVs via DRL](https://ar5iv.labs.arxiv.org/html/2104.04477)).

Bu ayrım, EH değerlendirmesinde **üç ayrı kopma sayacının** tutulmasını gerektirir:

1. **Fiziksel kopma:** SINR eşiğinin altına inen bağlantı-zaman olayları (yer gerçekliği).
2. **Protokol-algılamalı kopma:** Yönlendirme protokolünün komşuluk kaybı ilan ettiği olaylar (OLSR'da NEIGHB_HOLD_TIME dolması, AODV'de ALLOWED_HELLO_LOSS aşımı).
3. **Rota geçersizleşme olayları:** Kopan bağlantı yüzünden geçersizleşen rota sayısı (AODV'de RERR üretimi).

Bu üçünün arasındaki fark, protokolün EH altındaki **algılama duyarlılığını** ölçer ve doğrudan Bölüm 6'daki kurtarma süresini belirler. FANET'e özgü karıştırma çalışmalarında bu ayrım genellikle bağlantısallık, karıştırılmış düğüm sayısı ve ada (island) sayısı olarak raporlanmıştır: ışın sıfırlama, 3B İHA mesh ağında bağlantısallığı %42,47 artırırken karıştırılmış düğüm sayısını %96,65 ve ada sayısını %91,21 azaltmıştır ([Bhunia, Regis & Sengupta](https://sbhunia.me/publications/manuscripts/comnet2018.pdf)).

### 5.4 Protokol düzeyinde kopmanın ilan edilme süresi

Bir kopmanın ne zaman "sayıldığı", protokol zamanlayıcılarının doğrudan fonksiyonudur:

| Protokol | İlgili zamanlayıcı | Varsayılan | Sonuç |
|---|---|---|---|
| AODV | HELLO_INTERVAL | 1000 ms | Algılama çözünürlüğü |
| AODV | ALLOWED_HELLO_LOSS | 2 | Kopma ilanı ≈ 2–3 s sonra |
| AODV | ACTIVE_ROUTE_TIMEOUT | 3000 ms | Kullanılmayan rota geçersizleşmesi |
| OLSR | HELLO aralığı | 2 s | Komşuluk yenileme |
| OLSR | NEIGHB_HOLD_TIME | 6 s | Komşuluk kaybı ilanı ≈ 6 s |
| OLSR | TC aralığı | 5 s | Topoloji yayılımı |
| OLSR | TOP_HOLD_TIME | 15 s | Topoloji girdisi ömrü |

AODV değerleri [RFC 3561](https://www.rfc-editor.org/rfc/rfc3561.html), OLSR değerleri [RFC 3626](https://www.rfc-editor.org/rfc/rfc3626.html) kaynaklıdır. Bu tablo, EH altında rota kurtarma süresinin alt sınırının protokol tasarımıyla önceden belirlenmiş olduğunu gösterir: hiçbir OLSR uygulaması, komşuluk kaybını 6 s'den (jitter dahil) daha hızlı ilan edemez — varsayılan zamanlayıcılarla.

### 5.5 Gerçek saha kanıtı: FANET'te bağlantı sürdürme farkı

Gerçek koşullarda yapılan bir FANET karşılaştırmasında BATMAN-adv ve Babel bağlantıları 60–70 m mesafeye kadar ayakta tutarken OLSR 40–50 m'de kopmuştur ([Guillen-Perez, Montoya, Sánchez-Aarnoutse & Cano](https://repositorio.upct.es/server/api/core/bitstreams/d2d604b7-86f5-4dea-8718-04988020241c/content)). Bu bulgu, bağlantı kopma sayısının protokolün bağlantı kalitesi metriğine (BATMAN-adv'nin TQ değeri gibi) doğrudan bağlı olduğunu ve karıştırma altında zayıf-bağlantı toleransının belirleyici olacağını gösterir.

---

## 6. Metrik 5 — Karıştırma Altında Rota Kurtarma Süresi

### 6.1 İki farklı metrik: Rota Edinme vs Rota Kurtarma

RFC 2501'in tanımladığı Rota Edinme Süresi, daha önce rotası olmayan bir hedefe rota bulunması için geçen süredir ([RFC 2501](https://www.rfc-editor.org/rfc/rfc2501)). AODV için operasyonel ölçüm reçetesi:

\[
T_{\mathrm{acq}}=t_{\text{ilk RREP alımı}}-t_{\text{ilk RREQ iletimi}}
\]

([Perkins & Royer](http://www.ronai.hu/library/AODV-Perkins.pdf)). Bu metrik EH değerlendirmesi için yetersizdir, çünkü karıştırma mevcut ve çalışan rotaları keser; sorun "rota bulma" değil "rotayı geri kazanma"dır.

### 6.2 Rota kurtarma gecikmesinin rigorous tanımı

Literatürdeki en net tanım, hem proaktif hem reaktif protokoller için geçerli olacak biçimde şöyledir:

\[
\Delta=\left|T_r-T_d\right|
\]

Burada \(T_d\), arıza nedeniyle düşürülen **ilk veri paketinin** zamanı; \(T_r\) ise kaynağın yönlendirme tablosunu yeniden hesapladığı andır ([Doghri, Reynaud & Guérin-Lassous](https://hal.science/hal-00708684v1/document)). Bu tanımın gücü, ölçümü kontrol düzlemi olaylarına değil **veri düzlemi kesintisine** bağlamasıdır; bu da karıştırma senaryolarına doğrudan uygundur.

### 6.3 OLSR için analitik yakınsama sınırları

Aynı çalışma, proaktif OLSR'ın kurtarma süresini zamanlayıcılar cinsinden sınırlar. Bir atlama komşuluk değişikliği için:

\[
\Delta_1\in\left[\mathrm{NHT}-\mathrm{HI},\ \mathrm{NHT}+\mathrm{TCI}+\mathrm{MJ}\right]
\]

İki atlama ve ötesi topoloji değişiklikleri için:

\[
\Delta_2\in\left[2\,\mathrm{TCI},\ 3\,\mathrm{TCI}\right]
\]

Burada NHT = NEIGHB_HOLD_TIME, HI = HELLO aralığı, TCI = TC aralığı, MJ = MAXJITTER ([Doghri, Reynaud & Guérin-Lassous](https://hal.science/hal-00708684v1/document); zamanlayıcı varsayılanları [RFC 3626](https://www.rfc-editor.org/rfc/rfc3626.html)). Varsayılan değerlerle (NHT = 6 s, HI = 2 s, TCI = 5 s, MJ = 0,5 s) bu \(\Delta_1\in[4;\ 11,5]\) s ve \(\Delta_2\in[10;\ 15]\) s aralıklarını verir — yani **EH altında saniyeler mertebesinde bir kesinti protokol tasarımının kaçınılmaz sonucudur**, uygulama hatası değildir.

### 6.4 Ampirik kurtarma süreleri

| Senaryo | Protokol / mekanizma | Ölçülen kurtarma süresi | Kaynak |
|---|---|---|---|
| Kablosuz çok-atlamalı benzetim | OLSR | ortalama **10,645 s** (4,818–14,545 s) | [Doghri et al.](https://hal.science/hal-00708684v1/document) |
| Aynı | MP-OLSR (çok yollu) | ortalama **13,214 s** | [Doghri et al.](https://hal.science/hal-00708684v1/document) |
| Aynı | OLSR + Fast TC (0,5 s) | <1 s (n ≤ 4) → 3 s (n = 8) | [Doghri et al.](https://hal.science/hal-00708684v1/document) |
| Aynı | OLSR + Route Extension (RE) | ≤1 s | [Doghri et al.](https://hal.science/hal-00708684v1/document) |
| 18 düğümlü gerçek NATO saha denemesi | OLSR | tüm rotaların kapanması 7,0 s / açılması 4,2 s | [Adjih et al.](https://www.sto.nato.int/publications/STO%20Meeting%20Proceedings/RTO-MP-IST-054/MP-IST-054-23.pdf) |
| 44 düğümlü mesh test yatağı | Merkezîlik tabanlı rota kurtarma (Pop-Routing) | kesinti süresinde %26 (Waxman) / %21 (caveman) azalma | [Segata et al.](https://disi.unitn.it/~msegata/bibfiles/segata2018centrality.pdf) |

Merkezîlik tabanlı yaklaşımın kullandığı toplam kesinti metriği, düğüm-başına ağırlıklı kesinti süresi olarak tanımlıdır:

\[
\tilde{L}=\sum_{h} r_h\left(T_h-T_{h-1}\right)
\]

Burada \(r_h\) etkilenen rota/düğüm sayısı, \(T_h-T_{h-1}\) ise ilgili kesinti aralığıdır ([Segata et al.](https://disi.unitn.it/~msegata/bibfiles/segata2018centrality.pdf)).

### 6.5 AODV'de yerel onarım ve süre sınırı

AODV, kopan bağlantıyı kaynağa kadar bildirmek yerine yerel onarım deneyebilir; onarım RREQ'sinin TTL değeri

\[
\mathrm{TTL}=\max\left(\mathrm{MIN\_REPAIR\_TTL},\ 0{,}5\times n_{\mathrm{hops}}\right)+\mathrm{LOCAL\_ADD\_TTL}
\]

biçiminde sınırlanır ve sonuç 'N' (no delete) bayrağıyla işaretlenir ([RFC 3561](https://www.rfc-editor.org/rfc/rfc3561.html)). Tam yeniden keşfin üst sınırı ise NET_TRAVERSAL_TIME = 2 × NODE_TRAVERSAL_TIME × NET_DIAMETER = 2 × 40 ms × 35 = 2,8 s'dir ([RFC 3561](https://www.rfc-editor.org/rfc/rfc3561.html)). Karıştırma altında bu üst sınır RREQ_RETRIES = 2 ile çarpılarak etkin olarak birkaç saniyeye çıkar — ve karıştırıcı RREQ'leri de bastırıyorsa yeniden keşif hiç tamamlanmayabilir.

### 6.6 Karıştırmaya özgü kurtarma metriği: COR

FANET karıştırma literatüründe kurtarmayı doğrudan hedefleyen tek nicel metrik, JarmRout çalışmasında tanımlanan İletişim Kurtarma Oranı'dır (Communication Recovery Ratio, COR): karıştırma sonrası **yeniden kurulan yolların, etkilenen yollara oranı** ([Pu](https://congpu.github.io/document/paper/ieee_access_2018.pdf)). Bu metrik, zaman yerine başarı oranı ölçtüğü için rota kurtarma gecikmesinin tamamlayıcısıdır: COR "kurtarılabildi mi?", \(\Delta\) ise "ne kadar sürdü?" sorusunu yanıtlar. Bir EH değerlendirmesinde ikisi birlikte raporlanmalıdır.

Not: JarmRout'un COR sayısal değerleri makalede yalnızca Şekil 8(a) ve 8(b) olarak sunulmuş, gövde metninde yalnızca eğilim verilmiştir; bu nedenle sayısal COR değerleri burada `n.a.` olarak bırakılmıştır ([Pu](https://congpu.github.io/document/paper/ieee_access_2018.pdf)).

### 6.7 Dayanıklılık ve erişilebilirlik metrikleriyle bağlantı

Kurtarma süresi, ağ dayanıklılığı literatürüne şu köprülerle bağlanır:

\[
A=\frac{\mathrm{MUT}}{\mathrm{MUT}+\mathrm{MDT}},\qquad \mathrm{MTTR}=\mathbb{E}\left[T\mid T>0\right]
\]

Burada MUT ortalama çalışma süresi, MDT ortalama kesinti süresidir ([Cholda et al., Quality of Resilience](https://resilinets.org/metrics_and_modelling.html) çerçevesiyle uyumlu olarak). Erişilebilirliğin eşdeğer formu \(A=\mathrm{MTBF}/(\mathrm{MTBF}+\mathrm{MTTR})\)'dir. ResiliNets çerçevesi ise dayanıklılığı durum-uzayı alanının normalize tümleyeni olarak tanımlar, \(R=1-\) normalize alan; referans ağlar için bildirilen değerler AT&T 0,6338, Sprint 0,5410 ve GEANT2 0,4721'dir ([ResiliNets](https://resilinets.org/metrics_and_modelling.html)). Kümülatif etki metriği ise dayanıklılık eğrisinin altındaki kayıp alanıdır:

\[
J=\int\left(P(t)-R(t)\right)dt
\]

([Infrastructure resilience curves](https://arxiv.org/pdf/2102.01009)). EH senaryolarında \(P(t)\) karıştırma öncesi başarım düzeyi, \(R(t)\) ise karıştırma sırasındaki ve sonrasındaki gerçekleşen başarım olarak alınabilir; bu, tek bir sayıyla "karıştırmanın toplam maliyeti"ni verir.

### 6.8 Kritik literatür boşluğu

Bu raporun hazırlanmasında taranan kaynaklar arasında **OLSR, AODV, BATMAN-adv, DSDV veya GPSR için RF karıştırma altında saniye ölçeğinde rota kurtarma gecikmesi bildiren hiçbir çalışma bulunamamıştır**. Yukarıdaki 6.4 tablosundaki saniye ölçekli değerler düğüm-kapatma veya kanal-değiştirme yoluyla arıza enjekte edilen MANET/mesh senaryolarından gelmektedir; karıştırmaya özgü FANET çalışmaları ise PDR, verim, bağlantısallık, ada sayısı ve COR raporlamaktadır. Dolayısıyla karıştırma dayanıklılığını bir kurtarma-süresi rakamına eşlemek, iki ayrı literatürün açıkça beyan edilen bir birleştirmesini gerektirir ve bu birleştirme yeni bir deneysel çalışmanın özgün katkısı olabilir.

---

## 7. Elektronik Harp Senaryosunun Parametrelendirilmesi

### 7.1 Karıştırıcı sınıflandırması

EH değerlendirmesinde "karıştırma" kelimesi tek başına yetersizdir; adlandırılmış bir taksonomi girdisi beyan edilmelidir.

| Karıştırıcı sınıfı | Tanımlayıcı davranış | Görev döngüsü | Protokol farkındalığı | Kaynak |
|---|---|---|---|---|
| Sürekli | MAC etiketini yok sayarak sürekli yayın | %100 | Yok | [Xu et al.](https://www.winlab.rutgers.edu/~trappe/Papers/JamDetect_Mobihoc.pdf) |
| Aldatıcı | Boşluksuz düzenli paket/preamble enjeksiyonu | %100 | Var (çerçeve formatı) | [Xu et al.](https://www.winlab.rutgers.edu/~trappe/Papers/JamDetect_Mobihoc.pdf) |
| Rastgele | \(t_j\) karıştır / \(t_s\) uyu | Rastgele | Yok | [Xu et al.](https://www.winlab.rutgers.edu/~trappe/Papers/JamDetect_Mobihoc.pdf) |
| Periyodik | Sabit aç/kapa deseni | %86, 74 µs periyot (802.11p) | Yok | [Pirayesh & Zeng](https://inss.egr.msu.edu/papers/Hossein22_COMST_jamming_survey.pdf) |
| Reaktif | Kanal etkinliği sezilince yayın | 802.11p: 40 µs sezme + 500 µs karıştırma | Var | [Xu et al.](https://www.winlab.rutgers.edu/~trappe/Papers/JamDetect_Mobihoc.pdf); [Pirayesh & Zeng](https://inss.egr.msu.edu/papers/Hossein22_COMST_jamming_survey.pdf) |
| Baraj (barrage) | İlgi bandının tamamına gürültü | %100 | Yok | [EMSOPEDIA](https://www.emsopedia.org/entries/barrage-noise/); [Lichtman et al.](https://buehrer.ece.vt.edu/content/dam/buehrer_ece_vt_edu/papers/Com_Jam_Taxonomy.pdf) |
| Spot / kısmi bant | Enerjiyi dar bantta yoğunlaştırma | Bant içinde %100 | Yok | [EMSOPEDIA](https://www.emsopedia.org/entries/spot-noise/) |
| Taramalı (swept) | Spot karıştırıcının bant boyunca gezdirilmesi | ör. 10 tarama/s, 60 MHz, ≈%60 | Yok | [EMSOPEDIA](https://www.emsopedia.org/entries/swept-jamming-against-radio-communications/) |
| Takipçi / DRFM | Anlık FHSS atlamasını sezip o frekansı karıştırma | Zaman-ilintili | Yüksek | [Lichtman et al.](https://buehrer.ece.vt.edu/content/dam/buehrer_ece_vt_edu/papers/Com_Jam_Taxonomy.pdf) |
| Kontrol kanalı | Yükü değil sinyalleşmeyi hedefleme | Kısa protokol-zamanlı patlamalar | Çok yüksek | [Lichtman et al.](https://buehrer.ece.vt.edu/content/dam/buehrer_ece_vt_edu/papers/Com_Jam_Taxonomy.pdf) |
| Akıllı / bilişsel | Kurban davranışını öğrenip uyarlama | Uyarlanır | Çok yüksek | [Herrera-Loera et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC12845974/) |

Kontrol kanalı karıştırması, yönlendirme protokolü değerlendirmesi açısından özellikle önemlidir: HELLO/TC/RREQ trafiğini seçici olarak bastıran bir karıştırıcı, veri kanalını hiç bozmadan protokolün topoloji görüşünü çökertebilir. LTE örneğinde PCFICH karıştırmanın barajdan yaklaşık 20 dB daha J/S-verimli olduğu bildirilmiştir ([Pirayesh & Zeng](https://ar5iv.labs.arxiv.org/html/2101.00292)).

### 7.2 Fiziksel katman parametreleri

Haberleşme karıştırmasında J/S oranı:

\[
\frac{J}{S}=\frac{P_j\,G_j\,R_t^{2}\,G_{r_j}}{P_t\,G_t\,R_j^{2}\,G_{r_s}\,L}
\]

Burada \(P_j\) karıştırıcı gücü, \(G_j\) karıştırıcı anten kazancı, \(R_t\) meşru bağlantı mesafesi, \(R_j\) karıştırıcı–alıcı mesafesi ve \(L\) kayıplardır ([RF Essentials](https://rfessentials.com/rf-knowledge-base/how-do-i-calculate-the-effective-radiated-power-required-for-a-communications-ja/)). Etkinlik eşikleri aynı kaynakta modülasyona göre verilmiştir: analog FM için J/S > 0–6 dB, FEC'siz sayısal QPSK için 10–15 dB, 30 dB işlem kazancı olan yayılı spektrum için 30–40 dB. Görev döngüsü düzeltmesi \(10\log(\text{görev döngüsü})\) veya \(20\log(\text{görev döngüsü})\) olarak uygulanır ([RF Cafe, EW & Radar Handbook](https://www.rfcafe.com/references/electrical/ew-radar-handbook/jamming-to-signal-ratio-constant-power.htm)).

İHA'ya özgü SINR formülasyonu, karıştırıcı girişim terimini açıkça ayırır:

\[
\mathrm{SINR}_i(t)=\frac{P_i(t)\,h^{(i,i)}_{TR}(t)}{\sum_{k\neq i,\ c_k=c_i}P_k(t)\,h^{(k,i)}_{TR}(t)+I_J^{(i)}(t)+\sigma^{2}},\qquad I_J^{(i)}(t)=P_J\,h^{(i)}_{JR}(t)
\]

([Coordinated Anti-Jamming Resilience in Swarm Networks via MARL](https://arxiv.org/html/2512.16813v1)).

### 7.3 Zorunlu raporlama listesi

| Parametre | Neden gerekli | Literatürden örnek değerler |
|---|---|---|
| Karıştırıcı iletim gücü | J/S'yi belirler; olmadan tekrarlanabilirlik yok | −4 dBm (MICA2) ([Xu et al.](https://www.winlab.rutgers.edu/~trappe/Papers/JamDetect_Mobihoc.pdf)) |
| J/S veya JSR | Bağlantının kopup kopmayacağını belirler | 0–6 / 10–15 / 30–40 dB eşikleri ([RF Essentials](https://rfessentials.com/rf-knowledge-base/how-do-i-calculate-the-effective-radiated-power-required-for-a-communications-ja/)) |
| SINR / SJR eşiği | Benzetimde "karıştırılmış" tanımını verir | \(T_s=-3\) dB ([ar5iv 2104.04477](https://ar5iv.labs.arxiv.org/html/2104.04477)) |
| Karıştırma yarıçapı / girişim menzili | Etkilenen düğüm ve bağlantı sayısını belirler | 6/12/18 m ([Won et al.](https://dl.ifip.org/db/conf/euc/eucw2006/WonYA06.pdf)); INET `interferenceRange = 500 m` ([INET](https://inet.omnetpp.org/docs/tutorials/wireless/doc/step5.html)) |
| Görev döngüsü | Etkin J/S'yi doğrudan ölçekler | %100 baraj; %86 periyodik; ≈%60 taramalı ([EMSOPEDIA](https://www.emsopedia.org/entries/swept-jamming-against-radio-communications/)) |
| Karıştırıcı sayısı | Saldırı ayak izini ölçekler | 1 karıştırıcı ([ar5iv 2104.04477](https://ar5iv.labs.arxiv.org/html/2104.04477)); 10 karıştırıcı → PSR 0,4 ([Pirayesh & Zeng](https://ar5iv.labs.arxiv.org/html/2101.00292)) |
| Karıştırıcı hareketliliği | Zaman-değişken yönlendirme boşlukları yaratır | 8/4/2/1 m/s ([Won et al.](https://dl.ifip.org/db/conf/euc/eucw2006/WonYA06.pdf)) |
| Karıştırıcı konumlandırma stratejisi | Hangi rotaların kesildiğini belirler | Ağ merkezinde karıştırma trafiği ([Kim & Chae](https://www.mdpi.com/1424-8220/10/4/3626)) |
| Spektral doluluk / bant genişliği | Barajı spot/kısmi banttan ayırır | 22 MHz WLAN karıştırıcı; 312,5 kHz tek alt-taşıyıcı ([Pirayesh & Zeng](https://inss.egr.msu.edu/papers/Hossein22_COMST_jamming_survey.pdf)) |
| Meşru düğüm hareketliliği ve kanal hata modeli | Karıştırma etkisini hareketlilik etkisinden ayırır | 802.11p, 300 m, 2 Mbps, RWP 30 m/s, %5–10 kanal hatası ([Pu](https://congpu.github.io/document/paper/ieee_access_2018.pdf)) |

2026 tarihli sistematik derleme, spektral dolulukun literatürde sistematik olarak eksik raporlandığını açıkça vurgulamaktadır ([Herrera-Loera et al.](https://pmc.ncbi.nlm.nih.gov/articles/PMC12845974/)).

### 7.4 GNSS aldatma: ayrı bir EH vektörü

Coğrafi yönlendirme (GPSR gibi) kullanılıyorsa GNSS bozma/aldatma ayrı bir bağımsız değişken olarak modellenmelidir, çünkü konum hatası bağlantıyı fiziksel olarak koparmadan yönlendirme kararını bozar. Konum sahteciliği çalışmasında %10 ve %40 sahte-konumlu düğüm için teslim oranının %4 ve %12 düştüğü, kötücül paket düşürme eklendiğinde bu kaybın %20 ve %32'ye (toplamda ≈%30) çıktığı bildirilmiştir ([Leinmüller, Schoch, Kargl & Maihöfer](https://www.uni-ulm.de/fileadmin/website_uni_ulm/iui.inst.100/institut/Papers/Prof_Weber/esas2005.pdf)).

### 7.5 Benzetici düzeyinde karıştırma uygulamaları

| Benzetici | Modül | Sağladıkları |
|---|---|---|
| ns-3 | UW NSL kablosuz karıştırma modeli | Sürekli/rastgele/reaktif/akıllı karıştırıcılar, PDR ve RSSI enstrümantasyonu ([nsnam wiki](https://www.nsnam.org/wiki/Wireless_jamming_model)) |
| ns-3 | Inria MSWiM 2022 modülü | Sürekli ve reaktif karıştırma; gerçek test yatağıyla doğrulanmış PDR ölçümü ([Bout & Loscrì](https://hal.science/hal-03765858/file/WSNIMhal.pdf)) |
| OMNeT++/INET | `NoiseSource` + skaler analog model | Gürültü kaynağı ve girişim menzili tanımı ([INET](https://inet.omnetpp.org/docs/showcases/wireless/analogmodel/doc/index.html)) |
| EMANE/CORE | Frekans manevrası senaryoları | 20 senaryo × 20 tekrar = 400 koşu, 24.000 mesaj, 950 m karıştırıcı yarıçapı ([Targowski et al.](https://www.mdpi.com/1424-8220/26/15/4785)) |
| OPNET | Darbe/tarama/tek-bant karıştırıcı | AODV/TORA/DSR verim bozulması ([Fu](https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=05d9bdfcc9629be6537c7e802719586d6c6fb89f)) |

Targowski ve arkadaşlarının çalışması özellikle dikkat çekicidir: 400 koşuluk sağlam bir istatistiksel tasarım ve açık karıştırıcı parametreleriyle (950 m yarıçap, 0,72–0,88 paket kaybı, 360°/120° sektör) frekans manevrasını değerlendirir, ancak **yönlendirme protokolünü kapsam dışı bırakır** ve "coverage continuity" adlı kendi metriğini kullanır ([Targowski et al.](https://www.mdpi.com/1424-8220/26/15/4785)). Bu, EH altında yönlendirme protokolü değerlendirmesi için doğal ve iyi tanımlanmış bir araştırma boşluğu oluşturur.

---

## 8. Hareketlilik Modeli Seçimi: Sonuçları Geçersiz Kılabilecek Bir Karar

FANET başarım karşılaştırmalarında hareketlilik modeli, karıştırıcı parametreleri kadar belirleyicidir. Rastgele Ara Nokta (Random Waypoint, RWP) modeli, sonsuz ivme ve ani yön değişimi gibi fiziksel olarak imkânsız davranışlar üretmesi nedeniyle eleştirilmiş; İHA senaryolarında "benzetim sonuçlarını ciddi biçimde yanıltabileceği" belirtilmiştir. Askerî keşif görevleri için Static, SRCM, Gauss-Markov, PRS ve DPR modelleri önerilmektedir ([Bujari, Calafate, Cano, Manzoni, Palazzi & Ronzani](https://www.math.unipd.it/~cpalazzi/papers/Palazzi-FlyModels-IJDSN.pdf)).

Hareketlilik modelinin protokol sıralamasını değiştirdiğine dair somut kanıt, çok-İHA keşif hareketlilik modelleri üzerinde yapılan karşılaştırmada görülür: AODV %81, OLSR %60 ve DSDV %46 PDR elde etmiştir. Aynı çalışma, keşif görevi başarımını yönlendirme başarımıyla birleştiren bir bileşik metrik önerir:

\[
\mathrm{RPDR}=R_t\times\mathrm{PDR}
\]

burada \(R_t\) keşif görevi tamamlama oranıdır ([Kim, Lee, Kim & Jo](https://scispace.com/pdf/fanet-routing-protocol-analysis-for-multi-uav-based-19eoyafn.pdf)). Bu tür görev-odaklı bileşik metrikler, EH senaryolarında salt ağ metriklerinden daha anlamlı olabilir: askerî bir değerlendirmede önemli olan paketin teslim edilmesi değil, görevin tamamlanmasıdır.

---

## 9. İstatistiksel Titizlik ve Tekrarlanabilirlik

### 9.1 Literatürdeki sistematik zayıflık

MANET benzetim çalışmalarının güvenilirliğini inceleyen kapsamlı bir tarama, incelenen MobiHoc bildirilerinin **%87,8'inin hiç güven aralığı raporlamadığını** ortaya koymuştur ([Kurkowski, Camp & Colagrosso](http://toilers.mines.edu/Publications/TechReports/TR11Feb05.pdf)). Aynı çalışma, ns-2'nin varsayılan tohum değeri (12345) ile çalıştırılan tekrarların bağımsız olmadığı tuzağını da belgeler. EH senaryolarında bu risk daha da büyüktür, çünkü karıştırma sonuçların varyansını belirgin şekilde artırır.

### 9.2 Uygulanması gereken kurallar

- **Bağımsız tekrar sayısı ve tohum yönetimi.** Her tekrar için bağımsız, açıkça raporlanmış PRNG tohumu kullanılmalıdır. Literatürdeki iyi uygulama örneği 10 bağımsız tohumdur ([Pu](https://congpu.github.io/document/paper/ieee_access_2018.pdf)); daha sağlam bir tasarım için 400 koşuluk (20 senaryo × 20 tekrar) örnek verilebilir ([Targowski et al.](https://www.mdpi.com/1424-8220/26/15/4785)).
- **Durdurma kuralı.** Bağıl istatistiksel hata, güven aralığı yarı genişliğinin nokta tahminine oranı olarak tanımlanır:

\[
\varepsilon_{\mathrm{rel}}=\frac{\text{GA yarı genişliği}}{\text{nokta tahmini}}
\]

Kabul edilebilir eşik olarak %5–10 önerilmektedir ([Pawlikowski](https://akaroa.canterbury.ac.nz/pdf/P1999.pdf)).
- **Isınma döneminin çıkarılması.** Kararlı durum benzetimlerinde geçici rejim verileri analize dahil edilmemelidir.
- **Karıştırıcı ve hareketlilik faktörlerinin ayrı ayrı taranması.** Faktöriyel bir tasarım (karıştırıcı sınıfı × J/S × düğüm sayısı × hareketlilik modeli) olmadan etkiler ayrıştırılamaz.

---

## 10. Konsolide Metrik Referans Tablosu

| # | Metrik (TR / EN) | Formül | Birim | Otoriter kaynak |
|---|---|---|---|---|
| 1 | Paket Teslim Oranı / PDR | \(\dfrac{\sum\left|\mathcal{R}_f\right|}{\sum\left|\mathcal{G}_f\right|}\times100\%\) | % | [Broch et al.](https://pages.cs.wisc.edu/~suman/courses/740/papers/broch98mobicom.pdf); [Xu et al.](https://www.winlab.rutgers.edu/~trappe/Papers/JamDetect_Mobihoc.pdf) |
| 1b | Paket Gönderim Oranı / PSR | \(m/n\) (MAC katmanı) | % | [Xu et al.](https://www.winlab.rutgers.edu/~trappe/Papers/JamDetect_Mobihoc.pdf) |
| 2 | Ortalama Uçtan Uca Gecikme | \(\bar D=\frac{1}{|S|}\sum_{k\in S}\left(t^k_{rx}-t^k_{tx}\right)\) | s / ms | [Ateya et al.](https://www.mdpi.com/1999-5903/17/10/473); bileşenler: [Das et al.](https://ebelding.cs.ucsb.edu/sites/default/files/publications/infocom00.pdf) |
| 2b | Gecikme yüzdelikleri (p50/p95/p99) | \(X\)'inci yüzdelik; kayıp = \(+\infty\) | s | [RFC 7679](https://datatracker.ietf.org/doc/html/rfc7679) |
| 2c | Titreşim (IPDV) | \(\frac{1}{N-1}\sum_{i=2}^{N}\left|D_i-D_{i-1}\right|\) | s | [Tu et al.](https://www.mdpi.com/1424-8220/25/24/7522) |
| 2d | Titreşim (RTP, düzleştirilmiş) | \(J(i)=J(i-1)+\frac{|D(i-1,i)|-J(i-1)}{16}\) | zaman damgası birimi | [RFC 3550](https://www.rfc-editor.org/rfc/rfc3550) |
| 3a | Kontrol paketi sayısı | \(O_{\mathrm{pkt}}=\sum\) atlama-başına kontrol iletimi | paket | [Broch et al.](https://pages.cs.wisc.edu/~suman/courses/740/papers/broch98mobicom.pdf) |
| 3b | Kontrol baytı | \(O_{\mathrm{byte}}=\sum\mathrm{size}(m)\) | bayt | [RFC 2501](https://www.rfc-editor.org/rfc/rfc2501) |
| 3c | Normalize Yönlendirme Yükü | \(O_{\mathrm{pkt}}/N_{\mathrm{data,delivered}}\) | boyutsuz | [Ateya et al.](https://www.mdpi.com/1999-5903/17/10/473) |
| 3d | Bant genişliği ek yük oranı | toplam bit / veri biti | boyutsuz | [Perkins & Royer](http://www.ronai.hu/library/AODV-Perkins.pdf) |
| 4a | Bağlantı değişim sayısı | menzil geçişi olaylarının sayımı | adet | [Broch et al.](https://pages.cs.wisc.edu/~suman/courses/740/papers/broch98mobicom.pdf) |
| 4b | Bağlantı Sona Erme Süresi (LET) | \(\Delta t=\frac{-(ab+cd)+\sqrt{(a^2+c^2)r^2-(ad-bc)^2}}{a^2+c^2}\) | s | [Su, Lee & Gerla](http://shiftleft.com/mirrors/www.hpl.hp.com/personal/Sung-Ju_Lee/abstracts/papers/ijnm2001.pdf) |
| 4c | Rota Sona Erme Süresi (RET) | \(\min_{l\in R}\mathrm{LET}_l\) | s | [Su, Lee & Gerla](http://shiftleft.com/mirrors/www.hpl.hp.com/personal/Sung-Ju_Lee/abstracts/papers/ijnm2001.pdf) |
| 4d | Karıştırılmış düğüm / ada sayısı | SINR eşiği altındaki düğüm ve bağlantısız bileşen sayısı | adet | [Bhunia, Regis & Sengupta](https://sbhunia.me/publications/manuscripts/comnet2018.pdf) |
| 5a | Rota Edinme Süresi | \(t_{\text{ilk RREP}}-t_{\text{ilk RREQ}}\) | ms | [Perkins & Royer](http://www.ronai.hu/library/AODV-Perkins.pdf); [RFC 2501](https://www.rfc-editor.org/rfc/rfc2501) |
| 5b | Rota Kurtarma Gecikmesi | \(\Delta=\left|T_r-T_d\right|\) | s | [Doghri et al.](https://hal.science/hal-00708684v1/document) |
| 5c | OLSR yakınsama sınırları | \(\Delta_1\in[\mathrm{NHT}-\mathrm{HI},\ \mathrm{NHT}+\mathrm{TCI}+\mathrm{MJ}]\); \(\Delta_2\in[2\,\mathrm{TCI},3\,\mathrm{TCI}]\) | s | [Doghri et al.](https://hal.science/hal-00708684v1/document); [RFC 3626](https://www.rfc-editor.org/rfc/rfc3626.html) |
| 5d | İletişim Kurtarma Oranı (COR) | kurulan yol / etkilenen yol | boyutsuz | [Pu](https://congpu.github.io/document/paper/ieee_access_2018.pdf) |
| 5e | Ağırlıklı toplam kesinti | \(\tilde L=\sum_h r_h\left(T_h-T_{h-1}\right)\) | düğüm·s | [Segata et al.](https://disi.unitn.it/~msegata/bibfiles/segata2018centrality.pdf) |
| 6a | Erişilebilirlik | \(A=\mathrm{MUT}/(\mathrm{MUT}+\mathrm{MDT})\) | boyutsuz | [ResiliNets](https://resilinets.org/metrics_and_modelling.html) |
| 6b | Kümülatif etki | \(J=\int(P(t)-R(t))dt\) | başarım·s | [Infrastructure resilience curves](https://arxiv.org/pdf/2102.01009) |
| 7 | Görev-ağırlıklı PDR (RPDR) | \(R_t\times\mathrm{PDR}\) | % | [Kim, Lee, Kim & Jo](https://scispace.com/pdf/fanet-routing-protocol-analysis-for-multi-uav-based-19eoyafn.pdf) |
| 8 | Bağıl istatistiksel hata | GA yarı genişliği / nokta tahmini | boyutsuz | [Pawlikowski](https://akaroa.canterbury.ac.nz/pdf/P1999.pdf) |

---

## 11. Önerilen Deney Tasarımı İskeleti

Yukarıdaki metriklerin bir arada, tutarlı ve tekrarlanabilir biçimde ölçülmesi için önerilen tasarım:

**Bağımsız değişkenler (faktöriyel):**
1. Karıştırıcı sınıfı: {yok (taban çizgisi), sürekli, reaktif, aldatıcı, taramalı} — Bölüm 7.1 taksonomisinden adlandırılmış girdiler.
2. J/S veya SINR eşiği: en az üç düzey (ör. eşiğin 3 dB altı, eşik, 3 dB üstü); eşik referansı \(T_s=-3\) dB ([ar5iv 2104.04477](https://ar5iv.labs.arxiv.org/html/2104.04477)).
3. Karıştırıcı sayısı ve konumu: {1 merkezî, 1 kenar, 3 dağıtık}.
4. Düğüm sayısı: {10, 25, 50}.
5. Hareketlilik modeli: Gauss-Markov veya PRS (RWP yalnızca kıyas amaçlı) ([Bujari et al.](https://www.math.unipd.it/~cpalazzi/papers/Palazzi-FlyModels-IJDSN.pdf)).
6. Protokol: {AODV, OLSR/OLSRv2, GPSR, BATMAN-adv} — proaktif, reaktif ve coğrafi aileleri kapsayacak biçimde.

**Bağımlı değişkenler:** Bölüm 10 tablosundaki tüm metrikler; asgari olarak PDR + PSR, \(\bar D\) ile p95, \(O_{\mathrm{pkt}}\) ile NRL, üç ayrı kopma sayacı (fiziksel / protokol-algılamalı / rota-geçersizleşme), \(\Delta=|T_r-T_d|\) ve COR.

**İstatistiksel tasarım:** Hücre başına ≥20 bağımsız tekrar, açıkça raporlanmış tohumlar, %95 güven aralıkları ve \(\varepsilon_{\mathrm{rel}}\le\%10\) durdurma kuralı ([Pawlikowski](https://akaroa.canterbury.ac.nz/pdf/P1999.pdf); [Kurkowski, Camp & Colagrosso](http://toilers.mines.edu/Publications/TechReports/TR11Feb05.pdf)).

**Enstrümantasyon:** ns-3 için UW NSL modeli veya Inria MSWiM-2022 modülü; OMNeT++ için INET `NoiseSource`; emülasyon için EMANE/CORE ([nsnam wiki](https://www.nsnam.org/wiki/Wireless_jamming_model); [Bout & Loscrì](https://hal.science/hal-03765858/file/WSNIMhal.pdf); [INET](https://inet.omnetpp.org/docs/showcases/wireless/analogmodel/doc/index.html); [Targowski et al.](https://www.mdpi.com/1424-8220/26/15/4785)).

Bu tasarım, Bölüm 6.8'de tespit edilen boşluğu — karıştırma altında protokol-spesifik rota kurtarma gecikmesinin ölçülmemiş olması — doğrudan hedefler.

---

## 12. Sonuç ve Öneriler

Elektronik harp altında FANET yönlendirme protokollerini değerlendirmek için beş metrik gereklidir ancak yeterli değildir; her biri EH bağlamına özgü bir tamamlayıcıyla eşlenmelidir:

1. **PDR** mutlaka **PSR** ile birlikte raporlanmalıdır; aksi halde reaktif karıştırma tespit edilemez ([Xu et al.](https://www.winlab.rutgers.edu/~trappe/Papers/JamDetect_Mobihoc.pdf)).
2. **Uçtan uca gecikme** yüzdeliklerle (p95/p99) ve kayıp paketlerin \(+\infty\) konvansiyonuyla raporlanmalıdır; ortalama tek başına hayatta kalan yanlılığı nedeniyle karıştırmayı iyileşme gibi gösterebilir ([RFC 7679](https://datatracker.ietf.org/doc/html/rfc7679)).
3. **Yönlendirme yükü** hem normalize (NRL) hem mutlak bayt biçiminde verilmelidir; NRL karıştırma altında çift taraflı şişer ([Ateya et al.](https://www.mdpi.com/1999-5903/17/10/473); [RFC 2501](https://www.rfc-editor.org/rfc/rfc2501)).
4. **Bağlantı kopma sayısı** üç ayrı sayaca ayrıştırılmalıdır: fiziksel (SINR eşiği), protokol-algılamalı ve rota-geçersizleştirici. Aralarındaki fark protokolün EH altındaki algılama duyarlılığıdır ([Bhunia, Regis & Sengupta](https://sbhunia.me/publications/manuscripts/comnet2018.pdf); [RFC 3626](https://www.rfc-editor.org/rfc/rfc3626.html)).
5. **Rota kurtarma süresi** \(\Delta=|T_r-T_d|\) ile veri düzlemi kesintisine bağlanmalı, COR ile birlikte raporlanmalı ve protokol zamanlayıcılarının analitik alt sınırlarına karşı yorumlanmalıdır ([Doghri et al.](https://hal.science/hal-00708684v1/document); [Pu](https://congpu.github.io/document/paper/ieee_access_2018.pdf)).

Bunların üzerine, sonuçların yorumlanabilmesi için karıştırıcı sınıfı, gücü, J/S veya SINR eşiği, görev döngüsü, spektral doluluk, karıştırıcı sayısı/konumu/hareketliliği ve meşru düğüm hareketlilik modeli ayrı ayrı beyan edilmelidir.

Nihai gözlem: mevcut literatürde karıştırma dayanıklılığı ile rota kurtarma gecikmesi iki ayrı kolda gelişmiştir. Bu iki kolu tek bir faktöriyel deneyde birleştirmek — yani protokol-spesifik \(\Delta\) değerlerini adlandırılmış karıştırıcı sınıfları ve nicel J/S düzeyleri altında ölçmek — hem bu raporun tespit ettiği boşluğu kapatır hem de EH ortamında FANET protokol seçimi için ilk doğrudan karşılaştırmalı taban çizgisini sağlar.

---

## Kaynakça (APA 7)

Adjih, C., Minet, P., Plesse, T., Laouiti, A., Plakoo, A., Badel, M., Mühlethaler, P., Jacquet, P., & Lecomte, J. (2005). Experiments with OLSR routing in a MANET. In *Military communications* (Meeting Proceedings RTO-MP-IST-054, Paper 23). NATO Research and Technology Organisation. https://www.sto.nato.int/publications/STO%20Meeting%20Proceedings/RTO-MP-IST-054/MP-IST-054-23.pdf

Ateya, A. A., et al. (2025). *Future Internet, 17*(10), 473. https://doi.org/10.3390/fi17100473 — https://www.mdpi.com/1999-5903/17/10/473

Bhunia, S., Regis, P. A., & Sengupta, S. (2018). Distributed adaptive beam nulling to survive against jamming in 3D UAV mesh networks. *Computer Networks*. https://sbhunia.me/publications/manuscripts/comnet2018.pdf

Bout, E., & Loscrì, V. (2022). An adaptable module for designing jamming attacks in WiFi networks for ns-3. In *Proceedings of the 25th International ACM Conference on Modeling, Analysis and Simulation of Wireless and Mobile Systems (MSWiM '22)*. https://doi.org/10.1145/3551659.3559059 — https://hal.science/hal-03765858/file/WSNIMhal.pdf

Broch, J., Maltz, D. A., Johnson, D. B., Hu, Y.-C., & Jetcheva, J. (1998). A performance comparison of multi-hop wireless ad hoc network routing protocols. In *Proceedings of the 4th Annual ACM/IEEE International Conference on Mobile Computing and Networking (MobiCom '98)*. ACM. https://pages.cs.wisc.edu/~suman/courses/740/papers/broch98mobicom.pdf

Bujari, A., Calafate, C. T., Cano, J.-C., Manzoni, P., Palazzi, C. E., & Ronzani, D. (2017). Flying ad-hoc network application scenarios and mobility models. *International Journal of Distributed Sensor Networks, 13*(10). https://doi.org/10.1177/1550147717738192 — https://www.math.unipd.it/~cpalazzi/papers/Palazzi-FlyModels-IJDSN.pdf

Ceviz, Ö. (2022). *Uçan tasarsız ağlara (FANET) yönelik yönlendirme saldırılarının analizi ve tespiti* [Yüksek lisans tezi]. Sivas Bilim ve Teknoloji Üniversitesi, Lisansüstü Eğitim Enstitüsü. https://acikerisim.sivas.edu.tr/dosyalar/722603_662bad6375888.pdf

Ceviz, O., Sadioglu, P., & Sen, S. (2022). Analysis of routing attacks in FANETs. In *Proceedings of AdHocNets 2022*. https://web.cs.hacettepe.edu.tr/~ssen/files/papers/AdhocNets22.pdf

Clausen, T., & Jacquet, P. (Eds.). (2003). *Optimized Link State Routing Protocol (OLSR)* (RFC 3626). Internet Engineering Task Force. https://www.rfc-editor.org/rfc/rfc3626.html

Corson, S., & Macker, J. (1999). *Mobile Ad hoc Networking (MANET): Routing protocol performance issues and evaluation considerations* (RFC 2501). Internet Engineering Task Force. https://www.rfc-editor.org/rfc/rfc2501

Das, S. R., Perkins, C. E., & Royer, E. M. (2000). Performance comparison of two on-demand routing protocols for ad hoc networks. In *Proceedings of IEEE INFOCOM 2000*. https://ebelding.cs.ucsb.edu/sites/default/files/publications/infocom00.pdf

Doghri, I., Reynaud, L., & Guérin-Lassous, I. (2012). On the recovery performance of single- and multipath OLSR in wireless multi-hop networks. In *Ad hoc networks: Third International ICST Conference, ADHOCNETS 2011* (p. 239). Springer. https://doi.org/10.1007/978-3-642-29096-1 — https://hal.science/hal-00708684v1/document

EMSOPEDIA. (n.d.). *Barrage noise*. https://www.emsopedia.org/entries/barrage-noise/

EMSOPEDIA. (n.d.). *Spot noise*. https://www.emsopedia.org/entries/spot-noise/

EMSOPEDIA. (n.d.). *Swept jamming against radio communications*. https://www.emsopedia.org/entries/swept-jamming-against-radio-communications/

Fu, T. (2012). *Modelling and simulation of jamming attacks in WLAN* [Master's thesis, East Carolina University]. https://citeseerx.ist.psu.edu/document?repid=rep1&type=pdf&doi=05d9bdfcc9629be6537c7e802719586d6c6fb89f

Guillen-Perez, A., Montoya, A.-M., Sánchez-Aarnoutse, J. C., & Cano, M.-D. (2021). A comparative performance evaluation of routing protocols for flying ad-hoc networks in real conditions. *Applied Sciences, 11*(10), Article 4363. https://doi.org/10.3390/app11104363 — https://repositorio.upct.es/server/api/core/bitstreams/d2d604b7-86f5-4dea-8718-04988020241c/content

Herrera-Loera, ., Del-Valle-Soto, C., Valdivia, L. J., Vázquez-Castillo, J., & Mex-Perera, C. (2026). A systematic review and energy-centric taxonomy of jamming attacks and countermeasures in wireless sensor networks. *Sensors, 26*(2), Article 579. https://doi.org/10.3390/s26020579 — https://pmc.ncbi.nlm.nih.gov/articles/PMC12845974/

INET Framework. (n.d.). *Analog models showcase; Wireless tutorial step 5 — interference*. https://inet.omnetpp.org/docs/showcases/wireless/analogmodel/doc/index.html ; https://inet.omnetpp.org/docs/tutorials/wireless/doc/step5.html

Kim, M., & Chae, K. (2010). DMP: Detouring using multiple paths against jamming attack for ubiquitous networking system. *Sensors, 10*(4), 3626–3640. https://doi.org/10.3390/s100403626

Kim, T., Lee, S., Kim, K. H., & Jo, Y.-I. (2023). FANET routing protocol analysis for multi-UAV-based reconnaissance mobility models. *Drones, 7*(3), Article 161. https://doi.org/10.3390/drones7030161 — https://scispace.com/pdf/fanet-routing-protocol-analysis-for-multi-uav-based-19eoyafn.pdf

Kurkowski, S., Camp, T., & Colagrosso, M. (2005). MANET simulation studies: The incredibles. *ACM SIGMOBILE Mobile Computing and Communications Review, 9*(4), 50–61. https://doi.org/10.1145/1096166.1096174 — http://toilers.mines.edu/Publications/TechReports/TR11Feb05.pdf

Leinmüller, T., Schoch, E., Kargl, F., & Maihöfer, C. (2005). Influence of falsified position data on geographic ad-hoc routing. In *Proceedings of the Second European Workshop on Security and Privacy in Ad hoc and Sensor Networks (ESAS 2005)*. https://www.uni-ulm.de/fileadmin/website_uni_ulm/iui.inst.100/institut/Papers/Prof_Weber/esas2005.pdf

Lichtman, M., Poston, J. D., Amuru, S., Shahriar, C., Clancy, T. C., Buehrer, R. M., & Reed, J. H. (n.d.). *A communications jamming taxonomy*. https://buehrer.ece.vt.edu/content/dam/buehrer_ece_vt_edu/papers/Com_Jam_Taxonomy.pdf

Naval Air Warfare Center. (n.d.). Jamming-to-signal ratio — Constant power. In *Electronic warfare and radar systems engineering handbook* (§4-10). https://www.rfcafe.com/references/electrical/ew-radar-handbook/jamming-to-signal-ratio-constant-power.htm

Ni, D., Ma, S., Du, J., Wu, Y., Zhou, C., & Xiao, H. (2026). A federated hierarchical DQN-based distributed intelligent anti-jamming method for UAVs. *Sensors, 26*(1), Article 181. https://doi.org/10.3390/s26010181

ns-3 Project. (n.d.). *Wireless jamming model* [Wiki page]. https://www.nsnam.org/wiki/Wireless_jamming_model

Pawlikowski, K. (1999). *Akaroa-2: Exploiting network computing by distributed stochastic simulation*. University of Canterbury. https://akaroa.canterbury.ac.nz/pdf/P1999.pdf

Perkins, C., Belding-Royer, E., & Das, S. (2003). *Ad hoc On-Demand Distance Vector (AODV) routing* (RFC 3561). Internet Engineering Task Force. https://www.rfc-editor.org/rfc/rfc3561.html

Perkins, C. E., & Royer, E. M. (1999). Ad-hoc on-demand distance vector routing. In *Proceedings of the Second IEEE Workshop on Mobile Computing Systems and Applications (WMCSA '99)* (pp. 90–100). IEEE. http://www.ronai.hu/library/AODV-Perkins.pdf

Pirayesh, H., & Zeng, H. (2021). *Jamming attacks and anti-jamming strategies in wireless networks: A comprehensive survey* (arXiv:2101.00292). arXiv. https://doi.org/10.48550/arXiv.2101.00292 — https://inss.egr.msu.edu/papers/Hossein22_COMST_jamming_survey.pdf

Pu, C. (2018). Jamming-resilient multipath routing protocol for flying ad hoc networks. *IEEE Access, 6*, 68472–68486. https://doi.org/10.1109/ACCESS.2018.2879758 — https://congpu.github.io/document/paper/ieee_access_2018.pdf

RF Essentials. (n.d.). *How do I calculate the effective radiated power required for a communications jammer?* https://rfessentials.com/rf-knowledge-base/how-do-i-calculate-the-effective-radiated-power-required-for-a-communications-ja/

Sarı, T. T., & Seçinti, G. (2024). Using centrality based topology control for FANET survivability against jamming. *Computer Networks, 242*, Article 110250. https://doi.org/10.1016/j.comnet.2024.110250 — https://research.itu.edu.tr/en/publications/using-centrality-based-topology-control-for-fanet-survivability-a/

Samar, P., & Wicker, S. B. (2004). On the behavior of communication links of a node in a multi-hop mobile environment. In *Proceedings of the 5th ACM International Symposium on Mobile Ad Hoc Networking and Computing (MobiHoc '04)* (p. 145). ACM. https://www.sigmobile.org/mobihoc/2004/presentations/p145-samar.pdf

Schulzrinne, H., Casner, S., Frederick, R., & Jacobson, V. (2003). *RTP: A transport protocol for real-time applications* (RFC 3550). Internet Engineering Task Force. https://www.rfc-editor.org/rfc/rfc3550

Segata, M., Facchi, N., Maccari, L., Gemmi, G., & Lo Cigno, R. (2018). Centrality-based route recovery in wireless mesh networks. https://disi.unitn.it/~msegata/bibfiles/segata2018centrality.pdf

Sterbenz, J. P. G., & Jabbar, A. (n.d.). *Resilience metrics and modelling* [ResiliNets research group web page]. University of Kansas. https://resilinets.org/metrics_and_modelling.html

Su, W., Lee, S.-J., & Gerla, M. (2001). Mobility prediction and routing in ad hoc wireless networks. *International Journal of Network Management*. http://shiftleft.com/mirrors/www.hpl.hp.com/personal/Sung-Ju_Lee/abstracts/papers/ijnm2001.pdf

Targowski, P., Łeska, S., Walczak, J., Chmielewski, S., & Furtak, J. (2026). Assessing the effectiveness of frequency manoeuvring in UAV networks under jamming and interference. *Sensors, 26*(15), Article 4785. https://doi.org/10.3390/s26154785 — https://www.mdpi.com/1424-8220/26/15/4785

Tu, ., et al. (2025). *Sensors, 25*(24), Article 7522. https://doi.org/10.3390/s25247522 — https://www.mdpi.com/1424-8220/25/24/7522

Ünal, S. D. (2026). *Impact of mobility on GPSR and AODV routing performance in FANETs* (Technical Report METU/II-TR-2026). Middle East Technical University, Informatics Institute. https://open.metu.edu.tr/bitstream/handle/11511/118337/Impact-of-Mobility-on-GPSR-and-AODV-Routing-Performance-in-FANETs.pdf

Ünsür, S., & Çelebi, H. (2024). FANET ağlar için düşük gecikmeli yönlendirme protokolü. *Bilgisayar Bilimleri ve Mühendisliği Dergisi, 17*(1), 56–66. https://dergipark.org.tr/tr/download/article-file/3802201

Won, C., Youn, J.-H., & Ali, H. (2006). Impact of high-mobility radio jamming in large scale wireless sensor networks. In *IFIP EUC Workshops Proceedings*. https://dl.ifip.org/db/conf/euc/eucw2006/WonYA06.pdf

Xu, W., Trappe, W., Zhang, Y., & Wood, T. (2005). The feasibility of launching and detecting jamming attacks in wireless networks. In *Proceedings of the 6th ACM International Symposium on Mobile Ad Hoc Networking and Computing (MobiHoc '05)*. ACM. https://www.winlab.rutgers.edu/~trappe/Papers/JamDetect_Mobihoc.pdf

Yalçın, N. O., & Boyacı, A. (2020). İnsansız hava araçlarının hareket ve yönlendirme protokollerine göre performans ölçümü. *Teknoloji ve Uygulamalı Bilimler Dergisi, 3*(1), 27–40. https://dergipark.org.tr/tr/download/article-file/1390725

Zhang, X., & Liu, J. (2023). Research on UAV swarm network modeling and resilience assessment methods. *Sensors, 24*(1), Article 11. https://doi.org/10.3390/s24010011 — https://pmc.ncbi.nlm.nih.gov/articles/PMC10780659/

### Künye Notları (şeffaflık)

Aşağıdaki alanlar bu araştırma sırasında açılan sayfalarda basılı olmadığı için doğrulanamamıştır ve atıf öncesi kontrol edilmelidir: Ateya vd. (2025) ve Tu vd. (2025) tam yazar listeleri; Bhunia vd. (2018) cilt/sayı/sayfa; Lichtman vd. yıl ve yayın yeri; Pirayesh & Zeng'in yayımlanmış dergi künyesi; Segata vd. yayın yeri; Su, Lee & Gerla cilt/sayfa; Pawlikowski yayın türü ve yılı; Doghri vd. tam sayfa aralığı; Sarı & Seçinti sayfa aralığı. Pu (2018) çalışmasındaki COR sayısal değerleri yalnızca şekil olarak sunulduğundan bu raporda `n.a.` olarak bırakılmıştır.
