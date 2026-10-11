# 05 · GÖZLEM PENCERESİ — protokolün görebildiği her şey

> **Güncel:** 10 Ekim 2026 (öz sürüm; son içerik değişikliği K-232) · **Türü:** sözleşme — genişletilmez, gerekçeli değişikliğin yolu §7. Kod `sim2/gozlem/pencere.py` · yüzey testi `tests2/test_kontrol_duzlemi.py` (P6). Protokolün **yapabilecekleri** `13`te. Önceki sürümler `v2/arsiv/05-GOZLEM-PENCERESI-*.md`. Bölüm numaraları kodda atıflı, korunur (10 Eylül öncesinin A1–A4'ü = §3.1–3.5).

## 1 · Neden var

Jüri sorusu: *"Protokolünüz karıştırıcının nerede olduğunu nereden biliyordu?"* Cevap "bilmiyordu" olmalı ve kanıtı bir test olmalı (önceki simülatörde bir rakibin tazelik bilgisini nereden aldığı cevapsız kalmıştı).

## 2 · Temel ilke

> Protokolün bildiği her şey ya **aldığı bir paketten** ya da **kendi donanımının fiziksel olarak yapabileceği bir ölçümden** gelir. Simülatörden bedava okuma yok. Şüphede: *"Gerçek bir İHA'daki gerçek bir telsiz bunu ölçebilir mi?"*

## 3 · Görebilecekleri

**3.1 Kendi donanımından** — her alanın gerçek karşılığı (K-180):

| alan | gerçek karşılığı |
|---|---|
| `dugum` | kendi adresi (802.11 MAC adresi) |
| `saat_s` | kendi saati — ofset ve sapmalı (§3.2) |
| `olculen_gurultu_w` | anteninde ölçülen gürültü + girişim gücü (sürücünün gürültü tabanı raporu). Mutlak değeri serbest bir ölçek (K-110 EK-4): sezim oranla ya da değişimle yapılır, mutlak eşikle değil. **Simülatörde anlık, hatasız ve sürekli değerli.** Gerçek sürücü (ath9k, `02` G18) onu olağan kipte 30 s'de bir okur, son 5 ölçümün ortancasını alır, −95 dBm tabanından ve yonganın üst sınırında kırparak tamsayı dBm verir. Bu yüzden **protokol kararına girmez**: mimari denetimi okunmasını engeller (D17; K-227, denetim D-04) |
| `kanal_mesgul_mu` | CCA göstergesi (G2: mod 1/2/3; güç kipinde önbelge kilidi ya da ED, K-174) |
| `kuyruk_uzunlugu` · `kuyruk_kapasitesi` | kendi arayüz kuyruğu |
| `son_iletim_sonucu` · `son_iletim_hedefi` | MAC'in gönderim durumu raporu: onay · zaman aşımı. "Cevap gelmedi" bir gözlemdir, bayta mal olmaz |
| `gonderilen_bayt` · `alinan_bayt` | arayüz bayt sayaçları |
| `komsular` | yalnız alınan beacon'lardan (§3.5) |
| `paket` | karar verilen paketin başlığı (§3.3) |

Yeni beş alan (GPS/INS ve telsiz sayaçları) §3.3b'de, çerçeve başına RSSI §3.3a'da.

**3.2 Saat senkronu yok:** saatler ofset ve sapmayla ayrışır (taktik ağda GPS senkronu varsayılamaz). Tek yönlü gecikme ölçülemez; **gidiş-dönüş süresi** ve kendi kuyruğundaki bekleme ölçülür. Gecikme terimli maliyet gidiş-dönüşü kullanır. `dogum_s` bu yüzden pencerede yok — olsaydı iki düğüm saat farkını bedavaya öğrenirdi.

**3.3 Aldığı paketlerden:** başlıktaki her şey, üç koşulla — (1) her alan **bayt olarak ödenir** ve çerçeveyi uzatır, bedel kanalda da ödenir (K-111; kontrol mesajlarında `13` §02.1) · (2) bilgi gönderildiği anındır (bayat) · (3) paket kaybolabilir. Komşunun girişimi, kuyruğu, konumu ve hareketi ancak başlığa konup ödenirse gelir.
- `bildirdigi_konum` **kaldırıldı** (K-131): koşucu hiç doldurmuyordu (110 605 komşu kaydının %100'ü `None`); doldurmak "konum beacon'da taşınır" kararını protokol adına vermek olurdu.
- `kaynak_sira` **eklendi** (K-157): paketin kaynağın kendi ürettikleri arasındaki sırası; kimlik `(kaynak, kaynak_sira)`. Gerçek karşılığı IPv4 kimlik alanı ve DESPARETE'nin Data Sequence'i (tasarım paketi `19` §4), başlıkla ödenir (`veri_baslik_bayt`). Gerekçe: onarım tamponundaki paketi tanımak (tasarım paketi `21` §2.4 kotası, K-156). Küresel paket kimliği bilerek açılmadı — iki kimlik farkı bütün ağın ürettiğini söylerdi.
- `rota` **eklendi** (K-232): kaynak rotası — DSR ailesinde veri paketinin başlığında yazan ara düğümler (RFC 4728 §6.7). Gerçek karşılığı DSR'nin kaynak rotası seçeneği; bedeli adres başına bayt olarak çerçeveyi uzatır ve yönlendirme ek yüküne sayılır. Gerekçe: JarmRout'un (Pu 2018) DSR'ye dayanan iletimine sadakat. Rota taşımayan protokolde boş; önceki sonuçlar değişmez (regresyon).
- **Bilgi yokluğu sıfır değildir** (K-131): beacon'a konmayan alan komşu kaydında `None` döner, `0` değil.

**3.3a Çözdüğü her çerçeveden (K-172):** isteğe bağlı `cerceve_duyuldu` kancası — bana ya da başkasına adresli her çözülen çerçevenin gönderen komşusu (802.11 başlığındaki verici adresi), türü, adreslendiği düğüm, veri çerçevesinde paket başlığı ve RSSI (kilitlenilen güç + σ 2 dB hata, tamsayı dBm; σ kaynaksız — bugün okuyan protokol olmadığı için DUYARSIZ (K-214); bir protokol okumaya başlarsa mimari denetimi kaydı yeniden açar, D17). Gerçek karşılığı: telsizin izleme kipi ve sürücünün çerçeve başına RSSI raporu. Niyet döndürmez; karıştırıcı çerçevesi gelmez. "Bu paket bana hangi komşudan geldi" bilgisi buradan gelir.

**3.3b Kendi GPS/INS'i ve telsiz sayaçları (K-179):**

| alan | gerçek karşılığı | model |
|---|---|---|
| `kendi_konum` · `kendi_hiz` | otopilotun GPS/INS çözümü | gerçek + hata: yatay 1,5 m CEP (G7), dikey σ 2 m, hız σ 0,1 m/s (ikisi kaynaksız; okuyan yok → DUYARSIZ, K-214; okunursa mimari D17 yeniden açar), 1 Hz dilimde sabit |
| `mesgul_sure_s` | sürücünün "channel busy time" sayacı (802.11k kanal yükü) | CCA'nın meşgul kaldığı toplam süre, olay güdümlü tam integral; yalnız `kanal_dolulugu_ister` diyen protokole, ötekinde `None` |
| `phy_hata` | CRC hatalı çerçeve sayacı | kilitlenip gövdesi çözülemeyen çerçeve. Önbelgesi hiç kilitlenmeyen uzak zayıf çerçeveler sayılmaz — gerçek telsiz onları sezmez |
| `alinan_cerceve` | alınan çerçeve sayacı | başarıyla çözülen her çerçeve |

Komşunun konumu ve hareketi hâlâ YOK — yalnız bedeli ödenmiş mesajla (§3.3). Sızıntı sınavı korunur: beş alanın hiçbiri karıştırıcının yerini, gücünü ya da açık/kapalı durumunu doğrudan taşımaz. `mesgul_sure_s` karıştırıcının **enerjisini** içerir; bunu gerçek telsiz de ölçer.

**3.4 Kendi geçmişinden:** yukarıdakilerin her türlü işlenmiş hâli (ortalama, sayaç, tahmin, tablo).

**3.5 Komşu listesi — en kolay kaçırılan kâhin:** komşu yalnız **yakın geçmişte beacon'ı alınmış** düğümdür; menzilden ya da konumdan hazır liste verilmez. Beacon bayta sayılır · karıştırmada beacon da kaybolur, komşu görünmez olur · t = 0'da kimse kimseyi bilmez. Bedava liste, karıştırmanın en temel etkisini ("o düğüm hâlâ orada") iptal ederdi.

## 4 · Göremeyecekleri

| görmez | neden |
|---|---|
| karıştırıcının konumu, gücü, açık olup olmadığı | telsiz gürültüyü hisseder, kaynağını görmez |
| diğer düğümlerin konumu · başka düğümün tablosu/durumu | ancak ödenmiş bir paketle |
| gerçek topoloji · gerçek en kısa yol · bir bağın gerçek kalitesi | simülatörün bilgisi; protokol kendi tahminini kullanır |
| bir paketin ileride teslim edilip edilmeyeceği | geleceğe bakmak |
| olay kuyruğu, tohum, simülatör iç durumu | hiçbir koşulda |
| menzil içindeki düğümler · komşunun hâlâ hayatta olduğu | komşuluk ölçülür; beacon gelmiyorsa komşu yoktur |
| bir komşunun düştüğü (vurulma, arıza — K-180) | haber verilmez; protokol onu sessizliğinden anlar (K-180) |

## 5 · Nasıl zorlanıyor

- **Yapısal ayrım:** protokol donmuş bir görünüm alır; `protokoller/` yalnız `gozlem/`i içe aktarabilir (kaçamaklar dâhil taranır — `tests2/test_kosum.py`).
- **Yüzey testi:** izin listesi dışındaki alan testi kırar. Bugün **17 gözlem + 6 komşu + 7 paket = 30 alan** (K-131'de 23, K-157'de 24, K-179'da 29: B3'ün beş alanı, K-232'de 30: kaynak rotası).
- **Pencere her kancada sunulur** (K-131): önceden yalnız veri gönderme kararında üretiliyordu. Yüzey büyümedi; değişen sunulma anı.
- **Geri referans yok:** niyet tipleri dâhil hiçbir görünüm simülatöre ulaşan nesne taşımaz (`13` P6).

## 6 · Karıştırma sezimi ve taban protokoller

Sezim için gereken alanlar: ölçülen gürültü · son iletim sonucu · kanal meşguliyeti · duyulan beacon · son duyulma anı · kuyruk uzunluğu. K-111'de (koşum aletleri ve kâhinler) hiçbiri okunmuyordu. İkisi 16 Eylül'e kadar kullanılamazdı (K-131): `kanal_mesgul_mu` karar anlarının yalnız %2,17'sinde `True` idi (gözlem kanalın boş bulunduğu anda üretiliyordu) ve protokol ölçtüğü gürültüyü beacon'a koyamıyordu — kancalara gözlem verilmesi ikisini açtı.

Taban protokollerin sözleşmeye bastığı yerler: AODV/AOMDV RREQ/RREP'te ara düğüm paketin taşıdığından fazlasını çıkarmaz (§3.3) · OLSR MPR seçimi iki atlamalık komşuluğu yalnız HELLO'dan alır (§3.5) · hepsi rota tablosunu kendi geçmişinden kurar (§3.4).

## 7 · Değişiklik yolu

Yeni alan gerekirse: (1) önce bu belgeye gerekçesiyle ("gerçek telsiz ölçebilir mi?") · (2) `04`e karar kaydı · (3) önceki sonuçların geçerliliği ölçülür. Daraltma o güne kadarki ölçümleri, genişletme eski-yeni karşılaştırılabilirliğini etkiler; ikisi de kayıtla.

## 8 · Teşhis kanalı — ayrı

Simülatörün her şeyi bilen tarafı gerçek değerleri (gerçek bağ kalitesi, fiziksel kopma, kararın bilgi yaşı…) yalnız teşhis ve rapor için okur.

> Aynı büyüklüğün **gerçek değeri** yalnız rapora, **protokolün tahmini** yalnız karara gider. Kod incelemesinde ilk bakılacak yer burasıdır.

## 9 · Sonuç satırı

Her koşu tam konfigürasyonunu, tohumunu, kod özetini, korunum sonucunu ve ölçüm penceresini taşır; anında diske yazılır. Korunumu tutmayan satır geçersiz işaretlenir.
