# Gölgeleme hücresi birim düzeltmesi (K-188) — yeniden ölçümlerin beklentisi (ölçmeden önce)

> 27 Eylül 2026 · ajan

**Kusur (A7 atlaması, ajan):**
- `referans_2026` eski dünyanın `golgeleme_hucre_m = 50`sini ölçeklemeden taşıdı. O değer 1:50 uzaydaydı, yani gerçekte 2,5 km.
- 1:1 dünyada gölgeleme 50 kat hızlı değişti. Θ_OLSR bağımsız kolda 0,29'a çöktü (`e_theta.txt`); doğru birimle **8,18** (`e_theta_golge25.txt`).
- **Düzeltme:** `golgeleme_hucre_m = 50 × 50 = 2500 m`, değer SINANMAMIŞ kalır.
- Diğer uzunluk ve hız alanları tarandı: hepsi ya fiziksel birimde verilmiş ya ölçekle çevrilmiş.

**Etkilenen ölçümler ve öngörü:**

| ölçüm | 50 m ile | 2,5 km ile öngörü |
|---|---|---|
| alan (statik kolda kopukluk %0 olan en büyük) | 35 km | **30–35 km**: ilişkili gölgeleme zayıf bağları kümeler, bölünme biraz erken gelir |
| karıştırıcı aile × güç (35 km) | `derin_sizma` 10 W: ρ 0,16, büyük bölünme 2/30 | nitel olarak aynı: hava karıştırıcısı böler, yer/araç 10 W'ta kısmi; büyük bölünme sayısı ±5 |
| görev yarıçapı | 16 km (ızgara kenarı) | yine 14–16 km |
| yük (1 pkt/s geçer) | 0,993 | ≥ 0,97; statik kolda gölgelemenin marjinal dağılımı değişmez |
| Θ | bağımsız 0,29 · görev 0,32 · formasyon 0,65 | ölçüldü: 8,18 · 3,68 · tanımsız (%99,6 kopmuyor) |

Seçilen alan değişirse karıştırıcı ve görev ölçümleri o alanda yeniden koşulur.
