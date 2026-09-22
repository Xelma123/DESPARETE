# DESPARETE — Durum Makineleri ve Atomik Olay İşleme

**Sürüm:** 0.1 (onaylı ilk-sürüm state modeli)  
**Durum:** Onaylı field, safety, policy, repair, wire, zamanlama ve yeniden-edinim kararlarını uygulanabilir durum eksenlerine böler.  
**Tarih:** 2026-09-20

## 1. Amaç ve kapsam

Bu belge, DESPARETE node'unun `i` birimindeki sürekli durumları, olayları ve geçiş önceliğini tanımlar. Amaç, aşağıdaki iki hatayı yapmamaktır:

- Komşu doğrulaması, field erişilebilirliği ve policy postürünü tek bir dev FSM'de birbirine karıştırmak.
- Bir event handler'ın geçici olarak bile STALE/SUSPECT komşuyu, stale field-ilanını veya feasible olmayan route'u forwarding'de kullanmasına izin vermek.

Bu nedenle node durumu, bağımsız fakat atomik olay işlemiyle bağlanan beş eksene ayrılır. Metin bir flowchart değildir; pseudocode fazında uygulanacak normatif state/transition sözleşmesidir.

## 2. Durum eksenleri

### 2.1 Node yerel durumu

| Eksen | Anahtar | Durumlar | Görev |
|---|---|---|---|
| Komşu yaşamı | `N_i[j]` | UNQUALIFIED, ACTIVE, STALE, SUSPECT, EXPIRED | `j` üzerinden iki-yönlü forwarding kanıtını yönetir. |
| Field erişilebilirliği | `F_i[K]`, `K=(Destination-ID,OIID)` | FORWARDABLE, REPAIRING, UNREACHABLE | Bu field için safe successor ile data iletilebilip iletilemeyeceğini yönetir. |
| Policy postürü | `Π_i[K]` | STEADY, CAUTION, PROTECT | Gözlem, doğrulama ve koşullu redundancy yoğunluğunu yönetir. |
| Edinim/onarım kontrolü | `A_i[d]` veya `A_i[K]` | QUIESCENT, SOLICITING, REQUESTING | FIELD_SOLICIT ve bounded DFSN_REQUEST yaşamını yönetir. |
| Paket kaydı | `B_i[Data-ID]` | ABSENT, HELD, FORWARDED, DROPPED | Duplicate bastırma ve kısa repair buffer davranışını yönetir. |

`UNQUALIFIED`, eski dört durumlu komşu çekirdeğine ek bir forwarding durumu değildir; yalnız ilk kanıt toplama kaydını gösterir. `ABSENT` ise field kaydının bulunmadığı anlamına gelir, `F_i[K]`nin dördüncü erişilebilirlik durumu değildir.

### 2.2 Birlikte bulunamayacak durumlar

| Invariant | Zorunlu koşul |
|---|---|
| SM-01 | `F_i[K]=FORWARDABLE` ise `Succ_i[K]` tanımlıdır; successor ACTIVE, ilanı finite/geçerli/expire olmamış ve safe-successor koşuluna uygundur. `P_i[K]` sonludur. |
| SM-02 | `F_i[K]=REPAIRING` veya `UNREACHABLE` ise `Succ_i[K]=⊥` ve yeni DATA forwarding yasaktır. REPAIRING'de `P_i[K]=∞` ve aynı DFSN'de `FD_i[K]` artırılmaz/sıfırlanmaz. |
| SM-03 | `Π_i[K]=PROTECT` saklanıyor olsa bile yalnız `F_i[K]=FORWARDABLE` ve en az iki farklı immediate safe successor varken etkili olabilir. Bu koşul kaybolunca yeni redundancy derhal durur. |
| SM-04 | `A_i[K]=REQUESTING` iken aynı `K` için en çok tek coalesced yerel request oturumu vardır. Her yeni request dalgası yeni Request-ID taşır; aynı Request-ID yeniden iletilmez. |
| SM-05 | `B_i[Data-ID]` HELD/FORWARDED iken aynı Data-ID yeniden teslim, yeniden buffer veya yeniden replication üretmez. Duplicate cache süresi dolmadan state ABSENT'e dönmez. |
| SM-06 | Yeni OIID kabul edilince aynı Destination-ID'nin emekli `K` alanları, hiçbir yeni field/policy/buffer kararında forwarding bağlamı olamaz. |

## 3. Ortak atomik olay sırası

Bir node, bir paket, timer veya local link event'ini aşağıdaki sırayla işler. Aynı event birden çok state eksenini etkilerse ara durum dışarıdan gözlenebilir veya forwarding'e kullanılabilir değildir.

1. **Biçim ve güvenlik kapısı:** Version, type, length, reserved alanlar, Hop Limit, critical TLV, Security Profile 1 AUTH biçimi, roster/Key-ID bağı, HopSignature; packet türüne göre Origin/Source proof ve R1 control anti-replay doğrulanır. Başarısızsa state değişmez.
2. **Origin/field freshness kapısı:** OIID emekliliği, DFSN/ADS serial sırası ve half-space ambiguity işlenir. Yeni OIID eski instance'ları atomik emekliye ayırır; ambiguity mevcut field'i fail-closed yapar.
3. **Komşu kanıtı:** Geçerli unicast/ACK/PROBE_REPLY veya sert hata, önce `N_i[j]`yi günceller. ACTIVE olmayan komşuya dayalı tüm successor adayları aynı atomik işlemde askıya alınır.
4. **İlan/candidate güncellemesi:** Yalnız geçerli, güncel ve ACTIVE komşudan gelen `A_j[K]` cache'e yazılır. Withdrawal finite candidate değildir. Safe candidate kümesi yeniden hesaplanır.
5. **Field erişilebilirliği:** Safe candidate varsa deterministic successor seçilir; yoksa mevcut successor kaldırılır, gerekli withdrawal/repair işlemi başlatılır veya UNREACHABLE korunur.
6. **Policy ve paket işlemi:** Field safety sonucu kesinleştikten sonra `Π_i[K]` evidence timerları ve gerekiyorsa Data-ID/buffer/redundancy işlemi değerlendirilir. Policy hiçbir önceki kapıyı geri açamaz.
7. **Kontrol gönderimi:** Triggered FIELD_UPDATE, withdrawal, probe, solicit veya request yalnız bu yeni atomik state'e göre, coalescing/rate/budget sınırlarıyla planlanır.

Birden çok timer aynı anda dolarsa öncelik: güvenlik reddi/komşu invalidation → withdrawal → candidate yeniden hesabı → field expiry/repair → buffer sonlandırma → policy evidence. Bu, dengeli profilin timer önceliğiyle uyumludur.

## 4. Komşu yaşam makinesi

### 4.1 Durum anlamları

| Durum | İzin verilen kullanım |
|---|---|
| UNQUALIFIED | Ham/doğrudan kanıt kaydı vardır ancak node `i`nin `j`ye yönelik forwarding-grade iki-yönlü kanıtı yoktur. Data successor olamaz. |
| ACTIVE | Güncel forwarding-grade iki-yönlü kanıt vardır. Tek başına route yeterliliği sağlamaz; yalnız safe-candidate değerlendirmesine girebilir. |
| STALE | Son iki-yönlü kanıtın tazeliği bitmiştir. Data successor olamaz; doğrulama yapılabilir. |
| SUSPECT | Sert hata, çelişki veya failure-bound doğrulama gereği vardır. Data successor olamaz. |
| EXPIRED | Kayıt ve ona ait forwarding adayları geçersizdir. Yeni doğrudan kanıtla ancak UNQUALIFIED olarak yeniden başlar. |

### 4.2 Geçiş sözleşmesi

| Mevcut | Olay / guard | Atomik işlem | Sonraki |
|---|---|---|---|
| Kayıt yok / EXPIRED | Rosterla doğrulanmış direct-peer adayı veya bu node'a hedefli authenticated PROBE | Yeni `N_i[j]` ve retention kaydı aç; eski ilanı canlandırma; authenticated Sender-Instance görülürse R1 high-water'ı ilk değerle kur; `T_probe_start` içinde outbound qualification PROBE planla | UNQUALIFIED |
| UNQUALIFIED | `i → j` yönünü doğrulayan güncel ACK veya `i`nin başlattığı eşleşen PROBE_REPLY | Forwarding-grade kanıtı ve `T_fresh`/`T_retention`ı başlat | ACTIVE |
| UNQUALIFIED | Qualification oturumu `N_probe` tüketerek sonlanır veya `T_retention` dolar | İlan/candidate/R1 state'ini geçersizleştir | EXPIRED |
| ACTIVE | Geçerli forwarding-grade kanıt | `T_fresh`, `T_retention` ve gerekiyorsa `T_idle_probe`ı yenile | ACTIVE |
| ACTIVE | `T_idle_probe` doldu, yeni kanıt yok | Tek normal idle PROBE planla; state'i değiştirme | ACTIVE |
| ACTIVE | `T_fresh` dolar | Tüm field'lerde bu komşuyu candidate/successor olarak askıya al | STALE |
| ACTIVE | Doğrulanmış sert link hatası veya authenticated, yerel-linke bağlanmış kimlik çelişkisi | Candidate'leri askıya al; gerekliyse probe oturumu başlat veya derhal geçersizleştir | SUSPECT veya EXPIRED |
| STALE | Yeni forwarding-grade kanıt | Tazelik timerlarını başlat; field candidate'lerini yeniden değerlendirmeye aç | ACTIVE |
| STALE | Field için komşu gerekli veya ek negatif kanıt | `T_probe_start` içinde failure-bound PROBE oturumu aç | SUSPECT |
| STALE | `T_retention` dolar | İlan cache'ini successor kullanımından çıkar | EXPIRED |
| SUSPECT | Eşleşen, geçerli PROBE_REPLY veya yeni forwarding-grade ACK | Başarısızlık oturumunu kapat; timerları yenile | ACTIVE |
| SUSPECT | `N_probe` tüketilir, `T_probe_session` biter veya `T_retention` dolar | İlan/candidate state'ini geçersizleştir | EXPIRED |

Sadece `j`den gelen bir PROBE, `i`nin `j`ye veri gönderebildiğini kanıtlamaz. `i` PROBE_REPLY gönderir, niteliksiz kayıt yoksa açar ve ayrıca kendi outbound qualification PROBE'unu başlatır; fakat yalnız eşleşen kendi PROBE_REPLY veya uygun outbound ACK onu ACTIVE yapabilir. Böylece doğrudan peer discovery ile forwarding-grade kanıt ayrılır.

## 5. Field erişilebilirlik makinesi

### 5.1 Field kaydı oluşturma ve bağlam değişimi

Bir field record yalnız valid `K=(Destination-ID,OIID)` görüldüğünde oluşur. Destination için OIID bilinmiyorsa acquisition controller `A_i[d]` kullanılır; bilinmeyen `K` uydurulmaz.

| Olay | Zorunlu işlem |
|---|---|
| Yeni valid OIID | Aynı Destination-ID'nin eski `K` kayıtlarını ve successorlarını atomik emekliye ayır; yeni `K` için cache/FD bağlamını sıfırdan kur. |
| Aynı `K` için daha yeni DFSN | Eski successor'ı atomik devre dışı bırak; yeni DFSN'de feasibility sınırını yeni güvenli kurulumla yeniden başlat. |
| Aynı `K` için eşit DFSN ve daha yeni ADS | Sadece sender'ın yeni ilanını işle; feasibility ve expiry tekrar değerlendirilir. |
| Daha eski ADS/DFSN veya emekli OIID | State'i değiştirme; gerekirse diagnostic sayacını güncelle. |
| Tanımsız DFSN kıyası | Mevcut field'i forwarding'e kapat, successor'u kaldır ve freshness-ambiguity nedeni ile bounded acquisition/repair başlat. |

Yeni DFSN bağlamında henüz `FD_i[K]` yoksa, ilk ACTIVE/valid/finite ilan güvenli successor kurulumu için başlangıç referansı olabilir. Bundan sonra aynı DFSN'de yalnız onaylı feasibility koşulu kullanılır; `FD_i[K]` artırılmaz veya resetlenmez.

### 5.2 Erişilebilirlik geçişleri

| Mevcut | Olay / guard | Atomik işlem | Sonraki |
|---|---|---|---|
| Kayıt yok | Valid yeni `K` + ACTIVE komşudan başlangıçta kurulabilir safe candidate | `Succ`, `P`, `FD`yi kur; finite FIELD_UPDATE planla | FORWARDABLE |
| Kayıt yok | Valid yeni `K` var ama safe candidate yok | `Succ=⊥`, `P=∞`; tek bounded acquisition/repair oturumu başlat | REPAIRING |
| FORWARDABLE | Yeni daha iyi safe candidate veya mevcut successor değişimi | Deterministic seçimle successor/P güncelle; gerekirse ADS artırıp triggered update planla | FORWARDABLE |
| FORWARDABLE | Mevcut successor/ilan invalid; başka safe candidate var | Eski successor'u önce kaldır, sonra yeni safe successor'u atomik seç | FORWARDABLE |
| FORWARDABLE | Successor invalid ve safe candidate yok | `Succ=⊥`, `P=∞`, same-DFSN `FD`yi koru; withdrawal planla; `A_i[K]`yi başlat | REPAIRING |
| FORWARDABLE | Alan ilanı expiry guard'a girer | Successor hâlâ geçerliyse `A_i[K]=SOLICITING` başlat; forwarding devam eder | FORWARDABLE |
| REPAIRING | ACTIVE komşudan güncel, valid ve safe candidate | Pending solicit/request'i iptal et; successor/P/FD'yi uygun bağlamda kur; finite update planla | FORWARDABLE |
| REPAIRING | `T_repair_max` dolar ve safe candidate yok | Pending control işlemini kapat; field-local erişilemezliği kaydet | UNREACHABLE |
| UNREACHABLE | Yeni valid OIID veya tanımlı daha yeni DFSN ile safe candidate | Yeni bağlamı kur; successor seç; finite update planla | FORWARDABLE |
| UNREACHABLE | Yeni valid context gelir ama safe candidate yok; bir re-entry trigger'ı izinli | Yeni bounded repair oturumu başlat | REPAIRING |
| UNREACHABLE | Eski/ambiguous/unsafe ilan veya yalnız yeni DATA | Field state değişmez; packet işlemi local failure politikasına gider | UNREACHABLE |

REPAIRING'e girişte withdrawal, yalnız önce field FORWARDABLE iken finite lokal ilan mevcutsa üretilir. Aynı failure episode'unda tekrar tekrar withdrawal üretilmez; coalescing/ADS kuralı son state'i temsil eder.

### 5.3 UNREACHABLE sonrası yeniden giriş — seçilmiş karar

Kontrol fırtınasını önlemek için ilk sürüm şu kuralı kullanır: `UNREACHABLE` durumundaki her yeni DATA paketi otomatik yeni FIELD_SOLICIT veya DFSN_REQUEST başlatmaz. Yeni repair yalnız aşağıdakilerden biriyle başlar:

1. Yeni valid OIID/DFSN bağlamından usable field kanıtı gelir.
2. Daha önce hiç field olmayan Destination-ID için ilk acquisition tetiklenir.
3. Uygulama/operatör, ayrı ve açık bir `Acquire(Destination-ID)` yerel isteği üretir; mevcut `T_req_session`, `N_req` ve per-field bütçeler yine uygulanır.

Bu, data arrival ile sınırsız control amplification'ı engeller; bedeli, uygulamanın gerçekten yeni deneme istiyorsa bunu açıkça istemesidir. Proje sahibi bu MAJOR davranışı ilk sürüm için onaylamıştır.

## 6. Acquisition ve request makinesi

### 6.1 Durumlar

| Durum | Anlam |
|---|---|
| QUIESCENT | Bu destination/field için işlemde solicit veya DFSN request yoktur. |
| SOLICITING | Bir-atlama komşulardan mevcut field bilgisi istenmektedir. Bu, FORWARDABLE expiry guard sırasında veya REPAIRING/ilk acquisition sırasında bulunabilir. |
| REQUESTING | Coalesced DFSN_REQUEST oturumu vardır. Bu, yalnız REPAIRING veya OIID bilinmeyen ilk acquisition bağlamında bulunabilir; FORWARDABLE field için normal yol değildir. |

### 6.2 Geçişler

| Mevcut | Olay / guard | İşlem | Sonraki |
|---|---|---|---|
| QUIESCENT | İlk acquisition, field guard veya repair trigger | En çok `N_solicit=2` FIELD_SOLICIT denemesi planla | SOLICITING |
| SOLICITING | Valid safe FIELD_UPDATE ile field FORWARDABLE olur | Bekleyen solicit'leri iptal et | QUIESCENT |
| SOLICITING | İki deneme/yanıt penceresi biter ve yeni field gerekliyse | Request reason'ı kaydet; ilk Request-ID ile bounded session başlat | REQUESTING |
| REQUESTING | Valid safe new OIID/DFSN veya safe FIELD_UPDATE gelir | Field transition'ı uygula, oturumu iptal et | QUIESCENT |
| REQUESTING | İlk dalga sonuçsuz, `T_req_retry` dolmuş ve `N_req` bütçesi kalmış | Yeni Request-ID üret; ikinci request dalgasını planla | REQUESTING |
| REQUESTING | `T_req_session` veya `T_repair_max` biter | Yeni request üretme; field UNREACHABLE ise local failure politikasını kullan | QUIESCENT |

Her ara node, bir Request-ID'yi `T_req_duplicate=4 s` boyunca en fazla bir kez işler/iletir. Forwarder'ın Control Sender Block'u değişebilir, Request-ID değişmez. Requester'ın gerçek yeniden denemesi yeni Request-ID taşır. Hop Limit `H_req=16`, yalnız uzamsal sınırdır; request için wire lifetime yoktur.

## 7. Policy postür makinesi

Policy state `Π_i[K]`, field erişilebilirliğiyle aynı şey değildir. Fakat `F_i[K]≠FORWARDABLE` iken policy'nin forwarding, replication veya pre-failure eylemleri **etkisiz**dir.

| Mevcut | Olay / guard | İşlem | Sonraki |
|---|---|---|---|
| STEADY | M0.1 `CautionEvidence` (`H≥64 ∨ U≥128`) `T_caution_evidence=1.5 s` boyunca sürekli | Gözlem/probe yoğunluğunu artır, safe alternate izle | CAUTION |
| CAUTION | M0.1 `ProtectEvidence` (`H≥128`) `T_protect_evidence=2.5 s` boyunca sürekli **ve** ek safe successor **ve** traffic policy izni | Yalnız eligible data için bounded redundancy'ye izin ver | PROTECT |
| CAUTION | M0.1 `RecoveryEvidence` (`H<64 ∧ U<128`) `T_recovery_evidence=4.0 s` boyunca yeterli | Normal gözlem yoğunluğuna dön | STEADY |
| PROTECT | Ek safe successor kaybı veya forwarding eligibility kaybı | Yeni replication'ı hemen durdur; successor yoksa field repair transition'ını uygula | CAUTION veya etkisiz policy |
| PROTECT | Bozunma azalır ve `T_protect_min=2.0 s` sonrasında `T_recovery_evidence` tamamlanır | Yeni replication'ı durdur, artırılmış gözlemi sürdür | CAUTION |
| CAUTION/PROTECT | `F_i[K]` REPAIRING/UNREACHABLE olur | Evidence timerlarını sıfırla; policy değeri saklansa bile effective action yoktur | Etkisiz policy |
| Etkisiz policy | Field yeniden FORWARDABLE olur | Eski PROTECT'i diriltme; evidence'ı yeni kanıtla yeniden başlat | STEADY |

`PROTECT → STEADY` doğrudan geçişi yoktur. `T_protect_min`, safety gate kaybını geciktiremez. High uncertainty tek başına PROTECT ya da replication izni vermez.

## 8. Data-ID, buffer ve redundancy yaşamı

### 8.1 Paket kaydı

| Mevcut | Olay / guard | İşlem | Sonraki |
|---|---|---|---|
| ABSENT | Geçerli, daha önce görülmemiş DATA | Data-ID için atomik cache kaydı rezerve et | HELD veya FORWARDED |
| HELD | Field FORWARDABLE olmadan `T_buffer[class]` veya quota dolması | Paketi bırak, local delivery-failure olayı üret | DROPPED |
| HELD | Field FORWARDABLE olur ve paket hâlâ yaş geçerli | Güncel safe successor ile forwarding yap | FORWARDED |
| FORWARDED | Aynı Data-ID gelir | Yeniden teslim/forward/replication yapma | FORWARDED |
| DROPPED | Aynı Data-ID gelir | Yeni işlem yapma; diagnostic sayaç güncellenebilir | DROPPED |
| HELD/FORWARDED/DROPPED | `T_data_duplicate` dolar | Cache kaydını sil | ABSENT |

İlk DATA olayında field FORWARDABLE ise packet HELD olmadan FORWARDED olur. Field REPAIRING ise yalnız buffer quota, traffic policy ve `T_buffer[class]` uygunsa HELD olur. Field UNREACHABLE ise yeni DATA buffer'a kabul edilmez; local delivery-failure davranışı uygulanır. `Data-ID` cache kaydı forwarding/buffer kararından önce alınır; bu, aynı paketin eşzamanlı kopyalarının iki kez queue'ya girmesini engeller.

### 8.2 Koşullu redundancy

Bir FORWARDED packet için ek kopyalar ancak aşağıdakilerin tümü doğruysa oluşturulur:

1. `Π_i[K]=PROTECT` efektif durumdadır.
2. DATA `Protection-Eligible` bayrağını ve pozitif Replication Budget'ı taşır.
3. Primary dışında farklı immediate komşuya sahip en az bir safe successor vardır.
4. Yerel control/data kaynak bütçesi izin verir.
5. Toplam immediate forward sayısı `MaxReplicaFanout=2`yi aşmaz. Primary dışında üretilebilecek ek kopya sayısı `min(Replication-Budget, MaxReplicaFanout - 1)`dir; dolayısıyla ilk sürümde en çok birdir.

Kopyalar aynı değişmez Data-ID'yi taşır; yalnız kullanılacak budget azaltılabilir. Data-ID cache, aynı kopyanın tekrar gelişinde yeniden fanout'u engeller. İlk-sürüm ingress profili `RB∈{0,1}` olduğundan redundant forwarding sonrasındaki iki çıkışta RB `0` kalır; daha önce görmemiş downstream node da yeniden çoğaltamaz. PROTECT veya safe alternate sonradan kaybolursa in-flight kopyalar geri çağrılmaz fakat yeni kopya üretilmez.

## 9. Tüm durum makineleri için hata davranışı

| Olay | Zorunlu davranış |
|---|---|
| Malformed/unsupported/unknown critical paket | Sessizce bırak; field/neighbor/buffer state değiştirme. |
| Authentication gerekli fakat doğrulanamaz | Sessizce bırak; security diagnostic sayacı artırılabilir; forwarding kanıtı oluşmaz veya mevcut ACTIVE komşu tek paketle düşmez. |
| Duplicate control/data | İdempotent veya drop; eski state geri sarılamaz. |
| ADS/DFSN half-space ambiguity | Fail-closed; ilgili field forwarding'e kapalı, bounded acquisition/repair tetiklenir. |
| Timer yarışması | §3 önceliğini uygula; policy timerı safety sonucu üzerinde işlem yapamaz. |
| Yerel bellek/bütçe dolması | Yeni buffer/replica kabul etme; mevcut safe forwarding'i veya loop invariantını gevşetme. |

## 10. Gereksinim izlenebilirliği

| Unsur | Gereksinimler |
|---|---|
| Komşu state ve ACTIVE forwarding kapısı | FR-01, FR-07, FR-11, FR-13 |
| Field state + safe successor/FD transition | FR-06, FR-09, FR-10, FR-13 |
| Bounded solicit/request/UNREACHABLE | FR-03, FR-06, FR-10, FR-13, NFR-01 |
| Policy safety preemption | FR-02, FR-04, FR-08, FR-12 |
| Data-ID/buffer/redundancy lifecycle | FR-06, FR-12, FR-13, NFR-01–NFR-03 |
| Fail-closed parsing/freshness | FR-09, FR-10, FR-14, NFR-06 |

## 11. Onaylanmış durum makinesi kararı

Önerilen state-machine mimarisi:

1. Komşu, field, policy, request ve packet kayıtları ayrı state eksenleridir; yalnız §3'teki atomik event sırası ile etkileşir.
2. Safety transition'ları policy dwell ve buffer/redundancy davranışından önceliklidir.
3. Policy, FORWARDABLE olmayan field'i tekrar forwarding'e açamaz; recovery sonrası eski PROTECT postürü yeniden dirilmez.
4. `UNREACHABLE`da yeni DATA otomatik control re-entry başlatmaz; re-entry yeni valid field kanıtı, ilk acquisition veya explicit `Acquire(Destination-ID)` ile sınırlıdır.
5. İlk sürüm birincil olarak tek-sink profildir; wire ve field anahtarları çok-hedefe genellenebilir kalır. `MaxReplicaFanout=2`dir (primary + en çok bir alternate); traffic class `1…255` buffer profilleri ise açık parametredir.

**Kazanç:** Uygulama, timer yarışlarında dahi forwarding safety kapılarının hangi sırayla uygulandığını bilir; replication/buffer davranışı route uygunluğundan ayrılır; request flood'unu data arrival tetiklemez.

**Bedel:** Birden fazla küçük state kaydı ve explicit upper-layer reacquire işlemi gerekir; tek-sink başlangıç profilinde çok-hedef kaynak kontrolü bu sürümün kapsamı dışındadır; geniş fanout bilinçli olarak dışlanmıştır.

Bu, tüm uygulama algoritmalarının davranışını belirleyen ve proje sahibi tarafından ilk sürüm için onaylanan MAJOR karardır.
