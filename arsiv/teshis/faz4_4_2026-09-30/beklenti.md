# Faz 4.4 #1 · referans dünyanın eşleştirilmiş çözünürlüğü R — beklenti (ölçmeden önce)

> 30 Eylül 2026 12:15 · ajan · plan `arsiv/teshis/faz4_kapanis_2026-09-30/denetim.md` (4.4 tablosu #1) · öğrenci sırayı onayladı (K-204).
> Komut (dondurulmuş kopya `kopya/`, 8 işçi, yanında ağır iş yok): `py -3.11 -u kalibrasyon/cozunurluk.py --dunya referans_2026 --tohum 40` · ~30 dk

## Ne için

1. **Duyarlılık taraması** (4.4 #3–#6): `R = 2 · SD_tohum(ölçüt bedeli) / √40`, iki kâhinin aynı tohumdaki eşleştirilmiş farkından. Saklanan `duyarlilik.py::R_ESLESTIRILMIS = 0,0230` ESKİ dünyanın; araç bayatsa söyler.
2. **AOMDV'nin kâhin aşımı** (K-192 b, K-205): eşler arası formasyon 1000'de AOMDV 0,9777 · kâhin 0,9762 → **+0,0015**. Karar kuralı: aşım ≤ R ise "çözünürlük içinde, aşım sayılmaz" → U1-U geçer. Aşım > R ise üç kâhinin zarfına bakılır (aynı hücrede `en_kisa_yol_kahin` ve üçüncü kâhin); zarfı da aşıyorsa yazılım hatası aranır.

⚠️ R kol düzeyinde (40 tohumlu ortalama) bir görünürlük eşiğidir; tek hücrenin aşımıyla karşılaştırmak K-192 (b)'nin kuralıdır (öğrenci onaylı). Aşım çok küçük olduğu için sonuç büyük olasılıkla "R içinde" çıkar; yine de R ölçülmeden hüküm verilmez.

## Sonuç 1 (12:15) — R bu hücrede KULLANILAMAZ

`cozunurluk.txt`: R (eşleştirilmiş) = 0,0086 · pdr_etx ortalama **0,0287**. Aracın hücresi (statik-sürekli, kısa pencere, tek merkez karıştırıcı) eski dünyanın çekirdek hücresidir. Referans dünyada bu hücrede kâhin bile %3 teslim ediyor: taban etkisi, R yapay küçük. `R_ESLESTIRILMIS` güncellenmez. **4.4 planı düzeltilmeli:** "statik" duyarlılık hücresi de aynı tabanda (sahte DUYARSIZ riski); çalışma noktası birincil hücre.

## AOMDV — K-192 (b)'nin ikinci adımı (R geçerli ölçülemediği için doğrudan)

`aomdv_zarf.py` · aynı hücrede üç kâhin (ETX · en kısa yol · en olası teslim), U1'in konfigürasyonuyla. **Kural:** AOMDV (0,9777) ≤ zarf → "ETX kâhini bu hücrede üst sınır değil" beyanı, U1-U geçer · AOMDV > zarf → yazılım hatası aranır. Tutarlılık: ETX kâhini 0,9762'yi birebir üretmeli. ~40 dk, 3 süreç.

## Sonuç 2 (12:32) — AOMDV zarfın içinde ✅

`aomdv_zarf.txt`: ETX kâhini 0,9762 (U1'le birebir ✅) · en kısa yol 0,8861 · **en olası teslim 0,9986** → zarf 0,9986 ≥ AOMDV 0,9777. K-192 (b): "ETX kâhini bu hücrede üst sınır değil" beyanı; U1-U geçer. U1 aracında `KAHIN_ASIMI_ACIKLANMIS` (desen başına, ölü kayıt taramalı; test `test_K192b_KAHIN_ASIMI_ZARF_KAYDI`). Hüküm: AOMDV eşler arası U1-U 🟢; U1-B'de statik 1002 (0,889) keşifsel bulgu olarak kalır.

## Faz 4.4 yeniden — birincil hücrede (öğrenci onayı K-207 §4; plan `faz4_kapanis_2026-09-30/denetim.md` 4.4 notu)

> 2 Ekim 07:0x · ajan · taban protokoller dondu (K-211). Komutlar dondurulmuş kopyadan, sırayla, yanında ağır iş yok.

**R** · `py -3.11 -u kalibrasyon/cozunurluk.py --dunya referans_2026 --hucre birincil --tohum 40` (80 koşu, kâhin ikilisi, kısa pencere).
- Ön koşul: kâhinin hücre ortalaması PDR'si 0,1 ile 0,95 arasında olmalı (taban ya da tavan değil). Değilse R kullanılmaz.
- Sonuç `duyarlilik.py::R_ESLESTIRILMIS` sabitine yazılır (köken kaydı ÖLÇÜLMÜŞ, üretici bu komut). Eski dünyanın 0,0230'u arşiv notunda kalır.

**T1 · T2 · E** · `py -3.11 -u kalibrasyon/duyarlilik.py --dunya referans_2026 birincil <adlar>` (5 tohum, çarpanlar 0,5 · 2). Ölçüt aracın kendi kuralı:
- DUYARSIZ ⇔ |Δ| < R **ve** kendi hata payının içinde.
- Parmak izi birebir aynıysa "ÖLÇÜLEMEDİ" (DUYARSIZ değil).
- Duyarlı çıkan ve kaynağa bağlanamayan → öğrenciye eksen listesi.

## Sonuç 3 (08:09) — R birincil hücrede ✅

`faz4_4_birincil_2026-10-02/cozunurluk.txt` (07:02–08:09, kopyadan):
- pdr_etx 0,8342 (SD 0,0516) · pdr_atlama 0,6770 (SD 0,0723) · `olcut_bedeli` 0,1572 (SD 0,0595)
- **R (eşleştirilmiş) = 0,0188** · tek kol R'leri 0,0163 · 0,0229
- Ön koşul sağlandı: kâhin PDR'si 0,834, taban da tavan da değil.
- `duyarlilik.py::R_ESLESTIRILMIS` 0,0230 → **0,0188** (eski dünyanın değeri, 15 Eylül, K-128; aracın bayatlık kapısı kırmızı yanmıştı, sapma 0,0042). Köken kaydı ÖLÇÜLMÜŞ, üretici yukarıdaki komut.

**Taramadan önce düzeltilen (ölçmeden):** `kahin.py::ATLAMA_ESIGI = 0,90` bir olasılık eşiği. Düz çarpımla ×2 → 1,8 olur, hiçbir bağ geçmez, en kısa yol kâhini boş grafikte koşar. Araçta olasılık eşikleri için kural: çarpılan tolere edilen kayıp payı (1 − p), yani ×0,5 → 0,95 · ×2 → 0,80 (`OLASILIK_SABITLERI`, test `test_OLASILIK_ESIGI_kayip_payindan_oynatilir`). Ayrıca not: `rician_k_db` ve `yakalama_esigi_db` dB'de düz çarpılıyor (10 → 5 / 20 dB), yani doğrusal ölçekte ×0,3 / ×10. Eski dünyanın taramalarındaki kural bu; oynatma büyük olduğu için DUYARSIZ hükmü bu iki parametrede güçlü, DUYARLI hükmü ise etkinin büyüklüğü için üst kestirim sayılır.

**Taramalar** `faz4_4_birincil_2026-10-02/taramalar.sh` (kopya_2'den, 08:14'te başladı, dört parti sırayla: T1a 6 · T1b 5 · T2 5 · E 3 parametre; 390 koşu, ~6 sa). Çıktılar aynı klasörde `T1a.txt` … `E.txt`, saatler `zaman.txt`.

## K kalemleri (kanıtla kapanacaklar) — 2 Ekim 08:30–09:10

- **`BEKLEYEN_UYANDIRMA_TAVANI`** · `py -3.11 arsiv/teshis/faz4_4_birincil_2026-10-02/k_kalemleri.py` (k204 satırları, simülasyon yok → `k_kalemleri.txt`). Kontrol düzlemi olan 21 satırın hepsinde tepe ≤ **22/256** (en yükseği DESPARETE; taban protokoller ≤ 9). Aşılırsa koşu deterministik durur, sonucu sessizce değiştiremez → ÖLÇÜLMÜŞ. DESPARETE Faz 5'te değişince regresyon satırlarından yeniden okunur.
- **`ttl_baslangic`** · önce ağın çapı: `ttl_cap.py` (kâhin grafiği, pencere boyunca 5 s'de bir, 5 tohum → `ttl_cap.txt`). Ölçüt (ölçmeden): döngüsüz en uzun yol ≤ 8 (TTL ×0,5 = 16'nın yarısı). **Sonuç: BFS 8 · ETX yolu 9 (tohum 1003) → ölçüt AŞILDI.** 16'nın altında, ama pay iki kat değil. Kâhinle taranamaz (kâhin döngü yapmaz; TTL yalnız veri paketinin ömrü) → taban protokollerle doğrudan ölçülür: `ttl_olcum.py` (AODV · AOMDV · OLSR × TTL 16 · 32 · 64 × 5 tohum + sınav protokolüyle kablo denetimi, 47 koşu, ~1,5 sa, taramalardan SONRA). Ölçüt betiğin başında yazılı: beş tohumda iz birebir aynı ve kablo denetimi geçiyorsa BAĞLAMIYOR; değilse |Δ| < R ve band içinde ise DUYARSIZ; aksi DUYARLI.
- **`gorev_grup_sayisi`** · yalnız görev kolu okuyor (`mobilite_kur`'da `kol == "gorev"`; formasyon okumaz) → birincil hücrenin kod yoluna girmez. Görev kolunun hücresi referans dünyada tabana yapışık olabilir (eski çekirdek hücre gibi), orada ölçülen bir DUYARSIZ geçersiz olur. Öneri: K-204'teki gibi **kapsam ilanı** (görev kolunun tanımı; o kolun sonucu 10 × 4'e koşullu). Öğrenci kararı.

## Sonuç 4 (14:03) — T1 · T2 · E taramaları

`faz4_4_birincil_2026-10-02/T1a.txt` · `T1b.txt` · `T2.txt` · `E.txt` (kopya_2; 107 · 91 · 91 · 58 dk). Taban dört partide aynı: pdr_etx 0,8401 · pdr_atlama 0,6664 · bedel 0,1737. GEÇERSİZ 0. Aracın kuralıyla (en büyük |Δ| üç çıktının büyüğü):

| hüküm | parametre (en büyük \|Δ\|/R · \|Δ\|/band) |
|---|---|
| DUYARLI, güçlü | `rician_k_db` (8,5R · 4,4×; 5 dB'de pdr_etx −0,126, 20 dB'de +0,077) · `SONUMLEME_ORNEGI` (3,2R · 14,7×; ETX kâhininin kendisi oynuyor) · `ATLAMA_ESIGI` (4,1R; pdr_etx birebir 0 — yalnız en kısa yol kâhini) |
| DUYARLI, sınırda (\|Δ\| ≤ 1,3R, band ≤ 1,8×) | `gm_adim_s` (yalnız ×2: 1,0R; ×0,5 0,2R) · `kanal_dilimi_s` (yalnız ×2: 1,3R; ×0,5 0,9R) · `yakalama_esigi_db` (0,7R ama band 1,6×; iki yön de aşağı) · `cbr_titresim_s` (yalnız ×2: 0,9R · 1,7×) · `ISTASYON_TUTMA_S` (1,1R · 1,1× iki yönde) · `beacon_araligi_s` (yalnız ×0,5: 1,1R · 1,8×) · `beacon_bayt` (0,8R · 1,2×) |
| duyarsız | `golgeleme_hucre_m` (×0,5: \|Δ\| 0,0185 = 1,0R'nin hemen altı · 0,7×) |
| ÖLÇÜLEMEDİ (iz birebir) | `gm_pitch_sigma_rad` (formasyon okumuyor) · `kuyruk_kapasitesi` · `saat_ofset_araligi_s` · `saat_sapma_ppm` · `komsu_omru_katsayisi` · `gps_dikey_sigma_m` · `gps_hiz_sigma_ms` · `rssi_olcum_sigma_db` |

Okuma notları:
- Araç kasıtlı kuşkucu: 5 tohumda 2 SE bandı ~%88 kapsar, üç çıktı × iki çarpanla tek bir bacağın şansla takılması olasıdır. "DUYARLI" çoğu sınırdaki kayıtta "aklanamadı" demektir; aracın kendi kuralı sınırdakileri `--tohum N` ile yeniden ölçmektir.
- `SONUMLEME_ORNEGI` kâhinin bağ başına ortalama başarı KESTİRİMİNİN örneklemidir (sayısal parametre): 3 → 6 → 12 örnekte pdr_etx −0,060 · 0 · +0,030, yani kâhin yakınsamamış. ETX kâhini U1'in paydası, G2ç'nin ve R'nin aletidir (statik kol hariç: orada tek örnek, ölçülmüş).
- `ATLAMA_ESIGI` köken metni yanlıştı ("ETX kâhinini belirler"): ETX kâhini eşik kullanmaz, ölçüm de bunu birebir gösterdi (d_pdr_etx 0,00000).
- ÖLÇÜLEMEDİ olanların kâhin koşusuna girmediği koddan da görülüyor: kâhinin zamanlayıcısı yok (saat), kuyruğu dolmuyor, komşu tablosunu okumuyor; GM eğimini formasyon kullanmıyor (bağımsız ve görev kolları kullanıyor); konumu ve RSSI'ı bugün hiçbir protokol okumuyor (DESPARETE'nin RSSI kancası argümanı kullanmıyor).

**Sonraki ölçümler (ölçüt betiklerin başında, ölçmeden yazıldı; TTL'den sonra sırayla, `kuyruk_2.sh`):**
- `sonumleme_yakinsama.py` — ETX kâhini, birincil + `bagimsiz-yok` (U1'in en sınırdaki hareketli hücresi), N = 6 · 12 · 24 · 48 × 5 tohum (40 koşu). N → 2N adımında |Δ| < R ve band içinde → plato.
- `protokol_tarama.py` — `kuyruk_kapasitesi` · `saat_ofset_araligi_s` · `saat_sapma_ppm` taban protokollerle (AODV · AOMDV · OLSR × taban + ×0,5 · ×2 × 5 tohum, 105 koşu) + DESPARETE'de konum/RSSI birebirlik (4 koşu). Kural TTL'inkiyle aynı.

## Sonuç 5 (15:20) — TTL taban protokollerle

`faz4_4_birincil_2026-10-02/ttl_olcum.txt` (kopya_2, 47 koşu, 77 dk). Kablo denetimi 🟢 (sınav protokolü 16 ↔ 32 izi farklı; TTL ölümü 109 ↔ 196).

| protokol | TTL 16 | TTL 64 | hüküm |
|---|---|---|---|
| AODV | birebir | birebir | BAĞLAMIYOR (TTL ölümü her koşuda 0) |
| AOMDV | Δ −0,0063 (band 0,0127) | Δ +0,0007 (band 0,0013) | DUYARSIZ (yalnız tohum 1003'te 1–3 TTL ölümü) |
| OLSR | Δ −0,0306 (band 0,0644) | **Δ −0,0790** (band 0,0679) | **DUYARLI** |

- **Hüküm (ölçüt gereği): `ttl_baslangic` DUYARLI** — yalnız OLSR üzerinden. OLSR birincil hücrede kalıcı döngüye giriyor (TTL 32'de 5 tohumda 1–57 TTL ölümü); TTL büyüdükçe döngüdeki paket havada daha uzun kalıp kanalı ve kuyruğu dolduruyor: TTL 64'te üç tohumda PDR 0,11–0,15 düşüyor. Tohumlar arası yayılım çok büyük (band ~0,065): OLSR bu hücrede kaotik.
- Kaynak bağı: 32 kaynaksız. IP'nin önerilen varsayılan TTL'i 64 (RFC 1700 "Assigned Numbers"; RFC 1122 oraya gönderir; ns-3 `Ipv4L3Protocol::DefaultTtl` ve Linux `ip_default_ttl` da 64 — bellekten, depoda doğrulanmış kopya YOK; indirme öğrenci izniyle). RFC 791 ve RFC 3626 yalnız TTL'in anlamını verir, değer vermez.
- → Öğrenci kararı: (a) kaynağa bağla (64; OLSR'ın birincil hücredeki PDR'si düşer, regresyon gerekir), (b) eksen, (c) 32 dünya tanımı + kapsam beyanı.

## Sonuç 6 (15:50) — kâhinin sönümleme örneği yakınsaması

`faz4_4_birincil_2026-10-02/sonumleme_yakinsama.txt` (kopya_2, 40 koşu, 30 dk). ETX kâhini, kısa pencere, 5 tohum:

| N | birincil pdr_etx | bağımsız-yok pdr_etx | koşu |
|---|---|---|---|
| 6 (bugün) | 0,8401 | 0,7895 | 6,5 · 4,9 dk |
| 12 | 0,8703 | 0,8203 | 6,6 · 5,0 dk |
| 24 | 0,8737 | 0,8437 | 6,6 · 4,9 dk |
| 48 | 0,8795 | 0,8540 | 7,0 · 4,3 dk |

- Adımlar: birincil 6→12 +0,030 (band 0,002) · 12→24 +0,003 PLATO · 24→48 +0,006 PLATO. Bağımsız-yok 6→12 +0,031 · 12→24 +0,023 (band 0,013, değişiyor) · 24→48 +0,010 (band 0,011) PLATO.
- **Ölçüt gereği en küçük platolu N: birincil 12, bağımsız-yok 24 → kâhin 6 örnekte YAKINSAMAMIŞ.** 6 → 48'de kâhinin teslim oranı birincilde +0,039, bağımsız-yokta **+0,065**.
- Maliyet yok: koşu süresi N'den bağımsız (grafik kurulumu koşunun küçük payı).
- Sonuç: bugünkü ETX kâhini kendi tanımının (her şeyi bilen, beklenen iletimi en aza indiren) altında kalıyor; U1 oranları ŞİŞİK (hareketli kollarda; statik kol tek örnekle ölçülür, etkilenmez). Örnek: AODV-i yere toplama bağımsız-yok 1000'in U1'i 0,604 (eşik 0,60) — kâhin %5–8 iyileşirse eşiğin altına iner.

## Sonuç 7 (18:37) — kâhinin göremediği parametreler taban protokollerle

`faz4_4_birincil_2026-10-02/protokol_tarama.txt` (kopya_2, 109 koşu, 167 dk).

- `kuyruk_kapasitesi`: AODV ve AOMDV iki yönde BİREBİR (kuyruk hiç dolmuyor), OLSR ×0,5'te Δ −0,0067 (band 0,0134), ×2'de birebir → **DUYARSIZ**.
- `saat_sapma_ppm`: AODV ve AOMDV iki yönde BİREBİR, OLSR ×0,5'te Δ +0,0042 (band 0,0083), ×2'de birebir → **DUYARSIZ**.
- `saat_ofset_araligi_s`: OLSR iki yönde BİREBİR; AODV ×2 Δ −0,0248 (band 0,0215), AOMDV ×2 Δ −0,0309 (band 0,0476) → ölçüt gereği **DUYARLI**. Tohum başına: bazı tohumlar birebir, bazıları iki yöne oynuyor (1001: ×0,5 +0,031, ×2 −0,030) — sistematik bir etki değil, bir kararın yerel saate bağlı olarak öbür yana düşmesi. OLSR'ın birebir kalması simülatörün saat sızdırmadığını gösteriyor → bağımlılık AODV'nin kendisinde.
- **Birebirlik (DESPARETE, GPS dikey · GPS hız · RSSI ×2): BİREBİR** 🟢 — bugün hiçbir protokol bunları okumuyor (kodda da öyle); Faz 5'te bir mekanizma okursa yeniden açılır.

**Ofsetin AODV'deki sebebi (aday):** başlangıç durumu yerel saatin 0 anına çapalı — `_son_yayin_s = -1.0` (HELLO, yerel saat 0'a kadar susar: negatif ofsetli düğüm açılışta |ofset| s HELLO gönderemez) ve §10 hız sınırı pencereleri `[0.0, 0.0]` (ilk "saniye" penceresi 1 + |ofset| s sürer). RFC 3561 §6.9: hiç yayın yapmamış düğüm için "son HELLO_INTERVAL içinde başka yayın yok" koşulu doğrudur; §10: "saniyede". Yama (`saat_cekirdegi_yama.py`): başlangıç −∞, ilk pencere ilk olayda açılır. Önce yamalı kopyada sınanıyor (`saat_dogrulama.py`; ölçüt betiğin başında: AODV ve AOMDV, 1001 · 1003, ofset 0,25 · 0,5 · 1,0 → iz birebir).

## Sonuç 8 (19:15) — AODV'nin saat bağımlılığının sebebi bulundu

`faz4_4_birincil_2026-10-02/saat_dogrulama.txt` (kopya_3 = bugünkü kod + `saat_cekirdegi_yama.py`, 12 koşu, 35 dk): AODV ve AOMDV, tohum 1001 ve 1003, ofset aralığı 0,25 · 0,5 · 1,0 s → **dört durumda da iz BİREBİR** 🟢. Ölçüt sağlandı: ofset bağımlılığının tek sebebi başlangıç durumunun yerel saatin 0 anına çapalı olması. Yamalı AODV'nin sayıları yamasızdan farklı (1001: 0,6906 → 0,6981 · 1003: 0,5501 → 0,5167) — açılıştaki bir kararın öbür yana düşmesi; yön yok. Ana depoya uygulanması öğrenci kararı (dondurulmuş taban, K-211).
