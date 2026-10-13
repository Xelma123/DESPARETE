"""
DESPARETE · edinim ve onarım denetçisi — saf, zamanı dışarıdan alan makine.

Kaynak: `arsiv/DESPARETE_TASARIM_PAKETI_v0.1_2026-09-22/` — `22` §6 (makine) ·
`23` §5.1 (algoritma) · `21` §2.3 (sayılar) · `18` §5–§6 (mesajlar).
Kararlar: `v2/04` K-150 · K-152 · K-156.

🔒 ÜÇ DURUM, HEDEF BAŞINA — `22` §6
===================================
    QUIESCENT  → sessiz
    SOLICITING → tek atlamalı FIELD_SOLICIT: en çok `N_solicit` (2) deneme,
                 her birine `T_solicit_reply` (0,4 s) yanıt, arada en az
                 `T_solicit_backoff` (0,2 s) — toplam en çok 1,0 s
    REQUESTING → DFSN_REQUEST oturumu: en çok `N_req` (2) dalga, her dalga
                 YENİ Request-ID, dalgalar arası en az `T_req_retry` (1 s),
                 oturum en çok `T_req_session` (4 s)

Aynı hedef için ikinci başlatma BİRLEŞİR (`23` §5.1 *"coalesce"*). Alan
iletilebilir olunca oturum iptal edilir. Solicit'ler bittiğinde alana hâlâ
ihtiyaç yoksa (koruma solicit'i: ardıl hâlâ geçerli) istek AÇILMAZ.

🔒 NEDEN ÇAĞIRANA SORULUR — ajan seçimi (K-156)
===============================================
DFSN_REQUEST'in nedeni (edinim · uygulanabilirlik açlığı · tazelik
belirsizliği) her dalgada, dalga anındaki alan durumundan belirlenir;
denetçi yalnız "dalga zamanı" der. `23` §5.1 nedeni oturumun başında
sabitler — ama onarımın ilk anında komşuların yeni ilanları henüz gelmemiş
olabilir; açlık ancak birkaç yüz milisaniye sonra görünür ve hedef yalnız
açlık nedeniyle yeni tur üretir (`23` §5.4). Dalga anında sormak, aynı
kuralı daha güncel bilgiyle uygular.

🔒 BÖLÜM SONU — yeniden edinim kuralının zemini (K-152 §2)
==========================================================
Bir oturum bittiğinde (başarı ya da süre) bitiş anı saklanır; düğümün kendi
ürettiği veri, alan ulaşılamazken ya da hiç yokken, son bölümün bitişinden
en az `T_repair_max` (6 s) sonra yeni bir edinim başlatabilir.
"""

from __future__ import annotations

from dataclasses import dataclass

from protokoller.desparete_bicim import (
    N_REQ, N_SOLICIT, T_REPAIR_MAX_S, T_REQ_RETRY_S, T_REQ_SESSION_S,
    T_SOLICIT_BACKOFF_S, T_SOLICIT_REPLY_S)

__all__ = ["QUIESCENT", "SOLICITING", "REQUESTING", "EdinimEylemi",
           "EdinimDenetcisi"]

QUIESCENT = "QUIESCENT"
SOLICITING = "SOLICITING"
REQUESTING = "REQUESTING"

_ALAN_32 = (1 << 32) - 1


@dataclass(frozen=True, slots=True)
class EdinimEylemi:
    """`tur` "solicit" · "istek" (yeni Request-ID `sira` ile) · "bitti"."""

    tur: str
    hedef: int
    sira: int = 0


@dataclass(slots=True)
class _Oturum:
    durum: str
    deneme: int = 0                 # solicit denemesi
    yanit_son: float | None = None  # bu solicit'in yanıt son tarihi
    sonraki: float | None = None    # sonraki solicit ya da istek dalgası
    dalga: int = 0
    oturum_son: float | None = None


class EdinimDenetcisi:
    """Bir düğümün bütün hedefleri için edinim makinesi."""

    __slots__ = ("_oturum", "_son_bitis", "_istek_sira", "sayac")

    def __init__(self) -> None:
        self._oturum: dict[int, _Oturum] = {}
        self._son_bitis: dict[int, float] = {}
        self._istek_sira = 0
        self.sayac: dict[str, int] = {
            "baslatilan": 0, "birlesen": 0, "solicit": 0, "istek_dalgasi": 0,
            "basarili": 0, "sure_doldu": 0, "gereksiz_kapandi": 0,
            "yeniden_edinim": 0, "yeniden_edinim_bekledi": 0,
        }

    # ------------------------------------------------------------ okuma
    def durum(self, h: int) -> str:
        o = self._oturum.get(h)
        return QUIESCENT if o is None else o.durum

    def son_tarih(self, h: int) -> float | None:
        o = self._oturum.get(h)
        if o is None:
            return None
        adaylar = [x for x in (o.yanit_son, o.sonraki, o.oturum_son)
                   if x is not None]
        return min(adaylar) if adaylar else None

    def yeniden_edinim_serbest(self, h: int, t: float) -> bool:
        """K-152 §2: son bölümün bitişinden en az `T_repair_max` geçti mi."""
        if h in self._oturum:
            return False
        son = self._son_bitis.get(h)
        return son is None or t - son >= T_REPAIR_MAX_S

    # ---------------------------------------------------------- geçişler
    def baslat(self, h: int, t: float) -> list[EdinimEylemi]:
        """`23` §5.1 `StartAcquisition` — sürüyorsa birleşir."""
        if h in self._oturum:
            self.sayac["birlesen"] += 1
            return []
        self._oturum[h] = _Oturum(SOLICITING, deneme=1,
                                  yanit_son=t + T_SOLICIT_REPLY_S)
        self.sayac["baslatilan"] += 1
        self.sayac["solicit"] += 1
        return [EdinimEylemi("solicit", h)]

    def yeniden_edinim(self, h: int, t: float) -> list[EdinimEylemi]:
        """Yerel veri ulaşılamaz / alansız hedefe — kural serbestse başlat."""
        if not self.yeniden_edinim_serbest(h, t):
            self.sayac["yeniden_edinim_bekledi"] += 1
            return []
        self.sayac["yeniden_edinim"] += 1
        return self.baslat(h, t)

    def basarili(self, h: int, t: float) -> None:
        """Alan iletilebilir oldu — `CancelAcquisitionOrRepair`."""
        if self._oturum.pop(h, None) is not None:
            self._son_bitis[h] = t
            self.sayac["basarili"] += 1

    def zaman(self, h: int, t: float, pay: float,
              gerekli: bool) -> list[EdinimEylemi]:
        """Dolmuş son tarihler. `gerekli`: alan hâlâ iletilebilir değil mi."""
        o = self._oturum.get(h)
        if o is None:
            return []
        dolmus = t + pay
        if o.durum == SOLICITING:
            if o.sonraki is not None and o.sonraki <= dolmus:
                o.deneme += 1
                o.sonraki = None
                o.yanit_son = t + T_SOLICIT_REPLY_S
                self.sayac["solicit"] += 1
                return [EdinimEylemi("solicit", h)]
            if o.yanit_son is not None and o.yanit_son <= dolmus:
                o.yanit_son = None
                if o.deneme < N_SOLICIT:
                    o.sonraki = t + T_SOLICIT_BACKOFF_S
                    return []
                if not gerekli:
                    return self._kapat(h, t, "gereksiz_kapandi")
                o.durum, o.dalga = REQUESTING, 1
                o.oturum_son = t + T_REQ_SESSION_S
                o.sonraki = t + T_REQ_RETRY_S
                return [self._dalga(h)]
            return []
        # REQUESTING
        if o.oturum_son is not None and o.oturum_son <= dolmus:
            return self._kapat(h, t, "sure_doldu") + [
                EdinimEylemi("bitti", h)]
        if o.sonraki is not None and o.sonraki <= dolmus:
            o.sonraki = None
            if gerekli and o.dalga < N_REQ:
                o.dalga += 1
                return [self._dalga(h)]
        return []

    def zaman_asimi_bitir(self, h: int, t: float) -> None:
        """`T_repair_max` doldu (`23` §5.1): oturum da biter."""
        if h in self._oturum:
            self._kapat(h, t, "sure_doldu")

    # ------------------------------------------------------------ içsel
    def _dalga(self, h: int) -> EdinimEylemi:
        self._istek_sira = (self._istek_sira + 1) & _ALAN_32
        self.sayac["istek_dalgasi"] += 1
        return EdinimEylemi("istek", h, self._istek_sira)

    def _kapat(self, h: int, t: float, neden: str) -> list:
        del self._oturum[h]
        self._son_bitis[h] = t
        self.sayac[neden] += 1
        return []
