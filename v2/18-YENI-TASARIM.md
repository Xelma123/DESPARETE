# 18 · YENİ TASARIM — DESPARETE'nin baştan, bileşen bileşen tasarımı

> 24 Kasım 2026'da başladı (`12` §1.2 madde 3b). Faz 5-3'te üç sürüm ölçüldü: 18 Kasım çekirdeği, 19 Kasım çekirdeği ve bileşenleri, 20 Kasım'ın döngü kuralları. Her biri bir sorunu çözerken başka bir sorun açtı. Öğrenilenlerle protokolü baştan, tek tek ve eksiksiz tasarlamak istiyorum; ölçüm tasarım donduktan sonra yapılır.
>
> Bu belge yöntemi, eksiksizlik listesini ve aşamaların durumunu tutar. Bileşen kararları burada (bileşen başına bir bölüm), kuralları yeni kural kâğıtlarında yazılır. `17` ve `kural/KK-*` önceki tasarımdır: yeni tasarım donana kadar bugünkü kodun ve ölçümlerin belgesi olarak kalır, sonra arşive gider.

## Durum

| aşama | durum |
|---|---|
| 1 · Zemin | 1.1 hedef ve başarı ölçütü karara bağlandı; 1.2 kısıtlar ve 1.3 kanıt envanteri yazıldı (24 Kasım); sırada 1.4 mimari iskelet |
| 2 · Bileşen bileşen tasarım | bekliyor |
| 3 · Bütünlük ve donma | bekliyor |
| 4 · Kod ve ölçüm | bekliyor |

## Yöntem

- Her bileşende aynı adımlar izlenir:
  1. sorun ve ölçülmüş kanıt;
  2. en az iki seçenek, bedelleriyle; seçilmeyenin neden seçilmediği;
  3. kararım;
  4. kural kâğıdı (aşağıdaki eksiksizlik listesine göre);
  5. sade anlatım ve onayım.
- **Ölçüm:** tasarım sırasında A/B yapılmaz. Bir kararın girdisi eksikse kısa, önceden yazılı bir teşhis ölçümü yapılabilir (geliştirme tohumları 1003–1010; ana deney tohumları kullanılmaz).
- **Sayısal değerler:** her değerin kaynağı, neyi etkilediği, küçük ve büyük olursa ne olacağı ve sonra taranıp taranmayacağı yazılır.
- **Kanıt:** tek tohumluk sınama ve duman koşusu karar girdisi değildir; ölçülmemiş bir şey bulgu diye yazılmaz.
- **Eskiler:** eski kod ve kâğıtlar silinmez; kaynak ve karşılaştırma olarak kalır. Yeni tasarım yeni belgelere yazılır.

## Aşamalar

### 1 · Zemin (henüz tasarım kararı yok)

1. **Hedef ve başarı ölçütü:** ana ölçü birincil hücrede `PDR_açık`. Yanında en kötü tohum, sessiz dönemin teslimi, gecikmenin p99'u, kontrol payı ve "ikizde zarar yok". Hepsi Babel'e ve kâhine göre, sayıyla, önceden yazılır.
2. **Kısıtlar:**
   - gözlem sözleşmesi ve protokolün okuyamadıkları (`05`, `13`);
   - paket başlığına değer yazılamaması (K-232);
   - tek kanal;
   - trafik deseni (yere toplama ve komut);
   - hücreler ve kollar (`06`).
3. **Kanıt envanteri:** Faz 5'te ölçülen her şey tek yerde, kaynağıyla; ne biliniyor, ne bilinmiyor.
4. **Mimari iskelet:** bileşenler ve aralarındaki sözleşme; kim neyi okur ve yazar, hangi kancada çalışır, olayların sırası.

### 2 · Bileşen bileşen tasarım

Sıra bileşenlerin birbirine bağımlılığına göre. Her bileşenin yanında, ilk elde dayanacağı ölçülmüş kanıt var.

1. **Komşu ve bağın ölçüsü.**
   - Selam, girişimde bağı olduğundan kötü gösteriyor: bağ çıkışı anında selamın ölçtüğü `d_f · d_r` ~0,23–0,24, kâhinin tek deneme başarısı ~0,71–0,76 (`arsiv/teshis/faz5_3_aclik_2026-11-18/sonuc.md` §6).
   - Veri tetiği kapalıyken vazgeçmelerin %41'i en kötü beş bağda; selamı geçen ama veriyi taşıyamayan kalıcı bağlar var (aynı belge §6).
   - Veri denemelerinin yarısından fazlası başarısız, denemelerin %94–96'sı en düşük hızda (`arsiv/teshis/faz5_2_secenek_iletim_2026-11-15/sonuc.md`).
2. **Karıştırma kanıtı.**
   - Teşhis (d) (`arsiv/teshis/faz5_2_isaretler_2026-11-16/sonuc.md`):
     - ED bölgesinde altı işaretin altısı güçlü;
     - girişim bölgesinde çözülen çerçeve düşüşü ve selam kaybı güçlü ama tek başına yanlış alarmı yüksek;
     - art arda üç MAC vazgeçmesi yanlış alarmı seyrek tutuyor ama geç kalıyor.
   - Kalabalığın yarattığı yanlış alarm riski (`kural/KK-03` kural 12).
   - Karıştırma katmanı bütünüyle hiç ölçülmedi.
3. **Bağın durumu, bırakma ve geri dönüş zamanı.**
   - Birincilde sessiz dönemin teslimi: eğimli kollar 0,83–0,87, uygulanabilirlik koşullu yol seçimi 0,911, Babel 0,916 (`arsiv/teshis/faz5_3_dongu_kurallari_2026-11-24/sonuc.md` §8).
   - Karıştırma bittikten sonraki toparlanma bu bileşenin sorusu.
4. **Yol seçimi ve döngü.**
   - Veri tetiği uygulanabilirlik koşuluyla birleşince açlık zinciri doğdu (açlık teşhisi).
   - Ölçülmüş takas (`arsiv/teshis/faz5_3_yeni_cekirdek_2026-11-19/sonuc.md` · `arsiv/teshis/faz5_3_dongu_kurallari_2026-11-24/sonuc.md`):
     - eğim, karıştırmasız ağda ve ikizde önde (geri gönderme yasağı ve sınırlı yükselmeyle 0,958, Babel 0,930);
     - uygulanabilirlik koşulu karıştırma altında en kötü tohumda (0,470 ↔ 0,408) ve sessiz dönemde önde, döngüsüz.
   - Geri gönderme yasağı, döngü bekçisinin iki düğümlü döngü kanıtını siliyor; tek başına zararlı.
   - Sınırlı yükselme döngüyü %68 azaltıyor ama rota yokluğunu artırıyor.
5. **Karıştırma altında iletim** (yedek, gerekirse çoğaltma ya da fırsatçı iletim).
   - Birincilde beş farklı yol seçiminin `PDR_açık` ortalaması 0,659–0,666; kayıp çoğunlukla iletimde (0,267–0,335); kâhin 0,779. Kazanılabilecek pay burada.
   - Çoğaltma yalnız son çare (`17` T-14); her pakete kopya kanalı boğuyor (K-238).
   - Fırsatçı iletim simülatörde yeni bir iletim türü ister (`protokol_kaynaklari/faz5_3_arastirma_2026-11-19/NOTLAR.md` §3).
6. **Kontrol düzlemi** (selam aralığı, ara ilan, ileti boyutları).
   - Bugünkü tasarımda kontrol payı %6, Babel %15; eğimin selamı 7 bayt + komşu başına 2 bayt.
7. **Bekletme, komutun yolu, gecikme.**
   - Bekletme 1 s ↔ 2 s ikizde ayırt edilemedi.
   - Komutun geri izi (v0.4.1'in V11'i); gecikmenin p99'u.

### 3 · Bütünlük ve donma

1. Bütün bileşenler birlikte denetlenir (aşağıdaki "Bütünlük denetimi" listesi).
2. Bağımsız denetim (17 Kasım'daki kural denetimi gibi).
3. Tasarım donar. Büyük ölçümün beklentisi (hücreler, kollar, karar kuralı) tasarımla birlikte yazılır.

### 4 · Kod ve ölçüm

1. **Kod:** yeni, temiz modüller; her kurala birim testi, uçtan uca testler, mimari denetimi.
2. **Tek büyük ölçüm:**
   - hücreler: ikiz, birincil, dayanıklılık ve yer karıştırıcılı aile;
   - kollar: tam sürüm ve her mekanizmanın ablasyonu;
   - karşılaştırma: Babel ve kâhin.
3. **Geliştirme:** sonuçtan sonra sürer.

## Zemin

### 1.1 · Hedef ve başarı ölçütü (24 Kasım, kararım)

Sayılar `arsiv/teshis/faz5_3_tasarim_zemini_2026-11-24/hedef_sayilari.py` → `hedef_sayilari.txt` (teşhis (c) ve 19–24 Kasım ölçümlerinin kayıtları; tohum 1003–1010).

**Neden bu çizgi.** Ana deneyin hükmünü bağlayıcı ön-kayıt verir (`06` §0.4, K-153 · K-222):
- birincil test H2.c, DESPARETE ↔ Babel: birincil hücrede `PDR_açık`, 40 tohum; "üstün" için ortalama fark ≥ `Δ_hedef` = 0,05 ve ≥ δ, Holm'dan sonra p < 0,05 ve mekanizma kapısı;
- "karıştırmayı çözer" iddiası için ayrıca fark-içinde-fark (birincildeki fark − ikizdeki fark) anlamlı pozitif ve mekanizma kapısı geçmiş;
- dayanıklılık hücresi (10 s açık · 20 s sessiz) ön-kayıtlı ikincil test.

Tasarım bu çizgiye göre kurulur; kurulmazsa ana deneyde "ayırt edilemedi" ya da "kazanç var, karıştırmaya bağlanamadı" hükmü çıkar.

**Bugünkü yer** (8 tohum ortalaması; ikizde pencere PDR'si, ötekilerde `PDR_açık`):

| | ikiz | birincil (15/15) | dayanıklılık (10/20) |
|---|---|---|---|
| AODV | 0,525 | 0,396 | 0,358 |
| OLSRv2 | 0,809 | 0,495 | 0,413 |
| Babel | 0,930 · en kötü 0,863 | 0,663 · en kötü 0,485 · sessiz 0,916 · p99 1,31 s · kontrol %15,0 | 0,554 · en kötü 0,411 · sessiz 0,921 · p99 0,72 s · kontrol %15,4 |
| kâhin | 0,917 | 0,779 | 0,685 |
| 19 Kasım çekirdeği | 0,954 | 0,663 · en kötü 0,314 · sessiz 0,854 · p99 1,77 s · kontrol %5,5 | ölçülmedi |
| geri+sınır (20 Kasım) | 0,958 · en kötü 0,937 | 0,659 · en kötü 0,408 · sessiz 0,863 · p99 1,24 s · kontrol %5,6 | ölçülmedi |

Birincilde kâhin Babel'in +0,116 önünde (eşli farkın tohumlar arası sapması 0,073).

**1 · Ana hedef.** Birincil hücrede `PDR_açık`'ta Babel'den en az **+0,05** önde, yani ~0,71. Geliştirme ölçümünde (8 tohum) eşli fark ≥ 0,05 ve 8 tohumun en az 6'sında aynı yön. Babel en güçlü rakip; onu bu farkla geçen tasarım AODV'yi ve OLSRv2'yi de geçer.

**2 · Karıştırmaya özgü olması için:**
- **Fark-içinde-fark:** Babel'e farkım birincilde ikizdekinden büyük. Bugün ikizde +0,028 öndeyim; birincildeki fark bunu aşmalı.
- **Mekanizma kapısı:** karıştırmaya karşı mekanizmalar birlikte kapatılınca birincilde `PDR_açık` en az 0,02 düşer (6/8 tohum).

**3 · Koruma ölçütleri** (hiçbiri bozulmaz; "kötü değil" = eşli fark eksi yönde ayrışmıyor, eşik 0,02, 8 tohumun en az 6'sı):

| ölçüt | Babel | koşul |
|---|---|---|
| ikizde teslim | 0,930 | Babel'den kötü değil; karıştırma katmanı açıkken kapalı hâlinden de kötü değil (yanlış alarm zararı yok) |
| dayanıklılık hücresinde teslim | 0,554 | Babel'den kötü değil; hedef orada da +0,05 (tasarım tek bir 15/15 çizelgesine ayarlanmasın) |
| birincilde en kötü tohum | 0,485 | Babel'inkinin en çok 0,02 altında (≥ 0,465; tek sayı olduğu için eşli fark yerine döngü kuralları ölçümündeki K3'ün biçimi) |
| birincilde sessiz dönem | 0,916 | Babel'den kötü değil (karıştırma bitince toparlanma) |
| birincilde gecikmenin p99'u | 1,31 s | Babel'inkinden büyük değil |
| kontrol payı | %15 | Babel'den düşük; bugünkü %6 korunmaya çalışılır, %10'u aşan tasarım gerekçe ister |
| yer karıştırıcılı aile | ölçülmedi | Babel'den kötü değil; büyük ölçümde Babel de orada koşulur |

**Neden +0,05:**
- +0,02 ana deneyde "ayırt edilemedi" riskini yüksek bırakır.
- Kâhine yakın bir hedef (ör. 0,75) gerçekçi değil: kâhin girişimi görmeyen, her şeyi bilen bir referans (K-248).
- +0,05 ön-kaydın kendi eşiği; kâhinin bıraktığı boşluğun içinde.

**Not:** bu ölçütler tasarımın pusulası ve büyük geliştirme ölçümünün (Aşama 4) karar kuralının çekirdeğidir. Asıl hüküm ana deneyde, 40 tohumla ve `06`'nın kurallarıyla verilir. `Δ_hedef` ve δ Faz 6'da referans dünyanın gürültüsüyle yeniden değerlendirilir (`06` §0.4.2–0.4.4).

### 1.2 · Kısıtlar (24 Kasım)

Tasarımın değiştiremeyeceği çerçeve. Kaynaklar sözleşmelerdir; burada yalnız tasarımı etkileyen kısımları toplanır. Bir kısıtı genişletmenin yolu `05` §7'dir (gerekçe, `04`te karar, önceki sonuçların geçerliliği).

**A · Protokolün görebildikleri** (`05` §3; yüzey testi 30 alan):
- **Kendi donanımı:**
  - kanal meşgul göstergesi (`kanal_mesgul_mu`) ve meşgul süre sayacı (`mesgul_sure_s`, yalnız `kanal_dolulugu_ister` diyen protokole);
  - kuyruk uzunluğu ve kapasitesi;
  - MAC'in iletim sonucu: onay · vazgeçme, kaçıncı denemede (`iletim_sonucu`, `iletim_basarisiz`);
  - bayt ve çerçeve sayaçları (`alinan_cerceve`), PHY hatası (`phy_hata`).
- **Çözdüğü her çerçeve** (`cerceve_duyuldu`): göndereni, türü, adreslendiği düğüm, veri çerçevesinde paket başlığı (kaynak, hedef, `kaynak_sira`, atlama sayısı), RSSI (tamsayı dBm, σ 2 dB).
- **Aldığı kontrol iletileri:** yalnız taşıdığı ve bedelini ödediği alanlar; bilgi gönderildiği anındır ve ileti kaybolabilir.
- **Kendi GPS/INS'i:** konum (yatay 1,5 m CEP) ve hız. Komşunun konumu ancak ödenmiş bir iletiyle gelir.
- **Kendi saati:** ofset ve sapmalı; saat senkronu yok. Tek yönlü gecikme ölçülemez, gidiş-dönüş ölçülür.

**B · Protokolün göremedikleri** (`05` §4):
- Karıştırıcının yeri, gücü, açık olup olmadığı. Gerçek topoloji, bir bağın gerçek kalitesi.
- Komşunun düştüğü; ancak sessizliğinden anlaşılır. t = 0'da kimse kimseyi bilmez; komşu yalnız selamı alınmış düğümdür.
- **Yasak alan:** `olculen_gurultu_w` karara girmez (K-227; mimari denetimi D17).
- **Henüz sınanmamış alanlar:** RSSI'nin σ'sı ve konumun dikey σ'sı kaynaksız (K-233). Protokol bunları okursa duyarlılıkları mühürden önce ölçülür.

**C · Protokolün yapabildikleri** (`13`):
- Protokol çağırmaz, niyet döndürür. Niyetler:
  - kontrol iletisi: yayın ya da tek alıcılı, isteğe bağlı titreşimle;
  - uyandırma;
  - beyan: kopma, rota kuruldu, rota geçersiz.
- `iletim_sonucu` ve `cerceve_duyuldu` niyet döndüremez; gerektirdikleri iş bir sonraki niyetli kancada yapılır.
- İleti boyutu alanların bitlerinden (`⌈Σ bit / 8⌉`) + 64 bayt kapsülleme. Kontrol iletisi veriyle aynı kanalı, MAC'i ve kayıp fiziğini paylaşır; kuyrukta önceliklidir. Yayın onaysız ve tekrarsız, tek alıcılı ileti 7 deneme.
- Düğüm başına en çok 256 bekleyen uyandırma; aşılırsa koşu durur.
- **Veri paketinin başlığına değer yazılamaz.** Yazılabilen yalnız ara düğüm adresleridir (kaynak rotası, K-232) ve başlığın bedeli. Gönderenin maliyeti gibi bilgiler ancak kontrol iletisiyle gelir.
- **Kopya:** paket birden çok komşuya eşleriyle gönderilebilir (`kopyalar`, D-23, K-231). Hedefte ilk varan eş sayılır; eşlerin bedeli veri yüküne yazılır.

**D · Dünya** (`14`):
- **Radyo ve kanal:**
  - 802.11b, 1–11 Mb/s; önbelge her zaman 1 Mb/s; hız uyarlaması ARF (güçlü karıştırmada etkisiz).
  - EIRP 20 dBm; ED eşiği −76 dBm.
  - Tek kanal; frekans değiştirme yok.
- **MAC:** 7 iletim denemesi; CW 31/1023; RTS kapalı. Paketin ömrü (TTL) 64.
- **Sürü:** 40 İHA, 33 km kare, irtifa 50–300 m, geçit düğüm 0. Birincil hücrede formasyon kolu (yavaş manevra; medyan 12 km/h).
- **Karıştırıcı:**
  - referans 10 W; birincil hücrede `derin_sizma`: yer aracı, 15 s açık · 15 s sessiz, yalnız sessizken taşınır.
  - Etkisi iki türlü: uzakta alıcıda SINR düşer, yakında ED-CCA vericiyi susturur (kanal erişim kilidi).
  - Kısmi karıştırma rejimi: sürünün tamamını karartan güçte hiçbir yönlendirme teslimi kurtaramaz (kapsam dışı).
- **Trafik:** her düğümden geçide telemetri 1 paket/s × 512 bayt (yere toplama); geçitten 4 düğüme komut 0,25 paket/s.

**E · Deney** (`06`):
- **Hücreler:**
  - karıştırıcısız ikiz;
  - birincil (`formasyon · yere_toplama · derin_sizma · sürekli`, 10 W; ölçü `PDR_açık`);
  - dayanıklılık (10 s açık · 20 s sessiz);
  - bir yer karıştırıcılı aile: aday cephe hattı (3 sabit yer karıştırıcısı) ya da hedef koruma (2 sabit); seçim Aşama 4'ün beklentisinde.
- **Tohumlar:** geliştirme 1003–1010; δ'nın türetilmesi 1100–1119; ana deney 2000–2039 mühürden önce kullanılmaz.
- **Mekanizmalar:**
  - her mekanizmanın ablasyon bayrağı vardır;
  - sınıfı (karıştırmaya karşı ya da genel) ve amacı ölçmeden önce yazılır (K-247);
  - karıştırmaya karşı olanlar mekanizma kapısına girer (`06` §0.4.5).

**F · Proje** (`01` §6, `06` §6):
- Kâhin bilgisi yok; derin öğrenme yok; parametreler mühürde sabit.
- Durum tutan her bileşende başlangıç koşulu yazılır.
- Taban protokoller donmuş.
- Tek makine.
- Jüri önünde savunulamayacak yöntem ve iddia yok.

**G · Önceki tasarımda kullanılmamış ama izinli olanlar** (tasarım alanı, karar değil):
- çerçeve başına RSSI (önceki tasarım bilerek okumadı, KK-03 kural 11);
- PHY hatası (teşhis (d)'de zayıf işaret);
- kendi konumu ve hızı;
- kuyruk uzunluğu;
- tek alıcılı kontrol iletileri (eğimde hiç yok);
- kopya;
- kaynak rotası.

### 1.3 · Kanıt envanteri (24 Kasım)

Faz 5'te ölçülenler, tarihleriyle. Hepsi referans dünyada, geliştirme tohumlarında (8 tohum, 1003–1010), birincil ve ikiz hücrede (aksi yazılmadıkça). Ayrıntı her ölçümün `sonuc.md`'sinde.

**Ölçümler:**

| tarih | ölçüm | soru | ana bulgu |
|---|---|---|---|
| 10 Ekim | 5.0 kayıp anatomisi (`faz5_0_2026-10-10`) | paket nerede, neden ölüyor | K-243'ten önceki dünyada, Faz 4'ün rakipleriyle: fazla kayıp "rota yok"ta, çoğu karıştırıcıdan uzak rölelerde |
| 14 Kasım | (a) anatomi (`faz5_2_anatomi_2026-11-14`) | v0.4.1 ↔ Babel kayıp | ikizde açık 0,15 (%65 iletim, %35 rota yokluğu); karıştırıcı açılınca Babel 0,07 daha çok kaybediyor; açık evrede açık 0,09, tamamı rota yokluğu |
| 15 Kasım | (b) seçenek-iletim (`faz5_2_secenek_iletim_2026-11-15`) | v0.4.1'in iki seçeneği; iletim kaybının sebebi | iki seçenek teslimi değiştirmiyor; veri denemelerinin yarısından fazlası başarısız, %94–96'sı en düşük hızda; fark alıcıya ulaşan çerçevenin bozulmasında, yaklaşık yarısı seçilen bağın kalitesinden |
| 16 Kasım | (c) rakip çizgisi (`faz5_2_rakip_cizgisi_2026-11-15`) | rakipler ve kâhin üç hücrede | en güçlü rakip her hücrede Babel; Babel'in karıştırmadaki fazla kaybı iletimde (sayılar §1.1) |
| 17 Kasım | (d) işaretler (`faz5_2_isaretler_2026-11-16`) | karıştırmanın yerel işaretleri (Babel-a, üç hücre) | ED bölgesinde altı işaretin altısı güçlü, açıklanamayan kanal meşguliyeti ikizde yanlış alarmsız; girişim bölgesinde çözülen çerçeve düşüşü ve selam kaybı güçlü ama tek başına yanlış alarmı yüksek; sinyal tutarlılığı zayıf; art arda üç MAC vazgeçmesi seyrek yanlış alarm, ama geç ve seyrek |
| 18 Kasım | ilk çekirdek (`faz5_3_cekirdek_2026-11-18`) | 16–18 Kasım tasarımı ↔ Babel | ikiz 0,810 (Babel 0,930), birincil 0,410 (0,663); açığın tamamı rota yokluğunda (açık dönemde R 0,512); koşu başına 822 açlık |
| 19 Kasım | açlık teşhisi (`faz5_3_aclik_2026-11-18`) | açlığın kökü | kökün %99'u veri tetiği; düşürülen ardıl bağları kâhine göre %99,7 iyi; tetik kapalıyken ikiz 0,946 |
| 20 Kasım | yeni çekirdek (`faz5_3_yeni_cekirdek_2026-11-19`) | eğim + vazgeçme tetiği ↔ Babel, üç bileşenin ablasyonu | ikiz 0,954 (8/8 Babel önünde), birincil 0,663 = Babel; üç bileşenin katkısı ayırt edilemedi; birincilde koşu başına 3620 döngü dönüşü |
| 24 Kasım | döngü kuralları (`faz5_3_dongu_kurallari_2026-11-24`) | geri gönderme yasağı, sınırlı yükselme | hiçbir kol uygulanabilirlik koşullu yol seçiminin kuyruk ve toparlanma düzeyine gelmedi; geri+sınır ikizde 0,958 (Babel'den +0,028, 8/8) |

**Biliyoruz** (ölçüldü):
1. **Bağın ölçüsü:**
   - Yayın selamı girişimde bağı olduğundan kötü gösteriyor. Bağ çıkışı anında selamın `d_f · d_r`'si ~0,23–0,24, kâhinin tek deneme başarısı ~0,71–0,76 (açlık teşhisi §6).
   - Selamı geçen ama veriyi taşıyamayan kalıcı bağlar var; tetiksiz kolda vazgeçmelerin %41'i en kötü beş bağda.
   - Veriden hızlı tetik yanlış alarm verir: 18 Kasım'ın veri tetiği iyi bağları düşürüp açlığı başlattı.
   - Vazgeçme tetiği (19 Kasım) ikizde +0,014 (6/8), birincilde −0,009; ayırt edilemedi.
2. **Karıştırma kanıtı:** teşhis (d)'nin işaretleri ve eşikleri (`kural/KK-00` değer tablosu: ED payı ≥ 0,62 ile %80 yakalama, ikizde %0,035 yanlış alarm; `MAC_ARDISIK` 3).
3. **Yol seçimi:**
   - Uygulanabilirlik koşulu (FD) döngüsüz. Veri tetiğiyle birleşince açlık zinciri doğurdu; tetik kalkınca açlık seyrek (ikizde koşu başına ~31).
   - Eğim karıştırmasız ağda önde ("önce" evresi 0,954–0,956 ↔ 0,940). Karıştırma altında döngü yapıyor: döngü son çareyle (r = 0,95) ve tavana dayanmayla (r = 0,92) birlikte artıyor.
   - Geri gönderme yasağı döngü bekçisinin iki düğümlü döngü kanıtını siliyor.
   - Sınırlı yükselme döngüyü %68 azaltıyor ama rota yokluğunu artırıyor.
   - İki ölçülü geçiş isteğe bağlı geçişi azaltmadı.
4. **Karıştırma altındaki kayıp:** birincilde beş farklı yol seçimi (Babel dâhil) 0,659–0,666; kaybın büyüğü iletimde (açık dönemde 0,267–0,335). Kâhin 0,779.
5. **Toparlanma:** sessiz dönemde FD'li yol seçimi 0,911, Babel 0,916; eğimli kollar 0,826–0,863.
6. **Kontrol yükü:** selam tabanlı tasarımımız %6, Babel %15, v0.4.1 %33.
7. **Bekletme:** 1 s ↔ 2 s ikizde ayırt edilemedi. Gecikmenin p99'u döngülü kollarda Babel'in üstünde (1,49–1,77 s ↔ 1,31 s).

**Bilmiyoruz** (ölçülmedi; tasarımda varsayım olarak işaretlenir ya da teşhis ölçümü gerekir):
1. Karıştırma katmanı (karıştırılan bağın kanıtı, alıcı bildirimi, hatırlanan kalite) hiç ölçülmedi.
2. Yeni sürümler dayanıklılık hücresinde ve yer karıştırıcılı ailede ölçülmedi; hareketli kollarda da (bağımsız, görev).
3. "Selam geçiyor, veri geçmiyor" bağlarının sebebi. Adaylar: yayının temel hızı ↔ verinin ARF hızı, çerçeve boyu, gizli düğüm.
4. Selam kaybının ne kadarının tıkanıklıktan geldiği. Kalabalığın karıştırma işaretlerinde yarattığı yanlış alarm (`kural/KK-03` kural 12) yeni trafikte ölçülmedi.
5. Bağ kalitesinin değişim hızı, tek deneme başarısıyla (`17` §7 madde 8).
6. RSSI'nin karıştırma kanıtındaki değeri: teşhis (d)'de sinyal tutarlılığı zayıftı; RSSI'nin hata modeli sınanmadı.
7. Kopyanın ya da fırsatçı iletimin bu dünyadaki bedeli. Yalnız her pakete kopya ölçüldü: JarmRout, kanalı tıkadı (K-238).
8. Döngülerin hangi evrede biriktiği (karıştırma açıkken mi, bittikten sonra mı); sessiz dönemdeki yavaş toparlanmanın kesin sebebi.

## Eksiksizlik listesi

### Her bileşen kâğıdında

Hepsi cevaplanmadan bileşen bitmiş sayılmaz.

1. **Amaç ve sınıf:** karıştırmaya karşı mı, genel mi (K-247); hangi hedefe (Aşama 1.1) hizmet ediyor.
2. **Sorun ve kanıt:** ölçülmüş kanıt, kaynağıyla; ölçülmemiş olan açıkça "varsayım".
3. **Seçenekler:** en az iki; her birinin bedeli; seçilmeyenin neden seçilmediği.
4. **Kararım ve tarihi.**
5. **Gördüğü:** gözlem sözleşmesinin hangi alanları; yasak alanların okunmadığı.
6. **Tuttuğu durum:** her alanın başlangıç değeri, ne zaman güncellendiği, ne zaman silindiği; belleğin üst sınırı.
7. **Durumlar ve geçişler:** her durum, her geçiş ve tetikleyicisi; her durumdan bir çıkış olduğu (takılı kalma yok).
8. **Kurallar:** numaralı, tek anlamlı; formüller ve birimleri.
9. **İletiler:** alanlar, bit genişlikleri, boyut; kontrol yüküne katkısı.
10. **Değerler:** her değer için birim, kaynak, neyi etkilediği, küçük ve büyük olursa ne olacağı, sonra taranıp taranmayacağı.
11. **Kenar durumlar:**
    - soğuk açılış;
    - geçit düğümünün kendisi;
    - hiç komşu yok ve tek komşu;
    - düğüm kendisi karıştırılırken;
    - sayaç taşması (modüler karşılaştırma);
    - zaman aşımı;
    - aynı anda gelen olaylar;
    - tamponun dolması.
12. **Arayüz:** öteki bileşenlerden okuduğu ve onlara yazdığı; hangi kancada çalıştığı; olayların sırası.
13. **Kapalıyken davranış:** ablasyon bayrağı ve kapalıyken ne olduğu.
14. **Etkileşimler:** öteki kurallarla çakışma ya da birbirinin kanıtını silme (döngü kurallarında görüldü: geri gönderme yasağı döngü bekçisinin kanıtını sildi).
15. **Örnek senaryo:** sayılarla, baştan sona.
16. **Sınanması:** birim testlerinin listesi; ölçümde sayılacak tanı.
17. **Kaynak:** ödünç alınan her parçanın kaynağı ve özgün olan kısım.

### Bütünlük denetiminde (Aşama 3)

1. Bütün değerler tek tabloda; bir değer iki yerde tanımlı değil.
2. Bütün iletiler ve boyutları; kontrol payının kestirimi.
3. Bütün durumların birleşimi: iki bileşenin durumları birbiriyle çelişmiyor.
4. Uçtan uca senaryolar:
   - soğuk açılış ve sakin ağ;
   - karıştırma başlıyor ve bitiyor (ED ve girişim bölgesi);
   - düğüm kopuyor ve dönüyor;
   - döngü oluşuyor;
   - geçide yakın karıştırma;
   - komutun yolu.
5. İzlenebilirlik: her hedefin hangi bileşenle, hangi kuralla, hangi testle ve hangi ölçümle karşılandığı.
6. Her ilkenin (`17` §0'ın ve yeni tasarımın ilkeleri) hangi kurallarla karşılandığı.
7. Bağımsız denetimin bulguları ve kapanışı.
