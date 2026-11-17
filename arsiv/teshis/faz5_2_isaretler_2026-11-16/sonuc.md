# Faz 5-2 · teşhis (d): karıştırmanın yerel işaretleri — sonuç

> 17 Kasım 2026 · ölçüt `beklenti.md` (commit `8750574`, koşudan önce) · koşu (`zaman.txt`): ikiz 16 Kasım 19:25–21:11 (1 sa 47 dk) · birincil 21:11–23:20 (2 sa 9 dk) · dayanıklılık 23:20–01:10 (1 sa 50 dk); toplam 5 sa 46 dk (tahmin 6 ± 1,5 sa) · `kopya/` = `8750574` (152 dosya birebir; satır sonları normalleştirilerek karşılaştırıldı, `kopya_ozet.txt`) · ham çıktı `isaret_*.txt`, kayıt `kayit_*.json` · karar kuralının uygulanması `sonuc_hesap.py` → `sonuc_hesap.txt` · ek sayılar `ek_hesap.py` → `ek_hesap.txt` (koşudan sonra yazıldı, karar girdisi değil).
>
> Denetimden sonra düzeltilenler (17 Kasım, `arsiv/denetim/DENETIM-RAPORU-5-2-2026-11-17.md`): §0 ve §8'deki düğüm sayıları (K-6) · S3'ün yorumu (§4, §5, §8; Ö-3) · §8'de ED kanıtının gözlem sözleşmesine uyumu (E-1). Ölçüm, kayıtlar ve karar kuralının hükümleri değişmedi.

Hücreler teşhis (c)'deki üç hücre (İ ikiz · B birincil, 15 s açık · 15 s sessiz · D dayanıklılık, 10 s açık · 20 s sessiz), kol Babel-a, tohum 1003–1010. "Karıştırılan": açık evrede ED ya da girişim alanı; "temiz": aynı koşunun önce evresi.

## 0 · Geçerlilik

- 24 koşunun hepsi kayıtta, korunum geçerli, hiçbir koşu hata vermedi (kaydedicinin iç eşitlikleri geçti). Koşu başına süre: İ 1,30–1,78 · B 1,59–2,14 · D 1,52–1,84 sa.
- **Birebirlik tam:** 24 koşunun geçerliliği, PDR'si, pencere PDR'si, üretilen ve teslim sayısı ve bütün simülatör sayaçları teşhis (c)'nin aynı hücre ve tohumdaki Babel satırıyla aynı. Kaydedici Babel'in davranışını değiştirmedi.
- Sınıf büyüklüğü (düğüm-saniye, 8 tohum): B'de açık evrede ED 624 · girişim 4 929 · uzak 23 247; D'de 529 · 4 948 · 13 723; temiz B ve D'de 32 000; ikiz 86 400. Açık evrede ortalama düğüm sayısı B'de ED 0,9 · girişim 6,8, D'de 1,1 · 10,3 (açık süre B'de 90, D'de 60 s).

## 1 · S1a · düğüm-saniye işaretleri

Ayırma gücü `G = max(AUC, 1 − AUC)`; yön "+" karıştırılanda büyük. Tohum: tohum başına yönün havuzdaki yönle aynı olduğu tohum sayısı.

| alan | işaret | B: G · yön · tohum | D: G · yön · tohum | hüküm |
|---|---|---|---|---|
| ED | `mesgul` | 0,978 · + · 8/8 | 0,976 · + · 8/8 | güçlü |
| ED | `aciklanamayan` | 0,997 · + · 8/8 | 0,996 · + · 8/8 | güçlü |
| ED | `phy` | 0,972 · − · 8/8 | 0,974 · − · 8/8 | güçlü |
| ED | `cozulen` | 0,982 · − · 8/8 | 0,984 · − · 8/8 | güçlü |
| ED | `sessizlik` | 0,911 · + · 8/8 | 0,903 · + · 8/8 | güçlü |
| ED | `selam_kaybi` | 0,937 · + · 8/8 | 0,919 · + · 8/8 | güçlü |
| girişim | `mesgul` | 0,736 · − · 8/8 | 0,730 · − · 8/8 | zayıf |
| girişim | `aciklanamayan` | 0,638 · − · 8/8 | 0,604 · − · 7/8 | dışarıda |
| girişim | `phy` | 0,724 · − · 8/8 | 0,702 · − · 8/8 | zayıf |
| girişim | `cozulen` | 0,812 · − · 8/8 | 0,834 · − · 8/8 | güçlü |
| girişim | `sessizlik` | 0,596 · + · 8/8 | 0,595 · + · 8/8 | dışarıda |
| girişim | `selam_kaybi` | 0,842 · + · 8/8 | 0,852 · + · 8/8 | güçlü |

Karıştırılanların %80'ini yakalayan eşik ve o eşikte karıştırıcısız ikizin düğüm-saniyelerinde yanlış alarm (B · D):

| alan | işaret | eşik | ikizde yanlış alarm |
|---|---|---|---|
| ED | `aciklanamayan` | ≥ 0,58 | %0,000 · %0,000 |
| ED | `mesgul` | ≥ 0,62 | %0,035 · %0,035 |
| ED | `cozulen` | ≤ 9 · ≤ 14 çerçeve/s | %0,10 · %0,36 |
| ED | `phy` | ≤ 6 · ≤ 8 | %0,29 · %0,79 |
| ED | `sessizlik` | ≥ 0,1 s | %1,8 · %1,8 |
| ED | `selam_kaybi` | ≥ 0,65 · ≥ 0,60 | %9,9 · %17,7 |
| girişim | `cozulen` | ≤ 81 · ≤ 72 çerçeve/s | %39,0 · %31,9 |
| girişim | `selam_kaybi` | ≥ 0,50 | %40,8 · %40,8 |
| girişim | `mesgul` | ≤ 0,32 | %54,5 · %54,5 |
| girişim | `phy` | ≤ 36 · ≤ 37 | %56,1 · %58,8 |

Karıştırılmayan sınıflar ↔ temiz, en büyük G: açık evrede uzak alan 0,710 (D'de `cozulen`; B'de 0,652) · sessiz evre 0,603 · ikiz 0,504.

## 2 · S1b · bağ düzeyinde tutarlılık

Düşük teslimli (deneme başarısı < 0,5) bağ birimlerinde RSSI'ın AUC'si, karıştırılan alıcı ↔ temiz: B 0,705 (8/8) · D 0,708 (8/8) → **zayıf**. Düşük teslimli birimin payı: karıştırılanda %66,0 · %69,7, temizde %33,7.

## 3 · S2 · art arda MAC vazgeçmesi

`r_n` = uzunluğu ≥ n olan vazgeçme dizisi / çerçeve:

| sınıf | n = 1 | 2 | 3 | 4 | 5 | çerçeve başına deneme |
|---|---|---|---|---|---|---|
| ikiz | 1,82e-2 | 2,42e-3 | 5,90e-4 | 1,82e-4 | 6,61e-5 | 1,98 |
| B temiz | 1,76e-2 | 2,27e-3 | 5,53e-4 | 1,96e-4 | 8,40e-5 | 1,98 |
| B ED | 1,58e-1 | 8,02e-2 | 5,04e-2 | 3,70e-2 | 3,08e-2 | 6,34 |
| B girişim | 1,10e-1 | 4,76e-2 | 2,61e-2 | 1,75e-2 | 1,28e-2 | 3,93 |
| B uzak (açık) | 3,79e-2 | 9,78e-3 | 4,35e-3 | 2,45e-3 | 1,61e-3 | 2,26 |
| D temiz | 1,76e-2 | 2,26e-3 | 5,60e-4 | 2,03e-4 | 9,09e-5 | 1,98 |
| D ED | 1,48e-1 | 7,61e-2 | 6,11e-2 | 4,66e-2 | 3,93e-2 | 6,55 |
| D girişim | 1,15e-1 | 5,09e-2 | 2,97e-2 | 1,98e-2 | 1,38e-2 | 3,95 |
| D uzak (açık) | 4,77e-2 | 1,27e-2 | 5,76e-3 | 3,24e-3 | 2,19e-3 | 2,39 |

Tespit süresi (ED ve girişim birlikte; ortanca · dönem içinde ulaşılan pay; B'de 1 396, D'de 1 893 bağ-dönem):

| n | B | D |
|---|---|---|
| 1 | 3,63 s · %48 | 2,06 s · %47 |
| 2 | 4,96 s · %26 | 2,87 s · %25 |
| 3 | 5,56 s · %18 | 2,82 s · %18 |
| 4 | 5,46 s · %14 | 3,69 s · %14 |
| 5 | 5,81 s · %12 | 4,17 s · %11 |

`n* = 3` (temizde ve ikizde `r_3` ≤ 0,001 olan en küçük n).

## 4 · S3 · bağ kalitesinin değişim hızı (ikiz, kâhin)

Her tohumda en çok veri kararı taşıyan 80 bağ. Bant değişim oranı τ = 1 · 2 · 4 · 8 · 16 · 32 s'de %0,3 · %0,3 · %0,3 · %0,2 · %0,3 · %0,3; ortalama |Δp| her τ'da 0,001. Bant değişimi ≤ %10 olan en uzun τ: 32 s (ölçülen en uzun gecikme). Ölçü kâhinin 7 denemelik atlama başarısıdır ve doymuştur: tek deneme başarısı 0,28'in üstündeki bağ "iyi" banttadır.

## 5 · Karar kuralı

0. **Geçerlilik:** 24/24 koşu geçerli, birebirlik 24/24. Tablolar kullanılır.
1. **S1a:**
   - ED'de altı işaretin altısı **güçlü**: `mesgul` (+) · `aciklanamayan` (+) · `phy` (−) · `cozulen` (−) · `sessizlik` (+) · `selam_kaybi` (+).
   - Girişimde `cozulen` (−) ve `selam_kaybi` (+) **güçlü**; `mesgul` (−) ve `phy` (−) **zayıf**; `aciklanamayan` ve `sessizlik` **dışarıda**.
   - Kurala göre güçlü işaret T-5'in kanıtına tek başına, zayıf işaret yalnız birlikte girer, dışarıda kalan girmez. Eşikler ve ikizdeki yanlış alarm §1'de; kural kâğıdının girdisidir.
2. **S1b:** tutarlılık kuralı **zayıf** (AUC 0,705 · 0,708). T-5'in "teslim + sinyal tutarlılığı" maddesi yalnız başka işaretle birlikte girer.
3. **S2:** `n* = 3`; B'de tespit süresinin ortancası 5,56 s, D'de 2,82 s; ulaşılan pay iki hücrede de %18 → **"olay sayısı tek başına yetmez, T-5'in işaretleriyle birleşir"**. T-10'un "birkaç"ının ilk değeri 3.
4. **S3:** bant değişimi ölçülen en uzun gecikmede (32 s) bile %0,3; selam aralığının üst sınırına girdi: en çok kullanılan bağların 7 denemelik atlama başarısı 32 s içinde bant değiştirmiyor.
5. **Karıştırılmayanlar:** sessiz evre (0,603) ve ikiz (0,504) temizden ayrışmıyor. Açık evrede uzak alan `cozulen`de ayrışıyor (B 0,652 · D 0,710): karıştırılan komşular susunca uzaktaki düğüm de daha az çerçeve duyuyor.

## 6 · Öngörüler (24; 14 ✓ · 10 ✗)

| # | öngörü | ölçülen | |
|---|---|---|---|
| 1 | ED · `mesgul` G ≥ 0,95, + | 0,978 · 0,976, + | ✓ |
| 2 | ED · `aciklanamayan` G ≥ 0,90, + | 0,997 · 0,996, + | ✓ |
| 3 | ED · `cozulen` G ≥ 0,90, − | 0,982 · 0,984, − | ✓ |
| 4 | ED · `sessizlik` G ≥ 0,90, + | 0,911 · 0,903, + | ✓ |
| 5 | ED · `selam_kaybi` G ≥ 0,85, + | 0,937 · 0,919, + | ✓ |
| 6 | ED · `phy` −, G < 0,80 | −, 0,972 · 0,974 | ✗ |
| 7 | girişim · `mesgul` G < 0,70 | 0,736 · 0,730 (−) | ✗ |
| 8 | girişim · `selam_kaybi` G ≥ 0,75, + | 0,842 · 0,852, + | ✓ |
| 9 | girişim · `cozulen` G ≥ 0,70, − | 0,812 · 0,834, − | ✓ |
| 10 | girişim · `phy` +, G ≥ 0,65 | yön − (0,724 · 0,702) | ✗ |
| 11 | girişim · `aciklanamayan` 0,60 ≤ G < 0,85, + | 0,638 · 0,604, yön − | ✗ |
| 12 | ED'de ≥ 3 güçlü; girişimde güçlü ≤ 1 | ED 6 · girişim 2 | ✗ |
| 13 | D'nin G'si B'ninkinden büyük ya da eşit, çoğunda | 12 işaretin 4'ünde | ✗ |
| 14 | açık · uzak ↔ temiz: hepsinde G < 0,65 | en büyük 0,710 | ✗ |
| 15 | sessiz ↔ temiz: hepsinde G < 0,65 | en büyük 0,603 | ✓ |
| 16 | ikiz ↔ temiz: hepsinde G < 0,60 | en büyük 0,504 | ✓ |
| 17 | S1b AUC ≥ 0,75 | 0,705 · 0,708 | ✗ |
| 18 | düşük teslim payı karıştırılanda ≥ 3 kat | 1,96 · 2,07 kat | ✗ |
| 19 | temizde `r_1` %1–%5 | %1,76 · %1,76 | ✓ |
| 20 | `n*` 2 ya da 3 | 3 | ✓ |
| 21 | karıştırılanda `r_3` temizin ≥ 10 katı | ED 91 · 109, girişim 47 · 53 kat | ✓ |
| 22 | n = 3'te ortanca ≤ 3 s ve pay ≥ %50 | 5,56 · 2,82 s; %18 · %18 | ✗ |
| 23 | S3: τ = 4 s'de ≤ %5, τ = 16 s'de ≤ %10 | %0,3 · %0,3 | ✓ |
| 24 | birebirlik 24/24 | 24/24 | ✓ |

Tutmayan öngörülerin gerekçesi:
- **Girişimde kanal meşguliyetinin artacağını sanmıştım; azalıyor** (ortalama 0,20 ↔ temiz 0,31). Girişim alanında karıştırıcının gücü ED eşiğinin altında, yani kanalı doğrudan meşgul göstermiyor. Komşuların çerçevelerine kilitlenme ise azalıyor. CRC hatası da aynı sebeple azalıyor (24 ↔ 36/s): gövdesi bozulan çerçeveden çok, önbelgesine hiç kilitlenilemeyen çerçeve artıyor. Kanal doluluğuna bakan bir protokol girişim alanını "boş" sanar.
- **ED'de CRC hatasının azalmasını öngörmüştüm, ama bu kadar güçlü ayıracağını değil** (4,6 ↔ 36/s).
- **Tutarlılık zayıf**, çünkü düşük teslimli bağlar iki durumda da menzil sınırında. RSSI ortancası karıştırılanda −93, temizde −95 dBm; fark, ölçüm hatası (σ 2 dB) düzeyinde. Temizde de bağ birimlerinin üçte biri düşük teslimli: kanal kalabalık.
- **MAC vazgeçmesi yavaş ve seyrek.** Alıcısı karıştırılan bağların yarısı açık dönem boyunca tek bir vazgeçme bile görmüyor.

## 7 · Kuraldan sonra görülenler (karar girdisi değil; `ek_hesap.txt`)

- **ED bölgesi, düğümün kendi ölçümüyle ve tek saniyede tanınıyor.**
  - Kanal meşguliyetinin çözülen çerçevelerle açıklanamayan kısmı 0,83 (temiz 0,11), çözülen çerçeve 8/s (temiz 99/s).
  - Açıklanamayan meşguliyet ≥ 0,58 eşiği karıştırılanların %80'ini yakalıyor, ikizde hiç yanlış alarm vermiyor.
  - Ama ED'deki düğüm kanalı meşgul gördüğü için gönderemez. Bunu kendisi bildiremez; komşuları onun sessizliğinden anlar (T-6).
- **Girişim bölgesinde tek bir saniye ve tek bir işaret yetmiyor.** En iyi iki işaret çözülen çerçeve düşüşü (49 ↔ 99/s) ve selam kaybı (0,69 ↔ 0,44). Yakalama payı düştükçe ikizdeki yanlış alarm şöyle azalıyor:

  | yakalama | çözülen çerçeve | selam kaybı |
  |---|---|---|
  | %80 | %32–39 | %41 |
  | %50 | %10,5 | %5,9 |
  | %35 | %3,1 | %3,4 |
  | %20 | %0,4–0,5 | %0,6–1,6 |

  Birkaç saniyeyi ve birkaç işareti birlikte okuyan bir kural gerekiyor. Bu kayıt yalnız işaret başına dağılımları tuttuğu için birleşik kuralın başarısı buradan hesaplanamıyor.
- **Çözülen çerçeve düşüşü karıştırmaya özgü değil.** Açık evrede uzak alandaki düğüm de daha az çerçeve duyuyor (76 · 68 ↔ 99/s), çünkü karıştırılan komşuları susuyor. Düğümün kendi yakın geçmişine göre düşüş belki daha iyi ayırır; bu ölçülmedi.
- **Tespit süresi alana göre** (n = 3; ortanca · ulaşılan pay): ED'de B 2,90 s · %31, D 2,45 s · %32; girişimde B 5,72 s · %17, D 3,14 s · %17. Tek vazgeçmeye (n = 1) bile ED'deki bağların %72'si, girişimdekilerin %44–46'sı ulaşıyor.
- **Sessiz evrede girişim alanında kanal hareketli:** çözülen çerçeve 142/s (temiz 99), meşguliyet 0,42 (temiz 0,31). Karıştırma sırasında biriken trafik karıştırıcı susunca boşalıyor.
- **Temizde selam kaybı yüksek** (0,44). "Tanıdık" tanımı (son 16 s'de bir kez duyulmuş) menzil sınırındaki komşuları da kapsıyor.
- **S3'ün sınırı:** bağlar en çok kullanılanlardan seçildi (çoğu "iyi" bantta) ve kâhinin ölçüsü ağın öteki iletimlerini içermiyor. Sonuç, bağın kendi kalitesinin hareketle değişmediğini söylüyor; kanal yükünün değişimini söylemiyor.

## 8 · Bundan çıkan (tasarıma girdi)

- **T-5:**
  - ED bölgesi için kanıt düğümün kendi ölçümünden gelir: kanal meşguliyeti, çözülen çerçeve, CRC hatası. Açıklanamayan kanal meşguliyeti çözülen çerçevenin hava süresini ister; bu süre gözlem sözleşmesinde yok.
  - Girişim bölgesi için güçlü iki işaret çözülen çerçeve düşüşü ve selam kaybı; zayıf iki işaret kanal meşguliyetinin ve CRC hatasının düşmesi.
  - Girişimde kanıt birkaç işareti ve birkaç saniyeyi birlikte okumalı. Kuralın biçimi ve eşikleri 5-3'ün kural kâğıdında, A/B ile.
  - Sinyal tutarlılığı (RSSI) yalnız birlikte girer.
  - Girişimde son çözümden beri geçen süre ve açıklanamayan meşguliyet kanıta girmez.
- **T-6:** ED'deki düğüm kendi karıştırılmasını kesin bilir ama bildiremez; bu yüzden komşuların "sessizleşen komşu" kanıtı gerekli (komşu başına ölçülmedi). Kanıtın asıl işi girişim bölgesinde: açık evrede orada ortalama 6,8 (B) · 10,3 (D) düğüm, ED'de 0,9 · 1,1.
- **T-10:** art arda üç MAC vazgeçmesi yanlış alarmı çerçevelerin %0,06'sının altında tutuyor, ama tek başına geç ve seyrek. "Karıştırılıyor" kararı MAC vazgeçmesini T-5'in işaretleriyle birlikte okumalı.
- **T-1:** en çok kullanılan bağların 7 denemelik atlama başarısı 32 s içinde bant değiştirmiyor. Ölçü doymuş ve selamın ölçtüğü tek deneme başarısı ölçülmedi; bu yüzden selam aralığının üst sınırı için tek başına yetmez.
- **Kanal doluluğu girişim bölgesinde ters işaret veriyor** (karıştırılan alan daha "boş" görünür). T-4'ün yük ölçüsünü maliyete koymama kararı bunu da destekliyor.
