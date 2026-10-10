# 08 · EVRE METRİKLERİ — dört metrik, sıfır serbest parametre

> **Durum: uygulandı** (onay 8 Eylül · kapılar K-105 · tek α K-123). Güncel 10 Ekim 2026 (öz sürüm; ayrıntılı tarihçe ve eski ölçüm planı `v2/arsiv/08-EVRE-METRIKLERI-2026-09-25.md`). Bölüm numaraları kodda atıflı, korunur. Kod `sim2/olcum/evre.py` · kapılar `python -u kalibrasyon/evre_metrikleri_kapilari.py` · tek α kapısı `python -u kalibrasyon/anlamlilik_sabitleri.py`.
> Açık (10 Eylül): `T_j` parametre kalır; ısınma ve ölçüm penceresi birlikte taranır (`06` §8 koşul 1). **Çizelgeli karıştırıcı §08'de (K-209, onay K-207)**; çoklu/hareketli sürekli karıştırıcıda tek basamaklı tanım geçerli. M4'ün boş kol kapısı gerçek protokollerle geçti (G1-P, K-196).

---

## 00 · Neden

Şartname §08.2 toparlanmayı "temiz değerin %X'i" diye tanımlıyor; %X, "kararlı hâl", "en dip nokta" hiçbir sayıya bağlı değil. Sonuç görüldükten sonra seçilirse metrik hoşa giden cevabı ölçer. Dört metrik **sıfır serbest parametreyle**, sonucu görmeden tanımlanır.

## 01 · İlk tasarımdaki hata

Şok penceresi `[T_j; T_j+3)` idi, gerekçe AODV `ACTIVE_ROUTE_TIMEOUT` (3 s). Yanlıştı: o bir kullanılmama zaman aşımıdır, bağ arızası tespiti değil — reaktif protokol MAC denemeleri bitince **milisaniyede** RERR üretir. "Hiçbir protokolün tepki veremeyeceği pencere" yoktur → şok derinliği ile toparlanma hızı bir pencereyle ayrılamaz; doğru yol neyin ölçüldüğünü açıkça söylemektir (M1). 3 s artık hiçbir yerde kullanılmıyor.

## 02 · Kafes — iki sabit, ikisi RFC'den

| ne | değer | kaynak | işi |
|---|---|---|---|
| ızgara adımı `S` | **1 s** | RFC 3561 `HELLO_INTERVAL` | çözünürlük: hiçbir taban protokol komşu bilgisini daha hızlı tazelemez |
| pencere `L` | **15 s** | RFC 3626 `TOP_HOLD_TIME` | durağanlık: "kararlı" denebilecek en kısa süre |

Çözünürlük en hızlı taban protokolden, durağanlık en yavaştan (§06/1). Kafes `beacon_araligi_s`e değil RFC'ye çıpalı (ikisi bugün 1 s; ayrışırlarsa kafes yerinde kalır).

## 03 · Zemin ve evreler (referans dünya, birincil hücre)

Ölçüm penceresi `[50; 320)` s · `T_j = 150` s (`karistirici_baslangic_s`) · 40 pkt/s (yere toplama: 39 × 1 pkt/s telemetri + 4 × 0,25 pkt/s komut; eski dünyanın 10 akış × 4 pkt/s'iyle aynı yük) · gecikme p99 0,28–4,7 s (G4ç, K-212). Çizelgeli karıştırıcıda ŞOK ve TOPARLANMA'nın yerini açık/sessiz dönemler alır (§08).

| evre | aralık | paket/tohum | kol SE (30 tohum, Wald, p ≈ 0,6) |
|---|---|---|---|
| TEMİZ | `[50; T_j)` | 4 000 | 0,0014 |
| ŞOK | `[T_j; T_j+15)` | 600 | 0,0037 |
| TOPARLANMA | `[T_j+15; 320)` | 6 200 | 0,0012 |

Bölümleme boşluksuz (ilk tasarımdaki "GEÇİŞ" boşluğu 3 s penceresiyle gitti). PDR paketin **doğum** anına göre kovalanır (`pdr_pencere` ile aynı); evre sınırı gecikme kadar bulanıklaşır ve bu protokole bağlıdır (rota bekleyen paket) — G4 her kolda ölçer.

## 04 · Dört metrik (tohum başına; sayımlar havuzlanır)

**M1 · şok derinliği** `= PDR(TEMİZ) − PDR(ŞOK)`; `PDR(TEMİZ)` tanımsızsa `None`; SE M3'ünkiyle aynı (K-196). Darbenin sertliğini ve ilk 15 s'deki toparlanmayı **birlikte** ölçer (hızlı toparlanan protokolün çukuru gerçekten sığdır — artefakt değil üstünlük); M3 ile birlikte okunur. "En dip nokta" aşağı yanlı bir kestiricidir (pencere sayısıyla düşer) → yalnız `teshis`te, pencere sayısıyla.

**M2 · toparlanma tamlığı** `= PDR(TOPARLANMA) / PDR(TEMİZ)`; `> 1` kırpılmaz (kırpmak bozuk ölçümü gizlerdi), `PDR(TEMİZ) = 0` ise `None`.

**M3 · toparlanma süresi**

```
ızgara  t ∈ {T_j, T_j+1, …},  t + L ≤ ölçüm sonu
T_kur = en küçük t:  p̂([t; t+L)) ≥ p̂(TEMİZ) − z(1−α/2)·SE
SE = max( Agresti–Caffo (§05.1) ,  s_L·√(1 + L/T) )              (K-196, §05.4)
s_L = TEMİZ içindeki kayan L pencerelerinin PDR'lerinin örneklem SD'si
toparlanma_suresi = T_kur − T_j      yoksa SANSÜRLÜ = None
```

%X yok: band koşunun kendi sayımlarından. Sansür asla sayıya çevrilmez (yoksa hiç toparlanmayan protokol pencere uzunluğu kadar iyi görünürdü); kol başına sansür oranı raporlanır. Beyanlı sınır: gürültülü kolda band genişler; ilk başarılı pencereyi aldığı için "erken toparlandı" yanlılığı olabilir. `SE` metrikle birlikte raporlanır.

**M4 · tespit gecikmesi**

```
m̂, v̂ = TEMİZ evrenin 1 s kovalarındaki kopma BEYANI sayısının ortalaması ve varyansı (n − 1)
boş dağılım = negatif binom(m̂, v̂); v̂ ≤ m̂ ise Poisson(m̂)          (K-196, §05.4)
T_tespit = en küçük t > T_j:  [t−1; t) beyanı > boş dağılımın üst kuyruğu, pencere başına α / taranan pencere (Bonferroni, §05.3)
tespit_gecikmesi = T_tespit − T_j    yoksa SANSÜRLÜ = None
```

Var olan beyan kanalını kullanır (gözlem penceresi genişlemez). Boş hipotez aynı koşunun TEMİZ evresinden — "açılmadan sonraki ilk beyan" karıştırıcıyla ilgisiz kopmaları (sönümleme, hareket) ölçerdi. `beyan_etmiyor` → `None` (susan protokol hızlı görünemez).

## 05 · Kapılar — metrik kullanılmadan önce

| kapı | ölçüt | sonuç |
|---|---|---|
| G1 boş kol | kol ortalaması `sok_derinligi` 0'dan 2 SE içinde · her tohumda `toparlanma_suresi` = 0 · `tespit_gecikmesi` SANSÜRLÜ | ✓ −0,00125 · 2 SE 0,00204. Kâhinle (beyan etmez → tespit maddesi G1-P'de) |
| G1-P boş kol, gerçek protokoller (K-196) | referans dünya `statik-yok` yere toplama, AODV · OLSR · AOMDV · DESPARETE × 2 tohum: M4 yanlış tespit ≤ 1/8 · M3 ≠ 0 ≤ 1/8 · M1 2 SE dışında ≤ 1/4 protokol | ✓ 0/8 · 0/8 · 0/4 (aynı koşularda K-196 öncesi kural 6/8 · 3/8 · 2/4) — `arsiv/teshis/evre_g1p_2026-09-28/` |
| G2 tekdüzelik | şiddet arttıkça hiçbir düşüş iki noktanın birleşik 2 SE'sini aşmaz | ✓ |
| G3 ızgara fazı | yarım adım kaydırmada hiçbir karar hata payından fazla değişmez (8 Eylül ρ örnekleme dersinden) | ✓ eski dünyada en büyük fark 0,00187, band 0,00991. Referansta eski çekirdek hücre tabanda (M1 ≈ 1, SE çöküyor) → yerini **G3ç** aldı: birincil hücre, kâhin, 1003 · 1004, \|ΔM1\| 0,0028 · 0,0053 ≤ 2 SE ✓ (`… 3c`, K-219) |
| G4 bulanıklık | `gecikme_p99 / S < 1` (aşarsa atfetme kuralı yeniden yazılır) | ✓ 0,021 temiz · 0,029 karıştırılmış |

**05.1 · G1 ilk koşuda kaldı — kusur hata payındaydı.** Wald `SE² = p(1−p)/n`, `p = 1`'de sıfır; karıştırıcısız kolda kâhin PDR'si 1,000 olduğundan band en çok gereken yerde çöküyordu (M3'ün bandını da bozuyordu). Düzeltme **Agresti–Caffo** (iki oranın farkı için standart: her örneğe bir başarı ve bir başarısızlık; serbest parametre yok, band biraz geniş) ve verdikt **kol ortalamasında** (tohum başına 2 SE testi üç tohumda ~%14 rastgele reddeder).

**05.2 · G2'nin "kesin monoton artış"ı sınanamazdı** — gerçek değeri eşit iki noktada gürültü %50 düşüş gösterir; düzeltilen tanım, eşik değil. Ölçüm (kâhin, 3 tohum, şok derinliği ± SE): −30 dBm −0,00069 ± 0,00069 · −21 −0,00125 ± 0,00042 · **−15 +0,03707 ± 0,00618** · −9 +0,18742 ± 0,01540. Yan bulgu: çalışma noktasında mükemmel yönlendirmeyle şok derinliği yalnız 0,037 — ayırt edici güç protokolün körlüğünden gelmek zorunda (K-103).

**05.3 · Tek α** (`06` §7, K-123): modülde yalnız `ALFA = 0,05`; M3'ün z'si (1,95996) ve M4'ün eşiği ondan türer. Eski iki sabit (M3 2,0 SE · M4 pencere başına 0,01) gerekçesizdi ve M4 ~170 pencereyi taradığı için aile düzeyi yanlış alarm çok büyüktü. Sentetik boş hipotez (homojen Poisson beyan, 4 000 deneme/hücre, ± 2 SE):

| beyan hızı (1/s) | eski kural | bugünkü (0,05 / ~170) |
|---|---|---|
| 0,1 | 0,514 ± 0,016 | 0,022 ± 0,005 |
| 0,5 | 0,374 ± 0,015 | 0,024 ± 0,005 |
| 2,0 | 0,578 ± 0,016 | 0,034 ± 0,006 |
| 10,0 | 0,696 ± 0,015 | 0,030 ± 0,005 |

Kapı: bugünkü kural `ALFA`yı aşarsa çıkış 1.

**05.4 · Hata payı kümelenmeye dayanıklı (K-196).** G1 kâhinle geçmişti — kâhinde kayıplar bağımsız. Gerçek protokolde kayıp ve kopma beyanı zamanda KÜMELENİYOR: karıştırıcısız kolda OLSR 3/3 tohumda "tespit" etti (K-193); G1-P'de eski kural 8 koşunun 6'sında. Düzeltme serbest parametre getirmez, iki moment koşunun kendi temiz evresinden: M1 ve M3'ün SE'si `max(AC, s_L·√(1 + L/T))`, M4'ün boş dağılımı 1 s kova sayımlarının ortalaması ve varyansıyla negatif binom (varyans ≤ ortalama ise Poisson — bağımsız kolda eşik birebir aynı). Ölçülen kümelenme: temel protokollerde küme SE / AC 1,4–2,4 (OLSR **6–7**), kova beyanı var/ort 3,4–7; DESPARETE'de 1,2–2,2 ve 1,3. **Bedeli:** OLSR'da tohum başına M1'in 2 SE'si 0,22–0,26 (tek tohumda bilgisiz; kol düzeyinde 40 tohumla ~0,04) · temel protokollerde M4 eşiği saniyede ~50'den ~80–100 beyana çıkar, karıştırma daha geç tespit edilir. Ana deneyin H2 testi (tohum düzeyinde PDR) etkilenmez.

## 06 · İki soru — karara bağlandı

1. **İki çapa kalır.** Her şey 1 s olsa test penceresi 40 pakete iner (tohum SE ≈ 0,08, geçici sıçrama toparlanma sanılır); her şey 15 s olsa 155 s'lik toparlanma evresinde yalnız 10 ayırt edilebilir süre kalır ve 15 s'den az ayrışan protokoller aynı görünür — oysa şartname toparlanma süresini asıl ayırt edici sayıyor.
2. **Pencere 15 s, şok derinliği kol düzeyinde okunur.** Tohum başına 600 paket, SE ≈ 0,020; 30 tohumluk kolda ≈ 0,0037. Yük ya da tohum artırmak çalışma noktasını değiştirirdi. Tohum başına şok derinliği tek başına okunmaz; SE her koşuda metrikle raporlanır.

## 07 · Uygulama

Dördü de **son işlemdir**: paket defteri doğum/teslim anını, rota defteri beyanları zaten tutuyor. Sıcak yola sayaç eklenmez — eklenseydi ölçümün maliyeti sonuca karışırdı.

## 08 · Çizelgeli karıştırıcı (K-209 · onay K-207)

Birincil hücrenin karıştırıcısı (`derin_sizma`) `T_j`'den sonra 15 s açık · 15 s sessiz. Tek basamaklı tanımda TOPARLANMA açık ve sessiz dönemleri karıştırır. Eldeki veride (K-200 partisi) M3 0–45 s arasında anlamsız çıktı; M4'ün bütün tespitleri 2. ya da 3. açık dönemdeydi, yani "32 s" aslında "ilk açılmayı kaçırdı" demekti. Çizelge sonuç satırında `evre_cizelge_s`; karıştırıcının kendi `devrede_mi`siyle aynı olduğu test edilir.

| metrik | çizelgeli karıştırıcıda |
|---|---|
| **M1** | aynı; ŞOK `[T_j; T_j + min(L, açık))` = ilk açık dönem (temiz durumdan) |
| **M2** | `PDR(bütün sessiz dönemler) / PDR(TEMİZ)`, kırpılmaz |
| **M3** | **tanımsız**: `None`, `toparlanma_suresi_tanimsiz = "cizelgeli"`. Sessiz dönem `L`den uzun değil; yerine metrik uydurulmaz |
| **M4** | tarama ilk açık dönemle sınırlı; Bonferroni sayısı taranan pencereden (15) |

Sürekli karıştırıcıda dördü ve satır birebir kalır. **Betimleyici teşhis** (karar kuralı yok, iddia taşımaz):
- çevrim başına açık/sessiz PDR (`evre_cevrim_pdr`)
- katlanmış 1 s profili (`evre_katli_profil`; özdeş çevrim varsayımı beyanlı, çünkü karıştırıcı her sessizde 250 m taşınır)
- evre sızıntısı (`evre_sizinti`: teslim edilenlerden doğduğu evreden başka evrede teslim edilenlerin oranı)

**Kapılar (ölçmeden önce):**
- **G1ç** · birincil hücrenin hareketliliğinde karıştırıcısız kol, hayalet çizelgeyle; AODV · OLSR · AOMDV · DESPARETE × 2 tohum. G1-P kuralları aynen, artı `D = PDR(sessiz) − PDR(TEMİZ)` iki tohumda 2 SE dışında kalan protokol yok. Kalan protokolün M2'si "yorumlanamaz (ÖNCE referansı durağan değil)" diye yazılır.
- **G2ç** · kâhinde M1 kol ortalamasında 2 SE dışında ve D, kâhinin AYNI tohumdaki karıştırıcısız (hayalet çizelgeli) koşusunun D'sine göre 2 SE içinde (SE iki koşununkinin karelerinin toplamının kökü). İlk tanımla (D 0'a göre) 2 Ekim'de kalmıştı (K-212); sebep 6 örnekli kâhinin yakınsamamasıydı, formasyonun topolojisi değil (K-217). Eşleştirme tutucu olarak kaldı (K-215). **Durum (K-224, 7 denemeyle): G1ç ✓ · G2ç ✓ · G3ç ✓ · G4ç ✓** — yakınsamış kâhinle D eşleştirmesiz de 2 SE içinde.
- **G4ç** · `p99 < açık süre` (`bulaniklik_orani_evre < 1`); 1 s profili `p99 ≥ 1 s` ise "bulanık" etiketiyle çizilir.

Öneri ve v1'in neden geri çekildiği: `arsiv/teshis/faz4_kapanis_2026-09-30/evre_cizelgeli_oneri*.md`.
