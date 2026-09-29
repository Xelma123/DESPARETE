# G1-P — boş kol kapısı, gerçek protokollerle · BEKLENTİ (ölçümden önce)

Ajan, 28 Eylül 2026. K-196'nın evre metrikleri parçası (öğrenci onayı: "M3/M4 düzeltmesi").

## Soru
K-193'te karıştırıcısız kolda OLSR'ın M4'ü 3/3 tohumda "tespit" etti (16 · 6 · 9 s), şok derinliği ±0,06–0,09 çıktı. Sebep: kayıp ve kopma beyanı zamanda kümeleniyor; M4'ün Poisson boş hipotezi ve M1/M3'ün Agresti–Caffo hata payı bağımsızlık varsayıyor. Düzeltme (`sim2/olcum/evre.py`, serbest parametre yok, momentler koşunun kendi temiz evresinden):
- M1 · M3: SE = max(Agresti–Caffo, s_L · √(1 + L/T)) — s_L temizdeki kayan 15 s pencere PDR'lerinin SD'si.
- M4: 1 s kova sayımlarının ortalaması ve varyansıyla negatif binom (varyans ≤ ortalama ise Poisson, eşik eskisiyle aynı). Bonferroni aynı.

## Düzen
Referans dünya (`referans_2026`), `statik-yok`, yere toplama, tam pencere (ısınma 50 · hayali açılma 150 · ölçüm sonu 320 s). Protokoller AODV · OLSR · AOMDV · DESPARETE (v0.4.1), tohum 1000 · 1001 → 8 koşu, 8 işçi, dondurulmuş kopyadan. Tahmini süre ~20 dk.

Üretici:
```
DESPARETE_DUNYA=referans_2026 PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python -u kalibrasyon/evre_metrikleri_kapilari.py 1p
```

## Ölçüt (kapı — değiştirilmez)
| madde | ölçüt | nominal hata payı |
|---|---|---|
| M4 | yanlış tespit (sansürsüz) ≤ 1/8 koşu | koşu başına aile α ≤ 0,05 → P(≥2/8) ≤ 0,057 |
| M3 | toparlanma_suresi ≠ 0 ≤ 1/8 koşu | koşu başına ~0,025 (tek yanlı) |
| M1 | kol ortalaması 2 SE dışında ≤ 1/4 protokol | protokol başına ~0,05 → P(≥2/4) ≈ 0,014 |

Beyan etmeyen protokol M4'te "sınanmadı" diye ayrıca yazılır (geçti sayılmaz).

## Tahminim
- Eski kural aynı defterlerde: M4 yanlış tespit OLSR 2/2, toplam ≥ 3/8 (kapıyı geçemezdi); M1'de OLSR 2 SE dışında.
- Yeni kural: M4 0–1/8, M3 0/8, M1 0/4 → G1-P GEÇER.
- OLSR'ın kume_se'si AC'nin ~3–5 katı; DESPARETE ve AODV'de ~1–2 katı (daha az kümeli).

## Kalırsa
Kural gevşetilmez. Hangi madde, hangi protokol, ne kadar — öğrenciye; seçenekler: temiz evrenin uzunluğu (ısınma/açılma), blok bootstrap, M4'te kova yerine pencere sayımı.
