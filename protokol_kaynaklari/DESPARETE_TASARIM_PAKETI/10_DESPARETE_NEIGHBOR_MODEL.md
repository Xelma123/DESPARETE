# DESPARETE — Komşu Yaşam Döngüsü Modeli

**Sürüm:** 0.1 (onaylı komşu yaşam döngüsü; bootstrap eki)  
**Durum:** Bilgi, timer, wire ve Security Profile 1 sözleşmeleriyle tutarlı. Sayısal değerler `21`dedir.  
**Tarih:** 2026-09-21

## 1. Amaç

Komşuluk, “var/yok” ikiliği değildir. Bu model, `i` düğümünün `j` komşusunu veri forwarding için ne zaman yeterince güvenilir sayacağını; ne zaman doğrulayacağını; ne zaman kullanım dışına alacağını tanımlar.

Modelin güvenlik ilkesi şudur:

> CRISIS veya başka bir politika, doğrulanmamış ya da bayat komşuyu veri forwarding için geçerli kılmaz.

Politika, daha sık gözlem/probe ve daha erken alan yenileme isteyebilir; forwarding'in temel geçerlilik koşulunu gevşetemez.

## 2. Kanıt sınıfları

| Kanıt | Sağladığı bilgi | Yeterli olmadığı sonuç |
|---|---|---|
| Pasif duyma / overhearing | `j`'nin tek yönlü olarak duyulabildiği ve zaman bilgisinin yenilenebileceği | `i → j` yönünün veri göndermeye uygun olduğu |
| Geçerli kontrol mesajı alma | Kimlik, sürüm ve muhtemel hedef-ilanı | İlan edilen potansiyelin doğru ya da taze olduğu |
| Başarılı unicast/ACK | Son `i → j` iletim deneyi başarılı | Bağın uzun süre dayanacağı |
| Başarılı probe yanıtı | Yakın zamanlı iki yönlü erişilebilirlik | Düşük hazard veya düşük risk |
| Tekrarlanan başarısız iletim | Bağ bozunması/kopması için yerel kanıt | Kesin jamming nedeni |
| Zaman aşımı | Son yeterli kanıtın yaşlandığı | Komşunun fiziksel olarak ortadan kalktığı |

## 3. Durumlar ve kullanım yetkisi

Kayıt yokken veya kayıt EXPIRED iken, yalnız rosterla doğrulanmış doğrudan peer adayı ya da bu node'a hedefli authenticated PROBE yeni **niteliksiz** kayıt açabilir. Niteliksiz kayıt forwarding'de kullanılamaz; node gecikmeden kendi outbound qualification PROBE'unu başlatır. Yeterli doğrudan/iki-yönlü kanıt alındığında ACTIVE olur. Bu yaklaşım, v0'ın dört durumlu forwarding çekirdeğini değiştirmez.

| Durum | Kesin anlam | Veri forwarding | Alan/kontrol davranışı |
|---|---|---|---|
| ACTIVE | Yakın zamanlı, forwarding-grade iki-yönlü kanıt vardır; kayıt geçerlidir. | Yalnız alan güvenliği ve politika uygunluğu da sağlanırsa aday olabilir. | Alan ilanı alınabilir/işlenebilir; normal kontrol yapılabilir. |
| STALE | Son forwarding-grade kanıtın güncelliği sona ermiştir; fiziksel kopma hükmü yoktur. | Kullanılamaz. | Saklanan ilanlar güvenilir forwarding girdisi değildir; doğrulama/probe veya alan yenileme tetiklenebilir. |
| SUSPECT | Bozunma/hata nedeniyle etkin doğrulama gereklidir. | Kullanılamaz. | Sadece sınırlı doğrulama/onarım kontrolü; yeni veri successor'ı oluşturmaz. |
| EXPIRED | Kayıt, doğrulama başarısızlığı ya da saklama süresinin dolması nedeniyle geçersizdir. | Kullanılamaz. | İlan ve aday successor'lar kaldırılır; yalnız yeni keşif kanıtı yeni niteliksiz kayıt açabilir. |

ACTIVE'in “uygun” olması, hedef alanının geçerli veya döngüsüz olduğu anlamına gelmez. Bu ayrım, komşu güveni ile yönlendirme güvenliğini birbirinden ayırır.

## 4. Geçiş modeli

```text
Niteliksiz kayıt
  │ yeterli iki-yönlü/forwarding-grade kanıt
  ▼
ACTIVE ── tazelik süresi doldu ──► STALE
  │                                    │
  │ ciddi ardışık hata /              │ doğrulama başlatıldı veya
  │ doğrulama gereksinimi              │ bağ hakkında çelişkili kanıt var
  ▼                                    ▼
SUSPECT ◄──────────────────────────────┘
  │ probe/yeniden doğrulama başarılı       │ başarısız veya saklama süresi doldu
  ▼                                        ▼
ACTIVE                                  EXPIRED
                                            │ yeni doğrudan kanıt
                                            ▼
                                     Niteliksiz kayıt
```

| Geçiş | Tetikleyici | Zorunlu yerel işlem |
|---|---|---|
| Kayıt yok / EXPIRED → Niteliksiz | Rosterla doğrulanmış doğrudan peer adayı veya bu node'a hedefli authenticated PROBE | Yeni kayıt açılır; eski ilan/AR state'i canlandırılmaz; outbound qualification PROBE planlanır. |
| Niteliksiz → ACTIVE | `i`nin başlattığı PROBE'a eşleşen, güncel PROBE_REPLY veya `i → j` yönünü doğrulayan ACK | Yaşam durumu, son forwarding-grade kanıt ve gözlem özeti güncellenir. |
| ACTIVE → STALE | Forwarding-grade tazelik süresi `T_fresh` dolar; kesin hata yoktur | Data adaylığı kaldırılır; belirsizlik yükselir; doğrulama ihtiyacı değerlendirilir. |
| ACTIVE → SUSPECT | Ardışık başarısız iletim, geçersiz/çelişkili bağ kanıtı veya açık doğrulama gereksinimi | Data adaylığı ve bu komşu üzerinden successor kullanımı askıya alınır; sınırlı probe başlatılabilir. |
| STALE → ACTIVE | Yeni forwarding-grade iki-yönlü kanıt | Yaş/belirsizlik güncellenir; alan ilanı ayrıca bağımsız doğrulanır. |
| STALE → SUSPECT | Komşu hedef için gerekliyken doğrulama başlatılması veya ek negatif kanıt | Probe/onarım işlemi ve bekleyen durum kaydı oluşturulur. |
| STALE → EXPIRED | Saklama süresi `T_retention` dolar veya açık kopma kanıtı alınır | İlan önbelleği ve successor adaylığı geçersizleştirilir. |
| SUSPECT → ACTIVE | Probe veya iki-yönlü forwarding-grade doğrulama başarıyla tamamlanır | Başarısızlık kanıtı geçmişe kaydedilir; kalite/hazard yeniden kestirilir. |
| SUSPECT → EXPIRED | Failure-bound oturum `T_probe_session`/`N_probe` ile sonlanır veya doğrulama açıkça başarısız olur | İlgili hedef adayları kullanımdan çıkarılır; gerekli ise alan yenileme/onarım tetiklenir. |
| Her durum → EXPIRED | Authenticated, yerel-linke bağlanmış kimlik/oturum çelişkisi veya doğrulanmış kopma | Durumun gerekçesi kaydedilir; mevcut ilanlar güvenilmez sayılır. Malformed/bad-signature paket tek başına bu geçişi tetiklemez. |

`T_fresh`, `T_retention`, `T_probe_start`, `T_probe_reply` ve `T_probe_session` davranışsal zaman ilişkilerini ifade eder. Başlatma/sıfırlama kuralları `20`de, sayısal başlangıç değerleri `21`de tanımlıdır.

## 5. Bozunma ve belirsizlikle etkileşim

- ACTIVE durumunda yükselen hazard, komşuyu anında EXPIRED yapmaz. Politika daha fazla gözlem, güvenli alternatife hazırlanma veya alan yenileme isteyebilir.
- ACTIVE durumunda ciddi ve tekrarlanan iletim başarısızlığı, QUALITY/Hazard güncellemesiyle birlikte SUSPECT'e geçişi gerekçelendirebilir.
- STALE, bağın kötü olduğuna değil; forwarding için yeterli kanıtın yaşlandığına işaret eder. Bu nedenle belirsizlik artar.
- SUSPECT, jamming hükmü değildir. İletim başarısızlığının sebebi kayda “bozunma/hata kanıtı” olarak geçer.
- EXPIRED kaydın yeniden etkinleşmesi, eski alan ilanını diriltmez; yeni kanıtla yeniden nitelendirme gerekir.

## 6. Policy ile etkileşim

| Politika etkisi | STEADY | CAUTION/PROTECT |
|---|---|---|
| Gözlem yoğunluğu | Mevcut geçerliliği korumaya yetecek düzey | Hazard/belirsizlik gerekçesiyle artırılabilir |
| STALE komşu | Veri için geçersiz | Veri için yine geçersiz; probe/yenileme daha erken yapılabilir |
| SUSPECT komşu | Doğrulama veya bırakma | Daha hızlı, ancak sınırlı doğrulama/onarım |
| ACTIVE alternatif | Güvenli forwarding koşulunda birincil aday olabilir | CAUTION'da hazırlık, PROTECT'te koşullu sınırlı yedeklilikte kullanılabilir |

Bu tablo, policy'nin hız ve kaynak tüketimini değiştirdiğini; geçerlilik veya loop-freedom kurallarını değiştirmediğini sabitler.

## 7. Tazelik ve alan modeliyle bağ

Komşu durum geçişleri, `F_i[d]` alan kaydında şu etkileri doğurur:

- Bir successor ACTIVE olmaktan çıktığında, ona dayanan aday forwarding için kullanılamaz.
- Bu durum alanın versiyonunu veya hedef potansiyelini otomatik olarak değiştirmez; OIID/DFSN/FD ve repair işlemi `14` ve `23`teki tanımlı kurallarla yürür.
- Güvenli alternatif successor varsa, onun seçilmesi OQ-001'de tanımlanacak feasibility koşuluna tabidir.
- Güvenli alternatif yoksa, düğüm alan yenileme/onarım akışına geçer; veri paketi sınırlı bekleme ya da başarısızlık akışını kullanır.

## 8. Gereksinim izlenebilirliği ve açık sınırlar

Model FR-01, FR-02, FR-06, FR-07, FR-08, FR-11, FR-13 ile NFR-01 ve NFR-06'yı destekler.

Bu belgedeki forwarding-grade kanıt, timer, probe, kimlik doğrulama, alan yenileme ve feasibility bağımlılıkları sırasıyla `20`/`21`, `18`/`19`, `26` ve `13`/`23`te normatifleştirilmiştir. M0.1 link sonuçları `35`te tanımlıdır; kalan deployment kapasite kanıtı `29`un DC-01…DC-11 girdilerine bağlıdır.
