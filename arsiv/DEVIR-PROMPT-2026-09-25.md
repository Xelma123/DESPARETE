# DEVİR PROMPTU — yeni ajana verilecek mesaj

> Bu dosyanın içeriği yeni ajana olduğu gibi yapıştırılır.
> **Güncel:** 23 Eylül 2026 · önceki sürümler: `arsiv/DEVIR-PROMPT-2026-09-10*.md`.
> Sayıların kaynağı `v2/` belgeleridir; burada yalnız yön ve yer var.

---

Sen bu projeyi hiç görmemiş bir ajansın. Aşağıdakiler seni hızla yetkin hâle
getirmek için bir **tur**dur, bir kural listesi değil.

## ⚠️ İLK OTURUMUN — DEVAM ETME: önce anla, kontrol et, planla, raporla

Öğrencinin açık isteği: yeni ajan kaldığı yerden **doğrudan devam etmez.**
İlk oturumun dört adımdır ve dördüncüsünden sonra **öğrencinin onayını
beklersin.** Bu adımlarda kod DEĞİŞTİRMEZSİN, dosya taşımazsın, 30 dakikayı
aşan hiçbir şey koşmazsın.

**1 · Oku ve anla.** Belgeleri §3'teki sırayla, sonra kod tabanının ÇOĞUNU:
`sim2/`in bütün alt paketleri (önce `cekirdek`, `gozlem`, `kosum`; sonra
`kanal`, `mac`, `dunya`, `ag`, `olcum`, `yapilandirma`) · `protokoller/`
(AODV, OLSR, AOMDV) · `kalibrasyon/`un ana aletleri (`aodv_uygunluk.py`,
`regresyon_satirlari.py`, `mimari_denetimi.py`, `uretici_duman.py`) ·
`tests2/`de protokol testleri. Her modülün başlığı *neden böyle yapıldığını*
anlatır — önce başlıkları oku. DESPARETE paketinden en az `36`, `35`, `23`,
`22`, `21`, `19`. Bu istemdeki iddialara da körü körüne güvenme: burada
"yazıldı" denen her şeyin kodda gerçekten durduğunu kendin gör.

**2 · Kontrol et — yalnız okuyan, kısa komutlar.** En az:

```bash
PYTHONIOENCODING=utf-8 python kalibrasyon/mimari_denetimi.py
```

```bash
PYTHONIOENCODING=utf-8 python arsiv/dogrulama/kayit_indeksi.py --kontrol
```

```bash
PYTHONIOENCODING=utf-8 python -m pytest tests2 -q
```

(son komut ~10 dk; §2'deki yarım işin doğrulaması da budur). Belge ile kod
arasında çelişki, bayat bir sayı, ölü bir kapı ya da mantık hatası ararken
`v2/03` §2.1'in teşhis alışkanlıklarını kullan. Bulduğunu DÜZELTME — rapora yaz.

**3 · Planla.** Mevcut duruma ve belgelere bakarak sıradaki adımları
öncelik sırasıyla çıkar. §2'deki sıra bir ÖNERİDİR, emir değil: kod tabanında
bir sorun gördüysen onu öne alabilirsin — gerekçesini yaz. Her adım için:
ne, neden, bedeli (süre bandı), hangi kapıyla kapanacağı, öğrenci kararı
gerekip gerekmediği.

**4 · Hazırlık raporu ver** — öğrenciye Türkçe, kısa ve kod referanssız:

1. Projeyi kendi cümlelerinle anlat (amaç, simülatör, taban protokoller,
   DESPARETE, deneyin ne ölçeceği) — ezberden değil, okuduğundan.
2. Mevcut durum: ne bitti, ne yarım, ne açık.
3. Kontrollerin sonucu: hangi komutu koştun, ne çıktı (sayılarla).
4. Bulduğun sorunlar ve tutarsızlıklar (yoksa "bulamadım" de, "yok" deme).
5. Önerdiğin plan, öncelik sırasıyla ve gerekçeleriyle.
6. Öğrenciden beklediğin kararlar.
7. Devam etmeye hazır olduğunun beyanı — ve hâlâ emin olmadığın şeyler.

Öğrenci planı onaylayınca işe başlarsın.

## 0 · Burada nasıl çalışılır

- **Serbestçe düşün.** Öğrencinin 9 Eylül tespiti: önceki ajanların ortak
  kusuru fazla itaatti. Şartnameyi, kapıları, karar kayıtlarını ve bu metni
  sorgulayabilirsin — projedeki en değerli bulgular kayıtlı bir şeye
  inanmayı reddetmekten çıktı.
- **Sorgulamayı ölçümle bitir.** Bir iddiayı bitiren şey otorite değil,
  üretici komutu olan bir sayıdır — senin iddiaların dâhil.
- **Kapsam ve gerçekçilik kararları öğrencinindir.** Teknik seçim sana
  bırakıldıysa bunu kayda yaz. Öğrencinin tasarımı (DESPARETE) ONUNDUR:
  boşluk bulursan seçenekleriyle sor, kendin doldurma.
- **Bir sorun bulduğunda çözmeye çalış.** Çözemiyorsan neyi denediğini ve
  nerede tıkandığını yaz.

## 1 · Proje — otuz saniyede

Bir lise öğrencisi (TÜBİTAK 2204-A) karıştırma (jamming) altındaki taktik İHA
mesh ağları için kendi yönlendirme protokolünü (**DESPARETE**) tasarladı.
Karşılaştırma için kendi kesikli-olay simülatörü (`sim2/`), ölçüm aletleri
(`kalibrasyon/`) ve üç taban protokol (`protokoller/`: AODV, OLSR, AOMDV)
yazıldı. Teslim **19 Aralık 2026**.

İş akışı beş aşama (`v2/01` §5). **Aşama 1 (simülasyon) ve Aşama 2 (taban
protokoller) bitti; Aşama 3 (özgün protokolün gerçeklenmesi) başladı.**

## 2 · Nerede kaldık — 23 Eylül 2026

**Üç taban protokol KAPALI** — aynı 12 hücrede (dört `-yok` kolu × tohum
1000–1002), aynı ETX kâhinine karşı U1 kapısından geçti:
`AODV-e` (K-145) · `OLSR-b` (RFC 3626 §13 ile, K-146 · K-147) · `AOMDV-a`
(makale + RFC 3561, K-148 · K-149). Kod hâli etiketleri ve kayıtlar
`DEVIR.md` §2'de; hüküm saniyeler içinde yeniden üretilir:
`python -u kalibrasyon/aodv_uygunluk.py hukum ciktilar2/aodv_uygunluk/<protokol>_son.json`.

**DESPARETE** — öğrencinin v0.1 tasarım paketi:
`protokol_kaynaklari/DESPARETE_TASARIM_PAKETI/` (40 dosya; tek okuma: `36`,
sayılar: `35` M0.1 · `21` zamanlama · `19` tel biçimi · `23` algoritmalar ·
`22` durum makineleri). İnceleme ve öğrencinin kararları **K-150**'de:

- ana karşılaştırmada güvenlik (Ed25519) KAPALI, bayt bedeli ayrı kolda
- yedekli gönderim (PROTECT kopyası) ilk gerçeklemede YOK
- komut trafiği (geçitten düğümlere) için **isteğe bağlı hedef alanı**;
  alanlar koşu boyunca emekliye ayrılmaz
- CAUTION'a girişte seçili ardıla bir kez sınırlı doğrulama oturumu
- DFSN_REQUEST tek yayın; PROBE/PROBE_REPLY unicast; FIELD_UPDATE yayın
- v0.1 YAZILDIĞI GİBİ gerçeklenir; iki açık soru (boşta sondalama yükü ·
  belirsizlik eşiği ↔ sondalama hızı) önce ÖLÇÜLÜR, değişiklik v0.2'de
- U1'i YERE TOPLAMA deseninde koşulur (v0.1 eşler-arası yönlendiremez)

**`sim2/` K-151 Y1 · Y2 — 🟢 KAPANDI (23 Eylül, K-151 §6 · §7).** Y1 her
unicast sonucunu tekrar sayısıyla isteyen protokole bildirir
(`SonucBildirimliProtokol.iletim_sonucu`); Y2 protokolün veri başlığını
(`veri_baslik_bayt`) ödetir ve yönlendirme ek yüküne (`nrl_*`) sayar.
Kapanış: `kosu.py` 152 → 143 kod satırı (beacon gönderimi `gonderim.py`ye) ·
`643 passed` · regresyon `k151` 45/45 (23,5 dk) · `k144 ↔ k151` önceden
yazılan beklentiyle BİREBİR, çıkış 0. Regresyon aletine `--sifir` ve K-151'in
iki yolunu sınayan `j-` vakası eklendi. ⚠️ Ad çakışması: K-151'in Y1 · Y2'si
`v2/07` §18'in Y1 (PSR) · Y2 (onay) adımlarıyla aynı adı taşır — "K-151 Y1"
diye anılır. O gün geçerli taban `k151`; **bugün `k157`** (aşağıda, K-157).

**DESPARETE — gerçekleme başladı (K-152):** M0.1 (`protokoller/desparete_metrik.py`)
ve mesaj biçimleri (`protokoller/desparete_bicim.py`) yazıldı, `74 passed`.
Belgenin iki hatası ölçüldü: TV-02 kurallarla 28 verir, belge 40 diyor ·
DFSN_REQUEST'in diyagramı 76 bayt, metni 72 — diyagram izlendi. Öğrencinin
23 Eylül yanıtları K-152 §1'de: depo herkese açık değil · DESPARETE taslak,
iyileştirmeye açık (nasıl uygulandığı K-152 §1) · UNREACHABLE'dan çıkış
ajana devredildi (K-152 §2) · tampon kotası ölçülecek (K-152 §3).

**Devam — DESPARETE'nin gerçeklenmesi**, bu sırayla, her parça kendi testiyle:
biçimler 🟢 → M0.1 🟢 → komşu yaşamı → alan / FD / DFSN → edinim ve onarım
(isteğe bağlı hedef alanı dâhil) → postürler. 🔒 İlk entegrasyon koşusundan
(küçük dünyada bile) ÖNCE ön-kaydın §0.3 adım 3'ü — **yazıldı** (`v2/06`
§0.4, K-153) ve öğrenci aday birincil hücreyi seçti: **formasyon · yere
toplama · `hava_eslik` · sürekli · PDR · `Δ_hedef = 0,05`**. 3.3 komşu yaşamı
(`desparete_komsu.py`, K-154), 3.4 alan ve ardıl (`desparete_alan.py`,
K-155) ve 3.5 edinim ve onarım (`desparete_edinim.py`, K-156) bitti;
3.6 postürler (`desparete_politika.py`, K-158) ve 3.7 ablasyon bayrakları
(`desparete_bayrak.py`, K-159) de bitti. 🔴 3.8 kabul kapısında tam ölçekte
çöküş ölçüldü (K-160 §6–§9): sebep komut hedeflerinin alanları (K-150 §4 A);
🟢 öğrenci **C**'yi seçti (K-160 §12) — v0.1 yalnız geçit alanıyla, komutlar
düşer; A `komut_alanlari=True` ile duruyor. C ile de hareketli kollar
çöktüğü için öğrenci **v0.2 yalın profili** seçti (K-161); ardından test
öncesi iyileştirme (K-162 analiz) → **v0.3** = v0.2 + V1 + V5 + V7
(K-163 · K-164): DESPARETE'nin varsayılanı `PROFIL_V02` + `SECENEK_V03`;
v0.2 = `secenekler=SECENEK_YOK`, v0.1 = `bayraklar=PROFIL_V01,
secenekler=SECENEK_YOK`. V5a ve V2+ benimsenmedi (K-164 · K-165). U1'in
sayısal koşumu (5–7 sa) öğrencinin iznini ister. 🔴 **25 Eylül — bağımsız
denetim (K-166, rapor `DENETIM-RAPORU-2026-09-25.md`):** v0.3'te V5 edinim
yolunu kapatıyor (geçit kimseyi, röle aşağıdaki komşuyu nitelendirmez →
FIELD_SOLICIT ve DFSN_REQUEST kabul kapısında düşer, tur hiç artmaz); uzun
pencerede v0.3 formasyonda v0.2'nin gerisinde. 🟢 **K-167: öğrenci
çözümü ajana bıraktı → DESPARETE v0.4 = v0.3 + V8 + V10 VARSAYILAN**
(küçük dünyada v0.2'nin teslimi, yükünün ~yarısıyla; tam ölçekte
doğrulanmadı — sıradaki iş, öğrencinin izniyle). ⚠️ Öğrenci (25 Eylül):
**sorunları ajan ÇÖZER**, raporlayıp seçenek sunup beklemez; yalnız
kapsam/iddia/ön-kayıt metriği gibi fikrin değiştiği yerlerde önerisiyle
sorar. ⚠️ Koşu kimliği protokolü, profili, senaryoyu, trafik desenini ve
tehdit senaryosunu içermez (denetim Y-1) — düzeltmesine öğrenci onay
verdi (K-167 §1); yapı kodlamadan önce anlatılır. Paket kimliği gözlem yüzeyinde (`PaketGorunumu.
kaynak_sira`, kaynak başına sıra; küresel kimlik bilerek açılmadı) ve
DESPARETE'nin alan başına tampon kotası (6) yazıldı — `k151 ↔ k157` birebir,
geçerli regresyon tabanı `k157` (K-157). ⚠️ Simülatör testleri her
kancadan sonra döngüsüzlüğü denetler (`tests2/test_desparete.py`
`_desparete_kos_denetimli`) — yeni parçalarda da korunmalı. Tam yol haritası
ve "şu an neredeyiz": `v2/12` §5. Döngüsüzlük değişmezleri her olaydan sonra
denetlenmeli (örnek: `arsiv/teshis/aomdv_s10_2026-09-22/degismez_denetimi.py`).
Tampon: tasarımın 6 s'si onarım üst sınırıyla aynı — onarım bitiminde bir
`Uyandirma` tampondakileri yeniden sordurur ve düşürür.

**Temizlik (23 Eylül, öğrenci kararı — bağlam kirliliğini önlemek için; hiçbir
şey SİLİNMEDİ, taşındı):** K-001…K-089 → `v2/arsiv/04-NEDEN-BOYLE-K001-K089.md`
· eski denetim raporu ve teknik referans → `arsiv/` · eski kaynak listesi →
`v2/arsiv/` · literatür taraması → `protokol_kaynaklari/literatur_taramasi_2026-08-31/`
· 19 eski regresyon tabanı → `arsiv/regresyon_tabanlari/` (geçerli taban
23 Eylül'den beri `ciktilar2/regresyon/k157.jsonl`; `k151` bir önceki). `arsiv/` klasörlerini ancak bir tarihi
doğrulaman gerekirse aç.

## 3 · Okuma sırası

| # | belge | neden |
|---|---|---|
| 1 | `DEVIR.md` §1–§2 | durum ve doğrulama listesi (her maddenin komutu ve beklenen değeri) |
| 2 | `v2/04-NEDEN-BOYLE.md` — **K-150 … K-166** | son kararlar; defter baştan okunmaz, sondan geriye (K-166: bağımsız denetimin değerlendirmesi) |
| 3 | `v2/12-YOL-HARITASI.md` | aşamalar ve açık borçlar |
| 4 | `v2/07` §15 | öğrenci kararlarının TEK listesi |
| 5 | `v2/03-YONTEM-KURALLARI.md` §1 | çalışma anlaşmaları ve gerekçeleri |
| 6 | `v2/06-ON-KAYIT.md` | ön-kayıt: hipotezler, metrikler, U1–U4, sadakat protokolü |
| 7 | `v2/05` · `v2/13` | protokolün görebildikleri ve yapabildikleri |
| 8 | `protokol_kaynaklari/` | birincil kaynaklar (RFC 3561, RFC 3626, AOMDV makalesi) ve DESPARETE paketi |

## 4 · Çalışma anlaşmaları — kısa

`git` artık var ama **git komutlarını yalnız öğrenci çalıştırır** — salt-okur
olanlar (`status`, `log`, `ls-files`) dâhil · **dosya kalıcı olarak
SİLİNMEZ**; eskiyen belge `arsiv/`e taşınır (arşiv git'in dışında) · öğrenciyle
Türkçe, kısa ve kod referanssız özet · `sim2/`de yapısal değişiklikten önce
yapıyı anlat, onay al · 30 dakikayı aşacak koşumdan önce sor, süreyi bant
olarak ver · havuz varsayılanı **8 işçi** (öğrenci, 21 Eylül) · raporlanan
her sayının üretici komutu yazılır · ölçütler ölçümden ÖNCE ilan edilir,
sonra değiştirilmez · regresyonun beklenen farkı karşılaştırmadan ÖNCE yazılır
· **bir iş bitirilir, sonra ölçülür** (uzun kapılar yalnız kapanışta, bir kez;
kapanış betiği test kalırsa durmalı) · protokoller sırayla kapatılır · her
Python çağrısında `PYTHONIOENCODING=utf-8`, `Pool` kullanan betikte `__main__`
koruması, iç içe havuz ve stdin'den Python yok · uzun metin dosya yazma
aracıyla, heredoc'la değil · CRLF dosyalarda satır sonu korunur · indirme
izinle ve belge depoya girmeden önce TAMAMI okunur (istem enjeksiyonu
denetimi — `protokol_kaynaklari/README.md`) · paket kurulmaz.
Ayrıntı: `v2/03` §1.

## 5 · Bu projenin teşhis alışkanlıkları

- Bir ölçüm aletine, ölçtüğü şeye güvendiğinden daha az güven.
- Bir açıklama bir hücrenin neden EN DÜŞÜK olduğunu gösterir, kusur olmadığını
  değil (K-145) — mümkünse nedensel ölç (sebep kaldırılınca geçiyor mu?).
- Bir protokolün kusuru öbürünün aynasında görünür: aynı hücrede yan yana koş
  (K-143 · K-146).
- Bir makalenin şekli, altındaki protokolün durum makinesini varsayar;
  *"harfiyen"* yanlış olabilir (K-148 S10).
- "Ölçtüm, etkisi yok" ile "ölçemedim" ayrıdır.

Tam liste: `v2/03` §2.1.

## 6 · Açık borçlar (mühürden önce)

40 `SINANMAMIS` parametre · 9 duyarlılık borcu · `algilama_duyarliligi`nin
ikiye bölünmesi · ana deneyin koşum bütçesi ve hücre seçimi · OLSR §13'ün
hareketli kolda mekanizması (ölçülmedi) · AOMDV'nin bayat yedek yolu (S2) ·
DESPARETE'nin güvenlik kolu ve yedekliliği · Philox üreteci seçeneği (alınmadı).

> **Bir şeyi iddia etmeden önce ölç. Ölçemiyorsan iddia etme.**
