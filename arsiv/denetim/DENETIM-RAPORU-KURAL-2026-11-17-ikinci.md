# Faz 5-3 kural kâğıtları — bağımsız denetimin ikinci okuması (17 Kasım 2026)

## 0 · Başlık bilgisi

- **Denetlenen hâl:** `main` @ `94c0ed6fefe4e3d2ee7cd60e643ec1adad1403c7` + çalışma ağacındaki commit'lenmemiş düzeltmeler (`git diff 94c0ed6`: 7 dosya, 229 ekleme / 158 silme) + `arsiv/denetim/DENETIM-KURAL-KAPANIS-2026-11-17.md`.
- **Başlangıç:** `git rev-parse HEAD` → `94c0ed6fefe4e3d2ee7cd60e643ec1adad1403c7`; `git diff 94c0ed6 | md5sum` → `1269e7c9046c33859368d7cd1d6a5e6f` (istemdekiyle aynı); `git status --short` → ` M v2/17-TASARIM-KARARLARI.md` · ` M v2/kural/KK-00…KK-05` (6 dosya) · `?? arsiv/denetim/DENETIM-KURAL-KAPANIS-2026-11-17.md` · `?? arsiv/denetim/DENETIM-PROMPT-KURAL-2026-11-17.md` · `?? arsiv/denetim/DENETIM-RAPORU-KURAL-2026-11-17.md`.
- **Son:** HEAD ve md5 değişmedi (`94c0ed6…` · `1269e7c9046c33859368d7cd1d6a5e6f`); `git status --short`a yalnız bu rapor eklendi (`?? arsiv/denetim/DENETIM-RAPORU-KURAL-2026-11-17-ikinci.md`).
- **Okunanlar:** yeni KK-00…KK-05 tam metin; `v2/17` farkı (T-2, T-9, T-13); kapanış belgesi; ilk raporun kaynakları (RFC 8966, teşhis (d) `sonuc.md`, `sim2/` kancaları) gerektiği yerde yeniden kullanıldı.
- **Yöntem:** yeni durum makinesi için durum × olay tablosu yeniden kuruldu, her kapanış iddiası metinde arandı. Zaman çizelgeleri depo dışında iki yeni betikle yürütüldü (`askida.py`, `ceza_askida.py`; simülasyon değil, simülatör çağrılmadı, tohum kullanılmadı); varsayımlar ilgili bulguda.
- **Hüküm özeti:** **kodlamaya geçmeye engel yok.** Altı önemli ve yedi küçük yeni bulgu var. Hepsi yerel kural düzeltmesi ya da değer meselesi; döngü, ölü durum ya da geliştirme hücrelerinde kalıcı kara delik üretmiyor. Kodlamayla birlikte, bir kısmı ilgili A/B'nin beklentisinden önce kapatılmalı (§6).

---

## 1 · İlk raporun bulgularının durumu

| # | durum | gerekçe · yer |
|---|---|---|
| B-1 | kapandı | ∞ her zaman uygulanabilir, `A` yalnız sonlu ilanlı, ∞ yok sayılmaz, ardıl hemen bırakılır (`KK-04:20–24, :26, :30`; T-13). Zincir örneği kâğıtta (`KK-04:50`). |
| B-2 | kısmen | ED alıcısında kapandı: sessizlik kanıtı son selamdan `(k+0,5)·a` sonra tamamlanır, ASKIDA tetik anından `(k+1)·a` sürer; `k ≤ 4` (a = 2,2 s) iken kanıt her zaman ASKIDA içinde. Girişim alıcısında kanıt bittir ve gecikmesi ASKIDA'nın süresine bağlı değil (Y-1). Kendi karıştırılmamın başlangıcında yeni bir açık var (Y-2). KARIŞTIRILIYOR'a girişte veri penceresi boşaltılıyor (`KK-01:53`). |
| B-3 | kapandı | "Kendi" sebebi kalktı (`KK-03:37, :45`); KARIŞTIRILIYOR'un üst süresi var (`KK-01:59`); ASKIDA süreli. Yeni makinede ölü durum yok (§4). |
| B-4 | kapandı | Aynı olayda sıra (`KK-01:69`); sebep kümesi (`KK-03:38–45`); geçişler kural 7–12'de çelişkisiz. Ayrı kancalardaki olaylar da doğru işliyor: veri tetiği `iletim_sonucu`nda ASKIDA'ya alır, aynı vazgeçmenin MAC kanıtı `iletim_basarisiz`da ASKIDA'dan KARIŞTIRILIYOR'a taşır. Yazılmayan tek eşzamanlılık "ASKIDA + kendi durumumun başlaması" (Y-2). |
| B-5 | kapandı | Dondurmadan çıkışta boşluk için 0 yok, sıfırlama yok (`KK-01:42, :58, :64`). |
| B-6 | kapandı | `aralik` = katlamadan sonraki `I`'nın 1,1 katı, üst sınır (`KK-02:14, :25`; `KK-01:44`). Sayısal yan etkisi Y-9. |
| B-7 | kapandı | `s` algoritmik (`KK-03:25`); payda 0 → işaret yok; eşiğin kâhin sayımlı dayanağı yazıldı (`KK-00:41`). Küçük ayrıntı Y-10. |
| B-8 | kapandı | İstek yalnız OLAĞAN, sonlu, uygulanamaz ilanlı komşu varken; öteki durumlar açık (`KK-04:35–38`). |
| B-9 | kapandı | Uygulanabilirlik her seçimde güncel FD ile (`KK-04:20`). |
| B-10 | kapandı (kararla) | Tetik yalnız bekleyen isteği karşılayan tur değişiminde (`KK-02:28`); istek kaydı ve geri yayılım (`KK-04:42–44`). Yan etkiler Y-11 ve Z-2. |
| B-11 | kapandı (kararla) | Kendim karıştırılırken MAC sonuçları bağ kanıtı değil, veri tetiğine girmez (`KK-03:37`; `KK-01:47, :64`; T-9). İki yeni açık: başlangıç (Y-2), üst süre (Y-6). |
| B-12 | kapandı | `VERI_EN_AZ` = 4 (`KK-01:47`; `KK-00:30`). |
| B-13 | kısmen | Mekanizma–bayrak–sınıf–kapalıyken tablosu ve kapının "hepsi kapalı" yapılandırması var (`KK-00:60–75`). İki satır sorunlu: ASKIDA'nın beklemesinin sınıfı ve `karistirma_durumu` kapalıyken davranışı (Y-4); `uyarlanir_aralik` kapalıyken ara ilanla çelişki (Y-5). |
| B-14 | kapandı | Sınıfa göre A/B ölçütü; yer karıştırıcılı aile beklentide (`KK-00:77–83`). |
| B-15 | kapandı | `I_MAX`, `ISTEK_YINELEME`, `ISTEK_ATLAMA = 64`, `T_HATIRA` dayanakları düzeltildi (`KK-00:32, :36, :45, :48`). B-6'dan sonra sayılarda küçük kayma (Y-9). |
| B-16 | kapandı | Ardılsız ya da ardılı isteyen olan düğüm iletmez; RFC'den farkı yazılı (`KK-04:42–43`). |
| B-17 | kapandı | Yok sayma sayacı tam tanımlı (`KK-04:29–34`). |
| B-18 | kapandı, bir yan etkiyle | Birimler (`KK-00:21`), `c̄` (`KK-03:23`), işaretsiz saniye (`:26`), `k`'nın sınırı (`:35`), varış sırası (`:42`), silme duraklaması (`KK-01:64`), eşit maliyet (`KK-04:25`), çıkışta istek (`:38`). "Kaynak değişimi" kuralı ED'de yanlış çalışıyor (Y-3). ∞ ilanın tur alanı yazılmadı (Y-8). |
| B-19 | kapandı | Niyetsiz kancalar (`KK-00:19`); `ilk_bekletme` yaş sınırı; iz tazelenmesi (`KK-05:22–23, :28`). |
| B-20 | kapandı | T-18'in sınır türü (`KK-05:24`); T-11'in kalanı (`KK-01:63`); §7 madde 8–9 tanı kaydında (`KK-00:91`). |
| S-1 | izleniyor | Tanı kaydında (`KK-00:87`; `KK-01:78`). ASKIDA yanlış alarmın bedelini artırdı (Z-1). |
| S-2 | izleniyor | Tanı kaydında (`KK-00:88`; `KK-05:40`). |
| S-3 | izleniyor | Tanı kaydında (`KK-00:90`). |
| S-4 | izleniyor, önemi arttı | Tanı kaydında (`KK-00:89`; `KK-03:60`). Girişim alıcısında bitin güvenilirliği artık ASKIDA'nın sonucunu belirliyor (Y-1). |
| S-5 | kapandı | `ISTEK_ATLAMA = 64` ve en uzun atlama tanıda. |
| S-6 | kapandı | Çekince yazıldı (`KK-00:41`; `KK-03:25`). |
| S-7 | açık, kabul edilmiş | Değişiklik yok (bilinen sınır). |
| S-8 | açık, kabul edilmiş | T-13 kararlaştırmamış. |

---

## 2 · Düzeltmelerin getirdiği yeni bulgular

### Önemli

#### Y-1 · ASKIDA'nın süresi bit kanıtının gecikmesini kapsamıyor; KÖTÜ'de gelen geç kanıt cezayı kaldırmıyor

- **Yer:** `KK-00-DIZIN.md:31` (`ASKIDA_SURE`) · `KK-01-BAG.md:52` (kural 8) · `:62–63` (kural 11–12).
- **Ne yanlış:** `ASKIDA_SURE = min((k+1)·a, 10 s)` yalnız sessizlik kanıtının zamanına göre kurulmuş. Girişim alıcısının kanıtı ise bittir. Bitin gecikmesi `a`'dan bağımsızdır: `s`'nin 4 s'lik pencerede 0,6'yı geçmesi (~2,6 s), `GIRIS_SANIYE` ardışık işaretli saniye, ardından bir selam. Karıştırma başlarken komşulukta maliyet olayları sıktır; olaydan hemen sonra `a` 0,55 ya da 1,1 s'dir ve ASKIDA 2,2 ya da 4,4 s'ye iner. Kanıt ASKIDA'dan sonra gelirse bağ KÖTÜ'ye düşer; KÖTÜ'de kanıt izlenmez (kural 12) ve düşüş "kanıtsız" sayılıp cezayı katlar. Bu, kararın "ceza yalnız kanıtsız tekrarlarda katlanır" amacına ters.
- **Kanıt** (`askida.py`; varsayımlar: işaret ancak 3. saniyeden itibaren, her saniye p olasılıkla, iki ardışık işaretle karar, bit gönderende karar + 0,1 s; veri tetiği `t1 ~ U(1,4; 3,5)` s; `k = 3`). Bitin ASKIDA içinde gelme olasılığı:

  | p | a = 0,55 (2,2 s) | a = 1,1 (4,4 s) | a = 2,2 (8,8 s) |
  |---|---|---|---|
  | 0,4 | 0,15 | 0,37 | 0,62–0,64 |
  | 0,6 | 0,32 | 0,66 | 0,90–0,92 |
  | 0,8 | 0,52 | 0,89 | 0,99 |
  | 1,0 | 0,76 | 1,00 | 1,00 |

  İlk raporun ceza modeli düzeltilmiş kurallarla (`ceza_askida.py`; q = bitin ASKIDA içinde gelme olasılığı). Bağın sessiz evrede kullanılamadığı pay:

  | çizelge | q = 1 | 0,9 | 0,64 | 0,37 | 0,15 |
  |---|---|---|---|---|---|
  | 15 s açık · 15 s sessiz | 0,30 | 0,32 | 0,41 | 0,54 | 0,64 |
  | 10 s açık · 20 s sessiz | 0,22 | 0,26 | 0,40 | 0,57 | 0,70 |

  q yüksekken düzeltme amacına ulaşıyor (ilk raporda 0,30 ↔ 0,54). q düşükken sonuç ilk rapordakinden de kötü, çünkü ASKIDA cezadan önce bir bekleme ekliyor. Saniyelik işaret olasılığı p ölçülmedi (S-4; `17` §7 madde 7).
- **Öneri:**
  1. `ASKIDA_SURE`'ye bit gecikmesini kapsayan bir alt sınır, ör. `GIRIS_SANIYE + 4 s + 1,1·I_MIN ≈ 6,6 s`, 10 s tavanı korunarak.
  2. Veri sebepli KÖTÜ'de ceza sürerken KK-03'ün bağ kanıtı gelirse düşüş kanıtlı sayılsın (katlamaya girmesin), ya da ceza ASKIDA'ya girişten sayılsın (Z-1).

#### Y-2 · Kendi karıştırılmamın başlangıcında ASKIDA'ya düşen ardıl KÖTÜ'ye ve cezaya gidiyor

- **Yer:** `KK-01-BAG.md:51–52` (kural 7–8) · `:64` (kural 13) · `KK-03-KANIT.md:37` (kural 8).
- **Ne yanlış:** B-11 kararı ("kendim karıştırılırken MAC sonuçları bağı değiştirmez, ardıl korunur") yalnız durum kurulduktan sonra işliyor. Girişim alanındaki gönderici onayları çözemez; ardıl bağında `ETX_veri` birkaç çerçevede 4'ü geçer ve veri tetiği bağı ASKIDA'ya alır. Göndericinin kendi kararı daha geç gelir: `s` rampası ve iki ardışık işaretli saniye, Y-1'deki dağılımla ≥ ~4 s. Durum kurulunca bağ için kanıt gelemez: ardılın biti 0'dır; `gecmis` dondurulduğu için sessizlik yok (kural 13); MAC yok sayılır (kural 8). ASKIDA süre dolunca KÖTÜ olur (veri sebepli, kanıtsız): ceza alır, periyodik karıştırmada 60 s içinde yinelenip 10 → 20 → 40 s'ye katlanır. Ardıl "korunmaz"; ceza karıştırma bittikten sonraki sessiz evreye taşar. "ASKIDA + kendi durumum başladı" eşzamanlılığı kural 15'te de yok.
- **Kanıt:** kurallar arka arkaya yürütülerek; sıklık doğrulanamadı (gönderici girişimdeyken çerçeve istatistiği teşhis (d)'de yok, sınıflar alıcının alanına göre).
- **Öneri:** "ASKIDA iken kendi durumum 'karıştırılıyorum' olursa bağ ASKIDA'ya girişteki ölçüyle OLAĞAN'a döner, veri penceresi boşaltılır, düşüş cezaya sayılmaz". Ya da kendi girişim işaretim varken veri tetiği ASKIDA'yı başlatmasın (işaret karardan en az bir saniye önce görülür).

#### Y-3 · ED'de girişim işareti de çıktığı için "kaynak son görülen işaret" kuralı ED kaynağını girişime çeviriyor

- **Yer:** `KK-03-KANIT.md:28` (kural 4: "durum sürerken öteki işaret görülürse kaynak son görülen işaretin türü olur") · `KK-02-SELAM.md:33` (kural 5: "kendi ED kaynaklı … durumumda yeni selam kurulmaz") · `KK-03-KANIT.md:29` (çıkış).
- **Ne yanlış:** ED alanında girişim işaretinin iki koşulu da her saniye sağlanır: çözülen çerçeve 8/s ↔ temiz 99/s (`c < 0,5·c̄`, teşhis (d) §7); düğüm neredeyse hiçbir selamı çözemez, yani `s` ≈ 1. `s` rampası dolunca (~3. saniyeden itibaren) ED ve girişim işareti aynı saniyede görülür. "Son görülen" aynı saniyede tanımsızdır; değerlendirme sırası girişimi sona koyarsa kaynak girişim olur. Sonuçlar:
  1. KK-02 kural 5 artık selam kurulmasını durdurmaz: ED boyunca kurulan selamlar kontrol kuyruğunda birikir ve kanal açılınca bayat içerikle (bit = 1, eski maliyet) art arda gider; kuralın önlemek istediği tam budur.
  2. Çıkış 1 s yerine `CIKIS_SANIYE` (3 s) sürer. Komşular bayat bit = 1'i görüp "bit" sebebini ekler, bitti gecikir: sessiz evre kaybı S-3'ün üstüne ~2 s.
- **Öneri:** "ED işareti görülen saniyede kaynak ED'dir; kaynak girişime yalnız ED işaretinin olmadığı bir saniyede geçer."

#### Y-4 · ASKIDA'nın beklemesi "genel" bayrağın altında; `karistirma_durumu` kapalıyken de bekleniyor ve mekanizma kapısı DESPARETE lehine kayıyor

- **Yer:** `KK-00-DIZIN.md:63` (satır "veri tetiği, ASKIDA, ceza → `veri_kotu_tetigi`, genel") · `:64` ("kapalıyken: … veri tetiğiyle ASKIDA'ya giren bağ süre dolunca KÖTÜ olur") · `:75` (kapının "hepsi kapalı" yapılandırması) · `v2/17` T-2 (askıdanın amacı).
- **Ne yanlış:** T-2'nin yeni satırına göre ASKIDA'nın amacı karıştırmaya karşıdır: selam gönderemeyen alıcının bağı kötü sanılmasın. K-247'ye göre sınıf amaçtan belirlenir. Kapının "hepsi kapalı" kolunda kanıt hiç gelmediği hâlde her veri tetiği önce `ASKIDA_SURE` (2,2–10 s) bekletir, sonra `T_CEZA` uygular. Kapalı kol, karıştırmayla ilgisi olmayan fazladan bir bağ kesintisi öder. Bu, kapının istediği "`PDR_açık` anlamlı düşmeli" sonucunu DESPARETE lehine kolaylaştırır; `06` §0.4.5 kapının yönünü DESPARETE aleyhine tutucu ister. Aynı fark ikizdeki genel katkı beyanına da girer.
- **Öneri:** ASKIDA'nın beklemesi karıştırmaya karşı sınıfa alınsın; `karistirma_durumu` kapalıyken `ASKIDA_SURE = 0`, yani veri tetiği doğrudan KÖTÜ'ye ve cezaya.

#### Y-5 · `uyarlanir_aralik` kapalıyken çekirdek ara ilan `I`'yı `I_MIN`'e indiriyor; katlama ise bayrakta

- **Yer:** `KK-02-SELAM.md:25` (kural 2, bayrak) · `:26` (kural 3, çekirdek: "bir değişim olayında `I ← I_MIN`") · `KK-00-DIZIN.md:67` ("`I` sabit `I_MAX`; ara ilan sürer").
- **Ne yanlış:** Kural 3 bayraktan bağımsız `I ← I_MIN` yapar; `I`'yı yeniden büyüten katlama kural 2'dedir ve bayrak kapalıyken çalışmaz. Harfiyen kodlanırsa kapalı kolda ilk olaydan sonra `I` 0,5 s'de kalır: selam yükü 4 katı, kapalı kolun kontrol payı ölçüsü anlamsızlaşır. "`I` sabit `I_MAX`" cümlesi kurallarla çelişiyor.
- **Öneri:** kural 3'e "bayrak kapalıyken ara ilan hemen gider, `I` değişmez (`I_MAX`)".

#### Y-6 · Kendi "karıştırılıyorum" durumumun üst süresi yok; uzun karıştırmada kaybolan ardıl bırakılmıyor

- **Yer:** `KK-01-BAG.md:64` (kural 13: ölçü donar, silme durur) · `KK-03-KANIT.md:37` (kural 8: MAC yok sayılır, ardıl korunur) · `KK-04-ROTA.md:37` (istek yok).
- **Ne yanlış:** KARIŞTIRILIYOR'a üst süre eklendi (`T_HATIRA`), ama kendi durumuma eklenmedi. Durum sürerken ardıl yalnız ∞ ilanıyla ya da bit = 1'le bırakılabilir. Ölçü donduğu için sessizlik yok, MAC yok sayılıyor, silme durmuş. Ardıl ölür ya da uzaklaşırsa düğüm, karıştırılması bitene kadar sonlu maliyet ilan etmeyi ve ölü ardıla göndermeyi sürdürür; bütün alt ağacı için kara deliktir. Geliştirme ve birincil hücrelerde süre ≤ 15 s olduğu için sınırlı; uzun açık dönemli bir hücrede (`12` Faz 5'in her mekanizmada istediği yer karıştırıcılı aile, Aile 1'in başka sınıfları) karıştırma süresince sürer.
- **Öneri (küçük bir karar):** kendi durumuma üst süre (ör. `T_HATIRA`; dolunca dondurma ve MAC'in yok sayılması biter, ölçü yeniden başlar). Ya da ardıldan `T_SILME` kadar hiçbir çerçeve duyulmazsa ardıl kendi durumum sürerken de bırakılsın. Uzun açık dönemli herhangi bir hücreden önce yazılmalı.

### Küçük

- **Y-7 · ASKIDA'dan KARIŞTIRILIYOR'a geçişte hatıranın kaynağı iki kuralda farklı.** `KK-01:52` "ASKIDA'ya girişteki ölçüden", `:53` "`gecmis` sonundaki ardışık 0'lar atılarak" (o anki `gecmis`). Kararın istediği ilki. Giriş anındaki anlık görüntüde de sondaki sıfırlar olabilir (ED'de alıcı tetikten önce susmuş olabilir); onlar da atılmalı. Öneri: "hatıra = ASKIDA'ya girişteki `gecmis`, sonundaki ardışık 0'lar atılarak, ve o andaki `d_f`".
- **Y-8 · KÖTÜ'den OLAĞAN'a geçişte aynı selamın bit = 1'i işlenmiyor; ∞ ilanın tur alanı tanımsız.**
  - Kural 15'e göre önce kanıt değerlendirilir, bağ o an KÖTÜ olduğu için yok sayılır, sonra ETX eşiği bağı OLAĞAN yapar. Bağ bir selam aralığı (≤ 2,2 s) aday olur. Sürekli karıştırılan bir komşuda bu her `T_HATIRA` (30 s) döngüsünde yinelenir. Öneri: KÖTÜ → OLAĞAN'da selamın biti 1 ise doğrudan KARIŞTIRILIYOR.
  - Rotası olmayan düğümün ∞ selamındaki `tur` alanının değeri yazılı değil (`KK-02:15`, `KK-04:28`). Uygunluğa etkisi yok (∞ her zaman uygulanabilir), ama alan doldurulmak zorunda. Öneri: FD'nin turu.
- **Y-9 · B-6'dan sonra dayanak sayıları kaydı.** Kararlı ağda ilan edilen aralık 2,2 s. `k = 3` için kanıt son selamdan 7,7 s (yazılı 7 s), karıştırmanın başlangıcından 5,5–7,7 s; `d_r` 0,6 için 12,1–14,3 s (yazılı 11–13 s); kural 7'nin `2·a`'sı 4,4 s (`KK-00:36`). Sonuç değişmiyor.
- **Y-10 · `s`'nin `kacan` sayımında geri alma belirsiz.** KK-01 kural 2 geç gelen selamda zaman aşımı sıfırını geri alıyor; KK-03 kural 2'nin ham `kacan` sayımının da geri alıp almadığı yazılı değil (`KK-03:25`). 1,1 katsayısıyla geç selam seyrek; yine de tek cümle.
- **Y-11 · İstek kaydının tazelenmesi ve `ISTEK_ANIMSA`.** Aynı t için 1 s içinde ikinci istek iletilmez; o isteğin kaydı tazeleniyor mu, ikinci isteyen (g₂) kayda giriyor mu, yazılı değil (`KK-04:42`). Yanıt atlama başına en çok ~0,56 s geri döner (`SELAM_ARASI_EN_AZ` + titreşim). Geçide 5 atlamadaki iletici için en kötü durumda ~2,3 s; kayıt (2 s) yanıttan önce silinebilir, yanıt oradan olağan selamla (≤ 2,2 s/atlama) sürer. Öneri: kayıt istek yinelemesinde tazelensin; `ISTEK_ANIMSA` ≥ yineleme süresi + derinlik × 0,56 s olsun (ör. 4 s).
- **Y-12 · `d_r` tanımsız komşu listeden çıkınca karşı tarafta `d_f = 0`; tek örnekli `d_r` 1,0 bildirilir.** `T_HATIRA` dolunca ya da `hatirlanan_kalite` kapalıyken `gecmis` boşalır. Komşu listede görünmez, karşı taraf `d_f = 0` sayar ve kendi OLAĞAN bağını da KÖTÜ'ye alır (`KK-02:18`, `:34`). İlk selamdan sonra tek örnekle `d_r = 1,0` (255) bildirilir; `d_f`'nin örnek sayısı güvencesi yok. Öneri: `d_r` ancak `ORNEK_EN_AZ` örnekten sonra listeye girsin, karşı tarafta yokluk "bilinmiyor" sayılsın (bağ durumunu değiştirmesin).

---

## 3 · Sorunlar (bulgu değil, bilinmeli)

- **Z-1 · ASKIDA yanlış alarmın bedelini artırdı.** İkizde kanıtsız bir veri tetiği eskiden `T_CEZA` (10 s) kesinti veriyordu. Şimdi `ASKIDA_SURE + T_CEZA` (kararlı ağda 8,8 + 10 ≈ 19 s). "İkizde zarar yok" ölçütünü etkiler; Y-1'in ikinci önerisi (ceza ASKIDA'ya girişten) bunu da giderir.
- **Z-2 · B-10'un sonucu: yeni tur istek yolu dışında olağan selamla yayılıyor.** Bu, atlama başına en çok 2,2 s demek. Bir düğüm yeni turu ilan edince FD'si yeni tura geçer; eski turdaki komşuları uygulanamaz kalır. Bu pencere eskisine (0,5 s/atlama) göre genişledi; zincirleme tur artışı riski (`17` §7 madde 10) tanı kaydında izleniyor.
- **Z-3 · B-11'in bedeli.** Karıştırılan gönderici onayları duyamadığı için her çerçeveyi yeniden deneme sınırına kadar gönderir; girişim alanında kanal yükü artar. Kararın bilinen bedeli; kontrol ve veri yayın süresi tanısında görünür.
- **Z-4 · Kenar bağlarda ASKIDA'nın 10 s tavanı sessizliği kaçırıyor.** a = 2,2 s iken `k = 5` için tetik son selamdan ≥ 2,1 s sonra, `k = 6` için ≥ 4,3 s sonra gelmezse sessizlik ASKIDA'dan sonra tamamlanır (`askida.py`). `k ≥ 5`, `d_r ≲ 0,6` demek; kural 15 kenar bağın KÖTÜ'ye düşmesini zaten kabul ediyor.

## 4 · Temiz çıkanlar

- **Döngüsüzlük çekirdeği** artık şartsız: ∞'un uygulanabilirliği ve güncel FD ile hesap yazılı; FD nicemlenmiş ilan edilen değeri tutuyor; istek kaydı uygunluğa girmiyor. İstek iletimi ardıl zinciri üzerinde (döngüsüz), 64 atlama sınırlı, isteyene geri gönderilmiyor.
- **∞ ile zorunlu geçiş:** ∞ yok sayılmıyor, ardıl hemen bırakılıyor, `A` boşsa ∞ hemen ilan ediliyor (ara ilan); kayıp atlama başına ≤ 0,56 s'de yayılıyor. Açlık dalları tam: istek yalnız yeni turun yardım edebileceği durumda.
- **Yeni durum makinesi** (OLAĞAN · ASKIDA · KÖTÜ · KARIŞTIRILIYOR × selam, zaman aşımı, MAC sonucu, KK-03 kanıtı ve bitişi, kendi durumum, zamanlayıcılar, silme): her geçiş tanımlı. Ölü durum yok: ASKIDA süreli, KARIŞTIRILIYOR `T_HATIRA` ile sınırlı, KÖTÜ ölçüyle ya da silmeyle çıkıyor. Tek eksik eşzamanlılık Y-2.
- **Sebep kümesinin bitişi:** iki sebebin "bitti"si aynı olaydır (bit = 0 olan iki ardışık selam), küme her zaman kapanır. j duyuluyorsa iki selamla, duyulmuyorsa `T_SILME` (30 s, girişten önce dolar) ya da `T_HATIRA` ile.
- **ED alıcısının sınıflanması:** `(k+0,5)·a − D < (k+1)·a` olduğu için `(k+1)·a ≤ 10 s` iken sessizlik kanıtı her zaman ASKIDA içinde; ilk raporun en önemli senaryosu (B-2/1) kapandı.
- **İstek kaydıyla geri yayılım:** isteği ileten her düğüm yeni turu ardılından alınca hemen ilan ediyor; yanıt istek yolundan isteyene ulaşıyor (Y-11'deki süre sınırıyla).
- **Bayrak tablosunun öteki satırları tutarlı:** `alici_bildirimi` (alan kalır, bit 0, olay değil; sessizlik bitişi bit = 0 istediği için tutarlı) · `hatirlanan_kalite` (boş `gecmis` → KÖTÜ, kural 10 ile tutarlı; yan etkisi Y-12) · `istege_bagli_esik` · `bekletme` · çekirdek satırları.
- **Kapanış belgesindeki kayıtlar:** B-1, B-3…B-12, B-14…B-20 metinde bulundu; `v2/17` T-2, T-9, T-13 eklemeleri kâğıtlarla uyumlu.

## 5 · Doğrulanamayanlar

- Girişim alıcısında saniyelik işaret olasılığı p, dolayısıyla q (Y-1). Tablolar duyarlılık olarak verildi.
- Y-2'nin sıklığı: gönderici girişimdeyken çerçeve başına deneme ve vazgeçme ölçülmedi.
- Uzun açık dönemli hücrenin (yer karıştırıcılı aile) çizelgesi (Y-6'nın etkisi).

## 6 · Hüküm

**Kodlamaya geçmeye engel yok.** İlk raporun üç engelleyici bulgusu kapandı: B-1 tam; B-3 tam; B-2 ED alıcısında tam, girişim alıcısında değere bağlı. Önemli bulguların hepsi kapandı ya da kısmen kapandı. Düzeltmelerin getirdiği yeni bulgular döngü, ölü durum ya da geliştirme hücrelerinde kalıcı kara delik üretmiyor. Hepsi birkaç cümlelik yerel kural ekleri ya da değer seçimi; durum makinesinin yapısını değiştirmiyor.

Kodlamayla birlikte kapatılacaklar:

- **Önemli** (zamanlamasıyla):
  - Y-3 ve Y-2: KK-03 ve KK-01 kodlanırken. Kaynağın ED'de kalması; ASKIDA iken kendi durumum başlarsa OLAĞAN'a dönüş.
  - Y-1 ve Y-4: `veri_kotu_tetigi` ile `karistirma_durumu` A/B'lerinin ve mekanizma kapısının beklentisi yazılmadan önce. ASKIDA'nın alt sınırı ve geç kanıtın cezası; ASKIDA beklemesinin sınıfı ve kapalıyken sıfır olması.
  - Y-5: `uyarlanir_aralik` A/B'sinden önce.
  - Y-6: uzun açık dönemli herhangi bir hücreden (yer karıştırıcılı aile dâhil) önce. Kendi durumuma üst süre (küçük bir karar).
- **Küçük, kodla birlikte:** Y-7 (hatıranın kaynağı) · Y-8 (KÖTÜ → OLAĞAN'da bit; ∞'un tur alanı) · Y-9 (dayanak sayıları) · Y-10 (`kacan`'da geri alma) · Y-11 (istek kaydının tazelenmesi, `ISTEK_ANIMSA`) · Y-12 (`d_r`'nin listeye girişi).
- **Sorunlar:** Z-1…Z-4 tanı kaydında izlenir; Z-1, Y-1'in ikinci önerisiyle birlikte giderilebilir.
