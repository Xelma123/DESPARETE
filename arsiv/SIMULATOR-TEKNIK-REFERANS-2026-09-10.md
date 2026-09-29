# SİMÜLATÖR — TEKNİK REFERANS

> **Hazırlanma tarihi:** 10 Eylül 2026 · **Kapsam:** yalnızca `sim2/`,
> `kalibrasyon/`, `protokoller/`, `tests2/` — yani bugün var olan **kod**.
> **Amaç:** bu belge geçici bir çalışma dokümanıdır ("şu anlık bakmak için").
> `v2/*.md` serisi ve `DEVIR.md` projenin resmî, sürüm kontrollü belgeleridir;
> bu belge onların yerine geçmez, kodun kendisinden çıkarılmış **düz bir
> teknik dökümdür**. Kaynağı kod ve kodun docstring'leridir; bir karar kaydı
> (K-XXX) değildir, kimseye ölçüm sunmaz.
>
> Her başlık, o katmanın **ne yaptığını**, **neden öyle yapıldığını** ve
> **bugün hangi sayılarla çalıştığını** anlatır. Kodda hangi dosyada
> bulunduğunu görmek isteyen için dosya yolları köşeli değil, ters eğik
> çizgiyle (`sim2/...`) yazılmıştır.

---

## 0 · Otuz saniyede proje

Karıştırma (jamming) altındaki taktik İHA mesh ağlarında yönlendirme
protokollerini karşılaştıran bir **kesikli-olay simülatörü**. Ürün
öğrencinin kendi tasarlayacağı protokoldür; AODV, OLSR, AOMDV kıyas
tabanıdır. Bugün simülatör kalibre edilmiş durumda ama **hiçbir yönlendirme
protokolü henüz yazılmadı** — depodaki tek "protokol" gerçeklemeleri,
simülatörün kendi olay döngüsünü sınamak için yazılmış iki basit koşum
aletidir (`protokoller/kosum_kosumu.py`).

Kapsam cümlesi (öğrenci, 8 Eylül 2026): *"Kontrollü bir deney ortamında
routing protokolünün jamming karşısındaki davranışını izole etmek."*

Teslim: 19 Aralık 2026.

---

## 1 · Mimarinin altı ilkesi

Kod boyunca tekrar eden altı disiplin var; hepsi ölçülerek bulunmuş
kusurların üzerine kurulmuş yapısal çözümler:

1. **Tek kaynak, ikinci gerçekleme yok.** Bir büyüklüğün (çerçeve süresi,
   PER, sayaç adı, parametre köken kovası) hesaplandığı yer **tam olarak
   bir**dir. İkinci bir yerde aynı hesabı tekrarlamak, iki gerçeklemenin
   sessizce ayrışmasına yol açar — projenin geçmişinde bu birden çok kez
   gerçek kusur üretmiş (çerçeve süresi hesabı, sayaç listesi, yük
   muhasebesi).
2. **Ayrılmış rastgelelik.** İki tür kaynak var: **sıralı akışlar**
   (`cekirdek/rng.py::AKIS_ADLARI`, durum tutar, kurulumda tükenir) ve
   **hash alanları** (`HASH_ALANLARI`, durumsuz, koşu sırasında serbestçe
   çekilir). Bu ayrım, aynı tohumda farklı protokollerin **aynı dünyayı ve
   aynı trafiği** görmesini yapısal olarak garanti eder.
3. **Korunum denklemi + mutabakat.** `üretilen = teslim + düşen + kuyrukta
   + uçuşta` her koşuda otomatik denetlenir (`cekirdek/korunum.py`). Ayrı
   bir ikinci kapı — mutabakat — defterin *modelinin* gerçeği doğru temsil
   edip etmediğini sınar; denklem tutup mutabakat kırılabilir (bir paketin
   sessizce "kaybolduğu" ama defterin bunu göremediği durum).
4. **Kâhin izolasyonu.** Protokolün göreceği her şey `sim2/gozlem/pencere.py`
   ile kilitlenmiştir; kanala, topolojiye, `Konfig`e geri referans **yapısal
   olarak imkânsızdır** (AST testleri ve `Kahin[T]` sarmalayıcı tipi ile).
5. **Köken disiplini.** `Konfig`in her alanı ve `sim2/` altındaki her modül
   sabiti, `sim2/yapilandirma/kokenler.py`de yedi kovadan birine yazılmak
   **zorundadır**; eksik alan olduğunda modül içe aktarma anında patlar.
6. **Sonuç satırı kendi kendine yeter.** Her koşunun ürettiği tek `.jsonl`
   satırı, kendi konfigürasyonunu, kapsam sınırlarını ve metrikleri yeniden
   üretmeye yetecek ham veriyi birlikte taşır (`sim2/kosum/sonuc.py`).

---

## 2 · Dizin haritası

```
sim2/                     — model (53 dosya)
  cekirdek/                 rastgelelik · sayaçlar · korunum · kimlik · saat · olaylar · değişmezler
  yapilandirma/              Konfig · köken defteri · senaryolar · kapsam beyanı
  dunya/                     geometri · yerleşim · topoloji · mobilite (3 kol)
  kanal/                     yayılım · sönümleme · girişim · kanal (PER) · çerçeve · karıştırıcı (5 sınıf)
  mac/                       DCF (çekişme) · alıcı zinciri (durum makinesi)
  ag/                        paket · kuyruk · trafik (CBR üreteci)
  gozlem/                    protokolün gördüğü TEK yüzey — pencere, yük, karar, protokol sözleşmesi, teşhis
  olcum/                     paket defteri · rota olayları · fiziksel kopma · evre metrikleri · genel metrikler · kâhin sarmalayıcı
  kosum/                     kurulum · düğüm · gönderim · teslim · olay döngüsü (Kosu) · sonuç satırı

kalibrasyon/               — ölçüm aletleri (25 dosya) — taban çizgisi DEĞİL
protokoller/               — koşum test araçları (1 dosya, 2 sınıf) — taban çizgisi DEĞİL
tests2/                    — 15 dosya, 478 test
```

Katman yönü **tek yönlüdür** ve bir denetim kapısıyla (D1) korunur:

```
cekirdek → yapilandirma → dunya → kanal → mac → ag → gozlem → olcum → kosum
```

Bir katman yalnızca kendinden önceki katmanları içe aktarabilir. `kalibrasyon/`
ve `protokoller/` bu sıranın dışındadır; ikisi de yalnızca `sim2/`i kullanır,
`sim2/` hiçbirini kullanmaz.

---

## 3 · `cekirdek/` — hiçbir modelleme kararı taşımayan temel

### 3.1 · `degismezler.py` — `assert` yerine
`dogrula(kosul, mesaj)` fonksiyonu projedeki tek koruma idiomudur.
`python -O` altında çıplak `assert` satırları **derlenirken silinir**;
`dogrula` her zaman koşar. `dogrula_ayrintili` yalnız `SIM2_AYRINTILI`
ortam değişkeni açıkken (varsayılan açık) çalışan pahalı kontroller için.
`asla(mesaj)` ulaşılmaması gereken kod dallarını işaretler.

### 3.2 · `rng.py` — iki ayrı rastgelelik mekanizması
- **Sıralı akışlar** (`AKIS_ADLARI`, 17 tane): yerleşim, irtifa, mobilite
  (hız/azimut/pitch — üç ayrı akış, çünkü güncelleme sırası bir modelleme
  kararı olmamalı), görev kolu (merkez/istasyon/jitter), saat (ofset/sapma),
  trafik (çiftler/zaman), beacon fazı, MAC geri çekilme (düğüm başına alt
  akış), protokol keşfi (düğüm başına alt akış), ölçüm örneklemesi. Her akış
  kendi adından `blake2b` ile tohumlanır; akışlar birbirinden bağımsızdır.
- **Hash alanları** (`HASH_ALANLARI`, 7 tane): kanal kararı, gölgeleme,
  sönümleme I/Q, reaktif sezme, taramalı konak, aldatıcı içerik. Durumsuz —
  `hash_cekimi(alan, tohum, *anahtarlar)` her zaman aynı anahtarla aynı
  sayıyı verir, kaç kez çağrıldığından bağımsız. Yeni bir hash alanı eklemek
  hiçbir eski çekimi kaydırmaz; yeni bir sıralı akış eklemek de kaydırmaz
  (her akış kendi adından tohumlanır) ama **var olan bir akıştan fazladan
  çekim yapmak** kolları desenkronize eder — bu yüzden düğüm başına alt akış
  zorunludur (`Akislar.dugum(ad, dugum)`).
- `normal_cekimi` Box-Muller ile durumsuz `N(0,1)` üretir; tek bir 128-bit
  özetin iki yarısından iki bağımsız düzgün değer çıkarır.
- `akis_listesi_hash()` iki listenin parmak izini sonuç satırına yazar; liste
  değişirse iki satır biçimsel olarak karşılaştırılamaz hâle gelir.

### 3.3 · `korunum.py` — tek geçiş noktası
`KorunumDefteri`: `uret · kuyruktan_al · ucustan_kuyruga · teslim_et · dus`
metotlarının dışında paket durumu değiştirilemez. Sekiz kapı:
- **Denklem** (`kontrol()`/`denklem_tutuyor_mu`): `uretilen = teslim +
  Σdusen + kuyrukta + ucusta`. Tutmuyorsa satır `korunum_tamam=False` alır
  ve analiz onu dışlar.
- **Mutabakat** (`mutabakat(kuyrukta_gercek, ucusta_gercek)`): defterin
  *modelinin* gerçeği doğru temsil edip etmediğini sınar. Denklem defterin
  kendi iç tutarlılığını ölçer; mutabakat modelin dünyayı doğru okuyup
  okumadığını. Bir test bunu kırmaya çalışıp kıramayınca bu ikinci kapı
  eklendi.
- Düşme sebepleri **kapalı bir kümedir**: `kuyruk_tasmasi · ttl ·
  iletim_basarisiz · hedef_yok · rota_gecersiz`. Yeni bir sebep eklemek
  şema değişikliğidir.

### 3.4 · `sayaclar.py` — tüm sayaçların TEK kaynağı
`TANIMLAR` demeti (38 giriş) hem sayaçları (`SayacTanimi`) hem türevleri
(`Turev`, bir oranı iki sayaçtan türetir) tanımlar. Her sayaç için pencere
ikizi (`_pencere` sonekli), kâhin işareti ve kapalı-küme üyeliği otomatik
türer — ikinci bir liste elle tutulmaz. Ölçülmüş bir çarpıklık yüzünden
(kontrol baytının **%16,6–23,0'ı** ölçüm penceresi dışında üretiliyor,
kola göre değişen oranda) pencere ikizi varsayılan olarak **açıktır**;
kapatmak `ikizsiz_gerekce` yazmayı zorunlu kılar. Üç tür: `sayim` (tam
sayı, monoton), `birikim` (float, monoton), `tepe` (maksimum — farkla
türetilemez, ayrı izlenir). `sayac_semasi_hash()` şemanın parmak izini
sonuç satırına yazar.

Bugünkü sayaç envanteri (özet): veri düzlemi (3) · MAC/PHY (7) · kontrol
düzlemi (7) · kuyruk/TTL (4) · rota olayları/kopma (5) · ölçüm (1:
`islenen_olay`, pencere ikizsiz) · türevler (6: `psr · nrl_cerceve ·
nrl_bayt · nrl_airtime · cor · algilama_duyarliligi`).

### 3.5 · `kimlik.py` — bir satırın hangi koşudan geldiği
İki ayrı kimlik: `kosu_kimligi` (**belirlenimci** — aynı girdi aynı kimlik,
kopya tespiti için) ve `calisma_kimligi` (her `python ...` çağrısında yeni,
**hiçbir parmak izine girmez**). `arac_hash()` `sim2/`nin tüm `.py`
dosyalarının içeriğinin özeti (git'ten daha güvenilir: yerel, kaydedilmemiş
değişikliği de görür). `kurulum_hash` konfigürasyonun `TEDAVI_ALANLARI`
hariç tamamının özeti — iki koşunun "aynı deneyin iki kolu" sayılıp
sayılmayacağını belirler. `evren_hash` ölçüm penceresindeki paket evreninin
özeti.

### 3.6 · `saat.py` — senkron OLMAYAN saatler
`YerelZaman` ayrı bir tiptir (küresel zamanla karıştırılamaz).
`Saatler.yerel(dugum, t)`: `t·(1+sapma) + ofset`. Ofset `U(±0,5 s)`, sapma
`N(0, 20 ppm)`. Ablasyon: `Konfig.saat_senkron=True` ikisini de sıfırlar.
Protokolün gördüğü tek zaman budur — bedava kusursuz senkron yasaklanmadan
**imkânsız** hâle getirilir.

### 3.7 · `olaylar.py` — kesikli olay çekirdeği
`OlayKuyrugu`, `heapq` üstünde `(zaman, sıra_no, geri_çağrı, args)`
dörtlüleri tutar. Belirlenimcilik `sıra_no`dan gelir (eşit zamanlı olaylar
ekleme sırasına göre); olay nesneleri **asla karşılaştırılmaz** (bellek
adresine bağlı bir belirlenimsizlik kaynağı olurdu). `kostur(bitis_s)`
yeniden çağrılabilir — ısınma/pencere/boşalma üç ayrı çağrıyla işlenir ve
tek çağrıyla birebir aynı sonucu vermek zorundadır.

---

## 4 · `yapilandirma/` — parametreler ve köken disiplini

### 4.1 · `konfig.py` — 788 satır, tek `dataclass`
`Konfig` bir koşuyu **tam** belirleyen her şeyi taşır (donmuş —
`frozen=True`). ~74 alan, sekiz bölümde: kimlik · zaman · dünya · mobilite
(Gauss-Markov + görev kolu) · fiziksel katman · gölgeleme · sönümleme ·
alıcı · MAC · saat · trafik · kuyruk/TTL · kontrol düzlemi · karıştırıcı.
`__post_init__` içinde ~25 değişmez denetimi (pozitiflik, bant tutarlılığı,
darbeli-override çakışması, akış/düğüm oranı, grup yarıçapı/alan oranı vb.).

Türetilmiş özellikler (hiçbiri elle yazılmış sayı taşımaz):
`mobilite_kolu · hareketli · karistirici_sinifi · girisim_orani ·
girisim_menzili_m · difs_s · komsu_omru_s · olcum_penceresi ·
tepe_telafisi_db · karistirici_guc_dbm · karistirici_merkez ·
sunulan_paket_hizi_hz` ve ölçek eşlemesi (`gercek_alan_km`,
`gercek_capa_km`, `gercek_hiz_araligi_kmh`, `olcek_guc_farki_db`).

Modülün sonunda, içe aktarma anında koşan bir denetim: `Konfig`in her
alanı `kokenler.KOKENLER`de olmak **zorundadır**, yoksa modül hiç yüklenmez.

### 4.2 · `kokenler.py` — köken kayıt defteri, 868 satır
Yedi kova:

| kova | anlamı | bugün (Konfig+modül) |
|---|---|---|
| `TURETILMIS` | başka parametrelerden hesaplanıyor | 43 |
| `OLCULMUS` | bir kalibrasyon betiği üretti, komutu yazılı | 11 |
| `KAYNAK` | doğrulanmış dış kaynak (`02-DOGRULANMIS-KAYNAKLAR.md`de var) | 6 |
| `DUYARSIZ` | oynatıldı, çekirdek hücrenin çıktısı değişmedi | 18 |
| `TEDAVI` | deneyin ekseni; `kosum/sonuc.py::TEDAVI_ALANLARI` ile **aynı küme** olmak zorunda | 11 |
| `KOL_TANIMI` | bir kolun ne olduğunu tanımlayan sabit; `kurulum_hash`in içinde | 6 |
| `SINANMAMIS` | gerekçesi yok/yetersiz — mühürden önce boşalmalı | **33** |

`DUYARLILIK_BEKLEYEN` ayrı bir borç sayacıdır: `KOL_TANIMI`daki beş sabit
(`darbe_periyodu_s · darbe_gorev_cevrimi · taramali_konak_suresi_s ·
taramali_konak_sayisi · karistirici_konum`) kendi canlı kollarında
oynatılmış ve **dördü DUYARLI** çıkmış (biri karar bekliyor).

`MODUL_KOKENLERI` aynı yedi kovayı `sim2/` dışındaki (`kalibrasyon/`
dahil) modül düzeyi sabitler için tutar — `dosya::AD` anahtarıyla. Bugün
41+ girdi; kalibrasyon aletlerinin sabitleri de dahil (`ATLAMA_ESIGI`,
`SONUMLEME_ORNEGI`, `YENILIK_ONBELLEK_SINIRI` vb.).

### 4.3 · `senaryolar.py` — deney kolları
İki eksenin çapraz çarpımı:
- **Mobilite kolu** (3): `statik · bagimsiz · gorev`
- **Karıştırıcı sınıfı** (6): `yok · surekli · surekli_darbeli · reaktif ·
  aldatici · taramali`

18 senaryo, `SenaryoTanimi` ile tanımlı (`SENARYOLAR` sözlüğü). Güç
tablosu `KARISTIRICI_GUCU_DBM` beş sınıfın beşinde de **−15,0 dBm taban**
taşır (`yok` için `None`). `senaryo_adi(mobilite, karistirici)` iki
parçayı `-` ile birleştirir (örn. `"statik-yok"`, `"bagimsiz-surekli"`).

### 4.4 · `kapsam.py` — sonuç satırının kendi sınırlarını taşıması
İki liste: `MODELLENMEYEN` (elle yazılır, 10 madde — şartname §12'nin
aynası; her madde `(ne yok, sonucu hangi yöne çektiği)` çiftidir) ve
`bu_kosumda_kapali(konfig)` (konfigden **türer**, bayatlayamaz —
gölgeleme/sönümleme/anten/yakalama/karıştırıcı/mobilite kapalıysa
listeler). `kapsam_bolumu()` ikisini + `karistirici_baslangic_s` +
`olcum_penceresi_s`i sonuç satırının `kapsam` bölümüne yazar.

---

## 5 · `dunya/` — geometri, yerleşim, topoloji, mobilite

### 5.1 · `geometri.py`
`Nokta3(x,y,z)`, `Kutu(en, boy, yükseklik, taban)`. Sınır kuralı
**yansıma**dır (torus ve kelepçeleme ölçülerek elendi). `Kutu.yansit` hem
konumu hem **yönü** çevirir; `Kutu.ayna_ekseni` hangi eksende taşmanın
olduğunu döndürür. `yukselis_acisi_rad` anten deseni için kullanılır.

### 5.2 · `yerlesim.py`
Düğümler kutuya **düzgün rastgele**, reddetme olmadan dağıtılır (eski
"bağlı yerleşim koşullaması" ölçülerek kaldırıldı — hem gereksiz hem hiç
uygulanmamış bir "bağlı tohum süzgeci" beyanı beş dosyadan silindi). Yatay
(x,y) ve dikey (z) **ayrı akışlardan** çekilir. `komsuluk_listesi` ve
`bilesenler` (bağlı bileşen bulma, BFS/DFS) burada — **geometrik**, yani
kâhin bir graf; protokolün gördüğü şey değil.

### 5.3 · `topoloji.py`
`Topoloji.konum(dugum, t)` sıcak yoldaki tek çağrıdır ve **saf**tır. `Anlik`
dondurulmuş bir anlık görüntü (derece, bileşenler, bağlantılılık — hepsi
teşhis). `topoloji_kur(konfig, akislar)` Adım 3'ün tek giriş noktası:
yerleşim + mobilite kurulumunu birleştirir.

### 5.4 · `mobilite.py` — üç kol, tek fizik
- **`Sabit`**: konum sabit. U1 sanity testi (statik + bağlı → PDR ≈ 1)
  için.
- **`GaussMarkov3B`**: literatürün FANET standardı. `α = 0,983`
  (araç dinamiği zaman sabiti, **ölçeklenmez**), adım 0,5 s, hız
  `U(0,25; 0,75) m/s`, azimut σ `0,11 rad` (koordineli dönüşten türer,
  gerçek hızdan — yerçekimi ölçeklenmez), pitch ortalaması **0** (kalıcı
  tırmanışı önler), σ `0,05 rad`. Sınır aynalamasında hem anlık hem
  **ortalama** yön çevrilir — yalnız anlık çevrilirse düğüm duvara yapışır
  (ölçülmüş, düzeltilmiş bir kusur).
- **`GorevTabanli3B`**: koordineli sürü (RPGM ruhunda). Müfreze merkezleri
  kendi sektörlerinde `GaussMarkov3B` ile dolaşır; üyeler istasyonlarına
  (`ISTASYON_TUTMA_S = 2,0 s` zaman sabitiyle) çekilir ve kendi jitter'larını
  yaşar. Dikey yarıçap yatayın 1/4'ü (türetilmiş, ayar düğmesi değil).
  Ölçülen kazanç (bağımsız kola göre): bağıl hız 0,66× · rota ömrü **1,24×**.

Üçü de **tikler arası doğrusal aradeğerleme** kullanır (tik boyunca sabit
hız); yörünge kurulumda önceden hesaplanır çünkü kanal katmanı `konum()`u
parça başına, sıra dışı zamanlarda çağırır.

---

## 6 · `kanal/` — fiziksel katman

### 6.1 · `yayilim.py` — yavaş bileşenler
- **Yol kaybı**: log-mesafe, `PL(d) = PL(1m) + 10·α·log10(d)`, `α = 2,0`
  (hava-hava serbest uzay). `PL(1m) ≈ 40,05 dB` @ 2,4 GHz.
- **Verici gücü TÜRETİLİR**: menzil tanımı "girişimsiz SINR'in tam β'ya
  eşit olduğu mesafe"dir; `Pt` bundan çözülür (elle yazılmaz).
- **Anten deseni**: yarım dalga dipol, kapalı form (`F(φ) =
  cos(½π·sinφ)/cosφ`), bir bağda **iki** anten (`bag_anten_kaybi_db`).
- **Gölgeleme**: log-normal, bağ-simetrik (`min(i,j),max(i,j)`), konuma
  bağlı — hücre köşelerinden trilineer ağırlıklarla harmanlanır ve
  `√(Σw²)`ye bölünerek varyans her yerde tam 1'e normalize edilir. `σ = 3,0
  dB`, hücre `50 m`.
- Gürültü tabanı: `N = k·T·B·F`, 290 K / 2 MHz bantta ≈ **−105,0 dBm**.

### 6.2 · `sonumleme.py` — Rician, parça başına, DURUMSUZ
AR(1) yerine hash'lenmiş yenilikler üstünde FIR: `h_k = c·Σρᵐ·w_{k-m}`,
`w` durumsuz hash çekimi. Bu, iki protokolün aynı tohumda **birebir aynı**
kanalı görmesini sağlar (çekim sayısı protokole göre değişse bile). Parça
süresi kuralı: `T_c(p99)/4`, bugün **190 µs** (K = 6, Rician K'dan
bağımsız — donuk kolda K sonucu hiç değiştirmiyor, hareketli kolda 6
örnek "duyarsız" kovasında). Doppler **tam ölçek hızından** hesaplanır
(dalga boyu ölçeklenemez) — bu, K-102'de bulunan kritik bir kararın
kalbidir. `BAGIL_HIZ_TABANI_MS = 1,0` sıfır hızı önler.
`YENILIK_ONBELLEK_SINIRI = 250 000`, dolunca tamamen boşalır (saf memo,
sonucu değiştirmez).

### 6.3 · `girisim.py` — havadaki iletimler defteri
`Ortam`: aktif iletimlerin listesi. `Girisim.girisim_w(alici, t, haric)`:
`haric` **zorunludur** — alıcı kendi çerçevesini girişim sayamaz. Parça
sınırları sönümleme ızgarası ∪ girişim olayları ∪ karıştırıcı geçiş
anlarının **birleşimidir**.

### 6.4 · `kanal.py` — TEK `per()` gövdesi
Kâhin ve gerçek alım **aynı** `_hata_olasiligi` gövdesini çağırır; tek
fark girdideki SINR izinin uzunluğu (tek parça / çok parça). Modülasyon
**DQPSK** (802.11b'nin 2 Mb/s modu), Marcum-Q ile kapalı formda
(`scipy.stats.ncx2`, `scipy.special.i0e`). Önbelge PER'i **ayrı**: temel
hızda (1 Mb/s) **DBPSK** ile, gövdeden bağımsız bir kapalı form.

### 6.5 · `cerceve.py` — süre ve bit sayısının TEK yeri
`cerceve_kur(konfig, tip, bayt=None)`: `sure_s = onbelge_s + bayt·8/bit_hizi_bps`.
Dört tip: `veri · onay · beacon · kontrol` (sonuncusu tanımlı ama bugün
hiç kurulmuyor). Önbelge gövde hatasına **katılmaz** (fizik kararı: farklı
modülasyon).

### 6.6 · `karistirici.py` — beş sınıf
| sınıf | zamanlama | CSMA'ya görünür mü |
|---|---|---|
| `Surekli` | her an açık | hayır |
| `Darbeli` | periyodik (%50 görev çevrimi, aynı ortalama güç) | hayır |
| `Reaktif` | ortama tepki verir — zamanın saf fonksiyonu **değil**; sezme 16 µs, patlama 144 µs, **sürekli yeniden silahlanır** | hayır |
| `Aldatici` | geçerli görünümlü çerçeveler basar | **evet** |
| `Taramali` | konaklar arasında gezinir (tepe eşit, ortalama 1/3) | hayır |

Hepsi `KaristiriciTabani`den türer: konum **sabit** (alan merkezi),
tepe gücü `Konfig.karistirici_guc_dbm`den, **açılma anı** var
(`karistirici_baslangic_s`, projenin geçici-tepki iddiasını ölçülebilir
kılan mekanizma).

---

## 7 · `mac/` — 802.11 DCF, temel erişim

### 7.1 · `dcf.py` — yalnız çekişme mantığı, hiçbir fizik formülü yok
Durum makinesi: `bos → geri_cekilme → gonderiyor → onay_bekliyor`. Geri
çekilme sayacı `[0, cw]` düzgün, `cw` katlanması `min(2cw+1, cw_max)`.
`cw_min=31`, `yeniden_deneme_siniri=4` → dizi `31→63→127→255→511`de durur
(`cw_max=1023`e **erişilemez**, aritmetikle kanıtlı ve `TURETILMIS`).
Geri çekilme akışı **düğüm başına alt akış**tır (kuplajı önler).

### 7.2 · `alici.py` — tek radyo, durum makinesi
`bos → onbelge_kilidi → govde_aliyor → bos`. Aynı anda **en fazla bir**
kilitli çerçeve (fiziksel gerçeklik: tek radyo aynı anda iki çerçeveyi
alamaz). Capture effect (`yakalama_etkisi_acik` ablasyonu): güç farkı eşiği
+ yakalama penceresi koşulu birlikte. Alım sonuçları kapalı bir kümedir ve
toplamı denemeye eşit olmak zorundadır: `alim_basarili ·
alim_red_yari_cift · alim_red_mesgul · alim_red_onbelge · alim_red_per`.

---

## 8 · `ag/` — veri düzlemi birimleri

- **`paket.py`**: `Paket` donmuş, kimliği koşu boyunca değişmez. Üç alan
  şema taahhüdü: `akis_kimligi` (IPDV için), `dogum_s` (gecikmenin sıfır
  noktası), `ttl_kalan`.
- **`kuyruk.py`**: sonlu FIFO, **kuyruk-sonu atma** (drop-tail). Düşme
  korunum defterinden geçmek zorundadır — kuyruk kendi başına "yok etmez".
- **`trafik.py`**: CBR, **10 akış × 4 pkt/s × 512 B** (tek çarpışma
  alanının %36,9'u — 4 Eylül'de ölçülerek seçildi, ama bugün bayat: ölçüm
  eski çalışma noktasında yapıldı). Doğum çizelgesi **kurulumda** tam
  belirlenir (koşu sırasında çekim yapılsaydı iki kol farklı trafik
  görürdü). Kaynak-hedef çiftleri bağlantıya göre seçilmez (koşullansaydı
  eşleştirme kırılırdı).

---

## 9 · `gozlem/` — protokolün gördüğü TEK yüzey

Bu paket, projenin en sıkı kilitlenmiş sözleşmesidir.

### 9.1 · `pencere.py` — sözleşmenin kendisi
`Gozlem` (12 alan): kimlik/saat, kendi donanım ölçümleri
(`olculen_gurultu_w · kanal_mesgul_mu · kuyruk_uzunlugu ·
kuyruk_kapasitesi`), iletim geçmişi (`son_iletim_sonucu ·
son_iletim_hedefi · gonderilen_bayt · alinan_bayt`), komşular (yalnız
beacon'dan), taşınan paket (başlıkta yazan alanlar). `KomsuKaydi` (7 alan),
`PaketGorunumu` (5 alan). Üç izin listesi (`IZINLI_*`) ve bir **yasaklı
tipler** listesi (`YASAK_TIPLER` — `Konfig`, `Topoloji`, `Kanal` vb.,
20+ tip) bir yüzey testiyle korunur. Saat **kendi saatidir** (senkron
değil); `dogum_s` **yoktur** (olsaydı iki düğüm karşılaştırarak saat
farkını bedava öğrenirdi).

### 9.2 · `protokol.py` — dört kanca
```
sonraki_atlama(gozlem) -> Karar
beacon_yuku(dugum)     -> dict
beacon_alindi(dugum, komsu, yuk, saat_s) -> None
teshis(dugum)          -> dict
```
`Protokol` bir `Protocol` tipidir (varsayılan gövde yok — eksik kanca
çağrı anında `AttributeError` verir, sessizce "boş" bir protokol
davranışı üretmez). `protokoller/` yalnız bunu görür.

### 9.3 · `karar.py` — `Karar` ve `Beyan`
`Karar(sonraki: int|None, beyan: tuple[Beyan,...])`. `sonraki` tek
eylemdir; `beyan` **yalnız ölçüme gider**, davranışı etkilemez (istisna:
`rota_gecersiz` beyanı paketi düşürür). `Beyan.tip` kapalı küme: `kopma ·
rota_kuruldu · rota_gecersiz`. Bunlar Risk 3'ün (kâhin sızıntısının yeni
kapısı — hiç beyan etmeyen bir protokol yapay olarak iyi görünür) panzehiri.

### 9.4 · `yuk.py` — beacon yükünün bayt bedeli
`yuk_bayt(dict)`: tarife (bool=1, int=büyüklüğüne göre, float=4 bayt tek
duyarlık). **Öz-denetimli**: `_tasinan_bilgi_bayt` tarifeyi kullanmadan,
üretilen demetten **deneyerek** (to_bytes/struct) ölçer ve iki hesap
ayrışırsa `YukHatasi` fırlatır. `yuku_dondur` float'ı tel biçimine
(tek duyarlık) kırpar — bu kırpma olmadan geçmişte 2,00× bir bedel kaçağı
vardı (B-83).

### 9.5 · `karar.py` yanında `teshis.py` — teşhis sözleşmesi
`teshis()` kancasından dönen sözlük NaN reddi dahil tipli denetimden
geçer (`TESHIS_EN_UZUN_AD_BAYT=64`, `TESHIS_EN_COK_ALAN=32` vb.). Amaç:
koşu bittikten SONRA JSON serileştirmesinde çökme riskini önlemek.

---

## 10 · `olcum/` — ölçüm defterleri ve metrikler

### 10.1 · `paket_defteri.py`
Doğum (`dogdu`) ve teslim (`teslim_edildi`) kayıtları — sayaçlardan **ayrı**
(yüzdelik/IPDV bir toplamdan çıkmaz, tek tek gecikme gerekir). PDR **doğuma
göre** kohortlanır: pencerede doğan bir paket, ne zaman teslim edilirse
edilsin sayılır. `ham_sozluk()` sonuç satırının `ham` bölümünü üretir —
`teslim_*` dizileri + `dogum_s` (koşumun **tamamını** kapsar, pencereye
kırpılmaz — pay/payda farklı kümeden gelmesin diye).

### 10.2 · `rota_olaylari.py`
`RotaDefteri`: kopma/kurtarma olayları, Δ (`T_kurtarma − T_kopma`, hiç
beyan yoksa **None**, sıfır değil), COR (`rota_kurtarildi/rota_etkilendi`).
`algilama_duyarliligi = kopma_algilanan / kopma_fiziksel` — payda **kâhin**
sayaçtır (Risk 3'ün nicel yarısı).

### 10.3 · `kopma.py` — `kopma_fiziksel`in açık taahhüdünün kapanışı
`fiziksel_kopma_say`: **yavaş SINR** (hızlı sönümleme, girişim, karıştırıcı
HARİÇ) eşiğin altına inen bağ geçişlerini 1 s'lik ızgarada sayar. Karıştırıcı
kasten dışarıda (periyodik sınıfların salınımı "kopma" gibi sayılıp payda
şişmesin diye). Son işlemdir (koşu bitince, sıcak yola dokunmaz) — statik
kolda sonuç **tam sıfır olmak zorundadır** ve bu bir kapıdır.

### 10.4 · `evre.py` — şok · toparlanma · tespit
`IZGARA_ADIMI_S = 1,0` (RFC 3561 HELLO_INTERVAL — çözünürlük),
`PENCERE_S = 15,0` (RFC 3626 TOP_HOLD_TIME — durağanlık). Üç evre:
`TEMİZ [ölçüm_başı, açılma) · ŞOK [açılma, açılma+15) · TOPARLANMA
[açılma+15, ölçüm_sonu)`. Dört metrik, sıfır serbest parametreyle:
- **M1 şok derinliği**: `PDR(temiz) − PDR(şok)`, Agresti–Caffo standart
  hatasıyla (Wald `p=1`de çöker ve bu projede `p=1` kural, istisna değil).
- **M2 toparlanma tamlığı**: `PDR(toparlanma)/PDR(temiz)`, kırpılmaz.
- **M3 toparlanma süresi**: PDR'nin `temiz − 2·SE` bandına döndüğü ilk an;
  sansürlüyse `None`.
- **M4 tespit gecikmesi**: beyan hızının temiz evrenin Poisson kuyruğunu
  aştığı ilk an; susan protokolde `None`.

### 10.5 · `metrikler.py` — genel metrik sözlüğü
`YUZDELIKLER = (50, 95, 99)`. `yuzdelik()` doğrusal aradeğerlemeli, tek
tanım (analiz katmanının ikinci gerçeklemesi bununla karşılaştırılır).
`metrik_sozlugu()`: sayaçlardan gelenleri olduğu gibi taşır + ham liste
gerektiren metrikleri (gecikme yüzdelikleri, IPDV, Δ istatistikleri) +
`acilma_s` verilmişse evre metriklerini ekler (verilmezse "yok", `None`
değil — "ölçülmedi" ile "ölçüldü tanımsız çıktı" ayrımı).

### 10.6 · `kahin.py` (sim2 içindeki, kalibrasyon/kahin.py'den farklı)
`Kahin[T]` sarmalayıcı tipi: `.rapora()` dışında değeri okumanın yolu yok,
`__repr__` değeri gizler. Bir protokolün kâhin bir sayıyı kazara okuyamaması
için — okuyabilmesi için önce bu modülü içe aktarması, sonra `.rapora()`
çağırması gerekir; ikisi de görünür ve AST testiyle yasak.

---

## 11 · `kosum/` — olay döngüsü ve birleşim noktası

### 11.1 · `kurulum.py`
`kurulum_yap(konfig, tohum)`: bütün rastgelelik **burada tükenir**
(yerleşim, mobilite, saat, trafik, beacon fazı). Koşu sırasında çekim
yapan tek sıralı akış `mac_geri_cekilme`dir (düğüm başına alt akış).
`Kurulum` donmuş bir `dataclass` — koşu ortasında değişemez.

### 11.2 · `dugum.py` — bir düğümün tüm davranışı, 445 satır
`Dugum`: kuyruk + DCF + alıcı zinciri + komşu tablosu + protokol kancaları.
- `gozlem(t, paket)`: `Gozlem` nesnesini kurar (tek üretim yeri).
- `kanal_mesgul_mu`: taşıyıcı dinleme, **geometrik** duyma kümesiyle
  (girişim menzilinin ötesi zaten gürültü tabanının altında).
- `karistirici_mesgul_mu`: iki koşul birlikte — sınıf CSMA'ya görünür mü
  VE bu düğümde gücü gürültü tabanını aşıyor mu. (Geçmişte bir kusur:
  yalnız birinci koşul soruluyordu ve karıştırıcı **bütün ağı**
  ölçeksiz erteletiyordu.)
- `mesgul_bitisi_s`: donmuş bir düğümü uyandırma anını **hesaplar**
  (yoklama yerine — milyonlarca ölü olay üretmesin diye).
- Korunum defterine giden her yol (`kuyruga_al`, `dus`) tek noktadan geçer.
- `beacon_yuku()` artık **yük + bayt bedelini** birlikte döndürür (bedel
  sayaçta değil çerçevenin boyutunda ödenir — bkz. §13).

### 11.3 · `gonderim.py` · `teslim.py`
`gonder()`: çerçeveyi havaya verir, duyanlara olay zamanlar, gönderene
donma uygular. `veri_gonder`, `iletime_basla`, `vazgec` (yeniden deneme
hakkı bitince, paket el değiştirmişse **düşürülmez**). `teslim.py`:
el değiştirme **alıma bağlıdır, onaya değil** (gerçek 802.11 davranışı —
"veri alındı, onay kayboldu" durumunun tek doğru modeli). Tekrar bastırma
`(gönderen, uçuş_no)` ile, paket kimliğiyle değil (bir döngüde meşru
ikinci ziyaretin yutulmaması için).

### 11.4 · `kosu.py` — sekiz olay, olay döngüsünün kendisi
```
dogum · beacon · geri_cekilme_bitti · difs_bitti
iletim_bitti · cerceve_geldi · cerceve_bitti · onay_penceresi
```
Beacon **çekişir** (kanal meşgulse atlanır). Geri çekilme **olay
güdümlüdür**, slot güdümlü değil (350 s × 20 µs = 17,5 milyon olay/düğüm
olurdu; onun yerine boş kalan aralık bir kerede geçirilir).
`_beacon_cercevesi(ek_bayt)`: beacon çerçevesi artık **protokolün taşıdığı
yük kadar uzar** (9 Eylül 2026'da eklendi — bkz. §13). Olay iptali yok,
sürüm sayacı var (bayat bir zamanlanmış geri çekilme bitişi sessizce yok
sayılır).

### 11.5 · `sonuc.py` — tek satırlık sonuç, 8 bölüm
```python
BOLUMLER = ("kimlik", "ortam", "konfig", "kapsam", "metrikler",
            "korunum", "ham", "teshis")
```
Hiçbir sözlük literali yok — her bölüm kendi kayıt defterinden türer.
`TEDAVI_ALANLARI = ("kol", "senaryo", "tohum", "not_")`. `SatirYazici`
satır başına `flush + fsync` yapar (uzun bir tarama ortasında kesilirse
tamamlanan satırlar kaybolmasın diye).

---

## 12 · `protokoller/` — bugün var olan tek iki "protokol"

`kosum_kosumu.py` içinde iki sınıf, **taban çizgisi değil**, Adım 9'un
olay döngüsünü sınamak için:

- **`DogrudanKomsu`**: hedef doğrudan komşuysa gönderir, değilse
  `hedef_yok`. Tek atlamalı; kuyruk taşması ve `hedef_yok` dalını sınar.
- **`EnYakinKimlik`**: hedef komşu değilse, **kimliği** hedefe en yakın
  komşuya iletir. Kasıtlı kötü sezgi — düğüm numaraları uzayda anlam
  taşımaz, yani yol seçimi rastgeleye yakındır ve **döngü üretir**. TTL
  ölümü, tekrar bastırma ve `aktarilan_paket` dallarını ateşlemek için.

İkisi de yalnız `Gozlem`i görür; kâhin erişimi yok.

---

## 13 · Bu oturumda düzeltilen bir bedel kaçağı — beacon yükü

Gözlem sözleşmesinin maddesi: *"komşusunun bilgisini kullanmak isteyen
protokol, o alanı beacon'a koymak ve bedelini ödemek zorundadır."* Ölçüldü
(9 Eylül 2026): bedelin yalnız **yarısı** ödeniyordu — `kontrol_bayt`
sayacı yükü doğru sayıyordu ama beacon **çerçevesi** kurulumda bir kez
kurulmuş, sabit boyutluydu. 250 baytlık bir yük çerçeveyi 4,12 kat
uzatması gerekirken **320 µs'de sabit kalıyordu**: fazladan hava süresi
yok, çarpışma riski yok, gövde hata olasılığı yok.

Düzeltme: `Dugum.beacon_yuku()` artık `(yük, ek_bayt)` çifti döndürüyor;
`Kosu._beacon_cercevesi(ek_bayt)` çerçeveyi `beacon_bayt + ek_bayt`
boyutunda kuruyor (boyuta göre önbellekli, saf memo). Sayaç artık **tek
kaynaktan** — çerçevenin boyutundan — besleniyor; `Dugum` ayrıca
saymıyor (çift faturalama önlendi). Regresyon kanıtı: değişiklikten önce
yazılmış gerçek bir sonuç satırıyla aynı konfig/tohum karşılaştırıldı —
`metrikler · korunum · ham · teshis` **birebir aynı** çıktı (bugünkü üç
protokol gerçeklemesinin üçü de boş yük taşıdığı için).

---

## 14 · Bugünkü çalışma noktası — tek tabloda

| büyüklük | değer | nereden |
|---|---|---|
| alan | **1800 × 1800 m** | statik kolda 30 tohumda kopukluğun sıfır kaldığı en büyük alan |
| düğüm sayısı | 40 | onaylanmamış kapsam kararı (band: 20–80) |
| ortalama derece (çalışma noktası) | **8,67** | `kalibrasyon/calisma_noktasi.py` |
| ölçek | 1:50 | hızlar 30–400 km/h aralığına, verici gücü fiziksel bir telsize (2,5 W) düşecek şekilde |
| yol kaybı üsteli α | 2,0 | hava-hava serbest uzay (iki-ışın kırılma mesafesi bağ mesafesinin çok üstünde) |
| SINR eşiği β | 16 dB | 10 dB çözülebilirlik + 2σ gölgeleme marjı |
| gölgeleme σ | 3,0 dB | PER geçiş bandıyla (3,44 dB) aynı mertebe |
| Rician K | 6 dB | `SINANMAMIS` — Γ=0,50 yer yansıma katsayısı sorusuna indirgendi, kaynak kontrolü bekliyor |
| mobilite Θ (çekirdek kol) | **3,25** | kapı Θ≥3, marj yalnız %8 |
| mobilite hız aralığı | 0,25–0,75 m/s (45–135 km/h gerçek) | Θ kapısı + gerçekçilik kısıtının kesiştiği tek nokta |
| karıştırıcı gücü (taban) | **−15,0 dBm** | ρ (engellenen bağ oranı) en büyükken ağ hiç ayrılmıyor |
| ρ (referans sınıf `surekli`) | **0,258** | |
| bağ eşiği (`ATLAMA_ESIGI`) | 0,90 | kararların değişmediği platonun en küçük değeri |
| trafik | 10 akış × 4 pkt/s × 512 B | tek çarpışma alanının %36,9'u (bayat ölçüm) |
| ölçüm penceresi | `[50, 320) s`, karıştırıcı açılışı `150 s` | temiz 100 s / şok 15 s / toparlanma 155 s |
| deneyin çözünürlüğü | **0,036 PDR puanı** (2SE/√30) | `kalibrasyon/cozunurluk.py` |

---

## 15 · Mimari denetimi — 15 kapı (`kalibrasyon/mimari_denetimi.py`)

| kapı | ne sınar |
|---|---|
| D1 | Katman yönü — bir katman yalnız kendinden önceki katmanları içe aktarabilir |
| D2 | Çıplak `assert` yok (hepsi `dogrula()`) |
| D3 | Belirlenimsiz kaynak yok (`hash()`, `id()`, `time`/`datetime`/`uuid`/`os` içe aktarımı kimlik dışında) |
| D4 | Ölü kod — `__all__`da olup hiç **okunmayan** ad (10 Eylül'de eşiği düzeltildi: önceden 29 canlı adı yanlış "ölü" sayıyordu) |
| D5 | `Konfig` alanları — bildirim ≠ kullanım (her alan fiilen okunuyor mu ya da `HENUZ_OKUNMAYAN`da mı) |
| D6 | RNG akışları — bildirilen akış/hash alanı fiilen çekim alıyor mu |
| D7 | Kâhin yüzeyleri — `dunya.topoloji`, `dunya.yerlesim`, `olcum`, `gozlem` modüllerinin kâhin olduğunu **beyan** edip etmediği |
| D8 | Sayısal sağlık — türetilen büyüklüklerin tutarlılığı (girişim menzili > iletim menzili, DIFS > SIFS, `cw_max` erişilemezliği vb.) |
| D9 | Belirlenimcilik — aynı tohum aynı dünyayı, farklı tohum farklı dünyayı üretiyor mu |
| D10 | Mobilite kolu t=0 yerleşimini değiştirmiyor mu (statik ve bağımsız kol aynı başlangıçtan başlamalı) |
| D11 | İçe aktarılabilirlik — her `sim2/` modülü hatasız import ediliyor mu |
| D12 | Parametre kökenleri — her sayının bir kovada olduğu, `SINANMAMIS`/`DUYARLILIK BORCU` sayaçları |
| D13 | Kalibrasyon kökenleri — `kalibrasyon/` sabitlerinin köken defterinde olduğu |
| D14 | Gölge fizik — tarihsel bir betiğin kopyaladığı sabitlerin **beyan edilip edilmediği** |
| D15 | Bayat üretici — `OLCULMUS` bir kaydın üreticisinin terk edilmiş bir çalışma noktasında olmadığı |

Bugünkü sonuç: **yapısal ihlal yok** · köken borcu **33** · duyarlılık
borcu **5** · 11 not (bilgi amaçlı, hata değil).

Bu kapıların dışında ayrı bir alet, **`kalibrasyon/uretici_duman.py`**,
köken defterinin andığı üretici komutların hâlâ koştuğunu sınar (9 Eylül
2026'da eklendi — dört üretici kırık bulundu ve onarıldı). Kendi kapısı
var (`--kapi`).

---

## 16 · `kalibrasyon/` — ölçüm aletleri envanteri

25 dosya, taban çizgisi **değil**. En önemlileri:

| dosya | ne ölçer |
|---|---|
| `mimari_denetimi.py` | 15 yapısal kapı |
| `bag_kumesi.py` | en yeni ve en kapsamlı alet (82 KB) — bağ eşiği, Θ, bağlantı bütçesi degenerasyonları, TTL/kuyruk kısıtlama kapısı, Rician K, kendi 4 kapısı (G-a…G-d) |
| `kahin.py` | `EnKisaYolKahin` (en az atlama) ve `EnGuvenilirKahin` (en az ETX — "gerçek tavan" iddiası kısmen çürüdü, K-110) |
| `karistirici_gucu.py` | ρ taraması — çalışma noktasının üreticisi |
| `calisma_noktasi.py` | alan, görev kolu yarıçapı, dört yarıçap tanımı |
| `duyarlilik.py` | 49 aday parametrenin duyarlılık taraması (OAT) |
| `cozunurluk.py` | deneyin çözünürlüğü (R = 2SD/√30) |
| `denetim_ornekleme.py` | kanal grafiğinin zaman/faz denetimi |
| `evre_metrikleri_kapilari.py` | evre metriklerinin 4 kapısı (G1–G4) |
| `pdr_tavani.py` | kâhin PDR tavanı — karıştırıcılı/karıştırıcısız |
| `adim9_kapanis.py` | korunum + mutabakat kapanışı |
| `li_replikasyonu.py` | tek dış çapa — Li vd. zincir replikasyonu |
| `yeniden_kullanim.py` | uzamsal yeniden kullanım mesafesi (Li replikasyonunun mekanizma açıklaması) |
| `sonumleme_onbellegi.py` | önbellek sınırının zararsızlığı |
| `adim4_sonumleme.py` | sönümleme parça süresinin üreticisi |
| `uretici_duman.py` | **meta-alet** — diğer aletlerin hâlâ koşup koşmadığını sınar |

---

## 17 · Test takımı

`tests2/` — 15 dosya, **478 test**, tam koşum **BANT 6–10 dk**.
Dosyalar katmanlara denk düşer: `test_cekirdek.py · test_yapilandirma.py ·
test_dunya.py · test_topoloji.py · test_kanal.py ·
test_kanal_yayilim.py · test_kanal_sonumleme.py · test_karistirici.py ·
test_mac_dcf.py · test_mac_alici.py · test_ag.py · test_saat_gozlem.py ·
test_olcum.py · test_evre.py · test_kosum.py`.

Doğrulama dört seviyede çalışır (`v2/03-YONTEM-KURALLARI.md` Bölüm D):
1. **Analitik** — Bianchi (DCF doygunluk), sönümleme marjinal varyansı,
   yol kaybı kapalı formu.
2. **Korunum** — denklem + mutabakat, her koşuda otomatik.
3. **İç tutarlılık** — uç durumlar, aynı tohum → bit-birebir aynı sonuç.
4. **Literatür replikasyonu** — Li vd. zincir kapasitesi (tek dış çapa,
   mekanizma tuttu, sayı α farkıyla açıklandı).

---

## 18 · Bilinen sınırlar (kasıtlı, beyan edilmiş)

`kapsam.MODELLENMEYEN` listesinden: hız uyarlaması yok, yayılma kazancı
(Barker ~10 dB) yok, enerji sezmeli CCA yok, çoklu kanal yok (projenin
öncülü), RTS/CTS yok (temel erişim), yayılım gecikmesi yok, arazi/engel
yok, havadan karıştırıcı yok, hareketli karıştırıcı yok (açılma anı var,
geçiş yok), patlamalı trafik yok (CBR).

Ayrıca kodda var ama henüz **hiçbir protokol tarafından kullanılmayan**
bir kapasite: protokolün kendi çerçevesini gönderebilmesi, zamanlayıcı
kurabilmesi, ayrı bir kontrol düzlemi periyodu ilan edebilmesi — bugün
temas yüzeyi 4 kanca + tek periyodik beacon + 3 canlı çerçeve tipinden
ibaret.

---

## 19 · Kısa terimler sözlüğü

| terim | anlamı |
|---|---|
| ρ | engellenen bağ oranı — karıştırıcı gücünün kalibre edildiği büyüklük |
| Θ | çalkantı sayısı — rota ömrünün OLSR TOP_HOLD_TIME'a oranı; mobilite kapısı |
| β | SINR eşiği — menzilin tanımlandığı çözülebilirlik sınırı |
| α | yol kaybı üsteli |
| PSR | MAC gönderim başarı oranı (`mac_gonderim_basarili/mac_deneme`) |
| PDR | paket teslim oranı (doğuma göre kohortlu) |
| NRL | normalize kontrol yükü (`nrl_cerceve`, `nrl_bayt`, `nrl_airtime`) |
| COR | iletişim kurtarma oranı |
| Δ | rota kurtarma gecikmesi |
| IPDV | akış içi ardışık gecikme farkı (jitter) |
| kâhin | protokolün erişemediği, yalnız ölçüme giden bilgi/aygıt |
| TEDAVİ | deneyin ekseni (kol, senaryo, tohum, not) |
| KOL_TANIMI | bir kolun ne olduğunu tanımlayan, `kurulum_hash`in içindeki sabit |
