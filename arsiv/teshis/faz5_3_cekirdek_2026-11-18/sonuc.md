# Faz 5-3 · yeni sürümün çekirdeği ↔ Babel, karıştırıcısız ikizde ve birincil hücrede — sonuç

> 18 Kasım 2026 · ölçüt `beklenti.md` (öngörüler ve karar kuralı commit `236f7af`, dumandan önce; duman notu commit `0fdd3ce`) · koşu (`zaman.txt`): ikiz 13:39–14:57 (1 sa 17 dk) · birincil 14:57–16:09 (1 sa 12 dk); tahmin ~4 sa üst sınırdı · `kopya/` = `0fdd3ce` (164 dosya birebir, satır sonları normalleştirilerek; `kopya_ozet.txt`) · ham çıktı `anatomi_*.txt`, kayıt `kayit_cekirdek_*.json` · karar kuralı `sonuc_hesap.py` → `sonuc_hesap.txt` · ek sayılar `ek_hesap.py` → `ek_hesap.txt` (koşudan sonra yazıldı, karar girdisi değil). Babel, kâhin ve v0.4.1'in satırları teşhis (c)'nin kayıtlarından.

## 0 · Geçerlilik ✓

- Çekirdeğin 16 koşusunun hepsi kayıtta. Korunum geçerli, doğum çelişkisi 0, atfsız düşüş yok; ikincil sayım pencere PDR'siyle tutarlı.
- Teşhis (c)'nin Babel, kâhin ve v0.4.1 satırları 16'şar.
- Duman koşusunda Babel 1003 iki hücrede teşhis (c)'nin dumanıyla birebirdi (beklenti, son bölüm).

## 1 · Düzeyler (8 tohum ortalaması ± ölçüt sapması)

| kol | İ · pencere PDR | B · `PDR_açık` |
|---|---|---|
| kâhin | 0,917 ± 0,029 | 0,779 ± 0,077 |
| Babel | 0,930 ± 0,030 | 0,663 ± 0,139 |
| **çekirdek** | **0,810 ± 0,187** | **0,410 ± 0,123** |
| v0.4.1 | 0,785 ± 0,040 | 0,567 ± 0,085 |

Çekirdek, tohum başına:

| | 1003 | 1004 | 1005 | 1006 | 1007 | 1008 | 1009 | 1010 |
|---|---|---|---|---|---|---|---|---|
| İ | 0,693 | 0,978 | 0,401 | 0,843 | 0,920 | 0,895 | 0,937 | 0,811 |
| B | 0,379 | 0,436 | 0,131 | 0,447 | 0,468 | 0,487 | 0,536 | 0,399 |

B'de çekirdeğin evreleri: önce 0,820 · açık 0,410 · sessiz 0,612 (Babel 0,932 · 0,663 · 0,916).

## 2 · S1 — genel düzey (karar)

`G_İ = PDR(Babel) − PDR(çekirdek)` = **+0,120**. 7/8 tohumda Babel önde: 1003 +0,250 · 1004 −0,024 · 1005 +0,462 · 1006 +0,074 · 1007 +0,037 · 1008 +0,045 · 1009 +0,006 · 1010 +0,112. Ayrışma kuralıyla **AYRIŞIYOR**.

**Hüküm: çekirdek geride.** Karar kuralının 1. maddesi gereği sıradaki iş bu genel açığın teşhisi; karıştırma katmanının A/B'leri ondan sonra.

Çekirdek − v0.4.1: +0,025 (6/8). Ayrışma kuralıyla geçiyor, ama tohumlar iki yöne dağılmış (1004 +0,181 · 1005 −0,317).

## 3 · S2 — başlangıç çizgisi (betimleyici)

- Babel − çekirdek: **+0,253**, 8/8 → ayrışıyor (çekirdek geride).
- v0.4.1 − çekirdek: +0,157, 8/8 → ayrışıyor (çekirdek geride).
- Karıştırmaya özgü kayıp `Δ_k`: kâhin −0,137 · Babel −0,265 · v0.4.1 −0,222 · çekirdek −0,391 (hayalet 0,802 → hücre 0,410).
- `Δ_k(çekirdek) − Δ_k(Babel)` = −0,126 (3/8 artı, 5/8 eksi) → 8 tohumda ayırt edilemedi.

## 4 · S3 — kontrol yükü ve gecikme

| | kontrol kanal süresi · payı (İ) | kontrol kanal süresi · payı (B) | 5 s tavanın bedeli (İ · B) | p99 (İ · B) |
|---|---|---|---|---|
| kâhin | 19,0 s · %6,0 | 19,5 s · %5,6 | 0,000 · 0,003 | 0,14 · 0,33 s |
| Babel | 67,8 s · %14,7 | 77,0 s · %15,0 | 0,000 · 0,006 | 0,23 · 1,31 s |
| çekirdek | 34,6 s · %8,4 | 33,5 s · %9,4 | 0,004 · 0,002 | 3,40 · 3,81 s |
| v0.4.1 | 185,4 s · %33,1 | 186,6 s · %33,3 | 0,001 · 0,006 | 2,51 · 3,67 s |

Tavan hiçbir hücrede bağlayıcı değil (bedel < 0,02).

## 5 · S4 — tanı (betimleyici)

| | kayıp R · İ (İ) | kayıp R · İ (B, açık) | karar/paket (İ) | atlama başarısızlığı (İ) | deneme başarısı `g` (İ) |
|---|---|---|---|---|---|
| kâhin | 0,000 · 0,083 | 0,008 · 0,206 | 2,51 | %3,28 | 0,434 |
| Babel | 0,000 · 0,070 | 0,000 · 0,335 | 3,57 | %2,22 | 0,469 |
| çekirdek | **0,139** · 0,049 | **0,512** · 0,077 | 3,69 | %1,45 | 0,509 |
| v0.4.1 | 0,043 · 0,172 | 0,237 · 0,196 | 2,62 | %6,52 | 0,371 |

Çekirdeğin sayaçları (koşu başına, ağ toplamı; İ · B):

| sayaç | İ | B |
|---|---|---|
| açlık · ortalama süresi | 822 · 1,90 s | 1083 · 3,12 s |
| tur isteği (açlıkta) · iletilen istek · karşılanan | 1634 · 2532 · 1793 | 2243 · 2638 · 1741 |
| geçidin tur artışı | 92 | 96 |
| ardıl değişimi · zorunlu geçiş · isteğe bağlı geçiş | 3368 · 747 · 937 | 3882 · 814 · 864 |
| ardıldan geri çekme (∞) alındı | 1146 | 1389 |
| veriyle KÖTÜ · selamdan KÖTÜ · KÖTÜ'den dönüş | 399 · 777 · 1527 | 482 · 883 · 1647 |
| `d_f` bayatladı · komşu silindi | 585 · 337 | 608 · 356 |
| selam · ara ilan | 13745 · 5232 | 14401 · 5791 |
| bekletilen · süresi dolan | 4559 · 1707 | 6913 · 3578 |
| komut: giden · bekletilen · düşen | 996 · 2049 · 47 | 843 · 3321 · 86 |

## 6 · Kâhin

- İ'de çekirdek kâhini 2/8 tohumda `R`'den fazla aşıyor (1004 +0,017 · 1009 +0,043). Babel 4/8.
- B'de hiçbir kol kâhini aşmıyor.

## 7 · Öngörülerle karşılaştırma

| öngörü | sonuç | |
|---|---|---|
| İ'de çekirdek 0,92 ± 0,03, Babel'le ayırt edilemez | 0,810 ± 0,187, Babel önde (7/8) | tutmadı |
| İ'de çekirdek − v0.4.1 +0,10 … +0,17, 8/8 | +0,025, 6/8 | tutmadı |
| B'de 0,66 ± 0,08, Babel'le ayırt edilemez | 0,410, Babel önde (8/8) | tutmadı |
| B'de çekirdek − v0.4.1 +0,03 … +0,15 | −0,157 | tutmadı |
| `Δ_k(çekirdek)` −0,22 … −0,32 | −0,391 | tutmadı |
| `Δ_k` farkı ayırt edilemez | ayırt edilemedi | tuttu |
| kontrol kanal süresi İ'de 6–20 s | 34,6 s (Babel'in yarısı) | aralık tutmadı, yön tuttu |
| 5 s tavanın bedeli < 0,01 | 0,004 · 0,002 | tuttu |
| p99 İ'de 0,2–1,0 s · B'de 1,0–3,0 s | 3,40 · 3,81 s | tutmadı |
| İ'de R 0,000–0,02 · İ 0,05–0,09 | 0,139 · 0,049 | R tutmadı, İ tuttu |
| B açıkta R 0,02–0,10 · İ 0,20–0,32 | 0,512 · 0,077 | tutmadı |
| İ'de atlama başarısızlığı %1,5–%3,5 · karar/paket 3,0–3,9 · `g` 0,46–0,54 | %1,45 · 3,69 · 0,509 | tutmadı (aralığın hemen altında, Babel'den iyi) · tuttu · tuttu |
| İ'de açlık < 40 · tur artışı ≤ 10 | 822 · 92 | tutmadı |
| veriyle KÖTÜ İ'de 20–300; B'de en az 1,5 kat | 399 · 482 (1,2 kat) | tutmadı |
| İ'de kâhini 1–5 tohumda aşar; B'de aşmaz | 2/8; aşmıyor | tuttu |

## 8 · Kuraldan sonra görülenler (karar girdisi değil)

`ek_hesap.txt` (tohum başına sayaçlar):
- **Açığı açlık belirliyor.** İkizde teslim ile açlık sayısı arasında Pearson r = −0,97; ardıl değişimiyle −0,95. B'de −0,87 · −0,83.
  - Çöken tohum 1005'te İ 0,401: koşu başına 2151 açlık, R kaybı 0,483.
  - 1004'te İ 0,978 (Babel 0,954, kâhin 0,961): 90 açlık, R kaybı 0,001.
- **Tur artışı her tohumda yüksek** (İ'de 55–120), ama teslimle zayıf ilişkili (r = −0,46). En iyi tohumda da 55 kez arttı.
- **İletim Babel'inkinden iyi:**
  - İ kaybı 0,049 (Babel 0,070), atlama başarısızlığı %1,45 (Babel %2,22), deneme başarısı 0,509 (Babel 0,469).
  - Kontrol kanal süresi Babel'in yarısı.

  Açığın tamamı rota yokluğunda (R).
- **Varsayım (ölçülmedi):**
  - Bağlar sık kullanımdan çıkıyor: selamın iki eşiği, veri tetiği ve cezası, bayatlayan `d_f`, silme. Babel bu durumda bağı tutup daha pahalı yoldan göndermeyi sürdürür.
  - Ardıl gidince uygulanabilirlik koşulunu geçen yedek çoğu zaman yok, çünkü FD önceki iyi ilanlarla düşmüş. Düğüm ∞ ilan eder ve altındakiler de aç kalır.
  - Yeni tur yalnız olağan selamla, atlama başına en çok 2,2 s'de yayılıyor (denetimin Z-2'si). Yeni turu erken alan düğümün eski turdaki komşuları uygulanamaz kalıyor; bu da yeni açlıklar ve yeni tur istekleri doğurabilir (`17` §7 madde 10).
  - Bekletme 2 s; ikizde ortalama açlık 1,9 s, B'de 3,1 s.

  Bu zincirin hangi halkasının ağır bastığı sıradaki teşhisin sorusu.
