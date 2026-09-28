# 03 · YÖNTEM — ilkeler ve bilinen tuzaklar

> Bir pusula, kural listesi değil: bir ilke bir durumda yanlış görünüyorsa gerekçesine bakılır, durum ölçülür, sonuç karar günlüğüne yazılır. Çalışma anlaşmaları (git, dil, uzun koşu vb.) `DEVIR-PROMPT.md` §2'de. Güncel: 28 Eylül 2026; önceki sürüm `arsiv/03-YONTEM-KURALLARI-2026-09-28-temizlik.md`.

## 1 · Bilimsel ilkeler

| ilke | neden |
|---|---|
| **Ölçülmemiş bir şey ölçülmüş gibi sunulmaz;** sayı üretici komutuyla yazılır | kod değişince sayı sessizce bayatlar |
| **Sonuç çok tohumla verilir:** ana deney 40 tohum + güven aralığı; yeterliliği güç analiziyle | tohumlar arası yayılım çoğu etkiden büyüktür |
| **Negatif sonuç gizlenmez;** bir eşik sonuç görüldükten sonra gevşetilmez. Ölçüt sınanamaz çıkarsa tarihiyle düzeltilir, eskisi silinmez | ön-kayıtlı bir koşulun değeri, tetiklendiğinde ona uyulmasıdır |
| **Rakip protokol kaynağına sadık kurulur;** hiçbir kol — kendi protokolümüz dâhil — senaryoya göre ayarlanmaz | senaryo başına ayar kâhinliktir; sadakat denetlenebilir |
| **Kâhin bilgisi karara girmez:** simülatörün bilip gerçek telsizin ölçemeyeceği hiçbir şey protokole ulaşmaz | bunu gören bir jüri üyesi bütün sonuçları geçersiz sayar |
| **Özgünlük iddiası kod ve ablasyon koluyla** gösterilir | tasarlanmış ama uygulanmamış bir özellik iddia edilemez |
| **Beklenmeyen sonuçta önce sebep ölçülür;** parametre oynatılıp sonuç tutturulmaz | literatürden hikâye uydurmak kurulumu denetlemekten kolaydır |
| **Durum tutan her bileşende başlangıç koşulu sorulur** | ısınma hataları bu alanın en sinsi sınıfıdır |
| **Derin öğrenme kullanılmaz** (öğrenci) | SWaP kısıtı; tablo tabanlı öğrenme serbest |

## 2 · İşe yarayan düşünme alışkanlıkları

- Bir ölçüm aletine, ölçtüğü şeye güvendiğinden daha az güven — bulunan kusurların çoğu modelde değil aletlerdeydi.
- Tabloda değişmeyen sütuna bak: 20 dB güç farkına rağmen aynı çıkan satırlar kapalı bir karıştırıcıyı ölçüyordu.
- "Ölçtüm, etkisi yok" ile "hesaba hiç girmedi" ayrıdır.
- Gürültü üreten kapı bozuktur; doğru işi kırmızıya boyayan bir kapı kapıyı görmezden gelmeyi öğretir.
- Bir kapının "X yapmaz" sonucunu sınarken X'e bağlı kapıları da sor.
- Kısa pencere zamanla biriken etkiyi göremez; profil kararları uzun pencerede verilir.
- Ölçeklenen bir dünyada her sabitin birimini sor (gölgeleme hücresi ölçeklenmemişti, K-188).
- Tek tohumlu küçük farklar yörünge gürültüsüdür; bir mekanizmanın bedeli aynı tohumlarda eşli A/B ile, birden çok tohumla ölçülür.
- Öğrencinin verdiği sayılar yaklaşıktır, cevabı ölçüm verir; kapsam ve gerçekçilik kararları ise öğrencinindir.

## 3 · Bilinen tuzaklar

**Ölçüm tasarımı.** Kontrol kolu olmadan etki ölçmek · "mekanizma çalışıyor" ile "mekanizma bilgi taşıyor"u karıştırmak (bilgi taşımayan bir boş model kurulur) · bir ayarın iyileşmeyi mekanizmayı kapatarak üretmesi · ablasyon kolunu kod düzenleyerek üretmek (kol bir yapılandırma bayrağıdır) · mekanizma kapısını atlayıp sonuca bakmak.

**İstatistik.** Eşleştirmeyi yok saymak (aynı tohum = aynı senaryo) · tek yönlü test (ters yöndeki bulguyu göremez) · aile içinde çoklu karşılaştırma düzeltmesi yapmamak (Holm) · `scipy.stats.wilcoxon`un bütün farklar sıfırken NaN döndürüp Holm'dan sonra bütün p'leri 1 yapması · "p > 0,05"i "etki yok" sanmak (negatif sonucun gücü dışladığı etki büyüklüğündedir) · sınırda çöken hata payı (Wald SE p = 1'de sıfır → Agresti–Caffo) · çok pencereli taramada yanlış alarm birikmesi · kayıpların zamanda kümelenmesini yok sayan hata payı (K-196).

**Metrikler.** Tek metrikle sıralama (teslim · gecikme · kontrol yükü birlikte) · gecikmede seçilim yanlılığı (ortak alt küme, kesişim oranı yazılır) · ölçüm penceresini koşu uzunluğuyla eşitlemek · bulguyu çalışma noktası yazmadan vermek · kontrol yükünü paketle saymak (bayt ve kanal süresi) · bir kâhini kesin tavan sanmak.

**Teşhis.** Bir kusuru ölçmek onu sebep yapmaz (nedensel kol kurulur) · kusurların birbirini dengelediğini görmemek · ders kitabı düzeltmesinin bağlayıcı kısıt başka yerdeyken zarar vermesi · ablasyona yalnız sonucu sormak (mekanizmayı da sor) · neyi eleyeceği önceden söylenemeyen deneyi koşmak.

**Kod ve belge.** Bildirilen bir şeyin gerçekten kullanıldığını sınamamak · yorumun kodla çelişmesi (kod belgenin kanıtıdır) · yargıyı elle yazmak (yargı veriden çıkar) · göreli dosya yolu · uzun koşuda ara kayıt tutmamak · aynı kuralı iki yerde yazmak.

**Kurulum.** Kod doğru, testler geçiyor, kurulum yanlış (tarama sessizce başka şeyi ölçer) · periyodik iki sürecin aynı fazda kilitlenmesi · ölçüm anında kapalı bir mekanizmayı ölçmek (ön koşul kapıyla sınanır) · sahte bir bileşenin ölçüleni yutması.

## 4 · Simülatörün doğrulama seviyeleri

1 analitik (yol kaybı, gürültü, çerçeve süreleri, sönümleme momentleri, Bianchi) · 2 korunum (hiçbir paket sessizce kaybolmaz; her koşuda) · 3 iç tutarlılık (uç durumlar; aynı tohum → birebir aynı sonuç) · 4 literatür replikasyonu (Li vd. zincir kapasitesi, `09`). Dördüncüsü "öğrenci bir simülasyon yazdı"yı "öğrenci bir araştırma aleti geliştirdi ve doğruladı"ya taşır.
