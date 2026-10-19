# BAŞLANGIÇ — bu projede çalışacak yeni ajan için

> Yürütücü bu dosyayı yeni bir ajana ilk mesaj olarak verir. Güncel: 13 Ekim 2026 (K-241'den sonra). Durum ve plan yalnız `v2/12`de tutulur; burada yalnız giriş için gereken kadarı var. Önceki sürümler `arsiv/DEVIR-PROMPT-*.md`.

## 0 · İlk oturumun görevi

1. **Projeye hakim ol.**
   - §4'teki belgeleri ve kod dosyalarını, verilen öncelik sırasıyla oku. Bu bir harita, zorunlu kontrol listesi değil: anlamak için gerektiği kadar derine in, gerekmeyen ayrıntıda boğulma.
   - Okurken belgelerdeki iddiaları kodla karşılaştır; belge ile kod ayrışıyorsa not et.
2. **Bağımsız ve özgür düşün.**
   - `v2/12`deki plan ve `v2/04`teki kararlar önceki çalışmanın ürünüdür; doğru olduklarını varsayma.
   - Yöntemi, simülatörün gerçekçiliğini, rakip seçimini, DESPARETE'nin yönünü, ölçüm planını ve takvimi kendi gözünle değerlendir.
   - Bir kararın gerekçesi zayıfsa ya da daha iyi bir yol görüyorsan açıkça söyle; öneri sunmak için onay gerekmez.
   - Sabit olan yalnız §3'teki yürütücü kuralları. Onları değiştirmeyi önerebilirsin, kendin değiştirmezsin.
3. **İlk cevapta hiçbir şeyi değiştirme.** Dosya düzenleme, ölçüm koşma ya da commit komutu verme. Yürütücüye iki şey sun, Türkçe ve kısa:
   - **Projeden ne anladığın:** amaç, simülatör, rakipler, DESPARETE'nin bugünkü hâli, nerede kaldığımız.
   - **Düşüncelerin:** bu projede ne yapmamız gerektiği, gerekçeleriyle:
     - öncelikler ve sıralama;
     - gördüğün riskler, zayıflıklar ve fırsatlar;
     - katılmadığın kararlar.

     Neyi doğruladığını, neyi varsaydığını ve nerede emin olmadığını ayrı yaz.

   Sonra dur. Ne yapılacağını yürütücü yazar.

## 1 · Proje

- **Ne:** bir lise öğrencisinin TÜBİTAK 2204-A projesi (Yazılım / Havacılık ve Uzay); teslim **19 Aralık 2026**, ön-kayıt mühürü ~20 Kasım.
- **Konu:** karıştırma (jamming) altındaki taktik İHA sürüsünde mesh yönlendirme. Sürü telemetrisini yer istasyonuna (geçit) taşır, komutlar ters yönde gider; yer ve hava karıştırıcıları bağları bozar ya da kanalı kilitler.
- **İki katkı:**
  1. taban protokollerin bu koşullarda nasıl bozulduğunu gerçekçi bir simülasyonda ölçmek;
  2. bu çalışmada önerilen **DESPARETE** protokolünü karıştırma altında daha yüksek teslim sağlayacak şekilde geliştirip ön-kayıtlı istatistikle karşılaştırmak.
- **Kıyas tabanı:** AODV ve OLSRv2. Üçüncü rakip açık karardır: JarmRout kodlandı ve dondu, ama kesin değildir. Yürütücü tanımı tam, bilimsel olarak güvenilir ve straw-man eleştirisine açık olmayan başka bir protokol arayabilir (K-240, `v2/04` §10).
- **Ölçüm ortamı:** projenin kendi simülatörü `sim2/` (Python, kesikli olay; 802.11b telsiz, 1:1 referans dünya).
- **Birincil metrik:** `PDR_açık`, karıştırıcının açık dönemlerinde doğan paketlerin teslim oranı. "Karıştırmaya özgü kazanç" iddiası ancak fark-içinde-fark ve mekanizma kapısıyla kurulur (`v2/06` §0.4.5).
- **Nerede kaldık** (ayrıntı `v2/12` §1.1):
  - Faz 4b'nin ilk dört adımı bitti: yeni rakipler, U1, evre kapıları, donma, belge ve kod temizliği.
  - Sıradaki konular: üçüncü rakip kararı · derin blok denetimi (simülatör ve rakipler ayrı denetçilerce) · ardından Faz 5 (DESPARETE'nin karıştırmaya özgü mekanizmaları).

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
10. **Belge üslubu:** belgeler yalnız bilgi düzeyinde ve nesnel yazılır; kişilik, duygu, slogan ve emoji kullanılmaz; "öğrenci/ajan" dili yerine "yürütücü", "karar K-xxx" kullanılır. Karar günlüğü tarihsel kayıttır, yeniden yazılmaz.
11. **Gerçekçilik esastır:** bir ölçütle gerçekçilik çatışırsa gerçekçi olan seçilir ve gerekçesi yazılır (K-185).
12. **Kusurun ele alınışı:**
    - Bilimsel güvenilirliği bozan bir zafiyet beyanla geçilmez, düzeltilir.
    - Savunulabilir bir seçim için simülatör sarsılmaz; her küçük sorun rapora bulgu diye yazılmaz.
    - Yürütücüye kapsam, iddia, ön-kayıt metriği ve büyük tasarım değişikliklerinde sorulur.

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
| 3 | `arsiv/teshis/jarmrout_sel_2026-10-12/inceleme.md` · `arsiv/teshis/faz4b_kapi_teshis_2026-10-13/teshis.md` | JarmRout'un toplu akış çöküşü ve evre kapıları |
| 4 | `arsiv/denetim/DENETIM-RAPORU-2026-10-08.md` | son bağımsız denetim (kararları K-222…K-226) |
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
| taban protokoller | `protokoller/aodv.py` · `olsrv2.py` · `jarmrout.py` ve beyan tabloları `*_bicim.py` | rakiplerin gerçeklemesi; beyan tabloları kaynaktan sapmaları anlatır |
| aletler | `kalibrasyon/kahin.py` · `aodv_uygunluk.py` · `kayip_anatomisi.py` · `evre_metrikleri_kapilari.py` | kâhinler · U1 kabul kapısı · kayıp anatomisi (Faz 5'in teşhis aleti) · evre kapıları |
| denetim | `kalibrasyon/regresyon_satirlari.py` · `mimari_denetimi.py` · `tests2/test_donma.py` | regresyon matrisi · yapı ve köken denetimi · donmuş dosyalar |
| analiz | `analiz/hucre.py` · `satir.py` | ön-kaydın istatistik planı ve `PDR_açık`ın ikinci gerçeklemesi |

DESPARETE'nin v0.1 tasarım taslağı (`arsiv/DESPARETE_TASARIM_PAKETI_v0.1_2026-09-22/`) bayattır; okunacak belge değildir.

## 5 · Bilinmesi gereken tuzaklar

- **İki dünya:** `Konfig()` varsayılanı eski 1:50 dünyadır; deneyler **referans dünyada** (`referans_2026`) koşar. Araçlar dünyayı `--dunya referans_2026` ya da `DESPARETE_DUNYA=referans_2026` ile seçer. 25 Eylül'den önceki bütün sayılar eski dünyanındır.
- **Python 3.11:** `python` komutu başka bir proje için kurulan 3.12'yi açıyor; bütün komutlar `py -3.11` ile çalıştırılır.
- **Windows:**
  - Python çağrılarında `PYTHONIOENCODING=utf-8` gerekir.
  - `Pool` kullanan betikte `if __name__ == "__main__":` korunur; iç içe havuz yok.
- **Satır sonları karışıktır (CRLF/LF) ve korunur:**
  - Write aracı LF yazar; `sed -i` CRLF dosyayı bozabilir. Değişikliği Python'la bayt düzeyinde yap.
  - Kimlik özetleri (`dosya_hash`) satır sonunu normalleştirir.
- **Kabuk:**
  - Heredoc'u tırnaklı ayraçla aç; uzun Python düzenlemelerini dosyaya yazıp çalıştır.
  - `timeout` yalnız `py` başlatıcısını öldürebilir; süreç listesine bak.
- **Arka plan işi:** kabuk kesilince Python yaşamaya devam edebilir. Bir süreci durdurmadan ya da yeniden başlatmadan önce süreç listesine bak; iki kopya koşmasın.
- **Gürültülü tek koşu:** statik kolda sönümleme donuktur. Kısa pencerede (30 s) tek tohumun PDR'si ±0,15 oynar; tek tohumlu kısa pencere sayısı tek başına karara girmez.
- **MAC deneme sayısı:** `yeniden_deneme_siniri` YENİDEN deneme sayısıdır (toplam = sınır + 1; referans dünyada en çok 7 iletim denemesi, K-223).
- **Regresyon:**
  - Taban `k236` (85 vaka); taban dosyaları `ciktilar2/regresyon/`de (git dışı, dondurulmuş kopyada yoktur).
  - `Konfig`e alan eklemek bütün satırların `kurulum_hash`ini değiştirir; beklenen farkı önceden yaz.
  - Köken kovası değişince karşılaştırmada `--izin teshis.koken_kovalari` gerekir.
  - K-240 ve K-241'den sonra kod özetleri beklenen farktır.
- **Kâhin:** U1'in paydası ve R'nin aletidir. Kâhin ya da MAC değişirse U1 ve R yeniden ölçülür.
- **JarmRout koşuları uzundur:** yere toplamalı hücrelerde koşu başına 5,6–9 sa (`v2/12` §3).
- **Evre kapılarında kayıtlı muafiyet (K-239):** `evre_metrikleri_kapilari.py hukum <çıktı>` kayıtlı bir kapı çıktısını bugünkü hükümle yeniden değerlendirir.
- **Pencere sonu:** trafik ölçüm bitişinde (320 s) durur. Uzun bekleyişli protokolde son doğumlar boşalan ağda teslim edilir (K-239); pencere üçlüsü Faz 6'da ölçülür.
- **Derin denetime açık iki not** (`v2/12` §1.1 adım 4):
  - G1-P yeni rakip kümesiyle koşulmadı;
  - bütün kontrol mesajları UDP/IP ile faturalanıyor, gerçek DSR (JarmRout) UDP kullanmaz.

## 6 · Doğrulama — referans dünyada geçerli olanlar

Bütün komutlar `py -3.11` ve `PYTHONIOENCODING=utf-8` ile koşulur.

| komut | beklenen | süre |
|---|---|---|
| `-m pytest tests2 -q` | `1059 passed` (13 Ekim) | ~15 dk |
| `kalibrasyon/mimari_denetimi.py` | `Yapisal ihlal YOK` · SINANMAMIŞ 5 · borç 0 · kapsam ilanı 13 | < 1 dk |
| `-u kalibrasyon/regresyon_satirlari.py uret <etiket>` · `karsilastir k236 <etiket> [--izin …] [--degisen …] [--yeni …]` | ilan edilen farklar dışında BİREBİR; beklenen fark önceden yazılır | ~70 dk + < 1 dk |
| `arsiv/dogrulama/kayit_indeksi.py --kontrol` | indeks güncel | saniyeler |
| `-u kalibrasyon/evre_metrikleri_kapilari.py 1c` · `… 2c` · `… 3c` (`DESPARETE_DUNYA=referans_2026`) · `… hukum <çıktı>` | G1ç · G2ç + G4ç · G3ç `GECTI` (K-239'un kaydıyla) | JarmRout'la 8–9 sa · 6–7 sa · 30 dk · saniyeler |
| `-u kalibrasyon/cozunurluk.py --dunya referans_2026 --hucre birincil --tohum 40` | `KULLANILACAK ESIK R = 0.0126` (K-224) | ~70 dk |
| `-u kalibrasyon/duyarlilik.py --dunya referans_2026 birincil <adlar>` | parametre başına DUYARLI / DUYARSIZ / ÖLÇÜLEMEDİ; sınırdaki kayıt `--tohum 20` | 5 tohumda parametre başına ~17 dk |
| `-u kalibrasyon/aodv_uygunluk.py --dunya referans_2026 --desen <yere_toplama\|esler_arasi> --protokol <p,…>` · hüküm `… --protokol <p> hukum <kayıt>` | U1-U ve U1-B iki desende (`v2/04` §5) | JarmRout'la yere toplama ~17 sa, eşler arası ~7,5 sa · saniyeler |
| `-u kalibrasyon/kayip_anatomisi.py --dunya referans_2026 [--sinif yok] --kol <kol> --protokoller <p> --tohumlar <…> --kayit <json>` | düşme sebepleri × bölge, karar bağının bandı | koşu başına 1–9 sa |
| `-u kalibrasyon/li_replikasyonu.py --dunya referans_2026` · `-u arsiv/teshis/faz4_2026-09-26/b_li_ayristirma.py <kopya>` | araç: H1 ≈ 0,042 (ARF açık) tutmaz · sabit hızda 0,1250 tutar (K-226) | 4 dk · 3 dk |
| `kalibrasyon/denetim_ornekleme.py` · `kontrol_duzlemi_kapilari.py` · `ust_referans.py --kapi` · `bag_kumesi.py a` (`DESPARETE_DUNYA=referans_2026`) · `anlamlilik_sabitleri.py` · `uretici_duman.py` | 4/4 · 21/21 · üç kapı · G-a/G-b · KAPI GEÇTİ · bütün kesitler (K-226) | dakikalar; duman 29 dk |
