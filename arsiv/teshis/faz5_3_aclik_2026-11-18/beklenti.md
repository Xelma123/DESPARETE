# Faz 5-3 · açlık teşhisi — çekirdeğin rota yokluğu kaybının kökü, karıştırıcısız ikizde — beklenti ve karar kuralı (ölçmeden önce)

> 18 Kasım 2026 · ilk ölçümün kararı (`../faz5_3_cekirdek_2026-11-18/sonuc.md` §2: çekirdek ikizde geride → sıradaki iş genel açığın teşhisi) · kod `protokoller/desparete5*.py` (ilk ölçümün kodu, `0fdd3ce`'den beri değişmedi) · alet `aclik_teshisi.py`, hesap `sonuc_hesap.py` (bu dizinde, koşudan önce yazıldı). Sonuçlar ayrı `sonuc.md`ye yazılır; bu dosyaya dokunulmaz. Bu bir A/B değil, bir teşhistir; eşikler karar kolaylığıdır. Öngörüler duman koşusundan önce yazıldı ve commit'lendi.

## Bilinenler (ilk ölçüm, ikiz, koşu başına)

- Çekirdeğin Babel'e açığı (0,810 ↔ 0,930) tamamen R grubunda: rota yokluğu kaybı 0,139, Babel'de 0. İletim kaybı ve kontrol yükü Babel'den iyi.
- Sayaçlar (bütün koşu): açlık 822 · zorunlu geçiş 747 · ardıldan ∞ alındı 1146 · veriyle KÖTÜ 399 · selamdan KÖTÜ 777 · `d_f` bayatladı 585 · komşu silindi 337 · geçidin tur artışı 92 · ortalama açlık 1,90 s.
- Kuraldan sonra görülen (karar girdisi değildi): teslim ile açlık sayısı arasında r = −0,97.
- Babel aynı hücrede koşu başına 18 geri çekme gönderiyor (teşhis (c), `kayit_ikiz.json`, `geri_cekme`; bütün hedefler için). Çekirdekte ardıldan ∞ alınması 1146.

## Sorular

- **S1 · kök.** Açlık zincirinin ilk halkası ne? Ardılın bağının kullanımdan çıkması mı (hangi kuralla), komşunun silinmesi mi, yok saymanın dolması mı?
- **S2 · çıkış haklı mı.** Kök bağ kaynaklıysa, ardılın bağı kullanımdan çıktığı anda gerçekte kötü müydü? Ölçü kâhinin bağ kalitesi.
- **S3 · elde ne vardı.** Kök bölüm başladığında düğümün elinde iki tür komşu olabilir:
  - OLAĞAN ama ilanı uygulanamaz komşu: yeni bir tur yardım ederdi.
  - Bağı dışlanmış ama ilanı uygulanabilir komşu: bağ kullanılsaydı yol vardı.
- **S4 · zincir.** Kaybın ne kadarı, yukarıdaki düğümün ∞ ilanıyla açılan bölümlerde?
- **S5 · veri tetiği.** `veri_kotu_tetigi` kapalıyken ikizde teslim ne olur?
- **Betimleyici:**
  - bölüm süreleri ve bölümlerin nasıl bittiği;
  - bağ çıkışlarının sebepleri ve KÖTÜ'de kalış süresi;
  - yeni turun ağa yayılması.

## Düzen

    # adım 1 · çekirdek (ilk ölçümün koşusunun aynısı, kayıtla)
    cd kopya && PYTHONIOENCODING=utf-8 py -3.11 -u ../aclik_teshisi.py --dunya referans_2026 \
        --kollar cekirdek --tohumlar 1003,1004,1005,1006,1007,1008,1009,1010 --isci 8 \
        --kayit ../kayit_cekirdek.json
    # adım 2 · veri tetiği kapalı
    … --kollar vtk0 … --kayit ../kayit_vtk0.json

- **Hücre:** ilk ölçümün İ hücresi, karıştırıcısız ikiz.
  - `formasyon · yere_toplama`, tam pencere: ısınma 50 s, ölçüm sonu 320 s, koşu 350 s.
  - Bayraklar: `--sinif yok --hayalet 10:20`.
  - Tohumlar 1003–1010.
- **Kollar:**
  - `cekirdek`: `desparete5_cekirdek`, ilk ölçümle aynı.
  - `vtk0`: aynısı, yalnız `veri_kotu_tetigi` kapalı.

  İki kol × 8 tohum = 16 koşu.
- **Alet** (`aclik_teshisi.py`):
  - Kayıp anatomisi aletinin işçisini (`kayip_anatomisi._is`) olduğu gibi çağırır. Sonuç satırı, kayıp grupları ve sayaçlar ilk ölçümle aynı yoldan çıkar.
  - Protokolün sınıflarına yalnız okuyan sarmalayıcılar takar ve koşudan sonra geri alır. Protokolün hiçbir alanına yazmaz; okurken sıfırlayan yöntemleri çağırmaz.
  - Koşudan sonra her bağ çıkışına kâhinin o andaki bağ kalitesi eklenir. Bu ölçü yalnız teşhiste kullanılır; protokol onu görmez.
  - `vtk0` kolunda bayrak, işçinin içinde o koşu süresince değiştirilir. Bayraklar koşu kimliğine girer.
- **Aletin sınaması (ölçüm değil):**
  - Küçük test dünyasında (12 düğüm; `formasyon-yok` ve `bagimsiz-yok`; iki kol): dört koşunun dördünde sonuç kaydediciyle ve kaydedicisiz birebir aynı, iç denetimler geçti.
  - Geliştirme dünyasında (`olcek_1_50`, kısa pencere, tohum 1003) alet ve hesap uçtan uca çalıştı. Geçerlilik denetimi, referans dünyanın duman kaydıyla farkı beklendiği gibi yakaladı.
  - Bu koşuların sayıları hiçbir öngörüye ya da karara girmez.
- **Yürütme:**
  - Koşu dondurulmuş kopyadan (`kopya/`), `kosu.sh` ile iki adımda; saatler `zaman.txt`e yazılır. Kopyanın dosya özeti, duman notunun commit'iyle birebir olmalı (`kopya_ozet.txt`). Yanında başka ağır iş yok.
  - Sıra: bu beklenti (öngörüler) commit'lenir → duman koşusu → duman notu bu dosyanın son bölümüne yazılır ve ikinci commit'le girer → o commit'ten dondurulmuş kopya → ölçüm.
  - Duman: `sh kosu.sh duman` (kısa pencere, tohum 1003, iki kol; çalışma ağacından, kod bu commit'le aynı) → `duman_kisa.txt`. Ölçüm değil, hiçbir karara girmez.
- **Süre tahmini ~2,5–3 sa:**
  - Her adım ~1,3–1,5 sa (8 koşu, 8 işçi, tek dalga). Dayanak: ilk ölçümde ikiz koşuları 51–77 dk sürdü. Kaydedicinin ve kâhin ekinin payı küçük.
  - Duman ~10 dk.
  - Her adım 8 saatin altında.

## Tanımlar

- **Ardıl kaybı:** ardılın, seçimde uygun aday olmaktan çıkması. Sonucu açlık ya da başka komşuya geçiştir. Sebepler:
  - `silindi`: komşu kaydı silindi.
  - `bag:<çıkış sebebi>`: ardılın bağı OLAĞAN'dan çıktı.
  - `geri_cekme`: ardıl ∞ ilan etti.
  - `yoksay_doldu`: yok sayma süresi doldu ve son ilan uygulanamıyor.
  - `maliyet`: toplam maliyet taştı.
- **Bağ çıkışı:** bağın OLAĞAN'dan çıkışı. Sebepler:
  - `selam_asim`: beklenen selam gelmedi ve ETX_selam > E_CIK.
  - `selam_alim`: selam alındı (boşlukla ya da düşen `d_f` ile) ve ETX > E_CIK.
  - `veri`: veri tetiği.
  - `df_bayat`: komşu beni `T_SILME` boyunca listelemedi.
  - `silindi`: komşu kaydı silindi.
- **Açlık bölümü:** ardıl kaybı açlıkla sonuçlanınca açılır, ardıl yeniden seçilince kapanır. Sayaçtaki `rota.aclik` ile aynı olay; alet ikisinin eşitliğini denetler.
- **Zincir ve kök:**
  - Bölümün sebebi `geri_cekme` ise ve eski ardılın o an açık bir bölümü varsa, o bölüm bunun üstüdür.
  - Kök, üst zincirinin başıdır. Üstü olmayan bölüm kendi köküdür.
- **Kayıp ağırlığı:** ölçüm penceresinde doğup açlıktaki bir düğümde rotasızlıktan düşen telemetri paketleri. Protokolün kararı "gönderme, bekletme" ise paket düşmüştür. Her paket, düştüğü düğümün açık bölümüne ve onun köküne yazılır.
  - **Kapsama:** bölümlerde düşen artı bölüm dışında düşen paketlerin R grubuna oranı.
- **Komşu sayımı:** kök bölümün başında eski ardıl dışındaki komşular iki eksende sınıflanır:
  - bağın durumu: OLAĞAN ya da değil;
  - ilanın sınıfı: `sonsuz`, `uygulanabilir`, `eski_tur` (turu FD'ninkinden küçük) ya da `pahali` (aynı tur, maliyet ≥ FD).
- **Kâhin bandı:**
  - Bağ çıkışı anında kâhinin tek deneme başarısı `p` kullanılır (i→j; sönümleme dâhil, girişim hariç, ARF tabanında; `kalibrasyon/kahin.py`).
  - `p_atlama = 1 − (1 − p)^8`.
  - Bant: ≥ 0,90 iyi · 0,50–0,90 orta · < 0,50 kötü. Kayıp anatomisinin bandıyla aynı.
- **Karar ölçüleri** (kayıp ağırlıklı, köke göre; 8 tohum ortalaması):
  - **M1 · bağ kökenli:** kökün sebebi `bag:*` olan düşüşlerin payı.
  - **M2 · yanlış alarm:** bağ kökenli düşüşlerde, kökün ardıl bağının çıkış anında kâhin bandı iyi olanların payı.
  - **M3 · tur yardım ederdi:** kökte OLAĞAN, ilanı sonlu ama uygulanamaz bir komşu olan düşüşlerin payı. Eski turlu olanlar ayrıca yazılır.
  - **M3b · yedek bağ vardı:** kökte bağı dışlanmış ama ilanı uygulanabilir bir komşu olan düşüşlerin payı.
  - **M4 · zincir:** üstü olan bölümlerde düşenlerin payı.
- **Ayrışma kuralı ve eşli fark:** ilk ölçümdeki gibi. Eşli farkın ortalaması eşiği aşar ve 8 tohumun en az 6'sında yön aynıysa "ayrışıyor".

## Karar kuralı (8 tohum; hesap `sonuc_hesap.py`)

0. **Geçerlilik.**
   - 16 koşunun hepsi kayıtta.
   - Her koşuda korunum geçerli, doğum çelişkisi 0, atfsız düşüş yok.
   - Aletin iç denetimleri geçmiş:
     - bölüm sayısı = `rota.aclik`;
     - ardıl kaybı = `rota.aclik` + `rota.zorunlu_gecis`;
     - sebebi bulunamayan açlık 0;
     - veri sebepli çıkış = `bag.veri_kotu`.
   - `vtk0` kolunda veri tetiği kapalı ve `bag.veri_kotu` = 0.
   - **Çekirdek kolu her tohumda ilk ölçümün kaydıyla birebir:** PDR, pencere PDR'si, üretilen, teslim, sayaçların tamamı, doğum evresine göre düşenler. Bu, kaydedicinin davranışa dokunmadığının kanıtı.
   - Duman koşusunda çekirdek 1003'ün kısa pencere satırı, ilk ölçümün dumanıyla birebir: pencere PDR'si 0,9457.
   - Biri tutmazsa önce sebebi aranır; tablolar o zamana kadar kullanılmaz.
1. **S1–S2 · kök (karar).**
   - **M1 ≥ 0,5 ve M2 ≥ 0,5 → bağ kökenli, yanlış alarm.** Bağ çıkış kuralları gerçekte iyi bağları düşürüyor. Sıradaki iş bağ çıkışının seçenekleri: T-2'nin eşikleri, T-3'ün veri tetiği ve cezası, Y-12'nin `d_f` bayatlığı, KÖTÜ bağın son çare olarak kullanılması.
   - **M1 ≥ 0,5 ve M2 < 0,5 → bağ kökenli, bağ gerçekten bozuluyor.** Çıkış haklı; açık, yedek rotanın yokluğunda. Sıradaki iş yedek rotanın seçenekleri:
     - FD ve tur kuralları (T-12, T-13) ve yeni turun yayılması (M3 ve tur yayılımı yön verir);
     - rotayı ∞ yapmadan önce kötü bağla sürdürmek.
   - **M1 < 0,5 → bağ kökenli değil.** En büyük kök sebep (`silindi`, üstsüz `geri_cekme`, `yoksay_doldu`) yazılır; sıradaki iş onun seçenekleri.
2. **S4 · zincir.** M4 ≥ 0,5 ise kaybın çoğu yukarıdaki düğümün ∞'undan açılan bölümlerde demektir. Bu durumda ∞'un yayılma biçimi (geri çekmenin hemen gitmesi) de seçenek listesine girer. Kök düzeldikçe zincirin de azalması beklenir; bu, düzeltmenin A/B'sinde ölçülür.
3. **S5 · veri tetiği.** `PDR(vtk0) − PDR(çekirdek)`, eşli, eşik 0,02, ayrışma kuralıyla:
   - **vtk0 önde:** veri tetiği ikizde yararından çok zarar veriyor. T-3'ün tetik kuralı seçenek listesine girer.
   - **Ayırt edilemedi:** veri tetiği ikizdeki açığın ana sebebi değil.
   - **vtk0 geride:** veri tetiği ikizde yararlı.

   Ayrıca R ve İ kayıpları ile bölüm sayısının oranı yazılır.
4. **Betimleyiciler** karar değiştirmez:
   - kapsama;
   - bölüm, kök ve zincir sayıları;
   - süre medyanı, p90, ortalama ve ≥ 2 s payı (bekletme 2 s), uzun bölümlerde düşenlerin payı;
   - eski ardılla ve yeni turla biten pay, istek dizisi başlayan pay;
   - bağ çıkışlarının sebebi, ardıl bağındakilerin sebebi, sebep başına kâhin bandı ve KÖTÜ'de kalış;
   - tur yayılımı: pencerede artış sayısı, artışlar arası medyan, sonraki artıştan önce yetişen düğüm payı, yetişme gecikmesi.
5. **Sonrası:**
   - Teşhis bir düzeltme değildir. Hüküm hangi tasarım kararına dokunuyorsa, seçenekleri artı ve eksileriyle değerlendirip kararı ben veririm (`v2/17`).
   - Düzeltme kendi beklentisiyle, mekanizma kapısının A/B'si olarak ölçülür.
   - Karıştırma katmanının A/B'leri genel açık kapandıktan sonra gelir; Y-1 o beklentiden önce kapanır.

## Öngörü

Gerekçe: Bağ, ETX_selam > 4 olunca kullanımdan çıkıyor; bu, aşağı yukarı kâhinin 0,90 bandının sınırına denk gelir. Örnek: her iki yönde selamın yarısı gidiyorsa ETX 4'tür; tek deneme başarısı ~0,25 ise sekiz denemeyle atlama başarısı ~0,90 olur. Ancak:

- 16 örneklik geçmiş gürültülüdür ve zaman aşımı her kaçan selamda hemen 0 yazar. Bu yüzden gerçek kalitesi ETX ~2,5 olan bağların da sık sık eşiği aştığını düşünüyorum.
- Veri tetiği, 8 çerçevelik pencerede yalnız ~4 çerçeveyle karar verir. Tek bir kötü anda, sekiz denemeyle iyi taşıyan bir bağı 10 s cezayla dışlayabilir.
- Babel bağı maliyeti sonlu kaldıkça tutar ve geri çekmeyi nadiren gönderir. Çekirdek ise ardılını kaybedince hemen ∞ ilan eder ve altındakileri de aç bırakır.

Bu yüzden kökün çoğunlukla bağ kaynaklı olmasını, çıkışların yarısından fazlasının yanlış alarm olmasını ve kaybın büyük kısmının zincirde düşmesini bekliyorum.

| ölçü | öngörü |
|---|---|
| **M1** bağ kökenli | 0,60–0,85 (0,72) |
| **M2** yanlış alarm | 0,45–0,75 (0,60) |
| **hüküm** | bağ kökenli, yanlış alarm (M2 sınıra yakın olabilir) |
| M3 · tur yardım ederdi (eski turlu payı) | 0,50–0,80 (0,15–0,45) |
| M3b · yedek bağ vardı | 0,20–0,50 |
| **M4** zincir | 0,50–0,75 |
| kapsama | 0,90–1,00 |
| bölüm · kök / koşu (pencerede) | 550–700 · 150–300; zincir payı (sayı) 0,55–0,75 |
| süre medyanı · p90 · ≥ 2 s payı | 0,4–1,2 s · 4–8 s · 0,15–0,35 |
| ≥ 2 s bölümlerde düşenlerin payı | ≥ 0,95 (bekletme 2 s olduğu için) |
| eski ardılla · yeni turla biten · istek başlayan | 0,40–0,70 · 0,30–0,60 · 0,60–0,90 |
| bağ çıkışı / koşu (pencerede) | 800–1100 |
| çıkış sebebi | selam (iki tür) %45–60 · veri %25–35 · `df_bayat` %5–15 · silindi < %10 |
| ardıl bağı çıkışlarında veri payı | 0,45–0,75 |
| ardıl bağı çıkışında kâhin iyi payı | 0,40–0,70; veri çıkışlarında selamınkinden yüksek |
| KÖTÜ'de kalış medyanı | veri ≥ 10 s (ceza gereği) · selam 2–8 s |
| tur artışı (pencerede) · ara medyanı | 60–80 · 2–4 s |
| sonraki artıştan önce yetişen pay · yetişme gecikmesi | 0,30–0,60 · 1–3 s |
| **S5** `PDR(vtk0) − PDR(çekirdek)` | +0,03 (−0,02 … +0,08); en olası hüküm "vtk0 önde", "ayırt edilemedi" de olası |
| vtk0'da bölüm oranı · İ kaybı farkı | 0,4–0,8 · +0,01 … +0,03 (tetik kapanınca kötü bağlar daha uzun kullanılır) |

## Duman koşusundan sonra (ölçümden önce)

- **Koşu:** `sh kosu.sh duman`, 18 Kasım 20:51–20:57. Kısa pencere, tohum 1003, iki kol birlikte. Çıktı `duman_kisa.txt`, kayıt `duman/kayit_duman.json`.
- **Kural 0 tuttu:**
  - Çekirdek 1003'ün kısa pencere satırı ilk ölçümün dumanıyla birebir: pencere PDR'si 0,9457; PDR, üretilen, teslim, sayaçların tamamı ve doğum evresine göre düşenler aynı.
  - İç denetimler iki kolda geçti.
  - `vtk0`'da veri tetiği kapalı, `bag.veri_kotu` 0.
  - Hesap uçtan uca çalıştı.
- **Kâhin ölçüsünün sağlaması:** Penceredeki bütün bağ çıkışları iyi bantta çıktığı için ham değerlere bakıldı.
  - Selam çıkışlarında kâhinin tek deneme başarısı en az 0,32 (`selam_asim`) ve 0,33 (`selam_alim`), medyanı ~0,73.
  - Aynı çıkışlarda selamla ölçülen `d_f · d_r`'nin medyanı 0,23.
  - Ölçü doğru hesaplanıyor: konumdan ve kanaldan, koşunun sırasından bağımsız. Kayıp anatomisi aleti de bantlarını aynı yoldan, koşudan sonra hesaplıyor.
- **M2'nin okunuşu** (karar kuralı değişmedi):
  - Kâhin girişimi dışarıda bırakır. "İyi" bant, bağın yol kaybı ve sönümleme bakımından iyi olduğunu söyler; yayın selamlarının çarpışma ve girişimle kaybı bu ölçüde görünmez.
  - Rotanın taşıdığı veri ise tek alıcılıdır ve sekiz denemeyle girişimi çoğunlukla aşar (ilk ölçümde İ kaybı 0,049).
  - Yanlış alarm bu anlamdadır: bağ veriyi taşıyabilirdi.
  - Dumandaki fark (kâhin ~0,73 ↔ selam ~0,23), selam kaybının büyük kısmının bağın kendi kalitesinden değil girişimden geldiğini düşündürüyor. Bu bir gözlemdir; ölçümde sınanmaz.
- **Kısa pencerenin tek tohumluk sayıları** yalnız aletin sınamasıdır; öngörüye ve karara girmez:
  - pencerede 12 bölüm, 6 kök (hepsi veri tetiği);
  - M4 0,38;
  - `vtk0`'da pencerede açlık yok.
- **Süre:** kol başına ~5 dk (kısa pencere). Ölçümün tahmini değişmedi (~2,5–3 sa).
- **Öngörüler ve karar kuralı değişmedi.**
