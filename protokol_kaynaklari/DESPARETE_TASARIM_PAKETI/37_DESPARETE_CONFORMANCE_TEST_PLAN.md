# DESPARETE v0.1 — Conformance ve Test Planı

**Sürüm:** v0.1 test-sözleşmesi  
**Durum:** Uygulama öncesi kabul planıdır; hiçbir testin çalıştırıldığı veya geçtiği iddiasını taşımaz.  
**Tarih:** 2026-09-21

## 1. Amaç ve sınır

Bu belge, bir DESPARETE v0.1 implementasyonunun hangi gözlenebilir davranışları üretmesi gerektiğini pass/fail ölçütlerine dönüştürür. Amaç, `36` candidate specification'ın aynı uygulama tarafından tutarlı biçimde yürütüldüğünü kanıtlamaktır.

Bu plan aşağıdakileri **yapmaz**:

- simülasyon motoru, deney matrisi veya AODV/OLSR karşılaştırması tanımlamak;
- throughput, PDR, gecikme, enerji veya uçuş performansı için başarı eşiği koymak;
- DC-01…DC-11 olmadan platform/deployment kabulü vermek;
- R2 persistent replay, payload gizliliği veya multi-sink davranışı test edilmiş gibi göstermek.

Her vaka için `PASS`, yalnız belirtilen oracle'ların tamamı event-trace veya deterministic çıktı ile kanıtlanırsa verilir. Eksik telemetry, belirsiz sonuç veya forbidden olay, `FAIL` ya da `BLOCKED` sonucudur; varsayımla PASS verilemez.

## 2. Test çalıştırma kimliği ve ortak fixture

Her run, `38`deki trace header'ını içermelidir. Minimum fixture:

| Öğeler | Sabit test varsayımı |
|---|---|
| Node'lar | Kaynak `S`, relay `A`, alternate relay `B`, target `D`; kimlikler farklıdır. |
| Field | `K=(D,OIID-1)`; target `D`, `P_D[K]=0` ve geçerli OriginSignature üretir. |
| Güven | Dört node aynı TrustRoster ve Security Profile 1 ile yapılandırılmıştır. Aksi vaka açıkça belirlenir. |
| Metric | M0.1, aynı `MetricProfile-ID`, `CostQuantum` ve tüm test vektörleriyle sağlanır. |
| Zaman | Local monotonic time kullanılır; başlangıç timer değerleri `21`den alınır. |
| Paket | Wire encoding/decoding `19`, security coverage `26`, handler sırası `23` ile uyumludur. |

Bir vaka daha küçük fixture gerektiriyorsa yalnız gerekli node'lar kullanılır. Tek bir test, önceki testin mutable state'ine güvenemez; state ya sıfırdan kurulur ya da trace header'ında fixture devamlılığı açıkça yazılır.

## 3. Ortak oracle kuralları

Her vaka aşağıdaki genel kurallara ek olarak kendi oracle'ını sağlar:

1. `DROP`, yasaklanmış bir neighbor/field/FD/policy/buffer state değişimi üretmez.
2. DATA forwarding yalnız ACTIVE + fresh + finite + feasible successor üzerinden mümkündür.
3. Timer önceliği, safety/neighbor invalidation'ı policy veya buffer eyleminden önce işler.
4. `FIELD_UPDATE`, `DATA` veya control paketinin security kapsamındaki byte'ları değişirse ilgili HopSignature yeniden doğrulanır/üretilir.
5. Test logu payload, private key, raw signature veya roster anahtar materyali içermez.

## 4. Conformance vaka matrisi

### 4.1 Metrik, preflight ve wire

| Kimlik | Kurulum / tetikleyici | PASS oracle | Başlıca kanıt |
|---|---|---|---|
| CT-MET-01 | `35` M0-TV-01…M0-TV-05 girdileri verilir. | Q/H/U/R/C sonuçları test vektörleriyle birebir aynıdır; TV-05 `∞` doyumudur. | `METRIC` eventleri veya pure-function çıktısı. |
| CT-MET-02 | M0-TV-06'daki profile mismatch. | Node forwarding admission alamaz; `metric_preflight_reject` artar; field/neighbor forwarding state'i açılmaz. | Preflight sonucu + counter. |
| CT-MET-03 | Q bandı değişmeden ardışık metric epochlar. | Yeni triggered FIELD_UPDATE yalnız metric epoch nedeniyle planlanmaz. | `METRIC` + `CONTROL` event sırası. |
| CT-WIRE-01 | Her v0.1 paket türü minimum geçerli biçimde encode/decode edilir. | Alanlar aynı semantiğe round-trip döner; Header Length ve alignment geçerlidir. | Decode özeti; raw key/payload yok. |
| CT-WIRE-02 | Reserved bit, malformed length, Hop Limit 0 veya unknown critical TLV verilir. | Paket drop olur; yalnız format/hop-limit sayacı artar; state değişmez. | `SECURITY`/`CONTROL` eventleri. |

### 4.2 Authentication, replay ve komşu nitelendirme

| Kimlik | Kurulum / tetikleyici | PASS oracle | Başlıca kanıt |
|---|---|---|---|
| CT-SEC-01 | Bad HopSignature, unknown Key-ID veya yanlış Origin/SourceSignature içeren paket. | Drop; mevcut ACTIVE peer düşmez; `rx_drop_auth` artar. | `SECURITY` event + önce/sonra neighbor snapshot. |
| CT-SEC-02 | Aynı authenticated control Message Sequence yeniden veya belirsiz sırada gelir. | Drop; R1 high-water geri sarmaz; field/timer yenilenmez. | `SECURITY replay-reject` + AR snapshot. |
| CT-SEC-03 | FIELD_UPDATE relay tarafından forward edilir; mutable Hop Limit/Control Sender Block değişir. | OriginSignature korunur; yeni HopSignature geçerlidir. | Security verification özeti. |
| CT-NEI-01 | Roster doğrulanmış direct-peer candidate ilk kez görünür. | Yalnız UNQUALIFIED kayıt açılır; successor adaylığı oluşmaz. | `NEIGHBOR` event. |
| CT-NEI-02 | Node'a hedefli geçerli incoming PROBE, peer için R1 state'i yokken alınır. | İlk R1 high-water atomik kurulur; PROBE_REPLY gönderilir ve outbound qualification planlanır; peer UNQUALIFIED kalır. | `SECURITY R1_INITIALIZED`, `CONTROL` + `NEIGHBOR` eventleri. |
| CT-NEI-03 | Node'un başlattığı matching PROBE_REPLY veya confirmed local unicast/ACK alınır. | Peer ACTIVE olur; `T_fresh`/`T_retention` yenilenir. | `NEIGHBOR ACTIVE` event + timer snapshot. |
| CT-NEI-04 | ACTIVE peer için `T_fresh` dolar veya authenticated local link failure oluşur. | Candidate'ler atomik çıkarılır; STALE/SUSPECT/EXPIRED yolu ve gerekiyorsa repair başlar. | `NEIGHBOR` ardından `FIELD`/`ACQUISITION` sırası. |

### 4.3 Freshness, field ve loop-safety

| Kimlik | Kurulum / tetikleyici | PASS oracle | Başlıca kanıt |
|---|---|---|---|
| CT-FLD-01 | ACTIVE peer'dan fresh, finite, feasible ve origin-authenticated FIELD_UPDATE gelir. | Candidate cache yazılır; deterministic recompute yalnız uygun koşulda FORWARDABLE/successor üretir. | `FIELD` event + successor snapshot. |
| CT-FLD-02 | Eşit/eski ADS veya expired ilan gelir. | Lifetime uzamaz; candidate/FD/successor geriye dönmez. | `FIELD freshness-reject` + expiry snapshot. |
| CT-FLD-03 | DFSN kıyaslaması `AMBIGUOUS` olur. | Field fail-closed olur; eski field geri açılmaz; bounded recovery değerlendirilir. | `FIELD` + `ACQUISITION` eventleri. |
| CT-FLD-04 | Yeni, geçerli OIID kabul edilir. | Aynı Destination-ID için retired field'ler atomik forwarding dışı kalır. | Retire + yeni field snapshot. |
| CT-FLD-05 | AR/R1 kaydı saklanan fakat ACTIVE olmayan peer'dan, geçerli OriginSignature taşıyan yeni OIID update'i gelir. | Update yalnız tanısal kayda girer; mevcut field'ler retire edilmez, candidate/FD/successor/repair state'i değişmez. | Önce/sonra field snapshot + diagnostic event. |
| CT-LOOP-01 | Aynı DFSN'de `P_j = M_FD` olan candidate verilir. | Candidate feasible değildir; successor kurulmaz. | Feasibility karar kaydı. |
| CT-LOOP-02 | İki feasible candidate eşit `Cost(a,j)` üretir. | Küçük unsigned `(Node-ID, Instance-ID)` seçilir. | `FIELD successor-changed` event. |
| CT-LOOP-03 | Feasible alternatif yokken maliyet artışı/successor kaybı oluşur. | FD aynı DFSN'de yükselmez/sıfırlanmaz; withdrawal + repair başlar. | FD önce/sonra + `FIELD`/`CONTROL` trace. |
| CT-DFSN-01 | Ara node FEASIBLE_STARVATION dışı request veya current+1 olmayan minimum ile target davranışını tetikler. | Target yeni DFSN üretmez; current origin update davranışı uygulanır. | Target control trace. |

### 4.4 Repair, partition ve policy

| Kimlik | Kurulum / tetikleyici | PASS oracle | Başlıca kanıt |
|---|---|---|---|
| CT-REP-01 | Primary başarısız, en az bir safe alternate hâlâ vardır. | Deterministic local failover; REPAIRING'e gereksiz giriş yoktur. | `FIELD successor-changed` event. |
| CT-REP-02 | Primary başarısız, safe alternate yoktur. | `P=∞`, withdrawal, REPAIRING, bounded solicit/request sırası; eski route kullanılmaz. | `FIELD` → `CONTROL` → `ACQUISITION` trace. |
| CT-REP-03 | `T_repair_max` sonunda valid successor hâlâ yoktur. | UNREACHABLE; Class-0 buffer ömrü/quota sonunda yalnız local delivery failure. | `FIELD unreachable`, `DATA` eventleri. |
| CT-REP-04 | Valid feasible update veya yeni OIID/DFSN healing sırasında gelir. | Field FORWARDABLE olur; yalnız ömrü dolmamış HELD DATA iletilir. | `FIELD` ardından `DATA` trace. |
| CT-POL-01 | `H≥64` veya `U≥128` 1.5 s süreklidir. | STEADY → CAUTION; ekstra gözlem/alternate hazırlığı vardır, safety gate değişmez. | `METRIC` + `POLICY` trace. |
| CT-POL-02 | Yalnız `U` yüksek, H `<128`dir. | PROTECT/redundancy açılmaz. | `POLICY` snapshot + replica sayacı. |
| CT-POL-03 | `H≥128`, 2.5 s kanıt, safe alternate ve traffic izni vardır. | CAUTION → PROTECT; safety koşulları tekrar doğrulanır. | `POLICY` event. |
| CT-POL-04 | PROTECT'te safe alternate veya forwarding eligibility kaybolur. | Replication derhal kapanır; `T_protect_min` beklenmez. | `POLICY` + `FIELD`/`DATA` trace. |

### 4.5 DATA, redundancy, admission ve gözlemlenebilirlik

| Kimlik | Kurulum / tetikleyici | PASS oracle | Başlıca kanıt |
|---|---|---|---|
| CT-DATA-01 | UNREACHABLE field'e yeni DATA gelir. | DATA otomatik acquisition/re-entry başlatmaz; local failure davranışı uygulanır. | `DATA` + field snapshot. |
| CT-DATA-02 | PROTECT, iki safe successor, eligible DATA ve `RB=1`. | En çok primary + bir secondary çıkar; iki kopyada RB=0; Data-ID aynıdır. | İki `DATA_FORWARDED` event + RB değerleri. |
| CT-DATA-03 | Same Data-ID tekrar gelir. | Duplicate drop; yeni buffer/forward/replica yoktur. | `rx_drop_duplicate` + state snapshot. |
| CT-DATA-04 | Buffer quota/lifetime veya replica/control budget doludur. | Kaynak reddi/local failure; unsafe route, ek request veya extra replica oluşmaz. | `RESOURCE` + `DATA` trace. |
| CT-OBS-01 | 10.000 malformed/bad-signature paket gönderilir. | Ağ error mesajı yoktur; rate-limited/coalesced counter vardır; existing safety state değişmez. | Counter delta + on-air control sayımı. |
| CT-OBS-02 | FAILURE_REPORT için bağımsız FORWARDABLE report field yoktur. | Local failure görünür; report-suppressed artar; ağ mesajı gönderilmez. | `DATA` counter + tx trace. |

## 5. Kanonik senaryo kapsamı

`33`teki 17 masa-başı senaryo, aşağıdaki test aileleriyle runtime kanıtına bağlanır:

| Senaryo ailesi | En az conformance vakaları |
|---|---|
| Kararlı ağ / yarışan next hop | CT-FLD-01, CT-LOOP-02, CT-DATA-03 |
| Kademeli/sudden bozunma, hız, girişim | CT-MET-01, CT-POL-01…04, CT-NEI-04 |
| Stale/ambiguous/eşzamanlı field değişimi | CT-FLD-02…05, CT-LOOP-01…03 |
| Repair, no candidate, partition, healing | CT-REP-01…04, CT-DATA-01 |
| Alternatif/redundancy | CT-DATA-02…04 |
| Restart, replay, sahte/bayat bilgi | CT-SEC-01…03, CT-NEI-01…03, CT-FLD-04 |

Her 17 senaryo için en az bir pass/fail event-trace, gerçek implementasyon kanıtı tamamlanırken eklenmelidir. Aynı trace birden fazla vaka için kullanılabilir; ancak hangi oracle'ları kanıtladığı açıkça listelenmelidir.

## 6. Sonuç sınıfları ve kanıt paketi

| Sonuç | Anlam |
|---|---|
| PASS | Vakanın tüm oracle'ları, trace ve ilgili deterministic çıktı ile kanıtlandı. |
| FAIL | Bir oracle veya yasak davranış ihlal edildi. |
| BLOCKED | Testi yürütmek için gereken link-feedback, crypto, timer veya telemetry kanıtı yok. |
| NOT-RUN | Test henüz yürütülmedi; PASS/FAIL çıkarılamaz. |

Her test sonucu şu minimum bilgileri içerir: `Test-ID`, run kimliği, implementation revision/build kimliği, fixture, PASS/FAIL/BLOCKED/NOT-RUN, trace dosyası/segmenti, oracle özeti, ilgili counter delta ve varsa sapma açıklaması.

## 7. Gerekli çıkışlar ve açık sınır

Bir implementasyon conformance iddiası yapmadan önce en az şunları vermelidir:

1. CT-MET-01…03 için deterministic çıktı;
2. CT-WIRE/SEC/NEI/FLD/LOOP/REP/POL/DATA/OBS aileleri için trace kanıtı;
3. `38`e uygun ve correlate edilebilir event-trace;
4. DC-11 link-feedback semantiğinin mevcut olduğuna dair platform kanıtı;
5. `39`daki implementation ve deployment kapılarının durum raporu.

Bu belge test kodu, test runner veya platform artefaktı değildir. Bunlar ortaya çıktığında bu planın kimlikleri değişmeden test otomasyonuna bağlanır.
