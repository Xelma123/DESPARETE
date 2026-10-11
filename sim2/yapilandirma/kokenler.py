"""
Parametre kökenleri — her sayının nereden geldiği, tek kaynakta.

`Konfig`in her alanı ve davranış belirleyen her modül sabiti burada
tam olarak bir kovaya yazılır. Kaydı olmayan `Konfig` alanı kurulumu
durdurur; modül sabitlerini `kalibrasyon/mimari_denetimi.py` tarar.

🔒 GEREKÇELER REFERANS DÜNYANIN DEĞERİNİ ANLATIR (K-203)
=======================================================
Deneyler `kanal/dunya.py::referans_2026`de koşar (`v2/14`). `Konfig`in
varsayılanı eski 1:50 dünyadır ve yalnız regresyonun eski vakaları
için yaşar; değeri farklıysa gerekçede "eski dünyada …" diye anılır.
Eski dünyanın uzun gerekçeleri: `arsiv/kokenler-2026-09-30-eski-dunya.py`.

🔒 ÖN-KAYIT MÜHÜRLENMEDEN ÖNCE `SINANMAMIS` = 0 VE DUYARLILIK BORCU BOŞ
(borçlu kol tanımı ya ölçülür ya eksen/kapsam ilan edilir).
"""

from __future__ import annotations

__all__ = ["KOVALAR", "KOKENLER", "MODUL_KOKENLERI", "DUYARLILIK_BEKLEYEN",
           "KAPSAM_ILANI",
           "kova_sayimi", "eksik_alanlar", "duyarlilik_borcu"]

# ===========================================================================
# KOVALAR
# ===========================================================================
KOVALAR: dict[str, str] = {
    "TURETILMIS": "başka parametrelerden hesaplanıyor; serbest değil",
    "OLCULMUS": "bir kalibrasyon betiği üretti — üretici komut yazılı",
    "KAYNAK": "doğrulanmış dış kaynak; `02-DOGRULANMIS-KAYNAKLAR.md`de VAR",
    "DUYARSIZ": "oynatıldı, çekirdek hücrenin çıktısı DEĞİŞMEDİ — beyanla değil "
        "ÖLÇÜMLE hak edilir",
    "TEDAVI": "deneyin EKSENİ; iki kolun meşru olarak ayrıldığı alan "
        "(`kosum/sonuc.py::TEDAVI_ALANLARI` ile AYNI KÜME olmak ZORUNDA — "
        "test bunu sınıyor)",
    "KOL_TANIMI": "bir kolun NE OLDUĞUNU tanımlayan sabit; eksen DEĞİL, "
        "`kurulum_hash`in İÇİNDE — duyarlılık borcu taşır",
    "DUNYA_TANIMI": "öğrencinin onayladığı referans dünya tanımı ve birincil hücre "
        "(`v2/14`; K-169 · K-186 · K-203) — projenin KAPSAMI: sonuçlar bu "
        "dünyaya koşullu, kapsam beyanıyla; duyarlılık borcu taşımaz",
    "SINANMAMIS": "🔴 gerekçesi yok ya da yetersiz — mühürden önce boşalmalı",
}

# `TEDAVI` tam olarak `kosum/sonuc.py::TEDAVI_ALANLARI`dır (test sınar):
# iki kolun meşru olarak ayrılabildiği alanlar. Bir kolun NE OLDUĞUNU
# tanımlayan sabit `KOL_TANIMI`dır ve `kurulum_hash`in içindedir.

# 🔴 DUYARLILIK BORCU — `KOL_TANIMI`ndaki bir sabit sonucu belirleyebilir
# (eski dünyada darbeli ve taramalı sabitleri DUYARLI çıktı, 8 Eylül).
# Borç burada sayılır; mühürden önce ölçülür ya da eksen/kapsam ilan
# edilir. Bir adı silmek, gerekçesine ölçümün üretici komutunu ya da
# kapsam kararını (`KAPSAM_ILANI`) yazmayı gerektirir. `DUYARSIZ` gerekçeleri ölçülen |Δ|'yı taşır (D12 sayar) ve
# referans dünyanın eşleştirilmiş çözünürlüğüne karşı verilir (Faz 4.4).
DUYARLILIK_BEKLEYEN: frozenset[str] = frozenset()

# 🔒 KAPSAM İLANI (K-204, öğrenci 30 Eylül) — borç ölçülmeden kapanmadı,
# kapsam olarak beyan edildi: keşifsel sınıfların (darbeli · reaktif ·
# taramalı), tekli merkezin ve hava eşliğin tanım sabitleri. Hiçbiri
# birincil hücrenin kod yoluna girmez (yalnız kendi sınıfı ya da ailesi
# okur); o kolların sonucu bu değerlere koşulludur ve eski dünyada darbeli
# ile taramalı sabitleri DUYARLI çıkmıştı — rapor kapsam bölümünde yazar.
# Test: her ad `KOL_TANIMI`nda ve gerekçesi K-204'ü taşır.
# K-215 (öğrenci, 6 Ekim): iki mobilite kolu tanımı daha — görev kolunun
# müfreze sayısı ve bağımsız/görev kollarının GM eğim gürültüsü; ikisini de
# formasyon (birincil hücre) okumaz, Faz 4.4'te iz birebir.
KAPSAM_ILANI: frozenset[str] = frozenset({
    "darbe_gorev_cevrimi",
    "gm_pitch_sigma_rad",
    "gorev_grup_sayisi",
    "gorev_jitter_hiz_ms",
    "darbe_periyodu_s",
    "karistirici_konum",
    "reaktif_esik_dbm",
    "reaktif_patlama_s",
    "reaktif_sezme_olasiligi",
    "reaktif_sezme_s",
    "taramali_konak_sayisi",
    "taramali_konak_suresi_s",
    "tehdit_hava_hiz_kmh",
})

# ===========================================================================
# KÖKENLER — `Konfig`in her alanı, tam olarak bir kez
# ===========================================================================
KOKENLER: dict[str, tuple[str, str]] = {
    "kol": ("TEDAVI",
        "koşum etiketi; kurulum_hash dışında"),
    "senaryo": ("TEDAVI",
        "mobilite × karıştırıcı hücresi"),
    "tohum": ("TEDAVI",
        "eşleştirmenin ekseni"),
    "not_": ("TEDAVI",
        "serbest not; hiçbir davranışa girmez"),
    "isinma_s": ("SINANMAMIS",
        "50 s. Isınma ve ölçüm penceresi `06` §8 koşul 1 gereği BİRLİKTE "
        "taranır (koşu uzunluğundan bağımsızlık) — birincil hücrede, taban "
        "protokollerle, mühürden önce (Faz 6)"),
    "olcum_bitis_s": ("SINANMAMIS",
        "320 s — pencere 270 s; `isinma_s` ile aynı tarama (Faz 6)"),
    "kosu_bitis_s": ("SINANMAMIS",
        "350 s — pencereden sonra 30 s boşalma; `isinma_s` ile aynı tarama "
        "(Faz 6). Eski dünyadaki DUYARSIZ aklaması (8 Eylül) referans dünyada"
        " geçerli değil"),
    "dugum_sayisi": ("DUNYA_TANIMI",
        "40 İHA — `v2/14` §3 (onaylı K-169)"),
    "alan_en_m": ("DUNYA_TANIMI",
        "referansta 33 km (`kanal/dunya.py::REFERANS_ALAN_M`, ölçüldü K-188);"
        " eski dünyada 1 800 m"),
    "olcek": ("DUNYA_TANIMI",
        "referansta 1:1 (`v2/14`, K-169); eski dünya 1:50"),
    "alan_boy_m": ("DUNYA_TANIMI",
        "`alan_en_m` ile aynı; kare alan"),
    "irtifa_min_m": ("DUNYA_TANIMI",
        "50 m AGL — `v2/14` §3 bant 50–300 m (onaylı; `02` G9 NATO Sınıf I "
        "zarfı içinde); eski dünyada 20 m"),
    "irtifa_maks_m": ("DUNYA_TANIMI",
        "300 m AGL — `irtifa_min_m` ile aynı bant; eski dünyada 120 m"),
    "nominal_bag_m": ("TURETILMIS",
        "referansta `kanal/dunya.py` türetir: ortalama SNR'ın "
        "`menzil_snr_db` olduğu mesafe (≈ 1,66 km, EIRP 20 dBm) — nominal "
        "bağ, bir menzil değil güç çapası (`v2/07` §11). K-220'ye kadar adı "
        "`iletim_menzili_m`ydi (öğrenci). Eski dünyada 280 m"),
    "gm_alfa": ("DUYARSIZ",
        "α = exp(−adım/τ_v), τ_v ≈ 30 s hız korelasyonu (araç dinamiği "
        "zamanı, ölçeklenmez; τ_v kaynaksız bir seçim). Formasyon kolu "
        "(birincil hücre) da okur. Birincil hücrede τ'dan oynatılarak "
        "ölçüldü (τ×0,5 → α 0,9663 · τ×2 → 0,9915; "
        "`duyarlilik.py::KORELASYON_KATSAYILARI`), 20 tohum, R 0,0126: en "
        "büyük |Δ| = 0,0024 (pdr_etx; 0,2R, band 0,6×). 5 tohumda 0,0110 "
        "(0,9R) sınırdaydı. Üretici: `py -3.11 -u kalibrasyon/duyarlilik.py "
        "--dunya referans_2026 birincil --tohum 20 gm_alfa` (10 Ekim 2026, "
        "K-225; "
        "`arsiv/teshis/denetim_duzeltme_2026-10-09/C2_gm_alfa_20.txt`)"),
    "gm_adim_s": ("DUYARSIZ",
        "0,5 s mobilite adımı (adımda ≤ 17 m, hız korelasyonu `gm_alfa` ile "
        "korunur). Faz 4.4'te 20 tohumla ölçüldü: en büyük |Δ| = 0,0068 "
        "(×2, pdr_atlama; 0,5R, band 0,8×). Üretici: `py -3.11 -u "
        "kalibrasyon/duyarlilik.py --dunya referans_2026 birincil --tohum "
        "20 …` (7 Ekim 2026, K-217; yakınsamış kâhin, R 0,0142). 5 tohumluk "
        "ölçüm sınırdaydı (K-214)"),
    "gm_hiz_min_ms": ("DUNYA_TANIMI",
        "40 km/h = 11,1 m/s — `v2/14` §3 (onaylı); eski dünyada 0,25 m/s "
        "(ölçekli)"),
    "gm_hiz_maks_ms": ("DUNYA_TANIMI",
        "120 km/h = 33,3 m/s — `v2/14` §3 (onaylı); eski dünyada 0,75 m/s"),
    "gm_hiz_sigma_ms": ("DUNYA_TANIMI",
        "azami hızın %10'u (referansta 3,33 m/s) — kaynaksız bir seçim; "
        "formasyon kolunun (birincil hücre) manevra gürültüsü de buradan. "
        "Öğrencinin kararıyla referans dünyanın tanımı (10 Ekim 2026, "
        "K-225; K-220'nin emsali). Ölçülen duyarlılığı raporda yazılır: "
        "birincil hücrede (5 tohum, R 0,0126) ×0,5 en büyük |Δ| 0,0089 "
        "(0,7R) · ×2 0,0274 (pdr_atlama; 2,2R, band 2,9×) → DUYARLI. "
        "Üretici: `py -3.11 -u kalibrasyon/duyarlilik.py --dunya "
        "referans_2026 birincil gm_alfa gm_hiz_sigma_ms` (9 Ekim 2026, "
        "K-224; "
        "`arsiv/teshis/denetim_duzeltme_2026-10-09/B1_duyarlilik.txt`)"),
    "gm_azimut_sigma_rad": ("TURETILMIS",
        "koordineli dönüş ω = g·tan(φ)/v. Yerçekimi ÖLÇEKLENMEZ, o yüzden "
        "GERÇEK hızdan: 90 km/h'de 30° banka → 0,226 rad/s → 0,5 s adımda "
        "0,11 rad"),
    "gm_pitch_ort_rad": ("TURETILMIS",
        "0 — kalıcı tırmanış olmaması gerektiği için; testle bağlı"),
    "gm_pitch_sigma_rad": ("KOL_TANIMI",
        "0,05 rad — Gauss–Markov eğim gürültüsü; bağımsız ve görev "
        "kollarının mobilitesi okur, formasyon okumaz (Faz 4.4: birincil "
        "hücrede iz birebir, K-214) · KAPSAM (K-215): mobilite kolunun "
        "tanımı — o kolun sonucu bu değere koşullu; birincil hücrenin kod "
        "yoluna girmez"),
    "gorev_grup_sayisi": ("KOL_TANIMI",
        "10 müfreze × 4 — görev kolunun tanımı; yalnız görev kolunun "
        "mobilitesi okur, formasyon okumaz · KAPSAM (K-215): mobilite "
        "kolunun tanımı — o kolun sonucu bu değere koşullu; birincil "
        "hücrenin kod yoluna girmez"),
    "gorev_grup_yaricapi_m": ("OLCULMUS",
        "referansta 16 km (`kanal/dunya.py::REFERANS_GOREV_YARICAPI_M`, "
        "K-188). Üretici: `python kalibrasyon/calisma_noktasi.py --dunya "
        "referans_2026 --bolum gorev_kolu`; eski dünyada 650 m"),
    "gorev_jitter_hiz_ms": ("KOL_TANIMI",
        "azami hızın ~%7'si — görev kolunun tanımı; yalnız görev kolu okur "
        "· KAPSAM (K-222): mobilite kolunun tanımı — o kolun sonucu bu "
        "değere koşullu; birincil hücrenin kod yoluna girmez (denetim "
        "2026-10-08 D-07)"),
    "istasyon_kayma_hiz_ms": ("DUNYA_TANIMI",
        "0 — formasyon kolunda istasyonlar sabit (`v2/07` §4, öğrenci onayı "
        "Y6); birincil hücrenin kolu"),
    "bit_hizi_bps": ("KAYNAK",
        "802.11b DQPSK 2 Mb/s — `02` G1 (Pei & Henderson: 1/2 Mb/s "
        "DBPSK/DQPSK) ve G2 (Boer, DSSS PHY). K-189'da kapandı; referans "
        "dünyada ARF bu hızdan başlar"),
    "temel_bit_hizi_bps": ("KAYNAK",
        "1 Mb/s DBPSK (önbelge, yayın, onay) — `02` G1 · G2"),
    "onbelge_s": ("KAYNAK",
        "192 µs = uzun önbelge 144 + başlık 48 µs — `02` G2 · G12 "
        "(`dsss-phy.cc`)"),
    "bant_genisligi_hz": ("KAYNAK",
        "referansta 22 MHz — `02` G1 (802.11b gürültü bandı; "
        "`DSSS_KANAL_BANDI_HZ`); eski dünyada 2 MHz"),
    "frekans_hz": ("KAYNAK",
        "referansta 2 437 MHz = kanal 6 — `v2/14` §1, `02` G2; eski dünyada "
        "2,4 GHz"),
    "tasiyici_dinleme": ("KAYNAK",
        "anahtar (`v2/15` A3, K-174): 'guc' = 802.11b CCA — önbelge sezme "
        "(alıcı kilidi) ya da enerji sezme — `02` G2 (Boer 1996, CCA mod "
        "1/2/3). Varsayılan 'geometrik' = eski dünya; dünya değişimi A8'de"),
    "ed_esigi_dbm": ("KAYNAK",
        "−76 dBm — `02` G2 (Boer 1996): ED eşiği iletilen >100 mW → −80 · >50"
        " mW → −76 · ≤50 mW → −70 dBm; referans telsiz 61 mW (`v2/14`)"),
    "karistirici_denetim_araligi_s": ("TURETILMIS",
        "10 ms — ED ile kilitli düğümün karıştırıcı gücünü yeniden denetleme "
        "aralığı (200 km/h'de 0,55 m; `v2/15` A3, onaylı K-170). Referans "
        "dünyada (gerçekçi karıştırıcı) HER ZAMAN: karıştırıcı bağının "
        "sönümlemesi ve düğümün hareketi gücü sürekli değiştirir (denetim B4,"
        " 30 Eylül); eski dünyada yalnız hareketli karıştırıcıda"),
    "dunya": ("TURETILMIS",
        "anahtar (`v2/15` A7, K-178): 'referans_2026' = `v2/14`ün onaylı 1:1 "
        "dünyası (K-169), `kanal/dunya.py` kurar; varsayılan 'olcek_1_50' = "
        "eski dünya; değişim A8'de"),
    "verici_eirp_dbm": ("KAYNAK",
        "20 dBm referansta — AB/TR 2,4 GHz EIRP sınırı, `02` G2 · G7 (`v2/14`"
        " §1); eski dünyada None (güç menzilden türer)"),
    "alici_anten_kazanci_dbi": ("TURETILMIS",
        "referansta 2,15 dBi — yarım dalga dipolün en büyük kazancı (`v2/14` "
        "§1, onaylı; `bag_butcesi.py` ile aynı); eski dünyada 0 (verici gücü "
        "türetildiği için sadeleşir)"),
    "menzil_snr_db": ("TURETILMIS",
        "referansta SNR(PER %10, 2 Mb/s) + 10 dB pay — `bag_butcesi.py` ile "
        "aynı tanım (`kanal/dunya.py`); eski dünyada None (menzilde SNR = β)"),
    "karistirici_taban_dbm": ("DUNYA_TANIMI",
        "referansta 40 dBm = 10 W toplam ortalama, her ailede eşit — öğrenci "
        "kararı K-186 (`v2/14` §4); eski dünyada None (ρ kalibrasyonu "
        "`KARISTIRICI_GUCU_DBM`)"),
    "kayip_dugum_sayisi": ("TEDAVI",
        "TEDAVİ ekseni — düğüm kaybı (`v2/15` C1, K-180); varsayılan 0"),
    "kayip_bas_s": ("TEDAVI",
        "düğüm kaybı penceresinin başı (`v2/15` C1, K-180)"),
    "kayip_bitis_s": ("TEDAVI",
        "düğüm kaybı penceresinin sonu (`v2/15` C1, K-180)"),
    "enerji_gonderim_w": ("KAYNAK",
        "10,6 W — `02` G7 (Doodle Labs, gönderimde en çok); `v2/14` §8"),
    "enerji_alim_w": ("KAYNAK",
        "2 W — `02` G7 (alım/dinleme); `v2/14` §8"),
    "karistirici_gercekci": ("KAYNAK",
        "anahtar (`v2/15` A6, K-176): karıştırıcı bağında sönümleme (düğüm "
        "bağıyla aynı model) · yer–hava kanalı `02` G6 (Al-Hourani 2014) · "
        "reaktif sezme eşiği · aldatıcının sahte çerçevesi alıcıyı kilitler "
        "(`02` G5). Varsayılan kapalı = eski dünya"),
    "yer_karistirici_yukseklik_m": ("DUNYA_TANIMI",
        "3 m — `v2/14` onaylı aralığın (1,5–5 m) ortası"),
    "a2g_ortam": ("KAYNAK",
        "banliyö — `02` G6'da açık kırsal yok, en yakını banliyö (`v2/14`, "
        "onaylı); S-eğrisi a = 4,880, b = 0,429 makalenin Tablo I–II'sinden "
        "hesaplanır (`kanal/yer_hava.py`)"),
    "a2g_durum_dilimi_s": ("TURETILMIS",
        "1 s — banliyöde bina aralığı 1/√β ≈ 37 m (β = 750/km², G6); 100 "
        "km/h'de ≈ 1,3 s"),
    "reaktif_esik_dbm": ("KOL_TANIMI",
        "−90 dBm — reaktif kolun tanımı (802.11b duyarlılığı mertebesi, "
        "K-173); keşifsel sınıf"
        " · KAPSAM (K-204): keşifsel kolun tanımı — o kolun sonucu bu değere koşullu; birincil hücrenin kod yoluna girmez"),
    "reaktif_sezme_olasiligi": ("KOL_TANIMI",
        "0,95 — reaktif kolun tanımı; keşifsel sınıf"
        " · KAPSAM (K-204): keşifsel kolun tanımı — o kolun sonucu bu değere koşullu; birincil hücrenin kod yoluna girmez"),
    "yayilim_gecikmesi": ("TURETILMIS",
        "anahtar (`v2/15` A5, K-175): açıkken varış gecikmesi d/c (ışık hızı "
        "— fizik); onay bekleme en uzak duyma mesafesinin gidiş-dönüşünü "
        "kapsar. Varsayılan kapalı = eski dünya (1:50'de ihmal edilebilirdi, "
        "gerçek ölçekte slottan uzun)"),
    "hiz_uyarlamasi": ("KAYNAK",
        "anahtar (`v2/15` A4, K-177): ARF `02` G14 (ns-3 `ArfWifiManager`); "
        "hızlar 1/2/5,5/11 Mb/s ve CCK hata modeli G1 · G12; yayın ve onay "
        "temel hızda 1 Mb/s. Varsayılan kapalı = eski dünya (sabit 2 Mb/s)"),
    "arf_basari_esigi": ("KAYNAK",
        "10 — `02` G14 (ns-3 `SuccessThreshold` varsayılanı)"),
    "arf_zamanlayici_esigi": ("KAYNAK",
        "15 — `02` G14 (ns-3 `TimerThreshold` varsayılanı; özgün ARF'nin "
        "zaman sayacının paket sayaçlı karşılığı)"),
    "islem_kazanci": ("KAYNAK",
        "anahtar (`v2/15` A2, K-173): açıkken Eb/N0 = SINR · B/R_b, B = 22 "
        "MHz — `02` G1 (Pei & Henderson 2009; ns-3 `DsssErrorRateModel`) · G2"
        " (Boer 1996). Varsayılan kapalı = eski dünya; dünya değişimi A8'de"),
    "modulasyon": ("KAYNAK",
        "DQPSK (2 Mb/s veri, ARF'nin başlangıcı) — `02` G1 · G2"),
    "yol_kaybi_usteli": ("KAYNAK",
        "α = 2 serbest uzay — hava–hava ölçümleri 1,92–2,6 (`02` G10); "
        "iki-ışın kırılma mesafesi 100 m irtifada ~325 km, bağların çok "
        "üstünde (`v2/14` §2)"),
    "sinr_esigi_db": ("TURETILMIS",
        "referansta `kanal/dunya.py` türetir: SNR(PER %50, 2 Mb/s, işlem "
        "kazancıyla) + 2σ gölgeleme payı (≈ 6,05 dB); eski dünyada 16 dB"),
    "gurultu_figuru_db": ("KAYNAK",
        "referansta 7 dB → gürültü −93,6 dBm — `02` G1, `v2/14` §1; eski "
        "dünyada 6 dB"),
    "sicaklik_k": ("TURETILMIS",
        "290 K — gürültü figürünün tanımlı referans sıcaklığı (gürültü = "
        "kTB·NF, `v2/14` §1)"),
    "kanal_dilimi_s": ("DUYARSIZ",
        "0,1 ms — hash tabanlı kanal kararlarının zaman dilimi (reaktif "
        "sezme, alıcı ve RSSI yolları). Faz 4.4'te 20 tohumla ölçüldü: en "
        "büyük |Δ| = 0,0048 (×0,5, pdr_atlama; 0,3R, band 0,5×). Üretici: "
        "`py -3.11 -u kalibrasyon/duyarlilik.py --dunya referans_2026 "
        "birincil --tohum 20 …` (7 Ekim 2026, K-217; yakınsamış kâhin, R "
        "0,0142). 5 tohumluk ölçüm sınırdaydı (K-214)"),
    "golgeleme_acik": ("TURETILMIS",
        "açık; kapalıyken bağlar gerçeğe göre keskin açılıp kapanıyor — "
        "ablasyon için False yapılabilir"),
    "golgeleme_sigma_db": ("DUNYA_TANIMI",
        "σ 3 dB log-normal — `v2/14` §2 (onaylı K-169)"),
    "golgeleme_hucre_m": ("DUNYA_TANIMI",
        "2,5 km (eski dünyanın 50 m'si × 50; K-188) — değeri kaynakta yok · "
        "DÜNYA TANIMI (öğrenci, K-220): sonuçlar bu değere koşullu, ölçülen "
        "duyarlılık raporun kapsam bölümünde. Faz 4.4'te 20 tohumla: ×0,5 "
        "(1,25 km) pdr_atlama +0,030 (2,1R), pdr_etx +0,014 (1,0R); ×2 "
        "duyarsız (0,1R). Üretici: `py -3.11 -u kalibrasyon/duyarlilik.py "
        "--dunya referans_2026 birincil --tohum 20 …` (7 Ekim 2026, K-217)"),
    "sonumleme_acik": ("TURETILMIS",
        "açık; ablasyon için False"),
    "sonumleme_uretec": ("TURETILMIS",
        "uygulama seçimi, fiziksel parametre değil (K-198): aynı yenilik "
        "dağılımı (bağımsız N(0, 1)), aynı süzgeç; 'blok' = bağ başına "
        "blake2b anahtarı + SplitMix64 sayacı (Steele ve ark. 2014), birincil"
        " hücrede sönümleme maliyetini düşürmek için. Varsayılan 'tekil' = "
        "eski dünya birebir; referans dünyada 'blok'. İstatistiksel denkliği "
        "testlerde (ortalama, varyans, otokorelasyon, basıklık) sınanır"),
    "rician_k_db": ("TEDAVI",
        "EKSEN (öğrenci, K-215): birincil test 10 dB'de, 6 ve 15 dB'de "
        "keşifsel tekrar (`06`'ya Faz 6'da). Hava–hava için doğrudan ölçüm "
        "yok, dolaylı aralık 6–15 dB (`02` G11, S1; `v2/14` §2). Faz 4.4'te "
        "DUYARLI ölçüldü: 5 dB'de pdr_etx −0,126, 20 dB'de +0,077 (8,5R; "
        "`py -3.11 -u kalibrasyon/duyarlilik.py --dunya referans_2026 "
        "birincil …`, 2 Ekim 2026, K-214)"),
    "sonumleme_parca_suresi_s": ("TURETILMIS",
        "190 µs ≤ T_c/4: en büyük bağıl hız 2 × 120 km/h = 66,7 m/s, λ = 12,3"
        " cm → T_c = 0,423 λ/v ≈ 0,78 ms → T_c/4 ≈ 195 µs (Clarke)"),
    "anten_deseni_acik": ("TURETILMIS",
        "açık; ablasyon için False"),
    "yakalama_etkisi_acik": ("TURETILMIS",
        "açık; ablasyon için False"),
    "yakalama_esigi_db": ("DUYARSIZ",
        "10 dB, 192 µs'lik önbelge penceresinde — ns-3 5 dB, 16 µs (`02` "
        "G15). Faz 4.4'te 20 tohumla ölçüldü (5 · 20 dB): en büyük |Δ| = "
        "0,0118 (×0,5, pdr_atlama; 0,8R, band 0,9×). Üretici: `py -3.11 -u "
        "kalibrasyon/duyarlilik.py --dunya referans_2026 birincil --tohum "
        "20 …` (7 Ekim 2026, K-217; yakınsamış kâhin, R 0,0142). 5 tohumluk "
        "ölçüm sınırdaydı (K-214)"),
    "gps_yatay_cep_m": ("KAYNAK",
        "1,5 m CEP — `02` G7 (Doodle Labs veri sayfası, yerleşik GPS); "
        "`v2/14` §3"),
    "gps_dikey_sigma_m": ("SINANMAMIS",
        "2 m (`v2/15` B3, onaylı K-170; kaynak yok). 🔴 11 Ekim 2026 (K-233): "
        "JarmRout konum okuyor (RREQ'nun P_coord'u; makale 2B, dikey "
        "kullanılmıyor) → DUYARSIZ hükmü düştü, JarmRout'la yeniden ölçülür. "
        "Önceki hüküm: hiçbir protokol konum okumuyordu (kodda). Faz 4.4'te ölçüldü: kâhinle ×0,5 · ×2'de "
        "ve DESPARETE'yle ×2'de |Δ| = 0,0000 (iz birebir). Üretici: `py "
        "-3.11 -u kalibrasyon/duyarlilik.py --dunya referans_2026 birincil "
        "…` ve `kalibrasyon/duyarlilik.py`nin oynatmasıyla "
        "`arsiv/teshis/faz4_4_birincil_2026-10-02/protokol_tarama.py` (2 "
        "Ekim 2026, K-214). Faz 5'te bir mekanizma okursa yeniden ölçülür"),
    "gps_hiz_sigma_ms": ("DUYARSIZ",
        "0,1 m/s (`v2/15` B3; kaynak yok). Bugün hiçbir protokol hız "
        "okumuyor. Faz 4.4'te ölçüldü: kâhinle ve DESPARETE'yle |Δ| = "
        "0,0000 (iz birebir). Üretici: `py -3.11 -u "
        "kalibrasyon/duyarlilik.py --dunya referans_2026 birincil …` ve "
        "`kalibrasyon/duyarlilik.py`nin oynatmasıyla "
        "`arsiv/teshis/faz4_4_birincil_2026-10-02/protokol_tarama.py` (2 "
        "Ekim 2026, K-214). Faz 5'te bir mekanizma okursa yeniden ölçülür"),
    "gps_tazeleme_s": ("TURETILMIS",
        "1 s — `v2/15` B3 (1 Hz tazeleme), onaylı K-170"),
    "rssi_olcum_sigma_db": ("SINANMAMIS",
        "σ 2 dB (`v2/15` B2, onaylı K-170; kaynak yok). 🔴 11 Ekim 2026 "
        "(K-233): JarmRout RSSI okuyor — bağ kalitesi RSSI örneklerinin "
        "varyansı (Pu 2018 Eş. 5), ölçüm hatası doğrudan girer → DUYARSIZ "
        "hükmü düştü; kaynak aranır ve JarmRout'la yeniden ölçülür. Önceki "
        "hüküm: hiçbir protokol RSSI okumuyordu (DESPARETE'nin kancası argümanı "
        "kullanmıyor). Faz 4.4'te ölçüldü: kâhinle ve DESPARETE'yle |Δ| = "
        "0,0000 (iz birebir). Üretici: `py -3.11 -u "
        "kalibrasyon/duyarlilik.py --dunya referans_2026 birincil …` ve "
        "`kalibrasyon/duyarlilik.py`nin oynatmasıyla "
        "`arsiv/teshis/faz4_4_birincil_2026-10-02/protokol_tarama.py` (2 "
        "Ekim 2026, K-214). Faz 5'te bir mekanizma okursa yeniden ölçülür"),
    "yakalama_penceresi_s": ("TURETILMIS",
        "192 µs = önbelge süresi (`onbelge_s`: uzun PLCP önbelgesi 144 µs + "
        "başlık 48 µs, ns-3 `dsss-phy.cc`) — TANIM gereği: alıcı PLCP "
        "başlığını çözene kadar daha güçlü bir çerçeveye geçebilir, gövdede "
        "kilidi bırakmaz (`konfig.py` gerekçesi). Ayrı sabit kasıtlı (önbelge"
        " aritmetiği `cerceve.py`de kalsın); SESSİZ ayrışmayı "
        "`test_K198_yakalama_penceresi_ONBELGEYE_esit` yakalar (K-198; eski "
        "borç: 'ikisi bağımsız değişebilir')"),
    "slot_s": ("KAYNAK",
        "20 µs — `02` G2 · G12 (*Table 16-4 … 802.11-2020*)"),
    "sifs_s": ("KAYNAK",
        "10 µs — `02` G12 (*Table 16-4 … 802.11-2020*)"),
    "cca_s": ("KAYNAK",
        "REFERANS DÜNYADA 15 µs — `02` G2 (Boer: enerji sezme 15 µs); "
        "`kanal/dunya.py` yazar. Eski dünyanın varsayılanı 4 µs tarihseldir "
        "(gerekçesiz), deneyler referansta koşar (K-189)"),
    "cw_min": ("KAYNAK",
        "31 — `02` G12 (`wifi-mac.cc`, 802.11b)"),
    "cw_max": ("KAYNAK",
        "1023 — `02` G12 (`wifi-mac.cc`, 802.11b). Referansta 7 denemede "
        "(31 → 63 → 127 → 255 → 511 → 1023) 6. denemede erişilir; eski "
        "dünyada (5 deneme) erişilemez — mimari D8 iki dünyada sınar"),
    "yeniden_deneme_siniri": ("KAYNAK",
        "REFERANS DÜNYADA 6 yeniden deneme = 7 İLETİM DENEMESİ — "
        "dot11ShortRetryLimit 7 *maximum number of transmission attempts* "
        "(`02` G12, ns-3 `FrameRetryLimit`; G13 Linux `retry_short = 7`); "
        "512 B'lık çerçeve RTS eşiğinin altında. Alan YENİDEN deneme "
        "sayısıdır (toplam = sınır + 1); K-223'e kadar 7 yazılıydı, yani 8 "
        "deneme yapılıyordu (denetim D-10). Eski dünyanın 4'ü (uzun sınır) "
        "tarihsel; etkisi ölçülmüştü: yok (K-189)"),
    "onay_bayt": ("KAYNAK",
        "14 B = başlık 10 B + FCS 4 B — `02` G15 (`wifi-mac-header.cc`, "
        "`wifi-standard-constants.h`)"),
    "saat_senkron": ("TURETILMIS",
        "False; bedava kusursuz senkron yasak — ablasyon için True"),
    "saat_ofset_araligi_s": ("DUYARSIZ",
        "±0,5 s — saatler senkron değil (`v2/05` §3.2). Faz 4.4'te AODV ve "
        "AOMDV'de DUYARLI'ydı; sebep AODV'nin başlangıç durumunun yerel "
        "saatin 0 anına çapalı olmasıydı ve giderildi (`AODV-j`, K-215). "
        "Yeniden ölçüldü (±0,25 · ±1 s, 5 tohum): AODV-j ve AOMDV-f İZ "
        "BİREBİR, OLSR birebir (K-214), kâhin birebir → |Δ| = 0,0000. "
        "Üretici: `kalibrasyon/duyarlilik.py`nin oynatmasıyla "
        "`arsiv/teshis/faz4_4_birincil_2026-10-02/protokol_tarama.py` (TTL "
        "32, K-214) ve "
        "`arsiv/teshis/faz4_4_k215_2026-10-06/protokol_kontrol.py` (TTL 64, "
        "K-217)"),
    "saat_sapma_ppm": ("DUYARSIZ",
        "20 ppm kristal (802.11'in ±25 ppm toleransının içinde) — 350 s'de "
        "≤ 7 ms. Kâhinin zamanlayıcısı yok (iz birebir). Taban "
        "protokollerle (10 · 40 ppm): AODV ve AOMDV birebir; OLSR en büyük "
        "|Δ| = 0,0042 (TTL 32) · 0,0035 (TTL 64). Üretici: "
        "`kalibrasyon/duyarlilik.py`nin oynatmasıyla "
        "`arsiv/teshis/faz4_4_birincil_2026-10-02/protokol_tarama.py` (TTL "
        "32, K-214) ve "
        "`arsiv/teshis/faz4_4_k215_2026-10-06/protokol_kontrol.py` (TTL 64, "
        "K-217)"),
    "paket_bayt": ("DUNYA_TANIMI",
        "512 B telemetri — `v2/14` §5 (onaylı; MAVLink ölçeği `02` G4)"),
    "akis_sayisi": ("TURETILMIS",
        "10 — eşler arası desen 10 × 4,0 pkt/s = 40 pkt/s, yere toplamanın "
        "sunumuna (39 × 1,0 + 4 × 0,25) eşit (K-126); `akis_paket_hizi_hz` "
        "TEDAVİ"),
    "akis_paket_hizi_hz": ("TEDAVI",
        "TEDAVİ ekseni — trafik yoğunluğu (`v2/15` C2, K-180). Varsayılan 4,0"
        " — `akis_sayisi` ile AYNI kayıt; ikisi tek yükü (10 × 4,0 = 40 "
        "pkt/s) birlikte tanımlar (K-126)"),
    "cbr_titresim_s": ("DUNYA_TANIMI",
        "50 ms — periyodik kilitlenmeyi kırar (trafik üretecinin tanımı) · "
        "DÜNYA TANIMI (öğrenci, K-220): ölçülen duyarlılık raporda. Faz "
        "4.4'te 20 tohumla ×2'de |Δ| 0,0070 (pdr_etx; 0,5R — deneyin "
        "çözünürlüğünün altında, yalnız istatistik bacağı: band 1,2×); ×0,5 "
        "duyarsız. Üretici: `py -3.11 -u kalibrasyon/duyarlilik.py --dunya "
        "referans_2026 birincil --tohum 20 …` (7 Ekim 2026, K-217)"),
    "trafik_deseni": ("TEDAVI",
        "trafik deseni ekseni: `esler_arasi` · `yere_toplama` (`v2/07` §06.2,"
        " §18 Y4; öğrenci onayı 10–11 Eylül 2026)"),
    "tehdit_senaryosu": ("TEDAVI",
        "karıştırıcı kümesinin biçimi: `tekli_merkez` · `cephe_hatti` · "
        "`derin_sizma` · `hedef_koruma` · `hava_eslik` (`v2/07` §05.3.1, §18 "
        "Y5; öğrenci kararları 11 Eylül 2026, K-119)"),
    "tehdit_acik_s": ("DUNYA_TANIMI",
        "15 s — birincil hücrenin çizelgesi (`derin_sizma`, K-186 · K-192)"),
    "tehdit_sessiz_s": ("DUNYA_TANIMI",
        "15 s — birincil hücrenin çizelgesi; araç yalnız bu dönemde taşınır "
        "(K-186 · K-192)"),
    "tehdit_arac_hiz_kmh": ("DUNYA_TANIMI",
        "60 km/h — birincil hücrenin yer aracı (`v2/07` §5, K-186)"),
    "tehdit_hava_hiz_kmh": ("KOL_TANIMI",
        "200 km/h — hava eşlik ailesinin tanımı; keşifsel aile (1–5 W sürüyü "
        "böler, K-186)"
        " · KAPSAM (K-204): keşifsel kolun tanımı — o kolun sonucu bu değere koşullu; birincil hücrenin kod yoluna girmez"),
    "gecit_konumu": ("DUNYA_TANIMI",
        "`kenar` — geçit batı kenarının ortasında sabit röle (`v2/07` §6; "
        "birincil hücre)"),
    "telemetri_paket_hizi_hz": ("TEDAVI",
        "TEDAVİ ekseni — trafik yoğunluğu (`v2/15` C2, K-180). Varsayılan 1,0"
        " pkt/s. 🟢 C3 KOSTU (15 Eylul 2026, K-126). Uretici: `python -u "
        "kalibrasyon/yere_toplama_yuku.py`. Olcut TARAMADAN ONCE ilan edildi "
        "(K-124): karistiricisiz kolda kahin PDR >= 0,95 tutan EN BUYUK "
        "telemetri hizi. Olcut harfiyen 2,0 seciyordu (PDR 0,9841) ama eksen "
        "dengesini BOZUYORDU: 39x1,0 + 4x0,25 = 40,0 pkt/s ve `esler_arasi` "
        "da 10x4,0 = 40,0 sunuyor; `trafik_deseni` bir TEDAVI ekseni oldugu "
        "icin 2,0 o ekseni IKI KAT YUKLE karistirirdi. Ogrenci 1,0'da kaldi. "
        "🔒 OLCUM HIZI SECMEDI, DOGRULADI: 1,0 esigi 0,9923 ile geciyor ve "
        "ucurumdan %150 uzakta (2,5'te tek tohumlar esigin altina dusuyor, "
        "3,0'da cokuyor). ⚠️ `02` §S4 kaynak boslugu KAPANMADI — 1,0 hala "
        "literatur capasi tasimiyor; degisen sey olculmus bir UST SINIRI ve "
        "beyan edilmis bir gerekcesi olmasidir"),
    "komut_akis_sayisi": ("DUNYA_TANIMI",
        "4 — referans dünyanın trafik tanımı (`v2/14` §trafik: *geçitten 4 "
        "düğüme komut 0,25 pkt/s*; K-169, birincil hücre K-186). Çift yönlü "
        "yolları sınar, yükteki payı küçük; 39×1,0 + 4×0,25 = 40,0 pkt/s ve "
        "`esler_arasi` da 10×4,0 = 40,0 sunar (K-126). TÜRETİLMİŞ "
        "kovasındaydı; sayı eşitlikten değil tanımdan gelir (denetim D-07 "
        "taraması, K-223)"),
    "komut_paket_hizi_hz": ("TEDAVI",
        "TEDAVİ ekseni — trafik yoğunluğu (`v2/15` C2, K-180). Varsayılan "
        "0,25 — telemetriye ORANLA gider (telemetri × 0,25) ve C3 taramasında"
        " o oranla birlikte oynadı; ayrı bir eksen açmak taramayı iki boyutlu"
        " yapardı ve komut akışı yükün küçük parçasıdır. 40 pkt/s dengesinin "
        "parçası (K-126)"),
    "rota_tamponu_kapasitesi": ("KAYNAK",
        "64 paket — uygulama kaynağı (K-198): ns-3 `aodv-routing-protocol.cc`"
        " `MaxQueueLen` varsayılanı 64; kuyruk dolunca EN ESKİ paket düşer "
        "(`aodv-rqueue.cc`) — buradaki kuralla aynı. ns-3 AODV'si NS-2'nin "
        "CMU/MONARCH modeline dayanır (Das ve Marina ayarlı). RFC 3561 §6.3 "
        "tamponlamayı şart koşar, sayı vermez. Sonlu olması gerekçeli: "
        "tavansız tampon sonsuz kuyruktur ve gecikme metriğini "
        "anlamsızlaştırır. Değerin SONUCA etkisi ayrıca ölçülecek (birincil "
        "hücrede 64 ↔ 256, `v2/12` İ-8c)"),
    "rota_tamponu_omru_s": ("KAYNAK",
        "30,0 s — uygulama kaynağı (K-198): ns-3 `MaxQueueTime` varsayılanı "
        "`Seconds(30)`; süresi dolan paket `Purge`da düşer. Süre tavanı AYRI "
        "bir tavandır ve gereklidir: sayı tavanı az sayıda paketin sonsuza "
        "kadar beklemesini engellemez. ⚠️ Ölçüm penceresine göre 30 s ÖNEMLİ "
        "bir süre — PDR'yi ve gecikmeyi doğrudan oynatabilir; etkisi birincil"
        " hücrede 30 ↔ 60 s ölçülecek (İ-8c)"),
    "kuyruk_kapasitesi": ("DUYARSIZ",
        "50 paket (NS-2 `ifqlen` geleneği; ns-3 MAC kuyruğu 500 · 500 ms, "
        "`02` G15). Kâhinin kuyruğu 25'e dolmuyor (iz birebir). Taban "
        "protokollerle (25 · 100): AODV ve AOMDV birebir; OLSR en büyük |Δ| "
        "= 0,0067 (TTL 32, band 0,0134) · 0,0053 (TTL 64, band 0,0107). "
        "Üretici: `kalibrasyon/duyarlilik.py`nin oynatmasıyla "
        "`arsiv/teshis/faz4_4_birincil_2026-10-02/protokol_tarama.py` (TTL "
        "32, K-214) ve "
        "`arsiv/teshis/faz4_4_k215_2026-10-06/protokol_kontrol.py` (TTL 64, "
        "K-217). DESPARETE mühürden önce son hâliyle yeniden"),
    "ttl_baslangic": ("KAYNAK",
        "referansta 64 — IP'nin önerilen varsayılan TTL'i: RFC 1700 'IP "
        "TIME TO LIVE PARAMETER' ve ns-3 `Ipv4L3Protocol::DefaultTtl` (`02` "
        "G17; `kanal/dunya.py::REFERANS_TTL`, öğrenci K-215). Yalnız VERİ "
        "paketinin ömrü (kontrol mesajlarının TTL'i yükte). Faz 4.4'te "
        "ölçüldü (K-214): AODV birebir, AOMDV duyarsız, OLSR DUYARLI (32 → "
        "64 Δ −0,079: döngüdeki paket kanalı doldurur) — bu yüzden kaynağa "
        "bağlandı. Eski dünyada 32"),
    "beacon_araligi_s": ("KAYNAK",
        "1 s = AODV `HELLO_INTERVAL` (RFC 3561 §10; `02` R1). Beacon yalnız "
        "kâhinlerde açık (dört protokolde koşum beacon'ı KAPALI, denetim "
        "B3): kâhinin kontrol yükü AODV'nin HELLO'suyla birebir (K-215). "
        "Faz 4.4 taramasında sınırdaydı (×0,5: 1,1R, K-214)"),
    "beacon_bayt": ("KAYNAK",
        "referansta 84 B = AODV HELLO çerçevesi: RREP 20 B (RFC 3561 §5.2, "
        "§6.9) + kontrol kapsüllemesi 64 B (`02` G15 · G16) — "
        "`kanal/dunya.py::REFERANS_BEACON_BAYT`, RREP biçimine testle bağlı "
        "(öğrenci K-215). Yalnız kâhinlerde etkin. Eski dünyada 32 B"),
    "komsu_omru_katsayisi": ("DUYARSIZ",
        "10 × beacon aralığı — komşu tablosunun BELLEK sınırı (tazelik "
        "kararı protokolün). Deneyde okuyan yok: dört protokolde beacon "
        "kapalı, kâhin tabloyu okumaz. Faz 4.4'te ölçüldü: ×0,5 · ×2'de |Δ| "
        "= 0,0000 (iz birebir). Üretici: `py -3.11 -u "
        "kalibrasyon/duyarlilik.py --dunya referans_2026 birincil …` (2 "
        "Ekim 2026, K-214). Bir protokol beacon açarsa yeniden ölçülür"),
    "karistirici_guc_override_dbm": ("KOL_TANIMI",
        "karıştırıcı şiddeti. 🔒 DUYARLILIK BORCU TAŞIMAZ ve sebebi ölçüm: bu "
        "sabit duyarlılık denetimini BEKLEMİYOR, çünkü ρ taraması onu zaten "
        "yedi güçte oynatıyor (−30 … −6 dBm) ve çalışma noktası o taramanın "
        "sonucudur. Varsayılanı `None`: koşu, kalibre edilmiş tabanı "
        "kullanır. Üretici: kalibrasyon/karistirici_gucu.py"),
    "karistirici_baslangic_s": ("TURETILMIS",
        "ölçüm penceresinden: temiz evre 100 s (4 000 paket, PDR SE ≈ 0,005),"
        " karıştırılmış evre 170 s. Toparlanma rota ömrü (89 s) ve protokol "
        "zamanlayıcıları mertebesinde"),
    "karistirici_konum": ("KOL_TANIMI",
        "None → alan merkezi — tekli merkez ailesinin tanımı (tohumlar arası "
        "karşılaştırılabilir). Eski dünyada oynatıldı, karar verilemedi (|Δ| "
        "0,048 kendi bandı içinde, 8 Eylül)"
        " · KAPSAM (K-204): keşifsel kolun tanımı — o kolun sonucu bu değere koşullu; birincil hücrenin kod yoluna girmez"),
    "darbe_periyodu_s": ("KOL_TANIMI",
        "2,7 s — darbeli kolun tanımı; keşifsel sınıf. Eski dünyada kendi "
        "kolunda DUYARLI çıktı (×2 → PDR −0,093, 8 Eylül)"
        " · KAPSAM (K-204): keşifsel kolun tanımı — o kolun sonucu bu değere koşullu; birincil hücrenin kod yoluna girmez"),
    "darbe_gorev_cevrimi": ("KOL_TANIMI",
        "%50 — darbeli kolun tanımı (açık/kapalı simetrisi); tepe telafisi "
        "buradan türer. Eski dünyada DUYARLI (×2 → PDR +0,066)"
        " · KAPSAM (K-204): keşifsel kolun tanımı — o kolun sonucu bu değere koşullu; birincil hücrenin kod yoluna girmez"),
    "taramali_konak_suresi_s": ("KOL_TANIMI",
        "100 ms — taramalı kolun tanımı (en hızlı protokol zamanlayıcısının "
        "onda biri); eski dünyada DUYARLI"
        " · KAPSAM (K-204): keşifsel kolun tanımı — o kolun sonucu bu değere koşullu; birincil hücrenin kod yoluna girmez"),
    "taramali_konak_sayisi": ("KOL_TANIMI",
        "3 konak — taramalı kolun tanımı; ortalama gücü −4,77 dB düşürür "
        "(`06` H1.3'te beyanlı); eski dünyada DUYARLI"
        " · KAPSAM (K-204): keşifsel kolun tanımı — o kolun sonucu bu değere koşullu; birincil hücrenin kod yoluna girmez"),
    "reaktif_sezme_s": ("KOL_TANIMI",
        "16 µs — reaktif kolun tanımı (`02` G5: < 4 µs geçiş ister; 16 µs ED "
        "süresi mertebesi); keşifsel"
        " · KAPSAM (K-204): keşifsel kolun tanımı — o kolun sonucu bu değere koşullu; birincil hücrenin kod yoluna girmez"),
    "reaktif_patlama_s": ("KOL_TANIMI",
        "144 µs — reaktif kolun tanımı (çevrim %90 görev); keşifsel"
        " · KAPSAM (K-204): keşifsel kolun tanımı — o kolun sonucu bu değere koşullu; birincil hücrenin kod yoluna girmez"),
}

# ===========================================================================
# MODÜL SABİTLERİ — davranış ya da ölçüm belirleyen sabitler
# ===========================================================================
# Anahtar `dosya::AD`; `mimari_denetimi.py` (D12, D13) bu dosyaları
# tarar ve burada olmayanı bulgu sayar. Yalnız dizgi tutar, hiçbir şey
# içe aktarmaz.
MODUL_KOKENLERI: dict[str, tuple[str, str]] = {
    "sim2/yapilandirma/konfig.py::DSSS_KANAL_BANDI_HZ": ("KAYNAK",
        "22 MHz — `02` G1 (Pei & Henderson 2009): 802.11b gürültüsü 22 "
        "MHz'lik kanalda; işlem kazancı Eb/N0 = SINR·B/R_b bu banttan (A2, "
        "K-173)"),
    "sim2/yapilandirma/konfig.py::HIZLAR_BPS": ("KAYNAK",
        "1 · 2 · 5,5 · 11 Mb/s — `02` G1 (DBPSK, DQPSK, CCK 5,5/11) ve G2 "
        "(DSSS 1/2 Mb/s); ARF'nin basamakları (A4, K-177)"),
    "sim2/kanal/cerceve.py::HIZ_MODULASYONU": ("KAYNAK",
        "1 Mb/s DBPSK · 2 Mb/s DQPSK · 5,5/11 Mb/s CCK — `02` G1; önbelge her"
        " hızda 1 Mb/s DBPSK (G2). Çerçeve düzeyinde kip (A4, K-177)"),
    "sim2/kanal/yer_hava.py::A2G_ORTAMLARI": ("KAYNAK",
        "`02` G6 (Al-Hourani 2014): ortam parametreleri (α, β, γ) Şekil 2 "
        "metninden, ek kayıp (η_LoS, η_NLoS) §III'ten — banliyö (0,1; 21) · "
        "kentsel (1,0; 20) · yoğun (1,6; 23) · yüksek (2,3; 34) dB (A6, "
        "K-176)"),
    "sim2/kanal/dunya.py::REFERANS_TTL": ("KAYNAK",
        "64 — RFC 1700 'IP TIME TO LIVE PARAMETER' · ns-3 `DefaultTtl` "
        "(`02` G17, öğrenci K-215)"),
    "sim2/kanal/dunya.py::REFERANS_EIRP_DBM": ("KAYNAK",
        "20 dBm — `02` G7: Avrupa EIRP sınırı 100 mW (2,4 GHz); `v2/14` §1 "
        "(A7, K-178)"),
    "sim2/kanal/dunya.py::REFERANS_GOREV_YARICAPI_M": ("OLCULMUS",
        "16 km — Üretici: `python kalibrasyon/calisma_noktasi.py --dunya "
        "referans_2026 --bolum gorev_kolu` (8 tohum × 3 an; 33 km). Görev "
        "derecesi 8,10 ↔ bağımsız 8,16 (fark 0,06, oran 0,993); ızgara 6–16 "
        "km, 2r < alan sınırı 16,5 km (K-188)"),
    "sim2/kanal/dunya.py::REFERANS_PAY_DB": ("DUNYA_TANIMI",
        "10 dB — nominal bağın PER %10 duyarlılığının üstündeki payı; menzil "
        "ve yerleşim ondan türer (`v2/14` §1: 10 dB payla 1,65 km; onaylı "
        "K-169)"),
    "sim2/kanal/dunya.py::REFERANS_ALAN_M": ("OLCULMUS",
        "33 km — Üretici: `python kalibrasyon/calisma_noktasi.py --dunya "
        "referans_2026 --bolum alan_taramasi 25000 30000 33000 35000 37000 "
        "40000 45000` (30 tohum; K-188, gölgeleme birimi düzeltilmiş). "
        "Altındaki HER alanın kopmadığı en büyük alan: derece 9,67, derin "
        "çift %26,9. 35 ve 37 km kopar; 40 km'nin geçmesi örnekleme şansı. "
        "(K-185'teki 35 km hatalı gölgeleme birimiyle ölçülmüştü.) `v2/14` "
        "§3'ün ~6–8 km'si 10 dB paylı nominal bağa dayanıyordu; simülatörün "
        "kanalında bağ ~9–10 km. Öğrenci gerçekçiliği öne koydu, karar ajanın"
        " (K-185). ⚠️ Gövde gölgelemesi ve anten yönelimi modellenmiyor — bağ"
        " üst sınır, alan da öyle"),
    "sim2/kanal/dunya.py::REFERANS_KARISTIRICI_DBM": ("DUNYA_TANIMI",
        "40 dBm (10 W) — öğrenci kararı K-186; `karistirici_taban_dbm` bunu "
        "yazar"),
    "sim2/kanal/cerceve.py::KONTROL_KAPSULLEME": ("KAYNAK",
        "MAC 24 + FCS 4 + LLC/SNAP 8 + IPv4 20 + UDP 8 = 64 B — `02` G15 "
        "(802.11 başlığı, FCS) · G16 (RFC 1042, 791, 768)"),
    "sim2/kosum/kontrol.py::BEKLEYEN_UYANDIRMA_TAVANI": ("OLCULMUS",
        "256 — güvenlik sınırı: aşılırsa koşu deterministik DURUR, tamamlanan"
        " hiçbir sonucu değiştiremez. Referans dünyada kontrol düzlemli 21 "
        "regresyon satırının hepsinde tepe bekleyen ≤ 22 (DESPARETE; taban "
        "protokoller ≤ 9) — hiç bağlamıyor. Üretici: satırlar `python -u "
        "kalibrasyon/regresyon_satirlari.py uret k204`, okuma `arsiv/teshis/"
        "faz4_4_birincil_2026-10-02/k_kalemleri.py` (2 Ekim 2026, K-214). "
        "DESPARETE Faz 5'te değişince regresyondan yeniden okunur"),
    "sim2/kanal/yayilim.py::BOLTZMANN": ("KAYNAK",
        "SI tanımlı sabit; tartışma konusu değil"),
    "sim2/kanal/yayilim.py::ISIK_HIZI": ("KAYNAK",
        "SI tanımlı sabit; tartışma konusu değil"),
    "sim2/kanal/yayilim.py::REFERANS_MESAFE_M": ("TURETILMIS",
        "1 m — log-mesafe modelinin referansı. Serbest bir seçim değil: PL(1 "
        "m) kapalı formda hesaplanıyor ve model onun üstüne kuruluyor"),
    "sim2/kanal/sonumleme.py::YENILIK_ONBELLEK_SINIRI": ("OLCULMUS",
        "kalibrasyon/sonumleme_onbellegi.py — 1 000 000 · 250 000 · 100 000 "
        "sınırlarının ÜÇÜ de sınırsız hâlle BİREBİR aynı sonucu verdi; "
        "ıskalama artışı sırasıyla %0,09 · %0,36 · %0,88"),
    "sim2/kanal/sonumleme.py::AGIRLIK_ONBELLEK_SINIRI": ("TURETILMIS",
        "20 000 — FIR ağırlık önbelleğinin tavanı (performans, 28 Eylül "
        "2026). Sonucu DEĞİŞTİREMEZ: ağırlıklar aynı işlemle aynı sırada "
        "üretilir, dolunca boşaltılır ve yeniden hesaplanır; yalnız süreyi ve"
        " belleği belirler. Birebirlik tam sonuç satırı karşılaştırmasıyla ve"
        " regresyonla gösterilir"),
    "sim2/kanal/sonumleme.py::PENCERE_ONBELLEK_SINIRI": ("TURETILMIS",
        "20 000 — blok üretecinin (K-198) pencere önbelleği tavanı. Sonucu "
        "DEĞİŞTİREMEZ: pencere indeksin saf fonksiyonu, dolunca boşaltılır ve"
        " aynı değerle yeniden üretilir (`test_K198_blok_IZLER_…` tavanı 3 "
        "yapıp tahliye altında izi karşılaştırır). Girdi ~2,3 KB → tavanda "
        "~46 MB; birincil hücrenin 4 s'lik koşusunda 4 tahliye"),
    "sim2/kanal/yayilim.py::YAVAS_ONBELLEK_SINIRI": ("TURETILMIS",
        "1<<18 — yavaş kayıp önbelleğinin tavanı (K-190). Sonucu "
        "DEĞİŞTİREMEZ: anahtar tam girdidir, dolunca boşaltılır ve değer aynı"
        " işlemle yeniden hesaplanır; yalnız süreyi ve belleği belirler. "
        "Birebirlik regresyonla gösterilir"),
    "sim2/kanal/yayilim.py::KOSE_ONBELLEK_SINIRI": ("OLCULMUS",
        "1<<19 gölgeleme köşe önbelleği. 🟢 18 Eylül 2026'da ÖLÇÜLDÜ (`python "
        "-u kalibrasyon/sonumleme_onbellegi.py 4`): sınır 1 024 ↔ 4 194 304 "
        "arasında **4 096 kat** oynatıldı, DÖRT değerde de sonuç satırı VE "
        "ham teslim imzası BİREBİR aynı çıktı (hareketli kol, `bagimsiz-yok` "
        "1000, 50 s). Ölçüt taramadan ÖNCE yazıldı. Bedel yalnız süre: en "
        "küçük sınırda %7 yavaşlama (133 → 142 s). Saf memo olduğu artık bir "
        "iddia değil, bir kapı"),
    "sim2/yapilandirma/senaryolar.py::MOBILITE_BOLUNME": ("OLCULMUS",
        "ESKİ DÜNYA (regresyonun eski vakaları). Üretici: `python -u "
        "kalibrasyon/dugum_sayisi.py --bolunme` (16 Eylül 2026); referans "
        "karşılığı `MOBILITE_BOLUNME_REFERANS`"),
    "sim2/yapilandirma/senaryolar.py::BOLUNME_OLCULEN_ARALIK": ("KOL_TANIMI",
        "Ana deney tohumları (2000–2039), `06` §2. Hangi tohumların "
        "ölçüldüğünü tanımlar; bu aralığın DIŞINDAKİ bir tohumda "
        "`bolunme_payi` `None` döner — *'bölünme yok'* ile *'bakılmadı'* ayrı"
        " (`None ≠ 0`). Duyarlılık borcu YOK: bir ölçümün kapsamıdır, sonucu "
        "belirleyen bir değer değildir."),
    "sim2/yapilandirma/senaryolar.py::MOBILITE_THETA_REFERANS": ("OLCULMUS",
        "Üretici: `python -u kalibrasyon/theta_kollari.py --dunya "
        "referans_2026` (27 Eylül 2026, K-188; 33 km, gölgeleme 2,5 km, 6 "
        "tohum). Bağımsız 5,15 · görev 2,79 · formasyon tanımsız (%99,6 "
        "kopmuyor, tek ömür) · statik tanımsız"),
    "sim2/yapilandirma/senaryolar.py::MOBILITE_BOLUNME_REFERANS": ("OLCULMUS",
        "Üretici: `python -u kalibrasyon/dugum_sayisi.py --dunya "
        "referans_2026 --bolunme` (27 Eylül 2026, K-188; 33 km). 8/160 "
        "bölünmüş (kol, tohum); çoğu tek kenar düğümü"),
    "sim2/yapilandirma/senaryolar.py::MOBILITE_THETA": ("OLCULMUS",
        "ESKİ DÜNYA. Üretici: `python -u kalibrasyon/theta_kollari.py` (14 "
        "Eylül 2026); referans karşılığı `MOBILITE_THETA_REFERANS`"),
    "sim2/yapilandirma/senaryolar.py::KARISTIRICI_GUCU_DBM": ("OLCULMUS",
        "ESKİ DÜNYA — ρ kalibrasyonu (`kalibrasyon/karistirici_gucu.py`, −15 "
        "dBm, ρ 0,258). Referans dünyada güç öğrenci kararıdır "
        "(`REFERANS_KARISTIRICI_DBM`)"),
    "sim2/kanal/sonumleme.py::FIR_EN_COK_KATSAYI": ("TURETILMIS",
        "64 × 190 µs = 12,2 ms. Marjinal varyans `c` ile düzeltildiği için "
        "derinliği değil yalnız korelasyonun taşındığı mesafeyi belirliyor"),
    "sim2/kanal/sonumleme.py::BAGIL_HIZ_TABANI_MS": ("OLCULMUS",
        "1 m/s — sıfır hızda T_c'nin sonsuza gitmesini önler. Referans "
        "dünyada çift-anların %0,2'sinde (formasyon), bağımsız ve görevde %0 "
        "bağlar. Üretici: `py -3.11 kalibrasyon/bagil_hiz_tabani.py` (30 "
        "Eylül 2026)"),
    "sim2/dunya/mobilite.py::ISTASYON_TUTMA_S": ("DUNYA_TANIMI",
        "2 s — istasyon tutma zaman sabiti; görev ve formasyon kollarının "
        "(birincil hücre) mobilite tanımı · DÜNYA TANIMI (öğrenci, K-220): "
        "sonuçlar bu değere koşullu, ölçülen duyarlılık raporda. Faz 4.4'te "
        "20 tohumla ×2'de pdr_atlama +0,016 (1,1R, band 1,1×), pdr_etx "
        "+0,001; ×0,5 duyarsız. Üretici: `py -3.11 -u "
        "kalibrasyon/duyarlilik.py --dunya referans_2026 birincil --tohum "
        "20 …` (7 Ekim 2026, K-217)"),
    "sim2/olcum/metrikler.py::YUZDELIKLER": ("TURETILMIS",
        "(50, 95, 99) — ortanca + iki kuyruk. Bir DEĞER seçimi değil, sonuç "
        "şemasının kapalı listesi: sonradan eklemek eski satırları "
        "karşılaştırılamaz yapar. Karara değil rapora girer"),
    "sim2/olcum/evre.py::IZGARA_ADIMI_S": ("KAYNAK",
        "1 s — RFC 3561 §10, AODV `HELLO_INTERVAL` = '1,000 Milliseconds'. "
        "Birincil belge 8 Eylül 2026'da açıldı ve `02` §R1'e işlendi. Evre "
        "kafesinin ÇÖZÜNÜRLÜĞÜ: iki taban çizgisinin komşu yenileme "
        "aralıkları AODV 1 s ve OLSR 2 s (RFC 3626 §18), yani 1 s EN "
        "HIZLISIDIR — daha ince bir ızgara hiçbir protokolün gösteremeyeceği "
        "bir hızı ölçmeye çalışırdı"),
    "sim2/olcum/evre.py::PENCERE_S": ("KAYNAK",
        "15 s — RFC 3626 §18, OLSR `TOP_HOLD_TIME` = '3 x TC_INTERVAL' ve "
        "`TC_INTERVAL` = '5 seconds'. Birincil belge 8 Eylül 2026'da açıldı "
        "ve `02` §R2'ye işlendi. Evre kafesinin DURAĞANLIĞI: en yavaş taban "
        "çizgisinin topoloji bilgisini tuttuğu süre. AYNI ÇAPA Θ'nın "
        "paydasıdır (K-101) — iki yerde iki farklı çapa kullanmak, ikisinin "
        "ayrışması demek olurdu"),
    "sim2/olcum/evre.py::ALFA": ("TURETILMIS",
        "0,05 — ön-kaydın tek α'sı (`06` §7); M3'ün z'si ve M4'ün eşiği "
        "buradan türer (K-123)"),
    "sim2/gozlem/yuk.py::YUK_BOOL_BAYT": ("TURETILMIS",
        "1 bayt — bir bool'un kablodaki asgari bedeli"),
    "sim2/gozlem/yuk.py::YUK_FLOAT_BAYT": ("TURETILMIS",
        "4 bayt — tek duyarlıklı float; çift duyarlık bir protokol için "
        "savunulamaz bir lüks"),
    "sim2/gozlem/yuk.py::YUK_INT_TABAN_BAYT": ("TURETILMIS",
        "1 bayt taban; büyüklüğe göre büyüyor"),
    "sim2/gozlem/teshis.py::TESHIS_EN_UZUN_AD_BAYT": ("TURETILMIS",
        "teşhis sözlüğü rapora girer, karara girmez; sınırlar bellek koruması"),
    "sim2/gozlem/teshis.py::TESHIS_EN_UZUN_DIZGI_BAYT": ("TURETILMIS",
        "aynı gerekçe"),
    "sim2/gozlem/teshis.py::TESHIS_EN_COK_ALAN": ("TURETILMIS",
        "aynı gerekçe"),
    "sim2/gozlem/teshis.py::TESHIS_EN_COK_ELEMAN": ("TURETILMIS",
        "aynı gerekçe"),
    "kalibrasyon/kahin.py::ATLAMA_ESIGI": ("KOL_TANIMI",
        "0,90 — EN KISA YOL kâhininin TANIMI: 'kullanılabilir bağ' = "
        "yeniden denemelerle teslim olasılığı ≥ 0,90. ETX kâhini eşik "
        "kullanmaz (U1 paydası değil; Faz 4.4'te pdr_etx birebir). Aletin "
        "tanımı olduğu için DUYARLI olması tanım gereği: 0,95 → pdr_atlama "
        "+0,049 · 0,80 → −0,077 (`py -3.11 -u kalibrasyon/duyarlilik.py "
        "--dunya referans_2026 birincil "
        "kalibrasyon/kahin.py::ATLAMA_ESIGI`, 2 Ekim 2026, K-214). Hiçbir "
        "hipoteze ve U1'e girmez; `olcut_bedeli`nin (çözünürlük R'nin "
        "ikilisi, K-128) ve K-192 (b) zarfının bir üyesi. Öğrenci K-215"),
    "kalibrasyon/kahin.py::SONUMLEME_ORNEGI": ("OLCULMUS",
        "48 örnek — kâhinin bağ başına sönümleme KESTİRİMİNİN örneklemi "
        "(sayısal parametre; hareketli kollarda, statikte tek örnek). "
        "Ölçüldü: ETX kâhininin PDR'si 6 · 12 · 24 · 48 örnekte birincilde "
        "0,840 · 0,870 · 0,874 · 0,880, bağımsız-yokta 0,790 · 0,820 · "
        "0,844 · 0,854; N → 2N adımı birincilde 12'den, bağımsız-yokta "
        "24'ten sonra |Δ| < R ve band içinde. Tam yakınsama DEĞİL: 48'de "
        "kalan artış tahminen ≤ ~0,01 (bağımsız-yokta 24 → 48 hâlâ +0,010; "
        "96 Faz 6'da, denetim D-15). Koşu süresi N'den bağımsız → 48 "
        "(öğrenci K-215). Üretici: `kalibrasyon/duyarlilik.py`nin "
        "koşucusuyla "
        "`arsiv/teshis/faz4_4_birincil_2026-10-02/sonumleme_yakinsama.py` "
        "(2 Ekim 2026, K-214). 6 örnekte kâhin yakınsamamıştı"),
    "kalibrasyon/kahin.py::SONUMLEME_ADIMI_S": ("TURETILMIS",
        "5 ms — sönümleme tutarlılık süresinden (~2 ms) BÜYÜK seçildi ki "
        "örnekler bağımsız olsun; küçük seçilseydi aynı fade tekrar sayılırdı"),
    "kalibrasyon/kahin.py::ETX_TAVANI": ("TURETILMIS",
        "1e9 — p = 0 olan bağlar için sonsuz yerine büyük bir sayı; "
        "Dijkstra'yı basitleştirir ve bu bağlar zaten hiç seçilmez. Bir DEĞER"
        " seçimi değil, sonsuzun sonlu karşılığı"),
    "kalibrasyon/kayip_anatomisi.py::BAG_DILIMI_S": ("TURETILMIS",
        "5 s — yalnız TEŞHİS (K-193): hareketli ya da karıştırıcılı kolda "
        "protokolün karar bağlarının kâhin kalitesinin okunduğu dilim. "
        "`derin_sizma`nın 15 s açık · 15 s kapalı çizelgesinin üçte biri — "
        "her evre en az iki dilimle örneklenir. Başarısız bağlar dilimsiz, "
        "düşüş anında okunur. Simülasyona ve protokol kararına girmez"),
    "kalibrasyon/calisma_noktasi.py::BASARI_ESIGI": ("TURETILMIS",
        "0,90 — `kahin.py::ATLAMA_ESIGI` ile aynı sayı, bilerek (iki eşik "
        "ayrışmasın)"),
    "kalibrasyon/calisma_noktasi.py::SONUMLEME_ORNEGI": ("TURETILMIS",
        "6 — `kahin.py::SONUMLEME_ORNEGI` ile aynı sayı, aynı ölçüm"),
    "kalibrasyon/calisma_noktasi.py::UZAK_KESME_M": ("TURETILMIS",
        "1200 m — bu mesafenin ötesinde PER zaten 1; hesap kısaltması. Sonucu"
        " değiştiremez, yalnız işi azaltır"),
    "kalibrasyon/calisma_noktasi.py::ALANLAR": ("TEDAVI",
        "(1000…2000 m) — alan büyüklüğü TARAMASININ ekseni. Bir değer değil, "
        "aranan aralık; çalışma noktası (1800 m) bu taramanın SONUCU"),
    "kalibrasyon/calisma_noktasi.py::ALANLAR_REFERANS": ("TEDAVI",
        "(5…30 km) — referans dünyada alan taramasının ekseni; seçilen 35 km "
        "komut satırından genişletilmiş taramanın SONUCU (K-185)"),
    "kalibrasyon/calisma_noktasi.py::YARICAPLAR": ("TEDAVI",
        "(250…750 m) — görev kolu yarıçap taramasının ekseni (eski dünya; "
        "K-183'e kadar satır içindeydi)"),
    "kalibrasyon/calisma_noktasi.py::YARICAPLAR_REFERANS": ("TEDAVI",
        "(6…16 km) — aynı eksen referansta; alan 35 km (K-185) → alan "
        "oranıyla ~12,6 km, ızgara onu kuşatır (K-187)"),
    "kalibrasyon/calkanti.py::OLSR_TOP_HOLD_S": ("KAYNAK",
        "15 s — RFC 3626 §18, OLSR `TOP_HOLD_TIME` = 3 × `TC_INTERVAL` ve "
        "`TC_INTERVAL` = 5 s. Birincil belge 8 Eylül 2026'da açıldı, `02` "
        "§R2. Θ'nın PAYDASI budur"),
    "kalibrasyon/duyarlilik.py::R_ESLESTIRILMIS": ("OLCULMUS",
        "0,0126 — birincil hücrede eşleştirilmiş çözünürlük, KISA PENCERE "
        "kesitinde (koşu 50 s, ölçüm 10–40 s, karıştırıcı 5. s'de; "
        "duyarlılık taramasının penceresi) — ana deneyin 270 s'lik "
        "penceresinin çözünürlüğü DEĞİL; o Faz 6'da δ ölçümüyle aynı "
        "koşulardan ölçülür ve DUYARSIZ'lar ona karşı yeniden okunur "
        "(denetim D-03). Yakınsamış kâhinle (48 örnek), en çok 7 iletim "
        "denemesiyle (K-223); 40 tohum, `olcut_bedeli` SD 0,0400; kâhin PDR "
        "0,8675. Üretici: `py -3.11 -u kalibrasyon/cozunurluk.py --dunya "
        "referans_2026 --hucre birincil --tohum 40` (9 Ekim 2026, 69 dk, "
        "K-224). DUYARSIZ kayıtlarının en büyük |Δ|'sı 0,0118 < 0,0126 — "
        "hiçbiri dönmedi. Önceki: 0,0142 (8 deneme, K-216) · 0,0188 (6 "
        "örnekli kâhin, K-213) · eski dünya 0,0230"),
    "kalibrasyon/calkanti.py::ETKIN_YARICAP_M": ("TURETILMIS",
        "400 m — yalnız `calkanti.py`nin hızlı teşhis taramasında; hiçbir "
        "karar taşımaz (Θ yavaş SINR tanımıyla ölçülür, `theta_kollari.py`)"),
    "kalibrasyon/calkanti.py::ADIM_S": ("TURETILMIS",
        "1 s rota ömrü örnekleme adımı — ölçülen ömürler adımın çok üstünde; "
        "örneklemdir, karar hata payıyla okunur"),
    "kalibrasyon/calkanti.py::BITIS_S": ("TURETILMIS",
        "350 s — `Konfig.kosu_bitis_s` ile aynı koşu uzunluğu; Θ ölçümü "
        "gerçek koşuyla aynı zaman ölçeğinde yapılsın diye"),
    "kalibrasyon/calkanti.py::CIFT_SAYISI": ("TURETILMIS",
        "40 çift — tohum başına örneklem; Θ'nın hata payı çıktıda, karar (Θ ≥"
        " 3) payın üstünde"),
    "kalibrasyon/karistirici_gucu.py::GUCLER_REFERANS": ("TEDAVI",
        "(20…47 dBm) — referans dünyada güç taramasının ekseni; `v2/14` §4'ün"
        " kaynak bandı: İHA taşıyıcılı 1–5 W · taşınabilir 10 W · araç 50 W "
        "(K-183)"),
    "kalibrasyon/karistirici_gucu.py::MESAFE_ORANLARI": ("TEDAVI",
        "(0…1,5 × yarım kenar) — karıştırıcı mesafe taramasının ekseni: "
        "merkez, kenar ve alan dışı (K-183)"),
    "kalibrasyon/karistirici_gucu.py::BUYUK_BOLUNME_ORANI": ("TURETILMIS",
        "0,10 — ikinci bileşen ≥ bir MÜFREZE (N/10 = 4 İHA; "
        '`gorev_grup_sayisi` 10 × 4 üye). Sert kısıtın gerekçesi "ağın İKİ '
        'BÜYÜK parçaya ayrılması"; daha küçük kopuk grup boğulmadır (K-186)'),
    "kalibrasyon/karistirici_gucu.py::ISCI": ("TURETILMIS",
        "8 — havuz işçisi (çalışma kuralı). Sonucu DEĞİŞTİRMEZ: tohum "
        "sonuçları `map` ile tohum sırasıyla toplanır; yalnız süreyi belirler"),
    "kalibrasyon/karistirici_gucu.py::TESHIS_X": ("TURETILMIS",
        "0,60 — teşhis varyantının batıya kaydırılmış x'i (depodaki 0,75 "
        "yerine). Bir ölçüt değil, *konum mu suçlu* sorusunun ikinci noktası;"
        " cevap HAYIR çıktı (K-127)"),
    "kalibrasyon/yere_toplama_yuku.py::MARJ_HIZLARI": ("TURETILMIS",
        "(2,25 · 2,50) — ilan edilmiş ızgaranın 2,0 ile 3,0 arasındaki "
        "boşluğunu dolduran iki nokta. 🔒 Bir ÖLÇÜT DEĞİL: seçilen hızı "
        "büyütemez, yalnız çalışma noktasının uçuruma uzaklığını ölçer "
        "(K-126)"),
    "kalibrasyon/yere_toplama_yuku.py::ESLER_HIZLARI": ("TURETILMIS",
        "(4,0 · 8,0) — bugünkü eşler arası akış hızı ve İKİ KATI; ikincisi "
        "*iki deseni 80 pkt/s'te eşitlemek mümkün mü* sorusunun cevabıdır "
        "(geçti, ama kullanılmadı: öğrenci 1,0'da kaldı — K-126)"),
    "kalibrasyon/yere_toplama_yuku.py::ADAYLAR_HZ": ("TEDAVI",
        "(0,5…3,0 pkt/s) — telemetri hızı TARAMASININ ekseni. Bir değer "
        "değil, aranan aralık; bugünkü varsayılan (1,0) içeride, seçilen hız "
        "bu taramanın SONUCU (K-126)"),
    "kalibrasyon/yere_toplama_yuku.py::KOMUT_ORANI": ("TURETILMIS",
        "0,25 — komut hızı telemetriye ORANLA gider; bugünkü çiftin (1,0 ↔ "
        "0,25) oranı korunur. Ayrı bir eksen açmak taramayı iki boyutlu "
        "yapardı ve komut akışı yükün küçük parçasıdır"),
    "kalibrasyon/yere_toplama_yuku.py::TESLIM_ESIGI": ("TEDAVI",
        "0,95 — ilan edilmiş ölçüt (K-124): karıştırıcısız kolda kâhin PDR bu"
        " eşiğin üstünde kalmalı. Ölçütün kendisi; taramadan ÖNCE öğrenci "
        "onayıyla yazıldı, ölçülen bir sayı değil"),
    "kalibrasyon/yere_toplama_yuku.py::YAN_GOZLEM_PENCERESI": ("TURETILMIS",
        "Kısa pencere (ısınma 10 s · ölçüm 30 s · koşu 50 s) — regresyon "
        "matrisinin kısa vakalarıyla AYNI. Yan gözlem bir KAPI değildir ve "
        "hareketli kolda tam uzunluk kâhin koşusu 10 dakikanın üstünde "
        "sürüyor (ölçüldü)"),
    "kalibrasyon/dugum_sayisi.py::ADAYLAR": ("TEDAVI",
        "(30…50) — düğüm sayısı TARAMASININ ekseni; `12` §3 C1 aralığı. Bir "
        "değer değil, aranan küme. Sonuç: adaylar ayrılamadı (K-125)"),
    "kalibrasyon/dugum_sayisi.py::ALAN_CAPASI_M": ("OLCULMUS",
        "ESKİ DÜNYA — N = 40 için 1 800 m (`kalibrasyon/calisma_noktasi.py`); referansta "
        "alan `REFERANS_ALAN_M`"),
    "kalibrasyon/dugum_sayisi.py::CAPA_N": ("TURETILMIS",
        "40 — çapanın ölçüldüğü düğüm sayısı; `ALAN_CAPASI_M` ile AYNI "
        "ölçümden gelir, ondan ayrı bir seçim değildir"),
    "kalibrasyon/dugum_sayisi.py::ALTERNATIF_ORAN": ("TEDAVI",
        "0,90 — ilan edilmiş sert kısıt (K-124): geçide düğüm-ayrık ikinci "
        "yolu olan kaynakların en az bu payı. Ölçütün kendisi; taramadan ÖNCE"
        " öğrenci onayıyla yazıldı, ölçülen bir sayı değil"),
    "kalibrasyon/aodv_uygunluk.py::U1_ESIK_STATIK": ("TEDAVI",
        "0,90 — U1'in statik koldaki ölçütü (`06` §4.3): AODV'nin PDR'si, "
        "AYNI konfigürasyonda koşan ETX kâhininin PDR'sine bu orandan az "
        "olamaz. Ölçütün kendisi; öğrenci kararı (K-136), ölçülen bir sayı "
        "DEĞİL. ⚠️ Ölçüm GÖRÜLDÜKTEN SONRA seçildi ve bu, ön-kayıt "
        "disiplininin zayıf tarafıdır — U1 bir kabul kapısı olduğu ve hiçbir "
        "sonuç iddiası ona dayanmadığı için taşınıyor; gerekçe dosyanın "
        "başlığında açık. Üretici: `python -u kalibrasyon/aodv_uygunluk.py`"),
    "kalibrasyon/aodv_uygunluk.py::U1_ESIK_HAREKETLI": ("TEDAVI",
        "0,60 — U1'in hareketli koldaki ölçütü. Statikten düşük olmasının "
        "sebebi `06` §4.3'te zaten yazılı: kâhin her an en güvenilir yolu "
        "BİLİR, gerçek protokol onu HELLO gecikmesi kadar sonra öğrenir. "
        "Ölçütün kendisi; öğrenci kararı (K-136). Aynı zayıflık beyanı "
        "`U1_ESIK_STATIK`teki gibidir. Üretici: `python -u "
        "kalibrasyon/aodv_uygunluk.py`"),
    "kalibrasyon/aodv_uygunluk.py::TOHUMLAR": ("TEDAVI",
        "(1000, 1001, 1002) — GELİŞTİRME tohumları. Ana deney tohumları "
        "(2000–2039) burada koşulmaz: `06` §0.2 *'hiçbir kolda koşulmaz'* der"
        " ve mühür bozulmaz. Üç tohum bir kabul kapısı için yeterlidir; U1 "
        "bir hipotez testi değildir, güç hesabı gerektirmez"),
    "kalibrasyon/sonumleme_onbellegi.py::KOSE_SINIRLARI": ("TEDAVI",
        "(1<<22, 1<<19, 1<<14, 1<<10) — gölgeleme köşe önbelleği sınırının "
        "TARAMA ekseni, bir değer değil. Aralık 4 096 kat seçildi: memo saf "
        "değilse bu genişlikte kesinlikle ayrışır. Varsayılan (1<<19) "
        "aralığın ortasında. Üretici: `python -u "
        "kalibrasyon/sonumleme_onbellegi.py 4`"),
    "kalibrasyon/aodv_uygunluk.py::ACIKLANMIS_DUSUK": ("TEDAVI",
        "U1-B'nin açıklanmış düşük hücreleri, PROTOKOL BAŞINA (`06` §4.4 "
        "madde 3 · K-137 · K-142: bir protokolün açıklaması öbürünü aklamaz)."
        " Bir eşik değil, bir MUAFİYET listesi ve girmesinin şartı ÖLÇÜM: "
        "kaybın protokolün kendi mekanizmasından geldiği gösterilmiş olmalı. "
        "🔒 Liste iki yönden denetleniyor — listede olmayan düşük hücre ve "
        "artık düşük olmayan liste kaydı, ikisi de kapıyı kırmızı yakar"),
    "kalibrasyon/aodv_uygunluk.py::ACIKLANMIS_DUSUK_REFERANS": ("TEDAVI",
        "Referans dünyada U1-B'nin açıklanmış düşük hücreleri, anahtar "
        "(desen, kol, tohum) — `ACIKLANMIS_DUSUK`un referans dünya karşılığı "
        "(K-196 OLSR-c · K-207 AODV-i). Bir eşik değil, MUAFİYET listesi; "
        "girmesinin şartı ölçüm ve mekanizma (K-193, K-208). Ölü kayıt "
        "taraması aynı: artık düşük olmayan kayıt kapıyı kırmızı yakar"),
    "kalibrasyon/aodv_uygunluk.py::KAHIN_ASIMI_ACIKLANMIS": ("TEDAVI",
        "K-192 (b) zarf beyanları, anahtar (desen, kol, tohum): ETX kâhinini "
        "aşan hücre, aynı hücrede üç kâhinin zarfının İÇİNDEYSE girer (K-206,"
        " K-211); zarfı da aşan giremez, yazılım hatası aranır. Ölü kayıt "
        "taraması araçta (artık aşmayan kayıt kırmızı)"),
    "kalibrasyon/aodv_uygunluk.py::U3_SURELERI_S": ("TEDAVI",
        "(60, 120) s — U3 yük profilinin ÖLÇÜM ekseni, bir değer değil. İki "
        "süre, yükün süreyle nasıl büyüdüğünü tek bir oranla söyler: ~2 sabit"
        " hız, belirgin biçimde 2'nin altı başta yığılan yük. Küçük test "
        "dünyası `tests2/test_kosum.py::_konfig`. Üretici: `python -u "
        "kalibrasyon/aodv_uygunluk.py u3` (K-144)"),
    "kalibrasyon/aodv_uygunluk.py::DUMAN_PENCERESI": ("TURETILMIS",
        "Kısa pencere (ısınma 10 s · ölçüm 40 s · koşu 50 s) — duman kesiti "
        "SAYIYI ÜRETMEZ. Tam pencerede tek bir (AODV, kâhin) çifti 505 s "
        "sürüyor, yani `uretici_duman.py`nin 'ucuz kesit' sözleşmesi tam "
        "pencereyle tutturulamaz. "
        "`yere_toplama_yuku.py::YAN_GOZLEM_PENCERESI` ile AYNI idiom ve aynı "
        "beyan"),
    "kalibrasyon/aodv_uygunluk.py::DUMAN_TOHUMLARI": ("TEDAVI",
        "(1000,) — duman kesitinin tohumu; `TOHUMLAR`ın ilki. Kesit SAYIYI "
        "ÜRETMEZ, yalnız aletin hâlâ koştuğunu gösterir (`uretici_duman.py` "
        "sözleşmesi): tam koşum 24 koşumdur, duman 2'dir"),
    "kalibrasyon/theta_kollari.py::AODV_ACTIVE_ROUTE_S": ("KAYNAK",
        "3 s — RFC 3561 §10, AODV `ACTIVE_ROUTE_TIMEOUT` = '3,000 "
        "Milliseconds'. Birincil belge 8 Eylül 2026'da açıldı ve `02` §R1'e "
        "işlendi; `olcum/evre.py::IZGARA_ADIMI_S` ile AYNI kaynak. Θ'nın "
        "ikinci paydası"),
    "kalibrasyon/evre_metrikleri_kapilari.py::CIZ_TOHUMLAR": ("TEDAVI",
        "(1003, 1004) — çizelgeli karıştırıcı kapılarının (G1ç · G2ç · G4ç, "
        "K-209) GELİŞTİRME tohumları; K-200 birincil hücre partisinin "
        "tohumları, yani anatomisi bilinen koşular. Ana tohumlar (2000–2039) "
        "koşulmaz. Verdikt kol ortalamasında; tek tohum bilgisiz (K-212)"),
    "kalibrasyon/duyarlilik.py::TOHUMLAR": ("TURETILMIS",
        "5 tohum — tarama örneklemi; karar eşleştirilmiş R'ye ve kendi 2 SE "
        "bandına karşı (kasıtlı kuşkucu); sınırdaki kayıt `--tohum N` ile "
        "yeniden ölçülür"),
    "kalibrasyon/duyarlilik.py::CARPANLAR": ("TURETILMIS",
        "(0,5; 2,0) — ölçekten bağımsız TEK çarpan. Süre, sayı, mesafe, oran;"
        " hepsinde aynı anlama gelir. Mutlak bir ±X her parametre için ayrı "
        "gerekçe isterdi"),
    "kalibrasyon/evre_metrikleri_kapilari.py::TOHUMLAR": ("TURETILMIS",
        "3 tohum — kapı verdikti kol ortalamasında; kapı sınırda kalırsa ilk "
        "artırılacak sayı"),
    "kalibrasyon/evre_metrikleri_kapilari.py::G1P_TOHUMLAR": ("TURETILMIS",
        "2 tohum × 4 protokol = 8 koşu = havuzun 8 işçisi: referans dünyada "
        "tam pencere bir koşu ~16 dk, yani kapı TEK turda ~20 dk'da biter (30"
        " dk sınırının altında). Ölçüt koşu SAYISINA göre yazıldı (≤ 1/8; "
        "`arsiv/teshis/evre_g1p_2026-09-28/beklenti.md`), K-196"),
    "kalibrasyon/iki_cift.py::TOHUMLAR": ("TURETILMIS",
        "3 tohum — iki çift probu DETERMİNİSTİK bir soru soruyor ('iki uzak "
        "iletim aynı anda başarılı mı') ve ölçülen oranlar tohumdan bağımsız "
        "çıktı (1,000 · 1,000 · 1,000). Daha fazla tohum bilgi eklemiyor"),
    "kalibrasyon/li_replikasyonu.py::BAND": ("TURETILMIS",
        "(0,10; 0,20) — ÖN-KAYITLI kabul bandı, `09` §04'te ölçümden ÖNCE "
        "ilan edildi. Li'nin 1/7 = 0,143'ü etrafında ±%40; iki farklı 802.11 "
        "uygulaması arasında beklenen ayrımın mertebesi. Sonradan "
        "GENİŞLETİLMEYECEK"),
    "kalibrasyon/li_replikasyonu.py::IDEAL_MAC_TAVANI": ("KAYNAK",
        "0,25 — Li vd. §3.2, ideal MAC'te zincirin uçtan uca verimi tek "
        "atlamanın 1/4'ü. `02` A5b'de doğrulanmış"),
    "kalibrasyon/li_replikasyonu.py::TOHUMLAR": ("TURETILMIS",
        "5 tohum — zincir TEMİZ kanalda koşuyor (gölgeleme ve sönümleme "
        "kapalı), dolayısıyla tohumlar arası varyans yalnız trafik fazından "
        "geliyor ve küçük. Ölçüldü: 2 SE değerleri 0,19–4,68 pkt/s"),
    "kalibrasyon/yeniden_kullanim.py::BAG_M": ("TURETILMIS",
        "280 m = eski dünyanın `nominal_bag_m`i — Li replikasyonunun eski "
        "dünya açık sınavı (`09`); ⚠️ elle kopya"),
    "kalibrasyon/yeniden_kullanim.py::AYRIMLAR": ("TEDAVI",
        "çiftler arası mesafe TARAMASININ ekseni; yeniden kullanım mesafesi "
        "bu taramanın SONUCU"),
    "kalibrasyon/yeniden_kullanim.py::ALFALAR": ("TEDAVI",
        "(2,0; 3,0; 4,0) — yol kaybı üsteli taramasının ekseni. 🔒 α = 3 ve 4 "
        "bu projede KULLANILMIYOR; tarama bir öneri değil, girişim/iletim "
        "oranı türetmesinin SINAVI"),
    "kalibrasyon/yeniden_kullanim.py::ESIK": ("TURETILMIS",
        "1,5 — iki çift tam paralelse toplam verim 2,0, tamamen "
        "serileştirilmişse 1,0. Orta nokta; ölçülen değerler zaten 1,05 ya da"
        " 2,00 çıkıyor, yani eşik hiçbir kararı belirlemiyor"),
    "kalibrasyon/yeniden_kullanim.py::SACILMA_SINIRI": ("TURETILMIS",
        "1,35 — çarpanın α'dan bağımsız sayılması için izin verilen saçılma. "
        "Izgara 1 atlama çözünürlüklü olduğu için 3 atlamalık bir ölçümde tek"
        " adımlık belirsizlik zaten ±%33; sınır ondan dar seçilemez. Ölçülen "
        "saçılma 1,08"),
    "kalibrasyon/bag_kumesi.py::ESIKLER": ("TEDAVI",
        "(0,50…0,99) — bağ eşiği TARAMASININ ekseni. Bir değer değil, aranan "
        "aralık; `ATLAMA_ESIGI`nin platosu bu taramanın SONUCU. Alt sınır "
        "0,50: altında `ETX_TAVANI` kelepçesi geri türetmeyi bozar"),
    "kalibrasyon/bag_kumesi.py::K_ADAYLARI": ("TEDAVI",
        "(1…32) — sönümleme örnek sayısı taramasının ekseni; ikişer katlar, "
        "`duyarlilik.py::CARPANLAR` ile aynı 'ölçekten bağımsız tek çarpan' "
        "gerekçesi"),
    "kalibrasyon/bag_kumesi.py::KAYDIRMALAR": ("TURETILMIS",
        "(0…35 ms, 7 ms adımlı) — örnekleme fazı kaydırmaları. İki kısıt "
        "birlikte belirledi: tutarlılık süresinden (~1,7 ms) BÜYÜK olmalı ki "
        "çekimler bağımsız olsun (küçük olsaydı ölçülen saçılma kestiricinin "
        "gürültüsünü OLDUĞUNDAN KÜÇÜK gösterirdi), ve dünyayı oynatmayacak "
        "kadar küçük olmalı (35 ms'de düğüm 2,6 cm gider; gölgeleme hücresi "
        "50 m). G-b kapısı ikinci kısıtı her koşumda sınıyor"),
    "kalibrasyon/bag_kumesi.py::DERECE_TOLERANSI": ("TURETILMIS",
        "0,3 — görev kolunu bağımsız kolla eşitleyen ölçütün toleransı (eski "
        "dünya, `calisma_noktasi.py` §4 ile aynı); bu bölümden karar çıkmaz"),
    "kalibrasyon/bag_kumesi.py::COZUNURLUK_R": ("OLCULMUS",
        "ESKİ DÜNYA — 0,036 (30 tohum, `kalibrasyon/cozunurluk.py`); elle kopya, kaynak "
        "`cozunurluk.py`"),
    "kalibrasyon/bag_kumesi.py::GUCLER": ("TEDAVI",
        "(−30…−6 dBm) — `karistirici_gucu.tarama`nın varsayılan ekseniyle "
        "AYNI. Aynı olması ZORUNLU: eşik taraması, güç seçimini yeniden "
        "koşturuyor ve iki tarama farklı ızgarada olsaydı sonuçlar "
        "karşılaştırılamazdı"),
    "kalibrasyon/onay_semantigi.py::COZUNURLUK_R": ("OLCULMUS",
        "ESKİ DÜNYA — 0,0318 (40 tohum, `kalibrasyon/cozunurluk.py --tohum 40`); elle "
        "kopya"),
    "kalibrasyon/regresyon_satirlari.py::REFERANS_VAKALARI": ("TEDAVI",
        "regresyon matrisinin referans dünya vakaları (30 Eylül 2026, K-203) "
        "— bir değer değil, deneylerin dünyasında sınanan yolların listesi: "
        "birincil hücre × dört protokol + ETX kâhini, dört karıştırıcı "
        "sınıfı, yer karıştırıcısı ailesi, düğüm kaybı, eşler arası"),
}


# ===========================================================================
# DENETİM
# ===========================================================================
def eksik_alanlar(alan_adlari) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """`(kökeni yazılmamış alanlar, artık var olmayan köken kayıtları)`."""
    adlar = set(alan_adlari)
    kayitli = set(KOKENLER)
    return (tuple(sorted(adlar - kayitli)), tuple(sorted(kayitli - adlar)))


def duyarlilik_borcu() -> tuple[str, ...]:
    """Faz 1 duyarlılık denetiminin HÂLÂ oynatmadığı kol tanımı sabitleri.

    🔒 Bu, `SINANMAMIS`in kardeş sayacıdır. `KOL_TANIMI` kovası hiç boşalmaz
    (bir kolun tanımı silinmez), ama borç bu kümede durur ve BOŞALIR.
    Ön-kayıt mührü ikisinin de sıfır olmasını ister.
    """
    return tuple(sorted(DUYARLILIK_BEKLEYEN))


def kova_sayimi() -> dict[str, int]:
    """Kova başına parametre sayısı — sonuç satırına yazılır."""
    sayim = {k: 0 for k in KOVALAR}
    for kova, _ in KOKENLER.values():
        sayim[kova] += 1
    for kova, _ in MODUL_KOKENLERI.values():
        sayim[kova] += 1
    return sayim
