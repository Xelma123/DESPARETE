# U1 · `AODV-i` + `AOMDV-e` (K-210) — beklenti ve karar kuralları (ölçmeden önce)

> 1 Ekim 2026 sabah · ajan · sebep: U1 `AOMDV-c`'de eşler arası statik 1001 0,991 → 0,870 ve yere toplamada iki yeni düşük hücre. Teşhiste iki kusur bulundu:
> 1. AOMDV'nin kendi RREP/RREQ işleyicilerinde RFC §6.7/§6.6.2 öncül adımları yoktu.
> 2. RFC durum (ii)'nin RERR'i öncül listesine göre süzülüyordu; RFC'nin bu cümlesi normatif değil, ns-2 ve ns-3 süzmüyor. Süzme ters yoldan öğrenilmiş rotalarla kara delik doğuruyordu.
> Ayrıntı `denetim.md` (AOMDV ve K-210 bölümleri).
> Komutlar (dondurulmuş kopya `kopya_2/`, 8 işçi): `--desen yere_toplama --protokol aodv,aomdv`, sonra `--desen esler_arasi`. Süre ~9–10 sa. Makinede başka bir projenin deneyi (Kargoz, 8 işçi) koşarsa uzar.

## Ölçmeden önce bilinen (teşhis koşuları)

| hücre | protokol | PDR |
|---|---|---|
| eşler arası statik 1001 | AOMDV-b | 0,982 |
| | AOMDV-c | 0,862 |
| | AOMDV-e | **0,987** ("hedef yok" 1 225 → 2) |
| yere toplama statik 1002 | AOMDV-d | 0,903 |
| | AODV-h | 0,871 |
| | AODV-i | 0,866 |

## Karar kuralları (değişmez)

- **Tutarlılık:** kâhin PDR'leri 29 Eylül'le birebir.
- **U1-U** iki desende, iki protokolde de geçmeli. Kâhin aşımı K-192 (b) zarfı.
- **U1-B:** K-207. Sadakat denetimi geçmiş AODV'nin eşik altı hücreleri protokolün kendi sorunu (bulgu). AOMDV için de aynı ilke, çünkü RFC tabanı makalenin sustuğu yerlerde AODV-i ile aynı kurallara getirildi. AODV-h'nin açıklanmış hücre kaydı yeni sonuçla yeniden yazılır; ölü kayıt kalmaz.
- Ardından evre kapıları (1c, 2c), regresyon (k204; beklenti `arsiv/teshis/regresyon_k204/beklenti.md`, AODV/AOMDV vakaları değişebilir) ve donma kaydı.

## Sonuç (2 Ekim 01:00) ve kâhin aşımı kuralı

Kâhin PDR'leri birebir ✅.
- AODV-i: U1-U ✅ ✅. U1-B: yere toplamada yalnız statik 1002 (0,873, K-207 kaydı); bağımsız 1000 artık 0,604 (kaydı ölü, kaldırıldı). Eşler arası temiz.
- AOMDV-e: yere toplama temiz. Eşler arası U1-B temiz, ama iki yeni kâhin aşımı: bağımsız 1000 (0,9403 / 0,9351) · formasyon 1002 (0,9210 / 0,9143). Formasyon 1000 kayıtlı zarfın içinde (0,9854 ≤ 0,9986).

**Kural (K-192 b, ölçmeden önce):** iki hücrede üç kâhin (`aomdv_zarf_hucre.py`). AOMDV ≤ zarf → "ETX kâhini bu hücrede üst sınır değil", kayda girer. AOMDV > zarf → yazılım hatası aranır, donma bekler. Tutarlılık: ETX kâhini U1'deki değeri birebir üretmeli.
