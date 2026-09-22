# Yüksek Mobiliteli 3D Taktik İHA Ağlarında Yönlendirme Protokolleri — Karşılaştırma

Bağlam: Elektronik harp (EH) — RF karıştırma (jamming) ve GPS-denied/spoofing — altındaki 3D FANET / taktik İHA mesh ağları. Sütunlar kullanıcının istediği tanımlara göre düzenlenmiştir; hücre değerleri proje bilgi tabanındaki doğrulanmış kanıtlarla ([FANET'te Elektronik Harp Şartları...](https://www.perplexity.ai/computer/tasks/08fea210-b91b-4a45-aee8-9d2edb8e70ae)) ve RFC'lerle ([RFC 3561](https://www.rfc-editor.org/rfc/rfc3561.html), [RFC 3626](https://www.rfc-editor.org/rfc/rfc3626.html)) uyumludur.

| Protokol | Kategori | Rota Keşif Mantığı | Karıştırma Altındaki Başarım | GPS Bağımlılığı | Temel Kırılma Noktası |
|---|---|---|---|---|---|
| **OLSR** | Proaktif (tablo-güdümlü); link-state | Çok-Nokta Aktarım (MPR) seçimi ile iki-atlamalık komşuları kapsar; periyodik **HELLO** (2 s) ve **TC** (5 s) paketleriyle topoloji tablolarını sürekli güncel tutar; rota veri trafikten bağımsız, önceden hazır olur ([RFC 3626](https://www.rfc-editor.org/rfc/rfc3626.html)) | Periyodik kontrol trafiği zamanlayıcıya bağlı olduğu için yükü nispeten sabit kalır; ancak HELLO/TC'yi bastıran (kontrol-kanalı) bir karıştırıcı, veri kanalını bozmadan topoloji görüşünü çökertebilir. Komşuluk kaybı ilanı NEIGHB_HOLD_TIME (6 s) dolana kadar gecikir; kurtarma sınırları Δ₁∈[4; 11,5] s, Δ₂∈[10; 15] s. Ampirik OLSR kurtarma süresi ortalama **10,6 s** (4,8–14,5 s) | Yok | Stale topoloji + algılama gecikmesi: karıştırmanın yarattığı bağlantı kopmasını HELLO kaybı gibi dolaylı, gecikmeli algılar; yüksek mobilitede periyodik tablolar çabuk eskir ve kontrol yükü sabit kalıp verim düşer |
| **AODV** | Reaktif (talep-üzerine); mesafe-vektör | İletişim gerektiğinde kaynak **RREQ** yayınlar; hedef/ara düğüm **RREP** ile yanıt verir; kopan bağlantıda **RERR** üretilir. Hedef sıra numaralarıyla döngüsüz rota kurulur; yerel onarım TTL=½·hop+LOCAL_ADD_TTL ile sınırlandırılır ([RFC 3561](https://www.rfc-editor.org/rfc/rfc3561.html)) | Her kopan rota yeni RREQ selleme turu tetikler; karıştırma altında yük çift-taraflı şişer (RREQ_RETRIES=2 ile NET_TRAVERSAL_TIME=2,8 s çarpılır). RREQ'leri de bastıran bir karıştırıcı yeniden keşfi tamamen tıkayabilir. Standart AODV'de güvenlik yok — black-hole/sinkhole'e açıktır | Yok | Rota keşif gecikmesi + yeniden selleme: karıştırma altında yedek rota yoktur, tek yol kopunca veri akışı tamamen durur; selleme fırtınası (broadcast storm) yoğunluğu artar |
| **GPSR** | Konum/coğrafi-tabanlı; durumsuz | Açgözlü iletim (greedy forwarding): hedefe coğrafi olarak en yakın komşuya iletir; açgözlü başarısız olursa çevre (perimeter) iletimiyle düzeltir. Yalnızca tek-atlamalık komşu konum bilgisini tutar — düğüm başına durum minimumdur ([Karp & Kung, GPSR](https://www.cs.cornell.edu/people/egs/615/gpsr.pdf)) | Beacon (konum yayın) kaybı altında komşuluk tablosu bozulur; 3D FANET'te topoloji değişimine AODV'den daha yavaş uyum sağladığı, PDR'yi düşürdüğü gözlenmiştir. Karıştırıcı 8→1 m/s hızla hareket edince teslim başarı oranı %10'a kadar düşer; GPSR rota bilgisinin güncellenmesini beklediği için daha hızlı bozulur | **Tam** — düğümlerin ve hedefin konumunu GPS/lokasyon servisinden alır | GPS kaynağı/çürümesi: GPS jamming konum bilgisini anında bozar; GPS spoofing düğümlere sahte konum enjekte ederek yönlendirme döngüsü ve boş (void) bölgeler yaratır. Konum hatası + boşluk (local maxima) zaten en zayıf halkadır |
| **AOMDV** | Reaktif çok-yollu; AODV uzantısı | Tek bir RREQ selleme turunda birden çok **döngüsüz, bağ-ayrık (link-disjoint)** yol keşfeder; "advertised hopcount" ile döngüsüzlük sağlanır, çoğaltılmış RREQ kopyalarından yedek ters yollar türetilir. Bir yol kopunca yedek yola geçer; yalnızca tüm yollar kopunca yeniden keşif başlar ([Marina & Das, AOMDV](https://www3.cs.stonybrook.edu/~samir/Pubs/icnp-01.pdf)) | AODV'ye göre daha dayanıklı: karıştırma tek bir yolu kopardığında yedek yol anında devreye girer, rota kurtarma gecikmesini azaltır. Ancak ek RREP/RERR trafiği keşif yükünü artırır; korelasyonlu karıştırma (çoklu yolu aynı anda kesen) veya yoğun topoloji değişimi tüm yolları geçersizleştirebilir ve keşif tıkanabilir | Yok | Yol korelasyonu + keşif yükü: bağ-ayrık yollar yine de ortak coğrafi bölgeden geçiyorsa tek bir karıştırıcı hepsini birden kesebilir; çok-yollu keşfin ek kontrol yükü yoğun karıştırma altında selleme fırtınasını ağırlaştırır |

---

## Kritik notlar (yorumlama çerçevesi)

1. **Tek-metrik yanılgısı:** Karıştırma altında PDR tek başına yanıltıcıdır. Reaktif karıştırıcıda gönderici PSR %99–100 kalırken alıcı PDR %0'a düşebilir — saldırı gönderici tarafından görünmez kalır ([Xu et al.](https://www.winlab.rutgers.edu/~trappe/Papers/JamDetect_Mobihoc.pdf)).

2. **Boşluk (proje varlık gerekçesi):** OLSR, AODV, GPSR ve AOMDV'nin **RF karıştırma altında saniye ölçeğinde rota kurtarma gecikmesi** bildiren doğrudan birincil kaynak literatürde bulunamamıştır; bu boşluk TÜBİTAK projesinin ölçeceği şeydir.

3. **Evrensel sıralama verilemez:** Karıştırma altındaki başarım; karıştırıcı tipine (sürekli/reaktif/taramalı/takipçi), mobilite modeline, düğüm yoğunluğuna, MAC/PHY katmanına ve trafik yüküne bağlıdır. Yukarıdaki değerler davranışsal eğilimleri yansıtır, mutlak bir sıralama önermez.

---

## Kaynakça (APA 7)

Clausen, T., & Jacquet, P. (Eds.). (2003). *Optimized Link State Routing Protocol (OLSR)* (RFC 3626). Internet Engineering Task Force. https://www.rfc-editor.org/rfc/rfc3626.html

Doghri, I., Reynaud, L., & Guérin-Lassous, I. (2012). On the recovery performance of single- and multipath OLSR in wireless multi-hop networks. In *Ad hoc networks: Third International ICST Conference, ADHOCNETS 2011* (p. 239). Springer. https://hal.science/hal-00708684v1/document

Karp, B., & Kung, H. T. (2000). GPSR: Greedy perimeter stateless routing for wireless networks. In *Proceedings of the 6th Annual International Conference on Mobile Computing and Networking (MobiCom '00)* (pp. 243–254). ACM. https://www.cs.cornell.edu/people/egs/615/gpsr.pdf

Marina, M. K., & Das, S. R. (2001). On-demand multipath distance vector routing in ad hoc networks. In *Proceedings of the Ninth International Conference on Network Protocols (ICNP 2001)* (pp. 14–23). IEEE. https://www3.cs.stonybrook.edu/~samir/Pubs/icnp-01.pdf

Perkins, C., Belding-Royer, E., & Das, S. (2003). *Ad hoc On-Demand Distance Vector (AODV) routing* (RFC 3561). Internet Engineering Task Force. https://www.rfc-editor.org/rfc/rfc3561.html

Won, C., Youn, J.-H., & Ali, H. (2006). Impact of high-mobility radio jamming in large scale wireless sensor networks. In *IFIP EUC Workshops Proceedings*. https://dl.ifip.org/db/conf/euc/eucw2006/WonYA06.pdf

Xu, W., Trappe, W., Zhang, Y., & Wood, T. (2005). The feasibility of launching and detecting jamming attacks in wireless networks. In *Proceedings of the 6th ACM International Symposium on Mobile Ad Hoc Networking and Computing (MobiHoc '05)* (pp. 46–57). ACM. https://www.winlab.rutgers.edu/~trappe/Papers/JamDetect_Mobihoc.pdf

> **Şeffaflık notu:** Karp & Kung (2000) ve Marina & Das (2001) için sayfa aralıkları, bu seminer makalelerin yerleşik bibliyografik künyelerinden alınmıştır.
