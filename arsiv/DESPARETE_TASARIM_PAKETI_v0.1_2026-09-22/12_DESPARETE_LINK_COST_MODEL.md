# DESPARETE — Link Maliyet Modeli

**Sürüm:** 0.1 (onaylı maliyet mimarisi; M0.1 sayısal başlangıç profili)  
**Durum:** Yönlü `C_hop+C_quality(Q)+C_risk(R)` yapısı ve maliyetten bağımsız safety gate onaylıdır. M0.1 tamsayı dönüşümleri `35`te tanımlıdır; deployment calibration ayrı kalır.  
**Tarih:** 2026-09-21

## 1. Amaç

Bu belge, `i → j` linkinin hedefe yönelik potansiyel alan hesabına nasıl maliyet kattığını tanımlar. Maliyet; gözlem, kalite, hazard, belirsizlik veya riskin eş anlamlısı değildir. Bunların yönlendirme için ortak, toplanabilir temsilidir.

Önerilen ayrım:

```text
Q(i,j): mevcut iletişim koşulu ─────► C_quality(i,j)
H(i,j), U(i,j) ─► R(i,j) ──────────► C_risk(i,j)
                                          │
Pozitif atlama tabanı ─────────────────────┤
                                          ▼
                         C(i,j) = C_hop + C_quality + C_risk
```

Bu model, kalite cezası ile geleceğe dönük/bilgi temelli ihtiyat cezasını ayrı tutar. `J(i,j)` jamming evidence'i doğrudan ayrı bir maliyet terimi değildir; aksi hâlde aynı teslim kaybı hem Q hem J üzerinden iki kez sayılabilir.

## 2. Maliyet alanı ve varsayımlar

### 2.1 Önerilen biçim

Bir `i → j` linki için:

```text
C(i,j) = C_hop + C_quality(Q(i,j)) + C_risk(R(i,j))
```

Bu denklem, sayısal ağırlık veya dönüşüm fonksiyonu atamaz. Yalnızca aşağıdaki zorunlu özellikleri koyar:

- `C_hop` tüm kullanılabilir linkler için pozitif sabittir.
- `C_quality` negatif değildir; daha kötü mevcut kalite daha düşük ceza üretemez.
- `C_risk` negatif değildir; daha yüksek risk daha düşük ceza üretemez.
- Kullanılabilir bir linkin maliyeti sonlu ve yönlüdür.
- Kullanılamayan bir link “çok pahalı” sayılarak seçilmez; forwarding aday kümesinden çıkarılır.

### 2.2 Neden pozitif atlama tabanı vardır?

Yalnız kalite/risk cezası kullanılırsa sıfır veya birbirine çok yakın maliyetli link dizileri, çok-atlamalı dolambaçların maliyet açısından ayırt edilmesini zorlaştırabilir. Pozitif `C_hop`:

- her ek atlamanın toplam maliyete bir bedel eklemesini;
- sonlu, pozitif maliyetli yolların iyi tanımlı sıralanmasını;
- eşit kalitede gereksiz uzun yolların tercihen seçilmemesini

sağlar. Bu, hop sayısını ayrıca ikinci bir rota metriği olarak eklememektir: hop etkisi yalnız `C_hop` aracılığıyla bir kez bulunur.

### 2.3 Yönlülük

`C(i,j)` ve `C(j,i)` bağımsız hesaplanır. Radyo, yük, gözlem yaşı ve risk kanıtı farklı olabileceği için simetrik maliyet varsayımı yapılmaz. Bir düğüm, kendi çıkış link maliyetini hesaplar; komşunun ilan ettiği hedef potansiyeli bu maliyetin yerine geçmez.

## 3. Uygunluk önce, maliyet sonra

Maliyet en düşük olan komşuyu otomatik olarak forwarding next hop yapmaz. Aday seçimi iki katmanlıdır:

```text
1. Güvenlik/uygunluk kapısı
   - komşu ACTIVE mi?
   - iki-yönlü forwarding-grade kanıt güncel mi?
   - hedef alanı geçerli mi?
   - komşu, seçilecek loop-free successor koşulunu sağlıyor mu?

2. Tercih
   - güvenli adaylar arasında P_d(j) + C(i,j) değeri en düşük olanı seç.
```

Bu kapı, yüksek riskin ya da CRISIS politikasının STALE/SUSPECT komşu üzerinden forwarding yapmasını önler. Risk, güvenli adaylar arasındaki maliyet/tercihi etkileyebilir; güvenlik koşulunun yerine geçemez.

## 4. Maliyet bileşenlerinin semantiği

| Bileşen | Girdi | Rol | Kesinlikle değildir |
|---|---|---|---|
| `C_hop` | Uygun linkin varlığı | Yol uzunluğunu bir kez, pozitif ve düzenli biçimde cezalandırır | Ayrı bir hop-count hedefi veya dinamik link kalitesi |
| `C_quality` | `Q(i,j)` | Şimdiki iletişim koşulunun maliyet etkisi | Hazard, bilgi yaşı veya jamming hükmü |
| `C_risk` | `R(i,j)=g(H,U)` | Bozunma eğilimi ve belirsizlik nedeniyle ihtiyat bedeli | Mevcut kaliteyi yeniden sayan ek ETX cezası |
| `J(i,j)` | Destekleyici yerel kanıt | Denetim/politika açıklaması için bağlam | Bağımsız otomatik maliyet terimi |

### 4.1 Kalite cezası

`C_quality`, Q'nun tanımlı ölçeğinden ortak maliyet alanına monoton dönüştürülür. Dönüşüm seçildiğinde şu sorular cevaplanmalıdır: ölçüm penceresi, az trafikte örnek yeterliliği, yeniden iletimin etkisi, radyo kanıtının rolü, nicemleme ve doygunluk. Bu sorular çözülmeden “ETX benzeri” ifadesi yeterli bir spesifikasyon sayılmaz.

### 4.2 Risk cezası

`C_risk`, onaylanan `R=g(H,U)` risk kestiriminden ortak maliyet alanına monoton dönüştürülür. Hazard'ın yükselmesi veya bilgi belirsizliğinin büyümesi, diğer her şey eşitken risk cezasını azaltamaz. Belirsizlik nedeniyle artan ceza, linkin fiziksel olarak kötüleştiği iddiası değildir; forwarding kararındaki ihtiyat maliyetidir.

### 4.3 Enerji ve kaynak etkisi

Enerji, bu aşamada dinamik link maliyetine dahil edilmemiştir. Sebebi, enerji ilanlarının güncelliği/güvenliği ile alan dalgalanmasını tek metrikte birleştirmenin ek karmaşıklığıdır. Bunun yerine tasarım şu asgari taahhütleri taşır:

- kontrol sıklığı ve çoğaltma etkisi NFR-02 kapsamında ayrı enerji maliyeti olarak izlenecektir;
- iki güvenli aday aynı toplam maliyetle ayrışmazsa, deterministik karar kuralından önce veya sonra enerji tercihinin kullanılıp kullanılmayacağı ayrıca kararlaştırılacaktır;
- çok düşük enerji bilgisi bir gün kullanılacaksa, ölçüm kaynağı, ilan güvenliği, yaşlanma ve hard-gate/tie-break rolü açıkça tanımlanmalıdır.

Bu, enerji farkındalığını reddetmez; onu doğrulanmamış dinamik maliyet bileşeni yapmayı erteler.

## 5. Kararlılık ve dalgalanma sınırları

Maliyet dinamik olabilir; sınırsız hızda veya gürültülü biçimde değişmemelidir.

| Kaynak | Dalgalanma riski | Bu aşamada getirilen sınır |
|---|---|---|
| Tekil teslim hatası | Anlık kayıp nedeniyle rota sıçraması | Q/H güncelleme penceresi ve komşu yaşam döngüsü ayrıdır; tek hata eğilim değildir. |
| Hazard | Kısa süreli trend gürültüsü | H yalnız ardışık kanıtla yükselir; M0.1'in üç-epoch penceresi `35`te tanımlıdır. |
| Belirsizlik | Trafik azlığında hızla yükselme | U, kaliteyi sahte biçimde kötüleştirmez; risk/politika etkisi kademeli olmalıdır. |
| Maliyet azalması | Eski iyimser alanın yayılması | Freshness ve successor koşulu çözülmeden hızlı kullanım kuralı yoktur. |
| Maliyet artması | Distance-vector count-to-infinity/döngü | Yeni epoch, feasible successor veya eşdeğer mekanizma OQ-001/OQ-002'de zorunludur. |

Metrik yumuşatma, update rate limit ve hysteresis için v0.1 başlangıç kuralları `21` ve `35`te verilmiştir. Bu belge yalnız maliyet dalgalanmasının alan güvenliğinden ayrı çözülemeyeceğini kaydeder.

## 6. Additivite ve alan hesabı koşulları

Önerilen maliyet yapısı, link maliyetleri negatif olmadığı ve `C_hop > 0` olduğu sürece hedefe ilişkin additif potansiyel hesabıyla uyumludur:

```text
P_d(i) = min_{j ∈ SafeCandidates_i[d]} [ P_d(j) + C(i,j) ]
P_d(d) = 0
```

`SafeCandidates_i[d]`, aktif komşu, geçerli alan ve feasible-successor koşullarını sağlayan aday kümesidir; bu küme `13_DESPARETE_POTENTIAL_AND_LOOP_FREEDOM.md` tarafından ayrıntılandırılır. Dinamik maliyetin yayılım ve güvenli successor semantiği olmadan kullanılması geçici döngü ya da yanlış yönlendirme üretebilir. Dolayısıyla `P_d(j) < P_d(i)` ilişkisi, successor seçildiği ve alıcının yerel potansiyelini bu ilana göre güncellediği anda sağlanan maliyet ilişkisidir; forwarding hakkını tek başına vermez. Asenkron güncellemelerde kalıcı güvenlik, potansiyel inişinden değil feasibility-distance invariantından gelir.

## 7. Eşitlik ve deterministik seçim

Güvenli adaylar arasında toplam değerler tam olarak eşitse, düğüm kararlı/deterministik bir bağ kırma kuralı kullanmalıdır. En basit aday, komşu kimliğine dayalı sabit sıralamadır.

“Yakın” fakat eşit olmayan maliyetlerde enerji veya başka ikincil metrik kullanmak için, önce maliyet nicemleme/eşdeğerlik bandı ve bunun güvenlik/kararlılık etkisi tanımlanmalıdır. Bu tanım henüz yoktur; dolayısıyla v0'daki yakın-maliyet enerji tercihi şu aşamada onaylanmamıştır.

## 8. Gereksinim izlenebilirliği

| Model unsuru | Gereksinimler |
|---|---|
| Q ve R'nin ayrı cezası | FR-02, FR-04, FR-07 |
| Pozitif/additif/yönlü maliyet | FR-03, FR-09, NFR-03 |
| Uygunluk kapısı | FR-01, FR-09, FR-11, FR-13 |
| Dalgalanma sınırları | FR-01, FR-02, FR-10 |
| Enerji kararının görünür ertelenmesi | FR-05, NFR-02 |
| Deterministik eşitlik kuralı | FR-09, NFR-06 |

## 9. Karar gerektiren mimari öneri

Öneri, üç parçalı ve additif yönlü maliyettir:

```text
C = C_hop + C_quality(Q) + C_risk(g(H,U))
```

Alternatifler:

1. `C_hop` olmadan yalnız Q/R cezası: daha az parametre içerir; fakat uzun, düşük-cezalı dolambaçları düzenli biçimde sınırlamaz.
2. Q, H, U, jamming, enerji ve diğer tüm gözlemleri tek ağırlıklı toplamda birleştirmek: tek sayı üretir; fakat çifte sayma, açıklanamaz ağırlıklar ve dalgalanma riski yüksektir.
3. R'yi sadece hard-gate yapmak: ihtiyatlıdır; ancak kalibrasyonsuz keskin eşiklerle alternatif yolları gereksiz dışlama riski taşır.

Bu yapı DL-008 ile onaylanmıştır. Risk yalnız güvenli adaylar arasında yumuşak tercihi etkiler; hard-gate rollerine komşu/alan/loop-freedom doğrulaması ayrılmıştır. DL-042 ile M0.1, `C_hop=16` ve monoton tamsayı `C_quality`/`C_risk` tablolarını `35`te tanımlar; bu seçim tek başına yeni bir safety kuralı veya deployment iddiası yaratmaz.
