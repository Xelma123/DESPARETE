"""
DESPARETE · alan, uygulanabilirlik ve ardıl — saf, zamanı dışarıdan alan tablo.

Kaynak: `arsiv/DESPARETE_TASARIM_PAKETI_v0.1_2026-09-22/` — `13` (potansiyel ve
döngüsüzlük) · `14` (tazelik) · `22` §5 (alan makinesi) · `23` §4 (algoritma)
· `21` §2.2 (sayılar). Kararlar: `v2/04` K-150 · K-152 · K-155.

🔒 DÖNGÜSÜZLÜK — `36` §3.3
==========================
Her alan `K` için düğüm, aynı DFSN içinde ARTMAYAN bir uygulanabilirlik
mesafesi `FD = (S_FD, M_FD)` tutar. Komşu `j`nin ilanı ancak

    S_j daha yeni   ya da   S_j = S_FD ve P_j < M_FD

ise uygulanabilirdir; eşit potansiyel uygulanabilir DEĞİLDİR. Seçilen
ardılın her kenarında `FD_j ≤ P_j < FD_i` olur ve kesin azalış veri döngüsünü
yapısal olarak engeller. TTL / Hop Limit kanıt değildir. Bu modülün
yapabileceği tek yanlış, bu koşulu gevşetmektir — testler onu her olaydan
sonra denetler.

🔒 ALANIN ÜÇ DURUMU — `22` §5.2
===============================
    FORWARDABLE  güvenli ardıl var, veri iletilir
    REPAIRING    ardıl yok; `T_repair_max` (6 s) boyunca yeni ilan beklenir
    UNREACHABLE  onarım süresi doldu; aynı DFSN'de uygulanabilir bir ilan ya
                 da daha yeni bir DFSN alanı geri açar (`23` §4.3 · K-152 §2)

Edinim ve onarımın MESAJLARI (FIELD_SOLICIT, DFSN_REQUEST) ve onarım tamponu
3.5'tedir; burada REPAIRING yalnız bekler.

🔒 İLAN — `23` §4.1 · `20` §6
=============================
  · Yalnız ACTIVE komşunun ilanı aday olabilir; olmayanınki yok sayılır.
  · Aynı `(komşu, K, DFSN)` bağlamında yalnız DAHA YENİ ADS kabul edilir —
    eşit ya da eski ADS ömrü uzatamaz, withdrawal'ı geri alamaz.
  · Withdrawal sonlu aday değildir; sıra bilgisi `T_withdraw_cache` tutulur.
  · Alınan ömür `min(Lifetime × 100 ms, L_adv_max)` ile sınırlanır.

🔒 TETİK İLANI — `21` §2.2 · `20` §6.1
======================================
Ardıl değişimi ya da potansiyel artışı → en geç `T_urgent` (0,1 s); diğer
değişim → en geç `T_coalesce` (0,2 s); alan başına saniyede en çok beş tetik.
İçerik GÖNDERİM anında okunur, yani bekleyen değişimler tek ilanda birleşir
(ADS son durumu temsil eder). Withdrawal bir arıza bölümünde BİR kez.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from protokoller.desparete_bicim import (
    DURUM_REACHABLE, DURUM_WITHDRAWAL, G_ADV_REFRESH_S, L_ADV_MAX_S,
    OMUR_KUANTA_S, T_ADV_CACHE_S, T_COALESCE_S, T_REPAIR_MAX_S, T_URGENT_S,
    T_WITHDRAW_CACHE_S)
from protokoller.desparete_metrik import SONSUZ, sat_add

__all__ = ["FORWARDABLE", "REPAIRING", "UNREACHABLE", "ESKI", "ESIT",
           "YENI", "BELIRSIZ", "seri_karsilastir", "Ilan", "Alan",
           "AlanTablosu", "IlanIstegi"]

FORWARDABLE = "FORWARDABLE"
REPAIRING = "REPAIRING"
UNREACHABLE = "UNREACHABLE"

ESKI, ESIT, YENI, BELIRSIZ = "OLDER", "EQUAL", "NEWER", "AMBIGUOUS"
_YARIM = 1 << 31
_MOD = 1 << 32


def seri_karsilastir(a: int, b: int) -> str:
    """RFC 1982, 32 bit: `a`, `b`ye göre … (`19` §12.2)."""
    if a == b:
        return ESIT
    fark = (a - b) % _MOD
    if fark == _YARIM:
        return BELIRSIZ
    return YENI if fark < _YARIM else ESKI


@dataclass(slots=True)
class Ilan:
    """Bir komşunun bir alan için son ilanı (`A_j[K]`)."""

    dfsn: int
    ads: int
    durum: int
    potansiyel: int
    bitis: float            # sonlu ilanın aday olabildiği son an
    onbellek_son: float     # sıra bilgisinin tutulduğu son an


@dataclass(frozen=True, slots=True)
class IlanIstegi:
    """"`hedef` alanı için ilan gönder" — içerik gönderim anında okunur."""

    hedef: int
    en_erken_s: float       # bu andan önce değil (hız sınırı)
    pencere_s: float        # en_erken + [0, pencere] içinde


@dataclass(slots=True)
class Alan:
    """`F_i[K]` — bir hedefin alanı bu düğümde."""

    hedef: int
    kendi: bool = False
    dfsn: int | None = None
    fd: tuple[int, int] | None = None
    ardil: int | None = None
    potansiyel: int = SONSUZ
    durum: str = REPAIRING
    ilanlar: dict[int, Ilan] = field(default_factory=dict)
    onarim_son: float | None = None
    ads: int = 0
    # Komşulara en son SÖYLENEN: `(durum, potansiyel)` — tetiğin ölçütü.
    soylenen: tuple[int, int] | None = None
    tetik_bekliyor: bool = False
    tetik_acil: bool = False
    son_tetik_s: float = float("-inf")
    # Koruma solicit'i (`20` §6.2) hangi ilan bitişi için ateşlendi — bir kez.
    koruma_bitis: float | None = None


class AlanTablosu:
    """Bir düğümün bütün alanları.

    `aktif_mi(j)` komşunun ACTIVE olup olmadığını, `maliyet(j)` M0.1'in
    `C(i,j)`sini (tanımsızsa `None`) verir; ikisi de komşu tablosundan gelir.
    """

    __slots__ = ("_aktif_mi", "_maliyet", "alanlar", "istekler", "olaylar",
                 "sayac")

    def __init__(self, aktif_mi, maliyet) -> None:
        self._aktif_mi = aktif_mi
        self._maliyet = maliyet
        self.alanlar: dict[int, Alan] = {}
        self.istekler: list[IlanIstegi] = []
        # `(olay, hedef)`: "onarim" · "iletilebilir" · "ulasilamaz" · "koruma"
        # — edinim denetçisini ve onarım tamponunu sürer (3.5, K-156).
        self.olaylar: list[tuple[str, int]] = []
        self.sayac: dict[str, int] = {
            "ilan_kabul": 0, "ilan_eski": 0, "ilan_aktif_disi": 0,
            "ilan_gecersiz": 0,
            "ardil_degisti": 0, "onarima_girdi": 0, "ulasilamaz": 0,
            "tetik_ilan": 0, "withdrawal": 0, "fd_yeni_tur": 0,
            "tur_artirildi": 0, "koruma": 0,
        }

    # ------------------------------------------------------------ okuma
    def ardil(self, hedef: int) -> int | None:
        a = self.alanlar.get(hedef)
        return a.ardil if a is not None and a.durum == FORWARDABLE else None

    def durum(self, hedef: int) -> str | None:
        a = self.alanlar.get(hedef)
        return None if a is None else a.durum

    def ardillar(self) -> set[int]:
        return {a.ardil for a in self.alanlar.values()
                if a.durum == FORWARDABLE and a.ardil is not None}

    # ---------------------------------------------------------- kurulum
    def kendi_alani(self, hedef: int, dfsn: int) -> Alan:
        """Hedef kendi alanının tek üreticisidir: `P = 0`, `FD = (DFSN, 0)`."""
        a = self.alanlar[hedef] = Alan(hedef=hedef, kendi=True, dfsn=dfsn,
                                       fd=(dfsn, 0), potansiyel=0,
                                       durum=FORWARDABLE)
        return a

    def tur_artir(self, hedef: int, t: float) -> None:
        """`23` §5.4 — hedef kendi alanının DFSN'sini BİR artırır ve ilan eder."""
        a = self.alanlar[hedef]
        a.dfsn = (a.dfsn + 1) % _MOD
        a.fd = (a.dfsn, 0)
        self.sayac["tur_artirildi"] += 1
        self._tetik(a, t, acil=True)

    def kaynak_ilani(self, hedef: int, t: float) -> None:
        """`SendOriginFieldUpdate` — hedefin güncel ilanı, tetikle (acil)."""
        self._tetik(self.alanlar[hedef], t, acil=True)

    def ulasilamaz_yap(self, hedef: int) -> None:
        """İstek oturumu bitti ve güvenli ardıl yok (`23` §5.1)."""
        a = self.alanlar.get(hedef)
        if a is not None and a.durum == REPAIRING:
            self._ulasilamaz(a)

    def aclik_mi(self, hedef: int, t: float) -> bool:
        """Uygulanabilirlik açlığı: aynı turda geçerli, sonlu, ACTIVE bir
        ilan VAR ama hiçbiri uygulanabilir değil (`23` §5.4 FEASIBLE_STARVATION)."""
        a = self.alanlar.get(hedef)
        if a is None or a.kendi or a.dfsn is None or a.fd is None:
            return False
        return any(self._aktif_mi(j) and i.durum == DURUM_REACHABLE
                   and i.bitis > t and i.dfsn == a.dfsn
                   and i.potansiyel >= a.fd[1]
                   for j, i in a.ilanlar.items())

    def yanit_icerigi(self, hedef: int) -> tuple | None:
        """FIELD_SOLICIT / DFSN_REQUEST'e tek alıcılı yanıt — güncel durum,
        yeni ADS. Bekleyen tetik ilanını ve söylenen durumu DEĞİŞTİRMEZ: yanıtı
        yalnız bir komşu duyar."""
        a = self.alanlar.get(hedef)
        if a is None or a.durum != FORWARDABLE or a.dfsn is None:
            return None
        a.ads = (a.ads + 1) % _MOD
        return (a.dfsn, a.ads, DURUM_REACHABLE, a.potansiyel)

    # ------------------------------------------------------------- ilan
    def ilan_al(self, j: int, hedef: int, dfsn: int, ads: int, durum: int,
                potansiyel: int, omur: int, t: float) -> None:
        """`23` §4.1 `ReceiveFieldUpdate` — biçim ve kimlik denetimi çağıranda."""
        # `19` §6: REACHABLE sonlu ve ömürlü · WITHDRAWAL ∞ ve ömürsüz ·
        # P = 0 yalnız hedefin kendi ilanında. Aksi yasak birleşim → bırak.
        if (durum not in (DURUM_REACHABLE, DURUM_WITHDRAWAL)
                or (durum == DURUM_REACHABLE
                    and (potansiyel >= SONSUZ or omur == 0))
                or (durum == DURUM_WITHDRAWAL
                    and (potansiyel != SONSUZ or omur != 0))
                or (potansiyel == 0 and j != hedef)):
            self.sayac["ilan_gecersiz"] += 1
            return
        if not self._aktif_mi(j):
            self.sayac["ilan_aktif_disi"] += 1     # yalnız tanısal
            return
        a = self.alanlar.get(hedef)
        if a is not None and a.kendi:
            return                                 # kendi alanım
        if a is None:
            a = self.alanlar[hedef] = Alan(hedef=hedef)
        eski = a.ilanlar.get(j)
        if eski is not None and eski.onbellek_son > t:
            kiyas = seri_karsilastir(dfsn, eski.dfsn)
            if kiyas in (ESKI, BELIRSIZ) or (
                    kiyas == ESIT
                    and seri_karsilastir(ads, eski.ads) != YENI):
                self.sayac["ilan_eski"] += 1
                return
        if durum == DURUM_WITHDRAWAL:
            a.ilanlar[j] = Ilan(dfsn, ads, durum, SONSUZ, bitis=t,
                                onbellek_son=t + T_WITHDRAW_CACHE_S)
        else:
            bitis = t + min(omur * OMUR_KUANTA_S, L_ADV_MAX_S)
            a.ilanlar[j] = Ilan(dfsn, ads, durum, potansiyel, bitis=bitis,
                                onbellek_son=bitis + T_ADV_CACHE_S)
        self.sayac["ilan_kabul"] += 1
        self.yeniden_hesapla(hedef, t)

    # -------------------------------------------------- yeniden hesaplama
    def yeniden_hesapla(self, hedef: int, t: float) -> None:
        """`23` §4.3 `RecomputeField`."""
        a = self.alanlar.get(hedef)
        if a is None or a.kendi:
            return
        for j in [j for j, i in a.ilanlar.items() if i.onbellek_son <= t]:
            del a.ilanlar[j]
        s_yeni = self._en_yeni_dfsn(a)
        if s_yeni is BELIRSIZ:
            return self._kapat(a, t)               # tazelik belirsiz: fail-closed
        if s_yeni is not None and (
                a.dfsn is None or seri_karsilastir(s_yeni, a.dfsn) == YENI):
            a.ardil, a.potansiyel = None, SONSUZ
            a.dfsn, a.fd = s_yeni, None
            self.sayac["fd_yeni_tur"] += 1
        if a.dfsn is None:
            return
        adaylar = self._guvenli_adaylar(a, t)
        if adaylar:
            maliyet, j = min(adaylar)              # eşitlikte küçük kimlik
            eski_ardil, eski_p = a.ardil, a.potansiyel
            a.ardil, a.potansiyel = j, maliyet
            if a.fd is None or maliyet < a.fd[1]:
                a.fd = (a.dfsn, maliyet)
            if a.durum != FORWARDABLE:
                self.olaylar.append(("iletilebilir", a.hedef))
            a.durum, a.onarim_son = FORWARDABLE, None
            if eski_ardil != j:
                self.sayac["ardil_degisti"] += 1
            if eski_ardil != j or maliyet != eski_p:
                self._tetik(a, t, acil=(eski_ardil != j or maliyet > eski_p))
            return
        if a.durum == FORWARDABLE:
            self._onarima_gir(a, t)
        elif a.durum == REPAIRING and a.onarim_son is None:
            a.onarim_son = t + T_REPAIR_MAX_S      # ilk kez görülen alan
            self.olaylar.append(("onarim", a.hedef))

    def _guvenli_adaylar(self, a: Alan, t: float) -> list[tuple[int, int]]:
        """`(maliyet, j)` — ACTIVE, güncel turdan, ömrü süren, uygulanabilir."""
        adaylar = []
        for j, i in a.ilanlar.items():
            c = self._maliyet(j)
            if not (self._aktif_mi(j) and i.durum == DURUM_REACHABLE
                    and i.bitis > t and i.dfsn == a.dfsn
                    and i.potansiyel < SONSUZ and c is not None):
                continue
            if a.fd is not None and not i.potansiyel < a.fd[1]:
                continue                           # uygulanabilir DEĞİL
            maliyet = sat_add(i.potansiyel, c)
            if maliyet < SONSUZ:
                adaylar.append((maliyet, j))
        return adaylar

    def ek_ardil_var(self, hedef: int, t: float) -> bool:
        """Seçili ardıldan BAŞKA bir güvenli ardıl var mı (`22` §7 · §8.2)."""
        a = self.alanlar.get(hedef)
        if a is None or a.durum != FORWARDABLE or a.dfsn is None:
            return False
        return any(j != a.ardil for _, j in self._guvenli_adaylar(a, t))

    def hepsini_hesapla(self, t: float) -> None:
        for hedef in sorted(self.alanlar):
            self.yeniden_hesapla(hedef, t)

    def komsu_degisti(self, j: int, t: float, silindi: bool) -> None:
        """Komşu ACTIVE oldu ya da olmaktan çıktı; EXPIRED ise ilanları silinir
        (`22` §4.2 · `23` §3.2 `InvalidateCandidatesFrom`)."""
        for hedef in sorted(self.alanlar):
            a = self.alanlar[hedef]
            if j not in a.ilanlar:
                continue
            if silindi:
                del a.ilanlar[j]
            self.yeniden_hesapla(hedef, t)

    # ------------------------------------------------------ zamanlayıcı
    def son_tarih(self, hedef: int) -> float | None:
        """Ardılın ilanının koruma anı ve bitişi ya da onarımın sonu."""
        a = self.alanlar.get(hedef)
        if a is None or a.kendi:
            return None
        adaylar = []
        if a.durum == FORWARDABLE and a.ardil in a.ilanlar:
            bitis = a.ilanlar[a.ardil].bitis
            adaylar.append(bitis)
            if a.koruma_bitis != bitis:
                adaylar.append(bitis - G_ADV_REFRESH_S)
        if a.durum == REPAIRING and a.onarim_son is not None:
            adaylar.append(a.onarim_son)
        return min(adaylar) if adaylar else None

    def zaman(self, hedef: int, t: float, pay: float) -> None:
        a = self.alanlar.get(hedef)
        if a is None or a.kendi:
            return
        if (a.durum == REPAIRING and a.onarim_son is not None
                and a.onarim_son <= t + pay):
            self._ulasilamaz(a)
            return
        self.yeniden_hesapla(hedef, t)
        # `20` §6.2: seçili ilan bitmeden `G_adv_refresh` önce yeni ilan
        # gelmediyse FIELD_SOLICIT — ilan başına BİR kez.
        if a.durum == FORWARDABLE and a.ardil in a.ilanlar:
            bitis = a.ilanlar[a.ardil].bitis
            if a.koruma_bitis != bitis and bitis - G_ADV_REFRESH_S <= t + pay:
                a.koruma_bitis = bitis
                self.sayac["koruma"] += 1
                self.olaylar.append(("koruma", a.hedef))

    # ---------------------------------------------------------- gönderim
    def ilan_icerigi(self, hedef: int, tetik: bool) -> tuple | None:
        """Gönderilecek ilan `(dfsn, ads, durum, potansiyel)` — ya da yok.

        Periyodik tazeleme (`tetik=False`) yalnız FORWARDABLE alan içindir;
        withdrawal bir arıza bölümünde yalnız tetikle ve BİR kez gider.
        """
        a = self.alanlar.get(hedef)
        if a is None or a.dfsn is None:
            return None
        if tetik:
            if not a.tetik_bekliyor:
                return None
            a.tetik_bekliyor = a.tetik_acil = False
        if a.durum == FORWARDABLE:
            icerik = (DURUM_REACHABLE, a.potansiyel)
        elif tetik and a.soylenen is not None \
                and a.soylenen[0] == DURUM_REACHABLE:
            icerik = (DURUM_WITHDRAWAL, SONSUZ)
            self.sayac["withdrawal"] += 1
        else:
            return None
        a.ads = (a.ads + 1) % _MOD
        a.soylenen = icerik
        if tetik:
            self.sayac["tetik_ilan"] += 1
        else:
            a.tetik_bekliyor = a.tetik_acil = False   # güncel durum söylendi
        return (a.dfsn, a.ads) + icerik

    def tetik_gonderildi(self, hedef: int, t: float) -> None:
        a = self.alanlar.get(hedef)
        if a is not None:
            a.son_tetik_s = t

    # ------------------------------------------------------------ içsel
    def _en_yeni_dfsn(self, a: Alan):
        en = None
        for j, i in a.ilanlar.items():
            if not self._aktif_mi(j):
                continue
            if en is None:
                en = i.dfsn
                continue
            kiyas = seri_karsilastir(i.dfsn, en)
            if kiyas == BELIRSIZ:
                return BELIRSIZ
            if kiyas == YENI:
                en = i.dfsn
        if en is not None and a.dfsn is not None \
                and seri_karsilastir(en, a.dfsn) == BELIRSIZ:
            return BELIRSIZ
        return en

    def _onarima_gir(self, a: Alan, t: float) -> None:
        a.ardil, a.potansiyel = None, SONSUZ
        a.durum, a.onarim_son = REPAIRING, t + T_REPAIR_MAX_S
        self.sayac["onarima_girdi"] += 1
        self.olaylar.append(("onarim", a.hedef))
        self._tetik(a, t, acil=True)               # withdrawal

    def _ulasilamaz(self, a: Alan) -> None:
        a.durum, a.onarim_son = UNREACHABLE, None
        self.sayac["ulasilamaz"] += 1
        self.olaylar.append(("ulasilamaz", a.hedef))

    def _kapat(self, a: Alan, t: float) -> None:
        if a.durum == FORWARDABLE:
            self._onarima_gir(a, t)

    def _tetik(self, a: Alan, t: float, acil: bool) -> None:
        if a.tetik_bekliyor and (a.tetik_acil or not acil):
            return                                 # birleşir
        a.tetik_bekliyor = True
        a.tetik_acil = a.tetik_acil or acil
        en_erken = max(t, a.son_tetik_s + T_COALESCE_S)
        self.istekler.append(IlanIstegi(
            a.hedef, en_erken, T_URGENT_S if acil else T_COALESCE_S))
