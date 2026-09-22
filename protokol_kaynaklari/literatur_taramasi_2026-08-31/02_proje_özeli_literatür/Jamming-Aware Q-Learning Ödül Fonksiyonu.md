# Karıştırma Farkındalıklı (Jamming-Aware) Q-Learning Yönlendirme Ödül Fonksiyonu — Matematiksel Formülasyon

> **Akademik mod.** Bu belge, tablo tabanlı Q-learning yönlendirme protokollerine
> RF karıştırma seviyesini ve hat kalitesini (SINR/PER) entegre eden bir ödül
> fonksiyonunun matematiksel formülasyonunu sunar. Temel yapı, önceki belgelerde
> tanımlanan RF Karıştırma SINR-PER Soyutlama Modeli ve FANET Yönlendirme
> Protokol Başarım Metrikleri üzerine inşa edilmiştir.

---

## İçindekiler

1. [MDP Formülasyonu](#1-mdp-formülasyonu)
2. [Durum Uzayı (State Space)](#2-durum-uzayı-state-space)
3. [Eylem Uzayı (Action Space)](#3-eylem-uzayı-action-space)
4. [Ödül Fonksiyonu (Reward Function)](#4-ödül-fonksiyonu-reward-function)
5. [Karıştırma Farkındalıklı Terim: f_jam](#5-karıştırma-farkındalıklı-terim-f_jam)
6. [Q-Değer Güncelleme Kuralı](#6-q-değer-güncelleme-kuralı)
7. [Gözlemlenebilirlik ve Tahmin (Oracle Varsayımı Yok)](#7-gözlemlenebilirlik-ve-tahmin-oracle-varsayımı-yok)
8. [Tablo Tabanlı Q-learning için Ayrıklaştırma](#8-tablo-tabanlı-q-learning-için-ayrıklaştırma)
9. [Çok-Hoplu Yol Kalitesi](#9-çok-hoplu-yol-kalitesi)
10. [Opsiyonel: Sert EW Kaçınma Kısıtı](#10-opsiyonel-sert-ew-kaçınma-kısıtı)
11. [SimPy/NetworkX Uygulama Notları](#11-simpynetworkx-uygulama-notları)
12. [Kaynakça](#kaynakça)

---

## 1. MDP Formülasyonu

FANET yönlendirme problemi, bir Markov Karar Süreci (MDP) olarak modellenir.
Bir veri paketi, kaynaktan hedefe (örn. GCS) ulaşana kadar bir "ajan" olarak
davranır; her düğümde next-hop seçerek ilerler ([Sutton & Barto, 2018](https://web.stanford.edu/class/psych209/Readings/SuttonBartoIPRLBook2ndEd.pdf)).

**MDP bileşenleri:**

- **Durum uzayı \(\mathcal{S}\):** Düğüm \(i\)'nin gözlemlediği ağ durumu
- **Eylem uzayı \(\mathcal{A}\):** Komşu düğümlerden birini next-hop olarak seçme
- **Geçiş olasılığı \(\mathcal{P}\):** \(P(s' | s, a)\) — eylem \(a\) sonrası yeni durum
- **Ödül fonksiyonu \(\mathcal{R}\):** \(R(s, a)\) — eylem sonrası alınan ödül
- **İndirim faktörü \(\gamma \in [0, 1]\):** Gelecek ödüllerin ağırlığı

---

## 2. Durum Uzayı (State Space)

### 2.1. Tanım

Düğüm \(i\)'den candidate next-hop \(j\)'ye geçiş anındaki durum vektörü:

\[
s_t = \big( \Delta d_{ij}, \, E^{res}_j, \, \text{PER}_{ij}, \, \widehat{\text{SINR}}_{ij}, \, \widehat{\text{JSR}}_{ij}, \, \rho_j, \, q_j \big)
\]

burada:

| Bileşen | Tanım | Birim |
|---|---|---|
| \(\Delta d_{ij}\) | Hedefe mesafe azalışı: \(d(i, \text{GCS}) - d(j, \text{GCS})\) | m |
| \(E^{res}_j\) | Düğüm \(j\)'nin normalize kalan enerjisi | [0, 1] |
| \(\text{PER}_{ij}\) | Link \((i,j)\)'nin paket hata oranı (link-layer'dan ölçülen) | [0, 1] |
| \(\widehat{\text{SINR}}_{ij}\) | Link \((i,j)\)'nin tahmini SINR değeri | dB |
| \(\widehat{\text{JSR}}_{ij}\) | Link \((i,j)\)'nin tahmini karıştırma-sinyal oranı | dB |
| \(\rho_j\) | Düğüm \(j\)'nin karıştırıcı etki alanında olma olasılığı | [0, 1] |
| \(q_j\) | Düğüm \(j\)'nin normalize kuyruk yükü: \(Q_j / Q_{\max}\) | [0, 1] |

### 2.2. Karıştırma ile ilgili durum değişkenleri

\(\widehat{\text{SINR}}_{ij}\), \(\widehat{\text{JSR}}_{ij}\) ve \(\rho_j\) değişkenleri,
ajanın doğrudan jammer parametrelerini bilmek zorunda olmadığı, ölçü/tahmin tabanlı
değerlerdir (Bölüm 7'de açıklanmıştır).

---

## 3. Eylem Uzayı (Action Space)

\[
\mathcal{A}(i) = \{ j \in \mathcal{N}(i) \}
\]

burada \(\mathcal{N}(i)\), düğüm \(i\)'nin mevcut komşu kümesidir. Ajan, bir komşuyu
next-hop olarak seçer. Eylem uzayı, topoloji değiştikçe dinamik olarak güncellenir.

---

## 4. Ödül Fonksiyonu (Reward Function)

### 4.1. Genel yapı

Ödül fonksiyonu, **toplanabilir (additive)** ve **normalize edilmiş** bileşenlerden
oluşur. Tüm bileşenler \([0, 1]\) aralığına normalize edilir ve ağırlıklar
\(\sum w_k = 1\) olacak şekilde seçilir. Cezalar (penalties) negatif işaretle
çıkarılır:

\[
R_{ij}(t) = w_p \cdot f_{\text{prog}}(i,j) + w_e \cdot f_{\text{energy}}(j) + w_l \cdot f_{\text{link}}(i,j) - w_q \cdot f_{\text{queue}}(j) - w_j \cdot f_{\text{jam}}(i,j)
\]

burada:
- \(w_p, w_e, w_l, w_q, w_j \geq 0\), \(\sum w_k = 1\)
- Tüm \(f_k \in [0, 1]\)

### 4.2. Bileşen tanımları

#### 4.2.1. İlerleme ödülü

\[
f_{\text{prog}}(i,j) = \frac{\max\big(0, \, d(i, \text{GCS}) - d(j, \text{GCS})\big)}{d(i, \text{GCS}) + \epsilon}
\]

Hedefe yaklaşan düğümler yüksek ödül alır. Hedeften uzaklaşan düğümler için ödül 0'dır
([Tho et al., 2025](https://onlinelibrary.wiley.com/doi/full/10.4218/etrij.2024-0298)).

#### 4.2.2. Enerji ödülü

\[
f_{\text{energy}}(j) = \frac{E^{res}_j}{E_{\max}}
\]

Kalan enerjisi yüksek olan düğüm tercih edilir ([Sharvari et al., 2023](https://arxiv.org/abs/2308.16719)).

#### 4.2.3. Link kalitesi ödülü

\[
f_{\text{link}}(i,j) = 1 - \widehat{\text{PER}}_{ij}
\]

Düşük PER'e sahip linkler tercih edilir. \(\widehat{\text{PER}}_{ij}\), EWMA
(exponentially weighted moving average) ile link-layer ACK/NACK istatistiklerinden
tahmin edilir ([Tho et al., 2025](https://onlinelibrary.wiley.com/doi/full/10.4218/etrij.2024-0298)):

\[
\widehat{\text{PER}}_{ij}(t) = (1 - \beta) \cdot \widehat{\text{PER}}_{ij}(t-1) + \beta \cdot \mathbb{1}\{\text{NACK}_{ij}(t)\}
\]

burada \(\beta \in (0, 1]\) EWMA güncelleme oranıdır (tipik \(\beta = 0.1\)).

#### 4.2.4. Kuyruk yükü cezası

\[
f_{\text{queue}}(j) = \frac{Q_j}{Q_{\max}}
\]

Kuyruğu dolu düğümlerden kaçınılır.

#### 4.2.5. Karıştırma cezası (YENİ — Bölüm 5)

\[
f_{\text{jam}}(i,j) = \lambda_1 \cdot \widehat{\text{JSR}}^{(n)}_{ij} + \lambda_2 \cdot \Delta\text{PER}^{J}_{ij} + \lambda_3 \cdot P_{\text{out},ij} + \lambda_4 \cdot \rho_j
\]

burada \(\lambda_1 + \lambda_2 + \lambda_3 + \lambda_4 = 1\) ve tüm bileşenler \([0, 1]\)
aralığına normalize edilmiştir. \(\Delta\text{PER}^{J}_{ij}\), karıştırmadan kaynaklanan
ek PER artışı ve \(\rho_j\), düğüm \(j\)'nin karıştırıcı etkisi altında olma tahmidir.

---

## 5. Karıştırma Farkındalıklı Terim: f_jam

### 5.1. Link düzeyinde SINR (karıştırıcı altında)

Düğüm \(i\)'den \(j\)'ye iletim sırasında, alıcı \(j\)'deki SINR
([RF Jamming SINR-PER Modeli](https://www.perplexity.ai/projects/iha-WDGBzwRYQCibQ8Lqr.z_9Q)):

\[
\text{SINR}^{J}_{ij} = \frac{P_{i \to j}}{N_0 B + I_j + J_j}
\]

burada:
- \(P_{i \to j}\): Düğüm \(i\)'den \(j\)'ye alınan sinyal gücü (mW)
- \(N_0 B\): Termal gürültü gücü (mW)
- \(I_j\): Diğer meşru kullanıcıların girişimi (mW)
- \(J_j\): Alıcı \(j\)'deki toplam karıştırma gücü (mW)

dB cinsinden:

\[
\text{SINR}^{J}_{ij}[\text{dB}] = 10 \log_{10} \left( \frac{P_{i \to j}}{N_0 B + I_j + J_j} \right)
\]

### 5.2. Jamming-to-Signal Ratio (JSR)

\[
\text{JSR}_{ij} = \frac{J_j}{P_{i \to j}}
\]

dB cinsinden:

\[
\text{JSR}_{ij}[\text{dB}] = 10 \log_{10} \left( \frac{J_j}{P_{i \to j}} \right)
\]

Karıştırma baskın olduğunda (\(J_j \gg N_0 B\)):

\[
\text{SINR}^{J}_{ij} \approx \text{SNR}_{ij} - \text{JSR}_{ij} \quad (\text{dB cinsinden})
\]

### 5.3. Normalize JSR

JSR değerini \([0, 1]\) aralığına normalize etmek için sigmoid fonksiyonu kullanılır:

\[
\widehat{\text{JSR}}^{(n)}_{ij} = \frac{1}{1 + \exp\big(-c \cdot (\text{JSR}_{ij}[\text{dB}] - \text{JSR}_0)\big)}
\]

burada:
- \(c\): Geçiş eğriliği (tipik \(c = 1\))
- \(\text{JSR}_0\): Geçiş noktası (tipik \(\text{JSR}_0 = 0\) dB, yani karıştırma gücü sinyal gücüne eşit olduğunda)

### 5.4. Karıştırma altında PER

Lojistik (sigmoid) PER modeli kullanılarak ([RF Jamming SINR-PER Modeli](https://www.perplexity.ai/projects/iha-WDGBzwRYQCibQ8Lqr.z_9Q)):

\[
\text{PER}^{J}_{ij} = \frac{1}{1 + \exp\big(a \cdot (\text{SINR}^{J}_{ij} - \gamma_0)\big)}
\]

burada:
- \(a\): PER-SINR eğrisinin eğriliği (tipik \(a = 2\))
- \(\gamma_0\): SINR geçiş noktası (tipik \(\gamma_0 = 4\) dB, 802.11b 1 Mbps BPSK için)
- \(\text{SINR}^{J}_{ij}\): dB cinsinden, Bölüm 5.1'de tanımlı

### 5.5. Outage olasılığı

Link \((i,j)\)'nin kullanılamaz (outage) olma olasılığı:

\[
P_{\text{out},ij} = \mathbf{1}\left\{ \text{SINR}^{J}_{ij} < \gamma_{\text{th}} \right\}
\]

veya Rayleigh sönümlemesi altında yumuşak bir tahmin:

\[
P_{\text{out},ij} = 1 - \exp\left( -\frac{\gamma_{\text{th}}}{\bar{\gamma}_{ij}} \right)
\]

burada \(\bar{\gamma}_{ij}\), link \((i,j)\)'nin ortalama SINR değeridir ve
\(\gamma_{\text{th}}\), iletişim için minimum SINR eşiğidir (tipik 4–6 dB).

### 5.6. Karıştırıcı yakınlık göstergesi

Düğüm \(j\)'nin karıştırıcı etki yarıçapı içinde olup olmadığı:

\[
\mathbf{1}\{d(j, J) \leq R_J\}
\]

burada:
- \(d(j, J)\): Düğüm \(j\) ile karıştırıcı \(J\) arasındaki mesafe
- \(R_J\): Karıştırıcı etki yarıçapı

Karıştırıcı etki yarıçapı ([RF Jamming SINR-PER Modeli](https://www.perplexity.ai/projects/iha-WDGBzwRYQCibQ8Lqr.z_9Q)):

\[
R_J = \left( \frac{P_J \cdot K}{J_{\text{req}}} \right)^{1/n}
\]

burada:
- \(P_J\): Karıştırıcı iletim gücü
- \(K\): Anten kazançları ve sabit kayıplar
- \(n\): Yol kaybı üssü
- \(J_{\text{req}} = \frac{P_{i \to j}}{\gamma_{\text{th}}} - N_0 B\): Minimum gerekli karıştırma gücü

### 5.7. Tam f_jam formülü

\[
f_{\text{jam}}(i,j) = \lambda_1 \cdot \underbrace{\frac{1}{1 + \exp\big(-c \cdot (\text{JSR}_{ij} - \text{JSR}_0)\big)}}_{\text{normalize JSR}} + \lambda_2 \cdot \underbrace{\frac{1}{1 + \exp\big(a \cdot (\text{SINR}^{J}_{ij} - \gamma_0)\big)}}_{\text{PER under jamming}} + \lambda_3 \cdot \underbrace{P_{\text{out},ij}}_{\text{outage}} + \lambda_4 \cdot \underbrace{\mathbf{1}\{d(j, J) \leq R_J\}}_{\text{jammer proximity}}
\]

burada \(\lambda_1 + \lambda_2 + \lambda_3 + \lambda_4 = 1\).

### 5.8. Önerilen varsayılan ağırlıklar

| Bileşen | Simge | Önerilen ağırlık | Gerekçe |
|---|---|---|---|
| Normalize JSR | \(\lambda_1\) | 0.25 | Karıştırma gücünün sinyal gücüne oranı |
| PER under jamming | \(\lambda_2\) | 0.35 | Doğrudan paket başarısızlığına etki |
| Outage olasılığı | \(\lambda_3\) | 0.25 | Link tamamen kullanılamaz durumu |
| Jammer proximity | \(\lambda_4\) | 0.15 | Önleyici kaçınma |

| Ödül bileşeni | Simge | Önerilen ağırlık |
|---|---|---|
| İlerleme | \(w_p\) | 0.25 |
| Enerji | \(w_e\) | 0.10 |
| Link kalitesi | \(w_l\) | 0.25 |
| Kuyruk cezası | \(w_q\) | 0.10 |
| Karıştırma cezası | \(w_j\) | 0.30 |

> **Not:** Karıştırma cezasına ayrılan 0.30 ağırlık, EW koşullarında karıştırma
> etkisinin QoS metriklerinden daha baskın olduğunu yansıtır. Karıştırma yoksa
> (\(f_{\text{jam}} = 0\)), ödül fonksiyonu standart Q-learning routing ödülüne
> indirgenir.

---

## 6. Q-Değer Güncelleme Kuralı

Tablo tabanlı Q-learning güncelleme kuralı:

\[
Q_{t+1}(s_i, j) \leftarrow Q_t(s_i, j) + \alpha \left[ R_{ij}(t) + \gamma \max_{k \in \mathcal{N}(j)} Q_t(s_j, k) - Q_t(s_i, j) \right]
\]

burada:
- \(\alpha \in (0, 1]\): Öğrenme oranı (tipik \(\alpha = 0.7\))
- \(\gamma \in [0, 1]\): İndirim faktörü (tipik \(\gamma = 0.4\)–0.9)
- \(R_{ij}(t)\): Bölüm 4'te tanımlanan karıştırma-farkındalıklı ödül
- \(\max_{k \in \mathcal{N}(j)} Q_t(s_j, k)\): Bir sonraki durumda en iyi eylemin Q-değeri

**Önemli:** \(\max Q(s_j, k)\) terimi, downstream path kalitesini zaten içerir.
Bu nedenle, tek-hopluk \(R_{ij}\) yeterlidir; ayrıca bir "end-to-end SINR" hesabına
gerek yoktur (Bölüm 9'a bakınız).

### 6.1. Eylem seçimi: \(\epsilon\)-greedy politika

\[
a_t = \begin{cases}
\arg\max_{j \in \mathcal{N}(i)} Q(s_i, j), & \text{olasılık } 1 - \epsilon \\
\text{rastgele } j \in \mathcal{N}(i), & \text{olasılık } \epsilon
\end{cases}
\]

burada \(\epsilon \in [0, 1]\) keşif (exploration) oranıdır. \(\epsilon\) genellikle
zamanla azalır: \(\epsilon_t = \max(\epsilon_{\min}, \, \epsilon_0 \cdot \eta^t)\)
(\(\eta < 1\)).

---

## 7. Gözlemlenebilirlik ve Tahmin (Oracle Varsayımı Yok)

### 7.1. İlke: Ajan jammer parametrelerini doğrudan bilmez

Karıştırıcı gücü \(P_J\), konumu veya etki yarıçapı \(R_J\) yalnızca simülatör
motoru tarafından bilinir. Yönlendirme ajanı bunlara doğrudan erişemez.
Bunun yerine, aşağıdaki ölçülebilir/tahmin edilebilir değerleri kullanır:

### 7.2. PER tahmini (link-layer)

\[
\widehat{\text{PER}}_{ij}(t) = (1 - \beta) \cdot \widehat{\text{PER}}_{ij}(t-1) + \beta \cdot \mathbb{1}\{\text{NACK}_{ij}(t)\}
\]

- Kaynak: MAC katmanı ACK/NACK geri bildirimi
- Kullanılan: \(f_{\text{link}}\) bileşeninde ve \(f_{\text{jam}}\)'de dolaylı olarak

### 7.3. SINR tahmini (PHY/cross-layer)

SINR, iki yolla tahmin edilebilir:

**Yöntem 1 — PER'den tersine çevirme:**

Lojistik PER modelini ters çevirerek SINR tahmini:

\[
\widehat{\text{SINR}}_{ij} = \gamma_0 + \frac{1}{a} \ln\left( \frac{1}{\widehat{\text{PER}}_{ij}} - 1 \right)
\]

**Yöntem 2 — RSSI tabanlı:**

Eğer alıcı RSSI ölçümü yapabiliyorsa:

\[
\widehat{\text{SINR}}_{ij} = \text{RSSI}_{ij} - \widehat{I}_{j} - N_0 B
\]

burada \(\widehat{I}_j\), dinleme (sensing) ile ölçülen toplam girişim gücüdür.

### 7.4. JSR tahmini

JSR, doğrudan ölçülemez ancak SINR ve SNR farkından tahmin edilebilir:

\[
\widehat{\text{JSR}}_{ij} \approx \text{SNR}_{ij} - \widehat{\text{SINR}}_{ij} \quad (\text{dB})
\]

burada:
- \(\text{SNR}_{ij}\): Karıştırma yokken ölçülen/tahmin edilen SNR
- \(\widehat{\text{SINR}}_{ij}\): Mevcut ölçülen SINR

Eğer karıştırıcı aktif değilse, \(\text{JSR} \approx 0\) ve \(f_{\text{jam}} \approx 0\).

### 7.5. Jammer yakınlık tahmini (\(\rho_j\))

Düğüm \(j\)'nin karıştırıcı etkisi altında olma olasılığı, ani PER artışından
tespit edilebilir. Ajan bu bilgiyi jammer konumu bilmeden elde eder:

\[
\rho_j = \sigma\left( \frac{\widehat{\text{PER}}_{ij}(t) - \widehat{\text{PER}}_{ij}^{\text{baseline}}}{\tau_{\text{PER}}} \right)
\]

burada:
- \(\widehat{\text{PER}}_{ij}^{\text{baseline}}\): Karıştırma yokken ölçülen PER
- \(\tau_{\text{PER}}\): PER artış eşiği (tipik 0.1)
- \(\sigma(\cdot)\): Sigmoid fonksiyonu

Bu yaklaşım, karıştırıcının varlığını jammer konumu bilmeden tespit etmeye çalışır;
jammer konumu yalnızca simülatör tarafından bilinir ve \(R_J\) hesabında kullanılır,
ama ajan bu bilgiyi doğrudan kullanmaz — bunun yerine \(\rho_j\) ve
\(\widehat{\text{JSR}}_{ij}\) gibi ölçülebilir göstergeleri kullanır.

---

## 8. Tablo Tabanlı Q-learning için Ayrıklaştırma

Tablo tabanlı Q-learning, sürekli durum değişkenlerini ayrık (discrete) değerlere
bölmeyi gerektirir. Aksi takdirde Q-tablosu pratik bir boyuta ulaşamaz.

### 8.1. Ayrıklaştırma şeması

| Değişken | Sürekli aralık | Ayrık seviye sayısı | Bölmeler |
|---|---|---|---|
| \(\Delta d_{ij}\) (m) | \([-500, 500]\) | 5 | \(\{-500\!-\!200, \ldots, 200\!-\!500\}\) |
| \(E^{res}_j\) | \([0, 1]\) | 3 | \(\{0\!-\!0.33, 0.33\!-\!0.67, 0.67\!-\!1\}\) |
| \(\text{PER}_{ij}\) | \([0, 1]\) | 4 | \(\{0\!-\!0.1, 0.1\!-\!0.3, 0.3\!-\!0.6, 0.6\!-\!1\}\) |
| \(\widehat{\text{SINR}}_{ij}\) (dB) | \([-10, 30]\) | 5 | \(\{-10\!-\!0, 0\!-\!5, 5\!-\!10, 10\!-\!20, 20\!-\!30\}\) |
| \(\widehat{\text{JSR}}_{ij}\) (dB) | \([-20, 20]\) | 4 | \(\{-20\!-\!-5, -5\!-\!0, 0\!-\!5, 5\!-\!20\}\) |
| \(q_j\) | \([0, 1]\) | 3 | \(\{0\!-\!0.33, 0.33\!-\!0.67, 0.67\!-\!1\}\) |

### 8.2. Q-tablosu boyutu

Toplam durum sayısı (en kötü durum):

\[
|S| = 5 \times 3 \times 4 \times 5 \times 4 \times 3 = 3,600
\]

Her düğüm için: \(|S| \times |\mathcal{A}(i)|\) boyutunda Q-tablosu.
\(N = 40\) düğüm için ortalama komşu sayısı \(\bar{d} \approx 6\) ise:

\[
\text{Toplam Q-tablosu} = 40 \times 3,600 \times 6 \approx 864,000 \text{ giriş}
\]

Bu, tablo tabanlı Q-learning için yönetilebilir bir boyuttur. Bellek gereksinimi:
~7 MB (double precision).

> **Not:** Daha fazla ayrıklaştırma seviyesi daha yüksek çözünürlük sağlar ama
> Q-tablosu boyutunu ve öğrenme süresini artırır. Yukarıdaki şema, N≤40 düğümlü
> taktik FANET için önerilen başlangıç noktasıdır.

---

## 9. Çok-Hoplu Yol Kalitesi

### 9.1. Link düzeyi SINR yeterlidir

Q-learning'in bootstrapping yapısı sayesinde, \(\max_k Q(s_j, k)\) terimi
downstream path kalitesini zaten içerir. Bu nedenle, tek-hopluk \(R_{ij}\) ve
\(\text{SINR}^{J}_{ij}\) yeterlidir; ayrıca bir "end-to-end SINR" hesabına
gerek yoktur.

### 9.2. Yol düzeyinde PER (analiz için)

Eğer analiz amaçlı yol düzeyinde PER hesaplanmak istenirse:

\[
\text{PER}_{\text{path}} = 1 - \prod_{\ell \in \text{path}} (1 - \text{PER}^{J}_{\ell})
\]

ve yol düzeyinde PDR:

\[
\text{PDR}_{\text{path}} = \prod_{\ell \in \text{path}} (1 - \text{PER}^{J}_{\ell}) = \prod_{\ell \in \text{path}} \text{PDR}_{\ell}
\]

Bu formül, yol boyunca her linkin bağımsız olarak hata yapma olasılığını
varsayar. Bu, Q-learning'in \(\max Q(s', a')\)'nin içermediği bir bilgidir;
ancak öğrenme süreci bunu örtük olarak öğrenir.

---

## 10. Opsiyonel: Sert EW Kaçınma Kısıtı

Taktik senaryolarda, belirli bir SINR eşiğinin altındaki linklerin tamamen
kaçınılması gerekebilir. Bu, bir "sert kapı" (hard gate) olarak modellenir:

\[
R_{ij}^{\text{final}} = R_{ij} - C_{\text{drop}} \cdot \mathbf{1}\left\{ \widehat{\text{SINR}}^{J}_{ij} < \gamma_{\min} \right\}
\]

burada:
- \(C_{\text{drop}}\): Büyük bir ceza sabiti (örn. \(C_{\text{drop}} = 10\))
- \(\gamma_{\min}\): Minimum izin verilen SINR eşiği (örn. \(\gamma_{\min} = 0\) dB)

Bu yaklaşım, düşük SINR'li linkleri "yasaklı" bölgeye iter ve ajanın bu linkleri
denemesini engeller. Ancak, çok agresif bir \(C_{\text{drop}}\) değeri, ajanın
keşif yapmasını engelleyebilir ve yerel optimuma takılmasına yol açabilir.

> **Uyarı:** Çarpımsal (multiplicative) ödül formülü — \(R_{ij} \cdot (1 - \rho \cdot f_{\text{jam}})\)
> — yalnızca \(R_{ij} \geq 0\) olduğunda kullanılmalıdır. \(R_{ij}\) negatif
> olduğunda, çarpımsal formül negatif cezayı azaltabilir (işaret hatası).

---

## 11. SimPy/NetworkX Uygulama Notları

### 11.1. Veri yapısı

```python
import numpy as np
from collections import defaultdict

class JammingAwareQLearning:
    def __init__(self, n_nodes, config):
        self.alpha = config.get('alpha', 0.7)
        self.gamma = config.get('gamma', 0.4)
        self.epsilon = config.get('epsilon', 0.3)
        self.epsilon_min = config.get('epsilon_min', 0.01)
        self.epsilon_decay = config.get('epsilon_decay', 0.995)
        
        # Ağırlıklar
        self.w = {
            'prog': 0.25, 'energy': 0.10, 'link': 0.25,
            'queue': 0.10, 'jam': 0.30
        }
        
        # f_jam alt-ağırlıkları
        self.lam = {'jsr': 0.25, 'per': 0.35, 'outage': 0.25, 'proximity': 0.15}
        
        # PER modeli parametreleri
        self.gamma_0 = 4.0    # SINR geçiş noktası (dB)
        self.a_log = 2.0      # PER eğriliği
        self.c_jsr = 1.0      # JSR eğriliği
        self.jsr_0 = 0.0      # JSR geçiş noktası (dB)
        self.gamma_th = 6.0   # SINR eşiği (dB)
        self.beta_ewma = 0.1  # PER EWMA oranı
        
        # Ayrıklaştırma bölmeleri
        self.sinr_bins = [-10, 0, 5, 10, 20, 30]
        self.per_bins = [0, 0.1, 0.3, 0.6, 1.0]
        self.jsr_bins = [-20, -5, 0, 5, 20]
        
        # Q-tablosu: Q[state_key][action] = value
        self.Q = defaultdict(lambda: defaultdict(float))
        
        # PER tahminleri (EWMA)
        self.per_est = defaultdict(float)  # per_est[(i,j)] = EWMA PER
        
    def discretize(self, sinr, per, jsr, energy, queue_load, delta_d):
        """Sürekli değerleri ayrık duruma dönüştür."""
        sinr_bin = np.digitize(sinr, self.sinr_bins)
        per_bin = np.digitize(per, self.per_bins)
        jsr_bin = np.digitize(jsr, self.jsr_bins)
        energy_bin = int(energy * 3)  # 3 seviye
        queue_bin = int(queue_load * 3)  # 3 seviye
        prog_bin = np.digitize(delta_d, [-500, -200, 0, 200, 500])
        return (sinr_bin, per_bin, jsr_bin, energy_bin, queue_bin, prog_bin)
    
    def compute_f_jam(self, sinr_j, jsr, per_jam, outage, in_jamming_radius):
        """Karıştırma farkındalıklı ceza terimi."""
        jsr_norm = 1.0 / (1.0 + np.exp(-self.c_jsr * (jsr - self.jsr_0)))
        per_jam_val = 1.0 / (1.0 + np.exp(self.a_log * (sinr_j - self.gamma_0)))
        
        f_jam = (self.lam['jsr'] * jsr_norm +
                 self.lam['per'] * per_jam_val +
                 self.lam['outage'] * outage +
                 self.lam['proximity'] * in_jamming_radius)
        return min(f_jam, 1.0)
    
    def compute_reward(self, i, j, gcs_pos, node_states, link_metrics):
        """Tam ödül fonksiyonu."""
        # İlerleme
        d_i = node_states['dist_to_gcs'][i]
        d_j = node_states['dist_to_gcs'][j]
        f_prog = max(0, d_i - d_j) / (d_i + 1e-6)
        
        # Enerji
        f_energy = node_states['energy'][j]
        
        # Link kalitesi (PER tabanlı)
        per_ij = self.per_est[(i, j)]
        f_link = 1.0 - per_ij
        
        # Kuyruk
        f_queue = node_states['queue_load'][j]
        
        # Karıştırma (simülatörden veya tahminden)
        sinr_j = link_metrics['sinr'][i, j]  # Karıştırıcı altında SINR
        jsr = link_metrics['jsr'][i, j]
        outage = 1.0 if sinr_j < self.gamma_th else 0.0
        in_radius = link_metrics['in_jamming_radius'][j]
        
        f_jam = self.compute_f_jam(sinr_j, jsr, per_ij, outage, in_radius)
        
        # Toplam ödül
        R = (self.w['prog'] * f_prog +
             self.w['energy'] * f_energy +
             self.w['link'] * f_link -
             self.w['queue'] * f_queue -
             self.w['jam'] * f_jam)
        
        return R
    
    def update(self, state_i, action_j, reward, state_j, neighbors_j):
        """Q-değer güncelleme."""
        if neighbors_j:
            max_q = max(self.Q[state_j][k] for k in neighbors_j)
        else:
            max_q = 0.0
        
        old_q = self.Q[state_i][action_j]
        self.Q[state_i][action_j] = old_q + self.alpha * (
            reward + self.gamma * max_q - old_q
        )
    
    def select_action(self, state_i, neighbors):
        """epsilon-greedy eylem seçimi."""
        if not neighbors:
            return None
        if np.random.random() < self.epsilon:
            return np.random.choice(neighbors)
        else:
            q_values = {n: self.Q[state_i][n] for n in neighbors}
            return max(q_values, key=q_values.get)
    
    def decay_epsilon(self):
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
```

### 11.2. PER EWMA güncellemesi

Her iletim denemesinden sonra:

```python
def update_per_estimate(self, i, j, ack_received):
    """Link-layer ACK/NACK'tan PER tahminini güncelle."""
    nack = 0.0 if ack_received else 1.0
    self.per_est[(i, j)] = ((1 - self.beta_ewma) * self.per_est[(i, j)] 
                            + self.beta_ewma * nack)
```

### 11.3. SimPy entegrasyonu

Ödül fonksiyonu, her paket iletisinden sonra çağrılır:

```python
def on_packet_forwarded(self, env, i, j, packet, routing):
    """Paket iletildiğinde Q-learning güncellemesi."""
    # Link-layer sonucu
    ack_received = packet.get('ack', False)
    self.update_per_estimate(i, j, ack_received)
    
    # Durumu ayrıklaştır
    state_i = self.discretize(...)
    
    # Ödülü hesapla
    reward = self.compute_reward(i, j, ...)
    
    # Sonraki durum
    state_j = self.discretize(...)
    neighbors_j = routing.get_neighbors(j)
    
    # Q-tablosunu güncelle
    self.update(state_i, j, reward, state_j, neighbors_j)
    
    # Epsilon'u azalt
    self.decay_epsilon()
```

---

## 12. Özet

### Formülasyon özeti

\[
\boxed{
R_{ij}(t) = w_p \cdot f_{\text{prog}} + w_e \cdot f_{\text{energy}} + w_l \cdot f_{\text{link}} - w_q \cdot f_{\text{queue}} - w_j \cdot f_{\text{jam}}
}
\]

\[
\boxed{
f_{\text{jam}}(i,j) = \lambda_1 \cdot \widehat{\text{JSR}}^{(n)}_{ij} + \lambda_2 \cdot \Delta\text{PER}^{J}_{ij} + \lambda_3 \cdot P_{\text{out},ij} + \lambda_4 \cdot \rho_j
}
\]

\[
\boxed{
Q_{t+1}(s_i, d, j) \leftarrow Q_t(s_i, d, j) + \alpha \left[ R_{ij}(t) + \gamma \max_{k \in \mathcal{N}(j)} Q_t(s_j, d, k) - Q_t(s_i, d, j) \right]
}
\]

### Önemli tasarım kararları

1. **Toplanabilir (additive) ödül:** Çarpımsal değil, toplanabilir form tercih edilir
   — daha kolay ağırlık ayarı, ablasyon ve akademik gerekçelendirme
2. **Normalize edilmiş bileşenler:** Tüm \(f_k \in [0, 1]\), \(\sum w_k = 1\)
3. **Oracle yok:** Ajan jammer parametrelerini bilmez; ölçülebilir PER, SINR, JSR
   tahminleri kullanır
4. **Link-düzeyi SINR:** Çok-hoplu yol kalitesi Q-bootstrapping ile örtülü olarak
   öğrenilir; end-to-end SINR hesabına gerek yok
5. **Ayrıklaştırma:** Tablo tabanlı Q-learning için sürekli değerler bin'lere bölünür
6. **Opsiyonel sert kapı:** Taktik senaryolarda \(\gamma_{\min}\) altındaki linkler
   için ekstra ceza

---

## Kaynakça (APA 7)

Badia, L., Erta, A., Lenzini, L., & Zorzzi, M. (2015). Evaluating the effect of jammers on the performance of wireless ad hoc networks. *Proceedings of European Wireless*. http://www.dei.unipd.it/~badia/papers/2015_05_EW_jam.pdf

ns-3 Project. (n.d.-a). *InterferenceHelper class reference*. ns-3. https://www.nsnam.org/docs/release/3.19/doxygen/classns3_1_1_interference_helper.html

ns-3 Project. (n.d.-b). *Wi-Fi error rate models*. WNS3 2018 Tutorial. https://www.nsnam.org/tutorials/consortium18/slides/wns3_2018_wifi_final.pdf

Sharvari, N. P., Das, D., Bapat, J., & Das, D. (2023). Energy efficient UAV-assisted emergency communication with reliable connectivity and collision avoidance. *arXiv preprint arXiv:2308.16719*. https://arxiv.org/abs/2308.16719

Sutton, R. S., & Barto, A. G. (2018). *Reinforcement learning: An introduction* (2nd ed.). MIT Press. https://web.stanford.edu/class/psych209/Readings/SuttonBartoIPRLBook2ndEd.pdf

Tho, M. C., Ly, N. T. H., Binh, L. H., & Vo, T. T. (2025). QLR-FANET: A Q-learning and rate control-based routing protocol for flying ad hoc networks. *ETRI Journal*. https://onlinelibrary.wiley.com/doi/full/10.4218/etrij.2024-0298

---

> **Not:** Bu formülasyon, önceki belgelerde tanımlanan RF Jamming SINR-PER
> Soyutlama Modeli ve FANET Yönlendirme Protokol Başarım Metrikleri üzerine
> inşa edilmiştir. Önerilen ödül fonksiyonu, karıştırma yokken standart
> Q-learning routing ödülüne indirgenir (\(f_{\text{jam}} = 0\)). Karıştırma
> varken, ceza terimi link kalitesini ve karıştırma tehdidini dikkate alarak
> rota seçimini EW-farkındalıklı hale getirir. Tüm jammer parametreleri
> (\(P_J\), \(R_J\), konum) yalnızca simülatör tarafından bilinir; yönlendirme
> ajanı bunları doğrudan değil, ölçülebilir/tahmin edilen değerler üzerinden
> kullanır.
