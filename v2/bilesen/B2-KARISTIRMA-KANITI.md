# B2 · Karıştırma kanıtı

> Yeni tasarımın (`../18-YENI-TASARIM.md`) ikinci bileşeni. İskelet `18` §1.4; sorun, kanıt, seçenekler ve kararım `18` §2.2 (24 Kasım; kanal kilidi kuralı 25 Kasım). Kuralların ve eşiklerin kaynağı teşhis ölçümüdür: `arsiv/teshis/faz5_3_b2_isaretler_2026-11-24/` (`beklenti.md`, `sonuc.md`, `ek_hesap.txt`; bundan sonra "teşhis"). Değerler, bayraklar ve gözlemin kullanımı yalnız `00-DIZIN.md`de; burada adlarıyla anılır. Durum: onaylandı (25 Kasım). Önceki tasarımda karşılığı `../kural/KK-03` (orada kendi durumum, bağ kanıtı ve bağın "bitti"si tek kâğıttaydı; bağın durumu artık B3'te).
>
> Eksiksizlik listesinin maddeleri (`18`): 1 §1 · 2–4 `18` §2.2 · 5 §2 · 6 §3 · 7 §4 · 8 §5 · 9 §6 · 10 §7 · 11 §8 · 12 §9 · 13 §10 · 14 §11 · 15 §12 · 16 §13 · 17 §14. Ölçülen kurallardan farklar ve kapsam §15.

## 1 · Amaç ve sınıf

B2 iki soruyu cevaplar:
- **Ben karıştırılıyor muyum?** Kendi durumum: yok · girişim (gönderebilirim, duyamam) · kanal kilidi (kanal hep dolu; ne gönderebilirim ne duyabilirim).
- **Hangi komşumla bağım karıştırılıyor?** Bağ başına iki kanıt: komşunun selamındaki bitle kendisi için söylediği (alıcının bildirimi) ve ona gönderdiğim verinin sonucundan çıkan (göndericinin kanıtı).

Karar vermez: bağın kullanılması, bırakılması ve geri dönüşü B3'ün; B1'in hariç aralık listesi B3'ün karıştırma ekinin (B1 kural 10); yol B4'ün (`18` §1.4 sözleşme 3).

- **Sınıf:** karıştırmaya karşı (K-247). Bütünü karıştırma katmanının bayrak grubuyla kapanır (§10) ve mekanizma kapısına girer (`06` §0.4.5).
- **Hizmet ettiği hedef** (`18` §1.1): ana hedef ve karıştırmaya özgülük. Birincilde yol seçimi ortalamayı belirlemiyor (beş yol seçimi 0,659–0,666); kaybın büyüğü karıştırılan bağda, iletimde (açık dönemde 0,267–0,335). Kâhin karıştırılan bağları bildiği için 0,779'a çıkıyor (`18` §2.2). Koruma ölçütlerinden ikizde zarar yok (yanlış alarm, §7), sessiz dönem (çıkış 1 s) ve kontrol payı (selamda 1 bit, §6) bu bileşene dokunur.

## 2 · Gördüğü (`05`; yasak alanlar okunmaz)

| gözlem | B2'nin kullandığı | kullanmadığı |
|---|---|---|
| `mesgul_sure_s` (`kanal_dolulugu_ister`; yalnız karıştırma katmanı açıkken) | son saniyedeki artışı: kanal meşgul payı `m` (kural 1) | — |
| `alinan_cerceve` | son saniyedeki artışı: çözülen çerçeve `c`, her türden (kural 1) | — |
| B1'in selam örnekleri ve `son_selam_t` | selam kaybı payı `s` (kural 3); ham örnekler, hariç aralıksız | sondaki sessizlik (B1 kural 16; Aşama 3'te kaldırıldı): sessizlik kuralları ikizde 1000 kullanılabilir bağ-saniyesinde 14–45 yanlış alarm verdi; E alanında 3 s içinde en çok 0,14 yakaladı (teşhis §4, seçim yarısı, `sonuc_hesap.txt`) |
| B1'in veri kayıtları (an, deneme, onay) | göndericinin kanıtı (kural 12) | `E_veri` ve vazgeçme payı (B3'ün) |
| B1'in komşu kümesi ve silinen komşu olayı | komşu kayıtlarının budanması | — |
| selam (`kontrol_alindi`; iletiyi B6 çözer) | gönderen, karıştırma biti (kural 10) | sıra, aralık, oranlar (B1'in) · maliyet (B4'ün) |
| `saat_s` | yalnız süreler | — |

**Okumadıkları:** `olculen_gurultu_w` (yasak, K-227) · RSSI: teşhis (d)'de zayıftı (AUC 0,71), hata modeli sınanmadı (K-233) · `phy_hata`: seçilen kurallara girmedi · `kanal_mesgul_mu`: anlık gösterge; meşgul payı sayaçtan okunur · `iletim_sonucu` doğrudan: veri sonucu B1'in kaydından okunur, aynı kayıt iki yerde tutulmaz (sözleşme 3) · `cerceve_duyuldu` · `kendi_konum`, `kendi_hiz` · kuyruk · `komsular`.

## 3 · Tuttuğu

Düğüm başına:

| alan | başlangıç | güncellenir | silinir | üst sınır |
|---|---|---|---|---|
| `onceki`: son saniye sonundaki `mesgul_sure_s`, `alinan_cerceve` ve an | ilk saniye sonu | her saniye sonu | — | — |
| `cbar_gecmis`: işaretsiz saniyelerin `c`'si | boş | her işaretsiz saniye (kural 4) | `CBAR_SANIYE`'yi aşınca en eskisi | `CBAR_SANIYE` |
| girişim sayımları: ardışık işaretli ve ardışık işaretsiz saniye | 0 · 0 | her saniye sonu (kural 6) | — | — |
| alt durumlar: kanal kilidi, girişim (var · yok) | yok · yok | her saniye sonu (kural 6) | — | — |
| `durum` (yok · girişim · kanal kilidi), `durum_t` (girildiği saniye sonu) | yok · ilk saniye sonu | her saniye sonu (kural 7) | — | — |
| kendi aralıklarım: [başlangıç, bitiş]; sürmekteki bitiş ∞ | boş | kural 8 | `KANIT_SAKLA`'yı aşınca en eskisi | `KANIT_SAKLA` |
| son işaretler: `m`, `c`, c̄, `s`, kanal kilidi ve girişim işareti | tanımsız | her saniye sonu | — | — |

Komşu j başına (B1'de kayıtlıyken):

| alan | başlangıç | güncellenir | silinir | üst sınır |
|---|---|---|---|---|
| `kb` (j'nin son selamındaki bit), `kb_t` (o selamın anı) | j'nin ilk selamı | her selamında (kural 10) | j silinince | — |
| bildirim aralıkları: [bitin 1 olduğu ilk selam, sonraki ilk 0'lı selam]; sürmekteki bitiş ∞ | boş | kural 10 | `KANIT_SAKLA`'yı aşınca en eskisi; j silinince | `KANIT_SAKLA` |
| göndericinin sayımı: ardışık tam denemeli kayıt sayısı, işlenen son kaydın anı | 0 · yok | kural 12 | j silinince | — |
| gönderici olayları (an) | boş | kural 12 | `KANIT_SAKLA`'yı aşınca en eskisi; j silinince | `KANIT_SAKLA` |

Kanca başına: "bit değişti" olayı (kural 9); bir sonraki kancanın başında boşalır.

**Bellek:** düğüm başına `CBAR_SANIYE` + `KANIT_SAKLA` + 255 × 2 × `KANIT_SAKLA` kayıt (komşu tablosu B1'inkidir, en çok 255).

## 4 · Durumlar ve geçişler

| döngü | durumlar | geçiş ve tetikleyici | çıkış |
|---|---|---|---|
| kanal kilidi alt durumu | yok · var | yok → var: kanal kilidi işaretli saniye · var → yok: işaretsiz saniye (kural 6) | iki yönde de bir saniyelik işarete bağlı; takılı kalma yok |
| girişim alt durumu | yok · var | yok → var: art arda `G_GIRIS` işaretli saniye · var → yok: art arda `G_CIKIS` işaretsiz saniye (kural 6) | aynı; işaretin sürmesi alımın bozuk sürmesidir (§8 "uzun süren durum") |
| kendi durumum | yok · girişim · kanal kilidi | alt durumlardan (kural 7); kanal kilidi öncelikli | alt durumlarınki |
| komşunun bildirimi | 0 · 1 | yalnız j'nin selamıyla (kural 10) | 1'den çıkış j'nin 0'lı selamı ya da j'nin silinmesi (`T_SILME`, B1 kural 3); takılı kalma yok |

Göndericinin kanıtı bir durum değil, zamanlı bir olaydır (kural 12). Ne kadar süre kanıt sayılacağı B3'ün kararıdır (§11 madde 2).

Önceki tasarımdaki üst süre (`KENDI_UST_SURE` 30 s, Y-6) yoktur. Kendi durumum bir dondurma değil, bir gözlemdir; bitmesi işaretlere bağlıdır (§8). Hariç aralığın üst süresi B3'ündür (§11 madde 2).

## 5 · Kurallar

**A · Saniyelik işaretler** (saniyelik zamanlayıcıda; bundan sonra "saniye sonu")

1. **Sayaçlar:** saniyelik zamanlayıcı her `TIK_S`'de bir dolar. İlk saniye sonunda sayaçlar yalnız okunur. Sonraki her saniye sonunda, önceki saniye sonundan beri geçen süre Δt ile:
   - `m` = Δ`mesgul_sure_s` / Δt, [0, 1] aralığına kırpılır;
   - `c` = Δ`alinan_cerceve` / Δt (çerçeve/s).

   Sayaçlardan biri azalmışsa (simülatörde olmaz) o saniye atlanır: işaret hesaplanmaz, sayımlar ilerlemez, c̄'ye girmez; yalnız sayaçlar yeniden okunur.
2. **Kanal kilidi işareti:** `m` ≥ `ED_ESIK`.
3. **Selam kaybı payı `s`:** tanıdık komşu, B1'de kayıtlı ve `son_selam_t` ≥ şimdi − `TANIDIK_S` olan komşudur. Tanıdık komşuların B1 selam örneklerinden anı (şimdi − `KAYIP_PENCERE_S`, şimdi] içinde olanlar sayılır: `s` = sıfırlar / bütün örnekler. Hiç örnek yoksa `s` tanımsızdır.
   - B1'in o anki ham örnekleri okunur: ileri sarmanın araya dağıttığı ve zaman aşımının eklediği sıfırlar dâhil, hariç aralık uygulanmaz.
   - Geri almanın sonradan sileceği sıfırlar o an sayılır; geçmiş saniyelerin işaretleri sonradan değişmez (B1 §11 madde 4).
4. **Kendi olağan düzeyim c̄:** son `CBAR_SANIYE` işaretsiz saniyenin `c` ortalaması; daha azsa olanların; hiç yoksa tanımsız.
   - İşaretsiz saniye: girişim işareti yok ve `m` < `CBAR_ED_ESIK`.
   - c̄ o saniyenin işaretinden önce okunur; saniye işaretsizse sonra geçmişe eklenir.
   - Sebep: karıştırılan saniyeler düzeyi aşağı çekmesin. Düzey karıştırma sürerken donar, ilk işaretsiz saniyede yeniden işler.
5. **Girişim işareti:** c̄ ve `s` tanımlıyken `c` < `G_ALFA` · c̄ **ve** `s` ≥ `G_BETA`.

**B · Kendi durumum**

6. **Alt durumlar:**
   - **kanal kilidi:** kanal kilidi işaretli saniyenin sonunda girilir, işaretsiz ilk saniyenin sonunda çıkılır;
   - **girişim:** art arda `G_GIRIS` işaretli saniye tamamlanınca girilir, art arda `G_CIKIS` işaretsiz saniye tamamlanınca çıkılır. Ardışık sayımlar kanal kilidi sürerken de işler.
7. **Durum:** kanal kilidi alt durumu varsa "kanal kilidi"; yoksa girişim alt durumu varsa "girişim"; ikisi de yoksa "yok".
   - Kanal kilidi önceliklidir. ED alanında girişim işaretinin iki koşulu da çoğu saniye sağlanır (E alanında çözülen çerçeve 6,2/s, selam kaybı 0,86; teşhis §1), ama düğüm gönderemez. Önceki tasarımda da öyleydi (KK-03 kural 4, Y-3).
   - Birleşimin yakalaması kuraldan sonra ölçüldü (teşhis §8.2): 3 s içinde E alanında 0,56–0,61, G alanında 0,36–0,39.
8. **Kendi aralıklarım:** durumun "yok" olmadığı her kesintisiz dönem bir aralıktır.
   - **Başlangıç:** girişe yol açan işaretli saniyelerin ilkinin başı; kanal kilidinde girişten 1 s, girişimde `G_GIRIS` s geriye. Sebep: o saniyeler bozulmanın başladığını zaten gösterir; karar onlardan sonra verilir. İki alt durum aynı saniye sonunda girerse erken olan başlangıç alınır.
   - **Bitiş:** durum "yok"a dönünce, son işaretli saniyenin sonu (`G_CIKIS` 1 iken çıkıştan 1 s geriye). Durum sürüyorsa bitiş ∞.
   - Önceki aralıkla çakışan ya da ona bitişik aralık onunla birleşir.
   - Aralıkları B3 okur: hariç aralık (B1 kural 10) ve göndericinin kanıtının geçerliliği (kural 13).
9. **Bit:** selamın karıştırma biti, durum "yok" değilse 1, "yok"sa 0.
   - Bit değişince "bit değişti" olayı oluşur (B6 için, Ö-2).
   - Kanal kilidi ile girişim arasındaki geçiş biti değiştirmez.
   - `alici_bildirimi` kapalıyken bit hep 0'dır ve olay oluşmaz.

**C · Komşunun bildirimi** (göndericide)

10. j'den selam gelince, B1 selamı işledikten sonra, bit `kb` ve an `kb_t` yazılır.
    - Bit 0'dan 1'e dönünce, ya da kaydın ilk selamının biti 1 ise, j için bir bildirim aralığı açılır: başlangıcı bu selamın anı, bitişi ∞.
    - Bit 1'den 0'a dönünce açık aralık bu selamın anıyla kapanır.
    - `alici_bildirimi` kapalıyken bit okunmaz; `kb` 0 kalır.
11. **Bildirim yalnız selamla değişir.** j susarsa son değer kalır: kanal kilidindeki j gönderemez, girişimdeki j'nin selamları da kaybolabilir; susmak bildirimin bittiğini göstermez. j silinince (B1'in silinen komşu olayı) j'nin bütün kayıtları gider.
    - Başlangıç geç kalır: j durumunu kendi kuralıyla bulur (girişim kuralı 3 s içinde %34–35) ve bit selamla, uzak bir komşuya selam başına 0,35 olasılıkla ulaşır (teşhis K6). Bildirim aralığı j'nin gerçek bozulmasından sonra başlar; hariç aralıkta bunun payını B3 belirler.

**D · Göndericinin kanıtı**

12. **Gönderici olayı:** j'ye giden veri kayıtları (B1 kural 8) zaman sırasıyla ve her biri bir kez işlenir. Ardışık sayım:
    - kaydın anı kendi aralıklarımdan birine düşüyorsa sayım sıfırlanır, kayıt sayılmaz;
    - deneme `GK_DENEME` ise (bütün denemeler harcandı: onay son denemede geldi ya da vazgeçildi) sayım bir artar;
    - değilse sayım sıfırlanır.

    Sayım `GK_ARDISIK`'e ulaştığı kayıtta olay oluşur; anı o kaydın anıdır. Sayım sürerken yeni olay oluşmaz; sayım kırılınca yeniden başlar. `gonderici_kaniti` kapalıyken olay oluşmaz.

    Kuralın seçimi (teşhis K3–K4, 27 kural): yanlış alarm sınırını (ikizde ve önce evresinde 1000 çerçevede 1) üç kural geçti. G alanındaki alıcıyı en erken yakalayan, art arda 3 çerçeve ve her biri 7 deneme (DEN7x3); doğrulamada ikizde 1000 çerçevede 0,40 yanlış alarm. Art arda 3 vazgeçme (VAZ3) bunun içindedir, çünkü vazgeçme 7 denemedir. Seçim yarısında E alanında ikisinin sayıları aynı (3 s içinde 0,205, dönem içinde 0,432); G alanında DEN7x3 daha erken (0,159 ↔ 0,141). Gönderici alıcının alanını bilmediği için iki alana tek kural uygulanır.
13. **Geçerlilik:** anı kendi aralıklarımdan birine düşen olay "kendimle açıklandı" sayılır ve çıktıda yer almaz.
    - Aralık geriye dönük açıldığı için (kural 8) bir olay, oluştuktan en çok `G_GIRIS` s sonra açıklanabilir.
    - Sebep: kendi alımım bozukken onayları duyamam; başarısızlık bütün komşularda görünür ve göndereni gösterir (önceki KK-03 kural 8; `17` T-6).
    - Teşhiste bu ayıklama yoktu (§15).

**E · Çıktılar** (okuma anında hesaplanır; hesap yalnız burada yapılır, sözleşme 3)

14. **Kendi durumum:** değeri, `durum_t` ve kendi aralıklarım.
15. **Bağ başına (komşu j):** bildirim (`kb`, `kb_t`) ve bildirim aralıkları; en yeni geçerli gönderici olayının anı (yoksa tanımsız) ve geçerli olayların sayısı.
16. **Bit ve olay:** selamın biti (kural 9) ve bu kancanın "bit değişti" olayı (B6 için).
17. **Son işaretler** (`m`, `c`, c̄, `s`, iki işaret): yalnız tanı içindir; hiçbir bileşenin kararına girmez.

**F · Sıra**

18. B2 her kancada B1'den sonra, B3'ten önce çalışır (`18` §1.4 olay sırası 1 ve 3):
    - selam gelen kancada, B1 selamı işledikten sonra kural 10;
    - saniye sonunda, B1 zaman olaylarını işledikten sonra (B1 kural 20) kural 1–9;
    - her niyetli kancada yeni veri kayıtları (kural 12) ve B1'in silinen komşu olayıyla budama.

    Saniye sonu ile bir selam aynı anda gelirse önce selamın gözlemi (B1, sonra kural 10), sonra saniye sonunun işleri. Aynı saniye sonunda önce kendi durumum (kural 6–9), sonra veri kayıtları (kural 12): kayıt, o saniye sonunda açılan aralığa göre değerlendirilir.

## 6 · İletiler

B2 kendisi ileti göndermez. Selamda bir alanı vardır; biçim ve gönderim B6'dadır (`18` §1.4 sözleşme 6). B6'dan beklediklerim (Aşama 2.6'da kapanır, bütünlük denetiminde denetlenir):

- **Ö-1** Selamda 1 bitlik karıştırma alanı bulunur; değeri kural 9'dandır, selam kurulurken okunur. İleti boyu ⌈Σ bit / 8⌉ + 64 bayt olduğundan (`18` §1.2 C) alan selamı en çok 1 bayt büyütür; ~100 baytlık selamda en çok %1.
- **Ö-2** "Bit değişti" olayında selam en kısa sürede gider; iki selam arasındaki en kısa süre (B1 Ö-4) korunur. Sebep: A'nın gerekçesi bitin doğduğu yerden hızlı gitmesidir (`18` §2.2). Girişimin çıkışı 1 s; komşuların bağı geri alması bu selamı bekler.
- **Ö-3** Durum sürdükçe bit her selamda gider. Uzak bir komşuya selam başına ulaşma payı 0,35 (teşhis K6); selamlar bağımsız sayılırsa 3 selamda ~0,72, 5 selamda ~0,88 (kestirim, teşhis §8.7). Durum sürerken aralığın kısaltılması B6'nın kararıdır; bedeli kontrol payıdır (en çok %10, `18` §1.1).
- **Ö-4** Kanal kilidinde kurulup kuyrukta bekleyen selam, kanal açılınca bayat bir bit taşıyabilir. Durum değiştiyse "bit değişti" olayı yeni bir selamla bunu düzeltir (Ö-2). Bayat içeriğin sakıncası B6'nın sorusudur (B1 Ö-5 ile aynı).
- **Ö-5** `alici_bildirimi` kapalıyken alan kalır ve 0 gider: boy aynıdır, ablasyon kontrol yükünü değiştirmez (önceki tasarımda da böyleydi, KK-00).

**Kontrol yüküne katkı:** alan (Ö-1) ve "bit değişti" selamları. Kaba kestirim: birincilde açık dönemde E ve G alanında ortalama ~8 düğüm var (0,9 + 6,8; `18` §2.2). Dönem başına iki değişimle 30 s'lik çevrimde ~16 ek selam olur; ağın kendi selamı saniyede ~20–80'dir (40 düğüm, 0,5–2 s aralık). Görüş hattının titremesi değişimi artırabilir (§8); tanıda sayılır (§13).

## 7 · Değerler

`TIK_S` · `ED_ESIK` · `G_ALFA` · `G_BETA` · `G_GIRIS` · `G_CIKIS` · `CBAR_SANIYE` · `CBAR_ED_ESIK` · `KAYIP_PENCERE_S` · `TANIDIK_S` · `GK_DENEME` · `GK_ARDISIK` · `KANIT_SAKLA`. Değeri, birimi, kaynağı, küçük ve büyük olursa ne olacağı ve taranıp taranmayacağı `00-DIZIN.md`'nin değer tablosunda.

**Ölçülen başarı** (teşhisin doğrulama yarısı, tohum 1007–1010; kurallar seçim yarısında, 1003–1006'da seçildi; iki değer birincil · dayanıklılık):

| kural | ikizde yanlış alarm | 3 s içinde yakalama, dönem başından | 3 s içinde yakalama, alana girişten (kuraldan sonra) |
|---|---|---|---|
| kanal kilidi (`m` ≥ 0,55) | düğüm-saniyelerin %0,007'si | 0,463 (iki hücre birlikte); bu birimle tavan da 0,463 (E8) | 0,95 · 0,90; ortanca 1 s (E7) |
| girişim G(0,4 · 0,6 · 2 · 1) | %0,002; açık dönemde uzak alanda %0,5–1,5 | 0,344 · 0,347; dönem içinde 0,530 · 0,545 | 0,375 · 0,392; ortanca 2 s (E7) |
| gönderici olayı (DEN7x3) | 1000 çerçevede 0,40 | G alanındaki alıcıda 0,184 · 0,213; E alanında en az VAZ3'ünki, 0,348 · 0,268 | ölçülemedi (alıcının kimliği kayda girmedi) |

## 8 · Kenar durumlar

- **Soğuk açılış:** ilk saniye sonunda yalnız sayaçlar okunur; kanal kilidi ikinci saniye sonundan itibaren çalışır. c̄ ilk işaretsiz saniyeyle tanımlanır, o zamana kadar girişim işareti çıkmaz. `s`, tanıdık komşu olunca tanımlanır. Karıştırma açılıştan beri sürüyorsa c̄ karıştırılan düzeyden kurulur ve girişim kendi ortalamasıyla tanınmaz; kanal kilidi mutlak eşikle tanınır. Bu tutucu yöndedir: yanlış alarm değil, kaçırma.
- **Geçit:** B2 geçitte de aynı çalışır. Geçidin biti "geçit duyamıyor" der, ama geçit hedeftir ve ondan kaçınılamaz. Karşılığı B3'ün kararıdır (B3 kural 8; §11 madde 2).
- **Hiç komşu yok:** `s` tanımsız, girişim işareti çıkmaz; kanal kilidi çalışır. **Tek komşu:** `s` bir komşunun 4 s'deki örneklerinden (2–8 örnek) gelir ve gürültülüdür; girişim için `c`'nin de düşmesi gerekir.
- **Düğüm kendisi karıştırılırken:** kural 6–9 bunun içindir. Kanal kilidinde gönderemem: bit kuyrukta bekler (Ö-4), veri kaydı oluşmaz, göndericinin kanıtı üretilmez. Girişimde gönderebilirim, ama onayları duyamadığım için komşulara giden kayıtlar tam denemeli olur; kural 12–13 bunları kendi aralığımla ayıklar.
- **Komşu karıştırılırken:** girişimdeki komşu bitini gönderebilir. Kanal kilidindeki komşu gönderemez: onu göndericinin kanıtı (kural 12) ve B1'in ölçüsü gösterir, biti ancak kilit kalkınca gelir.
- **Uzun süren durum:** üst süre yoktur. Durumdan bir işaretsiz saniyede çıkılır; durumun sürmesi her saniye `c` < 0,4 · c̄ ve `s` ≥ 0,6 demektir, yani alım gerçekten bozuktur ve bit doğrudur. Düğüm sürüden uzaklaştığı için `c` düşer ve tanıdık komşuların selamları kaybolursa, o komşular `TANIDIK_S` sonra tanıdık olmaktan çıkar ve `s` kalan komşulardan ölçülür; durum en geç böyle biter.
- **Görüş hattının titremesi:** düğümün alanı aynı açık dönem içinde değişebilir (ardışık iki saniye arasında birincilde ve dayanıklılıkta %3,3–3,4, cephe hattında %7,8; teşhis §8.1, §8.6). Kanal kilidinin 1 s'lik girişi ve çıkışı ile girişimin 1 s'lik çıkışı bunu izler. Her değişim bir "bit değişti" olayıdır; sıklığı B6'nın en kısa selam aralığıyla sınırlıdır.
- **Sayaç azalması:** kural 1 (simülatörde olmaz).
- **Zaman aşımı:** B2'nin kendi zaman aşımı yoktur; komşu kayıtları B1'in silmesiyle (`T_SILME`) gider.
- **Aynı anda gelen olaylar:** kural 18.
- **Tamponun dolması:** B2'nin tamponu yoktur; listelerin sınırı §3'te, dolunca en eskisi atılır.

## 9 · Arayüz

**Kancalar:**

| kanca | B2'ye giden | B2'nin işi |
|---|---|---|
| saniyelik zamanlayıcı | `mesgul_sure_s`, `alinan_cerceve`, şimdi | kural 1–9, sonra 12 |
| kontrol iletisi alındı, selam | gönderen, karıştırma biti | kural 10, sonra 12 |
| öteki niyetli kancalar (uyandırma, iletim başarısız, sonraki atlama) | — | kural 12; budama |
| iletim sonucu, çerçeve duyuldu (niyetsiz) | — (veri kaydı B1'de oluşur) | — (bir sonraki niyetli kancada kural 12) |

**Okuduğu:** yalnız B1: komşu kümesi ve olayları, selam örnekleri, `son_selam_t`, veri kayıtları (sözleşme 1).

**Çıktılar ve okuyanlar:**

| çıktı | kural | okuyan |
|---|---|---|
| kendi durumum, `durum_t` | 7, 14 | B4 (kural 14), B6 (kilit kuralı, B6 kural 11) |
| kendi aralıklarım | 8, 14 | B3 (hariç aralık, B1 kural 10), B4 (ilanın yaşı, B4 kural 4) |
| bağ başına bildirim ve bildirim aralıkları | 10–11, 15 | B3 |
| bağ başına geçerli gönderici olayı | 12–13, 15 | B3 |
| selamın biti, "bit değişti" olayı | 9, 16 | B6 |
| son işaretler | 17 | yalnız tanı |

**Olay sırası** (`18` §1.4): B1'in zaman olayları (adım 1) ve gözlemin dağıtımı (adım 2) B1'le başlar; B2'nin işi adım 3'tedir, B3'ten önce. Niyet döndüremeyen kancalarda B2 çalışmaz; işi bir sonraki niyetli kancada yapılır.

## 10 · Kapalıyken davranış

- **`karistirma_katmani` kapalı** (B2'nin bütünü; B3'ün karıştırma eki, B4'ün ve B6'nın kendi karıştırılmam kuralları da kapanır): B2 çalışmaz ve `kanal_dolulugu_ister` denmez. Kendi durumum hep "yok"tur; aralık ve kanıt yoktur; bit hep 0 gider (alan kalır); olay oluşmaz. B1'in hariç aralık listesi boştur (B1 §10). Kalan protokol eksiksiz çalışır: çekirdek bu koldur (`18` §1.4).
- **`alici_bildirimi` kapalı:** bit hep 0 gider, alınan bit okunmaz, "bit değişti" olayı oluşmaz. Kendi durumum ve aralıklar sürer (hariç aralık ve kural 13). A, B olur (`18` §2.2); bitin katkısı Aşama 4'te bu bayrakla ölçülür.
- **`gonderici_kaniti` kapalı:** gönderici olayı oluşmaz.

Grup kapalıyken alt bayraklar etkisizdir. Mekanizma kapısının "hepsi kapalı" kolu grubu kapatır (`06` §0.4.5).

## 11 · Etkileşimler

1. **B1 ile:**
   - B2, B1'in ham selam örneklerini okur (kural 3); B1'i değiştirmez ve dondurmaz.
   - Kendi aralıklarım B3 üzerinden B1'in hariç aralık listesine girer (B1 kural 10). Böylece kendi karıştırılmamdaki selam sıfırları ve tam denemeli kayıtlar bağın ölçüsüne girmez.
   - B1'in sondaki sessizliği (kural 16) B2'de kullanılmıyordu (§2); başka kullanan da çıkmadı, Aşama 3'te kaldırıldı (`01-BUTUNLUK.md` §11).
   - B1'in geri alması, kanal kilidindeki komşunun sıfırlarını selamı dönünce siler. B2 onları o saniyelerde sayar (kural 3); geçmiş saniyelerin işaretleri değişmez.
2. **B3'e kalanlar** (B2 kanıtı verir, kararı B3 verir):
   - bildirime ve gönderici olayına göre bağın durumu; olayın ne kadar süre kanıt sayılacağı; geri dönüşün koşulu (İlke 3: kanıt kalkınca geri al; girişimin çıkışı 1 s);
   - bir olayın, oluştuktan en çok `G_GIRIS` s sonra kendi aralığımla geçersizleşebileceği (kural 13);
   - hariç aralıkların payı ve üst süresi. Bildirim aralığının başlangıcı geç kalır (kural 11); B1'in saklaması 30 s'lik hariç aralığa göre hesaplandı (`SELAM_SAKLA`);
   - geçidin biti: hedeften kaçınılamaz (§8);
   - bir bağa gönderilmeyince o bağda yeni veri kaydı ve gönderici olayı oluşmaz; dönüşün bilgisi selamdan (bit 0) gelir. "Veri yok" kötü değildir (B1 §11 madde 5).
3. **B4, B5 ve B6:** kendi durumum B4'e (kendi karıştırılmamda istek gitmez, B4 kural 14) ve B6'ya (kanal kilidinde selam kurulmaz, B6 kural 11) gider. B5'in karıştırma eki yok (`18` §2.5); B5 kendi durumumu okumaz.
4. **B6:** Ö-1…Ö-5.
5. **Kendini besleme:** bitim 1 iken komşular bana daha az veri gönderir, `c` biraz daha düşer. Çıkış `c`'nin bütün çözülen çerçevelerle (selam, onay, başkasına giden veri) toparlanmasına ve `s`'ye dayanır. Ölçülen çıkış ortancası 1 s, ama teşhiste biti okuyan bileşen yoktu (§15); etkisi Aşama 4'te ölçülür.
6. **Kalabalık** (önceki KK-03 kural 12'nin riski): temiz kanalda da selam kaybı yüksektir (ikizde `s`'nin ortalaması 0,46). Kural selam kaybını `c` düşüşüyle birlikte arayarak tıkanıklıktan ayırır: ikizde yanlış alarm 86 400 düğüm-saniyenin 2'si, ikisi de en az yüklü üçte birde (teşhis K5). Yük koruması gerekmedi.
7. **Kanıtı silmeme** (sözleşme 4): B2 hiçbir bileşenin gözlemini silmez. Kendi aralığımla açıklanan olaylar B2'nin kaydında kalır, yalnız çıktıda geçerli sayılmaz. B2'ye dayanan kararların (B3, B4, B6) kanıtı nasıl etkilediği madde 2'de.
8. **Trafik:** işaretler bugünkü çekirdeğin trafiğinde ölçüldü. B4–B6'nın kararları trafiği değiştirebilir (ör. selam aralığı `s`'nin örnek sayısını değiştirir). Eşikler başlangıçtır; Aşama 4'te yeniden bakılır.

## 12 · Örnek senaryo

Düzeyler teşhisten: ikizde `c`'nin ortalaması 71,4/s; birincilde G alanında 38,3/s, `s` 0,73 (teşhis §1). Her düğümün saniye sonları kendi fazındadır.

1. **Girişime giriş:** i'nin saniye sonları 149,4 · 150,4 · 151,4 · … s. Karıştırıcıdan önce c̄ = 70, eşik 0,4 × 70 = 28. Karıştırıcı 150,0 s'de açılır; i G alanındadır.
   - (149,4–150,4]: `c` 52, `s` 0,48 → işaretsiz (`c` ≥ 28).
   - (150,4–151,4]: `c` 25, `s` 0,55 → işaretsiz (`s` < 0,6).
   - (151,4–152,4]: `c` 23, `s` 0,66 → girişim işareti, 1.
   - (152,4–153,4]: `c` 21, `s` 0,74 → işaret, 2 → 153,4'te durum "girişim", aralık [151,4, ∞), bit 1, "bit değişti".
   - B6 selamı hemen gönderir; durum sürdükçe her selamda bit 1 gider. Karıştırmanın başından karara 3,4 s geçti.
2. **Komşunun gördüğü:** k, i'ye veri gönderir; k uzak alandadır, kendi durumu "yok".
   - k'nin i'ye kayıtları: 152,1 s'de 7 deneme (vazgeçme) · 152,9 s'de 7 · 153,6 s'de 7 → üçüncüsünde gönderici olayı (153,6 s).
   - i'nin ilk selamı k'ye ulaşmaz; ikincisi 155,1 s'de gelir: `kb` = 1, bildirim aralığı [155,1, ∞).
   - B3 bu iki kanıtla i'ye giden bağı karıştırılıyor sayabilir; karar B3'ündür.
3. **i'nin kendi gönderimi:** i'nin ardılı j alanın dışındadır. i'nin çerçeveleri j'ye ulaşır, ama i onayları duyamaz; j'ye giden kayıtlar 151,6 · 152,1 · 152,8 s'de tam denemelidir. 152,9 s'de gelen bir selamın kancasında B2 kayıtları işler: sayım 3'e ulaşır, olay oluşur (152,8 s). 153,4'te aralık [151,4, ∞) açılınca olay kendimle açıklanır (kural 13): B3 onu yalnız 152,9–153,4 arasında gördü.
4. **Çıkış:** karıştırıcı 165,0 s'de kapanır.
   - (164,4–165,4]: `c` 46 ≥ 28 → işaretsiz → 165,4'te durum "yok"; aralık [151,4, 164,4]; bit 0, "bit değişti", selam hemen gider.
   - k bu selamı 165,9 s'de alır: `kb` = 0, bildirim aralığı [155,1, 165,9].
5. **Kanal kilidi** (teşhisteki örnek, §8.1: birincil, tohum 1003, düğüm 32): karıştırıcı 180,0 s'den beri açıktır, İHA saniyede ~4 m alçalır. 183,2 s'de görüş hattı açılır; karıştırıcının gücü −88,7'den −67,7 dBm'e, meşgul payı 0,33'ten 0,94'e çıkar.
   - Düğümün saniye sonları 182,7 · 183,7 · … olsun. (182,7–183,7] saniyesinin yarısı kilitlidir: `m` ≈ 0,5 × 0,33 + 0,5 × 0,94 ≈ 0,64 ≥ 0,55 → 183,7'de "kanal kilidi", aralık [182,7, ∞).
   - Düğüm gönderemez; bit 1 kuyrukta bekler (Ö-4). Ona veri gönderen komşuların kayıtları vazgeçmeyle dolar; art arda üçüncüde gönderici olayı oluşur.
   - Görüş hattı kapanınca meşgul payı düşer: ilk işaretsiz saniyenin sonunda kanal kilidinden çıkılır. Girişim alt durumu sürüyorsa durum "girişim" olur, bit 1 kalır ve ilk giden selam bunu bildirir.

## 13 · Sınanması

**Birim testleri** (Aşama 4):

1. Sayaçlar: ilk saniye sonu yalnız okur; `m` ve `c` farktan, Δt'ye bölünerek hesaplanır; `m` [0, 1]'e kırpılır; azalan sayaçta saniye atlanır.
2. `s`: tanıdık komşunun `TANIDIK_S` sınırı; pencere (şimdi − 4 s, şimdi]; ileri sarma ve zaman aşımı sıfırları dâhil; örnek yokken tanımsız; silinen komşu sayılmaz.
3. c̄: yalnız işaretsiz saniyeler (girişim işareti yok ve `m` < `CBAR_ED_ESIK`); `CBAR_SANIYE` sınırı; daha azsa olanların ortalaması; hiç yokken tanımsız ve girişim işareti yok; saniye işaretten önce okunur.
4. Girişim işaretinin sınırları: `c` = 0,4 · c̄ işaret değil; `s` = 0,6 işaret.
5. Kanal kilidi: `m` = 0,55 işaret; 1 s giriş ve çıkış.
6. Girişim alt durumu: 2 ardışık işaretli saniyede giriş, 1 işaretsiz saniyede çıkış; kanal kilidi sürerken sayımlar işler.
7. Öncelik: ikisi birlikte kanal kilidi; kanal kilidi bitip girişim sürerse girişim, bit değişmez.
8. Aralıklar: başlangıç geriye dönük (kanal kilidinde 1 s, girişimde `G_GIRIS` s); bitiş son işaretli saniyenin sonu; sürerken ∞; birleşme; `KANIT_SAKLA`.
9. Bit ve olay: yalnız "yok" ile ("girişim" ya da "kanal kilidi") arasındaki değişimde; `alici_bildirimi` kapalıyken bit hep 0, olay yok.
10. Bildirim: aralığın açılması (ilk selamı 1 olan kayıt dâhil) ve kapanması; susmakla değişmez; silinmeyle gider; bayrak kapalıyken okunmaz.
11. Gönderici olayı: üçüncü tam denemeli kayıtta bir kez; sayım sürerken yeni olay yok; denemesi 7'den az kayıtta sıfırlanma; kendi aralığımdaki kayıtta sıfırlanma; her kayıt bir kez; bayrak kapalıyken olay yok.
12. Geçerlilik: sonradan, geriye dönük açılan aralığa düşen olay çıktıdan düşer; ondan önceki geçerli olay görünür.
13. Grup kapalı: hiçbir kural çalışmaz, `kanal_dolulugu_ister` denmez, bit 0, çıktılar boş.
14. Sıra (kural 18): aynı saniye sonunda önce durum, sonra kayıtlar; selam ile saniye sonu aynı anda.
15. Bellek sınırları aşılmaz.
16. Örnek senaryonun (§12) sayıları uçtan uca.
17. **Ölçülen kuralla eşdeğerlik:** teşhisin kayıtlarındaki saniyelik `m`, `c`, `s` dizileri (`kayit_*.json`) B2'nin saf işlevlerinden geçirilince kanal kilidi ve girişim alt durumları `isaret.py`'ninkiyle aynı çıkar (aynı saniye sınırlarıyla).

**Ölçümde sayılacak tanı** (Aşama 4):
- kendi durumum: temiz sınıflarda (ikiz, önce, sessiz, uzak) yanlış alarm; alana girişten ve dönem başından yakalama ve gecikme; çıkış gecikmesi; açık dönem başına geçiş sayısı (önceki tasarımda S-4);
- bit: değişim sayısı, "bit değişti" selamları ve kontrol payına etkisi, bitin komşulara ulaşma süresi;
- gönderici olayı: sayısı, temiz sınıfta 1000 çerçevede kaç olduğu, kendi aralığımla açıklananlar;
- kendi aralıklarımın ve bildirim aralıklarının süre dağılımı.

## 14 · Kaynak

- **Kanal meşguliyetiyle tanıma; elle konan eşiklerin tıkanıklıkta yanılması; komşularla birleştirmenin doğruluğu artırması:** Puñal vd. 2014 [23]. Kanal doluluğu tepkisel karıştırıcıyı görmez [23].
- **Teslim oranının tıkanıklığı karıştırmadan ayırması ama kötü bağdan ayıramaması:** Xu vd. 2005 [66] ↪ (özet; özgün metin açılmadı). Girişim kuralının çözülen çerçeve düşüşünü selam kaybıyla birlikte araması bu uyarıya karşılıktır.
- **Karıştırılan düğümün komşularına haber vermesi:** JAM, Wood, Stankovic, Son 2003 ↪ (`protokol_kaynaklari/faz5_3_arastirma_2026-11-19/NOTLAR.md` §4; kaynakçaya girmedi). JAM karıştırılan bölgeyi haritalar; burada yalnız selamda bir bit vardır.
- **Önceki tasarım** (`../kural/KK-03`): kendi ortalamasına göre düşüş ve selam kaybıyla girişim kuralının biçimi; kanal kilidinin önceliği (Y-3); kendi karıştırılmamda MAC sonucunun bağ kanıtı sayılmaması (kural 8); bayrak kapalıyken alanın kalması.
- **Bu tasarımın:**
  - eşiklerin 295 kurallık ızgaradan, seçim ve doğrulama yarılarıyla seçilmesi (teşhis);
  - göndericinin kanıtının 27 kural arasından ölçümle seçilmesi (DEN7x3) ve kendi aralığımla geriye dönük ayıklanması;
  - kendi aralıklarımın geriye dönük başlangıcı ve hariç aralık olarak B1'e gitmesi;
  - kanıtın karar olmadan, zamanlı olarak verilmesi (bildirim aralıkları, olaylar).

## 15 · Ölçümden kâğıda: farklar ve kapsam

**Ölçülen kurallardan farklar** (Aşama 4'te kâğıdın kuralı ölçülür):

1. **Saniyeler:** teşhiste simülasyon saatinin tam saniyeleri kullanıldı. Protokolde periyodik zamanlayıcının saniyeleri vardır; düğüm başına rastgele bir fazla kayıktır (`sim2/kosum/kontrol.py`, `zamanlayicilari_kur`). Pencere boyu aynıdır.
2. **B1'in silmesi:** teşhiste yalnız selamlardan yaklaşıklandı (teşhis beklentisi, "Sınırlar"); B1'de her çerçeve kaydı tazeler. `s` değişmez, çünkü tanıdık olmak gerçek selama bağlıdır.
3. **Birleşim ve öncelik:** iki kural teşhiste ayrı ölçüldü; birleşimin yakalaması kuraldan sonra hesaplandı (teşhis §8.2). Birleşimin yanlış alarmı ikisinin toplamını aşmaz (ikizde %0,007 + %0,002).
4. **Göndericinin kanıtında kendi aralığım:** teşhiste yoktu, bütün kayıtlar sayıldı. Ayıklama yanlış alarmı azaltır; gönderici de karıştırılıyorsa yakalamayı azaltır.
5. **Kanal kilidi kuralı:** K1'in hükmü önceden yazılı birimle "tutmaz"dır ve öyle kalır (teşhis §2). 25 Kasım kararım: kural (`m` ≥ 0,55) yine de alındı. Dayanak sonuçtan sonra ölçüldü:
   - K1'in birimi gecikmeyi dönem başından sayıyor. Yer–hava görüş hattı aynı dönem içinde açılıp kapandığı için E birimlerinin yarısından fazlası alana dönemin 3. saniyesinden sonra giriyor. Bu birimle hiçbir kanal kilidi kuralı 0,80'e ulaşamazdı: ulaşılabilecek en yüksek pay doğrulamada 0,463, kuralınki de 0,463 (`ek_hesap.txt` E8).
   - Alana girişten sayınca kural birincilde %95'ini, dayanıklılıkta %90'ını 3 s içinde yakalıyor; gecikme ortancası 1 s (E7).
   - Teşhis (d)'de aynı işaret, Babel'in trafiğinde, güçlüydü.
   - Yanlış alarm koşulu doğrulamada geçti (%0,007; sınır %0,1).

   Seçilmeyenler: önceden yazılı sonuca uyup başka işaret aramak aynı tavana takılırdı; kanal kilidi durumunu kaldırmak iyi çalışan bir işareti atardı. Karar `v2/06` §10'a "sonuçtan sonra" diye yazıldı; kuralın katkısı Aşama 4'te ablasyonla ölçülür.
6. **Bit:** teşhiste biti okuyan bileşen yoktu; yalnız selamın ulaşma payı ölçüldü (K6). Bitin etkisi ve kendini besleme (§11 madde 5) Aşama 4'te ölçülür.

**Kapsam:**
- Yalnız sürekli karıştırıcı ölçüldü (`derin_sizma`, `cephe_hatti`). Darbeli, tepkisel, aldatıcı ve taramalı sınıflar ölçülmedi; kanal doluluğu tepkisel karıştırıcıyı görmez [23].
- **Cephe hattı** (teşhis K7, §8.6): girişim kuralı orada zayıf (3 s içinde 0,133 ↔ birincilde 0,341); G alanındaki alıcı için göndericinin kanıtı da öyle (0,046 ↔ 0,171). Üç sabit yer karıştırıcısının çevresinde G alanı görüş hattıyla titriyor. Bu bir kapsam sınırıdır. Eşikler cephe hattıyla yeniden seçilmedi: cephe hattı genellemenin denetimiydi, seçime girerse denetim olmaktan çıkar. Yer karıştırıcılı aile Aşama 4'te ölçülür (`18` §1.2 E).
- Hareketli kollar (bağımsız, görev) ölçülmedi.
- Kanal kilidindeki alıcı göndericide geç tanınır: bit gönderemez, göndericinin kanıtı 3 s içinde %27–35.
- Bit komşuya selam başına 0,35 olasılıkla ulaşır; birkaç selam ister (Ö-3).
- Eşikler bugünkü çekirdeğin trafiğinde ölçüldü (§11 madde 8).
