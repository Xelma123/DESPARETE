# Faz 5.0 · DESPARETE'nin açık evre kaybı — beklenti ve karar kuralı (ölçmeden önce)

> 29 Eylül 2026 gece · ajan · U1 bittikten sonra koşulur (iki ağır iş birlikte koşmaz) · dondurulmuş kopyadan
> Komut: `PYTHONIOENCODING=utf-8 py -3.11 -u kalibrasyon/kayip_anatomisi.py --dunya referans_2026 --protokoller desparete,en_guvenilir_kahin --tohumlar 1003,1004,1005,1006 --isci 8 --kayit <bu dizin>/kayit.json`
> Sürüm notu: ilk yazımda karar kuralı yalnız açlık ↔ adaysız ayrımına bakıyordu; aynı gece kısa koşuda (1003, 50 s — ölçüm değil, aletin sınaması) bölümlerin çoğu çok kısa çıktı (medyan 0,2 s), bu da kaybın bölüm uzunluğundan değil onarım tamponunun kotasından gelebileceğini düşündürdü. Kural tam ölçümden ÖNCE iki basamaklı yazıldı.

## Soru

K-200: birincil hücrede DESPARETE açık evrede 0,56, kâhin 0,73; farkın büyüğü `rota_gecersiz` (alan iletilebilir değil). K-202'nin kısa okuması: kayıp, yolu karıştırılan merkezden geçen uzak rölelerde. **Paket alanın hangi durumunda ölüyor ve alan neden iletilemez kalıyor?**

- **onarımda, kota dolu:** alan onarımda (REPAIRING); tampon alan başına en çok 6 ayrı paket tutar (`21` §2.4, K-157), fazlası düşer. Toplayıcı rölede saniyede onlarca paket geçer → 1–2 s'lik bir onarım kotayı taşırır.
- **ulaşılamaz:** onarım 6 s içinde bitmedi. Sebebi ya **açlık** (aynı turdan geçerli ilanı olan ACTIVE komşu var ama P < FD koşulu dışlıyor — Babel'in "spurious starvation"ı, RFC 8966 §2.5; çaresi kaynaktan yeni tur, §3.8.2.1 MUST; v0.2'de onarım edinimi kapalı, K-161) ya da **adaysız** (hiçbir komşunun geçerli ilanı yok).

## Ölçülen (alet K-202 + 29 Eylül gece eki)

Pencerede `rota_gecersiz` anında alanın durumu × evre · pencerede başlayan onarım bölümleri: evre × giriş (açlık / adaysız) × son (aynı tur / yeni tur / koşu sonu; `+U` ulaşılamaz oldu), süreler · evre × etki alanı tabloları · DESPARETE'nin iç sayaçları.

## Karar kuralı (4 tohum toplamı, açık evre)

1. `rota_gecersiz` düşüşlerinin **≥ %50'si alan onarımdayken** → ilk mekanizma **onarım tamponunun kapasitesi**: kaybı kota taşması yapıyor, onarımın uzunluğu değil. Aday: alan başına sayı kotası yerine süreye bağlı tutma (onarım bölümü en çok `T_repair_max`; simülatörün ortak tamponu zaten 64 paket · 30 s) ya da kotanın toplayıcı röledeki akış sayısına oranlanması. Ablasyon bayrağıyla; güvenlik değişmezlerine dokunmaz.
2. **≥ %50'si ulaşılamazken** → ulaşılamaz bölümlerin girişine bakılır: iletilemez düğüm-saniyesinin ≥ %50'si açlık girişliyse **açlıkta tur isteği** (Babel §3.8.2.1–3.8.2.2; istek taşkın değil, uygulanamaz ilanın sahibine tek alıcılı, oradan ardıl zinciriyle geçide; geçitte hız kapısı — tasarım paketi TG-04); değilse adaysız bölümlerin yapısı (komşuların aynı anda geri çekilmesi mi, bölünme mi) ölçülür.
3. İkisi de %50'nin altındaysa (karışık) → büyük paydan başlanır, ikincisi sıradaki mekanizma olur.

Seçilen mekanizma öğrenciye tasarım önerisi olarak götürülür (büyük tasarım değişikliği).

## Öngörü

`rota_gecersiz`in çoğu (%55–80) alan onarımdayken, kota taşmasından; kalan ulaşılamazken ve orada açlık girişli pay yüksek. Kâhinle fark (açık evrede ~0,17) tamamen kapanmaz: iletim başarısızlığı kâhin düzeyinde, kalan fark rota kararının kalitesinden.
