# B6 · Kontrol iletileri

> Yeni tasarımın (`../18-YENI-TASARIM.md`) altıncı bileşeni. İskelet `18` §1.4; sorun, kanıt, seçenekler ve kararım `18` §2.6 (27 Kasım: Z1, uyarlanır aralık). Bugünkü selamın bedeli `arsiv/teshis/faz5_3_b6_kontrol_bedeli_2026-11-27/kontrol_bedeli.txt`'te (kayıtlardan hesap, yeni koşu yok). Kurallar Babel'den (RFC 8966 [4], `protokol_kaynaklari/rfc8966_babel.txt`) ve Trickle'dan (RFC 6206 [62], `protokol_kaynaklari/faz5_arastirma_2026-10-21/rfc6206_trickle.txt`) uyarlandı; bölüm numaraları kurallarda. Değerler, bayraklar ve gözlemin kullanımı yalnız `00-DIZIN.md`de; burada adlarıyla anılır. Durum: onaylandı (27 Kasım). Önceki tasarımda karşılığı `../kural/KK-02` (selam ve ara ilan).
>
> Eksiksizlik listesinin maddeleri (`18`): 1 §1 · 2–4 `18` §2.6 · 5 §2 · 6 §3 · 7 §4 · 8 §5 · 9 §6 · 10 §7 · 11 §8 · 12 §9 · 13 §10 · 14 §11 · 15 §12 · 16 §13 · 17 §14. Ölçülen ve ölçülmeyen §15.

## 1 · Amaç ve sınıf

B6 kontrol iletilerinin biçimini ve gönderimini tek yerde toplar (`18` §1.4 sözleşme 6):
- **hangi ileti:** selam ve tur isteği;
- **ne zaman:** selamın uyarlanır aralığı ve onu öne çeken olaylar;
- **kime:** selam çoklu yayın; tur isteği B4'ün dediği gibi çoklu yayın ya da tek alıcılı.

Alınan iletileri çözer ve alanlarını sahiplerine dağıtır (sözleşme 2). Neyin taşınacağına karar vermez: değerler B1–B4'ten gelir, "hemen gönder" olaylarını onlar verir.

**Sınıf:** genel (K-247), çekirdek. Karıştırma eki tek kuraldır: kendi kanal kilidimde selam kurulmaz (kural 11). B2'nin çıktısını okur; karıştırma katmanıyla kapanır (§10).

**Hizmet ettiği hedef** (`18` §1.1):
- Koruma ölçütlerinden kontrol payı. Protokolün kendi iletileri bugün kanal süresinin %2,6'sı, onaylar dâhil %6; Babel-a'da %11 ve %15. Hedefin sınırı %10.
- Öteki bileşenlerin tepki hızı: bit değişimi, geri çekme ve tur değişimi 0,5 s içinde duyurulur. İlanın ömrü, zaman aşımı ve B2'nin selam kaybı penceresi selamın aralığına bağlıdır.

## 2 · Gördüğü (`05`; yasak alanlar okunmaz)

| kaynak | B6'nın kullandığı | kullanmadığı |
|---|---|---|
| selam ve tur isteği (`kontrol_alindi`) | alanların hepsi; çözer ve dağıtır (kural 3) | — |
| B1 | yeni komşu olayı (kural 7) | ölçüler (B3 üzerinden) |
| B2 | selamın biti ve "bit değişti" olayı; kendi durumum kanal kilidi mi (kural 11) | işaretler, aralıklar, kanıt |
| B3 | bildirilecek oran listesi (B3 kural 10, B1 kural 17) | maliyetler, durumlar |
| B4 | ilan (tur, C); "hemen gönder" olayları; tur isteği iletileri; kural 4a'nın anı (B4 Ö-5) | aday listesi, FD |
| `saat_s` | yalnız süreler | — |

**Okumadıkları:** `olculen_gurultu_w` (yasak, K-227) · RSSI · kuyruk · konum · `komsular` (simülatörün beacon listesi; protokolün kendi selamı var, `kosum_beaconi = False`) · veri paketleri.

## 3 · Tuttuğu

Düğüm başına:

| alan | başlangıç | güncellenir | silinir |
|---|---|---|---|
| `I` (geçerli aralık) | `I_MIN` | kural 5 | — |
| `sira` (bir sonraki selamın sırası) | 0 | her kurulan selamda bir artar (16 bit, modüler) | — |
| `son_selam_t` (son selamın kurulduğu an) | yok | her kurulan selamda | — |
| olay bayrağı (son selamdan beri olay oldu mu) | hayır | kural 7'de evet, selam kurulunca hayır | — |
| `C_ilan` (son selamda ilan ettiğim maliyet) | yok | her kurulan selamda | — |
| `tur_ilan` (son selamda ilan ettiğim tur) | yok | her kurulan selamda | — |
| plan: hedef anı ve nesil numarası | yok · 0 | kural 13 | — |
| kilit bekleyişi (kanal kilidi bitince selam gidecek mi) | hayır | kural 11 | — |
| son tarih planı (kural 4a'nın anı) ve nesli | yok | kural 13 | B4'ün anı değişince |

**Bellek:** sabit. Geçerli plan en çok iki (selam ve son tarih). Yeniden planlanan eski nesillerin uyandırmaları iptal edilemediği için dolana kadar bekler (en çok `I_MAX` + titreşim); sayıları birkaçı geçmez, simülatörün düğüm başına sınırı 256.

## 4 · Durumlar ve geçişler

| durum | koşul | çıkış |
|---|---|---|
| olağan | planlı selam bekleniyor; I `I_MIN`…`I_MAX` arasında | olay: I ← `I_MIN`, selam öne çekilir (kural 5, 7–8) |
| olay bekliyor | olay oldu, en kısa ara henüz dolmadı | ara dolunca selam gider (kural 8) |
| kilitte | B2'nin durumu kanal kilidi | durum değişince selam hemen gider (kural 11) |

Takılı kalma yok: her plan bir uyandırmayla biter; kilitten çıkış B2'nin bir saniyelik işaretine bağlıdır (B2 kural 6).

## 5 · Kurallar

**A · İletiler**

1. **Selam** (çoklu yayın). Alanlar:

   | alan | bit | beklenti | anlamı |
   |---|---|---|---|
   | `sira` | 16 | B1 Ö-1 | 0'dan başlar, her kurulan selamda bir artar; modüler karşılaştırılır |
   | `aralik` | 16 | B1 Ö-2, B4 Ö-4 | bir sonraki planlı selama kadarki üst sınır (kural 6); `ARALIK_BIRIMI_S` biriminde, yukarı yuvarlanır, 0xFFFF'te doyar (RFC 8966 §4.6.5) |
   | `tur` | 16 | B4 Ö-1 | ilan edilen tur (B4 kural 8) |
   | `maliyet` | 16 | B4 Ö-1 | ilan edilen maliyet, B3 kural 2'nin birimi; 0xFFFF = ∞ |
   | `bit` | 1 | B2 Ö-1 | B2 kural 9; `alici_bildirimi` kapalıyken 0 (alan kalır, B2 Ö-5) |
   | `komsu` · `oran` (tekrarlı) | 8 · 8 | B1 Ö-3, B3 §6 | bildirilecek oran listesi: adres ve `d_r` · `ORAN_OLCEK`, aşağı yuvarlanır; adrese göre sıralı |

   Boy: sabit alanlar 65 bit, yani 9 bayt; komşu başına 2 bayt; 64 bayt kapsülleme (`13` §03.1). 15 komşuyla 103 bayt (1,02 ms), 39 komşuyla 151 bayt (1,40 ms; `kontrol_bedeli.txt`).
   - Liste her selamda tamdır: her komşu her selamda listelenir. B1 Ö-3'ün sınırı (`DF_UNUT_S` içinde en az bir kez) böylece hep sağlanır.
   - Seçilmeyen: Babel'deki gibi ters yön bildirimini seyrek göndermek (kayıpsız bağda üç selamda bir, RFC 8966 Ek B). Bugün liste selamın ~29 baytı; üç selamda bire inmesi protokolün kanal payını ~%0,4 azaltırdı (kestirim: selam ~1,01 ms'den ~0,86 ms'ye). Ama B3'ün maliyeti `d_f`'yi doğrudan kullanır ve temiz kanalda bile selamların ~%46'sı kaybolur (B2 §11 madde 6); seyrek liste `d_f`'yi bayatlatırdı.
2. **Tur isteği** (B4 Ö-3): `istenen_tur` 16 bit, `kalan_atlama` 8 bit; 3 bayt + 64 = 67 bayt. Alıcısını B4 söyler:
   - çoklu yayın: açlık (B4 kural 11);
   - tek alıcılı (7 deneme): yok sayma (kural 10), tercih edilir ilan (kural 10a), iletme (kural 12), rota isteği (kural 4a; kalan atlama 1).
3. **Alınan iletinin çözülmesi ve dağıtımı** (sözleşme 2):
   - selam: sıra, aralık ve benim için bildirilen oran B1'e; bit B2'ye; tur ve maliyet B4'e. Gönderen beni listelemiyorsa oran "bilinmiyor"dur (B1 kural 7);
   - tur isteği: gönderen, istenen tur ve kalan atlama B4'e.

   Çözme, olay sırasının 2. adımıdır (`18` §1.4, 28 Kasım düzeltmesi): alanlar B1'in zaman olaylarından sonra, öteki bileşenlerin o kancadaki kararlarından önce dağıtılır.

**B · Selamın zamanlaması** (Z1; Trickle'ın aralığı, RFC 6206 §4.2 kural 5–6)

4. **Açılış:** I = `I_MIN`. İlk selam hemen, titreşimle gider (kural 9).
5. **Uyarlama** (`uyarlanir_aralik`):
   - Selam kurulurken son selamdan beri olay yoksa önce I ← min(2 · I, `I_MAX`); olay varsa I değişmez.
   - Bir olay (kural 7) I'yı `I_MIN`'e indirir ve selamı öne çeker (kural 8).
   - Sonraki planlı selam, kurulan selamdan I sonradır.
   - Sonuç: sakin ağda aralıklar 1, 2, 2, … s; bir olaydan sonra 0,5, 1, 2, 2, … s.
   - `uyarlanir_aralik` kapalıyken I sabit `I_MAX`'tır; olay yine selamı öne çeker, I'yı değiştirmez (önceki tasarım, Y-5).
   - **Trickle'dan farklar:** bastırma yok (RFC 6206 kural 3–4): komşular bağımı selamlarımın sıra numarasından ölçer, atlanan selam onlarda kayıp sayılırdı (`17` T-16). Gönderim anı aralığın ikinci yarısında rastgele değil (kural 2), başında küçük bir titreşimle: olay en kısa sürede duyulur; eşzamanlanmayı en kısa ara ve titreşim önler (kural 8–9).
6. **Aralık alanı:** her selam, bu selamdan sonra geçerli I'nın `ARALIK_PAYI` katını taşır: titreşim payıyla bir sonraki planlı selamın üst sınırı (RFC 8966 §4.6.5).
   - I yalnız selam kurulurken büyür, arada yalnız küçülür (olay). Böylece alan her zaman bir üst sınırdır (RFC 8966 §3.4.1: aralık her an azaltılabilir, ancak selamdan hemen önce artırılabilir).
   - Alıcının zaman aşımı (B1 kural 5) ve ilanın ömrü (B4 kural 4) bu alana dayanır.
7. **Olaylar** (selamı öne çekenler; birkaçı birleşebilir):
   - **B4:** geri çekme ya da dönüş (C ∞ ↔ sonlu); ilan edilen turun değişmesi (istek yanıtı dâhil); B4 kural 12'nin "hemen gönder"i (tur isteğine ve kural 4a'nın rota isteğine yanıt); maliyetin önemli değişimi: |C − `C_ilan`| ≥ `ILAN_ESIGI` · `C_ilan`. Geçitte C hep 0'dır.
   - **B2:** "bit değişti" (B2 kural 9, Ö-2).
   - **B1:** yeni komşu (B1 kural 18). İki yönlü ölçüm ancak her iki tarafta `ORNEK_EN_AZ` selamla kurulur (B1 Ö-7); en kısa aralıkla ~2 s sürer.
   - Kendi kanal kilidimin bitişi (kural 11).

   **Olay olmayanlar:**
   - **Tek başına ardıl değişimi:** maliyeti önemli değiştiriyorsa maliyet maddesine girer. RFC 8966 §3.7.2 maliyeti belirgin değiştirmeyen ardıl değişiminde tetiklenen güncelleme istemez (SHOULD NOT). v0.4.1'de her ardıl değişiminde giden ilan kanalı dolduruyordu (`17` T-17: koşu başına 24 122 tetik ilanı). B4 kural 15'in olay listesi buna göre düzeltildi (27 Kasım).
   - **Bir komşunun durum değişimi** (S'ye düşmesi, dönmesi): yolumu değiştiriyorsa maliyet maddesine girer (önceki tasarım, KK-02 kural 3). Karıştırma sırasında, kanal zorlanırken selam seli böylece oluşmaz.
8. **En kısa ara:** iki selam arasında en az `SELAM_ARASI_EN_AZ` geçer (B1 Ö-4). Olay selamı, son selamdan bu kadar süre geçtiyse hemen, geçmediyse süre dolunca gider. Arada olan olaylar o selamda birleşir.
9. **Titreşim** (RFC 8966 §3.1, SHOULD):
   - planlı ve olay selamı U(0, `TITRESIM_ORANI` · I) titreşimle gider;
   - çoklu yayın tur isteği U(0, `TITRESIM_ORANI` · `ISTEK_ARALIK_S`) ile;
   - tek alıcılı iletiler titreşimsiz gider: alıcı tek, MAC'in geri çekilmesi yeter.

   Gerekçe: aynı olayı (ör. geçitteki tur artışı) duyan komşuların selamları eşzamanlanmasın. Babel'in acil iletileri 0,2 s içinde gider (Ek B); burada olay selamının titreşimi en çok 0,05 s (I = `I_MIN`). ETX'in yoklamaları da ±0,1 · τ titreşimlidir [36].
10. **Selam anında kurulur:** içerik, uyandırmanın titreşimden sonraki anında, o anki bilgiyle kurulur: B2'nin biti, B3'ün oran listesi, B4'ün (tur, C). Titreşim boyunca bayatlamaz (önceki tasarım, G-5). Kuyrukta beklerken içerik kurulduğu gibi kalır.

**C · Kendi karıştırılmam** (karıştırma eki)

11. **Kendi kanal kilidimde selam kurulmaz:** B2'nin durumu "kanal kilidi" iken selam uyandırması selam kurmaz, sırayı tüketmez ve yeni plan kurmaz; olaylar da plan kurmaz. Durum değişince (yok ya da girişim) selam hemen gider; bu bir olaydır (kural 7).
    - Gerekçe: kanal kilidinde geri çekilme bitmez (simülatör). Kurulan selamlar kontrol kuyruğunda birikir, kanal açılınca bayat içerikle art arda giderdi (B2 Ö-4). Sırası tüketilip gönderilmeyen selam alıcıda kayıp sayılır (B1 Ö-5); kurulmayan selam sıra tüketmez. Alıcıda zaman aşımının eklediği sıfırları, selamım dönünce geri alma siler (B1 kural 4).
    - Kilitten hemen önce kurulup kuyrukta bekleyen en çok bir selam, kilit bitince eski bitiyle gidebilir. Ardından gelen olay selamı onu düzeltir.
    - Girişimde selam olağan kurallarla gider; bit 1'dir.
    - Durum sürerken (bit 1) aralık ayrıca kısaltılmaz (B2 Ö-3); `18` §2.6'da Z3 seçilmedi: bitin hızlanması J1'e en çok 0,004 katar.
    - Karıştırma katmanı kapalıyken B2 hep "yok" der: selam kilitte de kurulur ve kuyrukta bekler.
12. **Kendi kanal kilidimde tur isteği** de gitmez: B4 kural 14 onu zaten bastırır. B6 ayrıca bir şey yapmaz.

**D · Uyandırma ve sıra**

13. **Uyandırmalar:** simülatörde uyandırma iptal edilemez; her plan bir nesil numarası taşır, eski nesilden gelen uyandırma yok sayılır (önceki tasarım). İki plan tutulur:
    - **selam:** bir sonraki planlı ya da olay selamının anı (kural 5, 8);
    - **son tarih:** B4 kural 4a'nın anı (B4 Ö-5). Ancak selam planından önceyse ve henüz istek gitmediyse kurulur. Her niyetli kancada yeniden değerlendirilir; B4'ün anı değişince (yeni ilan, ardıl değişimi) yeni nesille yeniden kurulur.

    B1'in son tarihi (B1 Ö-6) ve B4 kural 4'ün düşme anı için ayrı uyandırma kurulmaz. Anları doğru yazıldığı için bir sonraki niyetli kancada işlenirler. Her paket kararı (`sonraki_atlama`) ve her alınan kontrol iletisi böyle bir kancadır; saniyelik zamanlayıcı da gecikmeyi en çok 1 s'de tutar. Kural 4a'nın penceresi ise bir selam aralığıdır (0,55 s'ye inebilir); onun için uyandırma kurulur.
14. **Sıra:** B6 her niyetli kancada B1–B5'ten sonra çalışır (`18` §1.4 olay sırası 5). O kancanın olaylarını toplar (kural 7), gerekirse selamı planlar ya da kurar ve B4'ün tur isteklerini gönderir. Selamın kurulması kendi uyandırmasında olur (kural 10). Kontrol iletileri yalnız `kontrol_alindi` kancasında gelir ve orada çözülür (kural 3). Niyet döndüremeyen kancalarda (`iletim_sonucu`, `cerceve_duyuldu`) B6 çalışmaz; o kancalarda doğan olaylar bir sonraki niyetli kancada işlenir.

## 6 · İletiler

Bu bileşenin iletileri kural 1–2'dedir.

**Kontrol yüküne katkı:**
- **Bugün** (`eğim0`, aynı biçim ve zamanlama; `kontrol_bedeli.txt`): düğüm başına saniyede 0,62–0,67 selam, %15–19'u ara ilan. Protokolün iletileri kanal süresinin %2,6–2,7'si, ileti başına ~100 bayt.
- **Yeni tasarımın ekleri:**
  - bit değişimleri: kaba kestirim, birincilde 30 s'lik çevrimde ağda ~16 ek selam (B2 §6);
  - kural 4a'nın rota istekleri ve yanıt selamları;
  - kural 10a'nın tur istekleri.

  Sayıları ölçülmedi; tanıda sayılır (§13). Kaba kestirimle protokolün payı %3 dolayında, onaylar dâhil %6–7 kalır; hedefin sınırı %10'un ve Babel'in %15'inin altında.

**Beklentilere karşılık** (B1–B4'ün B6'dan beklediği):

| beklenti | karşılığı |
|---|---|
| B1 Ö-1 sıra · Ö-2 aralık alanı · Ö-3 komşu listesi | kural 1, 6 |
| B1 Ö-4 iki selam arası en az 0,5 s | kural 8 (`SELAM_ARASI_EN_AZ`) |
| B1 Ö-5 sırası tüketilen selam gönderilir | kural 11: kilitte selam kurulmaz, sıra tüketilmez |
| B1 Ö-6 son tarih için uyandırma | kural 13: kurulmaz, bir sonraki niyetli kancada işlenir |
| B1 Ö-7 yeni komşu | kural 7: olay |
| B2 Ö-1 bit · Ö-5 bayrak kapalıyken alan | kural 1 |
| B2 Ö-2 "bit değişti"de hemen selam | kural 7–8 |
| B2 Ö-3 durum sürerken aralık | kural 11: kısaltılmaz (Z3 seçilmedi) |
| B2 Ö-4 kilitte bekleyen bayat selam | kural 11 |
| B3 §6 oran listesi | kural 1 |
| B4 Ö-1 her selamda ilan | kural 1 |
| B4 Ö-2 "hemen gönder" | kural 7–8; tek başına ardıl değişimi olay değil (B4 kural 15 düzeltildi) |
| B4 Ö-3 tur isteği iletisi | kural 2 |
| B4 Ö-4 aralık alanı ilanın ömrü için | kural 6 |
| B4 Ö-5 kural 4 ve 4a'nın anları için uyandırma | kural 13: 4a için kurulur, 4 için bir sonraki niyetli kanca |

## 7 · Değerler

`I_MIN` · `I_MAX` · `ARALIK_PAYI` · `TITRESIM_ORANI` · `SELAM_ARASI_EN_AZ` · `ILAN_ESIGI` · `ARALIK_BIRIMI_S` · `ORAN_OLCEK`. B4'ten kullanılan: `ISTEK_ARALIK_S` (kural 9). Değeri, birimi, kaynağı, küçük ve büyük olursa ne olacağı ve taranıp taranmayacağı `00-DIZIN.md`'nin değer tablosunda.

## 8 · Kenar durumlar

- **Soğuk açılış:** ilk selam hemen gider (kural 4). Komşu listesi boştur (73 bayt). İlk komşular yeni komşu olayıyla I'yı `I_MIN`'de tutar; iki yönlü ölçüm ~2 s'de kurulur.
- **Geçit:** aynı kurallar. Maliyeti hep 0, turu kendi turudur; turu istekle artınca bu bir olaydır (kural 7).
- **Hiç komşu yok:** selam yine gider; liste boş. **Tek komşu:** özel bir durum yok.
- **Düğüm kendisi karıştırılırken:** kanal kilidinde selam kurulmaz (kural 11); girişimde olağan, bit 1.
- **Komşu karıştırılırken:** B6 için özel bir durum yok. Rotam değişirse maliyet olayı, komşunun biti değişirse onun selamı gelir.
- **Sayaç taşması:** `sira` 16 bit, modüler (65535'ten sonra 0). Aralık alanı 0xFFFF'te doyar (655 s; `I_MAX` 2 s'yle hiç olmaz).
- **Zaman aşımı:** B6'nın kendi zaman aşımı yok; uyandırmalar kural 13'te.
- **Aynı anda olaylar:** birleşir (kural 8). Aynı kancada hem selam uyandırması hem olay varsa tek selam gider.
- **Tamponun dolması:** kontrol kuyruğu simülatörün (kapasite 50, dolunca `kuyruk_tasmasi`, `13` §03.2). Kilitte selam kurulmadığı için kilit kuyruğu selamla doldurmaz. Katman kapalıyken doldurabilir; tanıda sayılır.

## 9 · Arayüz

**Kancalar:**

| kanca | B6'ya giden | B6'nın işi |
|---|---|---|
| `kontrol_alindi` | ileti, gönderen | çözme ve dağıtım (kural 3, olay sırası 1); sonra kural 7–9, 13 (olay sırası 5) |
| `uyandi`: selam ya da son tarih | etiket (nesil) | güncel nesilse selamı kurar (kural 5–6, 10–11) ya da o kancada B4'ün kural 4a'sı çalışır |
| saniyelik zamanlayıcı, `iletim_basarisiz`, `sonraki_atlama` | — | kural 7–9, 13 (o kancanın olayları) |
| niyetsiz kancalar | — | — |

**Okuduğu:** B1, B2, B3, B4 (§2); yalnız kendinden aşağıdakileri (sözleşme 1).

**Çıktılar:**

| çıktı | kural | okuyan |
|---|---|---|
| selam (`KontrolIstegi`, çoklu yayın, titreşimli) | 1, 4–11 | simülatör |
| tur isteği (`KontrolIstegi`, B4'ün alıcısıyla) | 2, 9 | simülatör |
| uyandırmalar (`Uyandirma`, nesil numaralı) | 13 | simülatör |
| çözülen alanlar | 3 | B1, B2, B4 |

## 10 · Kapalıyken davranış

B6'nın bütünü çekirdektir: selam olmadan komşu, bağ ve yol bilinemez. Alt mekanizmalar:
- **`uyarlanir_aralik` kapalı** (genel): I sabit `I_MAX`; olaylar selamı yine öne çeker, I'yı değiştirmez.
- **Karıştırma katmanı kapalı** (`karistirma_katmani`): kural 11 çalışmaz, selam kilitte de kurulur; bit hep 0 gider (B2), "bit değişti" olayı oluşmaz.
- `alici_bildirimi` kapalıyken bit alanı kalır ve 0 gider; ileti boyu ve kontrol yükü değişmez (B2 Ö-5).

## 11 · Etkileşimler

1. **B1:**
   - zaman aşımı aralık alanına dayanır; alan hep üst sınırdır (kural 6);
   - B1'in saklaması (`SELAM_SAKLA`) ve boşluk sınırı (`BOSLUK_EN_COK`) en kısa araya (0,5 s) dayanır;
   - kilitte selam kurulmadığı için sıra boşluğu oluşmaz (Ö-5).
2. **B2:**
   - bit ve "bit değişti" olayı kural 1 ve 7'de;
   - kendi durumum kural 11'de;
   - B2'nin selam kaybı penceresi (`KAYIP_PENCERE_S`, 4 s) bu aralıkla komşu başına 2–8 örnek görür; eşikler bu trafikte ölçüldü.
3. **B3:** oran listesi kendi aralıklarımla istenir (B3 kural 10); B6 yalnız taşır.
4. **B4:**
   - ilan her selamdadır;
   - FD, ilan B4'ten B6'ya verildiği anda B4'te güncellenir (B4 kural 9); selamın gidip gitmemesi FD'yi etkilemez;
   - "hemen gönder" olayları kural 7'de; tek başına ardıl değişimi olay değildir, B4 kural 15 buna göre düzeltildi;
   - kural 4a'nın yanıtı bir olay selamıdır; en kısa ara (0,5 s) bu yüzden `SURE_ISTEK_PAYI` (bir selam aralığı) içinde kalır.
5. **B5, B7:** B6 veri paketine dokunmaz. Kontrol kuyruğu veriden önceliklidir (`13` §03.2); sık selam veri paketlerinin bekleyişini uzatır. Bedeli kontrol payındadır.
6. **Kanıtı silmeme** (sözleşme 4): B6 hiçbir gözlemi silmez. Kilitte selam kurmamak alıcılarda o süre için selam boşluğu bırakır; geri alma sıfırları siler (B1 kural 4). Kanıt kaybolmaz: kilitteki komşuyu göndericinin kanıtı ve ilanın ömrü gösterir (B2 §8, B4 kural 4).
7. **Mekanizma kapısı:** çekirdek (zamanlama, olaylar, biçim) iki kolda aynıdır. Kapıya giren tek kural 11'dir. Katman kapalıyken kilitte kurulan selamların bayat birikmesi kapının kolunda kalır.

## 12 · Örnek senaryo

Düğüm i'nin selamları. Titreşim yazılmadı (en çok 0,1 · I).

1. **Açılış:** 0,30 s'de ilk selam (sıra 0). Olay yok: I 0,5'ten 1'e çıkar, aralık alanı 1,1 s. Sonra 1,30 (I → 2, alan 2,2 s), 3,30, 5,30 s…
2. **Bit değişimi:** 152,9 s'de planlı selam gitti (I = 2). 153,4'te B2'nin biti 1 olur: olay, I = 0,5. Son selamdan 0,5 s geçtiği için selam 153,4'te gider, alan 0,55 s. Sonra 153,9 (olay yok, I → 1, alan 1,1), 154,9 (I → 2), 156,9…
3. **Önemli olmayan maliyet değişimi:** `C_ilan` 3,2 ETX (205 birim). Yeni C 3,5 ETX (224): |224 − 205| = 19 < 0,15 × 205 = 30,75. Olay değil; değer bir sonraki planlı selamla gider.
4. **Önemli maliyet değişimi:** yeni C 3,8 ETX (244): 39 ≥ 30,75, olay. Selam en kısa arayla gider.
5. **Tek başına ardıl değişimi:** isteğe bağlı geçişle ardıl j'den k'ye, C 2,3'ten 2,4 ETX'e: fark %4, olay değil.
6. **Geri çekme:** açlık, C ∞: olay, selam hemen. B4'ün açlık isteği çoklu yayınla gider, titreşimi U(0, 0,05 s); 0,5 s arayla üç kez daha yinelenir (B4 kural 11).
7. **Rota isteği** (B4 kural 4a): ardıl l'nin son ilanı 300,0 s'de, aralığı 2,0 s. 305,0 için son tarih uyandırması kurulur; i o anda l'ye titreşimsiz, tek alıcılı istek gönderir. l'de istek `kontrol_alindi` ile B4'e gider, kural 12 "hemen gönder" der. l'nin son selamı 304,0'da olduğu için en kısa ara dolmuştur: l'nin selamı 305,0x'te gider.
8. **Kendim kanal kilidinde:** i 180,0–190,0 s arasında karıştırıcıya çok yakın; 183,7'de B2'nin durumu "kanal kilidi".
   - 184,2'deki planlı uyandırma selam kurmaz, sırayı tüketmez.
   - 190,3'te durum "yok"a döner: olay, selam hemen, taze içerikle (sıra bir öncekinin devamı); alan 0,55 s.
   - Komşularda zaman aşımının eklediği sıfırlar, sıra ilerlemediği için geri almayla silinir (B1 kural 4).

## 13 · Sınanması

**Birim testleri** (Aşama 4):
1. **Biçim:** selamın alanları ve boyu (9 bayt + komşu başına 2); oranın 8 bitlik biçimi (aşağı yuvarlama); aralık alanının yukarı yuvarlanması ve doyması; tur isteğinin 3 baytı.
2. **Çözme ve dağıtım:** alanların B1'e, B2'ye ve B4'e gitmesi; beni listelemeyen selamda oran "bilinmiyor".
3. **Zamanlama:**
   - açılışta hemen;
   - olaysız ikiye katlama ve `I_MAX` sınırı;
   - olayda `I_MIN`;
   - aralık alanının planlı ve olay selamında üst sınır olması.
4. **En kısa ara:** 0,5 s içinde birden çok olayın tek selamda birleşmesi.
5. **Olaylar:**
   - her olay türü;
   - tek başına ardıl değişimi ve komşunun durum değişimi olay değil;
   - `ILAN_ESIGI` sınırı (tam eşitlik dâhil);
   - ∞ ↔ sonlu; geçitte maliyet 0.
6. **Titreşim:** aralığı; tek alıcılı iletide titreşim yok.
7. **Kanal kilidi:** selam kurulmaz, sıra tüketilmez; bitişte hemen selam; katman kapalıyken kurulur.
8. **Uyandırma:** nesil numarası; eski nesil yok sayılır; kural 4a'nın son tarihi.
9. **`uyarlanir_aralik` kapalı:** I sabit `I_MAX`; olaylar öne çeker, I değişmez.
10. Örnek senaryonun (§12) sayıları uçtan uca.

**Ölçümde sayılacak tanı:**
- selam sayısı ve aralığın dağılımı; ara ilanların olaya göre sayısı;
- kilitte kurulmayan selamlar; kontrol kuyruğunda bekleme süresi ve taşma;
- tur isteklerinin türüne göre sayısı (açlık, yok sayma, 10a, 4a, iletme);
- kontrol payı, protokolün iletileri ve veri onayları ayrı (`kontrol_bedeli.py`'nin ayrımı).

## 14 · Kaynak

- **Selam, sıra numarası, aralık alanı (üst sınır, santisaniye) ve aralığın değiştirilme kuralı:** Babel, RFC 8966 [4] §3.4, §3.4.1, §4.6.5. Ters yön bildiriminin selamda taşınması ETX'ten [36] ve Babel'den.
- **Aralığın ikiye katlanıp olayda en küçüğe inmesi:** Trickle, RFC 6206 [62] §4.2 kural 5–6. Bastırma (kural 3–4) ve aralığın ikinci yarısında rastgele gönderim (kural 2) alınmadı (kural 5).
- **Tetiklenen güncellemenin kuralları:** RFC 8966 §3.7.2 (geri çekmede SHOULD; maliyeti belirgin değiştirmeyen ardıl değişiminde SHOULD NOT).
- **Titreşim:** RFC 8966 §3.1 ve Ek B (acil iletiler 0,2 s içinde); ETX'in yoklama titreşimi [36].
- **Önceki tasarım:** `../kural/KK-02` (`17` T-1, T-16, T-17): zamanlama, ara ilan, kilitte selam kurmama, selamın anında kurulması. Değerler oradan; kurallar bu kâğıt için yeniden yazıldı.
- **Bu tasarımın:**
  - ilanın ve oran listesinin tek selamda, listenin her selamda tam taşınması;
  - olay kümesi: tek başına ardıl değişiminin ve komşu durumunun olay sayılmaması;
  - kural 4a'nın anı için uyandırma; öteki son tarihlerin bir sonraki niyetli kancaya bırakılması;
  - tek alıcılı iletilerin titreşimsiz gönderilmesi.

## 15 · Ölçülen ve ölçülmeyen

**Ölçülen** (bugünkü kodun `eğim0` kolu, aynı biçim ve zamanlama; `kontrol_bedeli.txt`):
- selam sıklığı (düğüm başına saniyede 0,62–0,67) ve ara ilan payı (%15–19);
- protokolün iletilerinin kanal payı (%2,6–2,7) ve veri onaylarınınki (%3,2–3,5); Babel-a'nın kendi iletileri %11–12;
- B2'nin eşikleri ve B3, B5 teşhisleri bu selam trafiğinde ölçüldü.

**Ölçülmeyen** (Aşama 4'te sayılır ya da ablasyonla ölçülür):
- yeni tasarımın selam sıklığı (bit değişimleri, kural 4a ve 10a'nın istekleriyle);
- `uyarlanir_aralik`'ın katkısı;
- kilitte selam kurmamanın katkısı (karıştırma katmanıyla birlikte);
- `ILAN_ESIGI` ve `I_MAX`'ın etkisi (seçenek Z2'nin sorusu).
