# BAŞLANGIÇ — bu projede çalışacak yeni ajan için

> Yürütücü bu dosyayı yeni bir ajana ilk mesaj olarak verir. Güncel: 17 Kasım 2026 (Faz 5-3'ün kodlamasının devri). Durum ve plan yalnız `v2/12`de tutulur; burada yalnız giriş için gereken kadarı var. Önceki sürümler `arsiv/DEVIR-PROMPT-*.md` (bir öncekisi `arsiv/DEVIR-PROMPT-2026-10-19.md`).
>
> **19 Kasım notu:** bu devirden sonra tasarım değişti (`v2/17` T-2, T-11, T-12, T-13: vazgeçme tetiği, maliyet eğimi ve döngü bekçisi, açlık ve tur kalktı). §0'daki görev ve KK-04'ün tanımı 17 Kasım'ındır; güncel durum yalnız `v2/12`de.

## 0 · Bu devrin görevi (17 Kasım 2026, Faz 5-3: kodlama)

Faz 5'in ürünü DESPARETE'nin yeni sürümüdür. İlk iki aşama bitti, üçüncüsü başladı:

- **5-1 hâkimiyet** ✓ (14 Kasım): yürütücü v0.4.1'i öğrendi.
- **5-2 araştırma ve öğrenim** ✓ (17 Kasım): dört teşhis ölçümü (`arsiv/teshis/faz5_2_*`); tasarım kararları, protokolün kimliği ve üç ilke `v2/17-TASARIM-KARARLARI.md`de (T-1…T-20); bağımsız denetimden geçti (`arsiv/denetim/DENETIM-RAPORU-5-2-2026-11-17.md` ve kapanışı).
- **5-3 geliştirme** başladı: kararlar `v2/kural/KK-00…KK-05` kural kâğıtlarına çevrildi; bağımsız denetim iki okumada "kodlamaya engel yok" dedi (`arsiv/denetim/DENETIM-RAPORU-KURAL-2026-11-17.md` · `…-ikinci.md` · `DENETIM-KURAL-KAPANIS-2026-11-17.md`). **Sıradaki iş kod.**

**İş bölümü (17 Kasım):** tasarım kararları yürütücünündür (`17`). Kural kâğıtlarını ve kodu sen yazarsın; yürütücüye sade anlatır, onayını alırsın. Bir kâğıt kararı değiştirecekse önce yürütücüye sorarsın.

İlk oturumda:

1. **Projeye ve tasarıma hâkim ol.** §4'teki belgeleri ve kodu öncelik sırasıyla oku (harita, zorunlu liste değil). Özellikle:
   - `v2/17` ve `v2/kural/` (her kuralın hangi karara dayandığı);
   - iki denetim raporu ve kapanış (neden böyle yazıldığı; açık bulgular);
   - protokol arayüzü: `v2/05`, `v2/13`, `sim2/gozlem/`, `sim2/kosum/kontrol.py` ve `dugum.py`'nin bekletme tamponu;
   - `protokoller/babel.py` (aynı arayüzün çalışan örneği) ve `protokoller/desparete.py` (v0.4.1'in yapısı, geçidin kimliği, geri iz).
2. **Kâğıtları kodla karşılaştırarak oku:** her kuralın hangi kancada ve hangi yapıda gerçekleneceğini çıkar; belirsizlik ya da çelişki görürsen not et.
3. **İlk cevapta hiçbir şeyi değiştirme** (dosya, ölçüm, commit komutu yok). Yürütücüye Türkçe ve kısa:
   - anladıkların (protokolün çalışma mantığı, kâğıtların özü);
   - kodlama planın (aşağıdaki iskelet üzerinden, kendi değerlendirmenle);
   - açık bulguların nerede kapanacağı ve yürütücünün vermesi gereken kararlar (Y-6);
   - neyi doğruladığın, neyi varsaydığın.

   Sonra dur; onay bekle.

**Kodlama iskeleti** (öneri; sen değerlendir):

1. **Yeni modüller:** `protokoller/desparete5*.py`. v0.4.1'in dosyalarına dokunulmaz; karşılaştırma için kalır. Bayraklar, sınıflar ve başlangıç değerleri `KK-00`'ın tablolarından.
2. **Önce saf parçalar ve birim testleri** (simülatörsüz):
   - KK-01 durum makinesi; denetim raporlarındaki senaryolar teste dönüşür: alıcısı karıştırıcıya çok yakın bağ, girişim alıcısı, kendi karıştırılmam, ASKIDA, dondurmadan çıkış, sebep kümesi, üst süre;
   - KK-02 aralık ve değişim olayları;
   - KK-04 uygulanabilirlik, FD, ∞ ilan, açlık, istek kaydı;
   - KK-05 bekletme ve geri iz;
   - en sonda KK-03.
3. **Simülatöre bağlama:** `kalibrasyon/aodv_uygunluk.py`'nin `_fabrika`sı ve `PROTOKOLLER`; kontrol kancaları hepsi ya da hiçbiri; mimari denetimi; gözlem sözleşmesi testleri (`tests2/test_kontrol_duzlemi.py`, `test_kosum.py`).
4. **Kısa duman koşusu**, sonra ilk ölçüm: karıştırmaya karşı bayraklar kapalı çekirdek, ikizde ve birincil hücrede Babel'e karşı. Beklenti önce yazılır, yürütücünün commit'iyle girer, koşu dondurulmuş kopyadan (§3 madde 3, 6).
5. **Sonra karıştırma katmanı** ve mekanizma başına A/B: `KK-00`'ın sınıfa göre ölçütleri ve tanı kaydı.
6. **Açık bulgular** (`arsiv/denetim/DENETIM-KURAL-KAPANIS-2026-11-17.md`, "İkinci okuma"):
   - Y-3 ve Y-2 kodlarken;
   - Y-1 ve Y-4 ilgili A/B beklentisinden önce;
   - Y-5 uyarlanır aralığın A/B'sinden önce;
   - Y-6 yürütücüye sorulur: kendi "karıştırılıyorum" durumunun üst süresi;
   - Y-7…Y-12 kodla birlikte.
7. **Kâğıt ile kod:** kod kâğıda uyar. Kâğıtta hata ya da boşluk çıkarsa kâğıt düzeltilir ve yürütücüye bildirilir; `17`'yi değiştiren her şey yürütücüye sorulur.

## 1 · Proje

- **Ne:** bir lise öğrencisinin TÜBİTAK 2204-A projesi (Yazılım / Havacılık ve Uzay); proje hedefi **19 Aralık 2026**, resmî son başvuru 4 Ocak 2027. Mühür tarihi 5-3'ten sonra yeniden yazılır; takvim uyarısı yapma.
- **Konu:** karıştırma (jamming) altındaki taktik İHA sürüsünde mesh yönlendirme. Sürü telemetrisini yer istasyonuna (geçit) taşır, komutlar ters yönde gider; yer ve hava karıştırıcıları bağları bozar ya da kanalı kilitler.
- **İki katkı:**
  1. taban protokollerin bu koşullarda nasıl bozulduğunu gerçekçi bir simülasyonda ölçmek;
  2. bu çalışmada önerilen **DESPARETE** protokolünü karıştırma altında daha yüksek teslim sağlayacak şekilde geliştirip ön-kayıtlı istatistikle karşılaştırmak.
- **Kıyas tabanı:** AODV (`AODV-k`), OLSRv2 (`OLSRv2-b`) ve Babel (`Babel-a`, RFC 8966); üçü donmuş (K-239, K-249). Üç geliştirme hücresinde de en güçlüsü Babel.
  - Teşhis (c), 8 tohum, ikiz · birincil · dayanıklılık: Babel 0,930 · 0,663 · 0,554 ↔ v0.4.1 0,785 · 0,567 · 0,453.
  - Hedefler Babel'e göre yazılır (K-252).
- **Ölçüm ortamı:** projenin kendi simülatörü `sim2/` (Python, kesikli olay; 802.11b telsiz, 1:1 referans dünya, 40 İHA).
- **Birincil metrik:** `PDR_açık`, karıştırıcının açık dönemlerinde doğan paketlerin teslim oranı. "Karıştırmaya özgü kazanç" iddiası ancak fark-içinde-fark ve mekanizma kapısıyla kurulur (`v2/06` §0.4.5).

## 2 · Doğrulama ilkesi

- **Hiçbir şeyi doğrulamadan kesin doğru kabul etme.** Bu dosya, `v2/` belgeleri, kural kâğıtları, kod yorumları, karar günlüğü ve önceki ajanların özetleri bayat ya da yanlış olabilir. Bir iddiayı kullanmadan önce kodla, ölçümle ya da birincil kaynakla doğrula; doğrulayamıyorsan varsayım olarak işaretle.
- **Çelişkide ölç.** Belge ile kod çelişirse hangisinin yanlış olduğunu ölçerek bul.
- **Beklenmeyen sonuçta önce sebebi ölç;** parametre oynatıp sonucu tutturma.
- **Emin olmadığını kesin diye sunma;** neyi ölçtüğünü, neyi varsaydığını ayır.
- **Kendi denetimin yetmez:** kural kâğıtlarının kendi içindeki üç denetiminin her biri yeni sorun buldu; bağımsız göz 20 bulgu daha çıkardı. Önemli bir aşama geçişinden önce bağımsız denetimi ayrı bir oturumda yaptır (istemler `arsiv/denetim/`).
- **Gerekçesi görünmeyen bir kural** sorgulanır ve yürütücüye sorulur.

## 3 · Çalışma kuralları (yürütücü kararları)

1. **Dil:** yürütücüyle Türkçe konuşulur; özetler kısa, yeni başlayan birine anlatır gibi sade (terimi ilk geçtiği yerde aç, örnek sayı ver).
2. **Git:** okuma komutları (`status`, `diff`, `log`) serbesttir. Commit, push ve dal işlemleri **yalnız yürütücüdedir**. Komutu mesajın düz metninde ver, soru kutusundan önce; mesaj tek satır, bir blokta tek komut. "Commit ettim" denince `git log` ile doğrula.
3. **Ölçüm süreci (denetim D-05):**
   - Her sayı üretici komutuyla yazılır.
   - Sonucu ya da bir kararı etkileyen her ölçümün ölçütü (`beklenti.md`) ölçmeden önce yazılır ve koşudan önce yürütücünün commit'iyle girer. Öngörüler duman koşusundan önce yazılır; duman sonrası not ayrı bölümde.
   - Sonuçlar ayrı `sonuc.md`ye yazılır; beklentiye dokunulmaz. Kuraldan sonra görülenler ayrı bölümde, karar girdisi değil. Her ölçümden sonra push.
   - Sonuçtan sonra değişen bir ölçüt `v2/06` §10'a yazılır.
4. **Tohumlar:** ana deney tohumları 2000–2039 mühürden önce hiçbir protokolle koşulmaz; geliştirme tohumları 1003–1010.
5. **Protokoller:**
   - Protokol kâhin bilgisi göremez; yalnız `v2/05`'in sözleşmesindekini okur (`KK-00` "gözlemin kullanımı").
   - Rakip protokoller kaynağına sadık kalır ve senaryoya göre ayarlanmaz; negatif sonuç gizlenmez.
   - Taban protokoller donmuştur (`tests2/test_donma.py`).
6. **Uzun koşu** (~30 dk üstü):
   - Süresini önceden söyle; iki ağır işi aynı anda koşma (12 mantıksal çekirdek, havuz 8 işçi; tam test takımı da ağırdır). Arka plan işinden önce süreç listesine bak.
   - Uzun koşu dondurulmuş kod kopyasından yapılır: `py -3.11 arsiv/teshis/faz4_2026-09-26/dondur.py <klasör>`. Kopyanın commit'le birebir olduğunu dosya özetleriyle doğrula (`kopya_ozet.txt`).
   - Birden çok uzun adım bir kabuk betiğinde sırayla koşar; her adımın saati `zaman.txt`e; her adım 8 saatin altında.
   - Uzun koşudan önce kısa bir duman koşusuyla aleti sına; ham veriyi analizden önce diske yaz.
7. **Simülatörün davranışını değiştiren** her değişiklikten sonra regresyon ve mimari denetimi koşulur; tam test takımı iş kapanışında.
8. **Dosyalar:** dosya silinmez; eskiyen belge `arsiv/`e taşınır. Paket kurulmaz; indirme yürütücünün izniyle yapılır.
9. **Kararlar:**
   - Proje ve yöntem kararları `v2/kayit/KARAR-GUNLUGU.md` ve `v2/04-KARARLAR.md`de; DESPARETE'nin tasarım kararları `v2/17`de (`T-n`), kuralları `v2/kural/`de (`KK-n`). Kod yorumları bunlara atıf verir.
   - Durum değişince yalnız `v2/12` güncellenir.
10. **Belge üslubu:** belgeler yürütücünün kendi sesiyle yazılır: kararlar birinci tekil, işler edilgen. "Yürütücü", "ajan", "öğrenci" ve "X şöyle dedi" kullanılmaz. Bilgi düzeyinde; emoji yok. Yapay zekânın kullanımı README'deki gibi genel anlatılır; ayrıntılı katkı tablosu yok. Bu yönerge ve sohbet mesajları kuralın dışındadır.
11. **Gerçekçilik esastır:** bir ölçütle gerçekçilik çatışırsa gerçekçi olan seçilir ve gerekçesi yazılır (K-185).
12. **Kusurun ele alınışı:** bilimsel güvenilirliği bozan zafiyet düzeltilir. Savunulabilir bir seçim için simülatör sarsılmaz; her sorun bulgu diye yazılmaz. Tek protokolün sonucundan sınıf yargısı kurulmaz.
13. **Faz 5-3'te çalışma biçimi:**
    - DESPARETE özgündür: mevcut bir protokolü alıp üstüne ekleme yaparak sunulmaz; özellik alınabilir, kaynağı yazılır (`17` kimlik, "Ödünç" satırları).
    - Tasarım kararları yürütücünündür. Kâğıtları ve kodu sen yazarsın; her kâğıdı ve önemli kodu sade, örnekli ve kısa anlatır, onay alırsın. Kontrolü tek kısa soruyla yap.
    - Karar gerektiğinde seçenekleri artı ve eksileriyle, önerinle sun; yürütücünün kendi fikrine alan bırak.
    - Ölçüm ve kayıt disiplini aynen sürer.

## 4 · Okuma haritası

**Belgeler** (önce bunlar):

| öncelik | belge | ne için |
|---|---|---|
| 1 | `v2/17-TASARIM-KARARLARI.md` | protokolün kimliği, üç ilke, T-1…T-20, §7 açılış listesi |
| 1 | `v2/kural/KK-00…KK-05` | kurallar, formüller, başlangıç değerleri, bayraklar, sınıflar, A/B ölçütleri, tanı kaydı |
| 1 | `arsiv/denetim/DENETIM-KURAL-KAPANIS-2026-11-17.md` ve iki rapor | kâğıtların neden böyle yazıldığı; açık bulgular |
| 1 | `v2/12` · `v2/04` | durum ve plan · geçerli proje kararları |
| 2 | `v2/05` · `v2/13` | protokolün görebildiği ve yapabildiği (sözleşmeler) |
| 2 | `arsiv/teshis/faz5_2_*/sonuc.md` | dört teşhis: kayıp anatomisi · seçenekler ve iletim · rakiplerin çizgisi · karıştırma işaretleri |
| 2 | `protokol_kaynaklari/faz5_arastirma_2026-10-21/NOTLAR.md` · `protokol_kaynaklari/rfc8966_babel.txt` | seçenekler ve kaynaklar · döngüsüzlüğün kaynağı |
| 3 | `v2/06` · `v2/08` | ön-kayıt · evre metrikleri |
| 3 | `v2/01` · `v2/07` · `v2/14` | problem ve kapsam · simülatör · referans dünya |
| 3 | `arsiv/denetim/DENETIM-RAPORU-5-2-2026-11-17.md` ve kapanışı | 5-2'nin bağımsız denetimi |
| gerektikçe | `v2/kayit/KARAR-GUNLUGU.md` | bir `K-xxx` atfının tarihçesi |

**Kod:**

| alan | dosya | ne için |
|---|---|---|
| protokol yüzeyi | `sim2/gozlem/pencere.py` · `protokol.py` · `karar.py` · `kontrol.py` | gözlem, kancalar (`iletim_sonucu` ve `cerceve_duyuldu` niyet döndüremez), `Karar.beklet`, `KontrolIstegi`, `Uyandirma`, `MesajBicimi` |
| kontrol düzlemi ve tampon | `sim2/kosum/kontrol.py` · `dugum.py` · `kosu.py` | kancaların çağrılma sırası; bekletme tamponu (yalnız uyanmadan sonra dökülür, K-135); kanal meşgul integrali |
| çalışan örnek | `protokoller/babel.py` · `babel_bicim.py` | aynı arayüzle yazılmış Babel: selam geçmişi, FD, sıra isteği, zamanlayıcılar |
| eski sürüm | `protokoller/desparete.py` ve `desparete_*.py` | v0.4.1: geçidin kimliği kurucudan, geri iz (V11), bayrak profilleri |
| bağlama | `kalibrasyon/aodv_uygunluk.py` | `_fabrika`, `PROTOKOLLER` |
| aletler | `kalibrasyon/kayip_anatomisi.py` · `karistirma_isaretleri.py` · `kahin.py` | kayıp anatomisi · karıştırma işaretleri kaydedicisi · kâhin |
| denetim | `kalibrasyon/mimari_denetimi.py` · `regresyon_satirlari.py` · `tests2/test_donma.py` | yapı ve köken denetimi · regresyon · donmuş dosyalar |
| analiz | `analiz/satir.py` · `hucre.py` | `PDR_açık`, ikincil metrikler, istatistik planı |

## 5 · Bilinmesi gereken tuzaklar

- **İki dünya:** `Konfig()` varsayılanı eski 1:50 dünyadır; deneyler **referans dünyada** (`referans_2026`) koşar: `--dunya referans_2026` ya da `DESPARETE_DUNYA=referans_2026`.
- **Python 3.11:** bütün komutlar `py -3.11` ile; `PYTHONIOENCODING=utf-8`. `Pool` kullanan betikte `if __name__ == "__main__":`.
- **Satır sonları karışıktır (CRLF/LF) ve korunur:** `v2/*.md`nin çoğu CRLF. Write aracı LF yazar; CRLF dosyayı Python'la bayt düzeyinde düzenle (yama betiğini dosyaya yaz, heredoc'a uzun Python koyma). Satır sonunu Python'la bayt sayarak doğrula.
- **Kancaların sırası:** MAC vazgeçince simülatör önce `iletim_sonucu`yu, sonra `iletim_basarisiz`ı çağırır (`sim2/kosum/kosu.py`).
- **Kontrol kancaları hepsi ya da hiçbiri;** `iletim_sonucu` ve `cerceve_duyuldu` isteğe bağlıdır. Kendi selamı olan protokol `kosum_beaconi = False` der; `gozlem.komsular` o zaman boştur.
- **Bekletme tamponu** ortak tavanlıdır (64 paket, 30 s, dolunca en eski düşer); protokol kendi süre sınırını paket kimliğiyle tutar.
- **Sürekli karıştırıcı sınıfında `gecis_anlari` boş döner;** açılıp kapanma anı evre örneklemesiyle bulunur (`kalibrasyon/karistirma_isaretleri.py`).
- **Aletle ölçerken birebirlik:** bir kaydedici ya da sarmalayıcı ekleyince satırı önceki bir kayıtla (PDR, sayaçlar) karşılaştır; teşhis (d)'deki uygulamaya bak.
- **MAC deneme sayısı:** `yeniden_deneme_siniri` yeniden deneme sayısıdır (toplam = sınır + 1, en çok 7 iletim, K-223).
- **Kâhin tavan değildir** (K-110, K-248); kâhin bilgisi protokole girmez.
- **Arka plan kabuğu ~9,5 sa'te kesilebilir:** uzun işi < 8 sa'lik adımlara böl, adım betiği biten adımı atlasın.
- **Gürültülü tek koşu:** kısa pencerede tek tohumun PDR'si ±0,15 oynar; tek tohum karar değildir.
- **Mimari denetiminde "ihlal" ile "bulgu" ayrıdır:** çıkış koduna bak. Protokol yeni bir gözlem alanı okumaya başlarsa o alanın hata parametresi DUYARSIZ kalamaz (D17).

## 6 · Doğrulama — referans dünyada geçerli olanlar

Bütün komutlar `py -3.11` ve `PYTHONIOENCODING=utf-8` ile koşulur.

| komut | beklenen | süre |
|---|---|---|
| `-m pytest tests2 -q` | `1101 passed` (17 Kasım) | ~20 dk |
| `kalibrasyon/mimari_denetimi.py` | ihlal 0 | < 1 dk |
| `-u kalibrasyon/regresyon_satirlari.py uret <etiket>` · `karsilastir k249 <etiket> …` | ilan edilen farklar dışında BİREBİR | ~80 dk + < 1 dk |
| `arsiv/dogrulama/kayit_indeksi.py --kontrol` | indeks güncel | saniyeler |
| `-u kalibrasyon/kayip_anatomisi.py --dunya referans_2026 [--sinif yok] --kol formasyon --protokoller <p> --tohumlar <…> --kayit <json>` | düşme sebepleri, ikincil metrikler, veri denemesinin sonucu | 8 işçide adım başına ~1–3,7 sa (AODV-k en uzun) |
| `-u kalibrasyon/karistirma_isaretleri.py --dunya referans_2026 --sinif yok\|surekli --protokoller babel[@…] --tohumlar <…> --kayit <json>` | karıştırma işaretlerinin dağılımları; satır kayıp anatomisiyle birebir | 8 işçide adım başına ~1,8–2,1 sa |
| `-u kalibrasyon/aodv_uygunluk.py --dunya referans_2026 --desen yere_toplama --protokol <p>` | U1 (`v2/04` §5) | saatler |
