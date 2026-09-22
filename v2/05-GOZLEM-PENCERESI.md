# 05 · GÖZLEM PENCERESİ — protokolün görebildiği her şey

> **Güncel:** 16 Eylül 2026 (K-131) · **Türü:** sözleşme. Öğrenci kararı:
> genişletilmez; gerekçeli bir değişikliğin yolu §7'de.
> Kod karşılığı: `sim2/gozlem/pencere.py` ve yüzey taraması testleri.
> Protokolün **yapabilecekleri** ayrı bir sözleşmededir: `13-KONTROL-DUZLEMI.md`.
> Önceki sürüm: `arsiv/05-GOZLEM-PENCERESI-2026-09-10.md`.

## 1 · Neden var

Bir jüri üyesi şunu sorabilir: *"Protokolünüz karıştırıcının nerede olduğunu
nereden biliyordu?"* Cevap *"bilmiyordu"* olmalı ve kanıtı bir cümle değil, bir
test olmalı. Önceki simülatörde bir rakibin tazelik bilgisini kendi
paketlerinden mi aldığı yoksa simülatörden mi okuduğu cevapsız kalmıştı; bu
sözleşme o belirsizliği yapısal olarak kapatır.

## 2 · Temel ilke

> Bir protokolün bildiği her şey ya **aldığı bir paketten** ya da **kendi
> donanımının fiziksel olarak yapabileceği bir ölçümden** gelir. Simülatörden
> bedava okuma yoktur.

Emin olunamayan durumda sorulacak soru: *"Gerçek bir İHA'nın üstündeki gerçek
bir telsiz bunu ölçebilir mi?"*

---

## 3 · Görebilecekleri

### 3.1 Kendi donanımından

| alan | gerçek karşılığı |
|---|---|
| anteninde ölçülen toplam gürültü + girişim gücü | gürültü tabanı ölçümü |
| kanalın meşgul olup olmadığı | taşıyıcı dinleme |
| kuyruğundaki paket sayısı | kendi belleği |
| kendi saati | düğümler arası senkron değil (§3.2) |
| son iletiminin sonucu | onay geldi · zaman aşımı |
| gönderdiği ve aldığı bayt | kendi sayaçları |

"Cevap gelmedi" bir bilgi yokluğu değil, bir gözlemdir ve bayta mal olmaz.

Bu simülatörde gürültünün **mutlak** değeri serbest bir ölçektir (K-110 EK-4):
karıştırmayı mutlak bir eşikle sezen protokol, fizikte karşılığı olmayan bir
sayıya dayanır. Sezim oranla ya da değişimle yapılır.

### 3.2 Saat senkronu yok

Düğüm saatleri ofset ve sapmayla ayrışır; gerçek taktik ağlarda da GPS
senkronu varsayılamaz. Sonuç:

| | |
|---|---|
| ölçülemez | tek yönlü gecikme (iki farklı saat gerekir) |
| ölçülebilir | **gidiş-dönüş süresi** (gönderim → onay, tek saatle) · kendi kuyruğunda bekleme süresi |

Gecikme terimi kullanan bir maliyet fonksiyonu gidiş-dönüş süresini kullanır.

### 3.3 Aldığı paketlerden

Başlıkta yazan her şey okunabilir, üç koşulla:

1. Başlıktaki her alan **bayt olarak ödenir** ve çerçeveyi uzatır — bedel
   yalnız sayaçta değil **kanalda da** ödenir (K-111; kontrol mesajlarında
   `13` §02.1).
2. Bilgi **bayattır**: gönderildiği andaki hâline aittir.
3. Paket **kaybolabilir**.

Komşusunun girişim seviyesini ya da kuyruk durumunu kullanmak isteyen
protokol, o alanları başlığa koyar ve bedelini öder. Konum ve hareket
bilgisi de böyledir: pencereye bedava gelmez.

🔴 **`bildirdigi_konum` alanı 16 Eylül 2026'da KALDIRILDI (K-131).** Sözleşme
onu *"3B, bedeli otomatik faturalanır"* diye anlatıyordu ama koşucu onu hiç
doldurmuyordu: ölçüldü, 110 605 komşu kaydının **%100'ünde** `None`. Belge bir
yetenek anlatıyor, kod vermiyordu. Doldurmak yerine kaldırıldı — çünkü
doldurmak, *"konum beacon'da taşınır"* kararını protokol adına simülatörün
vermesi olurdu. Konum isteyen protokol onu yukarıdaki yoldan taşır ve öder.

🔴 **Bilgi yokluğu sıfır değildir (K-131).** Bir protokol bir alanı beacon'a
koymazsa komşu kaydında o alan **`None`** döner, `0` değil. Önceden `0`
dönüyordu ve *"ölçtü, sıfır buldu"* ile *"hiç koymadı"* ayrışmıyordu; bu,
projenin her yerinde uygulanan `None ≠ 0` kuralının tek istisnasıydı.

### 3.4 Kendi geçmişinden

Yukarıdakilerin her türlü işlenmiş hâli: ortalamalar, sayaçlar, tahminler,
tablolar.

### 3.5 Komşu listesi — en kolay kaçırılan kâhin

Komşu, **yalnız yakın geçmişte beacon'ı alınmış** düğümdür. Menzil
hesabından ya da konumlardan türetilmiş hazır bir liste verilmez. Sonuçları:

1. Beacon bayta sayılır — komşu bilmek bedava değildir.
2. Karıştırma altında beacon da kaybolur ve komşu görünmez olur; gerçek bir
   telsizde de böyledir.
3. t = 0'da hiçbir düğüm hiçbir komşusunu bilmez.

Komşu listesi bedava verilseydi protokol karıştırma altında *"o düğüm hâlâ
orada"* bilgisini ücretsiz alırdı; bu, karıştırmanın en temel etkisini iptal
ederdi.

---

## 4 · Göremeyecekleri

| görmez | neden |
|---|---|
| karıştırıcının konumu, gücü, açık olup olmadığı | hiçbir telsiz bunu bilmez; gürültüyü hisseder, kaynağını görmez |
| diğer düğümlerin konumu | ancak bir pakette geldiyse ve bedeli ödendiyse |
| ağın gerçek topolojisi | hiçbir düğümde bütünsel görüntü yoktur |
| bir bağın gerçek kalitesi | yalnız kendi denemelerinden çıkardığı tahmin kullanılır |
| gerçek en kısa yol | simülatörün bilgisidir |
| bir paketin ileride teslim edilip edilmeyeceği | geleceğe bakmak |
| başka bir düğümün tablosu ya da durumu | ancak paketle geldiyse |
| simülatörün olay kuyruğu, tohumu, iç durumu | hiçbir koşulda |
| menzil içindeki düğümlerin listesi | komşuluk ölçülür, verilmez (§3.5) |
| bir komşunun hâlâ hayatta olduğu | beacon gelmiyorsa komşu yoktur |

Simülatörün belleğindeki "gerçek ETX" gibi değerlere protokol dokunamaz;
yalnız teşhis ve analiz kodu okur ve okuduğu şey rapora girer, karara değil.

---

## 5 · Nasıl zorlanıyor

- **Yapısal ayrım:** protokol simülatör nesnesini görmez; donmuş bir görünüm
  alır. `protokoller/` paketi yalnız `gozlem/`i içe aktarabilir.
- **Otomatik test:** görünümün yüzeyi taranır; izin listesinin dışındaki bir
  alan testi kırar. Bugünkü yüzey **12 gözlem + 6 komşu + 5 paket = 23
  alan**dır (`13` §04). *(24 → 23: `bildirdigi_konum` kaldırıldı, K-131.)*
- **Pencere artık HER KANCADA sunuluyor (K-131).** Gözlem 16 Eylül 2026'ya
  kadar TEK bir yerde üretiliyordu: veri gönderme kararı. Kontrol düzleminin
  beş kancası, `beacon_yuku` ve `beacon_alindi` gözlem almıyordu. Yüzey
  BÜYÜMEDİ — değişen tek şey, pencerenin ne zaman sunulduğudur.
- **Geri referans yok:** kontrol düzleminin niyet tipleri de dahil hiçbir
  görünüm simülatöre ulaşan bir nesne taşımaz (`13` P6).

---

## 6 · Bugünkü kullanım ve Aşama 2'de dikkat edilecekler

Depodaki koşum aletleri ve kâhinler 23 alanın yalnız **5**'ini okuyor.
Karıştırma sezimi için gereken alanların (ölçülen gürültü, son iletim sonucu,
kanal meşguliyeti, duyulan beacon, son duyulma anı, kuyruk uzunluğu) hiçbiri
henüz okunmuyor.

🔴 **İkisi 16 Eylül 2026'ya kadar kullanılamaz durumdaydı (K-131).**
`kanal_mesgul_mu` yapısal olarak neredeyse sabitti — ölçüldü, 24 558 karar
anının yalnız **%2,17**'sinde `True` — çünkü gözlem tam da düğümün kanalı
BOŞ BULDUĞU anda üretiliyordu. Ve protokol kendi ölçtüğü gürültüyü beacon'a
koyamıyordu, çünkü koyarken ölçemiyordu. Kancalara gözlem verilmesi ikisini
de açtı; Aşama 3'ün tasarım uzayı farkında olmadan daraltılmış durumdaydı. *(K-111 §5; yöntem: `protokoller/` ve kâhin modülünde AST
nitelik adı taraması — okunan sayı için üst sınırdır; çalıştırılabilir bir
komut olarak kaydedilmedi.)* Bu bir kusur değil, protokollerin henüz
yazılmadığının göstergesidir.

Taban protokoller bu sözleşmeye şu yerlerde basacak:

| protokol | riskli yer | ilgili madde |
|---|---|---|
| AODV · AOMDV | RREQ/RREP ağ çapında dolaşır; ara düğüm paketin taşıdığından fazlasını çıkarmamalı | §3.3 — başlıktaki her alan ödenir |
| OLSR | MPR seçimi iki atlamalık komşuluk ister; bu bilgi yalnız HELLO'lardan gelmeli | §3.5 — komşuluk ölçülür |
| hepsi | rota tablosu kendi geçmişinden kurulur | §3.4 |

---

## 7 · Değişiklik yolu

Bir protokol yeni bir alana ihtiyaç duyarsa:

1. Alan önce bu belgeye gerekçesiyle yazılır: gerçek bir telsiz bunu
   ölçebilir mi?
2. `04`e karar kaydı düşülür.
3. Önceki sonuçların hâlâ geçerli olup olmadığı ölçülür.

Daraltma o güne kadarki ölçümleri, genişletme ise eski ve yeni sonuçların
karşılaştırılabilirliğini etkiler; ikisi de bu yüzden kayıtla yapılır.

---

## 8 · Teşhis sayaçları — ayrı kanal

Simülatörün her şeyi bilen tarafı gerçek değerleri (gerçek bağ kalitesi,
fiziksel kopma, karar anındaki bilginin yaşı…) teşhis ve rapor için okur;
bunlar karara girmez.

> Aynı büyüklüğün **gerçek değeri** yalnız rapora, **protokolün tahmini**
> yalnız karara gider. Kod incelemesinde ilk bakılacak yer burasıdır.

---

## 9 · Sonuç satırı

Her koşu tam konfigürasyonunu, tohumunu, kod özetini, korunum sonucunu ve
ölçüm penceresini taşır; satır anında diske yazılır. Korunumu tutmayan satır
geçersiz işaretlenir.
