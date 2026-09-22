# DESPARETE — Tasarım Paketi Dizini

**Paket türü:** V0.1 tasarım snapshot'ı  
**Hazırlanma tarihi:** 22 Eylül 2026  
**Paket durumu:** `DESIGN-ONLY`; frozen, deployment-ready veya operasyonel performans kanıtı değildir.

## 1. Paketin amacı ve sınırı

Bu klasör, DESPARETE'nin v0.1 tasarımını anlamak, gözden geçirmek ve karar vermek için gerekli tasarım belgelerini bir arada tutar. Ana proje klasöründeki kaynakların paket oluşturulduğu andaki kopyasıdır.

- Paket içindeki 39 kaynak tasarım belgesi, oluşturulurken ana klasördeki karşılıklarıyla SHA-256 düzeyinde birebir aynıydı.
- Bu index paketleme bilgisidir; yeni bir protokol kuralı, karar veya onay üretmez.
- Sonraki değişiklikler önce ana proje corpusunda yapılmalı; pakete yeniden, kontrollü biçimde yansıtılmalıdır.

## 2. Normatif okuma ve çelişki sırası

Bir davranış hakkında belgeler arasında çelişki görünürse, [birleşik candidate specification](36_DESPARETE_V0_1_CANDIDATE_SPEC.md) §1'deki sıra uygulanır:

1. [Golden rules](00_DESPARETE_GOLDEN_RULES.md), karar günlüğü ve gereksinim baseline'ı;
2. bit düzeyi wire formatı, güvenlik profili ve sayısal metrik profili;
3. timer, state machine ve algoritmalar;
4. candidate assembly ile açıklayıcı/izlenebilirlik belgeleri.

Bu paket içinde temel okuma noktası [36 — v0.1 Candidate Specification](36_DESPARETE_V0_1_CANDIDATE_SPEC.md)'dır. Bu belge tek başına yeni kural üretmez; üstteki kaynakları tek operasyon akışında birleştirir.

## 3. Önerilen okuma sırası

| Sıra | Amaç | Okunacak belge |
|---:|---|---|
| 1 | Mevcut durum, kapsam ve kabul edilmiş kararlar | [04 — Current State](04_DESPARETE_CURRENT_STATE.md), [05 — Decision Log](05_DESPARETE_DECISION_LOG.md), [06 — Requirements](06_DESPARETE_REQUIREMENTS.md), [07 — Open Questions](07_DESPARETE_OPEN_QUESTIONS.md) |
| 2 | Güncel protokolün tek parça okuması | [36 — Candidate Specification](36_DESPARETE_V0_1_CANDIDATE_SPEC.md) |
| 3 | Komşu, risk, maliyet, safety, freshness ve policy ayrıntıları | [10](10_DESPARETE_NEIGHBOR_MODEL.md)–[17](17_DESPARETE_MULTIPATH_REDUNDANCY.md) |
| 4 | Kontrol mesajları, wire, timer, state ve algoritmalar | [18](18_DESPARETE_CONTROL_MESSAGES.md)–[23](23_DESPARETE_ALGORITHMS.md) |
| 5 | Doğruluk, güvenlik, kaynak, telemetri ve kapasite sınırları | [24](24_DESPARETE_CORRECTNESS_AND_CONVERGENCE.md)–[29](29_DESPARETE_DEPLOYMENT_CAPACITY_GATE.md) |
| 6 | İzlenebilirlik, senaryo, metrik, test ve freeze | [30](30_DESPARETE_INTEGRATION_AUDIT_AND_TRACEABILITY.md)–[39](39_DESPARETE_CANDIDATE_FREEZE_CHECKLIST.md) |
| 7 | Bağımsız geliştirme önerileri | [40 — Tasarım Gözden Geçirmesi](40_DESPARETE_TASARIM_GOZDEN_GECIRME_VE_GELISTIRME_ONERILERI.md) |

Tarihsel kavram evrimini gerektiğinde [08](08_DESPARETE_CONCEPTUAL_MODEL.md), [09](09_DESPARETE_INFORMATION_MODEL.md) ve [ilk v0 taslağından](<DESPARETE – Protokol Taslağı v0.md>) takip et. Güncel davranışta `36` ve onun üstün kaynakları esas alınır.

## 4. Paket dışında, bilinçli olarak tutulan kaynaklar

Aşağıdaki dosyalar protokolün normatif davranışını tanımlayan tasarım paketine kopyalanmadı; yine de gerekçe, araştırma veya yönetim geçmişi gerektiğinde ana klasörden erişilebilir:

| Dış kaynak | Neden pakette yok? | Ne zaman okunmalı? |
|---|---|---|
| [00_MASTER_PROMPT.md](../00_MASTER_PROMPT.md) | Agent/proje yönetimi ve çalışma yönergeleri; protokol davranış spesifikasyonu değildir. | Süreç, yetki veya geçmiş çalışma bağlamı gerektiğinde. |
| [01_FANET_ROUTING_FOUNDATION.md](../01_FANET_ROUTING_FOUNDATION.md) | Problem gerekçesi ve G1–G14'ün ilk araştırma kaynağıdır; resmî baseline `06`dadır. | Gereksinimlerin bilimsel/başlangıç gerekçesi incelendiğinde. |
| [02_DESPERATE_PRIOR_ART.md](../02_DESPERATE_PRIOR_ART.md) | İlk prior-art taramasıdır; güncel sınır ve düzeltmeler paketteki `32`dedir. | Tarihsel literatür taraması veya claim geçmişi incelendiğinde. |

Bu ayrım, paketin yalnız tasarım odağını korur. Paket içindeki belgelerin bu dosyalara yaptığı atıflar kırık bağlantı değil, bilinçli olarak dışarıda tutulan provenance bağlantılarıdır.

## 5. Bilerek pakette olmayan kanıtlar

Bu klasörde aşağıdakiler bulunmaz; bunların yokluğu belge eksikliği değil, henüz üretilmemiş veya kapsam dışı artefakt anlamına gelir:

- Kullanıcının hazırladığı diyagramlar ve metin eşleme denetimi: `39` FZ-12'de bekler.
- Runtime conformance çıktıları, test runner/fixture ve event trace dosyaları: tasarım planı `37`–`38`dedir; test sonucu değildir.
- Platform MTU, ACK/retry, Ed25519 kapasitesi, RAM ve airtime ölçümleri: `29` DC-01…DC-11 kapsamında deployment öncesi kanıttır.
- Uçuş/operasyon performans veya SWaP iddiası: mevcut tasarımın kapsamı dışındadır.

## 6. Tasarım önerilerinin statüsü

[40 — Tasarım Gözden Geçirmesi](40_DESPARETE_TASARIM_GOZDEN_GECIRME_VE_GELISTIRME_ONERILERI.md), özellikle carrier/link sonucu sözleşmesi, provision edilmemiş Traffic Class, MTU preflight, DFSN advancement gate ve OIID yaşam döngüsü için öneriler içerir.

Bu öneriler kabul edilene kadar `05` karar günlüğünü veya normatif belgeleri değiştirmez. Kabul edilen her önemli öneri önce karar günlüğüne, sonra ilgili normatif belgeye ve conformance planına yansıtılmalıdır.

## 7. Hızlı durum özeti

| Alan | Durum |
|---|---|
| Yazılı v0.1 candidate tasarım | Mevcut — `36` |
| Tasarım düzeyi güvenlik/safety kaynakları | Mevcut — `13`, `14`, `23`, `24`, `26`, `35` |
| Test ve trace sözleşmesi | Mevcut; sonuçlar henüz yok — `37`, `38` |
| Freeze | Hazır değil — `39` FZ-12…FZ-20 bekliyor |
| Deployment kapasite kabulü | Ertelenmiş / `DESIGN-ONLY` — `29`, `39` FZ-21…FZ-22 |

