"""
ADIM 4 — `kanal/karistirici.py`: beş sınıf.

🔴 İKİSİ MİMARİYİ DEĞİŞTİRİYOR ve bu dosya ikisini de bağlıyor:
  · **reaktif** ortamdan besleniyor — zamanın saf fonksiyonu DEĞİL
  · **aldatıcı** CSMA'ya görünüyor — eski *"karıştırıcı CSMA'yı tetiklemez"*
    beyanı bu sınıf için kalkıyor
"""

from __future__ import annotations

import math
import pathlib
import statistics as ist
import sys

import pytest

KOK = pathlib.Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.cekirdek.degismezler import DegismezHatasi  # noqa: E402
from sim2.cekirdek.rng import Akislar  # noqa: E402
from sim2.dunya.topoloji import topoloji_kur  # noqa: E402
from sim2.kanal.cerceve import cerceve_kur  # noqa: E402
from sim2.kanal.girisim import Iletim  # noqa: E402
from sim2.kanal.kanal import Kanal  # noqa: E402
from sim2.yapilandirma import senaryolar  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402

GUC_DBM = 5.0          # ölçülmemiş; testler için açıkça verilen çalışma gücü


def _kanal(sinif: str, guc_dbm: float = GUC_DBM, **ek) -> Kanal:
    k = Konfig(kol="t", senaryo=f"statik-{sinif}",
               karistirici_guc_override_dbm=guc_dbm, **ek)
    return Kanal(k, topoloji_kur(k, Akislar(1)))


def _devrede_an(k: Konfig, gecikme_s: float = 10.0) -> float:
    """🔒 Karıştırıcının GERÇEKTEN devrede olduğu bir an — konfigden türer.

    🔴 NEDEN VAR: `karistirici_baslangic_s` eklendiğinde (150 s) güç yolundan
    geçen testler t≈0'da ölçüyordu ve karıştırıcı orada KAPALI. Üçü kırıldı,
    ikisi ise BOŞ YERE YEŞİL kaldı — biri kayan nokta gürültüsüyle (bağıl
    fark 3,1e-16), biri de "meşgul etmiyor" diye kapalı bir karıştırıcıyı
    doğrulayarak. Sabiti elle yazmak aynı çürümeyi tekrar üretirdi.
    """
    return k.karistirici_baslangic_s + gecikme_s


# 🔴 EŞİK DEĞİL, İKİ FİZİKSEL İDDİA — 8 Eylül 2026 denetimi
# ==========================================================
# Burada `ANLAMLI_PER_ARTISI = 1e-6` duruyordu ve iki kusuru vardı:
#   1. Bir FARK eşiğiydi. *"Neden 1e-6"* sorusunun cevabı yoktu; köken
#      defteri de test sabitlerini kapsamıyor, yani hiçbir yerde yoktu.
#   2. Yanındaki *"kirli 1,0 · temiz ~1e-64"* ölçümünün ÜRETİCİSİ yoktu.
#
# 🔒 ÖLÇÜLDÜ (25 dBm karıştırıcı · gölgeleme ve sönümleme kapalı · ilk komşu
# çifti · `karistirici_baslangic_s + 10 s`; dört sınıfın DÖRDÜ de aynı):
#     temiz PER = 1,076e−64        karıştırılmış PER = 1,000000
#
# Ayrım **64 ondalık mertebe**. Yani (1e−63; 1) aralığındaki HER eşik aynı
# kararı verir — seçilecek bir sayı yok, kurulacak bir BRAKET var.
#
# 🔒 Bu yüzden tek bir fark eşiği yerine İKİ MUTLAK İDDİA sınanır:
#     · temiz bağ çerçeveyi teslim EDER          → PER < TEMIZ_TAVANI
#     · karıştırılmış bağ çerçeveyi teslim ETMEZ → PER > KIRLI_TABANI
# İkisi de fiziksel cümledir ve ölçülen ayrımın çok içindedir: 1e−3, ölçülen
# temizin 10^61 katı; 0,5 ise ölçülen kirlinin yarısı. Bir ULP farkı ikinci
# iddiayı asla geçemez, çünkü iddia FARKA değil DEĞERE bakıyor.
#
# Üretici: `python -m pytest tests2/test_karistirici.py -q`
TEMIZ_TAVANI = 1e-3      # "temiz bağ çalışıyor"      — ölçülen 1,1e−64
KIRLI_TABANI = 0.5       # "karıştırılmış bağ çökmüş" — ölçülen 1,000


# ==========================================================================
# KURULUM ve GÜÇ KAPISI
# ==========================================================================

def test_bes_sinifin_besi_de_KURULUYOR():
    beklenen = {"surekli": "Surekli", "reaktif": "Reaktif",
                "aldatici": "Aldatici", "taramali": "Taramali"}
    for sinif, ad in beklenen.items():
        assert type(_kanal(sinif).karistirici).__name__ == ad
    assert senaryolar.UYGULANMAMIS_KARISTIRICI == frozenset()


def test_karistiricisiz_kolda_None():
    k = Konfig(kol="t", senaryo="statik-yok")
    assert Kanal(k, topoloji_kur(k, Akislar(1))).karistirici is None


def test_OLCULMEMIS_GUCLE_kosmak_REDDEDILIYOR(monkeypatch):
    """🔒 Kapı kalkmadı, İKİ KEZ YER DEĞİŞTİRDİ.

    Önce "uygulanmamış sınıf" kapısıydı; beş sınıf uygulanınca tetiklenemez
    oldu. Yerini "ölçülmemiş güç" kapısı aldı. 8 Eylül 2026'da güçler ÖLÇÜLDÜ
    ve tablo doldu — kapı yine tetiklenemez hâle geldi ama KALKMADI: yeni bir
    sınıf eklenip gücü ölçülmezse koşum durmalı. Test artık o durumu KURUYOR,
    çünkü tablonun boş olmasına dayanan eski hâli tabloyla birlikte bayatladı.
    """
    monkeypatch.setitem(senaryolar.KARISTIRICI_GUCU_DBM, "surekli", None)
    k = Konfig(kol="t", senaryo="statik-surekli")
    assert k.karistirici_guc_dbm is None
    with pytest.raises(DegismezHatasi):
        Kanal(k, topoloji_kur(k, Akislar(1)))


def test_karistirici_BASLANGICTAN_ONCE_susuyor():
    """🔴 `karistirici_baslangic_s` kapısı — kendisi test edilmeliydi.

    Bu kapı eklendiğinde güç yolundan geçen üç testi kırdı, ikisini de boş
    yere yeşil bıraktı. Kapının KENDİSİ test edilmiş olsaydı, etkisi
    başkalarının içinde sessizce keşfedilmezdi.
    """
    kanal = _kanal("surekli", guc_dbm=25.0)
    bas = kanal.konfig.karistirici_baslangic_s
    j = kanal.karistirici
    assert not j.devrede_mi(bas - 1e-6), "başlangıçtan önce susmalı"
    assert j.devrede_mi(bas + 1e-6), "başlangıçtan sonra devrede olmalı"
    # Güç yolunda da sıfır olmalı — `devrede_mi` yalnız bir bayrak değil.
    konum = kanal.topoloji.konum(0, bas - 1e-6)
    assert j.alinan_guc_w(0, konum, bas - 1e-6) == 0.0
    assert j.alinan_guc_w(0, kanal.topoloji.konum(0, bas + 1e-6),
                          bas + 1e-6) > 0.0


def test_karistirici_SENARYODAN_geliyor():
    """Elle verilebilseydi aynı etiketli iki koşu farklı karıştırıcı taşırdı."""
    import inspect
    assert "karistirici" not in inspect.signature(Kanal.__init__).parameters


# ==========================================================================
# SÜREKLİ ve DARBELİ
# ==========================================================================

def test_surekli_HER_AN_acik_ve_CSMAya_gorunmez():
    j = _kanal("surekli").karistirici
    assert all(j.acik_mi(t) for t in (0.0, 0.317, 12.5, 349.9))
    assert not any(j.csma_ya_gorunur(t) for t in (0.0, 1.0, 12.5))
    assert j.gecis_anlari(0.0, 10.0) == ()


def test_darbeli_ORTALAMA_gucu_surekliyle_esitliyor(monkeypatch):
    """🔒 `surekli_darbeli`nin sorduğu soru: *aynı ORTALAMA güçte darbeli
    olmak fark eder mi?* Tepe telafisi görev çevriminden TÜRETİLİR.

    ⚠️ Güç tablosu ölçülmediği için burada geçici olarak doldurulur; darbeli
    senaryo override kabul etmez (override nihai güçtür ve telafiyi atlar).
    """
    monkeypatch.setitem(senaryolar.KARISTIRICI_GUCU_DBM, "surekli", 5.0)
    monkeypatch.setitem(senaryolar.KARISTIRICI_GUCU_DBM,
                        "surekli_darbeli", 5.0)
    k_sur = Konfig(kol="t", senaryo="statik-surekli")
    k_dar = Konfig(kol="t", senaryo="statik-surekli_darbeli")
    assert k_dar.karistirici_guc_dbm == pytest.approx(
        5.0 + 10.0 * math.log10(1.0 / k_dar.darbe_gorev_cevrimi))

    sur = Kanal(k_sur, topoloji_kur(k_sur, Akislar(1))).karistirici
    dar = Kanal(k_dar, topoloji_kur(k_dar, Akislar(1))).karistirici
    konum = sur.topoloji.konum(0, 0.0)
    ornek = [dar.alinan_guc_w(0, konum, 0.0011 * n) for n in range(20000)]
    ort_darbeli = ist.mean(ornek)
    surekli_guc = sur.alinan_guc_w(0, konum, 0.0)
    assert ort_darbeli == pytest.approx(surekli_guc, rel=0.03)


def test_darbeli_gorev_cevrimi_ve_GECIS_ANLARI():
    import unittest.mock as mock
    with mock.patch.dict(senaryolar.KARISTIRICI_GUCU_DBM,
                         {"surekli_darbeli": 5.0}):
        k = Konfig(kol="t", senaryo="statik-surekli_darbeli")
        j = Kanal(k, topoloji_kur(k, Akislar(1))).karistirici
        acik = sum(j.acik_mi(0.0007 * n) for n in range(30000))
        assert acik / 30000 == pytest.approx(k.darbe_gorev_cevrimi, abs=0.02)
        anlar = j.gecis_anlari(0.0, 3.0 * k.darbe_periyodu_s)
        assert len(anlar) >= 5
        assert list(anlar) == sorted(anlar)


# ==========================================================================
# 🔴 REAKTİF — ortama tepki verir
# ==========================================================================

def test_reaktif_BOS_ORTAMDA_susuyor():
    kanal = _kanal("reaktif")
    assert kanal.ortam.bos_mu()
    assert not kanal.karistirici.acik_mi(10.0)


def test_reaktif_ILETIM_BASLAYINCA_patliyor_ve_YENIDEN_SILAHLANIYOR():
    """🔴 Bu testin şekli bir TASARIM HATASINDAN geliyor.

    İlk yazımda karıştırıcı iletim başına BİR kez patlıyordu. Zamanlama
    hesaplandı: sezme 16 µs + patlama 144 µs = 160 µs, ama önbelge 192 µs —
    yani patlama, tepki verdiği çerçevenin GÖVDESİNE HİÇ DEĞMİYORDU
    (kapsanan gövde payı %0,0). Gerçek bir reaktif karıştırıcı kanalı sürekli
    dinler; enerji sürdükçe sezer, patlar, yeniden sezer. Yeni hâlde kapsanan
    gövde payı **%90,6**.
    """
    kanal = _kanal("reaktif")
    k = kanal.konfig
    c = cerceve_kur(k, "veri")
    bas = 10.0
    kanal.ortam.ekle(Iletim(gonderen=0, cerceve=c, baslangic_s=bas,
                            guc_w=kanal.yayilim.verici_gucu_w))
    j = kanal.karistirici
    cevrim = k.reaktif_sezme_s + k.reaktif_patlama_s
    assert not j.acik_mi(bas - 1e-6), "iletimden ÖNCE susmalı"
    assert not j.acik_mi(bas + 0.5 * k.reaktif_sezme_s), "sezme süresi dolmadan"
    assert j.acik_mi(bas + k.reaktif_sezme_s + 1e-9), "sezmeden sonra patlamalı"
    # ikinci çevrim: yeniden sezme boşluğu, sonra yeniden patlama
    assert not j.acik_mi(bas + cevrim + 0.5 * k.reaktif_sezme_s)
    assert j.acik_mi(bas + cevrim + k.reaktif_sezme_s + 1e-9)
    # iletim bitince susar
    assert not j.acik_mi(bas + c.sure_s + 1e-6)

    # 🔒 GÖVDE KAPSAMA — sayının kendisi
    govde_bas, _ = c.govde_araligi(bas)
    n = 2000
    kapsanan = sum(j.acik_mi(govde_bas + c.govde_suresi_s * i / n)
                   for i in range(n)) / n
    assert kapsanan > 0.85, (
        f"🔴 reaktif karıştırıcı gövdenin yalnız %{100*kapsanan:.1f}'ini "
        f"kapsıyor; tek atışlık tasarımda bu %0,0 idi")


def test_reaktif_gecis_anlari_PARCA_SINIRINA_giriyor():
    """Patlama çerçevenin ortasında başlıyorsa SINR sıçraması parçalanmalı;
    yoksa reaktif karıştırıcı sürekli olanın zayıf kopyası gibi ölçülür."""
    kanal = _kanal("reaktif")
    c = cerceve_kur(kanal.konfig, "veri")
    kanal.ortam.ekle(Iletim(gonderen=0, cerceve=c, baslangic_s=10.0003,
                            guc_w=kanal.yayilim.verici_gucu_w))
    sinirlar = kanal.girisim.parca_sinirlari(10.0, c.sure_s)
    sezme = 10.0003 + kanal.konfig.reaktif_sezme_s
    assert any(abs(s - sezme) < 1e-12 for s in sinirlar)


def test_reaktif_sezme_HASH_tabanli_ve_belirlenimci():
    """🔒 Sıralı akış olsaydı, çok iletim yapan protokol akışı kaydırır ve
    karıştırıcı kollar arasında farklı davranırdı."""
    kanal = _kanal("reaktif")
    c = cerceve_kur(kanal.konfig, "veri")
    kanal.ortam.ekle(Iletim(gonderen=7, cerceve=c, baslangic_s=20.0,
                            guc_w=kanal.yayilim.verici_gucu_w))
    j = kanal.karistirici
    ilk = [j.acik_mi(20.0 + 1e-5 * n) for n in range(60)]
    # araya bir sürü başka sorgu sıkıştır — durumlu olsaydı ayrışırdı
    for n in range(500):
        j.acik_mi(100.0 + 0.001 * n)
    assert [j.acik_mi(20.0 + 1e-5 * n) for n in range(60)] == ilk


# ==========================================================================
# 🔴 ALDATICI — CSMA'ya görünür
# ==========================================================================

def test_aldatici_CSMAya_GORUNUYOR():
    """🔴 Eski *"karıştırıcı CSMA'yı tetiklemez"* beyanı bu sınıf için kalkar."""
    j = _kanal("aldatici").karistirici
    gorunur = [t for t in (0.0001 * n for n in range(3000))
               if j.csma_ya_gorunur(t)]
    assert gorunur, "aldatıcı hiç görünmüyor"
    assert all(j.acik_mi(t) for t in gorunur), "görünürken açık da olmalı"


def test_aldatici_TASIYICI_DINLEMEYI_mesgul_ediyor():
    kanal = _kanal("aldatici", guc_dbm=20.0)
    assert kanal.ortam.bos_mu()
    bas = _devrede_an(kanal.konfig)
    assert kanal.karistirici.devrede_mi(bas), "karıştırıcı devrede değil"
    mesgul = [kanal.girisim.kanal_mesgul_mu(0, bas + 0.0001 * n)
              for n in range(400)]
    assert any(mesgul), "🔴 aldatıcı karıştırıcı kanalı meşgul göstermiyor"


def test_surekli_TASIYICI_DINLEMEYI_mesgul_ETMIYOR():
    """Ayrım sınıfa aittir: gürültü karıştırıcısı geçerli önbelge basmaz.

    🔴 BU TEST BOŞ YERE YEŞİLDİ: `karistirici_baslangic_s` eklendikten sonra
    t≈0'da ölçüyordu ve orada karıştırıcı zaten KAPALI — yani "meşgul
    etmiyor" iddiası sınıfı değil, kapalı olmayı doğruluyordu. Bir testin
    geçmesi, doğru sebeple geçtiği anlamına gelmiyor.
    """
    kanal = _kanal("surekli", guc_dbm=20.0)
    bas = _devrede_an(kanal.konfig)
    assert kanal.karistirici.devrede_mi(bas), "karıştırıcı devrede değil"
    assert not any(kanal.girisim.kanal_mesgul_mu(0, bas + 0.0001 * n)
                   for n in range(400))


def test_aldatici_icerik_hash_alanini_KULLANIYOR():
    j = _kanal("aldatici").karistirici
    a = j.sahte_icerik(1.0)
    assert 0.0 <= a < 1.0
    assert j.sahte_icerik(1.0) == a
    assert len({j.sahte_icerik(0.01 * n) for n in range(50)}) > 5


# ==========================================================================
# TARAMALI
# ==========================================================================

def test_taramali_gorev_cevrimi_KONAK_SAYISINA_bolunuyor():
    """🔒 TEPE gücü sürekliyle eşit, ortalaması konak sayısına bölünür.
    Ortalamayı da eşitlemek onu darbelinin kopyası yapardı."""
    kanal = _kanal("taramali")
    j = kanal.karistirici
    n = kanal.konfig.taramali_konak_sayisi
    acik = sum(j.acik_mi(kanal.konfig.taramali_konak_suresi_s * (m + 0.5))
               for m in range(4000))
    assert acik / 4000 == pytest.approx(1.0 / n, abs=0.03)


def test_taramali_konak_boyunca_SABIT():
    kanal = _kanal("taramali")
    j = kanal.karistirici
    konak = kanal.konfig.taramali_konak_suresi_s
    for m in range(20):
        bas = m * konak
        degerler = {j.acik_mi(bas + konak * f) for f in (0.01, 0.5, 0.99)}
        assert len(degerler) == 1, "konak içinde durum değişmemeli"


# ==========================================================================
# UÇTAN UCA — karıştırıcı PER'i yükseltiyor
# ==========================================================================

@pytest.mark.parametrize("sinif", ["surekli", "reaktif", "aldatici", "taramali"])
def test_karistirici_PERi_YUKSELTIYOR(sinif):
    temiz_k = Konfig(kol="t", senaryo="statik-yok", golgeleme_acik=False,
                     sonumleme_acik=False)
    temiz = Kanal(temiz_k, topoloji_kur(temiz_k, Akislar(1)))
    a = temiz.topoloji.anlik(0.0)
    i, j = next((i, ks[0]) for i, ks in enumerate(a.komsular) if ks)
    c = cerceve_kur(temiz_k, "veri")

    kanal = _kanal(sinif, guc_dbm=25.0, golgeleme_acik=False,
                   sonumleme_acik=False)
    # 🔒 Karıştırıcının DEVREDE olduğu bir an; elle yazılmış 10,0 s
    # `karistirici_baslangic_s` eklendiğinde testi sessizce boşaltmıştı.
    bas = _devrede_an(kanal.konfig)
    if sinif == "taramali":
        # 🔴 Taramalı karıştırıcı konak süresince (100 ms) tek kanaldadır ve
        # çerçeve 2,24 ms'dir: rastgele bir an seçmek çoğu zaman onu BAŞKA
        # kanalda yakalar ve test hiçbir şey ölçmez. Bizim kanalımızda
        # olduğu bir an aranır.
        j_kar = kanal.karistirici
        bas = next(t for t in (bas + 0.05 * n for n in range(400))
                   if j_kar.acik_mi(t) and j_kar.acik_mi(t + c.sure_s))
    if sinif == "reaktif":
        kanal.ortam.ekle(Iletim(gonderen=i, cerceve=c, baslangic_s=bas,
                                guc_w=kanal.yayilim.verici_gucu_w))

    # 🔒 ÖN KOŞUL: karıştırıcı gerçekten devrede mi? Bu satır olmadan test,
    # kapalı bir karıştırıcıyı ölçüp geçmiş sayılabiliyordu.
    assert kanal.karistirici.devrede_mi(bas), "karıştırıcı devrede değil"

    taban = temiz.alim_per(i, j, c, bas_s=bas)
    kirli = kanal.alim_per(i, j, c, bas_s=bas)
    # 🔴 `kirli > taban` YETMEZ: reaktif kolu bir ULP farkıyla (bağıl 3,1e-16)
    # karıştırıcı KAPALIYKEN geçiyordu. İki MUTLAK iddia sınanır; gerekçesi
    # ve ölçülen braket dosya başındaki notta.
    assert taban < TEMIZ_TAVANI, \
        f"temiz bağ zaten çalışmıyor (PER {taban}) — test bir şey ölçemez"
    assert kirli > KIRLI_TABANI, \
        f"{sinif} çerçeveyi çökertmiyor: kirli {kirli} vs temiz {taban}"


def test_karistirici_gecis_anlari_PARCA_SINIRINA_giriyor():
    for sinif in ("aldatici", "taramali"):
        kanal = _kanal(sinif)
        c = cerceve_kur(kanal.konfig, "veri")
        j = kanal.karistirici
        for bas in (10.0, 10.0007, 33.3):
            anlar = j.gecis_anlari(bas, bas + c.sure_s)
            sinirlar = kanal.girisim.parca_sinirlari(bas, c.sure_s)
            for an in anlar:
                assert any(abs(s - an) < 1e-12 for s in sinirlar), (
                    f"{sinif}: geçiş anı {an} parça sınırlarında yok")
