# Faz 5-2 · Araştırma notları — kaynak taraması

> 21 Ekim 2026 · Faz 5'in araştırma ve öğrenim aşaması (`v2/12` §1.2, K-252). Amaç: DESPARETE'nin yeni tasarımı için konu konu seçenekler ve kanıt. **Bu notlarda tasarım kararı verilmez;** seçenekler kararlarımın girdisidir.
> Kaynakların doğrulama durumu `v2/02` §F, rapor künyeleri `v2/16` [23] · [36] · [53]–[67], dosyaların SHA-256'ları ve denetimleri `protokol_kaynaklari/README.md`. Dosyalar bu klasörde.
> İşaretler: ✓ açıldı, ilgili bölüm okundu · ↪ yalnız başka bir kaynak üzerinden biliniyor · ○ açılamadı ya da açılmadı.
> Ölçülen DESPARETE ve Babel sayıları: K-244 kuyruğu (1003 · 1004, iki tohum, karar değil; `v2/04` §6).

---

## 0 · Kısa özet

| konu | literatürde başlıca yollar | v0.4.1'in bugünkü hâli | tasarım sorusu |
|---|---|---|---|
| 1 · komşunun varlığı | düzenli selam (ETX, Babel) · uyarlanır selam aralığı · kulak misafiri dinleme | selam yok; yoklama + MAC onayı; yedekler 3 s'de bayat | komşuluk kanıtı nereden gelecek, yedekler nasıl canlı kalacak |
| 2 · bağ kalitesi | iki yönlü teslim oranı (ETX) · donanım ölçüleri (RSSI) yalnız bağlam · düzgünleştirme | yalnız kendi unicast sonuçları; maliyet trafik hacmine bağlı | ölçü kaliteyi mi ölçecek, örnek azlığı nasıl ayrılacak |
| 3 · karıştırmanın yerel kanıtı | teslim oranı ↔ sinyal gücü tutarlılığı · kanal doluluğu · boşta kalma süresi · komşularla karşılaştırma | yok | hangi gözlemler, hangi kuralla; sürekli ↔ reaktif ayrımı |
| 4 · yedek yol, çok yol, çoğaltma | uygulanabilir yedek ardıl (DUAL) · döngüsüz yedek (LFA) · ebeveyn kümesi (RPL) · risk ağırlıklı trafik paylaştırma | ikinci uygulanabilir ardıl varsa geçiş var, yedekler canlı tutulmuyor | yedek önceden hazır mı olacak, trafik bölünecek mi |
| 5 · döngüsüzlük | hedef sıra no + FD (Babel, DSDV) · komşularla ortak yeniden hesap (DUAL) · yükseklik kuralı + veri yolunda döngü sezme (RPL) | Babel ailesi; tur yalnız açlıkta ve geç artıyor | çekirdek korunacak mı, açlık nasıl hızlı çözülecek |
| 6 · bırakma zamanı | histerezis eşiği · düzgünleştirme · rotayı kolay bırakmama | histerezis yok; MAC başarısızlığında hemen onarım | ne kadar inatçı, ne kadar tepkisel |
| 7 · kontrol yükü, bekletme | Trickle (sakinken seyrek, değişimde sık ilan) · sakla-taşı-ilet | sabit 1 s ilan; onarımda alan başına 6 paket | ilan sıklığı, bekletmenin süresi ve sınırı |

---

## 1 · Komşunun varlığı

**Kanıtlar:**
- **ETX** ✓ [De Couto 2003, §3]: her düğüm saniyede bir (τ = 1 s, ±0,1τ titreşim) 134 baytlık yayın yoklaması gönderir; komşular son 10 s'de (w) kaç yoklama aldığını sayar. Yayın yoklaması onaylanmadığı için ölçüm iki yönde ayrı yapılır; düğüm kendi yoklamasında komşularından kaç yoklama aldığını bildirir.
- **Babel** ✓ (kod, RFC 8966 Ek A): 4 s'de bir selam, son 16 selamın geçmişi; ters yönü komşunun IHU iletisi bildirir. Bütün komşular sürekli bilinir; bedel sabit ve küçük.
- **Pasif ↔ etkin ölçüm** ✓ [Cerar 2021, §II]: bağ kalitesi verisi pasif (yalnız var olan trafik), etkin (yoklama) ya da karma toplanır; ölçüm alıcıda, vericide ya da ikisinde yapılır. Yoklama yükü önemliyse yalnız yerelde zaten bulunan veri (pasif) önerilir.
- **Kulak misafiri dinlemenin bir kullanımı** ✓ [Puñal 2014, §II-B]: "boşta kalma süresi", yani komşulardan iki başarılı alım arasındaki en uzun süre, karıştırmanın iyi bir göstergesi çıkmış (bkz. §3).
- **Uyarlanır selam aralığı** ○ [Mahmud & Cho 2019, IEEE Access, açılamadı]: aralık hız, yoğunluk ve menzile göre ayarlanır. Aynı fikrin 2026 sürümü ○ [arXiv 2606.26124].

**Bizim ölçtüğümüz:** v0.4.1'de boşta yoklama kapalı. Denetimde koşu başına ~15 000 komşu silinmesi, 0 boşta yoklama sayıldı (DD-28). Yoklamanın kapatılma gerekçesi eski 1:50 dünyanın kontrol yükü ölçümüydü (K-161); referans dünyada sınanmadı.

**Seçenekler:**
1. **Düzenli selam** (Babel, ETX gibi). Artı: bütün komşular ve iki yönlü kalite her an bilinir. Eksi: sabit kontrol trafiği; selam küçük ve temel hızda gittiği için büyük veri paketinin kaybını olduğundan iyi gösterir (ETX'in kendi bulgusu, §2).
2. **Yalnız kendi trafiğinden kanıt** (v0.4.1). Artı: fazladan mesaj yok. Eksi: kullanılmayan komşu hakkında bilgi yok, yedekler bayatlar.
3. **Kulak misafiri dinleme** (bedava; ilk taslağımda vardı, `arsiv/DESPARETE_TASARIM_PAKETI_v0.1_2026-09-22/DESPARETE – Protokol Taslağı v0.md` §6). Artı: yük yok; RSSI de gelir. Eksi: yalnız komşu → ben yönünü kanıtlar; ben → komşu yönü için ara sıra yoklama gerekir.
4. **Karma:** dinleme + yalnız gerektiğinde yoklama + uyarlanır aralık (Trickle mantığı, §7).

---

## 2 · Bağ kalitesi

**Kanıtlar:**
- **ETX** ✓ [De Couto 2003]: `ETX = 1 / (d_f · d_r)` — ileri yönde verinin, geri yönde onayın ulaşma olasılığı. Yol maliyeti bağların toplamı. 29 düğümlü 802.11b ağında uzun yollarda en az atlama ölçüsüne göre çoğu zaman iki kat ve üstü verim.
  - Makalenin önemli cümlesi (§1): atlama sayısını azaltmak her atlamanın mesafesini büyütür; bu da sinyali zayıflatıp kaybı artırır. Faz 5.0'da başarısız iletimlerin bağları uzundu: ortanca ~11 km, menzil ~9 km (K-243'ten önceki dünya). Ama bu kâhinde de böyleydi; ne kadarının bağ seçiminden geldiği ölçülmedi.
  - Bilinen sınırı (değerlendirme bölümü, Şekil 8): küçük yoklamalar büyük veri paketinden kolay geçtiği için bağ olduğundan iyi görünür. %51 yoklama teslimli bir bağda 1 386 baytlık paketin teslimi ~%1'e iner.
  - Hareketlilikle ilgili (§3): ölçümün doğruluğu ile hareketliliğe tepki hızı arasında bir değiş tokuş var.
- **Donanım ↔ yazılım ölçüleri** ✓ [Cerar 2021, §II, "Input metrics"]: RSSI, SNR gibi donanım ölçüleri telsizden doğrudan gelir ama tek başına kaliteyi vermez; teslim oranına dayalı (yazılım) ölçüler kaliteyi doğrudan ölçer. Derlemenin bulgusu: verinin ön işlemesi ve özellik seçimi, seçilen algoritmadan daha belirleyici.
- **OLSRv2'nin DAT ölçüsü** ✓ (RFC 7779, depoda): paket sıra numaralarından kayıp ve hız; bizim rakibimiz.
- **Yüke bağlı ölçünün tehlikesi** ✓ [Jonglez & Chroboczek 2014, "Stability issues" bölümü]: gecikme ya da yük ölçüye girerse geri besleme döngüsü oluşur. Az yüklü yol seçilir, yüklenir, pahalılaşır, terk edilir; rotalar salınır. Çare: ölçüye üst sınır ("doyma") ve histerezis. Ders 5'te konuştuğumuz "yoğun bağ pahalı olmalı" fikrinin bedeli bu.
- **Sınır değerler** ✓ [RFC 6719 §5]: RPL'nin MRHOF'u ETX'le bağ başına en çok 4 beklenen iletime izin veriyor (MAX_LINK_METRIC 512). Daha kötü bağ hiç kullanılmıyor.

**v0.4.1'in M0.1'iyle karşılaştırma:** M0.1 yalnız kendi unicast sonuçlarını kullanıyor. Örnek sayısı az olunca "belirsizlik" cezası biniyor; yani az trafik taşıyan iyi bir bağ pahalı görünüyor. Kötüleşme ölçüsü ancak saniyede ≥ 8 sonuçlu bağda çalışıyor (`protokoller/desparete_metrik.py`; Ders 5).

**Seçenekler:**
1. **Teslim oranına dayalı ölçü** (ETX benzeri): iki yön, belirli bir pencerede, gerekirse büyük paketle. Örnek kaynağı dinleme, yoklama ya da veri olabilir.
2. **Belirsizliği maliyetten ayırmak:** "az örnek" bir güven ölçüsü olarak tutulur, maliyete eklenmez. Ya da yalnız bağ yeterince ölçülünce aday sayılır.
3. **Bağ için üst sınır:** belli bir kalitenin altındaki bağ (ör. 4'ten çok beklenen iletim) hiç kullanılmaz.
4. **Yük:** maliyete girerse doyma ve histerezisle birlikte; yoksa yalnız eşit maliyetli adaylar arasında ikincil ölçüt olarak (ilk taslağımdaki enerji fikri gibi).

---

## 3 · Karıştırmanın yerel kanıtı

**Kanıtlar:**
- **Puñal vd. 2014** ✓ (802.11, deney; [Puñal 2014, §II]). Standart sürücüden okunabilen altı ölçü:
  - kanal ölçüleri: **gürültü** · **kanal doluluk oranı (CBR)**;
  - başarım ölçüleri: **boşta kalma süresi** (komşulardan iki başarılı alım arasındaki en uzun süre) · **teslim oranı** (bilinen sıklıktaki yoklamalardan);
  - sinyal ölçüleri: **en küçük ve en büyük alınan sinyal gücü**.
  - Bulgular:
    - **Sürekli karıştırıcı** kanal doluluğunu yükseltiyor. Gürültüye ise ancak örneklerin %30'unda yansıyor.
    - **Reaktif karıştırıcı** gürültüyü ve kanal doluluğunu **hiç değiştirmiyor**, çünkü ancak meşru iletim başladıktan sonra yayın yapıyor. Teslim oranı ve boşta kalma süresi her iki karıştırıcıda da güçlü gösterge.
    - **Sinyal gücü** tek başına karıştırmayı göstermez; bağlam verir. Zayıf sinyal karıştırıcı yokken de düşük teslim demektir.
    - **Elle eşik koymak** 802.11'de pratik değil. Xu vd.'nin teslim oranı ↔ sinyal tutarlılık kuralı zor yayılım koşullarında doğru alarmları kaçırıyor (Şekil 10).
    - Eğitilmiş sınıflandırıcı ile komşularla işbirliği ve hareketli ortalama birlikte kullanılınca bütün tespit oranları %95'in üstünde (§IV).
- **Xu vd. 2005** ↪ (Puñal 2014'ün [24]'ü, An & Weber 2018'in [2]'si; özgün makale açılamadı ○): karıştırma saldırılarının teslim oranına ve sinyal gücüne etkisi. Önerilen kural: düşük teslim + güçlü sinyal = karıştırma; düşük teslim + zayıf sinyal = kötü bağ.
- **Reaktif karıştırıcının sezilmesi** ✓ [An & Weber 2018]: dinleme kuralına uyan istasyon kanal meşgulken susar, reaktif karıştırıcı ise tam o anda yayın yapar; erişim noktası bu ihlali sezebilir. Gizli terminaller (birinin duyup ötekinin duymadığı yayınlar) karıştırıcıya "inkâr payı" verir. Tek atlamalı ve erişim noktalı bir model; bizim çok atlamalı sürümüze doğrudan uymaz, fikir olarak yararlı.
- **Wi-Fi karıştırma tespitinin özeti** ✓ [Pirayesh & Zeng 2022, WLAN bölümü, "Jamming Detection Mechanisms", depoda]: Puñal vd.'nin özellikleri ve doğruluğu (sürekli %98,4 · reaktif %94,3).
- **İHA ağında öğrenmeli tespit** ○ [Greco vd. 2021, Applied Soft Computing; sitenin sertifikası geçersiz, dosya alınamadı]: verim, teslim oranı ve RSSI'den özellikler; örnekleme aralığı kısaldıkça doğruluk artıyor (arama özetinden, açılmadı).
- **Yeni derleme (2025)** ✓ [Yang vd. 2025, strateji sınıflandırması]: İHA karıştırmasına karşı altı strateji: karşı koyma (güç) · kaçınma (frekans atlama, yön) · bastırma (süzgeç) · gizlenme (yayılı spektrum) · aldatma · **dolaşma**. Dolaşma ağ katmanının stratejisi: karıştırılan bölgenin etrafından başka yol seçmek. Derlemede tek paragraf ve bir atıfla geçiyor.

**Bizim gözlem sözleşmemizle eşleme** (`v2/05` §3, §6):

| Puñal'in ölçüsü | simülatörde | not |
|---|---|---|
| gürültü | `olculen_gurultu_w` | **kullanılamaz** (K-227: gerçek sürücü 30 s'de bir, ortancayla verir) |
| kanal doluluk oranı | `mesgul_sure_s` (`kanal_dolulugu_ister`) | sürekli karıştırıcıyı ve tıkanıklığı görür, reaktifi görmez |
| boşta kalma süresi | `cerceve_duyuldu` ve `alinan_cerceve`'den | bedava |
| teslim oranı | MAC sonuçları (`iletim_sonucu`) · dinlenen çerçeveler | onaylı unicast'te yeniden deneme sayısı da var (Puñal yayın kullandığı için bunu atmıştı) |
| sinyal gücü | çerçeve başına RSSI (σ 2 dB) | `rssi_olcum_sigma_db` SINANMAMIŞ; okunursa duyarlılığı ölçülür (`v2/04` §9) |
| — | `phy_hata` (CRC hatalı çerçeve) | reaktif karıştırma çerçeveyi ortasından bozarsa artar (gerçek telsiz de sayar) |

**Tasarım için dikkat:**
- Öğrenmeli bir dedektör simülasyonun "karıştırıcı açık" etiketleriyle eğitilirse simülatörün karıştırıcı modelini ezberler; jüri önünde savunması da zordur. Kâhin bilgisinin protokole girmemesi kuralına (`v2/04` §4) dolaylı bir sızıntı olarak bakılabilir. Kurala dayalı, açık bir tutarlılık denetimi bu açıdan daha savunulabilir. Seçim benim.
- Sinyal gücü tek başına yanıltır; teslimle birlikte okunmalı.
- **Komşularla karşılaştırma:** aynı anda birçok komşuya başarısızlık "sorun bende ya da yakınımda" der; tek komşuya başarısızlık "o bağda". Puñal'de işbirliği doğruluğu belirgin artırıyor.
- **Bizim seyrek dünyamızda** bağlar menzil sınırında; teslim karıştırıcısız da düşük. Puñal'in tutarlılık kuralı için "zor yayılım" bulgusu bize de uyar.

---

## 4 · Yedek yol, çok yol ve çoğaltma

**Kanıtlar:**
- **Uygulanabilir yedek** ✓ [RFC 7868 §2.2, §3.2–§3.3, DUAL]: komşunun bildirdiği uzaklık benim en iyi kaydımdan (FD) küçükse o komşu döngüsüz bir yedektir ("feasible successor"). Ardıl kopunca hesap yapmadan hemen ona geçilir. v0.4.1'deki kural aynı; fark, yedeklerin hazır tutulup tutulmaması.
- **Döngüsüz yedek koşulları** ✓ [RFC 5286 §1, §3]:
  - LFA: `D(N,D) < D(N,S) + D(S,D)`.
  - Aşağı akış yolu: `D(N,D) < D(S,D)`. Komşunun uzaklığı benim bugünkü uzaklığımdan küçük; uzaklık-vektöründe bilinen sayılarla denetlenebilir ve mikro döngü yapmaz.
  - Düğüm koruyan yedek: `D(N,D) < D(N,E) + D(E,D)`. Yedeğin yolu ana ardıldan da geçmiyor.
- **Ebeveyn kümesi** ✓ [RFC 6550 §3.5, §8.2.1]: RPL'de her düğüm kökten (bizde geçit) daha düşük yükseklikte birden çok ebeveyn tutabilir. Biri seçilidir, ötekiler hazır yedektir.
- **Karıştırma farkında trafik paylaştırma** ✓ [Tague vd. 2011]:
  - Her bağın paket başarı oranının hem **ortalaması** hem **değişkenliği** üstel hareketli ortalamayla, T saniyelik dönemlerde izlenir ve kaynağa bildirilir.
  - Kaynak trafiği yollar arasında finanstaki portföy seçimi gibi böler: beklenen teslimi artırırken riski (değişkenlik, ortak düğümler) azaltır.
  - Yollar ayrık olmak zorunda değil; ortak düğümler riskin bir parçası. Kaynak rotalamalı ve merkezî hesaplı bir model, fikir olarak yararlı.
- **Atlama başına çok yol** ✓ [Zhao vd. 2026]: her İHA trafiği geçide doğru birden çok komşuya böler. Öğrenmesiz karşılaştırma yöntemleri: eşit bölme ve kapasiteye göre bölme. Önerdikleri yöntem çok etmenli derin öğrenme (MAPPO), bizde kapsam dışı (`v2/01` §3).
- **AOMDV** ✓ (depoda, Marina & Das 2001) ve **JarmRout** ✓ (depoda, Pu 2018): keşifle çok yol; JarmRout her paketi iki yoldan yolluyor ve toplu akışta tıkanıyordu (K-238).
- **İHA komut paketlerini çoğaltma** ○ [PMC 2021, "Enabling Reliable UAV Control by Utilizing Multiple Protocols and Paths for Transmitting Duplicated Control Packets", dosya alınamadı].

**Seçenekler:**
1. **Hazır yedek, çoğaltmasız:** ardıl + 1–2 uygulanabilir yedek canlı tutulur (yoklama ya da dinlemeyle). Kopuşta anında geçilir. v0.4.1'in `hedefli_canlilik` seçeneği bunun bir hâli; eski dünyada reddedilmişti (K-165, DD-28).
2. **Atlama başına bölme:** trafik birden çok uygulanabilir komşuya bölünür. Artı: tek bağın kopması paketlerin yalnız bir kısmını vurur. Eksi: kötü bağa da trafik gider.
3. **Seçici çoğaltma** (ilk tasarımımdaki CRISIS/PROTECT): yalnız kanıt kötüyse, sınırlı bütçeyle, farklı ilk atlamalara kopya. Simülatörde kopya defteri hazır (K-231). JarmRout'un dersi: her pakete kopya toplu akışta kanalı boğar.
4. **Yedeklerin mekânsal ayrışması:** ortak bir karıştırıcıya aynı anda yakalanmamaları için. Konum ancak ödenmiş mesajla gelir (`v2/05` §3.3); Tague'nin "ortak düğüm riski" fikri.

---

## 5 · Döngüsüzlük

Üç yöntem ailesi:

| aile | nasıl | açlık / tıkanma nasıl çözülür | kaynak |
|---|---|---|---|
| **hedef sıra no + FD** | komşunun ilanı ya daha yeni sıradan ya da FD'den küçükse kabul | kaynağa sıra isteği; kaynak sıra no'yu artırır | RFC 8966 ✓ · DSDV ↪ [De Couto 2003 §4] · v0.4.1 |
| **komşularla ortak hesap (DUAL)** | aynı FD kuralı; sıra no yok | yol "etkin" duruma geçer, komşulara Query/Reply; herkes yanıtlayınca FD sıfırlanır; uzun sürerse "stuck in active" | RFC 7868 ✓ |
| **yükseklik kuralı + veri yolunda sezme (RPL)** | ebeveynin yüksekliği benimkinden küçük olmalı; yerel onarımda sınırlı yükselme (MaxRankIncrease) | kök sürüm numarasını artırır (genel onarım); paket başlığındaki gönderen yüksekliği yanlış yönü gösterirse paket işaretlenir, ikincisinde düşer ve onarım tetiklenir | RFC 6550 ✓ |

**Notlar:**
- **Babel uygulanamaz güncellemede seçili rotayı bırakmıyor** ✓ (kod, RFC 8966 §3.5.3). Aynı kaynaktan gelen güncelleme yok sayılıyor, hemen tek alıcılı sıra isteği gidiyor; rota tümden kaybolursa çoklu yayın, üç kez yinelenen istek gidiyor. v0.4.1'de aynı durumda alan onarıma giriyor; tur isteği ancak 6 s'lik onarım bitince ve yalnız kendi paketiyle çıkıyor. Tur yalnız açlık isteğiyle artıyor.
- **RPL'nin felsefesi farklı** ✓ [RFC 6550 §3.7]: döngüsüzlüğü garanti etmez. Döngüyü önlemeye çalışır, olursa veri yolunda yakalar ve onarır. Karşılığında daha esnek ebeveyn seçimi.
- **Açgözlülük uyarısı** ✓ [RFC 6550 §3.7.1]: daha çok ebeveyn için derine inen düğümler birbirini besleyen kararsızlık yaratır; RPL daha derindeki düğümün ilanını işlemeyi yerel onarıma kısıtlar.
- **Tek hedefe toplama** (yere toplama) RPL'nin de asıl işi. DESPARETE'nin geçit alanı RPL'nin kökten kurulan ağacına kavramca yakın. Aşağı yönlü komut için RPL'de ayrı bir ileti var (DAO, §9); v0.4.1'in geri izi (V11) ek ileti kullanmıyor.

---

## 6 · Bırakma zamanı: kararlılık ↔ tepkisellik

**Kanıtlar:**
- **Rota çırpınması** ✓ [Ramachandran vd. 2007, iki gerçek mesh ağı]:
  - baskın rota zamanın ancak %57–65'inde kullanılıyor;
  - değişimlerin çoğu bir dakika sürüyor;
  - değişimlerin %27–50'si %10'dan az iyileşme getiriyor;
  - %10 eşikli ya da süre eşikli bir histerezis baskın rotanın ömrünü 4–5 kat uzatıyor.
  - Ağlar durağan; zaman ölçeği dakika, bizimki saniye.
- **Babel'in seçimi** ✓ (kod; [Jonglez & Chroboczek 2014, "Hysteresis" bölümü]): her rota için ilan edilen metrik ve 4 s zaman sabitiyle düzgünleştirilmiş metrik tutuluyor. Başka bir rotaya ancak ikisi birden daha iyiyse geçiliyor.
- **MRHOF** ✓ [RFC 6719]: yeni yola ancak bugünkünden en az bir eşik kadar iyiyse geçilir. ETX'le önerilen eşik 192, yani en az 1,5 daha az beklenen iletim.
- **Babel MAC başarısızlığını kullanmıyor** ✓ (`protokoller/babel.py`, beyan tablosu), rotası 56 s yaşıyor. Karıştırıcı 15 s sonra susunca rota hazır. v0.4.1'de MAC başarısızlığı komşuyu hemen "şüpheli" yapıyor ve onarım başlıyor.
- **ETX'in uyarısı** ✓ [De Couto 2003, §3]: ölçüm doğruluğu ile hareketliliğe tepki hızı arasında değiş tokuş.

**Tasarım sorusu:** 15 s açık / 15 s kapalı (ve 10/20) bir karıştırıcıda:
- bağı hemen bırakıp başka yoldan gitmek mi;
- beklemek mi;
- "bu bağ az önce karıştırılmıştı" hafızasıyla yedeği hazır tutup karıştırıcı susunca eski yola dönmek mi?

Zaman sabitleri tek bir çizelgeye ayarlanmamalı; dayanıklılık hücresi bunun için var (`v2/06` §0.4.5).

---

## 7 · Kontrol yükü, bekletme ve gecikme

- **Trickle** ✓ [RFC 6206 §4.2]: ilan aralığı her dönemde iki katına çıkar (en çok Imax). Tutarsız bir şey duyulunca en küçüğe (Imin) iner. Komşulardan yeterince tutarlı ilan duyulmuşsa (k) kendi ilanını atlar. Sonuç: ağ sakinken seyrek, değişince sık ilan. RPL ilanlarını böyle zamanlıyor (RFC 6550 §8.3). v0.4.1 sabit 1 s'de bir ilan ediyor.
- **Sakla-taşı-ilet** ○ (yalnız arama özetleri): bağlantının sık koptuğu ağlarda paket bir süre saklanıp sonra iletilir. Bizde karıştırıcı 15 s sonra susuyor.
- **Bekletmenin iki yüzü** (K-242, K-246):
  - `PDR_açık`, açık dönemde doğup sonra teslim edilen paketi de sayar; bekletme bu yüzden ödüllendirilir.
  - Telemetri 5 s'den geç gelirse değeri azalır; tavanlı ikincil metrik bunu ölçer.
  - v0.4.1'in p99 gecikmesi birincil hücrede 4,3–4,7 s, Babel'inki 0,3–0,8 s.

---

## 8 · Babel ↔ DESPARETE v0.4.1 (kod üzerinden)

| | Babel-a | DESPARETE v0.4.1 |
|---|---|---|
| hedefler | her düğüm kendi önekini duyurur | yalnız geçit alanı |
| komşuluk | selam 4 s, 16'lık geçmiş; IHU 12 s | selam yok; yoklama + MAC onayı; aktiflik 3 s, silinme 5 s |
| bağ maliyeti | ETX, iki yön, veri trafiğinden bağımsız | M0.1, yalnız kendi unicast sonuçları; az örnekte belirsizlik cezası |
| yedekler | her komşunun rotası tabloda, rota ömrü 56 s | yalnız aktif komşunun ilanı; yedekler bayatlıyor |
| MAC başarısızlığı | kullanılmaz | komşu şüpheli → onarım |
| ardıl seçimi | düzgünleştirme (4 s) + histerezis | her hesapta en küçük maliyet, histerezis yok |
| seçili rotaya uygulanamaz güncelleme | yok sayılır, rota korunur, hemen sıra isteği | ardıl aday olmaktan çıkar → onarım |
| açlık | hemen çoklu yayın sıra isteği, 3 yineleme | ≥ 6 s sonra, yalnız kendi paketiyle tur isteği |
| tetik ilanı | eşikli (küçük farklar gönderilmez) | her ardıl ve potansiyel değişiminde (alan başına ≤ 5/s) |
| bekletme | yok | onarımda alan başına 6 paket, en çok 6 s |
| ölçülen (1003 · 1004) | ikiz 0,945 · 0,952 · birincil 0,547 · 0,787 | ikiz 0,757 · 0,786 · birincil 0,518 · 0,603 |

Babel'in üstünlüğünün hangi satırdan geldiği **ölçülmedi.** Tablo, teşhis ölçümünün hangi sorulara bakacağını gösteriyor (§10).

**Gerçek ağda Babel her zaman en iyisi değil** ✓ [Turlykozhayeva vd. 2024]: 11 Raspberry Pi'lik deneyde ağ büyüdükçe teslimi en çok Babel kaybetti, açık havada en yüksek bant genişliği OLSR'deydi. Sıralama düzeneğe bağlı; bizim sonucumuz yalnız bizim hücrelerimiz için geçerli.

---

## 9 · Kapsam dışı ya da zayıf kalanlar

- **Derin ve çok etmenli pekiştirmeli öğrenmeye dayalı yönlendirme** [Zhao 2026; arXiv 2601.10299 ○]: güncel İHA çok yollu yönlendirme çalışmalarının çoğu bu yolda. `v2/01` §3 gereği yöntemleri alınmaz; atlama başına bölme fikri ve öğrenmesiz karşılaştırma yöntemleri alınabilir.
- **Öğrenmeli karıştırma dedektörleri** [Puñal 2014, Greco 2021]: göstergeler alınabilir; eğitilmiş sınıflandırıcı için §3'teki dikkat.
- **Fiziksel katman çözümleri** (frekans atlama, yön, süzgeç) [Yang 2025, Pirayesh & Zeng 2022]: kapsam dışı (`v2/01` §3).
- **Fırsatçı yönlendirme** (paketi duyan herhangi bir komşu iletir; ExOR) ○: MIT sunucusuna ulaşılamadı. Yeni bir aday konu.

---

## 10 · Sonraki adım

- **Teşhis ölçümleri** (uzun koşuya izin verilince; her biri önceden yazılı beklentiyle, geliştirme tohumlarında):
  - (a) ikiz ve birincil hücrede DESPARETE ↔ Babel kayıp anatomisi: §8'deki farkın hangi satırdan geldiği;
  - (b) v0.4.1'in `hedefli_canlilik` ve `onarim_edinimi` seçenekleri ikizde: §1 ve §5'in payı;
  - (c) rakiplerin 1003–1010'da üç geliştirme hücresindeki çizgisi;
  - (d) aday: karıştırılan ve karıştırılmayan bölgelerde kanal doluluğu, `phy_hata`, RSSI ve MAC sonuçlarının nasıl davrandığı. §3'ün tasarımına doğrudan girdi; yeni bir kayıt aracı gerektirebilir.
- **Açılamayanlar:** Xu vd. 2005 (ACM; açık kopya yok) · Greco vd. 2021 (sertifika) · Mahmud & Cho 2019 · PMC 2021 · ExOR. Rapora girmeden önce açılmalı ya da "…'de aktarıldığı gibi" diye anılmalı (`v2/16` kuralı).

---

## Kaynaklar (bu klasördeki dosyalar)

| kısa ad | dosya | `v2/16` |
|---|---|---|
| De Couto 2003 | `decouto_2003_etx.pdf` | [36] |
| Puñal 2014 | `punal_2014_wifi_jamming_detection.pdf` | [23] |
| Tague 2011 | `tague_2011_jamming_aware_traffic_allocation.pdf` | [53] |
| Ramachandran 2007 | `ramachandran_2007_routing_stability.pdf` | [54] |
| Jonglez & Chroboczek 2014 | `jonglez_chroboczek_2014_delay_metric.pdf` | [55] |
| An & Weber 2018 | `an_weber_2018_reactive_jamming.pdf` | [56] |
| Cerar 2021 | `cerar_2021_lqe_survey.pdf` | [57] |
| Turlykozhayeva 2024 | `telecom_2024_olsr_batman_babel.pdf` | [58] |
| Yang 2025 | `yang_2025_uav_antijamming_survey.pdf` | [59] |
| Zhao 2026 | `zhao_2026_perhop_multipath_uav.pdf` | [60] |
| RFC 5286 (LFA) | `rfc5286_lfa.txt` | [61] |
| RFC 6206 (Trickle) | `rfc6206_trickle.txt` | [62] |
| RFC 6550 (RPL) | `rfc6550_rpl.txt` | [63] |
| RFC 6719 (MRHOF) | `rfc6719_mrhof.txt` | [64] |
| RFC 7868 (EIGRP/DUAL) | `rfc7868_eigrp_dual.txt` | [65] |
