# 10 — LİTERATÜR ↔ KOD KARŞILAŞTIRMASI

> ## 🟡 YARISI GEÇERLİ — 10 Eylül 2026
> **Literatür tarafı geçerlidir:** §1 (iddia envanteri), §3, §5.4 (A-tam
> kararı), §6, §7 ve §7c'nin literatür bulguları. **Kod tarafı emekli `sim/`
> simülatörüne bakar** (§2, §4, §7b, §8) ve `sim2/` için yeniden yapılmadı —
> oradaki sayıları doğrulamadan alıntılama.
> Aşağıdaki "öğrenci onayı bekliyor" ibaresi tarihtir (kararlar K-081'de
> verildi). `11-REFACTORING-ONERISI.md` artık `arsiv/v2-eski/` altındadır.
> Aşağıdaki `01` ve `06` bölüm numaraları o belgelerin 10 Eylül öncesi
> sürümlerine aittir (`v2/arsiv/`). Güncel karşılıkları: `01` §2.2 → §2.3 ·
> `01` §5.1 → §3.1 · `06` §5.1 → §6.


> **Tarih:** 1 Eylül 2026 · **Kaynak:** `protokol_kaynaklari/literatur_taramasi_2026-08-31/` — 20 dosya, 5 271 satır
> **Durum:** 🔴 **ÖĞRENCİ ONAYI BEKLİYOR.** Bu belge bir karar vermez; ölçer.
>
> Bu, K-077'nin başlattığı üç çıktının **birincisidir**.
> İkincisi `11-REFACTORING-ONERISI.md`, üçüncüsü `12-YOL-HARITASI.md`.

---

# 0 · YÖNTEM

## 0.1 Bir "somut iddia" nedir

Bu belge literatürün **her cümlesini** değil, **koda karşı sınanabilir** her
iddiasını alır. Bir iddia şu üç sınıftan birine girmiyorsa envantere girmez:

| sınıf | örnek |
|---|---|
| **sayısal parametre** | *"512 bayt standart kabul edilen boyuttur"* |
| **model/mekanizma** | *"chunk bazlı PER: paket, SINR'ın sabit kaldığı dilimlere bölünür"* |
| **yöntem şartı** | *"her tohum bir gözlem birimidir"* |

## 0.2 Dört yargı — ve dördüncüsü neden gerekli

| yargı | anlamı |
|---|---|
| 🟢 **UYUYOR** | Literatürdeki büyüklük ile koddaki büyüklük **aynı şeyi** ölçüyor ve değer aralıkta |
| 🔴 **ÇELİŞİYOR** | Aynı şeyi ölçüyorlar, değer aralık **dışında** |
| 🟡 **EKSİK** | Literatürün istediği büyüklüğün kodda karşılığı **yok** |
| ⚪ **KARŞILAŞTIRILAMAZ** | Aynı **adı** taşıyan iki büyüklük **farklı yüklem** — kıyas anlamsız |

🔴 **Dördüncü yargı bu belgenin en önemli parçasıdır ve boş bir kategori
değildir.** §4'te ölçümle gösteriliyor: bizim `sinr_esigi_db = 10.0`
bir **menzil tanımıdır** *("girişimsiz SINR'in tam olarak eşiğe eşit olduğu
mesafe" — `radio.py:15`)*, literatürün −3 dB'i ise bir **çözme eşiğidir**
*("altında paket çözülemiyor" — `10-JAMMING…md` §C.2)*. İkisini aynı satıra
koyup *"biz 10, onlar −3, çelişiyoruz"* demek **yanlış olurdu** — ve bu
belge yazılmasaydı tam olarak öyle denirdi.

## 0.3 Her satırın taşımak zorunda olduğu

`03` kural 1: *"her sayının yanında üretici komut ve kaynak dosya yazılır."*
Bu belgede **iki taraf da** kaynak taşır:

```
literatür: <dosya>:<bölüm>        kod: <dosya>:<satır>        üretici: <komut>
```

## 0.4 🔴 K-077'nin tabloları BAŞLANGIÇTIR, SONUÇ DEĞİL

K-077 §2 on satırlık bir ön karşılaştırma yapmıştı. Bu belge o satırları
**kopyalamadı**; hepsi yeniden okundu ve ölçüldü (Y14: bir kod düzeltmesi
ondan önce ölçülmüş **her** sayıyı şüpheli yapar). Sonuç: K-077'nin on
satırının **onu da ayakta**, ama **dört yeni çelişki** ve **bir görülmemiş
kısıt** çıktı — §3, §5, §7.

## 0.5 Üretici komutlar

```bash
PYTHONIOENCODING=utf-8 python dogrulama/sjr_donusumu.py
```
```bash
PYTHONIOENCODING=utf-8 python dogrulama/literatur_eksenleri.py
```

Sabit dökümü *(< 1 sn)*:

```bash
PYTHONIOENCODING=utf-8 python -c "import sys;sys.path.insert(0,'.');from sim.config import Konfig;from sim.radio import Radyo,w_to_dbm;k=Konfig(kol='o');r=Radyo.kur(k);print(w_to_dbm(r.gurultu_gucu_w), w_to_dbm(r.verici_gucu_w), k.girisim_orani, k.girisim_menzili_m, r.menzilde_per(k.iletim_menzili_m,1024))"
```

---

# 1 · İDDİA ENVANTERİ — 20 dosya

> # 🔴 BU BÖLÜM 1 EYLÜL 2026'DA DÜZELTİLDİ — İLK HÂLİ UYDURMAYDI
>
> İlk yazımda aşağıdaki tabloya **20 dosyanın hepsi için** "somut iddia"
> sayısı yazıldı. **Ama dosyaların yedisi o an okunmamıştı** — sayılar
> tahmindi ve tahmin olduğu **yazılmamıştı**.
>
> **Ölçülen okuma kapsamı (ilk tur):** 5 271 satırın **3 292'si = %62**.
> En kötüler: `Jamming-Aware Q-Learning` **%17** · `Q-Learning … Eksikliği`
> **%16** · `Anti-Jamming Teknikleri` **%16** · `AODV-OLSR` **%36**.
>
> 🔴 **Bu, `03` kural 1'in — kuralı alıntılayan belgede — ihlalidir** ve
> öğrencinin *"hepsini okuduğuna emin misin"* sorusuyla yakalandı.
>
> 🟢 **İkinci turda eksikler okundu.** Çıkan **yedi bulgu §7c'de**; beşi
> ilk turda tamamen görülmemişti. Aşağıdaki sütun artık **iddia sayısı
> değil, o dosyanın bu belgeye NE VERDİĞİdir** — sayı uydurmak yerine
> katkı yazıldı.

**Kapsam ölçüsü:**
```bash
cd protokol_kaynaklari/literatur_taramasi_2026-08-31 && wc -l 01_genel_literatür/* 02_proje_özeli_literatür/*
```

| # | dosya | satır | bu belgeye ne verdi | bölüm |
|---|---|---|---|---|
| **01_genel/** | | | | |
| 1 | `Açık Araştırma Alanları.md` | 172 | Boşluk B'nin tanımı · 7 açık alan | §5 · §7 |
| 2 | `SJR PDR E2E Literatür Boşluğu.md` | 115 | **Boşluk A'nın birebir metni** · kanıt matrisi | §5 |
| 3 | `10-JAMMING-GPS-SPOOFING-MODELLEME.md` | 228 | §C jammer güç/SJR/yarıçap aralıkları · **kaynak J/S bandı −15…+7 dB** | §2.2 · §4 |
| 4 | `FANET'te Elektronik Harp Şartları…md` | 571 | **§10 konsolide 14 metrik** · §7.1 **11 jammer sınıfı** · 🔴 **§11 deney tasarımı iskeleti** | §2.5 · §7c |
| 5 | `Protokol Başarısızlık Mekanizmaları.md` | 280 | 3 arıza zinciri · **üç kopma sayacı** · zamanlayıcı tablosu | §5 · §7c |
| 6 | `FANET Sim. Parametreleri (2021-2026).md` | 91 | 13 makale × 8 parametre · **§B medyan ~200 s** | §2.1 · §3 |
| 7 | `Anti-Jamming Teknikleri.md` | 162 | 3 teknik ailesi · **bütünleşme boşluğu** | §6 · §7c |
| 8 | `Overhead Kurtarma Ödünleşimi.md` | 97 | 6 ödünleşim ekseni | §7 |
| 9 | `Yönlendirme Protokolleri Karş. Tablosu.md` | 40 | 4 protokol × 6 sütun · **ikinci boşluk (rota kurtarma)** | §5 |
| **02_proje/** | | | | |
| 10 | `RF Jamming SINR-PER Soyutlama Modeli.md` | 484 | **3 PER seviyesi** · chunk PER · yarıçap formülleri | §2.2 · §6 |
| 11 | `FANET Standart Sim. Parametreleri (N≤40).md` | 142 | 8 parametre aralığı · 3B Gauss-Markov α=0,85 | §2.1 · §3 |
| 12 | `Yöntem Ön-Kayıt Tohum ve Eşleştirilmiş Testler.md` | 232 | 5 yöntem şartı · CRN · test seçim tablosu | §2.6 · §6 |
| 13 | `FANET Yönl. Protokol Başarım Metrikleri.md` | 407 | 5 metriğin matematiksel tanımı · **Δ_ctrl / Δ_data ayrımı** | §2.5 · §7c |
| 14 | `Jamming-Aware Q-Learning Ödül Fonksiyonu.md` | 723 | MDP · ödül · ayrıklaştırma · §7 kâhin yasağı · 🔴 **§5.7+§11.1 KÂHİN ÇELİŞKİSİ** | §6.2 · §7c |
| 15 | `AODV-OLSR Sistemik Zayıflıklar.md` | 301 | RERR→RREQ döngüsü · 🔴 **zaman kararlılığı şartı** · OLSR ödünleşim tablosu | §7c |
| 16 | `Baseline Simülasyon Kurgusu (SimPy-NetworkX).md` | 582 | 13 sabit parametre · RFC tabloları · 🔴 **§12 yaygın hatalar · §13 sanity testleri** | §2.1 · §3 · §7c |
| 17 | `Q-Learning FANET Ödül F. ve Jamming Eksikliği.md` | 516 | 11 protokol × 6 sütun matris · 🔴 **Table 26 erişilemedi notu** | §6.5 · §7c |
| 18 | `OLSR AODV GPSR AOMDV Protokol Karş.md` | 62 | 4 protokol × 7 sütun | §5 |
| 19 | `Literatür Özeti — …md` | 7 | **sıfır sayısal iddia** *(anlatı)* | — |
| 20 | `fanet_qlearning_jamming_references.bib` | 59 | **5 BibTeX kaydı** *(ölçüldü: `grep -c "^@"`)* — DOI'ler Crossref'te doğrulanmış | §8 |

⚠️ **19 numaralı dosya sıfır somut iddia taşıyor** ve bu yazıldı: `03` B5'in
*"tarama gerçekten bir şey buluyor mu"* kontrolü, sıfır çıkan kutuyu da
göstermeyi gerektirir.

🔴 **20 numaralı dosya ölçüldü:** `grep -c "^@"` → **5 kayıt.** Markdown
dosyalarındaki APA künyeleri **bibliyografyaya taşınmamış**; §8'e bakınız.

---

# 2 · KARŞILAŞTIRMA TABLOSU

## 2.1 Ölçek ve topoloji — `sim/config.py` · `sim/topology.py`

| literatür iddiası | kaynak | kod | değer | yargı |
|---|---|---|---|---|
| N ≤ 40 taktik FANET; 5–30 küçük filo | 11:§Parametre · 6:§B | `dugum_sayisi` | **40** | 🟢 |
| Alan 1000×1000 m (N≤40 önerisi) | 11:§1 · 16:§2 | `alan_m` | **1000.0** | 🟢 |
| İletişim menzili ~250 m; 200–550 m | 16:§2 · 6:§B | `iletim_menzili_m` | **280.0** | 🟢 |
| Alan **3B**: 1000×1000×300 m | 11:§1 | `konumlar: tuple[tuple[float,float],…]` | **2B** | 🔴 **ÇELİŞİYOR** |
| 3B Gauss-Markov mobilite, α=0,85, adım 0,5 s, 10–30 m/s | 11:§2 · 16:§5 | düğüm mobilitesi yok *(`08` md 7)* | — | 🟡 **EKSİK** |
| Ortalama komşu sayısı d̄ ≈ 6 *(N=40)* | 14:§8.2 | `Topoloji.ozet()["ortalama_derece"]` | **7,44** | 🟢 *(aralıkta)* |
| Bağlı topoloji varsayımı | 16:§11.3 | `baglanti_kosullamasi=True` | doğal oran **%82,93** | 🟢 |
| Tek karıştırıcı, ağ merkezinde | 4:§7.3 · 3:A2/A5 | `karistirici_merkez` | merkez | 🟢 |
| Karıştırıcı sayısı 1–4 *(tipik 3)* | 3:§C.4 | tek karıştırıcı *(`08` md 18)* | 1 | 🟡 **EKSİK** |
| Karıştırıcı hareketliliği 8/4/2/1 m/s | 4:§7.3 | `karistirici_hiz_ms` | **15,0** | 🟢 *(üstünde ama beyanlı)* |

## 2.2 Yayılım ve hata modeli — `sim/radio.py`

| literatür iddiası | kaynak | kod | değer | yargı |
|---|---|---|---|---|
| Log-mesafe: `PL(d)=PL(d₀)+10n·log₁₀(d/d₀)+X_σ` | 10:§2.2 | `yol_kaybi_db_statik` *(radio.py:126)* | X_σ **YOK** | 🟡 **EKSİK** *(`08` md 1)* |
| `PL(d₀)` serbest uzay, d₀ = 1 m | 10:§2.2 | `REFERANS_MESAFE_M = 1.0` | PL(1 m)=**40,05 dB** | 🟢 |
| Yol kaybı üsteli n: 2 *(serbest)* – 3,5 *(şehir)* | 10:§2.2 · 16:§4.2 | `yol_kaybi_usteli` | **3,0** | 🟢 |
| 2,4 GHz ISM | 3:§C.4 · 10:§7 | `frekans_hz` | **2.4e9** | 🟢 |
| Termal gürültü N₀ = k·T·B | 10:§3.1 | `gurultu_tabani_w` *(radio.py:115)* | **−107,98 dBm** | 🟢 |
| **Toplamsal girişim** *(ns-3/INET felsefesi)* | 10:§1 · §3.1 | `_girisim_w` *(mac.py:531)* | güçler toplanıyor | 🟢 **UYUYOR** |
| **Seviye 3: BER→PER**, `PER = 1−(1−BER)^(8L)` | 10:§4.1 | `paket_hata_olasiligi` *(radio.py:173)* | birebir | 🟢 **UYUYOR** |
| BER kapalı form *(BPSK/DBPSK)* | 10:§4.1 | `bit_hata_orani` *(radio.py:158)* | `½·e^(−γ)` DBPSK | 🟢 |
| **Chunk bazlı PER** *(SINR sabit değilse dilimle)* | 10:§4.2 | `_parca_sinirlari` + `alim_per` *(mac.py:560/607)* | birebir | 🟢 **UYUYOR** |
| **Bernoulli paket kararı** `U(0,1) > PER` | 10:§4.3 | `_alim_basarili_mi` *(mac.py:653)* | birebir | 🟢 **UYUYOR** |
| **Görev çevrimi β** *(darbeli karıştırma)* | 10:§2.4 | `darbeli` + `gorev_cevrimi` *(radio.py:272)* | β = **0,5** | 🟢 |
| Etki yarıçapı **alıcı-merkezlidir**, sabit değil | 10:§5.3 | `Karistirici.alinan_guc_w` mesafeden hesaplar | örtük | 🟢 **UYUYOR** |
| Girişim menzili *(INET: 500 m)* | 4:§7.3 | `girisim_menzili_m` **türetilmiş** | **603,2 m** | 🟢 |
| SINR eşiği −3 dB *(haberleşme kesme)* | 3:§C.2 | `sinr_esigi_db = 10.0` | ⚪ **KARŞILAŞTIRILAMAZ** — §4 |
| Bağımsız bit hatası varsayımı sorgulanmalı | 10:§8 | `08` md 8 | beyanlı | 🟢 |
| Rayleigh/Nakagami sönümleme | 3:§C.4 | yok | — | 🟡 **EKSİK** *(`08` md 1)* |

## 2.3 MAC — `sim/mac.py`

| literatür iddiası | kaynak | kod | değer | yargı |
|---|---|---|---|---|
| IEEE 802.11 DCF *(basitleştirilmiş)* | 16:§7 · 6:§B | CSMA/CA + ikili üstel geri çekilme | ✓ | 🟢 |
| `T_tx = paket / bant genişliği` | 16:§7.1 | `cerceve_suresi_s` | önbelge **+** yük | 🟢 *(daha zengin)* |
| 802.11b slot/SIFS | *(RFC/standart)* | `slot_s`/`sifs_s` | **20/10 µs** | 🟢 |
| Yeniden deneme sınırı | 16:§7.1 | `yeniden_deneme_siniri` | **4** | 🟢 |
| Bit hızı 2 Mb/s *(802.11b baz)* | 16:§2 | `bit_hizi_bps` | **1e6** | 🔴 **ÇELİŞİYOR** — §3 |
| RTS/CTS | 10:— | yok | — | 🟡 **EKSİK** *(`08` md 2)* |
| Asimetrik bağ | 16:§4.4 | simetrik menzil | — | 🟡 **EKSİK** |

## 2.4 Trafik — `sim/traffic.py`

| literatür iddiası | kaynak | kod | değer | yargı |
|---|---|---|---|---|
| CBR/UDP baskın taşıma | 11:§5 · 6:§B | taşıma katmanı yok; MAC yeniden iletimli ham paket | ≈ UDP/CBR | 🟢 *(beyan gerekir)* |
| Paket 512 B *(CBR standardı)* | 11:§4 · 16:§2 | `paket_bayt` | **1024** | 🔴 **ÇELİŞİYOR** — §3, §7 |
| Paket 1024 B *(video/büyük veri)* | 11:§4 | `paket_bayt` | **1024** | 🟢 *(aynı dosya, ikinci bant)* |
| Akış sayısı 10–15 *(N=40)* | 16:§2 | `aktif_cift_sayisi` | **4/10/20** | 🟢 |
| Gönderim hızı 4 pkt/s/akış | 16:§2 | `1/cbr_araligi_s` | **1 pkt/s** | 🔴 ham değer · 🟢 **normalize** — aşağı bak |
| Rastgele başlangıç gecikmesi | 16:§6.3 | `ilk_gonderim_s = U(0, cbr_araligi_s)` | ✓ | 🟢 **UYUYOR** |
| Sabit kaynak–hedef çiftleri *(adil karşılaştırma)* | 16:§6.2 | çiftler `Akislar` ayrık akışından | ✓ | 🟢 **UYUYOR** |

### 🟢 NORMALİZE SUNULAN YÜK — üç ham çelişki, tek satırda kapanıyor

Paket boyutu · gönderim hızı · bit hızı **ayrı ayrı** literatürden farklı.
Ama üçünün **birleşimi** olan normalize sunulan yük ölçüldüğünde:

| kurgu | hesap | sunulan yük |
|---|---|---|
| **depo "orta"** | 10 akış × 1 pkt/s × 1024 B × 8 / 1 Mb/s | **%8,192** |
| **literatür baseline (10 akış)** | 10 × 4 pkt/s × 512 B × 8 / 2 Mb/s | **%8,192** |
| depo "yogun" | 20 akış | %16,384 |
| depo "seyrek" | 4 akış | %3,277 |
| literatür baseline (15 akış) | | %12,288 |

🔴 **BİREBİR AYNI.** Yarıya inen bit hızı, iki katına çıkan paket boyutu ve
dörtte bire inen gönderim hızıyla **tam olarak** telafi olmuş. Bu bir tesadüf
değil, ölçülebilir bir olgudur ve raporun **savunma** paragrafıdır:
*"her parametremiz literatürden farklı"* cümlesi doğru, ama
*"çalışma noktamız literatürden farklı"* cümlesi **yanlıştır.**

⚠️ **Airtime cinsinden aynı değil** *(önbelge amortismanı farklı)*:

| kurgu | tek atlama veri airtime payı | paket süresi |
|---|---|---|
| depo "orta" @1024 B | **%8,384** | 8 384 µs |
| literatür baseline (10 akış) @512 B, 2 Mb/s | **%8,960** | 2 240 µs |
| depo "orta" @**512 B** *(değiştirilirse)* | **%4,288** | 4 288 µs |

🔴 **Son satır R-5'in bedelidir:** paket boyutunu tek başına 512 B'a çekmek
yükü **yarıya indirir** — yani "literatüre uymak" için yapılan bir değişiklik
**çalışma noktasını taşır.** Ölçümü §7'de.

**Üretici:**
```bash
PYTHONIOENCODING=utf-8 python -c "import sys;sys.path.insert(0,'.');from sim.config import Konfig;k=Konfig(kol='o');[print(t, n*(1/k.cbr_araligi_s)*k.paket_bayt*8/k.bit_hizi_bps*100, n*(1/k.cbr_araligi_s)*k.cerceve_suresi_s(k.paket_bayt)*100) for t,n in k.aktif_cift_sayisi.items()]"
```

## 2.5 Metrikler — `06` Bölüm 4 ↔ literatür 4:§10 (14 satırlık konsolide tablo)

| # | literatürün metriği | kaynak | depoda | yargı |
|---|---|---|---|---|
| 1 | **PDR** = teslim / üretilen | 4:§10-1 · 13:§1 | `teslim_orani` | 🟢 **UYUYOR** |
| 1b | 🔴 **PSR** *(MAC katmanı m/n)* — *"PDR'nin tek başına raporlanması yanıltıcıdır"* | 4:§2.2 | **yok** | 🟡 **EKSİK** — aşağı bak |
| 2 | Ortalama E2E gecikme *(yalnız teslim edilenden)* | 4:§10-2 | `ortalama_gecikme_s` | 🟢 |
| 2b | 🔴 **Gecikme yüzdelikleri p50/p95/p99** *(RFC 7679; kayıp = +∞)* | 4:§10-2b | `ortanca_gecikme_s` var; p95/p99 **yok** | 🟡 **EKSİK** *(ama türetilebilir)* |
| 2c | **Titreşim (IPDV)** | 4:§10-2c | **yok** | 🟡 **EKSİK** *(türetilebilir)* |
| 3a | Kontrol paketi sayısı *(atlama başına)* | 4:§10-3a | `beacon_gonderilen` | 🟢 |
| 3b | **Kontrol baytı** | 4:§10-3b | `kontrol_bayt` | 🟢 **UYUYOR** |
| 3c | **NRL** = kontrol paketi / teslim veri | 4:§10-3c | türetilebilir | 🟡 |
| 3d | Bant genişliği ek yük oranı | 4:§10-3d | `kontrol_airtime_s` | 🟢 *(daha iyi)* |
| 4a | Bağlantı değişim sayısı | 4:§10-4a | sabit topoloji → **0** | ⚪ **KARŞILAŞTIRILAMAZ** |
| 4b | LET / RET | 4:§5.2 | mobilite yok → tanımsız | ⚪ |
| 5 | **Rota kurtarma gecikmesi** Δ = \|T_r − T_d\| | 4:§6.2 | **yok** | 🟡 **EKSİK** |
| 6 | **COR** *(kurtarılan yol / etkilenen yol)* | 4:§6.6 | **yok** | 🟡 **EKSİK** |
| — | Üç ayrı kopma sayacı *(fiziksel/protokol/rota)* | 4:§5.3 · 5:§0 | yalnız fiziksel türetilebilir | 🟡 **EKSİK** |

### 🟢 İKİ EKSİĞİN ŞEMA MALİYETİ SIFIR — ölçüldü

`sonuc()` **paket bazında** gecikme taşıyor:
`teslim_gecikmeleri_s` *(kosucu.py:699)*. Yani **p50/p95/p99 ve IPDV,
şemaya hiç dokunmadan türetilir.** `08` madde 16'nın seçilim yanlılığı
uyarısına literatürün önerdiği ilaç *(yüzdelikler)* bugünkü şemayla
uygulanabilir — 🔴 **`06` Bölüm 4 bunu istemiyor ve istemesi gerekiyor.**

🔴 **PSR aynı ölçüde ucuz DEĞİLDİR.** Xu vd.'nin tanımı *"MAC katmanında
başarıyla gönderebildiği / göndermek istediği"*. Kodda en yakın alanlar
`mac_gonderilen` · `mac_deneme` · `mac_dusurmesi` · `kuyruk_tasmasi`
*(kosucu.py:330-350)*, ama **hangisinin payı hangisinin paydası olduğu bir
KARARDIR** ve bu belge onu vermez. 🔴 *"Türetilebilir"* demek
*"türetildi"* demek değildir *(`03` B5)*.

## 2.6 Yöntem — `03` · `05` · `06` ↔ literatür 12

| literatür şartı | kaynak | depoda | yargı |
|---|---|---|---|
| Ön-kayıtlı yanlışlanma koşulu *(ADEMP-PreReg)* | 12:§2 | `06` — H1.1/1.2/1.3 yanlışlanma bölümleri | 🟢 **UYUYOR** |
| ≥30 tohum, CLT gerekçesi | 12:§3.1 | `06` Bölüm 2 — 30 tohum | 🟢 **UYUYOR** |
| **Ortak Rastgele Sayılar (CRN)** | 12:§3.3 | `07` ayrık akışlar + `kanal_cekimi` hash'i | 🟢 **UYUYOR** |
| CRN uyarısı: *"uyarlamalı protokoller akışı desenkronize eder"* | 12:§3.3.1 | 🔴 **kanal rastgeleliği akıştan DEĞİL hash'ten** | 🟢 **DAHA GÜÇLÜ** |
| Eşleştirilmiş test *(t / Wilcoxon)* | 12:§4 | `06` Bölüm 3 — Wilcoxon çift yönlü | 🟢 |
| Çoklu karşılaştırma düzeltmesi | 12:§4.5 | `06` — Holm–Bonferroni, aile içinde | 🟢 **DAHA GÜÇLÜ** *(Holm > Bonferroni)* |
| **Analiz birimi = tohum, paket değil** | 12:§4.4 | `06` Bölüm 3 | 🟢 |
| Etki büyüklüğü + %95 GA raporlama | 12:§5.1 | `06` Bölüm 3 | 🟢 |
| Tohum listesi açıkça raporlanmalı | 12:§5.1 | `06` Bölüm 2 — 1–30 / 2000–2029 | 🟢 |
| Durdurma kuralı ε_rel = GA yarı genişliği / nokta ≤ %5–10 | 4:§9.2 | `08` Ç4.2 **GA %2,04** | 🟢 **SAĞLANIYOR** |
| **İstatistik katmanı KODLANMIŞ olmalı** | 12:§4 | 🔴 `wilcoxon`/`holm`/`scipy` depoda **geçmiyor** | 🟡 **EKSİK** *(`08` md 21)* |
| Isınma döneminin çıkarılması | 4:§9.2 · 16:§10.3 | `isinma_s = 50.0`, ölçüm penceresi | 🟢 **UYUYOR** |
| **Kâhin yasağı** *(jammer parametreleri yalnız motorda)* | 14:§7.1 | `03` kural 5 + `05` §B + yapısal koruma | 🟢 **BİREBİR** — §6 |
| Hesaplama ortamı raporlanmalı | 12:§5.1 | `kaynak_hash` her satırda | 🟢 **DAHA GÜÇLÜ** |

---

# 3 · 🔴 LİTERATÜR KENDİ İÇİNDE ÇELİŞİYOR

**Bu bölüm olmadan §2'nin 🔴 satırları yanlış okunur.** Aynı taramanın iki
dosyası, aynı parametre için farklı değer veriyor:

| eksen | dosya 6 §B *(13 makale, tam metin doğrulamalı)* | dosya 16 §2 *(tasarım ilkesi)* | depo |
|---|---|---|---|
| **koşu süresi** | medyan **~200 s**, aralık 100–600 s | **900–1000 s** | **350 s** |
| **bit hızı** | CBR 1–2 Mbps | **2 Mb/s** | **1 Mb/s** |
| **menzil** | 200–550 m | ~250 m | **280 m** |
| **paket** | 512 B baskın; 100–300/512/1024/2048 listeli | **512 B** | **1024 B** |
| **tekrar sayısı** | 400 koşu *(20×20)* örneği | **min 10 tohum** | **30 tohum** |
| **alan** | 2D 800–2500 m; 3D 1000³–2000×2000×300 | 1000×1000 m | **1000×1000 m** |

🔴 **Üç sonucu var:**

1. **Koşu süresinde depo, dosya 6'nın aralığında** *(100–600 s)* ve
   dosya 16'nın önerisinin **dışında**. Yani *"literatür 900 s diyor,
   biz 350 s koşuyoruz"* cümlesi **eksik alıntıdır.**
2. **Tekrar sayısında depo İKİSİNİ DE AŞIYOR** *(30 > 10)* ve dosya 4 §9.1
   şunu ölçmüş: *"MobiHoc bildirilerinin **%87,8'i** hiç güven aralığı
   raporlamadı."* Depo hem GA raporluyor hem 30 tohum kullanıyor.
3. 🔒 **KURAL:** bu belgede ve raporda *"literatür şunu diyor"* cümlesi
   **hangi dosyanın hangi örneklemden söylediği** yazılmadan kurulmaz.

⚖️ Bu, `03` B2'nin *"gürültüden dar tarama"* tuzağının literatür
tarafındaki karşılığıdır: **kaynakların kendi varyansı, bizim kaynaktan
sapmamızdan büyük.**

---

# 4 · 🔴 SJR / JSR DÖNÜŞÜMÜ — ölçüldü

**Üretici:** `PYTHONIOENCODING=utf-8 python dogrulama/sjr_donusumu.py`
*(30 tohum · 8 864 yönlü bağ örneklemi · S2)*

## 4.1 Neden gerekliydi

Literatür karıştırma şiddetini **SJR/JSR (dB)** ekseninde raporluyor
*(tarama −40…+40 dB — 3:§C.2)*. Depo **mutlak dBm** kullanıyor. Dönüşüm
hiçbir yerde yazılı değildi. **Boşluk A'nın hedeflediği tablo bu dönüşüm
olmadan literatürün eksenine oturtulamaz.**

## 4.2 Ölçülen tablo

| senaryo | tepe dBm | **kaynak J/S** | SJR ortanca | SJR p05 | SJR p95 | SINR ortanca | SINR p05 | **<−3 dB** | **<10 dB** |
|---|---|---|---|---|---|---|---|---|---|
| S0 | — | — | — | — | — | 15,00 | 10,37 | 0,0000 | 0,0000 |
| S1 | −4,00 | **−19,49** | 27,85 | 11,21 | 44,18 | 14,28 | 8,47 | 0,0069 | 0,1057 |
| **S2** | **+2,00** | **−13,49** | **21,85** | **5,21** | 38,18 | **13,38** | 4,48 | **0,0159** | **0,2069** |
| S3 *(darbeli, tepe)* | −0,99 | −16,48 | 24,84 | 8,20 | 41,17 | 13,93 | 6,68 | 0,0111 | 0,1500 |
| S4 *(darbeli, tepe)* | +5,01 | −10,48 | 18,84 | 2,20 | 35,17 | 12,56 | 1,77 | 0,0237 | 0,2905 |
| S5 *(hareketli)* | +2,00 | −13,49 | 24,69 | 7,01 | 41,49 | 13,76 | 5,91 | 0,0123 | 0,1638 |

🟢 **Belirlenimcilik doğrulandı** *(`03` Bölüm D seviye 3)*: iki ardışık
koşu **birebir aynı**, ve `PYTHONHASHSEED=7` ile koşu da **birebir aynı**.
**Üretici:**
```bash
PYTHONIOENCODING=utf-8 python dogrulama/sjr_donusumu.py > a.txt; PYTHONHASHSEED=7 PYTHONIOENCODING=utf-8 python dogrulama/sjr_donusumu.py > b.txt; diff a.txt b.txt && echo AYNI
```

**H1.2 dirsek taraması** *(aynı üretici)*:

| override | kaynak J/S | SJR ortanca | SINR ortanca | <−3 dB | <10 dB |
|---|---|---|---|---|---|
| −10 dBm | −25,49 | 33,85 | 14,70 | 0,0029 | 0,0488 |
| −4 dBm | −19,49 | 27,85 | 14,28 | 0,0069 | 0,1057 |
| +2 dBm | −13,49 | 21,85 | 13,38 | 0,0159 | 0,2069 |
| +8 dBm | −7,49 | 15,85 | 11,44 | 0,0356 | 0,3863 |
| +11 dBm | −4,49 | 12,85 | 10,06 | 0,0582 | 0,4959 |

## 4.3 🔴 ÜÇ BULGU — ve üçü de rapora girer

### (a) Kaynak J/S oranımız literatürün bandında, ama İHA lehine uçta

Literatür *(3:§C.1)*: *"Jammer/İHA güç oranı **0 dB ile +7 dB** arası …
veya İHA lehine **−15 dB**. **'Jammer her zaman çok daha güçlü' varsayımı
literatürde desteklenmiyor**; güçler aynı mertebede tutulup coğrafi yakınlık
belirleyici yapılıyor."*

Ölçülen: türetilmiş verici gücü **15,49 dBm**, S2 karıştırıcısı **+2,00 dBm**
→ **kaynak J/S = −13,49 dB**. Bandın *(−15 … +7 dB)* **İHA lehine ucunda**,
ama **içinde.** 🟢 Ve literatürün kendi cümlesi bu tercihi destekliyor:
belirleyici olan coğrafi yakınlıktır, bizde de öyle.

### (b) ⚪ SINR eşiği KARŞILAŞTIRILAMAZ — ve ölçüm bunu kanıtlıyor

Literatürün kesme eşiği **−3 dB**. Bizim `sinr_esigi_db` **10 dB**.
İkisi **aynı büyüklük değil**:

| | bizim 10 dB | literatürün −3 dB |
|---|---|---|
| ne | *menzil TANIMI* — `Pt` bundan türetilir *(radio.py:15)* | *çözme eşiği* — altında paket çözülemez |
| kod | `Radyo.kur` verici gücünü buradan hesaplar | karşılığı **yok** — PER sürekli fonksiyon |

🔴 **Ölçüm ayrımı kanıtlıyor:** S2'de bağların yalnızca **%1,59'u**
literatürün −3 dB eşiğinin altında. Yani literatürün ölçütüyle bakılırsa
S2 **"neredeyse karıştırılmamış"** görünür. Oysa aynı S2'de uçtan uca
teslim **0,5252** *(`06` §SENARYOLAR)*.

⚖️ **Bu bir çelişki değil, iki farklı katmanın ölçüsüdür** — ve tam olarak
`03` B4'ün *"bir kusuru ölçmek onu sebep yapmaz"* uyarısının tersi:
**ağ seviyesindeki büyük etki, bağ seviyesindeki küçük bir orandan doğuyor.**
Sebep ölçülü: bizim bağlarımız zaten eşiğin **kenarında** *(S0 SINR ortanca
15,00 dB · p05 **10,37 dB**)*, yani karıştırıcının birkaç dB'i marjinal
bağları koparmaya yetiyor. `06`nın *"~10–14 dB'lik dar pencere"* bulgusunun
bağ seviyesindeki karşılığı budur.

### (c) 🔴 Etkinlik eşiği kıyası — literatürün kendi ölçütüyle "zayıf" görünüyoruz

Literatür *(4:§7.2, RF Essentials)*: etkin karıştırma için gereken J/S —
analog FM **0–6 dB**, **FEC'siz sayısal modülasyon 10–15 dB**, 30 dB işlem
kazançlı yayılı spektrum 30–40 dB.

Ölçülen S2 medyan bağ J/S = **−21,85 dB** *(= −SJR)*. Yani literatürün
sayısal modülasyon için verdiği etkinlik eşiğinin **~32–37 dB altında.**

🔴 **VE BU BİR KUSUR DEĞİL, BİR ÇALIŞMA NOKTASI KARARIDIR — ama YAZILMAMIŞTI.**
Karıştırıcı gücü `06`/K-039'da **ağın dinamik aralığının ortasına** göre
seçildi *(teslim 0,5252)*, literatürün **bağ seviyesindeki** etkinlik
eşiğine göre değil. İki ölçüt farklı şeyleri en iyiler:

| ölçüt | seçtiği nokta | sonucu |
|---|---|---|
| deponun ölçütü *(ağ dinamik aralığının ortası)* | +2 dBm | teslim 0,5252 — **protokol farkı görünür** |
| literatürün etkinlik eşiği *(J/S ≥ 10 dB)* | ≫ +11 dBm | teslim ≪ 0,1198 — **ağ bölünür, hiçbir protokol kazanamaz** |

⚖️ **Deponun ölçütü bu deney için DOĞRU olandır** *(`03` B3: tabanda/tavanda
protokol farkları sıkışır)* — ama gerekçesi rapora **literatürün eşiğiyle
birlikte** yazılmalıdır, yoksa jüri *"karıştırıcınız neden bu kadar zayıf"*
diye sorar ve cevap hazır olmaz. **Şimdi hazır ve ölçülü.**

---

# 5 · 🔴 BOŞLUK A'NIN ADLANDIRMA SORUNU — K-077'nin GÖRMEDİĞİ KISIT

## 5.1 Boşluk nasıl yazılmış

`SJR PDR E2E Literatür Boşluğu.md` *(dosya 2)*, boşluğu **adlandırılmış
protokollerle** tanımlıyor:

> *"2022–2026 FANET literatüründe **OLSR, AODV ve GPSR** için değişen SJR
> altında doğrudan raporlanmış PDR ve E2E gecikme düşüş yüzdeleri
> bulunamamıştır."*

Aynı dosyanın "proje çıkarımı" bölümü, projenin iddia edebileceği cümleyi
de yazıyor — ve o cümle de üç protokolü **adıyla** anıyor.

## 5.2 🔴 Depoda bugün ne var

| yer | ne | kâhin mi |
|---|---|---|
| `dogrulama/aktaricilar.py:257` | `en_kisa_yol` | 🔴 **KÂHİN** |
| " | `hedefe_en_yakin` | 🟡 yarı-kâhin |
| " | `dongu_yapan` · `olu` | uç durum tetikleyici |
| " | `gurultuden_kacan` | 🟢 saf gözlem |
| `dogrulama/kontrol_payi.py:44` | `mesafe_vektoru` — **40 satır**, beacon yüküyle tablo taşıyor | 🟢 kâhinsiz |

🔴 **Adlandırılmış AODV, OLSR ya da GPSR uygulaması YOKTUR.** En yakın şey
`mesafe_vektoru` ve o da AODV değil, bir **DSDV benzeri** dağıtık
Bellman-Ford taslağıdır.

## 5.3 🔴 Ve ön-kayıt bunu ZATEN dışlıyor

| belge | satır | ne diyor |
|---|---|---|
| `06-ON-KAYIT.md:321` | H1.1 | *"**Atlama-sayısı temelli** yönlendirme, **bağ-kalitesi temelli**ne göre…"* — protokol **SINIFI**, adı değil |
| `08-AILE0-KAPSAM.md:361` | md 6 | *"**OLSR** — MPR seçimi **kapsam dışı**"* |

⚖️ **Yani proje, boşluğun adlandırılmış hâlini bilinçli olarak dışlamış** —
ama o karar **literatür taraması gelmeden önce** verildi ve boşluğun
adlandırılmış olduğu o zaman bilinmiyordu.

## 5.4 🔒 KARAR VERİLDİ — **A-tam**, GPSR hariç *(1 Eylül 2026, K-081)*

> ⚠️ **BU BÖLÜM 1 EYLÜL'DE DEĞİŞTİ.** Aşağıda **A-dar** öneriliyordu ve
> öğrenci 31 Ağustos'ta onu kabul etmişti. **1 Eylül'de karar tersine
> döndü** çünkü öğrenci projenin özgünlük çerçevesini netleştirdi:
> **özgünlük kendi protokolünden gelir ve o protokol STANDART
> protokollerle karşılaştırılmalıdır.** *"Protokol sınıfı"* karşılaştırması
> bu iddiayı taşıyamaz.
>
> 🔒 **YÜRÜRLÜKTEKİ KARAR:** **AODV · OLSR · AOMDV** adlarıyla kurulur.
> **GPSR kapsam dışı** *(`01` §5.1 · `08` md 33)*.
>
> 🟢 **Ve bu, Boşluk A'yı yan ürün olarak DOLDURUR** — rakipleri kurup SJR
> ekseninde ölçmek §5.1'in boşluğunu tam olarak kapatır.
> ⚠️ Boşluk metni *"OLSR, AODV **ve GPSR**"* diyor; GPSR olmadan iddia
> **kısmen** doldurulur ve bu **açıkça yazılır**.

### Eski öneri — kayıt için korunuyor



| # | iddia | gerektirdiği | maliyet |
|---|---|---|---|
| **A-dar** | *"Sabit topolojide, adlandırılmış karıştırıcı sınıfları altında, **atlama-sayısı temelli ve bağ-kalitesi temelli yönlendirme sınıflarının** SJR'ye bağlı PDR/E2E bozunumu"* | **bugünkü araç** | 🟢 **sıfır** |
| **A-tam** | *"**OLSR, AODV ve GPSR** için SJR'ye bağlı PDR/E2E"* | üç protokolün RFC uyumlu uygulaması | 🔴 `06` H1.1 + `08` md 6 **yeniden yazılır**; ön-kayıt mührü etkilenir |

🔴 **A-dar bir geri çekilme DEĞİLDİR:** literatürün kendi boşluk cümlesi
*"bu protokollerin karşılaştırmalı davranışı"* diyor ve dosya 9 §2 **ikinci
bir boşluk** daha beyan ediyor — *"OLSR, AODV, GPSR ve AOMDV'nin RF
karıştırma altında **saniye ölçeğinde rota kurtarma gecikmesi** bildiren
doğrudan birincil kaynak bulunamamıştır."* İkisi de **sınıf düzeyinde**
ölçülebilir.

⚠️ Fiyatlandırma `11-REFACTORING-ONERISI.md` **R-9**'dadır.

---

# 6 · 🟢 LİTERATÜRÜN DOĞRULADIKLARI

## 6.1 Soyutlama seviyesi — tam yerinde

`RF Jamming SINR-PER Soyutlama Modeli.md` dört seviye sayıyor ve
**Seviye 3'ü** *"en yaygın ve en titiz"* diye niteliyor. Depo tam orada:

```
Karıştırıcı → yol kaybı → J_r ─┐
Verici → yol kaybı → S_r ──────┼→ SINR → BER → PER → Bernoulli
Termal gürültü N₀B ────────────┘
```

🟢 Ve **chunk bazlı PER** *(§4.2)* gibi ince bir ayrıntı bile birebir
uygulanmış — üstelik o mekanizma **B-117/M07 ile mutasyonla korumaya
alınmış** *(K-074)*. Bir dış kaynağın *"gerekir"* dediği şey, depoda
**kırılabilir bir testle** duruyor.

## 6.2 🔴 KÂHİN YASAĞI — dışarıdan, bağımsız doğrulama

`Jamming-Aware Q-Learning Ödül Fonksiyonu.md` **§7.1**:

> *"Karıştırıcı gücü P_J, konumu veya etki yarıçapı R_J **yalnızca
> simülatör motoru tarafından bilinir**. Yönlendirme ajanı bunlara doğrudan
> erişemez."*

Bu, `03` **kural 5**'in ve `05` **§B**'nin birebir aynısıdır. 🟢 Projenin en
katı kuralı artık **dış kaynaklı bir gerekçeye** de sahip.

## 6.3 🟢 GİZLİ VARLIK — `08` madde 22'nin yeniden okunması

Literatürün ajandan istediği tahmin girdileri, `05`te **zaten var**:

| literatürün istediği | kaynak | `05` alanı | bugün |
|---|---|---|---|
| ACK/NACK'ten PER tahmini | 14:§7.2 | `son_iletim_sonucu` | 🔴 okunmuyor |
| Dinlemeyle girişim → SINR tahmini | 14:§7.3 | `olculen_gurultu_w` | 🔴 okunmuyor |
| JSR tahmini = SNR − SINR | 14:§7.4 | ikisinden türetilir | 🔴 |
| Komşunun bildirdiği durum | 14:§2.2 | `bildirdigi_gurultu_w` · `bildirdigi_kuyruk` | kısmen |

🔴 **BEYAN DEĞİŞMİYOR, GEREKÇESİ DEĞİŞİYOR.** `08` madde 22'nin
*"14 alanın tüketicisi yok"* ölçümü **aynen geçerlidir** — okunmayan alan
okunmayan alandır. Değişen şey: bu alanlar **ölü ağırlık değil, Aile 3'ün
sensör takımıdır.**

## 6.4 🟢 Tablo tabanlı Q-learning `03` kural 9'u ihlal etmiyor

> ⚠️ **BU BİR TASARIM KARARI DEĞİL, BİR MÜSAADE TESPİTİDİR.**
> Projenin özgün protokolü **Q-learning değildir**; tasarım öğrenciden
> gelecek ve `06` §5.1 bilerek boş *(K-081)*. Aşağıdaki paragraf yalnızca
> şunu söyler: **eğer** bir gün tablo tabanlı bir yaklaşım seçilirse,
> kural 9 buna engel değildir.

`14:§8.2` ölçüyor: |S| = 3 600 durum × 40 düğüm × d̄≈6 eylem ≈ **864 000
giriş ≈ 7 MB**. Kural 9 **derin** öğrenmeyi yasaklıyor *(DQN/PyTorch — SWaP)*;
tablo tabanlı yaklaşım yeni bağımlılık gerektirmiyor. 🟢 Serbest.

## 6.5 🟢 `01-PROBLEM-VE-AMAC.md` §2.2'nin boşluk iddiası doğrulandı

`01` §2.2, *Mathematics* 2022 derlemesine dayanarak *"mevcut ödül
fonksiyonlarının hiçbirinde girişim/karıştırma terimi yok"* demişti.
Dosya 17 §3.12 bunu **bağımsız olarak, 11 protokollük bir matrisle**
doğruluyor: "Açık Jamming" sütunu 9 protokolde **Yok**, 1'inde *kısmen*,
1'inde *evet* — ve o birinde *(RLGM)* jammer **tespiti** var, yönlendirme
**ödül fonksiyonu yok**.

## 6.6 🟢 Ön-kayıt yöntemi literatürle aynı çerçevede

`Yöntem Ön-Kayıt…md` ADEMP-PreReg *(Siepe vd. 2024)* çerçevesini anlatıyor
ve `06`nın yaptığı şeyle örtüşüyor. 🔴 **İki yerde depo daha güçlü:**

1. **Holm > Bonferroni** — literatür Bonferroni öneriyor *(12:§4.5)*,
   `06` Holm–Bonferroni kullanıyor *(daha güçlü, aynı hata kontrolü)*.
2. **CRN'in kırılganlığı çözülmüş** — literatür uyarıyor *(12:§3.3.1)*:
   *"uyarlamalı protokollerde farklı kontrol yolları farklı sayıda RNG
   çağrısı yapabilir ve akışları desenkronize edebilir"*, çözüm olarak
   **ön-üretilmiş iz dosyaları** öneriyor. `07` bunu **hash tabanlı kanal
   çekimiyle** çözüyor: `(tohum, gönderen, alan, dilim)`. Dosya gerekmiyor
   ve desenkronizasyon **yapısal olarak imkânsız.**

---

# 7 · 🔴 LİTERATÜRÜN MEYDAN OKUDUKLARI

| # | konu | ağırlık | nereye gider |
|---|---|---|---|
| **1** | **3B geometri** — literatürde standart, depo 2B | 🔴 stratejik | R-8 |
| **2** | **3B Gauss-Markov mobilite** — α=0,85, adım 0,5 s, 10–30 m/s | 🔴 stratejik | R-8 |
| **3** | **Adlandırılmış protokoller** — §5 | 🔴 stratejik | R-9 |
| **4** | **İstatistik katmanı kodlanmamış** | 🔴 **Aile 1'den önce** | R-2 |
| **5** | **PSR raporlanmıyor** — *"PDR tek başına yanıltıcıdır"* | 🔴 metrik | R-12 |
| **6** | **Gecikme yüzdelikleri + IPDV** — RFC 7679 | 🟢 şema maliyeti **sıfır** | R-13 |
| **7** | **Rota kurtarma gecikmesi Δ ve COR** | 🟡 Aile 1'in ikinci boşluğu | R-14 |
| **8** | **SJR raporlama ekseni** | 🟢 ucuz, kazanç büyük | R-7 |
| **9** | Paket boyutu 512 B | 🟡 **çalışma noktasını taşır** — §2.4 | R-5 |
| **10** | Bit hızı 2 Mb/s *(Li'nin kendi noktası)* | 🟡 | R-10 |
| **11** | Gölgeleme X_σ | 🟡 beyanlı | R-6 |
| **12** | Çoklu karıştırıcı *(1–4, tipik 3)* | 🟡 beyanlı *(`08` md 18)* | R-15 |
| **13** | Karıştırıcı sınıf taksonomisi *(11 sınıf)* — depoda **3** *(sabit/darbeli/hareketli)* | 🟡 | R-15 |
| **14** | Kontrol kanalı karıştırması *(baraja göre ~20 dB daha J/S-verimli)* | 🟡 | R-15 |

---

# 7b · 🔴 İKİ EKSEN ÖLÇÜLDÜ — tahmin değil

**Üretici:** `PYTHONIOENCODING=utf-8 python dogrulama/literatur_eksenleri.py`
**300 tam koşu · 4,3 dk · korunum 300/300 · yazılan satır 300/300**
*(tahmin bandı 4,5–9,6 dk; gerçekleşen bandın hemen altında)*

🔒 **İki kol birden koşuldu** — `en_kisa_yol` *(kâhin, Ç1'in iş atı)* ve
`gurultuden_kacan` *(saf gözlem)*. Tek kolla ölçülen bir etki, kolun
özelliği sanılabilirdi *(`03` B1)*.
🔒 **İÇ İÇE koşuldu** — tek `Pool` yığını, karıştırılmış sıra *(K-075)*.

## 7b.1 🟢 ÖNCE: ARAÇ KENDİNİ DOĞRULADI — 0,5252 BİREBİR ÜRETİLDİ

Yeni ölçüm boru hattı, üretim boru hattıyla aynı sonucu veriyor mu?
`config.py`nin kalibrasyon tablosu S2 için **0,5252** diyor ve
`06` §SENARYOLAR o sayının **5 tohumdan** *(1·7·13·19·23)* geldiğini yazıyor.

| örneklem | teslim oranı |
|---|---|
| bu ölçüm, **aynı 5 tohuma** kısıtlanmış | **0,5252** |
| `config.py` / `06` beyanı | **0,5252** |
| bu ölçüm, **30 tohum** | **0,5120** *(std 0,1569 · [0,1996 · 0,7904])* |

🟢 **Dört ondalığa kadar birebir.** Bu, F-4'ün *"üretilemeyen üretici"*
bulgusunun **tersidir**: kalibrasyon sayısı bugün üretilebiliyor ve üretildi.

⚖️ **VE ÇALIŞMA NOKTASI KARARI 30 TOHUMDA DAHA İYİ ÇIKTI** *(Y6 — kendi
lehime çıkan sonuca da uygulanır)*: K-039'un hedefi dinamik aralığın ortası
**0,5076**'ydı.

| örneklem | teslim | ortadan uzaklık |
|---|---|---|
| 5 tohum *(kararın verildiği)* | 0,5252 | 0,0176 |
| **30 tohum** | **0,5120** | **0,0044** |

🔒 **S2 = +2 dBm seçimi DEĞİŞMİYOR** ve gerekçesi güçleniyor.
⚠️ Ama tohumlar arası std **0,1569** ve aralık **[0,1996 · 0,7904]** —
karar 5 tohumla verilmişti ve o beşinin kendisi 0,2973–0,7683 arasında
geziniyordu. `03` kural 2'nin *"tek/az tohumlu sonuç"* uyarısı burada
**ölçülmüş** hâliyle duruyor.

## 7b.2 EKSEN 1 — paket boyutu 512 B ↔ 1024 B *(eşleştirilmiş, 30 tohum)*

| kol | senaryo | metrik | 512 B | 1024 B | fark | std | işaret |
|---|---|---|---|---|---|---|---|
| `en_kisa_yol` | S0 | teslim | 0,9998 | 0,9962 | **+0,0036** | 0,0050 | **30/30** |
| | S0 | gecikme (s) | 0,0219 | 0,0459 | **−0,0240** | 0,0081 | 0/30 |
| | **S2** | **teslim** | **0,5597** | **0,5120** | **+0,0477** | 0,0539 | **28/30** |
| | S2 | gecikme (s) | 0,0210 | 0,0426 | **−0,0216** | 0,0108 | 0/30 |
| | S2 | kontrol bayt | 422 245 | 413 919 | +8 326 | 9 634 | 26/30 |
| `gurultuden_kacan` | S0 | teslim | 0,3297 | 0,3432 | −0,0135 | 0,0354 | 8/30 |
| | S0 | gecikme (s) | 0,1425 | 2,4018 | **−2,2593** | 2,4517 | 0/30 |
| | S2 | teslim | 0,2530 | 0,2578 | −0,0048 | 0,0228 | 9/30 |
| | S2 | gecikme (s) | 0,0774 | 1,6662 | **−1,5888** | 2,0960 | 0/30 |

🔴 **R-5 "ucuz bir değişiklik" DEĞİLDİR — üç ölçülmüş sonuç:**

1. **S2'de teslim +0,0477** *(28/30 tohumda pozitif)*. Yani 512 B'a geçmek
   çalışma noktasını **0,5120 → 0,5597**'ye taşır ve K-039'un
   *"dinamik aralığın ortası"* gerekçesi **yeniden ölçülmeden geçersizdir**
   *(hedef 0,5076; yeni uzaklık 0,0521 — eskisinin 12 katı)*.
2. **Gecikme 30/30 tohumda düşüyor** — paket süresi 8 384 → 4 288 µs.
3. 🔴 **Sebebi ölçülü ve iki bileşenli:** menzilde PER **%16,97 → %8,88**
   *(radio.py)* **ve** sunulan airtime yükü **%8,384 → %4,288** *(§2.4)*.
   Yani 512 B *"aynı deney, farklı paket"* değil, **daha kolay bir deneydir.**

⚖️ **Öneri (karar öğrencinin):** 1024 B **birincil** kalsın — literatürün
*(11:§4)* "video/büyük veri" bandında ve normalize yük baseline'la birebir
*(§2.4)*; 512 B **ilan edilmiş bir duyarlılık ekseni** olarak raporlansın.
Bu tablo o duyarlılık ekseninin **kendisidir** ve şimdiden ölçülmüştür.

## 7b.3 EKSEN 2 — koşu uzunluğu 200 s ↔ 350 s · `06` Bölüm 5 koşul 1

> `06` Bölüm 5: *"Dördü birden sağlanmayan hiçbir sonuç raporlanmaz:
> **1. Sonuç koşu uzunluğundan bağımsız** …"*
> 🔴 **Bu koşul bugüne kadar HİÇ ÖLÇÜLMEMİŞTİ.**

| kol | metrik | kısa (200 s) | tam (350 s) | fark | std | işaret |
|---|---|---|---|---|---|---|
| `en_kisa_yol` | teslim | 0,5125 | 0,5120 | **+0,0005** | 0,0056 | **15/30** |
| `en_kisa_yol` | gecikme (s) | 0,0445 | 0,0426 | +0,0019 | 0,0056 | 16/30 |
| `gurultuden_kacan` | teslim | 0,2532 | 0,2578 | **−0,0046** | 0,0112 | **8/30** |
| `gurultuden_kacan` | gecikme (s) | 1,5284 | 1,6662 | −0,1378 | 0,6676 | 10/30 |

🟢 **`en_kisa_yol` için koşul SAĞLANIYOR** — fark 0,0005, işaret 15/30
*(yazı-tura)*. Kâhin aktarıcının sonucu koşu uzunluğundan bağımsız.

🔴 **`gurultuden_kacan` için SAĞLANMIYOR** — işaret **8/30** *(yani 22/30'da
kısa koşu daha DÜŞÜK)*. Büyüklük küçük *(−0,0046, std'nin ~0,4 katı)* ama
**yön sistematik**.

⚖️ **Bu tam olarak `03` B3'ün uyardığı şeydir:** *"Isınma **asimetriktir** —
protokoller farklı hızda yakınsar."* Gözlem tabanlı kol 200 s'de **henüz
yakınsamamış**; kâhin kol zaten ilk andan itibaren en iyi yolu biliyor.

🔒 **İKİ SONUCU VAR:**
1. **350 s KORUNMALI.** Literatürün 200 s medyanına inmek *(dosya 6 §B)*
   yavaş yakınsayan kolları **sistematik olarak cezalandırır** — ve Aile 1'in
   rakipleri tam olarak o sınıftır.
2. 🔴 **Aile 1'in her kolu için bu ölçüm TEKRARLANMALI.** Bugün ölçülen iki
   kol; bir protokol daha yavaş yakınsıyorsa `06` koşul 1 onun için düşer.

## 7b.4 🔴 GECİKME YÜZDELİKLERİ — literatürün uyarısı KENDİ ARACIMIZDA doğrulandı

**Şemaya dokunulmadı** — hepsi `teslim_gecikmeleri_s`den türetildi.

| kol | senaryo | teslim | ort (ms) | **p50** | **p95** | **p99** |
|---|---|---|---|---|---|---|
| `en_kisa_yol` | S0 | 0,9962 | 45,83 | 27,06 | 92,04 | 560,67 |
| `en_kisa_yol` | **S2** | **0,5120** | **44,29** | **22,92** | **115,95** | 398,59 |
| `gurultuden_kacan` | S0 | 0,3432 | 2 031,47 | 99,62 | 12 563,03 | 26 603,33 |
| `gurultuden_kacan` | S2 | 0,2578 | 1 274,61 | 65,49 | 7 872,35 | 21 399,28 |

🔴 **S0 → S2'de teslim YARIYA iniyor** *(0,9962 → 0,5120)* **ve:**

| metrik | S0 → S2 | ne söylüyor |
|---|---|---|
| **ortalama** | 45,83 → 44,29 ms *(**−%3,4**)* | 🔴 *"karıştırma gecikmeyi İYİLEŞTİRDİ"* — **yalan** |
| **p50** | 27,06 → 22,92 ms *(−%15,3)* | aynı yalan, daha güçlü |
| **p95** | 92,04 → **115,95 ms** *(**+%26,0**)* | 🟢 **gerçek: kuyruk kötüleşti** |
| p99 | 560,67 → 398,59 ms *(−%28,9)* | 🔴 en kötü paketler artık **hiç teslim edilmiyor** |

⚖️ **Bu, `08` madde 16'nın ve literatürün *(4:§3.2, RFC 7679)* uyardığı
hayatta-kalan yanlılığının kendi aracımızdaki ÖLÇÜLMÜŞ hâlidir.**
Ortalama ve p50 **ters yönü** gösteriyor; yalnızca **p95** doğru yönü
gösteriyor; p99 ise **kesiliyor** çünkü en zor paketler dağılıma hiç
girmiyor.

🔴 **Rapora giren cümle:** *"S2'de ortalama gecikme S0'a göre %3,4 DÜŞÜKTÜR
ve bu bir iyileşme DEĞİLDİR: aynı noktada p95 %26,0 ARTMIŞTIR ve teslim
oranı 0,9962'den 0,5120'ye inmiştir."*

🟢 **Maliyeti sıfır:** `06` Bölüm 4 yüzdelik istemiyor; istemesi gerekiyor
ve **şema zaten taşıyor** *(R-13)*.

---

# 7c · 🔴 İKİNCİ OKUMA TURU — %62'den tam kapsama

> **Neden bu bölüm var:** ilk tur %62 kapsamdı *(§1)*. Öğrenci sordu,
> ölçüldü, eksikler okundu. **Yedi bulgu çıktı; beşi ilk turda hiç
> görülmemişti.**

## Y-1 🔴 LİTERATÜRÜN KENDİ ÖDÜL FORMÜLÜ KÂHİN İÇERİYOR

`Jamming-Aware Q-Learning Ödül Fonksiyonu.md` **kendi içinde çelişiyor:**

| yer | ne diyor |
|---|---|
| **§7.1** | *"Karıştırıcı gücü, konumu veya etki yarıçapı **yalnızca simülatör motoru tarafından bilinir.** Ajan bunlara doğrudan erişemez."* |
| 🔴 **§5.7** *(tam formül)* | `f_jam` dördüncü terimi: **1{d(j, J) ≤ R_J}** — *düğümün karıştırıcıya mesafesi* |
| 🔴 **§11.1** *(referans kod)* | `in_radius = link_metrics['in_jamming_radius'][j]` · `sinr_j = link_metrics['sinr'][i,j]` · `jsr = link_metrics['jsr'][i,j]` — **üçü de simülatörden** |

🔴 **§11.1'i kopyalayan bir uygulama `03` kural 5'i ihlal eder ve tüm Aile 3
sonuçlarını geçersiz kılar.** §7 düzeltmeyi veriyor *(ρ_j PER sapmasından
tahmin edilir)* ama **§5.7'nin formülü ve §11.1'in kodu düzeltilmemiş.**

⚖️ **Bu, `03` B5'in *"belge kodun kanıtı değildir"* tuzağının literatür
tarafındaki karşılığıdır** — ve bu depo tam olarak o hatayı yakalayacak
donanıma sahip. 🔒 Aile 3'e girilirse **§7 uygulanır, §5.7/§11.1
uygulanmaz** ve bu karar kaydına geçer.

## Y-2 🔴 `01` §2.2'NİN "TABLE 26" İDDİASI YENİDEN DOĞRULANAMADI

| kaynak | ne diyor |
|---|---|
| `01` §2.2 | *"Aynı derlemenin **Table 26**'sı … **doğrulanmış bir tablodan** okunan somut bir boşluktur"* |
| `02` B6/B7 | ✅ *"Mathematics 2022, 10, 3017, **s.49 + Table 26**"* · 5 satırlık **kısmi** kopya |
| 🔴 **yeni tarama** *(dosya 17, kapanış notu)* | *"**MDPI tam metnine erişim kısıtlı olduğundan** Lansky vd. (2022) derlemesinin protokol listesi **arama özeti ve metadata üzerinden** doğrulanmıştır"* |

Ayrıca **protokol sayısı uyuşmuyor:**

| kaynak | sayı | fark |
|---|---|---|
| `01` §2.2 · `02` B6 | **13** | TARRAQ var |
| dosya 17 §2 | **14** | DQN-VR + TQNGPSR var, TARRAQ yok |

🔴 **BU, B7'Yİ ÇÜRÜTMEZ** — `02` tabloyu kısmen kopyalamış, yani bir zaman
erişilmiş. **Ama yeniden üretilemedi.** Y14'ün tarifi: *"mühürlenecek bir
belgedeki sayı, yeniden koşulmadan mühürlenemez."*

🔒 **Karar gerekir:** B7 raporun **özgünlük iddiasını** taşıyan cümledir.
Ya *(a)* tam metne erişilip Table 26 yeniden doğrulanır, ya *(b)* iddia
**dosya 17'nin kendi matrisine** dayandırılır *(11 protokol, "Açık Jamming"
sütunu 9'da **Hayır**)* — ki o matris **erişilebilir kaynaklardan
derlenmiş** ve bu yazılı. **Önerim: (b)** — daha zayıf görünür, ama
**yeniden üretilebilir**.

## Y-3 🔴 LİTERATÜR "2B MOBİLİTE"Yİ *YAYGIN HATA* SAYIYOR

`Baseline Simülasyon Kurgusu.md` **§12 Yaygın Hatalar**:

| hata | etki | çözüm |
|---|---|---|
| **2D mobilite modeli kullanmak** | *"3D FANET dinamiklerini kaçırmak"* | *"3D Gauss-Markov"* |
| Isınma süresi olmadan metrik toplamak | transient etki | ilk 50–100 sn atla 🟢 **bizde var** |
| Tek tekrar yapılması | istatistiksel güvenilmezlik | min. 10 tekrar 🟢 **bizde 30** |
| Free-space yayılım modeli | aşırı iyimser bağlantı | log-distance 🟢 **bizde var** |
| MAC katmanını atlamak | çarpışma modeli yok | 802.11 DCF 🟢 **bizde var** |
| Rota keşif süresini gecikmeye dahil etmemek | E2E eksik | 🟡 Aile 1'de geçerli olacak |

🔴 **Beş hatanın dördünden temizyiz; biri bizde var ve literatür ona
"hata" diyor.** `08` madde 17/7 bunu *"beyan edilmiş sınır"* diye taşıyor —
**beyan doğru, ama çerçeve değişiyor:** bu bir nötr parametre tercihi
değil, literatürün **adlandırılmış bir hatası**.

⚖️ Bu, R-8'in *(3B + mobilite)* gerekçesini **güçlendirir** — ama maliyeti
değiştirmez *(+5–8 hafta)*. Karar hâlâ takvim kararıdır, sadece artık
"literatür farklı yapıyor" değil, **"literatür buna hata diyor"** olarak
yazılmalı.

## Y-4 🔴 LİTERATÜRÜN **ASGARİ** BAĞIMLI DEĞİŞKEN KÜMESİ — bizde 2/7

`FANET'te EH…md` **§11 Önerilen Deney Tasarımı İskeleti**:

> *"**Bağımlı değişkenler:** … **asgari olarak** PDR + PSR, D̄ ile p95,
> O_pkt ile NRL, üç ayrı kopma sayacı, Δ = |T_r − T_d| ve COR."*

| # | asgari metrik | bizde |
|---|---|---|
| 1 | PDR | 🟢 `teslim_orani` |
| 2 | **PSR** | 🔴 **yok** *(R-12)* |
| 3 | D̄ | 🟢 `ortalama_gecikme_s` |
| 4 | **p95** | 🔴 **yok** *(R-13 — şema taşıyor)* |
| 5 | O_pkt + **NRL** | 🟡 türetilebilir |
| 6 | **üç kopma sayacı** | 🔴 **yok** |
| 7 | **Δ + COR** | 🔴 **yok** *(R-14)* |

🔴 **R-12 · R-13 · R-14 artık "isteğe bağlı iyileştirme" DEĞİL — literatürün
ilan ettiği ASGARİ kümenin parçası.** `11`'deki öncelikleri buna göre
yükseltildi.

🟢 **Aynı §11'in istatistiksel tasarım şartlarını KARŞILIYORUZ:**
hücre başına **≥20 tekrar** *(bizde 30)* · açıkça raporlanmış tohumlar ·
%95 GA · **ε_rel ≤ %10** *(bizde Ç4.2'de %2,04)*.

## Y-5 🟢 SANITY DOĞRULAMA TESTLERİ — birincisi bizde geçiyor

`Baseline…md` **§13**:

| # | test | bizde |
|---|---|---|
| 1 | **Statik ağ, bağlı → PDR ≈ 1** | 🟢 `en_kisa_yol` S0: **0,9962** *(30 tohum, min 0,9719)* |
| 2 | Tek link kopması → AODV RERR / OLSR zaman aşımı | ⚪ protokol yok |
| 3 | Hareket/kayıp yok → OLSR periyodik, AODV keşifte | ⚪ protokol yok |
| 4 | Olay izleri RFC/ns-3 ile karşılaştırma | 🔴 yapılmadı |

⚠️ **`gurultuden_kacan` S0'da 0,3432** veriyor — testi geçmiyor. Ama o bir
**protokol değil**, hedef farkındalığı olmayan bir doğrulama aktarıcısıdır
*("en az gürültü bildiren komşuyu seçer")*. Test 1 gerçek protokollere
uygulanır. 🔒 **Aile 1'in her kolu bu testi geçmek zorunda** ve bu şimdi
yazılı.

## Y-6 🔴 AODV'NİN ANA ARIZA MEKANİZMASI BİZİM KURGUMUZDA TETİKLENEMEZ

`AODV-OLSR Sistemik Zayıflıklar.md` §1.1(e) — **zaman kararlılığı şartı**:

```
T_link ≥ T_RTT ≈ 2 · h · T_trav
```

*"Eğer link ömrü rota keşif RTT'sinden kısa ise, rota kurulmadan eskir."*

🔴 **Sabit topolojide `T_link = ∞`.** Yani AODV sınıfının literatürde
tanımlanan **birincil çöküş mekanizması** *(mobilite → kopma → RREQ selleme
→ pozitif geri besleme)* bizim kurgumuzda **tanım gereği oluşamaz.**
Bizde kopma yalnızca **karıştırmadan** gelir.

⚖️ **Bu bir kusur değil, iddianın SINIRIDIR** — ve A-dar'ın metnine
girmelidir: *"karıştırma kaynaklı bozunum ölçülmüştür; mobilite kaynaklı
kontrol düzlemi çöküşü kapsam dışıdır."* 🔴 Bu cümle olmadan bir jüri üyesi
haklı olarak *"AODV zaten böyle çökmez"* diyebilir.

## Y-7 🟡 JAMMER SINIF/KONUM EKSENİ — 3'e karşı 5 ve 1'e karşı 3

`FANET'te EH…md` §11 bağımsız değişkenleri:

| eksen | literatürün istediği | bizde |
|---|---|---|
| karıştırıcı sınıfı | {yok, sürekli, reaktif, aldatıcı, taramalı} — **adlandırılmış** | 3 *(S0 · sabit · darbeli · hareketli)* |
| J/S düzeyi | ≥3 düzey *(eşiğin −3/0/+3 dB'i)* | 🟢 8 nokta *(H1.2)* |
| karıştırıcı sayısı/konumu | **{1 merkezî, 1 kenar, 3 dağıtık}** | 🔴 yalnız **1 merkezî** |
| düğüm sayısı | {10, 25, 50} | 🔴 sabit **40** |

🔴 **"1 merkezî" `08` madde 18'de zaten *"sonucu bizim lehimize çevirebilecek
en büyük tek modelleme sınırı"* diye yazılı.** Literatür bunu bağımsız
olarak doğruluyor: **kenar ve dağıtık karıştırıcı ayrı eksenler.**
🟢 **Ucuz kısmı var:** `karistirici_konum` **zaten bir `Konfig` alanı**
*(`config.py:186`)* — kenar karıştırıcı **kod değişikliği gerektirmez**,
yalnızca bir tarama ekseni. *(R-15b)*

---

# 8 · 🔴 ÜRETİLEMEYEN ÜRETİCİ KOMUTLAR — yeni bulgu

**Ölçüldü:**

```bash
ls -d scratchpad          # -> No such file or directory
grep -rhno "scratchpad/[A-Za-z0-9_./]*\.py" v2/*.md sim/*.py dogrulama/*.py tests/*.py | sed 's/^[0-9]*://' | sort -u
```

**Sonuç: `scratchpad/` dizini depoda YOK**, ama **9 ayrı betiğe 14 referans**
var, **6 dosyada**:

| dosya | referans |
|---|---|
| `v2/04-NEDEN-BOYLE.md` | 6 |
| `v2/08-AILE0-KAPSAM.md` | **2** |
| `sim/kosucu.py` | 1 |
| `dogrulama/mutasyon_paketi.py` | 1 |
| `tests/test_gozlem.py` | 1 |
| `tests/test_kosucu.py` | 3 |

Betikler: `b101_derinlik` · `b105_kapsam` · `b105_pencere` · `b109_li` ·
`b117_kacirmalar` · `b117_olcum` · `c13_tani` · `d10_ust_uc` · `olu_dallar`.

🔴 **İkisi `08`'in MÜHÜRLENMEYİ BEKLEYEN sayfasında:**

| `08` yeri | sayı | üretici |
|---|---|---|
| madde 31 | pencere dışı kontrol baytı **%17,63–22,84** | `scratchpad/b105_pencere.py` |
| Ç4 çalışma noktası | Li @2 Mbit/s: **1,761 / 0,277 Mbps** | `scratchpad/b109_li.py` |

⚖️ **Bu, B-25 · B-80 · B-81'in birebir aynı örüntüsüdür** — *"üretici satırı
var, sayı üretilemiyor"* — ama **ölçeği daha büyük**: tek bir sayı değil,
dokuz betik ve iki mühür bekleyen değer.

🟢 **Ve bu belge o hatayı tekrarlamıyor:** yeni ölçüm betikleri
`dogrulama/` altına yazıldı *(`sjr_donusumu.py` · `literatur_eksenleri.py`)*,
scratchpad'e değil.

🔴 **Y13 gereği kapanış iddiası YOK:** bu bir **bulgudur**, düzeltmesi
`11-REFACTORING-ONERISI.md` **R-16**'dadır ve öğrenci onayına tabidir.

---

## 8.1 🟢 F-4 KAPANDI — iki mühür bekleyen sayı yeniden üretildi *(B0.6)*

| `08` yeri | sayı | eski üretici | 🟢 yeni üretici | sonuç |
|---|---|---|---|---|
| **Ç4** çalışma noktası | Li @2 Mbit/s **1,761 / 0,277 Mbps** · plato 1/6,36 | `scratchpad/b109_li.py` ❌ | `dogrulama/li_calisma_noktasi.py` | 🟢 **dördü de BİREBİR** |
| **md 31** | pencere dışı kontrol baytı **%17,63–22,84** | `scratchpad/b105_pencere.py` ❌ | `dogrulama/pencere_kapsami.py` | 🟢 **%18,17–22,86** *(uyumlu)* |

> ## ⚠️ BU BLOK B0.7'DE DÜZELTİLDİ — **B-120 · B-123**
>
> Aşağıdaki iki iddia **yanlıştı** ve yedinci bağımsız denetim ikisini de
> kırdı. Metin **silinmiyor** *(`04`ün kuralı: çürütülen iddia görünür
> kalır)*; doğrusu altında yazılı.

🔴 ~~**AMA md 31'in İKİNCİ SAYISI YENİDEN ÜRETİLEMEDİ.** İlan edilen
*"çarpıklık 1,004–1,079"* değerleri bir **tüm koşu / pencere** oranı
**olamaz**: o oran analitik olarak **[1,1852 · 1,2963]** bandına hapistir
*(320/270 ve 350/270)*.~~ · ~~ölçüldü: **1,2221–1,2963**~~

## 🔴 DOĞRUSU *(B0.7, 900 tam koşu, 30 tohum)*

| iddia | ne oldu |
|---|---|
| *"[1,1852 · 1,2963] **analitik** bir banddır"* | 🔴 **YANLIŞ** — band üç varsayıma dayanıyor *(sayaç zamanda düzgün · üretim [0, koşu bitişi] · pencere [50, 320])* ve **üçü de kırılıyor** |
| *"1,004–1,079 **olamaz**"* | 🔴 **YANLIŞ** — `isinma_s` = 5/15/25'te çarpıklık **1,0144/1,0446/1,0766** doğrudan üretiliyor |
| *"çarpıklık 1,2221–1,2963"* | ⚠️ **TEK TOHUMLUKTU** *(B-123)*. 30 tohumda: **1,1993 – 1,2993** |
| *"pencere dışı pay %18,17–22,86"* | ⚠️ tek tohumluk. 30 tohumda: **%16,62 – %23,03** *(ortanca %21,12)* |

🔴 **Bandın kırıldığının üç ölçülmüş kanıtı:** *(a)* aracın **kendi
sayaçlarından üçü** dışarıda — `beacon_gonderilen` **1,3398** *(üstten)*,
`veri_bayt` ve `mac_deneme` **1,1786** *(alttan)*; *(b)* `hedefe_en_yakin`
**tohum 4**'te 1,2993 ile üst çapayı aşıyor; *(c)* yukarıdaki `isinma_s`
taraması.

🔴 **Ve bedeli iki katlıydı:** yanlış varsayım bir `assert`e dönüşmüştü ve
`pencere_kapsami.py` **tohum 4'te çöküyordu** — yani `08` md 31'in yeni
üreticisi yalnızca B0'ın seçtiği tek tohumda koşuyordu.

🟢 **Gerçekten analitik olan tek çapa korundu ve güçlendi:** `olu` kolu
yalnız beacon üretir; oranı **1,2963 = 350/270**'e oturmak zorundadır ve
**180 hücrede en büyük sapma 0,000000**.

🟢 **Bağlayıcı cümle ayakta:** çarpıklık kola göre değişiyor, dolayısıyla
tüm koşu hâliyle yapılan eşleştirilmiş bir kol karşılaştırması yanlıdır.

⚠️ **Kalan ölü referanslar BEYAN EDİLDİ, uydurulmadı:** `sim/kosucu.py`nin
`_PENCERE_SAYACLARI` yorumu *(b105_kapsam)* artık *"üretici ölü"* diyor;
`04`ün altı tarihî referansı ve `tests/` içindeki dördü **mühür beklemiyor**
ve tarihî kayıt olarak duruyor *(`04` kuralı: eski kayıt silinmez)*.

## 8.2 🔴 VE BİR ÜÇÜNCÜ ÖLÜ ÜRETİCİ ÇIKTI — `08` md 25

F-4 taraması `scratchpad/` referanslarını arıyordu; **md 25'in üreticisi
çalışıyordu ama sayısı `03` kural 2'yi ihlal ediyordu**: bağlayıcı
*"8,3–17,8 kat"* oranı **3 tohumdan** geliyordu *(kural: ≥30)*.
30 tohumla yeniden ölçüldü — ayrıntı `08` md 25.

| okuma | eşleştirilmiş oran |
|---|---|
| tüm koşu · bayt *(eski)* | **4,3–38,1 kat** |
| 🔒 pencere · bayt | **4,0–38,0 kat** |
| pencere · airtime | **2,6–18,9 kat** |

⚖️ **İki ders:** *(a)* açıklık ilan edilenden **iki kat geniş** — üç tohum
onu dar gösteriyordu; *(b)* **airtime okuması bayttan DAHA DAR**, yani
bayt metriği asimetriyi **abartıyor**.

---

# 9 · ÖZET — sayılarla

| büyüklük | değer |
|---|---|
| İncelenen literatür dosyası | **20** *(5 271 satır)* |
| **§2'de yargı taşıyan satır** | **68** |
| 🟢 UYUYOR | **47** |
| 🔴 ÇELİŞİYOR | **3** *(3B alan · bit hızı · paket boyutu)* |
| 🟡 EKSİK | **14** |
| ⚪ KARŞILAŞTIRILAMAZ | **3** |
| 🔴🟢 KARIŞIK *(ham çelişiyor, normalize uyuyor)* | **1** *(gönderim hızı — §2.4)* |
| Yeni ölçüm betiği | **2** *(`sjr_donusumu` · `literatur_eksenleri`)* |
| Bu oturumda koşulan tam koşu | **300** *(4,3 dk · korunum 300/300)* |
| SJR dönüşümü için bağ örneklemi | **8 864** *(S2, 30 tohum)* |
| Yeni bulgu | **4** *(F-1 adlandırma · F-2 iç çelişki · F-3 SJR ekseni · F-4 ölü üretici)* |

**Üretici** *(depo kökünden — yargılar §2'nin tablolarındaki SON hücreden
sayılır)*:

```bash
PYTHONIOENCODING=utf-8 python -c "import pathlib,collections; t=pathlib.Path('v2/10-LITERATUR-KOD-KARSILASTIRMA.md').read_text(encoding='utf-8'); g=t.split('# 2 · KARŞILAŞTIRMA TABLOSU')[1].split('# 3 ·')[0]; c=collections.Counter(); r=[[x.strip() for x in s.strip('|').split('|')] for s in g.splitlines() if s.rstrip().startswith('|') and s.rstrip().endswith('|')]; r=[h for h in r if len(h)>=4 and not set(h[0].replace(' ',''))<=set('-:') and h[-1]!='yargı']; [c.update([('KARIŞIK' if sum(y in h[-1] for y in '\U0001f7e2\U0001f534\U0001f7e1⚪')>1 else next(a for y,a in ((' \U0001f7e2','UYUYOR'),('\U0001f534','CELISIYOR'),('\U0001f7e1','EKSIK'),('⚪','KARSILASTIRILAMAZ')) if y.strip() in h[-1]))]) for h in r]; print(sum(c.values()), dict(c))"
```

Beklenen çıktı: `68 {'UYUYOR': 47, 'EKSIK': 14, 'CELISIYOR': 3, 'KARSILASTIRILAMAZ': 3, 'KARIŞIK': 1}`

> ⚠️ **BU SATIR BİR KEZ YANLIŞ YAZILDI VE DÜZELTİLDİ.** İlk hâli
> *"62 satır · 34 uyuyor · 4 çelişiyor · 20 eksik · 4 karşılaştırılamaz"*
> diyordu ve **hiçbiri ölçülmemişti** — `03` kural 1'in birebir ihlali,
> üstelik **kuralı alıntılayan bir belgede**. Sayılar ölçüldü, üretici
> komut yazıldı. ⚖️ Depoya göre bu, B-114/B-25 örüntüsünün aynısıdır:
> *"araç doğru, çıktısı elle yazılmış."*

## 9.1 🔴 EN ÖNEMLİ ALTI CÜMLE

1. **Aracın soyutlama seviyesi literatürün "en titiz" dediği yerdedir** ve
   chunk bazlı PER gibi ince ayrıntılar birebir uygulanmıştır *(§6.1)*.
2. **Normalize sunulan yükümüz literatür baseline'ıyla BİREBİR aynıdır**
   *(%8,192)* — üç ham parametre farkı tek satırda kapanıyor *(§2.4)*.
3. 🔴 **Boşluk A adlandırılmış protokoller istiyor; depoda yok ve ön-kayıt
   onları zaten dışlıyor** *(§5)*. K-077'nin görmediği kısıt; yol
   haritasının en büyük çatalı.
4. 🟢 **Kalibrasyonun 0,5252'si BİREBİR yeniden üretildi**, ve 30 tohumda
   çalışma noktası hedefe **daha da yakın** çıktı *(0,0176 → 0,0044)* —
   S2 = +2 dBm kararı güçlendi *(§7b.1)*.
5. 🔴 **`06` Bölüm 5 koşul 1 ilk kez ölçüldü ve KISMEN DÜŞTÜ:** kâhin kol
   koşu uzunluğundan bağımsız *(15/30)*, gözlem tabanlı kol **değil**
   *(8/30)*. **350 s korunmalı** *(§7b.3)*.
6. 🔴 **Hayatta-kalan yanlılığı kendi aracımızda ölçüldü:** S2'de teslim
   yarıya inerken **ortalama gecikme %3,4 DÜŞÜYOR**, ama **p95 %26,0
   ARTIYOR** *(§7b.4)*. Ortalama yalan söylüyor; yüzdelik söylemiyor —
   ve şema onu **zaten taşıyor**.

## 9.2 🔒 BU BELGENİN KAPSAMADIĞI

| kapsanmayan | neden önemli |
|---|---|
| **Somut iddia sayıları elle sayıldı** *(§1)* | Üretici komutu yok; `03` kural 1'in sınırında ve öyle işaretlendi |
| Ölçümler **iki aktarıcıyla** yapıldı | Aile 1'in protokolleri farklı davranabilir; §7b.3 bunu açıkça şart koşuyor |
| **Hiçbir literatür sayısı projeye alınmadı** | Bir makaledeki değer bizim ölçümümüz değildir *(K-077 §5)* |
| Ölçümler **ayarlama tohumlarında** *(1–30)* | Ana deney tohumları mühürden önce koşulmaz *(K-025)* |
| **Kapı koşulmadı** | `sim/` değişmedi; 165–330 dk bedelin karşılığı yok |
| 🔴 **Hiçbir refactoring uygulanmadı** | Fiyatlandırma `11`de, karar öğrencinin *(`03` kural 8)* |
