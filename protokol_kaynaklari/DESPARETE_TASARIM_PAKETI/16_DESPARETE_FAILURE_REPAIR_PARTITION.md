# DESPARETE — Hata, Yerel Onarım ve Partition Davranışı

**Sürüm:** 0.1 (onaylı repair/partition mimarisi)  
**Durum:** Withdrawal + bounded DFSN_REQUEST + field-local REPAIRING/UNREACHABLE ve local delivery-failure semantiği onaylıdır; timer/handler ayrıntıları `20`…`23`tedir.  
**Tarih:** 2026-09-21

## 1. Amaç ve temel ayrım

DESPARETE iki farklı davranışı ayırır:

| Davranış | Ne zaman? | Amaç |
|---|---|---|
| Pre-failure adaptation | Seçili successor hâlâ güvenli ve kullanılabilirken hazard veya ilgili bozunma kanıtı yükselir. | Güvenli alternatif varsa kopmadan önce ihtiyatlı geçişe hazırlanmak. |
| Post-failure repair | Seçili successor artık ACTIVE/safe/valid değildir ya da alan forwarding için geçersizdir. | Döngü oluşturmadan geçerli successor bulmak veya erişilemezliği açıkça ilan etmek. |

Policy postürü pre-failure davranışın yoğunluğunu değiştirir. Post-failure repair ise STEADY, CAUTION veya PROTECT fark etmeksizin safety gate tarafından zorunlu kılınan işlem akışıdır.

## 2. Hata sınıfları

| Sınıf | Yerel kanıt | Anlamı | İlk işlem |
|---|---|---|---|
| Link forwarding failure | Seçili `i → j` unicast/ACK/probe başarısızlığı veya `j`nin ACTIVE olmaktan çıkması | Seçili successor kullanılamaz olabilir. | Komşuyu SUSPECT/EXPIRED akışına sok; successor'ı askıya al. |
| Field-advertisement failure | Seçili `A_j[K]` ilanının ömrü dolar, kimlik/instance/DFSN doğrulaması başarısız olur | Link duyuluyor olsa bile hedef alan bilgisi forwarding için geçersizdir. | Bu ilandan türeyen successor'ı kaldır. |
| Feasibility failure | Mevcut/alternatif ilan, §13 koşulunu artık sağlamaz | Döngüsüz successor seçilemez. | İlanı forwarding adayından çıkar. |
| Originator/freshness failure | OIID emekli, DFSN kıyaslaması tanımsız veya alan geçersizleşmiş | Alan güvenlik bağlamı kullanılamaz. | Fail-closed; yeni alan edinimi/DFSN istemi. |
| Control-plane failure | DFSN istemi, probe veya alan edinimi sınırlı denemelerde sonuç vermez | Hedefe ilişkin güncel alan edinilemedi. | Field-local UNREACHABLE; buffer/drop politikası. |

Bu sınıfların hiçbiri tek başına “ağ tamamen bölündü” veya “jamming doğrulandı” demek değildir.

## 3. Post-failure yerel onarım işlemi

Bir düğüm `i`, alan `K` için selected successor'ını kaybettiğinde aşağıdaki sıralı işlemi atomik mantıkla uygular:

```text
1. Başarısız successor üzerinden yeni data forwarding'i durdur.
2. Kalan ACTIVE komşular içinden SafeCandidates_i[K] kümesini yeniden hesapla.
3. Safe candidate varsa deterministik en iyi successor'ı seç ve forwarding'i sürdür.
4. Safe candidate yoksa local withdrawal yap, field'i REPAIRING yap ve DFSN istemini sınırlandırılmış biçimde başlat.
5. Yeni geçerli alan gelene dek yalnız sınırlı buffer/failure akışını kullan.
```

### 3.1 Feasible alternatifle onarım

Yerel onarım, yalnız aşağıdaki aday varsa “başarılı” sayılır:

- komşu ACTIVE'dir;
- `A_j[K]` ilanı güncel/geçerli ve OIID/DFSN bağlamıyla uyumludur;
- ilan feasibility koşulunu sağlar;
- yönlü `C(i,j)` sonludur;
- aday, deterministik tercih kuralıyla seçilmiştir.

Bu koşul sağlanıyorsa `i`, yeni successor'ı seçebilir. Yeni yolun toplam potansiyeli eskisinden büyük olabilir; aynı DFSN'de `FD_i` yine de artırılmaz. Bu, “daha yüksek maliyetli ama güvenli alternatif” ile “feasible olmayan geri rota”yı ayırır.

### 3.2 Feasible alternatif yoksa withdrawal

Feasible successor kalmadığında `i`:

1. `Succ_i[K]`yi tanımsız yapar ve `P_i[K]=∞` olarak işaretler.
2. Önceki finite route'u veya stale ilanı forwarding için kullanmaz.
3. `FD_i[K]`yi aynı DFSN'de yükseltmez ya da sıfırlamaz.
4. Komşularına `K` için **withdrawal/retraction** yayımlar; bu, finite potential ilanı değildir ve successor olarak kullanılamaz.
5. Aynı alan için birleştirilmiş/rate-limited DFSN istemi başlatır.

Withdrawal, downstream düğümlerin `i`yi eski field yolu olarak tutmasını hızla bırakmalarına yardım eder. Onun wire biçimi ve tekrar sınırı control-message fazında tanımlanacaktır.

### 3.3 In-flight paket belirsizliği

Bir unicast denemesi başarısız olduğunda paketin alıcıya ulaşıp ulaşmadığı her zaman kesin değildir. DESPARETE bu nedenle exactly-once teslim garantisi vermez.

- Link katmanı kesin başarısızlık bildirirse paket, yalnız yerel queue/packet-id kuralları izin veriyorsa buffer akışına alınabilir.
- Teslimin belirsiz olduğu durumda yeniden gönderim, üst katmanın idempotency veya packet duplicate semantiğine bağlıdır.
- Yeni successor'a geçiş, paket kimliği ve bounded yeniden deneme kuralı olmadan kör yeniden iletim yapmaz.

## 4. Field-local erişilebilirlik durumları

Bu durumlar policy postürü değildir ve her `F_i[K]` kaydında tutulur.

| Field durumu | Kesin anlam | Data davranışı |
|---|---|---|
| FORWARDABLE | Seçilmiş safe successor ve geçerli alan mevcuttur. | Seçili successor'a ilet. |
| REPAIRING | Successor yoktur; withdrawal ve/veya DFSN/alan edinim işlemi sürmektedir. | Yeni data forward edilmez; uygun paket sınırlı buffer'a kabul edilebilir. |
| UNREACHABLE | Bu düğüm, bu `K` için geçerli successor edinemez; repair sınırı veya buffer şartı tamamlanmıştır. | Data forward edilmez; yeni paket kabulü trafik politikasına göre bırakılır. |

`UNREACHABLE`, `i`nin `K` hedefine mevcut güvenli alanıyla ulaşamadığı anlamına gelir. Fiziksel ağ partition'ı, hedefin kapanması veya geçici kontrol kaybı arasında kesin neden ayrımı yapmaz.

## 5. Partition davranışı

### 5.1 Yerel partition çıkarımı

`i`, yalnız şu dar sonucu çıkarabilir:

> “Bu an itibarıyla, `K` için doğrulanmış bir safe successor yok ve sınırlandırılmış alan edinimi başarılı olmadı.”

Bu durum, “tüm FANET bölündü” veya “hedef kesinlikle yok oldu” ifadesi değildir. Düğüm, alanı UNREACHABLE tutar ve eski/feasible olmayan route üzerinden denemez.

### 5.2 Buffer kabul ve sonlandırma

Buffering, DTN deposu değil onarım sırasında kısa süreli basınç sönümleyicidir.

| Kural | Semantik |
|---|---|
| Kapsam | Buffer sınırı hedef alanı ve trafik sınıfına göre uygulanır; tek alan tüm belleği tüketemez. |
| Kabul | Yalnız FORWARDABLE'dan REPAIRING'e geçişte veya REPAIRING sırasında, paket kimliği ve kaynak bütçesi uygunsa kabul edilir. |
| Sınır | Maksimum bekleme ömrü ve maksimum kuyruk payı vardır; değerler timer/resource fazında belirlenir. |
| Yeniden açılma | Yeni safe successor geldiğinde hâlâ geçerli paketler yeniden forwarding uygunluğu ile işlenir. |
| Sonlandırma | Yaş/kapasite sınırı aşılınca paket bırakılır ve yerel delivery-failure olayı üretilir. |
| Yasak | Sınırsız bekleme, eski route'a geri dönüş veya uygun olmayan komşuya “son şans” iletimi yoktur. |

### 5.3 Delivery failure kapsamı

v0'daki `DELIVERY_FAILURE` adayının çekirdek bir ağ-geneli hata mesajı olması önerilmez. Tek-sink trafik profilinde, hata oluşan düğümden kaynağa güvenli bir ters yönlendirme alanı her zaman bulunmayabilir.

Bu nedenle önerilen ayrım:

- **Zorunlu:** Paket bırakıldığında node yerel bir delivery-failure olayı ve neden kodu üretir; uygulama/taşıma katmanı bunu gözlemleyebilir.
- **İsteğe bağlı:** Ayrı ve geçerli bir dönüş/hedef alanı varsa bir `FAILURE_REPORT` kontrol mesajı üretilebilir. Bu mesajın kendi güvenli yönlendirme/ömrü olmalıdır; “başarısız data yolunu tersine izleme” varsayamaz.

Bu, bilinmeyen ters yol üzerinden hata mesajı göndererek yeni döngü veya gereksiz kontrol yükü oluşmasını önler.

## 6. Partition healing ve alan geri kazanımı

Bir `K` alanı UNREACHABLE/REPAIRING durumundan yalnız şu olaylarla FORWARDABLE'a dönebilir:

1. ACTIVE komşudan, mevcut DFSN için feasibility koşulunu sağlayan yeni/geçerli ilan alınması.
2. Hedeften veya onun alan yayılımından, tanımlı olarak daha yeni DFSN taşıyan geçerli ilan alınması.
3. Hedef restartı sonrası yeni OIID altında alanın sıfırdan kurulması.

Her durumda node, safe-successor koşulunu yeniden uygular. Sadece eski buffer paketi, eski potansiyel veya komşunun yeniden duyulması alanı tekrar FORWARDABLE yapmaz.

Partition iyileşmesinde özel bir “eski alanı canlandır” mesajı gerekmez. Geçerli field update ve gerektiğinde DFSN isteminin hedefe ulaşması, mevcut freshness/feasibility semantiğiyle alanı yeniden kurar.

## 7. Pre-failure adaptation ile etkileşim

CAUTION/PROTECT postürü, successor geçersizleşmeden önce şunları yapabilir:

- daha güncel gözlem ve hedefli doğrulama istemek;
- zaten feasible olan alternatif successor'ları izlemek;
- zorunlu olduğunda kontrollü DFSN/alan yenilemesi istemek;
- PROTECT'te kritik trafik için alternatifleri kullanmaya hazırlanmak.

Ancak hiçbir pre-failure eylem, aşağıdakileri yapamaz:

- `FD_i`yi artırmak;
- yeni DFSN üretmek;
- STALE/SUSPECT komşuyu data için kullanmak;
- feasible olmayan komşuya geri dönmek.

## 8. Düşünce deneyi iz sürmeleri

| Vaka | Beklenen davranış |
|---|---|
| Bağ kademeli bozulur | H yükselir → CAUTION → güvenli alternatif izlenir; alternatif varsa PROTECT'e koşullu geçiş, yoksa selected safe successor geçerli kaldığı sürece tek yol devam eder. |
| Bağ aniden kaybolur | Successor askıya alınır → safe alternatif varsa yerel onarım → yoksa withdrawal + DFSN istemi + REPAIRING. |
| Hiç descending/feasible komşu yok | `P=∞`, UNREACHABLE/REPAIRING; eski route veya geri yön forwarding yok. |
| Ağ bölünür | İstem hedefe ulaşamaz; buffer sınırı sonunda local delivery failure; ağ-geneli partition iddiası yok. |
| Partition iyileşir | Geçerli feasible ilan ya da yeni DFSN/OIID gelir; safe successor yeniden kurulur; geçerli buffered paketler ilerletilir. |
| Eşzamanlı maliyet artışları | Her node yalnız feasible alternatif seçer; alternatifsiz node withdraw eder/DFSN ister, kötü route'larla count-to-infinity yapmaz. |

## 9. Gereksinim izlenebilirliği

| Unsur | Gereksinimler |
|---|---|
| Pre/post-failure ayrımı | FR-02, FR-04 |
| Safe local repair ve withdrawal | FR-06, FR-09, FR-10, FR-13 |
| Field-local REPAIRING/UNREACHABLE | FR-06, FR-13, NFR-06 |
| Bounded buffer/local delivery failure | FR-06, NFR-02, NFR-03 |
| Healing kuralları | FR-01, FR-06, FR-10 |
| Optional FAILURE_REPORT sınırı | FR-13, NFR-01 |

## 10. Onaylanmış repair/partition kararı

Önerilen kararlar:

1. Alternatifsiz post-failure durumunda `withdrawal + bounded DFSN request + REPAIRING/UNREACHABLE` kullanılmalı; eski route veya feasible olmayan detour kullanılmamalıdır.
2. Partition, ağ-geneli değil field-local erişilemezlik olarak modellenmelidir.
3. `DELIVERY_FAILURE` zorunlu bir ağ-geneli mesaj değil, zorunlu yerel olay olmalıdır; ağ üzerinden `FAILURE_REPORT` yalnız bağımsız güvenli dönüş alanı varsa isteğe bağlıdır.

| Kazanç | Bedel |
|---|---|
| Döngü güvenliği repair sırasında korunur; partition davranışı dürüst ve sınırlıdır. | Bazı hatalarda kaynağa ağ üzerinden bildirim ulaşmayabilir. |
| Buffer ve kontrol yükü sınırlandırılır. | Protokol DTN veya exactly-once teslim sunmaz. |
| Tek-sink profilde olmayan ters-yol varsayımı kaldırılır. | Uygulama katmanı yerel hata gözlemlerini toplamayı tercih edebilir. |

Bu kararlar DL-016 ile MAJOR olarak onaylanmıştır. Field state, control, timer, buffering, local failure ve telemetry davranışları `18`…`23` ve `28`de normatifleştirilmiştir.
