# DESPARETE — Açık Sorular

**Durum tarihi:** 2026-09-21  
**Kural:** Bu listedeki hiçbir soru, açıkça kaydedilmiş karar veya kanıt olmadan varsayımla kapatılmaz.

## Bloke edici sorular

| Kimlik | Soru | Neden bloke edici? | Çözüm ölçütü |
|---|---|---|---|
| OQ-001 | Dinamik maliyet altında döngü özgürlüğü hangi kesin invarianta dayanacak? | Sıkı iniş, bayat ilanlara karşı tek başına yeterli değildir. | **Çözüldü:** DFSN + feasibility distance ile her successor kenarında kesin azalan feasibility invariantı onaylandı. |
| OQ-002 | Freshness/epoch yetkisi, maliyet artışı, hedef erişilemezliği, node restart ve rollover için nasıl işleyecek? | Alanın güvenli yakınsaması ve partition recovery buna bağlıdır. | **Çözüldü:** OIID + target-only DFSN + local age; ara düğüm yalnız DFSN istemi yapar, restart yeni OIID üretir, belirsiz serial kıyas fail-closed'dur. |
| OQ-003 | Bağ riski `R(i,j)` kalite, hazard ve belirsizlikten hangi anlamla üretilecek? | Risk, maliyet ve jamming kanıtını birbirine karıştırmamak gerekir. | **Tasarım düzeyinde çözüldü:** `11` O-DEL/O-AGE/O-TREND vb. kaynakları, Q/H/U anlamını ve hata modunu; M0.1 (`35`) `R=max(H,U)`, pencere ve kuantizasyonu tanımlar. Platform kalibrasyonu/deployment ayrıdır. |
| OQ-004 | Risk maliyete mi eklenmeli, aday uygunluğunu mu kısıtlamalı, yoksa ikisi de mi olmalı? | Additivite, kararlılık ve forwarding güvenliği seçime bağlıdır. | **Çözüldü:** Risk yalnız onaylı maliyet bileşenidir; ACTIVE/fresh/feasible uygunluk kapıları maliyetten bağımsızdır. |
| OQ-005 | Protokolün uygulama profili tek-sink mi, genel çok-hedef mi? | Alan durumu, mesaj maliyeti ve başarısızlık semantiği hedef sayısına bağlıdır. | **Çözüldü:** İlk operasyon profili tek-sink'tir; wire/field anahtarları gelecekte çok-hedefe genişletilebilir kalır. |

## Yüksek öncelikli sorular

| Kimlik | Soru | Gerekli çıktı |
|---|---|---|
| OQ-006 | `C_link` ile bozulma cezasının bilgi kaynakları ve ayrımı nedir? | **Tasarım düzeyinde çözüldü:** `11` kaynak/semantik ayrımını, `12` `C_quality(Q)+C_risk(R)` ayrımını, M0.1 (`35`) tamsayı dönüşümleri ve policy eşiklerini tanımlar. Göreve özgü kalibrasyon ayrı profile revizyonudur. |
| OQ-007 | NORMAL/CRISIS ikiliği yeterli mi, yoksa sürekli risk + ayrık politika seviyeleri mi daha tutarlı? | **Çözüldü:** hedef alanı başına STEADY/CAUTION/PROTECT; U önce doğrulama, bozunma+safe-alternatif PROTECT gerekçesidir. |
| OQ-008 | MODE_NOTICE kalacaksa tek-atlama kanıt mı, sınırlı duyuru mu, yoksa kaldırılacak mı? | **Çözüldü:** MODE_NOTICE çekirdekten kaldırıldı; ileride yalnız advisory, tek-atlama ve forwarding'i etkilemeyen uzantı olabilir. |
| OQ-009 | Komşu durumları hangi gözlemler ve zamanlayıcılarla değişecek; hangi durumlar forwarding'e uygundur? | **Çözüldü:** yalnız ACTIVE forwarding'e adaydır; timer mimarisi ve ilk dengeli sayısal profil onaylıdır. |
| OQ-010 | Alan başlatma için FIELD_REQUEST, FIELD_INITIATE ve olası FIELD_REPLY mesajları nasıl ayrılacak? | **Çözüldü:** FIELD_SOLICIT tek-atlama mevcut-alan sorgusu; DFSN_REQUEST sınırlı yeni-tur isteği; yanıt FIELD_UPDATE ile verilir. |
| OQ-011 | Pre-failure adaptation ile post-failure repair arasında hangi gözlemsel sınır vardır? | **Çözüldü:** successor geçerliyken risk/policy eylemi pre-failure; successor ACTIVE/safe/valid değilse repair zorunlu post-failure işlemidir. |
| OQ-012 | Alternatifler ne zaman tutulur/etkinleşir/sona erer; çoğaltma hangi garanti ile yapılır? | **Çözüldü:** opportunistic safe alternate; PROTECT + protection eligibility + finite budget ile first-hop-diverse redundancy; ilk sürümde primary + en çok bir alternate; uçtan uca ayrıklık garantisi yok. |
| OQ-013 | Bölünmede tamponlama süresi, teslim başarısızlığı ve iyileşme davranışı nedir? | **Kısmen çözüldü:** field-local REPAIRING/UNREACHABLE, local delivery-failure ve healing onaylı; UNREACHABLE yeni DATA ile re-entry yapmaz, explicit reacquire gerekir. Class-0 için 6 s buffer/10 s duplicate profili tanımlı, diğer traffic class profilleri açıktır. |
| OQ-014 | Minimum güvenlik varsayımı nedir? | Kimlik doğrulama, replay koruması ve korumayan saldırıların dürüst sınırı. | **Çözüldü:** Security Profile 1 (`26`): public-key roster, HopSignature, FIELD_UPDATE OriginSignature, DATA SourceSignature ve R1 active-peer replay sınırı. R2/persistent replay ve payload gizliliği kapsam dışıdır. |
| OQ-020 | `H_req=8`, `H_data=16` iken feasibility-starvation yaşayan uzak node target DFSN isteğini nasıl ulaştıracak? | `H_req` data çapından küçükse recovery liveness'i 8 hop ötesinde garanti edilemezdi. | **Çözüldü:** `H_req=H_data=16` onaylandı; mevcut request duplicate/rate limitleri korunur. |
| OQ-021 | Security Profile 1 hangi UAV/radyo platformunda hangi payload/roster/traffic yüküyle çalıştırılacak? | MTU, Ed25519 CPU, airtime, RAM, cache ve M0.1 link-feedback sınırları olmadan deployment/SWaP iddiası yapılamaz. | **Ertelendi:** Proje sahibi DL-041 ile platform girdisine kadar `DESIGN-ONLY` statüsünü kabul etti. Deployment için `29`daki DC-01…DC-11 yine zorunludur. |

## Gereksinim modelinde çözülmesi gerekenler

| Kimlik | Soru |
|---|---|
| OQ-015 | **Çözüldü:** G1–G14, `06`daki FR/NFR öncelikleri, çakışma ilkeleri ve kabul kanıtlarına dönüştürüldü; baseline DL-041 ile kabul edildi. |
| OQ-016 | **Çözüldü (tasarım düzeyi):** Erken uyarlama/control-load takası `06` §6, `15`, `21`, `27` ve M0.1 (`35`)de bounded evidence/budget/eşik ilkeleriyle kayıtlıdır. Göreve özgü kalibrasyon deployment profile ayrı kalır. |
| OQ-017 | **Çözüldü:** İlk operasyon profili tek-sink'tir (OQ-005); çok-hedef shared-budget profile geleceğe bırakılmıştır. |
| OQ-018 | **Çözüldü:** `16` ve `06` kapsam dışı bölümleri; DTN, sınırsız buffer, exactly-once veya uçtan uca teslim garantisi vermez. |
| OQ-019 | **Çözüldü:** `11`deki ölçüm güncelleme izleri ve `28`deki local event/counter sözleşmesi NFR-05 gözlemlenebilirliğini sağlar. |

## Açık profil kararı

| Kimlik | Soru | Neden açık? | Durum |
|---|---|---|---|
| OQ-022 | Q/H/U/R, `C_quality` ve `C_risk` dönüşümleri hangi sürümlü metric/policy profile'ında kuantize edilecek? | Deterministik implementasyon ve göreve özgü trade-off bununla belirlenir. | **Tasarım düzeyinde çözüldü:** Proje sahibi görev öncesi ortak profil + `R=max(H,U)` (A/M1) yönünü onayladı; M0.1, gözlem algoritmasını, tamsayı tabloları, policy predicate'lerini ve test vektörlerini `35`te tanımlar (DL-042). Platform kalibrasyonu/deployment yine `29`a bağlıdır. |

## Dış doğrulama gerektirenler

- **Güncellendi:** Kan vd. (2012), MGRF (2019), UAV potential-field (2024), güncel anti-jamming FANET çalışmaları ve açık patent sinyalleri `32`de yeniden incelendi. Kan'ın jamming-dynamics + proaktif multipath yaklaşımı artık açık öncül sayılır.
- **Güncellendi:** Genişletilmiş prior-art screening `32` ile yapıldı; DESPARETE için yenilik/patentlenebilirlik iddiası yasaktır. Yayın veya ticarileşme öncesi claim-level FTO/hukuk taraması yine dış uzmanlık gerektirir.
- Seçilen döngü-özgürlüğü yaklaşımının feasibility-condition ailesi ve uygulanabilirlik sınırları `13`, `24` ve RFC 7868'e bağlanmıştır. Uygulama seviyesinde edge-case trace/test gereği G-07 altında kalır.
