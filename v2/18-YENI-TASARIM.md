# 18 · YENİ TASARIM — DESPARETE'nin baştan, bileşen bileşen tasarımı

> 24 Kasım 2026'da başladı (`12` §1.2 madde 3b). Faz 5-3'te üç sürüm ölçüldü: 18 Kasım çekirdeği, 19 Kasım çekirdeği ve bileşenleri, 20 Kasım'ın döngü kuralları. Her biri bir sorunu çözerken başka bir sorun açtı. Öğrenilenlerle protokolü baştan, tek tek ve eksiksiz tasarlamak istiyorum; ölçüm tasarım donduktan sonra yapılır.
>
> Bu belge yöntemi, eksiksizlik listesini ve aşamaların durumunu tutar. Bileşen kararları burada (bileşen başına bir bölüm), kuralları yeni kural kâğıtlarında yazılır. `17` ve `kural/KK-*` önceki tasarımdır: yeni tasarım donana kadar bugünkü kodun ve ölçümlerin belgesi olarak kalır, sonra arşive gider.

## Durum

| aşama | durum |
|---|---|
| 1 · Zemin | sırada |
| 2 · Bileşen bileşen tasarım | bekliyor |
| 3 · Bütünlük ve donma | bekliyor |
| 4 · Kod ve ölçüm | bekliyor |

## Yöntem

- Her bileşende aynı adımlar izlenir:
  1. sorun ve ölçülmüş kanıt;
  2. en az iki seçenek, bedelleriyle; seçilmeyenin neden seçilmediği;
  3. kararım;
  4. kural kâğıdı (aşağıdaki eksiksizlik listesine göre);
  5. sade anlatım ve onayım.
- **Ölçüm:** tasarım sırasında A/B yapılmaz. Bir kararın girdisi eksikse kısa, önceden yazılı bir teşhis ölçümü yapılabilir (geliştirme tohumları 1003–1010; ana deney tohumları kullanılmaz).
- **Sayısal değerler:** her değerin kaynağı, neyi etkilediği, küçük ve büyük olursa ne olacağı ve sonra taranıp taranmayacağı yazılır.
- **Kanıt:** tek tohumluk sınama ve duman koşusu karar girdisi değildir; ölçülmemiş bir şey bulgu diye yazılmaz.
- **Eskiler:** eski kod ve kâğıtlar silinmez; kaynak ve karşılaştırma olarak kalır. Yeni tasarım yeni belgelere yazılır.

## Aşamalar

### 1 · Zemin (henüz tasarım kararı yok)

1. **Hedef ve başarı ölçütü:** ana ölçü birincil hücrede `PDR_açık`. Yanında en kötü tohum, sessiz dönemin teslimi, gecikmenin p99'u, kontrol payı ve "ikizde zarar yok". Hepsi Babel'e ve kâhine göre, sayıyla, önceden yazılır.
2. **Kısıtlar:**
   - gözlem sözleşmesi ve protokolün okuyamadıkları (`05`, `13`);
   - paket başlığına değer yazılamaması (K-232);
   - tek kanal;
   - trafik deseni (yere toplama ve komut);
   - hücreler ve kollar (`06`).
3. **Kanıt envanteri:** Faz 5'te ölçülen her şey tek yerde, kaynağıyla; ne biliniyor, ne bilinmiyor.
4. **Mimari iskelet:** bileşenler ve aralarındaki sözleşme; kim neyi okur ve yazar, hangi kancada çalışır, olayların sırası.

### 2 · Bileşen bileşen tasarım

Sıra bileşenlerin birbirine bağımlılığına göre. Her bileşenin yanında, ilk elde dayanacağı ölçülmüş kanıt var.

1. **Komşu ve bağın ölçüsü.**
   - Selam, girişimde bağı olduğundan kötü gösteriyor: bağ çıkışı anında selamın ölçtüğü `d_f · d_r` ~0,23–0,24, kâhinin tek deneme başarısı ~0,71–0,76 (`arsiv/teshis/faz5_3_aclik_2026-11-18/sonuc.md` §6).
   - Veri tetiği kapalıyken vazgeçmelerin %41'i en kötü beş bağda; selamı geçen ama veriyi taşıyamayan kalıcı bağlar var (aynı belge §6).
   - Veri denemelerinin yarısından fazlası başarısız, denemelerin %94–96'sı en düşük hızda (`arsiv/teshis/faz5_2_secenek_iletim_2026-11-15/sonuc.md`).
2. **Karıştırma kanıtı.**
   - Teşhis (d) (`arsiv/teshis/faz5_2_isaretler_2026-11-16/sonuc.md`):
     - ED bölgesinde altı işaretin altısı güçlü;
     - girişim bölgesinde çözülen çerçeve düşüşü ve selam kaybı güçlü ama tek başına yanlış alarmı yüksek;
     - art arda üç MAC vazgeçmesi yanlış alarmı seyrek tutuyor ama geç kalıyor.
   - Kalabalığın yarattığı yanlış alarm riski (`kural/KK-03` kural 12).
   - Karıştırma katmanı bütünüyle hiç ölçülmedi.
3. **Bağın durumu, bırakma ve geri dönüş zamanı.**
   - Birincilde sessiz dönemin teslimi: eğimli kollar 0,83–0,87, uygulanabilirlik koşullu yol seçimi 0,911, Babel 0,916 (`arsiv/teshis/faz5_3_dongu_kurallari_2026-11-24/sonuc.md` §8).
   - Karıştırma bittikten sonraki toparlanma bu bileşenin sorusu.
4. **Yol seçimi ve döngü.**
   - Veri tetiği uygulanabilirlik koşuluyla birleşince açlık zinciri doğdu (açlık teşhisi).
   - Ölçülmüş takas (`arsiv/teshis/faz5_3_yeni_cekirdek_2026-11-19/sonuc.md` · `arsiv/teshis/faz5_3_dongu_kurallari_2026-11-24/sonuc.md`):
     - eğim, karıştırmasız ağda ve ikizde önde (geri gönderme yasağı ve sınırlı yükselmeyle 0,958, Babel 0,930);
     - uygulanabilirlik koşulu karıştırma altında en kötü tohumda (0,470 ↔ 0,408) ve sessiz dönemde önde, döngüsüz.
   - Geri gönderme yasağı, döngü bekçisinin iki düğümlü döngü kanıtını siliyor; tek başına zararlı.
   - Sınırlı yükselme döngüyü %68 azaltıyor ama rota yokluğunu artırıyor.
5. **Karıştırma altında iletim** (yedek, gerekirse çoğaltma ya da fırsatçı iletim).
   - Birincilde beş farklı yol seçiminin `PDR_açık` ortalaması 0,659–0,666; kayıp çoğunlukla iletimde (0,267–0,335); kâhin 0,779. Kazanılabilecek pay burada.
   - Çoğaltma yalnız son çare (`17` T-14); her pakete kopya kanalı boğuyor (K-238).
   - Fırsatçı iletim simülatörde yeni bir iletim türü ister (`protokol_kaynaklari/faz5_3_arastirma_2026-11-19/NOTLAR.md` §3).
6. **Kontrol düzlemi** (selam aralığı, ara ilan, ileti boyutları).
   - Bugünkü tasarımda kontrol payı %6, Babel %15; eğimin selamı 7 bayt + komşu başına 2 bayt.
7. **Bekletme, komutun yolu, gecikme.**
   - Bekletme 1 s ↔ 2 s ikizde ayırt edilemedi.
   - Komutun geri izi (v0.4.1'in V11'i); gecikmenin p99'u.

### 3 · Bütünlük ve donma

1. Bütün bileşenler birlikte denetlenir (aşağıdaki "Bütünlük denetimi" listesi).
2. Bağımsız denetim (17 Kasım'daki kural denetimi gibi).
3. Tasarım donar. Büyük ölçümün beklentisi (hücreler, kollar, karar kuralı) tasarımla birlikte yazılır.

### 4 · Kod ve ölçüm

1. **Kod:** yeni, temiz modüller; her kurala birim testi, uçtan uca testler, mimari denetimi.
2. **Tek büyük ölçüm:**
   - hücreler: ikiz, birincil, dayanıklılık ve yer karıştırıcılı aile;
   - kollar: tam sürüm ve her mekanizmanın ablasyonu;
   - karşılaştırma: Babel ve kâhin.
3. **Geliştirme:** sonuçtan sonra sürer.

## Eksiksizlik listesi

### Her bileşen kâğıdında

Hepsi cevaplanmadan bileşen bitmiş sayılmaz.

1. **Amaç ve sınıf:** karıştırmaya karşı mı, genel mi (K-247); hangi hedefe (Aşama 1.1) hizmet ediyor.
2. **Sorun ve kanıt:** ölçülmüş kanıt, kaynağıyla; ölçülmemiş olan açıkça "varsayım".
3. **Seçenekler:** en az iki; her birinin bedeli; seçilmeyenin neden seçilmediği.
4. **Kararım ve tarihi.**
5. **Gördüğü:** gözlem sözleşmesinin hangi alanları; yasak alanların okunmadığı.
6. **Tuttuğu durum:** her alanın başlangıç değeri, ne zaman güncellendiği, ne zaman silindiği; belleğin üst sınırı.
7. **Durumlar ve geçişler:** her durum, her geçiş ve tetikleyicisi; her durumdan bir çıkış olduğu (takılı kalma yok).
8. **Kurallar:** numaralı, tek anlamlı; formüller ve birimleri.
9. **İletiler:** alanlar, bit genişlikleri, boyut; kontrol yüküne katkısı.
10. **Değerler:** her değer için birim, kaynak, neyi etkilediği, küçük ve büyük olursa ne olacağı, sonra taranıp taranmayacağı.
11. **Kenar durumlar:**
    - soğuk açılış;
    - geçit düğümünün kendisi;
    - hiç komşu yok ve tek komşu;
    - düğüm kendisi karıştırılırken;
    - sayaç taşması (modüler karşılaştırma);
    - zaman aşımı;
    - aynı anda gelen olaylar;
    - tamponun dolması.
12. **Arayüz:** öteki bileşenlerden okuduğu ve onlara yazdığı; hangi kancada çalıştığı; olayların sırası.
13. **Kapalıyken davranış:** ablasyon bayrağı ve kapalıyken ne olduğu.
14. **Etkileşimler:** öteki kurallarla çakışma ya da birbirinin kanıtını silme (döngü kurallarında görüldü: geri gönderme yasağı döngü bekçisinin kanıtını sildi).
15. **Örnek senaryo:** sayılarla, baştan sona.
16. **Sınanması:** birim testlerinin listesi; ölçümde sayılacak tanı.
17. **Kaynak:** ödünç alınan her parçanın kaynağı ve özgün olan kısım.

### Bütünlük denetiminde (Aşama 3)

1. Bütün değerler tek tabloda; bir değer iki yerde tanımlı değil.
2. Bütün iletiler ve boyutları; kontrol payının kestirimi.
3. Bütün durumların birleşimi: iki bileşenin durumları birbiriyle çelişmiyor.
4. Uçtan uca senaryolar:
   - soğuk açılış ve sakin ağ;
   - karıştırma başlıyor ve bitiyor (ED ve girişim bölgesi);
   - düğüm kopuyor ve dönüyor;
   - döngü oluşuyor;
   - geçide yakın karıştırma;
   - komutun yolu.
5. İzlenebilirlik: her hedefin hangi bileşenle, hangi kuralla, hangi testle ve hangi ölçümle karşılandığı.
6. Her ilkenin (`17` §0'ın ve yeni tasarımın ilkeleri) hangi kurallarla karşılandığı.
7. Bağımsız denetimin bulguları ve kapanışı.
