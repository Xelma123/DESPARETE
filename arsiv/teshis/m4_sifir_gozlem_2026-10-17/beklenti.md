# M4: temiz evrede sıfır beyan — üst güven sınırı · beklenti (ölçmeden önce)

> 17 Ekim 2026 · yürütücü (*"önerini seçiyorum"*) · tetik: G1-P teşhisi (`arsiv/teshis/g1p_k244_2026-10-17/sonuc.md`). Kural değişikliği sonuçtan sonra (`06` §10'a yazılır). Kod değişikliği ölçmeden önce bu beklentiyle commit'lenir; regresyon ve G1-P yeni donmuş kopyadan koşar.

## Değişiklik (`sim2/olcum/evre.py`, `Evreler.tespit_gecikmesi`)

- **Bugün:** temiz evrede hiç kopma beyanı yoksa M4'ün boş dağılımı Poisson(0) ve eşiği 0. Açılmadan sonraki ilk beyan "tespit" sayılıyor. Hiç beyan etmeyen protokol (`beyan_etmiyor`) ise M4'ün dışında.
- **Yeni:** temiz evrede sıfır beyan varsa kova başına hız 0 alınmaz. Sıfır gözlemle uyumlu tek yanlı (1 − α) üst güven sınırı alınır: `λ = −ln α / n`. Burada n temiz evrenin kova sayısıdır, α modülün tek α'sı (0,05). Boş dağılım Poisson(λ), eşik eskisi gibi α / taranan pencere.
- **Örnek:** G1-P'de n = 100 → λ ≈ 0,030. Eşik 2: bir saniyede en az 3 beyan tespittir.
- **Dokunmadığı yerler:** temizde en az bir beyan olan koşular birebir aynı kalır; `beyan_etmiyor` kuralı ve K-196'nın negatif binomu da değişmez. Yeni sabit yok.
- **Gerekçe:** sonlu bir temiz evrede sıfır sayım "hız 0" demek değildir. Poisson(0) eşiği tek bir beyanı karıştırmaya bağlıyor. Babel'in tek beyanı bunu G1-P'de gösterdi.

## Yan etkinin yönü

Değişiklik yalnız temizde sıfır beyanlı koşularda eşiği 0'dan yukarı alır. Yani bir tespiti kaldırabilir ya da geciktirebilir, hiçbir zaman yeni tespit doğurmaz.

## Ölçüt

1. **Testler:** `tests2/test_evre.py`'ye iki yeni test.
   - Temizde 0 beyan ve sonra tek beyan → tespit yok.
   - Temizde 0 beyan ve sonra bir saniyede 5 beyan → tespit.
   - Mevcut evre testlerinin hepsi geçmeli. Mimari denetimi ihlalsiz olmalı.
2. **Regresyon `k244 → k249`** (yeni donmuş kopyadan):
   - 87 vakanın hepsi ölçümde birebir aynı olmalı; değişen yalnız kod kimliği (`arac_hash`, `kosu_kimligi`).
   - Sebep: satırlarda M4 taşıyan 5 vaka var (kâhin ve doğrudan komşu) ve beşinde de tespit yok; değişiklik yeni tespit doğuramaz.
   - `--degisen` ve `--izin` yok. Bir vaka ölçümde değişirse sebebi bulunmadan devam edilmez.
3. **G1-P yeniden** (`evre_metrikleri_kapilari.py 1p`, aynı kopyadan):
   - Babel 1001'in tespiti kalkmalı. Öteki yedi koşunun M4'ü, M3'ü ve M1'i birebir aynı olmalı.
   - Beklenen: M4 yanlış tespit 1/8 (OLSRv2 1001) · M3 1/8 · M1 1/4 → **GEÇTİ**.
4. **G1ç ve G2ç + G4ç yeniden koşulmaz.**
   - Gerekçe: değişiklik yeni tespit doğuramaz ve iki kapıda da Babel'in tespiti yoktu. G1ç'de Babel 1003 · 1004, G2ç'de Babel 1003 · 1004 M4 "yok".
   - Bu kapılardaki öteki tespitlerin (AODV 1004, G2ç) temiz evresinde beyan var.
5. **Ardından donma:** AODV-k ve Babel-a (kuyruk beklentisi, "Donma"), sonra tam takım ve mimari denetimi.

## Süre

- Regresyon üretimi ~80 dk (k244'te 78,6 dk). G1-P ~25 dk. Sırayla, tek ağır iş, ~1 sa 45 dk.
