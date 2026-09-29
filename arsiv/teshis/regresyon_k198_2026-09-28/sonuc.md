# Regresyon k196 → k198 · SONUÇ · 🟢 BİREBİR (ilan edilen farklar dışında)

Ajan, 28 Eylül 2026. Beklenti `beklenti.md` (koşudan önce). Çıktılar `uret.txt` (67/67 tek seferde, 31,7 dk, hata 0 — `dondur.py` artık `tests2/`yi kopyalıyor) · `karsilastir.txt` · `karsilastir_2.txt`. Kopya `arac_hash 8f099aa1…`.

- **Eski dünyanın 64 vakası birebir:** `"tekil"` yolu bayt bayt aynı. Farklar yalnız yeni alan `konfig.sonumleme_uretec = "tekil"`, köken kovaları (TÜRETİLMİŞ 65 → 67 · KAYNAK 27 → 29 · SINANMAMIŞ 44 → 42) ve kimlikler.
- ⚠️ **Önceden ilan edilmemiş fark:** `kimlik.kurulum_hash` 64 vakada. Sebep: kurulum özeti tedavi dışındaki BÜTÜN konfig alanlarını özetler, yeni alan onu değiştirir. Kanıt: k196 satırına yalnız `sonumleme_uretec = "tekil"` eklenince konfig k198'inkiyle 64/64 aynı ve yeniden hesaplanan özet 64/64 k198'dekiyle aynı. İzinle yeniden karşılaştırıldı: 🟢 (`karsilastir_2.txt`). Ders: konfig alanı eklemek her zaman `kurulum_hash`i değiştirir — beklentiye yazılmalıydı.
- **Referans dünyanın 3 vakası değişti** (ilan edilmiş, geçerli):
  | vaka | PDR (pencere) |
  |---|---|
  | `r-referans-statik-yok-dogrudan_komsu` | 0,300 → 0,111 |
  | `r-referans-statik-surekli-aodv` | 0,100 → 0,000 |
  | `r-referans-bagimsiz-surekli-dogrudan_komsu` | 0,012 → 0,011 |

## Statik vakadaki büyük fark bir kusur mu?
Hayır, ama önemli bir özellik. Statik kolda sönümleme DONUK: her bağa kalıcı tek bir Rician çekimi. Üç tohumda 780 bağın donuk kazanç dağılımı iki üreteçte aynı: ortalama 0,985–1,015, varyans 0,166–0,188 (analitik 0,174), p5 ≈ −4 dB, sistematik sapma yok. Değişen gerçekleşme: bu kısa, tek atlamalı, az akışlı koşuda kıyıdaki birkaç bağın kalıcı çekimi PDR'yi belirliyor. **Sonuç:** statik hücrelerde tohum başına sonuç sönümleme gerçekleşmesine çok duyarlı — referans dünyadaki eski U1 statik hücre sayıları (K-190/191) yeni üreteçle yeniden koşulunca değişebilir; hücre düzeyinde "düşük hücre" okumaları tohumlar arası bu varyansla birlikte okunmalı.
