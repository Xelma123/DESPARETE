# 17 · TASARIM KARARLARI — DESPARETE'nin yeni sürümü

> Faz 5-2'nin çıktısı (`12` §1.2, K-252). Her konuda: ölçülmüş kanıt, kararım ve gerekçesi, ödünç alınan her özelliğin kaynağı. Seçeneklerin ayrıntısı ve kaynak notları `protokol_kaynaklari/faz5_arastirma_2026-10-21/NOTLAR.md`de, ölçümler `arsiv/teshis/faz5_2_*/sonuc.md`de. Köşeli parantezli numaralar `16`nın kaynaklarıdır.
>
> Sayısal değerler (aralıklar, pencereler, eşikler) burada seçilmez; 5-3'te kural kâğıtlarında yazılır ve geliştirme tohumlarında ölçülerek ayarlanır. Zaman sabitleri tek bir karıştırıcı çizelgesine göre ayarlanmaz; dayanıklılık hücresi bunun için var (`06` §0.4.5).
>
> Kararlar `T-n` diye numaralanır; kod yorumları bu numaralara atıf verir. Güncel: 17 Kasım 2026.

---

## Protokolün kimliği (17 Kasım)

DESPARETE, karıştırma altında çalışan taktik İHA sürüsü için tek hedefe yönelik bir yönlendirme protokolüdür: her düğümden geçide giden telemetriyi taşır, geçitten düğümlere dönen komutu ise telemetrinin geldiği yolun tersinden (geri iz) götürür. Çekirdeği bilinen yöntemlerden kurulur ve her birinin kaynağı yazılıdır: bağın maliyeti iki yönde ölçülen teslim oranıdır (ETX); yol, maliyeti geçide doğru azalan komşulardan seçilir ve oluşabilecek döngü veri yolunda yakalanıp onarılır (CTP, RPL); selam aralığı ağın sakinliğine göre uzar (Trickle). Veriyi taşıyamayan bağ, veri çerçevelerinin MAC'te tümden kaybolmasından (vazgeçme) tanınır ve yedek varken bırakılır. DESPARETE'yi ayıran, karıştırmayı yerel kanıtla tanıması ve ona kanıtla karşılık vermesidir. Karıştırıcıya çok yakın düğüm bunu kendi kanal ölçümünden hemen anlar: kanalı sürekli meşgul görür. Daha uzaktaki karıştırılan düğümde tek bir işaret yetmez; düğüm çözdüğü çerçeveleri, komşularının selamlarını ve MAC sonuçlarını birkaç saniye boyunca birlikte okur. Bu birleşik kuralın biçimi ve başarısı geliştirmede ölçülür. Karıştırılan alıcı bunu selamıyla komşularına bildirir; gönderemeyecek kadar yakın olanı komşuları sessizliğinden tanır. Karıştırılan bağ geçici olarak bırakılır ve hazır bir yedeğe yerelde geçilir; bağın karıştırmadan önceki kalitesi hatırlanır ve kanıt kalkınca bağ hemen geri alınır. Protokol karıştırıcının çizelgesini bilmez. Kullanmadığı bağları da ölçmeyi sürdürür ve kopan yerlerini kendiliğinden onarır. Kısa bağların karıştırmaya karşı büyük payından ayrı bir kuralla değil, ölçülen teslim oranıyla yararlanır. Kontrol yükünü düşük tutar: uzaklık ilanı selamla birlikte gider, ara ilan yalnız önemli değişimde çıkar.

Taslak 16 Kasım'da yazıldı; karıştırma kanıtını anlatan cümleler teşhis (d)'nin sonucuyla (§2, T-5) ve 5-2'nin bağımsız denetimiyle (`arsiv/denetim/DENETIM-RAPORU-5-2-2026-11-17.md`), komutun yolu T-20'yle 17 Kasım'da son hâlini aldı. 19 Kasım'da, ilk ölçüm ve açlık teşhisinden sonra yol seçimi ve bağın veri ölçüsü değişti (T-2, T-9, T-11, T-12, T-13, T-14, T-17, T-18); önceki metin `v2/arsiv/17-TASARIM-KARARLARI-2026-11-18.md`.

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
- Selam o anki aralığını taşır. Aralık değişince alıcı, belli bir sürede kaç selam beklediğini (T-2) ve bir komşunun sustuğunu (T-6) ancak böyle bilir; sıra numarasındaki boşluk kaybı ancak sonraki selam gelince gösterir (17 Kasım, denetim Ö-5).
- Komşu yalnız hiç duyulmayınca (ne selamı ne başka bir çerçevesi) silinir. Kötü kalite silme sebebi değildir (T-3).
- Gerekçe: düzenli selam bütün komşuları ve iki yönü bilir ama sabit bir yük getirir. Yalnız kendi trafiğinden kanıt (v0.4.1) kullanılmayan komşuyu bilemez ve yedekleri bayatlatır. Yalnız dinleme, benden komşuya giden yönü göremez. Karma, en çok bilgiyi en az yükle verir.
- Ödünç: selam ve ters yön bildirimi ETX [36] ve Babel [4]; selamın aralığını taşıması Babel [4] (RFC 8966 §4.6.5); uyarlanır aralık Trickle [62] (RFC 6206'da ilanlar için, burada selama uygulanır); dinleme ilk taslağımdan (`arsiv/DESPARETE_TASARIM_PAKETI_v0.1_2026-09-22/`, Protokol Taslağı v0 §6).
- **Teşhis (d)'nin sonucu (17 Kasım, `arsiv/teshis/faz5_2_isaretler_2026-11-16/sonuc.md` §4):** karıştırıcısız ikizde en çok kullanılan 80 bağın 7 denemelik atlama başarısı formasyonda 32 s içinde bant değiştirmiyor (%0,3). Bu ölçü doymuştur: tek deneme başarısı 0,28'in üstündeki bağ "iyi" banttadır. Selamın ölçtüğü tek deneme başarısı ve yedek bağlar ölçülmedi. Bu yüzden sonuç selam aralığının üst sınırı için tek başına yetmez; sınır, sessizliği fark etme süresi (T-6, T-10) ve kontrol payıyla (T-19) birlikte seçilir (§7).

**T-2 · Bağ kalitesi: iki yönlü teslim oranı.**
- Bağın maliyeti beklenen gönderim sayısıdır: `ETX = 1 / (d_f · d_r)`. `d_f` komşunun benden aldığı selam oranı (komşu bildirir), `d_r` benim komşudan aldığım selam oranı. Kaç selamın kaybolduğu sıra numarasından bilinir. Yol maliyeti, bağ maliyetlerinin toplamıdır.
- **Veri sonucu: vazgeçme (19 Kasım'da yeniden yazıldı).** Kendi veri gönderimlerimin sonucu (`iletim_sonucu`, K-151) maliyete girmez; yalnız bir bağın veriyi taşıyıp taşımadığını söyler. Sayılan, MAC'in bir çerçeveden **vazgeçmesidir**: bütün denemeler başarısız, paket o atlamada kayboldu. Yeniden denemeyle giden çerçeve başarılıdır.
  - Son veri çerçevelerinde vazgeçme belli bir sayıya ulaşırsa bağ "veriye uygun değil" sayılır. Maliyeti benimkinden düşük başka bir olağan komşu varsa bağ bir süre ardıl seçilmez; yoksa kullanılmaya devam eder, açlık doğurmaz. Yeniden tetiklenirse süre katlanır. Pencere, sayı ve süreler 5-3'te (kural kâğıdı).
  - Vazgeçmeyle birlikte selam da gelmiyorsa bu bir karıştırma kanıtıdır (T-9); selam geliyorsa bağ veriyi taşıyamıyordur (gizli uç, paket boyu ya da hız). İkisi bu yüzden ayrı tutulur.
  - Gerekçe (ilk ölçüm ve açlık teşhisi, `arsiv/teshis/faz5_3_cekirdek_2026-11-18/sonuc.md` · `arsiv/teshis/faz5_3_aclik_2026-11-18/sonuc.md`): 17 Kasım'daki tetik deneme / başarı oranını en az 4 çerçeveyle okuyordu; yeniden denemeler çoğunlukla geçici çarpışmadır. Karıştırıcısız ikizde ardıl bağını koşu başına 309 kez attı; atılanların %99,7'si kâhine göre iyiydi; rota yokluğu kaybının %99'u bu çıkışlardan başlıyordu; tetik kapalıyken pencere PDR'si 0,810 → 0,946. Ama tetik kapalıyken vazgeçmeler birkaç bağda toplanıyor: koşu başına en kötü bağda ~99 (en çok 200) vazgeçme, en kötü beş bağda vazgeçmelerin %41'i (tetik açıkken 22 ve %13). Küçük test dünyasında da tetiksiz bir düğüm böyle bir bağı bırakmadı. Selamı geçen ama veriyi taşıyamayan bağ vardır; ölçülmesi gereken yeniden deneme değil vazgeçmedir.
  - Selam iki yönde de yanılabiliyor: kalabalıkta iyi bağı olduğundan kötü gösteriyor (selamla çıkan bağlarda çıkış anında `d_f · d_r` ~0,23, kâhinin tek deneme başarısı ~0,73), gizli uçta veriyi taşıyamayan bağı iyi gösteriyor.
  - Veri sonucu maliyete girmez: kanal kalabalık, veri başarısı yükü izler ve maliyet salınır (T-4). 4B ve CTP veriyi maliyete katıyor [68], [69]; bizim simülatörümüzde bunu seçmiyorum.
  - Önceki karar (17 Kasım): veri denemelerinin belirgin biçimde kötü gösterdiği bağ hemen kullanımdan çıkar (askıda); karıştırma kanıtı gelmezse cezalı KÖTÜ olur. Askıda durumu ve veri cezası bu kararla kalktı.
- Dinlenen çerçeveler komşunun varlığını kanıtlar, teslim oranını tek başına vermez: komşunun kaç çerçeve gönderdiği bilinmeden "kaçını duydum" bir oran değildir.
- Sinyal gücü (RSSI) maliyete girmez; yalnız bağlam olarak kullanılır [23], [57].
- Gerekçe: teslim oranı kaliteyi doğrudan ölçer, en çok sınanmış ölçüdür ve raporda açıkça savunulabilir. v0.4.1'in M0.1'i yalnız kendi unicast sonuçlarını kullandığı için az trafik taşıyan iyi bir bağı belirsizlik cezasıyla pahalı gösteriyordu.
- Ödünç: ETX [36]; selam geçmişinden ölçme biçimi Babel [4].

**T-3 · Kötü bağ: kullanılmaz ama unutulmaz.**
- Beklenen gönderim sayısı bir üst sınırı aşan bağ yönlendirmede kullanılmaz. RPL'nin MRHOF'u bu sınırı 4 koyuyor [64].
- Bağ komşu listesinde kalır ve olağan selamlarla ölçülmeye devam eder. Bunun için ek yoklama gönderilmez: yedekleri yoklamayla canlı tutmak rota kaybını azaltmadı, kontrol trafiği zaten Babel'inkinin 2,69 katı.
- Kullanıma dönüş iki eşiklidir (histerezis): bağ, kullanımdan çıktığı eşikten belirgin biçimde iyi olunca yeniden aday olur. Tek eşikte, eşiğin çevresinde dolaşan bir bağ sürekli girip çıkar ve rotalar salınır (v0.4.1'de ardıl 1,3 saniyede bir değişiyor).
- Karıştırma bitince ya da İHA'lar yaklaşınca bağ kendiliğinden geri gelir (İlke 2).
- Bu iki eşik bağın kullanılabilirliği içindir; bir rotadan ötekine geçişin histerezisi ayrı bir konudur (bırakma zamanı).
- Ödünç: üst sınır MRHOF [64]. İki eşikli kullanılabilirlik benim uyarlamam; histerezis fikri MRHOF'ta ebeveyn seçiminde [64], Babel'de rota seçiminde [55].

**T-4 · Kanal yoğunluğu bağ maliyetine girmez.**
- Gerekçe: yüke bağlı ölçü bir geri besleme döngüsü kurar: az yüklü yol seçilir, yüklenir, pahalılaşır, terk edilir; rotalar salınır [55]. Yoğunluk, karıştırma kanıtında ya da eşit maliyetli adaylar arasında ikincil ölçüt olarak ayrıca düşünülebilir.

**5-3'e kalanlar:** vazgeçmenin penceresi, sayısı ve bekleme süresi (T-2; 19 Kasım) · selam aralığının alt ve üst sınırı ve hangi olayın "değişim" sayılacağı · teslim oranının penceresi ya da düzgünleştirmesi · iki eşiğin değerleri · veri sonuçlarının ve dinlenen çerçevelerin ölçüye katılma biçimi · selamın biçimi ve boyutu (`13` §02.1, `MesajBicimi`).

---

## 2 · Karıştırmanın yerel kanıtı (16 Kasım)

**Ölçülmüş kanıt** (birincil hücre; `arsiv/teshis/faz5_2_anatomi_2026-11-14/sonuc.md` §5 · `arsiv/teshis/faz5_2_rakip_cizgisi_2026-11-15/sonuc.md`):
- Babel'in bağ ölçüsü son 16 selama bakıyor (4 s aralıkla). Karıştırıcı açılınca atlama başına başarısızlığı %2,6'dan %10,0'a çıkıyor; başarısız iletimlerinin %20'si kâhinin "kötü" dediği bağda (ikizde %0). Rotasını koruyup kesik bağa göndermeyi sürdürüyor.
- v0.4.1'de bir ardıl kopunca onarım geçide giden yol boyunca yayılıyor. Açık evredeki rota kaybı çoğunlukla karıştırıcının etki alanının dışında: uzak 0,177 · girişim 0,034 · ED 0,007.
- Karıştırmanın getirdiği kayıp Babel'de iletim başarısızlığına, v0.4.1'de rota yokluğuna gidiyor (teşhis (c) §5).
- Karıştırıcının etrafında üç bölge var (`kalibrasyon/kayip_anatomisi.py`'nin tanımı): ED bölgesi (karıştırıcının gücü ≥ −76 dBm; verici kanalı meşgul sanır, gönderemez) · girişim bölgesi (gürültü tabanının üstü; kanal boş görünür, alıcıda çerçeve bozulur) · uzak. Babel'in açık evrede artan iletim kaybı en çok girişim bölgesinde: 0,035 → 0,182 (ED 0,002 → 0,049 · uzak 0,048 → 0,119). Kanal doluluğu yalnız ED bölgesini görür.

**T-5 · Kanıtın işaretleri.**
- Karıştırma tek bir işaretten değil, birkaç işaretin birlikte okunmasından anlaşılır. Aday işaretler (16 Kasım): teslim düşüşü ile sinyal gücünün tutarlılığı · kanal meşguliyeti · bozuk çerçeve sayısı (`phy_hata`) · çözülen çerçeve sayısı · beklenen selamların gelmemesi (sıra numarasındaki boşluk) · komşulardan iki alım arasındaki en uzun süre.
- Hangi işaretlerin bizim simülatörde karıştırmayı gerçekten ayırt ettiği teşhis (d)'de ölçüldü; ayırt etmeyen işaret kanıta girmez.
- **Geçerli işaret listesi (17 Kasım; teşhis (d), `arsiv/teshis/faz5_2_isaretler_2026-11-16/sonuc.md`):**
  - **ED bölgesi:** kanal meşguliyeti (`mesgul_sure_s`) tek başına yeter: G 0,978 · 0,976; karıştırılanların %80'ini yakalayan eşikte (≥ 0,62) karıştırıcısız ikizde yanlış alarm %0,035. Çözülen çerçeve ve CRC hatasının düşmesi de güçlü. Kaydedicinin "açıklanamayan meşguliyet"i (G 0,997) çözülen çerçevenin hava süresini ister; bu süre gözlem sözleşmesinde yok (`05` §3.3a), kanıta girmez (denetim E-1).
  - **Girişim bölgesi:** çözülen çerçeve düşüşü ve selam kaybı güçlü (G 0,81–0,85); kanal meşguliyetinin ve CRC hatasının düşmesi zayıf. Tek işaret ve tek saniye yetmiyor: %50 yakalamada ikizde yanlış alarm %6–11 (kuraldan sonra görülen). Kural birkaç işareti ve birkaç saniyeyi birlikte okur; biçimi, eşikleri ve başarısı 5-3'te, A/B ile.
  - Selam, çözülen çerçevelerin bir parçasıdır; ikisinin birlikte düşmesi bağımsız iki kanıt sayılmaz.
  - Çözülen çerçeve düşüşü karıştırmaya özgü değil: karıştırılan komşular susunca uzaktaki düğüm de daha az duyuyor. Kanal meşguliyeti girişim alanında düşer; karıştırılan alan "boş" görünür.
  - Sinyal tutarlılığı zayıf (AUC 0,71; düşük teslimli bağlar iki durumda da menzil sınırında, RSSI farkı ~2 dB); yalnız birlikte girer.
  - Dışarıda: düğüm düzeyinde son çözümden beri geçen süre (girişimde G 0,60). Puñal'in komşu başına en uzun boşluk süresi ölçülmedi (§7).
  - Koşul: bu sonuçlar Babel-a'nın trafiğinde ve sürekli sınıfta (araç, derin sızma) ölçüldü. Yeni sürümün seyrek selamı ve daha az kontrol trafiğiyle düzeyler değişir; öteki karıştırıcı sınıflarında ölçülmedi (§7).
- Kanıt tek bir karıştırıcı türüne bağlanmaz: Puñal 2014'te teslim oranı ve en uzun boşta kalma süresi iki türü de gösteriyor, kanal doluluğu reaktif karıştırıcıyı görmüyor [23].
- Gözlem sınırı: ölçülen gürültü kullanılamaz (K-227). RSSI'nin ölçüm hatası (σ 2 dB) sınanmamıştır; kullanıldığı için duyarlılığı ölçülür (`04` §9).
- Ödünç: işaretler Puñal 2014 [23]; tutarlılık kuralı Xu vd. 2005 (Puñal 2014'te aktarıldığı gibi; özgün makale açılamadı).

**T-6 · Kanıtı kim söyler: gönderen ve alıcı.**
- Gönderen, kendi MAC sonuçlarından bağ başına kanıt toplar. Tek komşuya başarısızlık o bağı ya da o alıcıyı, bütün komşulara başarısızlık gönderenin kendisini gösterir.
- Alıcı, karıştırıldığını kendi işaretlerinden anlar ve selamında birkaç bitle bildirir; bedeli selamın boyutuna eklenir (`13` §02.1). Girişim bölgesindeki düğüm gönderebildiği için bu bilgi komşularına ulaşır.
- ED bölgesindeki düğüm gönderemez; komşuları onun sessizliğini (beklenen selamın gelmemesi) kanıt sayar.
- Gerekçe: karıştırılan çoğu zaman alıcıdır (SINR kaybı alıcıda), gönderen bunu ancak paket kaybettikten sonra öğrenir. Komşuların kanıtını birleştirmek Puñal'in tek atlamalı düzeneğinde tespiti iyileştiriyor [23]; çok atlamalı dünyamızdaki kazancı ölçülür (§7).
- Ödünç: komşularla işbirliği Puñal 2014 [23].
- **Teşhis (d):** ED'deki düğüm karıştırıldığını kendi kanal ölçümünden tek saniyede bilir ama kanalı meşgul gördüğü için bildiremez; onu komşuları sessizliğinden tanımalı. Bu "sessizleşen komşu" işareti komşu başınadır ve ölçülmedi: (d)'nin selam kaybı, alıcının bütün tanıdık komşularından beklediği selamların kaçan payıdır ve temizde bile 0,44. Komşu başına işaretin yanlış alarmı bu tabanla birlikte ölçülür (§7). Açık evrede ortalama düğüm sayısı birincil hücrede ED 0,9 · girişim 6,8, dayanıklılık hücresinde 1,1 · 10,3; kanıtın asıl işi girişim bölgesinde.

**T-7 · Kanıtın sonucu: ayrı bir "karıştırılıyor" durumu.**
- Karıştırma kanıtı bulunan bağ geçici olarak kullanılmaz. Karıştırmadan önceki kalitesi hatırlanır; kanıt kalkınca bağ o değerle hemen geri döner, teslim oranının yeniden dolmasını beklemez.
- Kötü bağ (T-3) ile karıştırılan bağ ayrı tutulur: kötü bağ kalitesi düzelince, karıştırılan bağ kanıt kalkınca döner.
- Bağın maliyetine karıştırma cezası eklenmez: karıştırma bitince ceza yavaş söner ve maliyetteki salınım riski (T-4) geri gelir.
- Ne kadar kanıtla "karıştırılıyor" ve "bitti" denileceği bırakma zamanının konusudur.
- Yanlış alarmın bedeli (iyi bir bağın gereksiz bırakılması) 5-3'te ölçülür.
- "Karıştırılıyor" iken toplanan selam ve MAC örnekleri bağ ölçüsüne (T-2) girmez; hatırlanan kalite korunur. Sezilmeyen zayıf karıştırmada bağ ölçüsü kendisi düşer ve rotalar kısa bağlara kayar (İlke 1). Bağın üç durumu (olağan · kötü · karıştırılıyor) ve geçişleri 5-3'ün ilk kural kâğıdında yazılır (17 Kasım, denetim Ö-6; §7).
- Hatırlanan kaliteyle geri dönüş benim tasarımımdır. Yakın fikirler: karıştırılan bölgenin etrafından dolaşmak, ağ katmanının bilinen karıştırma stratejisidir [59]; bağ başına karıştırmanın etkisini izleyip trafiği ona göre dağıtmak Tague vd. 2011'de var [53].

**T-8 · Kurala dayalı kanıt, öğrenme yok.**
- Kanıt, eşikleri yazılı açık kurallarla verilir; eğitilmiş sınıflandırıcı kullanılmaz.
- Gerekçe: simülasyonun "karıştırıcı açık" etiketleriyle eğitilen bir sınıflandırıcı simülatörün karıştırıcı modelini ezberler. Bu, kâhin bilgisinin protokole girmemesi kuralına (`04` §4) dolaylı bir sızıntıdır. Açık kural raporda savunulabilir.
- Bedeli: bağlarımız menzil sınırında olduğundan elle konan eşik zor yayılımda yanılabilir [23]; eşikler geliştirme tohumlarında ölçülerek ayarlanır.

**5-3'e kalanlar:** birleşik kanıt kuralının biçimi (hangi işaretler, kaç saniye) ve eşikleri (teşhis (d)'nin eşik ve yanlış alarm tabloları girdi) · düşüşün düğümün kendi yakın geçmişine göre okunup okunmayacağı · alıcının bildirdiği bitlerin sayısı ve anlamı · yanlış alarm oranı.

---

## 3 · Bırakma zamanı (16 Kasım)

Yol iki sebeple değişir ve ikisinin kuralı ayrıdır: **zorunlu geçiş** (ardıl kullanılamaz hâle gelmiştir) ve **isteğe bağlı geçiş** (yol çalışıyor, başka bir yol daha ucuz görünüyor).

**Ölçülmüş kanıt** (`arsiv/teshis/faz5_2_rakip_cizgisi_2026-11-15/sonuc.md` §1 · `arsiv/teshis/faz5_2_anatomi_2026-11-14/sonuc.md` §5 · `arsiv/teshis/faz5_2_secenek_iletim_2026-11-15/sonuc.md` §5):
- Birincil hücrede evrelere göre teslim (önce · açık · sessiz; 8 tohum): kâhin 0,919 · 0,779 · 0,916 · Babel 0,932 · 0,663 · 0,916 · v0.4.1 0,779 · 0,567 · 0,763. Kâhin bile açık dönemde 0,14 kaybediyor; Babel 0,27, v0.4.1 0,21 (karıştırmaya özgü kayıpta Babel ile v0.4.1'in farkı 8 tohumda ayırt edilemedi: +0,042, 5/8; teşhis (c) S3). Sessiz dönemde üçü de önceki düzeye yakın dönüyor; asıl iş açık dönemde.
- Babel MAC başarısızlığını kullanmıyor ve rotası 56 s yaşıyor (`protokol_kaynaklari/faz5_arastirma_2026-10-21/NOTLAR.md` §6). Karıştırmada başarısız iletimlerinin %20'si kesik bağda.
- v0.4.1 tek bir MAC başarısızlığında komşuyu "şüpheli" yapıp onarıma giriyor. Ardılı düğüm başına 1,3 saniyede bir değişiyor (ikiz); Babel'in seçimi düğüm–hedef çifti başına kabaca 20 saniyede bir (25 015 değişim, 40 düğüm, 39'ar hedef).
- Kanal kalabalık: üç protokolde de veri denemelerinin yarısından fazlası başarısız. Tek bir atlama kaybı çoğu zaman karıştırma değildir.

**T-9 · Zorunlu geçiş: MAC başarısızlığı kanıttır, karar değildir.**
- MAC'in bir çerçeveden vazgeçmesi (`iletim_basarisiz`) ardılı tek başına bıraktırmaz; T-5 ve T-6'nın kanıtına girer.
- Kanıt birikince bağ "karıştırılıyor" durumuna (T-7), kalitesi üst sınırı aşınca kullanılmaz duruma (T-3) geçer ve ardıl yerelde başka bir komşuya değiştirilir (T-12). Vazgeçmeler selamla birlikte okunur: selam da gelmiyorsa karıştırma kanıtına, selam geliyorsa veriye uygunsuzluğa (T-2) gider (19 Kasım).
- Hiç yedek yoksa en iyi sonlu komşu seçilir; ayrıca yol aranmaz (T-12, T-13; 19 Kasım).
- Kendim karıştırılırken MAC başarısızlıkları bağ durumunu değiştirmez; ardıl korunur. Bütün komşulara başarısızlık gönderenin kendisini gösterir (T-6): veri çerçevesi alandan dışarıdaki ardıla çoğu zaman ulaşır, onayını ben duyamam; yedeğe geçmek bir şey kazandırmaz (17 Kasım, kural kâğıtlarının bağımsız denetimi B-11; `kural/KK-03` kural 8). Bu dondurmanın üst süresi 30 s'dir (KARIŞTIRILIYOR'unkiyle aynı): süre dolunca bağlar yeniden ölçülür, MAC sonuçları yeniden kanıt sayılır; bit, işaretler sürdükçe bildirilir. Böylece ardılım bu sırada ölür ya da uzaklaşırsa, uzun karıştırmada en geç 30 s sonra bırakılır (18 Kasım, bağımsız denetimin ikinci okuması Y-6; `kural/KK-01` kural 13).
- Gerekçe: Babel'in tepkisizliği kesik bağa göndermeyi sürdürüyor, v0.4.1'in aşırı tepkisi kalabalık kanaldaki her çarpışmada onarım başlatıyor. MAC sonucunu karar değil kanıt saymak bu ikisinin arasındaki seçimimdir.

**T-10 · Kanıtın eşiği: birkaç ardışık olay, iki yönde de.**
- "Karıştırılıyor" ve "bitti" kararları birkaç ardışık olayla verilir; sayılar 5-3'te.
- Erken dönmenin bedeli küçüktür: karıştırma sürüyorsa bağ birkaç olayda yeniden çıkar, hatırlanan kalite korunur (T-7).
- Karıştırmanın başlaması komşulukta bir değişim sayılır; selamlar sıklaşır (T-1) ve karıştırmanın bittiği daha çabuk duyulur.
- Gerekçe: birincil hücrede karıştırıcı 15 s açık kalıyor; tespit 5 s sürerse açık sürenin üçte biri kesik bağda geçer. İlk olayda karar kalabalık kanalda yanlış alarm üretir; kayan bir penceredeki oran Babel'in yavaşlığına döner. Doğruluk ile tepki hızı arasındaki değiş tokuş ETX'in de uyarısıdır [36].
- **Teşhis (d):** art arda üç MAC vazgeçmesi yanlış alarmı çerçevelerin %0,06'sının altında tutuyor, ama tek başına geç ve seyrek: alıcısı karıştırılan bağların yalnız %18'inde açık dönem içinde ulaşılıyor; ulaşılanların ortancası birincil hücrede 5,6 s, dayanıklılık hücresinde 2,8 s (orada açık dönem 10 s olduğu için uzun süreler kesiliyor). Olay sayısının ilk değeri 3; "karıştırılıyor" kararı MAC vazgeçmesini T-5'in işaretleriyle birlikte okur.

**T-11 · İsteğe bağlı geçiş: anlık ve düzgünleştirilmiş maliyet birlikte (19 Kasım).**
- Her aday yol için anlık maliyetin yanında zamanla düzgünleştirilmiş maliyet tutulur; zaman sabiti selam aralığının birkaç katıdır. Çalışan bir yoldan başkasına ancak ikisi birden daha iyiyse geçilir. Ardıl kullanılamaz olunca beklenmez (zorunlu geçiş, T-9); yalnız bir alternatifin iyileşmesi temkinle karşılanır.
- Gerekçe: eğime geçince (T-12) seçim her komşuya açılır ve maliyetteki dalgalanmayla sık yol değişimi riski artar. Babel'in kuralı dalgalanmayı süzer ve ölçeğe bağlı değildir; sabit fark eşiğinin kısa yolu donduran sorunu yoktur. 16 Kasım'da bu kural, T-2'nin ölçüm penceresinin üstüne ikinci bir yavaşlık ekleyeceği için seçilmemişti; seçim artık ölçülerek verilir.
- Önceki karar (16 Kasım): oransal eşik (%10; Ramachandran vd. 2007 [54]). Kodda bayrakla kalır; ikisi ölçülerek karşılaştırılır.
- Ödünç: Babel [4] (RFC 8966 Ek A.3); CTP'de eşik 1,5 ETX [68].

**5-3'e kalanlar:** "karıştırılıyor" ve "bitti" için olay sayıları · düzgünleştirmenin zaman sabiti (T-11) · kötü bağ (T-3) için de aynı olay sayısı kuralının geçerli olup olmayacağı.

---

## 4 · Yedek yol ve döngüsüzlük (16 Kasım)

Yedek, döngü yaratmadan geçilebilecek komşudur; hangi komşunun güvenli olduğunu döngüsüzlük kuralı söyler. Bu yüzden iki konu birlikte karara bağlandı. 19 Kasım'da T-12 ve T-13 değişti: döngü önlenmek yerine veri yolunda yakalanıp onarılır, açlık kalkar.

**Ölçülmüş kanıt** (`arsiv/teshis/faz5_2_rakip_cizgisi_2026-11-15/sonuc.md` §2 · `arsiv/teshis/faz5_2_anatomi_2026-11-14/sonuc.md` §5 · `arsiv/teshis/faz5_2_secenek_iletim_2026-11-15/sonuc.md` §5–§6):
- Birincil hücrede açık dönemde doğan paketlerin rota yokluğundan kaybı: Babel 0,000 · kâhin 0,008 · v0.4.1 0,237. Babel de FD kuralını kullanıyor; fark açlığın çözülüşünde.
- v0.4.1'de açık evredeki onarımların %67'si açlıkla, %33'ü aday yokluğuyla başlıyor.
- v0.4.1 açlıkta en az 6 s bekliyor ve yeni turu yalnız kendi paketiyle istiyor: ikizde 131 isteğe 2 yanıt. Babel hemen soruyor, seçili rotasına uygulanamaz bir güncelleme gelince rotayı bırakmıyor (`protokol_kaynaklari/faz5_arastirma_2026-10-21/NOTLAR.md` §5, §8).
- Yol istemek (`onarim_edinimi`) ikizde rota kaybını %40 azalttı (0,054 → 0,032); kazanç iletimde geri gitti (paket başına atlama +%17, kontrol kanal süresi +%45).
- Yedekleri yoklamayla canlı tutmak (`hedefli_canlilik`) rota kaybını azaltmadı. v0.4.1'de alınan duyuruların %64'ü işlenmiyordu; yedekler bilinmiyordu (T-1 bunu çözer).
- **Açlık teşhisi** (19 Kasım; `arsiv/teshis/faz5_3_aclik_2026-11-18/sonuc.md`): 16–18 Kasım kararlarıyla kodlanan çekirdeğin ikizdeki açığı (0,810 ↔ Babel 0,930) tamamen rota yokluğunda. Açlık bölümlerinin %69'u yukarıdaki düğümün ∞ ilanıyla açılıyor. Kayıp ağırlıklı köklerin %92'sinde, açlık başladığında elde olağan ve sonlu maliyetli ama uygulanabilirlik koşulunu geçemeyen bir komşu vardı.

**T-12 · Yol seçimi ve döngü: maliyet eğimi, veri yolunda döngü bekçisi (19 Kasım).**
- Ardıl, olağan ve sonlu ilanlı komşular arasında (bağ maliyeti + komşunun maliyeti) en küçük olandır. Önce maliyeti benim şimdiki maliyetimden küçük ("yokuş aşağı") komşulara bakılır; hiç yoksa son çare olarak en iyi sonlu komşu seçilir, maliyetim yükselir ve ara ilanla hemen duyurulur (T-17). Düğüm, olağan ve sonlu maliyetli bir komşusu olduğu sürece yolsuz kalmaz.
- Maliyet tavanı: yol maliyeti bir sınırı aşarsa yol yok sayılır ve ∞ ilan edilir. Kopan bir bölgede maliyetlerin karşılıklı tırmanması böyle durur. Tavan 5-3'te.
- Döngü bekçisi; veri başlığına alan eklenmez (`13` §02.5):
  - Bana iletilmek üzere veri gönderen komşunun selamında ilan ettiği maliyet benimkinden büyük değilse onun bilgisi bayattır ya da döngü vardır: hemen selam gönderirim (T-17).
  - Aynı paket (kaynak ve kaynak sırası) bana daha çok atlama yapmış olarak yeniden gelirse döngü kesindir: paket geldiği komşuya gönderilmez, ardıl yeniden seçilir, selam gider.
  - Paketin ömrü (TTL) son güvencedir; döngünün bedeli ömür kaybında ve atlama sayısında görünür (T-19).
- Döngüsüzlük artık garanti değildir: döngü önlenmez, oluşunca yakalanır ve onarılır. Bu RPL'nin ve CTP'nin yoludur [63], [68].
- Gerekçe: açlık teşhisi (yukarıda). Uygulanabilirlik koşulu, elde sonlu maliyetli komşu varken düğümü yolsuz bırakıyor; ∞ ilanı zincirleme açlık doğuruyor; kaybın kaynağı bu. CTP döngüyü veri yolunda yakalıyor, paketi düşürmüyor ve seyrek geçici döngünün bedelini genel iletim bedeline göre küçük buluyor [68]. CTP gönderenin maliyetini her veri paketine yazıyor; bizim simülatörde başlığa değer yazılamadığı için aynı bilgi komşunun selamından okunur, döngü de paketin kimliğinden ve atlama sayısından anlaşılır.
- Önceki karar (16 Kasım): uygulanabilirlik koşulu ve geçidin tur numarası (Babel [4], RFC 8966 §3.5.1, §3.7.3). Kodda bayrakla kalır; ikisi ölçülerek karşılaştırılır.
- Ödünç: maliyet eğimi ve veri yolunda doğrulama CTP [68] ve RPL [63]; "yokuş aşağı" koşulu LFA'nın aşağı akış yolu [61]. Son çare, maliyet tavanı ve başlıksız döngü bekçisi benim uyarlamam.

**T-13 · Açlık ve tur isteği (19 Kasım'da kalktı).**
- Eğimle (T-12) düğüm, olağan ve sonlu maliyetli bir komşusu olduğu sürece yolsuz kalmaz. Geçidin turu, açlıkta tur isteği, isteğin iletilmesi ve uygulanamaz güncellemenin yok sayılması gereksiz kalır.
- Önceki karar (16–17 Kasım): uygun komşu kalmayınca yeni tur hemen istenir (Babel [4], RFC 8966 §3.8.2). İlk ölçümde ikizde koşu başına 822 açlık ve 92 tur artışı (`arsiv/teshis/faz5_3_cekirdek_2026-11-18/sonuc.md`). Metnin tamamı `v2/arsiv/17-TASARIM-KARARLARI-2026-11-18.md`'de.

**T-14 · Yedek yol: hazır yedek kümesi, tek yoldan gönderim; çoğaltma yalnız son çare.**
- Olağan ve sonlu ilanlı bütün komşular yedektir; önce maliyeti benimkinden küçük olanlar (T-12; 19 Kasım). Ardıl kullanılamaz olunca (T-2, T-3, T-7) en iyisine anında geçilir. Yedekler için ek mesaj gönderilmez; selam (T-1) ve ilanlar yeter.
- Trafik komşulara bölünmez: bölme daha kötü bağa da trafik gönderir, açığın büyük kalemi ise zaten iletim kaybı.
- Seçici çoğaltma çekirdekte yoktur. Kullanılırsa yalnız son çare olarak, nadiren ve sıkı bir bütçeyle kullanılan bir yan özelliktir; 5-3'te ayrı bir bayrakla ölçülür, kazandırmazsa kalmaz. Gerekçe: bizim simülatörümüzde çoğaltma çok pahalı. Kanal kalabalık (veri denemelerinin yarısından fazlası başarısız) ve her pakete kopya toplu akışta kanalı boğuyor (JarmRout, K-238).
- Ödünç: hazır yedek fikri DUAL'ın uygulanabilir ardılı [65] (RFC 7868) ve RPL'nin ebeveyn kümesi [63]; seçici çoğaltma ilk taslağımdan (PROTECT).

**T-15 · Yedeklerin ayrışması: kanıtla.**
- "Karıştırılıyor" işaretli komşu (T-7) yedek sayılmaz. Karıştırılan bölge kanıttan görünür; konum gerekmez.
- Konum selama eklenmez: karıştırıcının yeri bilinmediği için ardıldan uzak bir yedeğin neye yarayacağı belli değil, bedeli ise her selamda ödenir.
- K-230'un sorusunun cevabı budur.
- Ödünç: ortak düğüm riski fikri Tague vd. 2011 [53].

**5-3'e kalanlar:** maliyet tavanı (T-12) · "son çare"nin tanımı ve kopya bütçesi · yedeklerin sıralanması.

---

## 5 · Kontrol yükü ve bekletme (16 Kasım)

**Ölçülmüş kanıt** (karıştırıcısız ikiz, 350 s; `arsiv/teshis/faz5_2_secenek_iletim_2026-11-15/sonuc.md` §1, §5 · `arsiv/teshis/faz5_2_anatomi_2026-11-14/sonuc.md` §4–§5 · `arsiv/teshis/faz5_2_rakip_cizgisi_2026-11-15/sonuc.md` §2):
- Kontrol trafiğinin toplam gönderim süresindeki payı: v0.4.1 %32 · Babel %14 · kâhin %6. v0.4.1'in kontrol kanal süresi Babel'inkinin 2,69 katı.
- v0.4.1 ~35 000 yoklama ve 35 823 ilan gönderiyor (24 122'si tetik ilanı); aynı sürede veri iletimi 34 016.
- Kanaldaki toplam gönderim süresi her 100 s arttığında alıcıların çerçeveye kilitlenme payı kabaca 2 puan düşüyor.
- v0.4.1 1 s'de bir ve her ardıl değişiminde ilan ediyor (alan başına saniyede 5'e kadar). Babel'de selam 4 s, ters yön bildirimi 12 s, güncelleme 16 s'de bir (`protokoller/babel_bicim.py`); küçük değişimler için tetik yok.
- Gecikmenin p99'u (ikiz · birincil · dayanıklılık; 8 tohum): Babel 0,23 · 1,31 · 0,72 s · v0.4.1 2,51 · 3,67 · 3,51 s · kâhin 0,14 · 0,33 · 0,27 s. 5 s'lik gecikme tavanı hiçbir hücrede sonucu değiştirmiyor (en çok 0,010).
- v0.4.1 onarımda alan başına 6 paketi en çok 6 s bekletiyor; ikizde rota yokluğuna (`rota_gecersiz`) düşen paketlerin %64'ü bu kota doluyken düşüyor. Babel bekletmiyor.

**T-16 · Uzaklık ilanı selamla tek iletidir.**
- Selam, geçide maliyetimi, seçili rotamın turunu ve o anki aralığını da taşır; T-1'in uyarlanır aralığıyla gider. Ayrı ve düzenli bir ilan iletisi yoktur.
- Selam bastırılmaz: komşular benim bağımı selamlarımın sıra numarasından ölçer (T-2).
- Gerekçe: tek hedef olduğundan ilan birkaç bayttır (tur ve maliyet); her çerçevenin 64 baytlık sabit ek yükü (`13` §03.1) ve kanal erişimi bir kez ödenir. Ölçek için: 1 s'de bir ilan, 40 düğümde 350 s'de tek başına 14 000 çerçeve eder; 4 s'de bir birleşik selam 3 500.
- Ödünç: aralığın uyarlanması Trickle [62]; Trickle'ın bastırması alınmadı. Bir pakette birden çok bilgi taşımak Babel'de de var [4] (RFC 8966 §4.2).

**T-17 · Ara ilan yalnız önemli değişimde.**
- Ara ilan şu durumlarda gider: maliyet belli bir oranda değişince · döngü işareti görülünce (T-12) · yol kaybolunca ya da geri gelince · "karıştırılıyorum" durumu değişince (T-6). Düğüm başına bir sıklık sınırı vardır.
- Gerekçe: v0.4.1'de her ardıl değişiminde giden ilan, ardıl 1,3 saniyede bir değiştiği için kanalı dolduruyordu (24 122 tetik ilanı). Kötü haber ise beklemeden yayılmalı.
- Ödünç: Babel [4] (RFC 8966 §3.7.2: küçük dalgalanmalar ve maliyeti belirgin değiştirmeyen ardıl değişimleri için tetik gönderilmez).

**T-18 · Bekletme: kısa ve küçük tampon, dolunca en eskisi düşer.**
- Yol yokken gelen paket, yol bulunana kadar küçük bir tamponda kısa süre tutulur; bir düğümdeki tutma süresi 5 s'lik gecikme tavanını aşmaz. Tampon dolunca en eski paket düşer.
- Paketin yaşı protokole görünmez (`dogum_s` yok, saatler eşzamanlı değil; `05` §3.2). Birkaç röle sırayla tutarsa uçtan uca gecikme 5 s'yi aşabilir. Sınırın türü (atlama başına sınır ve paketin en çok kaç kez tutulabileceği ya da başlıkta bedeli ödenen birikmiş bekleme) 5-3'te seçilir (§7).
- Paket karıştırıcı susana kadar saklanmaz (sakla-taşı-ilet yok).
- Gerekçe: tampon, yol yokken geçen kısa aralığı köprüler. Eğimle (T-12) yol ancak hiç sonlu komşu kalmayınca yoktur; tampon seyrek çalışır. Telemetri saniyede bir üretildiği için tutma süresi 5-3'te yeniden seçilir (19 Kasım). Telemetride en taze paket değerlidir. 15 s'lik saklama telemetrinin değerini yitirir ve karıştırıcı susunca biriken paketleri kanala aynı anda döker. `PDR_açık` geç teslimi de saydığı için uzun saklama ölçüyü yanıltıcı biçimde yükseltirdi (K-246).
- Ödünç: bekletme v0.4.1'de de var (alan başına 6 paket, 6 s); dolunca en eskiyi düşürme benim seçimim.

**T-19 · Kontrol yükü ve gecikme her ölçümde görünür.**
- Kontrol trafiğinin kanal süresindeki payı, 5-3'teki her A/B'de ikincil ölçü olarak raporlanır. Her mekanizmanın kontrol bedeli böylece görünür kalır.
- Gecikme tavanlı `PDR_açık` (5 s) ve gecikmenin p99'u da her A/B'de raporlanır: bekletme davranışı değişiyor ve `PDR_açık` geç teslimi de sayıyor (K-246) (17 Kasım, denetim Ö-7).

**5-3'e kalanlar:** tamponun boyutu ve süresi · tetik eşikleri ve sıklık sınırı · selamın biçimi ve boyutu.

---

## 6 · Komutun yolu (17 Kasım)

**Ölçülmüş kanıt** (teşhis (c), v0.4.1, 8 tohum; `arsiv/teshis/faz5_2_rakip_cizgisi_2026-11-15/kayit_v041_ikiz.json` · `kayit_v041_karistirma.json`, `teshis_toplam`): komut iletme kararlarının ikizde %95,7'sinde, birincil ve dayanıklılık hücresinde %92,9 · %93,2'sinde taze bir geri iz hazırdı. Kalanında iz yok ya da bayat ve v0.4.1 komutu düşürüyor.

**T-20 · Komut telemetrinin geri iziyle gider.**
- Her röle, bir düğümün telemetrisini hangi komşudan aldığını hatırlar; o düğüme giden komut o komşuya verilir. Ek ileti gerekmez.
- İzi olmayan ya da bayatlamış komut düşürülmez. Kısa tamponda (T-18) bekler; hedefin bir sonraki telemetrisi izi tazeleyince yola çıkar.
- Gerekçe: telemetri her düğümden saniyede bir geldiği için iz tazedir. Bağ maliyeti iki yönde ölçüldüğü için (T-2) iyi bir yukarı bağın tersi de iyidir. Yukarı yol karıştırmadan kaçınca sonraki telemetri izi de yeni yola taşır. Ayrı bir aşağı yön ilanı (RPL'nin DAO'su [63]) ek kontrol trafiği ister. Kaynak rotası (K-232) her komutta adres başına bayt ister ve yolun ortasında kopan bağı onaramaz.
- Ödünç: v0.4.1'in geri izi (V11, K-172).

**5-3'e kalanlar:** izin tazelik süresi · izsiz komutun bekleme süresi.

---

## 7 · 5-3'ün açılış listesi (17 Kasım)

Geliştirmeye geçerken ilk ele alınacaklar; bölüm sonlarındaki "5-3'e kalanlar"a ek olarak, 5-2'nin bağımsız denetiminden (`arsiv/denetim/DENETIM-RAPORU-5-2-2026-11-17.md`).

**İlk kural kâğıdı:**
1. Bağın üç durumu (olağan · kötü · karıştırılıyor) ve geçişleri: "karıştırılıyor" iken toplanan örnekler bağ ölçüsüne girmez (T-7); T-3'ün iki eşiği ile T-7'nin dönüşünün sırası; ölçüm penceresinin her durumda nasıl tutulduğu (denetim Ö-6).
2. Selamın biçimi: aralığını taşır (T-1, T-16); ara ilan (T-17) bir selam mı (sıra numarası alır, aralığın zamanlayıcısını sıfırlar mı), ayrı bir ileti mi (Ö-10).
3. Selam aralığının üst sınırı, sessizliği fark etme süresi (kaçan selam sayısı × aralık) ve kontrol payı (T-19) birlikte seçilir. 4 s'lik aralıkla üç kaçan selam 12 s eder; dayanıklılık hücresinin 10 s'lik açık döneminden uzun (Ö-5).
4. Tamponun sınırının türü (T-18); komutla telemetrinin tamponu paylaşması ve önceliği (T-20). Birincil metrikte komutların yeri açık karar (KR-2, `04` §10) (Ö-7).
5. T-20'nin izi "karıştırılıyor" (T-7) ya da "kötü" (T-3) işaretli bir komşuyu gösteriyorsa iz bayat sayılır mı (Ö-10).

**Yeni sürümle ölçülecekler:**
6. Komşu başına sessizlik ve komşu başına en uzun boşluk: ayırma gücü ve yanlış alarm, temizdeki 0,44'lük selam kaybı tabanıyla; komşuların kanıtını birleştirmenin çok atlamalı dünyamızdaki kazancı (Ö-2; Puñal'in sonucu tek atlamalı düzenekte).
7. Girişim bölgesinde birleşik kanıt kuralının başarısı (birkaç işaret, birkaç saniye) ve düşüşün düğümün kendi yakın geçmişine göre okunması. Teşhis (d)'de alanlar karıştırmadan önce de temizden ayrışıyordu; aynı alanın öncesine göre işaretler daha güçlü (Ö-1; denetim §2.2).
8. Bağ kalitesinin değişim hızı tek deneme başarısıyla ve yedekler dâhil bütün komşu bağlarıyla (Ö-3).
9. İşaretlerin yeni sürümün trafiğinde ve en az bir başka karıştırıcı sınıfında (darbeli, reaktif, aldatıcı, taramalı) ya da yer karıştırıcılı ailede yeniden ölçülmesi (Ö-4).
10. Çizelgeli karıştırmada tur artışının sayılması: yedeğe geçiş → ara ilan → uygulanamaz güncelleme → tur isteği zinciri her dönemde yinelenebilir ve T-13'ün "tur düzenli artırılmaz" gerekçesine ters işleyebilir (denetim §2.3). 19 Kasım: tur kalktı (T-13); ilk ölçümde ikizde koşu başına 92 artış sayılmıştı.

**Kayıt ve ön-kayıt:**
11. Mekanizmaların ablasyon bayraklarına eşlenmesi ve Aile 3'ün mekanizma kapısına hangilerinin gireceği. `06` §0.4.5 eski adları ("5.1 karıştırma kanıtı · 5.3 postür · 5.4 PROTECT") taşıyor; mühürden önce bu belgeyle hizalanır (Ö-10).
12. `rssi_olcum_sigma_db` ve `gps_dikey_sigma_m` SINANMAMIŞ kayıtları (`04` §9): RSSI başlangıç kuralında okunmuyor (`kural/KK-03`; tutarlılık zayıf çıktı), A/B'de okunursa duyarlılığı ölçülür; kendi konumun okunup okunmayacağı yazılır (T-15 yalnız selama konum eklenmeyeceğini söylüyor) (Ö-10).
13. Kaydedici yeni sürümle yeniden kullanılırsa evre, ikiye bölme, selam kaybı ve bağ birimlerinin gruplanması için sentetik testler (K-9).
