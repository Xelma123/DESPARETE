# K-172 · B1/B2 kancası + DESPARETE V11 komut geri izi — ölçmeden ÖNCE yazılan beklenti (26 Eylül 2026)

Soru: K-171 bulgusu — DESPARETE komutları hiç taşımıyor (40/40 `politika`). V11 komutu telemetrinin geri iziyle, ek kontrol mesajı olmadan taşıyabilir mi; telemetriyi bozmadan?

## 1 · Tam takım
`PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python -m pytest tests2 -q -p no:cacheprovider` → hepsi geçer (830 + 5 B1/B2 + 4 V11 = 839).

## 2 · Regresyon `k171 ↔ k172` — davranış değişmemeli (V11 varsayılan KAPALI)
`python kalibrasyon/regresyon_satirlari.py karsilastir k171 k172 --izin "kimlik.kurulum_hash,kimlik.sayac_semasi_hash,konfig.rssi_olcum_sigma_db,metrikler.duyma_bildirimi*,teshis.koken_kovalari,teshis.dugum" --sifir "metrikler.duyma_bildirimi,metrikler.duyma_bildirimi_pencere"`
- Otomatik: `arac_hash`, `kosu_kimligi`, `protokol_hash` 49/49.
- İzinli: `kurulum_hash` (yeni konfig alanı) · `sayac_semasi_hash` (yeni sayaç) · `konfig.rssi_olcum_sigma_db` · `metrikler.duyma_bildirimi*` (49/49'da 0 — hiçbir protokol kancayı taşımıyor, DESPARETE de V11 kapalıyken) · `teshis.koken_kovalari` (SINANMAMIŞ 40 → 41) · `teshis.dugum` **yalnız** `k-…-desparete` vakasında (seçenek listesi + 4 yeni sayaç).
- Bunların dışında hiçbir alan değişmez; 49/49 bulgusuz.

## 3 · V11 A/B — tam ölçek (N = 40), kısa pencere, eşli tohum
`python arsiv/teshis/v11_komut_geri_izi_2026-09-26/ab.py` · kollar v0.4 ↔ v0.4 + V11 · `statik-surekli`, `bagimsiz-surekli` · tohum 1003–1007 · pencere regresyonunki (50 s koşu, 10–40 s ölçüm) · 8 işçi · süre bandı 8–15 dk.
- `pdr_komut`: A = 0 (hepsi `politika`). B ≈ geri izin tazeliği × yol teslimi → statikte 0,6–0,85; hareketlide daha düşük (0,4–0,75).
- `pdr_telemetri` (pencere): B − A ortalaması |Δ| ≤ 0,02 — komut yükü 1 pkt/s, telemetri 39 pkt/s (~%2,5); tek tohum farkları yörünge gürültüsüdür (K-158 §5), işaretin tutarlılığına bakılır.
- Kontrol yükü (`kontrol_bayt`): V11 kontrol mesajı eklemez → |Δ| küçük, yön tutarsız.
- Komut döngüsü: `veri_hop_siniri` ve `ttl` düşüşü B'de A'dan fazla değil.
- Maliyet: B'nin duvar saati kancadan dolayı A'dan %10–40 uzun.
