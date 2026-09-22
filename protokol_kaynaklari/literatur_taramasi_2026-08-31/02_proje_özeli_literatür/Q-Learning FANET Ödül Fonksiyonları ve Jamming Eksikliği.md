# Q-Learning Tabanlı FANET Yönlendirme Protokollerinde Ödül Fonksiyonlarının Durum Matrisi ve RF Karıştırma Eksikliği

> **Akademik mod.** Bu belge, FANET yönlendirme protokollerine ilişkin Q-learning tabanlı
> çalışmalarda kullanılan ödül fonksiyonlarının (reward functions) durum-ödül bileşenlerini
> literatür matrisi halinde karşılaştırır ve RF girişimi/karıştırma (interference/jamming)
> teriminin eksikliğini analiz eder.

---

## İçindekiler

1. [Kavramsal Çerçeve: Q-learning'de S, A, R, Q(s,a)](#1-kavramsal-çerçeve-q-learningde-s-a-r-qsaa)
2. [Mathematics 2022 Derlemesi](#2-mathematics-2022-derlemesi)
3. [Literatür Durum-Ödül Matrisi](#3-literatür-durum-ödül-matrisi)
4. [Ödül Fonksiyonu Taksonomisi](#4-ödül-fonksiyonu-taksonomisi)
5. [Eksik Terim Analizi](#5-eksik-terim-analizi)
6. [Eksikliğin Gerekçelendirilmesi](#6-eksikliğin-gerekçelendirilmesi)
7. [Anti-Jamming RL Literatürü (Karşı Alan)](#7-anti-jamming-rl-literatürü-karşı-alan)
8. [Araştırma Boşluğu Bildirimi](#8-araştırma-boşluğu-bildirimi)
9. [Kaynakça](#kaynakça)

---

## 1. Kavramsal Çerçeve: Q-learning'de S, A, R, Q(s,a)

Q-learning, model-free bir pekiştirmeli öğrenme (reinforcement learning, RL) algoritmasıdır.
FANET yönlendirme bağlamında, temel bileşenler şunlardır ([Sutton & Barto, 2018](https://web.stanford.edu/class/psych209/Readings/SuttonBartoIPRLBook2ndEd.pdf)):

- **Durum (State, \(S\)):** Ağ düğümünün gözlemlediği çevresel durum — komşu listesi,
  link kalitesi, hız, enerji vb.
- **Eylem (Action, \(A\)):** Next-hop (bir sonraki düğüm) seçimi
- **Ödül (Reward, \(R\)):** Seçilen eylemin sonucunda alınan geri besleme — gecikme,
  enerji, ilerleme, link kalitesi vb. metriklerin ağırlıklı toplamı
- **Q-değeri (\(Q(s,a)\)):** Durum-eylem çiftinin uzun vadeli beklenen getirisi

Q-tablosu güncelleme kuralı:

\[
Q_{\text{new}}(s,a) \leftarrow Q_{\text{old}}(s,a) + \alpha \left[ R_{t+1} + \gamma \max_{a'} Q(s_{t+1}, a') - Q_{\text{old}}(s,a) \right]
\]

burada \(\alpha\) öğrenme oranı, \(\gamma\) indirim faktörüdür.

> **"Durum matrisi" kavramı üzerine not:** Q-learning'de formel yapı \(Q(s,a)\) tablosudur.
> Bu belgede "durum matrisi" ifadesiyle, literatürdeki çeşitli FANET yönlendirme çalışmalarının
> kullandığı durum/eylem/ödül bileşenlerini sistematik biçimde karşılaştıran literatür
> matrisi kastedilmektedir. Standart, tek bir evrensel durum matrisi yoktur; her çalışma
> kendi durum ve ödül tasarımını kullanır.

---

## 2. Mathematics 2022 Derlemesi

Lansky et al. (2022), *Mathematics* dergisinde yayımlanan derleme makalesinde FANET'lerde
kullanılan pekiştirmeli öğrenme tabanlı yönlendirme protokollerini sınıflandırmıştır.
Bu sınıflandırma üç ana eksene dayanmaktadır:

1. **Öğrenme algoritması** (Q-learning, DQN, çok-ajanlı RL vb.)
2. **Yönlendirme algoritması** (coğrafi, topoloji-farkında, hibrit vb.)
3. **Veri yayılım süreci** (broadcast, unicast, multicast)

Derlemede incelenen protokoller aşağıda listelenmiştir (MDPI arama özeti ve erişilebilir
metadata üzerinden doğrulanabilen liste; tam metne erişim kısıtlı olduğundan protokol-düzeyi
ödül ayrıntıları erişilebilen birincil/ikincil kaynaklardan derlenmiştir):

| # | Protokol | Öğrenme Algoritması |
|---|---|---|
| 1 | DQN-VR | Deep Q-Network |
| 2 | QTAR | Q-learning |
| 3 | TQNGPSR | Tabular Q-learning + GPSR |
| 4 | QMR | Q-learning |
| 5 | QGeo | Q-learning |
| 6 | QSRP | Q-learning |
| 7 | QLGR | Q-learning (çok-ajanlı) |
| 8 | FEQ-Routing-SA | Federated ELearning Q-routing |
| 9 | Q-FANET | Geliştirilmiş Q-learning |
| 10 | PPMAC+RLSRP | Q-learning + MAC katmanı |
| 11 | PARRoT | Q-learning (zaman-varyalı indirim) |
| 12 | QFL-MOR | Q-learning |
| 13 | 3DQ | 3D Q-learning |
| 14 | ICRA | Q-learning |

Derleme, protokolleri öğrenme algoritması, yönlendirme yaklaşımı ve veri yayılım sürecine
göre sınıflandırmış; ancak protokol düzeyinde ödül fonksiyonu ayrıntıları her zaman
açıkça vermemiştir. Aşağıdaki matrisin ödül bileşenleri, erişilebilen birincil ve ikincil
kaynaklardan derlenmiştir.

---

## 3. Literatür Durum-Ödül Matrisi

Aşağıdaki tablo, Q-learning tabanlı FANET yönlendirme protokollerinin durum (state),
eylem (action) ve ödül (reward) bileşenlerini sistematik biçimde karşılaştırır.

### 3.1. QGeo

| Bileşen | İçerik |
|---|---|
| **State** | Belirtilmemiş (komşu listesi ve mesafe bilgisi ima ediliyor) |
| **Action** | Next-hop seçimi |
| **Reward** | Paket seyahat hızı (distance + packet transmission time tabanlı link metrik) |
| **Link kalitesi** | Yok — "link stability" ve "channel quality" hesaba katılmıyor |
| **Açık RF interference/jamming** | Yok |
| **Kaynak** | [Sharvari et al., 2023](https://arxiv.org/abs/2308.16719) |

### 3.2. RFLQGEO

| Bileşen | İçerik |
|---|---|
| **State** | Belirtilmemiş |
| **Action** | Next-hop seçimi |
| **Reward** | MAC delay, link error, localization error, residual energy, distance progress |
| **Link kalitesi** | Kısmen — link error kullanılıyor |
| **Açık RF interference/jamming** | Yok |
| **Kaynak** | [Sharvari et al., 2023](https://arxiv.org/abs/2308.16719) |

### 3.3. QMR

| Bileşen | İçerik |
|---|---|
| **State** | Belirtilmemiş |
| **Action** | Next-hop seçimi |
| **Reward** | One-hop delay + remaining energy (çok-amaçlı reward fonksiyonu) |
| **Link kalitesi** | Yok — ETX kullanılıyor ancak SIR öneriliyor ama kullanılmıyor |
| **Açık RF interference/jamming** | Yok |
| **Kaynak** | [Sharvari et al., 2023](https://arxiv.org/abs/2308.16719) |

### 3.4. Q-FANET

| Bileşen | İçerik |
|---|---|
| **State** | Belirtilmemiş (kanal koşulları ve residual energy içerdiği belirtilmiş) |
| **Action** | Next-hop seçimi |
| **Reward** | Hedefe direkt götüren linklere yüksek ödül; local minima'ya ceza |
| **Link kalitesi** | Kısmen — Q-learning+ algoritması SINR seviyesini kanal koşulu olarak kullanıyor |
| **Açık RF interference/jamming** | Yok — SINR kullanılıyor ama jamming-aware değil |
| **Kaynak** | [Tho et al., 2025](https://onlinelibrary.wiley.com/doi/full/10.4218/etrij.2024-0298) |

### 3.5. QTAR

| Bileşen | İçerik |
|---|---|
| **State** | İki-hop komşu bilgisi |
| **Action** | Next-hop seçimi |
| **Reward** | Two-hop packet travel speed + two-hop latency + remaining energy |
| **Link kalitesi** | Yok — SINR dahil değil |
| **Açık RF interference/jamming** | Yok |
| **Kaynak** | [Sharvari et al., 2023](https://arxiv.org/abs/2308.16719) |

### 3.6. QLR-FANET

| Bileşen | İçerik |
|---|---|
| **State** | Komşu başına tuple: PER, current load, relative velocity, distance-to-destination farkı, forwarding capability |
| **Action** | Next-hop seçimi |
| **Reward** | LocalReward (0.7 ağırlık) + ActionReward (0.3 ağırlık); local reward = relative velocity + distance + PER + load; action reward = PER + forwarding capability |
| **Link kalitesi** | Evet — PER kullanılıyor |
| **Açık RF interference/jamming** | Yok — PER kullanılıyor ama jamming'e özel değil |
| **Routing void penalty** | Düşük forwarding capability durumunda ceza uygulanır (eşik: 0.9 minimum, 0.30 ceza eşiği) |
| **Retransmission penalty** | 3 deneme sonrası Q-tablo girdisi siliniyor |
| **Kaynak** | [Tho et al., 2025](https://onlinelibrary.wiley.com/doi/full/10.4218/etrij.2024-0298) |

### 3.7. IQMR (Improved Q-learning Multi-hop Routing)

| Bileşen | İçerik |
|---|---|
| **State** | \(S_n = [E^{res}_n, P^{rs}_n, P^{cov}_n, P^{coll}_n]\) — residual energy, packet reception status, coverage probability, collision probability |
| **Action** | Next-hop seçimi |
| **Reward** | \(R = w_1(1-P^{coll}) + w_2 P^{rs}(L3) + w_3 P^{rs}(L2) + w_4 P^{cov} + w_5 E^{res}\) |
| **Link kalitesi** | Evet — SIR/coverage probability kullanılıyor (\(P^{cov} = E[\text{SIR} \geq \theta_{th}]\)) |
| **Açık RF interference/jamming** | Kısmen — SIR ve aggregate interference power kanal modelinde var, ama jamming terimi reward'da değil |
| **Kaynak** | [Sharvari et al., 2023](https://arxiv.org/abs/2308.16719) |

### 3.8. PARRoT

| Bileşen | İçerik |
|---|---|
| **State** | Tahmin edilen gelecekteki pozisyon + link expiry time |
| **Action** | Belirtilmemiş (next-hop seçimi ima ediliyor) |
| **Reward** | **Ödül fonksiyonu kullanılmıyor** — zaman-varyalı indirim faktörü kullanılıyor |
| **Link kalitesi** | Yok |
| **Açık RF interference/jamming** | Yok |
| **Kaynak** | [Tho et al., 2025](https://onlinelibrary.wiley.com/doi/full/10.4218/etrij.2024-0298) |

### 3.9. QSR (Q-learning Secure Routing)

| Bileşen | İçerik |
|---|---|
| **State** | Güvenli komşu keşfi + paket relay davranışı izleme |
| **Action** | Next-hop/route seçimi |
| **Reward** | One-hop delay + hop count + packet loss ratio + TX/RX frequencies |
| **Link kalitesi** | Kısmen — packet loss ratio kullanılıyor |
| **Açık RF interference/jamming** | Yok — güvenlik wormhole attack'lara odaklanmış, jamming'e değil |
| **Kaynak** | [Tho et al., 2025](https://onlinelibrary.wiley.com/doi/full/10.4218/etrij.2024-0298) |

### 3.10. RLGM (Reinforcement Learning Gradient Monitoring)

| Bileşen | İçerik |
|---|---|
| **State** | Belirtilmemiş |
| **Action** | Belirtilmemiş |
| **Reward** | Belirtilmemiş |
| **Amaç** | Jamming saldırılarının tespiti ve ağ bütünlüğünün korunması |
| **Açık RF interference/jamming** | Evet — jammer tespiti için RL kullanılıyor; ancak rota seçimi için değil |
| **Kaynak** | [Tho et al., 2025](https://onlinelibrary.wiley.com/doi/full/10.4218/etrij.2024-0298) |

### 3.11. DQL-AODV

| Bileşen | İçerik |
|---|---|
| **State** | Link life + remaining node capacity (lokal); hop count + average E2E delay (global) |
| **Action** | Daha az hop ve düşük gecikmeli rotaların seçimi |
| **Reward** | Belirtilmemiş |
| **Link kalitesi** | Kısmen — link life kullanılıyor |
| **Açık RF interference/jamming** | Yok |
| **Kaynak** | [Tho et al., 2025](https://onlinelibrary.wiley.com/doi/full/10.4218/etrij.2024-0298) |

### 3.12. Özet Matris

| Protokol | RL Türü | State Değişkenleri | Reward Bileşenleri | Link Kalitesi | Açık Jamming |
|---|---|---|---|---|---|
| QGeo | Q-learning | Belirtilmemiş | Packet travel speed | Yok | Yok |
| RFLQGEO | Q-learning | Belirtilmemiş | MAC delay, link error, energy, distance | Kısmen | Yok |
| QMR | Q-learning | Belirtilmemiş | Delay, energy | Yok (ETX) | Yok |
| Q-FANET | İyileştirilmiş Q-learning | Kanal koşulu, enerji | Hedefe ilerleme, local minima cezası | Kısmen (SINR) | Yok |
| QTAR | Q-learning | İki-hop komşu | Two-hop speed, latency, energy | Yok | Yok |
| QLR-FANET | Q-learning | PER, load, velocity, distance, capability | PER, load, velocity, distance | Evet (PER) | Yok |
| IQMR | Q-learning | Energy, PDR, coverage (SIR), collision | Collision, PDR, coverage, energy | Evet (SIR) | Kısmen (interference) |
| PARRoT | Q-learning (zaman-varyalı) | Pozisyon, link expiry | Ödül yok | Yok | Yok |
| QSR | Q-learning | Güvenli komşu tablosu | Delay, hop count, packet loss, TX/RX freq | Kısmen | Yok |
| RLGM | RL | Belirtilmemiş | Belirtilmemiş | Yok | Evet (jammer tespiti) |
| DQL-AODV | DQL | Link life, capacity, hop count, delay | Belirtilmemiş | Kısmen | Yok |

---

## 4. Ödül Fonksiyonu Taksonomisi

Literatürdeki Q-learning FANET yönlendirme ödül fonksiyonları, aşağıdaki taksonomiye
göre sınıflandırılabilir:

### 4.1. QoS/Mobilite Odaklı Ödüller

Bu kategori, ağ katmanı QoS metriklerini optimize eder:

\[
R = w_1 \cdot f_{\text{delay}} + w_2 \cdot f_{\text{energy}} + w_3 \cdot f_{\text{progress}} + w_4 \cdot f_{\text{mobility}}
\]

- **Geçikme (delay):** QMR, QTAR, QSR
- **Enerji (energy):** QMR, QTAR, RFLQGEO, IQMR
- **İlerleme (progress):** QGeo, Q-FANET, QLR-FANET
- **Mobilite (mobility):** PARRoT (link expiry), QLR-FANET (relative velocity)

### 4.2. Kanal Kalitesi Odaklı Ödüller

Bu kategori, link kalitesi göstergelerini kullanır ama jamming-aware değildir:

\[
R = w_1 \cdot f_{\text{PER}} + w_2 \cdot f_{\text{SINR}} + w_3 \cdot f_{\text{load}}
\]

- **PER:** QLR-FANET
- **SINR/SIR:** Q-FANET (SINR), IQMR (SIR + coverage probability)
- **Yük (load):** QLR-FANET

> **Uyarı:** Bu metrikler kanal kalitesini dolaylı yansıtsa da, karıştırma (jamming)
> kaynaklı bozulmayı açıkça modellemez. PER, jamming olmasa bile zayıf link kalitesinden
> kaynaklanıyor olabilir; SINR ise interferansın doğal bir parçası olsa da jammer gücü
> (\(P_J\)), jammer etki yarıçapı veya JSR gibi EW-spesifik parametreler içermez.

### 4.3. Güvenlik Odaklı Yaklaşımlar (RLGM)

RLGM, jammer tespiti için RL kullanır, ancak rota seçimi için bir ödül fonksiyonu
tanımlamaz. Bu, anti-jamming ile yönlendirme arasındaki yapısal ayrımı gösterir.

---

## 5. Eksik Terim Analizi

### 5.1. Tipik bir Q-learning FANET routing ödül fonksiyonu

Literatürdeki tipik ödül fonksiyonu şu genel yapıya sahiptir:

\[
R(s, a) = w_1 \cdot f_{\text{delay}}(s,a) + w_2 \cdot f_{\text{energy}}(s,a) + w_3 \cdot f_{\text{link}}(s,a) + w_4 \cdot f_{\text{progress}}(s,a)
\]

burada:
- \(f_{\text{delay}}\) — gecikme veya paket seyahat hızı
- \(f_{\text{energy}}\) — residual enerji
- \(f_{\text{link}}\) — PER, SINR/SIR veya ETX gibi link kalitesi göstergesi
- \(f_{\text{progress}}\) — hedefe mesafe azalması

### 5.2. Eksik terim: Jamming-aware ödül bileşeni

Bir RF karıştırma (jamming) modelini açıkça içeren ödül bileşeni şu yapıda olmalıdır:

\[
f_{\text{jam}} = g(\text{SINR}_{\text{under-jamming}}, \text{JSR}, P_J, r_J, \text{PER}_{\text{under-jamming}}, I)
\]

burada:
- \(\text{SINR}_{\text{under-jamming}}\) — karıştırıcı varlığında SINR
- \(\text{JSR}\) — Jamming-to-Signal Ratio (karıştırma gücü / sinyal gücü)
- \(P_J\) — Karıştırıcı iletim gücü
- \(r_J\) — Karıştırıcı etki yarıçapı
- \(\text{PER}_{\text{under-jamming}}\) — Karıştırma altında paket hata oranı
- \(I\) — Toplam interferans gücü

### 5.3. Mevcut durum

| Terim | QGeo | RFLQGEO | QMR | Q-FANET | QTAR | QLR-FANET | IQMR | PARRoT | QSR |
|---|---|---|---|---|---|---|---|---|---|
| Gecikme | Evet | Evet | Evet | Evet | Evet | Kısmen | Evet | Hayır | Evet |
| Enerji | Hayır | Evet | Evet | Hayır | Evet | Hayır | Evet | Hayır | Hayır |
| İlerleme | Evet | Evet | Hayır | Evet | Hayır | Evet | Evet | Hayır | Hayır |
| PER | Hayır | Hayır | Hayır | Hayır | Hayır | Evet | Hayır | Hayır | Hayır |
| SINR/SIR | Hayır | Hayır | Hayır | Kısmen | Hayır | Hayır | Kısmen | Hayır | Hayır |
| JSR | Hayır | Hayır | Hayır | Hayır | Hayır | Hayır | Hayır | Hayır | Hayır |
| \(P_J\) (jammer gücü) | Hayır | Hayır | Hayır | Hayır | Hayır | Hayır | Hayır | Hayır | Hayır |
| \(r_J\) (etki yarıçapı) | Hayır | Hayır | Hayır | Hayır | Hayır | Hayır | Hayır | Hayır | Hayır |
| \(\text{PER}_{\text{jam}}\) | Hayır | Hayır | Hayır | Hayır | Hayır | Hayır | Hayır | Hayır | Hayır |
| Interference | Hayır | Hayır | Hayır | Hayır | Hayır | Hayır | Kısmen | Hayır | Hayır |

> **Sonuç:** İncelenen ve erişilebilir kaynaklarda doğrulanabilen next-hop FANET routing
> çalışmalarında açık jammer-aware terimler — \(P_J\), JSR, jammer konumu, jammer etki
> yarıçapı veya \(\mathrm{PER}_{jam}\) — sistematik biçimde reward fonksiyonuna entegre
> edilmemiştir; ancak PER, SIR/SINR ve link quality gibi örtük kanal kalitesi göstergeleri
> bazı çalışmalarda vardır (QLR-FANET: PER; Q-FANET: SINR; IQMR: SIR/interference).

---

## 6. Eksikliğin Gerekçelendirilmesi

Bu eksiklik, çoğu Q-learning FANET routing çalışmasında açıkça gerekçelendirilmemiştir.
Literatürden çıkarılabilen açıklama, aşağıdaki üç varsayımdan kaynaklanmaktadır:

### 6.1. Ağ katmanı optimizasyonu odak noktası

Q-learning FANET routing çalışmaları, ağ katmanı QoS metriklerini (gecikme, enerji,
PDR, rota stabilitesi) optimize etmeye odaklanır. PHY katmanı EW tehditleri
(SINR, jammer gücü, JSR) ayrı bir problem alanı olarak ele alınır. Bu katmanlı ayrım,
OSI modeline uygun olsa da, EW koşullarında yetersizdir — çünkü jamming etkisi
PHY'den ağ katmanına PER artışı ve bağlantı kopması olarak yayılır ve bu etki rota
seçimine yansımalıdır.

### 6.2. İdealize edilmiş simülasyon varsayımları

Çoğu çalışma, simülasyonda benign (iyi niyetli) kanal koşulları varsayar:

- **Bağlantı modeli:** Mesafe-tabanlı eşik (two-ray ground veya log-distance)
- **Karıştırıcı yok:** Senaryoda jammer tanımlanmaz
- **SINR/SIR:** Yalnızca IQMR ve Q-FANET kullanır; diğerleri kullanmaz
- **PER:** QLR-FANET kullanır ama jamming-bağlamında değil

Bu varsayımlar, EW tehditlerini simülasyon ortamından dışlar ve dolayısıyla ödül
fonksiyonunda jamming terimine ihtiyaç doğurmaz.

### 6.3. Anti-jamming RL'in ayrı bir araştırma alanı olması

Anti-jamming RL literatürü, aşağıdaki bölümlerde incelendiği üzere genellikle
**kanal seçimi, güç kontrolü, frekans atlama veya rol seçimi** düzeyinde çalışır;
FANET next-hop routing ödül fonksiyonuna entegre edilmez. Bu yapısal ayrım,
literatürde açıkça tartışılmamış olsa da, iki alanın ayrı gelişmesinden anlaşılabilir.

### 6.4. Survey'lerin açık problemleri

Lansky et al. (2022) derlemesi, FANET RL routing için şu zorlukları listeler:
- Düğümlerin çok hızlı hareketi
- Sık topoloji değişiklikleri
- Düşük düğüm yoğunluğu

Ancak güvenlik, jamming veya interferens ile ilgili açık bir problem tanımlamamıştır.
Benzer şekilde, Tho et al. (2025), QLR-FANET makalesinde gelecek çalışma olarak
"ek metrik kısıtları" eklemeyi önerir, ancak jamming veya güvenlik spesifik bir
gelecek çalışma kalemi vermez.

---

## 7. Anti-Jamming RL Literatürü (Karşı Alan)

Anti-jamming RL literatürü, FANET routing literatüründen ayrı bir alan olarak
gelişmiştir. Aşağıdaki tablo, bu alanın temel çalışmalarını özetler:

### 7.1. FL-HDQN — Federated Hierarchical DQN

| Bileşen | İçerik |
|---|---|
| **Uygulama** | UAV sürü iletişimi, hiyerarşik MANET |
| **RL türü** | Hierarchical DQN + Federated Learning |
| **Eylem** | Katman 1: Kanal seçimi; Katman 2: Güç + modülasyon-kodlama seçimi |
| **Ödül** | Katman 1: Başarılı iletim = 1, başarısız = 0 (BER < 10⁻⁵); Katman 2: \(\alpha \cdot \text{power} + \beta \cdot \text{modulation}\) |
| **SINR** | Ödülde değil; BER eşiği ile dolaylı |
| **JSR** | Yok |
| **Routing?** | Hayır — kanal/güç/modülasyon seçimi düzeyinde |
| **Kaynak** | [Ni et al., 2025](https://www.mdpi.com/1424-8220/26/1/181) |

### 7.2. QoS ve Jamming-Aware DRL

| Bileşen | İçerik |
|---|---|
| **Uygulama** | General ad-hoc network (FANET değil) |
| **RL türü** | DRL (rol seçimi: TX, RX, CJ, AJ, Wait) |
| **Eylem** | Düğüm rolü seçimi + jamming-aware geometric routing |
| **Ödül** | Throughput (\(N_T\)) + kooperatif jamming (\(N_{CJ}\)) + adversarial jamming (\(N_{AJ}\)) − enerji (\(N_E\)) − delay (\(N_D\)) |
| **SINR** | Evet — \(I(\text{SINR} > \tau)\) iletim/receive ödülünde |
| **JSR** | Yok |
| **Routing?** | Evet — jamming-aware geometric routing (ancak DQN rota seçimi için değil, rol seçimi için) |
| **Kaynak** | [Abuzainab et al., 2019](https://ar5iv.labs.arxiv.org/html/1910.05766) |

### 7.3. DRL Anti-Jamming Channel Selection (UAV)

| Bileşen | İçerik |
|---|---|
| **Uygulama** | UAV FHSS iletişim sistemi |
| **RL türü** | DQN (vanilla) |
| **Eylem** | 16 kanaldan birini seç |
| **Ödül** | \(r = -2 \cdot I\{\text{jammed}\} + \frac{1}{1+\text{BER}} + \beta H(p)\) |
| **SINR** | Kanal modelinde (SNR = \(P_s|h|^2 / (P_n + P_j|h|^2 I_{\text{jammed}})\)) |
| **JSR** | Simülasyon parametresi (0.5, 1.2) ama ödüllü değil |
| **Routing?** | Hayır — kanal seçimi düzeyinde |
| **Kaynak** | [Grekhov et al., 2026](https://arxiv.org/abs/2601.06095) |

### 7.4. DRL Anti-Jamming via Energy Harvesting (UAV Jammer)

| Bileşen | İçerik |
|---|---|
| **Uygulama** | UAV jammer'a maruz kalan ambient backscatter sistemi |
| **RL türü** | DQN |
| **Eylem** | İletişim modu seçimi (idle, AT, EH, AmBC, rate-adapted AT) |
| **Ödül** | Başarıyla teslim edilen paket sayısı (\(d_t, d_n^J, d_m^r\)) |
| **SINR** | Kanal modelinde (\(\theta = P_R / (P_{J,\text{eff}} + \sigma^2)\)) ama ödüllü değil |
| **JSR** | Yok |
| **Routing?** | Hayır — mod seçimi düzeyinde |
| **Kaynak** | [Nguyen et al., 2025](https://arxiv.org/abs/2512.08351) |

### 7.5. Karşılaştırma: Anti-Jamming RL vs FANET Routing RL

| Özellik | FANET Routing RL | Anti-Jamming RL |
|---|---|---|
| **Eylem düzeyi** | Next-hop seçimi | Kanal/güç/modülasyon/mod seçimi |
| **Ödül odağı** | QoS metrikleri (gecikme, enerji, PDR) | İletim başarısı (BER, throughput) |
| **Jamming farkındalığı** | Yok (RLGM hariç) | Evet (BER, SINR, jamming indicator) |
| **Katman** | Ağ katmanı (L3) | PHY/MAC katmanı (L1/L2) |
| **Uygulama alanı** | FANET (çoklu UAV) | Tek UAV veya genel ad-hoc |
| **JSR kullanımı** | Yok | Sınırlı (simülasyon parametresi) |

---

## 8. Araştırma Boşluğu Bildirimi

Mevcut Q-learning tabanlı FANET routing literatürü çoğunlukla gecikme, enerji,
ilerleme, komşu/link kararlılığı ve kısmen PER/SINR gibi kanal kalitesi
göstergelerini optimize eder; ancak jammer gücü (\(P_J\)), JSR, jammer etki
yarıçapı (\(r_J\)), SINR-under-jamming veya EW kaynaklı PER artışını ödül
fonksiyonuna açık terim olarak entegre eden next-hop routing çalışmaları sınırlıdır.

Bu boşluk, aşağıdaki şekilde formüle edilebilir:

**Mevcut tipik ödül fonksiyonu:**
\[
R_{\text{current}} = w_1 f_{\text{delay}} + w_2 f_{\text{energy}} + w_3 f_{\text{link}} + w_4 f_{\text{progress}}
\]

**Önerilen EW-farkındalıklı ödül fonksiyonu:**
\[
R_{\text{proposed}} = w_1 f_{\text{delay}} + w_2 f_{\text{energy}} + w_3 f_{\text{link}} + w_4 f_{\text{progress}} + w_5 \cdot f_{\text{jam}}(\text{SINR}_J, \text{JSR}, P_J, r_J, \text{PER}_J)
\]

burada \(f_{\text{jam}}\), jamming etkisini açıkça modelleyen bir ödül/ceza terimidir.

### 8.1. Önerilen araştırma soruları

1. Jamming-aware bir ödül terimi, FANET routing protokollerinin EW altında PDR ve
   E2E gecikme metriklerini ne kadar iyileştirir?
2. JSR ve jammer etki yarıçapı, next-hop seçim kararını nasıl etkiler?
3. Anti-jamming RL (kanal seçimi) ile jamming-aware routing RL entegre edildiğinde
   sinerjik bir etki oluşur mu?
4. SimPy/NetworkX ortamında, jamming-aware ödül fonksiyonuna sahip bir Q-learning
   routing protokolü, RFC-default AODV/OLSR baseline'ına göre EW koşullarında
   nasıl bir performans gösterir?

---

## Kaynakça (APA 7)

Abuzainab, N., Saad, W., & Poor, H. V. (2019). QoS and jamming-aware wireless networking using deep reinforcement learning. *arXiv preprint arXiv:1910.05766*. https://ar5iv.labs.arxiv.org/html/1910.05766

Arafat, M. Y., & Moh, S. (2021). A Q-learning-based topology-aware routing protocol for flying ad hoc networks. *IEEE Internet of Things Journal*, *9*(3), 1985–2000. https://ieeexplore.ieee.org/document/9412448

da Costa, L. A. L., Kunst, R., & Pignaton de Freitas, E. (2021). Q-FANET: Improved Q-learning based routing protocol for FANETs. *Computer Networks*, *198*, 108379. https://www.sciencedirect.com/science/article/pii/S1389128621003595

Lansky, J., Ali, S., Rahmani, A. M., Yousefpoor, M. S., Yousefpoor, E., Khan, F., & Hosseinzadeh, M. (2022). Reinforcement learning-based routing protocols in flying ad hoc networks (FANET): A review. *Mathematics*, *10*(16), 3017. https://www.mdpi.com/2227-7390/10/16/3017

Nguyen, N.-T., Hoang, T.-T., Hoang, T.-D., & Nguyen, T.-D. (2025). Turning threat into opportunity: DRL-powered anti-jamming via energy harvesting in UAV-disrupted channels. *arXiv preprint arXiv:2512.08351*. https://arxiv.org/abs/2512.08351

Ni, D., Ma, S., Du, J., Wu, Y., Zhou, C., & Xiao, H. (2025). A federated hierarchical DQN-based distributed intelligent anti-jamming method for UAVs. *Sensors*, *26*(1), 181. https://www.mdpi.com/1424-8220/26/1/181

Sutton, R. S., & Barto, A. G. (2018). *Reinforcement learning: An introduction* (2nd ed.). MIT Press. https://web.stanford.edu/class/psych209/Readings/SuttonBartoIPRLBook2ndEd.pdf

Tho, M. C., Ly, N. T. H., Binh, L. H., & Vo, T. T. (2025). QLR-FANET: A Q-learning and rate control-based routing protocol for flying ad hoc networks. *ETRI Journal*. https://onlinelibrary.wiley.com/doi/full/10.4218/etrij.2024-0298

Sharvari, N. P., Das, D., Bapat, J., & Das, D. (2023). Energy efficient UAV-assisted emergency communication with reliable connectivity and collision avoidance. *arXiv preprint arXiv:2308.16719*. https://arxiv.org/abs/2308.16719

Grekhov, A., Kharchenko, V., & Kondratiuk, V. (2026). Deep Q-network based resilient drone communication: Neutralizing first-order Markov jammers. *arXiv preprint arXiv:2601.06095*. https://arxiv.org/abs/2601.06095

---

> **Not:** Bu belge, Q-learning tabanlı FANET routing ödül fonksiyonlarının literatür
> analizini sunar. "Durum matrisi" ifadesi, tek bir evrensel matris değil, çalışmalardaki
> durum/ödül bileşenlerinin sistematik karşılaştırmasını ifade eder. Protokol düzeyinde
> ödül ayrıntıları erişilebilen ikincil kaynaklardan (Sharvari et al., 2023; Tho et al.,
> 2025) derlenmiştir; MDPI tam metnine erişim kısıtlı olduğundan Lansky et al. (2022)
> derlemesinin protokol listesi arama özeti ve metadata üzerinden doğrulanmıştır.
> Anti-jamming RL literatürü ayrı bir alan olarak incelenmiş ve FANET routing ödül
> fonksiyonlarına entegre edilmediği gösterilmiştir.
