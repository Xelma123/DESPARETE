# G1-P — SONUÇ · 🟢 GEÇTİ

Ajan, 28 Eylül 2026. Beklenti `beklenti.md` (ölçümden önce), tam çıktı `tam.txt` (son satır `KAYIT` = 8 koşunun bütün sayıları). Dondurulmuş kopya `arac_hash 8aa7a4fd…`.

| madde | ölçüt | yeni kural | aynı koşularda eski kural |
|---|---|---|---|
| M4 yanlış tespit | ≤ 1/8 | **0/8** | 6/8 (2–45 s) |
| M3 toparlanma ≠ 0 | ≤ 1/8 | **0/8** | 3/8 (4 · 31 · 17 s) |
| M1 kol ortalaması 2 SE dışında | ≤ 1/4 | **0/4** | 2/4 (AOMDV · DESPARETE) |

Kümelenmenin büyüklüğü (8 koşunun 8'inde küme SE > Agresti–Caffo):
| protokol | küme SE / AC | temiz kova beyanı ort / var (1/s) | M4 eşiği NB (Poisson) |
|---|---|---|---|
| AODV | 2,4 · 1,9 | 30,7 / 105 · 34,2 / 196 | 77 · 102 (51 · 56) |
| OLSR | 6,1 · 6,8 | 27,4 / 193 · 33,7 / 191 | 100 · 100 (47 · 55) |
| AOMDV | 2,4 · 1,4 | 33,3 / 135 · 33,3 / 206 | 86 · 104 (55 · 55) |
| DESPARETE | 2,2 · 1,2 | 3,7 / 4,8 · 1,5 / 1,9 | 14 · 9 (12 · 7) |

## Tahminlerin tutması
- Eski kural kapıyı geçemezdi (M4 ≥ 3/8): ✅ 6/8.
- "Eski kuralda M1'de OLSR 2 SE dışında": ❌ — dışarıda kalanlar AOMDV ve DESPARETE; OLSR'ın şok derinliği küçük çıktı (−0,022).
- Yeni kural geçer: ✅ üç maddede de sıfır.
- Küme SE / AC: OLSR 3–5 kat beklendi, **6–7 kat** çıktı; ötekiler 1–2 kat beklendi, 1,2–2,4 kat.

## Bedeli (beyan)
- OLSR'da tohum başına M1'in 2 SE'si **0,22–0,26**: tek tohumda şok derinliği OLSR için neredeyse bilgisiz. Kol düzeyinde 40 tohumla ~0,04. Ana deneyin H2 testi tohum düzeyinde PDR'dir, etkilenmez.
- Temel protokollerde M4 eşiği saniyede ~50'den ~80–100 kopma beyanına çıktı: gerçek bir karıştırma daha geç "tespit" edilir. DESPARETE'nin beyanları neredeyse Poisson (var/ort 1,3), eşiği az değişti.

## Not
- Süre: koşu başına 596–2644 s, duvar ~45 dk (beklenti ~20 dk). Sebep: aynı anda tam test takımını koşturdum, çekirdekler paylaşıldı. Sonuçlar deterministik, etkilenmez; 30 dk sınırı benim hatamla aşıldı.
- Koşudan SONRA `_negatif_binom_esigi`de `log1p` kaldırıldı (mimari test: `log1p` PER gövdesinin imzası, `kanal.py` dışında yasak). İki yol 15 960 (ortalama, varyans, α) noktasında ve bu 8 koşunun momentlerinde **birebir aynı eşiği** veriyor; sonuç depodaki kod için geçerli.
