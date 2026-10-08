# Faz 4.5 · doğrulama listesinin referans dünyada bir kez koşulması — ölçütler (ölçmeden önce)

> 8 Ekim 2026 ~02:00 · ajan · kod K-215…K-218 (taban protokoller dondu, K-218). Dondurulmuş kopyadan (`kopya`), sırayla, yanında ağır iş yok. Liste `arsiv/DEVIR-2026-09-28-temizlik.md` §2'nin ayıklama taslağı + `DEVIR-PROMPT.md` §5. Her adımın süresi kaydedilir (bütçe).

**Zaten koşuldu (K-216…K-218):** regresyon k215 · çözünürlük R · U1 iki desen + hüküm · evre kapıları 1c · 2c · kayıt indeksi. Tam test takımı ve mimari denetimi kapanışta yeniden.

| # | komut (DESPARETE_DUNYA=referans_2026 ortamıyla, aksi yazılmadıkça) | ölçüt |
|---|---|---|
| 1 | `anlamlilik_sabitleri.py` (sentetik, dünyadan bağımsız) | `KAPI GECTI` |
| 2 | `bag_kumesi.py a` | `G-a` · `G-b GECTI`, çıkış 0 |
| 3 | `li_replikasyonu.py --dunya referans_2026` | sabit hızda H1 ≈ 0,127 TUTTU (K-187); Li AODV/kâhin kullanıyorsa sayı K-215 kodu yüzünden oynayabilir — oynarsa sebebi yazılır |
| 4 | `kontrol_duzlemi_kapilari.py` | `KAPI OZETI` hepsi GECTI (eski dünyada 21/21) |
| 5 | `denetim_ornekleme.py` | `KAPI OZETI: 4/4 GECTI` |
| 6 | `ust_referans.py --kapi` | üç kapı `OK`, çıkış 0 |
| 7 | `evre_metrikleri_kapilari.py` (varsayılan: 1 · 1p · 2 · 3 · 4) | beşi `GECTI` |
| 8 | `uretici_duman.py` (kesitler kendi dünyalarında) | bütün kesitler çıkış 0; kapsam kapısı temiz |

**Kural:** kalan bir kapı önce kendi anlamıyla okunur. Eski çekirdek hücreye (`statik-surekli`) bağlıysa ve o hücre referansta tabandaysa (kâhin PDR 0,03, K-206) → "referansta anlamsız" diye AYIKLANIR (tarihçe, kapı değil) ve hangi referans aletinin yerini tuttuğu yazılır. Değilse BULGU — sebebi aranır, sayı uydurulmaz.

**Ayıklanmış, koşulmayacak (taslaktaki gerekçeyle):** adım 9 kapanışı (eski dünya, arşivde) · onay semantiği 14/17 (Y2 mekanizması, eski dünyanın tarihçesi) · kâhin tavanı `pdr_tavani.py 1` (yerini U1'in kâhin sütunu tuttu: statik 0,99–1,00, hareketli 0,84–0,97, K-217) · karıştırıcı çalışma noktası 5/5b/5c (yerini K-186'nın aile × güç ölçümü tuttu).

## Sonuç 1 (03:42) — sekiz adım, toplam 2 sa 1 dk

| # | sonuç | süre |
|---|---|---|
| 1 anlamlılık | 🟢 KAPI GEÇTİ | 12 s |
| 2 bağ kümesi | 🟢 G-a · G-b | 6 s |
| 3 Li | H1 = 0,0427 (A8/ARF; K-187'de 0,0426) — **sabit hız (0,127) bu araçla değil**, `arsiv/teshis/faz4_2026-09-26/b_li_ayristirma.py` ile; DEVIR satırı yanlış yazılmış | 4 dk |
| 4 kontrol düzlemi | 🟢 21/21 · P6 17/6/6 | 21 dk |
| 5 örnekleme denetimi | 🔴 3/4 — C: `aldatici` ↔ `surekli` kenar kümeleri 0/270 birebir | 5 dk |
| 6 üst referans | 🟢 üç kapı | 2 dk |
| 7 evre (1 · 1p · 2 · 3 · 4) | G1 · G1-P · G2 · G4 🟢 · **G3 🔴** | 61 dk |
| 8 üretici dumanı | 🟢 bütün kesitler | 28 dk |

**Okuma (kural gereği, önce kapının anlamı):**
- **C kapısı** önermesi "aldatıcı ile sürekli'nin TEK farkı CSMA görünürlüğü"dür ve kâhin grafiğinde CSMA'nın OLMADIĞI geometrik kipte kurulmuştu. Referansta kâhin ED susturmasını içerir (K-183) ve aldatıcı tanım gereği ED'yi tetikler (statik-aldatıcıda derece 0) → kenar kümeleri tam da CSMA yüzünden ayrışır. Kapı referansta aynı soruyu ED dışarıda bırakılarak sorar (araç uyarlandı; geometrik kipte birebir eski). 🔵 Faz 6'ya not: referansta 10 W aldatıcı bütün ağı susturuyor — `06` H1.3'ün aldatıcı ↔ sürekli kontrastı bu dünyada dejenere olabilir.
- **G3** eski çekirdek hücrede (`statik-surekli`) koşar; referansta o hücre tabanda (M1 ≈ 1,0 → Agresti–Caffo SE'si 0,003'e çöküyor, 0,005'lik fark "karar değişti" sayılıyor) → AYIKLANIR. Yerini **G3ç** alır: aynı soru birincil hücrede, kâhinle, `CIZ_TOHUMLAR` (araca `3c` kipi eklendi).

## Sonraki üç adım — ölçüt (ölçmeden önce, 04:00)

- **5C (referans biçimi)** `denetim_ornekleme.py c`: ED dışarıda bırakılınca `aldatici` ↔ `surekli` kenar kümeleri **270/270 birebir** → "tek fark CSMA" önermesi referansta da geçerli; değilse fark CSMA'dan başka bir yerden de geliyor (bulgu, aranır).
- **G3ç** `evre_metrikleri_kapilari.py 3c`: iki tohumda ızgara yarım adım (0,5 s) kayınca |ΔM1| ≤ 2 SE.
- **Li sabit hız** `b_li_ayristirma.py <kopya>`: A8-arf kolunda H1 ≈ 0,127 TUTTU (K-187); A8 kolunda ≈ 0,043 TUTMADI.

## Sonuç 2 (04:25)

- **5C referans biçimi:** ED dışarıda `aldatici` ↔ `surekli` **270/270 birebir** 🟢 (ED dâhil 0/270, bilgi) → "tek fark CSMA" önermesi referansta da geçerli. Örnekleme denetimi 4/4.
- **G3ç** 🟢: 1003 M1 0,2158 → 0,2130 (|Δ| 0,0028 ≤ 2 SE 0,0382) · 1004 0,0716 → 0,0663 (0,0053 ≤ 0,0243); M4 iki fazda da tespit yok.
- **Li sabit hız:** A8-arf H1 = **0,1188 TUTTU** (bant 0,1–0,2); K-187'de 0,1270. Sebep ölçüldü (`li_beacon.py`, ölçüt betiğin başında): beacon 32 B'la **0,1270 birebir** → fark K-215'in 84 B beacon'ı (doygun zincirde beacon havada daha uzun). A8 0,0409 (32 B'la 0,0407) TUTMADI — K-187 gibi; `li_replikasyonu.py`nin kendi H1'i 0,0427 (K-187: 0,0426).
- **Faz 4.5 kapandı:** referansta anlamlı her kapı geçti; iki kapı referans biçimine taşındı (5C, G3 → G3ç), dört alet ayıklandı (beklenti başı).
