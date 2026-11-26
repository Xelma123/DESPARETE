# 18 · YENİ TASARIM — DESPARETE'nin baştan, bileşen bileşen tasarımı

> 24 Kasım 2026'da başladı (`12` §1.2 madde 3b). Faz 5-3'te üç sürüm ölçüldü: 18 Kasım çekirdeği, 19 Kasım çekirdeği ve bileşenleri, 20 Kasım'ın döngü kuralları. Her biri bir sorunu çözerken başka bir sorun açtı. Öğrenilenlerle protokolü baştan, tek tek ve eksiksiz tasarlamak istiyorum; ölçüm tasarım donduktan sonra yapılır.
>
> Bu belge yöntemi, eksiksizlik listesini ve aşamaların durumunu tutar. Bileşen kararları burada (bileşen başına bir bölüm, "Bileşenler"), kuralları yeni kural kâğıtlarında (`bilesen/`) yazılır; değerler, bayraklar ve gözlemin kullanımı tek yerde, `bilesen/00-DIZIN.md`de. `17` ve `kural/KK-*` önceki tasarımdır: yeni tasarım donana kadar bugünkü kodun ve ölçümlerin belgesi olarak kalır, sonra arşive gider.

## Durum

| aşama | durum |
|---|---|
| 1 · Zemin | tamam (24 Kasım): 1.1 hedef ve başarı ölçütü, 1.2 kısıtlar, 1.3 kanıt envanteri, 1.4 mimari iskelet |
| 2 · Bileşen bileşen tasarım | sürüyor: 2.1 B1 komşu ve bağın ölçüsü tamam (24 Kasım); 2.2 B2 karıştırma kanıtı tamam (25 Kasım: alıcı ve gönderici birlikte; kurallar teşhis ölçümüyle seçildi, kanal kilidi kuralı sonuçtan sonra karara bağlandı; kâğıt onaylandı); 2.3 B3 bağın durumu tamam (26 Kasım: teşhis ölçümüyle seçenek 2'nin dayanağı tutmadı, yeniden kararım A: bağın maliyeti selamdan, eşikle düşürme yok, veri yalnız güvenlik ağı; karıştırılan bağ son çare; kâğıt onaylandı); sırada 2.4 B4 yol |
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
   - Selam eşiğiyle düşen bağlar kâhine göre iyi: tek deneme başarısı ~0,71–0,76 (kâhin ağın kendi trafiğinden gelen çarpışmayı saymaz). Selamın o andaki `d_f · d_r`'si ~0,23–0,24; eşik (ETX 4) gereği 0,25'in hemen altında (`arsiv/teshis/faz5_3_aclik_2026-11-18/sonuc.md` §6; okunuşu §2.1'de).
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
   - Selam eşiğiyle düşen bağlar kâhine göre iyi: tek deneme başarısı ~0,71–0,76; kâhin ağın kendi trafiğinden gelen çarpışmayı saymaz. Selamın o andaki `d_f · d_r`'si ~0,23–0,24; eşik (ETX 4) gereği 0,25'in hemen altında, tek başına bilgi taşımaz (açlık teşhisi §6; okunuşu §2.1'de, 24 Kasım).
   - Alıcının çözdüğü veri çerçevelerinin onayı %94–96 geri geliyor: tek denemede kaybolan onay denemelerin %1,7–2,1'i (seçenek-iletim teşhisi §5).
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

### 1.4 · Mimari iskelet (24 Kasım, kararım)

Bileşenlerin ne olduğu, neyin sahibi oldukları ve birbirleriyle nasıl konuştukları. Bileşenlerin içi Aşama 2'de tasarlanır; iskelet onların arasındaki sözleşmedir. Gerekçe: Faz 5-3'teki sürümlerde bileşenler birbirinin durumuna doğrudan bakıyordu ve kimin neyin sahibi olduğu yazılı değildi. Bir kuralın başka bir kuralın kanıtını silmesi (geri gönderme yasağı ↔ döngü bekçisi) böyle görünmeden kaldı.

**Üç yapı kararım** ve seçilmeyen seçenekler:
1. **Tek yönlü akış; gözlemler sahibine gider** (sözleşme 1–2). Seçilmeyen: bileşenlerin birbirinin durumuna doğrudan bakması ve yazması (önceki tasarım). Bir kanıtın kaybolmasını görünmez bırakıyordu. Bedeli: biraz daha fazla yazı ve kod.
2. **Karıştırmaya karşı mekanizmalar ayrı bir katman, tek bayrak grubuyla kapanır** (sözleşme 7). Seçilmeyen: karıştırma mantığının bağın durumuna ve rotaya dağılması. Mekanizma kapısı ölçümünü bulandırır, "karıştırmaya özgü kazanç" iddiasını zayıflatır. Bedeli: karıştırma mantığı ayrı tutulmak zorunda.
3. **Rota durumu ile paket kararı ayrı** (sözleşme 5). Seçilmeyen: tek ardıl, her paket ardıla. Paket başına sapma (getirene geri göndermemek, karıştırma altında yedekten göndermek) rotayı bozuyordu. Bedeli: B4 ile B5 arasındaki sözleşme dikkatle yazılır.

**Bileşenler** (aşağıdan yukarıya; numaralar Aşama 2'nin sırası):

| # | bileşen | sorusu | sahibi olduğu durum | öteki bileşenlere verdiği | sınıf |
|---|---|---|---|---|---|
| B1 | komşu ve bağın ölçüsü | komşu kim; bağ iki yönde ne kadar iyi; veri taşıyor mu | komşu tablosu: selam geçmişi, iki yöndeki oran, veri sonuçlarının geçmişi, son duyulma | komşu kümesi; bağ başına ölçüler (selamdan, veriden) ve tazelikleri | genel |
| B2 | karıştırma kanıtı | ben karıştırılıyor muyum; hangi komşuyla bağım karıştırılıyor | saniyelik işaretler (kanal meşgul payı, çözülen çerçeve, selam kaybı, MAC vazgeçmesi), kendi durumum, komşuların bildirdiği durum | kendi durumum (yok · girişim · kanal kilidi); bağ başına karıştırma işareti | karıştırmaya karşı |
| B3 | bağın durumu | bağ kullanılır mı; ne zaman bırakılır, ne zaman döner | bağ başına durum ve süreleri; hatırlanan kalite | bağ başına durum, maliyet (tek kaynak) ve işaretler | genel çekirdek + karıştırma eki |
| B4 | yol | geçide hangi komşular üzerinden gidilir; maliyetim ne; döngü nasıl önlenir ya da yakalanır | komşuların ilanları; ardıl ve sıralı aday listesi (her adayın türü: döngüsüz yedek, son çare…); kendi maliyetim; döngü kaydı | aday listesi; kendi maliyetim; ilan olayları | genel |
| B5 | iletim kararı | bu paket hangi komşuya, şimdi mi, kopyalı mı | paket başına kayıtlar (getiren, gönderilen, denemeler) | simülatöre karar: sonraki atlama, bekletme, kopyalar | genel çekirdek + karıştırma eki |
| B6 | kontrol iletileri | hangi ileti, ne zaman, kime | ileti sırası, aralık, plan | simülatöre kontrol iletileri ve uyandırmalar | genel |
| B7 | bekletme ve komut | yol yokken paket ne kadar tutulur; komut hangi yoldan iner | tampon kayıtları; geri iz | B5'e bekletme kararı; komutun sonraki atlaması | genel |

**Sözleşme:**
1. **Tek yönlü akış.** Her bileşen yalnız kendinden aşağıdakilerin çıktılarını okur; hiçbir bileşen başkasının durumuna yazmaz.
2. **Gözlemler sahibine gider.** Simülatörden gelen her gözlem, o bilginin sahibi olan bileşene dağıtılır:
   - MAC sonucu B1'e ve B2'ye;
   - komşunun ilanı B4'e;
   - "paket daha büyük atlama sayısıyla geri döndü" B4'e (döngü kanıtı);
   - paketi getiren komşu B4'e ve B7'ye.

   Yukarıdaki bir bileşenin kararı aşağıdakine ancak böyle, bir sonraki gözlem olarak yansır.
3. **Tek kaynak.** Her büyüklük tek bileşende hesaplanır: bağın maliyeti B3'te, kendi maliyetim B4'te, karıştırma işareti B2'de. Öteki bileşenler okur, yeniden hesaplamaz. Her değer de tek yerde tanımlanır.
4. **Kanıtı silmeme.** Bir bileşenin kararı başka bir bileşenin kullandığı gözlemi ortadan kaldırıyorsa (ör. paket getirene gönderilmeyince döngünün dönüş kanıtı oluşmaz), bu etkileşim iki bileşenin kâğıdında da yazılır ve kanıtın yerine geçen şey tanımlanır (eksiksizlik listesi madde 14).
5. **Rota durumu ile paket kararı ayrı.** B4 sıralı bir aday listesi tutar; paketin yönünü B5 seçer. Paket başına bir sapma (ör. getiren komşuya geri göndermemek) rota durumunu değiştirmez. Rota durumunu değiştirecek bir kanıt varsa B4'e gözlem olarak gider.
6. **Kontrol iletileri tek yerde.** İletilerin biçimi ve gönderimi B6'dadır. Öteki bileşenler B6'ya yalnız taşınacak değerleri ve "hemen gönder" olaylarını verir.
7. **Ablasyon.** Her mekanizmanın bayrağı ve "kapalıyken" davranışı yazılır. Karıştırmaya karşı olanlar (B2'nin tamamı, B3 ve B5'in karıştırma ekleri) tek bir bayrak grubuyla birlikte kapanabilir. Kapalıyken kalan protokol eksiksiz çalışır; mekanizma kapısı bunu ister (`06` §0.4.5).
8. **Bellek sınırı.** Her tablonun üst sınırı ve silme kuralı yazılır (komşu, paket kayıtları, tampon, iz).

**Olay sırası** (her niyetli kancada aynı):
1. Gözlemi sahibine dağıt.
2. Zaman olayları: zaman aşımları, süre dolumları.
3. B2 → B3 → B4: kanıt, bağın durumu, yol.
4. B5: paket varsa kararı (B7'ye danışarak).
5. B6: değişim olaylarından doğan ve planlı kontrol iletileri.
6. B7: tampon için uyandırma.
7. Beyanlar: kopma, rota kuruldu.

Niyet döndüremeyen kancalarda (`iletim_sonucu`, `cerceve_duyuldu`) yalnız 1. adım yapılır; gerisi bir sonraki niyetli kancada.

**Kancalar ve gözlemleri:**

| kanca | dağıtılan gözlem | sonra |
|---|---|---|
| saniyelik zamanlayıcı | B2: kanal meşgul süresi, çözülen çerçeve sayısı, selam kaybı | 2–7 |
| uyandırma | B6: selam zamanı · B7: tampon · zaman olayları | 2–7 |
| kontrol iletisi alındı | B1: selamın sırası ve oranları · B2: komşunun durumu · B4: ilanı | 2–7 |
| iletim sonucu (niyetsiz) | B1: veri sonucu · B2: MAC vazgeçmesi | — |
| iletim başarısız | — | 2–7 |
| çerçeve duyuldu (niyetsiz) | B1: komşu hâlâ orada · B4: paketi getiren, bayat bilgi · B7: geri iz | — |
| sonraki atlama | B4: döngü kanıtı | 2–7, B5'in kararı |

**Karıştırma katmanı kapalıyken çekirdek:** B1, B3'ün çekirdeği, B4, B5'in çekirdeği, B6, B7. Çekirdek kendi başına eksiksiz bir yönlendirme protokolüdür; ikizde zarar olmadığını ve kapı ölçümünü bu kol verir.

## Bileşenler

Her bileşenin sorunu, kanıtı, seçenekleri ve kararım burada; kuralları `bilesen/` altındaki kâğıdında, değerleri `bilesen/00-DIZIN.md`de.

### 2.1 · B1 · Komşu ve bağın ölçüsü (24 Kasım, kararım)

Kâğıt: `bilesen/B1-KOMSU-VE-BAG.md` (onaylandı, 24 Kasım). Kâğıttaki yapı kararları: ölçü hiç donmaz, her örnek zamanıyla tutulur ve yukarıdaki bileşen sayılmayacak aralıkları söyler (kural 10); onay çerçevesi yalnız kendi çerçeveme yanıtsa varlık kanıtıdır (kural 2); geri almanın ve yeniden başlamanın sınırı 64 selam (kural 4); kendi karıştırılmamda komşu silme durmaz (§11).

**Sorun.** Önceki tasarımda bağın iyiliği yalnız yayın selamıyla ölçülüyordu. Yol seçiminin bilmesi gereken ise bir veri paketinin o bağda kaça mal olduğudur. Selam bunu üç yerden farklı ölçer (simülatörün kodu: `sim2/kanal/cerceve.py`, `sim2/kosum/kontrol.py`, `sim2/yapilandirma/konfig.py`):
- **boy:** selam ~100 bayt (15 komşuyla 101), veri 512 bayt;
- **deneme:** selam bir kez ve onaysız gider; veri en çok 7 kez denenir;
- **ters yön:** selamda ters yönü komşunun yayın selamı ölçer, veride ters yön 14 baytlık onaydır.

Hız farkı küçüktür: selam temel hızda (1 Mb/s) gider, veri denemelerinin de %94–96'sı 1 Mb/s'de.

**Kanıt** (ölçüldü):
- Selam eşiğiyle düşen bağlar kâhine göre iyi: tek deneme başarısı 0,71–0,76. Kâhin ağın kendi trafiğinden gelen çarpışmayı saymaz; selam ise çarpışmalar dâhil iki yönü tek denemeyle ölçer. Selamın o andaki `d_f · d_r`'si (~0,23–0,24) eşik (ETX 4) gereği 0,25'in hemen altındadır, tek başına bilgi taşımaz. Veri tetiği kapalı kolda kalan açlıkların kökü bu çıkışlar: 1005'te 155 bölüm, hepsi selam eşiğinden (`arsiv/teshis/faz5_3_aclik_2026-11-18/sonuc.md` §6).
- Selamı geçen ama veriyi taşıyamayan kalıcı bağlar var: tetik kapalıyken vazgeçmelerin %41'i en kötü beş bağda ve bu bağlar kâhine göre iyi bantta (aynı belge §6). Sebebi ölçülmedi; en güçlü aday boy farkı (varsayım).
- Ters yön: alıcının çözdüğü veri çerçevelerinin onayı %94–96 geri geliyor (`arsiv/teshis/faz5_2_secenek_iletim_2026-11-15/sonuc.md` §5). ETX'in ters yön terimi bu onayı temsil eder; selamdan ölçülen ters yön onu olduğundan kötü gösterebilir (varsayım, ölçülmedi).
- Açığı ölçünün üstüne eklenen tetiklerle kapatma denemeleri: 18 Kasım'ın veri tetiği attığı bağların %99,7'si iyiydi ve açlık doğurdu (açlık teşhisi); 19 Kasım'ın vazgeçme tetiği ayırt edilemedi (ikizde +0,014, birincilde −0,009) ve iki hücrede ters yönde çalıştı (`arsiv/teshis/faz5_3_yeni_cekirdek_2026-11-19/sonuc.md` §5, §9).
- Babel yalnız selamla ölçüyor; birincilde başarısız iletimlerinin %20'si kâhinin kötü dediği bağda (`arsiv/teshis/faz5_2_anatomi_2026-11-14/sonuc.md` §5).
- Kanal kalabalık: ikizde veri denemelerinin yarısından fazlası başarısız; tek deneme başarısı Babel'de ve 19–24 Kasım sürümlerimizde 0,46–0,49 (seçenek-iletim teşhisi §2, yeni çekirdek §6).

Kök: ölçü verinin kendi bedelini ölçmüyordu.

**Seçenekler:**

| | ne ölçülür | artı | eksi ve bedel |
|---|---|---|---|
| 1 · yalnız selam, veriden yalnız vazgeçme sayımı (önceki tasarım) | bağ kalitesi selamdan; veriden "gitti mi, vazgeçildi mi" | ölçüldü, basit; Babel'in yolu | kanıtlanmış iki yanılgı kalır; veri kanıtı ancak paket kaybolunca ve kaba gelir |
| **2 · selam ve verinin kendi ölçüsü** | selam iki yönde ayrı ayrı; her veri gönderiminin kaçıncı denemede geçtiği ya da vazgeçildiği; varlık için duyulan çerçeveler | kullanılan bağın bedeli doğrudan ölçülür; ek ileti yok; kullanılmayan bağlar selamla bilinmeye devam eder | kullanılan ve kullanılmayan bağ farklı kaynakla ölçülür; veri ölçüsü kanal yüküyle oynar; daha çok kayıt |
| 3 · selamı veriye benzetmek (veri boyunda yoklama) | kullanılmayan bağlar da veri boyunda ölçülür | ölçü verinin boyunda | selam ~4,3 kat uzar (1 Mb/s'de önbelge dâhil ~1,0 → ~4,3 ms); kaba kestirimle kontrol payı %6'dan ~%21'e çıkar (ikizde selamın kanal süresi 21,3 s, yeni çekirdek §4); hâlâ yayın: 7 deneme ve onay yok |

Önceden elenenler: yalnız veriden ölçmek (`17` T-1: kullanılmayan yedekler bilinmiyordu; v0.4.1'de koşu başına 15 171 komşu silinmesi, Babel'de 315) · RSSI (kaybın büyüğü çarpışma ve RSSI onu göstermez; karıştırmada fark ~2 dB, ölçüm hatası düzeyinde, teşhis (d) §6; okunursa ölçüm hatasının duyarlılığı mühürden önce ölçülür, K-233).

**Kararım: seçenek 2.** B1 selamın ölçüsünü (iki yön ayrı) ve verinin kendi ölçüsünü ham ve aynı birimde (beklenen deneme sayısı), örnek sayıları ve tazelikleriyle verir; karar vermez.
- Sorunun kökünü tetik eklemeden çözer.
- Ek ileti ve kontrol yükü getirmez: MAC'in sonucu zaten gelir (`13` §02.5, K-151).
- Ölçülerin birleştirilmesini ve kullanımını bütün bilgiyle B3'e bırakır.

Seçilmeyenler: 1, kanıtlanmış iki yanılgıyı bıraktığı için; 3, kontrol payını Babel'in (%15) ve hedefin %10 sınırının (§1.1) üstüne çıkardığı ve yine de verinin denemesini ve onayını ölçmediği için.

**B3'e kalan riskler:** veri ölçüsü kanal yüküyle oynar; maliyete girerse rotalar salınabilir (`17` T-4). Kullanılan bağ veriyle, kullanılmayan bağ selamla ölçülür. İki ölçünün aynı bağda ne kadar ayrıştığı B3'ün kararından önce kısa bir teşhis ölçümüyle sınanabilir.

### 2.2 · B2 · Karıştırma kanıtı (24 Kasım, kararım)

Kâğıt: `bilesen/B2-KARISTIRMA-KANITI.md` (onaylandı, 25 Kasım); teşhis ölçümü `arsiv/teshis/faz5_3_b2_isaretler_2026-11-24/`. Kâğıttaki yapı kararları: kendi durumum iki kuralın birleşimi, kanal kilidi öncelikli (kural 7); kendi aralıklarımın başlangıcı geriye dönük, işaretli ilk saniyeden (kural 8); bit, durum "yok" değilken 1 (kural 9); göndericinin kanıtı art arda 3 tam denemeli çerçeve (art arda 3 vazgeçmeyi kapsar), kendi aralığıma düşen olay geçersiz (kural 12–13); sessizlik kuralı yok (§2); B2 kanıt verir, bağın durumu ve süreleri B3'ün (§11); kendi durumun üst süresi yok (§4); c̄'nin dışlama eşiği ölçüldüğü gibi 0,62 (`bilesen/00-DIZIN.md`); cephe hattı kapsam sınırı (§15).

**Sorun.** B2 iki soruyu cevaplar: "ben karıştırılıyor muyum" (yok · girişim · kanal kilidi) ve "hangi komşumla bağım karıştırılıyor". Karar vermez: bağı bırakmak B3'ün, yolu değiştirmek B4'ün işidir. Karıştırıcının çevresinde iki bölge vardır:
- **kanal kilidi** (ED, karıştırıcıya çok yakın): düğüm kanalı hep dolu görür, ne gönderebilir ne duyabilir; birincilde açık dönemde ortalama 0,9 düğüm;
- **girişim** (daha uzak): düğüm gönderebilir ama duyamaz, bozulan alıcı tarafıdır; ortalama 6,8 düğüm, dayanıklılıkta 10,3.

Temel güçlük: bilgi alıcıda, karar göndericidedir. Karıştırılan düğüm durumu kendi alımının çökmesinden anlar; ona paket gönderen komşu ise ancak paketleri boşa gidince fark eder.

**Neden şart:**
- Birincilde ortalamayı yol seçimi belirlemiyor (beş farklı yol seçimi 0,659–0,666); kaybın büyüğü karıştırılan bağda, iletimde (açık dönemde 0,267–0,335; `arsiv/teshis/faz5_3_dongu_kurallari_2026-11-24/sonuc.md` §8). Kâhin karıştırılan bağları bildiği için 0,779'a çıkıyor.
- Ön-kayda göre karıştırmaya karşı mekanizma yoksa "üstün" hükmü verilemez (`06` §0.4.2, §0.4.5).

**Kanıt** (teşhis (d), Babel'in trafiğinde, 8 tohum; `arsiv/teshis/faz5_2_isaretler_2026-11-16/sonuc.md`):
- Kanal kilidi kendini tek saniyede tanır: kanal meşgul payı ≥ 0,62 karıştırılanların %80'ini yakalıyor, ikizde yanlış alarm %0,035. Ama gönderemediği için söyleyemez.
- Girişimde tek işaret yetmiyor: çözülen çerçeve düşüşü (49 ↔ 99/s) ve selam kaybı (0,69 ↔ 0,44) güçlü; ama karıştırılanların yarısını yakalayan eşikte ikizde düğüm-saniyelerin %10,5'inde ve %5,9'unda yanlış alarm. Birleşik kural hiç ölçülmedi (kayıt yalnız işaret başına dağılım tutuyordu).
- Yanıltıcı işaretler: girişimde kanal meşguliyeti düşer (0,20 ↔ 0,31); çözülen çerçeve uzak alanda da düşer (76 ve 68 ↔ 99/s).
- Göndericinin gördüğü: karıştırılan alıcıya giden veri çerçevesi ortalama 6,3 (kanal kilidi) ve 3,9 (girişim) deneme harcıyor, temizde 2,0. "Art arda 3 vazgeçme" ise geç ve seyrek: birincilde ortanca 5,6 s, karıştırılan bağların yalnız %18'inde açık dönem içinde ulaşılıyor.
- Komşunun sessizliğinden tanımak yavaş: bugünkü selam aralığıyla üç kaçan selam, karıştırma başladıktan 5,5–7,7 s sonra (iyi bağda); `d_r` 0,6 olan bağda 12–14 s (önceki KK-00).
- RSSI zayıf (AUC 0,71). Kanal doluluğu tepkisel karıştırıcıyı görmez (Puñal 2014).
- Yanlış alarmın bedeli ağır: 18 Kasım'ın veri tetiği iyi bağları bırakıp açlık doğurdu. Yalancı bir "karıştırılıyorum" bütün komşulara o düğümü bıraktırır.
- Kalabalık: temizde bile selam kaybı 0,44 (önceki KK-03 kural 12'nin riski).
- Hiç ölçülmeyen: karıştırma katmanının bütünü; işaretlerin bizim trafiğimizdeki (0,5–2 s'de bir selam, kontrol payı %6) düzeyi.

**Seçenekler:**

| | kanıtı kim toplar | artı | eksi ve bedel |
|---|---|---|---|
| **A · alıcı ve gönderici birlikte** | alıcı kendi durumunu kendi işaretlerinden belirler, selamında bir bitle bildirir; gönderici bağ başına kendi kanıtını toplar (deneme sayısı ve vazgeçme, B1'in veri kaydından; komşunun sessizliği) | bilgi doğduğu yerden, en hızlı yoldan gelir; kullanılmayan yedeklerin durumu da bilinir; bedeli selamda 1 bit | alıcının girişim kuralı ölçülmedi; yanlış alarmı bütün komşulara yayılır |
| B · yalnız gönderici | bit yok; gönderici yalnız kendi MAC sonuçlarından ve komşunun sessizliğinden; düğümün kendi durumu yalnız kendi MAC sonuçlarını yorumlamak için | yanlış alarm komşulara yayılmaz; daha basit | paket harcayarak ve yalnız kullandığı bağ için öğrenir; yedeğin durumu deneyerek bulunur |
| C · A + bölge hafızası | A'ya ek: bildirimler bölge olarak birleşir ya da sık karıştırılan bağdan bir süre kaçınılır (JAM, IAMP, Tague; `12`'de fikir olarak duran bölge risk skoru) | çizelgeli karıştırıcıda bir sonraki açık dönemden önceden kaçınabilir | İlke 3'e ters (kanıt kalkınca geri al); sessiz dönemde de kaçınırsa toparlanma düşer; en karmaşığı |
| D · açık kanıt yok | karıştırmaya yalnız genel ölçüler (B1) karşılık verir | en basiti | ön-kayda göre "üstün" hükmü verilemez; protokolün kimliğine (`17`) ters; elendi |

**Kararım: A.**
- Bilgi alıcıda doğuyor; girişimdeki düğüm gönderebildiği için bitini hemen yayabilir.
- Kullanılmayan yedeklerin karıştırıldığı da bilinir; ardıl bırakılınca doğrudan temiz bir yedeğe geçilir. Kâhinin kazancı da bu dolaşmadan gelir.
- A'nın gönderici tarafı B'nin kendisidir: bitin bayrağı kapatılınca A, B olur. Bitin katkısı Aşama 4'ün büyük ölçümünde ablasyonla ölçülür.

Seçilmeyenler: B güvenli ama yavaş ve kör; C İlke 3'e ters ve sessiz dönem bir koruma ölçütü (§1.1); A ölçüldükten sonra ek olarak düşünülebilir.

**Kuralların seçimi ölçümle.** A'nın en riskli parçası alıcının girişim kuralıdır. Kural ve eşikler tahminle değil, önceden yazılı bir teşhis ölçümüyle seçilir (yöntem: girdi eksikse kısa teşhis). Sorular, karar kuralı ve öngörüler `arsiv/teshis/faz5_3_b2_isaretler_2026-11-24/beklenti.md`de; B2'nin kâğıdı sonucuna göre yazılır.

**Teşhisin sonucu** (25 Kasım, `arsiv/teshis/faz5_3_b2_isaretler_2026-11-24/sonuc.md`; çekirdeğimizin trafiği, dört hücre, 32 koşu):
- **Girişim kuralı var** (K2): G(α 0,4 · β 0,6 · giriş 2 s · çıkış 1 s), yani çözülen çerçeve kendi ortalamasının %40'ının altında ve selam kaybı ≥ 0,6, iki saniye üst üste. Doğrulama yarısında ikizde yanlış alarm %0,002; karıştırılan düğümlerin %34–35'i 3 s içinde, %53–55'i dönem içinde yakalanıyor.
- **Kanal kilidi kuralı tutmaz** (K1, önceden yazılı birimle). Kuraldan sonra görülen: yer–hava görüş hattı aynı dönem içinde açılıp kapandığı için düğümler kanal kilidine dönemin ortasında giriyor. Girişten itibaren kural (m ≥ 0,55) %90–95'ini 3 s içinde, ortanca 1 s'de yakalıyor.
- **Göndericinin bağ kanıtı tanımıyor** (K3, K4): en iyileri art arda 3 vazgeçme ve art arda 3 tam denemeli çerçeve; yanlış alarmları düşük, ama 3 s içinde E alanında %27–35, G alanında %18–21 yakalıyorlar.
- **Yük koruması gerekmiyor** (K5). Girişimdeki düğümün selamlarının uzak komşulara ulaşma payı 0,35 (K6). Girişim kuralı cephe hattında düşüyor (K7); orada G alanı görüş hattıyla titriyor.

**Kanal kilidi kuralı** (25 Kasım, kararım). K1'in hükmü önceden yazılı birimle "tutmaz"; beklentinin bu hükme yazdığı sonuç "kanal kilidi için başka işaret aranır". Kuraldan sonra ölçülen: K1'in birimi gecikmeyi dönem başından sayıyor ve yer–hava görüş hattı yüzünden E birimlerinin yarısından fazlası alana dönemin 3. saniyesinden sonra giriyor. Bu birimle ulaşılabilecek en yüksek erken yakalama doğrulamada 0,463, kuralınki de 0,463 (`ek_hesap.txt` E8).

| | ne | bedel |
|---|---|---|
| **1 · kuralı kullanmak, dayanağın sonuçtan sonra olduğunu açıkça yazmak** | `m` ≥ 0,55; dayanak alana girişten ölçü (E7), tavan (E8) ve teşhis (d); `06` §10'a kayıt | dayanağın bir kısmı sonuç görüldükten sonra kuruldu |
| 2 · önceden yazılı sonuca uymak: başka işaret (çözülen çerçeve, CRC hatası) | kayıtlar elde, yeni koşu gerekmez | hesap yine sonuçtan sonra; aynı birimle aynı tavana takılır |
| 3 · kanal kilidi durumunu kaldırmak | kendi durumum yalnız yok · girişim | kilitli düğüm daha geç ve daha az tanınır (girişim kuralı E alanında 3 s içinde 0,40–0,49; teşhis §8.2); hariç aralık zayıflar |

Kararım: 1. Hüküm işaretin zayıflığından değil, birimin tanımından geliyor; 2 aynı yere varır, 3 iyi çalışan bir işareti atar. Kuralın katkısı Aşama 4'te ablasyonla ölçülür (`bilesen/B2-KARISTIRMA-KANITI.md` §15).

### 2.3 · B3 · Bağın durumu (25–26 Kasım, kararım)

Kâğıt: `bilesen/B3-BAG-DURUMU.md` (onaylandı, 26 Kasım); teşhis ölçümü `arsiv/teshis/faz5_3_b3_bag_olculeri_2026-11-25/`. Kâğıttaki yapı kararları:
- üç durum, OLAĞAN · SON ÇARE · KULLANILMAZ; eşik yok (kural 3–4);
- maliyet `n_s` ≥ `ORNEK_EN_AZ` ile; tamsayı birimi 1 ETX = 64 (kural 1–2);
- gönderici kanıtı başarısızlık sürdükçe uzar, son başarısızlıktan 5 s sonra kalkar ve bağ yeniden denenir (kural 6);
- "veri yok" güvenlik ağı: son 4 kaydın hepsi vazgeçme (kural 7);
- geçide giden bağ karıştırma kanıtıyla sona düşmez (kural 8);
- hariç aralık: kendi aralıklarım ve 3 s öne çekilmiş bildirim aralıkları, her biri en çok 30 s (kural 9);
- komşulara oran yalnız kendi aralıklarımla bildirilir (kural 10);
- B1'in sondaki sessizliği kullanılmıyor.

**Sorun.** B3 her bağ için iki şeye karar verir: bağ kullanılabilir mi (ve hangi sırada) ve maliyeti ne (B4 yol seçerken toplar). Girdileri B1'in iki ölçüsü (`E_selam`, `E_veri`; ikisi de beklenen deneme sayısı) ve B2'nin kanıtıdır. Önceki tasarımda eşikler iyi bağları düşürüyordu; karıştırılan bağ ise hiç kullanılmıyordu (`kural/KK-01`).

**Kanıt** (ölçüldü):
- Selam eşiğiyle çıkan bağlar kâhine göre iyi: çıkış anında `d_f · d_r` ~0,23–0,24, kâhinin tek deneme başarısı ~0,71–0,76. Veri tetiği kapalıyken kalan açlıkların kökü bu: tohum 1005'teki 155 bölümün hepsi selam eşiğinden (`arsiv/teshis/faz5_3_aclik_2026-11-18/sonuc.md` §6).
- Veriden hızlı tetik iyi bağları attı (%99,7'si iyi); kalkınca ikizde 0,810 → 0,946 (aynı belge §1–§3).
- Vazgeçme tetiği ayırt edilemedi: ikizde +0,014 (6/8), birincilde −0,009. Birincilde tetiklediği bağların %40'ı kâhine göre kötü bantta; iki hücrede döngüyü ters yönde etkiledi (`arsiv/teshis/faz5_3_yeni_cekirdek_2026-11-19/sonuc.md` §5, §6, §9).
- Eski veri tetiği yokken ikizde vazgeçmelerin %36–41'i en kötü beş bağda ve bu bağlar kâhine göre iyi bantta: selamı geçen ama veriyi taşımayan bağlar (açlık teşhisi §6; yeni çekirdek §6). Sebebi ölçülmedi.
- Kanal kalabalık: veri denemelerinde tek deneme başarısı 0,46–0,49; onay %94–96 geri geliyor (§2.1).
- Birincilde açık dönem kaybının büyüğü karıştırılan bağda, iletimde (0,267–0,335); kâhin bu bağları bildiği için 0,779 (§2.2).
- Karıştırılan alıcıya giden veri çerçevesi başına deneme: girişimde 3,9, kanal kilidinde 6,3, temizde 2,0 (`arsiv/teshis/faz5_2_isaretler_2026-11-16/sonuc.md` §3). Vazgeçme 7 deneme olduğundan girişimdeki alıcıya giden çerçevelerin önemli bir kısmı ulaşıyor olmalı (varsayım; payı ölçülmedi).
- Sessiz dönemde teslim: eğimli kollar 0,826–0,863, uygulanabilirlik koşulu 0,911, Babel 0,916. Farkın büyüğü yol seçiminden (B4); B3'ün payı karıştırma bitince bağın dönüş hızıdır.

**Seçenekler · çekirdek** (iki ölçüden maliyet ve kullanılabilirlik):

| | ne | artı | eksi ve bedel |
|---|---|---|---|
| 1 · önceki yol | maliyet selamdan; iki eşikle (4'te çıkar, 3'te döner) KÖTÜ; veri yalnız uyarı (vazgeçme işareti) | ölçüldü, basit | eşiğin yanılgısı kalır (iyi bağlar düşer, açlığın kökü); vazgeçme işareti ayırt edilemedi; `E_veri` kullanılmaz |
| **2 · kullanılan bağ veriyle, kullanılmayan selamla; eşikle düşürme yok** | yeterli ve taze veri kaydı varsa maliyet `E_veri`, yoksa `E_selam`; bağ yalnız maliyeti ∞ ise kullanılmaz (tek yönlü ya da verisi hiç geçmiyor); kötü bağ pahalıdır, yedeği varsa yol seçimi onu bırakır | kullanılan bağın gerçek bedeli, çarpışmalar dâhil; eşik çıkışı yok; veriyi taşımayan bağ pahalılaşır; veri tetik değil maliyettir (4B [69]) | iki kaynak aynı terazide: selam kötümser olduğundan veriyle ölçülen ardıl, selamla ölçülen yedekten ucuz görünebilir; veri ölçüsü yükle oynar (salınım, `17` T-4; histerezis B4'te); değerleri ölçülmedi |
| 3 · tek birleşik tahmin (4B gibi) | selam başlatır, veri inceltir; tek üstel ortalama | tek sayı, kaynak geçişi yok; 4B sabit deney ağlarında paket başına iletimi %29–44 azalttı | selamın kötümserliği ortalamaya karışır; iki zaman sabiti; karıştırmaya yavaş tepki; bizde ölçülmedi |

**Seçenekler · karıştırma eki** (B2'nin kanıtı bağa ne yapar):

| | ne | artı | eksi ve bedel |
|---|---|---|---|
| **E1 · son çare** | kanıt varken bağ, karıştırılmayan aday yoksa kullanılır; kanıt kalkınca eski maliyetiyle hemen döner | yedek varken kâhin gibi dolaşır; yedek yokken paketi yine dener; açlık doğurmaz | kanal kilidindeki alıcıya gönderim çoğu zaman boşa kanal süresidir |
| E2 · kullanım dışı (önceki `17` T-7) | kanıt varken bağ hiç kullanılmaz | en basit; kilitli alıcıya boşa gönderim yok | yedek yoksa yol yok: paket bekler ya da düşer (açlık riski) |
| E3 · maliyete karıştırma payı | kanıt varken maliyet bir katsayıyla büyür | maliyet sırası korunur | katsayı tahmine dayanır; önceki tasarım reddetti (T-7: ceza yavaş söner, salınım); pay kanıt kalkınca hemen silinirse E1'e yaklaşır |

**Kararım: 2 ve E1.**
- 2, sorunun kökü olan eşikle düşürmeyi tetik eklemeden kaldırır ve kullanılan bağın gerçek bedelini ölçer. Selamı geçen ama veriyi taşımayan bağ pahalılaşır, yedek varsa bırakılır. B1'in iki ölçüsü de kullanılır.
- E1, yedek varken E2 gibi davranır. Yedek yokken girişimdeki alıcıya göndermek göndermemekten iyidir (çerçeve başına 3,9 deneme). Açlık doğurmaz.
- Ek ne olursa olsun: dondurma yok, karıştırmadan önceki kalite B1'in hariç aralığıyla korunur; kendi karıştırılmamda bağlar MAC sonucuyla değişmez (B2 ayıklar); kanıt kalkınca hemen dönüş (İlke 3).

Seçilmeyenler: 1, kanıtlanmış yanılgıyı bıraktığı ve `E_veri`'yi kullanmadığı için; 3, selamın kötümserliğini veriye karıştırdığı ve karıştırmaya yavaş kaldığı için; E2, yedek yokken yol bırakmadığı için; E3, katsayısı tahmine dayandığı için. Karıştırma eki hiç ölçülmedi; katkısı Aşama 4'te ablasyonla ölçülür.

**Kâğıttan önce teşhis.** 2'nin iki riski ve değerleri ölçülmedi: (a) iki kaynak aynı terazide, (b) veri ölçüsünün yükle oynaması; ayrıca kaç veri kaydının "yeterli" olduğu ve selamın veri cinsine çevrilip çevrilmeyeceği. Kısa, önceden yazılı bir teşhis (yöntem: girdi eksikse kısa teşhis): bugünkü çekirdeğin trafiğinde aynı bağda `E_selam`, `E_veri`, kâhinin tek deneme başarısı ve bağın sonraki veri bedeli yan yana. Sorular, karar kuralı ve öngörüler beklentide.

**Teşhisin sonucu** (26 Kasım, `arsiv/teshis/faz5_3_b3_bag_olculeri_2026-11-25/sonuc.md`; çekirdeğimizin trafiği, ikiz ve birincil, 16 koşu):
- **Veri üstün değil** (K2): veri ölçüsü kullanılan bağın sonraki veri bedelini daha iyi kestiriyor (doğrulamada ortanca hata 0,231 ↔ 0,305 bit, yani ~%17 ↔ ~%24), ama fark önceden yazılı 0,10 bitlik sınırın altında. Beklentinin hükmüyle seçenek 2'nin dayanağı tutmadı; çekirdeğin seçeneği yeniden konuşulur.
- Veri ölçüsü selamı ancak 12 kayıtla 0,05 bit geçiyor (K3); 6 kayıtla iyi değil. 30 s'ye kadar tazelik sorun değil.
- Selamın veri cinsine çevrilmesi kazanç getirmiyor (K1: genel katsayıyla 0,016 bit).
- Veri yükle oynamıyor (K4: çiftlerin %0,5'i 10 s'de iki katına değişiyor). Selamı geçen ama veriyi taşımayan bağ seyrek ve kısa (K5: örneklerin %1,1–1,3'ü, ortanca 2 s).
- Karıştırmada selam hiç tepki vermiyor; veri, bağ-dönemlerin ~%40'ında dönem içinde iki katına çıkıyor (K6).
- Kuraldan sonra görülen: önceki tasarımın eşiğini (`E_selam` > 4) aşan bağların kullanılmayanlarda %45'i, kullanılanlarda %99'u kâhine göre iyiydi. Zarar ölçüden değil eşikten geliyordu (sonuç §10.2).

**Yeniden karar · çekirdek** (26 Kasım, kararım). K2'nin hükmüyle seçenek 2'nin dayanağı tutmadı. Seçenekler:

| | ne | artı | eksi ve bedel |
|---|---|---|---|
| **A · selam maliyet, eşikle düşürme yok** | bütün bağların maliyeti `E_selam` (tek terazi); bağ yalnız maliyeti ∞ iken kullanılmaz; veri yalnız güvenlik ağı: son kayıtlarda hiç onay yoksa bağ "veriyi taşımıyor" sayılır | kanıtlanmış zarar (eşik) kalkar; tek terazi; selamın hatası veriden yalnız 0,074 bit fazla; en basiti; çekirdek karıştırmaya tepki vermediğinden karıştırmaya özgü kazanç B2'nin katmanında ölçülür | selam ölçeği sıkıştırır: iyi bağ ~%20 ucuz, kenar bağ ~%15–28 pahalı görünür (sonuç §10.1); kullanılan bağın gerçek bedeli maliyete girmez |
| B · seçenek 2'de kalmak | kullanılan bağ en az 12 kayıtla veriden, değilse selamdan | kullanılan bağda daha doğru maliyet; çekirdek karıştırmaya biraz tepki verir | önceden yazılı eşiği geçemedi; iki terazi, ardıl ile yedeğin sırası ~%10 değişir (sonuç §10.3); 12 kayıt gerekir; çekirdeğin tepkisi genel mekanizma sayıldığından mekanizma kapısındaki farkı küçültebilir |

Önceki tasarımın eşikli yolu (seçenek 1) kuraldan sonra görülenle elendi: eşiği aşan bağların %45–99'u kâhine göre iyiydi (sonuç §10.2).

**Kararım: A.**
- Önceden yazılı kural, verinin yeterince üstün olmadığını söylüyor.
- Asıl zarar eşikteydi; A onu kaldırıyor. Tek terazi en sade çözüm.
- Karıştırma ekinde E1 değişmedi.
- B1'in kararı (iki ölçü ham ve aynı birimde) değişmez; birleştirmek B3'ün işiydi (§2.1). Veri ölçüsü B3'te yalnız güvenlik ağında ve tanıda kullanılır.

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
