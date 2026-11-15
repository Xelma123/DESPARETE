# Faz 5-2 · v0.4.1'in iki kapalı seçeneği ve iletim başarısızlığının sebebi — sonuç

> 15 Kasım 2026 · ölçüt `beklenti.md` (commit `3d4dc34`, koşudan önce) · koşu: taban 01:04–03:16 (2 sa 11 dk) · seçenek 03:16–07:18 (4 sa 2 dk), `zaman.txt` · `kopya/` = `3d4dc34` (150 dosya birebir; satır sonları normalleştirilerek karşılaştırıldı, `kopya_ozet.txt`) · ham çıktı `anatomi_taban.txt` · `anatomi_secenek.txt`, kayıt `kayit_taban.json` · `kayit_secenek.json` · karar kuralının uygulanması `sonuc_hesap.py` → `sonuc_hesap.txt` · ek sayılar `ek_hesap.py` → `ek_hesap.txt` (koşudan sonra yazıldı, karar girdisi değil).

Kollar: **T** v0.4.1 · **C** `hedefli_canlilik` açık · **O** `onarim_edinimi` açık · **CO** ikisi açık · Babel · kâhin (en güvenilir yol). Hücre karıştırıcısız ikiz, tohum 1003–1006, 24 koşu.

## 0 · Geçerlilik ✓

Korunum 24/24 geçerli · doğum çelişkisi 0 · atfsız düşüş yok · aletin iki iç denetimi 24 koşuda geçti · T, Babel ve kâhin kollarının pencere PDR'si ilk ölçümün ikiz kaydıyla 12/12 birebir (altı basamak) · seçenek kollarında açık alanlar adı verilenlerle aynı, T'de ikisi de kapalı.

## 1 · S1 — seçenekler (pencere, 4 tohum havuzlanmış)

| kol | PDR | ΔPDR | R · rota yok | İ · iletim | ΔR | Δİ | 1003 | 1004 | 1005 | 1006 |
|---|---|---|---|---|---|---|---|---|---|---|
| T | 0,768 | — | 0,054 | 0,178 | — | — | 0,752 | 0,797 | 0,718 | 0,804 |
| C | 0,757 | −0,011 | 0,055 | 0,187 | +0,002 | +0,009 | 0,750 | 0,806 | 0,704 | 0,770 |
| O | 0,768 | 0,000 | 0,032 | 0,200 | −0,021 | +0,021 | 0,762 | 0,834 | 0,659 | 0,817 |
| CO | 0,768 | 0,000 | 0,030 | 0,201 | −0,023 | +0,023 | 0,765 | 0,843 | 0,670 | 0,795 |

- Tohum başına ΔPDR — C: −0,003 · +0,009 · −0,015 · −0,034 · O: +0,010 · +0,037 · −0,059 · +0,013 · CO: +0,013 · +0,046 · −0,048 · −0,010.
- K ve T grupları dört kolda 0.

Çalkantı ve kontrol trafiği (ağ toplamı, tohum ortalaması, 350 s):

| kol | silinen komşu | ardıl değişimi | onarıma giriş | ulaşılamaz | yol isteği | tur artışı | boşta yoklama | duyuru | kontrol çerçevesi | kontrol kanal süresi |
|---|---|---|---|---|---|---|---|---|---|---|
| T | 15 171 | 10 804 | 3 753 | 68 | 131 | 13 | 0 | 35 823 | 221 860 | 185 s |
| C | 13 922 | 12 212 | 3 297 | 50 | 136 | 14 | 4 227 | 36 744 | 228 239 | 191 s |
| O | 16 464 | 18 800 | 3 862 | 0 | 4 503 | 76 | 0 | 55 998 | 310 125 | 268 s |
| CO | 15 022 | 18 985 | 3 283 | 1 | 3 794 | 72 | 4 901 | 53 584 | 304 332 | 262 s |

## 2 · S2 — iletim başarısızlığı (bütün koşu, 4 tohum toplamı)

Atlama düzeyi (bir atlama yedi denemeye kadar sürer):

| kol | karar / paket | gerçekleşen `f_a` | girişimsiz beklenen `b_a` | fazla | bağımsız denemeyle `(1 − g)^7` |
|---|---|---|---|---|---|
| kâhin | 2,64 | %3,29 | %0,22 | +3,07 | %1,84 |
| Babel | 3,74 | %2,32 | %0,06 | +2,27 | %1,29 |
| T | 2,72 | %6,49 | %0,41 | +6,08 | %3,92 |
| C | 2,65 | %7,00 | %0,46 | +6,54 | %4,28 |
| O | 3,19 | %6,16 | %0,23 | +5,94 | %3,76 |
| CO | 3,11 | %6,47 | %0,23 | +6,24 | %4,19 |

Deneme düzeyi (yeniden denemeler dâhil):

| kol | deneme / karar | gerçekleşen `f_d` | beklenen `b_d` | fazla | `g` = `g0` × `k` |
|---|---|---|---|---|---|
| kâhin | 2,21 | %56,5 | %19,3 | +37,2 | 0,435 = 0,807 × 0,539 |
| Babel | 2,10 | %53,7 | %9,5 | +44,1 | 0,463 = 0,905 × 0,512 |
| T | 2,50 | %63,0 | %18,0 | +44,9 | 0,370 = 0,820 × 0,452 |
| C | 2,53 | %63,8 | %18,8 | +45,0 | 0,362 = 0,812 × 0,446 |
| O | 2,48 | %62,6 | %13,7 | +48,8 | 0,374 = 0,863 × 0,434 |
| CO | 2,53 | %63,6 | %14,5 | +49,0 | 0,364 = 0,855 × 0,426 |

Adreslenen alıcıdaki sonuç, denemeye oranla:

| kol | başarılı | meşgul | yarı çift | önbelge | gövde | duyma dışı |
|---|---|---|---|---|---|---|
| kâhin | %45,2 | %26,9 | %2,6 | %8,0 | %17,3 | 0 |
| Babel | %48,3 | %31,5 | %3,9 | %4,8 | %11,5 | 0 |
| T | %39,2 | %30,8 | %4,6 | %7,7 | %17,7 | 0 |
| C | %38,4 | %30,8 | %4,6 | %8,1 | %18,1 | 0 |
| O | %39,6 | %32,8 | %5,3 | %6,5 | %15,8 | 0 |
| CO | %38,7 | %32,7 | %5,2 | %6,8 | %16,5 | 0 |

Deneme hızı — denemelerin payı (o hızda adreslenen alıcıdaki başarı):

| kol | 1 Mb/s | 2 Mb/s | 5,5 Mb/s | 11 Mb/s |
|---|---|---|---|---|
| kâhin | %94,2 (%44,1) | %4,7 (%62,4) | %0,9 (%65,3) | %0,1 (%61,6) |
| Babel | %93,7 (%47,4) | %5,1 (%60,8) | %1,0 (%66,7) | %0,2 (%72,0) |
| T | %95,8 (%38,2) | %3,5 (%59,8) | %0,5 (%65,0) | %0,1 (%66,8) |

Kanal yükü (ağ toplamı, tohum ortalaması, 350 s). Toplam gönderim, bütün düğümlerin gönderim sürelerinin toplamıdır (onaylar dâhil); birden çok düğüm aynı anda gönderebildiği için koşu süresini aşabilir.

| kol | kontrol çerçevesi | kontrol kanal süresi | veri kanal süresi | toplam gönderim | koşu süresine oranı | veri denemesi |
|---|---|---|---|---|---|---|
| kâhin | 44 486 | 20 s | 310 s | 329 s | %94 | 74 548 |
| Babel | 97 465 | 69 s | 417 s | 485 s | %139 | 100 534 |
| T | 221 860 | 185 s | 389 s | 574 s | %164 | 86 816 |
| C | 228 239 | 191 s | 383 s | 575 s | %164 | 85 769 |
| O | 310 125 | 268 s | 453 s | 721 s | %206 | 101 203 |
| CO | 304 332 | 262 s | 452 s | 714 s | %204 | 100 714 |

## 3 · Karar kuralı

0. Geçerlilik tuttu; tablolar kullanılır.
1. **S1 · üç kol da "4 tohumda ayırt edilemedi".**
   - **C:** ΔPDR −0,011; üç tohumda negatif, −0,02 eşiğine ulaşmıyor. ΔR +0,002 ≥ 0 → **"yedeği canlı tutmak rota kaybını azaltmıyor"**: rota kaybının sebebi yedek yokluğu değil, uygulanabilirlik kuralı. Δİ +0,009.
   - **O:** ΔPDR 0,000; üç tohumda pozitif, 1005'te −0,059. ΔR −0,021 · Δİ +0,021. Yol isteği 131 → 4 503 (34 kat) · tur artışı 13 → 76 (5,8 kat).
   - **CO:** ΔPDR 0,000; ΔR −0,023 · Δİ +0,023.
   - Bu madde benimseme kararı değildir; komşuluk ve onarım konularının girdisidir.
2. **S2 · `π` = 0,44 < 0,5 → "bağın kendi kalitesi dışında".** `g(T) / g(Babel)` = 0,800 = `g0` oranı 0,906 × `k` oranı 0,882.
   - Alt ayrım: T − Babel farkının en büyüğü **önbelge + gövde** (+9,1 puan); onay kaybı +0,8 · yarı çift +0,7 · meşgul −0,7.
   - Hıza göre: denemelerin %96'sı (Babel'de %94'ü) en düşük hızda ve fark orada (başarı %38,2 ↔ %47,4); 2 Mb/s'de fark yok (%59,8 ↔ %60,8) → kuralın **"girişimle bozulma"** dalı. Hız uyarlamasıyla bağ seçiminin etkileşimi dalı desteklenmedi.
   - En düşük hızdaki deneme payı farkı +2,1 puan < 10: "hız uyarlaması iki kolda farklı çalışıyor" yazılmaz.
   - Kanal yükü: kontrol kanal süresi T / Babel = 2,69 ≥ 1,5 → **"belirgin yüksek"**.
   - Atlama düzeyi (betimleyici): `F` = +4,17 puan · `B` = +0,35 puan · `B / F` = 0,08. `f_a` üç taban kolda da bağımsız denemelerin vereceği `(1 − g)^7` değerinin 1,7–1,8 katı.
3. **Kâhin:** en iyi bağ seçimiyle de denemelerin %56,5'i başarısız; `k` = 0,539, yani bağın kendi kalitesine göre geçmesi beklenen denemelerin %46'sı geçmiyor.

## 4 · Öngörüler

| öngörü | ölçülen | |
|---|---|---|
| C: silinen komşu en az %15 azalır | −%8 | ✗ |
| C: kontrol çerçevesi en az %10 artar | +%3 | ✗ |
| C: onarıma giriş azalır | −%12 | ✓ |
| C: ΔR −0,005 … −0,02 | +0,002 | ✗ |
| C: Δİ 0 … +0,02 | +0,009 | ✓ |
| C: ayırt edilemez | ayırt edilemedi (−0,011) | ✓ |
| O: yol isteği en az 10 kat | 34 kat | ✓ |
| O: tur artışı en az 3 kat | 5,8 kat | ✓ |
| O: zararlı (ΔPDR ≤ −0,02) | 0,000, ayırt edilemedi | ✗ |
| CO: zararlı | 0,000, ayırt edilemedi | ✗ |
| `b_a` DESPARETE %0,3–1,5 · kâhin %0,1–1 · Babel ≤ %0,5 | %0,41 · %0,22 · %0,06 | ✓ |
| Gerçekleşen atlama başarısızlığının çoğu üç kolda "fazla" | fazlanın payı %94 · %93 · %98 | ✓ |
| `B / F` < 0,3 | 0,08 | ✓ |
| Alt ayrımda en büyük fark meşgul ile önbelge + gövde toplamında; yarı çift farkın %20'sinden az | önbelge + gövde +9,1 · meşgul −0,7 · yarı çift farkın %8'i | ✓ (fark yalnız önbelge + gövdede; meşgulde fark yok) |
| Başarısızlıklar kümeli; `f_d` DESPARETE'de %25–45 | `f_d` %63,0; kümelenme hafif (`f_a`, bağımsız denemenin 1,7 katı) | ✗ |
| En düşük hızdaki deneme payı T'de en az 5 puan yüksek | +2,1 puan | ✗ |
| Kontrol çerçevesi sayısı Babel'in 1,2–2 katı | 2,28 katı | ✗ |
| Kontrol kanal süresi "benzer" | 2,69 katı, belirgin yüksek | ✗ |

Tutmayan öngörülerin iki gerekçesi yanlıştı:

- Kanalın ne kadar kalabalık olduğunu küçük görmüştüm. Deneme başına %68 başarısızlığın olamayacağını, atlama başarısızlığının kümelenmeyle açıklanacağını yazmıştım; deneme başına başarısızlık %63 çıktı ve denemeler bağımsıza yakın.
- `onarim_edinimi`nin bedelini doğru (kontrol trafiği ve iletim kaybı arttı), kazancını küçük öngörmüştüm: rota kaybı %40 azaldı ve bedeli dengeledi. `hedefli_canlilik`te ise yedeği canlı tutmanın rota kaybını azaltacağını beklemiştim; azaltmadı.

## 5 · Kuraldan sonra görülenler (karar girdisi değil)

**Kuralın 2. maddesindeki alt dalın sınırı.** "Önbelge + gövde" sonucu yalnız girişimle bozulan çerçeveyi değil, bağın kendi zayıflığıyla bozulan çerçeveyi de içerir; kural ikisini ayırmıyordu. T − Babel farkında girişimsiz beklenen başarısızlık farkı (`b_d`) +8,5 puan, önbelge + gövde farkı +9,1 puan. "Girişimle bozulma" hükmü bu yüzden tek başına okunmaz; aşağıdaki ayrımla birlikte okunur.

**Alıcıdaki iki aşama.** Bir denemenin başarısı iki aşamadan geçer: alıcı çerçeveye kilitlenir (o an başka çerçeveyi dinlemiyor ve kendisi göndermiyor), sonra kilitlenen çerçeveyi çözer.

| kol | kilitlenme | kilitlenince çözülen | `g0` | toplam gönderim |
|---|---|---|---|---|
| kâhin | %70,5 | %64,2 | 0,807 | 329 s |
| Babel | %64,6 | %74,7 | 0,905 | 485 s |
| T | %64,6 | %60,6 | 0,820 | 574 s |
| C | %64,6 | %59,5 | 0,812 | 575 s |
| O | %61,9 | %64,0 | 0,863 | 721 s |
| CO | %62,0 | %62,3 | 0,855 | 714 s |

- Kilitlenme T'de ve Babel'de aynı (%64,6; dört tohumun her birinde fark en çok 0,6 puan). T − Babel farkının tamamı kilitlenen çerçevenin çözülmesinde.
- Kilitten sonraki başarısızlık (önbelge + gövde + onay kaybı) T %27,6 · Babel %18,3; fark 9,2 puan. Bunun 5,5 puanı bağın kendi kalitesinden beklenen, 3,8 puanı beklenenin üstü. Bu okumayla bağ seçiminin payı %59; kuralın ölçüsüyle %44. `π` tohum başına 0,47 · 0,46 · 0,39 · 0,45. İki ölçü aynı şeyi söylüyor: fark, seçilen bağın kendi kalitesi ile kilitlenen çerçevenin girişimle bozulması arasında yaklaşık yarı yarıya bölünüyor.
- Beklenenin üstündeki 3,8 puanın sebebi bu kayıtla ayrılamıyor: DESPARETE'nin toplam gönderim süresi Babel'inkinden %18 fazla; daha zayıf bağ da aynı girişime daha az dayanır. İkisi aynı sonucu verir.
- Sayaçtaki "onay kaybı" (`mac_onaysiz_onay`; T %5,2 · Babel %4,4) paket alıcıya bir kez ulaştıktan sonraki bütün onaysız denemeleri sayar. Tek denemede kaybolan onay (alıcıda çözülen − onaylanan) T %2,1 · Babel %2,0 · kâhin %1,7.

**Kanal üç protokolde de kalabalık.**

- Denemelerin yarısından fazlası başarısız: kâhin %56,5 · Babel %53,7 · T %63,0. En büyük tek kalem alıcının başka çerçeveyi dinliyor olması (%27–33).
- Denemelerin %94–96'sı en düşük hızda (1 Mb/s). Hız uyarlaması yukarı çıkmak için on ardışık başarı ister; deneme başarısı %37–46 iken bu nadirdir.
- Kollar arasında toplam gönderim süresi arttıkça kilitlenme düşüyor: kâhin 329 s → %70,5 · T 574 s → %64,6 · O 721 s → %61,9 (kabaca 100 saniyede 2 puan). Babel bu çizginin 2 puan altında (485 s → %64,6). Tohumlar arasında da yön aynı: kilitlenme altı kolda da 1005'te en düşük; 1005 kâhin dışındaki beş kolda en yüklü tohum.
- T'nin toplam gönderim süresinin %32'si kontrol trafiği; Babel'de %14, kâhinde %6.
- Babel paket başına %37 daha çok atlama yapıyor (3,74 ↔ 2,72 karar) ve paket başına daha çok deneme harcıyor (7,9 ↔ 6,8); atlama başına başarısızlığı yine de üçte bir (%2,3 ↔ %6,5).

**Atlama başarısızlığı neden katlanıyor.** Bir atlama yedi denemenin hepsi başarısız olunca düşer. Deneme başarısı Babel'deki 0,463'ten T'deki 0,370'e inince (oran 0,80) atlama başarısızlığı %2,3'ten %6,5'e çıkıyor (2,8 kat).

**Seçenekler.**

- **O** rota kaybını %40 azaltıyor (0,054 → 0,032). Yol isteği yanıt buluyor (4 503 isteğe 10 690 yanıt; T'de 131 isteğe 2 yanıt); ulaşılamaz durumu 68 → 0.
- Kazancın tamamı iletimde geri gidiyor. Paket başına karar 2,72 → 3,19 (+%17); atlama başına başarısızlık aynı düzeyde (%6,5 → %6,2). Paketler daha çok atlama yapıyor ve her atlamada aynı oranda kayboluyor.
- O'nun kontrol bedeli: kontrol kanal süresi +%45 (185 → 268 s), duyuru +%56, ardıl değişimi +%74; kilitlenme 2,7 puan düşüyor. Seçilen bağlar daha iyi (`g0` 0,820 → 0,863), ağın öteki iletimlerinden sağ çıkan pay daha düşük (`k` 0,452 → 0,434).
- O, en yüklü tohum 1005'te zararlı (−0,059; ΔR +0,002 · Δİ +0,057), öteki üçünde yararlı yönde (+0,010 · +0,037 · +0,013).
- **C:** boşta yoklama 4 227 · silinen komşu −%8 · onarıma giriş −%12 · ardıl değişimi +%13. Rota kaybı değişmiyor, iletim kaybı +0,009.
- **CO:** O'nun yanına C'yi eklemek sonucu değiştirmiyor.

## 6 · Bundan çıkan

- İki seçenek de bu hâliyle teslimi değiştirmiyor. `onarim_edinimi` rota kaybının azaltılabildiğini gösterdi; bedeli (atlama sayısı ve kontrol trafiği) düşürülmeden kazanç teslime yansımıyor. `hedefli_canlilik` rota kaybını azaltmıyor: rota kaybı yedek yokluğundan gelmiyor.
- Karıştırıcısız açığın büyük kalemi olan iletim kaybında Babel'den fark, alıcıya ulaşan çerçevenin bozulmasında. Alıcının meşgul olması iki protokolde aynı. Farkın yaklaşık yarısı doğrudan seçilen bağın kalitesi.
- Kanal bu senaryoda bütün protokoller için kalabalık ve ağ en düşük hızda çalışıyor. Bu ortamda deneme başarısındaki küçük fark atlama düzeyinde katlanıyor.
- Tasarım konularına girdi:
  - **bağ kalitesi:** Babel daha kısa bağla daha çok atlama yapıyor ve bu hücrede kazanıyor. DESPARETE kâhin gibi uzun bağ seçiyor; kâhinin kanalı ise çok daha boş (toplam gönderim 329 ↔ 574 s). Bağ maliyetinde bağın payı (marjı) ele alınacak.
  - **kontrol yükü:** DESPARETE'nin kontrol kanal süresi Babel'in 2,7 katı ve kendi gönderim süresinin üçte biri. Toplam gönderim süresi arttıkça kilitlenme düşüyor.
  - **onarım:** yol istemek rota kaybını azaltıyor; bedeli atlama sayısı ve kontrol trafiği.
  - **komşunun varlığı:** yedeği yoklayarak canlı tutmak rota kaybını azaltmıyor.
- Sıradaki ölçüm plandaki gibi: rakiplerin ve kâhinin 1003–1010'da üç geliştirme hücresindeki çizgisi.
