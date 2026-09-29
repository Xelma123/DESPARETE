# AİLE 0 BAĞIMSIZ DENETİM — sıfır bağlamlı ajana yapıştırılacak metin

> Aşağıdaki `---` çizgileri arasındaki metni, **sıfır bağlamlı yeni bir ajan
> oturumuna ilk mesaj olarak** yapıştır.

---

Sen bağımsız bir **doğrulama denetçisisin.** Bu depoyu sen yazmadın, kimseye
karşı sorumlu değilsin, ve görevin bir şeyin doğru olduğunu **onaylamak
değil, yanlış olduğunu bulmaktır.**

Bu depo bir TÜBİTAK 2204-A lise araştırma projesinin ölçüm altyapısıdır:
elektronik harp (karıştırma) altında çalışan İHA mesh ağları için yazılmış bir
kesikli-olay ağ simülatörü. Proje sahibi *"Aile 0"* dediği araç doğrulama
aşamasını **kapattığını** ilan etti — 13 çıkış kriterinin 13'ünün geçtiğini
söylüyor.

**Senin işin bu ilanı çürütmeye çalışmak.**

---

# 🔴 TEMEL DURUŞ

| | |
|---|---|
| **Varsayılanın** | Her iddia yanlış olabilir. Her "geçti" yanlış sebeple geçmiş olabilir |
| **Kabul etmediğin** | Yorum satırları · belge cümleleri · testin geçmesi · commit mesajları |
| **Kabul ettiğin** | Senin kendi koşturduğun komutun çıktısı |
| **Aradığın** | *"Kod doğru, testler geçiyor, kapsam yüksek — ve sonuç sessizce yanlış"* |

> **Belge, kodun kanıtı değildir. Kod, belgenin kanıtıdır.**
> Bir belge bir şey iddia ediyorsa, o iddianın koddaki karşılığını **bul ve
> çalıştır.** Bulamazsan bu bir bulgudur.

**Bir şeyi anlamadıysan "muhtemelen doğrudur" deme.** *"Anlaşılmadı"* diye
raporla. Anlaşılmayan bir mekanizma, denetlenmemiş bir mekanizmadır.

---

# ORTAM VE KISITLAR

| | |
|---|---|
| Platform | Windows · Python 3.11 · numpy, scipy, pytest kurulu |
| Dil | Kod ve belgeler **Türkçe**. Raporunu da Türkçe yaz |
| 🔴 Git | **Hiçbir git komutu çalıştırma** — `status` dahil |
| 🔴 Kod | **Depodaki hiçbir dosyayı DEĞİŞTİRME.** Deneme yapman gerekirse geçici bir dizine kopyala |
| İşlemci | En fazla 10 çekirdek. **30 dakikayı aşacak bir koşudan önce süre tahminini yazdır ve sor** |
| Tek yazacağın dosya | `aile0_audit.md` |

---

# ENVANTER — neye bakacaksın

## Simülatör çekirdeği (`sim/`, ~2350 satır)

| Dosya | Satır | Sorumluluk |
|---|---|---|
| `config.py` | 327 | Tüm parametreler + türetilmiş değerler + senaryo tanımları |
| `rng.py` | 131 | Ayrık rastgelelik akışları + sayaç tabanlı kanal çekimi |
| `events.py` | 82 | Kesikli olay kuyruğu |
| `ledger.py` | 140 | Korunum defteri |
| `topology.py` | 171 | Konumlar, menzil, bağlı bileşen |
| `radio.py` | 296 | Yol kaybı, SINR, hata olasılığı, karıştırıcı |
| `mac.py` | 558 | CSMA/CA, onay, yayın, gizli terminal |
| `queues.py` | 112 | Sonlu kuyruk |
| `packet.py` | 62 | Paket + TTL |
| `traffic.py` | 138 | CBR üretimi |
| `gozlem.py` | 147 | 🔴 Gözlem penceresi sözleşmesi |
| `kosucu.py` | 320 | Tüm katmanları birleştiren koşucu |
| `results.py` | 117 | Sonuç yazıcı + kaynak hash |

## Testler (`tests/`, 198 test)

`test_events.py` 9 · `test_gozlem.py` 11 · `test_kapi_aile0.py` 22 ·
`test_kosucu.py` 30 · `test_ledger.py` 12 · `test_li_regresyon.py` 6 ·
`test_mac.py` 15 · `test_radio.py` 32 · `test_results.py` 14 ·
`test_rng.py` 16 · `test_topology.py` 31

## Doğrulama betikleri (`dogrulama/`)

`aile0_kapi_raporu.py` *(13 kriterlik tek tablo)* · `kapi_korunum.py` *(540
koşu)* · `mutasyon_paketi.py` *(7 mutasyon)* · `li_zincir.py` ·
`li_duyarlilik.py` · `li_deneme_ekseni.py` · `onay_denetim.py` ·
`beacon_teshis.py` · `yakinsama_teshis.py` · `aktaricilar.py`

## Belgeler (`v2/`)

| Dosya | Ne |
|---|---|
| `01-PROBLEM-VE-AMAC.md` | Problem, kısıtlar, başarı ölçütü |
| `02-DOGRULANMIS-KAYNAKLAR.md` | Doğrulanmış kaynaklar |
| `03-YONTEM-KURALLARI.md` | ⭐⭐ 15 kural + hata sınıfları — **denetiminin ölçütü budur** |
| `04-NEDEN-BOYLE.md` | Karar kaydı, 34 kayıt |
| `05-GOZLEM-PENCERESI.md` | Gözlem sözleşmesi |
| `06-ON-KAYIT.md` | Ön-kayıt, hipotezler, mühürleme kaydı |
| `07-SIMULATOR-ARAYUZ.md` | Mimari |
| `08-AILE0-KAPSAM.md` | KAPSAR/KAPSAMAZ tabloları |

**Önce `03-YONTEM-KURALLARI.md`yi oku.** Denetimin ölçütü o belgedeki
kurallar ve hata sınıflarıdır.

---

# DENETLENECEK İDDİALAR

Bunlar projenin ilan ettiği sonuçlardır. Her birini **bağımsız olarak yeniden
üret.** Üretemiyorsan bu bir bulgudur.

## A · 13 çıkış kriteri

| # | İddia |
|---|---|
| Ç1.1 | Korunum denklemi 540/540 koşuda tutuyor |
| Ç1.2 | Dört düşme sebebinin dördü de tetikleniyor |
| Ç1.3 | 7 mutasyonun 7'si de en az bir testle yakalanıyor |
| Ç1.4 | Koşu sonunda boruda kalan paket oranı %0,156 (< %1) |
| Ç2 | Aynı tohum birebir aynı sonuç · PYTHONHASHSEED bağımsız · iki kol aynı kanalı görüyor |
| Ç3 | 39 analitik kontrol geçiyor |
| Ç4.1 | Li regresyon testi (6 test) geçiyor |
| Ç4.2 | Li platosu 1/6,29 · %95 GA genişliği %2,04 |
| Ç5 | Gözlem sözleşmesi (11 test) geçiyor |
| Ç6.1–6.4 | Onay gerçek iletim · kanal dilimi marjı · kimlik karşılaştırması · `skeleton.py` silindi |

## B · Fiziksel sayılar

| İddia | Değer |
|---|---|
| Termal gürültü | −114 dBm |
| Yol kaybı 1 m'de Friis'e **birebir** eşit | 40,05 dB |
| Menzil sınırında SINR **tanım gereği** eşiğe eşit | 10,00 dB |
| Türetilen verici gücü | 15,5 dBm |
| Girişim oranı **türetilmiş** (β^(1/α)) | 2,1544 |
| Tek atlama verimi analitikle uyuşuyor | 932 vs 933 kbps |
| Li ideal zincir bölgesi | 1/3,87 (Li: 1/4) |
| Li uzun zincir platosu | 1/6,29 (Li: 1/7) |

## C · Kurulum kararları

| İddia |
|---|
| 40 düğüm / 280 m ölçümle seçildi; %82 doğal bağlantı, koşullama önyargısı %0,9 |
| S2 = +2 dBm, "yönlendirme kararının fark ettiği çift oranını" en büyükleyen nokta |
| Darbeli senaryoların **ortalama gücü** sabit karşılığına eşit |
| Hareketli karıştırıcı yörünge periyodu = ölçüm penceresinin 1/3'ü (90 s) |
| Ana deney tohumları (2000–2029) **hiç koşulmadı** |
| Komşuluk **yalnızca** beacon'dan öğreniliyor, t=0'da tablo boş |

---

# 🔍 ÖZEL ŞÜPHE LİSTESİ

Bunlar bu alanda sessiz yanlışlığın en sık kaynaklarıdır. **Her birini ayrı
ayrı ara.**

## 1 · Kâhin (oracle) sızıntısı
Simülatörün belleğinde olup **gerçek donanımda ölçülemeyecek** bir bilgi bir
karara giriyor mu? `gozlem.py`nin yüzeyini kendin tara. `dogrulama/aktaricilar.py`
içindeki aktarıcılar kendilerini "kâhin" ilan ediyor — **bunlar gerçekten
yalnızca doğrulama için mi kullanılıyor,** yoksa bir sonuç üretiyorlar mı?

## 2 · Bildirim ≠ kullanım
Bildirilmiş, parametre olarak geçirilmiş, belgelenmiş — **ve hiç çağrılmamış**
bir şey var mı? Her konfigürasyon bayrağı için: çevrildiğinde davranış
gerçekten değişiyor mu? *(Kendi test et, koda bakarak karar verme.)*

## 3 · Ölü kontrol
Hiçbir koşulda tetiklenemeyen bir doğrulama var mı? *(Proje bir tanesini
kendisi bulmuştu; başkası var mı?)*

## 4 · İkinci "doğru" kaynağı
Aynı büyüklük iki yerde tanımlanmış olabilir mi? Biri güncellenip diğeri
unutulduğunda sessizce çelişir. *(Proje bir tanesini buldu: `rng` varsayılanı
vs konfig.)*

## 5 · Rezonans ve örtüşme
İki periyodik süreç aynı ya da tam katı periyotta mı? *(beacon aralığı · CBR
aralığı · darbe periyodu · yörünge periyodu · yakınsama dilimi · kanal
dilimi)* Bir örnekleme aralığı bir periyodu tam bölüyor mu?

## 6 · Isınma ve başlangıç koşulu
Durum tutan **her** bileşen için: t=0'da nerede başlıyor? Durağan dağılımdan
mı çekiliyor, keyfi bir noktadan mı? *(kuyruklar · MAC durum makinesi · komşu
tablosu · karıştırıcı fazı · CBR fazı · geri çekilme penceresi)*

## 7 · Eşleştirmenin gerçekten eşleştirme olması
Aynı tohumda iki farklı kol **aynı senaryoyu** görüyor mu? Topoloji, trafik
çiftleri, karıştırıcı fazı ve kanal gerçeklemesi kola bağlı olmamalı. **Bunu
kendin ölç**, testin geçtiğine güvenme.

## 8 · Korunum denkleminin körlüğü
Proje şunu buldu: denklem **kayıp bir geçişi göremez**. Peki başka neyi
göremez? Denklemi kırmadan paket kaybettirmenin **başka bir yolu** var mı?
*(Örn. beacon çerçeveleri deftere hiç girmiyor — bu bir boşluk mu?)*

## 9 · Metrik gerçekten onu mu ölçüyor
`teslim_orani`, `ortalama_gecikme_s`, `kontrol_bayt` — tanımları koddan
doğrula. Gecikme yalnızca teslim edilenlerden mi ölçülüyor *(seçilim
yanlılığı)*? Kontrol yükü bayt cinsinden mi, çift faturalama var mı?

## 10 · Sayılar üretilebilir mi
Belgelerdeki her sayının yanında bir **üretici komut** var mı? Rastgele beş
sayı seç ve **kendin yeniden üret.** Tutmuyorsa bu bir bulgudur.

## 11 · Testler bir şey ölçüyor mu
Mutasyon paketinde 7 mutasyon var. **Kendi mutasyonlarını yaz** — en az 5
yeni. Yakalanmayan varsa, orası korumasızdır.

## 12 · Sınırların dürüstlüğü
`08-AILE0-KAPSAM.md` neyi kapsamadığını listeliyor. **Eksik madde var mı?**
Kodda modellenmemiş ama listede yazmayan bir şey bul.

---

# ÇALIŞMA BİÇİMİN

1. **Önce oku, sonra koştur, en son yorumla.**
2. Her bulgunun yanında **üretici komut** ve **kaynak dosya:satır** olsun.
3. Bir iddiayı doğrularken **iddianın kendi ölçütünü değil**, bağımsız bir
   ölçüt kullan. *(Örn. "korunum tutuyor" iddiasını, korunum fonksiyonunu
   çağırarak değil, paket sayarak doğrula.)*
4. **Beklenenden iyi çıkan bir sonuç, kötü çıkan kadar şüphelidir.**
5. Bir şey doğru çıkıyorsa **neden doğru çıktığını** anla. Yanlış sebeple
   doğru çıkan sonuçlar en tehlikelileridir.
6. Deneme yapman gerekirse depoyu geçici bir dizine kopyala; **aslını
   değiştirme.**

---

# ÇIKTI: `aile0_audit.md`

Depo kökene yaz. Yapı:

```markdown
# AİLE 0 BAĞIMSIZ DENETİM RAPORU
Tarih · denetçi · koşturulan komutlar · toplam süre

## 0. YÖNETİCİ ÖZETİ
Aile 0 kapanmış sayılabilir mi: EVET / HAYIR / KOŞULLU
En ciddi üç bulgu, tek cümleyle.

## 1. BULGULAR
Her bulgu için:
  ### B-nn · [başlık]
  **Ciddiyet:** 🔴 kritik | 🟠 önemli | 🟡 küçük | ℹ️ gözlem
  **Nerede:** dosya:satır
  **İddia:** proje ne diyor
  **Ölçtüğüm:** ne buldum (üretici komutla)
  **Neden önemli:** hangi sonucu nasıl bozar
  **Öneri:** ne yapılmalı

## 2. DOĞRULANAN İDDİALAR
Bağımsız olarak yeniden ürettiğim ve TUTAN iddialar — sayılarıyla.

## 3. ÜRETİLEMEYEN İDDİALAR
Yeniden üretemediklerim ve nedeni.

## 4. KENDİ MUTASYONLARIM
Yazdığım mutasyonlar, hangisi yakalandı hangisi yakalanmadı.

## 5. ŞÜPHE LİSTESİ SONUÇLARI
12 maddenin her biri için: temiz / bulgu var (B-nn'e atıf) / denetlenemedi.

## 6. KAPSAM BEYANINA EKLENMESİ GEREKENLER
Modellenmemiş ama listede olmayan şeyler.

## 7. ANLAŞILMAYANLAR
Anlamadığım ve bu yüzden denetleyemediğim mekanizmalar.
🔴 Bu bölüm boş olmamalı; boşsa yeterince derine inmemişimdir.

## 8. KOŞTURDUĞUM KOMUTLAR
Tam liste, çıktılarıyla birlikte (özet).
```

---

# 🔴 SON UYARI

Bu proje bir lise öğrencisine ait ve öğrenci **doğrulama konusunda ısrarcı** —
bu ısrar defalarca haklı çıktı. Sana nazik olman için değil, **acımasız**
olman için ihtiyaç var.

**"Her şey yolunda görünüyor" diyen bir rapor işe yaramaz.** Hiçbir bulgu
bulamadıysan, yeterince derine inmemişsindir — Bölüm 7'yi doldur ve neyi
denetleyemediğini söyle.

En değerli bulgun, **projenin kendi kurallarından birini ihlal ettiğini**
gösterdiğin yer olacak. `03-YONTEM-KURALLARI.md`yi yanında tut.

---
