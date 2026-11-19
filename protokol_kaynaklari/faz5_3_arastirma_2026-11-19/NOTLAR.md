# Faz 5-3 · Araştırma notları — yol seçimi, bağın ölçüsü ve karıştırma katmanı

> 19 Kasım 2026 · 5-2'nin notlarının devamı (`../faz5_arastirma_2026-10-21/NOTLAR.md`); orada geçen kaynaklar burada yinelenmez, yalnız yeni bir şey söylüyorsa anılır.
> **Sebep:**
> - Açlık teşhisi (`arsiv/teshis/faz5_3_aclik_2026-11-18/sonuc.md`).
> - Küçük test dünyasında görülen bir gözlem (§0).
> - Yol seçimini daha uyarlanır bulmak ve karıştırma katmanını geliştirmek istiyorum.
>
> **Bu notlarda tasarım kararı verilmez;** seçenekler kararlarımın girdisidir.
> İşaretler: ✓ ilgili bölüm okundu · ↪ yalnız özetinden ya da arama sonucundan biliniyor · ○ açılmadı.
> Okunan iki makalenin (4B, CTP) dosyaları bu klasörde; künye, SHA-256 ve denetimler `protokol_kaynaklari/README.md`de.

---

## 0 · Dayanak: bizim ölçtüklerimiz

- **Açlık teşhisi (ikiz, 8 tohum):**
  - Rota yokluğu kaybının %99'u, veri tetiğinin ardıl bağını kullanımdan çıkarmasıyla başlıyor.
  - Çıkarılan ardıl bağlarının %99,7'si o anda kâhine göre iyi.
  - Tetik kapalıyken pencere PDR'si 0,810 → 0,946; iletim kaybı 0,049 → 0,052.
- **Küçük test dünyası** (12 düğüm, durağan, karıştırıcısız, tek tohum; ölçüm değil; 19 Kasım):
  - Tetik kapalıyken bir düğüm, selamı iyi geçen ama veriyi taşıyamayan bir bağı ardıl seçiyor ve bırakmıyor.
  - Tam sürümde iletim kaybı 10 → 75 paket, teslim 818 → 752 / 839. Çekirdekte 817 → 801.

  Tetiğin gerçek bir işlevi var: "selam geçiyor, veri geçmiyor" bağını yakalamak. Bu, ETX makalesinin bilinen uyarısıdır (5-2 notları §2). Referans ikizde ise zararı faydasından çok büyük.
- **Selam bağı olduğundan kötü gösteriyor:** selam eşiğiyle çıkan bağlarda, çıkış anında selamın ölçtüğü `d_f · d_r` ~0,23; kâhinin tek deneme başarısı ~0,71–0,76 (girişim hariç; açlık teşhisinin `ek_hesap.txt`'i).

**Sonuç:** Selam tek başına bağı kötü, veri tek başına (tetik olarak) bağı aşırı sert ölçüyor. İkisinin birleşimi ve bu birleşimin yol seçimine nasıl gireceği asıl soru.

---

## 1 · Yol seçimi: iki aile

| | **Babel / DSDV ailesi** (bugünkü tasarım, T-12, T-13) | **Eğim ailesi** (CTP, RPL) |
|---|---|---|
| döngü | hiç olmaz: komşunun ilanı ya daha yeni turdan ya FD'den küçük olmalı | olabilir; veri yolunda yakalanır ve onarılır |
| ardıl gidince | uygun yedek yoksa açlık: ∞ ilanı, tur isteği, yeni tur beklenir | maliyeti benimkinden küçük herhangi bir komşu seçilir; açlık yok |
| bedel | açlık bölümleri (teşhiste kaybın kaynağı); tur artışı | geçici döngüler; veri başlığında maliyet alanı |
| kaynak | RFC 8966 · 5-2 notları §5 | CTP (aşağıda) · RFC 6550 §3.7 (5-2 notları §5) |

**CTP** ✓ [Gnawali vd. 2009, SenSys; §3.1, §3.2, §4.1, §4.3, §5]:
- **Maliyet:** bağın ETX'i + ebeveynin maliyeti; toplama noktası 0 ilan eder.
- **Ebeveyn değişimi:** histerezisle, ancak öteki yol en az **1,5 ETX** daha iyiyse (§4.1).
- **Veri yolunda doğrulama** (§3.1, §4.3):
  - Her veri paketi gönderenin maliyetini taşır.
  - Gönderenin maliyeti alanınkinden büyük değilse topoloji bayattır ve döngü olabilir.
  - Paket **düşürülmez**. Kısa bir bekleme (en küçük selam aralığı) yapılır ve önce selam gönderilir. Bayat düğüm yolunu düzeltir.
  - Yazarlar, seyrek geçici döngülerin bedelini genel iletim bedeline göre küçük buluyor.
- **Uyarlanır selam** (Trickle; §3.2, §4.3):
  - Aralık 64 ms ile 1 saat arası; her dolumda iki katına çıkar.
  - En küçüğe üç olayda döner:
    - döngü işareti;
    - maliyetin 1,5 ETX'ten fazla düşmesi;
    - komşunun "çek" (P) biti. Yolu olmayan düğüm bu biti koyar ve komşularından selam ister.
- **İletim** (§5): paket başına **32 yeniden denemeye** kadar. Düşürmek yerine bekleme ile topolojinin onarımını birleştirir; tek hedef olduğundan sıradaki paketin sonucu da aynı olurdu.
- **Ölçek** (§1): 12 deney ağı, 20–310 düğüm, yedi donanım; yazarların deyişiyle sahada değil, laboratuvar deney ağları. Hareketlilik yok.

**Babel'in yol seçimi** ✓ [RFC 8966 Ek A.3, depoda]:
- Her rota için anlık maliyet ve düzgünleştirilmiş maliyet tutulur. Düzgünleştirmenin zaman sabiti selam aralığının ~3 katıdır.
- Seçili rotadan ancak **ikisi birden** daha iyiyse ayrılınır.
- Seçili rota yoksa en küçük anlık maliyetli seçilir.
- Ek B: kopuş 1,5–3,5 selam aralığında fark edilir; önerilen selam aralığı 4 s.

**MRHOF** (5-2 notları §6): eşik 1,5 ETX.

**Bizim bugünkü kuralımız:**
- %10 oransal eşik (T-11, Ramachandran);
- düzgünleştirme yok;
- FD katı;
- KÖTÜ bağ hiç aday değil.

---

## 2 · Bağın ölçüsü: selam ve veri birlikte

**4B tahmincisi** ✓ [Fonseca vd. 2007, HotNets; §2.2, §3.3, §4]:
- **Gerekçe** (§2.2): yayın yoklamalı tahminciler (ETX, MintRoute) bağ tahminini veri trafiğinden ayırır. Bağ bozulunca tahmin, bir sonraki selam kaybolana kadar bunu göstermez.
- **Nasıl:** her veri gönderiminin onay biti (`ack bit`) tahmine girer.
  - Tek alıcılı tahmin her `k_u` gönderimde hesaplanır: `a` onay alındıysa ETX = `k_u / a`. Hiç onay yoksa ETX = son başarıdan beri başarısız gönderim sayısı.
  - Selam tahmini pencereli üstel ortalamadan hesaplanır.
  - İki tahmin ikinci bir üstel ortalamada birleşir. Ağır trafikte veri, sessizken selam baskın olur.
  - Selam, tahminin yalnız başlangıcını sağlar; sonra veri inceltir.
- **Sonuç** (§1): karşılaştırma MultihopLQI'yle (CC2420 telsizinin kalite göstergesine dayanan tahminci). Mirage'da (85 düğüm) paket başına iletim maliyeti %29 düşer, teslim %99,9 (MultihopLQI %93); TutorNet'te (94 düğüm) %44 düşer, teslim %99 (MultihopLQI %85). Deney ağları sabit düğümlü. Düşük güçte kaybın azlığı, tahmincinin kayıpları fark edip yolu değiştirecek kadar çevik olduğunu gösteriyor (§4).
- **Bizim için anlamı:** veri sonucu bağı bir **tetikle kesip atmıyor**, **maliyetini** yükseltiyor. Pahalılaşan bağdan ancak daha iyi bir yol varsa ayrılınır; yol yoksa bağ kullanılmaya devam eder.
- **Risk:** T-2, veri sonucunu maliyete sokmayı yük salınımı (T-4) yüzünden reddetmişti; veri başarısı kanal yüküne bağlıdır. 4B ve CTP bunu histerezisle (1,5 ETX) yönetiyor. Jonglez & Chroboczek'in (5-2 notları §2) çaresi de doyma ve histerezis.

**Hareketlilik** ↪ [Bindel, Chaumette, Hilt; F-ETX, 2015–2016, HAL'de açık]:
- Sabit pencere ve üstel ortalama, tahmini hareketliliğe yavaşlatır. Kısa pencere tepkisel, uzun pencere ağır.
- F-ETX, dört tahminciyle bağın durumunu ve gidişini (öngörü) verir; ölçüye "kararlılık" bilgisi ekler.
- Bir çalışmada hareketli senaryoda atlama sayısı ETX'i geçmiş.

**Hız farkındalığı** ↪ [ETT, Roofnet, Bicket vd. 2005]: ETT = ETX · paket boyu / hız. Tek hızlı ETX'te iki 1 Mb/s iletimle iki 2 Mb/s iletim karşılaştırılamaz. Bizde veri ARF'yle hız değiştiriyor, selam temel hızda gidiyor. Küçük test dünyasındaki "selam geçiyor, veri geçmiyor" bağının bir açıklaması bu olabilir; ölçülmedi.

---

## 3 · Fırsatçı (her-yol) yönlendirme ↪

- **ExOR** [Biswas & Morris 2005]: paket yayınlanır; kimin aldığı öğrenildikten sonra ilerletecek düğüm seçilir. Uzun yollarda verim 2–4 kat (özet).
- **ORW** [Landsiedel vd. 2012]: toplama ağı için; paket bir alıcı kümesine adreslenir, ilk uyanan iletir; "her-yol eğimi" ve ona uygun bir ölçü (EDC).

**Bizim için:** bir paket birçok olası alıcıdan biriyle ilerleyebildiği için tek bağın kesilmesi açlık doğurmaz. Bedeli MAC'te alıcılar arası eşgüdüm ve simülatörde yeni bir iletim türü. En büyük değişiklik; şimdilik aday olarak not edilir.

---

## 4 · Karıştırma katmanı

**Tespit:**
- **Xu vd. 2005** ↪ (özet; özgün metin hâlâ açılmadı): teslim oranı tıkanıklığı karıştırmadan ayırır, ama hareketlilikten (kötü bağdan) ayıramaz. Çare olarak sinyal gücü ya da konumla tutarlılık denetimi önerilir. Bizde ikisi de okunmuyor (KK-03 kural 11; konum ödenmiş mesajla gelir).
- **Bölge düzeyinde teslim** ↪ [Siddhabathula vd. 2012]: saldırgan iki düğümü değil bir bölgeyi karıştırır; teslim oranı düğüm çifti yerine bölgede değerlendirilir. Çift başına karar uzun gözlem ister.
- **Puñal vd. 2014** (5-2 notları §3 ✓): elle konan eşikler tıkanıklık ve zor yayılım koşullarında yanılır; komşularla işbirliği doğruluğu belirgin artırır.
- **Bizim gözlemimiz** (§0): selam eşiğiyle çıkan, kâhine göre iyi bağlarda selamla ölçülen iki yönlü teslim çarpımı ~0,23; yön başına kabaca yarı yarıya kayıp. KK-03'ün selam kaybına dayanan işaretleri (`s ≥ 0,6` ve sessizlik kanıtı) tıkanıklıkla yanlış alarm verebilir. Küçük test dünyasında karıştırıcısız koşuda da birkaç sessizlik kanıtı çıkmıştı (kapanış belgesi). Xu ve Puñal'in uyarısıyla aynı yönde.

**Karşılık:**
- **JAM** ↪ [Wood, Stankovic, Son 2003]:
  - Karıştırılan bölgenin sınırındaki düğümler bölgeyi haritalar. Bölge, kopuk bağlar kümesi olarak değil tek bir varlık olarak ele alınır ve yönlendirme ondan kaçınabilir.
  - Haritalama 1–5 s'de çıkıyor.
  - Eleştirisi: dağıtık olduğu için ileti yükü yüksek, bölge içinde yayın fırtınası var.
- **Karıştırma etkinliği ölçüsü** ↪ [Kan & Fan 2012, EURASIP, açık erişim; IAMP]: düğüm başına "karıştırılıyor" durumu ve kanalın karıştırılmış geçirdiği zamanın payı bir ölçü olarak yol seçimine girer.
  - Bizim için: ikili "karıştırılıyor / değil" yerine bağın karıştırma geçmişi (örneğin son dakikada açık kalma payı). Çizelgeli karıştırıcıda (15/15) "az önce karıştırılmıştı" hafızasıyla sık karıştırılan bağdan kaçınmak (5-2 notları §6'nın sorusu).
- **Tetikleyen düğümler** ↪ [Xuan vd. 2012, IEEE TMC]: tepkisel karıştırıcıyı hangi düğümlerin gönderimi tetikliyorsa onlar bulunur ve yalnız alıcı olacak biçimde yönlendirme yapılır. Bizim tepkisel karıştırıcı sınıfımız için aday fikir; bulma yöntemi (grup testi) ağır.
- **Tague vd. 2011** (5-2 notları §4 ✓): bağ başarısının ortalaması ve değişkenliği birlikte, portföy gibi risk. İkili durum yerine değişkenlik.
- **Derlemenin uyarısı** ↪ [Pirayesh & Zeng 2022, depoda]: karıştırmaya ancak fiziksel katmanda tam karşı konabileceğini savunur. Ağ katmanının yapabileceği dolaşmaktır (5-2 notları §3, Yang 2025).

---

## 5 · Zaman değerleri: nereden geldiler, ne işe yarıyorlar

| değer | nerede | dayanak (`KK-00`) | etkisi | değerlendirme |
|---|---|---|---|---|
| bekletme 2 s / atlama | KK-05 | T-18: bir düğümde tutma 5 s'lik gecikme tavanını aşmaz (K-246: ArduPilot, MAVLink kopma sınırı) | yalnız yol yokken; olağan pakette gecikme p50 0,04 · p99 0,30 s (tetiksiz ikiz) | telemetri 1 Hz: 1 s'den eski paketin yerine yenisi zaten var; 1 s ya da "kaynak başına en yeni paket" daha anlamlı olabilir. Komut (0,25 Hz) farklı |
| yeniden sorma 0,5 s | KK-05 | simülatör tamponu yalnız uyandırmadan sonra döker (K-135) | yol bulununca 1 ms'de gönderilir; 0,5 s yalnız yedek | sorun değil |
| selam 0,5–2 s | KK-02 | Trickle; sessizlik kanıtının süresi (Y-9) | kopuşun ne kadar sürede fark edileceği (Babel'in RFC'sine göre 1,5–3,5 selam aralığı; bizde ölçülmedi) | CTP 64 ms – 1 saat; Babel 4 s |
| silme 30 s | KK-01/14 | İlke 2: 15 s'lik karıştırmada komşu silinmesin | yalnız kayıt; bağ çok önce kullanım dışı kalır | yol seçimini etkilemez |
| `T_HATIRA` 30 s | KK-01/10 | karıştırılıyor süresi iki çizelgede 11–15 s | "bitti" hiç gelmezse üst süre; normalde iki temiz selamda çıkılır | yedek; hatıranın 30 s geçerli sayılması hareketlilikte uzun olabilir |
| `KENDI_UST_SURE` 30 s | KK-01/13 | Y-6, 18 Kasım (seçenek A) | kendi karıştırılmamda ölçümleri dondurmanın üst sınırı | dondurma sürerken komşular uzaklaşırsa ölçü bayatlar; ölçülmedi |
| ortalama penceresi 30 s | KK-03 | çözülen çerçeve düşüşünün tabanı | işaretin karşılaştırma tabanı | tıkanıklıkla değişen taban; ölçülmedi |
| ceza 10–40 s | KK-01/11 | veri tetiğinin gidip gelmesini önlemek | tetikle KÖTÜ'ye düşen bağın en az kullanım dışı süresi | teşhiste açlığın süresini uzatan şey; tetikle birlikte gider |
| tur isteği 0,5 s × 3, dizi 5 s | KK-04 | Babel'in sayısı; aralık bu tasarımın | açlıkta yanıt süresi | — |

Değerlerin hiçbiri referans dünyada taranmadı (`KK-00`: "değerler başlangıçtır").

---

## 6 · Tasarım için seçenekler (karar değil)

**Bağın ölçüsü ve veri tetiği:**
1. **Tetiği kaldırmak** (ikizde ölçüldü). Kalıcı "selam geçiyor, veri geçmiyor" bağı yakalanmaz (§0).
2. **Veriyi maliyete katmak** (4B): selam ve veri sonucu tek bir ETX'te birleşir; bağ kesilmez, pahalılaşır. Yük salınımı riski histerezisle yönetilir (T-2 ve T-4'ün gerekçesi yeniden tartılır).
3. **Tetiği yalnız uygun yedek varken çalıştırmak**, cezasız.

**Yol seçimi:**
- **A · Babel ailesinde kalıp yumuşatmak:**
  - düzgünleştirilmiş maliyet ve "ikisi birden daha iyi" kuralı (Babel A.3);
  - ölçüsü 2. madde;
  - ETX eşiğini mutlak (MRHOF ve CTP gibi 1,5) ya da oransal tutmak.

  Açlık mekanizması (FD, tur) kalır; açlık, kökü (bağ çıkışı) azaldığı ölçüde azalır.
- **B · Eğim ailesine geçmek (CTP gibi):**
  - ardıl, maliyeti benimkinden küçük komşulardan seçilir;
  - veri başlığı gönderenin maliyetini taşır, döngü veri yolunda yakalanır, paket düşürülmez.

  Açlık ortadan kalkar; geçici döngü olabilir. T-12, T-13 ve kimlik metnindeki "döngüsüzlük Babel'in koşuluyla" cümlesi değişir; başlık alanının baytı ödenir (K-232).
- **C · Fırsatçı (her-yol) iletim:** en büyük değişiklik; simülatörde yeni iletim türü ister. Sonraya aday.

**Karıştırma katmanı:**
- Selam kaybına dayanan işaretleri tek başına kanıt saymamak; çözülen çerçeve düşüşü ya da kanal doluluğuyla birlikte istemek (tıkanıklık yanlış alarmına karşı).
- Komşuların bitlerini bölge görüşü olarak birleştirmek (bölge düzeyinde teslim, Puñal'in işbirliği).
- İkili "karıştırılıyor" yerine ya da yanında bağın karıştırma geçmişi (IAMP'nin etkinlik payı, Tague'nin değişkenliği): çizelgeli karıştırıcıda sık karıştırılan bağdan kaçınmak.
- Tepkisel karıştırıcı sınıfı için tetikleyen düğüm fikri (sonra).

---

## 7 · Sonraki okuma

- **Tam metni okunacaklar:**
  - Kan & Fan 2012 (açık erişim);
  - F-ETX (HAL);
  - JAM (DTIC PDF);
  - Xuan vd. 2012;
  - ExOR ve ORW (yazar kopyaları);
  - Siddhabathula vd. 2012;
  - Xu vd. 2005 (açık kopya aranacak).
- **Ölçülmemiş sorular:**
  - "Selam geçiyor, veri geçmiyor" bağının referans dünyada ne sıklıkta olduğu;
  - selamın temel hızı ile verinin ARF hızı farkının payı (ETT);
  - selam kaybının ne kadarının tıkanıklıktan geldiği.

---

## Kaynaklar

| kısa ad | künye | durum |
|---|---|---|
| 4B | Fonseca, Gnawali, Jamieson, Levis, "Four-Bit Wireless Link Estimation", HotNets 2007 — www2.cs.uh.edu/~gnawali/papers/4blehotnets2007.pdf | ✓ §2.2, §3.3, §4 · `fonseca_2007_4b_link_estimation.pdf` |
| CTP | Gnawali, Fonseca, Jamieson, Moss, Levis, "Collection Tree Protocol", SenSys 2009 — www2.cs.uh.edu/~gnawali/papers/ctpsensys2009.pdf | ✓ §3.1, §3.2, §4.1, §4.3, §5 · `gnawali_2009_ctp.pdf` |
| RFC 8966 Ek A.3, Ek B | `protokol_kaynaklari/rfc8966_babel.txt` | ✓ |
| F-ETX | Bindel, Chaumette, Hilt, hal.archives-ouvertes.fr/hal-01277084 | ↪ |
| ETT, Roofnet | Bicket vd., MobiCom 2005 | ↪ |
| ExOR | Biswas & Morris, SIGCOMM 2005 | ↪ |
| ORW | Landsiedel, Ghadimi, Duquennoy, Johansson, IPSN 2012 | ↪ |
| Xu 2005 | Xu, Trappe, Zhang, Wood, MobiHoc 2005 | ↪ (özet) |
| Bölge düzeyinde teslim | Siddhabathula vd., ICC 2012 | ↪ |
| JAM | Wood, Stankovic, Son, RTSS 2003 — apps.dtic.mil/sti/pdfs/ADA446986.pdf | ↪ |
| IAMP | Kan & Fan, EURASIP JWCN 2012 — doi 10.1186/1687-1499-2012-267 | ↪ |
| Tetikleyen düğümler | Xuan, Shen, Nguyen, Thai, IEEE TMC 11(5), 2012 | ↪ |
| Pirayesh & Zeng 2022 | `protokol_kaynaklari/pirayesh_zeng_2021_jamming_survey.pdf` | 5-2 notlarında ✓ (WLAN bölümü) |

---

## 8 · Sonrası (19 Kasım)

Kararlar `v2/17`'de: T-2 vazgeçme tetiği (veri sonucu maliyete girmez; yalnız MAC vazgeçmeleri sayılır; bağ yalnız yedek varken bırakılır; §6'daki üç seçeneğin dışında bir dördüncü yol, kayıtlardaki vazgeçme dağılımına dayanarak) · T-11 anlık ve düzgünleştirilmiş maliyet birlikte · T-12 maliyet eğimi, son çare, maliyet tavanı ve başlıksız döngü bekçisi (§6'nın B'si, uyarlanmış) · T-13 açlık ve tur kalktı. Karıştırma işaretlerinin kalabalıkla yanlış alarmı karıştırma katmanının A/B'leriyle düzeltilecek; bölge risk skoru fikir olarak duruyor.
