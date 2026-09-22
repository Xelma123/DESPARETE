# 13 · KONTROL DÜZLEMİ — protokolün YAPABİLECEKLERİ

> **Tarih:** 10 Eylül 2026 · **Durum: 🟢 SÖZLEŞME SON HÂLİ ve UYGULANDI.**
> Öğrencinin beş kararıyla kapatıldı; kod bu belgeyle birebir.
> Karar kaydı: `04-NEDEN-BOYLE.md` → **K-112** · Ayrışma defteri: `07` §17 (A19)
> Kapılar: `tests2/test_kontrol_duzlemi.py` (bağlayıcı) ·
> `python -u kalibrasyon/kontrol_duzlemi_kapilari.py` (40 düğümde kanıt)
>
> 🔒 **KAPSAM:** yalnız MEKANİZMA. AODV · OLSR · AOMDV gerçeklemeleri bu
> belgenin konusu **değildir** ve henüz yazılmadı.

---

## 00 · NEDEN

`05-GOZLEM-PENCERESI.md` protokolün ne **GÖRECEĞİNİ** kilitliyordu; ne
**YAPABİLECEĞİNİ** hiçbir belge tanımlamamıştı. Ölçülen yüzey dört kanca, tek
koşum düzeyinde periyodik beacon, üç canlı çerçeve tipi ve **sıfır
zamanlayıcıydı** — yani `06` §4.3'ün şart koştuğu RREQ/RREP/RERR ve U2/U3
uygunluk testleri ifade edilemiyordu. Bu sözleşme o boşluğu kapatır;
gözlem penceresini **genişletmez**.

---

## 01 · ÖĞRENCİNİN BEŞ KARARI → SÖZLEŞME MADDESİ

| # | karar | uygulandığı yer |
|---|---|---|
| **1** | Mesaj boyutu RFC alanlarından türer; PHY/MAC/çerçeve ek yükü **tek kaynak** `cerceve_kur()` | `MesajBicimi.bayt` · `cerceve_kur(…, "kontrol", mesaj_bayt=)` · `KONTROL_KAPSULLEME` |
| **2** | Uyandırma kuyruğunda düğüm başına güvenlik tavanı; aşımda **deterministik FAIL**, sessiz düşürme yok | `BEKLEYEN_UYANDIRMA_TAVANI` · `UyandirmaTavaniAsildi` |
| **3** | Kontrol ve veri **aynı** kanal/MAC/çekişme/kayıp fiziği | aynı DCF alt akışı · aynı `gonderim.gonder` · aynı alıcı zinciri |
| **4** | `kontrol_alindi()` **yalnız başarılı teslimde**; yayın her alıcı için ayrı | `kosum/kontrol.py::cerceve_alindi` |
| **5** | Periyodik ve dinamik zamanlayıcı **ayrı mekanizma** | `zamanlayicilar/zamanlayici_doldu` ↔ `Uyandirma/uyandi` |

---

## 02 · API — protokole görünen (`sim2/gozlem/`)

🔒 Protokol **çağırmaz, niyet döndürür.** Aşağıdaki tiplerin hepsi donmuştur ve
simülatöre geri referans taşımaz (P6).

### 02.1 · `MesajBicimi(ad, alanlar, tekrarli=())`
| alan | tip | kural |
|---|---|---|
| `ad` | `str` | boş olamaz |
| `alanlar` | `tuple[(ad, bit)]` | sabit genişlik; `bit` pozitif tamsayı |
| `tekrarli` | `tuple[(ad, bit)]` | değeri sayı demeti olan alan; boyuta `eleman × bit` |

Alan adları tekildir. **Boyut:** `bayt(yuk) = ⌈(Σ sabit bit + Σ len·bit) / 8⌉`
— projede TEK hesap.

### 02.2 · `KontrolIstegi.kur(hedef, bicim, yuk: dict, jitter_s=0.0)`
| kural | ihlal |
|---|---|
| `hedef` `None` (YAYIN) ya da `≥ 0` düğüm (UNICAST) | `DegismezHatasi` |
| `set(yuk) == biçimin alan adları` — eksik de fazla da olmaz | `KontrolHatasi` |
| `int` → `0 ≤ v < 2^bit` · `bool` → her genişlikte | `KontrolHatasi` |
| `float` → yalnız **32 bitlik** alanda, tek duyarlığa sığmalı | `KontrolHatasi` |
| tekrarlı alan bir demettir, her eleman kendi genişliğine sığar | `KontrolHatasi` |
| doğrudan kurulumda `mesaj_bayt` biçimden türeyenle aynı olmalı | `DegismezHatasi` |
| `jitter_s` negatif olmayan ve sonlu (Y3 · R4) | `DegismezHatasi` |

🔒 **Taşınan bilgi ödenen bitten fazla olamaz** — bir değer alanına sığmıyorsa
mesaj kurulamaz. Yük sıralı, donmuş demete çevrilir (`yuku_dondur`).

### 02.3 · `Uyandirma(gecikme_s, etiket, jitter_s=0.0)` — DİNAMİK zamanlayıcı
`gecikme_s` pozitif ve sonlu · `etiket` boş olmayan `str` · `jitter_s`
negatif olmayan ve sonlu. İhlal: `DegismezHatasi`. Alt sınır ve tavan
simülatörde uygulanır (§03.5); titreşim alt sınırın ÜSTÜNE eklenir (§03.7).

### 02.4 · `Karar.niyetler: tuple = ()`
`KontrolIstegi | Uyandirma` demeti. Varsayılan boş. Başka tip → `KontrolHatasi`.
🔒 **`Beyan` buraya GİREMEZ** (16 Eylül 2026, K-134): `Karar`ın zaten bir
`beyan` alanı var ve iki yol açmak aynı şeyi iki yerden söylemek olurdu.
Kanca dönüşlerinde ise `Beyan` serbesttir (§02.5).

### 02.5 · `KontrolluProtokol` — beş kanca, **hepsi ya da hiçbiri**
| kanca | çağrılma | dönüş |
|---|---|---|
| `zamanlayicilar() -> dict[str, float]` | kurulumda **bir kez** | `{etiket: periyot_s}` |
| `zamanlayici_doldu(gozlem, etiket)` | ilan edilmiş periyot doldu | niyet demeti |
| `uyandi(gozlem, etiket)` | bir `Uyandirma` doldu | niyet demeti |
| `kontrol_alindi(gozlem, gonderen, bicim, yuk, yayin)` | **yalnız başarılı teslim** | niyet demeti |
| `iletim_basarisiz(gozlem, hedef, tur)` | MAC bir UNICAST çerçeveden **vazgeçti** (Y3 · R3) | niyet demeti |
| `iletim_sonucu(gozlem, hedef, basarili, tekrar, tur)` — 🆕 **İSTEĞE BAĞLI**, hepsi-ya-hiç kuralına GİRMEZ (22 Eylül 2026, `04` K-151 · Y1) | her unicast (veri ve kontrol) sonucu kesinleşince; başarısızlıkta `iletim_basarisiz`den ÖNCE | **niyet döndürmez** |

🆕 **Veri başlığı (K-151 · Y2):** protokol sınıfı isteğe bağlı
`veri_baslik_bayt` ile veri paketine eklediği yönlendirme başlığını bildirir
(yoksa 0); çerçeve o kadar uzar ve bayt yönlendirme ek yüküne (`nrl_*`) sayılır.

🔴 **İMZALAR 16 EYLÜL 2026'DA DEĞİŞTİ (K-131, denetim B4).** Kancalar
`(dugum, …, saat_s)` yerine bir **`Gozlem`** alıyor. `Gozlem` düğüm kimliğini
ve yerel saati zaten taşıdığı için hiçbir bilgi EKSİLMEDİ; donanım ölçümleri
(ölçülen gürültü · kanal meşguliyeti · kuyruk doluluğu · son iletim sonucu ·
komşu tablosu) eklendi. Aynı değişiklik `beacon_yuku(gozlem)` ve
`beacon_alindi(gozlem, komsu, yuk)` kancalarına da uygulandı.
🔒 **Gözlem penceresi BÜYÜMEDİ** (P6 hâlâ bağlayıcı): değişen tek şey,
pencerenin ne zaman sunulduğudur. Bu çağrılarda `gozlem.paket` `None`dur.

🔴 **KANCALAR BEYAN DA DÖNDÜREBİLİR — 16 Eylül 2026 (K-134).** Niyet demeti
artık `KontrolIstegi | Uyandirma | Beyan` taşır. Sebebi ölçülmüş bir
asimetridir: `Karar.beyan` protokolün *"rotam koptu"* diyebildiği TEK kanaldı
ve yalnız **veri gönderme kararında** açılıyordu. Ama protokol kopmayı orada
öğrenmez — `iletim_basarisiz`te ya da HELLO zaman aşımında öğrenir. Kuyruğu
boş bir düğüm hiçbir şey bildiremiyordu; AODV kopmayı zaten gönderirken
öğrenir, OLSR ise HELLO'dan ve o düğümün trafiği olmayabilir. Yani
`algilama_duyarliligi` **proaktif aileyi sistematik olarak düşük** gösterirdi
(`06` §8 koşul 3'ün ihlali).

🔴 **DÜŞME SEBEBİ BEYANA BAKAR — 16 Eylül 2026 (K-134).** `Karar(sonraki=None)`
ile birlikte `Beyan("rota_gecersiz")` verilirse paket `hedef_yok` yerine
**`rota_gecersiz`** sebebiyle düşer. Bu cümle `gozlem/karar.py`de baştan
yazılıydı ama DAL KODDA YOKTU — ölçüldü: 320 beyan, o sebeple 0 düşüş.
AODV'de ayrım gerçektir (RFC 3561 §6.11: geçersiz rotası olan ara düğüm RERR
gönderir ve paketi düşürür).

`gozlem.saat_s` alıcının **yerel** saatidir. `bicim` mesaj biçiminin adıdır
(`str`).
Kısmi kanca taşıyan protokol → kurulumda `KontrolDuzlemiHatasi`. Kancaları
taşımayan protokol `Karar.niyetler` doldurursa → `KontrolDuzlemiHatasi`.
⚠️ Kancaları taşımayan protokolün davranışı **birebir aynıdır** (P7 ·
§06 regresyon).

---

## 03 · SİMÜLATÖR SÖZLEŞMESİ (`sim2/kanal/cerceve.py` · `sim2/kosum/kontrol*.py`)

### 03.1 · Çerçeve (karar 1)
`cerceve_kur(konfig, "kontrol", mesaj_bayt=n)` → `bayt = n + Σ KONTROL_KAPSULLEME`:

| katman | bayt | kaynak |
|---|---|---|
| 802.11 MAC başlığı (veri, 3 adres) | 24 | IEEE 802.11-2016 §9.3.2.1 |
| 802.11 FCS | 4 | IEEE 802.11-2016 §9.2.4.8 |
| LLC/SNAP | 8 | RFC 1042 |
| IPv4 başlığı (seçeneksiz) | 20 | RFC 791 §3.1 |
| UDP başlığı | 8 | RFC 768 |
| **toplam** | **64** | `kontrol_kapsulleme_bayt()` |

Süre ve hataya açık bit **aynı** `cerceve_kur` satırından (PHY önbelgesi dâhil).
`kontrol` tipinde `bayt=` verilemez; başka tipte `mesaj_bayt=` verilemez.
`veri` · `onay` · `beacon` boyutları **değişmedi**. ⚠️ Köken: `SINANMAMIS`
(`02`de açılmadı).

### 03.2 · Kuyruk ve öncelik
- Düğüm başına **ayrı** kontrol FIFO'su; kapasite = `Konfig.kuyruk_kapasitesi`
  (ikinci bir sayı yok). Dolu kuyruk → `kuyruk_tasmasi` (kontrol defteri).
- **Öncelik:** uçuşta kontrol varsa o; yoksa uçuşta VERİ yoksa kuyruktaki
  kontrol; yoksa veri. Uçuştaki bir veri MSDU'sunun yeniden denemeleri
  kesilmez. *(NS-2 `PriQueue` geleneği.)*
- Kontrol çerçeveleri **veri korunum defterine girmez** ve mutabakatı etkilemez.

### 03.3 · MAC (karar 3)
- Aynı `Dcf` durum makinesi ve aynı `mac_geri_cekilme` düğüm alt akışı.
- Aynı `gonderim.gonder`: duyma kümesi, geri çekilme donması, alıcı zinciri
  (önbelge · gövde PER · yakalama · yarım çift).
- **UNICAST:** gönderen onay bekler (`SIFS + onay + slot`); gelmezse `Dcf`
  pencereyi katlar ve `yeniden_deneme_siniri`ne kadar **aynı mesajı aynı
  uçuş numarasıyla** yeniden dener; sonra `unicast_vazgecilen`.
- **YAYIN:** onay yok, yeniden deneme yok; iletim bitince `yayin_gonderilen`.
- 🔒 Kontrol onayı **yalnız gönderenin kendisi çözdüğünde** sayılır.

### 03.4 · Teslim (karar 4)
| alıcıdaki durum | ne olur |
|---|---|
| alıcı zinciri başarısız | hiçbir şey (kanca çağrılmaz) |
| başarılı · YAYIN | `kontrol_alindi(yayin=True)` · `teslim_yayin` |
| başarılı · UNICAST · hedef bu düğüm · yeni numara | onay + `kontrol_alindi(yayin=False)` · `teslim_unicast` |
| başarılı · UNICAST · hedef bu düğüm · tekrar | onay · **teslim yok** · `tekrar_bastirilan` |
| başarılı · UNICAST · başkasına adresli | **teslim yok, onay yok** · `baskasina_adresli` |

Tekrar bastırma anahtarı `(gönderen, uçuş_no)` — veri yolunun kuralıyla aynı.

### 03.5 · Zamanlayıcılar (karar 5 · karar 2)
| | PERİYODİK | DİNAMİK |
|---|---|---|
| istek | `zamanlayicilar()` — bir kez | `Uyandirma` niyeti — her an |
| kanca | `zamanlayici_doldu` | `uyandi` |
| faz / an | `U(0, periyot)`, `beacon_faz` **düğüm alt akışı**, etiket sırasıyla | `t + gecikme_s` |
| zincir | `t_{k+1} = t_k + periyot`, `≤ kosu_bitis_s` | tek atış |
| alt sınır | `periyot ≥ slot_s` | `gecikme_s ≥ slot_s` |
| tavan | ilanla sınırlı (etiket başına 1 bekleyen) | **`BEKLEYEN_UYANDIRMA_TAVANI = 256` / düğüm** |
| ihlal | `KontrolDuzlemiHatasi` | alt sınır: `KontrolDuzlemiHatasi` · tavan: **`UyandirmaTavaniAsildi`** |

🔒 Tavan aşımında zamanlayıcı düşürülmez: koşu, aşımın olduğu olayda durur ve
mesaj düğümü, anı ve sayıyı taşır — aynı tohumda birebir aynı (P5).
⚠️ Köken: `SINANMAMIS`; tepe bekleyen sayısı her satıra yazılır.

> 🔴 **Numara düzeltmesi (15 Eylül 2026).** Y3'ün üç bölümü eklenirken
> numaralar ÇAKIŞMIŞTI: 03.6, 03.7 ve 03.8 belgede ikişer kez geçiyordu.
> Y3 bölümleri numaralarını korudu (K-121 onlara atıf yapıyor); eski üçlü
> 03.9–03.11'e taşındı. Sözleşmede hiçbir madde değişmedi.

### 03.6 · İletim başarısızlığı (Y3 · R3)
`iletim_basarisiz` MAC bir UNICAST çerçeveden vazgeçtiği anda çağrılır:
veri yolunda onay penceresi dolup yeniden deneme hakkı bittiğinde,
kontrol yolunda `unicast_vazgecilen` anında. `hedef` gönderenin denediği
komşudur ve uçuştan İNDİRİLMEDEN önce okunur; `tur` `veri` ya da
`kontrol`dur. YAYIN çerçevesi onaylanmadığı için buraya hiç gelmez.
🔒 Çağrı sayılır (`basarisiz_bildirim`): sayılmasaydı kancanın hiç
çağrılmadığı bir koşu ile her vazgeçmede çağrıldığı koşu satırdan ayırt
edilemezdi. Kontrol düzlemi taşımayan protokolde çağrı YOKTUR ve satır
birebir aynı kalır.

### 03.7 · Titreşim (Y3 · R4)
`jitter_s > 0` ise simülatör `U(0, jitter_s)` çeker — `protokol_kesif`
akışının **düğüm alt akışından**. Protokol rastgelelik nesnesi görmez.

| niyet | titreşimin etkisi | defter |
|---|---|---|
| `KontrolIstegi` | kuyruğa GİRMEYİ geciktirir; mesaj o ana kadar `istenen` sayılmaz | `jitter_istenen` → `jitter_ates` |
| `Uyandirma` | `gecikme_s`in ÜSTÜNE eklenir; alt sınır (bir slot) `gecikme_s`e uygulanır | uyandırma defteri değişmez |

🔒 Kapalı denklem (uyandırmanınkiyle aynı biçim):
`jitter_istenen = jitter_ates + bekleyen_jitter`. Tutmayan satır
`gecerli=False` olur — bekleyen bir istek sessizce kaybolamaz.
⚠️ Titreşim kullanmayan protokolde `protokol_kesif` akışından HİÇ çekim
yapılmaz; bugünkü satırlar birebir aynıdır.

### 03.8 · Koşum beacon'ını kapatma (Y3 · R2)
Kontrol düzlemini KULLANAN protokol `kosum_beaconi = False` bildirebilir:
o protokolün düğümlerinde koşum düzeyindeki beacon hiç çizelgelenmez ve
gözlemdeki komşu listesi boş kalır. 🔒 Kancasız protokolde `False` →
`KontrolDuzlemiHatasi`: beacon'sız ve kontrol düzlemsiz bir protokol
kalıcı olarak kördür ve ölçülen şey kararı değil körlüğü olurdu.
Beacon fazları yine KURULUMDA çekilir, yani çekim dizisi kaymaz ve öteki
kollar etkilenmez. Satırda beyan:
`teshis.kontrol_duzlemi.kosum_beaconi_kapali_dugum`.

### 03.9 · Belirlenimcilik
Olaylar `(zaman, ekleme sırası)` ile sıralanır. Niyetler döndürüldükleri
sırayla uygulanır. `Karar.niyetler`, veri çerçevesi havaya çıktıktan sonra
aynı anda uygulanır. Kontrol düzlemi kullanılmıyorsa hiçbir olay eklenmez ve
hiçbir akış çekilmez.

### 03.10 · Bedel (karar 1 · 3)
Her kontrol iletimi (yeniden denemeler dâhil): `kontrol_cerceve += 1` ·
`kontrol_bayt += cerceve.bayt` · `kontrol_airtime_s += cerceve.sure_s`. Kontrol
onayı, veri onayıyla aynı biçimde `kontrol_*`a yazılır. 🔒 **Yeni sayaç
yok** — sayaç şeması özeti değişmez.

### 03.11 · Sonuç satırı
Yalnız kontrol düzlemi **kullanıldıysa**:
- `korunum`: `kontrol_mesaj_tamam` · `kontrol_uyandirma_tamam` ·
  `kontrol_kuyrukta` · `kontrol_ucusta` · `kontrol_bekleyen_uyandirma`;
  `gecerli` ikisini de içerir.
- `teshis.kontrol_duzlemi`: `defter` (13 alan) · `tepe_bekleyen_uyandirma` ·
  `bekleyen_uyandirma_tavani`.

**Kontrol defteri (düğüm başına, kapalı):**
```
istenen         = kuyruk_tasmasi + yayin_gonderilen + unicast_onaylanan
                  + unicast_vazgecilen + kuyrukta + ucusta
dinamik_istenen = dinamik_ates + bekleyen_uyandirma
```

---

## 04 · DEĞİŞMEYENLER — bağlayıcı

- Gözlem penceresi: 12 · **6** · 5 alan (P6). *(7 → 6: `bildirdigi_konum`
  kaldırıldı, K-131 — alan protokolden bağımsız olarak HER ZAMAN boştu.)*
- `veri`/`onay`/`beacon` çerçeve boyutları · beacon mekanizması · sayaç şeması.
- 🔒 Beyan kanalı genişledi (K-134) ama **sayaç şeması DEĞİŞMEDİ**: aynı üç
  sayaç (`kopma_algilanan` · `rota_kurtarildi` · `kopma_rota_gecersiz`) artık
  iki yoldan artabiliyor, üçüncü bir sayaç eklenmedi.
- `gonderilen_bayt` ve `son_iletim_sonucu` yalnız VERİ iletimini yansıtır
  (bugünkü hâl); `alinan_bayt` her başarılı alımı sayar (bugünkü hâl).
- `mac_*` sayaçları ve iletim sonucu kapalı kümesi yalnız veriyi sayar.
- Kontrol düzlemini kullanmayan protokolün sonuç satırı birebir aynı (§06).

---

## 05 · P1–P8 — kapılar (bağımsız gözlemle, boş geçmez)

| kapı | ne sınar | kanıt |
|---|---|---|
| **P1** | Boyut RFC alanlarından; kapsülleme tek kaynak; sığmayan değer kaçak taşıyamaz; `kontrol_*` sayaçları havaya çıkan çerçevelerle **birebir**, çift fatura yok | `Ortam.ekle` casusu |
| **P2** | Aynı MAC: kontrol eklenince veri zamanlaması değişir; onay yalnız unicast teslim/tekrarına; kayıplı kolda yeniden deneme gözlenir | veri ikizi · `OlayKuyrugu.ekle` casusu |
| **P3** | Teslim ⇔ fiziksel başarı, alıcı başına, **multiset eşitliği**; başkasına adresli sayısı birebir; kayıp > 0 | `AliciZinciri.cerceve_bitti` casusu |
| **P4** | Periyodik zincir kesin; ateş sayıları; dinamik ateş anı; iki mekanizmanın ayrımı; geçersiz ilan / slottan kısa uyandırma reddi | olay casusu · kayıt |
| **P5** | Tavan aşımı → `UyandirmaTavaniAsildi`, iki koşuda aynı mesaj; tavan altında düşürme yok | — |
| **P6** | Pencere büyümedi; niyet tiplerinde geri referans yok; `KontrolluProtokol` ↔ `KONTROL_KANCALARI` birebir; kısmi kanca ve kancasız niyet reddi | tip taraması |
| **P7** | Kontrol trafiği varken aynı tohum → birebir satır; `PYTHONHASHSEED` sonucu değiştirmez | alt süreç |
| **P8** | Karıştırıcı altında uçtan uca: kayıp > 0 ve başarı > 0; veri defteri + mutabakat + iletim sonucu **ve** kontrol defteri kapanır; her niyet deftere girer | tam satır |

Regresyon (kapı değil, ön koşul): değişiklik öncesi anlık kopyadan üretilen
35 sonuç satırı ile sonrası **alan alan** karşılaştırılır.

---

## 06 · KALAN RİSKLER — bu sözleşmenin kapatmadığı

| # | risk | sonucu |
|---|---|---|
| R1 | 🔴 **Veri onayı göndereni değil, onayı çözen HERHANGİ bir düğümü kredilendiriyor** (`teslim.onay_alindi` alıcıyı sormuyor). Ölçüldü (değişiklik öncesi kod, 40 s): göndericinin kendisinin **çözemediği** ama seyirci yüzünden başarılı sayılan onay **34 · 18 · 184** (`statik-yok` · `statik-surekli` · `bagimsiz-surekli`). Kontrol onayı doğru uygulandı; veri yolu düzeltilirse ölçülmüş sonuçlar değişir | iki onay semantiği ayrışık; öğrenci kararı |
| R2 | Koşum düzeyindeki **beacon hâlâ açık**; kendi HELLO'sunu gönderen bir protokol çift komşu trafiği üretir, gözlemdeki komşu tablosu hâlâ 1 s beacon'dan dolar | Faz 3'te protokol başına beacon kapatma/aralık kararı |
| R3 | **Bağ kopması geri bildirimi yok:** MAC vazgeçtiğinde protokol anında haberdar edilmez (AODV RERR/yerel onarım) | Faz 3 ön koşulu |
| R4 | **Protokolün rastgelelik kaynağı yok** (RREQ jitter, OLSR `MAXJITTER`) | `protokol_kesif` alt akışının sözleşmesi gerekli |
| R5 | Kapsülleme asimetrisi: veri 512 B toplam, kontrol mesaj + 64 B | `nrl_*` karşılaştırmasında kontrolü en çok 64 B pahalı gösterir |
| R6 | `BEKLEYEN_UYANDIRMA_TAVANI` ve `KONTROL_KAPSULLEME` `SINANMAMIS` | köken borcu 33 → 35 |
| R7 | Tavan **bekleyen** sayısını sınırlar, **oranı** değil: slot aralıklı zincirleme uyandırma yavaş ama belirlenimci bir koşu üretir | tepe/ateş sayısı satırda |
| R8 | Kontrol istatistikleri sayaç kütüğünde değil teşhiste; pencere ikizleri yok | Faz 3 başında şema kararı |

### 06.1 · 10 Eylül 2026 — kararlar ve öneriler (K-113)

Tablodaki "Faz 3" eski numaralamadır; bugünkü karşılığı **Aşama 2** (taban
protokoller). R2–R4'ün mekanizması protokollerden önce, Aşama 1'de hazırlanır.
Kapılar testlerde "§09" diye anılıyor; bu belgede §05'tir.

| # | durum |
|---|---|
| R1 | **Öğrenci kararı:** önce etkisi ayrı ölçülecek, sonra karar verilecek. Ölçüm tasarımı: aynı tohum ve kollarda bugünkü onay semantiği ile "onay yalnız gönderenin kendisi çözdüğünde sayılır" semantiği eşleştirilmiş koşulur; PDR, PSR, gecikme, yeniden deneme/vazgeçme, evre metrikleri ve kalibrasyon çıktıları (ρ, kâhin PDR'si) karşılaştırılır (`12` §3). Ölçüm betiği depoya yazıldı: `kalibrasyon/onay_semantigi.py` (K-112'deki ölçümün betiği depoda kalmamıştı). **Ölçüldü (11 Eylül, `04` K-114 §4.2):** kısa pencerede 4 kol × 2 kâhin × 8 tohum. PDR farkı hiçbir hücrede çözünürlük üstünde değil: altında 5, karar yok 3, üçü de hareketli kollarda. Evre metrikleri ve ρ ölçülmedi, çünkü tam uzunluk gerekir. Seyirci kredisi alan iletimde veri zaten ulaşmış oluyor; kusur göndericinin bilgisini ve MAC sayaçlarını değiştiriyor ve karıştırıcı altında büyüyor. 🟢 **Uygulandı (11 Eylül, `04` K-115):** veri onayı artık yalnız göndericinin kendisi çözdüğünde işleniyor (`07` §18 Y2). Kapısı: düz koşu, Y2'den önce kaydedilmiş `duzeltilmis` parmak izleriyle 16/16 birebir (`python -u kalibrasyon/onay_semantigi.py y2kapi kisa_2026-09-11`) |
| R2 | Öneri: koşum düzeyindeki beacon, kontrol düzlemini kullanan protokol için kapatılabilir olur; komşu tablosu protokolün kendi HELLO'sundan dolar. Gözlem penceresi değişmez. `sim2` değişikliği — yapı onayı gerekir |
| R3 | Öneri: MAC bir unicast iletimden vazgeçtiğinde protokole bir **iletim sonucu** kancası gelir ve protokol niyet döndürebilir (AODV RERR, yerel onarım). Gönderenin kendi MAC'inin bildiği bir olaydır; `05` §3.1'deki "zaman aşımı" gözleminin olay biçimidir. Yapı onayı gerekir |
| R4 | Öneri: protokol başına, düğüm başına ayrı bir rastgelelik alt akışı (RREQ jitter, OLSR `MAXJITTER`); kontrol düzlemini kullanmayan protokolde hiç yaratılmaz, dolayısıyla bugünkü satırlar değişmez. Yapı onayı gerekir |
| R8 | 🟢 **Uygulandı (11 Eylül, `04` K-115):** 13 defter alanı sayaç kütüğünde pencere ikizleriyle, mesaj biçimi dökümü teşhiste. **Öğrenci onayladı (10 Eylül); yapısı `07` §18 Y1.** Öneri: kontrol defterinin **toplam** alanları (yayın gönderilen, unicast onaylanan ve vazgeçilen, kontrol kuyruk taşması, yayın ve unicast teslim, dinamik ateş) sayaç kütüğüne girer ve pencere ikizleri otomatik türer; böylece `nrl_*` ve U3 ölçüm penceresinde okunabilir. Düğüm başına ayrıntı ve **mesaj biçimi başına** bayt/çerçeve dökümü teşhiste kalır (HELLO ↔ TC ↔ RREQ yükünü ayırmak için). Bedeli: sayaç şeması özeti değişir; ana deney satırları zaten yeniden üretileceği için ölçülmüş bir sonucu etkilemez. Yapı onayı gerekir |

**11 Eylül 2026:** R2–R4'ün (`07` §18 Y3) ve R8'in (`07` §18 Y1) yapısı öğrenci
tarafından onaylandı. Tablodaki "yapı onayı gerekir" ifadeleri o tarihten
önceki durumu anlatır.

**14 Eylül 2026 — R2, R3 ve R4 🟢 UYGULANDI** (`04` K-121). Sözleşmedeki
karşılıkları §02.2 · §02.3 · §02.5 · §03.6 · §03.7 · §03.8. R1 zaten
11 Eylül'de kapanmıştı (Y2, K-115). Açık kalan riskler: R5 (kapsülleme
asimetrisi, beyanlı) · R6 (iki sabitin kökeni) · R7 (tavanın oran değil
sayı sınırlaması, beyanlı).
