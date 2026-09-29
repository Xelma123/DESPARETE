# 4.1d · Hareketli kollar referans dünyada (35 km) — beklenti (ölçmeden önce)

> 27 Eylül 2026 · ajan · komutlar (dondurulmuş kopyadan, `--dunya referans_2026`):
> - `python -u kalibrasyon/theta_kollari.py`
> - `python -u kalibrasyon/dugum_sayisi.py --bolunme`
> - `python kalibrasyon/calisma_noktasi.py --bolum gorev_kolu`

⚠️ **K-187 öncesi uyarı:** `theta_kollari` `--dunya` alıyordu ama ölçüm gövdesi (`bag_kumesi`) eski dünyayı kuruyordu. Bu ölçümler K-187 düzeltmesinden SONRA koşulur.

## Ölçütler (değişmez)

- **Θ:** Θ_OLSR = τ / 15 s, Θ_AODV = τ / 3 s. τ = rota ömrü (yavaş SINR ≥ β, Kaplan–Meier).
- **Bölünme tablosu:** 4 kol × 40 ana deney tohumu × pencerede 9 an, kâhin grafiği.
- **Görev yarıçapı:** |görev derecesi − bağımsız derecesi| en küçük.

## Tahmin

**Görelilik:** eski dünya 1:50'de 1800 m'lik alanı (gerçek karşılığı 90 km) ~26 km'lik gerçek bağla, 10–30 m/s'e karşılık gelen hızlarla kuruyordu. Referans: 35 km, bağ ~10 km, hız 11–33 m/s. Bağ uzunluğu / hız oranı ~2,6 kat küçük, yani bağlar daha hızlı eskir.

- **Θ:** eski değerlerin **~0,3–0,5 katı** (ör. formasyon Θ_OLSR 2,31 → ~0,7–1,2); kopmayan çift oranı azalır.
- **Bölünme:** bağımsız kolda zaman ve kol ölçümünde 10 tohumun 4'ü koptu. Tablo için **25–45/160** bölünmüş (kol, tohum); eskiden 15/160. Statik 0, formasyon statik yerleşimi tuttuğu için az.
- **Görev yarıçapı:** alan oranıyla ~12,6 km; seçilen **10–14 km**.
