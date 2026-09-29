"""
OLSR — RFC 3626'ya sadık gerçekleme. Aşama 2'nin ikinci taban protokolü.

🔒 KÂHİN ERİŞİMİ YOK
====================
Bu modül yalnız `sim2/gozlem/`i içe aktarır (`aodv.py` ile aynı sözleşme).
Bildiği her şey ya aldığı bir OLSR paketinden ya kendi saatinden gelir. Bağ
kalitesini bile KENDİ ölçer: bağ histerezisi (§14) komşunun paket sıra
numaralarındaki boşluklardan ve sessizlik sürelerinden beslenir — simülatörün
SINR'ından değil.

🔒 PARAMETRELER RFC VARSAYILANIDIR, SEÇİLMEDİ
=============================================
Hepsi `olsr_bicim.py`de ve hepsi RFC 3626 §18'in ham metninden. Bu dosyada
ayarlanabilir tek bir sayı yoktur — tek istisna süpürme ızgarası, aşağıda
gerekçesiyle.

🔴 KARAR KURALI — öğrencinin (19 Eylül 2026): SHOULD UYGULANIR, MAY BEYAN EDİLİR
=================================================================================
Uygulanan SHOULD'lar: bağ histerezisi (§14) · üretim VE iletme titreşimi
(§3.5) · ANSN'nin eklemede de artması (§9.2) · boş TC'nin `TOP_HOLD_TIME`
boyunca sürmesi ve bağ kaybına bağlı erken TC (§9.3). Beyan edilen MAY'ler
`olsr_bicim.py` başlığında tabloyla.

🔴 TİTREŞİM RFC'NİN DAĞILIMIYLA — erkene çekme, gecikme DEĞİL
=============================================================
§3.5: *"Actual message interval = MESSAGE_INTERVAL − jitter"*, jitter
`U(0, MAXJITTER)`. Basit yol (sabit periyot + `U(0, MAXJITTER)` gecikme)
ortalama HELLO aralığını 2,0 s tutardı; RFC'ninki **1,75 s** — yani OLSR'ın
kontrol yükü %14 olduğundan DÜŞÜK ölçülürdü. Doğru dağılım sözleşmeyle
birebir kuruluyor: her HELLO kendinden sonrakini
`Uyandirma(ARALIK − MAXJITTER, jitter=MAXJITTER)` ile çizelgeler; gerçek
aralık `ARALIK − MAXJITTER + U(0, MAXJITTER) = ARALIK − U(0, MAXJITTER)`.

🔒 SÜPÜRME IZGARASI — `HELLO_INTERVAL / 2` = 1,0 s
==================================================
RFC ayrı bir periyot tanımlamaz; süpürme bir gerçekleme ayrıntısıdır. İki
işi var: (1) histerezisin *"uzun sessizlik"* kuralı — bir Htime boyunca
komşudan paket gelmemesini fark etmek — ve (2) süresi dolan girdileri
temizlemek. Htime'ın yarısı, sessizliğin en geç yarım Htime gecikmeyle fark
edilmesi demek. 🔒 AODV'nin süpürmesiyle (1,0 s) aynı çıkması KASITLI: iki
protokolün zaman aşımı çözünürlüğü farklı olsaydı karşılaştırmayı o fark
yönlendirirdi.
⚠️ Yönlendirme KARARI ızgaraya bağlı değildir: süresi dolmuş her girdi karar
anında zaten süzülür (tembel süzme). Izgara yalnız temizlik ve olay
tetiklemesi içindir.

🔴 PAKET SIRA NUMARASI TİTREŞİMDEN ÖNCE VERİLİYOR — alıcı bunu telafi eder
=========================================================================
RFC'de paket sıra numarası (PSN) paket HAVAYA ÇIKARKEN verilir (§3.3.1:
*"incremented by one each time a new OLSR packet is transmitted"*); titreşim
ondan önce uygulanır. Yani havada PSN'ler hep ARTAN sırada gider. Kontrol
düzlemi sözleşmesinde ise titreşim, istek OLUŞTURULDUKTAN sonra uygulanıyor
(`KontrolIstegi.jitter_s`) — PSN'si önce verilen bir iletme, rastgele
gecikmesi yüzünden sonrakinin ARDINDAN çıkabiliyor.
🔴 ÖLÇÜLDÜ, ilk koşuda: 14 düğüm, 30 s — ~900 paket gönderilmişken histerezis
**2 563** "kayıp" saydı; bağlar sahte kayıplarla "bekleyen"e düştü ve PDR
0,577'de kaldı. Düzeltilmeseydi OLSR'ı olduğundan kötü gösteren bir
straw-man olurdu.
🔒 Düzeltme PARAMETRESİZ: bir sıra boşluğu hemen kayıp sayılmaz, eksik
numara `MAXJITTER` kadar BEKLENİR. Titreşimin üst sınırı tam olarak budur —
önce oluşturulmuş bir paket sonrakinden en fazla `MAXJITTER` geç gelebilir
(MAC kuyruğu FIFO'dur). Pencerede gelirse kayıp değildir. RFC'nin kendi
modelinde hiç sıra değişmediği için bu, RFC'nin anlamını BİREBİR geri kurar.

🔒 ÖLÇÜM BEYANLARI — AODV ile AYNI anlam (`04` K-139)
=====================================================
    kopma(K)         simetrik komşu K kaybedildi VE yönlendirme tablosunda en
                     az bir hedefin sonraki atlamasıydı
    rota_kuruldu(K)  K'nin kaybının etkilediği bir hedefe yeniden rota var
    rota_gecersiz    daha önce rotası olan bir hedefe artık rota yok
İki protokolün Δ'sı ve COR'u böylece aynı şeyi ölçer.
"""

from __future__ import annotations

from dataclasses import dataclass

from sim2.gozlem.karar import Beyan, Karar
from sim2.gozlem.kontrol import KontrolIstegi, Uyandirma
from sim2.gozlem.pencere import Gozlem
from protokoller.olsr_bicim import (
    ASYM_LINK, DUP_HOLD_TIME_S, HELLO, HELLO_INTERVAL_S, HYST_SCALING,
    HYST_THRESHOLD_HIGH, HYST_THRESHOLD_LOW, LOST_LINK, MAXJITTER_S,
    MPR_NEIGH, NEIGHB_HOLD_TIME_S, NOT_NEIGH, SYM_LINK, SYM_NEIGH, TC,
    TC_INTERVAL_S, TC_TTL, TIP_HELLO, TIP_TC, TOP_HOLD_TIME_S, UNSPEC_LINK,
    WILL_ALWAYS, WILL_DEFAULT, WILL_NEVER, bag_kodu, bag_kodu_coz,
    zaman_coz, zaman_kodla)

__all__ = ["OLSR"]

_ALAN_16 = 0xFFFF
# 🔒 Süpürme ızgarası — başlıkta gerekçesiyle. RFC sabiti DEĞİL, türetme.
BAKIM_ARALIGI_S: float = HELLO_INTERVAL_S / 2
# Vtime/Htime alanları her mesajda aynı; bir kez kodlanır.
_VTIME_HELLO = zaman_kodla(NEIGHB_HOLD_TIME_S)
_VTIME_TC = zaman_kodla(TOP_HOLD_TIME_S)
_HTIME = zaman_kodla(HELLO_INTERVAL_S)


def _sira_buyuk(s1: int, s2: int) -> bool:
    """§19 · sarmalı karşılaştırma — `s1`, `s2`den "büyük" mü?"""
    return ((s1 > s2 and s1 - s2 <= _ALAN_16 // 2)
            or (s2 > s1 and s2 - s1 > _ALAN_16 // 2))


@dataclass(slots=True)
class _Bag:
    """§4.2.1 · bağ girdisi (tek arayüz: komşu arayüzü = komşu)."""
    sym_bitis: float                # L_SYM_time
    asym_bitis: float               # L_ASYM_time
    bitis: float                    # L_time — dolunca girdi SİLİNİR


@dataclass(slots=True)
class _Hist:
    """§14.1 · histerezis alanları — komşu ilk DUYULDUĞUNDA kurulur.

    🔒 Bağ girdisinden AYRI tutuluyor: bir TC, komşudan HELLO'dan önce
    gelebilir ve §14.3 kaliteyi *"NI ilk duyulduğunda"* başlatır. Bağ girdisi
    ise yalnız HELLO ile kurulur (§7.1.1). Kalite, bağ girdisi silinip yeniden
    kurulsa da sürer — ilk duyulma bir kez olur.
    """
    kalite: float                   # L_link_quality
    bekleyen: bool                  # L_link_pending
    kayip_bitis: float              # L_LOST_LINK_time
    son_psn: int
    son_duyulma_s: float
    htime_s: float                  # komşunun HELLO aralığı (son Htime)
    sessiz_sayilan: int             # bu sessizlik döneminde sayılmış kayıp
    # Sessizlik kuralının ÖNCEDEN saydığı, PSN'den henüz doğrulanmamış kayıp.
    # PSN kaybı kesinleşince önce bu krediden düşülür: aynı kayıp iki kez
    # sayılmaz.
    sessiz_kredi: int
    # Eksik PSN → kesinleşme anı (`MAXJITTER` sonra). Başlıkta gerekçesiyle.
    eksik: dict[int, float]


class OLSR:
    """Optimized Link State Routing — RFC 3626."""

    ad = "olsr"
    # 🔒 `13` §03.8 — kendi HELLO'sunu kendi RFC hızında (2 s) gönderir.
    # `02` §R3'ün straw-man riski (ortak 1 s beacon OLSR'ı RFC'sinin iki
    # katı hızda koşturuyordu) böylece yapısal olarak kapanır.
    kosum_beaconi = False

    __slots__ = ("kimlik", "_psn", "_msn", "_ansn", "_bag", "_hist", "_istek",
                 "_iki", "_mpr", "_secici", "_topoloji", "_tekrar", "_rota",
                 "_kirli", "_yenile_s", "_sym_onceki", "_kopuk", "_bilinen",
                 "_ilan", "_bos_tc_bitis", "_erken_tc_verildi", "_basladi",
                 "_sayac", "_s13")

    def __init__(self, kimlik: int, s13: bool = False) -> None:
        """`s13` — RFC 3626 §13 bağ katmanı bildirimi (MAY). 🔒 Varsayılan
        KAPALI (`OLSR-c`, K-196): öğrencinin kuralı "MAY beyan edilir";
        K-147'nin istisnası (`OLSR-b`, `s13=True`) eski dünyada ölçülmüş bir
        kazanca dayanıyordu, referans dünyada §13 OLSR'a zarar veriyor
        (K-193: §13'süz +0,031 · +0,028 · +0,105). `s13=True` eski hâli
        birebir üretir."""
        self.kimlik = kimlik
        self._s13 = bool(s13)
        self._psn = 0                   # §3.3.1 · paket sıra numarası
        self._msn = 0                   # §3.3.2 · mesaj sıra numarası
        self._ansn = 0                  # §9.2 · ilan edilen komşu sırası
        self._bag: dict[int, _Bag] = {}
        self._hist: dict[int, _Hist] = {}
        self._istek: dict[int, int] = {}            # N_willingness
        self._iki: dict[tuple[int, int], float] = {}  # (N, 2-atlama) → N_time
        self._mpr: frozenset[int] = frozenset()
        self._secici: dict[int, float] = {}         # MS_main_addr → MS_time
        # (T_dest, T_last) → (T_seq, T_time)
        self._topoloji: dict[tuple[int, int], tuple[int, float]] = {}
        # (D_addr, D_seq_num) → (D_retransmitted, D_time)
        self._tekrar: dict[tuple[int, int], tuple[bool, float]] = {}
        self._rota: dict[int, tuple[int, int]] = {}  # hedef → (sonraki, uzaklık)
        self._kirli = True
        self._yenile_s = float("inf")   # en erken girdi bitişi — tembel süzme
        self._sym_onceki: frozenset[int] = frozenset()
        # 🔒 ÖLÇÜM DURUMU — karara GİRMEZ (K-139 anlamı).
        self._kopuk: dict[int, set[int]] = {}
        self._bilinen: set[int] = set()
        self._ilan: frozenset[int] = frozenset()
        self._bos_tc_bitis = float("-inf")
        self._erken_tc_verildi = False
        self._basladi = False
        self._sayac: dict[str, int] = {
            "hello_uretilen": 0, "tc_uretilen": 0, "tc_iletilen": 0,
            "tc_islenen": 0, "tc_sira_disi": 0, "tc_tekrar": 0,
            "tc_simetriksiz": 0, "erken_tc": 0, "rota_hesap": 0,
            "hist_kayip_psn": 0, "hist_kayip_sessiz": 0,
            "komsu_kaybi": 0, "bag_katmani_kopma": 0,
        }

    # ==================================================================
    # SIRA NUMARALARI
    # ==================================================================
    def _psn_al(self) -> int:
        self._psn = (self._psn + 1) & _ALAN_16
        return self._psn

    def _msn_al(self) -> int:
        self._msn = (self._msn + 1) & _ALAN_16
        return self._msn

    # ==================================================================
    # §14 · BAĞ HİSTEREZİSİ — protokol bağ kalitesini KENDİ ölçer
    # ==================================================================
    def _histerezis_paket(self, ni: int, psn: int, simdi_s: float) -> None:
        """§14.3 · NI'dan bir OLSR paketi alındı: kayıplar + kararlılık kuralı."""
        h = self._hist.get(ni)
        if h is None:
            # *"the first time NI is heard by I, L_link_quality is set to
            # HYST_SCALING (L_link_pending is set to true and
            # L_LOST_LINK_time to current time − 1)"*. İlk duyuluş KURULUMDUR;
            # kararlılık kuralı bir sonraki paketten itibaren uygulanır.
            self._hist[ni] = _Hist(
                kalite=HYST_SCALING, bekleyen=True, kayip_bitis=simdi_s - 1,
                son_psn=psn, son_duyulma_s=simdi_s,
                htime_s=HELLO_INTERVAL_S, sessiz_sayilan=0,
                sessiz_kredi=0, eksik={})
            self._kirli = True
            return
        if psn in h.eksik:
            del h.eksik[psn]            # geç geldi — titreşim, KAYIP DEĞİL
        elif _sira_buyuk(psn, h.son_psn):
            # Aradaki numaralar EKSİK — kesinleşmeleri `MAXJITTER` sonra.
            p = (h.son_psn + 1) & _ALAN_16
            while p != psn:
                h.eksik[p] = simdi_s + MAXJITTER_S
                p = (p + 1) & _ALAN_16
            h.son_psn = psn
        self._eksik_kesinlestir(h, simdi_s)
        h.kalite = (1.0 - HYST_SCALING) * h.kalite + HYST_SCALING  # kararlılık
        h.son_duyulma_s = simdi_s
        h.sessiz_sayilan = 0
        self._histerezis_esik(ni, simdi_s)

    def _eksik_kesinlestir(self, h: _Hist, simdi_s: float) -> None:
        """Süresi dolan eksik PSN'ler KAYIPTIR — kararsızlık kuralı (§14.3).

        🔒 ÇİFT SAYMA YOK: sessizlik kuralı bu kayıpların bir kısmını ZATEN
        saydıysa, kesinleşen kayıplar önce o krediden düşülür.
        """
        biten = [p for p, t in h.eksik.items() if t <= simdi_s]
        if not biten:
            return
        for p in biten:
            del h.eksik[p]
        yeni = len(biten)
        dus = min(yeni, h.sessiz_kredi)
        h.sessiz_kredi -= dus
        yeni -= dus
        for _ in range(yeni):
            h.kalite *= (1.0 - HYST_SCALING)           # kararsızlık kuralı
        self._sayac["hist_kayip_psn"] += yeni

    def _histerezis_sessizlik(self, simdi_s: float) -> None:
        """§14.3 · *"long period of silence"* — her Htime'lık sessizlik bir kayıp."""
        for ni, h in self._hist.items():
            self._eksik_kesinlestir(h, simdi_s)
            donem = int((simdi_s - h.son_duyulma_s) // h.htime_s)
            yeni = donem - h.sessiz_sayilan
            if yeni > 0:
                for _ in range(yeni):
                    h.kalite *= (1.0 - HYST_SCALING)
                h.sessiz_sayilan = donem
                h.sessiz_kredi += yeni
                self._sayac["hist_kayip_sessiz"] += yeni
            self._histerezis_esik(ni, simdi_s)

    def _histerezis_esik(self, ni: int, simdi_s: float) -> None:
        """§14.3 · kalite eşiklerle karşılaştırılır; aradaki bant DOKUNULMAZ."""
        h = self._hist[ni]
        onceki = (h.bekleyen, h.kayip_bitis >= simdi_s)
        if h.kalite > HYST_THRESHOLD_HIGH:
            h.bekleyen = False
            h.kayip_bitis = simdi_s - 1
        elif h.kalite < HYST_THRESHOLD_LOW:
            h.bekleyen = True
            b = self._bag.get(ni)
            sinir = simdi_s + NEIGHB_HOLD_TIME_S
            h.kayip_bitis = min(b.bitis, sinir) if b is not None else sinir
        if (h.bekleyen, h.kayip_bitis >= simdi_s) != onceki:
            self._kirli = True

    # ==================================================================
    # KOMŞULUK — §14.2'nin "simetrik bağ" tanımı
    # ==================================================================
    def _simetrik_mi(self, n: int, simdi_s: float) -> bool:
        """§14.2 · LOST_LINK dolmuş · bekleyen değil · L_SYM_time dolmamış."""
        b = self._bag.get(n)
        if b is None or b.bitis < simdi_s or b.sym_bitis < simdi_s:
            return False
        h = self._hist.get(n)
        return h is not None and not h.bekleyen and h.kayip_bitis < simdi_s

    def _simetrik_komsular(self, simdi_s: float) -> frozenset[int]:
        return frozenset(n for n in self._bag if self._simetrik_mi(n, simdi_s))

    # ==================================================================
    # §8.3.1 · MPR BULUŞSALI — tek arayüz
    # ==================================================================
    def _mpr_hesapla(self, simdi_s: float, sym: frozenset[int]) -> None:
        ulasim: dict[int, set[int]] = {}
        for (y, z), t in self._iki.items():
            if t < simdi_s or y not in sym:
                continue
            if self._istek.get(y, WILL_DEFAULT) == WILL_NEVER:
                continue
            if z == self.kimlik or z in sym:
                continue
            ulasim.setdefault(y, set()).add(z)
        n2: set[int] = set().union(*ulasim.values()) if ulasim else set()
        # D(y): y'nin simetrik komşuları, N ve kendimiz HARİÇ.
        derece = {y: sum(1 for (yy, z), t in self._iki.items()
                         if yy == y and t >= simdi_s and z != self.kimlik
                         and z not in sym)
                  for y in sym}
        # Adım 1 — WILL_ALWAYS olanlar.
        mpr = {y for y in sym if self._istek.get(y) == WILL_ALWAYS}
        kapsanan: set[int] = set()
        for y in mpr:
            kapsanan |= ulasim.get(y, set())
        # Adım 3 — bir N2 düğümüne TEK başına erişen N üyeleri.
        for z in sorted(n2 - kapsanan):
            saglayan = [y for y in ulasim if z in ulasim[y]]
            if len(saglayan) == 1 and saglayan[0] not in mpr:
                mpr.add(saglayan[0])
                kapsanan |= ulasim[saglayan[0]]
        # Adım 4 — istek → erişim → derece; eşitlikte küçük kimlik (RFC
        # belirtmiyor; belirlenimci olsun diye).
        while n2 - kapsanan:
            kalan = n2 - kapsanan
            _, _, _, eksi = max(
                (self._istek.get(y, WILL_DEFAULT), len(ulasim[y] & kalan),
                 derece.get(y, 0), -y)
                for y in ulasim if y not in mpr and ulasim[y] & kalan)
            mpr.add(-eksi)
            kapsanan |= ulasim[-eksi]
        # Adım 5 (fazla MPR'yi ele) MAY — beyanlı, uygulanmıyor.
        self._mpr = frozenset(mpr)

    # ==================================================================
    # §10 · YÖNLENDİRME TABLOSU — en kısa yol, h = 1, 2, sonra topoloji
    # ==================================================================
    def _rota_hesapla(self, simdi_s: float, sym: frozenset[int]) -> None:
        rota: dict[int, tuple[int, int]] = {n: (n, 1) for n in sorted(sym)}
        for (n, z), t in sorted(self._iki.items()):
            if t < simdi_s or n not in sym:
                continue
            if self._istek.get(n, WILL_DEFAULT) == WILL_NEVER:
                continue
            if z == self.kimlik or z in rota:
                continue
            rota[z] = (rota[n][0], 2)
        h = 2
        while True:
            eklenen = False
            for (d, son), (_seq, t) in sorted(self._topoloji.items()):
                if t < simdi_s or d == self.kimlik or d in rota:
                    continue
                r = rota.get(son)
                if r is not None and r[1] == h:
                    rota[d] = (r[0], h + 1)
                    eklenen = True
            if not eklenen:
                break
            h += 1
        self._rota = rota
        self._sayac["rota_hesap"] += 1

    # ==================================================================
    # GÜNCELLEME — §8.5 komşuluk değişimi + MPR + rota + beyanlar
    # ==================================================================
    def _en_erken_bitis(self, simdi_s: float) -> float:
        """Tembel süzme için: bir sonraki girdi ne zaman dolacak?"""
        adaylar = [x for b in self._bag.values()
                   for x in (b.sym_bitis, b.bitis) if x >= simdi_s]
        adaylar += [h.kayip_bitis for h in self._hist.values()
                    if h.kayip_bitis >= simdi_s]
        adaylar += [t for t in self._iki.values() if t >= simdi_s]
        adaylar += [t for _s, t in self._topoloji.values() if t >= simdi_s]
        adaylar += [t for t in self._secici.values() if t >= simdi_s]
        return min(adaylar) if adaylar else float("inf")

    def _guncelle(self, simdi_s: float) -> tuple[tuple, tuple]:
        """Gerekiyorsa her şeyi yeniden hesaplar. Döner: (beyanlar, niyetler)."""
        if not self._kirli and simdi_s < self._yenile_s:
            return (), ()
        self._kirli = False
        beyanlar: list = []
        niyetler: list = []
        sym = self._simetrik_komsular(simdi_s)
        kaybolan = self._sym_onceki - sym
        secici_kayip = False
        for n in sorted(kaybolan):
            # §8.5 · komşu kaybı: 2-atlama girdileri ve MPR seçici SİLİNİR.
            self._sayac["komsu_kaybi"] += 1
            for k in [k for k in self._iki if k[0] == n]:
                del self._iki[k]
            if self._secici.pop(n, None) is not None:
                secici_kayip = True
            etkilenen = {d for d, (s, _u) in self._rota.items() if s == n}
            if etkilenen:
                self._kopuk.setdefault(n, set()).update(etkilenen)
                beyanlar.append(Beyan("kopma", komsu=n))
        self._mpr_hesapla(simdi_s, sym)
        self._rota_hesapla(simdi_s, sym)
        # K-139 anlamı: kopan komşunun etkilediği bir hedefe yeniden rota var.
        for n in [n for n, h in self._kopuk.items() if h & self._rota.keys()]:
            del self._kopuk[n]
            beyanlar.append(Beyan("rota_kuruldu", komsu=n))
        self._bilinen |= self._rota.keys()
        self._sym_onceki = sym
        # §9.3 · *"When a change to the MPR selector set is detected and this
        # change can be attributed to a link failure, a TC-message SHOULD be
        # transmitted after an interval shorter than TC_INTERVAL."* İki düzenli
        # TC arasında EN ÇOK BİR erken TC — RFC sıklığı belirtmiyor.
        if secici_kayip and not self._erken_tc_verildi:
            tc = self._tc_kur(simdi_s, erken=True)
            if tc:
                self._erken_tc_verildi = True
                self._sayac["erken_tc"] += 1
                niyetler.extend(tc)
        self._yenile_s = self._en_erken_bitis(simdi_s)
        return tuple(beyanlar), tuple(niyetler)

    # ==================================================================
    # §6.2 · HELLO ÜRETİMİ
    # ==================================================================
    def _hello_kur(self, simdi_s: float) -> KontrolIstegi:
        bloklar: dict[int, list[int]] = {}
        ilan_edilen: set[int] = set()
        for n, b in self._bag.items():
            if b.bitis < simdi_s:
                continue
            h = self._hist.get(n)
            if h is not None and h.kayip_bitis >= simdi_s:
                bt = LOST_LINK                          # §14.2 (1)
            elif h is None or h.bekleyen:
                continue                                # §14.2 (2)
            elif b.sym_bitis >= simdi_s:
                bt = SYM_LINK
            elif b.asym_bitis >= simdi_s:
                bt = ASYM_LINK
            else:
                bt = LOST_LINK
            bloklar.setdefault(bag_kodu(self._komsu_tipi(n, simdi_s), bt),
                               []).append(n)
            ilan_edilen.add(n)
        # §6.2 · bağı ilan edilmemiş komşular UNSPEC_LINK ile.
        for n, b in self._bag.items():
            if b.bitis >= simdi_s and n not in ilan_edilen:
                bloklar.setdefault(
                    bag_kodu(self._komsu_tipi(n, simdi_s), UNSPEC_LINK),
                    []).append(n)
        kodlar = sorted(bloklar)
        adresler = tuple(a for k in kodlar for a in sorted(bloklar[k]))
        mesaj_boyu = 12 + 4 + 4 * len(kodlar) + 4 * len(adresler)
        self._sayac["hello_uretilen"] += 1
        return KontrolIstegi.kur(None, HELLO, {
            "paket_boyu": mesaj_boyu + 4, "paket_sira": self._psn_al(),
            "mesaj_tipi": TIP_HELLO, "vtime": _VTIME_HELLO,
            "mesaj_boyu": mesaj_boyu, "kaynak": self.kimlik,
            "ttl": 1, "atlama": 0, "mesaj_sira": self._msn_al(),
            "ayrilmis": 0, "htime": _HTIME, "istek": WILL_DEFAULT,
            "blok_kodu": tuple(kodlar),
            "blok_ayrilmis": tuple(0 for _ in kodlar),
            "blok_boyu": tuple(4 + 4 * len(bloklar[k]) for k in kodlar),
            "komsu_adresi": adresler,
        })

    def _komsu_tipi(self, n: int, simdi_s: float) -> int:
        if n in self._mpr:
            return MPR_NEIGH
        return SYM_NEIGH if self._simetrik_mi(n, simdi_s) else NOT_NEIGH

    # ==================================================================
    # §9.2 · §9.3 · TC ÜRETİMİ
    # ==================================================================
    def _tc_kur(self, simdi_s: float, erken: bool = False) -> tuple:
        ilan = frozenset(n for n, t in self._secici.items() if t >= simdi_s)
        if ilan != self._ilan:
            # §9.2: ANSN kaldırmada MUST, eklemede SHOULD artar — ikisi de.
            self._ansn = (self._ansn + 1) & _ALAN_16
            self._ilan = ilan
        if ilan:
            self._bos_tc_bitis = simdi_s + TOP_HOLD_TIME_S
        elif simdi_s > self._bos_tc_bitis:
            return ()      # §9.3: boş küme — geçerlilik süresi dolunca DUR
        adresler = tuple(sorted(ilan))
        mesaj_boyu = 12 + 4 + 4 * len(adresler)
        self._sayac["tc_uretilen"] += 1
        return (KontrolIstegi.kur(None, TC, {
            "paket_boyu": mesaj_boyu + 4, "paket_sira": self._psn_al(),
            "mesaj_tipi": TIP_TC, "vtime": _VTIME_TC,
            "mesaj_boyu": mesaj_boyu, "kaynak": self.kimlik,
            "ttl": TC_TTL, "atlama": 0, "mesaj_sira": self._msn_al(),
            "ansn": self._ansn, "ayrilmis": 0, "komsu_adresi": adresler,
        # Erken TC'nin "TC_INTERVAL'dan kısa aralığı" iletme titreşimiyle.
        }, jitter_s=MAXJITTER_S if erken else 0.0),)

    # ==================================================================
    # §7.1.1 · §8.2.1 · §8.4.1 · HELLO İŞLEME
    # ==================================================================
    def _hello_isle(self, ni: int, y: dict, gecerlilik: float,
                    simdi_s: float) -> None:
        liste: list[tuple[int, int, int]] = []       # (adres, komşu t., bağ t.)
        i = 0
        for kod, boy in zip(y["blok_kodu"], y["blok_boyu"]):
            n = (boy - 4) // 4
            kt, bt = bag_kodu_coz(kod)
            liste.extend((a, kt, bt) for a in y["komsu_adresi"][i:i + n])
            i += n
        self._istek[ni] = y["istek"]
        self._hist[ni].htime_s = zaman_coz(y["htime"])
        # §7.1.1 · bağ algılama
        b = self._bag.get(ni)
        if b is None:
            b = _Bag(sym_bitis=simdi_s - 1, asym_bitis=simdi_s - 1,
                     bitis=simdi_s + gecerlilik)
            self._bag[ni] = b
        b.asym_bitis = simdi_s + gecerlilik
        for adres, _kt, bt in liste:
            if adres != self.kimlik:
                continue
            if bt == LOST_LINK:
                b.sym_bitis = simdi_s - 1
            elif bt in (SYM_LINK, ASYM_LINK):
                b.sym_bitis = simdi_s + gecerlilik
                b.bitis = b.sym_bitis + NEIGHB_HOLD_TIME_S
            break
        b.bitis = max(b.bitis, b.asym_bitis)
        # §8.2.1 · 2-atlama kümesi — yalnız SİMETRİK komşunun HELLO'sundan.
        if self._simetrik_mi(ni, simdi_s):
            for adres, kt, _bt in liste:
                if kt in (SYM_NEIGH, MPR_NEIGH):
                    if adres != self.kimlik:
                        self._iki[(ni, adres)] = simdi_s + gecerlilik
                elif kt == NOT_NEIGH:
                    self._iki.pop((ni, adres), None)
        # §8.4.1 · beni MPR seçti mi?
        for adres, kt, _bt in liste:
            if adres == self.kimlik and kt == MPR_NEIGH:
                self._secici[ni] = simdi_s + gecerlilik
        self._kirli = True

    # ==================================================================
    # §3.4 · §9.5 · TC İŞLEME ve §3.4.1 · VARSAYILAN İLETME
    # ==================================================================
    def _tc_isle(self, gonderen: int, y: dict, gecerlilik: float,
                 simdi_s: float) -> tuple:
        anahtar = (y["kaynak"], y["mesaj_sira"])
        kayit = self._tekrar.get(anahtar)
        taze_kayit = kayit is not None and kayit[1] >= simdi_s
        if taze_kayit:
            # §3.4 3.1 + 4.1 · tek arayüzde: işlendi VE iletme için düşünüldü.
            self._sayac["tc_tekrar"] += 1
            return ()
        simetrik = self._simetrik_mi(gonderen, simdi_s)
        if simetrik:
            self._topoloji_guncelle(y, gecerlilik, simdi_s)
        else:
            # §9.5 adım 1 · §3.4.1 adım 1 — işlenmez, iletilmez, tekrar
            # kümesine YAZILMAZ: sonraki bir kopya simetrik komşudan gelirse
            # işlenebilsin.
            self._sayac["tc_simetriksiz"] += 1
            return ()
        s = self._secici.get(gonderen)
        ilet = s is not None and s >= simdi_s and y["ttl"] > 1
        self._tekrar[anahtar] = (ilet, simdi_s + DUP_HOLD_TIME_S)
        if not ilet:
            return ()
        # §3.4.1 adım 6–8: TTL −1, atlama +1, mesaj başlığının geri kalanı
        # DEĞİŞMEZ. Paket başlığı atlama başınadır: kendi paket sıramız.
        yeni = dict(y)
        yeni["ttl"] = y["ttl"] - 1
        yeni["atlama"] = y["atlama"] + 1
        yeni["paket_sira"] = self._psn_al()
        self._sayac["tc_iletilen"] += 1
        # §3.5 · iletme titreşimi: *"Keep message period = jitter"*.
        return (KontrolIstegi.kur(None, TC, yeni, jitter_s=MAXJITTER_S),)

    def _topoloji_guncelle(self, y: dict, gecerlilik: float,
                           simdi_s: float) -> None:
        """§9.5 adım 2–4."""
        son, ansn = y["kaynak"], y["ansn"]
        for (_d, l), (seq, t) in self._topoloji.items():
            if l == son and t >= simdi_s and _sira_buyuk(seq, ansn):
                self._sayac["tc_sira_disi"] += 1
                return                              # adım 2 · sıra dışı
        for k in [k for k, (seq, _t) in self._topoloji.items()
                  if k[1] == son and _sira_buyuk(ansn, seq)]:
            del self._topoloji[k]                   # adım 3
        for d in y["komsu_adresi"]:
            self._topoloji[(d, son)] = (ansn, simdi_s + gecerlilik)
        self._sayac["tc_islenen"] += 1
        self._kirli = True

    # ==================================================================
    # KANCA · veri gönderme kararı
    # ==================================================================
    def sonraki_atlama(self, gozlem: Gozlem) -> Karar:
        if gozlem.paket is None:
            return Karar()
        simdi = float(gozlem.saat_s)
        beyanlar, niyetler = self._guncelle(simdi)
        hedef = gozlem.paket.hedef
        r = self._rota.get(hedef)
        if r is not None:
            return Karar(sonraki=r[0], beyan=beyanlar, niyetler=niyetler)
        # 🔒 Proaktif protokol TAMPONLAMAZ: rota yoksa paket düşer. Daha önce
        # rotası olan bir hedefse düşme sebebi `rota_gecersiz` (K-134).
        if hedef in self._bilinen:
            beyanlar = beyanlar + (Beyan("rota_gecersiz", komsu=hedef),)
        return Karar(sonraki=None, beyan=beyanlar, niyetler=niyetler)

    # ==================================================================
    # KANCA · beacon — koşum beacon'ı KAPALI
    # ==================================================================
    def beacon_yuku(self, gozlem: Gozlem) -> dict:
        return {}

    def beacon_alindi(self, gozlem: Gozlem, komsu: int, yuk) -> None:
        return None

    # ==================================================================
    # KANCA · zamanlayıcılar
    # ==================================================================
    def zamanlayicilar(self) -> dict:
        return {"bakim": BAKIM_ARALIGI_S}

    def zamanlayici_doldu(self, gozlem: Gozlem, etiket: str) -> tuple:
        simdi = float(gozlem.saat_s)
        niyet: tuple = ()
        if not self._basladi:
            # HELLO ve TC zincirleri ilk süpürmede başlar; her biri
            # kendinden sonrakini RFC'nin titreşim dağılımıyla çizelgeler.
            self._basladi = True
            niyet = (Uyandirma(HELLO_INTERVAL_S - MAXJITTER_S, "hello",
                               jitter_s=MAXJITTER_S),
                     Uyandirma(TC_INTERVAL_S - MAXJITTER_S, "tc",
                               jitter_s=MAXJITTER_S))
        self._histerezis_sessizlik(simdi)
        self._temizle(simdi)
        beyanlar, ek = self._guncelle(simdi)
        return niyet + beyanlar + ek

    def _temizle(self, simdi_s: float) -> None:
        """Süresi dolan girdiler — §4'ün *"MUST be removed"*leri."""
        for n in [n for n, b in self._bag.items() if b.bitis < simdi_s]:
            del self._bag[n]
            self._kirli = True
        for k in [k for k, t in self._iki.items() if t < simdi_s]:
            del self._iki[k]
            self._kirli = True
        for k in [k for k, (_s, t) in self._topoloji.items() if t < simdi_s]:
            del self._topoloji[k]
            self._kirli = True
        for n in [n for n, t in self._secici.items() if t < simdi_s]:
            del self._secici[n]
        for k in [k for k, (_r, t) in self._tekrar.items() if t < simdi_s]:
            del self._tekrar[k]

    def uyandi(self, gozlem: Gozlem, etiket: str) -> tuple:
        simdi = float(gozlem.saat_s)
        beyanlar, ek = self._guncelle(simdi)
        if etiket == "hello":
            return (self._hello_kur(simdi),
                    Uyandirma(HELLO_INTERVAL_S - MAXJITTER_S, "hello",
                              jitter_s=MAXJITTER_S)) + beyanlar + ek
        if etiket == "tc":
            self._erken_tc_verildi = False
            return self._tc_kur(simdi) + (
                Uyandirma(TC_INTERVAL_S - MAXJITTER_S, "tc",
                          jitter_s=MAXJITTER_S),) + beyanlar + ek
        return beyanlar + ek

    # ==================================================================
    # KANCA · kontrol mesajı alındı
    # ==================================================================
    def kontrol_alindi(self, gozlem: Gozlem, gonderen: int, bicim: str,
                       yuk, yayin: bool) -> tuple:
        simdi = float(gozlem.saat_s)
        y = dict(yuk)
        # §14.3 · her OLSR paketi bağ kalitesini besler — HELLO da, TC da.
        self._histerezis_paket(gonderen, y["paket_sira"], simdi)
        niyet: tuple = ()
        # §3.4 adım 2 · TTL tükendi ya da kendi mesajımız.
        if y["ttl"] > 0 and y["kaynak"] != self.kimlik:
            gecerlilik = zaman_coz(y["vtime"])
            if bicim == "HELLO":
                # §7.1.1 · HELLO ne iletilir ne tekrar kümesine yazılır.
                self._hello_isle(gonderen, y, gecerlilik, simdi)
            else:
                niyet = self._tc_isle(gonderen, y, gecerlilik, simdi)
        beyanlar, ek = self._guncelle(simdi)
        return niyet + beyanlar + ek

    # ==================================================================
    # KANCA · iletim başarısız
    # ==================================================================
    def iletim_basarisiz(self, gozlem: Gozlem, hedef: int | None,
                         tur: str) -> tuple:
        """§13 bağ katmanı bildirimi — MAY; varsayılan KAPALI (K-196),
        `s13=True` ile açılır (`OLSR-b`, `04` K-147).

        §13'ün üç maddesi: (1) `L_LOST_LINK_time` dolmamışsa bağ HELLO'da
        LOST_LINK ilan edilir ve simetrik sayılmaz — `_hello_kur` ile
        `_simetrik_mi` bunu §14 için zaten yapıyor; (2) aşağıda; (3) §8.5
        kaybı `_guncelle`de. ⚠️ §13 histerezisle BİRLİKTE yaşar: kalite
        eşiği aşan bir sonraki paket `L_LOST_LINK_time`ı geri alır (§14.3).

        🔒 VARSAYILAN KAPALI (`OLSR-c`; K-196, öğrenci onayı): referans
        dünyada bildirimlerin %99,7'si §14.3 ile ~0,5 s'de geri alınıyor, ama
        o arada §8.5 komşu kaybı 2-atlama kayıtlarını silip geçide rotayı
        boşaltıyor (K-193); birincil hücrede de §13'süz sürüm 4/4 tohumda
        ort. +0,052 iyi (K-200). `s13=True` eski `OLSR-b`yi birebir üretir.
        """
        if not self._s13:
            return ()
        simdi = float(gozlem.saat_s)
        b = self._bag.get(hedef) if hedef is not None else None
        if b is None:
            return ()
        # (2) *"L_LOST_LINK_time and L_time are set to current time +
        # NEIGHB_HOLD_TIME"*.
        sinir = simdi + NEIGHB_HOLD_TIME_S
        b.bitis = sinir
        h = self._hist.get(hedef)
        if h is not None:
            h.kayip_bitis = sinir
        self._kirli = True
        self._sayac["bag_katmani_kopma"] += 1
        beyanlar, ek = self._guncelle(simdi)
        return beyanlar + ek

    # ==================================================================
    # KANCA · teşhis
    # ==================================================================
    def kimlik_parametreleri(self) -> dict:
        """Koşu kimliğine giren seçim (K-171 kancası): §13 açık mı (K-196)."""
        return {"s13": self._s13}

    def teshis(self, dugum: int) -> dict:
        """🔴 Yalnız sonuç satırına; karara GİRMEZ."""
        # 🔒 Teşhis saat almaz; protokolün SON HESAPLADIĞI simetrik küme
        # raporlanır — kararların dayandığı küme tam olarak odur.
        return {**self._sayac,
                "komsu_simetrik": len(self._sym_onceki),
                "komsu_bekleyen": sum(1 for h in self._hist.values()
                                      if h.bekleyen),
                "iki_atlama": len(self._iki),
                "mpr": len(self._mpr),
                "mpr_secici": len(self._secici),
                "topoloji": len(self._topoloji),
                "rota": len(self._rota)}
