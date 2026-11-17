# KK-04 · Rota seçimi, döngüsüzlük, açlık

> Kararlar: T-11 · T-12 · T-13 · T-14 · T-15 (`17`). Değerler `KK-00`. Güncel: 17 Kasım 2026.

## Amaç ve sınıf

Geçide giden ardılı seçmek, döngüyü önlemek, uygun komşu kalmayınca hemen yeni tur istemek. **Genel** (bayrak `istege_bagli_esik`).

## Gördüğü ve tuttuğu

- Komşu selamlarından her komşunun son kabul edilen ilanı: (`tur_j`, `C_j`) ve uygulanabilir mi.
- KK-01'den her bağın ETX'i ve durumu.
- `FD = (tur, maliyet)`: bu turda **ilan ettiğim** sonlu maliyetlerin en küçüğü (T-12).
- `ardil`, kendi maliyetim `C`, son ilan ettiğim maliyet.
- Geçit, kendi turunu tutar; geçidin kimliği yapılandırmadan gelir.

## Kurallar

1. **Uygulanabilirlik:** j'nin ilanı uygulanabilir ⇔ `tur_j > FD.tur` ya da (`tur_j = FD.tur` ve `C_j < FD.maliyet`). FD'si olmayan düğüm her ilanı uygulanabilir sayar.
2. **Aday küme** `A`: durumu OLAĞAN (KK-01) ve ilanı uygulanabilir komşular. KARIŞTIRILIYOR komşu aday da yedek de değildir (T-15).
3. **Maliyet:** kendi maliyetim seçili rotamınkidir: `C = ETX(i, ardil) + C_ardil`; geçit için `C = 0`; ardıl yoksa `C = ∞`. Adayların maliyeti `ETX(i, j) + C_j`, ardılı seçmek için karşılaştırılır (kural 4–5). İlan edilen maliyetle paketin gittiği yol aynı olmalı: ucuz bir adayın maliyetini ilan edip pahalı ardıla göndermek, komşuların uygulanabilirlik hesabını yanlış bir sayıya dayandırırdı (Babel de seçili rotanın metriğini ilan eder, RFC 8966 §3.7).
4. **Zorunlu geçiş:** ardıl `A`'dan çıkarsa (KÖTÜ, KARIŞTIRILIYOR, silindi, uygulanamaz) `A`'nın en ucuzuna anında geçilir; onarım yok (T-9, T-14).
5. **İsteğe bağlı geçiş:** aday maliyeti `< (1 − GECIS_ORANI) · C` ise geçilir; değilse ardıl korunur (T-11).
6. **İlan ve FD:** maliyet selamla ilan edilir (KK-02). İlanın turu **seçili rotamın turudur**: ardılımın ilan ettiği tur; geçitte kendi turu. Rotası olmayan düğüm ∞ ilan eder ve daha yeni bir tur ilan etmez. Sebep: bir düğüm duyduğu ama rotasının dayanmadığı yeni bir turu ilan etseydi, komşuları onun eski bir yoldan gelen maliyetini yeni turla uygulanabilir sanır ve döngü kurulabilirdi (Babel'de sıra numarası seçili rotanınkidir, RFC 8966 §3.7). Sonlu bir maliyet ilan edilirken: `tur` FD'ninkinden yeniyse `FD ← (tur, C)`; aynı turda `C < FD.maliyet` ise `FD.maliyet ← C`.
7. **Seçili ardıldan uygulanamaz ilan:** ilan yok sayılır, ardıl son kabul edilen `C_j` ile kalır, ardıla tek alıcılı tur isteği gider. Yok sayma en çok `ISTEK_ARA` (5 s) sürer: o sürede yeni tur gelmezse ilan uygulanır ve ardıl bırakılır (yedeğe geçilir ya da açlık, kural 8). Böylece bayat ve gerçekten iyi olmayan bir maliyet süresiz ilan edilmez. İlan uygulanırsa ardıl hemen bırakılır; uygulanamaz bir rota seçili tutulmaz (RFC 8966 §3.5.3, §3.8.2.2).
8. **Açlık:** `A` boş ama tabloda uygulanamaz ilanlı komşular var → komşulara tur isteği (`istenen = FD.tur + 1`), `ISTEK_YINELEME` kez; açlık sürerse dizi `ISTEK_ARA`'da bir yinelenir. `A` boş ve sonlu ilanlı komşu da yoksa (adaysız) istek gönderilmez: yanıtlayabilecek kimse yok; paketler bekletilir (KK-05), sonraki selamlar beklenir. Kendim karıştırılırken (KK-03 kural 4) de istek gönderilmez: sorun benim alıcımda, yanıtları duyamam; gereksiz tur artışı da bütün ağın rotalarını çalkalar (`17` §7 madde 10).
9. **Tur isteği gelince:**
   - seçili rotamın turu ≥ istenen ve maliyetim sonlu → hemen selam (ara ilan, KK-02); yalnız duyduğum ama rotamın dayanmadığı bir tur yanıt sayılmaz (kural 6);
   - geçitsem ve turum < istenen → tur bir artar, hemen selam;
   - değilsem ve atlama sınırı (`ISTEK_ATLAMA`) dolmadıysa → istek ardılıma iletilir; ardılım isteği gönderense iletilmez (RFC 8966 §3.8.1.2); aynı istenen tur için 1 s içinde ikinci istek iletilmez.
10. **Tur yalnız istekle artar** (T-13).
11. **İleti:** `tur_istegi` = istenen tur 16 bit · kalan atlama 8 bit (`13` §02.1).

## Örnek

i'nin FD'si (tur 7, 2,0). Ardıl k'nin bağı karıştırılıyor; adaylar j (ilanı tur 7, 1,8 → uygulanabilir, 1,8 < 2,0) ve m (tur 7, 2,5 → uygulanamaz). i anında j'ye geçer: `C = ETX(i, j) + 1,8`. Yalnız m kalsaydı açlık olurdu: i, tur 8'i ister; seçili rotası tur 8'de olan ilk komşu ya da en sonunda geçit selamla yanıtlar; yeni turda m'nin ilanı uygulanabilir olur.

## Sınanması

- `istege_bagli_esik` açık ↔ kapalı: ardıl değişim sıklığı, ikizde iletim kaybı.
- Döngünün göstergesi TTL kaybı (T grubu); tur artışı ve tur isteği sayısı izlenir (`17` §7 madde 10).

## Kaynak

Uygulanabilirlik, FD, tur isteği ve yanıtı Babel [4] (RFC 8966 §3.5.1, §3.5.3, §3.7.3, §3.8.1.2, §3.8.2.1–§3.8.2.2); DSDV ailesi (De Couto 2003'te [36] aktarıldığı gibi); hazır yedek DUAL [65] ve RPL [63]; oransal geçiş Ramachandran [54].
