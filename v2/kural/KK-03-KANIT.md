# KK-03 · Karıştırma kanıtı

> Kararlar: T-5 · T-6 · T-8 · T-10 (`17`). Değerler `KK-00`; eşiklerin başlangıcı teşhis (d)'nin dağılımlarından (`arsiv/teshis/faz5_2_isaretler_2026-11-16/sonuc.md`). Güncel: 17 Kasım 2026.

## Amaç ve sınıf

Karıştırmayı kötü bağdan ve kalabalık kanaldan ayırıp KK-01'e "karıştırılıyor" ve "bitti" olaylarını vermek. **Karıştırmaya karşı** (bayraklar `karistirma_durumu`, `alici_bildirimi`). Açık kurallar, eğitilmiş sınıflandırıcı yok (T-8).

## Gördüğü

- Kendi telsizinin sayaçları (`05` §3.3b): kanal meşgul süresi (`mesgul_sure_s`; protokol `kanal_dolulugu_ister` der), çözülen çerçeve sayısı (`alinan_cerceve`).
- Komşu selamları (KK-02) ve KK-01'in beklenen selam sayımı.
- Kendi tek alıcılı gönderimlerinin sonucu (`iletim_sonucu`).
- Gözlem sözleşmesinde olmayan hiçbir şey: ölçülen gürültü yok (K-227), çerçeve süresi yok (E-1).

## Kurallar

**A · Kendi durumum (her saniye bir kez):**
1. `m` = son saniyedeki kanal meşgul payı; `c` = son saniyede çözülen çerçeve; `c̄` = işaretsiz saniyelerin son 30 s ortalaması; `s` = son 4 s'de tanıdık komşulardan (son 16 s'de selamı duyulan) beklenen selamların kaçırılan payı.
2. **ED işareti:** `m ≥ ED_ESIGI`. Bir saniye yeter: ikizde yanlış alarm %0,035.
3. **Girişim işareti:** `c < DUSUS_ORANI · c̄` **ve** `s ≥ KAYIP_ESIGI`. Tek başına her biri yanlış alarm veriyor (teşhis (d): %50 yakalamada %6–11); ikisi birlikte ve düğümün kendi ortalamasına göre okunur. Çözülen çerçeve düşüşü uzaktaki düğümde de olduğu için selam kaybı şartı onu ayırır.
4. **Karar:** ED işareti 1 saniye ya da girişim işareti `GIRIS_SANIYE` ardışık saniye → "karıştırılıyorum". `CIKIS_SANIYE` ardışık işaretsiz saniye → "bitti". Bu durum selamın `karistiriliyorum` bitine yazılır (değişim olayı, KK-02).

**B · Komşu j'ye bağım (j OLAĞAN iken; göndericide):**
5. j'nin selamında `karistiriliyorum` = 1 → "karıştırılıyor" (alıcı söyledi).
6. j'den `SESSIZ_SELAM` ardışık beklenen selam gelmedi (j'nin ilan ettiği aralıkla) → "karıştırılıyor". ED'deki j gönderemez; sessizliği kanıttır (T-6). Ölen ya da uzaklaşan j de böyle görünür; zararı yok, bağ kullanılmaz ve `T_SILME`'de silinir.
7. j'ye `MAC_ARDISIK` ardışık vazgeçme **ve** (j'den son 2 aralıkta selam yok ya da kendi girişim işaretim var) → "karıştırılıyor". Vazgeçme tek başına karar değildir (T-9); teşhis (d)'de tek başına geç ve seyrekti.
8. **Bitti:** j'den `karistiriliyorum` = 0 olan 2 ardışık selam → "bitti" (KK-01 hatırayla döner).

**C · Sınırlar:**
9. Sinyal tutarlılığı (RSSI) başlangıç kuralına girmez: teşhis (d)'de zayıftı (AUC 0,71). A/B'de birlikte denenebilir.
10. Bütün eşikler başlangıçtır; birleşik kuralın başarısı ve yanlış alarmı A/B'de ölçülür (`17` §7 madde 6–7).

## Örnek

Girişim alanındaki bir düğüm saniyede ortalama 99 çerçeve çözüyordu (`c̄`). Karıştırıcı açılınca 45 çözüyor (< 0,5 × 99) ve tanıdık komşularından beklediği selamların %70'i gelmiyor (≥ 0,6). İki saniye üst üste böyle olunca "karıştırılıyorum" der ve bunu bir sonraki selamında bildirir. Ona veri gönderen komşu, selamı görünce bu bağı KARIŞTIRILIYOR'a alır ve hazır yedeğe geçer (KK-04). Karıştırıcı susunca üç saniye işaretsiz geçer, bit 0'a döner, komşular iki temiz selamdan sonra bağı hatırlanan ETX'le geri alır.

## Sınanması

- `karistirma_durumu` açık ↔ kapalı: birincil ve dayanıklılık hücresinde `PDR_açık`; ikizde zarar yok (yanlış alarmın bedeli). Mekanizma kapısına girer (`06` §0.4.5).
- `alici_bildirimi` açık ↔ kapalı: kural B5'in payı.
- Tanı kaydı: yanlış alarm (ikizde "karıştırılıyorum" denen düğüm-saniye) ve tespit süresi (açılmadan kararın verilmesine kadar).

## Kaynak

İşaretler ve en uzun boşluk Puñal 2014 [23]; komşularla birleştirme [23]; karıştırılan bölgenin etrafından dolaşma [59]; ardışık olay eşiği ve kendi ortalamasına göre düşüş bu tasarımın (teşhis (d)'nin ölçümüyle).
