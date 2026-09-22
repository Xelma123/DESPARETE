# DESPARETE — Uyarlamalı Politika Modeli

**Sürüm:** 0.1 (onaylı politika mimarisi; M0.1 eşik eki)  
**Durum:** Field-local STEADY/CAUTION/PROTECT ve MODE_NOTICE'un çekirdekten çıkarılması onaylıdır; evidence/dwell değerleri `21`, sayısal metrik predicate'leri `35`te verilir.  
**Tarih:** 2026-09-21

## 1. Amaç

Uyarlamalı politika, farklı bozunma koşullarında **aynı güvenli yönlendirme motorunun** ne kadar gözlem, onarım hazırlığı ve yedeklilik kullanacağını belirler. Yeni bir routing algoritması veya jamming tespit mekanizması değildir.

Politika şu güvenlik sınırlarını değiştiremez:

- yalnız ACTIVE komşu veri forwarding adayı olabilir;
- yalnız safe-successor koşulunu sağlayan aday seçilebilir;
- DFSN/OIID tazelik ve feasibility kontrolleri atlanamaz;
- riskli ya da bayat bir geri rota “acil durum” gerekçesiyle kullanılamaz;
- güvenli alternatif yoksa veri çoğaltılamaz.

Bu sınırlar, dayanıklılık politikasının FR-09 döngü güvenliğini aşmasını engeller.

## 2. Politika kapsamı: düğüm-geneli değil, alan-geneli

Politika durumu her hedef alanı için tutulur:

```text
Π_i[K] = i düğümünün K=(Destination-ID, OIID) alanı için yerel operasyonel postürü
```

Bu, v0 taslağındaki düğüm-geneli NORMAL/CRISIS fikrinden bilinçli bir ayrımdır.

| Seçenek | Sonuç |
|---|---|
| Düğüm-geneli mod | Bir hedefin successor bozulması, ilgisiz hedef akışlarında da control/redundancy maliyeti doğurabilir. |
| Alan-geneli yerel postür (öneri) | Karar, ilgili successor kümesi, alan tazeliği ve hedefe giden gözlemlerle sınırlıdır; birden çok hedefte daha az yan etki yaratır. |

Bağ gözlemleri `N_i[j]` içinde link-geneldir; bunların politikaya etkisi yalnız o linkin aday olduğu `K` alanlarında görünür. Tek-sink v0 profili için fark pratikte sınırlı olabilir, ancak genel şartnamede doğru kapsamı korur.

## 3. Politika durumları

Önerilen üç postür:

| Durum | Kesin anlam | Veri düzlemi | Kontrol/ölçüm davranışı |
|---|---|---|---|
| STEADY | Seçili safe successor ve alan hakkında yeterli güncel kanıt vardır; önemli kalıcı bozunma kanıtı yoktur. | Tek selected safe successor üzerinden iletim. | Normal gözlem ve soft-state koruma. |
| CAUTION | Bozunma eğilimi veya bilgi belirsizliği, ek doğrulama ve alternatif hazırlığını gerekçelendirir; henüz korumalı çoğaltma gerekçesi yoktur. | Tek selected safe successor üzerinden iletim. | Sınırlı daha sık gözlem/probe; güvenli alternatifleri izleme; gerektiğinde alan yenileme istemi. |
| PROTECT | Süregelen/şiddetli bozunma kanıtı vardır ve tanımlı korumalı davranışın kullanılabileceği en az bir ek safe successor mevcuttur. | Trafik sınıfı izin verirse, yalnız güvenli alternatifler üzerinden sınırlı çoğaltma. | En yüksek izinli gözlem yoğunluğu; hızlı güvenli alternatif hazırlığı ve kontrollü alan yenileme. |

**REPAIR**, **BUFFERING** ve **UNREACHABLE** politika durumları değildir. Bunlar herhangi bir postürde ortaya çıkabilen alan/packet işlemleridir. Örneğin CAUTION içindeki bir successor kaybı, otomatik olarak PROTECT'e geçiş demek değildir; önce güvenli alternatif aranır, yoksa repair akışı yürür.

## 4. Politika kanıtı: risk bileşenlerini tekrar saymama

Politika, `R(i,j)=g(H,U)` riskini tek başına mutlak bir ağ tehlikesi olarak yorumlamaz. Aşağıdaki kanıt sınıfları ayrı tutulur:

| Kanıt sınıfı | Anlamı | Uygun ilk politika etkisi | Tek başına yapamayacağı |
|---|---|---|---|
| Süregelen hazard / bozunma | Seçili successor'ın yakın karar ufkunda uygunsuzlaşma eğilimi | CAUTION; güvenli alternatif varsa PROTECT değerlendirmesi | Jamming hükmü veya loop kuralını geçersiz kılma |
| Yüksek belirsizlik | Seçili successor/alan hakkında yeterli güncel kanıt yok | CAUTION: ek ölçüm, probe, alan tazeliği doğrulaması | PROTECT çoğaltması için yeterli gerekçe olma |
| Sert successor arızası | Unicast/probe başarısızlığı veya komşunun forwarding için geçersizleşmesi | Alan repair/withdrawal işlemi; postür kanıtı yeniden değerlendirilir | Feasible olmayan successor'a geçme |
| Güvenli alternatif kullanılabilirliği | En az bir ek ACTIVE ve feasible successor var | Korumalı davranışın mümkün olup olmadığını belirler | Tek başına bozunma kanıtı olma |
| Jamming evidence | Bozunma örüntüsünün ihtiyatlı açıklama bağlamı | Denetim ve gerekirse ek gözlem bağlamı | Bağımsız “CRISIS” veya güvenlik suçu kararı |

Bu tablo, `U`nun yüksek olduğu fakat fiziksel bozunma kanıtının zayıf olduğu durumda protokolün önce doğrulama yapmasını sağlar. Salt belirsizlik, aynı veriyi iki yoldan çoğaltmak için yeterli gerekçe değildir.

## 5. Durum geçişleri

M0.1 (`35`), CAUTION için `H≥64 ∨ U≥128`, PROTECT için `H≥128` ve recovery için `H<64 ∧ U<128` predicate'lerini tanımlar. `21`deki dwell süreleriyle birlikte geçişler hâlâ “tek ölçüm” değil **sürdürülen ya da açık sert kanıt** kavramlarına dayanır.

```text
                     sustained uncertainty or hazard
          ┌────────────────────────────────────────────────┐
          │                                                ▼
       STEADY ───────────────────────────────────────► CAUTION
          ▲                                                │
          │ stable evidence held for recovery dwell        │ sustained/severe degradation
          │                                                │ + additional safe successor
          └────────────────────────── CAUTION ◄────────────┤
                                           ▲                ▼
                                           └────────── PROTECT
                                              recovery evidence held
```

| Geçiş | Giriş kanıtı | Zorunlu işlem |
|---|---|---|
| STEADY → CAUTION | Seçili successor için sürdürülen hazard, yüksek belirsizlik, alan/komşu tazelik endişesi veya açık arıza öncesi kanıt | Gözlem doğrulamasını ve güvenli alternatif değerlendirmesini artır; normal data forwarding'i safety gate içinde koru. |
| CAUTION → PROTECT | Süregelen/şiddetli bozunma kanıtı **ve** ek safe successor **ve** bu alanın trafik politikasında korumalı davranış izni | Korumalı davranışı yalnız izinli trafik için, bounded kapsamla etkinleştir. |
| CAUTION → STEADY | Giriş kanıtı kaybolur; güncel ve yeterli olumlu kanıt toparlanma bekleme süresince korunur | Artırılmış kontrolü normal düzeye indir. |
| PROTECT → CAUTION | Bozunma kanıtı azalır veya yedek uygunluğu kaybolur; toparlanma kanıtı korunur | Yeni çoğaltmayı durdur; açık çoğaltılmış paketleri duplicate kurallarıyla sonlandır. |
| PROTECT → CAUTION (zorunlu) | Ek safe successor artık yoktur | Çoğaltmayı hemen durdur; tek güvenli successor varsa CAUTION, yoksa repair/buffer akışına geç. |

PROTECT → STEADY doğrudan geçişi önerilmez: önce CAUTION'a dönmek, kontrol yoğunluğunu kademeli indirir ve flapping riskini azaltır.

## 6. Histerezis ve dwell ilkeleri

Her alan postürü için şu mantıksal parametreler gerekir:

| Parametre sınıfı | Amaç | Bu aşamadaki kural |
|---|---|---|
| Giriş kanıtı süresi | Tekil gürültüyle yükselmeyi engellemek | CAUTION/PROTECT girişi, sert arıza dışında sürekli kanıt ister. |
| Çıkış toparlanma süresi | Erken normale dönüşü engellemek | Çıkış, girişten daha uzun ya da en az eşdeğer kanıt ister. |
| Asgari PROTECT ikamet süresi | Kısa aralıklı yedeklilik aç/kapa davranışını sınırlamak | Ancak güvenli alternatif kaybı halinde derhal sonlandırılabilir. |
| Kontrol bütçesi | Birçok alan aynı anda CAUTION/PROTECT olduğunda yükü sınırlamak | Yerel bir üst sınıra tabi olmalıdır; sınır değeri daha sonra belirlenir. |
| Olay birleştirme | Aynı nedenden tekrarlanan DFSN istemi/probe fırtınasını önlemek | Aynı `K` için dedup/backoff semantiği gerekir. |

Histerezis yalnız policy postürleri içindir. Komşu ACTIVE→SUSPECT geçişi veya safe successor kaybı, ayrı güvenlik/hata davranışlarıyla derhal işlenebilir.

## 7. Politikanın izin verilen eylemleri

| Eylem | STEADY | CAUTION | PROTECT | Güvenlik sınırı |
|---|---|---|---|---|
| Pasif gözlem/normal soft-state | Evet | Evet | Evet | Komşu geçerliliğinin yerine geçmez. |
| Hedefli probe veya aktif doğrulama | Gerektiğinde | Öncelikli | Öncelikli ve sınırlandırılmış | STALE/SUSPECT'i data için geçerli yapmaz. |
| Feasible alternatif izleme | Mevcut ilanlardan | Öncelikli | Öncelikli | Yalnız safe-successor kabul koşuluyla. |
| Alan yenileme/DFSN istemi | Safety/freshness gerektiğinde | Daha erken değerlendirilebilir | Daha erken değerlendirilebilir | Ara node DFSN üretmez. |
| Tek yol data iletimi | Evet | Evet | Evet | Yalnız selected safe successor. |
| Kritik trafik çoğaltması | Hayır | Hayır | Evet, koşullu | En az iki safe successor, bounded fanout, trafik izni. |
| Alan maliyetini “daha ağır” yapma | Hayır | Hayır | Hayır | Risk zaten `C_risk`te bir kez temsil edilir; çifte sayım yasaktır. |

Özellikle PROTECT postürü, v0 taslağındaki “jamming cezası daha ağır” davranışını kabul etmez. Risk zaten onaylanan maliyet modelinde bir kez maliyete yansır; policy, ek bir maliyet çarpanı yerine kontrol ve yedeklilik davranışını değiştirir.

## 8. MODE_NOTICE'un çekirdekten kaldırılması

v0, yerel CRISIS değişiminde `MODE_NOTICE` önermişti. Alan-geneli yerel postür modelinde bu mesaj DL-014 ile çekirdekten çıkarılmıştır.

| Seçenek | Kazanç | Maliyet / risk |
|---|---|---|
| MODE_NOTICE'u yaymak | Komşulara erken durum ipucu verebilir | Yerel postürü ağ/komşu gerçeği gibi sunar; ek yük, spoofing/replay yüzeyi ve alarm yayılımı oluşturur. |
| MODE_NOTICE'u çekirdekten kaldırmak (seçildi) | Kararı doğrudan kanıta bağlı, yerel ve düşük yükte tutar | Komşuların dolaylı erken uyarı bilgisi yoktur. |

Bir komşunun kendi alan ilanı veya link ölçümü, başka düğüm için doğrudan bağ-riski kanıtı değildir. Bu nedenle öneri, MODE_NOTICE'u zorunlu kontrol mesajı olmaktan çıkarır. İleride korunacaksa yalnız doğrulanmış, tek-atlama, advisory telemetri uzantısı olarak değerlendirilmelidir; forwarding/policy kararına zorunlu girdi olamaz.

## 9. Trafik sınıfı ve redundancy bağlantısı

Politika yalnız “koruma izinli” trafik sınıflarında çoğaltma isteyebilir. Mevcut v0'daki tüm görev verisini CRISIS'te kopyalama varsayımı kabul edilmemiştir. Redundancy profili (`17`, `23`) aşağıdakileri kesinleştirir:

- hangi trafik sınıfının koruma izni taşıdığı;
- maksimum fanout ve paket kimliği;
- link/node/hata-korelasyonu iddiasının sınırı;
- duplicate bastırma ve kapatma davranışı.

## 10. Gereksinim izlenebilirliği

| Politika unsuru | Gereksinimler |
|---|---|
| Alan-geneli yerel postür | FR-02, FR-08, NFR-01, NFR-03 |
| U/H ayrımı ve doğrulama önceliği | FR-02, FR-04, FR-07, FR-11 |
| Safety gate'in değişmezliği | FR-09, FR-10, FR-13 |
| Histerezis/dwell/control budget | FR-08, NFR-01, NFR-02 |
| Koşullu PROTECT çoğaltması | FR-06, FR-12, NFR-01, NFR-02 |
| MODE_NOTICE'un çekirdekten kaldırılması | FR-07, FR-13, FR-14, NFR-01 |

## 11. Onaylanmış politika kararı

Birlikte değerlendirilmesi gereken iki değişiklik önerilir:

1. v0'ın düğüm-geneli NORMAL/CRISIS modu, alan-geneli üç postürlü `STEADY → CAUTION → PROTECT` modeliyle değiştirildi.
2. `MODE_NOTICE`, çekirdek protokolden çıkarıldı; komşu durumunun doğrudan policy girdisi olmasına izin verilmez.

**Kazanç:** Bir alandaki sorun ilgisiz alanları etkilemez; yüksek belirsizlik ile gerçek bozunma farklı davranış alır; risk çifte sayılmaz; kontrol yükü ve sahte alarm yüzeyi azalır.

**Bedel:** Biraz daha fazla hedef-alanı durumu ve komşular arasında dolaylı “erken uyarı” paylaşımının kaybı. Tek-sink profilede alan-geneli ile düğüm-geneli pratikte yakın davranır.

Bu kararlar DL-014 ile MAJOR olarak onaylanmıştır. State, timer, control-message ve redundancy bağları `17`…`23`te normatifleştirilmiştir.
