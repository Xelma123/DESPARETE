# DESPARETE — Metrik Profili Karar Seçenekleri

**Sürüm:** 0.1 karar taslağı  
**Durum:** Karar hazırlığı tamamlandı; proje sahibi A/M1 yönünü onayladı. Seçimin normatif sayısal karşılığı `35` M0.1'dir.  
**Tarih:** 2026-09-21

## 1. Karar konusu

`11` ve `12`, yerel kalite/hazard/belirsizlik/maliyet semantiğini; `19`, potansiyelin ortak sabit-noktalı `CostQuantum` ile taşınacağını tanımlar. Ancak aşağıdaki dönüşümler için aynı sürümlü kuralın bütün forwarding düğümlerinde nasıl sağlanacağı açık değildir:

```text
Q  ─────────► C_quality(Q)
H,U ─► R=g(H,U) ─► C_risk(R)
C = C_hop + C_quality + C_risk
```

Bu, yalnız tuning tercihi değildir. Aynı FIELD_UPDATE potansiyelini iki düğüm farklı maliyet ölçeğiyle yorumlar veya üretirse, potansiyellerin karşılaştırılabilirliği kaybolur. Feasibility/FD güvenlik kapısı yine çalışsa bile, dağıtık maliyet semantiği ve rota tercihleri belirlenmiş bir protokol davranışı olmaz.

Bu karar, `29`daki cihaz kapasitesi veya uçuş performansı kabulü değildir. Platform verisi olmadan seçilen hiçbir seçenek deployment-ready, kalibre edilmiş veya optimum ilanı vermez.

## 2. Değişmeyen sınırlar

Seçenek ne olursa olsun aşağıdaki kurallar korunur:

1. `Q`, mevcut doğrudan link koşuludur; `H` bozunma eğilimi, `U` epistemik belirsizliktir. `Q`, `R`ye ikinci kez katılamaz.
2. `R=g(H,U)` her iki girdide de monoton olmalı; olasılık veya jamming teşhisi olarak yorumlanmamalıdır.
3. `C_hop > 0`; `C_quality` ve `C_risk` negatif değildir. Uygun olmayan link, yüksek sayılı maliyetle değil aday kümesinden çıkarılarak reddedilir.
4. Hesaplar yalnız sonlu tamsayılarla yapılır; 32-bit potential toplamında doygunluk `∞` ve withdrawal/repair davranışı üretir.
5. Metrik, ACTIVE, freshness veya feasible-successor güvenlik kapılarını gevşetemez.
6. Çalışan bir alan içinde maliyet profilinin sessizce değişmesi yasaktır. Bir profil değişimi ancak kontrollü, alan kayıtları temizlenmiş yeni bir operasyon bağlamında yapılabilir.

## 3. Mevcut wire sınırı

`19`daki `CostQuantum` ortak olmalıdır; fakat v0.1 packet body'de bir `MetricProfile-ID` yoktur. Mevcut `CAPABILITY` TLV'si isteğe bağlıdır ve forwarding güvenliğini değiştiremez. Bu yüzden CAPABILITY bitmap'ine profile adı koymak, uyumsuz maliyetleri güvenle engelleyen bir çözüm **değildir**.

Güvenli bir in-band kontrol istenirse, critical/core alan, kabul kuralları, signature coverage ve state-machine etkileri birlikte yeniden tasarlanmalıdır. Bu, onaylı wire profile'a MAJOR değişikliktir.

## 4. Seçenekler

| Seçenek | Yaklaşım | Kazanç | Bedel / açık risk |
|---|---|---|---|
| **A — Görev öncesi sabit ortak profil (seçildi)** | Aynı sürümlü metrik artefaktı her forwarding node'a görev öncesi yüklenir; uçuş sırasında değişmez, in-band müzakere yoktur. | Mevcut wire/security/state-machine değişmez; en küçük airtime ve doğrulama yüzeyi; tek-sink v0.1 için en basit deterministik yön. | Mismatch ancak görev öncesi konfigürasyon/admission denetimiyle yakalanır; sıcak katılım ve canlı profil değişimi desteklenmez. Sayısal M0.1 tablosu `35`te yer alır. |
| **B — Kritik in-band profil kimliği ve admission** | Profile kimliği, profile bağlı tüm field/potential bağlamına critical/core biçimde eklenir; node uyuşmazsa alanı kabul etmez veya forward etmez. | Uyuşmazlık çalışma anında görünür olur; daha heterojen filolara ve kontrollü profile geçişine zemin hazırlar. | Yeni wire sürümü/critical alan, imza kapsamı, field key, hata/telemetri ve test matrisi gerekir; header/işlem maliyeti ve bootstrap karmaşıklığı artar. |
| **C — Sayısal profili ertele (mevcut durum)** | Yalnız monotonluk ve ortak CostQuantum ilkesi korunur. | Şimdilik parametre varsayımı yapılmaz. | Referans uygulama aynı rotayı üretmek zorunda değildir; OQ-022, candidate-spec freeze ve deterministik conformance kapalı kalır. |

## 5. A seçeneğinin önerilen çerçevesi

A seçilirse aşağıdaki çerçeve normatif profile belgesine dönüştürülecektir:

- Her node aynı `Protocol-Version`, `MetricProfile-ID`, `CostQuantum`, Q/H/U ölçek tanımı, `g`, `C_hop`, `C_quality` tablosu ve `C_risk` tablosunu içeren sürümlü tek metrik artefaktını taşır.
- Operasyon öncesi admission, forwarding'e katılacak her node'da bu artefaktın aynı sürüm ve bütünlükte olduğunu doğrular. Uyuşmaz veya doğrulanmamış konfigürasyonlu node forwarding rolüne alınmaz.
- Metrik artefaktı görev boyunca sabittir. Yeni artefakt, önceki field/neighbor metric state'i temizlenip yeni operasyon bağlamı başlatılmadan etkinleşmez.
- A'nın ilk risk-birleştirme önerisi `R = max(H,U)`dur. Bu, serbest ağırlık seçmeden her iki ihtiyat kaynağının baskın etkisini korur ve monotondur. Aşırı muhafazakâr davranış veya iki kaynağın birlikte daha ağır cezalandırılması istenirse, bu seçim yeni profile revizyonu gerektirir.
- `C_quality` ve `C_risk` yalnız artan, sonlu, tamsayı lookup-table veya eşdeğer belirlenmiş tamsayı fonksiyonlarıyla hesaplanır. Eşikler, pencereler, örnek yeterliliği, taban maliyet ve doygunluk sınırları tek artefaktın açık parametreleridir; kod içinde gizli sabit olamaz.

Karar anında bu çerçeve, sayısal değer seçmek değildi. Sonraki M0.1 artefaktı `35`; 0–255 endeks yönünü, her dönüşüm tablosunu, gözlem penceresi/örnek yeterliliğini, policy predicate'lerini ve sınır test vektörlerini açıkça tanımlamıştır.

## 6. Risk-birleştirme alternatifleri

| Biçim | Davranış | Değerlendirme |
|---|---|---|
| `max(H,U)` **(A ile önerilir)** | Hazard veya belirsizlikten büyük olan ihtiyat sinyali maliyete yansır. | Ağırlık kalibrasyonu istemez; açıklaması kolaydır. İki sinyal birlikte yükseldiğinde ek sinerji vermez. |
| `sat(a×H + b×U)` | İki ihtiyat nedeni birlikte maliyeti büyütür. | Daha esnektir; ancak `a`, `b` ve doygunluk noktası için ölçümlü kalibrasyon veya ayrı insan kararı gerekir. |
| Tablo/kural matrisi | Belirli H/U bölgelerine açık policy davranışı atanır. | Açıklanabilir mission kuralı sağlayabilir; eşik çevresinde flapping/histerezis tasarımı gerekir. |

`Q`yu `g` içine alma ve serbest çok-metrikli ağırlıklı toplam seçenekleri bu belgedeki değişmeyen sınırlara aykırıdır; karar alternatifi değildir.

## 7. Karşılaştırmalı etki

| Ölçüt | A: görev öncesi sabit | B: in-band admission | C: ertele |
|---|---:|---:|---:|
| Mevcut packet formatı korunur | Evet | Hayır | Evet |
| Çalışma anında mismatch algısı | Hayır; operasyon öncesi | Evet | Hayır |
| Uçuş içi profil değişimi | Hayır | Kontrollü tasarım gerektirir | Tanımsız |
| Ek airtime / doğrulama | Yok | Vardır | Yok |
| Deterministik conformance'a ilerleme | Evet, tablo tamamlanınca | Evet, wire değişikliği tamamlanınca | Hayır |
| v0.1 sadeliği | Yüksek | Düşük | Yüksek ama eksik |

## 8. Öneri ve insan kararı sonucu

İlk v0.1 prototipi için **A seçeneğiyle birlikte `R=max(H,U)`** önerilir. Bu, onaylı wire profile'ı korur, profil uyumluluğunu görev öncesi açık bir admission sorumluluğuna bağlar ve kalibre edilmemiş ağırlıkları protokole gizlemez. Numeric tablolar sonraki, ayrı ve açık bir `Metric Profile M0` kararında verilir; o karar deployment kanıtı yerine geçmez.

Proje sahibi, 2026-09-21'de önerilen **A/M1** yönüyle devam edilmesini onayladı. Bu nedenle M0.1, `35`te ortak görev öncesi profile ve `R=max(H,U)`ye bağlanmıştır. B veya C seçeneği bu v0.1 için seçilmemiştir.

Karar anındaki seçenekler şunlardı:

1. **A/M1 — Seçildi:** görev öncesi sabit ortak profil + `R=max(H,U)`; M0 sayısal tablo profili `35`te hazırlanmıştır.
2. **B:** önce in-band kritik profile admission/wire revizyonu tasarlanır.
3. **C:** OQ-022 sayısal profile kararı ertelenir; tasarım `DESIGN-ONLY` ve freeze-preparation aşamasında kalır.

## 9. İzlenebilirlik

| Konu | Kaynak / etkilenen belge |
|---|---|
| Q/H/U/R semantiği ve monotonluk | `11`, `31` |
| Additif maliyet ve safety gate | `12`, `13`, `23` |
| Fixed-point potential, CostQuantum, TLV sınırı | `19` |
| Sayısal timer profilinin metrikten ayrı oluşu | `21` |
| Deployment/capacity kabulünün ayrı kapı oluşu | `29` |
| OQ-022 ve freeze kapısı | `07`, `30` |
