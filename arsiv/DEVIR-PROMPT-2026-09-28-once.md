# DEVİR PROMPTU — yeni ajana verilecek mesaj

> Bu dosyanın içeriği yeni ajana olduğu gibi yapıştırılır. **Güncel:** 28 Eylül 2026 (gece) · önceki sürümler `arsiv/DEVIR-PROMPT-*.md`. Sayıların kaynağı `v2/`; burada yalnız yön ve yer.

---

Sen bu projeyi hiç görmemiş bir ajansın. Aşağıdakiler bir **tur**dur, kural listesi değil.

## ⚠️ İlk oturumun — DEVAM ETME: önce anla, kontrol et, planla, raporla

Öğrencinin açık isteği: yeni ajan kaldığı yerden doğrudan devam etmez. İlk oturum dört adımdır; dördüncüsünden sonra **öğrencinin onayını beklersin.** Bu adımlarda kod değiştirmez, dosya taşımaz, 30 dakikayı aşan bir şey koşmazsın. Devirde arkada koşan iş yok (§2.1).

1. **Oku ve anla.** Belgeler §3'teki sırayla; sonra kodun çoğu: `sim2/` (önce `cekirdek`, `gozlem`, `kosum`; sonra `kanal`, `mac`, `dunya`, `ag`, `olcum`, `yapilandirma`) · `protokoller/` · `kalibrasyon/`un ana aletleri (`dunya_secimi.py`, `aodv_uygunluk.py`, `regresyon_satirlari.py`, `mimari_denetimi.py`, `kahin.py`, `kayip_anatomisi.py`) · `analiz/` · `tests2/`. Modül başlıkları *neden böyle*yi anlatır. DESPARETE paketinden en az `36`, `35`, `23`, `22`, `21`, `19`. Bu istemdeki iddialara da körü körüne güvenme.
2. **Kontrol et** — kısa, yalnız okuyan komutlar (hepsi `PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1` önekiyle): `python kalibrasyon/mimari_denetimi.py` · `python arsiv/dogrulama/kayit_indeksi.py --kontrol` · `python -m pytest tests2 -q` (~15–25 dk). Çelişki, bayat sayı, ölü kapı ararken `v2/03` §2.1'in alışkanlıklarını kullan. Bulduğunu düzeltme — rapora yaz.
3. **Planla** — sıradaki adımlar (§2.2) öncelik sırasıyla: ne, neden, süre bandı, hangi kapıyla kapanır, öğrenci kararı gerekir mi.
4. **Hazırlık raporu** — öğrenciye Türkçe, kısa, kod referanssız: projeyi kendi cümlelerinle · mevcut durum · kontrollerin sonucu (sayılarla) · bulduğun sorunlar (yoksa "bulamadım") · plan · beklediğin kararlar · emin olmadıkların.

## 0 · Burada nasıl çalışılır

- **Serbestçe düşün, ölçümle bitir.** Önceki ajanların ortak kusuru fazla itaatti; en değerli bulgular kayıtlı bir şeye inanmayı reddetmekten çıktı. Bir iddiayı bitiren şey üretici komutu olan bir sayıdır.
- **Sorunu sen çöz** (öğrenci, 25 Eylül): bir kusur bulunca çöz, ölç (beklentiyi ölçmeden önce yaz), kaydet, kanıtla getir — yalnız raporlayıp seçenek sunarak bekleme. DESPARETE "yapım aşamasında"dır, geliştirilir. Öğrenciye yalnız fikrinin değiştiği yerlerde (kapsam, iddia, ön-kayıt metriği) **önerinle** sor. Ajan katkısını kayıtta "ajan" diye etiketle — fikir sahipliği (2204-A) için şart.
- **Öz yaz, kısa ölç** (öğrenci, 25 Eylül): aynı bilgi tek yerde, ötekiler atıf verir; bir koşu yalnız bir kararı değiştirecekse ve en kısa gerekli hâliyle koşulur.
- **Gerçekçilik esas** (öğrenci, 25–27 Eylül): *"hayal dünyasında İHA yarıştırmıyoruz"*; bir ölçütle gerçekçilik çatışırsa gerçekçi olanı seç, gerekçesini yaz (K-185: *"ölçütü boşver, en mantıklı ve gerçekçi olana önem ver"*).

## 1 · Proje — otuz saniyede

Bir lise öğrencisi (TÜBİTAK 2204-A) karıştırma altındaki taktik İHA mesh ağları için kendi yönlendirme protokolünü (**DESPARETE**) tasarladı. Karşılaştırma için kendi kesikli-olay simülatörü (`sim2/`), ölçüm aletleri (`kalibrasyon/`, `analiz/`) ve üç taban protokol (AODV, OLSR, AOMDV) yazıldı. Teslim **19 Aralık 2026**. 25 Eylül'de yön değişti (K-168): simülatör önce 1:1, kaynaklı bir taktik sürüye (**referans dünya `referans_2026`**) oturdu, sonra DESPARETE karıştırmayı gerçekten çözecek. Onaylı plan Faz 0–7 → `v2/12`.

## 2 · Nerede kaldık

Ayrıntı `DEVIR.md` §1 ve `v2/12` §1. Özet: Faz 0–3 kapandı (K-169…K-181). **Faz 4 sürüyor** (plan `arsiv/teshis/faz4_2026-09-26/plan.md`; öğrenci onayı 4.1–4.3):
- **4.1 bitti:** alan 33 km, görev yarıçapı 16 km, gölgeleme birim hatası düzeldi (K-188). Birincil hücre `formasyon · yere_toplama · derin_sizma · sürekli`, 10 W (öğrenci, K-186).
- **4.2 bitti:** Li sabit hızda tutuyor (0,127); ARF çok atlamayı bozuyor; Bianchi ±%0,6; PER eğrileri (K-187).
- **4.3'ün yere toplama yarısı bitti** (K-190, K-191). Üç protokolde U1-U 🟢, U1-B 🔴.
  - AODV: statik 0,858, hareketli 0,63–0,78.
  - AOMDV: AODV'den biraz iyi, düşük hücreleri aynı.
  - **OLSR ağır kalıyor:** statik 0,642, hareketli 0,45–0,51; 12 hücreden 11'i eşik altında.
  - AODV'nin statik düşük hücreleri açıklandı: en az atlamanın zayıf bağ bedeli (`m_dusuk_hucre_sonuc.md`).
  - **Taban protokoller DONMADI.**
- **Performans:** yavaş kayıp önbelleği %41, tam pencerede de birebir (K-190, K-191). Taban `k186`.

### 2.1 · Arkada koşan iş YOK

Öğrencinin isteği (27 Eylül): devir, arkada iş kalmadan yapılır. Koşuların çıktıları `arsiv/teshis/faz4_2026-09-26/` (`h_u1_*`, `m_*`), JSON kayıtları `ciktilar2/aodv_uygunluk/<p>_referans_2026_yere_toplama_*.json`.
- Özet dosyası `h_u1_ozet.txt`'teki `aomdv … sure=25688 s` satırı durdurulan ÇİFT kopyanındır ve geçersizdir (K-191 §3).
- `h_u1_aodv_esler_arasi.txt` yarım kalmıştır, geçersizdir.
- Önceki ajanın dondurulmuş kopyaları (`kopya_43`, `m_kopya`) Temp altındaydı; kalıcı değildir, gerekmez.

### 2.2 · Sıradaki işler — öğrencinin onayladığı sıra

1. **Öğrenciye kararlar** — önerinle sor, taban protokoller donmadan önce:
   - **(a) U1 eşiği ve U1-B okuması referans dünyada.** K-136'nın eşikleri eski dünyada seçilmişti. Referans dünyada üç protokol de kalıyor, OLSR ağır (`h_u1_beklenti.md` "Kalırsa": eşik öğrenciye yeniden sorulur).
   - **(b) KR-1:** kâhin kuralının okuması; `v2/12` §4 "U1'lerden önce" diyordu, açık kaldı.
   - **(c)** "Protokolün tasarım bedeli" (en az atlamanın zayıf bağı seçmesi) U1-B'de açıklanmış sayılır mı?
2. **OLSR'ın neden bu kadar düşük olduğu:**
   - Hipotez, ölçülmedi: 802.11b "gri bölge" (Lundgren ve ark. 2002). HELLO uzun zayıf bağlarda duyuluyor ama veri taşınamıyor; tepkisel onarım yok.
   - Araç: `kalibrasyon/kayip_anatomisi.py --dunya referans_2026 --sinif yok --kol statik --protokoller olsr,en_guvenilir_kahin --tohumlar <t>`.
   - Tohum tohum koş, çünkü araç tohumları **toplar**. Karıştırıcısızken bütün düşüşler "uzak" bölgededir; bilgi sebep sütunundadır.
   - Statik 3 tohum ~26 dk sürdü. Beklentiyi önce yaz. OLSR'da bir uygulama kusuru da olabilir (eski dünyada U1'i geçmişti) — ikisini ayır.
3. **Bağımsız 1000 düşük hücresi** (AODV ve AOMDV). Aynı araç, `--kol bagimsiz --tohumlar 1000` ve karşılaştırma için `1001`; 45–90 dk, önce sor. Öğrenci 27 Eylül'de bunu sana bıraktı.
4. **Birincil hücrede kayıp anatomisi** (Faz 5.0'ın girdisi): `--kol formasyon --aile derin_sizma` ile taban protokoller, kâhin ve DESPARETE v0.4.1, tohumlar 1003–1005. 30 dk'yı aşar; önce sor.
5. **U1 eşler arası** (AODV, OLSR, AOMDV). Öğrenci onaylı: *"önerdiğin gibi yapalım da kalan işler bittikten sonra"*, 27 Eylül; başlatması sana bırakıldı.
   - **Önbellekli** güncel koddan, **yeni bir dondurulmuş kopyayla** (`python arsiv/teshis/faz4_2026-09-26/dondur.py <klasör>`), `--desen esler_arasi`, protokoller sırayla.
   - Tahmini 10–17 sa. Başlatmadan önce öğrenciye söyle.
   - (a) kararı eşler arasından önce gelirse koşunun anlamı değişebilir; sırayı öğrenciyle konuş.
6. **Faz 4.4:**
   - yeni regresyon tabanı;
   - doğrulama listesinin tamamı (`DEVIR.md` §2). Birçok satır eski dünyanın aracı; hangilerinin referans dünyada anlamlı olduğu önce ayıklanır. 4–6 sa, önce sor;
   - kalan SINANMAMIŞ parametreler (`arsiv/teshis/faz4_2026-09-26/sinanmamis_plan.md`);
   - `yakalama_penceresi_s` türetimi.
7. **Hesap bütçesi:** referans dünyada 350 s'lik bir koşu önbelleksiz ~1–2 sa sürüyor (U1: protokol başına 24 koşu, 8 işçiyle 5,6–5,8 sa). Faz 6–7 bütçesi (`v2/12` §5) yeniden yazılmalı ve öğrenciye bildirilmeli.
8. **Açık öğrenci kararları:** KR-1 · KR-2 · KR-D (`v2/12` §4) ve yukarıdaki (a), (c).

## 3 · Okuma sırası

| # | belge | neden |
|---|---|---|
| 1 | `DEVIR.md` | durum ve doğrulama listesi |
| 2 | `v2/04` — sondan geriye, en az **K-168…K-191** | kararlar (öz; K-090…K-167 tam metni `v2/arsiv/04-NEDEN-BOYLE-K090-K167.md`) |
| 3 | `v2/12` | plan (Faz 0–7), durum, öğrenci kararları |
| 4 | `v2/14` · `v2/15` · `v2/16` | referans dünya · gerçekçilik yapı paketi · kaynakça |
| 5 | `arsiv/teshis/faz4_2026-09-26/plan.md` | Faz 4'ün satır satır planı ve beklenti dosyaları |
| 6 | `v2/07` §15 | öğrenci kararlarının tek listesi |
| 7 | `v2/03` §1 | çalışma anlaşmaları |
| 8 | `v2/06` | ön-kayıt |
| 9 | `v2/05` · `v2/13` | protokolün görebildikleri ve yapabildikleri |
| 10 | `protokol_kaynaklari/` | RFC 3561 · RFC 3626 · AOMDV makalesi · DESPARETE paketi |

## 4 · Çalışma anlaşmaları — kısa (ayrıntı `v2/03` §1)

**Git komutlarını yalnız öğrenci çalıştırır** — salt-okur olanlar dâhil · dosya silinmez, `arsiv/`e taşınır · Türkçe, kısa, kod referanssız özet · `sim2/`de yapısal değişiklikten önce yapıyı anlat, onay al · 30 dk'yı aşan koşumdan önce sor, bant ver; havuz 8 işçi · her sayının üretici komutu · ölçütler ölçmeden önce yazılır · regresyonun beklenen farkı karşılaştırmadan önce · bir iş bitirilir, sonra ölçülür · her Python çağrısında `PYTHONIOENCODING=utf-8` ve `PYTHONDONTWRITEBYTECODE=1` (izlenen `.pyc`'ler var) · `Pool`'da `__main__`, iç içe havuz yok · biçim tercihleri (`python -c`, stdin, heredoc) serbest — öğrenci, 27 Eylül: sonucu etkilemedikçe katı olma · satır sonları (CRLF/LF) korunur · indirme izinle, belge depoya girmeden tamamı okunur · paket kurulmaz · **koşan bir işin kullandığı koda dokunulmaz — uzun koşular dondurulmuş kopyadan** · her `sim2/` adımından sonra tam takım + `mimari_denetimi.py` + regresyon · K kaydından sonra `arsiv/dogrulama/kayit_indeksi.py` yeniden üretilir.

## 5 · Teşhis alışkanlıkları (tam liste `v2/03` §2.1)

Ölçüm aletine ölçtüğü şeyden az güven · bir açıklama hücrenin neden en düşük olduğunu gösterir, kusursuzluğu değil — mümkünse nedensel ölç · bir protokolün kusuru öbürünün aynasında görünür · "harfiyen" yanlış olabilir (K-148 S10) · bir kapının "X yapmaz" sonucunu sınarken X'e bağlı kapıları da sor (K-166) · "ölçtüm, etkisi yok" ile "ölçemedim" ayrıdır · kısa pencere zamanla biriken etkiyi göremez.

**27 Eylül'e kadar referans dünyada öğrenilenler:**
- **Araç sessizce eski dünyayı koşabilir.** `Konfig()` varsayılanı eski dünyadır. Her araç `kalibrasyon/dunya_secimi.konfig` kullanır (AST testi zorlar); dünya `--dunya referans_2026` ya da `DESPARETE_DUNYA` ile seçilir (K-183, K-187).
- **Ölçeklenen dünyada her sabitin birimini sor.** Gölgeleme hücresi ölçekle çarpılmamıştı; Θ 0,29'a çöktü ve alan yanlış seçildi (K-188).
- **Yönlü grafikte bileşen BFS ile bulunmaz.** ED susturması grafiği yönlü yapar; güçlü bileşen kullan (K-186).
- **Süre tahminleri referans dünyada 5 kat yanıldı** (duyma menzili ~28 km, her iletim neredeyse herkese ulaşıyor). Uzun bir koşudan önce kısa bir profil koş (`arsiv/teshis/faz4_2026-09-26/j_profil.py`).
- **Arka plan işleri:** `( … ) &` alt kabuğu bitişte bildirim vermez. Bash aracı kesilince altındaki **betik ve Python yaşamaya devam eder** — 27 Eylül'de bu yüzden AOMDV iki kez başladı (K-191 §3). Bir süreci "öldü" saymadan önce süreç ağacına bak (`Get-CimInstance Win32_Process`: komut satırı, ana PID). Bir betiği durdururken ÖNCE en üstteki betik kabuğunu durdur, sonra çocukları; yoksa döngü bir sonraki koşuya geçer.
- **Hüküm aracı dünyayı kayıt adından okur:** referans kaydını `--dunya referans_2026` ile hükme sok; uyuşmazlıkta araç reddeder (K-191 §4).

> **Bir şeyi iddia etmeden önce ölç. Ölçemiyorsan iddia etme.**
