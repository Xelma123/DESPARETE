# A8 · Referans dünyada bütün anahtarlar — beklenti (ölçmeden önce)

> 26 Eylül 2026 · `v2/15` A8 · ajan · C (K-180) tamamlandıktan sonra uygulanır

## Neyi değiştirir

1. **`referans_2026()` Faz 1'in bütün anahtarlarını açar:**
   - işlem kazancı — zaten açıktı;
   - güç kipi taşıyıcı dinleme ve ED-CCA (A3);
   - ARF (A4);
   - yayılım gecikmesi (A5);
   - karıştırıcı gerçekçiliği (A6).

   `Konfig` varsayılanları eski dünyada kalır.
2. **Kapsam beyanı düzeltmesi (ajan hatası).** A2–A5 dört sınırı anahtarın arkasında modelledi, ama `kapsam.MODELLENMEYEN` güncellenmedi.
   - Anahtarı açık satırlar bu yüzden "hız uyarlaması yok", "yayılma kazancı yok" gibi yanlış beyan taşıyordu. Modülün kendi uyarısı tam da bunu söylüyordu.
   - Düzeltme: anahtarlı dört sınır satırın kendi konfiginden okunur.

## Analitik girdi (koşu değil)

Komut: `python arsiv/teshis/a8_referans_anahtarlar_2026-09-26/ed_payi.py` → `ed_payi.txt`

Merkezdeki 1 W karıştırıcının sürüde bıraktığı güç:
- `statik-surekli`: 16/40 düğüm ED eşiğinin (−76 dBm) üstünde.
- `bagimsiz-surekli`: 6–15/40 düğüm.
- Ortanca güç ≈ −77 dBm, yani tam eşikte.

Bu düğümler güç kipinde karıştırıcı açık kaldıkça susar. Sonuç ED eşiğine ve karıştırıcı gücüne çok duyarlı; bu Faz 4.1'in girdisidir.

## Tam takım

- C'nin (K-180) son sayısı + 2 = **889 passed** bekleniyor (C: 887).

## Regresyon `k180 ↔ k181`

**Eski (`r-` dışı) vakalar birebir.** Tek istisna `kapsam.modellenmeyen`; yalnız anahtarı açık 9 vakada, yalnız o anahtarın sınırı düşer:

| vaka | düşen sınır |
|---|---|
| `l-…-islem_kazanci` | `yayilma_kazanci` |
| `n-…-tasiyici_guc` · `n-…-tasiyici_guc-hava_eslik` | `enerji_sezmeli_cca` |
| `o-…-yayilim_gecikmesi` | `yayilim_gecikmesi` |
| `o-…-tasiyici_guc-yayilim_gecikmesi` | `enerji_sezmeli_cca`, `yayilim_gecikmesi` |
| `p-…-tasiyici_guc-karistirici_gercekci` | `enerji_sezmeli_cca` |
| `q-statik-…-islem_kazanci-hiz_uyarlamasi` · `q-bagimsiz-…-kontrol_sinav-islem_kazanci-hiz_uyarlamasi` | `yayilma_kazanci`, `hiz_uyarlamasi` |
| `s-…-doluluk_sinav-tasiyici_guc` | `enerji_sezmeli_cca` |

**`r-` vakaları ilan edilmiş değişen** (`--degisen r-referans-`); üçü de `gecerli=True`.

1. **`r-referans-statik-yok-dogrudan_komsu`** (A7'de PDR 0,8836)
   - PDR ∈ [0,80; 0,95].
   - `korunum.enerji_gonderim_s` k180'dekinden az: ARF iyi bağlarda 2 Mb/s'nin üstüne çıkar, çerçeveler kısalır.
2. **`r-referans-statik-surekli-aodv`** (0,2128) · **`r-referans-bagimsiz-surekli-dogrudan_komsu`** (0,1877)
   - Susan düğümlerin paketleri gönderilemez.
   - `korunum.kuyrukta` (koşu sonu) k180'dekinden fazla.
   - Susan düğümün beacon'ı da çıkmaz; tek atlamada `hedef_yok` artar.
   - `korunum.enerji_gonderim_s` azalır.
   - **Birincil hipotez:** PDR ikisinde de A7 değerinin altına iner.
   - **Karşı etkiler:** 1 Mb/s'ye inen ARF +3 dB Eb/N0 kazandırır; karıştırıcının sönümlemesi fırsat pencereleri açar.
   - PDR yükselirse baskın anahtar tek anahtarlı eski dünya vakalarıyla ayrılır ve rapor edilir; taban yine de değişir, çünkü bu ilan edilmiş bir dünya değişikliğidir.

## Yanlışlanırsa

- `r-` dışı bir vakada `kapsam` dışında bir fark çıkarsa, anahtar varsayılanı sızıyor demektir. Bulgu kök nedenine kadar izlenir.
- `r-` vakası geçersiz çıkarsa, anahtarların birleşimi daha önce hiç birlikte koşmamış demektir. Tek tek açılarak ayrılır.
