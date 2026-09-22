# DESPARETE — Hata İşleme ve Gözlemlenebilirlik Sözleşmesi

**Sürüm:** 0.1 (onaylı hata/gözlemlenebilirlik semantiği; local management export profili henüz seçilmedi)  
**Durum:** FR-13, FR-14 ve NFR-05 için packet reddi, local failure, field/neighbor state değişimi ve kaynak tükenmesinin gözlemlenebilir semantiğini tanımlar. Yeni routing control mesajı eklemez.  
**Tarih:** 2026-09-21

## 1. Amaç ve temel ilke

DESPARETE hata işlendiğinde ağda otomatik bir “ERROR” paketi üretmez. Paket hatası, replay, signature reddi veya kapasite taşması için cevap üretmek saldırganın küçük bir paketten çoklu kontrol trafiği doğurmasına izin verebilir. Hata önce **yerel state etkisi** ve ardından **yerel gözlemlenebilir olay/counter** olarak tanımlanır.

`FAILURE_REPORT`, bu kuralın istisnası değil ayrı bir uygulama-seviyesi rapordur: yalnız gerçek local delivery-failure sonrası, bağımsız FORWARDABLE report field varsa gönderilebilir. Ters yol çıkarımı, başarısız data field üzerinde onarım veya packet-hatasına yanıt olarak rapor üretimi yoktur.

## 2. Local event kaydı

Her gözlemlenebilir event, uygulama içi bir yönetim/telemetri arayüzüne aşağıdaki minimum kayıtla verilebilir:

| Alan | Semantik |
|---|---|
| `Event-ID` | Yerel node instance içinde monoton tanılayıcı sıra; routing seriali değildir. |
| `Local-Monotonic-Time` | Sıralama/latency hesabı için yalnız yerel saat. GPS veya global zaman değildir. |
| `Event-Class`, `Reason-Code`, `Severity` | §3teki standart sınıflandırma. |
| `Node-ID`, `Node-Instance-ID` | Olayı üreten yerel node örneği. |
| `Destination-ID`, `OIID`, `DFSN` | İlgiliyse field bağlamı; bilinmiyorsa boş/zero olarak açık işaretlenir. |
| `Neighbor-ID`, `Neighbor-Instance-ID` | İlgili authenticated peer; doğrulanmamış paketten türetilmiş kimlik kesin fact olarak kaydedilmez. |
| `Data-ID` veya `Request-ID` | İlgiliyse correlation; payload veya private key içermez. |
| `Counter-Delta` / `Snapshot` | Rate-limited aggregation için artış veya sayısal anlık değer. |

Event export, DESPARETE wire mesajı değildir. Saklama, şifreleme, erişim kontrolü, dışarı aktarım biçimi ve merkezi toplayıcı bu protokolün kapsamı dışındadır; sensitive topology/identity bilgisinin export edilmesi ayrı yönetim güvenliği gerektirir.

## 3. Event sınıfları ve zorunlu olaylar

| Sınıf | Zorunlu olay | Minimum reason / veri |
|---|---|---|
| `NEIGHBOR` | ACTIVE, STALE, SUSPECT, EXPIRED geçişi | Transition cause: matching probe, ACK, freshness expiry, authenticated link failure. |
| `FIELD` | FORWARDABLE, REPAIRING, UNREACHABLE geçişi; successor/alternate değişimi | Trigger, `K`, old/new successor, potential/FD bağlamı. |
| `ACQUISITION` | SOLICITING/REQUESTING başlatma, wave retry, session sonu | Reason, attempt/wave count, local result. |
| `POLICY` | STEADY/CAUTION/PROTECT geçişi veya protection kapanışı | Evidence category; ham risk/jamming hükmü değil. |
| `METRIC` | M0.1 epoch, Q/H/U/R band değişimi, maliyet doygunluğu veya profile preflight reddi | MetricProfile-ID, yerel reason ve band; ham RF örneği veya jamming hükmü değil. |
| `DATA` | buffer hold, forward, duplicate drop, local delivery-failure | Data-ID, traffic class, local reason, buffer/replication sonucu. |
| `SECURITY` | Format, roster, signature, origin/source proof veya R1 replay reddi | Paket türü + anonimleştirilebilir reason; raw imza/payload değil. |
| `RESOURCE` | Verification queue, cache, repair buffer, replica veya control budget reddi | Hangi bounded source, kullanım/sınır snapshot'ı. |
| `CONTROL` | FIELD_UPDATE/withdrawal planı, DFSN_REQUEST forward/dedup/Hop Limit sonu | `K`/Request-ID, local action; mesaj payload kopyası değil. |

`SECURITY` ve yüksek hızlı `DATA` eventleri paket başına zorunlu export değildir. Node, her reason için counter tutar ve yönetim exportunu rate-limit/coalesce eder. Bu sayede saldırgan geçersiz paket akışıyla log/bant genişliği tüketemez.

## 4. Hata karar matrisi

| Girdi / olay | Packet/state işlemi | Zorunlu yerel kayıt | Ağ mesajı |
|---|---|---|---|
| Unsupported version/type, malformed length/TLV/reserved | Drop; hiçbir neighbor/field/buffer state'i değişmez | `SECURITY` veya `CONTROL` format-reject counter | Yok |
| Eksik/yanlış AUTH, roster/Key-ID uyuşmazlığı, invalid Hop/Origin/Source signature | Drop; mevcut ACTIVE komşu tek paketle düşmez | `SECURITY auth-reject` counter | Yok |
| R1 old/equal/ambiguous control sequence | Drop; AR high-water geri sarmaz | `SECURITY replay-reject` counter | Yok |
| ADS/DFSN stale veya ambiguity | Stale ise drop; ambiguity ise field fail-closed ve bounded repair/acquisition | `FIELD freshness-reject/ambiguity` | Yalnız normal bounded control akışı |
| Duplicate Request-ID / control / Data-ID | İdempotent drop; yeni forward/buffer/replica yok | `CONTROL`/`DATA duplicate` counter | Yok |
| Hop Limit 0 veya one-hop constraint ihlali | Drop | `CONTROL hop-limit-reject` counter | Yok |
| Neighbor freshness/link failure | Candidate'i kaldır; state machine ve repair işle | `NEIGHBOR` + varsa `FIELD` transition | Yalnız scheduled probe/withdrawal/request |
| Field candidate yok / repair timeout | REPAIRING → UNREACHABLE; local delivery-failure | `FIELD unreachable`, `DATA delivery-failure` | Koşullu FAILURE_REPORT |
| DATA buffer quota/lifetime | DATA drop + local delivery-failure; duplicate state korunur | `RESOURCE buffer-reject`, `DATA delivery-failure` | Koşullu FAILURE_REPORT |
| Verification/cache/replica/control budget dolu | Yeni işi drop; mevcut safe state'i değiştirme | `RESOURCE admission-reject` counter | Yok |
| Optional FAILURE_REPORT alanı yok | Rapor üretilmez; local failure event kalır | `DATA report-suppressed` | Yok |

Bu matris, malformed/auth reddinin neighbor state'ini düşürmemesi ile doğrulanmış local link failure'ın state transition başlatması arasındaki ayrımı zorunlu kılar.

## 5. Failure reason kodları

`LocalDeliveryFailure` ve isteğe bağlı `FAILURE_REPORT` için mevcut wire Reason değerleri korunur:

| Kod | Anlam | Global iddia değildir |
|---:|---|---|
| 0 | Buffer lifetime | Target veya ağ partition hükmü değildir. |
| 1 | Buffer quota | Uygulama/yerel kaynak reddi. |
| 2 | Field unreachable | Yalnız local field erişilemezliği. |
| 3 | Freshness invalid | Stale/ambiguous context. |
| 4 | Local link failure | Fiziksel jammer veya global kopuş hükmü değildir. |

Security, resource ve policy olayları FAILURE_REPORT reason alanına zorla sıkıştırılmaz. Bunlar yalnız yerel telemetry sınıfında kalır; başka field üzerinde güvenli report yolunun varlığı dahi bu olaylardan otomatik ağ mesajı üretmez.

## 6. Counter ve snapshot sözleşmesi

Node, en az aşağıdaki monotonic sayaçları tutmalıdır. Counter overflow için implementation belirli unsigned wrap veya saturating davranışını ve exportta bu davranışı görünür kılmalıdır.

```text
rx_drop_format
rx_drop_auth
rx_drop_replay
rx_drop_freshness
rx_drop_duplicate
rx_drop_hop_limit
security_verify_admission_drop
field_repair_started
field_unreachable
dfsn_request_sent
dfsn_request_deduped
metric_epoch_processed
metric_insufficient_sample
metric_hazard_raised
metric_uncertainty_band_changed
metric_cost_band_changed
metric_cost_saturated
metric_preflight_reject
data_buffered
data_buffer_drop
data_local_delivery_failure
failure_report_sent
failure_report_suppressed
replica_secondary_sent
```

Yüksek sıklıklı counterlar her pakette event export etmek yerine per-reason delta snapshot olarak aktarılabilir. Export timerı/formatı burada atanmaz; bir yönetim profile bu export yükünün `27`deki `V_i`, queue ve radio bütçelerine müdahale etmediğini göstermelidir.

## 7. Güvenlik ve veri minimizasyonu

- Geçersiz paketin claimed Sender-ID'si, imza doğrulanmadan güvenilir komşu kimliği olarak evente yazılmaz.
- Raw packet, payload, private key, shared secret, tam signature veya roster public key materyali routing evente zorunlu alan değildir.
- R1 replay eventinde yalnız authenticated sender/instance ve reason kaydedilebilir; raw eski packet yeniden export edilmez.
- `DIAGNOSTIC` TLV, local telemetry yerine geçmez ve routing/policy kararını doğrudan değiştiremez.
- Telemetry export kanalının bütünlüğü/gizliliği, DESPARETE routing AUTH TLV'si tarafından korunmaz.

## 8. Doğrulama yükümlülükleri

| Senaryo | Beklenen gözlem |
|---|---|
| 10.000 malformed veya bad-signature paket | Hata yanıtı çıkmaz; yalnız coalesced counter; neighbor/field state değişmez. |
| Replay edilmiş authenticated FIELD_UPDATE | `rx_drop_replay` artar; AR/ADS/field geri sarmaz. |
| Origin proof yok FIELD_UPDATE | `rx_drop_auth` artar; yeni OIID/DFSN kabul edilmez. |
| ACTIVE neighbor timeout | `NEIGHBOR` transition, candidate removal, ilgili repair/withdrawal olayları doğru sırada görünür. |
| Buffer quota dolması | `RESOURCE` ve `DATA` local failure görünür; extra repair/redundancy doğmaz. |
| FAILURE_REPORT alanı yok | Local delivery failure görünür; network report sayacı artmaz. |
| PROTECT alternate kaybı | Replication kapanışı görünür; eski PROTECT action restore edilmez. |

## 9. Açık yönetim profili soruları

Bu taslak, routing semantiğini gözlemlenebilir yapar; aşağıdakileri seçmez:

- event export protokolü/taşıyıcısı, log retention ve merkezi toplayıcı;
- severity eşikleri, export frekansı, counter bit genişliği ve overflow politikası;
- topology/identity telemetry'sinin hangi operatör veya sistemle paylaşılacağı;
- platformun verification/admission limitlerinin hangi event eşiğinde alarm üreteceği.

Bu seçimler, routing safety algoritmasını değiştirmediği sürece deployment/management profile kararıdır. Yeni ağ-geneli hata mesajı, reputation feedback'i veya telemetry'nin routing kararını etkilemesi MAJOR mimari değişiklik olur.
