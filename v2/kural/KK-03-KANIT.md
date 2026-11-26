# KK-03 · Karıştırma kanıtı

> **Önceki tasarım (26 Kasım notu):** bu kâğıt 5-3'ün ilk tasarımının kuralıdır (kararları `17`); bugünkü kodun (`protokoller/desparete5*.py`) ve 18–24 Kasım ölçümlerinin belgesi olarak kalır, yeni tasarım donunca arşive gider. Yeni tasarım `18`de, kuralları `bilesen/`de (K-253).

> Kararlar: T-5 · T-6 · T-8 · T-9 · T-10 (`17`). Değerler ve genel kurallar `KK-00`; eşiklerin başlangıcı teşhis (d)'nin dağılımlarından (`arsiv/teshis/faz5_2_isaretler_2026-11-16/sonuc.md`). Kod: A `protokoller/desparete5_kanit.py` · B `desparete5_bag.py`. Güncel: 19 Kasım 2026 (`17` T-2, T-9: askıda durumu kalktı; vazgeçmelerin selamla birlikte okunması; kalabalıkla yanlış alarm riski not edildi). Önceki: 18 Kasım (`v2/arsiv/kural/KK-03-KANIT-2026-11-18.md`; kodlamayla Y-3 · Y-6 · Y-10).
>
> **Kod:** 19 Kasım'da bu kâğıda göre yazıldı. 18 Kasım'ın davranışı `egim` · `vazgecme_tetigi` · `duzgun_gecis` kapalı, `veri_kotu_tetigi` açık ve `DEGERLER_ESKI`yle birebir yeniden üretilir (küçük test dünyasında sekiz koşuda denetlendi: `arsiv/teshis/faz5_3_kod_2026-11-19/esdegerlik.txt`).

## Amaç ve sınıf

Karıştırmayı kötü bağdan ve kalabalık kanaldan ayırmak: kendi durumumu ("karıştırılıyorum") belirlemek ve KK-01'e bağ kanıtı ("karıştırılıyor", sebebiyle) ile "bitti" olaylarını vermek. **Karıştırmaya karşı** (`karistirma_durumu`, `alici_bildirimi`). Açık kurallar, eğitilmiş sınıflandırıcı yok (T-8).

## Gördüğü

- Kendi telsizinin sayaçları (`05` §3.3b): kanal meşgul süresi (`mesgul_sure_s`; protokol `kanal_dolulugu_ister` der) ve çözülen çerçeve sayısı (`alinan_cerceve`).
- Komşu selamları (KK-02) ve KK-01'in sayımı.
- Kendi veri gönderimlerinin sonucu (`iletim_sonucu`).
- Gözlem sözleşmesinde olmayan hiçbir şey: ölçülen gürültü yok (K-227), çerçeve süresi yok, RSSI okunmaz (kural 11).

## Kurallar

**A · Kendi durumum** (saniyelik zamanlayıcıda bir kez)

1. **Büyüklükler:**
   - `m` = son saniyedeki kanal meşgul payı;
   - `c` = son saniyede çözülen çerçeve sayısı;
   - `c̄` = son 30 işaretsiz saniyenin ortalaması (30'dan azsa olanların; hiç yoksa tanımsız);
   - `s` = selam kaybı payı, aşağıdaki sayımla.
2. **`s`'nin sayımı** (protokolün görebildiği veriyle): tanıdık komşu = son 16 s'de en az bir selamı gerçekten alınmış komşu. Her komşu için hiç dondurulmayan bir **gölge geçmiş** tutulur: KK-01 kural 2–3'ün aynısı (zaman aşımı, sıra boşluğu, geri alma), her kayıt olduğu anla. Her tanıdık komşu j için son 4 s'de `gelen_j` = gölgedeki 1'ler, `kacan_j` = gölgedeki 0'lar. Sıra boşluğu da kayıptır: aralık kısalınca kaybolan selamları zaman aşımı eksik sayar, boşluk bir sonraki selamda gösterir; geç gelen selamın geri aldığı 0'lar kayıp sayılmaz (18 Kasım, Y-10). `s = Σ kacan / Σ (gelen + kacan)`. Payda 0 ise `s` tanımsızdır ve girişim işareti çıkmaz. Not: teşhis (d)'deki 0,6 eşiği göndericinin gerçek selam zamanlarıyla (protokolün göremeyeceği bilgi) ve Babel'in 4 s'lik Hello'suyla ölçüldü; buradaki sayım protokolün kendi tahminidir, eşik A/B'de yeniden ayarlanır (`17` §7 madde 7).
3. **İşaretler:** ED işareti `m ≥ ED_ESIGI`. Girişim işareti `c̄` ve `s` tanımlıyken `c < DUSUS_ORANI · c̄` **ve** `s ≥ KAYIP_ESIGI`. "İşaretsiz saniye": iki işaret de yok.
4. **Durum:**
   - "karıştırılıyorum"a giriş: ED işareti 1 saniye ya da girişim işareti `GIRIS_SANIYE` ardışık saniye. Kaynak, girişe yol açan işaretin türüdür. Durum sürerken: ED işareti görülen saniyede kaynak ED'dir; kaynak girişime yalnız ED işaretinin olmadığı bir saniyede geçer. Sebep: ED alanında girişim işaretinin iki koşulu da her saniye sağlanır (çözülen çerçeve düşer, selamlar gelmez); "son görülen" aynı saniyede tanımsız kalır ve kaynak girişime dönerse gönderemediğim hâlde selam kurulur, çıkış da 1 s yerine 3 s sürerdi (18 Kasım, Y-3). Kaynak ED'den girişime geçince gönderebilirim: selam hemen gider (KK-02 kural 5).
   - "bitti": kaynak ED ise 1 işaretsiz saniye (ED eşiğinin yanlış alarmı çok küçük); kaynak girişimse `CIKIS_SANIYE` ardışık işaretsiz saniye.
   - Durum selamın `karistiriliyorum` bitine yazılır (`alici_bildirimi` açıkken; değişimi olaydır, KK-02).

**B · Komşu j'ye bağ kanıtı** (göndericide; bağ OLAĞAN iken)

5. **Bit:** j'nin selamında `karistiriliyorum` = 1 → kanıt, sebep "bit" (alıcı söyledi; `alici_bildirimi` açıkken).
6. **Sessizlik:** j'nin `gecmis`inin sonunda ardışık `k` sıfır → kanıt, sebep "sessizlik". `k = min(N, max(3, ⌈log 0,01 / log(1 − d_r)⌉))`; `d_r` sondaki ardışık sıfırlar hariç hesaplanır (sessizlikten önceki kalite); tanımsızsa `k = N`. Örnekler: `d_r` 0,9 ya da 0,8 → 3; 0,6 → 6; 0,5 → 7; 0,25 ve altı → 16. Anlamı: bağın kendi kayıp oranıyla %1'den düşük olasılıkla açıklanabilecek bir sessizlik. ED'deki j gönderemez; sessizliği kanıttır (T-6). Ölen ya da uzaklaşan j de böyle görünür; zararı yok, bağ kullanılmaz ve `T_SILME`'de silinir.
7. **MAC:** j'ye `MAC_ARDISIK` ardışık vazgeçme **ve** j'den son `2·a` içinde selam yok → kanıt, sebep "sessizlik". Vazgeçme tek başına kanıt değildir (T-9; teşhis (d)'de tek başına geç ve seyrekti). Selam geliyorken vazgeçmeler bu kurala değil vazgeçme tetiğine gider: bağ veriyi taşıyamıyordur (KK-01 kural 7, 15).
8. **Kendim karıştırılırken** MAC sonuçları bağ kanıtı sayılmaz, vazgeçme kaydına da girmez (KK-01 kural 6, 13); ardıl korunur. Üst süresi KK-01 kural 13'ündür (30 s; 18 Kasım, Y-6). Sebep: bütün komşulara başarısızlık gönderenin kendisini gösterir (T-6); veri çerçevesi alandan dışarıdaki ardıla çoğu zaman ulaşır, onayı ise ben duyamam; yedeğe geçmek bir şey kazandırmaz (17 Kasım, denetim B-11; `17` T-9).
9. **Bitti, sebebe göre:**

| sebep | o sebebin "bitti"si |
|---|---|
| bit | j'den `karistiriliyorum` = 0 olan 2 ardışık selam (varış sırasıyla) |
| sessizlik | j'den 2 ardışık selam (varış sırasıyla), ikisi de bit = 0; bit = 1 gelirse "bit" sebebi kümeye eklenir |

   Kümedeki bütün sebeplerin "bitti"si gelince KK-01'e "bitti" verilir. "Kendi" sebebi yoktur (kural 8): kendi karıştırılmam bağları değiştirmez.

**C · Sınırlar**

10. Bütün eşikler başlangıçtır; birleşik kuralın başarısı ve yanlış alarmı A/B'de ölçülür (`17` §7 madde 6–7).
11. Sinyal tutarlılığı (RSSI) başlangıç kuralına girmez: teşhis (d)'de zayıftı (AUC 0,71). Protokol bu sürümde RSSI okumaz; A/B'de denenirse ölçüm hatasının (σ 2 dB) duyarlılığı da ölçülür (`04` §9).
12. **Bilinen risk: kalabalık** (19 Kasım; açlık teşhisi). Kalabalık kanalda yayın selamları çarpışıp kayboluyor: kâhine göre iyi olan bağlarda selamla ölçülen `d_f · d_r` ~0,23 (kâhinin tek deneme başarısı ~0,71–0,76). Kural 2'nin `s`'si ve kural 6'nın sessizliği selam kaybına dayandığı için karıştırıcı yokken de yanlış alarm verebilir (küçük test dünyasında karıştırıcısız koşuda birkaç sessizlik kanıtı görüldü; Xu vd. 2005 ve Puñal 2014'ün uyarısı [23]). Düzeltme, karıştırma katmanının A/B'lerinden önce yazılır (`v2/12`); aday: sessizlikte "selam gelmedi" yerine "hiçbir çerçevesi duyulmadı".

## Örnek

Girişim alanındaki bir düğüm saniyede ortalama 99 çerçeve çözüyordu (`c̄`). Karıştırıcı açılınca 45 çözüyor (< 0,5 × 99) ve tanıdık komşularından beklediği selamların %70'i gelmiyor (≥ 0,6). İki saniye üst üste böyle olunca "karıştırılıyorum" der, bunu hemen bir selamla bildirir ve kendi ölçümlerini dondurur. Bu sırada kendi gönderimleri onay alamasa da ardılını değiştirmez. Ona veri gönderen komşu selamdaki biti görünce bu bağı KARIŞTIRILIYOR'a alır ve hazır yedeğe geçer (KK-04). Karıştırıcı susunca üç işaretsiz saniye geçer, bit 0'a döner; komşular iki temiz selamdan sonra bağı hatırlanan ETX'le geri alır.

## Sınanması

- `karistirma_durumu` açık ↔ kapalı: birincil ve dayanıklılık hücresinde `PDR_açık`; ikizde zarar yok (yanlış alarmın bedeli). Mekanizma kapısına girer (`06` §0.4.5; `KK-00`).
- `alici_bildirimi` açık ↔ kapalı: kural 5'in payı.
- Tanı kaydı: yanlış alarm (ikizde "karıştırılıyorum" denen düğüm-saniye) · tespit süresi (açılmadan karara kadar) · girişim kaynaklı durumun bir açık dönemdeki geçiş sayısı (denetim S-4).

## Kaynak

İşaretler ve en uzun boşluk Puñal 2014 [23]; komşularla birleştirme [23]; karıştırılan bölgenin etrafından dolaşma [59]; ardışık olay eşiği, kendi ortalamasına göre düşüş ve sebebe göre bitiş bu tasarımın (teşhis (d)'nin ölçümüyle).
