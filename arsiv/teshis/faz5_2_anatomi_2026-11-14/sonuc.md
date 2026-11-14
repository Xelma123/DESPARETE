# Faz 5-2 · DESPARETE ↔ Babel kayıp anatomisi — sonuç

> 14 Kasım 2026 · ölçüt `beklenti.md` (commit `6d6d67e`, koşudan önce) · koşu: ikiz 16:31–18:43 (2 sa 12 dk) · birincil 19:31–22:03 (2 sa 31 dk), `zaman.txt` · `kopya/` = `6d6d67e` (150 dosya birebir, `kopya_ozet.txt`) · ham çıktı `anatomi_ikiz.txt` · `anatomi_birincil.txt`, kayıt `kayit_ikiz.json` · `kayit_birincil.json` · karar kuralının uygulanması `sonuc_hesap.py` → `sonuc_hesap.txt` · ek sayılar `ek_hesap.py` → `ek_hesap.txt` (koşudan sonra yazıldı, karar girdisi değil).

## 0 · Geçerlilik ✓

Korunum 24/24 geçerli · doğum evresi çelişkisi 0 · atfsız düşüş yok · birincilde aletin açık evre PDR'si satırın `pdr_acik`ıyla 12/12 birebir · 1003 ve 1004'te birincil `PDR_açık` K-244 kuyruğunun G2ç değerleriyle 6/6 birebir (altı basamak).

## 1 · İkiz hücre (karıştırıcı yok) — bütün pencere, 4 tohum havuzlanmış

| kol | PDR | R · rota yok | İ · iletim | K | T | 1003 | 1004 | 1005 | 1006 |
|---|---|---|---|---|---|---|---|---|---|
| kâhin | 0,913 | 0,000 | 0,088 | 0 | 0 | 0,896 | 0,961 | 0,898 | 0,895 |
| Babel | 0,920 | 0,000 | 0,080 | 0 | 0 | 0,944 | 0,954 | 0,863 | 0,918 |
| DESPARETE | 0,768 | 0,054 | 0,179 | 0 | 0 | 0,752 | 0,797 | 0,718 | 0,804 |

- **`G` = PDR(Babel) − PDR(DESPARETE) = +0,152.** Tohum başına +0,192 · +0,157 · +0,145 · +0,114 (dördü pozitif).
- **Paylar: İ %65 · R %35** (`E_İ` +0,098 · `E_R` +0,054 · K 0 · T 0). Tohum başına İ payı %69 · %64 · %46 · %83; 1005'te R öne geçiyor (R +0,079 · İ +0,066).
- DESPARETE'nin R'si: `rota_gecersiz` 0,051 · `hedef_yok` 0,003.

## 2 · Birincil hücre (karıştırıcı 10 W, sürekli)

Açık evrede doğan paketler:

| kol | PDR | R | İ | K | T | 1003 | 1004 | 1005 | 1006 |
|---|---|---|---|---|---|---|---|---|---|
| kâhin | 0,769 | 0,008 | 0,211 | 0,013 | 0 | 0,748 | 0,844 | 0,657 | 0,825 |
| Babel | 0,646 | 0,000 | 0,351 | 0,003 | 0 | 0,547 | 0,787 | 0,485 | 0,764 |
| DESPARETE | 0,557 | 0,226 | 0,217 | 0 | 0 | 0,518 | 0,603 | 0,446 | 0,662 |

- Açık evrede `G` = **+0,089** (tohum başına +0,029 · +0,185 · +0,039 · +0,101). `E_R` +0,225 · `E_İ` −0,134: açığın tamamı R grubunda; iletimde DESPARETE Babel'den az kaybediyor.

Karıştırmaya özgü kayıp, `Δ = açık − önce`:

| kol | önce | açık | Δ | R | İ | K | sessiz evre |
|---|---|---|---|---|---|---|---|
| kâhin | 0,913 | 0,769 | −0,145 | +0,008 | +0,124 | +0,013 | 0,912 |
| Babel | 0,916 | 0,646 | −0,270 | 0,000 | +0,267 | +0,003 | 0,903 |
| DESPARETE | 0,755 | 0,557 | −0,198 | +0,166 | +0,031 | 0 | 0,726 |

- Tohum başına Δ: DESPARETE −0,209 · −0,201 · −0,252 · −0,129 · Babel −0,391 · −0,168 · −0,362 · −0,159.
- Birincilin "önce" evresi ikizin tablosunu yineliyor: `G` +0,161 · İ %63 · R %37.

## 3 · Karar kuralı

0. Geçerlilik tuttu; tablolar kullanılır.
1. **İkizde ana kalem İ (%65 ≥ %50) → önce bağ kalitesi.** Alt ayrım: karar bağlarında orta + kötü payı DESPARETE %1,1 ↔ Babel %0,1, fark 1,0 puan < 5 → **"iyi bağda başarısızlık"** (çarpışma, trafik yığılması, kontrol yükü). "Metrik kötü bağ seçiyor" dalı desteklenmedi. K ve T 0: döngü ve erişim kaybı yok.
2. **Birincilde karıştırmaya özgü kayıp ayırt edildi:** `Δ(DESPARETE) − Δ(Babel)` = +0,072 ≥ 0,03. Babel karıştırıcı açılınca daha çok kaybediyor; kaybı İ grubunda (+0,267). DESPARETE'nin kaybı R grubunda (+0,166; İ +0,031). 4 tohumun 3'ünde yön aynı; 1004'te ters (−0,201 ↔ −0,168).
3. **İkizde R payı %35 ≥ %30 → (b) ölçümü koşulur:** v0.4.1'in `hedefli_canlilik` ve `onarim_edinimi` seçenekleri, ikizde, ayrı beklentiyle.
4. Kâhine oran: ikizde DESPARETE 0,841 · Babel 1,008; birincilin açık evresinde 0,725 · 0,840. Babel ikizde en güvenilir yol kâhinini 0,007 aşıyor (1003 ve 1006'da). Bu koşuda üç kâhinin zarfı ölçülmedi; aşım K-248'de kayıtlı desenle aynı yönde, karar değiştirmez.

## 4 · Öngörüler

| öngörü | ölçülen | |
|---|---|---|
| İkizde `G` ≈ 0,17 (±0,04) | 0,152 | ✓ |
| İkizde R baskın (%55–75), İ ikinci (%25–45) | İ %65 · R %35 | ✗ (ters) |
| K ve T ≈ 0 | 0 · 0 | ✓ |
| Onarım bölümü tohum başına > 1 000 | 2 633–3 465 | ✓ |
| Girişlerin çoğu açlık (≥ %60) | %74 | ✓ |
| Çoğu aynı turda, p50 < 0,5 s | aynı tur %96 · p50 0,13–0,16 s | ✓ |
| Kaybın çoğu `+U` ile biten uzun bölümlerden | `rota_gecersiz`in %36'sı ulaşılamaz durumda, %64'ü kota doluyken; alet düşüşü bölüme bağlamıyor | sınanamadı |
| `rota_gecersiz` anında kota ≥ %50 | %64 | ✓ |
| Karar bağlarında orta + kötü farkı < 5 puan | 1,0 puan | ✓ |
| Babel'in karar mesafesi DESPARETE'ninkinden uzun değil | p50 5,9–7,0 ↔ 7,0–8,2 km | ✓ |
| Birincilde `Δ(Babel) − Δ(DESPARETE)` ≤ −0,03 | −0,072 | ✓ |
| Babel'in özgü kaybı İ'de, DESPARETE'ninki R'de | İ +0,267 · R +0,166 | ✓ |
| Birincilde açık evrede `G` 0,05–0,15 | 0,089 | ✓ |

Tutmayan öngörünün gerekçesi yanlıştı: DESPARETE ikizde ardılını yitirip onarımda paket düşürüyor (R 0,054), ama Babel'e göre asıl fazlası seçtiği bağda geçmeyen paketlerde (İ 0,179 ↔ 0,080).

## 5 · Kuraldan sonra görülenler (karar girdisi değil)

**İkiz — iletim başarısızlığı** (bütün koşu; karar = sonraki atlaması olan veri kararı):

| kol | karar / paket | başarısız / karar | kâhinin "iyi" dediği bağda | tek deneme bandı iyi · orta · kötü | karar mesafesi p50 |
|---|---|---|---|---|---|
| kâhin | 2,64 | %3,29 | %3,11 | %55 · %40 · %5 | 7,2–8,8 km |
| Babel | 3,74 | %2,32 | %2,25 | %77 · %22 · %1 | 5,9–7,0 km |
| DESPARETE | 2,72 | %6,49 | %5,74 | %63 · %32 · %5 | 7,0–8,2 km |

- DESPARETE'nin bağ seçimi kâhininkine yakın: aynı atlama sayısı, benzer mesafe, tek denemede kâhinden iyi bağlar. Atlama başına başarısızlığı ise kâhinin iki katı. Başarısızlıklarının %87'si kâhinin "iyi" dediği bağlarda.
- Kâhin bandı ağın kendi iletimlerinden gelen girişimi içermez (K-248). Fark iki sebepten gelebilir: çarpışma ve kanal yükü, ya da bağ ölçümünün bayat kalması. Bu kayıt ikisini ayıramıyor.
- Babel daha kısa bağlardan daha çok atlamayla gidiyor; atlama başına başarısızlığı kâhininkinden de düşük.

**İkiz — komşuluk ve kontrol trafiği** (ağ toplamı, tohum ortalaması, 350 s):

- DESPARETE komşu kaydı: aday açılan 14 326 · etkin olan 16 823 · şüpheli 4 851 · bayat 12 119 · **silinen 15 171**. Babel'de silinen komşu 315.
- DESPARETE yoklama gönderimi ~35 000 (nitelik 17 155 · ölçüm 13 756 · hata 3 208 · doğrulama 912) ve duyuru gönderimi 35 823 (tetiklenen duyuru sayacı 24 122 · geri çekme 2 433). Aynı sürede veri iletimi 34 016.
- Alınan duyuruların 138 239'u gönderen komşu etkin olmadığı için işlenmedi; kabul edilen 79 132.
- Ardıl değişimi 10 804: düğüm başına ortalama 1,3 saniyede bir. Onarıma giriş 3 753 · ulaşılamaz 68 · tur artışı 13.
- Açlık yayını (`FIELD_SOLICIT`) 131, yanıtlanan 2.
- Babel: Hello 4 006 · seçim değişimi 25 015 (40 hedefin tamamı) · alınan güncelleme 704 982 · sıra isteği 8 260. Çerçeve sayısı ve kanalda kaplanan süre iki protokol için de bu kayıtta yok; kontrol yükü karşılaştırması buradan yapılamaz.

**Birincil:**

- Olay anına göre atlama başına başarısızlık (önce → açık → sessiz): DESPARETE %6,6 → %9,1 → %6,1 · Babel %2,6 → %10,0 → %2,2 · kâhin %3,2 → %6,8 → %3,3. Babel'in başarısız iletimlerinin %20'si kâhinin "kötü" dediği bağda (ikizde %0): rotasını koruyup kesik bağa göndermeyi sürdürüyor.
- DESPARETE'nin açık evredeki `rota_gecersiz` kaybı karıştırıcının alanında değil: düşüşün olduğu yere göre uzak 0,177 · girişim 0,034 · ed 0,007 (önce 0,042 · 0,014 · 0,000). Faz 5.0'daki desenle aynı: karıştırma bir ardılı koparınca onarım geçide giden yol boyunca yayılıyor.
- Babel'in açık evredeki iletim kaybı karıştırıcının alanında yoğunlaşıyor: girişim 0,035 → 0,182 · ed 0,002 → 0,049 · uzak 0,048 → 0,119.
- Açık evrede DESPARETE'nin onarım bölümleri: giriş açlık %67 · adaysız %33; `rota_gecersiz` anında alan ulaşılamaz %59 (ikizde %36). Bölümlerin sıklığı açık evrede yaklaşık %30 artıyor (dört tohum toplamında saniyede 45 → 59; sessiz evrede 43); uzun bölümlerin payı da artıyor (`yeni_tur+U` %1 → %3).
- Sessiz evrede DESPARETE "önce" düzeyine dönmüyor (0,755 → 0,726); Babel 0,916 → 0,903.

## 6 · Bundan çıkan

- Açığın büyük kalemi karıştırmadan bağımsız: karıştırıcı yokken 0,15–0,16. Bunun üçte ikisi seçilen bağda geçmeyen paket, üçte biri rota yokluğu.
- Karıştırma altında DESPARETE Babel'den 0,07 daha az kaybediyor; taban açığı bunu örtüyor ve açık evrede 0,09 geride kalıyor. Açık evredeki açığın tamamı rota yokluğu.
- İki protokolün hatası zıt yönde: Babel rotayı bırakmıyor ve kesik bağda kaybediyor; DESPARETE rotayı bırakıyor ve onarımda kaybediyor. Kâhin ikisinin arasında değil, ikisinden de iyi (R 0,008 · İ 0,211).
- Sıradaki ölçümler: kural gereği (b); ayrıca "iyi bağda başarısızlık"ın sebebini ayıran bir teşhis (başarısız iletim denemesinde alıcıda başka iletim var mıydı; kontrol trafiğinin kanalda kapladığı süre). İkisi ayrı beklentiyle.
