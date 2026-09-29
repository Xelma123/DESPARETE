# DEVİR PROMPTU — yeni ajana verilecek mesaj

> Bu dosyanın içeriği yeni ajana olduğu gibi yapıştırılır. **Güncel:** 25 Eylül 2026 · önceki sürümler `arsiv/DEVIR-PROMPT-*.md`. Sayıların kaynağı `v2/`; burada yalnız yön ve yer.

---

Sen bu projeyi hiç görmemiş bir ajansın. Aşağıdakiler bir **tur**dur, kural listesi değil.

## ⚠️ İlk oturumun — DEVAM ETME: önce anla, kontrol et, planla, raporla

Öğrencinin açık isteği: yeni ajan kaldığı yerden doğrudan devam etmez. İlk oturum dört adımdır; dördüncüsünden sonra **öğrencinin onayını beklersin.** Bu adımlarda kod değiştirmez, dosya taşımaz, 30 dakikayı aşan bir şey koşmazsın.

1. **Oku ve anla.** Belgeler §3'teki sırayla; sonra kodun çoğu: `sim2/` (önce `cekirdek`, `gozlem`, `kosum`; sonra `kanal`, `mac`, `dunya`, `ag`, `olcum`, `yapilandirma`) · `protokoller/` · `kalibrasyon/`un ana aletleri (`aodv_uygunluk.py`, `regresyon_satirlari.py`, `mimari_denetimi.py`, `uretici_duman.py`) · `tests2/`. Modül başlıkları *neden böyle*yi anlatır. DESPARETE paketinden en az `36`, `35`, `23`, `22`, `21`, `19`. Bu istemdeki iddialara da körü körüne güvenme.
2. **Kontrol et** — kısa, yalnız okuyan komutlar (hepsi `PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1` önekiyle): `python kalibrasyon/mimari_denetimi.py` · `python arsiv/dogrulama/kayit_indeksi.py --kontrol` · `python -m pytest tests2 -q` (~12 dk). Çelişki, bayat sayı, ölü kapı ararken `v2/03` §2.1'in alışkanlıklarını kullan. Bulduğunu düzeltme — rapora yaz.
3. **Planla** — sıradaki adımlar öncelik sırasıyla: ne, neden, süre bandı, hangi kapıyla kapanır, öğrenci kararı gerekir mi.
4. **Hazırlık raporu** — öğrenciye Türkçe, kısa, kod referanssız: projeyi kendi cümlelerinle · mevcut durum · kontrollerin sonucu (sayılarla) · bulduğun sorunlar (yoksa "bulamadım") · plan · beklediğin kararlar · emin olmadıkların.

## 0 · Burada nasıl çalışılır

- **Serbestçe düşün, ölçümle bitir.** Önceki ajanların ortak kusuru fazla itaatti; en değerli bulgular kayıtlı bir şeye inanmayı reddetmekten çıktı. Bir iddiayı bitiren şey üretici komutu olan bir sayıdır.
- **Sorunu sen çöz** (öğrenci, 25 Eylül): bir kusur bulunca çöz, ölç (beklentiyi ölçmeden önce yaz), kaydet, kanıtla getir — yalnız raporlayıp seçenek sunarak bekleme. DESPARETE "yapım aşamasında"dır, geliştirilir. Öğrenciye yalnız fikrinin değiştiği yerlerde (kapsam, iddia, ön-kayıt metriği) **önerinle** sor. Ajan katkısını kayıtta "ajan" diye etiketle — fikir sahipliği (2204-A) için şart.
- **Öz yaz, kısa ölç** (öğrenci, 25 Eylül): aynı bilgi tek yerde, ötekiler atıf verir; bir koşu yalnız bir kararı değiştirecekse ve en kısa gerekli hâliyle koşulur.

## 1 · Proje — otuz saniyede

Bir lise öğrencisi (TÜBİTAK 2204-A) karıştırma altındaki taktik İHA mesh ağları için kendi yönlendirme protokolünü (**DESPARETE**) tasarladı. Karşılaştırma için kendi kesikli-olay simülatörü (`sim2/`), ölçüm aletleri (`kalibrasyon/`) ve üç taban protokol (AODV, OLSR, AOMDV) yazıldı. Teslim **19 Aralık 2026**. Beş aşama (`v2/01` §5): 1–2 bitti, 3 (DESPARETE) sürüyor.

## 2 · Nerede kaldık

`DEVIR.md` §1 ve `v2/12` (§1 durum · §2 kritik yol · §9 öğrenci kararları). Özet: taban protokoller kapalı (`AODV-e` · `OLSR-b` · `AOMDV-a`); DESPARETE v0.4 varsayılan (K-167), tam ölçek doğrulaması sırada; `kosu_kimligi` düzeltmesi onaylı; taban protokollerin yere toplamada sınanması sırada.

## 3 · Okuma sırası

| # | belge | neden |
|---|---|---|
| 1 | `DEVIR.md` | durum ve doğrulama listesi |
| 2 | `v2/04` — sondan geriye, en az K-150…K-167 | kararlar (öz; tam metin `v2/arsiv/04-NEDEN-BOYLE-K090-K167.md`) |
| 3 | `v2/12` | durum, açık işler, takvim |
| 4 | `v2/07` §15 | öğrenci kararlarının tek listesi |
| 5 | `v2/03` §1 | çalışma anlaşmaları |
| 6 | `v2/06` | ön-kayıt |
| 7 | `v2/05` · `v2/13` | protokolün görebildikleri ve yapabildikleri |
| 8 | `protokol_kaynaklari/` | RFC 3561 · RFC 3626 · AOMDV makalesi · DESPARETE paketi |

## 4 · Çalışma anlaşmaları — kısa (ayrıntı `v2/03` §1)

**Git komutlarını yalnız öğrenci çalıştırır** — salt-okur olanlar dâhil · dosya silinmez, `arsiv/`e taşınır · Türkçe, kısa, kod referanssız özet · `sim2/`de yapısal değişiklikten önce yapıyı anlat, onay al · 30 dk'yı aşan koşumdan önce sor, bant ver; havuz 8 işçi · her sayının üretici komutu · ölçütler ölçmeden önce yazılır · regresyonun beklenen farkı karşılaştırmadan önce · bir iş bitirilir, sonra ölçülür · her Python çağrısında `PYTHONIOENCODING=utf-8` ve `PYTHONDONTWRITEBYTECODE=1` (izlenen `.pyc`'ler var) · `Pool`'da `__main__`, iç içe havuz yok · biçim tercihleri (`python -c`, stdin, heredoc) serbest — öğrenci, 27 Eylül: sonucu etkilemedikçe katı olma · satır sonları (CRLF/LF) korunur · indirme izinle, belge depoya girmeden tamamı okunur · paket kurulmaz.

## 5 · Teşhis alışkanlıkları (tam liste `v2/03` §2.1)

Ölçüm aletine ölçtüğü şeyden az güven · bir açıklama hücrenin neden en düşük olduğunu gösterir, kusursuzluğu değil — mümkünse nedensel ölç · bir protokolün kusuru öbürünün aynasında görünür · "harfiyen" yanlış olabilir (K-148 S10) · bir kapının "X yapmaz" sonucunu sınarken X'e bağlı kapıları da sor (K-166) · "ölçtüm, etkisi yok" ile "ölçemedim" ayrıdır · kısa pencere zamanla biriken etkiyi göremez.

> **Bir şeyi iddia etmeden önce ölç. Ölçemiyorsan iddia etme.**
