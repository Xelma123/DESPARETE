# AODV sadakat denetimi — RFC 3561 ve ns-3'e karşı, kural kural (K-207 şartı)

> 30 Eylül 2026 · donma şartı (K-207): AODV ancak kaynağına kural kural sadık olduğu gösterilirse donar. Kaynaklar yerel: `protokol_kaynaklari/rfc3561_aodv.txt`, `protokol_kaynaklari/uygulama_kaynaklari/ns-3/aodv-routing-protocol.cc`.
> K-205'te "`AODV-g` RFC'ye sadık" denmişti; bu denetim bunun fazla iddialı olduğunu gösterdi — aşağıda 10 sapma daha.

## İlke

**RFC birincil.** ns-3 yalnız RFC'nin sustuğu ya da kendi içinde çeliştiği yerde hakem. ns-3'ün RFC'de olmayan eklemeleri alınmaz. Gerekçeli, beyanlı sapmalar (biçim dosyasında) yerinde kalır.

## Bulunan sapmalar → `AODV-h`

| # | RFC | RFC ne diyor | ns-3 | `AODV-g` | karar |
|---|---|---|---|---|---|
| H1 | §6.5 ilk cümle | RREQ alınınca önceki atlamaya rota *"without a valid sequence number"* kurulur ya da güncellenir | aynı (`toNeighbor.SetValidSeqNo(false)`) | geçerli tek atlamalı rotanın sırası korunuyordu | RFC |
| H2 | §6.5 (1)–(5) | ters rota oluşturulur ya da güncellenir; sıra *"copied if greater"*; ömür `max(Existing, Minimal)` | koşulsuz günceller, sıra büyüğü, ömür büyüğü | koşullu günceller; ömür tabanı `ACTIVE_ROUTE_TIMEOUT` (RFC'de yok), mevcut ömrü kısaltabilir | RFC |
| H3 | §6.5 son paragraf | iletilen RREQ'in hedef sırası *"set to the maximum of"* gelen değer ile düğümün bildiği | aynı (bilinen geçerliyse; U bayrağı kalkar) | değiştirmeden iletiyordu | RFC |
| H4 | §6.6.2 | ara düğüm, geçerli sırası RREQ'inkinden büyük ya da eşitse cevap verir; ters rotanın öncül listesine hedefe doğru sonraki atlama eklenir | U bayraklı RREQ'e de cevap verir; iki öncül | U bayraklı RREQ'e cevap vermiyordu; ters rota öncülü yoktu | RFC (U: ns-3 hakem) |
| H5 | §6.7 | RREP yalnız ileri rota *"created or updated"* ise iletilir; iletilirken ters rota ömrü `max(mevcut, şimdi + ACTIVE_ROUTE_TIMEOUT)`, hedefe doğru sonraki atlamanın öncülüne kaynağa doğru sonraki atlama | koşulsuz iletir (RFC'den sapma) | koşulsuz iletiyordu; reddedilen RREP rotanın ömrünü uzatıyordu (RFC'de yok); ters rota ömrü ve komşu öncülü yoktu | RFC |
| H6 | §6.9 | HELLO alınınca komşuya etkin rota, ömür ≥ `ALLOWED_HELLO_LOSS × HELLO_INTERVAL`, sıra *"MUST … latest Destination Sequence Number from the Hello"* | aynı (`ProcessHello`) | HELLO sırayı rotaya yazmıyordu | RFC |
| H7 | §6.4 | geçersiz girdi varsa ilk RREQ TTL'i *"Hop Count plus TTL_INCREMENT"* | aynı | hep `TTL_START` | RFC (SHOULD) |
| H8 | §6.11 (ii) | ara düğüm, etkin rotası olmayan hedefe veri alırsa RERR (öncül varsa) ve düşürür; geçersiz rotaya veri gelince silinme süresi `şimdi + DELETE_PERIOD` | düşürür, RERR | girdi yok ya da süresi dolmuşsa ara düğüm paketi tamponlayıp KENDİSİ keşif başlatıyordu; silinme süresi uzamıyordu | RFC |
| H9 | §6.11 madde 1 | sıra yalnız RERR durumlarında (i · ii) artar, (iii)'te kopyalanır | ömür dolunca sıraya dokunmaz | ömür dolunca da artırıyordu (yerel sıra şişmesi) | RFC |
| H10 | §10 `RREQ_RATELIMIT` | saniyede en çok 10 RREQ (SHOULD NOT originate more) | aşan RREQ ERTELENİR | ilk keşifte deneme bırakılıyordu; **yeniden denemede zamanlayıcı kurulmadan dönülüyor, keşif kaydı silinmediği için o hedefe bir daha keşif başlamıyordu** (tampon süresine kadar takılma) | ns-3 (RFC susuyor) |

## Uyumlu bulunanlar (değişmedi)

§6.1 kaynak sırası RREQ'ten önce artar · §6.2 rota kullanımında kaynak, hedef, sonraki atlama ömrü · §6.3 tampon ve RREQ_RETRIES · §6.4 halka ilerleyişi ve bekleme süreleri · §6.5 tekrar bastırma (`PATH_DISCOVERY_TIME`), TTL > 1 ise iletim · §6.6.1 hedef cevabı (sıra +1 kuralı) · §6.7 dört güncelleme durumu (K-205) · §6.8 kara liste (K-194) · §6.9 HELLO gönderme koşulu (son aralıkta yayın yoksa) · §6.10 komşuluk (her paket kanıt) · §6.11 (i) bağ kopması, öncül süzmesi, (iii) RERR işleme ve kopyalama (K-205) · §10 sabitleri.

## RFC'nin kendi çelişkisi ve belirsizlikleri (hakem ns-3)

- §6.1 *"MUST update its own sequence number to the maximum"* ile §6.6.1 *"MUST increment … if equal to that incremented value. Otherwise … does not change"* RREQ sırası kendi sırasının iki fazlasından büyükse çelişir. ns-3 §6.6.1'i uygular; biz de (değişmedi).
- §6.9 *"SHOULD only use hello messages if it is part of an active route"*: RFC'nin kendi tanımında "active route" = geçerli girdisi olan rota; hemen her düğümde geçerli bir girdi olduğundan ns-3 gibi HELLO her zaman (son aralıkta yayın yoksa) gönderilir. Değişmedi, beyan.

## ns-3'ün RFC'de olmayan eklemeleri — ALINMADI

- Ara düğümün hedefe rotası RREQ'i gönderenden geçiyorsa RREQ'i düşürmesi (döngü koruması).
- Kaynağın keşif sürerken her RREP'i sıraya bakmadan kabul etmesi.
- ~~Etkin rotası olmayan ara düğümün öncül listesine bakmadan RERR göndermesi.~~ → **K-210'da ALINDI** (aşağıda): RFC'nin süzme cümlesi küçük harf "should" (normatif değil), ns-2 ve ns-3 ikisi de süzmüyor; süzme ters yoldan öğrenilmiş rotalarla kara delik doğuruyordu.

## Beyanlı sapmalar (biçim dosyasında, gerekçeli — yerinde)

Yerel onarım §6.12 (MAY) · RREP-ACK mesajı (kara liste bağ katmanı onayıyla) · karşılıksız RREP §6.6.3 · önek · önceki atlama ömrü (gözlem yüzeyi) · RERR her zaman yayın · TTL yükte (+1 bayt) · sıra karşılaştırması sarmasız (değerler binlerde).

## AOMDV'ye etkisi

AOMDV, AODV'nin `sonraki_atlama`, keşif başlatma ve yeniden deneme (`_kesif_baslat`, `uyandi`) ile `_bakim` ve `kontrol_alindi` metotlarını devralır. H7, H8, H9 ve H10 AOMDV'nin AODV'den gelen kısmını da değiştirir; aynı RFC onun da tabanıdır. AOMDV'nin kendi kuralları (Şekil 3, S10) değişmez. → U1 AODV ve AOMDV için birlikte yeniden koşulur.

## AOMDV — K-210 (1 Ekim sabahı, U1'den sonra)

**U1 `AOMDV-c` (1 Ekim 05:17):**
- yere toplamada iki yeni düşük hücre: statik 1002 0,914 → 0,888 · bağımsız 1000 0,606 → 0,588
- eşler arası statik 1001 **0,991 → 0,870**

**Teşhis** (`aomdv_teshis.py`, eşler arası statik-yok 1001, tam pencere):

| kod | PDR | "hedef yok" düşüşü |
|---|---|---|
| AOMDV-b | 0,982 | 0 |
| AOMDV-c | 0,862 | 1 697 (ara düğümde girdi yok) |
| AOMDV-c, yalnız veri kararı eski (nedensellik) | 0,950 | — |
| AOMDV-c + öncül düzeltmesi | **0,980** | **0** |

**Kusur:** AOMDV'nin kendi `_rrep_isle`'sinde RFC §6.7'nin son paragrafı yoktu (ters yolun ömrü ve hedefe doğru komşunun öncülü). Ara düğüm cevabında §6.6.2'nin ters rota öncülü yoktu. RERR yukarı ulaşamıyor, kara delik oluşuyordu. Eski kodun RFC dışı "ara düğüm kendi keşfini yapar" davranışı (H8) bunu örtüyordu.

Bir iddia düzeltmesi: daha önce "makalede her yolun kendi zaman aşımı var" denmişti. Makalenin Şekil 2'sinde zaman aşımı **girdi başına tek**; yol başına zaman aşımı ns-2 gerçeklemesinde. Kodumuz bu noktada makaleye sadık (`marina_das_metin.txt`).

**`AOMDV-d` — RFC tabanı, makalenin sustuğu yerlerde AODV-h'nin kuralı:**
- öncül ve ters yol ömrü (§6.7, §6.6.2)
- komşu rotası sırasız (§6.2)
- RREQ'te önceki atlama sırasız (§6.5)
- iletilen RREQ'in sırası bilinenin büyüğüne (§6.5)
- ara düğüm U bayraklı RREQ'e cevap (§6.6.2)
- HELLO sırası, Şekil 3'ün kuralından geçen atlama-0 ilanı olarak (§6.9)
- kaynak keşfi yalnız rota kurulunca kapatır
- RERR'de sıra kopyalama (§6.11 iii)

Makaleye özgü kurallar değişmedi: Şekil 3 güncelleme kuralı · §3.2 çok RREP, k cevap, ilk atlama ile ayrık yollar · S10.

## K-210 · durum (ii)'nin RERR'i öncül süzmesiz (AODV-i · AOMDV-e)

AOMDV-d (A1–A7 + öncül) eşler arası statik 1001'de yine kara delik üretti: 1 225 paket, hepsi tek bir (33 → 5, hedef 9) çiftinden (`aomdv_kara_delik.py`). 33'ün 9'a rotası 9'un RREQ'inden öğrenilmiş bir ters yol, 33 veri gönderdikçe tazeleniyor; 5'in rotası düşmüş, 33 5'in öncülü değil, (ii)'nin RERR'i öncüle göre süzüldüğü için 33 hiç haber almıyor.

Varyantlar (aynı hücre):

| varyant | PDR | "hedef yok" |
|---|---|---|
| tam | 0,897 | 1 225 |
| A4'süz | 0,969 | 194 |
| A2'siz | 0,843 | 1 904 |
| yalnız öncül | 0,980 | 0 |

→ Kök mekanizma yapısal (RFC'nin normatif olmayan süzme cümlesi). Düzeltme: (ii)'de RERR öncüle bakmadan gider (ns-2/ns-3); (i)'nin süzmesi (K-143) kalır.
