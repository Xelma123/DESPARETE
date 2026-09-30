# Faz 4.4 #1 · referans dünyanın eşleştirilmiş çözünürlüğü R — beklenti (ölçmeden önce)

> 30 Eylül 2026 12:15 · ajan · plan `arsiv/teshis/faz4_kapanis_2026-09-30/denetim.md` (4.4 tablosu #1) · öğrenci sırayı onayladı (K-204).
> Komut (dondurulmuş kopya `kopya/`, 8 işçi, yanında ağır iş yok): `py -3.11 -u kalibrasyon/cozunurluk.py --dunya referans_2026 --tohum 40` · ~30 dk

## Ne için

1. **Duyarlılık taraması** (4.4 #3–#6): `R = 2 · SD_tohum(ölçüt bedeli) / √40`, iki kâhinin aynı tohumdaki eşleştirilmiş farkından. Saklanan `duyarlilik.py::R_ESLESTIRILMIS = 0,0230` ESKİ dünyanın; araç bayatsa söyler.
2. **AOMDV'nin kâhin aşımı** (K-192 b, K-205): eşler arası formasyon 1000'de AOMDV 0,9777 · kâhin 0,9762 → **+0,0015**. Karar kuralı: aşım ≤ R ise "çözünürlük içinde, aşım sayılmaz" → U1-U geçer. Aşım > R ise üç kâhinin zarfına bakılır (aynı hücrede `en_kisa_yol_kahin` ve üçüncü kâhin); zarfı da aşıyorsa yazılım hatası aranır.

⚠️ R kol düzeyinde (40 tohumlu ortalama) bir görünürlük eşiğidir; tek hücrenin aşımıyla karşılaştırmak K-192 (b)'nin kuralıdır (öğrenci onaylı). Aşım çok küçük olduğu için sonuç büyük olasılıkla "R içinde" çıkar; yine de R ölçülmeden hüküm verilmez.

## Sonuç 1 (12:15) — R bu hücrede KULLANILAMAZ

`cozunurluk.txt`: R (eşleştirilmiş) = 0,0086 · pdr_etx ortalama **0,0287**. Aracın hücresi (statik-sürekli, kısa pencere, tek merkez karıştırıcı) eski dünyanın çekirdek hücresidir. Referans dünyada bu hücrede kâhin bile %3 teslim ediyor: taban etkisi, R yapay küçük. `R_ESLESTIRILMIS` güncellenmez. **4.4 planı düzeltilmeli:** "statik" duyarlılık hücresi de aynı tabanda (sahte DUYARSIZ riski); çalışma noktası birincil hücre.

## AOMDV — K-192 (b)'nin ikinci adımı (R geçerli ölçülemediği için doğrudan)

`aomdv_zarf.py` · aynı hücrede üç kâhin (ETX · en kısa yol · en olası teslim), U1'in konfigürasyonuyla. **Kural:** AOMDV (0,9777) ≤ zarf → "ETX kâhini bu hücrede üst sınır değil" beyanı, U1-U geçer · AOMDV > zarf → yazılım hatası aranır. Tutarlılık: ETX kâhini 0,9762'yi birebir üretmeli. ~40 dk, 3 süreç.

## Sonuç 2 (12:32) — AOMDV zarfın içinde ✅

`aomdv_zarf.txt`: ETX kâhini 0,9762 (U1'le birebir ✅) · en kısa yol 0,8861 · **en olası teslim 0,9986** → zarf 0,9986 ≥ AOMDV 0,9777. K-192 (b): "ETX kâhini bu hücrede üst sınır değil" beyanı; U1-U geçer. U1 aracında `KAHIN_ASIMI_ACIKLANMIS` (desen başına, ölü kayıt taramalı; test `test_K192b_KAHIN_ASIMI_ZARF_KAYDI`). Hüküm: AOMDV eşler arası U1-U 🟢; U1-B'de statik 1002 (0,889) keşifsel bulgu olarak kalır.
