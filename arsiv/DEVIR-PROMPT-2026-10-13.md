# BAŞLANGIÇ — bu projede çalışacak ajan için

> Yürütücü bu dosyayı yeni bir ajana ilk mesaj olarak verir. Güncel: 13 Ekim 2026. Durum burada tekrarlanmaz: `v2/12`. Önceki sürümler `arsiv/DEVIR-PROMPT-*.md`.

## 0 · İlk iş

1. **Belgeleri oku ve projeyi anla:**
   - önce `v2/01`, `v2/04-KARARLAR.md`, `v2/12`;
   - simülatör ve protokoller için `v2/07`, `v2/14`, `v2/05`, `v2/13`;
   - yöntem için `v2/06`, `v2/08`, `v2/03`.

   Anlamak için gerektiği kadar koda bak.
2. **Nerede kaldığımızı çıkar:** `v2/12` §1 ve §1.1.
3. **Bundan sonrası için bir plan yap.**
4. **İlk cevabında hiçbir dosyayı değiştirme.** Yürütücüye kısa bir özet ver: projeden ne anladığın, nerede kaldığımız, planın ve emin olmadığın noktalar. Onay bekle.

## 1 · Proje

- **Ne:** bir lise öğrencisinin TÜBİTAK 2204-A projesi; teslim **19 Aralık 2026**.
- **Konu:** karıştırma (jamming) altındaki taktik İHA sürüsünde mesh yönlendirme. Sürü telemetrisini yer istasyonuna (geçit) taşır, komutlar ters yönde gider; yer ve hava karıştırıcıları bağları bozar ya da kanalı kilitler.
- **İki katkı:**
  1. taban protokollerin bu koşullarda nasıl bozulduğunu gerçekçi bir simülasyonda ölçmek;
  2. bu çalışmada önerilen **DESPARETE** protokolünü karıştırma altında daha yüksek teslim sağlayacak şekilde geliştirip istatistiksel olarak karşılaştırmak.
- **Kıyas tabanı:** AODV ve OLSRv2. Üçüncü rakip açık karardır: JarmRout kodlandı ve dondu ama kesin değildir; yürütücü tanımı tam ve straw-man eleştirisine açık olmayan başka bir protokol arayabilir (K-240, `v2/04` §10).
- **Ölçüm ortamı:** projenin kendi simülatörü `sim2/` (Python, kesikli olay; 802.11b telsiz, gerçek ölçekli referans dünya).
- **Birincil metrik:** `PDR_açık`, karıştırıcının açık dönemlerinde doğan paketlerin teslim oranı. "Karıştırmaya özgü kazanç" iddiası ancak fark-içinde-fark ve mekanizma kapısıyla kurulur (`v2/06` §0.4.5).

## 2 · Doğrulama ilkesi

- **Hiçbir şeyi doğrulamadan kesin doğru kabul etme.** Bu dosya, `v2/` belgeleri, kod yorumları, karar günlüğü ve önceki ajanların özetleri bayat ya da yanlış olabilir. Bir iddiayı kullanmadan önce kodla, ölçümle ya da birincil kaynakla doğrula; doğrulayamıyorsan varsayım olarak işaretle.
- **Çelişkide ölç.** Belge ile kod çelişirse hangisinin yanlış olduğunu ölçerek bul; kod yorumları çoğu zaman tarihçe taşır ("ilk yazımda…").
- **Beklenmeyen sonuçta önce sebebi ölç;** parametre oynatıp sonucu tutturma.
- **Emin olmadığını kesin diye sunma.** Yürütücüye emin olmadığın bir şeyi kesin bilgi gibi sunma; neyi ölçtüğünü, neyi varsaydığını ayır.
- **Gerekçesi olmayan kural:** bir kuralın gerekçesini göremiyorsan sorgula ve yürütücüye sor.

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
7. **Simülatörün davranışını değiştiren** her değişiklikten sonra regresyon ve mimari denetimi koşulur; tam test takımı iş kapanışında.
8. **Dosyalar:** dosya silinmez; eskiyen belge `arsiv/`e taşınır. Paket kurulmaz; indirme yürütücünün izniyle yapılır.
9. **Kararlar:**
   - Yeni karar kısa bir kayıtla `v2/kayit/KARAR-GUNLUGU.md`nin sonuna eklenir (ne · neden · kim · sayı + komut).
   - Geçerli bir kararı değiştiriyorsa `v2/04-KARARLAR.md` de güncellenir.
   - Ardından `py -3.11 arsiv/dogrulama/kayit_indeksi.py` ve `--kontrol` koşulur; bir kaydın yerini yenisi aldıysa aracın `SUPERSEDE` tablosu da güncellenir.
   - Durum değişince yalnız `v2/12` güncellenir.
10. **Belge üslubu:** belgeler yalnız bilgi düzeyinde ve nesnel yazılır; kişilik, duygu, slogan ve emoji kullanılmaz; "öğrenci/ajan" dili yerine "yürütücü", "karar K-xxx" kullanılır. Karar günlüğü tarihsel kayıttır, yeniden yazılmaz.
11. **Gerçekçilik esastır:** bir ölçütle gerçekçilik çatışırsa gerçekçi olan seçilir ve gerekçesi yazılır (K-185).
12. **Kusurun ele alınışı:**
    - Bir kusur bulunursa düzeltilir, ölçülür ve kanıtıyla getirilir.
    - Yürütücüye yalnız kapsam, iddia, ön-kayıt metriği ve büyük tasarım değişikliklerinde sorulur.
    - Her sorun rapora bulgu diye yazılmaz; savunulabilir bir seçimde simülatör sarsılmaz.

## 4 · Neyin nerede olduğu

| soru | yer |
|---|---|
| problem, kapsam, başarı ölçütü | `v2/01` |
| **bugün geçerli bütün kararlar**, açık kararlar | `v2/04-KARARLAR.md` (§10) |
| **durum, plan, sıradaki iş, hesap bütçesi** | `v2/12` |
| simülatör ve referans dünya | `v2/07` · `v2/14` |
| protokolün görebildiği / yapabildiği | `v2/05` · `v2/13` |
| ön-kayıt, metrikler, istatistik | `v2/06` · `v2/08` |
| yöntem ilkeleri ve bu projede görülen hatalar | `v2/03` |
| DESPARETE'nin bugünkü yapısı (v0.4.1) | `protokoller/desparete*.py` (sürüm geçmişi `desparete.py` başlığında, profil ve seçenekler `desparete_bayrak.py`de) · günlük K-150…K-172, K-200, K-228 |
| taban protokollerin kaynağa sadakati | `arsiv/teshis/aodv_sadakat_2026-09-30/` · `olsrv2_sadakat_2026-10-11/` · `jarmrout_sadakat_2026-10-11/` · beyan tabloları `protokoller/*_bicim.py` |
| JarmRout'un toplu akış çöküşü | `arsiv/teshis/jarmrout_sel_2026-10-12/inceleme.md` · evre kapıları `arsiv/teshis/faz4b_kapi_teshis_2026-10-13/teshis.md` |
| bir `K-xxx` atfı ya da bir kararın tarihçesi | `v2/kayit/KARAR-GUNLUGU.md` |

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
- **Kâhin:** U1'in paydası ve R'nin aletidir. Kâhin ya da MAC değişirse U1 ve R yeniden ölçülür.
- **JarmRout koşuları uzundur:** yere toplamalı hücrelerde koşu başına 5,6–9 sa (`v2/12` §3).
- **Evre kapılarında kayıtlı muafiyet var (K-239):** `evre_metrikleri_kapilari.py hukum <çıktı>` kayıtlı bir kapı çıktısını bugünkü hükümle yeniden değerlendirir.
- **Pencere sonu:** trafik ölçüm bitişinde (320 s) durur. Uzun bekleyişli protokolde son doğumlar boşalan ağda teslim edilir (K-239); pencere üçlüsü Faz 6'da ölçülür.

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
