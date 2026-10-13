# DESPARETE — Potansiyel Alan ve Döngü Özgürlüğü

**Sürüm:** 0.1 (onaylı loop-freedom mimarisi)  
**Durum:** Target DFSN + FD + safe successor yönü onaylıdır; wire, timer, freshness ve algoritma ayrıntıları `14`, `19`…`24`te normatifleştirilmiştir.  
**Tarih:** 2026-09-21

## 1. Tasarım problemi

Naif Bellman–Ford alanı, dinamik maliyet artışında geçici döngü ve count-to-infinity oluşturabilir. Salt `P_next < P_current`, TTL veya komşu zaman aşımı bunu asenkron/bayat ilanlar altında kanıtlı olarak engellemez.

Bu belge, hedef-üretili sıra numarası ve feasible-successor koşulunu potansiyel alanla birleştiren bir aday sunar. Esin kaynağı, Babel'in kaynak sıra numaralarıyla genişletilmiş feasibility koşuludur; RFC 8966, koşulu sağlamayan ilanları reddetmenin döngüleri engellediğini, güvenli rota bulunamadığında ise kaynak sıra numarası istemiyle starvation'ın çözüldüğünü açıklar. DESPARETE, bu mekanizmayı kopyalamaz: kendi yönlü maliyeti, komşu yaşam döngüsü ve risk politikasıyla birleştirir. [RFC 8966](https://www.rfc-editor.org/rfc/rfc8966.html)

## 2. Alan kaynak anahtarı ve varsayımlar

Her hedef alanı için kaynak anahtarı:

```text
K = (Destination-ID, Originator-Instance-ID)
```

- `Destination-ID`, veri hedefini tanımlar.
- `Originator-Instance-ID`, hedefin bu alanı başlatan tekil çalıştırma örneğini ayırt eder.
- Aynı `K` için yalnız hedef, hedef alan sıra numarası üretebilir.
- Birden fazla bağımsız hedef aynı hizmet/prefix için alan üretirse, bunlar tek bir alanın eşdeğer kaynakları değil ayrı `K` değerleridir. Bu ilk sürüm, aynı `K` için birden çok originator'a döngü özgürlüğü garantisi vermez.

Bu varsayımlar kimlik doğrulama, node restart ve very-large rollover işleminden önce mantıksal ön koşuldur. Bu ön koşullar sağlanmazsa bu belgedeki kesin loop-freedom iddiası da sağlanmaz.

## 3. Alan değerleri

Her düğüm `i`, alan kaydı `F_i[K]` içinde aşağıdakileri tutar:

| Sembol | Ad | Anlam |
|---|---|---|
| `S_K` | Destination Field Sequence Number (DFSN) | Yalnız hedefin artırdığı alan sürümü/sıra numarası |
| `P_i[K]` | Güncel potansiyel | `i`'nin `K` hedefi için seçilmiş sonlu toplam maliyeti; erişilemezse `∞` |
| `FD_i[K] = (S_FD, M_FD)` | Feasibility distance | `i`'nin aynı alan sürümünde şimdiye dek ilan ettiği en düşük yerel potansiyel sınırı |
| `A_j[K] = (S_j, P_j)` | Komşu ilanı | `j`'nin `K` için duyurduğu alan sürümü ve potansiyeli |
| `Succ_i[K]` | Successor | Geçerli forwarding için seçilmiş, güvenli komşu; yoksa tanımsız |

`FD_i` güncel en iyi maliyet değildir. Bir düğümün maliyeti kötüleştiğinde `P_i`, `M_FD` değerinden yükselmiş olabilir; `M_FD` eski en düşük ilan sınırını korur. Bu fark, geri yönlü döngüleri önleyen bilgidir.

## 4. DFSN ve potansiyel semantiği

### 4.1 Hedef davranışı

Hedef `d`, kendi `K` alanı için `P_d[K] = 0` ilan eder. Yeni alan sürümü gerektiğinde yalnız hedef `S_K` değerini artırır ve yeni sürüm için sıfır potansiyeli yayar.

Ara düğüm, tek taraflı olarak hedef sıra numarası artıramaz. Bu kural, link maliyeti artışını “daha yeni alan” gibi göstererek döngü güvenliğini bozmasını engeller.

### 4.2 Sıra karşılaştırması

DFSN için bir toplam/seri sıralama tanımlanmalıdır. Daha sonra wire formatta sıra numarası uzunluğu, rollover eşiği ve belirsiz yarım-aralık işlemi belirtilecektir. Bu belge, karşılaştırmanın tutarlı ve rollover sırasında belirsiz olmayan olduğunu varsayar.

Bir komşu ilanı, `FD_i[K]`ye göre **feasible**dir, ancak ve ancak:

```text
S_j, S_FD'den daha yenidir;
veya
S_j = S_FD ve P_j < M_FD'dir.
```

Eşit potansiyel feasible değildir. Bu katı eşitsizlik, alanın içinde yönlü bir sıra oluşturur.

### 4.3 Yeni sürümün alınması

`i`, daha yeni `S_j` taşıyan geçerli bir ilanı aldığında, eski `K` alanını yeni DFSN bağlamına geçirir. Yeni bağlamda feasibility sınırı henüz hesaplanmamış kabul edilir; `i`, önce yeni sürümün güvenli bir successor'ını ve kendi `P_i` değerini kurar, sonra kendi ilanını yapar. Sıra numarası, aynı sürümde en düşük maliyeti seçmek için kullanılmaz; yalnız feasibility/reset kapısıdır.

## 5. Safe successor koşulu

Bir `j` komşusu, `i` için yalnız aşağıdaki koşulların **tamamı** doğruysa `Succ_i[K]` olabilir:

1. `N_i[j]` ACTIVE durumundadır ve forwarding-grade kanıtı günceldir.
2. `A_j[K]` geçerli, kimlikle ilişkilendirilmiş ve `F_i[K]`nin işlediği DFSN bağlamındadır.
3. `A_j[K]`, `FD_i[K]` koşuluna göre feasible'dir.
4. `C(i,j)` sonlu ve yönlü kullanılabilir maliyettir.
5. `i`, kendi potansiyelini atomik olarak `P_j + C(i,j)` değerine kurar; pozitif `C(i,j)` nedeniyle bu güncellenmiş yerel görünümde `P_j < P_i` olur.
6. Tüm uygun successor'lar içinde seçilen aday, en düşük sonlu toplam maliyetle; eşitlikte küçük unsigned `(Node-ID, Instance-ID)` ile deterministik seçilir (`23`).

Bir önceki successor başarısız olduğunda, yalnız bu koşulları sağlayan başka aday anında kullanılabilir. “Eski komşu beni hâlâ iyi görüyor olabilir” gerekçesiyle feasible olmayan route seçilemez.

Potansiyel inişi, successor seçimi ve ilgili potansiyel güncellemesi anındaki yerel maliyet ilişkisidir. Asenkron bir ağda komşunun gerçek-time potansiyeli, alıcının son duyduğu değerden önce değişmiş olabilir. Bu nedenle data forwarding'in kalıcı güvenlik dayanağı `P`nin anlık global inişi değil, §9'daki strictly decreasing feasibility-distance invariantıdır.

## 6. Feasibility distance güncelleme kuralları

| Olay | `P_i` | `FD_i` | Successor / ilan etkisi |
|---|---|---|---|
| Hedef alanı başlatır | `0` | `(S_K, 0)` | Hedef sıfır potansiyel ilan eder. |
| Yeni DFSN kabul edilir | Uygun komşu üzerinden yeniden hesaplanır veya `∞` | Yeni sürüm için yerel ilan sonrası `(S_K, P_i)` olur | Eski sürüm successor'ı veri için kullanılmaz. |
| Aynı DFSN'de daha düşük güvenli yol bulunur | Düşer | Yeni `P_i` daha küçükse sınır da düşer | Triggered field update yapılabilir. |
| Aynı DFSN'de maliyet artar fakat feasible alternatif vardır | Artabilir | **Artmaz**; eski en düşük sınır korunur | Yeni route yalnız feasible adayla kurulursa ilan edilir. |
| Feasible successor kalmaz | `∞` / erişilemez | **Sıfırlanmaz veya artırılmaz** | Successor kaldırılır; logical withdrawal ve yeni DFSN istemi başlar. |
| Hedeften daha yeni DFSN gelir | Yeni potansiyel hesaplanır | Yeni sürüm altında yeniden kurulur | Alan, yeni güvenlik bağlamında ilerler. |

`FD_i`nin aynı DFSN'de artırılması veya `∞`ye sıfırlanması yasaktır. Böyle bir sıfırlama, eski kötü route'ların yeniden feasible görünmesine ve count-to-infinity davranışına yol açabilir.

## 7. Maliyet değişimleri ve erişilemezlik

### 7.1 Maliyet azalması

Aktif bir komşunun ilanı feasibility koşulunu sağlıyor ve yeni toplam maliyet daha iyi ise `i`, aynı DFSN içinde güvenli olarak daha düşük potansiyele geçebilir. Yeni minimum ilan edilirse `FD_i` daraltılır.

### 7.2 Maliyet artması veya successor kaybı

`i`, sırf mevcut potansiyeli kötüleşti diye aynı DFSN'de daha kötü bir komşu ilanını kabul edemez. Önce feasible alternatifler aranır. Böyle bir alternatif yoksa `i`:

1. `Succ_i[K]`yi kaldırır ve alanı yerel olarak erişilemez sayar;
2. geçersiz potansiyeli forwarding için kullanmaz;
3. hedefe yeni DFSN isteme işlemini başlatır;
4. paketleri sadece sınırlı repair/buffer akışına sokar.

Bu tercih, kısa süreli erişilemezliği potansiyel döngüsüne göre önceler. Bedeli, hedefe ulaşılabilen yeni DFSN gelene kadar bazı güvenli olmayan ama fiziksel olarak var olabilecek detour'ların kullanılmamasıdır.

### 7.3 Bölünme ve iyileşme

Bir bölünmede DFSN isteği hedefe erişmezse, düğüm yeni sıra numarası üretmez ve geçersiz route üzerinden forwarding yapmaz. Sınırlı buffering süresi dolunca teslim başarısızlığı bildirilir. Bağlantı geri geldiğinde hedeften yayılan daha yeni DFSN, alanın güvenli biçimde yeniden kurulmasına izin verir.

## 8. DFSN istemi (semantic işlem)

Feasible route bulunmayan ve alanı hâlâ isteyen düğüm, hedefe **DFSN istemi** gönderebilir. Bu belge, istemin packet türünü, yayılım sınırını veya tekrar sayısını belirlemez; yalnız semantiğini belirler:

- İstem, `K` ve istenen en az yeni DFSN bilgisini taşır.
- Hedef geçerli bir istem aldığında DFSN'yi artırır ve yeni alan güncellemesi üretir.
- İstem, feasibility koşuluna tabi veri forwarding değildir; bu nedenle duplicate suppression ve sınırlı yaşam süresi gerektirir.
- İstem hedefe ulaşmazsa yerel node eski/feasible olmayan alanı kullanmaya geri dönmez.

Bu işlem, Babel'in güvenli olmayan route'u forwarding için kullanmadan yeni kaynak sequence isteme yaklaşımına kavramsal olarak benzer. [RFC 8966](https://www.rfc-editor.org/rfc/rfc8966.html)

## 9. Döngü özgürlüğü argümanı

### 9.1 İddianın kapsamı

Bu argüman, aynı `K` için doğru çalışan DESPARETE düğümleri arasında **veri forwarding döngüsü oluşmadığını** iddia eder. Kontrol isteği yayılımı, duplicate bastırma kuralları tanımlanmadan bu iddianın kapsamına girmez.

### 9.2 Ön koşullar

1. Her `K` için yalnız tek hedef originator DFSN üretir.
2. DFSN kıyaslaması toplam ve tutarlıdır; belirsiz rollover kabul edilmez.
3. Kullanılabilir tüm `C(i,j)` maliyetleri sonlu ve kesinlikle pozitiftir.
4. Düğümler yalnız §5'teki bütün safe-successor koşullarını sağlayan ACTIVE komşuya forwarding yapar.
5. Aynı DFSN içinde `FD_i` yalnız azalır; reset veya artış yalnız hedef-üretili daha yeni DFSN bağlamında yapılır.
6. Bir düğüm yeni DFSN'yi seçmeden ya da potansiyelini atomik güncellemeden o sürüm üzerinden veri forward etmez.

### 9.3 İnvariant

Aynı DFSN içindeki her successor kenarında `i → j` için:

```text
FD_j.metric ≤ P_j < FD_i.metric
```

İlk eşitsizlik, `FD_j`nin `j`nin şimdiye kadar ilan ettiği en düşük potansiyel olması nedeniyle; ikinci eşitsizlik `i`nin feasible koşulundan gelir. Bu nedenle feasibility distance, her successor kenarında kesin olarak hedefe doğru azalır.

Kesin azalan bir değer, sonlu bir düğüm döngüsü boyunca başlangıç değerine dönemez. Dolayısıyla aynı `K` ve DFSN bağlamındaki forwarding grafiği döngüsüzdür. Daha yeni DFSN, yalnız hedeften başlayıp yayılır; bir düğüm eski sürümdeki komşuya yeni sürümde successor olarak dönemez. Böylece sürümler arası kenarlar da döngü oluşturmaz.

### 9.4 TTL'nin rolü

TTL/hop-limit, hatalı uygulama, paket çoğaltma veya öngörülmeyen hata durumunda zarar sınırlama aracıdır. Yukarıdaki invariantın yerine geçmez ve loop-freedom kanıtında kullanılmaz.

## 10. Yakınsama, ödünler ve sınırlar

| Kazanç | Bedel / sınır |
|---|---|
| Dinamik maliyet artışında güvenli olmayan geri route reddedilir. | Güvenli fakat daha uzun yol, yeni DFSN gelene kadar geçici olarak kullanılamayabilir. |
| Yerel feasible alternatif varsa hızlı repair mümkündür. | Feasible alternatif yoksa hedeften yeni DFSN istemi gerekir. |
| Count-to-infinity yerine kontrollü geçici erişilemezlik oluşur. | Bölünmede istem hedefe ulaşamaz; protokol DTN garantisi vermez. |
| Risk/policy seçimleri safety gate'i aşamaz. | CRISIS, güvenlik uğruna anlık erişilebilirliği her zaman artıramaz. |
| Her alanın özgün source key'i vardır. | Çok-originatorlı tek alan için bu v0.1 argümanı garanti vermez. |

## 11. Tamamlanan bağımlılıklar

- DFSN bit uzunluğu, serial aritmetiği, rollover ve originator restart: `14`, `19`, `23`.
- DFSN istem sınırı, duplicate kontrolü ve hata işlemi: `18`, `20`, `23`, `28`.
- `P_i` ve `FD_i` güncelleme pseudocode'u: `23`; safety/conditional liveness argümanı: `24`.
- Withdrawal wire biçimi: `18`, `19`, `20`.
- Safe alternate/replikasyon sınırı: `17`, `23`.
- Sahte DFSN/FIELD_UPDATE tehdidi: `25`, `26`.

## 12. Onaylanmış mimari karar

**Öneri:** v0'ın tek başına epoch + `P_next < P_current` kuralı yerine, hedef-üretili DFSN + feasibility distance + safe successor + DFSN istemi mekanizması seçilsin.

| Alternatif | Artı | Eksik / maliyet |
|---|---|---|
| Salt sıkı potansiyel inişi ve TTL | En basit görünüm | Bayat/eşzamanlı ilanlarda temel loop-freedom kanıtı yoktur. |
| Hedef-üretili DFSN + feasibility (öneri) | Tek-originator alan için açık, yerel invariant; güvenli alternatifle hızlı geçiş | Geçici starvation; DFSN istemi ve source anahtarı gerektirir. |
| Diffusing computation/DUAL benzeri aktif sorgu | Daha geniş yerel onarım sağlayabilir | Mobil FANET'te daha ağır koordinasyon ve durum makinesi. |
| RPL-benzeri rank alanı | Yönlü asiklik yapı | Mevcut v0'ın dinamik DV maliyet/alan amacına doğrudan çözüm değildir; yeniden mimari gerektirir. |

Bu seçim DL-010 ile onaylanmıştır. Ana gerekçe, DESPARETE'nin hedef-yönlü dinamik maliyet alanını korurken loop-freedom'u ölçülebilir bir invariantla sağlamasıdır. Bedeli, repair/buffer modeliyle sınırlandırılan kısa süreli erişilemezliktir; bu davranış `16`, `20`…`24`te tamamlanmıştır.
