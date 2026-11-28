# Yeni DESPARETE tasarımı — bağımsız denetim raporu (28 Kasım 2026)

## 0 · Başlık bilgisi

- **İstem:** depo kökündeki `DENETIM-PROMPT.md` (arşiv kopyası `arsiv/denetim/DENETIM-PROMPT-TASARIM-2026-11-28.md`).
- **Denetlenen hâl:** `main` @ `a305643e9aa6233e708a9d81d398f7c4ac36f300`. Tasarım belgeleri `3a71a0b`'deki hâliyle: `git diff --stat 3a71a0b -- v2/18-YENI-TASARIM.md v2/bilesen` boş.
- **Başlangıç durumu:** `git rev-parse HEAD` → `a305643e9aa6233e708a9d81d398f7c4ac36f300` · `git status --short` → boş.
- **Son durum:** `git rev-parse HEAD` → `a305643e9aa6233e708a9d81d398f7c4ac36f300` · `git status --short` → `?? arsiv/denetim/DENETIM-RAPORU-TASARIM-2026-11-28.md` (yalnız bu rapor).
- **Çalışma ağacına dair not:** kayıtları okuyan betikler teşhis klasörlerinin modüllerini içe aktardı; `-I` bayrağı `PYTHONDONTWRITEBYTECODE`'u yok saydığı için üç klasörde `__pycache__` oluştu (`faz5_3_b2_isaretler_2026-11-24`, `faz5_3_b3_bag_olculeri_2026-11-25`, `faz5_3_b5_iletim_kaybi_2026-11-26`; git bunları yok sayar). Üçü de bu oturumda oluşmuştu ve silindi; ağaç başlangıçtaki hâline döndü. Ek A'daki betikler bunu `sys.dont_write_bytecode = True` ile önler.
- **Okunan tasarım belgeleri:** `v2/18-YENI-TASARIM.md` (tamamı) · `v2/bilesen/00-DIZIN.md` · `01-BUTUNLUK.md` · `B1`…`B7` (tamamı) · `arsiv/denetim/DENETIM-RAPORU-KURAL-2026-11-17.md` · `DENETIM-KURAL-KAPANIS-2026-11-17.md` · `v2/kural/KK-00-DIZIN.md` (genel kural 4) · `v2/kural/KK-02-SELAM.md` (kural 3) · `v2/13-KONTROL-DUZLEMI.md` §02–03 · `v2/05-GOZLEM-PENCERESI.md` §2–3 · `v2/06-ON-KAYIT.md` (ölçü satırları).
- **Okunan kod:** `sim2/gozlem/protokol.py` · `pencere.py` · `karar.py` · `kontrol.py` · `sim2/kosum/kontrol.py` · `kontrol_durum.py` · `kosu.py` · `gonderim.py` · `teslim.py` · `alim.py` · `dugum.py` (gözlem, tampon, kancalar) · `sim2/cekirdek/olaylar.py` · `sim2/kanal/dunya.py` · `sim2/yapilandirma/konfig.py` (ilgili alanlar) · `sim2/ag/trafik.py` (`kaynak_sira`) · `protokoller/babel.py` (uygulanabilirlik, istekler, seçim, beyanlar) · `babel_bicim.py` · `protokoller/desparete5.py` · `desparete5_egim.py` · `desparete5_rota.py` (sayaçlar).
- **Birincil kaynak:** `protokol_kaynaklari/rfc8966_babel.txt`: §2.4, §3.2.7, §3.4.1, §3.5–§3.8 (bütün alt bölümler), §4.6.5, Ek A.1–A.3, Ek B.
- **Teşhis kayıtları ve hesapları:** B2 `sonuc.md` · `isaret.py` · `kayit_birincil.json` · `kayit_dayaniklilik.json` · B3 `sonuc.md` · `ek_hesap.txt` · B5 `sonuc.md` · `ek_hesap.txt` · `olcum.py` · `sonuc_hesap.py` · `ek_hesap.py` · `kayit_birincil.json.gz` · B6 `kontrol_bedeli.txt` · B7 `bekletme_komut.txt` · bütünlük `butunluk_hesap.txt` · döngü kuralları `sonuc.md` · `sonuc_hesap.py` · yeni çekirdek `kayit_egim0_ikiz.json` · `kayit_egim0_birincil.json` · `kayit_cekirdek_birincil.json`.
- **Yöntem:** okuma ve kaynakla karşılaştırma; kuralların adım adım yürütülmesi; karşı örnek kurma; var olan kayıtlardan depo dışında küçük betiklerle yeniden hesap (Ek A; simülasyon koşulmadı, tohum kullanılmadı). Kayıtlar bugünkü kodun `eğim0` kolunun trafiğidir; yeni tasarımın durumu değildir. Bu yüzden kayıtlardan çıkan sayılar büyüklük göstergesidir, yeni tasarımın ölçümü değildir.
- **Hüküm özeti:** tasarım bu hâliyle dondurulmaya ve kodlanmaya hazır değil. Bir engelleyici bulgu var: B4 kural 10a'nın sınıf dalı isteği çoğunlukla düğümün kendi alt ağacına gönderiyor ve her tur benimsenişinde yeniden kuruluyor; karıştırma altında art arda tur artışı doğurabiliyor. Beş önemli ve altı küçük bulgu var. Hepsi belge düzeyinde düzeltilebilir; simülasyon gerekmez. Mekanizma kapısının ölçülmüş payı, alt ağaç hedefleri çıkarılınca ~0,03'ten ~0,02'ye iniyor.

---

## 1 · Bulgular

Ağırlık sırasıyla. **Engelleyici:** kod yazılmadan düzelmeli · **önemli:** kodlamadan önce bir karar ya da açık kural gerekir · **küçük:** kodla birlikte düzeltilebilir.

### E-1 · B4 kural 10a'nın sınıf dalı: istek çoğunlukla kendi alt ağacıma gidiyor ve her tur benimsenişinde yeniden kuruluyor; tur art arda artıyor — **engelleyici**

- **Yer:** `v2/bilesen/B4-YOL.md:133–141` (kural 10a) · `:203` (§6: "en çok `YOK_SAYMA_S`'de bir gider") · `:273` (§11 madde 8) · `v2/bilesen/01-BUTUNLUK.md:46` (§2: "10a seyrek … ~0") · `:258` (§10: 0,014) · `v2/18-YENI-TASARIM.md:555` (§2.4 eki: 0,038) · `:621` (§2.5'in bedeli).
- **Ne yanlış:**
  1. **Hedef.** Sınıf dalı ("j O'da, ardıl S'de") hiçbir maliyet koşulu istemez. Ardılım S'deyken ve olağan aday yokken, ilanı sonlu, taze ve uygulanamaz her olağan komşu "tercih edilir" sayılır. Kendi alt ağacımdaki komşular (yolu benden geçenler) bu tanıma tam uyar: ilanları benimkinden türediği için FD'mi geçemez. Yeni tur onları aday yapamaz. Benim yeni turlu ilanım onlara ulaşmadan onların ilanı yeni turu taşımaz; ulaştıktan sonra benim FD'm de yeni turla güncellenmiştir ve ilanları yine uygulanamazdır. RFC 8966 §3.8.2.2'nin ikinci paragrafı ve babeld bunu metrikle dışlar: alt ağaçtaki komşunun metriği seçili rotamınkinden büyüktür, "preferable" olamaz (`rfc8966_babel.txt:1443–1448`; `protokoller/babel.py:374–390`; `babel_bicim.py:148–150`). B4'ün "önce sınıfa bakılır" uyarlaması (`B4-YOL.md:140`) bu dolaylı korumayı kaldırıyor.
  2. **Bekleme.** Bekleme yalnız "istenen turu aynı ya da daha büyük" bir isteği engelliyor (`:137`). İstenen tur FD.tur + 1'dir. FD, yeni turlu ilan "ilan için verildiği anda" güncellenir (kural 9). Kural 10a aynı kancada, seçim ve FD'den sonra çalışır (kural 16'nın sırası: 5 → 6 → 8). Yeni tur benimsendiği kancada koşul sürüyorsa (ardıl S, olağan aday yok, alt ağaçtaki komşu hâlâ eski turlu ilanla) bir sonraki tur hemen istenir ve bekleme onu engellemez. §6'nın ve `01-BUTUNLUK` §2'nin "en çok `YOK_SAYMA_S`'de bir" ve "seyrek" sözleri kuralın metniyle çelişiyor.
  3. **İstek ölmüyor.** Alt ağaçtaki komşu c isteği kendi ardılına (bana, isteyen g) gönderemez. Kural 12 onu c'nin başka bir adayına, yoksa uygulanamaz bir komşusuna iletir (`:152`). c'nin benden geçmeyen bir adayı varsa ya da istek başka bir dala çıkarsa, istek geçide ulaşır ve tur artar.
- **Karşı örnek** (adım adım; maliyetler ETX):
  - Bağlar: G–j 1,0 · j–i 1,0 · i–c 1,0 · c–x 1,6 · x–G 1,5. x, i'nin komşusu değil.
  - Durgun: C_j = 1,0. C_i = 2,0 (ardıl j), FD_i = (T, 2,0). c'nin adayları i (m 3,0) ve x (m 3,1); ardılı i, C_c = 3,0. C_x = 1,5.
  - j girişime girer ve biti i'ye ulaşır: j S olur (B3 kural 5). i'nin olağan adayı yok, çünkü c'nin ilanı 3,0 ≥ 2,0. Kural 10a: c olağan, ilanı taze, sonlu ve uygulanamaz, sınıfı ardıldan iyi → c'ye istek (T+1).
  - c'nin turu T < T+1. c isteği ardılına (i = g) gönderemez, x'e iletir (kural 12). x geçide iletir. Geçit T+1 olur ve ilan eder.
  - Yeni tur G → j → i yolundan döner; her düğümde tur değişimi olaydır (B6 kural 7, Ö-1). i, j'nin (T+1, 1,0) ilanını kabul eder (yeni tur); j hâlâ S; FD_i ← (T+1, 2,0).
  - Aynı kancada kural 10a: c'nin i'deki ilanı hâlâ (T, 3,0); FD_i'ye göre eski turlu, uygulanamaz; c olağan → istek T+2. Bekleme son isteği (T+1) görür ama T+2'yi engellemez.
  - c yine x'e iletir, geçit T+2 olur. Döngü j'nin bildirimi sürdükçe (girişim dönemi boyunca) yinelenir.

  Hiçbir adımda c, i'nin adayı olmaz; istekler yalnız turu artırır. Her artışta ağdaki her düğümün ilan ettiği tur değişir.
- **Kayıtlardan büyüklük** (B5 teşhisinin karar satırları; Ek A.1–A.2; yol, her düğümün t'den önceki son telemetri kararının ardılıyla, 2 s tazelikle izlendi):
  - E8'in a2 payı (ardılın kanıtı var, olağan aday yok; 0,0383, yeniden üretildi): **0,0274'ünde (%72) temiz engelli komşunun o andaki yolu kararı veren düğümden geçiyor**; 0,0022'sinde yol izlenemedi. Karar olarak 1 103'ün 788'i.
  - Aynı payın katman kanıtlı kısmı (0,0143, yeniden üretildi): 0,0109'u (%76) alt ağaçta.
  - K6'nın 0,1364'ü (yeniden üretildi): 0,0829'u (%61) alt ağaçta.
  - Sınıf dalının koşulu birincilde koşu başına 244 kararda (25–644) sağlanıyor; bunların %58'inde hedef alt ağaçta. Düğüm başına ayrık bölüm koşu başına 21 (7–50), 13 düğümde. İkizde 4 bölüm.
  - Bugün (`eğim0`, kural 10a yok) koşu başına tur artışı 26 (ikiz) · 33 (birincil) (`rota.tur_artirildi`; Ek A.4).
- **Etkileri:**
  - `18` §2.4 ekinin ve §2.5'in kural 10a için verdiği 0,038'lik üst sınır, alt ağaç hedefleri çıkarılınca en çok ~0,011.
  - `01-BUTUNLUK` §10'daki kural 10a'nın katman payı 0,014 → en çok ~0,003; kapının ölçülmüş üst sınırı ~0,02'ye iner (§4).
  - Her ek tur artışı, B6 kural 7 her tur değişimini olay saydığı sürece (Ö-1) bütün ağda olay selamı ve I'nın `I_MIN`'e inmesi demektir.
  - Yeni turu benimseyen düğüm, eski turlu komşularını geçici olarak uygulanamaz görür. §11 madde 8'in "gevşetir" sözü geçiş anında yalnız yarı doğru; art arda artış ağı bu geçiş hâlinde tutar ve açlık isteklerini de besleyebilir.
  - Kontrol payı kestirimine girmemiş (§4).
- **Öneri** (karar gerektirir; ana seçenek Y1 değişmez):
  - Sınıf dalına alt ağacı dışlayan bir koşul: ör. j'nin ilan ettiği maliyet benimkinden küçük (C_j < C), ya da babeld'in metrik koşulu sınıf dalında da (m_j < m_ardil).
  - Beklemenin istenen turdan bağımsız olması: ardılın S'de kaldığı her bölümde ya da her `YOK_SAYMA_S`'de kural 10a için en çok bir istek, tur ne olursa olsun.
  - Bağlı sayıların düzeltilmesi: `B4` §6, `01-BUTUNLUK` §2 ve §10, `18` §2.4 eki ve §2.5.
  - Tanıya: kural 10a isteklerinden doğan tur artışları; isteğin hedefi sonradan aday oldu mu.

### Ö-1 · B6 kural 7 her tur değişimini olay sayıyor: RFC'ye, 17 Kasım kararına ve B4 kural 15'e aykırı; bedeli kestirimde yok — **önemli**

- **Yer:** `v2/bilesen/B6-KONTROL-ILETILERI.md:104` · `:20` · `B4-YOL.md:170` · `v2/18-YENI-TASARIM.md:682` · `01-BUTUNLUK.md:41–49`.
- **Ne yanlış:**
  - B6 kural 7: "ilan edilen turun değişmesi (istek yanıtı dâhil)" olaydır; kural 12'nin "hemen gönder"i ayrı bir madde olarak da sayılıyor. Yani yanıt olmayan tur değişimi de olay. Geçitte tur her arttığında yeni tur ardıl zinciri boyunca bütün ağa olay selamlarıyla yayılır ve her düğümde I ← `I_MIN` olur.
  - RFC 8966 §3.7.2 (`rfc8966_babel.txt:1240–1245`): tetiklenen güncelleme "to propagate a new sequence number (except to satisfy a request)" için SHOULD NOT. B6 §14 bu bölümü kaynak gösteriyor ama yalnız ardıl değişimine ilişkin SHOULD NOT'ı alıyor.
  - 17 Kasım denetiminin B-10 bulgusu ve kapanışı bunu kapatmıştı: "yalnız bekleyen bir isteği karşılayan tur değişimi hemen selam gönderir" (`arsiv/denetim/DENETIM-KURAL-KAPANIS-2026-11-17.md:13`). Bugünkü kod da öyle (`v2/kural/KK-02-SELAM.md:34`). `18` §2.6'nın "Z1 ölçülmüş koşuldur" gerekçesi ve ölçülmüş %2,69'luk pay bu dar kuralla ölçüldü.
  - B4 kural 15 aynı olayı "tur değişimi (istek yanıtı)" diye yazıyor. İki kâğıt aynı olayın kapsamını farklı tanımlıyor.
- **Bedel** (kestirim): bugünkü sıklıkla (birincilde koşu başına 33 tur artışı) her artış ~40 düğümde olay ve aralığın yeniden kısalması demek. Kısalma 2 s'lik çizelgeye göre ~4 s içinde düğüm başına ~2 ek selam getirir. Koşu başına ~2 600 ek selam (9 384'ün %28'i) ve protokolün payında ~+0,7 puan. E-1 tur artışını sıklaştırırsa bu bedel onunla çarpılır.
- **Öneri:** B6 kural 7'deki tur maddesini, bekleyen bir isteği karşılayan değişime (B4 kural 12'nin "tutulan istek varken rotamın turu ≥ t" dalı) ve geçidin istekle artışına daraltmak; B4 kural 15 aynı cümleyle. Ya da geniş hâli kararla, bedeliyle ve RFC'den fark olarak yazmak.

### Ö-2 · Döngü tanısının "0 olmalı" beklentisi kuramca yanlış; "ölçüldü: 0" bir ölçüm değil — **önemli**

- **Yer:** `B4-YOL.md:189` (kural 17) · `:348` (§13 madde 12) · `:399–403` (§15) · `01-BUTUNLUK.md:147` (S4 madde 4) · `v2/18-YENI-TASARIM.md:527` (§2.4'ün tablosu), `:542` ("döngüsüzlük garanti (ölçüldü: 0)") · `arsiv/teshis/faz5_3_dongu_kurallari_2026-11-24/sonuc.md:17`, `:121`.
- **(a) Kuram.** Uygulanabilirlik koşulu iletim grafiğinin her an döngüsüz olduğunu garanti eder (RFC 8966 §2.4, `rfc8966_babel.txt:345–351`). Aynı paketin aynı düğüme dönmemesini garanti etmez. FD yeni turla "iyileşir" (kural 1'in sıralaması), paket bir düğümde (kuyrukta ya da B7'nin bekletmesinde) dururken yol değişebilir. B4 §15'in "paketin geçtiği düğümlerin FD'si her atlamada kesin iyileşir. Bu yüzden paket aynı düğüme dönemez" çıkarımı FD'lerin zamanla değişmediğini varsayıyor.
- **Karşı örnek** (`01-BUTUNLUK` S4'ün kendisi):
  - l'nin ardılı i. l'nin bir telemetri paketi p, i'nin kuyruğunda.
  - i'nin ardılı düşer, i açlığa girer ve p'yi bekletir (B7 kural 1).
  - l, i'nin ∞ ilanını alır; başka yolu (m üzerinden) uygulanamazdır; tur ister. Geçit turu artırır. l yeni turla m üzerinden yol kurar ve (T+1, C_l) ilan eder.
  - i için bu ilan yeni turlu olduğu için uygulanabilirdir. i'nin ardılı l olur, i açlıktan çıkar, B7 tamponu hemen yeniden sordurur (kural 3) ve p l'ye gider.
  - p, l'ye daha büyük atlama sayısıyla döner; kural 17 bunu döngü sayar. Oysa iletim grafiği her an döngüsüzdür: önce l → i → j, sonra i → l → m. Bekletme 1 s'dir; sığ düğümlerde tur isteğinin gidiş-dönüşü bunun altında kalabilir (17 Kasım denetimi S-2: atlama başına ~0,3 s).
- **(b) Ölçüm.** `eğim0` kolunun kayıtlarında `rota.dongu` sayacı hiç yok (ikiz ve birincil, 16 koşunun hepsi; Ek A.3). Sayacı yalnız eğim modülü tutuyor (`protokoller/desparete5_egim.py:302–312`) ve yalnız `egim` açıkken çağrılıyor (`protokoller/desparete5.py:316–318`); `desparete5_rota.py`'de karşılığı yok. Döngü kuralları ölçümünün hesabı eksik anahtara 0 döndürüyor (`arsiv/teshis/faz5_3_dongu_kurallari_2026-11-24/sonuc_hesap.py:63–64`, `.get(ad, 0)`). Tablodaki "0 · 0" ve `18` §2.4'teki "ölçüldü: 0" ölçüm değil, ölçülmemişlik.
- **Sonuç:** B4 §13 madde 12'nin sınaması ("rastgele maliyet değişimleri ve kopmalarla döngü tanısı 0") doğru bir kodda da kırılabilir. "0'dan büyük çıkması hatadır" sözü doğru davranışı "düzeltmeye" yöneltir. Projenin kısıtı (`18` §1.2 F, savunulamayacak iddia yok) açısından "ölçüldü" ifadesi düzeltilmeli.
- **Öneri:**
  - Kural 17'yi "aynı düğüme dönüş" diye adlandırıp yalnız tanı olarak tutmak; hata sayılmaması.
  - Döngüsüzlüğün sınamasını paket dönüşüyle değil, her olaydan sonra bütün düğümlerin ardıl grafiğinin döngüsüz olduğunu denetleyerek yapmak.
  - `18` §2.4'ün tablosuna ve Y1 satırına ve döngü kuralları sonucunun eğim0 satırına "sayaç yoktu, ölçülmedi" notu. Döngüsüzlüğün dayanağı RFC'nin ispatıdır.

### Ö-3 · Niyet döndürmeyen kancada oluşan "silinen komşu" olayı, onu okuyan bileşenler çalışmadan siliniyor — **önemli**

- **Yer:** `B1-KOMSU-VE-BAG.md:107` (kural 18) · `:42` · `:152` (§9: "her kancanın başı … olay listeleri boşalır") · `01-BUTUNLUK.md:85`, `:93` · `v2/18-YENI-TASARIM.md:302–310`.
- **Ne yanlış:**
  - B1'in zaman olayları (silme dâhil) her kancanın başında, niyet döndürmeyen kancalarda da işlenir (kural 20; olay sırası 1).
  - Olay listesi "bir sonraki kancanın başında boşalır" (kural 18).
  - Silinen komşu olayını okuyanlar (B2'nin budaması, B3'ün kaydı silmesi, B4'ün budaması, B7 kural 7) yalnız niyetli kancalarda çalışır.
  - Silme bir `iletim_sonucu` ya da `cerceve_duyuldu` kancasında işlenirse olay, bir sonraki kancanın başında (o kanca niyetli olsa bile) okuyanlar çalışmadan boşalır. Bu bir olasılık değil, kuralın kendisinden çıkıyor.
  - `cerceve_duyuldu` en sık kancadır (çözülen her çerçeve; ikizde düğüm başına saniyede ~71, B2 §12). Silmenin işlendiği ilk kanca çoğu zaman odur.
- **Sonuç:** B2, B3 ve B4'ün komşu başına kayıtları ve B7'nin izi budanmaz; sözleşme 8'in silme kuralı ve B7 kural 7 çoğu silmede çalışmaz. Davranışa etkisi sınırlı: B4'ün adayları B1'de kayıtlı olmayı istiyor, B7'nin izi 3 s'lik tazelikle zaten bayatlıyor. Ama kuralın metni bu hâliyle kodlanamaz, ve B7 kural 8 silinmiş komşunun B3'teki eski durumunu okuyabilir.
- **Öneri:** olay listeleri bir sonraki niyetli kancanın sonunda boşalsın (niyetsiz kancalarda birikir). Ya da okuyanlar her niyetli kancada B1'in komşu kümesiyle karşılaştırarak budasın; kural 18 yalnız B6'nın "yeni komşu" olayı için kalsın (kayda giriş yalnız `kontrol_alindi`'de olur, o kanca niyetlidir).

### Ö-4 · "Kopma" ve "rota kuruldu" beyanları tanımsız — **önemli**

- **Yer:** `v2/18-YENI-TASARIM.md:307` (olay sırası 7) · `01-BUTUNLUK.md:91` · `B7-BEKLETME-KOMUT.md:75` (yalnız `rota_gecersiz`) · önceki tasarım `v2/kural/KK-00-DIZIN.md:26` (genel kural 4) · `v2/06-ON-KAYIT.md:84–85`.
- **Ne eksik:**
  - Olay sırasının 7. adımı kopma ve rota kuruldu beyanlarını sayıyor. Hiçbir kâğıt bunların ne zaman, hangi bileşende ve hangi komşu için üretileceğini yazmıyor; `00-DIZIN`'de de yok.
  - Önceki tasarımda KK-00 genel kural 4 tanımlıyordu ve anlamın Babel, AODV ve OLSRv2 ile aynı olmasını istiyordu (K-139).
  - Ön-kayıtta protokolün algıladığı kopma, algılama duyarlılığı, Δ ve COR bu beyanlara dayanıyor. Beyan üretmeyen kol "beyan etmiyor" diye etiketlenir (`sim2/gozlem/karar.py`).
  - Yeni tasarımda kopmanın üç adayı var ve seçim karar ister: ardılın S'ye düşmesi (bağ kullanılmaya devam eder), KULLANILMAZ olması, ilanın ömrüyle aday dışı kalması. Babel-a "kullanılır komşu kümesinden çıkan ve seçili rotası olan komşuyu" kopma sayıyor (`protokoller/babel.py:897–911`).
- **Öneri:** beyanların sahibi olan bileşene (B4 en doğal yer) bir kural. Örnek: "kopma(K): bir önceki niyetli kancada ardılım olan K bu kancada aday değil; S'ye düşmek kopma değildir · rota_kuruldu(K): K'nin kopmasından sonra yeniden ardılım var". Anlamın Babel-a ile karşılaştırılabilirliği yazılmalı.

### Ö-5 · B6 kural 11 kısmi kanal kilidinde de selamı susturuyor; "kilitteyken gönderemem" varsayımı kilit saniyelerinin çoğunda tutmuyor — **önemli**

- **Yer:** `B6-KONTROL-ILETILERI.md:123–128` · `B5-ILETIM-KARARI.md:82` · `B2-KARISTIRMA-KANITI.md:10` · `01-BUTUNLUK.md:64` · `v2/18-YENI-TASARIM.md:377`.
- **Ne yanlış:**
  - B2'nin "kanal kilidi" durumu, bir saniyenin meşgul payının 0,55'i geçmesidir (kural 2 ve 6).
  - Kural 11'in gerekçesi ("kanal kilidinde geri çekilme bitmez; kurulan selamlar kuyrukta birikir") yalnız meşgul payı 1'e yakınken doğru. Meşgul payı 0,55–0,95 olan saniyede kanal %5–45 boştur: geri çekilme biter, veri gider (B5 sorulur), selam da giderdi.
  - Kural 11 bu saniyelerde selamı kurmaz. Komşularda ilanım 3,5 · a sonra bayatlar ve alt ağacım beni aday olmaktan çıkarır; ben veri göndermeyi sürdürürüm. Bitim de bu sürede komşulara gitmez.
  - B5 kural 6'nın ve `01-BUTUNLUK` §3'ün "geri çekilme bitmez, sorulmaz" ifadesi yalnız tam kilit için doğru.
- **Kanıt** (B2 teşhisinin saniyelik kayıtları, `m` binde birim; açık evre, kilit işaretli düğüm-saniyeler; Ek A.5):

  | hücre | düğüm-saniye | m 0,55–0,70 | 0,70–0,85 | 0,85–0,95 | ≥ 0,95 | kâhinin alanı E · G · U |
  |---|---|---|---|---|---|---|
  | birincil | 1 009 | %46,1 | %10,7 | %9,4 | %33,8 | %60,8 · %2,2 · %37,1 |
  | dayanıklılık | 694 | %36,7 | %12,2 | %8,5 | %42,5 | %73,6 · %3,9 · %22,5 |

  Kilit saniyelerinin %57–66'sında düğüm kanalın bir kısmında gönderebiliyor. Birincilde bu saniyelerin %37'si kâhinin U alanında.
- **Öneri** (karar): kural 11'i gerçekten gönderemediğim duruma bağlamak (ör. meşgul payı ≥ 0,95); ya da kuralı korumak ve bedelini (kısmi kilitte susturulan selamlar, alt ağaçta bayatlayan ilanlar) yazıp tanıya koymak. B5 kural 6 ve `01-BUTUNLUK` §3 kısmi kilidi kapsayacak biçimde düzeltilir. Kural 11 karıştırma katmanındadır; kapının payını eksiye çekebilir (§4).

### K-1 · B4 kural 3: yok saymadaki ardılın adaylığında hangi ilan kullanılır? — **küçük**

- **Yer:** `B4-YOL.md:86` (kural 3) · `:127–132` (kural 10) · `:177–187` (kural 16) · `:41–42` (§3).
- **Ne belirsiz:** B4 komşu başına iki ilan tutuyor (son ilan, kabul edilen ilan). Kural 3 adaylığı "ilanı sonlu, taze ve uygulanabilir" diye tanımlıyor ama ardıl yok saymadayken hangisinin kullanılacağını söylemiyor.
  - Son ilan kullanılırsa ardıl 3. adımda aday dışı kalır, 5. adımda zorunlu geçiş olur ve kural 10 hiç çalışmaz.
  - Tazelik kabul edilen ilanın yaşıyla ölçülürse, olaydan sonra a = 0,55 s iken ömür 1,9 s'dir; yok sayma 5 s dolmadan biter.

  Doğru okuma kural 10 ile kural 7'den çıkarılabilir (uygulanabilirlik kabul edilen ilanla, tazelik son ilanla), ama tek anlamlı değil. Ardıl değişince yok saymanın bittiği de yazılı değil.
- **Öneri:** kural 3'e bir cümle: "Ardıl yok saymadayken uygulanabilirlik kabul edilen ilanla, tazelik son ilanla değerlendirilir; ardıl değişince yok sayma biter."

### K-2 · B2 kural 12: geriye dönük açılan aralık sayımı sıfırlamıyor — **küçük**

- **Yer:** `B2-KARISTIRMA-KANITI.md:120–131`.
- **Ne eksik:** kayıtlar geldikleri kancada sayılır. Aralık sonradan (en çok `G_GIRIS` s geriye) açılınca o kayıtların olayı geçersizleşir (kural 13), ama sayım sıfırlanmaz. Aralığa düşen yeni bir kayıt gelmezse sayım 3'ün üstünde kalır. "Sayım sürerken yeni olay oluşmaz" kuralı yüzünden aralıktan sonraki tam denemeli seri olay doğurmaz.
- **Senaryo:** i'nin j'ye kayıtları 151,6 · 152,1 · 152,8 s'de tam denemeli → olay. 153,4'te aralık [151,4, ∞) açılır, olay geçersiz. i 153,4–164,4 arasında j'ye göndermez (ardılı kısa süre k olmuştur). Aralık 164,4'te biter. j'ye 165,2 · 165,9 · 166,4 kayıtları tam denemeli → sayım 4, 5, 6, olay yok; j'nin karıştırılması gönderici kanıtı vermez.
- **Öneri:** aralık açıldığında ya da bir kaydın aralığa düştüğü sonradan anlaşıldığında sayım sıfırlansın; ya da sayım her kancada aralık dışındaki kayıtlardan yeniden kurulsun. §13 madde 11–12'ye sınama.

### K-3 · B7 §8 ile kural 5 çelişiyor: kilitten sonra "süre dolduysa düşer" — **küçük**

- **Yer:** `B7-BEKLETME-KOMUT.md:122` · `:78`.
- **Ne tutarsız:** §8 "kilit bitince sorulurlar: yol varsa gider, yoksa ilk bekletmeden beri süre dolduysa düşer" diyor. Kural 5 ilk bekletme kaydını 2 s sonra siliyor. 15 s'lik kilitten sonra kayıt yoktur; paket yeni sayılır ve 1 s daha bekletilir. Etkisi küçük, ama §8 ile §13 madde 1'in sınaması çelişir.
- **Öneri:** §8'i kural 5'e göre düzeltmek; ya da kayıt silmeyi değiştirmek (protokol paketin tamponda mı kuyrukta mı olduğunu bilemez).

### K-4 · Rotası ∞ olan ardıl rota isteğine yanıt vermiyor (RFC 8966 §3.8.1.1, MUST) — **küçük**

- **Yer:** `B4-YOL.md:95` · `:149–156`.
- **Ne farklı:** RFC §3.8.1.1'e göre seçili rota yoksa rota isteğine geri çekmeyle yanıt verilir (MUST; `rfc8966_babel.txt:1318–1322`); Babel-a da öyle (`protokoller/babel.py:436–456`). B4'te ardılın rotası ∞ ise yanıt yoktur; gerekçe, ∞'un zaten "hemen gönder"le ilan edilmiş olması. Ama kural 4a tam da ardılın ilanı tazelenmeyince çalışır; yani ∞ ilanı büyük olasılıkla kaybolmuştur. Yanıtsızlık ardılın bırakılmasını ilanın ömrünün sonuna, en çok bir aralık (≤ 2,2 s) erteler; bu sürede paketler rotasız ardıla gider.
- **Öneri:** kalan atlama 1 iken rota ∞ ise "hemen gönder" (selamda ∞).

### K-5 · Ardılsız düğüm tur isteğini iletiyor; 17 Kasım B-16 kararı yazılmadan tersine döndü — **küçük**

- **Yer:** `B4-YOL.md:152` · `arsiv/denetim/DENETIM-KURAL-KAPANIS-2026-11-17.md:31` · `rfc8966_babel.txt:1344–1348`.
- **Ne farklı:** RFC iletmeyi "the node is advertising the prefix" koşuluna bağlıyor; Babel-a seçili rotası yokken iletmiyor (`protokoller/babel.py:471–473`). B4 kural 12'nin "öteki hâllerde" dalı açlıktaki düğümü de kapsıyor ve isteği uygulanamaz bir komşuya iletiyor. B4 §14 yalnız "uygulanamaz yola iletme"nin eklendiğini yazıyor. Ardılsız düğümün iletmesi ve 17 Kasım'daki "ardılsız düğüm iletmez" kararının değiştiği yazılı değil. Ağ çapında açlıkta (ör. geçit kanal kilidindeyken) her açlık isteği onu duyan açlıktaki düğümlerce iletilir; bastırma (1 s) ve 64 atlama bunu sınırlar.
- **Öneri:** kararı gerekçesiyle yazmak ya da RFC'ye dönmek.

### K-6 · Küçük metin hataları ve belirsizlikler — **küçük**

- `B6-KONTROL-ILETILERI.md:195`: çözme ve dağıtım "olay sırası 1" diye yazılı; 28 Kasım'dan beri 2. adımdır (B6 kural 3, `:88`).
- `B2-KARISTIRMA-KANITI.md:93–95`: girişim alt durumunun çıkışı için "işaretsiz saniye", kural 4'ün (`:86`) aynı adlı tanımıyla (girişim işareti yok ve m < 0,62) karışabilir. Teşhisin kuralı yalnız girişim işaretine bakıyor (`arsiv/teshis/faz5_3_b2_isaretler_2026-11-24/isaret.py:277–295`); §13 madde 17'nin eşdeğerlik sınaması bunu ister. "Girişim işareti olmayan saniye" denmeli.
- `B3-BAG-DURUMU.md:93`: "son `VERI_YOK_N` kaydın hepsi vazgeçme" için en az `VERI_YOK_N` kayıt bulunması koşulu yazılı değil. Teşhisin E4'ü bunu şart koşuyor ("en az n önceki kaydı olan").
- `B7-BEKLETME-KOMUT.md:71–73` (kural 3): "tamponda paket varken her `YENIDEN_SOR_S`'de bir uyandırma". Daha erken bir plan varken yenisinin kurulmayacağı yazılmalı (bugünkü kodun kuralı, `protokoller/desparete5.py:171–178`); yoksa her bekletme kararı yeni bir nesil üretir.
- Örnek senaryolardaki bazı anlar yazılmamış kayıp ve kuyruk varsayımlarına dayanıyor. Örnek: B2 §12 ve B3 §12'de ikinci bit selamı 155,1 s'de geliyor; B6 §12'nin çizelgesiyle selamlar 153,9 · 154,9 s'dedir. Her kâğıdın §13'ündeki "örnek senaryonun sayıları uçtan uca" sınaması için bu varsayımların yazılması gerekir.

---

## 2 · Sorunlar (bulgu değil, bilinmeli)

- **S-1 · Genel mekanizmalar katmanın işinin büyüğünü görüyor.** B3 kural 7 (veri yok) temiz kanalda örneklerin %0,01–0,15'inde, karıştırılan alıcıda %7–26'sında ateşliyor (B3 teşhisi E4). J1'in 0,0324'ünü veri yok ve ilanın ömrü de görüyor (B5 teşhisi E7). K-247'ye göre sınıf amaçla belirlenir ve ikisinin amacı genel; `01-BUTUNLUK` §10 bunu yazıyor. Kapının kolunu inceltir (§4).
- **S-2 · Uzun karıştırmada sınırların tutarsızlığı.** B3 kural 9 ve B4 kural 4'ün kendi aralığımdan çıkardığı süre `HARIC_UST_S` (30 s) ile sınırlı; B4 kural 14'ün istek bastırması ve B2'nin durumu sınırsız. `DF_UNUT_S` de 30 s olduğu için 30 s'yi aşan bir kendi aralığının sonunda bütün komşuların `d_f`'si bir an tanımsız olabilir: aralıktaki bildirimler sayılmaz, öncesindeki 30 s'den eskidir. Bu durumda yeni bir bildirim gelene kadar bütün bağlar KULLANILMAZ olur. Birincil (15 s) ve dayanıklılık (10 s) hücresinde oluşmaz; sürekli yer karıştırıcılı ailede oluşabilir.
- **S-3 · Kendi karıştırılmamda ölen ardıl.** Kendi aralığımda ilanların yaşı durur ve MAC sonuçları kanıt sayılmaz. Bu yüzden o sırada ölen ya da kilide giren ardıl, aralığım bitene kadar aday kalır ve paketler ona gider. Kendi alımım bozukken bunu ayırt etmenin yolu yok; tasarımın bilinçli sonucu, ama hiçbir kâğıtta yazılı değil.
- **S-4 · İki meşgul payı eşiği.** 0,55–0,62 arası saniyeler kanal kilidi sayılır ama c̄'ye girer (`ED_ESIK` · `CBAR_ED_ESIK`). `00-DIZIN` bunu Aşama 4'e bırakmış.
- **S-5 · Yol maliyetinin doyması.** `m_j` 0xFFFE'de doyunca kesin artış (M(c, m) > m) o noktada bozulur. ~1 000 ETX'lik yol bu dünyada oluşmaz.
- **S-6 · Rota isteği yanıtı aralığı kısaltıyor.** Kural 4a'nın yanıtı B6 kural 7'de olaydır; ardılın I'sı `I_MIN`'e iner. İstek başına ardılda ~1–2 ek selam getirir (~+0,1–0,3 puan). Kestirime girmemiş ama küçük.
- **S-7 · Bekletme tamponunun dökülmesi.** Simülatör tamponu her uyandırmada döker. Bu, tampondaki her paket için yeni bir `sonraki_atlama` çağrısı demek; davranışı değiştirmez, koşu süresini uzatır.

## 3 · Temiz çıkanlar

- **İletim grafiğinin döngüsüzlüğü:** karşı örnek kurulamadı. Dayanakları:
  - ∞ ilan her zaman uygulanabilir ve yok sayılmaz (kural 1, 10);
  - bağ maliyeti en az 64 olduğu için yol maliyeti kesin artar (kural 2);
  - FD ilan için verildiği anda güncellenir; bu, gönderilenden büyük olmamasını sağlar (kural 9);
  - yok sayma, hâlâ uygulanabilir olan kabul edilmiş ilanı korur: ardılın kabul edilen ilanı, FD yalnız benim ilan ettiğim ve ondan en az 64 büyük maliyetlerle güncellendiği için uygulanabilir kalır;
  - kuyrukta bayatlayan selam içeriği değişmezi bozmaz.

  Ö-2 döngüyle değil, aynı düğüme dönüşle ilgili.
- **17 Kasım'ın hata türleri yeniden doğmamış** (iki geri dönüş dışında):
  - ∞ ilanın uygulanabilirliği: doğru (B4 kural 1, 10).
  - Çıkışı olmayan durum: yok. B3 geçmiş tutmuyor ve her sebebin çıkışı var; B2'nin durumları bir işaretsiz saniyede biter; B6'nın kilidi B2'ye bağlı; B4'ün yok saymasının üst süresi var; B7 sınırlı.
  - Aynı olayda iki geçiş: yok. B3 her kancada kanıttan yeniden hesaplar; B4 kural 16 ve B2 kural 18 sırayı veriyor.
  - Niyet döndüremeyen kancada karar: kararlar bir sonraki niyetli kancaya bırakılmış; tek açık Ö-3, o da bir olayla ilgili.
  - Geri dönüşler: B-10 (Ö-1) ve B-16 (K-5).
- **Komutun geri izi döngüsüz.** İz, bir hedefin en büyük sıralı telemetrisinin bana ilk geldiği komşuyu gösterir. İzden ize ilerlerken sıra azalmaz. Sıra eşitse aynı paketin geliş anları kesin sıralıdır: a'nın izi b'yi gösteriyorsa paket b'de daha önce vardı. Döngü kurulamaz; aynı paketin bir düğüme iki kez gelmesi (Ö-2) de bunu bozmaz, çünkü ikinci geliş izi güncellemez.
- **Gözlem sözleşmesi:** yasak ya da kâhin alanı okunmuyor (`olculen_gurultu_w`, `komsular`, RSSI, konum hiçbir kâğıtta karara girmiyor). Simülatörle ilgili varsayımlar koda uyuyor:
  - `kanal_dolulugu_ister` örnek özniteliği olarak okunuyor (`sim2/kosum/dugum.py:138`) ve yalnız bir integral açıyor, rastgele çekim yok;
  - `cerceve_duyuldu` çerçevenin işlenmesinden önce çağrılıyor (`sim2/kosum/alim.py:49`);
  - vazgeçmede `iletim_sonucu`, `iletim_basarisiz`'den önce geliyor (`sim2/kosum/kosu.py:214–216`);
  - veri onayı yalnız göndericide sayılıyor (`sim2/kosum/teslim.py:118–124`);
  - uyandırmanın alt sınırı bir yuva (`sim2/kosum/kontrol.py:111–114`);
  - tampon yalnız uyandırmadan sonra, kuyruğun sonuna dökülüyor (`sim2/kosum/dugum.py:717–743`; `kontrol.py:296–300`);
  - tamponun süre tavanı ilk girişten sayılıyor (`dugum.py:680–684`);
  - karar havaya çıkarken veriliyor (`sim2/kosum/gonderim.py:250–318`);
  - `Karar.niyetler` çerçeve havaya çıktıktan sonra uygulanıyor (`kosu.py:167–168`).
- **İleti biçimi:** selamın sabit alanları 65 bit = 9 bayt, komşu başına 2 bayt, 64 bayt kapsülleme; 0 · 15 · 39 komşuyla 73 · 103 · 151 bayt (`kontrol_bedeli.txt` ile aynı). Değerler alanlara sığıyor: 40 düğüme 8 bitlik adres; aralık 0,01 s birimiyle 16 bitte 655 s'ye kadar; oran × 255; bit alanı `bool`. `MesajBicimi`'nin iki tekrarlı alanıyla kurulabilir. Tur isteği 24 bit, 67 bayt.
- **Değerler tek yerde:** 54 değer yeniden sayıldı (B1 11 · B2 13 · B3 5 · B4 13 · B6 8 · B7 4); kural atıfları doğru.
- **Bayraklar:** her alt mekanizma ayrı kapatılabiliyor; kapalıyken kalan kurallar tanımlı. Karıştırma katmanı kapalıyken kalan çekirdek eksiksiz bir protokol: selam kilitte de kurulur, bit 0 gider, yaş kesintisiz işler, istek bastırılmaz.
- **Yeniden doğrulanan sayılar:**
  - B6: %6,04 · %5,86; protokolün payı %2,59 · %2,69; Babel-a %11,0 · %11,6; selam boyları.
  - B7: açlık 103 bölüm, ortalama 2,08 s; bekletilen 525, %38 · %62; teslimin %2,05'i; p99 1,08 s, Babel 1,31 s; komut %22 · %30.
  - Bütünlük H1: %1,86 · %22,75 · 0,0020 · 0,0001.
  - B5: J1 0,0485 · 0,0447; J2 0,022; J3 0,036; D 0,1005; K3 %2,19 · %1,52; K6 0,137; E8 a2 0,038; E7 0,016.
  - B3: K2 0,231 ↔ 0,305; E4 9/82 424 · 81/53 530 · %7,0 · %25,9 · %0,56.
  - B2: `ED_ESIK` %0,037 · %0,007; G %0,002, 0,344 · 0,347; DEN7x3 binde 0,40; K6 0,35; E8 0,463.
  - `00-DIZIN`'in `I_MIN` gerekçesindeki ~0,05 s (7 denemenin ortalama geri çekilmesi ~30 ms, en çok ~61 ms, artı çerçeveler).
- **Zaman çizelgeleri** (15/15 ve 10/20):
  - hiçbir değer çizelgeye bağlı değil;
  - B2'nin girişi 2–4 s, çıkışı ~1 s;
  - bit uzak komşuya selam başına 0,35 olasılıkla, ~3 selamda ~%73 ulaşır;
  - B3'ün kilitli ardıla yeniden denemesi 5 s'de bir;
  - B6'nın selam sıklığı düğüm başına en çok 2/s ile sınırlı;
  - B7'nin bekletmesi en çok 1,5 s.

  Tur artışı seli dışında (E-1) gidip gelme ya da sınırsız sel bulunmadı.
- **`01-BUTUNLUK` §5'in senaryoları:** S1, S2, S3, S5 ve S6 kâğıtların kurallarıyla yürüyor. S2'de birkaç an yazılmamış kayıp ve titreşim varsayımına dayanıyor (K-6). S4'ün 4. maddesi Ö-2'de.

## 4 · Mekanizma kapısı ve kontrol payı

### Mekanizma kapısı (madde 8)

- **Bayraklar ve sınıflar:** grup ve alt bayraklar tutarlı. `kanal_dolulugu_ister` grubu izliyor ve simülasyonu değiştirmiyor. Sınıflar K-247'ye göre amaçla doğru; S-1'in çekincesiyle.
- **Kestirimin yeniden hesabı** (`01-BUTUNLUK` §10):

  | kalem | `01-BUTUNLUK` | bu denetim | dayanak |
  |---|---|---|---|
  | J1'in yalnız katman kanıtlı kısmı | 0,016 | 0,016 | E7; olağan aday uygulanabilir olduğu için alt ağaç sorunu yok |
  | kural 10a'nın katman kanıtlı istekleri | 0,014 | **en çok ~0,003** | E8'in 0,0143'ünün 0,0109'u alt ağaçta (Ek A.1) |
  | **ölçülmüş üst sınırların toplamı** | **~0,03** | **~0,019–0,020** | eşik 0,02 |

- **Sonuç:** ölçülmüş üst sınırlar kapının eşiğine ancak dayanıyor; bunlar üst sınırdır, gerçekleşecek pay altında kalır. Kapının geçmesi ölçülmemiş paylara bağlı:
  - B4 kural 4'te kendi aralığımda yaşın durması: büyük olabilir, açık dönemde G alanında ~6,8 düğüm var;
  - B3'ün hariç aralığı: çoğu sessiz döneme gider;
  - B6 kural 11: Ö-5'e göre eksi olabilir;
  - katmanın kendi bedeli: bildirim ve gönderici kanıtının S'ye düşürdüğü ardıl, E-1'in tur pompasını açık kolda kapalı koldan sık başlatır.

  `01-BUTUNLUK` §10'un "kapı geçebilir ama güvence değil" sonucu yönce doğru; ama sayısı iyimser. Aşama 4'ün beklentisine "ölçülmüş paylar eşikte; kapı ölçülmemiş paylara bağlı" diye yazılmalı. B4 kural 4'ün payı var olan kayıtlardan (girişimdeki düğümün ardılının ilanının kendi aralığında bayatlaması ve ardından gelen açlık) kestirilebilir; bunun yapılıp yapılmayacağı karar konusu.

### Kontrol payı (madde 9)

- **Taban doğru:** bugünkü olay kümesiyle protokolün payı %2,69, onaylar %3,18, toplam %5,86 (birincil). Bit değişimi (~%0,05) ve kural 4a (~%0,4) kalemleri savunulabilir. Kural 4a'nın kestirimi tutucu: ölçülen üç ardışık kayıptan (%2,1) bağımsızlıkla iki ardışık kayba gidiyor, kayıpların kümelenmesi iki ardışık kaybı bu kestirimin altında tutar.
- **Kestirimde olmayan kalemler:**
  - Ö-1, her tur değişiminin olay olması: bugünkü tur artışı sıklığıyla ~+0,7 puan;
  - E-1, kural 10a'nın her tur benimsenişinde yeniden kurulması: açık dönemde tur artışını sıklaştırır, her artış ~80 ek selam demek;
  - S-6, rota isteği yanıtının aralığı kısaltması: ~+0,1–0,3 puan.
- **Tavan:** `SELAM_ARASI_EN_AZ` (0,5 s) her düğümü saniyede en çok iki selamla sınırlar. Bütün düğümler sürekli `I_MIN`'deyse koşu başına ~28 000 selam olur ve kontrol payı onaylarla birlikte ~%10'a çıkar. %10'u ortalamada aşmak beklenmez. E-1 ile Ö-1 birlikte açık dönemde ağı bu tavana yaklaştırabilir; kaba kestirimle ortalama protokol payı %4–5, onaylarla %7–9.
- **Çok komşulu düğüm:** 39 komşuyla selam 151 bayt (1,40 ms), 15 komşuyla 103 bayt (1,02 ms). O düğümün selamı %37 uzar; ağ ortalamasında küçük (ölçülen ileti başına ~99 bayt).
- **Değerlendirme:** "~%3 · ~%6–7" kestirimi bugünkü olay kümesi için savunulabilir. Kâğıtların yazdığı olay kümesiyle (Ö-1) ve kural 10a'yla (E-1) iyimser.

## 5 · Doğrulanamayanlar

- E-1'in yeni tasarımdaki tur artışı sıklığı ve kontrol bedeli. Kayıtlar `eğim0`ın trafiğidir; alt ağaç, her düğümün son telemetri kararının ardılıyla yaklaşık izlendi.
- Kural 10a'nın hedefi olan komşunun B3 durumu (kayıt yalnız kâhinin "temiz" etiketini tutuyor, sınıfı değil).
- Ö-2'deki aynı düğüme dönüşün sıklığı.
- Ö-5'in teslime etkisi; U alanındaki kilit saniyelerinin karıştırıcıdan mı tıkanıklıktan mı geldiği (kayıt yalnız alanı tutuyor).
- Kapının ölçülmemiş payları (B4 kural 4, B3 kural 9, B6 kural 11).
- Gerçek kontrol payı (Aşama 4'te, B6 §13'ün tanısıyla).

## 6 · Hüküm

**Tasarım bu hâliyle dondurulmaya ve kodlanmaya hazır değil.**

Kararlar kâğıtlara büyük ölçüde sadık. İskelet ve sözleşmeler tutarlı; kâğıtlar eksiksizlik listesini cevaplıyor. Döngüsüzlüğün çekirdeği, gözlem sözleşmesi, ileti biçimi, değerler ve sayısal dayanakların çoğu temiz. Ama bir kural (B4 kural 10a), birincil hücrenin tam hedeflediği durumda yanlış komşuyu hedefliyor ve kendini yeniden kurarak art arda tur artışı doğurabiliyor; bu, tasarımın kendi sıklık ve kapı kestirimlerini de değiştiriyor. Ayrıca kodlayanın tahmin etmek zorunda kalacağı birkaç boşluk ve iki geri dönüş var. Hepsi belge düzeyinde düzeltilebilir; simülasyon gerekmez.

Kod yazılmadan önce, sırasıyla:

1. **E-1:** kural 10a'nın sınıf dalına alt ağacı dışlayan koşul ve istenen turdan bağımsız bekleme (karar). Bağlı sayıların düzeltilmesi: `B4` §6, `01-BUTUNLUK` §2 ve §10, `18` §2.4 eki ve §2.5.
2. **Ö-1:** tur değişimi olayının kapsamı; B4 kural 15 ile B6 kural 7 tek cümlede. RFC'ye ve 17 Kasım kararına dönüş, ya da gerekçeli geniş kural (karar).
3. **Ö-5:** B6 kural 11'in tetiği (kısmi kilit; karar). B5 kural 6 ve `01-BUTUNLUK` §3'ün ifadesi.
4. **Ö-3:** olay listelerinin niyet döndürmeyen kancalardaki anlamı (B1 kural 18, §9).
5. **Ö-4:** kopma ve rota kuruldu beyanlarının tanımı (karar).
6. **Ö-2:** döngü tanısının adı, beklentisi ve sınaması (B4 kural 17, §13 madde 12, §15; `01-BUTUNLUK` S4). `18` §2.4'teki "ölçüldü: 0"ın düzeltilmesi.
7. **K-1 ve K-6'nın B2 ile B3 cümleleri:** kodlamadan önce; K-2…K-5 ve K-6'nın kalanı kodla birlikte kapatılabilir.
8. **Kestirimlerin yeniden yazılması:** mekanizma kapısının ölçülmüş payı ~0,02 (Aşama 4'ün beklentisine); kontrol payına Ö-1 ve E-1'in kalemleri.

Bu liste kapanınca B4'ün (kural 3, 10, 10a, 12, 15, 17, §6, §11, §15), B6'nın (kural 7, 11, §9), B1 kural 18'in ve `01-BUTUNLUK` §2, §5 S4 ve §10'un kısa bir ikinci okumadan geçmesi önerilir. E-1'in çözümü B4'ün istek kurallarının birbirini nasıl beklediğini değiştirecek; Ö-1'inki ile birlikte okunmalı.

---

## Ek A · Yeniden hesaplar

Betikler depo dışında, oturumun geçici klasöründe yazıldı. Bütün komutlar depo kökünden koşuldu, kayıtları yalnız okur. `-I` bayrağı `PYTHONIOENCODING` ve `PYTHONDONTWRITEBYTECODE`'u yok saydığı için betikler çıktıyı kendileri UTF-8'e çevirir ve içe aktarılan teşhis modüllerinin `__pycache__` yazmasını `sys.dont_write_bytecode` ile önler.

Komutların biçimi (`<betik>` aşağıdaki dosyalardan biri):

```
py -3.11 -I <betik> arsiv/teshis/faz5_3_b5_iletim_kaybi_2026-11-26
```

### A.1 · Kural 10a'nın hedefi alt ağaçta mı (`e8_alt_agac.py`)

```python
import bisect, statistics as ist, sys
from collections import defaultdict
from pathlib import Path
sys.dont_write_bytecode = True
sys.stdout.reconfigure(encoding="utf-8")
D = Path(sys.argv[1]); sys.path.insert(0, str(D))
import iletim as L, sonuc_hesap as SH
KATMAN = L.K_BILDIRIM_A | L.K_GONDERICI
CEKIRDEK = L.K_VERI_YOK | L.K_ILAN_BAYAT | L.K_KULLANILMAZ
ADAY_DISI = L.K_ILAN_BAYAT | L.K_KULLANILMAZ
oz = defaultdict(list)
for r in SH.oku(D)["birincil"]:
    n, kl = SH.dogan(r), SH.kararlar(r)
    kar = defaultdict(list)
    for o in kl:
        kar[o.i].append((o.t, o.j))
    for v in kar.values():
        v.sort()
    zam = {d: [t for t, _ in v] for d, v in kar.items()}
    def ardil(d, t):                      # son telemetri kararının ardılı, 2 s taze
        v = kar.get(d)
        x = bisect.bisect_right(zam[d], t) - 1 if v else -1
        return v[x][1] if x >= 0 and t - v[x][0] <= 2.0 else None
    def alt_agac(u, i, t):                # u'nun yolu i'den geçiyor mu
        d = u
        for _ in range(40):
            a = ardil(d, t)
            if a is None: return None
            if a == i: return True
            if a == 0: return False
            d = a
        return None
    p = defaultdict(float)
    for o, _ in SH.kayiplar(r, kl):
        if o.sinif("A") not in ("J3", "J4", "U2"): continue
        if not (o.uK >= 0 and L.temiz(o.zuK, o.p7uK)): continue
        w, aa = o.p7uK, alt_agac(o.uK, o.i, o.t)
        p["k6"] += w; p["k6_alt"] += w if aa else 0
        if not o.kanit & L.KANIT_A or (o.k1 >= 0 and o.k1_O == 1) \
                or (o.kanit & ADAY_DISI and o.k1 < 0):
            continue                      # E8'in a2 dalı değil
        p["a2"] += w; p["a2_alt"] += w if aa else 0; p["a2_bilinmiyor"] += w if aa is None else 0
        if o.kanit & KATMAN and not o.kanit & CEKIRDEK:
            p["a2_katman"] += w; p["a2_katman_alt"] += w if aa else 0
    for k in ("a2", "a2_alt", "a2_bilinmiyor", "a2_katman", "a2_katman_alt", "k6", "k6_alt"):
        oz[k].append(p[k] / n)
for k, v in oz.items():
    print(f"{k:16s} {ist.mean(v):.4f}")
```

Çıktı (birincil, 8 tohum): a2 0,0383 · a2_alt 0,0274 · a2_bilinmiyor 0,0022 · a2_katman 0,0143 · a2_katman_alt 0,0109 · k6 0,1364 · k6_alt 0,0829. a2, a2_katman ve k6 E8 ile K6'yı birebir üretiyor.

### A.2 · Kural 10a'nın sınıf dalının koşulu: karar ve bölüm sayısı (`k10a_bolum.py`)

A.1'in `ardil` ve `alt_agac` işlevleriyle. Her telemetri kararında koşul: ardılın B3 son çare sebebi var (`kanit & (K_BILDIRIM_A | K_GONDERICI | K_VERI_YOK)`, `K_ILAN_BAYAT | K_KULLANILMAZ` yok), olağan aday yok (`k1 < 0` ya da `k1_O == 0`), temiz engelli komşu var. Aynı düğümde 10 s'den uzun arayla gelen karar yeni bölüm sayılır.

Çıktı (koşu başına ortalama, en az–en çok):
- ikiz: koşul 11,6 (1–60) · alt ağaç 4,8 · bölüm 4,4 (1–17) · düğüm 3,1;
- birincil: koşul 244,4 (25–644) · alt ağaç 171,4 (%58) · bölüm 21,0 (7–50) · düğüm 12,9 · kararların %0,82'si.

### A.3 · Eğim0'ın döngü sayacı (`dongu_sayaci.py`)

`arsiv/teshis/faz5_3_yeni_cekirdek_2026-11-19/kayit_egim0_{ikiz,birincil}.json` ve `kayit_cekirdek_birincil.json`'da her koşunun `teshis_toplam` sözlüğünde `rota.dongu` aranır. Çıktı:
- eğim0, iki hücre, 16 koşu: anahtar yok;
- `rota.*` anahtarları açlık, istek ve geçiş sayaçlarından ibaret;
- 19 Kasım çekirdeğinde var (birincil: 7 827 · 183 · 13 251 · 41 · 477 · 3 830 · 326 · 3 027).

### A.4 · Eğim0'ın tur artışı ve istekleri (`tur_sayisi.py`)

Aynı eğim0 kayıtlarından `rota.tur_artirildi`, `rota.aclik`, `rota.aclik_istegi`, `rota.yoksay_istegi`, `rota.istek_iletilen` koşu başına ortalama:
- ikiz: 26,1 · 17,8 · 34,1 · 55,1 · 189,9;
- birincil: 32,5 · 103,0 · 213,8 · 83,9 · 462,5.

### A.5 · Kilit işaretli saniyelerde meşgul payı (`kilit_m.py`)

`arsiv/teshis/faz5_3_b2_isaretler_2026-11-24/kayit_{birincil,dayaniklilik}.json` okunur. Her koşunun `kaydedici.ds.m` (binde birim) ve `ds.z` (kâhinin alanı) dizilerinde, `kaydedici.evre == "a"` olan saniyelerden m ≥ 550 olanların m dağılımı ve alanı sayılır. Çıktı §1 Ö-5'in tablosundadır.

---

## 7 · İkinci okuma (28 Kasım)

- **Okunan hâl:** `a305643` ve çalışma ağacındaki commit edilmemiş düzeltmeler: `git diff --stat` 12 dosya, +207 −160 (B1–B7, `00-DIZIN`, `01-BUTUNLUK`, `v2/18`, `v2/12`, döngü kuralları `sonuc.md`). Kapanış taslağı `arsiv/denetim/DENETIM-TASARIM-KAPANIS-2026-11-28.md`. Okuma sırasında `git status --short`: 12 değişmiş dosya; izlenmeyen yalnız bu rapor ve kapanış taslağı.
- **Yöntem:** farkın tamamı okundu. Değişen kurallar kaynağıyla (RFC 8966, `protokoller/babel.py`, `babel_bicim.py`) ve birbirleriyle karşılaştırıldı; eski anışlar tarandı; bir sayı kayıtlardan okundu (§7.2, Y-1). Simülasyon yok.

### 7.1 · Düzeltmeler bulguları kapatıyor mu

| bulgu | sonuç | not |
|---|---|---|
| E-1 | kapandı | Bekleme istenen turdan bağımsız (`B4` kural 10a; kaydı §3'te): her yeni turda yinelenen istek kesildi, düğüm başına `YOK_SAYMA_S`'de en çok bir 10a isteği. `C_j` < C kararlı durumda doğrudan alt ağacı dışlıyor. Metrik koşulu yerine `C_j` < C seçimi savunulabilir: yeni turdan sonra hedefin uygulanabilir olmasını da sağlıyor. Bedeli §7.2'de. |
| Ö-1 | kapandı | `B4` kural 15 ile `B6` kural 7 aynı cümle; RFC 8966 §3.7.2 ve 17 Kasım'ın B-10 kararıyla uyumlu. İsteğin yanıtı istek yolu boyunca yine olay selamıyla döner (tutulan istek, kural 12), açlıktan çıkışın hızı korunuyor. |
| Ö-2 | kapandı | Kural 17 yalnız tanı; döngünün sınaması ardıl grafiğinde (§13 madde 12, tanı listesi); §15'in çıkarımı düzeltildi; "ölçüldü: 0" notları yazıldı. Tablo biçimi için Y-2. |
| Ö-3 | kapandı | Listeyi okuyanların hepsi (B2, B3, B4, B7) her niyetli kancada çalışıyor; liste niyetli kancanın sonunda boşalıyor. |
| Ö-4 | kural yazıldı | Anlamı Babel-a'nınkinden ayrılıyor: Y-1. |
| Ö-5 | kapandı | Kuralı kaldırmak savunulabilir. Kilitten sonra ilk bayat selamın farkı −(zaman aşımı sayısı) olur, geri alma sıfırları siler; ötekiler fark 0'la eklenir (B1 kural 4). 15 s'lik kilitte 5–9 selam birikir; B1 Ö-5 ~100 s'den kısa kilitte tutuyor. B6'nın karıştırma eki kalmadı; B6 kapının iki kolunda aynı. Kalan küçük etkiler §7.2'de. |
| K-1 … K-6 | kapandı | `B4` kural 3; `B2` kural 12; `B7` §8; `B4` kural 4a ve 12'nin iki dalı; `B6` §9, `B2` kural 6, `B3` kural 7, `B7` kural 3 ve örneklerin varsayımları. |
| S-2 · S-3 · S-6 | kapandı | `B1` kural 12 (yaş hariç aralıklar çıkarılarak; metin için Y-3) · `B4` kural 14'ün notu · `01-BUTUNLUK` §2'nin kalemi. |

### 7.2 · Yeni bir sorun açıyor mu

**Y-1 · Kopma tanımı susan ardılı dışarıda bırakıyor; anlam Babel-a'dan ayrılıyor — önemli**

- **Yer:** `v2/bilesen/B4-YOL.md:196` (kural 18) · `:378` (§13 madde 18).
- **Ne yanlış:** kural 18 kopmayı, ardılın bağı KULLANILMAZ olunca ya da ardıl silinince sayıyor; ilanın ömrüyle aday dışı kalmayı saymıyor. Susan ardılı (ölmüş, uzaklaşmış ya da kanal kilidinde) önce ilanın ömrü bırakır: 3,5 · a, en çok 7,7 s. Bağ ise ancak ~30 s'de KULLANILMAZ olur (`d_f` `DF_UNUT_S`'de tanımsızlaşır; `d_r`'nin 0'a inmesi 16 zaman aşımı, ~36 s) ya da komşu silinir (`T_SILME`, 30 s). O anda K artık ardıl değildir. Susan ardıl için kopma hiç beyan edilmez, ardından rota kuruldu da gelmez.
- **Babel-a'da sıra tersi:** susan bir sonraki atlamanın maliyeti IHU tutma süresiyle ~42 s'de ∞ olur (3,5 × 12 s), rota 56 s'de sona erer (3,5 × 16 s). Kopma, rota hâlâ seçiliyken beyan edilir (`protokoller/babel.py:242–247`, `:803–846`, `:897–911`; `babel_bicim.py:106–109`).
- **Sonuç:** aynı fiziksel olay iki protokolde farklı sayılıyor. Bu, ön-kayıtlı kopma ölçülerinde (protokolün algıladığı kopma, algılama duyarlılığı, Δ, COR; `v2/06-ON-KAYIT.md:84–85`) yöntemsel bir asimetri; `06` §8'in "gizli asimetri yok" koşuluna dokunuyor.
- **Büyüklük:** küçük. Teşhis (c)'nin kayıtlarında koşu başına, penceredeki sayaçlarla: Babel-a 1,9 (ikiz) · 6,5 (birincil) kopma beyan ediyor; fiziksel kopma 3,8. DESPARETE'nin sayısı sıfıra yakın kalırsa kol "beyan etmiyor" diye etiketlenir ve Δ boş döner (`sim2/gozlem/karar.py`).
  - Komut: `py -3.11 -I kopma_sayisi.py arsiv/teshis/faz5_2_rakip_cizgisi_2026-11-15`.
  - Betik `kayit_{ikiz,birincil}.json`'daki her satırın `sayaclar` sözlüğünden `kopma_algilanan_pencere`, `kopma_fiziksel_pencere` ve `rota_kurtarildi_pencere`'yi protokol başına ortalar.
- **Öneri** (karar): ardılın ilanının ömrüyle aday dışı kalmasını da kopma saymak. DESPARETE susan komşuyu bu yolla tanır; Babel-a'da bu iş komşunun maliyetinindir. S'ye düşmek, ∞ ilan, uygulanamaz ilan ve daha iyi sınıfa geçiş yine kopma değildir. Ya da tanımı korumak ve farkı Aşama 4'ün beklentisine yazmak. Değişiklik tek bir cümle ve §13 madde 18.

**Y-2 · `v2/18` §2.4'ün tablosu dipnotla bölünmüş — küçük**

- **Yer:** `v2/18-YENI-TASARIM.md:529–531`.
- **Ne yanlış:** dipnot tablonun iki satırı arasına girmiş; "eğim + geri yasağı + sınırlı yükselme" satırı tablodan kopuk kalıyor.
- **Öneri:** dipnotu tablonun altına almak.

**Y-3 · B1'de `d_f`'nin süresi üç yerde eski ifadeyle — küçük**

- **Yer:** `v2/bilesen/B1-KOMSU-VE-BAG.md:53` (§4) · `:141` (§8) · `:234` (§13 madde 6).
- **Ne yanlış:** üçü de "o bildirimden beri `DF_UNUT_S` geçti", "`DF_UNUT_S`'den sonra" diyor. Kural 12 artık yaşı hariç aralıklar çıkarılarak ölçüyor.
- **Öneri:** "yaşı (hariç aralıklar çıkarılarak) `DF_UNUT_S`'yi aşınca". Sınama 6'ya, hariç aralıkta yaşın işlemediğini denetleyen bir madde.

**Sorunlar (bulgu değil):**

- **Kural 10a'nın kapsamı daraldı.**
  - Kararlı durumda FD maliyetime eşittir. Aynı turdaki uygulanamaz komşunun `C_j`'si FD'den küçük olamaz; koşul yalnız [FD, C) bandını (maliyetim bu turda yükseldiyse) ve eski turlu ilanları bırakır.
  - 27 Kasım ekinin asıl durumu artık kapsanmıyor: karıştırılan ardıl tek aday, benden pahalı ama temiz bir kardeş dal var.
  - Kapanış bunu yazıyor ("kazancı küçük, ama artık zararsız"). Ama B4 §1 kural 10a'yı hâlâ o kayba karşı sunuyor. "En çok ~0,011" ise (B4 §15, `18` §2.4 eki, §2.5) yeni koşulun ancak bir kısmına ulaşabileceği bir üst sınır. Ne kadarına ulaştığı ölçülemedi: kayıt hedefin ve kararı verenin ilan ettiği maliyeti tutmuyor. B4 §1 ve §15'e ve `18` §2.4–2.5'e yazılması yeter.
  - Kardeş dalları korumak istenirse (seçenek, gerekli değil): son birkaç saniyede bana veri getiren komşuyu dışlamak. B1 bunu `cerceve_duyuldu`'dan görüyor ve bir çıktı olarak verebilir; kalan torun hedeflerini yeni bekleme bölümde bir istekle sınırlar.
  - Maliyetim yükselip alt ağacım henüz yeni ilanımı almamışken koşul kısa süre alt ağaca da izin verebilir; bekleme bunu da bir istekle sınırlar.
- **Kilitten sonraki bayat selamlar.** Bayat selamlar bit 1 taşır. Kilitten önce biti 0 bilinen düğümde alıcı kısa bir bildirim aralığı açar ve olay selamıyla kapatır. Bayat selamların örnekleri bu aralığın 3 s'lik öne çekmesine düşer; `d_r`'nin kısa süreli iyimserliğini büyük ölçüde siler. Alıcıda bağ birkaç milisaniye S olabilir. Zararsız; tanıda görülebilir.
- **Tur artık daha yavaş yayılıyor.** Ö-1'den sonra yeni tur, istek yolu dışında planlı selamlarla (atlama başına en çok ~2,2 s) yayılıyor; eski turlu ilanlar daha uzun kalıyor. Kural 10a'nın eski turlu ilan durumu bu geçişlerde çalışabilir. Düğüm başına `YOK_SAYMA_S`'de bir istekle sınırlı ve tur artışı artık olay selamı doğurmuyor. B4 §13'teki "tur artışının sebebe göre sayısı" bunu gösterir.

### 7.3 · Hüküm

**Engelleyici bulgu kalmadı.** E-1, Ö-1, Ö-2, Ö-3, Ö-5 ve K-1…K-6 kapandı. Ö-4 kural olarak yazıldı; anlamı Y-1'de. Dondurmadan önce:

1. **Y-1:** kopmanın tanımı (karar; tek cümle ve §13 madde 18).
2. **Y-2 ve Y-3:** metin düzeltmeleri.
3. **Kural 10a:** daralan kapsamının B4 §1, §15 ve `18` §2.4–2.5'e yazılması.

Bunlar yapılınca tasarım dondurulmaya ve kodlanmaya hazır. Değişiklikler tek bir tanım ve metinlerden ibaret olduğu için yeni bir okuma gerekmez.
