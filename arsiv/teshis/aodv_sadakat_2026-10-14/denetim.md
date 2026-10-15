# AODV sadakat taraması — tamamlama (K-242 · K-244)

> 14 Ekim 2026 · kaynaklar: RFC 3561 (`protokol_kaynaklari/rfc3561_aodv.txt`), ns-3 `aodv-routing-protocol.cc` (`protokol_kaynaklari/uygulama_kaynaklari/ns-3/`) · önceki denetim K-208 (`arsiv/teshis/aodv_sadakat_2026-09-30/denetim.md`) · bağımsız denetimin AODV taraması (DD-04): 40 kural hedefinden önce beş bulguyla kesilmişti; dördü K-242'de düzeltildi, beşincisi (RERR'in hep yayınla gitmesi) bu taramada ele alındı.

## İlke

RFC birincil: MUST ve SHOULD uygulanır. RFC'nin sustuğu ya da kendi içinde çeliştiği yerde ve seçeneğe ya da MAY'e bıraktığı yerde ns-3'ün varsayılanı alınır (K-244; Babel'de babeld, OLSRv2'de olsrd2 aynı rolde). ns-3'ün RFC'de olmayan eklemeleri alınmaz (K-208).

## Sonuç

42 kural. Bu taramada iki yeni değişiklik: karşılıksız RREP (G bayrağı) ve RERR'in iletim biçimi. İkisi de ns-3'ün varsayılanı; ikisi de AODV'yi güçlendirir. Kalan beyanlı sapmalar: yerel onarım (ns-3'te de yok), RREP-ACK mesajı (bilgi getirmez), TTL'nin yükte taşınması (+1 B), sıra karşılaştırmasının sarmasız olması.

"Kanıt" sütunu: **14 Ekim** = bu taramada kod, RFC ve ns-3 satırları yeniden okundu; **K-208** = 30 Eylül'ün kural kural denetimi, bu taramada yalnız testinin geçtiği görüldü.

| # | RFC | kural | gerçekleme | durum | kanıt |
|---|---|---|---|---|---|
| 1 | §5.1 | RREQ 24 B | 24 + 1 B (TTL yükte, beyanlı) | beyanlı | test |
| 2 | §5.2 | RREP 20 B | 20 B | uyumlu | test |
| 3 | §5.3 | RERR 4 + 8n B | aynı | uyumlu | test |
| 4 | §6.1 | kaynak sırası RREQ'ten önce artar | `_rreq_kur` | uyumlu | 14 Ekim |
| 5 | §6.1 · §6.6.1 | hedef yanıtında sıra: §6.1 ile §6.6.1 çelişir | §6.6.1 (ns-3) | uyumlu | K-208 |
| 6 | §6.1 | sıra karşılaştırması işaretli 32 bit, sarmalı | sarmasız (değerler binlerde) | beyanlı | K-208 |
| 7 | §6.2 | kullanılan rotada hedef, sonraki atlama ve kaynak ömrü | `sonraki_atlama` | uyumlu | 14 Ekim |
| 8 | §6.2 | önceki atlamanın ömrü ve komşuluğu | K-242 | düzeltildi | 14 Ekim |
| 9 | §6.2 | öncül listeleri | `Rota.oncular` | uyumlu | K-208 |
| 10 | §6.3 | G bayrağı: *"SHOULD … if for any reason the destination is likely to need a route"* | her RREQ'te (ns-3 `GratuitousReply` varsayılanı) | **K-244** | 14 Ekim |
| 11 | §6.3 | hedef sırası bilinmiyorsa U | `BAYRAK_U` + `SONSUZ_SIRA` | uyumlu | 14 Ekim |
| 12 | §6.3 | RREQ kimliği artar; kendi RREQ'i `PATH_DISCOVERY_TIME` saklanır | `_rreq_kur` · `_bakim` | uyumlu | 14 Ekim |
| 13 | §10 | `RREQ_RATELIMIT` 10/s, aşan RREQ ertelenir | ns-3 gibi | uyumlu | K-208 H10 |
| 14 | §6.3 | keşif sürerken veri tamponda | 64 paket · 30 s (ns-3, K-198) | uyumlu | K-198 |
| 15 | §6.3 | en büyük TTL'de `RREQ_RETRIES` deneme, üstel geri çekilme | iki deneme, `NET_TRAVERSAL_TIME · 2^(n−1)`; ns-3 `RouteRequestTimerExpire` · `ScheduleRreqRetry` ile aynı | uyumlu | 14 Ekim |
| 16 | §6.3 | başarısız keşfin paketleri düşer (SHOULD) | K-242 | düzeltildi | 14 Ekim |
| 17 | §6.4 | genişleyen halka: TTL 1 · 3 · 5 · 7, sonra `NET_DIAMETER`; bekleme `RING_TRAVERSAL_TIME` | ns-3 ile aynı ilerleyiş | uyumlu | 14 Ekim |
| 18 | §6.4 | geçersiz girdide ilk TTL atlama + `TTL_INCREMENT` | K-208 H7 | uyumlu | 14 Ekim |
| 19 | §6.5 | önceki atlamaya sırasız rota | K-208 H1 | uyumlu | K-208 |
| 20 | §6.5 | (kaynak, RREQ kimliği) tekrar bastırma | `_gorulen_rreq` | uyumlu | 14 Ekim |
| 21 | §6.5 | ters rota oluşturma/güncelleme, ömür `max` | K-208 H2 | uyumlu | K-208 |
| 22 | §6.5 | TTL > 1 ise iletim, atlama + 1, hedef sırası `max` | K-208 H3; U iner, G kalır (K-244) | uyumlu | 14 Ekim |
| 23 | §6.8 | kara listedeki komşunun RREQ'i yok sayılır | `kontrol_alindi` | uyumlu | 14 Ekim |
| 24 | §6.6.1 | hedef yanıtı: atlama 0, ömür `MY_ROUTE_TIMEOUT` | 11,2 s (K-242) | düzeltildi | 14 Ekim |
| 25 | §6.6.2 | ara düğüm yanıtı koşulu (U bayraklı RREQ dâhil, ns-3) | K-208 H4 | uyumlu | 14 Ekim |
| 26 | §6.6.2 | ara düğüm yanıtının alanları ve iki öncül | `_rreq_isle` | uyumlu | 14 Ekim |
| 27 | §6.6.2 | D bayrağı | kurulmaz (ns-3 `DestinationOnly` kapalı) | uyumlu | 14 Ekim |
| 28 | §6.6.3 | G kuruluysa hedefe karşılıksız RREP (MUST), RFC'nin alan listesi | K-244 | **K-244** | 14 Ekim |
| 29 | §6.7 | dört güncelleme koşulu (i)–(iv) | K-205 | uyumlu | K-208 |
| 30 | §6.7 | RREP yalnız rota kurulduysa ya da güncellendiyse iletilir | RFC (ns-3 koşulsuz iletir, alınmadı) | uyumlu | 14 Ekim |
| 31 | §6.7 | iletirken ters rota ömrü ve öncül eklemeleri | K-208 H5 | uyumlu | 14 Ekim |
| 32 | §6.8 | RREP başarısızlığında kara liste, `BLACKLIST_TIMEOUT` halka formülüyle | bağ katmanı onayıyla (RFC'nin izni, K-194); karşılıksız RREP dâhil; RERR başarısızlığı kara liste kurmaz (K-244, `iletim_sonucu` eşlemesi) | uyumlu | 14 Ekim |
| 33 | §5.4 · §6.7 | RREP-ACK mesajı | gönderilmez: ns-3 yalnız komşu hedefe ara düğüm yanıtında ister; tek-yayın RREP'in 802.11 onayı aynı tek yönlü bağı sezer | beyanlı | 14 Ekim |
| 34 | §6.9 | HELLO yalnız son `HELLO_INTERVAL`da yayın yoksa | `_hello` | uyumlu | 14 Ekim |
| 35 | §6.9 | HELLO alanları: TTL 1, ömür `ALLOWED_HELLO_LOSS · HELLO_INTERVAL` | `_hello` | uyumlu | 14 Ekim |
| 36 | §6.9 | HELLO alınınca komşu rotası, sıra MUST | K-208 H6 | uyumlu | K-208 |
| 37 | §6.9 · §6.10 | `ALLOWED_HELLO_LOSS · HELLO_INTERVAL` boyunca hiçbir paket yoksa bağ kayıp | her kontrol mesajı ve veri teması kanıt | uyumlu | 14 Ekim |
| 38 | §6.11 (i) | kopmada ulaşılamazlar: komşu ve onu sonraki atlama yapan rotalar; öncül süzmesi; sıra artar; `DELETE_PERIOD` | `_bag_koptu` · `_gecersizlestir` | uyumlu | 14 Ekim |
| 39 | §6.11 (ii) | etkin rotası olmayan ara düğüm RERR gönderir, paket düşer | öncül süzmesiz (K-210) | uyumlu | 14 Ekim |
| 40 | §6.11 (iii) | RERR alınınca gönderenden geçen rotalar geçersiz, sıra kopyalanır, öncüllere iletilir | `_rerr_isle` | uyumlu | 14 Ekim |
| 41 | §6.11 | RERR'in iletim biçimi: yayın, tek-yayın ya da ardışık tek-yayın (MAY) | tek öncüle tek-yayın, çok öncüle yayın; (ii)'de veri kaynağına rota varsa tek-yayın (ns-3 `SendRerrMessage` · `SendRerrWhenNoRouteToForward`) | **K-244** | 14 Ekim |
| 42 | §10 | `RERR_RATELIMIT` 10/s | `_hiz_sinirli_mi` | uyumlu | 14 Ekim |

**Beyanlı, değişmedi:**
- §6.12 yerel onarım: MAY, ns-3'te yok.
- §6.13 yeniden başlatma: koşularda yeniden başlatma yok.
- §5.2 önek: tek arayüz, düz adresleme.

**§10 sabitleri** ns-3'ün öznitelik varsayılanlarıyla karşılaştırıldı: `ActiveRouteTimeout` 3 s · `HelloInterval` 1 s · `AllowedHelloLoss` 2 · `NetDiameter` 35 · `NodeTraversalTime` 40 ms · `RreqRetries` 2 · `TtlStart` 1 · `TtlIncrement` 2 · `TtlThreshold` 7 · `TimeoutBuffer` 2 · `RreqRateLimit` · `RerrRateLimit` 10 · `MyRouteTimeout` 11,2 s (K-242) · `MaxQueueLen` 64 · `MaxQueueTime` 30 s; hepsi aynı. Tek fark `BlackListTimeout`: ns-3 5,6 s (`RREQ_RETRIES · NET_TRAVERSAL_TIME`), bizde 16,8 s. RFC §10 halka araması kullanılınca formülü SHOULD ile büyütüyor; RFC'nin değeri alındı (K-194).

## Kara listenin tür eşlemesi (K-244)

RERR ve karşılıksız RREP tek-yayın olunca "kontrol iletimi başarısız" bildirimi artık yalnız RREP'e ait değil. AODV `iletim_sonucu`yu (K-151) taşır: her tek-yayın kontrol çerçevesinin sonucu, o komşuya gönderilen kontrol mesajlarının sıradakiyle eşlenir ve `iletim_basarisiz` kara listeyi yalnız RREP'te kurar.

Eşleme iki durumda kayabilir: kontrol kuyruğunun taşması (mesaj iletilmeden düşer) ve titreşimin aynı komşuya 10 ms içinde giden bir RREP ile bir RERR'in sırasını değiştirmesi. Kayan eşlemede tür bilinmez ve RREP sayılır; bu, K-244'ten önceki davranış. İkisi de seyrek; etkisi yalnız kara liste kararıdır.

## AOMDV'ye etkisi

AOMDV `_rreq_kur`, `_rerr_kur`, `_rrep_kur` ve `iletim_basarisiz`i AODV'den devralır:
- RERR'in iletim biçimi ve kara listenin tür eşlemesi AOMDV'de de geçerli.
- G bayrağı AOMDV'nin RREQ'inde de kurulur, ama AOMDV'nin kendi ara düğüm yanıtı karşılıksız RREP göndermez ve iletimde bayrakları sıfırlar.
- AOMDV rakip değil; regresyon vakaları değişir (Faz 4'ün kaydı).
