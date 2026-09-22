# Taktik İHA Mesh Ağlarında Anti-Jamming Yönlendirme: Q-Learning, Çok Yollu Dinamik Anahtarlama ve Mobilite Tahmini

> **Kapsam:** Üç tekniğin (Q-learning/RL, çok yollu dinamik anahtarlama, mobilite tahmini)
> karıştırmaya karşı dirençli FANET yönlendirmesinde güncel (2022–2026) uygulanış biçimleri.
> Tarihsel arka plan (2018–2021) ayrı belirtilmiştir.

## Özet: Parçalı Uygulama

Üç teknik de literatürde uygulanmaktadır, ancak **farklı katmanlarda ve nadiren birleşik**.
Bu taramada doğrulanan örneklerde: anti-jamming RL'leri genellikle **kanal/güç/modülasyon**
(PHY) seçimi yapar; Q-learning'in **yönlendirme** (next-hop) versiyonları jamming'i ele almaz;
mobilite tahmini (Kalman) jamming'i ele almaz; çok yollu anahtarlama jamming'i ele alır ama
çoğu tarihsel. Üçünü standart OLSR/AODV/GPSR için birleştiren bir çalışma doğrulanamadı.

---

## 1. Q-Learning / Pekiştirmeli Öğrenme

### 1a. Yönlendirme (next-hop) düzeyinde — jamming dışı

**QLR-FANET (ETRI Journal 2025):** Veri paketi bir "sanal öğrenme ajanı" olarak modellenir;
mevcut düğüm komşu İHA'lardan birini next-hop olarak seçer ve kümülatif ödülü maksimize eder.
Durum değişkenleri: paket hata oranı (PER), komşu kuyruk yükü, göreli hız; ödül D-ACK geri
bildirimiyle hesaplanır; dinamik link-bitrate ayarı + yeniden iletim cezası mekanizması vardır.
Ancak **çok yollu anahtarlama ve Kalman tahmini içermez**; RF jamming'i ele almaz
([Mai vd. 2025](https://onlinelibrary.wiley.com/doi/full/10.4218/etrij.2024-0298)).

**6G UAV Q-learning (CMC 2026):** Q-learning + link-farkındalığı + mobilite-farkındalığı.
Kalman filtresi sabit-hız modeliyle İHA konumunu tahmin eder; durum = depoya mesafe
(discrete state bin) + komşular; ödül = enerji + bağlantı kalitesi (mesafe, göreli hız, paket
kaybı) + E2E gecikme; eylem = next-hop/relay seçimi (Softmax + ε-greedy keşif). **RF jamming
ele alınmaz** ([Nam vd. 2026](https://www.techscience.com/cmc/v86n1/64490/html)).

### 1b. Anti-jamming düzeyinde — kanal/güç/modülasyon seçimi (PHY)

**FL-HDQN (Sensors 2026):** Federated hierarchical Deep Q-Network; iki katmanlı:
(1) kanal seçimi — spektrum enerji algılama ile her kanalın dolu/boş durumu (0/1),
durum uzayı \(2^c\); (2) seçilen kanal üzerinde güç + modülasyon-coding ortak optimizasyonu.
Ödül: başarılı iletim (BER < \(10^{-5}\)) için R=1. **Açıkça jamming'e karşı:** çok-kanallı
spektrum algılama + güç/modülasyon adaptasyonu. Kanal seçimi düzeyinde, rota seçimi değil
([Ni vd. 2026](https://www.mdpi.com/1424-8220/26/1/181)).

**Meta-MMFQ (Radioengineering 2024):** Meta-öğrenme + mean-field Q-learning ile büyük ölçekli
çok-UAV ağlarda uyarlamalı anti-jamming **kanal seçimi** (rota seçimi değil). Durum:
İHA/jammer konumları + jammer'ın önceki kanalı + ACK/NACK + jammer mesafeleri; eylem = kanal
seçimi; ödül = SINR ≥ χ iken ulaşılabilir verim. **Açıkça kötü niyetli jamming + eş-kanal
girişim**; Gaussian Markov mobilite modeli, ama **Kalman tahmini değil**
([Hu vd. 2024](https://www.radioeng.cz/fulltexts/2024/24_03_0417_0431.pdf)).

**Yang vd. 2025 (anket):** Ajan-tabanlı "Algılama-Karar-Eylem" (P-D-A) çerçevesi; oyun teorisi
ile UAV-jammer etkileşimi + RL ile uyarlamalı strateji. Kaçınma stratejisi temel olarak frekans
atlama (frequency hopping) ve kanal değiştirme; PHY odaklıdır
([Yang vd. 2025](https://arxiv.org/abs/2508.11687)).

### 1c. Hibrit: Q-learning + Kalman mobilite tahmini

**TARRAQ (2023):** Topoloji-farkındalıklı dayanıklı yönlendirme, uyarlamalı Q-learning;
Kalman filtresi komşunun kalan link süresini (residual link duration) tahmin eder ve son kullanma
zamanı olarak kullanır. Q-learning-tabanlı, mobilite tahmin-tabanlı ve GPSR-EEH'ye göre
overhead %25,23 daha düşük, PDR %9,41 daha yüksek, enerji %5,12 daha düşük. **Mobilite-dayanıklı,
RF-jamming'e özgü değil** ([Cui vd. 2023](https://ar5iv.labs.arxiv.org/html/2306.17360)).

> **Gözlem:** Anti-jamming RL'leri genellikle PHY düzeyinde kanal/güç/modülasyon seçer;
> yönlendirme RL'leri next-hop seçer (network) ama jamming bilmez. İki katmanı birleştiren
> (jamming-farkındalığı rota seçimine yansıtan) çalışma sınırlıdır.

---

## 2. Çok Yollu Dinamik Anahtarlama

**CentAir (Sarı & Seçinti 2024, Computer Networks):** Topoloji kontrolü + eigenvector
centrality ile aldatıcı (deceptive) jammer'lara karşı dayanıklılık. Üç mod: temel CentAir
(maliyet = iletim zamanı + hop sayısı), CentAir-Q (interframe space'leri centrality ile
azaltır, düşük gecikme), Hybrid CentAir (akışa göre en iyi modu seçer). Çok-kanallı yapısı
jammer'ın tek kanalı hedeflemesini engeller; OMNeT++'da PDR +%11,5, gecikme −%21,1, enerji
verimliliği +%17,8. **Sınırlama:** yalnız tek hedefli
([Sarı & Seçinti 2024](https://www.sciencedirect.com/science/article/abs/pii/S1389128624000823)).

**Karınca kolonisi melez çok yollu (Scientific Reports 2024):** Düşük hata toleransı için
bağlantı kalitesi, trafik yükü ve uzamsal mesafe dikkate alan girişime-dirençli çok yollu
yönlendirme. Tam yazar listesi kaynak sayfasında doğrulanmamıştır
([Scientific Reports 2024](https://www.nature.com/articles/s41598-024-64454-1)).

**Tarihsel arka plan:** JarmRout (IEEE Access 2018), FANET'lerde kasıtlı jamming ve lokal
arıza için çok yollu yönlendirme; tüm yollar eşzamanlı çökmedikçe iletişim sürer
([JarmRout 2018](https://congpu.github.io/document/paper/ieee_access_2018.pdf)). AFRL (JCN 2020),
federated RL ile FANET'te jamming savunması — temel çalışma.

---

## 3. Mobilite Tahmini (Kalman / Yörünge)

**Tahmin-Güçlendirmeli OLSR + Kalman (NaNA 2025):** Kalman filtresi İHA düğüm konumlarını
tahmin eder; bağlantı durumunu proaktif tahmin eder, potansiyel link kopmasını önceden algılar.
Sonuca dayalı **yedek rota seçimi + kopma öncesi yol değiştirme (pre-switching)**; Hello/TC
mesaj sıklığını mobiliteye göre dinamik ayarlar. **Jamming ele alınmaz**
([An vd. 2025](https://www.computer.org/csdl/proceedings-article/nana/2025/147200a490/2ckdX3QzKGk)).

**SDN-FANET 3D-GPSR + Kalman (Sensors 2025):** Adaptif Genişletilmiş Kalman (EKF) ile 3B İHA
hareketini takip/tahmin; SDN denetleyici tahmin sonucuyla iletim yolunu hesaplar; yüksek hızda
paket kaybını azaltır; OPNET'te PDR ve E2E gecikme iyileşmesi. **Jamming ele alınmaz**
([Sun vd. 2025](https://www.mdpi.com/1424-8220/25/5/1417)).

> **Gözlem:** Kalman-tabanlı mobilite tahmini OLSR ve GPSR'ye uygulanmıştır, ama jamming
> senaryosunda değil. Tahmin, kopmayı önceden sezip yedek yola geçmeye yarar — bu, jamming
> kaynaklı kopmada da değerli olabilir, ama literatürde bu birleşim doğrulanamadı.

---

## Uygulama Tablosu

| Teknik | Katman | Jamming mi? | Güncel örnek (2022–2026) | Mekanizma |
|---|---|---|---|---|
| Q-learning (yönlendirme) | Network (next-hop) | Hayır | [QLR-FANET 2025](https://onlinelibrary.wiley.com/doi/full/10.4218/etrij.2024-0298), [CMC 2026](https://www.techscience.com/cmc/v86n1/64490/html) | Paket=ajan; durum=PER/yük/hız; ödül=D-ACK |
| Q-learning (anti-jamming) | PHY (kanal/güç/modülasyon) | Evet | [FL-HDQN 2026](https://www.mdpi.com/1424-8220/26/1/181), [Meta-MMFQ 2024](https://www.radioeng.cz/fulltexts/2024/24_03_0417_0431.pdf) | Enerji algılama→kanal; güç+modülasyon; SINR ödül |
| Q-learning + Kalman (hibrit) | Network | Hayır | [TARRAQ 2023](https://ar5iv.labs.arxiv.org/html/2306.17360) | Kalman→link süresi; Q-learning→relay |
| Çok yollu anahtarlama | Network | Kısmen | [CentAir 2024](https://www.sciencedirect.com/science/article/abs/pii/S1389128624000823) | Çok-kanallı + centrality; yedek yol |
| Mobilite tahmini (Kalman) | Network/PHY | Hayır | [Prediction-OLSR 2025](https://www.computer.org/csdl/proceedings-article/nana/2025/147200a490/2ckdX3QzKGk), [SDN-3D-GPSR 2025](https://www.mdpi.com/1424-8220/25/5/1417) | Konum tahmini→proaktif link kopması algı+yedek yol |

## Bütünleşme boşluğu

Üç teknik ayrı ayrı olgundur, ama **aynı deneyde** birleştiğinde:
- Q-learning'in anti-jamming versiyonu kanal seçer ama rota seçmez → PHY-level jamming
  kaçınma rota kararına yansımaz.
- Yönlendirme Q-learning'i jamming bilmez → karıştırma altında yanlış next-hop seçer.
- Mobilite tahmini jamming bilmez → kopmanın jamming mi mobilite mi olduğunu ayırt edemez.

Projenin özgün katkısı, **üç tekniği aynı simülasyon çerçevesinde** birleştirebilir: Kalman ile
kopma nedenini ayırt et (mobilite/jamming), Q-learning ile jamming-farkındalığı rota seçimine
yansıt, çok yollu dinamik anahtarma ile karıştırılmış yoldan karıştırılmamış yola proaktif geç.

---

## Kaynakça (APA 7)

An, J., Yang, Z., Xiao, Z., & Liu, Q. (2025). A prediction-enhanced OLSR protocol for reliable routing in FANETs using Kalman filtering. In *2025 International Conference on Networking and Network Applications (NaNA)* (pp. 490–495). IEEE. https://doi.org/10.1109/NaNA66698.2025.00084

Cui, Y., Zhang, Q., Feng, Z., Wei, Z., Shi, C., & Yang, H. (2023). *Topology-aware resilient routing protocol for FANETs: An adaptive Q-learning approach* (arXiv:2306.17360). arXiv. https://ar5iv.labs.arxiv.org/html/2306.17360

Hu, L., Shao, Y., Qian, Y., Du, F., Li, J., Lin, Y., & Wang, Z. (2024). Meta-reinforcement learning in time-varying UAV communications: Adaptive anti-jamming channel selection. *Radioengineering, 33*(3), 417–431. https://doi.org/10.13164/re.2024.0417

Hybrid ant colony-based inter-cluster routing protocol for FANET. (2024). *Scientific Reports, 14*, 64454. https://www.nature.com/articles/s41598-024-64454-1

Mai, C. T., et al. (2025). QLR-FANET: A Q-learning and rate control-based routing protocol for flying ad hoc network. *ETRI Journal, 47*(6), 1015–1027. https://doi.org/10.4218/etrij.2024-0298

Nam, V. H., Hue, C. T. M., & Anh, D. V. (2026). An improved reinforcement learning-based 6G UAV communication for smart cities. *Computers, Materials & Continua, 86*(1), 1–15. https://doi.org/10.32604/cmc.2025.070605

Ni, D., Ma, S., Du, J., Wu, Y., Zhou, C., & Xiao, H. (2026). A federated hierarchical DQN-based distributed intelligent anti-jamming method for UAVs. *Sensors, 26*(1), Article 181. https://doi.org/10.3390/s26010181

Sarı, T. T., & Seçinti, G. (2024). Using centrality based topology control for FANET survivability against jamming. *Computer Networks, 242*, Article 110250. https://www.sciencedirect.com/science/article/abs/pii/S1389128624000823

Sun, K., Liu, M., Yin, C., & Wang, Q. (2025). Adaptive extended Kalman prediction-based SDN-FANET segmented hybrid routing scheme. *Sensors, 25*(5), Article 1417. https://doi.org/10.3390/s25051417

Yang, J., Cui, M., Zhang, H., Ji, F., Lai, Z., & Wang, Y. (2025). *Agent-based anti-jamming techniques for UAV communications in adversarial environments: A comprehensive survey* (arXiv:2508.11687). arXiv. https://arxiv.org/abs/2508.11687

### Tarihsel arka plan (2022–2026 kanıtı sayılmaz)

JarmRout. (2018). Jamming-resilient multipath routing protocol for flying ad hoc networks. *IEEE Access*. https://congpu.github.io/document/paper/ieee_access_2018.pdf

> **Şeffaflık notu:** QLR-FANET (2025) tam yazar listesi ve karınca kolonisi makalesi (2024)
> tam yazar listesi kaynak sayfalarında doğrulanamamıştır; "et al."/başlığa-göre format
> kullanılmıştır. Atıf öncesi nihai kontrol önerilir.
