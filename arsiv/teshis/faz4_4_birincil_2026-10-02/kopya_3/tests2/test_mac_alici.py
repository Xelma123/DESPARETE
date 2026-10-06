"""
ADIM 6a — `mac/alici.py` kapanış ölçütleri.

Yol haritası:
    🔴 Çakışan iki çerçeveden **yalnız biri** alınıyor (sıfır ihlal).
    Her başarısız alım bir **sebep** taşıyor, `Σ sebep = toplam`.

Bu dosya iki kusuru bağlıyor:
  · **Kusur 2** — eski simülatörde bir düğüm zamanda çakışan İKİ çerçeveyi de
    başarıyla alabiliyordu; her alım bağımsız bir PER çekimiydi ve alıcının
    meşgul olup olmadığı hiç sorulmuyordu.
  · **Kusur 3** — capture effect / önbelge kilidi yoktu.
"""

from __future__ import annotations

import ast
import pathlib
import random
import sys

import pytest

KOK = pathlib.Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))
SIM2 = KOK / "sim2"

from sim2.cekirdek.degismezler import DegismezHatasi  # noqa: E402
from sim2.cekirdek.rng import Akislar  # noqa: E402
from sim2.dunya.topoloji import topoloji_kur  # noqa: E402
from sim2.kanal.cerceve import cerceve_kur  # noqa: E402
from sim2.kanal.girisim import Iletim  # noqa: E402
from sim2.kanal.kanal import Kanal  # noqa: E402
from sim2.mac.alici import (ALIM_SONUCLARI, DURUMLAR,  # noqa: E402
                            AliciZinciri, sonuc_dogrula)
from sim2.yapilandirma.konfig import Konfig  # noqa: E402


def _kur(senaryo="statik-yok", **ek):
    k = Konfig(kol="t", senaryo=senaryo, **ek)
    kanal = Kanal(k, topoloji_kur(k, Akislar(1)))
    return k, kanal


def _iletim(kanal, gonderen, bas_s, tip="veri"):
    return Iletim(gonderen=gonderen, cerceve=cerceve_kur(kanal.konfig, tip),
                  baslangic_s=bas_s, guc_w=kanal.yayilim.verici_gucu_w)


def _yakin_cift(kanal, t_s=0.0):
    """Menzil içi bir (gönderen, alıcı, ikinci_gönderen) üçlüsü."""
    a = kanal.topoloji.anlik(t_s)
    for i, komsular in enumerate(a.komsular):
        for j in komsular:
            for k in a.komsular[j]:
                if k not in (i, j):
                    return i, j, k
    raise AssertionError("uygun üçlü yok")


# ==========================================================================
# DURUM MAKİNESİ
# ==========================================================================

def test_baslangicta_BOS():
    k, kanal = _kur()
    z = AliciZinciri(0, k, kanal)
    assert z.durum == "bos"
    assert z.kilitli_iletim is None and z.gonderiyor is False


def test_YARIM_CIFT_gonderirken_alinamaz():
    """🔴 Tek radyolu telsizde gönderirken almak imkânsız."""
    k, kanal = _kur()
    i, j, _ = _yakin_cift(kanal)
    z = AliciZinciri(j, k, kanal)
    z.gonderime_basla()
    yeni, ezilen = z.cerceve_geldi(_iletim(kanal, i, 10.0), 10.0)
    assert yeni is not None and yeni.sebep == "alim_red_yari_cift"
    assert ezilen is None
    z.gonderim_bitti()
    assert z.gonderiyor is False


def test_gonderime_baslamak_KILIDI_dusuruyor():
    k, kanal = _kur(golgeleme_acik=False, sonumleme_acik=False)
    i, j, _ = _yakin_cift(kanal)
    z = AliciZinciri(j, k, kanal)
    z.cerceve_geldi(_iletim(kanal, i, 10.0), 10.0)
    assert z.kilitli_iletim is not None
    z.gonderime_basla()
    assert z.kilitli_iletim is None, "kendi iletimimiz kilidi bastırmalı"


def test_kendi_cercevesini_almak_REDDEDILIYOR():
    k, kanal = _kur()
    z = AliciZinciri(5, k, kanal)
    with pytest.raises(DegismezHatasi):
        z.cerceve_geldi(_iletim(kanal, 5, 1.0), 1.0)


def test_temiz_kanalda_KILITLENIP_ALIYOR():
    k, kanal = _kur(golgeleme_acik=False, sonumleme_acik=False)
    i, j, _ = _yakin_cift(kanal)
    z = AliciZinciri(j, k, kanal)
    it = _iletim(kanal, i, 10.0)
    yeni, ezilen = z.cerceve_geldi(it, 10.0)
    assert yeni is None and ezilen is None, "karar gövde bitince verilmeli"
    assert z.durum in ("onbelge_kilidi", "govde_aliyor")
    sonuc = z.cerceve_bitti(it, 10.0 + it.cerceve.sure_s)
    assert sonuc is not None and sonuc.sebep == "alim_basarili"
    assert z.durum == "bos"


def test_kilitlenmemis_cerceve_IKINCI_KEZ_sayilmiyor():
    """🔴 `cerceve_bitti` kilitli olmayan çerçeve için `None` dönmeli.

    Dönmeseydi, `cerceve_geldi`de zaten reddedilmiş bir çerçeve ikinci kez
    sayılır ve `Σ sebep = toplam` bozulurdu.
    """
    k, kanal = _kur()
    i, j, m = _yakin_cift(kanal)
    z = AliciZinciri(j, k, kanal)
    ilk = _iletim(kanal, i, 10.0)
    ikinci = _iletim(kanal, m, 10.0005)
    z.cerceve_geldi(ilk, 10.0)
    z.cerceve_geldi(ikinci, 10.0005)
    assert z.cerceve_bitti(ikinci, 10.0005 + ikinci.cerceve.sure_s) is None


# ==========================================================================
# 🔒 KAPANIŞ ÖLÇÜTÜ — ÇAKIŞAN İKİ ÇERÇEVEDEN YALNIZ BİRİ
# ==========================================================================

def test_CAKISAN_IKI_CERCEVEDEN_yalniz_biri(monkeypatch):
    """🔒 Kapanış ölçütünün birinci yarısı — sıfır ihlal.

    Eski simülatörde her alım bağımsız bir PER çekimiydi ve İKİSİ DE
    başarılı olabiliyordu. Burada bu yapısal olarak imkânsız.
    """
    k, kanal = _kur(golgeleme_acik=False, sonumleme_acik=False,
                    yakalama_etkisi_acik=False)
    i, j, m = _yakin_cift(kanal)
    ihlal = 0
    for n in range(300):
        z = AliciZinciri(j, k, kanal)
        t0 = 10.0 + 0.013 * n
        ilk = _iletim(kanal, i, t0)
        # ikinci çerçeve BİRİNCİNİN İÇİNDE başlıyor
        ikinci = _iletim(kanal, m, t0 + 0.3 * ilk.cerceve.sure_s)
        kanal.ortam.ekle(ilk)
        kanal.ortam.ekle(ikinci)
        sonuclar = []
        a1, _ = z.cerceve_geldi(ilk, ilk.baslangic_s)
        if a1:
            sonuclar.append(a1)
        a2, ezilen = z.cerceve_geldi(ikinci, ikinci.baslangic_s)
        for x in (a2, ezilen):
            if x:
                sonuclar.append(x)
        for it in (ilk, ikinci):
            r = z.cerceve_bitti(it, it.bitis_s)
            if r:
                sonuclar.append(r)
        basarili = sum(s.basarili for s in sonuclar)
        if basarili > 1:
            ihlal += 1
        assert len(sonuclar) == 2, "her çerçeve TAM BİR sonuç üretmeli"
        kanal.ortam.bitenleri_at(1e9)
    assert ihlal == 0, f"🔴 {ihlal} kez iki çerçeve de alındı"


def test_SEBEP_TOPLAMI_deneme_sayisina_esit():
    """🔒 Kapanış ölçütünün ikinci yarısı: `Σ sebep = toplam`.

    Sebep kümesi kapalı olduğu için toplamın denemeye eşit olmaması, bir
    denemenin ya hiç sayılmadığı ya İKİ KEZ sayıldığı anlamına gelir.
    """
    k, kanal = _kur("bagimsiz-yok")
    r = random.Random(4242)
    sayim = {s: 0 for s in ALIM_SONUCLARI}
    deneme = 0
    zincirler = {n: AliciZinciri(n, k, kanal) for n in range(k.dugum_sayisi)}

    for adim in range(400):
        t0 = 20.0 + 0.05 * adim
        a = kanal.topoloji.anlik(t0)
        gonderenler = [n for n in range(k.dugum_sayisi) if a.komsular[n]]
        if len(gonderenler) < 2:
            continue
        kanal.ortam.bitenleri_at(t0)
        secilen = r.sample(gonderenler, min(3, len(gonderenler)))
        iletimler = []
        for sira, g in enumerate(secilen):
            it = _iletim(kanal, g, t0 + sira * 0.0004)
            kanal.ortam.ekle(it)
            iletimler.append(it)
        for it in iletimler:
            for alici in a.komsular[it.gonderen]:
                z = zincirler[alici]
                deneme += 1
                yeni, ezilen = z.cerceve_geldi(it, it.baslangic_s)
                for s in (yeni, ezilen):
                    if s:
                        sayim[s.sebep] += 1
        for it in iletimler:
            for alici in a.komsular[it.gonderen]:
                s = zincirler[alici].cerceve_bitti(it, it.bitis_s)
                if s:
                    sayim[s.sebep] += 1

    assert deneme > 500, "test anlamlı olacak kadar deneme üretmeli"
    sonuc_dogrula(sayim, deneme)
    assert sum(sayim.values()) == deneme
    # her sebep en az bir kez görülmeli, yoksa o dal hiç sınanmamış demektir
    gorulmeyen = [s for s, n in sayim.items() if n == 0]
    assert gorulmeyen in ([], ["alim_red_yari_cift"]), (
        f"hiç görülmeyen sebep: {gorulmeyen}")


# ==========================================================================
# 🔴 KUSUR 3 — CAPTURE EFFECT
# ==========================================================================

def test_GUCLU_cerceve_zayifi_EZIYOR():
    """⚠️ İki çerçeve de KİLİTLENEBİLİR olmalı; aralarındaki fark yakalama
    eşiğini (10 dB) aşmalı.

    İlk yazımda zayıf çerçeve `Pt × 1e-3` idi ve önbelgeyi hiç
    kilitleyemiyordu — alıcı boşta kalıyor, yakalama dalı hiç koşmuyordu.
    Kurulum fiziksel olarak tutarsızdı: yakalama, kilitli bir çerçevenin
    ezilmesidir; kilitlenemeyen çerçeve zaten ezilecek bir şey değildir.
    """
    k, kanal = _kur(golgeleme_acik=False, sonumleme_acik=False)
    i, j, m = _yakin_cift(kanal)
    z = AliciZinciri(j, k, kanal)
    zayif = Iletim(gonderen=i, cerceve=cerceve_kur(k, "veri"),
                   baslangic_s=10.0, guc_w=kanal.yayilim.verici_gucu_w)
    z.cerceve_geldi(zayif, 10.0)
    assert z.kilitli_iletim is zayif
    guclu = Iletim(gonderen=m, cerceve=cerceve_kur(k, "veri"),
                   baslangic_s=10.00005, guc_w=kanal.yayilim.verici_gucu_w * 100.0)
    yeni, ezilen = z.cerceve_geldi(guclu, 10.00005)
    assert yeni is None, "güçlü çerçeve kilitlenmeli"
    assert ezilen is not None and ezilen.sebep == "alim_red_mesgul"
    assert ezilen.yakalama is True, "yakalama İŞARETİ konmalı"
    assert z.kilitli_iletim is guclu


def test_ZAYIF_cerceve_gucluyu_EZEMIYOR():
    k, kanal = _kur(golgeleme_acik=False, sonumleme_acik=False)
    i, j, m = _yakin_cift(kanal)
    z = AliciZinciri(j, k, kanal)
    guclu = Iletim(gonderen=i, cerceve=cerceve_kur(k, "veri"),
                   baslangic_s=10.0, guc_w=kanal.yayilim.verici_gucu_w * 100.0)
    z.cerceve_geldi(guclu, 10.0)
    zayif = Iletim(gonderen=m, cerceve=cerceve_kur(k, "veri"),
                   baslangic_s=10.00005, guc_w=kanal.yayilim.verici_gucu_w)
    yeni, ezilen = z.cerceve_geldi(zayif, 10.00005)
    assert yeni is not None and yeni.sebep == "alim_red_mesgul"
    assert ezilen is None
    assert z.kilitli_iletim is guclu


def test_YAKALAMA_PENCERESI_disinda_ezemiyor():
    """🔴 Pencere koşulu olmasaydı alıcı, neredeyse bitmiş bir gövdeyi bırakıp
    yeni bir önbelgeye geçer — gerçek alıcılar bunu yapmaz."""
    k, kanal = _kur(golgeleme_acik=False, sonumleme_acik=False)
    i, j, m = _yakin_cift(kanal)
    z = AliciZinciri(j, k, kanal)
    zayif = Iletim(gonderen=i, cerceve=cerceve_kur(k, "veri"),
                   baslangic_s=10.0, guc_w=kanal.yayilim.verici_gucu_w)
    z.cerceve_geldi(zayif, 10.0)
    gec = 10.0 + k.yakalama_penceresi_s * 2.0
    guclu = Iletim(gonderen=m, cerceve=cerceve_kur(k, "veri"),
                   baslangic_s=gec, guc_w=kanal.yayilim.verici_gucu_w * 100.0)
    yeni, ezilen = z.cerceve_geldi(guclu, gec)
    assert yeni is not None and yeni.sebep == "alim_red_mesgul"
    assert z.kilitli_iletim is zayif


def test_YAKALAMA_ABLASYONU():
    k, kanal = _kur(golgeleme_acik=False, sonumleme_acik=False,
                    yakalama_etkisi_acik=False)
    i, j, m = _yakin_cift(kanal)
    z = AliciZinciri(j, k, kanal)
    zayif = Iletim(gonderen=i, cerceve=cerceve_kur(k, "veri"),
                   baslangic_s=10.0, guc_w=kanal.yayilim.verici_gucu_w)
    z.cerceve_geldi(zayif, 10.0)
    guclu = Iletim(gonderen=m, cerceve=cerceve_kur(k, "veri"),
                   baslangic_s=10.00005, guc_w=kanal.yayilim.verici_gucu_w * 100.0)
    yeni, ezilen = z.cerceve_geldi(guclu, 10.00005)
    assert yeni is not None and yeni.sebep == "alim_red_mesgul"
    assert ezilen is None, "yakalama kapalıyken kimse ezilmemeli"
    assert z.kilitli_iletim is zayif


# ==========================================================================
# ÖNBELGE ↔ GÖVDE — iki AYRI başarısızlık kipi
# ==========================================================================

def test_ONBELGE_ve_GOVDE_ayri_cekimler():
    """🔴 Aynı çekim kullanılsaydı önbelgeyi geçen her çerçeve gövdeyi de
    geçerdi ve `alim_red_per` HİÇ ateşlenmezdi."""
    k, kanal = _kur("bagimsiz-yok")
    a = kanal.topoloji.anlik(30.0)
    sayim = {s: 0 for s in ALIM_SONUCLARI}
    for n, (i, komsular) in enumerate(enumerate(a.komsular)):
        for j in komsular:
            z = AliciZinciri(j, k, kanal)
            it = _iletim(kanal, i, 30.0 + 0.0007 * n)
            yeni, _ = z.cerceve_geldi(it, it.baslangic_s)
            if yeni:
                sayim[yeni.sebep] += 1
                continue
            s = z.cerceve_bitti(it, it.bitis_s)
            sayim[s.sebep] += 1
    assert sayim["alim_basarili"] > 0
    assert sayim["alim_red_per"] + sayim["alim_red_onbelge"] > 0, (
        "hiçbir çerçeve hata almıyorsa kanal fazla iyimser")


def test_ONBELGE_govdeden_DAYANIKLI():
    """Ölçülen fizik: önbelge 192 bit DBPSK, gövde 4096 bit DQPSK."""
    k, kanal = _kur(golgeleme_acik=False, sonumleme_acik=False)
    c = cerceve_kur(k, "veri")
    for db in (8.0, 10.0, 12.0):
        g = 10.0 ** (db / 10.0)
        onbelge = kanal.onbelge_per(c, ((c.onbelge_bit, g),))
        govde = kanal.kahin_per(c, g)
        assert onbelge < govde, f"{db} dB: önbelge gövdeden dayanıksız çıktı"


# ==========================================================================
# 🔒 KUSUR 5 — MAC'te FİZİK YOK
# ==========================================================================

def test_alicida_TEK_BIR_FIZIK_FORMULU_YOK():
    """🔒 `mac/` yalnız durum makinesidir; SINR, PER ve güç `kanal/`a sorulur."""
    yasak_ad = {"exp", "log", "log10", "log1p", "expm1", "sqrt", "hypot"}
    yasak_alan = {"gurultu_w", "verici_gucu_w", "yol_kaybi_db",
                  "golgeleme_db", "guc_kazanci", "bit_hizi_bps", "onbelge_s"}
    ihlal: list[str] = []
    for yol in sorted((SIM2 / "mac").rglob("*.py")):
        if "__pycache__" in yol.parts:
            continue
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        for n in ast.walk(agac):
            if isinstance(n, ast.Attribute) and n.attr in yasak_ad | yasak_alan:
                ihlal.append(f"{yol.name}:{n.lineno} → {n.attr}")
            if isinstance(n, ast.Name) and n.id in yasak_ad:
                ihlal.append(f"{yol.name}:{n.lineno} → {n.id}")
    assert not ihlal, (
        f"🔴 `mac/` içinde fizik: {ihlal}. Kusur 5 tam olarak buydu — "
        f"`alim_per`, `_girisim_w`, `_parca_sinirlari` aslında kanal fiziğiydi "
        f"ve `mac.py` içinde duruyordu.")


def test_ALIM_KARARI_hashten_protokolden_BAGIMSIZ():
    """Aynı tohumda aynı çerçeve, kaç deneme yapıldığından bağımsız olarak
    aynı sonucu vermeli."""
    k, kanal = _kur("bagimsiz-yok")
    i, j, m = _yakin_cift(kanal, 40.0)
    it = _iletim(kanal, i, 40.0)

    z1 = AliciZinciri(j, k, kanal)
    z1.cerceve_geldi(it, it.baslangic_s)
    ilk = z1.cerceve_bitti(it, it.bitis_s)

    z2 = AliciZinciri(j, k, kanal)
    # "öteki protokol" araya bir sürü başka alım sıkıştırıyor
    for n in range(50):
        baska = _iletim(kanal, m, 100.0 + 0.01 * n)
        z3 = AliciZinciri(j, k, kanal)
        z3.cerceve_geldi(baska, baska.baslangic_s)
        z3.cerceve_bitti(baska, baska.bitis_s)
    z2.cerceve_geldi(it, it.baslangic_s)
    ikinci = z2.cerceve_bitti(it, it.bitis_s)

    assert (ilk is None) == (ikinci is None)
    if ilk is not None:
        assert ilk.sebep == ikinci.sebep


def test_sonuc_dogrula_KIRILDIGINDA_konusuyor():
    from sim2.cekirdek.degismezler import DegismezHatasi as DH
    with pytest.raises(DH):
        sonuc_dogrula({"alim_basarili": 3}, deneme=5)
    with pytest.raises(DH):
        sonuc_dogrula({"alim_basarili": 2, "kedi_yedi": 3}, deneme=5)
    sonuc_dogrula({s: 1 for s in ALIM_SONUCLARI}, deneme=len(ALIM_SONUCLARI))


def test_durum_listesi_KAPALI():
    """🔴 `DURUMLAR` BILDIRILMIS ama HIC KULLANILMIYORDU — 9 Eylul 2026.

    Mimari denetiminin D4 kapisi bunu goruyordu, ama esigi yanlis oldugu
    icin ayni notta 29 CANLI ad daha vardi ve gercek olan aralarinda
    kayboluyordu. Esik duzeltilince geriye TEK bu kaldi.

    🔒 Kardesi `mac/dcf.py::DCF_DURUMLARI`nin boyle bir testi VAR
    (`test_mac_dcf.py::test_durum_listesi_KAPALI`) ve alici zincirinin
    yoktu: iki yerde ayni disiplin, birinde uygulanmis birinde degil.
    `03` B5 — *bildirim != kullanim*.

    Iddia: alici zinciri, ilan edilen UC durumun UCUNU de fiilen ziyaret
    eder. Bir durum ilan edilip hic ulasilamiyorsa ya makine ya liste
    yanlistir.
    """
    k, kanal = _kur(golgeleme_acik=False, sonumleme_acik=False)
    i, j, _ = _yakin_cift(kanal)
    z = AliciZinciri(j, k, kanal)
    gorulen = {z.durum}                       # "bos"

    it = _iletim(kanal, i, 10.0)
    z.cerceve_geldi(it, 10.0)
    gorulen.add(z.durum)                      # "onbelge_kilidi"

    # 🔒 Gövde asamasi, ONBELGE bittikten SONRA baslar. Sinir `cerceve.py`den
    # okunur — elle yazilmis bir sure ikinci bir dogru kaynagi acardi.
    onbelge_bitis = it.cerceve.onbelge_araligi(it.baslangic_s)[1]
    z._kilit_ani_s = onbelge_bitis            # gövde asamasina gec
    gorulen.add(z.durum)                      # "govde_aliyor"

    assert gorulen == set(DURUMLAR), (
        f"ilan edilen durumlarin hepsi ziyaret edilmedi: "
        f"gorulen={sorted(gorulen)} ilan={sorted(DURUMLAR)}")
