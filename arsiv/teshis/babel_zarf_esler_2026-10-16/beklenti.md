# Babel'in kâhin aşımı, eşler arası — K-192 (b) zarf prosedürü · beklenti (ölçmeden önce)

> 16 Ekim 2026 · tetik: K-244 kuyruğunun U1'i, eşler arası (`arsiv/teshis/rakipler_k244_2026-10-14/U1_esler_arasi_2.txt`; U1-U KALDI, kâhin aşımı). Kural kuyruğun beklentisinde (§2.1, commit `1163f81`): *"U1-U … iki protokolde, iki desende ✅ olmalı. Kâhin aşımı R'den büyükse K-192 (b) zarf prosedürü … Zarfın içindeyse kayıt; zarfı da aşıyorsa yazılım hatası aranır."*
>
> Betik `zarf.py`, yere toplamanınkiyle (`arsiv/teshis/babel_zarf_2026-10-15/`, sonucu `db6e6fe`) aynı. Değişenler yalnız desen, hücreler ve işçi sayısı. Donmuş kopyadan (`1163f81`) koşar.

## Hücreler (oran > 1 + R = 1,0126)

| kol | tohum | Babel | ETX kâhini | oran |
|---|---|---|---|---|
| bağımsız | 1002 | 0,8963 | 0,8787 | 1,020 |
| görev | 1000 | 0,9755 | 0,9612 | 1,015 |
| görev | 1001 | 0,8935 | 0,8403 | 1,063 |
| görev | 1002 | 0,8638 | 0,8392 | 1,029 |
| formasyon | 1001 | 0,9636 | 0,9424 | 1,022 |

R içindeki üç aşım için kayıt yeter, zarf gerekmez: statik 1001 (1,004), formasyon 1000 (1,004), formasyon 1002 (1,009).

## Düzen

- Üç kâhin `kalibrasyon/ust_referans.py::KAHINLER`: ETX · en kısa yol · en olası teslim.
- ETX kâhini U1'de aynı yapılandırmayla ölçüldü (deterministik); öteki ikisi koşulur.
- Zarf = üç PDR'nin en büyüğü.
- 10 iş, 5 işçi. AODV-k'nin döngü izi (3 işçi, `arsiv/teshis/aodv_k_dongu_2026-10-16/`) aynı anda koşar; toplam 8 işçi, tek ağır iş yükü.
- Süre tahmini ~2–2,5 sa: yere toplamada en olası teslim kâhini 57–78 dk sürdü; 10 iş 5 işçide iki dalga.

`aomdv_zarf_hucre.py` (kuyruk beklentisinde adı geçen betik) aynı prosedürü yürütür: aynı yapılandırma, aynı üç kâhin. Farkı ETX kâhinini yeniden koşması; burada U1'deki değeri kullanılır.

## Ölçüt

- **Her hücrede Babel ≤ zarf:** "ETX kâhini bu hücrelerde üst sınır değil" beyanı.
  - Sekiz hücre `KAHIN_ASIMI_ACIKLANMIS["babel"]`a ve `KAYITLI_ORAN`a girer: zarflı beş ve R içindeki üç.
  - Eşler arası kayıt `hukum` ile yeniden yargılanır; U1-U geçer.
- **Bir hücrede Babel > zarf:** yazılım hatası aranır (kâhin sızıntısı, sayım, korunum); Babel donmaz.

## Öngörü (ölçüt değil)

- Yere toplamada zarfı her hücrede en olası teslim kâhini verdi ve ETX kâhinini 0,047–0,059 aştı.
- Görev 1001'in aşımı (0,053) bu aralığın sınırında; zarfın içinde kalması da dışına çıkması da olası.
