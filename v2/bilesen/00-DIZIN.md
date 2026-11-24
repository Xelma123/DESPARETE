# Bileşen kâğıtları — dizin, değerler, bayraklar, gözlemin kullanımı

> Yeni tasarımın (`../18-YENI-TASARIM.md`) kural kâğıtları: bileşen başına bir kâğıt. Bileşenin sorunu, kanıtı, seçenekleri ve kararım `18`'in "Bileşenler" bölümünde; kuralları kâğıdında. Değerler, bayraklar ve gözlemin kullanımı **yalnız bu dosyada** tutulur; kâğıtlar adlarıyla anar (`18` bütünlük listesi madde 1). Kod Aşama 4'te bu kâğıtlardan yazılır. Önceki tasarımın kâğıtları `../kural/KK-*`; yeni tasarım donana kadar bugünkü kodun belgesidir. Güncel: 24 Kasım 2026 (B1).

## Kâğıtlar

| # | bileşen | kâğıt | durum |
|---|---|---|---|
| B1 | komşu ve bağın ölçüsü | `B1-KOMSU-VE-BAG.md` | onaylandı (24 Kasım) |
| B2 | karıştırma kanıtı | — | sırada |
| B3 | bağın durumu | — | bekliyor |
| B4 | yol | — | bekliyor |
| B5 | iletim kararı | — | bekliyor |
| B6 | kontrol iletileri | — | bekliyor |
| B7 | bekletme ve komut | — | bekliyor |

## Ortak birimler

- **Süre:** saniye, düğümün kendi saatiyle (`saat_s`); saatler senkron değildir, yalnız süreler kullanılır (`05` §3.2).
- **Sıra numarası:** 16 bit, modüler karşılaştırılır: fark = (yeni − eski) mod 2^16, [−32768, 32767] aralığına çevrilir.
- **Bağın ölçüleri (B1):** gerçek sayı; birimi beklenen deneme sayısı (ETX). Maliyetin tamsayı birimi ve ilan biçimi B3, B4 ve B6'da yazılır.

## Değerler (tek yer)

Her değer için: kuralı, kaynağı ve gerekçesi, küçük ve büyük olursa ne olacağı, sonra taranıp taranmayacağı (`18` yöntem). Değerler başlangıçtır; hiçbiri tek bir karıştırıcı çizelgesine göre seçilmez (`17` İlke 3).

| ad | değer | kural | kaynak ve gerekçe | küçük olursa · büyük olursa | taranır mı |
|---|---|---|---|---|---|
| `N_SELAM` | 16 örnek | B1/11 | Babel'in Hello geçmişi (RFC 8966 Ek A.1); önceki tasarımın `N`'i | oran gürültülü olur (16 örnekte bir örnek oranı 0,06 oynatır, 8'de 0,13) · bağın değişimine geç tepki (2,2 s aralıkta 16 örnek ~35 s) | ilk ölçümde hayır; B2'nin sessizlik kanıtı buna bağlıysa B2'de yeniden bakılır |
| `SELAM_SAKLA` | 128 örnek | B1/6 | hariç aralık önceki tasarımda en çok 30 s sürüyordu (`T_HATIRA`); iki selam arası en az 0,5 s olduğundan (B1 Ö-4) bu sürede en çok ~60 örnek oluşur; öncesinin `N_SELAM` örneği de kalsın diye en az 76; iki kat payla 128. B3 bu süreyi değiştirirse yeniden hesaplanır | uzun hariç aralıktan sonra karıştırmadan önceki kalite kaybolur · bellek (düğüm başına en çok 255 × 128 örnek) | hayır |
| `ZAMAN_ASIMI_KATSAYI` | 1,5 × `a` | B1/4–5 | Babel (RFC 8966 Ek A.1: titreşim payı; `protokoller/babel_bicim.py`); önceki tasarımın `ZAMAN_ASIMI` | titreşimle geç gelen selam önce kayıp sayılır, geri alma düzeltir ama arada ölçü düşük görünür · kayıp ve sessizlik geç görülür | hayır |
| `ARALIK_EN_AZ` | 0,01 s | B1/4 | selamın aralık alanının birimi (önceki biçim); 0 aralık zaman aşımını sonsuz döngüye sokardı | yalnız bozuk girdiye karşı koruma | hayır |
| `BOSLUK_EN_COK` | 64 selam | B1/4 | Babel'de sınır geçmişinin boyudur (16; RFC 8966 Ek A.1); burada saklama 128 örnek. Sınır, kayıt silinmeden (`T_SILME`, 30 s) önce oluşabilecek en büyük farka göre seçildi: bu sürede en çok ~60 selam kaçabilir (iki selam arası ≥ 0,5 s) ve zaman aşımı en çok ~55 sıfır sayabilir (en kısa ilan edilen aralık 0,55 s). Daha büyük fark ancak yeniden başlamayla oluşur. Etkisi susan ama henüz silinmeyen komşuda görülür; simülatörde bu, kanal kilidindeki komşudur (B1 §10, §12) | uzun sessizlikten sonra geçmiş silinir, öncesinin kalitesi kaybolur · gerçek yeniden başlama geç tanınır (simülatörde düğüm yeniden başlamaz) | hayır |
| `ORNEK_EN_AZ` | 4 örnek | B1/17 | önceki tasarım (KK-02, Y-12): tek örnekle 1,0 bildirilmesin | ilk selamlarda aşırı iyimser oran (1/1 = 1,0) bildirilir · yeni komşu geç ölçülür (en kısa aralıkta 4 selam ~2 s) | hayır |
| `DF_UNUT_S` | 30 s | B1/12 | önceki tasarım (KK-01, Y-12); `T_SILME`'ye eşit | komşunun listesinden geçici düştüğümde `d_f` gereksiz tanımsız olur · bayat `d_f` kullanılır | hayır |
| `T_SILME` | 30 s | B1/3 | `17` İlke 2: birincilde 15 s, dayanıklılıkta 10 s'lik açık dönemde komşu silinmesin; önceki tasarımın `T_SILME`'si | karıştırma sırasında komşular silinir ve yeniden öğrenilir · ölü komşu kayıtta ve selam listesinde kalır | hayır; daha uzun açık dönemli sınıflarda tanıda bakılır |
| `VERI_PENCERE` · `VERI_PENCERE_S` | 16 kayıt · 30 s | B1/14 | önceki vazgeçme penceresi (KK-00, 19 Kasım): saniyede bir telemetri gönderen uç düğümde 16 çerçeve ~16 s; 30 s bayat kaydı atar | `E_veri` gürültülü olur (16 kayıtta ~30 deneme) · bayat ve yavaş olur | B3'ün veri kuralıyla birlikte; karar B3'te |
| `VERI_SAKLA` | 64 kayıt | B1/9 | 4 × `VERI_PENCERE`; yalnız bellek sınırı | hariç aralıktan sonra veri penceresi boş kalabilir · bellek | hayır |

## Bayraklar ve sınıflar

Her mekanizmanın bayrağı, sınıfı (karıştırmaya karşı ya da genel; K-247) ve kapalıyken davranışı burada yazılır. Karıştırmaya karşı olanlar tek bir bayrak grubuyla birlikte kapanabilir (`18` §1.4 sözleşme 7).

| mekanizma | bileşen · kural | bayrak | sınıf | kapalıyken |
|---|---|---|---|---|
| komşu kaydı, selam sayımı, veri kaydı, ölçüler | B1 | yok (çekirdek) | genel | — (selam olmadan komşu ve bağ bilinemez; ölçmek davranışı değiştirmez, ölçünün kullanımının bayrağı kullanan bileşendedir, B1 §10) |

## Gözlemin kullanımı (`05`; mimari denetimi D17)

| bileşen | okur | okumaz |
|---|---|---|
| B1 | selam: göndereni, sırası, aralığı, benim için bildirilen oran (B6 çözer) · `iletim_sonucu`: hedef, başarı, `tekrar` (ölçüye yalnız tür `veri`; onayın gelmesi her türde varlık kanıtı) · `cerceve_duyuldu`: göndereni, yalnız tür `veri` ve `kontrol` · `saat_s` (yalnız süreler) | `olculen_gurultu_w` (yasak, K-227) · RSSI · `phy_hata` · `alinan_cerceve` · `mesgul_sure_s` · `kendi_konum` · `kendi_hiz` · `komsular` (simülatörün beacon listesi) · kuyruk · duyulan onay ve kontrol onayının göndereni (gerçek 802.11 onayı verici adresi taşımaz) |

## Aşama 3'e açık kalanlar

- **Olay sırası:** B1, bir gözlemi işlemeden önce o ana kadarki kendi zaman olaylarını işler (B1 kural 20); `18` §1.4'ün olay sırasında gözlemin dağıtımı (1) zaman olaylarından (2) önce yazılı. Bütün bileşenler için ortak kural bütünlük denetiminde yazılır.
- **Bileşenler arası beklentiler:** B1'in B6'dan beklentileri (B1 §6, Ö-1…Ö-7); B3 ile B6 arasında komşulara hangi oranın bildirileceği (B1 §11 madde 3).
