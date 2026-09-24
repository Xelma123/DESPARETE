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
    RREQ_RETRIES, TIP_RERR, TIP_RREP, TIP_RREQ, TTL_INCREMENT, TTL_START,
    TTL_THRESHOLD, halka_suresi_s)
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
    p._rota[9] = Rota(sonraki=1, atlama=2, hedef_sira=5,
                      son_gecerli_s=100.0, oncular={3})

    cikti = p.iletim_basarisiz(_gozlem(0, 1.0), hedef=1, tur="veri")

    beyan = _beyanlar(cikti)
    assert any(b.tip == "kopma" and b.komsu == 1 for b in beyan), (
        "MAC vazgeçti ama protokol KOPMA bildirmedi")
    rerr = [i for i in _istekler(cikti) if i.bicim is RERR]
    assert len(rerr) == 1, "RERR üretilmedi"
    assert dict(rerr[0].yuk)["ulasilamaz"] == (9,)
    assert rerr[0].yayin_mi, "RERR yayın olarak gider"
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
    assert y["ttl"] == TTL_START, "genişleyen halka TTL_START ile başlar"
    assert _uyandirmalar(karar.niyetler), "keşif zaman aşımı kurulmadı"


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

    # …ama GERÇEK bir RREP (kaynak ≠ hedef) İLETİLİR.
    alan._rota[3] = Rota(sonraki=9, atlama=1, hedef_sira=1,
                         son_gecerli_s=100.0)
    gercek = dict(hello[0].yuk) | {"kaynak": 3}
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
    # 🔒 Öncül 3 — RERR'in yayılması için (K-143).
    p._rota[9] = Rota(sonraki=1, atlama=2, hedef_sira=5, son_gecerli_s=100.0,
                      oncular={3})
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
