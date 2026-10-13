# DESPARETE — Timerlar, Yaşlandırma ve Yerel Süre Sınırları

**Sürüm:** 0.1 (onaylı timer/aging mimarisi; sayısal başlangıç profilleri `21` ve M0.1 `35`tedir)  
**Durum:** Onaylı alan, komşu, tazelik, onarım, kontrol, wire, R1 anti-replay ve M0.1 metric-epoch kararlarını zaman/state davranışına bağlar.  
**Tarih:** 2026-09-20

## 1. Amaç, kapsam ve değişmez sınırlar

Bu belge, DESPARETE'nin soft-state'ini hangi yerel zamanların yönettiğini; timerın ne zaman başlatılıp sıfırlandığını ve süre sonunda hangi **yerel** davranışın zorunlu olduğunu tanımlar. Sayısal eşik veya saniye değeri tanımlamaz.

Timerlar aşağıdaki güvenlik kanıtlarının yerine geçmez:

- Hop Limit, timer ve retry sayısı data-plane döngü özgürlüğünün kanıtı değildir; safe-successor / DFSN / feasibility kuralları değişmeden kalır.
- Bir timerın dolması jamming, fiziksel ağ partition'ı veya hedef kaybı hükmü değildir.
- Timer yalnızca local monotonic clock ile ölçülür. Node'lar arasında saat eşitlemesi, mutlak zaman damgası veya GPS zamanı varsayılmaz.
- Sert yerel link hatası, authenticated yerel-link kimlik/oturum çelişkisi veya ACTIVE successor kaybı, bekleyen timerdan önce forwarding'i durdurur. Biçim, AUTH veya replay reddi yalnız ilgili paketi düşürür; tek başına mevcut successor/neighbor state'ini değiştirmez. Timerlar güvenlik kapısını geciktiremez.

Bu ayrım, RFC 8966'daki farklı komşu, rota, istek ve periyodik-update zamanlarının ayrı tutulması yaklaşımıyla uyumludur; ancak o RFC'nin önerilen saniye değerleri DESPARETE için varsayılan değildir. [RFC 8966](https://www.rfc-editor.org/rfc/rfc8966.html)

## 2. Zaman kaynakları ve ortak notasyon

| Sınıf | Tanım | Saat/encoding | Güvenlik rolü |
|---|---|---|---|
| Alınan süre ipucu | `FIELD_UPDATE.Lifetime` içindeki, göndericinin ilanını tekrar etme üst sınırına ilişkin hint | Wire'da 16-bit, 100 ms kuanta | Alıcı, aday alan-ilanını ne kadar tutabileceğini sınırlar. |
| Yerel geçerlilik timerı | Bir kanıt veya ilanın son geçerli alımından itibaren node'un başlattığı süre | Yerel monotonic clock | Süre bitince ilgili candidate/neighbor forwarding'den çıkar. |
| Yerel işlem timerı | Probe, solicit, DFSN request, repair veya buffer işlemi için yapılan yerel bekleme | Yerel monotonic clock | İşlem tekrarını, sonlanmasını ve kaynak kullanımını sınırlar. |
| Periyodik gönderim timerı | FIELD_UPDATE tazeleme ve normal gözlem için node'un gönderim ritmi | Yerel monotonic clock + bounded jitter | Soft-state'in gereksiz sonlanmasını azaltır; correctness'in tek dayanağı değildir. |
| Dwell/evidence timerı | Policy postürü giriş-çıkışında kanıtın sürmesini ölçer | Yerel monotonic clock | Tekil gürültüden kaynaklı flapping'i azaltır. |
| Metric epoch timerı | ACTIVE peer ölçümlerinden Q/H/U/R/C yeniden hesaplama ritmi | Yerel monotonic clock | Metrik band değişimlerini deterministikleştirir; komşu/field safety timerı değildir. |

`T_x` bir yerel süreyi; `N_x` azami deneme sayısını; `J_x` gönderim/scheduling jitter üst sınırını; `D_x` tek işlem için profile tanımlı üst gecikmeyi belirtir. Hiçbir `T_x` negatif olamaz. Bir profile, `T_x=0` ile "hemen" davranışı tanımlamak isterse bunun pakete, kuyruğa veya tekrar döngüsüne yol açmadığını ayrıca göstermelidir.

## 3. Parametre profili: sayı değil, açık sözleşme

Her uyumlu node aynı **zamanlama sınıfını** kullanmalıdır. Farklı sayısal değerler birbiriyle birlikte çalışabilir; fakat en yavaş/uzun profile göre convergence ve kaynak sınırı kötüleşir. Bu nedenle `TimingProfile-ID` gelecekte CAPABILITY veya yönetim profiliyle açıkça ilan edilmelidir; v0.1 core mesajları bu alanı henüz taşımaz.

| Grup | Zorunlu parametreler | Kullanıldığı yer |
|---|---|---|
| Komşu | `T_fresh`, `T_idle_probe`, `T_probe_start`, `T_probe_reply`, `N_probe`, `T_retention` | ACTIVE/STALE/SUSPECT/EXPIRED yaşam döngüsü |
| Alan ilanı | `T_adv_refresh`, `J_adv`, `L_adv_max`, `G_adv_refresh`, `T_adv_cache`, `T_withdraw_cache`, `T_coalesce`, `T_urgent` | FIELD_UPDATE alımı, tazeleme, withdrawal |
| Tek-atlama alan edinimi | `T_solicit_reply`, `T_solicit_backoff`, `N_solicit` | FIELD_SOLICIT |
| Çok-atlama DFSN istemi | `T_req_session`, `T_req_retry`, `N_req`, `T_req_duplicate` | DFSN_REQUEST coalescing, retry ve duplicate bastırma |
| Onarım/buffer | `T_repair_max`, `T_buffer[class]`, `Q_buffer[field,class]` | REPAIRING/UNREACHABLE ve delivery-failure |
| Politika | `T_caution_evidence`, `T_protect_evidence`, `T_recovery_evidence`, `T_protect_min` | STEADY/CAUTION/PROTECT histerezisi |
| Metrik | `T_metric_epoch`, `W_Q`, `N_Q`, hazard epoch örnek sayısı | M0.1 Q/H/U/R/C hesaplama ve policy predicate kaynakları |
| Duplicate/replay | `T_ctrl_duplicate`, `T_data_duplicate`, `T_retired_oiid`, `AR_i[(Sender-ID,Instance-ID)]` | Kısa duplicate cache, DATA cache, OIID state ve R1 authenticated-control high-water |

Bu parametreler protokol sabiti değil profile bağlıdır. Uygulama, bir alan veya trafik sınıfına daha dar bir **yerel** sınır koyabilir; ancak bir alıcının aldığı ilanın wire Lifetime'ını uzatamaz.

## 4. Zorunlu zaman ilişkileri

Sayılar seçilmeden önce aşağıdaki ilişkiler korunmalıdır. Bunlar yalnız performans önerisi değil; erken expiry, stale replay ve kontrol fırtınasını önleyen tasarım koşullarıdır.

| Kimlik | Koşul | Gerekçe |
|---|---|---|
| TR-01 | `T_retention >= T_fresh + T_probe_session` | STALE sonrası probe süreci bitmeden kayıt EXPIRED olmamalıdır. |
| TR-02 | `T_probe_session >= N_probe × T_probe_reply` ve her deneme arasında rate-limit/jitter bütçesi hesaba katılmalıdır. | Probe sayısı kağıt üzerinde değil gerçek bir sonlanma sınırı olmalıdır. |
| TR-03 | `L_adv_sent > T_adv_refresh + J_adv + D_adv` | Göndericinin normal tazelemesi, alıcının ilanı düşürmesinden önce ulaşabilecek bir boşluk bırakmalıdır. |
| TR-04 | `L_adv_effective = min(Lifetime × 100 ms, L_adv_max)` | Gönderen alıcının soft-state sınırını büyütemez. |
| TR-05 | `G_adv_refresh >= T_solicit_reply + J_solicit + D_solicit` | Seçili ilan expire olmadan önce FIELD_SOLICIT yanıtı için bir fırsat kalmalıdır. |
| TR-06 | `T_withdraw_cache >= L_adv_max + D_reorder` | Eski sonlu ilanın withdrawal cache silindikten sonra yeniymiş gibi kabul edilmesi engellenir. `D_reorder`, profile ait azami tek-atlama kontrol gecikmesi/reorder varsayımıdır. |
| TR-07 | `T_req_duplicate >= T_req_session` | Aynı DFSN_REQUEST, yerel işlem tamamlanmadan yeniden işlenemez/iletilemez. |
| TR-08 | `T_repair_max` en az seçilen solicit ve DFSN-request deneme pencerelerinin toplamını kapsamalıdır. | Node, istem hâlâ yürürken UNREACHABLE sonucuna atlamaz. |
| TR-09 | `T_recovery_evidence >= max(T_caution_evidence, T_protect_evidence)` | Çıkışın girişten daha zayıf kanıtla yapılması flapping yaratmaz. |
| TR-10 | `T_data_duplicate` en az `T_buffer[class] + H_data × D_data` kadar olmalıdır. | Buffer'dan gecikmiş veya birden çok ilk-atlama kopyası duplicate-cache dışında kalmamalıdır. `H_data` ve `D_data` profile sınırlarıdır. |
| TR-11 | `T_retired_oiid` serial ve mesaj gecikmesi üst sınırlarını aşmalıdır. | Eski instance'a ait geç paket yeni field olarak canlanamaz. |
| TR-12 | `T_idle_probe + T_probe_reply + J_probe + D_probe < T_fresh` | Sessiz fakat sağlıklı ACTIVE komşu, normal doğrulama fırsatı olmadan STALE'e düşmez. |

Bir sistem `D_reorder` veya `D_data` için sonlu operasyonel üst sınır vermiyorsa, timer temelli stale/replay korunması hakkında güçlü bir garanti veremez. Security Profile 1, aktif peer için R1 strict high-water uygular; receiver restartından sonraki kalıcı anti-replay bu profilin iddiası değildir.

## 5. Komşu timerları

| Timer / olay | Başlatma veya yenileme | Süre sonu / hata işlemi | Forwarding etkisi |
|---|---|---|---|
| `T_fresh` | Yalnız forwarding-grade iki-yönlü kanıt: uygun unicast/ACK veya eşleşen PROBE_REPLY | ACTIVE → STALE; seçili successor ise doğrulama planlanır | Komşu hemen data adayı olmaktan çıkar. |
| `T_idle_probe` | ACTIVE komşudan `T_idle_probe` boyunca forwarding-grade kanıt gelmemişse | Normal profilde tek PROBE başlat; geçerli reply `T_fresh`i yeniler | Sessiz/boşta linklerde gereksiz ACTIVE → STALE dalgalanmasını önler; tekrar sayısı `N_probe` tüketmez. |
| `T_probe_start` | Niteliksiz, rosterla doğrulanmış doğrudan peer adayı; veya STALE/CAUTION/PROTECT'te ek doğrulama ihtiyacı | Geçerli gerekçe hâlâ sürüyorsa qualification veya failure-bound PROBE oturumu başlat | Tek başına ACTIVE yapmaz. |
| `T_probe_reply` | Geçerli qualification ya da failure-bound PROBE gönderildiğinde | Deneme başarısız sayılır; `N_probe` tüketilir; kalan deneme varsa rate-limitli tekrar, yoksa UNQUALIFIED/SUSPECT → EXPIRED | Bekleyen probe, komşuyu ACTIVE tutmaz. |
| `T_retention` | Niteliksiz direct-peer kaydı açıldığında ve her forwarding-grade kanıtta | ACTIVE dışındaki kayıt EXPIRED olur; ilanlar, successor adaylığı ve varsa ilgili R1 high-water kaydı kaldırılır | EXPIRED komşu ancak yeni doğrudan kanıtla yeniden nitelendirilebilir. |

Sert link hatası veya authenticated, yerel-linke bağlanmış kimlik/oturum çelişkisi, `T_fresh` beklemeden ACTIVE → SUSPECT/EXPIRED yolunu tetikleyebilir. Malformed veya bad-signature paket tek başına komşu state'ini düşürmez. Pasif duyma, `T_fresh`i yenilemez; yalnız gözlem/belirsizlik bilgisini etkileyebilir.

## 6. FIELD_UPDATE ve alan-ilanı yaşlandırması

### 6.1 Gönderim ve coalescing

Bir node, FORWARDABLE alanı için kendi mevcut `P_i[K]` veya withdrawal durumunu `T_adv_refresh` ritminde tazeler. Successor, potential veya state değişiminde triggered update üretir.

| Durum | En geç gönderim | Coalescing kuralı |
|---|---|---|
| Sonlu potential düşüşü / aynı durum güncellemesi | `T_coalesce` içindeki en güncel state | Aynı `K` için birden çok değişim tek FIELD_UPDATE'ta birleştirilebilir; ADS son state'i temsil eder. |
| Successor değişimi veya potential artışı | `T_urgent` içinde | Eski state yerine yalnız en güncel state ilan edilir; ADS artar. |
| Withdrawal | Yerel forwarding durdurulduğu anda veya en geç `T_urgent` içinde | Sonlu update ile asla birlikte kodlanmaz; withdrawal daha eski queued finite update'i geçersiz kılar. |

`T_urgent <= T_coalesce` olmalıdır. Withdrawal'ın kendi forwarding gate'i zamanlanmış ilandan önce uygulanır; timer yalnız komşulara görünürlüğü sınırlar.

### 6.2 Alım ve expiry

`j`den alınan geçerli `A_j[K]` ilanı için `i` aşağıdaki kaydı tutar:

```text
advertisement_expiry = receipt_monotonic_time + L_adv_effective
L_adv_effective = min(received Lifetime × 100 ms, L_adv_max)
```

Bu timer yalnız ileti biçimi, sender-instance, `K`, DFSN, ADS ve komşu durumu doğrulandıktan sonra yenilenir. Eşit/eski ADS, süreyi uzatamaz. Komşu ACTIVE değilse ilan cache'de kalabilir fakat successor adayı değildir.

Seçili `A_j[K]` için `advertisement_expiry - G_adv_refresh` anında node, aynı alan için bekleyen bir solicit yoksa ve budget izin veriyorsa `FIELD_SOLICIT` gönderir. İlan expire olursa:

1. ilgili ilan successor adaylığından çıkarılır;
2. safe candidate kümesi yeniden hesaplanır;
3. alternatif yoksa §16'daki withdrawal + REPAIRING + coalesced DFSN_REQUEST işlemi uygulanır.

Withdrawal alınca node önce ADS/freshness bilgisini `T_withdraw_cache` boyunca tutar; withdrawal finite successor olarak asla tutulmaz. Bu cache, normal advertised-potential cache'inden ayrı yönetilir.

## 7. FIELD_SOLICIT, DFSN_REQUEST ve repair zamanları

| İşlem | Başlatma | Bounded çalışma | Başarı | Sonlandırma |
|---|---|---|---|---|
| FIELD_SOLICIT | Alan yok, seçili ilan expiry guard'a girdi veya tazelik yeniden edinimi gerekli | En çok `N_solicit`; her deneme için `T_solicit_reply`, ardından `T_solicit_backoff` | Geçerli FIELD_UPDATE gelir; normal field kuralları yine uygulanır | Başarısızsa yalnız uygun koşulda coalesced DFSN_REQUEST veya devam eden repair. |
| DFSN_REQUEST | Acquisition, feasible-starvation veya freshness ambiguity; aynı `K` için tek pending işlem | `T_req_session` boyunca en çok `N_req`; retry arası en az `T_req_retry`; duplicate cache `T_req_duplicate` | Yeni/geçerli OIID/DFSN veya safe FIELD_UPDATE field'i FORWARDABLE yaparsa işlem sonlanır | Süre biterse eski alan geri açılmaz; `REPAIRING → UNREACHABLE` değerlendirilir. |
| REPAIRING | Safe successor kalmaz | En çok `T_repair_max`; solicit/request işlemlerini içerir | Geçerli safe successor bulunur | Sınır sonunda UNREACHABLE; buffer politikası ayrı uygulanır. |

DFSN_REQUEST için retry, her hop'ta bağımsız flooding değildir. Aynı Request-ID bir node'da `T_req_duplicate` süresince en fazla bir kez işlenir/iletilebilir. Bu nedenle requester'ın gerçek yeniden denemesi yeni bir Request-ID üretmelidir; aynı `K` için farklı request'ler coalescing tablosunda birleştirilebilir ve hedefte tek DFSN ilerletmesine karşılık gelebilir.

### 7.1 Wire/semantik uyuşmazlığı — çözülmüş karar

`18_DESPARETE_CONTROL_MESSAGES.md`, başlangıçta DFSN_REQUEST'ın "Hop-limit ve lifetime" taşıdığını söylerken onaylı `19_DESPARETE_WIRE_FORMAT_TLV.md` yalnız Hop Limit içeriyordu. Bu uyuşmazlık proje sahibi kararıyla aşağıdaki B seçeneği yönünde çözülmüştür.

| Seçenek | Değişiklik | Kazanç | Bedel |
|---|---|---|---|
| A — Wire lifetime ekle | DFSN_REQUEST'taki mevcut 16-bit Reserved alanını `Request Lifetime` (100 ms kuanta) yap. | Her request, gönderici tarafından ifade edilmiş bir temporal üst sınır taşır. | Ek wire semantiği; forwarder/alıcının lifetime yorumunu ve ileride authentication'ın mutable-field kuralını tanımlamak gerekir. |
| **B — Yerel işlem süresi kullan (seçildi)** | `18`deki "lifetime taşır" ifadesini kaldır; temporal sınırı yalnız `T_req_session` ve `T_req_duplicate` ile yerel profile bağla. | Onaylı wire profile değişmez; Hop Limit mekânsal, yerel timer zamansal sınır olur. | Heterojen profillerde aynı request farklı node'larda farklı süre yaşar; profil uyumu daha önemli olur. |

`18` belgesi B seçeneğine göre düzeltilmiştir. DFSN_REQUEST'ın temporal sınırı artık local monotonic timerlardır; 16-bit Reserved wire alanı rezerve kalır.

## 8. Buffer, duplicate ve emekli state yaşları

| Kayıt | Başlatma | En az saklama / silme kuralı | Kaynak sınırı |
|---|---|---|---|
| REPAIR buffer'daki DATA | Paket kabul edildiğinde | Paket `T_buffer[class]` sonunda veya quota aşılınca bırakılır; local delivery-failure oluşur | `Q_buffer[field,class]`; hiçbir field tüm belleği alamaz. |
| DATA duplicate cache | Data-ID ilk görülünce | TR-10 koşulu | Sabit/bounded LRU benzeri profil; eviction exact-once vaadi doğurmaz. |
| Kontrol duplicate cache | Control Message-ID ilk görülünce | `T_ctrl_duplicate`; request için ayrıca TR-07 | Sender-instance ve kapasite bağlamlıdır. |
| DFSN request cache | Request-ID ilk görülünce | `T_req_duplicate` | Bounded; same-K coalescing ayrı kayıttır. |
| Withdrawal cache | Geçerli withdrawal alınca | TR-06 | Finite candidate cache'den mantıksal olarak ayrıdır. |
| Retired OIID | Yeni OIID kabul edilince | TR-11 | Destination başına bounded emekli-instance listesi gerekir. |

`T_buffer[class]` ile `T_repair_max` için evrensel bir sıralama zorunlu değildir. Düşük gecikmeli trafik `T_buffer < T_repair_max` seçebilir ve onarım tamamlanmadan teslim başarısızlığı üretebilir. Güvenilirlik odaklı trafik `T_buffer >= T_repair_max` seçebilir. Bu, uygulama trafik-sınıfı sözleşmesinde seçilmelidir; çekirdek protokol bu iki davranışı eşitlemez.

## 9. Policy evidence ve dwell timerları

| Timer | Başlatma | Süre sonu etkisi | Güvenlik sınırı |
|---|---|---|---|
| `T_caution_evidence` | M0.1 `CautionEvidence` (`H≥64 ∨ U≥128`) başlar | Kanıt kesintisiz sürerse STEADY → CAUTION | Yüksek U tek başına PROTECT/replication açmaz. |
| `T_protect_evidence` | M0.1 `ProtectEvidence` (`H≥128`) ve ek safe successor birlikte görülür | Kanıt sürer ve trafik izinliyse CAUTION → PROTECT | Safe alternate kaybı bu timerı beklemeden replication'ı kapatır. |
| `T_recovery_evidence` | M0.1 `RecoveryEvidence` (`H<64 ∧ U<128`) kesintisiz oluşur | CAUTION → STEADY veya PROTECT → CAUTION | Doğrudan PROTECT → STEADY yoktur. |
| `T_protect_min` | PROTECT girişinde | En erken normal çıkış değerlendirme anı | Successor/feasibility kaybı bu dwell'i geçersiz kılar; unsafe yedeklilik asla sürmez. |

Policy timerları risk maliyetini veya feasibility distance'i değiştirmez. Bu timerların expire olması, yalnız gözlem sıklığı, prepare/solicit hakkı ve izinli redundancy davranışını değiştirir.

## 10. Sayısal profili seçmek için gerekli insan kararı

Bu mimari, aşağıdaki operasyonel tempo seçilmeden dürüst sayısal default üretmez:

| Tempo | Beklenen etki | Uygun çalışma bağlamı |
|---|---|---|
| Hızlı taktik | Daha kısa `T_fresh`, hızlı repair/probe; daha yüksek kontrol enerjisi ve collision riski | Kısa bağlantı ömürleri, düşük gecikme önceliği, yeterli kontrol bütçesi |
| Dengeli (başlangıç önerisi) | Saniye mertebesinde evidence/refresh; orta overhead | Heterojen FANET ve ilk uygulanabilir profil |
| Tasarruf odaklı | Daha uzun freshness/refresh; daha düşük overhead fakat daha geç arıza algısı | Enerji ve kanal yükünün baskın olduğu, gecikmeye toleranslı görev |

Seçimden sonra sayısal profil, her parametre için değer, birim, jitter aralığı, minimum/maksimum, trafik-sınıfı farklılığı ve TR-01…TR-11 doğrulamasıyla ayrı bir profile belgesinde dondurulmalıdır. Simülasyon, bu tasarım fazının parçası değildir; sayılar burada doğrulanmış performans sonucu gibi sunulmayacaktır.

## 11. Gereksinim izlenebilirliği

| Unsur | Gereksinimler |
|---|---|
| Ayrı komşu/alan/istek soft-state timerları | FR-01, FR-03, FR-06, FR-10, FR-11 |
| Bounded solicit/request/repair/buffer | FR-03, FR-06, FR-13, NFR-01–NFR-03 |
| Withdrawal, OIID ve duplicate saklama | FR-09, FR-10, FR-13, NFR-06 |
| Policy histerezisi | FR-02, FR-08, FR-12 |
| Saat senkronizasyonu gerektirmeme | NFR-03, NFR-06 |

## 12. Karar gerektiren tasarım önerisi

Önerilen timer mimarisi şudur:

1. Her soft-state türü (komşu, alan-ilanı, request, buffer, duplicate, OIID) ve M0.1 metric epoch'u bağımsız yerel timerla işletilir.
2. Wire'daki FIELD_UPDATE Lifetime, alıcıda `min(received, local cap)` olarak kullanılır; gönderici periyodu lifetime ve jitter ilişkisini TR-03'e uydurur.
3. Safety event'leri timerdan önce forwarding'i durdurur; timerın rolü yalnız kanıtın yaşlanması ve bounded recovery'dir.
4. Sayısal sabitler, seçilecek operasyonel tempo ve traffic-class sözleşmesi olmadan verilmez.
5. DFSN_REQUEST için B seçeneği uygulanır: wire lifetime yoktur; temporal kapsam yerel request-session ve duplicate timerlarıyla sınırlandırılır.

Bu karar, komşu availability, field expiry, repair gecikmesi ve kontrol yükünü etkilediği için MAJOR'dır.
