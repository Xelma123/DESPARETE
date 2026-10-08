# Regresyon k215 → k220 — beklenen farklar (ölçmeden önce)

> 8 Ekim 2026 · ajan · K-220: `iletim_menzili_m` → `nominal_bag_m` (yalnız ad) · üç parametre DÜNYA TANIMI · kalibrasyon aletleri (U1 kayıtları, G3ç, 5C, duman kapsamı). Simülatör davranışı DEĞİŞMEDİ.
> `py -3.11 -u kalibrasyon/regresyon_satirlari.py uret k220` → `karsilastir k215 k220 --izin kimlik.kurulum_hash,kimlik.tedavi_hash,konfig.iletim_menzili_m,konfig.nominal_bag_m,teshis.koken_kovalari`

## Değişen (izinli)

- `konfig.iletim_menzili_m` yok, `konfig.nominal_bag_m` var — BÜTÜN vakalarda, değer aynı.
- `kimlik.kurulum_hash` · `kimlik.tedavi_hash` — alan adı özete girdiği için bütün vakalarda.
- `teshis.koken_kovalari` — K-217 (altı DUYARSIZ) ve K-220 (üç DÜNYA TANIMI) kova değişiklikleri.
- Kod kimliği (otomatik).

## Değişmemesi gerekenler

80 vakanın HEPSİNDE metrikler, korunum, ham ve öteki teşhis alanları BİREBİR. `--degisen` yok. Kural: izinli alanlar dışında her fark BULGU'dur.
