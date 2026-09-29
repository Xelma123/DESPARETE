# 12 · YOL HARİTASI — durum, bütün açık işler, kararlar, bütçe, takvim

> **Güncel:** 25 Eylül 2026 — öğrencinin isteğiyle ayrıntılı yeniden yazıldı (*"hiçbir şeyi atlama, yapmamız gereken her şeyi detaylıca yaz"*). Önceki sürümler: öz `v2/arsiv/12-YOL-HARITASI-2026-09-25-oz.md` · tam `…-2026-09-25.md`.
> Kaynaklar: `06` §9 · `07` §14 · §17 · `02` §S · `13` §06 · bağımsız denetim (`arsiv/denetim/DENETIM-RAPORU-2026-09-25.md`, K-166) · K-150 … K-167.
> **İşaretler:** 🟢 bitti · 🟡 sürüyor · ⏳ sırada · ⚪ zamanı gelince · 🟦 öğrenci kararı gerekir (§9) · **[yapı]** `sim2/` değişikliği: önce yapı anlatılır, onay alınır, regresyon koşulur · **[süre]** 30 dk'yı aşan koşum: önce sorulur · **[git]** öğrenci koşar. Süreler **tahmin** ve bant; ölçülmüş sayının yanında üretici komut. İş (İ-n) ve karar (KR-n) numaraları bu belgeye özgüdür. Kodda geçen eski atıflar: "`12` §3 C1…C7" = Aşama 1 kalibrasyonları (C1 · C2 · C3 · C7 kapandı, K-125…K-128; C4–C6 = İ-13…İ-15) · "`12` §5" = eski tam yol haritası (protokolsüz kapanamayan borçlar → İ-8 · İ-16; DESPARETE'nin parça parça yazımı → 3.1–3.7, bitti).

---

## 1 · Nerede duruyoruz

**📍 Aşama 3, adım 3.8 — DESPARETE'nin kabul kapısı.** Sıradaki: v0.4'ün tam ölçek doğrulaması, sonra resmi U1.

| | |
|---|---|
| aşamalar | 1 (simülasyon) 🟢 16 Eylül · 2 (taban protokoller) 🟢 22 Eylül · 3 (DESPARETE) 🟡 23 Eylül'den beri · 4 ⏳ · 5 ⏳ · teslim **19 Aralık 2026** |
| taban protokoller | `AODV-e` (K-145) · `OLSR-b` (§13 ile, K-147) · `AOMDV-a` (K-149) — U1-U geçti, U1-B'de 2 · 0 · 1 açıklanmış düşük hücre; **yalnız eşler arası desende** sınandı. Hüküm: `python -u kalibrasyon/aodv_uygunluk.py hukum ciktilar2/aodv_uygunluk/<aodv\|olsr\|aomdv>_son.json` |
| DESPARETE | gerçekleme tamam (3.1–3.7, K-152…K-159) · **v0.4 varsayılan** = `PROFIL_V02` + `SECENEK_V04` (V1 + V5 + V7 + V8 + V10; K-167, ajan — öğrencinin devriyle). Küçük dünya 300 s, geliştirme tohumları 1003–1005: pencere PDR v0.2 0,787 · 0,818 → v0.3 0,686 · 0,764 → v0.4 **0,786 · 0,808**; kontrol yükü v0.2'nin %57'si (`arsiv/teshis/desparete_edinim_2026-09-25/uzun_ab.py` + `ozet.py`). **Tam ölçekte (N = 40) ve karıştırıcılı hücrede doğrulanmadı** |
| test takımı | `820 passed` — `python -m pytest tests2 -q` (25 Eylül, 751 s) |
| regresyon tabanı | `k157`, 45 vaka — `python -u kalibrasyon/regresyon_satirlari.py karsilastir k151 k157` BİREBİR; `k157`'den sonra `sim2/` değişmedi. ⚠️ Matriste gerçek protokol vakası yok |
| mimari denetimi | ihlal 0 · 133 modül · 169 parametre · **SINANMAMIŞ 40** · **duyarlılık borcu 9** — `python kalibrasyon/mimari_denetimi.py`; adlar `python arsiv/teshis/belge_guncelleme_2026-09-25/borc_listesi.py` |
| çalışma noktası | tek karıştırıcı −15,0 dBm, ρ = 0,258 · 1800 m · N = 40 · 40 pkt/s (iki desen eşit) · ana deney tohumlarının 15 (kol, tohum) çiftinde ağ pencerede bölünüyor (K-132, beyanlı) |
| ön-kayıt | taslak; §0.4 (eşik formülü, güç yöntemi, aday birincil hücre `formasyon · yere_toplama · hava_eslik · sürekli`, PDR, Δ_hedef 0,05) bağlayıcı (K-153) |
| dış çapa · çözünürlük | Li H1 = 0,0871 (tutmadı; mekanizma doğrulandı; 25 Eylül yeniden koşuldu) · eşleştirilmiş R = 0,0230 (40 tohum) |

## 2 · Kritik yol — sıra neden böyle

```
KR-1 kâhin teyidi ──────────────────────────────────────────────┐
KR-2 birincil metrik ─┐                                          │
KR-4 yapı paketi ─────┴→ İ-1 simülatör yapı paketi (kimlik + PDR yönü) ──┐
                                                                 │        │
İ-2 v0.4 tam ölçek → İ-3 iyileştirmeler → İ-6 profil dondurulur → İ-4 resmi U1 + U3 ─┐
                                                                                    │
İ-7 taban U1 yere toplamada ─┐                                                      │
İ-8 adillik → taban protokoller DONAR ─┴→ İ-26 gürültü ölçümü → İ-27 güç → tohum sayısı ─┤
                                                                                    │
İ-13…İ-25 kalanlar · İ-28 ön-kayıt metni · İ-29 analiz katmanı · İ-30 doğrulama ──┴→ İ-32 🔒 MÜHÜR → İ-33 ana deney → Aşama 5
```

Üç bağımlılık sırayı belirliyor:
1. **δ taban protokollerden türüyor** (`06` §0.4.2). Taban protokollerde bir adillik düzeltmesi (İ-8) gürültü ölçümünden (İ-26) SONRA gelirse δ bayatlar → önce İ-8, taban protokoller donar, sonra İ-26.
2. **Satır bugün PDR'yi trafik yönüne göre ayırmıyor** (telemetri ↔ komut) ve **koşu kimliği tedaviyi ayırmıyor** → gürültü ölçümü ve ana deney bu iki düzeltmeden (İ-1) sonra koşulmalı; aksi hâlde yeniden koşulur.
3. **DESPARETE mühürde sabitlenir** (`06` §0.2) → iyileştirmeler (İ-3) mühürden önce biter; Aile 3 kolları (KR-14) son profile göre adlandırılır.

---

## 3 · Aşama 3 — DESPARETE (sıradaki, sırayla)

### İ-1 · Simülatör yapı paketi — tek regresyonla [yapı] 🟦 KR-4

Birden çok `sim2/` değişikliği tek pakette yapılırsa tek regresyon (`uret` ~35–45 dk) yeter. Hepsi önce yapı anlatımıyla öğrenciye sunulur.

| # | ne | neden | durum |
|---|---|---|---|
| 1a | **`kosu_kimligi`** — kimliğe tedavi alanlarının özeti ve protokol parmak izi (ad + `protokoller/` kod özeti + protokolün bildirdiği parametreler, DESPARETE'de bayrak ve seçenek demeti); satıra `tedavi_hash`, `protokol_hash`; araç özetinde CRLF normalizasyonu | bugün farklı senaryo, desen, tehdit, protokol ve profildeki koşular aynı kimliği alabiliyor (denetim Y-1); ana deneyde ve Aile 3 kollarında satırlar karışır (Ö-7) | ✅ öğrenci onaylı (25 Eylül); yapı anlatımı bekleniyor |
| 1b | **PDR'nin trafik yönüne göre ayrılması** — satıra telemetri (geçide) ve komut (geçitten) PDR'si ayrı, pencere ve tüm koşu | KR-2 hangi tanımı seçerse seçsin ikisi de raporlanmalı; bugün satır yalnız toplam PDR taşıyor, sonradan hesaplanamaz | öneri |
| 1c | **Politika düşmesi için ayrı düşme sebebi** — C kararıyla düşen komutlar bugün `hedef_yok`a karışıyor | düşme sebepleri protokoller arasında karşılaştırılıyor; "rota bulunamadı" ile "tasarım kapsamı dışı" ayrı şeyler (denetim D-4) | öneri |
| 1d | **Regresyon matrisine gerçek protokol vakaları** — AODV · OLSR · AOMDV · DESPARETE, kısa pencere, birer vaka | matriste yalnız koşum aletleri ve kâhinler var; protokol davranışındaki kaymayı hiçbir kapı yakalamıyor (O-4) | öneri |
| 1e | `07` §17 **A6** (`iletim_menzili_m` adı yanlış bir iddia taşıyor — "verici gücü çapası") ve **A8** (`Konfig` varsayılan deseni hâlâ `esler_arasi`; birincil desen yere toplama) | ad ve varsayılan, ana deney aletinin yanlış bir şeyi sessizce koşmasına yol açabilir | öneri — A8 yerine "ana deney aleti deseni açıkça verir" kuralı da yeter |
| 1f | küçük `sim2/` belge–kod uyumsuzlukları (denetim D-6: `YerelZaman`, docstring'ler) | araç özeti zaten değişecek | öneri |

**Kapı:** tam takım · yeni test "farklı koşu → farklı kimlik" · `uret <yeni>` + `karsilastir k157 <yeni>`: beklenen fark ÖNCEDEN yazılır (yalnız kimlik alanları, yeni alanlar ve araç özeti; hiçbir metrik değişmez). **Süre:** kod 2–4 sa · regresyon 35–45 dk.

### İ-2 · v0.4'ün tam ölçek doğrulaması [süre] 🟦 KR-3

- **Ne:** v0.2 ↔ v0.4, N = 40. Hücreler: `bagimsiz-yok` ve `formasyon-yok` (K-1'in göründüğü kollar) + **birincil hücre** (formasyon · yere toplama · hava eşlik · sürekli). Geliştirme tohumları 1003–1005 (U1'in 1000–1002'si değil — denetim Y-3).
- **Neden:** v0.4 yalnız küçük dünyada (14 düğüm), karıştırıcısız, 2 kolda ölçüldü. Tam ölçekte ve karıştırmada davranışı bilinmiyor; resmi U1 (5–7 sa) bundan önce koşulursa boşa gidebilir.
- **Ölçülecek:** pencere PDR (telemetri) · zaman dilimli PDR · kontrol/veri kanal süresi · gecikme p95 (ortak alt küme + kesişim oranı) · geçitte işlenen istek → tur artışı · açlık istekleri · her kancadan sonra döngü 0 · **iş başına süre** (ana deney bütçesi, O-11).
- **Önerilen biçim:** birincil hücre **350 s** (ana deneyin uzunluğu; 40 s ve 120 s'nin zamanla biriken etkiyi göremediği K-165/K-166'da görüldü) + iki `-yok` kolu 120 s; 3 tohum × 2 profil = 18 iş.
- **Beklentiler ölçmeden önce yazılır** (örnek taslak: v0.4 pencere PDR'si v0.2'den en çok 0,03 düşük · kontrol/veri her koşuda v0.2'nin altında · tur artışı her koşuda > 0 · döngü 0).
- **Süre:** 3–5 sa (8 işçi). **Kapı:** beklentiler; tutmayan her beklenti İ-3'te çözülür.

### İ-3 · DESPARETE iyileştirmeleri — ajan çözer, ölçer, kanıtla getirir

Öğrencinin kuralı (25 Eylül): kusur bulununca ajan çözer; davranışı değiştiren her karar kayda "ajan" diye geçer, öğrenci geri alabilir. Tasarımın **fikrini** değiştirenler 🟦.

| # | sorun (kanıt) | aday çözüm | ölçüm | karar |
|---|---|---|---|---|
| 3a | v0.4'ün kontrol yükü v0.3'ün +%26'sı; önceden yazılan %15 sınırı tutmadı (K-167 E8); nitelik PROBE'u 1 103–1 786 → 2 214–3 148 | nitelik PROBE'unun MAC onayını ilk M0.1 örneği saymak → V7'nin ek PROBE'u gereksizleşir (denetim Ö-6; `35` §3.1'in yorumu) | küçük dünya 300 s + birincil hücre, eşli A/B, 3 tohum | 🟦 KR-8 (tasarım yorumu) |
| 3b | FIELD_SOLICIT yolu v0.4'te de ölü: yanıt ACTIVE ister (`23` §5.2), V9 zararlıydı (K-167) | önce soru: solicit'in işe yaradığı durum (yeni katılan, uzak düğüm) var mı → yoksa "V8'in istek yolu yeterli" diye beyan; varsa yanıt koşulunu `23` §2'nin tanıdık kuralına bağlamak | solicit gönderilen/yanıtlanan, geç katılan düğüm senaryosu | 🟦 KR-7 |
| 3c | DFSN yalnız istekle artıyor; istek yolu herhangi bir sebeple kapanırsa açlıktan çıkış yok (denetim Ö-3) | hedefin seyrek periyodik tur artışı (DSDV gibi, 30–60 s) ya da TG-04'ün oran kapısıyla | 350 s, FD açlığı sayacı, ulaşılamaz bölüm, eşli A/B | 🟦 KR-5 — İ-2 açlık gösterirse |
| 3d | CAUTION girişlerinin %100'ü belirsizlikten (U ≥ 128, 190/190); PROTECT yapı gereği yok; karıştırmada +%4,4 yük, teslime katkı görünmüyor (K-158) | CAUTION yalnız H ≥ 64 ile · U eşiği trafik hızına bağlı · belirsizlikte yalnız izleme · ya da postür Aile 3'te ablasyon kolu olur; ölçülmezse "temel fikir" iddiası README'den çıkar (O-7) | birincil hücre, eşli A/B | 🟦 KR-6 |
| 3e | ölçülmemiş iki sabit: onarım tamponu kotası 6 ↔ 32 · belirsizlik eşiği ↔ sondalama hızı (K-150 §3.4, K-158 §6) | kısa duyarlılık | birincil hücre, 3 tohum | ajan |
| 3f | DESPARETE sabitleri köken defterinde yok (`protokoller/`; denetim D-5) | sabitler kovalarına yazılır (tasarım paketinden KAYNAK, ölçülenler ÖLÇÜLMÜŞ) | mimari denetimi kapsamı `protokoller/`e | ajan |

**Süre:** her aday 1–3 sa (kod + kısa ölçüm). **Kapı:** her adayın beklentisi önceden yazılı; tam takım.

### İ-4 · DESPARETE resmi U1 + U3 [süre] ← KR-1

- **U1:** yere toplamada (K-150), dört `-yok` kolu × 1000–1002, tam pencere, **tüm koşu PDR'si** (öğrenci), oran = DESPARETE / ETX kâhini, eşik statik ≥ 0,90 · hareketli ≥ 0,60. `python -u kalibrasyon/aodv_uygunluk.py --protokol desparete` · **5–7 sa**.
- **Kâhin aşımı** KR-1'e göre okunur: aşım otomatik ret değil, "yazılım hatası mı, kâhin bu hücrede üst sınır değil mi" incelemesi.
- **U3:** kontrol yükünün 60 → 120 s davranışı. `… aodv_uygunluk.py u3` bugün yalnız üç taban protokolü koşuyor; DESPARETE eklenir (yalnız `kalibrasyon/`) — < 30 dk koşum. U2 ve U4 karşılıkları testlerde var (K-160).
- **Kapı:** U1-U geçer (kalırsa protokol kabul edilmez) · U1-B eşik altı her hücre ölçümle açıklanır · sonuç kaydı ve `06` §10.

### İ-5 · Tasarım paketinin güncellenmesi 🟦 KR-9

Paket öğrencinindir (`protokol_kaynaklari/DESPARETE_TASARIM_PAKETI/`). İşlenecekler: TV-02 (kurallar 28 verir, belge 40) · DFSN_REQUEST boyu (diyagram 76 ↔ metin 72) · durum makinesindeki eksik satır · C kararı (yalnız geçit alanı; komutlar politika hatası) · yalın profil (v0.2) · V1 · V5 · V7 · V8 · V10 (neden, kanıt, kimin) · UNREACHABLE'dan çıkış (ajan seçimi, K-152) · CAUTION'ın eylemi (girişte doğrulama, K-150) · tek yayın DFSN_REQUEST ve kabul kuralı (K-167) · gelecek çalışmalar (§13). Ajan değişiklik listesini taslak olarak hazırlayabilir.

### İ-6 · Profilin dondurulması (Aşama 3'ün çıkışı)

Son profil adı ve içeriği (v0.4 ya da İ-3 sonrası v0.5) · bütün sabitler kovalı (3f) · ablasyon bayraklarının ve seçeneklerin listesi (Aile 3 için, KR-14) · tam takım · regresyon · U1. **Aşama 3'ün çıkış kapısı:** son profil tam ölçekte doğrulandı (İ-2) · resmi U1-U geçti, U1-B açıklandı, U3 ölçüldü (İ-4) · tasarım paketi güncel (İ-5) · kayıt (`04`).

---

## 4 · Aşama 2'den kalanlar — taban protokoller (İ-26'dan ÖNCE kapanmalı)

### İ-7 · Taban protokollerin yere toplamada U1'i [süre]

- **Ne:** `AODV-e` · `OLSR-b` · `AOMDV-a`, dört `-yok` kolu × 1000–1002, yere toplama deseni, tam pencere, tüm koşu PDR.
- **Neden:** birincil hücre yere toplamada; taban protokollerin kabulü bugün yalnız eşler arası desende (denetim Y-3). Öğrenci onayladı (25 Eylül).
- **Hazırlık:** U1 aletine `--desen` seçeneği (yalnız `kalibrasyon/`; bugün desen yalnız DESPARETE için sabit) ve sonuç dosyası ayrı ad alır (eşler arası kayıtlar ezilmez). Kâhin koşuları protokolden bağımsız → bir kez koşulup paylaşılabilir (İ-4 ile de).
- **Süre:** eşler arası kayıtlı iş süreleri AODV 15 · OLSR 21 · AOMDV 18 iş-saat (kâhin dâhil; `python arsiv/teshis/belge_guncelleme_2026-09-25/u1_sureler.py`) → 8 işçiyle **7–9 sa**; kâhin paylaşılırsa **5,5–7 sa**. Bir gece.
- **Kapı:** her protokolde U1-U geçer · U1-B eşik altı hücre açıklanır. Kalırsa: mekanizma teşhisi, gerekiyorsa İ-8'le birlikte düzeltme.

### İ-8 · Adillik ölçümleri [süre] — öğrenci onaylı (*"senin önerini yapalım"*)

| # | soru | yöntem | süre |
|---|---|---|---|
| 8a | karıştırmada bağlar ne kadar **tek yönlü**? AODV/AOMDV'nin RREP-ACK ve kara listeyi atlamasının gerekçesi "bağ simetrik"ti; karıştırıcı gücü alıcıda eklendiği için SINR asimetrik (denetim O-1) | birincil hücrede kanal grafiğinden tek yönlü bağ oranı — **protokolsüz, ucuz** | < 30 dk |
| 8b | 8a büyükse: RREP-ACK + kara liste (RFC 3561 §6.8) AODV ve AOMDV'de seçenek olarak yazılır | birincil hücre, 5 geliştirme tohumu, eşli A/B | 3–5 sa |
| 8c | rota tamponu 64 paket · 30 s AODV'de doluyor (tepe 64/64, süre tavanından düşen 89; O-8) | birincil hücrede 64 ↔ 256 ve 30 ↔ 60 s | 2–3 sa |
| 8d | yeniden deneme sınırı 4 (802.11 kısa sınırı 7; K-098'de etkisiz ölçülmüştü) | birincil hücrede 4 ↔ 7 | 2–3 sa |

**Kapı:** fark çözünürlüğün (R = 0,0230) altındaysa beyan; üstündeyse taban protokol RFC'ye yaklaştıran yönde düzeltilir (yeni kod hâli, ör. `AODV-f`), U1 yeniden koşulur, kaydedilir 🟦 KR-10. 8d ve 8c'nin varsayılanı değişirse [yapı] (Konfig varsayılanı → regresyon). **Bu iş bitince taban protokoller DONAR.**

### İ-9 · AOMDV'nin U2/U4 karşılıkları adıyla eşlenir (`06` §9) — test adları ve belge; < 1 sa.

### İ-10 · M4'ün boş kol kapısı — gerçek protokolle

Evre metriği "tespit gecikmesi"nin G1 maddesi o gün beyan etmeyen bir koşum aletiyle boş geçmişti (`08` §05). Karıştırıcısız kolda gerçek bir protokolle (AODV ve DESPARETE) yanlış tespit oranı ≤ α = 0,05 mi? U1 koşularının satırlarından hesaplanabiliyorsa 0 ek koşum; değilse 1–2 sa.

### İ-11 · ⚪ Açıklama ölçümleri (şart değil; raporda "hipotez" kalabilir)

OLSR §13'ün hareketli kollardaki bedelinin mekanizması (K-147) · AOMDV'nin bayat yedek yolu (S2, K-149). Ana deneyi beklemez; zaman kalırsa.

### İ-12 · AOMDV öngörüsü → ön-kayda (İ-28)

Eski öngörü karıştırıcı modeli değiştiği için geçersiz; yeni tehdit modeline göre, **sonuç görülmeden** yazılır (`06` §4.1) 🟦 KR-13.

---

## 5 · Aşama 1'den kalanlar — simülatör, kalibrasyon, kaynaklar (mühürden önce)

| # | iş | neden | süre | karar |
|---|---|---|---|---|
| İ-13 | **C4** · formasyonda Θ daha çok tohumla | kestirici az örnekle çalışıyor (çiftlerin %92'si hiç kopmuyor, Θ aşağı yanlı) | 10–30 dk | — |
| İ-14 | **C5** · görev kolu yarıçapı büyük örneklemle (~140 tohum; `calisma_noktasi.py --bolum gorev_kolu`) | görev kolu tanımının sabiti | 1–3 sa [süre] | 🟦 KR-17 (görev kolu ana deneye girmiyorsa düşebilir) |
| İ-15 | **C6** · ısınma × ölçüm penceresi birleşik taraması; açılma anı parametre | `06` §8 koşul 1 (koşu uzunluğundan bağımsızlık); `isinma_s` ve `olcum_bitis_s` SINANMAMIŞ'tan çıkar | 1–3 sa [süre] | — |
| İ-16 | **SINANMAMIŞ 40 → 0** (aşağıdaki tablo) | mühür şartı (`06` §9) | literatür 3–6 sa · ölçüm 3–8 sa | 🟦 KR-11 (indirmeler) |
| İ-17 | **Duyarlılık borcu 9 → 0** — `darbe_periyodu_s` · `darbe_gorev_cevrimi` · `taramali_konak_suresi_s` · `taramali_konak_sayisi` · `karistirici_konum` · `gecit_konumu` · `istasyon_kayma_hiz_ms` · `tehdit_acik_s` · `tehdit_sessiz_s` | ilk dördü 8 Eylül'de DUYARLI ölçüldü (sonucu belirliyor); her biri ya gerekçelenir ya ön-kayıtta **eksen** ilan edilip oynatılır | eksen ilanı: 0 sa · ölçüm: 2–6 sa | 🟦 KR-12 |
| İ-18 | **Kaynak doğrulamaları** `02` §S: S1 Rician K = 6 dB · S2 802.11b sabitleri (IEEE 802.11-2016) · S3 karıştırıcı saha davranışı künyeleri · S4 telemetri hızı/boyu · S5 kapsülleme (RFC 791 · 768 · 1042) · S6 Babel RFC 8966 (README'de anılıyor) | KAYNAK kovası yalnız açılıp okunmuş belgeyle; README'deki atıf doğrulanmadan rapora giremez | kaynak başına 0,5–1 sa | 🟦 KR-11 |
| İ-19 | `07` §17 **A23** — kodun kapsam listesi `07` §12 ile karşılaştırılır (A6, A8 İ-1e'de) | ayrışma defteri | < 1 sa | — |
| İ-20 | **Bölünme tablosunun yeniden koşulması** (K-132; `--bolunme`, protokolsüz kanal grafiği) | bugünkü kodla geçerliliği doğrulanmadı (denetim §6); ana deneyin formasyon kolunda 2 tohum bölünüyor | < 30 dk | — |
| İ-21 | **Çoklu/hareketli karıştırıcıda evre tanımı** — birincil hücre `hava_eslik`: açılma anı, şok penceresi, M1–M4'ün okunuşu | `08` şok evresini tek açılma anıyla tanımlıyor; hareketli karıştırıcıda "şok" ne demek, sonuç görülmeden yazılmalı | yazı 1–2 sa | 🟦 KR-13 |
| İ-22 | **PSR'nin doğrulama kapısı** (`06` §8 koşul 2 🔵) · bağ başına PSR (🔵) | rapora sonuç olarak girecekse kapı gerekir; yalnız betimleyiciyse gerekmez | kapı 2–4 sa | 🟦 KR-18 |
| İ-23 | **`algilama_duyarliligi`nin ikiye bölünmesi** — fiziksel kopma sayımı çalkantıyı ölçüyor, karıştırmayı değil | kopma metriklerinin ne ölçtüğü | 2–4 sa [yapı] | — |
| İ-24 | **İz kanalı (Y8)** — görselleştirme için; ölçüme dokunmaz, kapısı "iz açık/kapalı satır birebir" (`07` §13) | Aşama 5'in canlı gösterimi | 1–2 gün [yapı] | — |
| İ-25 | Kontrol düzlemi açık riskleri R5 (kapsülleme asimetrisi) · R7 (tavan sayıyı sınırlar) → rapor beyanı; R6 → İ-16 | `13` §06 | yazı | — |

**İ-16'nın dökümü — 40 SINANMAMIŞ, nasıl kapanır** (adlar ve gerekçe metinleri `borc_listesi.py`'nin çıktısında):

| yol | parametreler |
|---|---|
| **kaynakla** (İ-18) | `bit_hizi_bps` · `onay_bayt` · `cca_s` · `yeniden_deneme_siniri` · `yakalama_esigi_db` · `yakalama_penceresi_s` · `KONTROL_KAPSULLEME` · `rician_k_db` · `beacon_araligi_s` (RFC 3561 zaten `02`de) · `saat_ofset_araligi_s` · `saat_sapma_ppm` (kristal belgesi) · `tehdit_arac_hiz_kmh` · `tehdit_hava_hiz_kmh` (S3) · `rota_tamponu_kapasitesi` · `rota_tamponu_omru_s` (İ-8c ile) · `ttl_baslangic` |
| **ölçümle** (duyarlılık denetimi, birincil hücre) | `golgeleme_hucre_m` · `gm_adim_s` · `kanal_dilimi_s` · `irtifa_maks_m` · `komsu_omru_katsayisi` · `kuyruk_kapasitesi` · `beacon_bayt` · `BAGIL_HIZ_TABANI_MS` · `ISTASYON_TUTMA_S` · `akis_sayisi` · `akis_paket_hizi_hz` · `gorev_grup_sayisi` · `UYE_TABANI` |
| **pencere taramasıyla** (İ-15) | `isinma_s` · `olcum_bitis_s` |
| **gerekçe yazımıyla** (örneklem büyüklüğü hata payından; aletin kendi sabitleri) | `calisma_noktasi::BASARI_ESIGI` · `calkanti::ADIM_S` · `calkanti::CIFT_SAYISI` · `duyarlilik::TOHUMLAR` · `evre_metrikleri_kapilari::TOHUMLAR` · `formasyon_olcumu::ORNEK_ADIM_S` · `formasyon_olcumu::YARICAP_M` |
| **güvenlik sınırı / ön-kayıttan** | `BEKLEYEN_UYANDIRMA_TAVANI` (aşılırsa koşu FAIL — sonucu etkileyemez; tepe değer satırda) · `evre::ALFA` (`06` §7'den → TÜRETİLMİŞ) |

---

## 6 · Aşama 4 — pürüz temizleme ve veri

### İ-26 · Gürültü ölçümü → δ [süre] ← KR-2 · İ-1 · İ-8

`06` §0.4.2: üç taban protokol × 20 geliştirme tohumu (1100–1119) × birincil hücre, tam pencere → `d_XY(s)`, `SD_ref`, `δ = 2 · SD_ref / √40`. **Süre:** kayıtlı formasyon iş süreleri AODV 71 · OLSR 118 · AOMDV 80 dk (karıştırıcısız; karıştırmada daha uzun olabilir) → 60 iş ≈ 90–135 iş-saat → 8 işçiyle **11–17 sa**. Bir gece + bir gün.

### İ-27 · Güç analizi ve tohum sayısı

`06` §0.4.3: B = 2 000, `MDE₈₀`, δ'daki güç; `MDE₈₀ > Δ_hedef` ise mühürden ÖNCE tohum artırılır (`n' = ⌈n · (MDE₈₀/Δ_hedef)²⌉`). **Eksik (denetim O-9):** benzetim bugün yalnız Wilcoxon'u sınıyor; "üstün" hükmünün öteki iki koşulu (ortalama fark ≥ δ ve mekanizma kapısı) da benzetime girmeli. Betik `arsiv/teshis/guc_on_tahmin_2026-09-23/guc.py` → izlenen yere (İ-42). Süre: 2–4 sa.

### İ-28 · Ön-kaydın tamamlanması (`06` §9) 🟦 KR-13 · KR-14 · KR-15

- Birincil hücrenin kesinleşmesi (aday §0.4.4) · birincil metriğin tanımı (KR-2) · α · δ'nın değeri · güç · tohum sayısı.
- **Aile 1** (taban protokollerin karakterizasyonu): H1.1 · H1.2 · H1.3'ün birincil hücreleri, eşikleri, birincil testleri; ölçülmüş tahminler (`06` §5.1).
- **Aile 3** (mekanizma): ablasyon kolları (KR-14; v0.4'e göre adlandırılır, ör. "v0.4 − risk terimi"; her kol kimlikte ayrışır — İ-1a) · mekanizma kapısının tanımı (O-9) · eski m = 5 permütasyon ölçütünün yeniden yazılması (`06` §5.3).
- **AOMDV öngörüsü** (İ-12) · **çekirdek matris**: hangi kol × aile × sınıf (KR-15) · koşul 1'in `k` değeri (İ-15'ten) · **durdurma kuralı** mutlak birimle · evre metriklerinin sabitleri ve çoklu karıştırıcı tanımı (İ-21).
- Parametrelerin sabitlenmesi: taban protokoller RFC varsayılanında (İ-8 sonrası), DESPARETE son profilde (İ-6).
- Güvenlik Profili 1'in bayt bedeli kolu (K-150 kararı: ayrı duyarlılık kolu) — keşifsel mi çekirdek mi.
- Mühür sırasının öğrenci onayı (KR-20) · `06` §10 kayıt tablosu.

### İ-29 · İstatistik katmanı `analiz/` (henüz yok)

Eşleştirilmiş, çift yönlü Wilcoxon · Holm (aile içinde) · %95 GA ve etki büyüklüğü · negatif sonuçta dışlanan etki ve ulaşılan güç · **NaN tuzağı kapısı** (tüm farklar sıfırken `scipy` NaN döndürüyor) · gecikmede ortak alt küme + kesişim oranı · yüzdeliklerin ham listeden yeniden üretimi · satırdaki bayrak/seçenek demetinin kol etiketiyle ve kimlikle denetimi (Ö-7) · geçersiz satır kuralı. Testleriyle. **Süre:** 1–2 gün; İ-26 koşarken yazılabilir (O-11 önerisi).

### İ-30 · Doğrulama listesinin tamamı — Aşama 3 → 4 geçişi

`DEVIR.md` §2'nin bütün maddeleri yeni kodla bir kez (K-129: koşulmayan kapı kapı değildir). Uzun maddeler: duman 30–45 dk · adım 9 kapanışı 60–90 · evre kapıları 50–70 · kontrol düzlemi 16–20 · PDR tavanı 15–25. **Süre:** 4–6 sa, bir gece.

### İ-31 · Hesap bütçesi ve kod dondurma (denetim O-11)

Ana deneyin iş sayısı × ölçülmüş iş süresi (İ-2'de DESPARETE'nin 350 s süresi ölçülür) → takvime sığıyor mu (§10). Kod dondurma noktası (hangi commit) mühürde yazılır.

### İ-32 · 🔒 MÜHÜR — öğrenci

Hipotezler · eşik değerleri · parametreler · tohum sayısı · birincil hücre · çekirdek matris · bütçe · kod dondurma. Hedef ~1 Kasım. Mühürden sonraki her değişiklik `06` §10'a, ilgili hipotez keşifsel etiketlenir.

### İ-33 · Ana deney [süre]

4 protokol × çekirdek hücreler × 40 tohum (2000–2039 — mühürden önce hiç koşulmaz) + Aile 3 kolları. Parça parça koşulabilir; her satır kendi konfigürasyonunu ve kimliğini taşır. Geçersiz (korunumu tutmayan) satırın yeniden koşum kuralı mühürde. **Bütçe §10.**

### İ-34 · Keşifsel eksenler 🟦 KR-16

Yüksek çalkantı · görev kolu · eşler arası desen · kalan dört tehdit ailesi ve dört karıştırıcı sınıfı · güç (ρ) taraması (H1.2'nin dirseği) · derinlik · Güvenlik Profili 1 kolu · (iki geçit: yapı gerektirir, bugün yok → gelecek çalışma). Takvim sıkışırsa ilk düşenler (§12). Tohum sayısı 40 olmak zorunda değil (keşifsel; KR-16).

### İ-35 · Analiz ve sonuç tabloları

Üçlü sunum (teslim · gecikme · kontrol yükü; tek metrikle sıralama yok) · aile başına hükümler · negatif sonuçlar dürüstçe · koşul 1–4'ün her sonuç için kontrolü (`06` §8).

---

## 7 · Aşama 5 — rapor ve sunum (~15 Kasım – 19 Aralık; yazım ~5 hafta, kısaltılmaz)

| # | iş |
|---|---|
| İ-36 | **Rapor yazımı** — problem, yöntem, simülatör ve doğrulaması (Li dâhil), taban protokoller, DESPARETE, sonuçlar, negatif sonuçlar, sınırlar |
| İ-37 | **Görselleştirme** — iz kanalıyla (İ-24) düğümler, bağlar, karıştırıcı etki alanı ve hareketi, geçide rotalar, kopma/kurtarma, evre çizgili PDR eğrisi (`07` §13) |
| İ-38 | **Beyanlar** — simülasyon–gerçeklik beyanı (`01` §8) · kapsam dışı (`07` §12) · taban protokol sapmaları (AODV yerel onarım yok, RREP-ACK/kara liste (İ-8), karşılıksız RREP yok, RREQ'te 1 B fazla · OLSR §13 istisnası · AOMDV S1–S10) · DESPARETE sapmaları (güvenliksiz ana karşılaştırma, yedekliliksiz, hedef alanı emekliliği yok, komutlar düşer, V1–V10'un tasarımdan farkları) · Li'nin α farkı · bölünen tohumlar · ana deney tohumlarıyla kanal grafiği kurulduğu (B-1) |
| İ-39 | **Fikir sahipliği** — katkı tablosu: her mekanizma ve karar kimin (öğrenci / ajan), kayıt numarasıyla (O-10) · ablasyonla ölçülmüş katkı payları · tasarım paketinin üretim süreci belgesi (hangi araçla, nasıl yazıldı — denetim: kaynağı depoda yok) 🟦 KR-19 |
| İ-40 | Poster, sunum, jüri savunması hazırlığı (olası sorular: kâhin, "bu sayının ne kadarı senin", Li neden tutmadı, neden kendi simülatörü) |
| İ-41 | ⚪ TÜBİTAK 2204-A başvuru biçimi ve rehberi — öğrenci 10 Eylül'de iş planına almadı; yazım başlamadan kontrol edilmeli |

---

## 8 · Depo ve yöntem — sürekli işler

| # | iş | neden | kim |
|---|---|---|---|
| İ-42 | **Kanıtın depoya alınması** — DESPARETE teşhis betikleri (`arsiv/teshis/…`, git dışı) profilleri açık, küçük çıktılarıyla izlenen bir dizine; `kayit_indeksi.py` → `kalibrasyon/`; güç betiği | kayıtlardaki sayıların üreticisi depoda yok (denetim Y-6) | ajan taşır, öğrenci commit eder 🟦 KR-19 |
| İ-43 | **Git hijyeni** — izlenen 154 `.pyc`'yi indeksten çıkar (`git rm --cached`) · `.gitattributes` (satır sonları) · iş başına commit · "ölçmeden önce" beklentilerini koşudan ÖNCE commit etmek (O-6'nın tek kanıtı) · bekleyen değişikliklerin commit'i | yeniden üretilebilirlik; denetim D-2 · D-3 · O-6 | [git] öğrenci |
| İ-44 | **README iddiaları** — postür "temel fikir" (İ-3d'ye bağlı, O-7) · değerlendirilen profil tablosu · Babel atfı (İ-18 S6) | kamu yüzü doğru olmalı | ajan |
| İ-45 | Her işten sonra `v2/12`, `DEVIR.md`, `04` güncellenir; belgeler öz | bayat belge (O-5) | ajan |

---

## 9 · Öğrenci kararları — tek liste (öneriyle)

| # | karar | ne zamana kadar | ajanın önerisi |
|---|---|---|---|
| KR-1 | **Kâhin kuralı okumasının teyidi:** kâhini aşmak otomatik ret değil, "yazılım hatası mı / kâhin bu hücrede üst sınır değil mi" incelemesi | İ-4'ten önce | teyit — karıştırıcısız hareketli kollarda kâhin PDR'si 0,76–0,89; aşmak gerçekçi |
| KR-2 | **Birincil metrikte komutlar** — (a) bütün trafik: C kararıyla DESPARETE'nin komutları yapısal olarak düşer (~%2,5, PDR tavanı ~0,975; δ ve Δ_hedef mertebesinde) · (b) yalnız telemetri · (c) birincil telemetri, bütün trafik ikincil | İ-26'dan önce (δ metriğe bağlı) | **(c)** — birincil test bir kapsam kararını değil yönlendirmeyi ölçmeli; komut kaybı önceden bilinen, yapısal. Senin 24 Eylül cümlen ("komut kaybı DESPARETE'nin aleyhine sayılır") ikincil metrikte ve ayrı komut teslim tablosunda korunur. Bedeli: (a)'dan daha az muhafazakâr |
| KR-3 | **İ-2'nin kapsamı** — yalnız 120 s × 3 tohum (2,5–4 sa) · birincil hücre 350 s dâhil (3–5 sa) · her şey 350 s × 5 tohum (~10–15 sa) | İ-2'den önce | **birincil hücre 350 s dâhil** — ana deneyin uzunluğu ve bütçe ölçümü birlikte |
| KR-4 | **İ-1 yapı paketinin kapsamı** — yalnız kimlik (onaylı) mı, + 1b PDR yönü + 1c politika düşme sebebi + 1d protokol vakaları + 1e A6/A8 + 1f belgeler mi | İ-1'den önce | hepsi tek pakette (tek regresyon); 1b KR-2'den bağımsız olarak şart |
| KR-5 | DFSN'nin periyodik tur artışı (Ö-3) — tasarıma yeni kural | İ-2 açlık gösterirse | önce ölç; açlık görülmezse beyan |
| KR-6 | **Postür/CAUTION** — dört seçenek (İ-3d); ölçülmezse "temel fikir" iddiası daralır | mühürden önce | Aile 3'te ablasyon kolu + U eşiğinin trafik hızına bağlanması denenir |
| KR-7 | FIELD_SOLICIT'in akıbeti (İ-3b) | İ-3b'nin ölçümünden sonra | işe yaradığı durum yoksa beyanla bırakılır |
| KR-8 | Nitelik PROBE'unun onayı ilk M0.1 örneği sayılsın mı (İ-3a) | İ-3a'dan sonra | ölçülüp yük düşüyorsa evet |
| KR-9 | Tasarım paketini kim günceller (İ-5) | Aşama 3 çıkışı | ajan değişiklik listesini hazırlar, sen işlersin |
| KR-10 | Adillik farkı çözünürlük üstündeyse taban protokol düzeltilsin ve U1 yeniden koşulsun mu (İ-8) | İ-8 sonucu | evet, RFC'ye yaklaştıran yönde |
| KR-11 | **İndirme izinleri** — IEEE 802.11-2016 (ücretli olabilir; yoksa erişilebilir ikincil kaynak + beyan) · RFC 8966 · RFC 791 · 768 · 1042 · S3 künyeleri | İ-16 / İ-18 | RFC'ler serbest; IEEE için erişim yolunu sen seç |
| KR-12 | Duyarlılık borçlusu dokuz sabit: gerekçe mi, eksen mi | mühür | birincil hücrede (sürekli, hava eşlik) devrede olmayanlar — darbeli ve taramalı sınıfın sabitleri, yay–sus süreleri — keşifsel eksene ya da beyana; devrede olanlar (`gecit_konumu`, formasyonun `istasyon_kayma_hiz_ms`'i, gerekirse `karistirici_konum`) birincil hücrede ölçülür. Hangisinin devrede olduğu önce kodda doğrulanır |
| KR-13 | **Aile 1 hipotezleri** ve hücreleri · AOMDV öngörüsü · çoklu karıştırıcıda evre tanımı (İ-21) | mühür | taslakları ajan hazırlar, sonuç görülmeden sen onaylarsın |
| KR-14 | **Aile 3 kolları** — sekiz bayrak + seçenekler (V1 · V5 · V7 · V8 · V10) arasından hangileri | mühür | sonucu en çok belirleyenler: kalite terimi, risk terimi, postür, V5, V8+V10 |
| KR-15 | **Çekirdek matris** — ana deneye kaç hücre (bütçe §10) | mühür | birincil hücre + Aile 1 için 2 hücre + Aile 3 kolları birincil hücrede |
| KR-16 | Keşifsel eksenler ve tohum sayıları | mühür | 10–20 tohum; kayma sırası §12 |
| KR-17 | Görev kolu (C5) ve yüksek çalkantı — keşifsel mi, düşer mi | İ-14'ten önce | görev kolu ana deneye girmiyorsa C5 düşer |
| KR-18 | PSR raporda sonuç mu betimleyici mi | mühür | betimleyici (kapı gerekmez) |
| KR-19 | Kanıtın depoya alınması (dizin, çıktı boyutu) · katkı tablosunun biçimi · tasarım paketinin üretim süreci belgesi | Aşama 4 başı | `kalibrasyon/teshis/` altında, çıktılar metin |
| KR-20 | **Mühür sırası ve tarihi** | ~1 Kasım | §11'deki takvim |

Verilmiş ve yürürlükte (hatırlatma): U1 tüm koşu PDR'siyle, ana deney pencere PDR'siyle · taban protokoller yere toplamada sınanır · `kosu_kimligi` düzeltilir · DESPARETE'nin sorunlarını ajan çözer (v0.4, geri alınabilir) · C (komutlar düşer) · belgeler öz, ölçümler kısa.

---

## 10 · Hesap bütçesi (tahmin — iş süreleri kayıtlı U1 koşularından)

**Tek iş süresi, 350 s, karıştırıcısız** (`python arsiv/teshis/belge_guncelleme_2026-09-25/u1_sureler.py`, çıktı yanında): statik 6–20 dk · bağımsız AODV 55 · AOMDV 60 · OLSR 81 dk · formasyon AODV 71 · AOMDV 80 · OLSR 118 dk · görev 67–77 dk · ETX kâhini 28–49 dk. Karıştırıcılı hücrede daha uzun olabilir; **DESPARETE'nin 350 s süresi ölçülmedi** (İ-2 ölçer; v0.3'ün 120 s'lik işi 35–49 dk idi).

| iş | makine süresi (8 işçi) |
|---|---|
| İ-1 regresyon | 35–45 dk |
| İ-2 v0.4 tam ölçek | 3–5 sa |
| İ-3 iyileştirmeler | aday başına 1–3 sa |
| İ-4 DESPARETE U1 + U3 | 5–7 sa |
| İ-7 taban U1 yere toplamada | 5,5–9 sa |
| İ-8 adillik | 5–10 sa |
| İ-13 … İ-17 kalibrasyon ve borçlar | 6–15 sa |
| İ-26 gürültü | 11–17 sa |
| İ-30 doğrulama listesi | 4–6 sa |
| **mühürden önce toplam** | **~45–75 sa** |
| İ-33 ana deney — hücre başına (4 protokol × 40 tohum) | **~30–50 sa** |
| İ-33 Aile 3 — kol başına (40 tohum) | ~10–15 sa |
| İ-34 keşifsel — hücre başına | 40 tohumla ~30–50 sa · 10 tohumla ~8–12 sa |

**Sonuç:** ana deney kaba olarak **birincil hücre (4 protokol) + 2 Aile 1 hücresi (3 taban protokol) + 4 Aile 3 kolu ≈ 115–180 sa ≈ 5–7,5 gün kesintisiz**. 2–15 Kasım penceresine ancak makine gece ve gündüz koşarsa sığar. Çekirdek matrisin (KR-15) ve keşifsel tohum sayısının (KR-16) asıl kısıtı budur. Gürültü ölçümü (İ-26) DESPARETE'yi beklemediği için erkene çekilebilir.

---

## 11 · Takvim (tahmin)

| dönem | işler |
|---|---|
| **26 Eyl – 4 Eki** | KR-1 · KR-2 · KR-3 · KR-4 · İ-1 yapı paketi (anlat → onay → kod → regresyon) · İ-2 v0.4 tam ölçek · İ-7 taban U1 yere toplamada (gece) · İ-8a asimetri · İ-20 bölünme · İ-43 git hijyeni |
| **5 – 11 Eki** | İ-3 iyileştirmeler (İ-2'ye göre) · İ-8b–d adillik → **taban protokoller donar** · İ-9 · İ-18 kaynaklar · İ-13 |
| **12 – 18 Eki** | İ-6 profil dondurma · İ-4 DESPARETE resmi U1 + U3 (gece) · İ-26 gürültü (gece + gün) · İ-5 tasarım paketi · İ-10 |
| **19 – 25 Eki** | İ-27 güç · İ-15 pencere taraması · İ-16 · İ-17 borçlar · İ-21 · İ-22 · İ-23 · İ-29 analiz katmanı |
| **26 Eki – 1 Kas** | İ-28 ön-kayıt metni · İ-30 doğrulama listesi · İ-31 bütçe · İ-42 kanıt depoda · **İ-32 🔒 mühür (~1 Kasım)** |
| **2 – 15 Kas** | İ-33 ana deney · İ-34 keşifsel · İ-24 iz kanalı (paralel) · İ-35 analiz başlar |
| **15 Kas – 19 Ara** | Aşama 5: İ-36 … İ-41 (yazım ~5 hafta, kısaltılmaz) |

Bir dönem kayarsa sonrakinin başı kayar; yazım süresi kısaltılmaz. Aşama 1–2'de kazanılan ~3 hafta Aşama 3'ün ölçümlerine ayrıldı.

## 12 · Kayma planı — öneri (kapsam kararı öğrencinin)

Takvim sıkışırsa düşme sırası: (1) İ-11 açıklama ölçümleri · (2) keşifsel eksenlerin bir kısmı (görev kolu + C5, derinlik, bazı aile ve sınıflar) ya da keşifsel tohum 10'a · (3) İ-24 iz kanalının zengin gösterimi (temel gösterim kalır) · (4) Aile 3 kol sayısı · (5) çekirdek hücre sayısı. **Korunanlar:** birincil hücre, üç taban protokol, DESPARETE, 40 ana deney tohumu, yazım süresi.

## 13 · Gelecek çalışma olarak beyan edilecekler (bu projede yapılmayacak)

Yedekli gönderim (PROTECT'in ikinci kopyası; simülatörde kopyalama + paket kimliği yapısı ister) · hedef alanı emekliliği · komutların yönlendirilmesi (A′: talep yolunda komut alanı · B: ters ağaç, RPL benzeri — yeni döngüsüzlük argümanı ister) · iki geçit · ~2 000 s'lik uzun koşu · protokol farkında (kontrol kanalını hedefleyen) karıştırıcı · hız uyarlaması, RTS/CTS, yayılma kazancı, enerji sezmeli CCA · derin öğrenme · GPSR · gerçek RF/SDR/uçuş testi.
