"""
Konfigürasyon — bir koşuyu TAM olarak belirleyen her şey.

🔒 Bu nesnede olmayan hiçbir şey koşunun davranışını etkilemez; her deney
kolu bir alan değişikliğidir (kod düzenlemesiyle üretilen bir kol
kaynağından ayırt edilemez). Nesne dondurulmuştur.

🔒 İKİ DÜNYA: alanların varsayılanı ESKİ 1:50 dünyadır ve yalnız
regresyonun eski vakaları için yaşar. Deneyler REFERANS dünyada koşar;
onu `kanal/dunya.py::referans_2026` kurar (`v2/14`). Her alanın gerekçesi
— referans dünyadaki değeriyle — `kokenler.py`dedir; buradaki yorumlar
alanın ne olduğunu söyler.

Burada kasıtlı olarak olmayan iki şey: çerçeve süresi (tek tanımı
`kanal/cerceve.py`de; iki ayrı PER tanımı ayrışıyordu) · kutu nesnesi
(katman yönü `yapilandirma → dunya`).
"""

from __future__ import annotations

import dataclasses as _dc
import math
from dataclasses import asdict, dataclass
from typing import Any, ClassVar

from sim2.cekirdek.degismezler import DegismezHatasi as _DegismezHatasi
from sim2.cekirdek.degismezler import dogrula
from sim2.yapilandirma import kokenler as _kokenler
from sim2.yapilandirma.senaryolar import (
    KARISTIRICI_GUCU_DBM, SENARYOLAR, TEHDIT_SENARYOLARI, TRAFIK_DESENLERI,
    UYGULANMAMIS_KARISTIRICI)

__all__ = ["Konfig", "HENUZ_OKUNMAYAN"]


# 🔒 802.11b DSSS kanalının gürültü bandı — işlem kazancının paydası
# (`v2/15` A2; G1 · G2: 11 Mchip/s Barker, 22 MHz kanal).
DSSS_KANAL_BANDI_HZ: float = 22e6
# 🔒 802.11b hızları — `v2/15` A4 (G1 · G2): DBPSK · DQPSK · CCK · CCK.
HIZLAR_BPS: tuple[float, ...] = (1e6, 2e6, 5.5e6, 11e6)
# 🔒 Taşıyıcı dinleme kipleri — `v2/15` A3 (K-174). Kapalı küme.
TASIYICI_DINLEME_KIPLERI: tuple[str, ...] = ("geometrik", "guc")
# 🔒 Dünyalar — `v2/15` A7 (K-178). Kapalı küme.
DUNYALAR: tuple[str, ...] = ("olcek_1_50", "referans_2026")
# 🔒 Yer–hava ortamları — `kanal/yer_hava.py::A2G_ORTAMLARI` ile AYNI KÜME
# (bir test bağlar); yapılandırma kanal katmanını içe aktarmaz.
A2G_ORTAM_ADLARI: tuple[str, ...] = ("banliyo", "kentsel", "yogun", "yuksek")

# 🔒 `rng.HENUZ_KULLANILMAYAN`ın Konfig'deki karşılığı: bir alan ya bir
# `sim2/` modülünce OKUNUR ya burada yazılıdır — okunmayan bir alan sonuç
# satırını yalancı yapar. Aşağıdakiler yalnız `Konfig`in kendi türetilmiş
# özelliklerince okunuyor (bu, davranışı etkilediklerini kanıtlamaz).
# Liste modüller indikçe kısalır; testi iki yönlü çalışır.
HENUZ_OKUNMAYAN: frozenset[str] = frozenset({
    "isinma_s",
    "komsu_omru_katsayisi",
    "karistirici_taban_dbm",
    "karistirici_guc_override_dbm", "karistirici_konum",
})


@dataclass(frozen=True)
class Konfig:
    # ==================================================================
    # KİMLİK
    # ==================================================================
    kol: str                          # hangi protokol kolu
    senaryo: str = "statik-yok"       # `senaryolar.SENARYOLAR` anahtarı
    tohum: int = 1000

    # ==================================================================
    # ZAMAN (saniye)
    # ==================================================================
    # ısınma 50 · ölçüm penceresi 270 · boşalma 30 s (pencere taraması
    # `06` §8 koşul 1, Faz 6)
    isinma_s: float = 50.0
    olcum_bitis_s: float = 320.0      # trafik üretimi burada durur
    kosu_bitis_s: float = 350.0       # boru bu aralıkta boşalır

    # ==================================================================
    # DÜNYA
    # ==================================================================
    # Referansta 40 İHA · 33 km kare alan (`kanal/dunya.py`, K-188);
    # eski dünyada 1 800 m.
    dugum_sayisi: int = 40
    alan_en_m: float = 1800.0
    alan_boy_m: float = 1800.0

    # Ölçek: referansta 1 (1:1). Eski dünya 1:50 geometrik ölçek modeliydi;
    # `olcek` fiziği değiştirmez, yalnız gerçek dünya eşlemesini verir.
    # Ölçeklenmeyen iki şey: dalga boyu (Doppler gerçek hızdan) ve
    # yerçekimi (dönüş hızı gerçek hızdan).
    olcek: float = 50.0

    # İrtifa bandı (referansta 50–300 m AGL) hem başlangıç yerleşiminin hem
    # kutunun dikey sınırıdır; ayrı bir yükseklik alanı ikinci bir doğru
    # kaynağı olurdu.
    irtifa_min_m: float = 20.0
    irtifa_maks_m: float = 120.0

    # Referansta verici gücü GİRDİDİR (`verici_eirp_dbm`) ve
    # `nominal_bag_m` o güçle ortalama SNR'ın `menzil_snr_db` olduğu
    # mesafedir (türetilmiş nominal bağ; bir menzil değil, güç çapası —
    # K-220'ye kadar adı `iletim_menzili_m`ydi). Eski dünyada ikisi `None`:
    # güç bu mesafeden türer ve orada SNR = β.
    nominal_bag_m: float = 280.0
    # Dünya anahtarı (`v2/15` A7, K-178): 'olcek_1_50' | 'referans_2026'.
    dunya: str = "olcek_1_50"
    verici_eirp_dbm: float | None = None
    menzil_snr_db: float | None = None
    # Alıcı anteninin en büyük kazancı (dBi); desen kaybı buna göre
    # normalize. EIRP vericininkini içerir. Eski dünyada 0 (sadeleşir).
    alici_anten_kazanci_dbi: float = 0.0

    # ------------------------------------------------------- 3B Gauss-Markov
    # FANET'te standart model (Random Waypoint sonsuz ivme üretir). Hız zarfı
    # referansta 40–120 km/h (`v2/14` §3); eski dünyada ölçekli 0,25–0,75
    # m/s. Θ = rota ömrü / 15 s ≥ 3 bir kapıdır (K-101; kol başına Θ
    # `senaryolar.MOBILITE_THETA_REFERANS`). `gm_alfa` ve
    # `gm_azimut_sigma_rad` araç dinamiğidir, ölçeklenmez: hız korelasyonu
    # ~30 s → α = exp(−0,5/30) = 0,983 · koordineli dönüş ω = g·tan(φ)/v,
    # 90 km/h'de 30° banka → 0,5 s adımda 0,11 rad.
    gm_alfa: float = 0.983
    gm_adim_s: float = 0.5
    gm_hiz_min_ms: float = 0.25
    gm_hiz_maks_ms: float = 0.75
    gm_hiz_sigma_ms: float = 0.075
    gm_azimut_sigma_rad: float = 0.11
    # Ortalama pitch 0: sıfırdan farklı ortalama kalıcı tırmanış demektir
    # (350 s'de 0,05 rad → +299 m); σ 0,05 ile tipik |pitch| ≈ 2,3°.
    gm_pitch_ort_rad: float = 0.0
    gm_pitch_sigma_rad: float = 0.05

    # ------------------------------------------- görev tabanlı kol (RPGM)
    # Müfreze sayısı ve yarıçap, ortalama dereceyi bağımsız kolla
    # eşitleyecek biçimde seçilir (bağıl hız ve rota ömrü sonuçtur, ölçüt
    # değil). Referansta yarıçap 16 km (`kanal/dunya.py`, K-188). Üyeler
    # görev merkeziyle birlikte hareket eder (`dunya/mobilite.py`).
    gorev_grup_sayisi: int = 10
    gorev_grup_yaricapi_m: float = 650.0
    gorev_jitter_hiz_ms: float = 0.05

    # ----------------------------------------------- formasyon kolu (Y6)
    # Birincil hücrenin kolu (öğrenci onayı). İstasyonlar yerleşim
    # çekimleridir; tutma zaman sabiti `mobilite.ISTASYON_TUTMA_S`, manevra
    # gürültüsü GM alanlarından. `istasyon_kayma_hiz_ms` > 0 keşifsel eksendir
    # (istasyonların yavaş yeniden düzenlenmesi); çekirdekte 0.
    istasyon_kayma_hiz_ms: float = 0.0

    # Sınır kuralının ayarlanacak parametresi yok (kasıtlı): yansımada
    # ortalama yön de aynalanır; bir sınır marjı ortalama dereceyi
    # seçilebilir yapardı (`dunya/mobilite.py`).

    # ==================================================================
    # FİZİKSEL KATMAN
    # ==================================================================
    # 802.11b DSSS: veri 2 Mb/s DQPSK (ARF açıkken başlangıç hızı), önbelge +
    # başlık 192 µs her zaman 1 Mb/s DBPSK. Önbelgenin bit sayısı bu ikisinden
    # `kanal/cerceve.py`de türer; önbelge gövdeden dayanıklıdır, bu yüzden
    # `alim_red_onbelge` ile `alim_red_per` ayrı iki başarısızlık kipidir.
    # Bant ve frekans referansta 22 MHz · 2 437 MHz (kanal 6).
    bit_hizi_bps: float = 2e6
    onbelge_s: float = 192e-6
    temel_bit_hizi_bps: float = 1e6
    bant_genisligi_hz: float = 2e6
    frekans_hz: float = 2.4e9
    # α = 2: hava–hava serbest uzay (ölçümler 1,92–2,6, `02` G10); iki-ışın
    # kırılma mesafesi bağ mesafelerinin çok üstünde.
    yol_kaybi_usteli: float = 2.0     # α — hava-hava, serbest uzay rejimi

    # β: referansta `kanal/dunya.py` türetir — SNR(PER %50, 2 Mb/s, işlem
    # kazancıyla) + 2σ gölgeleme payı ≈ 6 dB; eski dünyada 16 dB.
    # `nominal_bag_m` veri yolunda hiçbir şeyi kapamaz: kimin duyacağını
    # alınan güç, alınıp alınmadığını SINR belirler (K-096).
    sinr_esigi_db: float = 16.0       # β — menzil sınırının tanımlandığı SINR
    gurultu_figuru_db: float = 6.0
    sicaklik_k: float = 290.0

    # 2 Mb/s DQPSK; önbelge ve yayın 1 Mb/s DBPSK.
    modulasyon: str = "dqpsk"
    # 🔒 DSSS İŞLEM KAZANCI — `v2/15` A2 (K-173). Açıkken BER'in girdisi
    # Eb/N0 = SINR · (B / bit hızı): gürültü ve girişim işaretin kapladığı
    # 22 MHz'de ölçülür, alıcı 11 çiplik Barker dizisini toplayarak her biti
    # o banttan toplar (G1 Pei & Henderson · G2 Boer; ns-3
    # `DsssErrorRateModel`: 1 Mb/s ×22, 2 Mb/s ×11). Kapalıyken bugünkü
    # model: SINR doğrudan Eb/N0 sayılır (2 MHz'lik "birim" bandında ısıl
    # gürültüye karşı eşdeğer, girişime karşı ~10,4 dB fazla zarar — `02` G1).
    # Açmak `bant_genisligi_hz` = 22 MHz ister: çarpan ancak GERÇEK kanal
    # bandında fiziksel anlam taşır (aşağıda doğrulanır).
    islem_kazanci: bool = False
    # 🔒 HIZ UYARLAMASI — `v2/15` A4 (K-177). Açıkken tek yönlü (unicast) veri
    # ve kontrol çerçeveleri komşu başına ARF hızıyla gider (G14 — ns-3
    # `ArfWifiManager`: 10 art arda başarı ya da 15 iletim → bir hız yukarı;
    # kurtarmada ilk, normalde art arda 2 başarısızlık → bir hız aşağı);
    # yayınlar ve onaylar temel hızda (1 Mb/s). Hızlar `HIZLAR_BPS`; CCK'nın
    # hata modeli G1/G12. İşlem kazancı ister (Eb/N0 eşlemesi gerçek bantta).
    hiz_uyarlamasi: bool = False
    arf_basari_esigi: int = 10
    arf_zamanlayici_esigi: int = 15

    # Kanal rastgeleliği sıralı akıştan DEĞİL, hash'ten gelir.
    kanal_dilimi_s: float = 1e-4

    # ---------------------------------------------------------- gölgeleme
    # Log-normal, bağ-simetrik ve konuma bağlı (hücrelenmiş hash + trilineer
    # yumuşatma: hareket eden düğüm gölgeleme alanında sürekli ilerler).
    # Gölgelemesiz bağlar gerçeğe göre keskin açılıp kapanırdı (PER geçiş
    # bandı ~3 dB, σ mertebesinde). Referansta σ 3 dB, hücre 2,5 km.
    golgeleme_acik: bool = True
    golgeleme_sigma_db: float = 3.0
    golgeleme_hucre_m: float = 50.0

    # ---------------------------------------------------------- sönümleme
    # Hava–hava bağda güçlü doğrudan görüş → Rician (referansta K 10 dB).
    # Parça başına çekilir: 190 µs ≤ T_c/4 (en büyük bağıl hız 66,7 m/s'de
    # T_c ≈ 0,78 ms); Doppler gerçek hızdan. Üreteç (K-198): `tekil` her
    # yenilik bir blake2b özeti (eski dünya, birebir) · `blok` bağ başına
    # özet + SplitMix64 (referans dünya) — aynı dağılım, farklı sayılar.
    sonumleme_acik: bool = True
    rician_k_db: float = 6.0
    sonumleme_parca_suresi_s: float = 190e-6
    sonumleme_uretec: str = "tekil"

    # ------------------------------------------------------- anten deseni
    # Dipol deseni: izotropik bırakmak yakın komşularda modeli iyimser
    # yapardı.
    anten_deseni_acik: bool = True

    # ==================================================================
    # ALICI ZİNCİRİ (Adım 6a)
    # ==================================================================
    yakalama_etkisi_acik: bool = True
    yakalama_esigi_db: float = 10.0
    # 🔒 YAKALAMA PENCERESİ = önbelge süresi (192 µs). Gerçek bir alıcı hâlâ
    # senkronizasyon aşamasındayken daha güçlü bir çerçeveye geçebilir; gövde
    # çözümüne başladıktan sonra kilidi kolay bırakmaz. Pencere koşulu
    # olmasaydı alıcı neredeyse bitmiş bir gövdeyi bırakıp yeni bir önbelgeye
    # geçer ve gerçekte imkânsız bir davranış üretirdi.
    # Sayı beyan edilir, `onbelge_s`ten türetilmez: önbelge aritmetiği
    # `cerceve.py` dışına çıkmasın.
    yakalama_penceresi_s: float = 192e-6
    # 🔒 RSSI ÖLÇÜM HATASI — `v2/15` B2 (K-170 onayı). Telsizin çerçeve başına
    # raporladığı alınan güç = alıcının kilitlendiği güç + N(0, σ²), tamsayı
    # dBm. Yalnız `cerceve_duyuldu` kancasını taşıyan protokole gider; alım
    # kararına GİRMEZ.
    rssi_olcum_sigma_db: float = 2.0
    # 🔒 KENDİ GPS/INS'İ — `v2/15` B3 (K-179), öğrenci kararı 25 Eylül:
    # her düğüm kendi konumunu küçük bir hatayla bilir (GPS karıştırması
    # kapsam dışı). Hata hash'ten, `gps_tazeleme_s` dilimi boyunca sabit.
    gps_yatay_cep_m: float = 1.5
    gps_dikey_sigma_m: float = 2.0
    gps_hiz_sigma_ms: float = 0.1
    gps_tazeleme_s: float = 1.0

    # ==================================================================
    # MAC — CSMA/CA, 802.11b değerleri
    # ==================================================================
    slot_s: float = 20e-6
    sifs_s: float = 10e-6
    # CCA gecikmesi SIFIR OLAMAZ: sıfır olsaydı geri sayımı aynı slotta biten
    # iki düğüm asla çarpışmazdı ve 802.11'in temel çakışma kaynağı silinirdi.
    cca_s: float = 4e-6
    # 🔒 TAŞIYICI DİNLEME KİPİ — `v2/15` A3 (K-174).
    # "geometrik" (eski dünya): girişim menzilindeki her iletim ve CSMA'ya görünen
    # karıştırıcı kanalı meşgul eder. "guc": 802.11b CCA (G2 — CCA mod 3):
    # (1) önbelge sezme = alıcı bir çerçeveye KİLİTLİ (kilit önbelge
    # PER'iyle kurulur, eşik oradan türer) · (2) enerji sezme = düğümdeki
    # toplam alınan güç (bütün iletimler + HER sınıf karıştırıcı)
    # `ed_esigi_dbm`i aşıyor. Sezme `cca_s` sürer.
    tasiyici_dinleme: str = "geometrik"
    ed_esigi_dbm: float = -76.0
    # Hareketli karıştırıcı yüzünden donmuş düğümün yeniden denetimi —
    # yalnız "guc" kipinde ve yalnız hareketli karıştırıcıda.
    karistirici_denetim_araligi_s: float = 0.010
    # 🔒 YAYILIM GECİKMESİ — `v2/15` A5 (K-175). Açıkken çerçeve alıcıya d/c
    # sonra ulaşır (alım, donma, taşıyıcı dinleme varış penceresiyle); onay
    # bekleme en uzak duyma mesafesinin gidiş-dönüşünü kapsar (802.11
    # kapsama sınıfının karşılığı). Girişim hesabı gönderim anlarıyla kalır
    # (beyanlı hata: ≤ d/c, 8 km'de 27 µs / 2,5 ms'lik çerçeve).
    yayilim_gecikmesi: bool = False
    # 🔒 KARIŞTIRICI GERÇEKÇİLİĞİ — `v2/15` A6 (K-176). Açıkken:
    # (1) karıştırıcı bağlarında hızlı sönümleme (düğüm bağlarıyla aynı
    #     Rician model, bağıl hız karıştırıcının yörüngesinden);
    # (2) yer platformları (`sabit_yer`, `arac`) `yer_karistirici_yukseklik_m`
    #     yükseklikte ve bağları Al-Hourani yer–hava kanalıyla (G6; görüş
    #     hattı olasılığı yükseklik açısından, durum geometriden ve kalıcı —
    #     DD-01, K-242);
    # (3) reaktif karıştırıcı iletimi ancak aldığı güç `reaktif_esik_dbm`i
    #     aşarsa sezer (sezme olasılığı her kipte `reaktif_sezme_olasiligi`);
    # (4) aldatıcının sahte çerçevesi, başını yakalayan boştaki alıcıyı
    #     önbelge PER'iyle KİLİTLER; çerçeve boyunca gerçek çerçeve alınamaz.
    karistirici_gercekci: bool = False
    yer_karistirici_yukseklik_m: float = 3.0
    a2g_ortam: str = "banliyo"
    reaktif_esik_dbm: float = -90.0
    reaktif_sezme_olasiligi: float = 0.95
    cw_min: int = 31
    cw_max: int = 1023
    yeniden_deneme_siniri: int = 4
    onay_bayt: int = 14

    # ==================================================================
    # SAAT (Adım 7)
    # ==================================================================
    # 🔒 Yasak değil, FİZİK: protokol beacon'a zaman damgası koyabilir ama
    # alıcı ofseti görür. Bedava kusursuz senkron imkânsız hâle gelir.
    saat_senkron: bool = False        # ablasyon: True → tek küresel saat
    saat_ofset_araligi_s: float = 0.5  # ofset ~ U(−bu, +bu)
    saat_sapma_ppm: float = 20.0       # sapma ~ N(0, bu)

    # ==================================================================
    # TRAFİK
    # ==================================================================
    # Telemetri 512 B (`v2/14` §5). Eşler arası (keşifsel): 10 akış × 4 pkt/s
    # = 40 pkt/s, yere toplamanın sunumuna eşit (K-126).
    paket_bayt: int = 512
    akis_sayisi: int = 10
    akis_paket_hizi_hz: float = 4.0
    cbr_titresim_s: float = 0.05      # periyodik süreçlerin kilitlenmesini kırar

    # Trafik deseni (`v2/07` §6): `yere_toplama` birincil — geçit (düğüm 0,
    # sabit röle) ← her düğümden telemetri, geçitten birkaç düğüme komut;
    # 39 × 1,0 + 4 × 0,25 = 40 pkt/s. `esler_arasi` keşifsel ve varsayılan
    # (ana deney aleti deseni açıkça verir). İki geçit uygulanmadı.
    trafik_deseni: str = "esler_arasi"
    gecit_konumu: str = "kenar"        # kenar · merkez
    telemetri_paket_hizi_hz: float = 1.0
    komut_akis_sayisi: int = 4
    komut_paket_hizi_hz: float = 0.25
    # 🔒 DÜĞÜM KAYBI — `v2/15` C1 (K-180), TEDAVİ ekseni. Pencere içinde bu
    # kadar İHA düşer (vurulma, arıza); hangileri ve anları hash'ten, geçit
    # düşmez. Telsiz kapanır; protokole haber verilmez (`kosum/kayip.py`).
    kayip_dugum_sayisi: int = 0
    kayip_bas_s: float = 0.0
    kayip_bitis_s: float = 0.0
    # 🔒 ENERJİ — `v2/15` C3 (K-180). Telsiz gücü (G7, taktik mesh telsizi):
    # gönderimde / alımda ve dinlemede. Raporlanır, tasarım ölçütü değildir
    # (İHA'da itki enerjisinin yanında küçük).
    enerji_gonderim_w: float = 10.6
    enerji_alim_w: float = 2.0

    # ==================================================================
    # KUYRUK ve TTL
    # ==================================================================
    # Sonsuz kuyruk yasak: gecikme metriğini anlamsızlaştırır.
    kuyruk_kapasitesi: int = 50
    # ==================================================================
    # ROTA BEKLEME TAMPONU — `Karar.beklet` (K-131)
    # ==================================================================
    # Hem paket sayısıyla hem süreyle sınırlı; aşım `tampon_asimi` ile düşer.
    # Tavansız tampon sonsuz kuyruk olurdu. Değerler ns-3 AODV'sinin
    # (`MaxQueueLen` 64 · `MaxQueueTime` 30 s, K-198).
    rota_tamponu_kapasitesi: int = 64
    rota_tamponu_omru_s: float = 30.0
    # TTL olmadan döngüye giren paket "uçuşta" olarak sonsuza dek asılı kalır.
    ttl_baslangic: int = 32

    # ==================================================================
    # KONTROL DÜZLEMİ
    # ==================================================================
    beacon_araligi_s: float = 1.0
    beacon_bayt: int = 32
    # ⚠️ Bir PROTOKOL parametresi DEĞİL, bellek sınırlamasıdır. Tazelik kararı
    # protokole aittir. Geniş tutuluyor ki protokolün kararını kısıtlamasın.
    komsu_omru_katsayisi: float = 10.0

    # ==================================================================
    # KARIŞTIRICI — sınıf SENARYODAN gelir, parametreler burada
    # ==================================================================
    # Sınıf elle ayarlanabilseydi aynı etiketli iki koşu farklı karıştırıcı
    # taşıyabilir ve sonuç satırındaki etiket yalan söylerdi.
    karistirici_guc_override_dbm: float | None = None  # yalnız güç taraması
    # Referans dünyanın karıştırıcı TABAN gücü (K-186); darbeli sınıfta tepe
    # telafisi eklenir. Eski dünyada `None` (ρ kalibrasyonu,
    # `KARISTIRICI_GUCU_DBM`).
    karistirici_taban_dbm: float | None = None
    karistirici_konum: tuple[float, float] | None = None  # None → alan merkezi

    # Açılma anı pencereden türer: temiz evre [50, 150) · karıştırılmış
    # [150, 320). Geçici tepki (şok ve toparlanma) bu sayede ölçülür;
    # birincil hücrede açılmadan sonra 15 s açık · 15 s sessiz çizelge.
    # Karıştırıcısız kolda okunmaz.
    karistirici_baslangic_s: float = 150.0
    darbe_periyodu_s: float = 2.7     # ⚠️ trafik aralığının tam katı DEĞİL
    darbe_gorev_cevrimi: float = 0.5  # 🔒 tepe telafisi bundan TÜRETİLİR
    reaktif_sezme_s: float = 16e-6
    reaktif_patlama_s: float = 144e-6
    taramali_konak_suresi_s: float = 0.1
    taramali_konak_sayisi: int = 3

    # Tehdit senaryosu (Y5b, K-119): sinyal sınıfı senaryo adından, küme
    # biçimi bu eksenden (`kanal/tehdit.py`). Birincil hücre `derin_sizma`
    # (K-186). Süreler protokol zaman sabitleri cinsinden (çekirdek 15 s =
    # OLSR TOP_HOLD_TIME); hızlar km/h ÷ 3,6 ÷ `olcek`.
    tehdit_senaryosu: str = "tekli_merkez"
    tehdit_acik_s: float = 15.0             # yay–sus–taşın: yayın dönemi
    tehdit_sessiz_s: float = 15.0           # yay–sus–taşın: sessiz, taşınma
    tehdit_arac_hiz_kmh: float = 60.0
    tehdit_hava_hiz_kmh: float = 200.0

    # ==================================================================
    not_: str = ""

    UYGULANMAMIS_ALANLAR: ClassVar[frozenset[str]] = frozenset()

    # ------------------------------------------------------------------
    def __post_init__(self) -> None:
        dogrula(bool(self.kol.strip()), "kol adı boş olamaz")
        if self.senaryo not in SENARYOLAR:
            raise ValueError(
                f"bilinmeyen senaryo: {self.senaryo!r} — "
                f"seçenekler: {sorted(SENARYOLAR)}")

        dogrula(0.0 <= self.isinma_s < self.olcum_bitis_s <= self.kosu_bitis_s,
                "zaman sınırları tutarsız: 0 ≤ ısınma < ölçüm_bitiş ≤ koşu_bitiş")
        dogrula(self.dugum_sayisi >= 2, "en az iki düğüm gerekli")
        dogrula(self.alan_en_m > 0 and self.alan_boy_m > 0,
                "alan boyutları pozitif olmalı")
        dogrula(0.0 <= self.irtifa_min_m < self.irtifa_maks_m,
                "irtifa bandı artan ve negatif olmayan olmalı")
        dogrula(self.nominal_bag_m > 0, "nominal bağ pozitif olmalı")
        dogrula(0.0 <= self.gm_alfa < 1.0, "gm_alfa [0, 1) aralığında olmalı")
        dogrula(self.gm_adim_s > 0.0, "mobilite adımı pozitif olmalı")
        dogrula(0.0 < self.gm_hiz_min_ms <= self.gm_hiz_maks_ms,
                "hız bandı tutarsız")

        # β > 1 ve α > 0 → girişim menzili iletim menzilinden GENİŞ olur, yani
        # gizli terminal mümkün kalır. Ayrı bir "oran > 1" kontrolü YAZILMADI:
        # bundan matematiksel olarak çıkar ve asla tetiklenemezdi. Tetiklenemeyen
        # bir kontrol, koruma sağlamadan koruma izlenimi verir.
        dogrula(self.sinr_esigi_db > 0 and self.yol_kaybi_usteli > 0,
                "SINR eşiği ve yol kaybı üsteli pozitif olmalı")
        dogrula(self.bit_hizi_bps > 0 and self.bant_genisligi_hz > 0,
                "bit hızı ve bant genişliği pozitif olmalı")
        dogrula(not self.hiz_uyarlamasi or self.islem_kazanci,
                "hız uyarlaması işlem kazancı ister — CCK'nın Eb/N0 eşlemesi "
                "ancak gerçek kanal bandında anlamlı")
        dogrula(self.arf_basari_esigi >= 1 and self.arf_zamanlayici_esigi >= 1,
                "ARF eşikleri pozitif olmalı")
        dogrula(not self.islem_kazanci
                or self.bant_genisligi_hz == DSSS_KANAL_BANDI_HZ,
                "işlem kazancı açıkken gürültü bandı 802.11b DSSS kanalının "
                "bandı (22 MHz) olmalı — 2 MHz eski dünyanın birim seçimidir")
        dogrula(self.golgeleme_sigma_db >= 0.0, "gölgeleme σ negatif olamaz")
        dogrula(self.golgeleme_hucre_m > 0.0, "gölgeleme hücresi pozitif olmalı")
        dogrula(self.sonumleme_parca_suresi_s > 0.0, "parça süresi pozitif olmalı")
        dogrula(self.sonumleme_uretec in ("tekil", "blok"),
                f"bilinmeyen sönümleme üreteci: {self.sonumleme_uretec!r} — "
                f"'tekil' ya da 'blok'")
        dogrula(self.kanal_dilimi_s > 0.0, "kanal dilimi pozitif olmalı")
        dogrula(self.dunya in DUNYALAR,
                f"bilinmeyen dünya: {self.dunya!r} — seçenekler: {DUNYALAR}")
        dogrula((self.verici_eirp_dbm is None) == (self.menzil_snr_db is None),
                "verici EIRP'si ve menzildeki SNR birlikte verilir")
        dogrula(self.dunya != "referans_2026"
                or (self.olcek == 1.0 and self.verici_eirp_dbm is not None
                    and self.islem_kazanci),
                "referans dünya: ölçek 1, verici gücü girdi, işlem kazancı "
                "açık — `kanal/dunya.py::referans_2026` kurar")
        dogrula(self.tasiyici_dinleme in TASIYICI_DINLEME_KIPLERI,
                f"bilinmeyen taşıyıcı dinleme kipi: {self.tasiyici_dinleme!r} "
                f"— seçenekler: {TASIYICI_DINLEME_KIPLERI}")
        dogrula(self.karistirici_denetim_araligi_s > 0.0,
                "karıştırıcı denetim aralığı pozitif olmalı")
        dogrula(0 <= self.kayip_dugum_sayisi < self.dugum_sayisi
                and 0.0 <= self.kayip_bas_s <= self.kayip_bitis_s,
                "düğüm kaybı: sayı [0, N) ve pencere sıralı olmalı")
        dogrula(self.enerji_gonderim_w >= 0.0 and self.enerji_alim_w >= 0.0,
                "telsiz güçleri negatif olamaz")
        dogrula(min(self.gps_yatay_cep_m, self.gps_dikey_sigma_m,
                    self.gps_hiz_sigma_ms) >= 0.0
                and self.gps_tazeleme_s > 0.0,
                "GPS hataları negatif olamaz, tazeleme pozitif olmalı")
        dogrula(self.a2g_ortam in A2G_ORTAM_ADLARI,
                f"bilinmeyen yer–hava ortamı: {self.a2g_ortam!r}")
        dogrula(self.yer_karistirici_yukseklik_m > 0.0,
                "yer karıştırıcı yüksekliği pozitif olmalı")
        dogrula(0.0 < self.reaktif_sezme_olasiligi <= 1.0,
                "reaktif sezme olasılığı (0, 1] aralığında olmalı")
        dogrula(self.cca_s > 0.0,
                "CCA gecikmesi sıfır olamaz — aynı-slot çarpışması silinir")
        dogrula(1 <= self.cw_min <= self.cw_max, "çekişme penceresi tutarsız")
        dogrula(self.yeniden_deneme_siniri >= 0, "yeniden deneme sınırı negatif")
        dogrula(self.kuyruk_kapasitesi > 0, "kuyruk kapasitesi sonlu ve pozitif")
        dogrula(self.rota_tamponu_kapasitesi > 0,
                "rota bekleme tamponu kapasitesi sonlu ve pozitif olmalı — "
                "tavansız tampon sonsuz kuyruktur")
        dogrula(self.rota_tamponu_omru_s > 0.0,
                "rota bekleme tamponu ömrü pozitif olmalı")
        dogrula(self.ttl_baslangic > 0, "TTL pozitif olmalı")
        dogrula(self.akis_sayisi >= 1 and self.akis_paket_hizi_hz > 0,
                "trafik parametreleri pozitif olmalı")
        if self.trafik_deseni not in TRAFIK_DESENLERI:
            raise ValueError(
                f"bilinmeyen trafik deseni: {self.trafik_deseni!r} — "
                f"seçenekler: {TRAFIK_DESENLERI}")
        if self.trafik_deseni == "esler_arasi":
            dogrula(2 * self.akis_sayisi <= self.dugum_sayisi,
                    "akış sayısı düğüm sayısının yarısını aşamaz — "
                    "aynı düğüm birden çok akışın kaynağı olurdu")
        else:
            dogrula(self.gecit_konumu in ("kenar", "merkez"),
                    "geçit konumu `kenar` ya da `merkez` olmalı")
            dogrula(self.telemetri_paket_hizi_hz > 0
                    and self.komut_paket_hizi_hz > 0,
                    "telemetri ve komut hızı pozitif olmalı")
            dogrula(0 <= self.komut_akis_sayisi <= self.dugum_sayisi - 1,
                    "komut akışı sayısı geçit dışındaki düğüm sayısını aşamaz")
        dogrula(1 <= self.gorev_grup_sayisi <= self.dugum_sayisi,
                "mufreze sayisi 1 ile dugum sayisi arasinda olmali")
        dogrula(self.gorev_grup_yaricapi_m > 0.0
                and 2.0 * self.gorev_grup_yaricapi_m
                < min(self.alan_en_m, self.alan_boy_m),
                "grup capi alandan buyuk olamaz")
        dogrula(self.gorev_jitter_hiz_ms >= 0.0,
                "titresim hizi negatif olamaz")
        dogrula(self.istasyon_kayma_hiz_ms >= 0.0,
                "istasyon kayma hızı negatif olamaz")
        dogrula(0.0 < self.darbe_gorev_cevrimi <= 1.0,
                "darbe görev çevrimi (0, 1] aralığında olmalı")
        if self.tehdit_senaryosu not in TEHDIT_SENARYOLARI:
            raise ValueError(
                f"bilinmeyen tehdit senaryosu: {self.tehdit_senaryosu!r} — "
                f"seçenekler: {TEHDIT_SENARYOLARI}")
        dogrula(self.tehdit_acik_s > 0.0 and self.tehdit_sessiz_s > 0.0,
                "tehdit süreleri pozitif olmalı")
        dogrula(self.tehdit_arac_hiz_kmh > 0.0
                and self.tehdit_hava_hiz_kmh > 0.0,
                "tehdit platform hızları pozitif olmalı")
        dogrula(self.saat_ofset_araligi_s >= 0.0 and self.saat_sapma_ppm >= 0.0,
                "saat parametreleri negatif olamaz")

        # 🔴 Güç override yalnız güç taraması içindir ve NİHAİ güçtür: darbeli
        # bir senaryoyla birleşirse "aynı ortalama güç" koşulu sessizce kırılır.
        if (self.karistirici_guc_override_dbm is not None
                and SENARYOLAR[self.senaryo].darbeli):
            raise ValueError(
                "karistirici_guc_override_dbm darbeli senaryoyla "
                "birleştirilemez: override nihai güçtür, tepe telafisi "
                "uygulanmaz ve 'aynı ortalama güç' koşulu kırılır.")


    # ==================================================================
    # TÜRETİLENLER — elle yazılmış sayı YOK
    # ==================================================================
    @property
    def mobilite_kolu(self) -> str:
        """Mobilite kolu — bir yapılandırma bayrağı: `statik` · `bagimsiz`
        (Gauss-Markov) · `gorev` (koordineli sürü) · `formasyon` (istasyon
        tutma; birincil hücre)."""
        return SENARYOLAR[self.senaryo].mobilite_kolu

    @property
    def hareketli(self) -> bool:
        """Turetilmis: `statik` disindaki her kol hareketlidir."""
        return SENARYOLAR[self.senaryo].hareketli

    @property
    def karistirici_sinifi(self) -> str:
        return SENARYOLAR[self.senaryo].karistirici_sinifi

    @property
    def karistirici_darbeli(self) -> bool:
        return SENARYOLAR[self.senaryo].darbeli

    @property
    def karistirici_var_mi(self) -> bool:
        return SENARYOLAR[self.senaryo].karistirici_var_mi

    # ------------------------------------------------------ ölçek eşlemesi
    # 🔒 `olcek` bu özellikler üzerinden OKUNUR — uyuyan bir alan değildir.
    # Gösterim katmanı da ("1 m = N m · bu kutu X km") verisini buradan alır,
    # sonradan uydurmaz.
    @property
    def gercek_alan_km(self) -> float:
        """Kutunun gerçek dünyadaki kenar uzunluğu."""
        return self.alan_en_m * self.olcek / 1000.0

    @property
    def gercek_capa_km(self) -> float:
        """Güç çapasının gerçek karşılığı."""
        return self.nominal_bag_m * self.olcek / 1000.0

    @property
    def gercek_hiz_araligi_kmh(self) -> tuple[float, float]:
        """Simüle edilen hızların gerçek karşılığı — A5a ile karşılaştırılır."""
        return (self.gm_hiz_min_ms * self.olcek * 3.6,
                self.gm_hiz_maks_ms * self.olcek * 3.6)

    @property
    def gercek_irtifa_km(self) -> tuple[float, float]:
        return (self.irtifa_min_m * self.olcek / 1000.0,
                self.irtifa_maks_m * self.olcek / 1000.0)

    @property
    def olcek_guc_farki_db(self) -> float:
        """`Pt_gerçek = Pt_sim + bu` — eski dünyanın ölçek eşlemesi; fiziksel
        olarak var olabilecek bir verici vermelidir (α = 3'ü eleyen hesap)."""
        return 10.0 * self.yol_kaybi_usteli * math.log10(self.olcek)

    @property
    def girisim_orani(self) -> float:
        """Girişim menzilinin iletim menziline oranı — TÜRETİLMİŞ.

        Menzilde girişimsiz SNR `snr_R` ise, gücü gürültü tabanına eşit
        girişimcinin mesafesi D = snr_R^(1/α) · R. Referansta snr_R =
        `menzil_snr_db` (nominal bağ, 10 dB paylı); eski dünyada β.
        """
        snr_db = (self.sinr_esigi_db if self.menzil_snr_db is None
                  else self.menzil_snr_db)
        return (10.0 ** (snr_db / 10.0)) ** (1.0 / self.yol_kaybi_usteli)

    @property
    def girisim_menzili_m(self) -> float:
        return self.nominal_bag_m * self.girisim_orani

    @property
    def difs_s(self) -> float:
        return self.sifs_s + 2 * self.slot_s

    @property
    def komsu_omru_s(self) -> float:
        """Komşu kaydının BELLEKTE tutulduğu süre — TÜRETİLMİŞ.

        Beacon aralığının katı olarak yazılır ki beacon aralığı değişince
        ömür sessizce ayrışmasın. ⚠️ Bir tazelik eşiği DEĞİL: tazelik kararı
        protokolündür, bu yalnız komşu tablosunun sınırsız büyümesini önler.
        """
        return self.komsu_omru_katsayisi * self.beacon_araligi_s

    @property
    def olcum_penceresi(self) -> tuple[float, float]:
        """Metriklerin hesaplandığı aralık.

        ⚠️ Korunum denklemi BU aralıkta değil, TÜM koşu üzerinden kontrol
        edilir — ikisi ayrı defterdir.
        """
        return (self.isinma_s, self.olcum_bitis_s)

    @property
    def tepe_telafisi_db(self) -> float:
        """Darbeli karıştırıcının tepe gücüne eklenen telafi — TÜRETİLMİŞ.

        Ortalama = tepe × görev çevrimi; ortalamayı sabit karşılığına
        eşitlemek için tepeyi 1/d kadar yükseltmek gerekir. Bir modül sabiti
        OLARAK yazılsaydı görev çevrimiyle ikinci bir doğru kaynağı oluşur ve
        ikisi bağımsız değişebilirdi.
        """
        return 10.0 * math.log10(1.0 / self.darbe_gorev_cevrimi)

    @property
    def karistirici_guc_dbm(self) -> float | None:
        """Karıştırıcının TEPE gücü. `None` = ölçülmedi (0,0 DEĞİL)."""
        if self.karistirici_guc_override_dbm is not None:
            return self.karistirici_guc_override_dbm
        taban = (KARISTIRICI_GUCU_DBM[self.karistirici_sinifi]
                 if self.karistirici_taban_dbm is None
                 else self.karistirici_taban_dbm)
        if taban is None:
            return None
        return taban + self.tepe_telafisi_db if self.karistirici_darbeli else taban

    @property
    def karistirici_merkez(self) -> tuple[float, float]:
        """Varsayılan alanın merkezi — tohumlar arasında KARŞILAŞTIRILABİLİR.

        Rastgele bir karıştırıcı konumu, tohumlar arası varyansa karıştırıcının
        nereye düştüğünü de katardı ve protokol farkını gizlerdi.
        """
        return self.karistirici_konum or (self.alan_en_m / 2.0,
                                          self.alan_boy_m / 2.0)

    @property
    def yere_toplama(self) -> bool:
        return self.trafik_deseni == "yere_toplama"

    @property
    def gecit(self) -> int | None:
        """Geçit düğümü — yere toplamada düğüm 0; eşler arası desende yok."""
        return 0 if self.yere_toplama else None

    @property
    def sunulan_paket_hizi_hz(self) -> float:
        """Ağa sunulan toplam paket hızı — teşhis ve yük kontrolü için."""
        if self.yere_toplama:
            return ((self.dugum_sayisi - 1) * self.telemetri_paket_hizi_hz
                    + self.komut_akis_sayisi * self.komut_paket_hizi_hz)
        return self.akis_sayisi * self.akis_paket_hizi_hz

    # ------------------------------------------------------------------
    def sozluk(self) -> dict[str, Any]:
        """Sonuç satırına yazılacak TAM konfigürasyon."""
        return asdict(self)


# ===========================================================================
# 🔴 KÖKEN KAPSAMASI — GEREKÇESİZ PARAMETRE DEPOYA GİREMEZ
# ===========================================================================
# `Konfig`in her alanı `kokenler.KOKENLER`de bir kovaya yazılmak zorundadır.
# Bu denetim İÇE AKTARMA anında koşar: eksik bir alan varsa modül hiç
# yüklenmez ve hiçbir koşu başlamaz.
#
# 🔒 Neden burada ve neden import anında: bir sonraki geliştirici `Konfig`e
# alan eklediğinde, o alanın nereden geldiğini yazmayı UNUTAMASIN diye.
# Disiplin değil, mekanizma — `cekirdek/sayaclar.py`nin sayaçlar için
# yaptığının parametreler için yapılmış hâli.
_eksik, _fazla = _kokenler.eksik_alanlar(
    tuple(_a.name for _a in _dc.fields(Konfig)))
if _eksik:
    raise _DegismezHatasi(
        f"kökeni yazılmamış Konfig alanı: {_eksik}. Her parametre "
        f"sim2/yapilandirma/kokenler.py'de bir kovaya yazılmak zorundadır "
        f"(kovalar: `kokenler.KOVALAR`).")
if _fazla:
    raise _DegismezHatasi(
        f"artık var olmayan alan için köken kaydı: {_fazla}. Kayıt "
        f"defterinde ölü giriş bırakmak, kaydın güvenilirliğini bitirir.")
