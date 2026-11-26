# 13 · KONTROL DÜZLEMİ — protokolün YAPABİLECEKLERİ

> **Durum: sözleşme uygulandı.** Güncel 13 Ekim 2026 (26 Kasım: §07'deki DESPARETE cümlesi yeni tasarıma göre); tarihçe ve kapanmış risklerin ayrıntısı `v2/arsiv/13-KONTROL-DUZLEMI-*.md`. Bölüm numaraları kodda atıflı, korunur (testlerdeki "§09" = §05). Karar K-112 · kapılar `tests2/test_kontrol_duzlemi.py` (bağlayıcı) · `python -u kalibrasyon/kontrol_duzlemi_kapilari.py` (40 düğümde kanıt).

---

## 00 · Neden

Kapsam yalnız MEKANİZMA; protokol gerçeklemeleri `protokoller/`de. `05` protokolün ne GÖRECEĞİNİ kilitler, bu belge ne YAPABİLECEĞİNİ — gözlem penceresini genişletmez.

## 01 · Beş tasarım kararı

| # | karar | uygulandığı yer |
|---|---|---|
| 1 | mesaj boyutu RFC alanlarından; PHY/MAC/çerçeve ek yükü tek kaynak `cerceve_kur()` | `MesajBicimi.bayt` · `KONTROL_KAPSULLEME` |
| 2 | uyandırma kuyruğunda düğüm başına tavan; aşımda **deterministik FAIL** | `BEKLEYEN_UYANDIRMA_TAVANI` · `UyandirmaTavaniAsildi` |
| 3 | kontrol ve veri **aynı** kanal/MAC/çekişme/kayıp fiziği | aynı DCF alt akışı, `gonderim.gonder`, alıcı zinciri |
| 4 | `kontrol_alindi()` yalnız başarılı teslimde; yayında alıcı başına | `kosum/kontrol.py::cerceve_alindi` |
| 5 | periyodik ve dinamik zamanlayıcı ayrı mekanizma | `zamanlayicilar/zamanlayici_doldu` ↔ `Uyandirma/uyandi` |

## 02 · API — protokole görünen (`sim2/gozlem/`)

Protokol **çağırmaz, niyet döndürür**; tipler donmuş, simülatöre geri referans yok (P6).

- **02.1 `MesajBicimi(ad, alanlar, tekrarli=())`** — `alanlar` `(ad, bit)` demeti (sabit genişlik), `tekrarli` sayı demeti taşıyan alanlar; adlar tekil. Boyut, projede TEK hesap: `bayt(yuk) = ⌈(Σ sabit bit + Σ len·bit) / 8⌉`.
- **02.2 `KontrolIstegi.kur(hedef, bicim, yuk, jitter_s=0.0)`** — `hedef` `None` (yayın) ya da düğüm (unicast) · `yuk` tam olarak biçimin alanları · `int` `0 ≤ v < 2^bit`, `bool` her genişlikte, `float` yalnız 32 bitlik alanda · tekrarlı alan demet · `jitter_s ≥ 0`. Taşınan bilgi ödenen bitten fazla olamaz.
- **02.3 `Uyandirma(gecikme_s, etiket, jitter_s=0.0)`** — dinamik zamanlayıcı; `gecikme_s > 0`, alt sınır ve tavan simülatörde.
- **02.4 `Karar.niyetler`** — `KontrolIstegi | Uyandirma`; `Beyan` buraya giremez (`Karar.beyan` ayrı alan).
- **02.5 Kancalar** (`KontrolluProtokol`, **hepsi ya da hiçbiri**; her biri bir `Gozlem` alır — düğüm kimliği ve yerel saat içinde; `gozlem.paket` `None`):

| kanca | çağrılma | dönüş |
|---|---|---|
| `zamanlayicilar()` | kurulumda bir kez | `{etiket: periyot_s}` |
| `zamanlayici_doldu(gozlem, etiket)` | ilan edilmiş periyot doldu | niyet demeti |
| `uyandi(gozlem, etiket)` | bir `Uyandirma` doldu | niyet demeti |
| `kontrol_alindi(gozlem, gonderen, bicim, yuk, yayin)` | yalnız başarılı teslim | niyet demeti |
| `iletim_basarisiz(gozlem, hedef, tur)` | MAC bir unicast çerçeveden **vazgeçti** | niyet demeti |
| `iletim_sonucu(gozlem, hedef, basarili, tekrar, tur)` — **isteğe bağlı**, hepsi-ya-hiç kuralına girmez (K-151) | her unicast (veri ve kontrol) sonucu; başarısızlıkta `iletim_basarisiz`den önce | **niyet döndürmez** |
| `cerceve_duyuldu(gozlem, gonderen, tur, hedef, rssi_dbm, paket)` — **isteğe bağlı** (K-172) | çözülen her çerçeve (veri · onay · beacon · kontrol · konay), bana ya da başkasına; çerçeve işlenmeden önce | **niyet döndürmez** |

Kanca niyet demetleri `Beyan` da taşıyabilir (K-134) — kopma, öğrenildiği yerde bildirilir; aksi hâlde kuyruğu boş düğüm bildiremez ve algılama duyarlılığı proaktif aileyi düşük gösterirdi. `Karar(sonraki=None)` + `Beyan("rota_gecersiz")` → paket `rota_gecersiz` sebebiyle düşer (yoksa `hedef_yok`); + `Beyan("politika")` → `politika` sebebiyle (protokol paketi bilerek taşımıyor; rota olayı değil, yalnız `Karar`da, `rota_gecersiz`le birlikte verilemez — K-171). Protokol isteğe bağlı `kimlik_parametreleri()` bildirirse değerleri koşu kimliğine girer (K-171). Protokol sınıfı isteğe bağlı `veri_baslik_bayt` bildirir (K-151): veri çerçevesi o kadar uzar, bayt `nrl_*`e sayılır. `beacon_yuku(gozlem)` · `beacon_alindi(gozlem, komsu, yuk)` da gözlem alır. Kısmi kanca ya da kancasız protokolün niyet döndürmesi → `KontrolDuzlemiHatasi`; kancasız protokolün satırı birebir aynı.

## 03 · Simülatör sözleşmesi (`sim2/kanal/cerceve.py` · `sim2/kosum/kontrol*.py`)

- **03.1 Çerçeve:** `bayt = mesaj + 64` (802.11 MAC başlığı 24 · FCS 4 · LLC/SNAP 8 · IPv4 20 · UDP 8; kökeni KAYNAK, `02` G15 · G16). Süre ve hataya açık bit aynı `cerceve_kur` satırından. `veri`/`onay`/`beacon` boyutları değişmedi.
- **03.2 Kuyruk:** düğüm başına ayrı kontrol FIFO'su (kapasite `kuyruk_kapasitesi`; dolunca `kuyruk_tasmasi`). Öncelik: uçuşta kontrol → uçuşta veri yoksa kuyruktaki kontrol → veri; uçuştaki veri MSDU'sunun yeniden denemeleri kesilmez (NS-2 `PriQueue`). Kontrol, veri korunum defterine girmez.
- **03.3 MAC:** aynı `Dcf`; unicast onay bekler, `yeniden_deneme_siniri`ne kadar aynı uçuş numarasıyla dener, sonra `unicast_vazgecilen`; yayın onaysız ve tekrarsız. Onay yalnız gönderenin kendisi çözdüğünde sayılır (veri yolunda da, Y2).
- **03.4 Teslim:** alıcı zinciri başarısız → hiçbir şey · yayın → `kontrol_alindi(yayin=True)` · unicast bu düğüme yeni → onay + teslim · tekrar → onay, teslim yok (`tekrar_bastirilan`) · başkasına adresli → teslim de onay da yok. Tekrar anahtarı `(gönderen, uçuş_no)`.
- **03.5 Zamanlayıcılar:** periyodik — faz `U(0, periyot)` (`beacon_faz` alt akışı), zincir `t_k + periyot`, etiket başına 1 bekleyen · dinamik — `t + gecikme_s`, tek atış, **düğüm başına en çok 256 bekleyen**; ikisinde de alt sınır bir slot. Tavan aşımında koşu o olayda durur, mesaj düğümü, anı ve sayıyı taşır (P5).
- **03.6 İletim başarısızlığı** (R3): veri yolunda onay penceresi ve yeniden deneme bitince, kontrol yolunda `unicast_vazgecilen` anında; `hedef` uçuştan indirilmeden okunur; çağrılar sayılır (`basarisiz_bildirim`).
- **03.7 Titreşim** (R4): `U(0, jitter_s)`, `protokol_kesif` akışının düğüm alt akışından; istekte kuyruğa girmeyi geciktirir, uyandırmada gecikmenin üstüne eklenir. Kapalı denklem `jitter_istenen = jitter_ates + bekleyen_jitter`; tutmazsa satır `gecerli=False`. Titreşimsiz protokolde bu akıştan çekim yok.
- **03.8 Koşum beacon'ı** (R2): kontrol düzlemli protokol `kosum_beaconi = False` bildirebilir (üç taban protokol ve DESPARETE bildiriyor); kancasız protokolde yasak (kalıcı körlük). Beacon fazları yine kurulumda çekilir.
- **03.9 Belirlenimcilik:** olaylar `(zaman, ekleme sırası)`; niyetler döndürüldükleri sırayla. Kontrol düzlemi kullanılmıyorsa hiçbir olay ve çekim eklenmez.
- **03.10 Bedel:** her kontrol iletimi (yeniden denemeler dâhil) `kontrol_cerceve` · `kontrol_bayt` · `kontrol_airtime_s`'e; kontrol istatistikleri sayaç kütüğünde pencere ikizleriyle (R8), mesaj biçimi dökümü teşhiste.
- **03.11 Sonuç satırı** (kontrol düzlemi kullanıldıysa): `korunum` — `kontrol_mesaj_tamam` · `kontrol_uyandirma_tamam` · kuyrukta · uçuşta · bekleyen; `teshis.kontrol_duzlemi` — defter (13 alan) · tepe bekleyen uyandırma. Defter kapalı: `istenen = kuyruk_tasmasi + yayin_gonderilen + unicast_onaylanan + unicast_vazgecilen + kuyrukta + ucusta` · `dinamik_istenen = dinamik_ates + bekleyen_uyandirma`.

## 04 · Değişmeyenler — bağlayıcı

Gözlem penceresi 17 · 6 · 7 = 30 alan (P6; `05` §5) · `veri`/`onay`/`beacon` boyutları · sayaç şeması (beyan kanalı genişledi ama üç kopma sayacı aynı) · `gonderilen_bayt`, `son_iletim_sonucu` ve `mac_*` yalnız veriyi yansıtır · kontrol düzlemini kullanmayan protokolün satırı birebir aynı.

## 05 · P1–P8 — kapılar (bağımsız gözlemle, boş geçmez)

| kapı | ne sınar |
|---|---|
| P1 | boyut RFC alanlarından; kapsülleme tek kaynak; sığmayan değer taşınamaz; `kontrol_*` havaya çıkan çerçevelerle birebir, çift fatura yok |
| P2 | aynı MAC: kontrol eklenince veri zamanlaması değişir; onay yalnız unicast teslim/tekrara; kayıplı kolda yeniden deneme ve unicast vazgeçme gözlenir |
| P3 | teslim ⇔ fiziksel başarı, alıcı başına (multiset eşitliği); başkasına adresli birebir; kayıp > 0 |
| P4 | periyodik zincir kesin; dinamik ateş anı; iki mekanizmanın ayrımı; geçersiz ilan ve slottan kısa uyandırma reddi |
| P5 | tavan aşımı → `UyandirmaTavaniAsildi`, iki koşuda aynı mesaj; tavan altında düşürme yok |
| P6 | pencere büyümedi; niyet tiplerinde geri referans yok; kısmi kanca ve kancasız niyet reddi |
| P7 | kontrol trafiği varken aynı tohum → birebir satır; `PYTHONHASHSEED` sonucu değiştirmez |
| P8 | karıştırıcı altında uçtan uca: kayıp ve başarı > 0; veri defteri, mutabakat, iletim sonucu ve kontrol defteri kapanır |

## 06 · Riskler

| # | açık risk | durum |
|---|---|---|
| R5 | kapsülleme asimetrisi: veri 512 B toplam, kontrol mesaj + 64 B | `nrl_*`de kontrolü en çok 64 B pahalı gösterir (beyanlı) |
| R7 | tavan bekleyen **sayısını** sınırlar, oranı değil | tepe/ateş sayısı satırda (beyanlı) |

Kapanmış riskler (koddaki atıflar için): R1 seyirci onay kredisi → onay yalnız gönderen çözünce (K-115) · R2 koşum beacon'ı kapatılamıyordu → §03.8 · R3 MAC vazgeçmesi bildirilmiyordu → §02.5, §03.6 · R4 protokolün rastgelelik kaynağı yoktu → §02.2, §02.3, §03.7 · R6 tavan ve kapsülleme kökeni → KAYNAK ve ÖLÇÜLMÜŞ (K-203, K-214) · R8 kontrol sayaçlarının pencere ikizi → §03.10.

## 07 · Uçtan uca kopya — D-23 · K-231

JarmRout her veri paketini iki düğüm-ayrık yoldan gönderir (Pu 2018 §VI.B; K-230); DESPARETE'de kopyanın kullanılıp kullanılmayacağı yeni tasarımın iletim kararında (`18`, B5) karara bağlanır; ilk taslaktaki PROTECT (Faz 5.4) alınmadı. Tanımlar ölçmeden önce (denetim D-23):

- **İstek:** `Karar(sonraki=j, kopyalar=(k, …))` — paket `j`ye, eşleri `k`lere. `kopyalar` yalnız gönderilen pakette; tekil ve `sonraki`den farklı. Eş düğümün kuyruğunun sonuna girer ve kuyruk başına gelince protokole yeniden sorulmadan o komşuya iletilir (karar kopya anında verildi). Kuyruk doluysa eş `kuyruk_tasmasi` ile düşer.
- **Kimlik:** eş aynı paketin kopya numaralı eşidir (`Paket.kopya` ≥ 1, ağ genelinde tekil); kimliği aynıdır, gözlem penceresine açılmaz.
- **PDR:** hedefte ilk varan eş teslim sayılır (gecikme onun anıyla); sonraki eşler `kopya_bastir` ile defterden çıkar, ikinci kez teslim SAYILMAZ. Paket düzeyi PDR paket defterindedir.
- **Korunum:** `üretilen + kopya_üretilen = teslim + kopya_bastırılan + düşen + kuyrukta + uçuşta`; mutabakat eşleri de sayar. Kopya varsa `düşen` eş düzeyindedir (eşi teslim edilmiş paketin düşen eşi de sayılır); kayıp anatomisi teslim edilmemiş paketin kaybını SON düşen eşine atfeder.
- **Fatura:** eşler VERİ çerçevesidir; yayın süresi ve MAC sayaçları veri yükünde, kontrol yükünde (`nrl_*`) değil.
- **U1 ve kâhin:** kâhin kopyalamaz; kopyalayan protokolün kâhine oranı aynı tanımla (paket düzeyi PDR) hesaplanır, kopyanın bedeli veri yükünde raporlanır.
- **Kaynak rotası (K-232):** `Karar(rota=…, kopya_rotalari=…)` paketin ve eşlerinin başlığına ara düğümleri yazar (DSR, RFC 4728 §6.7); protokol sınıfı `rota_adres_bayt` bildirir, çerçeve adres başına o kadar uzar ve bayt `veri_baslik_bayt`'a (yönlendirme ek yükü) sayılır. Başlıkta yazdığı için gözlem penceresinde `PaketGorunumu.rota`. Testler `tests2/test_kaynak_rotasi.py`.
- **Değişmeyen:** kopya istemeyen protokolde hiçbir olay eklenmez ve sonuç satırına alan girmez (`kopya_uretilen` · `kopya_bastirilan` yalnız kopya kullanılınca); regresyon birebir. Testler `tests2/test_kopya.py`.
