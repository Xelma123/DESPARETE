# Python Ağ Simülasyonlarında RF Karıştırma (Jamming) Etkisinin SINR ve PER Üzerinden Matematiksel Soyutlanması

> **Akademik mod — Soyutlama Seviyesi: PHY sembol/OFDM katmanı üstü**
>
> Tarih: 31 Ağustos 2026
>
> Kapsam: Sembol seviyesi PHY detayına (OFDM alt taşıyıcı, modülasyon şemaları) girmeden, Python ağ simülasyonlarında kasıtlı RF karıştırma etkisinin SINR ve PER üzerinden soyutlanması
>
> Kaynak sayısı: 12 (hakemli dergi/konferans + resmi simülatör dokümantasyonu)

---

## 1. Soyutlama Seviyesi ve Temel İlke

Sembol/OFDM seviyesine inilmediğinde, RF karıştırma (jamming) alıcıdaki **ek girişim gücü** olarak soyutlanır. Karıştırıcı sinyal, normal iletişim trafiğiyle aynı frekansta, alıcının bant genişliği içinde kasıtlı olarak yayılan bir girişim kaynağı olarak modellenir. Bu yaklaşım, ns-3'ün "additive interference model" ve OMNeT++/INET'in "scalar analog model" yaklaşımıyla aynı felsefeyi paylaşır: sinyal gücü skaler bir değer olarak temsil edilir, SINR hesaplanır ve PER bir hata modeli üzerinden belirlenir ([ns-3 Project, n.d.-a](https://www.nsnam.org/docs/release/3.19/doxygen/classns3_1_1_interference_helper.html); [INET Framework, n.d.-a](https://inet.omnetpp.org/docs/showcases/wireless/analogmodel/doc/index.html)).

Temel soyutlama hiyerarşisi:

```
Karıştırıcı → Yol Kaybı → Alınan Karıştırma Gücü (J_r)
                                        ↓
Verici → Yol Kaybı → Alınan Sinyal Gücü (S_r)  →  SINR  →  PER  →  Paket Başarısı/Başarısızlığı
                                        ↓
Termal Gürültü (N₀B)
```

---

## 2. Güç ve Yol Kaybı Modeli

### 2.1 Verici-Alıcı Bağlantısı

Bir $i$ vericisinden $r$ alıcısına ulaşan sinyal gücü, yaygın yol kaybı (path loss) modeli ile hesaplanır ([Rappaport, 1996](https://www2.ee.washington.edu/research/funlab/802_11_b_intf_model/trevor_ms_thesis.pdf)):

$$P_{r}(d) = P_{t} \cdot G_{t} \cdot G_{r} \cdot L(d)^{-1}$$

dB cinsinden:

$$P_{r}[\text{dBm}] = P_{t}[\text{dBm}] + G_{t}[\text{dBi}] + G_{r}[\text{dBi}] - PL(d)[\text{dB}] - L_{\text{misc}}[\text{dB}]$$

### 2.2 Log-Distance Yol Kaybı Modeli

$$PL(d) = PL(d_0) + 10n \log_{10}\left(\frac{d}{d_0}\right) + X_\sigma$$

burada:
- $PL(d_0)$: referans mesafe $d_0$ (tipik 1 m) yol kaybı (dB)
- $n$: yol kaybı üssü (serbest uzay $n=2$, şehir içi $n=2.7$–$3.5$)
- $X_\sigma \sim \mathcal{N}(0, \sigma^2)$: log-normal gölgeleme (shadowing) değişkeni

### 2.3 Karıştırıcı-Alıcı Bağlantısı

$J$ karıştırıcısından $r$ alıcısına ulaşan karıştırma gücü, aynı yol kaybı modeli kullanılarak hesaplanır ([Badia et al., 2015](http://www.dei.unipd.it/~badia/papers/2015_05_EW_jam.pdf)):

$$J_r(d_J) = P_J \cdot G_J \cdot G_r \cdot L(d_J)^{-1}$$

dB cinsinden:

$$J_r[\text{dBm}] = P_J[\text{dBm}] + G_J[\text{dBi}] + G_r[\text{dBi}] - PL(d_J)[\text{dB}]$$

### 2.4 Toplam Karıştırma Gücü

Birden fazla karıştırıcı varsa, toplam karıştırma gücü lineer (mW) cinsinden toplanır:

$$J_{\text{total}} = \sum_{k=1}^{K} \beta_k \cdot P_{J,k} \cdot G_{J,k} \cdot G_r \cdot L(d_{k,r})^{-1}$$

burada $\beta_k \in [0,1]$, $k$'nci karıştırıcının **duty cycle** (görev döngüsü) veya bant örtüşme faktörünü temsil eder — sürekli karıştırma için $\beta_k = 1$, atışlı (pulsed) karıştırma için $\beta_k < 1$.

---

## 3. SINR Modeli

### 3.1 Temel SINR Denklemleri

Alıcı $r$'deki SINR, $i$ vericisinden gelen sinyal için ([ns-3 Project, n.d.-b](https://www.nsnam.org/tutorials/consortium23/multi-bss-slides-wns3-2023.pdf); [Chalmers University, 2024](https://research.chalmers.se/publication/544687/file/544687_Fulltext.pdf)):

$$\text{SINR}_{i,r} = \frac{P_{i,r}}{N_0 B + \sum_{m \neq i} P_{m,r} + J_{\text{total}}}$$

dB cinsinden:

$$\text{SINR}[\text{dB}] = 10\log_{10}\left(\frac{P_{i,r}[\text{mW}]}{N_0 B[\text{mW}] + I[\text{mW}] + J_{\text{total}}[\text{mW}]}\right)$$

burada:
- $P_{i,r}$: hedef vericiden alınan sinyal gücü
- $N_0$: termal gürültü güç spektral yoğunluğu ($N_0 = k_B T$, $k_B = 1.38 \times 10^{-23}$ J/K, $T$ sıcaklık)
- $B$: kanal bant genişliği (Hz)
- $\sum_{m \neq i} P_{m,r}$: diğer meşru kullanıcıların girişimi
- $J_{\text{total}}$: toplam karıştırma gücü

### 3.2 Karıştırma Oranları (Jamming Ratios)

Karıştırma etkisini normalize etmek için iki temel oran kullanılır ([Baddeley et al., 2022](https://d197for5662m48.cloudfront.net/documents/publicationstatus/165685/preprint_pdf/1bdcfa2b95de87ff6cf0ec18e61af2a2.pdf)):

**Jamming-to-Noise Ratio (JNR):**

$$\text{JNR} = \frac{P_J}{\sigma^2} = \frac{P_J}{N_0 B}$$

**Jamming-to-Signal Ratio (JSR):**

Serbest uzay yol kaybı modeli altında:

$$\text{JSR} = \frac{J_r}{S_r} = \frac{\text{ERP}_J \cdot G_J \cdot d_T^n}{\text{ERP}_T \cdot G_T \cdot d_J^n}$$

burada $\text{ERP}_X = P_X + G_X - 32.44 - 20\log(f_X)$ etkili yayılan güçtür (dBm) ve $d_T$, $d_J$ sırasıyla verici-alıcı ve karıştırıcı-alıcı mesafeleridir. Karıştırma baskın olduğunda ($J \gg N$):

$$\text{SINR} \approx \text{SNR} - \text{JSR} \quad (\text{dB cinsinden})$$

### 3.3 Karıştırıcı Varlığında SINR

Tek karıştırıcı, tek verici durumunda, $d_T$ verici-alıcı ve $d_J$ karıştırıcı-alıcı mesafesi için ([Badia et al., 2015](http://www.dei.unipd.it/~badia/papers/2015_05_EW_jam.pdf)):

$$\Gamma(d_T, d_J) = \frac{P_T / a(d_T)}{N_0 B + P_J / a(d_J)}$$

burada $a(d) = d^n$ (yol kaybı fonksiyonu, $n$ yol kaybı üssü).

Sabit güç ve gürültü durumunda mesafe etkisi:

$$\Gamma(d_T, d_J) = \left(\frac{d_T^n}{K_1 + K_2 \cdot d_J^{-\beta}}\right)^{-1}$$

burada $K_1 = N_0 B \cdot a(d_T)$ ve $K_2 = P_J \cdot a(d_T)$ uygun sabitlerdir.

---

## 4. PER (Paket Hata Oranı) Modeli

### 4.1 SINR'den PER'e: Üç Soyutlama Seviyesi

PHY sembol seviyesine girmeden PER hesaplamak için üç yaygın yaklaşım vardır:

#### Seviye 1: Eşik Tabanlı (Threshold-Based)

En basit soyutlama — bir SINR eşiği $\gamma_{\text{th}}$ tanımlanır ([UPC, 2019](https://upcommons.upc.edu/bitstreams/fb2ba3f1-6e53-4bed-9e57-b9946c3209c8/download)):

$$\text{PER} = \begin{cases} 1, & \text{SINR} < \gamma_{\text{th}} \\ 0, & \text{SINR} \geq \gamma_{\text{th}} \end{cases}$$

**Avantaj:** Hesaplama açısından en ucuz. **Dezavantaj:** Gerçekçi değil — gerçek sistemlerde PER geçişi keskin değildir.

#### Seviye 2: Lojistik (Sigmoid) Model

Daha gerçekçi, yumuşak geçiş sağlayan model ([Semantic Scholar, n.d.](https://pdfs.semanticscholar.org/948d/70ee9c851200f42186c4604726c92d855eb5.pdf)):

$$\text{PER}(\gamma) = \frac{1}{1 + e^{a(\gamma - \gamma_0)}}$$

burada:
- $\gamma$: anlık SINR (dB)
- $\gamma_0$: SINR geçiş noktası (PER ≈ 0.5 olan SINR değeri)
- $a$: geçiş eğriliği (sıfıra yakın eşik davranışı için $a \to \infty$)

**Örnek kalibrasyon:** 802.11b 1 Mbps BPSK için $\gamma_0 \approx 4$ dB, $a \approx 2$ tipiktir.

#### Seviye 3: BER'den PER'e Türetilmiş Model

En yaygın ve en titiz soyutlama — önce BER (Bit Hata Oranı) hesaplanır, sonra paket uzunluğu ile PER elde edilir ([ns-3 Project, n.d.-c](https://pmc.ncbi.nlm.nih.gov/articles/PMC7312563/); [OMNeT++ INET, n.d.-b](https://inet.omnetpp.org/docs/showcases/wireless/errorrate/doc/index.html)):

$$\text{BER} = f(\text{SINR})$$

$$\text{PER} = 1 - (1 - \text{BER})^{8L}$$

burada $L$ paket boyutudur (bayt cinsinden).

**BER'in hesaplanması:** BER, modülasyon şemasına bağlıdır ancak bu soyutlamada modülasyon detayına girmeden, **önceden hesaplanmış bir lookup table (LUT)** veya analitik bir fonksiyon kullanılır. Örneğin, AWGN kanalında BPSK için:

$$\text{BER}_{\text{BPSK}} = Q\left(\sqrt{2\gamma_b}\right)$$

burada $\gamma_b = E_b/N_0$ bit başına enerji/gürültü yoğunluğu oranıdır ve SINR ile ilişkisi:

$$\gamma_b = \text{SINR} \cdot \frac{B}{R}$$

burada $R$ sembol/veri hızüdür ([PMC, 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7312563/)).

**QPSK için:**

$$\text{BER}_{\text{QPSK}} = Q\left(\sqrt{\gamma_b}\right)$$

**M-QAM için ($M = 2^k$):**

$$\text{BER}_{\text{M-QAM}} \approx \frac{4}{k}\left(1 - \frac{1}{\sqrt{M}}\right) Q\left(\sqrt{\frac{3k\gamma_b}{M-1}}\right)$$

> **Önemli Not:** Bu soyutlamada modülasyon detayına (OFDM alt taşıyıcı yapısı, kanal kodlama, interleaving) girilmez. Bunun yerine, her MCS (Modulation and Coding Scheme) için SINR-PER eğrisi önceden hesaplanıp bir lookup table olarak saklanır. ns-3'ün `NistErrorRateModel` ve `YansErrorRateModel` sınıfları bu yaklaşımı kullanır ([ns-3 Project, n.d.-d](https://www.nsnam.org/tutorials/consortium18/slides/wns3_2018_wifi_final.pdf)).

### 4.2 Chunk Bazlı PER Hesabı

Paket iletimi sırasında SINR sabit kalmaz (örneğin karıştırıcı atışlı çalışıyorsa). Bu durumda paket, SINR'ın sabit kaldığı zaman dilimlerine (chunk) bölünür ve her chunk için ayrı PER hesaplanır ([ns-3 Project, n.d.-a](https://www.nsnam.org/docs/release/3.19/doxygen/classns3_1_1_interference_helper.html)):

$$\text{PER}_{\text{total}} = 1 - \prod_{i=1}^{n}\left(1 - \text{PER}_i(\text{SINR}_i, L_i)\right)$$

burada $n$ chunk sayısı, $L_i$ $i$'nci chunk'ın bayt sayısıdır.

### 4.3 PER Karar Mekanizması

PER hesaplandıktan sonra, paketin başarıyla alınıp alınmadığı bir Bernoulli denemesi ile belirlenir ([ns-3 Project, n.d.-c](https://pmc.ncbi.nlm.nih.gov/articles/PMC7312563/)):

$$\text{Paket Başarılı} = \begin{cases} \text{Evet}, & U(0,1) > \text{PER} \\ \text{Hayır}, & U(0,1) \leq \text{PER} \end{cases}$$

burada $U(0,1)$ standart uniform rastgele değişkendir.

---

## 5. Karıştırma Etki Yarıçapı (Jamming Effect Radius)

### 5.1 Temel Türetme

Karıştırıcının bir alıcıyı etkilemesi için, alıcıdaki SINR'ı bir $\gamma_{\text{th}}$ eşiğinin altına indirmesi gerekir ([Rutgers WINLAB, n.d.](https://www.winlab.rutgers.edu/~yychen/daisylab/papers/Wireless%20Jamming%20Localization%20by%20Exploiting%20Nodes'%20Hearing%20Ranges.pdf); [NSF, 2023](https://par.nsf.gov/servlets/purl/10351874)):

$$\text{SINR}_r = \frac{S_r}{N_0 B + J_r(d_J)} < \gamma_{\text{th}}$$

Buradan, karıştırıcının alıcıda yaratması gereken minimum karıştırma gücü:

$$J_{\text{req}} = \frac{S_r}{\gamma_{\text{th}}} - N_0 B$$

> **Not:** Bu denklem lineer (mW) cinsinde geçerlidir. dB cinsinde yaklaşık olarak $J_{\text{req}}[\text{dBm}] \approx S_r[\text{dBm}] - \gamma_{\text{th}}[\text{dB}]$ kullanılabilir, ancak kesin hesap için lineer cinsine dönüştürmek gerekir.

### 5.2 Etki Yarıçapı Formülü

Karıştırıcının alıcıya olan mesafesi $d_J$ olduğunda, alınan karıştırma gücü:

$$J_r(d_J) = P_J \cdot K \cdot d_J^{-n}$$

burada $K = G_J \cdot G_r$ anten kazançları ve sabit kayıplardan oluşan bir sabittir.

Etki yarıçapı $R_J$, $J_r(R_J) = J_{\text{req}}$ eşitliğinden:

$$\boxed{R_J = \left(\frac{P_J \cdot K}{J_{\text{req}}}\right)^{1/n} = \left(\frac{P_J \cdot K}{\frac{S_r}{\gamma_{\text{th}}} - N_0 B}\right)^{1/n}}$$

dB cinsinden (yaklaşık):

$$R_J \approx d_0 \cdot 10^{\frac{P_J[\text{dBm}] + G_J[\text{dBi}] + G_r[\text{dBi}] - PL(d_0)[\text{dB}] - J_{\text{req}}[\text{dBm}]}{10n}}$$

### 5.3 Alıcı-Merkezli Etki Yarıçapı

Etki yarıçapı yalnızca karıştırıcı gücüne bağlı değildir; **alıcının sinyal gücüne** de bağlıdır. Aynı karıştırıcı, güçlü sinyal alan bir alıcıyı daha geniş bir alandan etkileyebilirken, zayıf sinyal alan bir alıcıyı daha yakın mesafeden etkiler. Bu, karıştırma etki yarıçapının **alıcı-merkezli** olduğunu gösterir ([Badia et al., 2015](http://www.dei.unipd.it/~badia/papers/2015_05_EW_jam.pdf)).

Etki yarıçapını belirleyen faktörler:

| Faktör | Etki |
|---|---|
| Karıştırma gücü $P_J$ ↑ | $R_J$ ↑ |
| Yol kaybı üssü $n$ ↑ | $R_J$ ↓ |
| Alıcı sinyal gücü $S_r$ ↑ | $R_J$ ↑ (daha fazla karıştırma gerekir) |
| SINR eşiği $\gamma_{\text{th}}$ ↑ | $R_J$ ↑ (daha düşük karıştırma yeterli) |
| Termal gürültü $N_0 B$ ↑ | $R_J$ ↓ |

### 5.4 Serbest Uzay ve Two-Ray Modeller için Özel Formlar

**Serbest uzay ($n = 2$):**

$$R_J = \sqrt{\frac{P_J \cdot G_J \cdot G_r \cdot \lambda^2}{(4\pi)^2 \cdot J_{\text{req}}}}$$

**Two-Ray ground reflection ($n = 4$):**

$$R_J = \sqrt{\frac{P_J \cdot G_J \cdot G_r \cdot h_J^2 \cdot h_r^2}{J_{\text{req}}}}$$

burada $h_J$ ve $h_r$ sırasıyla karıştırıcı ve alıcı anten yükseklikleridir ([FOI, n.d.](https://www.foi.se/rest-api/report/FOI-R--4222--SE)).

---

## 6. Hat Kalitesi Metrikleri

### 6.1 Paket Teslim Oranı (PDR)

$$\text{PDR} = 1 - \text{PER} = (1 - \text{BER})^{8L}$$

Karıştırma altında:

$$\text{PDR}_{\text{jammed}} = \frac{1}{1 + e^{a(\text{SINR}_{\text{jammed}} - \gamma_0)}}$$

### 6.2 Kapasite Düşüşü (Shannon)

Karıştırma altında etkin kanal kapasitesi:

$$C_{\text{jammed}} = B \cdot \log_2\left(1 + \text{SINR}_{\text{jammed}}\right)$$

Karıştırmasız duruma göre oransal kapasite düşüşü:

$$\eta = \frac{C_{\text{jammed}}}{C_{\text{clean}}} = \frac{\log_2(1 + \text{SINR}_{\text{jammed}})}{\log_2(1 + \text{SNR})}$$

([PMC, 2022](https://pmc.ncbi.nlm.nih.gov/articles/PMC9160013/))

### 6.3 Outage Olasılığı

$$P_{\text{out}} = P(\text{SINR} < \gamma_{\text{th}})$$

Rayleigh sönümlemesi altında:

$$P_{\text{out}} = 1 - \exp\left(-\frac{\gamma_{\text{th}}}{\bar{\gamma}}\right)$$

burada $\bar{\gamma}$ ortalama SINR'dir.

---

## 7. Python Simülasyonu İçin Minimal Algoritma

```python
import numpy as np

# ═══════════════════════════════════════════════════════════════
# PARAMETRELER
# ═══════════════════════════════════════════════════════════════
PT          = 20.0    # Verici gücü (dBm)
PJ          = 30.0    # Karıştırıcı gücü (dBm)
GT          = 2.0     # Verici anten kazancı (dBi)
GJ          = 2.0     # Karıştırıcı anten kazancı (dBi)
GR          = 2.0     # Alıcı anten kazancı (dBi)
f           = 2.4e9   # Frekans (Hz) — 2.4 GHz
B           = 20e6    # Bant genişliği (Hz) — 20 MHz
kT          = -174.0  # Termal gürültü (dBm/Hz)
N0B         = kT + 10*np.log10(B)  # Toplam gürültü gücü (dBm)
n           = 2.0     # Yol kaybı üssü (serbest uzay)
d0          = 1.0     # Referans mesafe (m)
gamma_th    = 6.0     # SINR eşiği (dB) — 802.11 tipik
gamma_0     = 4.0     # Lojistik PER geçiş noktası (dB)
a_log       = 2.0     # Lojistik PER eğriliği
L_pkt       = 512     # Paket boyutu (bayt)

# ═══════════════════════════════════════════════════════════════
# YOL KAYBI VE ALINAN GÜÇ
# ═══════════════════════════════════════════════════════════════
def path_loss_db(d, n=2.0, d0=1.0, f=2.4e9):
    """Log-distance yol kaybı (dB)"""
    PL_d0 = 20*np.log10(4*np.pi*d0*f / 3e8)  # Serbest uzay referans
    shadow = np.random.normal(0, 2.0)  # X_sigma
    return PL_d0 + 10*n*np.log10(d/d0) + shadow

def received_power_dbm(Pt, Gt, Gr, d, n=2.0):
    """Alınan sinyal gücü (dBm)"""
    PL = path_loss_db(d, n)
    return Pt + Gt + Gr - PL

# ═══════════════════════════════════════════════════════════════
# SINR HESABI
# ═══════════════════════════════════════════════════════════════
def sinr_db(S_dBm, J_dBm, N_dBm):
    """SINR hesabı (dB) — üç gücün dBm cinsinden"""
    S_lin = 10**(S_dBm/10)
    J_lin = 10**(J_dBm/10)
    N_lin = 10**(N_dBm/10)
    return 10*np.log10(S_lin / (N_lin + J_lin))

# ═══════════════════════════════════════════════════════════════
# PER MODELLERİ
# ═══════════════════════════════════════════════════════════════
def per_threshold(sinr_db, gamma_th=6.0):
    """Seviye 1: Eşik tabanlı PER"""
    return 1.0 if sinr_db < gamma_th else 0.0

def per_logistic(sinr_db, gamma_0=4.0, a=2.0):
    """Seviye 2: Lojistik (sigmoid) PER"""
    return 1.0 / (1.0 + np.exp(a * (sinr_db - gamma_0)))

def per_from_ber(sinr_db, L_pkt=512, modulation='BPSK'):
    """Seviye 3: BER'den PER'e türetilmiş model"""
    from scipy.stats import norm
    gamma_b = sinr_db  # BPSK için gamma_b ≈ SINR (dB)
    
    if modulation == 'BPSK':
        ber = norm.sf(np.sqrt(2 * 10**(gamma_b/10)))  # Q(sqrt(2*gamma_b))
    elif modulation == 'QPSK':
        ber = norm.sf(np.sqrt(10**(gamma_b/10)))
    else:
        ber = 0.5 * np.exp(-10**(gamma_b/10) / 2)
    
    per = 1 - (1 - ber)**(8 * L_pkt)
    return min(per, 1.0)

# ═══════════════════════════════════════════════════════════════
# KARIŞTIRMA ETKİ YARIÇAPI
# ═══════════════════════════════════════════════════════════════
def jamming_radius(S_dBm, PJ_dBm, gamma_th=6.0, N_dBm=None, n=2.0, 
                   GJ=2.0, GR=2.0, f=2.4e9, d0=1.0):
    """
    Karıştırma etki yarıçapı (metre)
    
    R_J = (P_J * K / J_req)^(1/n)
    J_req = S/gamma_th - N  (lineer cinsinden)
    """
    if N_dBm is None:
        N_dBm = kT + 10*np.log10(B)
    
    # Lineer cinsine dönüştür
    S_lin = 10**(S_dBm/10)
    N_lin = 10**(N_dBm/10)
    gamma_th_lin = 10**(gamma_th/10)
    
    # Gerekli minimum karıştırma gücü (alıcıda)
    J_req_lin = S_lin / gamma_th_lin - N_lin
    
    if J_req_lin <= 0:
        return float('inf')  # Gürültü zaten eşiği aşıyor
    
    # Karıştırıcının referans mesafedeki ERP'si
    PL_d0 = 20*np.log10(4*np.pi*d0*f/3e8)
    J_at_d0_dBm = PJ_dBm + GJ + GR - PL_d0
    J_at_d0_lin = 10**(J_at_d0_dBm/10)
    
    # Etki yarıçapı
    R_J = (J_at_d0_lin / J_req_lin)**(1/n)
    return R_J

# ═══════════════════════════════════════════════════════════════
# ÖRNEK SİMÜLASYON
# ═══════════════════════════════════════════════════════════════
d_T = 500     # Verici-alıcı mesafesi (m)
d_J = 300     # Karıştırıcı-alıcı mesafesi (m)

# Alınan güçler
S_r = received_power_dbm(PT, GT, GR, d_T, n)
J_r = received_power_dbm(PJ, GJ, GR, d_J, n)

# SINR
sinr = sinr_db(S_r, J_r, N0B)

# PER (üç modelle)
per1 = per_threshold(sinr, gamma_th)
per2 = per_logistic(sinr, gamma_0, a_log)
per3 = per_from_ber(sinr, L_pkt, 'BPSK')

# Etki yarıçapı
R_J = jamming_radius(S_r, PJ, gamma_th, N0B, n, GJ, GR)

print(f"Alınan sinyal gücü:    {S_r:.2f} dBm")
print(f"Alınan karıştırma:    {J_r:.2f} dBm")
print(f"Termal gürültü:       {N0B:.2f} dBm")
print(f"SINR:                 {sinr:.2f} dB")
print(f"PER (eşik):           {per1:.4f}")
print(f"PER (lojistik):       {per2:.4f}")
print(f"PER (BER'den):        {per3:.6f}")
print(f"Karıştırma etki yarıçapı: {R_J:.1f} m")
```

---

## 8. Özet ve Önemli Uyarılar

### Soyutlama Hiyerarşisi

| Seviye | Soyutlama | Hesaplama Maliyeti | Gerçekçilik |
|---|---|---|---|
| 1 | Eşik tabanlı PER | En düşük | Düşük |
| 2 | Lojistik/Sigmoid PER | Düşük | Orta |
| 3 | BER→PER (LUT destekli) | Orta | Yüksek |
| 4 | OFDM sembol/alt taşıyıcı seviyesi | Yüksek | En yüksek |

Bu çalışma, Seviye 1–3 aralığını kapsar. Seviye 4'e (OFDM alt taşıyıcı bazında EESM/RBIR yöntemleri) inilmeden, FANET simülasyonlarında karıştırma etkisi yeterli gerçekçilikle modellenebilir.

### Önemli Uyarılar

1. **PER tek başına SINR tarafından belirlenmez:** Gerçek PHY'de PER, modülasyon şeması, kodlama oranı, paket uzunluğu ve kanal koşullarına bağlıdır. Bu soyutlamada bu bağımlılıklar bir SINR-PER lookup table'ına (LUT) gömülür ([MathWorks, n.d.](https://www.mathworks.com/help/wlan/ug/physical-layer-abstraction-for-system-level-simulation.html)).

2. **Etki yarıçapı alıcı-merkezlidir:** Aynı karıştırıcı farklı alıcıları farklı yarıçaplardan etkiler. Yarıçap, verici-alıcı sinyal gücüne ve SINR eşiğine bağlıdır.

3. **Atışlı (pulsed) karıştırma için duty cycle faktörü ($\beta$) kullanılmalıdır:** Sürekli karıştırma $\beta = 1$ varsayımı gerçekçi olmayabilir; gerçek karıştırıcılar genellikle atışlı çalışır.

4. **SINR zamanla değişebilir:** Karıştırıcı hareketliyse veya atışlı çalışıyorsa, paket iletimi sırasında SINR değişir. Bu durumda chunk bazlı PER hesabı gerekir.

---

## Kaynaklar (APA 7)

Baddeley, M. et al. (2022). JamRF: Performance analysis, evaluation, and implementation of RF jamming in Wi-Fi networks. *Authorea Preprint*. https://d197for5662m48.cloudfront.net/documents/publicationstatus/165685/preprint_pdf/1bdcfa2b95de87ff6cf0ec18e61af2a2.pdf

Badia, L., Erta, A., Lenzini, L., & Zorzzi, M. (2015). Evaluating the effect of jammers on the performance of wireless ad hoc networks. *Proceedings of European Wireless*. http://www.dei.unipd.it/~badia/papers/2015_05_EW_jam.pdf

Chalmers University of Technology. (2024). *A simulation-based methodology to assess the impact of jamming in wireless networks*. https://research.chalmers.se/publication/544687/file/544687_Fulltext.pdf

FOI (Swedish Defence Research Agency). (n.d.). *Jamming effects on frequency-hopping ad hoc networks*. FOI-R--4222--SE. https://www.foi.se/rest-api/report/FOI-R--4222--SE

INET Framework. (n.d.-a). *Wireless signal analog domain representations*. OMNeT++. https://inet.omnetpp.org/docs/showcases/wireless/analogmodel/doc/index.html

INET Framework. (n.d.-b). *Packet loss vs. distance using various WiFi bitrates*. OMNeT++. https://inet.omnetpp.org/docs/showcases/wireless/errorrate/doc/index.html

MathWorks. (n.d.). *Physical layer abstraction for system-level simulation*. https://www.mathworks.com/help/wlan/ug/physical-layer-abstraction-for-system-level-simulation.html

ns-3 Project. (n.d.-a). *InterferenceHelper class reference*. ns-3. https://www.nsnam.org/docs/release/3.19/doxygen/classns3_1_1_interference_helper.html

ns-3 Project. (n.d.-b). *Multi BSS Wi-Fi simulations in ns-3*. WNS3 2023 Tutorial. https://www.nsnam.org/tutorials/consortium23/multi-bss-slides-wns3-2023.pdf

ns-3 Project. (n.d.-c). *An NS-3 implementation and experimental performance evaluation of Wi-Fi*. PMC. https://pmc.ncbi.nlm.nih.gov/articles/PMC7312563/

ns-3 Project. (n.d.-d). *Wi-Fi error rate models*. WNS3 2018 Tutorial. https://www.nsnam.org/tutorials/consortium18/slides/wns3_2018_wifi_final.pdf

NSF (National Science Foundation). (2023). *Exact and efficient protective jamming in SINR-based wireless networks*. https://par.nsf.gov/servlets/purl/10351874

Rutgers WINLAB. (n.d.). *Wireless jamming localization by exploiting nodes' hearing ranges*. https://www.winlab.rutgers.edu/~yychen/daisylab/papers/Wireless%20Jamming%20Localization%20by%20Exploiting%20Nodes'%20Hearing%20Ranges.pdf

Universitat Politècnica de Catalunya. (2019). *IEEE 802.11s mesh networking evaluation under NS-3*. https://upcommons.upc.edu/bitstreams/fb2ba3f1-6e53-4bed-9e57-b9946c3209c8/download
