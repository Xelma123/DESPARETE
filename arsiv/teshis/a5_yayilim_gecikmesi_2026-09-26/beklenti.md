# K-175 · A5 yayılım gecikmesi — ölçmeden ÖNCE yazılan beklenti (26 Eylül 2026)

Adım: `v2/15` A5. Anahtar `yayilim_gecikmesi` (varsayılan KAPALI). Açıkken alım, donma ve taşıyıcı dinleme varış penceresiyle (d/c), onay bekleme + 2 · en uzak duyma gecikmesi. Girişim hesabı gönderim anlarıyla (beyanlı hata ≤ d/c). Kapalıyken her gecikme tam 0,0.

## 1 · Tam takım
→ 851 + 5 (A5; biri iki parametreli) = **856 passed**.

## 2 · Regresyon `k174 ↔ k175`
`python kalibrasyon/regresyon_satirlari.py karsilastir k174 k175 --yeni o- --izin "kimlik.kurulum_hash,konfig.yayilim_gecikmesi,teshis.koken_kovalari"`
- Ortak **52/52 birebir** — güç kipi vakaları (`n-`) dâhil: güç kipindeki kilit ve enerji yolları varış penceresine çevrildi ama gecikme 0 iken cebirsel olarak aynı küme ve aynı sayılar.
- Farklar yalnız kod kimliği · `kurulum_hash` · `konfig.yayilim_gecikmesi` · köken kovaları (TÜRETİLMİŞ +1).
- Yeni vakalar `o-…-yayilim_gecikmesi` (geometrik) ve `o-…-tasiyici_guc-yayilim_gecikmesi` geçerli.
- Süre ~30 dk.
