# 07 · SİMÜLATÖR TASARIMI

> **Güncel:** 25 Eylül 2026 · **Türü:** bilgi belgesi — simülatörün ne olduğu, neden böyle olduğu, öğrenci kararlarının tek listesi (§15).
> Öz sürüm; uygulanmış öneriler, yapı planının ayrıntısı (§18) ve kapanmış ayrışma satırları: `v2/arsiv/07-SIMULATOR-TASARIMI-2026-09-25.md`. Karar geçmişi `04`.
> İşaretler: 🟢 uygulandı · 🟡 karar verildi, uygulanacak · 🔵 öneri, karar bekliyor · ⚪ açık soru.
> 🔴 **İKİ DÜNYA (28 Eylül notu):** §02–§05 ve §09'un sayıları **eski 1:50 dünyanındır** (`Konfig` varsayılanı, eski regresyon vakaları ve kalibrasyon tabloları onunla birebir). Deneyler **referans dünyada** (`referans_2026`, K-181) koşar: telsiz, kanal, sürü, tehdit ve trafiğin 1:1 sayıları `14`te, Faz 1–3'ün mekanizmaları (işlem kazancı, güce dayalı taşıyıcı dinleme + ED-CCA, ARF, yayılım gecikmesi, gerçekçi karıştırıcı, gözlem v2, düğüm kaybı, enerji) `15`te, Faz 4'ün kalibrasyonu `04` K-183…K-192'de. Referans dünyada alan 33 km, α = 2, gölgeleme σ 3 dB (hücre 2,5 km), Rician K 10 dB, yeniden deneme 7, birincil hücre `formasyon · yere_toplama · derin_sizma · sürekli` 10 W (`06` §0.4.4).

---

## 01 · Ne ölçüyoruz

*Karıştırma altında, önerilen yönlendirme protokolü AODV / OLSR / AOMDV'ye göre [şu metriklerde] [şu kadar] farklı davranır.* İddianın savunulması için: tehdit modeli · ağ modeli · sadık taban protokoller · iddiayı ölçen metrikler · ön-kayıtlı istatistik.

| aletin sınavı | durum |
|---|---|
| iç tutarlılık | 🟢 korunum + mutabakat |
| analitik | 🟢 Bianchi · sönümleme varyansı · yol kaybı |
| dış çapa | 🟢 Li vd.: mekanizma doğrulandı, sayı farkı yol kaybı üsteliyle açıklandı (`09`, K-108) |

## 02 · Dünya modeli

- Hacim, sürünün kütle merkezine bağlı **hareketli gözlem çerçevesidir**; hızlar göreli. Yer referanslı varlıklar (karıştırıcılar) bu çerçevede hareket eder.
- **Ölçek 1:50:** kutu ~90 km, hızlar 45–135 km/h, verici 2,5 W (K-101). Doppler tam ölçek hızından (dalga boyu ölçeklenmez, K-102).
- **Ölçek tutarlılığı bir kapıdır:** tam ölçekteki verici fiziksel olarak var olabilmeli (α = 3'ü eledi, K-097).

## 03 · Mobilite 🟢

**03.1 · Kapı:** Θ = ortalama rota ömrü / 15 s (OLSR `TOP_HOLD_TIME`, RFC 3626) ≥ 3; altında OLSR'ın topoloji bilgisi kullanılmadan bayatlar (K-101). Rota ömrü yavaş SINR bağ tanımı ve Kaplan–Meier ile ölçülür; her satır Θ_OLSR ve Θ_AODV'yi taşır (K-122).

**03.2 · Kollar** (03.3 yüksek çalkantı · 03.4 mobilite modeli önerisi arşivde):

| kol | model | Θ_OLSR · Θ_AODV | not |
|---|---|---|---|
| statik | sabit | ∞ | U1 referansı |
| bağımsız | Gauss-Markov 3B, 0,25–0,75 m/s (45–135 km/h) | 3,25 · 16,3 | |
| görev | müfreze + istasyon tutma | 3,99 · 19,9 | 10 × 4 grup |
| formasyon (çekirdek) | istasyon = yerleşim, istasyon tutma (K-118) | 2,31 · 11,5 | kestirici aşağı yanlı (soldan kesme, sansür) |
| yüksek çalkantı (keşifsel, **03.3**) | Gauss-Markov 0,5–1,5 m/s | 1,78 · 8,9 | 🟡 saklanmaz (öğrenci): iki Θ ve "OLSR zarfı dışında" etiketiyle, çekirdek hipotezlere girmeden raporlanır |

Üreticiler: `python -u kalibrasyon/theta_kollari.py` · `python -u kalibrasyon/formasyon_olcumu.py`. Formasyonda duvar teması nadir (%0,02), sayılır ve beyan edilir (K-119).

## 04 · Kanal ve fizik 🟢

| bileşen | karar |
|---|---|
| yol kaybı | log-mesafe, **α = 2,0** (hava-hava serbest uzay) |
| gölgeleme | log-normal, korelasyonlu, σ = 3 dB |
| sönümleme | Rician, FIR ile durumsuz, **K = 6 dB** · ⚪ K'nin kaynağı doğrulanacak (`02` §S1) |
| anten | yarım dalga dipol |
| girişim | toplamsal, parça başına SINR; karıştırıcı gücü alıcıda eklenir |
| PER | önbelge (DBPSK) + gövde (DQPSK 2 Mb/s) ayrı; SINR eşiği 16 dB (K-091) |
| MAC | 802.11b DCF temel erişim; Bianchi ile ±%15 · ⚪ sabitlerin kaynağı (`02` §S2) |

"Menzil" bağlantı yarıçapı değil, verici gücünün çapasıdır; bağ kümesi kanaldan ölçülür (K-098). Fizik ablasyon bayrakları: `golgeleme_acik` · `sonumleme_acik` · `anten_deseni_acik` · `yakalama_etkisi_acik` · `saat_senkron`.

## 05 · Tehdit modeli 🟢

**05.1 · Şart:** karıştırılan bölge alanın bir parçası olmalı — tamamı kapanırsa dolaşılacak yer kalmaz ve "fark yok" sorunun yokluğudur.

**05.2 · Sınıflar ve çalışma noktası** (tek merkez, açılma 150 s): **−15,0 dBm · ρ = 0,258** (ρ engellenen bağ oranı; ölçüt: 30 tohumda birden çok çok-üyeli bileşen yokken en büyük ρ). Sınıflar **harcanan ortalama güçte** eşitlenir, ρ sonuçtur (K-103). Üretici: `python kalibrasyon/karistirici_gucu.py tarama`.

| sınıf | açık oranı | ort. dBm | ρ | bölünen tohum |
|---|---|---|---|---|
| sürekli | 1,000 | −15,0 | 0,258 | 0/30 |
| darbeli | 0,499 | −15,0 | 0,169 | 1/30 |
| reaktif | 0,000 | −∞ | 0 (trafikle ölçülür) | 0/30 |
| aldatıcı | 0,978 | −15,1 | 0,258 | 0/30 |
| taramalı | 0,325 | −19,9 | 0,081 | 0/30 (tepe eşit, beyanlı) |

**05.3 · Çoklu ve hareketli karıştırıcı — 05.3.1 aile parametreleri** (`tehdit_senaryosu`, TEDAVİ; öğrenci kararı K-119, uygulama K-120): toplam ortalama yayılan güç her ailede eşit; üye güç payı = 1 / (K × açık oranı).

| aile | K | platform ve yerleşim | yayın | hareket |
|---|---|---|---|---|
| `tekli_merkez` (referans) | 1 | sabit, alan merkezi | sürekli | yok |
| `cephe_hatti` | 3 | sabit, doğu kenarı y = 1/6 · 1/2 · 5/6 | sürekli | yok |
| `derin_sizma` | 1 | yer aracı 60 km/h, merkezden batıya | yay–sus–taşın (açık 15 · sessiz 15 s) | yalnız susarken (~32 m) |
| `hedef_koruma` | 2 | sabit, x = 0,75, y = 1/4 · 3/4 | sürekli (çevrim K-127'de kaldırıldı) | yok |
| `hava_eslik` | 1 | hava 200 km/h, kuzeye; karıştırılmış evrenin ortasında merkezden geçer | sürekli | ~300 m |

Keşifsel süreler: açık 3 · 45 s, sessiz 5 · 45 s. 🔴 Eşit ortalama güç eşit tepe güç değildir: çevrimli `hedef_koruma` tepe gücüyle ağı böldüğü için çevrim kaldırıldı (K-127). **05.4 · Protokol karıştırıcıyı görmez** (`05` §4).

## 06 · Trafik 🟢

- **06.1 · Eşler arası** (keşifsel): 10 akış × 4 pkt/s × 512 B, CBR + titreşim.
- **06.2 · Yere toplama** (birincil; Y4, K-116, K-126): geçit düğüm 0, batı kenarının ortasında sabit röle İHA; her düğümden geçide telemetri 1,0 pkt/s + geçitten 4 düğüme komut 0,25 pkt/s = 40 pkt/s (eşler arasıyla eşit). Teşhis: `teshis.kayip_yeri` (düşüş sebebi × geçide mesafe bandı).
- **Beyanlar** (öğrencinin dürüstlük şartı): geçidin yere bağı ideal (ortak mod) · tek geçit darboğazı (yük ölçütle seçildi, kayıp yeri raporlanır) · yer istasyonlu mimari yok · telemetri hızı kaynaksız · CBR basitleştirmedir.
- ⚠️ `Konfig`in varsayılan deseni hâlâ `esler_arasi` (§17 A8): ana deney aleti deseni açıkça vermeli.

## 07 · Protokol yüzeyi, kâhinler, üst referans

- **Görebilecekleri:** `05` · **yapabilecekleri:** `13` (kontrol düzlemi, kancalar, `iletim_sonucu`, bekleme tamponu). Her taban protokol kendi HELLO'sunu kullanır (`kosum_beaconi = False`).
- **07.1 · Kâhinler ölçüm aletidir:** ETX kâhini (beklenen iletimi küçültür) **kesin tavan değil** — atlama kâhini bazı tohumlarda onu geçer (K-110); en kısa yol kâhini ölçütün bedeli için. *ETX kâhini − atlama kâhini = ölçütün bedeli · kâhin − protokol = protokolün körlüğünün bedeli.*
- **07.2 · Üst referans** 🟢 (öğrenci, 10 Eylül; Y9): teslim olasılığı kâhini (bağ başarısı `1 − (1 − p)^(sınır+1)`, yol ölçütü `Σ −ln s`) ve tohum başına üç kâhinin en iyisi (**zarf**). "Üst referans", kesin sınır değil; PDR için, gecikme için değil. Üretici: `kalibrasyon/ust_referans.py`.

## 08 · Metrikler 🟢

- **08.1 · Var olanlar:** PDR (doğum kohortu; tüm koşu ve pencere) · gecikme yüzdelikleri · `nrl_cerceve/bayt/airtime` · COR · rota kurtarma gecikmesi Δ · üç kopma sayacı ve algılama duyarlılığı · evre metrikleri M1–M4 (`08`) · kontrol istatistikleri (pencere ikizli).
- **08.2 · PSR — öğrencinin tanımı (10 Eylül):** bağ düzeyinde, tek atlamada veri iletiminin başarısı — alıcının CRC testinden geçirdiği oran. `psr = veri_alim_hedefte / mac_deneme` (yeniden denemeler dâhil, yalnız veri). Onaya dayalı eski oran `mac_basari_orani` (K-115). 🔵 bağ başına dağılım ve kontrol PSR'si yok.

## 09 · Senaryo matrisi ve istatistik

- **09.1–09.3 · Ön-kayıt yalnız çekirdeği mühürler**; kalan hücreler keşifsel, tam raporlanır. Çekirdek taslağı: çekirdek mobilite × karıştırma koşulları × 4 protokol × yere toplama × **40 tohum** (öğrenci). Aday birincil hücre ve istatistik: `06` §0.4.
- **Çözünürlük** (yeni çekirdek hücre, 40 tohum, K-128): ETX kâhini PDR R = 0,0244 · eşleştirilmiş R = **0,0230**. Üretici: `python -u kalibrasyon/cozunurluk.py --tohum 40`.
- **09.4 · Derinlik** keşifsel bir eksendir (sıralama derinliğe göre değişiyor mu?). Düğüm sayısı N = 40 (C1, K-125).
- **09.5 · Karıştırıcısız kâhin tavanı:** statik 1,000 · 0,999 · 0,996 · bağımsız 0,915 · 0,844 (`python -u kalibrasyon/pdr_tavani.py 1`).
- **09.6 · "Simülatör protokolü kısıtlamaz"** kapısı üç durumlu (aktarma yoksa KOŞULMADI); marj raporlanır (`python -u kalibrasyon/bag_kumesi.py k`). TTL'in yapısal alt sınırı var ama değeri sonucu oynatıyor (K-110 EK-6).

## 10 · Doğrulama planı

| seviye | ne | durum |
|---|---|---|
| 1 · değişmez | korunum · mutabakat · test takımı | 🟢 `922 passed` (28 Eylül) |
| 2 · analitik | Bianchi · sönümleme · yol kaybı | 🟢 |
| 3 · literatür | Li vd. zincir kapasitesi | 🟢 eski dünyada mekanizma, H1 = 0,0871 tutmadı · **referans dünyada sabit hızda H1 = 0,127 TUTTU**, ARF açıkken 0,0426 (K-187; `09` sonu) |
| 4 · gerçekçilik | karıştırıcısız + kâhin → PDR ≈ 1 | 🟢 statikte; hareketlide 0,84–0,92 |
| 5 · ölçek tutarlılığı | tam ölçek verici var olabilir mi | 🟢 |
| 6 · duyarlılık | sonucu belirleyen sayılar gerekçeli mi | 🟢 (K-107); borç §11 |
| 7 · üreticiler | defterin andığı komutlar koşuyor mu | 🟢 `kalibrasyon/uretici_duman.py` |
| 8 · kontrol düzlemi | P1–P8 | 🟢 `kalibrasyon/kontrol_duzlemi_kapilari.py` |

Doğrulama listesinin tamamı (`DEVIR.md` §2) her aşama geçişinde bir kez koşulur.

## 11 · Parametre disiplini

**11.1 · Yedi kova** (öğrenci, 10 Eylül): TÜRETİLMİŞ · ÖLÇÜLMÜŞ (üretici komutlu) · KAYNAK (`02`de doğrulanmış) · DUYARSIZ (ölçümle) · TEDAVİ (deney ekseni) · KOL TANIMI (duyarlılık borcu taşır) · SINANMAMIŞ (görünür borç). Kayıtsız `Konfig` alanı kurulumu durdurur; modül ve kalibrasyon sabitlerini mimari denetimi tarar.

**11.2 · Bugün** (`python kalibrasyon/mimari_denetimi.py`, 25 Eylül): 169 parametre — TÜRETİLMİŞ 52 · ÖLÇÜLMÜŞ 19 · KAYNAK 7 · DUYARSIZ 16 · TEDAVİ 24 · KOL TANIMI 11 · **SINANMAMIŞ 40** · duyarlılık borcu 9. Hedef, mühürden önce SINANMAMIŞ = 0 ve borç = 0 — ya da borçlu sabitler eksen olarak ilan edilir. Bilinen SINANMAMIŞ öbekleri: 802.11b sabitleri · yeniden deneme sınırı (4; 802.11 kısa sınırı 7) · rota tamponu (64 paket · 30 s; AODV'de doluyor) · saat çifti · Rician K · kuyruk, TTL. **11.3 · Duyarlılık denetimi:** `python -u kalibrasyon/duyarlilik.py <kol> [parametre…]` (K-107; sınırlar: tek tek oynatma, kâhin kolları). Isınma ve ölçüm penceresi birlikte taranacak (öğrenci).

## 12 · Kapsam dışı — beyan edilir

Satırın kendi kapsam bölümü (`kapsam`) modellenmeyenleri konfiginden okur: aşağıdaki ilk üç satır yalnız ESKİ dünyada geçerlidir; referans dünyada üçü de modellenir (A2 · A3 · A4, K-173 · K-174 · K-177; beyan K-181).

| modellenmeyen | sonucu |
|---|---|
| hız uyarlaması (yalnız eski dünya) | kötü bağda 1 Mb/s'ye düşme yok |
| yayılma kazancı (yalnız eski dünya) | Barker'ın ~10 dB'i yok → karıştırıcı ~10 dB etkili görünür |
| enerji sezmeli CCA (yalnız eski dünya) | güçlü gürültü karıştırıcısı ertelemeye yol açmaz; yalnız aldatıcı sınıf CSMA'yı tetikler |
| çoklu kanal / frekans çevikliği | projenin öncülü — çözüm yönlendirme katmanında |
| RTS/CTS | temel erişim |
| yayılım gecikmesi · arazi/engel · patlamalı trafik | slotun kesri · 3B engelsiz · CBR |
| geçidin yere bağı | ideal kabul (§06) |
| karıştırıcının akıllı hedef takibi | ⚪ reaktif sınıf dışında yok |

## 13 · Gösterim

Sunumda simülasyon görselleştirilecek (öğrenci; Aşama 5). İz kanalı ölçüme dokunamaz — kapısı: iz açık/kapalı sonuç satırı birebir. Gösterilecekler: düğümler ve bağlar · karıştırıcı etki alanı ve hareketi · geçide rotalar · kopma/kurtarma · evre çizgili PDR eğrisi · ölçek eşlemesi. ⚪ henüz yazılmadı.

## 14 · Uygulama durumu

| paket | bugün | açık |
|---|---|---|
| `cekirdek` · `yapilandirma` · `dunya` · `kanal` · `mac` | 🟢 yedi kova · dört mobilite kolu · beş sınıf + beş aile · veri onayı yalnız gönderenin çözdüğünde (Y2) | — |
| `ag` | 🟢 eşler arası · yere toplama · kaynak başına paket sırası (K-157) | varsayılan desen (§17 A8) |
| `gozlem` | 🟢 pencere + kontrol niyetleri · `iletim_basarisiz` · `iletim_sonucu` · veri başlığı · `(kaynak, kaynak_sira)` · `cerceve_duyuldu` + RSSI (K-172) | B3 alanları (`v2/15`) |
| `olcum` | 🟢 evre metrikleri · kopma · PSR · Θ protokol başına | 🔵 bağ başına PSR |
| `kosum` | 🟢 kontrol düzlemi · bekleme tamponu · beacon kapatma · rastgelelik alt akışı · `kosu_kimligi` tedavi + protokol parmak izi · PDR telemetri/komut · düşme sebebi `politika` (K-171) | — |
| `protokoller` | 🟢 AODV-e · OLSR-b · AOMDV-a eski dünyada kapalı; referans dünyada U1-B kalıyor, donmadı (K-191, K-192) · DESPARETE v0.4.1 (K-172) | OLSR teşhisi, donma öncesi eksikler · DESPARETE referans dünyada Faz 5 |
| `analiz` | 🟢 Wilcoxon · Holm · δ · güç · hücre koşucusu (K-184, K-189) | ana deney tablosu |
| dünyalar | 🟢 `olcek_1_50` (varsayılan, eski) · `referans_2026` (bütün gerçekçilik anahtarları açık, K-181) | — |

---

## 15 · Öğrenci kararları — tek liste

Ayrıntı ve gerekçe `04`teki kayıtta. Tırnak içi sözler öğrencinindir.

**8 Eylül.** Kapsam cümlesi (`01` §3) · yere toplama birincil, eşler arası keşifsel · mobilite yapısı ile çalkantı ayrı eksenler, çekirdekte düzgün istasyon (Θ ≈ 10 ulaşılamaz bulundu → Θ kapıya çevrildi, K-101 · K-110) · Li replikasyonu yapılacak.

**9 Eylül.** Beacon yükü çerçeveyi uzatır · simülatör fazında kalınır (K-111) · *"simülasyonu geliştirmek için gerekenleri yap sana bırakıyorum"* (K-110).

**10 Eylül (K-112 · K-113).** Kontrol düzleminin beş kararı (`13` §01) · yüksek çalkantı kolu saklanmaz, sorun varsa düzeltilir · ana deney 40 tohum · mobilitede ajan tercihini belirtir · görev yarıçapı daha büyük örneklemle ölçülür · düğüm sayısı 30–50, ajan ölçerek bulur · veri onayı kusuru önce ölçülür · yere toplama kabul · karıştırıcılar çoklu ve hareketli, saha davranışına paralel · sabit mühür tarihi yok · iş akışı beş aşama (`01` §5) · birincil karıştırıcı konumu çoklu tasarımla · PSR tanımı (§08) · tespit gecikmesinin boş kol kapısı protokol aşamasına · Rician K'nin kaynağı doğrulanacak · iki anlamlılık sabiti ajan ölçerek seçer · ısınma ve ölçüm penceresi birlikte taranır, açılma anı parametre kalır · kâhin tazeleme üst sınırı (10 s) kabul · üst referans isteniyor · kontrol istatistiklerini ajan önerir · yedi kova esas · belgeler bilgi kaynağına çevrilir, aşırı katı kurallar gevşer.

**10 Eylül, ikinci tur (K-114).** Mobilite: çekirdekte formasyon + istasyon tutma · yere toplama önerileri — *"projede dürüstlük ve gerçekçiliğe sıkıntı çıkarmayacaksa"* · çoklu hareketli karıştırıcı modeli (saha sentezi öğrenciden, `02` §S3) · üst referans (teslim olasılığı kâhini + zarf) · kontrol istatistikleri önerisi · mühür sırası gevşetildi.

**11 Eylül, üçüncü tur (K-114).** Veri onayı yalnız gönderenin kendisi çözdüyse sayılır (Y2) · üst referans yeni çekirdek hücrede C7 ile ölçülür · yapı planı Y1, Y3–Y7, Y10 onaylandı.

**11 Eylül, dördüncü tur (K-119).** Tehdit aileleri ve üye sayıları öneri olduğu gibi (toplam ortalama güç eşit) · süre eksenleri açık 15 · sessiz 15 · (hedef koruma çevrimi sonra kaldırıldı, K-127) · ~2 000 s'lik uzun koşu şimdilik yok, çekirdek 350 s · formasyonda duvar teması nadir kabul, sayılır, beyan edilir · derin sızma aracı yalnız susarken taşınır · yerleşim kuralları kabul.

**15 Eylül (K-124 · K-129).** C1 ve C3 ölçütleri tarama ÖNCESİ ilan edildi (C1: adaylar 30–50, yoğunluk sabit, statik kopukluk yok, geçide düğüm-ayrık ikinci yol ≥ 0,90, amaç en küçük ölçülmüş maliyet · C3: karıştırıcısız kolda kâhinle teslimin ≥ 0,95 tuttuğu en büyük telemetri hızı) · C1 → N = 40, C3 → 1,0 pkt/s (K-125 · K-126) · `hedef_koruma` çevrimi kaldırıldı (K-127) · doğrulama listesi koşsun — *"şimdi koşsun, temiz girelim"*.

**16 Eylül (K-130 · K-131 · K-132 · K-133 · K-134).** Bağımsız denetimin bulguları işlensin (`arsiv/DENETIM-2026-09-16.md`) · ayrı bekleme tamponu · pencere ikizi pencerede dondurulur · kancalara gözlem, `bildirdigi_konum` yüzeyden çıkar, bilgi yoksa `None` · Θ yeniden ölçümü (C4) şimdi değil · ağ bölünmesi: *"gerekeni yap, beyan ederek hiçbir şey çözülmez"* · aklamalar 20 tohumla yeniden ölçülsün · doğrulama listesi tamamı — *"evet, tamamını koş"* · kancalar beyan döndürsün, `rota_gecersiz` yolu uygulansın.

**17 Eylül (K-136 · K-137).** U1 eşiği: protokol PDR / aynı konfigte ETX kâhini, **statik ≥ 0,90 · hareketli ≥ 0,60** (ölçüm görüldükten SONRA seçildi, `06` §4.3'te beyanlı) · AODV yerel onarımı (§6.12) uygulanmaz, beyan edilir · U1 için A: eşik yerinde, eşik altı hücre açıklamasıyla bulgu; U1-U kapı · U1-B bulgu · çalışma ritmi: *bir iş bitirilir, sonra ölçülür*.

**18 Eylül (K-138).** *"Sen en mantıklı bulduğun şeyi yap"* — hız araştırması ajana; Philox alınmadı.

**19 Eylül (K-140…K-145).** AODV kapatılsın (K-143 geçersiz kıldı, yeniden K-145) · COR düzeltmesi kapanıştan sonra · OLSR: SHOULD uygulanır, MAY beyan edilir · *"ilk önce aodv bitsin sonradan olsryi koşacağız"* · AODV'nin U3'ü bulgu · birincil kaynaklar depoya ancak tamamı okunup denetlendikten sonra girer · AOMDV boşlukları için ns-2 çapraz kontrolü kabul (ns-2 kodu yazarlara ait değil çıktı).

**21 Eylül.** Ağır koşumlar 8 çekirdek — *"işlemcimin 8 çekirdeğini kullanabilirsin"* · OLSR kapanış ölçümü — *"devam edebiliriz"*.

**22 Eylül (K-146 · K-147 · K-150).** OLSR'da RFC 3626 §13 uygulanır (MAY kuralına ölçülmüş gerekçeli tek istisna; hareketli kollardaki bedeli bulgu) — ⚠️ K-196'da (28 Eylül) kaldırıldı, referans dünyada zarar veriyordu · AOMDV: makale + RFC 3561 · DESPARETE ana karşılaştırmada güvenliksiz, Güvenlik Profili 1'in bedeli ayrı kolda · yedekli gönderim ilk gerçeklemede yok · `sim2/` Y1 · Y2 onaylı (K-151) · hedef alanı simülasyonda emekliye ayrılmaz · CAUTION girişinde bir sınırlı doğrulama · ~~komutlar için isteğe bağlı hedef alanı (A)~~ → C (24 Eylül).

**23 Eylül (K-152 · K-153 · K-157).** Temizlik: silme yok, arşive taşıma · kök `README.md` GitHub okuru için · depo herkese açık değil · K-151 kapanış paketi · DESPARETE taslaktır — *"geliştirmek, eklemek veya düzeltmek istediğin bir yer varsa çekinme"* · TV-02 — *"ölçerek sen bul"* · UNREACHABLE'dan çıkış ajana — *"mantıklı olanı yapalım"* · tampon kotası ajan önerisi, ölçülür · DFSN_REQUEST diyagramdaki gibi (76 B) · ön-kaydın adım 3'ü ilk entegrasyon koşusundan önce · aday birincil hücre *"önerdiğin gibi olsun"*: formasyon · yere toplama · hava eşlik · sürekli, PDR, Δ_hedef = 0,05 · paket kimliği gözleme — *"a ile devam edebilirsin"* (kaynak başına sıra).

**24 Eylül (K-160…K-165).** Komut trafiği **C** — *"komutları taşımasın"*: DESPARETE yalnız geçit alanı; geçit dışı veri politika hatasıyla düşer; trafik herkes için aynı, komut kaybı DESPARETE'nin aleyhine sayılır · **v0.2'ye geç** · v0.2 = yalın profil — *"Yalın profil (V0)"* · resmi U1 — *"Daha sonra"* · test öncesi iyileştirme — *"şuanlık o protokolü test etmektense protokolü ilk önce mükemmelleştirmeye çalışalım"* · *"V5 + V1 ile başla"* (V7'yi ajan ekledi) · v0.3 = v0.2 + V1 + V5 + V7 — *"Üçlüyü benimse + V5a, sonra V2+"*; V5a ve V2+ ajanın önerisiyle kapalı, öğrenci ayrıca karar vermedi (*"şuanlık duralım"*). V7 ajanın mekanizması; V1 ve V5 ajanın önerisi, seçim öğrencinin.

**25 Eylül (K-166 · K-167).** Bağımsız denetim (rapor `arsiv/denetim/DENETIM-RAPORU-2026-09-25.md`) · *"başlayabilirsin düzeltmeler bitince sıradaki işi vericem"* · U1 tüm koşu PDR'siyle — *"u1 tüm koşuda kalabilir"* (ana deney pencere PDR'siyle) · kâhin kuralı — *"eğer kahini geçebiliyorsak ya yazılımsa bir sıkıntı vardır yada gerçekten tam manasıyla üst sınır değildir"* (ajanın okuması: aşım otomatik ret değil, inceleme; teyit bekliyor) · taban protokoller yere toplamada da sınanır — *"senin önerini yapalım"* · `kosu_kimligi` düzeltilir — *"simülatör konusunda da onayını veriyorum"* · DESPARETE'nin sorunlarını ajan çözer — *"bu protokolün şuanda yapılan versiyonunu kesin saymak yerine sorunları çözmeyi ve protokolü neden geliştirmeye çalışmıyorsun"* → **DESPARETE v0.4 = v0.3 + V8 + V10 varsayılan** (ajan, bu devirle; öğrenci geri alabilir) · belgeler öz ve kayıpsız, tam metin arşivde; testler ve ölçümler kısa ve gerekli olanla sınırlı — *"yapılan testler ve ölçümler hem çok uzun hem de çoğu zaman gereksiz oluyor"*. **Açık:** birincil metrikte komutlar.

---

## 16 · Statü

Bilgi belgesidir. Kodla çelişirse hangi tarafın yanlış olduğu ölçülerek bulunur ve §17'ye yazılır. `sim2` değişiklikleri yapı onayı ister.

## 17 · Şartname–kod ayrışma defteri — açık satırlar

| # | belge | kod | durum |
|---|---|---|---|
| A6 | menzil yalnız verici gücünün çapası | alanın adı hâlâ "iletim menzili" | ⚪ ad yanlış bir iddia taşıyor |
| A8 | yere toplama birincil | `Konfig` varsayılanı `esler_arasi` | 🟡 ana deney aleti deseni açık vermeli; satırın `konfig.trafik_deseni` analizde denetlenmeli |
| A23 | kapsam dışı listesi (§12) güncel | kodun kapsam listesi eski olabilir | ⚪ kontrol edilecek |

Kapanmış satırlar (A4, A14, A19–A22, A24–A27): arşiv sürümü §17.

## 18 · Yapı planı ve `sim2/` değişiklik kuralları

Aşama 1 yapı planı (Y0–Y10) uygulandı (K-114…K-123); açık yalnız **Y8 iz kanalı** (Aşama 5). Ayrıntı: arşiv sürümü §18. Kodda atıflı adımlar: Y0 regresyon aleti (K-114) · Y1 PSR ve kontrol istatistikleri (K-115) · Y2 veri onayı semantiği (K-115) · Y3 kontrol düzlemi eksikleri, `13` R2–R4 (K-121) · Y4 yere toplama (K-116) · Y5a çoklu hareketli karıştırıcı (K-117) · Y5b tehdit aileleri (K-120) · Y6 formasyon ve istasyon tutma (K-118) · Y7 Θ protokol başına (K-122) · Y8 iz kanalı (açık) · Y9 teslim olasılığı kâhini (K-114) · Y10 tek anlamlılık sabiti (K-123). Her `sim2/` değişikliğinde:

| kural | nasıl |
|---|---|
| varsayılan = bugünkü davranış | yeni alanın varsayılanı bugünkü kolu birebir üretir; regresyon (`kalibrasyon/regresyon_satirlari.py`) ve test takımı koşulur; değişmesine izin verilen alanlar önceden yazılır |
| yeni parametre | köken defterine kovasıyla |
| yeni rastgelelik | önce hash alanı; sıralı akış yalnız gerekiyorsa |
| yeni sayaç | sayaç kütüğünde; pencere ikizi otomatik |
| her mekanizmanın kapısı | boş geçmeyen test: mekanizma devredeyken kanıt > 0 |
