# Faz 5-2 · rakiplerin, kâhinin ve v0.4.1'in üç geliştirme hücresindeki çizgisi — sonuç

> 16 Kasım 2026 · ölçüt `beklenti.md` (commit `ef6d5cb`, koşudan önce) · koşu (`zaman.txt`): ikiz 15 Kasım 12:53–19:20 (6 sa 26 dk) · birincil 19:20–02:26 (7 sa 6 dk) · dayanıklılık 02:26–08:34 (6 sa 8 dk) · v0.4.1 ikiz 08:34–10:26 (1 sa 52 dk) · v0.4.1 birincil ve dayanıklılık 10:26–14:26 (4 sa); toplam 25 sa 32 dk (tahmin 22 ± 3 sa; AODV-k'nin koşuları koşu başına 2,4–3,7 sa sürdü) · `kopya/` = `ef6d5cb` (150 dosya birebir; satır sonları normalleştirilerek karşılaştırıldı, `kopya_ozet.txt`) · ham çıktı `anatomi_*.txt`, kayıt `kayit_*.json` · karar kuralının uygulanması `sonuc_hesap.py` → `sonuc_hesap.txt` · ek sayılar `ek_hesap.py` → `ek_hesap.txt` (koşudan sonra yazıldı, karar girdisi değil).

Hücreler (hepsi `formasyon · yere_toplama`, tam pencere): **İ** karıştırıcısız ikiz, ölçü pencere PDR'si · **B** birincil (araç, 15 s açık · 15 s sessiz, açıkken 20 W), ölçü `PDR_açık` · **D** dayanıklılık (10 s açık · 20 s sessiz, açıkken 30 W; ortalama ikisinde de 10 W), ölçü `PDR_açık`. Tohum 1003–1010. 5 kol × 3 hücre × 8 tohum = 120 koşu.

## 0 · Geçerlilik ✓

120/120 koşu kayıtta · korunum geçerli · doğum çelişkisi 0 · atfsız düşüş yok · aletin iç denetimleri geçti (çizelgeli 80 koşuda ikincil sayım aletin evre sayımına eşit) · ikincil sayımın pencere PDR'si satırınkiyle 120/120 aynı. Önceki kayıtlarla birebir (altı basamak): İ'de ikinci teşhisle 12/12 · B'de ilk teşhisle 24/24 (pencere PDR'si ve `PDR_açık`) · B'de K-244 G2ç ile 10/10 · İ'de hayalet `PDR_açık` K-244 G1ç ve G2ç boş koluyla 10/10.

## 1 · Düzeyler (8 tohum ortalaması ± ölçüt sapması)

| kol | İ · pencere PDR | B · `PDR_açık` | D · `PDR_açık` |
|---|---|---|---|
| kâhin | 0,917 ± 0,029 | 0,779 ± 0,077 | 0,685 ± 0,053 |
| Babel | 0,930 ± 0,030 | 0,663 ± 0,139 | 0,554 ± 0,090 |
| OLSRv2 | 0,809 ± 0,089 | 0,495 ± 0,110 | 0,413 ± 0,080 |
| v0.4.1 | 0,785 ± 0,040 | 0,567 ± 0,085 | 0,453 ± 0,100 |
| AODV-k | 0,525 ± 0,066 | 0,396 ± 0,089 | 0,358 ± 0,082 |

Tohum başına:

| İ | 1003 | 1004 | 1005 | 1006 | 1007 | 1008 | 1009 | 1010 |
|---|---|---|---|---|---|---|---|---|
| kâhin | 0,896 | 0,961 | 0,898 | 0,895 | 0,961 | 0,916 | 0,893 | 0,914 |
| Babel | 0,944 | 0,954 | 0,863 | 0,918 | 0,957 | 0,940 | 0,943 | 0,923 |
| OLSRv2 | 0,800 | 0,895 | 0,616 | 0,770 | 0,887 | 0,857 | 0,806 | 0,838 |
| v0.4.1 | 0,752 | 0,797 | 0,718 | 0,804 | 0,856 | 0,795 | 0,787 | 0,771 |
| AODV-k | 0,514 | 0,616 | 0,384 | 0,517 | 0,562 | 0,550 | 0,526 | 0,529 |

| B | 1003 | 1004 | 1005 | 1006 | 1007 | 1008 | 1009 | 1010 |
|---|---|---|---|---|---|---|---|---|
| kâhin | 0,748 | 0,844 | 0,657 | 0,825 | 0,900 | 0,783 | 0,764 | 0,710 |
| Babel | 0,547 | 0,787 | 0,485 | 0,764 | 0,834 | 0,668 | 0,731 | 0,488 |
| OLSRv2 | 0,409 | 0,499 | 0,345 | 0,623 | 0,643 | 0,534 | 0,529 | 0,379 |
| v0.4.1 | 0,518 | 0,603 | 0,446 | 0,662 | 0,669 | 0,562 | 0,611 | 0,464 |
| AODV-k | 0,353 | 0,421 | 0,214 | 0,447 | 0,475 | 0,451 | 0,465 | 0,340 |

| D | 1003 | 1004 | 1005 | 1006 | 1007 | 1008 | 1009 | 1010 |
|---|---|---|---|---|---|---|---|---|
| kâhin | 0,659 | 0,667 | 0,605 | 0,772 | 0,739 | 0,697 | 0,697 | 0,645 |
| Babel | 0,411 | 0,546 | 0,510 | 0,675 | 0,614 | 0,583 | 0,632 | 0,460 |
| OLSRv2 | 0,282 | 0,390 | 0,355 | 0,496 | 0,484 | 0,492 | 0,456 | 0,347 |
| v0.4.1 | 0,351 | 0,377 | 0,344 | 0,616 | 0,543 | 0,493 | 0,505 | 0,396 |
| AODV-k | 0,336 | 0,290 | 0,194 | 0,417 | 0,417 | 0,410 | 0,434 | 0,368 |

Karıştırıcının evreleri (8 tohum ortalaması; "önce" = açılmadan önce doğan paketler):

| kol | B önce · açık · sessiz | D önce · açık · sessiz |
|---|---|---|
| kâhin | 0,919 · 0,779 · 0,916 | 0,919 · 0,685 · 0,913 |
| Babel | 0,932 · 0,663 · 0,916 | 0,932 · 0,554 · 0,921 |
| OLSRv2 | 0,801 · 0,495 · 0,714 | 0,801 · 0,413 · 0,711 |
| v0.4.1 | 0,779 · 0,567 · 0,763 | 0,779 · 0,453 · 0,770 |
| AODV-k | 0,513 · 0,396 · 0,488 | 0,513 · 0,358 · 0,493 |

## 2 · Kayıp, kanal ve gecikme (betimleyici)

Kayıp grupları (İ'de pencerede, B ve D'de açık dönemde doğan paketlere oranla):

| kol | İ · R · İ | B · R · İ | D · R · İ |
|---|---|---|---|
| kâhin | 0,000 · 0,083 | 0,008 · 0,206 | 0,033 · 0,279 |
| Babel | 0,000 · 0,070 | 0,000 · 0,335 | 0,000 · 0,444 |
| OLSRv2 | 0,023 · 0,165 | 0,127 · 0,368 | 0,073 · 0,501 |
| v0.4.1 | 0,043 · 0,172 | 0,237 · 0,196 | 0,356 · 0,190 |
| AODV-k | 0,282 · 0,193 | 0,423 · 0,181 | 0,466 · 0,175 |

K ve T grupları her yerde 0,013'ün altında (en büyüğü OLSRv2'nin T'si, D'de 0,013).

İ hücresinde bağ ve kanal (bütün koşu, ağ toplamı, tohum ortalaması):

| kol | karar / paket | atlama başarısızlığı | `g` = `g0` × `k` | kontrol kanal süresi | toplam gönderim |
|---|---|---|---|---|---|
| kâhin | 2,51 | %3,28 | 0,434 = 0,810 × 0,536 | 19 s | 317 s |
| Babel | 3,57 | %2,22 | 0,469 = 0,910 × 0,516 | 68 s | 461 s |
| OLSRv2 | 2,88 | %5,66 | 0,399 = 0,788 × 0,507 | 63 s | 425 s |
| v0.4.1 | 2,62 | %6,52 | 0,371 = 0,823 × 0,451 | 185 s | 560 s |
| AODV-k | 2,63 | %7,37 | 0,365 = 0,806 × 0,453 | 281 s | 635 s |

Gecikmenin p99'u (pencere, 8 tohum ortalaması), İ · B · D: kâhin 0,14 · 0,33 · 0,27 s · Babel 0,23 · 1,31 · 0,72 s · OLSRv2 1,03 · 1,39 · 1,14 s · AODV-k 0,96 · 2,50 · 2,82 s · v0.4.1 2,51 · 3,67 · 3,51 s.

## 3 · Karar kuralı

0. Geçerlilik tuttu; tablolar kullanılır.
1. **S1 · üç hücrede de en güçlü rakip Babel.** Babel − OLSRv2: İ +0,122 · B +0,168 · D +0,141, üçünde de 8/8 tohumda → ayrışıyor. Rakiplerin sırası üç hücrede aynı: Babel > OLSRv2 > AODV-k (OLSRv2 − AODV-k İ +0,284 · B +0,099 · D +0,055, ayrışıyor).
   → **K-252'nin hedef cümlesi geçerli kalır.** Hedef çizgisi Babel'in bu ölçümdeki değerleri: **İ 0,930 · B 0,663 · D 0,554.**
2. **S2 · v0.4.1 üç hücrede de Babel'in gerisinde, 8/8 tohumda:**

   | hücre | `G` = Babel − v0.4.1 | tohum başına | açığın ayrımı |
   |---|---|---|---|
   | İ | **+0,145** | +0,192 · +0,157 · +0,145 · +0,113 · +0,101 · +0,145 · +0,156 · +0,152 | R +0,043 · İ +0,102 |
   | B | **+0,096** | +0,029 · +0,185 · +0,039 · +0,101 · +0,164 · +0,106 · +0,120 · +0,024 | R +0,237 · İ −0,139 |
   | D | **+0,101** | +0,060 · +0,170 · +0,165 · +0,059 · +0,071 · +0,090 · +0,127 · +0,064 | R +0,356 · İ −0,254 |

   - Karıştırıcısızda açığın %70'i iletim kaybı, %30'u rota yokluğu. Karıştırmada açığın tamamı rota yokluğu; iletimde v0.4.1 Babel'den az kaybediyor.
   - Öteki rakiplere göre: İ'de v0.4.1 OLSRv2'nin de gerisinde (+0,023, 6/8; eşiğin ve yön sayısının sınırında), B ve D'de önünde (−0,072, 8/8 · −0,040, 6/8). AODV-k'nin üç hücrede de önünde (8/8).
3. **S3 · karıştırmaya özgü kayıp** (`Δ_k` = `PDR_açık` − ikizin aynı zaman dilimindeki hayalet `PDR_açık`):

   | kol | B | D |
   |---|---|---|
   | kâhin | −0,137 | −0,233 |
   | Babel | −0,265 | −0,375 |
   | OLSRv2 | −0,313 | −0,395 |
   | v0.4.1 | −0,222 | −0,336 |
   | AODV-k | −0,136 | −0,177 |

   - `Δ_k(v0.4.1) − Δ_k(Babel)`: **B +0,042, 5/8 tohumda pozitif → 8 tohumda ayırt edilemedi.** İlk teşhisin "karıştırma altında v0.4.1 Babel'den az kaybediyor" bulgusu birincil hücrede dört tohuma özgü kalır; tasarımda dayanak yapılmaz.
   - D'de +0,038, 6/8 → ayrışıyor (eşiğin 0,008 üstünde, yön sayısının sınırında).
   - Karıştırmaya özgü kaybı en büyük kol iki hücrede de OLSRv2.
4. **S4 · beş kol da çizelgeye duyarlı (−):** `PDR_açık(D) − PDR_açık(B)` kâhin −0,094 (8/8) · Babel −0,109 (7/8) · OLSRv2 −0,082 (7/8) · AODV-k −0,038 (7/8) · v0.4.1 −0,114 (8/8). D'de en güçlü rakip değişmiyor, rakiplerin sırası aynı. Sessiz dönemin PDR'si iki hücrede aynı (fark −0,003 … +0,007).
5. **Gecikme tavanı hiçbir hücrede bağlayıcı değil:** 5 s tavanının bedeli en çok 0,010 (AODV-k, D); v0.4.1 0,001 · 0,006 · 0,008.
6. **Kâhin:** İ'de Babel kâhini 8 tohumun 4'ünde `R`'den fazla aşıyor (1003 +0,048 · 1006 +0,023 · 1008 +0,024 · 1009 +0,049; ortalama +0,013). Bu K-248'de kayıtlı desen; karar değiştirmez. B ve D'de hiçbir kol hiçbir tohumda aşmıyor. Kâhine oran İ · B · D: Babel 1,015 · 0,851 · 0,809 · v0.4.1 0,856 · 0,728 · 0,662 · OLSRv2 0,882 · 0,636 · 0,603 · AODV-k 0,572 · 0,508 · 0,523.

## 4 · Öngörüler

Düzeyler: on hücrenin onunda ölçülen değer öngörülen aralıkta ✓ (kâhin 0,917 · 0,779 · Babel 0,930 · 0,663 · OLSRv2 0,809 · 0,495 · v0.4.1 0,785 · 0,567 · AODV-k 0,525 · 0,396).

| öngörü | ölçülen | |
|---|---|---|
| Üç hücrede en güçlü rakip Babel, ikinci OLSRv2 | üçünde de | ✓ |
| Babel − OLSRv2 İ'de +0,05 … +0,11 | +0,122 | ✗ |
| Babel − OLSRv2 B'de +0,12 … +0,28 | +0,168 | ✓ |
| İkisinde de ayrışıyor | 8/8 · 8/8 | ✓ |
| Rakiplerin sırası üç hücrede aynı | aynı | ✓ |
| İ'de `G` +0,15 (±0,03), 8/8 geride | +0,145, 8/8 | ✓ |
| İ'de açığın büyüğü İ grubunda | İ +0,102 · R +0,043 | ✓ |
| B'de `G` +0,09 (±0,04), en az 6/8 geride | +0,096, 8/8 | ✓ |
| B'de açığın tamamı R'de, v0.4.1'in İ kaybı Babel'inkinden küçük | R +0,237 · İ −0,139 | ✓ |
| D'de `G` +0,05 … +0,15, geride | +0,101 | ✓ |
| B'de v0.4.1 OLSRv2'nin ve AODV-k'nin önünde (≥ +0,05) | +0,072 · +0,171 | ✓ |
| `Δ_k` kâhin −0,145 (±0,04) | −0,137 | ✓ |
| `Δ_k` Babel −0,27 (±0,06) | −0,265 | ✓ |
| `Δ_k` v0.4.1 −0,20 (±0,05) | −0,222 | ✓ |
| `Δ_k` OLSRv2 −0,39 (±0,07) | −0,313 | ✗ |
| `Δ_k` AODV-k −0,19 (±0,07) | −0,136 | ✓ |
| `Δ_k(v0.4.1) − Δ_k(Babel)` +0,04 … +0,10 ve ayrışıyor | +0,042, 5/8, ayırt edilemedi | ✗ |
| Karıştırmaya özgü kaybı en büyük OLSRv2 | OLSRv2 | ✓ |
| D'de `PDR_açık` beş kolda da B'dekinden düşük | beşinde de | ✓ |
| Fark kâhinde en küçük (−0,01 … −0,05) | −0,094; en küçük AODV-k (−0,038) | ✗ |
| Ötekilerde −0,02 … −0,10 | Babel −0,109 · OLSRv2 −0,082 · AODV-k −0,038 · v0.4.1 −0,114 | ✗ |
| Kâhin dışındaki kollarda en az ikisi çizelgeye duyarlı | dördü de | ✓ |
| D'de rakiplerin sırası değişmez | değişmedi | ✓ |
| Sessiz dönemin PDR'si D'de B'dekinden düşük değil | fark −0,003 … +0,007 | ✓ |
| 5 s tavanı hiçbir yerde bağlayıcı değil | en çok 0,010 | ✓ |
| Tavanın bedeli en büyük v0.4.1 (0,005 … 0,02); Babel, OLSRv2, kâhin < 0,005 | B'de v0.4.1 ve Babel 0,006; D'de en büyük AODV-k 0,010 | ✗ |
| B'de p99: kâhin < 1 · Babel < 1,5 · OLSRv2 1–2 · AODV-k 2–4 · v0.4.1 3,5–5,5 s | 0,33 · 1,31 · 1,39 · 2,50 · 3,67 s | ✓ |
| İ'de Babel 2–5 tohumda kâhini `R`'den fazla aşar; ortalamada 0,02 içinde | 4/8 · +0,013 | ✓ |
| B ve D'de hiçbir kol kâhini aşmaz | aşmıyor | ✓ |
| B'de Babel'in kaybının en az %90'ı İ grubunda | %99 | ✓ |
| B'de v0.4.1'in R ve İ kaybı yakın | 0,237 · 0,196 | ✓ |
| B'de AODV-k'nin R kaybı İ'den büyük | 0,423 · 0,181 | ✓ |
| B'de OLSRv2'nin R kaybı İ'den büyük | 0,127 · 0,368 | ✗ |
| İ'de `g` sırası Babel > kâhin > OLSRv2 > AODV-k; OLSRv2 0,35–0,45 · AODV-k 0,25–0,40 | 0,469 > 0,434 > 0,399 > 0,365 | ✓ |
| İ'de OLSRv2'nin kontrol kanal süresi 30–100 s | 63 s | ✓ |
| İ'de AODV-k'nin kontrol kanal süresi 40–200 s | 281 s | ✗ |

46 öngörünün 38'i tuttu, 8'i tutmadı. Tutmayanların gerekçeleri:

- **Dayanıklılık hücresinin etkisini protokolün zamanlamasından bekledim** ("açık dönem toparlanmaya yetmeyecek kadar kısa"). Kâhin de 0,094 düşüyor; düşüşün büyük kısmı kanalın kendisinden (§5).
- **OLSRv2'nin karıştırmadaki kaybını rota yokluğunda bekledim;** çoğu iletim kaybı. OLSRv2 karıştırılan bağı kullanmayı sürdürüyor.
- **AODV-k'nin kontrol yükünü küçük öngördüm:** kontrol kanal süresi v0.4.1'inkinden de fazla.
- **v0.4.1'in karıştırmaya özgü kayıpta Babel'den iyi olduğunu ilk teşhisin dört tohumuna dayanarak ayrışır diye yazdım;** sekiz tohumda yön 5/8.
- **OLSRv2'yi iki tohumdan (1003, 1004) öngördüm;** o iki tohum karıştırmada sekiz tohumun en kötülerindendi (`Δ_k` −0,408 · −0,411 ↔ ortalama −0,313).

## 5 · Kuraldan sonra görülenler (karar girdisi değil)

**Dayanıklılık hücresi iki şeyi birlikte değiştiriyor.** Açık dönem 15 s'den 10 s'ye kısalıyor, açıkken tepe güç 20 W'tan 30 W'a çıkıyor (eşit ortalama güç kuralı, K-186). Bağları önceden bilen kâhin de 0,094 düşüyor. Kâhinin düşüşüne göre bakınca (`[D − B](kol) − [D − B](kâhin)`, eşli):

| kol | kâhine oran B → D | kâhine göre sapma |
|---|---|---|
| Babel | 0,851 → 0,809 | −0,015 (5/8 eksi) |
| OLSRv2 | 0,636 → 0,603 | +0,012 (5/8 artı) |
| v0.4.1 | 0,728 → 0,662 | −0,020 (5/8 eksi) |
| AODV-k | 0,508 → 0,523 | +0,056 (8/8 artı) |

- Düşüşün büyük kısmı bütün kollarda ortak; protokole özgü kısım küçük ve yalnız AODV-k'de tutarlı (o da kâhinden az düşüyor).
- Kuralın "çizelgeye duyarlı" hükmü bu yüzden çizelgenin zamanlamasından çok güç farkını ölçüyor. 5-3'te bu hücrede bir mekanizmanın etkisi okunurken kâhinin düşüşü referans olabilir; bu, hücrenin nasıl okunacağına dair bir karar konusu.

**Karıştırmanın kaybı protokole göre farklı yere gidiyor** (açık dönemde doğan paketler, ikizin penceresine göre artış):

| kol | B · ΔR · Δİ | D · ΔR · Δİ |
|---|---|---|
| kâhin | +0,008 · +0,123 | +0,033 · +0,196 |
| Babel | 0,000 · +0,265 | 0,000 · +0,375 |
| OLSRv2 | +0,104 · +0,203 | +0,050 · +0,336 |
| v0.4.1 | +0,195 · +0,024 | +0,313 · +0,018 |
| AODV-k | +0,141 · −0,012 | +0,184 · −0,018 |

İlk teşhisin dört tohumdaki deseni sekiz tohumda ve iki hücrede yineleniyor: Babel rotayı bırakmıyor ve karıştırılan bağda paket kaybediyor; v0.4.1 rotayı bırakıyor ve paketi rota yokluğundan kaybediyor. Kâhinin kaybı da iletimde, ama Babel'inkinin yarısı kadar.

**Evreler.** Sessiz dönemde Babel, kâhin ve v0.4.1 açılmadan önceki düzeye 0,02 içinde dönüyor (v0.4.1 B'de −0,016; ilk teşhiste dört tohumda −0,029). OLSRv2 dönmüyor: B −0,087 · D −0,089.

**Açığın tohum yarılarında tutarlılığı** (`G`, 1003–1006 · 1007–1010): İ +0,152 · +0,138 · B +0,089 · +0,104 · D +0,113 · +0,088. İlk teşhislerin dört tohumdaki açığı sekiz tohumda değişmiyor.

**En zor tohum 1005:** 15 kol–hücre çiftinin 12'sinde en düşük değer bu tohumda (istisnalar: İ'de kâhin 1009, D'de Babel ve OLSRv2 1003).

**Kontrol yükü ve deneme başarısı (İ).** Ağın öteki iletimlerinden sağ çıkan pay `k`, kontrol kanal süresi en yüksek iki protokolde en düşük: AODV-k 0,453 (281 s) · v0.4.1 0,451 (185 s) ↔ Babel 0,516 (68 s) · OLSRv2 0,507 (63 s). Dört protokolde gözlem; sebep bu kayıtla ayrılmadı.

**Koşu süreleri** (8 işçi, 350 s'lik koşu, saat; İ · B · D): kâhin 0,59–0,74 · 0,76–1,07 · 0,56–0,82 · Babel 1,05–1,53 · 1,39–2,02 · 1,25–1,64 · OLSRv2 0,85–1,25 · 1,17–1,45 · 1,04–1,27 · v0.4.1 1,44–1,87 · 1,63–2,26 · 1,56–2,02 · AODV-k 2,96–3,72 · 2,67–3,37 · 2,37–3,06. AODV-k `v2/12` §3'teki tablodan (2,0–2,4 sa) uzun.

## 6 · Bundan çıkan

- **Hedef çizgisi sekiz tohumda kondu.** Üç hücrede de en güçlü rakip Babel: İ 0,930 · B 0,663 · D 0,554. K-252'nin hedef cümlesi doğrulandı; ayrı karar gerekmiyor.
- **Başlangıç çizgisi:** v0.4.1 0,785 · 0,567 · 0,453. Babel'e açık +0,145 · +0,096 · +0,101, her hücrede 8/8 tohumda.
- **Açığın yapısı iki teşhisin bulgusunu sekiz tohumda yineliyor:**
  - karıştırıcısızda açığın %70'i iletim kaybı, %30'u rota yokluğu;
  - karıştırmada açığın tamamı rota yokluğu. v0.4.1'in karıştırmaya özgü kaybının neredeyse hepsi rota yokluğu (B +0,195 · D +0,313); Babel'inki iletim kaybı.
- **"Karıştırma altında v0.4.1 Babel'den az kaybediyor" birincil hücrede doğrulanmadı** (+0,042, 5/8); dayanıklılık hücresinde sınırda geçti. Bu, tasarımda dayanak yapılmaz.
- Gecikme tavanı (5 s) hiçbir hücrede sonucu değiştirmiyor.
- Planın üç teşhis ölçümü tamamlandı. Sırada konu konu tasarım kararları.
