# 4.1c · Yere toplama yükü referans dünyada (35 km) — beklenti (ölçmeden önce)

> 26 Eylül 2026 · ajan · komut (dondurulmuş kopyadan): `python -u kalibrasyon/yere_toplama_yuku.py --dunya referans_2026 tarama`

**Ölçüt (K-124, değişmez):** karıştırıcısız statik kolda kâhin yönlendirmeyle teslim ≥ 0,95 tutan EN BÜYÜK telemetri hızı (ızgara 0,5 · 1,0 · 1,5 · 2,0 · 3,0 pkt/s; komut = telemetri × 0,25). 3 tohum, tam uzunluk.

**Tahmin:**
- Bütün telemetri geçide (batı kenarı) akar; darboğaz geçidin çevresi.
- Güç kipinde taşıyıcı sezme ~10 km; geçide yakın düğümler tek bir çekişme alanını paylaşır.
- 512 B'lık paket 1–11 Mb/s'te 0,5–4,5 ms. Yaklaşık kapasite 60–100 pkt/s; 1 Hz'te sunulan yük 40 pkt/s.
- **Öngörü:** 1,0 geçer (PDR ≥ 0,97). Seçilen hız **1,5–3,0** (ızgaranın üstünde de geçebilir). Eski dünyada 2,0'da 0,984 idi.
- Bugünkü değer (1,0) korunur ya da büyütülür. Eksen dengesi (39×1 + 4×0,25 = 40 = eşler arası 10×4) öğrenci kararıyla 1,0'da tutuluyordu (K-126); onu bozacak bir değişiklik önerilmez, yalnız marj raporlanır.
