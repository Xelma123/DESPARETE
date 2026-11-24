# Faz 5-3 · B2 teşhisi — karıştırma işaretleri, bizim çekirdeğimizin trafiğinde — beklenti

> 24 Kasım 2026 · `v2/18` §2.2'nin teşhis ölçümü (kararım: A, alıcı ve gönderici birlikte; kurallar ölçümle seçilir). Bu dosya koşudan ve dumandan önce commit'lenir; öngörüler referans dünyada hiçbir koşu yapılmadan yazıldı. Sonuç ayrı `sonuc.md`ye yazılır, bu dosyaya dokunulmaz.
>
> Alet: `olcum.py` (kaydedici) · `isaret.py` (saf işlevler; sınaması `sinama/saf.py`, 54 denetim) · `kosu.sh` · karar hesabı `sonuc_hesap.py` (bu kuralın kodu; koşudan önce yazıldı).

## Amaç

B2'nin kâğıdının üç girdisini ölçmek:
1. Girişim bölgesindeki düğümün kendini tanıyacağı birleşik kural ve eşikleri.
2. Göndericinin karıştırılan alıcıyı kendi gözleminden ne kadar hızlı ve güvenilir tanıdığı.
3. Kalabalığın yanlış alarmı.

Bunlar teşhis (d)'nin açık bıraktıklarıdır (`17` §7 madde 6, 7, 9; `18` §1.3 "bilmiyoruz" 1, 4). Teşhis (d) Babel'in trafiğinde ve yalnız işaret başına dağılımla ölçülmüştü; birleşik kuralların başarısı oradan hesaplanamıyordu.

## Sorular

- **S1 · kanal kilidi, kendi durumum:** kanal meşgul payı eşiği (m ≥ θ) bizim trafiğimizde ne kadar yanlış alarm veriyor, kanal kilidindeki düğümü ne kadar hızlı yakalıyor?
- **S2 · girişim, kendi durumum:** birleşik kuralların (G, GM) en iyisi hangisi; yakalama, gecikme, yanlış alarm ve karıştırma bitince çıkış ne?
- **S3 · kanal kilidindeki alıcı, göndericide:** 27 bağ kuralından hangisi, ne kadar hızlı ve ne kadar yanlış alarmla?
- **S4 · girişimdeki alıcı, göndericide:** aynı soru.
- **S5 · kalabalık:** seçilen girişim kuralının yanlış alarmı düğümün yüküyle nasıl değişiyor?
- **S6 · bitin ulaşması:** girişim bölgesindeki düğümün açık dönemdeki selamları komşularına ne kadar ulaşıyor (bit bu selamla gidecek)?
- **S7 · genelleme:** seçilen kurallar sabit yer karıştırıcılı bir ailede (cephe hattı) de çalışıyor mu?

## Düzen

- **Kol:** `desparete5_cekirdek`: karıştırmaya karşı mekanizmalar kapalı; geri gönderme yasağı ve sınırlı yükselme açık. Döngü kuralları ölçümünün `geri_sinir` kolunun aynısı. Sebep: işaretler trafiğe bağlıdır. Yeni tasarımın selamı (B1) bugünkü selamla aynı biçimde ve aralıkta gidecek (0,5–2 s); en yakın trafik bu kolun trafiği. Bugünkü kod döngü kuralları ölçümünün koduyla aynı (`git diff 9920d2e` simülatörde, protokollerde, araçlarda boş).
- **Hücreler** (`formasyon · yere_toplama`, tam pencere, 350 s):
  - **ikiz:** karıştırıcısız, hayalet çizelge 10:20;
  - **birincil:** `derin_sizma`, 15 s açık · 15 s sessiz;
  - **dayanıklılık:** `derin_sizma`, 10 s açık · 20 s sessiz;
  - **cephe:** `cephe_hatti`, 3 sabit yer karıştırıcısı, sürekli yayın. 150 s'de açılır, sonuna kadar açık kalır. Yalnız genellemenin denetimi (S7); kural seçimine girmez.
- **Tohumlar:** 1003–1010. **Seçim yarısı 1003–1006, doğrulama yarısı 1007–1010.** Kurallar seçim yarısında seçilir; hüküm doğrulama yarısındaki sayılarla verilir. Sebep: 295 kurallık ızgarada en iyiyi seçmek aynı veride iyimser sonuç verir.
- **Koşu:** dondurulmuş kopyadan, hücre başına bir adım (8 tohum, 8 işçi). Her koşu kayıp anatomisi aletinin işçisiyle yapılır. Kaydedici yalnız okuyan sarmalayıcılar takar. Tek ek: düğümlerin kanal meşgul sayacı açılır; çekirdek onu okumaz (`karistirma_durumu` kapalıyken kendi durum modülü hemen döner). Teşhis (d) Babel'de aynı yolla birebirdi.

## Tanımlar

**Birimler ve etiketler:**
- **Düğüm-saniye:** ölçüm penceresinde (50–320 s) bir düğümün bir saniyesi.
- **Evre** (saniyenin): önce · açık · sessiz · ikiz. İçinde açılma ya da kapanma anı olan saniye "geçiş"tir ve sayılmaz. Açık dönemin uçları ikiye bölmeyle bulunur (teşhis (d)'nin yolu).
- **Etki alanı** (düğümün, o saniyenin ortasında; kayıp anatomisinin tanımı): karıştırıcı açık olsaydı alınacak ortalama güç ≥ −76 dBm ise **E** (kanal kilidi), gürültü tabanının üstündeyse **G** (girişim), değilse **U** (uzak). Bu etiketler protokole girmez, yalnız değerlendirmede kullanılır (`05` §8).
- **Temiz sınıflar** (yanlış alarmın sayıldığı yer): ikiz · önce · sessiz · açık dönemde uzak alan.

**İşaretler** (protokolün görebildiği, saniye başına):
- **m:** kanal meşgul payı (`mesgul_sure_s`'in farkı).
- **c:** çözülen çerçeve sayısı (`alinan_cerceve`).
- **c̄:** son 30 işaretsiz saniyenin c ortalaması. İşaretsiz: ne m ≥ 0,62 ne kuralın kendi işareti (önceki KK-03 kural 1, 3).
- **s:** selam kaybı payı. Tanıdık komşuların (son 16 s'de gerçek selamı alınmış) son 4 s'deki B1 örneklerinde sıfırların payı. B1'in sayımı (`v2/bilesen/B1-KOMSU-VE-BAG.md` kural 4–6), saniye sonundaki o anki görünümle (geri alma sonradan sıfır silebilir).
- **M:** o saniyede en az 2 ayrı komşuya başarısız deneme ve başarısız deneme payı ≥ 0,5.

**Kendi durumum kuralları** (ızgara 295 kural, `isaret.izgara`):
- **ED(θ):** m ≥ θ; θ ∈ {0,50 · 0,55 · 0,60 · 0,62 · 0,65 · 0,70 · 0,80}; giriş ve çıkış 1 s.
- **G(α, β, giriş, çıkış):** işaret c < α·c̄ ve s ≥ β.
- **GM(α, β, giriş, çıkış):** C (c < α·c̄), S (s ≥ β), M üçünden en az ikisi.
- G ve GM'de α ∈ {0,4 · 0,5 · 0,6 · 0,7}, β ∈ {0,5 · 0,6 · 0,7 · 0,8}. Giriş: art arda işaretli saniye sayısı ∈ {1, 2, 3}; çıkış: art arda işaretsiz saniye sayısı ∈ {1, 2, 3}.
- Önceki KK-03'ün kuralı G(0,5, 0,6, 2, 3) ızgaradadır; kıyas için ayrıca raporlanır.

**Bağ kuralları** (göndericide, alıcı j için; 27 kural, `isaret.KURALLAR`). Kural, koşulunun art arda sağlandığı dizinin eşiğe ulaştığı anda bir kez ateşlenir:
- **VAZn:** n art arda vazgeçme (n = 1, 2, 3).
- **DENaxr:** art arda r çerçevenin her biri en az a deneme harcadı (a ∈ {4, 5, 6, 7}, r ∈ {1, 2, 3}; vazgeçme 7 denemedir).
- **BIRa_xxr:** art arda r çerçevede hem en az a deneme hem de "j'nin selamı gecikti": j'den son selam x × j'nin ilan ettiği aralıktan eski (a ∈ {4, 6}, x ∈ {1,0 · 1,5}, r ∈ {1, 2}).
- **SESn:** j'nin B1 örneklerinin sonunda ardışık n sıfır (n = 2, 3, 4).
- **SESu:** n, önceki KK-03 kural 6'nın uyarlanır k'sı.

**Değerlendirme birimleri:**
- **Düğüm-dönem:** her açık dönem ve o dönemin ortasında E ya da G alanında olan düğüm.
- **Veri taşıyan bağ-dönem:** göndericinin dönemden önceki 10 s'de alıcıya en az bir başarılı çerçevesi olan ve dönem içinde çerçeve gönderdiği bağ; alıcının alanı dönemin ortasında E ya da G. Bütün bağ kuralları bu birimlerde karşılaştırılır. Göndericinin dönemden önceki hızı > 1,5 çerçeve/s ise "röle", değilse "yaprak benzeri".
- **Kullanılabilir bağ:** sessizlikten önceki `d_r` ≥ 0,5. Sessizlik kurallarının yanlış alarmı bu bağların bağ-saniyeleriyle bölünür.

**Ölçüler:**
- **Erken yakalama:** karıştırma başladıktan sonra en geç 3 s içinde yakalanan birimlerin payı. Kendi durumumda karar saniye sonunda verilir, en erken gecikme 1 s'dir.
- **Dönem içinde yakalama:** dönem bitmeden yakalananların payı.
- **Gecikme ortancası:** yakalananların gecikmesinin ortancası.
- **Kapsama:** G alanındaki açık dönem düğüm-saniyelerinin durumda geçen payı.
- **Çıkış gecikmesi:** dönem bittikten sonra durumdan çıkma süresi; sonraki dönem başlamadan çıkılmayan pay ayrıca verilir.
- **Yanlış alarm:**
  - kendi durumumda: temiz sınıfın düğüm-saniyelerinden durumda geçen pay;
  - bağ kurallarında: temiz sınıfta (alıcısı karıştırılmayan) ateşlenme sayısı, veri kurallarında 1000 çerçevede, sessizlik kurallarında 1000 kullanılabilir bağ-saniyesinde.

## Karar kuralı (`sonuc_hesap.py`)

**K0 · Geçerlilik.** 32 koşu kayıtta, hepsi geçerli, iç denetimler geçti. Birebirlik: ikiz ve birincil satırları döngü kuralları ölçümünün `geri_sinir` satırlarıyla, aynı tohumda, bütün alanlarda (PDR, pencere PDR'si, üretilen, teslim, simülatör sayaçları, protokolün sayaçları) aynı. Tutmazsa kaydedici davranışı değiştirmiştir: tablolar kullanılmaz, sebep ölçülür.

**K1 · Kanal kilidi (S1).**
- Seçim: seçim yarısında ikizde yanlış alarmı ≤ %0,05 olan en küçük θ.
- Hüküm "tutar" ⇔ doğrulama yarısında ikizde yanlış alarm ≤ %0,1 ve E alanındaki düğüm-dönemlerde erken yakalama ≥ 0,80 (birincil ve dayanıklılık birlikte).

**K2 · Girişim (S2).**
- Seçim, seçim yarısında:
  - aday: ikizde ve önce evresinde ≤ %0,1, açık dönemde uzak alanda ≤ %1 yanlış alarm (önce ve uzak: birincil ve dayanıklılık birlikte);
  - adaylar arasında G alanındaki düğüm-dönemlerde erken yakalaması en yüksek olan;
  - 0,005 içinde eşitlikte sırasıyla: dönem içinde yakalama yüksek, ikizde yanlış alarm düşük, G (GM'den önce), giriş büyük, çıkış küçük.
- Hüküm "girişim kuralı var" ⇔ doğrulama yarısında ikizde ≤ %0,2 ve uzak alanda ≤ %2 yanlış alarm, birincilde ve dayanıklılıkta ayrı ayrı erken yakalama ≥ 0,25.

**K3 · Kanal kilidindeki alıcı (S3) · K4 · Girişimdeki alıcı (S4).**
- Seçim, seçim yarısında: ikizde ve önce evresinde ≤ binde 1 yanlış alarm veren kurallar arasında, alanı E (K3) ya da G (K4) olan veri taşıyan bağ-dönemlerde erken yakalaması en yüksek olan. 0,005 içinde eşitlikte: dönem içinde yakalama, sonra ikizde yanlış alarm, sonra kuralın sırası.
- Hüküm "göndericide tanınır" ⇔ doğrulama yarısında ikizde ≤ binde 2 ve erken yakalama ≥ 0,50 (K3) / ≥ 0,30 (K4).

**K5 · Kalabalık (S5).** Seçilen girişim kuralının (yoksa önceki KK-03 kuralının) ikizdeki yanlış alarmı, düğüm-saniyelerin meşgul payına göre üç eşit parçada. En yüklü üçte birde > %0,3 ise "yük koruması gerekir".

**K6 · Bitin ulaşması (S6).** Betimleyici: alıcının alanına göre ulaşan selam payı.

**K7 · Genelleme (S7).** Seçilen kuralların cephe hattında (bütün tohumlar) erken yakalaması birincilinkinin yarısından azsa "genellemede düşüyor"; cephe hattının önce evresindeki yanlış alarm ayrıca verilir.

**Hükmün tasarıma etkisi:**
- **K2 "var":** A, seçilen kural ve eşiklerle; B2'nin kâğıdı bu kuralla yazılır.
- **K2 "yok":** girişimde bit gönderilmez, A'nın alıcı tarafı düşer (B'ye dönüş, `18` §2.2). Kendi durumum yalnız kendi MAC sonuçlarımı yorumlamak ve B1'in hariç aralığını vermek için kalır; eşikleri daha gevşek seçilebilir, çünkü yanlış alarmı komşulara yayılmaz.
- **K1 "tutmaz":** kanal kilidi için başka işaret aranır (çözülen çerçeve, CRC hatası; teşhis (d)'de ikisi de güçlüydü).
- **K3 / K4 "tanınır":** göndericinin kuralı ve eşiği B2'ye girer. "Tanınmaz": o alan için göndericinin kanıtı yalnız geç gelen işaretlerle kalır, bitin önemi artar.
- **K5 "gerekir":** B2'nin girişim kuralına bir yük koşulu eklenir.
- **K7 "düşüyor":** eşikler cephe hattıyla birlikte yeniden düşünülür ya da B2'nin kâğıdında kapsam sınırı olarak yazılır.

**Eşiklerin gerekçesi:**
- **%0,1 düğüm-saniye** (girişim): ikiz koşusunda 40 düğüm × 270 s'de koşu başına ~11 yanlış alarm saniyesi, yaklaşık 3–4 bölüm. Her bölüm o düğümün komşularına onu birkaç saniye bıraktırır.
- **%0,05** (kanal kilidi): teşhis (d)'de bu kuralın yanlış alarmı %0,035 ölçülmüştü; tek saniyelik bir işarete daha sıkı bir sınır uygun.
- **Uzak alanda %1:** bu düğümlerin karıştırılan komşuları gerçekten susuyor, işaretleri bir ölçüde hareketlenir (teşhis (d): uzak alanda çözülen çerçeve düşüyor). Ama orada "karıştırılıyorum" demek karıştırma bölgesinin dışındaki sağlam bir röleyi komşularına bıraktırır.
- **Binde 1** (bağ): ikizde veri taşıyan bir bağda saniyede ~1–5 çerçeve var; binde 1, koşu başına bağ başına ~1 yanlış bırakma eder.
- **3 s:** birincilde açık dönem 15 s, dayanıklılıkta 10 s; 3 s içinde yakalamak dönemin en az %70'ini kurtarır.
- **0,25 · 0,30 · 0,50 · 0,80:** kuralın kullanılmaya değer sayılacağı en düşük pay. Gerçek katkı Aşama 4'te ablasyonla ölçülür; burada yalnız kullanılabilir mi diye bakılır. Kanal kilidinde daha yüksek, çünkü o düğüm kendini tek saniyede tanır (teşhis (d)) ve göndericide güçlü iz bırakır (çerçeve başına 6,3 deneme).
- **Doğrulamada sınırlar seçimdekinin iki katı:** yarım örneklemde sayısal oynamaya pay.

## Öngörüler (referans dünyada hiçbir koşudan önce)

Gerekçe: teşhis (d)'nin dağılımları (Babel'in trafiği) ve bizim trafiğimizin farkı. Bizde kontrol yükü Babel'inkinin üçte biri (%6 ↔ %15); selam daha sık (0,5–2 s ↔ 4 s), dolayısıyla 4 s'lik pencerede daha çok örnek ve daha az gürültülü s.

| # | öngörü |
|---|---|
| 1 | K0: birebirlik tutar, iç denetimler geçer |
| 2 | S1: seçilen θ 0,50–0,62; doğrulamada ikizde yanlış alarm ≤ %0,05; E alanında erken yakalama 0,85–1,00, gecikme ortancası 1,0–1,5 s; K1 "tutar" |
| 3 | S2: ikizde s'nin ortalaması 0,30–0,50 |
| 4 | S2: önceki KK-03 kuralı (G 0,5 · 0,6 · 2 · 3) ikizde yanlış alarm %0,1–%1 |
| 5 | S2: seçim yarısında yanlış alarm sınırlarını geçen kural sayısı ≥ 20 |
| 6 | S2: seçilen kuralın girişi 2 ya da 3 s |
| 7 | S2: seçilen kuralın doğrulamada erken yakalaması birincilde 0,25–0,55, dayanıklılıkta 0,20–0,50; dönem içinde yakalama 0,50–0,85; gecikme ortancası 2–4 s; çıkış ortancası 2–5 s; kapsama 0,30–0,65 |
| 8 | K2: en olası "girişim kuralı var"; ikinci olası dayanıklılıkta 0,25'in altında kalıp "yok" |
| 9 | S3: tek çerçeveli deneme kuralları hızlı ama yanlış alarmı yüksek: DEN6x1 ikizde binde 20–60; DEN6x2 binde 1–5; DEN6x3 binde 0,1–1 |
| 10 | S3: VAZ3 ikizde binde 0,5'in altında ama yavaş, erken yakalaması 0,10–0,35; SES3'ün erken yakalaması ≤ 0,15 |
| 11 | S3: seçilen kural DEN6x3, DEN7x2 ya da BIR6_15x2 türünden (art arda en az 2 çerçeve); doğrulamada erken yakalama 0,40–0,75; röle bağlarında yaprak benzerinden yüksek |
| 12 | K3: "tanınır" ile "tanınmaz" arasında belirsiz (0,50 sınırı çevresinde) |
| 13 | S4: seçilen kuralın erken yakalaması 0,10–0,35; K4 en olası "tanınmaz" |
| 14 | S5: seçilen kuralın ikizdeki yanlış alarmlarının yarısından fazlası en yüklü üçte birde; K5 en olası "gerekmez" |
| 15 | S6: G alanındaki düğümün selamlarının uzak komşulara ulaşan payı 0,50–0,85; G komşulara 0,10–0,40; E komşulara ≤ 0,10 |
| 16 | S7: kanal kilidi kuralı cephe hattında da tutar; girişim kuralının cephe hattındaki erken yakalaması birincilinkinin 0,5–1,0 katı; sürekli yayında çıkılmayan pay yüksek |

## Aletin denetimi

- **Saf işlevler:** `sinama/saf.py`, 54 denetim (B1 sayımı: düzenli selam, zaman aşımı, ileri sarma, geri alma, yeniden başlama, silme; selam kaybı payı; uyarlanır k; veri ve sessizlik kuralları; girişim işareti ve c̄; giriş ve çıkış; dönem ölçüsü; ızgara).
- **Mekanik denetim:** öngörüler yazıldıktan sonra, ölçülen tohumların dışındaki 1001 tohumuyla, kısa pencerede, dört hücrede bir kez koşulur. Bakılan tek şey kaydedicinin iç denetimlerinin geçmesi ve karar hesabının hatasız bitmesidir; sayılar okunmaz. Bu, kodun commit'ten önce çalıştığını gösterir.
- **Duman** (bu commit'ten sonra): kısa pencere, tohum 1003, dört hücre, kaydediciyle ve kaydedicisiz (birebir olmalı); ikiz ve birincil ayrıca döngü kuralları ölçümünün duman satırıyla birebir olmalı. Duman notu ayrı commit'le girer; karar girdisi değildir.

## Süre ve kayıt

- **Adım başına** (bir hücre, 8 tohum, 8 işçi): ~1–2 saat. Dayanak: döngü kuralları ölçümünde aynı çekirdeğin adımları 51–69 dk sürdü. Mekanik denetimde kaydedici kısa birincil koşusunu %17 uzattı (283 ↔ 241 s, iki süreç yan yana); cephe hattının kısa koşusu öteki hücrelerinkinden ~%30–50 uzun sürdü.
- **Toplam:** ~4,5–6,5 saat. Her adım 8 saatin altında; iki ağır iş birlikte koşulmaz.
- **Duman:** ~15 dk (dört hücre kaydediciyle, sonra dört hücre kaydedicisiz, her biri yan yana).
- **Kayıt:** hücre başına ~3–5 MB (düğüm-saniye dizileri); depoda sıkıştırılarak tutulur.

## Sınırlar

- İşaretler bugünkü çekirdeğin trafiğinde ölçülür; yeni tasarımın yolu (B4) ve iletimi (B5) trafiği değiştirebilir. Seçilen eşikler B2'nin kâğıdında başlangıç değeridir, Aşama 4'te yeniden bakılır.
- Yalnız sürekli karıştırıcı (`derin_sizma`, `cephe_hatti`). Kanal doluluğu tepkisel karıştırıcıyı görmez (Puñal 2014); öteki sınıflar ölçülmez.
- B1'in silmesi teşhiste yalnız selamlardan yaklaşıklanır (veri çerçevesi duyulması kaydı tazelemez). Etkisi 30 s'den uzun sessizlikle sınırlı.
- Bağ kurallarının sayımı gönderici açısındandır. Göndericinin kendisi karıştırılırken (onayları duyamaz) de sayılır; KK-03 kural 8 ile önceki tasarım bunu kendi durumla bastırıyordu. Bu yüzden açık dönemde "uzak" sınıfındaki ateşlenmeler raporlanır ama seçime girmez.
