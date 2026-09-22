# SJR'ye Bağlı PDR ve E2E Gecikme Düşüşleri — 2022–2026 FANET Literatür İncelemesi

> **Soru:** 2022–2026 FANET literatüründe, değişen Sinyal-Karıştırma Oranları (SJR) altında
> OLSR, AODV ve GPSR için deneysel/simüle edilmiş PDR ve E2E gecikme düşüş yüzdeleri.

## Doğrudan yanıt

**2022–2026 FANET literatüründe OLSR, AODV ve GPSR için değişen SJR altında doğrudan
raporlanmış PDR ve E2E gecikme düşüş yüzdeleri bulunamamıştır.** Bu, bir eksik arama değil,
doğrulanmış bir literatür boşluğudur — tıpkı projenin `01-PROBLEM-VE-AMAC.md` §2.1'inde
"~~AODV/OLSR/BATMAN karıştırma altında <%50 PDR~~ | 🔴 Birincil kaynak YOK | ❌ İDDİA
EDİLMEZ" olarak işaretlendiği gibi. Bu boşluk, TÜBİTAK projesinin ölçmeyi hedeflediği şeydir.

Bu doğrulama, hedefli bir arama (4 sorgu, 28 sonuç) ve bir ön-baskının tam metin fetch'i ile
yapılmıştır. Hiçbir kaynak, üç protokolü birden SJR taramasıyla PDR/E2E olarak karşılaştırmamaktadır.

---

## Kanıt matrisi

| # | Aranan veri | Bulgu | Yakın kaynak | Neden kullanılamaz |
|---|---|---|---|---|
| 1 | OLSR + RF jamming + SJR taraması + PDR/E2E + FANET + 2022–2026 | **Yok** | [Sarı & Seçinti 2024](https://research.itu.edu.tr/en/publications/using-centrality-based-topology-control-for-fanet-survivability-a/) | FANET + jamming + OLSR-ilişkili, ama CentAir'in çok-kanallı OLSR'a göre *iyileştirmesini* raporlar (PDR +%11,5; gecikme −%21,1); ham OLSR'nin SJR'ye bağlı PDR/E2E düşüşlerini vermez |
| 2 | AODV + RF jamming + SJR taraması + PDR/E2E + FANET + 2022–2026 | **Yok** | [Ceviz, Sadioglu & Sen 2022](https://web.cs.hacettepe.edu.tr/~ssen/files/papers/AdhocNets22.pdf) | FANET + AODV + PDR, ama **yönlendirme saldırıları** (blackhole/sinkhole), RF jamming değil; SJR yok; yalnız AODV (temel PDR %91,43 → %20 sinkhole %56,60 → %20 blackhole %56,81) |
| 3 | GPSR + RF jamming + SJR taraması + PDR/E2E + FANET + 2022–2026 | **Yok** | [Ünal 2026 (METU)](https://open.metu.edu.tr/bitstream/handle/11511/118337/Impact-of-Mobility-on-GPSR-and-AODV-Routing-Performance-in-FANETs.pdf) | FANET + GPSR + AODV + PDR/E2E, ama **jamming yok**; yalnız mobilite modelleri |
| 4 | OLSR+AODV+GRP + jamming + PDR/E2E (herhangi SJR) | **Sayısal veri yok** | [Gupta 2024 (Research Square ön-baskı)](https://www.researchsquare.com/article/rs-5393869/v1) | WSN (FANET değil), ön-baskı (hakemlik dışı), AODV/OLSR/GRP'yi jamming altında değerlendirir ama **hiç sayısal PDR/E2E değeri ve SJR değeri raporlamaz**; yalnız "protokol seçimi dayanıklılığı etkiler" nitel bulgusu |
| 5 | AODV+GPSR + mobil jammer + teslim oranı | **SJR yok, tarih dışı** | [Won, Youn & Ali 2006](https://dl.ifip.org/db/conf/euc/eucw2006/WonYA06.pdf) | WSN (FANET değil), 2006 (2022–2026 dışı), 12 m yarıçaplı mobil jammer, teslim %10'a düşer, GPSR AODV'den hızlı bozulur — ama SJR/J/S değeri yok; jammer hızı/mesafesi tek değişken |
| 6 | SJR/SINR değerleri (2022–2026) | **Protokol karşılaştırması yok** | [Gao & Zhi 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12504448/): SJR −5/−13/−14 dB; [Aich 2025](https://www.mdpi.com/1999-5903/17/10/474): JSR [−40,+40] dB; [Huang 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC12953576/): SINR eşiği −3 dB | SJR/JSR değerleri raporlanır ama bunlar DSSS/FH oyun teorisi, OFDM tespiti veya jammer lokalizasyonu çalışmalarıdır — OLSR/AODV/GPSR yönlendirme protokollerini değerlendirmezler |

---

## "Raporlanmış" ile "türetilebilir" ayrımı

İstenen değerler (ör. "OLSR için SJR=−5 dB'de PDR %X, E2E %Y düşüş") **literatürden alınamaz**;
yalnızca yeni bir simülasyonla üretilebilir. Aşağıdaki şema, projenin üretmeyi hedeflediği
çıktının boş hücreli örneğidir — değerler uydurulmamıştır, kasıtlı olarak `Raporlanmadı` bırakılmıştır:

| Protokol | SJR (dB) | PDR düşüşü | E2E gecikme artışı | Kaynak |
|---|---|---|---|---|
| OLSR | −5 | Raporlanmadı | Raporlanmadı | — |
| OLSR | −13 | Raporlanmadı | Raporlanmadı | — |
| AODV | −5 | Raporlanmadı | Raporlanmadı | — |
| AODV | −13 | Raporlanmadı | Raporlanmadı | — |
| GPSR | −5 | Raporlanmadı | Raporlanmadı | — |
| GPSR | −13 | Raporlanmadı | Raporlanmadı | — |

> SJR eşiği referansı: haberleşme kesintisi için \(T_s = -3\) dB
> ([ar5iv 2104.04477](https://ar5iv.labs.arxiv.org/html/2104.04477)); SJR tarama aralığı
> literatürde bağımsız değişken olarak −40…+40 dB kullanılır ([Aich 2025](https://www.mdpi.com/1999-5903/17/10/474)).

---

## Kısmi kanıtlar (dikkatle, sınırlarıyla)

Aşağıdaki sayılar gerçekten bildirilmiştir, ancak **hiçbiri** "FANET + 2022–2026 + OLSR/AODV/GPSR
+ SJR" koşullarını aynı anda sağlamaz; bu nedenle kullanıcıya istenen tablonun hücreleri olarak
sunulamazlar:

- **Won vd. 2006** (WSN, NS-2, AODV+GPSR, mobil jammer): teslim başarı oranı %10'a kadar düşer;
  GPSR, AODV'den daha hızlı bozulur; mobil jammer altında gecikme artışı %55'e kadar
  ([Won vd.](https://dl.ifip.org/db/conf/euc/eucw2006/WonYA06.pdf)). — 2006, WSN, SJR yok.
- **Sarı & Seçinti 2024** (FANET, aldatıcı jammer, CentAir vs çok-kanallı OLSR): PDR +%11,5;
  verim +%18,1; gecikme −%21,1; enerji verimliliği +%17,8
  ([Sarı & Seçinti](https://research.itu.edu.tr/en/publications/using-centrality-based-topology-control-for-fanet-survivability-a/)). —
  anti-jamming sisteminin kazanımları; ham OLSR'nin SJR'ye bağlı bozunumu değil.
- **Bout & Loscrì 2022** (ns-3 + gerçek 802.11, jammer): sürekli jammer PDR %100→%0;
  reaktif jammer PDR %60–70 (sim) / %50–60 (gerçek)
  ([Bout & Loscrì](https://hal.science/hal-03765858/file/WSNIMhal.pdf)). — protokol
  ayrımı yok, FANET değil, SJR değil (jammer tipi).
- **Ceviz vd. 2022** (FANET, ns-3, AODV): temel PDR %91,43; %20 sinkhole→%56,60;
  %20 blackhole→%56,81
  ([Ceviz vd.](https://web.cs.hacettepe.edu.tr/~ssen/files/papers/AdhocNets22.pdf)). —
  RF jamming değil (yönlendirme saldırısı), SJR yok, yalnız AODV.

---

## Proje çıkarımı

Bu bir eksik arama değil, bir **literatür boşluğu** ve geçerli bir araştırma katkısıdır. Proje
şunu iddia edebilir:

> 2022–2026 literatüründe, OLSR, AODV ve GPSR için SJR'ye bağlı PDR ve E2E gecikme bozunumuna
> ilişkin doğrudan karşılaştırmalı FANET verisi bulunmadığından, bu çalışma bu tabloyu
> adlandırılmış karıştırıcı sınıfları ve nicel SJR düzeyleri altında üretmeyi hedefler.

Bu, projenin `01-PROBLEM-VE-AMAC.md` §2.1'deki ⭐ işaretli "varlık gerekçesi" ile tutarlıdır:
literatürde bu protokollerin karıştırma altındaki karşılaştırmalı davranışı için doğrudan birincil
kaynak bulunamamıştır; kontrollü bir ortamda bunu ölçmek başlı başına bir katkıdır.

---

## Kaynakça (APA 7)

Aich, N., Oubrahim, Z., Ait Talount, H., & Abbou, A. (2025). Bi-scale Mahalanobis detection for reactive jamming in UAV OFDM links. *Future Internet, 17*(10), 474. https://www.mdpi.com/1999-5903/17/10/474

Bout, E., & Loscrì, V. (2022). An adaptable module for designing jamming attacks in WiFi networks for ns-3. In *Proceedings of the 25th International ACM Conference on Modeling, Analysis and Simulation of Wireless and Mobile Systems (MSWiM '22)*. https://hal.science/hal-03765858/file/WSNIMhal.pdf

Ceviz, O., Sadioglu, P., & Sen, S. (2022). Analysis of routing attacks in FANETs. In *Proceedings of AdHocNets 2022*. https://web.cs.hacettepe.edu.tr/~ssen/files/papers/AdhocNets22.pdf

Gao, P., & Zhi, Y. (2025). A dynamic confrontational game model of UAV's data link in the complicated electromagnetic environment. *Scientific Reports, 15*, 34927. https://pmc.ncbi.nlm.nih.gov/articles/PMC12504448/

Gupta, V. R. S. R. G. (2024). *Evaluating the impact of jamming on routing protocols in wireless sensor networks: A QoS perspective* (Preprint rs-5393869/v1). Research Square. https://www.researchsquare.com/article/rs-5393869/v1

Huang, L., Xiong, L., Huang, S., Wang, J., & Wan, C. (2026). Iterative localization method for multiple jammers in UAV collaborative jamming attacks. *Scientific Reports, 16*, 7927. https://pmc.ncbi.nlm.nih.gov/articles/PMC12953576/

Sarı, T. T., & Seçinti, G. (2024). Using centrality based topology control for FANET survivability against jamming. *Computer Networks, 242*, Article 110250. https://research.itu.edu.tr/en/publications/using-centrality-based-topology-control-for-fanet-survivability-a/

Ünal, S. D. (2026). *Impact of mobility on GPSR and AODV routing performance in FANETs* (Technical Report METU/II-TR-2026). Middle East Technical University, Informatics Institute. https://open.metu.edu.tr/bitstream/handle/11511/118337/Impact-of-Mobility-on-GPSR-and-AODV-Routing-Performance-in-FANETs.pdf

Wang, X., Gursoy, M. C., Erpek, T., & Sagduyu, Y. E. (2021). *Jamming-resilient path planning for multiple UAVs via deep reinforcement learning*. IEEE International Conference on Communications (ICC 2021). https://ar5iv.labs.arxiv.org/html/2104.04477

Won, C., Youn, J.-H., & Ali, H. (2006). Impact of high-mobility radio jamming in large scale wireless sensor networks. In *IFIP EUC Workshops Proceedings*. https://dl.ifip.org/db/conf/euc/eucw2006/WonYA06.pdf

> **Şeffaflık notu:** Gupta (2024) ön-baskısı (hakemlik dışı) ve kaynak sayfalarında basılı olmadığı
> için tam künyesi doğrulanamayan alanlar atıf öncesi kontrol gerektirir.
