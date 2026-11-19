# Faz 5-3 · yeni çekirdek ↔ Babel ve genel bileşenlerinin ablasyonu, karıştırıcısız ikizde ve birincil hücrede — sonuç

> 20 Kasım 2026 · ölçüt `beklenti.md` (öngörüler ve karar kuralı commit `1ee0cc5`, dumandan önce; duman notu commit `63f9a45`) · koşu (`zaman.txt`): 19 Kasım 16:04 – 20 Kasım 00:36 (8 sa 32 dk; adımlar 51 dk – 1 sa 23 dk). Tahmin ilk ~7 sa, dumandan sonra ~12 sa (10–14) idi; ilki daha yakın çıktı · `kopya/` = `63f9a45` (166 dosya birebir, satır sonları normalleştirilerek; `kopya_ozet.txt`) · ham çıktı `olcum_*.txt`, kayıt `kayit_*.json` · karar kuralı `sonuc_hesap.py` → `sonuc_hesap.txt` · ek sayılar `ek_hesap.py` → `ek_hesap.txt` (koşudan sonra yazıldı, karar girdisi değil). Babel, kâhin ve v0.4.1 teşhis (c)'nin; 18 Kasım çekirdeği ilk ölçümün; `vtk0` açlık teşhisinin kayıtlarından.

## 0 · Geçerlilik ✓

- 64 koşunun hepsi kayıtta. Korunum geçerli, doğum çelişkisi 0, atfsız düşüş yok, ikincil sayım pencere PDR'siyle tutarlı; kaydedicinin iç denetimleri 64 koşuda da geçti.
- Teşhis (c)'nin Babel, kâhin ve v0.4.1 satırları ve ilk ölçümün çekirdek satırları 16'şar; `vtk0` satırları 8.
- Duman koşusunda kaydedicili ve kaydedicisiz çekirdek iki hücrede bütün alanlarda birebirdi; 18 Kasım'ın çekirdeği iki hücrede ilk ölçümün duman satırıyla birebirdi (beklenti, son bölüm).

## 1 · Düzeyler (8 tohum ortalaması ± ölçüt sapması)

| kol | İ · pencere PDR | B · `PDR_açık` | B · önce · sessiz |
|---|---|---|---|
| kâhin | 0,917 ± 0,029 | 0,779 ± 0,077 | 0,919 · 0,916 |
| Babel | 0,930 ± 0,030 | 0,663 ± 0,139 | 0,932 · 0,916 |
| v0.4.1 | 0,785 ± 0,040 | 0,567 ± 0,085 | 0,779 · 0,763 |
| 18 Kasım çekirdeği | 0,810 ± 0,187 | 0,410 ± 0,123 | 0,820 · 0,612 |
| `vtk0` | 0,946 ± 0,025 | — | — |
| **çekirdek** | **0,954 ± 0,020** | **0,663 ± 0,199** | 0,954 · 0,854 |
| vaz0 | 0,940 ± 0,043 | 0,672 ± 0,139 | 0,947 · 0,874 |
| düz0 | 0,950 ± 0,036 | 0,671 ± 0,170 | 0,956 · 0,834 |
| eğim0 | 0,943 ± 0,023 | 0,665 ± 0,141 | 0,940 · 0,911 |

Çekirdek, tohum başına:

| | 1003 | 1004 | 1005 | 1006 | 1007 | 1008 | 1009 | 1010 |
|---|---|---|---|---|---|---|---|---|
| İ | 0,965 | 0,972 | 0,911 | 0,945 | 0,977 | 0,958 | 0,952 | 0,951 |
| B | 0,512 | 0,820 | 0,314 | 0,813 | 0,879 | 0,653 | 0,798 | 0,514 |

## 2 · S1 — genel düzey (karar)

`G_İ = PDR(Babel) − PDR(çekirdek)` = **−0,024**. 8/8 tohumda çekirdek önde: 1003 −0,021 · 1004 −0,018 · 1005 −0,048 · 1006 −0,028 · 1007 −0,020 · 1008 −0,018 · 1009 −0,010 · 1010 −0,028. Ayrışma kuralıyla **AYRIŞIYOR**.

**Hüküm: çekirdek ileride.** S4'te zararlı bileşen yok (§5); karar kuralının 1. maddesi gereği sıradaki iş karıştırma katmanı: kalabalık yanlış alarmının düzeltmesi (KK-03 kural 12) ve `karistirma_durumu`nun A/B'si.

Ayrıca (karar değiştirmez):
- çekirdek − `vtk0`: +0,008, 8/8 artı; eşiğin altında, "8 tohumda ayırt edilemedi". İlk ölçümün açığı kapandı ve tersine döndü; ama kazancın neredeyse tamamı eski veri tetiğinin kalkmasından geliyor.
- çekirdek − 18 Kasım çekirdeği: +0,144 (7/8; 1004 −0,006) → ayrışıyor.
- çekirdek − v0.4.1: +0,169 (8/8) → ayrışıyor.

## 3 · S2 — başlangıç çizgisi (betimleyici)

- Babel − çekirdek: **+0,000** (3/8 artı, 5/8 eksi; 1005 +0,171, 1009 −0,066) → 8 tohumda ayırt edilemedi.
- v0.4.1 − çekirdek: −0,096 (6/8 eksi) → ayrışıyor (çekirdek önde).
- 18 Kasım çekirdeği − çekirdek: −0,253 (8/8) → ayrışıyor (çekirdek önde).
- `Δ_k`: kâhin −0,137 · Babel −0,265 · v0.4.1 −0,222 · 18 Kasım çekirdeği −0,391 · çekirdek −0,290 ± 0,178 (hayalet 0,953 → hücre 0,663) · vaz0 −0,265 · düz0 −0,273 · eğim0 −0,281.
- `Δ_k(çekirdek) − Δ_k(Babel)` = −0,025 (4/8 · 4/8) → 8 tohumda ayırt edilemedi.
- Evreler: çekirdeğin "önce" teslimi 0,954 (Babel 0,932); sessiz dönemi 0,854 (Babel 0,916, eğim0 0,911).

## 4 · S3 — kontrol yükü ve gecikme

| | kontrol kanal süresi · payı (İ) | kontrol kanal süresi · payı (B) | 5 s tavanın bedeli (İ · B) | p99 (İ · B) |
|---|---|---|---|---|
| Babel | 67,8 s · %14,7 | 77,0 s · %15,0 | 0,000 · 0,006 | 0,23 · 1,31 s |
| `vtk0` | 22,0 s · %6,1 | — | 0,000 · — | 0,30 · — |
| çekirdek | 21,3 s · %6,0 | 23,7 s · %5,5 | 0,000 · 0,006 | 0,22 · 1,77 s |
| vaz0 | 21,2 s · %5,8 | 22,0 s · %5,3 | 0,000 · 0,005 | 0,24 · 1,52 s |
| düz0 | 21,6 s · %5,9 | 23,6 s · %5,5 | 0,000 · 0,005 | 0,30 · 1,43 s |
| eğim0 | 21,6 s · %6,0 | 23,1 s · %5,8 | 0,000 · 0,005 | 0,18 · 1,08 s |

Tavan hiçbir hücrede bağlayıcı değil (bedel < 0,02). Kontrol yükü Babel'inkinin üçte biri; dört kol arasında fark yok.

## 5 · S4 — bileşenler (karar)

Açık − kapalı, eşli, eşik 0,02:

| bileşen | İ | B |
|---|---|---|
| vazgeçme tetiği (çekirdek − vaz0) | +0,014 (6/8 artı) → katkı ayırt edilemedi | −0,009 (4/8 · 4/8) → zarar yok |
| iki ölçülü geçiş (çekirdek − düz0) | +0,005 (3/8 artı) → katkı ayırt edilemedi | −0,008 (2/8 artı) → zarar yok |
| eğim (vaz0 − eğim0) | −0,003 (4/8 · 4/8) → katkı ayırt edilemedi | +0,007 (4/8 · 4/8) → zarar yok |

**Hüküm: zararlı bileşen yok.** Katkısı ayrışan bileşen de yok; üçünün katkısı raporda "8 tohumda ayırt edilemedi" diye yazılır. Kural 4 gereği hiçbir bileşen kendiliğinden çıkmaz ya da kalmaz; kalıp kalmayacaklarına bu sonuçla ve tanıyla (§6, §9) karar veririm.

Betimleyici:
- yeni yol seçimi bütünüyle (çekirdek − eğim0): İ +0,011 (8/8 artı, eşiğin altında) · B −0,002 (4/8 · 4/8);
- 19 ↔ 18 Kasım çekirdeği: İ +0,144 (7/8) · B +0,253 (8/8);
- bekletme 1 s ↔ 2 s (eğim0 − `vtk0`, İ): −0,003 (3/8 artı) → ayırt edilemedi.

## 6 · S5 — tanı (betimleyici)

Kayıp grupları ve iletim:

| | kayıp R · İ (İ) | kayıp R · İ · K (B, açık) | karar/paket · atlama başarısızlığı · `g` (İ) |
|---|---|---|---|
| Babel | 0,000 · 0,070 | 0,000 · 0,335 · 0,002 | 3,57 · %2,22 · 0,469 |
| `vtk0` | 0,003 · 0,052 | — | 3,16 · %1,71 · 0,482 |
| çekirdek | 0,002 · 0,044 | 0,042 · 0,287 · 0,008 | 3,18 · %1,44 · 0,492 |
| vaz0 | 0,006 · 0,054 | 0,020 · 0,302 · 0,006 | 3,18 · %1,79 · 0,479 |
| düz0 | 0,006 · 0,044 | 0,035 · 0,289 · 0,006 | 3,27 · %1,38 · 0,493 |
| eğim0 | 0,002 · 0,055 | 0,037 · 0,297 · 0,001 | 3,12 · %1,83 · 0,478 |

Ömür (TTL) kaybı bütün kollarda iki hücrede de 0.

Çekirdeğin yol seçimi sayaçları (koşu başına, bütün koşu, ağ toplamı; İ · B):

| sayaç | İ | B |
|---|---|---|
| ardıl değişimi: zorunlu · isteğe bağlı · veriye uygunsuzluk | 55 · 576 · 86 | 476 · 703 · 197 |
| son çare | 9 | 141 |
| yol yok · ortalama süresi | 3,0 · 4,20 s | 117 · 2,21 s |
| tavan aşımı | 0 | 26,5 |
| bayat bilgi · kesin döngü · dışlama | 94 · 73 · 103 | 595 · **3620** · 5619 |
| selam · ara ilan | 8633 · 1338 | 9759 · 2343 |
| bekletilen · süresi dolan | 141 · 94 | 868 · 490 |

Kesin döngü öteki eğimli kollarda (İ · B): vaz0 466 · 2140 · düz0 424 · 3515. Eğim0'da döngü yoktur (FD); açlık 17,8 · 103, tur artışı 26,1 · 32,5.

Kaynak maliyeti ve atlama sayısı (çekirdek):
- İ: maliyet p50 5 · p90 8 · p99 14 ETX, en çok 29,4; 16 ETX ve üstü %0,44, ∞ %0,11. Teslim edilenlerin atlama sayısı p50 3 · p99 8, en çok 26; kararlarda en çok 25.
- B: maliyet p50 6 · p90 14 · p99 25 ETX, en çok 32,0 (tavan); 16 ETX ve üstü %6,8, ∞ %2,3. Atlama p50 3 · p99 11, teslimde en çok 39; kararlarda en çok 60.
- Eğim0'da B: maliyet p99 17, en çok 25,6; teslimde en çok 14 atlama.

Vazgeçme tetiği (çekirdek, penceredeki tetikler):

| | İ | B |
|---|---|---|
| tetik / koşu | 92 | 420 |
| kâhin bandı iyi · orta · kötü | 0,99 · 0,01 · 0,00 | 0,49 · 0,11 · 0,40 |
| ardıl payı | 1,00 | 0,99 |
| işaret sürerken ardılın değiştiği pay | 0,77 | 0,47 |
| işaret sürerken veri sonucu · vazgeçme (tetik başına) | 6,9 · 0,9 | 7,9 · 1,9 |
| bekleme 5 · 10 · 20 · 40 s | 0,42 · 0,21 · 0,12 · 0,25 | 0,28 · 0,14 · 0,08 · 0,50 |

Vazgeçmelerin bağlara dağılımı (bütün koşu; vazgeçme · ayrı bağ · en kötü bağ · en kötü beş bağın payı):
- İ: 18 Kasım çekirdeği 682 · 151 · 22 · 0,13 · `vtk0` 691 · 73 · 99 · 0,41 · çekirdek 586 · 77 · 73 · 0,36 · vaz0 727 · 78 · 91 · 0,39 · düz0 576 · 83 · 66 · 0,36 · eğim0 732 · 75 · 100 · 0,40.
- B: 18 Kasım çekirdeği 827 · 183 · 20 · 0,10 · çekirdek 1525 · 146 · 139 · 0,30 · vaz0 1644 · 119 · 212 · 0,38 · düz0 1519 · 153 · 166 · 0,32 · eğim0 1584 · 111 · 207 · 0,39.

## 7 · Kâhin

- İ'de çekirdek kâhini 7/8 tohumda `R`'den fazla aşıyor (ortalama +0,037); Babel 4/8.
- B'de çekirdek ve düz0 birer tohumda aşıyor (1009: +0,034 · +0,025); öteki kollar aşmıyor.

## 8 · Öngörülerle karşılaştırma

| öngörü | sonuç | |
|---|---|---|
| İ'de çekirdek 0,95 ± 0,02 · vaz0 0,945 · düz0 0,95 · eğim0 0,94 (± 0,02) | 0,954 · 0,940 · 0,950 · 0,943 | tuttu |
| B'de çekirdek 0,62 · vaz0 0,58 · düz0 0,62 (± 0,12) | 0,663 · 0,672 · 0,671 | tuttu |
| B'de eğim0 0,50 ± 0,12 | 0,665 | tutmadı (daha yüksek) |
| `G_İ` −0,04 … 0,00; en olası "ayırt edilemedi", ikinci olası "çekirdek ileride" | −0,024, çekirdek ileride | değer tuttu, hüküm ikinci olası |
| çekirdek − `vtk0` −0,01 … +0,02, ayırt edilemedi | +0,008, ayırt edilemedi | tuttu |
| çekirdek − 18 Kasım çekirdeği +0,10 … +0,17, en az 7/8 | +0,144, 7/8 | tuttu |
| B'de Babel − çekirdek −0,10 … +0,10, ayırt edilemedi | +0,000, ayırt edilemedi | tuttu |
| B'de 18 Kasım çekirdeği − çekirdek −0,30 … −0,10, 8/8 · v0.4.1 − çekirdek −0,15 … +0,05 | −0,253, 8/8 · −0,096 | tuttu |
| `Δ_k(çekirdek)` −0,45 … −0,20; Babel'le farkı ayırt edilemez | −0,290; ayırt edilemedi | tuttu |
| B'de önce 0,93–0,97 · sessiz 0,80–0,93 | 0,954 · 0,854 | tuttu |
| kontrol İ'de 17–28 s, %5–8; eğim0 18–26 s; B en çok 1,5 katı | 21,3 s, %6,0; 21,6 s; 1,11 kat | tuttu |
| 5 s tavanın bedeli < 0,01 | 0,000 · 0,006 | tuttu |
| p99 İ'de 0,2–0,6 s · B'de 0,4–2,0 s | 0,22 · 1,77 s | tuttu |
| vazgeçme tetiği İ'de +0,000 … +0,025 (ayırt edilemedi) · B'de +0,00 … +0,08 (zarar yok) | +0,014 · −0,009, zarar yok | tuttu · değer aralığın hemen altında, hüküm tuttu |
| iki ölçülü geçiş −0,01 … +0,01 iki hücrede · isteğe bağlı geçiş düz0'ınkinin 0,3–0,8 katı | +0,005 · −0,008 · 1,10 ve 0,97 kat | tuttu · tutmadı |
| eğim İ'de −0,01 … +0,015 · B'de +0,03 … +0,15, en olası birincilde katkı | −0,003 · +0,007, ayırt edilemedi | tuttu · tutmadı |
| çekirdek − eğim0 İ'de +0,00 … +0,03 · B'de +0,05 … +0,20 | +0,011 · −0,002 | tuttu · tutmadı |
| eğim0 − `vtk0` −0,01 … +0,005 | −0,003 | tuttu |
| İ'de R 0,000–0,006 · İ 0,030–0,055 · T ≤ 0,002; B açıkta R 0,02–0,15 · İ 0,18–0,32 · T ≤ 0,01 | 0,002 · 0,044 · 0; 0,042 · 0,287 · 0 | tuttu |
| eğim0'da B'nin R'si çekirdeğinkinden yüksek (0,05–0,30) | 0,037 (çekirdek 0,042) | tutmadı |
| tetik İ'de 50–300 · B'de 1,5–5 katı | 113 · 3,9 kat | tuttu |
| tetiklenen bağ İ'de iyi bantta 0,75–1,00 · ardıl payı ≥ 0,90 · ardılın değiştiği pay 0,30–0,80 | 0,99 · 1,00 · 0,77 | tuttu |
| en kötü beş bağın payı vaz0 0,30–0,50 · çekirdek 0,12–0,30; çekirdeğin vazgeçmesi %10–40 az | 0,39 · 0,36; %19 az | tuttu · tutmadı · tuttu |
| İ'de döngü 0–20 · bayat 10–300 · son çare 5–100 · tavan 0–5 · yol yok 0–30, süresi 0,2–2 s | 73 · 94 · 9 · 0 · 3,0, 4,20 s | tutmadı · tuttu · tuttu · tuttu · tuttu, süre tutmadı |
| B'de döngü 0–100; son çare ve yol yok İ'dekinin 2–10 katı | 3620; 15 ve 39 kat | tutmadı (çok daha yüksek) |
| kaynak maliyeti İ'de p50 4–8 · p99 ≤ 16 · ≥ 16 ETX < %1 · ∞ < %0,5 | 5 · 14 · %0,44 · %0,11 | tuttu |
| atlama İ'de teslim p50 3–4 · p99 6–8 · en çok ≤ 10; kararlarda ≤ 12 | 3 · 8 · 26; 25 | tuttu · tuttu · tutmadı; tutmadı |
| B'de kararlarda en çok, TTL'nin sınırına kadar (duman notunda 63'e düzeltildi) | 60 | tuttu |
| kâhini İ'de 2–7 tohumda aşar; B'de hiçbir kol aşmaz | 7/8; çekirdek ve düz0 1/8 | tuttu · tutmadı |

Düzeyler, kontrol yükü ve gecikme tuttu. Tutmayanların çoğu iki yerde toplanıyor: eğimin birincildeki katkısını beklemiştim, yoktu; döngüleri de çok az tahmin etmişim.

## 9 · Kuraldan sonra görülenler (karar girdisi değil)

`ek_hesap.txt` (tohum başına):

- **Döngüler zor tohumlarda toplanıyor.**
  - B'de çekirdeğin kesin döngüsü: 1005'te 13 251 · 1003'te 7827 · 1008'de 3830 · 1010'da 3027; öteki dört tohumda 41–477.
  - Döngü sayısı ile teslim arasında Pearson r = −0,93; rota yokluğu kaybıyla +0,86. Öteki eğimli kollarda da aynı yönde (−0,80 · −0,94).
  - Bu tohumlarda döngüsüz eğim0 de düşük (1005 0,470 · 1003 0,527 · 1010 0,519). Zorlanan ağda döngü çıkıyor; döngünün ayrıca ne kadar kaybettirdiği yalnız eğim0'la eşli farktan okunabiliyor.
- **Ortalamada bedel yok, en kötü tohumda var.**
  - Çekirdek − eğim0 (B): 1005 −0,156 · 1008 −0,046 · 1003 −0,015 · 1010 −0,004 · 1009 +0,116 · 1007 +0,071 · 1004 +0,020 · 1006 +0,000.
  - Tohumlar arası sapma: çekirdek 0,199, eğim0 0,141, Babel 0,139. En düşük tohum: çekirdek 0,314, eğim0 0,470, Babel 0,485.
  - 1005'te çekirdeğin iletim kaybı 0,537 (eğim0 0,429); döngüdeki paket fazladan atlama yapıyor ve her atlama yeni bir kayıp şansı.
  - Teslim edilenlerin ≥ 12 atlamalı payı en çok %3,7 (1005).
- **İki ölçülü geçiş döngüleri önlemiyor.**
  - B'de çekirdek 3620 · düz0 3515 kesin döngü; isteğe bağlı geçiş sayısı da hemen hemen aynı (703 ↔ 723; İ'de 576 ↔ 525).
  - Dumanda (tek tohum, 30 s) düz0'ın döngü fırtınası çekirdekte yoktu (2470 ↔ 22). Oradan "iki ölçülü geçiş yol seçimini frenliyor" diye çıkardığım yorum tam koşuda tutmadı: fırtına düz0'a özgü değil, eğimin kendisinde.
- **Vazgeçme tetiği iki hücrede ters yönde çalışıyor.**
  - İ'de döngüyü azaltıyor: 1005'te vaz0 3649 ↔ çekirdek 500 kesin döngü, teslimde +0,072.
  - B'de artırıyor: koşu başına vaz0 2140 ↔ çekirdek 3620; 1005'te teslimde −0,124.
  - B'de tetiklenen bağların %40'ı kâhine göre kötü bantta, tetiklerin yarısı en uzun beklemede (40 s). İşaret sürerken ardıl ancak %47 oranında değişebiliyor; çoğunda G1'de başka aday yok.
- **Eğimin karşılığı ölçülemedi.**
  - Eski veri tetiği kalkınca 18 Kasım'ın yol seçimi (eğim0) iki hücrede de eğimle aynı düzeyde.
  - Eğim0'da döngü yok, gecikmenin p99'u daha düşük (B'de 1,08 ↔ 1,77 s), sessiz dönem teslimi Babel düzeyinde (0,911 ↔ çekirdek 0,854).
  - Eğim0'da açlık ve tur artışı sürüyor (B'de koşu başına 103 açlık); B'nin açık döneminde rota yokluğu kaybı eğim0'da 0,037, çekirdekte 0,042.
- **Sessiz dönem eğimli kollarda Babel'in gerisinde** (0,834–0,874 ↔ 0,916). Karıştırma bittikten sonraki toparlanma eğimde yavaş; döngü sayaçları koşu toplamı olduğu için hangi evrede biriktikleri bu ölçümde ayrılamıyor.

Bu gözlemler karar kuralını değiştirmez. Karıştırma katmanı karıştırılan komşuyu aday kümesinden çıkaracağı için birincil hücrede zorunlu geçişi, dolayısıyla eğimin döngülerini artırabilir. Karıştırma katmanının A/B'lerinden önce eğimin döngü tepkisine bakılıp bakılmayacağına, eğimin ve vazgeçme tetiğinin sürümde kalıp kalmayacağına bu sonuçla karar veririm.
