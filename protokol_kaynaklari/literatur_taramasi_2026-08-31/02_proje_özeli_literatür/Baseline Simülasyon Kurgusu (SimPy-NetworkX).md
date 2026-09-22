# SimPy/NetworkX Ortamında AODV/OLSR Baseline Simülasyon Kurgusu — Tasarım İlkeleri

> **Kapsam:** Python (SimPy + NetworkX) ortamında yazılan ad-hoc ağ simülasyonlarında
> AODV ve OLSR gibi standart yönlendirme protokollerinin temel davranışlarını adil
> biçimde modellemek için kullanılan kontrol grubu (baseline) kurgularının tasarımı.
> Bu belge, RFC standartlarına ve simülasyon metodolojisi literatürüne dayanır.

---

## İçindekiler

1. [Temel İlke: Tek Değişkenli Deney Tasarımı](#1-temel-i̇lke-tek-değişkenli-deney-tasarımı)
2. [Sabit Parametreler (Kontrol Değişkenleri)](#2-sabit-parametreler-kontrol-değişkenleri)
3. [Bağımsız Değişkenler (Tarama)](#3-bağımsız-değişkenler-tarama)
4. [Radyo Yayılım Modeli](#4-radyo-yayılım-modeli)
5. [Mobilite Modeli](#5-mobilite-modeli)
6. [Trafik Modeli](#6-trafik-modeli)
7. [MAC Katmanı Modeli](#7-mac-katmanı-modeli)
8. [Protokol Parametreleri (RFC Uyumlu)](#8-protokol-parametreleri-rfc-uyumlu)
9. [Tohum Yönetimi ve Tekrarlanabilirlik](#9-tohum-yönetimi-ve-tekranlanabilirlik)
10. [İstatistiksel Geçerlilik](#10-i̇statistiksel-geçerlilik)
11. [SimPy/NetworkX Mimari Tasarımı](#11-simpy-networkx-mimari-tasarımı)
12. [Yaygın Hatalar](#12-yaygın-hatalar)
13. [Kaynakça](#kaynakça)

---

## 1. Temel İlke: Tek Değişkenli Deney Tasarımı

Adil karşılaştırmanın temel kuralı: **aynı senaryoyu, aynı tohumla (seed), aynı koşullarda
her protokol için tekrarlamak** ([Esquius, 2014](https://upcommons.upc.edu/bitstream/handle/2099.1/10751/PFC_Marc_Esquius.pdf)).

> "Rastgele tohum değerleri konum, hareket ve bağlantı parametreleri için tüm protokoller
> test edilene kadar değiştirilmemelidir. Bu şekilde her protokol tam olarak aynı koşullar
> altında test edilir." ([Esquius, 2014](https://upcommons.upc.edu/bitstream/handle/2099.1/10751/PFC_Marc_Esquius.pdf))

Bu, SimPy/NetworkX ortamında şu anlama gelir:

- Aynı `random.seed()` değeri tüm protokoller için kullanılır
- Aynı mobilite senaryosu (düğüm pozisyonları, hızlar, yönler) üretilir ve tüm protokoller için tekrar kullanılır
- Aynı trafik desenleri (kaynak-hedef çiftleri, paket gönderim zamanları) kullanılır
- Yalnızca yönlendirme protokolü değiştirilir; diğer her şey sabittir

---

## 2. Sabit Parametreler (Kontrol Değişkenleri)

Aşağıdaki parametreler bir baseline kurgusunda sabit tutulmalıdır:

| Parametre | Önerilen Değer | Gerekçe |
|---|---|---|
| **Simülasyon süresi** | 900–1000 s | İstikrarlı metrikler için yeterli süre ([DTIC, n.d.](https://apps.dtic.mil/sti/tr/pdf/ADA445585.pdf)) |
| **Alan boyutu** | 1000×1000 m (N≤40) | Taktik FANET için literatür standardı |
| **Düğüm sayısı (N)** | 20–40 | Taktik FANET ölçeği |
| **İletişim menzili (R)** | ~250 m | 802.11b tipik değer |
| **Bant genişliği** | 2 Mb/s | 802.11b baz hız |
| **Paket boyutu** | 512 bayt | CBR/UDP için literatür standardı |
| **Trafik tipi** | CBR/UDP | Yönlendirme değerlendirmesi için standart |
| **Kaynak-hedef çift sayısı** | 10–15 | N=40 için makul yük |
| **Gönderim hızı** | 4 pkt/sn/akış | Toplam ~40–60 pkt/sn ağ yükü |
| **Mobilite modeli** | 3D Gauss-Markov (α=0.85) | FANET için önerilen |
| **İHA hızı** | 10–30 m/s | Taktik İHA hız aralığı |
| **Radyo yayılım modeli** | Two-ray ground veya log-distance | Basit ama gerçekçi |
| **MAC protokolü** | 802.11 DCF (basitleştirilmiş) | Ad-hoc standardı |

---

## 3. Bağımsız Değişkenler (Tarama)

Baseline'ın dışında, aşağıdaki değişkenler taranarak protokollerin davranışları karşılaştırılır:

| Değişken | Tarama aralığı | Amaç |
|---|---|---|
| **İHA hızı** | 5, 10, 20, 30 m/s | Mobilite etkisi |
| **Düğüm sayısı** | 10, 20, 30, 40 | Ölçeklenebilirlik |
| **Duraklama süresi (pause time)** | 0, 10, 30, 60 s | Mobilite derecesi |
| **Karıştırma gücü (JSR)** | −10, −5, 0, +5 dB | EW dayanıklılığı |
| **Karıştırıcı sayısı** | 0, 1, 2, 3 | Karıştırma yoğunluğu |
| **Karıştırıcı tipi** | Sürekli, reaktif, taramalı | Karıştırma stratejisi |

> **Önemli:** Her tarama noktasında yalnızca bir değişken değiştirilir; diğerleri sabit tutulur.
> Çok değişkenli tarama yapılırsa, faktöriyel tasarım kullanılır ve her kombinasyon için
> bağımsız tekrarlar yapılır.

---

## 4. Radyo Yayılım Modeli

### 4.1. Basitleştirilmiş model (SimPy/NetworkX için)

NetworkX'de bağlantı (edge) varlığı, düğümler arası mesafe ile belirlenir:

```python
import networkx as nx
import numpy as np

def is_link_exists(pos_i, pos_j, R=250.0):
    """İletişim menzili içinde ise bağlantı var."""
    dist = np.linalg.norm(np.array(pos_i) - np.array(pos_j))
    return dist <= R
```

### 4.2. Daha gerçekçi: Log-distance yol kaybı

```
PL(d) = PL(d₀) + 10·n·log₁₀(d/d₀)
```

burada:
- `PL(d₀)` — referans mesafe (1 m) yol kaybı
- `n` — yol kaybı üssü (2-4 arası, tipik 3.0)
- `d` — düğümler arası mesafe

### 4.3. Uyarı: Free-space yeterli değildir

Newport (2007), basit free-space modelin gerçekçi sonuç vermediğini vurgular:

> "Radyo yayılım modeli hangi varsayımları yapıyor? Bu varsayımlar ne kadar gerçekçi?
> Bu varsayımların sonuçlara etkisi nedir?" ([Newport, 2007](https://people.cs.georgetown.edu/~cnewport/pubs/NewportDartmouthThesis.pdf))

Önerilen: Asgari two-ray ground veya log-distance model kullanın. Free-space model
aşırı iyimser bağlantı kalitesi verir ve protokol karşılaştırmasını yanıltır.

### 4.4. Asimetrik bağlantılar

Gerçek ad-hoc ağlarda bağlantılar asimetrik olabilir (A, B'yi duyabilir ama B, A'yı
duyamayabilir). Baseline kurgusunda bu, sinyal gücü eşiklerine dayalı olarak
modellenmelidir ([Newport, 2007](https://people.cs.georgetown.edu/~cnewport/pubs/NewportDartmouthThesis.pdf)).

---

## 5. Mobilite Modeli

### 5.1. 3D Gauss-Markov (FANET için önerilen)

```python
# 3D Gauss-Markov mobilite modeli (basitleştirilmiş)
def gauss_markov_3d(pos, vel, alpha=0.85, mean_vel=20.0, dt=0.5):
    """
    pos: (x, y, z) mevcut pozisyon
    vel: (vx, vy, vz) mevcut hız vektörü
    alpha: korelasyon parametresi (0=bağımsız, 1=sabit hız)
    """
    # Yeni hız = alpha * mevcut + (1-alpha) * ortalama + rastgele
    new_vel = alpha * vel + (1 - alpha) * mean_vel_dir + sqrt(1-alpha²) * random
    new_pos = pos + new_vel * dt
    return new_pos, new_vel
```

### 5.2. Uyarılar

- **Random Waypoint yeterli değildir** — FANET ana senaryosu için 3D Gauss-Markov önerilir; fakat literatür karşılaştırması için ek legacy baseline olarak verilebilir
- **Duraklama süresi (pause time)** mobilite derecesini belirler; 0 = sürekli hareket
- **Başlangıç transienti:** Gauss-Markov modelinin ilk ~50 sn'si geçici (transient)
  rejimdir; metrikler bu süreden sonra toplanmaya başlanmalıdır

---

## 6. Trafik Modeli

### 6.1. CBR/UDP (baseline standardı)

```python
# SimPy ile CBR trafik üretici
import simpy

def cbr_traffic(env, source, dest, rate=4.0, pkt_size=512, sink=None):
    """Sabit bit hızında trafik üretici."""
    interval = 1.0 / rate
    while True:
        # Paket oluştur ve yönlendirme katmanına gönder
        pkt = {'src': source, 'dst': dest, 'size': pkt_size,
               'time': env.now, 'id': next_pkt_id()}
        sink(pkt)  # Yönlendirme protokolüne teslim
        yield env.timeout(interval)
```

### 6.2. Kaynak-hedef çift seçimi

- **Rastgele seçim:** N düğümden rastgele K çift seçilir
- **Sabit çiftler:** Aynı çiftler tüm protokoller için kullanılır (adil karşılaştırma için)
- **Oran:** N=40 için 10–15 akış makul yük sağlar

### 6.3. Başlangıç gecikmesi

Düğümlerin başlangıçta rastgele gecikme ile trafik göndermeye başlaması önerilir:

```python
yield env.timeout(random.uniform(0, 2.0))  # Başlangıç gecikmesi
```

Bu, tüm düğümlerin aynı anda trafik başlatmasının yarattığı yapay senkronizasyonu önler
([DTIC, n.d.](https://apps.dtic.mil/sti/tr/pdf/ADA445585.pdf)).

---

## 7. MAC Katmanı Modeli

SimPy/NetworkX ortamında MAC katmanı genellikle basitleştirilmiş olarak modellenir:

### 7.1. Basitleştirilmiş 802.11 DCF

- **İletim süresi:** `T_tx = pkt_size / bandwidth`
- **Çarpışma modeli:** Aynı anda aynı komşu alanında iletim yapan iki düğüm çarpışır
- **Yeniden iletim:** Maksimum N_retry deneme, rastgele backoff bekleme

### 7.2. Önerilen yaklaşım

SimPy'de MAC katmanı bir kaynak (resource) olarak modellenir:

```python
class SimpleMAC:
    def __init__(self, env, node_id, bandwidth=2e6):
        self.env = env
        self.node_id = node_id
        self.tx_time_per_byte = 8 / bandwidth
        self.busy = simpy.Resource(env, capacity=1)

    def send(self, pkt_size):
        """Paket gönderimi (basitleştirilmiş)."""
        with self.busy.request() as req:
            yield req
            yield self.env.timeout(pkt_size * self.tx_time_per_byte)
```

---

## 8. Protokol Parametreleri (RFC Uyumlu)

### 8.1. AODV parametreleri (RFC 3561)

| Parametre | Varsayılan Değer | Açıklama |
|---|---|---|
| HELLO_INTERVAL | 1.0 s | Hello mesaj gönderim aralığı |
| ALLOWED_HELLO_LOSS | 2 | İzin verilen kaçırılan Hello sayısı |
| LINK_LOSS_DETECTION_TIME | ALLOWED_HELLO_LOSS × HELLO_INTERVAL = 2.0 s | Bağlantı kopma algılama süresi |
| NEIGHBOR_HOLD_TIME | 3 × HELLO_INTERVAL | Komşu geçerlilik süresi (bestecil eşleşme) |
| RREQ_RETRIES | 2 | RREQ yeniden deneme sayısı |
| NET_TRAVERSAL_TIME | 2 × NODE_TRAVERSAL_TIME × NET_DIAMETER | Ağ geçiş süresi |
| NODE_TRAVERSAL_TIME | 40 ms | Düğümler arası geçiş süresi |
| NET_DIAMETER | 35 | Ağ çapı (hop) |
| PATH_DISCOVERY_TIME | 2 × NET_TRAVERSAL_TIME | Rota keşif zaman aşımı |
| ACTIVE_ROUTE_TIMEOUT | 3.0 s | Aktif rota zaman aşımı |
| LOCAL_ADD_TTL | 2 | Yerel onarım TTL artışı |

> Kaynak: ([Perkins et al., 2003](https://www.rfc-editor.org/rfc/rfc3561.html))

### 8.2. OLSR parametreleri (RFC 3626)

| Parametre | Varsayılan Değer | Açıklama |
|---|---|---|
| HELLO_INTERVAL | 2.0 s | Hello mesaj gönderim aralığı |
| TC_INTERVAL | 5.0 s | Topology Control mesaj aralığı |
| NEIGHB_HOLD_TIME | 3 × HELLO_INTERVAL = 6.0 s | Komşu geçerlilik süresi |
| TOP_HOLD_TIME | 3 × TC_INTERVAL = 15.0 s | Topoloji geçerlilik süresi |
| WILLINGNESS | 3 (default) | MPR olma isteği |
| REFRESH_INTERVAL | HELLO_INTERVAL | Bilgi yenileme aralığı |
| MAXJITTER | HELLO_INTERVAL / 4 | Anti-collision rastgele gecikme |

> Kaynak: ([Clausen & Jacquet, 2003](https://www.rfc-editor.org/rfc/rfc3626.html);
> [Doghri et al., 2012](https://hal.science/hal-00708684v1/document))

### 8.3. Dikkat: Parametre adilliği

Protokol parametreleri değiştirilirken şu ilkelere uyulmalıdır:

1. **RFC varsayılan değerleri kullanın** — özel optimize edilmiş değerler karşılaştırmayı bozar
2. **Aynı NET_DIAMETER ve NODE_TRAVERSAL_TIME kullanın** — ağ çapı her iki protokol için aynı olmalı
3. **Hello aralıklarını aynı tutmayın** — AODV ve OLSR'ın Hello aralıkları farklıdır (1 s vs 2 s),
   bu protokollerin doğal davranışıdır; yapay olarak eşitlemeyin
4. **Zamanlayıcı tutarlılığını koruyun** — NEIGHB_HOLD_TIME = 3 × HELLO_INTERVAL ilişkisi her iki protokolde korunmalıdır

---

## 9. Tohum Yönetimi ve Tekrarlanabilirlik

### 9.1. Tohum stratejisi

```python
import random
import numpy as np

SEEDS = [42, 123, 456, 789, 1024, 2048, 3072, 4096, 8192, 16384]

for seed in SEEDS:
    random.seed(seed)
    np.random.seed(seed)

    # Mobilite senaryosu oluştur (aynı seed → aynı senaryo)
    mobility = generate_mobility(nodes=N, area=(1000, 1000, 300),
                                  speed=20, alpha=0.85, duration=900, seed=seed)

    # Trafik desenini oluştur (aynı seed → aynı trafik)
    traffic = generate_traffic(nodes=N, flows=10, rate=4.0,
                               duration=900, seed=seed)

    # Her protokol için aynı senaryoyu çalıştır
    for protocol in ['AODV', 'OLSR']:
        results = run_simulation(protocol, mobility, traffic, seed=seed)
        save_results(protocol, seed, results)
```

### 9.2. İki tohum katmanı

- **Senaryo tohumu:** Mobilite ve trafik deseni için — tüm protokoller için aynı
- **Protokol tohumu:** Rastgele backoff, jitter vb. için — protokole özel olabilir ama
  yine de sabitlenmelidir

> **En iyi uygulama:** Mobilite, trafik ve karıştırma desenlerini önceden üretip
> dosyaya kaydedin, sonra her protokol için aynı dosyayı tekrar oynatın (replay).
> Bu, tohum sapmalarını tamamen ortadan kaldırır.

> **Ayrı RNG akışları:** Mobilite, trafik, MAC jitter/backoff ve protokol zamanlayıcıları
> için ayrı rastgele sayı üreteci akışları kullanın. Tek bir global RNG'ye güvenmek,
> protokoller arasında desenkronizasyona yol açabilir.

### 9.4. Tekrarlanabilirlik kontrol listesi

- [ ] Aynı Python sürümü
- [ ] Aynı SimPy/NetworkX sürümü
- [ ] Aynı NumPy sürümü
- [ ] Tohum değerleri kod içinde sabit
- [ ] Mobilite senaryosu dosyaya kaydedilip yeniden yükleniyor
- [ ] Trafik deseni dosyaya kaydedilip yeniden yükleniyor
- [ ] Rastgele sayı üreteci `random.seed()` ve `np.random.seed()` ile her protokol öncesi sıfırlanıyor

---

## 10. İstatistiksel Geçerlilik

### 10.1. Minimum tekrar sayısı

- **Minimum 10 bağımsız tekrar** (farklı tohumlarla) her senaryo/protokol kombinasyonu için
- Her tekrar, farklı mobilite ve trafik deseni üretir ama aynı istatistiksel özelliklere sahiptir
- Metrikler 10 tekrarın ortalaması olarak raporlanır

### 10.2. Güven aralıkları

```python
from scipy import stats

def confidence_interval(data, confidence=0.90):
    """Verilerin %90 güven aralığı."""
    n = len(data)
    mean = np.mean(data)
    sem = stats.sem(data)
    h = sem * stats.t.ppf((1 + confidence) / 2, n - 1)
    return mean, mean - h, mean + h
```

> Marina & Das (2001), her veri noktasının 10 farklı rastgele mobilite senaryosunun
> ortalaması olduğunu ve %90 güven aralığı gösterdiğini belirtir
> ([Marina & Das, 2001](https://www3.cs.stonybrook.edu/~samir/Pubs/icnp-01.pdf)).

### 10.3. Isınma süresi (warmup)

- İlk 50–100 sn'lik simülasyon verisi atılır (transient rejim)
- Metrikler yalnızca kararlı durum (steady-state) verisinden hesaplanır
- Simülasyon süresi = ısınma + ölçüm süresi (örn. 100 sn ısınma + 800 sn ölçüm = 900 sn)

---

## 11. SimPy/NetworkX Mimari Tasarımı

### 11.1. Önerilen modüler mimari

```
simulation/
├── config.py           # Tüm parametreler ve sabitler
├── mobility.py         # 3D Gauss-Markov mobilite modeli
├── radio.py            # Radyo yayılım ve bağlantı modeli
├── mac.py              # Basitleştirilmiş 802.11 DCF
├── routing/
│   ├── base.py         # Soyut yönlendirme arayüzü
│   ├── aodv.py         # AODV uygulaması (RFC 3561)
│   └── olsr.py         # OLSR uygulaması (RFC 3626)
├── traffic.py          # CBR trafik üretici
├── metrics.py          # PDR, E2E, NRL, LBC, kurtarma süresi
├── runner.py           # Ana simülasyon koordinatörü
└── analysis.py         # Sonuç analizi ve istatistik
```

### 11.2. Soyut yönlendirme arayüzü

```python
from abc import ABC, abstractmethod

class RoutingProtocol(ABC):
    """Tüm yönlendirme protokolleri için ortak arayüz."""

    @abstractmethod
    def initialize(self, nodes, links):
        """Protokol başlatma (rota tabloları, zamanlayıcılar)."""
        pass

    @abstractmethod
    def on_packet_send(self, src, dst, pkt):
        """Uygulama katmanından paket geldiğinde çağrılır."""
        pass

    @abstractmethod
    def on_packet_receive(self, node, pkt):
        """MAC katmanından paket alındığında çağrılır."""
        pass

    @abstractmethod
    def on_link_break(self, node_i, node_j):
        """Bağlantı kopması algılandığında çağrılır."""
        pass

    @abstractmethod
    def on_timer(self, node, timer_type):
        """Zamanlayıcı tetiklendiğinde çağrılır (Hello, TC, route timeout)."""
        pass

    @abstractmethod
    def get_routing_overhead(self):
        """Toplam kontrol paketi sayısını döndürür."""
        pass
```

### 11.3. NetworkX graf yönetimi

> **Uyarı — Oracle routing riski:** NetworkX'in gerçek topoloji grafiği yalnızca
> simülatör motoru tarafından fiziksel bağlantı kontrolü için kullanılmalıdır.
> AODV/OLSR rota kararları, simüle edilmiş kontrol paketlerinden öğrendikleri
> bilgiyle yapmalıdır — `nx.shortest_path` gibi fonksiyonlar yalnızca **oracle
> üst sınır referansı** olarak kullanılmalı, protokol davranışı olarak değil.

```python
import networkx as nx

class NetworkGraph:
    """Zamanla değişen ağ topolojisi yöneticisi."""

    def __init__(self, nodes):
        self.graph = nx.Graph()
        self.graph.add_nodes_from(nodes)

    def update_links(self, positions, R=250.0):
        """Mevcut pozisyonlara göre bağlantıları günceller."""
        self.graph.remove_edges_from(list(self.graph.edges()))
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                if is_link_exists(positions[i], positions[j], R):
                    self.graph.add_edge(i, j)

    def get_neighbors(self, node):
        """Düğümün mevcut komşularını döndürür."""
        return list(self.graph.neighbors(node))

    def has_route(self, src, dst):
        """Kaynak ile hedef arasında yol var mı?"""
        return nx.has_path(self.graph, src, dst)

    def get_shortest_path(self, src, dst):
        """En kısa yolu döndürür (referans için)."""
        try:
            return nx.shortest_path(self.graph, src, dst)
        except nx.NetworkXNoPath:
            return None
```

### 11.4. Graf yönü ve asimetrik bağlantılar

Yukarıdaki `nx.Graph()` simetrik (çift yönlü) bağlantılar varsayar. Bu baseline
için uygundur, ancak belgeleme amacıyla açıkça belirtilmelidir. Asimetrik RF
bağlantıları modellenirse, `nx.DiGraph()` kullanılmalı veya komşular AODV/OLSR'a
sunulmadan önce yalnızca çift yönlü bağlantılar filtrelenmelidir.

### 11.5. SimPy ortam yönetimi

```python
import simpy

class SimulationRunner:
    """SimPy tabanlı simülasyon koordinatörü."""

    def __init__(self, config):
        self.config = config
        self.env = simpy.Environment()
        self.metrics = MetricsCollector()

    def run(self, protocol_name, mobility, traffic, seed):
        # Tohumları sıfırla
        random.seed(seed)
        np.random.seed(seed)

        # Ağ oluştur
        nodes = list(range(self.config.N))
        graph = NetworkGraph(nodes)

        # Yönlendirme protokolünü yükle
        if protocol_name == 'AODV':
            routing = AODVRouting(self.env, graph, self.config)
        elif protocol_name == 'OLSR':
            routing = OLSRRouting(self.env, graph, self.config)

        # Mobilite sürecini başlat
        self.env.process(self.mobility_process(mobility, graph))

        # Trafik süreçlerini başlat
        for flow in traffic:
            self.env.process(self.traffic_process(flow, routing))

        # Isınma süresi
        self.env.run(until=self.config.warmup_time)

        # Metrik toplamayı başlat
        self.metrics.start_collection()

        # Simülasyonu çalıştır
        self.env.run(until=self.config.sim_duration)

        return self.metrics.get_results()
```

---

## 12. Yaygın Hatalar

| Hata | Etki | Çözüm |
|---|---|---|
| Farklı tohumlarla farklı protokolleri çalıştırmak | Adil olmayan karşılaştırma | Aynı tohum, aynı senaryo |
| Free-space yayılım modeli kullanmak | Aşırı iyimser bağlantı | Two-ray veya log-distance |
| 2D mobilite modeli kullanmak | 3D FANET dinamiklerini kaçırmak | 3D Gauss-Markov |
| Isınma süresi olmadan metrik toplamak | Transient etki | İlk 50-100 sn atla |
| Tek tekrar yapılması | İstatistiksel güvenilmezlik | Min. 10 tekrar |
| Protokol parametrelerini yapay eşitlemek | Doğal davranışı bozmak | RFC varsayılanlarını kullan |
| MAC katmanını atlamak | Çarpışma modeli yok | Basitleştirilmiş 802.11 DCF ekle |
| **Kontrol ve veri paketleri aynı kuyrukta işlemek** | Yanlış gecikme ölçümü | Kontrol ve veri paketleri metriklerde ayrı etiketlenmeli, fakat kanal/MAC kapasitesi için aynı ortamda rekabet etmelidir; QoS önceliği ancak açıkça modellenirse kullanılmalıdır |
| Rota keşif süresini gecikmeye dahil etmemek | E2E gecikme eksik | Rota keşif gecikmesi ölçüme dahil |
| Asimetrik bağlantıları modellememek | Gerçekçi olmayan topoloji | Sinyal gücü eşik tabanlı bağlantı |

## 13. Kontrol Grubu (Baseline) Aileleri

Bir SimPy/NetworkX simülasyonunda, aşağıdaki baseline aileleri adil karşılaştırma
için kullanılır:

| Baseline | Açıklama | Amaç |
|---|---|---|
| **Sabit/Bağlantılı (sanity)** | N=20, hareket yok, kayıp yok | PDR ≈ 1 doğrulaması; protokol doğru çalışıyor mu? |
| **Mobilite-only** | Hareketli, kayıp yok | Mobilite etkisi; AODV keşif / OLSR stale route |
| **RFC-default AODV** | AODV, RFC 3561 varsayılan parametreleri | Referans davranış |
| **RFC-default OLSR** | OLSR, RFC 3626 varsayılan parametreleri | Referans davranış |
| **Oracle shortest-path** | NetworkX `nx.shortest_path` ile ideal rota | Üst sınır; hiçbir protokol bundan daha iyi olamaz |
| **Stres baseline** | Mobilite + RF karıştırma | EW dayanıklılığı; protokollerin zayıflıkları |

### Sanity doğrulama testleri

Simülasyon doğrulanırken şu testler yapılmalıdır:

1. **Statik ağ, bağlı:** PDR ≈ 1 olmalıdır (yakınsama sonrası)
2. **Tek link kopması:** AODV RERR/RREQ üretir; OLSR HELLO/TC zaman aşımından sonra güncellenir
3. **Hareket/kayıp yok:** OLSR yükü periyodik kalır; AODV yükü yalnız keşif sırasında oluşur
4. **Olay izleri:** RFC beklentileri veya ns-3 davranışı ile karşılaştırma

---

## Kaynakça (APA 7)

Clausen, T., & Jacquet, P. (Eds.). (2003). *Optimized Link State Routing Protocol (OLSR)* (RFC 3626). Internet Engineering Task Force. https://www.rfc-editor.org/rfc/rfc3626.html

Doghri, I., Reynaud, L., & Guérin-Lassous, I. (2012). On the recovery performance of single- and multipath OLSR in wireless multi-hop networks. In *Ad hoc networks: Third International ICST Conference, ADHOCNETS 2011* (p. 239). Springer. https://hal.science/hal-00708684v1/document

DTIC. (n.d.). *A performance analysis of routing protocols for ad-hoc networks* (Technical Report ADA445585). U.S. Department of Defense. https://apps.dtic.mil/sti/tr/pdf/ADA445585.pdf

Esquius, M. (2014). *Evaluation of MANET routing protocols* [Bachelor's thesis, Universitat Politècnica de Catalunya]. https://upcommons.upc.edu/bitstream/handle/2099.1/10751/PFC_Marc_Esquius.pdf

Marina, M. K., & Das, S. R. (2001). On-demand multipath distance vector routing in ad hoc networks. In *Proceedings of the Ninth International Conference on Network Protocols (ICNP 2001)* (pp. 14–23). IEEE. https://www3.cs.stonybrook.edu/~samir/Pubs/icnp-01.pdf

Newport, C. (2007). *Simulating mobile ad hoc networks: A quantitative evaluation of common MANET simulation models* [Master's thesis, Dartmouth College]. https://people.cs.georgetown.edu/~cnewport/pubs/NewportDartmouthThesis.pdf

Perkins, C., Belding-Royer, E., & Das, S. (2003). *Ad hoc On-Demand Distance Vector (AODV) routing* (RFC 3561). Internet Engineering Task Force. https://www.rfc-editor.org/rfc/rfc3561.html

---

> **Not:** Bu belge, SimPy/NetworkX ortamında yazılacak bir simülasyon için metodolojik
> çerçevedir. Kod örnekleri şematiktir; gerçek uygulamada hata yönetimi, loglama ve
> doğrulama (validation) adımları eklenmelidir. RFC parametre değerleri simülasyon
> ortamına uyarlanırken ağ çapı (NET_DIAMETER) ve düğüm geçiş süresi (NODE_TRAVERSAL_TIME)
> senaryoya göre ayarlanmalıdır.
