# C · Senaryo eksenleri — beklenti (ölçmeden önce)

> 26 Eylül 2026 · `v2/15` C1 (düğüm kaybı) · C2 (trafik ekseni tedavide) · C3 (telsiz enerjisi) · ajan

## Neyi değiştirdi

- **C1 · Düğüm kaybı.** Geçit dışındaki `kayip_dugum_sayisi` İHA'nın telsizi `[kayip_bas_s, kayip_bitis_s]` içinde, hash'ten seçilen bir anda kapanır.
  - Kuyruk, rota tamponu ve el değiştirmemiş uçuştaki paket `dugum_kaybi` sebebiyle düşer.
  - Onay beklerken ölen deneme `mac_kayip_askida` kovasına girer.
  - Ölü düğüm üretmez, duymaz, göndermez. Protokole haber verilmez.
- **C2 · Trafik ekseni.** Üç trafik hızı ve kayıp alanları `TEDAVI_ALANLARI`na girdi. Artık kurulum hash'ine değil, tedavi hash'ine sayılıyorlar.
- **C3 · Enerji.** Gönderim 10,6 W, alım ve dinleme 2,0 W (G7).
  - Düğüm başına enerji = P_tx·t_tx + P_rx·(ömür − t_tx); ömür = ölüm anı ya da koşu sonu.
  - Satıra giren metrikler: `metrikler.enerji_toplam_j`, düğüm p50/p95/maks.
  - Korunum bölümüne giren alanlar: süre değişmezi (`enerji_sure_tamam`) ve toplam süreler.

## Tam takım

- 882 + 3 = **885 passed** bekleniyor.

## Regresyon `k179 ↔ k180` (65 eski vaka + 2 yeni `t-`)

**Eski vakalar birebir.** Kayıp kapalıyken (varsayılan 0) hiçbir olay eklenmiyor; enerji yalnız süre sayıyor, davranışı değiştirmiyor.

İzinli farklar (hepsi yeni alan ya da kimlik):

- `kimlik.kurulum_hash` — yeni konfig alanları; trafik hızları kurulumdan tedaviye geçti.
- `kimlik.tedavi_hash` — tedavi alanları genişledi.
- `konfig.kayip_dugum_sayisi`, `konfig.kayip_bas_s`, `konfig.kayip_bitis_s`, `konfig.enerji_gonderim_w`, `konfig.enerji_alim_w`.
- `korunum.enerji_*` (4 alan), `metrikler.enerji_*` (4 alan).
- `teshis.koken_kovalari` — beş yeni köken kaydı.

`--sifir` (var ve sıfır olmalı): `korunum.dusen.dugum_kaybi`, `metrikler.dugum_kaybi_dusen*`, `metrikler.mac_kayip_askida*`.

**Enerji değerleri (yeni alan, sayı önceden):**

- Kısa vaka: 40 düğüm × 50 s × 2,0 W = 4 000 J taban; gönderim eki 8,6 W × toplam gönderim süresi.
  - `enerji_toplam_j` ∈ [4 000, 4 400] J.
  - `enerji_dugum_p50_j` ∈ [100, 110] J.
- Tam vaka (350 s): `enerji_toplam_j` ∈ [28 000, 30 000] J.
- `korunum.enerji_sure_tamam` her satırda `True`; `gecerli` değişmez.

**Yeni `t-` vakaları** (tohum ikizle aynı, fark yalnız 5 ölüm):

| vaka | ikiz | ikizin PDR'si |
|---|---|---|
| `t-bagimsiz-surekli-dogrudan_komsu-dugum_kaybi` | `m-bagimsiz-surekli-dogrudan_komsu` | 0,4593 · üretilen 1598 |
| `t-statik-surekli-aodv-dugum_kaybi` | `k-statik-surekli-aodv` | 0,6937 · üretilen 1600 |

Her ikisi için beklenti:

1. `gecerli=True` (korunum + mutabakat + enerji süresi).
2. `korunum.dusen.dugum_kaybi` = `metrikler.dugum_kaybi_dusen`.
   - AODV'de > 0 (kuyruk ve rota tamponu dolu olan düğümler var).
   - Tek atlamada ≥ 0.
3. `mac_kayip_askida` ∈ [0, 5]: ölüm başına en çok bir deneme.
4. Üretilen **ikizden az**, düşüş en çok %15. Ölü kaynak üretmez; 5/40 düğüm, ortalama 25 s erken susuyor → ~%6 civarı.
5. PDR **ikizden düşük**.
   - Ölü hedefe giden paket yeniden deneme hakkını tüketip düşer (tek atlama).
   - AODV'de ölü röle rotayı kırar.
6. `enerji_toplam_j`, ikizinkinden ~250 J (150–350 J) az: 5 düğüm × 2 W × ortalama 25 s.

## Yanlışlanırsa

Eski bir vakada izin dışı fark çıkarsa kayıp kapalıyken bir olay ya da çekim sızıyor demektir. Bu durumda bulgu kök nedenine kadar izlenir, taban değişmez.
