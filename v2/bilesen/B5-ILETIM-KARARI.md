# B5 · İletim kararı

> Yeni tasarımın (`../18-YENI-TASARIM.md`) beşinci bileşeni. İskelet `18` §1.4; sorun, kanıt, seçenekler ve kararım `18` §2.5 (27 Kasım: A, tek yol). Teşhis ölçümü `arsiv/teshis/faz5_3_b5_iletim_kaybi_2026-11-26/` (`beklenti.md`, `sonuc.md`, `ek_hesap.txt`; bundan sonra "B5 teşhisi"). Değerler, bayraklar ve gözlemin kullanımı yalnız `00-DIZIN.md`de; burada adlarıyla anılır. Durum: onaylandı (27 Kasım). Önceki tasarımda karşılıkları `../kural/KK-04` kural 13 (eğimde getirene geri göndermeme) ve `../kural/KK-05` (bekletme ve komutun yolu); orada paket kararı rota kurallarının içindeydi.
>
> Eksiksizlik listesinin maddeleri (`18`): 1 §1 · 2–4 `18` §2.5 · 5 §2 · 6 §3 · 7 §4 · 8 §5 · 9 §6 · 10 §7 · 11 §8 · 12 §9 · 13 §10 · 14 §11 · 15 §12 · 16 §13 · 17 §14. Ölçülen ve ölçülmeyen §15.

## 1 · Amaç ve sınıf

B5 her veri paketi için, paket havaya çıkarken (atlama başına bir kez) üç soruyu cevaplar:
- **hangi komşuya:** telemetride B4'ün ardılına, komutta B7'nin geri izine;
- **şimdi mi:** yol varsa şimdi; yoksa B7'nin kararıyla bekletilir ya da düşer;
- **kopyalı mı:** hayır; paket tek komşuya gider.

Rota durumunu değiştirmez (`18` §1.4 sözleşme 5). Karıştırmaya karşılık B2 → B3 → B4 zincirinden gelir: karıştırılan bağ B3'te son çareye düşer, B4 olağan bir adaya geçer, B5 paketi o adaya gönderir.

**Sınıf:** genel (K-247), çekirdek. **Karıştırma eki yoktur.** B5 teşhisinde ailelerin hiçbiri elenmedi, ama hızlı sapmanın tetiği yok, kopya pahalı, kurtarma da genel bir mekanizma ve mekanizma kapısını zayıflatıyor (`18` §2.5).

**Hizmet ettiği hedef** (`18` §1.1):
- Ana hedefe dolaylı hizmet eder: karıştırılan bağdan kaçış B3'ün son çaresi ve B4'ün seçimiyle olur; B5 bu seçimi pakete uygular.
- Fazladan veri yayını eklemez. Kontrol payı ve kalabalık kanal koruma ölçütlerine dokunur: C1 kopyası koşu başına 81 s, kurtarma 41 s eklerdi (B5 teşhisi E6).
- Mekanizma kapısını bulandırmaz: kapının iki kolunda aynı çalışır (§11 madde 6).
- Bedeli: B5'in ailelerinin ulaşabileceği kayıp açık kalır (§15).

## 2 · Gördüğü (`05`; yasak alanlar okunmaz)

| kaynak | B5'in kullandığı | kullanmadığı |
|---|---|---|
| paket başlığı (`sonraki_atlama` kancasının gözlemi) | hedef: geçit mi | kaynak, `kaynak_sira`, atlama sayısı (döngü tanısı B4'ün, geri iz B7'nin) · kaynak rotası (kullanılmaz) |
| B4 | ardıl; açlık durumu | aday listesinin öteki üyeleri (yalnız tanı) · maliyetler (tanı) |
| B7 | açlıkta bekletme ya da düşürme kararı; komutun sonraki atlaması (B7'nin kâğıdında) | — |
| B1, B2, B3 | doğrudan okumaz (B4 üzerinden) | kendi durumum: karıştırma eki olmadığı için gerekmez |

**Okumadıkları:** gözlem sözleşmesinin öteki alanları · `olculen_gurultu_w` (yasak, K-227) · RSSI · kuyruk uzunluğu · konum ve hız.

## 3 · Tuttuğu

B5 durum tutmaz. Her karar o kancadaki B4 ve B7 durumundan verilir.

İskelet (`18` §1.4) B5'e paket başına kayıt öngörmüştü (getiren, gönderilen, denemeler); bunlar paket başına sapma ve kopya içindi, A'da gerekmedi. Paketi getiren komşu B7'nin geri izine ve B4'ün döngü tanısına gider (sözleşme 2). İskeletin B5 satırı Aşama 3'te düzeltilir (`00-DIZIN`).

**Bellek:** yok.

## 4 · Durumlar ve geçişler

B5'in durumu yoktur; her paket bir karar tablosundan geçer (kural 1–4):

| paket | B4 · B7 | karar |
|---|---|---|
| telemetri (hedef geçit) | ardıl var (O ya da S sınıfında) | ardıla |
| telemetri | ardıl yok (açlık) | B7'nin kararı: beklet ya da düşür |
| komut (hedef geçit değil) | B7 sonraki atlamayı veriyor | o komşuya |
| komut | B7 vermiyor | B7'nin kararı: beklet ya da düşür |

**Takılı kalma yok:** bekletilen paket B7'nin uyandırmasıyla yeniden sorulur ya da B7'nin kuralıyla düşer; uçan paket MAC'in 7 denemesiyle biter.

## 5 · Kurallar

**A · Karar**

1. **Telemetri:** paketin hedefi geçitse ve B4'ün ardılı varsa paket ardıla gider: `Karar(sonraki = ardıl)`. Ardılın sınıfına bakılmaz: ardıl S'deyse bu, olağan aday olmadığı içindir (B4 kural 5).
   - Gerekçe: en iyi aday B4'ün ardılıdır; rota durumu ile paket kararı ayrıdır (sözleşme 5).
   - Ardıl S'deyken göndermek göndermemekten iyidir. Girişimdeki alıcıya giden veri çerçevesi ortalama 3,9 deneme harcıyor (temizde 2,0; teşhis (d), `arsiv/teshis/faz5_2_isaretler_2026-11-16/sonuc.md` §3). Vazgeçme 7 deneme olduğu için bu çerçevelerin önemli bir kısmı yine ulaşıyor olmalı (varsayım; B3'ün E1 gerekçesi, `18` §2.3).
   - Kanal kilidindeki ardıl selam gönderemez. İlanı `ILAN_OMUR_KAT` · a sonra düşer (B4 kural 4); B4 başka bir adaya geçer ya da açlığa girer.
   - B5 teşhisinde J4'ün (karıştırılan ardıldan başka aday yok, 0,053) yalnız 0,011'i kanal kilidindeki alıcıdaydı, 0,042'si girişimdeydi (`ek_hesap.txt` E10, kuraldan sonra). Bu yüzden son çaredeki ardıl için ayrı bir bekletme kuralı koymadım: kazanabileceği pay küçük, girişimdeki ardıla gönderim ise çoğu zaman işe yarıyor.
2. **Açlık:** paketin hedefi geçitse ve B4'ün ardılı yoksa karar B7'nindir:
   - bekletme: `Karar(beklet = True)`;
   - ya da düşürme: `Karar(sonraki = None)`, B7'nin bildirdiği sebeple (`13` §02.5: `rota_gecersiz` beyanı ya da `hedef_yok`).

   B5 B7'nin kararını değiştirmez. B4 bu sırada açlık isteğini gönderir (B4 kural 11).
3. **Komut:** paketin hedefi geçit değilse sonraki atlama B7'nin geri izidir (`17` T-20; B7'nin kâğıdı). B7 bir komşu verirse paket ona gider; vermezse B7'nin bekletme ya da düşürme kararı uygulanır. Geçidin gönderdiği her veri paketi komuttur.
4. **Tek alıcı:** her paket tek komşuya gider.
   - Kopya yok: `Karar.kopyalar` boş.
   - Paket başına sapma yok: paket ardıl dışındaki bir adaya gitmez.
   - Kurtarma yok: MAC vazgeçince paket düşer (simülatörün kuralı); B5 o paketi yeniden yönlendirmez.
   - Kaynak rotası yazılmaz: `Karar.rota` boş.
   - Gerekçe `18` §2.5'te: B'nin tetiği yok; C pahalı; D genel, simülatöre yetenek ister ve kapının kolunda katmanın kurtaracağı paketleri de kurtarır.

**B · Zaman ve kendi durumum**

5. **Geç bağlama:** karar paket kuyruğa girerken değil, kuyruktan havaya çıkarken verilir (simülatörün kuralı: `sim2/kosum/gonderim.py`, `iletime_basla`). Ardıl değişince kuyruktaki paketler kendiliğinden yeni ardıla gider; ayrıca bir iş gerekmez. DSR'nin kuyruktaki paketler sorunu (RFC 4728 §3.4.2) böylece doğmaz. Yeniden denemeler aynı komşuya gider; protokole yeniden sorulmaz.
6. **Kendi karıştırılmam:**
   - **Kanal kilidinde** geri çekilme bitmez; protokole sorulmaz, paketler kuyrukta bekler (kuyruk dolarsa `kuyruk_tasmasi`). Kilit kalkınca ilk paket o anki ardılla gider.
   - **Girişimde** kural 1–5 aynen uygulanır. Çerçevem ardıla ulaşır ama onayını duyamam; MAC 7 kez dener. Alıcı çerçeveyi çözmüşse paket düşmez (simülatörün kuralı, `vazgec`). B4 bu sırada ardılı korur (B4 kural 4, 14).

**C · Sıra**

7. **Sıra:** B5 her `sonraki_atlama` kancasında, aynı kancada B1–B4 çalıştıktan sonra karar verir (`18` §1.4 olay sırası 4). Karar o kancanın B4 durumunu ve B7'nin cevabını kullanır.

## 6 · İletiler

B5 ileti göndermez; kontrol yüküne katkısı yoktur. Her paket atlama başına bir kez gönderilir; kopya ve kurtarma olmadığı için fazladan veri yayını yoktur.

B7'den beklediklerim (Aşama 2.7'de kapanır):
- **Ö-1** Açlıkta telemetri için karar: bekletme ya da düşürme, düşürmede sebep. Bekletmenin sınırı B7'nindir (`17` T-18: kısa ve küçük tampon).
- **Ö-2** Komutun sonraki atlaması (geri iz, `17` T-20) ya da bekletme ve düşürme.
- **Ö-3** Bekletilen paket için uyandırma: B7 paketi yeniden sordurur; B5 o anki ardılla karar verir (kural 1).
- **Ö-4** B7'nin cevabı B5'ten önce hesaplanır. İskelet B5'in B7'ye danışmasını öngörüyor; sözleşme 1'e göre B7 bu iş için B5'in altında sayılır (`00-DIZIN`, Aşama 3'e açık kalanlar).

## 7 · Değerler

B5'in kendi değeri yok. Kullandığı süreler ve sınırlar B4'ün (`ILAN_OMUR_KAT`) ve B7'nin kâğıdındadır.

## 8 · Kenar durumlar

- **Soğuk açılış:** B4'ün ardılı yok; kural 2 (B7).
- **Geçit:** geçidin telemetrisi yoktur. Geçide gelen telemetriyi simülatör teslim eder, B5'e sorulmaz. Geçidin gönderdiği her paket komuttur: kural 3.
- **Hiç komşu yok:** açlık, kural 2. **Tek komşu:** ardılsa (O ya da S) paket ona gider.
- **Hedef komşuysa:** telemetride hedef geçittir. Geçit komşuysa B4'ün adayıdır (yol maliyeti yalnız bağınki, M + 0) ve çoğu zaman ardıldır. B5 ayrıca bir "hedef komşu" kuralı koymaz. Geçide giden bağ bildirim ve gönderici kanıtıyla S'ye düşmez (B3 kural 8).
- **Düğüm kendisi karıştırılırken:** kural 6.
- **Komşu karıştırılırken:** ardıl S'ye düşer ve B4 olağan bir adaya geçer. Olağan aday yoksa paket S'deki ardıla gider (kural 1); B4 kural 10a bu sırada temiz bir aday açabilir.
- **Paket aynı düğüme daha büyük atlama sayısıyla dönerse:** B4'ün döngü tanısı sayar (B4 kural 17; uygulanabilirlik koşuluyla olmamalıdır). B5 yine kural 1'le karar verir.
- **Sayaç taşması:** B5'in sayacı yok.
- **Zaman aşımı:** B5'in yok. Paketin ömrü (TTL 64) simülatörün.
- **Aynı anda olaylar:** kural 7.
- **Tamponun dolması:** arayüz kuyruğu simülatörün (`kuyruk_tasmasi`), bekletme tamponu B7'nin.

## 9 · Arayüz

**Kancalar:**

| kanca | B5'e giden | B5'in işi |
|---|---|---|
| `sonraki_atlama` | paket başlığı (hedef) | B1–B4 (olay sırası 1–3), B7'nin cevabı, sonra kural 1–7 |
| öteki kancalar | — | — |

**Okuduğu:** B4 (ardıl, açlık durumu); B7 (bekletme kararı, komutun sonraki atlaması; Ö-4).

**Çıktılar:**

| çıktı | kural | okuyan |
|---|---|---|
| `Karar(sonraki)` ya da `Karar(beklet)`; kopya ve rota yok | 1–4 | simülatör |

B5 öteki bileşenlere bir şey vermez; veri yolunun en üstündedir.

## 10 · Kapalıyken davranış

B5'in bayrağı yoktur: paket B5 olmadan gönderilemez. Karıştırma eki yoktur; mekanizma kapısının kolunda (karıştırma katmanı kapalı) B5 aynı çalışır. Seçilmeyen ailelerin (sapma, kopya, kurtarma) bayrağı da yoktur, çünkü kodlanmayacaklar.

## 11 · Etkileşimler

1. **B4:** B5 aday listesinden yalnız ardılı kullanır. Listenin her üyesi uygulanabilir olduğu için döngü oluşmaz (B4 §15). Ardıl değişti olayı B5'e iş çıkarmaz (kural 5).
2. **B3:** S'deki bağa paket yalnız ardıl S'deyken, yani olağan aday yokken gider (E1).
3. **Kanıtı silmeme** (sözleşme 4):
   - S'deki ardıla giden paketler veri kaydı üretir; B2'nin gönderici kanıtı ve B3'ün "veri yok"u sürer.
   - Ardıl değişince eski ardıla paket gitmez, yeni kayıt oluşmaz. Kanıt B3 kural 6–7'nin süresiyle kalkar ve bağ yeniden denenir (B3 §11 madde 7). Bu, B3'te zaten yazılı etkileşimdir.
   - Paketi getiren komşunun bilgisi B5'te kullanılmaz ve silinmez; B4'e ve B7'ye gider.
4. **B2:** B5 B2'yi okumaz. Kendi karıştırılmamda karar değişmez (kural 6); kendi aralığıma düşen MAC sonuçları kanıttan B2'de ayıklanır (B2 kural 12–13).
5. **B7:** açlıkta ve komutta karar B7'nindir (kural 2–3). Bekletilen paket yeniden sorulunca kural 1'le karar verilir.
6. **Mekanizma kapısı:** B5 genel ve tek yollu olduğu için kapının iki kolunda aynı çalışır; karıştırma katmanının payını küçültmez. B5 teşhisinde J1'in (katmanın kurtarabileceği kayıp, 0,0485) yalnız 0,016'sı katmana aitti (`ek_hesap.txt` E7). Genel bir kurtarma kapının kolunda bu payı da kurtarırdı; D bu yüzden alınmadı.
7. **Simülatör:** atlama başına bir karar; MAC aynı komşuya en çok 7 kez dener; vazgeçilen paket alıcı çözmediyse düşer (`sim2/kosum/gonderim.py`, `sim2/kosum/kosu.py`). Kopya kullanılmadığı için kopya defteri boş kalır (`13` §07: kopya istemeyen protokolde hiçbir olay eklenmez).

## 12 · Örnek senaryo

i'nin komşuları j, k, l; B4'e göre ardıl j (O). Paketler telemetri.

1. **Olağan:** 100,0 s'de p kuyruk başında, geri çekilme biter. B4'ün ardılı j: karar "sonraki j". MAC j'ye dener, 2. denemede onay gelir.
2. **Ardıl karıştırılıyor:** 120,0 s'de j'nin biti 1'li selamı gelir; j B3'te S olur, B4 olağan aday k'ye geçer. Kuyruğa 119,8 s'de giren p2, 120,1 s'de havaya çıkarken sorulur: ardıl k, paket k'ye gider (kural 5).
3. **Olağan aday yok:** k de karıştırılıyor (S). B4 S'deki adaylardan en ucuzunu seçer, ardıl k kalır. p3 k'ye gider (kural 1). B4 kural 10a ile temiz ama uygulanamaz ilanlı l'ye tur isteği gönderir. Yeni tur gelince l O'da aday ve ardıl olur; p4 l'ye gider.
4. **Vazgeçme:** p5 k'ye 7 denemede de geçmez ve alıcı çerçeveyi çözmemiştir: paket düşer (simülatör). B5 onu yeniden göndermez (kural 4). Vazgeçme B1'in veri kaydına ve B2'nin gönderici sayımına girer.
5. **Açlık:** bütün komşular ∞ ilan eder, B4 açlıkta. p6 için karar B7'nindir; B7 bekletir (kural 2). B4 açlık isteğini gönderir. Yeni tur gelince ardıl doğar; B7'nin uyandırmasıyla p6 yeniden sorulur ve ardıla gider.
6. **Komut:** geçitten düğüm 12'ye giden q, i'nin kuyruğunda. Hedef geçit değil: sonraki atlama B7'nin geri izinden gelir (kural 3).
7. **Kendim kanal kilidinde:** 200,0–205,0 s arasında geri çekilme bitmez, protokole sorulmaz; paketler kuyrukta bekler. 205,1 s'de kilit kalkar, ilk paket o anki ardılla gider (kural 5–6).

## 13 · Sınanması

**Birim testleri** (Aşama 4):
1. Telemetri ardıla gider; ardıl O'da da S'de de.
2. Ardıl yokken B7'nin kararı uygulanır: bekletme; düşürme ve sebebi.
3. Komutun sonraki atlaması B7'den gelir; B7 vermiyorsa B7'nin bekletme ya da düşürme kararı.
4. Karar hiçbir zaman kopya ya da kaynak rotası taşımaz; paket ardıl dışında bir adaya gitmez.
5. Geç bağlama: ardıl değişince kuyruktaki paket yeni ardıla gider (simülatörle uçtan uca).
6. Sıra: aynı kancada B4 güncellendikten sonra karar verilir.
7. Örnek senaryonun (§12) sayıları uçtan uca.

**Ölçümde sayılacak tanı:**
- kararlar ardılın sınıfına göre (O, S); S'deki ardıla giden paketlerin sonucu;
- açlıkta B7'ye giden paketlerin sayısı ve sonucu;
- vazgeçilen paketler, alıcının alanına ve ardılın sınıfına göre (alan yalnız teşhiste, kâhinden);
- sıradaki adayın temiz olduğu vazgeçmeler: kurtarmanın açık bıraktığı pay (B5 teşhisinin J2 + J3 + U1'i).

## 14 · Kaynak

- **Paketin seçili rotanın sonraki atlamasına gönderilmesi:** mesafe vektörü ailesi; Babel, RFC 8966 [4] §3.5 (seçili rota), DSDV. Babel paket başına yön seçmez; bu tasarımda da öyle.
- **Seçilmeyenler ve kaynakları** (`18` §2.5):
  - kurtarma: DSR'nin "salvaging"i, RFC 4728 [52] §3.4.1, §8.3.6;
  - kopya: JarmRout [51] (her pakete iki yol, K-230); önceki tasarımın son çare çoğaltması (`17` T-14);
  - paket başına sapma: önceki tasarımda eğimin getirene geri göndermeme kuralı (`../kural/KK-04` kural 13);
  - fırsatçı iletim (ExOR, ORW): MAC'te yeni bir iletim türü ister (`protokol_kaynaklari/faz5_3_arastirma_2026-11-19/NOTLAR.md` §3).
- **Bu tasarımın:** ailelerin bu dünyadaki kazancının ve bedelinin karar anındaki duruma göre ölçülmesi (B5 teşhisi) ve tek yolun kapının ayrımını koruduğu için seçilmesi.

## 15 · Ölçülen ve ölçülmeyen

**Ölçülen** (B5 teşhisi; bugünkü kodun `eğim0` kolunun trafiği; ağırlıklı paylar kâhine göre üst sınır):
- açık dönemde iletim kaybının yeri: J1 0,0485 · J2 0,022 · J3 0,036 · U1 0,043 (ağırlıklı) · J4 0,053 · J5 0,006 · U2 0,037 (ham) (K1);
- hızlı sapmanın tetiği yok (K3);
- kopyanın bedeli: C1 koşu başına +81 s; C2 ucuz ama 0,004'e ulaşıyor (K4, E2, E6);
- kurtarmanın üst sınırı birincilde 0,100, ikizde 0,0525; yayın eki 41 s (K5, E4, E6);
- katmanın J1'deki kendi payı en çok 0,016 (E7).

**Ölçülmeyen** (Aşama 4'te sayılır):
- A'nın kendisi: iletim kaybının yeni tasarımdaki dağılımı. Teşhis bugünkü kodun trafiğindeydi; yeni tasarımda ardıl kanıtla değişince trafik de değişir.
- S'deki ardıla göndermenin kazancı ve bedeli.
- Açık bırakılan pay: B5'in ailelerinin ulaşabileceği J2 + J3 + U1. Aşama 4'te hedef tutmazsa ilk düşünülecek kaldıraç kurtarmadır; kapıya etkisi o zaman yeniden hesaplanır (`18` §2.5).
