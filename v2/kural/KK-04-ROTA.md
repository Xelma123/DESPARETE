# KK-04 · Rota seçimi, döngüsüzlük, açlık

> Kararlar: T-11 · T-12 · T-13 · T-14 · T-15 (`17`). Değerler ve genel kurallar `KK-00`. Kod `protokoller/desparete5_rota.py`. Güncel: 18 Kasım 2026 (kodlamayla Y-8 · Y-11; iletimin, yinelemenin ve yok saymadaki isteğin ayrıntısı yazıldı). Önceki: 17 Kasım (bağımsız denetimden sonra: B-1 · B-8 · B-9 · B-10 · B-16 · B-17 · B-18).

## Amaç ve sınıf

Geçide giden ardılı seçmek, döngüyü önlemek, uygun komşu kalmayınca yeni tur istemek. **Genel** (`istege_bagli_esik`; öteki kurallar çekirdek).

## Gördüğü ve tuttuğu

- Her komşunun son alınan ilanı (`tur_j`, `C_j`); seçili ardıl için ayrıca son **kabul edilen** ilanı.
- KK-01'den her bağın ETX'i ve durumu.
- `FD = (tur, maliyet)`: bu turda **ilan ettiğim** (nicemlenmiş) sonlu maliyetlerin en küçüğü (T-12).
- `ardil`, kendi maliyetim `C`, son ilan ettiğim maliyet.
- Yok sayma sayacı (kural 7); son iletilen istekler: (istenen tur, isteyen, an), `ISTEK_ANIMSA` süreyle (kural 9).
- Geçit kendi turunu tutar; geçidin kimliği yapılandırmadan gelir. Bütün maliyetler ETX × 64 tamsayı biriminde; tur 16 bit, modüler karşılaştırılır.

## Kurallar

1. **Uygulanabilirlik** (her seçimde güncel FD ile hesaplanır, saklanmaz; RFC 8966 §3.5.3, §3.6):
   - ∞ ilan (geri çekme) her zaman uygulanabilirdir (RFC 8966 §3.5.1);
   - sonlu ilan uygulanabilir ⇔ `tur_j > FD.tur` ya da (`tur_j = FD.tur` ve `C_j < FD.maliyet`);
   - FD'si olmayan düğüm her ilanı uygulanabilir sayar.
2. **Aday küme** `A`: durumu OLAĞAN (KK-01) ve ilanı **sonlu ve uygulanabilir** komşular. ASKIDA, KÖTÜ ve KARIŞTIRILIYOR komşu aday da yedek de değildir (T-15).
3. **Maliyet:** kendi maliyetim seçili rotamınkidir: `C = ETX(i, ardil) + C_ardil` (ardıl için son kabul edilen ilan; yukarı yuvarlanır, 0xFFFE'de doyar); geçit için `C = 0`; ardıl yoksa `C = ∞`. Adayların maliyeti `ETX(i, j) + C_j`, ardılı seçmek için karşılaştırılır (kural 4–5). Eşit maliyette sıra: mevcut ardıl, düşük ETX, küçük adres. İlan edilen maliyetle paketin gittiği yol aynı olmalıdır (RFC 8966 §3.7).
4. **Zorunlu geçiş:** ardıl `A`'dan çıkarsa (ASKIDA, KÖTÜ, KARIŞTIRILIYOR, silindi, ∞ ilan, kural 7'nin süresi dolmuş uygulanamaz ilan) `A`'nın en ucuzuna anında geçilir; `A` boşsa `C = ∞` ilan edilir ve kural 8 uygulanır. Onarım yok (T-9, T-14).
5. **İsteğe bağlı geçiş** (`istege_bagli_esik`): aday maliyeti `< (1 − GECIS_ORANI) · C` ise geçilir; değilse ardıl korunur (T-11). Bayrak kapalıyken her hesapta en ucuz aday seçilir.
6. **İlan ve FD:** maliyet selamla ilan edilir (KK-02). İlanın turu **seçili rotamın turudur**: ardılımın ilan ettiği tur; geçitte kendi turu. Rotası olmayan düğüm ∞ ilan eder ve daha yeni bir tur ilan etmez (RFC 8966 §3.7); ∞ ilanın tur alanı FD'nin turudur, FD yoksa 0 (uygulanabilirliğe etkisi yok, ∞ her zaman uygulanabilir; Y-8). Sonlu bir maliyet ilan edilirken: `tur` FD'ninkinden yeniyse `FD ← (tur, C)`; aynı turda `C < FD.maliyet` ise `FD.maliyet ← C`.
7. **Seçili ardıldan uygulanamaz ilan:**
   - **∞ ilan** yok sayılmaz: ardıl hemen bırakılır (kural 4).
   - **Sonlu ve uygulanamaz ilan** yok sayılır: ardıl son kabul edilen `C_j` ile kalır; ilk yok saymada ardıla tek alıcılı tur isteği gider, istenen `FD.tur + 1` (RFC 8966 §3.5.3, §3.8.2.2); sonraki yok saymalar istek göndermez.
   - Yok sayma ilk yok sayılan ilandan başlayarak en çok `ISTEK_ARA` sürer; sonraki yok saymalar süreyi yenilemez; süre bir `Uyandirma` ile denetlenir.
   - Bu sürede ardıldan uygulanabilir bir ilan gelirse yok sayma biter, o ilan kabul edilir.
   - Süre dolunca ardılın son alınan ilanı uygulanır; uygulanamıyorsa ardıl bırakılır (kural 4).
8. **Açlık** (`A` boş):
   - Tur isteği yalnız en az bir **OLAĞAN** komşunun **sonlu ama uygulanamaz** ilanı varsa gider: `istenen = FD.tur + 1`, komşulara çoklu yayın, hemen ve ardından `ISTEK_YINELEME` kez daha 0,5 s arayla (Babel'in "en çok üç kez yeniden gönderilir"i, RFC 8966 Ek B); açlık sürerse dizi `ISTEK_ARA`'da bir yinelenir. Açlık biter ya da koşul kalkarsa dizi durur.
   - Öteki bütün durumlarda istek gitmez, paketler bekletilir (KK-05): sonlu ilanlı komşu yok (adaysız); uygulanamaz ilanlı komşuların hepsi ASKIDA, KÖTÜ ya da KARIŞTIRILIYOR (yeni tur onları aday yapmaz); kendim karıştırılıyorum (KK-03 kural 4; sorun benim alıcımda, yanıtları duyamam, gereksiz tur artışı bütün ağı çalkalar).
   - Kendi karıştırılmamdan çıkınca açlık sürüyorsa istek hemen gider.
9. **Tur isteği gelince** (isteyen g, istenen t):
   - seçili rotamın turu ≥ t ve `C` sonlu → hemen selam (ara ilan, KK-02); yalnız duyduğum ama rotamın dayanmadığı bir tur yanıt sayılmaz;
   - geçitsem ve turum < t → tur bir artar, hemen selam;
   - değilsem, ardılım var, ardılım g değil ve kalan atlama en az 2 ise → istek ardılıma kalan atlama bir eksiltilerek tek alıcılı iletilir (RFC 8966 §3.8.1.2); t'nin kaydı `ISTEK_ANIMSA` süre tutulur; aynı t için 1 s içinde ikinci istek iletilmez ama kayıt tazelenir (Y-11). Yanıt çok-yayın selam olduğu için kayıt isteyeni tutmaz;
   - ardılım yoksa ya da g ise istek iletilmez. Bu, bu tasarımın basitleştirmesidir: RFC 8966 §3.8.1.2 böyle bir isteği başka bir uygulanabilir rotanın ardılına iletmeyi ister.
   - Tutulan bir istek varken seçili rotamın turu ≥ t olursa hemen selam gönderilir (isteği karşılayan değişim, KK-02 kural 3) ve kayıt silinir. Yanıt böylece istek yolundan geri yayılır.
10. **Tur yalnız istekle artar** (T-13); geçidin turu 1'den başlar.
11. **İleti:** `tur_istegi` = istenen tur 16 bit · kalan atlama 8 bit (başlangıç `ISTEK_ATLAMA`) (`13` §02.1).

## Örnek

i'nin FD'si (tur 7, 2,0). Ardıl k'nin bağı karıştırılıyor; adaylar j (ilanı tur 7, 1,8 → uygulanabilir) ve m (tur 7, 2,5 → uygulanamaz). i anında j'ye geçer: `C = ETX(i, j) + 1,8`. Yalnız m kalsaydı ve m OLAĞAN olsaydı açlık olurdu: i, tur 8'i ister; istek ardıl zinciriyle geçide gider, geçit turu 8 yapar ve hemen ilan eder; istek yolundaki düğümler yeni turu benimseyince hemen ilan eder; yeni turda m'nin ilanı uygulanabilir olur. Bir zincirde X rotasını kaybedip ∞ ilan ederse, X'i ardıl kullanan Y bunu yok saymaz, hemen yedeğine geçer ya da ∞ ilan eder; kayıp beklemeden yayılır.

## Sınanması

- `istege_bagli_esik` açık ↔ kapalı: ikizde pencere PDR'si, ardıl değişim sıklığı, iletim kaybı.
- Tanı: döngünün göstergesi TTL kaybı (T grubu); tur artışı ve tur isteği sayısı (`17` §7 madde 10); en uzun atlama sayısı (`ISTEK_ATLAMA` ile karşılaştırma).

## Kaynak

Uygulanabilirlik, geri çekmenin her zaman uygulanabilir olması, FD, tur isteği ve yanıtı Babel [4] (RFC 8966 §3.5.1, §3.5.3, §3.6, §3.7, §3.7.3, §3.8.1.2, §3.8.2.1–§3.8.2.2); DSDV ailesi (De Couto 2003'te [36] aktarıldığı gibi); hazır yedek DUAL [65] ve RPL [63]; oransal geçiş Ramachandran [54].
