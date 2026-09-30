# U1 · `AODV-g` (K-205) — beklenti ve karar kuralları (ölçmeden önce)

> 30 Eylül 2026 08:15 · ajan · sebep: U1-B'de AODV statik 1000 · 1002 açıklanamadı, döngü izi gerçekleme kusurunu buldu (`arsiv/teshis/u1_2026-09-29/aciklama/beklenti.md` Sonuç 1–2). Düzeltme RFC 3561 §6.2 · §6.7 · §6.11'e ve ns-3'e dönüş. K-137 sırasının 2. adımı.
> Komutlar (dondurulmuş kopya `kopya/`, 8 işçi, yanında ağır iş yok):
> `py -3.11 -u kalibrasyon/aodv_uygunluk.py --dunya referans_2026 --desen yere_toplama --protokol aodv`, sonra aynısı `--desen esler_arasi`
> Süre (29 Eylül koşusunun süreleriyle): yere toplama ~2,5–3 sa · eşler arası ~1,5–2 sa.

## Tutarlılık (alet)

Kâhinin kodu değişmedi (araç kod kimliği değiştiği için yeniden koşar). **Kâhin PDR'leri 29 Eylül'dekilerle BİREBİR** olmalı (ör. yere toplama statik 0,9926 · 0,9921 · 0,9976). Farklıysa sebep bulunmadan hüküm verilmez.

## Ölçmeden önce bilinen (düzeltilmiş kodla döngü izi, statik, `aciklama/dongu_g_kuresel_*.txt`)

PDR (pencere) 1000: 0,8635 → 0,8865 · 1001: 0,9328 → 0,9256 · 1002: 0,8759 → 0,8681. Döngülü paket 77 → 5 · 4 → 1 · 23 → 32. Kalan döngüler RFC'ye uygun kurallardan: RERR'de sıra kopyalama (§6.11) + eşit sırada etkin olmayan rotanın güncellenmesi (§6.7 iii) + kabul edilmeyen RREP'in iletilmesi (ns-3 ile aynı).

## Karar kuralları (değişmez: K-136 · K-137 · K-192)

- **U1-U** iki desende de geçmeli → geçmezse `AODV-g` donmaz, sebep aranır.
- **U1-B** eşik altı hücreler `aciklama/beklenti.md`'deki kuralla değerlendirilir. ⚠️ Koşul 1 ("TTL düşüşü 0") RFC'ye sadık bir AODV'de sağlanamayabilir: kalan TTL düşüşleri RFC'nin kendi kurallarından doğuyor, gerçekleme kusurundan değil. Bu okuma ölçütün kendisini değiştirdiği için **öğrencinin onayına** gider. Ajan onu kendi başına uygulamaz.
- Hareketli hücreler: eski koşuda hepsi geçti; bir hücre eşiğin altına düşerse ayrıca ölçülerek açıklanır.
- AOMDV, OLSR ve DESPARETE'nin 29 Eylül kaydı geçerli kalır (kodları değişmedi; AOMDV'nin birebirliği regresyonla sınanır).
