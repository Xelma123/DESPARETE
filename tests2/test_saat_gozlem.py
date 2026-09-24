"""
ADIM 7 — `cekirdek/saat.py` ve `gozlem/` kapanış ölçütleri.

Yol haritası:
    Yüzey taraması yasak tipe ULAŞAMIYOR · `saat_senkron` ablasyonu
    ölçülebiliyor.

🔴 KUSUR 9 BURADA KAPANIYOR: tek küresel saat yapısal bir kâhin kanalıydı.
Bir protokol beacon'a zaman damgası koyduğu anda bedava kusursuz senkron
kazanıyordu ve hiçbir test bunu göremezdi.
"""

from __future__ import annotations

import ast
import dataclasses
import math
import pathlib
import statistics as ist
import sys

import pytest

KOK = pathlib.Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))
SIM2 = KOK / "sim2"

from sim2.cekirdek.degismezler import DegismezHatasi  # noqa: E402
from sim2.cekirdek.rng import Akislar  # noqa: E402
from sim2.cekirdek.saat import Saatler, YerelZaman  # noqa: E402
from sim2.gozlem.karar import BEYAN_TIPLERI, Beyan, Karar  # noqa: E402
from sim2.gozlem.pencere import (IZINLI_GOZLEM_ALANLARI,  # noqa: E402
                                 IZINLI_KOMSU_ALANLARI,
                                 IZINLI_PAKET_ALANLARI, YASAK_TIPLER,
                                 Gozlem, KomsuKaydi, PaketGorunumu)
from sim2.gozlem.protokol import KANCALAR, Protokol  # noqa: E402
from sim2.gozlem.teshis import TeshisHatasi, teshis_dogrula  # noqa: E402
from sim2.gozlem.yuk import YukHatasi, yuk_bayt, yuku_dondur  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402

K = Konfig(kol="test")


def _saatler(konfig: Konfig = K, tohum: int = 1) -> Saatler:
    return Saatler(dugum_sayisi=konfig.dugum_sayisi,
                   ofset_araligi_s=konfig.saat_ofset_araligi_s,
                   sapma_ppm=konfig.saat_sapma_ppm,
                   senkron=konfig.saat_senkron, akislar=Akislar(tohum))


# ==========================================================================
# 🔴 KUSUR 9 — SAAT
# ==========================================================================

def test_saatler_AYRISIYOR():
    """🔒 Bedava kusursuz senkron yasaklanmıyor, İMKÂNSIZ hâle geliyor."""
    s = _saatler()
    t = 100.0
    degerler = [float(s.yerel(i, t)) for i in range(K.dugum_sayisi)]
    assert len(set(degerler)) == K.dugum_sayisi, "iki düğüm aynı saati gösteremez"
    yayilim = max(degerler) - min(degerler)
    assert 0.5 < yayilim < 2.0 * K.saat_ofset_araligi_s + 0.1, (
        f"ölçülen ayrışma {yayilim*1000:.0f} ms")


def test_ofset_ve_sapma_ILAN_EDILEN_bandda():
    s = _saatler()
    ofsetler = [s.ofset_s(i) for i in range(K.dugum_sayisi)]
    sapmalar = [s.sapma_ppm(i) for i in range(K.dugum_sayisi)]
    assert all(abs(o) <= K.saat_ofset_araligi_s for o in ofsetler)
    assert abs(ist.mean(ofsetler)) < 0.2
    # sapma N(0, 20) ppm — 40 örnekte std bandı geniş tutuluyor
    assert 8.0 < ist.pstdev(sapmalar) < 45.0
    assert all(abs(v) < 5.0 * K.saat_sapma_ppm for v in sapmalar)


def test_sapma_ZAMANLA_buyuyor():
    """Ofset sabittir, sapma zamanla birikir — ikisi ayrı kiplerdir."""
    s = _saatler()
    fark_0 = float(s.yerel(0, 0.0)) - s.ofset_s(0)
    assert fark_0 == pytest.approx(0.0, abs=1e-12)
    for t in (10.0, 350.0):
        birikim = float(s.yerel(0, t)) - s.ofset_s(0) - t
        assert birikim == pytest.approx(t * s.sapma_ppm(0) * 1e-6, rel=1e-9)


def test_yerel_ve_kuresel_TERS():
    s = _saatler()
    for dugum in (0, 7, 39):
        for t in (0.0, 12.34, 349.9):
            assert s.kuresel(dugum, float(s.yerel(dugum, t))) == \
                pytest.approx(t, abs=1e-9)


def test_SENKRON_ABLASYONU():
    """🔒 *"Saat senkronizasyonu olsaydı ne olurdu"* ölçülebilir bir kol."""
    s = _saatler(Konfig(kol="t", saat_senkron=True))
    assert s.senkron is True
    for dugum in (0, 5, 39):
        for t in (0.0, 100.0, 350.0):
            assert float(s.yerel(dugum, t)) == t
    assert s.en_buyuk_fark_s(200.0) == 0.0


def test_SENKRON_ablasyonu_AKIS_TUKETMIYOR():
    """🔴 Ablasyon kolu öteki kolların rastgeleliğini KAYDIRMAMALI.

    Tüketseydi, `saat_senkron=True` koşusu bütün öteki çekimleri kaydırır ve
    ablasyon "saatin etkisi" yerine "başka bir dünya" ölçerdi.
    """
    a = Akislar(3)
    Saatler(dugum_sayisi=40, ofset_araligi_s=0.5, sapma_ppm=20.0,
            senkron=True, akislar=a)
    b = Akislar(3)
    assert a["saat_ofset"].random() == b["saat_ofset"].random()


def test_saat_BELIRLENIMCI():
    assert [_saatler().ofset_s(i) for i in range(5)] == \
           [_saatler().ofset_s(i) for i in range(5)]
    assert _saatler(tohum=1).ofset_s(0) != _saatler(tohum=2).ofset_s(0)


def test_gecersiz_saat_parametreleri_REDDEDILIYOR():
    for ek in (dict(dugum_sayisi=0), dict(ofset_araligi_s=-1.0),
               dict(sapma_ppm=-1.0)):
        arg = dict(dugum_sayisi=40, ofset_araligi_s=0.5, sapma_ppm=20.0,
                   senkron=False, akislar=Akislar(1))
        arg.update(ek)
        with pytest.raises(DegismezHatasi):
            Saatler(**arg)


def test_ZAMAN_DAMGASI_koyan_protokol_OFSETI_goruyor():
    """🔴 Kusur 9'un somut hâli.

    A düğümü kendi saatini beacon'a yazıyor; B onu kendi saatiyle
    karşılaştırıyor. Eski simülatörde fark SIFIR olurdu (bedava senkron).
    """
    s = _saatler()
    t = 150.0
    a_damgasi = float(s.yerel(3, t))
    b_saati = float(s.yerel(17, t))
    yanilma = a_damgasi - b_saati
    assert abs(yanilma) > 0.01, (
        "🔴 saat damgası bedava senkron veriyor — kusur 9 geri geldi")
    assert yanilma == pytest.approx(s.fark_s(3, 17, t), abs=1e-12)


def test_saat_cekirdekte_KONFIGI_ice_aktarmiyor():
    """Katman yönü: `cekirdek` `yapilandirma`dan öncedir."""
    agac = ast.parse((SIM2 / "cekirdek" / "saat.py").read_text(encoding="utf-8"))
    for n in ast.walk(agac):
        if isinstance(n, ast.ImportFrom) and n.module:
            assert not n.module.startswith("sim2.yapilandirma"), (
                f"🔴 katman yönü kırıldı: {n.module}")


# ==========================================================================
# GÖZLEM YÜZEYİ
# ==========================================================================

def _gozlem() -> Gozlem:
    return Gozlem(
        dugum=3, saat_s=YerelZaman(12.5), olculen_gurultu_w=1e-12,
        kanal_mesgul_mu=False, kuyruk_uzunlugu=4, kuyruk_kapasitesi=50,
        son_iletim_sonucu="onay", son_iletim_hedefi=9,
        gonderilen_bayt=1024, alinan_bayt=2048,
        komsular=(KomsuKaydi(dugum=9, son_duyulma_s=YerelZaman(11.0),
                             duyulan_beacon=7, bildirdigi_gurultu_w=2e-12,
                             bildirdigi_kuyruk=2,
                             bildirdigi_yuk=(("etx", 1.5),)),),
        paket=PaketGorunumu(hedef=20, kaynak=3, ttl=30, atlama_sayisi=2,
                            bayt=512, kaynak_sira=0))


def test_gozlem_DONDURULMUS():
    """Her nesne KENDİ alanıyla denenir: olmayan bir alana yazmak
    `TypeError` verir ve dondurulmuşluğu hiç sınamaz."""
    g = _gozlem()
    for nesne, alan in ((g, "dugum"), (g.komsular[0], "dugum"),
                        (g.paket, "hedef")):
        with pytest.raises(dataclasses.FrozenInstanceError):
            setattr(nesne, alan, 99)


def test_IZIN_LISTELERI_yuzeyle_birebir():
    """Listede olmayan bir alan eklemek testi kırar ve gözlem sözleşmesi
    belgesi güncellenmeden geçilemez."""
    assert {f.name for f in dataclasses.fields(Gozlem)} == IZINLI_GOZLEM_ALANLARI
    assert {f.name for f in dataclasses.fields(KomsuKaydi)} == IZINLI_KOMSU_ALANLARI
    assert {f.name for f in dataclasses.fields(PaketGorunumu)} == IZINLI_PAKET_ALANLARI


def test_YUZEY_TARAMASI_yasak_tipe_ULASAMIYOR():
    """🔒 Kapanış ölçütü. Pencereden gezerek hiçbir kâhin tipe varılamamalı."""
    gorulen: list[str] = []

    def gez(nesne, yol: str, derinlik: int = 0) -> None:
        if derinlik > 6:
            return
        ad = type(nesne).__name__
        gorulen.append(ad)
        assert ad not in YASAK_TIPLER, f"🔴 {yol} → yasak tip {ad}"
        if dataclasses.is_dataclass(nesne):
            for f in dataclasses.fields(nesne):
                gez(getattr(nesne, f.name), f"{yol}.{f.name}", derinlik + 1)
        elif isinstance(nesne, (tuple, list)):
            for i, x in enumerate(nesne):
                gez(x, f"{yol}[{i}]", derinlik + 1)

    gez(_gozlem(), "gozlem")
    assert "Gozlem" in gorulen and "KomsuKaydi" in gorulen


def test_gozlem_GERI_REFERANS_tasimiyor():
    """Pencerede simülatöre giden hiçbir nesne olmamalı — tip adlarıyla
    değil, ULAŞILABİLİR TİPLERLE denetlenir."""
    izinli = {"Gozlem", "KomsuKaydi", "PaketGorunumu", "int", "float", "str",
              "bool", "tuple", "NoneType"}
    def gez(nesne, derinlik=0):
        if derinlik > 6:
            return
        assert type(nesne).__name__ in izinli, (
            f"🔴 pencerede beklenmeyen tip: {type(nesne).__name__}")
        if dataclasses.is_dataclass(nesne):
            for f in dataclasses.fields(nesne):
                gez(getattr(nesne, f.name), derinlik + 1)
        elif isinstance(nesne, tuple):
            for x in nesne:
                gez(x, derinlik + 1)
    gez(_gozlem())


def test_DOGUM_ZAMANI_pencerede_YOK():
    """🔴 Kusur 9'un arka kapısı: farklı saatlerdeki iki düğüm doğum anını
    karşılaştırarak saat farkını sıfır maliyetle öğrenirdi."""
    assert "dogum_s" not in IZINLI_PAKET_ALANLARI
    assert "dogum_s" not in IZINLI_GOZLEM_ALANLARI


def test_MOBILITE_bedava_alan_EKLEMEDI():
    """🔒 Ağ hareketli ama pencerede hız/yön/yörünge yok. Hareket bilgisi
    isteyen protokol onu `bildirdigi_yuk` ile taşır ve bedelini öder."""
    yasak = {"hiz", "hiz_ms", "yon", "azimut", "yorunge", "bildirdigi_hiz",
             "komsu_hizi", "gorece_hiz"}
    assert not (yasak & (IZINLI_GOZLEM_ALANLARI | IZINLI_KOMSU_ALANLARI))


def test_KONUM_YUZEYDE_YOK_tasiyan_BEDELINI_oder():
    """🔴 `bildirdigi_konum` KALDIRILDI — 16 Eylül 2026 (denetim B4, K-131).

    Alan sözleşmede *"3B, bedeli otomatik faturalanır"* diye duruyordu ama
    koşucu onu hiç doldurmuyordu: ölçüldü, komşu kayıtlarının **%100'ünde**
    `None`. Belge bir yetenek anlatıyor, kod vermiyordu.

    🔒 Doldurmak yerine kaldırıldı: konum isteyen protokol onu `beacon_yuku`na
    KOYAR ve BAYT BEDELİNİ ÖDER — sözleşmenin zaten söylediği yol. Bu test o
    yolun hâlâ açık ve hâlâ ücretli olduğunu bağlar.
    """
    assert "bildirdigi_konum" not in IZINLI_KOMSU_ALANLARI
    iki_b = yuk_bayt({"k": (1.0, 2.0)})
    uc_b = yuk_bayt({"k": (1.0, 2.0, 3.0)})
    assert uc_b - iki_b == 4, "üçüncü bileşen tek duyarlıkla 4 bayt etmeli"
    # 🔒 Ve boşluk BEDAVA değil: yükü taşıyan çerçeve gerçekten uzar.
    assert yuk_bayt({"konum": (1.0, 2.0, 3.0)}) == len("konum") + 3 * 4


def test_bilgi_YOKLUGU_sifirdan_AYRI():
    """🔴 `None ≠ 0` — kuralın projedeki tek istisnası kapandı (K-131).

    Beacon'a alan koymayan bir protokolde `bildirdigi_*` artık `0` değil
    `None` döner. Sıfır gürültü bildiren komşu ile hiç bildirmeyen komşu
    ayırt edilebilir; edilemeseydi protokol olmayan bir ölçüme dayanarak
    karar verirdi.
    """
    bos = KomsuKaydi(dugum=1, son_duyulma_s=YerelZaman(0.0), duyulan_beacon=1,
                     bildirdigi_gurultu_w=None, bildirdigi_kuyruk=None)
    dolu = KomsuKaydi(dugum=2, son_duyulma_s=YerelZaman(0.0), duyulan_beacon=1,
                      bildirdigi_gurultu_w=0.0, bildirdigi_kuyruk=0)
    assert bos.bildirdigi_gurultu_w is None and bos.bildirdigi_kuyruk is None
    assert dolu.bildirdigi_gurultu_w == 0.0 and dolu.bildirdigi_kuyruk == 0


def test_komsu_YASI_kendi_saatine_gore():
    g = _gozlem()
    assert g.komsular[0].yas_s(g.saat_s) == pytest.approx(1.5)
    assert g.komsu(9) is not None and g.komsu(99) is None
    assert g.kuyruk_doluluk == pytest.approx(4 / 50)


# ==========================================================================
# KARAR ve BEYAN
# ==========================================================================

def test_karar_varsayilani_HEDEF_YOK():
    k = Karar()
    assert k.sonraki is None and not k.beyan_var_mi


def test_beyan_KAPALI_kume():
    for tip in BEYAN_TIPLERI:
        Beyan(tip=tip)
    with pytest.raises(DegismezHatasi):
        Beyan(tip="ucan_hali")


def test_beyan_TIPE_gore_suzuluyor():
    k = Karar(sonraki=5, beyan=(Beyan("kopma", 9), Beyan("rota_kuruldu"),
                                Beyan("kopma", 12)))
    assert len(k.beyanlar("kopma")) == 2
    assert len(k.beyanlar("rota_gecersiz")) == 0
    with pytest.raises(DegismezHatasi):
        k.beyanlar("uydurma")


def test_karar_DONDURULMUS():
    k = Karar(sonraki=1)
    with pytest.raises(dataclasses.FrozenInstanceError):
        k.sonraki = 2  # type: ignore[misc]


def test_rota_gecersiz_DUSME_SEBEBI_olarak_VAR():
    """🔒 Sebep listesi bir ŞEMA taahhüdüdür; protokoller yazılmadan ÖNCE
    eklenmişti, tam da bu yüzden."""
    from sim2.cekirdek.korunum import DUSME_SEBEPLERI
    assert "rota_gecersiz" in DUSME_SEBEPLERI
    assert "rota_gecersiz" in BEYAN_TIPLERI


# ==========================================================================
# PROTOKOL ARAYÜZÜ
# ==========================================================================

def test_protokol_KANCALARI():
    for kanca in KANCALAR:
        assert hasattr(Protokol, kanca)


def test_eksik_kancali_protokol_UYMUYOR():
    class Yarim:
        ad = "yarim"
        def sonraki_atlama(self, gozlem):
            return Karar()
    assert not isinstance(Yarim(), Protokol)


def test_tam_protokol_UYUYOR():
    class Tam:
        ad = "tam"
        def sonraki_atlama(self, gozlem):
            return Karar(sonraki=gozlem.paket.hedef if gozlem.paket else None)
        def beacon_yuku(self, gozlem):
            return {}
        def beacon_alindi(self, gozlem, komsu, yuk):
            pass
        def teshis(self, dugum):
            return {}
    p = Tam()
    assert isinstance(p, Protokol)
    assert p.sonraki_atlama(_gozlem()).sonraki == 20


def test_gozlem_paketi_SIMULATORU_ice_aktarmiyor():
    """🔒 `gozlem/` yalnız `cekirdek/`i görür: `Karar` ve `Gozlem`in içine
    kanal, dünya ya da ölçüm sızmamalı."""
    ihlal: list[str] = []
    for yol in sorted((SIM2 / "gozlem").rglob("*.py")):
        if "__pycache__" in yol.parts:
            continue
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        for n in ast.walk(agac):
            if isinstance(n, ast.ImportFrom) and n.module \
                    and n.module.startswith("sim2.") \
                    and not n.module.startswith(("sim2.cekirdek",
                                                 "sim2.gozlem")):
                ihlal.append(f"{yol.name}:{n.lineno} → {n.module}")
    assert not ihlal, f"🔴 `gozlem/` simülatörü içe aktarıyor: {ihlal}"


# ==========================================================================
# TAŞINAN MODÜLLER — kapıların hâlâ konuştuğu
# ==========================================================================

def test_yuk_bayt_TARIFEYI_uyguluyor():
    assert yuk_bayt({}) == 0
    assert yuk_bayt({"a": True}) == 1 + 1
    assert yuk_bayt({"ab": 1.5}) == 2 + 4
    assert yuk_bayt({"a": 255}) == 1 + 1
    assert yuk_bayt({"a": 256}) == 1 + 2      # büyüklüğüyle faturalanır


def test_yuk_SOZLESME_DISI_degeri_REDDEDIYOR():
    for kotu in ({"a": "metin"}, {"a": None}, {"a": ()}, {"a": ("x",)},
                 {"": 1}, {1: 2}):
        with pytest.raises(YukHatasi):
            yuk_bayt(kotu)
    with pytest.raises(YukHatasi):
        yuk_bayt({"a": 1e40})                 # tel biçimine sığmıyor


def test_IKI_HESAP_gercekten_AYRI():
    """🔒 `yuk_bayt` tarifeyi uygular, ölçüm yolu tarifeyi HİÇ kullanmaz.

    Bağımsızlık bir kez ÖLMÜŞTÜ (`assert x >= x`). Tarifeyi bozup ölçüm
    yolunun konuştuğunu göstererek sınanır.
    """
    import sim2.gozlem.yuk as Y
    eski = Y.YUK_FLOAT_BAYT
    try:
        Y.YUK_FLOAT_BAYT = 2                  # tarifeyi BOZ
        with pytest.raises(YukHatasi):
            Y.yuk_bayt({"a": 1.5})            # ölçüm yolu 4 der, tarife 2
    finally:
        Y.YUK_FLOAT_BAYT = eski


def test_yuku_dondur_TEK_DUYARLIGA_kirpiyor():
    """🔴 Kırpma olmasaydı 8 baytlık bir çift duyarlık değeri 4 bayt bedelle
    taşınırdı — ölçülmüş 2,00× kaçak."""
    ham = 1.0 / 3.0
    (_, kirpilmis), = yuku_dondur({"a": ham})
    assert kirpilmis != ham
    import struct
    assert kirpilmis == struct.unpack("<f", struct.pack("<f", ham))[0]


def test_yuku_dondur_SIRALI_ve_DONMUS():
    d = yuku_dondur({"z": 1, "a": 2, "m": 3})
    assert isinstance(d, tuple)
    assert [ad for ad, _ in d] == ["a", "m", "z"]


def test_teshis_NaN_reddediyor():
    """Tip denetimi NaN'ı KAÇIRIR: `nan` da bir `float`tır."""
    for kotu in (float("nan"), math.inf, -math.inf):
        with pytest.raises(TeshisHatasi):
            teshis_dogrula(0, {"x": kotu})


def test_teshis_SOZLESMESI():
    assert teshis_dogrula(0, None) == {}
    assert teshis_dogrula(0, {"a": 1, "b": 2.5, "c": "iyi", "d": (1, 2)}) is not None
    with pytest.raises(TeshisHatasi):
        teshis_dogrula(0, {"a": {"ic": 1}})            # sözlük taşınamaz
    with pytest.raises(TeshisHatasi):
        teshis_dogrula(0, {1: 2})                      # dizgi olmayan anahtar
    with pytest.raises(TeshisHatasi):
        teshis_dogrula(0, {f"a{n}": n for n in range(100)})   # çok alan


def test_sim2_altinda_hala_CIPLAK_ASSERT_YOK():
    """🔴 Taşınan modülde çıplak `assert` vardı ve `-O` altında kalkıyordu;
    taşımada `dogrula`ya çevrildi. Bu test onun geri gelmediğini bağlar."""
    bulunan: list[str] = []
    for yol in sorted(SIM2.rglob("*.py")):
        if "__pycache__" in yol.parts:
            continue
        for n in ast.walk(ast.parse(yol.read_text(encoding="utf-8"))):
            if isinstance(n, ast.Assert):
                bulunan.append(f"{yol.relative_to(KOK).as_posix()}:{n.lineno}")
    assert not bulunan, f"🔴 çıplak assert: {bulunan}"
