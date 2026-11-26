# KK-04 · Rota seçimi ve döngü bekçisi

> **Önceki tasarım (26 Kasım notu):** bu kâğıt 5-3'ün ilk tasarımının kuralıdır (kararları `17`); bugünkü kodun (`protokoller/desparete5*.py`) ve 18–24 Kasım ölçümlerinin belgesi olarak kalır, yeni tasarım donunca arşive gider. Yeni tasarım `18`de, kuralları `bilesen/`de (K-253).

> Kararlar: T-11 · T-12 · T-13 (kalktı) · T-14 · T-15 · T-17 (`17`). Değerler ve genel kurallar `KK-00`. Kod `protokoller/desparete5_egim.py` (`egim` kapalıyken 18 Kasım'ın `desparete5_rota.py`'si). Güncel: 20 Kasım 2026 (kural 13 geri gönderme yasağı ve kural 14 sınırlı yükselme eklendi, kural 2 ve 3'e sınırlı yükselmenin koşulu; sebep: yeni çekirdeğin ölçümünde birincil hücrede koşu başına binlerce döngü dönüşü, son çareyle birlikte artıyor, `arsiv/teshis/faz5_3_yeni_cekirdek_2026-11-19/sonuc.md`). Önceki: 19 Kasım (`v2/arsiv/kural/KK-04-ROTA-2026-11-19.md`: maliyet eğimi, son çare, tavan, döngü bekçisi; kural 1–12 aynı numaralarla) · 18 Kasım (`v2/arsiv/kural/KK-04-ROTA-2026-11-18.md`: FD, tur, açlık, tur isteği, yok sayma).
>
> **Kod:** kural 1–12 19 Kasım'da bu kâğıda göre yazıldı. 18 Kasım'ın davranışı `egim` · `vazgecme_tetigi` · `duzgun_gecis` kapalı, `veri_kotu_tetigi` açık ve `DEGERLER_ESKI`yle birebir yeniden üretilir (küçük test dünyasında sekiz koşuda denetlendi: `arsiv/teshis/faz5_3_kod_2026-11-19/esdegerlik.txt`). Kural 13–14 20 Kasım'da kodlandı (`desparete5_egim.py`: `_L`, `_adaylar`, `_c_ref`, `geri_alternatif`; karar `desparete5.py` `sonraki_atlama`). `geri_yasagi` ve `sinirli_yukselme` kapalıyken 19 Kasım'ın kodu birebir yeniden üretilir (`CEKIRDEK_19K`; küçük test dünyasında 12 koşuda denetlendi: `arsiv/teshis/faz5_3_kod_2026-11-20/esdegerlik.txt`).

## Amaç ve sınıf

Geçide giden ardılı seçmek; düğümü, olağan ve sonlu maliyetli bir komşusu olduğu sürece yolsuz bırakmamak; oluşan döngüyü veri yolunda yakalayıp onarmak. **Genel.** Bayraklar: `egim` (kapalıyken 18 Kasım'ın kuralları: FD, tur, açlık, tur isteği, yok sayma; arşivdeki kâğıt) · `istege_bagli_esik` ve `duzgun_gecis` (kural 5) · `geri_yasagi` (kural 13) · `sinirli_yukselme` (kural 14).

Döngüsüzlük garanti değildir (T-12; CTP ve RPL'nin yolu). İki kural döngünün kurulmasını zorlaştırır: paket getiren komşuya geri gönderilmez (kural 13), maliyet sınırsız tırmanamaz (kural 14). Kurulan döngü veri yolunda yakalanır ve onarılır (kural 8–9).

## Gördüğü ve tuttuğu

- Her komşunun selamla son ilan ettiği maliyet `C_j` (sonlu ya da ∞). Tur yoktur (KK-02).
- KK-01'den her bağın durumu, `ETX_selam`'ı ve "veriye uygun değil" işareti.
- `ardil`, kendi maliyetim `C`, son ilan ettiğim maliyet `C_ilan` (nicemlenmiş; hiç sonlu ilan etmediysem ∞).
- Her aday j için düzgünleştirilmiş toplam maliyet `ms_j` ve son güncelleme anı (kural 6).
- Son `YUKSELME_UNUT_S` içinde ilan ettiğim sonlu maliyetler ve anları; en küçüğü `L` (kural 14).
- Döngü bekçisi: son `DONGU_ANIMSA_S` içinde ilettiğim telemetri paketleri: `(kaynak, kaynak_sira)` → (o anki atlama sayısı, gönderdiğim komşu); bana gelen telemetri çerçevelerinin göndereni (`cerceve_duyuldu`), aynı anahtarla; dışlanan komşular ve dışlamanın bitişi (kural 9).
- Bütün maliyetler ETX × 64 tamsayı biriminde (yukarı yuvarlanır; sonlu en çok 0xFFFE, 0xFFFF = ∞). Geçidin kimliği yapılandırmadan gelir; geçidin maliyeti 0'dır ve geçit ardıl seçmez.

## Kurallar

1. **Toplam maliyet:** j üzerinden yolumun maliyeti `m_j = ETX_selam(i, j) + C_j` (yukarı yuvarlanır, 0xFFFE'de doyar).
2. **Aday küme `A`:** durumu OLAĞAN (KK-01), `C_j` sonlu, `m_j ≤ MALIYET_TAVANI`, döngü dışlaması (kural 9) olmayan ve (`sinirli_yukselme` açıkken, `L` varsa) `m_j ≤ L + YUKSELME_PAYI` olan komşular (kural 14). KÖTÜ ve KARIŞTIRILIYOR komşu aday da yedek de değildir (T-15).
3. **Yokuş aşağı `D ⊆ A`:** `C_j < C_ilan`. Komşuların benim için bildiği değer `C_ilan`'dır; j'nin yolu benden geçseydi `C_j ≥ ETX(j, i) + C_ilan > C_ilan` olurdu. Bu yüzden yokuş aşağı komşu, son bildiği hâliyle paketi bana geri göndermez (LFA'nın aşağı akış koşulu [61]). Ardılım az önce kaybolduysa `C_ilan` kaybolmadan önceki değerdir. `C_ilan` ∞ ise: `sinirli_yukselme` açıkken ve `L` varsa ölçüt `C_j < L`'dir (kural 14); öteki durumlarda `D = A`.
4. **Seçim sırası** (gruplar, iyiden kötüye; grup içinde en küçük `m_j`, eşitlikte mevcut ardıl, düşük ETX, küçük adres):
   - G1: `D` içinde ve "veriye uygun değil" olmayan;
   - G2: `D` içinde ve "veriye uygun değil";
   - G3: `A \ D` (yokuş yukarı) ve "veriye uygun değil" olmayan;
   - G4: `A \ D` ve "veriye uygun değil".

   Buna göre:
   - **Ardıl kayboldu** (`A`'da değil: KÖTÜ, KARIŞTIRILIYOR, silindi, ∞ ilan etti, tavanı aştı ya da dışlandı) ya da ardıl yok: boş olmayan ilk grubun en iyisi seçilir (zorunlu geçiş; T-9). G3 ya da G4'ten seçmek **son çaredir**: maliyetim yükselir ve bu bir değişim olayıdır (kural 7). `A` boşsa ardıl yoktur (kural 11).
   - **Ardıl "veriye uygun değil" oldu:** G1'de başka bir aday varsa onun en iyisine geçilir; yoksa ardıl kalır (`17` T-2: yedek yokken bağ kullanılmaya devam eder, açlık doğmaz).
   - **Ardıl `A`'da ve veriye uygun:** isteğe bağlı geçiş (kural 5).
5. **İsteğe bağlı geçiş** (T-11): adaylar G1'in öteki üyeleri. j'ye geçilir ⇔
   - `duzgun_gecis` açıkken: `m_j < m_ardil` **ve** `ms_j < ms_ardil` (anlık ve düzgünleştirilmiş maliyet ikisi birden daha iyi; Babel [4] Ek A.3);
   - `duzgun_gecis` kapalı, `istege_bagli_esik` açıkken: `m_j < (1 − GECIS_ORANI) · m_ardil` (16 Kasım'ın oransal eşiği);
   - ikisi kapalıyken: `m_j < m_ardil`.

   Birden çok aday geçerse en küçük `m_j`'li seçilir. `m_j < m_ardil = C` olduğu için bu adaylar zaten yokuş aşağıdır.
6. **Düzgünleştirilmiş maliyet:** her seçimde her aday için `ms_j ← ms_j + (m_j − ms_j) · (1 − e^(−Δt / DUZ_S))`, `Δt` son güncellemeden beri geçen süre. `A`'ya yeni giren adayda `ms_j = m_j`; `A`'dan çıkan adayın kaydı silinir. Zorunlu geçişte `ms` kullanılmaz: yol kaybolunca beklenmez (Babel Ek A.3: seçili rota yoksa yalnız anlık maliyete bakılır).
7. **Kendi maliyetim ve ilan:** `C = m_ardil`, ardıl yoksa ∞; selamla ilan edilir ve `C_ilan` olur (KK-02). Değişim olayları (hemen selam, KK-02 kural 3): `C`, `C_ilan`'dan `ILAN_ESIGI` kadar farklı ya da ∞ ↔ sonlu · son çare seçimi (kural 4) · döngü işareti (kural 8–9).
8. **Döngü bekçisi · bayat bilgi** (`cerceve_duyuldu`; niyet döndürmez, olay bir sonraki niyetli kancada verilir, `KK-00` genel kural 1): bana iletilmek üzere telemetri çerçevesi gelir (tür veri, hedefi ben, paketin hedefi geçit, kaynağı ben değilim), gönderen s. s'nin son ilanı `C_s ≤ C` ise ya da `C` ∞ ise s'nin bildiği eğim bayattır ya da döngü vardır: **değişim olayı** (selam). Paket olağan iletilir. Sebep: CTP her veri paketine gönderenin maliyetini yazar [68]; bizde başlığa değer yazılamadığı için (`13` §02.5) aynı bilgi s'nin selamından okunur.
9. **Döngü bekçisi · kesin döngü** (`sonraki_atlama`): kararı verilen telemetri paketi `(kaynak, kaynak_sira)` son `DONGU_ANIMSA_S` içinde bana **daha küçük bir atlama sayısıyla** gelmiş ve iletilmişse paket bir döngüden dönmüştür (atlama sayısı = başlangıç ömrü − kalan ömür, her atlamada bir artar):
   - iki komşu `DONGU_DISLA_S` süre `A`'dan dışlanır: o paketi önceki sefer gönderdiğim komşu (döngüye giden yol) ve paketi bu sefer bana getiren komşu (yolu benden geçiyor; `cerceve_duyuldu`'nun kaydı). İki düğümlü döngüde ikisi aynıdır;
   - ardıl yeniden seçilir (kural 4) ve paket yeni ardıla gider; ardıl yoksa paket bekletilir (KK-05);
   - **değişim olayı** (selam).

   Aynı atlama sayısıyla yeniden gelen paket MAC'in tekrarıdır, döngü değildir. Kendi ürettiğim paket (kaynak ben) ilk kararda atlama sayısı 0 ile kaydedilir. Kayıt, paket her gönderildiğinde o anki atlama sayısı ve komşuyla güncellenir; `DONGU_ANIMSA_S`'den yaşlı kayıt silinir. Paketin ömrü (TTL; referans dünyada başlangıç 64, K-215) son güvencedir.
10. **Maliyet tavanı:** `m_j > MALIYET_TAVANI` olan komşu aday değildir (kural 2). Kopan bir bölgede düğümler birbirini son çare seçince maliyetler her selam alışverişinde yükselir; tavanı aşınca adaylar biter, ∞ ilan edilir ve tırmanma durur. Sınırlı yükselme (kural 14) tırmanmayı tavandan çok önce keser; kapalıyken döngü bekçisi (kural 9) keser ya da tavan durdurur (19 Kasım'ın ölçümünde birincil hücrede maliyetler tavana dayandı).
11. **Yol yok:** `A` boşsa ardıl yoktur, `C = ∞` ilan edilir; paketler bekletilir (KK-05). Tur isteği yoktur (T-13).
12. **Kendim karıştırılırken** (KK-03 kural 4): seçim aynı kurallarla sürer. Bağ ölçüleri dondurulduğu için (KK-01 kural 13) adaylar ve maliyetleri değişmez; MAC sonuçları bağ kanıtı sayılmaz (KK-03 kural 8), ardıl korunur.
13. **Geri gönderme yasağı** (`geri_yasagi`; `sonraki_atlama`): telemetri paketinin sonraki atlaması, paketi bana getiren komşu g olamaz (`cerceve_duyuldu`'nun kaydı, kural 9). Ardılım g ise bu paket için:
   - `D`'deki öteki adaylardan kural 4'ün sırasıyla en iyisi seçilir (önce G1, sonra G2). Ardıl değişmez, yalnız bu paketin yönü değişir.
   - `D`'de başka aday yoksa paket bekletilir (KK-05); yokuş yukarı bir komşuya gönderilmez.

   Ardılımın bana telemetri göndermesi, ikimizin birbirini yokuş aşağı sandığını gösterir; kural 8 bunu zaten değişim olayı sayar ve selam bilgiyi düzeltir. CTP de böyle bir tutarsızlıkta paketi düşürmez, kısa bir süre bekletir ve önce selam gönderir [68]. Bu kural iki düğüm arasında gidip gelmeyi paket daha dönmeden keser; üç ve daha çok düğümlü döngüyü kural 9 yakalar. Kendi ürettiğim pakette getiren yoktur. Komutlar (geçitten aşağı) bu kuralın dışındadır; yolları geri izdir (KK-05).
14. **Sınırlı yükselme** (`sinirli_yukselme`): `L`, son `YUKSELME_UNUT_S` içinde ilan ettiğim en küçük sonlu maliyettir; bu sürede hiç sonlu maliyet ilan etmediysem `L` yoktur.
   - `L` varken maliyetimi `L + YUKSELME_PAYI`'nın üstüne çıkaracak komşu aday değildir (kural 2). Bu mevcut ardıla da uygulanır: ardılım üzerinden maliyetim sınırı aşarsa ardıl kaybolmuş sayılır (zorunlu geçiş, kural 4). Sınır içinde aday yoksa ardıl yoktur, ∞ ilan edilir, paketler bekletilir (kural 11, KK-05).
   - ∞ ilan ettikten sonra yokuş aşağı ölçütü `L`'dir (kural 3): kopmadan önceki maliyetimden alçak komşu yokuş aşağıdır; ötekiler yokuş yukarıdır ve yine sınıra tabidir.
   - `YUKSELME_UNUT_S` geçince `L` unutulur; düğüm sınırsız yeniden bağlanabilir.

   Sebep: son çareyle birbirini seçen düğümlerin maliyetleri her ilan alışverişinde birbirini yukarı iter (kural 10). Bu sınır olmasa tırmanma tavana kadar sürer. RPL aynı tırmanmayı aynı yolla durdurur: düğüm, bir sürüm içinde ilan ettiği en düşük yüksekliği `DAGMaxRankIncrease`'ten fazla aşamaz; aşacaksa sonsuz ilan eder (zehirleme) [63 §8.2.2.4–8.2.2.5]. RPL'de `L` ancak geçit yeni bir sürüm başlatınca sıfırlanır; bizde tur yok (T-13), yerine süre kullanılır.

## Örnek

X'in ardılı W'den yolu `C_ilan = 2,5`. W'nin bağı KÖTÜ olur.
- Komşu Y'nin ilanı 1,9 (< 2,5, yokuş aşağı): X anında Y'ye geçer, `C = ETX(X, Y) + 1,9`.
- Yokuş aşağı komşu yoksa ve tek aday Z ise (Z'nin yolu X'ten geçiyor, ilanı `ETX(Z, X) + 2,5 = 1,2 + 2,5 = 3,7`; iki yönde ETX 1,2): X son çare olarak Z'yi seçer, `C = 1,2 + 3,7 = 4,9` olur ve hemen ilan edilir. X'in Z'ye gönderdiği paket Z'den X'e geri döner. X onu daha büyük atlama sayısıyla görünce döngüyü anlar: Z'yi (hem önceki sefer gönderdiği hem paketi getiren komşu) 2 s dışlar, başka adayı yoksa ∞ ilan eder ve paketi bekletir. Z, ardılı X'ten ∞ duyunca o da adaysız kalır ya da kendi yedeğine geçer. Döngü tek bir paket turunda kesilir; döngü bekçisi olmasaydı maliyetler tavanı (32) aşana kadar tırmanırdı.

Aynı olay kural 13 ve 14 açıkken (`YUKSELME_PAYI` 4 ETX): X'in `L`'si 2,5.
- Z üzerinden maliyet 4,9 ≤ 2,5 + 4 = 6,5 olduğu için X yine son çare olarak Z'yi seçer ve 4,9 ilan eder.
- Z, X'ten gelen paketi X'e geri gönderemez: ardılı X, paketi getiren de X (kural 13). Başka yokuş aşağı adayı yoksa paketi bekletir.
- Z'nin yolu X'ten geçtiği için Z'nin maliyeti 1,2 + 4,9 = 6,1 olur ve ilan edilir. Z'nin `L`'si 3,7, sınırı 7,7; aşılmaz.
- X bunu duyunca Z üzerinden maliyeti 1,2 + 6,1 = 7,3 olur ve sınırı (6,5) aşar. Z aday olmaktan çıkar; X ∞ ilan eder, paketleri bekletir. Z de X'in ∞'unu duyunca adaysız kalır.

Tırmanma bir turda durur, paket bir kez bile geri dönmez. W ya da başka bir yol açılınca ikisi yeniden bağlanır; açılmazsa bekletilen paketler 1 s sonra düşer (KK-05).

## Sınanması

- `egim` açık ↔ kapalı (18 Kasım'ın kuralları): ikizde ve birincil hücrede teslim, rota yokluğu kaybı (R), ömür kaybı (T grubu, döngünün göstergesi), gecikmenin p99'u, kontrol yükü.
- `duzgun_gecis` açık ↔ kapalı: ardıl değişim sıklığı, ikizde pencere PDR'si.
- `geri_yasagi` açık ↔ kapalı ve `sinirli_yukselme` açık ↔ kapalı: birincil hücrede döngü kanıtı sayısı, en kötü tohumun `PDR_açık`ı, gecikmenin p99'u, sessiz dönemin teslimi, rota yokluğu kaybı (sınırın yol yok bölümü doğurma bedeli); ikizde zarar yok.
- Tanı: döngü kanıtı (kural 9) ve bayat bilgi olayı (kural 8) sayısı · son çare seçimi · tavan aşımı · yol yok bölümlerinin sayısı ve süresi · ardıl değişimi, sebebine göre (kopma, veriye uygunsuzluk, isteğe bağlı) · yol maliyetinin dağılımı (tavanın yeri için) · kural 13'ün başka adaya yönlendirdiği ve beklettiği paketler · kural 14 yüzünden kaybedilen ardıl.

## Kaynak

Maliyet eğimi, gönderenin maliyetiyle veri yolunda döngü doğrulaması ve paketi düşürmeden onarma CTP [68] (§3.1, §4.3) ve RPL [63] (§3.7); yokuş aşağı koşulu LFA'nın aşağı akış yolu [61] (RFC 5286); anlık ve düzgünleştirilmiş maliyetle geçiş Babel [4] (RFC 8966 Ek A.3); oransal eşik Ramachandran [54]. Geri gönderme yasağı RPL [63] §11.1 ("split horizon": seçilen sonraki atlama paketin öncülü olamaz); sınırlı yükselme ve zehirleme RPL [63] §8.2.2.4–8.2.2.5; payın ardıl değiştirme eşiğinden küçük olmaması MRHOF [64] (RFC 6719 §6.1). Son çare, maliyet tavanı, başlığa yazmayan döngü bekçisi (komşunun selamından ve paketin atlama sayısından), veriye uygunsuz bağın sona düşmesi ve `L`'nin süreyle unutulması bu tasarımın.
