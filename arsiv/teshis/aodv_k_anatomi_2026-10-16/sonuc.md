# AODV-k'nin U1 düşük hücreleri — kayıp anatomisi · sonuç

> 16 Ekim 2026 · ölçüt `beklenti.md` (commit `ec2cbe7`, koşudan önce) · kopya `1163f81` · koşu 12:53–15:39, 2 sa 46 dk (beklenti ~1–1,5 sa; statik 33 dk, hareketli koşular anatomi kaydıyla tek başına 2,2–2,8 sa) · çıktılar `anatomi_{statik,bagimsiz,gorev}.{txt,json}` · `zaman.txt` · `hukum.txt`

## 1 · Ölçütler

| ölçüt | sonuç |
|---|---|
| 1 · Kimlik: yedi PDR U1'le 4 basamak aynı, korunum geçerli | tuttu (0,8441 · 0,8445 · 0,8079 · 0,3900 · 0,4802 · 0,4451 · 0,5172; üç kolda `geçerli True`) |
| 2 · Kusur izi: TTL düşüşü her hücrede üretilenin < %1'i | tuttu: statik 0 · 0 · 0, bağımsız 1 · 0, görev 1 · 1 paket (%0,0) |

Anatomi aletinin "PDR" alanı U1'in değeridir. "Pencere PDR"ı ayrı bir okumadır, karşılaştırmaya girmez.

## 2 · Mekanizma (betimleyici, sıralama iddiası yok)

Düşen/üretilen oranları ve bağ bantları:

| kol | tohum | en büyük düşüş | ikinci | karar bağı, yeniden denemeli iyi | karar bağı, tek deneme iyi | başarısız bağ iyi |
|---|---|---|---|---|---|---|
| statik | 1000 | `iletim_basarisiz` %8,6 | `rota_gecersiz` %6,9 | %99 | %91 | %66 |
| statik | 1001 | `iletim_basarisiz` %9,4 | `rota_gecersiz` %6,2 | %99 | %92 | %71 |
| statik | 1002 | `iletim_basarisiz` %9,9 | `rota_gecersiz` %9,4 | %99 | %94 | %70 |
| bağımsız | 1000 | `rota_gecersiz` %39,3 | `iletim_basarisiz` %21,2 | %98 | %71 | %78 |
| bağımsız | 1002 | `rota_gecersiz` %30,0 | `iletim_basarisiz` %21,9 | %98 | %67 | %76 |
| görev | 1000 | `rota_gecersiz` %31,4 | `iletim_basarisiz` %23,9 | %98 | %70 | %82 |
| görev | 1001 | `rota_gecersiz` %25,9 | `iletim_basarisiz` %22,3 | %98 | %68 | %78 |

- **Bölge:** bütün düşüşler "uzak" bölgede; kollar karıştırıcısız.
- **`hedef_yok` ve kuyruk taşması:** `hedef_yok` en çok %0,5. Kuyruk taşması hiçbir hücrede yok.
- **Statik:** düşüşün büyüğü iletim başarısızlığı. Başarısız bağların %12–15'i kâhine göre kötü bant; K-224'teki OLSR'da bu oran %1–2'ydi.
  - Bunun nedeni atlama sayısıyla seçilen yollar: AODV'nin metriği bağ kalitesini görmez. Karar bağı mesafesinin medyanı 8,2–8,8 km, OLSR'da 6,6–7,5 km.
  - Karar bağlarının %99'u yeniden denemeli bantta yine iyi: başarısız iletimler seçilen bağların küçük bir kısmında toplanıyor.
- **Hareketli kollar:** en büyük düşüş `rota_gecersiz` (%26–39). Kopan rotalar keşifle yeniden kurulana kadar paket kaybediliyor. Tek deneme bandında karar bağlarının %67–71'i iyi; AODV'nin yayın düzlemi (RREQ, HELLO) hareketlide kayıplı.

Öngörü tuttu: statikte en büyük düşüş `iletim_basarisiz`, hareketlide `rota_gecersiz`.

## 3 · Kayıt ve yeniden hüküm

`kalibrasyon/aodv_uygunluk.py`'de iki kayıt güncellendi:

- **`ACIKLANMIS_DUSUK_REFERANS["aodv"]`:** yedi hücre. Gerekçeleri:
  - K-207 atfı;
  - sadakat denetimi (42 kural, K-244);
  - A/B sonucu;
  - bu anatomi; her hücrenin metnine oranı ve iki büyük düşüş sebebi yazıldı.
  - AODV-j'nin üç hücrelik kaydının yerini aldı.
- **`KAYITLI_ORAN["aodv"]`:** yedi hücrenin AODV-k oranı. Eşler arası kayıt (AODV-j, 1,0002) U1 eşler arası bitince yargılanır.

Yeniden hüküm `hukum` kipiyle, AODV-k'nin U1 kaydı üzerinden yapıldı (`ciktilar2/aodv_uygunluk/aodv_referans_2026_yere_toplama_20261015_150734.json`):

**U1-U GEÇTİ · U1-B TEMİZ** (çıkış 0, `hukum.txt`). Yedi düşük hücre "açıklanmış" sayılır; bulgu olarak raporlanır, kusur değildir.

Doğrulama:

- `tests2/test_aodv.py`: 53 geçti.
- Mimari denetimi: ihlal 0.
- Babel'in hükmü değişmedi: GEÇTİ · TEMİZ.
