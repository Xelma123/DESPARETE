# OLSR teşhisi — 2. tur sonucu (ölçümden SONRA)

> 28 Eylül 2026 · ajan · beklenti `beklenti_2.md` · çıktı `tam_2.txt`, ham `tam_2.json` · 1448 s (6 iş; dondurulmuş kopya `arac_hash` 0103fcdf…)

| öngörü | sonuç |
|---|---|
| 1 OLSR kimliği birebir | ✓ 0,5912 · 0,7953 · 0,5186 |
| 2 `rota_gecersiz` kararlarının ≥ %40'ında KENDİ bilgisinde düz yol var | ✗ sınırda: %38,5 · %40,2 · %35,8 (atlama medyan 3 · 5 · 4) |
| 2 düşüşler geçide 7–12 km'de | ✗ 13–35 km (1000: 17–26 · 1001: 26–36 · 1002: 13–16 km) — kısa pencereli duman yanıltmıştı |
| 3 `olsr_2atlama_lsym` üç tohumda da yüksek, `rota_gecersiz` ≥ %30 azalır | ✗ PDR +0,009 · −0,021 · +0,046; `rota_gecersiz` 29,0→28,5 · 9,2→11,1 · 32,7→28,4 |

**Karar kuralı (önceden yazıldı):** 3 tutmadı → aday sapma (2-atlama güncellemesinin histerezisli simetriye bağlanması) açıklama DEĞİL; OLSR bu noktada DEĞİŞMEZ. RFC'nin harfiyen okuması yine de beyan edilir (etkisi küçük ve işareti karışık).

## OLSR'ın referans dünyadaki U1-B düşüklüğü — bugünkü okuma

- **Elenen kusur adayları:** bayat rota (K1) 0 / 175 bin karar · §13'ün geri alınması RFC §13 ile §14.3'ün kendi etkileşimi · 2-atlama koşulu (yukarıda) · kuyruk/tampon düşüşü ~0.
- **Mekanizma:** geçide rota tablosu aralıklı boşalıyor (`rota_gecersiz` düşüşlerin %45–71'i); OLSR tamponlamadığı için o anda doğan paketler düşüyor. Rotasız kararların ~%36–40'ında düğümün kendi topoloji bilgisinde yol VAR ama RFC §10'un prosedürü (2-atlama kümesine dayanır, topoloji girdisini 2. atlamaya uygulamaz) onu kurmuyor; kalanında bilgi yok (%8–16'sında hiç simetrik komşu yok). Neden: HELLO histerezisli bağ algılaması 28 km'ye uzanan yayın ortamında sürekli çalkalanıyor (koşu başına ~10 bin komşu kaybı, ~300–450 bin OLSR paket kaybı, ~40 bin simetrik olmayan komşudan atılan TC).
- **Döngü:** `ttl` düşüşleri %3–6 — bağ durumu yönlendirmesinin tutarsız görünümlerde geçici döngüsü (OLSR'ın döngüsüzlük güvencesi yok).
- **§13:** referans dünyada OLSR'a ZARAR (1. tur: §13'süz +0,031 · +0,028 · +0,105).
- **Açık (K-192 (c) koşulu):** hücreleri ÖNCEDEN sıralayan bağımsız bir değişken bulunamadı (çalkantı miktarı sıralamıyor). Düşüşün yoğunlaştığı düğümün geçide uzaklığı tohuma göre değişiyor (1001'de en dıştaki düğümler, 1000/1002'de aktarıcı orta halka) — aktarıcı yükü × rota kaybı bir aday, ölçülmedi.

## 🔴 Yan bulgu — M4 boş kol kapısı gerçek protokolle KALDI

Karıştırıcısız kolda (açılma anı 150 s, hayali) OLSR'da tespit gecikmesi 3/3 tohumda SANSÜRSÜZ: 16 · 6 · 9 s (teşhis kolunda 62 · 1 · 5 s). Şok derinliği −0,088 · +0,059 · −0,078. `08` G1 kapısı kâhinle (PDR ≈ 1, kayıplar bağımsız) geçmişti; gerçek protokolde kayıp ve kopma beyanları zamanda KÜMELENİYOR — M4'ün Poisson boş hipotezi ve M1/M3'ün Agresti–Caffo hata payı paket bağımsızlığı varsayıyor. Ön-kayıt metriği → öğrenciye önerisiyle.
