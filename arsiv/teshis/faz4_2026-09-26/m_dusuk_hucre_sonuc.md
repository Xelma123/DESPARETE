# AODV U1-B düşük hücreleri (statik) — kayıp anatomisi · sonuç

> 27 Eylül · ajan · beklenti `m_dusuk_hucre_beklenti.md` (ölçmeden önce).
> Çıktılar `m_anatomi_statik_{1000,1001,1002}.txt`. Kopya `m_kopya` (önbellekli güncel kod). Süre 1544 s.

| tohum | U1 oranı | AODV düşüş / üretilen | `iletim_basarisiz` | `rota_gecersiz` | `ttl` | kâhin düşüş (hepsi `iletim_basarisiz`) |
|---|---|---|---|---|---|---|
| 1000 | 0,736 | 27,8 % | 1846 | 1672 | 36 | 1,8 % (233) |
| 1002 | 0,880 | 13,2 % | 995 | 691 | 0 | 1,3 % (169) |
| 1001 | 0,957 | 4,5 % | 430 | 143 | 0 | 0,2 % (30) |

Üretilen: tohum başına 12 798–12 799. Koşu sonunda kuyrukta 0. `kuyruk_tasmasi`, `tampon_asimi` ve `hedef_yok` 0. Bütün düşüşler "uzak" bölgede; karıştırıcı yok.

## Beklentiyle karşılaştırma

1. **Kimlik ✓ (sütun beyanıyla):**
   - Araç `pdr_pencere`yi basıyor, U1 ise tüm koşunun `pdr`sini kullanıyor. Beklenti dosyası yanlış sütunu karşılaştırılacak diye yazmıştı.
   - Korunumdan türetilen 1 − düşen/üretilen altı hücrenin altısında U1 değerine 4 basamakta eşit: AODV 0,7223 · 0,9552 · 0,8683; kâhin 0,9818 · 0,9977 · 0,9868.
   - Kanca davranışı değiştirmiyor. Önbellekli kod ile U1'in önbelleksiz kopyası aynı sonucu veriyor; bu, K-190'ın uzun pencerede ikinci doğrulaması.
2. **Neden ✓:**
   - Baskın sebep `iletim_basarisiz`, ikinci sebep `rota_gecersiz`.
   - Kuyruk ve tampon düşüşü 0.
   - Sıra 1000 > 1002 > 1001; 1000/1001 oranı 6,2 (≥ 3).
3. **Kâhin ✓:** düşüşü ≤ %1,8, hepsi `iletim_basarisiz`.
4. **Bölge ✓:** hepsi "uzak".
5. **Süre ✗:** 1,5–2,5 sa demiştim, 26 dk sürdü. Statik kol hızlı, önbellek de katkı yaptı.

## Okuma

**Gözlemsel, nedensel değil:**
- Düşük hücrelerde AODV'nin kaybı zayıf bağlarda MAC deneme hakkının bitmesi (`iletim_basarisiz`) ile başlıyor.
- Ardından rotanın geçersiz ilanı geliyor: `rota_gecersiz` düşüşleri ve sık yeniden keşif. Rota tamponu girişleri de aynı sırada: 6566 · 3970 · 1498.
- Kâhinin kendi kaybı da aynı sırada. Yani bu topolojilerde zayıf bağ daha çok ve en az atlama metriği onları seçiyor.
- AODV, kâhinin `iletim_basarisiz` sayısını 6–14 kat büyütüyor.
- Bu, en az atlama metriğinin bilinen bedelidir: uzun ve zayıf bağı seçer (De Couto ve ark. 2003, ETX'in çıkış nedeni). RFC 3561'e sadık bir AODV'nin beklenen davranışıdır; kodda kusur izi yok (kuyruk, tampon ya da döngü yok; `ttl` 36, %0,3).

**U1-B için:**
- Mekanizma bulundu ve üç hücreyi doğru sıralıyor.
- "Protokolün tasarım bedeli" U1-B'de **açıklanmış** sayılır mı? Bu bir okuma kararıdır; KR-1'in yanında öğrenciye sorulacak.
- Nedensel sınama önerisi: aynı tohumlarda en az atlama yerine ETX kullanan bir AODV ya da zayıf bağ eşiği. Faz 5'le örtüşür.

**Açık:** bağımsız 1000 (hareketli kol) ölçülmedi.
