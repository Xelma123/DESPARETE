# OLSRv2 — gerçekleme tasarımı (kod yazılmadan önce)

> 11 Ekim 2026 · K-229 · K-230 · kaynaklar `protokol_kaynaklari/` (`v2/02` R5): RFC 7181 (OLSRv2) · RFC 6130 (NHDP) · RFC 5444 (paket/mesaj biçimi) · RFC 5497 (zaman TLV'leri) · RFC 5148 (titreşim) · RFC 7779 (DAT metriği) · güncelleyenler RFC 7183 · 7187 · 7188 · 7466 · hakem olsrd2 (OONF, `uygulama_kaynaklari/olsrd2/`, commit `477e716`).

## 1 · Kaynak sırası ve karar kuralı

1. **RFC'ler — normatif metin.** MUST ve SHOULD uygulanır, MAY beyan edilir (19 Eylül kuralı; AODV K-208, OLSR K-223 ile aynı).
2. **olsrd2 — yalnız RFC'nin sustuğu ya da birden çok okumaya izin verdiği yerde hakem.** RFC'nin dışındaki eklemeleri alınmaz.
3. **Bizim seçimimiz — yalnız ikisinin de sustuğu yerde**, gerekçesiyle beyan tablosunda.

## 2 · Okuma notları (RFC 6130 · NHDP)

- **Bilgi tabanları:** Link Set (L_neighbor_iface_addr_list, L_HEARD_time, L_SYM_time, L_quality, L_pending, L_lost, L_time) · 2-Hop Set (N2_…, N2_2hop_addr, N2_time) · Neighbor Set (N_neighbor_addr_list, N_symmetric) · Lost Neighbor Set (NL_neighbor_addr, NL_time). Süre `>=` anında dolmuş sayılır (§7).
- **L_status** (§7.1): PENDING (L_pending) → LOST (L_lost) → SYMMETRIC (L_SYM_time dolmamış) → HEARD (L_HEARD_time dolmamış) → LOST.
- **HELLO** (§10–§11): hop limit 1, iletilmez; VALIDITY_TIME (H_HOLD_TIME) MUST; periyodik HELLO'da INTERVAL_TIME SHOULD; adresler LOCAL_IF · LINK_STATUS · OTHER_NEIGHB TLV'leriyle; her komşu bilgisi her REFRESH_INTERVAL'da en az bir kez (MUST); değişen bilgi bir sonraki HELLO'da (SHOULD).
- **İşleme** (§12): §12.3 Neighbor Set → §12.4 Lost Neighbor Set → §12.5 Link Set (LINK_STATUS HEARD/SYMMETRIC → L_SYM_time; LOST → L_SYM_time dolar, HEARD ise L_time = şimdi + L_HOLD_TIME; L_HEARD_time = max(şimdi + geçerlilik, L_SYM_time); L_time güncellemesi) → §12.6 2-Hop Set (yalnız gönderenle bağ SYMMETRIC ise; SYMMETRIC ilan edilen 2-atlama eklenir/tazelenir, LOST/HEARD silinir). Sıra MUST.
- **Değişiklikler** (§13): bağ SYMMETRIC olunca N_symmetric ve Lost Neighbor temizliği (§13.1); SYMMETRIC'ten düşünce 2-Hop tuple'ları silinir, komşunun simetrik bağı kalmadıysa N_symmetric false + Lost Neighbor (§13.2); L_HEARD_time dolunca komşu silinir (§13.3). Değişikliğe yanıt HELLO MAY; gönderilirse SHOULD koşulları §13.
- **Bağ kalitesi** (§14): tamamen MAY. Kullanılmayan dağıtımın değerleri §15.4 (HYST_ACCEPT 1 · HYST_REJECT 0 · INITIAL_QUALITY 1 · INITIAL_PENDING false).
- **Değerler** (§15): HELLO_INTERVAL 2 s · HELLO_MIN_INTERVAL 0,5 s · REFRESH_INTERVAL 2 s · H_HOLD_TIME 6 s · L_HOLD_TIME 6 s · N_HOLD_TIME 6 s · I_HOLD_TIME 6 s · HP_MAXJITTER 0,5 s · HT_MAXJITTER 0,5 s · C 1/1024 s.

## 3 · Okuma notları (RFC 7779 · DAT)

- L_in_metric bağın GELEN yönünün maliyeti: kayıp oranı (iki kuyruk: alınan · tahmini gönderilen, DAT_MEMORY_LENGTH 64 dilim × DAT_REFRESH_INTERVAL 1 s) ve gelen tek-yayın hızı. `L_in_metric = (2^24 / 8) · min(toplam/alınan, 8) / (hız / 1000)`; alınan < 1 → MAXIMUM_METRIC.
- Kayıp RFC 5444 **paket sıra numarasından** (arayüz başına, her pakette +1; DAT ile kullanılırken SHOULD) ve HELLO'nun INTERVAL_TIME'ından (SHOULD); paket gelmeyen her HELLO aralığı `lost_packet_intervals`a (§9.3 · §9.4 · §10.1 · §10.2). DAT_HELLO_TIMEOUT_FACTOR 1,2 · DAT_SEQNO_RESTART_DETECTION 256.
- **Gelen hız (L_DAT_rx_bitrate):** RFC'nin kapsamı dışında; *"static configuration via a configuration file"* açıkça izinli (§8). Gözlem penceresinde komşu başına alınan hız yok → **sabit yapılandırma** (beyan). Tek değer bütün bağlarda aynı olduğundan Dijkstra'nın sonucu değeri seçmeye duyarsızdır; yalnız 12 bitlik sıkıştırmanın yuvarlaması ve MAXIMUM_METRIC sınırı değere bağlı.
- RFC 7779 §3'ün uyarısı: çok-yayın, en yavaş tek-yayından yüksek alım olasılığıyla gitmemeli. 802.11b'de yayın temel hızda (1 Mbit/s) gider; kayıp tahmini tek-yayın için iyimserdir (beyan; simülatörün MAC'i değişmez).
- Kayıp histerezisi (Ek D) ve hız süzgeci (Ek C) bilgilendirici örnek; normatif değil.

## 4 · Okuma notları (RFC 7181 · OLSRv2)

- **Adres modeli (bizim dünyamız):** her yönlendiricinin tek arayüzü ve tek adresi var; kaynak adresi (originator) arayüz adresine eşit (§7 izin veriyor). Bağlı ağ yok (Local Attached Network Set boş). Sonuç: komşu metriği bağ metriğine eşit (tek bağ); Routable Address Topology Set Router Topology Set'le aynı düğümleri taşır, TC'de her komşu tek adresle ve `NBR_ADDR_TYPE = ROUTABLE_ORIG` ile ilan edilir (§13.3.2).
- **Bağ kümesine eklenenler** (§8.1): L_in_metric (dış süreç: DAT) · L_out_metric (komşunun HELLO'sundaki gelen bağ metriği) · L_mpr_selector (bayrak MPR seçicisi). Komşu kümesine (§9): N_orig_addr · N_in/out_metric (simetrik bağların en küçüğü) · N_will_flooding/routing · N_flooding_mpr · N_routing_mpr · N_mpr_selector · N_advertised; ANSN.
- **HELLO'ya eklenenler** (§15.1): MPR_WILLING (MUST) · HEARD/SYMMETRIC her bağa gelen bağ metriği · SYMMETRIC bağa giden bağ metriği · simetrik komşuya gelen ve giden komşu metriği · MPR TLV (FLOODING · ROUTING · FLOOD_ROUTE). MPR değişiminde ek HELLO MAY (§15.2).
- **HELLO işleme** (§15.3): NHDP'den sonra L_out_metric = komşunun bana ilan ettiği gelen bağ metriği; 2-Hop'a N2_in/out_metric; MPR seçicisi bayrakları (§15.3.2.3); N_mpr_selector true → N_advertised true.
- **Bağ durumu kuralları** (§17.2): L_out_metric bilinmiyorsa bağ SYMMETRIC olamaz; SYMMETRIC değilse L_mpr_selector false. (§17.3): N_mpr_selector → N_advertised; seçici olmayan simetrik komşuyu ilan etmek MAY, SHOULD gereksiz değişimden kaçın. ANSN ilan edilen küme ya da onun N_out_metric'i değişince artar (§17.4).
- **Taşma** (§14): kendi mesajı atılır; işleme — gönderen simetrik değilse işlemek İSTEĞE BAĞLI (§14.2 adım 1), Processed Set; iletme — gönderen simetrik değilse at, Received Set (arayüz başına), Forwarded Set, gönderen bayrak MPR seçicisiyse hop limit −1, hop count +1, ilet. İletmede titreşim MAY, kullanılırsa en çok F_MAXJITTER (SHOULD).
- **TC** (§16): originator, seq, hop limit TC_HOP_LIMIT, CONT_SEQ_NUM (COMPLETE) = ANSN, VALIDITY_TIME = T_HOLD_TIME; N_advertised komşular ROUTABLE_ORIG + giden komşu metriği; INTERVAL_TIME MAY. Periyodik TC_INTERVAL; ilanı boşalınca A_HOLD_TIME boyunca boş TC (MUST); değişime yanıt TC MAY (TC_MIN_INTERVAL'a uyar). Üretimde titreşim MAY (TP_MAXJITTER).
- **TC işleme** (§16.3): AR_seq_number > ANSN → at; topoloji demetleri (bilinmeyen metrik → sil); COMPLETE ise eski ANSN'li demetler silinir. AR süresi dolunca kaynağın bütün demetleri silinir (§17.5).
- **MPR** (§18): bayrak MPR'leri arayüz başına, giden bağ metriğiyle (A) ya da metriksiz (B) — seçim serbest, tutarlı olmalı; yönlendirme MPR'leri gelen komşu metriğiyle (zorunlu metrikli). Özellik: WILL_ALWAYS içinde; her 2-atlama komşu kapsanır ve en kısa uzaklık korunur (d(y,M) = d(y,N1)). Örnek algoritma Ek B; adım 4 (fazlayı atma) İSTEĞE BAĞLI. İstek değeri SHOULD dikkate alınır.
- **Rota kümesi** (§19 · Ek C): omurga X→Y (komşu, N_out_metric) ve W→U (TR_metric) üzerinde en küçük toplam metrik; eşit metrikte az atlamalı SHOULD. 2-atlama kenarları (Y→Z) İSTEĞE BAĞLI.
- **Sıra numarası** (§21): 16 bit sarmalı karşılaştırma.
- **Değerler** (§20 + RFC 6130 §15): TC_INTERVAL 5 s · TC_MIN_INTERVAL 1,25 s · T_HOLD_TIME 15 s · A_HOLD_TIME 15 s · RX/P/F_HOLD_TIME 30 s · O_HOLD_TIME 30 s · TP_MAXJITTER = HP_MAXJITTER 0,5 s · TT_MAXJITTER = HT_MAXJITTER 0,5 s · F_MAXJITTER = TT_MAXJITTER 0,5 s · TC_HOP_LIMIT 255 · WILL_FLOODING = WILL_ROUTING = WILL_DEFAULT 7 · MINIMUM_METRIC 1 · MAXIMUM_METRIC 16776960 · metrik 12 bit sıkıştırılmış (§6.2: (257+a)·2^b − 256).

## 5 · Tel biçimi (RFC 5444) — mesaj gerçek bayt dizisi olarak taşınır

Simülatörün biçim sözleşmesi (`MesajBicimi`) sabit ve tekrarlı alanlardan boyut hesaplar. RFC 5444'ün TLV'li, sıkıştırmalı biçimi sabit alan listesine sığmaz; bu yüzden protokol paketi **RFC 5444'e göre bayt bayt kodlar** ve tekrarlı 8 bitlik tek alanla taşır (`HELLO` · `TC` biçimleri). Ödenen bayt gerçek tel boyutudur; alıcı aynı baytları çözer. Kodlayıcı ve çözücü `protokoller/olsrv2_rfc5444.py`de, gidiş-dönüş testle bağlı.

- **Paket başlığı:** sürüm/bayraklar 1 + paket sıra numarası 2 (DAT için SHOULD, RFC 7779 §9.2) = 3 bayt; paket TLV'si yok. Her pakette tek mesaj (aynı anda gönderilen mesajların birleştirilmesi SHOULD, §13.2; bağımsız titreşimli zamanlayıcılarda iki mesaj aynı anda çıkmaz).
- **HELLO başlığı:** tür · bayrak/adres boyu · boy · kaynak adresi (olsrd2 gibi; hop alanları ve sıra numarası yok) = 8 bayt. Mesaj TLV'leri VALIDITY_TIME (H_HOLD_TIME) · INTERVAL_TIME (HELLO_INTERVAL; periyodik HELLO'da SHOULD) · MPR_WILLING.
- **TC başlığı:** kaynak · hop limit · hop count · sıra = 12 bayt (olsrd2 dördünü de koyar ve hop count'u ister). Mesaj TLV'leri VALIDITY_TIME (T_HOLD_TIME) · INTERVAL_TIME (TC_INTERVAL; MAY, olsrd2 koyar) · CONT_SEQ_NUM (COMPLETE).
- **Adres bloğu:** adresler sıralı; ortak baş (head) bayt kazandırıyorsa kullanılır; kuyruk yok; önek uzunluğu yok (tam adres). Adres modeli: düğüm `k` → IPv4 `10.0.0.0 + k + 1` (seçim; boyutu yalnız sıkıştırma üzerinden etkiler).
- **Adres TLV'leri:** her TLV türü (LINK_METRIC için gelen ve giden ayrı kanal) aynı TLV'yi taşıyan ardışık adres koşularına bölünür; koşuda değer tekse tek değerli, değilse çok değerli TLV; tek adres tek indeks, bütün blok indekssiz. Aynı metrik değerli tür/yön bitleri tek değerde birleşir (§13.3.2, "any combination").
- **Sayılar:** mesaj türü HELLO 0 · TC 1; mesaj TLV'si INTERVAL_TIME 0 · VALIDITY_TIME 1 · MPR_WILLING 7 · CONT_SEQ_NUM 8 (COMPLETE 0); adres TLV'si LOCAL_IF 2 · LINK_STATUS 3 · OTHER_NEIGHB 4 · LINK_METRIC 7 (tür uzantısı 0) · MPR 8 · NBR_ADDR_TYPE 9; değerler THIS_IF 0 · LOST 0 · SYMMETRIC 1 · HEARD 2 · FLOODING 1 · ROUTING 2 · ROUTABLE_ORIG 3. Zaman kodu RFC 5497 §5 (C = 1/1024 s), metrik kodu RFC 7181 §6.2.

## 6 · Kararlar (RFC'nin seçeneğe bıraktığı yerler)

| konu | RFC | karar | dayanak |
|---|---|---|---|
| bağ kalitesi (NHDP §14) | MAY | yok; §15.4 değerleri | metrik DAT'ta; olsrd2 de varsayılan histerezissiz |
| simetrik olmayan göndericinin TC'sini işlemek (§14.2 adım 1) | İSTEĞE BAĞLI | işlenir | olsrd2 işler |
| ilan edilen komşular (§17.3 madde 5) | MAY | yalnız yönlendirme MPR seçicileri | olsrd2; SHOULD "gereksiz değişimden kaçın" |
| bayrak MPR'lerinde metrik (§18.4 A/B) | serbest | B: atlama sayısı (K-236; ilk hâlde A) | olsrd2'nin bayrak alanı sabit "Hopcount metric"le kurulur |
| MPR algoritması | Ek B örnek | Ek B harfiyen: W → R → D → küçük adres; adım 4 (fazlayı atma) yok | §18.1 istek SHOULD dikkate alınır (olsrd2 istek adımını atlıyor) |
| RFC 7187 yönlendirme MPR iyileştirmesi | MAY | yok | olsrd2'de yok |
| 2-atlama rota kenarları (§19.1 · Ek C.7) | İSTEĞE BAĞLI | var, yalnız başka yol yoksa (RFC: tercih edilmez) | olsrd2 kullanır |
| değişime yanıt HELLO/TC (NHDP §13 · §15.2 · §16.2) | MAY | yok, yalnız periyodik | olsrd2 periyodik |
| HELLO/TC üretim titreşimi, iletme titreşimi | SHOULD (RFC 5148) | aralık U(0, 0,5 s) kısalır · iletme U(0, 0,5 s) gecikir | RFC 5148 §5.1 · §5.3 |
| TC'de gelen komşu metriği | — | yok (yalnız giden, MUST) | olsrd2 ekliyor, RFC istemiyor |
| bütünlük koruması (RFC 7183 ICV + zaman damgası) | gerçeklemede MUST, kurulumda SHOULD | kullanılmaz | tehdit modelinde mesaj sahteciliği yok (içeriden saldırılar kapsam dışı, K-230); öteki rakipler de imzasız; olsrd2'de varsayılan kapalı (ayrı eklenti) |
| DAT gelen hız (RFC 7779 §8) | dış süreç, sabit yapılandırma izinli | sabit 1 Mbit/s (802.11b temel hızı) | gözlemde komşu başına alınan hız yok; tek değer Dijkstra'yı değiştirmez; olsrd2'nin `ffdat_airtime=false` kipi (ETX'e iner) |
| bağ katmanı bildirimi | tanımsız | kullanılmaz | OLSR v1'de de kapalı (K-196) |
| proaktif protokolde veri tamponu | tanımsız | yok, rota yoksa paket düşer | OLSR v1 ile aynı |

## 7 · Sonuç

Gerçekleme ve kural kural sadakat denetimi K-235'te (`arsiv/teshis/olsrv2_sadakat_2026-10-11/denetim.md`). Kod `protokoller/olsrv2.py` · `olsrv2_rfc5444.py` · `olsrv2_bicim.py`; testler `tests2/test_olsrv2.py`. Uygulamada çıkan ek kararlar: yönlendirme MPR'lerinin d2'si N2_in_metric (§18.5'in metni ile izin koşulu ve §4.6 çelişiyor; olsrd2 gelen) · 2-atlama rotasının metriği N2_out_metric (Ek C.7'nin metni ile §19.1 çelişiyor) · omurga düğümüne 2-atlama kenarı kullanılmaz (§19.1) · iletme titreşiminin önüne simülatörün alt sınırı 20 µs.
