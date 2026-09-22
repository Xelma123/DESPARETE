# DESPARETE — Prior-Art Yeniden Denetimi

**Sürüm:** 0.1 (Phase 20 re-audit; teknik konumlandırma, hukuki görüş değildir)  
**Durum:** 2026-09-21 tarihinde yapılan kapsam genişletilmiş yeniden tarama. `02`deki başlangıç taramasındaki yenilik/diferansiyasyon cümlelerini bu belge sınırlar ve gerektiğinde düzeltir.  
**Tarih:** 2026-09-21

## 1. Amaç ve karar sınırı

Bu denetimin amacı, DESPARETE'nin bilinen mekanizmaları “yeni” diye sunmasını önlemek ve nihai şartnamenin teknik konumlandırma dilini belirlemektir. Patent geçerliliği, ihlal, özgürce uygulama (FTO) veya kapsamlı hukuki tarama sonucu vermez.

Bu nedenle sonuç aşağıdaki iki şeyi **söylemez**:

- “DESPARETE yenidir”;
- “DESPARETE mevcut patentleri ihlal etmez”.

Söyleyebileceği en güçlü ifade, seçili ve zaman-sınırlı taramada belirli mekanizmaların daha önce yayımlandığı veya yeterince yakın göründüğüdür.

## 2. Yöntem ve kapsam

Tarama; FANET/UAV/aviation ad-hoc, `gradient`, `potential field`, `mobility-aware`, `interference/jamming-aware`, `multipath`, `replica/adaptive forwarding`, `feasible successor` ve `route prediction` eş anlamlılarıyla yapıldı. Sonuçlar yayıncı/DOI kaydı veya patent yayını üzerinden, başlık-özet-açıklama düzeyinde karşılaştırıldı. Özellikle 2018–2025 aralığındaki FANET çalışmaları ve açık patent kayıtları dahil edildi.

Bu yöntem, Çince/Rusça tüm veri tabanları, kapalı savunma yayınları, tüm tezler, tüm patent aileleri veya claim-by-claim patent analizi değildir. Patent kaydı bir mekanizmanın varlığına işaret eder; hukuki durum veya claim kapsamı için yeterli değildir.

## 3. Yeni veya yeniden değerlendirilen yakın çalışmalar

| Kaynak | Doğrulanan yakın özellikler | DESPARETE'den görünen ayrım | Denetim sonucu |
|---|---|---|---|
| [Kan vd. 2012](https://doi.org/10.1016/j.compeleceng.2011.11.025), MHWN | Jamming dinamiği için interference-activity metriği ve proaktif multipath. | FANET değil; target-origin DFSN/FD safety veya imzalı routing state anlatmaz. | `02`de “tam metin yok” diye açık bırakılan kritik aday artık en az publisher abstract/description düzeyinde değerlendirildi; jamming metric + multipath öncüldür. |
| [Fan vd. 2018, C-OLSR](https://doi.org/10.1109/CompComm.2018.8781070), FANET | Cross-layer anti-jamming, fiziksel katman link-quality bilgisinin OLSR route kararına katılması. | Link-state/OLSR çizgisi; DESPARETE'nin field/DFSN/FD, source/origin/hop imza bileşimi yoktur. | FANET'te jamming-aware route metric yeni değildir. |
| [Pu 2018, JarmRout](https://doi.org/10.1109/ACCESS.2018.2879758), FANET | Jamming-resilient multipath; link quality, traffic load ve spatial-distance ile çoklu yol. | DESPARETE'nin multipath'ı sürekli end-to-end path seti değil, safe alternate ile bounded first-hop redundancy'dir. | FANET'te jamming + multipath yeni değildir; “conditional/bounded” farkı tek başına yenilik iddiası olamaz. |
| [Li 2019, MGRF](https://doi.org/10.1109/NaNA.2019.00032), FANET | Mobility-aware gradient routing; mobility bilgisi routing cost'a girer ve gradyan forwarding'i yönlendirir. | Kaynakta target-only freshness, feasibility distance, signed routing authority veya R1 replay görünmez. | `02` §6C-1'deki “FANET'te network-layer gradient/potential routing bulunamadı” cümlesi artık geçerli değildir. |
| [Liu vd. 2024](https://doi.org/10.1109/WCNC57260.2024.10571316), UAV multi-hop | Harmonic-function potential field ile interference ve mobility etkisini niceler; routing algoritmaları önerir. | DESPARETE'de local Q/H/U ayrımı, fail-closed freshness, safe-successor invariantı ve packet-security profile farklılaşır. | UAV multi-hop'ta potential field + interference/mobility de öncüldür. |
| [Sarı & Seçinti 2024](https://doi.org/10.1016/j.comnet.2024.110250), FANET | Jamming survivability için merkeziyet/topology-control ve pathloss temelli kararlar. | Routing field safety yerine topology control kullanır. | Jamming altında FANET dayanıklılığı geniş ve güncel bir çalışma alanıdır. |
| [Yu vd. 2025](https://doi.org/10.1109/ACCESS.2025.3583209), FANET | Spatial filtering temelli cross-layer anti-jamming routing; dynamic electromagnetic environment. | DESPARETE'nin radio kanıtını kesin jammer teşhisine çevirmeme ve crypto/wire korumaları farklıdır. | Yakın alan hâlen aktiftir; nihai yayın öncesi yeniden tarama gerekir. |

## 4. Patent/grey-literature risk sinyalleri

Bu kayıtlar claim analizi değildir. Yalnız akademik makalelerin bulunmamasının özgünlük/FTO için yeterli olmadığını gösterir.

| Yayın | Teknik yakınlık | Sonuç |
|---|---|---|
| [CN111343689A](https://patents.google.com/patent/CN111343689A/en) | High-dynamic aviation ad-hoc routing; neighbour discovery, mobility/TTI temelli greedy next-hop seçimi. | FANET/aviation routing ve komşu keşfi patent alanında mevcuttur. |
| [CN113207155B](https://patents.google.com/patent/CN113207155B/en) | Flight ad-hoc network'te connectivity estimate ve delivery prediction ile yerel replica sayısı kararı. | Connectivity/koşula göre çoğaltma fikri patent alanında görünür; DESPARETE'nin RB/fanout mekanizması hukuken ayrıştı varsayılamaz. |
| [WO2024125664A1](https://patents.google.com/patent/WO2024125664A1/en) | Flight ad-hoc network için adaptive route joint prediction. | Mobility/prediction odaklı route adaptation claimleri yakın alan oluşturur. |

## 5. Özellik bazında düzeltilmiş konumlandırma

| DESPARETE unsuru | Yeniden denetim hükmü | Nihai belgede kullanılabilecek güvenli dil |
|---|---|---|
| Gradient/potential + mobility | MGRF ve 2024 UAV potential-field çalışması nedeniyle öncüldür. | “FANET ihtiyaçları için seçilen bir gradyan/potential yaklaşımı.” |
| Interference/jamming-aware metric | Kan, C-OLSR, JarmRout ve yeni cross-layer çalışmalar nedeniyle öncüldür. | “Jamming teşhisi iddia etmeyen, gözlemsel bozulmaya tepki veren yerel maliyet bileşeni.” |
| Multipath/redundancy | JarmRout, Kan ve replica-adaptive patent nedeniyle öncüldür. | “Sınırlı first-hop redundancy profili; uçtan uca ayrıklık iddiası yoktur.” |
| Mobility/prediction | MGRF, 2024 potential field ve route-prediction patentleri nedeniyle öncüldür. | “Opsiyonel hareket kanıtını hazard'a bağlayan, kalibre edilmemiş ihtiyat girdisi.” |
| DFSN + FD + safe successor | Sequenced/feasibility yaklaşımı EIGRP/Babel/ROAM gibi ailelerde öncüldür. | “FANET için uyarlanmış safety mekanizması; yeni olduğu iddia edilmez.” |
| OIID/DFSN + local age, target-only authorization, R1 ve signed packet profile | Seçilen re-audit kaynaklarında tam aynı bileşim doğrulanmadı. | “Farklı bir güvenlik/operasyon bileşimi”; özgünlük veya patentlenebilirlik iddiası yok. |

## 6. `02` belgesine etkisi

`02`nin aşağıdaki başlangıç çıkarımları artık aktif olarak kullanılmamalıdır:

1. “FANET'te ağ-katmanı gradyan/potansiyel alan kullanan doğrulanmış protokol bulunamadı.”
2. “FANET'te potential/gradient + interference/mobility birleşimi doğrulanmış örnek vermedi.”
3. Kan vd. (2012) ayrıca okunmadan formal tasarıma geçilemez.

Bu maddeler sırasıyla MGRF, Liu vd. ve Kan'ın publisher kaydı ile aşılmıştır. `02`, başlangıç taramasının tarihsel kanıtı olarak korunur; prior-art/yenilik iddiası için `32` üstündür.

## 7. Sonuç ve zorunlu yayın dili

DESPARETE, bilinen gradyan/potential forwarding, dinamik maliyet, jamming/interference farkındalığı, mobility-aware seçim, multipath/replication veya feasibility yaklaşımının yeni sahibi olarak sunulmamalıdır. Seçili kaynakların hiçbiri, DESPARETE'nin bütün v0.1 paket/security/state bileşimini bütünüyle doğrulamadı; bu **yalnız araştırma boşluğu olabilir**, yenilik kanıtı değildir.

Bu nedenle v0.1 için izin verilen en güçlü teknik konumlandırma şudur:

> DESPARETE, bilinen dağıtık yönlendirme mekanizmalarını taktik tek-sink FANET operasyonu için; safety, freshness, sınırlı redundancy ve packet-level authentication sınırları açık biçimde bir araya getiren bir tasarım adayıdır.

Önerilen makale/protokol dili: “the design combines/adapts”, “is evaluated as”, “differs operationally from”; yasak dil: “first”, “novel”, “unprecedented”, “no prior work”, “guaranteed unique”. Resmî yayın, patent başvurusu veya ticarîleşme öncesinde yetkili patent uzmanı ile claim-level FTO taraması gerekir.
