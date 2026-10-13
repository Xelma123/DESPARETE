# DESPARETE — Alternatifler, Multipath ve Seçici Redundancy

**Sürüm:** 0.1 (onaylı ilk-sürüm profili)  
**Durum:** Onaylanan safe-successor, policy, repair ve bounded-fanout kararlarına dayanır.  
**Tarih:** 2026-09-20

## 1. Amaç ve terminoloji

Bu belge üç farklı kavramı ayırır:

| Terim | Anlam |
|---|---|
| Alternate successor | Aynı `K` için safe-successor koşulunu sağlayan, selected successor olmayan ACTIVE komşu. |
| Local failover | Selected successor kaybedilince, diğer safe successor'a tek-kopya forwarding ile geçiş. |
| Redundant forwarding | Aynı koruma-izinli data paketinin sınırlı sayıda farklı immediate safe successor'a kopyalanması. |

Bu ayrım önemlidir: alternate tutmak veya failure sonrası failover yapmak, veri çoğaltmak değildir. Multipath burada yük dengeleme, sürekli çok-yollu trafik veya uçtan uca ayrık rota garantisi anlamına gelmez.

## 2. Koruma kapsamı ve dürüst garanti sınırı

DESPARETE her forwarding düğümünde yalnız ilk sonraki atlamayı ve komşunun ilan ettiği alanı bilir. Bu nedenle şu garanti verilebilir:

> Aynı redundant forwarding işleminde seçilen kopyalar, farklı immediate ACTIVE safe successor komşularına gönderilir.

Şunlar garanti edilmez:

- sonraki atlamalardan itibaren node-disjoint veya link-disjoint uçtan uca yollar;
- bağımsız radyo/girişim/jamming hata alanları;
- kopyaların hiç yeniden birleşmemesi;
- en az bir kopyanın teslimi;
- tam olarak bir kez teslim.

Bu sınır, “multipath” iddiasını yerel olarak doğrulanabilir first-hop divergence ile sınırlar. Daha güçlü ayrıklık için path-vector, kaynak rota veya ağ-geneli koordinasyon gerekir; bunlar mevcut sade distance-vector alan tasarımının kapsamı dışındadır.

## 3. Alternate successor saklama

Her `F_i[K]`, selected successor yanında bir **alternate successor kümesi** tutabilir. Kümedeki her üye aşağıdaki tüm koşulları sürekli sağlamalıdır:

1. Komşu ACTIVE'dir ve forwarding-grade kanıt günceldir.
2. Alan ilanı, mevcut `K`, OIID ve DFSN bağlamında geçerlidir.
3. İlan feasibility koşulunu sağlar.
4. Yönlü link maliyeti sonludur.
5. Aday selected successor ile aynı immediate node kimliğine sahip değildir.

Alternatifler, ek bir çok-yollu keşif veya ağ-geneli duyuru ile kurulmaz; normal alan ilanlarından türetilir. CAUTION/PROTECT postürü bu ilanların gözlemini/doğrulanmasını önceliklendirebilir, fakat safety gate'i gevşetemez.

Bir aday yukarıdaki koşullardan birini kaybederse alternate kümesinden derhal çıkarılır. Bu, kopma anında stale yedeğin kullanılmasını önler.

## 4. Local failover

Local failover, §16 post-failure repair'in ilk ve tercih edilen sonucudur:

```text
Selected successor başarısız
        ↓
Başka safe alternate var mı?
  ├─ Evet → deterministik en iyi alternate'i selected successor yap; tek kopya ile sürdür.
  └─ Hayır → withdrawal + DFSN istemi + REPAIRING/UNREACHABLE.
```

Bu işlem STEADY, CAUTION veya PROTECT postüründe aynı safety koşullarıyla çalışır. PROTECT, failure sonrası unsafe route seçme izni vermez.

## 5. Redundant forwarding etkinleştirme

Bir düğüm `i`, bir data paketini yalnız aşağıdaki koşulların **tamamı** sağlanırsa çoğaltabilir:

1. `Π_i[K] = PROTECT`tir.
2. Paket, kaynak/uygulama trafik profili tarafından **protection-eligible** olarak işaretlenmiştir.
3. Seçilmiş successor yanında en az bir alternate successor vardır.
4. Tüm seçilecek next hop'lar o anda ACTIVE ve safe successor'dır.
5. Paket için kullanılabilir bir redundancy budget vardır.
6. Yerel control/data kaynak bütçesi çoğaltmaya izin verir.

Koşullardan biri sağlanmazsa, paket selected safe successor üzerinden tek kopya olarak ilerler veya §16'daki repair/buffer davranışına girer. Redundancy, tek güvenli yol bulunamadığında “çare” değildir.

### 5.1 Protection-eligible trafik

v0.1, protection eligibility'yi DATA `DFlags` bit 0 ile taşır (`19`); hangi uygulama trafik sınıflarının bu biti ayarlayabileceği ise profile-bağlı kalır. Bu nedenle sabit bir trafik sınıfı listesi seçilmemiştir:

- `eligible`: PROTECT postüründe, diğer koşullar sağlanırsa bounded redundancy kullanılabilir.
- `not eligible`: Her postürde tek-kopya forwarding uygulanır.

Kontrol mesajları, data redundancy kuralına otomatik olarak dahil edilmez. Her kontrol mesajının kendi tekrar, acknowledgement veya dissemination semantiği control-message fazında belirlenir.

## 6. Bounded replication budget

Her protection-eligible data paketi, kaynakta ya da ingress'te sonlu bir `Replication-Budget` ile ilişkilendirilir. Budget'ın semantiği:

| Kural | Anlam |
|---|---|
| Sonluluk | Bir paket için toplam replica üretimi sınırsız olamaz. |
| Tüketim | `Replication-Budget`, **ek** kopya üretim hakkını sayar. Primary forwarding budget tüketmez; her ek kopya üretiminde tüm çıkış kopyalarında budget bir azaltılır. |
| Tekrarsızlık | Budget tükendiğinde downstream düğümler paketi yeniden çoğaltmaz. |
| Fanout sınırı | Bir çoğaltma olayında seçilen toplam immediate successor sayısı (primary dahil) `MaxReplicaFanout` profil sınırını aşamaz. İlk sürümde `MaxReplicaFanout=2`dir: primary + en çok bir alternate. |
| Kaynak sınırı | Postür PROTECT olsa bile node yerel data/control bütçesi nedeniyle çoğaltmayı reddedebilir. |

İlk sürümde `MaxReplicaFanout=2` seçilmiştir. Başlangıç Replication-Budget, paket/traffic profile tarafından taşınır; `RB=1`, bu node'da en çok bir ek kopya üretimine izin verir ve oluşan iki çıkış kopyasında `RB=0` kalır. En az iki farklı safe successor olmadan redundancy aktif olamayacağı zaten zorunlu mantıksal koşuldur.

### 6.1 Çoğaltma işlemi

Redundancy etkinleştiğinde `i`:

1. selected successor'ı primary kopya için korur;
2. alternate kümesinden, deterministik tercih sırasıyla en çok bir ek immediate successor seçer;
3. aynı `Data-ID` ve aynı redundancy grubu ile kopyalar üretir;
4. ek kopya üretilmişse primary ve secondary çıkışta güncellenmiş replication budget; her çıkışta bağımsız hop-limit taşır;
5. budget tükendiğinde downstream tekrar çoğaltmasını engeller.

Kopyalar, `i`den sonra farklı safe successor'lar seçilse bile daha sonra aynı node veya radyo hata alanında birleşebilir. Bu durum çoğaltma mantığını geçersiz kılmaz fakat beklenen faydanın sınırıdır.

## 7. Duplicate işleme ve teslim semantiği

Bir redundancy grubu için tüm kopyalar aynı değişmez `Data-ID`yi taşır. Hedef ve ara düğümler, tanımlı soft-state ömrü boyunca görülen `Data-ID`leri duplicate bastırma önbelleğinde tutar.

| Olay | Davranış |
|---|---|
| İlk geçerli kopya alınır | Normal forwarding veya hedefte teslim işlemi uygulanır. |
| Aynı `Data-ID` tekrar alınır | Yeniden teslim/yeniden çoğaltma yapılmaz; duplicate sayacı güncellenebilir. |
| İlk kopyanın iletimi belirsiz/hatalı | §16'nın in-flight ve packet-id kuralları uygulanır; duplicate cache exactly-once garantisi değildir. |
| Cache ömrü biter | Aynı Data-ID, kaynak sıra alanı ve güvenlik kapsamı ile birlikte değerlendirilmelidir; değerler wire/timer fazında belirlenir. |

Data-ID cache, aynı kopyanın tekrar işlenmesini engeller; ilk kez gören downstream node'da `RB>0` ise tek başına yeniden fanout'u engellemez. Bu nedenle ilk sürümde ingress `Replication-Budget` değeri `0` veya `1` ile sınırlanır. `RB=1`de ilk redundant forwarding sonrasında iki çıkışın RB'si `0` olur; downstream yeniden çoğaltma yapamaz. Uçtan uca exactly-once teslim, uygulama/taşıma katmanı veya gelecekteki ayrı güvenilirlik profiline bırakılır.

## 8. Redundancy deactivation

Yeni kopya üretimi şu olaylardan herhangi birinde durur:

- `Π_i[K]` PROTECT'ten CAUTION/STEADY'ye geçer;
- gerekli alternate successor ACTIVE/safe olmaktan çıkar;
- paket budget'ı tükenir;
- yerel kaynak bütçesi çoğaltmayı reddeder;
- paket yaşam süresi/hop-limit sona erer;
- hedef veya ara düğüm duplicate cache'te aynı Data-ID'yi görür.

Deactivation, in-flight kopyaları geri çağıramaz. Bunlar normal duplicate/hop-limit kurallarıyla sonlanır. Yeni çoğaltma üretmek durur.

## 9. Bilinçli olarak dışlanan davranışlar

| Davranış | Neden çekirdekte yok? |
|---|---|
| Sürekli ECMP/load splitting | Paket sıralaması, adalet, korelasyon ve dinamik yük geri bildirimi için ek model gerektirir. |
| Ağ-geneli ayrık rota keşfi | NFR-01/NFR-03 ile çatışan ekstra kontrol ve durum gerektirir. |
| Her CRISIS/PROTECT paketini çoğaltma | Kontrol ve enerji yükünü sınırsız artırır. |
| Jamming doğrulandıysa otomatik multipath | Jamming evidence kesin hüküm değildir; safe alternatif de olmayabilir. |
| STALE/SUSPECT yedeği “son şans” kullanımı | Loop-safety ve komşu geçerliliğini ihlal eder. |

## 10. Düşünce deneyi iz sürmeleri

| Vaka | Beklenen davranış |
|---|---|
| PROTECT, iki safe successor, eligible trafik | Budget uygunsa farklı iki immediate komşuya bounded kopyalar; duplicate bastırma çalışır. |
| PROTECT, yalnız bir safe successor | Tek-kopya forwarding; redundancy etkinleşmez. |
| Primary kopar, alternate safe | Local failover; yeni çoğaltma policy/budget koşuluna bağlıdır. |
| Primary ve secondary daha sonra birleşir | Bir kopya duplicate olarak bastırılabilir; uçtan uca ayrıklık iddiası yapılmaz. |
| Secondary STALE olur | Alternate kümesinden çıkar; yeni kopya üretimi durur. |
| Birçok downstream node PROTECT | Budget tüketildiği için üstel yeniden çoğaltma olmaz. |

## 11. Gereksinim izlenebilirliği

| Unsur | Gereksinimler |
|---|---|
| Safe alternate kümesi ve failover | FR-02, FR-06, FR-09, FR-12 |
| PROTECT + eligible + budget kapısı | FR-12, NFR-01, NFR-02, NFR-03 |
| First-hop divergence sınırı | FR-12, NFR-06 |
| Data-ID ve duplicate bastırma | FR-13, NFR-01 |
| Deactivation ve kaynak bütçesi | FR-08, FR-12, NFR-01, NFR-02 |

## 12. Onaylanan mimari karar ve açık profil sınırı

DESPARETE, sürekli multipath veya load splitting yerine aşağıdaki dar kapsamlı redundancy modelini kullanır:

```text
Safe alternates always maintained opportunistically
        +
PROTECT posture + protection-eligible packet + finite budget
        +
distinct immediate safe successors
        =
bounded first-hop-diverse redundant forwarding
```

**Kazanç:** Mevcut alan bilgisinden ek küresel keşif olmadan, kontrol/enerji bütçesi altında seçici hata toleransı sağlar; first-hop riskine maruziyeti azaltabilir.

**Bedel:** Uçtan uca ayrıklık, teslim garantisi ve sıralama garantisi yoktur; Data-ID, budget ve duplicate state gerektirir. `MaxReplicaFanout=2` ile daha geniş fanout bilinçli olarak dışlanmıştır; başlangıç budget'ı traffic profile'ın açık parametresidir.

Bu seçim, packet semantiği, control/message tasarımı, timerlar ve kaynak karmaşıklığını etkileyen; proje sahibi tarafından onaylanmış MAJOR karardır. İlk-sürümde `RB ∈ {0,1}` sınırı da `23`teki algoritma kararıyla onaylanmıştır.
