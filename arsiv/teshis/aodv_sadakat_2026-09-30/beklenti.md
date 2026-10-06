# U1 · `AODV-h` + `AOMDV-c` (K-208) — beklenti ve karar kuralları (ölçmeden önce)

> 30 Eylül 2026 akşam · ajan · öğrenci şartı (K-207): AODV sadakatle donar, sonra eşik altı hücreler protokolün kendi sorunudur.
> Denetim ve düzeltmeler `denetim.md` (H1–H11). Testler 62 geçti.
> Komutlar (dondurulmuş kopya `kopya/`, 8 işçi, yanında ağır iş yok): `py -3.11 -u kalibrasyon/aodv_uygunluk.py --dunya referans_2026 --desen yere_toplama --protokol aodv,aomdv`, sonra aynısı `--desen esler_arasi`.
> Süre: yere toplama ~4,5 sa · eşler arası ~3 sa (29 Eylül koşusunun süreleriyle).

## Ölçmeden önce bilinen (statik, döngü izi `dongu_h_*.txt`)

| tohum | AODV-f → g → h: döngülü paket | TTL düşüşü | PDR (pencere) |
|---|---|---|---|
| 1000 | 77 → 5 → 6 | 42 → 4 → 1 | 0,864 → 0,887 → 0,898 |
| 1001 | 4 → 1 → 1 | 4 → 0 → 0 | 0,933 → 0,926 → 0,924 |
| 1002 | 23 → 32 → 5 | 16 → 21 → 2 | 0,876 → 0,868 → 0,871 |

RREQ yarıya indi (ara düğüm U bayraklı RREQ'e cevap veriyor), RERR ikiye katlandı (rotasız ara düğüm RERR gönderip düşürüyor), keşif başarısızlığı 0.

## Karar kuralları

- **Tutarlılık:** kâhin PDR'leri 29 Eylül'le birebir (kâhin kodu değişmedi).
- **U1-U** iki desende de, iki protokolde de geçmeli → geçmezse donma yok, sebep aranır. Kâhin aşımı K-192 (b) (zarf).
- **U1-B:** K-207 — sadakat sağlandı (denetim + testler); eşik altında kalan hücreler "protokolün kendi sorunu" olarak BULGU diye raporlanır, donmayı durdurmaz. Her birinin yanında denetimin sonucu durur.
- **AOMDV:** AODV'den devraldığı kısımlar değişti (H7 kısmen, H8, H9, H10, H11); kendi kuralları (Şekil 3, S10) aynı. U1-B'de yeni bir düşük hücre çıkarsa aynı ilke.
- Ardından regresyon: AODV ve AOMDV vakaları değişebilir (`k-statik-surekli-aodv` · `t-statik-surekli-aodv-dugum_kaybi` · `r-referans-statik-surekli-aodv` · `k-statik-surekli-aomdv` · `u-*-aodv` · `u-*-aomdv`), gerisi birebir.
