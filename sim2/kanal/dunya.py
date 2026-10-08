"""
Dünyalar — `v2/15` A7 · K-178.

`olcek_1_50` : bugünkü dünya (`Konfig` varsayılanları, K-101/K-102). Verici
               gücü menzilden TÜRETİLİR: menzil sınırında SNR = β.
`referans_2026`: `v2/14`ün (onaylı, K-169) 1:1 taktik sürüsü. Verici gücü
               GİRDİDİR (EIRP 20 dBm); menzil ve eşikler PER modelinden türer:

    menzil_snr_db    = SNR(PER %10, 2 Mb/s veri) + 10 dB pay   (`bag_butcesi.py`)
    nominal_bag_m = ortalama SNR'ın menzil_snr_db olduğu mesafe (nominal
                       bağ; yerleşim kuralları ve kayıp yeri bantları bunu kullanır)
    sinr_esigi_db β  = SNR(PER %50) + 2σ gölgeleme payı — eski β'nın (16 dB =
                       10 dB çözülebilirlik + 2σ) AYNI tanımı, işlem kazançlı
                       modelde (fiziksel kopma sayımı ve kâhin bağ kümesi)

🔒 Türetim bu dosyada, çünkü PER kanal katmanındadır (`kanal.cerceve_per`);
`yapilandirma/` kanalı içe aktarmaz. `Yayilim` tutarlılığı ayrıca denetler.

🔒 A8 (K-181) — FAZ 1'İN BÜTÜN ANAHTARLARI AÇIK: işlem kazancı (A2), güce
dayalı taşıyıcı dinleme + ED-CCA (A3), ARF hız uyarlaması (A4), yayılım
gecikmesi (A5), karıştırıcı gerçekçiliği (A6). `Konfig` varsayılanları eski
dünyada kalır; eski regresyon vakaları ve kalibrasyon tabloları onunla
birebir. Faz 4'ten sonra deneyler bu dünyada koşar.

⚠️ GEÇİCİ DEĞERLER (Faz 4'te kalibre edilir, K-178'de beyanlı):
  · hız yayılımı eski dünyanın bağıl yayılımıyla (σ / ortalama hız);
  · (karıştırıcı taban gücü K-186'da kesinleşti — aşağıda.)
"""

from __future__ import annotations

from dataclasses import fields

from sim2.cekirdek.degismezler import dogrula
from sim2.kanal.cerceve import cerceve_kur, kontrol_kapsulleme_bayt
from sim2.kanal.kanal import cerceve_per
from sim2.kanal.yayilim import Yayilim, lin_to_db
from sim2.yapilandirma.konfig import Konfig

__all__ = ["REFERANS_EIRP_DBM", "REFERANS_PAY_DB", "REFERANS_ALAN_M",
           "REFERANS_GOREV_YARICAPI_M", "REFERANS_TTL", "REFERANS_BEACON_BAYT",
           "referans_2026", "snr_esigi_db"]

REFERANS_EIRP_DBM = 20.0   # `v2/14` §1 — AB/TR 2,4 GHz EIRP sınırı (G2 · G7)
REFERANS_PAY_DB = 10.0     # nominal bağ: duyarlılığın 10 dB üstü (`bag_butcesi.py`)
# 🔒 K-185 (Faz 4.1a): 35 km. Bağ 1 Mb/s'te ~9–10 km (serbest uzay, 50–300 m
# irtifa); 7 km'de derece 37,4 ve çiftlerin %96'sı tek atlamaydı. 35 km,
# ağın 30 tohumda hiç kopmadığı en büyük alan (36–40 km kopar): derece 8,82,
# derin çift %31,9. Öğrenci gerçekçiliği öne koydu; menzili kaynaksız bir
# kayıpla kısaltmak yerine geometri fiziğe uyduruldu (G9 zarfı: ≤ 50 km).
# 🔒 K-188: gölgeleme birimi düzeltilince (2,5 km) 35 ve 37 km kopar
# (%0,5 · %0,3), 33 km ve altı geçer; 40 km'nin geçmesi örnekleme şansı
# (tekdüze bir özelliğin tekdüze olmayan sonucu). Sağlam sınır: 33 km.
REFERANS_ALAN_M = 33000.0
# 🔒 K-188: görev kolu müfreze yarıçapı — derece eşitliği ölçütü (bağımsız
# kolla |Δ derece| en küçük): 16 km'de 8,10 ↔ 8,16. Alan oranıyla türetme
# (650/1800 × alan) kaldırıldı; ölçülen değer.
REFERANS_GOREV_YARICAPI_M = 16000.0
# 🔒 K-186 (öğrenci kararı): 40 dBm = 10 W TOPLAM ORTALAMA güç, her ailede
# eşit (K-119). Birincil hücre `derin_sizma` (hareketli araç): ρ 0,16, büyük
# bölünme 2/30. 1–5 W'lık HAVA karıştırıcısı sürüyü her geometride böler
# (`arsiv/teshis/faz4_2026-09-26/b_aile_guc.txt`); `hava_eslik` keşifsel.
REFERANS_KARISTIRICI_DBM = 40.0
# 🔒 K-215 (öğrenci, kaynağa bağlama): VERİ paketinin TTL'i = IP'nin önerilen
# varsayılanı. RFC 1700 "IP TIME TO LIVE PARAMETER": 64; ns-3
# `Ipv4L3Protocol::DefaultTtl` 64 (`02` G17). Eski dünyanın 32'si kaynaksızdı
# ve OLSR'da DUYARLI ölçüldü (döngüdeki paket kanalı doldurur, K-214).
REFERANS_TTL = 64
# 🔒 K-215: kâhinin beacon'ı AODV'nin HELLO'suyla BİREBİR — HELLO bir RREP'tir
# (RFC 3561 §6.9) ve RREP 20 B'tır (§5.2); kontrol çerçevesi gibi kapsüllenir
# (`KONTROL_KAPSULLEME`, `02` G15 · G16). Beacon boyu TOPLAM çerçevedir.
# 20, `protokoller/aodv_bicim.py::RREP`e bir testle bağlı (sim2 protokolü içe
# aktaramaz). Aralık zaten 1 s = `HELLO_INTERVAL` (§10).
REFERANS_BEACON_BAYT = 20 + kontrol_kapsulleme_bayt()

# Türetilen alanlar — `ek` ile verilemez.
_TURETILEN = ("sinr_esigi_db", "menzil_snr_db", "nominal_bag_m")


def snr_esigi_db(per_fn, hedef: float) -> float:
    """PER = hedef olan SNR (dB) — ikiye bölme (PER SNR'da azalan)."""
    alt, ust = -30.0, 40.0
    for _ in range(90):
        orta = 0.5 * (alt + ust)
        if per_fn(10.0 ** (orta / 10.0)) > hedef:
            alt = orta
        else:
            ust = orta
    return 0.5 * (alt + ust)


def referans_2026(**ek) -> Konfig:
    """`v2/14`ün 1:1 dünyası. `ek` öteki alanları (kol, senaryo, tohum,
    anahtarlar…) verir; türetilen üç alan verilemez."""
    dogrula(not set(ek) & set(_TURETILEN),
            f"türetilen alanlar verilemez: {sorted(set(ek) & set(_TURETILEN))}")
    v = {f.name: f.default for f in fields(Konfig)}
    hiz_min, hiz_maks = 40.0 / 3.6, 120.0 / 3.6            # `v2/14` §3
    sigma_orani = v["gm_hiz_sigma_ms"] / (0.5 * (v["gm_hiz_min_ms"]
                                                 + v["gm_hiz_maks_ms"]))
    temel = dict(
        dunya="referans_2026", olcek=1.0, dugum_sayisi=40,
        alan_en_m=REFERANS_ALAN_M, alan_boy_m=REFERANS_ALAN_M,
        irtifa_min_m=50.0, irtifa_maks_m=300.0,
        gm_hiz_min_ms=hiz_min, gm_hiz_maks_ms=hiz_maks,
        gm_hiz_sigma_ms=sigma_orani * 0.5 * (hiz_min + hiz_maks),
        gorev_grup_yaricapi_m=REFERANS_GOREV_YARICAPI_M,
        gorev_jitter_hiz_ms=v["gorev_jitter_hiz_ms"] * v["olcek"],
        # 🔴 K-188 — A7 ATLAMASI (ajan): eski dünyanın gölgeleme hücresi
        # 1:50 ölçekli uzaydaydı (50 m → gerçekte 2,5 km). Ölçeklenmeden
        # taşınınca 1:1 dünyada gölgeleme 50 kat hızlı değişti ve rota ömrü
        # yapay olarak çöktü (Θ_OLSR 0,29). Değer kaynaksız: DÜNYA TANIMI,
        # ölçülen duyarlılığıyla (K-217, K-220).
        golgeleme_hucre_m=v["golgeleme_hucre_m"] * v["olcek"],
        frekans_hz=2.437e9, bant_genisligi_hz=22e6, gurultu_figuru_db=7.0,
        islem_kazanci=True, rician_k_db=10.0, yeniden_deneme_siniri=7,
        tasiyici_dinleme="guc", hiz_uyarlamasi=True,          # A8 · K-181
        yayilim_gecikmesi=True, karistirici_gercekci=True,
        sonumleme_uretec="blok",                                # K-198
        cca_s=15e-6, verici_eirp_dbm=REFERANS_EIRP_DBM,
        alici_anten_kazanci_dbi=2.15,           # yarım dalga dipol (`v2/14` §1)
        karistirici_taban_dbm=REFERANS_KARISTIRICI_DBM,
        ttl_baslangic=REFERANS_TTL, beacon_bayt=REFERANS_BEACON_BAYT,  # K-215
    )
    temel.update(ek)
    # Geçici konfig: eski türetim yoluyla — yalnız gürültü, yol kaybı ve PER.
    gecici = Konfig(**{**temel, "dunya": "olcek_1_50",
                       "verici_eirp_dbm": None, "menzil_snr_db": None})
    yayilim = Yayilim(gecici)
    cerceve = cerceve_kur(gecici, "veri")
    snr10 = snr_esigi_db(lambda s: cerceve_per(cerceve, s), 0.10)
    snr50 = snr_esigi_db(lambda s: cerceve_per(cerceve, s), 0.50)
    beta = snr50 + 2.0 * gecici.golgeleme_sigma_db
    menzil_snr = snr10 + REFERANS_PAY_DB
    kayip_hedef = (temel["verici_eirp_dbm"]
                   + temel["alici_anten_kazanci_dbi"]
                   - (lin_to_db(yayilim.gurultu_w * 1e3) + menzil_snr))
    alt, ust = 1.0, 1e6
    for _ in range(200):
        orta = 0.5 * (alt + ust)
        if yayilim.yol_kaybi_db(orta) < kayip_hedef:
            alt = orta
        else:
            ust = orta
    return Konfig(**{**temel, "sinr_esigi_db": beta,
                     "menzil_snr_db": menzil_snr,
                     "nominal_bag_m": 0.5 * (alt + ust)})
