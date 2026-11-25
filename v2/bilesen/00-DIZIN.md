# Bileşen kâğıtları — dizin, değerler, bayraklar, gözlemin kullanımı

> Yeni tasarımın (`../18-YENI-TASARIM.md`) kural kâğıtları: bileşen başına bir kâğıt. Bileşenin sorunu, kanıtı, seçenekleri ve kararım `18`'in "Bileşenler" bölümünde; kuralları kâğıdında. Değerler, bayraklar ve gözlemin kullanımı **yalnız bu dosyada** tutulur; kâğıtlar adlarıyla anar (`18` bütünlük listesi madde 1). Kod Aşama 4'te bu kâğıtlardan yazılır. Önceki tasarımın kâğıtları `../kural/KK-*`; yeni tasarım donana kadar bugünkü kodun belgesidir. Güncel: 25 Kasım 2026 (B2).

## Kâğıtlar

| # | bileşen | kâğıt | durum |
|---|---|---|---|
| B1 | komşu ve bağın ölçüsü | `B1-KOMSU-VE-BAG.md` | onaylandı (24 Kasım) |
| B2 | karıştırma kanıtı | `B2-KARISTIRMA-KANITI.md` | onaylandı (25 Kasım) |
| B3 | bağın durumu | — | sırada |
| B4 | yol | — | bekliyor |
| B5 | iletim kararı | — | bekliyor |
| B6 | kontrol iletileri | — | bekliyor |
| B7 | bekletme ve komut | — | bekliyor |

## Ortak birimler

- **Süre:** saniye, düğümün kendi saatiyle (`saat_s`); saatler senkron değildir, yalnız süreler kullanılır (`05` §3.2).
- **Sıra numarası:** 16 bit, modüler karşılaştırılır: fark = (yeni − eski) mod 2^16, [−32768, 32767] aralığına çevrilir.
- **Bağın ölçüleri (B1):** gerçek sayı; birimi beklenen deneme sayısı (ETX). Maliyetin tamsayı birimi ve ilan biçimi B3, B4 ve B6'da yazılır.
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
| `KANIT_SAKLA` | 128 aralık ya da olay | B2/8, 10, 12 | bellek sınırı. B1'in selam saklaması (128 örnek) en uzun aralıkta (2,2 s) ~280 s'ye yayılır; 1 s'lik giriş ve çıkışla bu sürede en çok ~140 aralık oluşabilir, birincilde düğüm başına dönem başına birkaç | eski örneklerin aralığı unutulur, hariç aralık eksik kalır · bellek | hayır |

## Bayraklar ve sınıflar

Her mekanizmanın bayrağı, sınıfı (karıştırmaya karşı ya da genel; K-247) ve kapalıyken davranışı burada yazılır. Karıştırmaya karşı olanlar tek bir bayrak grubuyla birlikte kapanabilir (`18` §1.4 sözleşme 7).

| mekanizma | bileşen · kural | bayrak | sınıf | kapalıyken |
|---|---|---|---|---|
| komşu kaydı, selam sayımı, veri kaydı, ölçüler | B1 | yok (çekirdek) | genel | — (selam olmadan komşu ve bağ bilinemez; ölçmek davranışı değiştirmez, ölçünün kullanımının bayrağı kullanan bileşendedir, B1 §10) |
| kendi durumum, kendi aralıklarım, işaretler; B3 ve B5'in karıştırma ekleri | B2 1–9, 14, 17 | `karistirma_katmani` (grup) | karıştırmaya karşı | B2 çalışmaz, `kanal_dolulugu_ister` denmez; durum hep "yok", aralık ve kanıt yok, bit hep 0 (alan kalır); B1'in hariç aralık listesi boş; alt bayraklar etkisiz (B2 §10) |
| alıcının biti | B2 9–11 | `alici_bildirimi` | karıştırmaya karşı | bit hep 0 gider, alınan bit okunmaz, "bit değişti" olayı yok (alan kalır, boy aynı); kendi durumum ve aralıklar sürer; A, B olur (`18` §2.2) |
| göndericinin kanıtı | B2 12–13 | `gonderici_kaniti` | karıştırmaya karşı | gönderici olayı oluşmaz |

**Mekanizma kapısının "hepsi kapalı" kolu** (`06` §0.4.5): `karistirma_katmani` kapalı, genel mekanizmalar açık.

## Gözlemin kullanımı (`05`; mimari denetimi D17)

| bileşen | okur | okumaz |
|---|---|---|
| B1 | selam: göndereni, sırası, aralığı, benim için bildirilen oran (B6 çözer) · `iletim_sonucu`: hedef, başarı, `tekrar` (ölçüye yalnız tür `veri`; onayın gelmesi her türde varlık kanıtı) · `cerceve_duyuldu`: göndereni, yalnız tür `veri` ve `kontrol` · `saat_s` (yalnız süreler) | `olculen_gurultu_w` (yasak, K-227) · RSSI · `phy_hata` · `alinan_cerceve` · `mesgul_sure_s` · `kendi_konum` · `kendi_hiz` · `komsular` (simülatörün beacon listesi) · kuyruk · duyulan onay ve kontrol onayının göndereni (gerçek 802.11 onayı verici adresi taşımaz) |
| B2 | `mesgul_sure_s` (`kanal_dolulugu_ister`; yalnız `karistirma_katmani` açıkken) · `alinan_cerceve` · selam: göndereni ve karıştırma biti (B6 çözer) · B1'in çıktıları: selam örnekleri, `son_selam_t`, komşu kümesi ve olayları, veri kayıtları · `saat_s` (yalnız süreler) | `olculen_gurultu_w` (yasak, K-227) · RSSI · `phy_hata` · `kanal_mesgul_mu` · `iletim_sonucu` ve `cerceve_duyuldu` doğrudan (veri sonucu B1'in kaydından) · `kendi_konum` · `kendi_hiz` · `komsular` · kuyruk |

## Aşama 3'e açık kalanlar

- **Olay sırası:** B1, bir gözlemi işlemeden önce o ana kadarki kendi zaman olaylarını işler (B1 kural 20); `18` §1.4'ün olay sırasında gözlemin dağıtımı (1) zaman olaylarından (2) önce yazılı. Bütün bileşenler için ortak kural bütünlük denetiminde yazılır.
- **Bileşenler arası beklentiler:** B1'in B6'dan beklentileri (B1 §6, Ö-1…Ö-7); B3 ile B6 arasında komşulara hangi oranın bildirileceği (B1 §11 madde 3); B2'nin B6'dan beklentileri (B2 §6, Ö-1…Ö-5); B2'nin B3'e bıraktıkları (B2 §11 madde 2).
- **İskeletin kanca tablosu** (`18` §1.4): iletim sonucu B2'ye ayrıca dağıtılmaz; B2 veri sonucunu B1'in kaydından okur (B2 §2, sözleşme 3). Tablo bütünlük denetiminde buna göre düzeltilir.
- **B1'in sondaki sessizliği** (B1 kural 16): B2 kullanmıyor (B2 §2). B3 kullanmazsa kaldırılır.
- **İki meşgul payı eşiği:** `ED_ESIK` (0,55) ve `CBAR_ED_ESIK` (0,62). Birleştirmek ölçülen kuralı değiştirir; Aşama 4'te bakılır.
