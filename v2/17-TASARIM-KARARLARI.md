# 17 · TASARIM KARARLARI — DESPARETE'nin yeni sürümü

> Faz 5-2'nin çıktısı (`12` §1.2, K-252). Her konuda: ölçülmüş kanıt, kararım ve gerekçesi, ödünç alınan her özelliğin kaynağı. Seçeneklerin ayrıntısı ve kaynak notları `protokol_kaynaklari/faz5_arastirma_2026-10-21/NOTLAR.md`de, ölçümler `arsiv/teshis/faz5_2_*/sonuc.md`de. Köşeli parantezli numaralar `16`nın kaynaklarıdır.
>
> Sayısal değerler (aralıklar, pencereler, eşikler) burada seçilmez; 5-3'te kural kâğıtlarında yazılır ve geliştirme tohumlarında ölçülerek ayarlanır. Zaman sabitleri tek bir karıştırıcı çizelgesine göre ayarlanmaz; dayanıklılık hücresi bunun için var (`06` §0.4.5).
>
> Kararlar `T-n` diye numaralanır; kod yorumları bu numaralara atıf verir. Güncel: 16 Kasım 2026.

---

## 0 · İlkeler

**İlke 1 · Kısa bağ karıştırmaya dayanıklıdır, ama tek ölçüt değildir (16 Kasım).**

Alıcıya ulaşan sinyal, bağın uzunluğunun karesiyle zayıflar (ters kare yasası; simülatörde yol kaybı üsteli α = 2, `sim2/yapilandirma/konfig.py`). Karıştırıcının alıcıya ulaşan gücü ise bağın uzunluğuna değil, karıştırıcının alıcıya uzaklığına bağlıdır. Bağ yarıya kısalınca sinyal dört katına çıkar (+6 dB), karıştırıcının gücü aynı kalır; kısa bağın karıştırmaya karşı payı (marjı) büyüktür. Az atlamalı, uzun bağlı yollara yaslanmak elektronik harbe dayanıklılık hedefime terstir.

Bu, yalnız kısa bağ kullanılacağı anlamına gelmez: her fazladan atlama kanalda bir gönderim, bir kayıp olasılığı ve biraz gecikme daha demektir. Kısa bağı ayrı bir kuralla zorlamıyorum; bağın maliyeti ölçülen teslim oranından gelir (T-2). Karıştırma başlayınca payı küçük olan uzun bağların teslimi önce düşer, maliyetleri artar ve rotalar kendiliğinden kısa bağlara kayar.

- Ölçülen (karıştırıcısız ikiz; `arsiv/teshis/faz5_2_anatomi_2026-11-14/sonuc.md` §5): v0.4.1 paket başına 2,72 atlama yapıyor, atlama başına başarısızlığı %6,49, seçtiği bağın ortanca mesafesi 7,0–8,2 km; Babel'de 3,74 atlama, %2,32, 5,9–7,0 km. Bu hücrede Babel'in daha kısa bağlardan daha çok atlaması kazanıyor (`arsiv/teshis/faz5_2_secenek_iletim_2026-11-15/sonuc.md` §5). Sonuç bizim hücrelerimiz içindir, genel bir yargı değildir.

**İlke 2 · Ölçmeyi bırakmamak: kendini onaran ağ (16 Kasım).**

İHA'ların formasyonunu ve yörüngesini değiştiremem; yalnız paketin hangi yoldan gideceğini seçerim. Bu yüzden bir bağın bugünkü kötülüğü kalıcı sayılmaz: karıştırma biter, İHA'lar yaklaşır, bağ düzelir. Kullanmadığım bağı da ölçmeye devam ederim; düzelen bağ kendiliğinden yeniden kullanılır. Böylece ağ, kopan yerlerini dışarıdan bir müdahale olmadan onarır. Uygulaması T-1 ve T-3'te.

**İlke 3 · Kanıta göre davranmak, çizelgeye göre değil (16 Kasım).**

Protokol karıştırıcının çizelgesini bilmez ve ona göre ayarlanmaz: bağı kanıt gelince bırakır, kanıt kalkınca geri alır. Böylece hangi çizelgede çalışırsa çalışsın karıştırıcıyı izler. Zaman sabitleri tek bir çizelgeye göre seçilmez; dayanıklılık hücresi (10 s açık · 20 s sessiz) bunu sınar. Uygulaması T-7, T-9 ve T-10'da.

---

## 1 · Komşu ve bağ kalitesi (16 Kasım)

**Ölçülmüş kanıt** (karıştırıcısız ikiz; `arsiv/teshis/faz5_2_anatomi_2026-11-14/sonuc.md` §5 · `arsiv/teshis/faz5_2_secenek_iletim_2026-11-15/sonuc.md`):
- v0.4.1'de selam yok; komşu yoklama ve MAC onayıyla bilinir, 5 s duyulmayınca silinir. Koşu başına 15 171 komşu silinmesi ↔ Babel'de 315.
- Alınan duyuruların %64'ü, gönderen komşu "etkin" sayılmadığı için işlenmiyor.
- Ardıl ortalama 1,3 saniyede bir değişiyor.
- Yedekleri yoklamayla canlı tutmak (`hedefli_canlilik`) rota kaybını azaltmadı. v0.4.1'in kontrol trafiğinin kanalda kapladığı süre Babel'inkinin 2,69 katı.
- İletim farkı alıcıya ulaşan çerçevenin bozulmasında; yaklaşık yarısı seçilen bağın kalitesinden.

**T-1 · Komşunun varlığı: dinleme ve seyrek selam.**
- Komşudan çözülen her çerçeve (veri, onay, kontrol) o komşunun yaşadığının kanıtıdır. Bedeli yoktur (`13` §02.5, `cerceve_duyuldu`, K-172).
- Her düğüm sıra numaralı küçük bir selam yayar. Selam, ters yönün ölçülebilmesi için duyduğum komşuları ve her birinden aldığım selam oranını da bildirir (T-2).
- Selam aralığı uyarlanır: komşuluk sakinken uzar, değişince kısalır. Aralığın bir üst sınırı vardır; bağın kötüleştiği ya da düzeldiği ne kadar sürede fark edilecek, bu sınır belirler (T-3).
- Komşu yalnız hiç duyulmayınca (ne selamı ne başka bir çerçevesi) silinir. Kötü kalite silme sebebi değildir (T-3).
- Gerekçe: düzenli selam bütün komşuları ve iki yönü bilir ama sabit bir yük getirir. Yalnız kendi trafiğinden kanıt (v0.4.1) kullanılmayan komşuyu bilemez ve yedekleri bayatlatır. Yalnız dinleme, benden komşuya giden yönü göremez. Karma, en çok bilgiyi en az yükle verir.
- Ödünç: selam ve ters yön bildirimi ETX [36] ve Babel [4]; uyarlanır aralık Trickle [62] (RFC 6206'da ilanlar için, burada selama uygulanır); dinleme ilk taslağımdan (`arsiv/DESPARETE_TASARIM_PAKETI_v0.1_2026-09-22/`, Protokol Taslağı v0 §6).

**T-2 · Bağ kalitesi: iki yönlü teslim oranı.**
- Bağın maliyeti beklenen gönderim sayısıdır: `ETX = 1 / (d_f · d_r)`. `d_f` komşunun benden aldığı selam oranı (komşu bildirir), `d_r` benim komşudan aldığım selam oranı. Kaç selamın kaybolduğu sıra numarasından bilinir. Yol maliyeti, bağ maliyetlerinin toplamıdır.
- Kullandığım bağlarda kendi unicast gönderimlerimin sonucu (`iletim_sonucu`, K-151) ek örnek olarak girer. Sebep: selam küçüktür ve büyük veri paketinin kaybını olduğundan iyi gösterir [36].
- Dinlenen çerçeveler komşunun varlığını kanıtlar, teslim oranını tek başına vermez: komşunun kaç çerçeve gönderdiği bilinmeden "kaçını duydum" bir oran değildir.
- Sinyal gücü (RSSI) maliyete girmez; yalnız bağlam olarak kullanılır [57].
- Gerekçe: teslim oranı kaliteyi doğrudan ölçer, en çok sınanmış ölçüdür ve raporda açıkça savunulabilir. v0.4.1'in M0.1'i yalnız kendi unicast sonuçlarını kullandığı için az trafik taşıyan iyi bir bağı belirsizlik cezasıyla pahalı gösteriyordu.
- Ödünç: ETX [36]; selam geçmişinden ölçme biçimi Babel [4].

**T-3 · Kötü bağ: kullanılmaz ama unutulmaz.**
- Beklenen gönderim sayısı bir üst sınırı aşan bağ yönlendirmede kullanılmaz. RPL'nin MRHOF'u bu sınırı 4 koyuyor [64].
- Bağ komşu listesinde kalır ve olağan selamlarla ölçülmeye devam eder. Bunun için ek yoklama gönderilmez: yedekleri yoklamayla canlı tutmak rota kaybını azaltmadı, kontrol trafiği zaten Babel'inkinin 2,69 katı.
- Kullanıma dönüş iki eşiklidir (histerezis): bağ, kullanımdan çıktığı eşikten belirgin biçimde iyi olunca yeniden aday olur. Tek eşikte, eşiğin çevresinde dolaşan bir bağ sürekli girip çıkar ve rotalar salınır (v0.4.1'de ardıl 1,3 saniyede bir değişiyor).
- Karıştırma bitince ya da İHA'lar yaklaşınca bağ kendiliğinden geri gelir (İlke 2).
- Bu iki eşik bağın kullanılabilirliği içindir; bir rotadan ötekine geçişin histerezisi ayrı bir konudur (bırakma zamanı).
- Ödünç: üst sınır ve histerezis MRHOF [64]; Babel'in histerezisi [55].

**T-4 · Kanal yoğunluğu bağ maliyetine girmez.**
- Gerekçe: yüke bağlı ölçü bir geri besleme döngüsü kurar: az yüklü yol seçilir, yüklenir, pahalılaşır, terk edilir; rotalar salınır [55]. Yoğunluk, karıştırma kanıtında ya da eşit maliyetli adaylar arasında ikincil ölçüt olarak ayrıca düşünülebilir.

**5-3'e kalanlar:** selam aralığının alt ve üst sınırı ve hangi olayın "değişim" sayılacağı · teslim oranının penceresi ya da düzgünleştirmesi · iki eşiğin değerleri · veri sonuçlarının ve dinlenen çerçevelerin ölçüye katılma biçimi · selamın biçimi ve boyutu (`13` §02.1, `MesajBicimi`).

---

## 2 · Karıştırmanın yerel kanıtı (16 Kasım)

**Ölçülmüş kanıt** (birincil hücre; `arsiv/teshis/faz5_2_anatomi_2026-11-14/sonuc.md` §5 · `arsiv/teshis/faz5_2_rakip_cizgisi_2026-11-15/sonuc.md`):
- Babel'in bağ ölçüsü son 16 selama bakıyor (4 s aralıkla). Karıştırıcı açılınca atlama başına başarısızlığı %2,6'dan %10,0'a çıkıyor; başarısız iletimlerinin %20'si kâhinin "kötü" dediği bağda (ikizde %0). Rotasını koruyup kesik bağa göndermeyi sürdürüyor.
- v0.4.1'de bir ardıl kopunca onarım geçide giden yol boyunca yayılıyor. Açık evredeki rota kaybı çoğunlukla karıştırıcının etki alanının dışında: uzak 0,177 · girişim 0,034 · ED 0,007.
- Karıştırmanın getirdiği kayıp Babel'de iletim başarısızlığına, v0.4.1'de rota yokluğuna gidiyor (teşhis (c) §5).
- Karıştırıcının etrafında üç bölge var (`kalibrasyon/kayip_anatomisi.py`'nin tanımı): ED bölgesi (karıştırıcının gücü ≥ −76 dBm; verici kanalı meşgul sanır, gönderemez) · girişim bölgesi (gürültü tabanının üstü; kanal boş görünür, alıcıda çerçeve bozulur) · uzak. Babel'in açık evrede artan iletim kaybı en çok girişim bölgesinde: 0,035 → 0,182 (ED 0,002 → 0,049 · uzak 0,048 → 0,119). Kanal doluluğu yalnız ED bölgesini görür.

**T-5 · Kanıtın işaretleri: tutarlılık.**
- Karıştırma tek bir işaretten değil, işaretlerin birbirini tutmasından anlaşılır:
  - teslim düşüşü ile sinyal gücünün tutarlılığı: düşük teslim ve güçlü sinyal karıştırmaya, düşük teslim ve zayıf sinyal kötü bağa işaret eder;
  - açıklanamayan kanal meşguliyeti: kanal meşgul, ama duyulan çerçeveler bu meşguliyeti açıklamıyor (ED bölgesi);
  - bozuk çerçeve sayısı (`phy_hata`) ve beklenen selamların gelmemesi (sıra numarasındaki boşluk; komşulardan iki alım arasındaki en uzun süre).
- Hangi işaretlerin bizim simülatörde karıştırmayı gerçekten ayırt ettiği teşhis (d)'de ölçülür; ayırt etmeyen işaret kanıta girmez.
- Kanıt tek bir karıştırıcı türüne bağlanmaz: kanal doluluğu reaktif karıştırıcıyı görmez, teslim ve tutarlılık işaretleri iki türü de görür [23].
- Gözlem sınırı: ölçülen gürültü kullanılamaz (K-227). RSSI'nin ölçüm hatası (σ 2 dB) sınanmamıştır; kullanıldığı için duyarlılığı ölçülür (`04` §9).
- Ödünç: işaretler Puñal 2014 [23]; tutarlılık kuralı Xu vd. 2005 (Puñal 2014'te aktarıldığı gibi; özgün makale açılamadı).

**T-6 · Kanıtı kim söyler: gönderen ve alıcı.**
- Gönderen, kendi MAC sonuçlarından bağ başına kanıt toplar. Tek komşuya başarısızlık o bağı ya da o alıcıyı, bütün komşulara başarısızlık gönderenin kendisini gösterir.
- Alıcı, karıştırıldığını kendi işaretlerinden anlar ve selamında birkaç bitle bildirir; bedeli selamın boyutuna eklenir (`13` §02.1). Girişim bölgesindeki düğüm gönderebildiği için bu bilgi komşularına ulaşır.
- ED bölgesindeki düğüm gönderemez; komşuları onun sessizliğini (beklenen selamın gelmemesi) kanıt sayar.
- Gerekçe: karıştırılan çoğu zaman alıcıdır (SINR kaybı alıcıda), gönderen bunu ancak paket kaybettikten sonra öğrenir. Komşuların kanıtını birleştirmek tespiti belirgin iyileştiriyor [23].
- Ödünç: komşularla işbirliği Puñal 2014 [23].

**T-7 · Kanıtın sonucu: ayrı bir "karıştırılıyor" durumu.**
- Karıştırma kanıtı bulunan bağ geçici olarak kullanılmaz. Karıştırmadan önceki kalitesi hatırlanır; kanıt kalkınca bağ o değerle hemen geri döner, teslim oranının yeniden dolmasını beklemez.
- Kötü bağ (T-3) ile karıştırılan bağ ayrı tutulur: kötü bağ kalitesi düzelince, karıştırılan bağ kanıt kalkınca döner.
- Bağın maliyetine karıştırma cezası eklenmez: karıştırma bitince ceza yavaş söner ve maliyetteki salınım riski (T-4) geri gelir.
- Ne kadar kanıtla "karıştırılıyor" ve "bitti" denileceği bırakma zamanının konusudur.
- Yanlış alarmın bedeli (iyi bir bağın gereksiz bırakılması) 5-3'te ölçülür.
- Hatırlanan kaliteyle geri dönüş benim tasarımımdır. Yakın fikirler: karıştırılan bölgenin etrafından dolaşmak, ağ katmanının bilinen karıştırma stratejisidir [59]; bağ başına karıştırmanın etkisini izleyip trafiği ona göre dağıtmak Tague vd. 2011'de var [53].

**T-8 · Kurala dayalı kanıt, öğrenme yok.**
- Kanıt, eşikleri yazılı açık kurallarla verilir; eğitilmiş sınıflandırıcı kullanılmaz.
- Gerekçe: simülasyonun "karıştırıcı açık" etiketleriyle eğitilen bir sınıflandırıcı simülatörün karıştırıcı modelini ezberler. Bu, kâhin bilgisinin protokole girmemesi kuralına (`04` §4) dolaylı bir sızıntıdır. Açık kural raporda savunulabilir.
- Bedeli: bağlarımız menzil sınırında olduğundan elle konan eşik zor yayılımda yanılabilir [23]; eşikler geliştirme tohumlarında ölçülerek ayarlanır.

**Teşhis (d)'ye ve 5-3'e kalanlar:** kanıta girecek işaretler ve eşikleri (teşhis (d)) · alıcının bildirdiği bitlerin sayısı ve anlamı · işaretlerin birleştirilme kuralı · yanlış alarm oranı.

---

## 3 · Bırakma zamanı (16 Kasım)

Yol iki sebeple değişir ve ikisinin kuralı ayrıdır: **zorunlu geçiş** (ardıl kullanılamaz hâle gelmiştir) ve **isteğe bağlı geçiş** (yol çalışıyor, başka bir yol daha ucuz görünüyor).

**Ölçülmüş kanıt** (`arsiv/teshis/faz5_2_rakip_cizgisi_2026-11-15/sonuc.md` §1 · `arsiv/teshis/faz5_2_anatomi_2026-11-14/sonuc.md` §5 · `arsiv/teshis/faz5_2_secenek_iletim_2026-11-15/sonuc.md` §5):
- Birincil hücrede evrelere göre teslim (önce · açık · sessiz; 8 tohum): kâhin 0,919 · 0,779 · 0,916 · Babel 0,932 · 0,663 · 0,916 · v0.4.1 0,779 · 0,567 · 0,763. Kâhin bile açık dönemde 0,14 kaybediyor; Babel 0,27, v0.4.1 0,21. Sessiz dönemde üçü de önceki düzeye yakın dönüyor; asıl iş açık dönemde.
- Babel MAC başarısızlığını kullanmıyor ve rotası 56 s yaşıyor (`protokol_kaynaklari/faz5_arastirma_2026-10-21/NOTLAR.md` §6). Karıştırmada başarısız iletimlerinin %20'si kesik bağda.
- v0.4.1 tek bir MAC başarısızlığında komşuyu "şüpheli" yapıp onarıma giriyor. Ardılı düğüm başına 1,3 saniyede bir değişiyor (ikiz); Babel'in seçimi düğüm–hedef çifti başına kabaca 20 saniyede bir (25 015 değişim, 40 düğüm, 39'ar hedef).
- Kanal kalabalık: üç protokolde de veri denemelerinin yarısından fazlası başarısız. Tek bir atlama kaybı çoğu zaman karıştırma değildir.

**T-9 · Zorunlu geçiş: MAC başarısızlığı kanıttır, karar değildir.**
- MAC'in bir çerçeveden vazgeçmesi (`iletim_basarisiz`) ardılı tek başına bıraktırmaz; T-5 ve T-6'nın kanıtına girer.
- Kanıt birikince bağ "karıştırılıyor" durumuna (T-7), kalitesi üst sınırı aşınca kullanılmaz duruma (T-3) geçer ve ardıl hazır bir yedeğe yerelde değiştirilir.
- Onarım yalnız hiç uygun yedek yoksa başlar.
- Gerekçe: Babel'in tepkisizliği kesik bağa göndermeyi sürdürüyor, v0.4.1'in aşırı tepkisi kalabalık kanaldaki her çarpışmada onarım başlatıyor. MAC sonucunu karar değil kanıt saymak bu ikisinin arasındaki seçimimdir.

**T-10 · Kanıtın eşiği: birkaç ardışık olay, iki yönde de.**
- "Karıştırılıyor" ve "bitti" kararları birkaç ardışık olayla verilir; sayılar 5-3'te.
- Erken dönmenin bedeli küçüktür: karıştırma sürüyorsa bağ birkaç olayda yeniden çıkar, hatırlanan kalite korunur (T-7).
- Karıştırmanın başlaması komşulukta bir değişim sayılır; selamlar sıklaşır (T-1) ve karıştırmanın bittiği daha çabuk duyulur.
- Gerekçe: birincil hücrede karıştırıcı 15 s açık kalıyor; tespit 5 s sürerse açık sürenin üçte biri kesik bağda geçer. İlk olayda karar kalabalık kanalda yanlış alarm üretir; kayan bir penceredeki oran Babel'in yavaşlığına döner. Doğruluk ile tepki hızı arasındaki değiş tokuş ETX'in de uyarısıdır [36].

**T-11 · İsteğe bağlı geçiş: oransal eşik.**
- Çalışan bir yoldan, yeni yolun maliyeti bugünkünden belli bir oranda düşükse geçilir; oran 5-3'te.
- Gerekçe: sabit fark eşiği (MRHOF'ta 1,5 beklenen gönderim [64]) maliyeti 2 olan yolda %75, maliyeti 8 olan yolda %19 iyileşme ister; kısa yol neredeyse hiç değişmez, uzun yol kolay değişir. Oransal eşik her uzunlukta aynı davranır. Düzgünleştirilmiş maliyetin de daha iyi olması şartı (Babel [55]) T-2'nin ölçüm penceresinin üstüne ikinci bir yavaşlık eklerdi.
- Ödünç: oransal histerezis Ramachandran vd. 2007 [54]; ölçümlerinde %10 eşik baskın rotanın ömrünü 4–5 kat uzatıyor (durağan ağlar, zaman ölçeği dakika; bizimki saniye).

**5-3'e kalanlar:** "karıştırılıyor" ve "bitti" için olay sayıları · isteğe bağlı geçişin oranı · kötü bağ (T-3) için de aynı olay sayısı kuralının geçerli olup olmayacağı.

---

## 4 · Yedek yol ve döngüsüzlük (16 Kasım)

Yedek, döngü yaratmadan geçilebilecek komşudur; hangi komşunun güvenli olduğunu döngüsüzlük kuralı söyler. Bu yüzden iki konu birlikte karara bağlandı.

**Ölçülmüş kanıt** (`arsiv/teshis/faz5_2_rakip_cizgisi_2026-11-15/sonuc.md` §2 · `arsiv/teshis/faz5_2_anatomi_2026-11-14/sonuc.md` §5 · `arsiv/teshis/faz5_2_secenek_iletim_2026-11-15/sonuc.md` §5–§6):
- Birincil hücrede açık dönemde doğan paketlerin rota yokluğundan kaybı: Babel 0,000 · kâhin 0,008 · v0.4.1 0,237. Babel de FD kuralını kullanıyor; fark açlığın çözülüşünde.
- v0.4.1'de açık evredeki onarımların %67'si açlıkla, %33'ü aday yokluğuyla başlıyor.
- v0.4.1 açlıkta en az 6 s bekliyor ve yeni turu yalnız kendi paketiyle istiyor: ikizde 131 isteğe 2 yanıt. Babel hemen soruyor, seçili rotasına uygulanamaz bir güncelleme gelince rotayı bırakmıyor (`protokol_kaynaklari/faz5_arastirma_2026-10-21/NOTLAR.md` §5, §8).
- Yol istemek (`onarim_edinimi`) ikizde rota kaybını %40 azalttı (0,054 → 0,032); kazanç iletimde geri gitti (paket başına atlama +%17, kontrol kanal süresi +%45).
- Yedekleri yoklamayla canlı tutmak (`hedefli_canlilik`) rota kaybını azaltmadı. v0.4.1'de alınan duyuruların %64'ü işlenmiyordu; yedekler bilinmiyordu (T-1 bunu çözer).

**T-12 · Döngüsüzlük: uygulanabilirlik koşulu ve sıra numarası.**
- Tur (sıra numarası) geçitten çıkar. Bir komşunun ilanı ya daha yeni turdaysa ya da aynı turda bildirdiği maliyet benim bu turdaki en iyi maliyetimden (FD) küçükse kabul edilir.
- Gerekçe: döngü hiç oluşmaz; bizim hücrelerimizde aynı kuralı kullanan Babel'in açık dönemdeki rota yokluğu kaybı 0,000. Komşulara sorarak ortak hesap (DUAL) kayıplı kanalda takılabilir; yükseklik kuralı (RPL) döngüyü önlemez, oluşunca yakalar ve her veri paketine bir alan ister. En garanti ve en çok sınanmış yol bu.
- Ödünç: Babel [4] (RFC 8966 §3.5) ve DSDV ailesi; v0.4.1'in çekirdeği de bu aileden.

**T-13 · Açlık: hemen istek.**
- Uygun komşu kalmayınca yeni tur hemen istenir. Daha yeni turu bilen herhangi bir düğüm yanıtlar, bilmeyen isteği geçide doğru iletir; tur yalnız geçitte ve bir artar.
- Seçili rota çalışıyorsa, ona uygulanamaz bir güncelleme geldi diye bırakılmaz; yeni tur istenir.
- Tur düzenli aralıklarla artırılmaz: yeni tur kimi zaman önce dolambaçlı bir yoldan ulaşır ve rotalar her turda çalkalanır (T-11'e ters).
- Gerekçe: v0.4.1'in bekleyen ve yalnız kendi paketiyle soran açlık çözümü açık dönemde 0,237'lik rota yokluğu kaybının başlıca kaynağı.
- Bedeli kontrol trafiğidir; isteklerin yinelenmesi ve sıklığı kontrol yükü konusunda sınırlanır.
- Ödünç: Babel [4] (RFC 8966 §3.8.1.2).

**T-14 · Yedek yol: hazır yedek kümesi, tek yoldan gönderim; çoğaltma yalnız son çare.**
- Uygulanabilirlik koşulunu (T-12) geçen bütün komşular hazır yedektir. Ardıl kullanılamaz olunca (T-3, T-7) en iyisine anında geçilir. Yedekler için ek mesaj gönderilmez; selam (T-1) ve ilanlar yeter.
- Trafik komşulara bölünmez: bölme daha kötü bağa da trafik gönderir, açığın büyük kalemi ise zaten iletim kaybı.
- Seçici çoğaltma çekirdekte yoktur. Kullanılırsa yalnız son çare olarak, nadiren ve sıkı bir bütçeyle kullanılan bir yan özelliktir; 5-3'te ayrı bir bayrakla ölçülür, kazandırmazsa kalmaz. Gerekçe: bizim simülatörümüzde çoğaltma çok pahalı. Kanal kalabalık (veri denemelerinin yarısından fazlası başarısız) ve her pakete kopya toplu akışta kanalı boğuyor (JarmRout, K-238).
- Ödünç: hazır yedek fikri DUAL'ın uygulanabilir ardılı [65] (RFC 7868) ve RPL'nin ebeveyn kümesi [63]; seçici çoğaltma ilk taslağımdan (PROTECT).

**T-15 · Yedeklerin ayrışması: kanıtla.**
- "Karıştırılıyor" işaretli komşu (T-7) yedek sayılmaz. Karıştırılan bölge kanıttan görünür; konum gerekmez.
- Konum selama eklenmez: karıştırıcının yeri bilinmediği için ardıldan uzak bir yedeğin neye yarayacağı belli değil, bedeli ise her selamda ödenir.
- K-230'un sorusunun cevabı budur.
- Ödünç: ortak düğüm riski fikri Tague vd. 2011 [53].

**5-3'e kalanlar:** tur isteğinin yinelenme sayısı ve aralığı · "son çare"nin tanımı ve kopya bütçesi · yedeklerin sıralanması.
