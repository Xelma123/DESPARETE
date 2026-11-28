# B7 · Bekletme ve komut

> Yeni tasarımın (`../18-YENI-TASARIM.md`) yedinci bileşeni. İskelet `18` §1.4; sorun, kanıt, seçenekler ve kararım `18` §2.7 (27 Kasım: H1, kısa bekletme; K1, geri iz). Bugünkü bekletmenin ve komutun sayıları `arsiv/teshis/faz5_3_b7_bekletme_2026-11-27/bekletme_komut.txt`'te (kayıtlardan hesap, yeni koşu yok). Değerler, bayraklar ve gözlemin kullanımı yalnız `00-DIZIN.md`de; burada adlarıyla anılır. Durum: onaylandı (27 Kasım); 28 Kasım'da bağımsız denetimden sonra düzeltildi (kural 3, §8; `../../arsiv/denetim/DENETIM-TASARIM-KAPANIS-2026-11-28.md`). Önceki tasarımda karşılığı `../kural/KK-05` (bekletme ve komutun yolu).
>
> Eksiksizlik listesinin maddeleri (`18`): 1 §1 · 2–4 `18` §2.7 · 5 §2 · 6 §3 · 7 §4 · 8 §5 · 9 §6 · 10 §7 · 11 §8 · 12 §9 · 13 §10 · 14 §11 · 15 §12 · 16 §13 · 17 §14. Ölçülen ve ölçülmeyen §15.

## 1 · Amaç ve sınıf

B7 iki soruyu cevaplar:
- **Bekletme:** yol yokken paket ne kadar tutulur, ne zaman yeniden sorulur, ne zaman düşer? Yol yokluğu, telemetride B4'ün ardılının olmaması (açlık), komutta taze ve kullanılır bir geri izin olmamasıdır.
- **Komutun yolu:** geçitten bir İHA'ya giden komut hangi komşuya verilir? Cevap: o İHA'nın telemetrisini bana getiren komşu (geri iz).

B5'e bu iki cevabı verir (B5 §6, Ö-1…Ö-4); paketi kendisi göndermez.

**Sınıf:** genel (K-247), çekirdek. Karıştırma eki yoktur.

**Hizmet ettiği hedef** (`18` §1.1):
- Koruma ölçütlerinden gecikmenin p99'u. Bekledikten sonra teslim edilen paketler birincilde teslimin %2'si olduğu için p99'u bekletmenin süresi belirliyor (`18` §2.7).
- Kısa açlıkları köprüleyerek rota yokluğu kaybını azaltır. Bugün birincilde bekletilen paketlerin %38'i yol bulununca gidiyor.
- Komutların teslimi: komutlar paketlerin ~%2,4'ü ve `PDR_açık`'a girer.

## 2 · Gördüğü (`05`; yasak alanlar okunmaz)

| kaynak | B7'nin kullandığı | kullanmadığı |
|---|---|---|
| paket başlığı (`sonraki_atlama`) | kaynak, hedef, `kaynak_sira` | atlama sayısı (B4'ün aynı düğüme dönüş tanısı) · kaynak rotası |
| `cerceve_duyuldu` (niyet döndürmez) | tür `veri`, bana adresli çerçevenin göndereni ve paket başlığı (kaynak, hedef, `kaynak_sira`) | RSSI · başkasına adresli çerçeveler · onay ve kontrol çerçeveleri |
| B1 | silinen komşu olayı | ölçüler |
| B3 | izin gösterdiği komşunun durumu (KULLANILMAZ mı) | maliyet, sebepler |
| B4 | ardıl var mı (açlık); açlıktan çıkış ("ardıl değişti" olayı). "Daha önce ardıl oldu mu" bilgisini B7 bundan kendisi tutar (§3) | aday listesi, maliyetler |
| yapılandırma | geçidin kimliği; ben kimim | — |
| `saat_s` | yalnız süreler | — |

**Okumadıkları:** `olculen_gurultu_w` (yasak, K-227) · RSSI · kuyruk uzunluğu · konum · B2 (karıştırma eki yok).

## 3 · Tuttuğu

| alan | anahtar | başlangıç | güncellenir | silinir | üst sınır |
|---|---|---|---|---|---|
| ilk bekletme anı | paket kimliği (kaynak, `kaynak_sira`) | yok | paket ilk bekletildiğinde (kural 1) | paket gidince ya da düşünce; `TUTMA_EN_COK_S` + `BEKLEME_KAYIT_PAYI_S`'den eskiyse (kural 5) | bekletme tamponu kadar (simülatörde 64) ve yeniden sorulmakta olanlar |
| geri iz: (komşu, `kaynak_sira`, an) | kaynak | yok | kural 6 | — (kural 7: gösterdiği komşu silinince geçersiz) | düğüm sayısı (en çok 255) |
| hedef biliniyor mu | hedef | hayır | ilk izde evet (komut); ilk ardılda evet (telemetri, B4) | — | düğüm sayısı |
| yeniden sorma planı: anı ve nesli | düğüm | yok | kural 3 | plan dolunca | bir |

**Bellek:** bekletme kaydı tamponla sınırlı; iz ve "biliniyor" düğüm sayısıyla.

## 4 · Durumlar ve geçişler

Bir paketin B7'deki yaşamı:

| durum | koşul | çıkış |
|---|---|---|
| yolu var | telemetride ardıl var; komutta iz taze ve komşusu kullanılır | B5 gönderir |
| bekletiliyor | yol yok, ilk bekletmeden beri `TUTMA_EN_COK_S` geçmedi | yol gelince gönderilir; süre dolunca düşer (kural 2) |
| düştü | yol yok ve süre doldu | sebebi kural 4'te |

**Takılı kalma yok:** her bekletilen paket en geç `TUTMA_EN_COK_S` + `YENIDEN_SOR_S` içinde yeniden sorulur ve ya gider ya düşer. Simülatörün tavanları (64 paket, 30 s) bunu ayrıca sınırlar.

## 5 · Kurallar

**A · Bekletme** (H1)

1. **Yol yokken:** B5 sorunca yol yoksa (telemetride B4'ün ardılı yok; komutta kural 8'in komşusu yok) cevap "beklet"tir: `Karar(beklet = True)`. Paketin bu düğümdeki ilk bekletme anı kimliğiyle (kaynak, `kaynak_sira`) tutulur. Bu, AODV'nin yol beklerken veriyi tamponda tutmasıdır (RFC 3561 §6.3, SHOULD).
2. **Yeniden sorulunca:**
   - yol varsa paket gider; kayıt silinir;
   - yol yoksa ve ilk bekletmeden beri `TUTMA_EN_COK_S` geçtiyse paket düşer (kural 4);
   - değilse yine bekletilir.

   Sınır atlama başınadır: paket her rölede en çok `TUTMA_EN_COK_S` bekler. Paketin yaşı protokole görünmez ve başlığa değer yazılamaz (K-232). Bu yüzden paket başına toplam bütçe (H4) seçilmedi.
3. **Yeniden sorma** (uyandırma; simülatör tamponu yalnız uyandırmadan sonra döker, K-135):
   - **yol gelince hemen:** B4 açlıktan çıktığı kancada ("ardıl değişti", öncesi ardılsız), ya da bekleyen komutun hedefine taze iz doğduğunda, B7 en kısa gecikmeli bir uyandırma döndürür (simülatörün alt sınırı bir yuva, `13` §03.5);
   - **aralıkla:** tamponda paket varken her `YENIDEN_SOR_S`'de bir uyandırma kurulur. Süresi dolanlar böylece düşer; komutun izi niyet döndürmeyen bir kancada tazelendiyse en geç bu aralıkta görülür.
   - Plan nesil numaralıdır; eski nesil yok sayılır. Daha erken bir plan varken yenisi kurulmaz; plan dolunca tamponda paket kaldıysa bir sonraki kurulur (bugünkü kodun kuralı, `protokoller/desparete5.py`; 28 Kasım, bağımsız denetim K-6).
   - Simülatör tamponu her uyandırmadan sonra döker (B6'nın selam uyandırması dâhil). Bu yalnız daha sık yeniden sormadır, zararı yok.
4. **Düşmenin sebebi** (ölçüm beyanı, K-134 · K-139; simülatör sebebi beyana bakar): paket bu düğümde daha önce yolu bilinen bir hedefe gidiyorsa `Karar(sonraki = None)` ile `Beyan("rota_gecersiz")` döner, değilse beyansız (`hedef_yok`).
   - Telemetride "biliniyor": B4'te bu düğüm daha önce ardıl kurmuştu.
   - Komutta "biliniyor": hedefin izi bir kez öğrenilmişti.
5. **Kaydın temizlenmesi:** `TUTMA_EN_COK_S` + `BEKLEME_KAYIT_PAYI_S`'den eski ilk bekletme kaydı silinir. Simülatörün tavanıyla düşen paketin (`tampon_asimi`) kaydı böylece kalmaz, gereksiz uyandırma da üretmez.

**B · Komutun yolu** (K1; v0.4.1'in V11'i, `17` T-20)

6. **Geri izin öğrenilmesi:** tür `veri`, bana adresli ve hedefi geçit olan bir telemetri çerçevesi `cerceve_duyuldu` ile gelince (kaynak ben değilken) `iz[kaynak]` ← (gönderen, `kaynak_sira`, şimdi). Bunun koşulu, paketin `kaynak_sira`sının izdekinden yeni olmasıdır (16 bit, modüler; `00-DIZIN` ortak birimler).
   - Sebep: izden ize ilerleyen her adımda sıra azalmaz. Çapraz giden iki paket iki düğümü birbirine gösteremez; komut ancak aynı telemetri paketinin yolunda bir döngüyle döngüye girebilirdi. O yol da uygulanabilirlik koşuluyla döngüsüzdür (B4 §15).
   - Geçit de izi kendisine gelen telemetriden öğrenir.
   - Bu kanca niyet döndürmez. Bekleyen bir komutun hedefine iz doğarsa bir sonraki niyetli kancada hemen yeniden sorulur (kural 3).
7. **İzin geçersizliği:** izin gösterdiği komşu B1'de silinince iz geçersizdir; hedef yine "biliniyor" sayılır (kural 4).
8. **Komutun kararı:** hedefin izi varsa, `IZ_TAZELIK_S` içindeyse ve gösterdiği komşunun B3 durumu KULLANILMAZ değilse komut o komşuya gider. Değilse bekletilir (kural 1–3); hedefin bir sonraki telemetrisi izi tazeler (her İHA saniyede bir telemetri gönderir).
   - İzin komşusu son çaredeyse (S) komut yine ona gider. Gerekçe: komutun bildiğim tek yolu odur. Bekletmek çoğu zaman bir şey kazandırmaz: girişimdeki komşu gönderebildiği için hedefin telemetrisini bana getirmeyi sürdürür, iz yine onu gösterir. Göndermek ise şans verir: girişimdeki alıcıya giden çerçevenin bir kısmı ulaşır (B3'ün E1 gerekçesi, `18` §2.3). Bugünkü kodda komutlar açık dönemde %22, telemetri %30 kayıpla iletildi (`bekletme_komut.txt`).
   - Seçilmeyen: önceki tasarımın kuralı, yani iz karıştırılan komşuyu gösterince komutu bekletmek (KK-05 kural 8). Bekleyişin sonunda iz büyük olasılıkla yine aynı komşuyu gösterir.
9. **Komut ve telemetri aynı tamponu paylaşır;** öncelik yoktur. Simülatör tamponu sırayla döker ve arayüz kuyruğunun sonuna koyar.

**C · Sıra**

10. **B7'nin cevabı B5'ten önce hesaplanır** (B5 Ö-4). Her `sonraki_atlama` kancasında B1–B4'ten sonra B7 yol var mı sorusunu cevaplar, sonra B5 karar verir (olay sırası 4). B7'nin yeniden sorma uyandırması olay sırasının 6. adımında döner. İskelet B5'in B7'ye danışmasını öngörür. Sözleşme 1'e (yalnız aşağıdakini okur) göre B7 bu iş için B5'in altında sayılır; iskelete 28 Kasım'da işlendi (`18` §1.4 sözleşme 1).
11. **Niyetsiz kanca:** `cerceve_duyuldu`'da yalnız iz öğrenilir (kural 6); uyandırma bir sonraki niyetli kancada döner.

## 6 · İletiler

B7 ileti göndermez; kontrol yüküne katkısı yoktur. Yeniden sorma uyandırmaları simülatörün olaylarıdır, kanal süresi harcamaz.

**B5'in beklentilerine karşılık:**

| beklenti | karşılığı |
|---|---|
| Ö-1 açlıkta telemetri için karar | kural 1–2, 4 |
| Ö-2 komutun sonraki atlaması | kural 6–8 |
| Ö-3 bekletilen paket için uyandırma | kural 3 |
| Ö-4 B7'nin cevabının B5'ten önce olması | kural 10 |

## 7 · Değerler

`TUTMA_EN_COK_S` · `YENIDEN_SOR_S` · `IZ_TAZELIK_S` · `BEKLEME_KAYIT_PAYI_S`. Simülatörün tavanları (bekletme tamponu 64 paket, 30 s) protokolün değeri değildir; her protokole aynıdır. Değeri, birimi, kaynağı, küçük ve büyük olursa ne olacağı ve taranıp taranmayacağı `00-DIZIN.md`'nin değer tablosunda.

## 8 · Kenar durumlar

- **Soğuk açılış:** henüz ardıl yokken gelen telemetri bekletilir. 1 s içinde yol kurulmazsa düşer; hedef "biliniyor" değildir, sebep `hedef_yok`.
- **Geçit:** geçidin telemetrisi yoktur; bekletme yalnız komut içindir. Komutun izi geçide gelen telemetriden öğrenilir. Henüz telemetrisi gelmemiş bir İHA'ya giden komut bekletilir, iz doğmazsa `hedef_yok` ile düşer.
- **Hiç komşu yok:** açlık; paketler 1 s bekletilir ve düşer.
- **Hedef komşuysa:** iz hedefin kendisini gösterir (telemetrisini doğrudan getirdiği için); komut doğrudan ona gider.
- **Düğüm kendisi karıştırılırken:**
  - tam kilitte protokole sorulmaz (B5 kural 6). Tampondaki paketler uyandırmayla arayüz kuyruğuna geçer ama havaya çıkamaz;
  - kanal açılınca sorulurlar: yol varsa gider. Yoksa ilk bekletme kaydı duruyorsa ve süre dolduysa düşer; kayıt silinmişse (kural 5) paket yeni sayılır ve en çok `TUTMA_EN_COK_S` daha bekletilir (28 Kasım, bağımsız denetim K-3);
  - girişimde kurallar aynıdır.
- **Komşu karıştırılırken:** izin komşusu son çaredeyse komut yine gider (kural 8).
- **Sayaç taşması:** `kaynak_sira` 16 bit, modüler karşılaştırılır.
- **Zaman aşımı:** bekletme (kural 2), kaydın temizlenmesi (kural 5), izin tazeliği (kural 8).
- **Aynı anda olaylar:** aynı kancada hem açlıktan çıkış hem süre dolumu varsa önce yol denetlenir: yol varsa paket gider.
- **Tamponun dolması:** simülatörün sayı tavanı (64), en eski düşer (`tampon_asimi`); kaydı kural 5 siler.

## 9 · Arayüz

**Kancalar:**

| kanca | B7'ye giden | B7'nin işi |
|---|---|---|
| `sonraki_atlama` | paket başlığı | kural 1–2, 4, 8 (B5'ten önce), sonra kural 3'ün uyandırması |
| `cerceve_duyuldu` (niyetsiz) | gönderen, tür, hedef, paket başlığı | kural 6 |
| `uyandi` (B7'nin planı) | etiket (nesil) | tampon simülatörce dökülür; B7 yeni planı kurar (kural 3) |
| öteki niyetli kancalar | — | açlıktan çıkış ya da yeni iz varsa hemen yeniden sorma (kural 3); kural 5; B1'in silinen komşu olayıyla kural 7 |

**Okuduğu:** B1, B3, B4 (§2); B5 B7'nin cevabını okur (kural 10).

**Çıktılar:**

| çıktı | kural | okuyan |
|---|---|---|
| yol var mı; komutun sonraki atlaması | 1–2, 8 | B5 |
| bekletme ya da düşürme (sebebiyle) | 1–2, 4 | B5 (simülatöre `Karar`) |
| yeniden sorma uyandırması | 3 | simülatör |

## 10 · Kapalıyken davranış

- **`bekletme` kapalı** (genel): yol yoksa paket hemen düşer, sebebi kural 4'le (seçenek H3, Babel'in davranışı). Komut da öyle.
- **Geri iz** çekirdektir, bayrağı yoktur: komutun başka bildiğim yolu yoktur.
- Karıştırma katmanı kapalıyken B7 aynı çalışır; izin komşusunun son çare olması karıştırma ekinden (bildirim, gönderici) ya da "veri yok"tan gelir.

## 11 · Etkileşimler

1. **B4:**
   - açlıkta paketler bekletilir; B4 bu sırada açlık isteğini gönderir (B4 kural 11);
   - açlıktan çıkışta tampon hemen yeniden sorulur (kural 3);
   - B4 kural 10a ve 4a açlığı azaltmaya yöneliktir. Bekletme yalnız kalan kısa açlıkları köprüler.
2. **B5:** B7'nin cevabını uygular (B5 kural 2–3). B5 durum tutmadığı için bekletilen paket yeniden sorulunca o anki ardılla karar verilir.
3. **B3:** izin komşusu KULLANILMAZ ise komut bekletilir, son çaredeyse gider (kural 8; E1).
4. **B1:** silinen komşu izi geçersiz kılar (kural 7). İz `cerceve_duyuldu`dan öğrenilir; B1 de aynı kancayı varlık kanıtı için kullanır.
5. **B6:** B7 ileti göndermez. B6'nın selam uyandırması da tamponu döktürür (kural 3).
6. **Kanıtı silmeme** (sözleşme 4): B7 hiçbir gözlemi silmez. Bekletme, bekletilen paketin bağlarda kayıt üretmesini geciktirir; kanıt kaybolmaz, çünkü yol yokken gönderilecek bağ yoktur.
7. **Gecikme:** bekletme gecikmenin p99'unu belirler (§1). `TUTMA_EN_COK_S` büyürse p99 onunla büyür.
8. **Mekanizma kapısı:** B7 genel; kapının iki kolunda aynı çalışır.

## 12 · Örnek senaryo

Düğüm i; yeniden sorma aralığı 0,5 s.

1. **Kısa açlık:** i'nin B4'ü 200,00 s'de açlığa girer.
   - p1 (kaynak 7, sıra 120) 200,10'da sorulur: beklet; ilk bekletme 200,10. Uyandırma 200,60'a kurulur.
   - p2 200,40'ta gelir: beklet (ilk 200,40).
   - 200,60'ta tampon dökülür: açlık sürüyor. p1'in yaşı 0,50, p2'ninki 0,20: ikisi de bekletilir; uyandırma 201,10'a.
   - 200,85'te B4'ün tur isteğine yanıt gelir, l ardıl olur. B7 bir yuvalık uyandırma döndürür; tampon hemen dökülür, p1 ve p2 l'ye gider. Bekleme p1'de 0,75 s, p2'de 0,45 s.
2. **Uzun açlık:** 210,00–212,50 arasında açlık.
   - p3 210,20'de bekletilir; 210,70'te yaşı 0,50, yine bekletilir.
   - 211,20'de yaşı 1,00 ≥ `TUTMA_EN_COK_S`: düşer. i daha önce ardıl kurmuştu: `rota_gecersiz`.
3. **Taze iz:** `iz[12]` = (k, 345, 215,30). Geçitten gelen komut q (hedef 12) 216,00'da sorulur. İz 0,70 s önce tazelendi ve k OLAĞAN: q k'ye gider.
4. **İzin komşusu son çarede:** k girişime girer, biti 1, B3'te S. 217,00'deki q2 yine k'ye gider (kural 8).
5. **Bayat iz:** 12'nin son telemetrisi 220,00'de geldi.
   - q3 223,50'de sorulur: izin yaşı 3,50 > `IZ_TAZELIK_S`, bekletilir; uyandırma 224,00'a.
   - 223,90'da 12'nin telemetrisi m'den gelir: `iz[12]` = (m, 352, 223,90).
   - 224,00'te tampon dökülür, q3 m'ye gider; bekleme 0,50 s.
6. **İzin komşusu silinmiş:** k B1'de silinir; iz geçersizdir. q4 bekletilir. 1 s içinde yeni iz doğmazsa düşer; hedef biliniyordu: `rota_gecersiz`.

## 13 · Sınanması

**Birim testleri** (Aşama 4):
1. **Bekletme:**
   - yol yokken beklet, ilk anın tutulması;
   - yol gelince gönder ve kaydın silinmesi;
   - `TUTMA_EN_COK_S` dolunca düş (tam eşitlik dâhil);
   - bayrak kapalıyken hemen düş.
2. **Sebep:** biliniyorsa `rota_gecersiz` beyanı, değilse beyansız (`hedef_yok`); telemetride ve komutta.
3. **Yeniden sorma:**
   - açlıktan çıkışta ve yeni izde en kısa uyandırma;
   - paket varken `YENIDEN_SOR_S` aralığı;
   - nesil numarası; tampon boşken uyandırma yok.
4. **Kaydın temizlenmesi:** `TUTMA_EN_COK_S` + `BEKLEME_KAYIT_PAYI_S`.
5. **Geri iz:**
   - yalnız bana adresli, hedefi geçit telemetri çerçevesinden;
   - yalnız daha yeni sırayla; 65535 → 0 taşması;
   - kendi telemetrimden öğrenilmez;
   - geçitte öğrenme.
6. **Komutun kararı:** taze iz ve OLAĞAN komşu; S komşu (gider); KULLANILMAZ komşu (beklet); silinmiş komşu (beklet, biliniyor); bayat iz (beklet).
7. **Döngüsüzlük (uçtan uca):** küçük test dünyasında komutların hiçbiri aynı düğüme iki kez uğramaz.
8. Örnek senaryonun (§12) sayıları uçtan uca.

**Ölçümde sayılacak tanı:**
- açlık bölümleri ve süresi (B4'le birlikte);
- bekletilen paket, bekledikten sonra giden ve süresi dolan payları; bekledikten sonra gidenin teslimdeki payı (p99'un sebebi);
- düşme sebebine göre sayılar (`rota_gecersiz`, `hedef_yok`, `tampon_asimi`);
- komut: izli giden, izi S komşuya giden ve sonucu, bekletilen, düşen; komutun teslimi ayrı.

## 14 · Kaynak

- **Yol beklerken veriyi tamponda tutmak:** AODV, RFC 3561 §6.3 (SHOULD; ilk giren ilk çıkar). Simülatörün tamponu NS-2'nin `aodv_rqueue`su gibi dolunca en eskiyi atar (`sim2/kosum/dugum.py`).
- **Bekletmenin süresi ve atlama başına sınır:** önceki tasarım (`17` T-18, `../kural/KK-05`); v0.4.1'de alan başına 6 paket, 6 s.
- **Geri iz:** v0.4.1'in V11'i (K-172; `17` T-20); yalnız daha yeni sırayla güncelleme kodlamada (18 Kasım, G-1).
- **Bu tasarımın:**
  - izin komşusu son çaredeyken komutun yine gönderilmesi (E1'in komuta uygulanması);
  - açlıktan çıkışta ve yeni izde tamponun hemen yeniden sorulması;
  - düşme sebebinin "biliniyor"la ayrılması (beyanın anlamı ortak, K-139).

## 15 · Ölçülen ve ölçülmeyen

**Ölçülen** (bugünkü kodun `eğim0` kolu, aynı bekletme ve geri iz; `bekletme_komut.txt`):
- açlık: birincilde koşu başına 103 bölüm, ortalama 2,1 s; ikizde 18, ortalama 1,1 s;
- bekletilenlerin %38'i yol bulununca gidiyor, %62'si süresi dolup düşüyor (birincil);
- bekledikten sonra gidenler teslimin %2,1'i (birincil); p99 1,08 s (Babel 1,31 s);
- komutların açık dönemde iletim kaybı %22 (telemetri %30).

**Ölçülmeyen** (Aşama 4'te sayılır ya da ablasyonla ölçülür):
- yeni tasarımdaki açlığın sıklığı (B3'ün eşiksiz maliyeti, B4 kural 4a ve 10a ile);
- `bekletme`'nin katkısı (H1 ↔ H3);
- izin komşusu son çaredeyken komut göndermenin etkisi;
- değerler (`TUTMA_EN_COK_S`, `IZ_TAZELIK_S`). `TUTMA_EN_COK_S`'nin büyümesi p99'la sınırlıdır.
