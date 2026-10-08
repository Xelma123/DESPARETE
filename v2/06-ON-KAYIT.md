# 06 · ÖN-KAYIT TASLAĞI

> **Durum:** taslak — mühürlenmedi; mühür Faz 6'da (~12 Kasım, `12`). Bağlayıcı hükümler (§0.2, §0.4.1–0.4.2, §4.4, §7) değişmez; mühürden sonraki her değişiklik §10'a tarihiyle yazılır. Güncel: 9 Ekim 2026 — birincil metrik `PDR_açık`a, karıştırmaya özgü kazanç ve mekanizma kapısı §0.4.5'e (K-222, denetim D-01); §4.4/3 uygulanan kurala çekildi ve Faz 4'te sonuçtan sonra değişen ölçütler §10'a yazıldı (D-06). Önceki sürümler `arsiv/06-ON-KAYIT-*.md`.

---

## 0 · Temel kavramlar

**0.1 · Faz ≠ aile.** Faz bir iş dönemidir (`12`; değişebilir). Aile bir çoklu karşılaştırma düzeltme birimidir: Holm–Bonferroni aile **içinde**; mühürden sonra değişmez.

**0.2 · Mühür neyi korur** — hipotez, eşik ve analiz planı sonuç görülmeden yazılır:
1. **Ana deney tohumlarıyla (2000–2039) mühürden önce hiçbir protokol koşulmaz** (yalnız bölünme denetimi için kanal grafikleri kuruldu, K-132).
2. **Eşikler rakiplerin gürültüsünden türer:** türetme formülü özgün protokolün ilk koşusundan önce yazılır; değeri taban protokollerin geliştirme tohumlarından hesaplanır.
3. **Parametreler mühürde sabitlenir:** rakipler RFC varsayılanında; özgün protokol mühür anındaki değerlerinde; hiçbir kol senaryoya göre ayarlanmaz.

**0.3 · Sıra:** taban protokoller yazılır, uygunluk testlerini geçer ve donar → eşiklerin türetme formülü, güç yöntemi ve aday birincil hücre özgün protokolün ilk koşusundan ÖNCE yazılır (yapıldı, §0.4) → özgün protokol geliştirme tohumlarında geliştirilir (Faz 5) → δ gürültüsü ölçülür → **MÜHÜR** (hipotezler · eşik değerleri · parametreler · tohum sayısı · birincil hücre) → ana deney. Formül önceden yazılı ve değeri rakiplerden geldiği için güvenli; birincil hücre mühürde değişirse gerekçesiyle kaydedilir ve hipotez keşifsel etiketlenir.

### 0.4 · Adım 3 — özgün protokolün ilk koşusundan ÖNCE yazıldı (23 Eylül 2026, K-153) — BAĞLAYICI

Yalnız Aile 2 (üstünlük) ve Aile 3 (mekanizma) için; Aile 1 yalnız taban protokolleri kapsar.

**0.4.1 · Birincil testler.** Rakip başına bir: **H2.a** DESPARETE ↔ AODV · **H2.b** ↔ OLSR · **H2.c** ↔ AOMDV — `m = 3`, Holm aile içinde. Her biri birincil hücrede, birincil metrikte, 40 ana deney tohumunda eşleştirilmiş, çift yönlü Wilcoxon. Gecikme ve kontrol yükü betimleyici (güven aralığıyla).

**0.4.2 · Eşiğin türetme formülü — serbest sabit yok.** Birincil hücrede, yalnız taban protokollerle, geliştirme tohumlarında (`G` = 1100–1119; ana deneyle kesişmez):

    d_XY(s) = M_X(s) − M_Y(s)          X, Y ∈ {AODV, OLSR, AOMDV}, s ∈ G
    SD_ref  = max( SD(d_AODV,OLSR) , SD(d_AODV,AOMDV) , SD(d_OLSR,AOMDV) )
    δ       = 2 · SD_ref / √n          n = ana deney tohum sayısı (40)

`M` birincil metrik. δ, projenin çözünürlük tanımının (`R = 2 · SD / √n`) gerçek rakiplerle eşleştirilmiş hâli; en gürültülü çift alınır. Özgün protokolün hiçbir koşusu δ'ya girmez.

| H2.x'in hükmü | koşul |
|---|---|
| **üstün** | Holm'dan sonra p < α = 0,05 **ve** eşleştirilmiş ortalama fark ≥ δ, DESPARETE lehine **ve** mekanizma kapısı geçer (Aile 3; kapı mühürde, ablasyon bayraklarıyla) |
| **aşağı** | aynı iki sayısal koşul ters yönde — negatif sonuç olarak raporlanır |
| **ayırt edilemedi** | geri kalan her durum; dışlanan etki (%95 GA uçları) ve ulaşılan güç yazılır |

δ koşulu Wilcoxon'un anlamlılığından ayrıdır (sıra testi çarpık dağılımda küçük ortalama farkı da anlamlı bulabilir).

**0.4.3 · Güç yöntemi** (Aşama 4 başında): (1) gürültü dağılımı = §0.4.2'nin `d_XY(s)` farkları, her çift kendi ortalamasından arındırılmış; DESPARETE'nin geliştirme farkları varsa YALNIZ yayılımları havuza girer, ortalama farkı hiçbir yerde kullanılmaz · (2) her Δ için `B = 2 000` örneklem: gürültüden yerine koyarak `n` fark, Δ eklenir, çift yönlü Wilcoxon, ret `p < α / m` (muhafazakâr); güç = ret oranı · (3) çıktı `MDE₈₀` ve δ'daki güç · (4) **tohum kuralı:** `MDE₈₀ > Δ_hedef` ise mühürden ÖNCE `n' = ⌈n · (MDE₈₀ / Δ_hedef)²⌉`, sonra yeniden · (5) tümü sıfır farklar için NaN tuzağı denetlenir. *Ön tahmin — eski dünyada* (normal gürültüyle, `n = 40`, `α/m = 0,05/3`): güç δ'da 0,31, 1,7·δ'da 0,81 → `MDE₈₀ ≈ 1,7 · δ`; eşleştirilmiş çözünürlükle (~0,023) `MDE₈₀ ≈ 0,039 < Δ_hedef`. Referans dünyada Faz 6'da yeniden. Üretici: `python arsiv/teshis/guc_on_tahmin_2026-09-23/guc.py`.

**0.4.4 · Aday birincil hücre** (öğrenci kararları 23 ve 26 Eylül, gerekçesi 28 Eylül — K-153, K-186, K-192): **`formasyon · yere_toplama · derin_sizma · sürekli`, karıştırıcı 10 W toplam ortalama · birincil metrik `PDR_açık` (§3; K-222) · `Δ_hedef = 0,05`.** Pencere PDR'si betimleyici kalır: ölçüm penceresinin yalnız %33'ünde karıştırıcı açık ve DESPARETE v0.4.1'in üstünlüğü karıştırıcısız kollarda da var (denetim D-01). Araç yalnız sessizken taşınır; ölçüm penceresinde ~1,3 km → fiilen merkezde, 15 s açık · 15 s sessiz, açıkken 20 W. Sınanan: periyodik açılıp kapanmaya zamansal uyum ve kısmi karıştırmada dolaşma. İlk aday (23 Eylül, eski dünya) `hava_eslik`ti; referans dünyada kaynaklı gücünde (1–5 W) sürüyü her geometride böldüğü için bırakıldı, keşifsel eksen. ⚠️ Δ_hedef eski dünyanın taban protokol farklarından seçildi; Faz 6'da referans dünyanın δ ve gücüyle birlikte yeniden değerlendirilir.

**0.4.5 · Karıştırmaya özgü kazanç ve mekanizma kapısı** (9 Ekim 2026, K-222 — DESPARETE'nin ilk koşularından SONRA yazıldı; yönü DESPARETE aleyhine tutucu, §10):
- **İkincil test — fark-içinde-fark.** Her H2.x çifti için aynı 40 tohumda karıştırıcısız ikiz hücre (`formasyon-yok`, aynı desen) koşulur; "açık" orada aynı çizelgenin hayalet dönemleridir. `DiD(s) = [PDR_açık(D) − PDR_açık(R)]_birincil − [PDR_açık(D) − PDR_açık(R)]_ikiz`; eşleştirilmiş çift yönlü Wilcoxon (DiD ↔ 0), Holm üç rakiplik ailede (`analiz/hucre.py::fark_icinde_fark_tablosu`). Eşiği (δ_DiD) mühürde §0.4.2'nin formülüyle ikiz hücrenin gürültüsünden.
- **Mekanizma kapısı (Aile 3, H2.x "üstün" için şart).** Karıştırmaya özgü mekanizmalar (Faz 5.1 karıştırma kanıtı · 5.3 postür · 5.4 PROTECT; bayrak adları Faz 5'te kesinleşir) birlikte kapatılınca birincil hücrede `PDR_açık` tam DESPARETE'ye göre anlamlı düşmeli (eşleştirilmiş Wilcoxon, aynı 40 tohum). Geçmezse hüküm "fark var, karıştırmaya özgü mekanizmaya bağlanamadı".
- **İddia dili.** H2.x "üstün" → *karıştırma altında daha yüksek teslim*. *Karıştırmaya özgü kazanç / karıştırmayı çözer* ancak H2.x üstün **ve** DiD anlamlı pozitif **ve** mekanizma kapısı geçerse söylenir.
- **Dayanıklılık hücresi** (denetim D-08): birincil hücrenin aynısı, çizelge 10 s açık · 20 s sessiz (ortalama güç korunur); `PDR_açık` ön-kayıtlı ikincil test. DESPARETE'nin zaman sabitleri tek bir 15/15 çizelgesine ayarlanmış olmasın diye; Faz 5'in geliştirme setinde de bulunur.

## 1 · Aileler

| aile | soru | birincil test |
|---|---|---|
| **1 · karakterizasyon** | taban protokoller karıştırma altında nasıl bozuluyor | mühürde |
| **2 · üstünlük** | özgün protokol rakiplere göre ne yapıyor | §0.4 |
| **3 · mekanizma** | kazanç hangi mekanizmadan geliyor | mühürde |

Her hipotezin tek birincil testi (hücresi) vardır; diğer hücreler betimleyici, güven aralıklarıyla tam raporlanır. Liste kısa tutulur (her yeni hipotez diğerlerinin eşiğini yükseltir). Hipotez sonuç görüldükten sonra aileler arasında taşınamaz.

## 2 · Tohumlar

| küme | tohumlar | ne için |
|---|---|---|
| kalibrasyon ve geliştirme | 2000–2039 dışındaki her tohum (U1: 1000–1002; DESPARETE geliştirme: 1003–1010; δ'nın gürültüsü: 1100–1119) | kalibrasyon · uygunluk · gürültü · özgün protokol geliştirme |
| **ana deney** | **2000–2039** — 40 tohum (öğrenci, 10 Eylül) | rapora giren sonuçlar |

1000–1029 eski simülatörde ana deney için görüldüğünden ana deney tohumu olamaz.

## 3 · Metrikler

**Sunum üçlüdür:** teslim · gecikme · kontrol yükü; tek metrikle sıralama yapılmaz.

| metrik | tanım |
|---|---|
| PDR | ölçüm penceresinde doğan paketlerin teslim oranı (doğum kohortu). U1 tüm koşu PDR'sini kullanır (öğrenci, 25 Eylül) |
| **PDR_açık** | **birincil metrik** (K-222): karıştırıcının açık dönemlerinde doğan paketlerin teslim oranı, ölçüm penceresinde (evre sözlüğünün `pdr_acik`ı; `analiz/satir.py::donem_pdr` ham listeden ikinci gerçekleme). Karıştırıcısız ikizde aynı çizelgenin hayalet dönemleriyle |
| PSR | bağ düzeyi: hedef alıcının CRC'den geçirdiği veri iletimi / veri iletim denemesi (öğrenci tanımı; K-115) |
| gecikme | **ortak alt küme** üzerinden; p50 · p95 · p99; kesişim oranı her zaman raporlanır (hayatta kalan yanlılığı) |
| kontrol yükü | bayt ve kanal süresi; NRL (çerçeve · bayt · airtime) pencere ikiziyle. İkiz `[pencere başı, pencere SONU)` — sayaçlar pencerede donar (K-130; boşalmayı sayan eski tanım NRL'yi aileye göre farklı ~%10 şişiriyordu). `nrl_bayt/airtime` payı = kontrol + protokolün **veri başlığı** (K-151) |
| kopma | fiziksel · protokolün algıladığı · rota geçersizleşmesi; algılama duyarlılığı (fiziksel sayım çalkantıyı ölçer, karıştırmayı değil) |
| Δ · COR | kopmadan kurtarmaya süre · kurtarılan / açılan döngü |
| evre | şok derinliği · toparlanma tamlığı · toparlanma süresi · tespit gecikmesi (`08`) |

Analiz birimi tohumdur; havuzlanmış okuma yalnız betimleyici.

## 4 · Taban protokoller ve uygunluk

**4.1** AODV (reaktif, tek yol) · OLSR (proaktif, bağ durumu) · AOMDV (reaktif, çok yol). GPSR kapsam dışı (`01` §3). ⏳ AOMDV öngörüsü yeni tehdit modeline göre mühürden önce yeniden yazılır.

**4.2 · Parametreler — RFC varsayılanı.** AODV (RFC 3561): HELLO_INTERVAL 1,0 s · ALLOWED_HELLO_LOSS 2 · ACTIVE_ROUTE_TIMEOUT 3,0 s · RREQ_RETRIES 2 · NODE_TRAVERSAL_TIME 40 ms · NET_DIAMETER 35. OLSR (RFC 3626): HELLO_INTERVAL 2,0 s · NEIGHB_HOLD_TIME 6,0 s · TC_INTERVAL 5,0 s · TOP_HOLD_TIME 15,0 s · WILLINGNESS 3 · MAXJITTER HELLO_INTERVAL/4. HELLO aralıkları eşitlenmez; kontrol yükü farkı raporlanır. Her protokol kendi HELLO'sunu kullanır.

**4.3 · Dört uygunluk testi**

| # | test | beklenen |
|---|---|---|
| U1 | karıştırıcısız, bağlı ağ | kâhin referansına oran (aşağıda) |
| U2 | tek bağ koptuğunda | AODV RERR + yeni RREQ; OLSR NEIGHB_HOLD_TIME dolunca günceller |
| U3 | karıştırma ve hareket yok | OLSR yükü periyodik; AODV yükü yalnız keşifte |
| U4 | olay izleri | RFC'nin mesaj sırası ve zamanlayıcıları |

**U1 ölçüsü** (K-136): `oran = PDR(protokol) / PDR(EnGuvenilirKahin)`, AYNI konfigürasyonda; 🔒 **statik ≥ 0,90 · hareketli ≥ 0,60**. Oran biçimi "bağlı ağ" ön koşulunu nötrler. ⚠️ **Eşik ölçüm görüldükten SONRA seçildi** (öğrenci) — U1 bir kabul kapısıdır, hipotez testi değil; eşik üç taban protokolü birden bağlar. Kapının yapı yarısı `tests2/` (kâhin aşılmıyor, defter kapanıyor), sayısal yarısı `kalibrasyon/aodv_uygunluk.py` (dört `-yok` kolu × 1000–1002, tam pencere; verdikt çıkış kodunda). Karıştırıcısız kâhin tavanı referans dünyada statikte 0,99–1,00, hareketlide 0,84–0,98 (yakınsamış kâhin, K-217; eski dünyada 0,996–1,000 · 0,84–0,92).

**U3 bulgusu** (K-144, öğrenci: bulgu olarak raporla; eski dünyada): "AODV yükü yalnız keşifte" tutmadı — 60 → 120 s kontrol oranı AODV 2,070 · OLSR 2,130 · AOMDV 2,310 (`python -u kalibrasyon/aodv_uygunluk.py u3`). Kayıplı, yüklü ağda tepkisel ailenin "rotayı bulunca susar" avantajı kayboluyor (H1.1 için bulgu).

### 4.4 · Sadakat protokolü

1. RFC parametreleri önceden yazılır (§4.2). 2. Hiçbir parametre senaryoya göre değiştirilmez.
3. U1–U4 koşulur. 🔒 **U1 iki parçadır** (K-137): **U1-U · uygunluk** — keşif tamamlanıyor · çok atlamalı teslim · korunum kapanıyor · kâhin aşılmıyor → kalırsa protokol KABUL EDİLMEZ. **U1-B · başarım** — oran eşiği → protokol reddedilmez ama eşik altı hücre **ölçümle açıklanmadan geçilemez** (kayıp yazılım kusurundan değil mekanizmadan). Açıklama "bilinen kusurlar düzeltildikten sonra hâlâ düşük" demektir; kusur yokluğunu kanıtlamaz (K-145). 🟢 **Kâhin aşımı** (KR-1, K-192 — öğrenci onayı 28 Eylül): aşım otomatik ret değil. Protokol ETX kâhinini çözünürlükten (R) fazla aşarsa üç kâhinin zarfına (üst referans) bakılır; zarfı da aşıyorsa yazılım hatası varsayılır ve aranır; aşmıyorsa "ETX kâhini bu hücrede üst sınır değil" diye beyan edilir (K-110). **Tasarım bedeli** (K-192): eşik altı hücre, mekanizması ölçülmüş ve kusur adayları (kuyruk/tampon düşüşü, bayat rota, kötü bağ seçimi) dışlanmışsa açıklanmış sayılır; mekanizmanın hücreleri doğru sıralaması aranır. **Faz 4'ün iki istisnası (sonuçtan sonra, öğrenci, §10):** OLSR'da sıralama koşulu sağlanmadan "açıklanmış, sıralamasız" (K-196) · kaynağına kural kural sadık bir protokolün eşik altı kalması — RFC kurallarından doğan geçici döngüler dâhil — protokolün kendi sınırıdır (K-207). U1 eşiği referans dünyada da değişmez.
4. Modellenmeyen özellikler ve sapmalar beyan edilir — **tek kaynak** her protokolün biçim dosyasındaki tablo (`protokoller/aodv_bicim.py` · `olsr_bicim.py` · `aomdv_bicim.py`/`aomdv.py`); özeti `04` §5. Kural: SHOULD uygulanır, MAY beyan edilir; gerekçesiz sapma düzeltilir (K-207, K-208).
5. Ana deneyde parametreler sabittir. Aynı disiplin özgün protokole uygulanır.

## 5 · Hipotezler — taslak

**5.1 · Aile 1** (hücreler, eşikler, birincil testler mühürde):
- **H1.1 · Protokol ailesi bozunumu belirler** — reaktif ve proaktif aynı karıştırmada farklı kayıp yaşar. Mekanizma kontrolü: kontrol düzlemi davranışı ayrıca gösterilir; desen yoksa sonuca bakılmaz. Yanlışlanma: farkın %95 GA'sı sıfırı içerir ya da mekanizma kontrolü geçmez.
- **H1.2 · Çöküş dirseklidir** — şiddet tarandığında teslim dirsekle düşer. Tarama aralığı tohum SD'sinin ≥ 3 katı değilse test edilmemiş sayılır; bağ PER eğrisinin dirseğiyle çakışırsa dirsek radyo modelinindir. Çoklu karıştırıcıda şiddet = toplam güç.
- **H1.3 · Yapı güçten önemlidir** — aynı ortalama güçte darbeli ↔ sürekli farklı kayıp; ölçülmüş kontrastlar darbeli ↔ sürekli ve aldatıcı ↔ sürekli (fark CSMA görünürlüğü + en çok 0,008 PER artığı).
- Ölçülmüş tahminler: taramalı konak süresi (100 ms) en hızlı zamanlayıcıdan kısa · taramalının ortalama gücü 4,77 dB düşük ("taramalı zayıf" mekanizmaya yazılamaz) · aldatıcı ↔ sürekli farkı saf CSMA değil.
- 🔵 Aday sorular: hareketli karıştırıcıda Δ protokol ailesine göre farklı mı (boşluk B) · karıştırıcı geçit çevresindeyken çok yollu protokolün yedekleri aynı anda mı kesiliyor.

**5.2 · Aile 2 — biçim.** H2.x: özgün protokol [AODV | OLSR | AOMDV] ile birincil hücrede `PDR_açık` bakımından ön-kayıtlı eşiği geçen bir fark üretir. Yanlışlanma: %95 GA sıfırı içerir **ya da** fark ters yönde **ya da** mekanizma kapısı geçmez. Sayısal hüküm §0.4.2; karıştırmaya özgü kazanç iddiası ve iddia dili §0.4.5.

**5.3 · Aile 3 — mekanizma.** Kol kendi ablasyonuna karşı okunur; eşleştirilmiş fark tohumların büyük çoğunluğunda pozitif ve %95 GA sıfırı dışlamalı; sayaçlar karar başına oran. Eski ölçüt (komşuların bildirdiği bilginin permütasyonu, m = 5 null) DESPARETE'nin bayraklarına göre mühürden önce yeniden yazılır (açık, `12`).

## 6 · Özgün protokol — DESPARETE

Tasarım öğrencinin (`protokol_kaynaklari/DESPARETE_TASARIM_PAKETI/`, tek okuma `36`); gerçekleme kararları K-150…K-172 (`kayit/KARAR-GUNLUGU.md`). Bugünkü varsayılan **v0.4.1** = bayrak profili `PROFIL_V02` + seçenekler `SECENEK_V041` (K-172); Faz 5'te v0.5'e gelişir. Sekiz ablasyon bayrağı (K-159; güvenlik değişmezleri bayrakla kapanmaz); hangilerinin Aile 3'te kol olacağı mühürde seçilir. Şartlar: kâhin bilgisi yok (`05`) · derin öğrenme yok · parametreler mühürde sabit · durum tutan her bileşende başlangıç koşulu sorulur. Tuzaklar: literatürdeki kâhinli ödül kodu kopyalanmaz (`02` §L) · gürültünün mutlak değeri anlamlı değil, karıştırma oranla ya da değişimle sezilir (K-110 EK-4).

## 7 · İstatistik planı

| konu | plan |
|---|---|
| tohum | 40, tüm kollarda aynı küme (2000–2039) |
| eşleştirme | ayrık rastgelelik → aynı tohum aynı senaryo; kanal rastgeleliği hash'ten (hangi protokol koşarsa koşsun aynı iletim aynı gerçeklemeyi görür) |
| test | Wilcoxon işaretli sıralar, çift yönlü |
| düzeltme | Holm–Bonferroni, aile içinde, yalnız birincil testlere |
| α | tek α = 0,05; evre metriklerinin anlamlılık sabiti buradan (`08`) |
| raporlama | etki büyüklüğü + güven aralığı; negatif sonuçta dışlanan etki ve ulaşılan güç |
| güç | §0.4.3; tohum mühürden önce artırılabilir, sonra artırılamaz |
| durdurma kuralı | mühürde mutlak birimle yazılır (eski göreli kural sıfıra yakın farklarda tanımsızdı) |

**NaN tuzağı:** `scipy.stats.wilcoxon` tüm farklar sıfırken NaN döndürür ve Holm'dan sonra bütün p'leri 1,00 yapar — test öncesi açıkça denetlenir.

## 8 · Bir sonucun geçerlilik koşulları — dördü birden

| # | koşul | nasıl |
|---|---|---|
| 1 | koşu uzunluğundan bağımsızlık | yön (işaret testi) ve büyüklük (GA uçları ≤ k × tohum SD; k güç analizinde); ısınma ve ölçüm penceresi birlikte taranır |
| 2 | metriğin ne ölçtüğü doğrulanmış | evre kapıları (`08`); PSR için kapı 🔵 |
| 3 | gizli asimetri yok | HELLO aralıkları · beacon · kapsülleme · veri onayı · beyan kanalı kancalarda (K-134) · bekleme tamponu ortak (K-131, K-198) · AODV/AOMDV kara listesi uygulanıyor (K-194) |
| 4 | regresyon testi | sonucu üreten kodun testi |

## 9 · Mühürden önce kapanması gerekenler

- [x] Taban protokoller dondu (K-218: `AODV-j` · `OLSR-c` · `AOMDV-f`; U1 iki desende, yakınsamış kâhinle). U2–U4 AODV ve OLSR'da 🟢 · AOMDV'nin U1–U4 karşılıkları 🟢 (K-194)
- [ ] OLSR'ın kural kural sadakat denetimi (denetim D-02, `OLSR-d`) ve MAC deneme sayısının 7'ye düzeltilmesi (D-10) — kod K-223'te ✅ → regresyon · U1 · R · evre kapıları; ardından taban protokoller yeniden donar
- [ ] çözünürlük R ve DUYARSIZ hükümleri ana deneyin penceresinde (bugünküler 50 s'lik kesitte, denetim D-03) · Faz 7 hesap bütçesi ve düşme sırası (D-09)
- [ ] SINANMAMIŞ = 0 ve duyarlılık borcu = 0 — ya da borçlular eksen olarak ilan edilir (bugünkü sayım `04` §9'da)
- [x] §0.3'ün eşik formülü, güç yöntemi, aday birincil hücre (K-153)
- [x] düğüm kaybında birincil metrik (K-182) · referans dünyanın alanı ve birincil hücrenin sabitleri (K-185…K-188)
- [x] kâhin aşımı prosedürü (K-192) · U1 tüm koşu PDR'siyle, ana deney pencereyle · taban protokoller yere toplamada da sınanır
- [ ] **birincil metrikte komutlar (KR-2):** DESPARETE'nin komut taşıması V11 ile var; birincil PDR bütün trafik mi yalnız telemetri mi (öğrenci)
- [ ] δ ve güç referans dünyada · çözünürlük referans dünyada · tohum sayısı
- [ ] özgün protokolün parametreleri ve ablasyon bayrakları; Aile 3'ün mekanizma kapısı (DESPARETE'nin bayraklarıyla)
- [ ] Aile 1 hipotezleri ve AOMDV öngörüsü · durdurma kuralı · evre metriklerinin sabitleri ve pencere taraması
- [ ] mühür sırasının öğrenci onayı

## 10 · Kayıt tablosu

| tarih | ne | sonuç |
|---|---|---|
| 17 Ağu 2026 | Ç4.4 bandı — eski simülatör, koşulmadan önce ilan | tutmadı |
| 26 Ağu 2026 | Aile 3 null çekim sayısı m = 5 | yeniden değerlendirilecek (§5.3) |
| 1 Eyl 2026 | yeniden kurgu (K-081): faz/aile ayrımı · üç rakip · sadakat protokolü | — |
| 8–9 Eyl 2026 | Li replikasyonu ön-kaydı (`09`) | H1 tutmadı, H2/H3 tuttu |
| 10 Eyl 2026 | `sim2`ye göre yeniden yazıldı · tohum 40 · PSR tanımı · sabit mühür tarihi kaldırıldı · mühür sırası gevşetildi (K-113) | taslak |
| 17 Eyl 2026 | U1 eşiği ölçüm görüldükten sonra seçildi, beyanlı (K-136 · K-137); sonra değişmedi | taslak |
| 23 Eyl 2026 | §0.4 DESPARETE'nin ilk koşusundan önce (K-153) | taslak |
| 25 Eyl 2026 | bağımsız denetimin soruları §9'a (K-166); U1 tüm koşu PDR'si ve taban protokollerin yere toplamada sınanması kararları (K-167) · belge özlendi, hükümler değişmedi | taslak |
| 28 Eyl 2026 | belge temizliği: hükümler değişmedi; eski dünyanın anlatıları ayıklandı, §9 güncellendi | taslak |
| 26–28 Eyl 2026 | referans dünyada aday birincil hücre `derin_sizma` 10 W'a geçti (K-186; sebep fizik: hava karıştırıcısı sürüyü bölüyor — DESPARETE referans dünyada hiç koşmamıştı), gerekçesi düzeltildi (K-192) · KR-1 kapandı, U1 eşiği referans dünyada değişmez (K-192) · ⚠️ Δ_hedef (0,05) ve §0.4.3 güç ön tahmini eski dünyanın; δ ve güç Faz 6'da referans dünyada ölçülür | taslak |

| 28 Eyl 2026 | U1-B: OLSR'ın düşük hücreleri sıralama koşulu sağlanmadan "açıklanmış, sıralamasız" (K-196, öğrenci) | **sonuçtan sonra** — §4.4/3 |
| 30 Eyl 2026 | U1-B: kaynağına sadık protokolün eşik altı kalması, RFC kurallarından doğan geçici döngüler dâhil, protokolün kendi sınırı (K-207, öğrenci) | **sonuçtan sonra** — §4.4/3 |
| 2–6 Eki 2026 | evre kapısı G2ç'nin D maddesi kâhinin karıştırıcısız koşusuna eşlendi (K-212 → K-215); asıl sebep yakınsamamış kâhindi, yakınsamış kâhinle özgün ölçütle de geçti (K-217) | **sonuçtan sonra** — `08` §08 |
| 8 Eki 2026 | örnekleme denetimi C (aldatıcı ↔ sürekli) referansta ED dışarıda sorulur, 0/270 → 270/270 · G3 → G3ç, eski çekirdek hücre tabanda (K-219) | **sonuçtan sonra** — kapının referans biçimi |
| 9 Eki 2026 | birincil metrik pencere PDR'sinden `PDR_açık`a; fark-içinde-fark ikincil test; Aile 3 mekanizma kapısı; iddia dili; dayanıklılık hücresi (K-222, denetim D-01 · D-08) | **DESPARETE'nin K-200 koşularından sonra**; yön DESPARETE aleyhine tutucu (v0.4.1'in farkı açık evrede en küçük) |

Mühürden sonraki her değişiklik tarihiyle buraya yazılır ve ilgili hipotez keşifsel etiketlenir.
