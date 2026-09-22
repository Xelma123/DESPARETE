# Taktik İHA Mesh Ağlarında Düşman Karıştırıcıların Saha Davranışları

## Kapsam

Bu çalışma, taktik İHA mesh/FANET ağlarında düşman karıştırıcıların saha davranışını **sinyal sınıfı × platform × yayın düzeni** eksenlerinde ve dört senaryo ailesiyle inceler: cephe hattı, derin sızma, hedef koruma ve havadan eşlik.

Bu çerçeve, açık literatürdeki karıştırma modelleri, mobil jammer çalışmaları ve FANET araştırmalarından türetilmiş analitik bir modeldir. Gerçek saha verileri sınırlı olduğundan, senaryo aileleri doğrudan standartlaştırılmış askerî sınıflar değil, deney tasarımı kategorileridir.

## Davranış eksenleri

### Sinyal sınıfı

| Sınıf | Tipik davranış | Ağ belirtisi |
|---|---|---|
| Dar bant/spot | Belirli taşıyıcıya yoğunlaşma | Hedef kanalda yüksek parazit |
| Geniş bant/barrage | Geniş spektrumu kaplama | Genel gürültü tabanı artışı |
| Ton/taşıyıcı | Sabit veya sınırlı frekans bileşeni | Spektrumda keskin çizgiler |
| Süpürmeli/frekans çevik | Frekanslar arasında geçiş | Zaman-frekans izinin hareketi |
| Protokol-farkında | Preamble, ACK veya kontrol trafiğini hedefleme | Paket anlarında hata ve yeniden iletim |
| Aldatıcı/paket-benzeri | Meşru çerçeveye benzeyen sinyal | CCA meşguliyeti, kanal kilitlenmesi |
| Reaktif | Meşru yayın algılanınca kısa yayın | Boşta normal, paket penceresinde bozulma |

### Platform

| Platform | Saha davranışı | Ağ anlamı |
|---|---|---|
| Sabit yer | Önceden seçilmiş mevziden yayın | İstikrarlı karıştırma bölgesi |
| Araç | Arazi/yol ve görev hareketiyle konum değişimi | Hareketli parazit bölgesi |
| Hava | İrtifa, hız ve yön değiştiren yayıncı | 3B parazit hacmi ve hızlı menzil değişimi |

### Yayın düzeni

| Düzen | Olası amaç | Gözlenebilir örüntü |
|---|---|---|
| Sürekli | Bölgesel erişimi reddetmek | Kalıcı yüksek enerji ve kanal meşguliyeti |
| Aralıklı/darbeli | Enerji tasarrufu ve daha düşük görünürlük | Periyodik/rastgele darbeler |
| Yayın-sus-yer değiştir | Etki oluşturup konum belirsizliği yaratmak | Farklı konumlarda tekrarlayan olaylar |
| Reaktif | Kritik trafik sırasında etki | Paket zamanlarına bağlı bozulma |

## Platform × yayın düzeni

| Platform | Sürekli | Aralıklı | Yayın-sus-yer değiştir |
|---|---|---|---|
| Sabit yer | Kalıcı karıştırma hücresi | Enerji tasarruflu alan reddi | Daha az doğal; yön/p güç değişimiyle taklit edilebilir |
| Araç | Konvoy veya mevzi boyunca hareketli etki | Dur-kalk ve kısa yayınlar | Doğal ve anlamlı bir davranış modeli |
| Hava | Dinamik, görüş hattı destekli kapsama | Görev anlarında kısa darbeler | 3B hareket ve sessizlikle konumlama zorlaşır |

## Senaryo aileleri

### 1. Cephe hattı

Amaç, temas bölgesindeki taktik haberleşme koridorunu veya ileri unsurların bağlantısını bölgesel olarak reddetmektir. Sabit yer platformları sürekli/geniş bant, araç platformları hat boyunca hareketli ve reaktif yayın kullanabilir. Beklenen belirtiler eşzamanlı komşu link kaybı, PDR düşüşü, rota değişiminde artış ve ağ bölünmesidir.

### 2. Derin sızma

Amaç, ağın kritik rölelerine veya omurga bağlantılarına yaklaşarak az sayıda link üzerinden yüksek ağ etkisi oluşturmaktır. Yayın-sus-yer değiştir ve reaktif davranışlar öne çıkar. Genel gürültü tabanından ziyade belirli rotalarda ETX artışı, link ömrü düşüşü, düzensiz PDR kaybı ve rota onarımları beklenir.

### 3. Hedef koruma

Amaç, yüksek değerli bir hedef çevresinde elektromanyetik reddetme alanı oluşturmaktır. Sabit yer, araç veya hava platformları hedefe yaklaşan bağlantıları seçici ya da geniş bant biçimde etkileyebilir. Etki yalnızca mesafeye bağlı değildir; anten yönelimi, irtifa, arazi ve kritik düğüm rolü birlikte değerlendirilmelidir.

### 4. Havadan eşlik

Amaç, hareketli hava unsurunu veya hava ağının kritik bağlantı geometrisini takip ederek bozunma oluşturmaktır. Hava platformu sürekli, aralıklı veya reaktif yayın yapabilir; irtifa ve yön değişimi parazit etkisini hızlı biçimde değiştirebilir. Bu senaryoda zaman pencereli SINR/SJR, PDR, CCA meşguliyeti, komşuluk değişimi, rota ömrü ve hareketlilik tahmini hatası birlikte izlenmelidir.

## Ölçüm ve sınıflandırma çerçevesi

Karıştırıcı durumu şu şekilde modellenebilir:

\[
S_J \in \{gözlemle, karıştır, sus, yer değiştir, yeniden karıştır\}
\]

Ölçülecek değişkenler:

- Yayın süresi, sessizlik süresi ve görev döngüsü.
- Merkez frekans, bant genişliği, kanal geçişi ve spektral yoğunluk.
- Platform konumu, hız, yön, irtifa ve dönüş oranı.
- PDR, PER, BER, SINR, SJR ve ETX.
- CCA meşgul oranı, ACK başarısızlığı ve yeniden iletim.
- Komşu kaybı, rota kırılması, ağ bölünmesi ve alternatif rota sayısı.
- Tespit edilme süresi ve konumlama hatası.

Doğal hareketlilik ile aktif karıştırmayı ayırmak için RSSI tek başına kullanılmamalıdır. RSSI–PDR tutarlılığı, gürültü/parazit tabanı, SJR/SINR, CCA meşguliyeti ve zaman örüntüsü birlikte incelenmelidir.

## Araştırma matrisi

Deney tasarımında 3 × 3 × 4 faktöriyel çerçeve kullanılabilir:

- Sinyal: dar bant, geniş bant, reaktif/protokol-farkında.
- Platform: sabit yer, araç, hava.
- Yayın: sürekli, aralıklı, yayın-sus-yer değiştir.
- Senaryo: cephe hattı, derin sızma, hedef koruma, havadan eşlik.

Her koşulda şu etkiler raporlanabilir:

\[
[\Delta PDR,\ \Delta SINR,\ \Delta ETX,\ \Delta RTT,\ \Delta rota\ ömrü,\ \Delta kontrol\ yükü]
\]

Ayrıca davranış; etki, gizlenebilirlik ve sürdürülebilirlik boyutlarıyla değerlendirilmelidir.

## Literatür sınırları

Açık literatür, sürekli, reaktif, aldatıcı ve rastgele/periyodik karıştırmanın farklı zaman ve spektrum imzaları oluşturduğunu; hareketli jammerların rota seçimi, bağlantı ömrü ve ağ bölünmesini etkilediğini desteklemektedir. Buna karşılık gerçek çatışma sahalarındaki platform, görev niyeti, yayın gücü ve çoklu jammer koordinasyonu hakkındaki doğrulanabilir açık veri sınırlıdır.

## Kaynakça (APA 7)

Ceviz, O., Sen, S., & Sadioglu, P. (2024). A survey of security in UAVs and FANETs: Issues, threats, analysis of attacks, and solutions. *IEEE Communications Surveys & Tutorials*. https://arxiv.org/pdf/2306.14281.pdf

Pirayesh, H., & Zeng, H. (2022). Jamming attacks and anti-jamming strategies in wireless networks: A comprehensive survey. *IEEE Communications Surveys & Tutorials, 24*(3), 1907–1951. https://doi.org/10.1109/COMST.2022.3158658

Savadatti, S. (2024). An extensive classification of 5G network jamming attacks. *Security and Communication Networks, 2024*, Article 2883082. https://doi.org/10.1155/2024/2883082

Sen, C. (2000). *Digital communications jamming* [Master’s thesis, Naval Postgraduate School]. https://upload.wikimedia.org/wikipedia/commons/9/9f/Digital_communications_jamming._(IA_digitalcommunica1094532961).pdf

Xu, B., Zhang, H., & Lu, M. (2023). Multi-agent modeling and jamming-aware routing protocols for movable-jammer-affected wireless sensor networks. *Sensors, 23*(8), Article 3846. https://doi.org/10.3390/s23083846

Xu, W., Trappe, W., Zhang, Y., & Wood, T. (2005). The feasibility of launching and detecting jamming attacks in wireless networks. In *Proceedings of the 6th ACM International Symposium on Mobile Ad Hoc Networking and Computing* (pp. 46–57). Association for Computing Machinery. https://doi.org/10.1145/1062689.1062697

Yau, K.-L. A., Imran, M., Khan, M. F., & Noor, R. M. (2019). Routing schemes in FANETs: A survey. *Sensors, 20*(1), Article 38. https://doi.org/10.3390/s20010038

Zhang, B., He, R., Wang, S., Yang, S., Hu, T., Li, T., & Xu, Z. (2024). Hybrid ant colony-based inter-cluster routing protocol for FANET. *Scientific Reports, 14*, Article 13945. https://doi.org/10.1038/s41598-024-64454-1

Zhao, M., & Xue, R. (2022). Cognitive-based high robustness frequency hopping strategy for UAV swarms in complex electromagnetic environment. *Wireless Communications and Mobile Computing, 2022*, Article 4139345. https://doi.org/10.1155/2022/4139345
