# AODV-k · üç TTL düşüşünün döngü izi · beklenti (ölçmeden önce)

> 16 Ekim 2026 · tetik: AODV-k anatomisi (`arsiv/teshis/aodv_k_anatomi_2026-10-16/sonuc.md` §0).
>
> - Kuyruğun ön-kaydı (`arsiv/teshis/rakipler_k244_2026-10-14/beklenti.md` §2.2) açıklama için "döngü/TTL düşüşü 0" ister. Bağımsız 1000, görev 1000 ve görev 1001'de birer TTL düşüşü var. Kuralın sonucu: *"kusur aranır, protokol donmaz"*.
> - Şartın okunuşunu K-207 madde 2 belirler (K-205'in açık sorusuna yürütücünün kararı): *"kusur izi = gerçeklemenin kaynağından sapması. RFC'nin kendi kurallarından doğan geçici döngü mekanizmadır, kusur değildir."*
> - Betik `dongu_izi.py`, K-205'in izinin (`arsiv/teshis/aodv_sadakat_2026-09-30/dongu_izi.py`) genelleştirmesi. Donmuş kopyadan (`1163f81`) koşar.

## Düzen

- **Hücreler:** üç hücre, U1'in yapılandırması (yere toplama, referans dünya, tam pencere); her biri ayrı süreç, 3 işçi.
- **Eşzamanlılık:** Babel'in eşler arası zarfı (5 işçi) aynı anda koşar; toplam 8 işçi.
- **Kayıt:** rota tablosunu değiştirebilen bütün AODV yöntemleri sarılır. Her değişiklik onu yapan en içteki yönteme yazılır.
- **Döngü:** paketin iletim zincirinde aynı düğüme ikinci uğrama.
- **Döngüyü kuran:** döngüdeki her düğümün, o hedef için döngüye girmeden önceki son rota değişikliği.
- **Süre:** kısa pencereli duman sınamasından sonra yazılır, koşudan önce `zaman.txt`'ye.

## Ölçüt

1. **Kimlik:** her hücrenin PDR'si U1'le 4 basamak aynı, korunum geçerli ve TTL düşüşü 1 olmalı (anatomiyle aynı). Tutmazsa iz yorumlanmaz.
2. **TTL ile ölen her paket için** döngüyü kuran değişiklikler sınıflanır. Değişikliği yapan yöntemin kod yolu RFC 3561 ve ns-3 (`aodv-routing-protocol.cc`) ile karşılaştırılır:
   - **Mekanizma:** bütün değişiklikler RFC'nin bir kuralından geliyor. Kurallar:
     - §6.2 komşu rotası (geçerli sırasız);
     - §6.5 ters rota;
     - §6.7 (i)–(iv) RREP güncellemesi (karşılıksız RREP dâhil);
     - §6.11 bağ kopması, RERR ve sıra kopyalama;
     - kabul edilmeyen RREP'in iletilmesi (ns-3 ile aynı; K-205'in kalan döngüleri).
   - **Kusur adayı:** şu üçünden biri.
     - Bayat RREP kabulü (§6.7'nin izin vermediği sırayla güncelleme, K-205'in H-a'sı).
     - Hiçbir RFC kuralının izin vermediği bir değişiklik.
     - Kaydı olmayan bir döngü girdisi ("yok").
3. **Karar:**
   - **Üç paket de mekanizma:** K-207 madde 2'ye göre üç hücre açıklanmış sayılır. `ACIKLANMIS_DUSUK_REFERANS["aodv"]`a ve `KAYITLI_ORAN`a bu ize atıfla girer, yere toplama kaydı `hukum` ile yeniden yargılanır.
   - **Bir paket kusur adayı:** RFC'ye ve ns-3'e göre düzeltilir; yeni K kaydı, U1 ve regresyon gelir. AODV-k donmaz; G1ç, G2ç ve G1-P düzeltmeden sonra koşulur.

Döngülü ama TTL'si tükenmeden çıkan paketler betimleyici olarak sayılır; ölçüte girmez.

## Öngörü (ölçüt değil)

K-205'te `AODV-g` sonrasında kalan döngüler RFC kurallarından geliyordu: `_rrep_isle` + `_ters_rota` ile `_ters_rota`. AODV-k'nin yeni yolu karşılıksız RREP, `_rrep_isle` üzerinden kaynağa doğru rota kurar; döngülerin bir kısmında görünebilir.
