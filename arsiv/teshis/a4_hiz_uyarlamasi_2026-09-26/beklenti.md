# K-177 · A4 hız uyarlaması — ölçmeden ÖNCE yazılan beklenti (26 Eylül 2026)

Adım: `v2/15` A4. Anahtar `hiz_uyarlamasi` (varsayılan KAPALI; işlem kazancı ister). Açıkken:
- unicast veri ve kontrol çerçeveleri komşu başına ARF hızıyla (G14 ns-3 `ArfWifiManager`, birebir aktarım);
- yayın ve onaylar 1 Mb/s'te;
- hızlar 1/2/5,5/11 Mb/s; CCK hata modeli ns-3 GSL formu (SEP₁₆ tablosu).

Modülasyon kanalın değil çerçevenin özelliği oldu (kapalıyken aynı fonksiyon).

## 0 · Kapılar (ölçüldü, `esikler.py`)
- **Duyarlılık** (PER %10, 512 B, 22 MHz, NF 7): 1 Mb/s −97,0 · 2 Mb/s −92,5 · 5,5 Mb/s −89,9 · 11 Mb/s −86,9 dBm. İlk ikisi `v2/14`ün kaynaklı değerleriyle aynı.
- **SEP₁₆ tablosu** doğrudan integralden en çok ~10⁻⁴ göreli ayrışıyor.
- **Tek bağ ARF:** ortalama hız SNR ile artıyor — −2 dB 1,09 · 2 dB 2,37 · 6 dB 7,67 · 10 dB 10,92 Mb/s. 10 dB'de zamanın %99'u 11 Mb/s.

## 1 · Tam takım
→ 866 + 8 (A4) = **874 passed**. Ablasyon testi çerçeve-modülasyonuna göre yeniden yazıldı; iddiası korundu.

## 2 · Regresyon `k176 ↔ k177`
`python kalibrasyon/regresyon_satirlari.py karsilastir k176 k177 --yeni q- --izin "kimlik.kurulum_hash,konfig.hiz_uyarlamasi,konfig.arf_basari_esigi,konfig.arf_zamanlayici_esigi,teshis.koken_kovalari"`
- Ortak **59/59 birebir** (işlem kazancı açık `l-` vakası dâhil: A4 kapalıyken gövde hızı ve modülasyon aynı).
- Farklar yalnız: kod kimliği · `kurulum_hash` · üç yeni konfig alanı · köken kovaları (KAYNAK +3).
- Yeni vakalar `q-…-islem_kazanci-hiz_uyarlamasi` (veri yolu ve kontrol düzlemi) geçerli.
- Süre ~27 dk.
