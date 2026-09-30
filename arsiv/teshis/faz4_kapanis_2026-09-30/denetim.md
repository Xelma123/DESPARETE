# Faz 4 kapanış denetimi — çalışma kaydı

> Başlangıç 29 Eylül 2026 gece · ajan · öğrencinin kuralı: Faz 5'e geride iş kalmadan, denetlenmiş yapı ve temiz belgelerle geçilir (`v2/12` §1.1). Bu dosya denetim sürerken dolar; kapanışta özeti K kaydına ve `v2/04`e, bu dosya arşivde kalır.

## Alanlar

| # | alan | soru | durum |
|---|---|---|---|
| D1 | köken defteri (Faz 4.4) | her parametrenin gerekçesi REFERANS dünyada geçerli mi | ✅ defter yeniden yazıldı · ölçümler U1'den sonra |
| D2 | alet envanteri (Faz 4.5) | `kalibrasyon/`deki 38 alet referans dünyada anlamlı mı, hangi karara hizmet ediyor | sırada |
| D3 | kapsam yeterliliği | ön-kayıdın ve hipotezlerin ölçmek istediği her şey referans dünyada ölçülebiliyor mu | sırada |
| D4 | kod | ölü kod, iki dünyanın dalları, bayat yorum ve adlar, testlerin referans dünyayı kapsaması | sırada |
| D5 | belgeler | `v2/*`, kök README, devir istemi, kod içi tarihçe — tek kaynak, güncel, arınmış | sırada |
| D6 | kapanış kanıtı | tam takım · regresyon (yeni taban) · mimari denetimi · K kaydı | en son |

## Bulgular

Önem: 🔴 sonucu ya da bir kararı etkileyebilir · 🟡 düzeltilmeli, sonucu etkilemesi beklenmiyor · ⚪ temizlik.

**B1 🔴 · Köken defteri eski dünyaya dayanıyor (D1).** `DUYARSIZ` kovasındaki 16 kaydın 16'sı 8–16 Eylül'de ESKİ 1:50 dünyada ölçüldü (R = 0,0316, "1000 m, α = 3" çalışma noktası); `OLCULMUS` kovasındaki 22 kaydın ~16'sı eski dünyanın ölçümü. Deneyler referans dünyada → bu gerekçeler bugün geçerli değil. Bayat değerler gerekçe metninde: `rician_k_db` "6 dB" (referans 10), `golgeleme_hucre_m` "50 m" (referans 2 500), `ttl_baslangic` "en uzak çift 5 atlama" (eski dünya). Üretici: `py -3.11` ile `sim2.yapilandirma.kokenler` dökümü (bu dizinde `koken_dokumu.py`).

**B2 🟡 · 802.11b sabitleri yanlış kovada (D1).** `slot_s` · `sifs_s` · `cw_min` · `onbelge_s` · `temel_bit_hizi_bps` · `modulasyon` eski dünyanın `DUYARSIZ` aklamasıyla duruyor; oysa `v2/02` S2 🟢 (G1, G2, G12, G13) bunları kaynağa bağladı → `KAYNAK`.

**B3 🟡 · Kâhinler koşum beacon'ını kullanıyor, protokoller kullanmıyor (D1/D4).** Dört protokol `kosum_beaconi = False`; kâhinlerde öznitelik yok → varsayılan açık (`sim2/kosum/kontrol_durum.py:94`). U1'in paydası (ETX kâhini) ve üst referans her düğümden saniyede bir 32 B beacon yükü taşıyor; kâhinin komşu keşfine ihtiyacı yok. Beklenen etki küçük (kâhin biraz düşük → oranlar biraz lehte) ama ölçülmedi. `beacon_araligi_s` · `beacon_bayt` · `komsu_omru_katsayisi` bu yüzden kâhinde etkin.

**B4 🟡 · Karıştırıcı altında kanalın yeniden dinlenme ufku `beacon_araligi_s`e bağlı (D4).** `sim2/kosum/dugum.py:446, 483`: karıştırıcı kanalı ED ile kilitliyorsa düğüm bir sonraki karıştırıcı geçişine, yoksa 1 s sonrasına kadar bakmıyor; hareketli karıştırıcıda 10 ms (`karistirici_denetim_araligi_s`). Birincil hücrede (hareketli araç) etkisiz; sabit karıştırıcılı ailelerde düğümün kendi hareketi ve karıştırıcı bağının sönümlemesi 1 s donuk. İki ilgisiz kavram tek sabitte.

**B5 · Sınanmamış 41'in ve eski dünyaya dayanan kayıtların sınıflaması (D1)** — `siniflama.md`: kaynak var/kova yanlış (K) · indirmeyle kapanır (İ) · referans dünyada türetilir (T) · öğrencinin dünya kararı (D) · bugün hiçbir protokol okumuyor (E) · ölçülmeli (Ö) · pencere (P) · güvenlik sınırı (G) · alet sabiti (A). `cw_max`ın "erişilemez" gerekçesi referans dünyada ÇÖKTÜ (yeniden deneme 7 → 5. denemede 1023); kaynağı (G12) var.

**B6 🔴 · Regresyon ağı deneylerin dünyasını kapsamıyor (D4/D6).** `kalibrasyon/regresyon_satirlari.py`: 67 vakanın 3'ü referans dünyada (iki `dogrudan_komsu`, bir AODV statik). AODV · OLSR · AOMDV · DESPARETE yalnız ESKİ dünyada (`k-` vakaları); birincil hücre, yere toplamada gerçek protokol, öteki karıştırıcı sınıfları ve düğüm kaybı referans dünyada hiç yok. Faz 5 DESPARETE'yi (belki simülatörü) değiştirecek → güvenlik ağı referans dünyada olmalı. Öneri: kısa pencereli referans vakaları — birincil hücre × {AODV, OLSR, AOMDV, DESPARETE, ETX kâhini} · statik × {darbeli, reaktif, aldatıcı, taramalı} · düğüm kaybı · eşler arası bir vaka (~12 vaka, üretime ~20–30 dk). Vaka adından anahtar çıkaran `_kos` (sonek kuralları) iki soneki birlikte taşıyamıyor → vaka tanımı açık alanlara geçmeli. **30 Eylül: 13 `u-` vakası eklendi** (`REFERANS_VAKALARI`, anahtarlar tablodan; eski 67 vaka dokunulmadı; konfigürasyonların hepsi kuruluyor) — üretim U1'den sonra, yeni taban kapanışta.

**B7 🟡 ✅ · `cozunurluk.py` ve `duyarlilik.py` `--dunya` okumuyor, dünyayı basmıyordu (D2).** Ölçüm gövdesi (`duyarlilik._kos`) dünyayı ortam değişkeninden seçtiği için referans dünyada koşabiliyorlardı, ama argüman sessizce yok sayılır ve başlık dünyayı söylemezdi. 30 Eylül: ikisi de `DS.secimi_oku()` + `DUNYA:` satırı. K-187 AST testi geçiyor.

**B8 🔴 · Evre metrikleri birincil hücrede tanımsız (D3).** `08`in M1/M3/M4'ü tek bir açılma basamağı varsayar; birincil hücrenin karıştırıcısı 15 s açık · 15 s sessiz çizelgeli (K-200). Bugün birincil hücrenin evre metrikleri anlamsız sayılar üretiyor. Tanım (açık/sessiz evre başına PDR, her açılmada şok, her sessizliğe geçişte toparlanma) ya kapanışta yazılır ya Faz 6'ya bırakılır — ❓ öğrenci.

**B9 🟡 · Faz 4.5'in kapsamı (D2).** Eski doğrulama listesinin (`arsiv/DEVIR-2026-09-28-temizlik.md` §2) ayıklama taslağı: referans dünyada yeniden koşulacak — bağ kümesi eşiği (4) · örnekleme denetimi (6) · kâhin tavanı (8) · evre kapıları G1–G4 (9) · üst referans (15) · kontrol düzlemi kapıları (10, beklenen P6 17/6/6) · üretici dumanı (3, bir kez). Karşılığı başka alet: karıştırıcı çalışma noktası (K-186) · Li (K-187). Yalnız eski dünya: adım 9 kapanışı · onay semantiği.

**B10 ⚪ · Aşama 1'in yapım aletleri (D2).** `adim3_kapanis` · `adim3_oncesi` · `adim4_kapanis` · `adim4_sonumleme` · `adim5_kapanis` · `adim6a_kapanis` · `adim9_kapanis` · `bag_kalitesi` · `denetim_ornekleme` · `calkanti` · `formasyon_olcumu` · `gorev_kalibrasyonu` · `mobilite_gercekcilik` · `onay_semantigi` eski dünyanın yapım tarihçesi. Bazıları hâlâ canlı bir köken kaydının üreticisi (`golgeleme_sigma_db` ← `adim4_kapanis`, `sonumleme_parca_suresi_s` ← `adim4_sonumleme`) → önce kayıt referans dünyaya göre gerekçelenir, sonra alet arşive.

**B11 · Kapsam — sağlam bulunanlar (D3).** H1.3'ün dayanağı: referans dünyada karıştırıcı sınıflarının ortalama gücü eşit (darbeli tepe telafisi `Konfig.karistirici_guc_dbm`; taramalı −4,77 dB beyanlı) · aileler ortalama güçte eşit (K-186) · birincil metrik, telemetri/komut ayrımı (K-171), düğüm kaybı kohortu (K-182), kontrol yükü (NRL, veri başlığı dâhil), Θ ve enerji satırda · mekanizma testleri dünyadan bağımsız küçük dünyada (uygun).

## İlerleme — 30 Eylül gece

- **B1 ✅ · Köken defteri referans dünyaya göre yeniden yazıldı** (öğrenci onayı, K-203). Eski hâli `arsiv/kokenler-2026-09-30-eski-dunya.py`. Yeni kova `DUNYA_TANIMI` (onaylı dünya tanımları ve birincil hücre, kapsam). Referans dünyanın tablosu: KAYNAK 42 · DÜNYA TANIMI 19 · TÜRETİLMİŞ 71 · ÖLÇÜLMÜŞ 15 · TEDAVİ 35 · KOL TANIMI 12 · **SINANMAMIŞ 25** · DUYARSIZ 0 · **duyarlılık borcu 10** (keşifsel kol tanımları: darbeli · taramalı · reaktif · tekli merkez konumu · hava eşlik hızı). Eski sayım (41 · borç 9) eski dünyanındı. Mimari denetimi ihlalsiz; `test_yapilandirma.py` 56/56.
- **B2 ✅** 802.11b sabitleri `KAYNAK` (G1 · G2 · G12 · G15). **İndirmeler** (K-203): ns-3 `wifi-mac-header.cc` · `llc-snap-header.cc` · `wifi-mac-queue.cc` · `simple-frame-capture-model.cc` · `frame-capture-model.cc` · `wifi-utils.h`; RFC 791 · 768 · 1042 → `v2/02` G15 · G16, S2 ve S5 kapandı. Onay 14 B ve kapsülleme 64 B kaynaklı; kuyruk (ns-3 500 p · 500 ms ↔ bizde 50) ve yakalama (ns-3 5 dB · 16 µs ↔ bizde 10 dB · 192 µs) farklı → ölçülecek.
- **B10 ✅** 11 eski dünya aleti `arsiv/kalibrasyon-2026-09-30-eski-dunya/`e (adım 3/4/5/6a/9 kapanışları, `adim3_oncesi`, `bag_kalitesi`, `formasyon_olcumu`, `gorev_kalibrasyonu`, `mobilite_gercekcilik`); defterdeki dört sabit kaydı ve duman listesindeki iki satır çıktı. Simülatör yorumlarındaki üretici atıfları yorum temizliğinde.
- **Yeni ölçüm:** sönümlemenin bağıl hız tabanı referans dünyada çift-anların %0,2'sinde (formasyon) bağlıyor → `ÖLÇÜLMÜŞ` (`kalibrasyon/bagil_hiz_tabani.py`).
- **Faz 4.4'ün ölçüm listesi** (defterde `SINANMAMIS`, gerekçesinde plan): pencere üçlüsü (Faz 6) · `gm_adim_s` · `gm_pitch_sigma_rad` · `gorev_grup_sayisi` · `kanal_dilimi_s` · `golgeleme_hucre_m` · `rician_k_db` · `yakalama_esigi_db` · RSSI/GPS hataları (birebirlik) · saat ofseti/sapması · `cbr_titresim_s` · `kuyruk_kapasitesi` · `ttl_baslangic` · beacon üçlüsü (kâhin) · `ISTASYON_TUTMA_S` · `BEKLEYEN_UYANDIRMA_TAVANI` (u- vakalarından okunur) · `kahin.py::ATLAMA_ESIGI` · `kahin.py::SONUMLEME_ORNEGI` · önce referans dünyanın eşleştirilmiş R'si.

**B12 🟡 · Çerçeve anlamı belgelerde iki türlü anlatılıyordu (D3/D5).** Eski dünyada (1:50) "kutu sürüyle birlikte hareket eden bir gözlem çerçevesidir; sabit karıştırıcı yer referanslı karıştırıcının iyi yaklaşımıdır (270 s'de 225 m kayma)" deniyordu. 1:1'de aynı transit 11 km eder. Kodun gerçekte yaptığı: alan yere göre sabit bir GÖREV ALANI, sürü onun üzerinde kalır (bağımsız/görev kollarında dolaşır, formasyonda istasyon tutar), ortak transit yok; karıştırıcılar yer ya da hava platformu, sabit ya da kendi yörüngesinde (birincil hücrenin aracı yalnız sessizken 60 km/h). Kod tutarlı; bayat olan belgeler: `karistirici.py`, `mobilite.py::Formasyon3B` düzeltildi; `v2/07` §4'ün cümlesi belge temizliğinde. Sürünün transiti gelecek çalışma (`v2/12` §5, ~2 000 s'lik koşu). ❓ Öğrenciye bilgi: senaryo "görev alanı üzerinde kalan sürü" — telemetri/ISR görevi için makul.

## Yorum temizliği — 30 Eylül gece (K-203 kapsamı: `sim2/` + `protokoller/`)

Denetçi `yorum_denetci.py` (taban `yorum_tabani/`): belge dizgileri çıkarılmış sözdizim ağaçları birebir → yalnız yorum değişti. Yardımcılar `belge_degistir.py`, `yorum_yama.py` (aralığın ilk satırını doğrular).
- `protokoller/`: `desparete.py` başlığı (102 → 61 satır, sürüm geçmişi tek satıra) · `aodv.py` · `olsr.py` · `olsr_bicim.py` hata hikâyeleri ve eski dünya sayıları.
- `sim2/`: `konfig.py` 1 058 → 717 · `senaryolar.py` 441 → 226 · arşivlenen aletlere atıf veren dokuz dosya (`trafik` · `topoloji` · `yerlesim` · `cerceve` · `yayilim` (referans dünyada verici gücü GİRDİ — başlık düzeltildi) · `sonumleme` · `kopma` · `mobilite` · `sonuc`) · `karistirici.py` (çerçeve, B12).
- Ek temizlik: `sayaclar.py` · `dugum.py` · `gozlem/protokol.py` · `kosum/kontrol.py` · `gozlem/karar.py` · `mobilite.py` (görev kolunun belgesi "merkezler daraltılmış kutuda" diyordu — kod her müfrezeye bir SEKTÖR veriyor; düzeltildi). Kalan dokuz kısa "eskiden X, bu yüzden Y" gerekçesi bilerek bırakıldı. Tek bilinçli kod farkı: `konfig.py` hata mesajındaki kova listesi (`kokenler.KOVALAR`a atıf).
- Belgeler: `v2/04` §9 (sekiz kova, sayım) · `v2/06` §9 sayı · `v2/07` §4 çerçeve cümlesi (B12) ve §9 · `v2/12` · devir istemi.

## B4 ✅ düzeltildi (simülatör davranışı, 30 Eylül gece)

`dugum.py::_guc_mesgul_bitisi_s`: gerçekçi karıştırıcıda ED kilidindeki düğüm her zaman `karistirici_denetim_araligi_s` (10 ms) sonra yeniden bakar; eski dünya birebir. Köken kayıtları güncellendi. Beklenen regresyon farkı ölçmeden önce `regresyon_beklenti.md`de (3 vaka + köken sayımı + 13 yeni `u-`).

## B8 · öneri v2 — `evre_cizelgeli_oneri.md` (öğrenci onayı bekliyor)

v1 (evre katlama, `evre_cizelgeli_oneri_v1.md`) öğrencinin "bir süre daha düşün" isteğiyle eldeki veriye karşı sınandı ve geri çekildi (K-204). Sayılar `evre_mevcut_veri.py`. v2: M1 aynı · M2 sessiz dönemler · M3 tanımsız · M4 ilk açık dönem; kapılar G1ç/G2ç/G4ç. Onaylanırsa kod regresyon k203'ten ÖNCE (tek regresyon ikisini doğrular).

## Faz 4.4 · ölçüm planı (U1 ve regresyondan sonra, sırayla)

> ⚠️ **30 Eylül 12:15 — plan kusurlu, düzeltilecek.** #1 koşuldu (`arsiv/teshis/faz4_4_2026-09-30/`): R 0,0086 çıktı ama hücrede ETX kâhininin PDR'si **0,029**. `statik-surekli` (tek merkez karıştırıcı, kısa pencere) eski dünyanın çekirdek hücresidir; referans dünyada neredeyse her şeyi öldürür. Taban etkisiyle R yapay küçük çıkar ve aynı hücrede yapılacak tarama (#3) her parametreyi **sahte DUYARSIZ** gösterir. Aynı kusur `hareketli` (bağımsız-sürekli) ve `gorev` hücrelerinde de olabilir, çünkü tek merkez karıştırıcı alan merkezinde 10 W.
>
> **Öneri:** R ve taramalar referans dünyanın çalışma noktasında, **birincil hücrede** (formasyon · yere toplama · derin sızma; `duyarlilik.py birincil` hazır). Tutarlılık için ikisi de aynı pencerede ölçülür. Her tarama hücresinin ETX kâhini PDR'si taramadan önce basılır; tabana (< 0,1) ya da tavana (> 0,95) yakın hücre tarama hücresi olamaz, kural ölçmeden önce. Maliyet sonra hesaplanır; birincil hücrenin koşusu statikten pahalı.

| # | ne | nasıl | maliyet (tahmin) |
|---|---|---|---|
| 1 | referans dünyanın eşleştirilmiş R'si | `cozunurluk.py --dunya referans_2026 --tohum 40` (statik-sürekli, kısa pencere, iki kâhin) | ~30 dk |
| 2 | E grubu birebirlik | RSSI/GPS hataları ×2 → satır birebir mi (kısa, statik, AODV) | < 10 dk |
| 3 | fizik ve MAC | `duyarlilik.py statik --tohum 10` : `rician_k_db` · `yakalama_esigi_db` · `kuyruk_kapasitesi` · `ttl_baslangic` · `cbr_titresim_s` · `kanal_dilimi_s` · saat ofseti/sapması · beacon üçlüsü | ~1–2 sa |
| 4 | hareket ve kanal (birincil hücre) | `duyarlilik.py birincil --tohum 10` : `gm_adim_s` · `gm_pitch_sigma_rad` · `golgeleme_hucre_m` · `rician_k_db` | ~1–2 sa |
| 5 | görev kolu | `duyarlilik.py gorev` : `gorev_grup_sayisi` | ~30 dk |
| 6 | modül sabitleri | `ISTASYON_TUTMA_S` · `kahin.py::ATLAMA_ESIGI` · `SONUMLEME_ORNEGI` · kâhin beacon'ı açık/kapalı (B3): işçide sabit yamalanır, kısa pencere | ~1 sa |
| 7 | güvenlik sınırı | `BEKLEYEN_UYANDIRMA_TAVANI`: `u-` regresyon satırlarından tepe bekleyen | 0 |
| — | pencere üçlüsü | Faz 6 (`06` §8 koşul 1) | — |
| — | 10 borçlu keşifsel kol tanımı | ✅ kapsam ilanı (öğrenci, K-204): defterde `KAPSAM_ILANI`, borç 0 | — |

Ölçüt değişmez (`duyarlilik.py`): DUYARSIZ = eşleştirilmiş |Δ| referans R'nin altında VE kendi 2 SE bandı içinde; aksi DUYARLI → kaynak/eksen/kapsam kararı öğrenciye.
