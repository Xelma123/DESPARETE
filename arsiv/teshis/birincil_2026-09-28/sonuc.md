# Birincil hücre partisi — SONUÇ (K-200)

Ajan, 29 Eylül 2026. Beklenti ve karar kuralları `beklenti.md` (ölçümden önce). Çıktılar: `tam.txt` (anatomi raporu) · `kayit.json`/`kayit.jsonl` (32 koşunun bütün sayıları) · `ozet.py` → `ozet.txt` (bu nottaki tablolar). Referans dünya, `formasyon · yere_toplama · derin_sizma · sürekli` 10 W, tam pencere, tohum 1003–1006, dondurulmuş kopya (`arac_hash 8f099aa1…`), 32/32 koşu hatasız, 7,1 sa (8 işçi).

## Kararlar — önceden yazılan kurallara göre

**1 · OLSR §13:** d = PDR(OLSR-c) − PDR(OLSR-b) = +0,049 · +0,059 · +0,037 · +0,064 → ort **+0,052** > R (0,023), 4/4 pozitif → **OLSR-c kalır, kanıtlı** (karıştırma altında da §13 zararlı). Eski dünyanın tek karıştırıcılı regresyon vakasındaki ters işaret (−0,13) yanıltıcıydı.

**2 · Rota tamponu:** 256 paket ve 60 s kolları temel AODV ile **tüm koşu PDR'si ve düşüş tablosu birebir aynı** (4/4 tohum) → tampon birincil hücrede hiç bağlamıyor; sonuç bu iki parametreye **duyarsız**. Değerler ns-3 kaynağında kalır (K-198).

## Anatomi (Faz 5.0'ın ilk ölçümü)

| kol | PDR pencere (ort) | tohumlar 1003 · 1004 · 1005 · 1006 | kâhin − protokol | doğuma göre: önce · açık · sessiz |
|---|---|---|---|---|
| DESPARETE v0.4.1 | **0,700** | 0,665 · 0,725 · 0,613 · 0,796 | 0,114 | 0,78 · 0,56 · 0,75 |
| AOMDV-b | 0,569 | 0,534 · 0,700 · 0,441 · 0,602 | 0,244 | 0,62 · 0,47 · 0,61 |
| AODV-f | 0,556 | 0,506 · 0,679 · 0,461 · 0,577 | 0,257 | 0,64 · 0,46 · 0,57 |
| OLSR-c | 0,418 | 0,463 · 0,402 · 0,278 · 0,529 | 0,395 | 0,48 · 0,27 · 0,52 |
| ETX kâhini | 0,813 | 0,766 · 0,891 · 0,780 · 0,818 | — | 0,86 · 0,73 · 0,85 |

Eşli farklar (tohum başına): DESPARETE − AODV +0,158 · +0,045 · +0,152 · +0,219 (ort +0,144, SD 0,072) · − AOMDV ort +0,130 · − OLSR ort +0,282 · AOMDV − AODV ort +0,013. **Geliştirme tohumları, 4 tohum — ana deney değil;** δ henüz ölçülmedi.

- **Düşüş sebepleri** (üretilene oran, 4 tohum): AODV rota_gecersiz %24 · iletim_basarisiz %19 · OLSR rota_gecersiz %44 · iletim_basarisiz %9 · AOMDV %22 · %19 · DESPARETE iletim_basarisiz %17 · rota_gecersiz %11 · kâhin iletim_basarisiz %17. Temel protokollerle kâhin arasındaki farkın büyük kısmı **rotasızlık** (rota_gecersiz); DESPARETE bunu yarıya indiriyor, iletim başarısızlığı kâhin düzeyinde.
- **Açık evre herkesi düşürüyor** (kâhin dâhil 0,86 → 0,73); sessiz evrede temel protokoller "önce" düzeyine dönmüyor (AODV 0,64 → 0,57), OLSR ve kâhin dönüyor. DESPARETE açıkken 0,56 — iyileştirilecek yer açık evre.
- **Karar bağlarının %92–98'i kâhine göre iyi**; başarısız bağların iyi payı AODV %55, DESPARETE %75, OLSR %82 → AODV başarısızlıklarının çoğu zayıf bağlarda (en az atlamanın bedeli, K-191).
- **Evre metrikleri:** şok derinliği AODV 0,155 · DESPARETE 0,233 (temizi yüksek, kaybedeceği çok) · toparlanma süresi AODV 15 s · DESPARETE 21 s · OLSR 3,5 s. ⚠️ Karıştırıcı periyodik (15 s açık/sessiz): M3'ün "tek basamak" tanımı burada anlamını yitiriyor — Faz 6'da çizelgeli karıştırıcıda evre tanımı yazılmalı (`08` açık maddesi).

## Aletin sınırı — yeni iş

**Bölge sınıflaması anlık:** bir düşüşün bölgesi (ed · girişim · uzak) o anki karıştırıcı gücüyle okunuyor; sessiz evrede her düşüş "uzak" sayılıyor. Bu yüzden bölge tablosu (%87–97 uzak) karıştırıcının etki alanını değil çoğunlukla sessizliği gösteriyor. Düzeltme: bölgeyi karıştırıcı AÇIK olsaydı alacağı güçle de sınıfla (evre × bölge çapraz tablo). Faz 5.0'ın ilk işi.

Üretici: tablolar `python arsiv/teshis/birincil_2026-09-28/ozet.py` (çıktı `ozet.txt`). Anatomi komutu:
```
DESPARETE_DUNYA=referans_2026 python -u kalibrasyon/kayip_anatomisi.py --dunya referans_2026 --kol formasyon --aile derin_sizma --sinif surekli --protokoller "olsr,olsr_s13,aodv,aodv@rota_tamponu_kapasitesi=256,aodv@rota_tamponu_omru_s=60,aomdv,desparete,en_guvenilir_kahin" --tohumlar 1003,1004,1005,1006 --isci 8 --kayit <yol>/kayit.json
```
