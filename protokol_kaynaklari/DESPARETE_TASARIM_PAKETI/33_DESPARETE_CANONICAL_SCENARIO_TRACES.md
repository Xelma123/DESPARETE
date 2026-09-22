# DESPARETE — Kanonik Senaryo İzleri

**Sürüm:** 0.1 (tasarım-seviyesi düşünce deneyi; test sonucu değildir)  
**Durum:** `00_MASTER_PROMPT.md` §39'daki 17 kanonik vakayı, onaylı v0.1 state/algorithm/security kurallarıyla izler. Simülasyon, uçuş testi veya performans iddiası içermez.  
**Tarih:** 2026-09-21

## 1. Amaç, notasyon ve ortak önkoşullar

Her vakada `i`, DATA'yı yapılandırılmış `SinkID`ye ileten node; `j`, mevcut primary successor; `K=(SinkID,OIID)` field anahtarıdır. Aksi söylenmedikçe paketler wire ve Security Profile 1 kapılarından geçmiştir.

Ortak kurallar:

1. DATA yalnız `F_i[K]=FORWARDABLE`, `Succ_i[K]` ACTIVE, ilan fresh ve candidate feasible ise iletilir.
2. Hop Limit/TTL zarar sınırıdır; safety, target DFSN + FD + safe-successor invariantına dayanır.
3. R, `g(H,U)`dir; Q ile karıştırılmaz; policy safety kapısını açamaz.
4. Invalid/malformed/bad-signature trafik, local telemetry sayaçlarını artırabilir ancak tek başına ACTIVE neighbor veya field state'ini değiştirmez.
5. Profile 1 kalıcı receiver-restart replay koruması (R2) ya da payload gizliliği iddia etmez.

## 2. Senaryo izleri

| Vaka | Girdi / olay | Zorunlu yerel iz | Yasak veya verilmemiş sonuç | Başlıca kaynak |
|---|---|---|---|---|
| 1. Kararlı ağ | `j` ACTIVE; ilan fresh/finite/feasible; yeni doğrudan kanıt timerları yeniler. | `RecomputeField` `j`yi successor tutar. Yeni DATA duplicate-cache'e rezerve edilir, Hop Limit azalır, HopSignature yenilenir ve tek primary'ye iletilir. | Sırf kararlı diye kontrol, replication veya yeni DFSN üretilemez. | `20`…`24`, `26` |
| 2. Bir bağın kademeli bozulması | Ardışık O-DEL/O-TREND kötüleşir; H yükselir, kanıt tutarlıysa U düşebilir. | Policy evidence/dwell sonrası STEADY → CAUTION; güvenli alternatif gözlenir. Ancak `j` hâlâ ACTIVE/feasible ise forwarding yalnız bu gerekçeyle kesilmez. | Tek örnek kayıp, jammer hükmü, DFSN artışı veya unsafe alternate seçimi değildir. | `11`, `15`, `21`, `23` |
| 3. Bağın aniden kaybolması | Yerel hard link failure veya doğrulanmış local-link identity contradiction. | `j`: ACTIVE → SUSPECT/EXPIRED; candidate'ler çıkarılır. Safe alternate varsa atomik successor seçilir. Yoksa withdrawal, REPAIRING ve bounded acquisition/DFSN_REQUEST başlar. | Eski successor, STALE/SUSPECT node veya feasible olmayan detour data için kullanılamaz. | `10`, `16`, `22`, `23`, `28` |
| 4. İki yarışan next hop | `j1` ve `j2` ACTIVE, fresh ve feasible candidate'tir. | En düşük sonlu `Cost(a,j)` seçilir; eşitlikte küçük unsigned `(NodeID, InstanceID)` kazanır. | Sadece daha düşük advertised potential, safety/feasibility yerine geçmez. | `12`, `13`, `23` |
| 5. Bayat bilgi | Eski/eşit ADS, expired ilan veya serial comparison `AMBIGUOUS`. | Eski/eşit ADS ilan yaşamını uzatmaz. Expired ilan candidate'den çıkarılır. Ambiguous DFSN/current context fail-closed ve REPAIRING işlemine gider. | Bayat mesaj yeni field, düşük potential veya ACTIVE kanıtı yaratamaz. | `14`, `19`, `20`, `23` |
| 6. Yüksek göreli hız | Yerel O-MOB veya komşu kararsızlığı gözlemi oluşur. | M0.1'de O-MOB yalnız tanısal kayıttır; tek başına Q/H/U/R veya policy değişmez. Teslim sonucu/yaşı değişirse M0.1 ve safety kuralları vaka 2/3'teki gibi uygulanır. | GPS/mobilite kaybı kesin kopma, daha iyi kalite veya tek başına policy girdisi değildir. | `11`, `15`, `20`, `35` |
| 7. Girişim | Yerel O-RADIO gözlemi değişir; O-DEL ile uyumlu veya çelişkili olabilir. | M0.1'de O-RADIO ve çelişki yalnız telemetry bağlamıdır; Q/H/U/R yalnız tanımlı teslim, yaş ve örnek kurallarıyla değişir. Safety/forwarding etkisi ancak bu kanonik girdilerden doğarsa değerlendirilir. | Tek başına radyo ölçümü jamming teşhisi, neighbor expiry, U artışı veya global alarm değildir. | `11`, `15`, `28`, `35` |
| 8. Jamming kaynaklı görünen bozunma | Teslim, radyo veya kanal örüntüsü birlikte kötüleşir. | Jamming evidence tanısal olarak kayda geçer; M0.1 tepkisi yalnız teslim/yaş örnekleri üzerinden vaka 2 veya 3'teki gözlemsel davranışı uygular. Bad-signature/control injection ayrı olarak accept gate'te bırakılır. | `JAMMER=true`, saldırgan kimliği veya jamming'e özgü garanti çıkarılamaz. | `11`, `25`, `26`, `28`, `35` |
| 9. Çoklu alternatif yol | Primary yanında bir veya daha fazla safe alternate vardır; DATA protection-eligible ve ingress RB=1'dir. | PROTECT ve local budget koşulları geçerse `i`, primary + deterministik tek alternate üretir. İki kopyada RB=0, HopSignature yenidir; Data-ID downstream duplicate'i bastırır. | Sürekli ECMP, iki alternatiften fazlası, downstream yeniden çoğaltma veya end-to-end disjointness iddiası yoktur. | `17`, `19`, `22`, `23`, `27` |
| 10. Uygun/feasible komşu yok | Current `K` için candidate kümesi boştur. | `P_i[K]=∞`, `Succ_i[K]=⊥`; previously forwardable ise withdrawal ve REPAIRING. İlk acquisition veya explicit reacquire bounded control başlatabilir. | Yeni DATA tek başına UNREACHABLE field'i yeniden başlatmaz; geri yön veya eski route ile forwarding yapılmaz. | `13`, `16`, `22`, `23` |
| 11. Ağ bölünmesi | FIELD_SOLICIT/DFSN_REQUEST target'a ulaşmaz; valid safe successor gelmez. | `T_req_session`/`T_repair_max` sonunda field UNREACHABLE olur. REPAIRING durumundaki yalnız quota/lifetime içindeki DATA tutulur; sonra local delivery failure üretilir. | Ağ-geneli partition duyurusu, DTN, sınırsız buffer veya zorunlu reverse ERROR yoktur. | `16`, `20`, `21`, `23`, `28` |
| 12. Partition healing | Yeni valid OIID/DFSN veya current context için valid FIELD_UPDATE ACTIVE peer'dan gelir. | Freshness/origin/ADS kapıları geçer; safe candidate oluşursa FORWARDABLE kurulur. Ömrü dolmamış HELD DATA forward edilir. | Eski retired OIID, stale ADS veya DATA'nın kendisi field'i canlandıramaz. | `14`, `20`, `22`, `23` |
| 13. Eşzamanlı maliyet değişimi | Birden çok ACTIVE komşunun `C(i,j)` veya advertised potential'i değişir. | Her node aynı DFSN'de yalnız feasible candidate seçer; FD yükselmez/sıfırlanmaz. Alternatif yoksa repair yolu seçilir. | Ara node maliyet artışına karşı DFSN/OIID üretemez veya count-to-infinity forwarding'i başlatamaz. | `12`, `13`, `23`, `24` |
| 14. Eşzamanlı field update | Aynı `K` için farklı relay ilanları, ADS değerleri veya daha yeni DFSN gelir. | Target OriginSignature doğrulanır; relay-local ADS yalnız kendi ilanını sıralar. Yeni OIID eski destination fields'i retire eder. Current DFSN kıyası ambiguous ise fail-closed. | Relay, kendi ADS/potential değişimiyle target yetkisi veya yeni DFSN kazanmaz. | `14`, `18`, `19`, `23`, `26` |
| 15. Node restart | Target restartı veya peer sender-instance değişimi. | Target restartı yeni OIID ve target proof üretir; alıcı eski field'leri retire eder. Peer yeni instance'ı imzalı qualification PROBE/REPLY ile R1 high-water'a girer; yalnız outbound kanıt ACTIVE yapar. | Eski OIID/AR state canlandırılamaz. Receiver restartından sonra persistent replay reddi iddia edilmez; R2 gerekir. | `14`, `20`, `22`, `23`, `26` |
| 16. Duplicate control mesajı | Aynı/older/ambiguous R1 Message Sequence veya aynı Request-ID tekrar gelir. | R1 `EQUAL`/`OLDER`/`AMBIGUOUS` control'u state değiştirmeden bırakır. Request-ID de `T_req_duplicate` boyunca en fazla bir kez işlenir/iletilir. | Duplicate, timer/ADS/field tazelemez; yeni request wave veya ACTIVE kanıtı olmaz. | `19`, `20`, `23`, `26` |
| 17. Yanlış/bayat risk bilgisi | Komşudan bir risk/jamming iddiası veya yerel olarak bayat/çelişkili ölçüm gelir. | MODE_NOTICE çekirdekte yoktur; komşunun iddiası `i`nin link riski değildir. M0.1'de çelişki tanısal telemetrydir; U yalnız yaş/örnek tablosuyla değişir. Valid local M0.1 evidence yoksa safety/field değişmez. Compromised relay'in kendi signed potential beyanı route tercih kalitesini etkileyebilir, ama target authorization/FD safety'i bypass edemez. | Uzaktan risk beyanı, jamming hükmü, STALE peer'i geçerli yapma veya loop-safety istisnası değildir. | `11`, `15`, `23`, `25`, `26`, `35` |

## 3. Senaryo denetimi sonucu

On yedi vakada da data forwarding, freshness, repair, policy, duplicate ve security davranışı mevcut normatif belgelere bağlanmıştır. Bu izler iki kalıcı sınırı görünür kılar:

- M0.1 (`35`) referans Q/H/U/R ve maliyet dönüşümünü tanımlar; platforma özgü kalibrasyon ve deployment kabulü yine `29`a bağlıdır.
- Bu belge masa-başı izdir; `29` kapasite kapısı ve gerçek implementation event trace'i olmadan deployment veya performans sonucu çıkarılamaz.

Bu nedenle senaryo düzeyinde açıklanamayan davranış bulunmamıştır; ancak G-07'nin runtime doğrulama bölümü ve kullanıcı diyagramlarının metin uyumu hâlâ açıktır.
