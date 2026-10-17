"""
Evre metrikleri — adım ⑤'in testleri.

🔴 BU TESTLERİN ORTAK SORUSU: metrik, sonucu görmeden tanımlanmış mı?
Sentetik defterlerle çalışırlar; cevabı ÖNCEDEN bilinen dünyalar kurup
metriğin o cevabı verip vermediğine bakarlar. Simülatör koşturmazlar —
koşturan doğrulama `kalibrasyon/evre_metrikleri_kapilari.py`dedir.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.cekirdek.degismezler import DegismezHatasi  # noqa: E402
from sim2.gozlem.karar import Beyan  # noqa: E402
from sim2.olcum.evre import (  # noqa: E402
    ALFA, BANT_SE_KATI, IZGARA_ADIMI_S, PENCERE_S, Evreler,
    _poisson_esigi, evre_sozlugu)
from sim2.olcum.paket_defteri import PaketDefteri  # noqa: E402
from sim2.olcum.rota_olaylari import RotaDefteri  # noqa: E402

BAS, ACILMA, BITIS = 50.0, 150.0, 320.0


def _defter(dogumlar, teslim_kimlikleri=(), bas=BAS, bitis=BITIS):
    """`dogumlar` = [(kimlik, dogum_s)]; teslim edilenler kimlikle verilir."""
    d = PaketDefteri(pencere_bas_s=bas, pencere_bitis_s=bitis)
    for kimlik, t in dogumlar:
        d.dogdu(kimlik, 0, t)
    for kimlik in teslim_kimlikleri:
        d.teslim_edildi(kimlik, dict(dogumlar)[kimlik] + 0.001)
    return d


def _duzgun(hiz_hz=40.0, bas=BAS, bitis=BITIS):
    """Sabit hızda doğan paketler — `(kimlik, dogum_s)` listesi."""
    adim = 1.0 / hiz_hz
    n = int(round((bitis - bas) / adim))
    return [(i, bas + i * adim) for i in range(n)]


# ==========================================================================
# KAFES — iki sabit, ikisi de dışarıdan
# ==========================================================================

def test_kafes_sabitleri_RFC_degerleri():
    """Izgara AODV'nin HELLO_INTERVAL'ı, pencere OLSR'ın TOP_HOLD_TIME'ı.

    🔒 Değerlerin kendisi burada dondurulur ki biri onları 'ayarlamak'
    isterse test kırılsın. Değiştirmek isteyen `08-EVRE-METRIKLERI.md` §02'yi
    değiştirmek zorunda.
    """
    assert IZGARA_ADIMI_S == 1.0        # RFC 3561 · AODV HELLO_INTERVAL
    assert PENCERE_S == 15.0            # RFC 3626 · OLSR TOP_HOLD_TIME
    # 🔒 Y10 — TEK α; band ondan TÜRER (`z(1 − α/2)`), elle yazılmaz.
    assert ALFA == 0.05
    assert BANT_SE_KATI == pytest.approx(1.959964, abs=1e-6)


def test_evreler_BOLUMLEMESI_TAM_bosluk_yok():
    """TEMİZ ∪ ŞOK ∪ TOPARLANMA = ölçüm penceresi, kesişimsiz."""
    e = Evreler(_defter([]), BAS, ACILMA, BITIS)
    sok_bas, sok_bitis = e.sok_araligi
    top_bas, top_bitis = e.toparlanma_araligi
    assert sok_bas == ACILMA
    assert sok_bitis == ACILMA + PENCERE_S == top_bas
    assert top_bitis == BITIS


def test_acilma_ani_PENCERE_DISINDAYSA_patliyor():
    """Açılma anı ölçüm penceresinin dışındaysa evre diye bir şey yoktur."""
    with pytest.raises(DegismezHatasi):
        Evreler(_defter([]), BAS, BITIS + 1.0, BITIS)
    with pytest.raises(DegismezHatasi):
        Evreler(_defter([]), BAS, BAS - 1.0, BITIS)


def test_izgara_OLCUM_SONUNU_asmiyor():
    """Son ızgara anı + pencere ≤ ölçüm sonu. Aksi hâlde kırpılmış bir
    pencerenin PDR'si tam pencerelerle kıyaslanırdı."""
    e = Evreler(_defter([]), BAS, ACILMA, BITIS)
    for t in e.izgara():
        assert t + PENCERE_S <= BITIS
    assert e.izgara()[0] == ACILMA


# ==========================================================================
# PDR — pay ve payda AYNI kümeden
# ==========================================================================

def test_pdr_DOGUM_anina_gore_kovalaniyor():
    """Teslim anı evreden sonraya düşse bile paket DOĞDUĞU evreye yazılır."""
    dogumlar = [(0, 149.9), (1, 150.1)]
    d = PaketDefteri(pencere_bas_s=BAS, pencere_bitis_s=BITIS)
    for k, t in dogumlar:
        d.dogdu(k, 0, t)
    d.teslim_edildi(0, 155.0)      # temizde doğdu, şokta teslim edildi
    d.teslim_edildi(1, 156.0)
    e = Evreler(d, BAS, ACILMA, BITIS)
    assert e.pdr(BAS, ACILMA) == (1.0, 1)
    assert e.pdr(*e.sok_araligi) == (1.0, 1)


def test_BOS_evrede_None_donuyor_SIFIR_degil():
    """🔴 'Ölçülmedi' ile 'sıfır' aynı şey değildir."""
    e = Evreler(_defter([]), BAS, ACILMA, BITIS)
    assert e.pdr(BAS, ACILMA) == (None, 0)
    assert e.sok_derinligi() == (None, None)
    assert e.toparlanma_tamligi() is None
    assert e.toparlanma_suresi() is None


# ==========================================================================
# M1 · ŞOK DERİNLİĞİ
# ==========================================================================

def test_sok_derinligi_BILINEN_dunyada_dogru():
    """Temizde hepsi teslim, şokta yarısı → derinlik tam 0,5."""
    dogumlar = _duzgun()
    teslim = [k for k, t in dogumlar
              if t < ACILMA or t >= ACILMA + PENCERE_S or k % 2 == 0]
    e = Evreler(_defter(dogumlar, teslim), BAS, ACILMA, BITIS)
    derinlik, se = e.sok_derinligi()
    assert derinlik == pytest.approx(0.5, abs=0.02)
    assert 0.0 < se < 0.05


def test_KARISTIRICISIZ_dunyada_sok_derinligi_SIFIR():
    """G1'in sentetik karşılığı: hiçbir şey olmuyorsa metrik susmalı."""
    dogumlar = _duzgun()
    e = Evreler(_defter(dogumlar, [k for k, _ in dogumlar]), BAS, ACILMA,
                BITIS)
    derinlik, se = e.sok_derinligi()
    assert derinlik == 0.0
    assert e.toparlanma_tamligi() == 1.0
    assert e.toparlanma_suresi() == 0.0


# ==========================================================================
# M2 · TOPARLANMA TAMLIĞI
# ==========================================================================

def test_toparlanma_tamligi_BIRDEN_BUYUK_kirpilmiyor():
    """🔒 Kırpmak, bozuk bir ölçümü gizlemek olurdu."""
    dogumlar = _duzgun()
    teslim = [k for k, t in dogumlar
              if t >= ACILMA + PENCERE_S or k % 2 == 0]
    e = Evreler(_defter(dogumlar, teslim), BAS, ACILMA, BITIS)
    assert e.toparlanma_tamligi() > 1.5


# ==========================================================================
# M3 · TOPARLANMA SÜRESİ
# ==========================================================================

def test_toparlanma_suresi_HIC_TOPARLANMAZSA_None():
    """🔴 SANSÜR SAYIYA ÇEVRİLMEZ — yoksa hiç toparlanmayan bir protokol,
    ölçüm penceresinin uzunluğu kadar iyi görünürdü."""
    dogumlar = _duzgun()
    teslim = [k for k, t in dogumlar if t < ACILMA]
    e = Evreler(_defter(dogumlar, teslim), BAS, ACILMA, BITIS)
    assert e.toparlanma_suresi() is None


def test_toparlanma_suresi_BILINEN_ani_buluyor():
    """Karıştırma 150–200 s arası; 200'den sonra tam teslim.

    Pencere 15 s olduğu için band ancak `[t; t+15)` tamamen temizken
    sağlanır: beklenen T_kur = 200 s, yani gecikme 50 s.
    """
    dogumlar = _duzgun()
    teslim = [k for k, t in dogumlar if not (ACILMA <= t < 200.0)]
    e = Evreler(_defter(dogumlar, teslim), BAS, ACILMA, BITIS)
    assert e.toparlanma_suresi() == pytest.approx(50.0, abs=IZGARA_ADIMI_S)


def test_toparlanma_suresi_IZGARA_FAZINA_dayanikli():
    """G3'ün sentetik karşılığı: ızgarayı yarım adım kaydır, karar değişmesin.

    🔒 Bu kapı doğrudan 8 Eylül dersinden geliyor — ρ'nun üç sabit örnekleme
    anı darbe periyoduyla örtüşüyordu ve bu SONRADAN fark edilmişti.
    """
    dogumlar = _duzgun()
    teslim = [k for k, t in dogumlar if not (ACILMA <= t < 200.0)]
    d = _defter(dogumlar, teslim)
    temel = Evreler(d, BAS, ACILMA, BITIS).toparlanma_suresi()
    kaydirilmis = Evreler(d, BAS, ACILMA + 0.5 * IZGARA_ADIMI_S,
                          BITIS).toparlanma_suresi()
    assert abs(temel - kaydirilmis) <= IZGARA_ADIMI_S


# ==========================================================================
# M4 · TESPİT GECİKMESİ
# ==========================================================================

def test_poisson_esigi_kuyruk_orani_TUTUYOR():
    """P(X > k) ≤ alfa olan EN KÜÇÜK k."""
    import math
    # Kuyruk sözleşmesi α'dan bağımsızdır; iki farklı değerde sınanır.
    for alfa in (0.01, ALFA / 170.0):
        for lam in (0.5, 1.0, 3.0, 7.0):
            k = _poisson_esigi(lam, alfa)
            kuyruk = 1.0 - sum(math.exp(-lam) * lam ** i / math.factorial(i)
                               for i in range(k + 1))
            onceki = kuyruk + math.exp(-lam) * lam ** k / math.factorial(k)
            assert kuyruk <= alfa < onceki


def test_SUSAN_protokol_HIZLI_gorunemiyor():
    """🔴 Hiç beyan etmeyen kol `None` alır — sıfır DEĞİL."""
    e = Evreler(_defter(_duzgun()), BAS, ACILMA, BITIS)
    assert e.tespit_gecikmesi(RotaDefteri()) is None


def test_tespit_TEMIZ_EVRE_gurultusunu_eliyor():
    """Sürekli arka plan beyanı varsa, açılmadan sonraki İLK beyan tespit
    SAYILMAZ — boş hipotez o gürültüden kestirilir."""
    r = RotaDefteri()
    # Temiz evrede saniyede ~3 beyan: gürültü tabanı yüksek.
    for i in range(300):
        r.beyan_isle(0, Beyan("kopma", komsu=i % 7), BAS + i / 3.0)
    # Açılmadan hemen sonra AYNI hızda devam — yükselme YOK.
    for i in range(300):
        r.beyan_isle(0, Beyan("kopma", komsu=i % 7), ACILMA + i / 3.0)
    e = Evreler(_defter(_duzgun()), BAS, ACILMA, BITIS)
    assert e.tespit_gecikmesi(r) is None


def test_tespit_GERCEK_yukselmeyi_yakaliyor():
    r = RotaDefteri()
    for i in range(100):                       # temizde saniyede 1 beyan
        r.beyan_isle(0, Beyan("kopma", komsu=i % 7), BAS + i * 1.0)
    for j in range(40):                        # açılmadan 5 s sonra patlama
        r.beyan_isle(0, Beyan("kopma", komsu=j % 7),
                     ACILMA + 5.0 + j * 0.01)
    e = Evreler(_defter(_duzgun()), BAS, ACILMA, BITIS)
    gecikme = e.tespit_gecikmesi(r)
    assert gecikme == pytest.approx(6.0, abs=IZGARA_ADIMI_S)


# ==========================================================================
# SÖZLÜK
# ==========================================================================

def test_evre_sozlugu_TESHISI_SONUCTAN_ayiriyor():
    """`en_dip` bir sonuç değil teşhistir ve pencere sayısıyla birlikte döner.

    🔴 Bir eğrinin minimumu AŞAĞI YANLI bir kestiricidir: pencere sayısı
    arttıkça düşer. Pencere sayısı yanında durmazsa okuyucu bunu bilemez.
    """
    dogumlar = _duzgun()
    teslim = [k for k, t in dogumlar if not (ACILMA <= t < 200.0)]
    s = evre_sozlugu(_defter(dogumlar, teslim), RotaDefteri(),
                     BAS, ACILMA, BITIS, gecikme_p99_s=0.006)
    assert s["en_dip_pencere_sayisi"] > 0
    assert s["en_dip_pdr"] <= s["pdr_sok"]
    # G4: bulanıklık oranı = p99 / ızgara adımı.
    assert s["bulaniklik_orani"] == pytest.approx(0.006 / IZGARA_ADIMI_S)
    assert s["evre_acilma_s"] == ACILMA


def test_evre_sozlugu_ACILMA_verilmezse_metrikler_YOK():
    """⚠️ 'Ölçülmedi' ile 'ölçüldü ve tanımsız' ayrı şeydir."""
    from sim2.olcum.metrikler import metrik_sozlugu
    d = _defter(_duzgun())
    yok = metrik_sozlugu({}, d, RotaDefteri())
    var = metrik_sozlugu({}, d, RotaDefteri(), acilma_s=ACILMA)
    assert "sok_derinligi" not in yok
    assert "evre_metrikleri_yok" not in yok
    assert "sok_derinligi" in var


def test_ACILMA_PENCERE_DISINDAYSA_satir_SEBEBINI_yaziyor():
    """🔴 SESSİZ ATLAMA YOK.

    Karıştırıcı açılmadan biten bir koşuda evreler tanımsızdır — ama bunu
    yazmadan atlamak, 8 Eylül 2026'da üç kalibrasyon tablosunu boşaltan
    hatanın aynısı olurdu: ölçülmemiş bir şey ölçülmüş gibi görünür.
    Satır sebebini KENDİ söyler.
    """
    from sim2.olcum.metrikler import metrik_sozlugu
    d = _defter([(0, 1.0)], bas=0.5, bitis=3.0)
    s = metrik_sozlugu({}, d, RotaDefteri(), acilma_s=150.0)
    assert "sok_derinligi" not in s
    assert "150.0" in s["evre_metrikleri_yok"]


# ==========================================================================
# `ham` BÖLÜMÜ — evre metrikleri SATIRDAN yeniden üretilebiliyor mu?
# ==========================================================================

def test_evre_metrikleri_HAM_BOLUMDEN_yeniden_uretilebiliyor():
    """🔴 `analiz/` KATMANININ DOĞRULAMA KAPISI — bugün burada koşuyor.

    `analiz/` `sim2/`den içe aktarma yapamaz; yüzdeliklerin ve evre
    metriklerinin ikinci bir gerçeklemesi orada olacak. İki gerçeklemenin
    SESSİZCE ayrışmasını engelleyen tek şey, ham listenin sonuç satırında
    bulunmasıdır.

    🔴 Ve 8 Eylül 2026'ya kadar bu MÜMKÜN DEĞİLDİ: `ham` bölümü satıra hiç
    yazılmıyordu, üstelik PAYDA (`dogum_s`) defterde de yoktu — yalnız
    `pencerede_uretilen` SAYISI vardı ve bir sayıdan zaman kovası çıkmaz.

    Bu test, satırdaki `sok_derinligi` ve `toparlanma_tamligi`yi YALNIZ
    `ham` + `kapsam` bölümlerinden yeniden hesaplar.
    """
    from bisect import bisect_left
    import sys as _sys
    _sys.path.insert(0, str(KOK / "tests2"))
    from test_kosum import _kos                       # noqa: E402
    from sim2.kosum.sonuc import sonuc_satiri         # noqa: E402

    kur, kosu = _kos("statik-yok", "enyakin", bitis=6.0,
                     karistirici_baslangic_s=3.0)
    satir = sonuc_satiri(kur, kosu.dugumler, "en_yakin_kimlik")

    ham, kapsam, m = satir["ham"], satir["kapsam"], satir["metrikler"]
    bas, bitis = kapsam["olcum_penceresi_s"]
    acilma = kapsam["karistirici_baslangic_s"]
    pencere = m["evre_pencere_s"]

    dogum = sorted(ham["dogum_s"])
    teslim = sorted(ham["teslim_dogum_s"])

    # 🔒 İKİSİ DE KOŞUMUN TAMAMINI kapsıyor; pencere FİLTREYLE elde edilir.
    # Kapsamların ayrışması, pay ile paydanın farklı kümelerden gelmesi
    # demektir — `pdr_pencere`de bir kez düzeltilmiş olan kusur.
    assert set(teslim) <= set(dogum)

    def _pdr(a, b):
        payda = bisect_left(dogum, b) - bisect_left(dogum, a)
        if payda == 0:
            return None
        return (bisect_left(teslim, b) - bisect_left(teslim, a)) / payda

    temiz = _pdr(bas, acilma)
    sok = _pdr(acilma, min(acilma + pencere, bitis))
    top = _pdr(min(acilma + pencere, bitis), bitis)

    assert temiz is not None and sok is not None
    assert m["pdr_temiz"] == pytest.approx(temiz)
    assert m["pdr_sok"] == pytest.approx(sok)
    assert m["sok_derinligi"] == pytest.approx(temiz - sok)
    if top is not None and temiz:
        assert m["toparlanma_tamligi"] == pytest.approx(top / temiz)


def test_kapsam_bolumu_KONFIGDEN_turuyor():
    """🔒 Elle yazılan liste bayatlar; türetilen liste bayatlayamaz.

    Sönümlemesi kapalı bir koşu bunu KENDİ satırında söyler.
    """
    import sys as _sys
    _sys.path.insert(0, str(KOK / "tests2"))
    from test_kosum import _kos                       # noqa: E402
    from sim2.kosum.sonuc import sonuc_satiri         # noqa: E402
    from sim2.yapilandirma.kapsam import MODELLENMEYEN  # noqa: E402

    kur, kosu = _kos("statik-yok", "enyakin", bitis=4.0,
                     sonumleme_acik=False)
    kapsam = sonuc_satiri(kur, kosu.dugumler, "en_yakin_kimlik")["kapsam"]
    assert "sonumleme" in kapsam["bu_kosumda_kapali"]
    assert "karistirici" in kapsam["bu_kosumda_kapali"]
    # Yapısal sınırlar da satırda ve HER BİRİ sonucu hangi yöne çektiğini
    # söylüyor — "ne yok" tek başına okuyucuya bir şey anlatmaz.
    assert set(kapsam["modellenmeyen"]) == {ad for ad, _ in MODELLENMEYEN}
    for ad, yon in kapsam["modellenmeyen"].items():
        assert len(yon) > 20, f"🔴 '{ad}' sınırının yönü yazılmamış"


# ==========================================================================
# Y10 · TEK α — M4'ün eşiği BONFERRONI ile kuruluyor
# ==========================================================================

def test_Y10_M4_esigi_BONFERRONI_ile_kuruluyor():
    """🔒 Eşik pencere BAŞINA `ALFA / taranan pencere`dir (Y10, K-123).

    Sayı örneği (bas 50 · açılma 150 · bitiş 320 · ızgara 1 s): taranan
    pencere 170, pencere başına α = 2,94e-4. Temiz evrede 100 beyan → λ = 1,0
    ve Poisson eşiği **6**. Y10 ÖNCESİ kural (pencere başına sabit 0,01)
    eşiği **4** veriyordu: tek bir pencereye düşen BEŞ beyan eskiden "tespit"
    sayılırdı, bugün sayılmaz. Yedi beyan iki kuralda da tespittir.

    ⚠️ Bu kapı deterministiktir: sentetik yanlış alarm ölçümü ayrı bir alette
    (`python -u kalibrasyon/anlamlilik_sabitleri.py`) ve orada da bir kapıdır.
    """
    taranan = int((BITIS - ACILMA) / IZGARA_ADIMI_S)
    assert taranan == 170
    assert _poisson_esigi(1.0, ALFA / taranan) == 6
    assert _poisson_esigi(1.0, 0.01) == 4          # Y10 öncesi kural

    r = RotaDefteri()
    for i in range(100):                            # temiz evre: λ = 1,0
        r.beyan_isle(0, Beyan("kopma", komsu=i % 7), BAS + i * 1.0 + 0.5)
    for j in range(5):                              # tek pencerede 5 beyan
        r.beyan_isle(1, Beyan("kopma", komsu=j), ACILMA + 10.0 + 0.01 * j)
    e = Evreler(_defter(_duzgun()), BAS, ACILMA, BITIS)
    assert e.tespit_gecikmesi(r) is None, \
        "beş beyan Bonferroni eşiğini AŞMAMALI"

    for j in (5, 6):
        r.beyan_isle(1, Beyan("kopma", komsu=j), ACILMA + 10.0 + 0.01 * j)
    gecikme = e.tespit_gecikmesi(r)
    assert gecikme is not None, "yedi beyan eşiği AŞMALI"
    assert gecikme == pytest.approx(11.0)


# ==========================================================================
# K-196 · HATA PAYI KÜMELENMEYE DAYANIKLI
# ==========================================================================

def test_K196_negatif_binom_esigi_kuyruk_orani_ve_MOMENTLER_tutuyor():
    """P(X > k) ≤ alfa olan EN KÜÇÜK k; dağılım istenen ortalama ve
    varyansı taşıyor. Olasılıklar modüldeki log-gamma yolundan BAĞIMSIZ,
    ardışık oranla (`P(k+1)/P(k) = (k+r)/(k+1)·(1−p)`) kurulur."""
    from sim2.olcum.evre import _negatif_binom_esigi
    for alfa in (0.01, ALFA / 170.0):
        for ort, var in ((0.8, 5.8), (2.0, 6.0), (26.0, 200.0), (0.3, 3.0)):
            r, p = ort * ort / (var - ort), ort / var
            pmf = [p ** r]
            for i in range(4000):
                pmf.append(pmf[-1] * (i + r) / (i + 1) * (1.0 - p))
            ortalama = sum(i * q for i, q in enumerate(pmf))
            varyans = sum((i - ortalama) ** 2 * q for i, q in enumerate(pmf))
            assert ortalama == pytest.approx(ort, rel=1e-6)
            assert varyans == pytest.approx(var, rel=1e-6)
            k = _negatif_binom_esigi(ort, var, alfa)
            kuyruk = 1.0 - sum(pmf[:k + 1])
            assert kuyruk <= alfa < kuyruk + pmf[k]


def test_K196_varyans_ortalamayi_ASMAZSA_esik_POISSON_ile_ayni():
    """🔒 Beyanları bağımsız olan kolda eşik K-196 öncesiyle BİREBİR."""
    from sim2.olcum.evre import _negatif_binom_esigi
    for alfa in (0.01, ALFA / 170.0):
        for lam in (0.0, 0.5, 1.0, 3.0, 7.0):
            for var in (lam, 0.5 * lam, 0.0):
                assert (_negatif_binom_esigi(lam, var, alfa)
                        == _poisson_esigi(lam, alfa))


def test_K196_tespit_KUMELENEN_temiz_gurultusunu_eliyor():
    """Temizde her 10 s'de bir kovaya 8 beyan yığılıyor (ortalama 0,8,
    varyans 5,8). Açılmadan sonra AYNI desen sürüyor — yükselme YOK.

    Poisson(0,8) eşiği 5 olurdu ve ilk yığın "tespit" sayılırdı (K-193'te
    karıştırıcısız OLSR'ın başına gelen tam buydu); negatif binomun eşiği
    31. Gerçek bir sıçrama (tek kovada 60 beyan) yine yakalanır."""
    r = RotaDefteri()
    for t0 in range(int(BAS), int(BITIS), 10):
        for j in range(8):
            r.beyan_isle(0, Beyan("kopma", komsu=j), t0 + 0.5 + 0.01 * j)
    e = Evreler(_defter(_duzgun()), BAS, ACILMA, BITIS)
    assert e.tespit_gecikmesi(r) is None
    for j in range(60):
        r.beyan_isle(1, Beyan("kopma", komsu=j % 7), ACILMA + 20.2 + 0.001 * j)
    assert e.tespit_gecikmesi(r) == pytest.approx(21.0)


def test_K196_toparlanma_KUMELENEN_kayipta_ANINDA_ve_SE_GENISLER():
    """Temizde her 20 s'nin ilk 5 s'i tam kesinti (PDR 0,75; kayıp zamanda
    kümeli). Açılmadan sonra AYNI desen — toparlanma süresi 0 olmalı.

    Yalnız Agresti–Caffo ile band ≈ 0,75 − 1,96·0,02 ≈ 0,71 idi; ilk
    pencere (kesinti 150–155 içinde, PDR 0,667) bandın DIŞINDA kalıyor ve
    metrik karıştırıcısız bir "toparlanma" uyduruyordu. Kümelenmeye dayanıklı
    SE temizin kendi pencere oynaklığını taşır."""
    dogumlar = _duzgun()
    teslim = [k for k, t in dogumlar if (t - BAS) % 20.0 >= 5.0]
    e = Evreler(_defter(dogumlar, teslim), BAS, ACILMA, BITIS)
    temiz, n_t = e.pdr(BAS, ACILMA)
    ilk, n_i = e.pdr(ACILMA, ACILMA + PENCERE_S)
    assert temiz == pytest.approx(0.75) and ilk == pytest.approx(2.0 / 3.0)
    ac = e._se(temiz, n_t, ilk, n_i)
    assert ilk < temiz - BANT_SE_KATI * ac, "kurgu: eski band ilk pencereyi REDDETMELİ"
    assert e._kume_se() > 3.0 * ac
    assert e.toparlanma_suresi() == 0.0
    _, se = e.sok_derinligi()
    assert se == pytest.approx(e._kume_se())


# ==========================================================================
# K-209 · ÇİZELGELİ KARIŞTIRICI (evre metrikleri v2, öğrenci onayı K-207)
# ==========================================================================
CIZELGE = (15.0, 15.0)


def _acik_mi(t: float) -> bool:
    return t >= ACILMA and (t - ACILMA) % 30.0 < 15.0


def test_K209_SUREKLI_karistiricida_SATIR_BIREBIR():
    """Çizelge yoksa yeni alan YOK ve metrikler bugünküyle aynı."""
    dogum = _duzgun()
    d = _defter(dogum, [k for k, _ in dogum])
    s = evre_sozlugu(d, RotaDefteri(), BAS, ACILMA, BITIS)
    assert "evre_cizelge_s" not in s and "pdr_acik" not in s
    assert s["toparlanma_suresi_s"] == 0.0


def test_K209_DONEMLER_kismi_son_sessiz_dahil():
    e = Evreler(_defter(_duzgun()), BAS, ACILMA, BITIS, cizelge=CIZELGE)
    assert e.donemler(True) == ((150.0, 165.0), (180.0, 195.0), (210.0, 225.0),
                                (240.0, 255.0), (270.0, 285.0), (300.0, 315.0))
    assert e.donemler(False)[-1] == (315.0, 320.0)
    assert len(e.donemler(False)) == 6
    assert e.sok_araligi == (150.0, 165.0), "ŞOK = ilk açık dönem"
    kisa = Evreler(_defter(_duzgun()), BAS, ACILMA, BITIS, cizelge=(10.0, 20.0))
    assert kisa.sok_araligi == (150.0, 160.0), "ŞOK açık dönemden taşmaz"


def test_K209_M1_M2_M3_BILINEN_dunyada():
    """Açıkta hiçbir paket geçmez, sessizde hepsi: M1 = 1 · M2 = 1 · M3
    tanımsız (sansürden ayrı alan)."""
    dogum = _duzgun()
    d = _defter(dogum, [k for k, t in dogum if not _acik_mi(t)])
    s = evre_sozlugu(d, RotaDefteri(), BAS, ACILMA, BITIS, cizelge=CIZELGE)
    assert s["sok_derinligi"] == pytest.approx(1.0)
    assert s["toparlanma_tamligi"] == pytest.approx(1.0)
    assert s["pdr_acik"] == 0.0 and s["pdr_sessiz"] == pytest.approx(1.0)
    assert s["toparlanma_suresi_s"] is None
    assert s["toparlanma_suresi_tanimsiz"] == "cizelgeli"
    assert s["en_dip_pdr"] is None
    assert s["evre_cizelge_s"] == [15.0, 15.0]


def test_K209_M4_ILK_ACIK_DONEMLE_sinirli():
    """İkinci açık dönemdeki patlama çizelgede tespit DEĞİL (ilk açılmayı
    kaçırdı); ilk açık dönemdeki patlama yakalanır."""
    def defter(patlama_s):
        r = RotaDefteri()
        for i in range(100):
            r.beyan_isle(0, Beyan("kopma", komsu=i % 7), BAS + i * 1.0)
        for j in range(40):
            r.beyan_isle(0, Beyan("kopma", komsu=j % 7),
                         ACILMA + patlama_s + j * 0.01)
        return r
    e = Evreler(_defter(_duzgun()), BAS, ACILMA, BITIS)
    ec = Evreler(_defter(_duzgun()), BAS, ACILMA, BITIS, cizelge=CIZELGE)
    assert e.tespit_gecikmesi(defter(31.0)) == pytest.approx(32.0, abs=1.0)
    assert ec.tespit_gecikmesi(defter(31.0)) is None
    assert ec.tespit_gecikmesi(defter(5.0)) == pytest.approx(6.0, abs=1.0)


def test_K209_TESHIS_cevrim_profil_sizinti():
    dogum = _duzgun()
    d = _defter(dogum, [k for k, t in dogum if not _acik_mi(t)])
    s = evre_sozlugu(d, RotaDefteri(), BAS, ACILMA, BITIS, cizelge=CIZELGE)
    assert len(s["evre_cevrim_pdr"]) == 6
    assert s["evre_cevrim_pdr"][0] == [0.0, pytest.approx(1.0)]
    assert s["evre_cevrim_pdr"][-1][0] == 0.0
    profil = s["evre_katli_profil"]
    assert len(profil) == 30
    assert all(p == 0.0 for p in profil[:15])
    assert all(p == pytest.approx(1.0) for p in profil[15:])
    assert s["evre_sizinti"] == pytest.approx(0.0, abs=0.01)


def test_K209_CIZELGE_konfigden_TURER():
    """Birincil hücrenin `derin_sizma`sı (15, 15); sürekli aile ve
    karıştırıcısız kol `None`."""
    from sim2.kanal.dunya import referans_2026
    from sim2.kosum.kurulum import kurulum_yap
    from sim2.kosum.sonuc import karistirici_cizelgesi
    ek = {"isinma_s": 10.0, "olcum_bitis_s": 40.0, "kosu_bitis_s": 50.0}
    birincil = kurulum_yap(referans_2026(
        kol="t", senaryo="formasyon-surekli", tohum=1003,
        tehdit_senaryosu="derin_sizma", trafik_deseni="yere_toplama", **ek))
    assert karistirici_cizelgesi(birincil) == (15.0, 15.0)
    # 🔒 TEK TANIM: evre bölümlemesi karıştırıcının kendi `devrede_mi`siyle
    # aynı (kayıp anatomisi o fonksiyonu kullanıyor).
    kar = birincil.kanal.karistirici
    uyeler = getattr(kar, "uyeler", (kar,))
    ac = birincil.konfig.karistirici_baslangic_s
    for i in range(700):
        t = ac + i * 0.1 + 0.05
        beklenen = (t - ac) % 30.0 < 15.0
        assert any(u.devrede_mi(t) for u in uyeler) == beklenen, t
    surekli = kurulum_yap(referans_2026(kol="t", senaryo="statik-surekli",
                                        tohum=1003, **ek))
    assert karistirici_cizelgesi(surekli) is None
    yok = kurulum_yap(referans_2026(kol="t", senaryo="statik-yok",
                                    tohum=1003, **ek))
    assert karistirici_cizelgesi(yok) is None


# ==========================================================================
# K-239 · EVRE METRİKLERİ YORUMLANAMAYAN PROTOKOL KAYDI
# ==========================================================================
def _satir(protokol, tohum, d=0.0, d_se=0.01, senaryo="formasyon-yok",
           sok=0.0, bulaniklik=0.1):
    """Çizelgeli kapının KAYIT satırı (yalnız hükmün okuduğu alanlar)."""
    return {"senaryo": senaryo, "protokol": protokol, "tohum": tohum,
            "sure_s": 1.0, "pdr_temiz": 0.5, "pdr_acik": 0.5,
            "pdr_sessiz": 0.5 + d, "sok": sok, "sok_se": 0.05, "d": d,
            "d_se": d_se, "m2": 1.0, "tespit": None, "beyan_etmiyor": False,
            "p99_s": 15.0 * bulaniklik, "bulaniklik_evre": bulaniklik,
            "sizinti": 0.01}


def test_K239_G1C_KAYIT_dahil_kayitsiz_kalir_olu_kirmizi(monkeypatch):
    """D'si iki tohumda 2 SE dışında kalan protokol kayıtlıysa G1ç geçer,
    kayıtsızsa kalır; kayıtlı protokolün D'si artık içerideyse kayıt ölüdür
    ve kapı kalır."""
    import kalibrasyon.evre_metrikleri_kapilari as E
    monkeypatch.setattr(E, "EVRE_YORUMLANAMAZ", {"x": {"G1c": "olculdu"}})
    temiz = [_satir("a", t) for t in (1003, 1004)]
    disarida = [_satir("x", 1003, d=-0.03), _satir("x", 1004, d=0.04)]
    assert E._g1c_hukum(temiz + disarida)
    kayitsiz = [dict(r, protokol="y") for r in disarida]
    assert not E._g1c_hukum(temiz + kayitsiz)
    olu = [_satir("x", t, d=0.001) for t in (1003, 1004)]
    assert not E._g1c_hukum(temiz + olu)
    assert E._g1c_hukum(temiz)                  # ölçülmeyen kayıt ölü değil


def test_K239_G4C_KAYIT_dahil_kayitsiz_kalir_olu_kirmizi(monkeypatch):
    """`p99 ≥ açık süre` olan protokol kayıtlıysa G4ç geçer, kayıtsızsa
    kalır; kayıtlı protokolün p99'u açık süreden kısaysa kayıt ölüdür."""
    import kalibrasyon.evre_metrikleri_kapilari as E
    monkeypatch.setattr(E, "EVRE_YORUMLANAMAZ", {"x": {"G4c": "olculdu"}})

    def kol(protokol, bulaniklik):
        kahin = protokol == "en_guvenilir_kahin"
        return [_satir(protokol, t, senaryo="formasyon-surekli",
                       sok=0.2 if kahin else 0.0, bulaniklik=bulaniklik)
                for t in (1003, 1004)]
    bos = [_satir("en_guvenilir_kahin", t) for t in (1003, 1004)]
    taban = kol("en_guvenilir_kahin", 0.05) + kol("a", 0.2) + bos
    assert E._g2c_hukum(taban + kol("x", 1.9))
    assert not E._g2c_hukum(taban + kol("y", 1.9))
    assert not E._g2c_hukum(taban + kol("x", 0.5))


def test_DD12_EVRE_YORUMLANAMAZ_KAYDI_KODA_BAGLI(monkeypatch, tmp_path):
    """Her kayıt ölçüldüğü protokol dosyasının özetini taşır ve özet bugünkü
    dosyaya uyar; kod değişirse kayıt uygulanmaz (JARM-3)."""
    import kalibrasyon.evre_metrikleri_kapilari as E
    from sim2.cekirdek.kimlik import dosya_hash
    assert set(E.EVRE_YORUMLANAMAZ) == set(E.EVRE_YORUMLANAMAZ_KOD)
    for p, (dosya, ozet) in E.EVRE_YORUMLANAMAZ_KOD.items():
        assert dosya_hash(E.KOK / "protokoller" / dosya) == ozet, p
    assert "jarmrout" in E._muaf("G1c")
    monkeypatch.setitem(E.EVRE_YORUMLANAMAZ_KOD, "jarmrout",
                        ("jarmrout.py", "0" * 32))
    assert "jarmrout" not in E._muaf("G1c")
    assert "jarmrout" not in E._muaf("G4c")



def test_K249_M4_TEMIZDE_SIFIR_beyanda_TEK_beyan_TESPIT_DEGIL():
    """G1-P (17 Ekim 2026): karıştırıcısız Babel koşu boyunca TEK bir kopma
    beyan ediyordu ve temiz evresi boştu; Poisson(0) eşiği 0 olduğu için o
    tek beyan "tespit" sayılıyordu. Sıfır gözlemin üst sınırıyla
    (−ln α / 100 kova ≈ 0,030 → eşik 2) tek beyan tespit değildir."""
    r = RotaDefteri()
    r.beyan_isle(1, Beyan("kopma", komsu=31), ACILMA + 46.2)
    e = Evreler(_defter(_duzgun()), BAS, ACILMA, BITIS)
    assert e._kova_momentleri(sorted(r.beyan_anlari("kopma"))) == (0.0, 0.0)
    assert e._sifir_gozlem_ust_siniri() == pytest.approx(0.02996, abs=1e-4)
    assert e.tespit_gecikmesi(r) is None


def test_K249_M4_TEMIZDE_SIFIR_beyanda_PATLAMA_yine_TESPIT():
    """Aynı boş temiz evre; açılmadan 10 s sonra bir saniyeye beş beyan →
    eşik 2 aşılır, tespit 11 s. Gerçek bir karıştırma patlaması kaçmaz."""
    r = RotaDefteri()
    for j in range(5):
        r.beyan_isle(0, Beyan("kopma", komsu=j), ACILMA + 10.2 + 0.01 * j)
    e = Evreler(_defter(_duzgun()), BAS, ACILMA, BITIS)
    assert e.tespit_gecikmesi(r) == pytest.approx(11.0)
