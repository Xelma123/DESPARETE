# K-186 uygulaması — beklenti (ölçmeden önce)

- **Değişenler:**
  - `REFERANS_KARISTIRICI_DBM` 30 → 40 dBm;
  - `kahin.ozet`e güçlü bileşenler (yalnız kalibrasyon özeti);
  - dünya seçimine `--alan`;
  - köken defterine `BUYUK_BOLUNME_ORANI`.
- **Tam takım:** 915 + 2 = **917 passed**.
- **Regresyon `k183 ↔ k184`:**
  - `r-referans-statik-yok-…` karıştırıcısız → birebir.
  - Karıştırıcılı iki `r-` vakası ilan edilmiş değişen (merkez karıştırıcı 1 → 10 W):
    - AODV PDR 0,354 → **< 0,15**;
    - tek atlama `bagimsiz` 0,118 → **< 0,08**;
    - ikisi de `gecerli=True`.
  - Geri kalan 64 vaka birebir. İzinli: `teshis.koken_kovalari` (yeni köken kaydı).
