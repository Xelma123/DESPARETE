# Faz 5-3 · B5 teşhisi — iletim kaybının yeri: karıştırılan alıcı, sıradaki aday ve kanıtın zamanı — beklenti

> 26 Kasım 2026 · `v2/18` §2.5'in (B5 iletim kararı) teşhis ölçümü. Kararım: B5'in ana seçeneğinden önce seçenek ailelerinin girdisi ölçülür. Aileler: A tek yol · B paket başına hızlı sapma · C seçici kopya · D kurtarma. Bu dosya koşudan ve dumandan önce commit'lenir. Öngörüler bu teşhisin hiçbir koşusundan önce yazıldı; dayanakları önceki ölçümlerin kayıtlarıdır. Sonuç ayrı `sonuc.md`ye yazılır, bu dosyaya dokunulmaz.
>
> Alet: `olcum.py` (kaydedici) · `iletim.py` (saf işlevler; sınaması `sinama/saf.py`) · `kosu.sh` · karar hesabı `sonuc_hesap.py` (bu kuralın kodu; koşudan önce yazıldı). İki parça önceki teşhislerden değiştirilmeden içe aktarılır: B1'in selam sayımı B3 teşhisinin `bag.py`'sinden, B2'nin kuralları B2 teşhisinin `isaret.py`'sinden.

## Amaç

Birincilde açık dönem kaybının büyüğü iletimdedir. Bugünkü kodda uygulanabilirlik koşulunu kullanan kolda (`eğim0`) `PDR_açık` 0,665, iletim kaybı 0,297. Bu kaybın alıcıya göre dağılımı (kayıp anatomisinin alanı):
- kanal kilidi 0,048;
- girişim 0,168;
- uzak 0,081.

Kaynak: `arsiv/teshis/faz5_3_yeni_cekirdek_2026-11-19/kayit_egim0_birincil.json`, `dogum_evre_dusen`, 8 tohum. Hedefe (~0,713) 0,048 eksik.

B5'in seçenek aileleri bu kaybın farklı parçalarına ulaşır:
- **A · tek yol:** paket hep ardıla gider; karıştırmaya karşılık B2 → B3 → B4 zincirinden gelir.
- **B · paket başına hızlı sapma:** ardıla giden çerçeve kötü bitince sonraki paketler kısa süre sıradaki adaya gider; yolun durumu değişmez.
- **C · seçici kopya:** ardılın kanıtı varken paketin bir eşi sıradaki adaya da gider.
- **D · kurtarma:** MAC vazgeçince paket düşmez, sıradaki adaya gider (DSR'nin "salvaging"i, RFC 4728 §3.4.1). Simülatörde bu yetenek yoktur.

Teşhis her kaybı, kararın verildiği andaki duruma göre sınıflar ve her ailenin ulaşabileceği payı ölçer. Ailelerin kendisi kodlanmaz ve ölçülmez (A/B yok). Karar anındaki durum kayıtlardan, yeni tasarımın kurallarıyla, protokolün dışında hesaplanır.

## Sorular

- **S1 · Kaybın yeri (karar):** açık dönemde doğan paketlerin iletim kaybı, kararın verildiği anda hangi durumda oluyor? Alıcı karıştırılıyor mu; yeni tasarımın kanıtı ya da kuralı ardılı zaten bırakır mıydı; sıradaki aday temiz mi?
- **S2 · Zaman (betimleyici):** karıştırılan alıcıdaki kayıp, dönemin başından, alıcının alana girişinden ve kanıttan ne kadar sonra oluyor?
- **S3 · Hızlı sapmanın tetiği (B elenmezse kâğıdın girdisi):** hangi tetik ve süre, karıştırılan alıcıya giden paketleri yakalar ve temiz kanalda az sapar?
- **S4 · Kopyanın bedeli (betimleyici):** iki kopya kuralı kaç kararda ateşlenir, kanala ne kadar yayın ekler?
- **S5 · Kurtarmanın kestirimi (betimleyici):** vazgeçmede sıradaki adaya gidilseydi kâhine göre ne kadarı geçerdi, kanala ne kadar yayın eklenirdi?

## Düzen

- **Kol:** `desparete5_egim0`. Tanımı yeni çekirdek ölçümündekinin aynısı: `CEKIRDEK`'ten `egim`, `vazgecme_tetigi` ve `duzgun_gecis` kapalı. Yani FD ve tur, veri tetiği yok, bekletme 1 s, karıştırma katmanı kapalı. Geri gönderme yasağı ve sınırlı yükselme yalnız eğimde çalışır, burada etkisizdir.
  - Sebep: B4'ün kararı (Y1, uygulanabilirlik koşulu) bu ailedendir. Bugünkü kodda adaylarını aynı kuralla seçen kol budur.
- **Hücreler** (`formasyon · yere_toplama`, tam pencere, 350 s):
  - **ikiz:** karıştırıcısız, hayalet çizelge 10:20;
  - **birincil:** `derin_sizma`, 15 s açık · 15 s sessiz.
- **Tohumlar:** 1003–1010.
  - S1'in hükmü sekiz tohumun ortalamasıyla verilir; burada seçim yapılmadığı için yarılara bölünmez.
  - S3'te **seçim yarısı 1003–1006, doğrulama yarısı 1007–1010**.
- **Koşu:** dondurulmuş kopyadan, hücre başına bir adım (8 tohum, 8 işçi), kayıp anatomisi aletinin işçisiyle. Kaydedici yalnız okuyan sarmalayıcılar takar. Tek ek, kanal meşgul integralinin açılmasıdır (B2 ve B3 teşhislerinde birebirdi).
- **Hesap protokolün dışında yapılır:** kayıtlardan, yeni tasarımın kurallarıyla (B1 kural 4–13; B2 kural 1–13; B3 kural 5–8; B4 kural 1–5). Bugünkü kodun bağ durumu ve rotası yalnız paketin nereye gittiğini verir.

## Tanımlar

**Karar ve kayıp:**
- **Karar:** bir telemetri paketi için bir düğümde (i) sonraki atlamanın (j, ardıl) seçildiği an (t). Paket o anda havaya çıkar. Kararın sonucu, o atlamanın MAC sonucudur (deneme sayısı, onay ya da vazgeçme).
- **Kayıp:** üç koşulu birden taşıyan paket:
  - ölçüm penceresinde (50–320 s) ve karıştırıcı açıkken doğmuş;
  - teslim edilmemiş;
  - tek düşüşü iletim başarısızlığı (MAC'in vazgeçmesi).

  Kaybın kararı, vazgeçilen atlamanın kararıdır. Paylar açık dönemde doğan bütün paketlere bölünür (`PDR_açık`'ın birimi). Komutların kaybı ayrı sayılır.

**Kâhin etiketleri** (yalnız değerlendirmede kullanılır, `05` §8):
- **Alan** (E · G · U): kayıp anatomisinin etki alanı, saniyenin ortasında. Sınıflamada karar anında karıştırıcı kapalıysa alıcının alanı U sayılır.
- **Bağın bandı:** 7 denemelik başarı p₇ = 1 − (1 − p)⁷. Burada p kâhinin tek deneme başarısıdır: sönümleme ve karıştırıcı dâhil, ağın kendi girişimi hariç, 5 s'lik dilimin ortasında. Bant p₇ ≥ 0,90 ise "iyi"dir.
- **Temiz aday:** alanı U ve bağı iyi bantta olan aday.

**Yeni tasarımın görünümü** (t anında, i'nin; yalnız t'den önceki olaylarla):
- **Bağ ve maliyet:** B1'in selam sayımıyla (B3 teşhisinin `b1_selam`'ı). M = ⌈64 · `E_selam`⌉. `E_selam` ∞ ise ya da `n_s` < 4 ise bağ kullanılmaz.
- **İlan:** komşunun son selamındaki (tur, maliyet). Selam aralığı `a`'nın 3,5 katından eskiyse ∞ sayılır (B4 kural 4).
- **FD:** i'nin selam kurarken güncellediği değer (B4 kural 9 ile bugünkü kodun kuralı aynı); kayıttan okunur.
- **Aday:** kayıtlı, kullanılır, ilanı taze ve sonlu, uygulanabilir (B4 kural 1–3) her komşu.
- **B2'nin durumu:** her düğümün saniyelik `m` (kanal meşgul payı), `c` (çözülen çerçeve) ve `s` (selam kaybı payı) dizilerinden B2'nin kurallarıyla:
  - kanal kilidi `m` ≥ 0,55;
  - girişim G(0,4 · 0,6 · 2 · 1);
  - kendi aralıklar geriye dönük başlar (B2 kural 8).

  Saniyeler simülasyon saatinin tam saniyeleridir (B2 teşhisindeki gibi).
- **SON ÇARE sebepleri** (B3 kural 5–8):
  - **Bildirim:** komşunun i'ye ulaşan son selamının biti 1'dir. Bit, selam kurulduğu andaki B2 durumudur. İki biçim hesaplanır:
    - **gerçekçi:** bit bugünkü kodun selamlarıyla gelir;
    - **anında:** bit, komşunun durumu değiştiği saniye sonunda i'de bilinir.
  - **Gönderici:** DEN7x3 olayı, B3 kural 6'nın uzatmasıyla ve 5 s'lik ömrüyle.
  - **Veri yok:** son 4 kaydın hepsi vazgeçme ve en yenisi 5 s içinde.

  Geçide giden bağda bildirim ve gönderici sebebi yoktur (B3 kural 8). Kendi aralıklarıma düşen kayıtlar sayılmaz.
- **Adayın sınıfı:** sebebi yoksa O, varsa S.
- **Sıradaki aday k1:** ardıl dışındaki en iyi aday. Önce O, sonra S; sınıf içinde m = M + C'ye göre; eşitlikte küçük M, sonra küçük adres (B4 kural 5).
- **Ardılın kanıtı:** karar anında ardıl için bir SON ÇARE sebebi vardır, ya da ardıl aday olmaktan çıkmıştır (ilanı bayat ya da bağı kullanılmaz). Yeni tasarım bu anda ardılı zaten bırakırdı.

**Sınıflar** (her telemetri kaybı birine girer):

| sınıf | koşul (karar anında) | ulaşan aile |
|---|---|---|
| J1 · katmanın işi | alıcı E ya da G, j geçit değil; ardılın kanıtı var ve en iyi O adayı temiz | B2–B4, kendiliğinden |
| J2 · kanıt geç | alıcı E ya da G, j geçit değil; ardılın kanıtı yok ve k1 temiz | B, D |
| J3 · aday kirli | alıcı E ya da G, j geçit değil; k1 var ama J1 ve J2 değil | C, D |
| J4 · tek aday | alıcı E ya da G, j geçit değil; k1 yok | — (yalnız bekletme) |
| J5 · hedef | j geçit, alıcı E ya da G | — |
| U1 · temiz alıcı, temiz aday | alıcı U, k1 temiz | D (genel bir B) |
| U2 · temiz alıcı | alıcı U, k1 yok ya da temiz değil | — |

J1 ile J2'nin ayrımı iki bildirim biçimiyle ayrı ayrı hesaplanır. Hüküm **anında** biçimle verilir: kanıt en erken geldiğinde bile kalan kayıp.

**Kâhinle ağırlık:** bir kaybın ağırlığı w, k1'in bağının p₇'sidir (k1 yoksa 0). Bu, paket bu atlamada k1'e gitseydi geçme olasılığının üst sınırıdır; kâhin ağın kendi girişimini görmez. J1'in ağırlığı en iyi O adayının p₇'sidir. Bir sınıfın ağırlıklı payı Σ w / açık dönemde doğan paket.

## Karar kuralı (`sonuc_hesap.py`)

**K0 · Geçerlilik.**
- 16 koşu kayıtta, hepsi geçerli, iç denetimler geçti.
- Birebirlik: satırlar yeni çekirdek ölçümünün `eğim0` satırlarıyla (`arsiv/teshis/faz5_3_yeni_cekirdek_2026-11-19/kayit_egim0_{ikiz,birincil}.json`; aynı kol, aynı tohum) aynı. Karşılaştırılanlar: PDR, pencere PDR'si, üretilen, teslim, simülatör sayaçları, protokol sayaçları.
- Kaydedicinin kaybı, kayıp anatomisinin `dogum_evre_dusen`'iyle aynıdır (iletim başarısızlığı, açık doğum, alan başına).

Tutmazsa tablolar kullanılmaz, sebep ölçülür.

**K1 · Kaybın yeri (S1).** Birincilde, sekiz tohumun ortalaması ve tohum başına:
- J1–J5 ile U1–U2'nin payı (ham ve ağırlıklı) ve komut kaybı.
- **Elemeler** (ağırlıklı pay, anında biçim):
  - **B:** J2 < 0,02 ise B (karıştırmaya karşı hızlı sapma) elenir;
  - **C:** J3 < 0,02 ise C elenir;
  - **D:** J2 + J3 + U1 < 0,02 ise D elenir.

  A hiç elenmez. Elenmeyen aileler, S3–S5'in sayılarıyla ana seçeneğin kararına girer.
- **Hedefe yeter mi** (betimleyici): J1 + J2 + J3 (ağırlıklı), gereken 0,048 ile yan yana.

**K2 · Zaman (S2), betimleyici.** J1 + J2'deki kayıplar için:
- kararın dönem başından ve alıcının alana girişinden gecikmesi;
- J1'de kanıtın başlangıcından gecikmesi;
- ortanca ve çeyrekler; dönemin ilk 3 s'sinde olan kaybın payı.

**K3 · Hızlı sapmanın tetiği (S3).** Tetikler ardıla giden veri kayıtlarından alınır; kendi aralıklarıma düşen kayıtlar sayılmaz. Tetik, son kaydın (ya da son iki kaydın) kötü olduğu her kayıtta ateşlenir (kayan):
- **DEN7x1:** bir tam denemeli kayıt (7 deneme: onay son denemede geldi ya da vazgeçildi);
- **VAZ1:** bir vazgeçme;
- **DEN7x2:** art arda iki tam denemeli kayıt.

Her tetik W ∈ {1, 3} s'lik sapma süresiyle denenir, yani altı aday var. Tetikten sonraki W s içinde aynı bağa düşen kararlar k1'e giderdi.
- **Yakalama:** J2'nin (anında) ağırlıklı payından sapma süresine düşenlerin oranı.
- **Temiz sapma:** temiz kararların sapma süresine düşen payı. Temiz karar: ikizde her karar; birincilde önce ve sessiz evredeki kararlar ve açık evrede alıcısı U olanlar. İki hücre birlikte sayılır.
- **Seçim** (seçim yarısında): temiz sapması ≤ %2 olanlardan yakalaması en büyüğü; eşitlikte temiz sapması küçük olan. Hiçbiri ≤ %2 değilse hüküm "tetik yok".
- **Doğrulama:** seçilen adayın doğrulama yarısında temiz sapması ≤ %2 ise "doğrulandı". Yakalama raporlanır.
- **Betimleyici:** sapan temiz kararlarda k1'in bandının ardılınkinden kötü olduğu pay.

**K4 · Kopyanın bedeli (S4), betimleyici.** İki kural:
- **C1:** ardılın kanıtı var ve k1 var;
- **C2:** ardılın kanıtı var, O adayı yok, k1 var (S).

Her biri için raporlananlar:
- ateşlediği kararların payı, evreye ve alıcının alanına göre;
- ekleyeceği yayın süresi: Σ (`E_selam`(i, k1) + C(k1) / 64) · bir veri çerçevesinin 1 Mb/s'deki süresi, koşunun veri yayın süresine oranla;
- kapsadığı kayıp, sınıfa göre.

**K5 · Kurtarmanın kestirimi (S5), betimleyici.**
- J2 + J3 + U1'in ağırlıklı payı (K1'in D satırı) ve sınıflara dağılımı.
- Ekleyeceği yayın süresi: koşudaki her vazgeçmede (bütün evreler, bütün telemetri kararları) k1'e bir gönderim. Bedeli `E_selam`(i, k1) · çerçeve süresidir; veri yayın süresine oranla raporlanır.

**Hükmün karara etkisi:**
- **Üç aile de elenirse:** B5'in çekirdeği A (tek yol) olur. Karıştırmaya özgü kazanç B2–B4'ün payından (J1) beklenir; B5'in karıştırma eki boş kalır.
- **B elenmezse:** K3'ün tetiği B'nin kâğıdının girdisidir. Hüküm "tetik yok" ise B'nin temiz kanaldaki bedeli yüksektir; bu da kararın girdisidir.
- **C elenmezse:** K4'ün yayın kestirimi kararın girdisidir.
- **D elenmezse:** kurtarma simülatörün yetenek sözleşmesini (`13`) genişletir. Bu bir kapsam kararıdır (`05` §7'nin yolu, K kaydı, regresyon); K5 girdisidir.
- Elenmeyen ailelerden ana seçeneği ben seçerim; birden çoğu birlikte seçilebilir.

**Eşiklerin gerekçesi:**
- **0,02 (`PDR_açık`):** mekanizma kapısının ve koruma ölçütlerinin eşiği (`v2/18` §1.1). Ağırlıklı pay bir üst sınırdır. Bir ailenin ulaşabileceği pay bunun altındaysa, katkısı Aşama 4'te ayırt edilemez.
- **%2 temiz sapma:** temiz kanalda 100 karardan en çok 2'si ikinci adaya gider. İkizde `eğim0`'ın atlama başına başarısızlığı %1,83 (yeni çekirdek ölçümü §6). Sapan paketin kaybı iki katına çıksa bile bedel 0,0004'ün altında kalır.
- **p₇ ≥ 0,90:** kayıp anatomisinin "iyi" bandı.
- **W 1 ve 3 s:** 1 s, saniyede bir telemetri üreten uç düğümde bir pakettir. 3 s, B2'nin girişim kuralının yakalama penceresidir.

## Öngörüler (bu teşhisin hiçbir koşusundan önce)

Gerekçe:
- **Alanların payı biliniyor.** Yeni çekirdek ölçümünün `eğim0` kayıtları aynı kod ve tohumdan; K0 aynısını verir: E 0,048 · G 0,168 · U 0,081.
- **B2 teşhisi:** girişim kuralı 3 s içinde %34–35, dönem içinde %53–55 yakalıyor. Bit uzak bir komşuya selam başına 0,35 olasılıkla ulaşıyor. DEN7x3 3 s içinde G alanında %18–21, E alanında %27–35 yakalıyor.
- **Teşhis (d):** karıştırılan alıcıya çerçeve başına deneme 3,9 (G) · 6,3 (E).
- **Yapı:** formasyonda geçide medyan 2 atlama (`04` §2). Geçide sonlu bağı olan her komşu için geçit uygulanabilir bir adaydır (maliyeti 0).

| # | öngörü |
|---|---|
| 1 | K0: birebirlik tutar, iç denetimler geçer; kaydedicinin kaybı anatomiyle aynı |
| 2 | Anatominin alanıyla kayıp E 0,048 · G 0,168 · U 0,081 (birebir) |
| 3 | Karar anındaki alanla J1–J5 toplamı 0,19–0,216, U1 + U2 0,081–0,11 |
| 4 | J5 ≤ 0,01, en olası < 0,005 |
| 5 | E + G'deki kayıpta k1'in temiz olduğu pay %30–60. J1 + J2 0,06–0,13 · J3 0,04–0,10 · J4 0,02–0,06 |
| 6 | J1 0,02–0,07 · J2 (anında) 0,03–0,08 · J2 (gerçekçi), J2 (anında)'dan 0,00–0,03 fazla |
| 7 | U1 0,04–0,07 · U2 0,015–0,04 |
| 8 | Ağırlıklı pay: J2'de hamın %90'ından fazlası; J3'te hamın %20–60'ı |
| 9 | Elemeler: en olası B elenmez, D elenmez; C belirsiz (iki yön de olası) |
| 10 | Hedefe yeter mi: J1 + J2 + J3 (ağırlıklı) 0,06–0,20; en olası 0,048'i aşar |
| 11 | K2: J1 + J2'nin dönemin ilk 3 s'sindeki payı %20–40; alana girişten gecikmenin ortancası 3–8 s |
| 12 | K3: DEN7x1 ve VAZ1, W 3 s'de temiz sapma sınırını aşar. En olası seçim DEN7x2, W 1 s; "tetik yok" olasılığı ~%30. Seçilenin yakalaması %10–40 |
| 13 | K4: birincilde açık evre kararlarının C1'de %5–20'si, C2'de %1–6'sı ateşler. C1'in yayın eki veri yayın süresinin %1–8'i, C2'ninki %0,3–2'si. İkizde iki kural da kararların %1'inden azında |
| 14 | K5: kurtarmanın yayın eki birincilde veri yayın süresinin %2–6'sı |
| 15 | Koşu başına telemetri kararı 35 000–45 000; birincilde açık doğumlu kayıp 800–1 400 |

## Aletin denetimi

- **Saf işlevler:** `sinama/saf.py`. Denetlenenler:
  - B2'nin durumu ve kendi aralıklar;
  - selamın biti ve bildirimin iki biçimi;
  - gönderici sebebi (DEN7x3, uzatma, ömür, kendi aralığımda ayıklama);
  - veri yok;
  - uygulanabilirlik ve tur taşması;
  - ilanın ömrü;
  - adayların sırası ve k1;
  - sınıflar;
  - tetikler ve sapma süreleri.
- **Mekanik denetim:** öngörüler yazıldıktan sonra yapılır. Ölçülen tohumların dışındaki 1001 tohumuyla, kısa pencerede, iki hücrede bir kez koşulur. Bakılan tek şey iç denetimlerin geçmesi ve karar hesabının hatasız bitmesidir; sayılar okunmaz.
- **Duman** (bu commit'ten sonra): kısa pencere, tohum 1003, iki hücre, kaydediciyle. Satırlar yeni çekirdek ölçümünün duman kaydındaki `eğim0` satırlarıyla (`arsiv/teshis/faz5_3_yeni_cekirdek_2026-11-19/duman/kayit_duman_{ikiz,birincil}.json`) birebir olmalı. Duman notu ayrı commit'le girer; karar girdisi değildir.

## Süre ve kayıt

- **Adım başına** (bir hücre, 8 tohum, 8 işçi): ~1,5–2,5 saat.
  - Dayanak: yeni çekirdek ölçümünde `eğim0`'ın adımları ikiz 51 dk, birincil 65 dk sürdü.
  - Bu kayda B2'nin saniyelik işaretleri, B1'in sayımı (bütün bağlarda) ve her kararda adayların hesabı eklenir. B3 teşhisinde benzer bir özet adımı ~1–1,9 saate çıkarmıştı.
- **Toplam:** ~3–4,5 saat. Dumandan sonra yeniden kestirilir. İki ağır iş birlikte koşulmaz.
- **Kayıt:** `kayit_<hücre>.json.gz`, ara kayıt `kayit_<hücre>.jsonl.gz` (sıkıştırılmış).

## Sınırlar

- **Görünüm bugünkü kodun trafiğinden hesaplanır.** Yeni tasarımda ardıl kanıtla değişince sonraki trafik de değişirdi; burada değişmez. J1, kanıttan sonraki kayıpların hepsini katmana yazar; B3'ün 5 s'lik yeniden denemesi de bir miktar kayıp doğururdu.
- **Bit, gerçekçi biçimde bugünkü kodun selam zamanlamasıyla gelir.** Yeni tasarımda "bit değişti" selamı hemen gider (B2 Ö-2). Hüküm bu yüzden anında biçimle verilir.
- **Kendi aralıklarım geriye dönüktür:** karar anında henüz bilinmeyebilir (en çok 2 s). Hesap tam aralıkları kullanır.
- **Ağırlık kâhindendir:** ağın kendi girişimini saymaz, k1'in geçide kalan yolunu görmez. Ağırlıklı pay bu yüzden bir üst sınırdır.
- **Kuralların kâğıdı yok:** sapma, kopya ve kurtarma kuralları burada yalnız ulaşılabilecek payı ve kaba bedeli kestirmek için tanımlıdır.
- **Kapsam:** yalnız formasyon kolu ve sürekli karıştırıcı ölçülür. Dayanıklılık hücresi ve yer karıştırıcılı aile ölçülmez.
