# B3 · Bağın durumu

> Yeni tasarımın (`../18-YENI-TASARIM.md`) üçüncü bileşeni. İskelet `18` §1.4; sorun, kanıt, seçenekler ve kararım `18` §2.3 (25 Kasım; çekirdekte yeniden kararım 26 Kasım). Teşhis ölçümü `arsiv/teshis/faz5_3_b3_bag_olculeri_2026-11-25/` (bundan sonra "B3 teşhisi"). Değerler, bayraklar ve gözlemin kullanımı yalnız `00-DIZIN.md`de; burada adlarıyla anılır. Durum: onaylandı (26 Kasım). Önceki tasarımda karşılığı `../kural/KK-01` (orada ölçü, eşikli durumlar ve dondurma tek kâğıttaydı).
>
> Eksiksizlik listesinin maddeleri (`18`): 1 §1 · 2–4 `18` §2.3 · 5 §2 · 6 §3 · 7 §4 · 8 §5 · 9 §6 · 10 §7 · 11 §8 · 12 §9 · 13 §10 · 14 §11 · 15 §12 · 16 §13 · 17 §14. Ölçülen ve ölçülmeyen §15.

## 1 · Amaç ve sınıf

B3 her komşu bağı (i → j) için iki şey verir:
- **durum:** OLAĞAN (kullanılır) · SON ÇARE (yalnız olağan aday yoksa kullanılır) · KULLANILMAZ;
- **maliyet:** bağın beklenen deneme sayısı; yol seçimi (B4) bunu toplar. Maliyet yalnız burada hesaplanır (`18` §1.4 sözleşme 3).

Yolu seçmez ve paketi yönlendirmez; o iş B4'ün ve B5'in.

**Sınıf:**
- **Çekirdek (genel, K-247):** maliyet selamdan, eşikle düşürme yok (kural 1–3); "veri yok" güvenlik ağı (kural 7, `veri_yok`).
- **Karıştırma eki (karıştırmaya karşı):** B2'nin kanıtıyla SON ÇARE (kural 5–6) ve hariç aralık (kural 9–10). Karıştırma katmanının bayrak grubuyla kapanır (§10).

**Hizmet ettiği hedef** (`18` §1.1):
- Çekirdek, iyi bağın gereksiz düşmesini önler. Önceki tasarımın eşiğini aşan bağların kullanılmayanlarda %45'i, kullanılanlarda %99'u kâhine göre iyiydi (B3 teşhisi §10.2).
- Eşikle düşme açlığın köküydü (açlık teşhisi). Bu, en kötü tohum koruma ölçütünü doğrudan ilgilendirir.
- Karıştırma eki, kaybın büyüğünün olduğu karıştırılan bağdan dolaşmayı sağlar; kâhin bu dolaşmayla 0,779'a çıkıyor (`18` §2.2). Ayrıca karıştırma bitince bağı eski maliyetiyle hemen geri getirir (sessiz dönem koruma ölçütü).

## 2 · Gördüğü (`05`; yasak alanlar okunmaz)

B3 gözlem sözleşmesinden doğrudan bir şey okumaz; yalnız aşağıdaki bileşenleri okur (sözleşme 1).

| kaynak | B3'ün kullandığı | kullanmadığı |
|---|---|---|
| B1 | `E_selam`, `n_s`, `d_f`, `d_r` (hariç aralık listesiyle, kural 9); veri kayıtları (an, deneme, onay; kural 6–7 için); komşu kümesi, yeni ve silinen komşu olayları; bildirilecek oran listesi (kural 10) | `E_veri` ve vazgeçme payı (çekirdekte maliyete girmez, B3 teşhisi K2; tanıda raporlanır) · sondaki sessizlik (B1 kural 16; Aşama 3'te kaldırıldı) |
| B2 | kendi aralıklarım; bağ başına bildirim (`kb`, `kb_t`) ve bildirim aralıkları; bağ başına geçerli gönderici olayı | kendi durumumun değeri (yalnız aralıklar) · son işaretler (tanı) |
| yapılandırma | geçidin kimliği (kural 8) | — |

**Okumadıkları:** gözlem sözleşmesinin hiçbir alanı (hepsi B1 ve B2 üzerinden gelir) · `olculen_gurultu_w` (yasak, K-227) · RSSI · konum.

## 3 · Tuttuğu

Komşu j başına (B1'de kayıtlıyken):

| alan | başlangıç | güncellenir | silinir | üst sınır |
|---|---|---|---|---|
| `durum` (OLAĞAN · SON ÇARE · KULLANILMAZ) | KULLANILMAZ | her niyetli kancada (kural 4) | j silinince | — |
| `sebepler` (bildirim · gönderici · veri yok) | boş | kural 4–7 | j silinince | 3 |
| `durum_t` (son değişim anı) | kayda giriş | durum değişince | j silinince | — |
| `maliyet`: gerçek E ve tamsayı M | ∞ · 0xFFFF | her niyetli kancada (kural 1–2) | j silinince | — |

Kanca başına: "durum değişti" olayları (kural 4); bir sonraki kancanın başında boşalır.

Hariç aralık listesi ve bildirilecek oran listesi tutulmaz: her okumada B2'nin aralıklarından kurulur (kural 9–10). Gönderici ve veri yok sebepleri de B1'in kayıtlarından ve B2'nin olayından her kancada yeniden hesaplanır; ayrı bir sayaçları yoktur.

**Bellek:** düğüm başına en çok 255 kayıt (B1'in komşu tablosu).

## 4 · Durumlar ve geçişler

Durum her niyetli kancada kanıttan yeniden hesaplanır; geçmişe bağlı bir histerezisi yoktur (kural 4).

| durum | koşul | kullanılır mı | çıkış |
|---|---|---|---|
| KULLANILMAZ | maliyet ∞ (tek yönlü, ölçülemiyor ya da `n_s` < `ORNEK_EN_AZ`) | hayır | ölçü sonlu olunca: komşunun selamları ve bildirimi gelince (B1) |
| SON ÇARE | maliyet sonlu ve en az bir sebep | yalnız olağan aday yoksa (B4) | her sebebin kendi çıkışı: bildirim → j'nin 0'lı selamı ya da j'nin silinmesi · gönderici ve veri yok → başarılı bir veri çerçevesi ya da son başarısızlıktan `KANIT_OMUR_S` sonra |
| OLAĞAN | öteki hâller | evet | sebep doğunca SON ÇARE, maliyet ∞ olunca KULLANILMAZ |

**Takılı kalma yok:** her sebebin bir çıkışı var. Bildirim, j'nin selamıyla ya da `T_SILME`'de silinmesiyle biter. Öteki iki sebep, son başarısızlıktan `KANIT_OMUR_S` sonra kendiliğinden kalkar (İlke 3). Kendi karıştırılmamın üst süresi yoktur (B2 §4); hariç aralığın üst süresi `HARIC_UST_S`'dir (kural 9).

Önceki tasarımın KÖTÜ durumu ve iki eşiği (4'te çık, 3'te dön; `17` T-3) yoktur. Yerlerinde maliyet sıralaması vardır: kötü bağ pahalıdır ve yedeği varken seçilmez (B3 teşhisi; `18` §2.3 yeniden karar).

## 5 · Kurallar

**A · Maliyet (çekirdek)**

1. **Maliyet:** bağın maliyeti `E_selam` = 1 / (`d_f` · `d_r`)'dir (B1 kural 13). B1'den hariç aralık listesiyle istenir (kural 9). `n_s` < `ORNEK_EN_AZ` ise maliyet ∞ olur. Sebep: tek örnekle `d_r` 1,0 çıkar ve bağ olduğundan iyi görünür; komşuya bildirilen oran da aynı sınırı kullanır (B1 kural 17).
2. **Tamsayı biçimi:** M = min(⌈`MALIYET_BIRIM` · E⌉, 0xFFFE); E = ∞ ise M = 0xFFFF. B4 ve B6 tamsayıyla çalışır. 1 ETX = 64 birim; 16 bitlik alan ~1 000 ETX'e kadar taşır.
3. **Eşik yok:** maliyet sonluysa bağ, ne kadar pahalı olursa olsun kullanılabilir. Kötü bağ pahalıdır; yedeği varken yol seçimi onu seçmez.
   - Sebep: önceki tasarımın eşiğini (`E_selam` > 4 → KÖTÜ) aşan bağların kullanılmayanlarda %45'i, kullanılanlarda %99'u kâhine göre iyiydi (B3 teşhisi §10.2). Eşikle düşme, açlığın köküydü (açlık teşhisi).
   - Veri maliyete girmez. Kullanılan bağın sonraki bedelini veri selamdan ancak 0,074 bit daha iyi kestiriyor; bu, önceden yazılı 0,10 bitlik sınırın altında (B3 teşhisi K2). Selam bütün bağları tek terazide ölçer.

**B · Durum**

4. **Durumun hesabı:** her niyetli kancada, B2'den sonra ve B4'ten önce (kural 11):
   - maliyet ∞ ise KULLANILMAZ;
   - maliyet sonlu ve kural 5–7'nin sebeplerinden en az biri varsa SON ÇARE;
   - değilse OLAĞAN.

   Sebepler kümesi ve `durum_t` tutulur. Durum değişince "durum değişti" olayı oluşur (B4 için).
5. **Sebep "bildirim"** (karıştırma eki): j'nin son selamının biti 1'dir (B2 kural 10–11). j'nin 0'lı selamıyla ya da j'nin silinmesiyle biter. Ömrü yoktur: j susarsa son bildirim geçerli kalır; kanal kilidindeki komşu gönderemez.
6. **Sebep "gönderici"** (karıştırma eki): B2'nin j için geçerli bir gönderici olayı vardır (anı e; B2 kural 12–13) ve iki koşul birlikte sağlanır:
   - e'den sonra j'ye giden bütün veri kayıtları tam denemelidir (deneme 7: vazgeçme ya da son denemede onay);
   - şimdi − max(e, bu kayıtların en yenisi) ≤ `KANIT_OMUR_S`.

   Kendi aralıklarıma düşen kayıtlar sayılmaz (B2 kural 13'ün ayıklaması). Başarılı bir çerçeve (7'den az denemeyle onay) sebebi hemen kaldırır.

   Gerekçe: B2'nin olayı sayım başına bir kez oluşur; ardından gelen başarısız çerçeveler yeni olay doğurmaz. Bu yüzden kanıt, başarısızlık sürdükçe kayıtlardan uzatılır. Bağ kullanılmazsa yeni kanıt gelmez; `KANIT_OMUR_S` sonra bağ yeniden denenir (İlke 3: kanıt kalkınca geri al). Karıştırma sürüyorsa tek bir başarısız çerçeve sebebi hemen geri getirir.
7. **Sebep "veri yok"** (çekirdek, `veri_yok`): j'ye son `VERI_YOK_N` veri kaydının (son `VERI_PENCERE_S` içinde, kendi aralıklarım dışında) hepsi vazgeçmedir ve şimdi − en yenisinin anı ≤ `KANIT_OMUR_S`.
   - Bir başarılı kayıt sebebi kaldırır.
   - Bağ kullanılmazsa `KANIT_OMUR_S` sonra yeniden denenir. Yeni bir vazgeçme sebebi hemen geri getirir, çünkü son `VERI_YOK_N` kayıt yine hepsi vazgeçme olur.
   - Selamı geçen ama veriyi taşımayan bağın güvenlik ağıdır.
   - Ölçülen sıklık (B3 teşhisi, kuraldan sonra, §15): temiz kanalda çok seyrek, karıştırılan alıcıda sık.
8. **Geçit istisnası:** j geçitse (yapılandırma) kural 5–6 sebep eklemez; tanıya yazılır. Geçit hedeftir; ondan kaçınmak paketi başka bir yoldan yine ona götürür. Girişimdeki alıcıya giden çerçevelerin önemli bir kısmı yine ulaşır (çerçeve başına 3,9 deneme; `18` §2.3). Kural 7 geçitte de geçerlidir: son 4 çerçevenin hepsi vazgeçmeyse başka bir bağ geçide daha iyi ulaşabilir.

**C · Hariç aralık (karıştırma eki)**

9. **j'nin ölçüsü için liste:**
   - kendi aralıklarım (B2 kural 8);
   - j'nin bildirim aralıkları (B2 kural 10), başlangıcı `BILDIRIM_PAYI_S` öne çekilerek.

   Her aralık en çok `HARIC_UST_S` uzunluğundadır: [b, s] yerine [b, min(s, b + `HARIC_UST_S`)].
   - **Sebep:** karıştırma sırasındaki selam sıfırları ve düşük oran bildirimleri bağın kalitesini olduğundan kötü gösterir. Bunlar sayılmayınca maliyet karıştırmadan önceki kalitede kalır ve kanıt kalkınca bağ o değerle hemen döner (önceki tasarımda `17` T-7'nin "hatırlanan kalite"si). B1 donmaz; formül B1'de kalır (B1 kural 10).
   - **Öne çekme:** komşu durumunu geç bulur (girişim kuralı 3 s içinde %34–35, ortanca gecikme 2–3 s; B2 §7) ve bit de geç ulaşır.
   - **Üst süre:** daha uzun karıştırmada bağın yeni hâli ölçüye girer (İlke 2). B1'in saklaması 30 s'lik hariç aralığa göre seçildi (`SELAM_SAKLA`).
   - Gönderici olayının çevresi listeye girmez. Kanal kilidindeki alıcının sıfırlarını B1'in geri alması zaten siler (B1 Ö-5); girişimdeki alıcının selamı bana ulaşır, `d_r` bozulmaz.
   - Grup ya da `haric_aralik` kapalıyken liste boştur.
10. **Bildirilecek oran listesi** (B6 için, B1 kural 17): yalnız kendi aralıklarımla, aynı üst süreyle istenir. Sebep: kendi karıştırılmamı komşulara bit bildirir. Ham oran bildirilseydi komşular bana olan bağı karıştırma bitince düşük oranla ölçer ve geç toparlanırdı (B1 §11 madde 3). Karıştırma eki kapalıyken ham oran bildirilir.

**D · Sıra**

11. Her niyetli kancada sıra B1 → B2 → B3 → B4'tür (`18` §1.4 olay sırası 1–3). B3'ün kendi sırası: önce maliyet (kural 1–2), sonra sebepler (kural 5–8), sonra durum (kural 4). Niyet döndüremeyen kancalarda B3 çalışmaz.

**E · Çıktılar**

12. **Bağ başına:** durum, sebepler, `durum_t`, maliyet (E ve M); kancanın "durum değişti" olayları; bildirilecek oran listesi (kural 10).

## 6 · İletiler

B3 ileti göndermez. Maliyeti ilanlarda B4 ve B6, oran listesini selamda B6 taşır. Beklentilerim:
- **B4:** SON ÇARE bağı, olağan aday yoksa kullanılır; KULLANILMAZ hiç kullanılmaz; aynı durumdakiler maliyetle sıralanır.
- **B6:** bildirilecek oran listesi kural 10'dan gelir.

## 7 · Değerler

`MALIYET_BIRIM` · `KANIT_OMUR_S` · `VERI_YOK_N` · `BILDIRIM_PAYI_S` · `HARIC_UST_S`. B1'den kullanılanlar: `ORNEK_EN_AZ` · `VERI_PENCERE_S`. Değeri, birimi, kaynağı, küçük ve büyük olursa ne olacağı ve taranıp taranmayacağı `00-DIZIN.md`'nin değer tablosunda.

## 8 · Kenar durumlar

- **Soğuk açılış:** j'nin ilk selamıyla kayıt açılır. `n_s` ≥ `ORNEK_EN_AZ` ve `d_f` tanımlı olana kadar maliyet ∞, durum KULLANILMAZ'dır; en kısa aralıkta ~2 s sürer (B1 §8).
- **Geçit:** B3 geçitte de çalışır; geçidin bağları komutun yolunda kullanılır. Geçide giden bağa istisna kural 8'dedir.
- **Hiç komşu yok:** çıktı boş. **Tek komşu:** olağan aday yoksa SON ÇARE bağı kullanılır (E1); KULLANILMAZ ise yol yoktur (B4, B7).
- **Düğüm kendisi karıştırılırken:**
  - kendi aralıklarım bütün bağların ölçüsünden çıkar (kural 9); maliyetler karıştırmadan önceki kalitede kalır;
  - gönderici ve veri yok sebepleri kendi aralığımdaki kayıtları saymaz;
  - komşulara karıştırmadan önceki oranlar bildirilir (kural 10).
- **Komşu karıştırılırken:**
  - girişimdeki komşu bitini gönderir, bildirim sebebi doğar;
  - kanal kilidindeki komşu gönderemez; onu gönderici ve veri yok sebepleri gösterir (B2 §8).
- **Uzun karıştırma** (`HARIC_UST_S`'den uzun): hariç aralık kesilir, ölçü yeni hâli görür. Bildirim sürdüğü sürece bağ SON ÇARE kalır.
- **Zaman aşımı:** kural 6–7'nin `KANIT_OMUR_S`'si; kayıt B1'in silmesiyle gider.
- **Aynı anda olaylar:** kural 11.
- **Sayaç taşması:** B3'ün sayacı yok. Tamsayı maliyet 0xFFFE'de doyar.
- **Tamponun dolması:** B3'ün tamponu yok.

## 9 · Arayüz

**Kancalar:** her niyetli kancada kural 1–12, B2'den sonra ve B4'ten önce. Yeni ve silinen komşu olayıyla (B1) kayıt açılır ve silinir.

**Okuduğu:** B1 ve B2 (§2); B3 yalnız kendinden aşağıdakileri okur (sözleşme 1).

**Çıktılar ve okuyanlar:**

| çıktı | kural | okuyan |
|---|---|---|
| bağ başına durum, sebepler, `durum_t` | 4–8 | B4, B7 (komutun kararı, B7 kural 8) |
| bağ başına maliyet (E, M) | 1–2 | B4 (yol maliyeti), B6 (ilan B4 üzerinden) |
| "durum değişti" olayları | 4 | B4, B6 |
| hariç aralık listesi | 9 | B1'e yapılan okuma isteği (B3'ün kendisi) |
| bildirilecek oran listesi | 10 | B6 |

## 10 · Kapalıyken davranış

- **`karistirma_katmani` kapalı:** bildirim ve gönderici sebepleri yok; hariç aralık listesi boş, B1 ham ölçer; oran ham bildirilir. Kalan çekirdek: maliyet selamdan, KULLANILMAZ ∞ için, veri yok sebebi (`veri_yok` açıksa). Mekanizma kapısının kolu budur (`06` §0.4.5).
- **`haric_aralik` kapalı** (grup açık): liste boş, oran ham. SON ÇARE sebepleri sürer. Karıştırma bitince bağ ham ölçüyle, selamlar dolana kadar pahalı döner. Hatırlanan kalitenin katkısı bu bayrakla ölçülür.
- **`veri_yok` kapalı:** kural 7 çalışmaz.
- B2'nin alt bayrakları (`alici_bildirimi`, `gonderici_kaniti`) kapalıyken ilgili sebep oluşmaz; B3'te ayrı işlem gerekmez.

## 11 · Etkileşimler

1. **B1 ile:**
   - B3 ölçüyü hariç aralıkla ister; B1'in örneklerini silmez, dondurmaz.
   - B1'in sondaki sessizliğini (kural 16) ne B2 ne B3 kullanıyordu; Aşama 3'te kaldırıldı (`01-BUTUNLUK.md` §11).
   - `E_veri` maliyete girmez; tanıda raporlanır.
2. **B2 ile:**
   - B2 kanıt verir, B3 karar verir. Gönderici olayının ömrü ve uzatılması kural 6'dadır.
   - B2'nin kendi aralıklarım çıktısı hem hariç aralığa (kural 9) hem kural 6–7'nin ayıklamasına girer.
3. **B4'e kalanlar:**
   - olağan adayları SON ÇARE'den önce sıralamak (E1);
   - yol değişiminin histerezisi (maliyetin kendisinde histerezis yok; B3 teşhisi K4: veri bile yükle oynamıyor, selam daha durgun);
   - "son çare" adı B4'ün aday türlerinde başka anlamda kullanılmamalı (Aşama 3'ün ortak sözlüğü).
   - Selam ölçeği sıkıştırır: iyi bağ ~%20 ucuz, kenar bağ ~%15–28 pahalı görünür (B3 teşhisi §10.1). Yol maliyeti bu yüzden az sayıda uzun bağ yerine iyi bağlardan geçen yolları biraz kayırır; bu İlke 1'le aynı yöndedir.
4. **B5 ve B7:** telemetri SON ÇARE bağına ancak B4 olağan aday vermezse gider (B5 kural 1). Komut izin gösterdiği komşuya, o S'de olsa da gider (B7 kural 8): komutun bilinen tek yolu odur.
5. **B6:** oran listesi (kural 10); "durum değişti" ve maliyet değişimi B4 üzerinden ara ilanı tetikleyebilir.
6. **B7:** hiç aday kalmayınca (açlık) bekletme kararı B7'nindir. Ardıl S'deyken paket ona gider, bekletilmez (B5 kural 1).
7. **Kanıtı silmeme** (sözleşme 4):
   - SON ÇARE'deki bağa veri gönderilmez, yeni kayıt ve yeni olay oluşmaz. Bu yüzden kanıt süreyle kalkar (kural 6–7) ve bağ yeniden denenir; böylece kanıtın kesilmesi bağı süresiz dışarıda bırakmaz.
   - Hariç aralık B1'in örneklerini silmez, yalnız saymaz.
8. **Mekanizma kapısı:** çekirdek (selamdan maliyet, eşiksiz, veri yok) karıştırmaya tepki vermez (B3 teşhisi K6: selam karıştırmada iki katına neredeyse hiç çıkmıyor). Karıştırmaya özgü kazanç B2 ile B3'ün karıştırma ekinden ölçülür.

## 12 · Örnek senaryo

i'nin komşuları j (maliyet 1,6) ve k (2,1); B4'e göre ardıl j. Sayılar örnektir.

1. **Olağan:** iki bağ OLAĞAN. M(j) = ⌈64 × 1,6⌉ = 103, M(k) = ⌈64 × 2,1⌉ = 135.
2. **j girişimde, bit geliyor:** j 152,1 s'den beri karıştırılıyor. 153,4'te durumunu bulur, bit 1'li selamı i'ye 155,1'de ulaşır.
   - i'nin bu kancasında j SON ÇARE olur (sebep bildirim); B4 olağan aday k'ye geçer.
   - j'nin ölçüsü için hariç aralık [152,1, ∞): 155,1 − 3 s. Maliyet 1,6'da kalır.
3. **j'ye giden çerçeveler:** 152,1–155,0 arasında i'nin j'ye üç çerçevesi tam denemeyle biter. B2 155,0'da gönderici olayı verir; 155,1'de bildirim de gelir. Sebepler {bildirim, gönderici}.
4. **Karıştırma biter:** 165,0'da j'nin girişimi biter, 165,9'da bit 0'lı selamı gelir.
   - Bildirim sebebi kalkar. Gönderici sebebi 155,0 + 5 = 160,0'da zaten süresiyle kalkmıştı; o sırada j'ye çerçeve gitmedi.
   - j OLAĞAN'a döner, maliyet 1,6: aralık [152,1, 165,9]. B4 j'ye döner.
5. **Kanal kilidi:** j 180,0–190,0 arasında karıştırıcıya çok yakın, selam gönderemez.
   - i'nin çerçeveleri vazgeçmeyle biter; 181,8'de gönderici olayı oluşur, j SON ÇARE olur.
   - 186,8'de (181,8 + 5) kanıt kalkar; B4 j'yi yeniden dener. 187,0'daki çerçeve de vazgeçmeyle biter, sebep hemen geri gelir: e'den sonraki bütün kayıtlar tam denemeli ve en yenisi 187,0. Son 4 kaydın hepsi vazgeçme olduğu için veri yok sebebi de doğar.
   - 192,0'da süre yine dolar. 192,2'deki deneme bu kez 2. denemede onay alır; iki sebep de kalkar, j OLAĞAN.
   - Bu sırada j'nin sıfırları B1'in geri almasıyla siliniyor (Ö-5); maliyet 1,6'ya döner.
6. **Veri yok** (karıştırma eki kapalı; açıkken üçüncü vazgeçmede gönderici sebebi de doğar): l, selamı iyi geçen bir komşu (maliyet 1,4). 220,0–223,0 arasında l'ye son 4 çerçevenin hepsi vazgeçmeyle biter.
   - l SON ÇARE olur (sebep veri yok); B4 başka adaya geçer.
   - 228,0'da kanıt kalkar, l yeniden denenir. Çerçeve onay alırsa l olağandır.
7. **Kendim karıştırılırken:** i 240,0–250,0 arasında girişimde; aralığı [238,0, 249,0] (B2 kural 8).
   - Bu aralıktaki selam sıfırları ve vazgeçmeler hiçbir bağın ölçüsüne ve kural 7'ye girmez.
   - Maliyetler 1,6 · 2,1'de kalır. i'nin komşulara bildirdiği oranlar karıştırmadan öncekilerdir.

## 13 · Sınanması

**Birim testleri** (Aşama 4):

1. Maliyet:
   - `E_selam` hariç aralık listesiyle istenir;
   - `n_s` < 4 iken ∞;
   - tamsayı biçimi (yukarı yuvarlama, 0xFFFE'de doyma, ∞ = 0xFFFF).
2. Eşik yok: sonlu ve çok büyük maliyetli bağ OLAĞAN kalır.
3. Durum: KULLANILMAZ ↔ OLAĞAN ↔ SON ÇARE geçişleri; birden çok sebep; sebepler kalkınca dönüş; "durum değişti" olayı yalnız değişimde.
4. Bildirim: bit 1'de girer, 0'da çıkar; susmakla değişmez; silinmeyle gider; `alici_bildirimi` kapalıyken oluşmaz.
5. Gönderici:
   - olayla girer;
   - başarısız kayıtlarla uzar;
   - başarılı bir kayıtta kalkar;
   - son başarısızlıktan `KANIT_OMUR_S` sonra kalkar;
   - kendi aralığımdaki kayıtlar sayılmaz.
6. Veri yok:
   - son 4 kaydın hepsi vazgeçmeyse girer;
   - başarılı bir kayıtta ve `KANIT_OMUR_S` sonra kalkar;
   - yeni vazgeçme sebebi hemen geri getirir;
   - kendi aralığımdaki kayıtlar sayılmaz;
   - bayrak kapalıyken oluşmaz.
7. Geçit: bildirim ve gönderici sebebi eklenmez, veri yok eklenir.
8. Hariç aralık:
   - kendi aralıklarım ve bildirim aralıkları;
   - `BILDIRIM_PAYI_S` öne çekme;
   - `HARIC_UST_S` kesmesi;
   - grup ya da `haric_aralik` kapalıyken boş.
9. Oran listesi: yalnız kendi aralıklarımla; karıştırma eki kapalıyken ham.
10. Sıra (kural 11): aynı kancada B2'nin yeni olayı B3'te görülür.
11. Örnek senaryonun (§12) sayıları uçtan uca.

**Ölçümde sayılacak tanı:**
- durum geçişleri ve sebebe göre SON ÇARE'de geçen süre;
- SON ÇARE bağına giden paket sayısı (olağan aday yokken);
- veri yok sebebinin sıklığı ve doğruluğu (kâhine göre);
- gönderici sebebinin uzatılması ve yeniden deneme sayısı;
- hariç aralıkların uzunluğu ve kesilen aralıklar;
- `E_veri` ile `E_selam` yan yana (tanı; maliyete girmez);
- geçit istisnasının kullanımı.

## 14 · Kaynak

- **Bağın maliyeti olarak beklenen deneme sayısı:** ETX, De Couto vd. 2003 [36]. Selam geçmişinden ölçme: Babel [4].
- **Eşiksiz kullanım:** maliyet sıralaması kötü bağı kendiliğinden geride bırakır. Eşiğin kaldırılması B3 teşhisinin sonucudur (§10.2); MRHOF'un üst sınırı [64] kullanılmaz.
- **Veriyi bağ tahminine katmak:** 4B, Fonseca vd. 2007 [69]. Bizde ölçüldü (B3 teşhisi K2) ve maliyete alınmadı; veri yalnız güvenlik ağında kullanılır.
- **Karıştırılan bağı kullanmamak, kanıt kalkınca hatırlanan kaliteyle geri almak:** önceki tasarım (`17` T-7). Burada dondurma yerine hariç aralıkla (B1 kural 10).
- **Karıştırılan bölgenin etrafından dolaşmak:** ağ katmanının bilinen stratejisi [59]; komşunun bildirdiği karıştırma JAM'den ↪ (B2 §14).
- **Bu tasarımın:**
  - eşiksiz maliyet ve üç durum;
  - karıştırılan bağın son çare olması (E1);
  - gönderici kanıtının başarısızlık sürdükçe uzatılması ve süreyle kalkıp yeniden denenmesi;
  - "veri yok" güvenlik ağı;
  - geçit istisnası;
  - hariç aralığın öne çekilmesi ve üst süresi.

## 15 · Ölçülen ve ölçülmeyen

**Ölçülen:**
- **Selam ile verinin doğruluğu** (B3 teşhisi K2, K3): kullanılan bağın sonraki bedelini selam ortanca %24, veri %17 hatayla kestiriyor; veri selamı ancak 12 kayıtla 0,05 bit geçiyor.
- **Önceki eşiğin zararı** (B3 teşhisi §10.2, kuraldan sonra).
- **Veri yok sebebinin sıklığı** (B3 teşhisi `ek_hesap.txt` E4; kuraldan sonra, 26 Kasım, bu kâğıt için eklendi): veri örneklerinde son 4 kaydın hepsinin vazgeçme olma payı:
  - ikizde %0,01 (9/82 424), birincilin önce ve sessiz evresinde %0,15 (81/53 530);
  - açık dönemde alıcı girişimdeyse %7,0, kanal kilidindeyse %25,9, uzaksa %0,56;
  - temiz sınıfta bu örneklerin sonraki bedeli sonlu (ikizde ortanca 7,8, birincilde 2,8): bağ toparlanıyor; karıştırılan alıcıda yarısı ∞;
  - 3 kayıtla temizde %0,05–0,32, 6 kayıtla %0,00–0,09.

**Ölçülmeyen** (Aşama 4'te sayılır ya da ablasyonla ölçülür):
- SON ÇARE'nin (E1) etkisi;
- `KANIT_OMUR_S`, `BILDIRIM_PAYI_S`, `HARIC_UST_S`;
- hariç aralığın katkısı (`haric_aralik`);
- veri yok sebebinin kayba etkisi (`veri_yok`);
- geçit istisnası.

Karıştırma katmanı bütünüyle hiç ölçülmedi.
