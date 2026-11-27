# Bileşen kâğıtları — dizin, değerler, bayraklar, gözlemin kullanımı

> Yeni tasarımın (`../18-YENI-TASARIM.md`) kural kâğıtları: bileşen başına bir kâğıt. Bileşenin sorunu, kanıtı, seçenekleri ve kararım `18`'in "Bileşenler" bölümünde; kuralları kâğıdında. Değerler, bayraklar ve gözlemin kullanımı **yalnız bu dosyada** tutulur; kâğıtlar adlarıyla anar (`18` bütünlük listesi madde 1). Kod Aşama 4'te bu kâğıtlardan yazılır. Önceki tasarımın kâğıtları `../kural/KK-*`; yeni tasarım donana kadar bugünkü kodun belgesidir. Güncel: 27 Kasım 2026 (B6; aynı gün B5 ve B4'ün eki).

## Kâğıtlar

| # | bileşen | kâğıt | durum |
|---|---|---|---|
| B1 | komşu ve bağın ölçüsü | `B1-KOMSU-VE-BAG.md` | onaylandı (24 Kasım) |
| B2 | karıştırma kanıtı | `B2-KARISTIRMA-KANITI.md` | onaylandı (25 Kasım) |
| B3 | bağın durumu | `B3-BAG-DURUMU.md` | onaylandı (26 Kasım) |
| B4 | yol | `B4-YOL.md` | onaylandı (26 Kasım; eki ve kural 15'in düzeltmesi 27 Kasım) |
| B5 | iletim kararı | `B5-ILETIM-KARARI.md` | onaylandı (27 Kasım) |
| B6 | kontrol iletileri | `B6-KONTROL-ILETILERI.md` | onaylandı (27 Kasım) |
| B7 | bekletme ve komut | — | sırada |

## Ortak birimler

- **Süre:** saniye, düğümün kendi saatiyle (`saat_s`); saatler senkron değildir, yalnız süreler kullanılır (`05` §3.2).
- **Sıra numarası:** 16 bit, modüler karşılaştırılır: fark = (yeni − eski) mod 2^16, [−32768, 32767] aralığına çevrilir.
- **Bağın ölçüleri (B1):** gerçek sayı; birimi beklenen deneme sayısı (ETX).
- **Bağın maliyeti (B3):** gerçek E (ETX) ve tamsayı M = min(⌈`MALIYET_BIRIM` · E⌉, 0xFFFE); ∞ = 0xFFFF (B3 kural 2). İlan biçimi B4 ve B6'da yazılır.
- **Kanıt aralıkları (B2):** [başlangıç, bitiş], kendi saatimle; sürmekteki aralığın bitişi ∞. B1'in hariç aralığıyla aynı biçimdedir (B1 kural 10).

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
| `TIK_S` | 1 s | B2/1 | teşhisin ve teşhis (d)'nin saniyesi: işaretler saniye başına ölçüldü; önceki tasarımın saniyelik zamanlayıcısı | `m` ve `c` gürültülü olur (ikizde saniyede ~71 çerçeve) · giriş ve çıkış en az bir saniye sürdüğü için yavaşlar | hayır |
| `ED_ESIK` | kanal meşgul payı 0,55 | B2/2 | B2 teşhisinin K1 seçimi: seçim yarısında ikizde yanlış alarmı ≤ %0,05 olan en küçük eşik (%0,037); doğrulamada %0,007. Yakalamanın dayanağı sonuçtan sonra: alana girişten 3 s içinde %90–95, ortanca 1 s (`ek_hesap.txt` E7); K1'in birimiyle tavanda (E8); 25 Kasım kararım, `06` §10 | 0,50: ikizde yanlış alarm %0,354 (seçim) · 0,62: dönem içinde yakalama 0,927'den 0,780'e (seçim) | Aşama 4'te bakılır |
| `G_ALFA` · `G_BETA` | 0,4 · 0,6 | B2/5 | B2 teşhisinin K2 seçimi: 288 G ve GM kuralından seçim yarısında yanlış alarm sınırlarını 61'i geçti, en erken yakalayan bu; doğrulamada ikizde %0,002, açık dönemde uzak alanda %0,5–1,5, 3 s içinde 0,344–0,347 | α büyür ya da β küçülürse yanlış alarm artar (önceki kural G(0,5 · 0,6 · 2 · 3) uzak alanda %3,2–6,9) · tersinde geç ve az yakalar | Aşama 4'te bakılır |
| `G_GIRIS` · `G_CIKIS` | 2 · 1 ardışık saniye | B2/6 | B2 teşhisinin K2 seçimi; çıkış ortancası 1 s | giriş 1: tek saniyelik dalgalanma yanlış alarm olur · giriş 3: bir saniye daha geç; çıkış 2–3: sessiz dönemde bağlar geç döner (önceki kuralın çıkışı 3 s) | Aşama 4'te bakılır |
| `CBAR_SANIYE` | 30 işaretsiz saniye | B2/4 | önceki KK-03 kural 1; teşhisin kuralı (`isaret.py`, `ORTALAMA_SANIYE`) | düzey gürültülü olur, kısa bir düşüş onu aşağı çeker · düzey değişen çevreye geç uyar | hayır |
| `CBAR_ED_ESIK` | kanal meşgul payı 0,62 | B2/4 | teşhisin kuralı (`isaret.py`, `ED_ISARETSIZ`; teşhis (d)'nin eşiği, önceki `ED_ESIGI`). `ED_ESIK`'ten ayrı tutuldu ki kâğıdın kuralı ölçülenle aynı olsun | 0,55–0,62 arası saniyeler de düzeyin dışında kalır (ikizde çok seyrek) · kilitli saniyeler düzeye girer | Aşama 4'te `ED_ESIK`'le birleştirilip birleştirilmeyeceğine bakılır |
| `KAYIP_PENCERE_S` | 4 s | B2/3 | önceki KK-03 kural 2; teşhisin kuralı | `s` gürültülü olur (0,5–2,2 s'lik selamlarla komşu başına 2–8 örnek) · `s` geç yükselir (G alanında dönemin ilk saniyesinde 0,57–0,59, 3 s'de 0,78–0,80; teşhis §8.3) | Aşama 4'te bakılır |
| `TANIDIK_S` | 16 s | B2/3 | önceki KK-03 kural 2; teşhisin kuralı | karıştırılan komşu tanıdık sayılmaktan erken çıkar, sıfırları sayılmaz · ölen ya da uzaklaşan komşunun sıfırları `s`'yi şişirir | hayır |
| `GK_DENEME` · `GK_ARDISIK` | 7 deneme · 3 ardışık kayıt | B2/12 | B2 teşhisinin K4 seçimi (DEN7x3): ikizde ve önce evresinde 1000 çerçevede 1 sınırını 27 kuraldan üçü geçti, G alanında en erken yakalayan bu; doğrulamada ikizde 1000 çerçevede 0,40. Art arda 3 vazgeçmeyi kapsar; E alanında onunla aynı sayılar (seçim yarısı) | DEN6x3 ikizde 1000 çerçevede 0,93, DEN7x2 2,34 (seçim) · daha geç yakalar | Aşama 4'te bakılır |
| `MALIYET_BIRIM` | 1 ETX = 64 birim | B3/2 | önceki tasarımın birimi (KK-00 genel kural 3: ETX × 64); 1/64 ETX çözünürlük (~%1,6); 16 bitlik alan ~1 000 ETX'e kadar taşır | maliyet kabalaşır, yakın bağlar eşit görünür · 16 bitlik alan taşar | hayır |
| `KANIT_OMUR_S` | 5 s | B3/6–7 | son başarısızlıktan sonra gönderici ve veri yok kanıtının ömrü; bağ kullanılmazken yeni kanıt gelmediği için yeniden denemenin aralığı (İlke 3). Birincilde açık dönem 15 s, dayanıklılıkta 10 s; G alanındaki alıcıların çoğu bütün dönem karıştırılıyor (B2 teşhisi §8.1): dönem başına 1–2 yeniden deneme, her biri bir çerçeve; karıştırma bitince bağ en çok 5 s geç döner | karıştırılan bağa sık yeniden deneme, boşa kanal süresi · karıştırma bitince bağ geç döner (sessiz dönem) | Aşama 4'te bakılır |
| `VERI_YOK_N` | 4 kayıt | B3/7 | B3 teşhisi `ek_hesap.txt` E4 (kuraldan sonra): son 4 kaydın hepsinin vazgeçme olması temiz kanalda veri örneklerinin %0,01–0,15'i, karıştırılan alıcıda %7–26'sı; 3 kayıtla temizde %0,05–0,32. B1'in `ORNEK_EN_AZ`'ıyla aynı | 3: temizde yanlış alarm ~2–5 kat · 6–8: kalıcı sorunda geç | Aşama 4'te bakılır |
| `BILDIRIM_PAYI_S` | 3 s | B3/9 | komşu durumunu geç bulur: girişim kuralı 3 s içinde %34–35, alana girişten gecikme ortancası 2 s (B2 teşhisi E7); bit selam başına %35 olasılıkla ulaşır | komşunun sezilmemiş karıştırmasındaki düşük bildirimler ölçüye girer · sağlam örnekler gereksiz dışarıda kalır | hayır |
| `HARIC_UST_S` | 30 s | B3/9–10 · B4/4 | İlke 2 (ölçmeyi bırakmamak); B1'in `SELAM_SAKLA`'sı 30 s'lik hariç aralığa göre seçildi; önceki tasarımın `T_HATIRA`'sı ve `KENDI_UST_SURE`'si. B4 kural 4'te kendi aralığımın ilanın yaşından çıkarılan kısmının sınırı da budur | uzun karıştırmada kalite erken bozulur · uzun karıştırmada bağın yeni hâli geç görülür, B1'in saklaması yetmez | hayır |
| `ILAN_OMUR_KAT` | 3,5 × komşunun selam aralığı `a` | B4/4 | Babel'in rota süresi: ilan aralığının 3,5 katı (RFC 8966 Ek B, "Route Expiry time"). Bizde ilan her selamdadır, aralık selamınki; tek kaybolan selam ilanı bayatlatmaz (~3 selam). B5 teşhisi (E9, kuraldan sonra): ikizde kararların %2,1'inde ardılın ilanı bu sınırı aşıyor, ardıla giden çerçevelerin %96'sı yine onaylanıyor; karşılığı kural 4a (27 Kasım). Kendi aralıklarımda yaş durur | gecikmeyle gelen selamda aday gereksiz düşer · ölü ya da kilitli komşu geç bırakılır | Aşama 4'te bakılır |
| `SURE_ISTEK_PAYI` | 1 × ardılın selam aralığı `a` | B4/4a | RFC 8966 §3.8.2.3: süre dolmadan kısa bir süre önce ("shortly before") istek. Babel-a tutma süresinin 7/8'inde ister (`protokoller/babel_bicim.py`); Babel'in 16 s'lik ilan aralığıyla bu, süre dolmadan 7 s, kabaca iki Babel selamıdır. Bizde ilan selamdadır ve yanıt bir selamdır; bir selam aralığı, en kısa aralıkta (0,5 s, B1 Ö-4) bile ardılın bir kez yanıtlamasına yeter | yanıt yetişmez, çalışan ardılın ilanı yine düşer · istek daha erken, her kaçan selamda gider: gereksiz istek ve kontrol yükü | Aşama 4'te bakılır |
| `TERCIH_FARKI` | 128 birim (2 ETX) | B4/10a | babeld `send_unfeasible_request`: seçili rotanın metriği yeni metrik + 512'den küçük değilse istek (Babel-a `TERCIH_FARKI` 512). Babel'de kusursuz bir bağ 256'dır (Ek A.2.2); 512 iki kusursuz atlamalık fark, bizim birimimizle (1 ETX = 64) 128. Sınıf farkı (O ↔ S) bu eşiğe bakmaz | küçük maliyet farkları için istek, sık tur artışı ve çalkalanma · belirgin daha iyi yol açılmaz | Aşama 4'te bakılır |
| `DUZ_S` | 6 s | B4/6 | RFC 8966 Ek A.3: düzgünleştirmenin zaman sabiti selam aralığının ~3 katı; önceki tasarımın `DUZ_S`'i (3 × `I_MAX` 2 s) | geçiş gecikmesiz olur, iki yol arasında salınım · daha iyi yola geç geçilir | B6'nın selam aralığına bağlı; aralık değişirse yeniden bakılır |
| `YOK_SAYMA_S` | 5 s | B4/10, 10a | önceki tasarımın `ISTEK_ARA`'sı (18 Kasım KK-04 kural 7): isteğin geçide gidip yanıtın dönmesine yeten süre. Kural 10a'da yeni isteğin beklemesi aynı süredir (bekleyen istekler, RFC 8966 §3.2.7; Babel-a §3.8.2.2 isteğini 2 s tutar) | tur gelmeden ardıl bırakılır, gereksiz açlık; 10a'da yinelenen istek · gerçekten kötüleşen ardıl geç bırakılır; 10a'da kaybolan isteğin yenisi geç gider | Aşama 4'te bakılır |
| `ISTEK_YINELEME` · `ISTEK_ARALIK_S` | 3 kez · 0,5 s | B4/11 | RFC 8966 §3.8.2.1 ve Ek B: istek kayba karşı birkaç kez, en çok üç kez yinelenir. Babel'in ilk aralığı 2 s ve her yinelemede ikiye katlanır; bizim selam aralığımız Babel'inkinin (4 s) 2–8'de biri olduğu için aralık kısaltıldı (önceki tasarım, KK-00) | kayıpta yanıt gecikir · kontrol yükü artar | Aşama 4'te bakılır |
| `ISTEK_ARA_S` | 5 s | B4/11 | önceki tasarım: açlık sürerken istek dizisinin yinelenmesi | gereksiz istek, kontrol yükü · uzun açlıkta yeni tur geç gelir | hayır |
| `ISTEK_ANIMSA_S` | 4 s | B4/12 | önceki tasarım: iletilen isteğin yanıtını beklerken kayıt | geç gelen yanıt geri yayılmaz · bellek | hayır |
| `ISTEK_BASTIRMA_S` | 1 s | B4/12 | önceki tasarım (Y-11): aynı ya da küçük tur için yinelenen istek iletilmez (RFC 8966 §3.8.1.2) | aynı istek çok kez iletilir · yinelenen istek başka bir yoldan gidemez | hayır |
| `ISTEK_ATLAMA` | 64 | B4/12 | RFC 8966 §3.8.2.1: ağın çapından büyük herhangi bir değer, 64 uygun varsayılan; paket ömrüyle (TTL 64) aynı | uzun yolda istek geçide ulaşmaz · döngüye giren istek daha uzun yaşar | hayır |
| `FD_UNUT_S` | 180 s | B4/9 | RFC 8966 Ek B: kaynak tablosunun çöp toplaması ("Source GC time", 3 dakika) | uzun açlıktan sonra eski FD gereksiz kısıtlar · bellek (tek hedef) | hayır |
| `TUR_BASLANGIC` | 1 | B4/13 | önceki tasarım: geçidin turu 1'den başlar | — | hayır |
| `I_MIN` | 0,5 s | B6/4–5, 8 | Trickle'ın Imin'i (RFC 6206 §4.2); önceki tasarımın değeri (KK-02). B1'in saklaması ve boşluk sınırı, B2'nin selam kaybı penceresi ve B4'ün istek aralığı buna göre yazıldı; ölçülmüş bütün kanıtın koşulu (`18` §2.6). RFC 6206 §5 Imin'i bağ katmanının en kötü gecikmesine göre ister: boş kanalda tek alıcılı bir iletinin 7 denemesi ~0,05 s sürer (kestirim: geri çekilme penceresi 31'den 1023 yuvaya, yuva 20 µs) | olay seli, kontrol yükü · olay (bit, geri çekme) geç duyulur | hayır |
| `I_MAX` | 2 s | B6/5 | önceki tasarımın değeri (KK-02); ilan edilen aralık 2,2 s; Babel'in selamı 4 s (RFC 8966 Ek B). Ölçülmüş bütün kanıtın koşulu; protokolün kanal payı bugün %2,6 (`arsiv/teshis/faz5_3_b6_kontrol_bedeli_2026-11-27/kontrol_bedeli.txt`) | selam sıklaşır: 1 s'de protokolün payı ~%4,5 (kestirim, `18` §2.6 Z2) · susan komşu ve bağın değişimi geç görülür: 4 s'de ilanın ömrü ~15 s (Z4) | Aşama 4'te bakılır |
| `ARALIK_PAYI` | 1,1 | B6/6 | aralık alanı = 1,1 × sonraki I: titreşimin (0,1 · I) üst sınırı dâhil, alan üst sınır kalsın diye (RFC 8966 §4.6.5); önceki tasarım | alan üst sınır olmaktan çıkar, alıcı geç gelen selamı kayıp sayar · zaman aşımı ve ilanın ömrü gereksiz uzar | hayır |
| `TITRESIM_ORANI` | 0,1 | B6/9 | RFC 8966 §3.1 (titreşim SHOULD); ETX'in yoklama titreşimi ±0,1 τ [36]; önceki tasarım; `ARALIK_PAYI` ile birlikte seçilir | aynı olayı duyan komşuların selamları çarpışır · olay selamı gecikir, aralık alanı büyür | hayır |
| `SELAM_ARASI_EN_AZ` | `I_MIN` (0,5 s) | B6/8 | B1 Ö-4; önceki tasarımın sıklık sınırı (`17` T-17) | olay seli · ardışık olaylar geç duyulur | hayır |
| `ILAN_ESIGI` | %15 | B6/7 | önceki tasarım (KK-02, `17` T-17). İlan her selamda gittiği için eşik yalnız değişimin ne kadar erken duyulacağını belirler, en çok bir selam aralığı (2,2 s). Babel'in eşikleri mutlaktır (babeld: kötüleşme ≥ 512 acil, 384'ten küçük fark gönderilmez; `protokoller/babel_bicim.py`), çünkü ilanı 16 s'de bir gider | küçük dalgalanmada ara ilan, selam sıklaşır · önemli değişim bir aralık geç duyulur | Aşama 4'te bakılır |
| `ARALIK_BIRIMI_S` | 0,01 s | B6/1, 6 | RFC 8966 §4.6.5: santisaniye; 16 bitle 655 s'ye kadar | — | hayır |
| `ORAN_OLCEK` | 255 | B6/1 | oranın 8 bitlik biçimi: `d_r` × 255, aşağı yuvarlanır (önceki tasarımın `ORAN_EN_COK`'u) | oran kabalaşır · alan büyür | hayır |
| `KANIT_SAKLA` | 128 aralık ya da olay | B2/8, 10, 12 | bellek sınırı. B1'in selam saklaması (128 örnek) en uzun aralıkta (2,2 s) ~280 s'ye yayılır; 1 s'lik giriş ve çıkışla bu sürede en çok ~140 aralık oluşabilir, birincilde düğüm başına dönem başına birkaç | eski örneklerin aralığı unutulur, hariç aralık eksik kalır · bellek | hayır |

## Bayraklar ve sınıflar

Her mekanizmanın bayrağı, sınıfı (karıştırmaya karşı ya da genel; K-247) ve kapalıyken davranışı burada yazılır. Karıştırmaya karşı olanlar tek bir bayrak grubuyla birlikte kapanabilir (`18` §1.4 sözleşme 7).

| mekanizma | bileşen · kural | bayrak | sınıf | kapalıyken |
|---|---|---|---|---|
| komşu kaydı, selam sayımı, veri kaydı, ölçüler | B1 | yok (çekirdek) | genel | — (selam olmadan komşu ve bağ bilinemez; ölçmek davranışı değiştirmez, ölçünün kullanımının bayrağı kullanan bileşendedir, B1 §10) |
| kendi durumum, kendi aralıklarım, işaretler; B3'ün karıştırma eki ve B4'ün kendi karıştırılmam kuralları, B6'nın kilit kuralı (B5'in karıştırma eki yok) | B2 1–9, 14, 17 | `karistirma_katmani` (grup) | karıştırmaya karşı | B2 çalışmaz, `kanal_dolulugu_ister` denmez; durum hep "yok", aralık ve kanıt yok, bit hep 0 (alan kalır); B1'in hariç aralık listesi boş; alt bayraklar etkisiz (B2 §10) |
| alıcının biti | B2 9–11 | `alici_bildirimi` | karıştırmaya karşı | bit hep 0 gider, alınan bit okunmaz, "bit değişti" olayı yok (alan kalır, boy aynı); kendi durumum ve aralıklar sürer; A, B olur (`18` §2.2) |
| göndericinin kanıtı | B2 12–13 | `gonderici_kaniti` | karıştırmaya karşı | gönderici olayı oluşmaz |
| bağın maliyeti (selamdan, eşiksiz), durumu, KULLANILMAZ | B3 1–4, 11–12 | yok (çekirdek) | genel | — (maliyetsiz yol seçilemez) |
| veri yok güvenlik ağı | B3 7 | `veri_yok` | genel | sebep oluşmaz |
| karıştırılan bağın son çare olması (bildirim, gönderici), geçit istisnası | B3 5–6, 8 | `karistirma_katmani` (grup) | karıştırmaya karşı | sebep oluşmaz |
| hariç aralık, karıştırmadan önceki oranın bildirilmesi | B3 9–10 | `haric_aralik` | karıştırmaya karşı | liste boş: B1 ham ölçer, oran ham bildirilir; SON ÇARE sebepleri sürer |
| uygulanabilirlik koşulu, seçim, ilan, FD, tur isteği | B4 1–3, 5, 7–13, 15–16 | yok (çekirdek) | genel | — (kapatılamaz: döngüsüzlüğü kaldırır) |
| anlık ve düzgünleştirilmiş maliyetle geçiş | B4 5–6 | `duzgun_gecis` | genel | isteğe bağlı geçişte yalnız anlık maliyet |
| ilanın ömrü | B4 4 | `ilan_omru` | genel | ilan, komşu B1'de silinene kadar geçerli; kural 4a da çalışmaz |
| süre dolmadan istek | B4 4a | `sure_istegi` | genel | istek gitmez; ilan tazelenmezse kural 4'le düşer |
| tercih edilir uygulanamaz ilanda tur isteği | B4 10a | `tercih_istegi` | genel | tur isteği yalnız yok saymada ve açlıkta gider |
| kendi karıştırılmamda ilanların yaşının durması ve isteğin bastırılması | B4 4 (yaş), 14 | `karistirma_katmani` (grup) | karıştırmaya karşı | B2 hep "yok" der: ilanların yaşı kesintisiz işler, istek bastırılmaz |
| paketin ardıla gönderilmesi (tek yol); kopya, sapma ve kurtarma yok | B5 1–7 | yok (çekirdek) | genel | — (paket B5 olmadan gönderilemez; B5'in karıştırma eki yok, `18` §2.5) |
| selam ve tur isteği: biçim, olaylar, en kısa ara, titreşim, uyandırmalar | B6 1–4, 6–10, 12–14 | yok (çekirdek) | genel | — (selam olmadan komşu, bağ ve yol bilinemez) |
| uyarlanır aralık | B6 5 | `uyarlanir_aralik` | genel | I sabit `I_MAX`; olaylar selamı yine öne çeker |
| kendi kanal kilidimde selam kurmama | B6 11 | `karistirma_katmani` (grup) | karıştırmaya karşı | selam kilitte de kurulur, kuyrukta bekler |

**Mekanizma kapısının "hepsi kapalı" kolu** (`06` §0.4.5): `karistirma_katmani` kapalı, genel mekanizmalar açık.

## Gözlemin kullanımı (`05`; mimari denetimi D17)

| bileşen | okur | okumaz |
|---|---|---|
| B1 | selam: göndereni, sırası, aralığı, benim için bildirilen oran (B6 çözer) · `iletim_sonucu`: hedef, başarı, `tekrar` (ölçüye yalnız tür `veri`; onayın gelmesi her türde varlık kanıtı) · `cerceve_duyuldu`: göndereni, yalnız tür `veri` ve `kontrol` · `saat_s` (yalnız süreler) | `olculen_gurultu_w` (yasak, K-227) · RSSI · `phy_hata` · `alinan_cerceve` · `mesgul_sure_s` · `kendi_konum` · `kendi_hiz` · `komsular` (simülatörün beacon listesi) · kuyruk · duyulan onay ve kontrol onayının göndereni (gerçek 802.11 onayı verici adresi taşımaz) |
| B2 | `mesgul_sure_s` (`kanal_dolulugu_ister`; yalnız `karistirma_katmani` açıkken) · `alinan_cerceve` · selam: göndereni ve karıştırma biti (B6 çözer) · B1'in çıktıları: selam örnekleri, `son_selam_t`, komşu kümesi ve olayları, veri kayıtları · `saat_s` (yalnız süreler) | `olculen_gurultu_w` (yasak, K-227) · RSSI · `phy_hata` · `kanal_mesgul_mu` · `iletim_sonucu` ve `cerceve_duyuldu` doğrudan (veri sonucu B1'in kaydından) · `kendi_konum` · `kendi_hiz` · `komsular` · kuyruk |
| B3 | yalnız B1'in ve B2'nin çıktıları (B3 §2) · yapılandırma: geçidin kimliği | gözlem sözleşmesinin hiçbir alanını doğrudan okumaz · `olculen_gurultu_w` (yasak, K-227) · RSSI · konum |
| B4 | selam: tur ve maliyet (B6 çözer) · tur isteği: gönderen, istenen tur, kalan atlama (B6 çözer) · B1: komşu kümesi ve olayları, komşunun selam aralığı `a` · B2: kendi durumum ve kendi aralıklarım · B3: bağın durumu ve maliyeti · `saat_s` (yalnız süreler) · yapılandırma: geçidin kimliği | gözlem sözleşmesinin öteki alanları · `olculen_gurultu_w` (yasak, K-227) · konum · paket başlığı |
| B5 | paket başlığından yalnız hedef (geçit mi) · B4: ardıl, aday listesi, açlık durumu · B7: bekletme kararı ve komutun sonraki atlaması (B7'nin kâğıdında) | gözlem sözleşmesinin öteki alanları · `olculen_gurultu_w` (yasak, K-227) · RSSI · kuyruk · konum · başlığın öteki alanları (kaynak, `kaynak_sira`, atlama sayısı: döngü tanısı B4'ün, geri iz B7'nin) · B1, B2, B3 doğrudan (B4 üzerinden) |
| B6 | selam ve tur isteği (`kontrol_alindi`): bütün alanlar; çözer ve dağıtır · B1: yeni komşu olayı · B2: bit, "bit değişti", kendi durumum kanal kilidi mi · B3: bildirilecek oran listesi · B4: ilan (tur, C), "hemen gönder" olayları, tur isteği iletileri, kural 4a'nın anı · `saat_s` (yalnız süreler) | `olculen_gurultu_w` (yasak, K-227) · RSSI · kuyruk · konum · `komsular` (simülatörün beacon listesi) · veri paketleri |

## Aşama 3'e açık kalanlar

- **Olay sırası:** B1, bir gözlemi işlemeden önce o ana kadarki kendi zaman olaylarını işler (B1 kural 20); `18` §1.4'ün olay sırasında gözlemin dağıtımı (1) zaman olaylarından (2) önce yazılı. Bütün bileşenler için ortak kural bütünlük denetiminde yazılır.
- **Bileşenler arası beklentiler:** B1'in, B2'nin, B3'ün ve B4'ün B6'dan beklentileri B6'da karşılandı (B6 §6'nın tablosu, 27 Kasım). B2'nin B3'e bıraktıkları (B2 §11 madde 2) bütünlük denetiminde denetlenir.
- **İskeletin kanca tablosu** (`18` §1.4): iletim sonucu B2'ye ayrıca dağıtılmaz; B2 veri sonucunu B1'in kaydından okur (B2 §2, sözleşme 3). Tablo bütünlük denetiminde buna göre düzeltilir.
- **B1'in sondaki sessizliği** (B1 kural 16): ne B2 (B2 §2) ne B3 (B3 §2) kullanıyor; kaldırılır.
- **B3'ün B4'ten beklentileri** (B3 §6, §11 madde 3): olağan adaylar SON ÇARE'den önce; yol değişiminin histerezisi B4'te.
- **Ortak sözlük:** B3'ün SON ÇARE durumu ile B4'ün aday türlerinin adları karışmamalı (B4 adaylarını O ve S sınıfı diye anar).
- **B4'ün B6'dan beklentileri** (B4 Ö-1…Ö-5): B6'da karşılandı (B6 kural 1–2, 6–8, 13). Tek başına ardıl değişimi olay sayılmadı; B4 kural 15 düzeltildi (27 Kasım).
- **İki meşgul payı eşiği:** `ED_ESIK` (0,55) ve `CBAR_ED_ESIK` (0,62). Birleştirmek ölçülen kuralı değiştirir; Aşama 4'te bakılır.
- **İskeletin B5 satırı** (`18` §1.4): A seçildi (27 Kasım). B5 paket başına kayıt tutmaz ve karıştırma eki yoktur; tablo bütünlük denetiminde düzeltilir.
- **B5'in B7'den beklentileri** (B5 §6): açlıkta bekletme kararı; komutun sonraki atlaması (geri iz).
- **B5 ile B7'nin sırası:** iskelet B5'in B7'ye danışmasını öngörüyor (`18` §1.4 olay sırası 4; B7'nin satırı "B5'e bekletme kararı"). Sözleşme 1'e (yalnız aşağıdakini okur) göre B7'nin bu cevabı B5'ten önce hesaplanır, yani B7 bu iş için B5'in altında sayılır. B7'nin kâğıdında ve bütünlük denetiminde yazılır.
- **Mekanizma kapısının payı:** B5 teşhisinde J1'in (karıştırma katmanının kurtarabileceği kayıp, 0,0485) yalnız 0,016'sı katmana ait; kalanını çekirdeğin "veri yok" ve ilanın ömrü kuralları da görüyor (`arsiv/teshis/faz5_3_b5_iletim_kaybi_2026-11-26/ek_hesap.txt` E7). Bütünlük denetiminde kapının beklenen payı yeniden kestirilir.
