# Tasarım Notu: RL Tabanlı Yönlendirmede Overhead–Kurtarma Hızı Ödünleşimi

> **Amaç:** İHA sürüleri için şiddetli karıştırma ortamlarında pekiştirmeli öğrenme (RL)
> tabanlı yönlendirmede, yönlendirme yükü (routing overhead) ile rota kurtarma hızı
> arasındaki temel ödünleşimlerin (trade-off) tasarım çerçevesi.
> **Durum:** Literatürden çıkarılan analitik ödünleşimler; sayısal optimum eşiği değildir.

## Temel tez

Şiddetli karıştırmada RL tabanlı yönlendirme, rota kurtarmayı hızlandırmak için **daha fazla
gözlem, geri bildirim, keşif ve yedek yol tutma** ister; bu da yönlendirme yükünü artırır.
Yük azaltılırsa öğrenme ve kopma algılama yavaşlar, rota kurtarma gecikir. Bu, karıştırma
altında daha da keskinleşir çünkü geri bildirim (ACK/NACK) kaybı RL ödül sinyalini bozar,
bu yüzden aynı güvenilirlik için daha fazla ölçüm gerekir.

## Ödünleşim eksenleri

| Eksen | Hızlı kurtarma tarafı | Overhead tarafı | Çatışma |
|---|---|---|---|
| **Keşif–sömürü** | Yeni/alternatif rota bulmak için keşif (exploration) sıkı; ε-greedy/Softmax ile yeni next-hop deneme | Her deneme = gereksiz paket + Q-table güncelleme yükü | Fazla keşif = kontrol fırtınası; az keşif = karıştırma altında eski rota ısrarı |
| **Proaktif izleme** | HELLO/TC/D-ACK/SINR ölçümünü sıklaştır → kopmayı erken algıla | Sık ölçüm = kontrol trafiği artışı (NRL şişmesi) | OLSR NEIGHB_HOLD_TIME≈6s; sıklaştırma erken kurtarma verir ama kontrol kanalını doyurur |
| **Çok yollu yedeklilik** | Yedek rota önceden hazır → failover anlık | Çoklu rota bakım + durum senkronizasyon maliyeti | Tüm yollar karıştırmadan etkilenirse yedeklilik faydasız, sadece yük |
| **Mobilite tahmini** | Kalman/trajectory ile kopmayı önceden sezip proaktif geçiş | Konum/hız takibi + durum güncelleme + hesaplama yükü | Tahmin hatası = gereksiz pre-switch (overhead) vs geç algılama (gecikme) |
| **Federated/DRL** | Jammer'a hızlı adaptasyon (kanal/güç) | Model senkronizasyonu + yakınsama gecikmesi + iletişim yükü | Eğitim trafiğinin kendisi karıştırmaya maruz → öğrenme döngüsü bozulur |
| **Geri bildirim güvenilirliği** | Karıştırmada D-ACK/ACK kaybı → ödül sinyali bozulur | Güvenilir ödül için tekrarlı ölçüm / çoğullama → ek paket | Kısır döngü: jamming → kötü ödül → daha fazla ölçüm → daha fazla kontrol trafiği → daha fazla jamming hedefi |

## Karıştırmaya özgü keskinleşme

Standart (karıştırmasız) koşullarda bu ödünleşim yönetilebilirdir; karıştırmada üç mekanizma
ödünleşimi bozar:

1. **Ödül sinyali bozulur:** AODV'nin D-ACK tabanlı ödülü ([QLR-FANET 2025](https://onlinelibrary.wiley.com/doi/full/10.4218/etrij.2024-0298))
   ve SINR-tabanlı ödül ([Meta-MMFQ 2024](https://www.radioeng.cz/fulltexts/2024/24_03_0417_0431.pdf))
   karıştırmada gürültülüləşir → ajan yanlış öğrenir → rota kurtarma yanlış yöne gider.
2. **Kontrol kanalı çöker:** Keşif/izleme yükü arttıkça kontrol trafiği karıştırılmış kanalı
   doyurur → AODV'de RREQ broadcast fırtınası + NRL çift şişme (bkz. `12-PROTOKOL-BASARISIZLIK-MEKANIZMALARI.md` §1).
3. **Keşif maliyeti affedilemez:** Karıştırmasızda keşif "yerel maliyet" iken, karıştırmada
   keşif paketleri karıştırılmış alana yazılır ve doğrudan iletişim başarısızlığına dönüşür.

## Literatürün çerçeveyi nasıl ele aldığı

- **Keşif-exploitation dengesi:** Keşif yükünü azaltmak için fuzzy logic ile Q-value + link
  quality + access'i dengeleyen mekanizma — keşif overhead'ini azaltmadan rota kalitesini
  koruma çabası ([UCL 2023](https://discovery.ucl.ac.uk/id/eprint/10205326/1/routing_protocol.pdf)).
- **Overhead itirafı:** QSCR/QFAN değerlendirmesinde "overhead in QFAN is slightly high" —
  Q-learning yönlendirmenin kontrol yükü maliyetini kabul eder
  ([Herts 2023](https://uhra.herts.ac.uk/bitstream/handle/2299/27554/1-s2.0-S1319157823004482-main.pdf)).
- **Hibrit yaklaşım:** TARRAQ, Kalman ile kalan link süresini tahmin edip Q-learning'i sadece
  gerektiğinde devreye sokarak overhead'i %25,23 azaltır — tahmin ile keşif ihtiyacını düşürme
  stratejisi ([TARRAQ 2023](https://ar5iv.labs.arxiv.org/html/2306.17360)).
- **Katman ayrımı:** Anti-jamming RL'leri (FL-HDQN, Meta-MMFQ) overhead'i PHY'de (kanal/güç)
  yönetir; yönlendirme RL'leri (QLR-FANET) overhead'i next-hop seçiminde yönetir — iki katman
  ayrı optimize edilince bütünsel overhead-recovery dengesi kaybolur
  ([FL-HDQN 2026](https://www.mdpi.com/1424-8220/26/1/181), [QLR-FANET 2025](https://onlinelibrary.wiley.com/doi/full/10.4218/etrij.2024-0298)).

## Tasarım çıkarımları (proje için)

1. **Kopma nedenini ayırt et:** Mobilite mi karıştırma mı? Karıştırma kaynaklı kopmada
   keşfi azalt, yedek yola proaktif geç; mobilite kaynaklı kopmada keşfi sürdür.
2. **Ödül sinyalini karıştırmaya dayanıklı yap:** D-ACK yerine çoklu ölçüm + zaman-pencere
   ortalaması; tek paket kaybı ödülü bozmasın.
3. **Keşfi duruma göre uyarla:** Karıştırma yoğun → düşük keşif + yüksek sömürü (yedek yollar);
   karıştırma düşük → yüksek keşif (yeni rota keşfi).
4. **Kontrol yükünü makasla:** Keşif/izleme paketlerini düşük öncelikli kanala veya
   zamanla bölüştürülmüş (time-staggered) yayına al; kontrol fırtınasını engelle.
5. **Katman bütünleşmesi:** PHY-level anti-jamming (kanal/güç) kararı ile rota kararını
   ortak değişken üzerinden birleştir; yoksa iki katman ayrı yük üretir.

## Özet

Temel ödünleşim: **karıştırmada hızlı rota kurtarma, öğrenme sinyalini güvenilir kılmak için
daha fazla gözlem/keşif/yedek yol ister, ama bu kontrol trafiği artışı karıştırmadan etkilenen
kanalı daha da yükler.** Literatür bu gerilimi keşif-exploitation dengesi, hibrit tahmin+RL,
ve katmanlar-arası ayrım ile hafifletmeye çalışır; ancak "overhead vs kurtarma hızı" için
raporlanmış nicel optimum eşiği doğrulanmamıştır (literatürden çıkarılan ödünleşimler olarak
sunulmuştur).

---

## Kaynakça (APA 7)

Cui, Y., Zhang, Q., Feng, Z., Wei, Z., Shi, C., & Yang, H. (2023). *Topology-aware resilient routing protocol for FANETs: An adaptive Q-learning approach* (arXiv:2306.17360). arXiv. https://ar5iv.labs.arxiv.org/html/2306.17360

Hu, L., Shao, Y., Qian, Y., Du, F., Li, J., Lin, Y., & Wang, Z. (2024). Meta-reinforcement learning in time-varying UAV communications: Adaptive anti-jamming channel selection. *Radioengineering, 33*(3), 417–431. https://doi.org/10.13164/re.2024.0417

Mai, C. T., et al. (2025). QLR-FANET: A Q-learning and rate control-based routing protocol for flying ad hoc network. *ETRI Journal, 47*(6), 1015–1027. https://doi.org/10.4218/etrij.2024-0298

Ni, D., Ma, S., Du, J., Wu, Y., Zhou, C., & Xiao, H. (2026). A federated hierarchical DQN-based distributed intelligent anti-jamming method for UAVs. *Sensors, 26*(1), Article 181. https://doi.org/10.3390/s26010181

Q-learning smart clustering. (2023). A Q-learning-based smart clustering routing method in flying Ad Hoc networks. *Journal of King Saud University – Computer and Information Sciences*. https://uhra.herts.ac.uk/bitstream/handle/2299/27554/1-s2.0-S1319157823004482-main.pdf

Q-learning fuzzy logic routing. (2023). A Q-learning and fuzzy logic based routing protocol. https://discovery.ucl.ac.uk/id/eprint/10205326/1/routing_protocol.pdf

> **Şeffaflık notu:** UCL (2023) ve Herts (2023) makalelerinin tam künyeleri (yazar/cilt/sayı/sayfa)
> kaynak sayfalarında doğrulanmamıştır; başlığa-göre format kullanılmıştır. QLR-FANET tam yazar
> listesi "et al." ile belirtilmiştir. Atıf öncesi nihai kontrol önerilir. TARRAQ'ın %25,23
> overhead azaltması kaynağın özet düzeyinde belirtilen değerdir.
