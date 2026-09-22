# FANET Yönlendirme Protokol Başarım Metrikleri — Matematiksel Tanımlar

> **Kapsam:** Taktik FANET simülasyonlarında yönlendirme protokollerinin (AODV, OLSR, GPSR vb.)
> başarımını ölçmek için kullanılan temel metriklerin matematiksel tanımları.
> Sembol seviyesi PHY detayına girilmez; tüm formüller ağ/katman seviyesindedir.

---

## İçindekiler

1. [Paket Teslim Oranı (PDR)](#1-paket-teslim-oranı-pdr)
2. [Uçtan Uca Gecikme (E2E Latency)](#2-uçtan-uca-gecikme-e2e-latency)
3. [Yönlendirme Yükü (Routing Overhead)](#3-yönlendirme-yükü-routing-overhead)
4. [Bağlantı Kopma Sayısı (Link Break Count)](#4-bağlantı-kopma-sayısı-link-break-count)
5. [Rota Kurtarma Süresi (Route Recovery Latency)](#5-rota-kurtarma-süresi-route-recovery-latency)
6. [Metrikler Arası İlişkiler](#6-metrikler-arası-i̇lişkiler)
7. [Kaynakça](#kaynakça)

---

## 1. Paket Teslim Oranı (PDR)

### Tanım

PDR, kaynak düğümün uygulama katmanında gönderdiği benzersiz veri paketlerinin hedef
düğümde başarıyla alınan oranıdır. Ağ güvenilirliğinin ve yönlendirme protokolünün
başarısının temel ölçüsüdür ([Mohammad El-Basioni, 2024](https://www.nature.com/articles/s41598-024-72983-y);
[Broyles et al., 2010](https://resilinets.org/papers/Broyles-Jabbar-Sterbenz-2010.pdf)).

### Matematiksel Tanım

\[
\text{PDR} = \frac{|P_{\text{recv}}|}{|P_{\text{sent}}|}
\]

**Değişken tanımları:**

| Sembol | Tanım |
|---|---|
| \(P_{\text{recv}}\) | Hedef düğümde alınan **benzersiz** veri paketleri kümesi (dublikalar hariç) |
| \(P_{\text{sent}}\) | Kaynak düğümün uygulama katmanında gönderdiği veri paketleri kümesi |
| \(|\cdot|\) | Kümenin kardinalitesi (eleman sayısı) |

### Detaylı formülasyon

Birden fazla kaynak-hedef çifti için, tüm düğümler üzerinde toplanır ([Mohammad El-Basioni, 2024](https://www.nature.com/articles/s41598-024-72983-y)):

\[
\text{PDR} = \frac{\left|\bigcup_{u \in U} \acute{P}_u\right|}{\left|\bigcup_{u \in U} S_u\right|}
\]

burada:
- \(U\) — ağdaki tüm düğüm kümesi
- \(\acute{P}_u\) — düğüm \(u\)'den alınan **dublikasız** paket kümesi
- \(S_u\) — düğüm \(u\)'nin gönderdiği paket kümesi

### Önemli notlar

- **Dublikalar hariç tutulur:** Aynı paket birden çok yol ile geldiğinde yalnızca bir kez sayılır.
- **Yalnız uygulama katmanı veri paketleri:** Kontrol paketleri (RREQ, RREP, RERR, HELLO, TC) ve MAC katmanı yeniden iletimleri PDR hesabına dahil edilmez.
- PDR ∈ [0, 1] aralığındadır; yüzde olarak \(\text{PDR} \times 100\) ifade edilir.
- **PDR = 0** hiçbir paketin teslim edilmediği anlamına gelir; bu durumda E2E gecikme tanımsızdır.

### Birim: Boyutsuz (oran), genelde % olarak raporlanır.

---

## 2. Uçtan Uca Gecikme (E2E Latency)

### Tanım

E2E gecikme, bir veri paketinin kaynak düğümde oluşturulduğu andan hedef düğümde
başarıyla alındığı ana kadar geçen ortalama süredir ([Mohammad El-Basioni, 2024](https://www.nature.com/articles/s41598-024-72983-y);
[Broyles et al., 2010](https://resilinets.org/papers/Broyles-Jabbar-Sterbenz-2010.pdf)).

### Matematiksel Tanım

\[
D_{\text{avg}} = \frac{1}{|P_{\text{recv}}|} \sum_{p \in P_{\text{recv}}} D_p
= \frac{1}{|P_{\text{recv}}|} \sum_{p \in P_{\text{recv}}} \left(T_{r_p} - T_{c_p}\right)
\]

**Değişken tanımları:**

| Sembol | Tanım |
|---|---|
| \(D_{\text{avg}}\) | Ortalama uçtan uca gecikme (saniye) |
| \(D_p\) | Paket \(p\)'nin uçtan uca gecikmesi |
| \(T_{c_p}\) | Paket \(p\)'nin kaynak düğümde oluşturulma zamanı |
| \(T_{r_p}\) | Paket \(p\)'nin hedef düğümde alınma zamanı |
| \(P_{\text{recv}}\) | Başarıyla teslim edilen paket kümesi |

### Gecikme bileşenleri

\(D_p\), aşağıdaki bileşenlerin toplamıdır ([Broyles et al., 2010](https://resilinets.org/papers/Broyles-Jabbar-Sterbenz-2010.pdf);
[DTIC, n.d.](https://apps.dtic.mil/sti/tr/pdf/ADA445585.pdf)):

\[
D_p = T_{\text{route}} + T_{\text{queue}} + T_{\text{tx}} + T_{\text{prop}} + T_{\text{proc}} + T_{\text{retrans}}
\]

| Bileşen | Tanım |
|---|---|
| \(T_{\text{route}}\) | Rota keşfi gecikmesi (rota yokken RREQ/RREP bekleme süresi) |
| \(T_{\text{queue}}\) | Arabirim kuyruğunda bekleme süresi |
| \(T_{\text{tx}}\) | İletim süresi (paket boyutu / bant genişliği) |
| \(T_{\text{prop}}\) | Yayılma süresi (mesafe / ışık hızı) |
| \(T_{\text{proc}}\) | İşleme süresi (yönlendirme tablosu arama, vb.) |
| \(T_{\text{retrans}}\) | MAC katmanı yeniden iletim gecikmeleri |

### Önemli notlar

- **Yalnız başarıyla teslim edilen paketler üzerinden hesaplanır.** Düşen paketler dahil değildir.
- \(|P_{\text{recv}}| = 0\) ise \(D_{\text{avg}}\) **tanımsızdır** (0 değildir).
- Düşük E2E gecikme, protokolün rota keşfi ve bakımında hızlı olduğunu gösterir.

### Birim: Saniye (s) veya milisaniye (ms).

---

## 3. Yönlendirme Yükü (Routing Overhead)

### Tanım

Yönlendirme yükü, yönlendirme protokolünün ağ kurmak ve sürdürmek için gönderdiği
kontrol paketlerinin miktarıdır. İki yaygın tanımlama biçimi vardır ([DTIC, n.d.](https://apps.dtic.mil/sti/tr/pdf/ADA445585.pdf);
[Ceviz et al., 2022](https://web.cs.hacettepe.edu.tr/~ssen/files/papers/AdhocNets22.pdf)).

### 3.1. Ham Yönlendirme Yükü (Raw Routing Overhead, ROH)

\[
\text{ROH} = \sum_{i=1}^{N} \sum_{k=1}^{K_i} h_{i,k}
\]

**Değişken tanımları:**

| Sembol | Tanım |
|---|---|
| \(N\) | Ağdaki toplam düğüm sayısı |
| \(K_i\) | Düğüm \(i\)'nin gönderdiği kontrol paketi sayısı |
| \(h_{i,k}\) | Düğüm \(i\)'nin \(k\)'ncı kontrol paketinin geçtiği hop sayısı |

> **Not:** Her hop bazlı iletim bir kez sayılır. Bir RREQ paketi 5 hop geçiyorsa,
> bu 5 iletim olarak sayılır ([DTIC, n.d.](https://apps.dtic.mil/sti/tr/pdf/ADA445585.pdf)).

### 3.2. Normalize Edilmiş Yönlendirme Yükü (Normalized Routing Load, NRL)

\[
\text{NRL} = \frac{\text{ROH}}{|P_{\text{recv}}|}
= \frac{\sum_{i=1}^{N} \sum_{k=1}^{K_i} h_{i,k}}{|P_{\text{recv}}|}
\]

**Değişken tanımları:**

| Sembol | Tanım |
|---|---|
| \(\text{ROH}\) | Ham yönlendirme yükü (kontrol paketi iletim sayısı) |
| \(|P_{\text{recv}}|\) | Hedefte başarıyla teslim edilen veri paketi sayısı |

### 3.3. Byte bazlı alternatif

Bazı çalışmalar yükü byte cinsinden ölçer ([Salma Badawi Mohammed, 2021](http://eprints.utm.my/103613/1/SalmaBadawiMohammed2021_PerformanceEvaluationofFANET.pdf)):

\[
\text{ROH}_{\text{byte}} = \sum_{\text{all control packets}} \text{size}(\text{pkt}) \times h_{\text{pkt}}
\]

### Önemli notlar

- **Karşılaştırma yaparken aynı sayma kuralı kullanılmalıdır.** Ham sayım (toplam kontrol paketi iletimi) ile normalize edilmiş sayım (kontrol/data oranı) farklı sonuçlar verebilir.
- NRL, her bir başarıyla teslim edilen veri paketi başına kaç kontrol paketi iletimi yapıldığını gösterir. Düşük NRL, protokolün veri iletimi için az kontrol trafiği kullandığını ifade eder.
- Proaktif protokoller (OLSR) periyodik HELLO/TC gönderir; reaktif protokoller (AODV) yalnızca ihtiyaçta rota keşfi yapar. Bu nedenle NRL değerleri mobilite seviyesine göre farklılaşır.

### Birim: ROH — paket sayısı (veya byte); NRL — boyutsuz oran.

---

## 4. Bağlantı Kopma Sayısı (Link Break Count)

### Tanım

Bağlantı kopma sayısı, simülasyon süresince aktif rota üzerindeki bağlantıların
kopma olaylarının toplam sayısıdır. FANET'lerde yüksek İHA hızı nedeniyle sık
bağlantı kopmaları yaşanır ve bu metrik protokolün dayanıklılığını gösterir
([Ceviz et al., 2022](https://web.cs.hacettepe.edu.tr/~ssen/files/papers/AdhocNets22.pdf);
[Tho et al., 2025](https://onlinelibrary.wiley.com/doi/full/10.4218/etrij.2024-0298)).

### Bağlantı geçerlilik koşulu

İki düğüm \(i\) ve \(j\) arasındaki bağlantı \(t\) anında **geçerli** ise:

\[
L_{ij}(t) = \mathbb{1}\{D_{ij}(t) \leq R\}
\]

burada:

\[
D_{ij}(t) = \|X_i(t) - X_j(t)\|
\]

**Değişken tanımları:**

| Sembol | Tanım |
|---|---|
| \(D_{ij}(t)\) | \(t\) anında düğüm \(i\) ve \(j\) arasındaki öklid mesafesi |
| \(X_i(t)\) | Düğüm \(i\)'nin \(t\) anındaki 3B pozisyonu |
| \(R\) | İletişim menzili (transmission range) |
| \(L_{ij}(t)\) | Bağlantı geçerlilik göstergesi (1: bağlı, 0: kopuk) |

### Alternatif: RF tabanlı bağlantı geçerliliği

Mesafe yerine RF sinyal gücü/SINR eşiği de kullanılabilir:

\[
L_{ij}(t) = \mathbb{1}\{\text{SINR}_{ij}(t) \geq \gamma_{\text{th}}\}
\]

### Bağlantı kopma sayısı tanımı

Simülasyon süresince, **aktif rotada** bulunan bağlantıların durum değişimi
(yukarı→aşağı geçişi) sayısıdır:

\[
\text{LBC} = \sum_{k=1}^{T/\Delta t} \sum_{(i,j) \in \mathcal{A}_k} \mathbb{1}\{L_{ij}(t_{k-1}) = 1 \land L_{ij}(t_k) = 0\}
\]

**Değişken tanımları:**

| Sembol | Tanım |
|---|---|
| \(\mathcal{A}_k\) | \(t_k\) anında aktif rotalardaki bağlantı kümesi |
| \(t_k = k \cdot \Delta t\) | \(k\)'ncı zaman adımı |
| \(\Delta t\) | Zaman çözünürlüğü (örn. HELLO interval) |
| \(T\) | Toplam simülasyon süresi |
| \(L_{ij}(t_k)\) | \(t_k\) anında bağlantı geçerlilik göstergesi |

### Önemli notlar

- **Aktif rota bağlantı kopmaları** sayılır; tüm komşuluk bağlantıları değil. Yalnızca
  veri paketi ileten veya iletecek rotadaki bağlantılar dikkate alınır.
- Bağlantı kopması tespiti Hello mesajları ile yapılır: bir düğüm art arda
  `ALLOWED_HELLO_LOSS` adet Hello mesajı alamazsa bağlantı kopmuş sayılır
  ([Mohammad El-Basioni, 2024](https://www.nature.com/articles/s41598-024-72983-y)).
- QLR-FANET çalışmasında 45 düğümde GPSR 206,88, AODV 104,38, QLR-FANET 16,5
  ortalama kopma bildirilmiştir ([Tho et al., 2025](https://onlinelibrary.wiley.com/doi/full/10.4218/etrij.2024-0298)).

### Birim: Tamsayı (kopma olayı sayısı).

---

## 5. Rota Kurtarma Süresi (Route Recovery Latency)

### Tanım

Rota kurtarma süresi, bir bağlantı kopması nedeniyle ilk veri paketinin düşmesi ile
kaynak düğümün yönlendirme tablosunu yeniden hesaplayıp geçerli bir rota yeniden
kurması arasındaki süredir. İki düzlemde tanımlanır.

### 5.1. Kontrol düzlemi kurtarma süresi (control-plane recovery)

\[
\Delta_{\text{ctrl}} = T_r - T_d
\]

**Değişken tanımları:**

| Sembol | Tanım |
|---|---|
| \(T_d\) | Bağlantı kopması nedeniyle ilk veri paketinin düşürüldüğü zaman |
| \(T_r\) | Kaynak düğümün yönlendirme tablosunu yeniden hesapladığı (geçerli rota kurulduğu) zaman |

> **Not:** \(T_r > T_d\) olmalıdır; kurtarma her zaman düşme sonrasında gerçekleşir.
> Mutlak değer kullanılmaz; \(\Delta_{\text{ctrl}} = T_r - T_d\).

Bu tanım, OLSR protokolü için tek yol ve çok yollu senaryolarda analitik olarak
doğrulanmıştır. Kurtarma gecikmesi, bağlantı kopmasının ne zaman tespit edildiğine
bağlı olarak iki durumda incelenir ([Badia et al., 2012](https://hal.science/hal-00708684v1/document)):

**Durum 1 — Komşu TC mesajı gönderirse:**

\[
\Delta_1 \in \left[\text{NEIGHB\_HOLD\_TIME} - \text{HELLO\_INTERVAL},\; \text{NEIGHB\_HOLD\_TIME} + \text{TC\_INTERVAL} + \text{MAXJITTER}\right]
\]

**Durum 2 — Eski topoloji bilgisi zaman aşımına uğrar:**

\[
\Delta_2 \in \left[2 \times \text{TC\_INTERVAL},\; 3 \times \text{TC\_INTERVAL}\right]
\]

Varsayılan OLSR parametreleri ile (\(\text{HELLO\_INTERVAL} = 2\) s, \(\text{TC\_INTERVAL} = 5\) s):
- \(\Delta_1 \in [4\text{ s},\; 11{,}5\text{ s}]\)
- \(\Delta_2 \in [10\text{ s},\; 15\text{ s}]\)

### 5.2. Veri düzlemi kurtarma süresi (data-plane recovery)

\[
\Delta_{\text{data}} = T_{\text{succ}} - T_d
\]

burada \(T_{\text{succ}}\) — bağlantı kopmasından sonra hedefe başarıyla ulaşan
**ilk** veri paketinin gönderilme zamanı.

### 5.3. AODV için tahmini kurtarma süresi

AODV protokolü için, Hello tabanlı bağlantı kopması tespiti ve rota onarım süresi
aşağıdaki gibi tahmin edilir ([Mohammad El-Basioni, 2024](https://www.nature.com/articles/s41598-024-72983-y)):

\[
T_{\text{det\_recov}} = N_{\text{Loss}} \times T_{\text{Interv}} + 2 \times H_{\text{Avg}} \times T_{\text{Trav}} + T_{\text{MaxDiscov}}
\]

**Değişken tanımları:**

| Sembol | Tanım |
|---|---|
| \(N_{\text{Loss}}\) | `ALLOWED_HELLO_LOSS` — izin verilen kaçırılan Hello sayısı |
| \(T_{\text{Interv}}\) | `HELLO_INTERVAL` — Hello mesaj gönderim aralığı |
| \(H_{\text{Avg}}\) | Ortalama hop sayısı |
| \(T_{\text{Trav}}\) | `NODE_TRAVERSAL_TIME` — düğümler arası ortalama geçiş süresi |
| \(T_{\text{MaxDiscov}}\) | Maksimum rota keşif süresi |

### 5.4. Rota keşif süresi (Route Discovery Time)

\[
T_{\text{Discov}} = \frac{1}{N_{\text{Discov}}} \sum_{n=1}^{N_{\text{Discov}}} \left(T_{e_n} - T_{s_n}\right)
\]

burada:
- \(N_{\text{Discov}}\) — simülasyon boyunca yapılan toplam rota keşif işlemi sayısı
- \(T_{s_n}\) — \(n\)'nci rota keşif işleminin başlangıç zamanı
- \(T_{e_n}\) — \(n\)'nci rota keşif işleminin bitiş zamanı

### Önemli notlar

- **Kontrol düzlemi vs. veri düzlemi:** Kontrol düzlemi kurtarma süresi (rota tablosu
  güncellendi) ile veri düzlemi kurtarma süresi (ilk paket başarıyla iletildi) farklı
  olabilir. Veri düzlemi genellikle daha uzundur.
- **Yerel onarım vs. uçtan uca:** Yerel rota onarımı (link-local repair) kopma
  noktasındaki düğüm tarafından yapılır; uçtan uca onarım kaynak düğüme RERR gönderir
  ve kaynak yeni rota keşfi başlatır. Yerel onarım daha hızlıdır.
- AODV'de \(T_{\text{det\_recov}}\) formülü bir tahmindir; gerçek değer simülasyon
  ile ölçülmelidir.

### Birim: Saniye (s) veya milisaniye (ms).

---

## 6. Metrikler Arası İlişkiler

Beş metrik birbirinden bağımsız değildir; aralarında ödünleşimler (trade-off) vardır:

### PDR ↔ E2E Latency

- Yüksek PDR, genellikle daha düşük E2E gecikme anlamına gelir (az paket düşer,
  daha az yeniden iletim).
- Ancak kurtarma mekanizmaları PDR'yi artırırken E2E gecikmeyi de artırabilir
  (yerel onarım sırasında paketler kuyruğa girer).

### Routing Overhead ↔ PDR

- Daha fazla kontrol paketi (yüksek NRL) daha iyi rota bilgisi → daha yüksek PDR.
- Ancak aşırı kontrol trafiği bant genişliğini tüketir → veri paketleri düşer → PDR düşer.
- Bu bir ödünleşimdir; optimal nokta senaryoya bağlıdır.

### Link Break Count ↔ Route Recovery Latency

- Daha fazla bağlantı kopması → daha sık rota kurtarma → daha yüksek E2E gecikme.
- Daha hızlı kurtarma (düşük \(\Delta\)) → daha düşük E2E gecikme ama daha yüksek
  kontrol trafiği (NRL).
- Protokol tasarımı bu ödünleşimi dengelemelidir.

### Özet tablo

| Metrik | Yön | İlişki | Etki |
|---|---|---|---|
| PDR ↑ | iyi | NRL ↓ veya ↑ | Az kontrol → düşük PDR; çok kontrol → bant tüketimi |
| E2E ↓ | iyi | LBC ↓ | Az kopma → düşük gecikme |
| NRL ↓ | iyi | PDR ↔ | Optimal NRL, PDR'yi maksimize eder |
| LBC ↓ | iyi | \(\Delta\) ↓ | Az kopma → az kurtarma → düşük gecikme |
| \(\Delta\) ↓ | iyi | NRL ↑ | Hızlı kurtarma → daha çok kontrol paketi |

---

## Kaynakça (APA 7)

Badia, L., Levorato, M., & Zorzi, M. (2012). On the recovery performance of single- and multipath OLSR in wireless multi-hop networks. *Computer Networks, 56*(17), 3729–3740. https://hal.science/hal-00708684v1/document

Broyles, D., Jabbar, A., & Sterbenz, J. P. G. (2010). Design and analysis of a 3-D Gauss-Markov mobility model for highly-dynamic airborne networks. *Internetwork Research Lab, University of Kansas*. https://resilinets.org/papers/Broyles-Jabbar-Sterbenz-2010.pdf

Ceviz, O., Sadioglu, P., & Sen, S. (2022). Analysis of routing attacks in FANETs. In *Proceedings of AdHocNets 2022*. https://web.cs.hacettepe.edu.tr/~ssen/files/papers/AdhocNets22.pdf

DTIC. (n.d.). *A performance analysis of routing protocols for ad-hoc networks* (Technical Report ADA445585). U.S. Department of Defense. https://apps.dtic.mil/sti/tr/pdf/ADA445585.pdf

Mohammad El-Basioni, B. M. (2024). Intensive study, tuning and modification of reactive routing approach to improve flat FANET performance in data collection scenario. *Scientific Reports, 14*, 23738. https://www.nature.com/articles/s41598-024-72983-y

Salma Badawi Mohammed. (2021). *Performance evaluation of FANET routing protocols in varying density and mobility scenarios* [Master's thesis, Universiti Teknologi Malaysia]. http://eprints.utm.my/103613/1/SalmaBadawiMohammed2021_PerformanceEvaluationofFANET.pdf

Tho, M. C., Ly, N. T. H., Binh, L. H., & Vo, T. T. (2025). QLR-FANET: A Q-learning and rate control-based routing algorithm for flying ad hoc networks. *ETRI Journal, 47*(6), 1010–1025. https://onlinelibrary.wiley.com/doi/full/10.4218/etrij.2024-0298

---

> **Not:** Bu belgedeki matematiksel tanımlar, literatürde yaygın olarak kabul görmüş
> formülasyonlardır. Simülasyon aracına (ns-3, OMNeT++) ve protokole (AODV, OLSR, GPSR)
> göre uygulamada küçük farklılıklar olabilir. Karşılaştırmalı çalışmalarda aynı
> tanımlamaların kullanılması önemlidir.
