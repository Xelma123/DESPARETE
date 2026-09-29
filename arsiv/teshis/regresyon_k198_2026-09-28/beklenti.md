# Regresyon k196 → k198 · BEKLENTİ (koşudan önce)

Ajan, 28 Eylül 2026. Taban `k196`. Yeni `k198`, dondurulmuş kopyadan (`dondur.py` artık `tests2/`yi de kopyalar), 8 işçi, başka ağır iş yanında koşulmaz.

## k196'dan bu yana değişen kod
| değişiklik | etkilemesi beklenen |
|---|---|
| `Konfig.sonumleme_uretec` (varsayılan `"tekil"`, referans dünyada `"blok"`) | her satırın `konfig` bölümünde YENİ alan `sonumleme_uretec` |
| sönümlemede blok kipi (`rng.normal_dizisi`, `Sonumleme._fir_blok`) | YALNIZ referans dünya vakaları (`r-referans-…`, 3 vaka): kanal izi değişir, istatistiği değişmez (`performans_2026-09-28/denklik.txt`) |
| köken defteri: +`sonumleme_uretec`, +`PENCERE_ONBELLEK_SINIRI` (TÜRETİLMİŞ); `rota_tamponu_*` SINANMAMIŞ → KAYNAK | her satırda `koken_kovalari`: TURETILMIS 65 → 67 · KAYNAK 27 → 29 · SINANMAMIS 44 → 42 |
| kayıp anatomisi, koruma testi, belgeler | hiçbir satır |

## Beklenen farklar (önceden ilan)
- `--degisen r-referans-` (3 vaka, geçerli olmak zorunda).
- `--izin konfig.sonumleme_uretec,teshis.koken_kovalari`.
- **Eski dünyanın 64 vakası BİREBİR** (yeni alan ve köken kovaları dışında) — `"tekil"` yolu bayt bayt aynı olmalı. Tek bir fark = bulgu.

Üretici:
```
PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python -u kalibrasyon/regresyon_satirlari.py uret k198
PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python -u kalibrasyon/regresyon_satirlari.py karsilastir k196 k198 --izin konfig.sonumleme_uretec,teshis.koken_kovalari --degisen r-referans-
```
Süre: k196 üretimi 30,9 + ~15 dk (eksik 5 vaka). Tek seferde ~35–45 dk.
