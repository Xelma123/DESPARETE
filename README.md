# DESPARETE

**Karıştırma (jamming) altındaki taktik İHA mesh ağları için yönlendirme protokolü — ve onu dürüstçe ölçmek için yazılmış bir simülatör.**

TÜBİTAK 2204-A Lise Öğrencileri Araştırma Projeleri · Yazılım / Bilgisayar Bilimleri

> *In English:* DESPARETE is a high-school research project (TÜBİTAK 2204-A) that designs a routing protocol for tactical UAV mesh networks under RF jamming. The repository contains a purpose-built discrete-event simulator with a 1:1 reference world (802.11b radio, realistic jammers), faithful implementations of three baseline protocols (AODV, OLSR, AOMDV), and the measurement tooling used to compare them. Documentation is in Turkish.

---

## Proje ne yapıyor?

Bir İHA sürüsünde düğümler birbirinin paketini taşır: telemetri yer istasyonuna, komutlar ters yönde gider. Karıştırıcı devreye girdiğinde bağlar rastgele değil **yapılı** biçimde bozulur — karıştırıcı bir yerde durur ya da hareket eder, sürekli ya da aralıklı yayın yapar, alıcıyı sağırlaştırır ya da yakınındaki vericiyi susturur. Proje iki soruya cevap arıyor:

1. Yaygın yönlendirme protokolleri (AODV · OLSR · AOMDV) bu koşullarda **nasıl ve ne kadar** bozuluyor?
2. Öğrencinin protokolü **DESPARETE** karıştırmayı gerçek bir telsizin ölçebildikleriyle fark edip ondan kaçınarak daha iyisini yapabilir mi?

Çalışma bir **tasarım projesidir**: çözüm kurulur ve kontrollü bir ortamda ölçülerek savunulur. Önceden ilan edilmiş bir yanlışlanma koşulu tetiklenirse sonuç, iyi teşhis edilmiş bir negatif sonuç olarak raporlanır.

## Durum — 28 Eylül 2026

Simülatör gerçek ölçekli referans dünyaya taşındı ve doğrulandı. Taban protokollerin son kalibrasyonu sürüyor; ardından DESPARETE'nin karıştırmaya özgü mekanizmaları geliştirilecek, ön-kayıt mühürlenecek (~12 Kasım) ve ana deney koşulacak. Teslim: 19 Aralık 2026. Güncel durum ve plan: [`v2/12-YOL-HARITASI.md`](v2/12-YOL-HARITASI.md).

---

## Depoda ne var?

| dizin | içerik |
|---|---|
| [`sim2/`](sim2) | kesikli-olay simülatörü |
| [`protokoller/`](protokoller) | AODV (RFC 3561) · OLSR (RFC 3626) · AOMDV (Marina & Das 2001) · DESPARETE (`desparete*.py`) |
| [`kalibrasyon/`](kalibrasyon) | ölçüm, kalibrasyon ve kabul kapısı araçları — belgelerdeki sayıların üreticileri |
| [`analiz/`](analiz) | ön-kaydın istatistik planı (Wilcoxon, Holm, eşik, güç) |
| [`tests2/`](tests2) | test takımı (pytest) |
| [`v2/`](v2) | proje belgeleri |
| [`protokol_kaynaklari/`](protokol_kaynaklari) | birincil kaynaklar, uygulama kaynakları, DESPARETE tasarım paketi, literatür taraması |

Betiklerin ürettiği sonuç dosyaları depoya dahil değildir; her makinede yerel olarak üretilir.

---

## Simülatör

Hazır bir ağ simülatörü yerine projenin kendi simülatörü yazıldı: karşılaştırmanın her varsayımı görünür, sınanabilir ve jüri önünde savunulabilir olsun diye.

- **Referans dünya (1:1):** 40 İHA, 33 km'lik alan, 50–300 m irtifa, 40–120 km/h; dört hareketlilik kolu — statik · bağımsız · görev · formasyon. Her sayı kaynaklı ya da ölçülmüş ([`v2/14`](v2/14-REFERANS-DUNYA.md)).
- **Telsiz ve kanal:** 802.11b DSSS (işlem kazancı, 1–11 Mb/s hız uyarlaması, enerji sezmeli taşıyıcı dinleme), 20 dBm EIRP; serbest uzay yol kaybı, gölgeleme, Rician hızlı sönümleme, yer–hava kanalı; parça başına SINR → paket hata olasılığı.
- **MAC:** IEEE 802.11 DCF, onay ve yeniden deneme, yakalama etkisi.
- **Tehdit:** beş karıştırıcı sınıfı (sürekli · darbeli · reaktif · aldatıcı · taramalı) ve beş tehdit ailesi (tek merkez · cephe hattı · derin sızma · hedef koruma · hava eşlik).
- **Trafik:** yere toplama (telemetri + komut) ve eşler arası.

Tasarımın dürüstlük güvenceleri koda yapısal olarak gömülüdür:

- **Kâhin bilgisi karara giremez.** Protokoller yalnız gerçek bir telsizin ve otopilotun verebileceği gözlem penceresini görür; sızıntı testle denetlenir.
- **Hiçbir paket sessizce kaybolmaz.** Her koşuda `üretilen = teslim + düşen + kuyrukta + uçuşta` denetlenir.
- **Aynı tohum, aynı dünya.** Kanal rastgeleliği protokolden bağımsızdır; aynı tohumda her protokol birebir aynı dünyayı, trafiği ve kanalı görür — karşılaştırmalar eşleştirilmiştir.
- **Her parametrenin kökeni kayıtlı:** türetilmiş · ölçülmüş · kaynak · duyarsız · tedavi · kol tanımı · sınanmamış; mimari denetimi sayar.

Doğrulama dört seviyededir: analitik karşılaştırma, korunum kontrolleri, iç tutarlılık ve yayımlanmış bir sonucun (Li vd., çok atlamalı zincir kapasitesi) yeniden üretilmesi. Ayrıntı: [`v2/07`](v2/07-SIMULATOR-TASARIMI.md).

## Taban protokoller

Üç protokol de birincil kaynaklarına sadık yazıldı; parametreler RFC varsayılanıdır ve hiçbiri senaryoya göre ayarlanmaz. Modellenmeyen özellikler ve belirsiz noktalardaki seçimler her protokolün başlığında gerekçesiyle beyan edilir ([`aodv_bicim.py`](protokoller/aodv_bicim.py) · [`olsr_bicim.py`](protokoller/olsr_bicim.py) · [`aomdv.py`](protokoller/aomdv.py)). Kabul kapısı (U1): karıştırıcısız kollarda protokolün teslim oranı aynı dünyada koşan bir kâhine oranlanır.

## DESPARETE

Hedef-yönlü bir uzaklık-vektörü protokolü: hedef — öncelikle geçit — ağa kendi "alanını" yayar, düğümler paketi bu alan boyunca iletir.

- **Döngüsüzlük** TTL'ye değil, hedefin ürettiği sıra numarasına ve uygulanabilirlik mesafesine dayanır (Babel, RFC 8966 ailesinin koşulu).
- **Yönlü bağ maliyeti** kalite ve riskten: kalite düğümün kendi iletim sonuçlarından ölçülür.
- **Postürler** (STEADY · CAUTION · PROTECT): gözlenen bozunmaya kademeli tepki.
- Geliştirilmekte olanlar: karıştırmaya özgü kanıt (RSSI, kanal doluluğu, PHY hataları), öngörülü kaçınma, kanıta dayalı postür, seçici çok yol ve çoğaltma. "Karıştırıcı tespiti" iddiası yoktur; protokol yalnız yerel olarak ölçebildiğine göre davranır.

Tasarım paketi: [`protokol_kaynaklari/DESPARETE_TASARIM_PAKETI/`](protokol_kaynaklari/DESPARETE_TASARIM_PAKETI) — tek okumalık özet `36_DESPARETE_V0_1_CANDIDATE_SPEC.md`.

## Yöntem

- **Ön-kayıt.** Hipotezler, eşiklerin türetme formülleri ve analiz planı sonuç görülmeden yazılır; ana deney tohumlarıyla (2000–2039) mühürden önce hiçbir protokol koşulmaz — [`v2/06`](v2/06-ON-KAYIT.md).
- **İstatistik.** Ana deney 40 tohum; eşleştirilmiş, çift yönlü Wilcoxon testi, aile içinde Holm düzeltmesi; sonuçlar etki büyüklüğü ve güven aralığıyla.
- **Metrikler üçlü sunulur:** teslim · gecikme · kontrol yükü; ayrıca karıştırmaya tepki (şok derinliği, toparlanma süresi, tespit gecikmesi).
- **Ablasyon.** Özgün protokolün mekanizmaları ayrı yapılandırma bayraklarıyla açılıp kapanır; bir kazancın hangi mekanizmadan geldiği ölçülür.
- **Kararlar** konu konu [`v2/04-KARARLAR.md`](v2/04-KARARLAR.md), tarihçesi [`v2/kayit/KARAR-GUNLUGU.md`](v2/kayit/KARAR-GUNLUGU.md).

> **Bir şeyi iddia etmeden önce ölç. Ölçemiyorsan iddia etme.**

---

## Kurulum ve çalıştırma

Gereksinimler: **Python 3.11**, `numpy`, `scipy`, `pytest` (geliştirme: Python 3.11.8 · numpy 2.4.6 · scipy 1.17.1 · pytest 8.2.2).

```bash
pip install numpy scipy pytest
```

Komutlar depo kökünden çalıştırılır; Windows konsolunda `PYTHONIOENCODING=utf-8` gerekir.

```bash
PYTHONIOENCODING=utf-8 python -m pytest tests2 -q            # test takımı, 15–30 dk
PYTHONIOENCODING=utf-8 python kalibrasyon/mimari_denetimi.py  # mimari ve parametre kökenleri
```

**Tek bir koşu** — referans dünyada, statik kolda, kısa pencerede AODV:

```python
from sim2.kanal.dunya import referans_2026
from sim2.kosum.kurulum import kurulum_yap
from sim2.kosum.kosu import Kosu
from sim2.kosum.sonuc import sonuc_satiri
from protokoller.aodv import AODV

kfg = referans_2026(kol="ornek", senaryo="statik-yok", tohum=1000,
                    trafik_deseni="yere_toplama",
                    karistirici_baslangic_s=5.0, isinma_s=10.0,
                    olcum_bitis_s=40.0, kosu_bitis_s=50.0)
kur = kurulum_yap(kfg)
kosu = Kosu(kur, lambda i: AODV(i))
kosu.kostur()
satir = sonuc_satiri(kur, kosu.dugumler, "aodv")
print(satir["korunum"]["gecerli"], satir["metrikler"]["pdr_pencere"])
```

Senaryo adı `<hareketlilik kolu>-<karıştırıcı sınıfı>` biçimindedir (ör. `formasyon-surekli`). `Konfig()` doğrudan kullanılırsa eski 1:50 ölçekli geliştirme dünyası kurulur; deneyler referans dünyada koşar. Tam uzunlukta (350 s) bir koşu karıştırıcılı hareketli kolda tek çekirdekte ~1 saat sürer.

---

## Simülasyon ve gerçeklik

Bu çalışma bir kavram kanıtıdır. Kullanılan yayılım ve karıştırma modelleri gerçek RF ortamının basitleştirilmiş temsilleridir. Sonuçlar saha performansı öngörüsü olarak yorumlanmamalıdır; bulgular yalnız modellenen koşullar altında **göreli** karşılaştırma olarak geçerlidir. Gerçek RF, SDR ve uçuş testi kapsam dışıdır.

## Yapay zekâ kullanımı

Proje fikri, kapsam ve gerçekçilik kararları ve DESPARETE'nin tasarımı öğrenciye aittir; yapay zekâ danışman ve uygulayıcı olarak kullanıldı. Kararlar tarihli olarak kayıtlıdır ve bir mekanizmanın katkısı ablasyonla ölçülür.

## Lisans

Henüz bir lisans seçilmedi. [`protokol_kaynaklari/`](protokol_kaynaklari) içindeki üçüncü taraf belgelerin hakları sahiplerine aittir.
