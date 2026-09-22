# DESPARETE — Link Risk Modeli

**Sürüm:** 0.1 (onaylı risk semantiği; M0.1 sayısal başlangıç profili)  
**Durum:** `Q`nun riskten ayrı kalması ve `R=g(H,U)` yönü onaylıdır. M0.1 için `g(H,U)=max(H,U)` ve tamsayı nicemleme `35`te tanımlıdır; platform kalibrasyonu ayrı kalır.  
**Tarih:** 2026-09-21

## 1. Amaç ve kapsam

Bu model, `i → j` yönündeki bir linkin yönlendirme bakımından ne kadar ihtiyat gerektirdiğini tanımlar. Amaç jamming tespiti, tam kopma zamanı tahmini veya evrensel en iyi metrik üretmek değildir.

Model şu ayrımı korur:

```text
Doğrudan teslim kanıtı ──► mevcut kalite Q
Zamansal / hareket eğilimi ──► hazard H
Yaş / örnek yeterliliği / çelişki ──► belirsizlik U
                              H + U ──► link riski R
```

`Q`, `H`, `U`, `R` yalnız `i` tarafından `j` için üretilir. `R(i,j)` hedefe ait toplam rota riski veya ağ-geneli kriz seviyesi değildir.

## 2. Tasarım koşulları

Risk modelinin karşılaması gereken koşullar:

1. **Nedensel ihtiyat:** Kayıp veya radyo bozunması jamming olarak etiketlenmez.
2. **Yönlülük:** `i → j` ve `j → i` için ayrı kanıt tutulur.
3. **Gözlemlenebilirlik:** Her risk girdisinin ölçüm kaynağı ve geçerlilik koşulu vardır.
4. **Eksik bilgi cezası:** Yeterli kanıt yoksa sonuç “güvenli bağ” değildir; belirsizlik yükselir.
5. **Çift saymayı önleme:** Aynı kayıp örneği hem kaliteyi hem jamming evidence'i bağımsız maliyet cezası olarak iki kez ağırlaştıramaz.
6. **Açıklanabilirlik:** Bir politika değişikliği, hangi bağdaki hangi kanıta dayandığıyla izlenebilir olmalıdır.
7. **Kararlılık:** Tekil gürültülü ölçüm risk durumunu kalıcı biçimde değiştirmemelidir; M0.1'in zaman penceresi ve policy dwell kuralları `21` ve `35`te tanımlıdır. Farklı bir metrik profilinin kendi kurallarını açıkça tanımlaması gerekir.

## 3. Minimum ve isteğe bağlı gözlem seti

| Kimlik | Gözlem | Statü | Semantik gerekçe | Eksik/arıza durumu |
|---|---|---|---|---|
| O-DEL | Doğrudan unicast teslim sonucu ve yeniden iletim davranışı | Minimum | `i → j` iletiminin doğrudan yerel kanıtıdır. | Örnek azsa Q kesinleşmez, U artar. |
| O-AGE | Son forwarding-grade kanıtın yaşı | Minimum | Bilginin güncelliğini gösterir. | Zaman kaynağı bozulursa kayıt forwarding için yeterli sayılmaz. |
| O-TREND | Ardışık teslim/kalite örneklerinin eğilimi | Minimum | Kötüleşme yönüne ilişkin hazard kanıtı sağlar. | Yeterli ardışık örnek yoksa H düşük ilan edilmez; U artar. |
| O-RADIO | RSSI, SINR/SJR veya kanal meşguliyeti gibi uygun yerel radyo kanıtı | İsteğe bağlı | Teslim sonucunu bağlama oturtabilir. | Kullanılamazsa O-DEL'nin yerine geçmez; U etkisi açıkça belirtilir. |
| O-MOB | Göreli hareket/konum veya komşu değişim kanıtı | İsteğe bağlı | Bağın sürdürülebilirliğine ilişkin ek hazard kanıtı sağlayabilir. | GPS yok/bayat/çelişkiliyse hazard düşürülmez; bu kaynak devre dışı kalır ve U artabilir. |
| O-CONFLICT | Kaynaklar arası uyuşmazlık | Minimum türetilmiş | Ölçümün yorum güvenini sınırlar. | Çelişki çözülemezse U yükselir; bir kaynağa kör güvenilmez. |

O-DEL dışındaki bir gözlemin bulunmaması protokol hatası değildir. Ancak bir model, kullandığı isteğe bağlı kanıtı zorunlu gibi varsayamaz.

**M0.1 sınırı:** Bu genel model, ileri profillerin O-RADIO/O-MOB/O-CONFLICT'i açık kurallarla kullanmasına izin verir. Ancak v0.1'in M0.1 profili bu üç aileyi yalnız tanısal telemetry kabul eder; `Q/H/U/R/C` yalnız `35`teki teslim sonucu, sonuç yaşı ve örnek sayısı kurallarından türetilir.

## 4. Kalite modeli `Q(i,j)`

### 4.1 Semantik

`Q(i,j)`, ölçüm penceresindeki doğrudan `i → j` teslim deneyinin **mevcut iletişim koşulu** kestirimidir. Spesifik olarak; yeniden iletim artışı, ACK başarısızlığı veya başarısız teslimlerin kaliteyi düşüren kanıtları olabilir. Uygun radyo gözlemleri bu kestirimi açıklayabilir fakat tek başına onun yerine geçmez.

Kalite, iki görünümü saklamalıdır:

- **Güncel gözlem özeti:** En son pencerenin teslim davranışı.
- **Kestirim güveni:** Bu özetin örnek sayısı ve yaşı; `U` tarafından ayrıca temsil edilir.

Bu yapı, “ölçüm yok” durumunu yapay biçimde iyi kalite olarak yorumlamaz.

### 4.2 Zaman davranışı ve gürültü sınırı

- Kalite örnekleri yerel, sonlu bir gözlem penceresinde toplanır.
- Tek paket sonucu, ancak açık bağlantı-katmanı başarısızlığı gibi ayrı bir sert kanıt varsa yaşam döngüsünü etkiler; aksi hâlde trendi tek başına belirlemez.
- Pencere uzunluğu, örnek sayısı, olası yumuşatma tekniği ve kalite ölçeği bu belgede belirlenmemiştir.
- Yüksek trafik ile düşük trafik arasındaki örnek farkı `U` içinde görünür olmalıdır; düşük trafikli bağ daha iyi gözlenmiş sayılmaz.

### 4.3 Kalitenin kullanımı

Kalite, sonraki maliyet fazında en az bir tercih sinyali olmayı amaçlar. Tek başına kullanıcı/veri forwarding uygunluğu veya risk anlamına gelmez; komşu ve alan güvenlik koşulları bağımsızdır.

## 5. Hazard modeli `H(i,j)`

### 5.1 Semantik

`H(i,j)`, mevcut kanıt altında bağın karar ufkunda forwarding için uygunsuzlaşma **eğilimini** gösterir. Kalite düzeyi ile değil, güvenilir bir kötüleşme yönüyle artar.

Hazard kanıtı iki bağımsız aileden gelebilir:

| Aile | Örnek | Sınır |
|---|---|---|
| Teslim eğilimi | Ardışık pencerelerde bozulan teslim başarısı veya artan yeniden iletim | Tek bir anlık kayıp, eğilim değildir. |
| Sürdürülebilirlik eğilimi | Geçerli göreli hareket/menzil yaklaşımı veya komşu kararsızlığı | Hareket bilgisi kesin kopma zamanı vermez; kullanılamıyorsa tahmin yoktur. |

Bu aileler birleştirildiğinde her biri hangi alt-hazard'a katkı yaptığını korumalıdır. Birbiriyle uyumsuz kanıtlar, hazard'ı keyfî biçimde büyütmek yerine belirsizliği artırmalıdır.

### 5.2 Tahmin iddiası sınırı

Hazard, istatistiksel olarak kalibre edilmiş bir kopma olasılığı değildir. “Hazard yükseldi” cümlesi yalnız mevcut seri ve varsa hareket kanıtının ihtiyatlı eylemi gerekçelendirdiğini ifade eder. DESPARETE, bu modelle geleceği kesin bildiğini iddia etmez.

### 5.3 Hazard'ın kullanımı

Hazard artışı, yalnız güvenli ve uygun ACTIVE alternatif varsa pre-failure adaptation hazırlığını tetikleyebilir. Güvenli successor kuralının yerine geçemez; riskli bir geri dönüş veya potansiyel yükselişi meşru kılamaz.

## 6. Belirsizlik modeli `U(i,j)`

`U(i,j)`, kalite veya hazard bilgisinin güvenilir yorumlanmasını sınırlayan epistemik belirsizliktir. Aşağıdaki alt nedenleri ayırt edilmelidir:

| Alt neden | Belirsizlik etkisi | Yanlış yorumlanmaması gereken |
|---|---|---|
| Yaş | Son forwarding-grade kanıt eskidikçe artar. | Fiziksel bağın kesin kötüleştiği |
| Örnek yetersizliği | Az ya da temsil etmeyen örnekle Q/H güveni azalır. | Sıfır kaybın mükemmel kalite olduğu |
| Kaynak kullanılamazlığı | Radyo/hareket kaynağı beklenmedik biçimde yoksa yorum alanı daralır. | Kaynağın yokluğunun saldırı olduğu |
| Kaynak çelişkisi | Teslim ve radyo/mobilite kanıtı anlaşmazsa artar. | Bir kaynağın otomatik yanlış olduğu |
| Kimlik/doğrulama sorunu | Komşu/oturum bilgisi güvenilmezse artar veya kayıt reddedilir. | Normal ölçüm gürültüsü |

Belirsizlik, riskin görünür bileşeni olarak saklanmalı; risk skoru oluşturulsa bile hata ayıklama ve politika açıklaması için atılmamalıdır.

## 7. Jamming evidence `J(i,j)` ve çift sayma kuralı

`J(i,j)`, yerel bozunma örüntüsünün jamming ile uyumunu belirtir; jamming teşhisi değildir. `J` ancak en az bir ek, bağımsız veya tamamlayıcı gözlem ailesiyle birlikte yorumlanabilir. Örneğin doğrudan teslim kaybı ile kanal/radyo örüntüsünün birlikte değişmesi, yalnız kayıptan daha kuvvetli bir kanıt olabilir; yine de alternatif nedenler dışlanmış sayılmaz.

Kurallar:

- Jamming evidence ağ-geneli suçlama veya kesin `JAMMER=true` ilanına dönüşmez.
- Aynı O-DEL örneği hem Q bozulması hem bağımsız `J` cezası olarak maliyete iki kez eklenmez.
- `J` kullanılamaz veya güvenilmezse protokol Q/H/U ile bozulmaya tepki vermeye devam eder.
- `J` yalnız güvenlik/politika açıklamasını zenginleştirebilir; loop-freedom veya komşu geçerliliğini gevşetemez.

## 8. Link riski `R(i,j)`

### 8.1 Önerilen temsil

Risk, uygulama içi karşılaştırılabilir **sürekli ve yönlü bir ihtiyat indeksi** olarak temsil edilmeli; ancak onu oluşturan `H` ve `U` bileşenleri saklanmalıdır. Risk fonksiyonu şu koşulları karşılamalıdır:

```text
R(i,j) = g(H(i,j), U(i,j))

H artarsa R azalmaz.
U artarsa R azalmaz.
g, olasılık anlamı taşımaz; kalibrasyon olmadan kesin kopma olasılığı diye yorumlanmaz.
```

Bu biçim, serbest ağırlıklı “metrik yığını” yerine iki anlamlı girdiyi sınırlar. `g`'nin sayısal seçimi (ör. maksimum, çarpan, dereceli kural veya başka monoton birleşim) deployment/calibration profile'ının işidir. Hangi seçim yapılırsa yapılsın, bu bölümdeki monotonluk, olasılık iddiası yapmama ve Q'yu ikinci kez risk cezasına katmama kurallarını korumalıdır.

### 8.2 Riskin izin verilen etkileri

Risk, aşağıdakileri etkileyebilir:

- politika tarafından daha sık gözlem/probe kararı;
- güvenli ACTIVE adaylar arasında ihtiyatlı tercih;
- güvenli alternatif için pre-failure hazırlık;
- koşullu yedeklilik değerlendirmesi.

Risk şunları etkileyemez:

- EXPIRED, SUSPECT veya STALE komşuyu veri için geçerli hâle getirmek;
- loop-freedom successor koşulunu aşmak;
- jamming'e ilişkin kesin hüküm üretmek;
- hedef alanının tazelik/versiyon kontrolünü atlamak.

## 9. Güncelleme, arıza ve denetlenebilirlik

| Olay | Q | H | U | R / politika sonucu |
|---|---|---|---|---|
| Yeni yeterli doğrudan teslim örneği | Güncellenir | Eğilim geçmişiyle değerlendirilir | Örnek güveni artabilir | R yeniden hesaplanır; yalnız güvenli eylem seçilir. |
| Tekil başarısızlık | Negatif kanıt kaydedilir | Tek başına eğilim sayılmaz | Örnek bağlamına göre değişir | Ani politika değişimi zorunlu değildir. |
| Ardışık bozunma | Kötüleşir | Yükselir | Kanıt tutarlıysa azalabilir | Pre-failure değerlendirme yapılabilir. |
| Uzun sessizlik | Son Q korunabilir ama bayatlar | Yeni trend çıkarılamaz | Yükselir | Komşu STALE/SUSPECT akışına girer. |
| Sensör/GPS/radyo kaynağı kaybı | Yerine veri uydurulmaz | O aile güncellemez | Artar | Daha ihtiyatlı policy; nedensel saldırı hükmü yok. |
| Çelişkili kaynaklar | Doğrudan kanıt korunur | Keyfî yükseltilmez | Yükselir | Ek ölçüm/probe gerekebilir. |
| Açık bağlantı başarısızlığı | Negatif sonuç | Hazard/kopma kanıtı | Duruma göre | Neighbor lifecycle ve repair akışı önceliklidir. |

Her güncelleme, kullanılan gözlem aileleri, yerel zaman, geçerlilik ve değişim nedeni ile denetlenebilir olmalıdır. Bu, NFR-05'in gerektirdiği gözlemlenebilirliği destekler; deney tasarımı değildir.

## 10. Gereksinim izlenebilirliği

| Model unsuru | Gereksinimler |
|---|---|
| O-DEL/O-TREND ve Q | FR-02, FR-04, FR-07 |
| H'nin eğilim-temelli yorumu | FR-02, FR-04 |
| U'nun yaş/örnek/çelişki modeli | FR-01, FR-07, FR-11 |
| Jamming evidence sınırı | FR-07, FR-14 |
| R'nin sınırlı eylem alanı | FR-02, FR-09, FR-12 |
| Güncelleme/hata tablosu | FR-11, FR-13, NFR-05, NFR-06 |

## 11. Karar gerektiren seçenek

Bu modelin önerdiği temel seçim, riskin yalnız `H` ve `U`dan türetilmesi; `Q`nun ise mevcut link maliyet/tercih katmanında ayrı kalmasıdır. Alternatif, `Q`yu doğrudan risk fonksiyonuna katmaktır.

**Öneri:** `Q`yu risk fonksiyonuna katmamak. Düşük mevcut kalite ile geleceğe dönük/epistemik risk farklı sorunlardır; onları ayırmak çift saymayı ve açıklanamaz ağırlıklı toplamı azaltır. Bedeli, maliyet modelinin Q ile R'nin farklı rollerini açıkça bağlamasını gerektirmesidir.

Bu semantik ayrım, proje sahibinin onayıyla DL-006'da kararlaşmıştır. M0.1, DL-042 ile `g=max(H,U)`, gözlem penceresi ve nicemlemeyi `35`te referans başlangıç olarak seçer. Bu, belirli bir platform için performans veya eşik iddiası değildir; platform kalibrasyonu ve deployment kabulü `29`daki ayrı girdilere bağlıdır.
