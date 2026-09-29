# DEVİR PROMPTU — yeni ajana verilecek mesaj

> Bu dosyanın içeriği yeni ajana olduğu gibi yapıştırılır. **Güncel:** 28 Eylül 2026 (gece) · önceki sürümler `arsiv/DEVIR-PROMPT-*.md`. Sayıların kaynağı `v2/`; burada yalnız yön ve yer.

---
(bu proje hala geliştirilme aşamasındadır ve yeni fikirlere ve geliştirmelere açık olabilirsin yani öğrenci onayını aldığım müddetçe mantıklı ve projeye katkı sağlayacak geliştirmeler konusunda serbest ol)
Sen bu projeyi hiç görmemiş bir ajansın. **Bu istem bir görev listesi değil.** Öğrencinin senden ilk beklentisi, projeye **sahibi kadar hâkim olman**: problemi, öğrencinin protokolünü, simülatörü, yöntemi ve bugüne nasıl gelindiğini kendi cümlelerinle, kaynağını göstererek anlatabilmen. İş listesi (§4.2) bu anlayışın üstüne kurulur. Anlamadan uygulanırsa önceki ajanların ortak hatası tekrarlanır: fazla itaat, bayat bilgiyle devam etmek, "şuradan kaldık" diye bağlamsız iş yapmak.

## ⚠️ İlk oturumun — DEVAM ETME: önce projeye hâkim ol

Öğrencinin açık isteği: yeni ajan kaldığı yerden doğrudan devam etmez.
- İlk oturumda kod değiştirmez, dosya taşımaz, 30 dakikayı aşan bir şey koşmazsın; sonunda öğrencinin onayını beklersin.
- **Acele etme.** Okuma bitmeden plan yapma. Oturumun uzun sürmesi beklenen bir şeydir; yarım anlayışla hız kazanılmaz.

1. **Oku** — §2'deki sırayla, *nedenden nereye*: önce problem ve protokol, sonra simülatör ve yöntem, **en son** durum ve iş listesi. Ardından kodun çoğunu oku (§2'nin sonu). Modül başlıkları *neden böyle*yi anlatır.
2. **Anladığını sına** — §3'teki soruların her birine belgeye ya da koda dayanarak cevap verebilmelisin. Cevaplayamadığın soru, okumanın bitmediğini gösterir: geri dön, oku.
3. **Kontrol et** — kısa, yalnız okuyan komutlar (hepsi `PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1` önekiyle):
   - `python kalibrasyon/mimari_denetimi.py`
   - `python arsiv/dogrulama/kayit_indeksi.py --kontrol`
   - `python -m pytest tests2 -q` (~15–25 dk)

   Çelişki, bayat sayı, ölü kapı ara (`v2/03` §2.1'in alışkanlıkları). **Bu istem dâhil hiçbir belgeye körü körüne güvenme**; bir iddiayı kodla ya da ölçümle sına. Bulduğunu düzeltme, rapora yaz.
4. **Planla** — §4.2'deki iş listesini eleştirerek:
   - Sıra yanlışsa, bir iş gereksizse ya da eksik bir iş varsa söyle.
   - Her iş için: ne, neden, süre bandı, hangi kapıyla kapanır, öğrenci kararı gerekir mi.
5. **Hazırlık raporu** — öğrenciye Türkçe, kısa, kod referanssız:
   - **Projenin kendi cümlelerinle anlatımı**, bir sayfa kadar: problem; DESPARETE'nin fikri ve bugünkü hâli; simülatörün neyi neden modellediği; yöntem; 25 Eylül'deki yön değişikliği ve Faz 4'e nasıl gelindiği. Öğrenci hâkimiyetini buradan ölçer.
   - Mevcut durum.
   - Kontrollerin sonucu, sayılarla.
   - Bulduğun sorunlar (yoksa "bulamadım").
   - Eleştirdiğin plan.
   - Beklediğin kararlar.
   - **Anlamadıkların ve emin olmadıkların** — dürüstçe. "Her şeyi anladım" demek, bir şeyi atladığının işaretidir.

## 0 · Burada nasıl çalışılır

- **Serbestçe düşün, ölçümle bitir.** Önceki ajanların ortak kusuru fazla itaatti; en değerli bulgular kayıtlı bir şeye inanmayı reddetmekten çıktı. Bir iddiayı bitiren şey üretici komutu olan bir sayıdır.
- **Sorunu sen çöz** (öğrenci, 25 Eylül): bir kusur bulunca çöz, ölç (beklentiyi ölçmeden önce yaz), kaydet, kanıtla getir — yalnız raporlayıp seçenek sunarak bekleme. DESPARETE "yapım aşamasında"dır, geliştirilir. Öğrenciye yalnız fikrinin değiştiği yerlerde (kapsam, iddia, ön-kayıt metriği) **önerinle** sor. Ajan katkısını kayıtta "ajan" diye etiketle — fikir sahipliği (2204-A) için şart.
- **Öz yaz, kısa ölç** (öğrenci, 25 Eylül): aynı bilgi tek yerde, ötekiler atıf verir; bir koşu yalnız bir kararı değiştirecekse ve en kısa gerekli hâliyle koşulur.
- **Gerçekçilik esas** (öğrenci, 25–27 Eylül): *"hayal dünyasında İHA yarıştırmıyoruz"*; bir ölçütle gerçekçilik çatışırsa gerçekçi olanı seç, gerekçesini yaz (K-185: *"ölçütü boşver, en mantıklı ve gerçekçi olana önem ver"*).

## 1 · Projenin büyük resmi — okumaya başlamadan önce haritan

Bu bölüm bir haritadır, kaynak değildir. Her cümlenin doğrusu parantezdeki belgede; oradan doğrula.

- **Kim, ne için:** Bir lise öğrencisinin TÜBİTAK 2204-A projesi, teslimi **19 Aralık 2026**. Karıştırma (jamming) altındaki taktik İHA sürülerinde mesh yönlendirme protokollerinin davranışını inceleyen bir araştırma projesi. Ürün öğrencinin kendi protokolü **DESPARETE**; AODV, OLSR ve AOMDV kıyas tabanıdır. **Protokol tasarımı öğrencinindir**; protokolü öğrenci ajanla birlikte yapacak o yüzden ajanda projede özgürce öğrenciye sunma ve onayını alma şartıyla geliştirebilir (`v2/01`, `v2/03` §1).
- **Problem:** Sürü telemetrisini yer istasyonuna (geçit) taşır, komutlar ters yönde gider. Hava ve yer karıştırıcıları (sürekli, darbeli, taramalı, reaktif, aldatıcı) bağları bozar ya da kanalı kilitler. Soru: paket nerede ve neden ölüyor, bir protokol bunu gözlemleyip kaçınabilir mi (`v2/01` §2–4, `v2/14` tehdit bölümü)? Genel olarak projenin asıl olayı: Standart protokollerin gerçek iha sahasında karıştırma veya farklı koşullarda nasıl performans sergilediğinin yazdığımız python simülasyonu ile ölçümü ve tasarlayacağımız desparete protokolünün standart protokollere kıyasla ne gibi artılarının olduğunun istatisliksel ve bilimsel biçimde tübitak 2204 a yarışmasında sunumu.
- **DESPARETE:** Öğrencinin tasarım paketinde (`protokol_kaynaklari/DESPARETE_TASARIM_PAKETI/`, dizin `00_…INDEX`, tek okumalık özet `36`) tanımlı. Öğeleri:
  - bağ maliyeti ve risk;
  - tazelik;
  - döngüsüzlüğü garanti eden potansiyel;
  - uyarlanır postür (NORMAL / CAUTION / PROTECT);
  - kontrol mesajları.

  **Bugünkü kod hâli v0.4.1.** Tam ölçekte çöküş (K-160) sonrası yalın profil, onarımlar ve komut geri izi eklendi (K-161…K-172). **Eksikleri (Faz 5'in konusu):** karıştırmaya özgü kanıt (C_jam), PROTECT'in çok yolu, pasif dinleme, bağ ömrü tahmini (`v2/12` §2 madde 8, §3 Faz 5).
- **Simülatör (`sim2/`):** Öğrencinin projesi için yazılmış kesikli olaylı bir simülatör.
  - **Katmanlar:** olay çekirdeği; kanal fiziği (yol kaybı, gölgeleme, sönümleme, girişim, karıştırıcı, işlem kazancı, ED-CCA, hız uyarlaması); 802.11b DCF MAC; koşum; ölçüm.
  - **Üç ilke:**
    - **Gözlem sözleşmesi:** protokol yalnız gerçek bir telsizin ve otopilotun verebileceğini görür; karıştırıcıyı ve gerçek bağ kalitesini göremez; sızıntı testle kapalıdır (`v2/05`, `v2/13`).
    - **Korunum defteri:** üretilen her paket teslim, kuyrukta ya da kapalı bir düşme sebebiyle hesaplanır.
    - **Kâhinler:** gerçek kanalı bilen üst referanslar. "Kâhin − protokol" farkı, körlüğün bedelidir.
- **Taban protokoller:** RFC 3561 (AODV), RFC 3626 (OLSR) ve Marina–Das 2001 (AOMDV) kaynaklarına sadık gerçeklendi (K-136…K-149). **U1** bir protokolün kâhine oranını sınar: **U1-U** uygunluk kapısıdır, **U1-B** başarım bulgusudur (K-137).
- **Yöntem:**
  - Ön-kayıt (`v2/06`): aileler, hipotezler, metrikler, istatistik; mühür ~12 Kasım.
  - Her ölçümün beklentisi ölçmeden önce yazılır.
  - Köken defteri: her parametrenin kovası TÜRETİLMİŞ / ÖLÇÜLMÜŞ / KAYNAK / SINANMAMIŞ …
  - Mimari denetim ve regresyon her değişiklikten sonra.
  - Geliştirme tohumları 1000–1010; ana deney tohumları 2000–2039 mühürden önce **koşulmaz** (`v2/03`, `v2/06`, `v2/07` §11).
- **Tarih:**
  - Aşama 1–2 (22 Eylül'e kadar) **eski 1:50 dünyada** yapıldı.
  - 25 Eylül'de öğrenci yönü değiştirdi (K-168): simülatör önce 1:1, kaynaklı bir taktik sürüye (**referans dünya `referans_2026`**, `v2/14`) oturacak, sonra DESPARETE karıştırmayı gerçekten çözecek.
  - Onaylı plan Faz 0–7 (`v2/12`). Faz 0–3 26 Eylül'de bitti; bugün Faz 4'teyiz (§4).
  - **25 Eylül'den önceki bütün sayılar eski dünyanındır**; bugünküyle karıştırma.

## 2 · Okuma sırası — nedenden nereye

| # | belge | neden |
|---|---|---|
| 0 | `v2/README.md` | belge haritası |
| 1 | `v2/01` | problem · kapsam · başarı ölçütü · simülasyon–gerçeklik beyanı |
| 2 | `protokol_kaynaklari/DESPARETE_TASARIM_PAKETI/` — önce `00_TASARIM_PAKETI_INDEX`, `00_DESPARETE_GOLDEN_RULES`, öğrencinin ilk metni `DESPARETE – Protokol Taslağı v0.md`; sonra `36`, `35`, `23`, `22`, `21`, `19`, `13`, `15`, `17`, `40` | öğrencinin protokolü ve fikirleri; hangi fikrin öğrenciye ait olduğunu buradan bil |
| 3 | `v2/13` · `v2/05` | protokolün yapabildikleri ve görebildikleri (sözleşmeler) |
| 4 | `v2/07` (§15 öğrenci kararları, §18 `sim2/` kuralları) | simülatörün tasarımı ve sınırları |
| 5 | `v2/14` · `v2/15` · `v2/16` · `v2/02` · `v2/10` | referans dünya ve her sayısının kaynağı · gerçekçilik yapı paketi · kaynakça · doğrulanmış kaynaklar · literatür |
| 6 | `v2/06` · `v2/08` · `v2/09` | ön-kayıt · evre metrikleri · Li replikasyonu (aletin dış çapası) |
| 7 | `v2/03` | çalışma anlaşmaları, bilimsel ilkeler, teşhis alışkanlıkları |
| 8 | `v2/12` | plan (Faz 0–7), durum, öğrenci kararları, hesap bütçesi |
| 9 | `v2/04` — karar kaydı | başındaki indeksten bütün kayıtları gez. **K-168…K-191'i tam oku.** Eski dönemden yöntemi kuranları da oku (tam metin `v2/arsiv/04-NEDEN-BOYLE-K090-K167.md`): K-101/102 ölçek · K-125…K-137 kalibrasyon ve U1 · K-145…K-149 taban protokoller · K-158…K-167 DESPARETE |
| 10 | `DEVIR.md` · `arsiv/teshis/faz4_2026-09-26/plan.md` | durum, doğrulama listesi, Faz 4'ün satır satır planı ve beklenti dosyaları |
| 11 | `protokol_kaynaklari/` — RFC 3561, RFC 3626, Marina–Das 2001 | taban protokollerin kaynağı (en az ilgili bölümler) |

**Kod** (belgelerden sonra):
- `sim2/` — önce `cekirdek`, `gozlem`, `kosum`; sonra `kanal`, `mac`, `dunya`, `ag`, `olcum`, `yapilandirma`.
- `protokoller/` — DESPARETE ve üç taban protokol.
- `kalibrasyon/`un ana aletleri: `dunya_secimi.py`, `aodv_uygunluk.py`, `kahin.py`, `kayip_anatomisi.py`, `regresyon_satirlari.py`, `mimari_denetimi.py`.
- `analiz/`, `tests2/`.

Bir paketi doğumundan teslimine ya da düşüşüne kadar kodda baştan sona izle.

## 3 · Hâkimiyet soruları — rapordan önce hepsine cevap verebilmelisin

1. Hangi sürü, hangi tehdit, hangi trafik? Proje neyi **kapsamıyor**, başarı ölçütü ne? Simülasyon–gerçeklik beyanı ne diyor?
2. Özgünlük iddiası tam olarak ne, ne değil? ns-3 ve benzerleriyle dürüst karşılaştırma nasıl kurulmuş (K-168)?
3. DESPARETE bir paketi nasıl yönlendirir? Maliyet ve risk, potansiyel ve döngüsüzlük, postürler, kontrol mesajları. v0.1'den v0.4.1'e neler değişti ve neden? Faz 5 neyi ekleyecek? Hangi fikirler öğrencinin taslağında, hangileri ajan önerisi?
4. Bir paketin kodda yolu: doğum, kuyruk, MAC denemesi, kanal (SINR, PER), alım, teslim ya da düşüş. Korunum defterinin düşme sebepleri neler, "diğer" neden yok?
5. Protokol neyi görebilir, neyi göremez? Sızıntı nasıl önleniyor ve sınanıyor? Kontrol düzlemi protokole ne yaptırır?
6. Referans dünyanın temel sayıları nereden geliyor: telsiz gücü, anten, duyarlılık, alan 33 km, N = 40, karıştırıcı 10 W? Eski 1:50 dünyadan farkı ne, neden bırakıldı?
7. Kâhinler ne ölçer? U1-U ile U1-B farkı ne, "açıklanmış düşük hücre" ne demek? Referans dünyada U1'de ne çıktı?
8. Ön-kayıt: aileler, hipotezler, birincil metrik (KR-2 açık), istatistik planı; mühürden önce ne kapanmalı (`v2/06` §9)?
9. Köken defterinin kovaları ne, SINANMAMIŞ neden sıfırlanmalı? Mimari denetim ve regresyon neyi yakalar?
10. Bugün: Faz 4'te ne bitti, ne kaldı? Hangi karar öğrencide? Son beş K kaydı ne öğretti?

## 4 · Nerede kaldık — EN SON oku

Ayrıntı `DEVIR.md` §1, `v2/12` §1 ve `v2/04` K-192…K-197. Faz 0–3 kapandı (K-169…K-181). **Faz 4 sürüyor.**
- **4.1–4.2 bitti** (K-186…K-188): alan 33 km, birincil hücre `formasyon · yere_toplama · derin_sizma · sürekli` 10 W · Li sabit hızda tutuyor, Bianchi ±%0,6.
- **4.3:** U1 yere toplama ESKİ kod hâlleriyle koşuldu (K-190, K-191; U1-U 🟢 üçünde, U1-B 🔴). 28 Eylül'de öğrenci kararları (K-192: eşik değişmez · KR-1 zarf prosedürü · tasarım bedeli açıklamadır · önce yazılım, pahalı koşu sonra). Sonra: OLSR teşhisi (K-193: geçide rotanın aralıklı boşalması, kusur adayları elendi) · AODV §6.8 kara liste + AOMDV U1–U4 (K-194) · kâhin karıştırıcı çizelgesini görüyor (K-195) · OLSR §13 varsayılan kapalı, OLSR U1-B "açıklanmış, sıralamasız", evre hata payı kümelenmeye dayanıklı + G1-P 🟢 (K-196) · anatomi aracında açık/sessiz evre, karıştırıcı geçişleri yapısal değişiklik istemiyor, performans ölçüldü (K-197).
- **Kod hâlleri:** `AODV-f` · `OLSR-c` · `AOMDV-b` · DESPARETE v0.4.1. Taban **`k198`** · `941 passed` · SINANMAMIŞ 41. Sönümleme referans dünyada blok üreteciyle (K-198, ~3,8 kat hızlı, istatistik denk).
- **Taban protokoller DONMADI.**

### 4.1 · Arkada koşan iş: BİRİNCİL HÜCRE PARTİSİ (28 Eylül gece başladı, ~10–12 sa)

32 koşu (§13 A/B · rota tamponu · anatomi), ön-kayıt ve karar kuralları `arsiv/teshis/birincil_2026-09-28/beklenti.md`. Çıktı `tam.txt`, her biten koşu `kayit.jsonl`e yazılır. Kesilirse aynı komut (beklenti dosyasındaki kollar, `--kayit …/kayit.json`) ara kayıttan kaldığı yerden sürer — **önce süreç ağacına bak**, iki kopya koşmasın. Dondurulmuş kopya Temp altında (`arac_hash 8f099aa1…`, depoyla aynı). Bu oturumun öteki çıktıları: `arsiv/teshis/olsr_referans_2026-09-28/` · `evre_g1p_2026-09-28/` · `regresyon_k196_2026-09-28/` · `regresyon_k198_2026-09-28/` · `performans_2026-09-28/`.

### 4.2 · Sıradaki işler

> İlk oturumda UYGULANMAZ. Projeyi anladıktan sonra eleştirerek planla (§ilk oturum, adım 4).

1. ✅ Hesap bütçesi (K-198: 350 s ~1 sa/koşu) · ✅ rota tamponu kaynağı (ns-3) · ✅ DESPARETE referans dünyada (G1-P ve duman). Öğrenci 28 Eylül gece **her şeye onay verdi** (pahalı koşular dâhil).
2. **Kalan yazılım:** Faz 4.4 köken borcu (SINANMAMIŞ 42, köken sayımı dünyaya duyarlı değil).
3. **Pahalı koşular** (`v2/12` Faz 4.3):
   - ⚠️ **birincil hücrede `OLSR-b ↔ OLSR-c`** eşli (§13 karıştırma altında sınanmadı; regresyonun tek karıştırıcılı OLSR vakasında §13'süz −0,13) — iyi olan taban olur;
   - rota tamponu 64 ↔ 256 · 30 ↔ 60 s (İ-8c);
   - U1 yeni kod hâlleriyle (yere toplama + eşler arası; OLSR düşük hücreleri K-196 okumasıyla açıklanmış listesine) → **taban protokoller DONAR**;
   - birincil hücrede kayıp anatomisi (açık/sessiz evre hazır) → Faz 5.0.
4. **Açık öğrenci kararları:** KR-2 · KR-D (`v2/12` §4) ve yukarıdaki 1.

## 5 · Çalışma anlaşmaları — kısa (ayrıntı `v2/03` §1)

**Git komutlarını yalnız öğrenci çalıştırır** — salt-okur olanlar dâhil · dosya silinmez, `arsiv/`e taşınır · Türkçe, kısa, kod referanssız özet · `sim2/`de yapısal değişiklikten önce yapıyı anlat, onay al · 30 dk'yı aşan koşumdan önce sor, bant ver; havuz 8 işçi · her sayının üretici komutu · ölçütler ölçmeden önce yazılır · regresyonun beklenen farkı karşılaştırmadan önce · bir iş bitirilir, sonra ölçülür · her Python çağrısında `PYTHONIOENCODING=utf-8` ve `PYTHONDONTWRITEBYTECODE=1` (izlenen `.pyc`'ler var) · `Pool`'da `__main__`, iç içe havuz yok · biçim tercihleri (`python -c`, stdin, heredoc) serbest — öğrenci, 27 Eylül: sonucu etkilemedikçe katı olma · satır sonları (CRLF/LF) korunur · indirme izinle, belge depoya girmeden tamamı okunur · paket kurulmaz · **koşan bir işin kullandığı koda dokunulmaz — uzun koşular dondurulmuş kopyadan** · her `sim2/` adımından sonra tam takım + `mimari_denetimi.py` + regresyon · K kaydından sonra `arsiv/dogrulama/kayit_indeksi.py` yeniden üretilir.

## 6 · Teşhis alışkanlıkları (tam liste `v2/03` §2.1)

Ölçüm aletine ölçtüğü şeyden az güven · bir açıklama hücrenin neden en düşük olduğunu gösterir, kusursuzluğu değil — mümkünse nedensel ölç · bir protokolün kusuru öbürünün aynasında görünür · "harfiyen" yanlış olabilir (K-148 S10) · bir kapının "X yapmaz" sonucunu sınarken X'e bağlı kapıları da sor (K-166) · "ölçtüm, etkisi yok" ile "ölçemedim" ayrıdır · kısa pencere zamanla biriken etkiyi göremez.

**27 Eylül'e kadar referans dünyada öğrenilenler:**
- **Araç sessizce eski dünyayı koşabilir.** `Konfig()` varsayılanı eski dünyadır. Her araç `kalibrasyon/dunya_secimi.konfig` kullanır (AST testi zorlar); dünya `--dunya referans_2026` ya da `DESPARETE_DUNYA` ile seçilir (K-183, K-187).
- **Ölçeklenen dünyada her sabitin birimini sor.** Gölgeleme hücresi ölçekle çarpılmamıştı; Θ 0,29'a çöktü ve alan yanlış seçildi (K-188).
- **Yönlü grafikte bileşen BFS ile bulunmaz.** ED susturması grafiği yönlü yapar; güçlü bileşen kullan (K-186).
- **Süre tahminleri referans dünyada 5 kat yanıldı** (duyma menzili ~28 km, her iletim neredeyse herkese ulaşıyor). Uzun bir koşudan önce kısa bir profil koş (`arsiv/teshis/faz4_2026-09-26/j_profil.py`).
- **Arka plan işleri:** `( … ) &` alt kabuğu bitişte bildirim vermez. Bash aracı kesilince altındaki **betik ve Python yaşamaya devam eder** — 27 Eylül'de bu yüzden AOMDV iki kez başladı (K-191 §3). Bir süreci "öldü" saymadan önce süreç ağacına bak (`Get-CimInstance Win32_Process`: komut satırı, ana PID). Bir betiği durdururken ÖNCE en üstteki betik kabuğunu durdur, sonra çocukları; yoksa döngü bir sonraki koşuya geçer.
- **Hüküm aracı dünyayı kayıt adından okur:** referans kaydını `--dunya referans_2026` ile hükme sok; uyuşmazlıkta araç reddeder (K-191 §4).

> **Bir şeyi iddia etmeden önce ölç. Ölçemiyorsan iddia etme.**
