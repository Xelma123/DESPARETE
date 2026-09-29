# AODV U1-B düşük hücreleri — kayıp anatomisi · beklenti (ölçmeden önce)

> 27 Eylül · ajan · öğrenci onayı (27 Eylül: "Evet, koş") · K-190 §6'nın devamı

**Soru:** statik-yok 1000 (oran 0,736) ve 1002 (0,880) neden düşük, 1001 (0,957) neden yüksek?

**Koşu:** `kalibrasyon/kayip_anatomisi.py --dunya referans_2026 --sinif yok --kol statik --protokoller aodv,en_guvenilir_kahin --tohumlar <t>`.
- Her tohum ayrı koşulur (1000, 1001, 1002), çünkü araç tohumları toplar.
- Tam pencere (50; 320; 350 s). Güncel (önbellekli) kodun dondurulmuş kopyası `m_kopya`.
- Süre 1,5–2,5 sa.

**Beklenti:**
1. **Kimlik:** anatomi aracının PDR'si U1 hücresiyle 4 basamakta aynı çıkar. `kol` etiketi yalnız üst veride; pencere ve desen aynı; kanca davranışı değiştirmez.
   - AODV: 0,7223 · 0,9552 · 0,8683.
   - Kâhin: 0,9818 · 0,9977 · 0,9868.
   - Tutmazsa önce bu açıklanır.
2. **Neden** (ön-bulgu: kayıplar "uzak" zayıf uzun bağlarda):
   - İpucu: rota tamponu girişleri düşük hücrelerle aynı sırada. 1000'de 6566, 1002'de 3970, 1001'de 1498.
   - Beklenen: AODV'nin düşüşlerinde baskın sebep `iletim_basarisiz`. En az atlamalı rota zayıf uzun bağlarda deneme hakkını bitiriyor, ardından RERR ve yeniden keşif. İkinci sebep `rota_gecersiz` ya da `hedef_yok` ve tampon.
   - `kuyruk_tasmasi` küçük kalır (< üretilenin %2'si).
   - AODV düşüş payının sırası 1000 > 1002 > 1001; 1000/1001 oranı ≥ 3.
3. **Kâhin:** düşüşleri üretilenin ≤ %3'ü, çoğu `iletim_basarisiz`.
4. **Bölge:** karıştırıcı yok, bütün düşüşler "uzak".

**Tutmazsa:**
- Baskın sebep kuyruk ya da tampon çıkarsa neden tıkanıklıktır, zayıf bağ değildir.
- 1000/1001 oranı < 2 çıkarsa fark düşüş sayısında değil "koşu sonu kuyrukta"dadır.
- Her iki durumda da açıklama değişir ve beyan edilir.
