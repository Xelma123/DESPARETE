"""
Babel — RFC 8966 (Chroboczek & Schinazi, 2021, Standards Track).

Kaynağına sadık gerçekleme (K-242). Biçimler, sabitler ve RFC'nin seçeneğe
bıraktığı her yerin kararı `babel_bicim.py`nin beyan tablosunda; RFC'nin
açık değer vermediği seçeneklerde ve MAY'lerde hakem babeld 1.14.

🔒 KÂHİN ERİŞİMİ YOK
Yalnız `sim2/gozlem/`i içe aktarır. Bildiği her şey aldığı bir Babel
paketinden ya da kendi saatinden gelir. Bağ maliyeti (ETX, Ek A.2.2)
komşunun çoklu-yayın Hello'larının geçmişinden KENDİ ölçülür; ters yönün
maliyeti komşunun IHU'sundan gelir.

🔒 TEK ARAYÜZ, TEK ADRES · HER DÜĞÜM KENDİ /32 ÖNEKİNİ DUYURUR
Komşu tablosu, kaynak tablosu (uygulanabilirlik mesafeleri), rota tablosu
(önek × komşu) ve sıra istekleri listesi RFC 8966 §3.2'deki gibi. Her önek
tek bir yönlendiriciden çıkar ve router-id'si önekten türer (beyan tablosu).

🔒 KURULU ROTA (babeld)
Seçili rotanın metriği ∞ olunca (geri çekme, komşu kaybı, süre dolumu)
babeld onu kayıt silinene dek "kurulu" tutar: çekirdekte ulaşılamaz rota
olarak durur, periyodik dökümde geri çekme olarak duyurulur ve aynı öneke
yeni rota seçildiğinde tetiğin aciliyeti ona göre belirlenir. `_kurulu` bunu
taşır. Veri düzleminde ∞ rota "rota yok"tur (paket düşer).

🔒 TETİKLER KANCA SONUNDA · GİDEN TLV'LER TAMPONDA
Her kanca sonunda zamanlayıcılar işlenir, rota seçimi (§3.6) koşar ve her
önekin seçili rotası bir önceki kanca sonundakiyle karşılaştırılır; babeld'in
`send_triggered_update` · `consider_route` · `route_lost` kuralları bu farka
uygulanır. Giden TLV'ler hedef başına (çoklu-yayın ya da komşu) tampona girer
(§3.1; babeld'in arayüz ve komşu tamponları): ilk acil TLV tamponu
U(0, 0,2 s), öteki TLV'ler U(0, Hello/2) içinde boşaltır. Aynı önekin
duyuruları tek Update'e iner ve gönderim anındaki hâliyle kurulur; Hello,
periyodik döküm ve açılış paketi bekleyen çoklu-yayın tamponunu da taşır.

🔒 ZAMANLAYICILAR
Hello ve periyodik tam döküm kendi titreşimli zincirlerinde; komşu Hello
zaman aşımı, IHU tutma, rota süresi, süre dolmadan rota isteği, istek
yinelemesi ve ömrü, tetik yinelemesi ve kaynak tablosunun çöp toplaması bir
"en erken son tarih" uyandırmasıyla işlenir (beyan tablosu).

🔒 ÖLÇÜM BEYANLARI — AODV, OLSRv2 ve DESPARETE ile AYNI anlam (K-139)
    kopma(K)         komşu K kullanılamaz oldu (maliyet ∞ ya da silindi) VE
                     en az bir seçili rotanın sonraki atlamasıydı
    rota_kuruldu(K)  K'nin kaybının etkilediği bir hedefe yeniden rota var
    rota_gecersiz    daha önce rotası olan bir hedefe artık rota yok
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from sim2.gozlem.karar import Beyan, Karar
from sim2.gozlem.kontrol import KontrolIstegi, Uyandirma
from sim2.gozlem.pencere import Gozlem
from protokoller.babel_bicim import (
    ACIL_ZAMAN_ASIMI_S, BABEL, ETX_CEZA_S, ETX_SONSUZ_MASKE, ETX_SONSUZ_S,
    GECMIS_BIT, GUNCELLEME_ARALIGI_S, HELLO_ARALIGI_S,
    HELLO_ZAMAN_ASIMI_KATSAYISI, IHU_ARALIGI_S, IHU_KAYIPLI_MASKE,
    IHU_TUTMA_KATSAYISI, IHU_TXCOST_ESIGI, ISTEK_LISTE_S, ISTEK_TEKRAR,
    ISTEK_ZAMAN_ASIMI_S, IYILESME_YOKSAY, KAYNAK_GC_S, KOTULESME_FARKI,
    KOTULESME_TABANI, ONEMSIZ_FARK, PAKET_UST_SINIRI_B, ROTA_ISTEGI_KOTULESME,
    ROTA_ISTEGI_ORANI, ROTA_SURESI_KATSAYISI, SIRA_ISTEGI_HOP, SONSUZ,
    TERCIH_FARKI, TETIK_YENIDEN_S, YARI_OMUR_S,
    BicimHatasi, Guncelleme, Hello, Ihu, RotaIstegi, SiraIstegi, adres,
    dugum, paket_coz, paket_kodla, sira_artir, sira_kucuk)

__all__ = ["Babel", "maliyet", "rxcost", "metrik"]

_HELLO, _DOKUM, _ACILIS, _ZAMAN = "hello", "dokum", "acilis", "zaman:"
_BOSALT = "bosalt:"
_MASKE = (1 << GECMIS_BIT) - 1
_EN_YENI = 1 << (GECMIS_BIT - 1)
_J_HELLO = HELLO_ARALIGI_S / 4                  # RFC 5148 §5 MAXJITTER
_J_DOKUM = GUNCELLEME_ARALIGI_S / 4
_J_NORMAL = HELLO_ARALIGI_S / 2                 # §3.1: acil olmayan TLV
_HELLO_CS = int(HELLO_ARALIGI_S * 100)
_IHU_CS = int(IHU_ARALIGI_S * 100)
_ARALIK_CS = int(GUNCELLEME_ARALIGI_S * 100)
_YARI_SONSUZ = SONSUZ // 2


# ==========================================================================
# Ek A.2.2 · §3.5.2 — saf fonksiyonlar
# ==========================================================================
def rxcost(gecmis: int, gecikme_s: float = 0.0) -> int:
    """Ek A.2.2 — babeld `neighbour_rxcost`: en yeni iki Hello'ya ağırlık
    veren geçmiş; son 12 Hello'nun hiçbiri yoksa ya da son Hello olayı
    180 s önceyse ∞, 40 s'den eskiyse ceza."""
    if (gecmis & ETX_SONSUZ_MASKE) == 0 or gecikme_s >= ETX_SONSUZ_S:
        return SONSUZ
    sreach = (((gecmis & 0x8000) >> 2) + ((gecmis & 0x4000) >> 1)
              + (gecmis & 0x3FFF))
    c = (0x8000 * 256) // (sreach + 1)
    if gecikme_s >= ETX_CEZA_S:
        ms = int(gecikme_s * 1000)
        c = (c * (ms - 20000) + 10000) // 20000
    return min(c, SONSUZ)


def maliyet(rx: int, tx: int) -> int:
    """Ek A.2.2: cost = 256 / (alpha · beta) = max(txcost, 256) · rxcost /
    256, babeld'in yuvarlamasıyla; biri ∞ ise ∞ (§3.4.3'ün MUST'ları)."""
    if rx >= SONSUZ or tx >= SONSUZ:
        return SONSUZ
    return min(SONSUZ, (max(tx, 256) * max(rx, 256) + 128) >> 8)


def metrik(c: int, m: int) -> int:
    """§3.5.2 toplamsal metrik M(c, m) = c + m; ∞'a kırpılır."""
    if c >= SONSUZ or m >= SONSUZ:
        return SONSUZ
    return min(SONSUZ, c + m)


# ==========================================================================
# Tablolar — §3.2
# ==========================================================================
@dataclass(slots=True)
class _Komsu:
    """§3.2.4 · Ek A.1."""
    gecmis: int = 0                     # 16 bit, en yeni en üst bitte
    beklenen: int = 0                   # ne
    hello_aralik_s: float = HELLO_ARALIGI_S
    hello_son: float = math.inf         # Hello zamanlayıcısının dolumu
    hello_t: float = -math.inf          # son Hello olayı (alınan ya da kaçan)
    txcost: int = SONSUZ
    ihu_son: float = math.inf           # IHU tutma süresinin dolumu


@dataclass(slots=True)
class _Rota:
    """§3.2.6 — bir önekin bir komşudan öğrenilmiş rotası."""
    router_id: int
    sira: int
    ilan_metrik: int                    # komşunun ilan ettiği
    bitis: float                        # süre zamanlayıcısı
    sure_s: float                       # ilan edilen aralıktan tutma süresi
    yumusak: float                      # Ek A.3 ms(R)
    yumusak_t: float
    son_m: int                          # ms'nin son güncellendiği metrik
    istek_bitis: float | None = None    # §3.8.2.3 isteği bu bitiş için yapıldı


@dataclass(slots=True)
class _Istek:
    """§3.2.7 · §3.8.1.2 — kendi ya da iletilmiş sıra isteği."""
    sira: int
    istekci: int | None                 # adına iletilen komşu (None: kendim)
    kalan: int                          # kalan yineleme
    son: float                          # yineleme zamanı
    bekleme_s: float
    bitis: float                        # listeden düşme
    # Karşılanınca acil güncelleme (babeld `unsatisfied_request`); §3.8.2.2
    # isteğinde yok (babeld onu tabloya yazmaz).
    acil_yanit: bool = True


@dataclass(slots=True)
class _Tampon:
    """§3.1 — bir hedefin (çoklu-yayın ya da komşu) giden tamponu."""
    nesil: int                          # boşaltma uyandırmasının etiketi
    ilan: dict = field(default_factory=dict)    # önek → None (sıralı küme)
    tlv: list = field(default_factory=list)
    acil: bool = False                  # acil boşaltma kuruldu
    normal: bool = False                # acil olmayan boşaltma kuruldu


class Babel:
    """The Babel Routing Protocol — RFC 8966."""

    ad = "babel"
    kosum_beaconi = False               # kendi Hello'su, 4 s

    __slots__ = ("kimlik", "_adres", "_sira", "_hello_sira", "_komsu",
                 "_kaynak", "_rota", "_secili", "_kurulu", "_istek",
                 "_yeniden", "_giden", "_tampon", "_tampon_nesil",
                 "_kayip_sebebi", "_basladi",
                 "_planli_s", "_plan_nesil", "_son_dokum_t", "_simdi",
                 "_secili_onceki", "_kopuk", "_bilinen",
                 "_kullanilir_onceki", "_sayac")

    def __init__(self, kimlik: int) -> None:
        self.kimlik = kimlik
        self._adres = adres(kimlik)
        self._sira = 0                          # §3.2.2 düğüm sırası
        self._hello_sira = 0                    # §3.2.3 çoklu-yayın Hello sırası
        self._komsu: dict[int, _Komsu] = {}
        # §3.2.5 kaynak tablosu: (önek, router-id) → [sıra, metrik, GC sonu]
        self._kaynak: dict[tuple[int, int], list] = {}
        # §3.2.6 rota tablosu: önek → komşu → rota
        self._rota: dict[int, dict[int, _Rota]] = {}
        self._secili: dict[int, int] = {}       # önek → seçili komşu
        self._kurulu: dict[int, tuple[int, int]] = {}  # önek → (komşu, rid)
        # §3.2.7 sıra istekleri: (önek, router-id) → istek
        self._istek: dict[tuple[int, int], _Istek] = {}
        # §3.7.2 yinelenen tetik: önek → [ilk gönderim, yapılan yineleme]
        self._yeniden: dict[int, list] = {}
        # Kanca sonunda paketlenecekler: (tür, veri, hedef, acil);
        # tür "ilan" (önek; seçimden SONRA bugünkü hâliyle kurulur) ya da
        # "tlv".
        self._giden: list[tuple] = []
        # §3.1 — hedef (None: çoklu-yayın) → giden tampon.
        self._tampon: dict[int | None, _Tampon] = {}
        self._tampon_nesil = 0
        # Bu kancada seçili rotası metrik ∞ yolundan başka bir yolla
        # kaybedilen önekler: "sure" · "kaynak" (babeld `route_lost`).
        self._kayip_sebebi: dict[int, str] = {}
        self._basladi = False
        self._planli_s = math.inf
        self._plan_nesil = 0
        self._son_dokum_t = -math.inf
        self._simdi = 0.0                       # işlenen kancanın saati
        # Önceki kanca sonundaki seçili rotalar: önek → (komşu, rid, sıra, m).
        self._secili_onceki: dict[int, tuple[int, int, int, int]] = {}
        # 🔒 ÖLÇÜM DURUMU — karara GİRMEZ (K-139 anlamı).
        self._kopuk: dict[int, set[int]] = {}
        self._bilinen: set[int] = set()
        self._kullanilir_onceki: frozenset[int] = frozenset()
        self._sayac: dict[str, int] = {
            "hello_gonderilen": 0, "ihu_gonderilen": 0,
            "dokum_gonderilen": 0, "tetik_acil": 0, "tetik_yeniden": 0,
            "tetik_normal": 0, "tetik_yinelenen": 0, "geri_cekme": 0,
            "guncelleme_alinan": 0, "uygulanamaz_alinan": 0,
            "uygulanamaz_yoksayilan": 0, "sira_istegi_uretilen": 0,
            "sira_istegi_bastirilan": 0,
            "sira_istegi_yinelenen": 0, "sira_istegi_iletilen": 0,
            "sira_istegi_yanitlanan": 0, "sira_artirildi": 0,
            "istek_karsilandi": 0, "rota_istegi_gonderilen": 0,
            "rota_istegi_kotulesme": 0, "rota_istegi_yanitlanan": 0,
            "joker_alinan": 0, "joker_dokum": 0, "rota_suresi_doldu": 0,
            "komsu_silindi": 0, "secim_degisti": 0, "gecersiz_paket": 0,
        }

    # ==================================================================
    # Komşu maliyeti — §3.4.3
    # ==================================================================
    def _rx(self, k: _Komsu, simdi: float) -> int:
        return rxcost(k.gecmis, simdi - k.hello_t)

    def _maliyet(self, n: int, simdi: float) -> int:
        k = self._komsu.get(n)
        if k is None:
            return SONSUZ
        tx = k.txcost if simdi < k.ihu_son else SONSUZ     # §3.4.2
        return maliyet(self._rx(k, simdi), tx)

    def _rota_metrigi(self, n: int, r: _Rota, simdi: float) -> int:
        return metrik(self._maliyet(n, simdi), r.ilan_metrik)

    # ==================================================================
    # §3.5.1 · §3.7.3 — uygulanabilirlik ve kaynak tablosu
    # ==================================================================
    def _uygulanabilir(self, onek: int, rid: int, sira: int, m: int) -> bool:
        if m >= SONSUZ:
            return True
        fd = self._kaynak.get((onek, rid))
        if fd is None:
            return True
        return sira_kucuk(fd[0], sira) or (sira == fd[0] and m < fd[1])

    def _fd_guncelle(self, onek: int, rid: int, sira: int, m: int,
                     simdi: float) -> None:
        """§3.7.3 — sonlu duyuru göndermeden ÖNCE."""
        fd = self._kaynak.get((onek, rid))
        if fd is None:
            self._kaynak[(onek, rid)] = [sira, m, simdi + KAYNAK_GC_S]
            return
        if sira_kucuk(fd[0], sira):
            fd[0], fd[1] = sira, m
        elif sira == fd[0] and fd[1] > m:
            fd[1] = m
        fd[2] = simdi + KAYNAK_GC_S

    # ==================================================================
    # Ek A.1 — Hello geçmişi · §3.4.2 IHU
    # ==================================================================
    def _hello_al(self, n: int, h: Hello, simdi: float) -> None:
        k = self._komsu.get(n)
        if k is not None:
            ileri = (h.sira - k.beklenen) & 0xFFFF
            geri = (k.beklenen - h.sira) & 0xFFFF
            if min(ileri, geri) > 16:
                self._komsu_sil(n)                  # yeniden başlamış komşu
                k = None
        if k is None:
            k = self._komsu[n] = _Komsu(beklenen=h.sira)
        elif sira_kucuk(h.sira, k.beklenen):        # "undo history"
            geri = (k.beklenen - h.sira) & 0xFFFF
            k.gecmis = (k.gecmis << geri) & _MASKE
        elif sira_kucuk(k.beklenen, h.sira):        # "fast-forward"
            k.gecmis >>= (h.sira - k.beklenen) & 0xFFFF
        k.gecmis = (k.gecmis >> 1) | _EN_YENI
        k.beklenen = sira_artir(h.sira)
        k.hello_t = simdi
        if h.aralik_cs:
            k.hello_aralik_s = h.aralik_cs / 100.0
            k.hello_son = simdi + HELLO_ZAMAN_ASIMI_KATSAYISI * k.hello_aralik_s

    def _komsu_sil(self, n: int) -> None:
        """§3.4: kullanılmayan komşu atılır; ondan öğrenilen rotalar gider."""
        self._komsu.pop(n, None)
        for onek in list(self._rota):
            rotalar = self._rota[onek]
            rotalar.pop(n, None)
            if not rotalar:
                del self._rota[onek]
        for onek in [o for o, s in self._secili.items() if s == n]:
            del self._secili[onek]
        for onek in [o for o, k in self._kurulu.items() if k[0] == n]:
            del self._kurulu[onek]
        self._sayac["komsu_silindi"] += 1

    def _ihu_al(self, n: int, i: Ihu, simdi: float) -> None:
        """§3.4.2: txcost = IHU'daki rxcost; tutma 3,5 × ilan edilen aralık."""
        k = self._komsu.get(n)
        if k is None or i.adres != self._adres:
            return
        k.txcost = i.rxcost
        k.ihu_son = simdi + IHU_TUTMA_KATSAYISI * i.aralik_cs / 100.0

    # ==================================================================
    # §3.5.3 — rota edinimi
    # ==================================================================
    def _guncelleme_al(self, n: int, g: Guncelleme, simdi: float) -> None:
        if n not in self._komsu or g.plen != 32 or g.onek == self._adres:
            return
        self._sayac["guncelleme_alinan"] += 1
        uygun = self._uygulanabilir(g.onek, g.router_id, g.sira, g.metrik)
        rotalar = self._rota.get(g.onek)
        r = rotalar.get(n) if rotalar is not None else None
        secili_idi = self._secili.get(g.onek) == n
        sure_s = ROTA_SURESI_KATSAYISI * g.aralik_cs / 100.0
        kaynak_degisti = False
        if r is None:
            if g.metrik >= SONSUZ:
                return                          # bilinmeyen rotanın geri çekmesi
            # Kayıt yokken uygulanamaz güncelleme MAY yok sayılır — babeld
            # yok saymaz, kayıt açılır (beyan tablosu).
            m = metrik(self._maliyet(n, simdi), g.metrik)
            ms = float(max(m, _YARI_SONSUZ)) if m < SONSUZ else float(SONSUZ)
            self._rota.setdefault(g.onek, {})[n] = _Rota(
                g.router_id, g.sira, g.metrik, simdi + sure_s, sure_s,
                yumusak=ms, yumusak_t=simdi, son_m=m)
        elif g.metrik >= SONSUZ:
            # Geri çekme router-id taşımaz: kaynağı kaydınki sayılır (babeld
            # `update_route`); süre tazelenmez (§3.5.3).
            r.ilan_metrik = SONSUZ
        else:
            kaynak_degisti = g.router_id != r.router_id
            if secili_idi and not uygun and not kaynak_degisti:
                # §3.5.3 MAY: seçili rotanın aynı router-id'li uygulanamaz
                # güncellemesi YOK SAYILIR. babeld kaydı günceller ama
                # seçimden çıkarmaz; RFC'de güncellenen uygulanamaz kayıt
                # hemen seçimden çıkar (MUST), babeld'in "seçili kalır"
                # amacına uyumlu dal yok saymadır. §3.8.2.2: istek SHOULD.
                self._sayac["uygulanamaz_alinan"] += 1
                self._sayac["uygulanamaz_yoksayilan"] += 1
                self._uygulanamaz_istek(n, g, True, simdi)
                return
            r.router_id, r.sira, r.ilan_metrik = g.router_id, g.sira, g.metrik
            r.bitis, r.sure_s = simdi + sure_s, sure_s
            r.istek_bitis = None
            if not uygun and secili_idi:
                # MUST: hemen seçimden çıkar (babeld: kaldırılır, kayıp).
                del self._secili[g.onek]
                self._kayip_sebebi[g.onek] = "kaynak"
        if not uygun:
            self._sayac["uygulanamaz_alinan"] += 1
            if not (secili_idi and kaynak_degisti):     # o dalda kayıp yolu
                self._uygulanamaz_istek(n, g, secili_idi, simdi)

    def _uygulanamaz_istek(self, n: int, g: Guncelleme, secili_idi: bool,
                           simdi: float) -> None:
        """§3.8.2.2 — uygulanamaz güncellemede ilan edene tek-yayın sıra
        isteği: seçili rotanınsa her zaman (SHOULD); seçili olmayanınsa
        seçili rota yoksa ya da seçilinin metriği yeni metrik + 512'den
        küçük değilse (babeld'in "tercih edilir" eşiği)."""
        if g.metrik >= SONSUZ:
            return
        if not secili_idi:
            s = self._secili.get(g.onek)
            if s is not None:
                seciliyi = self._rota_metrigi(s, self._rota[g.onek][s], simdi)
                yeni = metrik(self._maliyet(n, simdi), g.metrik)
                if seciliyi < yeni + TERCIH_FARKI:
                    return
        self._sira_istegi(g.onek, g.router_id, g.sira, n, simdi,
                          yinele=False)

    def _sira_istegi(self, onek: int, rid: int, yedek_sira: int | None,
                     hedef: int | None, simdi: float, yinele: bool) -> None:
        """İstenen sıra = kaynak tablosundaki + 1 (§3.8.2.1); tabloda yoksa
        bilinen sıra + 1. `hedef` None ise çoklu-yayın.

        🔒 §3.2.7: yerelde üretilen her istek bekleyen istekler tablosuna
        girer; aynı önek ve router-id için daha küçük olmayan sıralı istek
        beklerken yenisi üretilmez (yinelemeyi tablonun zamanlayıcısı
        yapar). `yinele`: açlık isteği (§3.8.2.1) — Ek B'ye göre yinelenir,
        `ISTEK_LISTE_S`de düşer; değilse (§3.8.2.2) yinelenmez, istek zaman
        aşımında düşer. Bekleyen açlık isteği yalnız başka bir açlık
        isteğini bastırır."""
        fd = self._kaynak.get((onek, rid))
        if fd is not None:
            sira = sira_artir(fd[0])
        elif yedek_sira is not None:
            sira = sira_artir(yedek_sira)
        else:
            sira = 0
        onceki = self._istek.get((onek, rid))
        if (onceki is not None and onceki.bitis > simdi
                and not sira_kucuk(onceki.sira, sira)
                and (not yinele or (onceki.istekci is None
                                    and onceki.kalan > 0))):
            self._sayac["sira_istegi_bastirilan"] += 1
            return
        if yinele:
            self._istek[(onek, rid)] = _Istek(
                sira=sira, istekci=None, kalan=ISTEK_TEKRAR,
                son=simdi + ISTEK_ZAMAN_ASIMI_S,
                bekleme_s=ISTEK_ZAMAN_ASIMI_S, bitis=simdi + ISTEK_LISTE_S)
        else:
            self._istek[(onek, rid)] = _Istek(
                sira=sira, istekci=None, kalan=0, son=math.inf,
                bekleme_s=ISTEK_ZAMAN_ASIMI_S,
                bitis=simdi + ISTEK_ZAMAN_ASIMI_S, acil_yanit=False)
        self._giden.append(("tlv", SiraIstegi(onek, 32, sira,
                                              SIRA_ISTEGI_HOP, rid),
                            hedef, False))
        self._sayac["sira_istegi_uretilen"] += 1

    # ==================================================================
    # §3.8.1 — gelen istekler
    # ==================================================================
    def _rota_istegi_al(self, n: int, r: RotaIstegi, simdi: float) -> None:
        """§3.8.1.1: seçili rota varsa güncelleme, yoksa geri çekme (MUST);
        çoklu-yayın, acil değil (babeld). Joker istekte o komşuya IHU ve hız
        sınırlı tam döküm (babeld)."""
        if r.joker:
            self._sayac["joker_alinan"] += 1
            k = self._komsu.get(n)
            if k is not None:
                self._giden.append(("tlv", Ihu(self._rx(k, simdi), _IHU_CS,
                                               adres(n)), None, False))
                self._sayac["ihu_gonderilen"] += 1
            if simdi - self._son_dokum_t >= max(HELLO_ARALIGI_S, 1.0):
                self._son_dokum_t = simdi
                for o in self._dokum_onekleri():
                    self._giden.append(("ilan", o, None, False))
                self._sayac["joker_dokum"] += 1
            return
        if r.plen != 32:
            return
        self._giden.append(("ilan", r.onek, None, False))
        self._sayac["rota_istegi_yanitlanan"] += 1

    def _sira_istegi_al(self, n: int, s: SiraIstegi, simdi: float) -> None:
        """§3.8.1.2. Yanıt acil çoklu-yayın (babeld); iletim acil tek-yayın
        (SHOULD)."""
        if s.plen != 32:
            return
        if s.onek == self._adres:
            if s.router_id == self._adres and sira_kucuk(self._sira, s.sira):
                self._sira = sira_artir(self._sira)     # en çok 1 (MUST)
                self._sayac["sira_artirildi"] += 1
            self._giden.append(("ilan", s.onek, None, True))
            self._sayac["sira_istegi_yanitlanan"] += 1
            return
        rotalar = self._rota.get(s.onek, {})
        secili = self._secili.get(s.onek)
        if secili is None:
            return                          # öneki duyurmuyor
        rs = rotalar[secili]
        if self._rota_metrigi(secili, rs, simdi) >= SONSUZ:
            return
        if rs.router_id != s.router_id or not sira_kucuk(rs.sira, s.sira):
            self._giden.append(("ilan", s.onek, None, True))    # MUST
            self._sayac["sira_istegi_yanitlanan"] += 1
            return
        if s.hop < 2:
            return
        onceki = self._istek.get((s.onek, s.router_id))
        if (onceki is not None and onceki.bitis > simdi
                and not sira_kucuk(onceki.sira, s.sira)):
            return                                  # yakında iletildi (SHOULD)
        uygun, diger = [], []
        for m, r in rotalar.items():
            if m == n or self._rota_metrigi(m, r, simdi) >= SONSUZ:
                continue
            if self._uygulanabilir(s.onek, r.router_id, r.sira, r.ilan_metrik):
                uygun.append(m)
            else:
                diger.append(m)
        # MUST uygulanabilir · SHOULD uygulanamaz; içinde seçili rotanın
        # komşusu, değilse en küçük düzgünleştirilmiş metrik (babeld).
        aday = uygun or diger
        if not aday:
            return
        hedef = secili if secili in aday else min(
            aday, key=lambda m: (rotalar[m].yumusak, m))
        self._istek[(s.onek, s.router_id)] = _Istek(
            sira=s.sira, istekci=n, kalan=0, son=math.inf,
            bekleme_s=ISTEK_ZAMAN_ASIMI_S, bitis=simdi + ISTEK_LISTE_S)
        self._giden.append(("tlv", SiraIstegi(s.onek, 32, s.sira, s.hop - 1,
                                              s.router_id), hedef, True))
        self._sayac["sira_istegi_iletilen"] += 1

    # ==================================================================
    # §3.6 · Ek A.3 — rota seçimi
    # ==================================================================
    def _sec(self, simdi: float) -> None:
        for onek in sorted(self._rota):
            rotalar = self._rota[onek]
            onceki = self._secili.get(onek)
            adaylar: dict[int, int] = {}
            for n, r in rotalar.items():
                m = self._rota_metrigi(n, r, simdi)
                self._yumusat(r, m, simdi)
                if m < SONSUZ and self._uygulanabilir(onek, r.router_id,
                                                      r.sira, r.ilan_metrik):
                    adaylar[n] = m
            yeni = onceki if onceki in adaylar else None
            if yeni is None:
                if adaylar:                         # Ek A.3: düzgünsüz en küçük
                    yeni = min(adaylar, key=lambda n: (adaylar[n], n))
            else:
                m_y, ms_y = adaylar[yeni], rotalar[yeni].yumusak
                daha_iyi = [n for n, m in adaylar.items()
                            if m < m_y and rotalar[n].yumusak < ms_y]
                if daha_iyi:
                    yeni = min(daha_iyi, key=lambda n: (adaylar[n], n))
            if yeni is None:
                self._secili.pop(onek, None)
            else:
                self._secili[onek] = yeni
            if yeni != onceki:
                self._sayac["secim_degisti"] += 1

    @staticmethod
    def _yumusat(r: _Rota, m: int, simdi: float) -> None:
        """Ek A.3 — babeld `route_smoothed_metric`: geçen süre boyunca o
        sürede geçerli olan metriğe doğru, yarı ömür 4 s; fark 4'ten küçükse
        ms = m; ∞ metrikte ms = ∞."""
        dt = simdi - r.yumusak_t
        if r.son_m >= SONSUZ:
            r.yumusak = float(SONSUZ)
        elif dt > 0.0:
            r.yumusak += (r.son_m - r.yumusak) * (1.0 - 2.0 ** (-dt
                                                                / YARI_OMUR_S))
        if m >= SONSUZ:
            r.yumusak = float(SONSUZ)
        elif abs(m - r.yumusak) < 4.0:
            r.yumusak = float(m)
        r.yumusak_t = simdi
        r.son_m = m

    # ==================================================================
    # §3.7.2 · §3.8.2.1 — tetikler ve kayıp (babeld)
    # ==================================================================
    def _secim_sonrasi(self, simdi: float) -> dict:
        """Seçili rotaları önceki kanca sonundakiyle karşılaştırır. Döner:
        önceki kanca sonundaki seçili rotalar."""
        onceki = self._secili_onceki
        for onek in sorted(set(onceki) | set(self._secili)):
            once = onceki.get(onek)
            n = self._secili.get(onek)
            if n is None:
                if once is not None:
                    self._kaybedildi(onek, once, simdi)
                continue
            r = self._rota[onek][n]
            m = self._rota_metrigi(n, r, simdi)
            if once is None:
                k = self._kurulu.get(onek)
                if k is None:
                    self._tetik(onek, "acil")           # `consider_route`
                else:
                    self._tetikle(onek, k[1], SONSUZ, r.router_id, r.sira, m)
            elif once[0] != n:
                eski = self._rota.get(onek, {}).get(once[0])
                m_eski = (self._rota_metrigi(once[0], eski, simdi)
                          if eski is not None else SONSUZ)
                self._tetikle(onek, once[1], m_eski, r.router_id, r.sira, m)
            else:
                self._tetikle(onek, once[1], once[3], r.router_id, r.sira, m)
            self._kurulu[onek] = (n, r.router_id)
        self._kayip_sebebi.clear()
        self._secili_onceki = {
            o: (n, self._rota[o][n].router_id, self._rota[o][n].sira,
                self._rota_metrigi(n, self._rota[o][n], simdi))
            for o, n in self._secili.items()}
        return onceki

    def _karsilaniyor(self, onek: int, rid: int, sira: int) -> bool:
        """babeld `unsatisfied_request`: bekleyen istek (rid, sira)'lı
        rotayla karşılanıyor mu."""
        for (o, r), i in self._istek.items():
            if (i.acil_yanit and o == onek
                    and (r != rid or not sira_kucuk(sira, i.sira))):
                return True
        return False

    def _tetikle(self, onek: int, rid_eski: int, m_eski: int, rid: int,
                 sira: int, m: int) -> None:
        """babeld `send_triggered_update`."""
        fark = abs(m - m_eski)
        if rid != rid_eski or (m_eski < SONSUZ and m >= SONSUZ):
            tur = "yeniden"
        elif m > m_eski and m_eski < KOTULESME_TABANI \
                and fark >= KOTULESME_FARKI:
            tur = "acil"
        elif self._karsilaniyor(onek, rid, sira):
            tur = "acil"
        elif m_eski >= SONSUZ:
            tur = "normal"                      # yeni rota
        elif m < m_eski and fark < IYILESME_YOKSAY:
            return
        elif fark < ONEMSIZ_FARK:
            return
        else:
            tur = "normal"
        self._tetik(onek, tur)
        if m_eski < SONSUZ and m >= m_eski + ROTA_ISTEGI_KOTULESME:
            self._giden.append(("tlv", RotaIstegi(onek, 32), None, False))
            self._sayac["rota_istegi_kotulesme"] += 1

    def _kaybedildi(self, onek: int, once: tuple, simdi: float) -> None:
        """Seçili rota kalmadı. Metrik ∞ yolunda (geri çekme, komşu kaybı)
        babeld `send_triggered_update`: yinelenen geri çekme ve rota isteği;
        süre dolumunda ve farklı router-id'li uygulanamaz güncellemede
        `route_lost`: yinelenen geri çekme. Açlık (§3.8.2.1): uygulanamaz
        rota varsa sıra isteği MUST; yoksa `route_lost` dalında eski metrik
        ≤ ∞/2 ise (MAY, babeld)."""
        sebep = self._kayip_sebebi.get(onek)
        self._sayac["geri_cekme"] += 1
        if sebep is None:
            self._tetikle(onek, once[1], once[3], once[1], once[2], SONSUZ)
        else:
            self._tetik(onek, "yeniden")
        uygulanamaz = any(
            self._rota_metrigi(m, r, simdi) < SONSUZ
            and not self._uygulanabilir(onek, r.router_id, r.sira,
                                        r.ilan_metrik)
            for m, r in self._rota.get(onek, {}).items())
        if uygulanamaz or (sebep is not None and once[3] <= _YARI_SONSUZ):
            self._sira_istegi(onek, once[1], once[2], None, simdi,
                              yinele=True)

    def _tetik(self, onek: int, tur: str) -> None:
        """Tetiklenen güncelleme: "acil" · "yeniden" (acil, 2 · 4 · 8 s
        sonra yinelenir) · "normal" (acil değil)."""
        self._giden.append(("ilan", onek, None, tur != "normal"))
        if tur == "yeniden":
            self._yeniden[onek] = [self._simdi, 0]
        self._sayac["tetik_" + tur] += 1

    # ==================================================================
    # Gönderim
    # ==================================================================
    def _ilan(self, onek: int, simdi: float) -> Guncelleme:
        """Bir önekin bugünkü duyurusu: kendi önekim, seçili rota ya da
        geri çekme. Sonlu olanda kaynak tablosu önce güncellenir (§3.7.3)
        ve karşılanan istekler listeden düşer (babeld `satisfy_request`)."""
        if onek == self._adres:
            self._fd_guncelle(onek, onek, self._sira, 0, simdi)
            return Guncelleme(onek, 32, _ARALIK_CS, self._sira, 0, onek)
        n = self._secili.get(onek)
        if n is None:
            return Guncelleme(onek, 32, _ARALIK_CS, 0, SONSUZ, 0)
        r = self._rota[onek][n]
        m = self._rota_metrigi(n, r, simdi)
        if m >= SONSUZ:
            return Guncelleme(onek, 32, _ARALIK_CS, 0, SONSUZ, 0)
        self._fd_guncelle(onek, r.router_id, r.sira, m, simdi)
        for anahtar in [a for a, i in self._istek.items()
                        if a[0] == onek and (a[1] != r.router_id
                                             or not sira_kucuk(r.sira,
                                                               i.sira))]:
            del self._istek[anahtar]
            self._sayac["istek_karsilandi"] += 1
        return Guncelleme(onek, 32, _ARALIK_CS, r.sira, m, r.router_id)

    def _dokum_onekleri(self) -> list[int]:
        """§3.7.1 — kendi önekim, seçili rotalar ve kurulu ∞ rotaların
        geri çekmeleri (babeld)."""
        return [self._adres] + sorted(set(self._secili) | set(self._kurulu))

    @staticmethod
    def _paket(tlvler, hedef: int | None, jitter_s: float) -> KontrolIstegi:
        return KontrolIstegi.kur(hedef, BABEL,
                                 {"babel": tuple(paket_kodla(tlvler))},
                                 jitter_s=jitter_s)

    def _paketle(self, tlvler: list, hedef: int | None,
                 jitter_s: float) -> list:
        """TLV dizisi `PAKET_UST_SINIRI_B`'yi aşmayan paketlere bölünür."""
        cikti, parca = [], []
        for t in tlvler:
            parca.append(t)
            if len(parca) > 1 and len(paket_kodla(parca)) > PAKET_UST_SINIRI_B:
                parca.pop()
                cikti.append(self._paket(parca, hedef, jitter_s))
                parca = [t]
        if parca:
            cikti.append(self._paket(parca, hedef, jitter_s))
        return cikti

    def _tampona_al(self) -> list:
        """§3.1 — kancanın giden TLV'leri hedef başına tampona girer. Yeni
        tamponda ya da ilk acil TLV'de boşaltma uyandırması kurulur: acil
        U(0, 0,2 s), öteki U(0, Hello/2) (babeld `schedule_update_flush` ·
        `schedule_flush`)."""
        uyandirma: list = []
        for tur, veri, hedef, acil in self._giden:
            t = self._tampon.get(hedef)
            if t is None:
                self._tampon_nesil += 1
                t = self._tampon[hedef] = _Tampon(self._tampon_nesil)
            if tur == "ilan":
                t.ilan[veri] = None
            else:
                t.tlv.append(veri)
            if acil and not t.acil:
                t.acil = True
                uyandirma.append(self._bosaltma(hedef, t, ACIL_ZAMAN_ASIMI_S))
            elif not acil and not (t.acil or t.normal):
                t.normal = True
                uyandirma.append(self._bosaltma(hedef, t, _J_NORMAL))
        self._giden.clear()
        return uyandirma

    @staticmethod
    def _bosaltma(hedef: int | None, t: _Tampon, j: float) -> Uyandirma:
        anahtar = "h" if hedef is None else str(hedef)
        return Uyandirma(1e-3, f"{_BOSALT}{anahtar}:{t.nesil}", jitter_s=j)

    def _bosalt(self, hedef: int | None, simdi: float,
                haric: frozenset = frozenset()) -> list:
        """Tamponun TLV'leri; duyurular gönderim anındaki hâliyle kurulur
        (babeld `flushupdates`). `haric`: aynı pakette zaten duyurulan
        önekler."""
        t = self._tampon.pop(hedef, None)
        if t is None:
            return []
        return ([self._ilan(o, simdi) for o in t.ilan if o not in haric]
                + t.tlv)

    def _hello_kur(self, simdi: float) -> list:
        """§3.4.1 · §3.4.2 · Ek B — çoklu-yayın Hello ve IHU'lar (babeld
        `send_hello`): sırası 3'e bölünen Hello'yla bütün komşulara, öteki
        Hello'larda kayıplı ya da txcost ≥ 384 olan komşulara."""
        self._hello_sira = sira_artir(self._hello_sira)
        tlvler: list = [Hello(self._hello_sira, _HELLO_CS)]
        tam = self._hello_sira % 3 == 0
        for n in sorted(self._komsu):
            k = self._komsu[n]
            tx = k.txcost if simdi < k.ihu_son else SONSUZ
            if (tam or tx >= IHU_TXCOST_ESIGI
                    or (k.gecmis & IHU_KAYIPLI_MASKE) != IHU_KAYIPLI_MASKE):
                tlvler.append(Ihu(self._rx(k, simdi), _IHU_CS, adres(n)))
                self._sayac["ihu_gonderilen"] += 1
        self._sayac["hello_gonderilen"] += 1
        return tlvler

    def _dokum_kur(self, simdi: float) -> list:
        """§3.7.1 — periyodik tam döküm; bekleyen çoklu-yayın tamponu da
        aynı pakete girer."""
        self._son_dokum_t = simdi
        self._sayac["dokum_gonderilen"] += 1
        onekler = self._dokum_onekleri()
        return self._paketle(
            [self._ilan(o, simdi) for o in onekler]
            + self._bosalt(None, simdi, frozenset(onekler)), None, 0.0)

    # ==================================================================
    # Zamanlayıcılar — en erken son tarih
    # ==================================================================
    @staticmethod
    def _istek_zamani(r: _Rota) -> float:
        """§3.8.2.3: tutma süresinin 7/8'i."""
        return r.bitis - r.sure_s * (1.0 - ROTA_ISTEGI_ORANI)

    def _son_tarih(self) -> float:
        en = math.inf
        for k in self._komsu.values():
            en = min(en, k.hello_son, k.ihu_son)
        for onek, rotalar in self._rota.items():
            s = self._secili.get(onek)
            for n, r in rotalar.items():
                en = min(en, r.bitis)
                if (s == n and r.ilan_metrik < SONSUZ
                        and r.istek_bitis != r.bitis):
                    en = min(en, self._istek_zamani(r))
        for i in self._istek.values():
            en = min(en, i.son, i.bitis)
        for t0, k in self._yeniden.values():
            en = min(en, t0 + TETIK_YENIDEN_S[k])
        for fd in self._kaynak.values():
            en = min(en, fd[2])
        return en

    def _zamanlari_isle(self, simdi: float) -> None:
        for n in sorted(self._komsu):
            k = self._komsu.get(n)
            while k is not None and k.hello_son <= simdi:  # Ek A.1
                k.gecmis >>= 1
                k.beklenen = sira_artir(k.beklenen)
                k.hello_t = k.hello_son
                if k.gecmis == 0:
                    self._komsu_sil(n)
                    k = None
                else:
                    k.hello_son += k.hello_aralik_s
        for k in self._komsu.values():
            if k.ihu_son <= simdi:
                k.txcost, k.ihu_son = SONSUZ, math.inf     # §3.4.2
        for onek in sorted(self._rota):
            rotalar = self._rota[onek]
            secili = self._secili.get(onek)
            for n in sorted(rotalar):
                r = rotalar[n]
                if r.bitis <= simdi:                       # §3.5.3
                    if r.ilan_metrik < SONSUZ:
                        r.ilan_metrik = SONSUZ
                        r.bitis = simdi + r.sure_s
                        if secili == n:
                            self._kayip_sebebi[onek] = "sure"
                        self._sayac["rota_suresi_doldu"] += 1
                    else:
                        del rotalar[n]
                        if secili == n:
                            del self._secili[onek]
                        if self._kurulu.get(onek, (None,))[0] == n:
                            del self._kurulu[onek]
                elif (secili == n and r.ilan_metrik < SONSUZ
                      and r.istek_bitis != r.bitis
                      and self._istek_zamani(r) <= simdi):
                    # §3.8.2.3: süresi dolmadan ilan edene tek-yayın istek.
                    r.istek_bitis = r.bitis
                    self._giden.append(("tlv", RotaIstegi(onek, 32), n,
                                        False))
                    self._sayac["rota_istegi_gonderilen"] += 1
            if not rotalar:
                del self._rota[onek]
                self._kurulu.pop(onek, None)
        for anahtar in sorted(self._istek):
            i = self._istek[anahtar]
            if i.bitis <= simdi:
                del self._istek[anahtar]
                continue
            if i.son > simdi:
                continue
            onek, rid = anahtar
            if i.istekci is None and i.kalan > 0 and onek not in self._secili:
                # §3.8.2.1 · Ek B: rota uygulanabilir olmadıysa yinele; her
                # yinelemede bekleme iki katı, en çok üç kez.
                i.kalan -= 1
                i.bekleme_s *= 2
                i.son = simdi + i.bekleme_s
                self._giden.append(("tlv", SiraIstegi(
                    onek, 32, i.sira, SIRA_ISTEGI_HOP, rid), None, False))
                self._sayac["sira_istegi_yinelenen"] += 1
            else:
                i.son = math.inf
        for onek in sorted(self._yeniden):
            t0, k = self._yeniden[onek]
            if t0 + TETIK_YENIDEN_S[k] <= simdi:
                # §3.7.2: yinelenen tetik önekin o anki duyurusunu taşır.
                self._giden.append(("ilan", onek, None, True))
                self._sayac["tetik_yinelenen"] += 1
                if k + 1 < len(TETIK_YENIDEN_S):
                    self._yeniden[onek][1] = k + 1
                else:
                    del self._yeniden[onek]
        for a in [a for a, fd in self._kaynak.items() if fd[2] <= simdi]:
            del self._kaynak[a]

    # ==================================================================
    # Kanca sonu: zaman → seçim → tetik → giden paketler → beyanlar
    # ==================================================================
    def _bitir(self, simdi: float, ek: tuple = ()) -> tuple:
        self._simdi = simdi
        self._zamanlari_isle(simdi)
        self._sec(simdi)
        onceki = self._secim_sonrasi(simdi)
        niyet: list = list(ek) + self._tampona_al()
        son = self._son_tarih()
        if son < math.inf and (son < self._planli_s - 1e-9
                               or self._planli_s <= simdi):
            self._planli_s = son
            self._plan_nesil += 1
            niyet.append(Uyandirma(max(son - simdi, 1e-3),
                                   f"{_ZAMAN}{self._plan_nesil}"))
        return tuple(niyet) + self._beyanlar(simdi, onceki)

    def _beyanlar(self, simdi: float, onceki: dict) -> tuple:
        kullanilir = frozenset(n for n in self._komsu
                               if self._maliyet(n, simdi) < SONSUZ)
        cikti: list = []
        for n in sorted(self._kullanilir_onceki - kullanilir):
            etkilenen = {o for o, v in onceki.items() if v[0] == n}
            if etkilenen:
                self._kopuk.setdefault(n, set()).update(etkilenen)
                cikti.append(Beyan("kopma", komsu=n))
        for n in [n for n, h in self._kopuk.items() if h & self._secili.keys()]:
            del self._kopuk[n]
            cikti.append(Beyan("rota_kuruldu", komsu=n))
        self._bilinen |= {dugum(o) for o in self._secili}
        self._kullanilir_onceki = kullanilir
        return tuple(cikti)

    # ==================================================================
    # KANCA · kontrol
    # ==================================================================
    def kontrol_alindi(self, gozlem: Gozlem, gonderen: int, bicim: str,
                       yuk, yayin: bool) -> tuple:
        simdi = float(gozlem.saat_s)
        try:
            tlvler = paket_coz(bytes(dict(yuk)["babel"]))
        except BicimHatasi:
            self._sayac["gecersiz_paket"] += 1
            return self._bitir(simdi)
        for t in tlvler:
            if isinstance(t, Hello):
                self._hello_al(gonderen, t, simdi)
            elif isinstance(t, Ihu):
                self._ihu_al(gonderen, t, simdi)
            elif isinstance(t, Guncelleme):
                self._guncelleme_al(gonderen, t, simdi)
            elif isinstance(t, RotaIstegi):
                self._rota_istegi_al(gonderen, t, simdi)
            elif isinstance(t, SiraIstegi):
                self._sira_istegi_al(gonderen, t, simdi)
            elif t[0] == "ack_istek":
                # §3.3: onay isteğine yanıt verilebilmeli (MUST), tek-yayın.
                self._giden.append(("tlv", ("ack", t[1]), gonderen, True))
        return self._bitir(simdi)

    def zamanlayicilar(self) -> dict:
        return {"bakim": 1.0}

    def zamanlayici_doldu(self, gozlem: Gozlem, etiket: str) -> tuple:
        simdi = float(gozlem.saat_s)
        ek: tuple = ()
        if not self._basladi:
            # Açılış paketi (babeld): Hello, kendi önekim, joker istek;
            # titreşimi Hello'nunki. Tam döküm zinciri RFC 5148 §5'in
            # dağılımıyla.
            self._basladi = True
            ek = (Uyandirma(1e-3, _ACILIS, jitter_s=_J_HELLO),
                  Uyandirma(GUNCELLEME_ARALIGI_S - _J_DOKUM, _DOKUM,
                            jitter_s=_J_DOKUM))
        return self._bitir(simdi, ek)

    def uyandi(self, gozlem: Gozlem, etiket: str) -> tuple:
        simdi = float(gozlem.saat_s)
        # Hello, açılış ve döküm: önce zamanlayıcılar, seçim ve tetikler
        # (`_bitir`), sonra paket — bu kancanın tetikleri de aynı pakete
        # girer.
        if etiket == _ACILIS:
            self._zamanlari_isle(simdi)
            tlvler = self._hello_kur(simdi)
            niyet = self._bitir(simdi, (Uyandirma(
                HELLO_ARALIGI_S - _J_HELLO, _HELLO, jitter_s=_J_HELLO),))
            tlvler += [self._ilan(self._adres, simdi), RotaIstegi(0, 0)]
            tlvler += self._bosalt(None, simdi, frozenset((self._adres,)))
            return (*self._paketle(tlvler, None, 0.0), *niyet)
        if etiket == _HELLO:
            self._zamanlari_isle(simdi)
            tlvler = self._hello_kur(simdi)
            niyet = self._bitir(simdi, (Uyandirma(
                HELLO_ARALIGI_S - _J_HELLO, _HELLO, jitter_s=_J_HELLO),))
            tlvler += self._bosalt(None, simdi)
            return (*self._paketle(tlvler, None, 0.0), *niyet)
        if etiket == _DOKUM:
            niyet = self._bitir(simdi, (Uyandirma(
                GUNCELLEME_ARALIGI_S - _J_DOKUM, _DOKUM,
                jitter_s=_J_DOKUM),))
            return (*self._dokum_kur(simdi), *niyet)
        if etiket.startswith(_BOSALT):
            anahtar, _, nesil = etiket[len(_BOSALT):].partition(":")
            hedef = None if anahtar == "h" else int(anahtar)
            niyet = self._bitir(simdi)
            t = self._tampon.get(hedef)
            if t is None or t.nesil != int(nesil):
                return niyet                    # tampon zaten boşaldı
            return (*self._paketle(self._bosalt(hedef, simdi), hedef, 0.0),
                    *niyet)
        if etiket.startswith(_ZAMAN):
            if int(etiket[len(_ZAMAN):]) == self._plan_nesil:
                self._planli_s = math.inf
        return self._bitir(simdi)

    # ==================================================================
    # KANCA · veri
    # ==================================================================
    def sonraki_atlama(self, gozlem: Gozlem) -> Karar:
        if gozlem.paket is None:
            return Karar()
        simdi = float(gozlem.saat_s)
        niyet = self._bitir(simdi) if simdi >= self._planli_s else ()
        beyan = tuple(x for x in niyet if isinstance(x, Beyan))
        niyet = tuple(x for x in niyet if not isinstance(x, Beyan))
        hedef = gozlem.paket.hedef
        n = self._secili.get(adres(hedef))
        if n is not None:
            return Karar(sonraki=n, beyan=beyan, niyetler=niyet)
        # Proaktif: tampon yok, rota yoksa paket düşer (beyan tablosu).
        if hedef in self._bilinen:
            beyan = beyan + (Beyan("rota_gecersiz", komsu=hedef),)
        return Karar(sonraki=None, beyan=beyan, niyetler=niyet)

    def iletim_basarisiz(self, gozlem: Gozlem, hedef: int | None,
                         tur: str) -> tuple:
        """Bağ katmanı bildirimi kullanılmaz (beyan tablosu)."""
        return ()

    def beacon_yuku(self, gozlem: Gozlem) -> dict:
        return {}

    def beacon_alindi(self, gozlem: Gozlem, komsu: int, yuk) -> None:
        return None

    # ==================================================================
    # KANCA · teşhis
    # ==================================================================
    def teshis(self, dugum_: int) -> dict:
        """🔴 Yalnız sonuç satırına; karara GİRMEZ (en çok 32 alan,
        `sim2/gozlem/teshis.py`)."""
        return {**self._sayac,
                "komsu": len(self._komsu),
                "rota_kaydi": sum(len(r) for r in self._rota.values()),
                "secili": len(self._secili),
                "istek": len(self._istek),
                "sira": self._sira}
