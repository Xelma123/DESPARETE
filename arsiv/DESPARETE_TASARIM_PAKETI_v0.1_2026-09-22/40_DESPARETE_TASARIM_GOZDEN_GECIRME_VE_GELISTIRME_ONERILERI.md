# DESPARETE v0.1 — Tasarım Gözden Geçirmesi ve Geliştirme Önerileri

**Durum:** Öneri / karar girdisi. Normatif protokol değişikliği değildir.  
**İncelenen baseline:** v0.1 candidate taslağı (`36`), M0.1 metrik profili (`35`), Security Profile 1 (`26`), algoritmalar (`23`), wire format (`19`), zamanlama (`21`), kaynak-kapasite kapıları (`27`, `29`) ve test/freeze paketi (`37`–`39`).  
**İnceleme tarihi:** 22 Eylül 2026

## 1. Kısa hüküm

DESPARETE'nin çekirdek tasarımı tutarlı ve doğru yönde ilerliyor. Özellikle aşağıdaki kararlar birbirini destekliyor:

- Döngü güvenliğinin TTL veya link kalitesine değil, `(OIID, DFSN)`, feasible distance ve safe-successor kapısına bağlanması.
- Riskin `Q`, `H`, `U` bileşenlerinden ayrı tutulması ve M0.1'in yalnız yerel, doğrudan ve ACTIVE komşu gözlemini kullanması.
- Freshness belirsizliğinde fail-closed davranış; eski alanı iyimser biçimde kullanmama.
- Roster + hop imzası + target-origin proof ayrımı; bir relay'in target adına yeni OIID/DFSN uyduramaması.
- Repair, redundancy ve kaynak tükenmesinde eski/unsafe rotaya dönüş yapılmaması.

Bu inceleme, çekirdek safety mekanizmasını değiştirmeyi gerektiren bir çelişki bulmadı. Ancak uygulamaya başlamadan önce üç konu net karar haline gelmelidir: **taşıyıcı/link sonucu sözleşmesi**, **tanımsız Traffic Class davranışı** ve **MTU/kaynak ön-kabulünün uygulama başlangıcına alınması**.

## 2. Korunması gereken tasarım çekirdeği

| Korunacak karar | Neden korunmalı |
|---|---|
| `FD` + safe-successor + target yetkili DFSN | Döngü özgürlüğünün esas dayanağıdır; risk, timer veya policy bu kapıyı açmamalıdır. |
| Yeni OIID/DFSN için target OriginSignature | Relay'in origin context üretmesini engeller; freshness ile güvenliği birbirine bağlar. |
| ACTIVE olmadan forwarding-grade komşu saymama | Sadece rosterda olmak ya da tek yönlü paket almak forwarding yetkisi vermemelidir. |
| M0.1'in sınırlı yerel gözlem modeli | Ölçülmeyen global risk/jamming iddialarından kaçınır; ilk profilin uygulanabilirliğini korur. |
| Fail-closed repair ve bounded control | Hata altında kontrol patlaması veya stale rota kullanımı yerine sınırlı, gözlemlenebilir davranış sağlar. |
| Data-plane ile telemetri/management kararını ayırma | Uzaktan rapor veya zayıf gözlem, routing safety girdisi haline gelmemelidir. |

Bu maddeler bir sonraki sürümde geliştirilebilir; fakat basitleştirme amacıyla kaldırılmaları DESPARETE'nin ana güvenlik mantığını zayıflatır.

## 3. Önceliklendirilmiş iyileştirme önerileri

| Kimlik | Öncelik | Konu | Önerilen yön | Karar gerekir mi? |
|---|---:|---|---|---|
| TG-01 | P0 | Taşıyıcı/link sonucu sözleşmesi | DC-10 ve DC-11'i somut bir platform arayüzüne dönüştür. | Evet |
| TG-02 | P0 | Traffic Class `1…255` | Provision edilmemiş sınıflar için tek, güvenli varsayılan davranış tanımla. | Evet |
| TG-03 | P0 | MTU ve kaynak preflight | `29`daki ölçümleri deployment sonuna değil uygulama başlangıcına koşul yap. | Evet |
| TG-04 | P1 | DFSN artışının hedefte sınırlanması | Eşdeğer istek coalescing'ine ek olarak hedef-başına advancement rate gate tanımla. | Evet |
| TG-05 | P1 | OIID üretim ömrü | Target restartlarında benzersiz OIID üretme mekanizmasını normatifleştir. | Evet |
| TG-06 | P1 | FAILURE_REPORT'un yönetim güveni | Raporu yönlendirme kararından ayrı, açık güven seviyesi olan tanısal veri yap. | Evet |
| TG-07 | P1 | Node-geneli kaynak paylaşımı | Per-field limitlerin üstüne node-geneli admission ve kuyruk adaleti ekle. | Evet |
| TG-08 | P1 | Çalıştırılabilir safety kanıtı | Test planını küçük bir referans state modeli ve property sorgularıyla destekle. | Hayır; uygulama planı |
| TG-09 | P2 | Düşük trafikte M0.1 davranışı | CAUTION'a geçişin uçuş/mission verisiyle kalibre edilmesini planla; şimdilik eşikleri değiştirme. | Sonuçlara bağlı |
| TG-10 | P2 | Tek-sink sınırının korunması | Çok-hedef desteği gelene kadar bunu deployment ve API sınırı olarak açıkça uygula. | Hayır |

`P0`, protokolün güvenlik mantığından değil, iki farklı implementasyonun farklı davranmasını önlemek için uygulama öncesi kapanması gereken tasarım borcudur. `P1` ilk prototip öncesi veya ilk prototip sırasında kapanmalıdır. `P2` ise ölçümle yönlendirilmelidir.

## 4. Önerilerin ayrıntısı

### TG-01 — Taşıyıcı/link sonucu sözleşmesini somutlaştır

`23` doğrudan peer kimliği ve iki yönlü forwarding-grade kanıtı ister; `35` yalnız hedefli unicast'in uygun doğrudan sonuçlarından `Q/H/U` üretir. `29`da DC-10 ile taşıyıcı davranışı, DC-11 ile de final başarı/başarısızlık, retry sayısı ve monotonic sonuç zamanı istenir. Bunlar doğru girdilerdir; fakat henüz tek bir uygulama sözleşmesinde birleşmez.

**Öneri:** Platform katmanı en az şu immutable sonucu DESPARETE'ye vermelidir:

```text
LinkResult {
  directPeerNodeID,
  localLinkBinding,
  transmissionKind,          # unicast | broadcast
  finalOutcome,              # success | failure | unavailable
  retryCount,
  monotonicCompletionTime,
  packetCorrelationID
}
```

Ek kurallar:

1. `directPeerNodeID`, roster kimliğiyle aynı yerel linke bağlı olmalıdır; yalnız paket içi Sender-ID bu kanıtın yerine geçmez.
2. M0.1'e yalnız hedefli unicast için `success`/`failure` sonuçları girer; broadcast ve belirsiz taşıyıcı olayları yalnız tanısaldır.
3. `RecordForwardingProof` yalnız yerel gönderilmiş PROBE ile eşleşen, authenticated PROBE_REPLY ve geçerli local link binding birlikte varsa çağrılır.
4. Taşıyıcı sonucu yoksa kalite cezasını sıfırlamak yerine M0.1 preflight reddedilir ya da açıkça başka bir metrik profili seçilir.

**Kazanç:** Neighbor, security ve metric katmanları aynı fiziksel olayı farklı yorumlamaz.  
**Bedel:** Radio/MAC adaptörü yazmak ve platform test fixture'ı üretmek gerekir.  
**Önerilen karar:** Bu sözleşmeyi v0.1'in zorunlu implementasyon arayüzü olarak kabul etmek.

### TG-02 — Provision edilmemiş Traffic Class için güvenli varsayılan

Wire format `Traffic Class 1…255`i profile-defined bırakır. Dengeli zamanlama profili ise sadece Class-0 için buffer ömrü ve quota tanımlar. Bu boşluk, iki implementasyonun aynı DATA paketi için farklı buffering, redundancy veya öncelik davranışı üretmesine yol açabilir.

**Önerilen varsayılan:** Mission profile bir sınıfı açıkça provision etmediyse node:

- güvenli ve güncel field varsa normal tek-kopya forwarding yapabilir;
- field yoksa veya forwarding yapılamıyorsa repair buffer ayırmaz ve yerel delivery-failure üretir;
- sınıfa özel redundancy, scheduler önceliği veya quota vermez;
- bu kararı `UNPROVISIONED_TRAFFIC_CLASS` telemetrisiyle kaydeder.

Bu yaklaşım, bilinmeyen sınıfın sınırsız kaynak tüketmesini engeller; ama mevcut güvenli rotası olan normal DATA'yı gereksiz yere düşürmez.

**Alternatif:** Tanımsız sınıfı ilk hopta tamamen drop etmek. Bu daha basittir, ancak uygulama sürüm uyumunda sert kırılma yaratır.  
**Önerilen karar:** Yukarıdaki “normal forward, buffer/replica yok” varsayılanını seçmek ve ilk mission profile'da yalnız Class-0'ı provision etmek.

### TG-03 — MTU ve kaynak ön-kabulünü uygulama başlangıcına çek

Profile 1'de FIELD_UPDATE için en büyük header 210 octet, DATA için 194 octet + payload'dur. Fragmentation DESPARETE core tarafından tanımlanmamıştır. Mevcut `29` belgesi bunu doğru biçimde deployment kapısı yapar; buna rağmen codec, radio adaptörü ve mesajlaşma mimarisini kurmadan önce taşıyıcının sığma durumunu bilmek daha düşük maliyetlidir.

**Öneri:** İlk implementasyon sprintinin giriş kapısı şu minimal ölçümlerin kaydedilmesidir:

1. `MTU_link ≥ 210` ve `MTU_link ≥ 194 + P_data_max` veya açıkça doğrulanmış alt-katman fragmentation davranışı.
2. Broadcast/unicast, ACK/retry ve kayıp semantiği.
3. Hedef donanımda Ed25519 sign/verify kaba kapasite ölçümü.
4. Beklenen roster, eşzamanlı komşu ve maximum ingress için RAM bütçesi.

Bu bir “deploy-ready” iddiası değildir. Ama uyumsuz taşıyıcıyı codec tamamlandıktan sonra keşfetmeyi önler.

### TG-04 — Hedefte DFSN advancement rate gate ekle

Mevcut dar yetki doğru biçimde yalnız current OIID/current DFSN bağlamındaki `FEASIBLE_STARVATION` isteğinin bir tur artırmasına izin verir ve eşdeğer isteklerin coalesce edilebileceğini söyler. Yine de farklı Request-ID veya farklı geçerli requester'lar, özellikle yoğun arıza koşulunda hedefte ardışık yeni turn üretimine sebep olabilir. Bu safety ihlali değildir; control churn ve gereksiz field yenilenmesi riskidir.

**Öneri:** Target tarafına `DFSNAdvanceGate(K)` eklenmelidir:

- Her `K` için son advance zamanı ve coalesced request sayısı tutulur.
- Aynı kısa window içindeki geçerli starvation istekleri tek advance ile karşılanır.
- Window içinde tekrar gelen istekler için current origin update gönderilir veya sessizce coalesce edilir; yeni DFSN üretilmez.
- Kesin `T_dfsn_min` sayısı mission ölçümünden seçilir; ilk taslakta uydurma bir sayı yazılmamalıdır.

**Kazanç:** Target, geçerli fakat gürültülü control olayında turn üretim amplifikatörü olmaz.  
**Bedel:** Çok hızlı gerçek topology değişiminde yeni turn biraz gecikebilir.  
**Önerilen karar:** Gate'in varlığını v0.1 tasarımına eklemek; süre değerini platform/mission profile'a bırakmak.

### TG-05 — OIID üretimini implementasyon tercihi olmaktan çıkar

OIID, target restartı sonrası eski ve yeni field örneğini ayıran safety kimliğidir. Tasarım “target restartında yeni OIID” kuralını koyuyor; fakat yeni değer üretiminin benzersizliğini nasıl garanti edeceği henüz bir implementasyon sözleşmesi değildir.

**Öneri:** Target için şu iki seçenekten biri açıkça seçilmelidir:

| Seçenek | Artı | Eksi |
|---|---|---|
| Kalıcı monotonic boot/instance sayacı + benzersiz mission bağlamı | Yeniden başlatmalarda güçlü benzersizlik iddiası | Non-volatile state ve wear/rollback değerlendirmesi gerekir. |
| Görev öncesi ayrılmış instance aralığı veya mission controller tarafından atama | Operasyonel audit kolaylaşır | Ek mission hazırlık altyapısı gerekir. |

Sadece rastgele 64-bit sayı kullanmak çakışma olasılığını çok küçültür, ancak “asla yeniden kullanma” kuralını tek başına mutlak garantiye dönüştürmez. Seçilen yöntem `0` üretmemeli, target'ın aynı görevde önce kullandığı bağlamla çakışmamalı ve restart/rollback davranışını kayıt altına almalıdır.

### TG-06 — FAILURE_REPORT'u düşük yetkili yönetim telemetrisi olarak etiketle

FAILURE_REPORT yalnız hop bütünlüğü taşır; protokol zaten raporu routing girdisi yapmaz. Bu ayrım korunmalıdır. Management endpoint, rapordaki olayın uçtan uca kanıtlandığını veya ilk raporlayanın değişmeden korunduğunu varsaymamalıdır.

**Öneri:** v0.1 için rapor semantiğini “authenticated current-hop taşıdığı yerel failure gözlemi” olarak belgelemek; management UI/collector'da trust level ve ingress hop bilgisini göstermek. Rapor bir gün otomatik operasyon kararı, ceza veya misbehavior mekanizması başlatacaksa o yeni kullanım için source/origin proof veya ayrı güvenli telemetri kanalı tasarlamak gerekir.

Bu değişiklik bugünkü routing behavior'ını değiştirmez; yalnız raporun yanlış yorumlanmasını önler.

### TG-07 — Per-field limitlerin üstüne node-geneli admission politikası ekle

Mevcut tasarım per-field rate limit, duplicate cache, buffer ve verification davranışı konusunda güçlüdür. Buna karşılık control ve DATA'nın aynı pre-auth/verification kuyruğunu nasıl paylaşacağı ile total `V_verify`, cache ve buffer payının hangi field/peer arasında dağıtılacağı platform profiline bırakılmıştır.

**Öneri:** Tek bir `NodeAdmissionBudget` tanımlanmalıdır:

- Sabit toplam verification, control, repair-buffer ve telemetry bütçesi.
- Öncelik sırası: format/roster reddi → güvenlik doğrulaması → zorunlu withdrawal/neighbor invalidation → sınırlı control → DATA buffer/replica.
- Bir peer veya field kendi kotasını tükettiğinde diğerlerinin safety state'ini düşürmemeli; yalnız yeni işi güvenli biçimde reddedilmelidir.
- Bütçe reddi olayları peer/field kimliği ve neden koduyla ölçülmelidir; telemetri paket taşmasına dönüşmemelidir.

Bu, `27`deki fail-closed ilkeyi koruyarak pratik DoS/adillik davranışını belirginleştirir.

### TG-08 — Doğruluk argümanını çalıştırılabilir küçük state modeliyle destekle

`24`teki döngü özgürlüğü argümanı doğru handler uygulamasına dayanır. `37` ve `38` iyi bir conformance/event-trace temeli sağlar; fakat metin tek başına implementation hatasını yakalayamaz.

**Öneri:** Uygulama öncesi veya ilk implementasyonla birlikte, bounded node/field sayısına sahip küçük bir referans state modeli oluşturulsun. Model aşağıdaki property'leri her event sonrası kontrol etsin:

1. Seçilmiş successor her zaman güncel `FD` ve feasibility koşulunu sağlar.
2. Relay OIID/DFSN üretmez veya artırmaz.
3. Stale/ambiguous context veya ACTIVE olmayan peer, forwarding state'ini değiştiremez.
4. `RB=1` tek output, `RB=0` sıfır redundant output üretir.
5. Aynı Request-ID node başına ikinci kez forward edilmez.

Bu çalışma büyük ölçekli flight simülasyonu yerine, algoritma geçişlerini ve trace oracle'larını mekanik olarak sınayan küçük bir safety kontrolüdür.

### TG-09 — M0.1 düşük trafik davranışını ölçerek kalibre et

M0.1, az veya yaşlı örneklerde `U`yu yükselterek bilinmezliği görünür kılar. Örneğin iki saniye içindeki yalnız iki uygun sonuçta `U=128` ve CAUTION evidence oluşabilir. Bu, güvenlik açısından bilinçli muhafazakârlıktır; doğrudan hata değildir.

**Öneri:** İlk mission testinde aşağıdaki gözlemler toplanmalıdır:

- düşük data oranı, seyrek probe ve uzun sessizlikte CAUTION/STEADY oranı;
- bunun control airtime, alternate izleme ve user-visible delivery davranışına etkisi;
- aynı koşulda gerçek link başarısızlığı ile yalnız bilgi eksikliğinin ayrışma kalitesi.

Ölçüm olmadan `U` eşiklerini düşürmek veya “düşük trafik = sağlıklı link” varsayımı eklemek önerilmez. Gerekirse M0.2, sample coverage ve görev fazı bilgisini açık yeni bir profil olarak eklemelidir.

### TG-10 — Tek-sink v0.1 sınırını API ve konfigürasyonda zorla

Wire/field veri modeli çok-hedefe genellenebilir görünse de v0.1 algoritmaları tek `SinkID` için kaynak bütçesi, acquisition ve control davranışı tanımlar. Bu ayrım şimdiden doğru biçimde yazılıdır.

**Öneri:** İlk implementasyonda tek `SinkID` zorunlu konfigürasyon olmalı; farklı `Application-Destination-ID` için davranış açık yerel policy failure olmalıdır. Multi-sink desteği, ortak kaynak kotası, target key eşlemesi, class politikası ve control isolation için ayrı bir ADR olmadan etkinleştirilmemelidir.

## 5. Önerilen karar sırası

1. **D-TSR-01 — Carrier contract:** TG-01'deki minimum `LinkResult` ve direct-peer binding sözleşmesini onayla.
2. **D-TSR-02 — Traffic Class varsayılanı:** TG-02'deki “normal forward; buffer/replica/sınıf önceliği yok” kuralını onayla veya daha katı bir drop politikası seç.
3. **D-TSR-03 — Implementasyon preflight:** TG-03'teki MTU, ACK/retry, kripto ve RAM ölçümlerini kodlama başlangıç kapısı yap.
4. **D-TSR-04 — DFSN gate:** TG-04'teki target-başına advancement gate'i kabul et; sayısal window'u mission profile kararına bırak.
5. **D-TSR-05 — OIID lifecycle:** TG-05'teki kalıcı sayaç veya mission ön-atama seçeneklerinden birini seç.
6. **D-TSR-06 — Management trust:** TG-06'daki FAILURE_REPORT yorumunu kabul et.
7. **D-TSR-07 — Admission:** TG-07'deki node-geneli bütçeyi ilk implementasyonun architecture backlog'una al.

İlk beş karar, protokolün yönünü değiştirmez; mevcut tasarımın uygulamada deterministik ve denetlenebilir kalmasını sağlar.

## 6. Bilerek ertelenmesi gereken işler

Şu anda eklenmeleri, v0.1'i doğrulamadan karmaşıklaştırır:

- Otonom jamming teşhisi, reputation veya misbehavior routing.
- Multi-sink, çoklu target kaynak paylaşımı ve geniş QoS sınıf sistemi.
- R2 kalıcı global anti-replay state'i.
- DTN deposu, exactly-once teslim veya ters-yol flood.
- İkinci/üçüncü redundant output ve çok-atlama downstream fanout.

Bunlar ihtiyaç dışı değildir; yalnızca ayrı ölçüm, threat model ve kaynak bütçesi olmadan v0.1 çekirdeğine eklenmemelidir.

## 7. Önerilen sonraki çalışma akışı

```text
Tasarım kararları (TG-01...05)
        ↓
Carrier/MTU/crypto/RAM preflight
        ↓
Küçük referans state modeli + codec/metric testleri
        ↓
Conformance trace'leri ve 17 senaryo eşlemesi
        ↓
İnsan freeze değerlendirmesi
        ↓
Deployment-capacity kabulü
```

Bu sırada diyagramlar bağımsız bir iletişim artefaktı olarak daha sonra metne eşlenebilir. Bu belgedeki öneriler diyagramların yerine geçmez ve onları değiştirmez.

## 8. Sınırlar ve dürüst durum bildirimi

- Bu inceleme, belge tutarlılığı ve tasarım riskleri üzerinedir; flight test, radio benchmark veya runtime conformance sonucu değildir.
- V0.1 candidate metni tasarım düzeyinde güçlü bir baseline'dır; mevcut freeze kontrol listesine göre henüz `frozen`, `deploy-ready` veya SWaP-uygun değildir.
- Buradaki öneriler kabul edilmedikçe `05` karar günlüğü, `36` candidate specification veya diğer normatif dokümanlarda değişiklik yapmaz.

## 9. Kaynak haritası

| İnceleme başlığı | Birincil kaynaklar |
|---|---|
| Safety, freshness, repair, DFSN | `13`, `14`, `16`, `23`, `24`, `36` |
| Neighbor ve metrik | `10`, `11`, `12`, `15`, `21`, `35`, `36` |
| Wire, security ve reporting | `18`, `19`, `26`, `28`, `36` |
| Kaynak, taşıyıcı ve kapasite | `27`, `29` |
| Test, trace ve freeze durumu | `30`, `33`, `37`, `38`, `39` |

