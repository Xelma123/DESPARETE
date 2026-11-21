# KK-05 · Bekletme ve komutun yolu

> Kararlar: T-18 · T-20 (`17`). Değerler ve genel kurallar `KK-00`. Kod `protokoller/desparete5_bekletme.py`. Güncel: 20 Kasım 2026 (kural 1: KK-04 kural 13'ün bekletmesi; kural 14'ün kopması zaten "ardıl yok"tur). Önceki: 19 Kasım (`v2/arsiv/kural/KK-05-BEKLETME-KOMUT-2026-11-19.md`: `17` T-12, T-13, T-18) · 18 Kasım (`v2/arsiv/kural/KK-05-BEKLETME-KOMUT-2026-11-18.md`; G-1).
>
> **Kod:** 19 Kasım'da bu kâğıda göre yazıldı; kural 1'in KK-04 kural 13'ten gelen bekletmesi 20 Kasım'da (`desparete5.py` `sonraki_atlama`). 18 Kasım'ın davranışı `egim` · `vazgecme_tetigi` · `duzgun_gecis` kapalı, `veri_kotu_tetigi` açık ve `DEGERLER_ESKI`yle birebir yeniden üretilir (küçük test dünyasında sekiz koşuda denetlendi: `arsiv/teshis/faz5_3_kod_2026-11-19/esdegerlik.txt`).

## Amaç ve sınıf

Yol yokken (KK-04'te hiç aday kalmayınca) paketi kısa süre tutmak; komutu telemetrinin geldiği yolun tersinden götürmek. Bekletme **genel** (`bekletme`); geri iz **genel**, çekirdek (T-20).

## Gördüğü ve tuttuğu

- Karar anında paketin başlığı (`05` §3.3): kaynak, hedef, `kaynak_sira`.
- Bana gelen telemetri çerçevesinin göndereni (`cerceve_duyuldu`).
- `ilk_bekletme`: paket kimliği `(kaynak, kaynak_sira)` → bu düğümde ilk bekletildiği an.
- `iz`: kaynak → (komşu, `kaynak_sira`, son görülme anı).

## Kurallar

**A · Bekletme**

1. Paket için yol yoksa (KK-04'te `A` boş, ardıl yok; ya da ardıl paketi getiren komşu ve yokuş aşağı başka aday yok, KK-04 kural 13) karar `beklet` olur; paketin ilk bekletme anı tutulur. Bayrak kapalıyken paket düşer (`rota_gecersiz`).
2. Yeniden sorulduğunda: yol varsa gönderilir; yoksa ve bu düğümde `TUTMA_EN_COK` geçtiyse düşer (`rota_gecersiz`); değilse yine beklenir.
3. Yeniden sorma: yol bulunduğunda bir sonraki niyetli kancada, tamponda bekleyen paket varken her 0,5 s'de bir `Uyandirma` döndürülür (simülatör tamponu yalnız uyanmadan sonra döker, K-135; niyet döndüremeyen kancalar için `KK-00` genel kural 1).
4. `ilk_bekletme` kaydı `TUTMA_EN_COK + 1 s`'den yaşlıysa silinir: simülatörün sayı tavanıyla (`tampon_asimi`) düşen paketlerin kaydı kalmaz, gereksiz uyanma üretmez.
5. **Sınırın türü** (T-18'in 5-3'e kalanı): atlama başına süre sınırı. Paket başına tutulma sayısı sınırı ve başlıkta birikmiş bekleme alınmadı: ikincisi gözlem sözleşmesine (`05` §7) yeni bir başlık alanı ister. Sayı tavanı simülatörün ortak tavanıdır (`rota_tamponu_kapasitesi` 64; dolunca en eski düşer); her protokole aynı. Paketin yaşı görünmediği için uçtan uca 5 s'yi aşan gecikme gecikme tavanlı `PDR_açık`la ölçülür (T-19).

**B · Komutun yolu**

6. Geçide giden bir telemetri çerçevesi bana gelince (`cerceve_duyuldu`, hedefi ben) `iz[kaynak] ← (gönderen, kaynak_sira, şimdi)`, yalnız paketin `kaynak_sira`sı izdekinden büyükse. Sebep: izden ize ilerleyen her adımda sıra azalmaz; çapraz giden iki paket iki düğümü birbirine gösteremez, komut döngüye giremez. Döngü ancak aynı paketin yolunda olabilir, o yol da döngüsüzdür (v0.4.1'in V11 kuralı; 18 Kasım, kodlamada G-1). Bu kanca niyet döndüremez; iz tazelenince bekleyen komut bir sonraki uyanmada (en geç 0,5 s) gider.
7. Komut kararı: `iz[hedef]` var, `IZ_TAZELIK` içinde ve o komşu OLAĞAN ise `sonraki = komşu`; değilse komut bekletilir (kural 1–4). Hedefin bir sonraki telemetrisi izi tazeler.
8. İz KÖTÜ ya da KARIŞTIRILIYOR bir komşuyu gösteriyorsa bayattır (`17` §7 madde 5). "Veriye uygun değil" işaretli komşuyu gösteren iz bayat sayılmaz: komutun tek yolu odur, telemetri o yoldan gelmiştir.
9. Komutla telemetri aynı tamponu paylaşır, öncelik yoktur: simülatör tamponu sırayla döker. Komutların birincil metrikteki yeri açık karardır (KR-2).

## Örnek

Bütün komşuları KÖTÜ, karıştırılıyor ya da ∞ ilanlı olan bir düğüme (KK-04'te hiç aday yok) 0,3 s içinde iki telemetri gelir; ikisi bekletilir. 0,6 s sonra bir komşunun bağı OLAĞAN'a döner, yol açılır, bir sonraki uyanmada (1 ms) tampon dökülür ve iki paket gider. Yol `TUTMA_EN_COK` içinde açılmasaydı paketler düşerdi. Geçitten bu düğümün altındaki bir İHA'ya giden komut, o İHA'nın son telemetrisini getiren komşuya verilir; o komşu karıştırılıyorsa komut, bir sonraki telemetriyle tazelenen izi bekler.

## Sınanması

- `bekletme` açık ↔ kapalı: birincil hücrede rota yokluğu kaybı (R) ve gecikme tavanlı `PDR_açık`; ikizde zarar yok.
- Tanı: komut teslimi ayrı sayılır (izli · izsiz bekletilip giden · düşen); yol yok bölümlerinin sayısı ve süresi (KK-04).

## Kaynak

Bekletme v0.4.1'de de vardı (alan başına 6 paket, 6 s); geri iz v0.4.1'in V11'i (K-172); en eskiyi düşürme simülatörün ortak kuralı.
