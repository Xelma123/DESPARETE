# DESPARETE — Kontrol Mesajları Semantiği

**Sürüm:** 0.1 (onaylı control-message semantiği)  
**Durum:** Çekirdek mesaj ailesi onaylıdır; bit uzunlukları ve kesin encoding `19`, security bağları `26`, handler'lar `23`tedir.  
**Tarih:** 2026-09-21

## 1. Amaç ve tasarım ilkeleri

Kontrol düzlemi, alan edinimi, alan bakımı, komşu doğrulaması ve hata raporlaması için gerekli en küçük mesaj ailesini tanımlar. Her mesajın amacı, kapsamı ve forwarding semantiği ayrı olmalıdır.

İlkeler:

1. **Alan ilanı, keşif isteği ve yeni-DFSN isteği farklı işlemlerdir.**
2. **Hiçbir kontrol mesajı, data-plane safe-successor koşulunu gevşetmez.**
3. **Tek-atlama mesajlar normalde yeniden yayılmaz; çok-atlama istekler duplicate, kapsam ve rate sınırına tabidir.**
4. **Kontrol mesajı, yerel risk/jamming yargısını ağ-geneli gerçek gibi taşımaz.**
5. **Her mesaj, geçersiz sürüm/kimlik/alan/seri durumunda fail-closed işlenir.**

## 2. Ortak kontrol zarfı

Her DESPARETE kontrol mesajı, wire formatta bit uzunlukları belirtilecek aşağıdaki semantik öğeleri taşır:

| Öğe | Zorunluluk | Amaç |
|---|---|---|
| Protocol-Version | Zorunlu | Uyumlu olmayan mesajı değerlendirmeden reddetmek. |
| Message-Type | Zorunlu | Mesajın işlem semantiğini seçmek. |
| Sender-ID | Zorunlu | Gönderen komşu kaydı ve duplicate anahtarı. |
| Sender-Instance-ID | Zorunlu | Ara düğüm restartından sonra eski ilan/mesajı ayırmak. |
| Message-ID | Zorunlu | Yeniden oynatma/duplicate bastırma için gönderen-yerel tekil kimlik. |
| Authentication/Integrity extension | Opsiyonel, güvenlik profiline bağlı | Kaynak ve bütünlük koruması; güvenlik fazında zorunluluk düzeyi belirlenecek. |

`Message-ID`, aynı gönderici örneği içinde tekrarlanmamalıdır. Mesaj-ID'nin bit genişliği, rollover ve cache ömrü wire/timer fazlarında tanımlanacaktır. Message-ID tek başına alan freshness'i sağlamaz; field mesajları kendi OIID/DFSN/advertisement serial kurallarını uygular.

## 3. Mesaj ailesi özeti

| Mesaj | Kapsam | Temel işlev | Yeniden yayılım |
|---|---|---|---|
| FIELD_UPDATE | Tek atlama | Alan potential ilanı veya withdrawal | Düğümler kendi durum değişimini yeniden ilan eder; gelen mesajı körce forward etmez. |
| FIELD_SOLICIT | Tek atlama | Komşulardan mevcut geçerli alan bilgisini isteme | Hayır; uygun komşu FIELD_UPDATE ile yanıtlar. |
| DFSN_REQUEST | Sınırlı çok atlama | Hedeften yeni DFSN/alan turu isteme | Yalnız duplicate/rate/hop sınırlarıyla. |
| PROBE | Tek atlama unicast | Komşu doğrulaması isteme | Hayır. |
| PROBE_REPLY | Tek atlama unicast | PROBE'a iki yönlü doğrulama yanıtı | Hayır. |
| FAILURE_REPORT | İsteğe bağlı çok atlama | Yerel delivery failure'ı bağımsız güvenli dönüş alanı üzerinden raporlama | Yalnız kendi hedef alanının safe-successor kurallarıyla. |

`MODE_NOTICE` çekirdek mesaj değildir. `DELIVERY_FAILURE` ise ağ mesajı değil, zorunlu yerel olaydır; isteğe bağlı ağ iletisi `FAILURE_REPORT` olarak adlandırılır.

## 4. FIELD_UPDATE

### 4.1 Amaç ve kapsam

FIELD_UPDATE, bir düğümün `K=(Destination-ID,OIID)` alanı için **kendi** current potentialini veya withdrawal durumunu doğrudan komşularına ilan ettiği tek-atlama mesajdır. Hedef, `P=0` ile origin update üretir; ara düğüm kendi safe successor ve local cost hesabı değiştiğinde kendi ilanını üretir.

Gelen FIELD_UPDATE, paket düzeyinde aynen forward edilmez. Alıcı, kendi `F_i[K]` kaydını ve safe successor kararını güncellediyse ayrı bir yeni FIELD_UPDATE üretir. Böylece yayılım distance-vector gevşetmesidir; stateless flooding değildir.

### 4.2 Zorunlu alan semantiği

| Alan | Anlam |
|---|---|
| Field-Key `K` | Destination-ID ve OIID. |
| DFSN | Hedef-üretili alan turu. |
| Advertisement-Serial (ADS) | Gönderenin aynı `K` için kendi ilanlarının yerel sıra değeri; aynı DFSN içindeki potential/withdrawal sırasını belirler. |
| Advertised-Potential veya Withdrawal | Sonlu, negatif olmayan potential; withdrawal ise erişilemezliği açıkça gösterir. |
| Validity/Lifetime hint | Alıcının alan-ilanı yaşlandırmasını yapılandırmaya yardım eden profile bağımlı süre bilgisi; wire profile 100 ms kuantasında 16-bit kodlar. |

`FD_i[K]`, link maliyeti ve yerel risk gözlemleri FIELD_UPDATE ile ilan edilmez. Bunlar alıcının kendi yerel durumudur.

### 4.3 Tetikleyiciler

Bir node, aşağıdaki durumlarda kendi FIELD_UPDATE'sini üretir:

- hedef yeni OIID veya DFSN altında alan başlatır ya da yeniler;
- seçili safe successor değişir;
- kendi ilan edilecek potentiali değişir;
- local withdrawal/retraction üretir;
- soft-state yenileme politikası uyarınca mevcut field ilanını tazeler.

Update birleştirme, jitter, rate limit ve per-policy frekans timer fazında tanımlanacaktır. Semantik olarak güncel potansiyel/withdrawal değişimi saklanamaz; yalnız kısa bir birleştirme penceresinde bir araya getirilebilir.

### 4.4 Alıcı işlemi

Alıcı önce ortak zarfı, `K`, DFSN seri aritmetiğini, ADS sırasını, potential geçerliliğini ve gönderen komşu durumunu doğrular. Sonra:

1. geçerli daha yeni ADS ise `N_i[j].A_j[K]` önbelleğini günceller;
2. withdrawal ise ilanı successor adaylığından çıkarır;
3. finite ilan ise §13 feasibility ve §14 freshness koşullarıyla safe candidate değerlendirmesi yapar;
4. kendi field durumu/potential/successor değiştiyse kendi yeni FIELD_UPDATE'sini zamanlama kurallarıyla üretir.

Eşit veya eski ADS ile gelen aynı `(Sender-ID, Sender-Instance-ID, K, DFSN)` ilanı, local cache'i geriye saramaz. ADS karşılaştırması sender instance bağlamındadır; sender restartı yeni Sender-Instance-ID ile ayrılır.

## 5. FIELD_SOLICIT

### 5.1 Amaç

FIELD_SOLICIT, bir node'un doğrudan komşularından bir `K` veya bilinen Destination-ID için **mevcut geçerli alan** bilgisini istemesidir. Yeni DFSN üretimini istemez.

### 5.2 Gönderici, alıcı ve kapsam

- Gönderen: Hedef için FORWARDABLE alanı olmayan veya alan-ilanı tazeliğini yeniden edinmek isteyen node.
- Alıcı: Tek-atlama komşular.
- Kapsam: Tek atlama; alıcı mesajı forward etmez.
- Yanıt: Geçerli field bilgisi olan komşu FIELD_UPDATE gönderir. Alan yoksa sessiz kalabilir; negatif yanıt zorunlu değildir.

### 5.3 Gerekli semantik alanlar

`Destination-ID`, biliniyorsa `OIID`, bilinen son DFSN, solicit kimliği ve yanıtın hangi istek için üretildiğini bağlayan istek kimliği taşınır. İstek, requester'ın eski/stale alanını canlandırmaz.

### 5.4 Sınırlar

Aynı alan için tekrar eden solicit'ler birleştirilmeli ve rate-limited olmalıdır. FIELD_SOLICIT yanıtsız kalırsa node eski field üzerinden forwarding'e dönmez; uygun olduğunda §6'daki DFSN_REQUEST veya §16 repair/UNREACHABLE akışını kullanır.

## 6. DFSN_REQUEST

### 6.1 Amaç

DFSN_REQUEST, hedef `K` için feasible route bulunamadığında veya başlangıç alanı bulunamadığında hedefin yeni field turu üretmesini istemektir. Bu, FIELD_SOLICIT'ten farklı olarak yalnız hedefin karşılayabileceği bir taleptir.

### 6.2 Kapsam ve forwarding

İstek, data-plane successor üzerinden iletilmek zorunda değildir; forwarding için mevcut safe route bulunmayabilir. Bu nedenle yalnız kontrol düzleminde, şu sınırlarla komşular arasında yayılabilir:

- her istek benzersiz bir Request-ID taşır;
- node, aynı Request-ID'yi en fazla bir kez işler/iletir;
- istek hop-limit taşır; zamansal işlem sınırı, isteği işleyen node'un yerel `T_req_session` ve `T_req_duplicate` timerlarıyla sağlanır;
- aynı `K` için eşzamanlı istekler birleştirilebilir ve rate-limited olmalıdır;
- yalnız ACTIVE komşulara gönderilir;
- istek data forwarding veya field successor oluşturmak için kullanılamaz.

Bu kontrollü yayılım, kalıcı birincil flooding mekanizması değildir; yalnız alternatif kalmadığında ve alan gerektiğinde kullanılır.

### 6.3 Gerekli semantik alanlar

| Alan | Anlam |
|---|---|
| Destination-ID | Hedefi tanımlar. |
| Bilinen OIID ve DFSN | İstemin hangi alan bağlamından üretildiğini veya alanın bilinmediğini gösterir. |
| Requested-Minimum-DFSN | Hedefin üreteceği yeni tur için alt sınır talebi; serial aritmetik kurallarına tabidir. |
| Request-ID | Duplicate/coalescing anahtarı. |
| Hop-limit | Kontrol isteği yayılımının mekânsal kapsamını sınırlar. Zaman kapsamı wire alanı değil, yerel request-session/duplicate timerlarıdır. |
| Request reason | Alan edinimi, feasible-starvation veya freshness belirsizliği gibi yerel neden sınıfı. |

### 6.4 Hedef ve ara düğüm işlemi

- Ara düğüm geçerli, istenenden yeterince yeni alan biliyorsa ilgili FIELD_UPDATE ile yanıt verebilir; bu cevap safe-successor kabulünü alıcıda yine garanti etmez.
- İstem hedefe ulaştığında hedef, istek geçerli ve gerekli ise DFSN'yi ileri taşır ve yeni origin FIELD_UPDATE üretir. Eşdeğer istekleri tek artışta birleştirebilir.
- İstem hedefe ulaşmazsa alıcı eski/feasible olmayan route'u yeniden kullanmaz; §16 REPAIRING/UNREACHABLE davranışı sürer.

## 7. PROBE ve PROBE_REPLY

| Özellik | PROBE | PROBE_REPLY |
|---|---|---|
| Amaç | `i → j` komşuluğu için hedefli iki-yönlü kanıt istemek | Probe talebine doğrudan yanıt vermek |
| Kapsam | Tek atlama unicast | Tek atlama unicast |
| Tetikleyici | STALE/SUSPECT doğrulaması, CAUTION/PROTECT'te ek kanıt gereksinimi | Geçerli PROBE alınması |
| Gerekli bağ | Probe-ID, hedef komşu kimliği, request bağlamı | Aynı Probe-ID, yanıtlayan kimlik/instance, request bağlamı |
| Veri forwarding etkisi | Tek başına komşuyu ACTIVE yapmaz; reply ile birlikte forwarding-grade kanıt üretir | Geçerli/uyumlu reply, komşu modeline kanıt sağlar |

PROBE, hedef alan potentiali veya risk raporu taşımaz. PROBE_REPLY alınamazsa bu “jamming kanıtı” değildir; komşu yaşam döngüsü başarısızlık kanıtı olarak işlenir.

## 8. FAILURE_REPORT (isteğe bağlı)

FAILURE_REPORT, yalnız §16'da tanımlanan yerel delivery-failure olayı sonrasında ve rapor hedefi için bağımsız bir geçerli alan bulunuyorsa üretilebilir.

| Alan | Anlam |
|---|---|
| Failed Data-ID | Başarısız data paketini iliştirir. |
| Orijinal data hedefi / K | Hangi alanın başarısız olduğunu belirtir. |
| Yerel failure reason | Buffer süresi, field unreachable, doğrulama/alan hatası gibi sınıflandırılmış neden. |
| Rapor hedefi | Raporun bağımsız olarak yönlendirileceği node/uygulama uç noktası. |

FAILURE_REPORT, başarısız data yolunu tersine izleyemez ve aynı başarısız `K` alanı üzerinden rapor hedeflenemez. Rapor alanı yoksa yalnız yerel olay üretilir.

## 9. Mesaj ailesi değişim haritası

| v0 adayı | Bu tasarımdaki karşılığı | Karar durumu |
|---|---|---|
| FIELD_UPDATE | FIELD_UPDATE + açık withdrawal semantiği | Korunur, ayrıntılandırılır. |
| FIELD_REQUEST / FIELD_INITIATE | FIELD_SOLICIT ve DFSN_REQUEST olarak ayrılır | Birleştirilmiş ad kaldırılır. |
| PROBE | PROBE + PROBE_REPLY | İki-yönlü kanıt için ayrılır. |
| MODE_NOTICE | Yok | Policy onayıyla çekirdekten çıkarılmıştır. |
| DELIVERY_FAILURE | Yerel olay; isteğe bağlı FAILURE_REPORT | Ağ-geneli zorunlu mesaj olmaktan çıkarılmıştır. |

## 10. Ortak doğrulama ve hata davranışı

Bir kontrol mesajı işlenmeden önce alıcı en az şunları kontrol eder:

- desteklenen Protocol-Version ve Message-Type;
- Sender-ID/Sender-Instance-ID biçimi ve yerel komşu bağlamı;
- Message-ID/Request-ID duplicate durumu;
- zorunlu alanların varlığı, geçerli değer aralığı ve çelişkisizliği;
- `K`, OIID, DFSN ve ADS için ilgili serial/freshness kuralları;
- hop-limit ile yerel request-session/duplicate süre geçerliliği, gerektiğinde integrity/authentication profili.

Başarısız doğrulamada mesaj sessizce bırakılır ve güvenlik/diagnostic sayacı artırılabilir; hiçbir field, neighbor veya successor kaydı iyimser biçimde güncellenmez. Ayrıntılı hata davranışı ve yönetim görünürlüğü `23`, `26` ve `28`de normatifleştirilmiştir.

## 11. Gereksinim izlenebilirliği

| Mesaj/ilke | Gereksinimler |
|---|---|
| FIELD_UPDATE + withdrawal | FR-03, FR-09, FR-10, FR-13 |
| FIELD_SOLICIT | FR-03, FR-10, NFR-01 |
| DFSN_REQUEST scope/dedup | FR-03, FR-06, FR-09, FR-10, NFR-01 |
| PROBE/REPLY | FR-01, FR-07, FR-11, FR-13 |
| FAILURE_REPORT sınırı | FR-06, FR-13, NFR-01 |
| Common validation | FR-10, FR-13, FR-14, NFR-06 |

## 12. Onaylanmış control-message kararı

Önerilen çekirdek control-message ailesi şudur:

```text
FIELD_UPDATE (route + withdrawal)
FIELD_SOLICIT (one-hop existing-field inquiry)
DFSN_REQUEST (bounded new-field-turn request)
PROBE / PROBE_REPLY (one-hop neighbour verification)
FAILURE_REPORT (optional, independently routable)
```

**Kazanç:** Alan edinimi, safe recovery ve komşu doğrulamasının yetkileri ayrışır; `FIELD_REQUEST` ve `MODE_NOTICE` belirsizliği ortadan kalkar; zorunlu çok-atlama kontrol yalnız DFSN_REQUEST ile sınırlanır.

**Bedel:** FIELD_UPDATE için ADS, istek/cevap kimlikleri ve duplicate state gerekir; ilk wire format biraz daha fazla alan taşır. Ancak bu state, stale/reordered update işlemi için zaten gereklidir.

Bu seçim DL-020 ile MAJOR olarak onaylanmıştır. Wire biçimi `19`, timer yaşamı `20`/`21`, güvenlik `26` ve event handler'lar `23`tedir.
