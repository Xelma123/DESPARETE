# $N \le 40$ Düğümlü Taktik FANET Simülasyonlarında Kabul Gören Standart Parametreler

> **Akademik mod — Literatür taraması**
>
> Tarih: 31 Ağustos 2026
>
> Kapsam: Küçük ve orta ölçekli ($N \le 40$ düğüm) taktik FANET simülasyonlarında kullanılan standart parametreler
>
> Kaynak sayısı: 11 (hakemli dergi/konferans + resmi simülatör dokümantasyonu)

---

## Özet

FANET literatüründe tek bir resmi standart bulunmamaktadır; aşağıdaki değerler, simülasyon parametre tablolarında tekrarlanan kabul görmüş başlangıç aralıklarıdır ve $N \le 40$ düğüm içeren taktik senaryolar için optimize edilmiştir. Çalışma, beş temel parametre kategorisini kapsamaktadır: Simülasyon Alan Boyutu, 3D Gauss-Markov mobilite modeli parametreleri, İHA hızları, Paket Boyutu ve Taşıma Katmanı Protokolleri.

---

## Parametre Tablosu

| Parametre | Literatürde Kabul Gören Aralık/Değerler | $N \le 40$ Taktik FANET İçin Önerilen Başlangıç Değeri | Notlar | Kaynaklar |
|---|---|---|---|---|
| **Simülasyon Alan Boyutu** | XY: 250×250 m – 2000×2000 m; Z (irtifa): 100–2000 m. Örnek 3D: 400×400×400 m³, 1700×1700×1500 m³, 2000×2000×300 m³, 2000×2000×2000 m³ | 1000×1000×300 m (veya 1000×1000×500 m) | Kompakt taktik/SAR senaryolarında 250–400 m yatay boyut + 100–120 m irtifa yaygındır; geniş alanlı operasyonlarda 1700–2000 m boyut kullanılır. Çoğu çalışma 3D (X, Y, Z) sınırları kullanır | Azevedo et al. (2019); Maakar et al. (2018); Salazar et al. (2022); Wang et al. (2023) |
| **3D Gauss-Markov α (hafıza parametresi)** | 0.25 – 1.0; yaygın olarak 0.75–0.95 arası. ns-3 örnek/varsayılan değeri 0.85; OMNeT++ varsayılanı 0.5; Broyles et al. 0.25, 0.5, 0.85, 0.95 test etmiştir | α = 0.85 | α→0 Brown hareketi (tam rastgele), α→1 doğrusal hareket. 3D FANET için α=0.75–0.95 arası gerçekçi UAV yörüngeleri üretir. α=1.0 tamamen öngörülebilir düz çizgi uçuş anlamına gelir | Broyles et al. (2010); Safaa & Behadili (2025); Mary & Pradeep Kumar (2025); ns-3 Project (n.d.) |
| **3D Gauss-Markov TimeStep (güncelleme aralığı)** | 0.25–5.0 s; yaygın olarak 0.5–1.0 s | 0.5 s | Broyles et al. simülasyonda 5.0 s, küçük adım analizinde 0.25 s kullanmıştır. ns-3 örnek implementasyonunda 0.5 s kullanılır | Broyles et al. (2010); ns-3 Project (n.d.) |
| **3D Gauss-Markov MeanVelocity (ortalama hız)** | Çalışmaya göre değişir: U(0,20), U(10,30), U(800,1200) m/s (hava araçları için) | U(10,30) m/s | FANET için 5–40 m/s arası yaygındır; Broyles et al. 800–1200 m/s (hızlı hava araçları) kullanmıştır. Düşük hızlı SAR için 5–20 m/s, taktik İHA için 10–30 m/s tipiktir | Broyles et al. (2010); Azevedo et al. (2019); Safaa & Behadili (2025) |
| **3D Gauss-Markov MeanDirection** | U(0, 2π) = U(0, 6.283) radyan | U(0, 2π) radyan | Tam yatay açı aralığı; ns-3 ve OMNeT++ implementasyonlarında standarttır | ns-3 Project (n.d.); OMNeT++ (n.d.) |
| **3D Gauss-Markov MeanPitch** | 0.05 (sabit) veya U(0, 0.5) radyan | 0.05 radyan (~2.9°) | Düşük pitch açıları düz uçuşu simüle eder; daha fazla dikey hareket için U(0, 0.5) kullanılabilir. Birçok çalışma pitch parametresini ayrıca belirtmez | ns-3 Project (n.d.); Safaa & Behadili (2025) |
| **İHA Hızları (m/s)** | 5–60 m/s; taktik FANET için 10–30 m/s en yaygın; 0–15 m/s (düşük hız), 10–40 m/s (geniş aralık), 10–60 m/s (yüksek mobilite) | 10–30 m/s | Düşük hızlı SAR: 5–20 m/s; standart taktik: 10–30 m/s; yüksek mobilite testleri: 40–60 m/s. Bazı çalışmalarda sabit hız (20 m/s) kullanılır | Azevedo et al. (2019); Maakar et al. (2018); Wang et al. (2023); Maakar et al. (2025) |
| **Paket Boyutu** | 64–1200 bayt; en yaygın: 512 bayt ve 1000/1024 bayt. Kontrol/enerji çalışmaları: 100–300 bayt | 512 bayt (CBR/UDP için); 1000/1024 bayt (büyük veri/video için) | 512 bayt, MANET/FANET simülasyonlarında "standart kabul" edilen boyuttur; kontrol mesajları için 64–256 bayt, veri/video için 1024–1200 bayt kullanılır | Azevedo et al. (2019); Maakar et al. (2025); Safaa & Behadili (2025); Maakar et al. (2018) |
| **Taşıma Katmanı Protokolleri** | UDP (CBR trafiği ile, baskın); TCP (güvenilir/video akışı için); QUIC (yeni nesil, henüz standart değil) | UDP (CBR ile, yönlendirme/QoS değerlendirmesi için) | FANET yönlendirme protokol değerlendirmelerinde UDP/CBR baskındır. TCP, video akışı/güvenilir iletişim senaryolarında kullanılır. Taktik FANET'te düşük gecikme nedeniyle UDP tercih edilir. Bazı çalışmalar her ikisini karşılaştırır | Azevedo et al. (2019); Maakar et al. (2018); Wang et al. (2023); Salazar et al. (2022); Mary & Pradeep Kumar (2025) |

---

## Detaylı Parametre Açıklamaları

### 1. Simülasyon Alan Boyutu

FANET simülasyonlarında alan boyutu, senaryonun tipine (taktik, SAR, akıllı şehir, askeri) ve İHA sayısına göre büyük ölçüde değişir. $N \le 40$ düğüm içeren çalışmaların incelenmesiyle şu aralıklar tespit edilmiştir:

- **Kompakt senaryolar** (10–20 İHA): 250×250 m'den 400×400 m'ye kadar yatay boyut, 100–120 m irtifa (Salazar et al., 2022; Azevedo et al., 2019)
- **Orta ölçekli taktik senaryolar** (5–25 İHA): 1000×1000 m'den 1700×1700×1500 m³'ye kadar 3D boyut (Maakar et al., 2018)
- **Geniş alanlı operasyonlar** (10–40 İHA): 2000×2000×300 m³'den 2000×2000×2000 m³'ye kadar (Wang et al., 2023; Safaa & Behadili, 2025)

$N \le 40$ taktik FANET için önerilen başlangıç değeri **1000×1000×300 m**'dir; bu değer hem yeterli düğüm yoğunluğu sağlar hem de 3D iletişim dinamiklerini test etmeye olanak tanır.

### 2. 3D Gauss-Markov Mobilite Modeli Parametreleri

3D Gauss-Markov mobilite modeli, FANET simülasyonlarında en sık kullanılan memory-based mobilite modelidir. Broyles et al. (2010) tarafından havacılık ağları için uyarlanmıştır ve ns-3 simülatöründe standart implementasyon olarak yer almaktadır.

Modelin temel denklemi:

$$v_n = \alpha \cdot v_{n-1} + (1-\alpha) \cdot \bar{v} + \sqrt{1-\alpha^2} \cdot x_n$$

burada:
- $\alpha$: hafıza/ayarlama parametresi (0 ≤ α ≤ 1)
- $\bar{v}$: ortalama hız
- $x_n$: sıfır ortalamalı Gaussian rastgele değişken

**α Parametresi:**
- α = 0: Tamamen rastgele (Brown hareketi)
- α = 1: Tamamen doğrusal (öngörülebilir düz çizgi)
- α = 0.85: ns-3 örnek implementasyonunda kullanılan değer; FANET literatüründe en sık karşılaşılan değer
- OMNeT++ varsayılanı: α = 0.5

**TimeStep:** Hız/yön/pitch değerlerinin yeniden hesaplandığı zaman aralığı. ns-3'te yaygın olarak 0.5 s, Broyles et al. simülasyonlarda 5.0 s kullanmıştır.

**MeanDirection:** U(0, 2π) radyan — tam yatay açı aralığı.

**MeanPitch:** 0.05 radyan (~2.9°) — düşük dikey hareket. Daha fazla dikey manevra için U(0, 0.5) radyan kullanılabilir.

### 3. İHA Hızları

FANET simülasyonlarında İHA hızları, İHA tipine ve görev senaryosuna göre değişir:

| Senaryo Tipi | Hız Aralığı | Kaynak |
|---|---|---|
| Düşük hızlı SAR/arama-kurtarma | 5–20 m/s | Mary & Pradeep Kumar (2025); Azevedo et al. (2019) |
| Standart taktik FANET | 10–30 m/s | Safaa & Behadili (2025); Wang et al. (2023) |
| Yüksek mobilite testleri | 40–60 m/s | Maakar et al. (2025) |
| Sabit hız (basitleştirilmiş) | 20 m/s | Safaa & Behadili (2025); Zenodo (2025) |

$N \le 40$ taktik FANET için **10–30 m/s** aralığı önerilir; bu değer tipik orta sınıf taktik İHA'ların (örneğin, Bayraktar TB2 sınıfı) operasyonel hızlarını yansıtır.

### 4. Paket Boyutu

FANET simülasyonlarında paket boyutu, trafik tipine göre seçilir:

| Trafik Tipi | Paket Boyutu | Kullanım Amacı | Kaynak |
|---|---|---|---|
| CBR/UDP (standart) | 512 bayt | Yönlendirme protokol değerlendirme | Maakar et al. (2025); Azevedo et al. (2019) |
| Büyük veri/video | 1000–1024 bayt | Video akışı, görüntü transferi | Maakar et al. (2018); Semantic Scholar (2023) |
| Kontrol/enerji | 100–300 bayt | Kontrol mesajları, enerji optimizasyonu | Mary & Pradeep Kumar (2025) |
| Küçük paket | 64 bayt | Düşük bant genişliği testleri | Libyan Journal (2024) |

512 bayt, MANET/FANET simülasyonlarında "standart kabul" edilen boyuttur ve NS-2, NS-3 ve diğer simülasyon araçlarında varsayılan olarak kullanılır (Maakar et al., 2025).

### 5. Taşıma Katmanı Protokolleri

FANET simülasyonlarında taşıma katmanı protokol seçimi, uygulama gereksinimlerine bağlıdır:

| Protokol | Kullanım Senaryosu | Trafik Tipi | Yaygınlık | Kaynak |
|---|---|---|---|---|
| **UDP** | Yönlendirme protokol değerlendirmesi, QoS metrikleri | CBR (Constant Bit Rate) | En yaygın (baskın) | Azevedo et al. (2019); Maakar et al. (2018); Wang et al. (2023) |
| **TCP** | Güvenilir iletişim, video akışı | Video streaming, dosya transferi | Orta düzey | Salazar et al. (2022); Mary & Pradeep Kumar (2025) |
| **QUIC** | Yeni nesil iletişim | Çoklu yol, düşük gecikme | Gelişmekte olan | ArXiv (2026) |

**Taktik FANET için öneri:** UDP/CBR kombinasyonu, düşük gecikme ve yüksek paket teslim oranı gerektiren taktik senaryolar için en uygun seçimdir. TCP, ağın yüksek mobilitesi nedeniyle bağlantı kopması ve yeniden iletim yükü nedeniyle taktik FANET'te daha az tercih edilir.

---

## Önemli Notlar

- **Tek bir "resmi standart" yoktur:** FANET simülasyon parametreleri, çalışmanın senaryosuna (taktik, SAR, akıllı şehir, askeri), İHA tipine ve kullanılan simülatöre (ns-3, OMNeT++, NS-2) göre değişir. Yukarıdaki değerler literatürde en sık tekrarlanan aralıkları yansıtır.
- **3D Gauss-Markov parametreleri eksik raporlanır:** Birçok FANET çalışması Gauss-Markov mobilite modelini kullandığını belirtir ancak α, TimeStep, MeanPitch gibi alt parametrelerin değerlerini tam olarak vermez. Bu durum literatürde tutarsızlığa yol açar; simülasyon tekrarlanabilirliği için tüm parametrelerin açıkça belirtilmesi önerilir.
- **MAC katmanı bağlamı:** Yukarıdaki kaynakların çoğunda IEEE 802.11a/b/g/n standartları kullanılır; taktik FANET için 802.11n (5 GHz) yaygındır. Bu, tabloda ayrı bir satır olarak yer almamıştır ancak simülasyon kurulumu için kritik bir parametredir.

---

## Kaynaklar (APA 7)

Azevedo, M. I. B. A., Coutinho, C., Toda, E. M., Carvalho, T. C., & Jailton, J. (2019). Wireless communications challenges to flying ad hoc networks. IntechOpen. https://www.intechopen.com/chapters/67574

Broyles, D., Jabbar, A., & Sterbenz, J. P. G. (2010). Design and analysis of a 3-D Gauss-Markov mobility model for highly-dynamic airborne networks. *Proceedings of the International Telemetering Conference, 46*, 388–404.

Maakar, S. K., Singh, Y., & Singh, R. (2018). Performance investigation of OLSR and AODV routing protocols for 3D FANET environment using NS3. *Journal of Communication Engineering & Systems, 8*(2), 1–10.

Maakar, S. K., Sinwar, D., & Kaswan, K. S. (2025). Performance analysis of proactive routing protocols for flying ad-hoc networks using group mobility model. *International Journal of Networked and Distributed Computing, 13*, 31. https://doi.org/10.1007/s44227-025-00073-0

Mary, A. S., & Pradeep Kumar, T. S. (2025). Modeling and simulation of dual-battery FANET system using MADRL for energy optimization. *Scientific Reports, 16*, 821. https://doi.org/10.1038/s41598-025-30429-z

ns-3 Project. (n.d.). *GaussMarkovMobilityModel class reference*. Retrieved August 30, 2026, from https://www.nsnam.org/docs/release/3.9/doxygen/classns3_1_1_gauss_markov_mobility_model.html

OMNeT++. (n.d.). *GaussMarkovMobility*. Retrieved August 30, 2026, from https://doc.omnetpp.org/inet/api-4.2.0/neddoc/inet.mobility.single.GaussMarkovMobility.html

Rohrer, J. P., Cetinkaya, E. K., Narra, H., Broyles, D., Peters, K., & Sterbenz, J. P. G. (2011). AeroRP performance in highly-dynamic airborne networks using 3D Gauss-Markov mobility model. *2011 Military Communications Conference (MILCOM)*, 834–841. https://doi.org/10.1109/MILCOM.2011.6127781

Safaa, A., & Behadili, S. F. (2025). Combining Circular and Gauss-Markov mobility models (CCGM) for FANET enhancement. *Ibn Al-Haitham Journal for Pure and Applied Sciences, 38*(3), 376–389. https://doi.org/10.30526/38.3.4075

Salazar, F., Guamán-Molina, J., Romero-Mediavilla, J., & Arias-Espinoza, C. (2022). Drone collaboration using OLSR protocol in a FANET network for traffic monitoring in a smart city environment. *International Conference on Computer Science, Electronics and Industrial Engineering*. Universidad Autónoma de Madrid.

Wang, H., Li, Y., Zhang, Y., Huang, T., & Jiang, Y. (2023). Arithmetic optimization AOMDV routing protocol for FANETs. *Sensors, 23*(17), 7550. https://doi.org/10.3390/s23177550
