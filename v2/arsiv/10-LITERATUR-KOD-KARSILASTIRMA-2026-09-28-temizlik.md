# 10 — LİTERATÜR BULGULARI (taramanın projeye verdiği)

> **Güncel:** 25 Eylül 2026 — öz sürüm. Yalnız hâlâ geçerli **literatür** tarafı kaldı. 1 Eylül'deki tam belge (emekli `sim/` koduyla karşılaştırma tabloları §2 · §4 · §7b · §8, iddia envanteri, yöntem) `v2/arsiv/10-LITERATUR-KOD-KARSILASTIRMA-2026-09-01.md`; oradaki kod sayıları `sim2/` için geçerli DEĞİL.
> **Kaynak:** `protokol_kaynaklari/literatur_taramasi_2026-08-31/` (20 dosya, 5 271 satır). İlk okuma %62 kapsamdaydı ve bu yazılmamıştı (öğrencinin sorusuyla yakalandı); ikinci turda tamamı okundu (§7c). **Kural:** "literatür şunu diyor" cümlesi hangi dosyanın hangi örneklemden söylediği yazılmadan kurulmaz; hiçbir literatür sayısı projeye ölçülmeden alınmaz.

---

## 3 · Literatür kendi içinde çelişiyor

Aynı taramanın iki dosyası aynı parametreye farklı değer veriyor: koşu süresi medyan ~200 s (100–600 s; dosya 6, 13 makale) ↔ 900–1000 s (dosya 16) · bit hızı 1–2 ↔ 2 Mb/s · menzil 200–550 ↔ ~250 m · paket 512 B baskın · tekrar 10 tohum asgari. Kaynakların kendi varyansı projenin kaynaktan sapmasından büyük. MobiHoc bildirilerinin %87,8'i güven aralığı raporlamamış (dosya 4 §9.1).

## 5 · Boşluk A ve adlandırılmış protokoller

Dosya 2'nin boşluk metni: *"2022–2026 FANET literatüründe OLSR, AODV ve GPSR için değişen SJR altında doğrudan raporlanmış PDR ve E2E gecikme düşüş yüzdeleri bulunamamıştır."* 🔒 **Karar (K-081, 1 Eylül): A-tam** — AODV · OLSR · AOMDV adlarıyla kurulur, GPSR kapsam dışı. Özgünlük öğrencinin protokolünden gelir ve o protokol standart protokollerle karşılaştırılır; rakipleri SJR ekseninde ölçmek Boşluk A'yı yan ürün olarak doldurur — GPSR olmadığı için **kısmen**, ve bu açıkça yazılır.

## 6 · Literatürün doğruladıkları

- **6.1 Soyutlama seviyesi:** SINR → BER → PER → Bernoulli (dosya 10'un "Seviye 3", "en yaygın ve en titiz"); parça başına (chunk) PER dâhil. `sim2/` bu seviyede.
- **6.2 Kâhin yasağı dış kaynaklı:** dosya 14 §7.1 — *"karıştırıcı gücü, konumu veya etki yarıçapı yalnızca simülatör motoru tarafından bilinir; ajan bunlara erişemez."* Projenin gözlem sözleşmesiyle (`05`) aynı.
- **6.3** Literatürün ajandan istediği tahmin girdileri (ACK/NACK'ten PER, dinlemeyle girişim) gözlem yüzeyinde var (`05`).
- **6.4** Tablo tabanlı öğrenme yeni bağımlılık istemez (derin öğrenme yasağı buna değmez); DESPARETE Q-öğrenme değildir.
- **6.5** `01`'in boşluk iddiası dosya 17'nin 11 protokollük matrisiyle bağımsız doğrulandı: "açık karıştırma" terimi 9 protokolde yok.
- **6.6** Ön-kayıt yöntemi ADEMP-PreReg (Siepe vd. 2024) çerçevesiyle örtüşüyor; iki yerde proje daha güçlü: Holm (Bonferroni yerine) · hash tabanlı kanal çekimi ortak rastgele sayıların desenkronizasyonunu yapısal olarak önler.

## 7 · Literatürün meydan okudukları — bugünkü durum

| # | konu | durum (`sim2/`) |
|---|---|---|
| 1–2 | 3B geometri · 3B Gauss-Markov mobilite | 🟢 var |
| 3 | adlandırılmış protokoller | 🟢 AODV · OLSR · AOMDV |
| 4 | istatistik katmanı | 🔴 yok — Aşama 4 (`analiz/`) |
| 5 | PSR (*"PDR tek başına yanıltıcıdır"*) | 🟢 öğrencinin tanımıyla |
| 6 | gecikme yüzdelikleri + IPDV (RFC 7679) | 🟢 |
| 7 | rota kurtarma gecikmesi Δ ve COR | 🟢 |
| 8 | SJR raporlama ekseni | 🟡 ρ ve güç raporlanıyor |
| 9–10 | paket 512 B · 2 Mb/s | 🟢 |
| 11 | gölgeleme | 🟢 |
| 12–13 | çoklu karıştırıcı · sınıf taksonomisi | 🟢 beş sınıf + beş aile (dar bant ve ton temsil edilmez, beyanlı) |
| 14 | kontrol kanalı karıştırması (~20 dB daha J/S-verimli) | ⚪ protokol farkında karıştırıcı yok (`07` §05) |

## 7c · İkinci okuma turunun bulguları

- **Y-1 🔴 Literatürün kendi ödül formülü kâhin içeriyor** (dosya 14): §7.1 yasaklarken §5.7'nin `1{d(j,J) ≤ R_J}` terimi ve §11.1'in referans kodu (`in_jamming_radius`, `sinr`, `jsr` simülatörden) kâhin kullanıyor. O kod kopyalanmaz; yalnız §7 (ρ PER sapmasından tahmin) uygulanabilir.
- **Y-2** `01`'in "Table 26" iddiası yeniden doğrulanamadı (MDPI tam metni erişilemedi; protokol sayıları uyuşmuyor). **Karar (öğrenci, 1 Eylül):** özgünlük iddiası dosya 17'nin yeniden üretilebilir matrisine dayanır; B7 `02`de "yeniden doğrulanamadı" durumunda kalır.
- **Y-3** Literatür 2B mobiliteyi "yaygın hata" sayıyor (dosya 16 §12); `sim2/` 3B. Isınma, tekrar, log-mesafe, DCF maddeleri de karşılanıyor.
- **Y-4 🔴 Asgari bağımlı değişken kümesi** (dosya 4 §11): PDR + PSR · D̄ ve p95 · O_pkt ve NRL · üç kopma sayacı · Δ ve COR. 🟢 `sim2/` hepsini üretiyor. Aynı bölümün istatistik şartları (hücre başına ≥ 20 tekrar, açık tohumlar, %95 GA) ana deneyde (40 tohum) karşılanıyor.
- **Y-5** Sağlamlık testi 1 (statik, bağlı → PDR ≈ 1) kâhinle geçiyor; taban protokollerde U1 bunun karşılığı.
- **Y-6** AODV'nin literatürdeki birincil çöküş mekanizması (mobilite → kopma → RREQ seli; `T_link ≥ T_RTT` şartı) statik kurguda oluşamazdı; `sim2/`nin hareketli kolları bunu içeriyor. Statik kolda kopma yalnız karıştırmadan gelir — iddia bu sınırla yazılır.
- **Y-7** Karıştırıcı sayısı/konumu ayrı eksen olmalı ({1 merkez, 1 kenar, 3 dağıtık}) → `sim2/`de beş tehdit ailesi (`07` §05). Düğüm sayısı ekseni {10, 25, 50}: `sim2/`de N = 40 sabit (C1, K-125).
