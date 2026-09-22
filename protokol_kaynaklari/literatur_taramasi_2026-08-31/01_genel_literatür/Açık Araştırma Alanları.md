# Taktik FANET Yönlendirmesinde Açık Araştırma Alanları ve Çözülmemiş Zorluklar

> **Kapsam:** Yüksek 3B mobilite + dinamik topoloji + aktif RF karıştırmasının **bir arada** olduğu
> taktik FANET yönlendirme protokollerindeki açık araştırma alanları. Atıflar 2022–2026
> (tarihsel arka plan hariç).

## Temel gerilim

2022–2026 literatürü parçalıdır. 3B mobilite/dinamik topoloji çalışmaları çoğunlukla karıştırmayı
dışarıda bırakır; anti-jamming çalışmaları ise çoğunlukla PHY/MAC, topoloji kontrolü veya
tek-yeni-protokol düzeyindedir. **OLSR, AODV ve GPSR'nin aynı deney tasarımında yüksek 3B mobilite +
aktif RF jamming + SJR/PDR/E2E ile karşılaştırıldığı bir çalışma bu taramada doğrulanamamıştır.**

- **Mobilite/topoloji kampı** karıştırmayı açıkça kapsam dışı bırakır:
  [El-Basioni 2024](https://www.nature.com/articles/s41598-024-72983-y),
  [Amponis 2023](https://eprints.whiterose.ac.uk/id/eprint/205730/1/IET%20Networks%20-%202023%20-%20Amponis%20-%20Anchored%20self%E2%80%90similar%203D%20Gauss%E2%80%90Markov%20mobility%20model%20for%20ad%20hoc%20routing%20scenarios.pdf),
  [Kaur vd. 2026](https://link.springer.com/article/10.1007/s44227-026-00104-4),
  [Huang vd. 2023](https://dl.acm.org/doi/10.1145/3631530).
- **Karıştırma kampı** standart FANET yönlendirme protokollerini karşılaştırmaz:
  [Yang vd. 2025](https://arxiv.org/abs/2508.11687) ajan-tabanlı P-D-A çerçevesi oyun teorisi
  + RL kullanır ama OLSR/AODV/GPSR yönlendirme karşılaştırması yapmaz.

Aşağıdaki tüm açık alanların kök nedeni budur: **mobilite kaynaklı rota kopması ile karıştırma
kaynaklı rota kopması eşzamanlı oluştuğunda ne yapılacağına dair doğrulanmış bir çerçeve yoktur.**

### Kısmi kesişim çalışmaları (boşluğu tam kapatmayan)

| Çalışma | Ne çözüyor | Neden tam boşluğu kapatmıyor |
|---|---|---|
| [Sarı & Seçinti 2024](https://www.sciencedirect.com/science/article/abs/pii/S1389128624000823) | CentAir topoloji kontrolü + centrality, aldatıcı jammer'a karşı PDR +%11,5 | Yalnız tek hedefli; ham OLSR'nin SJR'ye bağlı bozunumu değil |
| [Zheng vd. 2024 (CLUN-LSR)](https://www.sciencedirect.com/science/article/abs/pii/S1570870524003135) | Link katmanından spektrum durumu + iki-komşu sayısı rota seçimi (askeri) | Tek yeni protokol; OLSR/AODV/GPSR karşılaştırması yok |
| [JA-RC 2023](https://link.springer.com/article/10.1007/s40747-023-00970-3) | Jamming-farkındalığı UAV yörünge + IoT kümeleme birleşik | IoT toplama senaryosu, taktik mesh değil |
| [SUNET 2023](https://link.springer.com/article/10.1007/s11276-023-03500-8) | Federated DRL + beamforming/güç kontrolü + LSAQ routing | PHY odaklı; standart protokollerle FANET karşılaştırması yok |

---

## Açık araştırma alanları

### A1. 3B taktik mobilite için yetersiz modeller

**Sorun:** Standart mobilite modelleri (Random Walk, Random Waypoint, RPGM) 3B hava araçı
dinamiklerini (rüzgâr, türbülans, irtifa değişimi, dönüş) yakalayamaz; yüksek hızda PDR'nin
~%1'e düştüğü, en yüksek %14 (AODV) / %10 (OLSR) değerlere ulaştığı gösterilmiştir
([Amponis 2023](https://eprints.whiterose.ac.uk/id/eprint/205730/1/IET%20Networks%20-%202023%20-%20Amponis%20-%20Anchored%20self%E2%80%90similar%203D%20Gauss%E2%80%90Markov%20mobility%20model%20for%20ad%20hoc%20routing%20scenarios.pdf)).
3B hareket standart MANET protokollerini FANET için uygun hale getirmeyi zorlaştırır
([El-Basioni 2024](https://www.nature.com/articles/s41598-024-72983-y)).

**Açık nokta:** Bu taramada doğrulanan 2022–2026 kaynaklarında, 3B taktik manevra (kaçınma/evasive)
ile elektronik harp etkilerini aynı anda modelleyen bir mobilite+jamming modeli bulunamadı.
Amponis'in ASSGM-3D modeli 3B dinamikleri iyileştirir ama jamming içermez; karıştırma modelleri
(ör. [Gao & Zhi 2025](https://pmc.ncbi.nlm.nih.gov/articles/PMC12504448/) SJR taraması) hareket içermez.

### A2. Bağlantı kalitesi vs. bağlantı durumu farkındalığı

**Sorun:** OLSR bağlantı *durumunu* (var/yok) algılar ama bağlantı *kalitesini* (SINR, hata
oranı) algılayamaz; bu da yüksek mobilitede orantısız paket kaybına neden olur
([Amponis 2023](https://eprints.whiterose.ac.uk/id/eprint/205730/1/IET%20Networks%20-%202023%20-%20Amponis%20-%20Anchored%20self%E2%80%90similar%203D%20Gauss%E2%80%90Markov%20mobility%20model%20for%20ad%20hoc%20routing%20scenarios.pdf)).

**Açık nokta:** Karıştırmalı ortamda "bağlantı kalitesi" zaten saldırgan tarafından
bozulmaktadır; rota metriğine SINR/spektrum durumunu entegre eden çapraz-katman tasarım
standart protokoller bağlamında doğrulanamadı. [Zheng vd. 2024 (CLUN-LSR)](https://www.sciencedirect.com/science/article/abs/pii/S1570870524003135)
link katmanından gerçek zamanlı spektrum durumu alıp iki-komşu sayısını rota seçimine
katır (askeri bağlam), ama tek yeni bir protokoldür — OLSR/AODV/GPSR'yi karşılaştırmaz.

### A3. Kopma nedeni belirsizliği: mobilite mi, karıştırma mı?

**Sorun:** Bir bağlantı koptuğunda AODV/OLSR/GPSR kopmanın nedenini ayırt edemez. Mobilite
kaynaklı kopmada rota yeniden keşfi anlamlıdır; karıştırma kaynaklı kopmada ise RREQ yeniden
yayını karıştırılmış alana yazılır ve daha da kötüleşir (kontrol yükü çöküşü).

**Açık nokta:** [Huang vd. 2023](https://dl.acm.org/doi/10.1145/3631530) dinamik yönlendirmenin
eski rota bilgisi nedeniyle uzun gecikme ve paket kaybına neden olduğunu, zaman-kritik İHA sürü
görevlerini başarısız kıldığını gösterir. [El-Basioni 2024](https://www.nature.com/articles/s41598-024-72983-y)
AODV rotalarının topoloji değişmese bile tablodan silinebildiğini belirtir. Ancak bu taramada
doğrulanan kaynaklarda, kopma nedenini (mobilite/jamming) sınıflandıran ve buna göre farklı
kurtarma eylemi tetikleyen bir mekanizma bulunamadı. Bu, projenin ölçebileceği özgün bir katkıdır.

### A4. SJR'ye bağlı karşılaştırmalı FANET verisi eksikliği

**Sorun:** 2022–2026 FANET literatüründe OLSR, AODV ve GPSR için değişen SJR altında
doğrudan raporlanmış PDR ve E2E gecikme düşüş yüzdeleri yoktur (bkz. proje dosyası
`13-SJR-PDR-E2E-LITERATUR-BOŞLUĞU.md`). Bu, doğrulanmış bir literatür boşluğudur.

### A5. Anti-jamming kararları ile yönlendirme kararlarının birleşik optimizasyonu

**Sorun:** Karıştırma karşıtı teknikler (frekans atlaması, beam nulling, güç kontrolü) çoğunlukla
PHY/MAC katmanında kalır; hangi yolun (rota) seçileceği ile karıştırmadan kaçınma kararı
ayrı optimize edilir. [Sarı & Seçinti 2024](https://www.sciencedirect.com/science/article/abs/pii/S1389128624000823)
CentAir ile topoloji kontrolü + centrality kullanarak aldatıcı jammer'lara karşı
PDR +%11,5, gecikme −%21,1 iyileştirir, ama yalnız tek hedeflidir. [Yang vd. 2025](https://arxiv.org/abs/2508.11687)
ajan-tabanlı P-D-A ile oyun teorisi + RL önerir ama standart FANET yönlendirme protokollerini
karşılaştırmaz.

**Açık nokta:** 3B yüksek mobilite + çok-kaynak karıştırma altında, spektrum-farkındalığı
olan rota seçiminin (rota + frekans/beam birlikte) FANET ölçeğinde çözümü yeterli değil.
[JA-RC 2023](https://link.springer.com/article/10.1007/s40747-023-00970-3) jamming-farkındalığı
UAV yörünge + IoT kümeleme birleşik optimize eder ama IoT toplama senaryosudur, taktik mesh değil.

### A6. GPSR'nin 3B çevre (perimeter) zafiyeti ve sahte konum

**Sorun:** GPSR'nin çevresel geri dönüş modu 3B'de zayıftır; yerel maksimum'a takılır.
GPSR, AODV'den daha hızlı bozulur (tarihsel arka plan, [Won vd. 2006](https://dl.ifip.org/db/conf/euc/eucw2006/WonYA06.pdf)).

**Açık nokta:** 3B GPSR variantları önerilmiştir (ör. [SDN-FANET 3D-GPSR + Kalman, Sensors 2025](https://www.mdpi.com/1424-8220/25/5/1417)),
ama bunlar karıştırma içermiyor. GPSR'nin konum bağımlılığı, karıştırma altında beacon
kaybı ve GPS spoofing ile birleştiğinde (tarihsel arka plan: Leinmüller vd. 2005 %10/%40 bozulma)
3B'de çözülmemiş bir güvenlik-mobilite birleşik sorun olarak değerlendirilir.

### A7. SDN/merkezî kontrolün tek-nokta zafiyeti

**Sorun:** SDN-FANET yaklaşımları merkezî denetimi kullanır ([SDN-FANET Sensors 2025](https://www.mdpi.com/1424-8220/25/5/1417));
bu denetleyicinin kendisi karıştırma/saldırı hedefidir.

**Açık nokta:** Merkezî topoloji bilgisine dayanan yönlendirme, denetleyici bağlantısı
koparsa çöker. Dağınık, jamming-dayanıklı alternatif (ör. [federated DRL + LSAQ routing,
SUNET 2023](https://link.springer.com/article/10.1007/s11276-023-03500-8)) önerilmiştir
ama yine PHY odaklı (beamforming + güç kontrolü) ve standart protokollerle karşılaştırmalı
FANET değerlendirmesi yapmaz.

---

## Çözülmemiş zorluklar (sentez)

| # | Zorluk | Mevcut durum | Açık boşluk |
|---|---|---|---|
| 1 | 3B taktik manevra + EW birleşik modeli | Mobilite ve jamming ayrı modelleniyor | Birleşik 3B model doğrulanamadı |
| 2 | Kopma nedeni (mobilite/jamming) ayrımı | Tüm protokoller kopmayı aynı ele alır | Sınıflandıran mekanizma bulunamadı |
| 3 | Bağlantı kalitesi farkındalığı | OLSR link state algılar, quality algılamaz | SINR'yi rota metriğine entegre az |
| 4 | SJR'ye bağlı OLSR/AODV/GPSR verisi | Hiçbir 2022–2026 kaynağı raporlamaz | Yeni simülasyon gerekli |
| 5 | Rota + frekans/beam birleşik optimizasyon | PHY ve routing ayrı çözülüyor | FANET ölçeğinde birleşik çözüm eksik |
| 6 | GPSR 3B perimeter + konum sahtekarlığı | 3D-GPSR var ama jamming yok | Güvenlik-mobilite birleşik analiz yok |
| 7 | SDN merkezî kontrol zafiyeti | Denetleyici hedef olabilir | Dağınık jamming-dayanıklı alternatif sınırlı |

## Proje çıkarımı

Bu açık alanlar, projenin `01-PROBLEM-VE-AMAC.md` §2.1'deki ⭐ varlık gerekçesiyle doğrudan
örtüşür: literatürde bu protokollerin karıştırma + yüksek 3B mobilite altındaki karşılaştırmalı
davranışı için doğrudan birincil kaynak yoktur; kontrollü bir ortamda bunu ölçmek başlı başına
bir katkıdır. Projenin özgün katkısı, **kopma nedenini ayırt eden** ve **SJR'ye bağlı** ölçümler
üreten bir simülasyon çerçevesi olabilir.

---

## Kaynakça (APA 7)

Amponis, G. (2023). Anchored self-similar 3D Gauss-Markov mobility model for ad hoc routing scenarios. *IET Networks, 12*(5), 250–259. https://doi.org/10.1049/ntw2.12089

El-Basioni, B. M. M. (2024). Intensive study, tuning and modification of reactive routing approach to improve flat FANET performance in data collection scenario. *Scientific Reports, 14*, 23467. https://doi.org/10.1038/s41598-024-72983-y

Gao, P., & Zhi, Y. (2025). A dynamic confrontational game model of UAV's data link in the complicated electromagnetic environment. *Scientific Reports, 15*, 34927. https://pmc.ncbi.nlm.nih.gov/articles/PMC12504448/

Huang, Z., Wu, W., Fu, C., Liu, X., Shan, F., Wang, J., & Xu, X. (2023). Communication-topology-preserving motion planning: Enabling static routing in UAV networks. *ACM Transactions on Sensor Networks, 20*(1), Article 24. https://doi.org/10.1145/3631530

Kaur, U., Kapila, D., Bharany, S., et al. (2026). Next-generation FANET routing: A systematic review of mobility models, routing protocol families, and future research roadmap. *International Journal of Networked and Distributed Computing*. https://doi.org/10.1007/s44227-026-00104-4

Sarı, T. T., & Seçinti, G. (2024). Using centrality based topology control for FANET survivability against jamming. *Computer Networks, 242*, Article 110250. https://www.sciencedirect.com/science/article/abs/pii/S1389128624000823

Yang, J., Cui, M., Zhang, H., Ji, F., Lai, Z., & Wang, Y. (2025). *Agent-based anti-jamming techniques for UAV communications in adversarial environments: A comprehensive survey* (arXiv:2508.11687). arXiv. https://arxiv.org/abs/2508.11687

Zheng, S., Zhu, X., Qin, Z., & Dong, C. (2024). Cross-layer UAV network routing protocol for spectrum denial environments. *Ad Hoc Networks*. https://www.sciencedirect.com/science/article/abs/pii/S1570870524003135

### Tarihsel arka plan (2022–2026 kanıtı sayılmaz)

Leinmüller, T., Schoch, E., Kargl, F., & Maihöfer, C. (2005). Influence of falsified position data on geographic ad-hoc routing. In *Proceedings of ESAS 2005*. https://www.uni-ulm.de/fileadmin/website_uni_ulm/iui.inst.100/institut/Papers/Prof_Weber/esas2005.pdf

Won, C., Youn, J.-H., & Ali, H. (2006). Impact of high-mobility radio jamming in large scale wireless sensor networks. In *IFIP EUC Workshops Proceedings*. https://dl.ifip.org/db/conf/euc/eucw2006/WonYA06.pdf

> **Şeffaflık notu:** [JA-RC (Complex & Intelligent Systems 2023)](https://link.springer.com/article/10.1007/s40747-023-00970-3)
> ve [SUNET (Telecommunication Systems 2023)](https://link.springer.com/article/10.1007/s11276-023-03500-8)
> tam künyeleri (cilt/sayı/sayfa) kaynak sayfalarında basılı olmadığı için doğrulanamamıştır;
> atıf öncesi nihai kontrol önerilir. [SDN-FANET 3D-GPSR (Sensors 2025)](https://www.mdpi.com/1424-8220/25/5/1417)
> ve Sarı & Seçinti (2024) için DOI kesinleştirilmemiştir.
