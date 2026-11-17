# Faz 5-3 · kural kâğıtlarının bağımsız denetiminin istemi

> 17 Kasım 2026 · sıfır bağlamla açılan ayrı bir oturuma ilk mesaj olarak verildi. Denetlenen hâl `94c0ed6`. Rapor `DENETIM-RAPORU-KURAL-2026-11-17.md`.

---

Sen bu projenin Faz 5-3 kural kâğıtları için **bağımsız denetçisisin**. Kâğıtları sen yazmadın. Görevin bir şeyin doğru olduğunu onaylamak değil; yanlış, eksik, belirsiz, tutarsız ya da kodlanamaz olanı bulmak ve sonunda tek bir soruya gerekçeli hüküm vermek: **kural kâğıtları kodlamaya hazır mı; kod yazılmadan önce ne düzeltilmeli?** Hiçbir şeyi düzeltmeyeceksin.

## 0 · Proje (kısa)

- Lise düzeyinde bir TÜBİTAK 2204-A projesi: karıştırma (jamming) altındaki taktik İHA sürüsünde mesh yönlendirme. Ürün, özgün protokol DESPARETE'nin yeni sürümü. Rakipler donmuş: AODV-k, OLSRv2-b, Babel-a (en güçlüsü Babel). Ölçüm ortamı projenin kendi simülatörü `sim2/` (Python, 802.11b, dünya `referans_2026`, 40 İHA, telemetri İHA'lardan tek geçide, komut geçitten 4 düğüme).
- Tasarım kararları `v2/17-TASARIM-KARARLARI.md`de (kimlik, üç ilke, T-1…T-20; 5-2'de bağımsız denetimden geçti, `arsiv/denetim/DENETIM-RAPORU-5-2-2026-11-17.md` ve kapanışı). Kararlar kişiye aittir; **kararların kendisini yeniden tartışma.** Senin konun kural kâğıtlarının o kararları doğru, eksiksiz, tutarlı ve kodlanabilir biçimde kurallara çevirip çevirmediği.
- Kural kâğıtları `v2/kural/`: `KK-00-DIZIN.md` (başlangıç değerleri, gözlemin kullanımı, ablasyon bayrakları) · `KK-01-BAG.md` (bağın durum makinesi ve ETX) · `KK-02-SELAM.md` · `KK-03-KANIT.md` (karıştırma kanıtı) · `KK-04-ROTA.md` (ardıl, döngüsüzlük, açlık) · `KK-05-BEKLETME-KOMUT.md`. Kâğıtlar üç kez kendi içinde denetlendi ve düzeltildi (`git log` 71a398e → 94c0ed6); her turda yeni sorun çıktı, bu yüzden bağımsız göz isteniyor.
- Savunulabilir bir tasarım seçimini "bulgu" diye yazma; sorun ile bulguyu ayır. Değerler başlangıçtır ve A/B'de ayarlanacaktır; bir değerin "en iyi" olup olmadığı değil, kuralın doğru ve sınanabilir olup olmadığı konu.

## 1 · Denetlenen hâl ve kapsam

Denetlenen hâl: `main` @ `94c0ed6` (çalışma ağacı temiz). Başlangıçta ve sonda `git rev-parse HEAD` ve `git status --short` al; ikisini rapora koy.

1. **Sadakat:** Her kural `v2/17`'deki bir karara (T-n, ilkeler) ve `v2/17` §7 açılış listesine dayanıyor mu? Bir karara aykırı kural, kuralı olmayan karar ya da kararın ötesine geçen sessiz bir tasarım seçimi var mı?
2. **Durum makinesinin tamlığı (KK-01, KK-03):** Her durum × her olay için davranış tanımlı mı? Çakışan geçişler (aynı anda iki koşul), ölü durum, sonsuz bekleme, gidip gelme (salınım) var mı? KK-03'ün "sebebe göre bitti" tablosu bütün giriş yollarını kapsıyor mu? Kendi karıştırılmam (KK-01 kural 9) ile bağın karıştırılması (kural 7) birlikte olunca ne oluyor?
3. **Döngüsüzlük ve kara delik (KK-04):** FD'nin ilan edilen maliyetle tanımı, seçili rotanın turunun ilanı, uygulanamaz ilanın en çok 5 s yok sayılması, hatırlanan kaliteyle dönüş, oransal isteğe bağlı geçiş ve tur isteğinin yanıtı birlikte döngü, sonsuza sayma ya da kalıcı kara delik üretebilir mi? `protokol_kaynaklari/rfc8966_babel.txt` (§3.5, §3.7, §3.8) ile karşılaştır; bir karşı örnek kurmaya çalış.
4. **Kararlılık:** 15 s açık · 15 s sessiz ve 10 s açık · 20 s sessiz karıştırıcı çizelgelerinde ve karıştırıcısız ağda kuralların zaman çizelgesini adım adım yürüt: tespit ve dönüş süreleri, selam aralığı, tur artışı, veri tetiğinin cezası, KÖTÜ ↔ OLAĞAN ↔ KARIŞTIRILIYOR geçişleri. Gidip gelme ya da selam seli var mı?
5. **Kodlanabilirlik:** Her girdi protokole gerçekten ve meşru biçimde görünüyor mu, her eylem simülatörde yapılabilir mi? Bak: `v2/05-GOZLEM-PENCERESI.md`, `v2/13-KONTROL-DUZLEMI.md`, `sim2/gozlem/` (`pencere.py`, `protokol.py`, `karar.py`, `kontrol.py`), `sim2/kosum/kontrol.py`, `sim2/kosum/dugum.py` (bekletme tamponu), `protokoller/babel.py` (aynı arayüzün çalışan bir örneği). Mesaj alanlarının bit sınırları, dinamik zamanlayıcı, `Karar.beklet`, kontrol kancalarının hepsi-ya-hiç kuralı, `kosum_beaconi`. Kâhin bilgisinin protokole sızması var mı?
6. **Sayıların dayanağı:** Kâğıtlardaki sayısal dayanaklar kaynaklarıyla tutuyor mu (teşhis (d)'nin eşikleri `arsiv/teshis/faz5_2_isaretler_2026-11-16/sonuc.md` ve `sonuc_hesap.txt`; Babel sabitleri `protokoller/babel_bicim.py`; RFC 6719, RFC 6206)?
7. **Ölçülebilirlik:** `KK-00`'ın ablasyon bayrakları her mekanizmayı ayrı açıp kapatabiliyor mu; bir bayrak kapalıyken kuralların geri kalanı tanımlı kalıyor mu? Sınıflar (karıştırmaya karşı · genel; K-247) doğru mu? A/B ölçütleri (`17` T-19, `v2/12` Faz 5) kâğıtlarla uyumlu mu?
8. **Eksikler:** Kodlamaya başlamadan karar gerektiren bir boşluk var mı (tanımsız davranış, çakışan zamanlayıcılar, sayılmamış uç durum: başlangıç, düğüm kaybı, geçidin kendisi, sıra numarasının sarması)?

Kapsam dışı: `v2/17`'nin kararlarının kendisi, simülatörün fiziği, rakiplerin sadakati, ön-kayıt.

## 2 · Kurallar

1. **Depoya dokunma.** Tek istisna raporun: `arsiv/denetim/DENETIM-RAPORU-KURAL-2026-11-17.md`. Git yalnız okuma (`log`, `show`, `diff`, `blame`); commit, dal ve push yok.
2. **Ağır iş yok.** Simülasyon ve tam test takımı koşma. Bir senaryoyu adım adım yürütmek için depo dışında küçük bir Python betiği yazabilirsin. Ana deney tohumları 2000–2039 hiçbir koşuda kullanılmaz.
3. **Ortam (Windows):** `py -3.11` ve her çağrıda `PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1`. Paket kurma. Satır sonları karışık (CRLF/LF).
4. **Dil ve üslup:** Türkçe. Rapor bilgi düzeyinde ve nesnel; emoji ve süs yok; kişi rolleri (yürütücü, ajan, öğrenci) anılmaz.

## 3 · Rapor

- **Başlık bilgisi:** denetlenen commit, başlangıç ve son durumu, okunan dosyalar ve kaynaklar.
- **Bulgular**, ağırlığa göre sıralı. Her bulguda:
  - yer (`dosya:satır`);
  - ne yanlış, eksik ya da belirsiz;
  - kanıt (alıntı, adım adım senaryo ya da karşı örnek);
  - ağırlık: **engelleyici** (kod yazılmadan düzelmeli) · **önemli** · **küçük**;
  - somut öneri.
- **Sorunlar:** bulgu olmayan ama bilinmesi gereken noktalar, ayrı bir bölümde.
- **Temiz çıkanlar:** denetlenip sorunsuz bulunanlar, kısaca.
- **Hüküm:** kural kâğıtları kodlamaya hazır mı; değilse önce yapılacaklar sıralı liste olarak.
- Doğrulayamadığın her şeyi "doğrulanamadı" diye ve sebebiyle yaz; tahmini bulgu gibi sunma.

Bitince raporun yolunu ve hükmünü kısaca bildir.
