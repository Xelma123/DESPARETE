# Bütünlük denetimi — yedi bileşen birlikte

> Aşama 3'ün ilk adımı (`../18-YENI-TASARIM.md` Aşama 3 madde 1): bütün bileşenler birlikte, `18`'in "Bütünlük denetiminde" listesine göre (madde 1–6; madde 7 bağımsız denetimin). Kâğıtlar `B1`…`B7`, değerler, bayraklar ve gözlemin kullanımı `00-DIZIN.md`. Hesaplar kayıtlardan, yeni koşu yok: `arsiv/teshis/faz5_3_butunluk_2026-11-27/butunluk_hesap.txt`, B6'nın `kontrol_bedeli.txt`'i, B7'nin `bekletme_komut.txt`'i. Durum: onaylandı (28 Kasım).

## Özet

- **Değerler** (madde 1): 54 değer, hepsi `00-DIZIN`'de bir kez tanımlı ve kâğıtlarda kullanılıyor; değer tablosunun kural atıfları doğru.
- **İletiler** (madde 2): iki ileti, selam ve tur isteği. Protokolün kendi iletilerinin kanal payı kabaca %3, veri onaylarıyla %6–7; hedefin sınırı %10, Babel %15.
- **Durumların birleşimi** (madde 3): bileşenler arasında çelişki yok. Bir etkileşim kayıtlardan ölçüldü: ilanın ömrü, girişimdeki son çare ardılı aday dışı bırakabiliyor. Bedelin üst sınırı 0,002; değişiklik gerekmiyor (§3).
- **Olay sırası:** bütün bileşenler için ortak kural yazıldı (§4): B1'in zaman olayları gözlemden önce, B7'nin cevabı B5'ten önce.
- **Uçtan uca senaryolar** (madde 4): altısı da kâğıtların kurallarıyla baştan sona yürüyor (§5).
- **İzlenebilirlik ve ilkeler** (madde 5–6): her hedef ve her ilke en az bir kurala, bir sınamaya ve bir ölçüme bağlı (§6–7).
- **Düzeltmeler** (§11; kuralların hiçbiri değişmedi):
  - iskelet (`18` §1.4): tablo, sözleşme 1, 2 ve 7, olay sırası ve kanca tablosu onaylı kâğıtlara göre düzeltildi;
  - B1 kural 16 (sondaki sessizlik) kaldırıldı;
  - B5'in kararından önce yazılmış dokuz anış düzeltildi (B2'de beş, B3'te üç, B4'te bir). Bunlar B5'e karıştırma eki ve paket başına karar, son çaredeki ardıl için de bekletme öngörüyordu;
  - B4'ün döngü tanısının girdisi ve kaydı yazıldı; B4 §2 başlığı okunmayanlar arasında sayıyordu, §3'te kaydı yoktu.
- **Mekanizma kapısı** (§10): karıştırma katmanının kendine ait payı ince. Ölçülmüş üst sınırların toplamı ~0,03; ayrıca ölçülmemiş bir pay var. Aşama 4'ün beklentisinde kapının tutmama olasılığı açıkça yazılmalı.

## 1 · Değerler tek yerde (madde 1)

Tarama (27 Kasım; `00-DIZIN`'in değer tablosu ile `B1`…`B7`'nin metni):
- `00-DIZIN`'de 54 değer var; hiçbiri iki kez tanımlı değil.
- Her değer en az bir kâğıtta adıyla anılıyor; kâğıtlarda anılıp `00-DIZIN`'de olmayan yeni tasarım değeri yok. `KENDI_UST_SURE` ve `T_HATIRA` önceki tasarımın adları, yalnız gerekçede anılıyor.
- Değer tablosunun "kural" sütunundaki her atıf (ör. B4/4a, B6/4–5, B7/1–2) kâğıtta var olan bir kurala gidiyor.
- Kâğıtlardaki sayılar ya bir değerin adıyla anılıyor ya da kanıt ve örnek sayısı.

Değerlerin bileşenlere dağılımı: B1 11 · B2 13 · B3 5 · B4 13 · B6 8 · B7 4. B5'in kendi değeri yok.

## 2 · İletiler ve kontrol payı (madde 2)

| ileti | alanlar | boy | gönderen kural | kime |
|---|---|---|---|---|
| selam | sıra 16 · aralık 16 · tur 16 · maliyet 16 · bit 1 · komşu listesi (adres 8, oran 8) × n | 9 bayt + 2n + 64; 15 komşuyla 103 bayt (1,02 ms), 39 komşuyla 151 bayt (1,40 ms) | B6 kural 1, 4–11 | çoklu yayın, titreşimli |
| tur isteği | istenen tur 16 · kalan atlama 8 | 3 + 64 = 67 bayt | B6 kural 2 (içerik B4 kural 4a, 10, 10a, 11, 12) | açlıkta çoklu yayın, titreşimli; öteki hâllerde tek alıcılı, 7 deneme |

Başka ileti yok. Komut ve telemetri veri çerçevesidir.

**Kontrol payının kestirimi** (birincil; protokolün kendi iletileri; kaba kestirim):

| kalem | dayanak | pay |
|---|---|---|
| selam ve bugünkü tur istekleri (bugünkü biçim ve zamanlama, ara ilanlar dâhil) | ölçüldü, `eğim0`: düğüm başına saniyede 0,67 selam, ~100 bayt (`kontrol_bedeli.txt`; `18` §2.6) | %2,7 |
| bit değişimiyle öne çekilen selamlar | B2 §6: 30 s'lik çevrimde ağda ~16 ek selam; selam sayısının ~%2'si | ~%0,05 |
| kural 4a'nın rota istekleri ve yanıt selamları | ardılın iki selamı art arda kaybolunca bir istek. Temiz kanalda ilan kararların %2,1'inde 3,5 · a'dan eski (B5 teşhisi E9); selam kaybı bağımsızsa ardılın selam kaybı ~0,27, iki kayıp ~%7,5. Düğüm başına saniyede ~0,05 istek; her biri ~2 ms (istek, onay, yanıt selamı) | ~%0,4 |
| açlık, yok sayma ve 10a'nın tur istekleri | açlık ve yok sayma istekleri bugünkü sayıma dâhil; 10a seyrek (en çok `YOK_SAYMA_S`'de bir) | ~0 |
| **toplam (protokolün iletileri)** | | **~%3** |
| veri çerçevelerinin MAC onayları (simülatör kontrol sayar) | ölçüldü: %3,2–3,4 (`18` §2.6) | %3,2–3,4 |
| **kontrol payı (koruma ölçütünün tanımı)** | | **~%6–7** |

Hedefin sınırı %10, Babel'in payı %15 (kendi iletileri %11). Kestirimlerin dayandığı selam kaybı bağımsızlığı bir varsayımdır; sayılar Aşama 4'te ölçülür (B6 §13'ün tanısı, iletiler ve onaylar ayrı).

## 3 · Durumların birleşimi (madde 3)

Her durumda yedi bileşenin yaptığı (i, bakılan düğüm; j, ardılı):

| durum | B1 | B2 | B3 | B4 | B5 | B6 | B7 |
|---|---|---|---|---|---|---|---|
| sakin | iki yönü ölçer | yok | OLAĞAN, maliyet selamdan | ardıl, sıralı adaylar | ardıla | aralık 1, 2, 2… s | izi öğrenir, komut izle |
| j girişimde | j'nin selamlarının bir kısmı kaybolur | j'nin biti 1 (bildirim); i'nin j'ye çerçeveleri tam denemeli → göndericinin olayı | j SON ÇARE; maliyet hariç aralıkla korunur | olağan aday varsa zorunlu geçiş; yoksa j S'de kalır, kural 10a'nın isteği; ilan bayatlarsa aday dışı | ardıla (O ya da S) | maliyet %15 değişirse olay | komut izle; izin komşusu S olsa da gider |
| j kanal kilidinde | j susar; dönüşte geri alma sıfırları siler | bit gelmez; göndericinin olayı | j SON ÇARE (gönderici, veri yok) | zorunlu geçiş ya da S; ilan 3,5 · a'da bayat; j ardılsa 4a'nın isteği yanıtsız | ardıla, aday kaldıkça | — | iz j'yi gösterirse komut j'ye; j'den telemetri gelmez, iz 3 s'de bayatlar |
| j öldü ya da uzaklaştı | 30 s'de silinir | göndericinin olayı | SON ÇARE; silinince yok | ilan bayat, aday dışı; açlıksa açlık isteği | ardıla, aday kaldıkça | — | iz 3 s'de bayat, j silinince geçersiz; komut bekler |
| i girişimde | sıfırlar (gerçek kayıp) | girişim, bit 1, kendi aralıklarım | hariç aralık: maliyetler korunur; komşulara önceki oran | ilanların yaşı durur; istek gitmez | olağan; çerçeve ulaşır, onayı duyulmaz | olağan, bit 1 | olağan |
| i kanal kilidinde | sıfırlar | kanal kilidi | hariç aralık | yaş durur; istek gitmez | sorulmaz (geri çekilme bitmez) | selam kurulmaz; kilit bitince hemen | paketler kuyrukta bekler |
| açlık | — | — | — | C = ∞; açlık isteği (çoklu yayın) | B7'nin kararı | ∞ olayı, istek titreşimli | 1 s bekletir; açlık bitince hemen yeniden sorar |
| geçit | ölçer | aynı kurallar | geçide giden bağ bildirim ve gönderici sebebiyle S'ye düşmez | C = 0, tur istekle artar | yalnız komut | C = 0 | komut izi gelen telemetriden |

**Çelişki yok:** her bileşenin bir durumdaki kuralı, ötekilerin kuralının varsaydığı şeyle uyumlu. Denetlenen birleşimler:
- son çare: B3 (E1) → B4'ün sıralaması → B5'in gönderimi: olağan aday yoksa son çare kullanılır. B7'de komutun bilinen tek yolu iz olduğu için izin komşusu S'de olsa da kullanılır (B7 kural 8); E1 ile uyumlu;
- kendi karıştırılmam: B3'ün hariç aralığı, B4'ün ilan yaşı ve istek bastırması, B6'nın kilit kuralı ve B2'nin gönderici ayıklaması aynı kaynağa, B2'nin kendi durumuna ve aralıklarına dayanıyor;
- kilitte selam kurulmaması (B6) ↔ B1'in sırası tüketilen selam beklentisi (Ö-5) ↔ B1'in geri alması;
- kural 4a'nın isteği (B4) ↔ B6'nın tek alıcılı titreşimsiz gönderimi ↔ B4 kural 12'nin yanıtı ↔ B6'nın olay selamı;
- B7'nin yeniden sorması ↔ simülatörün her uyandırmada tamponu dökmesi (B6'nın selam uyandırması dâhil): yalnız daha sık yeniden sorma, zararsız.

**Ölçülen etkileşim: ilanın ömrü ↔ son çare** (`butunluk_hesap.txt` H1):
- Girişimdeki ardılın selamları uzak komşulara selam başına ~0,35 olasılıkla ulaşıyor (B2 kural 11, B2 teşhisi K6). İlanı bu yüzden bayatlayabilir; başka aday yoksa B4 açlığa girer ve E1'in "son çareyi yine kullan" kuralı o anda çalışmaz.
- Birincilde açık dönemde alıcısı girişimde olan kararların %1,9'unda ilan bayattı ve başka aday yoktu. Bu kararlarda bugünkü kodda atlamanın onayı yalnız %23 geldi (kanal kilidinde %1,7).
- Ardıla gönderilseydi kazanılacak payın üst sınırı açık doğana oranla 0,002 (kanal kilidinde 0,0001).
- **Değişiklik gerekmiyor:** bedel küçük. Açlıkta paket 1 s bekler; ardılın bir sonraki selamı ilanı tazeler. Kural eklemek (ör. bildirimli komşunun ilanının yaşını durdurmak) bu küçük kazanç için karmaşıklık getirirdi.

## 4 · Olay sırası: ortak kural

`18` §1.4'ün olay sırası, B1 kural 20 ve B5–B7'nin kâğıtlarıyla şöyle birleşir (her niyetli kancada):

1. **B1'in zaman olayları:** zaman aşımları ve silmeler, kendi anlarının sırasıyla (B1 kural 20). Öteki bileşenlerin süreleri ayrı bir adımda işlenmez; her biri kendi adımında, o anın saatiyle değerlendirilir: B3'ün kanıt ömrü ve B4'ün ilan ömrü, yok sayması ve istek dizisi 3. adımda (B4 kural 16'nın sırasıyla), B7'nin bekletme süresi ve kayıt temizliği kendi adımlarında.
2. **Gözlemin dağıtımı:** kancanın gözlemi sahibine gider; kontrol iletisini B6 çözer (B6 kural 3).
3. **B2 → B3 → B4:** kanıt, bağın durumu, yol.
4. **B7'nin cevabı, sonra B5:** paket varsa B7 yolun olup olmadığını ve komutun sonraki atlamasını söyler, B5 karar verir (B7 kural 10).
5. **B6:** değişim olaylarından doğan ve planlı kontrol iletileri; B4'ün tur istekleri; B6'nın uyandırmaları (B6 kural 13–14).
6. **B7:** yeniden sorma uyandırması (B7 kural 3).
7. **Beyanlar:** kopma, rota kuruldu; düşen paketin `rota_gecersiz`i kararla birlikte (B7 kural 4).

Niyet döndüremeyen kancalarda (`iletim_sonucu`, `cerceve_duyuldu`) yalnız 1. ve 2. adım yapılır; gerisi bir sonraki niyetli kancada.

`18` §1.4'teki eski sıradan farklar:
- 1 ile 2 yer değiştirdi: B1 bir gözlemi, o ana kadarki kendi zaman olaylarından sonra işler; böylece her gözlem B1'in o ana kadar güncel hâline uygulanır (B1 kural 20). Eski sıra öteki bileşenlerin süreleri için de ayrı bir adım öngörüyordu. Onlar zaten kendi kurallarının sırasıyla değerlendiriliyor (ör. B4 kural 16).
- 4'te B7'nin cevabı açıkça B5'ten önce.
- B2 kural 18'in "saniye sonu ile selam aynı anda" durumu iki ayrı kancanın (saniyelik zamanlayıcı ve `kontrol_alindi`) sırasıdır. Simülatör eşit anlı olayları eklenme sırasıyla işler (`sim2/cekirdek/olaylar.py`). Kayan noktalı anların tam eşitliği pratikte olmaz. Ortak kuralla çelişmez.

## 5 · Uçtan uca senaryolar (madde 4)

Sayılar örnektir; maliyetler ETX cinsinden (tamsayısı × 64). Kural numaraları kâğıtlarındır.

### S1 · Soğuk açılış ve sakin ağ

Geçit G; röle r, G'nin komşusu; düğüm i, r'nin komşusu.
1. **t = 0:** bütün tablolar boş, kimse kimseyi bilmez. Her düğüm ilk selamını titreşimle gönderir (B6 kural 4). G'ninki 0,03 s'de çıkar: tur 1 (`TUR_BASLANGIC`), maliyet 0.
2. **0,03–2,1 s:** r, G'yi ilk selamıyla kaydeder (B1 kural 1). Yeni komşu olayı r'nin aralığını 0,5 s'de tutar (B6 kural 7). İki yönlü ölçü her iki tarafta 4 örnek ister (`ORNEK_EN_AZ`, ~2 s); o zamana kadar bağ KULLANILMAZ'dır (B3 kural 1).
3. **~2,1 s:** r'de `E_selam`(r→G) = 1,1, M = ⌈70,4⌉ = 71 (B3 kural 2). G'nin ilanı (1 · 0) uygulanabilir (FD yok, B4 kural 1). r'nin ardılı G, C = 71; FD (1, 71). C ∞'dan sonluya döndüğü için olay: r selamı hemen gönderir (B4 kural 15, B6 kural 7).
4. **~2,6 s:** i, r'nin ilanını (1 · 71) alır. Bağ maliyeti 1,2 (M = 77); i'nin ardılı r, C = 148 (2,3 ETX).
5. **Telemetri:** i'nin 1,0 s'de doğan paketi için yol yok. B7 onu bekletir (kural 1); 2,0 s'de 1 s dolar ve paket düşer. Hedef hiç bilinmediği için sebep `hedef_yok` (B7 kural 4). Ölçüm penceresi 50 s'de başlar. 2,6 s'den sonra doğanlar r üzerinden gider.
6. **Geri iz:** r, i'nin kendisine gelen ilk telemetrisiyle `iz[i]` = i'yi öğrenir; G de o paketle `iz[i]` = r'yi (B7 kural 6). Geçitten i'ye 5,0 s'de giden komut G → r → i yolunu izler (B7 kural 8).
7. **Sakin ağ:** selam aralıkları 1, 2, 2… s (B6 kural 5), ilanın ömrü 3,5 × 2,2 = 7,7 s (aralık alanı 1,1 × 2 s, B6 kural 6). Ardılın iki selamı art arda kaybolursa ilanın yaşı 5,5 s'yi geçer; kural 4a'nın rota isteği gider ve ilanı tazeler.

### S2 · Karıştırma başlıyor ve bitiyor

**Girişim bölgesi:** i'nin ardılı j, olağan yedeği k (B4 §12'nin sayıları: `m_j` 2,3, `m_k` 2,7; j'nin bağı 1,1). j 152,1 s'den beri karıştırılıyor; zaman çizelgesi B2 §12 ve B3 §12'nin örneklerinden.
1. i'nin j'ye 152,1 · 152,9 · 153,6 s'deki çerçeveleri tam denemeyle biter. Üçüncüsünde göndericinin olayı oluşur (B2 kural 12), j SON ÇARE olur (B3 kural 6).
2. B4 olağan aday k'ye zorunlu geçer (kural 5). C 2,3'ten 2,7'ye çıkar (+%17, eşik %15): olay, selam hemen (B6 kural 7). 153,6'dan sonraki paketler k'ye gider (B5 kural 1).
3. j 153,4'te kendi girişimini bulur ve biti 1 olan selamını hemen gönderir (B2 kural 9, B6 kural 7). Bu selam i'ye ulaşmaz, sonraki 155,1'de gelir: bildirim sebebi doğar (B3 kural 5). Girişimdeki düğümün biti uzak komşuya selam başına ~0,35 olasılıkla ulaşır (B2 kural 11). j'nin bağının maliyeti hariç aralıkla 1,1'de kalır (B3 kural 9).
4. Göndericinin sebebi 158,6'da (153,6 + 5 s) kalkar; j'ye çerçeve gitmediği için kanıt uzamaz (B3 kural 6). Bildirim sürdüğü için j S'de kalır.
5. Karıştırma 165,0'da biter. j 165,4'te bitini 0 yapar ve selamını hemen gönderir; i onu 165,9'da alır, j OLAĞAN olur.
6. `m_j` 2,3 < `m_k` 2,7 ve düzgünleştirilmiş maliyet de küçük: isteğe bağlı geçişle ardıl j'ye döner (B4 kural 5–6). C 2,7'den 2,3'e döner. Yeni maliyet, değişim eşiği aşıyorsa olay selamıyla, aşmıyorsa bir sonraki planlı selamla (en geç ~2,2 s) gider (B6 kural 7).
7. Kayıp yalnız 152,1–153,6 arasındaki tam denemeli çerçevelerden vazgeçilenlerdir.

**Kanal kilidi:** j 180,0–190,0 arasında karıştırıcıya çok yakın (B3 §12 madde 5'in sayıları); son selamı 179,5'te, aralığı 2,2 s.
1. j selam gönderemez. i'nin çerçeveleri vazgeçmeyle biter; üçüncüsünde (181,8) göndericinin olayı doğar, j S'ye düşer, B4 k'ye geçer.
2. 186,8'de (181,8 + 5) kanıt kalkar, j OLAĞAN'a döner ve B4 j'yi yeniden seçer. İlanının yaşı 7,3 s; rota isteğinin eşiği 5,5 s'yi geçmiş (B4 kural 4a): j'ye istek gider, kilitteki j yanıtlayamaz. 187,0'daki çerçeve de vazgeçmeyle biter. Sebep hemen geri gelir (B3 kural 6), ardıl yine k.
3. j'nin ilanı 187,2'de (179,5 + 7,7) bayatlar (B4 kural 4); j artık aday değildir.
4. j 190,0'da kilitten çıkar. B6 kilit bitince selamı hemen gönderir (kural 11). i'de geri alma, zaman aşımının sıfırlarını siler (B1 kural 4); ilan tazelenir.
5. 192,0'da (187,0 + 5) kanıt yine kalkar. j'nin ilanı taze, maliyeti geri almayla eski değerinde: B4 j'ye döner ve 192,2'deki çerçeve onay alır (B3 §12 madde 5).

**Son çare ardıl, olağan aday yok:** k de yokken j S'de kalır ve paketler j'ye gider (B5 kural 1). B4 kural 10a, yalnız uygulanabilirlik yüzünden aday olmayan temiz bir komşuya tur isteği gönderir. Yeni tur gelince o komşu olağan aday ve ardıl olur (B4 §12 madde 8).

### S3 · Düğüm kopuyor ve dönüyor

1. Ardıl j 100,0 s'de düşer. i'nin j'ye çerçeveleri vazgeçmeyle biter: üçüncüsünde göndericinin olayı (katman; B3 kural 6), j SON ÇARE olur. Olağan aday varsa B4 ona geçer. Yoksa j'ye gönderim sürer ve dördüncü vazgeçmede "veri yok" da doğar (çekirdek; B3 kural 7). Katman kapalıyken bağı yalnız bu sebep bırakır.
2. j'nin selamları gelmez. j ardıl kaldıysa kural 4a'nın isteği yanıtsız kalır; ilan 3,5 · a sonra bayatlar ve j aday olmaktan çıkar (B4 kural 4). B4 başka adaya geçer ya da açlığa girer: C = ∞; uygulanamaz ama sonlu bir ilan varsa açlık isteği gider (kural 11). Paketler en çok 1 s bekler (B7).
3. B1 j'yi 130,0'da (son duyulmadan 30 s sonra) siler. B2, B3 ve B4 j'nin kayıtlarını budar; j'yi gösteren izler geçersizdir (B7 kural 7).
4. j 140,0'da geri gelirse (kurgusal; simülatörde düğüm yeniden başlamaz) ilk selamıyla yeniden kaydedilir. ~2 s sonra iki yönü ölçülür ve ilanı uygulanabilirse yeniden adaydır.

### S4 · Döngü oluşur mu

1. i'nin FD'si (7, 2,0). Komşu l'nin ilanı (7, 2,3) uygulanamaz: l'nin yolu i'den geçiyor olabilir. B4 l'yi aday yapmaz (kural 1, 3).
2. i'nin ardılı ölür, i'nin hiç adayı kalmaz. i ∞ ilan eder; ardılı i olan l de yolunu kaybeder ve ∞ ilan eder. Kimse daha kötü bir ilanı kabul etmediği için sayı sayarak sonsuza gitme olmaz.
3. Uygulanamaz ama sonlu bir ilan duyan açlıktaki düğümler tur ister (kural 11). Geçit turunu 8 yapar; tur 8'li ilanlar uygulanabilirliği yeniden açar ve döngüsüz yeni bir ağaç kurulur (B4 §15).
4. B5 paketi yalnız ardıla gönderdiği ve her aday uygulanabilir olduğu için veri yolunda da döngü yoktur. B4'ün döngü tanısı 0 olmalıdır (kural 17; sınaması B4 §13 madde 12).
5. Komut izden ize ilerlerken izin dayandığı paket sırası azalmaz. Komut ancak aynı telemetri paketinin yolunda bir döngüyle döngüye girebilirdi; o yol uygulanabilirlik koşuluyla döngüsüzdür (B7 kural 6, B4 §15).

### S5 · Geçide yakın karıştırma

1. **Geçit girişimde:** G'nin biti 1 olur. Komşuları G'ye giden bağı bildirim ve gönderici sebebiyle S'ye düşürmez (B3 kural 8: hedeften kaçınılamaz). Çerçevelerin bir kısmı yine geçer (girişimdeki alıcıya çerçeve başına 3,9 deneme; `18` §2.3). "Veri yok" (son 4 vazgeçme) geçitte de geçerlidir: başka bir komşu geçide daha iyi ulaşıyorsa ona geçilir.
2. Bu kayıp B5 teşhisinde J5'tir (alıcı geçit ve karıştırılıyor): açık doğanların 0,006'sı. Hiçbir aile ona ulaşamaz.
3. G gönderebildiği için komutlar çıkar (B7); alıcıları karıştırılmıyorsa ulaşır.
4. **Geçit kanal kilidinde:** G ne gönderebilir ne duyabilir. Hiçbir yönlendirme bunu kurtaramaz (kapsam sınırı, `18` §1.2 D). Kilit bitince G selamını hemen gönderir, ağ toparlanır.

### S6 · Komutun yolu

Geçit G'den düğüm 12'ye: G – a – b – 12.
1. **İzler:** 12'nin son telemetrisi b'ye 12'den, a'ya b'den, G'ye a'dan geldi: G'de `iz[12]` = a, a'da b, b'de 12 (B7 kural 6).
2. G 216,0 s'de komut q'yu gönderir. İz taze ve a OLAĞAN (B7 kural 8): q a'ya, sonra b'ye, sonra 12'ye gider (B5 kural 3).
3. **12 girişimde:** 12 gönderebildiği için telemetrisi b'ye ulaşmayı sürdürür; b'nin izi 12'yi gösterir. 12'nin bağı b'de S'dir; komut yine 12'ye gönderilir ve bir kısmı ulaşır (B7 kural 8).
4. **İz bayat:** 12'nin yolu c'ye kaydı; a'nın izi 3 s'den eski. a'ya gelen komut bekler (B7 kural 1). 1 s içinde 12'nin telemetrisi a'dan geçmezse düşer, sebep `rota_gecersiz` (B7 kural 4).
5. G'nin izi 12'nin bir sonraki telemetrisiyle yeni yoldaki komşusunu gösterir; sonraki komutlar yeni yoldan gider.

## 6 · İzlenebilirlik (madde 5)

Hedefler `18` §1.1'den. "Sınama" kâğıtların §13'ündeki birim testleri; "ölçüm" Aşama 4'ün büyük ölçümü (tam sürüm ↔ Babel ve kâhin; ablasyon kolları).

| hedef | bileşen ve kural | sınama | ölçüm |
|---|---|---|---|
| birincilde `PDR_açık` Babel + 0,05 | B2 1–13 (kanıt) · B3 5–9 (son çare, hariç aralık) · B4 3, 5 (O önce S), 10a · B5 1 · B7 1–3 | B2 §13 · B3 §13 · B4 §13 · B5 §13 · B7 §13 | birincil hücre, 8 tohum |
| fark-içinde-fark (birincildeki fark > ikizdeki fark) | karıştırma katmanı (aşağıda) | — | ikiz ve birincil |
| mekanizma kapısı (katman kapalıyken birincilde ≥ 0,02 düşüş) | `karistirma_katmani`: B2'nin tamamı · B3 5–6, 8–10 · B4 4'ün yaşı, 14 · B6 11 | bayrak sınamaları (her kâğıdın §13'ü) | birincil, katman kapalı kol (§10) |
| ikizde zarar yok | B2'nin yanlış alarmı (doğrulamada düğüm-saniyelerin %0,002–0,007'si) · B3 eşiksiz maliyet · B4 4a (yanlış bayatlık) · B6 olay kümesi | B2 §13 · B3 §13 · B4 §13 · B6 §13 | ikiz; katman açık ↔ kapalı |
| dayanıklılık hücresi | zaman sabitleri çizelgeye bağlı değil (İlke 3): B2 `G_CIKIS` 1 s · B3 `KANIT_OMUR_S` 5 s · B4 ilanın ömrü | — | dayanıklılık hücresi (10 s açık · 20 s sessiz) |
| en kötü tohum ≥ 0,465 | B4 uygulanabilirlik koşulu (döngüsüz) · B3 eşiksiz maliyet (açlığın kökü kalktı) | B4 §13 madde 12 | birincil, tohum başına |
| sessiz dönem | B3 kural 9 (hariç aralık) · B6 bit değişiminde hemen selam · B4 kural 5–6 (dönüş) | B3 §13 · B6 §13 | sessiz dönem teslimi |
| gecikme p99 ≤ Babel | B7 `TUTMA_EN_COK_S` 1 s · B6 olay selamı 0,5 s | B7 §13 | p99, bekletilen payı |
| kontrol payı < Babel, %10 sınırı | B6 (Z1) · B4'ün istekleri | B6 §13 | kontrol payı, iletiler ve onaylar ayrı |
| yer karıştırıcılı aile | B2'nin kapsamı (cephe hattında girişim kuralı zayıf, B2 §15) | — | yer karıştırıcılı aile |

## 7 · İlkeler ve sözleşmeler (madde 6)

**İlkeler** (`17` §0):

| ilke | karşılayan kurallar |
|---|---|
| İlke 1 · kısa bağ dayanıklı ama tek ölçüt değil: maliyet ölçülen teslimden | B1 kural 11–13 (iki yönlü oran, ETX) · B3 kural 1–3 (maliyet selamdan, eşiksiz) · B4 kural 2 (yol maliyeti toplam). Kısa bağı zorlayan ayrı kural yok |
| İlke 2 · ölçmeyi bırakmamak, kendini onaran ağ | B1 kural 10 (ölçü donmaz, hariç aralık okumanın parametresi) · B1 selamla kullanılmayan bağları da ölçer · B3 kural 6–7 (`KANIT_OMUR_S` sonra yeniden deneme) · B3 kural 9 (`HARIC_UST_S`) · B4 kural 11 (açlıkta tur isteği) |
| İlke 3 · kanıta göre, çizelgeye göre değil | B2'nin durumu işaretlerden (çizelge yok) · B3'ün sebepleri kanıt kalkınca kalkar · B4 kural 4 ve 4a (yaşla, çizelgesiz) · hiçbir değer 15/15 çizelgesine göre seçilmedi (`00-DIZIN`) |

**Sözleşmeler** (`18` §1.4):

| sözleşme | karşılığı |
|---|---|
| 1 · tek yönlü akış | her kâğıdın §9'u yalnız aşağıdakileri okur. Tek istisna yazılı: B7'nin B5'e cevabı B5'ten önce hesaplanır (B7 kural 10; §11'de iskelete işlendi) |
| 2 · gözlemler sahibine | kanca tablosu (§11'de düzeltildi); kontrol iletisini B6 çözer; B4'ün döngü tanısının girdisi B4 §2'ye yazıldı (§11) |
| 3 · tek kaynak | bağın maliyeti B3'te, kendi maliyetim B4'te, kanıt B2'de, oran B1'de; değerler `00-DIZIN`'de (§1) |
| 4 · kanıtı silmeme | her kâğıdın §11'i. Örnek: B3'te gönderilmeyen bağın kanıtı süreyle kalkar ve bağ yeniden denenir; B6'da kilitte selam kurulmaması alıcının geri almasıyla iz bırakmaz |
| 5 · rota durumu ile paket kararı ayrı | B5 A: paket ardıla, sapma yok; B4'ün aday listesi döngüsüz. Bu, yapı kararı 3'ün seçilmeyeni (tek ardıl, B4 ile B5 bir arada) değildir: B5 ayrı ve durumsuzdur, komutun yolu (B7'nin izi) B4'ün ardılından ayrıdır. İskelete not düşüldü (§11) |
| 6 · kontrol iletileri tek yerde | B6 kural 1–2; öteki bileşenler değer ve olay verir |
| 7 · ablasyon | `00-DIZIN` bayrak tablosu; her kâğıdın §10'u |
| 8 · bellek sınırı | her kâğıdın §3'ü (B5 durum tutmaz); B4'ün döngü tanısının kaydı kaynak başına bir (§11) |

## 8 · Ortak sözlük

| terim | anlamı | sahibi |
|---|---|---|
| ardıl | paketin bu an gittiği komşu | B4 |
| aday | kayıtlı, bağı kullanılır, ilanı taze, sonlu ve uygulanabilir komşu | B4 kural 3 |
| O ve S sınıfı | adayın B3 durumu OLAĞAN ya da SON ÇARE | B4 kural 3 |
| OLAĞAN · SON ÇARE · KULLANILMAZ | bağın durumu | B3 kural 4 |
| E1 | karıştırılan bağın son çare olması: olağan aday yoksa yine kullanılır | `18` §2.3; B3 §1 |
| açlık | hiç aday yok; C = ∞ | B4 kural 11 |
| tur | geçidin sıra numarası; yalnız istekle artar | B4 kural 13 |
| FD (uygulanabilirlik uzaklığı) | ilan ettiğim en iyi (tur, maliyet); uygulanabilirliğin ölçütü | B4 kural 1, 9 |
| ilan | selamdaki (tur, maliyet) | B4 kural 8, B6 kural 1 |
| ilanın ömrü | ilanın geçerli sayıldığı yaş, 3,5 · a | B4 kural 4 |
| kendi durumum | yok · girişim · kanal kilidi | B2 kural 7 |
| kendi aralıklarım | durumumun "yok" olmadığı dönemler, geriye dönük | B2 kural 8 |
| bildirim, bildirim aralığı | komşunun selamındaki bit ve 1 olduğu dönem | B2 kural 10 |
| göndericinin olayı | bir komşuya art arda 3 tam denemeli çerçeve | B2 kural 12 |
| hariç aralık | ölçüde sayılmayan dönemler (kendi aralıklarım, öne çekilmiş bildirim aralıkları) | B3 kural 9 |
| ara ilan, olay selamı | değişim olayıyla öne çekilen selam | B6 kural 7–8 |
| rota isteği | kural 4a'nın tur isteği: kalan atlama 1, tur artırmaz | B4 kural 4a |
| bekletme | yol yokken paketi tamponda tutmak, atlama başına en çok 1 s | B7 kural 1–2 |
| geri iz | bir düğümün telemetrisini getiren komşunun kaydı | B7 kural 6 |

"Son çare" yalnız B3'ün durumudur; B4 adaylarını O ve S diye anar.

## 9 · Açık kalanların kapanışı (`00-DIZIN`'in listesi)

| madde | sonuç |
|---|---|
| olay sırası | kapandı: ortak kural §4; `18` §1.4 düzeltildi |
| bileşenler arası beklentiler | kapandı: B1–B4'ün B6'dan beklentileri B6 §6'da. B2'nin B3'e bıraktıkları (B2 §11 madde 2) denetlendi: bağın durumu (B3 kural 5–6), olayın süresi ve geri dönüş (kural 6, `KANIT_OMUR_S`), sonradan geçersizleşen olay (B3 her kancada B2'nin geçerli olayını okur), hariç aralığın payı ve üst süresi (kural 9), geçidin biti (kural 8), gönderilmeyen bağın kanıtı (§11 madde 7) |
| iskeletin kanca tablosu | kapandı: `18` §1.4 düzeltildi (§11) |
| B1'in sondaki sessizliği (kural 16) | kapandı: kaldırıldı (§11) |
| B3'ün B4'ten beklentileri | kapandı: B4 kural 3 ve 5 (olağan önce, histerezis) |
| ortak sözlük | kapandı: §8 |
| B4'ün B6'dan beklentileri | kapandı (B6) |
| iki meşgul payı eşiği (`ED_ESIK` 0,55, `CBAR_ED_ESIK` 0,62) | Aşama 4'e: birleştirmek ölçülen kuralı değiştirir |
| iskeletin B5 satırı | kapandı: `18` §1.4 düzeltildi |
| B5'in B7'den beklentileri | kapandı (B7) |
| B5 ile B7'nin sırası | kapandı: `18` §1.4'ün sözleşme 1'i ve olay sırası |
| mekanizma kapısının payı | kestirildi (§10); Aşama 4'ün beklentisine |

`00-DIZIN`'in listesi buna göre "kapanış" ve "Aşama 4'e kalanlar" diye yeniden yazıldı.

## 10 · Mekanizma kapısının beklenen payı

Kapı, karıştırma katmanı kapatılınca birincilde `PDR_açık`'ın en az 0,02 düşmesini ister (geliştirmede 8 tohumun 6'sında; `18` §1.1). Kapının kolunda genel mekanizmalar açık kalır. Katmanın yalnız kendine ait payı bu yüzden önemlidir:

| katmanın mekanizması | kendine ait payın kanıtı |
|---|---|
| B2'nin bildirimi ve göndericinin olayı (B3'te son çare) | J1'in yalnız katman kanıtlı kısmı en çok 0,016 (B5 teşhisi E7). Kalanını çekirdeğin "veri yok" ve ilanın ömrü kuralları da görüyor |
| B4 kural 10a'nın katman kanıtıyla tetiklenen istekleri | en çok 0,014 (B5 teşhisi E8) |
| B4 kural 4: kendi girişimimde ilanların yaşının durması | ölçülmedi. Açık dönemde G alanında ortalama ~6,8 düğüm var (B2 §6, `18` §2.2). Katman kapalıyken bu düğümler ardıllarının selamlarını duyamaz (girişim alanında selamların ~%73'ü kaybolur, B4 kural 4'ün gerekçesi). İlanlar bayatlar, açlık doğar; katman bunu önler |
| B6 kural 11: kilitte selam kurulmaması | ölçülmedi; küçük olmalı |
| B3 kural 9: hariç aralık | çoğu sessiz dönemin toparlanmasına gider, `PDR_açık`'a az girer |

**Sonuç:** ölçülmüş üst sınırların toplamı ~0,03. Gerçekleşecek pay bunun altında kalır, ama ölçülmemiş B4 kural 4 payı ekler. Kapı geçebilir, ama geçeceği güvence değil. Aşama 4'ün beklentisinde bu açıkça yazılmalı: kapı geçmezse hüküm "fark var, karıştırmaya özgü mekanizmaya bağlanamadı" olur (`06` §0.4.5).

## 11 · Yapılan düzeltmeler (28 Kasım)

Kuralların hiçbiri değişmedi. Düzeltilenler, onaylı kararlarla çelişen ya da sonradan bayatlayan metinler:

1. **`18` §1.4, iskelet** (onaylı kâğıtlara göre):
   - tablonun B2–B7 satırları: B2'nin işaretleri (MAC vazgeçmesi B1'in kaydından); B3'ün durumu (hatırlanan kalitenin yerini hariç aralık aldı); B4'ün durumu (FD, tur, O ve S sınıfları, istek kayıtları; döngü kaydı yok, yalnız tanı); B5 durum tutmaz, karıştırma eki yok; B6'nın planları; B7'nin cevabı B5'ten önce;
   - sözleşme 1: B7'nin istisnası;
   - sözleşme 2: MAC sonucu B1'e, B2 onu B1'in kaydından okur; kontrol iletisini B6 çözer; paketin başlığı B4'ün döngü tanısına (yalnız ölçüm); paketi getiren komşu B7'ye;
   - sözleşme 7: katmanın üyeleri (B2'nin tamamı, B3'ün eki, B4'ün kendi karıştırılmam kuralları, B6'nın kilit kuralı; B5'in eki yok);
   - olay sırası (§4) ve kanca tablosu;
   - "katman kapalıyken çekirdek" satırı;
   - tarihli not: yapı kararı 3'ün ayrımı korunur, B5'in A'sı onun içinde bir seçimdir.
2. **B1 kural 16 kaldırıldı** (sondaki sessizlik): kural 16, §9'un çıktı tablosu, §11 madde 4, §12 madde 4, §13 madde 9. Anışlar B2 §2, B2 §11 madde 1, B3 §2 ve B3 §11 madde 1'de "kaldırıldı" diye işaretlendi. Numaralar korunur.
3. **B5'in kararından önce yazılmış dokuz anış:**
   - B2 §8 (geçit: karşılığı yalnız B3'te);
   - B2 §9 (kendi durumumu B4 ve B6 okur, aralıklarımı B3 ve B4);
   - B2 §10 (katman kapanınca kapananlar);
   - B2 §11 madde 3 ve 7 (B5'in eki yok; B2'ye dayanan kararlar B3, B4, B6);
   - B3 §9 (bağın durumunu B4 ve B7 okur);
   - B3 §11 madde 4 (telemetri S'ye ancak olağan aday yokken, komut izle);
   - B3 §11 madde 6. "Son çarede bekletme" diyordu; doğrusu ardıl S'deyken paketin gitmesi, bekletmenin yalnız açlıkta olması (B5 kural 1);
   - B4 §1 (kazancın beklendiği bileşenler: B2 ile B3'ün eki).
4. **B4'ün döngü tanısı** (kural 17): tanı paketin kaynağını, sırasını ve atlama sayısını okur. B4 §2 başlığı okunmayanlar arasında sayıyordu, §3'te kaydı yoktu (sözleşme 8). Kural 17'ye nasıl sayıldığı yazıldı: kaynak başına en yeni paket tutulur, sayı bir alt sınırdır. §2–3 ve `00-DIZIN`'in gözlem tablosu da buna göre düzeltildi.
5. **Olay sırasına ve Aşama 3'e giden anışlar:** B1 kural 20 ve §9, B2 §9, B5 §3, §6 ve §11 madde 3, B6 kural 3, B7 kural 10.
6. **`00-DIZIN`:** açık kalanlar "kapanış" ve "Aşama 4'e kalanlar" diye yeniden yazıldı; kâğıtlar tablosunun altına bu belge eklendi.

## 12 · Bağımsız denetime kalanlar

- Bu denetimi kâğıtları yazan yaptı. Bağımsız denetim (Aşama 3 madde 2) ayrı bir oturumda, yeni bir istemle yapılır (eski istemler `arsiv/denetim/`de).
- Bakılması istenecek riskler:
  - mekanizma kapısının ince payı (§10);
  - kontrol payının kestirimindeki varsayımlar (§2);
  - kâğıtların kural sayısı ve birlikte kodlanabilirliği;
  - B2'nin eşiklerinin B4–B6'nın değiştirdiği trafikte geçerliliği (B2 §11 madde 8).
