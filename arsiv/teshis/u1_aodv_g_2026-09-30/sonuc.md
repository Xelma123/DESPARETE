# U1 · `AODV-g` — sonuç (30 Eylül 08:09 – 12:11)

Komutlar `beklenti.md`de · günlükler `yere_toplama.txt`, `esler_arasi.txt` · kayıtlar `ciktilar2/aodv_uygunluk/aodv_referans_2026_<desen>_son.json` (ara kayıt `…_aodv_g.jsonl`) · hüküm aracı koşunun hükmünü birebir üretti.

**Tutarlılık ✅:** 24 kâhin koşusunun PDR'si 29 Eylül'dekilerle birebir aynı.

## Oranlar (AODV / ETX kâhini) — `AODV-f` → `AODV-g`

| kol | 1000 | 1001 | 1002 | kol ort. |
|---|---|---|---|---|
| **yere toplama** statik (≥ 0,90) | 0,863 → **0,891** 🔴 | 0,939 → 0,933 | 0,874 → **0,867** 🔴 | 0,892 → 0,897 |
| bağımsız (≥ 0,60) | 0,601 → **0,598** 🔴 | 0,706 → 0,720 | 0,686 → 0,680 | 0,664 → 0,666 |
| görev | 0,736 → 0,710 | 0,706 → 0,696 | 0,731 → 0,722 | 0,725 → 0,709 |
| formasyon | 0,803 → 0,797 | 0,858 → 0,843 | 0,772 → 0,758 | 0,811 → 0,799 |
| **eşler arası** statik | 0,999 → 0,999 | 0,994 → 0,996 | 0,990 → 0,993 | 0,994 → 0,996 |
| bağımsız | 0,965 → 0,967 | 0,901 → 0,911 | 0,837 → 0,895 | 0,901 → 0,924 |
| görev | 0,934 → 0,952 | 0,686 → 0,741 | 0,774 → 0,777 | 0,798 → 0,823 |
| formasyon | 0,977 → 0,995 | 0,906 → 0,940 | 0,952 → 0,991 | 0,945 → 0,975 |

- **U1-U** iki desende de ✅.
- **U1-B:** eşler arası ✅; yere toplamada 3 hücre eşik altı: statik 1000 ve 1002, bağımsız 1000. Bağımsız 1000 eşiğin 0,002 altında; `AODV-f`'de 0,001 üstündeydi.
- **Yön:** eşler arasında düzeltme her kolda iyileştirdi. Yere toplamada statikte ortalama biraz arttı, hareketli kollarda biraz düştü (görev −0,016 · formasyon −0,012). Kurallara aykırı "bayat" rotalar bazen işe yarıyordu; RFC'ye sadık AODV biraz daha kötü. Straw-man değil, sadakatin bedeli.

## Karar kuralına göre

Üç düşük hücre ölçmeden önce seçilen değişkenle (orta + kötü karar payı) **açıklanmış sayılamaz**. Koşul 1 (TTL = 0) statikte sağlanmıyor (1000'de 4, 1002'de 21 TTL düşüşü); kalan döngüler RFC'ye uygun kurallardan (K-205). Veriye bakıp başka değişken seçmek ön-kaydı bozar. → **Donma kararı öğrenciye.**

Aday mekanizmalar (ölçülmedi, sıralayıcılığı sınanmadı): statikte `rota_gecersiz` (RERR ve yerel onarım yokluğu; döngü izinde 529 · 251 · 731) ve kâhinin iyi dediği bağlarda iletim başarısızlığı (kontrol trafiğiyle çarpışma olabilir).
