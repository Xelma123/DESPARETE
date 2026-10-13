# DESPARETE — Metrik Profili M0.1

**Sürüm:** M0.1 — A/M1 yönünün sayısal başlangıç profili  
**Durum:** Onaylı `DESIGN-ONLY` referans profili; kalibre edilmiş performans veya deployment kabulü değildir.  
**Tarih:** 2026-09-21

## 1. Amaç, kapsam ve yetki

Bu belge, `34`te seçilen görev öncesi sabit ortak profil yönünü somutlaştırır. M0.1, bütün forwarding node'ların aynı yerel gözlemden aynı `Q/H/U/R` değerini ve aynı link maliyetini üretmesi için tamsayı kurallarını verir.

```text
Q ─────────► C_quality(Q)
H,U ─► R=max(H,U) ─► C_risk(R)
C = 16 + C_quality + C_risk
```

M0.1, `11` ve `12`deki semantik ayrımları değiştirmez; `19`daki fixed-point potential formatını değiştirmez; `15`teki politika eylemlerini genişletmez. `Q/H/U/R` yalnız yerel `i → j` linki içindir. Hiçbiri jamming teşhisi, kopma olasılığı, global risk veya safety-gate istisnası değildir.

Bu sayılar, platform/mission verisi olmadan seçilmiş şeffaf başlangıç değerleridir. Uçuş, throughput, enerji, optimum rota veya düşük yanlış-alarm iddiası vermez. Bu nedenle M0.1, `29`daki tüm deployment kapıları geçene kadar yalnız `DESIGN-ONLY` statüsündedir.

## 2. Ortak artefakt ve görev öncesi admission

| Öğeler | M0.1 değeri / kural |
|---|---|
| `MetricProfile-ID` | `M0.1`; wire alanı değildir. |
| Protokol sürümü | `Ver = 1`. |
| CostQuantum | Bir unsigned tamsayı maliyet kuantasıdır; fiziksel birimi yoktur. Bu belgedeki bütün maliyetler bu kuantadadır. |
| Profil içeriği | Bu belgedeki Q/H/U algoritmaları, tablolar, eşikler, `C_hop`, doygunluk ve test vektörlerinin tamamı. |
| Dağıtım | Görev öncesinde güvenilir mission provisioning yoluyla bütün forwarding node'lara aynı artefakt yüklenir. |
| Değişim | Uçuş içinde veya çalışan field bağlamında profil değiştirilemez. Yeni profil, eski field/metric state temizlenmiş yeni operasyon bağlamı gerektirir. |

Operasyon öncesi admission, forwarding rolündeki her node'un `MetricProfile-ID` ve artefakt içeriğinin aynı olduğunu doğrulamak **ZORUNDADIR**. Bunu gösteremeyen node, görevde DESPARETE forwarding rolüne alınmamalıdır. M0.1 bu denetimin taşıma biçimini veya config-hash algoritmasını tanımlamaz; bu, güvenilir mission provisioning sorumluluğudur.

`19`da packet içi MetricProfile-ID bulunmadığından, bir node uçuş sırasında başka bir node'un gizli konfigürasyon uyuşmazlığını algılayamaz. Bu eksiklik CAPABILITY TLV ile giderilemez; CAPABILITY forwarding güvenliğini değiştiremez. Çalışma-anı uyumsuzluk tespiti istenirse `34` seçenek B kapsamında yeni wire sürümü gerekir.

## 3. Ortak sayısal alan ve gözlem girdileri

`Q`, `H`, `U` ve `R` kapalı `[0,255]` tamsayı aralığındadır. `Q` arttıkça mevcut doğrudan teslim koşulu daha iyidir; `H`, `U` ve `R` arttıkça ihtiyat gereği artar. Tüm ara hesaplar geniş tamsayıyla yapılır; yalnız bu belgede açıkça belirtilen `floor`, `min` ve `max` işlemleri uygulanır. Kayan nokta, platforma özgü yuvarlama veya gizli yumuşatma yasaktır.

M0.1 yalnız ACTIVE authenticated direct peer için forwarding kararını etkileyen metrik üretir. UNQUALIFIED, STALE, SUSPECT veya EXPIRED kayıtlarında toplanan ölçüm yalnız diagnostic olabilir; successor adayını veya policy'yi değiştiremez.

### 3.1 Uygun doğrudan sonuç

Bir uygun sonuç, `i`nin ACTIVE `j`ye yaptığı ve sonucu yerel link/MAC katmanından kesinleşen bir hedefli unicast denemesidir. Sonuç şunları taşır:

| Alan | Kural |
|---|---|
| `t` | Sonucun kesinleştiği yerel monotonic zaman. |
| `success` | Nihai link teslimi başarılıysa `1`, başarısızsa `0`. |
| `r` | Başarılı sonuçtaki ilk gönderimden sonraki link-katmanı yeniden iletim sayısı; ilk denemede başarı için `0`. Başarısız sonuçta değer kullanılmaz. |

Uygun sonuç, forwarding-grade DATA veya node'un başlattığı matching PROBE/PROBE_REPLY doğrulamasıyla ilişkilendirilebilir. Sadece alınmış paket, tek yönlü broadcast, uzaktan ilan edilen metrik veya imza doğrulamasız sonuç uygun kanıt değildir. Link katmanı `success` ve `r` bilgisini sağlayamıyorsa M0.1 o platformda deploy edilemez; `29`daki DC-11 bunu kapılar.

Başarılı bir sonucun skor katkısı şöyledir:

```text
s(r) = floor(255 / (1 + r))
```

Başarısız sonucun skor katkısı `0`dır. Bu kural, yeniden iletimi doğrudan güncel kaliteye yansıtır; aynı olayı ayrıca `J` veya ayrı bir maliyet terimi olarak saymaz.

### 3.2 Mevcut kalite `Q`

Her `T_metric_epoch = 0.5 s` anında node, son `W_Q = 2.0 s` içindeki en yeni en çok `16` uygun sonucu seçer. Bu seçilmiş kümenin büyüklüğü `N_Q`dir.

```text
Q = floor(sum(s(r) veya 0) / N_Q),              N_Q > 0
Q = son geçerli Q değeri,                       N_Q = 0
```

İlk uygun sonuç henüz yoksa Q tanımsızdır ve kayıt forwarding metrik kaynağı olarak kullanılamaz. `N_Q=0` durumunda eski Q iyiymiş gibi yenilenmez; §3.4teki belirsizlik `255` olur. Bu ayrım, sessizliğin yapay iyi kalite sayılmasını önler.

### 3.3 Hazard `H`

M0.1 hazard'ı, ardışık kısa pencerelerdeki **sürekli kötüleşme** ile sınırlı tutar. Her 0.5 saniyelik bağımsız epoch için `q_e`, o epochta kesinleşen uygun sonuçlardan §3.1 kuralıyla hesaplanır.

Son üç epochun her birinde en az dört uygun sonuç varsa ve aşağıdaki iki azalış da pozitifse:

```text
d_1 = q_(e-2) - q_(e-1) > 0
d_2 = q_(e-1) - q_e     > 0
H = min(255, d_1 + d_2)
```

aksi hâlde `H = 0`dır. Bu nedenle tek kayıp, tek pencere düşüşü veya yetersiz örnek hazard yükseltmez; bunların bilgi etkisi `U`da görünür. Optional radyo/hareket kanıtları M0.1'de telemetry bağlamıdır ve `Q/H/U/R` değerlerini değiştirmez.

### 3.4 Belirsizlik `U`

`U`, sonuç yaşı ve son iki saniyedeki örnek yetersizliğinin en kötü değeridir:

```text
U = max(U_age, U_sample)
```

`a`, en son uygun sonucun yaşıdır.

| `a` aralığı | `U_age` |
|---|---:|
| `< 0.5 s` | 0 |
| `0.5…<1.0 s` | 32 |
| `1.0…<1.5 s` | 64 |
| `1.5…<2.0 s` | 128 |
| `2.0…<3.0 s` | 192 |
| `≥ 3.0 s` veya hiç sonuç yok | 255 |

| `N_Q` | `U_sample` |
|---|---:|
| `12…16` | 0 |
| `8…11` | 32 |
| `4…7` | 64 |
| `1…3` | 128 |
| `0` | 255 |

`a ≥ 3.0 s`, `T_fresh=3.0 s` ile uyumludur; komşu state geçişi ayrı safety işlemidir. U'nun yükselmesi tek başına ACTIVE olmayan komşuyu kullanılabilir yapmaz ve fiziksel linkin kesin kötü olduğunu söylemez.

### 3.5 Risk `R`

```text
R = max(H, U)
```

Bu, M0.1'in seçilmiş M1 risk birleştirmesidir. `Q`, `R`ye dahil edilmez. `R`nin aynı anda hem `H` hem `U` yüksek olduğunda toplamsal büyümesi istenirse bu, yeni metrik profile kararıdır.

## 4. Maliyet dönüşümleri

Her ACTIVE uygun link için:

```text
C_hop     = 16
C(i,j)    = 16 + C_quality(Q(i,j)) + C_risk(R(i,j))
```

`C_hop` pozitiftir; diğer iki terim negatif değildir. Maliyet yalnız güvenli adaylar arasında tercih içindir. Komşu/field/feasibility kapısında başarısız link, bu tabloda yüksek maliyet bulunsa bile aday kümesine girmez.

### 4.1 Kalite cezası

| Q aralığı (iyi → kötü) | `C_quality` |
|---|---:|
| `224…255` | 0 |
| `192…223` | 2 |
| `160…191` | 4 |
| `128…159` | 8 |
| `96…127` | 16 |
| `64…95` | 32 |
| `32…63` | 64 |
| `0…31` | 128 |

### 4.2 Risk cezası

| R aralığı (düşük → yüksek) | `C_risk` |
|---|---:|
| `0…31` | 0 |
| `32…63` | 2 |
| `64…95` | 4 |
| `96…127` | 8 |
| `128…159` | 16 |
| `160…191` | 32 |
| `192…223` | 64 |
| `224…255` | 128 |

Toplama geniş tamsayıyla yapılır. `AdvertisedPotential + C(i,j) > 0xFFFFFFFE` ise sonuç `∞`ye doyurulur; candidate sonlu olmaz ve mevcut `withdrawal/repair` davranışı uygulanır. Negatif maliyet, kayan nokta, tablo dışı değer veya farklı CostQuantum ile hesaplanan potential geçersizdir.

## 5. M0.1 politika eşikleri

M0.1, `15`teki postür eylemlerini değiştirmeden onların sayısal giriş predicate'lerini tanımlar:

| Predicate | Kural | Zaman koşulu |
|---|---|---|
| `CautionEvidence` | `H ≥ 64` **veya** `U ≥ 128` | Koşul `T_caution_evidence = 1.5 s` sürekli sağlanırsa STEADY → CAUTION değerlendirilir. |
| `ProtectEvidence` | `H ≥ 128` | Koşul `T_protect_evidence = 2.5 s` sürekli sağlanırsa; ayrıca ek safe successor, forwarding eligibility ve traffic izinleri varsa CAUTION → PROTECT değerlendirilir. Yüksek U tek başına PROTECT değildir. |
| `RecoveryEvidence` | `H < 64` **ve** `U < 128` | Koşul `T_recovery_evidence = 4.0 s` sürekli sağlanırsa mevcut policy recovery kuralı uygulanır. |

`Q` düşük fakat stabil ise, önce `C_quality` üzerinden güvenli alternatif tercih edilir; Q tek başına policy postürü değiştirmez. Sert link arızası, safety/repair işlemi olarak policy timerından önce işlenir. `T_protect_min=2.0 s`, ek safe successor veya forwarding eligibility kaybında beklenmez.

## 6. Algoritma entegrasyonu

Her `T_metric_epoch`te, ACTIVE komşu için şu işlem yürütülür:

```text
OnMetricEpoch(j):
    update N_i[j].Q, H, U, R using §§3.1–3.5
    update N_i[j].C using §4
    for each K where j is a cached candidate:
        RecomputeField(K)       # existing FD/freshness/ACTIVE gates remain first
        EvaluatePolicy(K)       # §5 predicates and existing evidence timers
```

Bir değer bandı değişmediğinde yeni triggered FIELD_UPDATE üretmek yasaktır. Band değişimi sonucu selected successor veya local potential değişirse, `23`teki olağan `ScheduleFieldUpdate` akışı `T_coalesce`, `T_urgent` ve per-field rate sınırlarına bağlı kalır. M0.1, DFSN/OIID/ADS üretmez, FD'yi sıfırlamaz ve policy'nin safety sonucunu geri açmasına izin vermez.

## 7. Gözlemlenebilirlik ve uyum

Node, en az aşağıdaki local telemetry alanlarını görünür kılmalıdır:

```text
metric_profile_id = "M0.1"
metric_epoch_processed
metric_insufficient_sample
metric_hazard_raised
metric_uncertainty_band_changed
metric_cost_band_changed
metric_cost_saturated
metric_preflight_reject
```

Bu olaylar paket başına export edilmek zorunda değildir; `28`deki counter/coalescing kuralları uygulanır. Metrik telemetry'si routing girdisi olarak uzaktan kabul edilmez.

Bir M0.1 uyumlu implementasyon aşağıdakileri sağlamalıdır:

1. Bütün hesaplarda bu belgedeki tamsayı işlemlerini ve aralık tablolarını aynen kullanmak.
2. ACTIVE olmayan peer metriklerinin forwarding veya policy etkisi olmadığını göstermek.
3. Profil preflight kanıtı yokken node'u forwarding rolüne almamak.
4. Band değişiminde yalnız mevcut recompute/update rate kurallarıyla ilan üretmek.
5. §8 test vektörlerini birebir üretmek.

## 8. Deterministik test vektörleri

| Kimlik | Girdi | Beklenen sonuç |
|---|---|---|
| M0-TV-01 | Son 2 s içinde dört sonuç: success `r=0`, success `r=1`, success `r=3`, failure. | Skor toplamı `255+127+63+0=445`; `Q=floor(445/4)=111`; `C_quality=16`. |
| M0-TV-02 | Üç ardışık 0.5 s epoch, her birinde `N≥4`: `q_(e-2)=224`, `q_(e-1)=176`, `q_e=112`; son sonuç yaşı `<0.5 s`, `N_Q=12`. | `H=(224-176)+(176-112)=112`; `U=0`; `R=112`; `C_risk=8`; toplam `C=16+16+8=40`. |
| M0-TV-03 | `Q=240`, son 2 s içinde `N_Q=2`, son sonuç yaşı `0.6 s`; yeterli üç-epoch trend yok. | `H=0`; `U=max(32,128)=128`; `R=128`; `C_quality=0`; `C_risk=16`; `C=32`; yalnız CautionEvidence vardır. |
| M0-TV-04 | En son uygun sonuç yaşı `2.2 s`, `N_Q=0`; son Q değeri `200`. | `U=max(192,255)=255`; `R=255`; `C_quality=2`; `C_risk=128`; `C=146`. Komşu state ayrıca kendi `T_fresh` kuralını uygular. |
| M0-TV-05 | `AdvertisedPotential=0xFFFFFFE0`, `C=40`. | Doygun sonuç `∞`; bu candidate sonlu successor olamaz. |
| M0-TV-06 | Preflight manifesti M0.1 artefaktıyla uyuşmayan node. | Node forwarding rolüne admission alamaz; `metric_preflight_reject` görünür olur. |

## 9. İzlenebilirlik ve açık sınır

| Konu | Kaynak / etki |
|---|---|
| Q/H/U/R semantiği | `11` |
| Additif maliyet ve safety ayrımı | `12`, `13`, `23` |
| Alan/policy timerları | `15`, `21`, `22` |
| Fixed-point potential ve wire sınırı | `19` |
| Metric event/counter sözleşmesi | `28` |
| Link-feedback ve platform kapasite kanıtı | `29` DC-11 |
| İnsan karar kaydı | `05` DL-042; karar seçenekleri `34` |

M0.1, OQ-022'yi **tasarım düzeyinde** kapatır: referans implementasyon için sayı ve dönüşüm artık belirsiz değildir. Platforma uygun kalibrasyon, farklı radio feedback biçimi, live profile değişimi, enerji metriği, optional radyo/mobility kanıtını routing girdisi yapma veya deployment kabulü ise yeni profile/deployment kararı gerektirir.
