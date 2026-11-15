# Faz 5-2 · rakiplerin, kâhinin ve v0.4.1'in üç geliştirme hücresindeki çizgisi — beklenti ve karar kuralı (ölçmeden önce)

> 15 Kasım 2026 · `v2/12` §1.2, 5-2'nin teşhis ölçümü (c) · dayanak K-252 (hedefler en güçlü rakibe göre; iki tohumluk ölçüme dayanıyor) · K-222 (dayanıklılık hücresi) · ilk iki teşhisin sonuçları (`arsiv/teshis/faz5_2_anatomi_2026-11-14/sonuc.md` · `arsiv/teshis/faz5_2_secenek_iletim_2026-11-15/sonuc.md`). Sonuçlar ayrı `sonuc.md`ye yazılır; bu dosyaya dokunulmaz. Bu bir teşhistir, hipotez testi değildir; eşikler karar kolaylığıdır. Öngörüler duman koşusunun sonucu görülmeden yazıldı.

## Sorular

- **S1 · hedef çizgisi.** Üç rakip (AODV-k · OLSRv2-b · Babel-a) ve kâhin, 5-3'te her mekanizmanın sınanacağı üç hücrede ve sekiz geliştirme tohumunda hangi düzeyde? Her hücrede en güçlü rakip hangisi; K-252'nin "en güçlü rakip Babel" dayanağı (iki tohum, iki hücre) sekiz tohumda ve üç hücrede tutuyor mu?
- **S2 · başlangıç çizgisi.** v0.4.1 aynı tohumlarda ve hücrelerde en güçlü rakibin ne kadar gerisinde; açık hangi kayıp grubunda?
- **S3 · karıştırmaya özgü kayıp.** Her protokolün açık dönemdeki teslimi, karıştırıcısız ikizin aynı zaman dilimlerindeki teslimine göre ne kadar düşüyor? İlk teşhiste dört tohumda v0.4.1 Babel'den 0,07 daha az kaybetmişti; sekiz tohumda tutuyor mu?
- **S4 · çizelgeye duyarlılık.** Dayanıklılık hücresinde (10 s açık · 20 s sessiz) protokollerin sırası ve düzeyi birincil hücredekinden farklı mı?

## Düzen

    # adım 1 · ikiz (karıştırıcısız)
    PYTHONIOENCODING=utf-8 py -3.11 -u kalibrasyon/kayip_anatomisi.py --dunya referans_2026 \
        --kol formasyon --sinif yok --hayalet 10:20 \
        --protokoller aodv,babel,olsrv2,en_guvenilir_kahin \
        --tohumlar 1003,1004,1005,1006,1007,1008,1009,1010 --isci 8 --kayit <bu dizin>/kayit_ikiz.json
    # adım 2 · birincil
    … --sinif surekli --protokoller aodv,babel,olsrv2,en_guvenilir_kahin … --kayit <bu dizin>/kayit_birincil.json
    # adım 3 · dayanıklılık (her kolda @tehdit_acik_s=10+tehdit_sessiz_s=20)
    … --sinif surekli --protokoller "aodv@…,babel@…,olsrv2@…,en_guvenilir_kahin@…" … --kayit <bu dizin>/kayit_dayaniklilik.json
    # adım 4 · v0.4.1, ikiz
    … --sinif yok --hayalet 10:20 --protokoller desparete … --kayit <bu dizin>/kayit_v041_ikiz.json
    # adım 5 · v0.4.1, birincil ve dayanıklılık
    … --sinif surekli --protokoller "desparete,desparete@…" … --kayit <bu dizin>/kayit_v041_karistirma.json

- **Hücreler** (hepsi `formasyon · yere_toplama`, tam pencere: ısınma 50 · ölçüm sonu 320 · koşu 350 s; karıştırıcı 150. saniyede açılır):
  - **İ · karıştırıcısız ikiz** (`--sinif yok`). Birincil ölçü pencere PDR'si.
  - **B · birincil** (`derin_sizma`): araç, 15 s açık · 15 s sessiz; ortalama 10 W, açıkken tepe 20 W. Birincil ölçü `PDR_açık` (açık dönemde doğan paketlerin teslim oranı).
  - **D · dayanıklılık** (K-222): birincilin aynısı, çizelge 10 s açık · 20 s sessiz. Ailelerin eşit ortalama güç kuralı (K-186) gereği ortalama yine 10 W, açıkken tepe 30 W. Bu hücre ilk kez koşuluyor. Birincil ölçü `PDR_açık`.
- **Kollar:** AODV-k · OLSRv2-b · Babel-a (donmuş, K-249) · en güvenilir yol kâhini · DESPARETE v0.4.1. 5 kol × 3 hücre × 8 tohum (1003–1010) = 120 koşu.
- v0.4.1 planın cümlesinde yok ("rakiplerin ve kâhinin çizgisi"); açığın aynı tohumlarda ve hücrelerde ölçülmesi için eklendi. Son iki adımdır; rakiplerin çizgisi ondan önce tamamlanır.
- **Alet eki** (bu commit; `kalibrasyon/kayip_anatomisi.py`, testi `tests2/test_kayip_anatomisi.py`): ikincil metrikler kayda girer. Satırın ham kaydından, ön-kayıtlı ikincil metriğin kendi hesabıyla (`analiz.satir.donem_sayim`) çizelgenin açık ve sessiz dönemlerinde doğan paketler sayılır: doğan · teslim · gecikmesi 3,5 · 5 · 10 saniyeyi aşmayan teslim; ayrıca pencere gecikmesinin p50 · p95 · p99'u. Karıştırıcısız kolda aynı zaman dilimleri hayalet çizelgeyle okunur (15/15 ve 10/20). Simülatör ve protokoller değişmedi; alet yalnız sayar.
- Dondurulmuş kopyadan (`kopya/`, bu beklentinin commit'iyle dosya özeti birebir: `kopya_ozet.txt`), `kosu.sh` ile beş adımda; saatler `zaman.txt`e. Yanında başka ağır iş yok.
- Aletin gerçek koşuda sınaması `duman_kisa.txt` (kısa pencere, tohum 1003; ölçüm değil, hiçbir karara girmez).
- Karar kuralının hesabı `sonuc_hesap.py` (koşudan önce yazıldı; yalnız bu dizinin `kayit_*.json` dosyalarını ve geçerlilik için önceki kayıtları okur).
- **Süre tahmini ~22 sa (±3):** ikiz ~5 sa · birincil ~5,8 sa · dayanıklılık ~5,8 sa · v0.4.1 ikiz ~2,1 sa · v0.4.1 birincil ve dayanıklılık ~3,3 sa. Koşu başına süreler `v2/12` §3'ten ve ilk iki teşhisten (8 işçi): kâhin 0,6–0,9 · OLSRv2 0,8–1,1 · Babel 1,1–1,4 · v0.4.1 1,4–2,0 · AODV-k 1,8–2,2 sa. Her adım 8 saatin altında.

## Tanımlar

- **`PDR_açık`:** ölçüm penceresinde, karıştırıcının açık dönemlerinde doğan paketlerin teslim oranı (K-222). **Hayalet `PDR_açık`:** karıştırıcısız ikizde aynı zaman dilimlerinde doğan paketlerin teslim oranı.
- **Hücrenin birincil ölçüsü:** İ'de pencere PDR'si · B ve D'de `PDR_açık`. Hücre başına 8 tohumun ortalaması, ölçüt sapması ve tohum başına değerleri yazılır.
- **Eşli fark:** iki kolun aynı tohumdaki değerlerinin farkı; ortalaması ve aynı yöndeki tohum sayısı yazılır. **Ayrışma kuralı** (bu dosyanın her yerinde): eşli farkın ortalaması eşiği aşar ve 8 tohumun en az 6'sında yön aynıysa "ayrışıyor"; değilse "8 tohumda ayırt edilemedi".
- **Karıştırmaya özgü kayıp:** `Δ_k = PDR_açık(hücre) − hayalet PDR_açık(ikiz, aynı çizelge)`, tohum başına eşli (fark-içinde-farkın tek protokollük hâli; negatif = kayıp).
- **Gecikme tavanlı `PDR_açık`:** yalnız gecikmesi tavanı aşmayan teslimler sayılır (ana tavan 5 s; duyarlılık 3,5 ve 10 s; K-246). **Tavanın bedeli** `= PDR_açık − PDR_açık(5 s)`.
- **Kayıp grupları** ilk iki teşhisteki gibi (R · İ · K · T), hücrenin birincil ölçüsünün paydasına oranla (B ve D'de açık dönemde doğan paketler).
- **Kanal yükü ve deneme başarısı** ikinci teşhisteki tanımlarla (kontrol kanal süresi · toplam gönderim süresi · `g`); betimleyici.
- **Çözünürlük:** eşleştirilmiş `R` = 0,0126 (K-224).

## Karar kuralı (8 tohum)

0. **Geçerlilik.** 120 koşunun hepsi kayıtta · her koşuda korunum geçerli · doğum çelişkisi 0 · atfsız düşüş yok · aletin iç denetimleri geçmiş (koşu hata vermedi). Önceki kayıtlarla birebirlik (altı basamak):
   - İ'de Babel · kâhin · v0.4.1'in 1003–1006 pencere PDR'si ikinci teşhisin `kayit_taban.json`ıyla 12/12;
   - B'de aynı üç kolun 1003–1006 pencere PDR'si ve `PDR_açık`ı ilk teşhisin `kayit_birincil.json`ıyla 12/12;
   - B'de beş kolun 1003 · 1004 `PDR_açık`ı K-244 kuyruğunun `G2c.txt` kaydıyla 10/10;
   - İ'de beş kolun 1003 · 1004 hayalet `PDR_açık`ı (15/15) K-244 kuyruğunun `G1c.txt` ve `G2c.txt` (boş kol) kayıtlarıyla 10/10.
   Biri tutmazsa önce sebebi aranır; tablolar o zamana kadar kullanılmaz.
1. **S1 · hedef çizgisi.** Her hücrede en güçlü rakip, birincil ölçünün 8 tohum ortalaması en yüksek olan rakiptir (kâhin rakip değildir). İkinci rakiple arası ayrışma kuralıyla okunur (eşik 0,02).
   - Üç hücrede de en güçlü rakip Babel ise K-252'nin hedef cümlesi geçerli kalır; hedef çizgisi her hücrede Babel'in bu ölçümdeki değerleridir.
   - Bir hücrede başka bir rakip Babel'den ayrışarak öndeyse o hücrenin hedef çizgisi o rakiptir ve K-252 ayrı bir karar kaydıyla güncellenir.
   - İkisi ayırt edilemiyorsa ortalaması yüksek olan yazılır, ikisi birlikte anılır.
   - Bu madde hedef çizgisini verir. Yeni sürümün bu çizgiye göre ne kadar hedefleyeceği 5-2'nin çıktısındaki kararımdır; bu ölçümün kuralı değildir.
2. **S2 · v0.4.1'in açığı.** Her hücrede `G = birincil ölçü(en güçlü rakip) − birincil ölçü(v0.4.1)`, eşli; ayrışma kuralıyla (eşik 0,02) "geride" · "ileride" · "ayırt edilemedi". `G`, R ve İ gruplarına ayrılır. Bu satırlar 5-3'ün başlangıç çizgisidir.
3. **S3 · karıştırmaya özgü kayıp.** B ve D'de her kolun `Δ_k`'si yazılır. v0.4.1 ile Babel arası `Δ_k(v0.4.1) − Δ_k(Babel)` ayrışma kuralıyla okunur (eşik 0,03): pozitif ve ayrışıyorsa "karıştırmaya özgü kayıpta v0.4.1 Babel'den iyi" sekiz tohumda doğrulanmış sayılır; ayırt edilemezse ilk teşhisin bu bulgusu dört tohuma özgü kalır ve tasarımda dayanak yapılmaz.
4. **S4 · çizelgeye duyarlılık.** Her kolda `PDR_açık(D) − PDR_açık(B)` eşli; ayrışma kuralıyla (eşik 0,03) "çizelgeye duyarlı" ya da "ayırt edilemedi". Rakiplerin sırası iki hücrede karşılaştırılır. D'de en güçlü rakip değişirse 1. madde uygulanır.
5. **Gecikme tavanı.** Bir kolda bir hücrede tavanın bedelinin 8 tohum ortalaması ≥ 0,02 ise "tavan bağlayıcı" yazılır; 5-3'te o hücrede gecikme tavanlı `PDR_açık` birincil ölçüyle birlikte izlenir.
6. **Kâhin** yalnız referanstır (K-248): her kolun kâhine oranı yazılır. Bir kolun bir tohumda kâhini `R`'den fazla aştığı hücreler sayılır ve listelenir; karar değiştirmez.
7. Kayıp grupları, kanal yükü, deneme başarısı ve gecikme yüzdelikleri betimleyicidir; tasarım konularının girdisidir.

## Öngörü

Düzeyler (8 tohum ortalaması; parantez içi bildiğim tohumlar):

| kol | İ · pencere PDR | B · `PDR_açık` |
|---|---|---|
| kâhin | 0,91 ± 0,02 (1003–1006: 0,913) | 0,77 ± 0,04 (0,769) |
| Babel | 0,92 ± 0,02 (0,920) | 0,65 ± 0,06 (0,646) |
| OLSRv2 | 0,84 ± 0,04 (1003 · 1004) | 0,45 ± 0,06 (0,409 · 0,499) |
| v0.4.1 | 0,77 ± 0,03 (0,768) | 0,56 ± 0,05 (0,557) |
| AODV-k | 0,57 ± 0,06 (1003 · 1004) | 0,38 ± 0,06 (0,353 · 0,421) |

S1:
- Üç hücrede de en güçlü rakip Babel; ikinci rakip OLSRv2. Babel − OLSRv2 İ'de +0,05 … +0,11, B'de +0,12 … +0,28; ikisinde de ayrışıyor.
- Rakiplerin sırası üç hücrede aynı: Babel > OLSRv2 > AODV-k.

S2:
- İ'de `G` = +0,15 (±0,03), 8/8 tohumda v0.4.1 geride. Açığın büyüğü İ grubunda.
- B'de `G` = +0,09 (±0,04), en az 6/8 tohumda geride; açığın tamamı R grubunda (v0.4.1'in İ kaybı Babel'inkinden küçük).
- D'de `G` +0,05 … +0,15, geride.
- v0.4.1 B'de OLSRv2'nin ve AODV-k'nin önünde (eşli fark ≥ +0,05).

S3 (B hücresi):
- `Δ_k`: kâhin −0,145 (±0,04) · Babel −0,27 (±0,06) · v0.4.1 −0,20 (±0,05) · OLSRv2 −0,39 (±0,07) · AODV-k −0,19 (±0,07).
- `Δ_k(v0.4.1) − Δ_k(Babel)` +0,04 … +0,10 ve ayrışıyor (güven orta: dört tohumun birinde yön tersti).
- Karıştırmaya özgü kaybı en büyük kol OLSRv2.

S4:
- D'de `PDR_açık` beş kolda da B'dekinden düşük: açıkken güç 1,5 kat ve açık dönem protokolün toparlanmasına yetmeyecek kadar kısa. Fark kâhinde en küçük (−0,01 … −0,05), ötekilerde −0,02 … −0,10. Kâhin dışındaki kollarda en az ikisi "çizelgeye duyarlı" çıkar.
- Rakiplerin sırası değişmez.
- Sessiz dönemin PDR'si D'de B'dekinden düşük değil (toparlanmaya daha çok süre var; güven düşük).

Gecikme:
- 5 s tavanı hiçbir kolda hiçbir hücrede bağlayıcı değil. Bedeli en büyük kol v0.4.1 (0,005 … 0,02); Babel, OLSRv2 ve kâhinde 0,005'in altında.
- Pencere gecikmesinin p99'u (8 tohum ortalaması) B'de: kâhin < 1 s · Babel < 1,5 s · OLSRv2 1–2 s · AODV-k 2–4 s · v0.4.1 3,5–5,5 s.

Kâhin:
- İ'de Babel, 8 tohumun 2–5'inde kâhini `R`'den fazla aşar (ilk teşhiste 1003 ve 1006'da aşmıştı); 8 tohum ortalamasında ikisi 0,02 içinde.
- B ve D'de hiçbir kol hiçbir tohumda kâhini `R`'den fazla aşmaz.

Betimleyiciler (güven düşük):
- B'de açık dönemde doğan paketlerin kaybı: Babel'de en az %90'ı İ grubunda · v0.4.1'de R ve İ yakın · AODV-k'de R grubu İ'den büyük · OLSRv2'de R grubu İ'den büyük.
- İ'de deneme başarısı `g`: Babel > kâhin > OLSRv2 > AODV-k (Babel 0,46 · kâhin 0,44 biliniyor; OLSRv2 0,35–0,45 · AODV-k 0,25–0,40).
- İ'de kontrol kanal süresi (350 s, ağ toplamı): kâhin 20 s · Babel 69 s · v0.4.1 185 s biliniyor; OLSRv2 30–100 s · AODV-k 40–200 s.

## Duman koşusundan sonra (ölçümden önce)

Duman koşusu (`duman_kisa.txt`: kısa pencere, tohum 1003; İ'de beş kol, B'de beş kol, D'de Babel · OLSRv2 · kâhin; 13 koşu, 28 dakika) aleti ve hesap betiğini sınadı:

- 13 koşu hatasız bitti; korunum geçerli, çelişki ve atfsız düşüş yok. Çizelgeli sekiz koşuda (15/15 ve 10/20) ikincil sayım aletin evre sayımına eşit çıktı (eşit olmasaydı koşu hata verirdi).
- İ'de v0.4.1 · Babel · kâhinin kısa pencere PDR'si önceki iki teşhisin duman koşularıyla birebir (0,7730 · 0,8631 · 0,8681): alet eki davranışı değiştirmedi.
- `sonuc_hesap.py` duman kaydında baştan sona çalıştı; çıktısı `duman_kisa.txt`in sonunda.

Karar kuralı ve öngörüler değiştirilmedi. Duman tek tohum ve 30 saniyelik penceredir; sayıları ölçüm değildir, hiçbir karara girmez.
