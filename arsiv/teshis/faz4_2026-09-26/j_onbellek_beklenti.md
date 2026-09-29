# K-190 · Yavaş kayıp önbelleği — beklenti (ölçmeden önce)

- **Değişiklik:** `Yayilim.yavas_kayip_db` saf fonksiyon; anahtar tam girdi (i, j, a, b). Tavan 1<<18, dolunca boşaltılır.
- **Profil (20 s, statik, AODV, 33 km):** 341 → 202 s (−%41). Olay 818 571, MAC denemesi 3 508 ve alım 377 851 birebir aynı.
- **Tam takım:** 921 passed (yeni test yok).
- **Regresyon `k185 ↔ k186`:** 67/67 BİREBİR. İzinli yalnız `teshis.koken_kovalari` (K-189 kapanışları ve yeni köken); kod kimliği otomatik. Hiçbir metrik değişmez.
- **Yanlışlanırsa:** tek bir metrik farkı bile önbelleğin saf olmadığını gösterir; değişiklik geri alınır.
