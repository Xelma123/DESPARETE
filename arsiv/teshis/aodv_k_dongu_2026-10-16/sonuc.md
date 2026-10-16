# AODV-k · üç TTL düşüşünün döngü izi · sonuç

> 17 Ekim 2026 · ölçüt `beklenti.md` (commit `e0ab0b1`, koşudan önce) · kopya `1163f81` · çıktılar `dongu_{bagimsiz-yok_1000,gorev-yok_1000,gorev-yok_1001}.txt` · `zaman.txt` · `hukum.txt`

## 0 · İlk koşu ve aracın düzeltilmesi

- **İlk koşu** (16 Ekim 17:48–20:32): kimlik tuttu, ama iz eksikti.
  - Araç iç çağrıdan dönerken dış çağrının görüntüsüne bütün tabloyu yazıyordu. Rota kuran üç yöntem (`_komsu_rotasi`, `_ters_rota`, `_rrep_isle`) kuruluştan hemen sonra `_kurtarma`'yı çağırdığı için kuruluşlar kayda geçmiyordu; yalnız geçersizleştirmeler görünüyordu.
  - İzde aynı düğümün ardışık kayıtları birbirine bağlanmıyordu, hata buradan fark edildi.
  - Çıktılar `ilk_kosu_eksik_iz/`'de; sınıflaması geçersiz.
- **Düzeltme:** iç çağrıya girilirken dış çağrının o ana kadarki değişiklikleri kendi adına yazılır. Sonda zincir sürekliliği denetlenir. Kısa pencerede 36 112 ardışık kayıtta 0 boşluk çıktı.
- **Yeniden koşu:** 16 Ekim 22:26 – 17 Ekim 01:23, Babel teşhisiyle birlikte (8 işçi). Beklenti ve karar kuralı değişmedi.

## 1 · Kimlik ve süreklilik

| hücre | PDR (U1) | korunum | TTL düşüşü | zincir boşluğu |
|---|---|---|---|---|
| bağımsız 1000 | 0,3900 (0,3900) | geçerli | 1 | 0 / 309 450 |
| görev 1000 | 0,4451 (0,4451) | geçerli | 1 | 0 / 287 090 |
| görev 1001 | 0,5172 (0,5172) | geçerli | 1 | 0 / 249 966 |

Ölçüt 1 tuttu. Bayat RREP kabulü (K-205'in H-a'sı) üç hücrede de 0.

## 2 · TTL ile ölen paketlerin döngüsü

**Bağımsız 1000** · paket 6905, hedef 0, döngü 21 ↔ 24, t 172,7 s. Araç aynı döngüde iki paketi işaretledi: 6905 ve 6911, ölçüsü "TTL kalanı ≤ 1". Korunum defteri bir TTL düşüşü sayıyor; iki paketin döngüsünü aynı değişiklikler kuruyor.
- Yer istasyonu (0) aynı anlarda iki RREQ yayıyor (sıra 493 ve 494). 1 ms arayla iki düğüme farklı yollardan ulaşıyorlar. Her biri tekrar olmayan RREQ olduğu için ters rotayı günceller.
- 21'in rotası 24 üzerinden kuruluyor (172,668, `_ters_rota`); 24'ün rotası 21 üzerinden (172,672, `_ters_rota`).
- **Kural:** RFC §6.5, ters rotada sonraki atlama ve atlama sayısı her tekrar olmayan RREQ'te yazılır; yalnız sıra koşulludur ("copied if greater"). ns-3 `RecvRequest` aynı (`SetNextHop(src)`, `SetHop(hop)` koşulsuz).
- **Sonuç:** mekanizma.

**Görev 1000** · paket 7693, hedef 12, döngü 14 ↔ 21, t 192,4 s.
- 14'ün 12'ye rotası komşu rotası: 1 atlama, geçerli sırası yok (§6.2; ns-3 `UpdateRouteToNeighbor`).
- 192,299'da 21'den gelen, sırası 75 olan 4 atlamalık bir RREP bunu değiştiriyor (`_rrep_isle`). RFC §6.7 (i): sıra geçersizse güncellenir; ns-3 `RecvReply` aynı.
- 21'in 12'ye rotası ise 12'nin RREQ'inden 14 üzerinden kurulmuş (187,267, `_ters_rota`, §6.5).
- **Sonuç:** mekanizma.

**Görev 1001** · paket 2070, hedef 0, döngü 33 ↔ 22, t 51,7 s.
- 22 → 30 rotası RERR'le geçersizleşiyor ve RERR'in sırası kopyalanıyor (51,357, sıra 145 aynı kalıyor; §6.11 iii).
- Hemen ardından 33'ten gelen, sırası eşit (145) bir RREP geçersiz rotayı güncelliyor (51,389). RFC §6.7 (iii): eşit sıra ve rota etkin değil; ns-3 `RecvReply` aynı.
- 33'ün rotası ise 22'nin daha önce gönderdiği RREP'ten (51,358).
- K-205'te `AODV-g` sonrası kalan döngülerin mekanizmasıyla aynı.
- **Sonuç:** mekanizma.

## 3 · Karar

Ölçüt 2'ye göre üç paketin döngüsünü kuran değişikliklerin hepsi RFC'nin bir kuralından geliyor. Hepsi ns-3'le aynı; kusur adayı yok.

- K-207 madde 2'ye göre üç hücre açıklanmış sayılır.
- `ACIKLANMIS_DUSUK_REFERANS["aodv"]`a ve `KAYITLI_ORAN`a bu ize atıfla girdiler. Her hücrenin metninde döngünün kuralı yazılı.
- Yere toplama kaydı `hukum` ile yeniden yargılandı: **U1-U GEÇTİ · U1-B TEMİZ** (çıkış 0, `hukum.txt`). Yedi düşük hücre açıklanmış.
- `tests2/test_aodv.py`: 53 geçti.

Öngörü kısmen tuttu: karşılıksız RREP döngülerde görünmedi. Döngüleri kuranlar §6.5'in ters rotası, §6.7'nin (i) ve (iii) kabulleri ve §6.11'in sıra kopyalaması.

## 4 · Betimleyici (ölçüte girmez)

- Döngülü paket: 27 · 17 · 15. Paket başına döngüyü kuran son değişiklikler `_ters_rota`, `_rrep_isle` ya da ikisi birden.
- `_gecersizlestir`'in sırayı düşürdüğü durumlar 16 · 7 · 7. Bunlar RERR'den daha küçük bir sıranın kopyalanması (§6.11 iii'nin harfi); hiçbiri TTL ile ölen paketlerin döngüsünde yok.
