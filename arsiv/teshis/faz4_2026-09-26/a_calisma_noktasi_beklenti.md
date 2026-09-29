# 4.1a · Çalışma noktası (alan) — beklenti (ölçmeden önce)

> 26 Eylül 2026 · ajan · komut: `python kalibrasyon/calisma_noktasi.py --dunya referans_2026 --bolum yaricaplar,alan_taramasi` (30 tohum)

## Ölçüt (değişmez, K-101/K-102)

- **Sert kısıt:** statik kolda 30 tohumun hiçbirinde ulaşılamaz çift yok.
- **Amaç:** atlama derinliği en büyük.
- **Kullanılabilir bağ:** yeniden denemeler dâhil atlama başarısı ≥ 0,90; referansta ARF tabanında (1 Mb/s).

## Beklenen

**Yarıçaplar (analitik, serbest uzay, gölgelemesiz):**
- 1 Mb/s veri, PER %10 → ≈ **7,4 km**. Kaynak: 2 Mb/s'te 5,2 km (`v2/14` §1); 1 Mb/s +3 dB → ×√2.
- PER %50 → ≈ 9 km.

**Alan taraması:**
- 7 km'de (bugünkü referans): derece ≈ 25–35 (40'lık sürüde neredeyse tam örgü), ≥ 3 atlamalı çift ≈ %0, kopukluk 0. → **Bugünkü referans alanı yönlendirmeye iş bırakmıyor**.
- **Seçilecek alan: 20–25 km.** Ölçüt ölçekten bağımsız, yalnız L/r oranını görür.
  - Eski dünyada L = 1800 m, derece 8,67 → r_eski ≈ 530 m (kenar payıyla) → L/r ≈ 3,4.
  - Referansta r ≈ 7–7,5 km → L ≈ 24–25 km.
  - σ 3 dB gölgeleme ve K = 10 dB sönümleme dağılımı biraz değiştirir; bant bu yüzden geniş.
- Seçilen noktada derece ≈ 8–10, derin çift payı ≈ %25–35 (eski dünyada %31).

## Yanlışlanırsa

- Seçilen alan 16 km'nin altında çıkarsa bağ menzili tahminimden kısadır. Bu durumda yarıçap bölümüyle karşılaştırıp nedenini ararım.
- 30 km'de bile kopukluk %0 çıkarsa ızgara genişletilir.

## Sonuç kimde

Seçilen alan `v2/14` §3'ün ~6–8 km'sinden çok farklı çıkarsa bu, planın risk maddesidir: "yeni dünya yönlendirmeye iş bırakmazsa alan ve N kaynaklı sürü geometrisi içinde ayarlanır; öğrenciye sorulur". Karar öğrenciye seçenekleriyle gider. Ajan alanı kendisi değiştirmez.
