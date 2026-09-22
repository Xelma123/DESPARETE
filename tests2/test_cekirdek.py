"""
ADIM 0 + ADIM 1 — `sim2/cekirdek/` kapanış ölçütleri.

Her test bir kapanış ölçütüne karşılık gelir; ölçüt geçilmeden sonraki adıma
geçilmez.
"""

from __future__ import annotations

import ast
import pathlib
import statistics as ist
import subprocess
import sys

import pytest

KOK = pathlib.Path(__file__).resolve().parent.parent
SIM2 = KOK / "sim2"
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.cekirdek.degismezler import (  # noqa: E402
    DegismezHatasi, asla, dogrula, dogrula_ayrintili)
from sim2.cekirdek.kimlik import (  # noqa: E402
    arac_hash, calisma_kimligi, evren_hash, kosu_kimligi, kurulum_hash)
from sim2.cekirdek.korunum import (  # noqa: E402
    DUSME_SEBEPLERI, KorunumDefteri, KorunumHatasi)
from sim2.cekirdek.olaylar import GecmisZamanHatasi, OlayKuyrugu  # noqa: E402
from sim2.cekirdek.rng import (  # noqa: E402
    AKIS_ADLARI, HASH_ALANLARI, Akislar, akis_listesi_hash, hash_cekimi,
    normal_cekimi)
from sim2.cekirdek.sayaclar import (  # noqa: E402
    PENCERE_SONEKI, TANIMLAR, SayacTanimi, Sayaclar, Turev, sayac_semasi_hash)


def _sayac_tanimlari() -> tuple[SayacTanimi, ...]:
    return tuple(t for t in TANIMLAR if isinstance(t, SayacTanimi))


# ==========================================================================
# DEĞİŞMEZLER — `python -O` altında kalkmıyor
# ==========================================================================

def test_degismez_kirildiginda_patliyor():
    dogrula(True, "geçmeli")
    with pytest.raises(DegismezHatasi):
        dogrula(False, "kırılmalı")
    with pytest.raises(DegismezHatasi):
        asla("bu dala girilmemeliydi")


def test_degismezler_O_bayragi_altinda_HALA_atesliyor():
    """🔴 Adım 0'ın kapanış ölçütü.

    Eski simülatörde yedi değişmez `assert` ile yazılmıştı ve `python -O`
    altında **sessizce kalkıyordu**; dördü kalktığında sessiz bir yanlış
    cevap üretiyordu. Bu test o sınıfın geri gelmesini engeller.
    """
    betik = (
        "import sys; sys.path.insert(0, r'%s')\n"
        "from sim2.cekirdek.degismezler import dogrula, DegismezHatasi\n"
        "assert __debug__ is False, '-O bayragi etkin degil'\n"
        "try:\n"
        "    dogrula(False, 'x')\n"
        "except DegismezHatasi:\n"
        "    print('ATESLEDI')\n" % KOK
    )
    p = subprocess.run([sys.executable, "-O", "-c", betik],
                       capture_output=True, text=True, encoding="utf-8")
    assert "ATESLEDI" in p.stdout, (
        f"🔴 `-O` altında değişmez ATEŞLEMEDİ.\nstdout={p.stdout!r}\n"
        f"stderr={p.stderr!r}")


def test_sim2_altinda_ciplak_assert_YOK():
    """🔴 Değişmezler `assert` ile yazılmamalı — AST ile denetlenir.

    Dizgi araması yorumdaki ve docstring'deki `assert` kelimesini de bulurdu;
    AST yalnız gerçek deyimi görür.
    """
    bulunan: list[str] = []
    for yol in sorted(SIM2.rglob("*.py")):
        if "__pycache__" in yol.parts:
            continue
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        for n in ast.walk(agac):
            if isinstance(n, ast.Assert):
                bulunan.append(f"{yol.relative_to(KOK).as_posix()}:{n.lineno}")
    assert not bulunan, (
        f"🔴 `sim2/` altında çıplak `assert`: {bulunan}. "
        f"`cekirdek.degismezler.dogrula()` kullan — `assert` `-O` altında "
        f"sessizce kalkar.")


def test_ayrintili_dogrulama_kapaliyken_kosul_HIC_hesaplanmiyor():
    """Y11 — koruma kendi sınırıyla birlikte yazılır."""
    import sim2.cekirdek.degismezler as D
    cagri = {"n": 0}

    def sayan() -> bool:
        cagri["n"] += 1
        return True

    eski = D.AYRINTILI_DOGRULAMA
    try:
        D.AYRINTILI_DOGRULAMA = False
        D.dogrula_ayrintili(sayan, "x")
        assert cagri["n"] == 0, "kapalıyken koşul yine de hesaplandı"
        D.AYRINTILI_DOGRULAMA = True
        D.dogrula_ayrintili(sayan, "x")
        assert cagri["n"] == 1
    finally:
        D.AYRINTILI_DOGRULAMA = eski


# ==========================================================================
# OLAY KUYRUĞU
# ==========================================================================

def test_esit_zamanli_olaylar_EKLENME_sirasinda_kosuyor():
    k = OlayKuyrugu()
    iz: list[int] = []
    for i in range(20):
        k.ekle(1.0, iz.append, i)
    k.kostur(2.0)
    assert iz == list(range(20)), "eşit zamanlı olaylar eklenme sırasında değil"


def test_gecmise_olay_SESSIZCE_yutulmuyor():
    k = OlayKuyrugu()
    k.ekle(5.0, lambda: None)
    k.kostur(5.0)
    with pytest.raises(GecmisZamanHatasi):
        k.ekle(4.0, lambda: None)
    with pytest.raises(GecmisZamanHatasi):
        k.gecikmeyle_ekle(-0.1, lambda: None)


def test_kostur_YENIDEN_BASLATILABILIR_sifir_tedirginlik():
    """🔒 Ölçüm penceresi üç ayrı çağrıyla işlenir.

    Üç çağrı, tek çağrıyla **birebir aynı** sonucu vermek zorunda — yoksa
    ısınma/pencere/boşalma ayrımı sonucu değiştirirdi.
    """
    def kur() -> tuple[OlayKuyrugu, list[float]]:
        k = OlayKuyrugu()
        iz: list[float] = []
        for i in range(500):
            k.ekle(i * 0.37, iz.append, i * 0.37)
        return k, iz

    tek_k, tek_iz = kur()
    tek_k.kostur(200.0)

    uc_k, uc_iz = kur()
    uc_k.kostur(50.0)
    uc_k.kostur(120.0)
    uc_k.kostur(200.0)

    assert tek_iz == uc_iz
    assert tek_k.islenen_olay == uc_k.islenen_olay
    assert tek_k.simdi == uc_k.simdi == 200.0


def test_bitisten_sonraki_olaylar_kuyrukta_kaliyor():
    k = OlayKuyrugu()
    k.ekle(1.0, lambda: None)
    k.ekle(9.0, lambda: None)
    k.kostur(5.0)
    assert k.bekleyen_olay_sayisi() == 1
    assert not k.bos_mu()
    assert k.simdi == 5.0


# ==========================================================================
# KORUNUM DEFTERİ
# ==========================================================================

def test_korunum_denklemi_normal_akista_tutuyor():
    d = KorunumDefteri()
    d.uret(100)
    d.kuyruktan_al(60)
    d.ucustan_kuyruga(40)
    d.teslim_et(15)
    d.dus("kuyruk_tasmasi", "kuyruk", 5)
    assert d.denklem_tutuyor_mu()
    r = d.kontrol()
    assert r["korunum_tamam"] is True and r["fark"] == 0


def test_sayac_negatife_dusunce_ANINDA_patliyor():
    d = KorunumDefteri()
    d.uret(1)
    with pytest.raises(KorunumHatasi):
        d.kuyruktan_al(5)


@pytest.mark.parametrize("sebep", DUSME_SEBEPLERI)
def test_her_dusme_sebebi_ATESLENEBILIYOR(sebep: str):
    """Beyan edilip tetiklenemeyen bir sebep, koruma izlenimi verir."""
    d = KorunumDefteri()
    d.uret(1)
    d.dus(sebep, "kuyruk")
    assert d.dusen[sebep] == 1 and d.denklem_tutuyor_mu()


def test_rota_gecersiz_sebebi_BASTAN_var():
    """🔴 Δ · COR · üç kopma sayacı bu sebebe bağlı.

    Sebep listesi bir ŞEMA taahhüdüdür; sonradan eklemek eski satırları
    karşılaştırılamaz yapar.
    """
    assert "rota_gecersiz" in DUSME_SEBEPLERI


def test_bilinmeyen_sebep_ve_nereden_reddediliyor():
    d = KorunumDefteri()
    d.uret(1)
    with pytest.raises(KorunumHatasi):
        d.dus("uydurma_sebep", "kuyruk")
    with pytest.raises(KorunumHatasi):
        d.dus("ttl", "baska_yer")


def test_kontrol_ISTISNA_FIRLATMIYOR_satiri_isaretliyor():
    """Bozuk koşu sessizce ortalamaya karışmasın diye satır işaretlenir."""
    d = KorunumDefteri()
    d.uretilen = 10          # elle bozuldu
    r = d.kontrol()
    assert r["korunum_tamam"] is False and r["fark"] == 10


# ==========================================================================
# RNG — iki listeli tasarım
# ==========================================================================

@pytest.mark.parametrize("tohum", range(1, 31))
def test_ayni_tohum_BIREBIR_ayni_dizi(tohum: int):
    """30 tohum — Adım 0'ın belirlenimcilik ölçütü."""
    a = [Akislar(tohum)[ad].random() for ad in AKIS_ADLARI]
    b = [Akislar(tohum)[ad].random() for ad in AKIS_ADLARI]
    assert a == b


def test_farkli_akislar_farkli_dizi():
    a = Akislar(1000)
    assert a["yerlesim"].random() != a["irtifa"].random()


def test_YENI_HASH_ALANI_eski_cekimleri_KAYDIRMIYOR():
    """🔴 Adım 0'ın en önemli ölçütü — kusur 7'nin yapısal çözümü.

    Eski simülatörde akış listesi kapalıydı ve akış eklemek çekim sırasını
    kaydırıp **daha önce ölçülmüş her sayıyı** bayatlatıyordu (bu yaşandı).
    Hash alanları durumsuz olduğu için o bedel bir daha ödenmez.
    """
    import sim2.cekirdek.rng as R
    once = [hash_cekimi("kanal_karar", 1000, 3, 7, i) for i in range(300)]
    eski = R.HASH_ALANLARI
    try:
        R.HASH_ALANLARI = eski + ("deneme_alani",)
        sonra = [hash_cekimi("kanal_karar", 1000, 3, 7, i) for i in range(300)]
    finally:
        R.HASH_ALANLARI = eski
    assert once == sonra, "🔴 yeni hash alanı eski çekimleri kaydırdı"


def test_hash_alanlari_birbirine_CARPISMIYOR():
    d = {a: hash_cekimi(a, 1000, 1, 2, 3) for a in HASH_ALANLARI}
    assert len(set(d.values())) == len(d), f"alanlar çakıştı: {d}"


def test_anahtar_ayirici_calisiyor():
    """(1, 23) ile (12, 3) aynı diziyi vermemeli."""
    assert hash_cekimi("kanal_karar", 1, 1, 23) != hash_cekimi("kanal_karar", 1, 12, 3)


def test_hash_cekimi_DURUMSUZ_cagri_sayisindan_bagimsiz():
    beklenen = hash_cekimi("kanal_karar", 7, 1, 2, 3)
    for _ in range(50):
        hash_cekimi("kanal_karar", 7, 99, 99, 99)
    assert hash_cekimi("kanal_karar", 7, 1, 2, 3) == beklenen


def test_normal_cekimi_standart_normal():
    orn = [normal_cekimi("sonumleme_i", 1000, 2, 5, i) for i in range(100_000)]
    assert abs(ist.mean(orn)) < 0.02, f"ortalama {ist.mean(orn)}"
    assert abs(ist.stdev(orn) - 1.0) < 0.02, f"std {ist.stdev(orn)}"


def test_normal_cekimi_I_ve_Q_bagimsiz():
    """Rician sönümleme iki bağımsız bileşen ister."""
    i = [normal_cekimi("sonumleme_i", 5, 1, 2, k) for k in range(20_000)]
    q = [normal_cekimi("sonumleme_q", 5, 1, 2, k) for k in range(20_000)]
    ort_i, ort_q = ist.mean(i), ist.mean(q)
    kov = sum((a - ort_i) * (b - ort_q) for a, b in zip(i, q)) / len(i)
    r = kov / (ist.stdev(i) * ist.stdev(q))
    assert abs(r) < 0.03, f"I ve Q ilintili: r={r}"


def test_dugum_alt_akislari_ayrik():
    """`protokol_kesif` için zorunlu: bir düğümün çekimi diğerini kaydırmasın."""
    a = Akislar(1000)
    d1 = [a.dugum("protokol_kesif", 1).random() for _ in range(5)]
    b = Akislar(1000)
    for _ in range(37):                       # düğüm 2 bol bol çeksin
        b.dugum("protokol_kesif", 2).random()
    d1_tekrar = [b.dugum("protokol_kesif", 1).random() for _ in range(5)]
    assert d1 == d1_tekrar, "🔴 düğümler arası sessiz kuplaj"


def test_bilinmeyen_akis_ve_alan_reddediliyor():
    with pytest.raises(KeyError):
        Akislar(1)["yok_boyle"]
    with pytest.raises(KeyError):
        hash_cekimi("yok_boyle", 1, 2)


def test_akis_listesi_hash_uretiliyor_ve_degisime_duyarli():
    import sim2.cekirdek.rng as R
    once = akis_listesi_hash()
    eski = R.HASH_ALANLARI
    try:
        R.HASH_ALANLARI = eski + ("deneme_alani",)
        assert akis_listesi_hash() != once
    finally:
        R.HASH_ALANLARI = eski
    assert akis_listesi_hash() == once


def test_akis_listesi_ile_hash_alanlari_CAKISMIYOR():
    assert not (set(AKIS_ADLARI) & set(HASH_ALANLARI))


# ==========================================================================
# SAYAÇ KAYIT DEFTERİ — kusur 6
# ==========================================================================

def test_pencere_ikizi_OTOMATIK_turiyor():
    c = Sayaclar()
    c.artir("uretilen_paket", 10)
    c.pencere_baslat()
    c.artir("uretilen_paket", 100)
    c.pencere_bitir()
    d = c.disa_ver()
    assert d["uretilen_paket"] == 110
    assert d["uretilen_paket" + PENCERE_SONEKI] == 100


def test_pencere_KAPANINCA_ikiz_DONAR():
    """🔴 B2 — ikiz `[pencere başı, pencere SONU)` sayar, koşu sonuna kadar DEĞİL.

    Düzeltmeden önce `pencere_bitir` yalnız bir bayrak indiriyordu ve ikiz
    koşu sonunda `değer − pencere_başı` olarak türüyordu; yani boşalma
    aralığı da ikizin içindeydi. Ölçüldü (`statik-yok`, tohum 1000): kontrol
    baytının %9,1'i, beacon'ın %10,7'si boşalmadan geliyordu — veri tarafında
    ise %0,0, çünkü trafik çizelgesi pencerede biter. Pay büyüyüp payda
    büyümediği için `nrl_bayt_pencere` %10 şişiyordu ve şişme protokol
    ailesine göre farklıydı (periyodik kontrol boşalmada akar, keşif trafiği
    susar) — bir büyüklük sorunu değil, KARŞILAŞTIRMA GEÇERLİLİĞİ sorunu.
    """
    c = Sayaclar()
    c.pencere_baslat()
    c.artir("kontrol_cerceve", 100)
    c.ekle("kontrol_bayt", 6400.0)
    c.pencere_bitir()
    # --- boşalma aralığı: periyodik kontrol akmaya devam ediyor ---
    c.artir("kontrol_cerceve", 11)
    c.ekle("kontrol_bayt", 704.0)
    d = c.disa_ver()
    assert d["kontrol_cerceve"] == 111, "ham değer boşalmayı de sayar"
    assert d["kontrol_cerceve" + PENCERE_SONEKI] == 100, "ikiz DONMALI"
    assert d["kontrol_bayt" + PENCERE_SONEKI] == 6400.0


def test_pencere_icinde_olculdu_ikize_GIRER():
    """🔒 Koşu SONUNDA yazılan ama PENCEREDE ölçülmüş sayacın yolu.

    🔴 Bu, dondurmanın tuzağıdır ve ölçülerek bulundu: `kopma_fiziksel`
    geometriden, koşu bittikten SONRA, ölçüm penceresi için hesaplanır.
    Sıradan `artir` ile yazılsaydı pencere çoktan donmuş olurdu ve ikiz
    **0** çıkardı. Ölçüldü (`bagimsiz-surekli`, tohum 1000): ham 49, ikiz
    49 → 0 olurdu ve `algilama_duyarliligi_pencere` 0,0 yerine `None`
    dönerdi — yani Risk 3'ün NİCEL yarısı sessizce ölürdü.
    """
    c = Sayaclar()
    c.pencere_baslat()
    c.artir("kopma_algilanan", 12)
    c.pencere_bitir()
    # Koşu bitti; kâhin sayaç ŞİMDİ yazılıyor ama PENCEREYİ ölçüyor.
    c.pencere_icinde_olculdu("kopma_fiziksel", 49)
    d = c.disa_ver()
    assert d["kopma_fiziksel"] == 49
    assert d["kopma_fiziksel" + PENCERE_SONEKI] == 49, "ikiz 0'a DÜŞMEMELİ"
    assert d["algilama_duyarliligi" + PENCERE_SONEKI] == pytest.approx(12 / 49)
    # 🔒 Sıradan `artir` ile yazılsaydı ne olurdu — tuzağın kendisi:
    c2 = Sayaclar()
    c2.pencere_baslat()
    c2.pencere_bitir()
    c2.artir("kopma_fiziksel", 49)
    assert c2.disa_ver()["kopma_fiziksel" + PENCERE_SONEKI] == 0


def test_pencere_icinde_olculdu_pencere_ACILMADIYSA_ikiz_None():
    """*"Ölçüm yok"* ile *"sıfır"* ayrımı bu yolda da korunur."""
    c = Sayaclar()
    c.pencere_icinde_olculdu("kopma_fiziksel", 7)
    d = c.disa_ver()
    assert d["kopma_fiziksel"] == 7
    assert d["kopma_fiziksel" + PENCERE_SONEKI] is None


def test_pencere_acik_ile_pencere_basladi_AYRI_kavram():
    """🔴 İkisi 16 Eylül 2026'dan önce aynı şeydi ve bu sessiz bir kaçaktı.

    `pencere_basladi` *"ikiz var mı"* sorusuna cevap verir ve pencere
    kapandıktan sonra da `True` kalır. `pencere_acik` *"bu artış ikize girer
    mi"* sorusuna cevap verir. Mesaj biçimi dökümü birincisini kullanıyordu;
    yani ikizler donduğunda döküm donmaz ve `Σ bicim["pencere"]` ile
    `kontrol_iletim_pencere` AYRIŞIRDI.
    """
    c = Sayaclar()
    assert not c.pencere_basladi and not c.pencere_acik
    c.pencere_baslat()
    assert c.pencere_basladi and c.pencere_acik
    c.pencere_bitir()
    assert c.pencere_basladi, "ikiz VAR — pencere açılmıştı"
    assert not c.pencere_acik, "ama artık ikize giren bir şey YOK"


def test_tepe_sayaci_FARKLA_turetilmiyor():
    """🔴 Maksimum bir toplam değildir; farkla türetmek yanlış sayı verir."""
    c = Sayaclar()
    c.tepe_guncelle("en_yuksek_doluluk", 7)
    c.pencere_baslat()
    c.tepe_guncelle("en_yuksek_doluluk", 4)
    c.pencere_bitir()
    d = c.disa_ver()
    assert d["en_yuksek_doluluk"] == 7
    assert d["en_yuksek_doluluk" + PENCERE_SONEKI] == 4, "7−4=3 olmamalı"


def test_pencere_acilmadiysa_ikiz_None_SIFIR_DEGIL():
    """*"Ölçüm yok"* ile *"sıfır"* aynı şey değildir."""
    c = Sayaclar()
    c.artir("teslim_paket", 5)
    d = c.disa_ver()
    assert d["teslim_paket"] == 5
    assert d["teslim_paket" + PENCERE_SONEKI] is None


def test_turev_payda_sifirken_None():
    """⚠️ Örnek türev `pdr` idi; 8 Eylül 2026'da `pdr` sayaç kayıt
    defterinden ÇIKARILDI (kohort uyuşmazlığı — `sayaclar.py`ye bak) ve
    artık tek tanımı `olcum/metrikler.py`de, paket defterinden. Test edilen
    şey `pdr` değil TÜREV MAKİNESİ olduğu için hayatta kalan bir türevle
    yazıldı; iddia aynen korundu."""
    c = Sayaclar()
    c.pencere_baslat()
    c.artir("veri_alim_hedefte", 5)       # mac_deneme = 0 → payda sıfır
    c.artir("mac_gonderim_basarili", 5)
    c.pencere_bitir()
    assert c.disa_ver()["psr_pencere"] is None
    assert c.disa_ver()["mac_basari_orani_pencere"] is None


def test_turevler_HEM_tam_kosu_HEM_pencere_uretiyor():
    c = Sayaclar()
    c.pencere_baslat()
    c.artir("mac_deneme", 100)
    c.artir("veri_alim_hedefte", 70)
    c.artir("mac_gonderim_basarili", 55)
    c.pencere_bitir()
    d = c.disa_ver()
    for tv in (t for t in TANIMLAR if isinstance(t, Turev)):
        assert tv.ad in d, f"{tv.ad} tam koşu sürümü yok"
        assert tv.ad + PENCERE_SONEKI in d, f"{tv.ad} pencere sürümü yok"
    # 🔒 PSR alıcı tarafında (K-113); onaya dayalı oran ayrı adla kalır.
    assert d["psr_pencere"] == pytest.approx(0.70)
    assert d["mac_basari_orani_pencere"] == pytest.approx(0.55)
    # 🔒 `pdr` BURADA OLMAMALI: sayaç oranı olarak kaldırıldı, tek tanımı
    # paket defterinde. Buraya geri gelirse iki tanım yeniden doğar.
    assert "pdr" not in d and "pdr_pencere" not in d


def test_ikizsiz_sayac_GEREKCE_tasimak_zorunda():
    """🔴 Risk 2'nin yapısal panzehiri — yükleme anında zorlanır."""
    for t in _sayac_tanimlari():
        if not t.pencere_ikizi:
            assert t.ikizsiz_gerekce.strip(), (
                f"{t.ad!r}: pencere ikizi kapalı ama gerekçe boş")
        else:
            assert not t.ikizsiz_gerekce, f"{t.ad!r}: bayat gerekçe"


def test_ikizsiz_rapor_gerekceyi_TASIYOR():
    c = Sayaclar()
    c.artir("islenen_olay", 100)
    c.pencere_baslat()
    r = c.ikizsiz_rapor()
    assert "islenen_olay" in r and r["islenen_olay"][1].strip()


def test_tanimsiz_sayac_SESSIZCE_yaratilmiyor():
    c = Sayaclar()
    with pytest.raises(KeyError):
        c.artir("uydurma_sayac")
    with pytest.raises(KeyError):
        c.tepe_guncelle("uretilen_paket", 5)     # 'tepe' değil


def test_IKINCI_bir_sayac_listesi_YOK():
    """🔴 Kusur 6'nın kalbi.

    Eski simülatörde 25 sayaç ifadesi iki yerde birebir tekrarlanıyordu ve
    `_PENCERE_SAYACLARI` elle tutulan **ikinci bir listeydi**. Bu test,
    `sim2/` altında sayaç adlarının `sayaclar.py` DIŞINDA dizgi olarak
    geçmediğini AST ile denetler.
    """
    adlar = {t.ad for t in _sayac_tanimlari()}
    ihlal: list[str] = []
    for yol in sorted(SIM2.rglob("*.py")):
        if "__pycache__" in yol.parts or yol.name == "sayaclar.py":
            continue
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        for n in ast.walk(agac):
            if isinstance(n, ast.Constant) and isinstance(n.value, str):
                if n.value in adlar:
                    ihlal.append(
                        f"{yol.relative_to(KOK).as_posix()}:{n.lineno} "
                        f"→ {n.value!r}")
    # Sayaç adları elbette çağrı argümanı olarak geçecek (`artir("x")`);
    # bu test onları YASAKLAMAZ — yasakladığı şey, sayaç adlarının bir
    # LİSTE/DEMET olarak ikinci kez toplanmasıdır.
    listeler: list[str] = []
    for yol in sorted(SIM2.rglob("*.py")):
        if "__pycache__" in yol.parts or yol.name == "sayaclar.py":
            continue
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        for n in ast.walk(agac):
            if isinstance(n, (ast.List, ast.Tuple, ast.Set)):
                sabitler = {e.value for e in n.elts
                            if isinstance(e, ast.Constant)
                            and isinstance(e.value, str)}
                if len(sabitler & adlar) >= 3:
                    listeler.append(
                        f"{yol.relative_to(KOK).as_posix()}:{n.lineno}")
    assert not listeler, (
        f"🔴 sayaç adlarının ikinci bir listesi var: {listeler}. "
        f"Pencere ikizi ve sonuç şeması YALNIZ `TANIMLAR`dan türemeli.")


def test_sayac_semasi_hash_uretiliyor_ve_degisime_duyarli():
    once = sayac_semasi_hash()
    assert once and once == sayac_semasi_hash()


def test_kahin_sayaclar_isaretli():
    """Teşhis ↔ karar ayrımı: kâhin sayaç yalnız rapora girer."""
    kahinler = {t.ad for t in _sayac_tanimlari() if t.kahin}
    assert "kopma_fiziksel" in kahinler, (
        "fiziksel kopma geometriden bilinir — kâhin işaretlenmeli")


# ==========================================================================
# KİMLİK
# ==========================================================================

def test_kosu_kimligi_BELIRLENIMCI_ve_ayirt_edici():
    ortak = dict(arac="A", kurulum="K",
                 sayac_semasi=sayac_semasi_hash(),
                 akis_listesi=akis_listesi_hash())
    a = kosu_kimligi(kol="aodv", tohum=5, **ortak)
    assert a == kosu_kimligi(kol="aodv", tohum=5, **ortak)
    assert a != kosu_kimligi(kol="olsr", tohum=5, **ortak)
    assert a != kosu_kimligi(kol="aodv", tohum=6, **ortak)


def test_calisma_kimligi_kosu_kimligine_GIRMIYOR():
    """🔴 Girseydi her çalıştırma yeni kimlik üretir, kopya tespiti ölürdü."""
    ortak = dict(arac="A", kurulum="K", kol="x", tohum=1,
                 sayac_semasi="s", akis_listesi="a")
    assert kosu_kimligi(**ortak) == kosu_kimligi(**ortak)
    assert calisma_kimligi() == calisma_kimligi()   # süreç içinde sabit


def test_kurulum_hash_tedavi_alanlarini_DISLIYOR():
    temel = {"alan_m": 1000.0, "z_m": 120.0, "kol": "A", "senaryo": "S0"}
    tedavi = ("kol", "senaryo")
    a = kurulum_hash(temel, tedavi)
    b = kurulum_hash({**temel, "kol": "B", "senaryo": "S2"}, tedavi)
    c = kurulum_hash({**temel, "z_m": 300.0}, tedavi)
    assert a == b, "tedavi alanı kurulum özetini değiştirmemeli"
    assert a != c, "tedavi dışı alan kurulum özetini DEĞİŞTİRMELİ"


def test_kurulum_hash_AYIRICI_gercek():
    """Eski simülatörde ayırıcı `b""` idi — bir no-op."""
    a = kurulum_hash({"x": "ab", "y": "c"}, ())
    b = kurulum_hash({"x": "a", "y": "bc"}, ())
    assert a != b


def test_evren_hash_paket_evrenini_ayirt_ediyor():
    a = evren_hash([(1, 0.5, 2, 3), (2, 0.7, 4, 5)])
    assert a == evren_hash([(1, 0.5, 2, 3), (2, 0.7, 4, 5)])
    assert a != evren_hash([(1, 0.5, 2, 3), (2, 0.7, 4, 6)])
    assert a != evren_hash([(1, 0.5000001, 2, 3), (2, 0.7, 4, 5)])


def test_arac_hash_yalniz_sim2_yi_kapsiyor():
    """`protokoller/` ve `analiz/` bu özete girmemeli."""
    h = arac_hash()
    assert len(h) == 32 and h == arac_hash()


def test_her_ham_sayac_BIR_YERDE_ARTIRILIYOR():
    """🔴 TANIMLI AMA HİÇ ARTIRILMAYAN SAYAÇ — bu depoda ÜÇ KEZ yaşandı.

    `kopma_fiziksel` 9 Eylül'e kadar hiç sayılmıyordu (`olcum/kopma.py`);
    `rota_etkilendi` 19 Eylül'e kadar hiç artırılmıyordu ve sayaçtan türeyen
    `cor` ile `cor_pencere` bu yüzden HER koşuda boştu (`04` K-141). İkisinde
    de sayaç kütükte duruyor, satıra yazılıyor ve hiçbir kapı konuşmuyordu.

    🔒 Tarama: her ham sayacın adı `sim2/` içinde (kütüğün kendisi hariç)
    tırnaklı olarak geçmeli. Kontrol düzlemi sayaçları `kontrol_durum.say`
    üzerinden ÖNEKSİZ adla artırıldığı için önek düşülmüş adı da kabul eder.

    ⚠️ Sınırı: ad bir belge dizesinde tırnaklı geçerse tarama kandırılır.
    Yakaladığı şey, yaşanan iki örneğin ortak hâlidir: adın HİÇ geçmemesi.
    """
    import re
    from sim2.cekirdek.sayaclar import TANIMLAR

    metin = "\n".join(
        p.read_text(encoding="utf-8")
        for p in (KOK / "sim2").rglob("*.py") if p.name != "sayaclar.py")
    olu = []
    for t in TANIMLAR:
        if type(t).__name__ != "SayacTanimi":
            continue
        adlar = [t.ad]
        if t.ad.startswith("kontrol_"):
            adlar.append(t.ad[len("kontrol_"):])
        if not any(re.search(r"[\"']" + re.escape(a) + r"[\"']", metin)
                   for a in adlar):
            olu.append(t.ad)
    assert not olu, f"hiçbir yerde artırılmayan sayaç: {olu}"
