# Kasıtlı RF Karıştırma ve Yüksek Mobilite Altında AODV, OLSR ve GPSR Başarısızlık Mekanizmaları

> Bu belge, protokollerin RFC düzeyindeki tasarım sabitleriyle, EH/jamming literatüründeki
> doğrulanmış kanıtlarla sentezlenmiştir. Aşağıdaki mekanizmalar teknik olarak güçlüdür;
> ancak bu üç protokol için **RF karıştırma altında doğrudan saniye-ölçekli rota-kurtarma
> kanıtı sınırlıdır** — sayısal kurtarma süreleri düğüm-kapatma/kanal-değiştirme yoluyla arıza
> enjekte edilen MANET/mesh senaryolarından gelir ([Doghri vd.](https://hal.science/hal-00708684v1/document)).

---

## 0. Ortak Arıza Zemini

Üç protokol de farklı mantıkla çalışsa da başarısızlığın ortak kökü şudur: **protokol, fiziksel
katmandaki SINR düşüşünü doğrudan görmez; onu yalnızca "kontrol paketi/beacon/HELLO kaybı"
şeklinde dolaylı ve gecikmeli bir semptom olarak algılar.** Karıştırma altında bir bağlantının
"kopması", alıcıdaki SINR'ın bir eşiğin altına düşmesidir (İHA için referans eşik
\(T_s = -3\) dB) ([ar5iv 2104.04477](https://ar5iv.labs.arxiv.org/html/2104.04477));
[Won, Youn & Ali](https://dl.ifip.org/db/conf/euc/eucw2006/WonYA06.pdf)).

Bu, üç ayrı kopma sayacının tutulmasını zorunlu kılar ([Bhunia, Regis & Sengupta](https://sbhunia.me/publications/manuscripts/comnet2018.pdf)):

1. **Fiziksel kopma:** SINR eşiği altındaki bağlantı-zaman olayları (yer gerçekliği).
2. **Protokol-algılamalı kopma:** protokolün komşuluk kaybı ilan ettiği olaylar (OLSR'da
   NEIGHB_HOLD_TIME dolması, AODV'de ALLOWED_HELLO_LOSS aşımı).
3. **Rota geçersizleşme olayları:** kopan bağlantı yüzünden geçersizleşen rota sayısı
   (AODV'de RERR üretimi).

Bu üçünün arasındaki gecikme, protokolün EH altındaki **algılama duyarlılığını** belirler ve
doğrudan rota kurtarma süresinin alt sınırını oluşturur. Yüksek mobilite bu gecikmeyi
kötüleştirir: İHA'da Bağlantı Sona Erme Süresi (LET) tipik olarak protokolün HELLO aralığıyla
aynı mertebeye iner — yani hareketlilik-kaynaklı kopmalar ile zamanlayıcı-kaynaklı algılama
gecikmesi örtüşür ([Su, Lee & Gerla](http://shiftleft.com/mirrors/www.hpl.hp.com/personal/Sung-Ju_Lee/abstracts/papers/ijnm2001.pdf)).

Ayrıca tek-metrik tuzağı: karıştırma altında PDR tek başına yanıltıcıdır. Reaktif karıştırıcıda
gönderici PSR %99–100 kalırken alıcı PDR %0'a düşebilir — saldırı gönderici tarafından
görünmez kalır ([Xu, Trappe, Zhang & Wood](https://www.winlab.rutgers.edu/~trappe/Papers/JamDetect_Mobihoc.pdf)).

---

## 1. AODV — Kontrol Düzlemi Çöküşü

### 1.1 Tek-yol bağımlılığı ve reaktif keşif yükü

AODV reaktiftir: iletişim gerektiğinde kaynak **RREQ** yayınlar, hedef/ara düğüm **RREP** ile
yanıt verir, kopan bağlantıda **RERR** üretilir ([RFC 3561](https://www.rfc-editor.org/rfc/rfc3561.html)).
Temel kırılma noktası: **rotaya özgü tek bir yol vardır, yedek yoktur.** Tek yol kopunca veri
akışı tamamen durar ve sıfırdan keşif gerekir.

### 1.2 Arıza zinciri

1. **Karıştırıcı SINR eşiğini ihlal eder** → alıcı düğümde bağlantı fiziksel olarak kopar.
2. **AODV bunu hemen görmez.** HELLO_INTERVAL = 1000 ms, ALLOWED_HELLO_LOSS = 2 olduğu için
   kopma ancak ≈2–3 s sonra "komşuluk kaybı" olarak ilan edilir; ACTIVE_ROUTE_TIMEOUT = 3000 ms
   ile kullanılmayan rota geçersizleşir ([RFC 3561](https://www.rfc-editor.org/rfc/rfc3561.html)).
3. **RERR üretilir ve yukarı akışa gönderilir** — ama karıştırıcı RERR'yi de bastırıyorsa hata
   bildirimi kaynağa ulaşmaz; kaynak rotayı hâlâ "geçerli" sanır ve kuyruğa paket biriktirmeye
   devam eder.
4. **Kaynak yerel onarım dener:** `TTL = max(MIN_REPAIR_TTL, 0,5 × hop_count) + LOCAL_ADD_TTL`
   ile sınırlı bir RREQ yeniden yayınlar. Tam yeniden keşfin üst sınırı
   `NET_TRAVERSAL_TIME = 2 × NODE_TRAVERSAL_TIME × NET_DIAMETER = 2,8 s`'dir ([RFC 3561](https://www.rfc-editor.org/rfc/rfc3561.html)).
5. **RREQ_RETRIES = 2** ile yeniden denemeler bu süreyi çarpar; karıştırma devam ediyorsa
   keşif hiç tamamlanmayabilir.
6. **Her başarısız keşif yeni bir selleme turu tetikler** → kontrol trafiği çift-taraflı
   şişer: pay (kontrol paketleri) artarken payda (teslim edilen veri) düşer. Bu, Normalize
   Yönlendirme Yükü'nün (NRL) **iki yönden** patlamasıdır
   ([Ateya vd.](https://www.mdpi.com/1999-5903/17/10/473); [RFC 2501](https://www.rfc-editor.org/rfc/rfc2501)).

### 1.3 Broadcast storm ve kısa/kararsız rota seçimi

RREQ, ağdaki her yeniden iletiminde ayrı sayılmalıdır; aksi halde reaktif protokollerin
selleme maliyeti sistematik eksik ölçülür ([Broch vd.](https://pages.cs.wisc.edu/~suman/courses/740/papers/broch98mobicom.pdf)).
Karıştırma altında bu selleme, "broadcast storm" adı verilen ciddi bir soruna dönüşür: AODV,
sequence number/message ID/hop count parametreleriyle bunu engellemeye çalışır ama FANET
ortamında başarılı değildir ([PMC11291667](https://pmc.ncbi.nlm.nih.gov/articles/PMC11291667/)).

Kritik geri-besleme döngüsü: AODV rota seçiminde yalnızca **hop sayısı** ölçütünü kullanır;
bağlantı kalitesini, hareket hızını veya karıştırma durumunu dikkate almaz
([PMC11291667](https://pmc.ncbi.nlm.nih.gov/articles/PMC11291667/)). Sonuç olarak, yeni keşfedilen
kısa rota büyük olasılıkla yine karıştırılan bölgeden geçer → rota hemen yine kopar → yeniden
keşif tetiklenir → sistem **kararlı bir başarısızlık döngüsüne** kilitlenir.

### 1.4 Neden kendi kendine toparlanamaz

- Yedek yol yoktur (AOMDV'nin çok-yollu uzantısı tam olarak bu kırığı hedefler; ancak
  korelasyonlu karıştırmada çoklu yollar aynı anda kesilebilir — mimari beklenti, doğrudan
  RF-jamming kanıtı değil).
- Keşif süreci bizzat karıştırmanın hedefidir: RREQ/RREP/RERR kontrol paketleri bastırılınca
  protokolün "hata bildirme" ve "yeni rota bulma" mekanizmaları aynı anda çalışmaz.
- Karıştırıcı hareket ediyorsa, keşfin başarıldığı an rota zaten geçersizleşmiş olabilir.

---

## 2. OLSR — Bayat Rota Israrı (Stale Topology)

### 2.1 Proaktif tablo ve MPR yapısı

OLSR proaktiftir: Çok-Nokta Aktarım (MPR) düğümleri seçilir, iki-atlamalık komşuları kapsar;
periyodik **HELLO** (2 s) ve **TC** (5 s) paketleriyle topoloji tabloları sürekli güncel tutulur
([RFC 3626](https://www.rfc-editor.org/rfc/rfc3626.html)). Rota, veri trafiğinden bağımsız,
önceden hazırdır. Bu özellik normalde düşük gecikme avantajıdır; karıştırma altında ise
**zamanlayıcı-kaynaklı sert kısıt** olur.

### 2.2 Arıza zinciri

1. **Karıştırıcı HELLO/TC paketlerini bastırır.** Kontrol trafiği zamanlayıcıya bağlı olduğu
   için yük nispeten sabit kalır — ama bu "yarar" değil tuzaktır: zamanlayıcılar yenilenmediği
   için topoloji tablosu **eski (stale) kalır**.
2. **Ölü bağlantılar tabloda yaşamaya devam eder.** Komşuluk kaybı ilanı, varsayılan
   zamanlayıcılarla NEIGHB_HOLD_TIME = 6 s dolana kadar gecikir; TOP_HOLD_TIME = 15 s ile
   topoloji girdilerinin ömrü uzar ([RFC 3626](https://www.rfc-editor.org/rfc/rfc3626.html)).
3. **MPR'ler yanlış seçilir.** MPR seçimi, HELLO'larla öğrenilen iki-atlamalık komşuluk
   bilgisine dayanır. Karıştırma bu bilgiyi bozunca, seçilen MPR'ler ya karıştırılan bölgeden
   ya da çoktan hareket etmiş düğümlerden gelir. Paketler yanlış aktarıcıya gider.
4. **Aralıklı HELLO, hold timer'ı yanlışlıkla yeniler.** Karıştırma parçalı/kesintili
   (intermittent) ise, ara sıra ulaşan tek bir HELLO, ölmekte olan komşuluğu "yaşayan"
   olarak işaretler ve hold süresini sıfırlar — bu da hatalı komşuluğu **uzatır**.

### 2.3 Kurtarma sınırları (analitik)

Doghri vd., OLSR kurtarma süresini zamanlayıcılar cinsinden sınırlar
([Doghri vd.](https://hal.science/hal-00708684v1/document)):

- Tek atlama komşuluk değişikliği için:
  \(\Delta_1 \in [\text{NHT}-\text{HI},\ \text{NHT}+\text{TCI}+\text{MJ}]\)
- İki atlama ve ötesi için:
  \(\Delta_2 \in [2\,\text{TCI},\ 3\,\text{TCI}]\)

Varsayılan değerlerle (NHT = 6 s, HI = 2 s, TCI = 5 s, MJ = 0,5 s):
\(\Delta_1 \in [4;\ 11,5]\) s ve \(\Delta_2 \in [10;\ 15]\) s. Ampirik OLSR kurtarma süresi
ortalama **10,6 s** (4,8–14,5 s) ([Doghri vd.](https://hal.science/hal-00708684v1/document)).

Sonuç: **EH altında saniyeler mertebesinde kesinti, protokol tasarımının kaçınılmaz sonucudur,
uygulama hatası değildir.** Hiçbir OLSR uygulaması, varsayılan zamanlayıcılarla komşuluk kaybını
6 s'den (jitter dahil) daha hızlı ilan edemez.

### 2.4 Kontrol-kanalı karıştırması (en zararlı senaryo)

Kontrol kanalı karıştırması, yönlendirme değerlendirmesi açısından özellikle önemlidir:
HELLO/TC trafiğini seçici olarak bastıran bir karıştırıcı, **veri kanalını hiç bozmadan**
protokolün topoloji görüşünü çökertebilir. LTE örneğinde PCFICH karıştırmanın barajdan
yaklaşık 20 dB daha J/S-verimli olduğu bildirilmiştir
([Pirayesh & Zeng](https://ar5iv.labs.arxiv.org/html/2101.00292)).

### 2.5 Neden kendi kendine toparlanamaz

- Topoloji tablosunun güncellenmesi bizzat periyodik HELLO/TC'ye bağlıdır; bunlar bastırılınca
  tablo **dondurulur** ve kararlı bir yanılgıya dönüşür.
- Yüksek mobilitede periyodik tablolar çabuk eskir; kontrol yükü sabit kalıp verim düşer
  (proaktif-asimetri).
- Gerçek saha kanıtı: BATMAN-adv ve Babel bağlantıları 60–70 m'ye kadar ayakta tutarken OLSR
  40–50 m'de kopmuştur — karıştırma altında zayıf-bağlantı toleransı belirleyici olur
  ([Guillen-Perez vd.](https://repositorio.upct.es/server/api/core/bitstreams/d2d604b7-86f5-4dea-8718-04988020241c/content)).

---

## 3. GPSR — Konum Gerçeğinin Bozulması

### 3.1 Coğrafi yönlendirme ve minimum durum

GPSR açgözlü iletim (greedy forwarding) kullanır: hedefe coğrafi olarak en yakın komşuya iletir;
açgözlü başarısız olursa çevre (perimeter) iletimiyle düzeltir. Yalnızca tek-atlamalık komşu
konum bilgisini tutar — düğüm başına durum minimumdur
([Karp & Kung, GPSR](https://www.cs.cornell.edu/people/egs/615/gpsr.pdf)).

### 3.2 Arıza zinciri — konum hattı

1. **Beacon kaybı.** GPSR komşularının konumunu periyodik beacon'larla öğrenir. Karıştırma
   beacon'ları bastırınca komşuluk tablosu **eski/yanlış koordinatlarla** dolmaya başlar.
2. **Stale neighbor coordinates.** Düğüm, çoktan hareket etmiş bir komşuya paket göndermeye
   çalışır → paket düşer. 3D FANET'te GPSR, topoloji değişimine AODV'den daha yavaş uyum sağlar
   ve PDR'yi düşürür
   ([Ünal, METU 2026](https://open.metu.edu.tr/bitstream/handle/11511/118337/Impact-of-Mobility-on-GPSR-and-AODV-Routing-Performance-in-FANETs.pdf)).
3. **Greedy local maximum (boşluk).** Hiçbir komşu hedefe mevcut düğümden daha yakın değilse
   açgözlü iletim başarısız olur → perimeter kurtarma devreye girer.
4. **Perimeter modu 3B'de zayıftır.** Standart perimeter kurtarma **düzlemsel grafik
   varsayımıyla** tasarlanmıştır (Gabriel Graph üzerinde sağ el kuralı). 3B uzayda planar
   grafik tanımı ve sağ-el-çevreleme anlamsızlaşır; void kurtarması için ek adaptasyon gerekir.
   Yüksek mobilite + karıştırmada perimeter modu, döngüler yaratarak paketleri çöpe gönderir.
5. **GPS jamming konumu anında bozar.** Konum bağımlıdır (GPS şart değil, eşdeğer bir
   lokalizasyon servisi yeterlidir; ama pratikte çoğu FANET konumu GPS/GNSS'ten alır). GPS
   jamming, düğümün kendi koordinatını bile yanlış bilmesine yol açar → açgözlü karar tamamen
   yanlış hedefe hizmet eder.

### 3.3 GPS spoofing — sahte "hedefe daha yakın" düğüm

GPSR'nin en zararlı başarısızlık biçimi **konum sahteciliğidir**. Konum hata kaynakları üç
düzeyde sınıflandırılır ([Leinmüller, Schoch, Kargl & Maihöfer](https://www.uni-ulm.de/fileadmin/website_uni_ulm/iui.inst.100/institut/Papers/Prof_Weber/esas2005.pdf)):

- **Yanlış konum beyanı (position falsification):** kötücül düğüm, hedefe kendinden daha yakın
  olduğunu iddia eden sahte konum yayınlar → tüm çevre düğümler trafiği ona yönlendirir.
- **Seçici paket düşürme:** kötücül düğüm, çektiği trafiği düşürür.
- **Sybil saldırısı:** tek bir düğüm birden çok sahte kimlik/konum yaratır
  ([arXiv 1110.1579](https://arxiv.org/ftp/arxiv/papers/1110/1110.1579.pdf)).

Sayısal kanıt: %10 ve %40 sahte-konumlu düğüm için teslim oranının **%4 ve %12** düştüğü,
kötücül paket düşürme eklendiğinde bu kaybın **%20 ve %32'ye** (toplamda ≈%30) çıktığı
gözlenmiştir ([Leinmüller vd.](https://www.uni-ulm.de/fileadmin/website_uni_ulm/iui.inst.100/institut/Papers/Prof_Weber/esas2005.pdf)).

Kritik nokta: konum sahteciliği **bağlantıyı fiziksel olarak koparmadan** yönlendirme kararını
bozar — yani §0'daki üç kopma sayacının hiçbirinde görünmez; protokol, saldırının farkında
olmadan yanlış yola paket gönderir.

### 3.4 Karıştırma + mobilite etkileşimi

Hareketli karıştırıcı senaryosunda (8→1 m/s yarıçap küçülmesi) teslim başarı oranı %10'a kadar
düşmüş; GPSR, rota bilgisinin güncellenmesini beklediği için AODV'den daha hızlı bozulmuştur
([Won, Youn & Ali](https://dl.ifip.org/db/conf/euc/eucw2006/WonYA06.pdf)). Bu, GPSR'nin
"minimum durum" avantajının, karıştırma altında "yanlış bilgiye düşük maliyetle uyma"
dezavantajına dönüşmesini gösterir.

### 3.5 Neden kendi kendine toparlanamaz

- GPSR, konum bilgisinin **doğruluğunu doğrulayamaz** — beacon'larda gelen koordinatları
  sorgusuz kabul eder. Spoofing tespit edilmezse düzeltme mümkün değildir.
- Perimeter kurtarma 3B'de tanımsız/bozuk olduğu için local-maximum'dan çıkış yolu yoktur.
- GPS jamming, düğümün **kendi** konumunu bozar; bu, beacon yayınını da bozar → hata yayılır.

---

## 4. Kısa Karşılaştırma

| Protokol | Bozulan varsayım | Arıza zinciri (özet) | Gözlenen metrik belirtisi | Neden kendi kendine toparlanamaz |
|---|---|---|---|---|
| **AODV** | RREQ/RREP/RERR kontrol paketleri ulaşır | Kopma 2–3 s gecikmeli algılanır → RERR bastırılır → yerel onarım/keşif RREQ'leri de bastırılır → her kopan rota yeni selleme turu | NRL çift-taraflı şişer; PDR düşer, gecikme artar; broadcast storm | Yedek yol yok; keşif süreci bizzat karıştırmaya tabi; rota seçimi yalnız hop sayısı → yeni rota yine jammed bölgeden |
| **OLSR** | Periyodik HELLO/TC topoloji tablosunu güncel tutar | HELLO/TC bastırılır → tablo donar → ölü bağlantılar/yanlış MPR'ler kalır → aralıklı HELLO hold timer'ı sıfırlar → hatalı komşuluk uzar | Kararlı gecikme ama kopma sayısı yüksek; kurtarma 4–15 s; yük sabit, verim düşer | Topoloji güncellemesi bizzat periyodik kontrole bağlı; zamanlayıcılar sert alt sınır koyar (NHT=6 s); kontrol-kanalı karıştırması veriyi bozmadan görüşü çökertir |
| **GPSR** | Konum bilgisi doğrudur ve perimeter 3B'de çalışır | Beacon kaybı → stale koordinatlar → local maximum → perimeter 3B'de bozuk → GPS jamming/spoofing konumu yanlışlar → sahte "yakın" düğüm trafiği çeker | PDR/verim düşük (AODV'den düşük); gecikme düşük ama teslim az; spoofing'de ≈%30 teslim kaybı | Konumun doğruluğunu doğrulayamaz; perimeter 3B'de tanımsız; GPS jamming düğümün kendi konumunu bozarak hatayı yaygınlaştırır |

---

## 5. AOMDV Notu (ilgili ama kapsam dışı)

Çok-yolluluk, AODV'nin "yedek yol yok" kırığını azaltabilir: tek yol koptuğunda kopma
algılandıysa ve alternatif yol karıştırmadan etkilenmediyse, tam yeniden keşif yapmadan yedek
yola geçebilir. Ancak bu mimari-tabanlı bir beklentidir; korelasyonlu karıştırmada (çoklu yolun
aynı coğrafi bölgeden geçmesi) tek bir karıştırıcı tüm yolları birden kesebilir ve AOMDV'nin
ek keşif yükü selleme fırtınasını ağırlaştırabilir ([Marina & Das](https://www3.cs.stonybrook.edu/~samir/Pubs/icnp-01.pdf)).

---

## Kaynakça (APA 7)

Ateya, A. A., et al. (2025). *Future Internet, 17*(10), 473. https://www.mdpi.com/1999-5903/17/10/473

Bhunia, S., Regis, P. A., & Sengupta, S. (2018). Distributed adaptive beam nulling to survive against jamming in 3D UAV mesh networks. *Computer Networks*. https://sbhunia.me/publications/manuscripts/comnet2018.pdf

Broch, J., Maltz, D. A., Johnson, D. B., Hu, Y.-C., & Jetcheva, J. (1998). A performance comparison of multi-hop wireless ad hoc network routing protocols. In *Proceedings of the 4th Annual ACM/IEEE International Conference on Mobile Computing and Networking (MobiCom '98)*. ACM. https://pages.cs.wisc.edu/~suman/courses/740/papers/broch98mobicom.pdf

Clausen, T., & Jacquet, P. (Eds.). (2003). *Optimized Link State Routing Protocol (OLSR)* (RFC 3626). Internet Engineering Task Force. https://www.rfc-editor.org/rfc/rfc3626.html

Corson, S., & Macker, J. (1999). *Mobile Ad hoc Networking (MANET): Routing protocol performance issues and evaluation considerations* (RFC 2501). Internet Engineering Task Force. https://www.rfc-editor.org/rfc/rfc2501

Doghri, I., Reynaud, L., & Guérin-Lassous, I. (2012). On the recovery performance of single- and multipath OLSR in wireless multi-hop networks. In *Ad hoc networks: Third International ICST Conference, ADHOCNETS 2011* (p. 239). Springer. https://hal.science/hal-00708684v1/document

Erritali, M., Reda, O. M., & El Ouahidi, B. (2011). A contribution to secure the routing protocol “Greedy Perimeter Stateless Routing” using a symmetric signature-based AES and MD5 hash. *International Journal of Distributed and Parallel Systems (IJDPS), 2*(5), 95–103. https://doi.org/10.5121/ijdps.2011.2509

Guillen-Perez, A., Montoya, A.-M., Sánchez-Aarnoutse, J. C., & Cano, M.-D. (2021). A comparative performance evaluation of routing protocols for flying ad-hoc networks in real conditions. *Applied Sciences, 11*(10), Article 4363. https://repositorio.upct.es/server/api/core/bitstreams/d2d604b7-86f5-4dea-8718-04988020241c/content

Hosseinzadeh, M., Husari, F. M., Yousefpoor, M. S., Lansky, J., & Min, H. (2024). A local filtering-based energy-aware routing scheme in flying ad hoc networks. *Scientific Reports, 14*, 17733. https://doi.org/10.1038/s41598-024-68471-y

Karp, B., & Kung, H. T. (2000). GPSR: Greedy perimeter stateless routing for wireless networks. In *Proceedings of the 6th Annual International Conference on Mobile Computing and Networking (MobiCom '00)* (pp. 243–254). ACM. https://www.cs.cornell.edu/people/egs/615/gpsr.pdf

Leinmüller, T., Schoch, E., Kargl, F., & Maihöfer, C. (2005). Influence of falsified position data on geographic ad-hoc routing. In *Proceedings of the Second European Workshop on Security and Privacy in Ad hoc and Sensor Networks (ESAS 2005)*. https://www.uni-ulm.de/fileadmin/website_uni_ulm/iui.inst.100/institut/Papers/Prof_Weber/esas2005.pdf

Marina, M. K., & Das, S. R. (2001). On-demand multipath distance vector routing in ad hoc networks. In *Proceedings of the Ninth International Conference on Network Protocols (ICNP 2001)* (pp. 14–23). IEEE. https://www3.cs.stonybrook.edu/~samir/Pubs/icnp-01.pdf

Perkins, C., Belding-Royer, E., & Das, S. (2003). *Ad hoc On-Demand Distance Vector (AODV) routing* (RFC 3561). Internet Engineering Task Force. https://www.rfc-editor.org/rfc/rfc3561.html

Pirayesh, H., & Zeng, H. (2021). *Jamming attacks and anti-jamming strategies in wireless networks: A comprehensive survey* (arXiv:2101.00292). arXiv. https://inss.egr.msu.edu/papers/Hossein22_COMST_jamming_survey.pdf

Su, W., Lee, S.-J., & Gerla, M. (2001). Mobility prediction and routing in ad hoc wireless networks. *International Journal of Network Management*. http://shiftleft.com/mirrors/www.hpl.hp.com/personal/Sung-Ju_Lee/abstracts/papers/ijnm2001.pdf

Ünal, S. D. (2026). *Impact of mobility on GPSR and AODV routing performance in FANETs* (Technical Report METU/II-TR-2026). Middle East Technical University, Informatics Institute. https://open.metu.edu.tr/bitstream/handle/11511/118337/Impact-of-Mobility-on-GPSR-and-AODV-Routing-Performance-in-FANETs.pdf

Wang, X., Gursoy, M. C., Erpek, T., & Sagduyu, Y. E. (2021). *Jamming-resilient path planning for multiple UAVs via deep reinforcement learning*. IEEE International Conference on Communications (ICC 2021). https://ar5iv.labs.arxiv.org/html/2104.04477

Won, C., Youn, J.-H., & Ali, H. (2006). Impact of high-mobility radio jamming in large scale wireless sensor networks. In *IFIP EUC Workshops Proceedings*. https://dl.ifip.org/db/conf/euc/eucw2006/WonYA06.pdf

Xu, W., Trappe, W., Zhang, Y., & Wood, T. (2005). The feasibility of launching and detecting jamming attacks in wireless networks. In *Proceedings of the 6th ACM International Symposium on Mobile Ad Hoc Networking and Computing (MobiHoc '05)* (pp. 46–57). ACM. https://www.winlab.rutgers.edu/~trappe/Papers/JamDetect_Mobihoc.pdf

> **Şeffaflık notu:** Ateya vd. (2025) tam yazar listesi ve Bhunia vd. (2018) cilt/sayı/sayfa, kaynak sayfalarında basılı olmadığı için doğrulanamamıştır; atıf öncesi nihai kontrol gerektirir. Karp & Kung (2000) ve Marina & Das (2001) için sayfa aralıkları, bu seminer makalelerin yerleşik bibliyografik künyelerinden alınmıştır.
