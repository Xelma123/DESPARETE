# Faz 5-3 · döngü kuralları: geri gönderme yasağı ve sınırlı yükselme, karıştırıcısız ikizde ve birincil hücrede — sonuç

> 24 Kasım 2026 · ölçüt `beklenti.md` (öngörüler ve karar kuralı commit `520319e`, dumandan önce; duman notu commit `9920d2e`) · koşu (`zaman.txt`): 00:51–04:52 (4 sa 1 dk; adımlar 51 dk – 1 sa 9 dk; tahmin ~4,5 sa) · `kopya/` = `9920d2e` (166 dosya birebir, satır sonları normalleştirilerek; `kopya_ozet.txt`) · ham çıktı `olcum_*.txt`, kayıt `kayit_*.json` · karar kuralı `sonuc_hesap.py` → `sonuc_hesap.txt` · ek sayılar `ek_hesap.py` → `ek_hesap.txt` (koşudan sonra yazıldı, karar girdisi değil). 19 Kasım çekirdeği ve eğim0 yeni çekirdeğin ölçümünün, Babel ve kâhin teşhis (c)'nin kayıtlarından.

## 0 · Geçerlilik ✓

- 32 koşunun hepsi kayıtta. Korunum geçerli, kusur yok; kaydedicinin iç denetimleri 32 koşuda da geçti.
- Karşılaştırma satırları 16'şar (19 Kasım, eğim0, Babel, kâhin).
- Duman koşusunda kaydedicili ve kaydedicisiz geri+sınır iki hücrede bütün alanlarda birebirdi; 19 Kasım çekirdeği iki hücrede yeni çekirdeğin dumanıyla birebirdi (beklenti, son bölüm).

## 1 · Düzeyler (8 tohum ortalaması ± ölçüt sapması)

| kol | İ · pencere PDR | İ · en kötü | B · `PDR_açık` | B · en kötü | B · sessiz | B · p99 | döngü dönüşü / koşu (İ · B) |
|---|---|---|---|---|---|---|---|
| kâhin | 0,917 ± 0,029 | 0,893 | 0,779 ± 0,077 | 0,657 | 0,916 | 0,33 s | — |
| Babel | 0,930 ± 0,030 | 0,863 | 0,663 ± 0,139 | 0,485 | 0,916 | 1,31 s | — |
| eğim0 | 0,943 ± 0,023 | 0,905 | 0,665 ± 0,141 | 0,470 | 0,911 | 1,08 s | 0 · 0 |
| 19 Kasım | 0,954 ± 0,020 | 0,911 | 0,663 ± 0,199 | 0,314 | 0,854 | 1,77 s | 73 · 3620 |
| **geri** | **0,948 ± 0,037** | 0,860 | **0,666 ± 0,156** | 0,412 | 0,826 | 1,49 s | 275 · 3163 |
| **geri+sınır** | **0,958 ± 0,013** | 0,937 | **0,659 ± 0,156** | 0,408 | 0,863 | 1,24 s | 10 · 1014 |

> **28 Kasım düzeltmesi** (yeni tasarımın bağımsız denetimi, Ö-2; `arsiv/denetim/DENETIM-RAPORU-TASARIM-2026-11-28.md`): eğim0 satırındaki "0 · 0" bir ölçüm değil. eğim0'ın kayıtlarında (`arsiv/teshis/faz5_3_yeni_cekirdek_2026-11-19/kayit_egim0_{ikiz,birincil}.json`, 16 koşu) `rota.dongu` sayacı yok; sayacı yalnız eğim modülü tutuyordu. `sonuc_hesap.py`'nin `sayac` işlevi eksik anahtara 0 döndürüyordu. Kayıtlarda sayacın yokluğu 28 Kasım'da yeniden denetlendi. Döngüsüzlüğün dayanağı RFC 8966 §2.4'ün ispatıdır.

Tohum başına:

| | 1003 | 1004 | 1005 | 1006 | 1007 | 1008 | 1009 | 1010 |
|---|---|---|---|---|---|---|---|---|
| İ · geri | 0,970 | 0,972 | 0,860 | 0,944 | 0,977 | 0,956 | 0,956 | 0,951 |
| İ · geri+sınır | 0,965 | 0,972 | 0,937 | 0,948 | 0,976 | 0,958 | 0,955 | 0,953 |
| B · geri | 0,564 | 0,724 | 0,412 | 0,807 | 0,875 | 0,690 | 0,739 | 0,514 |
| B · geri+sınır | 0,541 | 0,672 | 0,408 | 0,817 | 0,870 | 0,675 | 0,749 | 0,538 |

## 2 · S1 — geri gönderme yasağı (betimleyici)

`geri − 19 Kasım`:
- İ: −0,006 (2/8 artı · 3/8 eksi; 1005 −0,051) → 8 tohumda ayırt edilemedi. Döngü dönüşü 73 → 275.
- B: +0,003 (3/8 · 5/8; 1004 −0,096 · 1005 +0,097) → ayırt edilemedi. Döngü dönüşü 3620 → 3163.

## 3 · S2 — sınırlı yükselme (betimleyici)

`geri+sınır − geri`:
- İ: +0,010 (4/8 · 3/8; 1005 +0,077) → ayırt edilemedi. Döngü dönüşü 275 → 10.
- B: −0,007 (3/8 · 5/8) → ayırt edilemedi. Döngü dönüşü 3163 → 1014.

## 4 · S3 — eğim0 düzeyi (karar)

| ölçüt | geri | geri+sınır |
|---|---|---|
| K1 · B'de − eğim0 eksi yönde ayrışmıyor | +0,001 → tamam | −0,006 → tamam |
| K2 · İ'de − eğim0 ve − 19 Kasım eksi yönde ayrışmıyor | +0,006 · −0,006 → tamam | +0,015 · +0,004 → tamam |
| K3 · B'de en kötü tohum ≥ 0,450 | 0,412 → **tutmadı** | 0,408 → **tutmadı** |
| K4 · B'de sessiz dönem − eğim0 eksi yönde ayrışmıyor | −0,085, ayrışıyor (−) → **tutmadı** | −0,048, ayrışıyor (−) → **tutmadı** |
| K5 · B'de p99 ≤ Babel (1,31 s) | 1,49 s → **tutmadı** | 1,24 s → tamam |
| K6 · B'de döngü dönüşü ≤ 362 | 3163 → **tutmadı** | 1014 → **tutmadı** |

**Hüküm: hiçbir kol eğim0 düzeyinde değil.** İki kural eğimi döngüden kurtarmadı. Karar kuralının 3. maddesi gereği yol seçiminde uygulanabilirlik koşuluna dönüş konuşulur; bu, yeniden tasarımın girdisidir.

## 5 · S4 — tanı (betimleyici; koşu başına, bütün koşu, ağ toplamı)

| sayaç (B) | 19 Kasım | geri | geri+sınır |
|---|---|---|---|
| döngü dönüşü · dışlama | 3620 · 5619 | 3163 · 5439 | 1014 · 1781 |
| tavan aşımı | 26,5 | 40,2 | 2,5 |
| son çare · zorunlu geçiş | 141 · 476 | 120 · 434 | 101 · 402 |
| yol yok · ortalama süresi | 117 · 2,21 s | 104 · 2,31 s | 136 · 2,67 s |
| başka adaya yönlendirilen · bekletilen karar (kural 13) | — | 417 · 3014 | 136 · 991 |
| yükselme kopması (kural 14) | — | — | 141 |
| bayat bilgi · ara ilan | 595 · 2343 | 788 · 2646 | 416 · 2107 |
| açık dönem kaybı R · İ · K | 0,042 · 0,287 · 0,008 | 0,052 · 0,280 · 0,002 | 0,066 · 0,267 · 0,008 |
| kaynağın ∞ payı · teslimde ≥ 12 atlama · kararlarda en çok atlama | 0,023 · 0,0083 · 60 | 0,023 · 0,0063 · 49 | 0,033 · 0,0025 · 29 |

İkizde geri+sınırda döngü dönüşü 10, tavan aşımı 0, yükselme kopması 10, kararlarda en çok 13 atlama; geride döngü 275, tavan 1,9.

Ömür (TTL) kaybı bütün kollarda 0. Kontrol payı İ'de %5,9, B'de %5,6 (Babel %14,7 · %15,0).

B'de tohum başına döngü dönüşü:
- 19 Kasım: 1003 7827 · 1004 183 · 1005 13251 · 1006 41 · 1007 477 · 1008 3830 · 1009 326 · 1010 3027;
- geri: 10560 · 1854 · 5513 · 296 · 97 · 2039 · 1655 · 3293;
- geri+sınır: 2500 · 1277 · 2524 · 27 · 118 · 1066 · 82 · 514.

## 6 · Kâhin

- İ'de geri 6/8, geri+sınır 7/8 tohumda kâhini `R`'den fazla aşıyor (ortalama +0,032 · +0,041).
- B'de iki kol da hiçbir tohumda aşmıyor.

## 7 · Öngörülerle karşılaştırma

| öngörü | sonuç | |
|---|---|---|
| geri: İ 0,95–0,96 · B 0,66–0,69 · en kötü 0,31–0,42 · sessiz 0,85–0,88 · p99 1,4–1,9 s · döngü 2000–3000 | 0,948 · 0,666 · 0,412 · 0,826 · 1,49 s · 3163 | İ hemen altında · tuttu · tuttu · tutmadı · tuttu · hemen üstünde |
| geri+sınır: İ 0,94–0,955 · B 0,60–0,69 · en kötü 0,28–0,45 · sessiz 0,83–0,90 · p99 1,2–2,0 s · döngü 500–3000 | 0,958 · 0,659 · 0,408 · 0,863 · 1,24 s · 1014 | İ hemen üstünde · tuttu · tuttu · tuttu · tuttu · tuttu |
| S1: İ −0,005 … +0,005 · B +0,00 … +0,03, ayırt edilemedi; İ'de döngü 40–73 | −0,006 · +0,003, ayırt edilemedi; döngü 275 | aralığın hemen altında, hüküm tuttu · tuttu · tutmadı |
| S2: İ −0,01 … +0,005 · B −0,06 … +0,03, en olası ayırt edilemedi | +0,010 · −0,007, ayırt edilemedi | aralığın üstünde, hüküm tuttu · tuttu |
| sınırla B'de tavan aşımı ~0 · yükselme kopması 200–1500 · yol yok 200–600 · R 0,05–0,12 | 2,5 · 141 · 136 · 0,066 | tuttu · tutmadı (az) · tutmadı (az) · tuttu |
| S3: en olası "hiçbir kol eğim0 düzeyinde değil"; K1 ve K2 tutar, K6 tutmaz | hiçbiri; K1, K2 tuttu, K6 tutmadı | tuttu |
| geri: B'de başka adaya 200–2000 · bekletilen 300–3000 · son çare 100–160 · tavan 15–30 | 417 · 3014 · 120 · 40,2 | tuttu · sınırda · tuttu · tutmadı (fazla) |
| geri+sınır: B'de son çare 100–300 · tavan 0–5 | 101 · 2,5 | tuttu |
| TTL kaybı 0 · kontrol payı %5–7 · teslimde ≥ 12 atlama ≤ %1 | 0 · %5,6–5,9 · ≤ %0,63 | tuttu |
| kâhin: İ'de 5–8 tohumda aşar · B'de en çok birinde | 6/8 · 7/8; B'de hiç | tuttu |

Hüküm ve düzeyler öngörüldüğü gibi çıktı. Tutmayanlar: yalnız geri gönderme yasağının ikizde döngüyü artırması (öngörü 40–73, sonuç 275) ve tavana tırmanmayı artırması (öngörü 15–30, sonuç 40). İkisi de duman notundaki varsayımın yönünde (§8).

## 8 · Kuraldan sonra görülenler (karar girdisi değil)

`ek_hesap.txt`:

- **Kural 13 kural 9'un kanıtını siliyor** (duman notundaki varsayım, tam koşuda destekleniyor):
  - Yalnız geri gönderme yasağıyla B'de tavan aşımı 8 tohumun 5'inde arttı (1004 0 → 58 · 1010 19 → 80 · 1009 0 → 13 · 1003 59 → 73 · 1008 10 → 14), 1'inde azaldı (1005 124 → 84), 2'sinde 0 kaldı.
  - İkizde tohum 1005'te tavan 0 → 15, döngü dönüşü 500 → 2123, teslim 0,911 → 0,860; sınır eklenince tavan 0, döngü 0, teslim 0,937.
  - İki düğümlü dönüşlerin üst sınırı 19 Kasım'da 0,45 (B) · 0,60 (İ); geride 0,28 · 0,19. Yasak iki düğümlü dönüşleri önlüyor; ama döngü bekçisi o dönüşleri döngüyü kırmak için kullanıyordu. Kırılmayan döngü maliyetleri tavana tırmandırıyor.
  - Sonuç: kural 13, "ardılım paketi bana getirdi" anında kural 9'un tepkisini (komşuyu kısa süre dışlamak, ardılı yeniden seçmek) kendisi vermeli. Kural bunu yapmadığı için tek başına zararlı.
  - Dumanda B'de 1003 tek tohumda 0,401'e çökmüştü; tam koşuda aynı tohum 0,564 (19 Kasım 0,512). Kısa pencere çöküşün büyüklüğünü abartmıştı, yönünü değil.
- **Geri+sınır ikizde şimdiye kadarki en iyi sonuç:** 0,958 ± 0,013, en kötü tohum 0,937. Babel'den +0,028 (8/8 artı, ayrışıyor), eğim0'dan +0,015 (8/8 artı, eşiğin altında), 19 Kasım'dan +0,004. Döngü dönüşü 10.
- **Birincilde ortalamayı yol seçimi belirlemiyor.** Beş kolun ortalaması (Babel, eğim0, 19 Kasım, geri, geri+sınır) 0,659–0,666 aralığında. Açık dönem kaybının büyük kısmı iletimde (0,267–0,335); fark rota yokluğu ile iletim arasında yer değiştiriyor. Karıştırılan bağın kendisi kaybın asıl kaynağı; bu karıştırma katmanının işidir.
- **Kuyrukta ve sessiz dönemde eğim geride.**
  - En kötü tohum: eğimli kollar 0,314–0,412, eğim0 0,470, Babel 0,485.
  - Sessiz dönem: eğimli kollar 0,826–0,863, eğim0 0,911, Babel 0,916. Karıştırma bittikten sonra eğim daha yavaş toparlanıyor; iki kural bunu düzeltmedi.
  - "Önce" evresi (karıştırıcı açılmadan) eğimli kollarda 0,954–0,956, eğim0 0,940, Babel 0,932: karıştırmasız ağda eğim önde.
- **Sınırın bedeli:** B'de döngü %68 azaldı (3163 → 1014), tavana tırmanma neredeyse bitti (40,2 → 2,5), kararlarda en uzun yol 49 → 29 atlama; ama rota yokluğu kaybı arttı (0,052 → 0,066), kaynağın ∞ payı 0,023 → 0,033. Teslim değişmedi.

Bu tablo yeniden tasarımın yol seçimi sorusunu iki yönüyle koyuyor:
- **Eğim:** karıştırmasız ağda ve ikizde önde (geri+sınırla en iyi ikiz sonucu).
- **Uygulanabilirlik koşulu:** karıştırma altında kuyrukta ve sessiz dönemde önde, döngüsüz.

Hangisinin temel olacağına ve kural 13'ün düzeltilip düzeltilmeyeceğine yeniden tasarımda karar veririm.
