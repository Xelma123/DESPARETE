# AODV Kontrol Yükü Çöküşü ve OLSR Bayat Rota Problemi — Sistemik ve Teorik Nedenler

> **Tez:** AODV'nin hızlı topoloji değişimlerinde kontrol paketi seline yol açması,
> protokolün olay-tetiklemeli (event-triggered) selleme geri besleme döngüsünden ve
> tek-yol varsayımından kaynaklanır. OLSR'ın bayat/eski rota (stale route) kullanma
> ısrarı ise periyodik soft-state topoloji bilgisinin doğasında yatar — protokol
> ısrarcı değil, geçerlilik zamanlayıcılarına (validity timers) sadık kalıyor.

---

## İçindekiler

1. [AODV: Kontrol Paketi Seli (Control Overhead Collapse)](#1-aodv-kontrol-paketi-seli-control-overhead-collapse)
2. [OLSR: Bayat Rota (Stale Route) Problemi](#2-olsr-bayat-rota-stale-route-problemi)
3. [Karşılaştırmalı Analiz](#3-karşılaştırmalı-analiz)
4. [Kaynakça](#kaynakça)

---

## 1. AODV: Kontrol Paketi Seli (Control Overhead Collapse)

### 1.1. Sistemik Mekanizma: RERR → RREQ Geri Besleme Döngüsü

AODV'nin kontrol yükü çöküşü, birbirini besleyen altı mekanizmanın sistemik
birleşimidir:

#### (a) Tek-yol bağımlılığı

AODV, her kaynak-hedef çifti için **tek bir geçerli yol** (active route) kullanır.
Bir ara bağlantı kopunca rota tamamen geçersiz olur — yedek rota yoktur. Bu, AODV'nin
en temel tasarım varsayımıdır ve RFC 3561'de açıkça belirtilir ([Perkins et al., 2003](https://www.rfc-editor.org/rfc/rfc3561.html)).

**Sonuç:** Tek bir link kopması = tüm rota geçersiz = sıfırdan rota keşfi gerekir.

#### (b) Kopma → RERR → yeni RREQ zinciri

Bir bağlantı kopması algılandığında (link-layer feedback veya Hello kaybı ile),
aşağıdaki zincir tetiklenir:

```
Link kopması → RERR üretimi → RERR kaynağa iletilir
→ Kaynak yeni RREQ yayınlar → RREQ ağ genelinde selleme yapar
→ Yeni rota kurulur (veya kurulamaz)
```

Her kopma olayı bu zinciri yeniden başlatır. Eğer ağda \(F_{\text{active}}\) aktif
akış varsa ve her akışın ortalama yol uzunluğu \(h\) hop ise, rota keşif oranı
yaklaşık olarak:

\[
\lambda_{\text{disc}} \approx F_{\text{active}} \cdot h \cdot \lambda_b
\]

burada \(\lambda_b\) link başına kopma oranıdır (link breakage rate). Bu bağıntı
bir analitik sezgidir — doğrudan bir RFC formülü değildir, ancak Clausen et al.'nin
kontrol yükü modeliyle tutarlıdır ([Clausen et al., 2004](https://www.thomasclausen.net/wp-content/uploads/2015/12/2004-ACM-WINET-Analyzing-Control-Traf%EF%AC%81c-Overhead-versus-Mobility-and-Data-Traf%EF%AC%81c-Activity-in-Mobile-Ad-hoc-Network-Protoc.pdf)).

**Örnek:** 100 düğümlü ağda, 25 aktif akış, ortalama 5 hop, \(\lambda_b = 0{,}5\)
kopma/s/link ise:

\[
\lambda_{\text{disc}} \approx 25 \times 5 \times 0{,}5 = 62{,}5 \text{ rota keşfi/sn}
\]

Her keşif ağ çapında RREQ selleme yaptığında, kontrol yükü katlanarak artar.

#### (c) RREQ selleme maliyeti

Rota keşfi, RREQ paketinin tüm ağa yayın (flood) edilmesiyle yapılır. Her ara
düğüm ilk aldığı RREQ'yi yeniden yayınlar. \(N\) düğümlü bir ağda, bir RREQ
sellemesinin kontrol iletim sayısı yaklaşık \(N\)'dir (her düğüm bir kez yeniden
yayınlar). Genişleyen halka (expanding ring) arama ile bu azaltılabilir, ancak
başarısızlık durumunda TTL artırılır ve selleme tekrarlanır
([Perkins et al., 2003](https://www.rfc-editor.org/rfc/rfc3561.html)).

RREQ_RETRIES = 2 olarak ayarlanmıştır; yani başarısız keşifte ek denemeler
yapılır. RREQ_RETRIES nedeniyle başarısız keşiflerde kontrol yükü ve bekleme
süresi çarpanlı olarak artar (her deneme NET_TRAVERSAL_TIME kadar bekler).

#### (d) Pozitif geri besleme (positive feedback loop)

Yüksek mobilite altında bir pozitif geri besleme döngüsü oluşur:

```
Yüksek mobilite → çok link kopması → çok RREQ/RERR → kanal doluluğu artar
→ çarpışmalar artar → RREP/Hello/veri paketleri düşer → rota keşfi başarısız olur
→ RREQ retry (RREQ_RETRIES=2) → daha çok kontrol yükü → daha çok çarpışma
→ kontrol yükü çöküşü
```

Bu döngü, AODV'nin en kritik sistemik zayıflığıdır. Clausen et al. (2004), AODV
kontrol trafiğinin mobite ile doğrusal arttığını ve çok yüksek mobilitede
"modelden sapma" olduğunu raporlamıştır — bu sapma, ağ tıkanıklığının ve
sellemenin kontrol altından çıkmasıdır ([Clausen et al., 2004](https://www.thomasclausen.net/wp-content/uploads/2015/12/2004-ACM-WINET-Analyzing-Control-Traf%EF%AC%81c-Overhead-versus-Mobility-and-Data-Traf%EF%AC%81c-Activity-in-Mobile-Ad-hoc-Network-Protoc.pdf)).

#### (e) Zaman kararlılığı şartı (temporal stability condition)

AODV'nin keşfettiği rotanın geçerli olması için, rota keşif süresi (round-trip
time, RTT) boyunca bağlantıların canlı kalması gerekir. Eğer link ömrü rota
keşif RTT'sinden kısa ise, rota kurulmadan eskir:

\[
T_{\text{link}} \geq T_{\text{RTT}} \approx 2 \times h \times T_{\text{trav}}
\]

FANET'lerde İHA hızları 10–30 m/s olduğunda ve iletişim menzili ~250 m olduğunda,
link ömrü saniyeler mertebesindedir. Ancak RREQ sellemesi ve RREP geri dönüşü
tıkalı bir ağda saniyeler sürebilir. Bu durumda rota kurulduğu anda zaten
geçersizdir — yeni bir kopma yeni bir RREQ tetikler.

#### (f) Çift-yönlü yük şişmesi

Kontrol yükü yalnızca RREQ ile sınırlı değildir. Her kopma RERR üretir ve her
RERR kaynağa iletildiğinde kaynak yeni RREQ başlatır. Ayrıca yerel onarım
(local repair) denenebilir, bu da ek RREQ selleme turu demektir. Sonuç olarak
RREQ + RREP + RERR trafiği birlikte artar — "üçlü selleme yükü" oluşur.

### 1.2. Matematiksel Yaklaşık Model

AODV'nin normalize rota yükü (NRL) için bir basitleştirilmiş sezgisel üst sınır:

\[
\text{NRL}_{\text{AODV}} \approx \frac{\lambda_{\text{disc}} \cdot C_{\text{flood}}}{R_{\text{data}}}, \quad C_{\text{flood}} \sim O(N)
\]

burada:
- \(\lambda_{\text{disc}}\) — rota keşif oranı (sn⁻¹)
- \(C_{\text{flood}}\) — ortalama selleme maliyeti (hop bazlı iletim sayısı / keşif), \(O(N)\) büyüklüğünde
- \(R_{\text{data}}\) — başarıyla teslim edilen veri paketi sayısı (sn⁻¹)
- \(N\) — düğüm sayısı (\(C_{\text{flood}}\) içine gömülüdür)

Yüksek mobilitede \(\lambda_{\text{disc}}\) artar ama \(R_{\text{data}}\) azalır
(çok paket düşer) — NRL hem pay hem payda tarafından artar, yani "çift etki"
oluşur.

#### Rota keşif oranı için daha formel ifade

Genel halde, aktif rota kümesi \(\mathcal{R}_{\text{active}}\) için rota keşif oranı:

\[
\lambda_{\text{disc}} \approx \sum_{r \in \mathcal{R}_{\text{active}}} \sum_{\ell \in r} \lambda_\ell \cdot \Pr(r \text{ hâlâ talep ediliyor})
\]

Homojen durumda (tüm link'ler aynı \(\lambda_b\) kopma oranına, tüm rotalar \(h\) hop'a
ve tüm aktif akışlar hâlâ talep ediliyorsa), bu ifade sadeleşir:

\[
\lambda_{\text{disc}} \approx F_{\text{active}} \cdot h \cdot \lambda_b
\]

Bu bir analitik sezgidir — doğrudan bir RFC formülü değildir, ancak Clausen et al.'nin
kontrol yükü modeliyle tutarlıdır.

---

## 2. OLSR: Bayat Rota (Stale Route) Problemi

### 2.1. Sistemik Mekanizma: Periyodik Soft-State Topoloji Bilgisi

OLSR'ın bayat rota kullanması, bir hata değil — protokolün tasarım felsefesinin
doğrudan sonucudur. OLSR, proaktif (tablo-güdümlü) bir protokoldür ve topoloji
bilgisini periyodik olarak günceller. Gerçek topoloji ile düğümün bildiği topoloji
arasında her zaman bir gecikme vardır.

#### (a) Gerçek vs. bilinen topoloji

Gerçek topolojiyi \(G(t) = (V, E(t))\) ile, düğümün bildiği (öğrenmiş) topolojiyi
\(\hat{G}(t) = (V, \hat{E}(t))\) ile gösterelim. Yüksek mobilitede \(G(t)\) sürekli
değişir, ancak \(\hat{G}(t)\) yalnızca HELLO ve TC mesajları alındığında güncellenir.
Bu nedenle her zaman:

\[
\hat{G}(t) \neq G(t), \quad \text{gecikme: } \Delta t = t_{\text{learn}} - t_{\text{change}}
\]

Düğüm, \(\hat{G}(t)\) üzerinden hesapladığı rotayı kullanır — bu rota gerçek
topolojide geçerli olmayabilir.

#### (b) Kayıp mesaj belirsizliği (message loss ambiguity)

Bir HELLO mesajı alınmadığında protokol bunu hemen "link koptu" olarak yorumlamaz.
Neden? Çünkü mesaj kaybı şu nedenlerden olabilir:
- Geçici kanal koşulları (fading, girişim)
- Çarpışma (collision)
- Düğüm geçici olarak meşgul
- Asıl link kopması

Bu belirsizliği çözmek için OLSR, NEIGHB_HOLD_TIME süresince bekler. Bir komşudan
HELLO alınmazsa, NEIGHB_HOLD_TIME (= 3 × HELLO_INTERVAL) dolana kadar link hâlâ
"geçerli" kabul edilir ([Clausen & Jacquet, 2003](https://www.rfc-editor.org/rfc/rfc3626.html)).

**Sonuç:** Link gerçekten kopmuş olsa bile, düğüm onu geçerli olarak kullanmaya
devam eder — bu, "bayat rota ısrarı"nın doğrudan nedenidir.

#### (c) Geçersizleme gecikmesi (invalidation delay)

Bir link'in geçersiz sayılması için iki yol vardır:

1. **Aktif komşu TC mesajı gönderirse:** Komşu, link kaybını öğrendiğinde yeni bir
   TC mesajı gönderir. Ama komşu da NEIGHB_HOLD_TIME bekler. Sonra TC_INTERVAL
   süresince yeni TC göndermez. Bu nedenle kurtarma gecikmesi:

\[
\Delta_1 \in \left[\text{NEIGHB\_HOLD\_TIME} - \text{HELLO\_INTERVAL},\; \text{NEIGHB\_HOLD\_TIME} + \text{TC\_INTERVAL} + \text{MAXJITTER}\right]
\]

2. **Eski topoloji bilgisi zaman aşımına uğrar:** Kaynak düğüm link kaybından
   haberdar olmazsa, eski topoloji bilgisi Local Topology Set'te zaman aşımına
   uğrayana kadar bekler:

\[
\Delta_2 \in \left[2 \times \text{TC\_INTERVAL},\; 3 \times \text{TC\_INTERVAL}\right]
\]

Varsayılan OLSR parametreleri ile (HELLO_INTERVAL = 2 s, TC_INTERVAL = 5 s):
- \(\Delta_1 \in [4\text{ s},\; 11{,}5\text{ s}]\)
- \(\Delta_2 \in [10\text{ s},\; 15\text{ s}]\)

Bu, OLSR'ın bir link kopması sonrası rota tablosunu güncellemesinin **4–15 saniye**
sürebileceği anlamına gelir ([Doghri et al., 2012](https://hal.science/hal-00708684v1/document)).

#### (d) MPR kısıtı (partial topology limitation)

OLSR, tüm linkleri değil yalnızca MPR (Multi-Point Relay) seçimiyle optimize edilmiş
kısmi topoloji bilgisini yayar. Bu, kontrol yükünü azaltır ama bir trade-off yaratır:

- MPR olmayan düğümler arasındaki link'ler topoloji tablosunda görünmez
- Bir MPR düğümü kaybolduğunda, alternatif rota bilgisi zaten tabloda olmayabilir
- MPR değişikliği yeni TC mesajları gerektirir, bu da gecikme yaratır

Bu, Clausen et al. (2004) tarafından doğrusal kontrol yükü-mobilite ilişkisi olarak
modellenmiştir ([Clausen et al., 2004](https://www.thomasclausen.net/wp-content/uploads/2015/12/2004-ACM-WINET-Analyzing-Control-Traf%EF%AC%81c-Overhead-versus-Mobility-and-Data-Traf%EF%AC%81c-Activity-in-Mobile-Ad-hoc-Network-Protoc.pdf)).

#### (e) Veri göndermeden önce rota doğrulama yok

OLSR'de veri paketi gönderilmeden önce rota doğrulanmaz. Proaktif tablo mantığı
gereği, rota tablosundan en kısa yol alınır ve paket iletilir. Eğer rota bayatsa
(yani gerçek topoloji değişmişse), paket bir ara düğüme ulaşır ve orada düşürülür.
OLSR'de veri düzlemindeki düşüş, protokol düzeyinde anlık bir RERR üretmez;
düzeltme bir sonraki HELLO/TC geçersizleme döngüsüne kalır. Veri paketleri bir
sonraki topoloji güncellemesine kadar yanlış rotada iletilmeye devam edebilir.

#### (f) Temel trade-off

OLSR'ın bayat rota problemi ile kontrol yükü arasında doğrudan bir ödünleşim vardır:

| Parametre değişikliği | Bayat rota süresi | Kontrol yükü |
|---|---|---|
| HELLO_INTERVAL azalt | ↓ Azalır | ↑ Artar |
| TC_INTERVAL azalt | ↓ Azalır | ↑ Artar |
| NEIGHB_HOLD_TIME azalt | ↓ Azalır | ↑ Yanlış kopma alarmı artar |
| HELLO_INTERVAL artır | ↑ Artar | ↓ Azalır |

Bu trade-off'u çözmek için HELLO/TC periyotlarını kısaltmak stale route'u azaltır
ama kontrol yükünü artırır — yani "AODV'nin problemine düşer". Periyotları uzatmak
yükü azaltır ama bayat rota süresi uzar. Optimal nokta senaryoya bağlıdır.

---

## 3. Karşılaştırmalı Analiz

| Kriter | AODV (Kontrol Yükü Çöküşü) | OLSR (Bayat Rota Problemi) |
|---|---|---|
| **Tetikleyici** | Olay-tetiklemeli (link kopması → RERR → RREQ) | Zaman-tetiklemeli (periyodik HELLO/TC) |
| **Kontrol davranışı** | Reaktif: her kopma yeni selleme turu başlatır | Proaktif: periyodik tablo güncellemesi, kopmadan bağımsız |
| **Gecikme kaynağı** | RREQ sellemesi + RREP geri dönüşü + retry bekleme | NEIGHB_HOLD_TIME + TC_INTERVAL + MAXJITTER |
| **Gecikme büyüklüğü** | NET_TRAVERSAL_TIME × RREQ_RETRIES (~2,8 s × 2) | 4–15 s (varsayılan parametrelerle) |
| **Yük-mobilite ilişkisi** | Doğrusal artış, yüksek mobilitede pozitif geri besleme ile çöküş | Doğrusal artış, sabit periyodik yük |
| **Yedek rota** | Yok (tek yol) | Özel yedek rota mekanizması yok; ancak güncel topoloji bilgisi varsa sonraki SPF hesaplamasında alternatif yol seçilebilir |
| **Veri paketi kaybı nedeni** | Rota keşfi sırasında paketler kuyruğa girer/düşer | Bayat rota ile paketler yanlış düğüme iletilir |
| **Yüksek mobilite sonucu** | NRL ↑↑, PDR ↓↓, E2E ↑↑ | Stale route süresi ↑, PDR ↓, E2E senaryoya bağlı; kayıp paketler çoğu E2E hesabında gecikmeye dahil edilmez |
| **Matematiksel özet** | \(\text{NRL} \propto \frac{N \cdot F \cdot h \cdot \lambda_b}{R_{\text{data}}}\) | \(\Delta \in [\text{NEIGHB\_HOLD\_TIME},\; 3 \times \text{TC\_INTERVAL}]\) |
| **Çözüm yönü** | Çok-yollu (AOMDV), selleme optimizasyonu | Adaptif HELLO/TC periyodu, hızlı link algılama |

### Kök neden farkı

AODV'nin problemi **mikro-düzeyde**: her bir kopma olayı bir selleme turu tetikler
ve bu turlar art arda geldiğinde kanal tıkanır. Problem, kontrol trafiğinin veri
trafiğiyle rekabet etmesidir.

OLSR'ın problemi **makro-düzeyde**: topoloji bilgisinin güncellenmesi periyodik
olduğu için, gerçek topoloji ile bilinen topoloji arasında her zaman bir gecikme
vardır. Problem, bilgi güncelliğinin (information freshness) yetersizliğidir.

İki problem farklı düzlemlerde çalışır ama aynı kök nedene dayanır: **her iki protokol
de topoloji değişim hızına ayak uyduramamaktadır** — AODV selleme maliyetiyle,
OLSR periyodik gecikmeyle.

---

## Kaynakça (APA 7)

Clausen, T., & Jacquet, P. (Eds.). (2003). *Optimized Link State Routing Protocol (OLSR)* (RFC 3626). Internet Engineering Task Force. https://www.rfc-editor.org/rfc/rfc3626.html

Clausen, T., Laouiti, A., Muhlethaler, P., & Viennot, Q. (2004). Analyzing control traffic overhead versus mobility and data traffic activity in mobile ad-hoc network protocols. In *Proceedings of the 2nd ACM International Workshop on Performance Evaluation of Wireless Ad Hoc, Sensor, and Ubiquitous Networks (PE-WASUN '05)*. https://www.thomasclausen.net/wp-content/uploads/2015/12/2004-ACM-WINET-Analyzing-Control-Traf%EF%AC%81c-Overhead-versus-Mobility-and-Data-Traf%EF%AC%81c-Activity-in-Mobile-Ad-hoc-Network-Protoc.pdf

Doghri, I., Reynaud, L., & Guérin-Lassous, I. (2012). On the recovery performance of single- and multipath OLSR in wireless multi-hop networks. In *Ad hoc networks: Third International ICST Conference, ADHOCNETS 2011* (p. 239). Springer. https://hal.science/hal-00708684v1/document

Marina, M. K., & Das, S. R. (2001). On-demand multipath distance vector routing in ad hoc networks. In *Proceedings of the Ninth International Conference on Network Protocols (ICNP 2001)* (pp. 14–23). IEEE. https://www3.cs.stonybrook.edu/~samir/Pubs/icnp-01.pdf

Perkins, C., Belding-Royer, E., & Das, S. (2003). *Ad hoc On-Demand Distance Vector (AODV) routing* (RFC 3561). Internet Engineering Task Force. https://www.rfc-editor.org/rfc/rfc3561.html
