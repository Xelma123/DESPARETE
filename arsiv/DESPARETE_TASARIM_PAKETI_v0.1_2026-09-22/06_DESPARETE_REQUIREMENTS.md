# DESPARETE — Resmî Gereksinim Modeli

**Sürüm:** 0.1 (onaylı gereksinim baseline'ı)  
**Durum:** Proje sahibi tarafından 2026-09-21'de v0.1 gereksinim baseline'ı olarak kabul edildi. Bu kabul, sayısal metric kalibrasyonunu, platform kapasitesini veya protokol dondurmasını otomatik onaylamaz.  
**Tarih:** 2026-09-21

## 1. Amaç ve sınırlar

Bu belge, DESPARETE'nin çözmesi gereken problemi ve tasarımın uyması gereken kısıtları tanımlar. Algoritma, formül, eşik, zamanlayıcı değeri veya wire formatı tanımlamaz. Bunlar ancak gereksinim–mekanizma izlenebilirliği kurulduktan sonra seçilebilir.

DESPARETE'nin hedefi, merkezi koordinatöre sürekli erişim varsaymadan, taktik FANET ortamlarında iletişim bozulması ve topoloji değişimi karşısında **tanımlı, güvenli ve kaynak-bilinçli** çok-atlamalı yönlendirme davranışı sağlamaktır. Protokol, bozunmanın nedeninin jamming olduğunu teşhis etmeyi vaat etmez; gözlenen bozunmaya tepki verir.

### 1.1 Kapsam içi

- Dağıtık ağ-katmanı yönlendirme davranışı.
- Komşu/bağ gözlemi, bilginin yaşlandırılması ve yerel rota kararı.
- Bozunma öncesi uyarlama, kopma sonrası onarım, sınırlı tamponlama ve bölünme davranışı.
- Kontrol bilgisi, durum ve algoritmaların sonradan uygulanabilir bir şartnameye dönüştürülmesi.

### 1.2 Kapsam dışı

- Uçuş/yörünge kontrolü, radyo kanal seçimi veya iletim gücü kontrolü.
- Jamming kaynağının kesin tespiti ya da saldırgana atıf.
- AODV/OLSR/AOMDV uygulaması, simülasyon mimarisi, deney matrisi ve parametre optimizasyonu.
- DTN teslim garantisi, sınırsız tamponlama veya kesintisiz bağlantı varsayımı.

## 2. Terimler ve öncelik ölçeği

- **Zorunlu (MUST):** Karşılanmazsa protokolün temel amacı veya doğruluğu bozulur.
- **Güçlü hedef (SHOULD):** Gerekçeli olarak ertelenebilir, ancak tasarım bunu açıkça göstermelidir.
- **Gelecek profil (MAY):** Çekirdek v0.x için zorunlu değildir.
- **Doğrulama:** “Analiz” mantıksal/biçimsel argümanla; “iz sürme” tanımlı olay senaryosuyla; “ölçüm” ise sonraki bağımsız değerlendirmede gözlemlenebilir protokol olaylarıyla yapılır. Sayısal başarı eşiği bu aşamada atanmaz.

## 3. Paydaş hedefleri ve tasarım ilkeleri

| Hedef | Tasarım sonucu |
|---|---|
| Doğruluk | Veri iletimi döngü oluşturmayacak; geçersiz/bayat bilgiyle yönlendirme açıkça sınırlanacak. |
| Dayanıklılık | Topoloji ve gözlenen bağ bozunması değiştiğinde tanımlı önleyici ve onarıcı davranış bulunacak. |
| Tutumluluk | Dayanıklılık için sürekli, sınırsız flood veya sürekli yedek kopyalama kullanılmayacak. |
| Dağıtıklık | Kararlar yerel bilgiyle alınacak; tek hata noktası kabul edilmeyecek. |
| Bilimsel dürüstlük | Jamming, risk ve yenilik iddiaları kanıt düzeyini aşmayacak. |
| Uygulanabilirlik | Düğüm durumu ve hesaplama, SWaP-kısıtlı platformlar için açıkça sınırlandırılacak. |

## 4. Fonksiyonel gereksinimler

| Kimlik | Öncelik | Gereksinim | Gerekçe / kaynak | Kabul kanıtı | Tasarıma getirdiği sınır |
|---|---|---|---|---|---|
| FR-01 | MUST | Protokol, 3B ve yüksek değişken hızlı FANET hareketinin neden olduğu komşuluk/topoloji değişimlerini gözlemleyip, bayat bilgi için tanımlı işlem uygulamalıdır. | Foundation G1, B1–B4 | Yüksek göreli hız ve bayat komşu bilgisi senaryosunda giriş, yaşlandırma, geçersizleştirme ve yeniden edinim iz sürmesi. | Sabit ve sınırsız geçerlilik varsayamaz. |
| FR-02 | MUST | Protokol, gözlenebilir bağ bozunması kopmaya dönüşmeden önce rota seçimini yeniden değerlendirebilmelidir; bu davranış öngörü doğruluğu iddiası gerektirmez. | Foundation G2; v0 pre-failure hedefi | Kademeli bozunma senaryosunda ölçüm → durum → politika/aday yeniden değerlendirme zinciri. | Bozunma sinyali ile kesin jamming veya kesin kopma eş tutulamaz. |
| FR-03 | MUST | Geçerli yönlendirme alanı olmayan hedef için alan edinimi, başarısız edinim ve yeniden deneme davranışı tanımlanmalıdır. | Foundation G3, B7 | Yeni hedef, bayat alan ve erişilemeyen hedef senaryolarında mesaj/yerel durum iz sürmesi. | Sürekli flooding birincil edinim mekanizması olamaz. |
| FR-04 | MUST | Bir sonraki atlama kararı, anlık iletişim kalitesi ile bağın bozunma eğilimini ayrı kavramlar olarak değerlendirebilmelidir. | Foundation G4, B5, B9 | Aynı anlık kaliteye fakat farklı kötüleşme eğilimine sahip iki bağda ayrımın nasıl temsil edildiğinin analizi. | Kalite, hazard, risk ve maliyet aynı değişken adıyla tanımlanamaz. |
| FR-05 | SHOULD | Tasarım, güvenilirlik/kararlılık, gecikme, enerji ve kontrol yükü arasındaki takasları açıkça ele almalı; birini iyileştirirken diğerleri üzerindeki etkisini gizlememelidir. | Foundation G5 | Gereksinim çakışma tablosu ve seçilen her mekanizma için etki kaydı. | Tüm hedeflerin aynı anda optimum olacağı varsayılamaz. |
| FR-06 | MUST | Geçerli bir sonraki atlama olmadığında protokol; veri tutma, bırakma/başarısızlık bildirimi ve bağlantı geri geldiğinde iyileşme için sınırlı davranış tanımlamalıdır. | Foundation G6 | Bölünme, tampon süresi dolması ve partition healing senaryolarının iz sürmesi. | Bu, DTN teslim garantisi veya sınırsız buffer gerektirmez. |
| FR-07 | MUST | Gözlenen iletişim bozunması ve konum bilgisindeki bozulma altında protokolün güvenli bozunma davranışı tanımlanmalıdır. | Foundation G7, B14 | Kayıp/girişim/jamming-benzeri ve GPS bilgisinin erişilemez/bayat olduğu senaryolarda karar girdileri ve geri çekilme davranışı. | “Jammer bulundu” veya konum her zaman güvenilir iddiası yasaktır. |
| FR-08 | SHOULD | Komşu gözlemi ve kontrol davranışı, yoğunluk ve değişim rejimine duyarlı olmalıdır. | Foundation G8 | Seyrek ve yoğun rejimlerde ölçüm/yaşlandırma/politika farkının açıklanması. | Rejim geçişleri için sabit evrensel eşik varsayılmaz. |
| FR-09 | MUST | Her hedef için forwarding kuralı, eşzamanlı/bayat güncellemeler ve maliyet değişimleri altında döngü özgürlüğünü sağlayan açık bir güvenlik koşuluna dayanmalıdır. | Master §11; v0 §3/§5 | İnvariant veya eşdeğer kanıt; stale update, maliyet artışı ve eşzamanlı güncelleme düşünce deneyleri. | TTL sadece hasar sınırlayıcı olabilir; kanıtın yerine geçemez. |
| FR-10 | MUST | Protokol, hedefe ilişkin tazelik/versiyon bilgisinin üretimini, karşılaştırılmasını, geçersizleştirilmesini ve yeniden başlatma/rollover davranışını tanımlamalıdır. | Master §18 | Epoch/sequence olay tablosu: hedef erişilebilir/değil, node restart, partition healing, eski/tekrar mesaj. | “Daha yeni” ifadesi toplam sıralama olmadan kullanılamaz. |
| FR-11 | MUST | Komşu durumları, veri/denetim kullanım yetkileri, geçiş kanıtları ve age-belirsizlik etkisi tanımlanmalıdır. | Master §17; v0 §6 | Her durum ve geçiş için olay, timer/koşul, forwarding izni ve başarısız davranış tablosu. | Belirsiz bir STALE/SUSPECT komşu sessizce kullanılmamalıdır. |
| FR-12 | SHOULD | Bozunma altında alternatif forwarding veya çoğaltma kullanılıyorsa, etkinleştirme, kapsam, bağımlı-hata sınırı ve kaldırma koşulları tanımlanmalıdır. | Master §21; Foundation B8 | Tek yol, alternatif var/yok, ortak hata alanı ve düzelme senaryoları. | Multipath kendi başına amaç veya yenilik değildir; bağımsızlık garanti edilmedikçe öyle sunulamaz. |
| FR-13 | MUST | Protokol, hatalı/tekrar/bayat kontrol mesajları, geçersiz alanlar, bilinmeyen sürüm/tip ve teslim başarısızlığı için tanımlı hata davranışı sağlamalıdır. | Master §28 | Her hata sınıfı için kabul/red, yerel durum etkisi ve bildirim davranışı. | Hata işleme yalnızca TTL'ye bırakılamaz. |
| FR-14 | MUST | Protokol, yönetim/alan/risk bilgisinin sahte veya tekrar oynatılmış olabileceği varsayımını güvenlik değerlendirmesinde ele almalıdır. | Master §29; Foundation B15 | Tehdit–etki–varsayım–azaltım/kalıntı risk tablosu. | Çözülmemiş saldırılar çözülmüş gibi sunulamaz. |

## 5. Kalite ve kaynak kısıtları

| Kimlik | Öncelik | Gereksinim | Gerekçe / kaynak | Kabul kanıtı |
|---|---|---|---|---|
| NFR-01 | MUST | Rota edinimi ve bakımında kalıcı birincil mekanizma olarak sınırsız ağ-geneli flooding kullanılmamalıdır. | Foundation G9, B6–B7 | Her kontrol mesajı için kapsam ve üst sınır/sonlanma koşulu. |
| NFR-02 | SHOULD | Enerji etkisi, özellikle kontrol trafiği ve çoğaltmada görünür bir tasarım maliyeti olarak ele alınmalıdır. | Foundation G10 | Mekanizma–enerji etkisi ve takas kaydı. |
| NFR-03 | MUST | Düğüm başına durum, hedef ve komşu sayısına göre ifade edilmeli; en kötü durum kontrol davranışı açıklanmalıdır. | Foundation G11 | Bellek, işlem ve mesaj karmaşıklığı analizi. |
| NFR-04 | SHOULD | Tasarım, zorunlu merkezi lider, küme başı veya sürekli erişilebilir ağ geçidi varsaymadan ölçeklenmelidir. | Foundation G12–G13 | Dağıtık karar ve tek-hata-noktası analizi. |
| NFR-05 | MUST | Şartname, gerçekçi hareket ve bozunma değerlendirmesine imkân verecek gözlemlenebilir olayları tanımlamalıdır. | Foundation G14 | Uygulamanın dışarı vereceği durum/olay arayüzü listesi; deney tasarımı değil. |
| NFR-06 | MUST | Kavramlar, algoritmalar, mesajlar ve timerlar arasında iç tutarlılık denetimi yapılabilir biçimde adlandırılmalıdır. | Master §38 | Terim sözlüğü, referans denetimi ve izlenebilirlik matrisi. |

## 6. Gereksinim çakışmaları ve çözüm ilkeleri

| Çakışma | Neden gerçek bir çakışmadır? | Bu aşamadaki çözüm ilkesi | İlgili açık soru |
|---|---|---|---|
| FR-02 erken uyarlama ↔ NFR-01 düşük kontrol yükü | Daha sık ölçüm ve alan yenileme enerji/bant tüketir. | Uyarlama yalnız kanıtın güncelliği ve beklenen fayda gerektirdiğinde etkinleşmeli; eşikler daha sonra gerekçelendirilmelidir. | OQ-006, OQ-007, OQ-016 |
| FR-04 zengin bağ bilgisi ↔ NFR-03 uygulanabilirlik | Çok metrik ölçmek ve paylaşmak durum/işlem maliyetini artırır. | Her değişken için bağımsız semantik ve gereklilik kanıtı zorunludur; tekil gürültülü ölçümler eklenmez. | OQ-003, OQ-006 |
| FR-06 tamponlama ↔ gecikme/kaynak bütçesi | Daha uzun bekleme olası teslimi artırabilir, gecikme ve bellek tüketimini artırır. | Tampon sınırlandırılmıştır; teslim garantisi çıkarılmaz. Sınırlar sonraki profillemede belirlenir. | OQ-013 |
| FR-12 yedeklilik ↔ NFR-01/NFR-02 | Alternatif korumak ve kopyalamak kontrol/veri yükünü yükseltir. | Yedeklilik yalnız açık hata-toleransı gerekçesiyle ve devreden çıkma kuralıyla kullanılabilir. | OQ-012 |
| FR-09 döngü güvenliği ↔ FR-02 hızlı tepki | Koruyucu feasibility/versiyon kuralları bazen en kısa anlık yanıtı geciktirebilir. | Güvenlik önceliklidir; hızlı uyarlama güvenli successor koşulunu geçemez. | OQ-001, OQ-002 |
| FR-07 bozunmaya tepki ↔ yanlış jamming atfından kaçınma | Kayıp birçok sebepten olabilir. | Tepki, gözlenen kalite/hazard/belirsizliğe verilir; jamming yalnız kanıt seviyesi olarak temsil edilir. | OQ-003, OQ-006 |

## 7. İzlenebilirlik başlangıç matrisi

Bu matris, mekanizma seçimi yapılmadan önce yalnızca hangi adayların hangi gereksinimlere cevap vermeyi amaçladığını gösterir. “Aday” bir onay değildir.

| Gereksinim | Taslakta görülen adaylar | Zorunlu sonraki tasarım çıktısı |
|---|---|---|
| FR-01, FR-11 | Adaptif komşu yaşlandırma; ACTIVE/STALE/SUSPECT/EXPIRED | Gözlem ve komşu modeli |
| FR-02, FR-04, FR-07 | Bağ kalitesi/bozunma gözlemi; yerel politika | Kalite, hazard, belirsizlik ve risk modeli |
| FR-03, FR-10 | Hedef-yönlü field; soft-state; epoch | Alan başlatma ve freshness modeli |
| FR-09 | Sıkı potansiyel inişi | Güvenli successor/loop-freedom mekanizması; mevcut aday yeterli kabul edilmemiştir |
| FR-06 | Field request, probe, sınırlı buffer, delivery failure | Bölünme ve hata işleme modeli |
| FR-12 | Koşullu alternatif sonraki atlama, seçici çoğaltma | Redundancy/failure-domain modeli |
| NFR-01–NFR-03 | Yerel karar, uyarlamalı kontrol, sınırlı durum | Kontrol kapsamı ve karmaşıklık analizi |
| FR-13–FR-14 | Kontrol mesajları ve freshness bilgisi | Hata ve güvenlik modeli |

## 8. Faz kabul kapısı

Gereksinim fazı, aşağıdakiler tamamlanmadan kapatılmış sayılmaz:

- [x] Her FR/NFR için benzersiz kimlik, gerekçe, öncelik ve kabul kanıtı vardır.
- [x] Çakışan gereksinimler görünürdür ve çözüm ilkeleri kaydedilmiştir.
- [x] Kapsam dışı konular açıkça ayrılmıştır.
- [x] Her v0 aday mekanizmasının en az bir gereksinim ilişkisi veya reddedilme gerekçesi vardır.
- [x] OQ-001–OQ-005 için çözüm planı kabul edilmiştir.
- [x] Proje sahibi, bu gereksinim tabanını v0.1 tasarım baseline'ı olarak onaylamıştır (DL-041).

## 9. Kaynak notu

Bu model, `01_FANET_ROUTING_FOUNDATION.md` içindeki G1–G14 ile `00_MASTER_PROMPT.md` içindeki doğruluk ve kapsam kurallarından türetilmiştir. Kaynak belgelerinin literatür atıfları burada çoğaltılmamıştır; bilimsel iddia veya nihai spesifikasyon yazılırken birincil kaynaklar yeniden doğrulanmalıdır.
