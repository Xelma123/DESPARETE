# K-179 · B3 gözlem v2 alanları — ölçmeden ÖNCE yazılan beklenti (26 Eylül 2026)

Adım: `v2/15` B3. `Gozlem`e beş alan: `kendi_konum`, `kendi_hiz` (GPS/INS + hata), `mesgul_sure_s` (CCA meşgul süresi — yalnız `kanal_dolulugu_ister` diyen protokole, ötekinde `None`), `phy_hata` (kilitlenip gövdesi çözülemeyen), `alinan_cerceve`. Yüzey 12 → 17. Olay döngüsünün alım işleyicileri `kosum/alim.py`ye taşındı (davranış birebir).

Onaylı tanımdan sapma (gerekçeli): `phy_hata` önbelgesi hiç kilitlenmeyen çerçeveleri SAYMAZ — budama menzili 22 kat uzağa uzandığı için uzak zayıf her iletim sayılır, gerçek telsiz onları sezmezdi.

## 0 · Sınavlar
- Düğüm sayaçlarının toplamı global `alim_basarili` / `alim_red_per` ile aynı.
- GPS: ortanca yatay hata 1,2–1,8 m (CEP 1,5), dikey σ 1,7–2,3 m, 1 s dilimde sabit.
- Güç kipinde 40 dBm sürekli karıştırıcıyla her düğümde 1–4 s TAMAMEN meşgul.
- İstemeyen protokolde `mesgul_sure_s` = `None`.

## 1 · Tam takım
→ 878 + 4 = **882 passed**.

## 2 · Regresyon `k178 ↔ k179`
`python kalibrasyon/regresyon_satirlari.py karsilastir k178 k179 --yeni s- --izin "kimlik.kurulum_hash,konfig.gps_yatay_cep_m,konfig.gps_dikey_sigma_m,konfig.gps_hiz_sigma_ms,konfig.gps_tazeleme_s,teshis.koken_kovalari"`
- Ortak **64/64 birebir**. Protokoller yeni alanları okumuyor; doluluk yalnız isteyende; alım işleyicisi taşıması birebir.
- Farklar yalnız: kod kimliği · `kurulum_hash` · dört GPS alanı · köken kovaları (KAYNAK +1, SINANMAMIŞ +2, TÜRETİLMİŞ +1).
- Yeni vaka `s-statik-surekli-doluluk_sinav-tasiyici_guc` geçerli; teşhisinde doluluk, PHY hatası, alınan çerçeve, GPS değerleri dolu.
- Süre ~32 dk.
