# DESPARETE — Bilgi Modeli

**Sürüm:** 0.1 (onaylı bilgi ayrımları)  
**Durum:** Tazelik, loop-freedom, timer, wire ve security semantiği ilgili v0.1 belgelerde tamamlanmıştır; bu belge onların kavramsal veri ayrımını korur.  
**Tarih:** 2026-09-21

## 1. Amaç ve ilkeler

Bu belge, bir düğümün hangi bilgiyi hangi kapsamda tuttuğunu tanımlar; bit düzeyi veya handler otoritesi değildir. v0.1'in bit uzunluğu/kodlama/mesaj zorunluluğu `19`, timerları `20`/`21`, security bağları `26` ve algoritmaları `23`te kanoniktir.

Her düğüm `i` aşağıdaki ilkeleri korur:

1. Doğrudan gözlem, komşudan gelen ilan ve hedefe ait alan bilgisi ayrı kaynak türleridir.
2. Her geçici bilgi yerel alınış zamanı ve geçerlilik durumu ile tutulur; global saat senkronizasyonu varsayılmaz.
3. Bir komşunun hedefe uzaklık/potansiyel ilanı, `i → komşu` bağının kalitesi ya da riskinin kanıtı değildir.
4. Bir risk veya jamming gözlemi, kaynak düğümün yerel olgusu olarak kalır; ağ-gerçeği diye yayılmaz.
5. Veri forwarding'inde kullanılacak her kayıt, hem komşu geçerlilik hem de hedef alanı güvenlik koşulunu sağlamalıdır.

## 2. Zaman ve tazelik sözlüğü

| Terim | Anlamı | Karıştırılmaması gereken kavram |
|---|---|---|
| Yerel alınış zamanı | Düğümün bilgiyi yerel monotonic saatine göre aldığı an | Gönderenin duvar saati |
| Gözlem yaşı | Doğrudan bağ gözleminin üzerinden geçen süre | Hedef alanı yaşı |
| İlan yaşı | Komşunun hedefe ilişkin ilanının yereldeki yaşı | Bağ kalitesi yaşı |
| Alan geçerliliği | Hedef alanı kaydının versiyon ve ömür bakımından kullanılabilirliği | Komşunun menzilde olma durumu |
| Belirsizlik | Yaş, örnek yetersizliği ve çelişkiden doğan bilgi güven sınırı | Kalite/hazard |

Tazelik değerlendirmesi, yerel zamanla yapılır. Gönderici zaman damgası ileride tanımlansa bile, alıcı onu kendi geçerlilik kararının tek dayanağı yapamaz.

## 3. Yerel kalıcı kayıtlar

### 3.1 Düğüm kimlik ve oturum kaydı

| Öğeler | Amaç | Sahip / kaynak |
|---|---|---|
| Düğüm kimliği | Mesajın ve komşu kaydının kararlı eşlemesi | Yerel yapılandırma |
| Yerel yeniden başlatma/oturum belirteci | Aynı kimlikle yeniden başlayan düğümü ayırt etmeye yardımcı olmak | Yerel çalışma zamanı |
| Desteklenen protokol sürümü/yetenekleri | Uyumsuz mesajı güvenle reddetmek | Yerel yapılandırma / komşu ilanı |

v0.1'de oturum belirtecinin wire-level karşılığı 64-bit Instance-ID'dir; roster/HopSignature ve R1 binding'i `19`/`26`da tanımlıdır. Bu kayıt, bu normatif ayrımın bilgi-modeli gerekçesini görünür kılar.

### 3.2 Komşu kaydı `N_i[j]`

`N_i[j]`, yalnızca `i`'nin `j` hakkında tuttuğu yönlü yerel kayıttır.

| Alt kayıt | İçerik | Kaynak | Kullanım sınırı |
|---|---|---|---|
| Kimlik ve erişim | Komşu kimliği, son doğrudan duyulma, doğrulama durumu | Alınan çerçeve, probe/ACK sonucu | Alım, tek başına ters-yön erişilebilirlik kanıtı değildir. |
| Yaşam döngüsü | ACTIVE/STALE/SUSPECT/EXPIRED ve geçiş nedeni | Yerel komşu modeli | Veri uygunluğu doğrudan bu durumdan etkilenir. |
| Gözlem özeti | Teslim deneyi, zaman davranışı, kanal/hareket kanıtı, örnek yeterliliği | Yerel ölçüm | Ham ölçüm uzaktan gerçek sayılmaz. |
| Kestirim | `Q(i,j)`, `H(i,j)`, `U(i,j)`, `R(i,j)` ve varsa `J(i,j)` | Yerel kestirim | Maliyet/potansiyel ile özdeş değildir. |
| Hedef ilan önbelleği | `j`'nin her `d` için ilan ettiği alan sürümü/potansiyeli/advertisement seriali/alınış zamanı | Komşudan alınan geçerli alan mesajı | `i`'nin kendi alan kaydı değildir. |
| Kontrol durumu | Son probe, bekleyen doğrulama, mesaj tekrar/dedup bilgisi | Yerel kontrol düzlemi | Zamanlayıcı değerleri henüz belirlenmemiştir. |

### 3.3 Hedef alan kaydı `F_i[d]`

`F_i[d]`, `i` düğümünün hedef `d` için tuttuğu yerel yönlendirme alanı kaydıdır.

| Öğeler | Amaç | Açık bağımlılık |
|---|---|---|
| Hedef kimliği ve alan versiyonu | Alanı ve güncellik sırasını belirlemek | OQ-002: version/epoch semantiği |
| Yerel potansiyel | `i`'nin `d` için mevcut tahmini toplam maliyeti | OQ-001/OQ-004: güvenli successor ve maliyet modeli |
| Aday successor kümesi | Güvenli olabilecek komşu adayları ve bunların dayandığı ilan | OQ-001: feasibility koşulu |
| Alan durumu | Geçerli, edinim bekliyor, geçersiz veya erişilemez gibi hedef-yerel durum | Field başlatma ve partition semantiği |
| Yerel alınış/yenileme bilgisi | Alanın yaşını ve geçerliliğini değerlendirmek | OQ-002 |
| Geçersizleştirme nedeni | Versiyon değişimi, süresi dolma, doğrulama hatası, erişilemezlik | Hata ve recovery modeli |

Bir `F_i[d]` kaydının bulunması, forwarding hakkı vermez. Veri göndermek için, seçilen `N_i[j]` kaydının uygunluğu ile loop-freedom kuralının da sağlanması gerekir.

### 3.4 Paket işlem kayıtları

| Kayıt | Amaç | Sınır |
|---|---|---|
| Tekrar bastırma önbelleği | Kontrol mesajlarının ve çoğaltılmış kritik verinin yeniden işlenmesini önlemek | Anahtar, ömür ve kapasite mesaj fazında tanımlanacak. |
| Sınırlı teslim bekleme kaydı | Geçici geçersizlikte paket için sınırlı bekleme/başarısızlık akışı | DTN deposu değildir. |
| Hata kaydı | Delivery failure veya alan/komşu hata nedenini üst katmana ya da upstream'e iliştirmek | Yeni rota bilgisi olarak kullanılmaz. |

## 4. Bilgi akışı ve güven sınırları

```text
Doğrudan iletim/ölçüm ──► N_i[j].gözlem ──► Q,H,U,R,J
                                              │
Komşu alan ilanı ──────► N_i[j].alan_ilanı ──┼──► F_i[d] aday değerlendirmesi
                                              │
Hedef alan geçerliliği ───────────────────────┘
                                              ↓
               Güvenli successor + politika koşulları
                                              ↓
                                     forwarding kararı
```

Bu akışta yalnız `i`'nin doğrudan deneyimi `i → j` bağ kestirimini günceller. Komşunun kendi potansiyel ilanı, yalnız hedefe erişim adayını etkiler. Böylece bir komşunun iyimser/malicious risk bildirimi, `i`'nin bağ riskini tek başına düşüremez.

## 5. Zorunlu bilgi ayrımları

| Ayrılması gereken kayıtlar | Neden |
|---|---|
| Komşu yaşaması ↔ alan geçerliliği | Komşu mevcut olabilir ama hedef alanı bayat; ya da alan kaydı varken komşu erişilemez olabilir. |
| Gözlem yaşı ↔ ilan yaşı | Yeni komşu duyulması, eski hedef potansiyelini tazelemez. |
| Kalite/hazard ↔ belirsizlik | Sessizlik, kötü fiziksel bağın kanıtı değildir; ancak yönlendirme için güveni azaltabilir. |
| Risk ↔ jamming evidence | Risk, doğrulanmamış saldırı etiketine indirgenemez. |
| Aday successor ↔ kullanılabilir next hop | Adayın forwarding yetkisi, güvenlik ve komşu koşulları geçtikten sonra oluşur. |

## 6. Gereksinim izlenebilirliği ve açık sınırlar

Bu model FR-01, FR-04, FR-07, FR-09, FR-10, FR-11, FR-13, FR-14 ile NFR-03 ve NFR-06'yı destekler. Önceden açık olan alan versiyonu, successor safety, timer/wire biçimi ve komşu yaşam döngüsü sırasıyla `14`, `13`/`23`, `19`…`21` ve `10`/`22`de tanımlanmıştır.

M0.1 (`35`), `Q/H/U/R` ile maliyetin referans tamsayı profile bağını kapatır. `11` ve `12` semantiği sabitler; görev/platform kalibrasyonu ve M0.1'in deployment kabulü `29` kapsamında ayrı kalır.
