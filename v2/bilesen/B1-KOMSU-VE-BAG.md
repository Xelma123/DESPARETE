# B1 · Komşu ve bağın ölçüsü

> Yeni tasarımın (`../18-YENI-TASARIM.md`) birinci bileşeni. İskelet `18` §1.4; sorun, kanıt, seçenekler ve kararım `18` §2.1 (24 Kasım). Değerler, bayraklar ve gözlemin kullanımı yalnız `00-DIZIN.md`de; burada adlarıyla anılır. Durum: onaylandı (24 Kasım). Önceki tasarımda karşılığı `../kural/KK-01` (orada ölçü ile bağın durumu tek kâğıttaydı; durum artık B3'te).
>
> Eksiksizlik listesinin maddeleri (`18`): 1 §1 · 2–4 `18` §2.1 · 5 §2 · 6 §3 · 7 §4 · 8 §5 · 9 §6 · 10 §7 · 11 §8 · 12 §9 · 13 §10 · 14 §11 · 15 §12 · 16 §13 · 17 §14.

## 1 · Amaç ve sınıf

B1 komşuların kim olduğunu, her bağın iki yönde ve veri için ne kadar iyi olduğunu ve bu bilgilerin ne kadar taze olduğunu ölçer. Karar vermez: bağın kullanılıp kullanılmayacağı, maliyeti ve "bu bağ veri taşımıyor" yargısı B3'ündür (`18` §1.4 sözleşme 3).

- **Sınıf:** genel (K-247). Çekirdeğin parçasıdır, bayrağı yoktur (§10).
- **Hizmet ettiği hedef** (`18` §1.1): bağ seçiminin kalitesi. Birincilde açık dönem kaybının büyüğü iletimde (0,267–0,335; `arsiv/teshis/faz5_3_dongu_kurallari_2026-11-24/sonuc.md` §8); ikizde Babel'le iletim farkının yaklaşık yarısı seçilen bağın kalitesinden (`arsiv/teshis/faz5_2_secenek_iletim_2026-11-15/sonuc.md` §5). Koruma ölçütlerinden en kötü tohuma (iyi bağların yanlışlıkla düşmemesi) ve kontrol payına (ek ileti yok) dokunur.

## 2 · Gördüğü (`05`; yasak alanlar okunmaz)

| gözlem | B1'in kullandığı | kullanmadığı |
|---|---|---|
| selam (`kontrol_alindi`; iletiyi B6 çözer) | gönderen, sıra, aralık (bir sonraki selama kadarki üst sınır, s), gönderenin benim için bildirdiği oran ya da "listede yokum" | maliyet (B4'ün), karıştırma biti (B2'nin) |
| `iletim_sonucu` (niyet döndürmez) | hedef, onay geldi mi, `tekrar`. Ölçüye yalnız tür `veri` (telemetri ve komut) girer; onayın gelmesi her türde varlık kanıtıdır (kural 2) | kontrol çerçevelerinin deneme sayısı: boyları veriden farklı |
| `cerceve_duyuldu` (niyet döndürmez) | gönderen; yalnız tür `veri` ve `kontrol` | duyulan onay ve kontrol onayı (`onay`, `konay`): gerçek 802.11'de onay çerçevesi verici adresi taşımaz, simülatör bildirse de okunmaz · RSSI: hata modeli sınanmamış (K-233) ve çarpışmayı göstermez · hedef ve paket başlığı (B4'ün ve B7'nin) |
| `saat_s` | yalnız süreler; saatler senkron değil (`05` §3.2) | — |

**Okumadıkları:** `olculen_gurultu_w` (yasak, K-227) · `phy_hata`, `alinan_cerceve`, `mesgul_sure_s` (B2'nin işaretleri) · `kendi_konum`, `kendi_hiz` · `komsular` (simülatörün beacon listesi; protokolün kendi selamı var, `kosum_beaconi = False`, beacon gönderilmez) · kuyruk.

**`tekrar`:** MAC'in ilk denemeden sonraki yeniden iletim sayısı (`sim2/kosum/kontrol.py`: `deneme − 1`). Deneme sayısı `tekrar + 1`, 1–7; vazgeçmede 7 (referans dünyada yeniden deneme sınırı 6, K-223).

## 3 · Tuttuğu

Komşu j başına:

| alan | başlangıç | güncellenir | silinir | üst sınır |
|---|---|---|---|---|
| `ilk_t` | kayda giriş anı | — | kayıtla | — |
| `son_duyulma_t` | kayda giriş anı | j'den çözülen her veri ve kontrol çerçevesinde ve j'ye giden çerçevemin onayında (kural 2) | kayıtla | — |
| selam örnekleri: (an, geldi 1 / gelmedi 0, j'nin benim için bildirdiği oran ya da yok) | ilk selam: tek örnek (an, 1, oranı) | kural 4, 5, 7 | kural 6 (saklama), yeniden başlama (kural 4), kayıtla | `SELAM_SAKLA` |
| `beklenen` (beklenen sıra) | ilk selamın sırası + 1 | her örnekte | kayıtla | 16 bit, modüler |
| `son_selam_t` | ilk selamın anı | her gerçek selamda | kayıtla | — |
| `a` (j'nin son ilan ettiği aralık) | ilk selamın aralığı | her selamda | kayıtla | — |
| `asim_t` (bir sonraki zaman aşımı) | `son_selam_t + ZAMAN_ASIMI_KATSAYI · a` | kural 4, 5 | kayıtla | — |
| veri kayıtları: (an, deneme 1–7, onay geldi mi) | boş | kural 8 | kural 9, kayıtla | `VERI_SAKLA` |

Kanca başına: bu kancada açılan ve silinen komşuların listesi (kural 18); bir sonraki kancanın başında boşalır.

**Bellek:** komşu tablosu en çok 255 kayıt (selamdaki adres 8 bit, düğüm kimliği < 256; referans dünyada 39 komşu); düğüm başına en çok 255 × (`SELAM_SAKLA` + `VERI_SAKLA`) örnek.

## 4 · Durumlar ve geçişler

B1'in bağ için durumu yoktur; OLAĞAN, KÖTÜ, KARIŞTIRILIYOR gibi durumlar B3'tedir. B1'in iki yaşam döngüsü vardır:

| döngü | durumlar | geçiş ve tetikleyici | çıkış |
|---|---|---|---|
| komşu kaydı | yok · kayıtlı | yok → kayıtlı: j'den ilk selam (kural 1) · kayıtlı → yok: `T_SILME` boyunca j'den hiç çerçeve duyulmadı (kural 3) | kayıtlıdan tek çıkış silmedir ve zamanla kendiliğinden gelir; yoktan çıkış ilk selamdır; takılı kalma yok |
| `d_f` | tanımsız · biliniyor | tanımsız → biliniyor: j'nin beni listeleyen selamı · biliniyor → tanımsız: o bildirimden beri `DF_UNUT_S` geçti (kural 12) | ikisinden de çıkış var (bildirim ya da süre) |

Selam sayımındaki "yeniden başlama" (kural 4) kaydı silmez, yalnız örnekleri siler.

## 5 · Kurallar

**A · Komşunun varlığı**

1. **Kayda giriş:** j'den ilk selam alınınca kayıt açılır; o selam ilk örnektir (an, 1, oranı) ve `beklenen` = sıra + 1. Selam dışındaki çerçeveler kayıt açmaz: ölçü selamın sıra numarasıyla başlar. Kayıt açılınca "yeni komşu" olayı oluşur (kural 18).
2. **Duyulma:** j'den çözülen her veri ve kontrol çerçevesi (bana ya da başkasına adresli) ve j'ye gönderdiğim bir çerçevenin onayı (`iletim_sonucu` başarılı; veri ya da kontrol) `son_duyulma_t`'yi o ana çeker. Onayın göndericisi ancak kendi çerçeveme yanıtsa bellidir: MAC onayı bekleyen çerçevesiyle eşler. Başkasına giden onaylar kullanılmaz (§2). Kayıtta olmayan göndericinin çerçevesi yok sayılır.
3. **Silme:** `son_duyulma_t + T_SILME` geldiğinde kayıt silinir ve "silinen komşu" olayı oluşur. B1 kendi karıştırılmamı bilmez (B2 ondan yukarıdadır); silme bu sırada da sürer (§11 madde 2).

**B · Selam sayımı** (RFC 8966 Ek A.1'in kuralları; fark = sıra − `beklenen`, 16 bit modüler, `00-DIZIN` "Ortak birimler")

4. **Selam gelince** (j kayıtlıyken), farka göre:
   - **fark = 0:** (an, 1, oran) eklenir.
   - **0 < fark ≤ `BOSLUK_EN_COK` (ileri sarma):** fark kadar 0, sonra (an, 1, oran) eklenir. Sıfırların anları `son_selam_t` ile şimdi arasına eşit aralıkla dağıtılır: k'ıncı sıfırın anı `son_selam_t + k · (şimdi − son_selam_t) / (fark + 1)`. Kaçan selamlar bu arada gönderilmiştir; hariç aralığın (kural 10) doğru çalışması için sıfıra ortaya çıktığı an değil, selamın gönderildiği tahmini an yazılır.
   - **−`BOSLUK_EN_COK` ≤ fark < 0 (geri alma):** son (−fark) örnek silinir (o kadar örnek yoksa hepsi), sonra (an, 1, oran) eklenir. Bu örnekler zaman aşımının saydığı sıfırlardır: zaman aşımı, komşunun hiç göndermediği selamları da kayıp saymıştır. Sıra ilerlemediyse onlar kaybolmamıştır. Babel'in gerekçesi aralığın fark edilmeden uzamasıdır; bizde bir sebep daha var: kanal kilidindeki komşu selam gönderemez (B1 Ö-5).
   - **|fark| > `BOSLUK_EN_COK` (yeniden başlama):** örnekler silinir, (an, 1, oran) eklenir. Kayıt kalır.
   - **Her durumda:** `beklenen` = sıra + 1, `son_selam_t` = şimdi, `a` = max(selamın aralığı, `ARALIK_EN_AZ`), `asim_t` = şimdi + `ZAMAN_ASIMI_KATSAYI` · `a`.
5. **Zaman aşımı:** `asim_t` gelince (an `asim_t`, 0, oran yok) eklenir, `beklenen` bir ilerler, `asim_t` ← `asim_t` + `a`. Komşu susarsa her `a`'da bir sıfır daha eklenir. `a` komşunun bir sonraki selamına kadarki üst sınır olduğu için olağan aralık uzaması sahte kayıp üretmez (Ö-2).
6. **Saklama:** örnek sayısı `SELAM_SAKLA`'yı aşınca en eskisi atılır. Ölçü yalnız son `N_SELAM` örneğe bakar (kural 11); fazlası, hariç aralıktan (kural 10) sonra karıştırmadan önceki kaliteyi geri getirmek için saklanır.

**C · Ters yön bildirimi**

7. j'nin selamı beni listeliyorsa bildirdiği oran (0–1 arası gerçek sayı; alanı B6 çözer) o selamın örneğine yazılır. Listelemiyorsa örnekte oran yoktur: "bilinmiyor", önceki bildirim geçerli kalır (önceki tasarımda Y-12).

**D · Veri kaydı**

8. `iletim_sonucu` tür `veri` ve hedefi kayıtlı bir komşu j iken (an, `tekrar + 1`, onay geldi mi) eklenir. Başarısızlık burada yalnız vazgeçmedir (MAC 7 denemenin hepsini bitirdi); ara denemelerin başarısızlığı deneme sayısında görünür. Kontrol çerçevelerinin sonucu ve kayıtta olmayan komşuya gidenin sonucu yazılmaz. Kopya eşleri (`kopyalar`, `13` §07) veri çerçevesi olduğu için yazılır.
9. **Saklama:** `VERI_PENCERE_S`'den eski kayıt ve `VERI_SAKLA`'yı aşan en eski kayıt atılır.

**E · Ölçüler** (B1'in çıktısı; istendiği anda hesaplanır; hesap yalnız burada yapılır, `18` §1.4 sözleşme 3)

10. **Hariç aralık:** her ölçü isteğe bağlı bir hariç aralık listesiyle istenebilir; her aralık [başlangıç, bitiş], bitişi ∞ olabilir. Anı bir hariç aralığa düşen örnek ve kayıt sayılmaz. Listeyi B3'ün karıştırma eki verir: karıştırılan bağın ve kendi karıştırılmamın aralıkları, B2'nin kanıtıyla. Karıştırma katmanı kapalıyken liste boştur.

    Neden bu yapı (iskeletin gerektirdiği; seçilmeyen iki yol):
    - **B1'in karıştırma sırasında dondurulması** (önceki tasarım, KK-01 kural 9, 13): B1 karıştırmayı bilemez, B2 ondan yukarıdadır (sözleşme 1). B3'ün B1'i dondurması başkasının durumuna yazmak olurdu. Dondurma B2 için ikinci bir sayım ("gölge geçmiş", Y-10) da gerektirmişti.
    - **B3'ün karıştırmadan önceki değeri kendisinin saklaması:** saklanan değer karıştırmadan sonra gelen örneklerle birleştirilemez. Birleştirmek için B3'ün ölçüyü yeniden hesaplaması gerekir (sözleşme 3, tek kaynak).

    Seçilen yolda formül B1'de kalır; hangi anların sayılmayacağını yukarıdaki bileşen söyler. Liste okuma isteğinin parametresidir, B1'in durumuna yazılmaz.

    Hesap en yeni örnekten geriye doğru yapılır ve gereken sayıda (`N_SELAM`, `VERI_PENCERE`) sayılan örnek bulununca durur. Hariç aralık yokken iş önceki tasarımın hesabı kadardır; koşu süresi uzamaz.
11. **`d_r` (j'den bana gelen yön):** hariç olmayan en yeni `N_SELAM` örnekte 1'lerin payı; dayandığı örnek sayısı `n_s`. `n_s` = 0 ise tanımsız.
12. **`d_f` (benden j'ye giden yön):** hariç olmayan ve oranı olan en yeni örneğin oranı. Öyle bir örnek yoksa ya da `DF_UNUT_S`'den eskiyse tanımsız.
13. **`E_selam` = 1 / (`d_f` · `d_r`)** (ETX [36]); biri tanımsız ya da 0 ise ∞ (tek yönlü bağ). Birimi beklenen deneme sayısıdır.
14. **Verinin ölçüsü:** hariç olmayan, `VERI_PENCERE_S` içindeki en yeni `VERI_PENCERE` kayıt üzerinden `n_v` (kayıt sayısı), `D` (toplam deneme), `G` (onay gelen kayıt):
    - `E_veri = D / G`: onaylanan bir paket başına harcanan deneme. Vazgeçilen paketin 7 denemesi de sayılır. `G` = 0 ve `n_v` > 0 ise ∞; `n_v` = 0 ise tanımsız.
    - **vazgeçme payı** = (`n_v` − `G`) / `n_v`; `n_v` = 0 ise tanımsız.

    `E_veri` veri çerçevesini ve onayını gerçek boylarıyla, çarpışmalar dâhil ölçer; ETX'in tahmin etmeye çalıştığı şey budur (4B [69]: veri onayının bağ ölçüsüne girmesi). `E_selam` ile aynı birimdedir; ikisinin nasıl birleştirileceği B3'ün kararıdır.
15. **Tazelik:** `ilk_t`, `son_duyulma_t`, `son_selam_t`, en yeni veri kaydının anı, `n_s`, `n_v` ve `d_f`'nin dayandığı bildirimin anı.
16. *Kaldırıldı (28 Kasım, Aşama 3):* sondaki sessizliği (ham örneklerin sonundaki ardışık sıfırlar) ne B2 ne B3 kullanıyor (B2 §2, B3 §2; `01-BUTUNLUK.md` §11). Numara korunur.
17. **Bildirilecek oran listesi (B6 için):** `n_s` ≥ `ORNEK_EN_AZ` olan her komşunun adresi ve `d_r`'si, adrese göre sıralı. Hangi hariç aralıkla isteneceği B3 ile B6'nın kararıdır (§11 madde 3). Tek örnekle 1,0 bildirilmez.
18. **Olaylar:** bu kancada açılan ("yeni komşu") ve silinen ("silinen komşu") kayıtların listesi. Kanca boyunca okunur, bir sonraki kancanın başında boşalır.
19. **Son tarih:** bekleyen en erken zaman olayının anı (zaman aşımı ya da silme). B1 uyandırma istemez; istenip istenmeyeceği B6'nın kararıdır (Ö-6).

**F · Sıra**

20. Her kancanın başında B1 o ana kadar gelmiş zaman olaylarını (kural 3, 5) kendi anlarının sırasıyla işler. Aynı anda olanlarda önce zaman aşımı, sonra silme gelir; komşular arasında küçük adres önce işlenir. Sonra kancanın gözlemini işler. Böylece her gözlem, B1'in o ana kadar güncel hâline uygulanır. Bütün bileşenler için ortak kural `01-BUTUNLUK.md` §4'tedir; `18` §1.4'ün olay sırası buna göre düzeltildi (28 Kasım): zaman olayları 1., gözlemin dağıtımı 2. adımdır.

## 6 · İletiler

B1 ileti göndermez; kontrol yüküne doğrudan katkısı yoktur. Ölçünün çalışması için selamdan beklediklerim (B6'ya; Aşama 2.6'da kapanır, bütünlük denetiminde denetlenir):

- **Ö-1** Her düğüm yayın selamı gönderir. Selamda 16 bitlik, 0'dan başlayan ve her selamda bir artan sıra numarası bulunur.
- **Ö-2** Selam, bir sonraki selama kadarki sürenin üst sınırını taşır (aralık alanı, RFC 8966 §4.6.5). Aralık uzarken yeni aralığın üst sınırı yazılır; alıcı sahte kayıp saymaz.
- **Ö-3** Selamda komşu listesi bulunur: kural 17'nin listesi (adres, oran). Komşu, benden kendisine giden yönün oranını (`d_f`) yalnız benim listemden öğrenir; listede olmayan komşuyla bağ ölçülemez. Her komşu en geç `DF_UNUT_S` içinde bir kez listelenmelidir. Listenin bedeli komşu başına adres ve oran bitleridir; önceki biçimde 2 bayt, 15 komşuyla 30 bayt.
- **Ö-4** İki selam arası en az 0,5 s olur; `SELAM_SAKLA` ve `BOSLUK_EN_COK` buna dayanır, değişirse yeniden hesaplanır.
- **Ö-5** Sırası tüketilen selam gönderilmelidir: sırası tüketilip hiç gönderilmeyen selamı alıcı kayıp sayar, geri alma (kural 4) onu silemez. Önceki tasarımda kendi kanal kilidimde selam hiç kurulmuyordu (KK-02 kural 5, karıştırma katmanına bağlıydı); kanal kilidindeki komşunun sessizliği, selamı dönünce alıcıda geri almayla iz bırakmadan kapanıyordu (§12). Kanal açılınca kuyrukta bekleyen eski selamların gönderilmesi de geri almayı bozmaz, çünkü ilk gelenin sırası bir sonraki sıradır. Bayat içeriğin sakıncası B6'nın sorusudur.
- **Ö-6** B1'in son tarihi (kural 19) için uyandırma kurulup kurulmayacağı kararlaştırılır. Kurulmazsa zaman olayları en geç bir sonraki kancada işlenir; anları doğru yazıldığı için ölçü değişmez, yalnız yukarıdaki bileşenlerin tepkisi gecikir.
- **Ö-7** Yeni komşu olayının karşılığı kararlaştırılır (önceki tasarımda selam hızlanıyordu, KK-02 kural 3). Yeni komşunun iki yönde ölçülmesi her iki tarafta en az `ORNEK_EN_AZ` selam ister.

## 7 · Değerler

`N_SELAM` · `SELAM_SAKLA` · `ZAMAN_ASIMI_KATSAYI` · `ARALIK_EN_AZ` · `BOSLUK_EN_COK` · `ORNEK_EN_AZ` · `DF_UNUT_S` · `T_SILME` · `VERI_PENCERE` · `VERI_PENCERE_S` · `VERI_SAKLA`. Değeri, birimi, kaynağı, küçük ve büyük olursa ne olacağı ve taranıp taranmayacağı `00-DIZIN.md`'nin değer tablosunda.

## 8 · Kenar durumlar

- **Soğuk açılış:** tablo boştur; t = 0'da kimse kimseyi bilmez (`05` §3.5). j'nin ilk selamıyla kayıt açılır. `E_selam` iki yönün ölçülmesini ister: j beni ancak benden `ORNEK_EN_AZ` selam aldıktan sonra listeler, en kısa aralıkta yaklaşık 2 s. O zamana kadar `d_f` tanımsız, `E_selam` ∞.
- **Geçit:** B1 geçitte de aynı çalışır. Geçidin veri kaydı gönderdiği komutlardan oluşur.
- **Hiç komşu yok:** bütün ölçüler boş, olay yok. **Tek komşu:** özel bir durum yok.
- **Düğüm kendisi karıştırılırken:** B1 bunu bilmez, olanı kaydeder. Girişimdeyken kaçan selamlar sıfır, başarısız veriler vazgeçme olarak yazılır. Kanal kilidinde gönderemem, veri kaydı oluşmaz; duyamadığım için sıfırlar eklenir. Hariç aralık B3'ten gelir (kural 10). 30 s'den uzun sürerse komşular silinir (§11 madde 2).
- **Komşu karıştırılırken:** kanal kilidindeki komşu selam gönderemez. Zaman aşımı sıfır ekler; selamı dönünce sıra ilerlemediği için geri alma bu sıfırları siler (Ö-5). Girişimdeki komşunun selamları gönderilir ama kaybolur; bu sıfırlar gerçektir, hariç aralıkları B3'ten gelir.
- **Sayaç taşması:** sıra modüler karşılaştırılır; 65535'ten sonra 0 gelir ve fark 1'dir.
- **Komşu yeniden başlarsa** (sıra farkı > `BOSLUK_EN_COK`): örnekler silinir, kayıt kalır. Simülatörde düğüm yeniden başlamaz; ölen düğüm susar ve silinir.
- **Zaman aşımı:** kural 5. Komşu susarsa her `a`'da bir sıfır eklenir, örnek sayısı `SELAM_SAKLA`'da doyar, `T_SILME`'de kayıt silinir.
- **Aralık 0 ya da çok küçük:** `ARALIK_EN_AZ` zaman aşımının sonsuz döngüye girmesini önler.
- **Komşu beni listelemiyor:** `d_f` önceki bildirimden gelir; `DF_UNUT_S`'den sonra tanımsız olur, `E_selam` ∞.
- **Aynı anda gelen olaylar:** kural 20. Selam tam zaman aşımı anında gelirse önce sıfır eklenir, sonra selamın geri alması onu siler; net etki yok. Silme anında aynı komşudan çerçeve gelirse (kayan noktada tam eşitlik; pratikte görülmez) kayıt silinir; gelen selamsa kayıt yeniden açılır. Takılı kalma yok.
- **Veri gönderilmeyen bağ:** `n_v` = 0, `E_veri` tanımsız. Bu "kötü" değil "bilinmiyor"dur (§11 madde 5).
- **Tamponun dolması:** B1'in tamponu yoktur. Tabloların sınırı §3'te: dolunca en eski örnek atılır; komşu tablosu 255'i aşamaz.

## 9 · Arayüz

**Kancalar:**

| kanca | B1'e giden | B1'in işi |
|---|---|---|
| her kancanın başı | şimdi | zaman olayları (kural 20); olay listeleri boşalır |
| kontrol iletisi alındı, selam | gönderen, sıra, aralık, benim için oran ya da yok | kural 1, 4, 7 |
| iletim sonucu (niyetsiz) | hedef, onay geldi mi, `tekrar`, tür | kural 2, 8 |
| çerçeve duyuldu (niyetsiz) | gönderen, tür | kural 2 |
| saniyelik zamanlayıcı, uyandırma, iletim başarısız, sonraki atlama | — | yalnız zaman olayları |

**Çıktılar ve okuyanlar:**

| çıktı | kural | okuyan |
|---|---|---|
| komşu kümesi; yeni ve silinen komşu olayları | 1, 3, 18 | B2, B3, B4 (kendi kayıtlarını budarlar), B6 (yeni komşu olayı, Ö-7) |
| `d_r`, `d_f`, `E_selam` (hariç aralıkla) | 11–13 | B3 |
| `E_veri`, vazgeçme payı, `n_v` (hariç aralıkla) | 14 | B3 |
| tazelik | 15 | B3, B2 |
| selam örnekleri, `son_selam_t`, `a` | 4–6 | B2 |
| bildirilecek oran listesi | 17 | B6 (B3 üzerinden, §11 madde 3) |
| son tarih | 19 | B6 |

**Olay sırası** (`18` §1.4): B1 her kancada olay sırasının ilk iki adımında çalışır: önce kendi zaman olaylarını işler, sonra gözlemi alır (kural 20). Sonraki adımlarda öteki bileşenler B1'in çıktısını okur. B1 hiçbir bileşenin durumunu okumaz (en alttadır).

## 10 · Kapalıyken davranış

B1'in bayrağı yoktur: çekirdektir; selam olmadan komşu ve bağ bilinemez. Ölçmek davranışı değiştirmez. Ölçülerin kullanımı ve bayrakları kullanan bileşendedir: verinin ölçüsünün kullanımı B3'te; hariç aralık yalnız B3'ün karıştırma eki açıkken verilir. Karıştırmaya karşı bütün mekanizmalar kapalıyken (mekanizma kapısının kolu, `18` §1.4 sözleşme 7) B1 aynı çalışır, hariç aralık listesi boştur.

**Mekanizma kapısı için not:** geri alma (kural 4) Babel'in genel kuralıdır. Kanal kilidindeki komşunun sessizliğini, selamı dönünce karıştırma katmanı kapalıyken de siler. Bu etki çekirdektedir ve kapıya girmez (K-247). Kapı açısından tutucu yöndedir: katman kapatılınca ölçülen düşüş çekirdeğin bu kazancını içermez, yani karıştırmaya özgü kazanç olduğundan büyük görünmez.

## 11 · Etkileşimler

1. **Kanıtı silme:** B1 hiçbir gözlemi başka bir bileşenin kararı yüzünden atmaz ve dondurmaz. Kendisinin sildikleri:
   - geri almanın sildiği sıfırlar (kural 4; sıra ilerlemediyse kayıp yoktur);
   - saklama sınırlarının dışına düşenler (kural 6, 9);
   - yeniden başlamada örnekler (kural 4);
   - silmede kayıt (kural 3).

   Silinen komşunun kayıtlarını öteki bileşenler de budar ("silinen komşu" olayı); B3'ün o bağ için tuttuğu hariç aralıklar da gider.
2. **Kendi karıştırılmam sırasında silme durmaz** (önceki tasarımda dururdu, KK-01 kural 13). 30 s'den uzun sessizlikte komşular silinir ve yeniden öğrenilir; bunun için en az `ORNEK_EN_AZ` selam gerekir. Birincil (15 s açık) ve dayanıklılık (10 s) hücrelerinde gerçekleşmez; daha uzun açık dönemli sınıflarda tanıda sayılır. Önceki tasarımda da kalitenin hatırası en çok 30 s tutuluyordu (`T_HATIRA`, `KENDI_UST_SURE`); 30 s'den uzun sağırlıktan sonra iki tasarımda da bağlar yeniden ölçülür. Bu yüzden silmeyi durdurmak için B1'e yukarıdan bilgi verilmez (sözleşme 1).
3. **Komşulara bildirdiğim oran** (kural 17): kendi karıştırılmam sırasında `d_r`'lerim düşer. Selamda ham değer giderse komşular bana olan bağı kötü ölçer; önceki tasarımda dondurmanın sebebi buydu (KK-01 kural 13). Hangi değerin gideceği B3 ile B6 arasında yazılır.
4. **B2'nin sayımı:** B2'nin selam kaybı payı B1'in örneklerini okur. B1 donmadığı için önceki tasarımdaki ikinci sayım (gölge geçmiş, KK-03 kural 2, Y-10) gerekmez. Geri alma, kanal kilidindeki komşunun sıfırlarını selamı dönünce siler; B2 bu sıfırları karıştırma sürerken okumalıdır, sonradan görünmezler.
5. **Seçim yanlılığı:** verinin ölçüsü yalnız veri gönderilen (çoğunlukla ardıl) bağlarda oluşur; yedekler yalnız selamla bilinir. B5 bir bağa göndermeyi bırakınca o bağın verisi `VERI_PENCERE_S` sonra tanımsız olur. B3 "veri yok"u "kötü" saymamalıdır.
6. **Kalabalık:** selam sıfırlarının bir kısmı çarpışmadır (önceki KK-03 kural 12'nin riski). B1 bunu ayırmaz; B2'nin sorusudur.
7. **Komşunun aralığı** (`a`) B6'nın kuralından gelir. Zaman aşımı, `SELAM_SAKLA` ve `BOSLUK_EN_COK` buna bağlıdır (Ö-2, Ö-4).

## 12 · Örnek senaryo

Komşu i ve j; aralıklar örnek (B6'nın kuralına bağlı).

1. **Tanışma:**
   - **t = 10,0 s:** j'nin ilk selamı gelir (sıra 0, aralık 0,55 s). Kayıt açılır, örnekler [1]; `d_r` = 1,00 (`n_s` 1). `d_f` tanımsız, `E_selam` ∞. Olay: yeni komşu.
   - **10,5 · 11,5 · 13,5 s:** sıra 1, 2, 3 gelir (aralık 1,1 · 2,2 · 2,2 s). Örnekler [1 1 1 1], `n_s` = 4; i artık j'yi listesinde bildirir. j de i'nin dört selamını almıştır: 13,5'teki selam i'yi 230/255 = 0,90 ile listeler. `d_f` = 0,90; `E_selam` = 1 / (0,90 · 1,00) = 1,11.
2. **Bir kayıp:** sıra 4, 15,5 s'de gönderilir ama kaybolur. `asim_t` = 13,5 + 1,5 × 2,2 = 16,8 s'de (16,8; 0) eklenir, `beklenen` 5 olur. 17,5 s'de sıra 5 gelir (fark 0). Örnekler [1 1 1 1 0 1]; `d_r` = 5/6 = 0,83; `E_selam` = 1 / (0,90 · 0,83) = 1,33.
3. **Veri:** i'nin ardılı j (B4'ün kararı). Son 16 veri kaydının 12'si ilk denemede, 2'si ikincide, 1'i üçüncüde onay aldı; 1'inden vazgeçildi.
   - `D` = 12 + 4 + 3 + 7 = 26, `G` = 15.
   - `E_veri` = 26 / 15 = 1,73; vazgeçme payı 1/16 = 0,06.

   B1 iki sayıyı da verir (1,33 ve 1,73); hangisinin nasıl kullanılacağı B3'ün kararıdır.
4. **Komşu kanal kilidinde:** j 40,0–55,0 s arasında karıştırıcıya çok yakın kalır, selam gönderemez ve sırası ilerlemez (Ö-5). Son selamı 39,5 s'de (sıra s, aralık 2,2 s).
   - i'de zaman aşımı 42,8 · 45,0 · 47,2 · 49,4 · 51,6 · 53,8 s'de altı sıfır ekler.
   - 55,3 s'de j'nin selamı sıra s + 1 ile gelir. i'de `beklenen` s + 7 olduğu için fark −6: altı sıfır silinir, (55,3; 1) eklenir.
   - `d_r` karıştırmadan önceki değerine döner; hariç aralığa gerek kalmaz.
5. **Kendim girişimde:** 70,0–85,0 s arasında i, j'nin selamlarını çözemez; j göndermeyi sürdürür. Zaman aşımlarının sıfırları gerçek kayıptır ve anları bu aralıktadır.
   - B3'ün karıştırma eki açıksa aralığı verir (ör. 70,0–88,0 s; bitişi B2'nin "bitti"sine bağlı). `d_r` bu aralık dışındaki en yeni 16 örnekten, yani karıştırmadan önceki ve sonra gelen örneklerden hesaplanır.
   - Kapalıysa ham `d_r` kullanılır: son 16 örnekte 7 sıfır varsa 9/16 = 0,56 ve `E_selam` = 1 / (0,90 · 0,56) ≈ 1,98. Yeni selamlarla birkaç aralıkta toparlanır.
6. **Komşu ölür:** j 100,0 s'de düşer. Her `a`'da bir sıfır eklenir; 130,0 s'de (`son_duyulma_t` + `T_SILME`) kayıt silinir ve "silinen komşu" olayı oluşur.

## 13 · Sınanması

**Birim testleri** (Aşama 4):

1. Kayıt yalnız selamla açılır; veri ve kontrol çerçevesi kayıt açmaz, var olan kaydı tazeler; kendi çerçeveme gelen onay tazeler, başkasına giden onay tazelemez.
2. Sıra:
   - fark 0;
   - ileri sarma (k sıfır, anları aradaki eşit noktalarda);
   - geri alma (son kayıtlar, en yeniden);
   - |fark| > `BOSLUK_EN_COK` iken yeniden başlama;
   - 65535 → 0 taşması.
3. Zaman aşımı: ilk sıfır 1,5 · `a`'da, sonra her `a`'da; aralık uzarken sahte kayıp yok; `ARALIK_EN_AZ`.
4. Saklama: `SELAM_SAKLA`'da en eskisi atılır; `d_r` yalnız son `N_SELAM` örneğe bakar.
5. Hariç aralık:
   - içindeki örnek ve kayıt sayılmaz;
   - bitişi açık aralık;
   - aralıktan sonra öncesinin kalitesi geri gelir;
   - liste boşken ham ölçü.
6. `d_f`: beni listelemeyen selam önceki değeri bozmaz; `DF_UNUT_S`'den sonra tanımsız; hariç aralıktaki bildirim sayılmaz.
7. `E_selam`: `d_f` ya da `d_r` tanımsız ya da 0 iken ∞.
8. Veri:
   - deneme = `tekrar` + 1, vazgeçmede 7;
   - `E_veri` = `D` / `G`; `G` = 0 iken ∞; kayıt yokken tanımsız;
   - `VERI_PENCERE` ve `VERI_PENCERE_S` sınırları;
   - kontrol sonucu ve kayıtsız komşunun sonucu yazılmaz.
9. *Kaldırıldı (kural 16 ile birlikte, 28 Kasım).*
10. Oran listesi: `ORNEK_EN_AZ`'ın altındaki komşu listelenmez; adrese göre sıralı.
11. Olaylar: yeni ve silinen komşu yalnız o kancada görünür.
12. Silme: `T_SILME`'de; silinen kaydın örnekleri ve veri kayıtları gider; aynı komşu yeni selamla yeniden açılır.
13. Kural 20: zaman olayları gözlemden önce işlenir; selam ile zaman aşımı aynı anda geldiğinde net etki yok.
14. Bellek sınırları aşılmaz.
15. Örnek senaryonun (§12) sayıları uçtan uca.

**Ölçümde sayılacak tanı:**
- bağ başına `E_selam`, `E_veri` ve kâhinin tek deneme başarısı yan yana (B3'ün teşhisi);
- kayda giriş ve silme sayısı; yeniden başlama sayısı (simülatörde 0 beklenir);
- geri almanın sildiği sıfırlar ve ileri sarmanın eklediği sıfırlar;
- `d_f`'nin tanımsız kaldığı süre; veri kaydı olan bağların sayısı ve `n_v`'nin dağılımı;
- kendi karıştırılmam sırasında silinen komşular (§11 madde 2).

## 14 · Kaynak

- **İki yönlü teslim oranı ve `E_selam` = 1 / (`d_f` · `d_r`):** ETX, De Couto vd. 2003 [36].
- **Selam sayımı:** son 16 selamın geçmişi, ileri sarma, geri alma, yeniden başlama ve 1,5 katlık zaman aşımı Babel'den, RFC 8966 Ek A.1 [4] (`protokoller/babel_bicim.py`).
- **Veri onayının bağ ölçüsüne girmesi:** 4B, Fonseca vd. 2007 [69]. Orada onay biti bağ tahminine girer; burada her veri çerçevesinin deneme sayısından beklenen deneme sayısı hesaplanır, selamla birleştirilmesi B3'tedir.
- **Bu tasarımın:**
  - zamanlı örnek ve hariç aralık;
  - ileri sarmanın sıfırlarının araya dağıtılması;
  - geri almanın ve yeniden başlamanın 64'lük sınırı (Babel'de 16, geçmişinin boyu);
  - onay çerçevesinin yalnız kendi çerçeveme yanıtsa varlık kanıtı sayılması;
  - iki ölçünün ham ve aynı birimde ayrı tutulması.
