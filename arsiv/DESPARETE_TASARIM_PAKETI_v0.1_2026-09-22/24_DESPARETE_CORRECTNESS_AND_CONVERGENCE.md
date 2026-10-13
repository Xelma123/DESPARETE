# DESPARETE — Doğruluk, Döngü Özgürlüğü ve Koşullu Yakınsama

**Sürüm:** 0.1 (onaylı correctness/conditional-convergence analizi)  
**Durum:** Onaylı ilk-sürüm algoritmaları ve state modelinden türetilen safety/liveness argümanı; `H_req=H_data=16` ile liveness kapsamı hizalanmıştır.  
**Tarih:** 2026-09-20

## 1. İddiaların kapsamı

Bu belge üç iddiayı birbirinden ayırır:

| İddia | Durum | Kapsam |
|---|---|---|
| Data-plane loop freedom | Safety argümanı verilir | Aynı Destination-ID/OIID alanındaki doğru çalışan node'lar; geçerli serial karşılaştırmaları ve algoritma invariants altında. |
| Stale/unsafe successor reddi | Safety argümanı verilir | ACTIVE komşu, expiry, ADS/DFSN ve feasibility kapıları doğru uygulandığında. |
| Route acquisition / recovery | Koşullu liveness argümanı verilir | Yeterince uzun süre kararlı ve erişilebilir bir yol, bounded control delivery ve DFSN isteğinin hedefe erişebilmesi altında. |

Bu belge şunları iddia etmez: kötü niyetli node'un kendi routing davranışını doğru uygulaması, jamming tespiti, her partition'da teslim, exactly-once teslim, uçtan uca ayrık yollar veya bütün koşullarda sabit yakınsama süresi. Dış radyo injection, target-origin authorization ve R1 control replay sınırı `26`daki güvenlik profiliyle ayrıca tanımlanmıştır.

## 2. Model ve varsayımlar

### 2.1 Safety varsayımları

| Kimlik | Varsayım |
|---|---|
| SA-01 | Aynı `K=(Destination-ID,OIID)` alanındaki participating node'lar onaylı handler/state-machine kurallarını uygular; dış radyo kaynaklı kabul edilen paketler ayrıca `26`daki roster/imza kapılarını geçer. |
| SA-02 | Hedef, OIID'yi restartta yeniler ve DFSN'yi tek üreticidir; ara node OIID/DFSN üretemez veya artırmaz. |
| SA-03 | `C(i,j)` sonlu olduğunda pozitiftir; potential toplaması doygunlukludur ve `∞` successor olmaz. |
| SA-04 | RFC 1982 serial kıyasındaki half-space belirsizliği fail-closed'dur; aynı saklama penceresindeki karşılaştırılabilir DFSN/ADS değerleri yarım uzayı aşmaz. [RFC 1982](https://www.rfc-editor.org/rfc/rfc1982.html) |
| SA-05 | Bir node, daha yeni aynı-OIID DFSN veya yeni OIID kabul ettikten sonra eski bağlama geri dönmez; intermediate restartı forwarding state'i siler. |
| SA-06 | Paket handler'ı §22'deki atomik olay sırasını uygular: invalidation/candidate removal, policy veya forwarding'den önce görünür olur. |
| SA-07 | `F_i[K]=FORWARDABLE` yalnız ACTIVE, fresh, finite ve feasible successor ile doğrudur; aksi durumda node data forward etmez. |

SA-01, doğrulanmış fakat kötü niyetli participating node'un algoritmayı ihlal etmesini dışlar. Sahte dış packet/kimlik taklidi için `26`daki imza kapıları tanımlıdır; compromised node davranışı için güvenlik garantisi iddia edilmez.

### 2.2 Liveness varsayımları

| Kimlik | Varsayım |
|---|---|
| LA-01 | Sink ile kaynak arasında uzunluğu `h ≤ H_data` olan, yönlü maliyeti sonlu ve komşuları ACTIVE kalacak bir yol yeterince uzun süre vardır. |
| LA-02 | Bu kararlı dönemde geçerli control mesajı tek atlamada profile ait `D_control` ve jitter bütçesi içinde en az bir kez ulaşır. |
| LA-03 | FIELD_UPDATE refresh/triggered update, `Lifetime=3.0 s` dolmadan alıcıya ulaşır; TR-03 korunur. |
| LA-04 | Feasibility starvation yeni DFSN gerektiriyorsa, `h≤H_req=16` kararlı aktif yol üzerinde talep hedefe ulaşır veya hedefin daha yeni DFSN update'i node'a ulaşır. |
| LA-05 | Yerel control/data/buffer bütçeleri ilgili meşru işlemi reddetmeyecek kadar kapasitelidir. |

`H_req=H_data=16` seçimi, LA-01'in kapsadığı en fazla 16 atlamalı data yolunu LA-04 için de kapsar. Bu, request tesliminin koşulsuz garantisi değildir; LA-02 ve kararlı ACTIVE yol varsayımı korunur.

## 3. Feasibility rank ve temel lemmalar

Bir node'un aynı OIID alanındaki sonlu feasibility distance'ı:

```text
FD_i[K] = (S_i, M_i)
```

olarak yazılsın. Successor kenarı boyunca kullanılan sıralama şu lexicographic ilişkidir:

```text
(S_i, M_i) ≺ (S_j, M_j)
  ancak ve ancak
  S_j, S_i'den tanımlı olarak daha yenidir;
  veya S_j = S_i ve M_j < M_i.
```

Bu sıra, hedefe yaklaştıkça “daha iyi metric” anlamına gelen normal sayısal sıralama değildir. Aynı DFSN segmentinde metric kesin azalır; yeni DFSN segmentine geçildiğinde sıra numarası kesin ilerler. Bu, sequenced feasibility yaklaşımının DESPARETE uyarlamasıdır. [RFC 8966](https://www.rfc-editor.org/rfc/rfc8966.html)

### Lemma 1 — Aynı DFSN'de kesin azalma

`i`, `j`yi aynı DFSN ile successor seçerse algoritma şunu zorunlu kılar:

```text
P_j < M_i
```

`j`nin kendi feasibility metriği, ilan ettiği sonlu potentialden büyük olamaz:

```text
M_j ≤ P_j
```

Dolayısıyla:

```text
M_j < M_i
```

Eşit potential feasible değildir. Bu, sadece “anlık komşu potentiali daha küçük” sezgisi değil, stored feasibility distance üzerinde kesin eşitsizliktir.

### Lemma 2 — Yeni DFSN geri dönüşü engeller

`i`, daha yeni `S_j` taşıyan ilanı kabul ettiğinde eski successor'u atomik devre dışı bırakır ve yeni DFSN bağlamında FD'yi yeniden başlatır. `j`, daha yeni DFSN altında `i`nin eski DFSN ilanını feasible kabul edemez; çünkü eski DFSN daha yeni değildir ve aynı DFSN değildir.

Bu nedenle bir paketin `i → j` geçişinde `j` daha yeni DFSN'e geçmişse, `j`nin aynı OIID içinde eski `i` bağlamına geri successor seçmesi mümkün değildir.

### Lemma 3 — Zamanla değişen state, eski kenarı tersine çeviremez

`i`, `j`den daha önce aldığı geçerli ilandan yararlanarak data gönderdiğinde, `j` paketi aldığında üç durum vardır:

1. `j` aynı DFSN'dedir: Lemma 1 uygulanır.
2. `j` daha yeni DFSN'e geçmiştir: Lemma 2 uygulanır.
3. `j` restart etmiş veya eski OIID'yi emekliye ayırmıştır: `j` eski forwarding state'i kullanmaz; yeni geçerli field kurmadan data forward etmez.

Bu, DATA paketinde DFSN taşınmamasına rağmen safety argümanının korunma nedenidir. DATA hedefi taşır; her hop kendi güncel güvenli field context'i ile işlem yapar. Eski context'e geri dönüş yasaktır.

### Lemma 4 — Withdrawal ve komşu expiry rank'i genişletmez

Withdrawal, finite candidate değildir. ACTIVE successor STALE/SUSPECT/EXPIRED olduğunda candidate kümesinden atomik çıkarılır. Feasible alternatif yoksa `P_i=∞` olur; aynı DFSN'de `FD_i` korunur, artırılmaz veya sıfırlanmaz.

Dolayısıyla maliyet yükselmesi, stale bilgi veya successor kaybı eski kötü route'u yeniden feasible yapamaz. Bu, count-to-infinity davranışını engelleyen yerel koşuldur.

## 4. Teorem — Data-plane döngü özgürlüğü

**Teorem.** SA-01…SA-07 altında, bir `K` alanında DESPARETE data forwarding graph'ı yönlü döngü içermez.

**İspat taslağı.** Aksini varsayalım: bir DATA paketi doğru çalışan node'larda `i_0 → i_1 → ... → i_n=i_0` kapalı forwarding çevrimini izlesin.

Her `i_r → i_{r+1}` kenarında node, yalnız safe successor kullanmıştır. Lemma 1 ve Lemma 2 nedeniyle her kenarda feasibility rank ya daha yeni DFSN segmentine kesin ilerler ya da aynı segmentte metric kesin azalır. Lemma 3, hoplar arasında state değişse dahi eski DFSN/OIID'e geri successor seçilemeyeceğini söyler.

Bir kapalı çevrimde rank'in başladığı değere dönmesi gerekir. Ancak SA-04 altında karşılaştırılabilir serial değerlerinde “tanımlı olarak daha yeni” ilişkisi kendi üzerine dönemeyen sıkı bir sıradır; aynı serial segmentte ise sonlu, negatif olmayan metric çevrim boyunca kesin azalır ve başlangıca dönemez. Bu çelişkidir. Dolayısıyla çevrim yoktur.

Hop Limit `H_data=16`, bu teoremin öncülü değildir. Yalnız paket hasar/kapsam sınırıdır; loop-freedom kanıtı FD/DFSN/OIID invariantlarına dayanır.

## 5. İkincil safety özellikleri

| Özellik | Argüman |
|---|---|
| STALE/SUSPECT forwarding yok | Neighbor transition, önce candidate'i kaldırır; policy bunu geri açamaz. |
| Eski ilan geri saramaz | Aynı sender instance/K/DFSN'de ADS daha yeni değilse expiry veya potential yenilenmez. |
| Restart replay'i kullanılmaz | Yeni OIID eski K'leri emekliye ayırır; intermediate restart forward state'i siler. |
| Repair sırasında unsafe detour yok | REPAIRING/UNREACHABLE `Succ=⊥` tutar; yalnız yeni safe candidate FORWARDABLE yapar. |
| DFSN request flood loop'u yok | Her Request-ID node başına en fazla bir kez iletilir ve Hop Limit azalır. |
| Redundancy ağacı ilk sürümde sınırlı | Ingress `RB∈{0,1}`; redundant forwarding iki RB=0 çıkış üretir. Aynı Data-ID duplicate cache'te bastırılır. |
| Partition iddiası aşırı değil | UNREACHABLE yalnız local field erişilemezliğidir; fiziksel ağın tümü hakkında hüküm vermez. |

`RB=1` alan bir paket, en fazla bir node'da iki immediate çıkışa ayrılır. Her çıkış `H_data=16` ile sınırlı olduğundan, iletim denemesi sayısı uygulama tekrarları hariç en fazla `2 × H_data = 32` atlama düzeyindedir. Bu exactly-once teslim garantisi değildir.

## 6. Koşullu yakınsama argümanı

### 6.1 İlk field edinimi

LA-01…LA-03 altında sink `P=0` origin FIELD_UPDATE yayar. Kararlı yol üzerindeki sinke en yakın ACTIVE node:

1. valid finite ilanı alır;
2. yeni/current DFSN bağlamında safe successor kurar;
3. kendi `P_i=C(i,j)+P_j` değerini hesaplar;
4. triggered FIELD_UPDATE ile sıradaki komşuya ilan eder.

Bu argüman yol boyunca indüksiyonla tekrarlanır. Her node yalnız sonlu, uygun successor kurar ve field, sinkten kaynak node'a doğru yayılır. Aynı DFSN'de feasibility koşulu bir node'u geçici olarak bloke ederse, LA-04 altında daha yeni target DFSN bu sınırı güvenle yeniden başlatır.

### 6.2 Dengeli profil zaman bütçesi

Kayıpsız/kararlı kontrol dönemi için profile ait muhafazakâr discovery bütçesi:

```text
Origin update wait        ≤ T_adv_refresh + J_adv + D_adv = 1.4 s
Bir relay genişleme adımı ≤ T_coalesce + J_adv + D_adv = 0.6 s
```

`h≤16` atlamalı yol için:

```text
T_discover(h) ≤ 1.4 s + 0.6 s × h
T_discover(16) ≤ 11.0 s
```

Bu, yalnız LA-01…LA-03 altında control scheduling bütçesidir; MAC contention, kalabalık topoloji, authentication overhead, fiziksel bozunma veya kayıplı tekrarlar için performans garantisi değildir.

### 6.3 Hata sonrası sonlanma

Son forwarding-grade komşu kanıtından sonra, hard link failure yoksa ilk sürümde:

```text
Data candidate kaldırma: en geç T_fresh = 3.0 s
Failure-bound probe sonucu: en geç T_fresh + T_probe_session = 4.3 s
Kayıt expiry üst sınırı: T_retention = 5.0 s
```

Seçili field-ilanı kaybolursa guard `1.5 s` sonra en çok iki solicit ile yenileme denenir; field geçersizleşip repair'e girerse en geç `T_repair_max=6.0 s` sonunda node FORWARDABLE veya UNREACHABLE'dır. Bu, hedefe erişildiği veya data teslim edildiği anlamına gelmez; yalnız local belirsizliğin sonsuz sürmediğini gösterir.

## 7. Liveness sınırları

| Durum | Protokolün garantisi | Vermediği garanti |
|---|---|---|
| Kararlı bağlı yol ve yeterli yeni field bilgisi | Safe successor kurulabilir ve data forward edilir. | Sabit gecikme/enerji optimumu. |
| Feasibility starvation ve request hedefe ulaşır | Hedef yeni DFSN üretir; node güvenli yeniden kurulum deneyebilir. | Requestin her zaman hedefe ulaşması. |
| Partition / target erişilemezliği | Bounded repair sonrası UNREACHABLE ve local delivery-failure. | Global partition tespiti veya teslim. |
| Yalnız eski/unsafe ilanlar | Forwarding yapılmaz. | Otomatik olarak daha kötü route'a geçiş. |
| İlk field edinimi | Acquisition control başlar. | İlk DATA'nın bufferlanması veya teslimi. |

## 8. Çözülen liveness kapsamı — `H_req=H_data=16`

İlk profil taslağındaki `H_req=8 < H_data=16` farkı, 8 atlamadan uzaktaki feasibility-starvation isteğinin sinke ulaşmasını engelleyebilirdi. Proje sahibi, request yayılımını `H_req=16`ya çıkararak data çapıyla hizalamayı onayladı.

Bu nedenle LA-01'deki `h≤16` kararlı yol üzerinde DFSN_REQUEST'in Hop Limit'i sinke erişmek için yeterlidir. Request-ID duplicate cache'i, yalnız ACTIVE komşulara yayılım, `N_req=2 / 4 s` alan-başı bütçesi ve `T_req_session=4 s` değişmeden kalır. Kapsamın büyümesi kontrol yükü açısından ölçülmüş bir performans sonucu değildir; kaynak sınırı olarak yalnız bu mekanizmalar iddia edilir.

Bu düzeltme safety teoremini değiştirmez. Safety zaten TTL'ye değil FD/DFSN/OIID invariantlarına dayanır; değişiklik yalnız conditional recovery liveness'in hop kapsamını data profiliyle tutarlı yapar.

## 9. Doğrulama yükümlülükleri

| Yükümlülük | Kanıt/araç türü | Durum |
|---|---|---|
| FD/DFSN/OIID invariantları | Unit/property test ve kod incelemesi | Uygulama aşamasında. |
| Serial half-space fail-closed | Sınır değer testleri | Uygulama aşamasında. |
| Timer ilişkileri TR-01…TR-12 | Config assertion ve test | İlk sürüm profili için gerekli. |
| Control duplicate/Hop Limit | Request flooding property test | Uygulama aşamasında. |
| Liveness varsayımları | Emülasyon/ölçüm veya saha doğrulaması | Simülasyon kapsam dışıdır; ayrı doğrulama planı gerekir. |
| Security varsayımları | Tehdit modeli ve authentication analizi | Güvenlik fazında. |

## 10. Onaylanan analiz sonucu

Onaylanan algoritmalar altında data-plane safety argümanı, SA-01…SA-07 varsayımlarıyla kurulmuştur. `H_req=H_data=16` onayıyla, LA-01…LA-05 altında ilk sürümün izin verdiği data-hop çapı içinde feasibility-starvation recovery için koşullu yakınsama iddiası da tutarlıdır.

Bu iddia, requestin her topolojide ulaşacağını, paket teslimini veya performans hedefini garanti etmez. Geçerli sınırlar; kararlı ACTIVE yol, bounded control delivery, target'ın çalışması ve yeterli yerel kaynak varsayımlarıdır.
