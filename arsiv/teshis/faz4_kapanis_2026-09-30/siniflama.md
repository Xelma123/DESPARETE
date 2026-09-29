# D1 · Köken defterinin referans dünyaya göre sınıflaması (Faz 4.4) — taslak

> 29–30 Eylül 2026 gece · ajan · üretici `koken_dokumu.py` (bu dizin). Öğrenci onayı bekleyen noktalar ❓ ile işaretli.

## Temel sorun

`sim2/yapilandirma/kokenler.py` `Konfig`in VARSAYILANLARINI, yani ESKİ 1:50 dünyayı gerekçelendiriyor. Referans dünya (`kanal/dunya.py::referans_2026`) ~30 alanı eziyor ve birkaç `REFERANS_*` sabiti kendi kaydını taşıyor. Sonuç: mimari denetiminin saydığı "SINANMAMIŞ 41" eski dünyanın borcu; referans dünyanın gerçek borcu sayılmıyor. Bayat ya da yanlışa dönen gerekçe örnekleri:

| alan | defterde | referans dünyada |
|---|---|---|
| `olcek` | 1:50 | 1 |
| `iletim_menzili_m` | 280 m, "modelin uzunluk birimi" | 1 664 m, EIRP'den türer |
| `bant_genisligi_hz` · `gurultu_figuru_db` · `sinr_esigi_db` | 2 MHz · 6 dB · β = 16 | 22 MHz · 7 dB · 6,05 dB (işlem kazancı) |
| `rician_k_db` · `golgeleme_hucre_m` | 6 dB · 50 m | 10 dB · 2 500 m |
| `cw_max` | "yeniden deneme 4'te erişilemez" (TÜRETİLMİŞ) | yeniden deneme 7'de 5. denemede ERİŞİLİR → gerekçe çöktü; kaynak G12 var |
| `alan_*` · `gm_hiz_*` · `gorev_grup_yaricapi_m` | eski dünyanın ölçümleri | 33 km (ölçüldü, K-188) · 40–120 km/h (onaylı `14` §3) · 16 km (ölçüldü) — ayrı kayıtlarda ya da hiç |
| 16 `DUYARSIZ` | 8–16 Eylül, eski dünya, R = 0,0316 | referans dünyada ölçülmedi |

## Öneri — yapı ❓

Defter REFERANS dünyanın değerini gerekçelendirsin (deneyler orada); eski dünyanın değeri yalnız "tarihsel, regresyon için" notu taşısın, uzun eski gerekçeler arşive. Mimari denetimi borcu referans dünya için saysın. Eski dünya regresyonun eski vakaları için kalır (davranış değişmez).

## Eylem grupları (SINANMAMIŞ 41 + DUYARSIZ 16 + eski dünyaya dayanan TÜRETİLMİŞ/OLCULMUS)

**K · Kaynak var, kova yanlış** (ölçüm gerekmez; `02`'de mevcut kaynak): `slot_s` · `sifs_s` · `cw_min` · `cw_max` · `onbelge_s` (G2, G12) · `temel_bit_hizi_bps` · `modulasyon` (G1, G2) · `frekans_hz` (kanal 6, `14` §1) · `bant_genisligi_hz` (G1) · `gurultu_figuru_db` (`14` §1).

**İ · Kaynak indirilirse kapanır** (öğrenci izniyle indirme ❓): `onay_bayt` (ns-3 `wifi-mac-header.cc`: ACK boyu) · `KONTROL_KAPSULLEME` (ns-3 `llc-snap-header.cc`; RFC 791/768 tanımları) · `kuyruk_kapasitesi` (ns-3 `wifi-mac-queue.cc` varsayılanı ya da NS-2 `ifqlen`) · `yakalama_esigi_db` (ns-3 `simple-frame-capture-model.cc`; ⚠️ değer farklıysa davranış değişir → regresyon ve U1 yeniden) · `saat_sapma_ppm` (802.11 ±25 ppm; uygun açık kaynak aranacak).

**T · Referans dünyada türetilir** (gerekçe yeniden yazılır): `olcek` · `iletim_menzili_m` · `sinr_esigi_db` · `menzil_snr_db` · `sonumleme_parca_suresi_s` (referans hızlardan T_c/4) · `ALFA` (`06` §7 ön-kayıt α) · `komut_akis_sayisi` · `karistirici_baslangic_s`.

**D · Öğrencinin dünya/kol kararı** — kaynakta değil ama onaylı (`14`, K-169, K-186): `dugum_sayisi` 40 · `gm_hiz_*` 40–120 km/h · `irtifa_min/maks_m` 50–300 m · `paket_bayt` 512 B · `karistirici_taban_dbm` · `REFERANS_KARISTIRICI_DBM` 10 W · `tehdit_arac_hiz_kmh` 60 · `tehdit_hava_hiz_kmh` 200 · `gorev_grup_sayisi` · `REFERANS_PAY_DB`. ❓ Yeni kova "DÜNYA_TANIMI" (öğrenci onaylı referans dünya; kapsam beyanıyla, duyarlılık borcu yok) mu, yoksa `KOL_TANIMI` (duyarlılık borcu taşır) mı?

**E · Bugün hiçbir protokol okumuyor** (yapısal olarak etkisiz; kısa bir "değer değişince satır birebir" ölçümüyle kapanır, Faz 5'te bir mekanizma okursa borç açılır): `rssi_olcum_sigma_db` · `gps_dikey_sigma_m` · `gps_hiz_sigma_ms`.

**Ö · Referans dünyada ölçülmesi gereken** (duyarlılık; hücre ve maliyet ayrıca): `rician_k_db` (6/10/15, `14` §2 söz verdi) · `golgeleme_hucre_m` (eski dünyada DUYARLI çıkmıştı) · `golgeleme_sigma_db` · `kuyruk_kapasitesi` (kaynak çıkmazsa) · `ttl_baslangic` · `saat_ofset_araligi_s` · `cbr_titresim_s` · `gm_pitch_sigma_rad` · `gm_adim_s` · `kanal_dilimi_s` · `BAGIL_HIZ_TABANI_MS` · `ISTASYON_TUTMA_S` · `beacon_araligi_s` · `beacon_bayt` · `komsu_omru_katsayisi` (yalnız kâhinde etkin, B3) · `reaktif_*` (keşifsel sınıf).

**P · Pencere** (`06` §8 koşul 1: ısınma ve ölçüm penceresi birlikte taranır — ön-kayıt işi): `isinma_s` · `olcum_bitis_s` · `kosu_bitis_s`. ❓ Faz 6'ya mı (mühür öncesi), 4.4'e mi?

**G · Güvenlik sınırı**: `BEKLEYEN_UYANDIRMA_TAVANI` — tepe bekleyen her satırda; K-200 ve U1 satırlarından okunur → hiç bağlamadığı gösterilir.

**A · Alet sabitleri** — alet referans dünyada kullanılıyorsa gerekçesi yazılır, kullanılmıyorsa alet sabitleriyle birlikte arşive (D2): `calkanti.py` · `formasyon_olcumu.py` · `gorev_kalibrasyonu.py` · `calisma_noktasi.py::BASARI_ESIGI` · `duyarlilik.py::TOHUMLAR` · `evre_metrikleri_kapilari.py::TOHUMLAR` · `dugum_sayisi.py::ALAN_CAPASI_M` · `bag_kumesi.py::COZUNURLUK_R` · `onay_semantigi.py::COZUNURLUK_R` · `yeniden_kullanim.py::BAG_M` · …

**Duyarlılık borcu (9 kol tanımı):** `tehdit_acik_s` · `tehdit_sessiz_s` · `gecit_konumu` birincil hücrenin tanımı → ❓ eksen mi (ör. açık/sessiz 15 ↔ 5/45 s keşifsel), beyan mı; `darbe_*` · `taramali_*` keşifsel sınıflar; `karistirici_konum` · `istasyon_kayma_hiz_ms` birincil hücrede kullanılmıyor.
