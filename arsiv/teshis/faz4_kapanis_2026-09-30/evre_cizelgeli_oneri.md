# Evre metrikleri — çizelgeli karıştırıcı · öneri v2 (denetim B8) — ÖĞRENCİ ONAYI BEKLİYOR

> 30 Eylül 2026 · ajan · öğrenci: *"yeni bir şey, hata olması durumunda sıkıntı olur — bir süre daha düşün"*. v1 (`evre_cizelgeli_oneri_v1.md`, evre katlama) geri çekildi; kusurları §2'de. Birincil metrik PDR (pencere) değişmez; evre metrikleri betimleyici/mekanizma kanıtıdır (`06` §3).

## 1 · Eldeki veri ne diyor (yeni koşu yok)

Komut: `PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz4_kapanis_2026-09-30/evre_mevcut_veri.py` — K-200 partisi, birincil hücre, geliştirme tohumları 1003–1006.

- **Çizelge:** `T_j` 150 s'den sonra 15 s açık · 15 s sessiz; ölçüm sonu 320 s. **İlk açık dönem `[150; 165)` = `08`in ŞOK penceresiyle birebir** (açık süre = `L` = 15 s). Açık 6 × 15 = 90 s · sessiz 5 × 15 + 5 = 80 s. Karıştırıcı her sessizde 250 m batıya taşınır (K-192) → çevrimler özdeş değil.
- **Bugünkü M3 anlamsız:** 0–45 s. 15 s'lik kayan pencere açık ve sessizi karıştırıyor.
- **Bugünkü M4 yanıltıcı:** 24 koşunun 4'ünde tespit var (AODV 32 · 32 · 62 s, DESPARETE 31 s). Hepsi **2. ya da 3. açık dönemin 1–2. saniyesinde**; ilk açık dönemde hiçbir koşuda yok. "32 s gecikme" gibi okunur, oysa anlamı "ilk açılmayı kaçırdı". Muhtemel sebep: ED ile kilitli düğüm iletimi erteliyor, MAC başarısızlığı yok, kopma beyanı yok (ölçülmedi).
- **Sessiz / önce oranı (M2 adayı):** kâhin 0,985 (0,96–1,04) · DESPARETE 0,964 · AOMDV 0,975 · AODV 0,891 · OLSR **1,096** (en çok 1,26) · OLSR §13 **1,197** (en çok 1,42). OLSR'ın sessizdeki PDR'si karıştırıcıdan ÖNCEKİNDEN yüksek. İki açıklama mümkün: OLSR önce evresinde durağan değil, ya da gerçek bir mekanizma (karıştırma kötü bağları budayıp MPR seçimini düzeltiyor). ÖNCE referansı bu ikisini ayıramaz.
- **Kuyruk 50 çerçeve, ömür yok:** kilitli düğümdeki paket bütün açık dönem boyunca bekleyip sessizde teslim edilebilir. Doğum anına göre kovalamada evre sınırı saniyelerce bulanıklaşabilir; G4 (`p99 / 1 s < 1`) bu hücrede ölçülmedi.

## 2 · v1'in kusurları

1. **M3ç 1 s'lik kovayla "toparlandı" diyordu.** Bu, `08` §02'nin kendi ilkesine aykırı (`L` = 15 s durağanlıktır; dar pencere geçici sıçramayı toparlanma sanar). Katlama gürültüyü azaltır, bu ilkeyi düzeltmez. Sessiz dönem `L`'ye eşit: `08` anlamında toparlanma süresi bir sessiz dönemin içinde tanımlanamaz.
2. **Katlama özdeş çevrim varsayıyordu.** Karıştırıcı her çevrimde yer değiştiriyor ve protokol önceki çevrimin durumunu taşıyor. İlk açılma temiz durumdan başlar, sonrakiler yarım toparlanmış durumdan; katlama bunları aynı kovaya karıştırırdı.
3. **M2ç'nin referansı (ÖNCE) protokolün durağan olduğunu varsayıyordu.** OLSR'ın 1'in üstündeki değerleri bunun sınanması gerektiğini gösteriyor. v1'in boş kol kapısı hareketliliği belirtmiyordu.
4. **M4ç'nin katlanmış kovadaki boş dağılımı yazılmamıştı** (k kovanın toplamı → çevrimler arası bağımsızlık varsayımı).
5. **G4 (bulanıklık) ele alınmamıştı.**

## 3 · v2 — en az yeni tanım

İlke: ön-kayıtlı metriğin anlamı korunuyorsa aynen kalır. Yalnız zorunlu olan tanımlanır. Gerisi karar kuralı taşımayan betimleyici teşhise gider. Yeni serbest sayı yok.

| metrik | çizelgeli karıştırıcıda | bugüne göre |
|---|---|---|
| **M1 · ilk vuruşun derinliği** | `PDR(ÖNCE) − PDR(ŞOK)`, ŞOK = `[T_j; T_j + min(L, açık_s))` | birincil hücrede **birebir** (ilk açık dönem, temiz durumdan). `min` yalnız koruma: açık süre `L`'den kısa olsaydı ŞOK sessize taşmasın |
| **M2 · toparlanma tamlığı** | `PDR(bütün sessiz dönemler) / PDR(ÖNCE)`, kırpılmaz | pencere: TOPARLANMA → sessiz dönemlerin birleşimi (kısmi son sessiz dâhil) |
| **M3 · toparlanma süresi** | **tanımsız** → `None`, sebep `cizelgeli` (sansürden ayrı alan) | yerine bir metrik uydurulmaz |
| **M4 · tespit gecikmesi** | tarama **ilk açık dönemle** sınırlı `[T_j; T_j + açık_s)`; Bonferroni sayısı taranan pencereden (15); dışındaki tespit → SANSÜRLÜ | tarama aralığı |

Sürekli karıştırıcılı hücrelerde dördü bugünküyle birebir kalır: açık dönem pencere sonuna kadar sürer, `min(L, ∞) = L`. Çizelgeli aile bugün yalnız `derin_sizma`.

Eldeki veriye uygulanınca: M1 aynı · M2 §1'deki oranlar · M3 `None` · M4 24 koşunun hepsinde SANSÜRLÜ. Sonuncusu bir bulgudur ve gizlenmez: beyan tabanlı tespit bu hücrede ilk açılmada ateşlenmiyor.

## 4 · Betimleyici teşhis (karar kuralı yok, iddia taşımaz)

- **Katlanmış 1 s profili:** 30 s'lik çevrim; protokol ve kâhin; çevrimler ve tohumlar havuzlanır. "Zamansal uyum"un şekli olarak rapora girer. Özdeş çevrim varsayımı şeklin altında beyan edilir.
- **Çevrim başına açık/sessiz PDR ve kâhine oranı.** Öğrenme ile karıştırıcının yaklaşmasını kâhin oranı ayırır.
- **Tespitin ilk görüldüğü açık dönem:** 1., 2., …, yok.
- **Evre sızıntısı:** bir evrede doğup akıbeti (teslim ya da düşme) başka evreye düşen paket oranı. Bu, G4'ün bu hücredeki ölçüsüdür.
- **Tek bölümleme:** anatomi aracının önce/açık/sessiz ayrımı aynı fonksiyondan gelir. İkinci bir kural ikisinin ayrışabileceği anlamına gelirdi (`evre.py` başlığındaki sansür ilkesinin aynısı).

## 5 · Kapılar — ölçüt ölçmeden önce, burada

- **G1ç · boş kol, birincil hücrenin hareketliliğiyle.** Hücre: formasyon · yere toplama · karıştırıcısız, hayalet çizelgeyle (150 s'den 15 · 15). Protokoller: AODV · OLSR · AOMDV · DESPARETE × tohum 1003 · 1004. G1-P'nin kuralları aynen:
  - M4 yanlış tespit ≤ 1/8
  - M1 2 SE dışında ≤ 1/4 protokol
  - **yeni madde:** `D = PDR(sessiz) − PDR(ÖNCE)` iki tohumda da 2 SE dışında kalan protokol yok (SE M1'inkiyle aynı, K-196).

  **D'de kalan protokol:** o protokolün M2'si birincil hücrede **"yorumlanamaz (ÖNCE referansı durağan değil)"** diye yazılır, boş koldaki değeri yanında durur. Düzeltilmiş bir sayı üretilmez: iki tohumdan düzeltme gürültüyü sonuca taşırdı.
- **G2ç · tutarlılık (karıştırıcı açık, kâhin, 1003 · 1004):**
  - kâhinde M1 kol ortalamasında 2 SE dışında, yani karıştırıcı etkili
  - kâhinde D 2 SE içinde: grafiği geçişte yenilenen kâhin sessizde anında temiz olmalı. Kalırsa evre bölümlemesinde hata aranır.
- **G4ç · bulanıklık:** evre sızıntısı ve gecikme p99 ölçülür. M1 ve M2 bütün-evre toplamıdır, ölçüt `p99 < açık_s` (G4'ün evre çözünürlüğündeki karşılığı). 1 s profili `p99 ≥ 1 s` ise "bulanık" etiketiyle çizilir.
- **Sentetik birim testleri** (bilinen cevaplı defterler):
  - bölümleme (kısmi son sessiz dâhil)
  - M4 taramasının ilk açık dönemde durması
  - M3'ün `cizelgeli` sebebi
  - sürekli karıştırıcıda dört metriğin birebir kalması (mevcut testler)

## 6 · Sıra ve maliyet

- **Kod onaydan sonra, U1 koşarken:** U1 dondurulmuş kopyadan koşuyor. Değişecekler: `sim2/olcum/evre.py` + `metrikler.py`; anatomi aynı bölümlemeyi kullanır; testler. Sıcak yola dokunmaz.
- **Regresyon k203 bu değişiklikten SONRA:** tek regresyon hem B4'ü hem bunu doğrular. `regresyon_beklenti.md`ye beklenen fark eklenir: `i-statik-surekli-dogrudan_komsu-derin_sizma` satırının evre alanları. `u-` vakaları zaten yeni.
- **Süreler:** G1ç ~1–1,5 saat (formasyon, 10 koşu) · G2ç ~30–60 dk · testler saniyeler. Hiçbiri başka bir ağır işle aynı anda koşmaz.

## 7 · Karar istenen

1. v2 tanımı: M1 aynı · M2 sessiz dönemler · M3 tanımsız · M4 ilk açık dönem.
2. Kapılar, ve G1ç'de kalan protokol için "yorumlanamaz" kuralı (düzeltilmiş sayı yok).
3. Katlanmış profil yalnız betimleyici (raporda şekil, iddia değil).
