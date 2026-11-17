# KK-05 · Bekletme ve komutun yolu

> Kararlar: T-18 · T-20 (`17`). Değerler `KK-00`. Güncel: 17 Kasım 2026.

## Amaç ve sınıf

Yol yokken paketi açlık çözülene kadar kısa süre tutmak; komutu telemetrinin geldiği yolun tersinden götürmek. **Genel** (bayrak `bekletme`).

## Gördüğü ve tuttuğu

- Karar anında paketin başlığı (`05` §3.3): kaynak, hedef, `kaynak_sira`.
- Bana gelen telemetri çerçevesinin göndereni (`cerceve_duyuldu`).
- `ilk_bekletme`: paket kimliği `(kaynak, kaynak_sira)` → bu düğümde ilk bekletildiği an.
- `iz`: kaynak → (komşu, son görülme anı).

## Kurallar

**A · Bekletme:**
1. Paket için yol yoksa (KK-04'te `A` boş) karar `beklet` olur; paketin ilk bekletme anı tutulur.
2. Yeniden sorulduğunda: yol varsa gönderilir; yoksa ve bu düğümde `TUTMA_EN_COK` geçtiyse düşer (`rota_gecersiz`); değilse yine beklenir.
3. Yeniden sorma: yol bulunduğunda hemen, tamponda bekleyen paket varken her 0,5 s'de bir `Uyandirma` döndürülür (simülatör tamponu yalnız uyanmadan sonra döker, K-135).
4. Sayı tavanı simülatörün ortak tavanıdır (`rota_tamponu_kapasitesi` 64; dolunca en eski düşer); her protokole aynı. Asıl sınır süredir.
5. Paketin yaşı görünmediği için sınır atlama başınadır; uçtan uca 5 s'yi aşan gecikme gecikme tavanlı `PDR_açık`la ölçülür (T-19).

**B · Komutun yolu:**
6. Geçide giden bir telemetri çerçevesi bana gelince `iz[kaynak] ← (gönderen, şimdi)`.
7. Komut kararı: `iz[hedef]` var, `IZ_TAZELIK` içinde ve o komşu OLAĞAN ise `sonraki = komşu`; değilse komut bekletilir (kural 1–3). Hedefin bir sonraki telemetrisi izi tazeler.
8. İz KARIŞTIRILIYOR ya da KÖTÜ bir komşuyu gösteriyorsa bayattır (`17` §7 madde 5).
9. Komutla telemetri aynı tamponu paylaşır, öncelik yoktur: simülatör tamponu sırayla döker. Komutların birincil metrikteki yeri açık karardır (KR-2).

## Örnek

Ardılı karıştırılan ve yedeği olmayan bir düğüme 0,3 s içinde iki telemetri gelir; ikisi bekletilir, tur isteği gider. 0,6 s sonra yeni tur gelir, yol açılır, uyanma tamponu döker ve iki paket gider. Yanıt 2 s'de gelmeseydi paketler düşerdi. Geçitten bu düğümün altındaki bir İHA'ya giden komut, o İHA'nın son telemetrisini getiren komşuya verilir; o komşu karıştırılıyorsa komut, bir sonraki telemetriyle tazelenen izi bekler.

## Sınanması

- `bekletme` açık ↔ kapalı: birincil hücrede rota yokluğu kaybı (R) ve gecikme tavanlı `PDR_açık`; ikizde fark yok.
- Komut teslimi ayrı sayılır: izli · izsiz-bekletilip-giden · düşen.

## Kaynak

Bekletme v0.4.1'de de vardı (alan başına 6 paket, 6 s); geri iz v0.4.1'in V11'i (K-172); en eskiyi düşürme simülatörün ortak kuralı.
