# Faz 5-2 · teşhis (d): karıştırmanın yerel işaretleri — beklenti ve karar kuralı (ölçmeden önce)

> 16 Kasım 2026 · `v2/12` §1.2, 5-2'nin teşhis ölçümü (d) · dayanak `v2/17` T-5 (kanıtın işaretleri), T-6 (kim söyler), T-10 (birkaç ardışık olay), T-1 (selam aralığının üst sınırı) · gözlem sözleşmesi `v2/05` §3, §6. Sonuçlar ayrı `sonuc.md`ye yazılır; bu dosyaya dokunulmaz. Bu bir teşhistir, hipotez testi değildir; eşikler karar kolaylığıdır. Öngörüler duman koşusunun sonucu görülmeden yazıldı.

## Sorular

- **S1 · işaretler (T-5).** Protokolün görebildiği işaretler, karıştırıcının ED ve girişim bölgesindeki düğümlerde karıştırılmayan düğümlerden ne kadar ayrışıyor? Hangileri kanıta girer?
  - **S1a** düğüm başına: kanal meşgul süresi · bunun çözülen çerçevelerle açıklanamayan kısmı · CRC hatası · çözülen çerçeve sayısı · son çözülen çerçeveden beri geçen süre · tanıdık komşulardan beklenen selamların kaçırılan payı.
  - **S1b** bağ başına: "düşük teslim + güçlü sinyal = karıştırma, düşük teslim + zayıf sinyal = kötü bağ" tutarlılığı karıştırılan bağı kötü bağdan ayırıyor mu?
- **S2 · ardışık olay (T-10).** Art arda MAC vazgeçmesi dizileri karıştırılan ve karıştırılmayan bağda ne uzunlukta? Kaç ardışık vazgeçme yanlış alarmı yeterince seyrek tutar, karıştırma başlayınca o sayıya ne kadar sürede ulaşılır?
- **S3 · bağ kalitesinin değişim hızı (T-1).** Karıştırıcısız ikizde, kullanılan bağların kalitesi ne kadar sürede belirgin değişiyor? Selam aralığının üst sınırına girdi.

## Düzen

    # adım 1 · ikiz (karıştırıcısız)
    PYTHONIOENCODING=utf-8 py -3.11 -u kalibrasyon/karistirma_isaretleri.py --dunya referans_2026 \
        --kol formasyon --sinif yok --protokoller babel \
        --tohumlar 1003,1004,1005,1006,1007,1008,1009,1010 --isci 8 --kayit <bu dizin>/kayit_ikiz.json
    # adım 2 · birincil
    … --sinif surekli --protokoller babel … --kayit <bu dizin>/kayit_birincil.json
    # adım 3 · dayanıklılık
    … --sinif surekli --protokoller babel@tehdit_acik_s=10+tehdit_sessiz_s=20 … --kayit <bu dizin>/kayit_dayaniklilik.json

- **Hücreler** teşhis (c)'deki üç hücre (hepsi `formasyon · yere_toplama`, tam pencere: ısınma 50 · ölçüm sonu 320 · koşu 350 s; karıştırıcı 150. saniyede açılır): İ karıştırıcısız ikiz · B birincil (araç, 15 s açık · 15 s sessiz, açıkken tepe 20 W) · D dayanıklılık (10 s açık · 20 s sessiz, açıkken tepe 30 W). 3 hücre × 8 tohum (1003–1010) = 24 koşu.
- **Kol: Babel-a** (donmuş, K-249). Sebep: trafik deseni yeni tasarıma en yakın kol (selamlı, kararlı rotalar); işaretlerin çoğu fiziksel, MAC sonuçları trafiğe bağlı. Babel MAC başarısızlığını kullanmadığı için karıştırılan alıcıya göndermeyi sürdürür; bu, S2'nin dizilerini kesmeden görmeyi sağlar.
- **Kaydedici** (bu commit; `kalibrasyon/karistirma_isaretleri.py`, testi `tests2/test_karistirma_isaretleri.py`). Babel'e kanca eklenmez. Simülatörün kanal meşgul integrali, CRC sayacı, alıcı zincirinin çözümü, MAC sonucu bildirimi ve Babel'in selam kurma ve alma yöntemleri bu işçi sürecinde sarılır (davranış aynı; yalnız kayıt). RSSI, `cerceve_duyuldu`nun formülüyle (kilitlenilen güç + durumsuz σ hatası) hesaplanır. Bölge ve evre etiketleri yalnız değerlendirmede kullanılır (`05` §8).
- Dondurulmuş kopyadan (`kopya/`, bu beklentinin commit'iyle dosya özeti birebir: `kopya_ozet.txt`), `kosu.sh` ile üç adımda; saatler `zaman.txt`e. Yanında başka ağır iş yok.
- Aletin gerçek koşuda sınaması `duman_kisa.txt` (kısa pencere, tohum 1003, ikiz ve birincil; ölçüm değil, hiçbir karara girmez).
- Karar kuralının hesabı `sonuc_hesap.py` (koşudan önce yazıldı; bu dizinin `kayit_*.json` dosyalarını ve birebirlik için teşhis (c)'nin kayıtlarını okur).
- **Süre tahmini ~6 sa (±1,5):** adım başına ~2 sa (8 Babel koşusu, 8 işçi). Teşhis (c)'de Babel'in koşu süresi 1,05–2,02 sa'ydi; kaydedicinin ek yükü duman koşusunda ölçülür. Her adım 8 saatin altında.

## Tanımlar

- **Düğüm-saniye:** ölçüm penceresinde (50–320 s) bir düğümün bir saniyelik dilimi. **Bağ birimi:** gönderen → alıcı, 5 s'lik dilim, en az 3 tek alıcılı çerçeve.
- **Evre** (dilimin): önce (karıştırıcı açılmadan) · açık · sessiz. İçinde açılma ya da geçiş anı olan dilim dışarıda kalır. İkizde tek sınıf "ikiz".
- **Etki alanı** (düğümün, dilimin ortasında; `kayip_anatomisi`nin tanımı): karıştırıcı açık olsaydı alınacak ortalama güç ≥ −76 dBm **ED** · ≥ gürültü tabanı **girişim** · altı **uzak**. Bağ birimleri ve MAC olayları **alıcının** alanıyla etiketlenir (SINR kaybı alıcıda).
- **Karıştırılan:** açık evrede ED ya da girişim alanı (ayrı ayrı). **Temiz:** aynı koşunun önce evresi (bütün alanlar).
- **İşaretler (S1a).**
  - `mesgul`: CCA'nın meşgul kaldığı süre / 1 s (`mesgul_sure_s`).
  - `aciklanamayan`: (meşgul süre − o dilimde çözülen çerçevelerin hava süresi) / 1 s, en az 0.
  - `phy`: CRC hatalı çerçeve sayısı (`phy_hata`).
  - `cozulen`: çözülen çerçeve sayısı (`alinan_cerceve`).
  - `sessizlik`: dilimin sonunda, son çözülen çerçeveden beri geçen süre (tavan 30 s).
  - `selam_kaybi`: son 4 s'de tanıdık komşulardan (son 16 s'de selamı duyulmuş) beklenen selamların kaçırılan payı; beklenen yoksa tanımsız ve dışarıda (payı yazılır).
- **Ayırma gücü:** `AUC` = rastgele bir karıştırılan birimin değerinin rastgele bir temiz birimden büyük olma olasılığı (eşitlik yarım). `G = max(AUC, 1 − AUC)`; yön, `AUC > 0,5` ise "+" (karıştırılanda büyük). Sabit kutulu histogramlardan hesaplanır.
- **Eşik ve yanlış alarm:** güçlü ya da zayıf bir işaretin, karıştırılanların %80'ini yakalayan en seçici eşiği; o eşikte karıştırıcısız ikizin düğüm-saniyelerinde alarm veren pay.
- **S1b:** bağ biriminde **deneme başarısı** = başarıyla giden çerçeve / toplam deneme; **RSSI** = göndericinin aynı komşudan son 10 s'de çözdüğü çerçevelerin ortalama RSSI'ı. Düşük teslim: deneme başarısı < 0,5.
- **S2:** **vazgeçme** = MAC'in bir çerçeveden bütün denemeler bitince vazgeçmesi. Bağ başına çerçeve sonuçlarının zaman sırasında art arda vazgeçme dizileri. `r_n` = uzunluğu ≥ n olan dizi sayısı / çerçeve sayısı (dizi, başladığı anın sınıfına yazılır). **Tespit süresi:** her açık dönemin başında alıcısı ED ya da girişim alanında olan, açılmadan önceki 10 s'de başarılı çerçevesi bulunan ve dönem içinde çerçeve gönderen bağda, açılmadan n'inci ardışık vazgeçmeye kadar geçen süre; dönem bitene kadar ulaşılmazsa "ulaşılmadı".
- **S3:** ikizde en çok veri kararı taşıyan bağlar (en çok 80, her biri ≥ 50 karar); kâhinin atlama başarısı (7 deneme) saniyede bir; bantlar iyi ≥ 0,90 · orta 0,50–0,90 · kötü < 0,50. τ gecikmeyle bant değişim oranı ve ortalama |Δp|.

## Karar kuralı (8 tohum)

0. **Geçerlilik.** 24 koşunun hepsi kayıtta · korunum geçerli · kaydedicinin iç denetimleri geçmiş (dilimlere yazılan meşgul süresi düğümün toplamına, kaydedilen çözüm ve CRC hatası simülatörün sayaçlarına eşit; koşu hata vermedi). **Birebirlik:** her koşunun geçerliliği, PDR'si, pencere PDR'si, üretilen ve teslim sayısı ve bütün simülatör sayaçları teşhis (c)'nin aynı hücre ve tohumdaki Babel satırına eşit (24/24). Biri tutmazsa kaydedici davranışı değiştirmiştir; sebebi bulunmadan tablolar kullanılmaz.
1. **S1a.** Her işaret ve alan (ED · girişim) için B'de ve D'de, karıştırılan ↔ temiz:
   - **güçlü:** iki hücrede de `G ≥ 0,80`, iki hücrede yön aynı ve her hücrede tohumların ≥ 6/8'inde tohum başına yön aynı;
   - **zayıf:** aynı koşullarla `0,70 ≤ G < 0,80`;
   - **dışarıda:** öteki her durum.
   - Güçlü işaret T-5'in kanıtına tek başına, zayıf işaret yalnız başka bir işaretle birlikte girer; dışarıda kalan girmez. Eşiğin değeri ve ikizdeki yanlış alarmı 5-3'ün kural kâğıdının girdisidir.
2. **S1b.** B'de ve D'de düşük teslimli birimlerde RSSI'ın AUC'si (karıştırılan alıcı ↔ temiz; yön: karıştırılanda güçlü sinyal): iki hücrede de ≥ 0,80 ve tohumların ≥ 6/8'inde > 0,5 ise tutarlılık kuralı **güçlü**; ≥ 0,70 ise **zayıf**; değilse **dışarıda**. Dışarıda kalırsa T-5'in "teslim + sinyal tutarlılığı" maddesi bu dünyada dayanak yapılmaz.
3. **S2.** `n*` = temizde (B ve D) ve ikizde `r_n ≤ 0,001` olan en küçük n (1…5). `n*` varsa ve B'de ve D'de tespit süresinin ortancası ≤ 3 s, ulaşılan pay ≥ %50 ise "n* ardışık vazgeçme tek başına yeter"; değilse "olay sayısı tek başına yetmez, T-5'in işaretleriyle birleşir". `n*` yoksa aynı hüküm. T-10'un "birkaç"ının ilk değeri `n*`dır; kesin değer 5-3'te.
4. **S3.** Bant değişim oranı ≤ %10 olan en uzun τ, selam aralığının üst sınırına (T-1) girdi olarak yazılır; karar değildir.
5. Karıştırılmayan sınıflar (açık evrede uzak alan · sessiz evre · ikiz) ile temiz arasındaki ayırma gücü, işaretlerin yalnız karıştırmaya tepki verip vermediğinin denetimidir; betimleyicidir.

## Öngörüler (duman koşusundan önce)

| # | öngörü |
|---|---|
| 1 | ED · `mesgul`: G ≥ 0,95, yön + (B ve D) |
| 2 | ED · `aciklanamayan`: G ≥ 0,90, yön + |
| 3 | ED · `cozulen`: G ≥ 0,90, yön − |
| 4 | ED · `sessizlik`: G ≥ 0,90, yön + |
| 5 | ED · `selam_kaybi`: G ≥ 0,85, yön + |
| 6 | ED · `phy`: yön −, G < 0,80 (önbelge kilitlenmediği için CRC hatası azalır) |
| 7 | girişim · `mesgul`: G < 0,70 (kanal doluluğu girişim bölgesini görmez) |
| 8 | girişim · `selam_kaybi`: G ≥ 0,75, yön + |
| 9 | girişim · `cozulen`: G ≥ 0,70, yön − |
| 10 | girişim · `phy`: yön +, G ≥ 0,65 |
| 11 | girişim · `aciklanamayan`: 0,60 ≤ G < 0,85, yön + |
| 12 | S1a hükmü: ED'de en az üç işaret güçlü; girişimde güçlü işaret en çok bir |
| 13 | D'nin G'si B'ninkinden büyük ya da eşit (tepe güç 30 W ↔ 20 W), ED ve girişimde işaretlerin çoğunda |
| 14 | açık evrede uzak alan ↔ temiz: bütün işaretlerde G < 0,65 |
| 15 | sessiz evre ↔ temiz: bütün işaretlerde G < 0,65 |
| 16 | ikiz ↔ temiz: bütün işaretlerde G < 0,60 |
| 17 | S1b: düşük teslimli birimlerde RSSI AUC'si ≥ 0,75 (B ve D) |
| 18 | S1b: düşük teslimli birimin payı karıştırılanda temizdekinin ≥ 3 katı |
| 19 | S2: temizde `r_1` %1–%5 arasında |
| 20 | S2: `n*` 2 ya da 3 |
| 21 | S2: karıştırılanda `r_3` temizdekinin ≥ 10 katı |
| 22 | S2: n = 3'te tespit süresinin ortancası ≤ 3 s, ulaşılan pay ≥ %50 (B ve D) |
| 23 | S3: τ = 4 s'de bant değişimi ≤ %5; τ = 16 s'de ≤ %10 |
| 24 | Birebirlik 24/24 |

## Duman koşusundan sonra (ölçümden önce)

Öngörüler yukarıda duman koşusundan önce yazıldığı gibi kalır. Duman (`duman_kisa.txt`; kısa pencere, tohum 1003, ikiz ve birincil):

- Kaydedici, kayıp anatomisinin aynı kısa koşularıyla birebir: iki hücrede de geçerlilik, PDR, pencere PDR'si, üretilen, teslim ve bütün simülatör sayaçları (127 · 128) eşit. Koşu içi eşitlikler (meşgul süresi, çözüm, CRC hatası) geçti.
- İlk koşuda açık dönem bulunamadı: sürekli sınıfın `gecis_anlari`'ı boş dönüyor. Evre artık dilimin başı, ortası ve sonu örneklenerek belirleniyor; açık dönem "açık" dilimlerden kuruluyor, uçları ikiye bölmeyle bulunuyor. Yeniden koşuda satır ve sınıf sayıları ilk koşuyla aynı, açık dönem bulundu.
- Aynı sebeple simülatörün `mesgul_sure_s` integrali karıştırıcının açılıp kapandığı anda bölünmüyor; parçanın durumu ortasında okunuyor. Kaydedici simülatörün aynısını yazar, yani protokolün göreceği değeri. Etkisi bir düğümün iki çerçeve olayı arasındaki süreyle sınırlı; ölçülmedi.
- Kısa pencerede "önce" evresi yok (karıştırıcı 5. saniyede açılıyor), bu yüzden S1 ve S2'nin temiz sınıfı boş; tam pencerede temiz sınıf 50–150 s. §4'teki sayılar tek tohum ve tek açık dönemdir, karar girdisi değildir.
- Kaydedicinin ek yükü, dört kısa koşu paralelken kayıp anatomisine göre %9–12. Süre tahmini değişmez: ~6 sa (±1,5).
