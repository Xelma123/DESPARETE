# DESPARETE — Terimler ve Uyum Dili

**Sürüm:** 0.1 (kanonik terim sözlüğü; normatif davranışları değiştirmez)  
**Durum:** `08`…`39` belgelerinde kullanılan terimleri tekilleştirir ve NFR-06'nın sözlük bölümünü karşılar. Çelişkide, `05`teki kararlar ve `19`…`26`daki normatif wire/security tanımları üstündür.  
**Tarih:** 2026-09-21

## 1. Uyum dili ve belge statüsü

- **MUST / ZORUNLU:** Uyumlu v0.1 davranışı için gereklidir.
- **MUST NOT / YASAK:** Uyumlu bir düğümün yapması yasaktır.
- **SHOULD / GÜÇLÜ ÖNERİ:** Gerekçeli profil istisnası olabilir; istisna görünür biçimde kaydedilmelidir.
- **MAY / İSTEĞE BAĞLI:** Çekirdek v0.1 uyumu için gerekli değildir.
- **Onaylı:** Proje sahibinin kabul ettiği tasarım yönü veya ayrıntı; ilgili karar `05`te bulunur.
- **Profile bağlı:** Çekirdek semantik tanımlıdır; sayısal değer veya kapasite seçilen platform/misyon profiline bırakılmıştır.
- **DESIGN-ONLY:** Protokol semantiğinin yazılı olduğu, ancak DC-01…DC-11 kapasite kanıtı olmadan deployment-ready olmadığı durumdur.

## 2. Kimlikler, roller ve kapsama ait terimler

| Terim | Kanonik anlam | Birincil kaynak |
|---|---|---|
| Node | DESPARETE çalıştıran tek bir ağ düğümü. | `19`, `23` |
| Node-ID | Wire'da 64-bit opaque düğüm kimliği. Deterministik tie-break için unsigned karşılaştırılabilir; anlam çıkarılmaz. | `19`, `23` |
| Instance-ID | Node yeniden başlatıldığında/örnek değiştiğinde ayırt etmeye yarayan 64-bit opaque örnek kimliği. | `14`, `19`, `26` |
| SinkID | Tek-sink v0.1 operasyon profilindeki yapılandırılmış application destination. | `22`, `23` |
| Destination-ID | Bir routing field'ın hedef kimliği. Tek-sink profilinde SinkID ile eşleşir. | `14`, `19` |
| `K` | Field anahtarı: `(Destination-ID, OIID)`. | `14`, `19`, `23` |
| Target / originator | `K` için OIID ve DFSN üretme yetkisi bulunan Destination-ID sahibi node. Relay bu yetkiyi kazanmaz. | `13`, `14`, `23`, `26` |
| Direct-peer candidate | Yerel link katmanı tarafından görünür kılınan veya bu node'a hedefli authenticated PROBE ile görülen roster doğrulanmış tek-atlama aday. Forwarding kanıtı ve ACTIVE komşu değildir. | `10`, `22`, `23`, `26` |
| Authenticated peer | HopSignature/roster kapısından geçen, belirli `(Sender-ID, Sender-Instance-ID)` bağlamındaki peer. Bu, tek başına forwarding-grade değildir. | `26` |

## 3. Komşuluk, gözlem ve maliyet terimleri

| Terim | Kanonik anlam | Birincil kaynak |
|---|---|---|
| `N_i[j]` | `i` düğümünün `j` için yerel neighbor kaydı. Yönlüdür; `N_i[j]`, `N_j[i]` değildir. | `10`, `22` |
| Forwarding-grade kanıt | `i → j` yönünü kanıtlayan, `i`nin başlattığı eşleşen PROBE_REPLY veya uygun confirmed local unicast/ACK. | `10`, `20`, `23` |
| UNQUALIFIED | Direct-peer candidate için başlangıç kaydı; data successor olamaz. | `22`, `23` |
| ACTIVE | Güncel forwarding-grade iki-yönlü kanıtı olan komşu. Yalnız candidate değerlendirmesine girebilir; route garantisi değildir. | `10`, `22` |
| STALE | Forwarding-grade tazeliği dolmuş komşu; data successor olamaz. | `10`, `20`, `22` |
| SUSPECT | Sert hata veya failure-bound doğrulama gerektiren komşu; data successor olamaz. | `10`, `22` |
| EXPIRED | Neighbor/ilan/candidate kullanımından çıkarılmış kayıt. Yeni doğrudan kanıt yalnız UNQUALIFIED kayıt açar. | `10`, `22`, `23` |
| `Q(i,j)` | `i → j` yönündeki mevcut doğrudan teslim koşulu kestirimi. Risk değildir. | `11`, `12` |
| `H(i,j)` | Bağın karar ufkunda uygunsuzlaşma eğilimi (hazard). Kalibre edilmiş kopma olasılığı değildir. | `11` |
| `U(i,j)` | Yaş, örnek yetersizliği, kaynak yokluğu veya çelişkiden doğan epistemik belirsizlik. | `11` |
| `R(i,j)` | `g(H,U)` ile türetilen yönlü ihtiyat indeksi. `Q`yu tekrar içermez ve jamming hükmü değildir. | `11`, `12` |
| M0.1 | Görev öncesi ortak, `DESIGN-ONLY` metrik profili. `Q/H/U/R` tamsayı algoritmaları, `R=max(H,U)`, maliyet tabloları ve policy predicate'lerini tanımlar. | `35` |
| MetricProfile-ID | Wire'da taşınmayan, görev öncesi admission ile bütün forwarding node'larda aynı olduğu doğrulanması gereken metrik artefakt kimliği. M0.1 için `M0.1`. | `34`, `35` |
| CostQuantum | Potential ve link maliyetinin ortak unsigned tamsayı kuantası; fiziksel birimi yoktur. M0.1 bütün maliyet tablolarını aynı kuantada verir. | `19`, `35` |
| `T_metric_epoch` | M0.1 Q/H/U/R/C yeniden hesaplama periyodu; v0.1'de `0.5 s`. | `23`, `35` |
| `CautionEvidence` / `ProtectEvidence` / `RecoveryEvidence` | M0.1'in sırasıyla CAUTION, PROTECT ve toparlanma policy timerlarını besleyen sayısal predicate'leri. Safety gate değildir. | `15`, `22`, `35` |
| Jamming evidence | Yerel bozunma örüntüsünün jamming ile uyumuna ilişkin, kesin teşhis olmayan ek kanıt. | `11`, `25`, `26` |
| `C(i,j)` | Sonlu, yönlü link maliyeti: `C_hop + C_quality(Q) + C_risk(R)`. Uygunluk/safety kapısı değildir. | `12`, `23` |

## 4. Field, freshness ve forwarding terimleri

| Terim | Kanonik anlam | Birincil kaynak |
|---|---|---|
| OIID | Originator Instance ID. Target restartında değişen, field instance kimliği. | `14`, `19`, `23` |
| DFSN | Hedefin ürettiği 32-bit Destination Field Sequence Number. Ara node artırmaz/üretmez. | `13`, `14`, `19`, `23` |
| ADS | Sender-local 32-bit Advertisement Serial. Aynı DFSN içindeki ilan sırasını taşır; DFSN değildir. | `18`, `19`, `23` |
| Serial comparison | RFC 1982 ile `NEWER`, `EQUAL`, `OLDER` veya `AMBIGUOUS` sonucu. AMBIGUOUS fail-closed'dur. | `14`, `19`, `23` |
| Potential `P_i[K]` | `i`nin `K` alanına ait mevcut toplam yönlendirme maliyeti. `∞` forwarding için kullanılamaz. | `12`, `13`, `23` |
| Advertised potential | Bir komşunun FIELD_UPDATE içinde ilan ettiği potential. Relay kendi değerini taşır; target yetkisi vermez. | `18`, `19`, `23` |
| FD | Feasibility distance: aynı DFSN'de yükselmeyen/sıfırlanmayan `(sequence, metric)` sınırı. | `13`, `23`, `24` |
| Candidate | ACTIVE komşudan gelen fresh, finite, REACHABLE ve sonlu maliyetli field ilanı. | `23` |
| Feasible / safe candidate | FD/DFSN koşulunu geçerek successor olabilen candidate. | `13`, `23`, `24` |
| Successor | Bir `K` için seçilmiş tek bir primary safe candidate. | `13`, `22`, `23` |
| Safe alternate | Primary dışında tüm candidate ve feasibility koşullarını geçen alternatif. Uçtan uca bağımsız yol garantisi değildir. | `17`, `23` |
| WITHDRAWAL | Sonlu local field durumunun artık forward edilemediğini sıralı biçimde ilan eden FIELD_UPDATE state'i. Finite candidate değildir. | `16`, `18`…`20`, `23` |
| FORWARDABLE / REPAIRING / UNREACHABLE | Field erişilebilirlik durumları: safe successor ile iletilebilir / bounded recovery sürüyor / recovery sonlanmış ve successor yok. | `16`, `22`, `23` |

## 5. Paket, güvenlik ve replay terimleri

| Terim | Kanonik anlam | Birincil kaynak |
|---|---|---|
| Control packet | FIELD_UPDATE, FIELD_SOLICIT, DFSN_REQUEST, PROBE, PROBE_REPLY veya FAILURE_REPORT. | `18`, `19`, `26` |
| DATA | Application payload taşıyan, SourceSignature zorunlu veri paketi. | `19`, `23`, `26` |
| Data-ID | Source identity/instance/sequence bileşimiyle tanımlanan duplicate-suppression kimliği. | `17`, `19`, `23` |
| Message Sequence | Control sender block içindeki R1 high-water sıralama değeri. Request-ID veya ADS değildir. | `19`, `23`, `26` |
| Request-ID | DFSN_REQUEST'in wave duplicate bastırma kimliği. R1 Message Sequence'den ayrıdır. | `18`, `19`, `23` |
| Replication-Budget (RB) | Bir DATA'nın ilave çoğaltma hakkı. v0.1 ingress değeri yalnız 0 veya 1'dir. | `17`, `19`, `23` |
| SourceRB | DATA source'unun imzaladığı başlangıç RB sınırı. Transit node current RB'yi bunun üstüne çıkaramaz. | `19`, `23`, `26` |
| TrustRoster | Görev öncesi `Node-ID → Key-ID → Ed25519 public key` doğrulama eşlemesi. | `26`, `29` |
| HopSignature | Her on-air paketin mutable son halini hop göndericisiyle bağlayan Ed25519 imzası. Her forwardda yenilenir. | `19`, `23`, `26` |
| OriginSignature | FIELD_UPDATE için target'ın `(Destination-ID,OIID,DFSN)` yetkisini bağlayan imza. | `19`, `23`, `26` |
| SourceSignature | DATA source'unun immutable Data-ID, flags, SourceRB ve payload'unu bağlayan imza. | `19`, `23`, `26` |
| R1 | Active/retention authenticated peer context'inde strict control high-water anti-replay profili. State yoksa yalnız active peer, hedefli ilk authenticated PROBE veya eşleşen pending PROBE_REPLY ilk kaydı kurabilir; bu kayıt ACTIVE kanıtı değildir. Receiver restartı sonrası persistent koruma değildir. | `23`, `26` |
| `AR_i` | `i`nin `(Sender-ID, Sender-Instance-ID)` için tuttuğu son kabul edilmiş R1 Message Sequence kaydı. Direct-peer candidate'in imzalı Sender-Instance'ı ilk kabul edildiğinde açılır ve EXPIRED'a kadar tutulur. | `20`, `23`, `26` |

## 6. Zaman, kaynak ve hata terimleri

| Terim | Kanonik anlam | Birincil kaynak |
|---|---|---|
| Local monotonic clock | Node'un timerları için kullandığı, node'lar arası eşitlenmesi gerekmeyen yerel saat. | `20` |
| `T_fresh` / `T_retention` | Sırasıyla forwarding-grade tazelik ve neighbor/AR kayıt saklama süresi. | `20`, `21`, `23` |
| Qualification probe | UNQUALIFIED direct-peer candidate'i ACTIVE yapmak için node'un başlattığı, nonce-bağlı bounded PROBE oturumu. | `20`…`23`, `26` |
| Failure-bound probe | STALE/SUSPECT komşu için `N_probe` ile sınırlı yeniden doğrulama oturumu. | `20`, `21`, `23` |
| `H_data` / `H_req` | Sırasıyla DATA ve DFSN_REQUEST Hop Limit profile sınırı. v0.1'de ikisi de 16'dır. | `21`, `23`, `24` |
| Local delivery failure | Data'nin yerel node'da iletilemediğini bildiren event. Ağ-geneli ERROR paketi değildir. | `16`, `23`, `28` |
| FAILURE_REPORT | Yalnız gerçek local delivery failure sonrası ve bağımsız safe report field varsa taşınabilen isteğe bağlı control mesajı. | `16`, `18`, `23`, `28` |
| Security admission drop | Doğrulama/kapasite bütçesi nedeniyle sessizce bırakılan paket. Safety, field veya ACTIVE neighbor state'ini değiştirmez. | `27`…`29` |
| Conformance testi | Belirli bir `CT-*` oracle'ının deterministic çıktı ve/veya event-trace ile değerlendirilmesi. Test planının varlığı veya düşünce deneyi, PASS sonucu değildir. | `37` |
| Event-trace | Bir test run'ındaki yerel sıralı state/neden/sonuç kanıtı. Pcap yerine geçmez; node'lar arası duvar saati sıralaması iddia etmez. | `38` |
| Candidate-freeze | Proje sahibinin, açıkça listelenmiş design ve insan kapılarından sonra verdiği aday taslağı sabitleme kararı. Hazırlanmış checklist, freeze edilmiş standard değildir. | `39` |

## 7. Yasak kısa yollar

- ACTIVE olmayan peer, “acil durum”, PROTECT veya risk gerekçesiyle successor olamaz.
- Hop Limit/TTL, retry sayısı veya timer expiry loop-freedom kanıtı yerine kullanılamaz.
- Relay, OIID veya DFSN üretemez ya da artırmaz.
- ADS, DFSN; R1 Message Sequence, Request-ID; authenticated peer, forwarding-grade peer ile eş anlamlı değildir.
- Invalid/malformed/bad-signature paket, tek başına ACTIVE neighbor'ı EXPIRED yapamaz.
- `DESIGN-ONLY`, deployment-ready veya performansla doğrulanmış anlamına gelmez.
- Test planı, trace şablonu veya checklist'in yazılı olması, herhangi bir `CT-*` vakasının PASS olduğu veya candidate'ın frozen olduğu anlamına gelmez.

## 8. Sözlük bakım kuralı

Yeni wire alanı, state, timer, güvenlik profili veya farklı profile eklenirse önce bu sözlükte tanımlanmalı; sonra `06`, `07`, `05` ve ilgili normatif belgeye izlenebilir referans eklenmelidir. Bu kural, ad değişikliğinin sessizce semantik değişikliğe dönüşmesini önler.
