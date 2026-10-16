# Babel'in kâhin aşımı — K-192 (b) zarf prosedürü · sonuç

> 16 Ekim 2026 · ölçüt `beklenti.md` (commit `67a52c6`, koşudan önce) · kopya `1163f81` · koşu 15 Ekim 23:46 – 16 Ekim 01:05, 78 dk (beklenti ~50 dk; en olası teslim kâhini koşuları 57–78 dk sürdü) · çıktılar `zarf.txt` · `zarf.jsonl` · `zaman.txt` · `hukum.txt`

## 1 · Zarf (yere toplama, referans dünya)

| kol | tohum | ETX kâhini | en kısa yol | en olası teslim | zarf | Babel | zarfa pay |
|---|---|---|---|---|---|---|---|
| bağımsız | 1001 | 0,8882 | 0,6762 | 0,9663 | 0,9663 | 0,9095 | 0,057 |
| bağımsız | 1002 | 0,8334 | 0,6311 | 0,8803 | 0,8803 | 0,8548 | 0,026 |
| görev | 1001 | 0,8679 | 0,5826 | 0,9261 | 0,9261 | 0,8957 | 0,030 |
| görev | 1002 | 0,8998 | 0,6739 | 0,9626 | 0,9626 | 0,9198 | 0,043 |

**Dört hücrede de Babel ≤ zarf.** Ölçüte göre bu hücrelerde ETX kâhini üst sınır değildir; aşım kayda geçer (K-192 b).

- Zarfı her hücrede en olası teslim kâhini veriyor; ETX kâhinini 0,047–0,059 aşıyor. Beklentideki öngörü (K-110'un zarf gerekçesi) bu yönde tuttu.
- En kısa yol kâhini dört hücrede de en düşük (0,58–0,68): hareketli kollarda atlama sayısını en aza indiren yol zayıf bağları seçiyor.

## 2 · Kayıt (`kalibrasyon/aodv_uygunluk.py`)

- `KAHIN_ASIMI_ACIKLANMIS["babel"]`: altı hücre.
  - Dördü zarfla, ölçülen üç kâhin değeri gerekçe metninde.
  - Formasyonun ikisi (1,0053 · 1,0057) R'nin içinde olduğu için zarf adımı gerektirmiyor; ölçümleriyle kayıtta.
- `KAYITLI_ORAN["babel"]`: aynı altı hücrenin oranı (DD-07 bandı).

## 3 · Yeniden hüküm (`hukum` kipi, ölçmez)

```
py -3.11 kalibrasyon/aodv_uygunluk.py --dunya referans_2026 --protokol babel hukum ciktilar2/aodv_uygunluk/babel_referans_2026_yere_toplama_son.json
```

**U1-U GEÇTİ · U1-B TEMİZ** (çıkış 0, `hukum.txt`).

- Altı aşım "açıklanmış" olarak basılıyor.
- Eşik altı hücre yok: en düşük oran statikte 0,989, hareketlide 0,899 (bağımsız 1000).

Doğrulama:

- `tests2/test_aodv.py`: 53 geçti.
- Mimari denetimi: ihlal 0, kuyruğun çıktısıyla aynı.

## 4 · Kalan

- Babel'in eşler arası U1'i kuyruğun kalanında koşulur; ara kayıttan devam eder.
- Babel donma adayıdır (`Babel-a`). Donma, kuyruğun sonunda AODV-k ile birlikte yapılır.
