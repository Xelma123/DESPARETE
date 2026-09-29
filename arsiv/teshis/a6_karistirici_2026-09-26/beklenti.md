# K-176 · A6 karıştırıcı gerçekçiliği — ölçmeden ÖNCE yazılan beklenti (26 Eylül 2026)

Adım: `v2/15` A6. Anahtar `karistirici_gercekci` (varsayılan KAPALI):
1. karıştırıcı bağında hızlı sönümleme;
2. yer platformları 3 m'de, Al-Hourani yer–hava kanalı (banliyö a = 4,880, b = 0,429 — makalenin tablosundan hesaplanır);
3. reaktif sezme eşiği −90 dBm + sezme olasılığı 0,95 köken defterinde;
4. aldatıcının sahte çerçevesi boştaki alıcıyı kilitler (tembel model).

EIRP güçleri A7'de.

## 0 · Kapı sınavları (ölçüldü, `tests2/test_kosum.py` A6)
- Banliyö katsayıları 4,88 / 0,429.
- P(LoS) dört ortamda da açıyla artıyor.
- Yer karıştırıcısı yerde; ek kayıp yalnız {0,1; 21} dB.
- Karıştırıcı bağı sönümlemesi ortalamayı koruyor: 1300 örnekte ortalama 0,85–1,15, değişiyor.
- Reaktif eşik: +200 dBm'de hiç sezmiyor, −300 dBm'de ≥ %80.
- Sahte çerçeve boştaki alıcıyı kilitliyor; başı kaçırılınca ve anahtar kapalıyken kilit yok.
- Beş senaryoda tam koşuda defter kapanıyor.

## 1 · Tam takım
→ 856 + 10 (A6; biri 5 parametreli) = **866 passed**.

## 2 · Regresyon `k175 ↔ k176`
`python kalibrasyon/regresyon_satirlari.py karsilastir k175 k176 --yeni p- --izin "kimlik.kurulum_hash,konfig.karistirici_gercekci,konfig.yer_karistirici_yukseklik_m,konfig.a2g_ortam,konfig.a2g_durum_dilimi_s,konfig.reaktif_esik_dbm,konfig.reaktif_sezme_olasiligi,teshis.koken_kovalari"`
- Ortak **54/54 birebir**. Reaktif vakalar da aynı: sezme olasılığı artık konfigden (0,95) ama karşılaştırma aynı.
- Farklar yalnız: kod kimliği · `kurulum_hash` · altı yeni konfig alanı · köken kovaları (KAYNAK +2, TÜRETİLMİŞ +2, SINANMAMIŞ +2).
- Beş yeni `p-` vakası geçerli.
- Süre ~27 dk.
