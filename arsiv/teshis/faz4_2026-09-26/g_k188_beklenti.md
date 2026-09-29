# K-188 değişiklikleri — tam takım ve regresyon beklentisi (ölçmeden önce)

- **Değişenler:**
  - `referans_2026`: gölgeleme hücresi 2,5 km, alan 33 km, görev yarıçapı 16 km;
  - kapsam Θ/bölünme dünyadan;
  - araç düzeltmeleri: 21 araçta dünya seçimi, `dugum_sayisi` alanı, `aodv_uygunluk` muafiyetleri, güçlü bileşenler, `--alan`;
  - köken kayıtları.
- **Tam takım:** 917 + 1 (K-187 yasak) + 1 (K-185 `--alan`) + 1 (K-186 güçlü bileşen) + 1 (K-188 kapsam) = **921 passed**.
- **Regresyon `k184 ↔ k185`:**
  - `r-` dışı 64 vaka birebir; izinli yalnız `teshis.koken_kovalari`, kod kimliği otomatik.
  - Üç `r-` vakası ilan edilmiş değişen: alan 33 km, gölgeleme 2,5 km, kapsamda referans Θ. `gecerli=True`.
  - `r-statik-yok` PDR 0,20–0,45: 33 km biraz daha yoğun, doğrudan komşu payı artar.
