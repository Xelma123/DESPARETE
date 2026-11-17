# Faz 5-3 kural kâğıtları — bağımsız denetim raporu (17 Kasım 2026)

## 0 · Başlık bilgisi

- **Denetlenen hâl:** `main` @ `94c0ed6fefe4e3d2ee7cd60e643ec1adad1403c7` ("Faz 5-3 kural kâğıtlarının üçüncü denetimi …").
- **Başlangıç durumu:** `git rev-parse HEAD` → `94c0ed6fefe4e3d2ee7cd60e643ec1adad1403c7`; `git status --short` → `?? arsiv/denetim/DENETIM-PROMPT-KURAL-2026-11-17.md`.
- **Son durum:** `git rev-parse HEAD` → `94c0ed6fefe4e3d2ee7cd60e643ec1adad1403c7`; `git status --short` → `?? arsiv/denetim/DENETIM-PROMPT-KURAL-2026-11-17.md` · `?? arsiv/denetim/DENETIM-RAPORU-KURAL-2026-11-17.md` (yalnız bu rapor eklendi).
- **Denetim konusu:** `v2/kural/KK-00-DIZIN.md` … `KK-05-BEKLETME-KOMUT.md`.
- **Okunan belgeler:** `v2/17-TASARIM-KARARLARI.md` (kimlik, ilkeler, T-1…T-20, §7) · `v2/05-GOZLEM-PENCERESI.md` · `v2/13-KONTROL-DUZLEMI.md` · `v2/12-YOL-HARITASI.md` (Faz 5) · `v2/04-KARARLAR.md` (K-222, K-247 satırları) · `v2/06-ON-KAYIT.md` §0.4.5 · `arsiv/teshis/faz5_2_isaretler_2026-11-16/sonuc.md` · `beklenti.md` (tanımlar) · yan oturumun 5-2 denetim notu.
- **Okunan kod:** `sim2/gozlem/pencere.py` · `karar.py` · `protokol.py` · `kontrol.py` · `sim2/kosum/kontrol.py` · `sim2/kosum/dugum.py` (tampon, `mesgul_guncelle`) · `sim2/kosum/kosu.py` (kanca sırası) · `sim2/kosum/kayip.py` (geçidin kaybı) · `sim2/yapilandirma/konfig.py` · `kokenler.py` (yeniden deneme sınırı) · `protokoller/babel.py` · `babel_bicim.py` · `protokoller/desparete.py` (geçit kimliğinin geçişi) · `kalibrasyon/karistirma_isaretleri.py` (teşhis (d) kaydedicisinin selam kaybı tanımı).
- **Kaynaklar:** `protokol_kaynaklari/rfc8966_babel.txt` (§3.5.1, §3.5.3, §3.6, §3.7.2, §3.7.3, §3.8.1.2, §3.8.2.1, §3.8.2.2, §4.6.5) · `protokol_kaynaklari/faz5_arastirma_2026-10-21/rfc6719_mrhof.txt` · `rfc6206_trickle.txt`.
- **Yöntem:** okuma, kaynakla karşılaştırma, durum makinesi vaka çözümlemesi; zaman çizelgeleri depo dışında iki küçük betikle adım adım yürütüldü (`zaman_cizelgesi.py`, `ceza_yarisi.py`; simülasyon değil, simülatör çağrılmadı, tohum kullanılmadı). Betiklerin varsayımları ilgili bulguda yazılıdır.
- **Hüküm özeti:** kâğıtlar bu hâliyle kodlamaya hazır değil. Üç engelleyici bulgu var: geri çekme (∞) uygulanabilir sayılmıyor ve kara delik üretiyor; veri tetiği karıştırma durumunu baypas ediyor; KARIŞTIRILIYOR durumunun çıkışı olmayan bir giriş yolu var. Düzeltmelerin tamamı belge düzeyindedir (§5).

---

## 1 · Bulgular

Ağırlık sırasıyla. "Engelleyici": kod yazılmadan düzelmeli · "önemli": kodlamadan önce karar ya da açık kural gerekir · "küçük": kodla birlikte düzeltilebilir.

### B-1 · Geri çekme (∞) uygulanabilir sayılmıyor; seçili ardılın ∞ ilanı 5 s yok sayılıyor ve bu her atlamada yineleniyor — **engelleyici**

- **Yer:** `v2/kural/KK-04-ROTA.md:19` (kural 1) · `:25` (kural 7) · `:20` (kural 2) · `:24` (kural 6).
- **Ne yanlış:** Kural 1'in koşulu (`tur_j > FD.tur` ya da `tur_j = FD.tur ve C_j < FD.maliyet`) ∞ ilanı için yanlış verir: 0xFFFF hiçbir sonlu FD'den küçük değildir ve rotası olmayan düğüm "daha yeni bir tur ilan etmez" (kural 6). Kural 7 seçili ardıldan gelen uygulanamaz ilanı 5 s yok sayar ve ardılı "son kabul edilen `C_j` ile" tutar. İkisi birlikte, ardılın rotasını kaybettiğini bildiren ilanı 5 s yok saydırır.
- **Kaynak:** RFC 8966 §3.5.1 geri çekmeyi her zaman uygulanabilir sayar ("retractions … are always feasible, since they cannot possibly cause a routing loop"); `protokoller/babel.py` `_uygulanabilir` `m >= SONSUZ` için `True` döndürür.
- **Senaryo:** geçit ← X ← Y ← Z zinciri. X'in `A`'sı boşalır, `C_X = ∞` olur ve X bunu hemen ilan eder (KK-02 kural 3, "∞ ↔ sonlu"). Y için bu ilan uygulanamazdır → kural 7: yok sayılır, Y sonlu maliyet ilan etmeyi ve paketleri X'e göndermeyi sürdürür, X'e tek alıcılı tur isteği gider. X yanıtlayamaz (maliyeti sonlu değil) ve iletemez (kural 9 bir ardıl varsayar; X'in ardılı yok). 5 s sonra Y ilanı uygular, ∞ olur; Z aynı kuralla 5 s daha yok sayar. Derinliği `d` olan alt ağaçta rota kaybı `≈ 5·d` s'de yayılır; bu sürede paketler X'e gider, X'te en çok 2 s bekletilip düşer (KK-05 kural 2). Her rota kaybında yinelenen, süreli ama sistematik bir kara deliktir.
- **Öneri:** kural 1'e "∞ ilan her zaman uygulanabilirdir (RFC 8966 §3.5.1)"; kural 2'ye "ilanı sonlu"; kural 7'nin yok sayması yalnız **sonlu** uygulanamaz ilan için; seçili ardıldan ∞ gelince ardıl hemen bırakılır (kural 4).

### B-2 · Veri tetiği karıştırmayı "kötü bağ" sınıfına sokuyor; KÖTÜ yapışkan ve ceza katlanıyor — **engelleyici**

- **Yer:** `KK-01-BAG.md:32–33` (kural 5) · `:46` (kural 8) · `:38` (geçiş tablosu) · `KK-03-KANIT.md:26–27` (kural 6–7) · `KK-00-DIZIN.md:26` (`T_CEZA`).
- **Ne yanlış:** Kural 5 kendi amacını ("karıştırma kötü bağ sanılmaz") en önemli durumda karşılamıyor. `ETX_veri > E_CIK` olunca bağ yalnız j'nin biti ya da benim girişim işaretim varsa KARIŞTIRILIYOR olur, yoksa KÖTÜ olur; KÖTÜ bağda karıştırma kanıtı izlenmez (kural 8) ve `T_CEZA` 60 s içinde yinelenirse katlanır.
- **Kanıt:**
  1. *ED alıcısı biti hiç gönderemez.* ED'deki j selam kurmaz (KK-02 kural 4a; T-6). Gönderici çoğunlukla girişim alanında değildir. Kural 5'in KARIŞTIRILIYOR dalı bu bağ için ulaşılamaz; bağ KÖTÜ olur.
  2. *Zamanlama* (teşhis (d) §3, çerçeve başına ortalamalar, Babel-a trafiği): temiz 1,98 deneme · %1,76 vazgeçme; alıcısı ED'de 6,34 · %15,8; girişimde 3,93 · %11,0. Karıştırmadan önce pencerede `ETX_veri ≈ 2,0`. Pencere 4'ü ED'de karıştırmadaki 4. çerçevede, girişimde 7. çerçevede aşıyor: bağdaki trafik 5 · 2 · 1 paket/s iken ED'de 0,8 · 2,0 · 4,0 s, girişimde 1,4 · 3,5 · 7,0 s. Rakip kanıtlar daha geç: alıcının biti, `s`'nin 4 s'lik pencerede 0,44'ten 0,69'a çıkarken 0,6'yı ~2,6 s'de geçmesi ve iki ardışık işaretli saniye ile gönderende ~4,1 s'de; sessizlik (kural 6, `k = 3`, `a = 2 s`) 5–7 s; kural 7, 2a = 4 s sessizlik ve üç **ardışık** vazgeçme ister (ED'de `r_3` çerçeve başına %5).
  3. *Aynı olayda sıra:* simülatör `iletim_sonucu`yu `iletim_basarisiz`dan önce çağırır (`sim2/kosum/kosu.py:215–216`; `sim2/gozlem/protokol.py` belge dizgisi). Üçüncü ardışık vazgeçmede `ETX_veri` 4'ü geçerse bağ, kural 7 değerlendirilmeden KÖTÜ olur.
  4. *Yapışkanlık ve katlanma:* sonradan gelen bit (~4 s) KÖTÜ bağı değiştirmez. 15/15 ve 10/20 çizelgelerinde her açık dönem bir öncekinin 60 s içindedir; ceza 10 → 20 → 40 s olur. Depo dışı model (`ceza_yarisi.py`; varsayımlar: girişim alıcısı, bit 4,1 s'de, veri tetiği bir dönemde p olasılıkla bitten önce, ceza bitince karıştırma sürüyorsa bit sayesinde KARIŞTIRILIYOR, bitiş karıştırıcı sustuktan 4,5 s sonra; 200 tekrar × 600 s): bağın **sessiz evrede** kullanılamaz kaldığı pay

     | çizelge | p = 0 | 0,25 | 0,5 | 0,75 | 1 |
     |---|---|---|---|---|---|
     | 15 s açık · 15 s sessiz | 0,30 | 0,32 | 0,38 | 0,46 | 0,54 |
     | 10 s açık · 20 s sessiz | 0,22 | 0,23 | 0,30 | 0,39 | 0,47 |

     p = 0 satırı tasarımın kabul ettiği çıkış gecikmesidir (T-10). Veri tetiği her dönem kazanırsa kayıp ikiye yaklaşır; KÖTÜ yolunda hatıra da yoktur. İlke 3'e ("kanıt kalkınca geri alır") ve T-7'ye ters.
  5. *Bayat veri penceresi:* KARIŞTIRILIYOR'a girişte `veri` penceresi boşaltılmıyor. Dönüş, tespit öncesindeki başarısız çerçevelerden 10 s içinde olursa (10 s'lik açık dönemde ED sebebiyle bitti, karıştırıcı sustuktan ~2 s sonra gelir) bayat `ETX_veri` bağı dönüşte KÖTÜ'ye ve cezaya düşürür.
- **Öneri (karar gerektirir):** örnek seçenekler: (a) veri tetiği ateşlenince bağ hemen `A`'dan çıkar ama sınıflama `2a` boyunca ertelenir; bu sürede KK-03 kanıtı (bit, sessizlik, kendi işaret) gelirse KARIŞTIRILIYOR (hatıra tetik öncesi `gecmis`ten), gelmezse KÖTÜ; (b) KÖTÜ (veri) iken KK-03 kanıtı gelirse KARIŞTIRILIYOR'a geçilir, ceza sayacı sıfırlanır; (c) `T_CEZA` katlanması yalnız karıştırma kanıtı olmayan art arda düşüşlerde. Her durumda KARIŞTIRILIYOR'a girişte `veri` penceresi boşaltılır (sondaki sıfırların atılmasıyla aynı mantık).

### B-3 · KARIŞTIRILIYOR'dan çıkışı olmayan giriş yolu; durumun üst süresi yok — **engelleyici**

- **Yer:** `KK-03-KANIT.md:34–35` (tablo: "MAC + kendi girişim işaretim" ve "veri tetiği … kendi durumum") · `:27` (kural 7) · `KK-01-BAG.md:32` (kural 5) · `:41` (çıkış satırı).
- **Ne yanlış:** Giriş koşulu **işarettir** (kural 3'ün saniyelik işareti), çıkış koşulu **durumun** "bitti"sidir (kural 4). Durum iki ardışık işaretli saniye ister. İşaret tek saniye sürüp durum hiç kurulmazsa "bitti" olayı hiç gelmez. KARIŞTIRILIYOR'un zaman aşımı yoktur (`T_HATIRA` yalnız bitti anında okunur), j duyulduğu için `T_SILME` da işlemez. Bağ kalıcı olarak kullanılmaz; İlke 2'ye ("kopan yerlerini kendiliğinden onarır") aykırı.
- **Kanıt:** tek işaretin ikizdeki yanlış alarmı %50 yakalamada %6–11 (teşhis (d) §7); birleşik işaretinki ölçülmedi, ama sıfır değil. Aynı saniyede bir bağda `ETX_veri > 4` ya da üç ardışık vazgeçme olması yeter. Sıklık doğrulanamadı (DESPARETE trafiği yok); sonuç kalıcı olduğu için seyrek olması yetmez.
- **Öneri:** "kendi" sebebinin bittisi seviye koşulu olsun: "kendi durumum karıştırılıyorum değil ve son `CIKIS_SANIYE` saniye işaretsiz". Ya da kural 5 ve 7'de işaret yerine durum aransın. Ayrıca KARIŞTIRILIYOR'a bir güvenlik üst süresi (ör. `T_HATIRA` dolunca `gecmis` boşaltılır, bağ KÖTÜ'den yeniden ölçülür).

### B-4 · Aynı olayda iki geçiş: öncelik kuralı yok — **önemli**

- **Yer:** `KK-01-BAG.md:36–42` (tablo) · `:32–33` · `KK-03-KANIT.md:26`.
- **Ne yanlış ve kanıt:**
  1. Bir zaman aşımı sıfırı hem `ETX_selam`'ı yükseltir hem de `k` ardışık sıfırı tamamlayabilir. En kötü durumda (düşen en eski örnek 1): `d_r = 10/16`, `d_f = 0,7` → ETX 2,29, `k = 5`; `ETX_selam` 5. sıfırda 4'ü aşar → OLAĞAN→KÖTÜ ve OLAĞAN→KARIŞTIRILIYOR **aynı olayda** doğrudur. `d_r = 0,5`, `d_f = 0,6` için KÖTÜ 2. sıfırda, sessizlik 7.'de: kenar bağlar hatırasız KÖTÜ'ye düşer. Bu tasarım sonucu kabul edilebilir ama yazılmamış.
  2. Veri tetiği ile kural 7 aynı vazgeçmede (B-2/3).
  3. Tablo satırı "OLAĞAN → KÖTÜ: `ETX_veri > E_CIK`" kural 5'in KARIŞTIRILIYOR dalını içermiyor; iki yer çelişiyor.
  4. Sebep tek değerli. "Kendi" sebebiyle KARIŞTIRILIYOR iken j'nin biti 1 gelirse bağ benim çıkışımda döner, j'nin bir sonraki selamıyla yeniden girer (bir gidip gelme).
- **Öneri:** aynı olayda değerlendirme sırası yazılsın (ör. önce KK-03 kanıtı, sonra KÖTÜ eşikleri; `k` sıfır varsa KÖTÜ denetimi sondaki sıfırlar atılarak yapılır). Tablo kural 5'le eşlensin. Sebep küme olsun (hepsi kalkınca bitti) ya da "son kanıt sebebi değiştirir" yazılsın.

### B-5 · Kendi dondurmamdan çıkışta sıra boşluğu: kural iki okumaya açık — **önemli**

- **Yer:** `KK-01-BAG.md:27` (kural 1: "dondurmadan çıkıştan sonraki ilk selamda bu kural uygulanmaz") · `:45` (kural 9).
- **Ne yanlış:** "Bu kural" yalnız sıfırlama alt kuralını mı (boşluk > N), yoksa boşluk kadar 0 eklemeyi de mi kapsıyor, belirsiz. Kural 9 yalnız `son_selam_t`'yi çeker (zaman aşımı), sıra boşluğunu değil.
- **Senaryo:** kendi ED'mde 15 s hiçbir çerçeve çözülmez, hiçbir komşunun `beklenen`i ilerlemez. Komşular bu sürede 7–30 selam gönderir (2 s; olaydan sonra 0,5 s). Çıkıştan sonraki ilk selamda boşluk o kadardır. Dar okumada boşluk kadar 0 (en çok 16) eklenir: `d_r ≈ 1/16`, bütün bağlar KÖTÜ, selamımdaki oranlar çöker. Kural 9'un "Sebep"inin önlemek istediği zarar tam olarak budur.
- **Öneri:** "Dondurmadan (kural 7 ve 9) çıkıştan sonraki ilk selamda boşluk için 0 eklenmez ve sıfırlama yapılmaz; `beklenen ← sira + 1`."

### B-6 · Selamın `aralik` alanının anlamı tanımsız; Trickle ikiye katlamasıyla sahte zaman aşımı — **önemli**

- **Yer:** `KK-02-SELAM.md:14` (`aralik`: "o anki aralık") · `:25` (kural 2) · `KK-01-BAG.md:28` (kural 2).
- **Ne yanlış:** Aralık her olaysız selamdan sonra ikiye katlanır. Selam katlamadan önceki `I`'yı taşırsa bir sonraki selam `2I`'da (+%10 titreşim) gelir, alıcının ilk zaman aşımı ise `1,5·a = 1,5I`'dadır. Her katlamada bir sahte 0 eklenir, selam gelince geri alınır. Bir olaydan sonra 0,5 → 1 → 2 dizisi komşu başına iki sahte sıfır üretir. KK-03'ün `s`'si (4 s pencere) bunları selam gelene kadar kayıp sayar; kural 6'nın sondaki sıfır sayımı geçici olarak +1 olur.
- **Kaynak:** RFC 8966 §4.6.5'te Interval, gönderenin bir sonraki planlı Hello'yu göndereceği sürenin **üst sınırıdır**.
- **Öneri:** `aralik` = bir sonraki planlı selama kadarki üst sınır (katlamadan sonraki `I`, titreşim dâhil, ör. `1,1·I`); ara ilanın taşıdığı değer de bu tanımla.

### B-7 · `s` (selam kaybı) protokolün görebildiği veriyle tanımlanmamış; eşiğin dayanağı kâhin sayımla ölçüldü — **önemli**

- **Yer:** `KK-03-KANIT.md:19` (kural 1) · `KK-00-DIZIN.md:34` (`KAYIP_ESIGI`).
- **Ne eksik:** "ham sayımdan (beklenen ↔ gelen)" bir algoritma değil. Protokol komşunun ne zaman selam gönderdiğini bilemez. Beklenen ya zamandan (`pencere / a_j`), ya sıra boşluğundan (geriye dönük; T-1: boşluk ancak sonraki selamla görülür), ya KK-01'in donmasız zaman aşımlarından çıkarılır. Üçü farklı `s` verir, en çok sessiz (ED) komşuda: boşluk yöntemi o komşu dönene kadar hiçbir kayıp görmez.
- **Kanıt:** teşhis (d) kaydedicisi beklenen selamı göndericinin gerçek selam kuruluşlarından saydı (`kalibrasyon/karistirma_isaretleri.py:397–407`, `selam_gonder` → `beklenen[(i, dilim)]`); bu kâhin bilgisidir. `KAYIP_ESIGI = 0,6` bu tanımdan ve Babel'in 4 s'lik Hello'suyla ölçüldü. Kaydedici "beklenen yoksa tanımsız" diyor; KK-03 bu durumu yazmıyor.
- **Öneri:** `s` algoritmik olarak yazılsın (ör. tanıdık her komşu için beklenen = 4 s pencerede KK-01 kural 2'nin dondurmasız zaman aşımları + gelenler). "Beklenen yok → işaret yok" eklensin. Eşiğin dayanağına kâhin sayım ve 4 s'lik Hello koşulu yazılsın.

### B-8 · Açlık kuralı bir durumu kapsamıyor; istek gereksiz tur artışı üretebiliyor — **önemli**

- **Yer:** `KK-04-ROTA.md:26` (kural 8).
- **Ne yanlış:** Kural iki dal tanımlar: "`A` boş ama uygulanamaz ilanlı komşular var → istek" ve "`A` boş ve sonlu ilanlı komşu da yok → istek yok". Bu dallar şu durumları kapsamıyor:
  1. `A` boş, çünkü uygulanabilir ve sonlu ilanlı komşuların hepsi KÖTÜ ya da KARIŞTIRILIYOR; uygulanamaz ilanlı komşu yok. İki dal da uymuyor; istek gönderilip gönderilmeyeceği tanımsız.
  2. Uygulanamaz ilanlı komşular var ama hepsi KÖTÜ ya da KARIŞTIRILIYOR. İstek gider, geçit turu artırır, yeni turla o komşular uygulanabilir olur ama yine `A`'ya giremez. İstek boşa gider; tur artışı bütün ağı çalkalar (`17` §7 madde 10; B-10'daki selam bedeli).
- **Öneri:** istek yalnız en az bir OLAĞAN komşunun sonlu ve uygulanamaz ilanı varsa gitsin; öteki bütün durumlarda istek yok, paket bekletilir. Kalan durum açıkça yazılsın.

### B-9 · Uygulanabilirliğin ne zaman hesaplandığı yazılı değil; saklanan sonuç bayatlarsa döngü kurulabilir — **önemli**

- **Yer:** `KK-04-ROTA.md:11` ("son kabul edilen ilanı … ve uygulanabilir mi") · `:19–20`.
- **Ne yanlış:** FD, düşük bir maliyet ilan edilince küçülür (kural 6). Uygulanabilirlik alımda hesaplanıp saklanırsa şu olabilir: j'nin (T, 2,5) ilanı FD (T, 3,0) iken "uygulanabilir" diye işaretlenir; FD (T, 2,0)'a inince işaret bayatlar; j seçilirse `FD_j < FD_i` değişmezi bozulur ve döngü olasılığı doğar.
- **Kaynak:** RFC 8966 §3.5.3: rota tablosunda "metrik dalgalanması yüzünden" uygulanamaz kayıt bulunabilir; §3.6: uygulanamaz rota hiç seçilmez.
- **Öneri:** "Uygulanabilirlik her seçimde güncel FD'ye göre hesaplanır, saklanmaz" (B-1'deki "sonlu" şartıyla birlikte).

### B-10 · Tur değişimi tetiği T-17'den geniş ve kaynağına aykırı — **önemli**

- **Yer:** `KK-02-SELAM.md:28` ("ilan ettiğim tur değişti") · `:49` (kaynak §3.7.2) · `v2/17-TASARIM-KARARLARI.md:220` (T-17: "tur bir isteğe yanıt olarak değişince").
- **Ne yanlış:** KK-02'nin maddesi, ardılı yeni turu benimseyen her düğümü tetikler: her tur artışında 40 düğümün hepsinde `I ← I_MIN` olur ve yeni tur ağ boyunca dalga hâlinde yayılır. T-17 yalnız isteğe yanıt olan değişimi sayar. RFC 8966 §3.7.2 de yeni sıra numarasını yaymak için tetik göndermemeyi önerir (isteği karşılamak dışında); kâğıt aynı paragrafı kaynak gösteriyor. RFC'de yanıtı istek yolunun düğümleri iletir: "son iletilen istekler" listesi (§3.8.1.2). KK-04 kural 9'da bu liste yok; geniş tetik bu eksikliği kapatıyor.
- **Bedel:** `zaman_cizelgesi.py` §6: tur artışı başına düğüm başına +2 selam (30 s'de 15 → 17); 40 düğümde artış başına +80, 30 s'de 4 artışta +280 selam.
- **Öneri (karar):** ya RFC'ye daraltılır (KK-04 kural 9'a son iletilen istek listesi eklenir, tetik yalnız bekleyen isteği karşılayan değişimde gider), ya geniş hâli T-17'ye bedeliyle yazılır ve §7 madde 10'un tanı kaydına girer.

### B-11 · Karıştırılan gönderici bütün kullandığı bağları KARIŞTIRILIYOR yapıyor; bunun kararı yok — **önemli**

- **Yer:** `KK-03-KANIT.md:27` (kural 7, "kendi girişim işaretim") · `KK-01-BAG.md:32` · `KK-04-ROTA.md:26` ("sorun benim alıcımda").
- **Ne eksik:** T-6'ya göre bütün komşulara başarısızlık göndericinin kendisini gösterir. Girişim alanındaki gönderici onayları çözemez; veri çerçevesi ise alandan dışarıdaki ardıla çoğu zaman ulaşır. Kural 7, kendi işaretiyle ardıl bağını KARIŞTIRILIYOR yapar. Sonraki bağlar da aynı biçimde düşer, `A` boşalır, `C = ∞` olur, istek de gönderilmez (kural 8). Düğümün kendi telemetrisi 2 s bekletilip düşer. Gönderici karıştırılırken bağı bırakmanın ya da göndermeyi sürdürmenin kararı T-6/T-9'da yok; kâğıt bunu sessizce seçiyor. KK-04 kural 8 aynı durumu "sorun benim alıcımda" diye tanıyor ama veri bağlarına uygulamıyor.
- **Öneri:** açık bir kural yazılsın ve sınıfı belirtilsin. Örnekler: "karıştırılıyorum" iken MAC başarısızlıkları bağ durumunu değiştirmez, ardıl korunur; ya da son ardıl son çare olarak tutulur. Tanı kaydında ölçülsün.

### B-12 · Veri penceresinin en az örneği yok: tek başarısız çerçeve `ETX_veri = ∞` — **önemli**

- **Yer:** `KK-01-BAG.md:31` (kural 5, "hiç başarı yoksa ∞") · `KK-00-DIZIN.md:24`.
- **Ne yanlış:** Son 10 s'de tek bir veri çerçevesi olan ve o çerçevesi başarısız olan bağ ∞ > 4 ile KÖTÜ olur ve ceza alır. Durumlar: yeni seçilen ardılın ilk çerçevesi (temizde %1,76 olasılık); yalnız komut taşıyan ters bağlar. KK-05 kural 7 OLAĞAN ister; tek başarısız komut çerçevesi o alt ağaca komutu 10–40 s kapatır.
- **Öneri:** `ORNEK_EN_AZ`'a benzer bir en az çerçeve sayısı (ör. 4) olmadan tetik ateşlenmesin.

### B-13 · Ablasyon bayraklarının bağımlılıkları ve mekanizma eşlemesi eksik — **önemli**

- **Yer:** `KK-00-DIZIN.md:53–62`.
- **Ne eksik:**
  1. `karistirma_durumu` kapalıyken KK-03'ün kendi durumu yine KK-01 kural 9'u (dondurma), KK-02 kural 4a'yı ve KK-04 kural 8'in isteği bastırmasını sürüyor mu? Kural 5'in KARIŞTIRILIYOR dalı KÖTÜ'ye mi gider? Yazılı değil.
  2. `alici_bildirimi` kapalıyken: alan kaldırılır mı (65 → 64 bit, 9 → 8 bayt), yoksa hep 0 mı gönderilir? Bit değişimi yine olay mı?
  3. `hatirlanan_kalite` kapalıyken: KARIŞTIRILIYOR'da ve kural 9'da `gecmis` yine donar mı?
  4. `uyarlanir_aralik` kapalıyken ("sabit `I_MAX`"): T-17'nin ara ilanı (olayda hemen selam) da kapanıyor mu? Bayrak T-1 ile T-17'yi birleştiriyor. Ara ilan kapanırsa tur yanıtı 2 s/atlama yayılır ve `TUTMA_EN_COK = 2 s` ile çatışır.
  5. Bayraksız mekanizmalar: 4a, kural 9'un dondurması, `T_CEZA`, uygulanamaz ilanı yok sayma, açlıkta istek. `17` §7 madde 11 eşlemeyi ve kapıya hangilerinin gireceğini istiyor. K-247 sınıfın ve amacın ölçmeden önce yazılmasını şart koşuyor. `06` §0.4.5 kapıyı "birlikte kapatılınca" tanımlıyor; hepsi kapalı yapılandırma tanımsız.
- **Öneri:** "mekanizma → bayrak (ya da 'çekirdek, bayraksız' ve gerekçe) → sınıf → kapalıyken bağımlı kuralların davranışı" tablosu; kapının hepsi kapalı yapılandırması tek satırda.

### B-14 · A/B ölçütü sınıfa göre ayrılmamış; yer karıştırıcılı aile eksik — **küçük**

- **Yer:** `KK-00-DIZIN.md:64–68` · `KK-01-BAG.md:54–56` · `KK-02-SELAM.md:44–45` · `KK-04-ROTA.md:40–41`.
- **Ne yanlış:** KK-00 her A/B için "birincil hücrede `PDR_açık` artışı ve ikizde zarar yok" diyor. Genel mekanizmaların kâğıtlardaki sınanması ise ikiz ölçüleri: `veri_kotu_tetigi` için ikizde iletim kaybı, `istege_bagli_esik` için ardıl değişim sıklığı. K-247 genel katkıyı ikizdeki ablasyonla beyan ettiriyor. `v2/12` §2 Faz 5 (satır 92) her mekanizmada "bir yer karıştırıcılı aile" de istiyor; KK-00'da yok.
- **Öneri:** kabul ölçütü sınıfa göre yazılsın (karıştırmaya karşı · genel); aile eklensin ya da neden çıkarıldığı yazılsın.

### B-15 · Sayısal dayanaklarda düzeltmeler — **küçük**

- `KK-00-DIZIN.md:29` (`I_MIN · I_MAX`): "3 kaçan selam × 2 s = 6 s". Kural 2'ye göre `k` sıfır son alınan selamdan `(k + 0,5)·a` sonra tamamlanır; karıştırıcının başlangıcına göre `(k − 0,5)·a … (k + 0,5)·a`. `k = 3` için 5–7 s (ortalama 6 s doğru). `k`, `d_r` ile büyür: 0,7 → 7–9 s · 0,6 → 11–13 s (10 s'lik açık dönemden uzun) · 0,5 → 13–15 s (`zaman_cizelgesi.py` §1). "< 10 s" yalnız `d_r ≥ 0,8` bağlar için geçerli.
- `KK-00-DIZIN.md:39` (`ISTEK_YINELEME`, "Babel [4]"): sayı (3) Babel'in (`babel_bicim.py` `ISTEK_TEKRAR = 3`), 0,5 s'lik aralık değil (`ISTEK_ZAMAN_ASIMI_S = 2,0`, her yinelemede × 2; acil 0,2 s).
- `KK-00-DIZIN.md:41` (`ISTEK_ATLAMA = 8`): dayanak yok. RFC 8966 §3.8.2.1 ağın çapından büyük bir değer istiyor (64 önerilir); çap denetlenmedi (S-5).
- `KK-00-DIZIN.md:25` (`T_HATIRA`, "teşhis (d) S3: 32 s'de bant değişmiyor"): S3 doymuş ölçüdür. Tek deneme başarısı ve yedek bağlar ölçülmedi; T-1 ve `sonuc.md` §8 tek başına yetmediğini yazıyor. Dayanak bu çekinceyi taşımalı (`17` §7 madde 8).

### B-16 · KK-04 kural 9'un iletim kuralı kaynağıyla uyuşmuyor; ardılsız düğüm tanımsız — **küçük**

- **Yer:** `KK-04-ROTA.md:30`.
- **Ne yanlış:** "ardılım isteği gönderense iletilmez (RFC 8966 §3.8.1.2)". RFC bu durumda isteği başka bir uygulanabilir rotanın ardılına iletmeyi zorunlu kılar (yoksa uygulanamaz olanınkine iletmeyi önerir). Basitleştirme savunulabilir, ama atıf tersini söylüyor. Ardılı olmayan (`C = ∞`) düğümün isteği ne yapacağı yazılı değil.
- **Öneri:** kendi seçim olarak yazılsın ya da RFC'ye uyulsun; ardılsız düğüm için "iletilmez" eklensin.

### B-17 · KK-04 kural 7'nin 5 s'lik sayacı ayrıntısız — **küçük**

- **Yer:** `KK-04-ROTA.md:25`.
- **Ne eksik:** 5 s ilk yok sayılan ilandan mı başlar, sonraki yok saymalar sayacı yeniler mi? Bu sürede uygulanabilir bir ilan gelirse yok sayma biter mi? "İlan uygulanır" hangi ilan (son alınan mı)? Sayaç bir `Uyandirma` mı ister, yoksa sonraki selamda mı bakılır?
- **Öneri:** dört soru tek cümlede yanıtlansın.

### B-18 · Kodlama ayrıntıları — **küçük**

- **Maliyet birimi:** `C`, FD ve bütün karşılaştırmalar `ETX × 64` tamsayı biriminde mi? Yuvarlama yönü ne? Sonlu değer 0xFFFE'de doyar mı? FD ilan edilen (nicemlenmiş) değeri tutmalı (T-12: "gönderdiğim değer").
- **`sira` ve `tur`:** başlangıç değerleri ve modüler karşılaştırma. 350 s'de en çok 2 selam/s ile sarma olmaz; yine de yazılmalı.
- **Eşit maliyetli adaylar:** sıralama kuralı (T-15'in 5-3'e kalanı "yedeklerin sıralanması").
- **`c̄`:** "son 30 s" zaman penceresi mi, son 30 işaretsiz saniye mi? Pencerede işaretsiz saniye yoksa son değer korunur mu? Sürekli karıştırmada pencere boşalır.
- **KK-03 kural 4:** "işaretsiz", iki işaretin de olmaması mı? Etkin işaretin türü değişirse çıkış kuralı hangisi?
- **KK-03 kural 6:** `gecmis` tamamen sıfırken `d_r` tanımsız; `d_r ≤ 0,25` için `k = 17 > N = 16`, yani tespit ulaşılamaz.
- **KK-01 kural 9:** "silme süresi işlemez": süre duraklar mı, çıkışta baştan mı başlar?
- **KK-04 kural 8:** kendi karıştırılmamdan çıkınca istek hemen mi, yoksa sonraki `ISTEK_ARA` adımında mı (en çok 5 s) başlar?
- **KK-03 kural 8:** "2 ardışık selam" sıra numarasına göre mi, varış sırasına göre mi?
- **KK-01:** kural numaraları 7, 9, 8 sırasında.

### B-19 · Niyet döndüremeyen kancalarda verilen kararlar — **küçük**

- **Yer:** `KK-01-BAG.md:31` · `KK-05-BEKLETME-KOMUT.md:21` (kural 3) · `:26` (kural 6).
- **Ne eksik:** `iletim_sonucu` ve `cerceve_duyuldu` niyet döndüremez (`sim2/gozlem/protokol.py` belge dizgileri; `sim2/kosum/kontrol.py` döndürülürse hata verir). Kural 5'in `iletim_sonucu`ndaki kararı ardılı değiştirebilir. Bu maliyet olayı (KK-02 kural 3, "hemen") başarılı çerçevede, arkasından `iletim_basarisiz` gelmediği için, bir sonraki niyetli kancaya kadar gönderilemez. KK-05 kural 3'ün "yol bulunduğunda hemen" ilkesi iz tazelenmesinde uygulanamaz, çünkü iz `cerceve_duyuldu`da tazelenir; komut bir sonraki 0,5 s uyanmasını bekler. `ilk_bekletme`nin simülatörün sayı tavanıyla (`tampon_asimi`) düşen paketler için temizlenme kuralı yok; kalan kayıtlar gereksiz uyanmalar üretir.
- **Öneri:** "niyetsiz kancadaki değişim, bir sonraki niyetli kancada (en geç 1 s'lik zamanlayıcıda) uygulanır" kuralı yazılsın; `ilk_bekletme` için bir yaş sınırı (ör. `TUTMA_EN_COK + 1 s`) eklensin.

### B-20 · Kararların 5-3'e bıraktığı üç nokta yazılmadı — **küçük**

- T-18: sınırın türü "atlama başına sınır ve paketin en çok kaç kez tutulabileceği ya da başlıkta birikmiş bekleme" (`17:226`). KK-05 kural 5 yalnız atlama başına sınırı seçiyor; sayı sınırı ve başlık seçeneği yanıtsız.
- T-11'in 5-3'e kalanı: "kötü bağ (T-3) için de aynı olay sayısı kuralının geçerli olup olmayacağı" (`17:158`). KK-01'in örtük yanıtı "hayır"; açıkça yazılmalı.
- `17` §7 madde 8 ve 9 (bağ kalitesinin değişim hızı, başka karıştırıcı sınıfları) hiçbir kâğıdın "Sınanması"nda yok.

---

## 2 · Sorunlar (bulgu değil, bilinmeli)

- **S-1 · Veri tetiğinin ikizdeki yanlış alarmı ve geçit hunisi.** Temizde `ETX_veri ≈ 1,98 / 0,982 ≈ 2,0`; `E_CIK = 4`. Sekiz çerçevelik pencerede iki vazgeçme olasılığı çerçeve başına %1,76'da ~%0,9. Geçidin komşularındaki bağlar en yüklü bağlardır; kullanılabilirliğe giren yük (T-4'ün kaygısı) burada yoğunlaşır. Bayrağın ikiz A/B'sinde bağ başına ve geçide uzaklığa göre veriyle KÖTÜ sayısı izlenmeli.
- **S-2 · `TUTMA_EN_COK` ve tur isteğinin gidiş-dönüşü.** Dönüş, atlama başına selam aralığı sınırını (0,5 s) ve titreşimi bekler. Atlama başına ortalama ~0,3 s, en kötü ~0,57 s. Geçide 4 atlamada ortalama 1,2 s, en kötü 2,3 s; kaybolan yayın isteği +0,5 s (`zaman_cizelgesi.py` §7, iyimser iletim süresiyle). KK-05'in örneğindeki 0,6 s derin düğümler için iyimser.
- **S-3 · KARIŞTIRILIYOR yolunun sessiz evre bedeli.** Bitin çıkışı (3 s) ve iki selam ~4,5 s sürer: 15/15'te sessiz evrenin %30'u, 10/20'de %22'si (B-2 tablosunda p = 0). T-10 bu bedeli kabul ediyor; KK-01'in sınanmasındaki "sessiz dönemin ilk saniyeleri" ölçüsü bunu görünür kılar.
- **S-4 · Girişim biti eşik çevresinde gidip gelebilir.** `DUSUS_ORANI = 0,5`, karıştırılanların ortalamasında duruyor (49 ↔ 0,5 × 99 = 49,5). Saniyelik işaret olasılığı p = 0,4 ise ortalama giriş 8,8 s, çıkış 9,1 s sürer; açık dönemde birkaç geçiş olur. Her geçiş `I_MIN`'e iniş ve komşularda ardıl değişimi demektir. Tanı kaydında geçiş sayısı ölçülmeli.
- **S-5 · `ISTEK_ATLAMA = 8` ile ağın çapı.** Çap denetlenmedi (doğrulanamadı); geliştirme verisinden en uzun atlama sayısına bakılmalı.
- **S-6 · Teşhis (d)'nin eşikleri Babel-a trafiğinden.** Ölçüm 4 s'lik Hello ve "tanıdık = son 16 s'de duyulmuş" tanımıyla yapıldı. 0,5–2 s'lik selam `s`'nin dağılımını değiştirir; T-5 bunu yazıyor.
- **S-7 · Hatıra, tespit öncesindeki ardışık olmayan kayıpları taşır.** Girişimde kısmi kayıp sondaki sıfırlar gibi atılmaz; dönem başına hatıra biraz aşınır.
- **S-8 · RFC 8966 §3.8.2.2'nin ikinci paragrafı alınmadı.** Seçili olmayan ama daha iyi görünen uygulanamaz komşuya istek önerisi uygulanmıyor. T-13 bunu kararlaştırmamış; kusur değil, olası bir iyileştirme.

## 3 · Temiz çıkanlar

- **Döngüsüzlük çekirdeği** (B-1 ve B-9'daki iki şartla): FD ilan edilen değerle tanımlanmış, güncellemesi RFC 8966 §3.7.3 ile aynı (`KK-04:13, :24`). İlanın turu seçili rotanınki. Seçili ardıldan gelen uygulanamaz **sonlu** ilanı yok saymak değişmezi korur: ardılın FD'si yalnız küçülür ve benim ilanım kabul edilmiş `(s, C_j)`'den pozitif bağ maliyetiyle türer. İsteğe bağlı geçiş turu hesaba katmıyor (RFC §3.6). Tur yalnız geçitte, istekle ve en çok 1 artıyor (RFC §3.8.1.2). Sonsuza sayma yok. Bu iki şart dışında döngü için karşı örnek kurulamadı.
- **Gözlem sözleşmesi:** okunan her girdi (`mesgul_sure_s` + `kanal_dolulugu_ister`, `alinan_cerceve`, `iletim_sonucu`, `iletim_basarisiz`, `cerceve_duyuldu`'nun göndereni/türü/hedefi/paket başlığı, `kontrol_alindi`) `sim2/gozlem/pencere.py`'nin izin listelerinde ve kancalarda var. RSSI, gürültü, GPS ve simülatörün komşu listesi okunmuyor. Geçidin kimliği kurucudan geliyor (v0.4.1'de de böyle: `DESPARETE(i, kfg.gecit, …)`). Kâhin sızıntısı bulunmadı.
- **Mesaj biçimi:** 65 + 16n bit → 9 + 2n bayt; 15 komşuda 39 bayt, 64 baytlık ek yükle 103 bayt, 1 Mb/s'de PLCP dâhil ~1,02 ms. Değerler alanlara sığıyor (40 düğüme 8 bit adres, 0,01 s birimli 16 bit aralık, `d_r × 255`). İki tekrarlı alan `MesajBicimi` ile kurulabilir. `tur_istegi` 24 bit.
- **Kontrol düzlemi:** dinamik selam `Uyandirma` ile, KK-03'ün saniyelik işi periyodik zamanlayıcıyla kurulabilir. Bekleyen uyandırma 256'nın çok altında kalır. Beş kanca zaten gerekli (hepsi-ya-hiç). `kosum_beaconi = False`. Tamponun yeniden sorulması yalnız `Uyandirma` ile (K-135). Simülatör tamponu en eskiyi atıyor, 64 paket, 30 s ömür (> 2 s). `rota_gecersiz` beyanı `sonraki=None` ile geçerli.
- **`mesgul_sure_s`:** her gözlemde integral o ana kadar kapanıyor (`sim2/kosum/dugum.py:186–193, 220–245`). Saniyelik zamanlayıcı, karıştırıcı geçişindeki bölünmeme beyanının etkisini 1 s ile sınırlıyor.
- **Sayılar kaynaklarıyla tutuyor:** `N = 16` ve `ZAMAN_ASIMI = 1,5` (`babel_bicim.py:115–116`) · `E_CIK = 4` (RFC 6719 MAX_LINK_METRIC 512 = ETX 4) · `GECIS_ORANI` %10 (T-11, [54]) · `ED_ESIGI` 0,62 / %0,035 · `KAYIP_ESIGI` 0,6 (0,69 ↔ 0,44) · `DUSUS_ORANI` dayanağı 49 ↔ 99/s · `MAC_ARDISIK = n* = 3` (teşhis (d) §1, §3, §7) · `k` formülünün örnekleri (0,9 ve 0,8 → 3, 0,6 → 6, 0,5 → 7).
- **KARIŞTIRILIYOR süresi** iki çizelgede de `T_HATIRA`'nın altında (11–15 s < 30 s).
- **Selam yükü:** ~%0,75 (15 × 0,5/s × 1 ms; kâğıttaki "kabaca %1"). Komşu durum değişimi olay sayılmadığı için karıştırma sırasında selam seli yok.
- **KK-01 kural 7:** bağ düzeyinde dondurmada `beklenen`in izlenmesi hatırayı koruyor. 4a, ED'deki düğümün sırasını ilerletmediği için dönüşte boşluk küçük.
- **Düğüm kaybı:** sessizlik → KARIŞTIRILIYOR/KÖTÜ → 30 s'de silme. Geçit düğüm kaybına girmiyor (`sim2/kosum/kayip.py:41`).
- **T-20 / KK-05:** geri iz, tazelik, OLAĞAN şartı (`17` §7 madde 5), ortak tampon ve öncelik yokluğu (madde 4) kararlarla uyumlu.
- **Sadakat:** T-1…T-20'nin her birinin kâğıtta karşılığı var. §7 madde 1–5 karşılanmış, madde 12 (RSSI) KK-03 kural 9'da.

## 4 · Doğrulanamayanlar

- Veri tetiği ile karıştırma kanıtı arasındaki yarışın DESPARETE trafiğindeki sıklığı. B-2'deki zamanlar Babel-a'nın çerçeve başına ortalamalarından ve ortalama `s` rampasından; bağ başına trafik hızı varsayım.
- B-3'teki ölü durumun sıklığı (birleşik girişim işaretinin ikizdeki yanlış alarmı ölçülmedi).
- Girişim için birleşik kuralın yakalama ve yanlış alarm oranı (teşhis (d) kaydı bunu hesaplayamıyor, `sonuc.md` §7).
- Ağın çapı (`ISTEK_ATLAMA`) ve S-4'teki saniyelik işaret olasılığı.

## 5 · Hüküm

**Kural kâğıtları bu hâliyle kodlamaya hazır değil.** Kararların kendisi kâğıtlara büyük ölçüde sadık. Döngüsüzlük çekirdeği, gözlem sözleşmesine uyum, mesaj biçimi, kontrol düzlemi ve sayısal dayanakların çoğu temiz. Ama durum makinesinde ve döngüsüzlük kuralında, kod yazılırsa davranışı kararların amacına ters çevirecek üç kusur ve kodlayanın tahmin etmek zorunda kalacağı birkaç boşluk var. Hepsi belge düzeyinde düzeltilebilir; simülasyon gerekmez.

Kod yazılmadan önce sırasıyla:

1. **B-1:** ∞ ilanı her zaman uygulanabilir; `A` yalnız sonlu ilanlı; kural 7 yalnız sonlu ilan için (KK-04 kural 1, 2, 7).
2. **B-3:** "kendi" sebepli KARIŞTIRILIYOR'un çıkışı seviye koşuluyla; KARIŞTIRILIYOR'a güvenlik üst süresi (KK-03 kural 8 tablosu, KK-01).
3. **B-2:** veri tetiği ile karıştırma kanıtının hakemliği, `T_CEZA` katlanmasının kapsamı, KARIŞTIRILIYOR'a girişte veri penceresinin boşaltılması (KK-01 kural 5, 8). Karar gerektirir.
4. **B-4:** aynı olayda geçiş sırası, tablo ile kural 5'in eşlenmesi, sebebin çokluğu (KK-01).
5. **B-5:** dondurmadan çıkışta sıra boşluğu (KK-01 kural 1, 9).
6. **B-9 ve B-8:** uygulanabilirliğin güncel FD ile hesaplanması; açlıkta istek koşulunun OLAĞAN komşuya bağlanması (KK-04).
7. **B-6 ve B-7:** `aralik`'ın anlamı; `s`'nin algoritması ve "beklenen yok" durumu (KK-02, KK-03).
8. **B-12:** veri penceresinde en az örnek (KK-01 kural 5).
9. **B-11:** karıştırılan göndericinin bağları için kural (KK-03 kural 7). Karar gerektirir.
10. **B-10:** tur değişimi tetiği; T-17 ile hizalama ya da RFC'ye daraltma (KK-02 kural 3, KK-04 kural 9). Karar gerektirir.
11. **B-13:** bayrak–mekanizma–sınıf tablosu ve kapalıyken bağımlı kurallar; kapının hepsi kapalı yapılandırması (KK-00).

B-14…B-20 küçük; kodla birlikte, ama ilk A/B'nin beklentisi yazılmadan önce kapatılabilir. Bu liste kapanınca kâğıtların yeniden okunması önerilir: B-2 ve B-11'in çözümü durum makinesine yeni geçişler ekleyecek, B-4'ün sırası onlarla birlikte yazılmalı.
