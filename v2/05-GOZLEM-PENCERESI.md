# 05 · GÖZLEM PENCERESİ — protokolün görebildiği her şey

> **Güncel:** 17 Kasım 2026 · **Türü:** sözleşme — gerekçesiz genişletilmez, değişikliğin yolu §7. Kod `sim2/gozlem/pencere.py` · yüzey testi `tests2/test_kontrol_duzlemi.py` (P6). Protokolün **yapabilecekleri** `13`te. Önceki sürümler `v2/arsiv/05-GOZLEM-PENCERESI-*.md`. Bölüm numaraları kodda atıflı, korunur.

## 1 · Amaç

Protokolün karıştırıcının yerini, gücünü ya da açık olup olmadığını bilmediğinin bir testle gösterilebilmesi. Karşılaştırmanın geçerliliği buna bağlıdır.

## 2 · Temel ilke

Protokolün bildiği her şey ya **aldığı bir paketten** ya da **kendi donanımının fiziksel olarak yapabileceği bir ölçümden** gelir. Simülatörden bedava okuma yoktur. Ölçüt: gerçek bir İHA'daki gerçek bir telsiz bunu ölçebilir mi?

## 3 · Görebilecekleri

**3.1 Kendi donanımından** (K-180):

| alan | gerçek karşılığı |
|---|---|
| `dugum` | kendi adresi (802.11 MAC adresi) |
| `saat_s` | kendi saati — ofset ve sapmalı (§3.2) |
| `olculen_gurultu_w` | anteninde ölçülen gürültü + girişim gücü (sürücünün gürültü tabanı raporu). Simülatörde anlık, hatasız ve sürekli değerlidir. Gerçek sürücü (ath9k, `02` G18) onu olağan kipte 30 s'de bir okur, son 5 ölçümün ortancasını alır ve kırparak tamsayı dBm verir. Bu yüzden **protokol kararına girmez**: mimari denetimi okunmasını engeller (D17; K-227) |
| `kanal_mesgul_mu` | CCA göstergesi (G2: mod 1/2/3; güç kipinde önbelge kilidi ya da ED, K-174) |
| `kuyruk_uzunlugu` · `kuyruk_kapasitesi` | kendi arayüz kuyruğu |
| `son_iletim_sonucu` · `son_iletim_hedefi` | MAC'in gönderim durumu raporu: onay · zaman aşımı. "Cevap gelmedi" bir gözlemdir, bayta mal olmaz |
| `gonderilen_bayt` · `alinan_bayt` | arayüz bayt sayaçları |
| `komsular` | yalnız alınan beacon'lardan (§3.5) |
| `paket` | karar verilen paketin başlığı (§3.3) |

GPS/INS ve telsiz sayaçları §3.3b'de, çerçeve başına RSSI §3.3a'da.

**3.2 Saat senkronu yok:** saatler ofset ve sapmayla ayrışır (taktik ağda GPS senkronu varsayılamaz).
- Tek yönlü gecikme ölçülemez; **gidiş-dönüş süresi** ve kendi kuyruğundaki bekleme ölçülür. Gecikme terimli maliyet gidiş-dönüşü kullanır.
- `dogum_s` bu yüzden pencerede yoktur; olsaydı iki düğüm saat farkını bedavaya öğrenirdi.

**3.3 Aldığı paketlerden:** başlıktaki her şey, üç koşulla:
1. her alan **bayt olarak ödenir** ve çerçeveyi uzatır; bedel kanalda da ödenir (K-111; kontrol mesajlarında `13` §02.1);
2. bilgi gönderildiği anındır (bayat);
3. paket kaybolabilir.

Komşunun girişimi, kuyruğu, konumu ve hareketi ancak başlığa konup ödenirse gelir.
- **`kaynak_sira`** (K-157): paketin kaynağın kendi ürettikleri arasındaki sırası; kimlik `(kaynak, kaynak_sira)`.
  - Gerçek karşılığı: IPv4 kimlik alanı; başlıkla ödenir (`veri_baslik_bayt`).
  - Küresel paket kimliği açılmaz; iki kimlik farkı bütün ağın ürettiğini söylerdi.
- **`rota`** (K-232): kaynak rotası, yani DSR ailesinde veri paketinin başlığında yazan ara düğümler (RFC 4728 §6.7).
  - Bedeli adres başına bayt olarak çerçeveyi uzatır ve yönlendirme ek yüküne sayılır.
  - Rota taşımayan protokolde boştur.
- **Bilgi yokluğu sıfır değildir** (K-131): beacon'a konmayan alan komşu kaydında `None` döner, `0` değil.

**3.3a Çözdüğü her çerçeveden (K-172):** isteğe bağlı `cerceve_duyuldu` kancası. Bana ya da başkasına adresli her çözülen çerçeve için şunları verir:
- gönderen komşu (802.11 başlığındaki verici adresi);
- tür ve adreslendiği düğüm;
- veri çerçevesinde paket başlığı;
- RSSI: kilitlenilen güç + σ 2 dB hata, tamsayı dBm.

σ kaynaksızdır ve JarmRout okuduğu için SINANMAMIŞ'tır (K-233); duyarlılığı mühürden önce ölçülür. Gerçek karşılığı telsizin izleme kipi ve sürücünün çerçeve başına RSSI raporudur. Kanca niyet döndürmez; karıştırıcı çerçevesi gelmez.

**3.3b Kendi GPS/INS'i ve telsiz sayaçları (K-179):**

| alan | gerçek karşılığı | model |
|---|---|---|
| `kendi_konum` · `kendi_hiz` | otopilotun GPS/INS çözümü | gerçek + hata: yatay 1,5 m CEP (G7) · dikey σ 2 m · hız σ 0,1 m/s; 1 Hz dilimde sabit. Dikey σ kaynaksız ve JarmRout konumu okuduğu için SINANMAMIŞ (K-233); hız σ okunmuyor (DUYARSIZ, K-214) |
| `mesgul_sure_s` | sürücünün "channel busy time" sayacı (802.11k kanal yükü) | CCA'nın meşgul kaldığı toplam süre, olay güdümlü tam integral; yalnız `kanal_dolulugu_ister` diyen protokole, ötekinde `None`. Beyan: çizelgeli sürekli sınıfta karıştırıcının açılıp kapandığı anda parça bölünmez (`gecis_anlari` boş), parçanın durumu ortasında okunur; etkisi bir düğümün iki çerçeve olayı arasıyla sınırlı, ölçülmedi (`arsiv/teshis/faz5_2_isaretler_2026-11-16/beklenti.md`, duman notu) |
| `phy_hata` | CRC hatalı çerçeve sayacı | kilitlenip gövdesi çözülemeyen çerçeve. Önbelgesi hiç kilitlenmeyen uzak zayıf çerçeveler sayılmaz; gerçek telsiz onları sezmez |
| `alinan_cerceve` | alınan çerçeve sayacı | başarıyla çözülen her çerçeve |

Komşunun konumu ve hareketi yalnız bedeli ödenmiş mesajla gelir (§3.3). Bu beş alanın hiçbiri karıştırıcının yerini, gücünü ya da açık/kapalı durumunu doğrudan taşımaz. `mesgul_sure_s` karıştırıcının enerjisini içerir; bunu gerçek telsiz de ölçer.

**3.4 Kendi geçmişinden:** yukarıdakilerin her türlü işlenmiş hâli (ortalama, sayaç, tahmin, tablo).

**3.5 Komşu listesi:** komşu yalnız **yakın geçmişte beacon'ı alınmış** düğümdür; menzilden ya da konumdan hazır liste verilmez.
- Beacon bayta sayılır.
- Karıştırmada beacon da kaybolur, komşu görünmez olur.
- t = 0'da kimse kimseyi bilmez.

Bedava bir liste, karıştırmanın en temel etkisini ("o düğüm hâlâ orada mı") ortadan kaldırırdı.

## 4 · Göremeyecekleri

| görmez | neden |
|---|---|
| karıştırıcının konumu, gücü, açık olup olmadığı | telsiz gürültüyü hisseder, kaynağını görmez |
| diğer düğümlerin konumu · başka düğümün tablosu/durumu | ancak ödenmiş bir paketle |
| gerçek topoloji · gerçek en kısa yol · bir bağın gerçek kalitesi | simülatörün bilgisi; protokol kendi tahminini kullanır |
| bir paketin ileride teslim edilip edilmeyeceği | geleceğe bakmak |
| olay kuyruğu, tohum, simülatör iç durumu | hiçbir koşulda |
| menzil içindeki düğümler · komşunun hâlâ hayatta olduğu | komşuluk ölçülür; beacon gelmiyorsa komşu yoktur |
| bir komşunun düştüğü (vurulma, arıza) | haber verilmez; protokol onu sessizliğinden anlar (K-180) |

## 5 · Nasıl zorlanıyor

- **Yapısal ayrım:** protokol donmuş bir görünüm alır; `protokoller/` yalnız `gozlem/`i içe aktarabilir (kaçamaklar dâhil taranır — `tests2/test_kosum.py`).
- **Yüzey testi:** izin listesi dışındaki alan testi kırar. Bugün **17 gözlem + 6 komşu + 7 paket = 30 alan** (son ekleme `rota`, K-232).
- **Pencere her kancada sunulur** (K-131).
- **Geri referans yok:** niyet tipleri dâhil hiçbir görünüm simülatöre ulaşan nesne taşımaz (`13` P6).
- **Okunan alanın kökeni:** bir protokol bir ölçüm alanını okumaya başlarsa mimari denetimi o alanın hata parametresini DUYARSIZ bırakmaz (D17).

## 6 · Karıştırma sezimi ve taban protokoller

Sezim için kullanılabilecek alanlar: son iletim sonucu · kanal meşguliyeti (`kanal_mesgul_mu`, `mesgul_sure_s`) · PHY hatası · çerçeve başına RSSI · duyulan beacon ve son duyulma anı · kuyruk uzunluğu. Ölçülen gürültü kullanılmaz (§3.1).

Taban protokollerin sözleşmeye bastığı yerler:
- **AODV:** RREQ/RREP'te ara düğüm paketin taşıdığından fazlasını çıkarmaz (§3.3).
- **OLSRv2:** iki atlamalık komşuluk yalnız HELLO'dan gelir (§3.5).
- **Babel:** bağ maliyeti komşunun çoklu-yayın Hello'larının kendi geçmişinden (ETX), ters yönün maliyeti komşunun IHU'sundan; bağ katmanı bildirimi kullanılmaz.
- **JarmRout** (rakip değil, Faz 4b'nin kaydı; K-242): bağ kalitesi kendi RSSI örneklerinden, yük kendi kanal doluluğu ve kuyruğundan, konum yalnız RREQ'de taşınan (ödenen) koordinattan gelir.
- **Hepsi** rota tablosunu kendi geçmişinden kurar (§3.4).

## 7 · Değişiklik yolu

Yeni alan gerekirse:
1. önce bu belgeye gerekçesiyle yazılır ("gerçek telsiz ölçebilir mi?");
2. `04`e karar kaydı girer;
3. önceki sonuçların geçerliliği ölçülür.

Daraltma o güne kadarki ölçümleri, genişletme eski-yeni karşılaştırılabilirliğini etkiler; ikisi de kayıtla yapılır.

## 8 · Teşhis kanalı — ayrı

Simülatörün her şeyi bilen tarafı gerçek değerleri (gerçek bağ kalitesi, fiziksel kopma, kararın bilgi yaşı…) yalnız teşhis ve rapor için okur. Aynı büyüklüğün **gerçek değeri** yalnız rapora, **protokolün tahmini** yalnız karara gider. Kod incelemesinde ilk bakılacak yer burasıdır.

## 9 · Sonuç satırı

Her koşu tam konfigürasyonunu, tohumunu, kod özetini, korunum sonucunu ve ölçüm penceresini taşır; anında diske yazılır. Korunumu tutmayan satır geçersiz işaretlenir.
