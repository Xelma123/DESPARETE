# DESPARETE

**Karıştırma (jamming) altındaki taktik İHA mesh ağları için yönlendirme protokolü — ve onu dürüstçe ölçmek için yazılmış bir simülatör.**

TÜBİTAK 2204-A Lise Öğrencileri Araştırma Projeleri · Yazılım / Bilgisayar Bilimleri

> *In English:* DESPARETE is a high-school research project (TÜBİTAK 2204-A) that designs a routing protocol for tactical UAV mesh networks under RF jamming. The repository contains a purpose-built discrete-event simulator, faithful implementations of three baseline protocols (AODV, OLSR, AOMDV), and the measurement tooling used to compare them. Documentation is in Turkish.

---

## Proje ne yapıyor?

Bir İHA sürüsünde düğümler birbirinin paketini taşır. Karıştırıcı devreye girdiğinde bağlar rastgele değil **yapılı** biçimde bozulur: karıştırıcı bir yerde durur ya da hareket eder, sürekli ya da darbeli yayın yapar, birden fazla olabilir. Proje iki soruya cevap arıyor:

1. Yaygın yönlendirme protokolleri (AODV · OLSR · AOMDV) bu koşullarda **nasıl ve ne kadar** bozuluyor?
2. Bağ kalitesini yerel olarak ölçen, döngüsüzlüğü sıra numarasıyla güvenceye alan özgün bir protokol — **DESPARETE** — daha iyisini yapabilir mi?

Çalışma bir **tasarım projesidir**: çözüm kurulur ve kontrollü bir ortamda ölçülerek savunulur. Önceden ilan edilmiş bir yanlışlanma koşulu tetiklenirse sonuç, iyi teşhis edilmiş bir negatif sonuç olarak raporlanır.

## Durum — 23 Eylül 2026

| aşama | içerik | durum |
|---|---|---|
| 1 · Simülasyon | ölçüm ortamının kurulması, doğrulanması ve kalibrasyonu | ✅ tamamlandı |
| 2 · Taban protokoller | AODV, OLSR, AOMDV; uygunluk kapıları (U1–U4) | ✅ üçü de kabul kapısından geçti |
| 3 · Özgün protokol | DESPARETE v0.1'in gerçeklenmesi | 🟡 sürüyor — tasarım hazır, gerçekleme başladı |
| 4 · Veri toplama | ön-kaydın mühürlenmesi, ana deney, istatistik | ⏳ |
| 5 · Rapor ve sunum | yazım, görselleştirme | ⏳ teslim: 19 Aralık 2026 |

Güncel durum, açık işler ve ölçülmüş sayılar (üretici komutlarıyla birlikte): [`v2/12-YOL-HARITASI.md`](v2/12-YOL-HARITASI.md).

---

## Depoda ne var?

| dizin | içerik |
|---|---|
| [`sim2/`](sim2) | kesikli-olay simülatörü |
| [`protokoller/`](protokoller) | taban protokoller: AODV (RFC 3561) · OLSR (RFC 3626) · AOMDV (Marina & Das 2001 + RFC 3561); DESPARETE buraya yazılacak |
| [`kalibrasyon/`](kalibrasyon) | ölçüm, kalibrasyon ve kabul kapısı betikleri — belgelerdeki sayıların üreticileri |
| [`tests2/`](tests2) | test takımı (pytest) |
| [`v2/`](v2) | proje belgeleri: problem, yöntem, karar kaydı, ön-kayıt, simülatör tasarımı, yol haritası |
| [`protokol_kaynaklari/`](protokol_kaynaklari) | birincil kaynaklar, DESPARETE tasarım paketi ve literatür taraması |

Betiklerin ürettiği sonuç dosyaları (`ciktilar2/`) depoya dahil değildir; her makinede yerel olarak üretilir.

---

## Simülatör

Hazır bir ağ simülatörü yerine projenin kendi simülatörü yazıldı: karşılaştırmanın her varsayımı görünür, sınanabilir ve jüri önünde savunulabilir olsun diye.

- **Dünya:** 40 İHA, 1800 m'lik alan, 3B Gauss-Markov hareketi; dört hareketlilik kolu — statik · bağımsız · görev (müfreze) · formasyon.
- **Kanal:** yol kaybı, gölgeleme, dipol anten deseni ve Rician hızlı sönümleme; SINR → paket hata olasılığı tek bir fonksiyonda; yakalama (capture) etkisi.
- **MAC:** IEEE 802.11 DCF (CSMA/CA, temel erişim), tek radyolu alıcı zinciri, onay ve yeniden deneme.
- **Tehdit:** beş karıştırıcı sınıfı (sürekli · darbeli · reaktif · aldatıcı · taramalı) ve beş tehdit senaryosu ailesi (tek merkez · cephe hattı · derin sızma · hedef koruma · hava eşlik).
- **Trafik:** yere toplama (düğümlerden geçide telemetri + geçitten düğümlere komut) ve eşler arası CBR.
- **Saatler:** her düğümün kendi, senkron olmayan saati — zaman damgası bedava senkronizasyon sağlamaz.

Tasarımın dürüstlük güvenceleri koda yapısal olarak gömülüdür:

- **Kâhin bilgisi karara giremez.** Protokoller yalnız gözlem penceresini görür (`sim2/gozlem/`); konum, topoloji ya da kanal bilgisine erişim içe aktarma grafiği testiyle engellenir.
- **Hiçbir paket sessizce kaybolmaz.** Her koşuda `üretilen = teslim + düşen + kuyrukta + uçuşta` korunum denklemi denetlenir.
- **Aynı tohum, aynı dünya.** Rastgelelik kaynak başına ayrı akışlardan ve durumsuz hash alanlarından gelir; aynı tohumda her protokol birebir aynı dünyayı, trafiği ve kanalı görür — karşılaştırmalar eşleştirilmiştir.
- **Her parametrenin kökeni kayıtlı.** Her sayı yedi kovadan birindedir (türetilmiş · ölçülmüş · kaynak · duyarsız · tedavi · kol tanımı · sınanmamış); mimari denetimi bunu her koşumda sayar.

Doğrulama dört seviyededir: analitik karşılaştırma, korunum kontrolleri, iç tutarlılık ve yayımlanmış bir sonucun (Li vd.) yeniden üretilmesi. Ayrıntı: [`v2/07-SIMULATOR-TASARIMI.md`](v2/07-SIMULATOR-TASARIMI.md).

## Taban protokoller

Üç protokol de birincil kaynaklarına sadık yazıldı; parametreler RFC varsayılanıdır ve hiçbiri senaryoya göre ayarlanmaz. Modellenmeyen özellikler ve belirsiz noktalardaki seçimler her protokolün başlığında gerekçesiyle beyan edilir ([`aodv_bicim.py`](protokoller/aodv_bicim.py) · [`olsr_bicim.py`](protokoller/olsr_bicim.py) · [`aomdv.py`](protokoller/aomdv.py)).

Üçü de aynı kabul kapısından (U1) geçti: karıştırıcısız dört kolda, protokolün teslim oranı aynı konfigürasyonda koşan bir ETX kâhinine oranlanır. Bu bir kabul testidir, ana deneyin karşılaştırması değildir.

## DESPARETE

Hedef-yönlü bir uzaklık-vektörü protokolü: her hedef — öncelikle geçit — ağa kendi "alanını" yayar ve düğümler paketi bu alan boyunca hedefe doğru iletir. Temel fikirleri:

- **Döngüsüzlük TTL'ye değil, hedefin ürettiği sıra numarasına ve uygulanabilirlik mesafesine (feasibility distance) dayanır** — Babel (RFC 8966) ailesinin koşulu.
- **Yönlü bağ maliyeti** `C = 16 + C_kalite(Q) + C_risk(R)`: kalite, düğümün kendi unicast sonuçlarından (tekrar sayısıyla ağırlıklı) ölçülür; risk, süregelen kötüleşme ve belirsizlikten.
- **Postürler** (STEADY · CAUTION · PROTECT): gözlenen bozunmaya ihtiyatlı, kademeli tepki.
- "Karıştırıcı tespiti" iddiası yoktur; protokol yalnız yerel olarak ölçebildiğine göre davranır.

Tasarım paketi (v0.1): [`protokol_kaynaklari/DESPARETE_TASARIM_PAKETI/`](protokol_kaynaklari/DESPARETE_TASARIM_PAKETI) — tek okumalık özet `36_DESPARETE_V0_1_CANDIDATE_SPEC.md`.

## Yöntem

- **Ön-kayıt.** Hipotezler, eşiklerin türetme formülleri ve analiz planı sonuç görülmeden yazılır; ana deney tohumları (2000–2039) mühürden önce hiçbir kolda koşulmaz — [`v2/06-ON-KAYIT.md`](v2/06-ON-KAYIT.md).
- **İstatistik.** Ana deney 40 tohum; eşleştirilmiş, çift yönlü Wilcoxon testi, aile içinde Holm–Bonferroni düzeltmesi; sonuçlar etki büyüklüğü ve güven aralığıyla raporlanır.
- **Metrikler üçlü sunulur:** teslim · gecikme · kontrol yükü. Tek metrikle sıralama yapılmaz.
- **Ablasyon.** Özgün protokolün her mekanizması ayrı bir yapılandırma bayrağıyla açılıp kapanabilecek; böylece bir kazancın hangi mekanizmadan geldiği ölçülebilecek.
- **Karar kaydı.** Her önemli karar tarihiyle, alternatifleriyle ve gerekçesiyle kayıtlıdır — [`v2/04-NEDEN-BOYLE.md`](v2/04-NEDEN-BOYLE.md).

> **Bir şeyi iddia etmeden önce ölç. Ölçemiyorsan iddia etme.**

---

## Kurulum ve çalıştırma

Gereksinimler: **Python 3.11**, `numpy`, `scipy`, `pytest`. Geliştirme ortamındaki sürümler: Python 3.11.8 · numpy 2.4.6 · scipy 1.17.1 · pytest 8.2.2.

```bash
pip install numpy scipy pytest
```

Komutlar depo kökünden çalıştırılır. Windows konsolunda Türkçe karakterler için `PYTHONIOENCODING=utf-8` gerekir.

**Test takımı** (makineye göre 8–25 dakika):

```bash
PYTHONIOENCODING=utf-8 python -m pytest tests2 -q
```

**Mimari denetimi** — katman yönü, belirlenimcilik, parametre kökenleri (birkaç saniye):

```bash
PYTHONIOENCODING=utf-8 python kalibrasyon/mimari_denetimi.py
```

**Tek bir koşu** — kısa pencerede, statik kolda AODV:

```python
from sim2.yapilandirma.konfig import Konfig
from sim2.kosum.kurulum import kurulum_yap
from sim2.kosum.kosu import Kosu
from sim2.kosum.sonuc import sonuc_satiri
from protokoller.aodv import AODV

kfg = Konfig(kol="ornek", senaryo="statik-yok", tohum=1000,
             karistirici_baslangic_s=5.0, isinma_s=10.0,
             olcum_bitis_s=40.0, kosu_bitis_s=50.0)
kur = kurulum_yap(kfg)
kosu = Kosu(kur, lambda i: AODV(i))
kosu.kostur()
satir = sonuc_satiri(kur, kosu.dugumler, "aodv")
print(satir["korunum"]["gecerli"], satir["metrikler"]["pdr_pencere"])
```

Senaryo adı `<hareketlilik kolu>-<karıştırıcı sınıfı>` biçimindedir (ör. `bagimsiz-surekli`). Örnekteki kısa pencere yarım dakika mertebesinde koşar; tam uzunlukta (350 s simülasyon zamanı) koşular çok daha uzundur ve hareketli kollarda tek bir koşu onlarca dakika sürebilir. Kalibrasyon ve kabul kapısı betiklerinin kullanımı ve süre bantları her betiğin başlığında yazılıdır; bazıları saatler sürer ve çok çekirdek kullanır.

---

## Belgeler

| belge | konu |
|---|---|
| [`01-PROBLEM-VE-AMAC`](v2/01-PROBLEM-VE-AMAC.md) | problem, kapsam, beş aşamalı iş akışı, başarı ölçütü |
| [`03-YONTEM-KURALLARI`](v2/03-YONTEM-KURALLARI.md) | yöntem ilkeleri ve bu alanın hata sınıfları |
| [`04-NEDEN-BOYLE`](v2/04-NEDEN-BOYLE.md) | karar kaydı — en yeniden geriye okunur |
| [`05-GOZLEM-PENCERESI`](v2/05-GOZLEM-PENCERESI.md) · [`13-KONTROL-DUZLEMI`](v2/13-KONTROL-DUZLEMI.md) | protokolün görebildikleri ve yapabildikleri — sözleşme |
| [`06-ON-KAYIT`](v2/06-ON-KAYIT.md) | hipotezler, metrikler, uygunluk testleri, istatistik planı |
| [`07-SIMULATOR-TASARIMI`](v2/07-SIMULATOR-TASARIMI.md) | simülatörün tasarımı ve öğrenci kararlarının tek listesi |
| [`12-YOL-HARITASI`](v2/12-YOL-HARITASI.md) | güncel durum ve plan |

Belgelerin tam listesi: [`v2/README.md`](v2/README.md).

## Simülasyon ve gerçeklik

Bu çalışma bir kavram kanıtıdır. Kullanılan yayılım ve karıştırma modelleri gerçek RF ortamının basitleştirilmiş temsilleridir. Sonuçlar saha performansı öngörüsü olarak yorumlanmamalıdır; bulgular yalnız modellenen koşullar altında **göreli** karşılaştırma olarak geçerlidir. Gerçek RF, SDR ve uçuş testi kapsam dışıdır.

## Fikir sahipliği ve yapay zekâ kullanımı

Proje fikri, kapsam ve gerçekçilik kararları ve DESPARETE'nin tasarımı öğrenciye aittir. Yapay zekâ bu projede danışman ve uygulayıcı olarak kullanıldı. Bu yüzden iki alışkanlık baştan tutuldu: her önemli kararın kim tarafından, hangi alternatiflere karşı ve neden verildiğinin tarihli kaydı ([`v2/04`](v2/04-NEDEN-BOYLE.md), öğrenci kararlarının tek listesi [`v2/07`](v2/07-SIMULATOR-TASARIMI.md) §15) ve bir mekanizmanın katkısının ablasyonla ölçülmesi.

## Lisans

Henüz bir lisans seçilmedi. [`protokol_kaynaklari/`](protokol_kaynaklari) içindeki üçüncü taraf belgelerin hakları sahiplerine aittir.
