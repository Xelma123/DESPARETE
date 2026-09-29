"""
Ç5 — GÖZLEM SÖZLEŞMESİ.

🔴 BU TESTLER OLMADAN `05-GOZLEM-PENCERESI.md` yalnızca bir DİLEK'tir.

Belge, kodun kanıtı değildir; kod, belgenin kanıtıdır. Bu dosya belgeyi koda
bağlar: pencereye bir alan eklenirse ya da simülatöre bir sızıntı açılırsa
test kırılır.

⚠️ Sonradan DARALTMAK, o zamana kadarki tüm ölçümleri geçersiz kılar.
Sonradan GENİŞLETMEK, önceki sonuçları yeni sonuçlarla karşılaştırılamaz
hâle getirir. Her iki yön de kayda geçmek zorunda.
"""

from __future__ import annotations

import dataclasses
import sys
from pathlib import Path

import pytest
import types

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dogrulama.aktaricilar import en_kisa_yol, gurultuden_kacan  # noqa: E402
from sim.config import Konfig  # noqa: E402
from sim.gozlem import (  # noqa: E402
    IZINLI_GOZLEM_ALANLARI, IZINLI_KOMSU_ALANLARI, IZINLI_PAKET_ALANLARI,
    YASAK_TIPLER, Gozlem, KomsuKaydi, PaketGorunumu,
)
from sim.kosucu import Kosu  # noqa: E402


def icerik_testi(*alanlar: str):
    """Bu testin İÇERİĞİNİ doğruladığı `Gozlem` alanlarını işaretler.

    🔴 B-43 (K-047) — NEDEN İŞARETLEYİCİ, NEDEN ELLE KÜME DEĞİL:
    Önceki sürüm `ICERIK_TESTI_OLAN` adında **elle yazılmış** bir küme
    taşıyordu ve kontrol şuna indirgeniyordu: *"iki dosyadaki iki elle
    yazılmış küme eşit mi?"* Üçüncü bağımsız denetim ölçtü:

      · bir içerik testinin adı devre dışı bırakıldığında koruma **sustu**
        (17 passed) — küme testin varlığından TÜREMİYORDU;
      · küme **zaten yanlıştı**: `olculen_gurultu_w` ve `paket` içerik
        testleri olduğu iddiasıyla listedeydi, hiçbiri yoktu.

    `03` B5 bu tuzağı adıyla sayıyor: *"etiketi elle taşımak — elle yazılan
    etiket sessizce yanlışlaşır."* B-06 (`UYGULANMAMIS_BAYRAKLAR`) ve B-10
    (`rng.HENUZ_KULLANILMAYAN`) korumaları DAVRANIŞA bağlıydı; bu koruma
    hiçbir şeye bağlı değildi — desenin üçüncüsü değil, **görünüşüydü**.

    Artık kapsam, testlerin **kendisinden** türüyor: bir test silinir, adı
    değişir ya da işaretleyicisi düşerse kapsam küçülür ve koruma konuşur.
    """
    def sar(fn):
        # 🔴 B-76 (K-056) — İŞARETLEYİCİ GÖVDEYİ DOĞRULAR.
        # Dördüncü bağımsız denetim ölçtü: `son_iletim_sonucu` işaretleyicisi,
        # gövdesinde o alanın ADI HİÇ GEÇMEYEN bir teste iliştirilmişti.
        # Alan fiilen korunuyordu — ama YANLIŞ ETİKETLİ komşu test sayesinde.
        # O test silinse `_icerik_testi_olan()` alanı hâlâ "kapsanmış" sayar
        # ve B-27b koruması SUSARDI.
        #
        # `03` B5'in "etiketi elle taşımak" tuzağı, B-43'ün düzeltmesinin
        # İÇİNDE. Kontrol artık davranışa bağlı: kaynağı okunabildiği için
        # işaretlenen alanın gövdede geçtiği ÇALIŞMA ANINDA doğrulanıyor.
        # 🔴 B-89 (BEŞİNCİ DENETİM, 26 Ağustos 2026) — PROZA KOD DEĞİLDİR.
        # Önceki hâl `inspect.getsource(fn)` METNİNDE düz alt dizgi arıyor ve
        # yalnızca `@` ile başlayan satırları eliyordu. **Docstring ve yorum
        # satırları gövdeye dâhildi**: alanın adı yalnızca PROZADA geçen bir
        # test "işaretlenmiş" sayılıyordu.
        #
        # ⚖️ Bu, B-68'in **AYNI OTURUMDA reddettiği** desenin ta kendisiydi:
        # *"bir kaynak denetimi prozayı koddan ayırt edemiyorsa ölçüt
        # değildir — AST'ye bağlandı."* B-76'nın düzeltmesi o dersi kendi
        # içine uygulamamıştı.
        #
        # Artık gövde AST'den okunuyor: docstring atılıyor, `ast.unparse`
        # zaten yorum taşımıyor, ve dekoratörler `body`de değil.
        import ast
        import inspect
        import textwrap

        agac = ast.parse(textwrap.dedent(inspect.getsource(fn)))
        dugum = agac.body[0]
        govde_dugumleri = list(getattr(dugum, "body", []))
        if (govde_dugumleri
                and isinstance(govde_dugumleri[0], ast.Expr)
                and isinstance(govde_dugumleri[0].value, ast.Constant)
                and isinstance(govde_dugumleri[0].value.value, str)):
            govde_dugumleri = govde_dugumleri[1:]        # docstring ATILIR
        govde = chr(10).join(ast.unparse(x) for x in govde_dugumleri)
        eksik = [a for a in alanlar if a not in govde]
        if eksik:
            raise AssertionError(
                f"{fn.__name__}: {eksik} alan(lar)ı işaretlenmiş ama test "
                f"gövdesinde geçmiyor. Etiket elle taşınmış olabilir (B-76).")
        fn._gozlem_alanlari = frozenset(alanlar)
        return fn
    return sar


def _bir_gozlem(senaryo="S2", tohum=1, an_s=100.0) -> Gozlem:
    """Koşuyu bir noktaya kadar ilerletip gerçek bir gözlem üretir."""
    k = Kosu(Konfig(kol="t", senaryo=senaryo, tohum=tohum), en_kisa_yol)
    k._beaconlari_basla()
    k.trafik.basla()
    k.olaylar.kostur(an_s)
    dolu = max(range(k.kon.dugum_sayisi),
               key=lambda d: len(k.komsu_tablosu[d]))
    return k._gozlem_uret(dolu, None)


# ==========================================================================
# Ç5.1 — SİMÜLATÖRE GERİ REFERANS YOK
# ==========================================================================

def _yuzeyi_gez(nesne, yol="gozlem", derinlik=0, gorulen=None):
    """Nesnenin ulaşılabilir yüzeyini özyinelemeli gezer."""
    if gorulen is None:
        gorulen = set()
    if derinlik > 6 or id(nesne) in gorulen:
        return []
    gorulen.add(id(nesne))
    bulgular = [(yol, type(nesne).__name__)]
    if dataclasses.is_dataclass(nesne):
        for alan in dataclasses.fields(nesne):
            bulgular += _yuzeyi_gez(getattr(nesne, alan.name),
                                    f"{yol}.{alan.name}", derinlik + 1, gorulen)
    elif isinstance(nesne, (tuple, list)):
        for i, x in enumerate(nesne[:5]):
            bulgular += _yuzeyi_gez(x, f"{yol}[{i}]", derinlik + 1, gorulen)
    elif isinstance(nesne, dict):
        for anahtar in list(nesne)[:5]:
            bulgular += _yuzeyi_gez(nesne[anahtar], f"{yol}[{anahtar!r}]",
                                    derinlik + 1, gorulen)
    return bulgular


def test_c5_1_simulatore_geri_referans_yok():
    """🔴 Ç5.1 — gözlemden simülatöre ULAŞILAMAZ."""
    g = _bir_gozlem()
    for yol, tip in _yuzeyi_gez(g):
        assert tip not in YASAK_TIPLER, (
            f"gözlem penceresinden {tip} nesnesine ulaşılıyor: {yol}"
        )


def test_c5_1b_mutasyon_sizinti_yakalaniyor():
    """Kontrol: kasten bir sızıntı eklenirse tarama YAKALAMALI.

    Yakalamıyorsa üstteki test boş bir testtir.
    """
    from sim.topology import Topoloji

    @dataclasses.dataclass(frozen=True)
    class SizanGozlem:
        dugum: int
        topo: Topoloji

    kon = Konfig(kol="t")
    from sim.rng import Akislar
    sizan = SizanGozlem(dugum=0, topo=Topoloji.uret(kon, Akislar(1)))
    tipler = [tip for _, tip in _yuzeyi_gez(sizan)]
    assert any(t in YASAK_TIPLER for t in tipler), (
        "tarama kasten eklenen sızıntıyı yakalamadı — test bir şey ölçmüyor"
    )


# ==========================================================================
# Ç5.2 — YÜZEY, BELGEYLE BİREBİR
# ==========================================================================

def test_c5_2_gozlem_alanlari_izinli_listeyle_ayni():
    alanlar = {a.name for a in dataclasses.fields(Gozlem)}
    assert alanlar == set(IZINLI_GOZLEM_ALANLARI), (
        f"fazla: {alanlar - IZINLI_GOZLEM_ALANLARI}, "
        f"eksik: {IZINLI_GOZLEM_ALANLARI - alanlar}"
    )


def test_c5_2b_komsu_ve_paket_alanlari_izinli():
    assert {a.name for a in dataclasses.fields(KomsuKaydi)} == set(IZINLI_KOMSU_ALANLARI)
    assert {a.name for a in dataclasses.fields(PaketGorunumu)} == set(IZINLI_PAKET_ALANLARI)


def test_c5_2c_paket_dogum_zamani_gorunmuyor():
    """Saatler senkron değil: `dogum_s` başka bir düğümde anlamsızdır.

    Ölçüm tarafı bilir, protokol bilemez. Bu ayrım korunmalı.
    """
    assert "dogum_s" not in IZINLI_PAKET_ALANLARI
    assert "teslim_s" not in IZINLI_PAKET_ALANLARI


def test_c5_2d_gozlem_dondurulmus():
    """Protokol gözlemi DEĞİŞTİREMEZ."""
    g = _bir_gozlem()
    with pytest.raises(Exception):
        g.dugum = 99          # type: ignore[misc]


# ==========================================================================
# Ç5.3 — KOMŞULUK YALNIZCA BEACON'DAN
# ==========================================================================

def test_c5_3_t0_da_komsu_tablosu_bos():
    """🔴 Başlangıç koşulu: hiçbir düğüm hiçbir komşusunu bilmez."""
    k = Kosu(Konfig(kol="t", senaryo="S0", tohum=1), en_kisa_yol)
    assert all(len(t) == 0 for t in k.komsu_tablosu.values())
    g = k._gozlem_uret(0, None)
    assert g.komsular == ()


def test_c5_3b_komsuluk_beaconla_ogreniliyor():
    """Beacon aktıkça komşu sayısı geometrik dereceye yaklaşmalı."""
    k = Kosu(Konfig(kol="t", senaryo="S0", tohum=1), en_kisa_yol)
    s = k.kostur()
    assert s["ort_komsu_sayisi"] == pytest.approx(
        s["topoloji"]["ortalama_derece"], rel=0.05), (
        s["ort_komsu_sayisi"], s["topoloji"]["ortalama_derece"])


def test_c5_3c_karistirma_beacon_kaybettiriyor():
    """Karıştırma altında beacon kaybolmalı — komşuluk bedava değil."""
    s0 = Kosu(Konfig(kol="t", senaryo="S0", tohum=1), en_kisa_yol).kostur()
    s2 = Kosu(Konfig(kol="t", senaryo="S2", tohum=1), en_kisa_yol).kostur()
    oran0 = s0["beacon_alinan"] / s0["beacon_gonderilen"]
    oran2 = s2["beacon_alinan"] / s2["beacon_gonderilen"]
    assert oran2 < oran0, (oran0, oran2)


@icerik_testi("komsular")
def test_c5_3d_komsuluk_menzil_tablosundan_turetilmiyor():
    """🔴 Menzil içindeki bir düğüm, beacon'ı duyulmadıkça komşu DEĞİLDİR.

    Bu, gözlem penceresinin en kolay ihlal edilen maddesi: menzil tablosunu
    protokole vermek karıştırmanın en temel etkisini iptal eder.

    🔴 19 AĞUSTOS 2026 — BU TEST YANLIŞ NESNEYE BAKIYORDU (K-037/B-21).

    Önceki hâli `k.komsu_tablosu`yu denetliyordu. Ama protokol o tabloyu
    GÖRMEZ; gördüğü şey `_gozlem_uret` tarafından kurulan `Gozlem.komsular`
    demetidir. Komşuluğu menzil tablosundan türeten mutasyon (M7) tam olarak
    `_gozlem_uret` içinde yaşıyor ve bu testi HİÇ KIRMIYORDU — test
    "yakalandı" sayılıyordu çünkü BAŞKA iki test kırılıyordu.

    `03` B3: *"metrik gerçekten onu mu ölçüyor?"* Sözleşme, protokolün
    gördüğü yüzey hakkındadır; denetim de orada yapılmalıdır.
    """
    k = Kosu(Konfig(kol="t", senaryo="S0", tohum=1), en_kisa_yol)
    k._beaconlari_basla()
    k.olaylar.kostur(0.05)          # ilk beacon fazlarından bile önce
    for d in range(k.kon.dugum_sayisi):
        geometrik = set(k.topo.geometrik_komsular(d))

        # 🔴 ASIL DENETİM: protokolün eline geçen yüzey
        gorulen = {x.dugum for x in k._gozlem_uret(d, None).komsular}
        assert gorulen < geometrik or not geometrik, (
            f"düğüm {d}: GÖZLEMDEKİ komşular menzil tablosuna eşit — "
            f"komşuluk türetiliyor (kâhin)"
        )

        # İkinci savunma hattı: iç tablo da türetilmemiş olmalı
        ogrenilen = set(k.komsu_tablosu[d])
        assert ogrenilen < geometrik or not geometrik, (
            f"düğüm {d}: öğrenilen komşular menzil tablosuna eşit — "
            f"komşuluk türetiliyor olabilir"
        )


# ==========================================================================
# Gözlem penceresi bir protokol yazmaya YETİYOR mu?
# ==========================================================================

def test_saf_gozlem_protokolu_kosabiliyor():
    """Kâhin hiçbir bilgi kullanmayan bir protokol koşabilmeli.

    Yetmiyorsa pencere fazla dar demektir ve bu, ölçümü değil TASARIMI
    kısıtlar. Protokolün İYİ olması gerekmiyor — koşması gerekiyor.
    """
    k = Kosu(Konfig(kol="t", senaryo="S2", tohum=1), gurultuden_kacan)
    s = k.kostur()
    assert k.defter.kontrol()["korunum_tamam"] is True
    assert s["pencerede_teslim"] > 0, "hiç paket teslim edilemedi"


# ==========================================================================
# 🔴 BAĞIMSIZ DENETİM REGRESYONLARI (19 Ağustos 2026)
#
# Aşağıdaki iki test, sıfır bağlamlı bir denetçinin bulduğu iki gerçek
# kâhin sızıntısının regresyonudur. İkisi de 198 testlik paketten SAĞ
# ÇIKMIŞTI — yani sözleşme katmanı korumasızdı.
# ==========================================================================

@icerik_testi("gonderilen_bayt", "alinan_bayt")
def test_b01_bayt_alanlari_dugume_ait_aga_degil():
    """🔴 B-01 — `Gozlem` bayt alanları DÜĞÜMÜN KENDİ sayaçları olmalı.

    Önceki sürümde `self.mac.veri_bayt` / `kontrol_bayt` bağlıydı; bunlar
    AĞ GENELİ toplam sayaçlar. Gerçek bir telsizin ölçemeyeceği bir
    büyüklük doğrudan protokolün eline geçiyordu (kural 5).

    Denetçi 7344 kararın 7343'ünde gözlemdeki değerin düğümün kendi
    baytından büyük olduğunu ölçtü.
    """
    k = Kosu(Konfig(kol="t", senaryo="S2", tohum=1), en_kisa_yol)
    k.kostur()

    # İki farklı düğümün gözlemi FARKLI değer vermeli
    gozlemler = [k._gozlem_uret(d, None) for d in range(k.kon.dugum_sayisi)]
    gonderilen = {g.gonderilen_bayt for g in gozlemler}
    alinan = {g.alinan_bayt for g in gozlemler}
    assert len(gonderilen) > 1, (
        "tüm düğümler aynı 'gönderilen bayt' değerini görüyor — ağ geneli sayaç"
    )
    assert len(alinan) > 1, (
        "tüm düğümler aynı 'alınan bayt' değerini görüyor — ağ geneli sayaç"
    )

    # Ve hiçbiri ağ toplamına eşit olmamalı
    assert max(gonderilen) < k.mac.veri_bayt + k.mac.kontrol_bayt
    # Düğüm toplamları ağ toplamıyla tutarlı olmalı
    assert sum(k.mac.dugum_gonderilen_bayt) == pytest.approx(
        k.mac.veri_bayt + k.mac.kontrol_bayt)


@icerik_testi("son_iletim_hedefi", "son_iletim_sonucu")
def test_b02_son_iletim_hedefi_gercek_komsuyu_tasiyor():
    """🔴 B-02 — `son_iletim_hedefi` sabit −1 OLAMAZ.

    `05` §B, bağ kalitesi için TEK bir kanala izin veriyor: "yalnızca kendi
    denemelerinden çıkardığı tahmin". Hedef taşınmazsa protokol "onay geldi"
    bilgisini alır ama HANGİ komşuya ait olduğunu bilemez — yani o kanal
    fiilen kapalıdır ve Aile 2'nin tazelik hipotezi yazılamaz.
    """
    hedefler, sonuclar = set(), set()

    def izleyen_fabrika(kon):
        ic = en_kisa_yol(kon)

        def sonraki(g):
            if g.son_iletim_hedefi is not None:
                hedefler.add(g.son_iletim_hedefi)
            if g.son_iletim_sonucu is not None:
                sonuclar.add(g.son_iletim_sonucu)
            return ic(g)
        return sonraki

    Kosu(Konfig(kol="t", senaryo="S2", tohum=1), izleyen_fabrika).kostur()

    assert hedefler - {-1}, f"son_iletim_hedefi hiç gerçek düğüm taşımadı: {hedefler}"
    assert len(hedefler) > 2, f"yalnızca {len(hedefler)} farklı hedef görüldü"
    assert sonuclar == {"onay", "zaman_asimi"}, sonuclar


def test_b02b_alici_kabul_etse_bile_gonderen_zaman_asimi_gorur():
    """🔴 Gönderenin gördüğü şey, GERÇEKTE olan değil.

    Yeniden deneme hakkı bitip alıcı paketi kabul etmişse, defter paketi
    teslim/aktarım olarak sayar — ama gönderen ONAY GÖRMEMİŞTİR. Gözleme
    "onay" yazmak simülatörün bilgisini sızdırmak olurdu.
    """
    from sim.mac import KanalErisimi
    kayit = []

    kon = Konfig(kol="t", senaryo="S2", tohum=1, yeniden_deneme_siniri=1)
    k = Kosu(kon, en_kisa_yol)
    asil = k._gonderim_bitti

    def izle(paket, gonderen, hedef, sonuc):
        kayit.append(sonuc)
        asil(paket, gonderen, hedef, sonuc)

    k.mac.gonderim_bitti = izle
    k.kostur()
    assert "zaman_asimi" in kayit, (
        "alıcı kabul edip onay kaybolduğu hâlde gönderen hiç zaman aşımı görmedi"
    )


# ==========================================================================
# 🔴 B-27b — HER GÖZLEM ALANININ İÇERİK TESTİ
#
# İkinci bağımsız denetim: dört alanın ne tüketicisi ne içerik testi vardı.
# `kanal_mesgul_mu` → sabit `False` ve `kuyruk_uzunlugu` → sabit `0`
# mutasyonları 240/240 test geçiyordu.
#
# Aşağıdaki testler her alanın değerini **bağımsız hesaplanmış** gerçek
# büyüklükle karşılaştırır — üretici ifadeyi tekrar etmezler.
# ==========================================================================

def _icerik_testi_olan() -> set[str]:
    """İşaretleyicilerden TÜRETİLMİŞ kapsam — çalışma anında toplanır."""
    kapsanan: set[str] = set()
    for ad, nesne in list(globals().items()):
        if ad.startswith("test_") and callable(nesne):
            kapsanan |= getattr(nesne, "_gozlem_alanlari", frozenset())
    return kapsanan


def test_b43_kapsam_ISARETLEYICIDEN_turuyor_ve_bos_degil():
    """🔴 Y7 — türetme bozulursa aşağıdaki kontrol `0 == 0`a düşer.

    `_icerik_testi_olan()` boş dönseydi, "her alanın testi var" kontrolü
    bütün alanları eksik sanardı; her şeyi kapsayan bir küme dönseydi hiçbir
    şeyi sormazdı. İkisi de sessiz olurdu.
    """
    kapsanan = _icerik_testi_olan()
    assert kapsanan, "hiçbir test işaretleyici taşımıyor — türetme bozuk"
    assert "kanal_mesgul_mu" in kapsanan


def test_b43_ISARETLEYICI_silininde_koruma_KONUSUYOR(monkeypatch):
    """🔴 Y11 — korumanın kapsamı DIŞINDA kalan vaka: markör kaybı.

    Eski elle yazılmış küme bu vakayı **tanım gereği** göremezdi: test
    silinse bile küme yerinde kalırdı. Burada bir işaretleyiciyi kaldırıp
    korumanın gerçekten konuştuğunu ÖLÇÜYORUZ.
    """
    monkeypatch.delattr(test_b27b_kanal_mesgul_mu_bagimsiz_hesapla_ayni,
                        "_gozlem_alanlari")
    assert "kanal_mesgul_mu" not in _icerik_testi_olan(), (
        "işaretleyici kaldırıldı ama kapsam değişmedi — türetme sahte")


# 🔴 B-99: `icerik_testi` çıplak alan ADI alıyor; iki kümede birden geçen
# bir ad hangi kümeyi kapsadığını söylemiyor. ÖLÇÜLDÜ, tek ad:
_BELIRSIZ_ALAN_CIFTLERI = {
    ("Gozlem", "KomsuKaydi"): frozenset({"dugum"}),
    ("Gozlem", "PaketGorunumu"): frozenset(),
    ("KomsuKaydi", "PaketGorunumu"): frozenset(),
}


def test_b27b_her_gozlem_alaninin_icerik_testi_var():
    """🔴 "Bildirim ≠ kullanım" — gözlem sözleşmesi için.

    `IZINLI_GOZLEM_ALANLARI`ndaki her alan ya bu dosyada **işaretlenmiş** bir
    içerik testine bağlıdır, ya `gozlem.HENUZ_ICERIK_TESTI_OLMAYAN`da beyan
    edilir. Gelecekte eklenen bir alan da bu ikisinden birine düşmek zorunda.
    """
    from sim import gozlem as gz

    # 🔴 B-99: kural ÜÇ kümeye birden uygulanıyor. Öncesinde yalnızca
    # `Gozlem`e uygulanıyordu ve `KomsuKaydi`nin 7 + `PaketGorunumu`nun 5
    # alanı kuralın DIŞINDAYDI — `duyulan_beacon` sabitlenince 367 test
    # görmüyordu (mutasyon X04).
    isaretli = _icerik_testi_olan()
    for kume_adi, alanlar, beyan in (
            ("IZINLI_GOZLEM_ALANLARI", gz.IZINLI_GOZLEM_ALANLARI,
             gz.HENUZ_ICERIK_TESTI_OLMAYAN),
            ("IZINLI_KOMSU_ALANLARI", gz.IZINLI_KOMSU_ALANLARI,
             gz.HENUZ_ICERIK_TESTI_OLMAYAN_KOMSU),
            ("IZINLI_PAKET_ALANLARI", gz.IZINLI_PAKET_ALANLARI,
             gz.HENUZ_ICERIK_TESTI_OLMAYAN_PAKET)):
        kapsanan = isaretli | set(beyan)
        eksik = set(alanlar) - kapsanan
        assert not eksik, (
            f"{kume_adi}: şu alanların ne içerik testi ne beyanı var: "
            f"{sorted(eksik)}. Bir alanın değerinin doğru olduğunu gösteren "
            f"hiçbir kayıt yoksa, onu ilk okuyan protokol doğrulanmamış bir "
            f"sayı kullanır (B-27b · B-99).")
        fazla = set(beyan) - set(alanlar)
        assert not fazla, (
            f"{kume_adi}: artık var olmayan alanlar beyanda: {sorted(fazla)}")

    # 🔴 İŞARETLEYİCİNİN ÖLÇÜLMÜŞ SINIRI (B-99): `icerik_testi` ÇIPLAK alan
    # ADI alıyor. İki kümede birden geçen bir ad, hangi kümeyi kapsadığını
    # SÖYLEMİYOR. Ölçüldü: bugün tek belirsiz ad `dugum`
    # (`Gozlem` ∩ `KomsuKaydi`). Aşağıdaki assert, listenin BÜYÜMESİNİ
    # yakalar — yeni bir belirsiz ad çıkarsa işaretleyici ad-uzaylı hâle
    # getirilmelidir.
    # ⚠️ ÇİFT BAZINDA ölçülüyor: yalnızca adların KÜMESİNE bakmak yetmez —
    # aynı ad YENİ bir çiftte belirsizleşirse küme değişmez ve nöbetçi
    # susar. (Mutasyonla ölçüldü: küme bazlı ilk hâli SAĞ KALDI.)
    olculen_belirsiz = {
        ("Gozlem", "KomsuKaydi"): frozenset(
            set(gz.IZINLI_GOZLEM_ALANLARI) & set(gz.IZINLI_KOMSU_ALANLARI)),
        ("Gozlem", "PaketGorunumu"): frozenset(
            set(gz.IZINLI_GOZLEM_ALANLARI) & set(gz.IZINLI_PAKET_ALANLARI)),
        ("KomsuKaydi", "PaketGorunumu"): frozenset(
            set(gz.IZINLI_KOMSU_ALANLARI) & set(gz.IZINLI_PAKET_ALANLARI)),
    }
    assert olculen_belirsiz == _BELIRSIZ_ALAN_CIFTLERI, (
        "birden çok kümede geçen alan adları DEĞİŞTİ. ölçülen: %r · "
        "beyan: %r. `icerik_testi` ÇIPLAK ad kullandığı için bu adlarda "
        "hangi kümenin kapsandığı BELİRSİZDİR; liste büyüyorsa "
        "işaretleyici ad-uzaylı yapılmalıdır (B-99)."
        % ({k: sorted(v) for k, v in olculen_belirsiz.items()},
           {k: sorted(v) for k, v in _BELIRSIZ_ALAN_CIFTLERI.items()}))

    _BELIRSIZ = frozenset().union(*_BELIRSIZ_ALAN_CIFTLERI.values())

    # 🔴 Y8/Y11 — KURAL BEYANA ÇÖKTÜRÜLEMEZ.
    # İlk yazımda buradaki nöbetçi *"en az bir alanın içerik testi olmalı"*
    # diyordu ve MUTASYONDAN SAĞ ÇIKTI: üç test edilen alan beyana eklenince
    # nöbetçi susuyordu, çünkü testler hâlâ duruyordu. Doğru değişmez şu:
    # **beyan "HENÜZ testi yok" demektir**; test edilen bir alanı beyana
    # koymak listeyi anlamsızlaştırır ve gerçek boşlukları gizler.
    for kume_adi, alanlar, beyan in (
            ("IZINLI_GOZLEM_ALANLARI", gz.IZINLI_GOZLEM_ALANLARI,
             gz.HENUZ_ICERIK_TESTI_OLMAYAN),
            ("IZINLI_KOMSU_ALANLARI", gz.IZINLI_KOMSU_ALANLARI,
             gz.HENUZ_ICERIK_TESTI_OLMAYAN_KOMSU),
            ("IZINLI_PAKET_ALANLARI", gz.IZINLI_PAKET_ALANLARI,
             gz.HENUZ_ICERIK_TESTI_OLMAYAN_PAKET)):
        celiski = (set(beyan) & isaretli) - _BELIRSIZ
        assert not celiski, (
            f"{kume_adi}: {sorted(celiski)} hem BEYAN edilmiş hem içerik "
            f"testi VAR. Beyan *'henüz testi yok'* demektir; test edilen bir "
            f"alanı beyana koymak kuralı beyana çöktürür ve gerçek "
            f"boşlukları gizler (B-99).")

    assert isaretli & set(gz.IZINLI_KOMSU_ALANLARI), (
        "`KomsuKaydi`nin HİÇBİR alanının içerik testi yok — kuralın "
        "genişletilmesi yalnızca beyandan ibaret kalmış (B-99).")


def test_b89_isaretleyici_PROZAYI_koddan_ayirt_ediyor(tmp_path):
    """🔴 B-89 — alan adı yalnızca PROZADA geçen bir test işaretlenemez.

    B-76 işaretleyiciyi *"gövdeyi çalışma anında doğruluyor"* diye
    düzeltmişti; ama gövde `inspect.getsource` METNİYDİ ve **docstring ile
    yorum satırları da gövdeye dâhildi.**

    ⚖️ B-68 **aynı oturumda** şunu yazmıştı: *"bir kaynak denetimi prozayı
    koddan ayırt edemiyorsa ölçüt değildir — AST'ye bağlandı."* B-76'nın
    düzeltmesi o dersi kendi içine uygulamamıştı.

    🔴 Y11 — B-76'nın KENDİ negatif kontrolü bu ekseni sınamıyordu: gövdesi
    `return 42` olan bir test kullanıyordu — ne docstring'i ne yorumu vardı.
    Koruma *"hiç geçmeyen"* vakayla sınanmış, *"yalnızca prozada geçen"*
    vakayla sınanmamıştı.
    """
    import importlib
    import sys as _sys

    satirlar = ['from tests.test_gozlem import icerik_testi', '', '', 'def yalnizca_docstring():', "    @icerik_testi('son_iletim_sonucu')", '    def sahte():', '        "`son_iletim_sonucu` alanini dogruladigini SOYLUYOR."', '        assert 1 == 1', '    return sahte', '', '', 'def yalnizca_yorum():', "    @icerik_testi('kanal_mesgul_mu')", '    def sahte2():', '        # kanal_mesgul_mu  <- yalnizca YORUMDA', '        assert 1 == 1', '    return sahte2', '', '', 'def gercek_kod():', "    @icerik_testi('kuyruk_uzunlugu')", '    def sahte3():', "        g = {'kuyruk_uzunlugu': 3}", "        assert g['kuyruk_uzunlugu'] == 3", '    return sahte3']
    (tmp_path / "b89_prova.py").write_text(
        chr(10).join(satirlar) + chr(10), encoding="utf-8")

    _sys.path.insert(0, str(tmp_path))
    try:
        _sys.modules.pop("b89_prova", None)
        prova = importlib.import_module("b89_prova")

        for ad, fn in (("yalnızca DOCSTRING", prova.yalnizca_docstring),
                       ("yalnızca YORUM", prova.yalnizca_yorum)):
            with pytest.raises(AssertionError):
                fn()

        # 🔴 Y11 — SINIRIN İÇİ GEÇMELİ, yoksa koruma her şeyi reddediyordur
        assert (prova.gercek_kod()._gozlem_alanlari
                == frozenset({"kuyruk_uzunlugu"}))
    finally:
        _sys.path.remove(str(tmp_path))
        _sys.modules.pop("b89_prova", None)


@icerik_testi("duyulan_beacon", "bildirdigi_gurultu_w")
def test_b99_komsu_kaydi_BAGIMSIZ_sayimla_ayni():
    """🔴 B-99 — `KomsuKaydi`nin içeriği bağımsız bir sayımla doğrulanıyor.

    Beşinci denetim ölçtü: `duyulan_beacon` sabit `1` yapıldığında gözlem
    penceresi parmak izi DEĞİŞTİ ve **367 testin 367'si geçti** (X04).
    B-27b'nin *"her alanın içerik testi olmak zorunda"* kuralı yalnızca
    `Gozlem`e uygulanıyordu; `KomsuKaydi` kuralın DIŞINDAYDI.

    Burada beacon alımları MAC yolundan bağımsız olarak sayılıyor ve komşu
    kaydının kendi sayacıyla karşılaştırılıyor.
    """
    sayac: dict = {}
    son_gurultu: dict = {}
    k = Kosu(Konfig(kol="t", senaryo="S2", trafik="orta", tohum=1),
             en_kisa_yol)
    asil = k.mac.yayin_alindi

    def izle(gonderen, alan, icerik):
        anahtar = (alan, gonderen)
        sayac[anahtar] = sayac.get(anahtar, 0) + 1
        son_gurultu[anahtar] = icerik["gurultu_w"]
        return asil(gonderen, alan, icerik)

    k.mac.yayin_alindi = izle
    k.kostur()

    # Y8 — kurulum anlamlı mı: beacon gerçekten alınıyor mu
    assert len(sayac) > 20, (
        f"yalnızca {len(sayac)} komşu çifti beacon aldı — test zayıf (Y7)")

    for alan, tablo in k.komsu_tablosu.items():
        for gonderen, kayit in tablo.items():
            beklenen = sayac.get((alan, gonderen))
            assert kayit.duyulan_beacon == beklenen, (
                f"🔴 düğüm {alan}, komşu {gonderen}: `duyulan_beacon` "
                f"{kayit.duyulan_beacon} diyor ama bağımsız sayım "
                f"{beklenen}. Alan sabitlenmiş olabilir (B-99 · X04).")
            assert kayit.bildirdigi_gurultu_w == son_gurultu[(alan, gonderen)], (
                f"düğüm {alan}, komşu {gonderen}: `bildirdigi_gurultu_w` "
                f"son beacon'ın taşıdığı değer değil")

    # 🔴 Y10 — DEĞİŞMEZ KIRILABİLİR Mİ: sayaç sabit 1 OLMAMALI, yoksa
    # `duyulan_beacon == 1` mutasyonu ayırt edilemez.
    en_buyuk = max(kayit.duyulan_beacon
                   for tablo in k.komsu_tablosu.values()
                   for kayit in tablo.values())
    assert en_buyuk > 1, (
        "hiçbir komşudan birden çok beacon alınmamış — bu koşuda "
        "`duyulan_beacon = 1` mutasyonu AYIRT EDİLEMEZ (Y8)")


@icerik_testi("kanal_mesgul_mu")
def test_b27b_kanal_mesgul_mu_bagimsiz_hesapla_ayni():
    """`kanal_mesgul_mu` gerçekten taşıyıcı dinlemeyi mi söylüyor?

    BAĞIMSIZ HESAP: `mac.aktif`ten, CS komşuluğu ve CCA gecikmesi elle
    uygulanarak. `mac.kanal_mesgul()` çağrılmaz — çağrılsaydı üretici
    ifadeyi tekrar etmiş olurdum.
    """
    kon = Konfig(kol="t", senaryo="S2", trafik="yogun", tohum=1)
    k = Kosu(kon, en_kisa_yol)

    gorulen = {True: 0, False: 0}
    ilk = k.protokol

    def izleyen(g):
        simdi = k.olaylar.simdi
        beklenen = any(
            il.gonderen != g.dugum
            and il.gonderen in k.mac.cs_komsu[g.dugum]
            and il.baslangic_s + kon.cca_s <= simdi
            for il in k.mac.aktif
        )
        assert g.kanal_mesgul_mu is beklenen, (
            f"t={simdi}: gözlem {g.kanal_mesgul_mu}, bağımsız hesap {beklenen}"
        )
        gorulen[beklenen] += 1
        return ilk(g)

    k.protokol = izleyen
    k.kostur()

    # Y8 — her iki değer de fiilen görülmeli, yoksa test bir şey ölçmüyor
    assert gorulen[True] > 100 and gorulen[False] > 100, gorulen


@icerik_testi("kuyruk_uzunlugu", "kuyruk_kapasitesi")
def test_b27b_kuyruk_alanlari_bagimsiz_sayimla_ayni():
    """`kuyruk_uzunlugu` gerçekten kuyruktaki paket sayısı mı?

    BAĞIMSIZ SAYIM: defterdeki paket nesnelerinden, `len(kuyruk)` yerine.
    """
    kon = Konfig(kol="t", senaryo="S2", trafik="yogun", tohum=1)
    k = Kosu(kon, en_kisa_yol)
    ilk = k.protokol
    dolu_gorulen = [0]

    def izleyen(g):
        gercek = sum(1 for p in k.kuyruklar[g.dugum]._paketler
                     if p is not None)
        assert g.kuyruk_uzunlugu == gercek, (g.kuyruk_uzunlugu, gercek)
        assert g.kuyruk_kapasitesi == kon.kuyruk_kapasitesi
        assert 0 <= g.kuyruk_uzunlugu <= g.kuyruk_kapasitesi
        if g.kuyruk_uzunlugu > 1:
            dolu_gorulen[0] += 1
        return ilk(g)

    k.protokol = izleyen
    k.kostur()
    assert dolu_gorulen[0] > 50, (
        f"kuyruk hiç dolmadı ({dolu_gorulen[0]}) — alan sabit 0 olsa da "
        f"test geçerdi (Y8)"
    )


@icerik_testi("saat_s")
def test_b27b_saat_gecmise_gitmiyor_ve_olay_zamani():
    """`saat_s` düğümün kendi saati — olay zamanıyla aynı ve monoton.

    ⚠️ `08` madde 13: kodda TEK küresel saat var; "senkron değil" yalnızca
    disiplinle sağlanıyor. Bu test o gerçeği **koruyor değil, kaydediyor**:
    bugün saatler aynı, ve bir protokol zaman damgası taşırsa o kolun
    sonucu geçersizdir.
    """
    kon = Konfig(kol="t", senaryo="S2", tohum=1)
    k = Kosu(kon, en_kisa_yol)
    ilk = k.protokol
    onceki = [-1.0]

    def izleyen(g):
        assert g.saat_s == k.olaylar.simdi
        assert g.saat_s >= onceki[0], "saat geriye gitti"
        onceki[0] = g.saat_s
        return ilk(g)

    k.protokol = izleyen
    k.kostur()
    assert onceki[0] > kon.isinma_s, onceki[0]


# ==========================================================================
# 🔴 B-44 + B-43(b) — LİSTEDE OLUP TESTİ OLMAYAN ÜÇ ALAN
#
# Üçüncü bağımsız denetim: `olculen_gurultu_w` ve `paket`, içerik testi
# olduğu İDDİASIYLA listedeydi; `grep -rn "olculen_gurultu_w" tests/`
# yalnızca kümenin kendi satırını buluyordu. Ve U14 — `Gozlem`in gürültü
# alanını sabit tabana bağlayan mutasyon — **284/284 testten sağ çıktı.**
# ==========================================================================

@icerik_testi("olculen_gurultu_w")
def test_b44_olculen_gurultu_karistiriciyi_ve_mesafeyi_TASIYOR():
    """🔴 U14: alanı sabit tabana bağlayan mutasyon 284/284 geçiyordu.

    BAĞIMSIZ HESAP — `mac.olculen_gurultu_w` çağrılmaz (üretici ifade o).
    Yalnızca iki fiziksel değişmez kullanılır:

      (a) Karıştırıcı yokken ve hiçbir iletim aktif değilken alan **tam
          olarak** taban gürültüye eşittir; asla altına inmez.
      (b) Karıştırıcı varken, karıştırıcıya YAKIN düğümlerin gördüğü
          ortalama, UZAK düğümlerinkinden büyüktür.

    Sabit bir taban (a)'yı geçer ama (b)'de iki ortalamayı eşitler.
    """
    import math

    # ---- (a) S0: karıştırıcı yok
    k0 = Kosu(Konfig(kol="t", senaryo="S0", tohum=1), en_kisa_yol)
    olculen0: list[float] = []
    ilk0 = k0.protokol
    k0.protokol = lambda g: (olculen0.append(g.olculen_gurultu_w), ilk0(g))[1]
    k0.kostur()
    taban_w = k0.radyo.gurultu_gucu_w

    assert olculen0, "hiç karar üretilmedi — test bir şey ölçmüyor"
    assert min(olculen0) == taban_w, (
        f"S0'da en düşük ölçüm {min(olculen0)}, taban gürültü {taban_w}; "
        f"aktif iletim yokken alan tam tabana inmeli")
    assert min(olculen0) >= taban_w, "alan taban gürültünün ALTINA indi"

    # ---- (b) S2: karıştırıcı açık, mesafeye duyarlılık
    k2 = Kosu(Konfig(kol="t", senaryo="S2", tohum=1), en_kisa_yol)
    per_dugum: dict[int, list[float]] = {}
    ilk2 = k2.protokol

    def izle2(g):
        per_dugum.setdefault(g.dugum, []).append(g.olculen_gurultu_w)
        return ilk2(g)

    k2.protokol = izle2
    k2.kostur()

    jx, jy = k2.karistirici.konum_t(0.0)
    uzaklik = {d: math.hypot(k2.topo.konumlar[d][0] - jx,
                             k2.topo.konumlar[d][1] - jy)
               for d in per_dugum}
    sirali = sorted(uzaklik, key=uzaklik.get)
    n = len(sirali) // 3
    assert n >= 3, f"yeterli düğüm yok: {len(sirali)}"
    yakin, uzak = sirali[:n], sirali[-n:]

    # Y8 — iki grup da yeterince karar üretmeli, yoksa ortalama anlamsız
    ky = sum(len(per_dugum[d]) for d in yakin)
    ku = sum(len(per_dugum[d]) for d in uzak)
    assert ky > 50 and ku > 50, f"karar sayısı yetersiz: yakın={ky} uzak={ku}"

    # 🔴 (b1) ALAN SABİT OLAMAZ — en doğrudan ölçüt.
    # ⚠️ Y10: bu satırın ilk yazımında yalnızca `ort_y > ort_u` vardı ve
    # U14'ü YAKALAMIYORDU. Sabit bir alanda iki ortalama matematiksel olarak
    # EŞİTTİR, ama farklı sayıda terim toplandığı için son basamakta
    # yuvarlama farkı kalır ve `>` tesadüfen True dönebilir — ölçüldü,
    # tam olarak bu oldu. Bir yaklaşık-eşitlik/sıralama iddiası, KIRILABİLİR
    # olduğu gösterilmeden yazılamaz.
    farkli = len({v for L in per_dugum.values() for v in L})
    assert farkli > 1, (
        f"gözlem gürültüsü koşu boyunca TEK bir değer aldı ({farkli}); "
        f"alan karıştırıcıyı da girişimi de taşımıyor. "
        f"(Sağlam koşuda ölçülen: 275 farklı değer.)")

    ort_y = sum(sum(per_dugum[d]) for d in yakin) / ky
    ort_u = sum(sum(per_dugum[d]) for d in uzak) / ku
    taban = k2.radyo.gurultu_gucu_w
    assert ort_y > taban and ort_u > taban, (
        f"karıştırıcı açıkken ortalamalar taban gürültüde: "
        f"yakın={ort_y:.3e} uzak={ort_u:.3e} taban={taban:.3e}")

    # 🔴 (b2) MESAFEYE DUYARLILIK — MARJLI.
    # Marj fiziksel: karıştırıcı gücü d^(-α) ile düşer (α ≈ 3) ve yakın/uzak
    # üçte birlerin mesafe oranı büyüktür; fark %20'nin çok üstünde OLMAK
    # ZORUNDA. Eşik bugünkü değerden türetilmedi — kayan nokta gürültüsünün
    # (~1e-16 göreli) çok üstünde, ölçülen değerin (1,787 kat) altında
    # seçildi ki sürüklenme görünür kalsın.
    assert ort_y > ort_u * 1.2, (
        f"karıştırıcıya yakın düğümler ({uzaklik[yakin[0]]:.0f}–"
        f"{uzaklik[yakin[-1]]:.0f} m) ortalama {ort_y:.3e} W görüyor; "
        f"uzaktakiler ({uzaklik[uzak[0]]:.0f}–{uzaklik[uzak[-1]]:.0f} m) "
        f"{ort_u:.3e} W — oran {ort_y/ort_u:.3f}, en az 1,2 bekleniyor. "
        f"Alan karıştırıcıyı ya da mesafeyi taşımıyor.")


@icerik_testi("paket")
def test_b43_paket_gorunumu_GERCEK_paketi_tasiyor():
    """`PaketGorunumu`nun beş alanı gerçek paketin karşılığı mı?

    BAĞIMSIZ HESAP: karar anında kuyruk başındaki **gerçek paket nesnesi**
    ile alan alan karşılaştırılır. Eşleme yanlış olsaydı (ör. `hedef=kaynak`)
    hiçbir mevcut test bunu görmezdi — kimse alanların DEĞERİNİ sormuyordu.

    Ayrıca `kimlik` ve `dogum_s`in görünüme SIZMADIĞI burada da doğrulanır.
    """
    k = Kosu(Konfig(kol="t", senaryo="S2", trafik="orta", tohum=1), en_kisa_yol)
    sayac = {"n": 0}
    ilk = k.protokol

    def izle(g):
        gercek = k.kuyruklar[g.dugum].bak()
        assert g.paket is not None and gercek is not None
        assert g.paket.hedef == gercek.hedef
        assert g.paket.kaynak == gercek.kaynak
        assert g.paket.ttl == gercek.ttl
        assert g.paket.atlama_sayisi == gercek.atlama_sayisi
        assert g.paket.bayt == gercek.bayt
        assert not hasattr(g.paket, "kimlik")
        assert not hasattr(g.paket, "dogum_s")
        sayac["n"] += 1
        return ilk(g)

    k.protokol = izle
    k.kostur()
    # Y8 — aktarılan paketler olmalı, yoksa eşleme hiç sınanmamış olur
    assert sayac["n"] > 1000, f"yalnızca {sayac['n']} karar görüldü"


@icerik_testi("dugum")
def test_b43_dugum_alani_KARAR_VERILEN_dugumu_tasiyor():
    """`dugum`, gözlemin ait olduğu düğüm mü?

    BAĞIMSIZ HESAP: gözlemi üreten çağrının kendi düğüm numarasıyla
    karşılaştırılır. `_gozlem_uret` sarmalanarak, ÜRETİCİNİN argümanı
    gözlemin alanıyla eşleştirilir.
    """
    k = Kosu(Konfig(kol="t", senaryo="S2", tohum=1), en_kisa_yol)
    asil = k._gozlem_uret
    sayac = {"n": 0}

    def sarmal(dugum, paket):
        g = asil(dugum, paket)
        assert g.dugum == dugum, f"gözlem {g.dugum}, üretici {dugum}"
        sayac["n"] += 1
        return g

    k._gozlem_uret = sarmal
    k.kostur()
    assert sayac["n"] > 1000, f"yalnızca {sayac['n']} gözlem üretildi"


# ==========================================================================
# 🔴 A-4 — ARAYÜZÜN KENDİSİNDEN GELEN KÂHİN KANALI
#
# Üçüncü bağımsız denetim §ANLAŞILMAYANLAR: *"`protokol_fabrikasi` koşu
# başına TEK BİR çağrılabilir üretiyor ve o çağrılabilir 40 düğümün hepsi
# için çalışıyor. Bunun bir bulgu mu yoksa bilinçli bir tasarım mı olduğunu
# belirleyemedim."*
#
# Yapısal olarak doğrulandı ve bir BULGUDUR: bir protokol, kapanışında
# tuttuğu bir sözlüğe düğüm A'nın gördüğünü yazıp düğüm B'nin kararında
# okuyabilirdi. Gerçek bir telsizde karşılığı olmayan, bedava ve kusursuz
# bir düğümler arası kanal — `03` kural 5'in tam hedefi.
#
# `08` Ç5 KAPSAMAZ tablosu yalnızca MODÜL global'lerini beyan ediyordu.
# ==========================================================================

def test_a4_her_dugum_KENDI_protokol_ornegini_aliyor():
    """Bir protokol kapanışı, düğümler arasında bilgi taşıyabiliyor mu?

    BAĞIMSIZ ÖLÇÜM: fabrika her çağrıldığında yeni bir küme yaratır ve o
    örnek hangi düğümler için karar verdiyse onları yazar. İzolasyon varsa
    **her örnek tek bir düğüm görür.**

    Tek bir örnek paylaşılsaydı, o örnek karar veren BÜTÜN düğümleri
    görürdü — ve gördüğü şeyi bir sonraki kararda kullanabilirdi.
    """
    ornek_gorduleri: list[set[int]] = []

    def izole_fabrika(kon):
        gordugu: set[int] = set()
        ornek_gorduleri.append(gordugu)

        def sonraki(g):
            gordugu.add(g.dugum)
            if not g.komsular:
                return None
            return min(k.dugum for k in g.komsular)

        return sonraki

    kon = Konfig(kol="t", senaryo="S2", tohum=1)
    k = Kosu(kon, izole_fabrika)
    k.kostur()

    assert len(ornek_gorduleri) == kon.dugum_sayisi, (
        f"fabrika {len(ornek_gorduleri)} kez çağrıldı, {kon.dugum_sayisi} "
        f"düğüm var. Tek bir örnek paylaşılıyorsa düğümler arası kapanış "
        f"kanalı AÇIKTIR."
    )

    karar_verenler = [x for x in ornek_gorduleri if x]
    # Y8 — birden çok düğüm fiilen karar vermeli, yoksa test bir şey ölçmüyor
    assert len(karar_verenler) > 1, (
        f"yalnızca {len(karar_verenler)} örnek karar verdi — izolasyon "
        f"iddiası sınanmamış olur")

    coklu = [x for x in karar_verenler if len(x) != 1]
    assert not coklu, (
        f"{len(coklu)} protokol örneği birden çok düğüm için karar verdi: "
        f"{[sorted(x) for x in coklu[:3]]}. Düğümler arası kâhin kanalı açık.")

    # Farklı örnekler farklı düğümlere ait olmalı
    sahipler = [next(iter(x)) for x in karar_verenler]
    assert len(set(sahipler)) == len(sahipler), (
        "iki örnek aynı düğüme bakıyor — sevk edici yanlış eşliyor")


# ==========================================================================
# 🔴 B-47 — PROTOKOLÜN ÇERÇEVEYE BİLGİ KOYMA HAKKI
#
# `05` §A2 bu hakkı veriyordu; 20 Ağustos'a kadar KOD KARŞILIĞI YOKTU.
# Üçüncü bağımsız denetim ölçtü: beacon içeriği simülatör tarafından
# sabitlenmişti, `PaketGorunumu` donmuş 5 alandı, ve protokolün yazabildiği
# tek yer (`protokol_teshis`) iletilmiyordu. Saf gözlemle yazılan bir ETX
# protokolü S0'da 0,0997 teslim ve **1,00 ortalama atlama** veriyordu —
# ön-kaydın iki rakip protokolü de kurulamıyordu.
#
# Kanca: `protokol.beacon_yuku(dugum) -> dict | None`
# ==========================================================================

def _yuklu_fabrika(yuk_uret):
    """Kancası olan bir protokol fabrikası — kararı en yakın komşuya verir."""
    def fabrika(kon):
        def sonraki(g):
            if not g.komsular:
                return None
            return min(k.dugum for k in g.komsular)
        sonraki.beacon_yuku = yuk_uret
        return sonraki
    return fabrika


def test_b47_protokol_BEACONA_alan_koyabiliyor():
    """Yük komşuya ULAŞIYOR mu — ve doğru düğümden mi geliyor?

    BAĞIMSIZ ÖLÇÜM: her düğüm kendi kimliğini yüke yazar; alıcı tarafta
    `bildirdigi_yuk` içindeki kimlik, kaydın `dugum` alanıyla eşleşmeli.
    Eşleşmiyorsa yük ya taşınmıyor ya yanlış komşuya yazılıyor.
    """
    k = Kosu(Konfig(kol="t", senaryo="S0", tohum=1),
             _yuklu_fabrika(lambda d: {"kim": d, "etx": 1.5}))
    k.kostur()

    gorulen = 0
    for alan, tablo in k.komsu_tablosu.items():
        for gonderen, kayit in tablo.items():
            yuk = dict(kayit.bildirdigi_yuk)
            assert yuk, f"düğüm {alan}, komşu {gonderen}: yük boş geldi"
            assert yuk["kim"] == gonderen, (
                f"yük düğüm {yuk['kim']}'den görünüyor ama kayıt "
                f"{gonderen}'e ait")
            assert yuk["etx"] == 1.5
            gorulen += 1

    # Y8 — yük yolu fiilen tetiklenmeli
    assert gorulen > 100, f"yalnızca {gorulen} komşu kaydı görüldü"


def test_b47_yuk_BAYTA_mal_oluyor():
    """`05` §A2 kural 1: *"başlıktaki her alan BAYT OLARAK SAYILIR."*

    BAĞIMSIZ HESAP: alan başına maliyet tel biçiminden elle hesaplanır
    (`yuk_bayt` çağrılmaz — üretici ifade o), ve iletilen beacon sayısıyla
    çarpılıp sonuç sözlüğüyle karşılaştırılır.
    """
    from sim.gozlem import yuk_bayt as _yb

    # 🔴 B-66 (K-056): bedel artık TİPE değil BOYUTA bağlı.
    #   "etx"(3) + float(4) + "derece"(6) + int 6 → 1 bayt  = 14
    # Eski biçim 10 diyordu (alan başına sabit 1 + 4) ve bir alan adında
    # 100 000 bayt taşımaya izin veriyordu.
    alan_basi = _yb({"etx": 1.25, "derece": 6})
    assert alan_basi == 14, f"beklenen 14, ölçülen {alan_basi}"

    # 🔴 ÇAĞRI ANINDA ÖLÇÜM — çapraz koşu karşılaştırması DEĞİL.
    # İlk yazımda bu test iki AYRI PROTOKOLÜN sonuç sözlüklerini
    # karşılaştırıyordu (`en_kisa_yol` vs yüklü) ve *"kontrol_bayt arttı"*
    # diyordu. İki koşu farklı evrenler olduğu için bu fark yükten de
    # gelebilirdi, protokol farkından da — `03` B1: **kontrol kolu olmadan
    # etki ölçmek**. Ölçüldü: yükün baytını çerçeveye EKLEMEYEN bir mutasyon
    # (M-F) o testten SAĞ ÇIKTI. Şimdi çerçeve boyutu, üretildiği yerde,
    # tek tek doğrulanıyor.
    kon = Konfig(kol="t", senaryo="S2", tohum=1)
    k = Kosu(kon, _yuklu_fabrika(lambda d: {"etx": 1.25, "derece": 6}))

    cagrilar: list[tuple[int, int]] = []
    asil = k.mac.yayin_gonder

    def izle(dugum, bayt, icerik, yuk_bayt=0):
        cagrilar.append((bayt, yuk_bayt))
        return asil(dugum, bayt, icerik, yuk_bayt)

    k.mac.yayin_gonder = izle
    yuklu = k.kostur()

    # Y8 — yayın yolu fiilen tetiklenmeli
    assert len(cagrilar) > 1000, f"yalnızca {len(cagrilar)} yayın üretildi"

    for bayt, yb in cagrilar:
        assert yb == alan_basi, f"yük baytı {yb}, beklenen {alan_basi}"
        assert bayt == kon.beacon_bayt + yb, (
            f"çerçeve {bayt} bayt, beklenen {kon.beacon_bayt} + {yb} = "
            f"{kon.beacon_bayt + yb}. 🔴 Yükün bedeli ÖDENMİYOR: `05` §A2 "
            f"kural 1 *(başlıktaki her alan bayt olarak sayılır)* ihlal "
            f"ediliyor ve protokol bedava bilgi taşıyor.")

    # Toplam sayaç İLETİLEN beacon'la tutarlı olmalı (üretilenle değil)
    assert yuklu["yuk_bayt_toplam"] == alan_basi * yuklu["beacon_gonderilen"], (
        f"yük baytı {yuklu['yuk_bayt_toplam']}, beklenen "
        f"{alan_basi * yuklu['beacon_gonderilen']}. 🔴 Sayaç İLETİLEN "
        f"beacon'la aynı olayda artmalı — üretilip eskiyen beacon havaya "
        f"çıkmaz, yükü de harcanmaz.")

    # Kancasız koşu hiç yük baytı saymamalı (kontrol kolu)
    assert Kosu(kon, en_kisa_yol).kostur()["yuk_bayt_toplam"] == 0


def test_b47_BOS_kanca_davranisi_DEGISTIRMIYOR():
    """Kancası olan ama boş dönen bir protokol, kancasızla BİREBİR aynı.

    🔴 Aile 0'ın bütün sayıları kancasız koşulardan geldi. Yük yolunun boş
    hâlde bile bir yan etkisi olsaydı *(fazladan bayt, kayan RNG çekimi)*,
    o sayıların hepsi sessizce geçersizleşirdi.
    """
    kon = Konfig(kol="t", senaryo="S2", tohum=1)

    def kancasiz(k):
        ic = en_kisa_yol(k)
        return lambda g: ic(g)

    def bos_kancali(k):
        ic = en_kisa_yol(k)
        def sonraki(g):
            return ic(g)
        sonraki.beacon_yuku = lambda d: None
        return sonraki

    a = Kosu(kon, kancasiz).kostur()
    b = Kosu(kon, bos_kancali).kostur()
    assert a == b, "boş kanca sonucu değiştiriyor — Aile 0'ın sayıları riskte"


def test_b47_SOZLESME_DISI_yuk_reddediliyor():
    """🔴 Y7/Y11 — koruma, kapsamı DIŞINDAKİ değerleri de reddetmeli.

    Mutlu yol yalnızca sayı taşıyor. Bir protokol beacon'a keyfi bir nesne
    koyabilseydi, hem kontrol yükü muhasebesi *(bedelsiz bilgi)* hem kâhin
    koruması *(nesne üzerinden simülatöre referans)* delinirdi.
    """
    from sim.gozlem import YukHatasi, yuk_bayt

    class Kotu:
        pass

    for kotu in ({"x": "metin"}, {"x": None}, {"x": Kotu()}, {"x": ()},
                 {"x": (1, "iki")}, {"": 1}, {"x": [1, 2]}, "sözlük değil"):
        with pytest.raises(YukHatasi):
            yuk_bayt(kotu)

    # Mutlu yol gerçekten geçiyor olmalı, yoksa koruma her şeyi reddediyordur
    assert yuk_bayt({"a": 1.0, "b": True, "v": (1.0, 2.0)}) > 0


@icerik_testi("bildirdigi_yuk")
def test_b47_yuk_BAYAT_ve_KAYBOLABILIR():
    """`05` §A2 kural 2 ve 3 — yük bayattır ve kaybolabilir.

    Beacon'la taşındığı için bu iki kural kendiliğinden geçerli. ÖLÇÜLÜR:
    karıştırma altında yükü hiç görülmemiş komşu çifti VARDIR, ve görülen
    yükün yaşı sıfırdan büyüktür.
    """
    sayac = {"n": 0}

    def artan(d):
        sayac["n"] += 1
        return {"sira": sayac["n"]}

    k = Kosu(Konfig(kol="t", senaryo="S2", trafik="yogun", tohum=1),
             _yuklu_fabrika(artan))
    s = k.kostur()

    # (a) Karıştırma altında beacon kaybı gerçek → kaçırılan yük var
    assert s["beacon_kacirilan"] > 0 or s["beacon_gonderilen"] < sayac["n"], (
        "karıştırma altında hiç beacon kaybolmamış — kurulum varsayımı yanlış")

    # (b) Taşınan yük BAYAT: kaydın yaşı > 0 olan komşu var
    bayat = 0
    for alan, tablo in k.komsu_tablosu.items():
        for kayit in tablo.values():
            if kayit.bildirdigi_yuk and kayit.yas_s(k.olaylar.simdi) > 0:
                bayat += 1
    assert bayat > 0, "hiçbir yük bayat değil — tazelik ölçümü anlamsız olur"


# ==========================================================================
# 🔴 B-66 (K-056) — BEDEL KAÇAĞI: TİP değil BOYUT
#
# `test_b47_SOZLESME_DISI_yuk_reddediliyor` sekiz kötü **TİP** deniyordu
# *(metin · None · nesne · boş demet · karışık demet · boş ad · liste ·
# sözlük değil)* ama **UZUNLUK/BÜYÜKLÜK eksenini hiç denemiyordu.**
# Dördüncü bağımsız denetim bu boşluktan girdi: 10 bayt bedelle 1 236 bayt
# taşıdı *(sentetik tavan 20 205×)*.
#
# ⚖️ Y11'in tam tanımı — ve Y11'i sağlamak için yazdığım testin İÇİNDE.
# ==========================================================================

@pytest.mark.parametrize("ad, yuk", [
    ("dürüst", {"etx": 1.5}),
    ("büyük int", {"a": 2 ** 8192}),
    ("uzun alan adı", {"z" * 100000: 0}),
    ("ikisi birden", {"z" * 100000: 2 ** 8192}),
    ("40'lık vektör", {"dv": tuple(float(i) for i in range(40))}),
    ("çok alan", {f"alan{i}": i for i in range(50)}),
    ("negatif büyük int", {"n": -(2 ** 4096)}),
    ("demet içinde büyük int", {"t": (1, 2 ** 2048)}),
])
def test_b66_odenen_bayt_TASINAN_BILGIDEN_kucuk_olamaz(ad, yuk):
    """🔴 DEĞİŞMEZ: ödenen ≥ taşınan. Kaçak yolu tek tek kapatılıyor.

    Bedel alan adının UTF-8 uzunluğunu ve tamsayının BÜYÜKLÜĞÜNÜ sayıyor.

    ⚠️ Y10 — BU DEĞİŞMEZ GEÇERLİ GİRDİDE HEP EŞİTLİKTİR (`odenen == tasinan`)
    ve bu **tasarım gereğidir**: tarife, taşınan bilgiyi tam karşılamalıdır.
    Değişmezin *kırılabilir* olduğu ayrı bir testte gösterilir —
    `test_b82_iki_hesap_GERCEKTEN_ayri`. O test olmadan bu satır `x >= x`tir
    (B-82, beşinci bağımsız denetim).
    """
    from sim.gozlem import _tasinan_bilgi_bayt, yuk_bayt

    odenen = yuk_bayt(yuk)
    tasinan = _tasinan_bilgi_bayt(yuk)
    assert odenen >= tasinan, (
        f"{ad}: {odenen} bayt ödeniyor, {tasinan} bayt taşınıyor "
        f"({tasinan/max(odenen,1):.0f}× kaçak)")


def test_b66_UZUN_ALAN_ADI_bedeli_gercekten_artiriyor():
    """Y8 — bedelin uzunlukla ARTTIĞI gösterilmeli, yoksa değişmez boştur."""
    from sim.gozlem import yuk_bayt

    kisa = yuk_bayt({"a": 1})
    uzun = yuk_bayt({"a" * 1000: 1})
    assert uzun - kisa == 999, (
        f"1000 karakterlik ad {uzun-kisa} bayt fazla ödedi, 999 beklenirdi")

    kucuk = yuk_bayt({"x": 1})
    buyuk = yuk_bayt({"x": 2 ** 8192})
    assert buyuk > kucuk * 100, (
        f"2**8192 yalnızca {buyuk} bayt ödedi (küçük int {kucuk}) — "
        f"tamsayı büyüklüğü faturalanmıyor")


def test_b66_KACAK_dogrudan_yakalaniyor(monkeypatch):
    """🔴 Y7 — `yuk_bayt`ın kaçak korumasının RAISE'i çalışıyor mu?

    ⚠️ 26 AĞUSTOS 2026 — BU TESTİN SINIRI ÖLÇÜLDÜ (B-82). Bu test
    `_tasinan_bilgi_bayt`ı **monkeypatch'liyor**, yani korumanın *sonucunu*
    zorluyor; korumanın **tetiklenebilir** olduğunu göstermiyor. Beşinci
    bağımsız denetim ölçtü: iki hesap aynı formülleri kullandığı için
    `yuk_bayt`ın kabul ettiği 105 943 girdinin **hiçbirinde** ateşlenemiyordu.

    🔴 Asıl Y11 kanıtı artık ayrı bir testte ve monkeypatch KULLANMIYOR:
    `test_b82_iki_hesap_GERCEKTEN_ayri` — orada bozulan şey **tarifedir**,
    ve ölçüm yolunun onu takip etmediği gösterilir.

    Bu test yine de duruyor: `raise` yolunun kendisini koruyor.
    """
    import sim.gozlem as gz
    from sim.gozlem import YukHatasi

    # alan adını yine sabit 1 bayt sayan bir "eski biçim" enjekte et
    monkeypatch.setattr(gz, "_tasinan_bilgi_bayt",
                        lambda yuk: 10 ** 6)          # taşınan çok büyük
    with pytest.raises(YukHatasi, match="BEDEL KAÇAĞI"):
        gz.yuk_bayt({"etx": 1.5})


# ==========================================================================
# 🔴 B-82 · B-83 (BEŞİNCİ DENETİM, 26 Ağustos 2026)
#
# B-66 iki hesap yazdı ve *"biri bozulunca diğeri konuşsun"* dedi. Ölçüldü:
# konuşamıyordu — ikisi aynı formülleri, aynı `_int_bayt`i ve aynı
# `YUK_FLOAT_BAYT`ı kullanıyordu. 105 943 kabul edilen girdide koruma
# **0 kez** ateşlenebiliyordu.
#
# Ve aynı körlük gerçek bir kaçağı saklıyordu: `float` 4 bayta faturalanıyor,
# gözlem penceresine **8 bayt** hâliyle giriyordu (2,00×).
# ==========================================================================


def test_b82_iki_hesap_GERCEKTEN_ayri():
    """🔴 Y11 — koruma, KAPSAMI DIŞINDAKİ bir vakayla sınanır.

    Burada monkeypatch YOKTUR. Bozulan şey **tarifedir**; `_tasinan_bilgi_bayt`
    ona dokunulmadan bırakılır. Ölçüm yolu tarifeyi takip etmiyorsa koruma
    konuşmak ZORUNDADIR.

    🔴 B-82'nin kanıtı bu üç vakadır: düzeltmeden ÖNCE üçü de SESSİZDİ.
    """
    import sim.gozlem as gz
    from sim.gozlem import YukHatasi

    # (a) yanlış alarm olmamalı — sağlam tarifede koruma SUSAR
    assert gz.yuk_bayt({"etx": 1.5}) == gz._tasinan_bilgi_bayt({"etx": 1.5})

    # (b) float tarifesi dejenere edilirse KONUŞMALI
    asil = gz.YUK_FLOAT_BAYT
    try:
        gz.YUK_FLOAT_BAYT = 1
        with pytest.raises(YukHatasi, match="BEDEL KAÇAĞI"):
            gz.yuk_bayt({"etx": 1.5})
    finally:
        gz.YUK_FLOAT_BAYT = asil

    # (c) int tarifesi dejenere edilirse KONUŞMALI
    asil_int = gz._int_bayt
    try:
        gz._int_bayt = lambda v: 1
        with pytest.raises(YukHatasi, match="BEDEL KAÇAĞI"):
            gz.yuk_bayt({"a": 2 ** 8192})
    finally:
        gz._int_bayt = asil_int

    # (d) sağlam tarife geri geldi mi — (b)/(c) kalıcı hasar bırakmasın
    assert gz.yuk_bayt({"etx": 1.5}) == gz._tasinan_bilgi_bayt({"etx": 1.5})


def test_b82_olcum_yolu_TARIFEYI_kullanmiyor():
    """🔴 B-82'nin YAPISAL koşulu: ölçüm yolu tarifeden hiç geçmemeli.

    Kaynak denetimi. `_tasinan_bilgi_bayt` ve çağırdığı yardımcılar
    `_int_bayt` ya da `YUK_FLOAT_BAYT` kullanırsa, iki hesap yeniden
    **aynı** olur ve koruma sessizce boşalır — hiçbir davranış testi
    bunu göremez.
    """
    import ast
    import inspect

    import sim.gozlem as gz

    YASAK = {"_int_bayt", "YUK_FLOAT_BAYT", "YUK_BOOL_BAYT",
             "YUK_INT_TABAN_BAYT"}
    for fn in (gz._tasinan_bilgi_bayt, gz._olculen_deger_bayt,
               gz._olculen_int_bayt):
        agac = ast.parse(inspect.getsource(fn))
        adlar = {d.id for d in ast.walk(agac) if isinstance(d, ast.Name)}
        adlar |= {d.attr for d in ast.walk(agac) if isinstance(d, ast.Attribute)}
        cakisma = adlar & YASAK
        assert not cakisma, (
            f"{fn.__name__} tarifeden geçiyor: {sorted(cakisma)}. "
            f"İki hesap ayrı olmazsa koruma `x >= x`e döner (B-82).")


def test_b83_float_TEL_BICIMINE_kirpiliyor():
    """🔴 B-83 — 4 bayt ödenen bir float, 8 bayt bilgi taşıyamaz.

    Ölçüldü (beşinci denetim): 8 KEYFİ bayt bir `float`a konup gözlem
    penceresinden **birebir** geri okunuyordu. Bedel 4, taşınan 8 → 2,00×.
    """
    import struct

    from sim.gozlem import _tasinan_bilgi_bayt, yuk_bayt, yuku_dondur

    ham = b"\xde\xad\xbe\xef\x01\x02\x03\x41"      # 8 keyfi bayt
    v = struct.unpack("<d", ham)[0]

    gelen = yuku_dondur({"a": v})[0][1]
    assert struct.pack("<d", gelen) != ham, (
        "8 keyfi bayt gözlem penceresinden BİREBİR geçiyor — kırpma yok, "
        "4 bayt bedelle 8 bayt bilgi taşınıyor (B-83)")

    # kırpılmış değer TEL BİÇİMİNE tam oturur
    assert gelen == struct.unpack("<f", struct.pack("<f", v))[0]

    # ve kaçak kapandı: ödenen == taşınan
    assert yuk_bayt({"a": v}) == _tasinan_bilgi_bayt({"a": v})

    # Y8 — kırpmanın GERÇEKTEN bir şey yaptığı gösterilir
    assert gelen != v, "kırpma bu değerde hiçbir şey değiştirmiyor"


def test_b83_tel_bicimine_SIGMAYAN_float_reddediliyor():
    """🔴 Y11 — kırpma bir bilgi kaybını SESSİZCE yapamaz.

    Tek duyarlığa sığmayan bir değer kırpılınca sonsuza taşar. O değer
    taşınamaz; yutulup 4 bayt faturalanamaz.
    """
    from sim.gozlem import YukHatasi, yuk_bayt

    for kotu in ({"x": 1e300}, {"x": -1e300}, {"v": (1.0, 1e39)}):
        with pytest.raises(YukHatasi, match="tel biçimine"):
            yuk_bayt(kotu)

    # sınırın İÇİ geçmeli, yoksa koruma her şeyi reddediyordur (Y11)
    assert yuk_bayt({"x": 3.0e38}) > 0
    assert yuk_bayt({"x": float("inf")}) > 0      # inf tek duyarlıkta VAR


# ==========================================================================
# 🔴 B-69 (K-056) — A-4'ÜN KAPATMADIĞI KANAL: FABRİKAYI SARAN KAPSAM
#
# A-4 *"tek çağrılabilir, 40 düğüm"* kanalını kapattı. Kapanmayan şey
# *"40 çağrılabilir, TEK PAYLAŞILAN DURUM"*: fabrikayı saran bir kapsamda
# yaratılan sözlük ne modül globalidir ne örneğe aittir — ve `test_a4_…`
# onu **göremez**, çünkü yalnızca "her örnek kaç düğüm gördü" sayıyor.
#
# ÖLÇÜLDÜ: paylaşılan bir sözlükte **14 düğümün** kendi anteninde ölçtüğü
# gürültü birikti ve komşu seçimi oradan yapıldı; `test_a4_…` yine GEÇTİ.
#
# ⚠️ Bu, Aile 1 için en doğal Python desenidir — bu yüzden yasak değil,
# **görünür** kılınıyor: kapanış hücreleri taranıyor.
# ==========================================================================

# --------------------------------------------------------------------------
# 🔴 B-86 (BEŞİNCİ DENETİM, 26 Ağustos 2026) — TARAMA DÖRT KANALDAN ÜÇÜNÜ
#    GÖREMİYORDU VE SINIF TABANLI BİR PROTOKOLDE ÇÖKÜYORDU.
#
# `08:194` dört kanal beyan ediyor: *"modül global'i · fabrikayı saran kapsam
# · **sınıf özniteliği** · fabrikanın kendi `__dict__`i"*. Eski tarama
# yalnızca `prot.__closure__` içindeki `dict/list/set`e bakıyordu — yani
# **birini.** Ve protokol bir SINIF ÖRNEĞİ olduğunda `AttributeError` ile
# **çöküyordu** — oysa o biçim deponun kendi davet ettiği biçim
# (`kosucu.py` kancaları `getattr(prot, "beacon_yuku")` ile okuyor).
#
# Denetçi ölçtü: örnek özniteliğiyle kurulan bir kanal, referans `dict`
# kanalıyla **birebir aynı teslim oranını** veriyordu (0,07857672…) — yani
# aynı düğümler arası bilgi kanalı çalışıyordu — ve tarama **sıfır** diyordu.
#
# 🔒 YENİ TARAMA — ölçüldü (K-065): denetçinin DÖRT vakasının DÖRDÜ de
# yakalanıyor, hiçbiri çökmüyor, ve bugünkü `AKTARICILAR`da **yanlış alarm
# yok.** İkisi birden şart: fazla dar bir tarama kanalı kaçırır, fazla geniş
# bir tarama yanlış alarm verir ve kimse ona bakmaz.
# --------------------------------------------------------------------------

_ESLEME_TIPLERI = (dict, types.MappingProxyType)
_YAZILABILIR_TIPLER = (dict, list, set, bytearray)
# 🔴 B-101 (ALTINCI DENETİM) — DERİNLİK SINIRI KALDIRILDI.
#
# Burada `_TARAMA_DERINLIGI = 3` vardı: **elle seçilmiş, ölçümden
# türetilmemiş** bir sabit. Denetçi derinlik 4'te bir düğümler arası
# yazılabilir kanal kurdu — her düğüm KENDİ sarmallarını kuruyor, paylaşılan
# tek şey en içteki sözlük — ve tarama **8/8 yapılandırmada 0 dedi**, oysa
# kanal sonucu değiştiriyordu *(teslim farkı −0,0149…+0,2040)*. Gerçek bir
# telsizde karşılığı olmayan, bedava ve kusursuz bir kanal (`03` kural 5).
#
# Sabiti YENİDEN TAHMİN ETMEK aynı kusuru bir adım öteye taşırdı. Ölçüldü
# (27 Ağu): sınırsız tarama gerçek bir protokolde **0,0 ms** sürüyor
# *(ulaşılabilir yazılabilir nesne: 0)*, ve gömme derinliği ≥ 4 olan bir
# kanalda sınırsız tarama **kesinlikle daha fazlasını** görüyor:
#
#     gömme 4 → derinlik 3: 4 paylaşılan  ·  SINIRSIZ: 5
#     gömme 8 → derinlik 3: 4 paylaşılan  ·  SINIRSIZ: 9
#
# Üretici: `python scratchpad/b101_derinlik.py`
#
# 🔴 SINIR ARTIK MALİYETTE, GÖRÜŞTE DEĞİL: gezilen nesne sayısı bir tavanı
# aşarsa tarama **susmaz, PATLAR**. Sessiz bir kör nokta, gürültülü bir
# sınıra çevrildi.
_TARAMA_TAVANI = 200_000


def _cocuk_nesneler(x):
    """Bir nesneden ULAŞILABİLEN alt nesneler — sınırlı ve öngörülebilir."""
    if isinstance(x, dict):
        yield from x.values()
    elif isinstance(x, (list, tuple, set, frozenset)):
        yield from x
    else:
        d = getattr(x, "__dict__", None)
        # 🔴 Bir SINIFIN `__dict__`i `mappingproxy`dir, `dict` DEĞİL —
        # `isinstance(d, dict)` sınıf özniteliklerini KAÇIRIR (A vakası).
        if isinstance(d, _ESLEME_TIPLERI):
            yield from d.values()


def _ulasilan_yazilabilir(kok, derinlik: int | None = None) -> dict:
    """`kok`tan ulaşılan YAZILABİLİR nesneler: `id -> nesne`.

    🔴 B-101: `derinlik` VARSAYILAN OLARAK YOKTUR — tarama, görülen nesne
    kümesi tükenene kadar sürer. Parametre yalnızca **ölçüm** için duruyor
    (derinlik 3 ile sınırsızı karşılaştırmak gibi); üretimde verilmez.
    """
    bulunan: dict[int, object] = {}
    gorulen: set[int] = set()
    yigin = [(kok, 0)]
    while yigin:
        x, d = yigin.pop()
        if (derinlik is not None and d > derinlik) or id(x) in gorulen:
            continue
        gorulen.add(id(x))
        # 🔴 Sessiz kör nokta yerine GÜRÜLTÜLÜ sınır (B-101).
        if len(gorulen) > _TARAMA_TAVANI:
            raise AssertionError(
                f"paylaşım taraması {_TARAMA_TAVANI} nesneyi aştı — nesne "
                f"grafiği beklenenden büyük. Tarama SUSMAZ: ya tavan "
                f"ölçülüp büyütülür ya kapsam daraltılır, ama kör nokta "
                f"BEYAN EDİLİR (B-101).")
        if isinstance(x, _YAZILABILIR_TIPLER):
            bulunan[id(x)] = x
        if isinstance(x, (str, bytes, int, float, bool, type(None))):
            continue
        for c in _cocuk_nesneler(x):
            yigin.append((c, d + 1))
    return bulunan


def _protokol_kokleri(prot) -> list:
    """`08`in beyan ettiği DÖRT kanalın kökleri."""
    kokler = []
    # 1 · fabrikayı saran kapsam — düz fonksiyon VE bağlı metot
    for f in (prot, getattr(prot, "__call__", None),
              getattr(prot, "__func__", None)):
        for h in (getattr(f, "__closure__", None) or ()):
            try:
                kokler.append(h.cell_contents)
            except ValueError:
                pass
    # 2 · fabrikanın/örneğin kendi `__dict__`i   3 · sınıf özniteliği
    kokler.append(prot)
    if not isinstance(prot, type):
        kokler.append(type(prot))
    # 4 · protokolün kodunun ADIYLA andığı modül global'leri
    #     (hepsi değil: her fonksiyon `__globals__`ı paylaşır, tümünü
    #      taramak yanlış alarm fırtınası olurdu)
    cagrilan = getattr(prot, "__call__", prot)
    kod = getattr(cagrilan, "__code__", None) or getattr(prot, "__code__", None)
    gl = getattr(cagrilan, "__globals__", None) or {}
    if kod is not None:
        for ad in getattr(kod, "co_names", ()):
            if ad in gl:
                kokler.append(gl[ad])
    return kokler


def _paylasilan_mutable(kosu) -> list:
    """Protokol örneklerinin PAYLAŞTIĞI yazılabilir durum — DÖRT KANAL.

    Salt-okunur ve MEŞRU paylaşımlar *(aynı `Konfig`, topoloji, trafik,
    olay kuyruğu)* elenir — aksi hâlde kontrol yanlış alarm verir ve kimse
    ona bakmaz. Muafiyet, koşunun **kendi** nesnelerinden türetilir; elle
    yazılmış bir liste değildir (elle yazılan liste sessizce bayatlar).
    """
    muaf: set[int] = set()
    for k in (getattr(kosu, "kon", None), getattr(kosu, "topo", None),
              getattr(kosu, "trafik", None), getattr(kosu, "olaylar", None)):
        if k is not None:
            muaf |= set(_ulasilan_yazilabilir(k))

    gorulen: dict[int, int] = {}
    cakisan = []
    for dugum, prot in kosu._protokoller.items():
        bulunan: dict[int, object] = {}
        for kok in _protokol_kokleri(prot):
            bulunan.update(_ulasilan_yazilabilir(kok))
        for kimlik, nesne in bulunan.items():
            if kimlik in muaf:
                continue
            if kimlik in gorulen and gorulen[kimlik] != dugum:
                cakisan.append((gorulen[kimlik], dugum, type(nesne).__name__))
            gorulen.setdefault(kimlik, dugum)
    return cakisan


# ==========================================================================
# 🔴 B-87 (BEŞİNCİ DENETİM) — `teshis`İN SÖZLEŞMESİ YOKTU
#
# K-056/B-68: *"Kanca `beacon_yuku`nun deseniyle BİREBİR AYNI."* Değildi.
# `beacon_yuku` `yuk_bayt`tan geçip tipi/boyutu denetleniyor ve ihlalde
# ANINDA `YukHatasi` fırlatıyordu; `teshis` hiçbir denetimden geçmiyordu.
# Denetçi sekiz sözleşme dışı yük denedi: 8'i de kabul edildi, 4'ü sonuç
# yazıcısını koşu BİTTİKTEN SONRA düşürdü, biri `YASAK_TIPLER`den bir
# `Konfig` taşıdı.
# ==========================================================================


def _teshis_veren(fn):
    """`teshis` kancası taşıyan bir SINIF protokolü — deponun davet ettiği biçim."""
    class P:
        def __init__(self, kon):
            pass

        def __call__(self, g):
            return min((k.dugum for k in g.komsular), default=None)

        def teshis(self, dugum):
            return fn(dugum)
    return P


def test_b87_teshis_SOZLESMESI_sozlesme_disini_reddediyor():
    """🔴 B-87 — sözleşme, kardeşi `yuk_bayt` kadar sıkı mı?

    ⚠️ Bu test `teshis_dogrula`yı DOĞRUDAN çağırır — tam koşu YAPMAZ.
    İlk yazımında her kötü vaka bir tam koşuya mal oluyordu (ölçüldü:
    **224 sn**) ve paket mutasyon kapısında **35 kez** koşuyor. Pahalı bir
    koruma, kapıyı ödenemez kılar (Y12'nin dersi).
    """
    from sim.config import Konfig as _K
    from sim.gozlem import TeshisHatasi, teshis_dogrula

    kendini_iceren = []
    kendini_iceren.append(kendini_iceren)

    KOTU = [
        ("ANAHTAR int", {12345: 1}),
        ("ANAHTAR demet", {(1, 2): 1}),
        ("ANAHTAR boş dizgi", {"": 1}),
        ("ANAHTAR 1 MB dizgi", {"z" * 1_000_000: 1}),
        ("DEĞER 100k liste", {"buyuk": list(range(100_000))}),
        ("DEĞER serileştirilemez", {"nesne": object()}),
        ("DEĞER Konfig (YASAK_TIPLER)", {"kon": _K(kol="x")}),
        ("DEĞER kendini içeren liste", {"d": kendini_iceren}),
        ("DEĞER iç içe liste", {"d": [[1, 2]]}),
        ("DEĞER 257 baytlık dizgi", {"d": "u" * 257}),
        ("SÖZLÜK değil", [("a", 1)]),
        ("33 alan", {f"a{i}": i for i in range(33)}),
    ]
    for ad, veri in KOTU:
        with pytest.raises(TeshisHatasi):
            teshis_dogrula(0, veri)

    # 🔴 Y11 — TİP EKSENİNİN DIŞINDA: `nan` da bir `float`tır ve yalnızca
    # tipe bakan bir koruma onu KABUL EDER. `03` B2'nin NaN disiplini.
    for deger in (float("nan"), float("inf"), float("-inf")):
        with pytest.raises(TeshisHatasi, match="sonlu olmayan"):
            teshis_dogrula(0, {"x": deger})

    # 🔴 Y11 — SINIRIN İÇİ GEÇMELİ, yoksa koruma her şeyi reddediyordur
    for iyi in ({"karar": 3}, {"a" * 64: 1.5}, {"b": True}, {"c": "kısa"},
                {"v": (1, 2.0, "u")}, {"w": [1] * 64}, {}, None,
                {f"a{i}": i for i in range(32)}):
        teshis_dogrula(0, iyi)


def test_b87_ihlal_KOSU_SIRASINDA_patliyor_YAZMA_aninda_degil():
    """🔴 B-87'nin ASIL bulgusu: *"anında"*.

    Eski hâlde ihlal koşu **bittikten sonra** `SonucYazici`da ham bir
    `TypeError` ile patlıyordu — o noktada koşu **zaten harcanmıştı.**
    Bu test iki tam koşu yapar: biri ihlalin `kostur()` içinde patladığını,
    biri mutlu yolun slota GERÇEKTEN yazdığını gösterir (Y8).
    """
    from sim.gozlem import TeshisHatasi

    kon = Konfig(kol="t", senaryo="S0", tohum=1)

    with pytest.raises(TeshisHatasi):
        Kosu(kon, _teshis_veren(lambda d: {12345: d})).kostur()

    s = Kosu(kon, _teshis_veren(lambda d: {"karar": d})).kostur()
    assert s["protokol_teshis"].get("karar"), (
        "mutlu yol slota YAZMADI — sözleşme her şeyi reddediyor olabilir")
    assert len(s["protokol_teshis"]["karar"]) > 1, (
        "yalnızca tek düğüm yazmış — kanca tüm düğümlerde çağrılmıyor (Y8)")


def test_b86_tarama_DORT_KANALIN_HEPSINI_goruyor():
    """🔴 B-86 — `08:194`ün beyan ettiği DÖRT kanal da görülmeli.

    Eski tarama yalnızca `prot.__closure__` içindeki `dict/list/set`e
    bakıyordu ve sınıf tabanlı bir protokolde `AttributeError` ile
    **çöküyordu.** Denetçi ölçtü: örnek özniteliğiyle kurulan bir kanal,
    referans `dict` kanalıyla **birebir aynı** teslim oranını veriyordu —
    yani kanal ÇALIŞIYORDU — ve tarama *"paylaşım yok"* diyordu.

    ⚠️ Bu test tam koşu YAPMAZ: `Kosu` kurulumu `_protokoller`i doldurmaya
    yetiyor. Ucuz olması bilinçli — Y12'nin dersi.
    """
    from dogrulama.aktaricilar import AKTARICILAR

    class SinifProtokol:                      # A · SINIF ÖZNİTELİĞİ
        ORTAK: dict = {}

        def __init__(self, kon):
            pass

        def __call__(self, g):
            SinifProtokol.ORTAK[g.dugum] = g.olculen_gurultu_w
            return min((k.dugum for k in g.komsular), default=None)

    def bytearray_fabrikasi():                # B · bytearray
        ORTAK = bytearray(64)

        def fab(kon):
            def sec(g):
                ORTAK[g.dugum % 64] = min(255, g.kuyruk_uzunlugu)
                return min((k.dugum for k in g.komsular), default=None)
            return sec
        return fab

    def oznitelik_fabrikasi():                # C · ÖRNEK ÖZNİTELİĞİ
        class Kutu:
            pass
        ORTAK = Kutu()
        ORTAK.tablo = {}

        def fab(kon):
            def sec(g):
                ORTAK.tablo[g.dugum] = g.olculen_gurultu_w
                return min((k.dugum for k in g.komsular), default=None)
            return sec
        return fab

    def dict_fabrikasi():                     # REFERANS · kapanış hücresi
        ORTAK = {}

        def fab(kon):
            def sec(g):
                ORTAK[g.dugum] = g.olculen_gurultu_w
                return min((k.dugum for k in g.komsular), default=None)
            return sec
        return fab

    kon = Konfig(kol="t", senaryo="S2", tohum=1)
    for ad, fab in (("REFERANS · kapanış hücresi", dict_fabrikasi()),
                    ("A · sınıf özniteliği", SinifProtokol),
                    ("B · bytearray", bytearray_fabrikasi()),
                    ("C · örnek özniteliği", oznitelik_fabrikasi())):
        SinifProtokol.ORTAK = {}
        k = Kosu(kon, fab)
        try:
            cakisan = _paylasilan_mutable(k)
        except Exception as e:                # noqa: BLE001
            raise AssertionError(
                f"{ad}: tarama ÇÖKTÜ ({type(e).__name__}: {e}). Sınıf tabanlı "
                f"protokol deponun kendi davet ettiği biçimdir "
                f"(`kosucu.py` kancaları `getattr` ile okuyor).") from e
        assert cakisan, (
            f"{ad}: düğümler arası YAZILABİLİR paylaşım GÖRÜLMEDİ. "
            f"`08:194` bu kanalı beyan ediyor; tarama onu görmüyorsa beyan "
            f"kâğıtta kalır (B-86).")

    # 🔴 Y11 — KAPSAM DIŞI: tarama her şeye *"paylaşım var"* demiyor olmalı,
    # yoksa hiçbir şey doğrulamaz. Bugünkü aktarıcıların hepsi TEMİZ çıkmalı.
    for ad, fab in AKTARICILAR.items():
        temiz = _paylasilan_mutable(Kosu(kon, fab))
        assert not temiz, (
            f"{ad}: YANLIŞ ALARM — {temiz[:2]}. Fazla geniş bir tarama, "
            f"fazla dar bir tarama kadar işe yaramazdır.")

    # ----------------------------------------------------------------
    # 🔴 AŞAĞIDAKİ İKİ VAKA, Y2'NİN SAĞ BIRAKTIĞI İKİ MUTASYONDAN DOĞDU.
    # İlk yazımda burada TOTOLOJİK bir `assert` vardı (`x >= x` — B-82'nin
    # tam olarak eleştirdiği şey) ve iki kök hiç sınanmıyordu.
    # ----------------------------------------------------------------

    # (D) 🔴 `type(prot)` KÖKÜ — kapanış YOK, modül global'i YOK.
    #     Yukarıdaki A vakası sınıfın ADINI kapatıyor, bu yüzden kapanış
    #     hücresinden de bulunuyordu; bu vaka yalnızca `type(prot)` ile
    #     bulunabilir. Ölçüldü: `__call__.__closure__ is None`.
    class YalnizcaSinif:
        ORTAK: dict = {}

        def __init__(self, kon):
            pass

        def __call__(self, g):
            self.ORTAK[g.dugum] = 1           # `self` üzerinden
            return min((k.dugum for k in g.komsular), default=None)

    YalnizcaSinif.ORTAK = {}
    kk = Kosu(kon, YalnizcaSinif)
    prot0 = next(iter(kk._protokoller.values()))
    assert getattr(prot0.__call__, "__func__").__closure__ is None, (
        "kurulum varsayımı: bu sınıf hiçbir şeyi KAPATMAMALI, yoksa vaka "
        "`type(prot)` kökünü sınamaz (Y8)")
    assert _paylasilan_mutable(kk), (
        "D · yalnızca `self.ORTAK`: sınıf özniteliğiyle kurulan kanal "
        "GÖRÜLMEDİ. `type(prot)` kökü olmadan bu kanal görünmez (B-86).")

    # (E) 🔴 MUAFİYET GERÇEKTEN GEREKLİ Mİ — Y8.
    #     Ölçüldü: bugünkü beş aktarıcının HİÇBİRİ muafiyeti tetiklemiyor
    #     (kesişim 0/5). Tetiklenmeyen bir kontrol koruma sağlamaz, koruma
    #     İZLENİMİ verir. Tetikleyen vaka: `kon`u KAPATAN bir kol — ki bu,
    #     Aile 1'in yazacağı en doğal desendir (fabrika `kon` alır).
    def kon_kapatan(k_on):
        def sec(g):
            _ = k_on.senaryo                  # `kon` kapanış hücresinde
            return min((k.dugum for k in g.komsular), default=None)
        return sec

    kc = Kosu(kon, kon_kapatan)
    muaf = set()
    for x in (kc.kon, getattr(kc, "topo", None), getattr(kc, "trafik", None),
              getattr(kc, "olaylar", None)):
        if x is not None:
            muaf |= set(_ulasilan_yazilabilir(x))
    ulasilan = set()
    for _d, _prot in kc._protokoller.items():
        for _kok in _protokol_kokleri(_prot):
            ulasilan |= set(_ulasilan_yazilabilir(_kok))

    assert ulasilan & muaf, (
        "kurulum varsayımı: `kon`u kapatan bir kol muafiyeti TETİKLEMELİ, "
        "yoksa aşağıdaki değişmez boştur (Y8)")
    assert not _paylasilan_mutable(kc), (
        "E · `kon`u kapatan bir kol YANLIŞ ALARM verdi. `Konfig` her düğümde "
        "paylaşılır ve bu MEŞRUDUR; muafiyet olmadan tarama kullanılamaz "
        "hâle gelir — ve kimse ona bakmaz.")


def test_b69_dogrulama_aktaricilari_YAZILABILIR_durum_PAYLASMIYOR():
    """Bugünkü aktarıcıların hiçbiri örnekler arası yazılabilir durum paylaşmıyor.

    Ölçüldü: `en_kisa_yol` 40 ayrı önbellek sözlüğü yaratıyor *(paylaşılan 0)*;
    diğer dördünde mutable kapanış nesnesi hiç yok.
    """
    from dogrulama.aktaricilar import AKTARICILAR

    for ad, fab in AKTARICILAR.items():
        k = Kosu(Konfig(kol="t", senaryo="S2", tohum=1), fab)
        cakisan = _paylasilan_mutable(k)
        assert not cakisan, (
            f"{ad}: {len(cakisan)} yazılabilir nesne örnekler arasında "
            f"paylaşılıyor — düğümler arası kâhin kanalı ({cakisan[:3]})")


def test_b69_PAYLASAN_bir_fabrika_YAKALANIYOR():
    """🔴 Y11 — koruma, yakalaması gereken durumu GERÇEKTEN yakalıyor mu?

    Denetçinin yazdığı desenin birebir aynısı: fabrikayı saran bir sözlük.
    Bu test olmasaydı, yukarıdaki kontrol *"hiç paylaşım yok"* diye
    sessizce geçerdi ve hiçbir şey doğrulamazdı.
    """
    def paylasan_fabrika_yap():
        ORTAK: dict = {}                      # modül globali DEĞİL

        def fabrika(kon):
            def sonraki(g):
                ORTAK[g.dugum] = g.olculen_gurultu_w      # A yazar
                if not g.komsular:
                    return None
                gorunen = [k.dugum for k in g.komsular if k.dugum in ORTAK]
                if gorunen:                                # B okur
                    return min(gorunen, key=lambda d: ORTAK[d])
                return min(k.dugum for k in g.komsular)
            return sonraki
        return fabrika

    k = Kosu(Konfig(kol="t", senaryo="S2", tohum=1), paylasan_fabrika_yap())
    k.kostur()
    cakisan = _paylasilan_mutable(k)
    assert len(cakisan) >= 30, (
        f"paylaşılan sözlük yalnızca {len(cakisan)} çakışma üretti — "
        f"kontrol bu kanalı görmüyor olabilir")


def test_b76_isaretleyici_YANLIS_alani_reddediyor():
    """🔴 B-76 (K-056) — işaretleyici artık gövdeyi doğruluyor.

    Bir alan, gövdesinde adı hiç geçmeyen bir teste iliştirilmişti ve
    kapsam kontrolü onu *"kapsanmış"* sayıyordu. Etiketin elle taşınması
    (`03` B5) tam olarak burada oluyordu — B-43'ün düzeltmesinin İÇİNDE.
    """
    with pytest.raises(AssertionError, match="gövdesinde geçmiyor"):
        @icerik_testi("kanal_mesgul_mu")
        def sahte_test():
            return 42                      # alan adı gövdede YOK


def test_b76_isaretleyici_DOGRU_alani_kabul_ediyor():
    """Kontrol kolu: koruma her şeyi reddetmiyor."""
    @icerik_testi("kanal_mesgul_mu")
    def sahte_test():
        _ = "kanal_mesgul_mu"              # alan adı gövdede VAR
        return _

    assert sahte_test._gozlem_alanlari == frozenset({"kanal_mesgul_mu"})


# ==========================================================================
# 🔴 B-101 (ALTINCI DENETİM) — PAYLAŞIM TARAMASI DERİNLİK ≥4'TE KÖRDÜ
#
# `_TARAMA_DERINLIGI = 3` elle seçilmişti, ölçümden türetilmemişti.
# Denetçinin kurduğu kanal: her düğüm KENDİ sarmallarını kurar, paylaşılan
# tek şey EN İÇTEKİ sözlük. Düğümler kendi ölçtükleri gürültüyü oraya yazıp
# BAŞKALARININKİNİ okuyor — gerçek bir telsizde karşılığı olmayan, bedava
# ve kusursuz bir düğümler arası kanal (`03` kural 5).
#
#     gömme 0·1·2·3 → tarama 15 gördü   (16 düğüm yazıyor)
#     gömme 4·5     → tarama  0 gördü   🔴 ve kanal SONUCU DEĞİŞTİRİYOR
#                                        (teslim farkı −0,0149…+0,2040)
#
# ⚖️ Denetçinin kendi ilk denemesi BAŞARISIZ olmuştu: sarmalları ORTAK
# kurmuş, tarama onları derinlik 0'da görmüş ve KAZANMIŞTI. Sarmalların
# düğüm başına kurulması şart — aşağıdaki kurgu onu birebir izliyor.
# ==========================================================================

def _derin_kanal_fabrikasi(gomme: int):
    """Denetçinin kanalı: paylaşılan tek nesne EN İÇTEKİ sözlük.

    `fabrika` düğüm başına çağrılır (A-4), yani sarmallar düğüme ÖZELDİR;
    yalnızca `ortak` bütün düğümlerde aynı nesnedir.
    """
    ortak: dict = {}

    def fabrika(kon):
        kutu = ortak
        for _ in range(gomme):
            kutu = {"ic": kutu}        # bu düğüme ÖZEL sarmal
        dis = kutu

        def prot(g):
            k = dis
            for _ in range(gomme):
                k = k["ic"]
            k[g.dugum] = g.olculen_gurultu_w      # kendi ölçümünü YAZ
            return None
        return prot
    return fabrika


def _paylasilan_sayisi(fabrika, derinlik=None, dugum_sayisi: int = 4,
                       cagir: bool = True) -> int:
    """Kaç nesne BİRDEN FAZLA düğümün grafiğinde görünüyor.

    `cagir=False`: protokol ÇAĞRILMAZ, yalnızca fabrikanın kurduğu nesne
    grafiğine bakılır. Gerçek aktarıcılar tam bir `Gozlem` bekliyor ve
    paylaşım sorusu çağrıdan önce de sorulabilir.
    """
    kon = Konfig(kol="t", senaryo="S2", tohum=1)
    protokoller = [fabrika(kon) for _ in range(dugum_sayisi)]

    class _SahteGozlem:
        olculen_gurultu_w = 1e-12

        def __init__(self, dugum):
            self.dugum = dugum

    if cagir:
        for i, p in enumerate(protokoller):
            p(_SahteGozlem(i))         # kanalı FİİLEN kullan (Y8)

    sayilar: dict[int, int] = {}
    for p in protokoller:
        gorulen = set()
        for kok in _protokol_kokleri(p):
            # 🔴 `derinlik` VERİLMEZSE ÜRETİM YOLU (varsayılan) kullanılır.
            # ⚠️ İlk yazımı `derinlik`i her zaman AÇIKÇA geçiriyordu ve
            # varsayılanı hiç sınamıyordu: varsayılanı 3'e döndüren bir
            # mutasyon bu testten SAĞ ÇIKTI (Y2, M-G6). Bir koruma,
            # üretimin çağırdığı yoldan çağrılmak zorundadır (Y11).
            gorulen |= set(
                _ulasilan_yazilabilir(kok) if derinlik is None
                else _ulasilan_yazilabilir(kok, derinlik))
        for i in gorulen:
            sayilar[i] = sayilar.get(i, 0) + 1
    return sum(1 for v in sayilar.values() if v > 1)


def test_b101_DERINLIK_4_teki_kanal_ARTIK_GORULUYOR():
    """🔴 Elle seçilmiş derinlik sınırı kaldırıldı — kanal görünüyor.

    Y8: kanalın FİİLEN kullanıldığı gösteriliyor (her düğüm yazıyor).
    Y11: eski sınırın körlüğü de ölçülüyor — koruma yalnızca "şimdi
    görüyor" demiyor, "eskiden GÖRMÜYORDU" da diyor.
    """
    for gomme in (4, 6, 9):
        sinirsiz = _paylasilan_sayisi(_derin_kanal_fabrikasi(gomme))
        assert sinirsiz >= 1, (
            f"🔴 gömme {gomme}: düğümler arası paylaşılan nesne GÖRÜLMÜYOR "
            f"— tarama yine kör (B-101 · `03` kural 5)")

        # 🔴 Y11 — ESKİ SINIR bu kanalı KAÇIRIYORDU (ölçülerek gösteriliyor)
        eski = _paylasilan_sayisi(_derin_kanal_fabrikasi(gomme), derinlik=3)
        assert eski < sinirsiz, (
            f"gömme {gomme}: derinlik 3 ile sınırsız AYNI sonucu veriyor "
            f"({eski} vs {sinirsiz}) — bu kurgu B-101'i ayırt etmiyor, "
            f"testin kendisi zayıf (Y8)")


def test_b101_TEMIZ_protokolde_YANLIS_ALARM_yok():
    """🔴 Y11'in öteki yüzü: tarama her şeyi 'paylaşım' sanmamalı.

    Sınır kalkınca tarama daha çok nesne geziyor; gerçek bir aktarıcıda
    yanlış alarm üretirse Ç5 sebepsiz düşer (K-058'in sınıfı).
    """
    assert _paylasilan_sayisi(
        lambda kon: (lambda g: None)) == 0, (
        "durum tutmayan bir protokolde paylaşım bulundu — yanlış alarm")

    # 🔴 ÖLÇÜT "ULAŞILABİLİR Mİ" DEĞİL, "PAYLAŞILIYOR MU".
    #
    # ⚠️ Bu testin ilk yazımı *"hiçbir yazılabilir nesne ulaşılabilir
    # OLMAMALI"* diyordu ve KIRILDI: `en_kisa_yol` düğüm başına bir sözlük
    # tutuyor. Ölçüldü — iki düğüm için ayrı ayrı kurulup karşılaştırıldı:
    #
    #     en_kisa_yol      düğüm1=1  düğüm2=1  PAYLAŞILAN=0
    #     gurultuden_kacan düğüm1=0  düğüm2=0  PAYLAŞILAN=0
    #
    # Yani nesne düğüme ÖZEL — meşru bir yerel önbellek, kâhin kanalı değil.
    # `05` §A3 protokolün kendi geçmişini tutmasına zaten izin veriyor.
    # Kırılan kod değil, testin varsayımıydı (Y5).
    for fab in (gurultuden_kacan, en_kisa_yol):
        assert _paylasilan_sayisi(fab, cagir=False) == 0, (
            f"{fab.__name__}: düğümler ARASINDA paylaşılan yazılabilir nesne "
            f"bulundu — ya gerçek bir kâhin kanalı var ya tarama yanlış "
            f"alarm veriyor (`03` kural 5)")


def test_b101_TAVAN_SUSMAZ_patlar():
    """🔴 Sessiz kör nokta, GÜRÜLTÜLÜ sınıra çevrildi.

    Derinlik sınırı sessizce kesiyordu: tarama 0 der, kimse sebebini
    bilmez. Tavan aşılırsa tarama PATLAR — sebep görünür olur.
    """
    zincir: dict = {}
    uc = zincir
    for _ in range(50):
        yeni: dict = {}
        uc["ic"] = yeni
        uc = yeni

    g = globals()
    eski = g["_TARAMA_TAVANI"]
    try:
        g["_TARAMA_TAVANI"] = 10
        with pytest.raises(AssertionError, match="tarama"):
            _ulasilan_yazilabilir(zincir)
    finally:
        g["_TARAMA_TAVANI"] = eski

    # 🔴 Y8 — tavan GERÇEKTEN yüksekken aynı girdi sorunsuz geçmeli
    assert len(_ulasilan_yazilabilir(zincir)) == 51
