# DESPARETE — Freshness ve DFSN Yaşam Döngüsü

**Sürüm:** 0.1 (onaylı freshness mimarisi)  
**Durum:** OIID + target-only DFSN + local age ve fail-closed serial karşılaştırması onaylıdır; encoding/timer/handler ayrıntıları `19`…`23`te normatifleştirilmiştir.  
**Tarih:** 2026-09-21

## 1. Amaç

Freshness modeli, aşağıdaki bilgileri birbirinden ayırır:

```text
Originator instance  → hangi hedef çalışma örneği?
DFSN                 → bu örneğin hangi güvenlik/feasibility turu?
Potansiyel           → bu turdaki hedefe tahmini maliyet nedir?
Yerel alınış yaşı    → bu ilan yerelde ne kadar süredir görülmedi?
Komşu yaşam durumu   → ilanı taşıyan komşu forwarding için geçerli mi?
```

Bu ayrım, v0'daki “epoch + potential freshness pair” fikrini daha kesin hâle getirir: potansiyel bir tazelik etiketi değil metriktir; `(Originator-Instance-ID, DFSN)` sürüm bağlamıdır; alınış yaşı ise yerel soft-state bilgisidir.

## 2. Alan kimliği ve sürüm alanı

Her alan, aşağıdaki anahtarla tutulur:

```text
K = (Destination-ID, Originator-Instance-ID)
```

| Öğe | Üreten taraf | Değişim kuralı | Amaç |
|---|---|---|---|
| Destination-ID | Hedef yapılandırması | Hedef değişmedikçe sabit | Veri hedefini tanımlar. |
| Originator-Instance-ID (OIID) | Yalnız hedef | Hedef yeniden başladığında veya kontrollü instance rollover'da değişir; yeniden kullanılmaz. | Eski hedef çalışma örneği ile yenisini ayırır. |
| DFSN | Yalnız `K`nin hedefi | Tanımlı seri aritmetiğiyle yalnız ileri artırılır. | Feasibility starvation'ını güvenli biçimde sıfırlayan alan turunu tanımlar. |
| Potential | Her node, kendi yönlü maliyetiyle | Gerekli successor değişimlerinde güncellenir. | Hedefe tahmini toplam maliyet. |

Ara düğüm, `OIID` ya da DFSN üretmez, atlamaz veya yeniden yazar. Bu değerler güvenlik doğrulamasından önce bile yalnız hedef-kaynaklı kontrol bilgisidir; güvenlik fazı sahte kaynakların nasıl engelleneceğini tamamlayacaktır.

## 3. DFSN seri aritmetiği

DFSN, sonlu genişlikte unsigned serial alanıdır. Karşılaştırma, seçilecek bit genişliği için [RFC 1982 seri numarası aritmetiğine](https://www.rfc-editor.org/rfc/rfc1982.html) uygun yapılmalıdır:

- Hedef DFSN'yi yalnız tanımlı pozitif, sınırlı artışlarla ileri taşır; normal işlemde artış birimdir.
- Aynı `K` içindeki iki DFSN'nin karşılaştırması eşit, daha yeni, daha eski veya **tanımsız yarım-aralık** sonucu verebilir.
- Tanımsız karşılaştırma sonucu kabul, forwarding veya feasibility için kullanılamaz.
- Bit genişliği ve azami alan tutma ömrü öyle seçilmelidir ki bir kayıt tutulurken hedefin ilerlemesi yarım sıra uzayına ulaşmasın.

RFC 1982, sonlu seri alanlarında yarım-aralık ayrımının tanımsız olduğunu ve uygulamaların bu tür çiftlerin birlikte bulunmasını engellemesi gerektiğini açıkça belirtir. [RFC 1982](https://www.rfc-editor.org/rfc/rfc1982.html)

### 3.1 Tanımsız karşılaştırma güvenlik davranışı

`i`, aynı `K` için mevcut DFSN ile gelen DFSN arasındaki kıyaslama tanımsızsa:

1. Gelen ilanı field/successor için kabul etmez.
2. `K` alanını forwarding için kullanılmaz sayar.
3. Sınırlı bir yeni alan/instance yenileme isteği başlatır.
4. Doğrulanmış yeni OIID veya tanımlı olarak daha yeni DFSN gelene kadar eski alanı geri yüklemez.

Bu fail-closed davranış, seri aritmetiğinde keyfî sıra seçerek loop-freedom invariantını bozmayı engeller.

## 4. DFSN oluşturma ve ilerletme

### 4.1 Hedef başlangıcı

Hedef ilk aktif alanını yeni bir OIID ve ilk DFSN ile üretir; `P_d[K]=0` ilan eder. Yeni OIID görüldüğünde önceki OIID'ye ait tüm alanlar aynı Destination-ID için emekliye ayrılır.

### 4.2 Aynı DFSN'de yenileme

Hedef, mevcut DFSN'yi artırmadan sıfır potansiyel alan ilanını yenileyebilir. Bu yalnız soft-state tazeliğini korur; feasibility sınırını sıfırlamaz. Ara düğümler, geçerli successorları oldukça aynı DFSN'yi yeniden ilan edebilir.

### 4.3 Yeni DFSN gerektiren olaylar

Yeni DFSN, aşağıdaki olaylarda yalnız hedef tarafından üretilir:

- hedef geçerli, coalesced bir DFSN istemi alır;
- hedef kendi alanını kontrollü olarak yeniden kurmaya karar verir;
- hedef, mevcut OIID altında yeni feasibility turu gerektiğini yerel olarak belirler.

Bir link maliyeti artışı veya ara düğümde successor kaybı, ara düğüme DFSN artışı yetkisi vermez. Ara düğüm yalnız istem oluşturabilir.

## 5. Alan ilanı kabul tablosu

Bir alan ilanı, `K`, DFSN, potansiyel, gönderen kimliği ve yerel alınış bağlamı ile değerlendirilir. v0.1 bit düzeyi biçimi `19`, origin doğrulaması `26`, kabul handler'ı `23`te tanımlıdır.

| Gelen durum | Alıcı işlemi | Forwarding etkisi |
|---|---|---|
| Bilinmeyen `Destination-ID` veya biçimsel olarak geçersiz alan | Reddet, hata/dedup kaydına gerekirse not düş | Yok |
| Aynı Destination-ID, yeni ve doğrulanabilir OIID | Eski OIID alanlarını emekliye ayır; yeni `K` için kayıt kur | Eski instance üzerinden forwarding durur. |
| Emekli OIID ile gelen ilan | Reddet; emekli instance kaydını yenileme | Yok |
| Aynı `K`, daha eski DFSN | Reddet veya yalnız tekrar istatistiğine kaydet | Mevcut alanı değiştirmez. |
| Aynı `K`, eşit DFSN | Sender-instance bağlamında daha yeni Advertisement-Serial varsa komşu ilanını/yaşını yenile; eşit/eski serial cache'i geriye saramaz; potential yalnız feasibility/alan kurallarıyla değerlendirilir | Safe successor dışında değişiklik yok. |
| Aynı `K`, daha yeni DFSN | Eski successor'ı atomik olarak devreden çıkar; yeni bağlamda potential/FD'yi kur; uygun ise yeniden ilan et | Yeni bağlam kurulana dek eski sürümden data forward edilmez. |
| Aynı `K`, tanımsız DFSN karşılaştırması | §3.1 fail-closed işlemi | Yok |

v0.1'de “doğrulanabilir OIID”, target roster key'iyle doğrulanmış OriginSignature ve `23`teki kabul sırasını gerektirir. Relay'in hop doğrulaması target-origin yetkisinin yerine geçmez.

## 6. Soft-state yaşlandırma

Freshness üç bağımsız ömür kullanır; sayısal değerleri timer fazında verilecektir.

| Ömür | Başlatma / yenileme | Sona erince | Karıştırılmaması gereken |
|---|---|---|---|
| Komşu forwarding tazeliği | İki-yönlü forwarding-grade kanıt | Komşu STALE/SUSPECT olur; data adayı düşer | Alan ilanı yaşı |
| Komşu alan ilanı tazeliği | O komşudan geçerli `K` alan ilanı alınması | `A_j[K]` successor adayı olmaktan çıkar | DFSN'nin yaşı |
| Emekli instance saklama ömrü | Yeni OIID görülmesi veya eski OIID emekliye ayrılması | Kayıt, rollover güvenlik penceresinden sonra silinebilir | Hedef alanının geçerliliği |

Bir node yalnızca ACTIVE komşudan alınmış ve alan-ilanı tazelik ömrü dolmamış `A_j[K]` bilgisini successor hesabında kullanır. v0.1 DATA paketi OIID/DFSN/ADS veya advertised potential taşımaz; bu nedenle yalnız kabul edilmiş FIELD_UPDATE komşu ilanını yenileyebilir. DATA tek başına komşuyu ACTIVE yapamaz veya DFSN kaynağı kanıtı sayılmaz.

## 7. Node restart ve OIID değişimi

### 7.1 Hedef restartı

Hedef yeniden başladığında eski DFSN'yi sürdürdüğünü varsaymaz. Yeni, tekrar kullanılmayan OIID üretir ve yeni `K` altında alanı başlatır. Alıcılar:

1. Yeni instance'ı kabul ederse eski `K` successorlarını hemen kaldırır.
2. Eski OIID'yi emekli listesine ekler ve bu instance'tan geç gelen ilanları kullanmaz.
3. Yeni `K` için potential/FD'yi sıfırdan kurar.

Bu kural, hedef resetinden sonra düşük DFSN'nin eski yüksek DFSN ile yanlış kıyaslanmasını önler.

### 7.2 Ara düğüm restartı

Ara düğüm restartında tüm `N_i`, `F_i`, `FD_i`, duplicate ve buffer durumunu geçersiz sayar. Önceki DFSN veya potential değerini varsayılan doğru bilgi olarak yeniden kullanmaz. Yeni komşu/alan kanıtı edinene kadar veri forward etmez.

Ara düğümün kendi oturum belirteci değişir; komşular önceki ara düğüm ilanlarını forwarding için kullanmayı bırakır. Bu davranış, stale update'i yeni bir ara düğüm ilanı gibi değerlendirmeyi engeller.

## 8. Stale update, duplicate ve potential değişimi

- Daha eski DFSN, mevcut veya yeni alanı asla ezemez.
- Eşit DFSN ve aynı ilan içeriği idempotenttir; duplicate suppression cache yalnız trafik azaltmak içindir, correctness'in tek dayanağı değildir.
- Eşit DFSN'de potansiyel değişimi, ancak §13 feasibility ve successor kurallarıyla etkili olur.
- Ara düğüm potentialini yükseltmek, `FD_i`yi yükseltmez. Feasible alternatif yoksa logical withdrawal + DFSN istemi gerekir.
- Eski OIID'den gelen yüksek görünen DFSN, yeni OIID alanını asla ezemez; instance kimliği önce karşılaştırılır.

## 9. Maliyet değişimleri ve alan iyileşmesi

| Olay | Ara düğümün yetkisi | Sonuç |
|---|---|---|
| Yerel maliyet azalması ve feasible alternatif | Aynı DFSN'de potansiyeli düşürebilir | Yeni düşük potential ilanı ve FD güncellemesi mümkündür. |
| Yerel maliyet artması, feasible alternatif var | Aynı DFSN'de güvenli alternatife geçebilir | FD eski sınırda kalır; potansiyel artabilir. |
| Yerel maliyet artması, feasible alternatif yok | DFSN istemi yapabilir; DFSN artıramaz | Local withdrawal, sınırlı repair/buffer. |
| Partition | İstem hedefe ulaşmayabilir | Eski/uygunsuz alanla forward etmez. |
| Partition healing | Yeni alan ilanı veya DFSN istemi hedefe ulaşır | Yeni/eşit geçerli alanla güvenli yeniden kurulum. |

## 10. DFSN isteminin güvenli yaşam döngüsü

Bir DFSN istemi, veri forwarding'den ayrı kontrol işlemidir. Mesaj, wire, timer ve handler ayrıntıları `18`…`23`te normatifleştirilmiştir; aşağıdaki ilkeler onların freshness sınırını açıklar:

- İstem `K`, alıcının bilinen DFSN'si ve tekrar bastırma kimliği taşır.
- Bir node aynı istemi sınırsız iletmez; duplicate suppression ve sınırlandırılmış ömür uygular.
- Hedef, yalnız current OIID/current DFSN ile eşleşen `FEASIBLE_STARVATION` istemi `Requested-Minimum-DFSN=current+1` taşıdığında birim ileri DFSN üretir; diğer geçerli istemlerde current origin update yollar ve eşdeğer istemleri birleştirebilir.
- İstem yanıtı zaman aşımına uğrarsa node, old field'ı kullanmaya geri dönmez; partition/başarısızlık akışına devam eder.
- DFSN istemi için olası kontrol döngüsü, data-plane loop-freedom iddiasına dahil değildir; ayrı duplicate ve hop-limit işlemleri zorunludur.

## 11. Gereksinim izlenebilirliği

| Unsur | Gereksinimler |
|---|---|
| OIID + DFSN ayrımı | FR-09, FR-10, FR-13 |
| Serial aritmetik ve fail-closed kıyaslama | FR-09, FR-10, NFR-06 |
| Target-only DFSN yetkisi | FR-09, FR-10, FR-14 |
| Soft-state ayrımları | FR-01, FR-06, FR-11 |
| Restart/healing işlemleri | FR-06, FR-10, FR-13 |
| İstem duplicate/lifetime kuralı | FR-03, FR-10, FR-13, NFR-01 |

## 12. Onaylanmış freshness kararı

**Öneri:** Epoch terminolojisi, `OIID + DFSN + yerel alınış yaşı` modeliyle değiştirilsin. Hedef restartında yeni OIID üretilsin; ara düğüm DFSN artıramasın; seri karşılaştırması tanımsızsa fail-closed davranılsın.

Alternatifler:

| Alternatif | Sorun |
|---|---|
| Sadece hedef epoch'u | Hedef restartı, rollover ve eski instance replay'i ayırt edilemez. |
| Her ara düğümün epoch artırması | Tek originator sequence invariantını ve feasibility güvenliğini bozar. |
| Salt yerel zaman damgası | Saat senkronizasyonu ve replay/yeni bilgi ayrımını güvenle çözmez. |
| OIID + DFSN + local age (öneri) | Daha fazla state gerektirir; fakat restart, ordering ve soft-state kavramlarını ayrıştırır. |

Bu karar DL-012 ile MAJOR olarak onaylanmıştır. OIID 64-bit, DFSN 32-bit ve ilgili timer profili `19`…`21`de seçilmiştir; OIID üretimindeki platforma özgü entropy/kalıcı-state yöntemi security/deployment profile'ının sorumluluğundadır.
