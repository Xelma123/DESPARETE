# 09 · Lİ vd. REPLİKASYONU — aletin TEK dış çapası

> **Durum: tamamlandı** — eski dünyada H1 tutmadı, H2 ve H3 tuttu; mekanizma üç α'da doğrulandı. **Referans dünyada sabit hızda H1 TUTTU** — 0,1270 (K-187), kâhin beacon'ı AODV HELLO'suna eşitlendikten sonra 0,1188 (K-219), MAC en çok 7 iletim denemesine çekildikten sonra 0,1250 (K-226) — üçü de bantta (belgenin sonu). Ön-kayıt (§03–§06) 8 Eylül'de ölçümden önce yazıldı ve değiştirilmez; özgün metin birebir `v2/arsiv/09-LI-REPLIKASYONU-2026-09-25.md`, bu öz sürüm ön-kaydın içeriğini değiştirmez. Bölüm numaraları kodda atıflı, korunur. Şartname `07` §10 seviye 3 · kaynak `02` A5b ✓.
> Üretici: `python -u kalibrasyon/li_replikasyonu.py` (~2 dk; son koşum **25 Eylül 2026**, çıktı `arsiv/teshis/belge_guncelleme_2026-09-25/li_replikasyonu_cikti.txt`) · iki çift probu `kalibrasyon/iki_cift.py` · α taraması `python -u kalibrasyon/yeniden_kullanim.py` (9 Eylül).
> Sayılar Y2 (veri onayı düzeltmesi, 11 Eylül, K-115) sonrası; 9–10 Eylül tablosu (H1 0,0861, 11 düğüm 0,0739) arşivde.

---

## 00 · Neden

Üç sınavın ikisi geçmişti — iç tutarlılık (korunum, mutabakat) ve analitik (Bianchi, sönümleme varyansı, yol kaybı). Üçüncüsü, **yayımlanmış bir sonucu yeniden üretmek**, yoktu; onsuz alet kendi içinde tutarlı ve tamamen yanlış olabilir. Bianchi tek çarpışma alanını sınar; bu projenin ölçtüğü şey **çok atlamalı** teslim (uzamsal yeniden kullanım, zincir boyu çarpışma).

## 01 · Replike edilen sonuç — Li, Blake, De Couto, Lee, Morris, *"Capacity of Ad Hoc Wireless Networks"* §3.2

| # | ne | değer |
|---|---|---|
| L1 | ideal MAC ile zincir kullanımı | 1/3 |
| L2 | ideal zincirin uçtan uca verimi / tek atlama | **1/4** |
| L3 | 802.11'in gerçekte verdiği | **1/7** |

Mekanizma: *i* iletirken *i±1* (alıcı/verici), *i±2* (taşıyıcı dinleme) ve *i±3* (alıcıyı bozar) susar → zincirin dörtte biri aynı anda konuşur (L2); 802.11'in geri çekilmesi, çarpışmaları ve onay yükü bunu 1/7'ye indirir. **L3/L2 ≈ 0,571 = 802.11'in kendi verimsizliği.**

## 02 · Kurulum

Zincir bir **ölçüm aletidir**, deney kolu değil: deney matrisine ve ön-kayda girmez, `kalibrasyon/` altında kendi dünyasını kurar. `Sabit` mobilite, tek eksende eşit aralık · sabit zincir yönlendiricisi · tek doygun akış `0 → N−1` · **kanal değişmez** (aynı yayılım, MAC, girişim — replikasyon deneydeki aleti sınamalı).

## 03 · Ölçümden önce bağlanan üç sayı

**03.1 · Aralık = `nominal_bag_m` (K-220'ye kadar `iletim_menzili_m`) = 280 m** (güç çapası; girişimsiz SINR tam eşikte → "bir atlama = bir iletim menzili" yapı gereği). İlk hâli "atlama PDR ≥ 0,99 olan en büyük aralık"tı; ilk ölçümden sonra 8 Eylül'de değişti çünkü gerekçesi yanlıştı — *i±2/i±3* girişimi artefakt değil Li'nin ölçtüğü mekanizmanın kendisi; aralığı büyütmek oranı yapay yükseltirdi. Eski ölçüt kapı olarak kaldı (her bağ ≥ 0,99).

**03.1b · Kapı bir kurulum kusurunu yakaladı.** 200 m'lik ilk denemede N ≥ 3'te teslim sıfırdı. Bağları öldüren sönümleme: statik kolda donmuş tek Rician çekimi, PER uçurumunda derin çekim bağı öldürür (ölü bağ %2–6; K-096'nın istenen özelliği). Li'nin kurulumunda gölgeleme/sönümleme yok → **replikasyon ikisi KAPALI koşar** (ön-kayıtlı kapının kendi işi, gevşetme değil). 280 m'de açık kanal: en kötü bağ 0,0000, ortalama 0,8800 · temiz kanal 1,0000 / 1,0000 (kapı geçer). Bedeli beyanlı: kanalın tamamını değil MAC + girişim + uzamsal yeniden kullanımı doğrular; gölgeleme ve sönümleme ayrıca doğrulandı (σ kaynaktan, K-096).

**03.2 · Zincir uzunluğu N = 1…10 atlama taranır** — tek nokta tesadüfen tutabilir; Li'nin iddiası bir şekil.

**03.3 · Doygunluk ölçülür:** sunulan yük, N = 1'de ölçülen tek atlama kapasitesinin 2 katı; kuyruk boş kalmamalı.

## 04 · Ön-kayıt (8 Eylül, değiştirilmez)

| # | hipotez | beklenen | başarısızlık |
|---|---|---|---|
| **H1** | uzun zincir verimi / tek atlama verimi | **1/7 ≈ 0,143**, band **[0,10; 0,20]** | band dışı |
| **H2** | eğrinin şekli | N arttıkça düşer, N ≳ 7'de düzleşir | monoton düşmüyor ya da düzleşmiyor |
| **H3** | ideal-MAC tavanı ile ilişki | ölçülen oran 1/4'ün **altında** | 1/4'ün üstü → uzamsal yeniden kullanım fazla iyimser |

Band ±%40: iki 802.11 uygulaması arasında beklenen ayrımın mertebesi; sonradan genişletilmez. Betikteki tanım: **uzun zincir = 8–11 düğümlü zincirlerin oranlarının ortalaması.**

**04.1 · Önceden ilan edilen model farkları** — sapma bandı aşarsa önce bunların büyüklüğü ölçülür; hiçbiri açıklamıyorsa kusur alettedir. "Herhalde X yüzündendir" açıklama değildir, X'i kapatıp ölçmek açıklamadır.

| fark | yönü |
|---|---|
| taşıyıcı dinleme menzili sert değil (Li "duyma ≈ 2 × iletim" varsayar; burada güç eşiği) | uzamsal yeniden kullanım farklı çıkabilir — iki yöne de |
| RTS/CTS yok · hız uyarlaması yok | aynı |
| gölgeleme ve sönümleme → KAPALI koşulur (§03.1b) | açık bırakmak zincirin beşte birini sıfırlıyordu |
| yayılma kazancı yok (Barker ~10 dB) | girişim güçlü → oran düşük tarafa |

## 05 · Neyi sınamaz

Yönlendirme (rota sabit) · karıştırma · mobilite. **Sınadığı tek şey:** MAC + girişim + uzamsal yeniden kullanımın birlikte davranışı — bütün çok atlamalı sonuçların altındaki katman.

## 06 · Çürütülürse

Şartname §10: *"Tutmazsa MAC ya da girişim modelinde bir şey yanlıştır ve **bulmadan devam edilmez**."* Mühürden önceki bir engeldir: Aşama 1'in bütün kalibrasyonu (çalışma noktası, ρ, evre metrikleri) çok atlamalı teslimin doğru modellendiğine dayanır.

---

## SONUÇ — H1 TUTMADI, H2 ve H3 TUTTU; mekanizma bulundu

Eğri (280 m · temiz kanal · 5 tohum · doygun · tek atlama 356,1 pkt/s · 25 Eylül):

| düğüm | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|
| verim (pkt/s) | 356,07 | 101,23 | 72,98 | 60,87 | 50,59 | 44,46 | 35,16 | 32,19 | 29,62 | 27,02 |
| tek atlamaya oran | 1,0000 | 0,2843 | 0,2050 | 0,1709 | 0,1421 | 0,1249 | 0,0987 | 0,0904 | 0,0832 | 0,0759 |

**H1 = 0,0871** (8–11 düğüm ortalaması) → ✗ band dışı · **H2** ✓ düşüyor ve düzleşiyor · **H3** ✓ 1/4'ün altında.

**Sebep arandı** — `oran × atlama ≈ 0,7` ve N ≥ 5'ten sonra sabit, yani verim atlamayla ters orantılı gibi. İki hipotez çürüdü:
- *Taşıyıcı dinleme çok geniş* (duyma/iletim = 6,31; Li ~2): duyma menzili tarandı — 1,0 → 0,0277 · 1,5 → 0,0277 · 2,0 → 0,0664 · 3,0 → 0,0858 · 4,5 → 0,0816 · 6,31 → 0,0759. Daraltmak kötüleştiriyor (gizli terminal); hiçbir değer banda girmiyor.
- *280 m'de bağ marjı sıfır*: aralık 100 → 280 m tarandı, oran 0,074–0,081, `oran × atlama` ≈ 0,74–0,81 her aralıkta (9 Eylül).

**Mekanizma doğrudan ölçüldü** (iki çift probu, 9 Eylül):
- Uzamsal yeniden kullanım **var**: birbirinden uzak 1 · 2 · 4 bağımsız çift → toplam verim 356,1 · 711,9 · 1 423,9 (K × tek, birebir). Alet serileştirmiyor.
- Yeniden kullanım **mesafesi**: iki çift arası 2–6 atlamada oran 1,05–1,07, **8 atlamada 2,00**. Li'nin modelinde 4.
- Türetme: girişim menzili / iletim menzili `= 10^(SINR_eşiği / (10·α)) = 10^(16/20) = 6,31` (α = 2,0; ölçülen birebir). Li: yeniden kullanım 4 atlama → ideal 1/4 → 802.11 çarpanı 0,571. Bizde 8 atlama → **0,571 / 8 = 0,0714**; ölçülen 11 düğüm **0,0759**, uyum **%6** (Y2 öncesi 0,0739, %4).

**α taraması — öngörü sınandı** (`yeniden_kullanim.py`, 9 Eylül; 2,00 = tam paralel, 1,00 = tam serileşmiş):

| α | girişim/iletim | ölçülen mesafe | mesafe / oran |
|---|---|---|---|
| 2,0 | 6,31 | 8 atlama | 1,268 |
| 3,0 | 3,41 | 4 atlama | 1,171 |
| 4,0 | 2,51 | 3 atlama | 1,194 |

`yeniden kullanım mesafesi ≈ 1,21 × 10^(SINR_eşiği / (10·α))` — çarpan 2,5 katlık oran aralığında %8 saçılmayla sabit (1'den büyük çünkü PER eğrisi sert basamak değil). Kayda geçmiş öngörü (K-108: α = 3 → ~4–5, α = 4 → ~3–4 atlama) tuttu. Betikteki ilk kapı "oran + 1 atlama" diyordu ve α = 2'de tesadüfen tutuyordu; üç α'da toplamsal değil **orantısal** ilişki çıktı — düzeltilen kapıydı, öngörü değil.

**Karar — sayı tutmadı, mekanizma tuttu.** Fark tek parametreden: yol kaybı üsteli α.

| | Li (yer tabanlı, ns-2) | bu proje |
|---|---|---|
| α | ~4 (iki-ışın) | **2,0** (hava-hava serbest uzay, `07` §4) |
| girişim/iletim | 2,5 | 6,31 |
| yeniden kullanım | ~4 atlama | 8 atlama |
| zincir oranı | 1/7 = 0,143 | ~0,076 |

α = 2,0 gerekçeli bir tasarım kararıdır (iki-ışın kırılma mesafesi bağ mesafesinin çok üstünde) ve §04.1'deki "taşıyıcı dinleme sert değil" farkının nicel hâlidir. Alet Li'nin fiziğini farklı bir yayılım rejiminde yeniden üretiyor; MAC + girişim + uzamsal yeniden kullanım katmanı **doğrulanmıştır**.

- Çok atlamalı sonuçlar bu projede Li'ninkinden **kötü** olacak — sebebi bilinen fizik (girişim iletimin 6,3 katı uzağa gider); sonuç bölümünde beyan edilir.
- Ön-kayıtlı band genişletilmedi; **H1 "tutmadı" yazıyor ve öyle kalır.** Doğrulanan sayı değil, sayının nereden geldiğidir.

---

## REFERANS DÜNYADA (27 Eylül 2026, K-187) — sabit hızda H1 TUTTU

Aynı ön-kayıt, aynı zincir aleti, referans dünyanın (`14`, K-181) bütün anahtarları açık. Üretici: `python -u kalibrasyon/li_replikasyonu.py --dunya referans_2026` · ayrıştırma `python arsiv/teshis/faz4_2026-09-26/b_li_ayristirma.py` (5 kol × 2 zincir × 5 tohum; çıktı `…/b_li_ayristirma.txt`).

| kol | tek atlama (pkt/s) | 11 düğüm (pkt/s) | H1 |
|---|---|---|---|
| referans, bütün anahtarlar | 832,8 | 33,88 | 0,0407 ✗ |
| **ARF kapalı — sabit 2 Mb/s (Li'nin kurulumu)** | 354,6 | 45,04 | **0,1270 ✓ bantta** |
| güç kipi taşıyıcı dinleme kapalı | 832,8 | 21,39 | 0,0257 |
| yayılım gecikmesi kapalı | 840,9 | 34,22 | 0,0407 |
| ARF ve güç kipi kapalı | 354,6 | 32,69 | 0,0922 |

- **K-226 (10 Ekim):** MAC en çok 7 iletim denemesiyle (K-223) sabit hızda **0,1250 ✓ bantta**, ARF açık 0,0415 ✗; aracın kendi H1'i ≈ 0,042 (`arsiv/teshis/denetim_duzeltme_2026-10-09/D2_li.txt`, `D3_li_sabit_hiz.txt`).
- **K-219 (8 Ekim):** beacon 32 → 84 B'tan sonra (K-215) sabit hızda **0,1188 ✓ bantta**, ARF açık 0,0409 ✗; 32 B'la 0,1270 birebir geri geldi (`arsiv/teshis/faz4_5_2026-10-08/li_beacon.py`) — fark beacon'ın havadaki süresi.
- Li'nin koşulunda (sabit hız) oran bandın içinde: işlem kazancı ve güce dayalı taşıyıcı dinleme girişim/iletim oranını düşürdü (`14` §9 öngörü 1 ✓). Aletin tek dış çapası ilk kez **sayıyla** geçti.
- Bütün anahtarlar açıkken H1'i bozan **ARF**: çok atlamalı çekişmede çarpışmayı kanal hatası sanıp hızı düşürüyor (literatürde bilinen ARF zaafı; ns-3 ARF'nin kendisi, `02` G14). Referans dünyada ARF açık kalır — gerçek telsiz böyle davranır ve bütün protokollere aynı MAC'le eşit etki eder.
