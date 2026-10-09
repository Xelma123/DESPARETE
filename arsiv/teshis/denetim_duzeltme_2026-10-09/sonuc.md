# Denetim düzeltmeleri (K-223) — sonuçlar

> Ölçütler `beklenti.md` (commit `90b400e`, koşudan önce) · kod `4fbc5fd` (kopya `kopya_a`, 138 dosya commit'le birebir, `kopya_a_ozet.txt`) · saatler `zaman.txt`.

## Kuyruk A (9 Ekim 00:11–02:19)

### A1 · Regresyon k220 → k223 — 🟢 alan karşılaştırması · 🔴 büyüklük kuralı iki satırda

- `karsilastir`: eski dünyanın **63/63** vakası izinli farklar dışında BİREBİR (kod kimliği · `kapsam.rota_tamponu.kaynak` · köken kovaları). İlan edilmiş 17 değişen vakanın hepsi GEÇERLİ; yeni evre vakası GEÇERLİ (`regresyon_k223/karsilastir.txt`). `protokol_hash` 58/63'te değişti — değişmeyen beşi sınav protokolleriyle koşan vakalar (`yuklu` ×2 · `kontrol_sinav` ×3; kodları `tests2/`de, `protokoller/` özetine girmez).
- `denetle.py`: 16 referans vakasında konfig farkı yalnız `yeniden_deneme_siniri` 7 → 6 ✅ · yeni evre vakası: çizelge 15/15, pencere 10–100 s, açılma 40 s, evre alanları dolu, açık + sessiz doğum = 2 400, `ham_denetimi` her alanda birebir (`pdr_acik` 0,7056 · `pdr_sessiz` 0,8734 · `pdr_temiz` 0,8618) ✅.
- **Büyüklük kuralı (|ΔPDR| > 0,10 → U1'den önce teşhis) iki satırda tetiklendi:** `u-birincil-desparete` 0,6928 → 0,5760 (−0,117) · `u-birincil-olsr` 0,3297 → 0,4699 (+0,140). Öteki referans satırlarında |Δ| ≤ 0,063 (AODV −0,042 · AOMDV −0,033 · kâhin −0,024). Teşhis: `teshis_beklenti.md` (ölçüt), sonuç aşağıda.
- **Yeni regresyon tabanı k223** — teşhisin T0'ı geçerse.

### A2 · R — 0,0142 → **0,0126**

`cozunurluk.py --hucre birincil --tohum 40` (69 dk): `olcut_bedeli` ort 0,1347, SD 0,0400 → R = 0,0126; kâhin PDR 0,8675 (ön koşul 0,1–0,95 ✓). Bayatlık kapısı kırmızı (sapma 0,0016 > 0,0005) → `duyarlilik.py::R_ESLESTIRILMIS = 0.0126`, köken kaydı güncellendi.
**R küçüldü** → ön-kayıtlı kural: DUYARSIZ kayıtlarının |Δ|'ları yeni R'yle karşılaştırıldı — en büyüğü `yakalama_esigi_db` 0,0118 (0,94R); ötekiler 0,0068 · 0,0067 · 0,0048 · 0,0042 ve 0. **Hiçbiri SINANMAMIŞ'a dönmedi.** (Bu |Δ|'lar 8 denemeyle ölçülmüştü; tam pencerede yeniden okunmaları zaten Faz 6'da, D-03.)

### A3 · OLSR anatomisi (statik-yok · yere toplama · tam pencere, `OLSR-d`, 7 deneme; 15 dk)

| tohum | PDR (pencere) | en büyük düşüş | karar bağı, yeniden denemeli bant iyi | karar bağı, TEK deneme bandı iyi · orta · kötü |
|---|---|---|---|---|
| 1000 | 0,658 | `rota_gecersiz` %17,4 (iletim_basarisiz %14,3) | %99 | %95 · 3 · 2 |
| 1001 | 0,822 | `iletim_basarisiz` %10,4 (rota_gecersiz %6,5) | %100 | %94 · 5 · 1 |
| 1002 | 0,741 | `iletim_basarisiz` %12,8 (rota_gecersiz %10,0) | %100 | %94 · 5 · 1 |

- **Kural 1 ✅** veri için kötü bağ seçimi değil (yeniden denemeli bantta %99–100 iyi).
- **Kural 2 ✅ güçlü biçim:** tek deneme bandında da %94–95 iyi (≥ %90) → K-193'ün "kötü bağ seçimi DEĞİL" hükmü yayın düzlemi için de ayakta; komşu çalkantısı (koşu başına 8 800–11 000 komşu kaybı) bağ kalitesinden gelmiyor.
- **Kural 3 ✗ — düşüş imzası değişti:** en büyük düşüş artık 3 tohumun 2'sinde `iletim_basarisiz` (toplamda %12,5 · `rota_gecersiz` %11,3; K-193'te %5–7 · %9–33). Başarısız bağların %85–92'si kâhine göre iyi (girişim). → B2'de OLSR'ın düşük hücrelerinin açıklama metni yeniden yazılır (`rota_gecersiz` + iyi bağda iletim başarısızlığı).
- Kural 4 (U1'le kimlik) B2'de denetlenecek.
