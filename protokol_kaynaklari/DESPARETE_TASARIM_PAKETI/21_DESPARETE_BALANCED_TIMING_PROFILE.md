# DESPARETE — Dengeli Zamanlama Profili

**Sürüm:** 0.1 (ilk sürüm başlangıç profili; performans doğrulaması değildir)  
**Durum:** Proje sahibinin onayladığı dengeli operasyonel tempo için `20`deki timer mimarisini somutlaştırır.  
**Tarih:** 2026-09-20

## 1. Amaç ve dürüst kapsam

Bu belge, ilk uygulanabilir DESPARETE profili için sayı seçer. Bu sayılar simülasyon, uçuş testi veya ölçülmüş optimum sonucu değildir. Aşağıdaki açık çalışma varsayımlarını karşılayan, birbiriyle tutarlı **başlangıç değerleri**dir:

- Tek-atlama kontrol iletimi için profile kabul edilen sıra/gecikme bütçesi `D_control = 100 ms`; kontrol jitter üst sınırı `J_control = 100 ms`dir.
- Aktif görev alanındaki tipik data hop sınırı `H_data = 16`; kontrollü DFSN_REQUEST yayılımı da `H_req = 16` atlamadır.
- Data'nın bir atlamada kuyruklama ve iletim için profile kabul edilen üst bütçesi `D_data = 250 ms`dir.
- Kısa süreli repair, normal trafik için kabul edilebilir; protokol DTN deposu veya exactly-once teslim sağlamaz.
- Birimler, aksi belirtilmedikçe saniyedir; `FIELD_UPDATE.Lifetime` wire alanında 100 ms kuanta ile kodlanır.

Bu varsayımlar sağlanmıyorsa profilin tamamı değil, yalnız ölçülen parametreleri revize edilmelidir; TR-01…TR-12 ilişkileri korunur. Timer değerleri, RFC 8966'nın timerlar arası ayrım ve fazla kısa periyotların kontrol yükü yaratabileceği ilkesiyle tutarlıdır, fakat onun varsayılan değerlerinden türetilmiş değildir. [RFC 8966](https://www.rfc-editor.org/rfc/rfc8966.html)

## 2. Baz parametre seti

### 2.1 Komşu doğrulama

| Parametre | Değer | İşlem |
|---|---:|---|
| `T_fresh` | 3.0 s | Son forwarding-grade iki-yönlü kanıttan sonra ACTIVE tutulma süresi. |
| `T_idle_probe` | 2.0 s | ACTIVE komşu bu süre boyunca iki-yönlü kanıt üretmezse normal liveness PROBE tetikler. |
| `T_probe_reply` | 0.5 s | Qualification veya failure-bound bir PROBE için eşleşen PROBE_REPLY bekleme süresi. |
| `J_probe` | 0.1 s | Probe scheduling jitter üst sınırı. |
| `D_probe` | 0.1 s | Tek-atlama probe/reply işleme-iletim bütçesi. |
| `T_probe_start` | 0.1 s | Niteliksiz direct-peer qualification veya STALE/SUSPECT doğrulama oturumu başlatma üst gecikmesi. |
| `N_probe` | 2 | Failure-bound probe oturumundaki en çok deneme. |
| Denemeler arası süre | 0.2 s | İlk başarısız probe sonrası ikinci denemeden önceki asgari bekleme. |
| `T_probe_session` | 1.3 s | `0.1 + 0.5 + 0.2 + 0.5` muhafazakâr operasyon bütçesi. |
| `T_retention` | 5.0 s | Niteliksiz direct-peer kaydı açıldığında veya son forwarding-grade kanıttan sonra komşu/AR kaydını saklama üst süresi. |

Kontrol: `T_idle_probe + T_probe_reply + J_probe + D_probe = 2.7 s < T_fresh = 3.0 s`; `T_fresh + T_probe_session = 4.3 s < T_retention = 5.0 s`.

Normal idle probe, `N_probe` tüketmez. Idle PROBE başarısız olur ve `T_fresh` dolarsa node ACTIVE → STALE geçer, ardından ayrı failure-bound oturum en çok iki deneme yapar. Doğrudan unicast/ACK kanıtı veya eşleşen PROBE_REPLY, tüm komşu tazelik zamanlarını yeniden başlatır.

### 2.2 FIELD_UPDATE ve alan-ilanı

| Parametre | Değer | İşlem |
|---|---:|---|
| `T_adv_refresh` | 1.0 s | FORWARDABLE alanın normal FIELD_UPDATE tazeleme aralığı. |
| `J_adv` | en çok 0.2 s | Normal update'e uygulanan rastlantısal jitter. |
| `D_adv` | 0.2 s | Tek-atlama update işleme/iletim bütçesi. |
| `Lifetime` / `L_adv_sent` | 3.0 s = 30 wire kuantası | Gönderilen REACHABLE FIELD_UPDATE lifetime değeri. |
| `L_adv_max` | 3.0 s | Alıcının kabul ettiği azami field-ilanı ömrü. |
| `G_adv_refresh` | 1.5 s | Seçili ilan expire olmadan FIELD_SOLICIT için ayrılan guard. |
| `T_coalesce` | 0.2 s | Aynı `K`de olağan triggered update birleştirme penceresi. |
| `T_urgent` | 0.1 s | Successor değişimi, potential artışı veya withdrawal için en geç ilan gecikmesi. |
| `T_adv_cache` | 4.0 s | Expire olmuş finite ilan metadatasını yalnız ordering/diagnostic için saklama süresi. |
| `T_withdraw_cache` | 4.0 s | Withdrawal ADS/state bilgisini saklama süresi. |
| `D_reorder` | 0.5 s | Tek-atlama eski/yeniden sıralanmış kontrol mesajı varsayım bütçesi. |

Kontrol: `1.0 + 0.2 + 0.2 = 1.4 s < 3.0 s`; iki solicit için `0.4 + 0.2 + 0.4 + 0.1 + 0.1 = 1.2 s < 1.5 s`; `3.0 + 0.5 = 3.5 s < 4.0 s`; `T_urgent <= T_coalesce`.

Alıcı her valid REACHABLE FIELD_UPDATE için `L_adv_effective = min(received Lifetime, 3.0 s)` uygular. `advertisement_expiry - 1.5 s` anında geçerli yeni update yoksa ve aynı `K`de pending solicit bulunmuyorsa solicit süreci başlar. Yeni update gelirse solicit iptal edilir. Withdrawal alımı, daha eski queued finite update'i ADS ile bastırır ve `T_withdraw_cache` boyunca routing candidate oluşturmaz.

### 2.3 FIELD_SOLICIT, DFSN_REQUEST ve repair

| Parametre | Değer | İşlem |
|---|---:|---|
| `T_solicit_reply` | 0.4 s | Bir FIELD_SOLICIT'e FIELD_UPDATE yanıtı için bekleme. |
| `T_solicit_backoff` | 0.2 s | Tekrarlanan solicit öncesi asgari bekleme. |
| `N_solicit` | 2 | Aynı local acquisition/refresh işlemi için en çok solicit denemesi. |
| `H_req` | 16 | DFSN_REQUEST'in başlangıç Hop Limit değeri; desteklenen data çapı içindeki feasibility-starvation isteğinin sinke erişebilmesi için `H_data` ile eşittir. |
| `T_req_session` | 4.0 s | Coalesced DFSN request işleminin toplam yerel ömrü. |
| `T_req_retry` | 1.0 s | Yeni Request-ID ile ikinci request dalgasından önceki asgari süre. |
| `N_req` | 2 | Bir repair/acquisition işlemi için en çok request dalgası. |
| `T_req_duplicate` | 4.0 s | Request-ID duplicate cache süresi. |
| `T_repair_max` | 6.0 s | REPAIRING durumunun zaman üst sınırı. |

İki solicit denemesi en çok `0.4 + 0.2 + 0.4 = 1.0 s` sürer. Ardından gerekiyorsa iki DFSN request dalgası, yeni Request-ID kullanarak, 4.0 saniyelik tek coalesced oturumda yürütülür. İlk request dalgası, aynı `K` için başka local request varsa onunla birleştirilir. `T_repair_max = 6.0 s`, solicit + request işlem zinciri için sınır bırakır.

DFSN_REQUEST'in wire lifetime alanı yoktur. Bu, proje sahibinin seçtiği B semantiğidir: Hop Limit yalnız yayılımın mekânsal kapsamını; `T_req_session` ve `T_req_duplicate` ise her node'daki zamansal kapsamı sınırlar. Aynı Request-ID ikinci kez iletilmez; gerçek retry yeni Request-ID ile yapılır.

### 2.4 Buffer ve duplicate saklama

| Parametre | Değer | İşlem |
|---|---:|---|
| `T_buffer[Traffic-Class 0]` | 6.0 s | Normal trafikte REPAIRING sırasında en uzun bekleme. |
| `Q_buffer[field, class]` | Yerel repair buffer'ın en çok %10'u ve en çok 32 paket | Alan başına adil kullanım sınırı; daha küçük değer uygulanır. |
| `H_data` | 16 | DATA başlangıç Hop Limit profili. |
| `D_data` | 0.25 s | Bir data atlaması için kuyruk/iletim bütçesi. |
| `T_data_duplicate` | 10.0 s | Data-ID duplicate cache saklama süresi. |
| `T_ctrl_duplicate` | 4.0 s | Normal control Message-ID duplicate cache süresi. |
| `T_retired_oiid` | 60.0 s | Eski target instance state saklama süresi. |

Kontrol: `T_buffer + H_data × D_data = 6.0 + 16 × 0.25 = 10.0 s = T_data_duplicate`.

Traffic Class `1…255` için buffer ömrü ve quota bu profil tarafından henüz atanmaz. Bunlar uygulama/QoS sözleşmesi ve security/complexity fazları tamamlandığında, TR-10'u bozmadan eklenebilir. Bu v0.1 profil, yalnız Traffic Class `0` için sayısal varsayımlar yapar.

### 2.5 Policy evidence ve kaynak bütçesi

| Parametre | Değer | İşlem |
|---|---:|---|
| `T_caution_evidence` | 1.5 s | Süregelen hazard/belirsizlik kanıtı bu süre tutulursa CAUTION değerlendirilir. |
| `T_protect_evidence` | 2.5 s | Süregelen/şiddetli bozunma + ek safe successor bu süre tutulursa PROTECT değerlendirilir. |
| `T_recovery_evidence` | 4.0 s | Olumlu toparlanma kanıtının gerekli minimum süresi. |
| `T_protect_min` | 2.0 s | Gerekçesi korunursa PROTECT'te kalınacak asgari süre. |
| Olağan triggered FIELD_UPDATE oranı | Alan başına en çok 5/s | `T_coalesce = 0.2 s` ile oluşan yerel üst sınır. |
| DFSN request dalgası | Alan başına en çok 2 / 4 s | `N_req` ve `T_req_session` ile sınırlandırılır. |

Kontrol: `T_recovery_evidence = 4.0 s >= max(1.5 s, 2.5 s)`. Safe successor/ACTIVE koşulu kaybedilirse `T_protect_min` beklenmez: yedeklilik derhal kapanır ve repair akışı uygulanır.

## 3. Uygulama zamanlayıcı işlemi

Bu profilin timerları aşağıdaki öncelik sırasıyla işletilir:

1. Paket veya link olayı, güvenlik / biçim / ACTIVE / feasibility / freshness kapılarını önce değerlendirir.
2. Mevcut successor için ACTIVE/feasibility/freshness kapısı başarısızsa forwarding hemen durur; timer yalnız repair veya cache temizliği için kalır. Biçim, AUTH veya replay reddi ise yalnız o paketi düşürür; mevcut successor'ı tek başına kaldırmaz.
3. Geçerli kanıt varsa ilgili komşu veya ilan timerı sıfırlanır; eski ADS/Message-ID bu etkiyi üretemez.
4. Aynı anda birden çok timer dolarsa önce withdrawal ve neighbor invalidation, sonra safe-candidate yeniden hesabı, sonra field expiry/repair, en son policy evidence işlenir.
5. Timer handler'ı kendi kendine sınırsız yeni mesaj üretemez; her mesaj `T_coalesce`, deneme sayısı ve per-field budget'a tabidir.

Bu sıra bir flowchart değildir; uygulamada atomik state güncellemesi ve event-queue önceliği için normatif işlem sırasıdır.

## 4. Doğrulama listesi

| Testlenebilir koşul | Beklenen sonuç |
|---|---|
| Sessiz ACTIVE komşu, 2.0 s boyunca iki-yönlü kanıt üretmez | Idle PROBE gider; geçerli reply 3.0 s fresh süreyi yeniler. |
| Idle PROBE ve iki failure-bound PROBE cevapsız kalır | Komşu STALE/SUSPECT/EXPIRED geçişini en geç 5.0 s içinde tamamlar; data candidate değildir. |
| Normal FIELD_UPDATE'ların biri kaybolur | 3.0 s lifetime içinde sonraki update ulaşır; field candidate expire olmaz. |
| Seçili field update'ler kaybolur | 1.5 s guard'da en çok iki FIELD_SOLICIT; gerekirse iki dalgalı, coalesced DFSN_REQUEST; en geç 6.0 s sonra FORWARDABLE veya UNREACHABLE. |
| Eski finite update, withdrawaldan sonra gelir | ADS/withdrawal cache nedeniyle finite successor olmaz. |
| Aynı DFSN_REQUEST tekrar gelir | Request-ID duplicate cache nedeniyle birden çok iletilmez. |
| Gerçek request retry gerekir | Yeni Request-ID kullanılır; aynı `K` için request coalescing ve `N_req` sınırı korunur. |
| REPAIR buffer'daki Class-0 DATA 6.0 s geçer | Paket bırakılır ve local delivery-failure üretilir; Data-ID cache 10.0 s korunur. |
| PROTECT'te safe alternate kaybolur | 2.0 s dwell beklemeden replication durur. |

## 5. Sınırlar ve sonraki kararlar

- Bu profil, gerçek radyo/MAC gecikmesini veya filo yoğunluğunu ölçmez; bu nedenle performans veya enerji garantisi değildir.
- `D_control`, `D_data`, `H_data`, `H_req` veya buffer boyutu çalışma ortamını karşılamazsa aynı TR ilişkileriyle yeni bir profil türetilmelidir.
- Traffic Class `1…255` buffer profilleri bu profile dâhil değildir. CostQuantum ve metrik eşikleri, ayrı fakat uyumlu M0.1 profile'ında `35`te tanımlıdır. Security Profile 1'in header/CPU overhead'i `26`da wire olarak tanımlıdır; ölçülmüş performans/enerji profili henüz değildir.
- Timerlar yalnız doğru çalışan düğümler için soft-state davranışını sınırlar. Kimlik sahteciliği ve R1 control replay `26`daki security profile ile ele alınır; RF/verification kaynak tüketim saldırılarının ölçülmüş kapasite sınırı complexity fazında ayrıca değerlendirilmelidir.

## 6. Karar gerektiren öneri

Bu belge, aşağıdaki **Dengeli Profile v0.1** seçimini önerir:

- 1.0 s FIELD_UPDATE refresh, 3.0 s ilan/freshness ömrü, 2.0 s idle probe;
- 0.5 s probe reply, en çok iki failure-bound probe, 5.0 s neighbor retention;
- 1.5 s field refresh guard, en çok iki solicit; `H_req=16`, iki DFSN request dalgası, 6.0 s repair;
- Class-0 için 6.0 s repair buffer ve 10.0 s DATA duplicate cache;
- 1.5/2.5/4.0 s policy evidence/recovery süreleri;
- field başına en çok 5 triggered update/s ve 2 DFSN request dalgası/4 s.

Bu profil; failure detection, control overhead, buffer gecikmesi ve policy tepkisini değiştirdiği için MAJOR bir karardı. Proje sahibi tarafından DESPARETE ilk sürümü için onaylanmıştır. Yine de "standart" veya doğrulanmış performans optimumu değildir; gerçek operasyon varsayımları değişirse sürümlü profil revizyonu gerekir.
