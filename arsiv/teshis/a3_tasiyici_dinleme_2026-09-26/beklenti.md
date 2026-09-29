# K-174 · A3 güce dayalı taşıyıcı dinleme + ED-CCA — ölçmeden ÖNCE yazılan beklenti (26 Eylül 2026)

Adım: `v2/15` A3. Anahtar `tasiyici_dinleme` = "geometrik" (varsayılan, bugün) | "guc".
"guc": önbelge sezme = alıcı kilidi · enerji sezme = toplam alınan güç (iletimler + her sınıf karıştırıcı) ≥ `ed_esigi_dbm` (−76, G2) · sezme `cca_s` sürer · donma alım kararından sonra · hareketli karıştırıcıda donmuş düğüm 10 ms'de yeniden bakar.

## 0 · Kapılar (ölçüldü, `kapi_sayilari.py`)
- Tek çarpışma alanı (ED −200 dBm): güç kipi geometrikle sayısı sayısına aynı — deneme 1045 · meşgul reddi 1651 · teslim 23 (Bianchi'nin doğrulandığı rejim korunur).
- Sürekli karıştırıcı (40 dBm) açıldıktan sonra güç kipinde veri denemesi 0, beacon 0; geometrikte aynı pencerede 179 deneme, 36 beacon.
- Hareketli karıştırıcıyla donmuş düğüm t + 10 ms'de, sabitte t + beacon aralığında yeniden bakar; hava eşlikli tam koşuda defter kapanır.

## 1 · Tam takım
→ 844 + 7 (A3) = **851 passed**.

## 2 · Regresyon `k173 ↔ k174`
`python kalibrasyon/regresyon_satirlari.py karsilastir k173 k174 --yeni n- --izin "kimlik.kurulum_hash,konfig.tasiyici_dinleme,konfig.ed_esigi_dbm,konfig.karistirici_denetim_araligi_s,teshis.koken_kovalari"`
- Ortak **50/50 birebir**; farklar yalnız otomatik kod kimliği · `kurulum_hash` · üç yeni konfig alanı · köken kovaları (KAYNAK +2, TÜRETİLMİŞ +1).
- Yeni vakalar `n-…-tasiyici_guc` ve `n-…-tasiyici_guc-hava_eslik` geçerli.
- Süre ~25 dk.
