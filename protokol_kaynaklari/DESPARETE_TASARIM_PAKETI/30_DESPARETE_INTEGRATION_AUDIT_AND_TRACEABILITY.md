# DESPARETE — Entegrasyon Denetimi ve Gereksinim İzlenebilirliği

**Sürüm:** 0.1 (ilk entegre denetim; design-complete kararı değildir)  
**Durum:** Normatif tasarım belgeleri `08`…`35`, birleşik candidate assembly `36` ve uygulama-doğrulama hazırlık belgeleri `37`…`39` için masa-başı tutarlılık ve gereksinim kapsamı denetimi. Platform ölçümü, uçuş testi, simülasyon veya nihai prior-art taramasının yerine geçmez.  
**Tarih:** 2026-09-21

## 1. Amaç ve denetim sınırı

Bu denetim, `00_MASTER_PROMPT.md`nin nihai kontrol listesinin iki parçasını yürütür:

1. Her FR/NFR için en az bir somut mekanizma ve belge kanıtı var mı?
2. Belgeler arasında bir mekanizmanın anlamını değiştiren veya tanımsız bırakan açık çelişki var mı?

Denetim, algoritmanın gerçek radyo/CPU'da çalıştığını, timer değerlerinin optimum olduğunu veya bir yenilik iddiasını kanıtlamaz. Bu tür iddialar yalnız `29`daki kapasite girdileri, sonraki uygulama doğrulaması ve final prior-art re-audit ile ele alınabilir.

## 2. Kullanılan normatif temel

| Katman | Belgeler | Denetimdeki rol |
|---|---|---|
| Yönetim ve gereksinim | `00`, `05`, `06`, `07` | Yetki, karar, kabul kapısı ve açık soru kaynağı. |
| Anlam/mekanizma | `08`…`18` | Gözlem, risk, maliyet, safety, recovery ve kontrol semantiği. |
| Uygulama sözleşmesi | `19`…`23` | Wire, timer, state machine ve handler davranışı. |
| Güvence ve sınırlar | `24`…`29`, `35` | Correctness, security, kaynak, hata/telemetri, deployment kapısı ve M0.1 metrik profili. |
| Birleşik candidate okuma | `36` | v0.1 davranışının tek okuma akışı; kanonik ayrıntıları değiştirmez. |
| Uyum kanıtı hazırlığı | `37`…`39` | Test oracle'ları, event-trace semantiği ve candidate-freeze kapıları; henüz runtime sonucu değildir. |

Bir belge içinde eski v0 taslağını anlatan tarihsel metin ile `05`te kayıtlı onaylı karar çelişirse, `05` ve onaylı v0.1 belgeleri üstündür. Taslak metin yeni normatif davranış yaratmaz.

## 3. Gereksinim–mekanizma matrisi

`Kapsandı`, tasarım davranışının tanımlı olduğu anlamına gelir; “ölçülmüş” veya “deployment kabul edildi” anlamına gelmez.

| Gereksinim | Başlıca mekanizma ve belge | Kapsam | Kalan kabul/evidence sınırı |
|---|---|---|---|
| FR-01 | Forwarding-grade komşu yaşamı, local aging ve `ACTIVE` kapısı: `10`, `20`…`23` | Kapsandı | Seçili radyo için `D_*`/timer davranışı ölçülmeli. |
| FR-02 | `Q/H/U/R` ayrımı, M0.1 tamsayı profil, field-local policy ve safety preemption: `11`, `12`, `15`, `23`, `35` | Kapsandı | M0.1 değerlerinin platform davranışı DC-11/uygulama trace ile doğrulanmalıdır. |
| FR-03 | FIELD_SOLICIT, bounded DFSN_REQUEST, acquisition state: `18`, `20`…`23` | Kapsandı | Gerçek request yükü DC-06/DC-08 ile kabul edilmelidir. |
| FR-04 | Q'nun R'den ayrılması, yönlü maliyet ve M0.1 kuantizasyonu: `11`, `12`, `35` | Kapsandı | Farklı radio feedback biçimi yeni metrik profile gerektirir. |
| FR-05 | Maliyet, policy, redundancy ve kaynak takas kayıtları: `12`, `15`, `17`, `27` | Kapsandı | Görev önceliklerine göre sayısal trade-off seçilmedi. |
| FR-06 | Withdrawal, REPAIRING/UNREACHABLE, bounded buffer ve local failure: `16`, `21`…`23`, `28` | Kapsandı | Class-0 dışı traffic-class buffer profilleri açık. |
| FR-07 | Belirsizlik, jamming-evidence sınırı ve fail-closed komşu davranışı: `11`, `15`, `20`, `28` | Kapsandı | Jamming tespiti iddiası yoktur. |
| FR-08 | STEADY/CAUTION/PROTECT, M0.1 evidence predicate'leri, dwell ve control budget: `15`, `20`, `21`, `35` | Kapsandı | Yoğunluk/misyon eşikleri platformda kalibre edilmemiştir. |
| FR-09 | Target DFSN, FD, safe successor, withdrawal ve safety argümanı: `13`, `14`, `22`…`24` | Kapsandı | Garanti, `24`teki doğru-node/freshness varsayımlarına koşulludur. |
| FR-10 | OIID, target-only DFSN, RFC-1982 fail-closed ve retired OIID: `14`, `19`, `20`, `23` | Kapsandı | Rollover/restart izleri uygulama testinde yürütülmelidir. |
| FR-11 | UNQUALIFIED/ACTIVE/STALE/SUSPECT/EXPIRED, bootstrap ve probe: `10`, `20`…`23`, `26` | Kapsandı | Direct-peer candidate üretimi DC-10 taşıyıcı sözleşmesine bağlıdır. |
| FR-12 | Safe alternate, PROTECT, eligibility, RB=0/1 ve fanout=2: `17`, `21`…`23`, `27` | Kapsandı | Sadece first-hop divergence iddiası vardır. |
| FR-13 | Ortak accept gate, TLV/serial hataları, local failure ve telemetry: `18`, `19`, `23`, `28` | Kapsandı | Management export taşıyıcısı seçilmemiştir. |
| FR-14 | Roster, hop/origin/source signature, R1 replay ve residual risk: `25`, `26`, `29` | Kapsandı | R2 persistent replay, key lifecycle ve confidentiality kapsam dışıdır. |
| NFR-01 | Hop/request/retry/buffer/redundancy sınırları: `16`…`18`, `20`…`23`, `27` | Kapsandı | Topolojiye göre airtime kabulü gerekir. |
| NFR-02 | Control/replication maliyet kaydı ve airtime kapısı: `17`, `21`, `27`, `29` | Kapsandı | Enerji ölçümü/mission budget yoktur. |
| NFR-03 | State, request, header, verify ve cache karmaşıklığı: `19`, `21`, `26`, `27`, `29` | Kapsandı | `n`, `d_max`, RAM ve CPU girdileri yoktur. |
| NFR-04 | Merkezi koordinatör olmadan local field/decision: `08`, `13`, `16`, `23` | Kapsandı | Tek-sink v0.1 operasyon sınırıdır; merkezileşme değildir. |
| NFR-05 | Q/H/U güncelleme nedeni, M0.1 test vektörleri ve local event/counter sözleşmesi: `11`, `28`, `35` | Kapsandı | Telemetry export ve retention profile bağlıdır. |
| NFR-06 | Wire/state/algorithm adlandırması, karar günlüğü, sözlük ve bu denetim: `05`, `19`…`23`, `30`, `31` | Kapsandı | Kanonik sözlük ve mekanik cross-reference taraması tamamlandı; RFC birleştirilince aynı tarama yeniden uygulanır. |

## 4. Çapraz-belge sözleşme denetimi

| Kimlik | Sözleşme | Sonuç |
|---|---|---|
| IA-01 | Data forwarding yalnız ACTIVE, fresh, finite ve feasible successor ile olur. | Geçer: `10`, `13`, `20`, `22`, `23`. |
| IA-02 | TTL/Hop Limit safety kanıtı değil; request/data kaynak sınırıdır. | Geçer: `13`, `20`, `23`, `24`. |
| IA-03 | OIID/DFSN target-only, ADS sender-local ve serial belirsizliği fail-closed'dur. | Geçer: `14`, `18`…`20`, `23`, `26`. |
| IA-04 | Q mevcut kalite; R yalnız `g(H,U)`; risk safety gate'i açmaz. | Geçer: `11`, `12`, `15`, `23`, `35`. M0.1 için `g=max(H,U)`, Q/H/U tamsayı dönüşümleri ve policy predicate'leri belirlenmiştir. |
| IA-05 | Link bootstrap, R1 anti-replay ve ACTIVE oluşumu birlikte uygulanabilir. | Geçer (2026-09-21 düzeltmesi): `10`, `20`…`23`, `26`. Authenticated direct-peer candidate yalnız UNQUALIFIED açar; yalnız local outbound kanıt ACTIVE yapar. |
| IA-06 | Komşu kaybı ara node'a DFSN/OIID üretme yetkisi vermez. | Geçer: `14`, `16`, `22`…`24`. |
| IA-07 | Redundancy, RB=1 girişinde en çok bir primary ve bir alternate üretir; downstream RB=0'dır. | Geçer: `17`, `19`, `22`, `23`, `27`. |
| IA-08 | Hata/invalid auth, kendiliğinden network ERROR veya ACTIVE-neighbor düşüşü üretmez. | Geçer: `23`, `26`, `28`. Authenticated local-link identity conflict istisnadır. |
| IA-09 | Security header/verification maliyeti deployment claiminden önce görünür ve kapılıdır. | Geçer: `19`, `26`, `27`, `29`. |
| IA-10 | Backtick'li sayısal belge referansları mevcut corpus'ta hedef dosyaya çözülür. | Geçer: `00`…`32` için mekanik tarama yapıldı. Tek dış değer olan `76`, `26`daki AUTH TLV octet uzunluğudur; belge referansı değildir. |
| IA-11 | `36` birleşik candidate, wire/security/metric ayrıntılarında kanonik `19`/`26`/`35`i geçersiz kılmaz. | Geçer: `36` yalnız normların özeti ve kaynak haritasıdır; packet layout, imza coverage ve M0.1 tablo/test vektörleri kaynak belgelere bağlı kalır. |
| IA-12 | M0.1 metric epoch; policy, algorithm, telemetry, resource ve deployment sözleşmeleriyle bağlıdır. | Geçer: `15`, `20`, `22`, `23`, `27`…`29`, `35`, `36`. `T_metric_epoch=0.5 s` paket üretmez; normal recompute/coalescing sınırını kullanır. |
| IA-13 | Conformance planı, trace sözleşmesi ve freeze listesi, dokümante edilmiş tasarım ile gerçek çalışma kanıtını birbirine karıştırmaz. | Geçer: `37` PASS için deterministic çıktı/event-trace ister; `38` negatif kanıtı tanımlar; `39` test çalıştırılmadığı sürece FZ-16…FZ-20'yi `BEKLİYOR` tutar. |
| IA-14 | İlk authenticated, hedefli PROBE R1 bootstrap'ta kabul edilir fakat peer'i ACTIVE yapmaz. | Geçer (2026-09-21 denetim düzeltmesi): `23` ilk R1 kaydını yalnız active-peer/targeted-PROBE/matching-REPLY bağlamında atomik kurar; `26` aynı sınırı taşır; CT-NEI-02 ve `38` `R1_INITIALIZED` kanıtını ister. |
| IA-15 | M0.1 dışındaki O-RADIO/O-MOB/O-CONFLICT semantiği, M0.1 routing/policy girdisi gibi okunmaz. | Geçer (2026-09-21 denetim düzeltmesi): `11` genel profil ile M0.1 sınırını ayırır; `33`ün 6, 7, 8 ve 17. vakaları yalnız teslim/yaş/örnek kurallarının routing etkisi olduğunu belirtir. |
| IA-16 | Malformed/AUTH/replay paketi ile gerçek successor invalidation ayrıdır. | Geçer (2026-09-21 denetim düzeltmesi): `20`/`21` biçim/auth/replay reddinin yalnız paketi düşürdüğünü; `23`/`26`/`28` mevcut ACTIVE peer veya successor'ın tek paketle kaldırılmayacağını birlikte belirtir. |
| IA-17 | ACTIVE olmayan peer'dan gelen target-authenticated FIELD_UPDATE, mevcut field tazeliğini veya OIID state'ini etkileyemez. | Geçer (2026-09-22 denetim düzeltmesi): `23`, ACTIVE kapısını OIID retirement'tan önce uygular; CT-FLD-05 ve `38` yalnız diagnostic kayıt ile `FIELD_RETIRED`/repair yokluğunu kanıtlar. |

## 5. Açık kapılar ve tamamlık etkileri

| Kimlik | Açık iş veya insan kararı | Etki | Kapanış koşulu |
|---|---|---|---|
| G-01 | Resmî gereksinim tabanının nihai proje-sahibi kabulü. | Tamamlandı: `06`, proje sahibi tarafından v0.1 baseline olarak kabul edildi (DL-041). | Baseline değişikliği yeni değişiklik kaydı ve izlenebilirlik güncellemesi gerektirir. |
| G-02 | Terim ve cross-reference denetimi. | Tamamlandı (ara denetim): `31` kanonik sözlük; IA-10 için `00`…`39` mekanik iki-haneli belge referans taraması; master envanterindeki iki eski dosya adı ile IA-14…IA-17 semantik uyumsuzlukları düzeltildi. | Diyagram eşlemesinden sonra FZ-13 kapsamında final RFC satır/section taraması tekrar çalıştırılır. |
| G-03 | Q/H/U/R ve maliyet dönüşümlerinin sayısal profile bağlanması. | Tamamlandı (tasarım düzeyi): DL-042 ile A/M1 seçildi; `35` M0.1 ortak admission, gözlem, tamsayı dönüşüm, policy predicate ve test vektörlerini tanımlar. | Platform kalibrasyonu/deployment M0.1'in tasarım tamamlığından ayrıdır; `29` DC-11 ve G-07 uygulanır. |
| G-04 | DC-01…DC-11 platform girdileri. | DL-041 ile `DESIGN-ONLY` kabul edildi; bu, v0.1 tasarım çalışmasını değil deployment kabulünü bekletir. | Deployment istenirse `29`daki kapasite kapısı geçer veya farklı profile seçilir. |
| G-05 | Prior-art re-audit. | Tamamlandı: `32` Kan, FANET gradient/potential, anti-jamming ve patent sinyallerini yeniden taradı; yenilik iddiasını yasakladı. | Yayın/ticarileşme öncesi claim-level FTO ve güncel tekrar tarama dış uzmanlık işidir. |
| G-06 | Kullanıcı tarafından hazırlanacak diyagramların metin/algoritmalarla eşleştirilmesi. | Master'ın diagram kriteri açıktır. | Her diyagramın davranışı `19`…`23` ile satır satır uyumlu denetlenir. |
| G-07 | Edge-case izleri ve uygulama doğrulaması. | Tasarım-seviyesi 17 kanonik iz `33`te tamamlandı; masa-başı safety argümanı yine gerçek çalışma kanıtı değildir. | Restart, stale/replay, repair, RB, capacity/admission senaryoları için implementation event trace/test çıktısı. |
| G-08 | Birleşik candidate specification. | Tamamlandı: `36`, modüler v0.1 normlarını üstünlük sırası ve açık sınırlarıyla tek okuma akışında birleştirir. | Candidate değişirse IA-11/IA-12 ve kaynak haritası yeniden denetlenir. |
| G-09 | Conformance vaka ve event-trace sözleşmesi. | Tamamlandı (dokümantasyon düzeyi): `37` test oracle'larını, `38` kanıt biçimini tanımlar. | Uygulama çıktılarıyla CT vakaları çalıştırılır; bu noktaya kadar hiçbir CT sonucu PASS değildir. |
| G-10 | Candidate-freeze hazırlık listesi. | Tamamlandı (dokümantasyon düzeyi): `39`, design, insan, implementation ve deployment kapılarını ayırır. | FZ-12…FZ-15 diyagram/denetim/sahip onayı; FZ-16…FZ-20 runtime kanıtı ile kapatılır. |

## 6. Denetim sonucu

2026-09-21/22 tarihli tam-corpus ara denetimi; R1 bootstrap kabul sırası, M0.1 telemetry sınırı, güvenlik reddi/state etkisi, ACTIVE olmayan peer'dan OIID kabul sırası, master envanterindeki eski dosya adları ve eski kavramsal referanslarda uyum boşlukları bulmuş; bunları yeni mimari kararı üretmeden mevcut onaylı semantiğe hizalamıştır. Bu düzeltmelerden sonra, bu denetimde bulunan açık bir safety veya bootstrap çelişkisi kalmamıştır. G-01, G-02, G-03, G-05, G-08, G-09 ve G-10 dokümantasyon düzeyinde tamamlandı; G-07'nin tasarım-seviyesi izleri de tamamlandı. Yazılı **candidate protocol draft** `36` ile, uygulama doğrulama sözleşmesi ise `37`…`39` ile mevcuttur. Ancak kullanıcı diyagramları ve G-07'nin implementation kanıtı kapanmadan DESPARETE **DESIGN COMPLETE** veya “nihai” olarak etiketlenemez; DC-01…DC-11 olmadan da deployment-ready değildir.

Bu nedenle sonraki uygun iş sırası: kullanıcı diyagram eşlemesi → final referans/terim/decision-log denetimi → proje sahibi candidate-freeze kararı → uygulama conformance trace'leri → deployment kapasite kanıtıdır. Son üç adımın hiçbiri bu belgelerin hazırlanmış olmasıyla kendiliğinden geçmiş sayılmaz.
