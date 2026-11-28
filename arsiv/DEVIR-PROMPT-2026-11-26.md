# BAŞLANGIÇ — bu projede çalışacak yeni ajan için

> Yürütücü bu dosyayı yeni bir ajana ilk mesaj olarak verir. Güncel: 26 Kasım 2026 (Faz 5-3, yeniden tasarım, Aşama 2.5: B5 iletim kararı). Durum ve plan yalnız `v2/12`de tutulur; burada yalnız giriş için gereken kadarı var. Önceki sürümler `arsiv/DEVIR-PROMPT-*.md` (bir öncekisi `arsiv/DEVIR-PROMPT-2026-11-17.md`: eski tasarımın kodlanma devri, artık geçersiz).

## 0 · Bu devrin görevi

**Nerede duruyoruz (ayrıntısı `v2/12` §1 ve §1.3):**
- Faz 5'in ürünü DESPARETE'nin yeni sürümüdür.
- **5-1 hâkimiyet** (14 Kasım) ve **5-2 araştırma** (17 Kasım) bitti.
- **5-3 geliştirme** iki dönemden geçti:
  - **17–24 Kasım, ilk tasarım:** kararları `v2/17`, kuralları `v2/kural/KK-*`, kodu `protokoller/desparete5*.py`. Dört ölçümde üç sürüm denendi; her biri bir sorunu çözerken başkasını açtı.
  - **24 Kasım'dan beri, yeniden tasarım** (K-253): protokol baştan, bileşen bileşen ve eksiksiz tasarlanıyor. Yöntem, aşamalar, hedef ve eksiksizlik listesi `v2/18`de, kural kâğıtları `v2/bilesen/`de.
- **Yeniden tasarımın aşamaları:**
  - Aşama 1 · zemin: tamam (hedef, kısıtlar, kanıt envanteri, mimari iskelet).
  - Aşama 2 · bileşenler: B1 komşu ve bağın ölçüsü, B2 karıştırma kanıtı, B3 bağın durumu ve B4 yol onaylandı (24–26 Kasım). **Sırada B5 iletim kararı**, sonra B6 kontrol iletileri ve B7 bekletme ve komut.
  - Aşama 3: bütünlük denetimi, bağımsız denetim, donma.
  - Aşama 4: kod ve tek büyük ölçüm.
- **Bugünkü kod yeni tasarımı içermez.** Kodda iki önceki sürüm var: v0.4.1 ve 5-3'ün ilk tasarımı. Yeni tasarım Aşama 4'te yeni modüllerle yazılır.

**İş bölümü:**
- Proje, kapsam ve gerçekçilik kararları yürütücünündür; her bileşenin **ana seçeneği** de onun kararıdır.
- Seçenekleri sen hazırlarsın ve sade anlatırsın.
- Kural kâğıtlarını ve kodu sen yazarsın. Kâğıttaki teknik alt kararlar senindir: gerekçesini ve seçilmeyen yolları kâğıda yazar, onayda kısaca bildirirsin.
- Onaylanmış bir kararı yeniden tartışmaya açma. Yeni bir kanıt onu sarsıyorsa kanıtla birlikte yürütücüye getir.

**İlk oturumda:**

1. **Projeye hâkim ol.** §4'teki okuma haritasını öncelik sırasıyla oku, belgeleri ve kodu birlikte.
   - Yeni tasarımın tamamını oku: `v2/18`, `v2/bilesen/00-DIZIN.md` ve B1–B4 kâğıtları, baştan sona.
   - Sıradaki işin (B5) kanıtını ve sözleşmelerini oku: §4'teki "B5 için" satırları.
   - Özetten iş yapma. Bir iddiayı belgeden aktarmadan önce birincil kaydına bak: `sonuc.md`, karar günlüğü, inceleme, kod. Örnek: `v2/18`'in iki satırı 24–26 Kasım arasında kopyanın kanalı boğduğunu K-238'e dayandırıyordu. K-238 ise çöküşün ~%90'ını yinelenen RREQ seline bağlıyor; 26 Kasım'da düzeltildi.
2. **Doğrula:**
   - `git log --oneline -5` ve `git status --short` (çalışma ağacı temiz olmalı);
   - kayıt indeksi (§6);
   - istersen mimari denetimi (< 1 dk).
   Kod 20 Kasım'dan beri değişmediği için tam test takımını (~20 dk) koşman gerekmez.
3. **İlk cevabında hiçbir şeyi değiştirme:** dosya, ölçüm ya da commit komutu yok. Yürütücüye Türkçe, sade ve kısa olarak şunları anlat:
   - **projeden anladıkların:** problem ve amaç, simülatör ve referans dünya, rakipler ve ölçüt, ve yeni tasarımın mantığı. B1–B4'ün her birini birkaç cümleyle, terimleri açarak anlat;
   - **kalan yol haritası:** B5, B6, B7 → Aşama 3 → Aşama 4 → Faz 5.7 → Faz 6 (ön-kayıt, mühür) → Faz 7 (ana deney, yazım); kısa;
   - **şimdi ne yapacağız:**
     - B5'in sorusu ne;
     - hangi ölçülmüş kanıta dayanacak;
     - aklındaki seçenek aileleri (karar vermeden);
     - kararın girdisi eksikse kısa bir teşhis ölçümü gerekip gerekmediği;
   - **neyi doğruladığın, neyi varsaydığın;** gördüğün çelişkiler.

   Sonra dur ve onay bekle; yürütücünün onayıyla devam edilir.

## 1 · Proje

- **Ne:** bir lise öğrencisinin TÜBİTAK 2204-A projesi (Yazılım / Havacılık ve Uzay). Proje hedefi 19 Aralık 2026, resmî son başvuru 4 Ocak 2027. Mühür tarihi 5-3'ten sonra yeniden yazılır. Takvim uyarısı yapma, zamana takılma.
- **Konu:** karıştırma (jamming) altındaki taktik İHA sürüsünde mesh yönlendirme. Telemetri İHA'lardan yer istasyonuna (geçit, düğüm 0) gider, komutlar ters yönde. Yer ve hava karıştırıcıları bağları bozar ya da kanalı kilitler.
- **Amaç:** projenin ürünü bu çalışmada önerilen **DESPARETE** protokolüdür. Simülatör, onu gerçek fiziğe ve saha koşullarına yakın bir ortamda rakiplerle karşılaştırmak içindir. Taban protokollerin bu koşullarda nasıl bozulduğu ikinci, bağımsız katkıdır.
- **Kıyas tabanı:** `AODV-k`, `OLSRv2-b`, `Babel-a` (RFC 8966). Üçü de donmuş (K-239, K-249). En güçlüsü Babel: 8 tohumda ikiz 0,930, birincil 0,663, dayanıklılık 0,554. Kâhin birincilde 0,779 (`v2/18` §1.1).
- **Ölçüm ortamı:** projenin kendi simülatörü `sim2/`: Python, kesikli olay; 802.11b, 1:1 referans dünya; 40 İHA, 33 km'lik alan, geçit düğüm 0.
  - Birincil hücre: formasyon, yere toplama, `derin_sizma`, sürekli karıştırıcı, 10 W, 15 s açık · 15 s sessiz.
  - Karıştırıcısız ikiz; dayanıklılık hücresi (10/20); yer karıştırıcılı aile (cephe hattı ya da hedef koruma).
- **Birincil metrik:** `PDR_açık`, karıştırıcının açık dönemlerinde doğan paketlerin teslim oranı.
  - Hedef (`v2/18` §1.1): birincilde Babel'den en az +0,05.
  - "Karıştırmaya özgü kazanç" ancak fark-içinde-fark ve mekanizma kapısıyla kurulur (`v2/06` §0.4.5).
  - Yedi koruma ölçütü: ikizde zarar yok, dayanıklılık, en kötü tohum, sessiz dönem, gecikmenin p99'u, kontrol payı, yer karıştırıcılı aile.

## 2 · Doğrulama ilkesi

- **Hiçbir şeyi doğrulamadan kesin doğru kabul etme.** Bu dosya, `v2/` belgeleri, kâğıtlar, kod yorumları, karar günlüğü ve önceki ajanların özetleri bayat ya da yanlış olabilir. Bir iddiayı kullanmadan önce kodla, ölçümle ya da birincil kaynakla doğrula; doğrulayamıyorsan varsayım diye işaretle.
- **Sabitleri bellekten değil, koddan ya da kayıttan oku.** Dünyaya bağlı sabitlerde konfig varsayılanına değil referans dünyaya bak (`sim2/kanal/dunya.py`). Referans dünyada MAC en çok 7 deneme yapar (yeniden deneme sınırı 6, K-223) ve TTL 64'tür. Konfigürasyon varsayılanı farklıdır; geçmişte iki kez yanlış sabit yazıldı.
- **Kullanıcıya söz ya da fikir atfetmeden önce kayda bak.** Belgelerdeki kararların çoğu, sunulan seçeneklerin kabulüdür.
- **Çelişkide ölç.** Belge ile kod çelişirse hangisinin yanlış olduğunu ölçerek bul. Beklenmeyen sonuçta önce sebebi ölç; parametre oynatıp sonucu tutturma.
- **Tek tohum ve duman koşusu karar girdisi değildir.** Ölçülmemiş bir şeyi bulgu diye yazma.
- **Kendi denetimin yetmez:** önemli bir aşama geçişinden önce bağımsız denetim ayrı bir oturumda yapılır. Aşama 3'te yeni bir istem yazılır; eski istemler `arsiv/denetim/`de.

## 3 · Çalışma kuralları (yürütücü kararları)

1. **Dil:** yürütücüyle Türkçe konuşulur. Yeni başlayan birine anlatır gibi sade yaz: terimi ilk geçtiği yerde aç, örnek sayı ver, kısaltma yığma. Kontrolü tek kısa soruyla yap.
2. **Git:**
   - Okuma komutları (`status`, `diff`, `log`, `show`) serbesttir. Commit, push ve dal işlemleri **yalnız yürütücüdedir**.
   - Komutu mesajın düz metninde, soru kutusundan önce ver. Her bloğa tek komut koy: `git add <dosyalar>` · `git commit -m "<tek satır>"` · `git push`.
   - Mesaj tek satırdır ve Co-Authored-By satırı taşımaz (yürütücünün commit'leri böyle).
   - "Commit ettim" denince `git log` ile doğrula. Her ölçümden sonra push.
3. **Ölçüm süreci (denetim D-05):**
   - Her sayı üretici komutuyla yazılır.
   - Sonucu ya da bir kararı etkileyen her ölçümün beklentisi (`beklenti.md`: sorular, karar kuralı, öngörüler) ölçmeden önce yazılır ve koşudan önce yürütücünün commit'iyle girer.
   - Öngörüler duman koşusundan önce yazılır. Duman notu beklentinin sonunda ayrı bir bölümdür ve ayrı commit'le girer; öngörüler ve karar kuralı değişmez.
   - Sonuç ayrı `sonuc.md`ye yazılır; beklentiye dokunulmaz. Kuraldan sonra görülenler ayrı bölümdedir ve karar girdisi değildir.
   - Sonuçtan sonra değişen bir ölçüt `v2/06` §10'a "sonuçtan sonra" diye yazılır.
4. **Tohumlar:** geliştirme 1003–1010. Ana deney tohumları 2000–2039 mühürden önce hiçbir protokolle koşulmaz.
5. **Protokoller:**
   - Protokol kâhin bilgisi göremez; yalnız `v2/05`'in sözleşmesindekini okur. `olculen_gurultu_w` karara girmez (K-227, mimari denetimi D17).
   - Bileşenin okuduğu ve okumadığı alanlar `bilesen/00-DIZIN.md`'nin "gözlemin kullanımı" tablosunda yazılır.
   - Rakipler kaynağına sadıktır, donmuştur (`tests2/test_donma.py`) ve senaryoya göre ayarlanmaz.
6. **Uzun koşu** (~30 dk üstü):
   - Süresini önceden söyle. İki ağır işi aynı anda koşma (12 mantıksal çekirdek, havuz 8 işçi). Arka plan işinden önce süreç listesine bak.
   - Uzun koşu dondurulmuş kopyadan yapılır: `py -3.11 arsiv/teshis/faz4_2026-09-26/dondur.py <klasör>/kopya`. Kopyanın commit'le birebir olduğunu `arsiv/teshis/faz4_2026-09-26/kopya_ozet.py <kopya> <commit> > <klasör>/kopya_ozet.txt` ile göster.
   - Adımlar bir kabuk betiğinde (`kosu.sh`) sırayla koşar; her adımın saati `zaman.txt`e yazılır ve her adım 8 saatin altında kalır. Makinenin uyanık kalmasını iste.
   - Önce kısa bir duman koşusuyla aleti sına; ham veriyi analizden önce diske yaz.
7. **Simülatörün davranışını değiştiren** her değişiklikten sonra regresyon ve mimari denetimi koşulur. Tam test takımı iş kapanışında koşulur.
8. **Dosyalar:** dosya silinmez; eskiyen belge `arsiv/`e (v2 belgeleri `v2/arsiv/`e) taşınır. Paket kurulmaz; indirme yürütücünün izniyle yapılır.
9. **Kararlar ve belgeler, her bilgi tek yerde:**
   - **Durum ve plan:** yalnız `v2/12`.
   - **Proje ve yöntem kararları:** `v2/kayit/KARAR-GUNLUGU.md` (K-xxx, son K-253) ve geçerli hâlleri `v2/04`. Günlüğe kayıt eklenince indeks üretilir: `py -3.11 arsiv/dogrulama/kayit_indeksi.py`.
   - **DESPARETE'nin güncel tasarımı:** bileşen kararları `v2/18`de, kuralları `v2/bilesen/`de. Değerler, bayraklar ve gözlemin kullanımı yalnız `bilesen/00-DIZIN.md`'de.
   - **Önceki tasarım:** `v2/17` (T-n) ve `v2/kural/KK-*`. Bugünkü kodun belgesidir ve yeni tasarım donunca arşive gider.
10. **Belge üslubu:**
    - Belgeler yürütücünün kendi sesiyle yazılır: kararlar birinci tekil ("kararım"), işler edilgen ("ölçüldü").
    - "Yürütücü", "ajan", "öğrenci" ve "X şöyle dedi" kullanılmaz. Bilgi düzeyinde yazılır; emoji yok.
    - Belgelere yapay zekânın rolü yazılmaz; README'deki genel beyan yeterlidir, yeniden açma.
    - Bu yönerge ve sohbet mesajları bu kuralın dışındadır.
11. **Gerçekçilik esastır:** bir ölçütle gerçekçilik çatışırsa gerçekçi olan seçilir ve gerekçesi yazılır (K-185).
12. **Kusurun ele alınışı:**
    - Bilimsel güvenilirliği bozan zafiyet düzeltilir.
    - Savunulabilir bir seçim için simülatör sarsılmaz; her sorun bulgu diye yazılmaz.
    - Tek protokolün sonucundan sınıf yargısı kurulmaz.
13. **Yeniden tasarımda çalışma biçimi** (K-253, `v2/18` "Yöntem"):
    - **Her bileşende aynı adımlar:**
      - sorun ve ölçülmüş kanıt;
      - en az iki seçenek, bedelleriyle;
      - yürütücünün kararı: `v2/18`'in bileşen bölümüne yazılır;
      - kural kâğıdı: `v2/18`'in 17 maddelik eksiksizlik listesinin hepsi cevaplanır;
      - sade anlatım ve onay;
      - durum işaretleri ve commit komutu.
    - **Onaydan sonra işaretlenenler:** kâğıdın "Durum" satırı · `00-DIZIN`'in kâğıt tablosu (sıradaki bileşen "sırada") · `v2/18`'in durum satırı ve bileşen bölümündeki "Kâğıt" satırı · `v2/12`'nin durum satırı ve §1.3.
    - **Tasarım sırasında A/B yapılmaz.** Bir kararın girdisi eksikse kısa, önceden yazılı bir teşhis ölçümü yapılır (madde 3 ve 6). Örnekleri: `arsiv/teshis/faz5_3_b2_isaretler_2026-11-24/` ve `arsiv/teshis/faz5_3_b3_bag_olculeri_2026-11-25/`. Yapıları beklenti, kaydedici (`olcum.py`), saf işlevler ve sınaması (`isaret.py` · `bag.py`, `sinama/`), `kosu.sh`, `sonuc_hesap.py`, `ek_hesap.py` ve `sonuc.md`'dir. Seçim ve doğrulama yarıları kullanılır: 1003–1006 ve 1007–1010.
    - **Kâğıt yazarken** ödünç alınan kuralları birincil kaynaktan yeniden oku (ör. `protokol_kaynaklari/rfc8966_babel.txt`) ve bölüm numarasını yaz. Önceki kâğıttan kopyalama.
    - **Değerler:** her değerin kaynağını, neyi etkilediğini, küçük ve büyük olursa ne olacağını ve taranıp taranmayacağını `00-DIZIN`'e yaz.
    - **Karar istemeden önce öğret:**
      - kavramı örnek sayılarla anlat;
      - seçenekleri artı ve eksileriyle sun, önerini söyle;
      - yürütücünün kendi fikrine alan bırak.
      Zaman değerlerini sahaya göre sorgular; bir değerin kaynağını ve neyi etkilediğini söyle.
14. **Rapor iskeleti ve hâkimiyet çalışması önerme;** ikisi de işler bittikten sonra yapılır.

## 4 · Okuma haritası

**Belgeler** (önce bunlar):

| öncelik | belge | ne için |
|---|---|---|
| 1 | `v2/12` | durum, plan, Faz 5-3'ün kaydı (§1.3), hesap bütçesi |
| 1 | `v2/18` (tamamı) | yeni tasarım: hedef ve başarı ölçütü, kısıtlar, kanıt envanteri, mimari iskelet ve sözleşme, yöntem, B1–B4'ün sorun–kanıt–seçenek–kararı, eksiksizlik listesi |
| 1 | `v2/bilesen/00-DIZIN.md` · `B1`…`B4` (tamamı) | onaylı kurallar; değerler, bayraklar, gözlemin kullanımı; Aşama 3'e açık kalanlar |
| 1 | `v2/04` · `v2/05` · `v2/13` | geçerli kararlar · protokolün gördüğü · protokolün yapabildiği (sözleşmeler) |
| 1 · B5 için | `v2/18` §1.3 (biliyoruz, bilmiyoruz), §1.4 (B5'in satırı, sözleşme 4–5, olay sırası) · B4 §1, §9, §11 madde 2, §15 · B3 §11 madde 4 · B2 §11 madde 3 | B5'in arayüzü: aday listesi, durumlar, kendi durumum |
| 1 · B5 için | `arsiv/teshis/faz5_3_dongu_kurallari_2026-11-24/sonuc.md` §8 · `faz5_2_anatomi_2026-11-14/sonuc.md` §2, §5 · `faz5_2_secenek_iletim_2026-11-15/sonuc.md` §2, §5 · `faz5_2_isaretler_2026-11-16/sonuc.md` §3 | kayıp nerede: birincilde açık dönem kaybının büyüğü iletimde; karıştırılan alıcıya giden çerçevenin deneme sayısı; Babel'in kaybının alanlara dağılımı |
| 1 · B5 için | `v2/17` T-9, T-14, T-15, T-18, T-20 · `v2/kural/KK-04` kural 13 · `KK-05` · K-238 ve `arsiv/teshis/jarmrout_sel_2026-10-12/inceleme.md` §3 · `protokol_kaynaklari/faz5_arastirma_2026-10-21/NOTLAR.md` §4 · `faz5_3_arastirma_2026-11-19/NOTLAR.md` §3 | önceki tasarımın iletim kararları; kopyanın bedeli (ölçülmedi); fırsatçı iletim |
| 2 | `v2/17` · `v2/kural/KK-00…05` | önceki tasarım; bugünkü kodun belgesi |
| 2 | B2 ve B3 teşhislerinin `beklenti.md` ve `sonuc.md`'si · `arsiv/teshis/faz5_3_yeni_cekirdek_2026-11-19/sonuc.md` · `faz5_3_aclik_2026-11-18/sonuc.md` · `faz5_2_rakip_cizgisi_2026-11-15/sonuc.md` | kâğıtların dayandığı ölçümler; teşhis ölçümünün nasıl yazıldığı |
| 2 | `protokol_kaynaklari/rfc8966_babel.txt` · iki araştırma notu | döngüsüzlüğün ve seçimin kaynağı; seçenekler |
| 2 | `v2/06` §0, §10 · `v2/08` | ön-kayıt (bağlayıcı hükümler, mekanizma kapısı, sonuçtan sonra değişenler) · evre metrikleri |
| 3 | `v2/01` · `v2/07` · `v2/14` · `v2/03` · `v2/02` · `v2/16` | problem ve kapsam · simülatör · referans dünya · yöntem kuralları · kaynaklar · kaynakça |
| 3 | `arsiv/denetim/` (5-2 ve kural kâğıtlarının denetimleri ve kapanışları) | önceki tasarımın neden böyle yazıldığı |
| gerektikçe | `v2/kayit/KARAR-GUNLUGU.md` | bir `K-xxx` atfının tarihçesi |

**Kod:**

| alan | dosya | ne için |
|---|---|---|
| protokol yüzeyi | `sim2/gozlem/pencere.py` · `protokol.py` · `karar.py` · `kontrol.py` | gözlem alanları (30), kancalar, `Karar` (sonraki, beklet, kopyalar, rota, beyan, niyetler), `KontrolIstegi`, `Uyandirma`, `MesajBicimi` |
| paket kararının anı | `sim2/kosum/gonderim.py` (`iletime_basla`, `vazgec`) · `kosu.py` (`_onay_penceresi`) | protokole atlama başına bir kez, geri çekilme bitip çerçeve havaya çıkarken sorulur; MAC aynı komşuya en çok 7 kez dener; vazgeçilen paket düşer (alıcı çözdüyse düşmez); önce `iletim_sonucu`, sonra `iletim_basarisiz` |
| kontrol düzlemi ve tampon | `sim2/kosum/kontrol.py` (`zamanlayicilari_kur`) · `dugum.py` | kancaların sırası; periyodik zamanlayıcının düğüm başına fazı; bekletme tamponu (64 paket, 30 s; yalnız uyanmadan sonra dökülür, K-135); kopya kuyruğu |
| çalışan örnek | `protokoller/babel.py` · `babel_bicim.py` | aynı arayüzle yazılmış Babel: selam geçmişi, FD, sıra isteği, zamanlayıcılar |
| önceki tasarımlar | `protokoller/desparete5*.py` (`desparete5.py` `sonraki_atlama`) · `protokoller/desparete.py` | 5-3'ün ilk tasarımı (KK-*) · v0.4.1 (geçidin kimliği, geri iz V11) |
| bağlama | `kalibrasyon/aodv_uygunluk.py` | `_fabrika`, `PROTOKOLLER` |
| aletler | `kalibrasyon/kahin.py` · `kayip_anatomisi.py` · `karistirma_isaretleri.py` · B3 teşhisinin `olcum.py`'si | kâhin (tavan değil) · kayıp anatomisi · karıştırma işaretleri · kaydedici örneği |
| denetim | `kalibrasyon/mimari_denetimi.py` · `regresyon_satirlari.py` · `tests2/test_donma.py` · `arsiv/dogrulama/kayit_indeksi.py` | yapı ve köken · regresyon · donmuş dosyalar · karar günlüğünün indeksi |
| analiz | `analiz/satir.py` · `hucre.py` | `PDR_açık`, ikincil metrikler, istatistik planı |

## 5 · Bilinmesi gereken tuzaklar

- **İki dünya:** `Konfig()` varsayılanı eski 1:50 dünyadır; deneyler **referans dünyada** koşar (`referans_2026`; `--dunya referans_2026` ya da `DESPARETE_DUNYA=referans_2026`).
- **Python 3.11:** bütün komutlar `py -3.11` ile ve `PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1` ile koşar; `python` başka bir 3.12'yi açar. `Pool` kullanan betikte `if __name__ == "__main__":` gerekir.
- **Satır sonları:**
  - Depoda `core.autocrlf=true`: git LF saklar, çalışma kopyasında var olan dosyaların çoğu CRLF'dir.
  - Var olan dosyada satır sonunu koru. Çok satırlı ya da büyük değişikliği scratchpad'deki bir Python betiğiyle bayt düzeyinde yap; her değişikliğin tam bir kez uygulandığını ve `\r\n` sayısını doğrula. Edit aracı satır sonunu korur.
  - Yeni dosya LF yazılabilir; git normalleştirir. "LF will be replaced by CRLF" uyarısı zararsızdır.
- **Paket başlığına değer yazılamaz** (K-232); yazılabilen yalnız kaynak rotasıdır. Kopya eşinin kimliği ara düğüme görünmez (`v2/13` §07). Gönderenin maliyeti gibi bilgiler ancak kontrol iletisiyle gelir.
- **Kancalar:**
  - Kontrol kancaları hepsi ya da hiçbiridir; `iletim_sonucu` ve `cerceve_duyuldu` isteğe bağlıdır ve niyet döndüremez; işleri bir sonraki niyetli kancada yapılır.
  - Kendi selamı olan protokol `kosum_beaconi = False` der.
- **Sürekli karıştırıcı sınıfında `gecis_anlari` boş döner;** açılıp kapanma anı evre örneklemesiyle bulunur.
- **Aletle ölçerken birebirlik:** kaydedici ya da sarmalayıcı ekleyince satırı kaydedicisiz bir koşuyla (PDR, sayaçlar) karşılaştır. B2 ve B3 teşhislerinin duman notlarında örnekleri var.
- **Kâhin tavan değildir** (K-110, K-248): girişimi görmez, karıştırılan bağları bilir. Kâhin bilgisi protokole girmez.
- **Arka plan kabuğu ~9,5 sa'te kesilebilir:** uzun işi < 8 sa'lik adımlara böl; adım betiği biten adımı atlasın.
- **Gürültülü tek koşu:** kısa pencerede tek tohumun PDR'si ±0,15 oynar.
- **Mimari denetiminde "ihlal" ile "bulgu" ayrıdır:** çıkış koduna bak. Protokol yeni bir gözlem alanı okumaya başlarsa o alanın hata parametresi DUYARSIZ kalamaz (D17). RSSI'nin ve dikey konumun hatası SINANMAMIŞ'tır (`v2/04` §9).
- **Bu dosya ve denetim istemleri git dışıdır** (`.gitignore`); arşiv kopyaları `arsiv/`de izlenir.
- **Bağlam sıkıştırılırsa** devam etmeden önce bu haritadaki belgeleri ve ilgili kodu yeniden oku.

## 6 · Doğrulama — referans dünyada geçerli olanlar

Bütün komutlar `py -3.11` ve `PYTHONIOENCODING=utf-8` ile koşulur.

| komut | beklenen | süre |
|---|---|---|
| `-m pytest tests2 -q` | `1203 passed` (20 Kasım; kod o günden beri değişmedi) | ~20 dk |
| `kalibrasyon/mimari_denetimi.py` | ihlal 0 | < 1 dk |
| `-u kalibrasyon/regresyon_satirlari.py uret <etiket>` · `karsilastir k249 <etiket> …` | ilan edilen farklar dışında BİREBİR (taban `k249`, 87 vaka) | ~80 dk + < 1 dk |
| `arsiv/dogrulama/kayit_indeksi.py --kontrol` | indeks güncel (164 kayıt, 26 Kasım) | saniyeler |
| `arsiv/teshis/faz4_2026-09-26/dondur.py <klasör>/kopya` · `kopya_ozet.py <kopya> <commit>` | kopya commit'le birebir | dakikalar |
| `-u kalibrasyon/kayip_anatomisi.py --dunya referans_2026 [--sinif yok] --kol formasyon --protokoller <p> --tohumlar <…> --kayit <json>` | düşme sebepleri, ikincil metrikler, veri denemesinin sonucu | 8 işçide adım başına ~1–3,7 sa |
| `-u kalibrasyon/karistirma_isaretleri.py --dunya referans_2026 --sinif yok\|surekli --protokoller babel[@…] --tohumlar <…> --kayit <json>` | karıştırma işaretlerinin dağılımları; satır kayıp anatomisiyle birebir | 8 işçide adım başına ~1,8–2,1 sa |

Koşu sürelerinin bütçesi `v2/12` §3'te.
