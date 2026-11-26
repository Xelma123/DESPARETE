# KK-01 · Bağın durumu ve ölçüsü

> **Önceki tasarım (26 Kasım notu):** bu kâğıt 5-3'ün ilk tasarımının kuralıdır (kararları `17`); bugünkü kodun (`protokoller/desparete5*.py`) ve 18–24 Kasım ölçümlerinin belgesi olarak kalır, yeni tasarım donunca arşive gider. Yeni tasarım `18`de, kuralları `bilesen/`de (K-253).

> Kararlar: T-2 · T-3 · T-7 · T-9 · İlke 2 (`17`). Değerler ve genel kurallar `KK-00`. Kod `protokoller/desparete5_bag.py`. Güncel: 19 Kasım 2026 (yeniden yazıldı: veri tetiği yerine vazgeçme tetiği; askıda durumu ve veri cezası kalktı; `17` T-2). Önceki: 18 Kasım (`v2/arsiv/kural/KK-01-BAG-2026-11-18.md`; kodlamayla Y-2 · Y-4 · Y-6 · Y-7 · Y-8 · Y-12, G-3 · G-4). Kural numaraları korunur; kalkan kurallar yerinde "kalktı" diye durur.
>
> **Kod:** 19 Kasım'da bu kâğıda göre yazıldı. 18 Kasım'ın davranışı `egim` · `vazgecme_tetigi` · `duzgun_gecis` kapalı, `veri_kotu_tetigi` açık ve `DEGERLER_ESKI`yle birebir yeniden üretilir (küçük test dünyasında sekiz koşuda denetlendi: `arsiv/teshis/faz5_3_kod_2026-11-19/esdegerlik.txt`).

## Amaç ve sınıf

Her komşu bağının ne kadar iyi olduğunu (ETX), şu an kullanılıp kullanılamayacağını ve veriyi taşıyıp taşımadığını bilmek. Ölçü ve iki eşik **genel** (çekirdek); vazgeçme tetiği **genel** (`vazgecme_tetigi`); "karıştırılıyor" durumu, dondurmalar ve hatırlanan kalite **karıştırmaya karşı** (`karistirma_durumu`, `hatirlanan_kalite`).

## Gördüğü

- Komşudan aldığı selamlar: sıra numarası, aralık (bir sonraki selama kadarki üst sınır), benim için bildirdiği oran (KK-02). Komşu beni listesinde bildirmiyorsa oran **bilinmiyor**dur: `d_f` değişmez; `T_SILME` boyunca bildirmezse ya da hiç bildirmemişse tanımsızdır (Y-12).
- Kendi veri gönderimlerinin sonucu (`iletim_sonucu`, K-151): yalnız **gitti mi, vazgeçildi mi**. Vazgeçme, MAC'in bütün denemelerinin (referans dünyada 7: ilk gönderim ve 6 yeniden deneme) onaysız bitmesidir; paket o atlamada kaybolmuştur. Yeniden deneme sayısı kullanılmaz.
- Komşudan çözülen her çerçeve (`cerceve_duyuldu`, K-172): yalnız "hâlâ orada" bilgisi.
- KK-03'ten bağ kanıtı ("karıştırılıyor", sebebiyle) ve "bitti" olayları; kendi durumum ("karıştırılıyorum").

## Tuttuğu (komşu başına)

- `gecmis`: son `N` selamın geldi (1) / gelmedi (0) dizisi; `beklenen` sıra numarası; `son_selam_t`; komşunun son ilan ettiği aralık `a`.
- `d_f`: komşunun benim için bildirdiği oran.
- `vaz`: bu komşuya giden son veri çerçevelerinin (an, vazgeçildi mi) kaydı; en çok `VAZ_PENCERE` çerçeve, en çok `VAZ_PENCERE_S` geriye.
- "Veriye uygun değil" işareti: beklemenin bitişi, son beklemenin süresi, son tetiklenme anı (kural 7).
- `durum`: OLAĞAN · KÖTÜ · KARIŞTIRILIYOR; KARIŞTIRILIYOR'da `sebepler` kümesi, `hatira` (`gecmis`, `d_f`) ve giriş anı.
- `son_duyulma_t`: komşudan çözülen son çerçevenin anı; dondurmadan çıkışı işaretleyen bayrak.

## Durumlar

| durum | kullanılır mı | ölçülür mü |
|---|---|---|
| OLAĞAN | evet (aday, KK-04); "veriye uygun değil" işaretliyse ardıl seçiminde sona düşer (KK-04 kural 4) | evet |
| KÖTÜ | hayır | evet (selamla) |
| KARIŞTIRILIYOR | hayır | hayır (donar); kalite hatırlanır |

"Veriye uygun değil" bir durum değil, OLAĞAN bağın üstündeki bir işarettir: bağ ölçülmeye ve kullanılabilir sayılmaya devam eder; yalnız ardıl seçiminde sona düşer. Bağın maliyeti değişmez (T-2: veri sonucu maliyete girmez).

## Kurallar

**Ölçü**

1. **Yeni komşu:** ilk selamıyla kayda girer ve KÖTÜ'de başlar. Selamı olmayan çerçeveler yalnız var olan kaydın `son_duyulma_t`sini tazeler.
2. **Selam gelince** (sıra karşılaştırması 16 bit, modüler):
   - `0 ≤ sıra − beklenen ≤ N`: aradaki boşluk kadar `gecmis`e 0, gelen selam için 1 eklenir (Babel'in "ileri sarma"sı, RFC 8966 Ek A);
   - boşluk `N`'den büyük: komşu yeniden başlamış sayılır, `gecmis` sıfırlanır, 1 eklenir;
   - `sıra < beklenen` (geç gelen): zaman aşımıyla fazla sayılan kayıtların hepsi (`beklenen − sıra` kadar, en yeniden başlayarak) geri alınır, sonra 1 eklenir ("geri alma"; RFC 8966 Ek A). Aralık kısaldıktan sonra zaman aşımı birden çok fazla 0 sayabilir; yalnız sonuncuyu geri almak kayıpları şişirirdi (18 Kasım, G-4);
   - **dondurmadan çıkıştan sonraki ilk selamda** (kural 9, 13): boşluk için 0 eklenmez, sıfırlama yapılmaz, yalnız 1 eklenir;
   - her durumda `beklenen ← sıra + 1`, `son_selam_t ← şimdi`, `a ← selamdaki aralık`.
3. **Zaman aşımı:** şimdi > `son_selam_t` + `ZAMAN_ASIMI` (1,5 × `a`) ise `gecmis`e 0 eklenir, `beklenen` bir ilerler; sonra her `a`da bir 0 daha. `a` komşunun bir sonraki selamına kadarki üst sınır olduğu için olağan aralık değişimi sahte kayıp üretmez (KK-02).
4. **Teslim oranı:** `d_r = gecmis'teki 1'ler / örnek sayısı` (en çok `N`); `gecmis` boşsa tanımsız.
5. **ETX:** `ETX_selam = 1 / (d_f · d_r)`; biri 0 ya da tanımsızsa ∞ (tek yönlü bağ kullanılmaz). Bağın maliyeti budur (KK-04).
6. **Vazgeçme kaydı** (`vazgecme_tetigi`): bağ OLAĞAN iken bu komşuya giden her veri çerçevesinin (telemetri ya da komut) sonucu `vaz`a yazılır: **gitti** (onay geldi; kaçıncı denemede geldiği önemsiz) ya da **vazgeçildi**. Kontrol çerçeveleri yazılmaz. Kendim karıştırılırken yazılmaz (kural 13). Pencerenin dışına düşen kayıt (`VAZ_PENCERE`'den eski ya da `VAZ_PENCERE_S`'den yaşlı) atılır. Bayrak kapalıyken veri sonucu yalnız KK-03 kural 7'ye girer.

**Geçişler**

7. **Vazgeçme tetiği:** OLAĞAN bağın `vaz`ında en az `VAZ_ESIK` vazgeçme varsa (önce KK-03'ün kanıtı denenir, kural 15) bağ **"veriye uygun değil"** işaretini alır:
   - Bekleme süresi: önceki tetiklenmeden beri `VAZ_YINELEME_S` geçmediyse önceki sürenin iki katı (en çok `VAZ_BEKLE_EN_COK_S`), geçtiyse `VAZ_BEKLE_S`.
   - `vaz` boşaltılır: yeniden tetiklenmek yeni vazgeçmeler ister.
   - Bağın durumu, `gecmis`i, `d_f`si ve maliyeti değişmez; selamla ölçülmeye devam eder (İlke 2: kötü bağdan tamamen vazgeçilmez).
   - Bekleme dolunca işaret kalkar; bağ yeniden her aday gibi seçilebilir. Yine vazgeçerse süre katlanır; kalıcı sorunu olan bağ giderek daha uzun sona düşer.
   - Sebep (`17` T-2): yeniden denemeler çoğunlukla geçici çarpışmadır ve MAC onları çözer; paketin gerçekten kaybolduğunu gösteren vazgeçmedir. Eski tetik (18 Kasım) deneme / başarı oranını en az 4 çerçeveyle okuyor, iyi bağları atıp açlık doğuruyordu; tetik kapalıyken ise vazgeçmeler birkaç bağda toplanıyordu (açlık teşhisi).
8. **(19 Kasım'da kalktı)** ASKIDA'dan çıkış. Askıda durumu yoktur.
9. **OLAĞAN → KARIŞTIRILIYOR** (KK-03'ün bağ kanıtıyla): sebep kümeye eklenir; hatıra bugünkü ölçüden alınır, `gecmis`in sonundaki ardışık 0'lar atılır ve o andaki `d_f` saklanır (Y-7); `vaz` boşaltılır ve "veriye uygun değil" işareti kalkar (son tetiklenme anı ve süresi saklanır). Bir selam bit = 1 taşıyorsa kanıt selam yazılmadan önce değerlendirilir: hatıra o selamdan önceki ölçüdür. KARIŞTIRILIYOR iken:
   - gelen selamlar `gecmis`e, bildirilen oran `d_f`ye yazılmaz, zaman aşımı 0 eklemez (ölçü donar, T-7);
   - `beklenen`, `son_selam_t` ve `a` gelen selamlarla izlenir; selam KK-03'e verilir;
   - yeni bir bağ kanıtı gelirse sebebi kümeye eklenir.
10. **KARIŞTIRILIYOR'dan çıkış:**
    - kümedeki her sebebin "bitti"si gelince (KK-03 kural 9): girişten beri `T_HATIRA` geçmediyse hatıra geri yüklenir (`hatirlanan_kalite` kapalıysa `gecmis` boşaltılır); hatıra ETX'i `E_CIK`ı aşmıyorsa OLAĞAN, aşıyorsa KÖTÜ. `vaz` boş başlar; ilk selamda kural 2'nin dondurma çıkışı uygulanır.
    - **üst süre:** girişten beri `T_HATIRA` geçtiği hâlde hâlâ KARIŞTIRILIYOR ise `gecmis` boşaltılır ve bağ KÖTÜ'ye geçer; bağ yeniden ölçülerek döner. Böylece "bitti"si gelmeyen bir giriş bağı süresiz kullanım dışı bırakamaz (İlke 2).
11. **OLAĞAN → KÖTÜ:** `ETX_selam > E_CIK`. Ceza yoktur (19 Kasım: veri cezası tetikle birlikte kalktı).
12. **KÖTÜ → OLAĞAN:** `ETX_selam < E_DON` ve örnek sayısı ≥ `ORNEK_EN_AZ`. KÖTÜ'de karıştırma kanıtı izlenmez (bağ zaten kullanılmıyor); tek istisna: bağı KÖTÜ'den çıkaran selamın biti 1 ise (`alici_bildirimi` açık) bağ OLAĞAN yerine doğrudan KARIŞTIRILIYOR olur, hatıra o anki ölçüdür (Y-8). KÖTÜ'ye girişte olay sayısı kuralı (T-10) uygulanmaz: iki eşikli histerezis aynı işi görür.
13. **Kendim karıştırılırken** (KK-03 kural 4, "karıştırılıyorum"): hiçbir komşunun `gecmis`ine, `d_f`sine ve `vaz`ına yazılmaz (bu sırada duyulan yeni komşu kayda girer ama ilk örneği yazılmaz); zaman aşımı 0 eklemez; `beklenen`, `son_selam_t`, `a` izlenir; silme süresi durur ve çıkışta kaldığı yerden sürer. Çıkışta her komşunun `son_selam_t`si o ana çekilir ve her komşunun ilk selamında kural 2'nin dondurma çıkışı uygulanır. Sebep: karıştırılan benim; komşularıma bildirdiğim oranları bozarsam, karıştırma bitince bana olan bağları hatırladıkları kaliteyle geri alırken benim düşük bildirimimle hemen KÖTÜ'ye düşerler.
    - **(19 Kasım'da kalktı)** başlangıçta ASKIDA'daki bağın OLAĞAN'a dönmesi (Y-2).
    - **Üst süre** `KENDI_UST_SURE` (= `T_HATIRA`, 30 s): süre dolunca dondurma ve MAC sonuçlarının yok sayılması (KK-03 kural 8) biter, bağlar yeniden ölçülür; "karıştırılıyorum" biti ve gönderemezken selam kurulmaması (KK-02 kural 5) durum sürdükçe sürer. Sebep: ardılım bu sırada ölür ya da uzaklaşırsa dondurma sürdükçe ona göndermeyi ve "yolum var" demeyi sürdürürdüm; her dondurmanın üst süresi aynıdır (kural 10) (18 Kasım, Y-6; `17` T-9).
14. **Silme:** `T_SILME` boyunca komşudan hiçbir çerçeve duyulmazsa kayıt silinir (her durumdan; kural 13'teki duraklama hariç).

**Aynı olayda sıra** (bir selam, zaman aşımı, MAC sonucu ya da saniyelik iş birden çok geçiş koşulunu doğurursa):

15. Önce KK-03'ün bağ kanıtı (→ KARIŞTIRILIYOR), sonra vazgeçme tetiği (→ "veriye uygun değil"), en son `ETX_selam` eşikleri. Vazgeçmeler böylece selamla birlikte okunur: selam da gelmiyorsa (KK-03 kural 7) karıştırma kanıtıdır, selam geliyorsa bağ veriyi taşıyamıyordur (`17` T-9). Kanıt önce denendiği için `gecmis`in sonundaki ardışık sıfırlar KK-03 kural 6'nın `k`sına ulaşınca bağ KÖTÜ'ye değil KARIŞTIRILIYOR'a gider: sessizlik karıştırma olarak sınıflanır. `karistirma_durumu` kapalıyken bu istisna yoktur: sessiz komşu ETX'ten KÖTÜ olur; yoksa kapalı kolda ölen komşu ancak 30 s'de silinince giderdi (18 Kasım, G-3). Kenar bağlarda (`k` büyük) `ETX_selam` eşiği sessizlikten önce aşılırsa bağ KÖTÜ olur; bu kabul edilen bir sonuçtur (kenar bağ zaten kötüye yakındır).

## Örnek

- **Veriyi taşıyamayan bağ:** i'nin ardılı j; selamlar iyi geçiyor (ETX 1,4) ama j'ye giden veri çerçevelerinin bazıları yedi denemede de gitmiyor. Son 16 çerçevede üçüncü vazgeçme olunca bağ 5 s "veriye uygun değil" olur. i'nin, maliyeti kendisininkinden düşük başka bir olağan komşusu k varsa ardıl k olur (KK-04); yoksa i j'ye göndermeyi sürdürür. 5 s sonra j yeniden her aday gibidir; i j'ye dönerse ve vazgeçmeler sürerse bu kez 10 s, sonra 20 s, en çok 40 s sona düşer. j'nin ETX'i bu sırada da selamla ölçülür.
- **Karıştırıcıya çok yakın alıcı:** j hiç selam gönderemez; j'ye giden çerçeveler vazgeçmeyle biter. `karistirma_durumu` açıkken art arda üç vazgeçmeden sonra j'den `2·a` içinde selam da gelmemişse KK-03 kural 7 bağ kanıtı verir; bağ KARIŞTIRILIYOR olur, kalitesi (ETX 1,4) hatırlanır. Karıştırıcı susunca j'nin iki temiz selamı gelir, bağ 1,4'le OLAĞAN'a döner.

## Sınanması

- `vazgecme_tetigi` açık ↔ kapalı (ve 18 Kasım'ın veri tetiği): ikizde pencere PDR'si ve iletim kaybı (İ); birincil hücrede zarar yok. Tanı: tetik sayısı, tetiklenen bağın kâhin bandı, tetikten sonra ardılın değişip değişmediği ve o bağdaki vazgeçmeler, vazgeçmelerin bağlara dağılımı (en kötü beş bağın payı; açlık teşhisinde tetiksiz kolda %41).
- `hatirlanan_kalite` açık ↔ kapalı: birincil ve dayanıklılık hücresinde `PDR_açık` ve sessiz dönemin ilk saniyelerindeki teslim; ikizde fark yok.
- Eşikler (`E_CIK`, `E_DON`): ardıl değişim sıklığı ve KÖTÜ ↔ OLAĞAN geçiş sayısı.

## Kaynak

ETX [36]; selam geçmişi, ileri sarma, geri alma ve zaman aşımı katsayısı Babel [4] (RFC 8966 Ek A; `protokoller/babel_bicim.py`); üst sınır MRHOF [64]; veri onayının bağ tahminine katılması 4B [69] (bizde maliyete değil, vazgeçme olarak yalnız ardıl seçimine); iki eşikli kullanılabilirlik, vazgeçme tetiği ve hatırlanan kalite bu tasarımın.
