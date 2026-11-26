# B4 · Yol

> Yeni tasarımın (`../18-YENI-TASARIM.md`) dördüncü bileşeni. İskelet `18` §1.4; sorun, kanıt, seçenekler ve kararım `18` §2.4 (26 Kasım: uygulanabilirlik koşulu, Babel ailesi). Kurallar Babel'in belirtiminden uyarlandı (RFC 8966 [4], `protokol_kaynaklari/rfc8966_babel.txt`; bölüm numaraları kurallarda). Değerler, bayraklar ve gözlemin kullanımı yalnız `00-DIZIN.md`de; burada adlarıyla anılır. Durum: onaylandı (26 Kasım). Önceki tasarımda karşılıkları `../kural/KK-04` (eğim) ve arşivdeki `../arsiv/kural/KK-04-ROTA-2026-11-18.md` (uygulanabilirlik koşulu).
>
> Eksiksizlik listesinin maddeleri (`18`): 1 §1 · 2–4 `18` §2.4 · 5 §2 · 6 §3 · 7 §4 · 8 §5 · 9 §6 · 10 §7 · 11 §8 · 12 §9 · 13 §10 · 14 §11 · 15 §12 · 16 §13 · 17 §14. Döngüsüzlüğün gerekçesi ve ölçülmeyen §15.

## 1 · Amaç ve sınıf

B4 tek bir hedefe, geçide giden yolu tutar:
- **ardıl** ve **aday listesi:** paketin gidebileceği komşular, sıralı;
- **kendi maliyetim** ve **turum:** komşulara ilan ettiğim yol;
- **döngüsüzlük:** uygulanabilirlik koşuluyla, baştan.

Paketin yönünü seçmez: aday listesinden paketi hangi komşuya göndereceğine B5 karar verir (`18` §1.4 sözleşme 5). Komutun yolu (geçitten aşağı) B7'nin geri izidir.

**Sınıf:** genel (K-247), çekirdek. B3'ün son çare durumunu sıralamada kullanır (kural 5); bu durumun karıştırma sebepleri B3'ün karıştırma ekinden gelir, B4'ün ayrı bir karıştırma eki yoktur.

**Hizmet ettiği hedef** (`18` §1.1): koruma ölçütleri. Ölçülen yollar içinde en kötü tohum, sessiz dönem ve gecikmenin p99'u ölçütlerinin hepsini geçen tek yol bu koşul (`18` §2.4). Birincilde ortalamayı yol seçimi belirlemiyor; asıl kazanç B2, B3 ve B5'ten beklenir.

## 2 · Gördüğü (`05`; yasak alanlar okunmaz)

| kaynak | B4'ün kullandığı | kullanmadığı |
|---|---|---|
| komşunun ilanı (selamda; iletiyi B6 çözer) | tur ve maliyet (kural 1–4) | öteki alanlar (B1'in, B2'nin) |
| tur isteği (`kontrol_alindi`; B6 çözer) | gönderen, istenen tur, kalan atlama (kural 12) | — |
| B1 | komşu kümesi, yeni ve silinen komşu olayları; komşunun ilan ettiği selam aralığı `a` (kural 4) | ölçüler (B3 üzerinden) |
| B2 | kendi durumum "yok" mu (kural 14) | öteki çıktılar (B3 üzerinden) |
| B3 | bağ başına durum ve maliyet (M) | sebepler (yalnız tanı) |
| `saat_s` | yalnız süreler | — |
| yapılandırma | geçidin kimliği; ben geçit miyim | — |

**Okumadıkları:** gözlem sözleşmesinin öteki alanları · `olculen_gurultu_w` (yasak, K-227) · konum · paket başlığı (B5'in, B7'nin).

## 3 · Tuttuğu

Komşu j başına (B1'de kayıtlıyken):

| alan | başlangıç | güncellenir | silinir | üst sınır |
|---|---|---|---|---|
| son ilan: (`tur_j`, `C_j`) ve anı | ilk ilanı | her ilanında | j silinince | — |
| kabul edilen ilan (yalnız ardıl için; kural 10) | seçimde | kural 10 | ardıl değişince | — |
| düzgünleştirilmiş maliyet `ms_j` ve son güncelleme anı | aday olunca `m_j` | her seçimde (kural 6) | aday olmaktan çıkınca | — |

Düğüm başına:

| alan | başlangıç | güncellenir | silinir |
|---|---|---|---|
| FD = (tur, maliyet) ve son güncellenme anı | yok | kural 9 | `FD_UNUT_S` boyunca güncellenmezse |
| `ardil`, kendi maliyetim C, ilan için verdiğim (tur, C) | yok · ∞ | her seçimde (kural 5–8) | — |
| yok sayma: başlangıç anı, istek gitti mi | yok | kural 10 | yok sayma bitince |
| açlık dizisi: sonraki istek anı, kalan yineleme | yok | kural 11 | açlık bitince |
| iletilen istekler: (istenen tur, isteyen, an) | boş | kural 12 | `ISTEK_ANIMSA_S`'den eski olunca |
| geçitte kendi turum | `TUR_BASLANGIC` | kural 13 | — |

Kanca başına olaylar: "hemen gönder" (B6 için), tur isteği iletileri (B6 gönderir), ardıl değişti (B5, B7 için). Bir sonraki kancanın başında boşalır.

**Bellek:** komşu başına sabit alanlar (en çok 255 komşu); iletilen istek kaydı `ISTEK_ANIMSA_S` içindekilerle sınırlı (aynı tur için bastırma, kural 12).

## 4 · Durumlar ve geçişler

| durum | koşul | çıkış |
|---|---|---|
| geçit | yapılandırma | — (maliyet 0, ardıl yok) |
| yolu var | ardıl var, C sonlu | ardıl aday olmaktan çıkar ve yerine aday yoksa: aç |
| yolu var, yok sayıyor | ardıldan uygulanamaz sonlu ilan geldi (kural 10) | uygulanabilir ilan gelir ya da `YOK_SAYMA_S` dolar |
| aç | aday yok, C = ∞ | bir aday doğar: komşunun uygulanabilir ilanı ya da yeni tur. Tur isteğiyle zorlanır (kural 11) |

Açlık dizisi kendi durumumda bekler (kural 14) ve açlık bitince durur. Yok saymanın üst süresi vardır. FD süreyle unutulur (kural 9). Takılı kalma yok.

## 5 · Kurallar

**A · Uygulanabilirlik ve maliyet**

1. **Uygulanabilirlik** (RFC 8966 §3.5.1): j'nin ilanı (t, c) uygulanabilirdir ⇔ aşağıdakilerden biri:
   - c = ∞ (geri çekme hiç döngü doğurmaz);
   - FD yok;
   - t, FD.tur'dan yeni;
   - t = FD.tur ve c < FD.maliyet.

   Turlar 16 bit, modüler karşılaştırılır (`00-DIZIN` ortak birimler). Uygulanabilirlik her seçimde güncel FD ile hesaplanır, saklanmaz.
2. **Yol maliyeti:** `m_j` = M_j + `C_j` (tamsayı birim, B3 kural 2; 0xFFFE'de doyar; biri ∞ ise ∞). M_j ≥ 64 olduğundan maliyet her atlamada kesin artar. RFC 8966 §3.5.2'nin döngüsüzlük için şart koştuğu kesin artan toplama budur.
3. **Aday kümesi:** j adaydır ⇔ B1'de kayıtlı, B3 durumu KULLANILMAZ değil, ilanı sonlu, taze (kural 4) ve uygulanabilir (kural 1). Adaylar iki sınıftadır:
   - **O:** B3 durumu OLAĞAN;
   - **S:** B3 durumu SON ÇARE.
4. **İlanın ömrü:** j'nin son ilanı `ILAN_OMUR_KAT` · a_j'den (B1'in tuttuğu, j'nin ilan ettiği selam aralığı) eskiyse ilan ∞ sayılır. Babel'de bu rotanın sona ermesidir (Ek B: ilan aralığının 3,5 katı); bizde ilan her selamdadır, aralık selamınkidir. Susan komşu (ölü, uzaklaşmış ya da kanal kilidinde) böylece birkaç selam aralığında aday olmaktan çıkar; bağ maliyetinin sonsuza gitmesini (B1'de 16 sıfır) beklemez.

**B · Seçim**

5. **Ardılın seçimi**, her niyetli kancada:
   - **Zorunlu geçiş:** ardıl yoksa, ardıl artık aday değilse ya da ardıl S'de ve O boş değilse, en iyi aday hemen seçilir. Önce O, O boşsa S; sınıf içinde en küçük `m_j`. Bu, E1'in kuralıdır (B3 §1). RFC 8966 Ek A.3'te de seçili rota yokken yalnız anlık maliyete bakılır.
   - **İsteğe bağlı geçiş:** ardıl adayken aynı ya da daha iyi sınıftaki bir j'ye geçilir ⇔ `m_j` < `m_ardil` **ve** `ms_j` < `ms_ardil` (Ek A.3). Birden çok aday geçerse en küçük `m_j`'li seçilir.
   - **Eşitlikte:** mevcut ardıl, sonra küçük M, sonra küçük adres.
   - Hiç aday yoksa açlıktır (kural 11).
6. **Düzgünleştirilmiş maliyet** (Ek A.3): her seçimde her aday için `ms_j` ← `ms_j` + (`m_j` − `ms_j`) · (1 − e^(−Δt / `DUZ_S`)); Δt, son güncellemeden beri geçen süredir.
   - Aday olan komşuda `ms_j` = `m_j` ile başlar; aday olmaktan çıkanın kaydı silinir.
   - S'deki adayların `ms`'i de güncellenir. Karıştırma bitince hariç aralıkla düşük kalan maliyeti (B3 kural 9) hem anlık hem düzgünleştirilmiş olarak iyi görünür; bağ hemen geri seçilir.
   - `duzgun_gecis` kapalıyken isteğe bağlı geçişte yalnız `m_j` < `m_ardil` aranır.
7. **Kendi maliyetim:** C = `m_ardil` (ardılın kabul edilen ilanıyla, kural 10). Geçitte C = 0. Ardıl yoksa C = ∞.

**C · İlan ve FD**

8. **İlan** (B6'ya): (tur, C).
   - Tur, ardılın kabul edilen ilanının turudur; geçitte kendi turum.
   - Ardıl yoksa C = ∞ ve tur FD'nin turudur (FD yoksa 0). Geri çekmenin turu uygulanabilirliği etkilemez (kural 1).
   - RFC 8966 §3.7: ilan edilen maliyet, paketin gittiği seçili rotanınkidir.
9. **FD'nin güncellenmesi** (RFC 8966 §3.7.3): ilan için sonlu bir (t, C) verildiğinde şunlardan ilki uygulanır:
   - FD yoksa ya da t, FD.tur'dan yeniyse: FD ← (t, C);
   - t = FD.tur ve C < FD.maliyet ise: FD.maliyet ← C.

   Geri çekme FD'yi değiştirmez. FD, verildiği anda güncellenir; B6'nın onu gerçekten gönderip göndermediğine bakılmaz. Bu tutucu yöndedir: FD gereğinden küçük olabilir ama hiç büyük olamaz, döngüsüzlük korunur. Sözleşme 1 de B4'ün B6'yı okumasına izin vermez. `FD_UNUT_S` boyunca sonlu ilan verilmezse FD unutulur (Babel'in kaynak tablosunun çöp toplaması).

**D · Uygulanamaz ilan ve açlık**

10. **Ardıldan gelen ilan** (RFC 8966 §3.5.3, §3.8.2.2):
    - **Uygulanabilir:** kabul edilir.
    - **∞ ilan** yok sayılmaz: ardıl aday olmaktan çıkar (kural 5).
    - **Sonlu ve uygulanamaz ilan** yok sayılır. Ardıl son kabul edilen ilanla kalır. İlk yok saymada ardıla tek alıcılı tur isteği gider (istenen FD.tur + 1); sonraki yok saymalar istek göndermez.
    - Yok sayma, ilk yok sayılan ilandan başlayarak en çok `YOK_SAYMA_S` sürer. Bu sürede uygulanabilir bir ilan gelirse biter. Süre dolunca ardılın son ilanı uygulanır; uygulanamıyorsa ardıl aday olmaktan çıkar.
    - Gerekçe: Babel, seçili rotasına uygulanamaz güncelleme gelince rotayı hemen bırakmıyor ve birincilde rota yokluğundan hiç kaybetmiyor (`18` §2.4).
11. **Açlık** (aday yok):
    - C = ∞ ilan edilir (kural 8) ve "hemen gönder" olayı oluşur. Paketlerin bekletilmesi B7'nindir.
    - **Tur isteği** (RFC 8966 §3.8.2.1), yalnız en az bir komşunun ilanı sonlu ama uygulanamazsa ve o bağ KULLANILMAZ değilse gider:
      - istenen tur FD.tur + 1, çoklu yayın;
      - hemen ve ardından `ISTEK_YINELEME` kez `ISTEK_ARALIK_S` arayla;
      - açlık sürerse dizi `ISTEK_ARA_S`'de bir yinelenir.
    - Açlık bitince ya da koşul kalkınca dizi durur. Öteki hâllerde istek gitmez; yeni tur hiçbir komşuyu aday yapmaz.
12. **Tur isteği gelince** (isteyen g, istenen t, kalan atlama h; RFC 8966 §3.8.1.2):
    - **Rotam sonlu ve turu ≥ t:** "hemen gönder" (selamla ilan).
    - **Geçitsem ve turum < t:** turum bir artar (bir istekle en çok bir) ve "hemen gönder".
    - **Öteki hâllerde h ≥ 2 ise** istek h − 1 ile tek alıcılı iletilir. Alıcı, g olmayan bir aday (önce ardıl, sonra aday sırası); yoksa ilanı sonlu ama uygulanamaz, g olmayan ve bağı KULLANILMAZ olmayan bir komşu.
      - Kayıt (t, g, an) `ISTEK_ANIMSA_S` tutulur.
      - Aynı ya da daha küçük bir t için `ISTEK_BASTIRMA_S` içinde ikinci istek iletilmez (RFC: yinelenen istek iletilmez); kayıt tazelenir.
      - Yanıt çok-yayın selam olduğu için kayıt isteyeni tutmaz.
    - **Tutulan bir istek varken** rotamın turu ≥ t olursa "hemen gönder" ve kayıt silinir. Yanıt böylece istek yolundan geri yayılır.
13. **Tur yalnız istekle artar**, yalnız geçitte; başlangıcı `TUR_BASLANGIC`'tir. RFC 8966 seçili rotanın turu yüzünden rota yeğlemeyi yasaklar (§3.6): seçim kuralı 5'te tur yoktur.

**E · Kendi karıştırılmam**

14. **Kendi durumum "yok" değilken** (B2): seçim aynı kurallarla sürer. B3'ün maliyetleri hariç aralıkla korunduğu için adaylar ve maliyetleri değişmez. Tur isteği (kural 10–11) gönderilmez; durumum "yok"a dönünce açlık sürüyorsa hemen gider. Gerekçe: sorun benim alıcımda, yanıtları duyamam; gereksiz tur artışı bütün ağı çalkalar (önceki KK-04'ün 18 Kasım sürümü, kural 8).

**F · Çıktılar ve sıra**

15. **Çıktılar:**
    - **aday listesi** (B5 için): O sınıfı `m_j` sırasıyla, sonra S sınıfı; her adayda (komşu, `m_j`, sınıf, ardıl mı);
    - **ilan:** (tur, C) (B6 için);
    - **olaylar** (B6 için "hemen gönder"):
      - ∞ ↔ sonlu;
      - ardılın değişmesi;
      - tur değişimi (istek yanıtı);
      - kural 12'nin yanıtları;
    - maliyetin önemli değişimi: önemlinin eşiği B6'nın;
    - **tur isteği iletileri:** (alıcı ya da çoklu yayın, istenen tur, kalan atlama) (B6 gönderir);
    - **ardıl değişti** olayı (B5, B7).
16. **Sıra:** her niyetli kancada B1 → B2 → B3 → B4 → B5. B4'ün kendi sırası:
    1. gelen ilanların ve isteklerin kaydı;
    2. ilanın ömrü (kural 4);
    3. uygulanabilirlik ve aday kümesi (kural 1–3);
    4. yok sayma (kural 10);
    5. seçim (kural 5–7);
    6. ilan ve FD (kural 8–9);
    7. açlık (kural 11);
    8. istekler (kural 12).

    Selam niyetli bir kancada gelir (`kontrol_alindi`); ilanı o kancada işlenir.
17. **Döngü tanısı** (yalnız ölçüm): paket bana daha büyük bir atlama sayısıyla yeniden gelirse sayılır. Uygulanabilirlik koşuluyla bu sayı 0 olmalıdır (§15). Bir mekanizma değildir; sınamada 0'dan büyük çıkması hatadır.

## 6 · İletiler

B4 ileti göndermez; ilanı ve tur isteğini B6 taşır. B6'dan beklediklerim (Aşama 2.6'da kapanır):

- **Ö-1** Her selamda ilan bulunur: tur (16 bit) ve maliyet (16 bit, B3 kural 2'nin birimi; 0xFFFF = ∞). Bedeli selam başına 4 bayt. Bugünkü çekirdekte yalnız maliyet var, yani 2 bayt eklenir.
- **Ö-2** "Hemen gönder" olayında selam en kısa sürede gider (B1 Ö-4'ün en kısa aralığıyla). Geri çekme (∞) ve ardıl değişimi olaylardır (RFC 8966 §3.7.2).
- **Ö-3** Tur isteği iletisi: istenen tur (16 bit) ve kalan atlama (8 bit, başlangıcı `ISTEK_ATLAMA`). Açlıkta çoklu yayın, yok saymada ve iletmede tek alıcılı (7 deneme). Boyu ⌈24/8⌉ + 64 = 67 bayt; yalnız açlıkta ve yok saymada gider.
- **Ö-4** Selamın aralık alanı (B1 Ö-2) ilanın ömrü için de kullanılır (kural 4). Aralık değişirse ömür ona göre değişir.

**Kontrol yüküne katkı:** selam başına 2 bayt (tur alanı) ve tur istekleri. İlk çekirdekte (18 Kasım) koşu başına 822 açlık ve 92 tur artışı vardı. Açlığın kökü kalktıktan sonra istek sayısı tanıda sayılır.

## 7 · Değerler

`ILAN_OMUR_KAT` · `DUZ_S` · `YOK_SAYMA_S` · `ISTEK_YINELEME` · `ISTEK_ARALIK_S` · `ISTEK_ARA_S` · `ISTEK_ANIMSA_S` · `ISTEK_BASTIRMA_S` · `ISTEK_ATLAMA` · `FD_UNUT_S` · `TUR_BASLANGIC`. Değeri, birimi, kaynağı, küçük ve büyük olursa ne olacağı ve taranıp taranmayacağı `00-DIZIN.md`'nin değer tablosunda.

## 8 · Kenar durumlar

- **Soğuk açılış:** FD yok, her ilan uygulanabilir. İlk aday ilk sonlu ilanla doğar; ilk sonlu ilanım FD'yi kurar.
- **Geçit:** maliyeti 0, ardılı yok, kendi turunu ilan eder ve yalnız istekle artırır (kural 13). Geçit için açlık yoktur.
- **Hiç komşu yok:** C = ∞, istek yok (uygulanamaz ilanlı komşu yok). **Tek komşu:** o komşu uygulanabilirse ardıldır; S'de ise yine kullanılır (E1).
- **Düğüm kendisi karıştırılırken:** kural 14.
- **Komşu karıştırılırken:**
  - girişimdeki komşu B3'te S'dir; O'da aday varsa ona geçilir;
  - kanal kilidindeki komşu susar; ilanı `ILAN_OMUR_KAT` · a sonra ∞ olur (kural 4).
- **Ardılın maliyeti yükselirken:** ilanı uygulanabilir kaldıkça kabul edilir. Uygulanamaz olursa yok sayılır ve tur istenir (kural 10).
- **Sayaç taşması:** tur 16 bit, modüler. Maliyet 0xFFFE'de doyar; FD.maliyet de öyle.
- **Zaman aşımı:** ilanın ömrü (kural 4), yok sayma (kural 10), istek dizisi (kural 11), istek kaydı (kural 12), FD (kural 9).
- **Aynı anda olaylar:** kural 16. Aynı kancada hem ilan hem tur isteği gelirse önce ilan işlenir.
- **Tamponun dolması:** B4'ün tamponu yok; paketlerin bekletilmesi B7'nin.

## 9 · Arayüz

**Kancalar:**

| kanca | B4'e giden | B4'ün işi |
|---|---|---|
| kontrol iletisi alındı: selam | gönderen, tur, maliyet | kural 16'nın sırasıyla bütün kurallar |
| kontrol iletisi alındı: tur isteği | gönderen, istenen tur, kalan atlama | kural 12, sonra seçim |
| saniyelik zamanlayıcı, uyandırma, iletim başarısız, sonraki atlama | — | kural 4–11 (süreler, seçim) |
| niyetsiz kancalar | — | — |

**Okuduğu:** B1, B2, B3 (§2), yalnız kendinden aşağıdakileri (sözleşme 1).

**Çıktılar ve okuyanlar:**

| çıktı | kural | okuyan |
|---|---|---|
| aday listesi (sınıf ve maliyetle) | 15 | B5 |
| ardıl, ardıl değişti olayı | 5, 15 | B5, B7 |
| ilan (tur, C), "hemen gönder" olayları | 8, 15 | B6 |
| tur isteği iletileri | 10–12 | B6 |
| açlık durumu | 11 | B7 (bekletme) |

## 10 · Kapalıyken davranış

B4'ün bütünü çekirdektir, bayrağı yoktur. Uygulanabilirlik koşulu kapatılamaz: kapatmak döngüsüzlüğü kaldırır. Alt mekanizmalar (genel):
- **`duzgun_gecis` kapalı:** isteğe bağlı geçişte yalnız anlık maliyet (kural 6).
- **`ilan_omru` kapalı:** ilan, komşu B1'de silinene kadar geçerli (kural 4).

Karıştırma katmanı kapalıyken B3 son çare durumunu yalnız "veri yok" sebebiyle verir; B4 aynı kurallarla çalışır.

## 11 · Etkileşimler

1. **B3:**
   - B4 bağ maliyetini B3'ten okur, yeniden hesaplamaz (sözleşme 3).
   - S sınıfı B3'ün son çare durumudur; "son çare" adı B4'te başka anlamda kullanılmaz (`00-DIZIN` ortak sözlük).
   - Selam ölçeği sıkıştırır (B3 §11 madde 3); yol maliyeti iyi bağlardan geçen yolları biraz kayırır.
2. **B5:**
   - Aday listesinin her üyesi uygulanabilirdir. B5 paketi listeden hangi komşuya gönderirse göndersin döngü oluşmaz (§15).
   - B5'in paket başına sapmaları (ör. karıştırma ekinde yedekten göndermek) rota durumunu değiştirmez (sözleşme 5).
3. **B6:** ilan her selamda (Ö-1); olaylar "hemen gönder"; tur isteği iletileri.
   - Karıştırmanın ilana yansıtılmaması bilinçli bir seçimdir. Ardılım S'deyken de ilan B3'ün maliyetiyle gider. Bu yüzden yukarıdaki düğümler yolumun karıştırıldığını ilandan bilmez; bunu kendi bağ ölçüleriyle ve B2'nin kanıtıyla görürler. Karıştırmayı ilana katmak, maliyeti yükseltip yukarıda uygulanamaz ilanlar ve açlık doğururdu (kural 1, 10). Bir "yolum karıştırılıyor" bitiyle bilgiyi bir atlama yukarı taşımak da düşünülebilir; ölçülmediği için alınmadı (§15).
4. **B7:** açlıkta paketler bekletilir; ne kadar ve ne zaman düşeceği B7'nin.
5. **B2:** kendi durumum yalnız tur isteğini bastırır (kural 14).
6. **Kanıtı silmeme** (sözleşme 4): B4 hiçbir gözlemi silmez. Uygulanamaz ilanı yok saymak (kural 10) yalnız seçimi geciktirir; ilan kaydedilir, süre dolunca uygulanır.
7. **Eski döngü kuralları:** geri gönderme yasağı ve döngü bekçisi gerekmez. Uygulanabilirlik koşulu paketi getiren komşuya geri göndermeyi de kendiliğinden önler: getiren komşu, yolu benden geçtiği için bana uygulanamaz görünür (§15). Döngü yalnız tanıda sayılır (kural 17).

## 12 · Örnek senaryo

Maliyetler ETX cinsinden (tamsayısı × 64). i'nin FD'si (tur 7, 2,0).

1. **Olağan:** komşular ve ilanları j (7 · 1,2), k (7 · 1,4), l (7 · 2,3); bağ maliyetleri (B3) j 1,1 · k 1,3 · l 1,0.
   - Uygulanabilirlik: j (1,2 < 2,0) ve k (1,4 < 2,0) uygulanabilir; l (2,3 ≥ 2,0) değil.
   - Adaylar: `m_j` = 2,3, `m_k` = 2,7. Ardıl j, C = 2,3, ilan (7, 2,3).
   - FD (7, 2,0)'da kalır, çünkü 2,3 > 2,0.
2. **Ardıl karıştırılıyor:** j'nin bağı B3'te SON ÇARE olur. O sınıfında k var: zorunlu geçiş (kural 5), ardıl k, C = 2,7, ilan (7, 2,7), "hemen gönder".
3. **Karıştırma bitiyor:** j'nin bağı OLAĞAN'a döner. B3'ün maliyeti hariç aralık sayesinde 1,1'de kalmıştı. Sonuç: `m_j` 2,3 < `m_k` 2,7 ve `ms_j` < `ms_k`; ardıl hemen j'ye döner.
4. **Uygulanamaz ilan:** j'nin maliyeti yükselir, ilanı (7, 2,1) olur ve uygulanamaz (2,1 ≥ FD 2,0).
   - i yok sayar: ardıl j, eski ilanla (1,2) kalır. j'ye tek alıcılı tur isteği gider (istenen 8).
   - İstek j'nin ardıl zinciriyle geçide ulaşır; geçit turunu 8 yapar ve ilan eder.
   - Yanıt istek yolundan döner. j (8, 2,1) ilan eder: daha yeni tur, uygulanabilir. i kabul eder, C = 1,1 + 2,1 = 3,2, ilan (8, 3,2) ve FD (8, 3,2) olur.
5. **Açlık** (4. adımdan sonra, FD (8, 3,2)): j ve k ∞ ilan eder (ikisi de yolunu kaybetti); l'nin ilanı (8, 3,5) uygulanamaz (3,5 ≥ 3,2).
   - Aday yok: i ∞ ilan eder.
   - l'nin bağı KULLANILMAZ değil: tur isteği (istenen 9) çoklu yayınla gider; 0,5 s arayla üç kez daha yinelenir.
   - Yeni tur gelince l (9, 3,5) ilan eder; ilan uygulanabilir olur ve l ardıl seçilir: C = 1,0 + 3,5 = 4,5, FD (9, 4,5).
6. **Susan komşu:** k kanal kilidinde; son ilanı 2,2 s aralıkla gelmişti. 3,5 × 2,2 = 7,7 s sonra k'nin ilanı ∞ sayılır ve k aday olmaktan çıkar. Kilit kalkınca k'nin selamı gelir, ilanı yeniden değerlendirilir.

## 13 · Sınanması

**Birim testleri** (Aşama 4):

1. **Uygulanabilirlik:**
   - ∞ hep uygulanabilir; FD yokken her ilan uygulanabilir;
   - daha yeni tur ve aynı turda küçük maliyet uygulanabilir, eşit maliyet uygulanamaz;
   - 65535 → 0 tur taşması.
2. **Yol maliyeti:** toplama, 0xFFFE'de doyma, ∞.
3. **Aday kümesi:**
   - KULLANILMAZ bağ, ∞ ilan, bayat ilan (kural 4) ve uygulanamaz ilan dışarıda;
   - O ve S sınıfları.
4. **Seçim:**
   - zorunlu geçişte O önce, O boşsa S;
   - ardıl S'deyken O doğunca geçiş;
   - isteğe bağlı geçişte iki maliyet birden;
   - eşitlik sırası;
   - `duzgun_gecis` kapalı.
5. **Düzgünleştirme:** zaman sabiti; yeni adayda başlangıç; S'deki adayın güncellenmesi.
6. **FD:** sonlu ilanla kurulur ve güncellenir; geri çekme FD'yi değiştirmez; `FD_UNUT_S`.
7. **Yok sayma:**
   - ilk yok saymada tek alıcılı istek;
   - `YOK_SAYMA_S` dolunca son ilanın uygulanması;
   - bu sürede uygulanabilir ilanla bitmesi;
   - ∞ ilanın yok sayılmaması.
8. **Açlık:**
   - istek yalnız uygulanamaz sonlu ilanlı ve bağı kullanılır komşu varken;
   - yineleme sayısı ve aralıkları;
   - kendi durumumda bastırma ve çıkışta hemen istek.
9. **İstek gelince:**
   - yanıt;
   - geçitte tur artışı (bir istekle bir);
   - iletme sırası ve alıcısı;
   - kalan atlama;
   - bastırma;
   - kayıt ve yanıtın geri yayılması.
10. **İlan:** turu ardılınki, geçitte kendininki; ∞'da FD'nin turu.
11. **Olaylar:** ∞ ↔ sonlu, ardıl değişimi, tur değişimi.
12. **Döngüsüzlük (uçtan uca):** küçük test dünyasında rastgele maliyet değişimleri ve kopmalarla döngü tanısı (kural 17) 0.
13. Örnek senaryonun (§12) sayıları uçtan uca.

**Ölçümde sayılacak tanı:**
- açlık bölümlerinin sayısı ve süresi, kökü (ardılın ∞'u, ilanın ömrü, uygulanamaz ilan);
- tur artışı ve tur isteği sayısı, isteğin geçide ulaşma süresi;
- yok sayma sayısı ve sonucu;
- ardıl değişimi, sebebine göre (zorunlu, isteğe bağlı, S'ye düşme ve dönüş);
- S sınıfından seçilen ardıl ve süresi;
- ilanın ömrüyle düşen adaylar;
- döngü tanısı (0 beklenir);
- yol maliyetinin dağılımı.

## 14 · Kaynak

- **Uygulanabilirlik koşulu, FD'nin tutulması, geri çekme, rota edinimi ve seçimi, tetiklenen ilanlar, tur istekleri ve iletilmeleri, açlığın önlenmesi, uygulanamaz güncellemeler:** Babel, RFC 8966 [4]: §3.5.1–§3.5.3, §3.6, §3.7.2–§3.7.3, §3.8.1.2, §3.8.2.1–§3.8.2.2. DSDV ailesinden (De Couto 2003'te [36] aktarıldığı gibi).
- **Anlık ve düzgünleştirilmiş maliyetle geçiş:** RFC 8966 Ek A.3.
- **İlanın ömrü:** Babel'in rota süresinden (Ek B), selam aralığına uyarlanarak.
- **Uygulanabilir komşuların hazır yedek olması:** DUAL'ın uygulanabilir ardılı [65].
- **Bu tasarımın:**
  - adayların B3'ün durumuna göre iki sınıfta sıralanması (E1);
  - kendi karıştırılmamda tur isteğinin bastırılması;
  - FD'nin ilan için verildiği anda, gönderilmesi beklenmeden güncellenmesi;
  - selama gömülü ilanın ömrü;
  - isteğin yalnız kullanılır bağlı uygulanamaz komşu varken gönderilmesi.

Önceki tasarımın 18 Kasım sürümü de bu ailedendi (`../arsiv/kural/KK-04-ROTA-2026-11-18.md`). Kurallar oradan alınmadı, RFC'den yeniden yazıldı. Farklar: aday sınıfları, ilanın ömrü, RFC'nin uygulanamaz yola istek iletmesinin eklenmesi.

## 15 · Döngüsüzlüğün gerekçesi ve ölçülmeyen

**Döngüsüzlük** (RFC 8966 §2.4, §3.5'in gerekçesi):
- Bir düğüm yalnız uygulanabilir komşuya paket gönderir: komşunun ilanı benim FD'mden kesin iyidir.
- Komşunun kendi FD'si, onun gönderdiği her sonlu ilandan iyi ya da ona eşittir. Bu yüzden paketin geçtiği düğümlerin FD'si her atlamada kesin iyileşir. Karşılaştırma önce tura, sonra maliyete bakar; maliyet her atlamada kesin artar (kural 2).
- Bu yüzden paket aynı düğüme dönemez. Kural, B5'in aday listesinden yaptığı her seçim için de geçerlidir: listedeki her aday uygulanabilirdir.
- FD'nin tutucu güncellenmesi (kural 9) bunu bozmaz: FD yalnız küçülebilir.

**Ölçülmeyen** (Aşama 4'te sayılır ya da ablasyonla ölçülür):
- açlığın yeni tasarımdaki sıklığı (iki kökü kalktı, kendisi ölçülmedi);
- ilanın ömrünün etkisi (`ilan_omru`);
- S sınıfının kullanım sıklığı ve etkisi;
- değerler (`DUZ_S`, istek aralıkları);
- karıştırmayı bir atlama yukarı taşıyan bir bitin (§11 madde 3) gerekip gerekmediği.

Açlık yüksek kalırsa `18` §2.4'teki Y3'ün açlıktaki son çaresi o zaman düşünülür.
