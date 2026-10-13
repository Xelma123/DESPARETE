# DESPARETE — Güvenlik Mimarisi ve Karar Seçenekleri

**Sürüm:** 0.1 (karar kaydı; Security Profile 1 seçildi)  
**Durum:** SD-01…SD-04 proje sahibi tarafından onaylandı; normatif semantik `26`ya taşındı. Bu belge seçenek ve takas kaydı olarak korunur.  
**Tarih:** 2026-09-20

## 1. Amaç ve sınır

DESPARETE'nin loop-freedom ve freshness argümanı, doğru çalışan node'ların OIID/DFSN yetkisine uyduğunu varsayar. Radyo erişimi olan bir saldırgan sahte veya tekrar oynatılmış paket enjekte edebiliyorsa bu varsayım tek başına geçerli değildir. Bu belge, özellikle `FIELD_UPDATE`, `DFSN_REQUEST`, `PROBE/PROBE_REPLY` ve DATA için hangi güvenlik bağının gerektiğini seçime hazırlar.

Bu taslak; kripto kütüphanesi, sertifika altyapısı, anahtar dağıtım protokolü, RF anti-jamming, güvenilir yürütme ortamı veya payload gizliliği uygulamaz. Authentication, erişilebilirlik garantisi değildir: saldırgan yine paketi bastırabilir, geciktirebilir veya radyo kanalını meşgul edebilir.

## 2. Mevcut tasarımın sağladığı ve sağlamadığı şeyler

| Mevcut mekanizma | Sağladığı | Tek başına sağlamadığı |
|---|---|---|
| OIID + DFSN + ADS + local age | Dürüst göndericiler arasındaki stale/ordering semantiği | Sahte sender, sahte target veya kaydedilmiş geçerli paketin sonsuz süre sonra yeniden oynatılması |
| Control/Data/Request duplicate cache | Kısa penceredeki aynı kimliğin tekrar işlemesini sınırlar | Cache atıldıktan sonraki cryptographic replay |
| ACTIVE + nonce-bağlı PROBE/REPLY | İki yönlü canlılık kanıtı | Gönderici kimliğinin kriptografik sahibi olduğu |
| `0x81` critical AUTHENTICATION TLV | Fail-closed uzantı yeri | Algoritma, anahtar kimliği, kapsam, replay ve key rollover semantiği |
| Hop Limit, request quota ve sessiz drop | Flood/yanıt amplifikasyonunu sınırlar | RF DoS, pahalı imza-doğrulama DoS'u veya yetkili kötü niyetli node |

Bu nedenle `23`teki “required authentication” kapısı, bir profil seçilene dek boş bir hook'tur. Bu belge onaylanmadan `SA-01`deki doğru-node varsayımı saldırgan radyo ortamına genişletilemez.

## 3. Korunacak varlıklar ve güvenlik hedefleri

| Kimlik | Hedef | Başarı ölçütü |
|---|---|---|
| SG-01 | Hop gönderen kimliği ve paket bütünlüğü | Yetkisiz bir radyo vericisi, kabul edilen paketin Sender-ID/Instance, body veya payload'ını üretemez ya da değiştiremez. |
| SG-02 | Target-only OIID/DFSN yetkisi | Target dışındaki node, kabul edilen yeni `(Destination-ID,OIID,DFSN)` bağlamını yetkiliymiş gibi başlatamaz veya ileri taşıyamaz. |
| SG-03 | Replay sınırı | Korunan paket, tanımlanan anti-replay penceresi dışında routing/neighbor state'i ilerletemez veya canlandıramaz. |
| SG-04 | Neighbor kanıtı | Authentication, canlılık yerine geçmez; yalnız geçerli, taze PROBE challenge'ına sahip doğrulanmış yanıt forwarding-grade kanıt üretir. |
| SG-05 | Kaynak korunumu | Biçim ve ucuz sınırlar, pahalı kriptografik doğrulamadan önce uygulanır; başarısız paket hata paketi üretmez. |
| SG-06 | Açık kalıntı risk | Doğrulanmış fakat kötü niyetli bir node'un kendi link metriği/potentiali hakkında yalan söylemesi, fiziksel jamming ve yol üzeri drop ayrı açık riskler olarak kalır. |

DATA gizliliği SG-01…SG-06'nın içinde değildir. Gizlilik gerekiyorsa uygulama veya link taşıyıcısı tarafından AEAD ile sağlanmalıdır; AEAD hem bütünlük hem gizlilik sağlar fakat anti-replay veya erişim kararlarını tek başına çözmez. [RFC 5116](https://www.rfc-editor.org/rfc/rfc5116.html)

## 4. Tehdit–etki–azaltım haritası

| Tehdit | Protokol etkisi | Seçilmiş profile gereken azaltım | Korunmayan kalıntı |
|---|---|---|---|
| Sahte FIELD_UPDATE / withdrawal | Sahte potential, route blackhole, yanlış repair | Hop kimlik doğrulaması + target origin proof | Doğrulanmış relay kendi local potentialini dürüst olmayan biçimde ilan edebilir. |
| Sahte OIID veya DFSN | Freshness/feasibility invariantının tabanını bozar | Target'ın imzaladığı origin proof zorunlu olmalı | Target private key compromise. |
| Eski FIELD_UPDATE replay | Expire olmuş route'un yeniden aday olması | Auth sonrası sender anti-replay penceresi, ADS ve OIID kuralları | Receiver state kaybı/uzun gecikme için seçilen replay profiline bağlıdır. |
| PROBE_REPLY replay/spoof | Sahte ACTIVE komşu | Authenticated, alıcıya özgü ve taze Probe-ID echo | Jamming veya gerçek peer'in yanıt vermemesi. |
| DFSN_REQUEST injection | Gereksiz target update/control yükü | Hop auth + Request-ID/quota + target-side request budget | Yetkili kötü niyetli node kendi kimliğiyle quota tüketebilir. |
| DATA değiştirme/replay | Yanlış payload, RB/hop/manipüle delivery | Seçime bağlı source ve hop integrity; Data-ID cache | Cache ötesi exactly-once yoktur. |
| Yanlış risk/DIAGNOSTIC | Haksız policy veya rota etkisi | Risk zaten wire route girdisi değildir; DIAGNOSTIC forwarding'i değiştiremez | Yerel doğrulanmış node ölçümünü yalanlayabilir. |
| Paket taşması / signature flood | CPU, bellek veya radyo tüketimi | Header/TLV boyut sınırı, pre-auth rate limit, sabit verification bütçesi, sessiz drop | RF DoS önlenemez. |

`MODE_NOTICE` çekirdekten kaldırıldığı için “sahte global kriz bildirimi” saldırı yüzeyi ilk sürümde yoktur.

## 5. Mutability ve doğrulama kapsamı

Bir kriptografik kapsama, yalnız hangi alanların immutable/mutable olduğuna göre güvenle anlam verilebilir.

| Paket / kanıt | Mutable alanlar | Zorunlu doğrulama kapsamı |
|---|---|---|
| Tek-atlama control (FIELD_UPDATE, SOLICIT, PROBE, REPLY) | Forward edilmez; normalde alan yoktur | Taban başlık, Control Sender Block, core body ve auth dışındaki TLV'ler. |
| DFSN_REQUEST hop iletimi | Hop Limit azalır; Control Sender Block forwarder'a ait olur | Her forwarder, kendi gönderdiği gerçek byte dizisi için yeni hop-auth üretir. Request-ID ve requester context body içinde değişmez. |
| DATA hop iletimi | Hop Limit azalır; geçerli redundant olayda RB azalabilir | Her hop-auth ile gönderilen gerçek header + payload korunur; source proof seçilirse immutable Data-ID/payload ayrıca bağlanır. |
| FIELD origin proof | Relay potentiali, ADS, Lifetime, sender kimliği ve Hop Limit'i kapsamaz | En az `protocol-domain, Destination-ID, Target-ID, OIID, DFSN` bağlanır; yalnız target public key'i ile doğrulanır. |

Önerilen wire kuralı: auth taşıyan paket tek bir kritik AUTHENTICATION TLV taşır ve bu TLV header'ın son TLV'sidir. Canonical coverage, AUTHENTICATION TLV'nin type/length/value/padding'i hariç kalan header byte'ları ile varsa DATA payload'un tamamıdır. Bu kural yalnız hop-auth için yeterlidir; target origin proof veya source proof aynı TLV içinde açık alt-kayıt olarak ayrı belirtilmelidir.

## 6. Anti-replay gerçeği

Mevcut `T_ctrl_duplicate=4 s`, `T_adv_cache=4 s`, `T_retired_oiid=60 s` değerleri routing soft-state yönetimidir; uzun gecikmiş, geçerli imzalı bir pakete karşı tek başına sınırsız cryptographic anti-replay garantisi değildir. Bu ayrım normatif güvenlik iddiasından önce çözülmelidir.

| Replay seviyesi | Mekanizma | Garanti | Bedel |
|---|---|---|---|
| R0 — operasyon penceresi | Authentication sonrası mevcut Message-ID/ADS/Request-ID/Data-ID cache'leri | Cache ve ilgili active context yaşadığı sürece. Node restartı veya cache atımı sonrası sınırsız değil. | Ek wire/state yok. |
| R1 — aktif-peer penceresi | Her authenticated `(Sender-ID,Instance-ID)` için serial high-water/sliding window; state ACTIVE + retention boyunca korunur. Yeni instance, taze nonce-bağlı PROBE ile kabul edilir. | Aktif bir peer ve tek çalışma oturumu içinde eski paket state'i geri saramaz. | Reordering penceresi, per-neighbor state ve rollover kuralı gerekir. |
| R2 — reboot-dayanıklı replay | R1'e ek olarak target için kalıcı monoton `Target-Generation` ve alıcıda kalıcı anti-replay/tombstone state. | Alıcı/target restartı sonrasında da eski generation geri kabul edilmez. | Non-volatile state, wire alanı/kanıtı ve key rollover semantiği gerekir. |

`OIID` opak ve sıralı olmayan bir değer olduğundan, R2 yalnız mevcut OIID cache süresini uzatarak dürüstçe sağlanamaz. R2 seçilirse yeni, target-imzalı monoton generation bağının wire profile eklenmesi gerekir. GPS/zaman senkronu bu taslakta önkoşul değildir.

## 7. Kriptografik profil seçenekleri

| Profil | Kimlik / anahtar modeli | SG-01 | SG-02 | Başlıca bedel |
|---|---|---|---|---|
| P0 — açık radyo | Yok | Hayır | Hayır | FR-14'ün saldırgan radyo beklentisini karşılamaz. |
| P1 — tek mission-group HMAC | Tüm node'larda aynı gizli anahtar; ör. HMAC-SHA-256 tabanlı MAC | Dışarıdaki anahtarsız vericiye karşı evet | Hayır; anahtarı bilen her node target gibi MAC üretebilir | Düşük overhead, fakat compromised member kimlik taklidi yapabilir. HMAC paylaşılan gizli anahtara dayanır. [FIPS 198-1](https://csrc.nist.gov/pubs/fips/198-1/final) |
| P2 — node-identity signature | Her node için önceden bilinen public key; her korunan paket güncel sender tarafından imzalanır | Evet | Yalnız ek target origin proof ile evet | Ed25519 imzası 64 octettir; her hop verification CPU ve header maliyeti getirir. [RFC 8032](https://www.rfc-editor.org/rfc/rfc8032.html) |
| P3 — hibrit | P2 target origin proof + ayrı hop-auth (pairwise MAC veya hop signature) | Seçilen hop-auth'a göre evet | Evet | En iyi ayrım, fakat iki kanıt türü ve anahtar tedariki açıkça tanımlanmalıdır. |

Bir group HMAC, pakete `Sender-ID` yazılmasını güvenilir kimlik kanıtına dönüştürmez: aynı grup anahtarına sahip herhangi bir member başka bir Sender-ID/Instance ile geçerli MAC üretebilir. Bu yüzden target-only DFSN/OIID yetkisi korunacaksa P1 tek başına yeterli değildir.

Ed25519, küçük public key ve 64-octet signature kullanan tanımlı bir EdDSA örneğidir; bu onu uygun bir aday yapar, fakat DESPARETE için performans sonucu değildir. Kriptografik paket boyutu, işlem süresi ve anahtar saklama saha ölçümü olmadan “uygun” diye kesinlenemez. [RFC 8032](https://www.rfc-editor.org/rfc/rfc8032.html)

## 8. Onaylanan ilk-sürüm yönü

Taktik, açık radyo ortamı ve target-only sequence yetkisi birlikte düşünüldüğünde **P3** onaylandı:

1. Görev öncesinde her node için sabit `Node-ID → public-key` rosterı yüklenir; key rollover için açık bir `Key-ID` bulunur.
2. Target, her yeni OIID/DFSN bağlamı için Ed25519 `OriginProof` üretir. Ara FIELD_UPDATE, bu proof'u taşır; alıcı target key'iyle doğrulamadan yeni bağlamı kabul etmez.
3. Her iletim, hop sender tarafından üretilmiş ayrı `HopAuth` taşır. İlk taslakta bunun node-identity signature olması, ek pairwise-key-establishment mekanizması gerektirmediği için varsayımsal yön olarak en sade seçenektir.
4. DATA için source proof gerekip gerekmediği, uygulama payload bütünlüğü/menşei gereksinimine göre ayrı karar olur. Hop-auth tek başına yalnız son hop'ta paketi göndereni doğrular.
5. İlk güvenlik profili R1 ile başlar; mission/reboot boyunca eski route context'inin asla geri gelmemesi zorunluysa R2 seçilmeli ve wire format MAJOR revize edilmelidir.

P3, compromised bir node'un kendi public key'iyle geçerli ama yanlış local potential, eski fakat kendi imzaladığı data veya sahte ölçüm göndermesini çözmez. Bu, reputation tabanlı yönlendirme eklemek için gerekçe değildir; o mekanizma ilk sürüm kapsamı dışındadır.

## 9. Seçim gerektiren kapılar

| Karar | Seçenekler | Öneri | Neyi değiştirir |
|---|---|---|---|
| SD-01 saldırgan sınırı | Yalnız dış radyo saldırganı / en az bir compromised member da varsayılır | **Onaylandı:** compromised member varsayımı | P1 yerine P3 gerektirir. |
| SD-02 kimlik tedariki | Tek group key / görev öncesi node public-key rosterı | **Onaylandı:** public-key roster | Node impersonation ve target-only yetkisi. |
| SD-03 replay hedefi | R0 operasyon penceresi / R1 aktif-peer / R2 reboot-dayanıklı | **Onaylandı:** R1 ilk sürüm; R2 yeni MAJOR profil | State, restart semantiği ve olası wire değişimi. |
| SD-04 DATA koruması | Yalnız hop integrity / source integrity / source integrity + application-layer confidentiality | **Onaylandı:** source integrity; gizlilik uygulama katmanında ayrı karar | DATA AUTH TLV boyutu ve uygulama sözleşmesi. |

Bu dört karar alınmadan AUTHENTICATION TLV'nin algorithm id'si, TLV body boyutu, canonical signature input'u, key rollover, kabul kapısı ve timer/cache değişiklikleri dondurulamaz.

## 10. Kabulden sonraki zorunlu çıktı

Seçimden sonra şu değişiklikler ayrı bir MAJOR security profile olarak yapılır:

- `19` için AUTHENTICATION TLV alt-biçimi, criticality, maksimum boyut, exact byte coverage ve packet-type zorunluluk tablosu;
- `23` için `AcceptPacket` sıralaması, auth-before-state ve anti-replay yüksek-su işaretçisi;
- `22` için security failure'ın komşu/field etkisi ve R1/R2 state yaşam döngüsü;
- `20`/`21` için key/anti-replay cache ilişkileri, yalnız ölçülmüş veya açıkça varsayımlı değerlerle;
- FR-14, saldırı–etki–azaltım–kalıntı risk matrisi ve testlenebilir negatif senaryolar;
- header üst sınırı, CPU doğrulama bütçesi, state ve worst-case control yükü için complexity değerlendirmesi.

Bu taslağın sonraki aşaması yalnız seçilen profile ilişkin normatif semantiktir; flowchart üretimi veya simülasyon kapsamına girmez.
