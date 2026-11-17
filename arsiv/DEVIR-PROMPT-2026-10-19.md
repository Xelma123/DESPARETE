# BAŞLANGIÇ — bu projede çalışacak yeni ajan için

> Yürütücü bu dosyayı yeni bir ajana ilk mesaj olarak verir. Güncel: 19 Ekim 2026 (K-251'den sonra; Faz 5'in devri). Durum ve plan yalnız `v2/12`de tutulur; burada yalnız giriş için gereken kadarı var. Önceki sürümler `arsiv/DEVIR-PROMPT-*.md`.

## 0 · Bu devrin görevi (19 Ekim 2026, Faz 5'in başı)

Faz 4b kapandı, Faz 5 açıldı (K-250, K-251). Bu fazın ürünü DESPARETE'dir.

- **Yürütücünün amacı:** protokole çalışma mantığından formüllerine kadar A'dan Z'ye hâkim olmak ve onu **kendisi üretmek**.
- **Özgünlüğün anlamı:** mevcut bir protokolü alıp üstüne ekleme yaparak "yeni protokol" diye sunmamak. Başka protokollerden özellik alınabilir.
- **Senin rolün:** danışman ve öğretmen (§3 madde 13).
- **Faz 5'in üç aşaması** (`v2/12` §1.2):
  1. **hâkimiyet:** yürütücü mevcut DESPARETE'yi (v0.4.1) tam olarak öğrenir;
  2. **araştırma ve öğrenim:** daha iyi bir protokol nasıl yapılır, hangi yöntemler kullanılmalı;
  3. **geliştirme.**

İlk oturumda:

1. **Projeye hâkim ol.**
   - §4'teki belgeleri ve kodu öncelik sırasıyla oku. Bu bir harita, zorunlu kontrol listesi değil.
   - **DESPARETE'ye özellikle derin in** (§4'teki DESPARETE haritası). Yürütücüye onu A'dan Z'ye öğreteceksin; bu yüzden kendin anlamış olmalısın:
     - her parçasını, formüllerini, durum makinelerini, mesajlarını ve ablasyon bayraklarını;
     - gerçekleme kararlarını (K-150…K-172);
     - ölçülen davranışını (K-228, K-244 kuyruğu).
   - Belgelerdeki iddiaları kodla karşılaştır; ayrışma varsa not et. v0.1 tasarım paketi bayattır, ama fikirlerin kökenidir.
2. **Mevcut durumu analiz et**, kendi gözünle:
   - simülatörün ve rakiplerin hâli;
   - DESPARETE'nin rakiplere, özellikle Babel'e göre durumu;
   - Faz 5.0'ın bulguları;
   - takvim ve hesap bütçesi (`v2/12` §3–§4).

   `v2/12` ve `v2/04` önceki çalışmanın ürünüdür; doğru olduklarını varsayma.
3. **Bu aşamadan sonrasını planla.**
   - **5-1 hâkimiyet:** DESPARETE'yi yürütücüye nasıl öğreteceğin.
     - konuların sırası ve her konunun hedefi;
     - anlatma yolu: sade dil, örnek sayılar, benzetme, kodun üzerinden yürüme;
     - yürütücünün kendi sözleriyle özetlemesi ve anlaşıldığını sınama yolu.
   - **5-2 araştırma ve öğrenim:**
     - hangi soruları araştıracağımız; örnekler: karıştırmanın ve bağ kalitesinin yerel kanıtı, yedek ve çok yollu yönlendirme, döngüsüzlük yöntemleri, rakiplerin mekanizmaları;
     - hangi kaynaklar: depodakiler `protokol_kaynaklari/` · `v2/02` · `v2/16`; indirme yürütücünün izniyle;
     - aşamanın çıktısı ne olacak.
   - **5-3 geliştirme:** yürütücünün tasarımından koda ve ölçüme nasıl geçileceği. Ön-kayıtla ve mekanizma kapısıyla (K-247) ilişkisi.
   - **Takvim:** mühür ~20 Kasım, proje hedefi 19 Aralık, son başvuru 4 Ocak 2027. İlk iki aşama geliştirmeyi öteler; etkisini ve seçenekleri açıkça yaz, karar yürütücünündür.
4. **İlk cevapta hiçbir şeyi değiştirme:** dosya düzenleme, ölçüm ya da commit komutu yok. Yürütücüye Türkçe ve özet hâlinde şunları sun:
   - **öğrendiklerin:** proje, simülatör, rakipler ve özellikle DESPARETE'nin bugünkü hâli (nasıl çalıştığı, güçlü ve zayıf yanları);
   - **durum raporu:** nerede olduğumuz ve açık riskler;
   - **plan önerin:** üç aşama ve takvim, gerekçeleriyle; katılmadığın kararlar.

   Neyi doğruladığını, neyi varsaydığını ve nerede emin olmadığını ayrı yaz. Sonra dur; ne yapılacağını yürütücü yazar.

## 1 · Proje

- **Ne:** bir lise öğrencisinin TÜBİTAK 2204-A projesi (Yazılım / Havacılık ve Uzay); teslim **19 Aralık 2026**, ön-kayıt mühürü ~20 Kasım.
- **Konu:** karıştırma (jamming) altındaki taktik İHA sürüsünde mesh yönlendirme. Sürü telemetrisini yer istasyonuna (geçit) taşır, komutlar ters yönde gider; yer ve hava karıştırıcıları bağları bozar ya da kanalı kilitler.
- **İki katkı:**
  1. taban protokollerin bu koşullarda nasıl bozulduğunu gerçekçi bir simülasyonda ölçmek;
  2. bu çalışmada önerilen **DESPARETE** protokolünü karıştırma altında daha yüksek teslim sağlayacak şekilde geliştirip ön-kayıtlı istatistikle karşılaştırmak.
- **Kıyas tabanı:** AODV (`AODV-k`), OLSRv2 (`OLSRv2-b`) ve Babel (`Babel-a`, RFC 8966); üçü donmuş (K-239, K-249). Üçü birincil hücrede eşit rolde, Holm m = 3 (KR-3, K-247). JarmRout K-242'de rakiplikten çıktı; kodu ve kayıtları Faz 4b'nin kaydıdır.
- **Ölçüm ortamı:** projenin kendi simülatörü `sim2/` (Python, kesikli olay; 802.11b telsiz, 1:1 referans dünya).
- **Birincil metrik:** `PDR_açık`, karıştırıcının açık dönemlerinde doğan paketlerin teslim oranı. "Karıştırmaya özgü kazanç" iddiası ancak fark-içinde-fark ve mekanizma kapısıyla kurulur (`v2/06` §0.4.5).
- **Nerede kaldık** (ayrıntı `v2/12` §1.1):
  - Faz 4b kapandı (K-250): üç rakip donmuş, bağımsız denetimin (14 Ekim, K-242) Faz 5 öncesi işleri tamam.
  - Şimdiki faz **Faz 5: DESPARETE'nin özgün tasarımı**. Çalışma biçimi §3 madde 13.

## 2 · Doğrulama ilkesi

- **Hiçbir şeyi doğrulamadan kesin doğru kabul etme.** Bu dosya, `v2/` belgeleri, kod yorumları, karar günlüğü ve önceki ajanların özetleri bayat ya da yanlış olabilir. Bir iddiayı kullanmadan önce kodla, ölçümle ya da birincil kaynakla doğrula; doğrulayamıyorsan varsayım olarak işaretle.
- **Çelişkide ölç.** Belge ile kod çelişirse hangisinin yanlış olduğunu ölçerek bul. Kod yorumları çoğu zaman tarihçe taşır ("ilk yazımda…"); bugünkü doğru `v2/04` ve kodun kendisidir.
- **Beklenmeyen sonuçta önce sebebi ölç;** parametre oynatıp sonucu tutturma.
- **Emin olmadığını kesin diye sunma;** neyi ölçtüğünü, neyi varsaydığını ayır.
- **Gerekçesi görünmeyen bir kural** sorgulanır ve yürütücüye sorulur.

## 3 · Çalışma kuralları (yürütücü kararları)

1. **Dil:** yürütücüyle Türkçe konuşulur; özetler kısa.
2. **Git:** okuma komutları (`status`, `diff`, `log`) serbesttir. Commit, push ve dal işlemleri **yalnız yürütücüdedir**; gerekince komutu ona ver (tek satır mesaj; bir blokta tek komut).
3. **Ölçüm süreci (denetim D-05):**
   - Her sayı üretici komutuyla yazılır.
   - Sonucu ya da bir kararı etkileyen her ölçümün ölçütü (`beklenti.md`) ölçmeden önce yazılır ve koşudan önce yürütücünün commit'iyle girer.
   - Sonuçlar ayrı `sonuc.md`ye yazılır; beklentiye dokunulmaz. Her ölçümden sonra push.
   - Sonuçtan sonra değişen bir ölçüt `v2/06` §10'a yazılır.
4. **Tohumlar:** ana deney tohumları 2000–2039 mühürden önce hiçbir protokolle koşulmaz.
5. **Protokoller:**
   - Protokol kâhin bilgisi göremez.
   - Rakip protokoller kaynağına sadık kalır ve senaryoya göre ayarlanmaz; negatif sonuç gizlenmez.
   - Taban protokoller donmuştur (`tests2/test_donma.py`); bir dosya değişirse yeni K kaydı, U1 ve regresyon gerekir.
6. **Uzun koşu** (~30 dk üstü):
   - Süresini önceden söyle; iki ağır işi aynı anda koşma (12 mantıksal çekirdek, havuz 8 işçi; tam test takımı da ağırdır).
   - Uzun koşu dondurulmuş kod kopyasından yapılır: `py -3.11 arsiv/teshis/faz4_2026-09-26/dondur.py <klasör>`. Kopyanın commit'le birebir olduğunu dosya özetleriyle doğrula.
   - Birden çok uzun adım bir kabuk betiğinde sırayla koşar; her adımın saati `zaman.txt`e yazılır.
   - Uzun koşudan önce kısa bir duman koşusuyla aleti sına; ham veriyi analizden önce diske yaz.
7. **Simülatörün davranışını değiştiren** her değişiklikten sonra regresyon ve mimari denetimi koşulur; tam test takımı iş kapanışında. Yalnız yorum değişikliğinde davranışın aynı kaldığı sözdizim ağacı karşılaştırmasıyla gösterilebilir (K-241).
8. **Dosyalar:** dosya silinmez; eskiyen belge `arsiv/`e taşınır. Paket kurulmaz; indirme yürütücünün izniyle yapılır.
9. **Kararlar:**
   - Yeni karar kısa bir kayıtla `v2/kayit/KARAR-GUNLUGU.md`nin sonuna eklenir (ne · neden · kim · sayı + komut).
   - Geçerli bir kararı değiştiriyorsa `v2/04-KARARLAR.md` de güncellenir.
   - Ardından `py -3.11 arsiv/dogrulama/kayit_indeksi.py` ve `--kontrol` koşulur.
   - Durum değişince yalnız `v2/12` güncellenir.
10. **Belge üslubu (19 Ekim):** belgeler (README, `v2/`, karar günlüğü) yürütücünün kendi sesiyle yazılır: kararlar birinci tekil ("Babel'i seçtim", "> tarih · kararım: …"), işler edilgen ("regresyon koşuldu", "hata bulundu ve düzeltildi"). "Yürütücü", "ajan", "öğrenci" ve "X şöyle dedi" alıntısı kullanılmaz; yürütücünün sözü birinci tekil olarak yeniden ifade edilir. Bilgi düzeyinde kalır; kişilik, duygu, slogan ve emoji yok. Yapay zekânın işi ve hatası silinmez, edilgen yazılır; yapay zekâ beyanı (README, `v2/01`) açık kalır. Karar günlüğünün içeriği (sayı, tarih, karar) değiştirilmez. Bu yönerge ve sohbet mesajları kuralın dışındadır.
11. **Gerçekçilik esastır:** bir ölçütle gerçekçilik çatışırsa gerçekçi olan seçilir ve gerekçesi yazılır (K-185).
12. **Kusurun ele alınışı:**
    - Bilimsel güvenilirliği bozan bir zafiyet beyanla geçilmez, düzeltilir.
    - Savunulabilir bir seçim için simülatör sarsılmaz; her küçük sorun rapora bulgu diye yazılmaz.
    - Yürütücüye kapsam, iddia, ön-kayıt metriği ve büyük tasarım değişikliklerinde sorulur.
13. **Faz 5'te çalışma biçimi (K-250, K-251):**
    - DESPARETE özgün bir protokol olacak: mevcut bir protokolü alıp üstüne ekleme yaparak sunulmaz; özellik alınabilir, kaynağı açıkça yazılır.
    - Yürütücü protokole A'dan Z'ye hâkim olup onu kendisi üretir. Sen danışman ve öğretmensin.
    - Öğretirken kavramı sade anlat: örnek sayı, benzetme, kod üzerinden. Yürütücünün kendi sözleriyle özetini dinle ve düzelt.
    - Seçenekleri artı ve eksileriyle sun; kendi fikrini üretmesine alan bırak. Tasarım kararı yürütücünündür.
    - Aşama atlanmaz: hâkimiyet → araştırma ve öğrenim → geliştirme.
    - Kodun kimin yazacağını yürütücünün planı belirler; varsayma, sor. Ölçüm ve kayıt disiplini aynen sürer.

## 4 · Okuma haritası

**Belgeler** (önce bunlar):

| öncelik | belge | ne için |
|---|---|---|
| 1 | `v2/01` | problem, kapsam, başarı ölçütü |
| 1 | `v2/04-KARARLAR.md` | bugün geçerli bütün kararlar; açık kararlar §10 |
| 1 | `v2/12` | durum, plan, hesap bütçesi, riskler |
| 2 | `v2/06` · `v2/08` | ön-kayıt (hipotezler, eşik, istatistik) · evre metrikleri ve kapıları |
| 2 | `v2/05` · `v2/13` | protokolün görebildiği ve yapabildiği (sözleşmeler) |
| 2 | `v2/07` · `v2/14` | simülatörün yapısı · referans dünyanın sayıları ve kaynakları |
| 3 | `v2/03` · `v2/02` · `v2/09` | yöntem ilkeleri · doğrulanmış kaynaklar · aletin dış çapası (Li replikasyonu) |
| 3 | `arsiv/teshis/faz5_0_2026-10-10/sonuc.md` | DESPARETE'nin karıştırma altında nerede kaybettiği — Faz 5'in hedefi |
| 3 | `arsiv/teshis/rakipler_k244_2026-10-14/sonuc.md` | AODV-k ve Babel'in regresyon, U1, evre kapıları ve donma yolu; teşhis zinciri |
| 4 | `arsiv/denetim/DENETIM-RAPORU-2026-10-14.md` | son bağımsız denetim (kararları K-242…K-246) |
| gerektikçe | `v2/kayit/KARAR-GUNLUGU.md` | bir `K-xxx` atfının tarihçesi; okuma belgesi değil |

**Kod** (simülatörün omurgası, protokoller, ölçüm aletleri):

| alan | dosya | ne için |
|---|---|---|
| dünya ve parametreler | `sim2/kanal/dunya.py` · `sim2/yapilandirma/konfig.py` | referans dünyanın anahtarları (`referans_2026`) · bütün parametreler; `kokenler.py` her parametrenin kökeni (göz gezdir) |
| koşu | `sim2/kosum/kurulum.py` · `kosu.py` · `dugum.py` | kurulum, olay döngüsü; düğüm: kuyruk, bekleme tamponu, düşüş sebepleri |
| paketin yolu | `sim2/kosum/gonderim.py` · `alim.py` · `teslim.py` · `kontrol.py` | veri ve kontrol çerçevesinin gönderimi, alımı, teslimi |
| MAC ve kanal | `sim2/mac/dcf.py` · `alici.py` · `sim2/kanal/kanal.py` · `girisim.py` · `sonumleme.py` | 802.11 DCF, alıcı zinciri, yol kaybı, SINR, sönümleme |
| tehdit | `sim2/kanal/karistirici.py` · `tehdit.py` | karıştırıcı sınıfları ve tehdit aileleri |
| protokol yüzeyi | `sim2/gozlem/pencere.py` · `protokol.py` · `kontrol.py` | gözlem penceresi, kancalar, kontrol düzlemi API'si |
| ölçüm | `sim2/olcum/paket_defteri.py` · `evre.py` · `sim2/kosum/sonuc.py` · `sim2/cekirdek/korunum.py` | teslim kayıtları, evre metrikleri, sonuç satırı, korunum |
| önerilen protokol | `protokoller/desparete.py` · `desparete_bayrak.py` (öteki `desparete_*.py` gerektikçe) | DESPARETE v0.4.1: sürüm geçmişi başlıkta, profil ve ablasyon bayrakları |
| taban protokoller | `protokoller/aodv.py` · `olsrv2.py` · `babel.py` ve beyan tabloları `*_bicim.py` | rakiplerin gerçeklemesi; beyan tabloları kaynaktan sapmaları anlatır |
| aletler | `kalibrasyon/kahin.py` · `aodv_uygunluk.py` · `kayip_anatomisi.py` · `evre_metrikleri_kapilari.py` | kâhinler · U1 kabul kapısı · kayıp anatomisi (Faz 5'in teşhis aleti) · evre kapıları |
| denetim | `kalibrasyon/regresyon_satirlari.py` · `mimari_denetimi.py` · `tests2/test_donma.py` | regresyon matrisi · yapı ve köken denetimi · donmuş dosyalar |
| analiz | `analiz/hucre.py` · `satir.py` | ön-kaydın istatistik planı ve `PDR_açık`ın ikinci gerçeklemesi |

**DESPARETE haritası** (§0 madde 1):

| ne | nerede |
|---|---|
| kod (~2 700 satır) | `protokoller/desparete.py` (simülatöre bağlanan sınıf, olay sırası, beyanlar) · `desparete_komsu.py` (komşu yaşamı, belirsizlik) · `desparete_metrik.py` (M0.1 bağ metriği) · `desparete_alan.py` (alan, uygulanabilirlik, ardıl, döngüsüzlük) · `desparete_edinim.py` (edinim ve onarım) · `desparete_politika.py` (postür) · `desparete_bicim.py` (mesaj biçimleri) · `desparete_bayrak.py` (profil, V1…V11 seçenekleri, ablasyon bayrakları) |
| testler | `tests2/test_desparete.py` (her parçanın kendi testi) |
| gerçekleme kararları | K-150…K-172: komşu yaşamı K-154 · alan ve ardıl K-155 · edinim K-156 · kota K-157 · postür K-158 · ablasyon K-159 · kabul kapısı ve v0.1'in çöküşü K-160 · v0.2…v0.4.1 K-161…K-172 |
| ölçülen davranış | Faz 5.0 `arsiv/teshis/faz5_0_2026-10-10/sonuc.md` (K-228) · K-244 kuyruğunun evre kapıları `arsiv/teshis/rakipler_k244_2026-10-14/sonuc.md` §5 · `v2/04` §6 |
| teşhisler | `arsiv/teshis/desparete_*_2026-09-2x/` (komşu, alan, onarım, kota, postür, ablasyon, kabul, v0.2, analiz, edinim) |
| sözleşmeler | `v2/05` (protokolün görebildiği) · `v2/13` (kontrol düzlemi ve bedeli) |
| kökeni (bayat; bugünkü doğru koddur) | `arsiv/DESPARETE_TASARIM_PAKETI_v0.1_2026-09-22/` (40 belge; kodun atıf verdiği `36` aday spesifikasyon) |
| rakiplerin mekanizmaları | `protokoller/babel.py` · `olsrv2.py` · `aodv.py` · sadakat denetimleri `arsiv/teshis/babel_sadakat_2026-10-14/denetim.md` · `aodv_sadakat_2026-10-14/denetim.md` |
| kaynaklar | `protokol_kaynaklari/` (RFC'ler, ns-3, olsrd2, babeld, otopilot) · `v2/02` · `v2/16` |

## 5 · Bilinmesi gereken tuzaklar

- **İki dünya:** `Konfig()` varsayılanı eski 1:50 dünyadır; deneyler **referans dünyada** (`referans_2026`) koşar. Araçlar dünyayı `--dunya referans_2026` ya da `DESPARETE_DUNYA=referans_2026` ile seçer. 25 Eylül'den önceki bütün sayılar eski dünyanındır.
- **Python 3.11:** `python` komutu başka bir proje için kurulan 3.12'yi açıyor; bütün komutlar `py -3.11` ile çalıştırılır.
- **Windows:**
  - Python çağrılarında `PYTHONIOENCODING=utf-8` gerekir.
  - `Pool` kullanan betikte `if __name__ == "__main__":` korunur; iç içe havuz yok.
- **Satır sonları karışıktır (CRLF/LF) ve korunur:**
  - Write aracı LF yazar; `sed -i` CRLF dosyayı bozabilir. Değişikliği Python'la bayt düzeyinde yap.
  - Kimlik özetleri (`dosya_hash`) satır sonunu normalleştirir.
  - Satır sonunu Python'la bayt sayarak doğrula; Git Bash'te `grep -c $'\r'` satır sonunu değil satır sayısını verir.
- **Kabuk:**
  - Heredoc'u tırnaklı ayraçla aç; uzun Python düzenlemelerini dosyaya yazıp çalıştır.
  - `timeout` yalnız `py` başlatıcısını öldürebilir; süreç listesine bak.
- **Arka plan işi:** kabuk kesilince Python yaşamaya devam edebilir. Bir süreci durdurmadan ya da yeniden başlatmadan önce süreç listesine bak; iki kopya koşmasın.
- **Gürültülü tek koşu:** statik kolda sönümleme donuktur. Kısa pencerede (30 s) tek tohumun PDR'si ±0,15 oynar; tek tohumlu kısa pencere sayısı tek başına karara girmez.
- **MAC deneme sayısı:** `yeniden_deneme_siniri` YENİDEN deneme sayısıdır (toplam = sınır + 1; referans dünyada en çok 7 iletim denemesi, K-223).
- **Regresyon:**
  - Taban `k249` (87 vaka); taban dosyaları `ciktilar2/regresyon/`de (git dışı, dondurulmuş kopyada yoktur).
  - `Konfig`e alan eklemek bütün satırların `kurulum_hash`ini değiştirir; beklenen farkı önceden yaz.
  - Köken kovası değişince karşılaştırmada `--izin teshis.koken_kovalari` gerekir.
  - K-240 ve K-241'den sonra kod özetleri beklenen farktır.
- **Kâhin:** U1'in paydası ve R'nin aletidir. Kâhin ya da MAC değişirse U1 ve R yeniden ölçülür.
- **En uzun koşu AODV-k'nin:** birincil hücrede koşu başına ~2,1–2,2 sa (`v2/12` §3).
- **Evre kapılarında kayıtlı muafiyet (K-239):** `evre_metrikleri_kapilari.py hukum <çıktı>` kayıtlı bir kapı çıktısını bugünkü hükümle yeniden değerlendirir.
- **Pencere sonu:** trafik ölçüm bitişinde (320 s) durur. Uzun bekleyişli protokolde son doğumlar boşalan ağda teslim edilir (K-239); pencere üçlüsü Faz 6'da ölçülür.
- **Mimari denetiminde "ihlal" ile "bulgu" ayrıdır** (DD-19): çıkış koduna bak. Köken defterinde kaydı olmayan yeni bir sabit bulgudur (K-249).
- **Beklenti yazmadan önce** aynı konudaki önceki ön-kayıtlara (kuyruk beklentileri) bak; önce yazılan kural geçerlidir (K-249).
- **İz ve teşhis araçları:** iç içe sarmalanan çağrılarda değişiklik kaybolabilir; zincir sürekliliği gibi bir öz-denetim ekle (`arsiv/teshis/aodv_k_dongu_2026-10-16/`).
- **Arka plan kabuğu ~9,5 sa'te kesilebilir:** uzun işi < 8 sa'lik adımlara böl, adım betiği biten adımı atlasın. Çıkış kodunu `$(date)`'ten önce al (K-243).
- **Kâhin tavan değildir** (K-110, K-248): kâhin aşımında önce hata aranır; temiz çıkarsa hücre beyanla kayda girer.
- **M4'ün boş dağılımı** temiz evrede sıfır beyanda sıfır gözlemin üst güven sınırıdır (K-249).

## 6 · Doğrulama — referans dünyada geçerli olanlar

Bütün komutlar `py -3.11` ve `PYTHONIOENCODING=utf-8` ile koşulur.

| komut | beklenen | süre |
|---|---|---|
| `-m pytest tests2 -q` | `1095 passed` (17 Ekim, K-249) | ~16 dk |
| `kalibrasyon/mimari_denetimi.py` | `Yapisal ihlal YOK` · SINANMAMIŞ 5 · borç 0 · kapsam ilanı 13 | < 1 dk |
| `-u kalibrasyon/regresyon_satirlari.py uret <etiket>` · `karsilastir k249 <etiket> [--izin …] [--degisen …] [--yeni …]` | ilan edilen farklar dışında BİREBİR; beklenen fark önceden yazılır | ~80 dk + < 1 dk |
| `arsiv/dogrulama/kayit_indeksi.py --kontrol` | indeks güncel | saniyeler |
| `-u kalibrasyon/evre_metrikleri_kapilari.py 1c` · `… 2c` · `… 1p` · `… 3c` (`DESPARETE_DUNYA=referans_2026`) · `… hukum <çıktı>` | G1ç · G2ç + G4ç · G1-P · G3ç `GECTI` (K-249) | ~1,8 sa · ~2,3 sa · ~25 dk · 30 dk · saniyeler |
| `-u kalibrasyon/cozunurluk.py --dunya referans_2026 --hucre birincil --tohum 40` | `KULLANILACAK ESIK R = 0.0126` (K-224) | ~70 dk |
| `-u kalibrasyon/duyarlilik.py --dunya referans_2026 birincil <adlar>` | parametre başına DUYARLI / DUYARSIZ / ÖLÇÜLEMEDİ; sınırdaki kayıt `--tohum 20` | 5 tohumda parametre başına ~17 dk |
| `-u kalibrasyon/aodv_uygunluk.py --dunya referans_2026 --desen <yere_toplama\|esler_arasi> --protokol <p,…>` · hüküm `… --protokol <p> hukum <kayıt>` | U1-U ve U1-B iki desende (`v2/04` §5) | AODV-k ve Babel'le yere toplama ~5,3 sa, eşler arası ~4,8 sa · saniyeler |
| `-u kalibrasyon/kayip_anatomisi.py --dunya referans_2026 [--sinif yok] --kol <kol> --protokoller <p> --tohumlar <…> --kayit <json>` | düşme sebepleri × bölge, karar bağının bandı | koşu başına 1–9 sa |
| `-u kalibrasyon/li_replikasyonu.py --dunya referans_2026` · `-u arsiv/teshis/faz4_2026-09-26/b_li_ayristirma.py <kopya>` | araç: H1 ≈ 0,042 (ARF açık) tutmaz · sabit hızda 0,1250 tutar (K-226) | 4 dk · 3 dk |
| `kalibrasyon/denetim_ornekleme.py` · `kontrol_duzlemi_kapilari.py` · `ust_referans.py --kapi` · `bag_kumesi.py a` (`DESPARETE_DUNYA=referans_2026`) · `anlamlilik_sabitleri.py` · `uretici_duman.py` | 4/4 · 21/21 · üç kapı · G-a/G-b · KAPI GEÇTİ · bütün kesitler (K-226) | dakikalar; duman 29 dk |
