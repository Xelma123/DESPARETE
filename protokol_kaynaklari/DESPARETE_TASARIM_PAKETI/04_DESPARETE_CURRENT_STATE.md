# DESPARETE — Güncel Proje Durumu

**Durum tarihi:** 2026-09-21  
**Tasarım sürümü:** v0.1 entegre aday  
**Durum:** Çekirdek semantik onaylı, test/trace hazırlığı belgelenmiş ve entegre denetim altında; tasarım tamamlanmış, deployment-ready veya mimari dondurulmuş değildir.

## 1. İncelenen kaynaklar ve kapsam

Bu durum özeti, yönetim belgeleriyle birlikte `06`…`31`deki v0.1 tasarım corpus'una dayanır. Aşağıdaki dört kaynak ilk inceleme bağlamıdır:

| Kaynak | Yetki düzeyi | Bu aşamadaki rolü |
|---|---:|---|
| `00_MASTER_PROMPT.md` ve `00_DESPARETE_GOLDEN_RULES.md` | Proje yönetimi | Süreç, kapsam ve doğruluk kuralları |
| `01_FANET_ROUTING_FOUNDATION.md` | Seviye 2 | FANET problem gerekçesi ve G1–G14 başlangıç gereksinimleri |
| `02_DESPERATE_PRIOR_ART.md` | Seviye 2 | Önceki çalışmalar, benzerlik analizi ve yenilik-iddaası sınırları |
| `DESPARETE – Protokol Taslağı v0.md` | Seviye 3 | İncelenecek başlangıç mimarisi ve çalışma fikirleri |

Resmî gereksinim modeli (`06`), açık sorular (`07`) ve karar günlüğü (`05`) artık mevcuttur. Güncel normatif davranış `10`…`31`de; candidate assembly `36`da, conformance/trace/freeze hazırlığı `37`…`39`dadır. Tarihsel v0 karşılaştırması ise yalnız bağlam içindir.

## 2. Kanıta dayalı olarak yerleşmiş hususlar

Bunlar DESPARETE tasarım kararları değil; araştırma belgelerinin dayandırdığı problem ve öncül-art sonuçlarıdır.

- FANET'lerde yüksek hareketlilik, kısa bağ/rota ömrü, seyreklik ve ağ bölünmesi, kanal değişkenliği, kontrol yükü ve taktik bozunma gerçek tasarım baskılarıdır.
- Tek başına hop sayısı, sabit beacon aralığı veya salt kopma-sonrası onarım bu baskıları yeterince ele almaz.
- Gradyan/potansiyel alan, Bellman–Ford/mesafe-vektör yayılımı, dinamik bağ maliyeti, uyarlamalı beacon, multipath ve öngörülü geçiş ayrı ayrı öncüllüdür; DESPARETE bunlardan hiçbirini tek başına yeni diye sunamaz.
- Döngü özgürlüğü için TTL, yalnızca hasar sınırlama aracıdır; kanıt değildir. Dinamik mesafe-vektör tasarımı güvenli successor/feasibility, sıra/epoch semantiği veya eşdeğer bir güvenlik koşulu gerektirir.
- Paket kaybı, jamming kanıtı değildir. Protokol bozulmaya tepki verebilir; nedensel jamming tespiti iddiası için ayrı doğrulama gerekir.
- İncelenen taramada, FANET bağlamında gradyan/DV + yerel risk değerlendirmesi + rejime bağlı koşullu yedekliliğin eşdeğer bir birleşimi belirlenmemiştir. Bu, yenilik kanıtı değil, kapsamı sınırlı bir prior-art gözlemidir.

## 3. Tarihsel v0'da bulunan tasarım adayları (aktif şartname değildir)

| Alan | v0 adayı | Durum |
|---|---|---|
| İşletim | Merkezi koordinatörsüz, hedef-yönlü dağıtık yönlendirme | Gerekçeli aday |
| Alan hesabı | `P(i) = min_j(P(j)+C(i,j))`, hedefte `P=0` | Aday; güvenlik koşulu eksik |
| İletim | Daha düşük potansiyelli komşuya yerel ilerleme | Aday; tek başına döngü kanıtı değil |
| Bağ maliyeti | Temel hop + bağlantı kalitesi + bozunma/jamming cezası | Aday; kavramlar ve fonksiyon tanımsız |
| Komşuluk | ACTIVE → STALE → SUSPECT → EXPIRED | Aday; geçiş kanıtları ve zamanlayıcılar tanımsız |
| Tazelik | Hedef üretimli epoch, soft-state, reaktif başlatma | Aday; artan maliyet, yeniden başlatma ve bölünme semantiği eksik |
| Politika | NORMAL ve CRISIS, aynı motorun iki politikası | Aday; risk modeli tamamlanmamış |
| Dayanıklılık | CRISIS'te seçici alternatif sonraki atlama ve kritik veri çoğaltma | Aday; bağımsızlık/korelasyon ve kapatma kuralları eksik |
| Arıza | Probe, alan yenileme, sınırlı tampon, teslim başarısızlığı | Aday; tetikleyici, sınır ve hata davranışları eksik |

## 4. Tespit edilen uyumsuzluklar ve tasarım boşlukları

1. **Döngü özgürlüğü:** v0, sıkı potansiyel inişi ve TTL'yi kullanır ancak güncel olmayan komşu potansiyelleri altında güvenli successor koşulu vermez. Master bağlamı bu eksikliği kritik olarak işaretler.
2. **Epoch yetkisi:** v0'daki hedef-üretimli epoch ile bağ maliyeti arttığında yeni epoch gereksinimi birlikte tanımlanmamıştır. Hedefin erişilemediği anda ara düğümün maliyet artışını nasıl güvenle temsil edeceği açıktır.
3. **Risk semantiği:** Master bağlamındaki kalite–hazard–belirsizlik–risk ayrımı, v0'daki `C_jam` ve `CrisisScore` ile henüz eşlenmemiştir. `C_jam` adı, doğrulanmamış nedensel jamming atfı yapma riski taşır.
4. **Mod yayılımı:** “Global kriz duyurusu yok” ilkesi ile `MODE_NOTICE` önerisi birlikte bulunur; menzil, alıcı davranışı ve güvenlik semantiği tanımlanmadığı için çelişki yaratabilir.
5. **Mesaj ailesi:** Metin `FIELD_INITIATE` kullanır; aday mesaj listesinde ise `FIELD_REQUEST` vardır. Başlatma/istek/yanıt ayrımı tamamlanmamıştır.
6. **Komşu kullanımı:** STALE komşunun NORMAL/CRISIS'te kullanımı ve SUSPECT komşunun veri iletimine uygunluğu kesin değildir.
7. **Başlatma kapsamı:** v0 tek/birincil sink varsayımına eğilimlidir. Bu, protokolün uygulama profili olarak tanımlanmalı; genel çok-hedef semantiğinin yerine geçmemelidir.
8. **Taslak statüsü:** v0 “mimari kilitlendi” ifadesini kullanır; yönetici bağlam ise tüm ana mimari unsurları değiştirilebilir adaylar olarak sınıflandırır. Yönetici bağlam üstün kabul edilmiştir.

## 5. Bilinçli olarak yapılmayan varsayımlar

- Metrik ağırlıkları, eşikler, pencere uzunlukları, zamanlayıcı değerleri veya paket bit uzunlukları atanmadı.
- Jamming tespit edildi, bağlantılar simetriktir, GPS sürekli doğrudur veya her zaman uçtan uca yol vardır varsayılmadı.
- v0'ın potansiyel alan mimarisinin kesinleştiği veya döngüsüz olduğu varsayılmadı.
- Önceki çalışmaların tüm literatürü tükettiği ya da DESPARETE'nin kesinlikle yeni olduğu varsayılmadı.
- Simülasyon mimarisi, deney matrisi veya parametre kalibrasyonu tasarım kapsamına alınmadı.

## 6. Faz durumu ve sonraki zorunlu tasarım işi

G1–G14, artık `06_DESPARETE_REQUIREMENTS.md` içinde FR/NFR biçimine, önceliklere, kabul kanıtlarına ve çakışma ilkelerine dönüştürülmüştür. Bu, gereksinim fazının ilk tam tabanıdır; proje sahibinin onayı olmadan mimari karara dönüşmez.

Kavramsal model kullanıcı onayıyla `08_DESPARETE_CONCEPTUAL_MODEL.md` içinde kabul edilmiş çalışma yönü oldu: kalite mevcut koşul, hazard bozunma eğilimi, belirsizlik bilgi güven sınırı ve risk link-yerel ihtiyat değişkenidir. Bu, sayısal risk fonksiyonu veya maliyet mimarisi kararı değildir.

Bilgi modeli (`09`) ve komşu yaşam döngüsü adayı (`10`) tamamlandı. Komşu modelinin temel güvenlik yönü: ACTIVE dışında hiçbir komşu veri forwarding'e aday olamaz; bozunma duyarlı politika bu sınırı gevşetmez. Bu detaylandırma, loop-freedom mekanizmasını henüz seçmez.

Risk modelinin yönü kullanıcı tarafından onaylandı: doğrudan teslim, yaş ve teslim eğilimi minimum gözlemler; radyo ve hareket isteğe bağlı kanıttır. Risk `R=g(H,U)` olarak ele alınır ve Q'dan ayrıdır. Q/H/U/R'nin sayısal formülü tanımlanmadı.

Link maliyet mimarisi kullanıcı tarafından onaylandı: pozitif atlama tabanı + kalite cezası + risk cezası; forwarding uygunluğu maliyet tercihinden önce gelen bağımsız bir güvenlik kapısıdır. Sayısal dönüşüm fonksiyonları tanımlanmadı.

Potansiyel alan ve loop-freedom mimarisi kullanıcı tarafından onaylandı: v0'ın salt epoch + sıkı inişi, hedef-üretili DFSN, feasibility distance, safe successor ve DFSN istemi ile değiştirilir. Garantinin kapsamı, tek originator `K` alanı ve doğru çalışan düğümlerle sınırlıdır.

Freshness mimarisi kullanıcı tarafından onaylandı: epoch terminolojisi OIID + DFSN + local-age olarak ayrıştırılır; hedef restartında OIID değişir; DFSN tanımsız seri kıyaslarında fail-closed davranılır. Bit genişlikleri ve timerlar açık kalır.

Uyarlamalı politika mimarisi kullanıcı tarafından onaylandı: node-geneli NORMAL/CRISIS yerine alan-geneli STEADY/CAUTION/PROTECT postürleri kullanılır; risk maliyette yalnız bir kez temsil edilir; MODE_NOTICE çekirdekten çıkarılır. Traffic-class ve redundancy ayrıntıları açık kalır.

Hata, yerel onarım ve partition mimarisi kullanıcı tarafından onaylandı: alternatifsiz repair'de withdrawal + bounded DFSN istemi + field-local REPAIRING/UNREACHABLE kullanılır; DELIVERY_FAILURE zorunlu yerel olay, ağ üzerinden FAILURE_REPORT ise yalnız bağımsız güvenli ters alan varsa isteğe bağlıdır. Buffer/timer sayısal başlangıç sınırları sonraki `21` profiliyle tanımlanmıştır.

Multipath/redundancy mimarisi kullanıcı tarafından onaylandı: sürekli multipath yerine safe alternate + PROTECT + protection eligibility + finite budget ile sınırlı first-hop-diverse redundancy kullanılır. Uçtan uca ayrıklık iddiası yapılmaz; ilk-sürüm fanout/budget profili `MaxReplicaFanout=2` ve ingress `RB∈{0,1}` olarak `22`/`23`te tanımlanmıştır.

Kontrol mesajı mimarisi kullanıcı tarafından onaylandı: FIELD_UPDATE (withdrawal dahil), FIELD_SOLICIT, sınırlı DFSN_REQUEST, PROBE/PROBE_REPLY ve isteğe bağlı FAILURE_REPORT çekirdek ailedir. FIELD_UPDATE'ta sender-local Advertisement-Serial kullanılır.

Wire format/TLV tasarımı (`19`) proje sahibi tarafından onaylandı: 4-octet base header, 64-bit opaque kimlikler, 32-bit DFSN/ADS, 32-bit sabit-noktalı potential ve 32-bit hizalı TLV uzantıları.

Timer ve yaşlandırma mimarisi (`20`) proje sahibi tarafından onaylandı. Komşu, alan-ilanı, solicit/request, repair, buffer, duplicate/OIID ve policy zamanları bağımsız yerel soft-state'tir. DFSN_REQUEST uyuşmazlığında B seçildi: request wire lifetime taşımaz; Hop Limit mekânsal, `T_req_session`/`T_req_duplicate` yerel zamansal sınırdır. Dengeli operasyonel tempo, sayısal profil için onaylanan başlangıç yönüdür. Sessiz ACTIVE komşuların gereksiz STALE dalgalanmasını önlemek için normal `T_idle_probe` denetimi de mimariye eklenmiştir.

Dengeli sayısal profil (`21`) proje sahibi tarafından ilk sürüm başlangıç profili olarak onaylandı. Profile; kontrol/data gecikme varsayımları, tüm timer değerleri, `H_req=H_data=16`, Class-0 buffer quota, duplicate saklama ve policy evidence süreleri eklenmiştir. Değerler ölçülmüş optimum değil, açık varsayımlı ve sürümlenebilir başlangıç tasarımıdır.

Durum makineleri (`22`) proje sahibi tarafından ilk sürüm için onaylandı. Komşu, field erişilebilirliği, policy, acquisition/request ve paket/buffer yaşamı ayrıldı; ortak atomik olay sırası tanımlandı. `UNREACHABLE` sonrası otomatik control re-entry yoktur: yalnız yeni valid field kanıtı, ilk acquisition veya explicit reacquire kullanılabilir. İlk operasyon profili tek-sink'tir; wire/field tasarımı ileride çok-hedefe genişletilebilir. Redundancy, toplamda primary + en çok bir alternate (`MaxReplicaFanout=2`) ile sınırlıdır.

Çekirdek algoritma/pseudocode (`23`) proje sahibi tarafından ilk sürüm için onaylandı. Paketin kabulü, komşu kanıtı, FIELD_UPDATE/DFSN_REQUEST, field yeniden hesaplama, repair, DATA forwarding ve timer dispatch handler'ları tanımlandı. Eşit maliyet tie-break'i, dar target DFSN-request yetkisi, ilk acquisition DATA'nın bufferlanmaması ve ingress `RB ∈ {0,1}` sınırı ilk-sürüm kurallarıdır.

Doğruluk ve koşullu yakınsama analizi (`24`) proje sahibi tarafından onaylandı. Safety argümanı FD/DFSN/OIID invariantlarına dayanır; TTL'ye dayanmaz. `H_req=H_data=16` hizası, ilk sürümün izin verdiği hop çapında feasibility-starvation recovery için koşullu liveness kapsamını tamamlar; request teslimi, global erişilebilirlik veya performans garantisi değildir.

Sıradaki faz, minimum güvenlik varsayımlarını, authentication/replay kurallarını ve kaynak tüketim sınırlarını somutlaştıran security mimarisidir.

Security mimarisi için karar kaydı (`25`) hazırlandı. Bu kayıt; başlangıçtaki AUTHENTICATION TLV hook'unun tek başına güvenlik mekanizması olmadığını, target-only OIID/DFSN yetkisi için group MAC'in yetersiz kaldığını ve R0/R1/R2 replay kapsamlarını ayırır. Proje sahibi P3 yönünü, görev öncesi public-key rosterı, R1'i ve DATA source integrity'yi onayladı.

Security Profile v0.1 (`26`) proje sahibi tarafından onaylandı ve `19`, `20`, `22`, `23`, `24`e bağlandı. Her pakette Ed25519 HOP authentication; FIELD_UPDATE'ta target OriginSignature; DATA'da SourceSignature zorunludur. Görev öncesi public-key roster kullanılır; R1, aktif authenticated peer için strict control high-water anti-replay sağlar. Bu; RF jamming, confirmed kötü niyetli relay metriği, persistent reboot-replay veya payload gizliliği garantisi değildir. Sayısal CPU/radio kaynak profili sonraki complexity aşamasına bırakılmıştır.

Kaynak/karmaşıklık analizi (`27`) proje sahibi tarafından ilk-sürüm için onaylandı. Routing soft state'i `O(d_i×f_i + b_i + duplicate-cache)`, security ek state'i `O(n+d_i)` olarak ayrıştırılır; request wave, replication, header ve signature doğrulama sınırları formüle edilir. Platform kapasitesi (`n`, `d_i`, MTU, `V_i`, ingress rate) ölçülmediği için sayısal performans iddiası yoktur.

Hata/telemetri sözleşmesi (`28`) proje sahibi tarafından ilk-sürüm için onaylandı. Hata paketine otomatik yanıt üretilmez; format/auth/replay ve kaynak redleri local state etkisi ile rate-limited event/counter olarak ayrılır. FAILURE_REPORT yalnız gerçek local delivery-failure ve bağımsız güvenli report field ile mümkündür. Yönetim export taşıyıcısı, retention, alarm eşikleri ve erişim güvenliği deployment profile açık kalır.

Deployment kapasite kabul kapısı (`29`) hazırlandı. Security Profile 1 için MTU, payload, roster, retained-neighbor/field, buffer, ingress, sign/verify, airtime ve bellek girdileri zorunlu ve ölçülebilir şekilde listelenmiştir. Değerler kullanıcı/platform tarafından sağlanana kadar DESPARETE'nin deployment etiketi `DESIGN-ONLY`dir; bu bir protokol eksikliği değil dürüst kapsam sınırıdır.

Entegrasyon denetimi ve gereksinim matrisi (`30`) hazırlandı. Yirmi FR/NFR maddesinin her biri somut mekanizma belgelerine bağlanmıştır; önceki security/neighbor bootstrap belirsizliği DL-039 ile, 2026-09-21/22 ara denetimindeki R1 bootstrap, M0.1 telemetry sınırı, güvenlik reddi, ACTIVE olmayan peer'dan OIID kabul sırası, master envanterindeki dosya adları ve eski kavramsal referans uyumsuzlukları IA-14…IA-17 ile hizalandı. Bu denetimin kapsadığı çekirdek safety/semantik için açık bir belge çelişkisi kalmamıştır; requirements baseline, sözlük/ref-denetimi, prior-art re-audit ve M0.1 metric profile tasarım kapıları kapanmıştır. Kullanıcı diyagramları, implementation edge-case izleri ve deployment kapasitesi sonraki tamamlık kapılarıdır.

Kanonik terim ve uyum dili (`31`) hazırlandı. `ACTIVE`, authenticated peer, direct-peer candidate, R1, ADS/DFSN/Request-ID ve DESIGN-ONLY ayrımları tek sözlükte sabitlenmiştir. Bir sonraki iş, sözlüğe karşı mekanik referans denetimi ile nihai prior-art re-audit kapsamının hazırlanmasıdır; DESPARETE bu aşamada **final** veya **DESIGN COMPLETE** değildir.

Prior-art yeniden denetimi (`32`) tamamlandı. Başlangıçtaki “FANET'te gradient/potential routing bulunamadı” çıkarımı MGRF (2019) ve UAV potential-field (2024) ile geçersizdir; jamming-aware multipath ve connectivity-uyarlamalı replikasyon için de yakın akademik/patent öncülleri vardır. DESPARETE artık yenilik/patentlenebilirlik iddiası taşımayacak; yalnız açık safety, freshness, redundancy ve packet-security sınırları olan bir tasarım adayı olarak konumlandırılacaktır.

Proje sahibi `06`yı v0.1 gereksinim baseline'ı olarak onayladı; platform/mission girdilerine kadar `DESIGN-ONLY` statüsünü kabul etti (DL-041). `33`te master bağlamdaki 17 kanonik düşünce deneyi tamamlandı; ancak bu bir runtime test sonucu değildir. Proje sahibi `34`te önerilen görev öncesi ortak profil + `R=max(H,U)` (A/M1) yönünü onayladı; `35` M0.1, ortak admission, gözlem, tamsayı maliyet/policy dönüşümleri ve test vektörlerini tanımlar (DL-042). `36`, modüler normları üstünlük sırasıyla tek bir candidate protocol draft'ta birleştirdi; `30` IA-11/IA-12 onun wire/security/metric bağlarını denetledi. `37`, uygulama conformance vakalarını; `38`, bunlar için trace/negatif kanıt biçimini; `39`, freeze kapılarını tanımladı. Bu üç belge test sonucu veya freeze kararı değildir. Mevcut çalışma noktası, kullanıcı diyagramlarının metin eşlemesini; sonrasında final belge denetimi, proje sahibi freeze kararı, implementation event-trace ve platform kapasite kanıtını bekleyen freeze-preparation aşamasıdır.
