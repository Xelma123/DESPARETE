# AODV-k'nin U1 düşüşü — hangi değişiklik? Sonuç

> 15 Ekim 2026 · ölçüt ve yorum kuralı `beklenti.md` (commit `1e51c4c`, koşudan önce) · kopya `1163f81` (`arsiv/teshis/rakipler_k244_2026-10-14/kopya`) · koşu 21:17–23:42, 2 sa 25 dk (beklenti ~1,5 sa; `titresim_yok` ve `mrt_6` koşuları 60–85 dk sürdü) · çıktılar `ab.txt` · `ab.jsonl` · `zaman.txt`

## 1 · Geçerlilik: tuttu

- `k` U1'i birebir tekrar etti: 0,8441 · 0,8445 · 0,8079.
- `j` AODV-j'nin kaydını (K-224) birebir tekrar etti: 0,8859 · 0,9084 · 0,8580.
- 21 koşunun hepsinde korunum geçerli.

## 2 · Oranlar (PDR / ETX kâhini, referans dünya, yere toplama, `statik-yok`)

| varyant | 1000 | 1001 | 1002 | ortalama | `k`'ye fark | tohum başına fark |
|---|---|---|---|---|---|---|
| `k` | 0,8522 | 0,8558 | 0,8123 | 0,8401 | | |
| `j` | 0,8944 | 0,9205 | 0,8628 | 0,8926 | +0,0524 | +0,042 · +0,065 · +0,050 |
| `g_yok` | 0,8611 | 0,8941 | 0,8325 | 0,8626 | **+0,0225** | +0,009 · +0,038 · +0,020 |
| `titresim_yok` | 0,8599 | 0,8899 | 0,8427 | 0,8642 | **+0,0240** | +0,008 · +0,034 · +0,030 |
| `rerr_yayin` | 0,8338 | 0,8542 | 0,8057 | 0,8312 | −0,0089 | −0,018 · −0,002 · −0,007 |
| `mrt_6` | 0,8705 | 0,8242 | 0,8019 | 0,8322 | −0,0079 | +0,018 · −0,032 · −0,010 |
| `dusurme_yok` | 0,8522 | 0,8558 | 0,8123 | 0,8401 | 0 | 0 · 0 · 0 |

Yorum kuralına göre (fark > R = 0,0126) **katkı yapan iki değişiklik var: G bayrağı ile karşılıksız RREP (K-244) ve yayın titreşimi (K-242).** İkisi üç tohumda da aynı yönde.

- İki katkının toplamı +0,0466; `j`'nin farkı +0,0524. Kalan 0,006 R'nin altında: §6.2 önceki atlama tazelemesi, öteki değişiklikler ve etkileşim.
- `rerr_yayin`: tek-yayın RERR yayından biraz iyi; düşüşe katkısı yok.
- `mrt_6`: tohumlar arasında işaret karışık. Tek bir değişikliğin tek tohumdaki etkisi ±0,03 oynayabiliyor; iki katkının ortalaması R'nin iki katı civarında, yönleri üç tohumda da aynı.
- `dusurme_yok` `k` ile birebir: statikte başarısız keşif yok (`kesif_basarisiz` 0), değişiklik bu hücrelerde hiç tetiklenmiyor. Bu düzen onun etkisini ölçemez.

Öngörü tutmadı. Katkısı beklenen `rerr_yayin` ve `dusurme_yok` katkı yapmadı; "küçük ya da ters" beklenen titreşim ve G katkı yaptı.

## 3 · (a) mı (b) mi — koddan ve ns-3 kaynağından

Kaynak: `protokol_kaynaklari/uygulama_kaynaklari/ns-3/aodv-routing-protocol.cc` (satır numaraları bu dosyanın).

### Titreşim → (a)

| ileti | ns-3 | bizim (`protokoller/aodv.py`) |
|---|---|---|
| RREQ üretimi | 1150, `GetInteger(0, 10)` ms | `_rreq_kur`, titreşimli |
| RREQ iletimi | 1512, aynı | `_rreq_isle` sonu, titreşimli |
| HELLO | 2011, aynı | `_rrep_kur(sonraki=None)`, titreşimli |
| RERR, tek-yayın ve yayın | 2182 · 2223, aynı | `_rerr_kur`, ikisi de titreşimli |
| RREP, tek-yayın (hedef, ara düğüm, karşılıksız) | `SendTo` doğrudan, titreşimsiz | titreşimsiz |

- Çağrı yerleri aynı. Değer 10 ms (`aodv_bicim.py`, `YAYIN_TITRESIMI_S`).
- Tek fark dağılım: ns-3 tamsayı milisaniye (0…10), biz sürekli U(0, 10 ms). Ortalama aynı.
- sim2 titreşimi mesajın MAC kuyruğuna girişini geciktirerek uygular (`sim2/kosum/kontrol.py`). Bu, ns-3'ün `Simulator::Schedule(…, SendTo)` çağrısıyla aynı yerdir.

### G bayrağı ve karşılıksız RREP → (a)

- **ns-3:**
  - `GratuitousReply` varsayılan açık (158 · 301–307).
  - `SendRequest` G'yi kurar (1108).
  - Ara düğüm yanıtında karşılıksız RREP (1593–1612). Alanları:
    - atlama: kaynağa giden girdinin atlaması;
    - hedef: kaynak;
    - kaynak: RREQ'in hedefi;
    - ömür: kaynağa giden girdinin ömrü.
  - Hedefe doğru sonraki atlamaya tek-yayın, titreşimsiz gider. İki öncül ilişkisi kurar (1576–1577).
- **Bizim** (`_rreq_isle`): aynı alanlar, aynı alıcı, titreşimsiz, aynı iki öncül.
  - Sıra alanında RFC §6.6.3'ün metnine uyuluyor: RREQ'in kaynak sırası. ns-3 tablodaki değeri koyuyor; ters rota güncellendikten hemen sonra o değer de aynı ya da daha büyük.
- **Bilinen fark:** ns-3, hedefe rotası RREQ'i gönderenden geçen ara düğümde RREQ'i düşürür (1452–1458). Bu RFC'de olmayan bir ek; 30 Eylül denetiminde alınmadı (`arsiv/teshis/aodv_sadakat_2026-09-30/denetim.md`) ve K-244'ün hakem ilkesiyle de alınmaz. Bu ek ns-3'te ara düğüm yanıtlarını, dolayısıyla karşılıksız RREP'leri azaltır; payı ölçülmedi.

### Öncül listeleri (beklentinin ön bilgisi) → değişmez

- `rerr_yayin` katkı yapmadı; yorum kuralı tetiklenmedi.
- ns-3 `RecvReply`, RFC §6.7'nin iki ilişkisine (1737 · 1742) ters yönde iki ilişki daha ekler (1745 · 1750). Bunlar RFC'de yok; hakem ilkesine (K-244) göre RFC dışı ek oldukları için alınmaz. Bizim gerçekleme RFC'nin ikisini kurar.

## 4 · Notlar (yorum kuralının dışında, mekanizma ölçülmedi)

Üç tohumun toplam sayaçları:

| sayaç | `j` | `k` | `g_yok` | `titresim_yok` |
|---|---|---|---|---|
| karşılıksız RREP | 0 | 31 705 | 0 | 27 038 |
| RREP iletimi | 21 439 | 48 695 | 26 450 | 41 589 |
| kara listeye ekleme | 1 868 | 4 931 | 2 844 | 3 856 |
| RERR üretimi | 36 697 | 44 933 | 35 597 | 42 868 |
| RREQ üretimi | 5 561 | 7 423 | 5 980 | 6 748 |
| veri iletim başarısızlığı | 2 932 | 3 569 | 3 645 | 2 908 |

- **G ve kara liste.** Ara düğüm yanıtlarının çoğu karşılıksız RREP de üretiyor; RREP trafiği yaklaşık iki katına çıkıyor. Bağ katmanında onaylanmayan karşılıksız RREP de kara liste kuruyor (K-194; AODV denetimi kural 32).
  - RFC §6.8 *"its transmission of a RREP message has failed"* der; karşılıksız RREP'i ayırmaz. Davranış metnin harfine uygun.
  - ns-3'te kara liste yalnız RREP-ACK zamanlayıcısından kurulur (`AckTimerExpire`, 1968). Bu dosyada zamanlayıcı yerel bir kopyada ayarlanıyor ve başlatılmıyor (1569–1574). K-194, RFC'nin bağ katmanı onayı iznine dayanır.
  - Bu etkileşimin PDR'deki payı ölçülmedi. Değişiklik önerilmiyor: davranış RFC'nin metnine uygun ve (a)/(b) ayrımı sonuçtan yapılmaz.
- **Titreşim ve veri iletim başarısızlığı.** Titreşimli kodda MAC'in vazgeçtiği veri çerçevesi yaklaşık %23 daha çok (2 908 → 3 569; `j` 2 932). Titreşimin amacı eşzamanlı yeniden yayınların çarpışmasını azaltmak; bu düzende veri çerçevelerinde ters yönde bir yan etki görünüyor. Mekanizma ölçülmedi. MAC bütün protokollerde ortak olduğundan bu, AODV'nin sadakat kararını değiştirmez.

## 5 · Karar ve sıradaki

**(a): iki değişiklik de ns-3'ün varsayılan davranışı ve gerçekleme ona uygun. AODV-k değişmez.** AODV-j'den düşüşü ns-3'ün iki varsayılanından geliyor: karşılıksız RREP ve yayın titreşimi. Rakibin kaynağına sadık hâli budur.

Yorum kuralına göre AODV-k'nin U1'deki düşük hücreleri anatomiyle protokolün sınırı olarak açıklanır (K-207). Yere toplamada yedi hücre:

- statik 1000 · 1001 · 1002;
- bağımsız 1000 · 1002;
- görev 1000 · 1001.

Anatomileri K-224'ün yoluyla, ayrı bir beklentiyle ölçülür (`kalibrasyon/kayip_anatomisi.py`). Ardından `ACIKLANMIS_DUSUK_REFERANS["aodv"]` ve `KAYITLI_ORAN["aodv"]` AODV-k'nin oranlarına güncellenir.

AODV kodu değişmediği için kuyruğun kalanı sürer:

- U1 eşler arası ara kayıttan devam eder;
- ardından G1ç, G2ç + G4ç ve G1-P.
