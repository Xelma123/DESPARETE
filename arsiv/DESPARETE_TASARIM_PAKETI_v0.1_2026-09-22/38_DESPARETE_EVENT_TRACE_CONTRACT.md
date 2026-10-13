# DESPARETE v0.1 — Event-Trace Sözleşmesi

**Sürüm:** v0.1 trace-sözleşmesi  
**Durum:** Uygulama doğrulaması için beklenen kanıt biçimidir; örnek izler çalışma sonucu değildir.  
**Tarih:** 2026-09-21

## 1. Amaç

Bu sözleşme, `37`deki conformance vakalarının uygulama çalışırken nasıl kanıtlanacağını tanımlar. Trace, paket pcap'i yerine geçmez; güvenli bir biçimde state, neden ve sıralama bilgisini verir. Her implementasyon JSON, CBOR, satır tabanlı log veya başka bir taşıyıcı kullanabilir; aşağıdaki alanların semantiğini korumak zorundadır.

Trace yalnız local monotonic time kullanır. Farklı node trace'leri duvar saatiyle kesin sıralıymış gibi birleştirilmez; correlation ID ve paket/field kimlikleri kullanılır.

## 2. Run header

Her trace run'ı, ilk eventten önce aşağıdaki header'ı taşır:

| Alan | Zorunluluk | Açıklama |
|---|---|---|
| `run_id` | MUST | Benzersiz test/run kimliği. |
| `test_ids` | MUST | Kanıtlanması hedeflenen bir veya daha çok `CT-*` kimliği. |
| `implementation_id` | MUST | Build/revision/konfigürasyon kimliği. |
| `protocol_version` | MUST | `1`. |
| `metric_profile_id` | MUST | `M0.1`. |
| `fixture_id` | MUST | Node/topoloji fixture kimliği; gerçek gizli anahtar içermez. |
| `node_id`, `node_instance_id` | MUST | Trace'i üreten local node bağlamı. |
| `timer_profile_id` | MUST | Dengeli v0.1 başlangıç profili veya açık eşdeğeri. |
| `start_local_monotonic_time` | MUST | Yalnız aynı node içi sıralama için başlangıç. |
| `dc11_capability` | MUST | `available`, `unavailable` veya `not-applicable`; link success/failure/retry arayüzü durumu. |

`metric_profile_id != M0.1` olan run, v0.1 M0.1 conformance PASS kanıtı değildir. DC-11 `unavailable` ise metrik/policy runtime vakaları `BLOCKED` olarak işaretlenir.

## 3. Ortak event biçimi

Her event aşağıdaki mantıksal biçime sahiptir:

```text
event = {
  trace_seq, local_monotonic_time, event_class, event_name,
  reason, node_context, optional field_context,
  optional neighbor_context, optional packet_context,
  optional metric_snapshot, optional state_before_after,
  optional counter_delta, correlation_id
}
```

| Alan | Kural |
|---|---|
| `trace_seq` | Node instance içinde kesin artan tamsayıdır. |
| `local_monotonic_time` | Aynı node trace'inde geri gidemez. |
| `event_class` | `NEIGHBOR`, `FIELD`, `ACQUISITION`, `POLICY`, `METRIC`, `DATA`, `SECURITY`, `RESOURCE` veya `CONTROL`. |
| `event_name` | §4teki normalize adlardan biri veya eşdeğer uygulama adı. |
| `reason` | İnsan okunur ancak sınırlı reason kodu; jamming veya saldırgan kimliği hükmü olamaz. |
| `field_context` | İlgiliyse `Destination-ID`, `OIID`, `DFSN`, ADS/potential/FD özetini içerir. |
| `neighbor_context` | Yalnız authenticated veya direct-peer bağlamında güvenilir kimlik; otherwise `untrusted` işareti. |
| `packet_context` | Type, Header Length, Hop Limit, Data-ID/Request-ID ve RB gibi gerekli metadata; payload/raw imza yok. |
| `metric_snapshot` | İlgiliyse `Q,H,U,R,C`, band ve `MetricProfile-ID`; ham RF örnek dizisi zorunlu değildir. |
| `state_before_after` | Etkilenen neighbor/field/policy state'in önce/sonra değeri. |
| `counter_delta` | Coalesced veya tekil sayaç artışı. |
| `correlation_id` | Aynı request, Data-ID, packet veya test eylemine bağlı eventleri iliştirir. |

## 4. Normalize event adları

| Sınıf | Event adları |
|---|---|
| `SECURITY` | `PACKET_DROPPED_FORMAT`, `PACKET_DROPPED_AUTH`, `PACKET_DROPPED_REPLAY`, `PACKET_DROPPED_HOP_LIMIT`, `R1_INITIALIZED` |
| `NEIGHBOR` | `CANDIDATE_UNQUALIFIED`, `QUALIFICATION_PROBE_SCHEDULED`, `PROBE_REPLY_SENT`, `NEIGHBOR_ACTIVE`, `NEIGHBOR_STALE`, `NEIGHBOR_SUSPECT`, `NEIGHBOR_EXPIRED` |
| `METRIC` | `METRIC_EPOCH`, `METRIC_BAND_CHANGED`, `METRIC_COST_SATURATED`, `METRIC_PREFLIGHT_REJECTED` |
| `FIELD` | `ADVERTISEMENT_ACCEPTED`, `ADVERTISEMENT_REJECTED`, `ADVERTISEMENT_DIAGNOSTIC_ONLY`, `FIELD_FORWARDABLE`, `SUCCESSOR_CHANGED`, `WITHDRAWAL_PLANNED`, `FIELD_REPAIRING`, `FIELD_UNREACHABLE`, `FIELD_RETIRED` |
| `ACQUISITION` | `SOLICIT_SENT`, `REQUEST_SENT`, `REQUEST_DEDUPED`, `REPAIR_TIMEOUT` |
| `POLICY` | `POLICY_CAUTION`, `POLICY_PROTECT`, `POLICY_RECOVERY`, `PROTECTION_DISABLED` |
| `DATA` | `DATA_FORWARDED`, `DATA_HELD`, `DATA_DROPPED_DUPLICATE`, `LOCAL_DELIVERY_FAILURE`, `FAILURE_REPORT_SUPPRESSED` |
| `RESOURCE` | `ADMISSION_REJECTED`, `BUFFER_REJECTED`, `REPLICA_REJECTED` |
| `CONTROL` | `FIELD_UPDATE_PLANNED`, `WITHDRAWAL_SENT`, `DFSN_REQUEST_FORWARDED`, `CONTROL_DEDUPED` |

Bir implementasyon farklı adı kullanırsa, `37`deki CT kimlikleriyle bu tabloya eşleme vermelidir.

## 5. Sıralama ve negatif kanıt kuralları

Trace yalnız olayların görüldüğünü değil, görülmemesi gereken olayları da kanıtlamalıdır:

1. `PACKET_DROPPED_*` sonrası aynı `correlation_id` için `NEIGHBOR_ACTIVE`, `FIELD_FORWARDABLE`, `SUCCESSOR_CHANGED`, `DATA_FORWARDED` veya `REQUEST_SENT` oluşmamalıdır.
2. `CANDIDATE_UNQUALIFIED` veya `PROBE_REPLY_SENT`, tek başına `NEIGHBOR_ACTIVE` ile sonuçlanamaz. ACTIVE için matching outbound proof event'i olmalıdır.
3. `FIELD_REPAIRING` öncesinde ilgili successor kaldırma veya candidate-yokluğu görünmelidir; `WITHDRAWAL_PLANNED`/acquisition ardından gelir.
4. `POLICY_PROTECT`ten önce sürekli M0.1 ProtectEvidence, alternate ve traffic eligibility kanıtı bulunmalıdır.
5. `DATA_FORWARDED` with secondary için aynı Data-ID, iki farklı immediate next hop, iki outputta `RB=0` ve en çok iki output görünmelidir.
6. `FIELD_UNREACHABLE` sonrası yeni DATA, explicit Acquire veya valid field update olmadan `REQUEST_SENT` üretmemelidir.

Bu negatif kurallar, “trace'te hata görünmedi” yorumuna dayanmaz. İlgili correlation/window için olay sorgusu yapılır ve sonuç test raporuna `absent-as-required` olarak yazılır.

## 6. Zorunlu trace şablonları

### 6.1 Geçersiz authentication — CT-SEC-01

```text
PACKET_DROPPED_AUTH(reason=invalid_hop_signature)
counter_delta(rx_drop_auth=+1)
assert no NEIGHBOR/FIELD/DATA/ACQUISITION state event for this correlation_id
```

### 6.2 Incoming PROBE ile nitelendirme — CT-NEI-02/03

```text
CANDIDATE_UNQUALIFIED(peer=j)
R1_INITIALIZED(peer=j, cause=targeted_initial_probe)
PROBE_REPLY_SENT(peer=j)
QUALIFICATION_PROBE_SCHEDULED(peer=j)
... matching outbound proof ...
NEIGHBOR_ACTIVE(peer=j, cause=matching_probe_reply_or_confirmed_ack)
```

Incoming PROBE'dan sonra matching outbound proof yoksa son event `NEIGHBOR_ACTIVE` olamaz. `R1_INITIALIZED`, yalnız control anti-replay başlangıcıdır; forwarding-grade kanıt değildir.

### 6.3 Alternatifsiz repair — CT-REP-02/03

```text
NEIGHBOR_SUSPECT or candidate invalidation
SUCCESSOR_CHANGED(old=j, new=none)
FIELD_REPAIRING(P=infinity)
WITHDRAWAL_PLANNED
REQUEST_SENT or SOLICIT_SENT
... no valid successor before deadline ...
REPAIR_TIMEOUT
FIELD_UNREACHABLE
```

Bu pencere içinde `DATA_FORWARDED(next_hop=old_j)` veya stale/unsafe next hop yasaktır.

### 6.4 PROTECT ve RB=1 — CT-POL-03 / CT-DATA-02

```text
METRIC_BAND_CHANGED(H>=128)
POLICY_PROTECT(evidence_duration>=2.5s, alternate=true, traffic_eligible=true)
DATA_FORWARDED(data_id=x, next_hop=primary, rb=0)
DATA_FORWARDED(data_id=x, next_hop=alternate, rb=0)
assert exactly 2 immediate outputs and distinct next_hop values
```

### 6.5 M0.1 doygunluğu — CT-MET-01

```text
METRIC_EPOCH(q,h,u,r,c)
METRIC_COST_SATURATED(advertised_potential, c, result=infinity)
ADVERTISEMENT_REJECTED(reason=nonfinite_total_cost)
assert no successor installation from this candidate
```

### 6.6 OIID/DFSN ambiguity — CT-FLD-03/04

```text
ADVERTISEMENT_REJECTED(reason=serial_ambiguous)
FIELD_REPAIRING or bounded acquisition evaluation
assert no restoration of retired/ambiguous field
```

### 6.7 ACTIVE olmayan peer'dan OIID — CT-FLD-05

```text
ADVERTISEMENT_DIAGNOSTIC_ONLY(reason=neighbor_not_active, peer=j, oiid=new)
assert no FIELD_RETIRED, SUCCESSOR_CHANGED, FIELD_REPAIRING or REQUEST_SENT
```

Bu durum, geçerli target origin proof'unu reddetmek değildir; update forwarding/candidate bağlamına alınmadan yalnız tanısal olarak kaydedilir.

## 7. Güvenlik ve veri minimizasyonu

Trace MUST NOT içerir:

- payload veya raw DATA application içeriği;
- private key, shared secret, full public roster veya raw signature;
- imza doğrulanmadan gerçek kabul edilen remote identity iddiası;
- “jammer bulundu” veya “malicious relay” hükmü.

Data-ID/Node-ID operasyonel hassas bilgi sayılabilir. Dışa verilen trace bunları hash/pseudonym ile taşıyabilir; ancak aynı run içinde correlation korunmalıdır.

## 8. Test raporuna bağ

Her `37` testi, raporda en az şu bağları taşır:

```text
Test-ID → run_id → trace_seq aralığı → oracle sorgusu → PASS/FAIL/BLOCKED/NOT-RUN
```

Bu sözleşme telemetry export taşıyıcısı, merkezi toplama, retention veya alarm eşiği seçmez. Bunlar routing semantics'ini değiştirmediği sürece management/deployment profile kapsamındadır.
