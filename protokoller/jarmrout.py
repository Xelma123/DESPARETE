"""
JarmRout — C. Pu, *"Jamming-Resilient Multipath Routing Protocol for Flying
Ad Hoc Networks"*, IEEE Access 6:68472–68486, 2018.

Makaleye HARFİYEN sadık gerçekleme (K-229 · K-231). Kuralların makaledeki
yeri J1–J13 (`arsiv/teshis/jarmrout_2026-10-11/tasarim.md`); biçimler,
sabitler ve makaleye göre her fark ile her DSR dolgusu `jarmrout_bicim.py`nin
beyan tablosunda.

🔒 KÂHİN ERİŞİMİ YOK
Yalnız `sim2/gozlem/`i içe aktarır. Bağ kalitesi kendi telsizinin çerçeve
başına RSSI'ından (`cerceve_duyuldu`), yük kendi kanal meşgul süresinden ve
kuyruğundan, konum kendi GPS/INS'inden; komşunun konumu RREQ'da ödenerek
gelir.

🔒 AKIŞ (makale §III.E · Şekil 4)
  · Kaynak: rota yoksa RREQ yayınlar (J1); RREP'lerdeki tam rotaları
    önbelleğe alır ve AYNI veri paketini iki yoldan gönderir (J8, §VI.B) —
    simülatörün kopya defteri (K-231) ve kaynak rotası (K-232).
  · Ara düğüm: RREQ'ya bağ kalitesini ve yükünü işler, kendini ve konumunu
    ekler, yeniden yayınlar (J3 · J4); önbellekten RREP vermez (J5); veriyi
    başlıktaki kaynak rotasıyla iletir (J13); iletemezse kaynağa RERR (J9).
  · Hedef: ilk RREQ'dan sonra `t_wait` boyunca düğüm-ayrık yolları kaydeder
    (J6), sonra çift önceliği en küçük iki yolu seçip iki RREP yollar (J7).
"""

from __future__ import annotations

import math
import struct
from collections import deque

from sim2.gozlem.karar import Beyan, Karar
from sim2.gozlem.kontrol import KontrolIstegi, Uyandirma
from sim2.gozlem.pencere import Gozlem
from protokoller.jarmrout_bicim import (
    AGIRLIK_BAG, AGIRLIK_UZAKLIK, AGIRLIK_YUK, BROADCAST_JITTER_S, KONUM_BIT,
    MAX_REQUEST_PERIOD_S, MAX_REQUEST_REXMT, N_RSSI, REQUEST_PERIOD_S, RERR,
    ROTA_ADRES_BAYT, ROUTE_CACHE_TIMEOUT_S, RREP, RREQ, T_WAIT_S,
    VERI_BASLIK_BAYT, YUK_DUZELTME, YUK_KANAL_AGIRLIGI, YUK_KANAL_SUZGECI,
    YUK_KUYRUK_SUZGECI)

__all__ = ["JarmRout", "bag_kalitesi", "yol_uzakligi", "cift_onceligi",
           "trafik_yuku"]

_KESIF, _TWAIT, _TAMPON = "kesif:", "twait:", "tampon"
# Gerçekleme ayrıntısı (protokol sabiti değil): rota kurulunca bekleyen
# paketleri yeniden sordurmak için kısa uyandırma (K-135; simülatörün alt
# sınırı bir slot). DSR'de karşılığı "Send Buffer hemen boşaltılır".
_TAMPON_YOKLAMA_S = 1e-3
_SIRA_MOD = 1 << 16                         # pkt_seq 16 bit (Şekil 2)
_ISTEK_TABLOSU_ID = 16                      # RFC 4728 §9 RequestTableIds
_KONUM_TAVAN = (1 << KONUM_BIT) - 1


# ======================================================================
# MAKALENİN DENKLEMLERİ — saf fonksiyonlar, makalenin örnekleriyle sınanır
# ======================================================================
def bag_kalitesi(ornekler) -> float:
    """Eş. 5 — RSSI örneklerinin varyansı: E(X²) − E(X)². Küçük = kararlı.
    Örnek yoksa 0 (makale tanımlamıyor; seçim, beyanlı)."""
    n = len(ornekler)
    if n == 0:
        return 0.0
    ort = sum(ornekler) / n
    return sum(x * x for x in ornekler) / n - ort * ort


def trafik_yuku(t_busy: float, q_buf: float) -> float:
    """Eş. 8 — TL = γ·T_busy + (1 − γ)·Q_buf + (T_busy + Q_buf)·ε;
    T_busy milisaniye, Q_buf paket (Tablo 2). γ = 0,5 · ε = 0,02 Tablo 2'den
    çözüldü."""
    g, e = YUK_KANAL_AGIRLIGI, YUK_DUZELTME
    return g * t_busy + (1.0 - g) * q_buf + (t_busy + q_buf) * e


def yol_uzakligi(p: tuple, q: tuple) -> float | None:
    """Eş. 9–12 — iki yolun ara düğümlerinin (x, y) konumlarından mekânsal
    uzaklık. Bir yolun ara düğümü yoksa tanımsız (`None`; size(p) = 0)."""
    if not p or not q:
        return None

    def dugum_yol(i, yol):                              # Eş. 9 · 10
        return min(math.hypot(i[0] - j[0], i[1] - j[1]) for j in yol)

    def yol_yol(a, b):                                  # Eş. 11
        return sum(dugum_yol(i, b) for i in a) / len(a)

    return (yol_yol(p, q) + yol_yol(q, p)) / 2.0        # Eş. 12


def cift_onceligi(lq_p: float, lq_q: float, tl_p: float, tl_q: float,
                  uzaklik: float | None) -> float:
    """Eş. 13 — P = α(Lq_p + Lq_q) + β(Tl_p + Tl_q) + γ·e^(1/Υ(p,q)).

    🔴 Üs 1/Υ'dur: Şekil 3'ün örneği (7,4638 · 6,8831 · 7,7095) ancak böyle
    tutar (PDF'in metni bozuk çıkıyor). Uzaklık büyüdükçe terim γ'ya iner,
    küçüldükçe büyür — uzak yollar yeğlenir. Υ tanımsızsa (ara düğümsüz yol)
    Υ = ∞ sayılır, terim γ (seçim, beyanlı); Υ = 0 sonsuz cezadır."""
    if uzaklik is None:
        uzam = 1.0
    elif uzaklik <= 0.0:
        uzam = math.inf
    else:
        uzam = math.exp(1.0 / uzaklik)
    return (AGIRLIK_BAG * (lq_p + lq_q) + AGIRLIK_YUK * (tl_p + tl_q)
            + AGIRLIK_UZAKLIK * uzam)


def _f32(x: float) -> float:
    """32 bitlik alana yazılan değer (Şekil 2: L_qt · T_ld 4 bayt)."""
    return struct.unpack("f", struct.pack("f", float(x)))[0]


class JarmRout:
    """JarmRout — Pu 2018. Kaynak yönlendirmeli, iki düğüm-ayrık yollu."""

    ad = "jarmrout"
    kosum_beaconi = False               # HELLO yok (DSR gibi)
    kanal_dolulugu_ister = True         # Eş. 6'nın kanal payı (J11)
    veri_baslik_bayt = VERI_BASLIK_BAYT
    rota_adres_bayt = ROTA_ADRES_BAYT

    __slots__ = ("kimlik", "_rssi", "_t_busy", "_q_buf", "_son_t",
                 "_son_mesgul", "_sira", "_istek", "_hedef_kayit",
                 "_rotalar", "_kesif", "_son_iletim", "_kopuk", "_beyan",
                 "_sayac")

    def __init__(self, kimlik: int) -> None:
        for ad, deger in (("T_WAIT_S", T_WAIT_S),
                          ("YUK_KANAL_SUZGECI", YUK_KANAL_SUZGECI),
                          ("YUK_KUYRUK_SUZGECI", YUK_KUYRUK_SUZGECI),
                          ("YUK_KANAL_AGIRLIGI", YUK_KANAL_AGIRLIGI),
                          ("YUK_DUZELTME", YUK_DUZELTME)):
            if deger is None:
                raise RuntimeError(
                    f"JarmRout: {ad} sabitlenmedi (`jarmrout_bicim.py`)")
        self.kimlik = kimlik
        # Komşu → son N_RSSI RSSI örneği (J10, Tablo 1).
        self._rssi: dict[int, deque] = {}
        # Eş. 6 · 7 süzgeçleri ve son ölçüm anı.
        self._t_busy = 0.0
        self._q_buf = 0.0
        self._son_t: float | None = None
        self._son_mesgul: float | None = None
        self._sira = 0
        # RFC 4728 §4.3 Route Request Table: başlatıcı → (pkt_seq, C_hop).
        self._istek: dict[int, deque] = {}
        # Hedef: (S, pkt_seq) → kayıtlı yollar; seçimden sonra `None`.
        self._hedef_kayit: dict[tuple[int, int], list | None] = {}
        # Kaynak: hedef → [(ara düğümler, son geçerlilik)] (en çok iki).
        self._rotalar: dict[int, list[tuple[tuple[int, ...], float]]] = {}
        # Kaynak: hedef → [deneme, periyot] (RFC 4728 §8.2 · §4.3).
        self._kesif: dict[int, list] = {}
        # Sonraki atlama → son gönderilen paketin (S, D, rota) — RERR'in
        # kime ve hangi yoldan döneceği (J9).
        self._son_iletim: dict[int, tuple[int, int, tuple[int, ...]]] = {}
        # 🔒 ÖLÇÜM DURUMU — karara GİRMEZ (beyan kanalı, K-139).
        self._kopuk: dict[int, set[int]] = {}
        self._beyan: list = []
        self._sayac: dict[str, int] = {
            "rreq_uretilen": 0, "rreq_iletilen": 0, "rreq_atilan": 0,
            "rrep_uretilen": 0, "rrep_iletilen": 0, "rerr_uretilen": 0,
            "rerr_iletilen": 0, "tek_yol": 0, "iki_yol": 0,
            "kesif_basarisiz": 0, "rotasiz_paket": 0, "yol_silinen": 0,
        }

    # ==================================================================
    # GÖZLEM — RSSI ve yük (J10 · J11)
    # ==================================================================
    def cerceve_duyuldu(self, gozlem: Gozlem, gonderen: int, tur: str,
                        hedef, rssi_dbm: int, paket) -> None:
        """Çözülen her çerçevenin RSSI'ı göndereninin örneklerine (J10)."""
        d = self._rssi.get(gonderen)
        if d is None:
            d = self._rssi[gonderen] = deque(maxlen=N_RSSI)
        d.append(float(rssi_dbm))

    def _yuk_guncelle(self, gozlem: Gozlem) -> None:
        """Eş. 6 · 7 — ortamın meşgul süresi ve kuyruk uzunluğu süzgeçleri.

        🔒 Yalnız düğümün KENDİ ortama erişiminde güncellenir (makale: "the
        measurement from the most recent medium access"): kuyruk başındaki
        veri iletim kararı ve ürettiği ya da ilettiği her kontrol çerçevesi.
        Alım erişim değildir (K-234: RREQ selinde birkaç ms arayla gelen
        kopyalar ölçümü sıfıra çekiyordu).

        Makalenin ölçümü erişimdeki NAV, birimi milisaniye (Tablo 2:
        T_busy ≈ 7 ms). Simülatörde RTS/CTS yok; karşılığı önceki erişimden
        bu yana CCA'nın meşgul kaldığı süre, ms (beyanlı sapma)."""
        t = float(gozlem.saat_s)
        m = gozlem.mesgul_sure_s
        if self._son_mesgul is not None and m is not None:
            nav_ms = max(0.0, m - self._son_mesgul) * 1e3
            a = YUK_KANAL_SUZGECI
            self._t_busy = a * self._t_busy + (1.0 - a) * nav_ms
        b = YUK_KUYRUK_SUZGECI
        self._q_buf = b * self._q_buf + (1.0 - b) * gozlem.kuyruk_uzunlugu
        self._son_t, self._son_mesgul = t, m

    def _erisimse_guncelle(self, gozlem: Gozlem, niyet: tuple) -> tuple:
        """Niyet bir kontrol çerçevesi gönderiyorsa bu bir erişimdir."""
        if any(isinstance(n, KontrolIstegi) for n in niyet):
            self._yuk_guncelle(gozlem)
        return niyet

    # ==================================================================
    # VERİ — J1 · J8 · J13
    # ==================================================================
    def sonraki_atlama(self, gozlem: Gozlem) -> Karar:
        p = gozlem.paket
        if p is None:
            return Karar()
        simdi = float(gozlem.saat_s)
        if p.kaynak != self.kimlik:
            # J13 — başlıktaki kaynak rotası.
            if self.kimlik not in p.rota:
                self._sayac["rotasiz_paket"] += 1
                return Karar()
            i = p.rota.index(self.kimlik)
            j = p.rota[i + 1] if i + 1 < len(p.rota) else p.hedef
            self._son_iletim[j] = (p.kaynak, p.hedef, p.rota)
            self._yuk_guncelle(gozlem)                  # veri erişimi
            return Karar(sonraki=j)
        rotalar = self._gecerli_rotalar(p.hedef, simdi)
        if not rotalar:
            # J1 — rota yok: tampona, keşif başlar (yoksa).
            return Karar(beklet=True, niyetler=self._erisimse_guncelle(
                gozlem, self._kesif_baslat(p.hedef, simdi)))
        self._yuk_guncelle(gozlem)                      # veri erişimi
        x = rotalar[0]
        j = x[0] if x else p.hedef
        self._son_iletim[j] = (p.kaynak, p.hedef, x)
        if len(rotalar) >= 2:
            y = rotalar[1]
            k = y[0] if y else p.hedef
            if k != j:
                # J8 · §VI.B — AYNI paket ikinci yoldan da (kopya, K-231).
                self._son_iletim[k] = (p.kaynak, p.hedef, y)
                return Karar(sonraki=j, rota=x, kopyalar=(k,),
                             kopya_rotalari=(y,))
        return Karar(sonraki=j, rota=x)

    def _gecerli_rotalar(self, hedef: int, simdi: float) -> list:
        lst = [r for r, son in self._rotalar.get(hedef, ()) if son > simdi]
        if not lst:
            self._rotalar.pop(hedef, None)
        return lst

    # ==================================================================
    # KEŞİF — J1 · J2 (RFC 4728 §8.2 · §9 yeniden deneme)
    # ==================================================================
    def _kesif_baslat(self, hedef: int, simdi: float) -> tuple:
        if hedef in self._kesif:
            return ()
        self._kesif[hedef] = [0, REQUEST_PERIOD_S]
        return self._rreq_gonder(hedef)

    def _rreq_gonder(self, hedef: int) -> tuple:
        k = self._kesif[hedef]
        k[0] += 1
        self._sira = (self._sira + 1) % _SIRA_MOD
        self._istek_kaydet(self.kimlik, self._sira, 0)
        self._sayac["rreq_uretilen"] += 1
        yuk = {"kaynak": self.kimlik, "hedef": hedef, "pkt_seq": self._sira,
               "c_hop": 0, "l_qt": 0.0, "t_ld": 0.0,
               "h_route": (), "x": (), "y": ()}
        return (KontrolIstegi.kur(None, RREQ, yuk),
                Uyandirma(k[1], _KESIF + str(hedef)))

    def _istek_bul(self, kaynak: int, sira: int) -> int | None:
        for s, c in self._istek.get(kaynak, ()):
            if s == sira:
                return c
        return None

    def _istek_kaydet(self, kaynak: int, sira: int, c_hop: int) -> None:
        d = self._istek.get(kaynak)
        if d is None:
            d = self._istek[kaynak] = deque(maxlen=_ISTEK_TABLOSU_ID)
        d.append((sira, c_hop))

    # ==================================================================
    # ZAMANLAYICILAR
    # ==================================================================
    def zamanlayicilar(self) -> dict:
        return {}

    def zamanlayici_doldu(self, gozlem: Gozlem, etiket: str) -> tuple:
        return ()

    def uyandi(self, gozlem: Gozlem, etiket: str) -> tuple:
        simdi = float(gozlem.saat_s)
        if etiket.startswith(_KESIF):
            hedef = int(etiket[len(_KESIF):])
            k = self._kesif.get(hedef)
            if k is None:
                return ()
            if self._gecerli_rotalar(hedef, simdi):
                del self._kesif[hedef]
                return ()
            if k[0] > MAX_REQUEST_REXMT:            # ilk + 16 yeniden
                del self._kesif[hedef]
                self._sayac["kesif_basarisiz"] += 1
                return ()
            k[1] = min(2.0 * k[1], MAX_REQUEST_PERIOD_S)
            return self._erisimse_guncelle(gozlem, self._rreq_gonder(hedef))
        if etiket.startswith(_TWAIT):
            kaynak, sira = (int(x) for x in etiket[len(_TWAIT):].split(":"))
            return self._erisimse_guncelle(gozlem,
                                           self._yol_sec(kaynak, sira))
        return ()                                    # _TAMPON

    # ==================================================================
    # KONTROL — J3–J9
    # ==================================================================
    def kontrol_alindi(self, gozlem: Gozlem, gonderen: int, bicim: str,
                       yuk, yayin: bool) -> tuple:
        simdi = float(gozlem.saat_s)
        y = dict(yuk)
        if bicim == "RREQ":
            # TL, süzgeçlerin bugünkü hâlinden (makale: "its current traffic
            # load"); yeniden yayın yeni erişimdir, ölçümü ondan sonra girer.
            niyet = self._rreq_isle(gozlem, gonderen, y)
        elif bicim == "RREP":
            niyet = self._rrep_isle(y, simdi)
        else:
            niyet = self._rerr_isle(y)
        self._erisimse_guncelle(gozlem, niyet)
        beyan, self._beyan = tuple(self._beyan), []
        return niyet + beyan

    def _rreq_isle(self, gozlem: Gozlem, gonderen: int, y: dict) -> tuple:
        kaynak, hedef, sira = y["kaynak"], y["hedef"], y["pkt_seq"]
        if kaynak == self.kimlik or self.kimlik in y["h_route"]:
            # Kendi isteği · rota kaydında kendisi var (RFC 4728 §8.2.2).
            self._sayac["rreq_atilan"] += 1
            return ()
        if hedef == self.kimlik:
            return self._hedefte_kaydet(y, kaynak, sira)            # J6
        c_onceki = self._istek_bul(kaynak, sira)
        if c_onceki is None:
            self._istek_kaydet(kaynak, sira, y["c_hop"])            # J3
        elif y["c_hop"] > c_onceki:
            self._sayac["rreq_atilan"] += 1                         # J4
            return ()
        # C_hop 8 bit (Şekil 2) · RFC 4728 §9 DiscoveryHopLimit 255.
        if y["c_hop"] >= 255:
            self._sayac["rreq_atilan"] += 1
            return ()
        lq = bag_kalitesi(self._rssi.get(gonderen, ()))
        tl = trafik_yuku(self._t_busy, self._q_buf)
        if lq > y["l_qt"]:
            y["l_qt"] = _f32(lq)
        if tl > y["t_ld"]:
            y["t_ld"] = _f32(tl)
        konum = gozlem.kendi_konum or (0.0, 0.0, 0.0)
        y["h_route"] = tuple(y["h_route"]) + (self.kimlik,)
        y["x"] = tuple(y["x"]) + (self._koordinat(konum[0]),)
        y["y"] = tuple(y["y"]) + (self._koordinat(konum[1]),)
        y["c_hop"] = y["c_hop"] + 1
        self._sayac["rreq_iletilen"] += 1
        return (KontrolIstegi.kur(None, RREQ, y,
                                  jitter_s=BROADCAST_JITTER_S),)

    @staticmethod
    def _koordinat(deger: float) -> int:
        return min(_KONUM_TAVAN, max(0, int(round(deger))))

    def _hedefte_kaydet(self, y: dict, kaynak: int, sira: int) -> tuple:
        anahtar = (kaynak, sira)
        yol = {"rota": tuple(y["h_route"]),
               "konum": tuple(zip(y["x"], y["y"])),
               "lq": y["l_qt"], "tl": y["t_ld"]}
        if anahtar not in self._hedef_kayit:
            self._hedef_kayit[anahtar] = [yol]
            return (Uyandirma(T_WAIT_S, f"{_TWAIT}{kaynak}:{sira}"),)
        kayit = self._hedef_kayit[anahtar]
        if kayit is None:                               # seçim yapıldı
            return ()
        ara = set(yol["rota"])
        if all(not (ara & set(k["rota"])) for k in kayit):
            kayit.append(yol)
        return ()

    def _yol_sec(self, kaynak: int, sira: int) -> tuple:
        """J7 — `t_wait` doldu: çift önceliği en küçük iki yol (Eş. 13)."""
        kayit = self._hedef_kayit.get((kaynak, sira))
        self._hedef_kayit[(kaynak, sira)] = None
        if not kayit:
            return ()
        if len(kayit) == 1:
            secilen = kayit
            self._sayac["tek_yol"] += 1
        else:
            enkucuk, secilen = math.inf, kayit[:2]
            for a in range(len(kayit)):
                for b in range(a + 1, len(kayit)):
                    p, q = kayit[a], kayit[b]
                    oncelik = cift_onceligi(
                        p["lq"], q["lq"], p["tl"], q["tl"],
                        yol_uzakligi(p["konum"], q["konum"]))
                    if oncelik < enkucuk:
                        enkucuk, secilen = oncelik, [p, q]
            self._sayac["iki_yol"] += 1
        niyet = []
        for yol in secilen:
            rota = yol["rota"]
            donus = tuple(reversed(rota))
            ilk = donus[0] if donus else kaynak
            self._sayac["rrep_uretilen"] += 1
            niyet.append(KontrolIstegi.kur(ilk, RREP, {
                "dsr_baslik": 0, "rrep_secenek": 0, "kaynak_rota_secenek": 0,
                "ip_hedef": kaynak, "yol": rota + (self.kimlik,),
                "donus": donus}))
        return tuple(niyet)

    def _rrep_isle(self, y: dict, simdi: float) -> tuple:
        kaynak = y["ip_hedef"]
        if kaynak != self.kimlik:
            sonraki = self._donus_sonraki(y["donus"], kaynak)
            if sonraki is None:
                return ()
            self._sayac["rrep_iletilen"] += 1
            return (KontrolIstegi.kur(sonraki, RREP, y),)
        hedef = y["yol"][-1]
        rota = tuple(y["yol"][:-1])
        lst = [(r, son) for r, son in self._rotalar.get(hedef, ())
               if son > simdi and r != rota]
        lst.append((rota, simdi + ROUTE_CACHE_TIMEOUT_S))
        self._rotalar[hedef] = lst[-2:]
        self._kesif.pop(hedef, None)
        for komsu, hedefler in list(self._kopuk.items()):
            if hedef in hedefler:
                hedefler.discard(hedef)
                self._beyan.append(Beyan("rota_kuruldu", komsu=komsu))
                if not hedefler:
                    del self._kopuk[komsu]
        return (Uyandirma(_TAMPON_YOKLAMA_S, _TAMPON),)

    def _rerr_isle(self, y: dict) -> tuple:
        kaynak = y["hata_hedefi"]
        if kaynak != self.kimlik:
            sonraki = self._donus_sonraki(y["donus"], kaynak)
            if sonraki is None:
                return ()
            self._sayac["rerr_iletilen"] += 1
            return (KontrolIstegi.kur(sonraki, RERR, y),)
        self._bagi_sil(y["hata_kaynagi"], y["ulasilamaz"])
        return ()

    def _donus_sonraki(self, donus: tuple, kaynak: int) -> int | None:
        if self.kimlik not in donus:
            return None
        i = donus.index(self.kimlik)
        return donus[i + 1] if i + 1 < len(donus) else kaynak

    def _bagi_sil(self, u: int, v: int) -> None:
        """J9 — kaynak, kopan bağı (u → v) içeren her yolu siler."""
        for hedef, lst in list(self._rotalar.items()):
            kalan = []
            for rota, son in lst:
                tam = (self.kimlik,) + rota + (hedef,)
                if any(tam[i] == u and tam[i + 1] == v
                       for i in range(len(tam) - 1)):
                    self._sayac["yol_silinen"] += 1
                    continue
                kalan.append((rota, son))
            if kalan:
                self._rotalar[hedef] = kalan
            else:
                del self._rotalar[hedef]

    # ==================================================================
    # BAĞ KOPMASI — J9
    # ==================================================================
    def iletim_basarisiz(self, gozlem: Gozlem, hedef: int | None,
                         tur: str) -> tuple:
        if tur != "veri" or hedef is None:
            return ()
        bilgi = self._son_iletim.get(hedef)
        if bilgi is None:
            return ()
        kaynak, son_hedef, rota = bilgi
        self._kopuk.setdefault(hedef, set()).add(son_hedef)
        beyan = (Beyan("kopma", komsu=hedef),)
        if kaynak == self.kimlik:
            self._bagi_sil(self.kimlik, hedef)
            return beyan
        tam = (kaynak,) + rota + (son_hedef,)
        if self.kimlik not in tam:
            return beyan
        k = tam.index(self.kimlik)
        donus = tuple(reversed(tam[1:k]))
        ilk = donus[0] if donus else kaynak
        self._sayac["rerr_uretilen"] += 1
        self._yuk_guncelle(gozlem)                      # RERR erişimi
        return beyan + (KontrolIstegi.kur(ilk, RERR, {
            "dsr_baslik": 0, "rerr_secenek": 0, "hata_kaynagi": self.kimlik,
            "hata_hedefi": kaynak, "ulasilamaz": hedef,
            "kaynak_rota_secenek": 0, "donus": donus}),)

    # ==================================================================
    # BEACON — yok (koşum beacon'ı kapalı, HELLO yok)
    # ==================================================================
    def beacon_yuku(self, gozlem: Gozlem) -> dict:
        return {}

    def beacon_alindi(self, gozlem: Gozlem, komsu: int, yuk) -> None:
        return None

    # ==================================================================
    # TEŞHİS
    # ==================================================================
    def teshis(self, dugum: int) -> dict:
        """🔴 Yalnız sonuç satırına; karara GİRMEZ."""
        return {**self._sayac,
                "rota_hedefi": len(self._rotalar),
                "suren_kesif": len(self._kesif)}
