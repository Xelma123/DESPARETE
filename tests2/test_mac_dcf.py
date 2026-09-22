"""
ADIM 6b — `mac/dcf.py` kapanış ölçütleri.

Yol haritası:
    Doygunluk verimi **Bianchi** analitiğiyle ±%15 (n = 5…40).
    `dcf.py`de tek fizik formülü yok (AST).

🔒 DOĞRULANAN ŞEY ile KULLANILAN ŞEY AYNI OLMALI
================================================
Aşağıdaki doygunluk koşumu **gerçek `Dcf` nesnelerini** sürer: geri çekilme
çekimi, pencere katlanması, yeniden deneme sayacı — hepsi modülün kendisinden.
Koşumun kendi yazdığı tek şey ORTAM'dır: "bu slotta kim gönderiyor". Adım 9'un
sürücüsü aynı `Dcf`yi gerçek kanalla sürecek; doğrulanan mantık ortak.

⚠️ Bianchi'nin varsayımları koşuma birebir uygulanır, yoksa karşılaştırma
anlamsız olurdu:
  · doygunluk — her düğümün her an gönderecek çerçevesi var
  · tek çarpışma alanı — herkes herkesi duyuyor, gizli terminal yok
  · sonsuz yeniden deneme — vazgeçme yok (üretim konfigi 4 kullanır)
  · ideal kanal — kayıp yalnız çarpışmadan
"""

from __future__ import annotations

import ast
import pathlib
import sys

import pytest

KOK = pathlib.Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))
SIM2 = KOK / "sim2"

from sim2.cekirdek.degismezler import (DegismezHatasi,  # noqa: E402
                                       dogrula)
from sim2.cekirdek.rng import Akislar  # noqa: E402
from sim2.dunya.topoloji import topoloji_kur  # noqa: E402
from sim2.kanal.cerceve import cerceve_kur  # noqa: E402
from sim2.kanal.girisim import Iletim  # noqa: E402
from sim2.kanal.kanal import Kanal  # noqa: E402
from sim2.mac.alici import AliciZinciri  # noqa: E402
from sim2.mac.dcf import DCF_DURUMLARI, Dcf, DcfZamanlari  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402


def _zamanlar(konfig: Konfig) -> DcfZamanlari:
    return DcfZamanlari.kur(konfig, cerceve_kur(konfig, "veri"),
                            cerceve_kur(konfig, "onay"))


# ==========================================================================
# BIANCHI ANALİTİĞİ — karşılaştırma hedefi
# ==========================================================================

def _bianchi_tau_p(p: float, w: int, m: int) -> float:
    """τ = 2(1−2p) / ((1−2p)(W+1) + pW(1−(2p)^m))."""
    return (2.0 * (1.0 - 2.0 * p)
            / ((1.0 - 2.0 * p) * (w + 1) + p * w * (1.0 - (2.0 * p) ** m)))


def bianchi_tau(n: int, w: int, m: int) -> tuple[float, float]:
    """Bianchi'nin sabit noktası: `(τ, p)`.

        τ = 2(1−2p) / ((1−2p)(W+1) + pW(1−(2p)^m))
        p = 1 − (1−τ)^(n−1)

    🔴 BASİT YİNELEME KULLANILMIYOR ve sebebi ölçüldü: `p ← 1−(1−τ(p))^(n−1)`
    biçiminde döndürülünce n = 20 ve n = 40'ta SALINIYOR, yakınsamıyor. İlk
    yazımda öyleydi ve döngü sınırında elde kalan `p` sabit noktayı hiç
    sağlamıyordu (n=40'ta 0,119 ↔ 0,879). Sonuç, verimin analitiği %129
    yanlış vermesiydi.

    İKİYE BÖLME kullanılıyor: `f(p) = 1−(1−τ(p))^(n−1) − p`. Kök önce
    TARAMAYLA kuşatılır, sonra ikiye bölünür.

    ⚠️ Kuşatma aralığı `(0, ½)` DEĞİL, `(0, 1)`. İlk yazımda ½ ile
    sınırlanmıştı ve n = 40'ta kök aralığın dışında kaldı: p → ½'de τ sıfıra
    gitmiyor, `2/(W+1+Wm/2) ≈ 0,0177`ye gidiyor ve f orada hâlâ pozitif.
    Çarpışma olasılığının ½'yi aşamayacağı varsayımı yanlıştı.
    """
    def f(p: float) -> float:
        return 1.0 - (1.0 - _bianchi_tau_p(p, w, m)) ** (n - 1) - p

    alt = ust = None
    onceki_p, onceki_f = 1e-9, f(1e-9)
    for adim in range(1, 2001):
        simdi_p = adim / 2001.0
        simdi_f = f(simdi_p)
        if onceki_f > 0.0 >= simdi_f:
            alt, ust = onceki_p, simdi_p
            break
        onceki_p, onceki_f = simdi_p, simdi_f
    dogrula(alt is not None, "Bianchi kökü kuşatılamadı")
    for _ in range(200):
        orta = 0.5 * (alt + ust)
        if f(orta) > 0.0:
            alt = orta
        else:
            ust = orta
    p = 0.5 * (alt + ust)
    return _bianchi_tau_p(p, w, m), p


def bianchi_verim(n: int, w: int, m: int, slot_s: float, ts_s: float,
                  tc_s: float, yuk_s: float) -> float:
    """Normalize doygunluk verimi: kanalın yükü taşıyan payı."""
    tau, _ = bianchi_tau(n, w, m)
    p_tr = 1.0 - (1.0 - tau) ** n
    p_s = n * tau * (1.0 - tau) ** (n - 1) / p_tr
    return (p_s * p_tr * yuk_s
            / ((1.0 - p_tr) * slot_s + p_tr * p_s * ts_s
               + p_tr * (1.0 - p_s) * tc_s))


# ==========================================================================
# DOYGUNLUK KOŞUMU — gerçek `Dcf` nesneleriyle
# ==========================================================================

def doygunluk_kosumu(n: int, konfig: Konfig, slot_sayisi: int = 400_000,
                     tohum: int = 1) -> float:
    """Slot slot çekişme. Ölçülen: kanalın yükü taşıyan payı.

    🔒 Koşumun yazdığı tek şey ORTAM: bu sanal slotta kim gönderiyor. Geri
    çekilme, pencere katlanması ve yeniden deneme kararlarının hepsi gerçek
    `Dcf` nesnelerinden gelir.
    """
    z = _zamanlar(konfig)
    yuk_s = cerceve_kur(konfig, "veri").govde_suresi_s
    akislar = Akislar(tohum)
    dcfler = [Dcf(i, konfig, akislar) for i in range(n)]
    for d in dcfler:
        d.cerceve_hazir()

    gecen_s = 0.0
    basarili = 0
    for _ in range(slot_sayisi):
        gonderenler = [d for d in dcfler if d.gonderime_hazir]
        if not gonderenler:
            gecen_s += z.slot_s
            for d in dcfler:
                d.slot_gecti()
            continue
        for d in gonderenler:
            d.gonderime_basladi()
            d.onay_bekle()
        if len(gonderenler) == 1:
            gecen_s += z.basari_turu_s
            basarili += 1
            gonderenler[0].onay_geldi()
        else:
            gecen_s += z.carpisma_turu_s
            for d in gonderenler:
                d.onay_gelmedi()
        # doygunluk: gönderen düğümün hemen yeni çerçevesi olur
        for d in gonderenler:
            if d.durum == "bos":
                d.cerceve_hazir()
    return basarili * yuk_s / gecen_s


# ==========================================================================
# 🔒 KAPANIŞ ÖLÇÜTÜ
# ==========================================================================

@pytest.mark.parametrize("n", [5, 10, 20, 40])
def test_DOYGUNLUK_VERIMI_Bianchi_ile_yuzde_15(n):
    """🔒 Kapanış ölçütü: Bianchi analitiğiyle ±%15, n = 5…40."""
    k = Konfig(kol="t", yeniden_deneme_siniri=1000)   # Bianchi: vazgeçme yok
    z = _zamanlar(k)
    yuk_s = cerceve_kur(k, "veri").govde_suresi_s
    analitik = bianchi_verim(n, k.cw_min + 1, 5, z.slot_s,
                             z.basari_turu_s, z.carpisma_turu_s, yuk_s)
    olculen = doygunluk_kosumu(n, k)
    bagil = abs(olculen - analitik) / analitik
    assert bagil < 0.15, (
        f"n={n}: ölçülen {olculen:.4f}, Bianchi {analitik:.4f}, "
        f"bağıl fark %{100*bagil:.1f}")


def test_verim_dugum_sayisiyla_DUSUYOR():
    """Çarpışma olasılığı n ile artar; verim düşmeli. Yanlış yönde bir eğilim,
    geri çekilmenin hiç çalışmadığının işareti olurdu."""
    k = Konfig(kol="t", yeniden_deneme_siniri=1000)
    verimler = [doygunluk_kosumu(n, k, slot_sayisi=120_000) for n in (5, 20, 40)]
    assert verimler[0] > verimler[1] > verimler[2]


def test_Bianchi_sabit_noktasi_TUTARLI():
    """Analitiğin kendi iç tutarlılığı — karşılaştırma hedefi doğru mu."""
    for n in (2, 5, 10, 40):
        tau, p = bianchi_tau(n, 32, 5)
        assert 0.0 < tau < 1.0 and 0.0 < p < 1.0
        assert p == pytest.approx(1.0 - (1.0 - tau) ** (n - 1), abs=1e-9)
    # n arttıkça çarpışma olasılığı artmalı, iletim olasılığı düşmeli
    taular = [bianchi_tau(n, 32, 5) for n in (2, 5, 10, 20, 40)]
    assert all(a[0] > b[0] for a, b in zip(taular, taular[1:]))
    assert all(a[1] < b[1] for a, b in zip(taular, taular[1:]))


# ==========================================================================
# DURUM MAKİNESİ
# ==========================================================================

def test_baslangicta_BOS():
    d = Dcf(0, Konfig(kol="t"), Akislar(1))
    assert d.durum == "bos" and not d.gonderime_hazir
    assert d.cekisme_penceresi == Konfig(kol="t").cw_min


def test_cerceve_hazir_geri_cekilme_CEKIYOR():
    k = Konfig(kol="t")
    d = Dcf(0, k, Akislar(1))
    d.cerceve_hazir()
    assert d.durum == "geri_cekilme"
    assert 0 <= d.geri_sayim <= k.cw_min


def test_sayac_SLOT_BASINA_azaliyor():
    k = Konfig(kol="t")
    d = Dcf(0, k, Akislar(1))
    d.cerceve_hazir()
    baslangic = d.geri_sayim
    for adim in range(baslangic):
        assert d.geri_sayim == baslangic - adim
        d.slot_gecti()
    assert d.geri_sayim == 0 and d.gonderime_hazir
    d.slot_gecti()
    assert d.geri_sayim == 0, "sayaç sıfırın altına inemez"


def test_CARPISMADA_pencere_katlaniyor_ve_DOYUYOR():
    k = Konfig(kol="t", yeniden_deneme_siniri=1000)
    d = Dcf(0, k, Akislar(1))
    d.cerceve_hazir()
    beklenen = [63, 127, 255, 511, 1023, 1023, 1023]
    for hedef in beklenen:
        while not d.gonderime_hazir:
            d.slot_gecti()
        d.gonderime_basladi()
        d.onay_bekle()
        assert d.onay_gelmedi() is False
        assert d.cekisme_penceresi == hedef
    assert d.cekisme_penceresi == k.cw_max


def test_BASARIDA_pencere_sifirlaniyor():
    k = Konfig(kol="t", yeniden_deneme_siniri=1000)
    d = Dcf(0, k, Akislar(1))
    d.cerceve_hazir()
    for _ in range(3):
        while not d.gonderime_hazir:
            d.slot_gecti()
        d.gonderime_basladi()
        d.onay_bekle()
        d.onay_gelmedi()
    assert d.cekisme_penceresi > k.cw_min
    while not d.gonderime_hazir:
        d.slot_gecti()
    d.gonderime_basladi()
    d.onay_geldi()
    assert d.cekisme_penceresi == k.cw_min
    assert d.durum == "bos" and d.deneme == 0


def test_YENIDEN_DENEME_SINIRI_vazgecmeye_goturuyor():
    k = Konfig(kol="t")           # varsayılan sınır 4
    d = Dcf(0, k, Akislar(1))
    d.cerceve_hazir()
    vazgecildi = False
    for _ in range(20):
        while not d.gonderime_hazir:
            d.slot_gecti()
        d.gonderime_basladi()
        d.onay_bekle()
        if d.onay_gelmedi():
            vazgecildi = True
            break
    assert vazgecildi, "yeniden deneme sınırı hiç ateşlenmedi"
    assert d.durum == "bos" and d.cekisme_penceresi == k.cw_min


def test_gecersiz_gecisler_REDDEDILIYOR():
    k = Konfig(kol="t")
    d = Dcf(0, k, Akislar(1))
    with pytest.raises(DegismezHatasi):
        d.slot_gecti()                    # geri çekilmede değil
    with pytest.raises(DegismezHatasi):
        d.gonderime_basladi()             # sayaç sıfırlanmadan
    d.cerceve_hazir()
    with pytest.raises(DegismezHatasi):
        d.cerceve_hazir()                 # boşta değilken
    with pytest.raises(DegismezHatasi):
        d.onay_geldi()                    # göndermeden


def test_vazgec_temiz_birakiyor():
    k = Konfig(kol="t")
    d = Dcf(0, k, Akislar(1))
    d.cerceve_hazir()
    d.vazgec()
    assert d.durum == "bos" and d.geri_sayim == 0
    d.cerceve_hazir()                     # yeniden kullanılabilir


def test_GERI_CEKILME_dugum_basina_ALT_AKIS():
    """🔒 Tek akış olsaydı çok ileti yapan düğüm ötekilerin dizisini kaydırır
    ve düğümler arasında sessiz bir kuplaj doğardı."""
    k = Konfig(kol="t", yeniden_deneme_siniri=1000)
    a = Akislar(5)
    d0 = Dcf(0, k, a)
    d1 = Dcf(1, k, a)
    d0.cerceve_hazir()
    ilk_d1 = None
    # düğüm 0 bir sürü çekim yapıyor
    for _ in range(50):
        while not d0.gonderime_hazir:
            d0.slot_gecti()
        d0.gonderime_basladi()
        d0.onay_bekle()
        d0.onay_gelmedi()
    d1.cerceve_hazir()
    ilk_d1 = d1.geri_sayim

    b = Akislar(5)
    temiz = Dcf(1, k, b)
    temiz.cerceve_hazir()
    assert temiz.geri_sayim == ilk_d1, (
        "düğüm 1'in geri çekilmesi düğüm 0'ın çekim sayısından etkilendi")


def test_zamanlar_CERCEVEDEN_geliyor():
    k = Konfig(kol="t")
    z = _zamanlar(k)
    veri = cerceve_kur(k, "veri")
    onay = cerceve_kur(k, "onay")
    assert z.veri_s == veri.sure_s and z.onay_s == onay.sure_s
    assert z.difs_s == k.difs_s == k.sifs_s + 2 * k.slot_s
    assert z.basari_turu_s == pytest.approx(
        k.difs_s + veri.sure_s + k.sifs_s + onay.sure_s)
    assert z.carpisma_turu_s == pytest.approx(k.difs_s + veri.sure_s)
    assert z.basari_turu_s > z.carpisma_turu_s


# ==========================================================================
# 🔒 KUSUR 5 — DCF'te FİZİK YOK
# ==========================================================================

def test_dcfte_TEK_BIR_FIZIK_FORMULU_YOK():
    yasak_ad = {"exp", "log", "log10", "log1p", "expm1", "sqrt", "hypot",
                "atan2", "cos", "sin"}
    yasak_alan = {"gurultu_w", "verici_gucu_w", "yol_kaybi_db", "golgeleme_db",
                  "guc_kazanci", "bit_hizi_bps", "onbelge_s", "sinr_esigi_db"}
    ihlal: list[str] = []
    agac = ast.parse((SIM2 / "mac" / "dcf.py").read_text(encoding="utf-8"))
    for n in ast.walk(agac):
        if isinstance(n, ast.Attribute) and n.attr in yasak_ad | yasak_alan:
            ihlal.append(f"satır {n.lineno} → {n.attr}")
        if isinstance(n, ast.Name) and n.id in yasak_ad:
            ihlal.append(f"satır {n.lineno} → {n.id}")
    assert not ihlal, (
        f"🔴 `dcf.py` içinde fizik: {ihlal}. Kusur 5 tam olarak buydu.")


def test_dcf_KANALI_ICE_AKTARMIYOR():
    """DCF çekişme mantığıdır; kanalı tanımaz. `Cerceve` yalnız SÜRE taşır."""
    agac = ast.parse((SIM2 / "mac" / "dcf.py").read_text(encoding="utf-8"))
    modulller = {n.module for n in ast.walk(agac)
                 if isinstance(n, ast.ImportFrom) and n.module}
    yasak = {m for m in modulller
             if m.startswith("sim2.kanal") and m != "sim2.kanal.cerceve"}
    assert not yasak, f"🔴 DCF kanalı içe aktarıyor: {sorted(yasak)}"


# ==========================================================================
# 🔴 KAZANIM — `alim_red_yari_cift` İLK KEZ ATEŞLENİYOR
# ==========================================================================

def test_GONDEREN_dugum_ALAMIYOR_yarim_cift():
    """🔴 Adım 6a'da bu dal hiç koşmuyordu (ölçüldü: %0,0), çünkü kimse
    göndermiyordu. DCF gönderime başlayınca alıcı zinciri onu görür."""
    k = Konfig(kol="t", senaryo="statik-yok")
    kanal = Kanal(k, topoloji_kur(k, Akislar(1)))
    a = kanal.topoloji.anlik(0.0)
    i, j = next((i, ks[0]) for i, ks in enumerate(a.komsular) if ks)

    dcf = Dcf(j, k, Akislar(1))
    alici = AliciZinciri(j, k, kanal)
    dcf.cerceve_hazir()
    while not dcf.gonderime_hazir:
        dcf.slot_gecti()
    dcf.gonderime_basladi()
    alici.gonderime_basla()               # aynı düğüm, tek radyo

    it = Iletim(gonderen=i, cerceve=cerceve_kur(k, "veri"), baslangic_s=10.0,
                guc_w=kanal.yayilim.verici_gucu_w)
    sonuc, ezilen = alici.cerceve_geldi(it, 10.0)
    assert sonuc is not None and sonuc.sebep == "alim_red_yari_cift"
    assert ezilen is None

    dcf.onay_bekle()
    dcf.onay_geldi()
    alici.gonderim_bitti()
    sonuc2, _ = alici.cerceve_geldi(it, 10.0)
    assert sonuc2 is None or sonuc2.sebep != "alim_red_yari_cift"


def test_durum_listesi_KAPALI():
    k = Konfig(kol="t")
    d = Dcf(0, k, Akislar(1))
    gorulen = {d.durum}
    d.cerceve_hazir()
    gorulen.add(d.durum)
    while not d.gonderime_hazir:
        d.slot_gecti()
    d.gonderime_basladi()
    gorulen.add(d.durum)
    d.onay_bekle()
    gorulen.add(d.durum)
    assert gorulen == set(DCF_DURUMLARI)
