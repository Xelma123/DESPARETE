# OLSR referans dünya teşhisi — 1. tur sonucu (ölçümden SONRA)

> 28 Eylül 2026 · ajan · beklenti `beklenti.md` · çıktı `tam.txt`, ham `tam.json` · 1028 s (6 iş, dondurulmuş kopya `arac_hash` e9b27fe1…)

| öngörü | sonuç |
|---|---|
| 1 kimlik 0,5912 · 0,7953 · 0,5186 | ✓ birebir |
| 2 `rota_gecersiz` düşüşlerin ≥ %50'si | ✓ 1000 (%71) · ✗ 1001 (%45) · ✓ 1002 (%68) |
| 2 `iletim_basarisiz` ≤ %25 | ✓ %13 · ✗ %28 · ✓ %14 |
| 2 `hedef_yok` yalnız ısınmada | ✓ (3 tohumda ~5'er tane dışında) |
| 2 `ttl` ≤ düşüşlerin %5'i | ✗ %10 · %14 · %13 — geçici döngüler beklenenden fazla |
| 3 sıra 1002 > 1000 > 1001 | ✓ |
| 4 karar bağı ≥ %95 iyi · başarısız bağ çoğu iyi | ✓ %100 · %92–98 |
| 5 §13 ≥ %90 geri alınır, medyan < 1 s | ✓ %99,7 · 0,32–0,57 s |
| 6 §13'süz |Δ| ≤ 0,05 | kısmen: +0,031 · +0,028 · **+0,105** (üçü de §13'süz lehine) |
| 7 komşu kaybı 4 000–10 000, sırası düşüş sırasıyla aynı | sayı ✓ (9 475 · 11 503 · 9 932); **sıra ✗** (en çok 1001'de) |
| 8 bayat rota ihlali 0 | ✓ 0 / 175 141 karar |

**Okuma:** H1 (zayıf bağ seçimi) düştü; H4 düştü; H2 (geçide rota tablosunun aralıklı boşalması) baskın; H3 (döngü) ikincil ama belirgin. §13 referans dünyada OLSR'a ZARAR veriyor (K-147'nin eski dünya statik kazancının tersi; eski dünyada da hareketli kollarda zararlıydı). Çalkantının MİKTARI hücreleri sıralamıyor → açıklama henüz "sıralayan mekanizma" değil (K-192 koşulu). Sıradaki: rota boşaldığı anda düğümün kendi bilgisinde yol var mı (RFC §10'un 2-atlama kümesine dayanması ve §8.5 silmesi), düşüşler hangi düğümlerde.
