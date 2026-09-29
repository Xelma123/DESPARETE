# 15 · GERÇEKÇİLİK YAPI PAKETİ — `sim2/` değişikliklerinin anlatımı (Faz 1–3)

> **Durum: 🟢 ONAYLANDI (KR-B, K-170)** — öğrenci, 25 Eylül 2026: *"önceki yapı paketini onaylıyorum"*; regresyon izni ve §F.3 sayıları dâhil. Kod adım adım §E sırasıyla yazılır. Dayanak: `v2/14` (onaylı referans dünya, K-169) · plan `v2/12` Faz 1–3 · kural `07` §18.
> **Neden tek paket:** her `sim2/` değişikliği regresyon ve kalibrasyon ister; tek tek yapılsaydı her biri için ayrı yeniden kalibrasyon gerekirdi. Paket bir kez anlatılır, adım adım yapılır, sonunda bir kez yeniden kalibre edilir (Faz 4).

---

## 0 · Çalışma biçimi — güvenli geçiş

🔒 **Her mekanizma, varsayılanı BUGÜNKÜ davranış olan bir anahtarla gelir** (`07` §18 kuralı: "varsayılan = bugünkü davranış"). Her adımdan sonra:
1. tam test takımı;
2. regresyon `uret` + `karsilastir <geçerli taban> <yeni>` → **BİREBİR** (yalnız ilan edilmiş kimlik ve şema alanları değişir). Geçerli taban `k171` (A1'den sonra; önce `k157`).

Bu, yeni kodun eski dünyayı kazara bozmadığının kanıtıdır. En sonda **tek bir "dünya değişimi" adımı** bütün anahtarları `v2/14`'e çevirir; beklenen farklar o adımda önceden yazılır. Faz 4 (yeniden kalibrasyon) oradan başlar. Eski dünya aynı kodla yeniden üretilebilir kalır.

**Korunan değişmezler:** gözlem sızıntısızlığı (protokol karıştırıcıyı ve gerçek bağ kalitesini göremez) · korunum defteri · hash tabanlı belirlenimcilik (aynı tohum = aynı dünya, protokolden bağımsız) · kâhin ile gerçek alım aynı PER gövdesini kullanır · bit hızı aritmetiği yalnız `cerceve_kur`'da · her yeni sabit köken defterinde kovasıyla.

---

## A · Fizik ve MAC (Faz 1)

### A1 · Sonuç satırı ve kimlik — İLK adım (eski İ-1) · ✅ YAPILDI (K-171: 830 passed · `k157 ↔ k171` 45/45 birebir)
- **`kosu_kimligi`:** tedavi alanlarının özeti + protokol parmak izi (ad + `protokoller/` kod özeti + protokolün bildirdiği parametreler; DESPARETE'de bayrak ve seçenek demeti) kimliğe girer; satıra `tedavi_hash` ve `protokol_hash` alanları. Araç özetinde CRLF normalizasyonu.
- **PDR yön ayrımı:** telemetri (geçide) ve komut (geçitten) PDR'si ayrı, pencere ve tüm koşu.
- **Politika düşmesi:** yeni düşme sebebi `politika` (C kararıyla düşen komutlar `hedef_yok`tan ayrılır; protokol `Beyan("politika")` döndürür).
- **Regresyon matrisi:** AODV · OLSR · AOMDV · DESPARETE birer kısa vaka.
- *Neden ilk:* sonraki her koşunun satırı ayırt edilebilir olsun.
- *Kapı:* "farklı koşu → farklı kimlik" testi; regresyonda yalnız kimlik/şema alanları.

### A2 · DSSS işlem kazancı — anahtar `islem_kazanci` (varsayılan kapalı) · ✅ YAPILDI (K-173)
- Açıkken gürültü 22 MHz'de, NF 7 dB; BER'in girdisi Eb/N0 = SINR · (B / bit hızı), B = 22 MHz: 1 Mb/s ×22 (önbelge), 2 Mb/s ×11 (gövde); girişim ve karıştırma gürültü gibi SINR'a girer (G1, G2). 🔴 *Düzeltme (K-173):* önceki metin "11 Mchip/s / bit hızı" diyordu — o 2 Mb/s'e ×5,5 verirdi; yanındaki çarpanlar (×22, ×11) ve ns-3 doğruydu, formül değil.
- Anahtar açıkken `bant_genisligi_hz` = 22 MHz zorunlu (konfig doğrular); NF 7 dB'ye geçiş A7'de. Çarpanlar `cerceve_kur`da hesaplanır, çerçeveyle taşınır (bit hızı aritmetiğinin tek yeri; A4'e hazır).
- *Ölçülen kapı:* gövde eşikleri ns-3'ten en çok 0,05 dB · önbelge birebir · 2 Mb/s duyarlılığı −92,5 dBm (`arsiv/teshis/a2_islem_kazanci_2026-09-26/`).
- Tek PER gövdesi (`Kanal.per`) korunur; kâhin de aynı yolu kullanır.
- *Kapı:* PER–SNR eğrisi, Pei & Henderson'ın formülleriyle sayısal olarak örtüşür (yayın karşılaştırması); kapalıyken birebir.

### A3 · Güce dayalı taşıyıcı dinleme ve ED-CCA — anahtar `tasiyici_dinleme` = `geometrik` (bugün) | `guc` · ✅ YAPILDI (K-174; önbelge sezme = alıcı kilidi, eşik PER'den türer)
- **Önbelge sezme:** bir çerçeve, alınan gücü önbelge sezme eşiğinin (1 Mb/s duyarlılığı, TÜRETİLMİŞ) üstündeyse duyulur → bu düğüm donar ve alım dener. Bugünkü "duyanlar kümesi" mesafeden değil güçten kurulur; mesafe yalnız hesap budaması olarak kalır.
- **Enerji sezme (ED):** karıştırıcının bu düğümdeki gücü ED eşiğini (−76 dBm, G2) aşıyorsa kanal meşgul. Bugün yalnız aldatıcı sınıf için var olan makine (`karistirici_mesgul_mu` · `mesgul_bitisi_s` · açılma/kapanma anlarında uyanma) **bütün sınıflara** genellenir.
- **Hareketli karıştırıcı:** gücü sürekli değiştiği için, karıştırıcı yüzünden donmuş düğümlere kısa aralıklı yeniden denetim olayı (öneri 10 ms; 200 km/h'de 0,55 m — TÜRETİLMİŞ). Olay sayısı yalnız donmuş düğümlerle sınırlı.
- `cca_s` gerçekten kullanılır (802.11b aCCATime ≤ 15 µs, G2).
- *Kapı:* sürekli karıştırıcı yanında vericinin ertelediğini gösteren analitik sınav; Bianchi ±%15 (tek çarpışma alanında); geometrik kipte birebir.

### A4 · Hız uyarlaması — anahtar `hiz_uyarlamasi` (varsayılan kapalı, **ilk düşecek madde**) · ✅ YAPILDI (K-177; kaynak ns-3 ARF, G14)
- 1 / 2 / 5,5 / 11 Mb/s; komşu başına basit bir kural (ARF: art arda başarı → yukarı, art arda başarısızlık → aşağı; **kaynak bekleniyor**). Bütün protokollerde aynı MAC.
- Yayınlar ve onaylar temel hızda (1 Mb/s; standart bekleniyor). `Cerceve` bir hız alanı kazanır; bit hızı hesabı yine yalnız `cerceve_kur`'da.
- *Kapı:* tek bağda SINR'a göre hız seçimi; kapalıyken birebir.

### A5 · Zamanlama — anahtar `yayilim_gecikmesi` (varsayılan kapalı) · ✅ YAPILDI (K-175; yeniden deneme sınırı 7 A7'de)
- Alım olayları alıcıya `d/c` gecikmeyle ulaşır; taşıyıcı dinleme de gecikmeli başlar; onay zaman aşımı en uzak bağın gidiş-dönüşünü kapsar.
- Girişim hesabı gönderim anlarıyla yapılır; hata ≤ 7 µs / 2,5 ms'lik çerçeve (beyanlı).
- `yeniden_deneme_siniri` bir Konfig alanı olarak zaten var: yeni dünyada 7 (standart bekleniyor, S2).

### A6 · Karıştırıcı gerçekçiliği — anahtar `karistirici_gercekci` (varsayılan kapalı) · ✅ YAPILDI (K-176; EIRP A7'de)
- Karıştırıcı bağlarına hızlı sönümleme (UAV bağlarıyla aynı model).
- Yer karıştırıcıları yerde (1,5–5 m) ve Al-Hourani yer–hava kanalıyla (G6): görüş hattı olasılığı yükseklik açısından; görüş hattı durumu hash'ten, zaman dilimli.
- Reaktif karıştırıcının duyma menzili (güç eşiği) ve algılama olasılığı köken defterine.
- Aldatıcı karıştırıcının sahte çerçeveleri havaya gerçek çerçeve olarak çıkar: alıcıyı kilitler, sonra "çözülemez" diye düşer (G5).
- Güçler EIRP olarak (`v2/14` §4).

### A7 · Referans dünyanın girdileri — anahtar `dunya` = `olcek_1_50` (bugün) | `referans_2026` · ✅ YAPILDI (K-178; `kanal/dunya.py::referans_2026`, alıcı dipol kazancı eklendi)
- **Verici gücü girdi olur** (EIRP 20 dBm, KAYNAK), menzil sonuç. Bugün menzilden türetiliyor; `iletim_menzili_m` yerine türetilmiş bir "nominal bağ menzili" (10 dB paylı, `bag_butcesi.py` ile aynı hesap) yerleşim kurallarına girdi olur.
- Alan, irtifa, hızlar, düğüm sayısı `v2/14` §3'ten; `olcek` 1'e iner.
- `sinr_esigi_db` (16 dB) kullanımı: fiziksel kopma sayımı ve kâhin bağ kümesi, işlem kazançlı PER modelinin eşiğinden **türer**.

### A8 · Dünya değişimi — paketin son adımı · ✅ YAPILDI (K-181; `referans_2026` bütün anahtarlar açık, `Konfig` varsayılanı eski dünya)
- Bütün anahtarlar `v2/14`'e çevrilir; beklenen farklar ÖNCEDEN yazılır (bütün metrikler değişir; korunum ve mutabakat kapanmaya devam eder).
- Yeni regresyon tabanı → Faz 4 başlar.

---

## B · Gözlem sözleşmesi v2 (Faz 2) — gerçek telsiz ve otopilot ne veriyorsa

### B1 · Yeni isteğe bağlı kanca `cerceve_duyuldu` · ✅ YAPILDI (K-172, §E sırasından önce — komut düzeltmesi gerektirdi)
- **Çağrılma:** başarıyla çözülen **her** çerçevede — bana ya da başkasına adresli; veri, onay, kontrol, beacon.
- **Argümanlar:** `(gozlem, gonderen, tur, hedef, rssi_dbm, paket)`; `paket` veri çerçevesinde başlık görünümüdür.
- **Niyet döndürmez.** `iletim_sonucu` gibi isteğe bağlıdır; hepsi-ya-hiç kuralına girmez. Kullanmayan protokolde hiçbir şey değişmez; bugünkü dört protokolün satırı birebir kalır.
- **Gerçek karşılığı:** telsizin izleme kipi ve sürücünün çerçeve başına RSSI raporu.
- **Yeri:** bugün başkasına adresli çerçevenin sessizce bırakıldığı yer (teslim ve kontrol kodu). Alıcı çerçeveyi fiziksel olarak zaten çözüyor.

### B2 · RSSI · ✅ YAPILDI (K-172; hata `kanal_karar` alanından `rssi` anahtarıyla, tamsayı dBm)
- Alıcının kilitlendiği güç (bugün alıcı zincirinde tutuluyor) + ölçüm hatası.
- Hata öneri: σ = 2 dB; **kaynak aranacak**. Çekim hash'ten, belirlenimci.
- dBm cinsinden, telsizin raporladığı gibi.

### B3 · Gözlemin yeni alanları · ✅ YAPILDI (K-179; `kendi_konum`/`kendi_hiz`, doluluk isteğe bağlı)
- `konum` ve `hiz` (x, y, z · vx, vy, vz): kendi GPS/INS'i. Yatay hata 1,5 m CEP (G7; eksen başına σ ≈ 1,3 m), dikey σ 2 m (öneri). Hata hash'ten, 1 Hz tazelenir.
- `mesgul_sure_s`: CCA'nın meşgul kaldığı toplam süre. Bir sayaçtır; protokol oranı kendi penceresinde hesaplar (gerçek sürücüler de "channel busy time" sayacı verir).
- `phy_hata`: sezilen ama çözülemeyen çerçevelerin (önbelge ya da CRC hatası) toplam sayısı.
- `alinan_cerceve`: başarıyla çözülen çerçevelerin toplam sayısı.

### B4 · Belge ve testler · ✅ YAPILDI (K-180; yüzey 29 alan)
- `v2/05` yeniden yazılır: her alan için "gerçek telsiz ya da otopilot bunu verir mi" ve kaynağı.
- Yüzey testi 12 · 6 · 6 → yeni sayılar.
- **Sızıntı testi korunur:** yeni alanların hiçbiri karıştırıcının yerini, gücünü ya da açık/kapalı durumunu doğrudan taşımaz. `mesgul_sure_s` karıştırıcının **enerjisini** içerir; bunu gerçek telsiz de ölçer.

---

## C · Senaryo eksenleri (Faz 3)

### C1 · Düğüm kaybı — tedavi alanı `dugum_kaybi` (varsayılan: yok) · ✅ YAPILDI (K-180; ölüm kendi çerçevesinin varışına ertelenir)
- **Konfig:** kaybın sayısı ve zaman penceresi. Hangi düğümlerin düşeceği hash'ten seçilir; geçit düşmez.
- **Kayıp anında:** telsiz kapanır (gönderim yok, alım yok). Kuyruktaki ve uçuştaki paketler yeni `dugum_kaybi` sebebiyle düşer.
- **Korunum:** yeni sebep defterin düşme kalemine girer; denklem kapanmaya devam eder.
- **Protokol haberdar edilmez.** Gerçekte de edilmez; bunu komşularının sessizliğinden anlar.

### C2 · Trafik yoğunluğu · ✅ YAPILDI (K-180)
- Mevcut hız alanları (`telemetri_paket_hizi_hz` vb.) köken defterinde TEDAVİ ekseni olarak ilan edilir. Yeni kod yok.

### C3 · Enerji · ✅ YAPILDI (K-180)
- Düğüm başına gönderim süresi, alım (kilitli) süresi ve dinleme süresi toplanır. Bu üçünün toplamı koşu süresine eşit olmak zorunda; bir değişmez olarak denetlenir.
- **Enerji** = P_tx · t_tx + P_rx · (t_alım + t_dinleme). Güçler G7'den: gönderimde 10,6 W, alım ve dinlemede 2 W.
- **Satırda:** ağ toplamı ve düğüm başına dağılım (p50, p95, en büyük).

---

## D · Bu pakette OLMAYANLAR (sonraki kendi paketleriyle)

- **PROTECT kopyası:** kararın ikinci atlamaya kopya taşıması, korunum defterinde kopya kalemi, hedefte tekilleştirme. DESPARETE'nin ihtiyacı netleşince Faz 5.4'te ayrı bir yapı anlatımıyla.
- **DATA başlığında protokol alanları:** potansiyel taşıma. Faz 5.5'te ayrı bir yapı anlatımıyla.
- **Taban protokollerin adillik düzeltmeleri:** RREP-ACK/kara liste, `protokoller/`. Ölçüme göre Faz 4.3'te.

---

## E · Sıra, süre, kapılar

| adım | içerik | süre (tahmin, ajan) | kapı |
|---|---|---|---|
| 1 | A1 sonuç satırı ve kimlik | 0,5–1 gün | kimlik testi · regresyon: yalnız ilan edilmiş alanlar |
| 2 | A2 işlem kazancı | 0,5 gün | PER–SNR yayın karşılaştırması · kapalıyken birebir |
| 3 | A3 güce dayalı dinleme + ED-CCA | 1,5–2 gün | ED analitik sınavı · Bianchi · geometrikken birebir |
| 4 | A5 zamanlama · A6 karıştırıcı | 1–1,5 gün | birim sınavları · kapalıyken birebir |
| 5 | A4 hız uyarlaması | 1 gün | tek bağ sınavı · kapalıyken birebir (takvim sıkışırsa düşer, beyan) |
| 6 | A7 referans dünyanın girdileri | 0,5–1 gün | bağ bütçesi testi (`bag_butcesi.py` ile aynı sayılar) |
| 7 | B gözlem v2 | 1–1,5 gün | yüzey · sızıntı · kanca yalnız çözülen çerçevede · birebir (eski protokoller) |
| 8 | C düğüm kaybı · enerji · yoğunluk | 1 gün | korunum ve enerji zaman değişmezi · kapalıyken birebir |
| 9 | A8 dünya değişimi | 0,5 gün | beklenen farklar önceden yazılı · yeni regresyon tabanı |

**Toplam:** ~8–11 iş günü (ajan).
- Her adımdan sonra tam takım (~13 dk) ve regresyon üretimi (~35–45 dk). Regresyon 30 dakikayı aşar ve adım başına gerekir → **tek seferlik izin** isteniyor: "her yapı adımından sonra regresyon".
- **Takvim:** plandaki Faz 1–3 (2–12 Ekim) biraz aşılabilir. Kayma sırası: önce A4, sonra A6'nın yer–hava kısmı; ikisi de beyan edilir.

## F · Senden istenen kararlar (KR-B)

1. Paketin tamamı ve çalışma biçimi (§0: önce anahtarlar varsayılan kapalı, en sonda tek dünya değişimi).
2. Her yapı adımından sonra regresyon (~35–45 dk) için tek seferlik izin.
3. Önerilen üç sayı:
   - RSSI ölçüm hatası σ = 2 dB;
   - dikey GPS σ = 2 m;
   - hareketli karıştırıcının yeniden denetim aralığı 10 ms.

   Kaynak bulunursa kaynağınki geçerli.
