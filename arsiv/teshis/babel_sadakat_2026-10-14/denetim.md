# Babel sadakat denetimi — RFC 8966 ve babeld 1.14'e karşı, kural kural (K-242 · K-244)

> 14 Ekim 2026 · kaynaklar: RFC 8966 (`protokol_kaynaklari/rfc8966_babel.txt`; §1–§4 ve Ek A–B tamamı okundu), babeld 1.14 (`protokol_kaynaklari/uygulama_kaynaklari/babeld/`; okunan dosyalar `protokol_kaynaklari/README.md`de) · gerçekleme `protokoller/babel.py`, `protokoller/babel_bicim.py` (beyan tablosu) · testler `tests2/test_babel.py`

## İlke (K-244)

- RFC'nin MUST ve SHOULD'u uygulanır. RFC açık bir değer ya da yordam veriyorsa o alınır.
- RFC'nin seçeneğe ya da MAY'e bıraktığı yerde babeld'in varsayılanı alınır; babeld yapmıyorsa alınmaz.
- babeld'in RFC'nin MUST ya da SHOULD'una uymadığı yerde RFC alınır. Bu durumda babeld'in amacına RFC'yle uyumlu en yakın dal seçilir.
- RFC'de olmayan babeld eklemeleri (RTT, kaynağa özgü yönlendirme, çeşitlilik, kimlik doğrulama) alınmaz.

## Kural kural

Durum: **RFC** = RFC'nin metni · **babeld** = RFC'nin bıraktığı seçenekte babeld'in varsayılanı · **beyanlı** = gerekçeli sapma · **RFC > babeld** = babeld RFC'den ayrılıyor, RFC alındı.

| # | RFC | kural | gerçekleme | durum | test |
|---|---|---|---|---|---|
| 1 | §4.2 | başlık: Magic 42 · Version 2 · gövde uzunluğu; geçersiz paket yok sayılır | `paket_kodla` · `paket_coz` (`BicimHatasi` → `gecersiz_paket`) | RFC | `TLV_BOYUTLARI` |
| 2 | §4.3 | tanınmayan TLV atlanır | `paket_coz` | RFC | `GIDIS_DONUS` |
| 3 | §4.6 | TLV boyları: Hello 8 · IHU (AE 1) 12 · Update 16 / 13 · Route Request 8, joker 4 · Seqno Request 20 | bayt bayt | RFC | `TLV_BOYUTLARI` |
| 4 | §4.5 · §4.6.9 | önek sıkıştırma (P, Omitted), R bayrağıyla router-id | aynı /24'te Omitted 3 | RFC | `GIDIS_DONUS` |
| 5 | §4.6.9 | geri çekmede router-id anlamsız | çözücü 0 verir; alıcı kaydın kaynağını kullanır (babeld `update_route`) | RFC · babeld | `GIDIS_DONUS` |
| 6 | §4 | UDP 6696, IPv6 RECOMMENDED | IPv4/UDP (simülatörün tek ağ katmanı), MTU içinde bölme | beyanlı | `PAKET_MTU` |
| 7 | §3.1 | acil TLV acil zaman aşımı (0,2 s) içinde (MUST) | U(0, 0,2 s) | RFC | — |
| 8 | §3.1 | öteki TLV'ler Hello aralığının yarısı içinde (SHOULD) | U(0, 2 s); periyodik Hello ve döküm RFC 5148 dağılımıyla, ilan edilen aralığı aşmaz | RFC (babeld ±%25, aralığı aşabilir; acil olmayan güncellemeyi 3–5 s'de boşaltır) | — |
| 8a | §3.1 | TLV'ler tamponlanır, rastgele gecikmeyle gönderilir (SHOULD); birleştirmeye izin verir | hedef başına tampon (çoklu-yayın ya da komşu); aynı önekin duyuruları tek Update'e iner, gönderim anındaki hâliyle kurulur; Hello, döküm ve açılış bekleyen çoklu-yayın tamponunu taşır | RFC · babeld (`buffer_update` · `flushupdates` · `flushbuf`) | `TAMPON` |
| 9 | §3.1 | açık zaman aşımlı TLV (Update, IHU) son tarihten önce (MUST) | döküm aralığı ≤ 16 s, tam IHU üç Hello'da bir (≤ 12 s) | RFC | — |
| 10 | §3.2.1 | sıra aritmetiği mod 2^16 | `sira_artir` · `sira_kucuk` | RFC | `SIRA_ARITMETIGI` |
| 11 | §3.3 | onay isteğine yanıt verilebilmeli (MUST) | tek-yayın Ack, acil | RFC | — |
| 12 | §3.4.1 · Ek A.1 | Hello geçmişi: 16 bit, beklenen sıra, geri alma/ileri sarma, >16 farkta komşu yenilenir | `_hello_al` | RFC | `HELLO_GECMISI` |
| 13 | Ek A.1 | zaman aşımı 1,5 × ilan edilen aralık, sonrakiler aralık kadar | `_zamanlari_isle` | RFC (babeld 1,7 ×) | `HELLO_GECMISI` |
| 14 | §3.4 | kullanılmayan komşu atılır (SHOULD) | iki geçmiş de boşsa | RFC | `HELLO_GECMISI` |
| 15 | §3.4.2 | IHU'nun rxcost'u txcost olur; tutma 3,5 × ilan edilen aralık | `_ihu_al` | RFC (babeld 10 ×) | — |
| 16 | Ek B | IHU kayıplı bağda her Hello'yla, kayıpsızda üç Hello'da bir | babeld `send_hello` · `send_marginal_ihu`: sırası 3'e bölünen Hello'da tam, öteki Hello'larda son 4 Hello'dan biri kaçmış ya da txcost ≥ 384 komşuya | babeld | `IHU_SIKLIGI` |
| 17 | §3.4.3 · Ek A.2.2 | rxcost Hello geçmişinden (ETX), Hello yoksa ∞ (MUST) | babeld `neighbour_rxcost`: ağırlıklı geçmiş, son 12 Hello yoksa ∞, 40 s / 180 s gecikme kuralları | babeld | `ETX` |
| 18 | Ek A.2.2 | cost = max(txcost, 256) · rxcost / 256; biri ∞ ise ∞ | babeld'in yuvarlaması (+128 ≫ 8) | RFC · babeld | `ETX` |
| 19 | §3.5.1 | uygulanabilirlik: daha yeni sıra ya da aynı sıra ve FD'den küçük metrik; geri çekme her zaman | `_uygulanabilir` | RFC | `UYGULANABILIRLIK` |
| 20 | §3.5.2 | toplamsal metrik, ∞'a kırpılır | `metrik` | RFC | `ETX` |
| 21 | §3.5.3 | kayıt yokken geri çekme yok sayılır | `_guncelleme_al` | RFC | — |
| 22 | §3.5.3 | kayıt yokken uygulanamaz güncelleme MAY yok sayılır | yok sayılmaz, kayıt açılır | babeld | `ACLIK` |
| 23 | §3.5.3 | seçili rotanın aynı router-id'li uygulanamaz güncellemesi MAY yok sayılır; yok sayılmazsa kayıt hemen seçimden çıkar (MUST) | yok sayılır, rota seçili kalır | RFC > babeld: babeld kaydı günceller ama seçimden çıkarmaz (`update_route`), yani RFC'nin iki dalının arası; amacına uyumlu dal yok saymadır | `UYGULANAMAZ_GUNCELLEME` |
| 24 | §3.5.3 | öteki güncellemede kayıt güncellenir, sonlu metrikte süre tazelenir, uygulanamazsa seçimden çıkar (MUST) | farklı router-id'li uygulanamaz güncellemede seçimden çıkar | RFC | `UYGULANAMAZ_GUNCELLEME` |
| 25 | §3.5.3 · Ek B | süre 3,5 × ilan edilen aralık; dolunca metrik ∞, ikinci dolumda silinir | `_zamanlari_isle` | RFC (babeld 6 ×, 7/8'i geçen rotayı ~30 s'lik taramada siler) | — |
| 26 | §3.5.4 | geri çekilen önek için ∞ kayıt tutulur | kayıt süresi dolana dek; daha kısa önek yok | RFC | — |
| 27 | §3.6 | ∞ metrikli ve uygulanamaz rota seçilmez (MUST) | `_sec` | RFC | `SECIM` |
| 28 | §3.6 | seçim sırayı hesaba katmaz (MUST NOT) | `_sec` metrikle | RFC | `SECIM` |
| 29 | §3.6 · Ek A.3 | histerezis: seçili R'den R''ye ancak m(R') < m(R) ve ms(R') < ms(R) ise | `_sec` | RFC | `SECIM` |
| 30 | Ek A.3 | ms'nin zaman sabiti "Hello × küçük bir sayı, örneğin 3" | yarı ömür 4 s; yeni rotada ms = max(m, ∞/2); ∞'da ms = ∞; fark < 4'te ms = m | babeld (`route_smoothed_metric`; her saniyeki rastgele yuvarlama alınmadı) | `SECIM` |
| 31 | §3.7.1 | her seçili rota her güncelleme aralığında en az bir kez (MUST) | periyodik tam döküm, aralık ≤ 16 s | RFC | uçtan uca |
| 32 | §3.7 | yakında geri çekilmiş önekler için geri çekme gönderilebilir (may) | kurulu ∞ rotalar dökümde geri çekme olarak | babeld | — |
| 33 | §3.7.2 | router-id değişince acil güncelleme (MUST) ve tüm komşulara ulaştırma girişimi (SHOULD) | acil, 2 · 4 · 8 s sonra yinelenir (kopya ≤ 5, MUST) | RFC · babeld | `TETIK_KURALLARI` |
| 34 | §3.7.2 | geri çekmede tetik (SHOULD) ve ulaştırma girişimi (SHOULD) | acil, yinelenir | RFC · babeld | `ACLIK` |
| 35 | §3.7.2 | belirgin metrik değişiminde tetik (MAY); küçük dalgalanma ve yalnız sıra için tetik yok (SHOULD NOT), istek karşılama hariç | babeld `send_triggered_update`: kötüleşme (eski < 1536, fark ≥ 512) acil; isteği karşılayan acil; ∞'dan dönüş acil değil; < 1024 iyileşme ve < 384 fark yok | babeld | `TETIK_KURALLARI` |
| 36 | §3.7.2 | ilk kez seçilen önek | acil, tek (`consider_route`) | babeld | `SURE_DOLUMUNDA_KAYIP` |
| 37 | §3.7.3 | sonlu güncellemeden önce FD güncellenir; geri çekmede güncellenmez; GC 3 dk | `_ilan` · `_fd_guncelle` | RFC | `UYGULANABILIRLIK` |
| 38 | §3.7.4 | 802.11 ad hoc'ta bölünmüş ufuk yok (SHOULD NOT) | yok | RFC | — |
| 39 | §3.8.1.1 | rota isteği: seçili rota varsa güncelleme, yoksa geri çekme (MUST) | çoklu-yayın, acil değil | RFC · babeld | `ROTA_ISTEGI` |
| 40 | §3.8.1.1 | joker istekte tam döküm (SHOULD), hız sınırlı (SHOULD) | son tam dökümden en az bir Hello aralığı geçtiyse; o komşuya IHU | RFC · babeld | `JOKER` |
| 41 | §3.8.1.2 | seçili sonlu rota istekle karşılanıyorsa güncelleme (MUST) | acil çoklu-yayın | RFC · babeld | `SIRA_ISTEGI` |
| 42 | §3.8.1.2 | kendi router-id'sinde sıra en çok 1 artar (MUST NOT > 1) | `_sira_istegi_al` | RFC | `SIRA_ISTEGI` |
| 43 | §3.8.1.2 | hop ≥ 2 ve önek duyuruluyorsa iletim: uygulanabilir rotaya MUST, yoksa uygulanamaza SHOULD; istekçiye değil; tek komşuya tek-yayın (MUST); acil (SHOULD) | seçili rotanın komşusu, değilse en küçük düzgünleştirilmiş metrik (babeld `handle_request`) | RFC · babeld | `SIRA_ISTEGI` |
| 44 | §3.8.1.2 | yakında iletilen isteklerin listesi, aynı önek, router-id ve küçük olmayan sırada iletilmez (SHOULD) | liste 65 s ya da karşılanana dek | RFC > babeld: babeld'in `request_redundant` karşılaştırması ters yönde (saklı sıra gelenden büyükse iletir); süre babeld `REQUEST_TIMEOUT` | `SIRA_ISTEGI` |
| 45 | §3.8.1.2 | iletilen isteğin yanıtı acil (SHOULD) | isteği karşılayan rota seçiliyken acil çoklu-yayın güncelleme (babeld `unsatisfied_request`) | RFC · babeld | `ILETILEN_ISTEGIN_YANITI` |
| 46 | §3.8.2.1 | uygulanamaz rota varken açlıkta sıra isteği (MUST), hepsine (SHOULD); istenen sıra FD + 1; hop 64 | çoklu-yayın | RFC | `ACLIK` |
| 47 | §3.8.2.1 | uygulanamaz rota yokken sıra isteği (MAY) | seçili rota süre dolumuyla ya da farklı router-id'li uygulanamaz güncellemeyle kaybedildiyse ve eski metrik ≤ ∞/2 ise | babeld `route_lost` | `SURE_DOLUMUNDA_KAYIP` |
| 48 | §3.8.2.1 · Ek B | rota uygulanabilir olmazsa yineleme (SHOULD): 2 s, her yinelemede × 2, en çok 3 | +2 · +6 · +14 s | RFC (babeld +2 · +4 · +8 s) | `ACLIK` |
| 49 | §3.8.2.2 | seçili rotanın uygulanamaz güncellemesinde ilan edene tek-yayın sıra isteği (SHOULD) | bekleyen eşdeğer istek yoksa, her seferinde | RFC > babeld (babeld yalnız rota eskiyse) | `UYGULANAMAZ_GUNCELLEME` |
| 49a | §3.2.7 | bekleyen istekler tablosu: yerelde üretilen ve iletilen istekler, yanıt gelene dek; zamanlayıcı yinelemeyi ve ömrü yönetir | her üretilen istek tabloda; aynı önek ve router-id için daha küçük olmayan sıralı istek beklerken yenisi üretilmez; §3.8.2.2 isteği yinelenmez, 2 s'de düşer | RFC (babeld §3.8.2.2 isteğini tabloya yazmaz) | `BEKLEYEN_ISTEKLER_TABLOSU` |
| 50 | §3.8.2.2 | seçili olmayan ama tercih edilir rotanın uygulanamaz güncellemesinde istek (SHOULD) | seçili rota yoksa ya da seçilinin metriği yeni metrik + 512'den küçük değilse | RFC · babeld eşiği | `ACLIK` |
| 51 | §3.8.2 | her an rota ya da sıra isteği gönderilebilir (MAY) | metrik ≥ 288 kötüleşip güncelleme gönderilince çoklu-yayın rota isteği | babeld | `TETIK_KURALLARI` |
| 52 | §3.8.2.3 | süre dolmadan seçili rotanın ilan edenine tek-yayın rota isteği (SHOULD) | tutma süresinin 7/8'inde | RFC · babeld eşiği | `ROTA_ISTEGI` |
| 53 | Ek B | parametreler: Hello 4 s · IHU 3 × Hello · güncelleme 4 × Hello · IHU tutma 3,5 × · rota süresi 3,5 × · istek 2 s × 2, 3 kez · acil 0,2 s · kaynak GC 3 dk | `babel_bicim.py` | RFC | — |

## babeld'den gelen, ayrıca not edilenler

- **Açılış.** babeld açılışta Hello, joker geri çekme, kendi öneki ve joker istek gönderir. Joker geri çekme yeniden başlatmada komşulardaki eski rotaları siler; koşularda yeniden başlatma olmadığı için gönderilmez.
- **7/8 isteği.** babeld'in `expire_routes`'u süresinin 7/8'ini geçen rotayı istek dalından önce siler; bu yüzden babeld'de "süre dolmadan rota isteği" dalı pratikte çalışmaz. Burada RFC'nin SHOULD'u uygulanır, eşik babeld'in `route_old` tanımından.
- **Yineleme zamanlaması.** babeld'in `do_resend`i bekleyişi her seferinde iki katına çıkarır ama ilk gönderim anından sayar: +2 · +4 · +8 s. Tetik yinelemelerinde babeld'in zamanlaması alındı (RFC sayıyı "say, 3" diye bırakıyor). İstek yinelemelerinde RFC Ek B'nin açık tanımı alındı: her yinelemede bekleme iki katı, yani +2 · +6 · +14 s.
- **∞ rota.** babeld ∞ metrikli kurulu rotayı çekirdeğe "unreachable" olarak koyar. Paket düşer; burada da rota yoksa paket düşer.

## Seçilmeyen babeld özellikleri

- RTT bileşeni (RFC 9616): varsayılan kapalı.
- Tek-yayın Hello: Ek B sonsuz.
- Kaynağa özgü yönlendirme.
- Kimlik doğrulama (HMAC).
- Çeşitlilik: 1.13'te kaldırıldı.
- Kablolu arayüz için 2-out-of-3.

## Duman koşuları ve bulunan iki eksik (14–15 Ekim)

12 düğümlük statik uçtan uca koşuda her düğüm 11 öneke rota seçiyor; korunum ve mutabakat tamam.

Referans dünyanın iki regresyon vakası (tek tohum, kısa pencere; öteki protokoller k243 satırları):

| vaka | kod | PDR (pencere) | kontrol çerçevesi | NRL bayt (pencere) | süre |
|---|---|---|---|---|---|
| `u-birincil-babel` | ilk taslak | 0,401 (0,408) | 97 521 | 0,92 | 2 020 s |
| | düzeltilmiş | 0,584 (0,626) | 11 134 | 0,10 | 357 s |
| | OLSRv2 · AODV · DESPARETE | (0,477) · (0,446) · (0,629) | 8 229 · 32 741 · — | 0,07 · 0,41 · 0,45 | — |
| `u-bagimsiz-surekli-babel-dugum_kaybi` | ilk taslak | 0,0625 (0,0) | 9 846 | 0,29 | 239 s |
| | düzeltilmiş | 0,0879 (0,0) | 3 824 | 0,17 | 124 s |
| | OLSRv2 | 0,0078 (0,0) | 1 183 | 1,38 | — |

Birincil hücrede kontrol çerçevesi AODV'nin üç, OLSRv2'nin on iki katıydı (NRL bayt 0,92). Sayaçlar iki eksiği gösterdi; ikisi de Babel'i olduğundan pahalı gösteriyordu:

1. **Tampon yoktu (§3.1).** Her kanca kendi paketini çıkarıyordu; aynı önek için art arda gelen rota isteklerinin her biri ayrı bir yanıt paketi doğuruyordu (27 575 yanıt). babeld arayüz ve komşu tamponlarında biriktirip tek pakette gönderir. → satır 8a.
2. **§3.8.2.2 istekleri tabloya yazılmıyordu (§3.2.7).** Seçili rota uygulanamaz güncellemeyle yok sayılınca komşunun aynı güncellemesi her geldiğinde yeni bir istek üretiliyordu (23 586 sıra isteği). RFC'nin tablosu yerelde üretilen her isteği tutar. → satır 49a.

İki düzeltmeden sonra birincil hücrede kontrol çerçevesi 97 521'den 11 134'e indi ve PDR (pencere) 0,408'den 0,626'ya çıktı: ilk taslağın kendi kontrol seli kanalı tıkıyordu. Tek tohum ve kısa pencere: sayılar protokol kıyası değil, kusurun büyüklüğüdür. Kayıtlı ölçüm `arsiv/teshis/rakipler_k244_2026-10-14/` kuyruğunun regresyonunda.
