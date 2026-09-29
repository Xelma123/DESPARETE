# 4.1b · Karıştırıcı şiddeti referans dünyada (35 km) — beklenti (ölçmeden önce)

> 26 Eylül 2026 · ajan · komutlar (dondurulmuş kopyadan):
> - `python kalibrasyon/karistirici_gucu.py --dunya referans_2026 tarama`
> - ardından `aile` ve `mesafe`

## İlke (öğrenci: "en mantıklı ve gerçekçi olana önem ver")

- **Güç kaynaktan gelir** (`v2/14` §4): İHA taşıyıcılı 1–5 W (30–37 dBm), taşınabilir 10 W (40), araç 50 W (47). Birincil hücrenin ailesi `hava_eslik`, yani İHA taşıyıcılı; güç bu bandın içinden seçilir.
- **Ağın bölünmemesi koşul olarak kalır.** Bu yalnız onaylı bir ölçüt değil, bilimsel geçerlilik şartıdır: bölünmüş bir ağda ölçülen şey yönlendirme değil bölünme olur (`karistirici_gucu` başlığı).
- **Seçim kuralı:** kaynak bandında ağı bölmeyen en güçlü değer. Bant dışı güçler (40–47 dBm) rejimin sınırını gösteren keşifsel eksen olur (H1.2 dirseği).

## Analitik tahmin

Merkezde tek karıştırıcı, sürekli; 1 Mb/s bağlarda işlem kazancı 13,4 dB.

**ED susturma yarıçapı** (−76 dBm):

| güç | 30 dBm | 37 dBm | 40 dBm | 47 dBm |
|---|---|---|---|---|
| yarıçap | ~2,5 km | ~5,6 km | ~7,9 km | ~17,7 km |

**Alıcı SINR'ı:** eşik ~8 dB Eb/N0, yani SIR ≥ −5 dB. Karıştırıcı 20 dBm'lik düğümden 10 dB güçlüyse, uzunluğu r olan bağ alıcısı karıştırıcıya ~1,8·r'den yakınsa kesilir.
- Bağlar uzun (5–9 km) olduğu için, 1 W bile merkezden ~10–15 km içindeki uzun bağları keser.
- Kısa bağlar ayakta kalır.

## Öngörü

| güç | ρ | ayrılan tohum |
|---|---|---|
| 30 dBm (1 W) | **0,25–0,50** | 0/30 |
| 37 dBm (5 W) | **0,45–0,65** | 0–3/30 |
| ≥ 40 dBm | ≥ 0,6 | ≥ 1/30 |

- **Seçilecek:** 33 ya da 37 dBm (kaynak bandının içi).
- Yanlışlanırsa, yani 30 dBm'de ayrılma varsa: güç bandın altına inmez, karıştırıcı `mesafe` bölümüyle merkezden uzaklaştırılır ("rejim konumdan").

## Sonuç (35 km, `b_karistirici_tarama.txt`) — YANLIŞLANDI

| güç | ρ | ulaşılabilirlik | ayrılan |
|---|---|---|---|
| 20 dBm | 0,257 | 0,987 | 4/30 |
| 25 dBm | 0,448 | 0,919 | 19/30 |
| **30 dBm (1 W)** | **0,666** | 0,472 | **30/30** |
| 37 dBm (5 W) | 0,881 | 0,080 | 30/30 |

- Öngörüm "1 W'ta ρ 0,25–0,50, bölünme yok" idi; ✗.
- **Neden:** 35 km, bağlılığın kenarındaki alan (yedeksiz). Uzun bağlar SINR'a çok duyarlı ve merkezdeki karıştırıcı ağı ikiye ayırıyor.

## Ek beklenti — alan × güç ortak taraması (`b_alan_guc.py`, ölçmeden önce yazıldı)

- **1 W:** 10 km'de ρ ≈ 0,2–0,4, bölünme yok · 15 km'de ρ ≈ 0,3–0,5, 0–2/30 · 20 km'den itibaren bölünme.
- **Seçilecek alan (1 W'ta bölünmeyen en büyük): 15–20 km.**
- **5 W:** bölünmeyen alan ≤ 10 km.

## Alan × güç ara sonucu (`b_alan_guc.txt`, ilk iki alan)

1 W'lık merkez karıştırıcı 10 km'de 15/30, 15 km'de 25/30 tohumda ağı bölüyor. "15–20 km'de bölünmeyen alan" öngörüsü ✗. Merkezdeki kaynaklı güçteki bir karıştırıcı hangi alanda olursa olsun ağı bölüyor.

## Ek beklenti — 35 km'de mesafe ve aileler (`b_karistirici_mesafe_aile.txt`, ölçmeden önce)

- **Mesafe (1 W, merkezden doğuya):** merkez ve 0,5 × yarım kenar bölünür. İlk geçen oran **0,75–1,25** (kenar civarı); orada ρ ≈ 0,1–0,3.
- **Aileler (toplam ortalama güç 1 W):**
  - `cephe_hatti` (3 yer karıştırıcısı doğu kenarında, yer–hava kaybıyla) **geçer**, ρ ≈ 0,05–0,25;
  - `hedef_koruma` (x = 0,75) 0–5/30;
  - `tekli_merkez` 30/30;
  - `hava_eslik` (merkezden geçen hava platformu) ve `derin_sizma` (merkezden başlayan araç): çoğu tohumda bölünür.

## Sonuç (35 km, 1 W, `b_karistirici_mesafe_aile.txt`) ve yeni ölçü

- **Mesafe:** kenarın 8,75 km dışında bile 13/30 bölünme. "İlk geçen oran 0,75–1,25" öngörüsü ✗.
- **Aileler:**
  - hava karıştırıcıları (`tekli_merkez` ρ 0,666 · `hava_eslik` ρ 0,661, ulaşılabilirlik ~0,46) 30/30;
  - yer aileleri (yer–hava kaybıyla) ρ 0,055–0,10, ulaşılabilirlik 0,97–0,99, ama 15–19/30 "ayrılma" — kenardan kopan küçük gruplar.
  - `cephe_hatti` "geçer" öngörüsü ✗, eski tanımla.

## Ek beklenti — aile × güç, büyük bölünmeyle (`b_aile_guc.py`, ölçmeden önce)

- **Büyük bölünme:** ikinci bileşen ≥ 4 İHA, yani bir müfreze.
- **Yer aileleri** (`cephe_hatti`, `hedef_koruma`, `derin_sizma`): 40 dBm'e kadar büyük bölünme 0–3/30; ilk büyük bölünmeler 44–47 dBm'de.
- **Hava** (`tekli_merkez`, `hava_eslik`): büyük bölünme 20–25 dBm'de başlar; 30 dBm'de ≥ 25/30.

## 🔴 Ölçü kusuru (ajan, K-186'da düzeltildi)

- İlk aile × güç koşusunda (`b_aile_guc_bfs_hatali.txt`) en kötü anın en büyük bileşeni %97,5 iken "ikinci bileşen ≥ %10" okundu. Bu imkânsız.
- **Neden:** referans dünyada kâhin grafiği YÖNLÜ; ED susturmasında susan düğümün yalnız gelen bağı var. `kahin.ozet` ise bileşenleri "ziyaret edilmemiş kaynaktan erişilen küme" diye sayıyordu. Yönlü grafikte bu kümeler üst üste biner.
- Eski dünyada grafik simetrik olduğundan sorun yoktu. Referansta eski `AYRILAN` sütunu da bu yüzden güvenilmez; 35 km'deki "yer aileleri 15–19/30 ayrılma" okuması da bundan etkilenmiş olabilir.
- **Düzeltme:** güçlü bağlı bileşenler (`gb_en_buyuk`, `gb_ikinci`). Büyük bölünme = ikinci güçlü bileşen ≥ 4 İHA. Beklenti değişmedi.

## Sonuç — aile × güç, güçlü bileşenlerle (`b_aile_guc.txt`)

| öngörü | ölçülen | |
|---|---|---|
| yer aileleri 40 dBm'e kadar büyük bölünme 0–3/30 | cephe 1/30 · hedef 5/30 · derin 2/30 (40 dBm) | ✓ (hedef_koruma sınırda ✗) |
| ilk büyük bölünmeler 44–47 dBm | cephe 3–5 · derin 15–28 · hedef 7–22 | ✓ |
| hava: büyük bölünme 20–25 dBm'de başlar | tekli 25 dBm 3/30 · hava_eslik 20 dBm 1/30, 25 dBm 10/30 | ✓ |
| hava: 30 dBm'de ≥ 25/30 | tekli 26/30 · hava_eslik 30/30 | ✓ |

- ⚠️ Çok yüksek güçte (44–47 dBm) havada "büyük bölünme" sayısı 0'a düşüyor, çünkü sürü tek tek düğümlere dağılıyor (en büyük bileşen %2,5). Bu bölünmemek değil, karartmadır. Büyük bölünme tek başına ölçüt olamaz; en büyük bileşen yanında okunur.
- **Karar:** K-186 (öğrenci): `derin_sizma` 10 W.
