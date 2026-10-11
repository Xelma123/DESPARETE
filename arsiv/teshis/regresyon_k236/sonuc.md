# Regresyon k232 → k236 · yeni rakipler JarmRout ve OLSRv2 — sonuç

> 11 Ekim 2026 · ölçüt `beklenti.md` (commit `88d0064`, koşudan önce) · `kopya/` = `88d0064` (147 dosya birebir, `kopya_ozet.txt`) · `uret` 12:41–13:50 (68,5 dk; en uzun vaka `u-birincil-jarmrout` 1979 s) · çıktılar `uret.txt` · `karsilastir.txt`

- **Eski 81 vaka bulgusuz** — `BIREBIR` (izinli farklar dışında) ✓
- Farklar beklenen sınıflarda: kod özetleri, `kimlik.protokol_hash` 76 vakada (değişmeyen 5 vaka `tests2`'deki tek dosyalık sınav protokolleriyle koşuyor: `yuklu` · `kontrol_sinav`) ✓
- İzinli `teshis.koken_kovalari`: her satırda DUYARSIZ 11 → 9 · SINANMAMIŞ 3 → 5, öteki kovalar aynı (K-233) ✓
- **Dört yeni vaka geçerli** (korunum ve mutabakat tamam) ✓

| vaka | PDR | kopya üretilen · bastırılan |
|---|---|---|
| `u-birincil-jarmrout` | 0,409 | 75 · 35 |
| `u-birincil-olsrv2` | 0,464 | — |
| `u-bagimsiz-surekli-jarmrout-esler_arasi` | 0,064 | 27 · 21 |
| `u-bagimsiz-surekli-olsrv2-dugum_kaybi` | 0,008 | — |

JarmRout vakalarında kopya oluşuyor ✓, OLSRv2'de kopya alanı yok ✓. Aynı kısa pencerede birincil hücrede AODV 0,470 · DESPARETE 0,527 (k232); sayılar regresyon vakasıdır, karşılaştırma değil. Yeni taban: **k236**.
