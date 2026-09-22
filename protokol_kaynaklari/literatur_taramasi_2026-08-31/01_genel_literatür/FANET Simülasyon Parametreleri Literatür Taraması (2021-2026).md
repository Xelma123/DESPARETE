# FANET Yönlendirme Protokolleri — Standart Simülasyon Parametreleri (2021–2026)

**Amaç:** TÜBİTAK elektronik harp / taktik İHA mesh ağ simülasyonu projesi için literatür taraması.
**Yöntem:** 13 hakemli makale (tümü Scopus/WoS dizinli) taranmış; her parametre değeri makalenin **tam metni fetch edilerek** doğrulanmıştır. Snippet'ten değer alınmamıştır; makalede geçmeyen değerler "Belirtilmemiş" olarak işaretlenmiştir (simülatör varsayılanından tahmin yapılmamıştır).
**Kapsam:** 2021 (1), 2022 (1), 2023 (3), 2024 (3), 2025 (3), 2026 (1) — MDPI Sensors/Sustainability, Springer Nature Scientific Reports, Springer Multimedia Tools and Applications, Frontiers in Neurorobotics.

---

## A. Ana Tablo — Makale Bazlı Simülasyon Parametreleri

| # | Kaynak | Yıl | Yayınevi / Dergi | Yönlendirme protokolleri | Simülatör | Alan boyutu | İHA sayısı | İHA hızı (m/s) | 3D mobilite modeli | Paket boyutu + trafik | Taşıma katmanı |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [Wei vd. (2021)](https://doi.org/10.3389/fnbot.2021.697624) | 2021 | Frontiers, *Neurorobotics* | GAR, AODV, DSR | NS-3 (sürüm belirtilmemiş) | 2500 × 2500 m (2D) | 10×10 ızgara (toplam sayı açık değil) | Belirtilmemiş | Random Waypoint (2D/3D belirtilmemiş) | Belirtilmemiş | Belirtilmemiş |
| 2 | [Mansour vd. (2022)](https://doi.org/10.3390/su14158980) | 2022 | MDPI, *Sustainability* | CLEA-AODV, AODV, SOC-GSO, EENFC-MRP | NS-2.34 | 1300 × 1300 m² | 30–180 (30 adımlı) | Belirtilmemiş | "accidental waypoint" (2D/3D belirtilmemiş) | 1024 bayt, CBR | Belirtilmemiş |
| 3 | [Lansky vd. (2023)](https://doi.org/10.1038/s41598-023-27567-7) | 2023 | Springer, *Scientific Reports* | Firefly-tabanlı, G-OLSR, OLSR | NS-3 | 500 × 1500 × 1500 m³ (3D) | 10–50 | 25 (sabit) | Random Waypoint (3D) | Belirtilmemiş (3 Mbps, 0,2 sn aralık) | Belirtilmemiş |
| 4 | [Wang vd. (2023)](https://doi.org/10.3390/s23177550) | 2023 | MDPI, *Sensors* | AO-AOMDV, AOMDV, AODV | NS-3 | 2000 × 2000 × 300 m (Z: 100–300 m) (3D) | 20–100 | 10–40 | 3D Gauss-Markov | Belirtilmemiş (CBR 1 Mbps) | UDP |
| 5 | [Zhang vd. (2023)](https://doi.org/10.1007/s11042-023-15932-7) | 2023 | Springer, *Multimedia Tools and Applications* | HTLR, GPSR_3D, SP_GMRF, GGFGD, 3DPBARP, N-HTLR | NS-3 | 1000 × 1000 × 1000 m³ (3D) | 50–150 (varsayılan 100) | Ort. 25 (10–40) | 3D Random Waypoint | 2048 bayt (320 kbps, 20 pkt/s) | Belirtilmemiş |
| 6 | [Rozario vd. (2024)](https://doi.org/10.3390/s24196334) | 2024 | MDPI, *Sensors* | CR-UAV, MDRMA, MA-DP-AODV, MDA-AODV, SecRIP, OLSR+GPSR | "Network Simulators" (isim/sürüm net değil) | 800 × 800 m (2D) | 100–200 | Belirtilmemiş | Belirtilmemiş | 512 bayt (ek: 1024), CBR 2 Mbps | Belirtilmemiş |
| 7 | [Hosseinzadeh vd. (2024)](https://doi.org/10.1038/s41598-024-68471-y) | 2024 | Springer, *Scientific Reports* | LFEAR, EARVRT, LoCaL, O-LAR | NS-2 | 10000 × 10000 × 10000 m³ (3D) | 5–30 | 10–110 (yoğunluk senaryosunda 60) | Random Waypoint (2D/3D etiketi belirtilmemiş) | 512 bayt, CBR 2 Mbps | Belirtilmemiş |
| 8 | [Yang vd. (2024)](https://doi.org/10.1038/s41598-024-64454-1) | 2024 | Springer, *Scientific Reports* | ICRP, AODV, fuzzy-AODV, Enhanced-Ant-AODV | OMNeT++ | 1500 × 1500 m² (2D) | 40–140 (20 adımlı) | 20–60 | Gauss-Markov (2D/3D belirtilmemiş) | 125 bayt, CBR 100 kbps | Belirtilmemiş |
| 9 | [Agrawal & Arafat (2025)](https://doi.org/10.3390/s25010072) | 2025 | MDPI, *Sensors* | HMAO, MFO, MWCRSF, DCFH, DCM, HMGOC | NS-3.35 | 2000 × 2000 × 500 m (3D) | 20–100 | 10–30 | 3D Gauss-Markov | 512 bayt, CBR 2 Mbps | Belirtilmemiş |
| 10 | [Dong vd. (2025)](https://doi.org/10.3390/s25020500) | 2025 | MDPI, *Sensors* | AODV-EM, AODV, OLSR, DSDV | NS-3.28 | 1000 × 1000 m (2D) | 50–140 | 5–50 | Random Waypoint (2D) | 512 bit, CBR | UDP |
| 11 | [Mary & Pradeep Kumar (2025)](https://doi.org/10.1038/s41598-025-30429-z) † | 2025 | Springer, *Scientific Reports* | Enerji-mesafe sezgiseli, DQN, PPO (MADRL) | NS-3.40 + ns3-gym | 3D sınır kutusu (10,10,10)–(100,100,90–100); irtifa 50–120 m | 5–15 (eğitim 5–50) | 5–20 (ort. 10) | Modified 3D Gauss-Markov | 100/200/300 bayt (karışık trafik) | TCP (tablo); metinde TCP/UDP/PING |
| 12 | [Sun vd. (2025)](https://doi.org/10.3390/s25051417) | 2025 | MDPI, *Sensors* | DSDV, 3D-GPSR, SDN-FANET, SDN-FANET (A-EKF) | OPNET 14.5 (+ MATLAB R2023b) | 5000 × 5000 × 2000 m (3D) | 30 | ~20 (40 m/s'te PDR > %75) | Random Waypoint (3D alan) | 1024 bit (5 pkt/s) | Belirtilmemiş |
| 13 | [Alwasel vd. (2026)](https://doi.org/10.3390/s26113352) | 2026 | MDPI, *Sensors* | WAY-CR, TMFCS, TDLS, SSACEER, SSAFANET, ICW, EESCRA, CSBWOA, AAFSA | MATLAB 2016b | 2000 × 2000 × 500 m (3D) | 50–150 | 10–30 | SmoothRW3D (3D smooth random walk) | 8192 bit (1 Mbps) | Belirtilmemiş |

> Not: "Belirtilmemiş" = makalede açıkça verilmemiş; simülatör varsayılanından tahmin edilmemiştir. Bazı makaleler paket boyutunu bit cinsinden verir (512 bit, 1024 bit, 8192 bit) — bunlar bayt cinsine çevrilmeden aynen aktarılmıştır.
> † Mary & Pradeep Kumar (2025): klasik yönlendirme protokolü değerlendirmesinden ziyade enerji/MADRL (DQN, PPO) karşılaştırması yapan sınırda/yardımcı kaynak olarak tutulmuştur; standart simülasyon parametreleri (3D Gauss-Markov, paket boyutu, taşıma katmanı) açısından dahil edilmiştir.

---

## B. Literatürdeki Yaygın (Standart) Aralıklar

| Parametre | Literatürdeki baskın değerler | Sık kullanılan aralık |
|---|---|---|
| Simülatör | NS-3 baskın (7/13; sürümler 3.28 / 3.35 / 3.40) | NS-3; alternatifler NS-2, OMNeT++, MATLAB, OPNET |
| Simülasyon alanı (3D) | 2000 × 2000 × 500 m (en yaygın kalıp) | 2D: 800×800 – 2500×2500 m; 3D: 1000³ – 2000×2000×300 m; uç: 10 km³ |
| İrtifa bandı | 100–500 m (taktik alçak irtifa 50–120 m) | 50–500 m |
| İHA sayısı | 20–100 veya 50–150 (ölçeklenebilirlik taraması) | 5–150; küçük filo 5–30 |
| İHA hızı | 10–30 m/s (tek değer kullanıldığında 25 m/s) | yüksek dinamik: 20–60 m/s; uç: 10–110 m/s |
| Mobilite modeli | Random Waypoint (6 makale) ve 3D Gauss-Markov (4 makale) | RWP, Gauss-Markov (3D); yeni varyant: SmoothRW3D |
| Paket boyutu | 512 bayt CBR en yaygın | 100–300 bayt (telemetri) / 512 / 1024 / 2048 bayt |
| CBR veri hızı | 1–2 Mbps | 100 kbps – 3 Mbps |
| Taşıma katmanı | Çoğunlukla belirtilmiyor (10/13) | açıkça belirtenlerde UDP (2), TCP (1) |
| MAC / PHY | IEEE 802.11 a/b/g/n evrensel | menzil 200–550 m |
| Simülasyon süresi | ~200 s (medyan) | 100–600 s |
| Taban protokoller | AODV evrensel taban çizgisi (7 makale) | AODV, OLSR, DSDV, DSR, GPSR_3D |

### Kritik gözlemler
- **En eksik raporlanan parametre taşıma katmanıdır:** 13 makalenin yalnızca 3'ü açıkça belirtir (UDP×2, TCP×1). Kalan 10 makale hiç belirtmez — bu, FANET literatüründeki sistematik bir raporlama boşluğudur.
- İkinci sırada eksik parametreler: İHA hızı (3 makale) ve mobilite modelinin 2D/3D niteliği (6 makale).
- 2024 sonrası eğilim: klasik protokoller (AODV/OLSR) yerine ML/RL (DQN, PPO) ve metaheuristik (ACO, firefly, MFO) tabanlı yönlendirme karşılaştırmaları.

### TÜBİTAK projesi için önerilen taban yapılandırma (literatür medyanı)
NS-3 (≥3.35) · 2000 × 2000 × 500 m 3D alan · 20–100 İHA (20 adımlı tarama) · 10–30 m/s hız (elektronik harp için 40–60 m/s ek tarama) · 3D Gauss-Markov mobilite · 512 bayt CBR @ 2 Mbps · UDP taşıma · IEEE 802.11 PHY/MAC · 200–300 s süre · senaryo başına ≥10 tekrar.

---

## C. Kaynakça (APA 7)

1. Agrawal, J., & Arafat, M. Y. (2025). Bio-inspired algorithms for efficient clustering and routing in flying ad hoc networks. *Sensors, 25*(1), 72. https://doi.org/10.3390/s25010072 (Tam metin: https://pmc.ncbi.nlm.nih.gov/articles/PMC11722752/)

2. Alwasel, B., Salim, A., Veetil, P. R. P., Khedr, A. M., & Osamy, W. (2026). A reliable and secure cluster-routing framework for drone-assisted disaster management in smart cities. *Sensors, 26*(11), 3352. https://doi.org/10.3390/s26113352 (Tam metin: https://www.mdpi.com/1424-8220/26/11/3352)

3. Dong, H., Yu, B., & Wu, W. (2025). Routing protocol for intelligent unmanned cluster network based on node energy consumption and mobility optimization. *Sensors, 25*(2), 500. https://doi.org/10.3390/s25020500 (Tam metin: https://pmc.ncbi.nlm.nih.gov/articles/PMC11769274/)

4. Hosseinzadeh, M., Husari, F. M., Yousefpoor, M. S., Lansky, J., & Min, H. (2024). A local filtering-based energy-aware routing scheme in flying ad hoc networks. *Scientific Reports, 14*, 17733. https://doi.org/10.1038/s41598-024-68471-y (Tam metin: https://pmc.ncbi.nlm.nih.gov/articles/PMC11291667/)

5. Lansky, J., Rahmani, A. M., Malik, M. H., Yousefpoor, E., Yousefpoor, M. S., Khan, M. U., & Hosseinzadeh, M. (2023). An energy-aware routing method using firefly algorithm for flying ad hoc networks. *Scientific Reports, 13*, 1323. https://doi.org/10.1038/s41598-023-27567-7 (Tam metin: https://pmc.ncbi.nlm.nih.gov/articles/PMC9873979/)

6. Mansour, H. S., Mutar, M. H., Aziz, I. A., Mostafa, S. A., Mahdin, H., Abbas, A. H., Hassan, M. H., Abdulsattar, N. F., & Jubair, M. A. (2022). Cross-layer and energy-aware AODV routing protocol for flying ad-hoc networks. *Sustainability, 14*(15), 8980. https://doi.org/10.3390/su14158980 (Tam metin: https://www.mdpi.com/2071-1050/14/15/8980)

7. Mary, A. S., & Pradeep Kumar, T. S. (2025). Modeling and simulation of dual-battery FANET system using MADRL for energy optimization. *Scientific Reports, 16*, 821. https://doi.org/10.1038/s41598-025-30429-z (Tam metin: https://pmc.ncbi.nlm.nih.gov/articles/PMC12779634/)

8. Rozario, A., Ahmed, E., & Mansoor, N. (2024). A robust routing protocol in cognitive unmanned aerial vehicular networks. *Sensors, 24*(19), 6334. https://doi.org/10.3390/s24196334 (Tam metin: https://www.mdpi.com/1424-8220/24/19/6334)

9. Sun, K., Liu, M., Yin, C., & Wang, Q. (2025). Adaptive extended Kalman prediction-based SDN-FANET segmented hybrid routing scheme. *Sensors, 25*(5), 1417. https://doi.org/10.3390/s25051417 (Tam metin: https://www.mdpi.com/1424-8220/25/5/1417)

10. Wang, H., Li, Y., Zhang, Y., Huang, T., & Jiang, Y. (2023). Arithmetic optimization AOMDV routing protocol for FANETs. *Sensors, 23*(17), 7550. https://doi.org/10.3390/s23177550 (Tam metin: https://www.mdpi.com/1424-8220/23/17/7550)

11. Wei, X., Yang, H., & Huang, W. (2021). A genetic-algorithm-based optimization routing for FANETs. *Frontiers in Neurorobotics, 15*, 697624. https://doi.org/10.3389/fnbot.2021.697624 (Tam metin: https://www.frontiersin.org/journals/neurorobotics/articles/10.3389/fnbot.2021.697624/full)

12. Yang, S., Wang, S., Li, T., Hu, T., Xu, Z., He, R., & Zhang, B. (2024). Hybrid ant colony-based inter-cluster routing protocol for FANET. *Scientific Reports, 14*, 15632. https://doi.org/10.1038/s41598-024-64454-1 (Tam metin: https://pmc.ncbi.nlm.nih.gov/articles/PMC11228038/)

13. Zhang, H., Lv, X., Liu, Y., & Zou, X. (2023). Hedge transfer learning routing for dynamic searching and reconnoitering applications in 3D multimedia FANETs. *Multimedia Tools and Applications*, 1–35. Advance online publication. https://doi.org/10.1007/s11042-023-15932-7 (Tam metin: https://pmc.ncbi.nlm.nih.gov/articles/PMC10250183/)

---

**Dizin geçerliliği:** MDPI *Sensors*/*Sustainability*, Springer Nature *Scientific Reports*, Springer *Multimedia Tools and Applications* ve *Frontiers in Neurorobotics* dergilerinin tümü Scopus ve Web of Science dizinlidir.
**Atıf notları:** Makale numarası kullanan dergilerde (MDPI, Scientific Reports) APA 7 uyarınca sayfa yerine makale numarası verilmiştir. Çevrimiçi ilk yayın (advance online publication) olarak çıkan makalelerde cilt/sayı yerine "1–35. Advance online publication" biçimi kullanılmıştır.
**Dışlanan adaylar:** Tam metni erişilemeyen (Access Denied / yalnızca özet) makaleler kanıt tablosuna dahil edilmemiştir; bunlar arasında MDPI *Drones* 6(1)9, 6(1)22, 7(3)161; MDPI *Electronics* 12(6)1334; Wiley *ETT* 10.1002/ett.4813; Wiley/Hindawi 10.1155/2022/5428280 ve 10.1155/2021/4734023; Springer *Complex & Intelligent Systems* 10.1007/s40747-024-01348-9; Springer *CEAS Aeronautical Journal* 10.1007/s13272-024-00801-2 yer alır.
