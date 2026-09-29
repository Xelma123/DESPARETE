# 4.3 · Taban protokollerin uygunluğu (U1) referans dünyada — beklenti (ölçmeden önce)

> 27 Eylül 2026 · ajan · öğrenci onayı (uzun koşu, "boş durma") · dondurulmuş kopya `kopya_43` (`arac_hash` c90c279c…)
> Komut: `python -u kalibrasyon/aodv_uygunluk.py --dunya referans_2026 --desen <d> --protokol <p>`, sırayla (yere toplama önce):
> AODV · OLSR · AOMDV × yere_toplama · esler_arasi

## Ölçüt (K-136, değişmez)

Protokol / ETX kâhini teslim oranı: statik ≥ 0,90, hareketli ≥ 0,60.
- 4 kol (`-yok`) × 3 geliştirme tohumu, tam uzunluk.
- Açıklanmış düşük hücre referans dünyada YOK (K-188); her düşük hücre ölçülerek açıklanır.

## Öngörü

Duman kesiti (kısa pencere, kapı değil): AODV statik yere toplama 0,704 / kâhin 0,983 → 0,716.

**Neden:** 1:1 dünyada bağ 1 Mb/s'te ~9 km. Atlama sayısıyla yönlendiren protokoller en uzun, en zayıf bağı seçer (eski dünyadaki K-137 mekanizması). ARF zayıf bağda 1 Mb/s'e iner, yeniden denemeler artar.

| protokol | statik oran | hareketli oran | U1 |
|---|---|---|---|
| AODV | **0,70–0,85** | 0,45–0,75 | statikte KALIR |
| OLSR (HELLO ile iki yönlü bağ) | 0,75–0,90 | 0,45–0,75 | sınırda |
| AOMDV | AODV'ye yakın | | |

**Kalırsa:**
- Bu, uygulama kusuru değil protokol mekanizması olabilir. Açıklama için ölçülür: eşiksiz en kısa yolun teslimi (K-137 §4) ve bağ kalitesi dağılımı.
- Referans dünyada eşik (K-136) öğrenciye yeniden sorulur.

**Süre bandı:** protokol ve desen başına ~0,7–1,5 sa → toplam 5–9 sa (onaylı 12–27 sa bandının altında).
