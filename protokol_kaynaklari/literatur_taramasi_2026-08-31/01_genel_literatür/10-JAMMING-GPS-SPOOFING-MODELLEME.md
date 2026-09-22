# FANET Simülasyonlarında Jamming ve GPS-Denied/Spoofing Modellemesi (2021–2026)

**Amaç:** TÜBİTAK elektronik harp / taktik İHA mesh ağ simülasyonu projesi için literatür taraması.
**Yöntem:** 25 hakemli makale (tümü Scopus/WoS dizinli) taranmış; her parametre değeri makalenin **tam metni fetch edilerek** doğrulanmıştır. Snippet'ten değer alınmamıştır; makalede geçmeyen değerler "Belirtilmemiş" olarak işaretlenmiştir (simülatör varsayılanından tahmin yapılmamıştır).
**Kapsam:** MDPI Sensors/Electronics/Remote Sensing/Future Internet/Entropy, Springer Scientific Reports/Complex & Intelligent Systems, Frontiers, PeerJ CS; 2021–2026.

**Yapısal ayrım:** İki katman ayrı işlendi:
- **KATMAN A — RF Jamming:** jamming gücü (dBm/W), SJR/SINR/JSR (dB), etki yarıçapı (m) burada aranır.
- **KATMAN B — GPS-denied / GPS-spoofing:** SJR ve yarıçap bu katmanda **neredeyse hiç raporlanmaz** (yapısal nedenler bölümde). Bunun yerine konum hatası, sabit bias, GNSS kesinti süresi, sensör gürültü σ'sı, pseudorange ikamesi, C/N₀, Doppler kayması gibi soyutlamalar kullanılır. SJR/radius GPS tarafında uydurulmamıştır.

---

## A. KATMAN A — RF JAMMING KANIT TABLOSU

| # | Kaynak | Yıl | Jammer tipi | Simülatör | Jamming gücü | SJR / SINR / JSR (dB) | Etki yarıçapı | Tx gücü (İHA/jammer) | Yönlendirme / anti-jamming |
|---|---|---|---|---|---|---|---|---|---|
| A1 | [Targowski vd. (2026)](https://doi.org/10.3390/s26154785) | 2026 | Mobil kasıtlı jammer (omni/sektörel) | EMANE + CORE | Belirtilmemiş (normalize "strength" 1,00–1,48) | Belirtilmemiş (0–1 link-kalitesi skoru) | **950 m** (jamming); 1500 m (çevresel) | Belirtilmemiş | Yönlendirme kapsam dışı; 5 frekans-manevra politikası |
| A2 | [Huang vd. (2026)](https://doi.org/10.1038/s41598-026-35259-1) | 2026 | Sabit, sabit güçlü çok-jammer (constant) | MATLAB R2024b | **20 mW** (10/15/20 mW) | SINR eşiği **−3 dB** | Belirtilmemiş | İHA 10 mW / jammer 20 mW (2:1) | RJSS tabanlı çok-jammer lokalizasyonu |
| A3 | [Gao & Zhi (2025)](https://doi.org/10.1038/s41598-025-18718-z) | 2025 | Strateji kümesi (tek-frekans, dar/geniş bant, FSK, darbe) | Özel model (sürüm belirtilmemiş) | Belirtilmemiş | **SJR = −5 / −13 / −14 dB**; (SJR)_dB = (P_r)_dBm − (J_r)_dBm | Belirtilmemiş | Belirtilmemiş | DSSS, FH, oyun teorisi (Nash) |
| A4 | [Aich vd. (2025)](https://doi.org/10.3390/fi17100474) | 2025 | **Reaktif** (güç-tetiklemeli) | MATLAB R2024a | P_jam ∈ **[−40, +40] dB** (göreli) | **JSR [−40, +40] dB**; JNR ~ N(12, 3²) dB; alıcı SNR 10 dB | Belirtilmemiş | Belirtilmemiş | Bi-scale Mahalanobis tespiti (OFDM) |
| A5 | [Wang vd. (2025)](https://doi.org/10.3390/e27090967) | 2025 | Sabit frekanslı/sabit güçlü yer jammer'ı (constant) | Sayısal sim. (adı yok) | **p_J = 20 dBm** | Radar SINR eşiği **−10 dB** | Belirtilmemiş (1/d² ile örtük) | İHA 35 dBm / jammer 20 dBm | ISAC + jammer konum tahmini |
| A6 | [Wu, T. vd. (2026)](https://doi.org/10.3390/s26020614) | 2026 | Protokol-farkında sürekli preamble enjeksiyonu | GNU Radio + USRP/AntSDR (deneysel) | **−30…+30 dBm** tarama; etkin −5/−10 dBm; saha **50 W** | Belirtilmemiş (PRR/SER/EJPD) | **≈200 m** (beyaz gürültü); **≈1000 m** (preamble), 50 W | Belirtilmemiş | Sinyal tespiti (CNN) + gürültü giderme (GAN) |
| A7 | [Ni vd. (2026)](https://doi.org/10.3390/s26010181) | 2026 | 6 senaryo: single/multi-tone, tracking, sweeping, full, hybrid | MATLAB R2021a + PyTorch | Belirtilmemiş | Belirtilmemiş (BER eşiği 10⁻⁵) | Belirtilmemiş | Belirtilmemiş | Federated hiyerarşik DQN |
| A8 | [Wu, D. vd. (2022)](https://doi.org/10.3390/electronics11203372) | 2022 | "Jamming nodes" (tip etiketi yok) | Belirtilmemiş | **1–5 W** (jammer) | Girişim eşiği **−80 dBmW** | Belirtilmemiş | İHA 1 W / jammer 1–5 W (0–7 dB) | Kümeleme + kanal/güç tahsisi |
| A9 | [Xu vd. (2023)](https://doi.org/10.3390/s23083846) | 2023 | **Constant + mobil** (movable) jammer | NetLogo | Belirtilmemiş | Belirtilmemiş | Etki mesafesi 16/11 (Sim.4: 24/18); lit. UAS **75 km**, kara **7,1 km** | Belirtilmemiş | **JRP vs AODV vs DSR** (WSN) |
| A10 | [Zhou vd. (2022)](https://doi.org/10.3390/electronics11020184) | 2022 | Dağıtık işbirlikli karıştırma (ECM) | Belirtilmemiş | **3 W** (anten 20 dB) | Belirtilmemiş | Belirtilmemiş | jammer 3 W | NS/AS komşuluk seçim stratejileri |
| A11 | [Jeon vd. (2022)](https://doi.org/10.3390/s22030865) | 2022 | Proaktif "dost" işbirlikli jamming | Octave 6.1 + Raspberry Pi (deneysel) | **24 dBm** | Belirtilmemiş (BER/ILR) | Formül: (2√3/3)·x (sayısal yok) | P_s = 24 dBm / P_j = 24 dBm (0 dB) | CFJ-DMZ güvenli bölge |
| A12 | [Šabić vd. (2025)](https://doi.org/10.3390/s25082383) | 2025 | Reaktif jamming (LoRa) | bladeRF + HackRF, GNU Radio | Belirtilmemiş (yüksek güç niteliksel) | Belirtilmemiş | Belirtilmemiş | Belirtilmemiş | ChirpDetector + PSD işleme |
| A13 | [Almasoud (2023)](https://doi.org/10.1007/s40747-023-00970-3) | 2023 | Sabit yer jammer'ı | CPLEX/GAMS + JA-RC | Belirtilmemiş (P^J sembolik) | SINR eşiği γ̄ sembolik | Belirtilmemiş (250 m = küme yarıçapı, dikkat) | Belirtilmemiş | Jamming-farkında kümeleme + yörünge |
| A14 | [Kim vd. (2022)](https://doi.org/10.3390/s22062384) | 2022 | IEMI: barrage/CW (deneysel) | Deneysel (Pixhawk 4) | **−20…+23 dBm**; amplifiye **50 dBm** | Belirtilmemiş | Belirtilmemiş (Eşik alan 55–95 V/m) | Belirtilmemiş | Eşik belirleme (sensör/video) |

> Not: A9, WSN bağlamında olsa da klasik yönlendirme protokollerini (AODV/DSR) jamming altında karşılaştıran tek makaledir. A1 yönlendirmeyi açıkça kapsam dışı bırakır.

---

## B. KATMAN B — GPS-DENIED / GPS-SPOOFING KANIT TABLOSU

| # | Kaynak | Yıl | Saldırı tipi | Platform | Modelleme biçimi | Konum/spoofing hatası | Kesinti/spoofing süresi | Yönlendirme/lokalizasyon |
|---|---|---|---|---|---|---|---|---|
| B1 | [Dułowicz vd. (2026)](https://doi.org/10.3390/s26144551) | 2026 | CW jamming + irtifa spoofing + statik konum spoofing | Skydel + USRP X310 (SDR test yatağı) | Senkronize sahte GNSS sinyali enjeksiyonu | İrtifa 100→≈350 m (≈250 m sapma) | **60 s** jamming, **90 s** spoofing, 300 s senaryo; takeover 23–255 s | SDR GNSS alıcı karşılaştırması |
| B2 | [Gao & Li (2022)](https://doi.org/10.3390/s22124503) | 2022 | Yavaş değişen GNSS spoofing (drag-off) | MATLAB | Kalman innovation'a bias enjeksiyonu; T_u = 50 | Hedef 30/30/30 m → ulaşılan 29,8/32,3/43,2 m | 0–120 s | GNSS/INS anti-spoofing |
| B3 | [Chen vd. (2025)](https://doi.org/10.1038/s41598-025-91560-5) | 2025 | Gizli konum spoofing (step/ramp) | MATLAB | Ölçüm vektörü değiştirme; chi-square eşiği 33,1 | **b = (20,20,20) m** | t=10 s başlangıç, 120 s ufuk | İyileştirilmiş GA |
| B4 | [Hou vd. (2026)](https://doi.org/10.3390/rs18142286) | 2026 | GNSS-denied (varsayım) | Özel dijital platform | GNSS saldırı modeli yok — sensör hata modelleri | RMSE 24,54→16,44 m (işbirlikli) | 250 s periyot | Dağıtık işbirlikli lokalizasyon |
| B5 | [Li vd. (2026)](https://doi.org/10.3390/s26061984) | 2026 | GNSS-denied (jammed battlefield) | MATLAB R2022b | TOA/AOA ölçüm modelleri | Belirtilmemiş (grafik) | Belirtilmemiş | Formasyon-kısıtlı işbirlikli lokalizasyon |
| B6 | [Tariq & Shaukat (2026)](https://doi.org/10.3389/frcmn.2026.1760543) | 2026 | Statik/mobil-takip/çok-verici/meaconing spoofing | C++/Python + ROS/Gazebo + MATLAB | **Pseudorange ikamesi** (Denk.17); gücü meşruyla eşitler | Formasyon sapması 1,5–10 m | Belirtilmemiş | PARMP mesh protokolü + LLM doğrulama |
| B7 | [Alhoraibi vd. (2024)](https://doi.org/10.3390/s24186156) | 2024 | GPS spoofing (3 seviye) | Veri kümesi + Keras/TF | Sinyal-seviyesi hipotez modeli; GAN | Belirtilmemiş | Belirtilmemiş | Adversarial ML tespiti |
| B8 | [Talaei Khoei vd. (2022)](https://doi.org/10.3390/s22020662) | 2022 | GPS spoofing (3 seviye) | MATLAB + USRP | Öznitelik-seviyesi (Doppler, pseudorange) | Doppler **±20 Hz** eşiği | Belirtilmemiş | Dinamik seçim teknikleri |
| B9 | [Badar vd. (2025)](https://doi.org/10.7717/peerj-cs.2714) | 2025 | GPS spoofing (3 seviye, drag-off) | Veri kümesi (Zenodo) | Saldırı modeli yok; CNN-BiLSTM | Lit: güç avantajı 0,4 dB; C/N₀ 45 dB-Hz; sapma −4/2,5/5 m; yön >3°, 1°/adım | Belirtilmemiş | DeepSpoofNet tespiti |
| B10 | [Chandrasekar vd. (2024)](https://doi.org/10.1038/s41598-024-57480-6) | 2024 | Sybil/DDoS (GPS spoofing anılır) | **NS-2.35** | GPS/GNSS modeli yok | Belirtilmemiş | Belirtilmemiş | **S-AODV** + 7 kıyaslama |
| B11 | [Abdelkreem vd. (2026)](https://doi.org/10.1038/s41598-026-39867-9) | 2026 | Konum tahrifi (CP/COP/RP/ROP/ES) | VeReMi veri kümesi | Taksonomik/öznitelik (RSSIConf) | Belirtilmemiş (birim yok) | Belirtilmemiş | ML tabanlı tespit (XGBoost) |

> **Kritik gözlem:** 11 makalenin **hiçbiri** SJR/JSR (dB) veya jamming etki yarıçapı (m) raporlamıyor. Bu yapısal bir durumdur, bir eksiklik değildir (nedenleri aşağıda).

---

## C. RF JAMMING — Standart Parametre Aralıkları

### C.1 Karıştırma Gücü (Jamming Power)
8/14 makalede sayısal olarak var; iki ayrı ölçek gözlenir:

| Ölçek | Değerler | Kaynaklar |
|---|---|---|
| mW–W (ağ/sürü sim.) | **10–20 mW** (İHA 10 / jammer 20); **1–5 W** (jammer) vs 1 W (İHA); **3 W** | [Huang](https://pmc.ncbi.nlm.nih.gov/articles/PMC12953576/), [Wu, D.](https://www.mdpi.com/2079-9292/11/20/3372), [Zhou](https://www.mdpi.com/2079-9292/11/2/184) |
| dBm (link/deney) | **20 dBm** (vs 35 İHA); **24 dBm**; **−30…+30 dBm** tarama, saha 50 W; **−5…+23 dBm** IEMI eşikleri | [Wang](https://pmc.ncbi.nlm.nih.gov/articles/PMC12468963/), [Jeon](https://www.mdpi.com/1424-8220/22/3/865), [Wu, T.](https://www.mdpi.com/1424-8220/26/2/614), [Kim](https://www.mdpi.com/1424-8220/22/6/2384) |
| Göreli (mutlak yok) | P_jam ∈ **[−40, +40] dB**; normalize "strength" 1,00–1,48 | [Aich](https://www.mdpi.com/1999-5903/17/10/474), [Targowski](https://www.mdpi.com/1424-8220/26/15/4785) |

**Önemli:** Jammer/İHA güç oranı literatürde **0 dB ile +7 dB** arası (Huang 3 dB; Wu D. 0–7 dB; Jeon 0 dB) veya İHA lehine **−15 dB** (Wang). "Jammer her zaman çok daha güçlü" varsayımı literatürde desteklenmiyor; güçler aynı mertebede tutulup coğrafi yakınlık belirleyici yapılıyor.

### C.2 Sinyal-Karıştırma Oranı (SJR / SINR / JSR / JNR)
Yalnızca 5/14 makalede sayısal:

| Metrik | Değer | Tanım | Kaynak |
|---|---|---|---|
| SJR | **−5 / −13 / −14 dB** | (SJR)_dB = (P_r)_dBm − (J_r)_dBm | [Gao & Zhi 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12504448/) |
| JSR | **[−40, +40] dB** tarama; en yüksek ayrışma ≈ −7 dB | jammer-to-signal ratio, P_J = 10^(JSR/10) | [Aich 2025](https://www.mdpi.com/1999-5903/17/10/474) |
| JNR | **N(12, 3²) dB** | jammer-to-noise ratio | [Aich 2025](https://www.mdpi.com/1999-5903/17/10/474) |
| SINR eşiği (haberleşme) | **−3 dB** | altında paket çözülemiyor | [Huang 2026](https://pmc.ncbi.nlm.nih.gov/articles/PMC12953576/) |
| SINR eşiği (radar) | **−10 dB** | radar algılama minimumu | [Wang 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12468963/) |
| Girişim eşiği (dBm) | **−80 dBmW** | SJR yerine mutlak eşik | [Wu, D. 2022](https://www.mdpi.com/2079-9292/11/20/3372) |
| Alternatif metrikler | BER eşiği 10⁻² (kesinti) / 10⁻⁵ (başarı); PRR/SER/EJPD; ILR | SJR yerine | [Ni](https://www.mdpi.com/1424-8220/26/1/181), [Wu, T.](https://www.mdpi.com/1424-8220/26/2/614), [Jeon](https://www.mdpi.com/1424-8220/22/3/865) |

**Sonuç:** SJR/JSR taranan bir bağımsız değişken olarak kullanılıyor (−40…+40 dB), sabit bir tasarım değeri olarak değil. Karar eşiği SINR üzerinden: haberleşme kesilme eşiği **−3 dB**, radar için **−10 dB**. Etkili karıştırma ölçütü BER eşikleri: 10⁻² (link kesintisi) ve 10⁻⁵ (başarılı iletim).

### C.3 Karıştırma Etki Yarıçapı (Jamming Impact Radius)
Literatürde **en zayıf raporlanan parametre** (yalnızca 3/14 makale):

| Değer | Bağlam | Kaynak |
|---|---|---|
| **950 m** (jamming); 1500 m (çevresel) | EMANE/CORE emülasyonunda doğrudan jammer profili parametresi | [Targowski 2026](https://www.mdpi.com/1424-8220/26/15/4785) |
| **≈200 m** (beyaz gürültü); **≈1000 m** (preamble), 50 W | Gerçek İHA uzaktan-kumanda linkine karşı deneysel | [Wu, T. 2026](https://www.mdpi.com/1424-8220/26/2/614) |
| 16/11 birim (Sim.4: 24/18); lit. UAS 75 km, kara 7,1 km | İki-kademeli etki bölgesi (WSN) | [Xu 2023](https://pmc.ncbi.nlm.nih.gov/articles/PMC10144817/) |

**Öneri:** Sabit bir "jamming yarıçapı" literatürde nadir; çoğu makale yarıçapı **1/d² mesafe-bağımlı SINR** ile örtük üretiyor (Wang: h_jam = β/d²·ψ; Huang: log-normal shadowing, yol kaybı üsteli 2,20). Açık yarıçap parametresi kullanılacaksa savunulabilir doğrudan referanslar: **950 m** (2,4 GHz, 8–40 MHz BW) ve deneysel **200–1000 m** (915 MHz, 50 W).

### C.4 Yardımcı standart değerler
- **Frekans:** 2,4 GHz (2412/2437/2462 MHz); 915 MHz LoRa; 5,8 GHz ISM; 28 GHz mmWave; 3,1 GHz radar
- **Kanal:** log-normal shadowing (üstel 2,20); iki-yollu Rayleigh (0/−6 dB, Doppler 10 Hz), alıcı SNR 10 dB; Nakagami-m (hava-yer); hava-hava yol kaybı üsteli 2, birim mesafe kazancı −30 dBm, gürültü −170 dBm/Hz
- **Reaktif jammer zamanlaması:** yanıt gecikmesi **16 μs** (320 örnek @20 MS/s), jamming patlaması **144 μs**
- **Takip (follow) jammer olasılığı:** aynı kanal → kesin; komşu kanal → **0,5**
- **Jammer sayısı:** 1–4 (tipik 3); dost jammer 3; 6 etmen

---

## D. GPS-DENIED / SPOOFING — SJR/Yarıçap Neden Kullanılmaz, Yerine Ne Kullanılır

**BULGU (11/11 makalede doğrulandı):** Hiçbir GPS/GNSS makalesi SJR/JSR (dB) veya jamming etki yarıçapı (m) raporlamıyor. Nedenleri:

1. **Saldırı yeri farklı:** GPS spoofing bir ağ katmanı/RF girişim sorunu değil, **navigasyon çözümüne yapılan ölçüm enjeksiyonu**dur. Modelleme noktası pseudorange/Kalman innovation'dır, SINR değil ([Tariq & Shaukat 2026](https://www.frontiersin.org/journals/communications-and-networks/articles/10.3389/frcmn.2026.1760543/full); [Gao & Li 2022](https://www.mdpi.com/1424-8220/22/12/4503)).
2. **Spoofing gücü kasıtlı olarak meşru sinyalle eşitlenir** (gizlilik gereği): "power control... allowed us to match authentic signal levels, thereby concealing the attack until takeover" ([Tariq & Shaukat 2026](https://www.frontiersin.org/journals/communications-and-networks/articles/10.3389/frcmn.2026.1760543/full)). Bu durumda bir "SJR" tanımlamak anlamsızlaşır; başarı ölçütü tespit edilmemektir.
3. **Deney kurulumları kablolu/korumalı:** yarıçap fiziksel olarak tanımsız ([Dułowicz 2026](https://www.mdpi.com/1424-8220/26/14/4551): SMA yolu + 60 dB zayıflatıcı veya RF-korumalı kabin).
4. **GNSS-denied çalışmaları saldırıyı hiç modellemez:** GNSS yokluğu bir başlangıç varsayımıdır ([Hou 2026](https://www.mdpi.com/2072-4292/18/14/2286); [Li 2026](https://www.mdpi.com/1424-8220/26/6/1984)).
5. **ML/veri kümesi tabanlı çalışmalar öznitelik uzayında çalışır:** Doppler, pseudorange, C/N₀ öznitelikleri üzerinden sınıflandırma; fiziksel geometri yoktur ([Alhoraibi 2024](https://www.mdpi.com/1424-8220/24/18/6156); [Talaei Khoei 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8779586/); [Badar 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11935755/)).

### SJR/Yarıçap yerine kullanılan soyutlamalar (somut değerlerle)

| Soyutlama | Değerler | Kaynak |
|---|---|---|
| Sabit konum bias'ı / step vektörü | **b = (20,20,20) m** | [Chen 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11873055/) |
| Hedeflenen yer değiştirme + ulaşılan | 30/30/30 m → 29,8/32,3/43,2 m | [Gao & Li 2022](https://www.mdpi.com/1424-8220/22/12/4503) |
| Pseudorange ikamesi (fake position) | ρ ← ‖p_fake − s_k‖ + c·δt_spoofer + η | [Tariq & Shaukat 2026](https://www.frontiersin.org/journals/communications-and-networks/articles/10.3389/frcmn.2026.1760543/full) |
| İrtifa spoofing profili | 100 m → ≈350 m | [Dułowicz 2026](https://www.mdpi.com/1424-8220/26/14/4551) |
| GNSS kesinti/spoofing süresi | **60 s** (jamming), **90 s** (spoofing), **300 s** (uzun) | [Dułowicz 2026](https://www.mdpi.com/1424-8220/26/14/4551) |
| Spoof takeover süresi | ucuz alıcı 23–27 s; kaliteli 250 s veya dirençli | [Dułowicz 2026](https://www.mdpi.com/1424-8220/26/14/4551) |
| Lokalizasyon RMSE (GNSS yoksa) | 24,54 → 16,44 m (işbirlikli); %20 paket kaybıyla 16,0 → 53,1 m | [Hou 2026](https://www.mdpi.com/2072-4292/18/14/2286) |
| Sensör gürültü σ'sı | UWB σ=20 m; altimetre σ=10 m; manyetometre σ=0,5°; GNSS konum SD 2,5 m, hız 0,1 m/s | [Hou 2026](https://www.mdpi.com/2072-4292/18/14/2286), [Gao & Li 2022](https://www.mdpi.com/1424-8220/22/12/4503) |
| TOA/AOA gürültü σ'sı | σ_τ ≈ 0,2 m; σ_ψ = 3,6° | [Li 2026](https://www.mdpi.com/1424-8220/26/6/1984) |
| Gizlilik/tespit eşiği | chi-square eşiği **33,1** (P_fa=10⁻⁵); normalize innovation T_u=50 | [Chen 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11873055/), [Gao & Li 2022](https://www.mdpi.com/1424-8220/22/12/4503) |
| Doppler kayması anomalisi | basit spoofing'de **±20 Hz** dışına çıkıyor | [Alhoraibi 2024](https://www.mdpi.com/1424-8220/24/18/6156), [Talaei Khoei 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC8779586/) |
| C/N₀ ve güç avantajı | C/N₀ 45 dB-Hz; güç avantajı 0,4 dB | [Badar 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11935755/) |
| Yörünge/yön sapma (drag-off) | yön değişimi >3°; 1°/adım; sapma −4/2,5/5 m | [Badar 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC11935755/) |
| Görev/formasyon seviyesi etki | formasyon sapması 1,5–10 m; kohezyon %88–95 | [Tariq & Shaukat 2026](https://www.frontiersin.org/journals/communications-and-networks/articles/10.3389/frcmn.2026.1760543/full) |

---

## E. İki Literatür Boşluğu (Özgünlük Argümanı)

1. **FANET yönlendirme protokollerinin RF jamming altında NS-3/OMNeT++ karşılaştırması:** 14 RF jamming makalesinden yalnızca 1'i (Xu 2023, WSN bağlamında) AODV/DSR karşılaştırıyor; Targowski yönlendirmeyi açıkça kapsam dışı bırakıyor. Standart FANET protokollerinin (AODV/OLSR/GPSR/DSDV) kasıtlı RF jamming altında NS-3/OMNeT++ ile karşılaştırmalı performans analizi 2021–2026 literatüründe belirgin bir boşluktur.

2. **GPS-denied/spoofing ortamında yönlendirme karşılaştırması:** 11 GPS makalesinin hiçbiri GPS-denied/spoofing'i NS-3 veya OMNeT++ içinde modellemiyor. NS-2 kullanan tek FANET makalesi (Chandrasekar 2024) GPS spoofing'i modellemiyor (Sybil/DDoS modelliyor). Yönlendirme protokolü değerlendiren tek spoofing makalesi (Tariq & Shaukat 2026) kendi mesh protokolünü sunuyor, standart FANET protokolleriyle karşılaştırma yapmıyor.

Bu iki boşluk, TÜBİTAK projesi için doğrudan özgünlük argümanı oluşturur.

---

## F. Proje Simülasyonu İçin Önerilen İki-Katmanlı Saldırı Modeli

| Katman | Modelleme girdisi | Literatür-destekli değer aralığı |
|---|---|---|
| **A — RF jamming** | Jammer Tx gücü | 10–20 mW / 1–5 W / 20–24 dBm (İHA'ya göre 0…+7 dB) |
| | SINR kesme eşiği | **−3 dB** (haberleşme) |
| | SJR tarama aralığı | **−40…+40 dB** (bağımsız değişken olarak) |
| | Etki yarıçapı | Doğrudan: **950 m** (2,4 GHz); veya 1/d² + log-normal shadowing (üstel 2,20) ile örtük; deneysel üst sınır 1000 m |
| | Jammer tipi | constant / reactive (yanıt gecikmesi 16 μs) / sweeping / tracking (komşu kanal 0,5) / mobil |
| | Etkinlik ölçütü | BER > 10⁻², PRR, PDR |
| **B — GPS-denied / spoofing** | **SJR/yarıçap KULLANILMAZ** | — |
| | Sabit bias ofseti | **20 m** (XYZ) veya 30 m (K/D/Aşağı) |
| | Kademeli drag-off | yön değişimi 1°/adım (tespit eşiğinin altında) |
| | GNSS blackout/spoofing süresi | **60 s** (jamming), **90 s** (spoofing), uzun **300 s**; başlangıç t=10 s |
| | Lokalizasyon hatası (GNSS yoksa) | konum RMSE **16–25 m**; UWB σ=20 m, altimetre σ=10 m |
| | Spoof takeover süresi | ucuz alıcı 23–27 s, kaliteli 250 s veya dirençli |
| | Gizlilik kısıtı | chi-square innovation eşiği **33,1** (P_fa=10⁻⁵) veya T_u=50 |
| | Görev-seviyesi etki | formasyon sapması 1,5–10 m |

---

## G. Kaynakça (APA 7)

**Katman A — RF Jamming:**

1. Aich, N., Oubrahim, Z., Ait Talount, H., & Abbou, A. (2025). Bi-scale Mahalanobis detection for reactive jamming in UAV OFDM links. *Future Internet, 17*(10), 474. https://doi.org/10.3390/fi17100474 (Tam metin: https://www.mdpi.com/1999-5903/17/10/474)

2. Almasoud, A. (2023). Jamming-aware optimization for UAV trajectory design and internet of things devices clustering. *Complex & Intelligent Systems, 9*, 4571–4590. https://doi.org/10.1007/s40747-023-00970-3 (Tam metin: https://link.springer.com/article/10.1007/s40747-023-00970-3)

3. Gao, P., & Zhi, Y. (2025). A dynamic confrontational game model of UAV's data link in the complicated electromagnetic environment. *Scientific Reports, 15*, 34927. https://doi.org/10.1038/s41598-025-18718-z (Tam metin: https://pmc.ncbi.nlm.nih.gov/articles/PMC12504448/)

4. Huang, L., Xiong, L., Huang, S., Wang, J., & Wan, C. (2026). Iterative localization method for multiple jammers in UAV collaborative jamming attacks. *Scientific Reports, 16*, 7927. https://doi.org/10.1038/s41598-026-35259-1 (Tam metin: https://pmc.ncbi.nlm.nih.gov/articles/PMC12953576/)

5. Jeon, G.-H., Lee, J.-H., Sung, Y.-S., Park, H.-J., Lee, Y.-J., Yun, S.-W., & Lee, I.-G. (2022). Cooperative friendly jamming techniques for drone-based mobile secure zone. *Sensors, 22*(3), 865. https://doi.org/10.3390/s22030865 (Tam metin: https://www.mdpi.com/1424-8220/22/3/865)

6. Kim, S.-G., Lee, E., Hong, I.-P., & Yook, J.-G. (2022). Review of intentional electromagnetic interference on UAV sensor modules and experimental study. *Sensors, 22*(6), 2384. https://doi.org/10.3390/s22062384 (Tam metin: https://www.mdpi.com/1424-8220/22/6/2384)

7. Ni, D., Ma, S., Du, J., Wu, Y., Zhou, C., & Xiao, H. (2026). A federated hierarchical DQN-based distributed intelligent anti-jamming method for UAVs. *Sensors, 26*(1), 181. https://doi.org/10.3390/s26010181 (Tam metin: https://www.mdpi.com/1424-8220/26/1/181)

8. Šabić, J., Perković, T., Begušić, D., & Šolić, P. (2025). Practical realization of reactive jamming attack on long-range wide-area network. *Sensors, 25*(8), 2383. https://doi.org/10.3390/s25082383 (Tam metin: https://pmc.ncbi.nlm.nih.gov/articles/PMC12031409/)

9. Targowski, P., Łeska, S., Walczak, J., Chmielewski, S., & Furtak, J. (2026). Assessing the effectiveness of frequency manoeuvring in UAV networks under jamming and interference. *Sensors, 26*(15), 4785. https://doi.org/10.3390/s26154785 (Tam metin: https://www.mdpi.com/1424-8220/26/15/4785)

10. Wang, J., Xu, R., Peng, L., & Wei, X. (2025). Multi-UAV-assisted ISAC system: Joint user association, trajectory design, and resource allocation. *Entropy, 27*(9), 967. https://doi.org/10.3390/e27090967 (Tam metin: https://pmc.ncbi.nlm.nih.gov/articles/PMC12468963/)

11. Wu, D., Zhang, Y., & Chen, Y. (2022). Joint optimization method of spectrum resource for UAV swarm information transmission. *Electronics, 11*(20), 3372. https://doi.org/10.3390/electronics11203372 (Tam metin: https://www.mdpi.com/2079-9292/11/20/3372)

12. Wu, T., Mao, R., Du, Y., Zhu, Q., Wei, S., & Hu, C. (2026). Preamble injection-based jamming method for UAV LoRa communication links. *Sensors, 26*(2), 614. https://doi.org/10.3390/s26020614 (Tam metin: https://www.mdpi.com/1424-8220/26/2/614)

13. Xu, B., Lu, M., & Zhang, H. (2023). Multi-agent modeling and jamming-aware routing protocols for movable-jammer-affected WSNs. *Sensors, 23*(8), 3846. https://doi.org/10.3390/s23083846 (Tam metin: https://pmc.ncbi.nlm.nih.gov/articles/PMC10144817/)

14. Zhou, Y., Song, D., Ding, B., Rao, B., Su, M., & Wang, W. (2022). Distributed cooperative jamming with neighborhood selection strategy for unmanned aerial vehicle swarms. *Electronics, 11*(2), 184. https://doi.org/10.3390/electronics11020184 (Tam metin: https://www.mdpi.com/2079-9292/11/2/184)

15. Zhang, P., Huang, Y., & Jin, Z. (2023). An electronic jamming method based on a distributed information sharing mechanism. *Electronics, 12*(9), 2130. https://doi.org/10.3390/electronics12092130 (Tam metin: https://www.mdpi.com/2079-9292/12/9/2130)

**Katman B — GPS-denied / GPS-spoofing:**

16. Abdelkreem, E., Hussein, S., & Tammam, A. (2026). A machine learning based scheme for enhancing the detection of position falsification attacks in vehicular ad hoc networks. *Scientific Reports, 16*, 8950. https://doi.org/10.1038/s41598-026-39867-9 (Tam metin: https://pmc.ncbi.nlm.nih.gov/articles/PMC12988126/)

17. Alhoraibi, L., Alghazzawi, D., & Alhebshi, R. (2024). Detection of GPS spoofing attacks in UAVs based on adversarial machine learning model. *Sensors, 24*(18), 6156. https://doi.org/10.3390/s24186156 (Tam metin: https://www.mdpi.com/1424-8220/24/18/6156)

18. Badar, A. U. R., Mahmood, D., Iqbal, A., Kim, S. W., Akleylek, S., Cengiz, K., & Nauman, A. (2025). DeepSpoofNet: A framework for securing UAVs against GPS spoofing attacks. *PeerJ Computer Science, 11*, e2714. https://doi.org/10.7717/peerj-cs.2714 (Tam metin: https://pmc.ncbi.nlm.nih.gov/articles/PMC11935755/)

19. Chandrasekar, V., Shanmugavalli, V., Mahesh, T. R., Shashikumar, R., Borah, N., Vinoth Kumar, V., & Guluwadi, S. (2024). Secure malicious node detection in flying ad-hoc networks using enhanced AODV algorithm. *Scientific Reports, 14*, 7818. https://doi.org/10.1038/s41598-024-57480-6 (Tam metin: https://pmc.ncbi.nlm.nih.gov/articles/PMC10991512/)

20. Chen, H., Wen, Z., & Lei, C. (2025). Optimization of covert spoofing parameters for loosely coupled GNSS/INS systems based on improved genetic algorithm. *Scientific Reports, 15*, 7285. https://doi.org/10.1038/s41598-025-91560-5 (Tam metin: https://pmc.ncbi.nlm.nih.gov/articles/PMC11873055/)

21. Dułowicz, J., Skokowski, P., & Kelner, J. M. (2026). Experimental evaluation of GNSS receiver vulnerability to spoofing and jamming using SDR-based testbed. *Sensors, 26*(14), 4551. https://doi.org/10.3390/s26144551 (Tam metin: https://www.mdpi.com/1424-8220/26/14/4551)

22. Gao, Y., & Li, G. (2022). A slowly varying spoofing algorithm on loosely coupled GNSS/IMU avoiding multiple anti-spoofing techniques. *Sensors, 22*(12), 4503. https://doi.org/10.3390/s22124503 (Tam metin: https://www.mdpi.com/1424-8220/22/12/4503)

23. Hou, Z., Xue, C., Chen, S., Xu, C., Jiang, C., & Niu, J. (2026). Consistent-innovation-aided distributed cooperative localization for multi-UAV navigation in GNSS-denied environments. *Remote Sensing, 18*(14), 2286. https://doi.org/10.3390/rs18142286 (Tam metin: https://www.mdpi.com/2072-4292/18/14/2286)

24. Li, Q., Wang, P., Li, X., Zhang, J., Luo, Y., Yu, W., & Cheng, H. (2026). Formation-constrained cooperative localization for UAV swarms in GNSS-denied environments. *Sensors, 26*(6), 1984. https://doi.org/10.3390/s26061984 (Tam metin: https://www.mdpi.com/1424-8220/26/6/1984)

25. Talaei Khoei, T., Ismail, S., & Kaabouch, N. (2022). Dynamic selection techniques for detecting GPS spoofing attacks on UAVs. *Sensors, 22*(2), 662. https://doi.org/10.3390/s22020662 (Tam metin: https://pmc.ncbi.nlm.nih.gov/articles/PMC8779586/)

26. Tariq, U., & Shaukat, K. (2026). Mission-aware BeiDou spoofing defense in UAV swarms with LLM-assisted context validation. *Frontiers in Communications and Networks, 7*, 1760543. https://doi.org/10.3389/frcmn.2026.1760543 (Tam metin: https://www.frontiersin.org/journals/communications-and-networks/articles/10.3389/frcmn.2026.1760543/full)

---

**Dizin geçerliliği:** MDPI Sensors/Electronics/Remote Sensing/Future Internet/Entropy, Springer Scientific Reports/Complex & Intelligent Systems, Frontiers in Communications and Networks ve PeerJ Computer Science dergilerinin tümü Scopus ve Web of Science dizinlidir.
**Atıf notları:** Makale numarası kullanan dergilerde (MDPI, Scientific Reports) APA 7 uyarınca sayfa yerine makale numarası verilmiştir. Advance online publication olarak çıkan makalelerde cilt/sayı yerine "1–35" biçimi kullanılmıştır.
**Doğrulama notu:** Tüm sayısal değerler, yanındaki URL'nin tam metni bu oturumda fetch edilerek doğrulanmıştır. Erişilemeyen (Access Denied / yalnızca özet) ve bu nedenle tabloya dahil edilmeyen adaylar arasında MDPI Drones 8(7)338, Drones 7(7)461; Elsevier Ad Hoc Networks 10.1016/j.adhoc.2023.103179; Elsevier Computer Networks 10.1016/j.comnet.2024.110276; Wiley/Hindawi 10.1155/2021/9959310; Wiley 10.1002/dac.4885 yer alır.
