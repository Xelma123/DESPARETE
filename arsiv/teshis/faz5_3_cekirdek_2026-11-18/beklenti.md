# Faz 5-3 · yeni sürümün çekirdeği ↔ Babel, karıştırıcısız ikizde ve birincil hücrede — beklenti ve karar kuralı (ölçmeden önce)

> 18 Kasım 2026 · `v2/12` §1.2 (5-3: kod, birim testi, duman, mekanizma başına A/B) · kurallar `v2/kural/KK-00`…`KK-05`, kod `protokoller/desparete5*.py` · karşılaştırma tabanı teşhis (c) (`arsiv/teshis/faz5_2_rakip_cizgisi_2026-11-15/`: Babel, kâhin ve v0.4.1'in aynı tohum ve hücrelerdeki satırları). Sonuçlar ayrı `sonuc.md`ye yazılır; bu dosyaya dokunulmaz. Bu bir A/B değil, çekirdeğin ilk ölçümüdür; eşikler karar kolaylığıdır. Öngörüler duman koşusundan önce yazıldı ve commit'lendi; yeni sürüm referans dünyada henüz hiç koşmadı.

## Sorular

- **S1 · genel düzey.** Karıştırmaya karşı mekanizmaları kapalı yeni sürüm (çekirdek), karıştırıcısız ikizde en güçlü rakip Babel'e göre nerede? v0.4.1'in açığı (ikizde 0,145, büyük kısmı genel; teşhis (c)) kapandı mı?
- **S2 · başlangıç çizgisi.** Birincil hücrede çekirdeğin `PDR_açık`ı ve karıştırmaya özgü kaybı Babel'e göre nerede? Karıştırma katmanının A/B'leri bu çizginin üstüne kurulur.
- **S3 · kontrol yükü ve gecikme** (T-19). Çekirdeğin kontrol trafiğinin kanaldaki payı ve gecikmesi Babel'e ve v0.4.1'e göre nerede?
- **S4 · tanı** (`KK-00` tanı kaydı). Kayıp hangi grupta? Veri tetiği karıştırıcısız ikizde ne sıklıkta bağ düşürüyor (denetim S-1)? Açlık ve tur artışı ne sıklıkta (S-2, `17` §7 madde 10)?

## Düzen

    # adım 1 · ikiz (karıştırıcısız)
    PYTHONIOENCODING=utf-8 py -3.11 -u kalibrasyon/kayip_anatomisi.py --dunya referans_2026 \
        --kol formasyon --sinif yok --hayalet 10:20 --protokoller desparete5_cekirdek \
        --tohumlar 1003,1004,1005,1006,1007,1008,1009,1010 --isci 8 --kayit <bu dizin>/kayit_cekirdek_ikiz.json
    # adım 2 · birincil
    … --sinif surekli --protokoller desparete5_cekirdek … --kayit <bu dizin>/kayit_cekirdek_birincil.json

- **Hücreler** teşhis (c)'nin ilk ikisi (`formasyon · yere_toplama`, tam pencere: ısınma 50 · ölçüm sonu 320 · koşu 350 s; karıştırıcı 150. saniyede açılır):
  - **İ · karıştırıcısız ikiz** (`--sinif yok`); ölçü pencere PDR'si.
  - **B · birincil** (`derin_sizma`: araç, 15 s açık · 15 s sessiz; ortalama 10 W, açıkken 20 W); ölçü `PDR_açık`.
- **Kol:** `desparete5_cekirdek`, tohum 1003–1010; 2 hücre × 8 tohum = 16 koşu.
  - Açık olanlar: genel bayraklar (`veri_kotu_tetigi` · `uyarlanir_aralik` · `istege_bagli_esik` · `bekletme`) ve bayraksız çekirdek (selamdan ETX, iki eşik, silme, ara ilan, FD ve tur, açlıkta istek, uygulanamaz ilanı yok sayma, geri iz).
  - Kapalı olanlar: `karistirma_durumu` · `alici_bildirimi` · `hatirlanan_kalite`; çoğaltma yok. Bu, mekanizma kapısının "hepsi kapalı" koludur (`KK-00`). Değerler `KK-00`'ın başlangıç değerleri.
- **Karşılaştırılanlar yeniden koşulmaz:** Babel-a, kâhin ve v0.4.1'in bu tohum ve hücrelerdeki satırları teşhis (c)'nin kayıtlarından okunur (`kayit_ikiz.json` · `kayit_birincil.json` · `kayit_v041_*.json`).
  - Gerekçe: teşhis (c)'den (`ef6d5cb`) bu yana simülatörde yalnız köken defteri değişti (kayıt; davranışa girmez). Babel donmuş; kayıp anatomisi aleti, kâhin ve analiz kodu aynı. Simülasyon belirlenimli.
  - Denetim: duman koşusunda Babel 1003'ün kısa pencere satırı teşhis (c)'nin dumanıyla birebir olmalı (kural 0).
- **Alet eki** (bu commit): protokolün tanı sayacına açlıktan çıkış sayısı ve açlıkta geçen toplam süre eklendi (`rota.aclik_bitti` · `rota.aclik_sure_ms`; karara girmez). Kayıp anatomisi aleti değişmedi; yeni sürümün sayaçlarını v0.4.1'inkiler gibi topluyor.
- **Yürütme:**
  - Koşu dondurulmuş kopyadan (`kopya/`, bu beklentinin commit'iyle dosya özeti birebir: `kopya_ozet.txt`), `kosu.sh` ile iki adımda; saatler `zaman.txt`e. Yanında başka ağır iş yok.
  - Sıra: bu beklenti (öngörüler) commit'lenir → duman koşusu → duman notu bu dosyanın son bölümüne yazılır ve ikinci commit'le girer → o commit'ten dondurulmuş kopya → ölçüm.
  - Aletin gerçek koşuda sınaması: `sh kosu.sh duman` (kısa pencere, tohum 1003; çekirdek ve Babel, iki hücre; çalışma ağacından, kod bu commit'le aynı) → `duman_kisa.txt`. Ölçüm değil, hiçbir karara girmez.
  - Karar kuralının hesabı `sonuc_hesap.py` (koşudan önce yazıldı; teşhis (c)'nin kayıtlarıyla denendi, sayılarını birebir üretiyor).
- **Süre tahmini ~4 sa (±1):** ikiz ~1,5–2 sa · birincil ~2–2,5 sa (8 koşu, 8 işçi, tek dalga). Dayanak: küçük test dünyasında yeni sürüm Babel'in hızında (süre oranı 0,8–1,1); Babel'in referans dünyada koşu başına süresi ikizde 1,05–1,53 · birincilde 1,39–2,02 sa (teşhis (c)). Duman ~25 dk. Her adım 8 saatin altında.

## Tanımlar

Teşhis (c)'deki gibi:
- **`PDR_açık`:** ölçüm penceresinde karıştırıcının açık dönemlerinde doğan paketlerin teslim oranı (K-222). **Hayalet `PDR_açık`:** ikizde aynı zaman dilimlerinde (15/15) doğan paketlerin teslim oranı.
- **Eşli fark:** iki kolun aynı tohumdaki değerlerinin farkı; ortalaması ve yönü aynı olan tohum sayısı yazılır.
- **Ayrışma kuralı:** eşli farkın ortalaması eşiği aşar ve 8 tohumun en az 6'sında yön aynıysa "ayrışıyor"; değilse "8 tohumda ayırt edilemedi".
- **Karıştırmaya özgü kayıp:** `Δ_k = PDR_açık(B) − hayalet PDR_açık(İ)`, tohum başına eşli.
- **Gecikme tavanlı `PDR_açık`:** gecikmesi tavanı aşmayan teslimler; ana tavan 5 s, duyarlılık 3,5 ve 10 s (K-246). **Tavanın bedeli** = ölçü − ölçü(tavan).
- **Kayıp grupları:** R (rota yokluğu: `rota_gecersiz` · `hedef_yok` · `tampon_asimi`) · İ (iletim) · K (kuyruk) · T (ömür), hücrenin birincil ölçüsünün paydasına oranla.
- **Kontrol payı:** kontrol çerçevelerinin kanal süresi / bütün gönderimlerin kanal süresi (bütün koşu, ağ toplamı).
- **Çözünürlük:** `R` = 0,0126 (K-224).

## Karar kuralı (8 tohum)

0. **Geçerlilik.**
   - 16 koşunun hepsi kayıtta; her koşuda korunum geçerli, doğum çelişkisi 0, atfsız düşüş yok, aletin iç denetimleri geçmiş.
   - Teşhis (c)'nin Babel, kâhin ve v0.4.1 satırları 16'şar.
   - Duman koşusunda Babel 1003'ün iki hücredeki kısa pencere satırı teşhis (c)'nin dumanıyla birebir: tüm koşu PDR'si · pencere PDR'si · üretilen = 0,8109 · 0,8631 · 1597 (İ) ve 0,5842 · 0,6260 · 1597 (B). Pencerede ~1000 paket var, bir paket dördüncü basamağı değiştirir.
   - Biri tutmazsa önce sebebi aranır; Babel gerekirse yeniden koşulur ve tablolar o zamana kadar kullanılmaz.
1. **S1 · genel düzey (İ).** `G_İ = PDR(Babel) − PDR(çekirdek)`, eşli, eşik 0,02, ayrışma kuralıyla.
   - **Çekirdek geride** (`G_İ` ≥ 0,02 ve ayrışıyor): yeni sürümün genel bir açığı var. Sıradaki iş bu açığın teşhisi (kayıp grupları, atlama, kontrol payı, veri tetiğinin sayısı) ve gerekirse genel bir düzeltme, kendi beklentisiyle. Karıştırma katmanının A/B'leri ondan sonra gelir.
   - **Ayırt edilemedi** ya da **çekirdek ileride:** genel düzey Babel'le eş. Sıradaki iş karıştırma katmanı: önce `karistirma_durumu`nun A/B'si, `KK-00`'ın sınıfa göre ölçütleriyle. Y-1 o beklentiden önce kapanır.
   - Ayrıca `PDR(çekirdek) − PDR(v0.4.1)` yazılır (eşik 0,02); karar değiştirmez.
2. **S2 · başlangıç çizgisi (B).** Betimleyici; karar 1. maddededir.
   - `PDR_açık(Babel) − PDR_açık(çekirdek)` ve `PDR_açık(v0.4.1) − PDR_açık(çekirdek)`, eşli, eşik 0,02.
   - Her kolun `Δ_k`'si ve `Δ_k(çekirdek) − Δ_k(Babel)` (eşik 0,03).
   - Çekirdek B'de Babel'den ayrışarak öndeyse bu kazanç genel mekanizmalardan gelir (veri tetiği, bekletme, açlıkta istek). "Karıştırmaya özgü" denmez; iddia dili `06` §0.4.5'tedir.
3. **S3 · kontrol yükü ve gecikme (T-19).**
   - Her hücrede kontrol kanal süresi, kontrol payı, tavanın bedeli (3,5 · 5 · 10 s) ve gecikmenin p50 · p95 · p99'u.
   - Bir hücrede 5 s tavanın bedeli ≥ 0,02 ise "tavan bağlayıcı" yazılır; o hücrede gecikme tavanlı `PDR_açık` birincil ölçüyle birlikte izlenir.
4. **S4 · tanı.** Kayıp grupları, karar/paket, atlama başarısızlığı, deneme başarısı ve çekirdeğin sayaçları betimleyicidir:
   - veriyle KÖTÜ ve ASKIDA'ya giriş · selamdan KÖTÜ ve dönüş · açlık, açlıktan çıkış ve ortalama açlık süresi · tur isteği ve tur artışı · istek iletimi ve karşılanması · selam ve ara ilan · bekletme ve süresi dolan · komut kararları.

   Veriyle KÖTÜ'nün geçide uzaklığa göre dağılımı ve en uzun atlama sayısı bu adımda ölçülmez; veri tetiğinin ve bekletmenin A/B'lerine kalır.
5. **Kâhin** yalnız referanstır (K-248): kâhine oran yazılır; bir kolun kâhini bir tohumda `R`'den fazla aştığı hücreler listelenir; karar değiştirmez.

## Öngörü

Düzeyler (8 tohum ortalaması; Babel, kâhin ve v0.4.1 teşhis (c)'den biliniyor):

| kol | İ · pencere PDR | B · `PDR_açık` |
|---|---|---|
| kâhin | 0,917 | 0,779 |
| Babel | 0,930 | 0,663 |
| **çekirdek** | **0,92 ± 0,03** | **0,66 ± 0,08** |
| v0.4.1 | 0,785 | 0,567 |

S1 (güven orta):
- `G_İ` −0,02 … +0,04 → "ayırt edilemedi". Kontrol trafiğinin azalması kanaldaki çarpışmayı azaltır. Veri tetiğinin kalabalık kanalda bağ düşürmesi (S-1) bunun bir kısmını geri alabilir.
- Çekirdek − v0.4.1 İ'de +0,10 … +0,17, 8/8 tohumda.

S2 (güven düşük):
- B'de Babel − çekirdek −0,06 … +0,06 → "ayırt edilemedi".
  - Veri tetiği karıştırılan bağı birkaç başarısız çerçevede bırakır; Babel bırakmaz. Bu iletim kaybını azaltır.
  - Buna karşılık açlıkta bekletme ve 2 s'lik sınır bir rota yokluğu kaybı getirir.
- Çekirdek − v0.4.1 B'de +0,03 … +0,15, en az 6/8 tohumda.
- `Δ_k(çekirdek)` −0,22 … −0,32 (Babel −0,265); `Δ_k(çekirdek) − Δ_k(Babel)` ayırt edilemedi.

S3:
- Kontrol kanal süresi İ'de 6–20 s (Babel 68 · v0.4.1 185); kontrol payı %1–5 (Babel %14,7).
  - Dayanak: selam 9 + 2 × komşu bayt + 64 bayt ek yük, temel hızda ~1,1 ms; düğüm başına 350 s'de ~170 selam ve ~%10 ara ilan.
  - B'de kontrol kanal süresi İ'dekinin en çok 1,5 katı.
- 5 s tavanın bedeli iki hücrede de < 0,01; bekletme atlama başına en çok 2 s.
- Gecikmenin p99'u: İ'de 0,2–1,0 s (Babel 0,23) · B'de 1,0–3,0 s (Babel 1,31).

S4 (güven düşük):
- Kayıp grupları:
  - İ'de R 0,000–0,02 · İ 0,05–0,09 (Babel 0,000 · 0,070);
  - B'nin açık döneminde R 0,02–0,10 · İ 0,20–0,32 (Babel 0,000 · 0,335).
- İ'de atlama başarısızlığı %1,5–%3,5 (Babel %2,22) · karar/paket 3,0–3,9 (Babel 3,57) · deneme başarısı `g` 0,46–0,54 (Babel 0,469).
- Veriyle KÖTÜ (koşu başına, ağ toplamı): İ'de 20–300; B'de İ'dekinin en az 1,5 katı.
- Açlık: İ'de koşu başına 40'ın altında; B'de İ'dekinin en az 3 katı. B'de ortalama açlık süresi 0,5–3 s.
- Tur artışı: İ'de koşu başına ≤ 10; B'de 10–80 (açık dönem başına birkaç; `17` §7 madde 10).

Kâhin:
- İ'de çekirdek kâhini 1–5 tohumda `R`'den fazla aşar (Babel 4/8); B'de hiç aşmaz.

## Duman koşusundan sonra (ölçümden önce)

(Duman koşusundan sonra yazılır.)
