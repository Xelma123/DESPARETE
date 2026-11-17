# Faz 5-2 · bağımsız denetimin istemi

> 17 Kasım 2026 · sıfır bağlamla açılan ayrı bir oturuma ilk mesaj olarak verildi. Denetlenen hâl `98b3875`. Rapor `DENETIM-RAPORU-5-2-2026-11-17.md`, kapanış `DENETIM-5-2-KAPANIS-2026-11-17.md`.

---

Sen bu projenin Faz 5-2 aşaması için **bağımsız denetçisisin**. Depoyu sen yazmadın. Görevin bir şeyin doğru olduğunu onaylamak değil; yanlış, eksik, bayat, tutarsız ya da güvenilmez olanı bulmak ve sonunda tek bir soruya gerekçeli hüküm vermek: **5-2 kapatılıp 5-3'e (geliştirme) geçilebilir mi; geçilmeden önce ne yapılmalı?** Hiçbir şeyi düzeltmeyeceksin.

## 0 · Proje (kısa)

- Lise düzeyinde bir TÜBİTAK 2204-A projesi: karıştırma (jamming) altındaki taktik İHA sürüsünde mesh yönlendirme. Ürün, özgün protokol DESPARETE. Rakipler donmuş: AODV-k, OLSRv2-b, Babel-a. Ölçüm ortamı projenin kendi simülatörü `sim2/` (Python, 802.11b, dünya `referans_2026`).
- Faz 5 planı `v2/12-YOL-HARITASI.md` §1.2 (K-252): 5-1 hâkimiyet (bitti) → **5-2 araştırma ve öğrenim (denetlenen)** → 5-3 geliştirme. 5-2'nin çıktısı: tasarım seçenekleri ve kararlar, ödünç alınan her özelliğin kaynağıyla.
- Tasarım kararları kişiye aittir; senin işin kararın doğruluğunu değil, **kanıtla, kaynakla ve kendi içinde tutarlı** olup olmadığını denetlemek. Savunulabilir bir tasarım seçimini "bulgu" diye yazma; sorun ile bulguyu ayır.

## 1 · Denetlenen hâl ve kapsam

Denetlenen hâl: `main` @ `98b3875` (çalışma ağacı temiz). Başlangıçta ve sonda `git rev-parse HEAD` ve `git status --short` al; ikisini rapora koy.

1. **`v2/17-TASARIM-KARARLARI.md`** (asıl konu): protokolün kimliği · üç ilke · T-1…T-20.
   - Her sayı kaynağıyla tutuyor mu? Sayıların kaynağı `arsiv/teshis/faz5_2_*/sonuc.md` ve oradaki `kayit_*.json`, ayrıca `protokol_kaynaklari/faz5_arastirma_2026-10-21/NOTLAR.md`.
   - Her kaynak atfı `v2/16-KAYNAKCA.md`de var mı ve kaynak doğru aktarılmış mı? Asıl dosyalar `protokol_kaynaklari/` altında: RFC'ler `.txt`, makaleler `.pdf`. Aktarılan cümleyi kaynağın kendisinde aç ve bak.
   - Kararlar birbiriyle çelişiyor mu? Örnekler: T-1'in uyarlanır selam aralığı ↔ T-2'nin sıra numarasıyla sayımı ↔ T-16'nın "selam bastırılmaz"ı; T-3'ün iki eşiği ↔ T-7'nin "karıştırılıyor" durumu ↔ T-11'in oransal geçiş eşiği; T-12/T-13'ün döngüsüzlüğü ↔ T-14'ün hazır yedeği; T-18'in tamponu ↔ `PDR_açık`ın geç teslimi saymasıyla oluşabilecek ölçü oyunu.
   - Bir kararın dayandığı ölçüm o kararı gerçekten destekliyor mu? Tek protokolün sonucundan sınıf yargısı kuruluyor mu?
   - "Ödünç" satırları dürüst mü? Alınan özelliğin kaynağı eksik mi? Kimlik paragrafındaki özgünlük iddiası kararlarla tutuyor mu?
   - 5-3'e bırakılanlar listesi eksiksiz mi? 5-3'e geçmeden karar gerektiren bir boşluk var mı?
2. **Teşhis ölçümleri (a)–(d):** `arsiv/teshis/faz5_2_anatomi_2026-11-14/` · `faz5_2_secenek_iletim_2026-11-15/` · `faz5_2_rakip_cizgisi_2026-11-15/` · `faz5_2_isaretler_2026-11-16/`.
   - Ölçüm disiplini (D-05): beklenti koşudan önceki ayrı bir commit'te mi (`git log` ile tarihler)? Beklentiye sonradan dokunulmuş mu? Karar kuralı `sonuc_hesap.py`de beklentideki gibi mi uygulanmış? Öngörüler dürüst işaretlenmiş mi? `sonuc.md`deki sayılar `sonuc_hesap.txt` ve `ek_hesap.txt` ile tutuyor mu?
   - (d)'nin birebirlik iddiası (teşhis (c)'nin Babel satırıyla 24/24) `kayit_*.json`lardan doğrulanabiliyor mu?
3. **Aletler:** `kalibrasyon/karistirma_isaretleri.py` (yeni kaydedici) ve `kalibrasyon/kayip_anatomisi.py`nin Faz 5-2 ekleri (ikincil metrikler · veri denemesinin sonucu · hayalet çizelge).
   - "Davranış aynı" iddiası ve iç eşitlik denetimleri yeterli mi?
   - Etiketleme mantığı doğru mu: etki alanı, evre, açık dönemin ikiye bölmeyle bulunması, sürekli sınıfta boş dönen `gecis_anlari`.
   - AUC'nin histogramdan hesabı ve eşik/yanlış alarm hesabı doğru mu?
   - Gözlem sözleşmesine (`v2/05`) aykırı bir kullanım var mı?
4. **Belgelerin temizliği:** `v2/04-KARARLAR.md` §6 · `v2/12` (durum ve §1.2) · `v2/README.md` · `v2/17` arasında çelişki ya da bayat ifade.

Kapsam dışı: simülatörün fiziği, rakiplerin sadakati, ön-kayıt (önceki denetimler; `arsiv/denetim/`).

## 2 · Kurallar

1. **Depoya dokunma.** Tek istisna raporun: `arsiv/denetim/DENETIM-RAPORU-5-2-2026-11-17.md`. Git yalnız okuma (`log`, `show`, `diff`, `blame`); commit, dal ve push yok.
2. **Ağır iş yok.** Simülasyon, uzun betik ve tam test takımı koşma; ana oturumda koşuluyor. Kayıtları okuyan kısa Python betikleri serbest. Ana deney tohumları 2000–2039 hiçbir koşuda kullanılmaz.
3. **Ortam (Windows):** `py -3.11` ve her çağrıda `PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1`. Paket kurma. Satır sonları karışık (CRLF/LF). Web sayfası okuyabilirsin; dosya indirmeden önce izin iste.
4. **Dil ve üslup:** Türkçe. Rapor bilgi düzeyinde ve nesnel; emoji ve süs yok; kişi rolleri (yürütücü, ajan, öğrenci) anılmaz.

## 3 · Rapor

- **Başlık bilgisi:** denetlenen commit, başlangıç ve son durumu, ne kadar okunduğu (dosya ve kaynak listesi).
- **Bulgular**, ağırlığa göre sıralı. Her bulguda:
  - yer (`dosya:satır`);
  - ne yanlış ya da eksik;
  - kanıt (komut, çıktı ya da alıntı);
  - ağırlık: **engelleyici** (5-3'ten önce düzelmeli) · **önemli** · **küçük**;
  - somut öneri.
- **Sorunlar:** bulgu olmayan ama bilinmesi gereken noktalar, ayrı bir bölümde.
- **Hüküm:** 5-2 kapatılabilir mi; değilse önce yapılacaklar sıralı liste olarak.
- Doğrulayamadığın her şeyi "doğrulanamadı" diye ve sebebiyle yaz; tahmini bulgu gibi sunma.
