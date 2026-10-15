"""
AOMDV — makale (Marina & Das 2001) + RFC 3561 uygunluk kapıları.

🔴 BU DOSYA BİR KABUL KAPISIDIR — `test_aodv.py` ve `test_olsr.py` gibi.
AODV'den MİRAS alınan RFC davranışı (HELLO, halka araması, tampon, hız
sınırları, RERR öncül kuralı) `test_aodv.py`de sınanıyor ve burada tekrar
edilmez; burası makalenin DEĞİŞTİRDİĞİ her şeyi ve beyanlı seçimleri sınar.

🔒 U1–U4 EŞLEMESİ (`06` §4.3 · §9, K-194) — AOMDV'nin kapıları adıyla:
    U1  `test_U1_YAPI_…` (yapı yarısı; sayısal yarısı `kalibrasyon/aodv_uygunluk.py`)
    U2  `test_BAG_KOPUNCA_…` (yedek yol kalır, RERR yok) · `test_SON_YOL_…`
        (son yol kopunca RERR) · `test_U2_AOMDV_…` (kaynak yeniden keşfeder)
    U3  AODV'nin U3'ü miras (keşif rotalar kurulunca durur) — bulgu K-144
    U4  `test_U4_AOMDV_…` (genişleyen halka ve RREQ_RETRIES AODV ile aynı;
        RREQ makalenin biçiminde, ilk atlama alanıyla)
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from protokoller.aodv_bicim import (  # noqa: E402
    NET_DIAMETER, RERR, RREP, RREQ as AODV_RREQ, RREQ_RETRIES, TIP_RERR,
    TIP_RREP, TIP_RREQ, TTL_INCREMENT, TTL_START, TTL_THRESHOLD)
from protokoller.aomdv import AOMDV, CokluRota  # noqa: E402
from protokoller.aomdv_bicim import K_CEVAP, RREQ  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.kosum.sonuc import sonuc_satiri  # noqa: E402
from test_aodv import _beyanlar, _gozlem, _istekler, _uyandirmalar  # noqa: E402
from test_kosum import _konfig  # noqa: E402


def _rreq(kaynak: int, kimlik: int, hedef: int, atlama: int, ilk: int,
          kaynak_sira: int = 3, hedef_sira: int = 0, ttl: int = 10) -> tuple:
    return tuple({"tip": TIP_RREQ, "bayraklar": 1, "ayrilmis": 0,
                  "atlama": atlama, "rreq_kimlik": kimlik, "hedef": hedef,
                  "hedef_sira": hedef_sira, "kaynak": kaynak,
                  "kaynak_sira": kaynak_sira, "ttl": ttl,
                  "ilk_atlama": ilk}.items())


def _rrep(hedef: int, kaynak: int, atlama: int, sira: int = 7) -> tuple:
    return tuple({"tip": TIP_RREP, "bayraklar": 0, "ayrilmis": 0,
                  "onek_boyu": 0, "atlama": atlama, "hedef": hedef,
                  "hedef_sira": sira, "kaynak": kaynak,
                  "omur_ms": 3000}.items())


def _al(p: AOMDV, t: float, gonderen: int, bicim: str, yuk: tuple) -> tuple:
    p._komsu[gonderen] = t
    return p.kontrol_alindi(_gozlem(p.kimlik, t), gonderen, bicim, yuk,
                            bicim == "RREQ")


# ==========================================================================
# BİÇİM — RREQ'e `ilk_atlama` (makale §3.2)
# ==========================================================================
def test_BICIM_RREQ_AODV_ARTI_ILK_ATLAMA_4_bayt():
    y = dict(_rreq(0, 1, 9, 0, 0))
    y_aodv = {k: v for k, v in y.items() if k != "ilk_atlama"}
    assert RREQ.bayt(y) == AODV_RREQ.bayt(y_aodv) + 4
    assert RREQ.ad == "RREQ", "kontrol düzlemi biçimi adıyla sayar"
    assert K_CEVAP == 3, "makalenin deneylerindeki k"


# ==========================================================================
# ŞEKİL 3 · GÜNCELLEME KURALI
# ==========================================================================
def test_SEKIL3_yeni_sira_LISTEYI_SIFIRLAR_esit_sirada_yalniz_KUCUK_ILAN():
    p = AOMDV(5)
    assert p._kural(9, 7, 2, 1, 100.0)                       # (1)–(6)
    assert p._rota[9].yollar == {1: 3}
    p._rota[9].ilan_et()                                     # adv_i = 3
    assert p._kural(9, 7, 1, 2, 100.0), "(9) 1 < 3 kabul edilmeli"
    assert p._rota[9].yollar == {1: 3, 2: 2}
    assert not p._kural(9, 7, 4, 3, 100.0), "(9) (3, 5) < (4, 3) reddedilmeli"


def test_SEKIL3_SOZLUK_SIRASI_esit_ilanda_KIMLIK_karar_verir():
    """(9): `(adv_i, i) > (adv_j, j)` — eşit ilanda büyük kimlikli düğüm
    küçük kimlikli komşudan yol alır, tersi alamaz."""
    buyuk = AOMDV(5)
    buyuk._kural(9, 7, 2, 1, 100.0)
    buyuk._rota[9].ilan_et()                                 # (3, 5)
    assert buyuk._kural(9, 7, 3, 4, 100.0), "(3, 5) > (3, 4)"
    kucuk = AOMDV(2)
    kucuk._kural(9, 7, 2, 1, 100.0)
    kucuk._rota[9].ilan_et()                                 # (3, 2)
    assert not kucuk._kural(9, 7, 3, 4, 100.0), "(3, 2) < (3, 4)"
    assert not kucuk._kural(9, 7, 5, 6, 100.0), "daha uzun ilan kabul edildi"
    assert not kucuk._kural(9, 6, 0, 6, 100.0), "BAYAT sıra kabul edildi"
    assert kucuk._kural(9, 8, 9, 6, 100.0), "(1) daha taze sıra"
    assert kucuk._rota[9].yollar == {6: 10}, "(5) liste sıfırlanmadı"


def test_ILAN_EDILEN_atlama_YOLLARIN_EN_BUYUGU_ve_ILAN_ANINDA():
    """§3.1: ilan edilen atlama, yolların atlamalarının EN BÜYÜĞÜDÜR ve
    düğüm bir ilan GÖNDERDİĞİNDE güncellenir — o ana kadar ∞."""
    p = AOMDV(5)
    p._kural(9, 7, 1, 1, 100.0)
    p._kural(9, 7, 3, 2, 100.0)
    assert p._rota[9].ilan_atlama == float("inf")
    assert p._rota[9].sonraki == 1 and p._rota[9].atlama == 2, "birincil (S1)"
    assert p._rota[9].ilan_et() == 4


# ==========================================================================
# §3.2 · RREQ — yinelenen kopyalar ve bağ-ayrık yollar
# ==========================================================================
def test_RREQ_YENI_ILK_ATLAMA_yedek_ters_yol_kurar_ama_ILETILMEZ():
    p = AOMDV(5)
    ilk = _al(p, 1.0, 1, "RREQ", _rreq(0, 77, 9, 1, ilk=1))
    iletilen = [i for i in _istekler(ilk) if i.bicim is RREQ]
    assert iletilen, "ilk kopya iletilmeli"
    assert dict(iletilen[0].yuk)["ilk_atlama"] == 1
    assert dict(iletilen[0].yuk)["atlama"] == 2, "ilan: yolların en büyüğü"
    # Farklı bir ilk atlamadan gelen kopya: (2, 5) > (1, 2) → yedek yol.
    ikinci = _al(p, 1.1, 2, "RREQ", _rreq(0, 77, 9, 1, ilk=2))
    assert not _istekler(ikinci), "§3.2: yalnız ilk kopya iletilir"
    assert p._rota[0].yollar == {1: 2, 2: 2}
    assert p._sayac["rreq_yeni_yol"] == 1
    # Aynı ilk atlamadan gelen kopya BASTIRILIR.
    _al(p, 1.2, 3, "RREQ", _rreq(0, 77, 9, 0, ilk=2))
    assert 3 not in p._rota[0].yollar
    assert p._sayac["rreq_bastirilan"] == 1


def test_RREQ_KAYNAGIN_komsusu_ILK_ATLAMA_olarak_kendini_yazar():
    p = AOMDV(5)
    cikti = _al(p, 1.0, 0, "RREQ", _rreq(0, 77, 9, 0, ilk=0))
    assert dict(_istekler(cikti)[0].yuk)["ilk_atlama"] == 5


def test_HEDEF_en_cok_K_BENZERSIZ_KOMSUYA_cevap_verir_ilk_atlamadan_bagimsiz():
    p = AOMDV(9)
    cevaplar = []
    for i, komsu in enumerate((1, 2, 3, 4, 1)):
        cikti = _al(p, 1.0 + 0.1 * i, komsu, "RREQ",
                    _rreq(0, 77, 9, 2, ilk=11))            # hep AYNI ilk atlama
        cevaplar += [x for x in _istekler(cikti) if x.bicim is RREP]
    assert [c.hedef for c in cevaplar] == [1, 2, 3], (
        "k = 3 benzersiz komşu, ilk atlamadan bağımsız")
    assert p._sayac["cevap_siniri"] == 2


# ==========================================================================
# §3.2 · RREP — ara düğüm, farklı ters yollar
# ==========================================================================
def test_RREP_ara_dugumde_FARKLI_TERS_YOLDAN_ve_KENDI_ILANIYLA():
    p = AOMDV(5)
    p._komsu.update({1: 0.0, 2: 0.0})
    p._rota[0] = CokluRota(hedef_sira=3, yollar={1: 2, 2: 3},
                           son_gecerli_s=100.0)
    birinci = _al(p, 1.0, 8, "RREP", _rrep(hedef=9, kaynak=0, atlama=0))
    ikinci = _al(p, 1.1, 7, "RREP", _rrep(hedef=9, kaynak=0, atlama=0))
    h1 = [i.hedef for i in _istekler(birinci) if i.bicim is RREP]
    h2 = [i.hedef for i in _istekler(ikinci) if i.bicim is RREP]
    assert h1 == [1] and h2 == [2], f"aynı ters yol: {h1} {h2}"
    assert dict(_istekler(ikinci)[0].yuk)["atlama"] == 1, "ilan: max(1, 1)"


# ==========================================================================
# BAKIM — S3 · S4 · S9
# ==========================================================================
def test_BAG_KOPUNCA_yedek_yol_KALIR_RERR_YOK_KOPMA_ve_KURTARMA_AYNI_ANDA():
    from sim2.olcum.rota_olaylari import RotaDefteri
    p = AOMDV(0)
    p._komsu.update({1: 0.0, 2: 0.0})
    p._rota[9] = CokluRota(hedef_sira=5, yollar={1: 2, 2: 3},
                           son_gecerli_s=100.0, oncular={4})
    defter = RotaDefteri()
    cikti = p.iletim_basarisiz(_gozlem(0, 2.0), hedef=1, tur="veri")
    for b in _beyanlar(cikti):
        defter.beyan_isle(0, b, 2.0)
    assert p._rota[9].gecerli and p._rota[9].sonraki == 2, "yedeğe geçmedi"
    assert not [i for i in _istekler(cikti) if i.bicim is RERR], (
        "yolu kalan hedef için RERR gönderildi (S3)")
    assert [b.tip for b in _beyanlar(cikti)] == ["kopma", "rota_kuruldu"]
    assert defter.delta_ler() == pytest.approx((0.0,)), "Δ = 0 (S9)"


def test_YEDEK_yolun_kopmasi_BEYAN_DEGILDIR():
    """S9 · birincil yol sağlam: hedef etkilenmedi — Δ AOMDV lehine yazılmaz."""
    p = AOMDV(0)
    p._komsu.update({1: 0.0, 2: 0.0})
    p._rota[9] = CokluRota(hedef_sira=5, yollar={1: 2, 2: 3},
                           son_gecerli_s=100.0)
    cikti = p.iletim_basarisiz(_gozlem(0, 2.0), hedef=2, tur="veri")
    assert p._rota[9].yollar == {1: 2}
    assert not _beyanlar(cikti)


def test_SON_YOL_kopunca_GECERSIZ_ve_RERR():
    p = AOMDV(0)
    p._komsu[1] = 0.0
    p._rota[9] = CokluRota(hedef_sira=5, yollar={1: 2}, son_gecerli_s=100.0,
                           oncular={4})
    # Öncül 4 komşu (K-244: tek öncüle tek-yayın RERR, rota gerekir).
    p._rota[4] = CokluRota(hedef_sira=0, yollar={4: 1}, son_gecerli_s=100.0)
    cikti = p.iletim_basarisiz(_gozlem(0, 2.0), hedef=1, tur="veri")
    r = p._rota[9]
    assert not r.gecerli and r.yollar == {} and r.hedef_sira == 6, (
        "RFC §6.11 geçersizleştirme — sıra artar, girdi silinmez")
    assert [i for i in _istekler(cikti) if i.bicim is RERR]
    assert [b.tip for b in _beyanlar(cikti)] == ["kopma"]


def test_RERR_yalniz_GONDERENDEN_gecen_yolu_siler():
    p = AOMDV(0)
    p._komsu.update({1: 0.0, 2: 0.0})
    p._rota[9] = CokluRota(hedef_sira=5, yollar={1: 2, 2: 3},
                           son_gecerli_s=100.0, oncular={4})
    yuk = tuple({"tip": TIP_RERR, "bayraklar": 0, "ayrilmis": 0,
                 "hedef_sayisi": 1, "ulasilamaz": (9,),
                 "ulasilamaz_sira": (6,)}.items())
    cikti = _al(p, 1.0, 1, "RERR", yuk)
    assert p._rota[9].gecerli and p._rota[9].yollar == {2: 3}
    assert not [i for i in _istekler(cikti) if i.bicim is RERR], "S4"


def test_S10_GECERSIZ_girdiye_DUSUK_SIRALI_ilan_KABUL_edilir():
    """🔴 Ölçümle bulunan kusurun kapısı (22 Eylül 2026).

    Yerel sıra şişmesi: geçersizleştirme sırayı YEREL olarak artırır. Şekil
    3 harfiyen uygulanınca kaynak hedefin kendi cevabını reddediyor, keşif
    kapanıyor ve paketler tampon tavanından düşüyordu (küçük dünya
    `bagimsiz-yok`: 184 RREP, 79 paket). Kaldırılırsa kapı yanar.
    """
    p = AOMDV(0)
    p._kesif[9] = None
    p._rota[9] = CokluRota(hedef_sira=8, yollar={}, gecerli=False,
                           silme_s=100.0)
    cikti = _al(p, 1.0, 2, "RREP", _rrep(hedef=9, kaynak=0, atlama=1, sira=6))
    assert p._rota[9].gecerli and p._rota[9].yollar == {2: 2}
    assert _uyandirmalar(cikti), "tampon yeniden sorulmadı"


# ==========================================================================
# U1 · YAPI — gerçek koşu
# ==========================================================================
def test_U1_YAPI_teslim_COK_ATLAMALI_defter_kapali_kahin_asilmiyor_COK_YOL():
    from kalibrasyon.kahin import EnGuvenilirKahin, KanalGrafigi

    kfg = _konfig("statik-yok", 1000, 60.0)
    kur = kurulum_yap(kfg)
    kosu = Kosu(kur, AOMDV)
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "u1")
    m, kor = satir["metrikler"], satir["korunum"]
    assert kor["gecerli"], f"satır geçersiz: {kor}"
    assert m["pdr"] and m["pdr"] > 0.0 and m["aktarilan_paket"] > 0
    toplam: dict = {}
    for d in satir["teshis"]["dugum"]:
        for k, v in d.items():
            toplam[k] = toplam.get(k, 0) + v
    assert toplam["rreq_yeni_yol"] > 0, "hiç yedek ters yol kurulmadı"
    assert toplam["yedek_yola_gecis"] > 0, "yedek yol hiç kullanılmadı"
    kur_k = kurulum_yap(kfg)
    grafik = KanalGrafigi(kur_k)
    kosu_k = Kosu(kur_k, lambda i: EnGuvenilirKahin(i, grafik))
    kosu_k.kostur()
    kahin = sonuc_satiri(kur_k, kosu_k.dugumler, "u1")["metrikler"]["pdr"]
    assert m["pdr"] <= kahin, f"AOMDV kâhini GEÇTİ: {m['pdr']} > {kahin}"


def test_korunum_ve_mutabakat_hareketli_kolda_kapaniyor():
    kur = kurulum_yap(_konfig("bagimsiz-yok", 1000, 30.0))
    kosu = Kosu(kur, AOMDV)
    kosu.kostur()
    kor = sonuc_satiri(kur, kosu.dugumler, "k")["korunum"]
    assert kor["gecerli"], f"korunum/mutabakat kapanmadı: {kor}"


def test_kosum_beaconi_KAPALI_ve_ad():
    assert AOMDV.kosum_beaconi is False and AOMDV.ad == "aomdv"


# ==========================================================================
# U2 · U4 — AODV'nin kapılarının AOMDV karşılıkları (K-194)
# ==========================================================================
def test_U2_AOMDV_son_yol_kopunca_KAYNAK_yeniden_KESFEDER():
    """U2'nin ikinci yarısı: son yolu kopan KAYNAK yeni keşif başlatır, paket
    BEKLER; RREQ makalenin biçimindedir (ilk atlama alanı)."""
    p = AOMDV(0)
    p._komsu[1] = 0.0
    p._rota[9] = CokluRota(hedef_sira=5, yollar={1: 2}, son_gecerli_s=100.0)
    p.iletim_basarisiz(_gozlem(0, 1.0), hedef=1, tur="veri")
    karar = p.sonraki_atlama(_gozlem(0, 1.1, paket_hedefi=9))
    assert karar.beklet and karar.sonraki is None
    rreq = [i for i in _istekler(karar.niyetler) if i.bicim is RREQ]
    assert len(rreq) == 1, "yeni keşif başlamadı"
    y = dict(rreq[0].yuk)
    assert y["hedef"] == 9 and y["kaynak"] == 0 and "ilk_atlama" in y
    assert y["ttl"] == TTL_START
    assert _uyandirmalar(karar.niyetler), "keşif zaman aşımı kurulmadı"


def test_U4_AOMDV_genisleyen_halka_ve_RREQ_RETRIES_AODV_ile_AYNI():
    """§6.4 · §6.3 — keşif AODV'den miras: TTL dizisi RFC kadar, deneme hakkı
    bitince keşif bırakılır. Makale keşfin ZAMANLAMASINI değiştirmez."""
    p = AOMDV(0)
    karar = p.sonraki_atlama(_gozlem(0, 1.0, paket_hedefi=9))
    ilk = [i for i in _istekler(karar.niyetler) if i.bicim is RREQ]
    ttl_dizisi = [dict(ilk[0].yuk)["ttl"]]
    t = 1.0
    for _ in range(3 + RREQ_RETRIES * 2):
        t += 10.0
        cikti = p.uyandi(_gozlem(0, t), "kesif:9")
        istek = [i for i in _istekler(cikti) if i.bicim is RREQ]
        if istek:
            ttl_dizisi.append(dict(istek[0].yuk)["ttl"])
    assert ttl_dizisi[:2] == [TTL_START, TTL_START + TTL_INCREMENT]
    assert TTL_THRESHOLD in ttl_dizisi and NET_DIAMETER in ttl_dizisi
    assert 9 not in p._kesif and p._sayac["kesif_basarisiz"] == 1


# ==========================================================================
# K-210 · AOMDV'NİN RFC 3561 TABANI (makalenin sustuğu yerlerde AODV-h kuralı)
# ==========================================================================
def test_K210_RREP_iletiminde_ONCULLER_ve_ters_yol_OMRU():
    """RFC §6.7 son paragraf: ters yolun ömrü `max(mevcut, şimdi +
    ACTIVE_ROUTE_TIMEOUT)`, hedefe doğru sonraki atlamanın girdisinin öncülüne
    kaynağa doğru sonraki atlama. İlk yazımda yoktu; RERR yukarı ulaşmıyor,
    eşler arası statik 1001'de 1 697 paket kara deliğe düşüyordu (K-210)."""
    from protokoller.aodv_bicim import ACTIVE_ROUTE_TIMEOUT_S, SONSUZ_SIRA
    q = AOMDV(5)
    q._komsu.update({2: 0.9, 3: 0.9})
    q._rota[0] = CokluRota(hedef_sira=3, yollar={2: 1}, son_gecerli_s=1.5)
    q._rota[3] = CokluRota(hedef_sira=SONSUZ_SIRA, yollar={3: 1},
                           son_gecerli_s=5.0)
    y = {"kaynak": 0, "hedef": 9, "hedef_sira": 8, "atlama": 1,
         "omur_ms": 3000}
    cikti = q._rrep_isle(3, y, 1.0)
    assert [i for i in _istekler(cikti) if i.bicim is RREP], "iletilmedi"
    assert 2 in q._rota[9].oncular
    assert 2 in q._rota[3].oncular, "komşu girdisinin öncülü yok"
    assert q._rota[0].son_gecerli_s == 1.0 + ACTIVE_ROUTE_TIMEOUT_S


def test_K210_son_yol_RERRle_duserse_SIRA_KOPYALANIR():
    """RFC §6.11 (iii): son yol RERR ile düşünce sıra RERR'den kopyalanır."""
    q = AOMDV(5)
    q._rota[9] = CokluRota(hedef_sira=5, yollar={1: 2}, son_gecerli_s=100.0)
    q._rerr_isle(1, {"ulasilamaz": (9,), "ulasilamaz_sira": (12,)}, 3.0)
    assert not q._rota[9].gecerli and q._rota[9].hedef_sira == 12


def test_K210_HELLO_komsu_rotasina_SIRAYI_yazar_ve_komsu_rotasi_SIRASIZ():
    """RFC §6.9: komşu rotası HELLO'nun sırasını taşır (Şekil 3'ün kuralından
    geçen atlama-0 ilanı); §6.2: yeniden kurulan komşu girdisi sırasız."""
    from protokoller.aodv_bicim import SONSUZ_SIRA
    q = AOMDV(8)
    q._rota[7] = CokluRota(hedef_sira=4, gecerli=False, silme_s=50.0)
    q._komsu_rotasi(7, 1.0)
    assert q._rota[7].hedef_sira == SONSUZ_SIRA
    hello = tuple({"tip": TIP_RREP, "bayraklar": 0, "ayrilmis": 0,
                   "onek_boyu": 0, "atlama": 0, "hedef": 7, "hedef_sira": 6,
                   "kaynak": 7, "omur_ms": 2000}.items())
    q.kontrol_alindi(_gozlem(8, 1.1), 7, "RREP", hello, True)
    assert q._rota[7].hedef_sira == 6 and q._rota[7].yollar == {7: 1}
