# DESPARETE v0.1 — Birleşik Candidate Specification

**Sürüm:** v0.1 candidate assembly  
**Durum:** Yazılı protokol taslağının birleşik okumasıdır; `DESIGN-ONLY`dir, deployment-ready veya frozen standard değildir.  
**Tarih:** 2026-09-21

## 1. Belgenin rolü ve üstünlük sırası

Bu belge, DESPARETE v0.1'in operasyonel davranışını tek yerde birleştirir. Yeni bir routing, wire veya security kararı üretmez. Çelişkide üstünlük sırası şöyledir:

1. `00` proje kuralları, `05` karar günlüğü ve `06` gereksinim baseline'ı;
2. bit düzeyi paket biçimi için `19`, güvenlik için `26`, sayısal metrik için `35`;
3. state/timer/algoritma için `20`…`23`;
4. bu candidate assembly ve diğer açıklayıcı/izlenebilirlik belgeleri.

v0.1, merkezî koordinatöre sürekli erişim varsaymayan, tek-sink operasyon profilli, yönlü link maliyetli ve hedef-yönlü bir FANET routing protokolüdür. Gözlenen bozunmaya ihtiyatlı tepki verir; jammer tespiti, DTN teslimi, exactly-once teslim, uçtan uca ayrık multipath veya performans optimumu iddia etmez.

## 2. Operasyon profili ve görev önkoşulları

| Konu | v0.1 kuralı |
|---|---|
| Hedef profili | İlk operasyon profili tek-sink'tir. Her node yapılandırılmış `SinkID`yi bilir; wire/field anahtarları gelecek çok-hedef profile genellenebilir kalır. |
| Kimlik ve güven | Görev öncesi TrustRoster, `Node-ID → Key-ID → Ed25519 public key` eşlemesini taşır. Rosterda olmayan node forwarding peer değildir. |
| Metrik admission | Forwarding node'lar görev öncesi aynı M0.1 metric artefaktını taşır. Mismatch veya doğrulama yoksa node forwarding rolüne alınmaz. Bu in-band algılanmaz. |
| Zaman | Her node yalnız local monotonic clock kullanır; GPS veya ağ-geneli saat eşitliği şart değildir. |
| Taşıyıcı | MTU, MAC retry/ACK ve link sonucu semantiği platform tarafından sağlanır. DESPARETE kendi fragmentation mekanizmasını tanımlamaz. |
| Deployment | DC-01…DC-11 ölçülmeden statü `DESIGN-ONLY`dir. |

Bir node'un rosterda bulunması veya authenticated paket göndermesi, onu otomatik ACTIVE komşu yapmaz. Forwarding için ayrıca yerel, iki-yönlü forwarding-grade kanıt gerekir.

## 3. Kimlikler, alan ve temel değişmezler

### 3.1 Alan anahtarı ve sürüm yetkisi

Her hedef alanı:

```text
K = (Destination-ID, Originator-Instance-ID)
```

ile anahtarlanır. Target, `K` için OIID ve 32-bit DFSN üretme yetkisine sahip tek node'dur. Target restartında yeni OIID üretir. Relay OIID/DFSN üretmez, artırmaz veya yeniden yazmaz.

DFSN ve ADS RFC 1982 serial aritmetiğiyle karşılaştırılır. `AMBIGUOUS` sonuç fail-closed'dur: field forwarding'den çıkarılır ve bounded recovery/acquisition değerlendirilir. ADS sender-local ilan sırasıdır; DFSN, Request-ID veya R1 Message Sequence değildir.

### 3.2 Safety kapısı

DATA forwarding, sırayla aşağıdakilerin hepsine bağlıdır:

1. paket biçimi, sürüm, reserved alan, authentication ve replay kabulü;
2. komşunun ACTIVE ve forwarding-grade olması;
3. field ilanının fresh, finite, REACHABLE ve doğru OIID/DFSN/ADS bağlamında olması;
4. adayın feasibility koşulunu sağlaması;
5. yerel link maliyetinin sonlu olması;
6. deterministic successor seçimi.

Policy, risk, redundancy veya timer bu kapılardan birini gevşetemez. Hop Limit/TTL yalnız hasar ve kaynak sınırıdır; loop-freedom kanıtı değildir.

### 3.3 Feasibility ve successor

`FD_i[K]=(S_FD,M_FD)` aynı DFSN içinde artırılamayan feasibility distance'tır. `j` ilanı ancak:

```text
S_j > S_FD
veya
S_j = S_FD ve P_j < M_FD
```

olduğunda feasible'dir. Equal potential feasible değildir. Safe successor ayrıca ACTIVE, fresh, finite ve sonlu maliyetli olmalıdır. Node seçildiğinde:

```text
P_i[K] = sat_add(P_j[K], C(i,j))
```

kurar. Eşit toplam maliyette düşük `(Node-ID, Instance-ID)` seçilir.

Bu kurallar altında her successor kenarında aynı DFSN bağlamı için:

```text
FD_j.metric ≤ P_j < FD_i.metric
```

olur. Bu kesin azalış, doğru çalışan node'lar ve tek target-originator önkoşulu altında data forwarding döngüsünü engeller.

## 4. Komşu yaşam döngüsü ve link gözlemi

Komşu state'leri `UNQUALIFIED → ACTIVE → STALE/SUSPECT → EXPIRED`dir.

- Roster doğrulanmış direct-peer candidate yalnız UNQUALIFIED kayıt açar.
- Node'un başlattığı nonce/matching PROBE_REPLY veya confirmed local unicast/ACK, forwarding-grade kanıttır ve ACTIVE kurabilir/yenileyebilir.
- Pasif paket duyma, incoming PROBE veya geçersiz paket ACTIVE kanıtı değildir.
- `T_fresh=3.0 s` sonunda ACTIVE komşu data adayı olmaktan çıkar; sert yerel link arızası daha erken SUSPECT/EXPIRED işlemine yol açabilir.
- `T_retention=5.0 s`, komşu/R1 state için sınırlı saklama süresidir. Invalid AUTH tek başına mevcut ACTIVE komşuyu düşürmez.

M0.1, yalnız ACTIVE direct peer için yerel `Q/H/U/R/C` üretir. Son iki saniyedeki en yeni en çok 16 link sonucu Q'yu, üç 0.5 s epochta sürekli düşüş H'yi, yaş ve örnek yetersizliği U'yu belirler. Risk:

```text
R = max(H,U)
C = 16 + C_quality(Q) + C_risk(R)
```

şeklindedir. Tablolar, eşikler ve tam test vektörleri `35`te kanoniktir. Q riskin parçası değildir; optional RF/movement gözlemleri M0.1'de routing girdisi değil diagnostic bağlamıdır.

## 5. Field ilanı, control düzlemi ve freshness

v0.1 control ailesi şunlardan oluşur:

| Tür | Kapsam | Temel işlev |
|---|---|---|
| FIELD_UPDATE | Tek-atlama | REACHABLE potential veya WITHDRAWAL ilanı; target OriginSignature zorunludur. |
| FIELD_SOLICIT | Tek-atlama | Mevcut bir alan ilanını yerel komşudan sorgular; yeniden yayılmaz. |
| DFSN_REQUEST | En çok `H_req=16` atlama | Feasibility-starvation/recovery için targettan yeni tur ister; Request-ID dedup uygulanır. |
| PROBE / PROBE_REPLY | Tek-atlama | Komşu qualification veya bounded failure doğrulaması. |
| FAILURE_REPORT | Koşullu | Sadece gerçek local delivery failure ve bağımsız safe report field varsa. |

FIELD_UPDATE'ta target `P=0` ilan eder. Ara düğüm, kendi seçilmiş successor'ı üzerinden hesaplanan potential'ını ilan eder. REACHABLE için potential sonlu, WITHDRAWAL için `∞`dir. Withdrawal finite candidate değildir.

`FIELD_UPDATE.Lifetime=3.0 s`, normal refresh `1.0 s`, solicitation guard `1.5 s` ve normal/triggered ilan coalescing sınırları `21`de tanımlıdır. Eşit/eski ADS field ömrünü uzatamaz. Daha yeni OIID eski aynı-destination field'ları atomik emekliye ayırır.

DFSN_REQUEST'in wire lifetime alanı yoktur. Zamansal sınırı `T_req_session=4.0 s`, `N_req=2`, duplicate cache ve coalescing ile; uzamsal sınırı Hop Limit ile sağlanır. Ara node isteği yeni DFSN üretme yetkisi vermez. Target, yalnız dar `FEASIBLE_STARVATION` koşulunda current DFSN'i bir artırır; diğer geçerli isteklerde current origin update'i yollar.

## 6. Field erişilebilirliği, repair ve partition

Her `K` için field state'i aşağıdakilerden biridir:

| State | DATA davranışı |
|---|---|
| FORWARDABLE | Selected safe successor üzerinden ilet. |
| REPAIRING | Yeni DATA forward edilmez; sınırlı ve uygun paket repair buffer'a alınabilir. |
| UNREACHABLE | Forwarding yoktur; yeni DATA otomatik control re-entry başlatmaz. |

Safe successor kaybolursa node önce safe alternate arar. Varsa deterministic local failover yapar. Yoksa eski/stale/feasible olmayan route'a geri dönmez; `P=∞` yapar, withdrawal ilan eder, bounded DFSN_REQUEST/acquisition başlatır ve REPAIRING'e geçer.

Class-0 için `T_buffer=6.0 s`, field/class başına buffer üst sınırı toplamın `%10`u ve en çok 32 pakettir. Süre/kapasite sonunda local delivery failure üretilir. Buffer, DTN deposu veya exactly-once mekanizması değildir. UNREACHABLE, yalnız mevcut güvenli alanın bulunmadığını söyler; global partition veya target kaybı hükmü değildir.

Yeni geçerli feasible ilan, daha yeni DFSN veya yeni OIID geldiğinde field tekrar FORWARDABLE olabilir. Eski buffer, pasif komşu duyumu veya eski field state bunu yapamaz.

## 7. Policy, alternatif ve redundancy

Policy field-localdır: `STEADY`, `CAUTION`, `PROTECT`.

| Geçiş/etki | v0.1 kuralı |
|---|---|
| STEADY → CAUTION | M0.1 `H≥64 ∨ U≥128`, `1.5 s` kesintisiz evidence. Daha sık doğrulama ve alternate izleme. |
| CAUTION → PROTECT | M0.1 `H≥128`, `2.5 s` kesintisiz evidence, ek safe successor ve traffic izni. High U tek başına yetmez. |
| Recovery | `H<64 ∧ U<128`, `4.0 s` kesintisiz evidence. PROTECT doğrudan STEADY olmaz. |
| Safety kaybı | Successor/alternate/eligibility kaybı policy dwell beklemeden güvenli eylemi durdurur. |

PROTECT, maliyete ikinci risk cezası eklemez. Yalnız protection-eligible DATA, RB>0, iki farklı immediate safe successor ve yerel kaynak bütçesi mevcutsa redundancy kullanabilir. İlk sürüm sınırı:

```text
MaxReplicaFanout = 2
Ingress RB ∈ {0,1}
```

`RB=1`de node primary + en çok bir secondary gönderir ve iki çıkışta RB `0` kalır. Kopyalar aynı immutable Data-ID taşır; duplicate cache tekrar forwarding/replication'ı bastırır. Garanti yalnız first-hop diversity'dir; uçtan uca disjointness, teslim veya sıralama garantisi yoktur.

## 8. Paket biçimi ve güvenlik profili

Her paket 4-octet taban başlıkla başlar: `Ver`, `Type`, `Header Length`, `Hop Limit`, `Base Flags`. v0.1 `Ver=1`dir; Hop Limit 0 geçersizdir; bilinmeyen critical TLV fail-closed'dur. DATA, FIELD_UPDATE, FIELD_SOLICIT, DFSN_REQUEST, PROBE, PROBE_REPLY ve FAILURE_REPORT bit düzeyi biçimleri `19`da kanoniktir.

Security Profile 1 zorunludur:

| Paket/kapsam | Zorunlu güvence |
|---|---|
| Tüm on-air paketler | Mutable son byte dizisini kapsayan Ed25519 HopSignature. Her forwardda yenilenir. |
| FIELD_UPDATE | HopSignature'a ek olarak `(Destination-ID,OIID,DFSN)` için target OriginSignature. |
| DATA | HopSignature'a ek olarak immutable Data-ID, DFlags, SourceRB ve payload için SourceSignature. |
| Control replay | Active/retention authenticated peer context'inde strict R1 high-water. |

R1 persistent receiver-restart replay koruması değildir; payload gizliliği de bu routing profile'ın parçası değildir. AUTH/replay/format reddi state'i iyimser biçimde değiştirmez ve tek paketle ACTIVE peer düşürmez.

## 9. Zamanlama, kaynak ve hata sınırları

Önemli başlangıç sınırları:

```text
T_fresh = 3.0 s          T_retention = 5.0 s
T_adv_refresh = 1.0 s    FIELD_UPDATE Lifetime = 3.0 s
H_data = H_req = 16      T_repair_max = 6.0 s
T_data_duplicate = 10 s  T_metric_epoch = 0.5 s
```

Timer önceliği: security/neighbor invalidation → withdrawal → candidate recompute → field expiry/repair → buffer termination → policy evidence. M0.1 band değişimi yalnız normal recompute ve `T_coalesce`/per-field triggered-update bütçeleriyle ilan etkisi doğurur.

Node state'i `O(d_i × f_i + b_i + duplicate-cache)`dir; roster/R1 buna `O(n+d_i)` ekler. M0.1 komşu başına en çok 16 sonuç ve üç epoch özeti taşır. Kaynak dolduğunda node yeni state/packet işini sessizce reddeder; güvenlik veya loop-safety kapısı gevşetilmez.

Hata davranışı packet sınıfına göre ağ-geneli ERROR üretmez. Format/auth/replay/duplicate hataları drop + rate-limited local telemetrydir. Local delivery failure yalnız bağımsız safe report field varsa FAILURE_REPORT üretebilir. Telemetry, uzaktan routing girdisi kabul edilmez.

## 10. Uyum ve doğrulama yükümlülükleri

Bir v0.1 implementasyonu en az aşağıdakileri gösterebilmelidir:

1. `35` M0-TV-01…M0-TV-06 tamsayı sonuçlarını üretir.
2. Stale/ambiguous OIID/DFSN/ADS, invalid AUTH/R1 ve candidate kaybında forwarding state'ini fail-closed korur.
3. RB=1 ile yalnız primary + secondary gönderir; downstream RB=0'dır.
4. ACTIVE bootstrap, repair, UNREACHABLE re-entry, withdrawal, replay ve duplicate senaryolarında `33`teki kanonik izlerle uyumludur.
5. Platforma geçişte `29`daki DC-01…DC-11'i, gerçek firmware/radio configuration üzerinde doğrular.

Vaka kimlikleri ve PASS/FAIL oracle'ları `37`de, run-level event-trace sözleşmesi `38`de, candidate-freeze kapıları ise `39`da kanoniktir. Bu belgelerin hazırlanmış olması, bu bölümdeki kanıtların henüz gösterildiği anlamına gelmez.

## 11. Bilinçli kapsam sınırları

Bu candidate specification aşağıdakileri sağlamaz veya seçmez:

- platforma özgü MTU/airtime/CPU/RAM/enerji kabulü;
- in-band metric/profile müzakeresi ya da canlı profile switch;
- R2 persistent replay, uçuş içi key lifecycle veya payload confidentiality;
- multi-sink ortak kaynak bütçesi;
- Traffic Class `1…255` için Class-0 dışı buffer/QoS profilleri;
- user tarafından üretilecek diyagramların metinle eşlenmesi;
- implementation event trace, bench/flight/simulation sonucu veya patent/FTO görüşü.

Bu sınırlar, taslağın eksik routing semantiği olduğunu değil, tasarım tamamlığı ile deployment/operasyon kanıtı arasındaki ayrımı gösterir.

## 12. Kaynak haritası

| Alan | Kanonik ayrıntı |
|---|---|
| Gereksinim ve karar | `05`, `06`, `07` |
| Model, neighbor, risk, cost, loop, freshness | `08`…`14` |
| Policy, repair, redundancy, control | `15`…`18` |
| Wire, timer, state, algorithms | `19`…`23` |
| Correctness, security, resources, telemetry, deployment | `24`…`29` |
| Entegrasyon, terimler, prior art, scenario traces | `30`…`33` |
| Metric decision ve M0.1 | `34`, `35` |
| Conformance, trace ve freeze hazırlığı | `37`…`39` |

Bu belgeyle v0.1'in yazılı candidate taslağı tek okuma akışında tamamlanmıştır. Candidate freeze, ancak `39`daki kapılara göre kullanıcı diyagram eşlemesi, final bütünleştirme denetimi, gereken proje sahibi kararı ve implementation evidence sonrası değerlendirilebilir.
