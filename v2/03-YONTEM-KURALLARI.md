# 03 · YÖNTEM — ilkeler ve bu projede görülen hata sınıfları

> Bir ilke bir durumda yanlış görünüyorsa gerekçesine bakılır, durum ölçülür, sonuç karar günlüğüne yazılır. Güncel: 13 Ekim 2026; önceki sürümler `arsiv/03-YONTEM-KURALLARI-*.md` (koddaki `03` §B5, §2.1 gibi eski bölüm atıfları oradadır).

## 1 · Bilimsel ilkeler

| ilke | gerekçe |
|---|---|
| **Belge ve kod yorumu kanıt değildir.** Bir iddia kodla, ölçümle ya da birincil kaynakla doğrulanana kadar varsayımdır; belge ile kod çelişirse hangisinin yanlış olduğu ölçülerek bulunur | belgeler ve yorumlar kod değiştikçe bayatlar |
| **Ölçülmemiş bir şey ölçülmüş gibi sunulmaz;** her sayı üretici komutuyla yazılır | kod değişince sayı sessizce bayatlar |
| **Sonuç çok tohumla verilir:** ana deney 40 tohum + güven aralığı; yeterliliği güç analiziyle | tohumlar arası yayılım çoğu etkiden büyüktür |
| **Negatif sonuç raporlanır;** bir eşik sonuç görüldükten sonra gevşetilmez. Ölçüt sınanamaz çıkarsa tarihiyle düzeltilir, eskisi silinmez (`06` §10) | ön-kayıtlı koşul ancak tetiklendiğinde uyulursa anlam taşır |
| **Rakip protokol kaynağına sadık kurulur;** hiçbir kol (DESPARETE dâhil) senaryoya göre ayarlanmaz | senaryo başına ayar kâhin bilgisidir; sadakat denetlenebilir |
| **Kâhin bilgisi karara girmez:** simülatörün bilip gerçek telsizin ölçemeyeceği hiçbir şey protokole ulaşmaz (`05`) | aksi hâlde karşılaştırma geçersizdir |
| **Özgünlük iddiası kod ve ablasyon koluyla** gösterilir | uygulanmamış bir özellik iddia edilemez |
| **Beklenmeyen sonuçta önce sebep ölçülür;** parametre oynatılıp sonuç tutturulmaz | açıklama ölçümle kurulur, varsayımla değil |
| **Durum tutan her bileşende başlangıç koşulu sorulur** | ısınma ve başlangıç hataları bu projede birden çok kez görüldü (K-215) |

## 2 · Bu projede görülen hata sınıfları ve karşılıkları

- **Alet kusuru:** bulunan kusurların çoğu modelde değil ölçüm aletlerindeydi. Yeni bir alet önce cevabı bilinen bir durumla sınanır.
- **Değişmeyen sütun:** 20 dB güç farkına rağmen aynı çıkan satırlar kapalı bir karıştırıcıyı ölçüyordu. Değişmesi beklenip değişmeyen bir değer incelenir.
- **"Etkisi yok" ile "hesaba girmedi" farklıdır:** bir anahtarın etkisizliği, anahtarın devrede olduğu kanıtlanmadan söylenmez.
- **Tek tohum ve kısa pencere:** kısa pencerede (30 s) tek tohumun PDR'si ±0,15 oynar (K-224). Mekanizma bedeli aynı tohumlarda eşli A/B ile, birden çok tohumla ölçülür.
- **Yanlış dünya:** `Konfig()` varsayılanı eski 1:50 dünyadır; referans dünya açıkça seçilmezse kod doğru, testler geçerken ölçüm başka şeyi ölçer (`04` §2).
- **Ölçeklenen sabit:** dünya ölçeklenince her sabitin birimi sorgulanır (gölgeleme hücresi ölçeklenmemişti, K-188).
- **Kümelenen kayıp:** gerçek protokolde kayıp ve kopma beyanı zamanda kümelenir; hata payı kümelenmeye dayanıklı kurulur (K-196).
- **Kâhin tavan değildir:** ETX kâhini bazı hücrelerde aşılabilir; aşım önce zarf ve kopya kurallarıyla açıklanır, açıklanamazsa sızıntı ya da hata aranır (K-192, K-238).
- **Uzun gecikmeli protokolde evre atfı bulanıklaşır:** paketin doğduğu evre ile teslim edildiği evre ayrışır; trafik ölçüm sonunda durduğu için son doğumlar boşalan ağda teslim edilir (K-239).
- **Aynı kural iki yerde:** bir kural ya da sayı tek yerde yazılır; ikinci kopya bir gün ayrışır.

## 3 · Mekanizma ölçümünde (Faz 5)

- Etki kontrol koluyla ölçülür; ablasyon kolu kod düzenleyerek değil, yapılandırma bayrağıyla üretilir.
- "Mekanizma çalışıyor" ile "mekanizma bilgi taşıyor" ayrı sorulardır; ikincisi bilgi taşımayan bir boş modelle sınanır.
- Bir ayar iyileşmeyi mekanizmayı kapatarak üretebilir; ablasyona yalnız sonuç değil mekanizmanın sayaçları da sorulur.
- Ölçüm anında mekanizmanın devrede olduğu bir ön koşul kapısıyla sınanır.
- Neyi eleyeceği önceden yazılamayan bir deney koşulmaz; ölçüt ölçümden önce yazılır (`06` §7).

## 4 · Simülatörün doğrulama seviyeleri

| seviye | içerik |
|---|---|
| 1 analitik | yol kaybı · gürültü · çerçeve süreleri · sönümleme momentleri · Bianchi |
| 2 korunum | hiçbir paket sessizce kaybolmaz; her koşuda denetlenir |
| 3 iç tutarlılık | uç durumlar; aynı tohum → birebir aynı sonuç |
| 4 literatür replikasyonu | Li vd. zincir kapasitesi (`09`) |

Dördüncü seviye, simülatörün yayımlanmış bir sonucu yeniden üretebildiğini gösterir.
