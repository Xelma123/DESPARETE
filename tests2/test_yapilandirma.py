"""
ADIM 3 — `sim2/yapilandirma/` kapanış ölçütleri.

Bu dosyanın koruduğu üç şey:
  1. `Konfig`de İKİNCİ bir çerçeve/bit sayımı yok (kusur 1'in geri gelme yolu)
  2. Bildirilmiş ama kimsenin okumadığı alan, sonuç satırını yalancı yapamaz
  3. Uygulanmamış bir karıştırıcı sınıfı sessizce etkisiz kalamaz
"""

from __future__ import annotations

import ast
import dataclasses
import math
import pathlib
import sys

import pytest

KOK = pathlib.Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

SIM2 = KOK / "sim2"

from sim2.cekirdek.degismezler import DegismezHatasi  # noqa: E402
from sim2.yapilandirma.konfig import HENUZ_OKUNMAYAN, Konfig  # noqa: E402
from sim2.yapilandirma.kokenler import (  # noqa: E402
    DUYARLILIK_BEKLEYEN, KOKENLER, KOVALAR, MODUL_KOKENLERI,
    duyarlilik_borcu, eksik_alanlar, kova_sayimi)
from sim2.yapilandirma.senaryolar import (  # noqa: E402
    KARISTIRICI_GUCU_DBM, KARISTIRICI_SINIFLARI, MOBILITE_KOLLARI,
    SENARYOLAR, UYGULANMAMIS_KARISTIRICI, senaryo_adi)


def _alan_adlari() -> set[str]:
    return {f.name for f in dataclasses.fields(Konfig)}


def _sim2_dosyalari(haric: set[str] = frozenset()):
    for yol in sorted(SIM2.rglob("*.py")):
        if "__pycache__" in yol.parts or yol.name in haric:
            continue
        yield yol


# ==========================================================================
# SENARYOLAR — mobilite bir EKSEN
# ==========================================================================

def test_senaryolar_capraz_carpim():
    assert len(SENARYOLAR) == len(MOBILITE_KOLLARI) * len(KARISTIRICI_SINIFLARI)
    for m in MOBILITE_KOLLARI:
        for j in KARISTIRICI_SINIFLARI:
            t = SENARYOLAR[senaryo_adi(m, j)]
            assert t.mobilite_kolu == m
            assert t.hareketli == (m != "statik")
            assert t.karistirici_sinifi == j


def test_U1_kolu_STATIK_ve_karistiricisiz():
    """🔒 U1 (*statik + bağlı → PDR ≈ 1*) yalnız burada koşabilir.

    Mobil kolda ağ zamanın %17,6'sında bölünüyor; PDR ≈ 1 tanım gereği
    imkânsız. Statik kolda ise tohumların %26,7'si kalıcı olarak kopuk —
    "bağlı" bir dayatma değil, bir TOHUM SÜZGECİ.
    """
    t = SENARYOLAR["statik-yok"]
    assert t.hareketli is False
    assert t.karistirici_var_mi is False


def test_karistirici_gucleri_OLCULDU_yok_HARIC():
    """🔴 `None` = ölçülmedi. `0.0` olsaydı ölçülmemiş bir hücre ortalamaya
    girerdi ve kimse fark etmezdi.

    8 Eylül 2026: güçler ölçüldü (`kalibrasyon/karistirici_gucu.py`) ve tablo
    doldu. `yok` kolunda `None` DOĞRUDUR — orada karıştırıcı yoktur.
    """
    assert KARISTIRICI_GUCU_DBM["yok"] is None, \
        "'yok' kolunda güç olamaz"
    olculmus = {s: g for s, g in KARISTIRICI_GUCU_DBM.items() if s != "yok"}
    assert all(isinstance(g, float) for g in olculmus.values()), \
        f"ölçülmemiş sınıf kaldı: {[s for s, g in olculmus.items() if g is None]}"
    # 🔒 TEK TABAN: çalışma noktası referans sınıfta seçilir ve hepsine
    # aynı taban gider. Sınıf başına ayrı güç, ρ bağımlı değişken olduğu için
    # aradığımız mekanizma farkını kalibrasyonla silerdi.
    assert len(set(olculmus.values())) == 1, \
        f"sınıflar aynı tabanı taşımalı: {olculmus}"


def test_guc_tablosu_ile_sinif_listesi_AYRISAMAZ():
    assert set(KARISTIRICI_GUCU_DBM) == set(KARISTIRICI_SINIFLARI)


# ==========================================================================
# KONFİG — temel sözleşme
# ==========================================================================

def test_konfig_DONDURULMUS():
    k = Konfig(kol="deneme")
    with pytest.raises(dataclasses.FrozenInstanceError):
        k.tohum = 7  # type: ignore[misc]


def test_bilinmeyen_senaryo_REDDEDILIYOR():
    with pytest.raises(ValueError):
        Konfig(kol="deneme", senaryo="uzay-yok")


def test_Y4_bilinmeyen_trafik_deseni_REDDEDILIYOR():
    with pytest.raises(ValueError):
        Konfig(kol="d", trafik_deseni="yayin")


def test_Y4_yere_toplama_DOGRULAMALARI_ve_GECIT_NOKTASI():
    with pytest.raises(DegismezHatasi):
        Konfig(kol="d", trafik_deseni="yere_toplama", gecit_konumu="tepe")
    with pytest.raises(DegismezHatasi):
        Konfig(kol="d", trafik_deseni="yere_toplama", komut_akis_sayisi=40)
    with pytest.raises(DegismezHatasi):
        Konfig(kol="d", trafik_deseni="yere_toplama",
               telemetri_paket_hizi_hz=0.0)
    from sim2.dunya.yerlesim import gecit_noktasi
    k = Konfig(kol="d", trafik_deseni="yere_toplama")
    assert k.yere_toplama and k.gecit == 0
    x, y, z = gecit_noktasi(k)
    assert (x, y) == (0.0, k.alan_boy_m / 2.0), "kenar: batı kenarının ortası"
    assert k.irtifa_min_m < z < k.irtifa_maks_m
    m = Konfig(kol="d", trafik_deseni="yere_toplama", gecit_konumu="merkez")
    assert tuple(gecit_noktasi(m))[:2] == (m.alan_en_m / 2.0, m.alan_boy_m / 2.0)
    assert gecit_noktasi(Konfig(kol="d")) is None


def test_bos_kol_adi_reddediliyor():
    with pytest.raises(DegismezHatasi):
        Konfig(kol="   ")


@pytest.mark.parametrize("degisiklik", [
    dict(isinma_s=400.0),                 # ısınma > ölçüm bitişi
    dict(olcum_bitis_s=400.0),            # ölçüm bitişi > koşu bitişi
    dict(irtifa_min_m=130.0),             # bant artan değil (min > maks)
    dict(irtifa_maks_m=10.0),             # bant artan değil
    dict(dugum_sayisi=1),                 # tek düğüm
    dict(cca_s=0.0),                      # aynı-slot çarpışması silinir
    dict(cw_min=2000),                    # cw_min > cw_max
    dict(kuyruk_kapasitesi=0),            # sonsuz/sıfır kuyruk
    dict(ttl_baslangic=0),
    dict(akis_sayisi=30),                 # 2*akış > düğüm
    dict(darbe_gorev_cevrimi=0.0),
    dict(gm_alfa=1.0),
    dict(sinr_esigi_db=0.0),
])
def test_tutarsiz_konfig_REDDEDILIYOR(degisiklik):
    with pytest.raises((DegismezHatasi, ValueError)):
        Konfig(kol="deneme", **degisiklik)


def test_secilen_calisma_noktasi_VARSAYILAN():
    """Öğrencinin verdiği kararlar varsayılan olmalı — bir kolun kurulumu
    kod düzenlemesi gerektirmemeli."""
    k = Konfig(kol="deneme")
    # ⚠️ 1000 → 1800 m, 5 Eylül 2026 (K-097). Alan ELLE seçilmedi:
    # statik kolda 30 tohumun hiçbirinde ulaşılamaz çift kalmayan EN
    # BÜYÜK alandır. Eski alanda çiftlerin %99,7'si bir ya da iki
    # atlamaydı — yönlendirmenin ifade edebileceği fark yoktu.
    # Üretici: `python kalibrasyon/calisma_noktasi.py`
    assert (k.alan_en_m, k.alan_boy_m) == (1800.0, 1800.0)
    assert (k.irtifa_min_m, k.irtifa_maks_m) == (20.0, 120.0)
    # 🔒 280 m VERİCİ GÜCÜNÜN ÇAPASIDIR, bağlantılılık yarıçapı değil.
    # Veri yolunda hiçbir yeri kapamaz (K-096).
    assert k.iletim_menzili_m == 280.0
    assert k.yol_kaybi_usteli == 2.0   # hava-hava, serbest uzay (K-097)
    assert k.dugum_sayisi == 40
    assert k.bit_hizi_bps == 2e6 and k.paket_bayt == 512
    assert k.akis_sayisi == 10 and k.akis_paket_hizi_hz == 4.0
    assert k.modulasyon == "dqpsk"
    assert k.golgeleme_acik and k.sonumleme_acik and k.anten_deseni_acik


# ==========================================================================
# 🔴 KUSUR 1 — ikinci bir bit/süre sayımı yazılamaz
# ==========================================================================

def test_konfig_CERCEVE_SURESI_HESAPLAMIYOR():
    """🔴 Kusur 1'in geri gelme yolu tam olarak buydu.

    Eski `Konfig`de `cerceve_suresi_s(bayt)` vardı ve `mac.alim_per` onu
    kullanıyordu; `radio.paket_hata_olasiligi` ise yalnız yükü sayıyordu.
    Ölçüldü: 1024 B @ 1 Mb/s'te %2,34, yeni parametrelerde (512 B @ 2 Mb/s)
    **%9,38** ayrışma. Süre ve hataya açık bit yalnız `kanal/cerceve.py`de
    tanımlanacak.
    """
    yasak = {"bit_hizi_bps", "onbelge_s", "paket_bayt", "onay_bayt"}
    agac = ast.parse((SIM2 / "yapilandirma" / "konfig.py")
                     .read_text(encoding="utf-8"))
    # Yasaklanan şey ARİTMETİK: `dogrula(self.bit_hizi_bps > 0, ...)` bir
    # karşılaştırmadır ve meşrudur; `self.onbelge_s + bayt * 8 / self.
    # bit_hizi_bps` ikinci bir çerçeve süresi tanımıdır ve değildir.
    ihlal: list[str] = []
    for n in ast.walk(agac):
        if not isinstance(n, ast.BinOp):
            continue
        for alt in ast.walk(n):
            if isinstance(alt, ast.Attribute) and alt.attr in yasak:
                ihlal.append(f"satır {n.lineno} → {alt.attr}")
    assert not ihlal, (
        f"🔴 `Konfig` çerçeve süresi/bit sayısı hesaplıyor: {ihlal}. "
        f"Bu alanlar yalnız BİLDİRİLİR; kullanan tek yer `kanal/cerceve.py`.")
    for ad in ("cerceve_suresi_s", "paket_suresi_s", "onay_suresi_s"):
        assert not hasattr(Konfig, ad), f"🔴 `Konfig.{ad}` ikinci bir sayımdır"


# ==========================================================================
# TÜRETİLENLER — elle yazılmış sayı yok
# ==========================================================================

def test_girisim_orani_TURETILMIS_elle_yazilmamis():
    """🔒 Oran β ve α'dan TÜRETİLİR — burada da elle sayı yazılmaz.

    ⚠️ 5 Eylül 2026: β 10 → 16 dB olunca bu testteki `10 ** (1/3)` sabiti
    kırıldı ve KIRILMASI GEREKİYORDU — testin işi tam olarak bu. Sabit
    yerine formül yazıldı; artık β değişince test kendiliğinden takip eder,
    ama formül değişirse yine kırılır.
    """
    k = Konfig(kol="deneme")
    beklenen = (10.0 ** (k.sinr_esigi_db / 10.0)) ** (1.0 / k.yol_kaybi_usteli)
    assert k.girisim_orani == pytest.approx(beklenen, rel=1e-12)
    assert k.girisim_menzili_m == pytest.approx(k.iletim_menzili_m * beklenen)
    # Elle yazılmış olsaydı β değişince sessizce yanlış kalırdı.
    k2 = Konfig(kol="deneme", sinr_esigi_db=k.sinr_esigi_db + 3.0)
    assert k2.girisim_orani > k.girisim_orani
    k3 = Konfig(kol="deneme", yol_kaybi_usteli=4.0)
    assert k3.girisim_orani < k.girisim_orani


def test_girisim_menzili_iletim_menzilinden_GENIS():
    """β > 1 ve α > 0 iken oran zorunlu olarak 1'den büyüktür → gizli
    terminal mümkün kalır. Ayrı bir kontrol yazılmadı çünkü tetiklenemezdi."""
    for esik in (3.0, 10.0, 20.0):
        for ustel in (2.0, 3.0, 4.0):
            k = Konfig(kol="d", sinr_esigi_db=esik, yol_kaybi_usteli=ustel)
            assert k.girisim_menzili_m > k.iletim_menzili_m


def test_tepe_telafisi_TURETILMIS():
    """Modül sabiti olsaydı görev çevrimiyle ikinci bir doğru kaynağı olurdu
    ve ikisi bağımsız değişebilirdi (eski depoda ölçülmüş: −6,99 dB'e kadar
    sessiz sapma)."""
    assert Konfig(kol="d", darbe_gorev_cevrimi=0.5).tepe_telafisi_db == \
        pytest.approx(10.0 * math.log10(2.0))
    assert Konfig(kol="d", darbe_gorev_cevrimi=0.25).tepe_telafisi_db == \
        pytest.approx(10.0 * math.log10(4.0))
    assert Konfig(kol="d", darbe_gorev_cevrimi=1.0).tepe_telafisi_db == \
        pytest.approx(0.0)


def test_mobilite_kolu_SENARYODAN_geliyor():
    """🔒 Mobilite bir konfigürasyon bayrağıdır; kod düzenlemesiyle üretilen
    bir kol kaynağından ayırt edilemez.

    🔒 ÜÇ KOL: `statik` (U1 sanity) · `bagimsiz` (Gauss-Markov, literatürün
    standardı) · `gorev` (sektörlü koordineli sürü). Üçüncüsü bir ÖLÇÜMÜN
    sonucu olarak eklendi — bağımsız kolda komşular arası bağıl hız 26,0 m/s
    ve rota ömrü 2,3 s çıkıyordu.
    """
    assert Konfig(kol="d", senaryo="statik-yok").mobilite_kolu == "statik"
    assert Konfig(kol="d", senaryo="statik-yok").hareketli is False
    assert Konfig(kol="d", senaryo="bagimsiz-yok").mobilite_kolu == "bagimsiz"
    assert Konfig(kol="d", senaryo="bagimsiz-yok").hareketli is True
    assert Konfig(kol="d", senaryo="gorev-yok").mobilite_kolu == "gorev"
    assert Konfig(kol="d", senaryo="gorev-yok").hareketli is True


def test_karistirici_gucu_None_kaliyor():
    assert Konfig(kol="d", senaryo="statik-yok").karistirici_guc_dbm is None


def test_sunulan_yuk_turetilmis():
    assert Konfig(kol="d").sunulan_paket_hizi_hz == pytest.approx(40.0)


def test_olcum_penceresi_ve_difs():
    k = Konfig(kol="d")
    assert k.olcum_penceresi == (50.0, 320.0)
    assert k.difs_s == pytest.approx(k.sifs_s + 2 * k.slot_s)


# ==========================================================================
# 🔴 UYGULANMAMIŞ KARIŞTIRICI — sessizce etkisiz kalamaz
# ==========================================================================

def test_UYGULANMAMIS_KARISTIRICI_bosaldi_ve_KAPI_YER_DEGISTIRDI():
    """🟢 Beş sınıfın beşi de uygulandı; liste boşaldı.

    🔴 Boş bir liste, kapının KALKTIĞI anlamına gelmez — YER DEĞİŞTİRDİ.
    Eski kapı *"uygulanmamış sınıfla koşma"*yı engelliyordu ve tetiklenemez
    hâle gelince kaldırıldı (tetiklenemeyen bir kontrol, koruma sağlamadan
    koruma izlenimi verir). Yerini alan kapı farklı bir şeyi koruyor:
    *ölçülmemiş güçle koşma*. Testi `test_karistirici.py`de.

    Bu test, listeye yeni bir sınıf eklenip UYGULANMADAN bırakılırsa konuşur.
    """
    from sim2.kanal.karistirici import _SINIFLAR
    assert UYGULANMAMIS_KARISTIRICI == frozenset()
    kurulabilen = set(_SINIFLAR) | {"yok"}
    eksik = sorted(set(KARISTIRICI_SINIFLARI) - kurulabilen)
    assert not eksik, (
        f"🔴 bildirilmiş ama kurucusu olmayan karıştırıcı sınıfı: {eksik}")
    # ve her senaryo gerçekten kurulabiliyor olmalı
    for sinif in KARISTIRICI_SINIFLARI:
        Konfig(kol="d", senaryo=senaryo_adi("statik", sinif))


def test_override_DARBELI_senaryoyla_birlesemez():
    """🔴 Bu kontrolün SIRASI önemli: uygulanmamış-sınıf kontrolünden ÖNCE
    koşmalı, yoksa hiç tetiklenemez ve koruma sağlamadan koruma izlenimi
    verir."""
    with pytest.raises(ValueError):
        Konfig(kol="d", senaryo="statik-surekli_darbeli",
               karistirici_guc_override_dbm=2.0)


# ==========================================================================
# 🔴 BİLDİRİM ≠ KULLANIM — iki yönlü
# ==========================================================================

def _konfig_erisimi_mi(n: ast.Attribute) -> bool:
    """`n` gerçekten bir `Konfig` alanına mı erişiyor?

    🔴 İLK YAZIMDA YALNIZ ADA BAKIYORDU ve yanlış pozitif verdi:
    `Gozlem.kuyruk_kapasitesi` ile `Konfig.kuyruk_kapasitesi` aynı adı
    taşıyor; gözlem penceresi yazılınca test "artık okunuyor" dedi, oysa
    okunan `Konfig`in alanı değildi. Aynı sınıf bir çakışma daha önce
    `kol`da yaşandı ve orada yeniden adlandırmayla çözülmüştü — ama iki
    alanın MEŞRU olarak aynı adı taşıdığı durumda çözüm testi keskinleştirmek.

    Kural: erişimin KAYNAĞI `konfig` ya da `self.konfig` olmalı.
    """
    kok = n.value
    if isinstance(kok, ast.Name):
        return kok.id in {"konfig", "kon", "k"}
    if isinstance(kok, ast.Attribute):
        return kok.attr == "konfig"
    return False


def _okunan_alanlar() -> set[str]:
    """`sim2/` içinde bir `Konfig` alanı olarak erişilen adlar.

    `konfig.py` hariç: bir alanın kendi türetilmiş özelliği tarafından
    okunması, o alanın bir DAVRANIŞI etkilediğini kanıtlamaz.
    """
    adlar: set[str] = set()
    for yol in _sim2_dosyalari(haric={"konfig.py"}):
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        for n in ast.walk(agac):
            if isinstance(n, ast.Attribute) and _konfig_erisimi_mi(n):
                adlar.add(n.attr)
    return adlar


def test_her_alan_ya_OKUNUYOR_ya_HENUZ_OKUNMAYAN_da():
    alanlar = _alan_adlari()
    okunan = _okunan_alanlar()
    sahipsiz = sorted(a for a in alanlar
                      if a not in okunan and a not in HENUZ_OKUNMAYAN)
    assert not sahipsiz, (
        f"🔴 Bu alanları hiçbir `sim2/` modülü okumuyor ve "
        f"`HENUZ_OKUNMAYAN`da da yazmıyorlar: {sahipsiz}. "
        f"Sonuç satırına yazılan ama hiçbir şeyi etkilemeyen bir parametre "
        f"satırı yalancı yapar.")


def test_HENUZ_OKUNMAYAN_bayatlayamaz():
    """Listeye giren bir alan fiilen okunmaya başlarsa test kırılır — liste
    modüller indikçe KISALMAK zorunda."""
    alanlar = _alan_adlari()
    okunan = _okunan_alanlar()
    hayalet = sorted(a for a in HENUZ_OKUNMAYAN if a not in alanlar)
    assert not hayalet, f"🔴 `HENUZ_OKUNMAYAN`da olmayan alan: {hayalet}"
    bayat = sorted(a for a in HENUZ_OKUNMAYAN if a in okunan)
    assert not bayat, (
        f"🔴 Artık okunuyor ama hâlâ `HENUZ_OKUNMAYAN`da: {bayat}. "
        f"Listeden çıkar — bayat bir gerekçe, gerekçe değildir.")


def test_adim3_te_okunan_alanlar_GERCEKTEN_dunyayi_kuruyor():
    """Listede olmayan alanların hangileri olduğunu SABİTLER.

    Bu test bir sayıyı değil, bir SÖZLEŞMEYİ tutar: her adım bu kümeyi
    büyütür ve testi BİLİNÇLİ olarak günceller. Sessizce büyümesi, sonuç
    satırındaki bir parametrenin fark edilmeden anlam kazanması demek olurdu.
    """
    dunya = {
        "dugum_sayisi", "alan_en_m", "alan_boy_m",
        "irtifa_min_m", "irtifa_maks_m", "iletim_menzili_m", "kosu_bitis_s",
        "gm_alfa", "gm_adim_s", "gm_hiz_min_ms", "gm_hiz_maks_ms",
        "gm_hiz_sigma_ms", "gm_azimut_sigma_rad", "gm_pitch_ort_rad",
        "gm_pitch_sigma_rad",
        "gorev_grup_sayisi", "gorev_grup_yaricapi_m", "gorev_jitter_hiz_ms",
        # 🔒 Y4 — dunya/yerlesim.py geçit noktası (11 Eylül 2026, bilinçli).
        "gecit_konumu",
        # 🔒 Y6 — dunya/topoloji.py formasyon kolunun kayma ekseni (11 Eylül 2026).
        "istasyon_kayma_hiz_ms",
    }
    kanal = {
        # kanal/cerceve.py
        "bit_hizi_bps", "temel_bit_hizi_bps", "onbelge_s",
        "paket_bayt", "onay_bayt", "beacon_bayt",
        # kanal/yayilim.py
        "frekans_hz", "yol_kaybi_usteli", "sinr_esigi_db", "gurultu_figuru_db",
        "sicaklik_k", "bant_genisligi_hz", "tohum",
        "golgeleme_acik", "golgeleme_sigma_db", "golgeleme_hucre_m",
        "anten_deseni_acik",
        # kanal/sonumleme.py
        "sonumleme_acik", "rician_k_db", "sonumleme_parca_suresi_s",
        # kanal/kanal.py
        "modulasyon",
        # 🔒 Y5b — kanal/tehdit.py aileleri ve yapilandirma/kapsam.py beyanı
        # (11 Eylül 2026, bilinçli).
        "tehdit_senaryosu", "tehdit_acik_s", "tehdit_sessiz_s",
        "tehdit_arac_hiz_kmh", "tehdit_hava_hiz_kmh",
        # kanal/karistirici.py
        "darbe_periyodu_s", "darbe_gorev_cevrimi",
        "reaktif_sezme_s", "reaktif_patlama_s",
        "taramali_konak_suresi_s", "taramali_konak_sayisi",
        "kanal_dilimi_s",
        # 🔴 `karistirici_baslangic_s` — 8 Eylül 2026. Karıştırıcı t=150 s'de
        # devreye giriyor; öncesi temiz evre, sonrası şok evresi. Bu test onu
        # DEFTERE YAZMADIĞIM için kırıldı ve haklıydı: alanı ekleyip
        # kaydetmemek, "hangi alan gerçekten okunuyor" muhasebesini bozar.
        "karistirici_baslangic_s",
        # 🔴 `olcek` — kanal/sonumleme.py, 8 Eylül 2026. Doppler TAM ÖLÇEK
        # hızından hesaplanıyor: dalga boyu ölçeklenemediği için ölçekli hız
        # kullanılsaydı kanal çerçeve boyunca donardı (çerçeve/T_c 0,03 ↔
        # 1,35). Ölçek artık bir raporlama parametresi DEĞİL, fiziğe giriyor.
        "olcek",
    }
    mac = {
        # mac/alici.py
        "yakalama_etkisi_acik", "yakalama_esigi_db", "yakalama_penceresi_s",
        # mac/dcf.py
        "slot_s", "sifs_s", "cca_s", "cw_min", "cw_max",
        "yeniden_deneme_siniri",
    }

    ag = {
        # ag/trafik.py · ag/kuyruk.py
        "akis_sayisi", "akis_paket_hizi_hz", "cbr_titresim_s",
        "ttl_baslangic", "olcum_bitis_s",
        # 🔒 Y4 · yere toplama — 11 Eylül 2026, BİLİNÇLİ olarak eklendi.
        # `trafik_deseni`: ag/trafik.py dalı · dunya/yerlesim.py geçit noktası
        # · yapilandirma/kapsam.py beyanı. Hızlar ve komut sayısı: ag/trafik.py.
        "trafik_deseni", "telemetri_paket_hizi_hz", "komut_akis_sayisi",
        "komut_paket_hizi_hz",
    }
    # 🔒 ADIM 9 — `kosum/`. Bu küme 5 Eylül 2026'da BİLİNÇLİ olarak eklendi.
    kosum = {
        # kosum/kurulum.py — saat ve kuyruk `Konfig` almayan modüllere
        # buradan taşınır (katman yönü)
        "saat_senkron", "saat_ofset_araligi_s", "saat_sapma_ppm",
        "kuyruk_kapasitesi",
        # kosum/kosu.py — beacon çizelgesi
        "beacon_araligi_s",
        # kosum/sonuc.py — sonuç satırının kimlik bölümü
        "kol", "not_", "senaryo",
        # 🔒 K-131 · rota bekleme tamponu — `kosum/dugum.py::beklemeye_al`
        # ikisini de okur, `yapilandirma/kapsam.py` ikisini de BEYAN eder.
        # ⚠️ Bu test onları deftere yazmadığım için kırıldı ve haklıydı:
        # alanı ekleyip kaydetmemek, "hangi alan gerçekten okunuyor"
        # muhasebesini bozar — `karistirici_baslangic_s`ın 8 Eylül'deki
        # aynı dersi.
        "rota_tamponu_kapasitesi", "rota_tamponu_omru_s",
    }
    assert _alan_adlari() - HENUZ_OKUNMAYAN == dunya | kanal | ag | mac | kosum


# ==========================================================================
# SONUÇ SATIRI
# ==========================================================================

def test_sozluk_TUM_alanlari_tasiyor_turevleri_TASIMIYOR():
    s = Konfig(kol="d").sozluk()
    assert set(s) == _alan_adlari()
    # Türetilenler sözlüğe girmez: girselerdi sonuç satırında aynı bilginin
    # iki kopyası olur ve biri bayatlayabilirdi.
    for turev in ("hareketli", "girisim_orani", "difs_s", "karistirici_sinifi"):
        assert turev not in s


def test_yapilandirma_dunyayi_ICE_AKTARMIYOR():
    """Katman yönü tek yönlü: `cekirdek → yapilandirma → dunya`."""
    ihlal: list[str] = []
    for yol in sorted((SIM2 / "yapilandirma").rglob("*.py")):
        if "__pycache__" in yol.parts:
            continue
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        for n in ast.walk(agac):
            if isinstance(n, ast.ImportFrom) and n.module:
                if n.module.startswith(("sim2.dunya", "sim2.kanal", "sim2.mac",
                                        "sim2.ag", "sim2.gozlem", "sim2.olcum",
                                        "sim2.kosum")):
                    ihlal.append(f"{yol.name}:{n.lineno} → {n.module}")
    assert not ihlal, f"🔴 katman yönü kırıldı: {ihlal}"


# ==========================================================================
# 🔴 RNG — belgelenen mekanizma KODLA UYUŞMALI
# ==========================================================================

def test_SIRALI_AKIS_eklemek_eski_cekimleri_KAYDIRMIYOR():
    """🔴 `rng.py`nin eski açıklaması bunun tersini iddia ediyordu.

    *"Bu listeye akış eklemek çekim sırasını kaydırır ve daha önce ölçülmüş
    HER SAYIYI bayatlatır."* — ölçüldü, YANLIŞ. Her akış kendi adından
    tohumlandığı için akışlar arasında paylaşılan bir sıra yok.

    Bu testin varlık sebebi: yanlış bir mekanizma açıklaması yanlış KARARLAR
    doğurur. O cümle duruyor olsaydı, mobilite modeline yeni bir akış eklemek
    *"tüm ölçümleri bayatlatır"* diye reddedilirdi — oysa bayatlatmıyor.
    """
    import sim2.cekirdek.rng as R

    def cekimler(adlar):
        eski = R.AKIS_ADLARI
        try:
            R.AKIS_ADLARI = adlar
            a = R.Akislar(1234)
            return {ad: [a[ad].random() for _ in range(30)] for ad in eski}
        finally:
            R.AKIS_ADLARI = eski

    once = cekimler(R.AKIS_ADLARI)
    sonra = cekimler(R.AKIS_ADLARI[:3] + ("yeni_deneme_akisi",)
                     + R.AKIS_ADLARI[3:])
    kayan = [ad for ad in once if once[ad] != sonra[ad]]
    assert not kayan, (
        f"🔴 akış eklemek şu akışların çekimlerini kaydırdı: {kayan}. "
        f"Her akış kendi adından tohumlanmalı.")


def test_AYNI_akistan_fazladan_cekim_SIRAYI_KAYDIRIR():
    """🔒 Gerçek tehlikenin kendisi — yukarıdakinin aynadaki hâli.

    Sırayı kaydıran şey listeye ad eklemek DEĞİL, var olan bir akıştan
    fazladan çekim yapmaktır. `protokol_kesif`in düğüm başına alt akış
    zorunluluğu bu yüzdendir.
    """
    from sim2.cekirdek.rng import Akislar
    a = Akislar(99)
    b = Akislar(99)
    a["trafik_zamani"].random()          # bir kol fazladan çekiyor
    assert a["trafik_zamani"].random() != b["trafik_zamani"].random(), (
        "🔴 aynı akıştan fazladan çekim diziyi kaydırmalı — kaydırmıyorsa "
        "akış durumsuzdur ve `HASH_ALANLARI`na ait demektir")


def test_HENUZ_KULLANILMAYAN_dogru_ve_BAYATLAMIYOR():
    """Bir akış ya fiilen çekim alır ya `HENUZ_KULLANILMAYAN`da yazar.

    `Konfig.HENUZ_OKUNMAYAN` ile aynı sözleşme, RNG'deki karşılığı.
    """
    import sim2.cekirdek.rng as R
    kullanilan: set[str] = set()
    for yol in _sim2_dosyalari(haric={"rng.py"}):
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        for n in ast.walk(agac):
            if isinstance(n, ast.Constant) and isinstance(n.value, str) \
                    and n.value in R.AKIS_ADLARI:
                kullanilan.add(n.value)
    sahipsiz = sorted(set(R.AKIS_ADLARI) - kullanilan
                      - set(R.HENUZ_KULLANILMAYAN))
    assert not sahipsiz, (
        f"🔴 bu akışlar hiçbir modülde çekim almıyor ve "
        f"`HENUZ_KULLANILMAYAN`da da yazmıyorlar: {sahipsiz}")
    bayat = sorted(set(R.HENUZ_KULLANILMAYAN) & kullanilan)
    assert not bayat, (
        f"🔴 artık çekim alıyor ama hâlâ `HENUZ_KULLANILMAYAN`da: {bayat}")
    hayalet = sorted(set(R.HENUZ_KULLANILMAYAN) - set(R.AKIS_ADLARI))
    assert not hayalet, f"🔴 var olmayan akış bildirilmiş: {hayalet}"


# ==========================================================================
# 🔴 PARAMETRE KÖKENLERİ — gerekçesiz sayı depoya giremesin
#
# 8 Eylül 2026'da ölçüldü: davranış belirleyen parametrelerin çoğunun DEĞERİ
# gerekçesizdi. Kova sistemi borcu ödemez, GÖRÜNÜR ve SAYILABİLİR kılar.
# Aşağıdaki testler mekanizmayı kilitler; bir kayıt defterinin testi yoksa
# o defter çürür.
# ==========================================================================

def test_HER_Konfig_alaninin_KOKENI_yazili():
    """🔒 Kapsama `konfig.py`de içe aktarma anında da denetleniyor; burada
    ikinci kez, çünkü o denetim sessizce kaldırılabilir."""
    adlar = tuple(f.name for f in dataclasses.fields(Konfig))
    eksik, olu = eksik_alanlar(adlar)
    assert not eksik, f"🔴 kökeni yazılmamış alan: {eksik}"
    assert not olu, f"🔴 artık var olmayan alan için köken kaydı: {olu}"


def test_KOVA_kumesi_KAPALI():
    """Sekizinci bir kova yoktur. Yeni kova, ölçütü gevşetmenin en kolay yolu.

    ⚠️ Küme 8 Eylül 2026'da BÜYÜDÜ (K-104) ve iki eklemenin de sebebi var:
    `DUYARSIZ` şartnamede (§11.1) vardı ama kodda YOKTU — Faz 1 duyarlılık
    denetiminin çıktısını yazacak yer yoktu. `KOL_TANIMI` ise `TEDAVI`nin
    içindeki ikinci anlamı ayırdı; gerekçesi `kokenler.py` başlığında.
    """
    assert set(KOVALAR) == {"TURETILMIS", "OLCULMUS", "KAYNAK", "DUYARSIZ",
                            "TEDAVI", "KOL_TANIMI", "SINANMAMIS"}
    for kova, _ in KOKENLER.values():
        assert kova in KOVALAR
    for kova, _ in MODUL_KOKENLERI.values():
        assert kova in KOVALAR


def test_TEDAVI_kovasi_TEDAVI_ALANLARI_ile_AYNI():
    """🔴 "Tedavi" sözcüğünün TEK bir anlamı olmalı — K-104.

    `kosum/sonuc.py::TEDAVI_ALANLARI`, iki kolun meşru olarak ayrılabileceği
    alanları sayar ve `kurulum_hash` tam olarak onları dışarıda bırakır.
    Köken defterinin `TEDAVI` kovası ise ayrı bir liste tutuyordu ve altı
    alan fazladan içindeydi — yani `kurulum_hash`in İÇİNDE olan sabitler
    "tedavi değişkeni" diye etiketlenmişti. İki liste sessizce ayrışıyordu.

    🔒 Bu test onları BİRBİRİNE BAĞLAR: ayrışma artık kırmızı test demektir.
    """
    from sim2.kosum.sonuc import TEDAVI_ALANLARI
    kovadaki = {ad for ad, (kova, _) in KOKENLER.items() if kova == "TEDAVI"}
    assert kovadaki == set(TEDAVI_ALANLARI), (
        "🔴 'TEDAVI' iki farklı şey anlamına geliyor: "
        f"köken defteri {sorted(kovadaki)}, "
        f"kurulum_hash {sorted(TEDAVI_ALANLARI)}")


def test_DUYARLILIK_BORCU_KOL_TANIMI_icinde():
    """Duyarlılık borcu, var olmayan bir parametreyi işaret edemez.

    🔒 Borç düzyazıda değil sayaçta durur; ama sayaç yanlış bir adı
    sayarsa, borç ödenmiş görünürken ödenmemiş olur — 8 Eylül 2026'da
    ölçümsüz bir borç düşüşü (50 → 46) tam olarak böyle olmuştu.
    """
    kol_tanimi = {ad for ad, (kova, _) in KOKENLER.items()
                  if kova == "KOL_TANIMI"}
    assert DUYARLILIK_BEKLEYEN <= kol_tanimi, (
        "🔴 duyarlılık borcunda `KOL_TANIMI` kovasında olmayan ad var: "
        f"{sorted(DUYARLILIK_BEKLEYEN - kol_tanimi)}")
    assert set(duyarlilik_borcu()) == DUYARLILIK_BEKLEYEN


def test_HER_KOKENIN_GEREKCESI_VAR():
    """Boş bir gerekçe, gerekçe yokluğunun gizlenmiş hâlidir."""
    bos = [ad for ad, (_, gerekce) in KOKENLER.items()
           if len(gerekce.strip()) < 10]
    bos += [ad for ad, (_, gerekce) in MODUL_KOKENLERI.items()
            if len(gerekce.strip()) < 10]
    assert not bos, f"🔴 gerekçesi boş ya da anlamsız kısa: {bos}"


def test_OLCULMUS_kova_URETICI_gostermek_zorunda():
    """🔒 `ÖLÇÜLMÜŞ` demek 'bir betik üretti' demektir. Betik adı yoksa
    iddia doğrulanamaz ve kova bir etiketten ibaret kalır."""
    kusurlu = [ad for ad, (kova, gerekce) in
               {**KOKENLER, **MODUL_KOKENLERI}.items()
               if kova == "OLCULMUS" and "kalibrasyon/" not in gerekce]
    assert not kusurlu, (
        f"🔴 ÖLÇÜLMÜŞ ama üretici betiği yazılmamış: {kusurlu}")


def test_KOKENI_YAZILMAYAN_alan_KONFIGI_PATLATIR():
    """🔴 Mekanizmanın kendisi sınanır: kayıt defterinden bir alan
    çıkarıldığında kapsama denetimi bunu YAKALAMALI."""
    adlar = tuple(f.name for f in dataclasses.fields(Konfig))
    eksik, _ = eksik_alanlar(tuple(a for a in adlar) + ("uydurma_alan",))
    assert eksik == ("uydurma_alan",), (
        "🔴 kapsama denetimi kayıtsız bir alanı yakalamıyor")


def test_SINANMAMIS_sayisi_RAPORLANIYOR():
    """⚠️ Bu test SINANMAMIS'ı yasaklamaz — bugün 51 tane var ve bu bilinen
    bir borç. Yasakladığı şey borcun GÖRÜNMEZ olmasıdır: sayım her koşunun
    sonuç satırına yazılır.

    🔒 Ön-kayıt mühürlenmeden önce bu sayı sıfırlanmalıdır; o gün geldiğinde
    bu testin iddiası `== 0`a çevrilecektir.
    """
    sayim = kova_sayimi()
    assert set(sayim) == set(KOVALAR)
    assert sum(sayim.values()) == len(KOKENLER) + len(MODUL_KOKENLERI)
    assert sayim["SINANMAMIS"] >= 0


# ==========================================================================
# Y7 · Θ — MOBİLİTE KOLU BAŞINA, İKİ PAYDAYLA (`v2/07` §03.3 · §18 Y7)
# ==========================================================================

def test_Y7_THETA_tablosu_KOLLARLA_ayni_ve_IKI_PAYDA_tutarli():
    """🔒 Her kolun Θ'sı var; Θ_AODV = Θ_OLSR × 5 (paydalar 15 s ve 3 s)."""
    from sim2.yapilandirma.senaryolar import MOBILITE_THETA
    assert set(MOBILITE_THETA) == set(MOBILITE_KOLLARI)
    for kol, (olsr, aodv, kopmayan) in MOBILITE_THETA.items():
        assert 0.0 <= kopmayan <= 1.0, kol
        assert (olsr is None) == (aodv is None), kol
        if olsr is None:
            # Θ yalnız HİÇ kopma olmayan kolda tanımsız olabilir.
            assert kopmayan == 1.0, kol
            continue
        assert aodv == pytest.approx(olsr * 5.0, rel=5e-3), kol


def test_Y7_kapsam_THETAYI_ve_TEMSIL_ORANINI_yaziyor():
    from sim2.yapilandirma.kapsam import kapsam_bolumu
    from sim2.yapilandirma.senaryolar import MOBILITE_THETA
    for kol in MOBILITE_KOLLARI:
        k = Konfig(kol="t", senaryo=f"{kol}-yok")
        b = kapsam_bolumu(k)
        olsr, aodv, kopmayan = MOBILITE_THETA[kol]
        assert b["theta_olsr"] == olsr
        assert b["theta_aodv"] == aodv
        assert b["theta_kopmayan_oran"] == kopmayan


def test_Y7_formasyonun_THETASI_ASAGI_YANLI_oldugunu_SATIRDA_soyluyor():
    """🔴 Formasyonun Θ_OLSR'ı kapının (3) ALTINDA görünür — ama çiftlerin
    %92'si hiç kopmuyor, yani ölçüme yalnız eşiğin kıyısındakiler giriyor.
    Sayı ile uyarısı AYNI satırda dolaşmak zorunda; kapı bunu bağlar."""
    from sim2.yapilandirma.kapsam import kapsam_bolumu
    from sim2.yapilandirma.senaryolar import MOBILITE_THETA
    olsr, _aodv, kopmayan = MOBILITE_THETA["formasyon"]
    assert olsr < 3.0 and kopmayan > 0.9
    b = kapsam_bolumu(Konfig(kol="t", senaryo="formasyon-yok"))
    assert b["theta_olsr"] < 3.0 and b["theta_kopmayan_oran"] > 0.9
    # Karşılaştırma: kopma bol olan kolda oran düşük ve Θ kapının üstünde.
    bagimsiz_olsr, _a, bagimsiz_kopmayan = MOBILITE_THETA["bagimsiz"]
    assert bagimsiz_olsr >= 3.0 and bagimsiz_kopmayan < 0.5

# ==========================================================================
# AĞ BÖLÜNMESİ — B6 (`04` K-132)
# ==========================================================================
def test_bolunme_payi_OLCULMEDI_ile_SIFIRI_ayiriyor():
    """🔒 `None ≠ 0` — kalibrasyon tohumu sessizce "temiz" okunmamalı.

    Tablo yalnız ana deney tohumları (2000–2039) için ölçüldü. Ölçülmemiş bir
    tohumda `0.0` dönseydi, kalibrasyon koşuları *"ağ hiç bölünmedi"* diye
    okunur ve ölçülmemiş bir şey ölçülmüş gibi sunulurdu (`03` §2 ilke 1).
    """
    from sim2.yapilandirma.senaryolar import bolunme_payi
    assert bolunme_payi("formasyon", 1000) is None, "ölçülmedi → None"
    assert bolunme_payi("formasyon", 2000) == 0.0, "ölçüldü, bölünme yok → 0.0"
    assert bolunme_payi("formasyon", 2011) > 0.0, "ölçüldü, bölünme VAR"


def test_bolunme_STATIK_kolda_sifir_HAREKETLIDE_var():
    """🔴 Boş geçmeyen kapı — ölçüm gerçekten bir şey bulmuş olmalı.

    Statik kol bir KONTROLDÜR: konumlar değişmediği için bölünme doğamaz ve
    orada sıfırdan farklı bir sayı ölçümün bozuk olduğunu gösterirdi.
    Hareketli kollarda ise sıfır çıkması, ölçümün hiçbir şey görmediği
    anlamına gelirdi — ve o zaman bu tablo bir yokluğu belgelerdi.
    """
    from sim2.yapilandirma.senaryolar import MOBILITE_BOLUNME
    assert MOBILITE_BOLUNME["statik"] == {}, "statik kolda bölünme OLAMAZ"
    hareketli = sum(len(MOBILITE_BOLUNME[k])
                    for k in ("bagimsiz", "gorev", "formasyon"))
    assert hareketli > 0, "hareketli kollarda hiç bölünme yok — tablo BOŞ"
    assert all(0.0 < p <= 1.0
               for k in MOBILITE_BOLUNME for p in MOBILITE_BOLUNME[k].values())


def test_bolunme_payi_SONUC_SATIRINA_giriyor():
    """Satır kendi sınırını taşımalı: ay sonra açılan bir satır, o tohumda
    ağın bölünmüş olduğunu KENDİSİ söylemeli."""
    from sim2.yapilandirma.kapsam import kapsam_bolumu
    bolunmus = kapsam_bolumu(
        Konfig(kol="t", senaryo="formasyon-yok", tohum=2011))
    temiz = kapsam_bolumu(
        Konfig(kol="t", senaryo="formasyon-yok", tohum=2000))
    olculmemis = kapsam_bolumu(
        Konfig(kol="t", senaryo="formasyon-yok", tohum=1000))
    assert bolunmus["bolunme_payi"] > 0.0
    assert temiz["bolunme_payi"] == 0.0
    assert olculmemis["bolunme_payi"] is None
