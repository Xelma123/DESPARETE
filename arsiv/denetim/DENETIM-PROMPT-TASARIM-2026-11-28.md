# Faz 5-3 · yeni tasarımın bağımsız denetiminin istemi

> 28 Kasım 2026 · sıfır bağlamla açılan ayrı bir oturuma ilk mesaj olarak verilir (git dışı kopyası depo kökünde `DENETIM-PROMPT.md`). Denetlenen hâl: tasarım belgeleri `3a71a0b`'deki hâliyle. Rapor `DENETIM-RAPORU-TASARIM-2026-11-28.md`.

---

Sen bu projenin yeni DESPARETE tasarımı için **bağımsız denetçisisin**. Tasarımı sen yazmadın. Görevin bir şeyin doğru olduğunu onaylamak değil; yanlış, eksik, belirsiz, tutarsız ya da kodlanamaz olanı bulmak ve sonunda tek bir soruya gerekçeli hüküm vermek: **yeni tasarım dondurulmaya ve kodlanmaya hazır mı; kod yazılmadan önce ne düzeltilmeli?** Hiçbir şeyi düzeltmeyeceksin.

## 0 · Proje (kısa)

- Lise düzeyinde bir TÜBİTAK 2204-A projesi: karıştırma (jamming) altındaki taktik İHA sürüsünde mesh yönlendirme. Ürün, özgün protokol DESPARETE'nin yeni sürümü. Rakipler donmuş: AODV-k, OLSRv2-b, Babel-a; en güçlüsü Babel. Ölçüm ortamı projenin kendi simülatörü `sim2/` (Python, kesikli olay, 802.11b, referans dünya `referans_2026`, 40 İHA). Telemetri İHA'lardan tek geçide (düğüm 0) gider, komut geçitten İHA'lara.
- Protokol 24 Kasım'dan beri baştan, bileşen bileşen yeniden tasarlandı (K-253). Belgeler:
  - `v2/18-YENI-TASARIM.md`: hedef ve başarı ölçütü (§1.1), kısıtlar (§1.2), kanıt envanteri (§1.3), mimari iskelet ve sözleşme (§1.4), yöntem ve eksiksizlik listesi, yedi bileşenin sorunu, kanıtı, seçenekleri ve kararı (§2.1–2.7);
  - `v2/bilesen/B1`…`B7`: kurallar (B1 komşu ve bağın ölçüsü · B2 karıştırma kanıtı · B3 bağın durumu · B4 yol · B5 iletim kararı · B6 kontrol iletileri · B7 bekletme ve komut);
  - `v2/bilesen/00-DIZIN.md`: değerler, bayraklar, gözlemin kullanımı;
  - `v2/bilesen/01-BUTUNLUK.md`: tasarımı yazanın yedi bileşeni birlikte yaptığı denetim (28 Kasım). Bunu da denetle; ona dayanma.
- Bileşenlerin ana seçenekleri kişinin kararıdır (`v2/18` §2.x'teki "Kararım"). **Kararların kendisini yeniden tartışma.** Bir karar ölçülmüş bir kanıtla ya da birincil kaynakla çelişiyorsa bunu kanıtıyla yaz. Senin konun kâğıtların bu kararları doğru, eksiksiz, tutarlı ve kodlanabilir biçimde kurallara çevirip çevirmediği ve yedi bileşenin birlikte çalışıp çalışmadığı.
- Bugünkü kod yeni tasarımı içermez. Kodda iki önceki sürüm var: v0.4.1 (`protokoller/desparete.py`) ve 5-3'ün ilk tasarımı (`v2/17`, `v2/kural/KK-*`, `protokoller/desparete5*.py`). Yeni tasarım Aşama 4'te yeni modüllerle yazılacak.
- İlk tasarımın kural kâğıtları 17 Kasım'da bağımsız denetimden geçti: `arsiv/denetim/DENETIM-RAPORU-KURAL-2026-11-17.md` (3 engelleyici, 10 önemli, 7 küçük bulgu) ve kapanışı `DENETIM-KURAL-KAPANIS-2026-11-17.md`. O denetimde çıkan türden hataların yeni kâğıtlarda yeniden doğup doğmadığına bak: ∞ ilanın uygulanabilirliği, çıkışı olmayan durum, aynı olayda iki geçiş, niyet döndüremeyen kancada verilen karar.
- Savunulabilir bir tasarım seçimini "bulgu" diye yazma; sorun ile bulguyu ayır. Değerler başlangıçtır: bir değerin "en iyi" olup olmadığı değil, kuralın doğru ve sınanabilir olup olmadığı konu. Tek protokolün ya da tek ölçümün sonucundan sınıf yargısı kurma.

## 1 · Denetlenen hâl ve kapsam

Başlangıçta ve sonda `git rev-parse HEAD` ve `git status --short` al, ikisini rapora koy. Tasarım belgeleri `3a71a0b`'deki hâliyle denetlenir: `git diff --stat 3a71a0b -- v2/18-YENI-TASARIM.md v2/bilesen` boş çıkmalı; çıkmazsa farkı rapora yaz.

1. **Sadakat:** Her kural `v2/18`'deki bir karara ve iskelete (§1.4) dayanıyor mu? Karara aykırı kural, kuralı olmayan karar ya da kararın ötesine geçen sessiz bir tasarım seçimi var mı? Ödünç alınan her kural kaynağıyla tutuyor mu, farklar yazılmış mı: RFC 8966 (`protokol_kaynaklari/rfc8966_babel.txt`; bölüm numaraları kurallarda), RFC 6206 (Trickle), RFC 3561 §6.3, ETX. Babel'in sabitleri `protokoller/babel_bicim.py`de.
2. **Eksiksizlik:** Her kâğıt `v2/18`'in 17 maddelik eksiksizlik listesini gerçekten cevaplıyor mu? Başlığın var olması yetmez.
3. **Durumların tamlığı:** B2'nin kendi durumu, B3'ün bağ durumu, B4'ün adayları, açlığı ve yok sayması, B7'nin bekletmesi için her durum × her olay tanımlı mı? Çakışan geçiş, ölü durum, sonsuz bekleme, gidip gelme var mı? Özellikle şu birleşimlere bak:
   - kendi karıştırılmam ile bağın karıştırılması birlikte;
   - kanal kilidi ile girişim arası geçiş;
   - aynı kancada birden çok olay;
   - bir bileşenin kararının başka bir bileşenin kanıtını kesmesi (sözleşme 4).
4. **Döngüsüzlük ve kara delik (B4, B5, B7):** Şunlar birlikte döngü, sonsuza sayma, kalıcı açlık ya da kara delik üretebilir mi?
   - uygulanabilirlik koşulu;
   - ilanın ömrü ve kendi aralıklarımda yaşın durması (kural 4);
   - yok sayma (kural 10);
   - kural 4a ve 10a'nın istekleri ve isteğin iletilmesi (kural 12);
   - O ve S sınıflarıyla seçim (kural 5);
   - kendi karıştırılmamda isteğin bastırılması (kural 14).

   RFC 8966 §3.5–3.8 ile karşılaştır; karşı örnek kurmaya çalış. Komutun geri izi (B7 kural 6–8) döngüye girebilir mi?
5. **Zaman çizelgesi ve kararlılık:** Kuralları adım adım yürüt: karıştırıcısız ağda, 15 s açık · 15 s sessiz (birincil) ve 10 s açık · 20 s sessiz (dayanıklılık) karıştırıcıda. Bak:
   - B2'nin giriş ve çıkış süreleri, bitin komşulara ulaşması;
   - B3'ün sebepleri ve hariç aralığı;
   - B4'ün geçişleri ve istekleri;
   - B6'nın selam aralığı (0,5 → 2 s) ve olay selamları;
   - B7'nin bekletmesi.

   Gidip gelme, selam seli ya da tur artışı seli var mı? `01-BUTUNLUK` §5'in altı senaryosunu bağımsız olarak yeniden yürüt.
6. **Kodlanabilirlik:** Her girdi protokole gerçekten ve meşru biçimde görünüyor mu, her eylem simülatörde yapılabilir mi? Bak:
   - belgeler: `v2/05-GOZLEM-PENCERESI.md`, `v2/13-KONTROL-DUZLEMI.md`;
   - protokol yüzeyi: `sim2/gozlem/` (`pencere.py`, `protokol.py`, `karar.py`, `kontrol.py`);
   - koşum: `sim2/kosum/kontrol.py`, `dugum.py` (bekletme tamponu), `gonderim.py` (paket kararının anı, vazgeçme), `sim2/cekirdek/olaylar.py` (eşit anlı olayların sırası);
   - aynı arayüzün çalışan örneği: `protokoller/babel.py`.

   Konular:
   - iletilerin alanları, bit sınırları ve boyları (B6);
   - uyandırmalar ve nesil numaraları;
   - `Karar.beklet` ve tamponun dökülmesi;
   - kontrol kancalarının hepsi-ya-hiç kuralı; niyet döndüremeyen kancalar;
   - `kanal_dolulugu_ister`;
   - `cerceve_duyuldu`'nun verdikleri;
   - paket başlığının alanları (`kaynak_sira`, atlama sayısı);
   - tabloların bellek sınırı (komşu, iz, bekletme kaydı, döngü tanısı).

   Kâhin bilgisinin ya da yasak alanın (`olculen_gurultu_w`, K-227) sızması var mı? Kâğıtlardaki ~100 kural ve aralarındaki bağlılık birlikte kodlanabilir ve sınanabilir mi? Kâğıtların sınama listeleri (§13) kuralları kapsıyor mu?
7. **Sayıların dayanağı:** Kâğıtlardaki ve `00-DIZIN`'deki sayısal dayanaklar kaynaklarıyla tutuyor mu? Bir sayıyı yeniden hesaplarsan komutunu yaz. Kaynaklar (`arsiv/teshis/` altında):
   - B2: `faz5_3_b2_isaretler_2026-11-24/sonuc.md`;
   - B3: `faz5_3_b3_bag_olculeri_2026-11-25/sonuc.md`;
   - B5: `faz5_3_b5_iletim_kaybi_2026-11-26/sonuc.md`, `ek_hesap.txt`;
   - B6: `faz5_3_b6_kontrol_bedeli_2026-11-27/kontrol_bedeli.txt`;
   - B7: `faz5_3_b7_bekletme_2026-11-27/bekletme_komut.txt`;
   - bütünlük: `faz5_3_butunluk_2026-11-27/butunluk_hesap.txt`.
8. **Ölçülebilirlik ve mekanizma kapısı:**
   - `00-DIZIN`'in bayrakları her mekanizmayı ayrı kapatabiliyor mu; bir bayrak kapalıyken kalan kurallar tanımlı mı?
   - Sınıflar (karıştırmaya karşı · genel; K-247) doğru mu?
   - `karistirma_katmani` grubu kapalıyken kalan çekirdek eksiksiz bir protokol mü?
   - Mekanizma kapısı (`v2/06` §0.4.5, `v2/18` §1.1), katman kapanınca birincilde `PDR_açık`'ın en az 0,02 düşmesini istiyor. `01-BUTUNLUK` §10'un kestirimine göre bu pay ince: ölçülmüş üst sınırların toplamı ~0,03, ayrıca ölçülmemiş bir pay var. Kestirim savunulabilir mi? Genel bir mekanizmanın katmanın işini yaptığı, böylece kapının kolunu bulandırdığı bir yer var mı?
9. **Kontrol payı:** `01-BUTUNLUK` §2'nin kestirimi (protokolün iletileri ~%3, veri onaylarıyla %6–7) ve varsayımları (selam kaybının bağımsızlığı) savunulabilir mi? %10'luk sınırı aşabilecek bir durum var mı: olay seli, istek seli, çok komşulu düğümde selamın boyu.
10. **Uç durumlar:**
    - başlangıç (soğuk açılış);
    - düğüm kaybı ve dönüşü;
    - geçidin kendisi (geçit karıştırılıyor, geçit kanal kilidinde);
    - 16 bitlik sıra numaralarının sarması;
    - eşit maliyetler;
    - çok komşulu (39) ve tek komşulu düğüm.
11. **Eksikler:** Kodlamaya başlamadan karar gerektiren bir boşluk var mı? Örneğin tanımsız davranış, çakışan zamanlayıcılar ya da olay sırasında belirsizlik (`v2/18` §1.4, `01-BUTUNLUK` §4).

Kapsam dışı:
- `v2/18`'in kararlarının kendisi (ölçülmüş kanıtla çelişmedikçe);
- simülatörün fiziği;
- rakiplerin sadakati;
- ön-kayıt (`v2/06`);
- bugünkü kod.

## 2 · Kurallar

1. **Depoya dokunma.** Tek istisna raporun: `arsiv/denetim/DENETIM-RAPORU-TASARIM-2026-11-28.md`. Git yalnız okuma (`log`, `show`, `diff`, `blame`); commit, dal ve push yok.
2. **Ağır iş yok.** Simülasyon ve tam test takımı koşma. Bir senaryoyu adım adım yürütmek ya da bir sayıyı var olan kayıtlardan (`arsiv/teshis/*/kayit_*.json.gz` ve `.jsonl.gz`; okuyan işlevler aynı klasörün `sonuc_hesap.py`'sinde) yeniden hesaplamak için depo dışında küçük bir Python betiği yazabilirsin. Ana deney tohumları 2000–2039 hiçbir koşuda kullanılmaz.
3. **Doğrula:** Belgelere, bu isteme ve `01-BUTUNLUK`'a körü körüne güvenme. Bir iddiayı kodla, kayıtla ya da birincil kaynakla doğrula. Sabitleri koddan oku; referans dünyanın sabitleri `sim2/kanal/dunya.py`de (MAC en çok 7 deneme yapar).
4. **Ortam (Windows):** `py -3.11`, her çağrıda `PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1`. Paket kurma. Satır sonları karışık (CRLF ve LF).
5. **Dil ve üslup:** Türkçe. Rapor bilgi düzeyinde ve nesnel; emoji ve süs yok; kişi rolleri (yürütücü, ajan, öğrenci) anılmaz.

## 3 · Rapor

- **Başlık bilgisi:** denetlenen commit, başlangıç ve son durum, okunan dosyalar ve kaynaklar.
- **Bulgular**, ağırlığa göre sıralı. Her bulguda:
  - yer (`dosya:satır`);
  - ne yanlış, eksik ya da belirsiz;
  - kanıt (alıntı, adım adım senaryo ya da karşı örnek);
  - ağırlık: **engelleyici** (kod yazılmadan düzelmeli) · **önemli** · **küçük**;
  - somut öneri.
- **Sorunlar:** bulgu olmayan ama bilinmesi gerekenler, ayrı bölümde.
- **Temiz çıkanlar:** denetlenip sorunsuz bulunanlar, kısaca.
- **Doğrulanamayanlar:** sebebiyle; tahmini bulgu gibi sunma.
- **Mekanizma kapısı ve kontrol payı:** madde 8 ve 9 için kısa, ayrı bir değerlendirme.
- **Hüküm:** tasarım dondurulmaya ve kodlanmaya hazır mı; değilse önce yapılacaklar sıralı liste olarak.

Bitince raporun yolunu ve hükmünü kısaca bildir.
