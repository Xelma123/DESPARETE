# DESPARETE — Kaynak Sınırları ve Karmaşıklık Analizi

**Sürüm:** 0.1 (onaylı kaynak/karmaşıklık analizi; platform kapasite profili henüz seçilmedi)  
**Durum:** NFR-01…NFR-03 için onaylı routing, timer ve Security Profile 1'in ölçülebilir state/message/CPU sınırlarını çıkarır. Simülasyon veya performans sonucu değildir.  
**Tarih:** 2026-09-21

## 1. Amaç ve analiz sınırı

Bu belge, “sınırlı” kelimesini sayısal performans iddiasına dönüştürmeden DESPARETE'nin hangi state ve işlemle büyüdüğünü gösterir. Buradaki üst sınırlar, doğru çalışan node'ların onaylı profile uyması ve saldırganın fiziksel radyo kanalını tamamen kapatmadığı varsayımı altındadır.

UAV işlemcisi, radio MTU, airtime, batarya, node sayısı, aktif komşu sayısı, uygulama data hızı ve signature verification kapasitesi ölçülmediği için bu belge bir kapasite kabul testi vermez. Bu parametreler deployment profile girdisidir; seçilmeden “SWaP uygundur” denemez.

## 2. Notasyon

| Sembol | Anlam |
|---|---|
| `n` | Görev rosterındaki toplam Node-ID sayısı. |
| `d_i` | Node `i`nin ACTIVE veya retention içindeki komşu örneği sayısı. |
| `f_i` | `i`de tutulmuş Destination/OIID field bağlamı sayısı; tek-sink v0.1'de normalde en fazla bir aktif destination, fakat retired/diagnostic state ayrıca olabilir. |
| `b_i` | `i`nin yerel repair buffer paket kapasitesi. |
| `λ_ctrl,i`, `λ_data,i` | `i`nin kabul ettiği control/data paket hızı; deployment profiliyle sınırlanmalıdır. |
| `V_i` | `i`nin sürdürülebilir Ed25519 verification kapasitesi (verify/s); ölçülmesi gerekir. |
| `E_H(i)` | `i`den en fazla `H_req=16` atlamada erişilebilen active directed control kenarları kümesi. |
| `Δ` | Bu kümedeki en büyük active degree. |

`n`, `d_i`, `f_i`, `λ_*` ve `V_i` için bu şartname sayı atamaz; bunlar platform/mission inputudur. `H_req=H_data=16`, `T_*` ve packet header boyutları ise onaylı v0.1 profile aittir.

## 3. Düğüm-başı kalıcı ve soft state

| State grubu | Asimptotik büyüme | Açıklama ve üst sınır davranışı |
|---|---|---|
| TrustRoster | `O(n)` | Her Node-ID için aktif public key(ler). Görev öncesi yüklenir; routing control ile büyümez. |
| Neighbor + R1 anti-replay | `O(d_i)` | Komşu lifecycle, probe, en çok son 16 uygun sonuç + üç 0.5 s M0.1 hazard epoch özeti ve `AR_i[(Sender-ID,Instance-ID)]` high-water. Her komşu için metrik state'i `O(1)`dir; AR kaydı komşu EXPIRED olana dek yaşar. |
| Per-neighbor field ilanları | `O(d_i × f_i)` | Her active/retained neighbor için field/OIID/DFSN/ADS/potential/expiry. Withdrawal/advertisement cache timerla atılır. |
| Local field, FD, policy, acquisition | `O(f_i)` | Successor, alternate, FD, policy evidence ve bounded request session. Tek-sink profile bu katmanı küçük tutar. |
| Duplicate / request cache | `O(λ_ctrl,i × T_ctrl_duplicate + λ_data,i × T_data_duplicate)` | Request-ID için ayrıca `T_req_duplicate`; cache kapasite dolarsa yeni paket state yaratmadan reddedilmelidir. |
| Repair buffer | `O(b_i)` | `Q_buffer[field,class]` ile field/class başına en çok yerel buffer'ın %10'u ve 32 paket sınırı uygulanır. |
| Retired OIID / ordering | `O(f_i)` ile profile bağlı bounded geçmiş | `T_retired_oiid`, `T_adv_cache`, `T_withdraw_cache` dolunca diagnostic state temizlenir; persistent R2 tombstone bu sürümde yoktur. |

Sonuç: routing soft state'i `O(d_i × f_i + b_i + duplicate-cache)`dir; Security Profile 1 bunun üstüne `O(n + d_i)` roster ve R1 state'i ekler. İlk-sürüm tek-sink kullanımı `f_i`yi pratikte sınırlasa da bu, çok-hedef için otomatik `O(1)` garantisi değildir.

## 4. Normal ve failure control üretimi

| Kaynak | Yerel üretim sınırı | Ağ kapsamı |
|---|---|---|
| Normal FIELD_UPDATE | Forwardable field başına `T_adv_refresh=1.0 s` ile en fazla 1/s | Tek-atlama. Gelen update körlemesine forward edilmez. |
| Triggered FIELD_UPDATE | Field başına en fazla 5/s | Tek-atlama; `T_coalesce=0.2 s` ile birleşir. Normal ve triggered bağımsız çakışırsa muhafazakâr yerel üst sınır `6 × f_i` update/s'dir. |
| Idle PROBE | Sessiz ACTIVE komşu başına en fazla 1 / `T_idle_probe=2.0 s` | Tek-atlama unicast; normal kanıt varsa tetiklenmez. |
| Failure-bound PROBE | Bir failure oturumunda en çok `N_probe=2` | Tek-atlama; oturum `T_probe_session=1.3 s` ile sonlanır. |
| FIELD_SOLICIT | Acquisition/refresh oturumunda en çok `N_solicit=2` | Tek-atlama; state coalescing uygulanır. |
| DFSN_REQUEST | Field başına en çok 2 dalga / 4 s | `H_req=16`, Request-ID başına node başına en çok bir forward. |
| FAILURE_REPORT | Sadece bağımsız safe report field varsa | Report field'in normal safe-successor yolu; ters-yol flood'u yoktur. |
| M0.1 metric epoch | Her `0.5 s`de ACTIVE komşu başına bounded yerel hesap | Paket üretmez; band değişimi ancak mevcut `T_coalesce`/field başına 5/s triggered-update sınırlarıyla etkili olabilir. |

Bir DFSN_REQUEST dalgasında, erişilebilir active subgraph içinde her node Request-ID'yi en çok bir kez işlediğinden toplam forward iletimi şu topoloji-bağımlı üst sınırı aşmaz:

```text
M_request-wave(i) ≤ |E_H(i)| ≤ Δ × |V_H(i)|
```

Burada `V_H(i)`, isteğin 16-hop yarıçapında gerçekten erişebildiği node kümesidir. Bu, requestin küçük veya enerji açısından ucuz olduğu iddiası değildir; yalnız kalıcı ve sınırsız mechanism olmadığını, her dalganın Hop Limit + Request-ID + `N_req` ile sonlandığını gösterir.

## 5. DATA çoğaltma ve iletim sınırı

İlk-sürüm ingress profili `RB∈{0,1}` ve `MaxReplicaFanout=2`dir. Bir source DATA paketi ya tek yoldan iletilir ya da yalnız bir node'da primary + secondary olarak ikiye ayrılır. İki çıkışın RB'si `0` olur.

Bu nedenle application tekrarları hariç toplam DESPARETE DATA iletim denemesi:

```text
M_data ≤ 2 × H_data = 32
```

atlama düzeyindedir. Bu, delivery, düşük gecikme, link-layer tekrarlarının sayısı veya radio broadcast maliyeti garantisi değildir. DATA source proof her kopyada aynı kalır; her hop kendi yeni HopSignature'ını üretir.

## 6. Security Profile 1 wire ve kripto maliyeti

| Paket türü | Uzantısız header | Profile-1 header | Artış | Alıcıdaki imza doğrulama |
|---|---:|---:|---:|---:|
| DATA | 36 | 194 | +158 octet | 2: HOP + SOURCE |
| FIELD_UPDATE | 60 | 210 | +150 octet | 2: HOP + ORIGIN |
| FIELD_SOLICIT | 52 | 130 | +78 octet | 1: HOP |
| DFSN_REQUEST | 72 | 150 | +78 octet | 1: HOP |
| PROBE | 40 | 118 | +78 octet | 1: HOP |
| PROBE_REPLY | 52 | 130 | +78 octet | 1: HOP |
| FAILURE_REPORT | 84 | 162 | +78 octet | 1: HOP |

Gönderen her iletimde bir HopSignature üretir. Source, DATA başına bir SourceSignature; target, yeni `(OIID,DFSN)` bağlamı başına bir OriginSignature üretir ve relay'ler bu origin proof'u yeniden üretmez. Bu tablo Ed25519 algoritma performansı hakkında benchmark değildir; yalnız `26`daki zorunlu doğrulama sayısını sayar.

Bir node, doğrulama kuyruğunu platform budget'ı ile sınırlandırmalıdır. Gerekli güvenlik koşulu:

```text
admitted signature-verification work ≤ V_i
```

Bu koşul sağlanamıyorsa node, yeni paketi pre-auth veya verification kuyruğunda sessizce bırakır; security, freshness veya safe-successor kapısını gevşetmez. Biçim/TLV/length/roster bağları signature verification'dan önce kontrol edilir. Bu, signature-flood'un fiziksel/radio DoS'a dönüşmesini önlemez; CPU ve state amplifikasyonunu sınırlar.

## 7. İşlem karmaşıklığı

| İşlem | Beklenen çalışma | Not |
|---|---|---|
| Roster ve komşu lookup | `O(1)` ortalama veya `O(log n)` | Seçilen map/indeks yapısına bağlıdır. |
| HOP/ORIGIN/SOURCE doğrulama | Sabit sayıda signature doğrulaması | Kripto primitive maliyeti `V_i` ile platforma bağlıdır; big-O burada yanıltıcı olabilir. |
| FIELD_UPDATE candidate yazma | `O(1)` kayıt güncelleme | Ardından field candidate seçimi gerekir. |
| Field recompute | Basit taramada `O(d_i)` | Heap/indeks optimizasyonu MAY olabilir, fakat stale/feasibility invalidation karmaşıklığını artırır. |
| DATA forward | `O(1)` primary; en fazla bir alternate kontrolüyle `O(d_i)` basit tarama | En fazla iki protected output. |
| DFSN_REQUEST forward | `O(d_i)` | ACTIVE komşulara birer copy; Request-ID cache bunu node başına bir kezle sınırlar. |
| M0.1 metric update | Komşu başına `O(1)`; tüm ACTIVE komşular için epoch başına `O(d_i)` | Etkilenen candidate alanlarının basit yeniden hesabı ek olarak en kötü `O(d_i × f_i)` tarama yapabilir; implementasyon yalnız değişen metric bandında bu işi planlar. |

Küçük `d_i` beklemek bir FANET gözlemidir, protokol garantisi değildir. İlk sürüm, daha düşük asimptotik katsayı uğruna safety/security state'ini sessizce atmaz.

## 8. Admission ve tükenme davranışı

Kaynak tükenmesi altında aşağıdaki öncelik sırası korunmalıdır:

1. Format veya roster kapısından geçemeyen paket için signature, buffer, field veya error-message state'i ayırma.
2. Geçerli fakat verification budget dışında kalan paket için sessiz drop; mevcut successor/FD/neighbor state'i değiştirmeme.
3. Authentication sonrası duplicate/replay paketi için yeni buffer, request veya forwarding oluşturmama.
4. Yeni DATA buffer/replica kabul edilemezse local delivery-failure; eski unsafe route'a geri dönmeme.
5. Yeni control üretimi, existing `T_coalesce`, `N_*`, per-field rate budget ve Request-ID sınırlarını aşmama.

Kontrol ile DATA'nın aynı pre-auth CPU kuyruğunu nasıl paylaşacağı, `V_i`, maksimum ingress hızları ve radio MTU deployment profile olmadan sayısal olarak atanamaz. Bu bir açık platform kapasitesi sorusudur; kabulden önce konfigurasyon/yük testi ile kapatılmalıdır.

## 9. Doğrulama yükümlülükleri

| Konu | Testlenebilir kabul sonucu |
|---|---|
| State limiti | Komşu, field, cache ve buffer sınırına geldiğinde yeni kayıt/packet güvenli biçimde reddedilir; mevcut FD/successor değişmez. |
| Control sınırı | Triggered update, solicit, probe, request dalgası kendi `T_*`/`N_*` üst sınırını geçmez. |
| Request sonlanması | Aynı Request-ID bir node'da ikinci kez forward edilmez; Hop Limit 0'da iletim olmaz. |
| Replication sınırı | RB 0/1 ile üçüncü output veya downstream fanout oluşmaz. |
| Crypto admission | Invalid/malformed trafik verify budget veya hata yanıtı amplifikasyonu yaratmaz. |
| M0.1 metric sınırı | Node başına yalnız 16 sonuç + üç epoch özeti tutulur; M0-TV-01…M0-TV-05, metric band değişiminde normal recompute/update rate sınırının korunduğunu gösterir. |
| Header sığması | Tüm Profile-1 minimumları 255-octet Header Length sınırını geçmez; taşıyıcı MTU uygunluğu deployment testidir. |
| Platform kapasitesi | Seçilmiş `n`, `d_i`, `λ_*`, `b_i`, `V_i` için measurement/load test sonucu kayıt altına alınır. |

## 10. Açık profil girdileri ve sonraki karar

Bu analiz algoritmik sınırları kapatır; aşağıdakiler bilerek açık kalır:

- görev roster büyüklüğü `n`, eşzamanlı active komşu/field üst sınırı ve taşıyıcı MTU;
- platformun Ed25519 sign/verify throughput'u, pre-auth/verification queue boyutu ve adil paylaşım politikası;
- application DATA hızı, payload boyutu, Traffic Class `1…255` buffer quota/ömürleri;
- Security Profile 1 header artışının radio airtime/batarya etkisi.

Bu değerler olmadan sayısal overhead veya uçuşa uygunluk iddia edilmez. Sonraki tasarım işi, hata/telemetri sözleşmesiyle bu admission/reddetme olaylarını gözlemlenebilir yapmak; ardından deployment-capacity profile ve tamamlık denetimidir.
