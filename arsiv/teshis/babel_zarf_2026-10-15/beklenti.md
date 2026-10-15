# Babel'in kâhin aşımı — K-192 (b) zarf prosedürü · beklenti (ölçmeden önce)

> 15 Ekim 2026 · tetik: K-244 kuyruğunun U1'i, yere toplama (`arsiv/teshis/rakipler_k244_2026-10-14/sonuc.md` §2). Kural kuyruğun beklentisinde, U1'den önce yazıldı: *"Kâhin aşımı R'den büyükse K-192 (b) zarf prosedürü … Zarfın içindeyse kayıt; zarfı da aşıyorsa yazılım hatası aranır."* Betik `zarf.py`, donmuş kopyadan (`1163f81`).

## Hücreler (oran > 1 + R = 1,0126)

| kol | tohum | Babel | ETX kâhini | oran |
|---|---|---|---|---|
| bağımsız | 1001 | 0,9095 | 0,8882 | 1,024 |
| bağımsız | 1002 | 0,8548 | 0,8334 | 1,026 |
| görev | 1001 | 0,8957 | 0,8679 | 1,032 |
| görev | 1002 | 0,9198 | 0,8998 | 1,022 |

Formasyonun iki aşımı (1,005 · 1,006) R içinde; kayıt yeter, zarf gerekmez.

## Düzen

- Üç kâhin `kalibrasyon/ust_referans.py::KAHINLER`: ETX · en kısa yol · en olası teslim.
- ETX kâhini U1'de aynı yapılandırmayla ölçüldü (deterministik); öteki ikisi koşulur. 8 iş, 8 işçi, ~50 dk.
- Zarf = üç PDR'nin en büyüğü.

## Ölçüt

- **Her hücrede Babel ≤ zarf:** "ETX kâhini bu hücrelerde üst sınır değil" beyanı. Altı hücre `KAHIN_ASIMI_ACIKLANMIS["babel"]`a ve `KAYITLI_ORAN`a girer (formasyonun ikisi R içinde diye), `hukum` ile yeniden yargılanır; U1-U geçer.
- **Bir hücrede Babel > zarf:** yazılım hatası aranır (kâhin sızıntısı, sayım, korunum); Babel donmaz.

## Öngörü (ölçüt değil)

En olası teslim kâhini hareketli kollarda ETX kâhinini geçebilir (K-110'un zarf gerekçesi). Babel'in saniyeler içinde uyarlanan ETX'i, kâhinin ortalama bağ kalitesinden yararlı olabilir. Yön belirsiz.
