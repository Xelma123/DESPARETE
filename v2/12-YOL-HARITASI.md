# 12 · DURUM VE YOL HARİTASI

> Projenin durumu ve planı YALNIZ burada tutulur; başka belgeler buraya atıf verir. Güncel: 17 Kasım 2026. Onaylı plan Faz 0–7 (25 Eylül, K-168). Kararlar `04`, tarihçe `kayit/KARAR-GUNLUGU.md`.

## 1 · Nerede duruyoruz

| | |
|---|---|
| **faz** | **5 · DESPARETE** (K-250) — aşama 5-3, geliştirme (5-2 tamam, 17 Kasım). 5-1 tamam (sekiz ders). 5-2'de kaynak taraması yapıldı (`protokol_kaynaklari/faz5_arastirma_2026-10-21/NOTLAR.md`) ve üç teşhis ölçümü koşuldu (`arsiv/teshis/faz5_2_anatomi_2026-11-14/sonuc.md` · `arsiv/teshis/faz5_2_secenek_iletim_2026-11-15/sonuc.md` · `arsiv/teshis/faz5_2_rakip_cizgisi_2026-11-15/sonuc.md`); altı konunun tasarım kararları verildi (`17`: üç ilke, T-1…T-19; 16 Kasım); teşhis (d) koşuldu (`arsiv/teshis/faz5_2_isaretler_2026-11-16/sonuc.md`); protokolün kimliği son hâlini aldı ve komutun yolu kararlaştırıldı (`17` T-20); aşamanın bağımsız denetimi yapıldı, bulguları kapatıldı (`arsiv/denetim/DENETIM-RAPORU-5-2-2026-11-17.md` · `arsiv/denetim/DENETIM-5-2-KAPANIS-2026-11-17.md`; 17 Kasım); 5-3 başladı: kural kâğıtları yazıldı ve iki kez denetlendi (`kural/KK-00`…`KK-05`, 17 Kasım; açılış listesi `17` §7); sırada kod; plan §1.2 (K-252). Faz 4b kapandı (K-250): üç rakip donmuş, bağımsız denetimin (14 Ekim, K-242) Faz 5 öncesi işleri tamam. Faz 4 kapandı (K-221) |
| simülatör | referans dünya (`14`) tamam; birincil hücrede 350 s'lik koşu süreleri §3'te. Yer–hava görüş hattı kalıcı (K-243) |
| taban protokoller | **AODV · OLSRv2 · Babel (K-242).** `OLSRv2-b` donmuş (K-239). `AODV-k` (K-243 · K-244) ve Babel (RFC 8966, hakem babeld; K-244) kodda, sadakat denetimlerinden geçti; regresyon `k244` temiz, U1 iki desende geçti (AODV-k'nin düşüşü ns-3'ün iki varsayılanından, düşük hücreleri anatomi ve döngü iziyle açıklı; Babel'in kâhin aşımları zarf ve hata aramasıyla kayıtlı, K-248); evre kapıları ve G1-P geçti (M4'ün sıfır gözlem kuralı); **`AODV-k` ve `Babel-a` dondu (K-249)**, regresyon tabanı `k249`. Hakem ilkesi: RFC'nin seçeneğe ve MAY'e bıraktığı yerde referans uygulamanın varsayılanı (K-244). JarmRout rakiplikten çıktı; kodu ve kayıtları Faz 4b'nin kaydı |
| DESPARETE | v0.4.1, taslak; Faz 5'te özgün tasarımımla yeniden yazılır (K-250). Son ölçüm (teşhis (c), 1003–1010, 8 tohum ortalaması; `arsiv/teshis/faz5_2_rakip_cizgisi_2026-11-15/sonuc.md`): birincil `PDR_açık` 0,567 — Babel 0,663 · OLSRv2 0,495 · AODV-k 0,396 · kâhin 0,779; dayanıklılık hücresinde 0,453 — Babel 0,554; karıştırıcısız ikizde pencere PDR'si 0,785 — Babel 0,930. Faz 5.0 (K-228): karıştırmaya özgü fazla kayıp `rota_gecersiz`'de |
| doğrulama | `1101 passed` (17 Kasım) · mimari denetimi ihlalsiz ve bulgusuz · regresyon tabanı **`k249`** (87 vaka) · R = **0,0126** (K-224, 7 deneme) · köken sayımı `04` §9 |
| arkada koşan | yok |
| takvim | mühür tarihi (~20 Kasım) güncel değil, 5-3'ten sonra yeniden yazılır · proje hedefi 19 Aralık 2026 · resmî son başvuru 4 Ocak 2027, 17:30 (TÜBİTAK 2204-A sayfası; aradaki süre tampon, K-242) |

### 1.1 · Faz 4b — kapandı (K-250)

> **Kural (29 Eylül):** bir faza geride iş kalmadan, yazılım ve yapı denetiminden geçmiş bir simülatörle ve güncel belgelerle geçilir; fazlar paralel yürümez. Faz 4 bu kapıdan geçti (K-221); Faz 5'e geçiş bağımsız denetimden ve düzeltmelerinden sonra (K-226). Faz 4b de aynı kapıdan geçer (K-229).

1. ✓ **Kopya defteri (denetim D-23, K-231):** JarmRout her veri paketini iki yoldan gönderir (K-230). Hedefte ilk teslim sayılır, eşler `kopya_bastirilan`; korunum eşleri kapatır; eşlerin yayın süresi veri yüküne. Kopya kullanmayan protokolde satır aynı: regresyon k223 → k231 birebir.
2. **JarmRout** (Pu 2018) ve **OLSRv2** (RFC 7181 · 6130 · 5444 · 5497 · 5148 · 7779; olsrd2 hakem): kaynaklar depoda ✓ (K-231) · simülatörde kaynak rotası ✓ (K-232, regresyon k232 birebir) · JarmRout kodu ve beyan tablosu ✓ (K-233; makalenin dört çözümlü örneği birim testi) · JarmRout'un kural kural sadakat denetimi ✓ (K-234, `JarmRout-b`) · OLSRv2 kodu (RFC 5444 tel biçimi bayt bayt), beyan tablosu ve sadakat denetimi ✓ (K-235 · K-236, `OLSRv2-b`).
   JarmRout'un seçimlerinin duyarlılık borcu (`t_wait`, Eş. 6–7 süzgeçleri) rakiplikten çıkınca düştü; `rssi_olcum_sigma_db` · `gps_dikey_sigma_m` DESPARETE'nin Faz 5'te bu alanları okuyup okumayacağına bağlı (K-242).
3. ✓ Regresyona yeni protokollerin vakaları (K-237, taban k236) · U1 iki desende (K-238: OLSRv2 temiz; JarmRout'un toplu akış çöküşü incelendi — makaleye birebir sadık, ölçek sınırı bulgu) · ikinci kuyruk (K-239): kopya kuralı sağlandı, dört temsilci anatomi geçti, çizelgeli evre kapıları yalnız JarmRout yüzünden kaldı → sebep ölçüldü (rota beklemesi; eğilim ve pencere sonu boşalması) → kayıtlı muafiyetle G1ç ✓ · G2ç + G4ç ✓ (R ve G3ç protokolden bağımsız, geçerli) → **donma ✓** (`JarmRout-b` · `OLSRv2-b`) · tam takım · mimari denetimi.
4. ✓ **Belge ve kod temizliği** (kararım, 11 Ekim): belgeler (K-240) · kod (K-241: yorumlar, araç varsayılanları, DESPARETE dosyalarındaki tasarım paketi yolu; davranış aynı, değişen simülatör ve protokol dosyalarının sözdizim ağacı birebir). Bilerek kalanlar: donmuş protokol dosyalarının yorumları (donma özeti değişmesin diye), OLSR ve AOMDV'nin modülleri ve regresyon vakaları (Faz 4'ün kaydı), köken gerekçelerindeki eski ölçümler.
   Derin denetime iki not: (a) G1-P (statik boş kol) yeni rakip kümesiyle koşulmadı (K-249'da koşuldu ve geçti); G1ç koşuldu · (b) bütün kontrol mesajları UDP/IP ile faturalanıyor; gerçek DSR (JarmRout) UDP kullanmaz, mesaj başına 8 B fazla (`sim2/kanal/cerceve.py`).
5. ✓ **Bağımsız tam denetim** (13–14 Ekim; `arsiv/denetim/DENETIM-RAPORU-2026-10-14.md`): KRİTİK yok, 16 ÖNEMLİ. Kararlar K-242.
6. **Denetimin Faz 5'ten önceki işleri** (K-242; bulgu numaraları rapordan):
   a. ✓ kapı sertleştirmeleri: sızdırmazlık taraması (DD-05) · `KontrolIstegi` bedel denetimi (DD-06) · U1-B'nin kayıtlı orana bağlanması (DD-07) · fark-içinde-farkın eşleşme denetimi ve tamsayı hesabı (DD-08) · mimari denetiminde köken eksiğinin bulgu ve çıkış kodu olması (DD-19) (K-243);
   b. ✓ kayıp anatomisinin açlık tanımı protokolünkiyle aynı (DD-11) (K-243);
   c. ✓ gecikme tavanlı `PDR_açık`: hesap (K-243) · eşikler 5 s ana, 3,5 s ve 10 s duyarlılık (K-246, DD-03);
   d. ✓ yer–hava görüş hattının kalıcı olması (DD-01) · `AODV-k` (DD-04) → regresyon k243 (K-243; 66/67 birebir, ilan edilmemiş tek vaka DD-01'in yolu, eski modelle birebir doğrulandı);
   e. ✓ Babel: kod · 55 kurallık sadakat denetimi · regresyon vakaları kodda · AODV taraması 42 kurala tamamlandı, `AODV-k`ya ns-3'ün iki varsayılanı (K-244);
   f. ✓ tek kuyruk (beklenti önce; `arsiv/teshis/rakipler_k244_2026-10-14/sonuc.md`): regresyon k244 · U1 iki desende (K-248) · G1ç · G2ç + G4ç · G1-P (K-249) → `AODV-k` ve `Babel-a` dondu · tam takım (K-249);
   g. ✓ belge düzeltmeleri (DD-02 · 12 · 13 · 17 · 18) ve JarmRout'un çıkışının temizliği (K-245);
7. ✓ Faz 5'e geçiş (K-250; §1.2).

### 1.2 · Faz 5 — açıldı (K-250)

**Çalışma biçimi (19 Ekim; K-250 · K-251):** DESPARETE özgün bir protokol olacak; mevcut bir protokolü alıp üstüne ekleme yaparak yeni protokol diye sunulmaz, özellik alınabilir. Amacım, protokole çalışma mantığından formüllerine kadar hâkim olmak ve onu kendim üretmek; yapay zekâ danışman ve öğretmen olarak kullanılır. Faz 5 temiz bağlamla yeni bir oturumda sürer (`DEVIR-PROMPT.md`).

**Aşamalar (K-251):**

| # | aşama | çıktı |
|---|---|---|
| 5-1 | **hâkimiyet** — mevcut DESPARETE'yi (v0.4.1) A'dan Z'ye öğrenirim: çalışma mantığı, formüller, durum makineleri, mesajlar, ölçülen davranışı | protokolü anlatabilmem |
| 5-2 | **araştırma ve öğrenim** — daha iyi bir protokol nasıl yapılır, hangi yöntemler kullanılmalı (literatür, rakiplerin mekanizmaları, karıştırmaya dayanıklı yönlendirme) | tasarım seçenekleri ve kararlarım |
| 5-3 | **geliştirme** — Faz 5'in asıl işi: tasarımım, ablasyon bayrakları, önceden yazılı beklentiler, A/B'ler | DESPARETE'nin yeni sürümü |

**Hedef (K-252):** en güçlü rakip Babel. K-244 kuyruğunda (1003 · 1004; iki tohum, karar değil) karıştırıcısız ikizde `PDR_açık` DESPARETE 0,757 · 0,786 ↔ Babel 0,945 · 0,952; birincil hücrede 0,518 · 0,603 ↔ 0,547 · 0,787; birincil hücrede gecikmenin p99'u 4,7 · 4,3 s ↔ 0,8 · 0,3 s. v0.4.1'in açığının büyük kısmı karıştırmaya özgü değil, genel; v0.4.1'de karıştırmaya özgü mekanizma yok. Faz 5.0 (K-228, `arsiv/teshis/faz5_0_2026-10-10/sonuc.md`; K-243'ten önceki dünya, Faz 4'ün rakipleri): fazla kayıp "rota yok"ta, çoğu karıştırıcıdan uzak rölelerde.

**Plan (K-252, sırayla):**
1. **5-1 · hâkimiyet** — v0.4.1, teorik, sekiz ders: problem ve ölçüt · yol bulmanın temeli · döngüsüzlük · komşuluk · bağ kalitesi · bağ kopunca olanlar · komut geri izi, postür, ablasyon bayrakları ve sürümler · ölçülen davranış. Her ders kendi sözlerimle özetlenir; aşama bir karıştırma senaryosunun baştan sona anlatımıyla biter. ✓ (14 Kasım)
2. **5-2 · araştırma ve öğrenim:**
   - güncel kaynaklar (künyeler `02` §F · `16` [53]–[67]) ve rakiplerin mekanizmaları, önce Babel. Kaynak taraması ✓ (21 Ekim): 15 dosya, yedi konunun seçenekleri ve Babel ↔ v0.4.1 karşılaştırması `protokol_kaynaklari/faz5_arastirma_2026-10-21/NOTLAR.md`;
   - konular: komşunun varlığı · bağ kalitesi · karıştırmanın yerel kanıtı · yedek yol ve çoğaltma · döngüsüzlük · bağı bırakma ya da bekleme zamanı · bekletme, gecikme ve kontrol yükü;
   - teşhis ölçümleri, her biri önceden yazılı beklentiyle, geliştirme tohumlarında: DESPARETE ↔ Babel kayıp anatomisi (ikiz ve birincil hücre) ✓ (14 Kasım, `arsiv/teshis/faz5_2_anatomi_2026-11-14/sonuc.md`: karıştırıcısız açık 0,15, %65'i iletim başarısızlığı, %35'i rota yokluğu; karıştırıcı açılınca Babel 0,07 daha çok kaybediyor, açık evrede açık 0,09 ve tamamı rota yokluğu) · v0.4.1'in `hedefli_canlilik` ve `onarim_edinimi` seçenekleri ikizde (K-165'teki ret eski dünyada, karıştırıcısız, 3 tohum × 40 s'lik ölçüme dayanıyordu; denetim DD-28) ✓ (15 Kasım, `arsiv/teshis/faz5_2_secenek_iletim_2026-11-15/sonuc.md`: iki seçenek de teslimi değiştirmiyor; `onarim_edinimi` rota kaybını 0,054'ten 0,032'ye indiriyor, kazanç iletim kaybına gidiyor; `hedefli_canlilik` rota kaybını azaltmıyor. Aynı ölçümde iletim başarısızlığının sebebi: üç protokolde de veri denemelerinin yarısından fazlası başarısız ve denemelerin %94–96'sı en düşük hızda; alıcının meşgul olma payı DESPARETE'de ve Babel'de aynı, fark alıcıya ulaşan çerçevenin bozulmasında ve yaklaşık yarısı seçilen bağın kalitesinden; DESPARETE'nin kontrol kanal süresi Babel'in 2,7 katı) · rakiplerin ve kâhinin 1003–1010'da üç geliştirme hücresindeki çizgisi ✓ (16 Kasım, `arsiv/teshis/faz5_2_rakip_cizgisi_2026-11-15/sonuc.md`; v0.4.1 de koşuldu: üç hücrede de en güçlü rakip Babel, v0.4.1 her hücrede 8/8 tohumda geride; karıştırmada v0.4.1'in fazla kaybı rota yokluğu, Babel'inki iletim kaybı) · teşhis (d): karıştırmanın yerel işaretleri ✓ (17 Kasım, `arsiv/teshis/faz5_2_isaretler_2026-11-16/sonuc.md`; Babel-a, üç hücre, 8 tohum: ED bölgesinde altı işaretin altısı güçlü, açıklanamayan kanal meşguliyeti ikizde yanlış alarmsız; girişim bölgesinde çözülen çerçeve düşüşü ve selam kaybı güçlü ama tek başına yanlış alarmı yüksek; sinyal tutarlılığı zayıf; art arda üç MAC vazgeçmesi yanlış alarmı seyrek tutuyor ama tek başına geç ve seyrek; en çok kullanılan bağların 7 denemelik atlama başarısı 32 s'de bant değiştirmiyor (doymuş ölçü; tek deneme başarısı ölçülmedi));
   - çıktı: tasarım seçeneklerim ve kararlarım, ödünç alınan her özelliğin kaynağıyla → `17`.
3. **5-3 · geliştirme:** tasarım parça parça yazılır; her mekanizmanın sınıfı (karıştırmaya karşı ya da genel) ve amacı ölçmeden önce yazılır (K-247) · kod, birim testi, duman koşusu · mekanizma başına A/B, §2 Faz 5'in kuralıyla; her A/B'de kontrol trafiğinin kanal süresindeki payı raporlanır (`17` T-19).
4. **5.7 · kapanış:** sürüm donar · resmi U1 + U3 · evre kapıları · güncel tasarım belgesi → Faz 6.

## 2 · Fazlar

**Faz 0 · Referans dünya ✓** (25 Eylül): `14` onaylandı (K-169), yapı paketi onaylandı (K-170; artık `arsiv/`).
**Faz 1 · Fizik ve MAC gerçekçiliği ✓** (26 Eylül): işlem kazancı · ED-CCA · ARF · yayılım gecikmesi · gerçekçi karıştırıcı · 1:1 girdiler (K-171…K-181).
**Faz 2 · Gözlem sözleşmesi v2 ✓** (26 Eylül): RSSI · kulak misafiri · kanal doluluğu · PHY hatası · kendi GPS/INS (K-172, K-179, K-180).
**Faz 3 · Senaryo eksenleri ✓** (26 Eylül): düğüm kaybı · trafik yoğunluğu · enerji (K-180, K-182).

### Faz 4 · Yeniden kalibrasyon ve doğrulama ✓ (8 Ekim, K-221)

| # | iş | durum |
|---|---|---|
| 4.1 | çalışma noktası: alan 33 km, N 40, karıştırıcı rejimi ve birincil hücre, görev yarıçapı 16 km | ✓ K-185…K-188 |
| 4.2 | doğrulama: Li (sabit hızda tuttu), Bianchi, PER eğrileri, kâhin tavanı | ✓ K-187 |
| 4.3 | taban protokoller: kara liste ✓ · AOMDV U1–U4 ✓ · evre metriklerinin boş kol kapısı ✓ · OLSR teşhisi ✓ · birincil hücrede §13 (kapalı kalır) ve rota tamponu (bağlamıyor) ✓ K-200 → **U1 yeni kod hâlleriyle** (yere toplama + eşler arası) → **taban protokoller DONAR** | ✓ K-218 (denetimden sonra `OLSR-d` ve 7 denemeyle yeniden, K-224) |
| 4.4 | köken defteri referans dünyaya göre (K-203) · kapsam ilanı (K-204, K-215) · R (bugün 0,0126, K-224) · 22 parametre ölçümle ya da kararla kapandı · Rician K eksen · TTL 64 · kâhin 48 örnek · AODV-j | ✓ K-213…K-220 |
| 4.5 | doğrulama listesinin referans dünyada anlamlı kısmı bir kez · iş başına süre (bütçe) | ✓ K-219 (son kodla yeniden K-226) |

### Faz 5 · DESPARETE — karıştırmayı gerçekten çözen protokol (şimdiki faz; plan §1.2, K-252). Aşağıdaki tablo K-228'in aday mekanizmalarıdır ve 5-2'nin kararlarıyla aşıldı; güncel tasarım `17` (17 Kasım): 5.2 öngörülü kaçınma ve 5.3 postür alınmadı, 5.4'ün yerine T-14 (hazır yedek, çoğaltma yalnız son çare), 5.6'nın periyodik DFSN'si yerine T-13 (tur yalnız istekle artar)

| # | mekanizma | ne çözer |
|---|---|---|
| 5.0 ✓ | **kayıp anatomisi** — birincil hücrede taban protokoller, kâhin, v0.4.1: paket nerede, neden ölüyor (K-228) | hedefleri ölçümle koyar |
| 5.1 | **karıştırma kanıtı** (taslaktaki C_jam) — komşu başına RSSI × teslim tutarlılığı, kanal doluluğu, PHY hatası; komşununki ilanda, bedeli ödenerek. "Karıştırıcı tespiti" iddiası yok | karıştırılan bağdan kopmadan önce kaçmak |
| 5.2 | **öngörülü kaçınma** — konum/hızdan bağ ömrü tahmini | hareketle kopan bağı önceden bırakmak |
| 5.3 | **kanıta dayalı postür** — CAUTION/PROTECT kanıtla, histerezisle; yanlış kriz oranı ölçülür | savunma modunun doğru anda açılması |
| 5.4 | **PROTECT = seçici çok yol + çoğaltma** — farklı ilk atlamalara sınırlı bütçeyle kopya, hedefte tekilleştirme (simülatöre kopya kalemi) | ani bağ kaybında paketi kurtarmak |
| 5.5 | **pasif bakım** — kulak misafiri + DATA'da potansiyel/DFSN | kontrol yükü ve bayat bilgi |
| 5.6 | **canlılık ve yük** — periyodik DFSN, onarım kotası, sabitler köken defterine | canlılık |
| 5.7 | **kapanış** — profil v0.5 donar · resmi U1 + U3 · güncel tasarım belgesi yazılır (v0.1 paketi arşivde) | protokolün çıkışı |

Her mekanizma: ablasyon bayrağı · önceden yazılı beklenti (iki ölçütle: birincil hücrede `PDR_açık` artışı **ve** karıştırıcısız kolda zarar yok) · geliştirme tohumları 1003–1010 · birincil hücre + **dayanıklılık hücresi** (10 s açık · 20 s sessiz; zaman sabitleri tek çizelgeye ayarlanmasın) + bir yer karıştırıcılı aile (K-222, denetim D-08).
**Öncelik:** K-228'in sırası K-252 ile kalktı; sıra 5-2'deki kararlarımla belirlenir. 5.2 birincil testte kazanç gösteremez: formasyonda bağ hareketle kopmuyor, Θ tanımsız (bağımsız ve görev kollarında keşifsel).
**Önkoşullar:** 5.0'ın beklentisi `PDR_açık`a göre yeniden yazıldı ve koşuldu (denetim D-22; K-228) ✓ · gürültü gözlemi kilitli kalır, 5.1'in kanıtı kanal doluluğu, PHY hatası, MAC sonucu ve RSSI'den (K-227; D-04 kapandı) · 5.4'ten önce çoğaltmanın PDR, korunum ve fatura tanımları yazılır (D-23).

### Faz 6 · Ön-kayıt ve mühür (tarih 5-3'ten sonra yazılır)

δ için gürültü ölçümü (AODV · OLSRv2 · Babel × 20 tohum 1100–1119, birincil hücre) · yer–hava ortamının duyarlılığı (banliyö ↔ açık arazi, K-242) · güç benzetimi ve tohum sayısı · ön-kayıdın kesinleşmesi (`06`): birincil metrik KR-2 (karar), hipotezler, Aile 3 kolları, çekirdek matris, durdurma kuralı, fark-içinde-fark eşiği · pencere üçlüsü (ısınma · ölçüm bitişi · koşu bitişi; SINANMAMIŞ 3) · ana deneyin penceresinde R ve DUYARSIZ hükümlerinin yeniden okunması (δ koşularından, denetim D-03) · uzun bağlarda slot zamanlamasının duyarlılığı (D-11) · kâhinin 96 sönümleme örneğiyle yakınsaması (D-15) · `06` H1.3'ün aldatıcı ↔ sürekli kontrastı referansta yeniden düşünülür (10 W aldatıcı ED'yle bütün ağı susturuyor, K-219) · Rician K ekseninin keşifsel tekrarı (6 · 15 dB, K-215) · **mühür**.

### Faz 7 · Ana deney ve yazım (mühürden sonra – 19 Aralık)

Ana deney 40 tohum (birincil hücre + Aile 1 hücreleri + Aile 3 kolları; keşifsel eksenler az tohumla) · yazım Kasım başında başlar, sonuç bölümleri ana deneyden sonra · simülasyonun görselleştirilmesi · jüri soru bankası · TÜBİTAK biçim gereklilikleri.

## 3 · Hesap bütçesi

Koşu başına süre, 350 s'lik koşu (Faz 4b kapanış kuyrukları, 12–13 Ekim; 12 mantıksal çekirdekte ~13 eşzamanlı süreçle ölçüldü, 8 işçide biraz kısalır):

| protokol | birincil hücre (`formasyon-surekli`, derin sızma) | karıştırıcısız ikiz (`formasyon-yok`) |
|---|---|---|
| kâhin | 0,8–0,9 sa | 0,6 sa |
| OLSRv2 | 1,1 sa | 1,1–1,3 sa |
| DESPARETE v0.4.1 | 1,5–1,6 sa | 1,9–2,0 sa |
| AODV | 2,0 sa | 2,3–2,4 sa |
| Babel | 1,35–1,43 sa | 1,06–1,07 sa |
| JarmRout (rakip değil) | 5,6–6,3 sa | 8,3–8,6 sa |

Kaynak: `arsiv/teshis/faz4b_kapanis2_2026-10-12/G1c.txt` · `G2c.txt` (`sure` sütunu). Tek makine. Babel'in süreleri K-244 kuyruğunun G1ç · G2ç'sinden (17 Ekim, 8 işçi); aynı kuyrukta AODV-k 2,11–2,20 · 1,78–1,80 sa, OLSRv2 1,06–1,09 · 0,82–0,92 sa, DESPARETE 1,37–1,45 · 1,33–1,38 sa (`arsiv/teshis/rakipler_k244_2026-10-14/sonuc.md` §7). Faz 5-2'nin teşhis (c)'sinde (15–16 Kasım, 8 işçi; ikiz · birincil · dayanıklılık hücresi): AODV-k 2,96–3,72 · 2,67–3,37 · 2,37–3,06 sa · v0.4.1 1,44–1,87 · 1,63–2,26 · 1,56–2,02 · Babel 1,05–1,53 · 1,39–2,02 · 1,25–1,64 · OLSRv2 0,85–1,25 · 1,17–1,45 · 1,04–1,27 · kâhin 0,59–0,74 · 0,76–1,07 · 0,56–0,82 sa (`arsiv/teshis/faz5_2_rakip_cizgisi_2026-11-15/sonuc.md` §5). Teşhis (d)'de (16–17 Kasım, 8 işçi, yalnız Babel, kaydediciyle; ikiz · birincil · dayanıklılık): 1,30–1,78 · 1,59–2,14 · 1,52–1,84 sa (`arsiv/teshis/faz5_2_isaretler_2026-11-16/sonuc.md` §0).

**Kaba plan** (denetim D-09; birim süreler yukarıdan):

| iş | koşu | süre |
|---|---|---|
| Faz 5 (K-228'in adlarıyla; 5-3'ün A/B listesi `17`'den kurulunca yeniden yazılır): 5.0 (~20) · 5.1 · 5.3 · 5.4 × (açık/kapalı × 8 tohum × 3 hücre) × ~2 deneme · 5.7 (U1, U3) | ~350 | ~80 sa |
| Faz 6: δ gürültüsü (3 taban × 20) · pencere üçlüsü · tam pencere R ve DUYARSIZ'ların yeniden okunması · Rician 6 · 15 dB · kâhin 96 örnek | ~200 | ~45 sa |
| Faz 7: birincil 5 kol × 40 · karıştırıcısız ikiz 5 × 40 · dayanıklılık hücresi 5 × 40 · Aile 3 (≤ 3 kol × 40) · Aile 1 (≤ 2 hücre × 3 protokol × 40) | ~960 | ~190 sa (~8 gün); hesap üçüncü rakibe koşu başına ≲ 2 sa varsaymıştı, Babel'in ölçülen süresi 1,35–1,43 sa (K-244), yani tutucu |

Faz 7'nin hesabı mühürden hemen sonra başlar; yazım hesapla paralel yürür. Faz 7 satırı kaba hesaptır: süreler yukarıdaki tablodan, 8 işçi.

## 4 · Riskler

- **Yeni dünya yönlendirmeye iş bırakmazsa** (ağ tek atlamaya iner ya da hep bölünür): geometri kaynaklı zarf içinde ayarlanır; karar kayda geçer.
- **Mekanizmalar kazanç göstermezse:** negatif sonuç raporlanır; neden çalışmadığı ölçülür.
- **Babel ve AODV'nin yeni sürümü (K-242):** ikisi de Faz 5'ten önce sadakat, U1, regresyon ve donma yolundan geçer; geliştirme süresi Faz 5'in süresinden düşer. Darboğaz hesap değil geliştirme süresidir (denetim §10).
- **Yapay zekâ kullanımı:** TÜBİTAK'ın Üretken Yapay Zekâ Rehberi önemli ölçüde kullanımın beyanını istiyor; beyanın metni benimdir.
- **Takvim ve hesap:** Aralık başında ~1 hafta tampon. Düşme sırası (önceden yazıldı, K-222): keşifsel eksenler (20 tohumla yetinilir: Rician 6 · 15 dB, eşler arası, hava eşlik) → görselleştirmenin zenginliği → Aile 1 hücreleri (en çok 2) → Aile 3 kol sayısı (en çok 3) → dayanıklılık hücresi 20 tohuma. Güç benzetimi n > 40 isterse önce Aile 1 düşer, sonra dayanıklılık hücresi. Korunanlar: birincil hücre ve karıştırıcısız ikizi, üç taban protokol, DESPARETE, 40 tohum.
- **Tek makine:** her ölçümden sonra commit + push (denetim D-05); elektrik kesintisinde uzun kuyruk biten adımları atlayarak sürer.

## 5 · Gelecek çalışma olarak beyan edilecekler

Komutların yönlendirilmesi · iki geçit · ~2 000 s'lik uzun koşu · protokol farkında karıştırıcı · GPS karıştırması ve aldatması · RTS/CTS · OFDM telsizler · derin öğrenme · GPSR · gerçek RF/SDR/uçuş testi.
