# U1-B · eşik altı hücrelerin açıklaması — beklenti ve karar kuralı (ölçmeden önce)

> 30 Eylül 2026 sabah · ajan · kurallar K-137 · K-192 (c) · K-196 · `v2/04` U1. Öğrenci sırayı onayladı ("U1 bitince hüküm ve eşik altı hücrelerin açıklanması"; K-204).

## U1 sonucu (hüküm aracı koşunun hükmünü birebir üretti)

`py -3.11 kalibrasyon/aodv_uygunluk.py --dunya referans_2026 --protokol <p> hukum ciktilar2/aodv_uygunluk/<p>_referans_2026_<desen>_son.json`

| | yere toplama (donmayı bağlar) | eşler arası (keşifsel) |
|---|---|---|
| AODV | U1-U ✅ · U1-B: statik 1000 (0,863) · 1002 (0,874) eşik altı | U1-U ✅ · U1-B ✅ |
| OLSR | U1-U ✅ · U1-B: 8 hücre eşik altı | U1-U ✅ · U1-B: 8 hücre |
| AOMDV | U1-U ✅ · U1-B ✅ | U1-U 🔴 formasyon 1000 oran 1,002 (+0,0015 PDR) · U1-B: statik 1002 (0,889) |
| DESPARETE (bilgi) | U1-U ✅ · U1-B ✅ (en düşük 0,779) | — |

## Karar kuralları

**OLSR** (yere toplama ve eşler arası): K-196 — *"`OLSR-c` ile U1 yeniden koşulunca düşük hücreler bu kayda atıfla girer"* (açıklanmış, sıralamasız; mekanizma K-193: geçide rotanın aralıklı boşalması, geçici döngüler). Yeni ölçüm gerekmez.

**AOMDV kâhin aşımı** (eşler arası, keşifsel): K-192 (b) — aşım çözünürlükten (R) büyük değilse aşım sayılmaz; büyükse üç kâhinin zarfına bakılır, zarfı da aşıyorsa yazılım hatası aranır. Referans dünyanın R'si henüz ölçülmedi (Faz 4.4 #1, `cozunurluk.py --dunya referans_2026`, ~30 dk) → önce R.

**AODV statik 1000 · 1002** (yere toplama; donmayı bağlar): K-192 (c) — iki koşul.

1. **Kusur izi yok:** TTL (döngü) düşüşü 0 ve rota tamponu düşüşü 0 (U1'de 0 ölçüldü). Kuyruk taşması sıfır değilse kâhinle karşılaştırılır ve ayrıca açıklanır.
2. **Mekanizma sıralar:** TEK birincil değişken, ölçmeden önce seçildi: AODV'nin veri kararlarında kâhine göre **orta + kötü bağ payı** (atlama sayısıyla yönlendirmenin bedeli: "protokol kötü bağı SEÇİYOR", K-193 bantları). Açıklanmış sayılması için iki düşük hücrede de bu pay geçen hücreden (1001) YÜKSEK olmalı. Öteki sütunlar (başarısızlıkların bandı, `rota_gecersiz`, düşüş tablosu) yalnız betimleyici — sonradan seçilen bir sütunla açıklama yapılmaz.

**Ölçmeden önce bilinen olumsuz işaret:** K-190'ın yapısal ölçüsü (eşiksiz en kısa yolun teslimi, simülasyonsuz) bugünkü kodla statik hücreleri U1'in TERSİNE sıralıyor: 1000 0,520 (en yüksek) · 1001 0,358 · 1002 0,441. Komut: `py -3.11 arsiv/teshis/faz4_2026-09-26/k_esiksiz_yol.py` → `aciklama/esiksiz_yol_k204.txt`. K-190'da (sönümleme blok üreteci K-198'den önce) 1000 0,342 · 1001 0,589 · 1002 0,230 idi. Yani "en az atlamanın bedeli" bu kolda yapısal olarak sıralamıyor; anatomi, kararların gerçekte hangi bağlara gittiğini ölçer.

**İki koşuldan biri sağlanmazsa:** hücreler açıklanmamış kalır, donma bekler, K-137'nin sırası (kapı doğru mu → gerçekleme doğru mu → kalan fark nereden) uygulanır ve öğrenciye getirilir.

**Tutarlılık denetimi (alet):** anatomi koşusunun AODV ve kâhin PDR'si U1'dekiyle aynı olmalı (AODV 0,8569 · 0,9316 · 0,8717 · kâhin 0,9926 · 0,9921 · 0,9976). Farklıysa sebebi (konfig etiketi, kod hâli) yazılır.

## Koşu

Dondurulmuş kopya `aciklama/kopya` · `PYTHONIOENCODING=utf-8 py -3.11 -u kalibrasyon/kayip_anatomisi.py --dunya referans_2026 --kol statik --sinif yok --protokoller aodv,en_guvenilir_kahin --tohumlar 1000,1001,1002 --kayit ../kayit.json` · 6 koşu, 8 işçi, ~20–30 dk, yanında ağır iş yok.

## Sonuç 1 — anatomi (30 Eylül 07:04) ve karar

`anatomi.txt`, `kayit.jsonl` · PDR'ler U1'le aynı (tutarlılık ✅). **Açıklanmış SAYILMAZ:**
- Koşul 1 KALDI: TTL düşüşü 1000'de 42 · 1002'de 16 · 1001'de 4 (TTL 32, yollar ~1,8 atlama → döngü).
- Koşul 2 harfiyen sağlandı ama bilgisiz: orta+kötü karar payı 1001 %1,64 < 1002 %2,03 < 1000 %2,38. Aradaki ~%0,7 karar, ~7 puanlık PDR açığını karşılayamaz. Açığın çoğu `rota_gecersiz` (+504) ve kâhinin iyi dediği bağlarda iletim başarısızlığı (+414).

→ K-137 sırası, adım 2 (gerçekleme doğru mu): döngünün kaynağı.

## Sonuç 2 — döngü izi (`dongu_izi.py`, eski kod `AODV-f`)

Aday ölçmeden önce betiğin başında yazılı (H-a bayat RREP kabulü · H-b ara düğüm keşfi · H-c öteki).

| tohum | döngülü paket | son değişiklik bayat kabul | koşu boyunca bayat kabul |
|---|---|---|---|
| 1000 | 77 | 61 (+6 karışık) | 331 |
| 1001 | 4 | 4 | 99 |
| 1002 | 23 | 14 | 336 |

H-b 1 kez → mekanizma değil. **Kusur H-a:** `_rrep_isle` geçersiz girdiyi sıraya bakmadan güncelliyordu; RFC 3561 §6.7 (i)–(iv) ve ns-3 `RecvReply` yalnız bilinmeyen · büyük · eşit sırayı kabul eder.

**Düzeltme `AODV-g` (K-205), dört parça RFC'den:** §6.7 kuralı · §6.2 komşu rotası geçerli sırasız (ns-3 `UpdateRouteToNeighbor`) · §6.11 sıra yalnız geçerliyse artar, RERR'de kopyalanır · kaynak keşfi yalnız rota kurulduysa kapatır (AOMDV S10 tuzağına karşı). AOMDV davranışı birebir korunur (kendi `_gecersizlestir`i eski kuralı taşır; test).

## Beklenti — düzeltmeden sonra (ölçmeden önce)

1. Aynı iz, `AODV-g` ile, 3 tohum: bayat kabul 0 · döngülü paket ~0 · TTL düşüşü ~0.
2. Keşif çökmesi YOK: `kesif_basarisiz` ve tampon düşüşü eskisinden belirgin fazla değil (AOMDV S10'daki gibi "keşif başarılı, rota yok" olmamalı).
3. PDR: 1000 ve 1002'de artması beklenir. Geçmeleri beklenmez; kalan fark `iletim_basarisiz` ve `rota_gecersiz`in geri kalanıdır. Karar U1'in yeniden koşusuyla verilir (AODV, iki desen, yeni dondurulmuş kopya); AOMDV, OLSR ve DESPARETE'nin kaydı değişmez.
4. Regresyon: eski ve referans dünyanın bütün AODV satırları değişebilir (beklenen fark); AOMDV satırları BİREBİR kalmalı.

## Sonuç 3 — düzeltmeden sonra, küresel saatle (`dongu_f_kuresel_*`, `dongu_g_kuresel_*`)

⚠️ İlk izler rota değişikliklerini düğümün YEREL saatiyle (ofset + sapma) kaydediyordu; "döngüden önceki son değişiklik" sıralaması saniyelerce kayabilirdi. Betik artık olay saatini kullanıyor; eski kod U1 kopyasından (`DONGU_KOK`). `dongu_odak*` geçersiz (kısa kesilen koşu tam koşuyla aynı olayları üretmiyor).

| tohum | kod | döngülü paket | son değişiklik bayat kabul | TTL düşüşü | PDR (pencere) |
|---|---|---|---|---|---|
| 1000 | AODV-f | 77 | 72 (+2 karışık) | 42 | 0,8635 |
| 1000 | AODV-g | 5 | 0 | 4 | 0,8865 |
| 1002 | AODV-f | 23 | 16 | 16 | 0,8759 |
| 1002 | AODV-g | 32 | 0 | 21 | 0,8681 |

Beklenti 1 kısmen: bayat kabul 0 ✅, döngü 1000'de ✅, 1002'de ❌. Beklenti 2 ✅ (keşif başarısızlığı 0). Elenen ikinci aday: ters rota sırayı düşürmüyor (AODV-g'de 0 olay; AODV-f'de 34 vardı, düzeltmeyle kalktı). 1002'deki döngü örneği (170–172 s): 26 geçide 3 üzerinden (sıra 266) → 3'ün rotası RERR'le düşer, sıra RERR'den KOPYALANIR (266, §6.11) → 3, 26'nın RREP'ini §6.7 (iii) (eşit sıra, etkin olmayan rota) ile kabul eder → 3 ↔ 26. RFC'ye uygun kurallar; gerçekleme kusuru değil. U1 `AODV-g` ile yeniden: `arsiv/teshis/u1_aodv_g_2026-09-30/`.
