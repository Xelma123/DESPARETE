

# K-188 · 🟢 GÖLGELEME BİRİM HATASI DÜZELDİ · referans alanı 33 km · Θ · görev yarıçapı 16 km · araç tuzakları (ikinci tur)
> 27 Eylül · Faz 4.1 · ajan · beklentiler ölçmeden önce `arsiv/teshis/faz4_2026-09-26/f_golge_beklenti.md`, `e_hareket_beklenti.md`

**1 · 🔴 Birim hatası** (A7 atlaması, ajan):
- `referans_2026` eski dünyanın `golgeleme_hucre_m = 50`sini ölçeklemeden taşıdı. Değer 1:50 uzaydaydı, yani gerçekte 2,5 km.
- 1:1 dünyada gölgeleme 50 kat hızlı değişti ve rota ömrü yapay olarak çöktü: bağımsız kolda Θ_OLSR 0,29 (`e_theta.txt`). Düzeltmeyle 8,18 (`e_theta_golge25.txt`).
- **Düzeltme:** `golgeleme_hucre_m = 50 × olcek = 2500 m`, SINANMAMIŞ kalır (duyarlılık ekseni).
- Bütün uzunluk ve hız alanları tarandı: hızlar, müfreze yarıçapı, titreşim ve tehdit hızları zaten çevrilmişti; GPS ve yer karıştırıcı yüksekliği fiziksel birimdeydi.

**2 · Alan yeniden: 33 km** (`a2_alan_golge25.txt`):

| alan | derece | ≥ 3 atlama | kopuk |
|---|---|---|---|
| 30 km | 11,1 | %18,3 | %0 |
| 33 km | 9,67 | %26,9 | %0 |
| 35 km | 8,88 | %31,3 | %0,5 |
| 37 km | 8,21 | %36,5 | %0,3 |
| 40 km | 7,17 | %44,9 | %0 |
| 45 km | 5,83 | %54,2 | %2,3 |

- Araç "geçen en büyük" alanı, yani 40 km'yi seçiyor. Ama 35 ve 37 km kopuyor: kopukluk nadir bir olay, tekdüze bir özelliğin tekdüze olmayan sonucu örnekleme şansıdır.
- **Sağlam sınır:** altındaki her alanın geçtiği en büyük değer, **33 km**. K-185'in 35 km'si hatalı gölgeleme birimiyle ölçülmüştü.
- Beklenti 30–35 km ✓.

**3 · Karıştırıcı 33 km'de** (`b2_aile_guc_33km.txt`):
- Birincil hücre (`derin_sizma`, 10 W): ρ 0,173, büyük bölünme 1/30, en kötü anda en büyük parça %82,5. 35 km'de 2/30 ve %48'di.
- Hava karıştırıcısı 1–5 W'ta 27–30/30 bölünüyor.
- K-186'nın kararı geçerli.

**4 · Görev yarıçapı: 16 km** (`e2_gorev_33km.txt`):
- Derece 8,10 ↔ bağımsız 8,16; fark 0,06.
- Izgara 6–16 km; 2r < alan sınırı 16,5 km. Beklenti 10–14 km ✗.
- `referans_2026` artık alan oranıyla türetmiyor, ölçülen değeri kullanıyor.

**5 · Θ (33 km)** (`e_theta_33km.txt`, 6 tohum):

| kol | Θ_OLSR | Θ_AODV | kopmayan | eski dünya |
|---|---|---|---|---|
| bağımsız | 5,15 | 25,7 | %88 | 3,25 |
| görev | 2,79 | 13,9 | %84 | 3,99 |
| formasyon | tanımsız | tanımsız | %99,6 | 2,31 |

- Formasyonda tek bir ömür gözlendi; statik kolun kuralıyla tanımsız sayıldı.
- Beklenti (eskinin 0,3–0,5 katı) ✗: bağımsız kolda daha büyük çıktı.

**6 · 🔴 Araç tuzakları, ikinci tur** (ajan):
- `dugum_sayisi` alanı eski dünyanın sabitinden (1800 m) kuruyordu → seçili dünyadan.
- `aodv_uygunluk`un açıklanmış düşük hücreleri eski dünyanın (kol, tohum) çiftleriydi → referans dünyada boş.
- **Kapsam beyanı:** satırın Θ ve bölünme payı eski dünyanın tablolarından okunuyordu → dünyaya göre ayrıldı (aşağıda).

**7 · Bölünme tablosu 33 km'de** (`e3_bolunme_33km.txt`; 4 kol × 40 ana deney tohumu × 9 an):
- **8/160** bölünmüş (kol, tohum); eski dünyada 15/160. Beklenti 25–45 ✗.
- Çoğu tek bir kenar düğümünün kopması (39 ulaşılamaz çift). Tohum 2029'da bir düğüm statik yerleşimde hep kopuk; statik ve formasyonda 9/9 ve 8/9 an.
- **Tablolar artık dünyaya ait:** `MOBILITE_THETA_REFERANS`, `MOBILITE_BOLUNME_REFERANS`; `kapsam` satırın dünyasını okur (test K-188).

**8 · Yük 33 km'de** (`d2_yuk_33km.txt`; ölçüt K-124, 3 tohum, tam uzunluk):

| telemetri | 0,5 | 1,0 | 1,5 | 2,0 | 3,0 |
|---|---|---|---|---|---|
| kâhin PDR | 0,998 | **0,989** | 0,965 | 0,892 | 0,605 |

- Ölçüt 1,5'i seçer. **Bugünkü 1,0 korunur:** eksen dengesi, öğrenci kararı K-126 (39 × 1 + 4 × 0,25 = 40 = eşler arası 10 × 4).
- Beklenti ≥ 0,97 ✓. Uçurum 1,5 ile 2,0 arasında; eski dünyada 2,5–3,0'dı, yani marj %150'den %50'ye indi (beyan).
- Hatalı birimle yapılan ilk koşu (`d_yuk_golge50_hatali.txt`) 1,0'da 0,993 vermişti; nitel olarak aynı.

**9 · PER eğrileri** (`b_per.py` → `b_per.txt`; 1024 B, PER %8):
- Duyarlılık: 1 Mb/s −96,6 · 2 Mb/s −92,0 · 5,5 Mb/s −89,5 · 11 Mb/s −86,5 dBm.
- Dördü de standardın alt sınırının (−80 dBm, G2) üstünde. 1 Mb/s, G1'in CMU Prism 2.5 ölçüm aralığında (−94 … −100).
- Hızlar arası aralıklar (4,6 · 2,5 · 3,0 dB) tipik 802.11b yongalarının mertebesinde.

**Ölçüm:**
- Tam takım **919 passed** (24,7 dk). Beklenti 921'di; K-185 ve K-186'nın testleri önceki takımda (917) zaten sayılmıştı, eklenen 2 test. Sayım hatası (beyan).
- Mimari denetimi "Yapısal ihlal YOK".
- `uret k185` 67/67 geçerli, 42,6 dk.
- `karsilastir k184 k185 --degisen r-referans- --izin teshis.koken_kovalari` → **64/64 BİREBİR**.
- `r-statik-yok` PDR 0,297 (beklenti 0,20–0,45 ✓).
- **Geçerli taban `k185`.**
- **⚠️ Kural:** takım ve regresyon bir alt kabukta arka plana atıldı; bitiş bildirimi gelmedi, izleme bekçi betiğiyle yapıldı. İlerlemeyi izlemek için bu biçim kullanılmaz.
