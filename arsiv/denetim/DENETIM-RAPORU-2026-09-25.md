# Bağımsız Denetim Raporu — İHA mesh yönlendirme projesi ve DESPARETE

> **Tarih:** 24–25 Eylül 2026 · **Denetçi:** yapay zekâ ajanı (Claude), bağımsız
> denetim istemiyle · **Denetlenen hâl:** `main`, son commit `c48fdc2`
> ("little more", 24 Eylül 22:20) + indekste bekleyen iki değişiklik
> (`.gitignore` düzeltmesi, `DENETIM-PROMPT.md` silme) + git dışı yerel
> dosyalar (`DEVIR*.md`, `arsiv/`, `ciktilar2/`, `v2/arsiv/`).
> **Tek yazılan dosya bu rapordur.** Denetim boyunca depoda başka hiçbir
> dosya değişmedi — başta ve sonda 669 dosyanın SHA-1 özetiyle doğrulandı
> (§3.4).

---

## 1 · Özet hüküm

**Projenin sağlığı: altyapı güçlü, DESPARETE'nin son 24 saatlik evrimi zayıf
kanıta dayanıyor ve varsayılan profilde ölçülmemiş bir canlılık kusuru var.**

Simülatör, ölçüm disiplini ve kayıt kültürü bir lise projesi için
olağanüstü: 810 testin 810'u geçti, aynı tohum farklı hash tohumlarında bile
birebir aynı satırı veriyor, taban protokollerin U1 hükmü kayıtlı ölçümden
birebir yeniden üretiliyor, regresyon tabanı `k157` hâlâ geçerli, güç ön
tahmini birebir çıkıyor. Kâhin sızıntısına karşı protokol katmanı bugün
yalnız gözlem katmanını içe aktarıyor. Aşama 4'e geçmeden önce ise aşağıdaki
sorunlar kapanmalı:

1. 🔴 **[Kritik] Resmi U1'i ve ana deneyi koşacak varsayılan profil (v0.3)
   doğrulanmamış.** (a) V5 (ihtiyaca bağlı nitelik), tasarımın edinim
   yolunu fiilen kapatıyor: tam ölçekte (N = 40, 120 s) üç v0.3 koşusunda
   ağdaki 410 FIELD_SOLICIT'ten **1**'i yanıtlandı, 283 DFSN isteğinden
   **17**'si iletildi, geçit **hiç** istek işlemedi, DFSN **hiç** artmadı.
   Birim testler bu yolu isteği gönderen komşuyu elle ACTIVE yaparak sınadığı
   için kusuru göremiyor. (b) Küçük dünyada 300 s'lik koşularda v0.3,
   v0.2'nin **6 / 6** tohum-kolda altında (pencere PDR'si ortalama −0,057,
   en kötü −0,198) — oysa v0.3 40 s'lik kanıtla benimsendi. (c) Nedensel
   kol: tasarımın "gelen PROBE nitelik açar" kuralını geri getirmek istek
   yolunu açıyor ama kaybın yalnız küçük bir kısmını geri getiriyor; kalanın
   sebebi bilinmiyor. (d) **Tam ölçekte, 120 s'lik pencerede, birincil
   hücrenin hareketliliği olan formasyonda v0.3 v0.2'nin 2 / 2 tohumda ~0,05
   (= `Δ_hedef`) gerisinde**; 40 s'lik kanıt ters yönü gösteriyordu. Buna
   karşılık gecikme ve kontrol yükü v0.3'te belirgin düşük — bir ödünleşim
   var, ama öğrencinin karar verdiği kanıt bunu göstermiyordu. **v0.3 ile
   resmi U1 koşulmamalı; profil kararı uzun pencerede yeniden verilmeli.**
2. **[Yüksek] Sonuç satırının `kosu_kimligi` alanı koşuyu tanımlamıyor.**
   Senaryo, trafik deseni, tehdit senaryosu, protokol ve profil kimliğe
   girmiyor; ölçüldü: statik-AODV, bağımsız-OLSR ve formasyon-karıştırıcılı-
   DESPARETE koşuları aynı kimliği taşıyor. Kodun kendi belgesi "aynı kimlik =
   kopya, analiz dışlamak zorunda" diyor → analiz katmanı veri silebilir.
3. **[Yüksek] U1-U'nun "kâhini geçen protokol kabul edilmez" kuralı, projenin
   kendi "ETX kâhini üst sınır değildir" bulgusuyla çelişiyor** (K-110,
   `kalibrasyon/kahin.py`). DESPARETE formasyon kolunda kâhine çok yakın
   (K-162: 0,736 ↔ 0,737; v0.3 oranı 0,95'e kadar) → resmi U1'de yanlış
   "KABUL EDİLMEZ" riski.
4. **[Yüksek] v0.2 → v0.3 kararlarının kanıtı iddiayı taşımıyor.** 40 s × 3
   tohum, yalnız karıştırıcısız kollar, U1'in kendi hücrelerinde; gecikme
   kazancı iki hücre/tek tohumdan genellenmiş; K-165'in V2+ ortalaması kendi
   tablosuyla çelişiyor (metin 0,662 / −0,032; tablodan **0,685 / −0,010**).
   "V5a ve V2+ kararlı durumda zararlı" hükmü V2+ için desteklenmiyor.
5. **[Yüksek] Birincil metrik PDR komut akışlarını da sayıyor**; DESPARETE C
   kararıyla bunları yapısal olarak düşürüyor (~2,5 puan tavan kaybı). Bu,
   ön-kayıtta (`v2/06`) yazılı değil ve `Δ_hedef = 0,05` ile aynı mertebede.
6. **[Yüksek] Taban protokoller birincil trafik deseninde (yere toplama) hiç
   kabul kapısından geçmedi** (U1'leri eşler arası desende); DESPARETE'nin
   profil seçimi ise U1'in kendi 12 hücre/tohumunda yapıldı.
7. **[Yüksek] DESPARETE döneminin (K-153…K-165) bütün kanıt betikleri git
   dışı `arsiv/`de ve hiçbir çıktısı saklanmamış**; ön-kayıttaki güç ön
   tahmininin üreticisi de öyle. Git deposundan bu sayılar üretilemez. Üstelik
   bu betiklerin 10'u profili sabitlemiyor: K-157'nin bir satırı betiğin
   bugünkü hâliyle 0,766 · 0,380 çıktı, o günün profili açıkça verilince
   0,829 · 2,168 birebir (ölçüldü) — kayıtta yazan komut o sayıyı artık
   üretmiyor.
8. **[Orta] AODV/AOMDV'de RREP-ACK ve kara liste "bağlar simetrik" diye
   yok**; oysa karıştırma altında alım başarısı asimetrik (karıştırıcı gücü
   alıcıda eklenir). Birincil hücre karıştırıcılı → taban protokol haksız
   zayıflayabilir; ölçülmedi.
9. **[Orta] Belgelerde çok sayıda bayat sayı ve durum**: kök README
   ("23 Eylül", "DESPARETE buraya yazılacak"), `v2/12` (130 ↔ 133 modül, k151 ↔
   k157, 3.9/3.10 "sırada"), `v2/07` §15'te v0.3 kararı yok, `v2/06`'nın kayıt
   tablosu 10 Eylül'de donmuş…

**En acil eylemler:** (1) v0.3 ile resmi U1'i ertele; V5–DFSN etkileşimini
öğrenci kararıyla düzelt ve ≥ 300 s, ≥ 3 tohumla ölç. (2) `kosu_kimligi`ne
protokol, profil ve tedavi alanlarını ekle (yapı onayı). (3) U1-U'nun kâhin
kuralını sonuç görülmeden yeniden tanımla. (4) Ön-kayda birincil PDR'nin
tanımını (komutlar dâhil mi) ve taban protokollerin yere toplamadaki kabulünü
yaz. (5) DESPARETE kanıt betiklerini ve çıktılarını izlenen bir yere al.

---

## 2 · Anladığım

**Amaç.** TÜBİTAK 2204-A (teslim 19 Aralık 2026) kapsamında bir lise
öğrencisinin tasarım projesi: karıştırma (jamming) altındaki taktik İHA mesh
ağlarında yönlendirme. Üç soru ailesi var: (Aile 1) yaygın protokoller — AODV,
OLSR, AOMDV — yapılı karıştırma altında nasıl ve ne kadar bozuluyor;
(Aile 2) öğrencinin protokolü DESPARETE onlardan daha iyisini yapabiliyor mu;
(Aile 3) kazanç varsa hangi mekanizmadan geliyor. Olumsuz sonuç, iyi teşhis
edilmişse meşru bir sonuçtur; özgünlük protokolden, ikinci katkı taban
protokollerin karıştırma altındaki ölçümünden gelir.

**Yöntem.** Hazır simülatör yerine kendi kesikli-olay simülatörü (`sim2/`):
40 İHA, 1800 m kutu (1:50 ölçek), dört hareketlilik kolu (statik · bağımsız
Gauss-Markov · görev · formasyon + istasyon tutma); log-mesafe yol kaybı
(α = 2), korelasyonlu gölgeleme (σ = 3 dB), Rician sönümleme (K = 6 dB),
dipol anten, parça başına SINR → PER (DQPSK 2 Mb/s), yakalama, 802.11b DCF;
beş karıştırıcı sınıfı ve beş tehdit ailesi; iki trafik deseni (eşler arası
10 × 4 pkt/s; yere toplama 39 × 1 + 4 × 0,25 pkt/s). Protokol yalnız
24 alanlık bir gözlem penceresi görür ve niyet döndürür; her koşuda korunum
defteri kapanır; ısınma ayrı, sayaçların pencere ikizleri pencerede donar;
her parametre yedi kovadan birindedir (bugün 169 parametre, 40'ı SINANMAMIŞ).
Ön-kayıt taslağı: 40 ana deney tohumu (2000–2039, mühürden önce hiçbir kolda
koşulmaz), eşleştirilmiş çift yönlü Wilcoxon, Aile 2'de Holm (m = 3), eşik
`δ = 2·SD_ref/√40` (taban protokol çiftlerinin en gürültülüsü, 20 geliştirme
tohumu), güç `MDE₈₀ ≈ 1,7·δ`, `Δ_hedef = 0,05`, aday birincil hücre
**formasyon · yere toplama · hava_eslik · sürekli · PDR (pencere)**.

**Bugünkü durum.** Aşama 1 (simülatör) ve Aşama 2 (AODV-e · OLSR-b · AOMDV-a;
üçü de U1'i eşler arası desende geçti) bitti. Aşama 3 sürüyor: DESPARETE
3.1–3.7 yazıldı; 3.8 kabul kapısında v0.1 tam ölçekte çöktü (komut hedefleri
için isteğe bağlı alanlar → öğrenci C'yi seçti: yalnız geçit alanı, komutlar
düşer); C ile hareketli kollar da çöktüğü için v0.2 "yalın profil" (boşta
sondalama, onarım edinimi, ilan koruması kapalı); ardından v0.3 = v0.2 + V1
(PROBE yanıtı yalnız istenirse) + V5 (ihtiyaca bağlı nitelik) + V7 (nitelik
sonrası ölçüm PROBE'u) varsayılan oldu; V5a ve V2+ denendi, benimsenmedi.
Resmi U1 (5–7 sa) öğrencinin iznini bekliyor. Önde: gürültü ölçümü, mühür,
ana deney, henüz yazılmamış analiz katmanı ve rapor.

**DESPARETE.** Hedef-yönlü, yönlü bağ maliyetli bir uzaklık-vektörü
protokolü. Her hedef (simülasyonda yalnız geçit) bir "alan" üretir;
düğümler ACTIVE komşularının ilanlarından en ucuz *uygulanabilir* ardılı
seçer. Döngüsüzlük TTL'ye değil Babel ailesinin koşuluna dayanır: aynı
hedef sıra numarasında (DFSN) yalnız potansiyeli düğümün uygulanabilirlik
mesafesinden (FD) KESİN küçük olan ilan kabul edilir; FD aynı turda artamaz;
yalnız hedef, yalnız "uygulanabilirlik açlığı" isteğiyle turu bir artırır.
Bağ maliyeti M0.1: `C = 16 + C_kalite(Q) + C_risk(R)`, Q son 2 s'deki en çok
16 unicast sonucundan (tekrar sayısıyla ağırlıklı), R = max(kötüleşme H,
belirsizlik U). Komşu yaşamı UNQUALIFIED → ACTIVE → STALE/SUSPECT → EXPIRED;
ACTIVE için iki yönlü kanıt (MAC onayı ya da eşleşen PROBE_REPLY) gerekir.
Postürler STEADY/CAUTION/PROTECT; PROTECT yedeklilik ister ve ilk gerçeklemede
yedeklilik ve güvenlik profili kapalı. Edinim/onarım: FIELD_SOLICIT → iki
dalgalı DFSN_REQUEST; REPAIRING en çok 6 s ve alan başına 6 paketlik onarım
tamponu. Tasarım paketi (v0.1, 39 belge + dizin) öğrencinin 20 Eylül tarihli
v0 taslağından türeyen, "proje sahibi onayladı" kayıtlarıyla ilerlemiş bir
şartname.

---

## 3 · Yöntem

### 3.1 · Okunanlar

- Kök `README.md`; `v2/01`, `03`, `05`, `06`, `12`, `README` tam; `v2/04`
  dizini ve K-150…K-165 tam, K-090, K-110, K-136/137 ilgili bölümler;
  `v2/07` §00–§05.3, §09–§18 başları, §15, §17; `v2/02`, `08`, `09`, `10`,
  `13` başlıkları ve durum bantları.
- `DEVIR.md`, `DEVIR-PROMPT.md` (yalnız bilgi olarak).
- Tasarım paketi: `36` tam; `00` dizini; `23` §2 (AcceptPacket), §5 (edinim,
  istek, hedefte işleme), §6 başı; `05` karar günlüğünün yapısı ve örnek
  MAJOR kayıtlar; `40`'ın öneri tablosu; v0 taslağının başı.
- Kod: `protokoller/desparete*.py` sekiz dosyanın tamamı; `aodv_bicim.py` ve
  `aomdv.py` başlıkları; `sim2/gozlem/*` (pencere, protokol, içe aktarmalar),
  `sim2/olcum/metrikler.py`, `sim2/kosum/sonuc.py` (kimlik bölümü),
  `sim2/cekirdek/kimlik.py`, `saat.py` başı, `kanal/kanal.py` başı,
  `kanal/girisim.py` (girişim hesabı), `yapilandirma/konfig.py`
  (varsayılanlar), `kokenler.py` (seçili kayıtlar), `senaryolar.py`
  (bölünme tablosu); `kalibrasyon/aodv_uygunluk.py` tam,
  `regresyon_satirlari.py` vaka matrisi, `kahin.py` (ETX kâhini),
  `dugum_sayisi.py` (ana deney tohumu bölümü), `mimari_denetimi.py`
  (içe aktarma), `arsiv/dogrulama/kayit_indeksi.py` (yazma yolu).
- Testler: `test_desparete.py`'nin simülatör, U1–U4, hedefte tur artırma ve
  v0.3 testleri; `test_kosum.py`'nin içe aktarma grafiği ve kimlik testleri;
  bütün test dosyalarında tautolojik iddia taraması.
- `arsiv/teshis/desparete_*` ve `guc_on_tahmin_*` betiklerinin tamamı.
- Git: `log --stat`, `show`, `diff --cached`, `ls-files`, `ls-files --eol`,
  `status` — hepsi `GIT_OPTIONAL_LOCKS=0` ile, salt-okur.

⚠️ **Çalışma anlaşmasıyla çelişki (bilgi):** `v2/03` §1 ve ajan hafızası
"git komutlarını — salt-okur olanlar dâhil — yalnız öğrenci çalıştırır"
diyor. Denetim istemi (§0.4) salt-okur ve kilitsiz git'e açıkça izin
verdiği için istem esas alındı; hiçbir durum değiştiren git komutu koşulmadı
ve `.git/index`'in özeti değişmedi (§3.4).

### 3.2 · Koşulanlar

Bütün Python çağrıları `PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1`
ile; denetimin kendi betikleri ve çıktıları proje DIŞINDA (oturumun geçici
dizininde), depo yalnız `sys.path` üzerinden içe aktarıldı.

| # | komut | süre | sonuç |
|---|---|---|---|
| 1 | `python -m pytest tests2 -q -p no:cacheprovider --durations=25` | **1 264,6 s** (makine eşzamanlı 6–12 simülasyon süreciyle paylaşımlı) | **`810 passed`**, çıkış 0 — beklenen sayıyla birebir |
| 2 | `python kalibrasyon/mimari_denetimi.py` | 9,8 s | `Yapisal ihlal YOK` · **133** modül · **169** parametre: TÜRETİLMİŞ 52 · ÖLÇÜLMÜŞ 19 · KAYNAK 7 · DUYARSIZ 16 · TEDAVİ 24 · KOL TANIMI 11 · **SINANMAMIŞ 40** · duyarlılık borcu 9 · D16 0 · DUYARSIZ \|Δ\| 13/13 · 11 not |
| 3 | `python arsiv/dogrulama/kayit_indeksi.py --kontrol` | 0,2 s | `✅ indeks güncel — 76 kayıt`, çıkış 0 |
| 4 | `python -u kalibrasyon/aodv_uygunluk.py hukum ciktilar2/aodv_uygunluk/{aodv,olsr,aomdv}_son.json` | saniyeler | 36 hücrenin oranları ve hükümler `DEVIR.md` §2 madde 19 ile **birebir** (AODV 2, AOMDV 1 açıklanmış düşük; OLSR 0) |
| 5 | `python -u kalibrasyon/regresyon_satirlari.py karsilastir k151 k157` | 2,4 s | bulgusuz 45/45 · `🟢 BIREBIR` · çıkış 0. `k157`'den sonra `sim2/`de değişen dosya yok (dosya zamanları) → taban geçerli |
| 6 | `python arsiv/teshis/guc_on_tahmin_2026-09-23/guc.py` | 11,8 s | 0,306 · 0,608 · 0,724 · 0,806 · 0,848 — `v2/06` §0.4.3 ve K-153 ile **birebir** |
| 7 | `belirlenimcilik.py` + `fark.py` (denetçinin) — küçük dünya, `bagimsiz-surekli`, 20 s, AODV ve DESPARETE, `PYTHONHASHSEED` 0 · 1 · 98765 | ~1 dk | PDR ve kontrol çerçevesi altı koşuda birebir; AODV satırında iki koşu arasındaki TEK farklar `calisma_kimligi`, `zaman_damgasi_utc` ve (farklı hash tohumunda) `ortam.hashseed` |
| 8 | `kimlik_carpisma.py` (denetçinin) | ~5 s | üç farklı koşu → aynı `kosu_kimligi` (bulgu Y-1) |
| 9 | `k165_aritmetik.py` (denetçinin) — K-163/164/165 tablolarından | < 1 s | bulgu Y-4'ün sayıları |
| 10 | `sink_dfsn.py` (denetçinin) — küçük dünya (14 düğüm), yere toplama, C, v0.2 ↔ v0.3, 300 s, bağımsız ve formasyon × 3 tohum (görev ve statik kolları CPU için durduruldu) | iş başına 4,6–19 dk (6 işçi, paylaşımlı) | bulgu K-1 |
| 10b | `k157_yeniden.py` (denetçinin) — K-157 §6'nın bir satırı, iki profille | 67 s | bulgu Y-6: o günün profiliyle **0,829 · 2,168 birebir**; betiğin bugünkü hâliyle 0,766 · 0,380 |
| 11 | `sink_dfsn_neden.py` (denetçinin) — küçük dünya, v0.3 ↔ v0.3 + "gelen PROBE nitelik açar", 300 s, 2 kol × 3 tohum | iş başına 5,7–12,1 dk (4 işçi, paylaşımlı) | bulgu K-1'in nedensel kolu |
| 12 | `tam_olcek_dfsn.py` (denetçinin) — TAM ÖLÇEK N = 40, 120 s, v0.2 ↔ v0.3, formasyon × 2 tohum + bağımsız × 1 tohum | duvar **4 588 s** (6 işçi); iş başına v0.3 35–49 dk, v0.2 60–76 dk | bulgu K-1 tam ölçekte |

Denetçinin betikleri ve ham çıktıları proje dışında kaldı; hepsi yalnız
depodaki kodu içe aktarıp çağırıyor, kaynak DEĞİŞTİRMİYOR (nedensel kol
bir alt sınıfla tek bir yöntemi geçersiz kılıyor). Gerekirse öğrenciye
verilebilir.

### 3.3 · Neye bakılamadı

- Resmi U1 (5–7 sa), `uretici_duman.py` (30–45 dk), doğrulama listesinin uzun
  maddeleri ve regresyon üretimi (`uret` diske yazar) — koşulmadı.
- K-160…K-165'in tam ölçekli kısa koşularının yeniden üretimi (her biri
  20–60 dk; 8 çekirdek) — yalnız aritmetiği ve betikleri denetlendi.
- Taban protokollerin RFC'ye satır satır sadakati — başlıklardaki beyanlar ve
  U1 kayıtları okundu, kod satır satır denetlenmedi.
- `v2/02`'deki literatür künyeleri, tasarım paketinin 39 belgesinin çoğu
  (başlık düzeyinde), `arsiv/`in DESPARETE dışı kısmı.

### 3.4 · Depoya dokunulmadığının kanıtı

Başta ve sonda `.git` dışındaki bütün dosyaların SHA-1 listesi alındı
(669 dosya) ve `.git/index`'in SHA-1'i kaydedildi. **Rapor yazılmadan hemen
önce 669 / 669 dosya birebir aynıydı** (yeni `__pycache__` ya da önbellek
dosyası yok) ve `.git/index` özeti değişmedi (`8d0cd7cc…`); `git status`
başlangıçtakiyle aynı (`M .gitignore`, `D DENETIM-PROMPT.md` — ikisi de
denetimden önce indekste bekliyordu). Tek yeni dosya bu rapordur.

---

## 4 · Bulgular

### 4.1 · Tablo

| kimlik | alan | önem | kısa | doğrulandı mı |
|---|---|---|---|---|
| K-1 | DESPARETE | **Kritik** | varsayılan v0.3 doğrulanmamış: V5 edinim/DFSN yolunu kapatıyor; uzun pencerede birincil kolda v0.2'nin ~0,05 gerisinde | kod + ölçüm (tam ölçek 120 s ve küçük dünya 300 s; nedensel kol) |
| Y-1 | yeniden üretilebilirlik · kod | Yüksek | `kosu_kimligi` senaryo/desen/tehdit/protokol/profil ayırt etmiyor | ölçüldü |
| Y-2 | yöntem | Yüksek | U1-U "kâhini geçmek = sızıntı" kuralı "kâhin tavan değil" bulgusuyla çelişiyor | kod + kayıt |
| Y-3 | yöntem · taban protokoller | Yüksek | taban protokollerin birincil desende kabulü yok; DESPARETE profili U1 hücrelerinde seçildi | kayıt + kod |
| Y-4 | DESPARETE · kayıtlar | Yüksek | v0.3 kararlarının kanıtı zayıf; K-165'te aritmetik çelişki; aşırı genelleme | aritmetik doğrulandı |
| Y-5 | yöntem | Yüksek | birincil PDR komutları sayıyor; DESPARETE'de ~%2,5 yapısal kayıp ön-kayıtta yok | kod + kayıt |
| Y-6 | yeniden üretilebilirlik | Yüksek | DESPARETE kanıt betikleri git dışı, çıktılar saklanmamış | doğrulandı |
| O-1 | taban protokoller | Orta | RREP-ACK/kara liste yokluğunun gerekçesi (simetrik bağ) karıştırma altında geçersiz | kod; etkisi ölçülmedi |
| O-2 | ölçüm · yöntem | Orta | U1 tüm-koşu PDR'si kullanıyor; ön-kayıt pencere PDR'si | kod |
| O-3 | testler | Orta | sahte ön koşullu birim testler K-1'i maskeliyor; uçtan uca DFSN testi yok; tautolojik iddialar | kod |
| O-4 | yeniden üretilebilirlik | Orta | regresyon matrisinde gerçek protokol yok | kod |
| O-5 | kayıtlar | Orta | bayat ve çelişkili belgeler | doğrulandı |
| O-6 | yöntem | Orta | "ölçmeden önce" sırası VCS ile doğrulanamıyor | doğrulandı (yokluk) |
| O-7 | DESPARETE · iddia | Orta | README'nin "temel fikirleri" ile değerlendirilen profil arasında fark | kod + kayıt |
| O-8 | simülatör · taban | Orta | SINANMAMIŞ tampon (64 · 30 s) AODV'de bağlıyor; MAC tekrar sınırı 4 (802.11 kısa sınır 7) | kayıt |
| O-9 | yöntem | Orta | "üstün" hükmünün mekanizma kapısı tanımsız; güç analizi iki koşulu dışarıda bırakıyor | kayıt |
| O-10 | risk · fikir sahipliği | Orta | v0.3'te ajan kaynaklı mekanizmalar; tasarım paketinin üretim süreci belgesiz; `v2/07` §15 eksik | kayıt |
| O-11 | risk | Orta | hesap bütçesi ve takvim | tahmin |
| D-1 | simülatör | Düşük | içe aktarma grafiği testi yalnız açık `sim2.X` içe aktarmalarını yakalıyor | kod; bugün ihlal yok (doğrulandı) |
| D-2 | kod · depo | Düşük | 154 `.pyc` izleniyor; `DENETIM-PROMPT.md` geçmişe girdi | doğrulandı |
| D-3 | kod · depo | Düşük | satır sonları; `.gitattributes` yok | doğrulandı |
| D-4 | kod | Düşük | C gereği düşen komutlar `hedef_yok` sebebine karışıyor | kod |
| D-5 | kod | Düşük | köken defteri `protokoller/` sabitlerini kapsamıyor | kod |
| D-6 | kod | Düşük | küçük belge–kod uyumsuzlukları (`YerelZaman`, docstring'ler) | kod |
| D-7 | simülatör | Düşük | `v2/07` §17'de açık A6 · A8 · A23; varsayılan desen hâlâ eşler arası | kod |
| B-1 | yöntem | Bilgi | ana deney tohumları dünya/grafik kurmak için kullanıldı (beyanlı) | kod |
| B-2 | yöntem | Bilgi (olumlu) | U1 eşiğinin sonradan seçildiği doğru beyan edilmiş | kayıt |
| B-3 | DESPARETE | Bilgi (olumlu, kısmen) | güvenlik değişmezleri kodda ve testte korunuyor; resmi koşularda denetim yok | kod |


### 4.2 · Ayrıntı

#### K-1 · 🔴 Kritik · DESPARETE — varsayılan v0.3 doğrulanmamış: V5 edinim yolunu kapatıyor, uzun koşuda v0.2'nin gerisinde

**Kanıt — kod.**
- V5 açıkken bir komşu yalnız o komşudan gelen, bizim için
  *uygulanabilir* bir FIELD_UPDATE ile nitelendirilir; PROBE dâhil hiçbir
  başka çerçeve nitelik açmaz (`protokoller/desparete.py:516-521`,
  `_nitelige_deger` `:556-571`). Geçidin kendi alanı olduğu için
  (`a.kendi → False`, `:566-567`) geçit **hiç kimseyi** nitelendirmez — bu,
  bir testle bile sabitlenmiş (`tests2/test_desparete.py:1615-1625`,
  `aday_acilan == 0`).
- FIELD_SOLICIT'e yanıt (`desparete.py:643-646`) ve DFSN_REQUEST'in kabulü
  (`:655-659`) gönderenin ACTIVE olmasını ister. İstekler hedefe doğru
  "yukarı" gider; ama V5 altında bir röle yalnız KENDİSİNE uygulanabilir ilan
  yapan (yani daha yukarıdaki) komşuları nitelendirir — aşağıdan gelen
  isteğin göndereni ACTIVE değildir. Geçitte ise hiçbir istek kabul
  kapısından geçemez → `_hedefte` (`:685-708`) hiç çalışmaz → hedef turu
  (DFSN) hiç artmaz.
- FD yalnız daha yeni bir DFSN ile sıfırlanır (`desparete_alan.py:261-265`);
  aynı turda yalnız küçülebilir (`:273-274`). DFSN artmazsa hareketli ağda
  düğümlerin FD'si zamanla "en iyi günlerindeki" potansiyele kilitlenir ve
  uygulanabilirlik açlığı (tasarımın `FEASIBLE_STARVATION`'ı) çözülemez; tek
  kaçış, tesadüfen daha yakın bir komşunun belirmesidir.
- Tasarım bu yolu açık tutuyordu: `23` §6 `ReceiveProbe → EnsureUnqualifiedPeer`
  (gelen PROBE nitelik sürecini açar, `23_…ALGORITHMS.md:398-401`). V5 bunu
  kaldırıyor. K-163 V5'i "başka çerçeve nitelik açmaz" diye kayda geçirmiş,
  ama edinim ve istek kapılarına etkisi hiç sorulmamış/ölçülmemiş —
  **kayda geçmiş ama sonucu ölçülmemiş bir tasarım sapması.**
- Birim testler isteği gönderen komşuyu önce elle ACTIVE yapıyor
  (`test_desparete.py:951`, `:981` `komsular.kanit(2, …)`, `:1000`, `:1008`);
  bu yüzden entegrasyondaki ön koşul (gönderen gerçekten ACTIVE mi) hiç
  sınanmıyor — `03` §B6'nın "sahte host ölçüleni yutar" sınıfı. Uçtan uca
  "açlık → istek → hedefte tur artışı" testi yok.

**Kanıt — ölçüm 1: TAM ÖLÇEK** (denetçinin `tam_olcek_dfsn.py`; N = 40,
yere toplama, C, U1'in kolları ve tohumları; 120 s — ısınma 10 · ölçüm
10–110 · boşalma 10 — yani K-163'ün 40 s'lik penceresinin 4 katı; v0.2 =
`SECENEK_YOK`, v0.3 = varsayılan; duvar 4 588 s, 6 işçi):

| kol · tohum | pencere PDR v0.2 → v0.3 | gecikme p95 (pencere) v0.2 → v0.3 | kontrol / veri kanal süresi | geçitte işlenen istek · DFSN artışı v0.2 / v0.3 | ağda solicit gönderilen → yanıtlanan (v0.3) | ağda istek gönderilen → iletilen (v0.3) | ulaşılamaz bölüm v0.2 / v0.3 |
|---|---|---|---|---|---|---|---|
| **formasyon · 1000** | 0,748 → **0,699 (−0,050)** | 1,61 → 0,76 s | 1,44 → 0,63 | 43 · 6 / **0 · 0** | 143 → **1** | 98 → 14 | 17 / **41** |
| **formasyon · 1001** | 0,777 → **0,719 (−0,058)** | 2,27 → 1,03 s | 1,48 → 0,62 | 31 · 3 / **0 · 0** | 135 → **0** | 92 → 3 | 15 / **49** |
| bağımsız · 1000 | 0,609 → 0,661 (+0,052) | 3,91 → 1,08 s | 1,28 → 0,58 | 24 · 6 / **0 · 0** | 132 → **0** | 93 → **0** | 28 / **50** |

- **Mekanizma, tam ölçekte:** v0.3'ün üç koşusunda ağdaki 410 solicit'ten
  **1**'i yanıtlandı, 283 istekten **17**'si iletildi (v0.2'de 116 istek
  gönderildi, röleler 3 785 kez iletti); geçit hiç istek işlemedi, DFSN
  hiç artmadı; ulaşılamaz bölüm 2,5–3 kat.
- **Başarım, tam ölçekte:** birincil hücrenin hareketliliği olan
  **formasyonda v0.3, v0.2'nin 2 / 2 tohumda ~0,05 gerisinde** — tam
  `Δ_hedef` kadar. Aynı tohumlarda 40 s'lik pencerede (K-163 §4) v0.3 önde
  ya da eşitti (+0,037 · −0,005; tüm-koşu PDR'si). v0.3'ün zaman dilimli
  teslimi formasyonda ilk 20 s'den sonra düşüyor (1000: 0,79 → 0,62–0,68), v0.2'ninki düz kalıyor
  (0,72–0,80). Bağımsız kolda ise v0.3 önde (+0,052). Gecikme ve kontrol
  yükünde v0.3 her üç koşuda açıkça iyi — gerçek bir ödünleşim var.
- Sınır: 120 s (350 s değil), 3 koşu; kol başına 1–2 tohum.

**Kanıt — ölçüm 2: küçük dünya, 300 s** (`sink_dfsn.py`; 14 düğüm, yere
toplama, C; ısınma 60 s, ölçüm 60–240 s; tohum 1000–1002).

| kol · tohum | pencere PDR v0.2 → v0.3 | geçidin nitelendirdiği aday v0.2 / v0.3 | hedefte işlenen istek v0.2 / v0.3 | DFSN artışı v0.2 / v0.3 | ağda ACTIVE-dışı diye reddedilen istek v0.2 / v0.3 | ulaşılamaz bölüm v0.2 / v0.3 |
|---|---|---|---|---|---|---|
| bağımsız · 1000 | 0,821 → **0,624** (−0,198) | 379 / **0** | 9 / **0** | 6 / **0** | 174 / 338 | 24 / 48 |
| bağımsız · 1001 | 0,840 → 0,776 (−0,064) | 365 / **0** | 4 / **0** | 3 / **0** | 143 / 241 | 17 / 24 |
| bağımsız · 1002 | 0,851 → 0,832 (−0,019) | 383 / **0** | 0 / 0 | 0 / 0 | 0 / 91 | 6 / 13 |
| formasyon · 1000 | 0,763 → 0,728 (−0,035) | 364 / **0** | 7 / **0** | 4 / **0** | 203 / 223 | 23 / 42 |
| formasyon · 1001 | 0,838 → 0,832 (−0,006) | 282 / **0** | 0 / 0 | 0 / 0 | 0 / 155 | 11 / 15 |
| formasyon · 1002 | 0,860 → 0,840 (−0,019) | 385 / **0** | 0 / 0 | 0 / 0 | 0 / 110 | 9 / 13 |

- 6 / 6 koşuda v0.3'ün pencere PDR'si v0.2'nin altında (ortalama bağımsız
  −0,094, formasyon −0,020). v0.3'te geçit 6 / 6 koşuda hiç aday açmadı, hiç
  istek işlemedi, turu hiç artırmadı; v0.2'de bu, DFSN'ye ihtiyaç duyulan
  üç koşuda 3–6 artışla çözülüyordu. v0.3'te ulaşılamaz bölüm sayısı her
  koşuda arttı ve gönderilen isteklerin hiçbiri hedefe ulaşmadı.
- v0.3'ün kaybı, yeniden edinimin çok olduğu koşularda büyük (bağımsız 1000:
  48 ulaşılamaz bölüm, 90 istek, −0,198) — kayıp, istek yolunun ölü olduğu
  yerde toplanıyor.

**Kanıt — ölçüm 3: nedensel kol** (`sink_dfsn_neden.py`; küçük dünya, aynı
tohumlar, 300 s; v0.3 ile, TEK fark "gelen PROBE nitelik açar" kuralı — `23` §6; kaynak
değiştirilmedi, bir alt sınıfla):

| kol · tohum | pencere PDR v0.3 → v0.3 + kural | geçitte işlenen istek | DFSN artışı | yanıtlanan solicit | PROBE (nitelik) | kontrol / veri kanal süresi |
|---|---|---|---|---|---|---|
| bağımsız · 1000 | 0,624 → 0,685 (+0,061) | 0 → 9 | 0 → 1 | 0 → 13 | 1 043 → 2 623 | 0,60 → 0,84 |
| bağımsız · 1001 | 0,776 → 0,794 (+0,018) | 0 → 7 | 0 → 0 | 0 → 22 | 1 146 → 2 438 | 0,62 → 0,85 |
| bağımsız · 1002 | 0,832 → 0,829 (−0,002) | 0 → 6 | 0 → 2 | 0 → 15 | 1 129 → 2 623 | 0,66 → 0,91 |
| formasyon · 1000 | 0,728 → 0,715 (−0,013) | 0 → 7 | 0 → 0 | 0 → 12 | 1 140 → 2 346 | 0,60 → 0,78 |
| formasyon · 1001 | 0,832 → 0,821 (−0,011) | 0 → 4 | 0 → 0 | 0 → 23 | 1 422 → 2 772 | 0,63 → 0,83 |
| formasyon · 1002 | 0,841 → 0,859 (+0,018) | 0 → 3 | 0 → 0 | 0 → 11 | 1 104 → 2 592 | 0,66 → 0,89 |

Kural geri gelince istek ve solicit yolu **yeniden işliyor** (6 / 6
koşuda), yani yol tıkanıklığının sebebi V5'in PROBE'la nitelik açmayı
kaldırması — **nedensel olarak doğrulandı**. Ama teslime etkisi küçük ve
karışık (ortalama +0,012; 3 / 6 artış) ve bedeli PROBE'ların ~2,2 katı.
Sonuç: **v0.3'ün 300 s'deki kaybının (v0.2'ye göre ortalama −0,057) yalnız
küçük bir kısmı bu yoldan**; kalanın sebebi ölçülmedi (adaylar: V5'in daha
az komşu → daha az uygulanabilir yedek bırakması; V1/V7'nin ölçüm
dinamiği). v0.3, v0.2'ye tam ölçek 40 s'de önde (K-163); küçük dünya
300 s'de 6 / 6, tam ölçek 120 s formasyonda 2 / 2 geride.
Nedensel koldaki v0.3 koşuları `sink_dfsn.py`nin v0.3 koşularıyla BİREBİR
(ör. bağımsız 1000: 0,6237 iki ayrı çalıştırmada) — belirlenimcilik bir
kez daha doğrulandı.

**Sınır:** 350 s'lik tam pencere hiç ölçülmedi; tam ölçekte 3, küçük dünyada
6 + 6 koşu; kol başına en çok 3 tohum.

**Etki.** v0.3 varsayılandır ve resmi U1 onunla koşacak
(`aodv_uygunluk.py:153-154`). (1) Tasarımın açlık çözme ve edinim
mekanizmaları bu profilde fiilen yok; Aile 3'te "onarım edinimi / yeniden
edinim" gibi kolların ablasyonu v0.3'te anlamsızlaşır ve DESPARETE'nin DFSN
tabanlı canlılık iddiası ölçülen protokolde sınanmamış olur. (2) Profil
seçimi 40 s'lik pencereye dayanıyor; 120 s'de birincil kolda sıralama
tersine dönüyor ve fark `Δ_hedef` mertebesinde. 5–7 saatlik resmi U1 ve ana
deney bu hâliyle koşulursa ölçülen, öğrencinin bilerek seçmediği bir
ödünleşimin (daha az yük ve gecikme ↔ formasyonda daha düşük teslim) bir
tarafı olur.

**Öneri.** (Öğrenci kararı; tasarım değişikliği.) Seçenekler ve ölçüm §5
Ö-1 ve Ö-2'de. Önce uçtan uca bir kapı: "geçit en az bir açlık isteği
işledi ve tur arttı", "ağda ACTIVE-dışı diye reddedilen istek oranı" ve
"yanıtlanan solicit oranı" raporlanır; birim testlerin ACTIVE ön koşulunu
elle kuran varyantlarının yanına ön koşulu KENDİSİ kuran bir simülatör
testi eklenir. Profil kararı (v0.2 · v0.3 · v0.3 + tasarım kuralı · V1 + V7)
tam ölçekte, ≥ 120 s (tercihen 350 s) ve ≥ 3 tohumla, birincil hücrenin
karıştırıcılı koşulu dâhil yeniden verilir.

**Doğrulandı mı:** mekanizma kodda, tam ölçekte (3 koşu) ve küçük dünyada
(12 koşu) ölçüldü ve nedensel kolla doğrulandı; başarım farkının 350 s ve
çok tohumdaki büyüklüğü doğrulanmadı.

---

#### Y-1 · Yüksek · yeniden üretilebilirlik — `kosu_kimligi` koşuyu tanımlamıyor

**Kanıt.** `sim2/kosum/sonuc.py:80-81`: `TEDAVI_ALANLARI = ("kol",
"senaryo", "tohum", "not_", "trafik_deseni", "tehdit_senaryosu")` kurulum
özetinden çıkarılıyor; `kosu_kimligi` (`sim2/cekirdek/kimlik.py:144-157`)
yalnız araç özeti (`sim2/` kodu — `protokoller/` DEĞİL, `kimlik.py:54-73`),
bu kurulum özeti, `kol`, `tohum`, sayaç ve akış şeması özetinden türüyor.
Senaryo, trafik deseni, tehdit senaryosu, protokol adı, protokol kodu ve
profil (bayraklar/seçenekler) kimliğe girmiyor.
**Ölçüldü** (`kimlik_carpisma.py`): `kol="u1"`, tohum 1000 ile
(statik-yok · eşler arası · AODV), (bagimsiz-yok · eşler arası · OLSR) ve
(formasyon-surekli · yere toplama · DESPARETE) → üçü de
`kosu_kimligi = a5396b0939c2e01134e28008`. Kodun kendi belgesi:
*"İki sonuç satırı aynı kimliği taşıyorsa … biri kopyadır ve analiz onu
dışlamak zorundadır"* (`kimlik.py:147-150`). K-159 yalnız "protokol
parametresi" boşluğunu görmüştü; boşluk daha geniş. Testler yalnız `kol` ve
`tohum`un ayırt ettiğini sınıyor (`tests2/test_cekirdek.py:570-577`,
`tests2/test_kosum.py:506-521`).
**Etki.** U1 aleti bütün koşularına aynı `kol`u veriyor; ana deneyde bir
kol etiketi unutulursa ya da analiz katmanı belgedeki kuralı uygularsa farklı
koşular "kopya" sayılıp sessizce silinir; ya da tersine, kimlik bir satırın
hangi DESPARETE sürümüne ait olduğunu kanıtlamaz (v0.2 ↔ v0.3 aynı kimlik).
**Öneri.** (`sim2/` yapı değişikliği → yapı onayı + regresyon.) Kimliğe
tedavi alanlarının hepsini, protokol adını, `protokoller/` kod özetini ve
protokolün parametre özetini (DESPARETE'de bayraklar + seçenekler + kota +
komut_alanlari) ekle; ya da `kurulum_hash` ile ayrı bir `tedavi_hash` ve
`protokol_hash` alanı yaz ve analiz katmanının kopya ölçütünü bunlara bağla.
Kapı: farklı senaryo/protokol/profil → farklı kimlik testi.
**Doğrulandı mı:** evet (ölçüldü).

---

#### Y-2 · Yüksek · yöntem — U1-U'nun "kâhini geçmek = sızıntı" kuralı kendi bulgusuyla çelişiyor

**Kanıt.** `v2/06:384` ve `kalibrasyon/aodv_uygunluk.py:491-501`: oran > 1
ise "kâhin bilgisi sızmış olabilir" ve **U1-U KALDI → protokol kabul
edilmez** ("gevşetilemez"). Öte yandan `kalibrasyon/kahin.py:420-429` ve
`v2/04` K-110 (`:2398-2409`), `v2/03` §B3 (`:133`), `v2/07` §07.1 (`:414`):
ETX kâhini **üst sınır değildir**; sonlu yeniden deneme sınırı yüzünden bir
protokolün onu geçmesi *"kusur işareti DEĞİLDİR"*; atlama kâhini bazı
tohumlarda onu zaten geçiyor. DESPARETE kalite duyarlı bir yönlendirici ve
formasyon kolunda kâhine çok yakın: K-162 §3 (30 s, tek tohum) 0,736 ↔
0,737; K-163 §4 (40 s) v0.3 oranı 0,911–0,951.
**Etki.** Resmi U1'de (tam pencere, 350 s) formasyon ya da başka bir kolda
oran 1'i geçerse DESPARETE, sızıntı olmadan, "gevşetilemez" bir kapıdan
kalır; ya da sonuç görüldükten sonra kural değiştirilmek zorunda kalınır —
tam da projenin kaçındığı şey.
**Öneri.** Resmi U1'den ÖNCE ve öğrenci kararıyla: kâhin aşımını bir
sızıntı *kanıtı* değil bir *teşhis tetikleyicisi* yap (aşan hücrede sızıntı
denetimi — içe aktarma, gözlem yüzeyi, yük içerikleri — ve kâhinin kayıp
sebepleri ölçülür); ya da gerçek bir üst referans (`ust_referans.py`'nin
teslim olasılığı kâhini / kâhin zarfı) kullan. Karar `06` §4.4'e ve kayıt
tablosuna (§10) yazılır.
**Doğrulandı mı:** çelişki belgede ve kodda doğrulandı; aşım olasılığı
tahmindir.

---

#### Y-3 · Yüksek · yöntem · taban protokoller — birincil desende taban protokollerin kabulü yok; DESPARETE profili U1 hücrelerinde seçildi

**Kanıt.** Taban protokollerin U1'i eşler arası desende
(`aodv_uygunluk.py:140-146`: yalnız DESPARETE yere toplamada); birincil hücre
yere toplama (`v2/06` §0.4.4). Taban protokollerin yere toplamada (39 kaynak
→ tek geçit; geçit çevresinde tıkanıklık, aynı hedefe yönelik keşif
fırtınası; AODV'de karşılıksız RREP yok) hiçbir kabul ölçümü yok (C3/K-126
yalnız kâhinle koştu). DESPARETE'nin v0.2/v0.3 seçimleri (K-161 §6,
K-163…K-165) U1'in kendi 12 hücresi ve tohumlarında (1000–1002, dört `-yok`
kolu) yapıldı; resmi U1 de aynı hücrelerde koşacak. Tam ölçekte hiçbir
v0.2/v0.3 ölçümü karıştırıcılı bir kolda yapılmadı (karıştırıcılı tek kanıt
K-163 §2'nin küçük dünya, 30 s, tek tohum tablosu).
**Etki.** (a) Birincil karşılaştırmada bir taban protokolün yere toplamaya
özgü bir gerçekleme kusuru (straw-man) görünmeden kalabilir; (b) DESPARETE'nin
U1'i kendi ayar hücrelerinde iyimser olur ("kapıya ayar"); (c) iki U1 tablosu
farklı desenlerde olduğundan karşılaştırılamaz (K-161 §7 bunu doğru beyan
ediyor).
**Öneri.** Mühürden önce: taban protokollerin U1-B'sini (ya da en azından
U1-U + kısa pencere oranlarını) yere toplamada da koş; DESPARETE'nin
ayarlamasını U1 tohumlarından AYRI geliştirme tohumlarında yap (ör.
1003–1007) ya da resmi U1'i ayrıca ayar görmemiş tohumlarda tekrarla; v0.x
seçimini birincil hücrenin karıştırıcılı koşulunda da ölç.
**Doğrulandı mı:** kayıt ve kodla doğrulandı; etki ölçülmedi.

---

#### Y-4 · Yüksek · DESPARETE · kayıtlar — v0.3 kararlarının kanıtı iddiayı taşımıyor

**Kanıt.**
- K-163 §4, K-164 §4, K-165 §3: tam ölçek, **40 s** (ölçüm 25 s), 3 tohum,
  yalnız karıştırıcısız kollar. K-165 §4'ün kendisi bu düzeyde PDR
  farklarını "YÖN işareti, kanıt değil" diye niteliyor.
- **Aritmetik çelişki:** K-165 §3 (D2) *"hareketli ortalama 0,694 → 0,662
  (−0,032)"* (`v2/04:9881`) diyor; aynı kaydın tablosundaki dokuz hücrenin
  ortalaması **0,6846** (fark **−0,0098**). Denetçinin hesabı
  (`k165_aritmetik.py`, tablolar K-163 §4 · K-164 §4 · K-165 §3):

  | karşılaştırma | ortalama fark | eşli SD | SE | t | artan hücre |
  |---|---|---|---|---|---|
  | v0.2 → V1+V5+V7 (v0.3) | +0,0282 | 0,0255 | 0,0085 | +3,3 | 8/9 |
  | v0.3 → +V5a | −0,0211 | 0,0317 | 0,0106 | −2,0 | 2/9 |
  | v0.3 → +V2+ | **−0,0098** | 0,0236 | 0,0079 | −1,2 | 3/9 |

  (Dokuz hücre üç kol × üç tohumdur, bağımsız örneklem değildir; t yalnız
  gösterge.) K-165 §4'ün "~0,016 SE" kaba ölçeği küçük dünyadan (K-158)
  taşınmış; bu tablolar daha küçük bir eşli SE veriyor. Yani 40 s'lik
  pencerede v0.3'ün PDR kazancı kayıtta *hafife*, V2+'nın zararı
  *abartılmış* — ama 120 s'lik pencerede formasyonda sıralama tersine
  dönüyor (K-1).
- `v2/12:213-216` ve `DEVIR.md:232` "hareketli gecikme p95'i 2,5–4 s'den
  0,1–0,8 s'ye" / "5–22× düşük" diyor; eşleşik ölçüm yalnız **iki hücre,
  tek tohum** (K-163 §5: 4,03 → 0,78 · 2,47 → 0,11); ötekiler farklı pencere
  ve tohumlardan (K-162, 30 s). Gecikme yalnız teslim edilenden ve ortak alt
  küme olmadan karşılaştırıldı — `03` §B3'ün "seçilim yanlılığı" kuralı
  uygulanmadı. Statik kolda v0.3'ün tüm-koşu PDR'si 3/3 tohumda düştü
  (K-163 B3 tutmadı).
- `v2/12:216` "V5a ve V2+ … kararlı durumda zararlı" — V2+ için bu tablolar
  desteklemiyor (hareketli ≈ −0,01; statik −0,020…−0,038).
- Hiçbiri 40 s'den uzun bir pencerede ölçülmedi; K-1'in gösterdiği türden
  zamanla biriken bir etki bu tasarımla görülemezdi.
**Etki.** Öğrencinin jüri önünde savunacağı "v0.3 neden böyle" sorusunun
cevabı bugün iki sağlam kazanca dayanıyor: kontrol yükü ~yarı (12/12
hücre) ve — denetçinin 120 s ölçümüyle de 3/3 koşuda desteklenen —
daha düşük gecikme (p95 1,6–3,9 s → 0,8–1,1 s);
öteki cümleler kanıttan geniş. Ayrıca yanlış bir ortalama bir benimseme
kararına girdi.
**Öneri.** K-165 §3'ün D2 satırı ve §4'ün ilgili cümlesi düzeltilsin (ya da
tablo yanlışsa `v2p.py` yeniden koşulup hangisinin doğru olduğu ölçülsün);
`v2/12` ve `DEVIR.md`deki genellemeler kanıtın boyuna indirilsin. Sonraki
profil kararları için değerlendirme tasarımı §5 Ö-2'de.
**Doğrulandı mı:** aritmetik doğrulandı; tablodaki sayıların kendisi
yeniden koşulmadı (hangisinin doğru olduğu doğrulanamadı).

---

#### Y-5 · Yüksek · yöntem — birincil PDR komutları sayıyor; DESPARETE'nin yapısal kaybı ön-kayıtta yok

**Kanıt.** C kararıyla DESPARETE geçit dışı hedefli her paketi düşürüyor
(`desparete.py:383-404`); yere toplamada bu 4 × 0,25 / 40 = **%2,5** trafik
(K-160 §10 kendisi "PDR tavanı ~0,975" diyor). `pdr_pencere` bütün doğan
paketleri sayar (`sim2/olcum/metrikler.py:118-120`). Ön-kaydın birincil
metriği "PDR (ölçüm penceresi)" (`v2/06:160`) ve hükmü `δ` ile `Δ_hedef =
0,05`'e bağlı; `v2/06`'da C kararı ve bu kayıp hiç geçmiyor. Kâhinin 40
tohumluk eşleşik çözünürlüğü ~0,023; yani 0,025'lik yapısal kayıp δ
mertebesinde.
**Etki.** "Üstün / aşağı / ayırt edilemedi" hükmü, protokolün yönlendirme
başarımından değil tek-sink kapsam kararından sistematik olarak etkilenir;
mühürden sonra fark edilirse ya hipotez keşifsel olur ya da sonuç görüldükten
sonra metrik değiştirilmiş olur.
**Öneri.** Mühürden önce öğrenci kararı: birincil metrik (a) bütün trafik
(bugünkü; kayıp DESPARETE'nin aleyhine ve dürüst — ama yazılmalı), (b)
yalnız telemetri (DESPARETE'nin işletme profili), ya da (c) ikisi de, biri
birincil. Hangisi seçilirse `06` §0.4 ve §3'e ve kayıt tablosuna yazılır;
öteki betimleyici olarak raporlanır.
**Doğrulandı mı:** kod ve belgeyle doğrulandı.

---

#### Y-6 · Yüksek · yeniden üretilebilirlik — DESPARETE kanıtı git dışında ve çıktısız

**Kanıt.** `.gitignore` `arsiv/`, `ciktilar2`, `DEVIR*.md`, `v2/arsiv`'i
dışlıyor. K-153…K-165'in "Üretici" satırlarındaki betiklerin hepsi
(`arsiv/teshis/desparete_*/*.py`, `guc_on_tahmin_*/guc.py`) git dışı; bu
klasörlerde (K-154…K-165'in hepsi için) **hiçbir çıktı dosyası yok** — sayılar yalnız
kayıt metninde (`ls arsiv/teshis/desparete_*`). `v2/04`'ün başındaki indeks
üreticisi (`arsiv/dogrulama/kayit_indeksi.py`) de git dışı. U1'in `hukum`
kipi `ciktilar2/aodv_uygunluk/*.json` ister (git dışı; üretmek saatler).
README ise "sonuç dosyaları her makinede yerel olarak üretilir" diyor.
**Üreticiler varsayılana bağlı — ölçüldü.** K-154…K-160 dönemine ait 10
betik (`kapi.py`, `ayna.py` ×3, `kopma.py`, `olcek3.py`, `sure.py`,
`ilk_kosu.py`, `tampon.py`, `ab.py`) DESPARETE'yi profil vermeden kuruyor;
o gün varsayılan v0.1 (+ A), bugün v0.3. Denetçi K-157 §6'nın
`statik-yok · kota 6` satırını (pdr_pencere 0,829 · nrl_bayt_pencere 2,168)
iki biçimde koştu (`k157_yeniden.py`, 67 s): **betiğin bugünkü hâli
0,766 · 0,380** verdi; o günün davranışı açıkça verilince (v0.1 bayrakları,
postür kapalı, `komut_alanlari=True`, seçenek yok) **0,829 · 2,168 birebir**
çıktı. Yani kod geçmişi koruyor (olumlu), ama kayıtlarda yazan üretici
komut bugün o sayıyı ÜRETMİYOR — `03` §2.1'in "bu sayıyı ürettiği yazılan
komut hâlâ koşuyor mu?" sınıfı. K-160'ın çöküş tablosunun üreticisi
`sure.py` de bu durumda.
**Etki.** Git deposunun sahibi öğrencidir ve fikir sahipliğinin kanıtı olarak
sunuluyor; ama DESPARETE'nin bütün tasarım kararlarını taşıyan sayılar o
depodan üretilemiyor ve metin içi bir yanlış (Y-4) ham çıktıyla
karşılaştırılamıyor.
**Öneri.** DESPARETE teşhis betiklerini izlenen bir dizine (ör.
`kalibrasyon/desparete/`) taşı; her betik profili (bayraklar, seçenekler,
`komut_alanlari`, kota) AÇIKÇA versin; her betik çıktısını küçük bir JSON/TXT
olarak (git'e girecek boyutta) yazsın; kayıt, sayının dosyasını ansın.
`kayit_indeksi.py`'yi `kalibrasyon/`a taşı. (Dosya taşıma öğrencinin
"silme yok, taşı" kuralıyla uyumlu.)
**Doğrulandı mı:** evet.

---

#### O-1 · Orta · taban protokoller — RREP-ACK / kara liste yokluğunun gerekçesi karıştırma altında geçersiz

**Kanıt.** `protokoller/aodv_bicim.py:44` RREP-ACK ve kara listeyi (RFC 3561
§5.4 · §6.8) *"bu simülatörde bağ SİMETRİKTİR"* diye dışarıda bırakıyor ve
"AODV'yi zayıflatmaz" hükmü veriyor; AOMDV aynen devralıyor
(`aomdv.py` başlığı). Bağ **kazancı** simetrik (`kanal/yayilim.py:185`), ama
karıştırıcı gücü alıcının konumunda eklenir (`kanal/girisim.py:147-148`):
karıştırıcıya yakın düğüm gönderebilir ama alamaz. RFC'nin kara listesi tam
bu tek yönlü bağlar içindir. DESPARETE ise ACTIVE için iki yönlü kanıt
(unicast + MAC onayı) istediğinden bu asimetriye yapısal olarak dayanıklı;
OLSR de HELLO'da simetrik bağ algılar.
**Etki.** Birincil hücre karıştırıcılı; AODV/AOMDV RREP'i tek yönlü bir
bağa gönderip tekrar tekrar aynı yolu keşfedebilir. Kazancın bir kısmı
DESPARETE'nin tasarımından değil taban protokolün eksik gerçeklemesinden
gelebilir (`06` §8 madde 3, "gizli asimetri").
**Öneri.** Mühürden önce birincil hücrede, geliştirme tohumlarında ölç:
başarısız RREP'lerin ne kadarı SINR'ı asimetrik bağlarda; önemliyse
RFC §6.8 kara listesini (RFC parametreleriyle) uygula; değilse ölçümle
beyan et.
**Doğrulandı mı:** gerekçenin geçersizliği kodla doğrulandı; AODV'ye etkisi
ölçülmedi.

---

#### O-2 · Orta · ölçüm — U1 tüm-koşu PDR'si kullanıyor, ön-kayıt pencere PDR'si

**Kanıt.** `aodv_uygunluk.py:257` `m["pdr"]` döndürür; `pdr` bütün koşunun
(ısınma dâhil) teslim oranıdır, `pdr_pencere` ise ölçüm penceresinde
doğanların (`metrikler.py:116-120`). `v2/06` §3 PDR'yi pencere olarak
tanımlıyor ve `06` §4.3'ün oran formülü "PDR" diyor. DESPARETE'nin kısa
koşu kanıtları da tüm-koşu PDR'si (`ab_v1v5v7.py`, `dogrulama.py`); K-163 §5
v0.3'ün statik "düşüşünün" tamamen başlangıçtan geldiğini (pencere PDR'si
eşit) kendisi ölçmüş.
**Etki.** Isınma, protokolün ilk yakınsamasını U1 oranına katar; yavaş
yakınsayan protokol (v0.3'te alan hop hop daha yavaş kuruluyor) kâhine göre
cezalanır. Kural üç taban protokole de aynı uygulandığından onlar arasında
adil, ama belge–kod uyumsuzluğu var ve DESPARETE için statik eşiğe (0,90)
yakın hücrelerde sonucu belirleyebilir.
**Öneri.** Resmi U1'den önce hangisinin ölçüleceğini yaz (öğrenci); kayıtlı
taban protokol U1 JSON'ları yalnız `pdr` taşıdığı için değiştirmek ya tam
yeniden koşum ister ya da iki metriği birlikte basan bir sonraki koşumu.
**Doğrulandı mı:** kodla doğrulandı.

---

#### O-3 · Orta · testler — sahte ön koşullar, eksik uçtan uca kapı, tautolojik iddialar

**Kanıt.**
- K-1'deki gibi, istek ve solicit testleri ön koşulu (gönderen ACTIVE) elle
  kuruyor (`test_desparete.py:944-958`, `975-993`, `996-1010`); v0.3
  entegrasyonunda ön koşul neredeyse hiç oluşmuyor (K-1: geçitte işlenen
  istek 0) ama test takımı yeşil.
- `_desparete_kos_denetimli`'nin belgesi *"`bayraklar=None`: varsayılan
  (hepsi açık, K-159)"* diyor (`test_desparete.py:501`); varsayılan artık
  PROFIL_V02 + SECENEK_V03 — simülatör testlerinin çoğu artık v0.3'ü
  sınıyor, adları ve belgeleri v0.1'i anlatıyor.
- Tanım gereği doğru iddialar: `test_kontrol_duzlemi.py:539`
  (`unicast_vazgecilen + kuyruk_tasmasi >= 0`), `test_yapilandirma.py:692`
  (`SINANMAMIS >= 0`; belgesi "bugün 51" diyor, gerçek 40).
- İçe aktarma grafiği testi (D-1) ve `kosu_kimligi` testleri (Y-1) iddia
  ettiklerinden dar.
- Olumlu: "sınav boş geçti" korumaları yaygın; her kancadan sonra döngü ve
  FD denetimi (`test_desparete.py:494-560`) gerçekten güvenlik değişmezini
  sınıyor; `PYTHONHASHSEED` testleri var ve bağımsız ölçümüm de doğruladı.
**Öneri.** v0.3 (ya da yeni profil) için uçtan uca canlılık testi (açlık →
istek → tur artışı; tampon → onarım → teslim); tautolojik iddiaları
kaldır ya da gerçek bir alt sınıra bağla; test adlarını/belgelerini
profille eşle.

---

#### O-4 · Orta · yeniden üretilebilirlik — regresyon matrisinde gerçek protokol yok

**Kanıt.** `kalibrasyon/regresyon_satirlari.py:113-207`: 45 vakanın hepsi
koşum protokolleri (`dogrudan_komsu`, `en_yakin_kimlik`), kâhinler ya da
sınav protokolleri. AODV, OLSR, AOMDV ve DESPARETE matriste yok. DESPARETE'nin
varsayılanı 24 Eylül'de üç kez değişti (v0.1 → v0.2 → v0.3) ve davranışını
koruyan tek şey birim/küçük dünya testleri.
**Etki.** `06` §8'in 4. koşulu ("sonucu üreten kodun regresyon testi")
protokol düzeyinde karşılanmıyor; bir protokol düzeltmesinin başka bir
davranışı sessizce değiştirip değiştirmediği görülmez.
**Öneri.** Her protokol için birer kısa pencere vakası (ör. `p-…-aodv`,
`p-…-desparete-v03`) ekle — bir sonraki `uret` bunları taban yapar.

---

#### O-5 · Orta · kayıtlar — bayat ve çelişkili belgeler

Hepsi doğrulandı (dosya:satır):

| yer | ne yazıyor | gerçek |
|---|---|---|
| `README.md:20-26` | "Durum — 23 Eylül 2026 … gerçekleme başladı" | v0.3 yazıldı, 3.8'de |
| `README.md:39` | "DESPARETE buraya yazılacak" | yazıldı (8 dosya) |
| `README.md:91` | ablasyon "açılıp kapanabilecek" | bayraklar K-159'da yazıldı |
| `v2/12:3` · `:194` | "Güncel: 23 Eylül" · "Tam yol haritası — 23 Eylül" | içerik 24 Eylül'ü anlatıyor |
| `v2/12:18` | geçerli regresyon tabanı `k151` | `k157` (K-157; `DEVIR.md:146`) |
| `v2/12:19` | 130 modül (K-155) | 133 (ölçüldü) |
| `v2/12:286-302` | 3.8 "U1'in sayısal koşumu ve U3 sırada", 3.9/3.10 "v0.2 kararları" sırada | v0.2 ve v0.3 kararları verildi |
| `v2/12:213-216` | gecikme ve "kararlı durumda zararlı" | Y-4 |
| `v2/07` §15 (`:941-954`) | 24 Eylül: C · v0.2 · V0 | K-162 · K-163 · **K-164 (v0.3)** · K-165 ve "resmi U1 daha sonra" yok — "öğrenci kararlarının TEK listesi" eksik |
| `v2/07:3`, `:591`, `:593` | "Güncel: 10 Eylül" · "503 passed" · Li H1 0,0861 | 810 · 0,0871 (`DEVIR.md:140`) |
| `v2/06:3`, `:214`, `:589-597`, `:575-585` | "Güncel: 10 Eylül" · PSR "kod değişecek" · kayıt tablosu 10 Eylül'de bitiyor · §9'da yapılmış işlerin kutusu boş | PSR uygulandı (K-115); K-153 (§0.4) ve U1 eşiği (K-136/137) tabloda yok |
| `v2/README.md:14` | `04` "K-160'a kadar" | K-165 |
| `v2/13:12-13` | taban protokoller "henüz yazılmadı" | üçü kapalı |
| `DEVIR-PROMPT.md:124` ↔ `:157` · `:178` | geçerli taban `k151` ↔ `k157`; okuma sırası "K-140…K-151" | `k157`; K-165 |
| `protokoller/desparete.py:5-6`, `:128` | "Kararlar … K-159" · "DESPARETE v0.1" | K-165 · v0.3 |

**Öneri.** Aşama geçişinde tek seferlik bir tazeleme; `v2/07` §15'e 24
Eylül'ün üç öğrenci kararının eklenmesi fikir sahipliği için önemli.

---

#### O-6 · Orta · yöntem — "ölçmeden önce" sırası VCS ile doğrulanamıyor

**Kanıt.** Depoda yalnız iki commit var: `8743a9a` (23 Eylül 00:42; K-150 ve
K-151'e kadar, DESPARETE kodu yok) ve `c48fdc2` (24 Eylül 22:20; K-152…K-165,
bütün DESPARETE kodu, `v2/06` §0.4). Yani `06` §0.4'ün (K-153) ilk DESPARETE
koşusundan önce yazıldığı ve kayıtlardaki 🔒 "ÖLÇMEDEN ÖNCE" bloklarının
sonuçtan önce yazıldığı git'le gösterilemez. Dolaylı kanıt tutarlı:
`guc.py` 23 Eylül 17:28, ilk koşu betiği `ilk_kosu.py` 17:50 (dosya
zamanları).
**Etki.** Ön-kaydın değeri bu sıradadır; jüri "bunun önceden yazıldığını
nereden bileceğiz?" diye sorabilir.
**Öneri.** Mühür ve ana deney için: beklenti/hipotez metni koşudan ÖNCE
ayrı bir commit (öğrenci koşar) ya da en azından özeti (SHA-256) tarihli bir
yere; mühür commit'inin özeti rapora.
**Doğrulandı mı:** yokluk doğrulandı; sıranın kendisi doğrulanamadı.

---

#### O-7 · Orta · DESPARETE · iddia — README'nin "temel fikirleri" ile değerlendirilen profil

**Kanıt.** README (`:77-82`) postürleri (STEADY · CAUTION · PROTECT) temel
fikirler arasında sayıyor. Değerlendirilecek v0.3'te: PROTECT'e hiç
girilmez (yedeklilik yok, `desparete.py:170-172`); CAUTION'a girişlerin
%100'ü yapısal belirsizlikten (K-158, 190/190); postürün tek etkisi girişte
bir doğrulama PROBE'u. Boşta sondalama, onarım edinimi ve ilan koruması
kapalı (PROFIL_V02); güvenlik profili kapalı; komutlar düşer; K-1 yüzünden
DFSN istek yolu işlemiyor.
**Etki.** Jüri önünde "hangi mekanizma kazandırdı" sorusunun cevabı, ilan
edilen fikirlerle ölçülen protokol arasındaki farkı açıkça söylemezse
aleyhe döner.
**Öneri.** Raporda ve README'de "değerlendirilen DESPARETE profili"ni tek
tabloyla ver (açık/kapalı mekanizmalar); postürün katkısını ablasyonla ölç
ya da iddiayı daralt.

---

#### O-8 · Orta · simülatör · taban protokoller — bağlayan SINANMAMIŞ parametreler

**Kanıt.** (a) Rota tamponu 64 paket · 30 s (SINANMAMIŞ): `aodv_uygunluk.py
hukum` çıktısında AODV'nin iki hareketli hücresinde tepe **64/64** ve süre
tavanından düşen 22 + 33 paket — tampon AODV için bağlıyor. (b)
`yeniden_deneme_siniri = 4` (`konfig.py:481`); köken kaydı
(`kokenler.py:449-452`) bunun 802.11'in UZUN çerçeve sınırı olduğunu, 512
baytlık çerçeve için KISA sınırın (7) geçerli olduğunu kendisi yazıyor ama
SINANMAMIŞ bırakıyor. Tekrar sınırı hem bütün protokollerin kopma algısını
hem DESPARETE'nin M0.1 skorunu (`skor = 255/(1+r)`) belirler.
**Öneri.** Mühürden önce: (a) tampon kapasitesi ve ömrü için AODV/AOMDV'de
birincil hücrede duyarlılık; (b) tekrar sınırını standarda (7) çek ya da
eksen ilan et (sim2 değişikliği → onay + regresyon).

---

#### O-9 · Orta · yöntem — "üstün" hükmünün üçüncü koşulu tanımsız

**Kanıt.** `v2/06` §0.4.2: "üstün" = Holm sonrası p < 0,05 **ve** ortalama
fark ≥ δ **ve** mekanizma kapısı (Aile 3) — kapı "mühürde" tanımlanacak.
Aile 3'ün bugünkü ölçütü (§5.3: komşuların bildirdiği bilginin permütasyonu)
eski tasarımdan taşınmış; DESPARETE'de hangi bilginin permüte edileceği
belli değil. Güç yöntemi (§0.4.3) yalnız Wilcoxon reddini sayıyor; δ ve
mekanizma koşulları güce girmiyor. Durdurma kuralı ve koşul 1'in k değeri de
açık (`06` §9).
**Öneri.** Mühürden önce Aile 3'ü DESPARETE'nin bayraklarına göre yeniden
yaz (hangi bayrak kapalı kol, ölçüt ne), gücü üç koşulun birleşimiyle
benzet.

---

#### O-10 · Orta · risk · fikir sahipliği — ajan katkısının görünürlüğü

**Kanıt.** README (`:161-163`) "DESPARETE'nin tasarımı öğrenciye aittir;
yapay zekâ danışman ve uygulayıcıdır" diyor. Kayıtlar kararları doğru
ayırıyor (ör. K-161 "Adaylar ve kanıt: ajan · Seçim: öğrenci"). Ancak:
(a) değerlendirilecek v0.3'ün üç mekanizmasından V7 tamamen ajanın, V1 ve V5
ajanın önerisi (K-162 §5, K-163); (b) tasarım paketinin karar günlüğü
"Proje sahibi … onayladı / Kullanıcı onayı" kalıbıyla ilerliyor ve paketin
dizini bir `00_MASTER_PROMPT.md` ("Agent/proje yönetimi ve çalışma
yönergeleri", `00_TASARIM_PAKETI_INDEX.md:46`) anıyor — 39 belgelik v0.1
paketi 20–22 Eylül'de, öğrencinin v0 taslağından bir ajan sürecinde
ayrıntılandırılmış görünüyor; bu süreç bu depoda belgeli değil; (c) `v2/07`
§15, v0.3 kararını içermiyor (O-5).
**Etki.** "Bu protokolün ne kadarı senin?" sorusuna depo bugün tam cevap
vermiyor; özellikle v0.3'teki ajan kaynaklı mekanizmalar.
**Öneri.** Rapora girecek bir "katkı tablosu": v0 taslağı (öğrenci), v0.1
paketinin nasıl üretildiği (hangi araçla, hangi kararlar öğrencinin),
gerçekleme (ajan), v0.2/v0.3 (ajan önerisi, öğrenci seçimi), ablasyonla
ölçülen katkı. `00_MASTER_PROMPT.md` ve paket kaynağının (ana corpus) bir
kopyası arşive.
**Doğrulandı mı:** kayıtlar doğrulandı; paketin kim tarafından hangi araçla
yazıldığı doğrulanamadı.

---

#### O-11 · Orta · risk — hesap bütçesi ve takvim (tahmin)

**Dayanak (kayıtlardan).** Taban protokol U1'leri 24 iş için 2,5–4,2 sa duvar
(AODV 4 işçi, OLSR ve AOMDV 8 işçi; `DEVIR.md` §2 madde 19); DESPARETE
v0.2'nin 350 s'lik hareketli işi 2,5–4,3 sa (K-161 §6 tahmini), resmi U1
~38 CPU-sa. **Denetçinin ölçümü:** tam ölçek, 120 s'lik hareketli iş v0.3'te
35–49 dk, v0.2'de 60–76 dk (6 paralel iş) → 350 s'lik bir v0.3 işi doğrusal
ölçekle ~1,7–2,4 sa. **Kaba tahmin:** çekirdek 2–3 hücre
× 40 tohum × 4 protokol ≈ 600–750 CPU-sa; Aile 3'ün her ablasyon kolu +40
DESPARETE koşusu (~100 CPU-sa); 4.1 gürültü ölçümü ~50 CPU-sa. 8 işçide
(4'ü verimlilik çekirdeği) toplam **~1–1,5 hafta kesintisiz makine**.
Kasım ortasına sığar ama bir kusur bulunup ana deney tekrarlanırsa takvim
kayar; K-162'nin koşumu makine paylaşıldığı için iki kat uzamıştı. Analiz
katmanı (`analiz/`) henüz yok.
**Öneri.** v0.3 (ya da düzeltilmiş profil) için 350 s'lik tek bir tam ölçek
işin süresini ölç; ana deneyin bütçesini mühürde yaz; ana deneyden önce kodu
dondur (etiket/commit); analiz katmanını gürültü ölçümüyle birlikte yaz ve
gürültü verisinde dene.

---

#### D-1 · Düşük · simülatör — içe aktarma grafiği testi dar

**Kanıt.** `tests2/test_kosum.py:555-569` yalnız `import sim2.X…` ve
`from sim2.X… import` biçimlerini ve `names[0]`'ı yakalıyor;
`from sim2 import kanal`, `import sim2`, `import os, sim2.kanal`,
`importlib`/`__import__` ve `kalibrasyon` (kâhin grafiği) yasak listesinde
değil. **Bugün ihlal yok** — `protokoller/` yalnız `sim2.gozlem` ve standart
kütüphaneyi içe aktarıyor (denetçi taradı); `sim2.gozlem` de yalnız
`cekirdek.degismezler` ve `cekirdek.saat`i.
**Öneri.** Testi `sim2`'nin gozlem dışı her alt modülünü, `kalibrasyon`u ve
`tests2`yi kapsayacak, `ImportFrom`'un `names`ini de denetleyecek biçimde
genişlet; README'deki "engellenir" ifadesini "denetlenir" yap.

#### D-2 · Düşük · depo — izlenen `.pyc` ve istemin geçmişe girmesi

154 `.pyc` git'te izleniyor (ilk commit'te `__pycache__/` kuralı yoktu;
`c48fdc2` onları güncelledi). `.gitignore`'daki `DENETIM_PROMPT.md` yazım
hatası yüzünden `DENETIM-PROMPT.md` `c48fdc2`'ye girdi; indekste silme ve
düzeltme bekliyor ama dosya geçmişte kalıyor (bilgi). **Öneri (öğrenci
koşar):** `git rm -r --cached` ile `__pycache__` dizinlerini indeksten çıkar.

#### D-3 · Düşük · depo — satır sonları

İndeks tamamen LF (`git ls-files --eol`: 201 dosya `i/lf`); çalışma kopyası
87 CRLF · 111 LF · 3 karma dosya (`.gitignore`, `tests2/test_cekirdek.py`,
`tests2/test_olcum.py`); `core.autocrlf=true`, `.gitattributes` yok. Git'te
sorun yok; ama `arac_hash` çalışma kopyasının baytlarını özetlediği için
(`kimlik.py:71`) aynı commit farklı satır sonu ayarlı bir makinede farklı
araç özeti verir. **Öneri:** `.gitattributes` (`* text=auto eol=lf` ya da
tersi) ve özetten önce satır sonu normalleştirme.

#### D-4 · Düşük · kod — komut düşüşleri `hedef_yok`a karışıyor

C gereği düşen komutlar beyansız düşüyor ve `hedef_yok` sebebine yazılıyor
(`desparete.py:401-404`); K-162 bunları elle ayırmak zorunda kaldı ("~35'i
… kalanı C gereği"). Ayrı bir düşme sebebi (`politika`) ya da satırda
`veri_sink_disi` toplamı analiz için yeterli olur.

#### D-5 · Düşük · kod — köken defteri protokol sabitlerini kapsamıyor

Köken taraması `sim2/` ve `kalibrasyon/` sabitlerini sayıyor (K-152 §5);
DESPARETE'nin ajan seçimi sabitleri (`K_YEDEK_CANLI = 2`, K-165; ölçüm
PROBE'u, V1 bit anlamı) ve `YEREL_TAMPON = 64`'ün Konfig'le ikinci kopyası
(`desparete_bicim.py:197`, bir testle bağlı) defterde değil. README "her
parametrenin kökeni kayıtlı" diyor.

#### D-6 · Düşük · kod — küçük belge–kod uyumsuzlukları

`sim2/cekirdek/saat.py:27-29` "çalışma anında `saat_s` yalnız `YerelZaman`
kabul eder" diyor; `YerelZaman` bir `NewType` (`:55`), çalışma anında denetim
yok. `desparete.py:232` başka sınıfın özel yöntemini (`_guvenli_adaylar`)
çağırıyor.

#### D-7 · Düşük · simülatör — `v2/07` §17'nin açık satırları

A6 (menzil alanının adı yanlış bir iddia taşıyor), A8 (`Konfig`in
varsayılan deseni hâlâ `esler_arasi`, `konfig.py:514`; birincil desen yere
toplama) ve A23 (kodun kapsam listesi kontrol edilecek) açık. A8 Aşama 4
için pratik bir risk: ana deney aleti deseni açıkça vermezse taban
protokoller sessizce eşler arası koşar. **Öneri:** ana deney aletinde desen,
tehdit senaryosu ve kol her satırda zorunlu parametre olsun; satırın
`konfig.trafik_deseni` alanı analizde denetlensin (Y-1 ile birlikte).

#### B-1 · Bilgi · yöntem — ana deney tohumları dünya kurmak için kullanıldı

`kalibrasyon/dugum_sayisi.py:236-260` (`--bolunme`) 2000–2039 tohumlarıyla
kanal grafiği kurdu (K-132); `senaryolar.py:195-218` sonucu (hangi ana deney
tohumunun bölündüğü) koda yazılı. Hiçbir protokol koşmadı, gerekçe açık ve
doğru; ama README'nin "hiçbir kolda koşulmaz" cümlesi harfiyen değil —
"hiçbir protokol koşulmaz; yalnız dünya grafiği kuruldu" demek daha doğru.
Denetçinin aramasında (`kalibrasyon`, `tests2`, `sim2`, `protokoller`,
`arsiv/teshis`, `arsiv/dogrulama`) ana deney tohumuyla protokol koşan bir
yer bulunmadı.

#### B-2 · Bilgi (olumlu) — U1 eşiğinin sonradan seçildiği doğru beyan edilmiş

`v2/06:334-339`, `aodv_uygunluk.py:60-80`, `v2/07` §15 (17 Eylül):
eşiğin ölçüm görüldükten sonra seçildiği, sebebi ve sınırı açıkça yazılı;
eşik üç taban protokolü birden bağlıyor ve sonra değiştirilmedi. Doğru ve
dürüst beyan.

#### B-3 · Bilgi (olumlu, kısmen) — güvenlik değişmezleri kodda ve testte korunuyor

Kodda: eşit potansiyel uygulanabilir değil (`desparete_alan.py:298-299`),
FD aynı turda yalnız küçülür (`:273-274`), DFSN karşılaştırması belirsizse
alan kapanır (fail-closed, `:259-260`), ACTIVE olmayan komşunun ilanı aday
olamaz (`:224-226`), DFSN'yi yalnız hedef üretir (`:171-177`, yalnız
`_hedefte`den çağrılır), Hop Limit verisi (`desparete.py:406-408`). Bunlar
ablasyon bayraklarıyla kapanmıyor (`desparete_bayrak.py:33-38`). Testler
küçük dünyada her kancadan sonra ardıl grafiğinde döngü ve aynı turda FD
artışı arıyor (`test_desparete.py:494-560`). **Sınır:** bu denetim yalnız
testlerde ve teşhis betiklerinde var; resmi U1 ve ana deney koşularında
çalışmıyor — ucuz bir örnekleme sürümü (ör. her 1 s'de bir) sonuç satırına
"döngü 0" diye yazılabilir. Döngüsüzlük güvenliktir; K-1 ise **canlılık**
kusurudur — ikisi ayrı.

---

## 5 · DESPARETE önerileri

Her öneri **öğrencinin kararıdır** (tasarım onun). "Ölçülmüş" ile
"öneri / tahmin" ayrı yazıldı.

### Ö-1 · V5'i edinim yoluyla barıştır (K-1'in düzeltmesi)

- **Gerekçe (ölçülmüş):** K-1 — v0.3'te geçit ve röleler istek/solicit
  gönderenini ACTIVE görmüyor; DFSN hiç artmıyor.
- **Seçenekler:**
  (a) Tasarımın kendi kuralını geri getir: *gelen PROBE nitelik açar*
  (`23` §6, `EnsureUnqualifiedPeer`); V5 yalnız pasif duymaya uygulanır.
  (b) V5'i kaldır, V1 + V7 kalsın (K-163: V1 + V7 küçük dünyada işliyor).
  (c) Güvenlik profili kapalıyken istek/solicit kabulünü "doğrudan komşudan
  gelen doğrulanmış çerçeve" koşuluna gevşet — güvenlik değişmezi (FD,
  DFSN'yi yalnız hedef üretir) değişmez, ama `23` §2'nin AcceptPacket
  kuralından sapmadır ve beyan ister.
  (d) Karar verilmeden önce profil sorusunu yeniden aç: v0.2, v0.3,
  v0.3 + (a) ve V1 + V7 (V5 yok) tam ölçekte, uzun pencerede eşli
  karşılaştırılsın (Ö-2).
- **Ölçülmüş kısım (nedensel kol, küçük dünya, 300 s, 6 koşu):** (a)
  istek/solicit yolunu 6 / 6 koşuda yeniden açıyor (geçitte işlenen istek
  0 → 3–9, yanıtlanan solicit 0 → 11–23) ama pencere PDR'sine etkisi küçük
  ve karışık (−0,013 … +0,061, ortalama +0,012) ve nitelik PROBE'larını
  ~2,2 katına, kontrol/veri kanal süresini 0,60–0,66'dan 0,78–0,91'e
  çıkarıyor. Yani (a) tek başına v0.3'ün uzun koşudaki kaybını kapatmıyor;
  **profil sorusu (v0.2 mi, v0.3 mü, başka bir bileşim mi) yeniden açık** —
  40 s kanıtıyla v0.3 önde; 300 s küçük dünyada 6 / 6, tam ölçek 120 s
  formasyonda 2 / 2 geride.
- **Beklenen etki (tahmin):** açlık çözülür; uzun koşuda ulaşılamaz bölüm
  azalır; bedeli PROBE ve kontrol yükü artışı.
- **Risk:** V5'in yük kazancının bir kısmı geri gelir; (c) tasarımdan sapma.
- **Nasıl sınanır:** tam ölçek, ≥ 120 s (tercihen 350 s), ≥ 3 tohum,
  v0.2 · v0.3 · v0.3 + (a) eşli; pencere PDR'si, zaman dilimli PDR, geçitte
  işlenen istek ve tur artışı, kontrol/veri kanal süresi; uçtan uca test.

### Ö-2 · Profil kararları için değerlendirme tasarımı

- **Gerekçe (ölçülmüş):** Y-4, K-1 — 40 s'lik pencere zamanla biriken
  etkiyi göremiyor; 3 tohumda ±0,03 gürültü; ayar hücreleri = kabul
  hücreleri.
- **Öneri:** ayar için U1'den ve ana deneyden AYRI bir geliştirme tohum
  kümesi (ör. 1003–1010); ≥ 5 tohum; ≥ 120 s ölçüm; pencere PDR'si birincil,
  tüm-koşu ikincil; gecikme ortak alt kümede (`03` §B3) ve kesişim oranıyla;
  en az bir karıştırıcılı hücre (birincil hücrenin kendisi); her aday için
  "önceden yazılan beklenti" + commit (O-6).
- **Risk:** hesap süresi (ölçüldü: tam ölçek 120 s'lik hareketli iş v0.3'te
  35–49 dk, v0.2'de 60–76 dk, 6 paralel işte).

### Ö-3 · Kaynak turunun (DFSN) canlılığını tasarımda güvenceye al (tahmin)

- **Gerekçe:** DESPARETE'de FD yalnız yeni turla sıfırlanıyor; tur yalnız
  istek üzerine artıyor. İstek yolu herhangi bir sebeple (K-1, karıştırma,
  bölünme) kapanırsa ağın açlıktan çıkış yolu kalmıyor.
- **Öneri (tasarım değişikliği):** hedefin turunu seyrek ve periyodik
  olarak da artırması (DSDV'nin periyodik sıra numarası artışı gibi; ör.
  30–60 s) ya da tasarım paketinin TG-04'ündeki "hedefte artış oran
  kapısı" ile birlikte ele alınması. Güvenlik argümanı değişmez (turu yine
  yalnız hedef üretir); bedeli periyodik bir yeniden yakınsama.
- **Nasıl sınanır:** 350 s koşularda FD açlığı sayacı ve ulaşılamaz bölüm;
  eşli A/B.

### Ö-4 · Postürü ya ölçerek savun ya iddiayı daralt

- **Gerekçe (ölçülmüş):** K-158: CAUTION girişlerinin %100'ü belirsizlikten
  (190/190); PROTECT yapı gereği yok; karıştırıcılı kolda doğrulamanın bedeli
  +%4,4 ek yük (5/5), teslime katkı görünmüyor.
- **Öneri:** (a) CAUTION'ı yalnız `H ≥ 64` ile tetikle (U'yu kanıttan çıkar)
  ya da U eşiğini trafik hızına bağla (K-158 §6'nın aday soruları); (b)
  postür bayrağını Aile 3'te bir ablasyon kolu yap; ölçülmezse README ve
  rapordan "postürler temel fikir" iddiası çıkar.

### Ö-5 · Komut trafiği ve birincil metrik

- **Gerekçe:** Y-5.
- **Öneri:** C kalsın; birincil metrik tanımı mühürden önce (tüm trafik mi,
  telemetri mi) yazılsın; ikisi de raporlansın. A′ (talep yolunda komut
  alanı) gelecek çalışma olarak beyan.

### Ö-6 · M0.1'in ilk örneği (tahmin)

- **Gerekçe (ölçülmüş, K-163 §2):** ilk örnek V7'nin ek PROBE'uyla
  üretiliyor.
- **Öneri:** nitelik PROBE'unun MAC onayını, ACTIVE'e geçişle aynı anda ilk
  M0.1 örneği saymak (`35` §3.1'in yorumu — tasarım kararı). Beklenen: V7'nin
  PROBE'u gereksizleşir. **Risk:** örnek, ACTIVE olmadan yapılmış bir
  denemeden gelir; tasarımın tanımından sapma.

### Ö-7 · Ablasyon kolları ve kimlik

- **Gerekçe:** Y-1; K-159'un "hepsi açık = v0.1" sözleşmesi, varsayılan v0.3
  olunca kol tanımlarını karıştırıyor.
- **Öneri:** Aile 3 kollarını mühürden önce v0.3 (ya da düzeltilmiş profil)
  temelinde adlandır (ör. "v0.3 − risk terimi"), her kolu kimlik düzeyinde
  ayırt edilebilir yap (Y-1'in düzeltmesi), analiz katmanı satırdaki
  bayrak/seçenek demetini kol etiketiyle karşılaştırsın.

---

## 6 · Doğrulanamayanlar

| konu | neden |
|---|---|
| K-1'in 350 s tam ölçekteki büyüklüğü ve 3'ten çok tohumda yönü | koşum saatler sürer; 120 s tam ölçek (3 koşu) ve 300 s küçük dünya (12 koşu) ölçüldü |
| K-165 §3 tablosu mu metni mi doğru | `v2p.py` (15 iş, ~25+ dk tam ölçek) yeniden koşulmadı; yalnız iç tutarsızlık gösterildi |
| "ÖLÇMEDEN ÖNCE" bloklarının gerçekten önce yazıldığı | iki büyük commit; yalnız dosya zamanları tutarlı |
| tasarım paketinin kim tarafından, hangi araçla yazıldığı | kaynağı ("ana proje corpusu", `00_MASTER_PROMPT.md`) depoda yok |
| RREP-ACK / kara liste yokluğunun AODV'ye etkisi (O-1) | birincil hücrede ölçüm gerekir |
| taban protokollerin RFC'ye satır satır sadakati | zaman; başlık beyanları ve U1 kayıtları okundu |
| K-132'nin ana deney tohumu bölünme tablosunun bugünkü kodla geçerliliği | yeniden koşulmadı (dünya/kanal kodu `k157`'den beri değişmedi) |
| `uretici_duman`, D1 listesinin uzun maddeleri, regresyon üretimi | süre ya da diske yazma |
| `v2/02`'nin kaynak doğrulamaları | kapsam dışı bırakıldı |
| hesap bütçesi (O-11) | tahmin; 350 s'lik v0.3 işi ölçülmedi |

---

## 7 · Öncelikli eylem listesi

1. **Resmi U1'i v0.3 ile koşma.** K-1'i öğrenciye anlat; Ö-1'in seçeneklerinden
   birini seç; seçileni ≥ 120–350 s, ≥ 3 tohum, eşli ölç (Ö-2) ve uçtan uca
   canlılık testini ekle. Sonra U1.
2. **U1-U'nun kâhin kuralını** (Y-2) ve **U1'in hangi PDR'yi ölçtüğünü**
   (O-2) resmi U1'den ÖNCE yaz (öğrenci kararı; `06` §4.4 + §10).
3. **`kosu_kimligi`ni düzelt** (Y-1): tedavi alanları + protokol + profil;
   farklı koşu → farklı kimlik testi (yapı onayı + regresyon `uret` +
   `karsilastir` beklentisi önceden yazılı).
4. **Ön-kaydı tamamla:** birincil PDR'nin komut tanımı (Y-5); taban
   protokollerin yere toplamada kabulü (Y-3); Aile 3'ün mekanizma kapısı ve
   gücün üç koşulla benzetimi (O-9); kayıt tablosunu (§10) ve §9'u güncelle.
5. **Taban protokol adilliği:** RREP-ACK/kara liste (O-1), tampon ve tekrar
   sınırı (O-8) birincil hücrede ölçülsün; gerekirse düzeltilsin.
6. **K-165 §3/§4'ü düzelt** ve `v2/12`, `DEVIR.md`deki v0.3 genellemelerini
   kanıt boyuna indir (Y-4).
7. **Kanıtı depoya al:** DESPARETE teşhis betikleri + küçük çıktı dosyaları
   izlenen bir dizine; `kayit_indeksi.py` `kalibrasyon/`a (Y-6); regresyon
   matrisine gerçek protokol vakaları (O-4).
8. **Belgeleri tazele** (O-5): README, `v2/12`, `v2/07` §15 (v0.3 kararı!),
   `v2/06`, `v2/README`, `v2/13`, `DEVIR*`; README'de değerlendirilen
   profilin tablosu (O-7).
9. **Fikir sahipliği tablosu** (O-10) ve tasarım paketinin üretim sürecinin
   arşive alınması.
10. **Git hijyeni** (öğrenci koşar): `.pyc`'leri indeksten çıkar,
    `.gitattributes`, commit başına bir iş; beklentileri koşudan önce commit
    et (O-6).
11. **Bütçe:** 350 s'lik tek bir tam ölçek DESPARETE işinin süresini ölç;
    ana deney bütçesini ve kod dondurma noktasını mühürde yaz; analiz
    katmanını gürültü ölçümüyle birlikte yaz (O-11).
