# K-173 · A2 DSSS işlem kazancı — ölçmeden ÖNCE yazılan beklenti (26 Eylül 2026)

Adım: `v2/15` A2. Anahtar `islem_kazanci` (varsayılan KAPALI). Açıkken Eb/N0 = SINR · B/R_b (B = 22 MHz): gövde ×11, önbelge ×22. Kapalıyken çarpan tam 1,0.

## 0 · Kapı (ölçüldü, `ns3_karsilastirma.py`)
PER–SINR eğrisi ns-3 `DsssErrorRateModel` ile: gövde eşikleri en çok 0,05 dB ayrışıyor (bizde kesin DQPSK, ns-3'te Ferrari–Corazza yaklaşımı), önbelge birebir. Duyarlılık 2 Mb/s 512 B PER %10: −92,5 dBm. Kapalı model tam 10·log₁₀11 = 10,41 dB fazla SINR istiyor.

## 1 · Tam takım
`PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python -m pytest tests2 -q -p no:cacheprovider` → 839 + 5 A2 = **844 passed**.

## 2 · Regresyon `k172 ↔ k173`
`python kalibrasyon/regresyon_satirlari.py karsilastir k172 k173 --yeni l- --degisen k-statik-surekli-desparete --izin "kimlik.kurulum_hash,konfig.islem_kazanci,teshis.koken_kovalari"`
- **Ortak 48 vaka birebir** (DESPARETE vakası hariç). Farklar yalnız: otomatik kod kimliği (`arac_hash`, `kosu_kimligi`, `protokol_hash`) · `kurulum_hash` ve `konfig.islem_kazanci` (yeni alan) · `teshis.koken_kovalari.KAYNAK` (+1).
- **İlan edilmiş değişen vaka** `k-statik-surekli-desparete-yere_toplama`: DESPARETE varsayılanı v0.4 → v0.4.1 (K-172). Geçerli; `korunum.dusen.politika` 40 → 0, `pdr_komut` 0 → > 0 (karşılaştırmadan sonra satırdan okunur).
- **Yeni vaka** `l-statik-surekli-dogrudan_komsu-islem_kazanci`: geçerli. (Deneme: pdr_pencere 0,900 ↔ aynı tohumda kapalı 0,279 — eski dünyada türetilen verici gücü yüzünden menzil de büyüyor; ölçüm değil, yolun işlediğinin kanıtı.)
- Süre: ~24 dk (1 yeni vaka ~90 s).
