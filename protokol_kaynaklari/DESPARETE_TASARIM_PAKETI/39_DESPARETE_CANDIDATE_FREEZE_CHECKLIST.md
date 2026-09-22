# DESPARETE v0.1 — Candidate-Freeze Kontrol Listesi

**Sürüm:** v0.1 freeze-readiness kontrolü  
**Durum:** Kontrol listesi hazırlanmıştır; freeze veya `DESIGN COMPLETE` kararı değildir.  
**Tarih:** 2026-09-21

## 1. Amaç ve durum dili

Bu liste, `00` §44'teki tamamlık ölçütünü uygulama öncesi/design-level kanıt ile runtime/deployment kanıtından ayırır. Bir satırın “Dokümante” olması, onun gerçek sistemde kanıtlandığı anlamına gelmez.

| Durum | Anlam |
|---|---|
| `DOKÜMANTE` | Normatif davranış, karar ve izlenebilirlik yazılıdır. |
| `DOĞRULANDI` | Fresh, denetlenebilir test/trace/ölçüm kanıtı vardır. |
| `BEKLİYOR` | İş tanımlı fakat henüz gerekli kanıt yoktur. |
| `ERTELENDİ` | Bilinçli kapsam dışı veya sonraki profile bırakılmıştır; freeze koşulunu geçersiz kılmaz. |

`DESIGN COMPLETE` yalnız tüm zorunlu satırlar `DOĞRULANDI` veya açıkça karar verilmiş `DOKÜMANTE` tasarım koşulunu karşılıyorsa ve alttaki insan kapıları kabul edildiyse kullanılabilir. `DEPLOYMENT-CAPACITY-ACCEPTED` bunun üstüne DC-01…DC-11 ölçümünü gerektirir.

## 2. Design-level candidate kontrolü

| Kimlik | Zorunlu kontrol | Mevcut durum | Kanıt / kapanış |
|---|---|---|---|
| FZ-01 | Problem, kapsam ve requirements baseline | DOKÜMANTE | `04`, `06`, DL-041. |
| FZ-02 | Terimler, kimlikler ve normatif üstünlük sırası | DOKÜMANTE | `31`, `36`. |
| FZ-03 | Neighbor, risk, cost, field, freshness ve policy semantiği | DOKÜMANTE | `10`…`15`, `35`, `36`. |
| FZ-04 | Loop-safety / FD / DFSN / failure/partition davranışı | DOKÜMANTE | `13`, `14`, `16`, `23`, `24`. |
| FZ-05 | Redundancy, control, wire, timer ve state makinesi | DOKÜMANTE | `17`…`23`. |
| FZ-06 | Security, resources, error/telemetry ve capacity gate | DOKÜMANTE | `25`…`29`. |
| FZ-07 | M0.1 metric profile, test vektörleri ve preflight | DOKÜMANTE | `34`, `35`, DL-042. |
| FZ-08 | Gereksinim izlenebilirliği, sözlük/ref denetimi ve prior-art re-audit | DOKÜMANTE | `30`…`32`. |
| FZ-09 | 17 kanonik düşünce deneyi | DOKÜMANTE | `33`; runtime kanıt değildir. |
| FZ-10 | Birleşik candidate protocol draft | DOKÜMANTE | `36`, IA-11/IA-12. |
| FZ-11 | Conformance planı ve event-trace sözleşmesi | DOKÜMANTE | `37`, `38`; test henüz çalıştırılmadı. |

## 3. Freeze öncesi insan ve belge kapıları

| Kimlik | Kontrol | Mevcut durum | Kapanış koşulu |
|---|---|---|---|
| FZ-12 | Diyagramlar metinle uyumlu | BEKLİYOR | Kullanıcının hazırladığı tüm diyagramlar, `19`…`23`, `35`, `36` ve `38`le satır/senaryo bazında eşlenir. Basitleştirilmiş eğitim diyagramı normatif ayrıntı eklemez veya değiştirmez. |
| FZ-13 | Final cross-reference ve terim taraması | BEKLİYOR | Diyagram eşlemesinden sonra `00`…`39` üzerinde mekanik referans, undefined term ve çelişki denetimi yeniden çalışır. |
| FZ-14 | Son karar günlüğü gözden geçirmesi | BEKLİYOR | Yeni MAJOR karar yoktur; değişen/ertelenen her konu `05` ve `07`yle uyumludur. |
| FZ-15 | Proje sahibi candidate-freeze onayı | BEKLİYOR | FZ-12…14 kanıtı gösterildikten sonra açık insan onayı. |

## 4. Uygulama conformance kapıları

| Kimlik | Kontrol | Mevcut durum | Kapanış koşulu |
|---|---|---|---|
| FZ-16 | Deterministic M0.1 / packet codec testleri | BEKLİYOR | `37` CT-MET-01…03 ve CT-WIRE-01…02 PASS; fresh output saklanır. |
| FZ-17 | Security, peer bootstrap ve replay trace'leri | BEKLİYOR | CT-SEC-01…03, CT-NEI-01…04 PASS; `38` negatif-event kuralları sağlanır. |
| FZ-18 | Field, FD, DFSN, repair ve partition trace'leri | BEKLİYOR | CT-FLD-01…05, CT-LOOP-01…03, CT-DFSN-01, CT-REP-01…04 PASS. |
| FZ-19 | Policy, redundancy, duplicate ve resource trace'leri | BEKLİYOR | CT-POL-01…04, CT-DATA-01…04, CT-OBS-01…02 PASS. |
| FZ-20 | 17 kanonik vaka runtime eşlemesi | BEKLİYOR | `33`teki her vaka en az bir PASS trace ile `37` CT kimliğine bağlanır. |

Bir FZ-16…20 sonucu `FAIL` veya `BLOCKED` iken `DESIGN COMPLETE` ya da deployment iddiası çıkarılamaz. Bu satırlar, test çalıştırılana kadar sırf tasarım belgeleri var diye geçilmiş sayılmaz.

## 5. Deployment kapısı — freeze'den ayrı

| Kimlik | Kontrol | Mevcut durum | Kapanış koşulu |
|---|---|---|---|
| FZ-21 | Platform/radyo kapasite kabulü | ERTELENDİ / DESIGN-ONLY | `29`daki DC-01…DC-11; MTU, payload, roster, state/cache/buffer, sign/verify, airtime, taşıyıcı ve link-feedback ölçülür. |
| FZ-22 | Uçuş/operasyon iddiası | ERTELENDİ / DESIGN-ONLY | FZ-21 geçer; ilgili görev konfigurasyonu, artefakt bütünlüğü ve test çıktıları kaydedilir. |

FZ-21/22, yazılı candidate taslağını oluşturmak için zorunlu değildir; ancak “deploy-ready”, SWaP-uygun veya operasyonel performans iddiası için zorunludur.

## 6. Freeze oturumu çıktı şablonu

Freeze değerlendirmesinde aşağıdaki formatla rapor üretilir:

```text
Status: not-ready | ready-for-owner-decision | frozen
Candidate: DESPARETE v0.1
Design gates: FZ-01...FZ-15
Implementation gates: FZ-16...FZ-20
Deployment gates: FZ-21...FZ-22
Evidence: document links, trace run IDs, test outputs, measurement artefacts
Open risks: explicit, bounded list
Need human input: only the next material decision
```

Bu belgenin hazırlanmış olması, `Status: frozen` sonucunu vermez. Mevcut durumda FZ-12…FZ-20 beklediği için status `not-ready`dir; bu, yazılı candidate taslağın yokluğu değil gerekli diyagram/runtime kanıtlarının henüz üretilmemiş olmasıdır.

## 7. İzlenebilirlik

| Konu | Birincil kaynak |
|---|---|
| Final completeness ve diagram kuralı | `00` §33, §38…§45 |
| Candidate specification | `36` |
| Conformance vaka kimlikleri | `37` |
| Trace formatı ve negatif kanıt | `38` |
| Entegrasyon ve açık kapılar | `30` |
| Deployment kapasitesi | `29` |
