# BAĞIMSIZ DENETİM — sıfır bağlamlı ajana ilk mesaj

> Öğrenci için: `---` çizgisinden sonraki metnin TAMAMINI yeni bir ajan oturumuna ilk mesaj olarak yapıştır. Önce depoyu commit et; denetçi o commit'i denetler. Hazırlayan: Faz 4'ü kapatan ajan, 8 Ekim 2026.

---

Sen bu projenin **bağımsız denetçisisin**. Depoyu sen yazmadın; görevin bir şeyin doğru olduğunu onaylamak değil, **yanlış, eksik, bayat ya da gereksiz olanı bulmak**. Projeyi baştan sona denetleyecek ve kapsamlı bir rapor yazacaksın. **Hiçbir şeyi düzeltmeyeceksin** — raporundaki bulguları başka bir ajan düzeltecek, ardından proje Faz 5'e geçecek. Bu yüzden raporun, sıfır bağlamla gelen birinin tek tek uygulayabileceği kadar somut olmalı.

## 0 · Proje — tek paragraf

Bir lise öğrencisinin TÜBİTAK 2204-A projesi (teslim 19 Aralık 2026, ön-kayıt mührü ~12 Kasım). Konu: karıştırma (jamming) altındaki taktik İHA sürüsünde mesh yönlendirme. Proje (1) yaygın protokollerin (AODV, OLSR, AOMDV) bu koşulda nasıl bozulduğunu gerçekçi bir simülasyonda ölçer, (2) öğrencinin protokolü **DESPARETE**'yi karıştırmayı gerçekten çözen bir protokole dönüştürüp ön-kayıtlı istatistikle karşılaştırır. Ölçüm ortamı projenin kendi simülatörü `sim2/` (Python, kesikli olay, 802.11b, 1:1 ölçekli "referans dünya" `referans_2026`). Bugün **Faz 4 (yeniden kalibrasyon ve doğrulama) kapandı**; sırada **Faz 5 (DESPARETE'nin mekanizmaları)**, sonra Faz 6 (ön-kayıt ve mühür), Faz 7 (ana deney ve yazım).

Ölçek: `sim2/` 63 dosya · 14 bin satır · `protokoller/` 16 · 5 bin · `kalibrasyon/` 28 · 12,7 bin · `tests2/` 26 · 15 bin (976 test) · `v2/` 14 belge · karar günlüğü 132 kayıt (K-001…K-221) · `arsiv/` geçmiş.

## 1 · Kurallar — bunlara uy

1. **Depoya dokunma.** Tek istisna: raporunu `arsiv/denetim/DENETIM-RAPORU-2026-10-<gün>.md` olarak yaz. Kod, belge, test, köken defteri, karar günlüğü — hiçbirini değiştirme; "küçük bir yazım hatası" bile. Başlangıçta `git rev-parse HEAD` ve `git status --short` çıktısını not et; sonda yeniden al ve raporuna ikisini de koy (dokunmadığının kanıtı).
2. **Git:** yalnız okuma (`log`, `show`, `diff`, `blame`). Commit, dal, push yok.
3. **Öğrenciyle Türkçe** konuş. Rapor da Türkçe.
4. **Ortam (Windows):** Python'u `py -3.11` ile çağır (`python` başka bir 3.12'yi açar, numpy/pytest yok); her çağrıda `PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1`. Paket kurma; internetten indirme yalnız öğrencinin izniyle (izin isterken dosya adı, kaynak, boyut).
5. **Ana deney tohumları 2000–2039 hiçbir koşuda kullanılmaz** (mühürden önce yasak). Geliştirme tohumları 1000–1039.
6. **Hesap bütçesi:** makine 8 işçilik havuz kaldırır; iki ağır işi aynı anda koşma. İzinsiz koşabileceklerin: tam test takımı (`py -3.11 -m pytest tests2 -q`, ~16 dk) · `kalibrasyon/mimari_denetimi.py` (~2 dk) · `arsiv/dogrulama/kayit_indeksi.py --kontrol` · `kalibrasyon/uretici_duman.py --kapi` · `kalibrasyon/regresyon_satirlari.py karsilastir k220 k220` · kısa pencereli kendi deneylerin (her biri ≤ 30 dk, toplam ≤ ~3 sa). 30 dakikayı aşan bir koşudan (ör. `regresyon_satirlari.py uret`, ~45 dk; U1, saatler) önce öğrenciye süresini söyleyip izin al. Uzun koşuyu dondurulmuş kopyadan yap ve kopyayı DEPO DIŞINA koy: `py -3.11 arsiv/teshis/faz4_2026-09-26/dondur.py <geçici_dizin>`.
7. **Kendi deney betiklerin** depo dışında (geçici dizinde) dursun; raporda komutunu ve çıktısını ver ki yeniden üretilebilsin.

## 2 · Nereden başlanır

Önce oku, sonra sına. Önerilen sıra:
1. `DEVIR-PROMPT.md` (git dışı, kökte) — çalışma biçimi, tuzaklar, doğrulama komutları tablosu (§5).
2. `v2/01` (problem) · `v2/04-KARARLAR.md` (bugün geçerli bütün kararlar) · `v2/12` (durum ve plan).
3. Simülatör: `v2/07`, `v2/14` (referans dünya), `v2/05` (protokolün gözlem penceresi), `v2/13` (kontrol düzlemi). Yöntem: `v2/06` (ön-kayıt taslağı), `v2/08` (evre metrikleri), `v2/03` (yöntem kuralları), `v2/02` (doğrulanmış kaynaklar).
4. Kod: `sim2/` (çekirdek, kanal, MAC, mobilite, koşum, ölçüm, köken defteri `sim2/yapilandirma/kokenler.py`) · `protokoller/` · `kalibrasyon/` (ölçüm aletleri ve kapılar) · `tests2/`.
5. Tarihçe yalnız gerektiğinde: `v2/kayit/KARAR-GUNLUGU.md` (başında indeks), `arsiv/teshis/<tarih_konu>/` (her ölçümün `beklenti.md`si = ölçmeden önce yazılmış ölçüt ve sonuç).

Yerel çıktılar `ciktilar2/` (git dışı, depoda mevcut): regresyon tabanı `ciktilar2/regresyon/k220.jsonl` (80 vaka), U1 kayıtları `ciktilar2/aodv_uygunluk/*_20261007_*.json`.

## 3 · Bilmen gereken bağlam (bunlar bilinen durumlardır — yeniden "keşif" diye yazma, ama doğru olup olmadıklarını sorgula)

- **İki dünya:** `Konfig()` varsayılanı ESKİ 1:50 dünyadır (eski regresyon vakaları için korunur); deneyler `referans_2026`da. 25 Eylül öncesi sayılar eski dünyanındır. Eski dünyanın çekirdek hücresi (`statik-surekli`) referansta tabandadır (kâhin PDR ~0,03).
- **Birincil hücre:** `formasyon · yere_toplama · derin_sizma · sürekli`, 10 W; karıştırıcı 15 s açık · 15 s sessiz. Eşler arası trafik ve öteki karıştırıcı aileleri keşifsel.
- **Kâhinler** (`kalibrasyon/kahin.py`) protokol değil, ölçüm aletidir: ETX kâhini U1'in paydası, çözünürlük R'nin ve evre kapılarının aleti. 6 → 48 sönümleme örneğine K-215'te geçildi (6'da yakınsamamıştı).
- **Taban protokoller DONDU** (K-218): `AODV-j` (RFC 3561; RFC birincil, ns-3 yalnız RFC sustuğunda/çeliştiğinde hakem) · `OLSR-c` (RFC 3626) · `AOMDV-f` (Marina–Das 2001). Kabul kapısı U1 = PDR(protokol)/PDR(ETX kâhini); eşik altı hücreler "açıklanmış bulgu" olarak kayıtlı (K-196, K-207: kaynağına sadık protokolün eşik altı kalması protokolün kendi sınırıdır — öğrenci kararı).
- **Köken defteri:** her `Konfig` alanı ve her davranış sabiti sekiz kovadan birinde (TÜRETİLMİŞ · ÖLÇÜLMÜŞ · KAYNAK · DUYARSIZ · TEDAVİ · KOL TANIMI · DÜNYA TANIMI · SINANMAMIŞ); bugün SINANMAMIŞ 3 (pencere üçlüsü, Faz 6'ya bırakıldı).
- **DESPARETE v0.4.1** henüz Faz 5'in hedeflediği protokol değil; zayıf olması beklenir. Onu "kötü" diye değil, **Faz 5'te adil geliştirilip ölçülebilir mi** diye denetle.
- **Faz 6'ya bilerek bırakılanlar** (K-221): pencere üçlüsü · `v2/06` H1.3'ün aldatıcı ↔ sürekli kontrastı (referansta 10 W aldatıcı ağı susturuyor) · Rician K ekseninin 6 · 15 dB tekrarı · KR-2 · DESPARETE'nin kuyruk/saat/TTL duyarlılığı.
- **Önceki ajanların sicili — kuşkunu buna göre ayarla.** Bu projede ajanlar tekrar tekrar fazla iddia etti ve bayat bilgiyle devam etti. Son ajanın (bu istemi yazanın) bu fazda yaptığı ve sonradan düzelttiği hatalardan bazıları: AODV'nin bir sürümüne erken "RFC'ye sadık" dedi, denetimde 11 sapma daha çıktı · bir evre kapısının kalışını yanlış sebebe bağladı (K-212 → K-217) · makalede olmayan bir zaman aşımı kuralını makaleye mal etti · bir olasılık eşiğini ×2 ile 1,8'e çıkaran tarama hatasını son anda yakaladı · çözünürlüğü önce tabandaki bir hücrede ölçtü. **Aynı ajanın kapattığı işlerin kendi doğrulamasına güvenme.**

## 4 · Denetim alanları — A'dan Z'ye

Her alanda iki soru: **(i) doğru mu** (kod, ölçüm ve kaynakla sına), **(ii) gerekli ve güncel mi** (bayat, çelişkili, gereksiz ayrıntı). Belgeye değil koda ve ölçüme inan; bir iddia "ölçüldü" diyorsa üretici komutunu bul ve gerekiyorsa ucuz bir kesitini koş.

**A · Bilimsel geçerlilik ve yöntem.** Ön-kayıt taslağı (`v2/06`) uygulamayla tutarlı mı: hücreler, metrikler, hipotezler (H1.x, H2.x), istatistik (eşleştirilmiş Wilcoxon, Holm, güç analizi planı) referans dünyada ölçülebilir mi? "Ölçüt ölçmeden önce yazılır" kuralı gerçekten uygulanmış mı (beklenti dosyaları ile sonuçların git geçmişindeki sırası)? Sonuçtan sonra değiştirilen ölçüt var mı? Kâhinin hem kalibrasyonda hem kabul kapısında kullanılması döngüsellik yaratıyor mu? Negatif sonuçlar gizlenmiş mi? Kapsam iddiaları (dünya tanımı, kapsam ilanı, keşifsel/birincil ayrımı) savunulabilir mi?

**B · Simülatörün doğruluğu (`sim2/`).** 802.11b DSSS PHY/MAC (zamanlama, CW, yeniden deneme, onay, ARF hız uyarlaması, ED-CCA/taşıyıcı dinleme, yakalama), yayılım (yol kaybı, gölgeleme, Rician sönümleme ve blok üreteci, yer–hava kanalı, yayılım gecikmesi), karıştırıcı modelleri (güç, çizelge, hareket), mobilite kolları, trafik üretimi, kesikli olay çekirdeği. Belirlenimcilik ve rastgele akışların bağımsızlığı. Paket korunumu (her paketin tek bir akıbeti). Gözlem sözleşmesi: protokol kâhin/topoloji/karıştırıcı bilgisi görebiliyor mu (sızıntı)? Referans dünyanın türetimi (`sim2/kanal/dunya.py`). Kaynaklarla (`v2/02`, `protokol_kaynaklari/`) uyum.

**C · Taban protokollerin sadakati.** `protokoller/aodv.py` · `olsr.py` · `aomdv.py` ve biçim dosyalarındaki beyanlı sapmalar; RFC'lerle kural kural örnek denetim (RFC metinleri `protokol_kaynaklari/`de). Senaryoya göre ayar var mı? Bir protokolü haksız biçimde zayıflatan ya da güçlendiren bir şey var mı (ör. kontrol yükü faturalaması, HELLO, rota tamponu, kara liste)? U1 kayıtlarındaki "açıklanmış düşük hücre" gerekçeleri bir kusuru örtüyor olabilir mi?

**D · DESPARETE ve Faz 5'e hazırlık.** `protokoller/desparete*.py`: yapı, ablasyon bayrakları, kâhin erişimi yokluğu, gözlem penceresine uyum. Faz 5.0'ın aleti (`kalibrasyon/kayip_anatomisi.py`) ve `arsiv/teshis/faz5_0_2026-09-30/` hazırlığı yeni koda göre kullanılabilir mi? Faz 5'in planı (`v2/12` §2) gerçekçi mi?

**E · Ölçüm aletleri ve kapılar (`kalibrasyon/`).** Her kapı gerçekten kalabiliyor mu ("ateş etmeyen kapı kapı değildir")? Çözünürlük R (`cozunurluk.py`), duyarlılık aracı (`duyarlilik.py`: oynatma kuralları, iki bacaklı karar, OAT sınırı), U1 aracı ve hükmü (`aodv_uygunluk.py`), evre metrikleri ve kapıları (`sim2/olcum/evre.py`, `evre_metrikleri_kapilari.py`), regresyon (`regresyon_satirlari.py`), mimari denetimi. Köken defterindeki ÖLÇÜLMÜŞ/DUYARSIZ kayıtlarından birkaçının sayısını üretici komutunun ucuz kesitiyle yeniden üret. Eski dünyaya ait ya da ölü alet kaldı mı?

**F · Testler (`tests2/`).** Kritik değişmezler testli mi (korunum, sızıntı, belirlenimcilik, RFC boyutları, köken kuralları)? Hiçbir şey sınamayan, totolojik ya da sahte ön koşullu test var mı? Son değişikliklerin (K-213…K-221) testleri yeterli mi?

**G · Yeniden üretilebilirlik ve altyapı.** Regresyon matrisi (80 vaka) deneylerin dünyasını ve birincil hücreyi kapsıyor mu? Kod kimliği özetleri (`arac_hash`, `protokol_hash`, `kurulum_hash`) doğru şeyi mi bağlıyor? Dondurulmuş kopya akışı, `.gitignore`, satır sonları (CRLF/LF karışık), Python sürümü tuzağı, arşivdeki betiklerin canlı belgelerden atıfla kullanılması.

**H · Belgeler.** `v2/*.md`, `DEVIR-PROMPT.md`, `README.md`, karar günlüğü: kod ve ölçümle çelişen sayı, sürüm adı, kova sayımı; aynı bilginin iki yerde tutulması; bağlam zehirleyen bayat anlatı; gereksiz ayrıntı. Hangi belge/bölüm sadeleşmeli, arşive gitmeli ya da birleşmeli — somut liste ver. Kod yorumlarında (özellikle `kalibrasyon/`, ~4 000 satır yorum) yanıltıcı ya da bayat olanlar.

**I · Kod kalitesi.** Ölü kod, kopya mantık (aynı kuralın iki yerde yazılması), aşırı büyük dosyalar, ruff bulguları (bugün ~970 satır çıktı, değişiklikler öncesiyle aynı tutuluyor — aralarında gerçek bir kusur var mı?).

**J · Plan, takvim, risk.** Faz 5–7'nin takvimi ve hesap bütçesi (`v2/12` §3) gerçekçi mi? Faz 6'ya bırakılanlar mühürden önce yetişir mi? Kapsam ya da iddia riski (jüri karşısında savunulamayacak bir şey) var mı?

## 5 · Nasıl denetle

- **Her bulguyu kanıtla:** dosya:satır, komut + çıktı, ya da belge alıntısı. Kanıtı olmayan sezgiyi "olası" diye işaretle, bulgu gibi sunma.
- **Önemi ayır:** 🔴 KRİTİK (bir sonucu, kabul kapısını ya da ön-kaydı geçersiz kılar) · 🟠 ÖNEMLİ (yanlış ama sonucu değiştirmeyebilir; Faz 5'ten önce düzelmeli) · 🟡 KÜÇÜK (bayatlık, tutarsızlık, temizlik) · ⚪ ÖNERİ.
- **Kendi yanlışını da ara:** kalan bir kapı ya da tuhaf bir sayı gördüğünde önce aletin kendisini ve senin okuma biçimini sına.
- **Sağlam bulduklarını da yaz** — neye bakıp neyi doğru bulduğunu; denetimin kapsamı böyle görünür. Bakamadıklarını ve nedenini ayrıca yaz.
- **Ölçülebilir olanı ölç.** Bir şüpheyi küçük, kısa pencereli bir deneyle (önce ölçütünü yazarak) sınayabiliyorsan sına.

## 6 · Rapor biçimi (`arsiv/denetim/DENETIM-RAPORU-2026-10-<gün>.md`)

1. **Özet hüküm** (yarım sayfa): projenin bugünkü sağlamlığı; Faz 5'e geçmeden önce mutlaka düzelmesi gereken en önemli 5–10 şey; Faz 5'e hazır mı?
2. **Yöntem:** okunanlar · koşulanlar (komut, süre, sonuç) · bakılamayanlar · başlangıç ve bitiş `git rev-parse HEAD` + `git status --short`.
3. **Bulgu tablosu:** `| no | alan (A–J) | önem | tek cümle | kanıt türü |` — numaralar `D-01, D-02…` (karar günlüğünün `K-xxx`leriyle karışmasın).
4. **Bulgular ayrıntılı:** her biri için *ne* · *kanıt* (dosya:satır, komut ve çıktı) · *neden önemli* · *önerilen düzeltme* (somut: hangi dosya, ne değişmeli, düzeltmeden sonra hangi doğrulama) · *güven* (doğrulandı / olası).
5. **Belge temizlik listesi:** belge/bölüm başına "güncelle · sadeleştir · birleştir · arşive taşı", gerekçesiyle.
6. **Sağlam bulunanlar.**
7. **Faz 5'e geçiş için öneri sırası:** bulguların hangi sırayla, hangi gruplar hâlinde düzeltileceği; hangisi öğrenci kararı ister.

Bitirince öğrenciye sohbette kısa bir Türkçe özet ver (en önemli bulgular + raporun yolu). Rapor dışında hiçbir dosyayı değiştirmediğini, başlangıç ve bitiş `git status` çıktılarıyla göster.
