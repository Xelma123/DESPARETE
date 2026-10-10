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

## Teşhis — regresyonun iki büyük farkı (9 Ekim 07:30–08:57)

Ölçüt `teshis_beklenti.md` (commit `5b054fb`, koşudan önce) · `teshis_birincil.txt` · 56 koşu, hepsi GEÇERLİ.

- **T0 · kimlik 🟢 GEÇTİ** — 1003'te altı kol regresyon satırlarıyla 16 basamak birebir (PDR ve düşme sebepleri): DESPARETE@7 · AODV@7 · `OLSR-c`@7 = k220; DESPARETE@6 · AODV@6 · `OLSR-d`@6 = k223. **k220 ile k223 arasında beyan edilmemiş davranış farkı yok.** → regresyon tabanı **k223**; kuyruk B başladı.
- **T1 · deneme sayısı** (Δ = PDR(6) − PDR(7), 8 tohum): DESPARETE −0,027 ± 0,028 · AODV −0,039 ± 0,011 · OLSR −0,031 ± 0,038; DESPARETE − AODV +0,012 ± 0,022. Ön-kayıtlı "duyarlı" koşulu (≤ −0,05 ve AODV'den 2 SE aşağı) **sağlanmadı** → 1003'teki −0,117 tek tohumun kısa pencere salınımı (aynı kolda 1004 +0,114, 1007 −0,131). Deneme sayısının etkisi bütün protokollerde küçük ve aynı yönde.
- **T2 · §8.2.1** (`OLSR-d`@7 − `OLSR-c`@7, 8 tohum): +0,026 ± 0,023 (< +0,05) — küçük, K-193'ün statik ölçümüyle (+0,009 · −0,021 · +0,046) uyumlu.
- **T3 · 1003'teki +0,140:** deneme +0,016 · §8.2.1 +0,124 — tek tohumda §8.2.1'in büyük salınımı (8 tohumda −0,044…+0,124).
- **Not (Faz 5 için):** kısa pencerede (30 s) tek tohumun PDR'si ±0,15 oynuyor — regresyonun büyüklük kuralı (0,10) bu pencerede gürültüye yakın; tek tohumlu kısa pencere sayısı hiçbir karara tek başına girmez.
- Tohum ortalamaları (8 tohum, kısa pencere, 6 = yeni): DESPARETE 0,663 · AODV 0,511 · `OLSR-d` 0,432.

## Kuyruk B (9 Ekim 08:57 – 10 Ekim 00:17) · kopya `kopya_b` = commit `5b054fb` (138 dosya birebir)

### B1 · D-07 (birincil hücre, 5 tohum, R 0,0126; 35 dk)

| parametre | ×0,5 | ×2 | hüküm |
|---|---|---|---|
| `gm_hiz_sigma_ms` | 0,7R · band 1,0× | **2,2R · band 2,9×** (pdr_atlama −0,027) | **DUYARLI** — sınırda değil → öğrencinin kararı |
| `gm_alfa` | (α = 0,49: τ 29 s → 0,7 s) | GEÇERSİZ (α = 1,97 ∉ [0, 1)) | **ölçülemedi — aletin tasarım hatası** |

`gm_alfa`: araç α'yı çarpıyordu; korelasyon katsayısı zaman sabitinden oynatılmalı (τ×c ⇔ α^(1/c)). Araç düzeltildi, yeniden ölçüm ek ölçütle (`beklenti_ek.md`). ×0,5 satırı hükme girmez.

### B2 · U1 (yere toplama 6 sa · eşler arası 4 sa 15 dk)

- **U1-U altı kayıtta ✅** (üç protokol × iki desen). Eşler arasında AODV'nin statik 1001 aşımı 0,0002 (< R; kayıt metni yeni sayılarla) · AOMDV'nin eski zarf kaydı ÖLDÜ (0,9814 < 0,9827), silindi.
- **U1-B yere toplamada üç protokolde ✅ TEMİZ** (listeler güncellendikten sonra `hukum`, `u1_kayitlari/hukum_*.txt`):
  - `AODV-j`: düşük hücreler aynı — statik 1000 (0,894) · statik 1002 (0,863) · bağımsız 1000 (0,556) → K-207.
  - `AOMDV-f`: bağımsız 1000 (0,588) + **yeni** statik 1000 (0,899) · statik 1002 (0,891) — eşiğin hemen altı, kod değişmedi → kural 3, K-207 (BULGU).
  - `OLSR-d`: 9 düşük hücre — statik 1000/1001/1002 (0,657 · 0,814 · 0,745) · bağımsız 1000 (0,388) · görev 1000/1001/1002 (0,445 · 0,567 · 0,580) · formasyon 1000/1002 (0,421 · 0,593). **Ölü:** bağımsız 1001 · 1002 (0,628 · 0,610, artık geçiyor). **Yeni:** görev 1002.
- **Kural 4 — OLSR anatomisi** (altı hareketli hücre; `B2_anatomi_*.txt`, 65 dk; PDR'ler U1'le birebir): her hücrede en büyük düşüş `rota_gecersiz` (%28–50; `iletim_basarisiz` %12–16) ve karar bağlarının %100'ü yeniden denemeli bantta iyi → yeni görev 1002 kuralı harfiyen sağlıyor, K-196 atfı. Tek deneme bandında karar bağlarının %75–84'ü iyi (statikte %94–95): hareketli kollarda OLSR'ın kontrol düzlemi seçtiği bağların %16–25'inde kayıplı — RFC'nin onaysız yayını, kusur değil; açıklama metnine girdi. Ölçüt yeni hücre için yazılmıştı; aynı ölçüt `OLSR-c` anatomisine dayanan öteki beş hücreye de uygulandı, hepsi sağlıyor.
- Kural 4'ün kimliği (A3): statik PDR'ler 0,6511 · 0,8037 · 0,7412 U1'le birebir ✅.
- **Eşler arası** (keşifsel): `OLSR-d`nin 9 düşük hücresi açıklanmamış BULGU (K-218'de de 9) — donmayı durdurmaz (kural 6).

### B3 · Evre kapıları (1c 1 sa 43 dk · 2c 2 sa 19 dk · 3c 28 dk)

**G1ç ✅** (boş kolda M1 2 SE dışında 0/4, D dışarıda yok) · **G2ç + G4ç ✅** (kâhin M1 +0,168, D 2 SE içinde; p99 < açık süre) · **G3ç ✅**.
Not (Faz 5.0 için, tam pencere, 1003 · 1004): açık evre PDR'si kâhin 0,734 · 0,827 · AODV 0,401 · 0,536 · AOMDV 0,348 · 0,521 · OLSR 0,258 · 0,193 · DESPARETE v0.4.1 0,476 · 0,538 — v0.4.1'in açık evredeki üstünlüğü AODV'ye +0,075 · +0,002 (D-01'le uyumlu).

### Hüküm

A1 (T0 ile) ✅ · U1-U iki desende ✅ · U1-B yere toplamada ✅ · evre kapıları ✅ → **taban protokoller yeniden DONDU: `AODV-j` · `OLSR-d` · `AOMDV-f`, en çok 7 iletim denemesi** (K-224). Açık: `gm_alfa` yeniden ölçümü · `gm_hiz_sigma_ms` kararı (öğrenci).

## `gm_alfa` yeniden (ek ölçüt `beklenti_ek.md`, commit `5733adb`; kopya `kopya_c`)

- **5 tohum** (10 Ekim 11:13–11:42; τ×0,5 → α 0,9663 · τ×2 → 0,9915): ×0,5 en büyük |Δ| 0,0110 (pdr_atlama; 0,9R, band 0,7×) · ×2 0,0048 (0,4R) → **duyarsız ama sınırda** (≥ 0,7R) → ön-kayıtlı kural: 20 tohum (11:43'ten).
- **Öğrencinin kararı (10 Ekim, K-225):** `gm_hiz_sigma_ms` → **DÜNYA TANIMI** (ölçülen duyarlılığı raporda); `gm_alfa` 20 tohumda DUYARLI çıkarsa aynısı.
