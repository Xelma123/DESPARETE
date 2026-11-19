# Faz 5-3 · yeni çekirdek ↔ Babel ve genel bileşenlerinin ablasyonu, karıştırıcısız ikizde ve birincil hücrede — beklenti ve karar kuralı (ölçmeden önce)

> 19 Kasım 2026 · `v2/12` §1.2 (5-3: mekanizma başına A/B) · tasarım `v2/17` (19 Kasım: T-2 vazgeçme tetiği, T-11 iki ölçülü geçiş, T-12 maliyet eğimi ve döngü bekçisi, T-13 tur ve açlık kalktı) · kurallar `v2/kural/KK-00`…`KK-05` (19 Kasım), kod `protokoller/desparete5*.py` (commit `d9a6df7`) · karşılaştırma tabanı: teşhis (c) (`arsiv/teshis/faz5_2_rakip_cizgisi_2026-11-15/`: Babel, kâhin, v0.4.1), ilk ölçüm (`../faz5_3_cekirdek_2026-11-18/`: 18 Kasım'ın çekirdeği), açlık teşhisi (`../faz5_3_aclik_2026-11-18/`: veri tetiği kapalı 18 Kasım çekirdeği, `vtk0`). Sonuçlar ayrı `sonuc.md`ye yazılır; bu dosyaya dokunulmaz. Öngörüler duman koşusundan önce yazıldı ve commit'lendi. Yeni çekirdek referans dünyada henüz hiç koşmadı; yalnız küçük test dünyasında (birim ve uçtan uca testler, eşdeğerlik) ve aletin sınamasında eski `olcek_1_50` dünyasında koştu (aşağıda).

## Sorular

- **S1 · genel düzey.** Yeni çekirdek (maliyet eğimi, vazgeçme tetiği, iki ölçülü geçiş; karıştırmaya karşı mekanizmalar kapalı) karıştırıcısız ikizde Babel'e göre nerede? İlk ölçümün açığı (`G_İ` = +0,120) kapandı mı?
- **S2 · başlangıç çizgisi.** Birincil hücrede yeni çekirdeğin `PDR_açık`ı ve karıştırmaya özgü kaybı Babel'e göre nerede? Karıştırma katmanının A/B'leri bu çizginin üstüne kurulur.
- **S3 · kontrol yükü ve gecikme** (T-19).
- **S4 · bileşenler** (genel sınıf; K-247, `KK-00` A/B ölçütleri). Vazgeçme tetiği, iki ölçülü geçiş ve maliyet eğiminin her biri ikizde katkı veriyor mu, birincil hücrede zarar veriyor mu?
- **S5 · tanı** (`KK-00` tanı kaydı). Döngü ve bayat bilgi ne sıklıkta? Son çare, maliyet tavanı ve yol yok bölümleri ne kadar? TTL kaybı, atlama sayısı ve yol maliyetinin dağılımı ne? Vazgeçme tetiği ne sıklıkla çalışıyor, hangi bağlarda, ardıl sonra değişiyor mu, vazgeçmeler bağlara nasıl dağılıyor?

## Düzen

    # bir adım = bir kol × bir hücre (sekiz adım)
    PYTHONIOENCODING=utf-8 py -3.11 -u <bu dizin>/olcum.py --dunya referans_2026 \
        --hucre ikiz|birincil --kollar <kol> \
        --tohumlar 1003,1004,1005,1006,1007,1008,1009,1010 --isci 8 --kayit <bu dizin>/kayit_<kol>_<hücre>.json

- **Hücreler** ilk ölçümle aynı (`formasyon · yere_toplama`, tam pencere: ısınma 50 · ölçüm sonu 320 · koşu 350 s; karıştırıcı 150. saniyede açılır):
  - **İ · karıştırıcısız ikiz** (`--sinif yok`, hayalet çizelge 10:20); ölçü pencere PDR'si.
  - **B · birincil** (`derin_sizma`: araç, 15 s açık · 15 s sessiz; ortalama 10 W, açıkken 20 W); ölçü `PDR_açık`.
- **Kollar** (tohum 1003–1010; 4 kol × 2 hücre × 8 tohum = 64 koşu). Değerler `KK-00`'ın 19 Kasım başlangıç değerleri (bekletme 1 s). Karıştırmaya karşı mekanizmalar (`karistirma_durumu` · `alici_bildirimi` · `hatirlanan_kalite`) hepsinde kapalı; çoğaltma yok.

  | kol | `egim` | `vazgecme_tetigi` | `duzgun_gecis` | ne ölçer |
  |---|---|---|---|---|
  | **çekirdek** (`desparete5_cekirdek`) | açık | açık | açık | yeni çekirdek (S1–S3) |
  | vaz0 | açık | kapalı | açık | vazgeçme tetiğinin katkısı: çekirdek − vaz0 |
  | düz0 | açık | açık | kapalı (%10 eşik) | iki ölçülü geçişin katkısı: çekirdek − düz0 |
  | eğim0 | kapalı (18 Kasım'ın yol seçimi: FD, tur, açlıkta istek) | kapalı | — | eğimin katkısı: vaz0 − eğim0 |

  - Eğimin katkısı vaz0 ile eğim0 arasında ölçülür, çünkü vazgeçme tetiğinin işaretini yalnız eğim okur (KK-04); eğim kapalıyken tetik açık olsa da etkisizdir. İki kolda da veri sonucuna bağlı hiçbir tetik yoktur; fark yalnız yol seçimidir (eğimle birlikte iki ölçülü geçiş; eğim0'da 18 Kasım'ın %10 eşiği).
  - Eğim0, açlık teşhisinin `vtk0` koluna karşılık gelir (18 Kasım'ın yol seçimi, veri tetiği yok); farkı bekletmenin 1 s olmasıdır (`vtk0`'da 2 s). Bu eşlik kod okumasına dayanır, koşuyla denetlenmedi; karşılaştırma yalnız betimleyicidir.
  - vaz0, düz0 ve eğim0 ölçüm aletinin içinde, koşu süresince profillere eklenir ve çıkarılır (`olcum.py`); protokolün kodu değişmez. Kolun etiketi koşunun rastgele akışlarına girmez: kollar aynı tohumda aynı dünyayı görür.
- **Karşılaştırılanlar yeniden koşulmaz:** Babel, kâhin ve v0.4.1 teşhis (c)'nin; 18 Kasım'ın çekirdeği ilk ölçümün; `vtk0` açlık teşhisinin kayıtlarından okunur.
  - Gerekçe: teşhis (c)'den (`ef6d5cb`) ilk ölçüme kadar simülatörde yalnız köken defteri değişti ve Babel'in duman satırı iki hücrede birebir çıktı (ilk ölçüm, kural 0). İlk ölçümün beklentisinden (`236f7af`) bu yana simülatörde, kayıp anatomisi aletinde, kâhinde ve Babel'de hiçbir değişiklik yok (`git diff --stat 236f7af d9a6df7 -- sim2 kalibrasyon protokoller/babel*`: yalnız `kalibrasyon/aodv_uygunluk.py`, profil eklendi). Simülasyon belirlenimli.
  - Denetim (kural 0): duman koşusunda 18 Kasım'ın çekirdeği (`desparete5_eski_cekirdek`; `ESKI_CEKIRDEK` bayrakları, `DEGERLER_ESKI`) iki hücrede ilk ölçümün duman satırıyla birebir olmalı. Bu ayrıca yeni kodun eski kipinin 18 Kasım davranışını referans dünyada da birebir ürettiğini gösterir (küçük test dünyasındaki eşdeğerliğin, `../faz5_3_kod_2026-11-19/esdegerlik.txt`, tamamlayıcısı).
- **Alet** (`olcum.py`, bu commit): her koşu kayıp anatomisi aletinin işçisiyle (`kalibrasyon/kayip_anatomisi.py::_is`) olduğu gibi yapılır; sonuç satırı, kayıp grupları ve protokol sayaçları ilk ölçümünkiyle aynı yoldan çıkar. Üstüne yalnız okuyan bir kaydedici eklenir:
  - **tetik:** vazgeçme tetiğinin her çalışması: düğüm, komşu, an, o an ardıl mıydı, bekleme süresi, kâhinin o andaki tek deneme başarısı; işaret sürerken ardılın değişip değişmediği ve ne kadar sonra; işaret sürerken o bağa yazılan veri sonucu ve vazgeçme sayısı.
  - **paket:** geçide giden her telemetri paketi için kaynağın ilk kararındaki geçide maliyeti ve kararlarda görülen en büyük atlama sayısı.
  - İç denetimler: tetik sayısı = `bag.vaz_tetik`; işaretliyken vazgeçme ≤ `bag.vazgecme`; tetiksiz kollarda tetik yok; ilk kararı kaynakta görülmeyen telemetri paketi yok.
  - Denetim (kural 0): duman koşusunda çekirdek, kaydediciyle ve doğrudan kayıp anatomisi aletiyle koşulur; iki satır bütün alanlarda birebir olmalı (kaydedici koşuyu değiştirmiyor).
  - `KK-00`'ın tanı kaydındaki "tetikten sonra o bağdaki vazgeçmeler" yalnız işaret sürerken sayılır; işaret bittikten sonrakiler o bağın vazgeçme dağılımında görünür.
- **Aletin sınaması** (ölçüm değil, karara girmez; `sinama/`, komutlar `sinama/komutlar.txt`): eski `olcek_1_50` dünyasında, kısa pencere, tohum 1003. Beş kol ikizde, çekirdek birincilde koşuldu; ayrıca çekirdek iki hücrede kaydedicisiz koşuldu.
  - Hepsi hatasız bitti, iç denetimler geçti.
  - Kaydedicili ve kaydedicisiz çekirdek iki hücrede bütün alanlarda birebir.
  - `sonuc_hesap.py` duman kipinde baştan sona çalıştı.
  - Bu sınamanın sayıları öngörüler yazılırken görüldü (ikizde pencere PDR'si: çekirdek 0,934 · vaz0 0,928 · düz0 0,943 · eğim0 0,928 · 18 Kasım çekirdeği 0,954). Başka dünya, tek tohum ve 30 saniyelik pencere oldukları için öngörülerin dayanağı değildir; öngörülerin dayanağı referans dünyanın kayıtlarıdır.
- **Dayanıklılık hücresi ve yer karıştırıcılı aile** (`12` Faz 5; `KK-00` A/B ölçütleri) bu ölçüme eklenmedi. Üç bileşen de genel sınıftadır (K-247): katkıları ikizdeki ablasyonla beyan edilir, karıştırma altındaki ölçütleri "birincil hücrede zarar yok"tur. İki hücre karıştırmaya karşı mekanizmaların A/B'lerinde ve kapanışta (5.7) koşulur; yeni çekirdeğin bu hücrelerdeki çizgisi de orada çıkar. Eklemek ölçümü iki katına çıkarırdı (~14 sa).
- **Yürütme:**
  - Koşu dondurulmuş kopyadan (`kopya/`, duman notunun commit'iyle dosya özeti birebir: `kopya_ozet.txt`), `kosu.sh` ile sekiz adımda; saatler `zaman.txt`e. Yanında başka ağır iş yok.
  - Sıra: bu beklenti (öngörüler) commit'lenir → duman koşusu → duman notu bu dosyanın son bölümüne yazılır ve ikinci commit'le girer → o commit'ten dondurulmuş kopya → ölçüm. Adımların sırası: çekirdek (İ, B) → vaz0 → eğim0 → düz0; S1–S3'ün girdisi ilk iki adımdadır.
  - Aletin gerçek koşuda sınaması: `sh kosu.sh duman` (kısa pencere, tohum 1003; dört kol ve 18 Kasım'ın çekirdeği iki hücrede, ayrıca çekirdek kaydedicisiz; çalışma ağacından, kod bu commit'le aynı) → `duman_kisa.txt`. Ölçüm değil, hiçbir karara girmez.
  - Karar kuralının hesabı `sonuc_hesap.py` (koşudan önce yazıldı; karşılaştırma kayıtlarının doğru kola yüklendiği denetlendi: eski çekirdek 0,810 · 0,410, `vtk0` 0,946, Babel 0,930 · 0,663, önceki sonuçlarla aynı; aletin sınama kaydıyla baştan sona çalıştı).
- **Süre tahmini ~7 sa (5,5–9):** adım başına 45–75 dk (8 koşu, 8 işçi, tek dalga). Dayanak: `vtk0`'ın koşu başına süresi ikizde 34–49 dk, 18 Kasım çekirdeğininki iki hücrede 48–77 dk (açlık teşhisi, ilk ölçüm); aletin sınamasında yeni kollar 18 Kasım çekirdeğinden biraz hızlı. Duman ~25 dk. Her adım 8 saatin altında; adımlar ayrı ayrı da koşulabilir.

## Tanımlar

İlk ölçümdeki gibi:
- **`PDR_açık`:** ölçüm penceresinde karıştırıcının açık dönemlerinde doğan paketlerin teslim oranı (K-222). **Hayalet `PDR_açık`:** ikizde aynı zaman dilimlerinde (15/15) doğan paketlerin teslim oranı.
- **Eşli fark:** iki kolun aynı tohumdaki değerlerinin farkı; ortalaması ve yönü aynı olan tohum sayısı yazılır.
- **Ayrışma kuralı:** eşli farkın ortalaması eşiği aşar ve 8 tohumun en az 6'sında yön aynıysa "ayrışıyor"; değilse "8 tohumda ayırt edilemedi".
- **Karıştırmaya özgü kayıp:** `Δ_k = PDR_açık(B) − hayalet PDR_açık(İ)`, tohum başına eşli.
- **Gecikme tavanlı `PDR_açık`:** gecikmesi tavanı aşmayan teslimler; ana tavan 5 s, duyarlılık 3,5 ve 10 s (K-246). **Tavanın bedeli** = ölçü − ölçü(tavan).
- **Kayıp grupları:** R (rota yokluğu: `rota_gecersiz` · `hedef_yok` · `tampon_asimi`) · İ (iletim) · K (kuyruk) · T (ömür, TTL), hücrenin birincil ölçüsünün paydasına oranla.
- **Kontrol payı:** kontrol çerçevelerinin kanal süresi / bütün gönderimlerin kanal süresi (bütün koşu, ağ toplamı).
- **Çözünürlük:** `R` = 0,0126 (K-224).

Bu ölçümde eklenenler:
- **Bileşen farkı:** açık kol − kapalı kol, eşli (çekirdek − vaz0 · çekirdek − düz0 · vaz0 − eğim0).
- **Kâhin bandı** (tetiklenen bağ): kâhinin tek deneme başarısı `p` (sönümleme dâhil, girişim hariç) ile `p_atlama = 1 − (1 − p)^7` (en çok 7 deneme); iyi ≥ 0,90 · orta ≥ 0,50 · kötü.
- **Kaynak maliyeti:** telemetri paketinin kaynağındaki ilk kararda kaynağın geçide maliyeti (ETX; 1 ETX'lik kutular, ∞ ayrı); yalnız ölçüm penceresinde doğan paketler.
- **Atlama sayısı:** teslim edilen telemetri paketinin = kararlarda görülen en büyük TTL harcaması + 1; döngüde harcanan atlamalar da sayılır.
- **Yol yok bölümü:** düğümde hiç aday kalmayan süre (KK-04, `rota.yol_yok`; süresi `rota.yol_yok_sure_ms`, yalnız biten bölümler).

## Karar kuralı (8 tohum)

0. **Geçerlilik.**
   - 64 koşunun hepsi kayıtta; her koşuda korunum geçerli, doğum çelişkisi 0, atfsız düşüş yok, kaydedicinin iç denetimleri geçmiş.
   - Teşhis (c)'nin Babel, kâhin ve v0.4.1 satırları ve ilk ölçümün çekirdek satırları 16'şar; açlık teşhisinin `vtk0` satırları 8.
   - Duman koşusunda: çekirdeğin kaydedicili ve kaydedicisiz satırı iki hücrede bütün alanlarda birebir; 18 Kasım'ın çekirdeği iki hücrede ilk ölçümün duman satırıyla birebir (ortak alanlar ve sayaçlar eşit, yeni sayaçlar sıfır).
   - Biri tutmazsa önce sebebi aranır; karşılaştırma satırları gerekirse yeniden koşulur ve tablolar o zamana kadar kullanılmaz.
1. **S1 · genel düzey (İ).** `G_İ = PDR(Babel) − PDR(çekirdek)`, eşli, eşik 0,02, ayrışma kuralıyla.
   - **Çekirdek geride** (`G_İ` ≥ 0,02 ve ayrışıyor): yeni çekirdeğin de genel bir açığı var. Sıradaki iş bu açığın teşhisi; S4'ün bileşen farkları ve S5'in tanısı onun girdisidir. Karıştırma katmanı ondan sonra.
   - **Ayırt edilemedi** ya da **çekirdek ileride:** genel düzey Babel'le eş ya da önde. S4'te zararlı bileşen yoksa sıradaki iş karıştırma katmanı: kalabalık yanlış alarmının düzeltmesi (KK-03 kural 12) ve `karistirma_durumu`nun A/B'si, `KK-00`'ın sınıfa göre ölçütleriyle.
   - Ayrıca çekirdek − `vtk0`, çekirdek − 18 Kasım çekirdeği ve çekirdek − v0.4.1 yazılır (eşik 0,02); karar değiştirmez.
2. **S2 · başlangıç çizgisi (B).** Betimleyici.
   - `PDR_açık(Babel) − PDR_açık(çekirdek)`, v0.4.1 − çekirdek ve 18 Kasım çekirdeği − çekirdek, eşli, eşik 0,02.
   - Her kolun `Δ_k`'si ve `Δ_k(çekirdek) − Δ_k(Babel)` (eşik 0,03).
   - Çekirdek B'de Babel'den ayrışarak öndeyse bu kazanç genel mekanizmalardan gelir. "Karıştırmaya özgü" denmez; iddia dili `06` §0.4.5'tedir.
3. **S3 · kontrol yükü ve gecikme (T-19).**
   - Her kolda ve hücrede kontrol kanal süresi, kontrol payı, tavanın bedeli (3,5 · 5 · 10 s) ve gecikmenin p50 · p95 · p99'u.
   - Bir hücrede 5 s tavanın bedeli ≥ 0,02 ise "tavan bağlayıcı" yazılır; o hücrede gecikme tavanlı `PDR_açık` birincil ölçüyle birlikte izlenir.
4. **S4 · bileşenler.** Her bileşen için açık − kapalı, eşli, eşik 0,02, ayrışma kuralıyla:
   - **İ:** artı yönde ayrışıyorsa "katkı var"; eksi yönde ayrışıyorsa **"zararlı"**; değilse "katkı 8 tohumda ayırt edilemedi".
   - **B:** eksi yönde ayrışıyorsa **"birincilde zarar"**; değilse "zarar yok" (artı yönde ayrışıyorsa ayrıca "birincilde katkı" yazılır, betimleyici).
   - İ'de zararlı ya da B'de zarar veren bir bileşen varsa, karıştırma katmanından önce o bileşenin teşhisi gelir, kendi beklentisiyle.
   - Bu kural bir bileşeni kendiliğinden çıkarmaz ya da tutmaz. Katkısı ayırt edilemeyen bir bileşenin sürümde kalıp kalmayacağına sonuçtan sonra, tanı ölçüleriyle birlikte karar veririm; katkısı raporda "8 tohumda ayırt edilemedi" diye yazılır.
   - Betimleyici: yeni yol seçimi bütünüyle (çekirdek − eğim0, iki hücre) · 19 Kasım ↔ 18 Kasım çekirdeği (çekirdek − eski, iki hücre) · bekletme 1 s ↔ 2 s (eğim0 − `vtk0`, İ).
5. **S5 · tanı** (betimleyici; sayaçlar bütün koşu, ağ toplamı, koşu başına):
   - Her kolda kayıp grupları (T dâhil), karar/paket, atlama başarısızlığı, deneme başarısı.
   - Vazgeçmelerin bağlara dağılımı: toplam, ayrı bağ, en kötü bağ, en kötü beş bağın payı (18 Kasım çekirdeği ve `vtk0` dâhil).
   - Sayaçlar: tetik, vazgeçme, katlama · selamdan KÖTÜ ve dönüş · ardıl değişimi, sebebine göre (zorunlu · isteğe bağlı · veriye uygunsuzluk) · son çare · yol yok ve ortalama süresi · tavan aşımı · bayat bilgi · kesin döngü · dışlama · selam ve ara ilan · bekletme ve süresi dolan · komut kararları. Eğim0'da 18 Kasım'ın sayaçları (açlık, tur artışı).
   - Kaynak maliyetinin p50 · p90 · p99'u, en büyüğü, 16 ETX ve üstünün payı, ∞ payı; teslim edilen paketlerin atlama sayısının p50 · p90 · p99'u ve en büyüğü; bütün kararlarda görülen en büyük atlama sayısı.
   - Penceredeki tetikler (çekirdek ve düz0): koşu başına sayı, kâhin bandı, ardıl payı, ardılın işaret sürerken değiştiği pay ve gecikmesinin medyanı, işaret sürerken veri sonucu ve vazgeçme sayısı, bekleme sürelerinin dağılımı.
6. **Kâhin** yalnız referanstır (K-248): kâhine oran yazılır; bir kolun kâhini bir tohumda `R`'den fazla aştığı hücreler listelenir; karar değiştirmez.

## Öngörü

Düzeyler (8 tohum ortalaması; kâhin, Babel, v0.4.1, 18 Kasım çekirdeği ve `vtk0` biliniyor):

| kol | İ · pencere PDR | B · `PDR_açık` |
|---|---|---|
| kâhin | 0,917 | 0,779 |
| Babel | 0,930 | 0,663 |
| v0.4.1 | 0,785 | 0,567 |
| 18 Kasım çekirdeği | 0,810 | 0,410 |
| `vtk0` (18 Kasım, veri tetiği kapalı) | 0,946 | — |
| **çekirdek** | **0,95 ± 0,02** | **0,62 ± 0,12** |
| vaz0 | 0,945 ± 0,02 | 0,58 ± 0,12 |
| düz0 | 0,95 ± 0,02 | 0,62 ± 0,12 |
| eğim0 | 0,94 ± 0,02 | 0,50 ± 0,12 |

S1 (güven orta):
- `G_İ` −0,04 … 0,00. En olası hüküm "ayırt edilemedi", ikinci olası "çekirdek ileride"; "çekirdek geride" olası değil.
  - Dayanak: `vtk0` aynı dünyada 0,946'ya çıktı (Babel'den +0,016, 8/8). Açığın kökü veri tetiğiydi; yeni çekirdekte yok. Kalan kayıp çoğunlukla iletimde (`vtk0`'da İ 0,052 · R 0,003).
  - Risk: son çare ve döngü ömür kaybı (T) ve fazladan atlama getirebilir; vazgeçme tetiği kalabalık kanalda yanlış bağları işaretleyebilir.
- Çekirdek − `vtk0` −0,01 … +0,02 → ayırt edilemedi. Çekirdek − 18 Kasım çekirdeği +0,10 … +0,17, en az 7/8.

S2 (güven düşük):
- B'de Babel − çekirdek −0,10 … +0,10 → ayırt edilemedi (Babel'in tohumlar arası sapması 0,139).
  - Eğim, karıştırmanın düşürdüğü bağlar yüzünden FD koşulunu geçen yedek kalmayınca başlayan açlık zincirini yok eder; uzak düğümler yokuş aşağı ya da son çare bir komşuyla rotada kalır. 18 Kasım çekirdeğinin B'deki açık dönem kaybı R 0,512'ydi; ilk ölçümün duman koşusunda rotasızlıktan düşenlerin neredeyse tamamı karıştırıcının etki alanı dışındaki düğümlerdeydi.
  - Vazgeçme tetiği karıştırılan alıcıya giden bağı üç vazgeçmede "veriye uygun değil" diye işaretler; G1'de başka aday varsa veri oraya gider (KK-04). Babel bunu yapmaz.
  - Buna karşılık selam eşikleri karıştırılan bölgedeki bağları KÖTÜ'ye düşürür; aday kalmayan düğümde bekletme 1 s'dir.
- 18 Kasım çekirdeği − çekirdek: −0,30 … −0,10, 8/8 (çekirdek önde). v0.4.1 − çekirdek: −0,15 … +0,05.
- `Δ_k(çekirdek)` −0,45 … −0,20 (Babel −0,265); `Δ_k(çekirdek) − Δ_k(Babel)` ayırt edilemedi.
- B'nin evreleri: çekirdeğin "önce" teslimi İ düzeyinde (0,93–0,97); sessiz dönemi 0,80–0,93 (Babel 0,916): KÖTÜ'ye düşen bağın dönmesi `ORNEK_EN_AZ` selam ister.

S3:
- Kontrol kanal süresi İ'de çekirdek, vaz0, düz0 için 17–28 s, kontrol payı %5–8 (Babel 67,8 s · %14,7; `vtk0` 22,0 s · %6,1).
  - Dayanak: eğimin selamı tur alanı olmadığı için 2 bayt küçük; tur isteği yok (`vtk0`'da koşu başına 342 istek). Buna karşılık son çare ve döngü işaretleri ara ilan doğurur.
  - Eğim0 `vtk0`'a yakın: 18–26 s. B'de her kol İ'dekinin en çok 1,5 katı.
- 5 s tavanın bedeli iki hücrede de < 0,01.
- Gecikmenin p99'u: İ'de çekirdek 0,2–0,6 s (`vtk0` 0,30 · Babel 0,23); B'de 0,4–2,0 s (Babel 1,31 · 18 Kasım çekirdeği 3,81).

S4 (güven düşük):
- **Vazgeçme tetiği** (çekirdek − vaz0): İ'de +0,000 … +0,025 → en olası "katkı ayırt edilemedi", ikinci olası "katkı var". B'de +0,00 … +0,08 → zarar yok.
  - Dayanak: tetik kapalıyken vazgeçmelerin %41'i en kötü beş bağda (açlık teşhisi, `vtk0`). Tetik bu bağlardan veriyi alırsa iletim kaybı azalır; ama her tetik üç kayıpla başlar, alternatif yoksa veri aynı bağda kalır.
- **İki ölçülü geçiş** (çekirdek − düz0): iki hücrede de −0,01 … +0,01 → ayırt edilemedi. İsteğe bağlı geçiş sayısı çekirdekte düz0'ınkinin 0,3–0,8 katı.
- **Eğim** (vaz0 − eğim0): İ'de −0,01 … +0,015 → ayırt edilemedi (`vtk0`'da R zaten 0,003; kazanılacak yer yok). B'de +0,03 … +0,15 → en olası "birincilde katkı"; zarar yok.
- Betimleyici:
  - yeni yol seçimi bütünüyle (çekirdek − eğim0) İ'de +0,00 … +0,03, B'de +0,05 … +0,20;
  - eğim0 − `vtk0` −0,01 … +0,005 (bekletme 1 s, süresi dolan biraz artar).

S5 (güven düşük; koşu başına, ağ toplamı):
- Kayıp grupları, çekirdek: İ'de R 0,000–0,006 · İ 0,030–0,055 · T 0,000–0,002; B'nin açık döneminde R 0,02–0,15 · İ 0,18–0,32 · T ≤ 0,01. Eğim0'da B'nin R'si çekirdeğinkinden yüksek (0,05–0,30).
- Vazgeçme tetiği, çekirdek: İ'de 50–300 tetik; B'de İ'dekinin 1,5–5 katı.
  - Tetiklenen bağların kâhin bandı İ'de çoğunlukla iyi (pay 0,75–1,00; kâhin girişimi görmez, açlık teşhisinde de veriyi taşıyamayan bağlar iyi banttaydı).
  - Ardıl payı ≥ 0,90 (veri yalnız ardıla gider).
  - İşaret sürerken ardılın değiştiği pay İ'de 0,30–0,80.
- Vazgeçmelerin dağılımı: vaz0'da en kötü beş bağın payı 0,30–0,50 (`vtk0` 0,41); çekirdekte 0,12–0,30. Çekirdeğin toplam vazgeçmesi vaz0'ınkinden %10–40 az.
- Yol seçimi, çekirdek, İ: kesin döngü 0–20 · bayat bilgi 10–300 · son çare 5–100 · tavan aşımı 0–5 · yol yok 0–30 bölüm, ortalama süresi 0,2–2 s. B'de döngü 0–100; son çare ve yol yok İ'dekinin 2–10 katı.
- Kaynak maliyeti, İ: p50 4–8 ETX · p99 ≤ 16 ETX · 16 ETX ve üstü < %1 · ∞ < %0,5 (tavan 32 ETX bağlayıcı değil).
- Atlama sayısı, İ: teslim edilenlerde p50 3–4 · p99 6–8 · en çok ≤ 10; bütün kararlarda en çok ≤ 12. B'de bütün kararlarda en çok 31'e kadar çıkabilir (bir döngüde TTL'nin tükenmesi).

Kâhin:
- İ'de çekirdek kâhini 2–7 tohumda `R`'den fazla aşar (Babel 4/8, `vtk0` ortalamada +0,029); B'de hiçbir kol aşmaz.

## Duman koşusundan sonra (ölçümden önce)

(Duman koşusundan sonra yazılır.)
