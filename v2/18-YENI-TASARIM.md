# 18 · YENİ TASARIM — DESPARETE'nin baştan, bileşen bileşen tasarımı

> 24 Kasım 2026'da başladı (`12` §1.2 madde 3b). Faz 5-3'te üç sürüm ölçüldü: 18 Kasım çekirdeği, 19 Kasım çekirdeği ve bileşenleri, 20 Kasım'ın döngü kuralları. Her biri bir sorunu çözerken başka bir sorun açtı. Öğrenilenlerle protokolü baştan, tek tek ve eksiksiz tasarlamak istiyorum; ölçüm tasarım donduktan sonra yapılır.
>
> Bu belge yöntemi, eksiksizlik listesini ve aşamaların durumunu tutar. Bileşen kararları burada (bileşen başına bir bölüm, "Bileşenler"), kuralları yeni kural kâğıtlarında (`bilesen/`) yazılır; değerler, bayraklar ve gözlemin kullanımı tek yerde, `bilesen/00-DIZIN.md`de. `17` ve `kural/KK-*` önceki tasarımdır: yeni tasarım donana kadar bugünkü kodun ve ölçümlerin belgesi olarak kalır, sonra arşive gider.

## Durum

| aşama | durum |
|---|---|
| 1 · Zemin | tamam (24 Kasım): 1.1 hedef ve başarı ölçütü, 1.2 kısıtlar, 1.3 kanıt envanteri, 1.4 mimari iskelet |
| 2 · Bileşen bileşen tasarım | tamam (27 Kasım): 2.1 B1 komşu ve bağın ölçüsü tamam (24 Kasım); 2.2 B2 karıştırma kanıtı tamam (25 Kasım: alıcı ve gönderici birlikte; kurallar teşhis ölçümüyle seçildi, kanal kilidi kuralı sonuçtan sonra karara bağlandı; kâğıt onaylandı); 2.3 B3 bağın durumu tamam (26 Kasım: teşhis ölçümüyle seçenek 2'nin dayanağı tutmadı, yeniden kararım A: bağın maliyeti selamdan, eşikle düşürme yok, veri yalnız güvenlik ağı; karıştırılan bağ son çare; kâğıt onaylandı); 2.4 B4 yol tamam (26 Kasım: uygulanabilirlik koşulu, Babel ailesi; olağan bağlar son çaredekilerden önce; kâğıt onaylandı); 2.5 B5 iletim kararı tamam (27 Kasım: teşhisten sonra kararım A, tek yol; kâğıt onaylandı; B4'e Babel'in iki kuralı eklendi, onaylandı); 2.6 B6 kontrol iletileri tamam (27 Kasım: kararım Z1, uyarlanır aralık; kâğıt onaylandı; B4 kural 15'in olay listesi düzeltildi); 2.7 B7 bekletme ve komut tamam (27 Kasım: kararım H1, kısa bekletme, ve geri iz; kâğıt onaylandı) |
| 3 · Bütünlük ve donma | sürüyor (28 Kasım): 3.1 bütünlük denetimi tamam (`bilesen/01-BUTUNLUK.md`, onaylandı); 3.2 bağımsız denetim tamam (1 engelleyici, 5 önemli ve 6 küçük bulgu işlendi; ikinci okumada engelleyici kalmadı; kapanış `../arsiv/denetim/DENETIM-TASARIM-KAPANIS-2026-11-28.md`); sırada 3.3 donma ve büyük ölçümün beklentisi |
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
   - Çoğaltma önceki tasarımda yalnız son çareydi (`17` T-14). Kopyanın bu dünyadaki bedeli ölçülmedi: kopya kullanan tek protokol JarmRout'tu ve toplu akıştaki çöküşünün ~%90'ı yinelenen RREQ kuralındandı; yinelenen RREQ yayılmayınca, veri kopyaları sürerken PDR 0,599'dan 0,914'e çıktı (statik, karıştırıcısız, tek koşu; `arsiv/teshis/jarmrout_sel_2026-10-12/inceleme.md` §3, K-238). Önceki metin çöküşü kopyaya bağlıyordu (26 Kasım'da düzeltildi).
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
7. Kopyanın ya da fırsatçı iletimin bu dünyadaki bedeli. Kopya kullanan tek protokol JarmRout'tu; toplu akıştaki çöküşünün ~%90'ı yinelenen RREQ kuralındandı ve kopyanın payı ayrıca ölçülmedi (K-238; 26 Kasım'da düzeltildi, önceki metin çöküşü kopyaya bağlıyordu).
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
| B2 | karıştırma kanıtı | ben karıştırılıyor muyum; hangi komşuyla bağım karıştırılıyor | saniyelik işaretler (kanal meşgul payı, çözülen çerçeve, selam kaybı), kendi durumum ve aralıklarım, komşuların bildirimi ve bildirim aralıkları, göndericinin olayları (B1'in veri kaydından) | kendi durumum (yok · girişim · kanal kilidi) ve aralıklarım; bağ başına bildirim ve göndericinin olayı; selamın biti | karıştırmaya karşı |
| B3 | bağın durumu | bağ kullanılır mı; ne zaman bırakılır, ne zaman döner | bağ başına durum, sebepleri ve maliyeti (karıştırmadan önceki kalite, B1'in okumasında hariç aralıkla korunur) | bağ başına durum ve maliyet (tek kaynak); bildirilecek oran listesi | genel çekirdek + karıştırma eki |
| B4 | yol | geçide hangi komşular üzerinden gidilir; maliyetim ne; döngü nasıl önlenir | komşuların ilanları ve yaşları; FD ve tur; ardıl ve sıralı aday listesi (O ve S sınıfı); kendi maliyetim; yok sayma ve istek kayıtları; aynı düğüme dönüşün tanı kaydı (yalnız ölçüm) | aday listesi ve ardıl; kendi maliyetim ve açlık; ilan, "hemen gönder" olayları ve tur istekleri (B6'ya); ölçüm beyanları (kopma, rota kuruldu) | genel (kendi karıştırılmam kuralları karıştırma katmanında) |
| B5 | iletim kararı | bu paket hangi komşuya, şimdi mi | yok: durum tutmaz (kararım A, §2.5) | simülatöre karar: sonraki atlama ya da bekletme; kopya ve sapma yok | genel (karıştırma eki yok) |
| B6 | kontrol iletileri | hangi ileti, ne zaman, kime | selamın sırası, aralığı (I) ve planları (selam, son tarih) | simülatöre kontrol iletileri ve uyandırmalar; alınan iletinin alanları (B1, B2 ve B4'e) | genel |
| B7 | bekletme ve komut | yol yokken paket ne kadar tutulur; komut hangi yoldan iner | bekletme kayıtları (paketin ilk bekletme anı); geri iz; yeniden sorma planı | B5'e, B5'ten önce: yol yoksa bekletme ya da düşürme ve sebebi; komutun sonraki atlaması | genel |

**Sözleşme:**
1. **Tek yönlü akış.** Her bileşen yalnız kendinden aşağıdakilerin çıktılarını okur; hiçbir bileşen başkasının durumuna yazmaz. Tek istisna B7'nin B5'e cevabıdır (yol var mı, komutun sonraki atlaması): B5'ten önce hesaplanır, yani bu iş için B7 B5'in altında sayılır (B7 kural 10).
2. **Gözlemler sahibine gider.** Simülatörden gelen her gözlem, o bilginin sahibi olan bileşene dağıtılır:
   - MAC sonucu B1'e; B2 göndericinin kanıtını B1'in veri kaydından okur (sözleşme 3);
   - kontrol iletisini B6 çözer: selamın sırası, aralığı ve oranı B1'e, biti B2'ye, ilanı B4'e; tur isteği B4'e;
   - paketin başlığı (kaynak, sıra, atlama sayısı) B4'ün aynı düğüme dönüş tanısına (yalnız ölçüm, karara girmez);
   - paketi getiren komşu B7'ye (geri iz).

   Yukarıdaki bir bileşenin kararı aşağıdakine ancak böyle, bir sonraki gözlem olarak yansır.
3. **Tek kaynak.** Her büyüklük tek bileşende hesaplanır: bağın maliyeti B3'te, kendi maliyetim B4'te, karıştırma işareti B2'de. Öteki bileşenler okur, yeniden hesaplamaz. Her değer de tek yerde tanımlanır.
4. **Kanıtı silmeme.** Bir bileşenin kararı başka bir bileşenin kullandığı gözlemi ortadan kaldırıyorsa (ör. paket getirene gönderilmeyince döngünün dönüş kanıtı oluşmaz), bu etkileşim iki bileşenin kâğıdında da yazılır ve kanıtın yerine geçen şey tanımlanır (eksiksizlik listesi madde 14).
5. **Rota durumu ile paket kararı ayrı.** B4 sıralı bir aday listesi tutar; paketin yönünü B5 seçer. Paket başına bir sapma (ör. getiren komşuya geri göndermemek) rota durumunu değiştirmez. Rota durumunu değiştirecek bir kanıt varsa B4'e gözlem olarak gider.
6. **Kontrol iletileri tek yerde.** İletilerin biçimi ve gönderimi B6'dadır. Öteki bileşenler B6'ya yalnız taşınacak değerleri ve "hemen gönder" olaylarını verir.
7. **Ablasyon.** Her mekanizmanın bayrağı ve "kapalıyken" davranışı yazılır. Karıştırmaya karşı olanlar (B2'nin tamamı, B3'ün karıştırma eki, B4'ün kendi karıştırılmam kuralları; B5'in ve B6'nın eki yok) tek bir bayrak grubuyla birlikte kapanabilir. Kapalıyken kalan protokol eksiksiz çalışır; mekanizma kapısı bunu ister (`06` §0.4.5).
8. **Bellek sınırı.** Her tablonun üst sınırı ve silme kuralı yazılır (komşu, paket kayıtları, tampon, iz).

**Olay sırası** (her niyetli kancada aynı; 28 Kasım'da düzeltildi, `bilesen/01-BUTUNLUK.md` §4):
1. B1'in zaman olayları: zaman aşımları, silmeler (B1 kural 20). Öteki bileşenlerin süreleri kendi adımlarında, o anın saatiyle değerlendirilir.
2. Gözlemi sahibine dağıt; kontrol iletisini B6 çözer.
3. B2 → B3 → B4: kanıt, bağın durumu, yol.
4. Paket varsa önce B7'nin cevabı (yol var mı, komutun sonraki atlaması), sonra B5'in kararı.
5. B6: değişim olaylarından doğan ve planlı kontrol iletileri; B4'ün tur istekleri; B6'nın uyandırmaları.
6. B7: yeniden sorma uyandırması.
7. Beyanlar: kopma ve rota kuruldu (B4 kural 18); düşen paketin `rota_gecersiz`i kararla birlikte (B7 kural 4).

Niyet döndüremeyen kancalarda (`iletim_sonucu`, `cerceve_duyuldu`) yalnız 1. ve 2. adım yapılır; gerisi bir sonraki niyetli kancada.

**Kancalar ve gözlemleri:**

| kanca | dağıtılan gözlem | olay sırasının adımları |
|---|---|---|
| saniyelik zamanlayıcı | B2: kanal meşgul süresi, çözülen çerçeve sayısı (selam kaybını B1'in örneklerinden hesaplar) | 1–7 |
| uyandırma | — (B6'nın selamı ve son tarihi, B7'nin yeniden sorması; simülatör bekletme tamponunu döker) | 1–7 |
| kontrol iletisi alındı | B6 çözer · B1: selamın sırası, aralığı, oranı · B2: karıştırma biti · B4: ilan; tur isteği | 1–7 |
| iletim sonucu (niyetsiz) | B1: veri sonucu ve onay (B2 B1'in kaydından okur) | 1–2 |
| iletim başarısız | — | 1–7 |
| çerçeve duyuldu (niyetsiz) | B1: komşu hâlâ orada · B7: geri iz | 1–2 |
| sonraki atlama | paket: B7 ve B5 (yön) · B4: aynı düğüme dönüşün tanısı (yalnız ölçüm) | 1–7; B7'nin cevabı ve B5'in kararı |

**Karıştırma katmanı kapalıyken çekirdek:** B1, B3'ün çekirdeği, B4 (kendi karıştırılmam kuralları olmadan), B5, B6, B7. Çekirdek kendi başına eksiksiz bir yönlendirme protokolüdür; ikizde zarar olmadığını ve kapı ölçümünü bu kol verir.

**28 Kasım düzeltmesi** (Aşama 3, `bilesen/01-BUTUNLUK.md` §11): tablo, sözleşme 1, 2 ve 7, olay sırası ve kanca tablosu onaylı kâğıtlara göre düzeltildi. 24 Kasım'daki metin B5'e paket başına kayıt ve karıştırma eki, B4'e döngü kaydı, B2'ye MAC vazgeçmesi öngörüyordu; olay sırasında gözlemin dağıtımı zaman olaylarından önceydi. Yapı kararı 3'ün ayrımı korunur: B5 ayrı ve durumsuzdur. Kararı A (sapma yok, §2.5) bu yapının içinde bir seçimdir; komutun yolu (B7'nin izi) B4'ün ardılından ayrıdır. Bağımsız denetimden sonra (28 Kasım; `../arsiv/denetim/DENETIM-TASARIM-KAPANIS-2026-11-28.md`): B6'nın kilit kuralı kaldırıldı; beyanlar B4 kural 18'de tanımlandı; B1'in olay listeleri niyetli kancanın sonunda boşalır.

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

### 2.4 · B4 · Yol (26 Kasım, kararım)

Kâğıt: `bilesen/B4-YOL.md` (onaylandı, 26 Kasım; 27 Kasım eki onaylandı, aşağıda). Kâğıttaki yapı kararları:
- adaylar iki sınıf: B3'te olağan olanlar (O) son çaredekilerden (S) önce, sınıf içinde maliyetle (kural 3, 5);
- geçiş Babel'in histerezisiyle: anlık ve düzgünleştirilmiş maliyet birlikte (kural 5–6);
- ilanın ömrü: komşunun son ilanı selam aralığının 3,5 katından eskiyse ∞ (kural 4);
- FD ilan için verildiği anda güncellenir (tutucu; kural 9);
- uygulanamaz ilan 5 s'ye kadar yok sayılır ve tur istenir (kural 10);
- tur isteği yalnız kullanılır bağlı ama uygulanamaz ilanlı komşu varken gider ve kendi karıştırılmamda bastırılır (kural 11, 14);
- karıştırma ilana yansıtılmaz (§11 madde 3);
- eski döngü bekçisi ve geri gönderme yasağı gerekmez, döngü yalnız tanıda sayılır (kural 17).

**Sorun.** B4 geçide giden yolu seçer:
- hangi komşu ardıl olur, hangileri sıralı yedektir;
- düğümün kendi maliyeti nedir;
- döngü nasıl önlenir.

Girdileri B3'ün bağ maliyetleri ve durumları (olağan · son çare · kullanılmaz) ile komşuların ilanlarıdır. Önceki tasarımda iki yol ölçüldü: uygulanabilirlik koşulu (18 Kasım; Babel'in yolu) açlık yüzünden, maliyet eğimi (19–20 Kasım; CTP ve RPL'nin yolu) döngü yüzünden zorlandı.

**Kanıt** (ölçüldü; 8 tohum; `arsiv/teshis/faz5_3_dongu_kurallari_2026-11-24/sonuc.md` §1, §5, §8 · `arsiv/teshis/faz5_3_yeni_cekirdek_2026-11-19/sonuc.md` §6, §9):

| | ikiz | birincil `PDR_açık` | en kötü tohum | sessiz dönem | gecikme p99 | döngü dönüşü / koşu (birincil) |
|---|---|---|---|---|---|---|
| Babel | 0,930 | 0,663 | 0,485 | 0,916 | 1,31 s | — |
| uygulanabilirlik koşulu (eğim0) | 0,943 | 0,665 | 0,470 | 0,911 | 1,08 s | ölçülmedi* |
| eğim (19 Kasım) | 0,954 | 0,663 | 0,314 | 0,854 | 1,77 s | 3 620 |
| eğim + geri yasağı + sınırlı yükselme | 0,958 | 0,659 | 0,408 | 0,863 | 1,24 s | 1 014 |

\* 28 Kasım düzeltmesi (bağımsız denetim Ö-2): eğim0'ın kayıtlarında döngü sayacı yoktu. Önceki "0", hesabın eksik sayacı 0 diye okumasından geliyordu (`arsiv/teshis/faz5_3_dongu_kurallari_2026-11-24/sonuc.md`'deki not). Döngüsüzlüğün dayanağı RFC 8966 §2.4'ün ispatıdır.

- **Ortalamayı yol seçimi belirlemiyor:** birincilde beş yol seçiminin ortalaması 0,659–0,666; kayıp karıştırılan bağda, iletimde.
- **Koruma ölçütleri:** en kötü tohum ≥ 0,465, sessiz dönem Babel'den kötü değil, p99 ≤ 1,31 s (§1.1). Hepsini geçen tek ölçülmüş yol uygulanabilirlik koşulu.
- **Eğimin ikizdeki üstünlüğü iletim kaybından geliyor:** 0,044 ↔ 0,055; atlama başına başarısızlık %1,44 ↔ %1,83. Eğimde daha çok komşu aday olabiliyor.
- **Uygulanabilirlik koşulunun açlığı:** ilk çekirdekte ikizde koşu başına 822; kökün %99'u eski veri tetiğiydi. Tetik kapalıyken ikizde koşu başına 18–31, birincilde (eğim0) 103; kalanın kökü selam eşiğiydi (açlık teşhisi §6). İki kök de kalktı (19 Kasım; B3).
- **Babel aynı koşulla birincilde rota yokluğundan hiç kaybetmiyor** (açık dönemde 0,000; eğim0'da 0,037). Babel açlığı hemen tur isteğiyle çözüyor ve uygulanamaz bir güncelleme gelince seçili rotasını hemen bırakmıyor (`17` §4).
- **Eğime eklenen iki kural döngüyü çözmedi:** geri gönderme yasağı döngü bekçisinin kanıtını sildi; sınırlı yükselme döngüyü %68 azalttı ama rota yokluğunu artırdı.

**Seçenekler:**

| | ne | artı | eksi ve bedel |
|---|---|---|---|
| **Y1 · uygulanabilirlik koşulu** (Babel ailesi: geçidin turu, tur isteği) | aday yalnız uygulanabilir komşudur; olağan bağlar son çaredekilerden önce, kendi aralarında maliyetle sıralanır; aday kalmayınca yeni tur istenir | döngüsüzlük RFC 8966 §2.4'ün ispatıyla garanti (eğim0'da sayaç yoktu, ölçülmedi; 28 Kasım); koruma ölçütlerini geçen tek ölçülmüş yol; RFC 8966'nın sınanmış mekanizması; açlığın iki kökü kalktı | ikizde eğimden geride (0,943 ↔ 0,958); aday kalmayınca açlık ve tur isteği; selamda tur alanı ve tur isteği iletisi |
| Y2 · maliyet eğimi + döngü bekçisi (önceki tasarım) | maliyeti benimkinden küçük her komşu aday, yoksa son çare; döngü veri yolunda yakalanır | ikizde en iyi; açlık yok | karıştırmada koşu başına 1 000–3 600 döngü; en kötü tohum ve sessiz dönem koruma ölçütünü geçmiyor; eklenen iki kural döngüyü çözmedi, biri döngü kanıtını sildi |
| Y3 · karma | normalde uygulanabilirlik; aday kalmayınca yeni tur gelene kadar eğimle son çare ve döngü bekçisi | normalde döngüsüz, açlıkta da paket ilerler | hiç ölçülmedi; iki mekanizmanın karmaşıklığı; açlık B3'ten sonra seyrekse kazancı küçük |

**Kararım: Y1.**
- Ölçülen yollar içinde koruma ölçütlerinin hepsini geçen tek yol; döngüsüzlüğü garanti.
- Zayıflığının (açlığın) iki kökü kalktı.
- İkizde Babel'in önünde (0,943 ↔ 0,930): "ikizde zarar yok" ölçütü tutuyor.
- Döngü kuralları ölçümünün önceden yazılı hükmü de "uygulanabilirlik koşuluna dönüş yeniden tasarımda konuşulur" diyordu.

Seçilmeyenler: Y2, en kötü tohumda ve sessiz dönemde koruma ölçütlerini geçemediği ve döngüyü iki kuralla da çözemediği için; Y3, ölçülmediği ve iki mekanizmayı birlikte taşıdığı için. Açlığın yeni tasarımdaki sıklığı Aşama 4'te ölçülür. Yüksek kalırsa Y3'ün açlıktaki son çaresi o zaman düşünülür.

**27 Kasım eki** (kararım; B5 teşhisinden sonra, yeni kanıtla). 26 Kasım'daki kâğıtta Babel'in iki SHOULD kuralı yoktu; ikisi de rakip Babel-a'da var. B5 teşhisi ikisinin bedelini gösterdi (`arsiv/teshis/faz5_3_b5_iletim_kaybi_2026-11-26/ek_hesap.txt` E8, E9; kuraldan sonra):
- **Tercih edilir uygulanamaz ilanda istek** (RFC 8966 §3.8.2.2'nin ikinci paragrafı; B4 kural 10a). Ardıl varken bir komşunun ilanı uygulanamaz ama sıralamada ardıldan önce geliyorsa o komşuya tur isteği gider. "Önce gelmek": sınıfı daha iyi (olağan ↔ son çare) ya da aynı sınıfta en az 2 ETX ucuz (babeld'in eşiği). Kanıt: ardılın kanıtı varken olağan aday yoksa, yalnız uygulanabilirlik yüzünden aday olmayan temiz bir komşu J3, J4 ve U2'nin kayıplarında 0,038 payda. B4 isteği yalnız hiç aday kalmayınca gönderiyordu. 28 Kasım düzeltmesi (bağımsız denetim E-1): bu payın ~%72'sinde engelli komşunun yolu kararı veren düğümden geçiyordu; yeni tur onları aday yapamaz ve istek her yeni turla yineleniyordu. Kurala `C_j` < C koşulu ve istenen turdan bağımsız bekleme eklendi; alt ağaç dışlanınca üst sınır en çok ~0,011. Yeni koşul bu payın ancak bir kısmına ulaşır: kararlı durumda sınıf dalı yalnız eski turlu ilanlarda ve maliyetim aynı turda yükseldiğinde çalışır, benden pahalı temiz kardeş dal artık hedef olmaz (ikinci okuma).
- **Süre dolmadan istek** (§3.8.2.3; B4 kural 4a). Ardılın ilanı bir selam aralığı kala tazelenmemişse ardıla tek alıcılı rota isteği gider; ardıl hemen selamla yanıtlar. Kanıt: ikizde kararların %2,1'inde ardılın ilanı bayattı, ama ardıla giden çerçevelerin %96'sı onaylanıyordu; bunların %31'inde başka aday yoktu. `ILAN_OMUR_KAT` 3,5'te kaldı.
- Seçilmeyenler: kuralları Aşama 4'e bırakmak (ölçülmüş bir bedel açık kalırdı); `ILAN_OMUR_KAT`'ı büyütmek (daha basit, ama susan komşu geç bırakılır ve değeri seçecek ölçü kayıtta yok).
- Eki yazarken bir tutarsızlık düzeltildi: kural 14 kendi karıştırılmamda "adaylar değişmez" diyordu, ama ilanların yaşı işlemeye devam ediyordu. Girişim alanında selamların ~%73'ü kaybolduğu için ardıl birkaç selam aralığında aday olmaktan çıkardı. Kendi aralıklarımda yaş artık durur (B4 kural 4), bağın maliyetinin hariç aralıkla korunması gibi (B3 kural 9).
- İki yeni kuralın bayrağı var (`sure_istegi`, `tercih_istegi`; genel); katkıları Aşama 4'te ölçülür.

### 2.5 · B5 · İletim kararı (26–27 Kasım, kararım)

Kâğıt: `bilesen/B5-ILETIM-KARARI.md` (onaylandı, 27 Kasım). Kâğıttaki yapı kararları: B5 durum tutmaz; karar paket havaya çıkarken verilir (geç bağlama); son çaredeki ardıla gönderim sürer, ayrı bekletme yok; açlıkta ve komutta karar B7'nindir; karıştırma eki yok.

**Sorun.** B5 her veri paketi için üç şeye karar verir:
- hangi komşuya: B4'ün sıralı aday listesinden; listedeki her aday uygulanabilir olduğu için döngü oluşmaz (`bilesen/B4-YOL.md` §15);
- şimdi mi, yoksa tutulsun mu (B7 ile);
- kopyalı mı.

Komutun sonraki atlaması B7'nin geri izindendir.

Simülatörün çerçevesi (kod):
- protokole atlama başına bir kez sorulur, geri çekilme bitip çerçeve havaya çıkarken (`sim2/kosum/gonderim.py`, `iletime_basla`); MAC aynı komşuya en çok 7 kez dener;
- 7 deneme de boşa giderse ve alıcı çerçeveyi çözmediyse paket düşer; protokol bunu sonra öğrenir (`sim2/kosum/kosu.py`: önce `vazgec`, sonra `iletim_sonucu` ve `iletim_basarisiz`). Başarısız paketi başka komşuya göndermek (kurtarma) bugün yoktur;
- kopya kuyruğun sonuna girer ve asıl paket geçse de gönderilir; ara düğüm onu tanımaz (`13` §07);
- kendi kanal kilidimde kanal hep meşgul olduğu için geri çekilme bitmez, protokole sorulmaz.

**Kanıt** (ölçüldü):
- Birincilde açık dönem kaybının büyüğü iletimde. Uygulanabilirlik koşulunu kullanan kolda (`eğim0`) iletim 0,297 · rota yokluğu 0,037; Babel'de 0,335 · 0 (`arsiv/teshis/faz5_3_dongu_kurallari_2026-11-24/ek_hesap.txt` §3).
- `eğim0`'da iletim kaybı alıcıya göre: kanal kilidi 0,048 · girişim 0,168 · uzak 0,081 (`arsiv/teshis/faz5_3_yeni_cekirdek_2026-11-19/kayit_egim0_birincil.json`, `dogum_evre_dusen`).
- Karıştırılan alıcıya çerçeve başına deneme: girişimde 3,9, kanal kilidinde 6,3, temizde 2,0 (`arsiv/teshis/faz5_2_isaretler_2026-11-16/sonuc.md` §3).
- Kanal kalabalık: denemelerin yarısından fazlası başarısız. Ağın toplam yayın süresi 100 s artınca alıcıların çerçeveye kilitlenmesi ~2 puan düşüyor (`arsiv/teshis/faz5_2_secenek_iletim_2026-11-15/sonuc.md` §5).
- Kopyanın bu dünyadaki bedeli ölçülmedi (§1.3, bilmiyoruz 7).
- Önceki tasarımda paket hep ardıla gitti; çoğaltma `17` T-14'te yazılmıştı ama kodlanmadı.

**Seçenek aileleri** (karar değil):

| | ne | artı | eksi ve bedel |
|---|---|---|---|
| A · tek yol | paket hep ardıla; karıştırmaya karşılık B2 → B3 → B4'ten | en basiti; fazladan yayın yok | kanıt gelene kadar ve temiz aday yokken paket karıştırılan bağa gider |
| B · paket başına hızlı sapma | ardıla giden çerçeve kötü bitince sonraki paketler kısa süre sıradaki adaya; yol durumu değişmez | göndericinin en hızlı işareti; bağ atılmadığı için açlık doğmaz | temiz kanalda yanlış sapma; ikinci aday daha pahalı |
| C · seçici kopya | ardılın kanıtı varken bir eş sıradaki adaya da | iki bağımsız şans | kalabalık kanala yayın; eş asıl geçse de gider; bedeli bilinmiyor |
| D · kurtarma | MAC vazgeçince paket düşmez, sıradaki adaya gider (DSR'nin "salvaging"i, RFC 4728 §3.4.1) | yalnız başarısızlıkta harcar | simülatörün yetenek sözleşmesini (`13`) genişletir; kapsam kararı |

Fırsatçı iletim (ExOR, ORW) MAC'te yeni bir iletim türü ister; en büyük değişikliktir ve bu karara girmez. Bekletme ayrı bir aile değil, bir alt sorudur: yalnız son çare adayı varken paketi kısa süre tutmak.

**Kararım (26 Kasım): ana seçenekten önce kısa bir teşhis.** Ailelerin her biri iletim kaybının başka bir parçasına ulaşıyor ve bu parçaların büyüklüğü ölçülmedi:
- kaybın ne kadarı karıştırılan alıcıda ve kanıttan önce oluyor;
- ne kadarı temiz aday yokken oluyor;
- ne kadarı temiz alıcıda oluyor.

Teşhis: `arsiv/teshis/faz5_3_b5_iletim_kaybi_2026-11-26/`. Bugünkü kodun `eğim0` kolunun trafiğinde, ikiz ve birincil, 16 koşu. Her iletim kaybı, karar anındaki duruma göre yeni tasarımın kurallarıyla sınıflanır; ulaşabileceği pay 0,02'nin altında kalan aile elenir. Sorular, karar kuralı ve öngörüler `beklenti.md`de.

**Teşhisin sonucu** (27 Kasım, `arsiv/teshis/faz5_3_b5_iletim_kaybi_2026-11-26/sonuc.md`; `eğim0`'ın trafiği, ikiz ve birincil, 16 koşu). Paylar açık dönemde doğan paketlere oranladır. "Ağırlıklı" pay, sıradaki adaya gidilseydi geçme olasılığının kâhine göre üst sınırıdır.
- **Elenen aile yok** (K1):
  - B'nin hedefi (J2: alıcı karıştırılıyor, kanıt henüz yok, sıradaki aday temiz) 0,022; 8 tohumun 4'ünde 0,02'yi geçiyor.
  - C'ninki (J3: sıradaki aday kirli) 0,036; D'ninki (J2 + J3 + U1) 0,100.
  - Katmanın kendi payı (J1: kanıt var ve temiz bir olağan aday var) 0,0485; hedefe gereken 0,048.
- **B'nin tetiği yok** (K3): hiçbir aday temiz kanalda kararların %2'sinden azını saptırmıyor. En yakını art arda iki tam denemeli çerçeve: seçimde %2,19, doğrulamada %1,52.
- **Kopya pahalı** (K4, E6): C1 birincilde koşu başına veri yayın süresine 81 s ekliyor (372 s'nin %22'si), ikizde 19 s. C2 ucuz ama yalnız 0,004'e ulaşıyor.
- **Kurtarmanın kazancı büyük ama önemli bir kısmı genel** (K5, E4, E6): ikizde de üst sınır 0,0525. Yayın eki birincilde 41 s, ikizde 17 s. Simülatörün yetenek sözleşmesini (`13`) genişletir.
- **Kuraldan sonra görülenler** (karar kuralının girdisi değil; `ek_hesap.txt` E7–E9):
  - J1'in 0,032'sinde karar anında çekirdeğin bir kanıtı da var (veri yok, ilan bayat). Katmanın kendine ait payı en çok 0,016. Mekanizma kapısının kolunda (katman kapalı, genel mekanizmalar açık) çekirdeğin kanıtı kalır; genel bir kurtarma bu kolda katmanın kayıplarını da kurtarır.
  - Yalnız uygulanabilirlik koşulu yüzünden aday olmayan temiz bir komşu J3, J4 ve U2'de 0,137 payda var. Bunun 0,038'inde ardılın kanıtı var ve olağan aday yok. RFC 8966 §3.8.2.2'nin ikinci paragrafı böyle bir komşuya tur isteği gönderilmesini ister (SHOULD); B4'te bu kural yok, Babel-a'da var.
  - İkizde kararların %2,1'inde ardılın ilanı bayat, ama ardıla giden çerçevenin onayı %96. Bu kararların %31'inde ardıldan başka aday yok; yeni tasarımda ardıl bu kararlarda aday olmaktan çıkar. RFC 8966 §3.8.2.3 seçili rotanın süresi dolmadan istek gönderilmesini ister (SHOULD); B4'te bu kural yok, Babel-a'da var.

**Kararım (27 Kasım): A, tek yol.** Paket hep B4'ün ardılına gider; kopya, paket başına sapma ve kurtarma yok. Karıştırmaya karşılık B2 → B3 → B4'ten gelir; B5'in karıştırma eki yoktur.
- Mekanizma kapısını bulandırmaz: kapının kolunda (karıştırma katmanı kapalı) B5 aynı çalışır. Katmanın J1'deki kendi payı zaten ince (en çok 0,016); onu küçültecek bir genel mekanizma eklemedim.
- Fazladan veri yayını eklemez; kalabalık kanalda bu bir koruma ölçütüdür.
- Simülatörün yetenek sözleşmesine dokunmaz.
- Bedeli: B5'in ailelerinin ulaşabileceği kayıp açık kalır (J2 + J3 + U1, üst sınır 0,100). Hedefe (+0,048) ulaşmak garanti değil; dayandığı paylar, katmanın J1'i (0,0485) ve B4'ün 27 Kasım eki (0,038; 28 Kasım'da alt ağaç hedefleri çıkınca en çok ~0,011, yeni koşulun ulaşabildiği pay bunun bir kısmı), birer üst sınırdır.

Seçilmeyenler:
- **B · hızlı sapma:** tetik yok; en iyi aday bile temiz kanalda kararların %1,5–2,2'sini saptırıyor. Ulaşabileceği pay sınırda (0,022; 8 tohumun 4'ünde 0,02'yi geçiyor).
- **C · seçici kopya:** C1 kalabalık kanala koşu başına 81 s yayın ekliyor (veri yayın süresinin %22'si). C2 ucuz ama 0,004'e ulaşıyor; Aşama 4'te ayırt edilemez.
- **D · kurtarma:** en büyük kaldıraç (0,100), ama dört bedeli var:
  - genel bir mekanizma: ikizde de üst sınırı 0,0525 (K-247); kapıya girmez;
  - kapının kolunda katmanın kurtaracağı paketleri de kurtarır ve katmanın kendi payını büyük ölçüde siler. Kapı "üstün" hükmünün şartıdır (`06` §0.4.5); geçmezse hüküm "fark var, karıştırmaya özgü mekanizmaya bağlanamadı" olur;
  - simülatörün yetenek sözleşmesini (`13`) genişletir; alıcı çerçeveyi çözmüş ama onay kaybolmuşsa kurtarılan paket bir kopyaya dönüşür;
  - birincilde koşu başına 41 s yayın eki.

  D ölçülmüş üst sınırıyla kayıtlıdır. Aşama 4'te hedef tutmazsa ilk düşünülecek kaldıraç odur; kapıya etkisi o zaman yeniden hesaplanır.
- **Son çaredeki ardıl için bekletme** (alt soru): alınmadı. J4'ün (karıştırılan ardıldan başka aday yok) 0,053'ünün yalnız 0,011'i kanal kilidindeki alıcıda, 0,042'si girişimde (`ek_hesap.txt` E10); girişimdeki ardıla gönderim çoğu zaman işe yarıyor. Açlıkta bekletme B7'nindir.

### 2.6 · B6 · Kontrol iletileri (27 Kasım, kararım)

Kâğıt: `bilesen/B6-KONTROL-ILETILERI.md` (onaylandı, 27 Kasım). Kâğıttaki yapı kararları: iki ileti (selam ve tur isteği), alanları B1–B4'ün beklentilerinden; komşu listesi her selamda tam; selamı öne çeken olaylar B4'ün geri çekmesi, istek yanıtı (tutulan isteği karşılayan tur değişimi dâhil) ve maliyetin önemli değişimi (%15), B2'nin bit değişimi ve B1'in yeni komşusu; tek başına ardıl değişimi olay değil (RFC 8966 §3.7.2; B4 kural 15 buna göre düzeltildi); en kısa ara 0,5 s; çoklu yayın titreşimli; B4 kural 4a'nın anı için uyandırma. 28 Kasım'da bağımsız denetimden sonra düzeltildi: isteği karşılamayan tur değişimi olay değil (RFC 8966 §3.7.2; Ö-1); kendi kanal kilidimde selam kurmama kuralı (karıştırma eki) kaldırıldı, çünkü kilit saniyelerinin çoğunda kanal kısmen boştu (Ö-5).

**Sorun.** B6 kontrol iletilerinin biçimini ve gönderimini tek yerde toplar (§1.4 sözleşme 6): hangi ileti, ne zaman, kime. Öteki bileşenler B6'ya yalnız taşınacak değerleri ve "hemen gönder" olaylarını verir. Kâğıtların B6'dan beklentileri:
- **B1** Ö-1…Ö-7: sıra numarası; bir sonraki selama kadarki üst sınırı taşıyan aralık alanı; komşu listesi (adres, oran); iki selam arası en az 0,5 s; sırası tüketilen selamın gönderilmesi; B1'in son tarihi için uyandırma; yeni komşu olayının karşılığı.
- **B2** Ö-1…Ö-5: 1 bitlik karıştırma alanı; "bit değişti"de hemen selam; durum sürerken aralığın kısaltılması (B6'nın kararı); kanal kilidinde kurulup bekleyen selamın bayat biti; bayrak kapalıyken alanın kalması.
- **B3** §6: bildirilecek oran listesi (B3 kural 10).
- **B4** Ö-1…Ö-5: her selamda ilan (tur ve maliyet, 16'şar bit); "hemen gönder" olayları; tur isteği iletisi (istenen tur 16 bit, kalan atlama 8 bit); aralık alanının ilanın ömrü için de kullanılması; kural 4 ve 4a'nın anları için uyandırma.

İletilerin içeriği bu beklentilerle büyük ölçüde belli. Selamın ilanı ve oran listesini taşıması B1'de ve B4'te yazılı; ayrı bir ilan iletisi önceki tasarımda da yoktu (`17` T-16: her çerçevenin 64 baytlık ek yükü ve kanal erişimi bir kez ödenir). Açık kalan asıl soru **selamın zamanlamasıdır**: selam ne sıklıkla gider, onu ne öne çeker. Öteki bileşenlerin değerleri bugünkü zamanlamaya göre yazıldı: ilanın ömrü 3,5 · a, B2'nin selam kaybı penceresi 4 s, B1'in saklaması (128 örnek) ve boşluk sınırı (64 selam), düzgünleştirmenin zaman sabiti 6 s, istek aralığı 0,5 s (`bilesen/00-DIZIN.md`).

Simülatörün çerçevesi (`13` §03, kod):
- kontrol iletisi veriyle aynı kanalı, MAC'i ve kayıp fiziğini paylaşır; kuyrukta önceliklidir;
- yayın onaysız ve tekrarsızdır; tek alıcılı ileti 7 kez denenir;
- ileti boyu ⌈Σ bit / 8⌉ + 64 bayttır. Selam temel hızda (1 Mb/s) gider: komşu listesi boşken 73 bayt ve 0,78 ms, 15 komşuyla 103 bayt ve 1,02 ms, 39 komşuyla 151 bayt ve 1,40 ms;
- uyandırma düğüm başına en çok 256; titreşimi protokol ister.

**Kanıt** (ölçüldü; bugünkü kodun `eğim0` kolu, ikiz ve birincil, 8 tohum; `arsiv/teshis/faz5_3_b6_kontrol_bedeli_2026-11-27/kontrol_bedeli.txt`, B5 teşhisinin ve teşhis (c)'nin kayıtlarından, yeni koşu yok):
- **Bugünkü selam** (`kural/KK-02`): aralık Trickle mantığıyla uyarlanır. I 0,5 s'den başlar, olaysız her selamdan sonra iki katına çıkar (en çok 2 s); bir değişim olayında 0,5 s'ye iner. İlan edilen aralık 1,1 · I, en çok 2,2 s.
- **Sıklık:** koşu başına 8 635 selam (ikiz) ve 9 384 (birincil), düğüm başına saniyede 0,62 ve 0,67. Bunların %15'i ve %19'u ara ilan. Yeni komşu olayı koşu başına ~1 080.
- **Bedel:** "kontrol payı" (kontrol kanal süresinin toplam gönderim süresine oranı) %6,0 ve %5,9. Bunun yalnız %2,6'sı ve %2,7'si protokolün kendi iletileri (selam ve tur istekleri, ileti başına ~100 bayt). Geri kalanı veri çerçevelerinin MAC onaylarıdır: simülatör onayı da kontrol çerçevesi sayıyor (`sim2/kosum/teslim.py`). Aynı ayrımla Babel-a'nın kendi iletileri %11,0 ve %11,6, onaylar dâhil %14,7 ve %15,1. Koruma ölçütü (§1.1) onaylı tanımla yazıldı; tanım değişmiyor.
- **Kanalın duyarlılığı:** kanaldaki toplam gönderim 100 s artınca alıcıların çerçeveye kilitlenmesi ~2 puan düşüyor (`arsiv/teshis/faz5_2_secenek_iletim_2026-11-15/sonuc.md` §5). Koşu başına ~9 s'lik selam süresi bu ölçekte küçük.
- **Selam kaybı:** temiz kanalda da yüksek: ikizde selam kaybı payının ortalaması 0,46 (B2 §11 madde 6). Ardılın ilanı kararların %2,1'inde 3,5 · a'dan eski (B5 teşhisi E9); B4 kural 4a bunun karşılığı.
- **Bit:** girişimdeki düğümün selamı uzak bir komşuya 0,35 olasılıkla ulaşıyor (B2 teşhisi K6). Bitin anında bilinmesi (ideal) ile bugünkü selamlarla gelmesi arasındaki fark, katmanın kurtarabileceği kayıpta (J1) yalnız 0,004 (0,0485 ↔ 0,0447; B5 teşhisi K1).
- **Babel** (RFC 8966 [4] Ek B, §3.7.2): selam 4 s; ters yön bildirimi üç selamda bir, kayıplı bağda her selamda; güncelleme 16 s; rotanın ömrü 3,5 × 16 s. Kopuş 1,5–3,5 selam aralığında fark edilir. Tetiklenen güncelleme geri çekmede SHOULD; maliyeti belirgin değiştirmeyen ardıl değişiminde SHOULD NOT.
- **Ölçülmüş kanıtın koşulu:** B2'nin eşikleri (`s` ve `c` bu selam trafiğiyle ölçüldü), B3 ve B5 teşhisleri hep bu zamanlamadadır.

**Seçenekler · selamın zamanlaması** (ana seçenek; karar değil):

| | ne | artı | eksi ve bedel |
|---|---|---|---|
| Z1 · uyarlanır aralık (bugünkü) | I 0,5 s'den 2 s'ye ikiye katlanır; değişim olayında 0,5 s'ye iner | ölçülmüş bütün kanıtın ve B2'nin eşiklerinin koşulu; bedeli ölçülü (%2,6); değişim en geç 0,5 s'de duyurulur; Trickle [62] ve Babel'in aralık alanı | sakin ağda aralık 2,2 s: ilanın ömrü 7,7 s; susan komşu ve bağın değişimi buna göre geç görülür (`d_r`'nin 16 örneği ~35 s) |
| Z2 · sabit kısa aralık (ör. 1 s) | her selam 1 s'de; olay yine öne çeker | öngörülebilir; ilanın ömrü ~3,9 s; `s` ve `d_r` daha çok örnekle; susan komşu iki kat çabuk fark edilir | selam ~%75 artar, protokolün payı %2,6'dan ~%4,5'e (kestirim); B2'nin eşikleri ve teşhislerin kanıtı bu trafikte ölçülmedi, Aşama 4'e kadar sınanmamış kalır; susan ardıla karşı kazancın üst sınırı küçük (kanal kilidindeki alıcının kaybı J3'te 0,016, J4'te 0,011; B5 teşhisi E10) |
| Z3 · Z1 + karıştırmaya duyarlı aralık | kendi bitim 1 iken aralık 0,5 s'de kalır (B2 Ö-3) | bit komşulara daha çabuk ulaşır; karıştırma katmanının parçası olur, kapıya girer | bitin hızlanmasının J1'e katkısı en çok 0,004 (yukarıda); girişimdeki ~7 düğüm açık dönemde selamı 4 kat sık gönderir |
| Z4 · Babel'in aralığı (4 s) | sabit 4 s | en az yük | ilanın ömrü ~15 s, açık dönem 15 s: karıştırmaya tepki çok geç |

**Kâğıda kalan teknik sorular** (ana seçenekten sonra, gerekçesiyle):
- iletilerin biçimi ve boyu: selam (sıra, aralık, tur, maliyet, bit, komşu listesi) ve tur isteği;
- "hemen gönder" olayları ve sıklık sınırı; maliyetin "önemli" değişiminin eşiği (önceki tasarımda %15). B4 Ö-2 ardıl değişimini olay sayıyor. RFC 8966 §3.7.2 maliyeti belirgin değiştirmeyen ardıl değişiminde tetik istemiyor (SHOULD NOT); önceki tasarım da almamıştı (`17` T-17: v0.4.1'de koşu başına 24 122 tetik ilanı);
- kendi kanal kilidimde selam: önceki tasarım kurmuyordu (KK-02 kural 5; B1 Ö-5, B2 Ö-4);
- uyandırmalar (B1 Ö-6, B4 Ö-5); titreşim; komşu listesinin her selamda tam olup olmayacağı (Babel ters yön bildirimini kayıpsız bağda üç selamda bir gönderir).

**Teşhis gerekir mi:** Z1 ölçülmüş koşuldur. Z2'nin ve Z3'ün kazancı ancak A/B ile ölçülür; tasarımda A/B yok. Var olan kanıt kazançlarının üst sınırını veriyor: bitin hızlanması J1'de en çok 0,004; kanal kilidindeki alıcının kaybı J3 ve J4'te birlikte 0,027. Kararın girdisi eksik değil; teşhis önermiyorum.

**Kararım (27 Kasım): Z1, uyarlanır aralık.** Selam aralığı I 0,5 s'den 2 s'ye ikiye katlanır, değişim olayında 0,5 s'ye iner; ilan edilen aralık 1,1 · I.
- Ölçülmüş bütün kanıtın koşulu: B2'nin eşikleri, B3 ve B5 teşhisleri bu zamanlamada ölçüldü; öteki bileşenlerin değerleri buna göre yazıldı.
- Hızlı tepkiyi olaylar verir: geri çekme, isteğe yanıt, maliyetin önemli değişimi, bit değişimi ve yeni komşu selamı 0,5 s içinde öne çeker.
- Bedeli ölçülü: protokolün kendi iletileri kanal süresinin %2,6'sı (Babel-a %11).

Seçilmeyenler: Z2, kazancının üst sınırı küçük (kanal kilidindeki alıcının kaybı J3 ve J4'te 0,027) ve B2'nin eşiklerini sınanmamış bırakırdı; Z3, bitin hızlanması J1'e en çok 0,004 katar; Z4, ilanın ömrü açık dönem kadar uzar.

### 2.7 · B7 · Bekletme ve komut (27 Kasım, kararım)

Kâğıt: `bilesen/B7-BEKLETME-KOMUT.md` (onaylandı, 27 Kasım). Kâğıttaki yapı kararları: bekletme yalnız ardıl yokken, atlama başına en çok 1 s; yol gelince tampon hemen, paket varken 0,5 s'de bir yeniden sorulur; düşen paketin sebebi daha önce yol ya da iz varsa `rota_gecersiz`, yoksa `hedef_yok`; geri iz yalnız daha yeni paket sırasıyla güncellenir, 3 s tazedir; izin gösterdiği komşu son çaredeyse komut yine ona gider, kullanılmazsa beklenir; B7'nin cevabı B5'ten önce hesaplanır.

**Sorun.** B7 iki soruyu cevaplar (§1.4):
- **Bekletme:** yol yokken (B4 açlıkta, ardıl yok) paket ne kadar tutulur; tutulan paket ne zaman yeniden sorulur, ne zaman düşer?
- **Komutun yolu:** geçitten bir İHA'ya giden komut hangi komşuya verilir?

B5'in beklentileri (`bilesen/B5-ILETIM-KARARI.md` §6): açlıkta telemetri için bekletme ya da düşürme kararı (Ö-1); komutun sonraki atlaması (Ö-2); bekletilen paket için uyandırma (Ö-3); B7'nin cevabının B5'ten önce hesaplanması (Ö-4).

Simülatörün çerçevesi (kod, `sim2/kosum/dugum.py`, `sim2/kosum/kontrol.py`):
- `Karar(beklet)` paketi bekletme tamponuna alır. Düğüm başına en çok 64 paket ve paket başına en çok 30 s; ikisi de simülatörün her protokole aynı tavanı. Dolunca en eski düşer (`tampon_asimi`).
- Tampon yalnız protokol bir uyandırma döndürünce yeniden sorulur (K-135). Bekleyenlerin hepsi arayüz kuyruğunun sonuna geçer ve havaya çıkarken yeniden sorulur.
- Paketin yaşı protokole görünmez: doğum anı başlıkta yok, saatler senkron değil (`05` §3.2). Başlığa değer yazılamaz (K-232).
- Geçit, komutun hedefine giden yolu bilmez. Başlığa yalnız kaynak rotası yazılabilir; aradaki düğümler telemetrinin geçtiği yolu başlığa ekleyemez.

**Kanıt** (ölçüldü; bugünkü kodun `eğim0` kolu: atlama başına en çok 1 s bekletme, 0,5 s'de bir yeniden sorma, geri izli komut; ikiz ve birincil, 8 tohum; `arsiv/teshis/faz5_3_b7_bekletme_2026-11-27/bekletme_komut.txt`, B5 teşhisinin ve teşhis (c)'nin kayıtlarından, yeni koşu yok):
- **Açlık:** ikizde koşu başına 18 bölüm, ortalama 1,1 s. Birincilde 103 bölüm, toplam 256 s, ortalama 2,1 s (tohum başına 0,6–4,1 s).
- **Bekletme:** birincilde koşu başına 525 paket bekletiliyor; %38'i yol bulununca gidiyor, %62'si 1 s dolunca düşüyor. İkizde 157 paket, %42 ve %58.
- **Rota yokluğu kaybı:** birincilde açık doğumlularda %3,7, sessiz doğumlularda %4,2, önce evresinde %0,3; ikizde %0,2. Babel'de ~%0,01: Babel bekletmiyor, açlığı tur isteğiyle hemen çözüyor (§2.4).
- **Gecikme:** birincilde bekledikten sonra giden paketler teslimin %2,1'i (0,8–5,3). Bu yüzden gecikmenin p99'u bekletmenin süresine bağlı: 1,08 s (0,18–3,25). Babel'inki 1,31 s; koruma ölçütü p99'un Babel'inkinden büyük olmaması (§1.1). İkizde bu pay %0,65, p99 0,18 s (Babel 0,23). Açık doğumluların %0,47'si 5 s'den geç teslim ediliyor.
- **Bekletmenin süresi:** 1 s ↔ 2 s ikizde ayırt edilemedi (−0,003, 8 tohumun 3'ünde artı; `arsiv/teshis/faz5_3_yeni_cekirdek_2026-11-19/sonuc.md` §5). Birincilde ölçülmedi.
- **Komut:** birincilde koşu başına açıkta ~88 komut doğuyor (paketlerin ~%2,4'ü). Bunların %22'si iletimde kayboluyor; telemetride bu pay %30. Geri izin hazır olma payı önceki sürümde (v0.4.1) ölçüldü: komut kararlarının ikizde %95,7'sinde, birincilde %92,9'unda taze iz vardı (`17` §6).
- **Yeni tasarımda açlığın sıklığı değişir:** B3 eşikle düşürmeyi kaldırdı (açlığın kökü, §2.3). B4'e süre dolmadan istek (kural 4a) ve tercih edilir ilanda istek (kural 10a) eklendi. Bugünkü kodun açlığı bu kurallar olmadan ölçüldü.

**Seçenekler · bekletme** (ana seçenek; karar değil):

| | ne | artı | eksi ve bedel |
|---|---|---|---|
| H1 · kısa bekletme (bugünkü) | yol yokken paket atlama başına en çok 1 s tutulur; yol gelince hemen, yoksa 0,5 s'de bir yeniden sorulur | ölçülmüş; p99 1,08 s, Babel'in altında; telemetride en taze paket değerlidir (`17` T-18) | birincilde bekletilenlerin %62'si düşüyor (açlık ortalama 2,1 s) |
| H2 · uzun bekletme (ör. 3 s) | sınır 3 s | açlığın ortalamasını kapsar; rota yokluğu kaybının (açıkta %3,7) bir kısmını kurtarır | bekledikten sonra gidenler teslimin %2'sinden fazlası olacağı için p99 ~2 s'ye çıkar (kestirim): koruma ölçütü (≤ 1,31 s) bozulur; birkaç röle sırayla tutarsa 5 s'lik tavan aşılır |
| H3 · bekletmesiz (Babel gibi) | yol yoksa paket hemen düşer | en basit; bekleme kuyruğu yok | bugün bekledikten sonra teslim edilenler (birincilde teslimin %2'si, ikizde %0,65) kaybolur |
| H4 · paket başına toplam bütçe | paketin birikmiş beklemesi başlıkta taşınır | uçtan uca gecikme sınırlı kalır | başlığa değer yazılamaz (K-232); elenir |

**Komutun yolu** (tek gerçekçi seçenek): **K1 · geri iz** (bugünkü; `17` T-20, v0.4.1'in V11'i). Her röle, bir düğümün telemetrisini hangi komşudan aldığını hatırlar; o düğüme giden komut o komşuya verilir. Ek ileti gerekmez. İz yalnız daha yeni bir paket sırasıyla güncellendiği için komut döngüye giremez (KK-05 kural 6). Seçilmeyenler:
- kaynak rotası: geçit yolu bilemez (yukarıda);
- her İHA'ya ayrı rota ilanı (Babel gibi her düğüm hedef): selamdaki ilan hedef başına 4 bayt büyür, 40 hedefle selam ~2,5 kat uzar (kestirim); her düğüme rota taşıyan Babel-a'nın kendi iletileri kanal süresinin %11'i;
- sel: her komut bütün ağa yayılır.

**Kâğıda kalan teknik sorular** (ana seçenekten sonra, gerekçesiyle): yeniden sormanın zamanı (yol gelince hemen; tamponda paket varken aralıkla); iz kaydının tazeliği (bugün 3 s) ve izin gösterdiği komşunun B3 durumu (son çaredeyse gönderilip gönderilmeyeceği); düşürmenin sebebi (`rota_gecersiz` ya da `hedef_yok`); komutun bekletilmesi; kayıtların bellek sınırı.

**Teşhis gerekir mi:** H1 ölçülmüş koşuldur. H2'nin kazancı açlık bölümlerinin süre dağılımına bağlı; kayıtta yalnız ortalaması var. Ama H2'nin bedeli (p99) bugünkü kanıtla açık. Kararın girdisi eksik değil; teşhis önermiyorum.

**Kararım (27 Kasım): H1, kısa bekletme; komut için K1, geri iz.** Yol yokken paket atlama başına en çok 1 s tutulur; komut, hedefinin telemetrisini getiren komşuya verilir.
- Gecikme koruma ölçütünü koruyan ve ölçülmüş tek seçenek: bekledikten sonra teslim edilenler birincilde teslimin %2'si olduğu için p99'u bekletmenin süresi belirliyor; bugün 1,08 s, Babel'in 1,31 s'sinin altında.
- Telemetride en taze paket değerlidir; uzun bekletme sahada da değerini yitirmiş paketi taşır.
- Rota yokluğu kaybının asıl çaresi açlığı azaltmaktır: B3 eşikle düşürmeyi kaldırdı, B4'e kural 4a ve 10a eklendi. Etkileri Aşama 4'te ölçülür.

Seçilmeyenler: H2, p99'u ~2 s'ye çıkarıp koruma ölçütünü bozardı (kestirim); H3, bugün bekledikten sonra teslim edilenleri (birincilde teslimin %2'si) kaybettirirdi; H4, başlığa değer yazılamadığı için elendi. Komutun yolunda kaynak rotası, her İHA'ya ayrı rota ilanı ve sel seçilmedi (yukarıda).

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
