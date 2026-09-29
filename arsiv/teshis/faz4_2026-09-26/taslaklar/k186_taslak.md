
# K-186 · 🟡 KARIŞTIRICI REJİMİ REFERANS DÜNYADA — hava karıştırıcısı sürüyü böler, yer karıştırıcısı kısmi kalır · birincil hücre öğrenciye
> 26 Eylül · Faz 4.1b · ölçüm ajan · beklentiler ölçmeden önce `arsiv/teshis/faz4_2026-09-26/b_karistirici_beklenti.md` (dört tur, hepsi yazıldı, yanlışlananlar işaretli)

**Ölçüler:** `karistirici_gucu` (kâhin grafiği, ED susturması dâhil, 30 tohum × 9 an, statik kol, 35 km).
- **Büyük bölünme = ikinci güçlü bileşen ≥ 4 İHA** (bir müfreze; K-186 tanımı).
- ⚠️ **Ölçü kusuru (ajan):** referans dünyada kâhin grafiği yönlüdür. Eski "birden fazla çok üyeli bileşen" sayımı BFS kümeleriyle yapılıyordu; yönlü grafikte bu kümeler üst üste biner ve güvenilmez. Bileşenler artık güçlü bağlı bileşenler (`kahin.ozet`; eski dünyada birebir aynı).

**Alan × güç** (`b_alan_guc.txt`): merkezdeki 1 W'lık karıştırıcı 10–35 km'nin HER alanında ağı böler (eski sayımla 15–30/30). Kenarın 8,75 km dışına çıkınca bile (`b_karistirici_mesafe_aile.txt`) 13/30.

**Aile × güç** (`b_aile_guc.txt`, güçlü bileşenlerle, 35 km):

| aile · platform | kaynak bandı | ρ | büyük bölünme | en kötü anda en büyük bileşen |
|---|---|---|---|---|
| `hava_eslik` · hava (görüş hattı) | 1–5 W (30–37 dBm) | 0,66–0,88 | **27–30/30** | %5–20 → sürü çöker |
| `tekli_merkez` · orta irtifa | — | 0,67–0,88 | 13–26/30 | %7–17 |
| `cephe_hatti` · 3 yer (yer–hava kaybı) | 10 W (40 dBm) | **0,20** | 1/30 | %85 |
| `hedef_koruma` · 2 yer | 10 W | 0,29 | 5/30 | %50 |
| `derin_sizma` · araç (hareketli) | 10 W | **0,16** | 2/30 | %48 |

**Fizik:**
- 1 W'lık görüş hattındaki karıştırıcı 100 mW'lık düğümlerden 10 dB güçlü. 8 km'lik bir bağın alıcısı karıştırıcıya ~14 km'den yakınsa bağ kopar.
- Seyrek ağ uzun bağlara, yoğun ağ ise karıştırıcının yakınlığına takılır; hiçbir alanda "kısmi" kalınmaz.
- Yer karıştırıcıları yer–hava kaybıyla (görüş hattı yokken ~21 dB) zayıflar; gerçekçi 10 W'ta bile kısmi kalır.
- `v2/14` §4'ün sınır cümlesi ("yönlendirmenin fark yarattığı yer, etki alanı sürüden küçük karıştırıcılar") ölçüldü: bu rejimi yer karıştırıcıları kurar, hava karıştırıcısı kurmaz.

**Sonuç:**
- Birincil hücrenin ailesi `hava_eslik` (öğrenci, 23 Eylül; eski dünyada −15 dBm'de kısmiydi) referans dünyanın kaynaklı gücünde sürüyü böler. Orada ölçülen yönlendirme değil, çöküş olur.
- **Karar öğrencide** (ön-kayıt §0.4.4).
