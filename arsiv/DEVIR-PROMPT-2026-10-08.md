# BAŞLANGIÇ — bu projede çalışacak ajana

> Öğrenci bu dosyayı yeni bir ajana ilk mesaj olarak verir. Güncel: 8 Ekim 2026. Durum burada tekrarlanmaz: `v2/12`.

## 0 · İlk iş

1. **Gerekli belgeleri oku ve projeyi anla** — §3'teki haritadan: önce `v2/01`, `v2/04-KARARLAR.md`, `v2/12`, sonra simülatör ve protokoller için `v2/07`, `v2/14`, `v2/05`, `v2/13`, yöntem için `v2/06`, `v2/08`, `v2/03`. Anlamak için gerektiği kadar koda bak.
2. **Nerede kaldığımızı anla** — `v2/12` §1 ve §1.1.
3. **Bundan sonra ne yapacağımıza dair bir plan yap.**
4. **İlk cevabında hiçbir dosyayı değiştirme.** Öğrenciye kısa bir özet ver: projeden ne anladığın, nerede kaldığımız, planın ve emin olmadığın noktalar. Öğrencinin onayını bekle.

Arkada koşan iş yok.

## 1 · Proje

Bir lise öğrencisinin TÜBİTAK 2204-A projesi, teslim **19 Aralık 2026**. Konu: karıştırma (jamming) altındaki taktik İHA sürüsünde mesh yönlendirme. Sürü telemetrisini yer istasyonuna (geçit) taşır, komutlar ters yönde gider; yer ve hava karıştırıcıları bağları bozar ya da kanalı kilitler. Proje iki şey yapar: (1) yaygın protokollerin (AODV, OLSR, AOMDV) bu koşullarda nasıl bozulduğunu gerçekçi bir simülasyonda ölçer; (2) öğrencinin protokolü **DESPARETE**'yi karıştırmayı gerçekten çözen bir protokole dönüştürüp istatistiksel olarak karşılaştırır. Ölçüm ortamı projenin kendi simülatörü `sim2/` (Python, kesikli olay; 802.11b telsiz, gerçek ölçekli referans dünya).

## 2 · Çalışma biçimi

**Öğrencinin senden beklediği:**
- **Serbest düşün.** Hiçbir belgeye (bu dahil) körü körüne güvenme; iddiaları kodla ya da ölçümle sına. Daha iyi bir yol görürsen öner. Önceki ajanların ortak kusuru fazla itaat ve bayat bilgiyle devam etmekti.
- **Sorunu çöz, raporlayıp bırakma.** Bir kusur bulursan düzelt, ölç, kanıtıyla getir. DESPARETE "yapım aşamasında"; geliştirmek senin işin. Öğrenciye yalnız fikrinin değiştiği yerlerde (kapsam, iddia, ön-kayıt metriği, büyük tasarım değişikliği) önerinle sor.
- **Gerçekçilik esas.** *"Hayal dünyasında İHA yarıştırmıyoruz."* Bir ölçütle gerçekçilik çatışırsa gerçekçi olanı seç, gerekçesini yaz.
- **Öz yaz, kısa ölç.** Aynı bilgi tek yerde. Bir koşu yalnız bir kararı değiştirecekse ve en kısa gerekli hâliyle koşulur.

**Kurallar** (kısa tutuldu; gerekçesi olmayan bir kural görürsen sorgula):
1. Öğrenciyle **Türkçe** konuş; özetler kısa ve kod referanssız.
2. **Git:** okuma komutları (`status`, `diff`, `log`) serbest; commit, push, dal işlemleri **yalnız öğrencide** — gerekince komutu ona ver.
3. **Her sayı üretici komutuyla** yazılır. Sonucu ya da bir kararı etkileyen ölçümün ölçütü ölçmeden önce yazılır.
4. **Ana deney tohumları 2000–2039 mühürden önce hiçbir protokolle koşulmaz.**
5. **Protokol kâhin bilgisi göremez**; rakip protokoller kaynağına sadık kalır ve senaryoya göre ayarlanmaz; negatif sonuç gizlenmez.
6. **Uzun koşu** (~30 dk üstü): süresini söyle; iki ağır işi aynı anda koşma (makine 4 performans + 4 verimlilik çekirdeği, havuz 8 işçi). Uzun koşu dondurulmuş kod kopyasından: `py -3.11 arsiv/teshis/faz4_2026-09-26/dondur.py <klasör>` (`tests2/` dâhil kopyalar); birden çok uzun adım bir kabuk betiğinde sırayla, her adımın saati `zaman.txt`e.
7. **Simülatörün davranışını değiştiren** değişiklikten sonra regresyon + mimari denetimi; tam test takımı iş kapanışında.
8. **Dosya silme; eskiyen belge `arsiv/`e taşınır.** Paket kurulmaz; indirme öğrencinin izniyle.
9. **Karar:** yeni karar kısa bir kayıtla `v2/kayit/KARAR-GUNLUGU.md`nin sonuna (ne · neden · kim · sayı + komut); geçerli bir kararı değiştiriyorsa `v2/04-KARARLAR.md` de güncellenir; sonra `python arsiv/dogrulama/kayit_indeksi.py`. Durum değişince yalnız `v2/12` güncellenir.

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
| bir `K-xxx` atfı ya da bir kararın tarihçesi | `v2/kayit/KARAR-GUNLUGU.md` |

Kod yorumları çoğu zaman uzun tarihçe taşır ("ilk yazımda…"); bugünkü doğru `04` ve kodun kendisidir.

## 4 · Bilinmesi gereken tuzaklar

- **İki dünya:** `Konfig()` varsayılanı ESKİ 1:50 dünyadır; deneyler **referans dünyada** (`referans_2026`). Araçlar dünyayı `--dunya referans_2026` ya da `DESPARETE_DUNYA=referans_2026` ile seçer. 25 Eylül'den önceki bütün sayılar eski dünyanındır.
- **Python 3.11:** `python` komutu başka bir proje için kurulan 3.12'yi açıyor, onda numpy/scipy/pytest yok → bütün komutlar `py -3.11` ile (aşağıdaki tablo dâhil; K-202).
- **Windows:** Python çağrılarında `PYTHONIOENCODING=utf-8` (Türkçe çıktı). `Pool` kullanan betikte `if __name__ == "__main__":`, iç içe havuz yok.
- **Satır sonları karışık** (CRLF/LF) ve korunur; Write aracı ve Python'un `write_text`i biçimi değiştirir — CRLF dosyaları bayt düzeyinde geri çevir.
- **Arka plan işi:** kabuk kesilince Python yaşamaya devam edebilir; bir süreci "öldü" saymadan ya da yeniden başlatmadan önce süreç listesine bak (`Get-CimInstance Win32_Process`), iki kopya koşmasın.
- **Statik kolda sönümleme donuktur** (bağ başına kalıcı tek çekim): tek tohumun sonucu buna çok duyarlıdır; hücre düzeyindeki bir okumayı tohumlar arası varyansla birlikte yap.
- **Regresyon:** `Konfig`e alan eklemek bütün satırların `kurulum_hash`ini değiştirir; beklenen farka önceden yaz. Referans dünyada sönümleme blok üreteciyle koşar (K-198), eski dünya birebir.
- **Kâhin (U1 paydası, R'nin aleti):** ETX kâhini hareketli kollarda bağ başına 48 sönümleme örneğiyle (K-215; 6 örnekte yakınsamamıştı ve hem U1 oranlarını hem G2ç'yi bozuyordu — K-217). Kâhin sayısı değişirse U1 ve R yeniden ölçülür.
- **Referans dünyanın K-215 ayarları:** veri TTL'i 64 (RFC 1700) · kâhin beacon'ı AODV HELLO çerçevesi (84 B, 1 s) · `Konfig.nominal_bag_m` (K-220'ye kadar `iletim_menzili_m`; menzil değil, güç çapası).
- **Duyarlılık aracı** kâhin ikilisiyle ölçer: kâhinin göremediği parametreler (saat, kuyruk, TTL) taban protokollerle ölçülür (`arsiv/teshis/faz4_4_*/protokol_*.py`); olasılık eşikleri kayıp payından oynatılır.
- **Araçlar:** kayıp anatomisi kol başına konfig farkı alır (`aodv@rota_tamponu_kapasitesi=256`) ve `--kayit` verilince her koşuyu ara kayda yazar, kesilirse kaldığı yerden sürer · U1 hüküm aracı kayıttaki dünyayla uyuşmazsa reddeder · kâhin grafiği hareket diliminde ve karıştırıcının açık/sessiz geçişinde yenilenir.

## 5 · Doğrulama — referans dünyada geçerli olanlar

| komut | beklenen | süre |
|---|---|---|
| `python -m pytest tests2 -q` | `976 passed` | ~15 dk (bilgisayar boştayken) |
| `python kalibrasyon/mimari_denetimi.py` | `Yapisal ihlal YOK` · SINANMAMIŞ 12 · borç 0 · kapsam ilanı 12 (K-204, K-215) | 1–5 dk |
| `python -u kalibrasyon/regresyon_satirlari.py uret <etiket>` ve `karsilastir k220 <etiket> [--izin …] [--degisen …]` | ilan edilen farklar dışında BİREBİR; beklenen fark karşılaştırmadan önce yazılır | ~30–45 dk + < 1 dk |
| `python arsiv/dogrulama/kayit_indeksi.py --kontrol` | indeks güncel | saniyeler |
| `DESPARETE_DUNYA=referans_2026 python -u kalibrasyon/evre_metrikleri_kapilari.py` (1 · 1p · 2 · 3 · 4) | G1 · G1-P · G2 · G4 `GECTI`; G3 referansta anlamsız (eski çekirdek hücre tabanda) → yerine `3c` | ~1 sa |
| `DESPARETE_DUNYA=referans_2026 python -u kalibrasyon/evre_metrikleri_kapilari.py 1c` · `… 2c` · `… 3c` | G1ç · G2ç + G4ç · G3ç `GECTI` (K-217, K-219) | ~2 sa 30 dk · ~2 sa 30 dk · ~30 dk |
| `python -u kalibrasyon/cozunurluk.py --dunya referans_2026 --hucre birincil --tohum 40` | `KULLANILACAK ESIK R = 0.0142` · saklanan sabit TAZE (K-216) | ~70 dk |
| `python -u kalibrasyon/duyarlilik.py --dunya referans_2026 birincil <adlar>` | parametre başına DUYARLI / DUYARSIZ / ÖLÇÜLEMEDİ (DUYARSIZ ⇔ \|Δ\| < R ve kendi bandının içinde) | parametre başına ~17 dk (20 koşu) + taban ~8 dk |
| `python -u kalibrasyon/li_replikasyonu.py --dunya referans_2026` · `python -u arsiv/teshis/faz4_2026-09-26/b_li_ayristirma.py <kopya>` | araç: H1 0,0427 (A8, ARF) TUTMADI · ayrıştırma: sabit hızda (A8-arf) **0,1188 TUTTU** (84 B beacon; 32 B'la 0,1270, K-219) | 4 dk · 3 dk |
| `DESPARETE_DUNYA=referans_2026 python -u kalibrasyon/denetim_ornekleme.py` · `… kontrol_duzlemi_kapilari.py` · `… ust_referans.py --kapi` · `… bag_kumesi.py a` · `python -u kalibrasyon/anlamlilik_sabitleri.py` · `python -u kalibrasyon/uretici_duman.py` | 4/4 (C: ED dışarıda 270/270) · 21/21 · üç kapı · G-a/G-b · KAPI GEÇTİ · bütün kesitler (K-219) | 5 · 21 · 2 dk · saniyeler · 28 dk |
| `python -u kalibrasyon/aodv_uygunluk.py --dunya referans_2026 --desen <desen> --protokol <p>` · hüküm `… hukum <kayıt>` | U1 (`v2/04` §5) | saatler · saniyeler |

Ayıklananlar (Faz 4.5, K-219): adım 9 kapanışı · onay semantiği (eski dünyanın tarihçesi) · kâhin tavanı (yerini U1'in kâhin sütunu tuttu) · karıştırıcı çalışma noktası (yerini K-186 tuttu).

"İhtiyaç duymadığın ikincil betiklerin veya geçmiş testlerin detayında boğulma; problemin özünü ve bugünkü koda yansımasını kavra."

> Bir şeyi iddia etmeden önce ölç. Ölçemiyorsan iddia etme.
