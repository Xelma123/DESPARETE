# BAŞLANGIÇ — bu projede çalışacak ajana

> Öğrenci bu dosyayı yeni bir ajana ilk mesaj olarak verir. Güncel: 10 Ekim 2026. Durum burada tekrarlanmaz: `v2/12`.

## 0 · İlk iş

1. **Gerekli belgeleri oku ve projeyi anla** — §3'teki haritadan: önce `v2/01`, `v2/04-KARARLAR.md`, `v2/12`, sonra simülatör ve protokoller için `v2/07`, `v2/14`, `v2/05`, `v2/13`, yöntem için `v2/06`, `v2/08`, `v2/03`. Anlamak için gerektiği kadar koda bak.
2. **Nerede kaldığımızı anla** — `v2/12` §1 ve §1.1. Faz 5'e geçiş kapısı bağımsız bir denetimle (8 Ekim, `arsiv/denetim/DENETIM-RAPORU-2026-10-08.md`) ve düzeltmeleriyle (K-222…K-226) kapandı; sıradaki iş **Faz 5.0**.
3. **Bundan sonra ne yapacağımıza dair bir plan yap.** Faz 5'in önkoşulları `v2/12` §2'de: 5.0 beklentisinin `PDR_açık`a göre yeniden yazılması · 5.1'den önce gürültü gözleminin ölçüm modeli · 5.4'ten önce çoğaltmanın tanımları.
4. **İlk cevabında hiçbir dosyayı değiştirme.** Öğrenciye kısa bir özet ver: projeden ne anladığın, nerede kaldığımız, planın ve emin olmadığın noktalar. Öğrencinin onayını bekle.

Arkada koşan iş yok.

## 1 · Proje

Bir lise öğrencisinin TÜBİTAK 2204-A projesi, teslim **19 Aralık 2026**. Konu: karıştırma (jamming) altındaki taktik İHA sürüsünde mesh yönlendirme. Sürü telemetrisini yer istasyonuna (geçit) taşır, komutlar ters yönde gider; yer ve hava karıştırıcıları bağları bozar ya da kanalı kilitler. Proje iki şey yapar: (1) yaygın protokollerin (AODV, OLSR, AOMDV) bu koşullarda nasıl bozulduğunu gerçekçi bir simülasyonda ölçer; (2) öğrencinin protokolü **DESPARETE**'yi karıştırmayı gerçekten çözen bir protokole dönüştürüp istatistiksel olarak karşılaştırır. Ölçüm ortamı projenin kendi simülatörü `sim2/` (Python, kesikli olay; 802.11b telsiz, gerçek ölçekli referans dünya). Birincil metrik `PDR_açık` (karıştırıcının açık dönemlerinde doğan paketlerin teslim oranı); "karıştırmaya özgü kazanç" iddiası ancak fark-içinde-fark ve mekanizma kapısıyla (`v2/06` §0.4.5).

## 2 · Çalışma biçimi

**Öğrencinin senden beklediği:**
- **Serbest düşün.** Hiçbir belgeye (bu dahil) körü körüne güvenme; iddiaları kodla ya da ölçümle sına. Daha iyi bir yol görürsen öner. Önceki ajanların ortak kusuru fazla itaat ve bayat bilgiyle devam etmekti.
- **Sorunu çöz, raporlayıp bırakma.** Bir kusur bulursan düzelt, ölç, kanıtıyla getir. DESPARETE "yapım aşamasında"; geliştirmek senin işin. Öğrenciye yalnız fikrinin değiştiği yerlerde (kapsam, iddia, ön-kayıt metriği, büyük tasarım değişikliği) önerinle sor.
- **Gerçekçilik esas.** *"Hayal dünyasında İHA yarıştırmıyoruz."* Bir ölçütle gerçekçilik çatışırsa gerçekçi olanı seç, gerekçesini yaz.
- **Öz yaz, kısa ölç.** Aynı bilgi tek yerde. Bir koşu yalnız bir kararı değiştirecekse ve en kısa gerekli hâliyle koşulur.

**Kurallar** (kısa tutuldu; gerekçesi olmayan bir kural görürsen sorgula):
1. Öğrenciyle **Türkçe** konuş; özetler kısa ve kod referanssız.
2. **Git:** okuma komutları (`status`, `diff`, `log`) serbest; commit, push, dal işlemleri **yalnız öğrencide** — gerekince komutu ona ver (tek satır mesaj; bir blokta tek komut).
3. **Her sayı üretici komutuyla** yazılır. **Ölçüm süreci (denetim D-05, öğrenci):** sonucu ya da bir kararı etkileyen her ölçümün ölçütü (`beklenti.md`) ölçmeden önce yazılır ve **koşudan önce öğrencinin commit'iyle** girer (sen komutu verirsin, o atar, sonra koşarsın); sonuçlar ayrı `sonuc.md`ye, beklentiye dokunulmaz; her ölçümden sonra push. Sonuçtan sonra değişen bir ölçüt `v2/06` §10'a yazılır.
4. **Ana deney tohumları 2000–2039 mühürden önce hiçbir protokolle koşulmaz.**
5. **Protokol kâhin bilgisi göremez**; rakip protokoller kaynağına sadık kalır ve senaryoya göre ayarlanmaz; negatif sonuç gizlenmez. Taban protokoller donmuş (`tests2/test_donma.py`); dosyalarından biri değişirse yeni K kaydı + U1 + regresyon.
6. **Uzun koşu** (~30 dk üstü): süresini söyle; iki ağır işi aynı anda koşma (makine 4 performans + 4 verimlilik çekirdeği, havuz 8 işçi; tam test takımı da ağırdır). Uzun koşu dondurulmuş kod kopyasından: `py -3.11 arsiv/teshis/faz4_2026-09-26/dondur.py <klasör>` (`tests2/` dâhil); kopyanın commit'le birebir olduğunu doğrula (örnek `arsiv/teshis/denetim_duzeltme_2026-10-09/kopya_*_ozet.txt`); birden çok uzun adım bir kabuk betiğinde sırayla, her adımın saati `zaman.txt`e.
7. **Simülatörün davranışını değiştiren** değişiklikten sonra regresyon + mimari denetimi; tam test takımı iş kapanışında.
8. **Dosya silme; eskiyen belge `arsiv/`e taşınır.** Paket kurulmaz; indirme öğrencinin izniyle.
9. **Karar:** yeni karar kısa bir kayıtla `v2/kayit/KARAR-GUNLUGU.md`nin sonuna (ne · neden · kim · sayı + komut); geçerli bir kararı değiştiriyorsa `v2/04-KARARLAR.md` de güncellenir; sonra `py -3.11 arsiv/dogrulama/kayit_indeksi.py` (bir kaydın yerini yenisi aldıysa aracın `SUPERSEDE` tablosuna da). Durum değişince yalnız `v2/12` güncellenir.

## 3 · Neyin nerede olduğu

| soru | yer |
|---|---|
| problem, kapsam, başarı ölçütü | `v2/01` |
| **bugün geçerli bütün kararlar** | `v2/04-KARARLAR.md` |
| **durum, plan, sıradaki iş** | `v2/12` (§1.1) |
| simülatör ve referans dünya | `v2/07` · `v2/14` |
| protokolün görebildiği / yapabildiği | `v2/05` · `v2/13` |
| ön-kayıt, metrikler, istatistik | `v2/06` · `v2/08` |
| yöntem ilkeleri ve bilinen tuzaklar | `v2/03` |
| DESPARETE'nin bugünkü yapısı (v0.4.1) | `protokoller/desparete*.py` (sürüm geçmişi `desparete.py` başlığında, profil ve seçenekler V1…V11 `desparete_bayrak.py`de) · günlük K-150…K-172, K-200 |
| taban protokollerin kaynağa sadakati | AODV `arsiv/teshis/aodv_sadakat_2026-09-30/denetim.md` · OLSR `arsiv/teshis/olsr_sadakat_2026-10-09/denetim.md` · beyan tabloları `protokoller/*_bicim.py` |
| bir `K-xxx` atfı ya da bir kararın tarihçesi | `v2/kayit/KARAR-GUNLUGU.md` |

Kod yorumları çoğu zaman uzun tarihçe taşır ("ilk yazımda…"); bugünkü doğru `04` ve kodun kendisidir.

## 4 · Bilinmesi gereken tuzaklar

- **İki dünya:** `Konfig()` varsayılanı ESKİ 1:50 dünyadır; deneyler **referans dünyada** (`referans_2026`). Araçlar dünyayı `--dunya referans_2026` ya da `DESPARETE_DUNYA=referans_2026` ile seçer. 25 Eylül'den önceki bütün sayılar eski dünyanındır.
- **Python 3.11:** `python` komutu başka bir proje için kurulan 3.12'yi açıyor, onda numpy/scipy/pytest yok → bütün komutlar `py -3.11` ile (K-202).
- **Windows:** Python çağrılarında `PYTHONIOENCODING=utf-8` (Türkçe çıktı). `Pool` kullanan betikte `if __name__ == "__main__":`, iç içe havuz yok.
- **Satır sonları karışık** (CRLF/LF) ve korunur; Write aracı LF, Python'un `write_text`i Windows'ta CRLF yazar — dosyayı bayt düzeyinde oku-yaz. Git'te `core.autocrlf=true`; kimlik özetleri satır sonunu normalleştirir.
- **Kabukta heredoc'u tırnaklı ayraçla aç:** tırnaksız heredoc metindeki ters tırnakları komut diye çalıştırır (9 Ekim'de bir köken metnini bozdu). `sed -i` CRLF dosyayı LF'ye çevirebilir; değişikliği Python'la bayt düzeyinde yap.
- **Arka plan işi:** kabuk kesilince Python yaşamaya devam edebilir; bir süreci "öldü" saymadan ya da yeniden başlatmadan önce süreç listesine bak (`Get-CimInstance Win32_Process`), iki kopya koşmasın.
- **Statik kolda sönümleme donuktur** (bağ başına kalıcı tek çekim): tek tohumun sonucu buna çok duyarlıdır. **Kısa pencerede (30 s) tek tohumun PDR'si ±0,15 oynar** (K-224 teşhisi) — tek tohumlu kısa pencere sayısı tek başına hiçbir karara girmez.
- **MAC deneme sayısı:** `yeniden_deneme_siniri` YENİDEN deneme sayısıdır (toplam deneme = sınır + 1); referans dünyada 6 → en çok 7 iletim denemesi = dot11ShortRetryLimit (K-223). Kâhin ve aletler `sınır + 1`'i okur.
- **Regresyon:** `Konfig`e alan eklemek bütün satırların `kurulum_hash`ini değiştirir; köken kovası değişince `teshis.koken_kovalari` oynar — beklenen farkı önceden yaz. Taban `k223`; ondan sonra köken kovaları değişti (K-225), karşılaştırmada `--izin teshis.koken_kovalari` gerekir. Taban dosyaları `ciktilar2/regresyon/`de (git dışı); dondurulmuş kopyada yoktur. Referans dünyada sönümleme blok üreteciyle koşar (K-198), eski dünya birebir.
- **Kâhin (U1 paydası, R'nin aleti):** ETX kâhini hareketli kollarda bağ başına 48 sönümleme örneğiyle (K-215). Kâhin ya da MAC değişirse U1 ve R yeniden ölçülür.
- **Referans dünyanın ayarları:** veri TTL'i 64 (RFC 1700) · kâhin beacon'ı AODV HELLO çerçevesi (84 B, 1 s) · `Konfig.nominal_bag_m` menzil değil, güç çapası ve teşhis birimi.
- **Duyarlılık aracı** kâhin ikilisiyle ölçer: kâhinin göremediği parametreler (saat, kuyruk, TTL) taban protokollerle ölçülür (`arsiv/teshis/faz4_4_*/protokol_*.py`). Oynatma türe göre: olasılık eşikleri kayıp payından, dBm ±3 dB, korelasyon katsayıları zaman sabitinden (K-224) — yeni bir sınırlı parametrede aracın oynatmasını önce kontrol et.
- **Araçlar:** kayıp anatomisi kol başına konfig farkı alır (`aodv@rota_tamponu_kapasitesi=256`), `--kayit` verilince her koşuyu ara kayda yazar, kesilirse sürer; karar bağlarını yeniden denemeli ve tek deneme bandıyla basar · U1 hüküm aracı kayıttaki dünyayla uyuşmazsa reddeder · kâhin grafiği hareket diliminde ve karıştırıcının açık/sessiz geçişinde yenilenir.

## 5 · Doğrulama — referans dünyada geçerli olanlar

| komut (hepsi `py -3.11`, `PYTHONIOENCODING=utf-8`) | beklenen | süre |
|---|---|---|
| `-m pytest tests2 -q` | `1006 passed` (11 Ekim) | ~15 dk (bilgisayar boştayken) |
| `kalibrasyon/mimari_denetimi.py` | `Yapisal ihlal YOK` · SINANMAMIŞ 5 (pencere üçlüsü · RSSI ve dikey GPS hatası, K-233) · borç 0 · kapsam ilanı 13 | < 1 dk |
| `-u kalibrasyon/regresyon_satirlari.py uret <etiket>` ve `karsilastir k232 <etiket> [--izin …] [--degisen …] [--yeni …]` | ilan edilen farklar dışında BİREBİR; beklenen fark karşılaştırmadan önce yazılır (81 vaka; biri çizelgeli evre yolu) | ~45 dk + < 1 dk |
| `arsiv/dogrulama/kayit_indeksi.py --kontrol` | indeks güncel | saniyeler |
| `-u kalibrasyon/evre_metrikleri_kapilari.py 1c` · `… 2c` · `… 3c` (`DESPARETE_DUNYA=referans_2026`) | G1ç · G2ç + G4ç · G3ç `GECTI` (K-224) | 1 sa 45 dk · 2 sa 20 dk · 30 dk |
| `-u kalibrasyon/evre_metrikleri_kapilari.py` (1 · 1p · 2 · 4) | G1 · G1-P · G2 · G4 `GECTI`; G3 referansta anlamsız → `3c` | ~1 sa |
| `-u kalibrasyon/cozunurluk.py --dunya referans_2026 --hucre birincil --tohum 40` | `KULLANILACAK ESIK R = 0.0126` · saklanan sabit TAZE (K-224) | ~70 dk |
| `-u kalibrasyon/duyarlilik.py --dunya referans_2026 birincil <adlar>` | parametre başına DUYARLI / DUYARSIZ / ÖLÇÜLEMEDİ (DUYARSIZ ⇔ \|Δ\| < R ve kendi bandının içinde); sınırdaki kayıt `--tohum 20` | 5 tohumda parametre başına ~17 dk |
| `-u kalibrasyon/aodv_uygunluk.py --dunya referans_2026 --desen <yere_toplama\|esler_arasi> --protokol aodv,olsr,aomdv` · hüküm `… --protokol <p> hukum <kayıt>` | U1 (`v2/04` §5): U1-U iki desende ✅, U1-B yere toplamada TEMİZ (K-224) | 6 sa · 4 sa 15 dk · saniyeler |
| `-u kalibrasyon/kayip_anatomisi.py --dunya referans_2026 [--sinif yok] --kol <kol> --protokoller <p> --tohumlar <…> --kayit <json>` | düşme sebepleri × bölge, karar bağının bandı | hareketli kolda koşu başına ~1 sa |
| `-u kalibrasyon/li_replikasyonu.py --dunya referans_2026` · `-u arsiv/teshis/faz4_2026-09-26/b_li_ayristirma.py <kopya>` | araç: H1 ≈ 0,042 (A8, ARF) TUTMADI · ayrıştırma: sabit hızda 0,1250 TUTTU (K-226) | 4 dk · 3 dk |
| `kalibrasyon/denetim_ornekleme.py` · `kontrol_duzlemi_kapilari.py` · `ust_referans.py --kapi` · `bag_kumesi.py a` (`DESPARETE_DUNYA=referans_2026`) · `anlamlilik_sabitleri.py` · `uretici_duman.py` | 4/4 (C: ED dışarıda 270/270) · 21/21 · üç kapı · G-a/G-b · KAPI GEÇTİ · bütün kesitler (K-226; dumanın regresyon kesiti taban dosyasını çalışılan ağaçta ister) | 5 · 18 · 2 dk · saniyeler · 29 dk |

"İhtiyaç duymadığın ikincil betiklerin veya geçmiş testlerin detayında boğulma; problemin özünü ve bugünkü koda yansımasını kavra."

> Bir şeyi iddia etmeden önce ölç. Ölçemiyorsan iddia etme.
