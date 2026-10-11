"""
OLSRv2 — RFC 7181, komşuluk RFC 6130 (NHDP), bağ metriği RFC 7779 (DAT).

Kaynaklara sadık gerçekleme (K-229). Biçimler, sabitler ve RFC'nin seçeneğe
bıraktığı her yerin kararı `olsrv2_bicim.py`nin beyan tablosunda; tel biçimi
`olsrv2_rfc5444.py`de; tasarım notu `arsiv/teshis/olsrv2_2026-10-11/
tasarim.md`.

🔒 KÂHİN ERİŞİMİ YOK
Yalnız `sim2/gozlem/`i içe aktarır. Bildiği her şey aldığı bir RFC 5444
paketinden ya da kendi saatinden gelir. Bağ metriği (DAT) komşunun paket
sıra numaralarından ve HELLO aralığından KENDİ ölçülür.

🔒 TEK ARAYÜZ, TEK ADRES
Her yönlendiricinin tek telsizi ve tek adresi var; kaynak adresi arayüz
adresine eşit (RFC 7181 §7). Bu yüzden bağ ve komşu demetleri komşu başına
birdir, komşu metriği bağ metriğine eşittir; Routable Address Topology Set
Router Topology Set'le aynı düğümleri taşıdığı için ayrıca tutulmaz (rota
hesabında o kenarlar §19.1 gereği zaten kullanılmaz).

🔒 ÖLÇÜM BEYANLARI — AODV ve OLSR ile AYNI anlam (`04` K-139)
    kopma(K)         simetrik komşu K kaybedildi VE en az bir hedefin sonraki
                     atlamasıydı
    rota_kuruldu(K)  K'nin kaybının etkilediği bir hedefe yeniden rota var
    rota_gecersiz    daha önce rotası olan bir hedefe artık rota yok
"""

from __future__ import annotations

import heapq
from collections import deque
from dataclasses import dataclass, field

from sim2.gozlem.karar import Beyan, Karar
from sim2.gozlem.kontrol import KontrolIstegi, Uyandirma
from sim2.gozlem.pencere import Gozlem
from protokoller.olsrv2_bicim import (
    A_HOLD_TIME_S, ADRES_TABANI, ATLV_LINK_METRIC, ATLV_LINK_STATUS,
    ATLV_LOCAL_IF, ATLV_MPR, ATLV_NBR_ADDR_TYPE, ATLV_OTHER_NEIGHB,
    CONT_COMPLETE, DAT_HELLO_TIMEOUT_FACTOR, DAT_MAXIMUM_LOSS,
    DAT_MEMORY_LENGTH, DAT_MINIMUM_BITRATE, DAT_REFRESH_INTERVAL_S,
    DAT_RX_BITRATE_BPS, DAT_SEQNO_RESTART_DETECTION, F_HOLD_TIME_S,
    F_MAXJITTER_S, H_HOLD_TIME_S, HEARD, HELLO, HELLO_INTERVAL_S,
    HP_MAXJITTER_S, L_HOLD_TIME_S, LOST, MAXIMUM_METRIC, METRIK_GELEN_BAG,
    METRIK_GELEN_KOMSU, METRIK_GIDEN_BAG, METRIK_GIDEN_KOMSU, MPR_FLOODING,
    MPR_ROUTING, MSG_HELLO, MSG_TC, MTLV_CONT_SEQ_NUM, MTLV_INTERVAL_TIME,
    MTLV_MPR_WILLING, MTLV_VALIDITY_TIME, N_HOLD_TIME_S, ORIGINATOR,
    P_HOLD_TIME_S, ROUTABLE_ORIG, RX_HOLD_TIME_S, SYMMETRIC, T_HOLD_TIME_S,
    TC, TC_HOP_LIMIT, TC_INTERVAL_S, THIS_IF, TP_MAXJITTER_S, WILL_ALWAYS,
    WILL_FLOODING, WILL_NEVER, WILL_ROUTING)
from protokoller.olsrv2_rfc5444 import (
    BicimHatasi, iletim_icin, mesaj_kodla, metrik_coz, metrik_kodla,
    paket_coz, paket_kodla, zaman_coz, zaman_kodla)

__all__ = ["OLSRv2", "mpr_sec"]

_SURESI_DOLMUS = float("-inf")             # RFC 6130 §12.2 "EXPIRED"
_ALAN_16 = 0xFFFF
_KALIP_HELLO = (bytes([zaman_kodla(H_HOLD_TIME_S)]),
                bytes([zaman_kodla(HELLO_INTERVAL_S)]))
_KALIP_TC = (bytes([zaman_kodla(T_HOLD_TIME_S)]),
             bytes([zaman_kodla(TC_INTERVAL_S)]))
_ISTEK = bytes([(WILL_FLOODING << 4) | WILL_ROUTING])   # §13.3.1
_HELLO, _TC, _ILET = "hello", "tc", "ilet:"   # Uyandırma etiketleri
# Simülatörün uyandırma alt sınırı bir MAC slotu (K-135; 802.11b DSSS
# aSlotTime 20 µs). İletme titreşimi U(0, F_MAXJITTER)'ın önüne 20 µs ekler.
_EN_KISA_S = 20e-6


def _adres(k: int) -> int:
    return ADRES_TABANI + k + 1


def _dugum(a: int) -> int:
    return a - ADRES_TABANI - 1


def _sira_buyuk(s1: int, s2: int) -> bool:
    """RFC 7181 §21 — 16 bitlik sarmalı karşılaştırma."""
    return ((s1 > s2 and s1 - s2 < 32768)
            or (s2 > s1 and s2 - s1 > 32768))


def _metrik_degeri(bayraklar: int, metrik: int) -> bytes:
    return (bayraklar | metrik_kodla(metrik)).to_bytes(2, "big")


def _metrik_oku(degerler: list[bytes], bit: int) -> int | None:
    for d in degerler:
        v = int.from_bytes(d[:2].ljust(2, b"\0"), "big")
        if v & bit:
            return metrik_coz(v & 0x0FFF)
    return None


# ======================================================================
# §18 · Ek B — MPR SEÇİMİ (saf fonksiyon)
# ======================================================================
def mpr_sec(n1: dict, n2_d1: dict, d2: dict) -> frozenset:
    """RFC 7181 Ek B. `n1`: x → (W(x), d1(x)) · `n2_d1`: y → d1(y) ya da
    None · `d2`: (x, y) → d2(x, y). Döner: MPR kümesi M (§18.3).

    Seçim sırası W → R → D → küçük kimlik; adım 4 (fazlayı atma) İSTEĞE
    BAĞLI, uygulanmaz (beyan tablosu)."""
    def d(x, y):
        m = d2.get((x, y))
        return None if m is None else n1[x][1] + m

    ulasan: dict = {}                       # y → N1(y)
    for (x, y) in d2:
        if x in n1 and y in n2_d1:
            ulasan.setdefault(y, []).append(x)
    # N: d1(y) tanımsız ya da bir x üzerinden daha kısa.
    n = []
    en_kucuk: dict = {}
    for y, xs in ulasan.items():
        dmin = min(d(x, y) for x in xs)
        d1y = n2_d1[y]
        if d1y is None or dmin < d1y:
            n.append(y)
            en_kucuk[y] = dmin
    m = {x for x, (w, _d) in n1.items() if w == WILL_ALWAYS}       # adım 1
    for y in n:                                                     # adım 2
        if len(ulasan[y]) == 1:
            m.add(ulasan[y][0])
    dx = {x: sum(1 for y in n if x in ulasan[y]
                 and d(x, y) == en_kucuk[y]) for x in n1}

    def r(x):
        say = 0
        for y in n:
            if x in ulasan[y] and d(x, y) == en_kucuk[y]:
                if not any(z in m and d(z, y) == en_kucuk[y]
                           for z in ulasan[y]):
                    say += 1
        return say

    while True:                                                     # adım 3
        adaylar = [(n1[x][0], rx, dx[x], -x)
                   for x in n1 if x not in m for rx in (r(x),) if rx > 0]
        if not adaylar:
            break
        m.add(-max(adaylar)[3])
    return frozenset(m)


# ======================================================================
# DEMETLER
# ======================================================================
@dataclass(slots=True)
class _Bag:
    """Link Tuple — RFC 6130 §7.1 + RFC 7181 §8.1 + RFC 7779 §8."""
    heard_bitis: float                      # L_HEARD_time
    sym_bitis: float                        # L_SYM_time
    bitis: float                            # L_time
    in_metrik: int | None = None            # L_in_metric (None = UNKNOWN)
    out_metrik: int | None = None           # L_out_metric
    mpr_secici: bool = False                # L_mpr_selector (bayrak MPR'si)
    durum: int = -1                         # son hesaplanan L_status
    # RFC 7779 §8 · §8.1
    alinan: deque = field(default_factory=lambda: deque(
        [0] * DAT_MEMORY_LENGTH, maxlen=DAT_MEMORY_LENGTH))
    toplam: deque = field(default_factory=lambda: deque(
        [0] * DAT_MEMORY_LENGTH, maxlen=DAT_MEMORY_LENGTH))
    paket_zamani: float = _SURESI_DOLMUS    # L_DAT_packet_time
    hello_araligi: float | None = None      # L_DAT_hello_interval
    kayip_aralik: int = 0                   # L_DAT_lost_packet_intervals
    son_psn: int | None = None              # L_DAT_last_pkt_seqno


@dataclass(slots=True)
class _Komsu:
    """Neighbor Tuple — RFC 6130 §8.1 + RFC 7181 §9."""
    simetrik: bool = False                  # N_symmetric
    kaynak: int | None = None               # N_orig_addr (düğüm kimliği)
    will_flooding: int = WILL_NEVER
    will_routing: int = WILL_NEVER
    flooding_mpr: bool = False
    routing_mpr: bool = False
    mpr_secici: bool = False                # N_mpr_selector (yönlendirme)
    ilan: bool = False                      # N_advertised


class OLSRv2:
    """Optimized Link State Routing Protocol version 2 — RFC 7181."""

    ad = "olsrv2"
    kosum_beaconi = False               # kendi HELLO'su (NHDP), 2 s

    __slots__ = ("kimlik", "_adres", "_psn", "_msn", "_ansn", "_bag",
                 "_komsu", "_kayip_komsu", "_iki", "_ar", "_tr", "_islenen",
                 "_alinan", "_iletilen", "_rota", "_kirli", "_ilan_onceki",
                 "_son_dolu_tc", "_basladi", "_kopuk", "_bilinen",
                 "_sym_onceki", "_bekleyen_ilet", "_ilet_sira", "_yenile_s",
                 "_sayac")

    def __init__(self, kimlik: int) -> None:
        self.kimlik = kimlik
        self._adres = _adres(kimlik)
        self._psn = 0                       # RFC 5444 paket sırası
        self._msn = 0                       # TC mesaj sırası
        self._ansn = 0                      # §9 ANSN
        self._bag: dict[int, _Bag] = {}
        self._komsu: dict[int, _Komsu] = {}
        self._kayip_komsu: dict[int, float] = {}       # NL → NL_time
        # (komşu, 2-atlama) → [N2_time, N2_in_metric, N2_out_metric]
        self._iki: dict[tuple[int, int], list] = {}
        self._ar: dict[int, tuple[int, float]] = {}    # AR → (seq, time)
        # (from, to) → (seq, metric, time)
        self._tr: dict[tuple[int, int], tuple[int, int, float]] = {}
        self._islenen: dict[tuple, float] = {}         # Processed Set
        self._alinan: dict[tuple, float] = {}          # Received Set
        self._iletilen: dict[tuple, float] = {}        # Forwarded Set
        self._rota: dict[int, tuple[int, int, int]] = {}  # hedef → (sonraki,
        #                                                   metrik, atlama)
        self._kirli = True
        # En erken süre dolumu: o anda temizlik ve yeniden hesap (OLSR v1'in
        # tembel süzmesi; karar zaman ızgarasına bağlı kalmaz).
        self._yenile_s = float("inf")
        self._ilan_onceki: dict[int, int | None] = {}
        self._son_dolu_tc = _SURESI_DOLMUS
        self._basladi = False
        # Titreşimle bekleyen iletmeler: sıra → mesaj baytları.
        self._bekleyen_ilet: dict[int, bytes] = {}
        self._ilet_sira = 0
        # 🔒 ÖLÇÜM DURUMU — karara GİRMEZ (K-139 anlamı).
        self._kopuk: dict[int, set[int]] = {}
        self._bilinen: set[int] = set()
        self._sym_onceki: frozenset[int] = frozenset()
        self._sayac: dict[str, int] = {
            "hello_uretilen": 0, "tc_uretilen": 0, "tc_bos": 0,
            "tc_iletilen": 0, "tc_islenen": 0, "tc_eski": 0,
            "tc_tekrar": 0, "gecersiz_mesaj": 0, "rota_hesap": 0,
            "mpr_hesap": 0, "komsu_kaybi": 0, "dat_guncelleme": 0,
        }

    # ==================================================================
    # YARDIMCILAR
    # ==================================================================
    def _psn_al(self) -> int:
        self._psn = (self._psn + 1) & _ALAN_16
        return self._psn

    @staticmethod
    def _durum(b: _Bag, simdi: float) -> int:
        """RFC 6130 §7.1 — bağ kalitesi yok: PENDING ve L_lost oluşmaz.
        Süre `simdi >= t` olunca dolmuştur (§7)."""
        if b.sym_bitis > simdi:
            return SYMMETRIC
        if b.heard_bitis > simdi:
            return HEARD
        return LOST

    def _n_metrik(self, n: int, simdi: float) -> tuple:
        """§17.3 — N_in_metric, N_out_metric (tek bağ)."""
        k = self._komsu.get(n)
        b = self._bag.get(n)
        if k is None or not k.simetrik or b is None \
                or self._durum(b, simdi) != SYMMETRIC:
            return None, None
        return b.in_metrik, b.out_metrik

    def _paket(self, mesaj: bytes) -> dict:
        return {"rfc5444": tuple(paket_kodla([mesaj], sira=self._psn_al()))}

    # ==================================================================
    # §13 · §17 — BİLGİ TABANI DEĞİŞİKLİKLERİ
    # ==================================================================
    def _bag_gecisleri(self, simdi: float) -> None:
        """RFC 6130 §13 + RFC 7181 §17.2 · §17.3: durum değişimlerinin ve
        süre dolumlarının sonuçları. Her kancada, kararlardan önce."""
        for n in list(self._bag):
            b = self._bag[n]
            yeni = self._durum(b, simdi)
            # §17.2: L_out_metric bilinmiyorsa SYMMETRIC olamaz.
            if yeni == SYMMETRIC and b.out_metrik is None:
                b.sym_bitis = _SURESI_DOLMUS
                yeni = self._durum(b, simdi)
            silinecek = b.bitis <= simdi
            if b.durum == SYMMETRIC and (yeni != SYMMETRIC or silinecek):
                self._simetrik_degil(n, simdi)                    # §13.2
            elif yeni == SYMMETRIC and b.durum != SYMMETRIC:
                k = self._komsu.setdefault(n, _Komsu())          # §13.1
                k.simetrik = True
                self._kayip_komsu.pop(n, None)
                self._kirli = True
            if yeni != SYMMETRIC:
                b.mpr_secici = False                              # §17.2
            if silinecek or b.heard_bitis <= simdi:
                if n in self._komsu:                              # §13.3
                    del self._komsu[n]
                    self._kirli = True
            if silinecek:
                del self._bag[n]
                self._kirli = True
                continue
            if yeni != b.durum:
                b.durum = yeni
                self._kirli = True

    def _simetrik_degil(self, n: int, simdi: float) -> None:
        """RFC 6130 §13.2 + RFC 7181 §17.3 madde 3."""
        for anahtar in [a for a in self._iki if a[0] == n]:
            del self._iki[anahtar]
        k = self._komsu.get(n)
        if k is not None and k.simetrik:
            k.simetrik = False
            k.flooding_mpr = k.routing_mpr = False
            k.mpr_secici = k.ilan = False
            self._kayip_komsu[n] = simdi + N_HOLD_TIME_S
        self._sayac["komsu_kaybi"] += 1
        self._kirli = True

    def _temizle(self, simdi: float) -> None:
        """Süresi dolan demetler — "MUST be removed"."""
        for a in [a for a, d in self._iki.items() if d[0] <= simdi]:
            del self._iki[a]
            self._kirli = True
        for n in [n for n, t in self._kayip_komsu.items() if t <= simdi]:
            del self._kayip_komsu[n]
        for o in [o for o, (_s, t) in self._ar.items() if t <= simdi]:
            del self._ar[o]                                       # §17.5
            for a in [a for a in self._tr if a[0] == o]:
                del self._tr[a]
            self._kirli = True
        for a in [a for a, (_s, _m, t) in self._tr.items() if t <= simdi]:
            del self._tr[a]
            self._kirli = True
        for kume in (self._islenen, self._alinan, self._iletilen):
            for a in [a for a, t in kume.items() if t <= simdi]:
                del kume[a]

    def _guncelle(self, simdi: float) -> tuple:
        """Geçişler → MPR (§17.6, §18) → ANSN (§17.4) → rota (§17.7, §19)
        → ölçüm beyanları. Döner: beyanlar."""
        if simdi >= self._yenile_s:
            self._temizle(simdi)
            self._yenile_s = self._en_erken(simdi)
        self._bag_gecisleri(simdi)
        if not self._kirli:
            return ()
        self._kirli = False
        self._mpr_hesapla(simdi)
        ilan = {n: self._n_metrik(n, simdi)[1]
                for n, k in self._komsu.items() if k.ilan and k.simetrik}
        if ilan != self._ilan_onceki:
            self._ansn = (self._ansn + 1) & _ALAN_16              # §17.4
            self._ilan_onceki = ilan
        onceki = self._rota
        self._rota_hesapla(simdi)
        beyanlar: list = []
        sym = frozenset(n for n, k in self._komsu.items() if k.simetrik)
        for n in sorted(self._sym_onceki - sym):
            etkilenen = {d for d, (s, _m, _h) in onceki.items() if s == n}
            if etkilenen:
                self._kopuk.setdefault(n, set()).update(etkilenen)
                beyanlar.append(Beyan("kopma", komsu=n))
        for n in [n for n, h in self._kopuk.items() if h & self._rota.keys()]:
            del self._kopuk[n]
            beyanlar.append(Beyan("rota_kuruldu", komsu=n))
        self._bilinen |= self._rota.keys()
        self._sym_onceki = sym
        self._yenile_s = self._en_erken(simdi)
        return tuple(beyanlar)

    def _en_erken(self, simdi: float) -> float:
        adaylar = [t for b in self._bag.values()
                   for t in (b.sym_bitis, b.heard_bitis, b.bitis) if t > simdi]
        adaylar += [d[0] for d in self._iki.values()]
        adaylar += [t for _s, t in self._ar.values()]
        adaylar += [t for _s, _m, t in self._tr.values()]
        return min(adaylar, default=float("inf"))

    # ==================================================================
    # §18 · MPR
    # ==================================================================
    def _mpr_hesapla(self, simdi: float) -> None:
        self._sayac["mpr_hesap"] += 1
        # §18.4 · bayrak MPR'leri, B: metrik yerine 1 (atlama sayısı) —
        # olsrd2'nin bayrak alanı sabit "Hopcount metric"le kurulur
        # (`nhdp_domain.c` `_flooding_domain.metric = &_no_metric`). Bilinmeyen
        # metrikli bağ ve 2-atlama demeti yine KULLANILMAZ (§18.4).
        ulasilir = {n for n, b in self._bag.items()
                    if self._durum(b, simdi) == SYMMETRIC
                    and b.out_metrik is not None}
        n1 = {n: (self._komsu[n].will_flooding, 1) for n in ulasilir
              if n in self._komsu
              and self._komsu[n].will_flooding > WILL_NEVER}
        d2 = {(x, y): 1 for (x, y), v in self._iki.items()
              if x in n1 and v[2] is not None}
        n2 = {y: (1 if y in ulasilir else None) for (_x, y) in d2}
        bayrak = mpr_sec(n1, n2, d2)
        # §18.5 · yönlendirme MPR'leri: gelen komşu metriği. 🔴 d2 için
        # N2_in_metric: §18.5'in metni "N2_out_metric" yazıyor ama izin
        # koşulu ve §4.6 gelen metrik diyor; olsrd2 de gelen kullanıyor
        # (beyan tablosu).
        n_in = {n: self._n_metrik(n, simdi)[0] for n in self._komsu}
        erisir = {n: m for n, m in n_in.items() if m is not None}
        n1 = {n: (self._komsu[n].will_routing, m) for n, m in erisir.items()
              if self._komsu[n].will_routing > WILL_NEVER}
        d2 = {(x, y): v[1] for (x, y), v in self._iki.items()
              if x in n1 and v[1] is not None}
        n2 = {y: erisir.get(y) for (_x, y) in d2}
        yonlendirme = mpr_sec(n1, n2, d2)
        for n, k in self._komsu.items():
            k.flooding_mpr = n in bayrak
            k.routing_mpr = n in yonlendirme

    # ==================================================================
    # §19 · Ek C — ROTA KÜMESİ
    # ==================================================================
    def _rota_hesapla(self, simdi: float) -> None:
        """Omurga: X→Y (komşu, N_out_metric) ve W→U (TR_metric) üzerinde en
        küçük toplam metrik; eşitlikte az atlama (§19.2 SHOULD), sonra Ek
        C.1'in komşu tercihi (N_will_routing büyük, MPR seçicisi), sonra
        küçük kimlik. Son olarak 2-atlama kenarları yalnız başka yolu
        olmayan hedeflere (§19.1 İSTEĞE BAĞLI, Ek C.7)."""
        self._sayac["rota_hesap"] += 1
        rota: dict[int, tuple[int, int, int]] = {}
        tercih: dict[int, tuple] = {}
        yigin: list = []
        for n, k in self._komsu.items():
            out = self._n_metrik(n, simdi)[1]
            if out is None or k.kaynak is None:
                continue
            t = (-k.will_routing, 0 if k.mpr_secici else 1, n)
            tercih[n] = t
            heapq.heappush(yigin, (out, 1, t, n, n))
        kenar: dict[int, list] = {}
        for (w, u), (_s, m, _t) in self._tr.items():
            kenar.setdefault(w, []).append((u, m))
        kesin: set[int] = set()
        while yigin:
            metrik, atlama, t, hedef, sonraki = heapq.heappop(yigin)
            if hedef in kesin or hedef == self.kimlik:
                continue
            kesin.add(hedef)
            rota[hedef] = (sonraki, metrik, atlama)
            for u, m in kenar.get(hedef, ()):
                if u not in kesin and u != self.kimlik:
                    heapq.heappush(yigin, (metrik + m, atlama + 1, t, u,
                                           sonraki))
        # Ek C.7 — 2-atlama kenarları Y→Z (N2_out_metric). §19.1: Z bir
        # omurga düğümüyse (komşu Y ya da TC kaynağı W) kenar KULLANILMAZ.
        omurga = {n for n, k in self._komsu.items() if k.kaynak is not None}
        omurga |= {w for (w, _u) in self._tr}
        aday: dict[int, tuple] = {}
        for (y, z), (_t, _i, out) in self._iki.items():
            if (out is None or z in rota or z in omurga
                    or z == self.kimlik):
                continue
            r = rota.get(y)
            if r is None or r[2] != 1:
                continue
            k = self._komsu.get(y)
            if k is None or k.will_routing == WILL_NEVER:
                continue
            yeni = (r[1] + out, 2, tercih.get(y, ()), y)
            if z not in aday or yeni < aday[z]:
                aday[z] = yeni
        for z, (m, h, _t, y) in aday.items():
            rota[z] = (y, m, h)
        self._rota = rota

    # ==================================================================
    # RFC 7779 · DAT
    # ==================================================================
    def _dat_paket(self, gonderen: int, psn: int | None,
                   simdi: float) -> None:
        """§9.3 — paketin mesajları işlendikten sonra."""
        b = self._bag.get(gonderen)
        if b is None or psn is None:
            return
        if b.son_psn is None:
            b.alinan[-1] = 1
            b.toplam[-1] = 1
        else:
            b.alinan[-1] += 1
            fark = (psn - b.son_psn) % 65536
            if fark > DAT_SEQNO_RESTART_DETECTION:
                fark = 1
            b.toplam[-1] += fark
        b.son_psn = psn
        if b.hello_araligi is not None:
            b.paket_zamani = simdi + b.hello_araligi * DAT_HELLO_TIMEOUT_FACTOR
        b.kayip_aralik = 0

    @staticmethod
    def _dat_hello(b: _Bag, aralik: float, simdi: float) -> None:
        """§9.4 — HELLO, NHDP işlemesinden sonra."""
        b.hello_araligi = aralik
        if b.son_psn is None:
            b.alinan[-1] += 1
            b.toplam[-1] += 1
            b.paket_zamani = simdi + aralik * DAT_HELLO_TIMEOUT_FACTOR

    def _dat_yenile(self, simdi: float) -> None:
        """§10.1 (paket zaman aşımları) · §10.2 (metrik)."""
        self._sayac["dat_guncelleme"] += 1
        for b in self._bag.values():
            while (b.hello_araligi is not None
                   and b.paket_zamani != _SURESI_DOLMUS
                   and b.paket_zamani <= simdi):
                if b.son_psn is None:
                    b.toplam[-1] += 1
                else:
                    b.kayip_aralik += 1
                b.paket_zamani += b.hello_araligi
            alinan = float(sum(b.alinan))
            toplam = float(sum(b.toplam))
            if b.hello_araligi is not None and b.kayip_aralik > 0:
                oran = (b.hello_araligi * b.kayip_aralik
                        / DAT_MEMORY_LENGTH)
                alinan *= max(0.0, 1.0 - oran)
            if alinan < 1.0:
                yeni = MAXIMUM_METRIC
            else:
                kayip = min(toplam / alinan, float(DAT_MAXIMUM_LOSS))
                hiz = max(DAT_RX_BITRATE_BPS, DAT_MINIMUM_BITRATE)
                yeni = int((1 << 24) / DAT_MAXIMUM_LOSS * kayip
                           / (hiz / DAT_MINIMUM_BITRATE))
                yeni = min(max(yeni, 1), MAXIMUM_METRIC)
            if yeni != b.in_metrik:
                b.in_metrik = yeni
                self._kirli = True
            b.toplam.append(0)
            b.alinan.append(0)

    # ==================================================================
    # HELLO ÜRETİMİ — RFC 6130 §11 + RFC 7181 §15.1
    # ==================================================================
    def _hello_kur(self, simdi: float) -> KontrolIstegi:
        adresler = {self._adres}
        local_if = {self._adres: bytes([THIS_IF])}
        durum: dict = {}
        diger: dict = {}
        metrik1: dict = {}
        metrik2: dict = {}
        mpr: dict = {}
        for n, b in self._bag.items():
            a = _adres(n)
            ls = self._durum(b, simdi)
            adresler.add(a)
            durum[a] = bytes([ls])
            degerler: list[tuple[int, int]] = []
            if ls in (HEARD, SYMMETRIC) and b.in_metrik is not None:
                bit = METRIK_GELEN_BAG
                k = self._komsu.get(n)
                if ls == SYMMETRIC and k is not None and k.simetrik:
                    bit |= METRIK_GELEN_KOMSU
                degerler.append((bit, b.in_metrik))
            if ls == SYMMETRIC and b.out_metrik is not None:
                degerler.append((METRIK_GIDEN_BAG | METRIK_GIDEN_KOMSU,
                                 b.out_metrik))
            if (len(degerler) == 2 and metrik_kodla(degerler[0][1])
                    == metrik_kodla(degerler[1][1])):
                degerler = [(degerler[0][0] | degerler[1][0],
                             degerler[0][1])]
            if degerler:
                metrik1[a] = _metrik_degeri(*degerler[0])
            if len(degerler) == 2:
                metrik2[a] = _metrik_degeri(*degerler[1])
            k = self._komsu.get(n)
            if ls == SYMMETRIC and k is not None and k.simetrik:
                v = ((MPR_FLOODING if k.flooding_mpr else 0)
                     | (MPR_ROUTING if k.routing_mpr else 0))
                if v:
                    mpr[a] = bytes([v])
        for n in self._kayip_komsu:                       # §11.1 madde 3
            a = _adres(n)
            if a not in adresler:
                adresler.add(a)
                diger[a] = bytes([LOST])
        vt, it = _KALIP_HELLO
        mesaj = mesaj_kodla(
            MSG_HELLO, kaynak=self._adres,
            mesaj_tlv=[(MTLV_VALIDITY_TIME, 0, vt),
                       (MTLV_INTERVAL_TIME, 0, it),
                       (MTLV_MPR_WILLING, 0, _ISTEK)],
            adresler=sorted(adresler),
            adres_tlv=[(ATLV_LOCAL_IF, 0, local_if),
                       (ATLV_LINK_STATUS, 0, durum),
                       (ATLV_OTHER_NEIGHB, 0, diger),
                       (ATLV_LINK_METRIC, 0, metrik1),
                       (ATLV_LINK_METRIC, 0, metrik2),
                       (ATLV_MPR, 0, mpr)])
        self._sayac["hello_uretilen"] += 1
        return KontrolIstegi.kur(None, HELLO, self._paket(mesaj))

    # ==================================================================
    # TC ÜRETİMİ — RFC 7181 §16.1 · §16.2
    # ==================================================================
    def _tc_kur(self, simdi: float) -> tuple:
        ilan = {n: m for n, m in self._ilan_onceki.items() if m is not None}
        if ilan:
            self._son_dolu_tc = simdi
        elif simdi >= self._son_dolu_tc + A_HOLD_TIME_S:
            return ()
        else:
            self._sayac["tc_bos"] += 1
        adresler = sorted(_adres(n) for n in ilan)
        self._msn = (self._msn + 1) & _ALAN_16
        vt, it = _KALIP_TC
        mesaj = mesaj_kodla(
            MSG_TC, kaynak=self._adres, hop_limit=TC_HOP_LIMIT, hop_count=0,
            sira=self._msn,
            mesaj_tlv=[(MTLV_VALIDITY_TIME, 0, vt),
                       (MTLV_INTERVAL_TIME, 0, it),
                       (MTLV_CONT_SEQ_NUM, CONT_COMPLETE,
                        self._ansn.to_bytes(2, "big"))],
            adresler=adresler,
            adres_tlv=[(ATLV_NBR_ADDR_TYPE, 0,
                        {a: bytes([ROUTABLE_ORIG]) for a in adresler}),
                       (ATLV_LINK_METRIC, 0,
                        {_adres(n): _metrik_degeri(METRIK_GIDEN_KOMSU, m)
                         for n, m in ilan.items()})])
        self._sayac["tc_uretilen"] += 1
        return (KontrolIstegi.kur(None, TC, self._paket(mesaj)),)

    # ==================================================================
    # HELLO İŞLEME — RFC 6130 §12 + RFC 7181 §15.3 + RFC 7779 §9.4
    # ==================================================================
    def _hello_gecerli(self, m) -> bool:
        """RFC 6130 §12.1 + RFC 7181 §15.3.1 (yapısal olanlar)."""
        if (m.hop_limit not in (None, 1) or m.hop_count not in (None, 0)
                or len(m.mesaj_tlv_degeri(MTLV_VALIDITY_TIME)) != 1
                or len(m.mesaj_tlv_degeri(MTLV_INTERVAL_TIME)) > 1
                or len(m.mesaj_tlv_degeri(MTLV_MPR_WILLING)) > 1
                or m.kaynak == self._adres):
            return False
        for a in m.adresler:
            ls = m.adres_degerleri(a, ATLV_LINK_STATUS)
            on = m.adres_degerleri(a, ATLV_OTHER_NEIGHB)
            if m.adres_degerleri(a, ATLV_LOCAL_IF) and (
                    a == self._adres or ls or on):
                return False
            if a == m.kaynak and (ls or on):                    # §15.3.1
                return False
            if (m.adres_degerleri(a, ATLV_MPR)                  # §15.3.1
                    and SYMMETRIC not in {d[0] for d in ls if d}):
                return False
            gorulen: dict = {}                                  # §15.3.1
            for d in m.adres_degerleri(a, ATLV_LINK_METRIC):
                v = int.from_bytes(d[:2].ljust(2, b"\0"), "big")
                for bit in (METRIK_GELEN_BAG, METRIK_GIDEN_BAG,
                            METRIK_GELEN_KOMSU, METRIK_GIDEN_KOMSU):
                    if v & bit:
                        if gorulen.setdefault(bit, v & 0x0FFF) != v & 0x0FFF:
                            return False
        return True

    def _hello_isle(self, gonderen: int, m, simdi: float) -> None:
        gecerlilik = zaman_coz(m.mesaj_tlv_degeri(MTLV_VALIDITY_TIME)[0][0])
        benim = [d[0] for d in m.adres_degerleri(self._adres,
                                                 ATLV_LINK_STATUS) if d]
        # §12.3 · Neighbor Set (tek adres: Removed/Lost Address List boş).
        k = self._komsu.setdefault(gonderen, _Komsu())
        # §12.5 · Link Set
        b = self._bag.get(gonderen)
        if b is None:
            b = _Bag(heard_bitis=_SURESI_DOLMUS, sym_bitis=_SURESI_DOLMUS,
                     bitis=simdi + gecerlilik)
            self._bag[gonderen] = b
            self._kirli = True
        if HEARD in benim or SYMMETRIC in benim:                   # 4.1.1
            b.sym_bitis = simdi + gecerlilik
        elif LOST in benim:                                        # 4.1.2
            if b.sym_bitis > simdi:
                b.sym_bitis = _SURESI_DOLMUS
                if self._durum(b, simdi) == HEARD:
                    b.bitis = simdi + L_HOLD_TIME_S
        b.heard_bitis = max(simdi + gecerlilik, b.sym_bitis)       # 4.3
        if self._durum(b, simdi) in (HEARD, SYMMETRIC):            # 4.5
            b.bitis = max(b.bitis, b.heard_bitis + L_HOLD_TIME_S)
            # RFC 7181 §15.3.2.1: L_in_metric HEARD/SYMMETRIC olunca
            # belirli olmalı; başka değer yoksa MAXIMUM_METRIC.
            if b.in_metrik is None:
                b.in_metrik = MAXIMUM_METRIC
        # RFC 7181 §15.3.2.1: SYMMETRIC bağın L_out_metric'i, komşunun
        # benim adresime ilan ettiği gelen bağ metriği.
        if self._durum(b, simdi) == SYMMETRIC:
            yeni = _metrik_oku(m.adres_degerleri(self._adres,
                                                 ATLV_LINK_METRIC),
                               METRIK_GELEN_BAG)
            if yeni != b.out_metrik:
                b.out_metrik = yeni
                self._kirli = True
        # §13 sonuçları hemen (§12'nin son paragrafı) — 2-Hop'tan önce.
        self._bag_gecisleri(simdi)
        if gonderen not in self._komsu:
            return
        k = self._komsu[gonderen]
        # §12.6 · 2-Hop Set (bağ SYMMETRIC ise).
        if self._durum(b, simdi) == SYMMETRIC:
            for z in m.adresler:
                if z == self._adres or z == _adres(gonderen):
                    continue
                ls = m.adres_degerleri(z, ATLV_LINK_STATUS)
                on = m.adres_degerleri(z, ATLV_OTHER_NEIGHB)
                ls_v = {d[0] for d in ls if d}
                on_v = {d[0] for d in on if d}
                anahtar = (gonderen, _dugum(z))
                if SYMMETRIC in ls_v or SYMMETRIC in on_v:
                    met = m.adres_degerleri(z, ATLV_LINK_METRIC)
                    yeni = [simdi + gecerlilik,
                            _metrik_oku(met, METRIK_GELEN_KOMSU),
                            _metrik_oku(met, METRIK_GIDEN_KOMSU)]
                    eski = self._iki.get(anahtar)
                    if eski is None or eski[1:] != yeni[1:]:
                        self._kirli = True
                    self._iki[anahtar] = yeni
                elif ls_v & {LOST, HEARD} or LOST in on_v:
                    if self._iki.pop(anahtar, None) is not None:
                        self._kirli = True
        # RFC 7181 §15.3.2 — MPR_WILLING varsa.
        istek = m.mesaj_tlv_degeri(MTLV_MPR_WILLING)
        if istek and istek[0]:
            k.kaynak = gonderen
            v = istek[0][0]
            if (v >> 4, v & 0x0F) != (k.will_flooding, k.will_routing):
                k.will_flooding, k.will_routing = v >> 4, v & 0x0F
                self._kirli = True
            mpr_v = 0
            for d in m.adres_degerleri(self._adres, ATLV_MPR):
                if d:
                    mpr_v |= d[0]
            sym_ilan = SYMMETRIC in benim
            if mpr_v & MPR_FLOODING:                           # §15.3.2.3
                b.mpr_secici = True
            elif sym_ilan:
                b.mpr_secici = False
            onceki = (k.mpr_secici, k.ilan)
            if mpr_v & MPR_ROUTING:
                k.mpr_secici = k.ilan = True
            elif sym_ilan:
                k.mpr_secici = k.ilan = False      # beyan: yalnız seçiciler
            if not k.simetrik:
                k.mpr_secici = k.ilan = False      # §17.3 madde 3
            if (k.mpr_secici, k.ilan) != onceki:
                self._kirli = True
        # RFC 7779 §9.4.
        it = m.mesaj_tlv_degeri(MTLV_INTERVAL_TIME)
        self._dat_hello(b, zaman_coz(it[0][0]) if it and it[0]
                        else gecerlilik, simdi)

    # ==================================================================
    # TC İŞLEME ve İLETME — RFC 7181 §14 · §16.3
    # ==================================================================
    def _tc_al(self, gonderen: int, m, simdi: float) -> tuple:
        if m.kaynak is None or m.sira is None:
            return ()                                          # §14
        if m.kaynak == self._adres:
            return ()                                          # §14.1 adım 1
        imza = (m.tur, m.kaynak, m.sira)
        # §14.2 — işleme (simetrik olmayan göndericininki de, beyan).
        if imza in self._islenen:
            self._sayac["tc_tekrar"] += 1
        else:
            self._islenen[imza] = simdi + P_HOLD_TIME_S
            self._tc_isle(m, simdi)
        # §14.3 — iletme.
        if not (m.hop_limit is not None and m.hop_limit > 1
                and (m.hop_count is None or m.hop_count < 255)):
            return ()
        b = self._bag.get(gonderen)
        if b is None or self._durum(b, simdi) != SYMMETRIC:
            return ()
        if imza in self._alinan:
            return ()
        self._alinan[imza] = simdi + RX_HOLD_TIME_S
        if imza in self._iletilen or not b.mpr_secici:
            return ()
        self._iletilen[imza] = simdi + F_HOLD_TIME_S
        # RFC 5148 §5.3: iletme U(0, F_MAXJITTER) gecikir; paket sıra
        # numarası paket havaya çıkarken verilir (Uyandırma'da).
        self._ilet_sira += 1
        self._bekleyen_ilet[self._ilet_sira] = iletim_icin(m)
        return (Uyandirma(_EN_KISA_S, f"{_ILET}{self._ilet_sira}",
                          jitter_s=F_MAXJITTER_S),)

    def _tc_isle(self, m, simdi: float) -> None:
        """§16.3.1 – §16.3.4."""
        vt = m.mesaj_tlv_degeri(MTLV_VALIDITY_TIME)
        csn = m.mesaj_tlv_degeri(MTLV_CONT_SEQ_NUM, CONT_COMPLETE)
        nbr = [a for a in m.adresler
               if any(d and d[0] & ORIGINATOR
                      for d in m.adres_degerleri(a, ATLV_NBR_ADDR_TYPE))]
        if (len(vt) != 1 or len(csn) > 1 or (nbr and not csn)
                or m.kaynak in nbr):
            self._sayac["gecersiz_mesaj"] += 1
            return
        if not csn:
            return
        gecerlilik = zaman_coz(vt[0][0])
        ansn = int.from_bytes(csn[0][:2].ljust(2, b"\0"), "big")
        o = _dugum(m.kaynak)
        ar = self._ar.get(o)
        if ar is not None and _sira_buyuk(ar[0], ansn):           # 16.3.3.1
            self._sayac["tc_eski"] += 1
            return
        self._ar[o] = (ansn, simdi + gecerlilik)
        for a in nbr:                                              # 16.3.3.2
            if a == self._adres:
                continue
            u = _dugum(a)
            met = _metrik_oku(m.adres_degerleri(a, ATLV_LINK_METRIC),
                              METRIK_GIDEN_KOMSU)
            if met is None:
                if self._tr.pop((o, u), None) is not None:
                    self._kirli = True
                continue
            eski = self._tr.get((o, u))
            if eski is None or eski[1] != met:
                self._kirli = True
            self._tr[(o, u)] = (ansn, met, simdi + gecerlilik)
        for a in [a for a, (s, _m, _t) in self._tr.items()          # 16.3.4.1
                  if a[0] == o and _sira_buyuk(ansn, s)]:
            del self._tr[a]
            self._kirli = True
        self._sayac["tc_islenen"] += 1

    # ==================================================================
    # KANCA · kontrol mesajı alındı
    # ==================================================================
    def kontrol_alindi(self, gozlem: Gozlem, gonderen: int, bicim: str,
                       yuk, yayin: bool) -> tuple:
        simdi = float(gozlem.saat_s)
        self._bag_gecisleri(simdi)
        try:
            psn, mesajlar = paket_coz(bytes(dict(yuk)["rfc5444"]))
        except BicimHatasi:
            self._sayac["gecersiz_mesaj"] += 1
            return self._guncelle(simdi)
        niyet: tuple = ()
        for m in mesajlar:
            if m.tur == MSG_HELLO:
                if self._hello_gecerli(m):
                    self._hello_isle(gonderen, m, simdi)
                else:
                    self._sayac["gecersiz_mesaj"] += 1
            elif m.tur == MSG_TC:
                niyet += self._tc_al(gonderen, m, simdi)
        self._dat_paket(gonderen, psn, simdi)                  # RFC 7779 §9.3
        return niyet + self._guncelle(simdi)

    # ==================================================================
    # KANCA · zamanlayıcılar ve uyandırmalar
    # ==================================================================
    def zamanlayicilar(self) -> dict:
        return {"dat": DAT_REFRESH_INTERVAL_S}

    def zamanlayici_doldu(self, gozlem: Gozlem, etiket: str) -> tuple:
        simdi = float(gozlem.saat_s)
        niyet: tuple = ()
        if not self._basladi:
            # HELLO ve TC zincirleri ilk tikte başlar; her biri kendinden
            # sonrakini RFC 5148 §5.1 dağılımıyla çizelgeler.
            self._basladi = True
            niyet = (Uyandirma(HELLO_INTERVAL_S - HP_MAXJITTER_S, _HELLO,
                               jitter_s=HP_MAXJITTER_S),
                     Uyandirma(TC_INTERVAL_S - TP_MAXJITTER_S, _TC,
                               jitter_s=TP_MAXJITTER_S))
        self._bag_gecisleri(simdi)
        self._temizle(simdi)
        self._dat_yenile(simdi)
        return niyet + self._guncelle(simdi)

    def uyandi(self, gozlem: Gozlem, etiket: str) -> tuple:
        simdi = float(gozlem.saat_s)
        beyan = self._guncelle(simdi)
        if etiket == _HELLO:
            return (self._hello_kur(simdi),
                    Uyandirma(HELLO_INTERVAL_S - HP_MAXJITTER_S, _HELLO,
                              jitter_s=HP_MAXJITTER_S)) + beyan
        if etiket == _TC:
            return self._tc_kur(simdi) + (
                Uyandirma(TC_INTERVAL_S - TP_MAXJITTER_S, _TC,
                          jitter_s=TP_MAXJITTER_S),) + beyan
        if etiket.startswith(_ILET):
            ham = self._bekleyen_ilet.pop(int(etiket[len(_ILET):]), None)
            if ham is not None:
                self._sayac["tc_iletilen"] += 1
                return (KontrolIstegi.kur(None, TC, {
                    "rfc5444": tuple(paket_kodla([ham],
                                                 sira=self._psn_al()))}),
                        ) + beyan
        return beyan

    # ==================================================================
    # KANCA · veri
    # ==================================================================
    def sonraki_atlama(self, gozlem: Gozlem) -> Karar:
        if gozlem.paket is None:
            return Karar()
        simdi = float(gozlem.saat_s)
        beyan = self._guncelle(simdi)
        hedef = gozlem.paket.hedef
        r = self._rota.get(hedef)
        if r is not None:
            return Karar(sonraki=r[0], beyan=beyan)
        # Proaktif: tampon yok, rota yoksa paket düşer (beyan tablosu).
        if hedef in self._bilinen:
            beyan = beyan + (Beyan("rota_gecersiz", komsu=hedef),)
        return Karar(sonraki=None, beyan=beyan)

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
    def teshis(self, dugum: int) -> dict:
        """🔴 Yalnız sonuç satırına; karara GİRMEZ."""
        return {**self._sayac,
                "komsu_simetrik": len(self._sym_onceki),
                "iki_atlama": len(self._iki),
                "mpr_bayrak": sum(1 for k in self._komsu.values()
                                  if k.flooding_mpr),
                "mpr_yonlendirme": sum(1 for k in self._komsu.values()
                                       if k.routing_mpr),
                "ilan": sum(1 for k in self._komsu.values() if k.ilan),
                "topoloji": len(self._tr),
                "rota": len(self._rota)}
