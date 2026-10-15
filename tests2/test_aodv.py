"""
AODV — RFC 3561 uygunluk kapıları (U1–U4) ve gerçekleme değişmezleri.

🔴 BU DOSYA BİR KABUL KAPISIDIR
===============================
`v2/06` §4.3 dört uygunluk testi tanımlıyor ve §4.4'ün sadakat protokolü
*"U1–U4 koşulur; geçilmeden protokol kabul edilmez"* diyor. Burası onların
**bağlayıcı** karşılığıdır — P1–P8'in test takımındaki karşılığı gibi. Tam
ölçekli kanıt ayrıca `kalibrasyon/`da koşar.

🔒 BOYUT KAPISI ÖNCE GELİR
==========================
*"RFC'ye sadık"* bir cümle değil, bir ölçüm olmalı. İlk testler mesaj
boyutlarını RFC 3561 §5'in bastığı bayt sayılarına karşı sınar; bir alan
genişliği yanlış yazılırsa toplam tutmaz ve kapı konuşur.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from protokoller.aodv import AODV, Rota  # noqa: E402
from protokoller.aodv_bicim import (  # noqa: E402
    ACTIVE_ROUTE_TIMEOUT_S, ALLOWED_HELLO_LOSS, DELETE_PERIOD_S,
    HELLO_INTERVAL_S, NET_DIAMETER, NET_TRAVERSAL_TIME_S,
    NODE_TRAVERSAL_TIME_S, PATH_DISCOVERY_TIME_S, RERR, RREP, RREQ,
    RREQ_RETRIES, SONSUZ_SIRA, TIP_RERR, TIP_RREP, TIP_RREQ, TTL_INCREMENT,
    TTL_START, TTL_THRESHOLD, halka_suresi_s)
from sim2.cekirdek.saat import YerelZaman  # noqa: E402
from sim2.gozlem.karar import Beyan  # noqa: E402
from sim2.gozlem.kontrol import KontrolIstegi, Uyandirma  # noqa: E402
from sim2.gozlem.pencere import Gozlem, PaketGorunumu  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.kosum.sonuc import sonuc_satiri  # noqa: E402
from test_kosum import _konfig  # noqa: E402


def _gozlem(dugum: int, saat_s: float, paket_hedefi: int | None = None,
            paket_kaynagi: int | None = None, paket_sira: int = 0) -> Gozlem:
    """Kanca çağrıları için gözlem. `paket_hedefi=None` → elde paket yok."""
    gorunum = None
    if paket_hedefi is not None:
        gorunum = PaketGorunumu(
            hedef=paket_hedefi,
            kaynak=dugum if paket_kaynagi is None else paket_kaynagi,
            ttl=30, atlama_sayisi=2, bayt=512, kaynak_sira=paket_sira)
    return Gozlem(
        dugum=dugum, saat_s=YerelZaman(saat_s), olculen_gurultu_w=1e-13,
        kanal_mesgul_mu=False, kuyruk_uzunlugu=1, kuyruk_kapasitesi=50,
        son_iletim_sonucu=None, son_iletim_hedefi=None,
        gonderilen_bayt=0, alinan_bayt=0, komsular=(), paket=gorunum)


def _istekler(niyetler) -> list[KontrolIstegi]:
    return [n for n in niyetler if isinstance(n, KontrolIstegi)]


def _beyanlar(niyetler) -> list:
    return [n for n in niyetler if isinstance(n, Beyan)]


def _uyandirmalar(niyetler) -> list[Uyandirma]:
    return [n for n in niyetler if isinstance(n, Uyandirma)]


# ==========================================================================
# MESAJ BOYUTLARI — RFC 3561 §5, birincil belgeden
# ==========================================================================
def test_RFC_mesaj_boyutlari_BIREBIR():
    """🔒 RFC'nin bastığı bayt sayıları: RREQ 24 · RREP 20 · RERR 4 + 8n.

    Alan genişlikleri `aodv_bicim.py`de bit bit yazılı; bu test toplamların
    RFC'ye oturduğunu bağlar. Bir genişlik yanlış yazılırsa burada kırılır.

    ⚠️ RREQ'te BİR BAYT FAZLA ödeniyor ve bu beyanlıdır: RFC'de TTL **IP
    başlığındadır** ve o başlık `KONTROL_KAPSULLEME`de zaten faturalanıyor,
    ama simülatörde bir çerçeveye "IP TTL" koymanın yolu yok — yük biçimle
    birebir eşleşmek zorunda. Yönü AODV'yi olduğundan PAHALI gösterir, yani
    `nrl_*` karşılaştırmasında AODV'nin LEHİNE bir sapma yok.
    """
    y_rreq = {"tip": TIP_RREQ, "bayraklar": 0, "ayrilmis": 0, "atlama": 0,
              "rreq_kimlik": 1, "hedef": 2, "hedef_sira": 0, "kaynak": 3,
              "kaynak_sira": 1, "ttl": NET_DIAMETER}
    assert RREQ.bayt(y_rreq) == 25, "RFC 24 bayt + 1 beyanlı TTL"

    y_rrep = {"tip": TIP_RREP, "bayraklar": 0, "ayrilmis": 0, "onek_boyu": 0,
              "atlama": 0, "hedef": 2, "hedef_sira": 1, "kaynak": 3,
              "omur_ms": 3000}
    assert RREP.bayt(y_rrep) == 20, "RFC 20 bayt"

    for n in (1, 2, 5, 10):
        y_rerr = {"tip": TIP_RERR, "bayraklar": 0, "ayrilmis": 0,
                  "hedef_sayisi": n, "ulasilamaz": tuple(range(n)),
                  "ulasilamaz_sira": tuple(range(n))}
        assert RERR.bayt(y_rerr) == 4 + 8 * n, f"RFC 4 + 8×{n}"


def test_RFC_sabitleri_TURETMELERI_belgeye_uyuyor():
    """🔒 RFC §10'un formülleri — birebir, elle hesaplanmadan."""
    assert NET_TRAVERSAL_TIME_S == pytest.approx(
        2 * NODE_TRAVERSAL_TIME_S * NET_DIAMETER)
    assert PATH_DISCOVERY_TIME_S == pytest.approx(2 * NET_TRAVERSAL_TIME_S)
    assert DELETE_PERIOD_S == pytest.approx(
        5 * max(ACTIVE_ROUTE_TIMEOUT_S, HELLO_INTERVAL_S))
    assert halka_suresi_s(1) == pytest.approx(2 * NODE_TRAVERSAL_TIME_S * 3)


# ==========================================================================
# U2 · TEK BAĞ KOPTUĞUNDA — RERR üretilir ve yeni RREQ başlar (§6.11)
# ==========================================================================
def test_U2_bag_koptugunda_RERR_ve_KOPMA_BEYANI():
    """🔴 `06` §4.3 U2. Ön koşulu 14 Eylül'de (kanca), beyan kanalı 16
    Eylül'de (K-134) karşılandı; ikisi olmadan bu kapı ifade edilemezdi."""
    p = AODV(0)
    p._komsu[1] = 0.0
    # 🔒 Öncül 3: bu rotayı 3 kullanıyor. §6.11 RERR'i YALNIZ öncülü olan
    # hedefler için gönderir (K-143); öncülsüz kurulum RFC'de RERR üretmez.
    # Öncül komşudur (rotayı ters yoldan kurmuştur): tek atlamalı rota.
    p._rota[9] = Rota(sonraki=1, atlama=2, hedef_sira=5,
                      son_gecerli_s=100.0, oncular={3})
    p._rota[3] = Rota(sonraki=3, atlama=1, hedef_sira=0, son_gecerli_s=100.0)

    cikti = p.iletim_basarisiz(_gozlem(0, 1.0), hedef=1, tur="veri")

    beyan = _beyanlar(cikti)
    assert any(b.tip == "kopma" and b.komsu == 1 for b in beyan), (
        "MAC vazgeçti ama protokol KOPMA bildirmedi")
    rerr = [i for i in _istekler(cikti) if i.bicim is RERR]
    assert len(rerr) == 1, "RERR üretilmedi"
    assert dict(rerr[0].yuk)["ulasilamaz"] == (9,)
    # K-244: tek öncül → ona tek-yayın (§6.11 MAY · ns-3 `SendRerrMessage`).
    assert rerr[0].hedef == 3 and not rerr[0].yayin_mi
    # §6.11 — rota geçersizleşir ve SIRA NUMARASI artar; girdi SİLİNMEZ.
    assert not p._rota[9].gecerli
    assert p._rota[9].hedef_sira == 6, "geçersizleşen rotanın sırası artmalı"
    assert 9 in p._rota, "girdi DELETE_PERIOD dolmadan silinmemeli"


def test_U2_kopmadan_sonra_YENI_RREQ_baslar():
    """U2'nin ikinci yarısı: kaynak yeni bir keşif başlatır ve paket BEKLER."""
    p = AODV(0)
    p._komsu[1] = 0.0
    p._rota[9] = Rota(sonraki=1, atlama=2, hedef_sira=5, son_gecerli_s=100.0)
    p.iletim_basarisiz(_gozlem(0, 1.0), hedef=1, tur="veri")

    karar = p.sonraki_atlama(_gozlem(0, 1.1, paket_hedefi=9))
    assert karar.beklet, "rota yokken paket DÜŞMEMELİ, beklemeli"
    assert karar.sonraki is None
    rreq = [i for i in _istekler(karar.niyetler) if i.bicim is RREQ]
    assert len(rreq) == 1, "yeni keşif başlamadı"
    y = dict(rreq[0].yuk)
    assert y["hedef"] == 9 and y["kaynak"] == 0
    # 🔒 §6.4 (K-208 H7): geçersiz girdi varsa ilk TTL *"the Hop Count plus
    # TTL_INCREMENT"* — burada 2 + 2. İlk yazımda hep TTL_START idi.
    assert y["ttl"] == 2 + TTL_INCREMENT, "halka son atlamadan başlamalı"
    assert _uyandirmalar(karar.niyetler), "keşif zaman aşımı kurulmadı"


def test_DD04_ONCEKI_ATLAMA_omru_ve_komsulugu_TAZELENIR():
    """K-242 (DD-04) · §6.2: veri iletilirken kaynağa giden girdinin sonraki
    atlamasının (önceki atlama) rotası ve komşuluğu tazelenir; komşu
    değilse diriltilmez."""
    from protokoller.aodv_bicim import ACTIVE_ROUTE_TIMEOUT_S
    p = AODV(5)
    p._rota[9] = Rota(sonraki=6, atlama=1, hedef_sira=5, son_gecerli_s=100.0)
    p._rota[0] = Rota(sonraki=4, atlama=2, hedef_sira=3, son_gecerli_s=1.0)
    p._rota[4] = Rota(sonraki=4, atlama=1, hedef_sira=1, son_gecerli_s=1.0)
    p._komsu.update({6: 9.0, 4: 8.0})
    karar = p.sonraki_atlama(_gozlem(5, 10.0, paket_hedefi=9, paket_kaynagi=0))
    assert karar.sonraki == 6
    assert p._rota[4].son_gecerli_s == 10.0 + ACTIVE_ROUTE_TIMEOUT_S
    assert p._komsu[4] == 10.0
    del p._komsu[4]
    p.sonraki_atlama(_gozlem(5, 12.0, paket_hedefi=9, paket_kaynagi=0))
    assert 4 not in p._komsu, "ölü komşu veriyle diriltilmemeli"


def test_K242_BASARISIZ_KESIFIN_TAMPONU_DUSER():
    """K-242 · RFC §6.3: RREQ_RETRIES denemeden sonra o hedefe giden
    tampondaki paketler düşer (ns-3 `DropPacketWithDst`); sonra doğan paket
    yeni bir keşif başlatır."""
    p = AODV(0)
    karar = p.sonraki_atlama(_gozlem(0, 1.0, paket_hedefi=9, paket_sira=5))
    assert karar.beklet
    t = 1.0
    while 9 in p._kesif:
        t += 30.0
        p.uyandi(_gozlem(0, t), "kesif:9")
    assert p._sayac["kesif_basarisiz"] == 1
    yeniden = p.sonraki_atlama(_gozlem(0, t, paket_hedefi=9, paket_sira=5))
    assert yeniden.sonraki is None and not yeniden.beklet
    assert p._sayac["kesif_basarisiz_dusen"] == 1
    yeni = p.sonraki_atlama(_gozlem(0, t, paket_hedefi=9, paket_sira=6))
    assert yeni.beklet and 9 in p._kesif


def test_DD04_YAYINLAR_TITRESIMLI_ve_MY_ROUTE_TIMEOUT_MUST():
    """K-242 (DD-04): RREQ, HELLO ve RERR yayınları ns-3 gibi U(0, 10 ms)
    titreşimli; unicast RREP titreşimsiz. MY_ROUTE_TIMEOUT RFC §10'un
    MUST'ı: en az 2 · PATH_DISCOVERY_TIME (11,2 s)."""
    from protokoller.aodv_bicim import (MY_ROUTE_TIMEOUT_S,
                                        PATH_DISCOVERY_TIME_S,
                                        YAYIN_TITRESIMI_S)
    assert YAYIN_TITRESIMI_S == 0.010
    assert MY_ROUTE_TIMEOUT_S >= 2 * PATH_DISCOVERY_TIME_S
    assert MY_ROUTE_TIMEOUT_S == pytest.approx(11.2)
    p = AODV(0)
    rreq = _istekler(p.sonraki_atlama(_gozlem(0, 1.0, paket_hedefi=9))
                     .niyetler)[0]
    assert rreq.bicim is RREQ and rreq.jitter_s == YAYIN_TITRESIMI_S
    hello = _istekler(p.zamanlayici_doldu(_gozlem(0, 5.0), "hello"))[0]
    assert hello.hedef is None and hello.jitter_s == YAYIN_TITRESIMI_S
    rerr = p._rerr_kur((9,), 6.0, oncul_suz=False)[0]
    assert rerr.bicim is RERR and rerr.jitter_s == YAYIN_TITRESIMI_S
    rrep = p._rrep_kur(hedef_adres=0, hedef_sira=1, atlama=0, kaynak=3,
                       omur_s=MY_ROUTE_TIMEOUT_S, sonraki=3)
    assert rrep.jitter_s == 0.0


def test_U2_ARA_dugum_kesif_BASLATMAZ_paketi_DUSURUR():
    """🔒 §6.11 — geçersiz rotası olan ARA düğüm RERR gönderir ve DÜŞÜRÜR.

    Keşif KAYNAĞIN işidir. Ara düğüm keşif başlatsaydı her kopma ağ çapında
    bir sel doğururdu. Düşme sebebi `hedef_yok` DEĞİL `rota_gecersiz`dir.
    """
    p = AODV(5)
    # 🔒 Öncül 0: paketin kaynağı bu rotayı kullanıyordu (K-143).
    p._rota[9] = Rota(sonraki=1, atlama=2, hedef_sira=5, son_gecerli_s=100.0,
                      gecerli=False, oncular={0})
    karar = p.sonraki_atlama(
        _gozlem(5, 2.0, paket_hedefi=9, paket_kaynagi=0))
    assert not karar.beklet and karar.sonraki is None
    assert [b.tip for b in karar.beyan] == ["rota_gecersiz"]
    assert not [i for i in _istekler(karar.niyetler) if i.bicim is RREQ]
    assert [i for i in _istekler(karar.niyetler) if i.bicim is RERR]


# ==========================================================================
# U4 · OLAY İZLERİ — RFC'nin öngördüğü mesaj sırası ve zamanlayıcılar
# ==========================================================================
def test_U4_genisleyen_halka_TTL_dizisi_RFC_kadar():
    """§6.4 · TTL_START → +TTL_INCREMENT → … → TTL_THRESHOLD → NET_DIAMETER.

    🔒 Genişleyen halka araması OLMASAYDI her keşif ağ çapında sel olurdu ve
    AODV'nin kontrol yükü olduğundan YÜKSEK ölçülürdü — `03` §2 ilke 4'ün
    yasakladığı *"eksik uygulamadan doğan straw-man"*.
    """
    p = AODV(0)
    karar = p.sonraki_atlama(_gozlem(0, 1.0, paket_hedefi=9))
    ttl_dizisi = [dict(_istekler(karar.niyetler)[0].yuk)["ttl"]]
    t = 1.0
    for _ in range(6):
        t += 5.0
        cikti = p.uyandi(_gozlem(0, t), "kesif:9")
        istek = [i for i in _istekler(cikti) if i.bicim is RREQ]
        if not istek:
            break
        ttl_dizisi.append(dict(istek[0].yuk)["ttl"])
    assert ttl_dizisi[0] == TTL_START
    assert ttl_dizisi[1] == TTL_START + TTL_INCREMENT
    assert TTL_THRESHOLD in ttl_dizisi, "eşik basamağı atlanmış"
    assert NET_DIAMETER in ttl_dizisi, "eşikten sonra ağ çapına çıkılmalı"


def test_U4_RREQ_RETRIES_asilinca_kesif_BIRAKILIR():
    """§6.3 — deneme hakkı bitince protokol keşfi bırakır.

    🔒 Paketleri protokol SİLMEZ: tamponun süre tavanı onları alır ve düşüş
    `tampon_asimi` sebebiyle deftere geçer. RFC de *"uygulamaya haber
    verilir"* der; paketleri protokolün kendisi atmaz.
    """
    p = AODV(0)
    p.sonraki_atlama(_gozlem(0, 1.0, paket_hedefi=9))
    t = 1.0
    for _ in range(3 + RREQ_RETRIES * 2):
        t += 10.0
        p.uyandi(_gozlem(0, t), "kesif:9")
    assert 9 not in p._kesif, "keşif bırakılmadı"
    assert p._sayac["kesif_basarisiz"] == 1


def test_U4_HELLO_RREP_bicimindedir_ve_ILETILMEZ():
    """§6.9 — HELLO, TTL 1 olan, hedefi KENDİSİ olan bir RREP'tir.

    🔴 Bu kapı bir HATADAN sonra yazıldı. Ayıraç önce *"hedef gönderen ve
    atlama 1"* idi ve GERÇEK bir RREP'i de yakalıyordu: hedefin komşusu olan
    ara düğüm, hedeften gelen RREP'i tam olarak böyle görür. Ölçüldü —
    `rrep_uretilen = 95` ama **`rrep_iletilen = 0`**, yani çok atlamalı keşif
    hiç tamamlanmıyordu (PDR 0,40). Doğru ayıraç `kaynak == hedef`tir.
    """
    p = AODV(7)
    hello = _istekler(p.zamanlayici_doldu(_gozlem(7, 5.0), "hello"))
    assert len(hello) == 1 and hello[0].bicim is RREP
    y = dict(hello[0].yuk)
    assert y["kaynak"] == y["hedef"] == 7, "HELLO kendisi hakkındadır"
    assert hello[0].yayin_mi
    assert y["omur_ms"] == int(ALLOWED_HELLO_LOSS * HELLO_INTERVAL_S * 1000)

    # Bir komşunun HELLO'su iletilmez…
    alan = AODV(8)
    cikti = alan.kontrol_alindi(_gozlem(8, 5.1), 7, "RREP", hello[0].yuk,
                                True)
    assert not _istekler(cikti), "HELLO iletilmemeli"
    assert 7 in alan._komsu, "HELLO komşuluğu kurmalı"

    # …ama GERÇEK bir RREP (kaynak ≠ hedef) İLETİLİR. 🔒 §6.7 (K-208 H5):
    # RREP yalnız ileri rotayı kurduysa ya da güncellediyse iletilir; HELLO
    # 7'ye rotayı sıra 1 ile kurdu, bu RREP sıra 2 getiriyor.
    alan._rota[3] = Rota(sonraki=9, atlama=1, hedef_sira=1,
                         son_gecerli_s=100.0)
    gercek = dict(hello[0].yuk) | {"kaynak": 3, "hedef_sira": 2}
    cikti = alan.kontrol_alindi(_gozlem(8, 5.2), 7, "RREP", tuple(
        gercek.items()), False)
    iletilen = [i for i in _istekler(cikti) if i.bicim is RREP]
    assert iletilen, "gerçek RREP iletilmedi — HELLO ayıracı fazla geniş"


def test_U4_HELLO_son_aralikta_YAYIN_yapildiysa_ATLANIR():
    """§6.9 — *"yalnız son HELLO_INTERVAL içinde başka bir yayın yoksa"*.

    🔒 Gerçek bir tasarruf: RREQ yayını zaten varlığı duyurur. Uygulanmazsa
    AODV'nin kontrol yükü olduğundan YÜKSEK ölçülür.
    """
    p = AODV(0)
    p.sonraki_atlama(_gozlem(0, 10.0, paket_hedefi=9))    # RREQ yayını
    assert not _istekler(p.zamanlayici_doldu(_gozlem(0, 10.5), "hello"))
    assert _istekler(p.zamanlayici_doldu(
        _gozlem(0, 11.5), "hello")), "aralık geçince HELLO dönmeli"


def test_U4_RREQ_TEKRARI_bastiriliyor():
    """§6.5 — aynı (kaynak, RREQ kimliği) ikinci kez işlenmez."""
    p = AODV(5)
    y = {"tip": TIP_RREQ, "bayraklar": 1, "ayrilmis": 0, "atlama": 0,
         "rreq_kimlik": 77, "hedef": 9, "hedef_sira": 0, "kaynak": 0,
         "kaynak_sira": 3, "ttl": 10}
    ilk = p.kontrol_alindi(_gozlem(5, 1.0), 1, "RREQ", tuple(y.items()),
                           True)
    assert _istekler(ilk), "ilk RREQ iletilmeli"
    ikinci = p.kontrol_alindi(_gozlem(5, 1.1), 2, "RREQ", tuple(y.items()),
                              True)
    assert not _istekler(ikinci), "tekrar bastırılmadı"
    assert p._sayac["rreq_bastirilan"] == 1


# ==========================================================================
# U1 · KARIŞTIRICISIZ BAĞLI AĞ — teslim kâhin referansına yakın
# ==========================================================================
def test_U1_YAPI_kapisi_teslim_var_ve_defter_kapaniyor():
    """🔴 `06` §4.3 U1'in YAPI yarısı. Sayısal yarısı burada DEĞİL.

    🔴 BURAYA ÖNCE MUTLAK BİR EŞİK YAZMIŞTIM (PDR ≥ 0,95) VE YANLIŞTI —
    eşik gevşek ya da sıkı olduğu için değil, YANLIŞ YERDE olduğu için.
    U1'in ölçütü *"teslim oranı KÂHİN REFERANSINA yakın"*dır ve ben o
    referansı BAŞKA BİR KONFİGÜRASYONDAN almıştım: tam ölçekteki 0,996–1,000
    sayısını 14 düğümlük test dünyasına uygulamıştım. Aynı dünyada ölçüldü —
    kâhinin kendisi orada 0,969, AODV 0,851, yani oran 0,879.

    🔒 Sayısal kapı artık `kalibrasyon/aodv_uygunluk.py`de ve TAM ÖLÇEKTE
    koşuyor: AODV'nin PDR'si, AYNI konfigürasyonda ölçülen ETX kâhininin
    PDR'sine oranlanıyor. Desen P1–P8'inkinin aynısı: bağlayıcı yapı kapısı
    testlerde, tam ölçek kanıtı kalibrasyonda.

    Buradaki kapı eşiksizdir ve boş geçmeye kapalıdır.

    🔴 İLK YAZIMINDA SON İDDİA `pdr <= 1.0` İDİ VE BU BİR KAPI DEĞİLDİ:
    PDR tanımı gereği 1'i aşamaz, yani o satır HİÇ ATEŞ EDEMEZDİ. Yorumu
    *"kâhini geçmek de bir hatadır"* diyordu ama kâhini hiç koşmuyordu —
    yani yorum bir şey iddia ediyor, iddia başka bir şey sınıyordu. K-103'ün
    dersi buydu: *ateş etmeyen bir kapı, kapı değildir.* Kâhin artık AYNI
    dünyada gerçekten koşuyor.
    """
    # 🔒 Yerel içe aktarma — `test_tehdit_senaryolari.py`nin emsali. Test
    # takımı `kalibrasyon/`a modül düzeyinde bağlanmaz.
    from kalibrasyon.kahin import EnGuvenilirKahin, KanalGrafigi

    kfg = _konfig("statik-yok", 1000, 30.0)
    kur = kurulum_yap(kfg)
    kosu = Kosu(kur, AODV)
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "u1")
    m, kor = satir["metrikler"], satir["korunum"]
    assert kor["gecerli"], f"satır geçersiz: {kor}"
    assert kor["uretilen"] > 0, "test BOŞ koşuyor — hiç paket üretilmemiş"
    assert m["pdr"] is not None and m["pdr"] > 0.0, "hiç teslim yok"

    # 🔒 Kâhini GEÇMEK bir kazanç DEĞİL, bir kaçaktır: kâhin her an en
    # güvenilir yolu BİLİR ve gerçek bir protokol onu aşamaz. Aşıyorsa
    # kâhin bilgisi protokole sızmış demektir. Eşiksiz — yalnız sıralama.
    kur_k = kurulum_yap(kfg)
    grafik = KanalGrafigi(kur_k)
    kosu_k = Kosu(kur_k, lambda i: EnGuvenilirKahin(i, grafik))
    kosu_k.kostur()
    kahin = sonuc_satiri(kur_k, kosu_k.dugumler, "u1")["metrikler"]["pdr"]
    assert kahin is not None and kahin > 0.0, "kâhin BOŞ koştu"
    assert m["pdr"] <= kahin, (
        f"AODV kâhini GEÇTİ: {m['pdr']:.4f} > {kahin:.4f} — "
        f"kâhin bilgisi protokole sızmış olabilir")


def test_U1_COK_ATLAMALI_teslim_var():
    """🔒 U1'in boş geçmeye kapalı yarısı.

    PDR yüksek çıkabilir ama teslimlerin hepsi TEK ATLAMALIYSA keşif hiç
    çalışmıyor demektir — ve bu gerçekten yaşandı: HELLO ayıracı bozukken
    PDR 0,40'tı ve teslim edilen HER paket doğrudan komşuya gidiyordu.
    """
    kur = kurulum_yap(_konfig("statik-yok", 1000, 30.0))
    kosu = Kosu(kur, AODV)
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "u1b")
    toplam = {}
    for d in satir["teshis"]["dugum"]:
        for k, v in d.items():
            toplam[k] = toplam.get(k, 0) + v
    assert toplam["kesif_basarili"] > 0, "hiç keşif tamamlanmamış"
    assert toplam["rrep_iletilen"] > 0, (
        "hiçbir RREP İLETİLMEMİŞ — çok atlamalı keşif çalışmıyor")
    assert satir["metrikler"]["aktarilan_paket"] > 0, (
        "hiç ara düğümde iletilen paket yok — teslimlerin hepsi tek atlamalı")


# ==========================================================================
# U3 · KARIŞTIRMA ve HAREKET YOK — AODV'nin yükü KEŞİF ANINDA
# ==========================================================================
def test_U3_BULGU_onculsuz_RERR_GERCEK_kosuda_bastiriliyor():
    """🔴 `06` §4.3 U3'ün AODV beklentisi TUTMADI — bulgu (`04` K-144).

    Beklenti *"AODV yükü yalnız keşif anında"* idi. Ölçüldü: kayıplı bir
    kablosuz ağda sürekli trafik altında keşif SUSMUYOR — bağlar çarpışma ve
    sönümlemeyle düşüyor, MAC vazgeçiyor, AODV yeniden keşfediyor. Yük süreyle
    neredeyse doğrusal büyüyor (60 → 120 s oranı **2,070**; OLSR 2,200).
    Üretici: `python -u kalibrasyon/aodv_uygunluk.py u3`. RFC'ye uygun
    davranış; beklenti değil ölçüm doğrudur.

    🔴 BU KAPI BİR ÖNCEKİNİN YERİNE KONDU, çünkü o HİÇ ATEŞ EDEMİYORDU:
    `hello` değişkenine yine RREP sayısı yazılmış ve iddia
    `kesif > 0 and hello > 0` idi. O zayıflık yüzünden AODV'nin sürekli
    RERR ürettiği görülmemişti — ta ki OLSR'ın ölçümü onu yan yana koyana
    kadar (K-142, K-143).

    🔒 Bu kapı, bulunan kusurun SINIFINI gerçek bir koşuda sınar: RFC'nin
    istemediği kontrol trafiği. §6.11'in öncül kuralı birim testte sınanıyor
    (`test_RERR_ONCULU_OLMAYAN_hedef_icin_GONDERILMEZ`); burada o süzgecin
    gerçek bir ağda GERÇEKTEN ateşlendiği ve keşfin yine de çalıştığı
    sınanır. Süzgeç kaldırılırsa `rerr_onculsuz` sıfır kalır ve kapı yanar.
    """
    kur = kurulum_yap(_konfig("statik-yok", 1000, 40.0))
    kosu = Kosu(kur, AODV)
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "u3")
    bicim = satir["teshis"]["kontrol_duzlemi"]["bicim"]["tum"]
    assert bicim.get("RREQ", {}).get("cerceve", 0) > 0, "hiç RREQ yok"
    assert bicim.get("RREP", {}).get("cerceve", 0) > 0, "hiç RREP yok"
    toplam: dict[str, float] = {}
    for d in satir["teshis"]["dugum"]:
        for k, v in d.items():
            toplam[k] = toplam.get(k, 0) + v
    assert toplam["rerr_onculsuz"] > 0, (
        "öncülsüz RERR adayı hiç bastırılmadı — §6.11 süzgeci gerçek bir "
        "koşuda ateşlenmiyor")


def test_U3_rotalar_kurulunca_KESIF_DURUYOR():
    """U3'ün asıl iddiası: hareket ve karıştırma yokken keşif SUSAR.

    🔒 Ölçüt önceden ilan edildi: koşu sonunda SÜREN keşif sayısı **sıfır**
    ve keşif başarısızlığı **sıfır**. Reaktif bir protokol kararlı bir
    topolojide bu noktaya gelmek zorundadır; gelmiyorsa ya keşif çalışmıyor
    ya rotalar sürekli geçersizleşiyordur.
    """
    kur = kurulum_yap(_konfig("statik-yok", 1000, 30.0))
    kosu = Kosu(kur, AODV)
    kosu.kostur()
    toplam = {}
    for d in sonuc_satiri(kur, kosu.dugumler, "u3b")["teshis"]["dugum"]:
        for k, v in d.items():
            toplam[k] = toplam.get(k, 0) + v
    assert toplam["suren_kesif"] == 0, "koşu sonunda takılı keşif var"
    assert toplam["kesif_basarisiz"] == 0, (
        f"kararlı topolojide keşif başarısız oldu: {toplam}")


# ==========================================================================
# GERÇEKLEME DEĞİŞMEZLERİ
# ==========================================================================
def test_kosum_beaconi_KAPALI_ve_komsuluk_KENDI_HELLOSUNDAN():
    """🔒 `13` §03.8 · `02` §R3'ün straw-man'ini kapatan karar.

    Koşum beacon'ı 1 s'dir ve o AODV'nin RFC hızıdır, ama OLSR'ın RFC'si
    2 s der — ortak beacon OLSR'ı kendi hızının İKİ KATINDA koştururdu. Her
    protokol kendi HELLO'sunu gönderince asimetri yapısal olarak kapanır.
    """
    kur = kurulum_yap(_konfig("statik-yok", 1000, 20.0))
    kosu = Kosu(kur, AODV)
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "beacon")
    assert satir["metrikler"]["beacon_gonderilen"] == 0, (
        "koşum beacon'ı kapatılmamış")
    kd = satir["teshis"]["kontrol_duzlemi"]
    assert kd["kosum_beaconi_kapali_dugum"] == kur.dugum_sayisi
    # Komşuluk yine de kuruluyor — kendi HELLO'sundan.
    komsu = sum(d["komsu"] for d in satir["teshis"]["dugum"])
    assert komsu > 0, "beacon kapalı ve komşu da yok — protokol KÖR"


def test_korunum_ve_mutabakat_AODV_ile_kapaniyor():
    """🔒 Defter kapanmadan hiçbir sayı okunmaz."""
    for senaryo in ("statik-yok", "bagimsiz-yok", "statik-surekli"):
        kur = kurulum_yap(_konfig(senaryo, 1000, 20.0))
        kosu = Kosu(kur, AODV)
        kosu.kostur()
        kor = sonuc_satiri(kur, kosu.dugumler, "k")["korunum"]
        assert kor["korunum_tamam"], f"{senaryo}: denklem kırıldı {kor}"
        assert kor["mutabakat_tamam"], f"{senaryo}: mutabakat kırıldı {kor}"


def test_gecersiz_rota_SILINMIYOR_sira_KORUNUYOR():
    """§6.11 · §6.2 — geçersiz girdi `DELETE_PERIOD` boyunca yaşar.

    Silinseydi düğüm bayat bir rotayı taze sanıp geri kabul ederdi: taşıdığı
    SIRA NUMARASI hâlâ değerlidir.
    """
    p = AODV(0)
    p._komsu[1] = 0.0
    p._rota[9] = Rota(sonraki=1, atlama=2, hedef_sira=5, son_gecerli_s=100.0)
    p.iletim_basarisiz(_gozlem(0, 1.0), hedef=1, tur="veri")
    assert 9 in p._rota and not p._rota[9].gecerli
    p.zamanlayici_doldu(_gozlem(0, 1.0 + DELETE_PERIOD_S - 0.1), "bakim")
    assert 9 in p._rota, "DELETE_PERIOD dolmadan silinmiş"
    p.zamanlayici_doldu(_gozlem(0, 1.0 + DELETE_PERIOD_S + 0.1), "bakim")
    assert 9 not in p._rota, "DELETE_PERIOD dolunca silinmeli"


def test_hedef_KENDISI_ise_RREP_uretiliyor():
    """§6.6.1 — hedefin kendisi RREP üretir ve sırasını gerekirse artırır."""
    p = AODV(9)
    y = {"tip": TIP_RREQ, "bayraklar": 0, "ayrilmis": 0, "atlama": 1,
         "rreq_kimlik": 4, "hedef": 9, "hedef_sira": p._sira + 1,
         "kaynak": 0, "kaynak_sira": 2, "ttl": 10}
    cikti = p.kontrol_alindi(_gozlem(9, 1.0), 5, "RREQ", tuple(y.items()),
                             True)
    rrep = [i for i in _istekler(cikti) if i.bicim is RREP]
    assert len(rrep) == 1 and not rrep[0].yayin_mi, "RREP unicast döner"
    yy = dict(rrep[0].yuk)
    assert yy["hedef"] == 9 and yy["kaynak"] == 0 and yy["atlama"] == 0
    assert p._sira == 2, "RREQ'in istediği sıra için kendi sırası artmalı"


# ==========================================================================
# ÖLÇÜM BEYANLARI — anahtar `(düğüm, KOPAN KOMŞU)` (19 Eylül 2026, K-139)
# ==========================================================================
def _rrep_yuku(hedef: int, kaynak: int, hedef_sira: int = 7) -> tuple:
    return tuple({"tip": TIP_RREP, "bayraklar": 0, "ayrilmis": 0,
                  "onek_boyu": 0, "atlama": 1, "hedef": hedef,
                  "hedef_sira": hedef_sira, "kaynak": kaynak,
                  "omur_ms": 3000}.items())


def test_BEYAN_bos_komsunun_zaman_asimi_KOPMA_DEGILDIR():
    """🔴 Üzerinden hiçbir rota geçmeyen komşunun düşmesi bir kopma DEĞİL.

    RFC 3561 §6.11 bağ kopmasını *"etkin bir rotanın sonraki atlaması"* için
    tanımlar. Önceden her komşu kaybı beyan ediliyordu ve §6.9'un HELLO
    bastırması boştaki komşuları sürekli düşürdüğü için ölçüldü: statik bir
    ağda, topoloji hiç değişmezken 50 s'de **1 082** "kopma".
    """
    p = AODV(0)
    p._komsu[1] = 0.0                       # komşu var, rota YOK
    cikti = p.zamanlayici_doldu(_gozlem(0, 10.0), "bakim")
    assert 1 not in p._komsu, "sınav boş geçti — komşu hiç düşmedi"
    assert not [b for b in _beyanlar(cikti) if b.tip == "kopma"], (
        "etkin rota taşımayan bir komşunun düşmesi kopma beyan edildi")


def test_BEYAN_RERR_bir_KOPMA_DEGILDIR():
    """🔴 RERR uzaktaki bir bağın haberidir; bu düğümün kendi bağı sağlam.

    Önceden her ulaşılamaz HEDEF bir `kopma` sayılıyordu; `algilama_
    duyarliligi` (fiziksel BAĞ kopmalarına oran) bu yüzden 430'a çıkmıştı.
    Rota yine geçersizleşir ve RERR yine yayılır — değişen yalnız beyan.
    """
    p = AODV(0)
    p._komsu[1] = 0.0
    # 🔒 Öncül 3 — RERR'in yayılması için (K-143); komşu, tek atlamalı
    # rotası var (K-244: tek öncüle tek-yayın).
    p._rota[9] = Rota(sonraki=1, atlama=2, hedef_sira=5, son_gecerli_s=100.0,
                      oncular={3})
    p._rota[3] = Rota(sonraki=3, atlama=1, hedef_sira=0, son_gecerli_s=100.0)
    yuk = tuple({"tip": TIP_RERR, "bayraklar": 0, "ayrilmis": 0,
                 "hedef_sayisi": 1, "ulasilamaz": (9,),
                 "ulasilamaz_sira": (6,)}.items())
    cikti = p.kontrol_alindi(_gozlem(0, 1.0), 1, "RERR", yuk, True)
    assert not p._rota[9].gecerli, "RERR rotayı geçersizleştirmedi"
    assert [i for i in _istekler(cikti) if i.bicim is RERR], "RERR yayılmadı"
    assert not [b for b in _beyanlar(cikti) if b.tip == "kopma"], (
        "uzak bir kopma, bu düğümün kopması diye beyan edildi")


def test_BEYAN_kopma_ve_kurtarma_AYNI_ANAHTARDA_ve_DELTA_KAPANIYOR():
    """🔒 Uçtan uca: `kopma(1)` → başka komşudan rota → `rota_kuruldu(1)`.

    Önceki hâlde kopma KOMŞUYLA, kurtarma HEDEFLE anahtarlanıyordu; defter
    ikisini eşleyemiyordu (bagimsiz-yok: 789 kopma anahtarı, 9 kurulum
    anahtarı, 6'sı ortak). Bu sınav gerçek `RotaDefteri`ni kullanır, yani
    eşleşme iddiası değil, Δ'nın kendisi sınanır.
    """
    from sim2.olcum.rota_olaylari import RotaDefteri

    p = AODV(0)
    p._komsu[1] = 0.0
    p._rota[9] = Rota(sonraki=1, atlama=2, hedef_sira=5, son_gecerli_s=100.0)
    defter = RotaDefteri()

    kopus = p.iletim_basarisiz(_gozlem(0, 2.0), hedef=1, tur="veri")
    for b in _beyanlar(kopus):
        defter.beyan_isle(0, b, 2.0)
    assert [b.komsu for b in _beyanlar(kopus) if b.tip == "kopma"] == [1]

    # Başka bir komşu (2) hedefe yeni ve daha taze bir rota getiriyor.
    donus = p.kontrol_alindi(_gozlem(0, 2.7), 2, "RREP",
                             _rrep_yuku(hedef=9, kaynak=0), False)
    kurulan = [b for b in _beyanlar(donus) if b.tip == "rota_kuruldu"]
    assert [b.komsu for b in kurulan] == [1], (
        f"kurtarma kopan KOMŞUNUN anahtarıyla beyan edilmedi: {kurulan}")
    for b in _beyanlar(donus):
        defter.beyan_isle(0, b, 2.7)

    assert defter.delta_ler() == pytest.approx((0.7,)), "Δ kapanmadı"
    assert defter.kapanmamis_kopma() == 0
    # Aynı hedefe ikinci bir rota Δ'yı İKİNCİ kez kapatmaz.
    tekrar = p.kontrol_alindi(_gozlem(0, 3.0), 3, "RREP",
                              _rrep_yuku(hedef=9, kaynak=0, hedef_sira=8),
                              False)
    assert not [b for b in _beyanlar(tekrar) if b.tip == "rota_kuruldu"]


def test_COR_SAYAC_IKIZI_ile_DEFTER_ayni_sayiyi_veriyor():
    """🔴 K-141 — sayaçtan türeyen `cor` ile defterden gelen `cor_olcum` aynı.

    Önceden `rota_etkilendi` sayacı HİÇBİR YERDE artırılmıyordu ve sayaç
    tarafındaki `cor` (dolayısıyla analiz penceresindeki `cor_pencere`)
    HER ZAMAN boştu. Gerçek beyan üreten tek taban protokol AODV olduğu için
    sınav burada, gerçek bir koşuda.
    """
    kur = kurulum_yap(_konfig("statik-yok", 1000, 30.0))
    kosu = Kosu(kur, AODV)
    kosu.kostur()
    m = sonuc_satiri(kur, kosu.dugumler, "cor")["metrikler"]
    assert m["kopma_algilanan"], "sınav boş geçti — hiç kopma beyan edilmedi"
    assert m["cor"] is not None, "sayaç ikizi hâlâ boş"
    assert m["cor"] == pytest.approx(m["cor_olcum"])
    assert 0.0 <= m["cor"] <= 1.0


def test_RERR_ONCULU_OLMAYAN_hedef_icin_GONDERILMEZ():
    """🔴 RFC 3561 §6.11 (K-143): *"The RERR should contain those
    destinations that ... have a non-empty precursor list."*

    İlk yazımda etkilenen rota varsa her zaman yayın yapılıyordu; öncül
    listeleri tutuluyor ama kullanılmıyordu. Kopma yine BEYAN edilir (K-139:
    bu düğümün kullandığı bir bağ koptu); yalnız kimseye duyurulmaz.
    """
    p = AODV(0)
    p._komsu[1] = 0.0
    p._rota[9] = Rota(sonraki=1, atlama=2, hedef_sira=5, son_gecerli_s=100.0)
    cikti = p.iletim_basarisiz(_gozlem(0, 1.0), hedef=1, tur="veri")
    assert not [i for i in _istekler(cikti) if i.bicim is RERR], (
        "öncülü olmayan hedef için RERR yayıldı")
    assert [b.komsu for b in _beyanlar(cikti) if b.tip == "kopma"] == [1]
    assert p._sayac["rerr_onculsuz"] == 1
    assert not p._rota[9].gecerli, "rota yine de geçersizleşmeli"


def _rreq_yuku(kimlik: int, kaynak: int = 0, hedef: int = 9) -> tuple:
    return tuple({"tip": TIP_RREQ, "bayraklar": 1, "ayrilmis": 0,
                  "atlama": 0, "rreq_kimlik": kimlik, "hedef": hedef,
                  "hedef_sira": 0, "kaynak": kaynak, "kaynak_sira": 3,
                  "ttl": 10}.items())


def test_K194_RREP_basarisizsa_KARA_LISTE_ve_RREQ_YOK_SAYILIR():
    """🔒 RFC 3561 §6.8 (K-194): RREP'i bağ katmanında onaylanmayan komşu
    kara listeye girer; ondan gelen RREQ `BLACKLIST_TIMEOUT` boyunca YOK
    SAYILIR (ters rota da iletme de yok), süre dolunca yine işlenir.
    Veri çerçevesinin başarısızlığı kara listeye SOKMAZ."""
    from protokoller.aodv_bicim import BLACKLIST_TIMEOUT_S
    assert BLACKLIST_TIMEOUT_S == pytest.approx(6 * NET_TRAVERSAL_TIME_S)
    p = AODV(5)
    p.iletim_basarisiz(_gozlem(5, 1.0), hedef=3, tur="kontrol")
    assert p._sayac["kara_liste_eklenen"] == 1
    cikti = p.kontrol_alindi(_gozlem(5, 1.5), 3, "RREQ", _rreq_yuku(1), True)
    assert not _istekler(cikti), "kara listedeki komşunun RREQ'i iletildi"
    assert 0 not in p._rota, "kara listedeki RREQ ters rota kurdu"
    assert 3 not in p._komsu, "yok sayılan RREQ komşu kanıtı sayıldı"
    assert p._sayac["rreq_kara_listeden"] == 1
    # Başka bir komşudan gelen aynı RREQ normal işlenir.
    cikti = p.kontrol_alindi(_gozlem(5, 1.6), 4, "RREQ", _rreq_yuku(1), True)
    assert _istekler(cikti) and p._rota[0].sonraki == 4
    # Süre dolunca 3 yeniden kabul edilir (yeni bir keşif).
    t = 1.0 + BLACKLIST_TIMEOUT_S
    cikti = p.kontrol_alindi(_gozlem(5, t), 3, "RREQ", _rreq_yuku(2), True)
    assert _istekler(cikti), "süre dolduktan sonra RREQ işlenmedi"
    assert 3 not in p._kara_liste
    # Veri başarısızlığı kara listeye sokmaz.
    q = AODV(5)
    q.iletim_basarisiz(_gozlem(5, 1.0), hedef=3, tur="veri")
    assert not q._kara_liste and q._sayac["kara_liste_eklenen"] == 0


def test_K194_AOMDV_kara_listeyi_MIRAS_alir():
    """AOMDV, AODV'nin kanca ve kara listesini miras alır (§6.8, K-194)."""
    from protokoller.aomdv import AOMDV
    p = AOMDV(5)
    p.iletim_basarisiz(_gozlem(5, 1.0), hedef=3, tur="kontrol")
    cikti = p.kontrol_alindi(_gozlem(5, 1.5), 3, "RREQ", _rreq_yuku(1), True)
    assert not _istekler(cikti) and p._sayac["rreq_kara_listeden"] == 1



def test_K189_uygunluk_DESEN_secimi_ve_KAYIT_adi(monkeypatch):
    """Faz 4.3: `--desen` U1 koşularına deseni işçilere de taşır; kayıt
    dosyası desenin adını taşır (desenler birbirini ezmez)."""
    import kalibrasyon.aodv_uygunluk as U
    monkeypatch.delenv(U.DESEN_ORTAM, raising=False)
    monkeypatch.delenv("DESPARETE_DUNYA", raising=False)
    assert U._desen("aodv") == {}
    assert U._desen("desparete") == {"trafik_deseni": "yere_toplama"}
    assert U._kayit_adi("aodv") == "aodv"
    monkeypatch.setenv(U.DESEN_ORTAM, "yere_toplama")
    assert U._desen("aodv") == {"trafik_deseni": "yere_toplama"}
    monkeypatch.setenv("DESPARETE_DUNYA", "referans_2026")
    assert U._kayit_adi("olsr") == "olsr_referans_2026_yere_toplama"


def test_K191_hukum_DUNYA_uyusmazligini_reddeder(monkeypatch, tmp_path):
    """Referans dünyanın U1 kaydı `--dunya` verilmeden hükme sokulursa eski
    dünyanın açıklanmış hücreleri uygulanırdı — araç reddeder (K-191)."""
    import pytest
    import kalibrasyon.aodv_uygunluk as U
    kayit = tmp_path / "aomdv_referans_2026_yere_toplama_son.json"
    kayit.write_text('{"protokol": "aomdv", "hucreler": []}', encoding="utf-8")
    monkeypatch.delenv("DESPARETE_DUNYA", raising=False)
    with pytest.raises(SystemExit, match="referans"):
        U.hukum(kayit)
    eski = tmp_path / "aomdv_son.json"
    eski.write_text('{"protokol": "aomdv", "hucreler": []}', encoding="utf-8")
    monkeypatch.setenv("DESPARETE_DUNYA", "referans_2026")
    with pytest.raises(SystemExit, match="eski"):
        U.hukum(eski)


def test_U1_KAHIN_PAYLASIMI_ve_ARA_KAYIT(monkeypatch, tmp_path, capsys):
    """29 Eylül: aynı desendeki protokoller TEK kâhin koşusunu paylaşır ve
    her protokolün kaydı onu taşır; ara kayıttaki bitmiş koşu yeniden
    koşulmaz, hatalı koşu yeniden koşulur, başka kod hâlinin satırı reddedilir."""
    import json
    import pytest
    import kalibrasyon.aodv_uygunluk as U
    monkeypatch.setenv(U.DESEN_ORTAM, "yere_toplama")
    monkeypatch.setenv("DESPARETE_DUNYA", "referans_2026")
    monkeypatch.setattr(U, "DIZIN", tmp_path)
    monkeypatch.setattr(U, "_kod_imzasi", lambda: "A")
    # Sahte PDR'lerle gerçek açıklanmış hücre listesi "ölü kayıt" sayılırdı.
    monkeypatch.setattr(U, "ACIKLANMIS_DUSUK_REFERANS",
                        {p: {} for p in U.ACIKLANMIS_DUSUK_REFERANS})
    yol = U._ara_kayit_yolu()
    assert yol.name == "u1_ara_referans_2026_yere_toplama.jsonl"
    olcum = {"pdr": 0.5, "gecerli": True, "tampon": {}, "sure": 1.0}
    def satir(kahin, protokol, hata=None):
        return {"kol": "statik-yok", "tohum": 1000, "kahin": kahin,
                "protokol": protokol, "desen": "yere_toplama",
                "olcum": None if hata else olcum, "hata": hata, "kod": "A"}
    satirlar = [satir(False, "aodv", hata="X"), satir(True, None),
                satir(False, "aodv"), satir(False, "olsr")]
    yol.write_text("\n".join(json.dumps(r) for r in satirlar) + "\n",
                   encoding="utf-8")
    assert set(U._ara_kayit_oku(yol, "A")) == {
        ("statik-yok", 1000, k, (), p, "yere_toplama")
        for k, p in ((True, None), (False, "aodv"), (False, "olsr"))}
    with pytest.raises(SystemExit, match="başka bir kod"):
        U._ara_kayit_oku(yol, "B")
    # İki protokol, bir kol, bir tohum → 3 koşu (kâhin bir kez); hepsi ara
    # kayıtta olduğu için havuz açılmaz.
    assert U.u1(("statik-yok",), (1000,), protokol=("aodv", "olsr")) == 0
    assert "3 kosu (0 kaldi)" in capsys.readouterr().out
    for p in ("aodv", "olsr"):
        kayit = json.loads((tmp_path / f"{p}_referans_2026_yere_toplama_son.json"
                            ).read_text(encoding="utf-8"))
        assert kayit["protokol"] == p
        assert [(h["kahin"], h["olcum"]["pdr"]) for h in kayit["hucreler"]]             == [(False, 0.5), (True, 0.5)]


def test_REFERANS_ACIKLANMIS_HUCRE_DESEN_BASINA(monkeypatch, tmp_path, capsys):
    """30 Eylül: referans dünyanın açıklanmış hücre listesi desen başınadır —
    yere toplamada K-196'ya atıfla açıklanan OLSR hücresi, eşler arasında
    (keşifsel) aynı (kol, tohum) olsa da açıklanmış SAYILMAZ."""
    import json

    import kalibrasyon.aodv_uygunluk as U
    monkeypatch.setenv("DESPARETE_DUNYA", "referans_2026")
    monkeypatch.delenv(U.DESEN_ORTAM, raising=False)
    olcum = {"pdr": 0.64, "gecerli": True, "tampon": {}}
    kahin = {"pdr": 0.99, "gecerli": True, "tampon": {}}
    hucreler = [{"kol": "statik-yok", "tohum": 1000, "kahin": k,
                 "olcum": kahin if k else olcum, "hata": None}
                for k in (False, True)]
    assert ("yere_toplama", "statik-yok", 1000) in         U.ACIKLANMIS_DUSUK_REFERANS["olsr"]
    for desen, beklenen in (("yere_toplama", 0), ("esler_arasi", 1)):
        yol = tmp_path / f"olsr_referans_2026_{desen}_son.json"
        yol.write_text(json.dumps({"protokol": "olsr", "hucreler": hucreler}),
                       encoding="utf-8")
        assert U.hukum(yol) == beklenen, desen
        cikti = capsys.readouterr().out
        assert f"desen  : {desen}" in cikti
        assert ("DUSUK (aciklanmis)" in cikti) == (beklenen == 0)


# ==========================================================================
# K-205 · SIRA NUMARASI KURALLARI — RFC 3561 §6.2 · §6.7 · §6.11 (ns-3 ile aynı)
# ==========================================================================
def _rrep(hedef_sira: int, atlama: int = 1, kaynak: int = 0,
          hedef: int = 9) -> dict:
    return {"kaynak": kaynak, "hedef": hedef, "hedef_sira": hedef_sira,
            "atlama": atlama, "omur_ms": 3000}


def test_K205_BAYAT_RREP_gecersiz_girdiyi_GUNCELLEMEZ():
    """🔴 §6.7 (i)–(iv): geçersiz girdi yalnız EŞİT ya da büyük sırayla
    güncellenir. İlk yazımda her RREP kabul ediliyordu; daha küçük sıralı
    (kopmadan önceki bir yolu anlatan) RREP döngü kuruyordu (K-205)."""
    p = AODV(5)
    p._rota[9] = Rota(sonraki=1, atlama=2, hedef_sira=7, gecerli=False,
                      son_gecerli_s=0.0, silme_s=100.0)
    p._rrep_isle(3, _rrep(hedef_sira=6), 1.0)
    assert p._rota[9].sonraki == 1 and not p._rota[9].gecerli, "bayat kabul"
    p._rrep_isle(3, _rrep(hedef_sira=7, atlama=4), 1.1)        # (iii)
    assert p._rota[9].sonraki == 3 and p._rota[9].gecerli
    assert p._rota[9].hedef_sira == 7 and p._rota[9].atlama == 5
    p._rrep_isle(4, _rrep(hedef_sira=7, atlama=5), 1.2)        # eşit, uzun
    assert p._rota[9].sonraki == 3
    p._rrep_isle(4, _rrep(hedef_sira=7, atlama=2), 1.3)        # (iv)
    assert p._rota[9].sonraki == 4 and p._rota[9].atlama == 3
    p._rrep_isle(6, _rrep(hedef_sira=8, atlama=9), 1.4)        # (ii)
    assert p._rota[9].sonraki == 6 and p._rota[9].hedef_sira == 8


def test_K205_komsu_rotasi_SIRASIZ_ve_gecersizlestirme_kurallari():
    """§6.2: komşu rotası geçerli sıra OLMADAN kurulur (ns-3
    `UpdateRouteToNeighbor`) ve (i) ile her RREP'le güncellenebilir. §6.11
    madde 1: sıra yalnız geçerliyse artar, RERR'de RERR'den kopyalanır."""
    p = AODV(5)
    p._rota[3] = Rota(sonraki=4, atlama=2, hedef_sira=8, gecerli=False,
                      silme_s=100.0)
    p._komsu_rotasi(3, 1.0)
    assert p._rota[3].hedef_sira == SONSUZ_SIRA and p._rota[3].atlama == 1
    p._rrep_isle(4, _rrep(hedef_sira=2, atlama=1, hedef=3), 1.1)   # (i)
    assert p._rota[3].hedef_sira == 2 and p._rota[3].sonraki == 4
    p._rota[7] = Rota(sonraki=3, atlama=1, hedef_sira=SONSUZ_SIRA)
    p._gecersizlestir(p._rota[7], 2.0)
    assert p._rota[7].hedef_sira == SONSUZ_SIRA, "bilinmeyen sıra uyduruldu"
    p._rota[8] = Rota(sonraki=3, atlama=2, hedef_sira=8)
    p._gecersizlestir(p._rota[8], 2.0)
    assert p._rota[8].hedef_sira == 9                          # yerel: +1
    p._rota[9] = Rota(sonraki=1, atlama=2, hedef_sira=5, son_gecerli_s=100.0)
    p._rerr_isle(1, {"ulasilamaz": (9,), "ulasilamaz_sira": (12,)}, 3.0)
    assert not p._rota[9].gecerli and p._rota[9].hedef_sira == 12


def test_K205_kaynak_REDDEDILEN_RREPle_kesfi_KAPATMAZ():
    """Keşif yalnız kullanılabilir rota varsa biter: bayat RREP keşfi
    "başarılı" sayıp kapatsaydı tampondaki paket rotasız beklerdi (AOMDV'de
    22 Eylül'de ölçülen tuzak)."""
    p = AODV(0)
    p._rota[9] = Rota(sonraki=1, atlama=2, hedef_sira=7, gecerli=False,
                      silme_s=100.0)
    karar = p.sonraki_atlama(_gozlem(0, 1.0, paket_hedefi=9))
    assert karar.beklet and 9 in p._kesif
    assert dict(_istekler(karar.niyetler)[0].yuk)["hedef_sira"] == 7
    assert p._rrep_isle(3, _rrep(hedef_sira=6), 1.1) == ()
    assert 9 in p._kesif and p._sayac["kesif_basarili"] == 0
    cikti = p._rrep_isle(3, _rrep(hedef_sira=7), 1.2)
    assert 9 not in p._kesif and p._sayac["kesif_basarili"] == 1
    assert _uyandirmalar(cikti), "tampon yeniden sorulmadı"


def test_K208_AOMDV_sira_kurali_AODVden_MIRAS():
    """AOMDV'nin §6.11 sıra kuralı AODV'den miras (K-208): bilinmeyen sıra
    bilinmeyen kalır, ömür dolması sırayı değiştirmez, yerel kopmada artar.
    AOMDV'nin kendi ilan kuralı (Şekil 3, S10) ayrı ve değişmedi."""
    from protokoller.aomdv import AOMDV
    q = AOMDV(5)
    q._komsu_rotasi(3, 1.0)
    assert q._rota[3].hedef_sira == SONSUZ_SIRA
    q._gecersizlestir(q._rota[3], 2.0)
    assert q._rota[3].hedef_sira == SONSUZ_SIRA and not q._rota[3].yollar
    assert q._son_atlama(q._rota[3]) is None, "yolsuz girdi atlama bilmez"


def test_K192b_KAHIN_ASIMI_ZARF_KAYDI(monkeypatch, tmp_path, capsys):
    """K-192 (b): zarf içinde kalan kâhin aşımı kayıtlıysa U1-U geçer; aynı
    hücre başka desende ya da kayıtsız aşım kalır; aşmayan kayıt ÖLÜ kayıttır."""
    import json

    import kalibrasyon.aodv_uygunluk as U
    monkeypatch.setenv("DESPARETE_DUNYA", "referans_2026")
    monkeypatch.delenv(U.DESEN_ORTAM, raising=False)
    monkeypatch.setattr(U, "KAHIN_ASIMI_ACIKLANMIS", {
        "aomdv": {("esler_arasi", "formasyon-yok", 1000): "zarf"}})
    monkeypatch.setattr(U, "KAYITLI_ORAN", {
        "aomdv": {("esler_arasi", "formasyon-yok", 1000): 0.975 / 0.97}})

    def kayit(desen, pdr):
        hucreler = [{"kol": "formasyon-yok", "tohum": 1000, "kahin": k,
                     "olcum": {"pdr": 0.97 if k else pdr, "gecerli": True,
                               "tampon": {}}, "hata": None}
                    for k in (False, True)]
        yol = tmp_path / f"aomdv_referans_2026_{desen}_son.json"
        yol.write_text(json.dumps({"protokol": "aomdv", "hucreler": hucreler}),
                       encoding="utf-8")
        return yol

    assert U.hukum(kayit("esler_arasi", 0.975)) == 0
    assert "kahin asimi ACIKLANMIS" in capsys.readouterr().out
    assert U.hukum(kayit("yere_toplama", 0.975)) == 1       # kayıtsız desen
    assert "KAHINI GECTI" in capsys.readouterr().out
    assert U.hukum(kayit("esler_arasi", 0.96)) == 1         # aşım yok → ölü
    assert "OLU ZARF KAYDI" in capsys.readouterr().out
    # DD-07 (K-242): kayıtlı aşımdan R'den fazla büyük aşım kayıtla örtülmez.
    assert U.hukum(kayit("esler_arasi", 0.995)) == 1
    assert "KAYIT SAPTI" in capsys.readouterr().out


def test_DD07_ACIKLANMIS_DUSUK_HUCRE_KAYITLI_ORANA_BAGLI(monkeypatch, tmp_path,
                                                        capsys):
    """Denetim DD-07 (K-242): açıklanmış düşük hücre yalnız kayıtlı oranının
    R kadar yakınında açıklanmış sayılır; AODV-j'nin 0,894'lük hücresi
    0,45'e düşerse kapı kalır."""
    import json

    import kalibrasyon.aodv_uygunluk as U
    monkeypatch.setenv("DESPARETE_DUNYA", "referans_2026")
    monkeypatch.delenv(U.DESEN_ORTAM, raising=False)
    kayitli = U.KAYITLI_ORAN["aodv"][("yere_toplama", "statik-yok", 1000)]

    def kayit(oran):
        hucreler = [{"kol": "statik-yok", "tohum": 1000, "kahin": k,
                     "olcum": {"pdr": 0.99 if k else 0.99 * oran,
                               "gecerli": True, "tampon": {}}, "hata": None}
                    for k in (False, True)]
        yol = tmp_path / "aodv_referans_2026_yere_toplama_son.json"
        yol.write_text(json.dumps({"protokol": "aodv", "hucreler": hucreler}),
                       encoding="utf-8")
        return yol

    assert U.hukum(kayit(kayitli)) == 0
    assert "DUSUK (aciklanmis)" in capsys.readouterr().out
    assert U.hukum(kayit(0.45)) == 1
    assert "KAYIT SAPTI" in capsys.readouterr().out


# ==========================================================================
# K-208 · SADAKAT DENETİMİ — RFC 3561 (birincil) ve ns-3 (hakem), H1–H11
# `arsiv/teshis/aodv_sadakat_2026-09-30/denetim.md`
# ==========================================================================
def _rreq(hedef_sira: int = 0, kaynak: int = 0, hedef: int = 9,
          kimlik: int = 1, atlama: int = 0, kaynak_sira: int = 3) -> tuple:
    return tuple({"tip": TIP_RREQ, "bayraklar": 1 if hedef_sira == 0 else 0,
                  "ayrilmis": 0, "atlama": atlama, "rreq_kimlik": kimlik,
                  "hedef": hedef, "hedef_sira": hedef_sira, "kaynak": kaynak,
                  "kaynak_sira": kaynak_sira, "ttl": 10}.items())


def test_K208_H1_RREQ_onceki_atlamanin_sirasini_GECERSIZ_yapar():
    """§6.5 ilk cümle: önceki atlamaya rota *"without a valid sequence
    number"* (ns-3 `RecvRequest`)."""
    p = AODV(5)
    p._rota[4] = Rota(sonraki=4, atlama=1, hedef_sira=7, son_gecerli_s=9.0)
    p._komsu[4] = 0.5
    p.kontrol_alindi(_gozlem(5, 1.0), 4, "RREQ", _rreq(kaynak=0), True)
    assert p._rota[4].hedef_sira == SONSUZ_SIRA


def test_K208_H2_ters_rota_KOSULSUZ_sira_ve_omur_BUYUGU():
    """§6.5 (1)–(5): ters rota tekrar olmayan her RREQ'te güncellenir; sıra
    büyüğü, ömür büyüğü tutulur (ns-3 `RecvRequest`)."""
    p = AODV(5)
    p._rota[0] = Rota(sonraki=2, atlama=1, hedef_sira=9, son_gecerli_s=50.0)
    p._ters_rota(0, kaynak_sira=4, atlama=3, sonraki=6, simdi_s=1.0)
    r = p._rota[0]
    assert r.sonraki == 6 and r.atlama == 3, "ters rota güncellenmeli"
    assert r.hedef_sira == 9, "sıra küçülemez (copied if greater)"
    assert r.son_gecerli_s == 50.0, "ömür kısalamaz (max)"


def test_K208_H3_iletilen_RREQin_sirasi_BILINENIN_BUYUGUNE_cikar():
    """§6.5: *"set to the maximum of"* gelen ile bilinen; U bayrağı iner;
    düğüm kendi değerini değiştirmez."""
    p = AODV(5)
    p._rota[9] = Rota(sonraki=1, atlama=2, hedef_sira=7, gecerli=False,
                      silme_s=100.0)
    cikti = p.kontrol_alindi(_gozlem(5, 1.0), 4, "RREQ",
                             _rreq(hedef_sira=0), True)
    iletilen = [dict(i.yuk) for i in _istekler(cikti) if i.bicim is RREQ]
    assert iletilen and iletilen[0]["hedef_sira"] == 7
    assert iletilen[0]["bayraklar"] == 0
    assert p._rota[9].hedef_sira == 7


def test_K208_H4_ara_dugum_U_bayrakli_RREQe_cevap_ve_IKI_oncul():
    """§6.6.2: etkin rota + geçerli sıra → U bayraklı RREQ'e de cevap (ns-3
    hakem); ileri rotaya gönderen, ters rotaya hedefe doğru sonraki atlama."""
    p = AODV(5)
    p._rota[9] = Rota(sonraki=1, atlama=2, hedef_sira=7, son_gecerli_s=100.0)
    cikti = p.kontrol_alindi(_gozlem(5, 1.0), 4, "RREQ",
                             _rreq(hedef_sira=0), True)
    rrep = [i for i in _istekler(cikti) if i.bicim is RREP]
    assert rrep and dict(rrep[0].yuk)["hedef_sira"] == 7
    assert 4 in p._rota[9].oncular and 1 in p._rota[0].oncular
    q = AODV(5)                                  # sırası bilinmeyen rota: cevap yok
    q._rota[9] = Rota(sonraki=1, atlama=1, hedef_sira=SONSUZ_SIRA,
                      son_gecerli_s=100.0)
    cikti = q.kontrol_alindi(_gozlem(5, 1.0), 4, "RREQ",
                             _rreq(hedef_sira=0), True)
    assert not [i for i in _istekler(cikti) if i.bicim is RREP]


def test_K208_H5_RREP_yalniz_GUNCELLEDIYSE_iletilir_ve_omur_UZAMAZ():
    """§6.7: *"AND a forward route has been created or updated"*; reddedilen
    RREP ömür uzatmaz; iletimde ters rota ömrü ve komşu öncülü güncellenir."""
    p = AODV(5)
    p._rota[0] = Rota(sonraki=2, atlama=1, hedef_sira=3, son_gecerli_s=1.5)
    p._rota[9] = Rota(sonraki=1, atlama=2, hedef_sira=7, son_gecerli_s=10.0)
    assert p._rrep_isle(3, _rrep(hedef_sira=7, atlama=4), 1.0) == ()
    assert p._rota[9].son_gecerli_s == 10.0, "reddedilen RREP ömür uzattı"
    p._rota[3] = Rota(sonraki=3, atlama=1, hedef_sira=SONSUZ_SIRA,
                      son_gecerli_s=5.0)
    cikti = p._rrep_isle(3, _rrep(hedef_sira=8, atlama=1), 1.0)
    assert [i for i in _istekler(cikti) if i.bicim is RREP], "iletilmedi"
    assert p._rota[0].son_gecerli_s == 1.0 + ACTIVE_ROUTE_TIMEOUT_S
    assert 2 in p._rota[9].oncular and 2 in p._rota[3].oncular


def test_K208_H6_HELLO_komsu_rotasina_SIRAYI_yazar():
    """§6.9: *"MUST … the latest Destination Sequence Number from the Hello"*."""
    p = AODV(8)
    hello = tuple({"tip": TIP_RREP, "bayraklar": 0, "ayrilmis": 0,
                   "onek_boyu": 0, "atlama": 0, "hedef": 7, "hedef_sira": 5,
                   "kaynak": 7, "omur_ms": 2000}.items())
    p.kontrol_alindi(_gozlem(8, 1.0), 7, "RREP", hello, True)
    r = p._rota[7]
    assert r.gecerli and r.atlama == 1 and r.hedef_sira == 5
    assert r.son_gecerli_s >= 1.0 + ALLOWED_HELLO_LOSS * HELLO_INTERVAL_S


def test_K208_H8_rotasiz_ARA_dugum_DUSURUR_tamponlamaz():
    """§6.11 (ii): girdisiz → `hedef_yok` + RERR; süresi dolmuş geçerli girdi
    → geçersizleşir (sıra +1), RERR, `rota_gecersiz`; keşif YOK."""
    p = AODV(5)
    karar = p.sonraki_atlama(_gozlem(5, 1.0, paket_hedefi=9, paket_kaynagi=0))
    assert not karar.beklet and karar.sonraki is None and not karar.beyan
    assert 9 not in p._kesif
    # 🔒 K-210: (ii)'nin RERR'i öncüle bakmadan gider (ns-2/ns-3; RFC'nin
    # süzme cümlesi normatif değil) — sıra bilinmiyor (0).
    rerr = [dict(i.yuk) for i in _istekler(karar.niyetler) if i.bicim is RERR]
    assert rerr and rerr[0]["ulasilamaz"] == (9,)
    assert rerr[0]["ulasilamaz_sira"] == (SONSUZ_SIRA,)
    p._rota[9] = Rota(sonraki=1, atlama=2, hedef_sira=5, son_gecerli_s=0.5,
                      oncular={0})
    karar = p.sonraki_atlama(_gozlem(5, 1.0, paket_hedefi=9, paket_kaynagi=0))
    assert not karar.beklet and [b.tip for b in karar.beyan] == ["rota_gecersiz"]
    assert not p._rota[9].gecerli and p._rota[9].hedef_sira == 6
    assert [i for i in _istekler(karar.niyetler) if i.bicim is RERR]
    p._rota[9].silme_s = 2.0
    p.sonraki_atlama(_gozlem(5, 3.0, paket_hedefi=9, paket_kaynagi=0))
    assert p._rota[9].silme_s == 3.0 + DELETE_PERIOD_S


def test_K208_H9_omru_dolan_rotanin_sirasi_ARTMAZ():
    """§6.11 madde 1 sırayı yalnız RERR durumlarında değiştirir (ns-3
    `Purge` de dokunmaz)."""
    p = AODV(5)
    p._rota[9] = Rota(sonraki=1, atlama=2, hedef_sira=5, son_gecerli_s=0.5)
    p._bakim(1.0)
    assert not p._rota[9].gecerli and p._rota[9].hedef_sira == 5


def test_K208_H10_hiz_sinirinda_RREQ_ERTELENIR_kesif_takilmaz():
    """§10 `RREQ_RATELIMIT` (ns-3 `SendRequest`): aşan RREQ ertelenir, pencere
    dolunca aynı adım gönderilir. İlk yazımda yeniden deneme zamanlayıcısız
    dönüyor ve keşif kalıcı olarak takılıyordu."""
    from protokoller.aodv_bicim import RREQ_RATELIMIT
    p = AODV(0)
    p._rreq_pencere[:] = [1.0, float(RREQ_RATELIMIT)]       # pencere dolu
    karar = p.sonraki_atlama(_gozlem(0, 1.2, paket_hedefi=9))
    assert karar.beklet and 9 in p._kesif
    assert not [i for i in _istekler(karar.niyetler) if i.bicim is RREQ]
    ertele = _uyandirmalar(karar.niyetler)
    assert ertele and ertele[0].etiket.startswith("kesif_ertele:9:")
    assert ertele[0].gecikme_s == pytest.approx(0.8 + 1e-4)
    cikti = p.uyandi(_gozlem(0, 2.0001), ertele[0].etiket)
    rreq = [dict(i.yuk) for i in _istekler(cikti) if i.bicim is RREQ]
    assert rreq and rreq[0]["ttl"] == TTL_START
    assert p._sayac["rreq_ertelenen"] == 1


def test_K208_H11_ag_capinda_bekleme_ve_ESKI_NESIL_yok_sayilir():
    """§6.3: ağ çapında ilk bekleme `NET_TRAVERSAL_TIME`, sonra iki katı
    (ns-3); biten keşfin eski zamanlayıcısı yeni keşfi ilerletmez."""
    p = AODV(0)
    karar = p.sonraki_atlama(_gozlem(0, 1.0, paket_hedefi=9))
    etiket = _uyandirmalar(karar.niyetler)[0].etiket
    t, beklemeler = 1.0, []
    while True:
        t += 20.0
        cikti = p.uyandi(_gozlem(0, t), etiket)
        u = _uyandirmalar(cikti)
        istek = [dict(i.yuk) for i in _istekler(cikti) if i.bicim is RREQ]
        if not u:
            break
        etiket = u[0].etiket
        if istek and istek[0]["ttl"] == NET_DIAMETER:
            beklemeler.append(u[0].gecikme_s)
    assert beklemeler == [pytest.approx(NET_TRAVERSAL_TIME_S),
                          pytest.approx(2 * NET_TRAVERSAL_TIME_S)]
    q = AODV(0)
    ilk = _uyandirmalar(q.sonraki_atlama(
        _gozlem(0, 1.0, paket_hedefi=9)).niyetler)[0].etiket
    del q._kesif[9]                                     # keşif bitti
    q.sonraki_atlama(_gozlem(0, 1.1, paket_hedefi=9))   # yeni nesil
    assert q.uyandi(_gozlem(0, 1.2), ilk) == ()
    assert q._kesif[9].ttl == TTL_START, "eski zamanlayıcı yeni keşfi ilerletti"


def test_K215_AODV_baslangici_YEREL_SAATIN_SIFIRINA_bagli_degil():
    """Faz 4.4: sonuç saat ofsetine bağlıydı. Başlangıç "hiç olmadı" (−∞):
    negatif yerel saatte ilk HELLO gider (§6.9) ve §10'un ilk "saniye"si ilk
    olayda açılır — yerel 0'a kadar uzamaz."""
    from protokoller.aodv_bicim import RREQ_RATELIMIT

    assert AODV(0)._hello(-0.5), "negatif yerel saatte HELLO susturuldu"
    b = AODV(1)
    for _ in range(RREQ_RATELIMIT):
        assert not b._hiz_sinirli_mi(b._rreq_pencere, RREQ_RATELIMIT, -0.8)
    assert b._hiz_sinirli_mi(b._rreq_pencere, RREQ_RATELIMIT, -0.8)
    # İlk pencere −0,8'de açıldı; 1,01 s sonra yeni pencere (eskiden yerel
    # 1,0'a kadar, yani 1,8 s sürerdi).
    assert not b._hiz_sinirli_mi(b._rreq_pencere, RREQ_RATELIMIT, 0.21)


def test_K215_kahin_beaconi_AODV_HELLO_cercevesiyle_BIREBIR():
    """Referans dünyada kâhinin beacon'ı = AODV HELLO çerçevesi: RREP (RFC
    3561 §5.2) + kontrol kapsüllemesi. sim2 protokolü içe aktaramadığı için
    20 sayısı burada RREP biçimine bağlanır; TTL de IP varsayılanı (G17)."""
    from sim2.kanal.cerceve import cerceve_kur, kontrol_kapsulleme_bayt
    from sim2.kanal.dunya import REFERANS_BEACON_BAYT, REFERANS_TTL, referans_2026

    y_rrep = {"tip": TIP_RREP, "bayraklar": 0, "ayrilmis": 0, "onek_boyu": 0,
              "atlama": 0, "hedef": 2, "hedef_sira": 1, "kaynak": 2,
              "omur_ms": 2000}
    hello = RREP.bayt(y_rrep) + kontrol_kapsulleme_bayt()
    assert REFERANS_BEACON_BAYT == hello == 84
    k = referans_2026(kol="t", senaryo="statik-yok", tohum=1000)
    assert k.beacon_bayt == hello and k.beacon_araligi_s == HELLO_INTERVAL_S
    assert cerceve_kur(k, "beacon").bayt == cerceve_kur(
        k, "kontrol", mesaj_bayt=RREP.bayt(y_rrep)).bayt
    assert k.ttl_baslangic == REFERANS_TTL == 64


# ==========================================================================
# K-244 · ns-3'ün varsayılanları: karşılıksız RREP · RERR'in iletim biçimi ·
# kara listenin tür eşlemesi
# ==========================================================================
def test_K244_RREQ_G_BAYRAGI_ve_KARSILIKSIZ_RREP_6_6_3():
    """Kaynak her RREQ'te G kurar (ns-3 `GratuitousReply`); yanıt veren ara
    düğüm hedefe karşılıksız RREP'i RFC'nin alanlarıyla gönderir; iletilen
    RREQ'te U iner, G kalır."""
    from protokoller.aodv_bicim import BAYRAK_G, BAYRAK_U, RREP, TIP_RREQ
    p = AODV(0)
    ist = p._rreq_kur(7, 1, 0.0)
    assert dict(ist.yuk)["bayraklar"] == BAYRAK_G | BAYRAK_U
    ara = AODV(5)
    ara._rota[7] = Rota(sonraki=6, atlama=2, hedef_sira=9,
                        son_gecerli_s=50.0)
    y = {"tip": TIP_RREQ, "bayraklar": BAYRAK_G, "ayrilmis": 0, "atlama": 1,
         "rreq_kimlik": 4, "hedef": 7, "hedef_sira": 8, "kaynak": 0,
         "kaynak_sira": 3, "ttl": 5}
    cikti = ara.kontrol_alindi(_gozlem(5, 1.0), 4, "RREQ",
                               tuple(y.items()), True)
    rrep = [i for i in _istekler(cikti) if i.bicim is RREP]
    assert [i.hedef for i in rrep] == [4, 6]
    g = dict(rrep[1].yuk)
    assert (g["hedef"], g["hedef_sira"], g["kaynak"], g["atlama"]) == \
        (0, 3, 7, 2)
    assert ara._sayac["rrep_karsiliksiz"] == 1
    # G'siz RREQ'te karşılıksız RREP yok.
    ara2 = AODV(5)
    ara2._rota[7] = Rota(sonraki=6, atlama=2, hedef_sira=9,
                         son_gecerli_s=50.0)
    cikti = ara2.kontrol_alindi(_gozlem(5, 1.0), 4, "RREQ",
                                tuple(dict(y, bayraklar=0).items()), True)
    assert [i.hedef for i in _istekler(cikti) if i.bicim is RREP] == [4]
    # İletilen RREQ: U iner, G kalır.
    ara3 = AODV(5)
    ara3._rota[7] = Rota(sonraki=6, atlama=2, hedef_sira=12,
                         gecerli=False, son_gecerli_s=50.0)
    cikti = ara3.kontrol_alindi(
        _gozlem(5, 1.0), 4, "RREQ",
        tuple(dict(y, bayraklar=BAYRAK_G | BAYRAK_U, hedef_sira=0).items()),
        True)
    iletilen = [dict(i.yuk) for i in _istekler(cikti)
                if i.bicim is not RREP and i.yayin_mi]
    assert iletilen and iletilen[0]["bayraklar"] == BAYRAK_G


def test_K244_RERR_ILETIM_BICIMI_ns3():
    """İki öncül → yayın; rotasız tek öncül → gönderilmez; (ii) veri
    kaynağına rota varsa onun sonraki atlamasına tek-yayın, yoksa yayın."""
    p = AODV(0)
    p._rota[9] = Rota(sonraki=1, atlama=2, hedef_sira=5,
                      son_gecerli_s=100.0, oncular={3, 4})
    p._rota[3] = Rota(sonraki=3, atlama=1, hedef_sira=0, son_gecerli_s=100.0)
    rerr = p._rerr_kur((9,), 1.0)
    assert len(rerr) == 1 and rerr[0].yayin_mi
    q = AODV(0)
    q._rota[9] = Rota(sonraki=1, atlama=2, hedef_sira=5,
                      son_gecerli_s=100.0, oncular={3})
    assert q._rerr_kur((9,), 1.0) == ()
    assert q._rerr_pencere[1] == 0.0          # hız sınırı hakkı harcanmadı
    r = AODV(0)
    r._rota[2] = Rota(sonraki=8, atlama=3, hedef_sira=4, son_gecerli_s=100.0)
    tek = r._rerr_kur((9,), 1.0, oncul_suz=False, veri_kaynagi=2)
    assert tek[0].hedef == 8 and not tek[0].yayin_mi
    yayin = r._rerr_kur((9,), 1.0, oncul_suz=False, veri_kaynagi=11)
    assert yayin[0].yayin_mi


def test_K244_KARA_LISTE_YALNIZ_RREP_BASARISIZLIGINDA():
    """`iletim_sonucu` tek-yayın kontrol çerçevesinin türünü komşu başına
    sırayla eşler: RERR'in başarısızlığı kara liste kurmaz, RREP'inki kurar;
    eşleme yoksa RREP sayılır (önceki davranış)."""
    p = AODV(0)
    p._rota[9] = Rota(sonraki=1, atlama=2, hedef_sira=5,
                      son_gecerli_s=100.0, oncular={3})
    p._rota[3] = Rota(sonraki=3, atlama=1, hedef_sira=0, son_gecerli_s=100.0)
    p._rrep_kur(9, 5, 2, 0, 3.0, 3)                 # RREP → 3
    p._rerr_kur((9,), 1.0)                          # RERR → 3
    p.iletim_sonucu(_gozlem(0, 1.1), 3, True, 0, "kontrol")   # RREP onaylandı
    p.iletim_sonucu(_gozlem(0, 1.2), 3, False, 6, "kontrol")  # RERR başarısız
    p.iletim_basarisiz(_gozlem(0, 1.2), 3, "kontrol")
    assert 3 not in p._kara_liste
    p._rrep_kur(9, 5, 2, 0, 3.0, 4)
    p.iletim_sonucu(_gozlem(0, 1.3), 4, False, 6, "kontrol")
    p.iletim_basarisiz(_gozlem(0, 1.3), 4, "kontrol")
    assert 4 in p._kara_liste
    p.iletim_basarisiz(_gozlem(0, 1.4), 5, "kontrol")   # eşleme yok → RREP
    assert 5 in p._kara_liste
