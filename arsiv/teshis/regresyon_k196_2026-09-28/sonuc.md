# Regresyon k186 → k196 · SONUÇ · 🟢 BİREBİR (ilan edilen farklar dışında)

Ajan, 28 Eylül 2026. Beklenti `beklenti.md` (koşudan önce). Çıktılar: `uret.txt` · `tamamla.txt` · `karsilastir.txt` · `degisenler.txt`. Dondurulmuş kopya `arac_hash b6105c67…` (depoyla aynı). Üretim 30,9 dk + eksik 5 vaka ~15 dk, 8 işçi.

## Karşılaştırma
- İlan edilmeyen **52/52 vaka birebir** → sönümleme ağırlık önbelleği bütün matriste bit-özdeş; DESPARETE vakası değişmedi.
- Kaynak koduna bağlı: `arac_hash`, `protokol_hash` (47), çalışma/koşu kimliği, zaman damgası.
- İzinli: `koken_kovalari.TURETILMIS` 62 → 65 (52 vakada) · `sok_derinligi_se` 2 vakada **büyüdü** (0,0138 → 0,0304 · 0,0165 → 0,0226) · `toparlanma_suresi_s` 1 vakada `None` → 90 s (band genişledi). Önceden yazılan yön şartları tuttu.
- İlan edilen 15 değişen vakanın hepsi geçerli.

## Değişen vakalar (hepsi ESKİ dünya · kısa pencere · tek tohum)
| vaka | pencere PDR | not |
|---|---|---|
| `k-statik-surekli-aodv` | 0,705 → **0,837** | kara liste: 41 ekleme, 616 RREQ yok sayıldı |
| `k-statik-surekli-aomdv` | 0,899 → **0,968** | kara liste 34 · 159 |
| `t-statik-surekli-aodv-dugum_kaybi` | 0,794 → **0,852** | kara liste 36 · 559 |
| `r-referans-statik-surekli-aodv` | aynı | kara liste 2 · 1 (sayaçlar değişti) |
| `k-statik-surekli-olsr` | 0,873 → **0,746** | §13 kapalı (k186'da 143 bağ katmanı kopması) |
| kâhin vakaları (10) | −0,11 … +0,01 | K-195 yalnız [5; 10) s'yi değiştirir (açılma 5 s, dilim 10 s — ısınmanın içinde); pencere farkları yörünge sapması. 6'sında ≤ 0,015; `c-gorev-surekli-en_guvenilir_kahin` 0,823 → 0,710 |

## 🔴 Uyarı — §13 kararı karıştırma altında sınanmadı
K-196'nın §13 kararı referans dünyanın **karıştırıcısız** statik kolundan geldi (3 tohum, §13'süz +0,03 · +0,03 · +0,105; K-193). Buradaki tek karıştırıcılı OLSR vakası (eski dünya, kısa, tek tohum) ters yönde: §13'süz **−0,127**. Ana deney karıştırma altında. Tek tohum ve eski dünya → karar için yetmez, ama taban protokolün birincil hücrede zayıflatılmış olma riski gerçek. → birincil hücrede `OLSR-b ↔ OLSR-c` eşli karşılaştırma taban protokoller donmadan önce şart (pahalı; izinle). İyi olan taban olur (daha güçlü taban tutucu seçimdir).

Kara liste aynı vakalarda AODV'yi ve AOMDV'yi belirgin güçlendiriyor — adillik yönünde (K-194'ün gerekçesi: karıştırmada bağ tek yönlü).

## Not
`dondur.py` `tests2/`yi kopyalamıyordu; `yuklu` ve `kontrol_sinav` vakaları (5) `ModuleNotFoundError` verdi. `tests2/` kopyaya eklenip bu 5 vaka aynı işçiyle (`regresyon_satirlari._is`) üretildi, dosyaya eklendi (`tamamla.py`). `dondur.py` artık `tests2/`yi de kopyalıyor.
