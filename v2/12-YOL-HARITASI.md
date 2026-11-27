# 12 · DURUM VE YOL HARİTASI

> Projenin durumu ve planı YALNIZ burada tutulur; başka belgeler buraya atıf verir. Güncel: 27 Kasım 2026 (Aşama 2 tamam: B5, B6 ve B7'nin kararları ve kâğıtları; 26 Kasım'da durum tablosu sadeleştirildi, Faz 5-3'ün kaydı §1.3'e taşındı; önceki hâli `arsiv/12-YOL-HARITASI-2026-11-26.md`). Onaylı plan Faz 0–7 (25 Eylül, K-168). Kararlar `04`, tarihçe `kayit/KARAR-GUNLUGU.md`.

## 1 · Nerede duruyoruz

| | |
|---|---|
| **faz** | **5 · DESPARETE** (K-250) — aşama 5-3, geliştirme (5-1 tamam 14 Kasım, 5-2 tamam 17 Kasım). 24 Kasım'dan beri protokol baştan, bileşen bileşen ve eksiksiz yeniden tasarlanıyor; ölçüm tasarım donduktan sonra yapılır (K-253; plan §1.2 madde 3b; yöntem, aşamalar ve eksiksizlik listesi `18`). Aşama 1 · zemin tamam (24 Kasım). Aşama 2 · bileşenler: B1 komşu ve bağın ölçüsü (24 Kasım) · B2 karıştırma kanıtı (25 Kasım) · B3 bağın durumu (26 Kasım) · B4 yol (26 Kasım; eki 27 Kasım) · B5 iletim kararı (27 Kasım) · B6 kontrol iletileri (27 Kasım) · B7 bekletme ve komut (27 Kasım) onaylandı; Aşama 2 tamam (27 Kasım). **Sırada Aşama 3** (bütünlük denetimi, bağımsız denetim, donma), sonra Aşama 4 (kod ve tek büyük ölçüm). Faz 5-3'ün kaydı §1.3. Faz 4b kapandı (K-250), Faz 4 kapandı (K-221) |
| **sıradaki iş** | Aşama 3 · bütünlük ve donma (`18` Aşama 3): (1) yedi bileşenin birlikte denetimi, `18`'in "Bütünlük denetiminde" listesine göre (değerler tek tabloda, iletiler ve kontrol payının kestirimi, durumların birleşimi, uçtan uca senaryolar, izlenebilirlik, ilkelerin karşılanması) ve `bilesen/00-DIZIN.md`'nin "Aşama 3'e açık kalanlar"ı; (2) ayrı bir oturumda bağımsız denetim, yeni istemle (eski istemler `arsiv/denetim/`de); (3) donma ve Aşama 4'ün büyük ölçümünün beklentisi (hücreler, kollar, karar kuralı). Aşama 2 tamam (27 Kasım; §1.3) |
| simülatör | referans dünya (`14`) tamam; birincil hücrede 350 s'lik koşu süreleri §3'te. Yer–hava görüş hattı kalıcı (K-243) |
| taban protokoller | **AODV · OLSRv2 · Babel (K-242).** `OLSRv2-b` donmuş (K-239). `AODV-k` (K-243 · K-244) ve Babel (RFC 8966, hakem babeld; K-244) kodda, sadakat denetimlerinden geçti; regresyon `k244` temiz, U1 iki desende geçti (AODV-k'nin düşüşü ns-3'ün iki varsayılanından, düşük hücreleri anatomi ve döngü iziyle açıklı; Babel'in kâhin aşımları zarf ve hata aramasıyla kayıtlı, K-248); evre kapıları ve G1-P geçti (M4'ün sıfır gözlem kuralı); **`AODV-k` ve `Babel-a` dondu (K-249)**, regresyon tabanı `k249`. Hakem ilkesi: RFC'nin seçeneğe ve MAY'e bıraktığı yerde referans uygulamanın varsayılanı (K-244). JarmRout rakiplikten çıktı; kodu ve kayıtları Faz 4b'nin kaydı |
| DESPARETE | Kodda iki sürüm var, ikisi de önceki tasarımdır: v0.4.1 (`protokoller/desparete.py`; taslak, karşılaştırma için kalır) ve 5-3'ün ilk tasarımı (`protokoller/desparete5*.py`; kararları `17`, kuralları `kural/KK-*`, ölçümleri §1.3). Yeni tasarım (`18`, `bilesen/`) henüz kodlanmadı; Aşama 4'te yeni modüllerle yazılır. Bugünkü yer (8 tohum, 1003–1010; `18` §1.1, §2.4): ikizde 19 Kasım çekirdeği 0,954, geri+sınır 0,958, uygulanabilirlik koşullu kol (eğim0) 0,943 ↔ Babel 0,930; birincilde `PDR_açık` dört sürümde 0,659–0,666 ↔ Babel 0,663 (kâhin 0,779); birincilde en kötü tohum eğim0 0,470 ↔ Babel 0,485. Hedef: birincilde Babel'den en az +0,05 (`18` §1.1). v0.4.1'in son ölçümü (teşhis (c), `arsiv/teshis/faz5_2_rakip_cizgisi_2026-11-15/sonuc.md`): birincil 0,567, dayanıklılık 0,453, ikiz 0,785 |
| doğrulama | `1203 passed` (20 Kasım; sonra simülatör, protokol, araç ve test kodu değişmedi, son kod commit'i `a79f104`) · mimari denetimi ihlalsiz ve bulgusuz (18 Kasım: teşhis (d) aletinin 16 sabitinin kökeni yazıldı, D13) · regresyon tabanı **`k249`** (87 vaka) · R = **0,0126** (K-224, 7 deneme) · köken sayımı `04` §9 · kayıt indeksi güncel (26 Kasım) |
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
3. **5-3 · geliştirme:** tasarım parça parça yazılır; her mekanizmanın sınıfı (karıştırmaya karşı ya da genel) ve amacı ölçmeden önce yazılır (K-247) · kod, birim testi, duman koşusu · mekanizma başına A/B, §2 Faz 5'in kuralıyla; her A/B'de kontrol trafiğinin kanal süresindeki payı raporlanır (`17` T-19). 17–24 Kasım bu yolla çalışıldı (§1.3); yerini 3b aldı.
3b. **5-3 · yeniden tasarım (24 Kasım, K-253):** üç sürümün ölçümünden sonra protokol baştan, bileşen bileşen ve eksiksiz tasarlanır; yöntem, aşamalar ve eksiksizlik listesi `18`de. Aşamalar: 1 · zemin (hedef ve başarı ölçütü, kısıtlar, kanıt envanteri, mimari iskelet) · 2 · bileşen bileşen tasarım (bağın ölçüsü · karıştırma kanıtı · bağın durumu · yol seçimi ve döngü · karıştırma altında iletim · kontrol düzlemi · bekletme ve komut) · 3 · bütünlük denetimi, bağımsız denetim, donma · 4 · kod ve tek büyük ölçüm (ikiz, birincil, dayanıklılık, yer karıştırıcılı aile; tam sürüm ve her mekanizmanın ablasyonu). Tasarım sırasında A/B yok; bir kararın girdisi eksikse kısa, önceden yazılı teşhis ölçümü yapılabilir.
4. **5.7 · kapanış:** sürüm donar · resmi U1 + U3 · evre kapıları · güncel tasarım belgesi (`18` ve `bilesen/`, donmuş hâliyle) → Faz 6.

### 1.3 · Faz 5-3'ün kaydı

**5-1 ve 5-2'nin çıktısı** (ayrıntı §1.2 madde 1–2): altı konunun tasarım kararları (`17`: üç ilke, T-1…T-19; 16 Kasım); teşhis (d) (`arsiv/teshis/faz5_2_isaretler_2026-11-16/sonuc.md`); protokolün kimliği ve komutun yolu (`17` T-20); aşamanın bağımsız denetimi ve kapanışı (`arsiv/denetim/DENETIM-RAPORU-5-2-2026-11-17.md` · `arsiv/denetim/DENETIM-5-2-KAPANIS-2026-11-17.md`; 17 Kasım).

**Önceki tasarımla (17–24 Kasım; kararları `17`, kuralları `kural/KK-*`, kodu `protokoller/desparete5*.py`):**
- **Kural kâğıtları** (17 Kasım): `kural/KK-00`…`KK-05` yazıldı, kendi içinde üç kez denetlendi ve bağımsız denetimden iki okumayla geçti (`arsiv/denetim/DENETIM-RAPORU-KURAL-2026-11-17.md` · `…-ikinci.md` · `DENETIM-KURAL-KAPANIS-2026-11-17.md`; kodlamaya engel yok, açık bulgular kodlamayla kapatılacaktı).
- **Kod** (18 Kasım): bütün kâğıtlar kodlandı (`protokoller/desparete5*.py`), ölçüm aletlerine `desparete5` ve `desparete5_cekirdek` adlarıyla bağlandı; birim testleri ve küçük test dünyasında uçtan uca testler geçti. Açık bulgulardan yalnız Y-1 kalmıştı (kapanış belgesi); konusu (askıda süresi) 19 Kasım'da T-2'nin yeniden yazılmasıyla kalktı.
- **İlk ölçüm** (18 Kasım; karıştırmaya karşı mekanizmalar kapalı çekirdek ↔ Babel, 8 tohum; `arsiv/teshis/faz5_3_cekirdek_2026-11-18/sonuc.md`): çekirdek ikizde Babel'in gerisinde (0,810 ↔ 0,930, 7/8; birincilde `PDR_açık` 0,410 ↔ 0,663); iletimi ve kontrol yükü Babel'inkinden iyi; açığın tamamı rota yokluğunda ve tohumlar arası teslim açlık sayısıyla belirleniyor (r = −0,97, kuraldan sonra).
- **Açlık teşhisi** (19 Kasım; `arsiv/teshis/faz5_3_aclik_2026-11-18/sonuc.md`): rota yokluğu kaybının kökü %99 veri tetiğinin gerçekte iyi olan ardıl bağlarını düşürmesi (kâhine göre %99,7'si iyi); veri tetiği kapalı çekirdek ikizde 0,946 (çekirdek 0,810, Babel 0,930; birincil hücrede ölçülmedi). Tetiği kaldırma kararı verildi, ama küçük test dünyasında tetiğin gerçek bir işlevi görülünce (selamı geçen ama veriyi taşımayan bağı yakalıyor) uygulanmadan beklemeye alındı.
- **Kaynak taraması** (19 Kasım; `protokol_kaynaklari/faz5_3_arastirma_2026-11-19/NOTLAR.md`): 4B, CTP, Babel'in yol seçimi; karıştırma tespiti ve karşılığı.
- **Tasarım kararları** (19 Kasım; `17`): T-2 vazgeçme tetiği (veri sonucu maliyete girmez, yalnız MAC vazgeçmeleri sayılır, bağ yalnız yedek varken bırakılır) · T-11 anlık ve düzgünleştirilmiş maliyet birlikte · T-12 maliyet eğimi, son çare, maliyet tavanı ve başlıksız döngü bekçisi (CTP ve RPL'den uyarlama) · T-13 açlık ve tur kalktı; önceki metin `v2/arsiv/17-TASARIM-KARARLARI-2026-11-18.md`. Kural kâğıtları yeniden yazıldı ve onaylandı (KK-01 vazgeçme tetiği, KK-04 eğim ve döngü bekçisi, KK-00/02/03/05 uyduruldu; eskileri `v2/arsiv/kural/`).
- **Kod** (19 Kasım): `protokoller/desparete5_egim.py`, vazgeçme tetiği `desparete5_bag.py`'de; 18 Kasım'ın davranışı bayrakla birebir yeniden üretiliyor (küçük test dünyasında sekiz koşu: `arsiv/teshis/faz5_3_kod_2026-11-19/esdegerlik.txt`); ölçüm aletinde `desparete5_eski_cekirdek`; mimari denetimi temiz, bütün test takımı 1197 test geçti.
- **Yeni çekirdeğin ölçümü** (20 Kasım; `arsiv/teshis/faz5_3_yeni_cekirdek_2026-11-19/sonuc.md`, 64 koşu): ikizde çekirdek 0,954, Babel 0,930, 8/8 önde; birincilde `PDR_açık` 0,663 ↔ 0,663, ayırt edilemedi; vazgeçme tetiği, iki ölçülü geçiş ve eğimin katkısı iki hücrede de 8 tohumda ayırt edilemedi, zararlı bileşen yok; 18 Kasım'a göre kazancın neredeyse tamamı eski veri tetiğinin kalkmasından; birincilde eğimli kollarda koşu başına binlerce kesin döngü, zor tohumlarda toplanıyor; en kötü tohumda çekirdek 0,314 ↔ eğim0 0,470; kontrol payı %6, Babel'in üçte biri. Kuralın hükmüyle sırada karıştırma katmanı vardı (karıştırma işaretlerinin kalabalıkla yanlış alarmı A/B'leriyle düzeltilecekti).
- **Döngü kuralları** (20 Kasım kararım): karıştırma katmanından önce eğime geri gönderme yasağı ve sınırlı yükselme eklendi (KK-04 kural 13–14, `17` T-12'nin 20 Kasım eki; RPL [63] §11.1, §8.2.2.4). Kod 20 Kasım'da yazıldı; iki bayrak kapalıyken 19 Kasım'ın kodu birebir (küçük test dünyasında 12 koşu: `arsiv/teshis/faz5_3_kod_2026-11-20/esdegerlik.txt`); mimari denetimi temiz, bütün test takımı 1203 test geçti.
- **Döngü kurallarının ölçümü** (24 Kasım; `arsiv/teshis/faz5_3_dongu_kurallari_2026-11-24/sonuc.md`, 32 koşu): hiçbir kol eğim0 düzeyine gelmedi (K1–K6); geri+sınır ikizde 0,958, Babel'den +0,028 (8/8); birincilde 0,659 ↔ eğim0 0,665, en kötü tohum 0,408 ↔ 0,470, sessiz dönem 0,863 ↔ 0,911, döngü dönüşü 3620 → 1014; yalnız geri gönderme yasağı, kural 9'un döngü kanıtını sildiği için tek başına zararlı. Kuralın hükmüyle yol seçiminde uygulanabilirlik koşuluna dönüş yeniden tasarımda konuşulur.

**Yeniden tasarım (24 Kasım'dan; K-253, `18`, kâğıtlar `bilesen/`, değerler `bilesen/00-DIZIN.md`):**
- **24 Kasım kararım:** protokol baştan, bileşen bileşen ve eksiksiz yeniden tasarlanır; ölçüm tasarım donduktan sonra yapılır (§1.2 madde 3b).
- **Aşama 1 · zemin** (24 Kasım, `18` §1.1–1.4): hedef ve başarı ölçütü (birincilde `PDR_açık`'ta Babel'den en az +0,05, ~0,71; fark-içinde-fark ve mekanizma kapısı; yedi koruma ölçütü) · kısıtlar · kanıt envanteri · mimari iskelet (yedi bileşen B1–B7; tek yönlü akış ve gözlemlerin sahibine gitmesi; karıştırmaya karşı mekanizmalar ayrı katman; rota durumu ile paket kararı ayrı).
- **2.1 · B1 komşu ve bağın ölçüsü:** kararım (24 Kasım, `18` §2.1): selamın ölçüsünün yanına verinin kendi ölçüsü, ikisi ham ve aynı birimde, birleştirme B3'te. Kâğıt `bilesen/B1-KOMSU-VE-BAG.md`, onaylandı (24 Kasım).
- **2.2 · B2 karıştırma kanıtı:** kararım (24 Kasım, `18` §2.2): A, alıcı ve gönderici birlikte; alıcının girişim kuralı ve göndericinin bağ kuralı ölçümle seçilir. Teşhis ölçümü (`arsiv/teshis/faz5_3_b2_isaretler_2026-11-24/`: çekirdeğimizin trafiğinde dört hücre, 32 koşu; seçim ve doğrulama yarıları) koşuldu ✓ (25 Kasım, `sonuc.md`): girişim kuralı var, G(α 0,4 · β 0,6 · giriş 2 · çıkış 1), doğrulamada ikizde yanlış alarm %0,002, 3 s içinde %34–35; kanal kilidi kuralı önceden yazılı birimle tutmaz (kuraldan sonra görülen: yer–hava görüş hattı dönem içinde açılıp kapanıyor; alana girişten itibaren kural %90–95'ini 3 s içinde yakalıyor, ortanca 1 s); göndericinin bağ kuralları tanımıyor; yük koruması gerekmiyor. Kanal kilidi kuralı için kararım (25 Kasım): kural (m ≥ 0,55) alındı, dayanağı sonuçtan sonra ölçüldü ve `06` §10'a yazıldı (K1'in birimiyle ulaşılabilecek en yüksek yakalama doğrulamada 0,463, kuralınki 0,463; `ek_hesap.txt` E8). Kâğıt `bilesen/B2-KARISTIRMA-KANITI.md`, onaylandı (25 Kasım).
- **2.3 · B3 bağın durumu:** kararım (25 Kasım, `18` §2.3): çekirdekte kullanılan bağın maliyeti veriden, kullanılmayanınki selamdan, eşikle düşürme yok; karıştırılan bağ son çare. Teşhis ölçümü (`arsiv/teshis/faz5_3_b3_bag_olculeri_2026-11-25/`: çekirdeğimizin trafiğinde ikiz ve birincil, 16 koşu; seçim ve doğrulama yarıları; iki ölçü aynı bağda, kâhin ve bağın sonraki veri bedeliyle yan yana) koşuldu ✓ (26 Kasım, `sonuc.md`): veri ölçüsü kullanılan bağın sonraki bedelini selamdan iyi kestiriyor (0,231 ↔ 0,305 bit) ama önceden yazılı 0,10 bitlik farkla değil, seçenek 2'nin dayanağı tutmadı; veri selamı ancak 12 kayıtla geçiyor; selamın veri cinsine çevrilmesi kazanç getirmiyor; veri yükle oynamıyor; selamı geçen ama veriyi taşımayan bağ seyrek ve kısa; kuraldan sonra görülen: zarar ölçüden değil eşikten. Yeniden kararım (26 Kasım): çekirdekte A, bağın maliyeti selamdan, eşikle düşürme yok, veri yalnız güvenlik ağı; karıştırılan bağ son çare (E1). Kâğıt `bilesen/B3-BAG-DURUMU.md`, onaylandı (26 Kasım).
- **2.4 · B4 yol:** kararım (26 Kasım, `18` §2.4): uygulanabilirlik koşulu, Babel ailesi; geçidin turu ve tur isteği; olağan bağlar son çaredekilerden önce. Kâğıt `bilesen/B4-YOL.md`, onaylandı (26 Kasım). 27 Kasım eki (B5 teşhisinden sonra, yeni kanıtla; `18` §2.4): Babel'in iki SHOULD kuralı, tercih edilir uygulanamaz ilanda istek (kural 10a) ve süre dolmadan istek (kural 4a); kendi aralıklarımda ilanın yaşı durur (kural 4, kural 14'le tutarsızlığın düzeltmesi); onaylandı (27 Kasım).
- **2.5 · B5 iletim kararı:** sorun, kanıt ve dört seçenek ailesi `18` §2.5'te. Kararım (26 Kasım): ana seçenekten önce teşhis (`arsiv/teshis/faz5_3_b5_iletim_kaybi_2026-11-26/`: bugünkü kodun `eğim0` kolunun trafiğinde ikiz ve birincil, 16 koşu; her iletim kaybı karar anındaki duruma göre sınıflanır, ulaşabileceği pay 0,02'nin altında kalan aile elenir); beklentisi yazıldı. Teşhis koşuldu ✓ (27 Kasım, `sonuc.md`): elenen aile yok (B'nin hedefi 0,022, C'ninki 0,036, D'ninki 0,100; katmanın kendi payı 0,0485); B'nin tetiği yok; C1'in yayın eki koşu başına +81 s; D'nin ikizde de üst sınırı 0,0525. Kuraldan sonra görülen: J1'in 0,032'si çekirdeğin kanıtıyla da görülüyor; uygulanabilirlik koşulunun bedeli 0,137; temiz kanalda ardılın ilanı kararların %2,1'inde yanlış alarmla bayat. Kararım (27 Kasım, `18` §2.5): A, tek yol; B, C ve D alınmadı (D genel, kapının kolunda katmanın kayıplarını da kurtarır, simülatöre yetenek ister; Aşama 4'te hedef tutmazsa ilk kaldıraç). Kâğıt `bilesen/B5-ILETIM-KARARI.md`, onaylandı (27 Kasım). Bölge risk skoru fikir olarak duruyor (`18` §2.2'nin C seçeneği).
- **2.6 · B6 kontrol iletileri:** sorun, kanıt ve seçenekler `18` §2.6'da (27 Kasım). Bugünkü selamın bedeli kayıtlardan hesaplandı (`arsiv/teshis/faz5_3_b6_kontrol_bedeli_2026-11-27/`): protokolün kendi iletileri kanal süresinin %2,6'sı, Babel-a'nınki %11; kontrol payının (%6) geri kalanı veri çerçevelerinin MAC onayları. Ana seçenek selamın zamanlaması (Z1 uyarlanır, bugünkü · Z2 sabit kısa · Z3 karıştırmaya duyarlı · Z4 Babel'in 4 s'si); teşhis gerekmiyor. Kararım (27 Kasım): Z1. Kâğıt `bilesen/B6-KONTROL-ILETILERI.md`, onaylandı (27 Kasım); B4 kural 15'in olay listesinden tek başına ardıl değişimi çıktı (RFC 8966 §3.7.2).
- **2.7 · B7 bekletme ve komut:** sorun, kanıt ve seçenekler `18` §2.7'de (27 Kasım). Bugünkü bekletme kayıtlardan hesaplandı (`arsiv/teshis/faz5_3_b7_bekletme_2026-11-27/`): birincilde bekletilen paketlerin %62'si 1 s dolunca düşüyor; bekledikten sonra gidenler teslimin %2'si olduğu için gecikmenin p99'u (1,08 s) bekletmenin süresine bağlı. Ana seçenek bekletmenin süresi (H1 1 s, bugünkü · H2 uzun · H3 bekletmesiz · H4 başlıkta bütçe, elenir); komutun yolu geri iz (K1, tek gerçekçi seçenek); teşhis gerekmiyor. Kararım (27 Kasım): H1 ve K1. Kâğıt `bilesen/B7-BEKLETME-KOMUT.md`, onaylandı (27 Kasım). Aşama 2 tamam: yedi bileşenin kararı `18` §2.1–2.7'de, kuralları `bilesen/B1`…`B7`'de, değerleri `bilesen/00-DIZIN.md`'de.

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

### Faz 5 · DESPARETE — karıştırmayı gerçekten çözen protokol (şimdiki faz; plan §1.2, durum §1, kayıt §1.3). Aşağıdaki tablo K-228'in aday mekanizmalarıdır ve tarihsel kayıttır: 5-2'nin kararları (`17`) onları aştı (5.2 öngörülü kaçınma ve 5.3 postür alınmadı, 5.4'ün yerine T-14, 5.6'nın periyodik DFSN'si yerine T-12); 24 Kasım'dan beri tasarım baştan yapılıyor (`18`, K-253)

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

Her mekanizma: ablasyon bayrağı · önceden yazılı beklenti (iki ölçütle: birincil hücrede `PDR_açık` artışı **ve** karıştırıcısız kolda zarar yok) · geliştirme tohumları 1003–1010 · birincil hücre + **dayanıklılık hücresi** (10 s açık · 20 s sessiz; zaman sabitleri tek çizelgeye ayarlanmasın) + bir yer karıştırıcılı aile (K-222, denetim D-08). Yeni tasarımda bu ölçüm Aşama 4'ün tek büyük ölçümüdür: tam sürüm ve her mekanizmanın ablasyonu, bu hücrelerde (`18` Aşama 4).
**Öncelik:** K-228'in sırası K-252 ile kalktı; sıra `18`'in bileşen sırasıdır. 5.2 birincil testte kazanç gösteremez: formasyonda bağ hareketle kopmuyor, Θ tanımsız (bağımsız ve görev kollarında keşifsel).
**Önkoşullar:** 5.0'ın beklentisi `PDR_açık`a göre yeniden yazıldı ve koşuldu (denetim D-22; K-228) ✓ · gürültü gözlemi kilitli kalır, 5.1'in kanıtı kanal doluluğu, PHY hatası, MAC sonucu ve RSSI'den (K-227; D-04 kapandı) · çoğaltmanın PDR, korunum ve fatura tanımları yazıldı (D-23, K-231, `13` §07) ✓.

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
| Faz 5-3 Aşama 4 (tek büyük ölçüm: ikiz, birincil, dayanıklılık, yer karıştırıcılı aile; tam sürüm ve ablasyon kolları; Babel ve kâhinle karşılaştırma) ve 5.7 (U1, U3): koşu sayısı ve süresi beklentiyle birlikte Aşama 3'te yazılır (önceki kestirim ~350 koşu) | — | ~80 sa (önceki kestirim) |
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
