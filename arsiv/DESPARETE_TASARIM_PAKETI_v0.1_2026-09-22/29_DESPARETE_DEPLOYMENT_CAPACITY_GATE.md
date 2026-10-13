# DESPARETE — Deployment Kapasite Kabul Kapısı

**Sürüm:** 0.1 (platform-bağımsız kabul sözleşmesi; sayısal cihaz profili seçilmedi)  
**Durum:** Security Profile 1 ve dengeli zamanlama profilinin belirli bir UAV/radyo platformuna alınabilmesi için zorunlu ölçüm ve konfigürasyon girdilerini tanımlar.  
**Tarih:** 2026-09-21

## 1. Amaç ve dürüst kapsam

Bu belge, DESPARETE'nin uçuşa veya belirli bir radyo taşıyıcısına hazır olduğunu iddia etmez. İlk sürüm, Security Profile 1 ile birlikte 118…210-octet control header ve 194-octet DATA header kullanır; bu nedenle taşıyıcı MTU, payload bütçesi, Ed25519 kapasitesi ve roster belleği deployment öncesi kanıtlanmalıdır.

Kapasite kapısı, routing semantics'ini değiştirmez. Başarısız olduğunda çözüm `T_*` değerlerini sessizce küçültmek, authentication'ı atlamak veya safety gate'ini açmak değildir. Platforma uygun yeni bir profile, açık karar ve karşılaştırmalı doğrulama gerekir.

## 2. Zorunlu deployment girdileri

| Kimlik | Girdi | Birim / tanım | Neden zorunlu |
|---|---|---|---|
| DC-01 | `MTU_link` | Taşıyıcının DESPARETE header + payload için gerçek tek-frame payload üst sınırı, octet | Fragmentation semantiği tanımlı değildir. |
| DC-02 | `P_data_max` | Uygulamanın en büyük DATA payload'u, octet | DATA frame sığması. |
| DC-03 | `n_roster`, `k_max` | Roster node sayısı ve node başına aktif key sayısı | TrustRoster RAM/flash hesabı. |
| DC-04 | `d_max`, `f_max` | Eşzamanlı retained neighbor ve field-context üst sınırı | Neighbor/field/AR state kapasitesi. |
| DC-05 | `b_total` | Yerel repair buffer toplam paket kapasitesi | `Q_buffer[field,class]` uygulanabilirliği. |
| DC-06 | `λ_ctrl,max`, `λ_data,max` | Kabul edilmesi beklenen en yüksek control/data ingress hızı | Cache ve verification admission. |
| DC-07 | `V_verify`, `V_sign` | Hedef platformda sürdürülebilir Ed25519 verify/sign hızı | Security Profile 1 CPU kapısı. |
| DC-08 | `A_radio` | MAC/PHY overhead, retry ve duty cycle dahil ölçülmüş kullanılabilir airtime | Header artışı ve control/data yükü. |
| DC-09 | `M_ram`, `M_flash` | DESPARETE için ayrılan çalışma/kalıcı bellek bütçesi | Roster, cache, buffer ve telemetry admission. |
| DC-10 | Taşıyıcı davranışı | Broadcast/unicast, link ACK/retry, paket kaybı ve payload MTU semantiği | PROBE kanıtı, `D_*` varsayımları ve airtime hesabı. |
| DC-11 | Link sonuç arayüzü | Her hedefli unicast için final success/failure, yeniden iletim sayısı `r` ve yerel monotonic sonuç zamanı | M0.1 `Q/H/U` hesapları ve policy eşikleri için zorunlu doğrudan kanıt. |

Bu girdiler platform üreticisinin teori değeri değil, seçilen firmware/radio configuration altında kaydedilmiş ölçüm veya doğrulanabilir konfigürasyon olmalıdır.

DC-11'de `r` bilgisi yoksa başarılı teslimi sadece başarı/başarısızlık olarak taklit etmek M0.1 uyumu değildir. Çözüm, uygun link katmanı telemetrisi sağlamak veya açıkça farklı bir metrik profile seçmektir; quality cezasını sessizce kaldırmak değildir.

## 3. Wire ve MTU kabul koşulları

Security Profile 1'de en büyük control header `FIELD_UPDATE = 210 octet`, DATA header `194 octet`tir. DESPARETE core, kendi fragmentation mekanizmasını tanımlamaz.

```text
MTU_link ≥ 210                              (DC-W01: tüm control türleri)
MTU_link ≥ 194 + P_data_max                 (DC-W02: uygulama DATA)
HeaderLength ≤ 255                          (DC-W03: zaten profile tarafından sağlanır)
```

Alt katman fragmentation kullanılıyorsa, onun reassembly, güvenlik, loss ve latency davranışı `D_control`, `D_data` ve signature coverage ile uyumluluğu kanıtlanmalıdır. Uyum kanıtı yoksa fragmentation varmış gibi varsayılmaz.

`MTU_link < 210` ise bu v0.1 Security Profile 1 doğrudan deploy edilemez. Çözüm; credentials veya imzaları kesmek değil, açıkça farklı bir taşıma/kapsülleme ya da yeniden tasarlanmış security profile seçmektir.

## 4. Kripto admission kabul koşulları

Alıcının en yüksek signature verification işi için muhafazakâr model:

```text
R_verify = 2 × (λ_DATA + λ_FIELD_UPDATE)
         + λ_FIELD_SOLICIT + λ_DFSN_REQUEST
         + λ_PROBE + λ_PROBE_REPLY + λ_FAILURE_REPORT

R_verify_admitted ≤ V_verify
```

DATA ve FIELD_UPDATE ikişer doğrulama, diğer v0.1 paketleri birer HopSignature doğrulaması gerektirir. `λ_*`, sadece format/roster kapısını geçen paketlerin kabul hedefidir; saldırganın sınırsız ingress'i bu denklemin normal çalışma varsayımı değildir.

Gönderici için:

```text
R_sign = R_hop_tx + R_source_data_created + R_origin_context_created
R_sign ≤ V_sign
```

Her on-air DESPARETE paketi için bir HopSignature; source oluşturduğu DATA için ek SourceSignature; target yeni `(OIID,DFSN)` context'i için ek OriginSignature üretir. Broadcast control tek on-air gönderim olsa da her retransmission yeni transmit/signature budget'ına sayılır.

Kabul kanıtı, en az aşağıdakileri içerir:

1. üretim benzeri compiler, crypto library ve power mode ile `V_verify`/`V_sign` ölçümü;
2. DC-06'daki ingress yükü altında p95/p99 processing latency, queue occupancy ve `security_verify_admission_drop` sayacı;
3. budget aşımında sessiz drop'un FD/successor/neighbor state'ini değiştirmediğine dair event trace.

## 5. Bellek ve cache kabul koşulları

Trust rosterın wire-anlamsal minimum kaydı node başına en az şu ham veriyi taşır:

```text
Node-ID (8) + Key-ID (8) + Ed25519 public key (32) = 48 octet/key
M_roster_raw ≥ 48 × n_roster × k_max octet
```

İndeks, key state, alignment, lookup table ve revocation/management metadata bu alt sınırın dışındadır; gerçek `M_roster` platformda ölçülmelidir.

Cache/buffer konfigürasyonu en az şunları karşılamalıdır:

```text
C_ctrl       ≥ ceil(λ_ctrl,max × T_ctrl_duplicate)
C_request    ≥ ceil(λ_request,max × T_req_duplicate)
C_data       ≥ ceil(λ_data,max × T_data_duplicate)
Q_buffer[field,class] ≤ min(0.10 × b_total, 32)
```

`λ_request,max`, accepted DFSN_REQUEST ingress hızıdır ve normal control trafficten ayrı ölçülmelidir. Bu denklemler entry sayısı alt sınırıdır; key/ID/timestamp/state alanlarının gerçek byte maliyeti implementasyondan çıkarılır. `C_*` dolduğunda yeni entry allocation yerine güvenli admission reject uygulanır ve `28`deki RESOURCE sayaçları artar.

## 6. Airtime ve zamanlama kabul koşulları

Her paket türü için platformun aşağıdaki ölçümü vermesi gerekir:

```text
airtime(type, header_length, payload_length, MAC retry regime)
```

Bu ölçüm, PHY bitrate tek başına değildir; MAC header/ack/backoff/retry, broadcast davranışı ve kapsülleme etkisini içermelidir. Onaylı routing üretim üst sınırları (`21`, `27`) ile birlikte aşağıdaki bağ kurulmalıdır:

```text
A_control + A_data + A_management ≤ A_radio
```

`A_management`, telemetry export varsa onun ayrı bütçesidir; routing AUTH TLV'siyle görünmez sayılmaz. `D_control=100 ms` ve `D_data=250 ms` ancak bu toplam, hedef topoloji/traffic yükünde kabul edilebilir p95/p99 link gecikmesiyle desteklenirse deployment profile korunabilir. Desteklenmiyorsa “dengeli” timer sayıları performans gerçekliği değil başlangıç varsayımı olarak kalır.

## 7. Topoloji, field ve failure load kabul koşulları

| Kontrol | Kabul kanıtı |
|---|---|
| `d_max`, `f_max` state kapasitesi | Bu sınırda field recompute, AR/advertisement cache ve buffer admission memory taşması olmadan çalışır. |
| DFSN_REQUEST worst case | En az `H_req=16` kapsam ve ilgili `Δ` altında Request-ID dedup, Hop Limit ve `N_req=2/4 s` korunur. |
| Neighbor failure burst | `d_max` komşuda eşzamanlı expiry/probe eventleri `T_probe_session`, `T_retention` ve control budget içinde sonlanır. |
| Protected DATA | RB=1 olayında yalnız iki immediate output, bu kopyalarda RB=0 ve source/hop signature kuralları ölçülür. |
| R1 replay | `d_max` authenticated peer state'i retention süresi boyunca high-water geri sarılmadan tutulur. |
| M0.1 link metriği | DC-11 sonuçlarıyla M0-TV-01…M0-TV-05 aynı Q/H/U/R/C değerini üretir; 0.5 s epoch altında candidate recompute/control rate sınırları korunur. |

Bir test bu koşulu yalnız lab topolojisinde gösteriyorsa, farklı görev yoğunluğu/airtime için genellenemez. Bu belge simülasyon istemez; seçilen hardware/configuration üstünde deterministik yük veya uçuş-öncesi bench test yeterli kanıt türüdür.

## 8. Deployment karar seçenekleri

| Seçenek | Karar | Kazanç | Bedel |
|---|---|---|---|
| A — Kapı-önce **(önerilen)** | DC-01…DC-11 ölçülür; ancak kapılar geçerse Profile 1 + M0.1 deployment etiketi verilir. | Güvenlik/timer/metrik varsayımları cihaz gerçeğine bağlanır. | Ölçüm ve test emeği gerekir. |
| B — Platformdan bağımsız “uygundur” ilanı | Değerler olmadan v0.1'i deploy-ready say. | Hızlı görünür sonuç. | MTU, CPU veya airtime uyumsuzluğunu gizler; kabul edilmez. |
| C — Düşük kapasiteli cihaz için farklı profil | Yeni transport/security/timer profile tasarla ve karşılaştırmalı doğrula. | Kısıtlı cihazlara uyum olasılığı. | Yeni MAJOR kararlar, correctness/security yeniden kontrolü. |

Bu v0.1 için önerilen karar A'dır. Bu, bir cihaz veya rakam seçmez; yalnız deployment kelimesini hangi kanıtın hak ettiğini tanımlar.

## 9. Kapı sonucu ve olay kaydı

| Sonuç | Etiket | Zorunlu davranış |
|---|---|---|
| Tüm DC ve DC-W kontrolleri geçer | `DEPLOYMENT-CAPACITY-ACCEPTED` | Ölçüm artefaktları, config hash'i ve platform sürümü ile kaydedilir. |
| Bir ölçüm henüz yok | `DESIGN-ONLY` | Protokol semantics'i geçerli kalır; uçuş/SWaP/throughput iddiası yapılmaz. |
| MTU/CPU/RAM/airtime kapısı başarısız | `PROFILE-INCOMPATIBLE` | V0.1 safety/security kapıları değiştirilmez; A veya C yoluyla yeniden ele alınır. |

## 10. Proje sahibinden gerekli bilgiler

Bir sayısal deployment profile oluşturmak için aşağıdaki kısa bilgi seti yeterlidir:

1. hedef uçuş bilgisayarı/işletim sistemi ve Ed25519 kütüphanesi;
2. radyo/MAC taşıyıcısı, gerçek payload MTU, link retry/ACK davranışı ve M0.1 için per-unicast success/failure/`r` sonucu;
3. maksimum UAV rosterı, beklenen eşzamanlı komşu sayısı ve tek-sink dışına çıkılıp çıkılmayacağı;
4. DATA payload üst sınırı ve en yüksek uygulama data hızı;
5. ayrılabilecek RAM/flash, hedef duty cycle/airtime ve telemetry export beklentisi.

Bu bilgi yoksa, seçenek A yine kabul edilebilir kapı olarak kalır fakat `DESIGN-ONLY` statüsü değişmez.
