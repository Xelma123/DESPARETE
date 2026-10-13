# DESPARETE

**Karıştırma (jamming) altındaki taktik İHA mesh ağları için bir yönlendirme protokolü ve onu ölçmek için yazılmış bir simülatör.**

TÜBİTAK 2204-A Lise Öğrencileri Araştırma Projeleri · Yazılım / Bilgisayar Bilimleri

> *In English:* DESPARETE is a high-school research project (TÜBİTAK 2204-A) that designs a routing protocol for tactical UAV mesh networks under RF jamming. The repository contains a purpose-built discrete-event simulator with a 1:1 reference world (802.11b radio, realistic jammers), source-faithful implementations of the baseline protocols (AODV, OLSRv2; a third baseline is under review), and the measurement tooling used to compare them. Documentation is in Turkish.

---

## Proje ne yapıyor?

Bir İHA sürüsünde düğümler birbirinin paketini taşır: telemetri yer istasyonuna, komutlar ters yönde gider. Karıştırıcı devreye girdiğinde bağlar rastgele değil **yapılı** biçimde bozulur: karıştırıcı bir yerde durur ya da hareket eder, sürekli ya da aralıklı yayın yapar, alıcıyı sağırlaştırır ya da yakınındaki vericiyi susturur. Proje iki soruya cevap arar:

1. Yaygın yönlendirme protokolleri bu koşullarda nasıl ve ne kadar bozuluyor? Kıyas tabanı reaktif AODV ve bağ durumu standardı OLSRv2'dir; üçüncü rakip açık karardır (`v2/04` §10).
2. Bu çalışmada önerilen **DESPARETE** protokolü, karıştırmayı gerçek bir telsizin ölçebildikleriyle fark edip ondan kaçınarak daha yüksek teslim sağlayabilir mi?

İkinci soru iki ayrı iddia olarak sınanır:
- **karıştırma altında daha yüksek teslim** (birincil test: karıştırıcının açık dönemlerinde doğan paketlerin teslim oranı);
- bu kazancın **karıştırmaya özgü** olması (karıştırıcısız ikiz hücreyle fark-içinde-fark ve mekanizmaların ablasyonu, [`v2/06`](v2/06-ON-KAYIT.md) §0.4.5).

Çalışma bir tasarım projesidir: çözüm kurulur ve kontrollü bir ortamda ölçülür. Önceden ilan edilmiş bir yanlışlanma koşulu tetiklenirse sonuç negatif sonuç olarak raporlanır.

## Durum — 13 Ekim 2026

- **Simülatör:** gerçek ölçekli referans dünyada kalibre edildi ve doğrulandı (Faz 4).
- **Taban protokoller:** AODV, OLSRv2 ve JarmRout kaynaklarına kural kural sadık yazıldı, kabul testinden geçti ve donduruldu. JarmRout'un kesin rakip olup olmayacağı açık karardır.
- **Sıradaki:** DESPARETE'nin karıştırmaya özgü mekanizmalarının geliştirilmesi (Faz 5), ön-kayıt mühürü (~20 Kasım) ve ana deney.
- **Teslim:** 19 Aralık 2026.

Güncel durum ve plan: [`v2/12-YOL-HARITASI.md`](v2/12-YOL-HARITASI.md).

---

## Depoda ne var?

| dizin | içerik |
|---|---|
| [`sim2/`](sim2) | kesikli-olay simülatörü |
| [`protokoller/`](protokoller) | taban protokoller: AODV (RFC 3561) · OLSRv2 (RFC 7181) · JarmRout (Pu 2018) · DESPARETE (`desparete*.py`). Faz 4'ün rakipleri OLSR (RFC 3626) ve AOMDV eski regresyon vakaları için durur |
| [`kalibrasyon/`](kalibrasyon) | ölçüm, kalibrasyon ve kabul kapısı araçları — belgelerdeki sayıların üreticileri |
| [`analiz/`](analiz) | ön-kaydın istatistik planı (Wilcoxon, Holm, eşik, güç) |
| [`tests2/`](tests2) | test takımı (pytest) |
| [`v2/`](v2) | proje belgeleri |
| [`protokol_kaynaklari/`](protokol_kaynaklari) | birincil kaynaklar, uygulama kaynakları, literatür taraması |
| [`arsiv/`](arsiv) | ölçüm teşhisleri, eski belge sürümleri, DESPARETE'nin v0.1 tasarım taslağı |

Betiklerin ürettiği sonuç dosyaları depoya dahil değildir; her makinede yerel olarak üretilir.

---

## Simülatör

Hazır bir ağ simülatörü yerine projenin kendi simülatörü yazıldı; amaç karşılaştırmanın her varsayımının görünür ve sınanabilir olmasıdır.

- **Referans dünya (1:1):** 40 İHA, 33 km'lik alan, 50–300 m irtifa, 40–120 km/h; dört hareketlilik kolu (statik · bağımsız · görev · formasyon). Her sayı kaynaklı ya da ölçülmüştür ([`v2/14`](v2/14-REFERANS-DUNYA.md)).
- **Telsiz ve kanal:**
  - 802.11b DSSS: işlem kazancı, 1–11 Mb/s hız uyarlaması, enerji sezmeli taşıyıcı dinleme; 20 dBm EIRP.
  - Kanal: serbest uzay yol kaybı, gölgeleme, Rician hızlı sönümleme, yer–hava kanalı.
  - Alıcı: parça başına SINR → paket hata olasılığı.
- **MAC:** IEEE 802.11 DCF, onay ve yeniden deneme, yakalama etkisi.
- **Tehdit:** beş karıştırıcı sınıfı (sürekli · darbeli · reaktif · aldatıcı · taramalı) ve beş tehdit ailesi (tek merkez · cephe hattı · derin sızma · hedef koruma · hava eşlik).
- **Trafik:** yere toplama (telemetri + komut) ve eşler arası.

Karşılaştırmanın geçerliliği için koda gömülü yapısal güvenceler:

- **Kâhin bilgisi karara giremez.** Protokoller yalnız gerçek bir telsizin ve otopilotun verebileceği gözlem penceresini görür; sızıntı testle denetlenir ([`v2/05`](v2/05-GOZLEM-PENCERESI.md)).
- **Hiçbir paket sessizce kaybolmaz.** Her koşuda `üretilen = teslim + düşen + kuyrukta + uçuşta` denetlenir.
- **Aynı tohum, aynı dünya.** Kanal rastgeleliği protokolden bağımsızdır; aynı tohumda her protokol birebir aynı dünyayı, trafiği ve kanalı görür, karşılaştırmalar eşleştirilmiştir.
- **Her parametrenin kökeni kayıtlıdır.** Kovalar: türetilmiş · ölçülmüş · kaynak · duyarsız · tedavi · kol tanımı · dünya tanımı · sınanmamış. Kapsamı daraltan kararlar ayrıca "kapsam ilanı" olarak kaydedilir; mimari denetimi sayar.

Doğrulama dört seviyededir: analitik karşılaştırma, korunum kontrolleri, iç tutarlılık ve yayımlanmış bir sonucun (Li vd., çok atlamalı zincir kapasitesi) yeniden üretilmesi. Ayrıntı: [`v2/07`](v2/07-SIMULATOR-TASARIMI.md).

## Taban protokoller

Protokoller birincil kaynaklarına kural kural sadık yazıldı; parametreler kaynak varsayılanıdır ve hiçbiri senaryoya göre ayarlanmaz. Modellenmeyen özellikler ve belirsiz noktalardaki seçimler her protokolün beyan tablosunda gerekçesiyle durur: [`aodv_bicim.py`](protokoller/aodv_bicim.py) · [`olsrv2_bicim.py`](protokoller/olsrv2_bicim.py) · [`jarmrout_bicim.py`](protokoller/jarmrout_bicim.py).

Kabul kapısı (U1): karıştırıcısız kollarda protokolün teslim oranı aynı dünyada koşan bir kâhine oranlanır. JarmRout'un makaledeki yinelenen istek kuralı toplu akışta tıkanıklık çöküşü üretir; bu ölçülmüş bir sınır olarak raporlanır ve üçüncü rakibin seçimi açık karardır ([`v2/04`](v2/04-KARARLAR.md) §5, §10).

## DESPARETE

Hedef-yönlü bir uzaklık-vektörü protokolü: hedef (öncelikle geçit) ağa kendi "alanını" yayar, düğümler paketi bu alan boyunca iletir.

- **Döngüsüzlük** TTL'ye değil, hedefin ürettiği sıra numarasına ve uygulanabilirlik mesafesine dayanır (Babel, RFC 8966 ailesinin koşulu).
- **Yönlü bağ maliyeti** kalite ve riskten oluşur; kalite düğümün kendi iletim sonuçlarından ölçülür.
- **Postürler** (STEADY · CAUTION · PROTECT): gözlenen bozunmaya kademeli tepki.
- **Geliştirilmekte olanlar:** karıştırmaya özgü kanıt (RSSI, kanal doluluğu, PHY hataları), yedek ardıl, kanıta dayalı postür, seçici çok yol ve çoğaltma. "Karıştırıcı tespiti" iddiası yoktur; protokol yalnız yerel olarak ölçebildiğine göre davranır.

Bağlayıcı olan bugünkü koddur (v0.4.1). İlk tasarım taslağı (v0.1, 22 Eylül) arşivdedir: [`arsiv/DESPARETE_TASARIM_PAKETI_v0.1_2026-09-22/`](arsiv/DESPARETE_TASARIM_PAKETI_v0.1_2026-09-22).

## Yöntem

- **Ön-kayıt.** Hipotezler, eşiklerin türetme formülleri ve analiz planı sonuç görülmeden yazılır. Ana deney tohumlarıyla (2000–2039) mühürden önce hiçbir protokol koşulmaz ([`v2/06`](v2/06-ON-KAYIT.md)).
- **İstatistik.** Ana deney 40 tohumdur; eşleştirilmiş, çift yönlü Wilcoxon testi ve aile içinde Holm düzeltmesi kullanılır. Sonuçlar etki büyüklüğü ve güven aralığıyla verilir.
- **Metrikler** üçlü sunulur: teslim · gecikme · kontrol yükü. Ayrıca karıştırmaya tepki ölçülür: şok derinliği, toparlanma süresi, tespit gecikmesi.
- **Ablasyon.** Önerilen protokolün mekanizmaları ayrı yapılandırma bayraklarıyla açılıp kapanır; bir kazancın hangi mekanizmadan geldiği ölçülür.
- **Ölçüm disiplini.** Her sayı üretici komutuyla yazılır; sonucu ya da bir kararı etkileyen her ölçümün ölçütü ölçümden önce kayda girer.
- **Kararlar** konu konu [`v2/04-KARARLAR.md`](v2/04-KARARLAR.md), tarihçesi [`v2/kayit/KARAR-GUNLUGU.md`](v2/kayit/KARAR-GUNLUGU.md).

---

## Kurulum ve çalıştırma

Gereksinimler: **Python 3.11**, `numpy`, `scipy`, `pytest` (geliştirme: Python 3.11.8 · numpy 2.4.6 · scipy 1.17.1 · pytest 8.2.2).

```bash
pip install numpy scipy pytest
```

Komutlar depo kökünden çalıştırılır; Windows konsolunda `PYTHONIOENCODING=utf-8` gerekir. Windows'ta birden çok Python kuruluysa `python` yerine `py -3.11` kullanın.

```bash
PYTHONIOENCODING=utf-8 python -m pytest tests2 -q            # test takımı, ~15 dk
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

Senaryo adı `<hareketlilik kolu>-<karıştırıcı sınıfı>` biçimindedir (ör. `formasyon-surekli`). `Konfig()` doğrudan kullanılırsa eski 1:50 ölçekli geliştirme dünyası kurulur; deneyler referans dünyada koşar. Tam uzunlukta (350 s) bir koşunun süresi protokole göre 1–8 saattir ([`v2/12`](v2/12-YOL-HARITASI.md) §3).

---

## Simülasyon ve gerçeklik

Bu çalışma bir kavram kanıtıdır. Kullanılan yayılım ve karıştırma modelleri gerçek RF ortamının basitleştirilmiş temsilleridir. Sonuçlar saha performansı öngörüsü olarak yorumlanmamalıdır; bulgular yalnız modellenen koşullar altında **göreli** karşılaştırma olarak geçerlidir. Gerçek RF, SDR ve uçuş testi kapsam dışıdır.

## Yapay zekâ kullanımı

Proje fikri, kapsam ve gerçekçilik kararları ve DESPARETE'nin tasarımı bana aittir; yapay zekâ araçları danışman ve kod uygulayıcısı olarak kullanılmıştır. Kararlar tarihli olarak kayıtlıdır ([`v2/kayit/KARAR-GUNLUGU.md`](v2/kayit/KARAR-GUNLUGU.md)) ve bir mekanizmanın katkısı ablasyonla ölçülür.

## Lisans

Özgün kaynak kodu ve belgeler [Apache License 2.0](LICENSE) ile lisanslanmıştır — Copyright 2026 Xelma123. [`protokol_kaynaklari/`](protokol_kaynaklari) içindeki üçüncü taraf malzeme (ns-3, Linux ve olsrd2 kaynak dosyaları, RFC metinleri, makaleler) bu lisansın kapsamında değildir; her biri kendi lisansı ve telif hakkıyla dağıtılır ([`NOTICE`](NOTICE)).
