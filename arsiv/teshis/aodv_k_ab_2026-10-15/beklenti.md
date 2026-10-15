# AODV-k'nin U1 düşüşü — hangi değişiklik? Beklenti (ölçmeden önce)

> 15 Ekim 2026 · tetik: K-244 kuyruğunun U1'i (`arsiv/teshis/rakipler_k244_2026-10-14/sonuc.md`). AODV-k yere toplamada AODV-j'nin kayıtlı oranlarının 0,04–0,08 altında: statik 1000 0,852 (0,894) · 1002 0,812 (0,863) · bağımsız 1000 0,475 (0,556). Betik `ab.py`, donmuş kopyadan (`KOK=arsiv/teshis/rakipler_k244_2026-10-14/kopya`; AODV-k kodu commit `1163f81`'le aynı).

## Düzen

7 varyant × 3 hücre (referans dünya, yere toplama, `statik-yok` 1000 · 1001 · 1002, tam pencere, U1'in yapılandırması). 21 koşu, 8 işçi, ~1,5 sa. Oran = PDR / ETX kâhini (U1 kaydından).

| varyant | geri alınan |
|---|---|
| `k` | hiçbiri (AODV-k) |
| `j` | hepsi (AODV-j, git `e5cd1b7~1`) |
| `g_yok` | G bayrağı ve karşılıksız RREP (K-244) |
| `rerr_yayin` | RERR'in tek-yayın dalı; her zaman yayın (K-244) |
| `dusurme_yok` | başarısız keşfin tamponunun düşmesi (K-242) |
| `mrt_6` | MY_ROUTE_TIMEOUT 11,2 → 6 s (K-242) |
| `titresim_yok` | yayın titreşimi (K-242) |

§6.2'nin önceki atlama tazelemesi (K-242) ayrıca geri alınmaz. Etkisi `j` ile tek değişiklikli varyantların farkından okunur.

## Ölçüt (geçerlilik)

- **`k` U1'i birebir tekrar etmeli:** 0,8441 · 0,8445 · 0,8079 (deterministik).
- **`j` AODV-j'nin kaydını tekrar etmeli:** PDR 0,8859 · 0,9084 · 0,8580 (`ciktilar2/aodv_uygunluk/aodv_referans_2026_yere_toplama_son.json`, K-224). Statik kol `-yok`; K-243'ün yer–hava değişikliği karıştırıcısız kola girmez.
- İkisinden biri tutmazsa teşhis düzeni hatalıdır; yorumlanmaz.

## Yorum kuralı (ölçmeden önce)

- Bir varyantın oranı `k`'ninkinden üç hücrenin ortalamasında **R'den (0,0126) fazla** yüksekse, geri aldığı değişiklik düşüşe katkı yapıyordur.
- Katkı yapan değişiklik için iki durum ayrılır:
  - **(a) ns-3'ün ve RFC'nin davranışı, gerçekleme doğru:** değişiklik kalır. Rakibin kaynağına sadık hâli budur; düşük hücreler anatomiyle protokolün sınırı olarak açıklanır (K-207).
  - **(b) Gerçekleme ns-3'ten ayrılıyor ya da bir kusur var:** düzeltilir, yeni K kaydı, U1 ve regresyon. Örnek: tek-yayın RERR'in dayandığı öncül listeleri ns-3'ünkinden eksikse.
- (a) ile (b)'nin ayrımı koddan ve ns-3 kaynağından yapılır, sonuçtan değil.

## Ön bilgi (ölçüt değil)

- ns-3 RREP iletiminde dört öncül ilişkisi kurar (`aodv-routing-protocol.cc` `RecvReply`): ileri rotaya ve hedefe doğru sonraki atlamanın girdisine kaynağa doğru sonraki atlama; ters rotaya ve kaynağa doğru sonraki atlamanın girdisine hedefe doğru sonraki atlama. Bizim gerçekleme RFC §6.7'nin metnindeki ilk ikisini kurar.
- Tek-yayın RERR (K-244) öncül listesine dayanır; eksik öncül, RERR'i alması gereken komşuyu dışarıda bırakabilir.

## Öngörüler (ölçüt değil)

- En olası katkı `rerr_yayin` (yayın RERR öncül listesinde olmayan kullanıcılara da ulaşıyordu, K-210'un dersi) ve `dusurme_yok` (başarısız keşfin paketleri artık düşüyor).
- `titresim_yok` ve `g_yok`un katkısı küçük ya da ters yönde beklenir.
