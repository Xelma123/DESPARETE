# A1 · sonuç satırı ve kimlik — ölçmeden ÖNCE yazılan beklenti (25 Eylül 2026)

Adım: `v2/15` A1 (K-171). Davranış değişikliği YOK; yalnız satırın kimlik ve şema alanları.

## Tam test takımı
`PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python -m pytest tests2 -q -p no:cacheprovider`
- Beklenti: hepsi geçer. Yeni testler: kimlik (4), politika (2), koşu kimliği (2), PDR yön ayrımı (2).

## Regresyon — `uret k171` ↔ `k157`
`python kalibrasyon/regresyon_satirlari.py karsilastir k157 k171 --yeni k- --izin <aşağıdaki> --sifir <aşağıdaki>`

Beklenen farklar (başka HİÇBİR alan değişmemeli; sayılar birebir):
- **KOD_KIMLIGI (otomatik):** `kimlik.arac_hash` (CRLF normalleştirme + kod), `kimlik.kosu_kimligi` (yeni girdiler), `kimlik.protokol_hash` (yeni alan) — bütün ortak vakalarda.
- **İzinli (--izin):**
  - `kimlik.tedavi_hash` — yeni alan, bütün vakalarda;
  - `kimlik.sayac_semasi_hash` — yeni sayaç `politika_dusen`;
  - `metrikler.politika_dusen*` — yeni sayaç ve pencere ikizi;
  - `korunum.dusen.politika` — yeni düşme sebebi;
  - `metrikler.pdr_telemetri*`, `metrikler.pdr_komut*` — yalnız iki `g-…-yere_toplama` vakasında.
- **Sıfır (--sifir):** `metrikler.politika_dusen`, `korunum.dusen.politika` — ortak vakaların hepsinde 0 (hiçbir eski vaka DESPARETE koşmuyor).
- **Yeni vakalar (--yeni k-):** `k-statik-surekli-{aodv,olsr,aomdv}`, `k-statik-surekli-desparete-yere_toplama` — dördü de `gecerli=True`. DESPARETE vakasında `korunum.dusen.politika` > 0, `hedef_yok` bu kadar azalmış olmalı (eski davranışta bunlar `hedef_yok`tu), `pdr_komut` = 0.
- Süre: eski üretim ~35–45 dk (8 işçi); 4 yeni kısa vaka paralel koşar, bant 35–50 dk.
