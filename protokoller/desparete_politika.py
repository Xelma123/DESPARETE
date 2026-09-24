"""
DESPARETE · alan başına politika postürü — saf, zamanı dışarıdan alan durum
makinesi.

Kaynak: `protokol_kaynaklari/DESPARETE_TASARIM_PAKETI/` — `15` (model) ·
`22` §7 (geçişler) · `35` §5 (M0.1 yüklemleri) · `21` §2.5 (süreler).
Kararlar: `v2/04` K-150 §4 · K-158.

🔒 POSTÜR YÖNLENDİRMEYİ DEĞİŞTİRMEZ — `15` §1 · §7
==================================================
Ardıl seçimi, uygulanabilirlik ve tazelik kapıları postürden bağımsızdır;
risk maliyete bir kez girer (`C_risk`), postür ikinci bir ceza eklemez.
Postür yalnız gözlem yoğunluğunu ve (izinliyse) yedekliliği değiştirir.

🔒 GEÇİŞLER — `22` §7
=====================
    STEADY  → CAUTION : CautionEvidence 1,5 s kesintisiz
    CAUTION → PROTECT : ProtectEvidence ∧ ek güvenli ardıl 2,5 s kesintisiz
                        ∧ trafiğin koruma izni
    CAUTION → STEADY  : RecoveryEvidence 4,0 s kesintisiz
    PROTECT → CAUTION : ek güvenli ardıl yok (HEMEN) · ya da en az 2,0 s
                        PROTECT'te kaldıktan sonra RecoveryEvidence 4,0 s
    alan iletilebilir değil → kanıt sıfırlanır, postürün etkisi yok
    alan yeniden iletilebilir → STEADY (eski PROTECT dirilmez)

Kanıt, seçili ardılın son epoch ölçümünden okunur (`35` §6: epoch başına
bir değerlendirme). *"Kesintisiz"*: yüklemin art arda her epochta doğru
olması; başlangıç, doğru olduğu İLK epochtur.

🔒 BELGENİN AÇIK BIRAKTIĞI, BURADA SEÇİLEN — ajan (K-158)
========================================================
  · Ardıl değişince kanıt SIFIRLANIR: eski ardılın kanıtı yenisi hakkında
    değildir. Postürün kendisi korunur (`15` §3: ardıl kaybı kendiliğinden
    postür değiştirmez).
  · Her postür geçişinde kanıt yeniden başlar (geçiş epochunda doğru olan
    yüklem o epochtan) — bekleme süreleri postürün İÇİNDE ölçülür. Aksi
    hâlde 4 s'lik toparlanma PROTECT → CAUTION'dan hemen sonra CAUTION →
    STEADY'yi de açardı: `15` §5'in yasakladığı doğrudan dönüş, yarım saniye
    arayla.
  · Doğrulama oturumu yalnız STEADY → CAUTION girişinde açılır (K-150 §4);
    PROTECT'ten CAUTION'a inişte gözlem zaten yüksektir.
  · Koruma izni: ilk gerçeklemede yedeklilik YOK (K-150 §4), dolayısıyla
    korumaya izinli trafik de yok → PROTECT'e girilmez. Koşulların izin
    dışında sağlandığı her kanıt bölümü `protect_izinsiz` diye BİR kez
    sayılır — yedekliliğin ileride ne sıklıkla devreye gireceğinin ölçüsü.
"""

from __future__ import annotations

from dataclasses import dataclass

from protokoller.desparete_bicim import (
    T_CAUTION_EVIDENCE_S, T_PROTECT_EVIDENCE_S, T_PROTECT_MIN_S,
    T_RECOVERY_EVIDENCE_S)
from protokoller.desparete_komsu import ZAMAN_PAYI_S
from protokoller.desparete_metrik import (H_UYARI, Olcum, koruma_kaniti,
                                          toparlanma_kaniti, uyari_kaniti)

__all__ = ["STEADY", "CAUTION", "PROTECT", "Postur", "PolitikaTablosu"]

STEADY = "STEADY"
CAUTION = "CAUTION"
PROTECT = "PROTECT"


@dataclass(slots=True)
class Postur:
    durum: str = STEADY
    ardil: int | None = None
    uyari_bas: float | None = None        # CautionEvidence başlangıcı
    koruma_bas: float | None = None       # ProtectEvidence ∧ ek ardıl
    toparlanma_bas: float | None = None   # RecoveryEvidence
    koruma_giris: float | None = None
    izinsiz_sayildi: bool = False

    def kaniti_sifirla(self) -> None:
        self.uyari_bas = self.koruma_bas = self.toparlanma_bas = None
        self.izinsiz_sayildi = False


def _surer(bas: float | None, kosul: bool, t: float) -> float | None:
    if not kosul:
        return None
    return t if bas is None else bas


def _doldu(bas: float | None, t: float, sure: float) -> bool:
    return bas is not None and t - bas >= sure - ZAMAN_PAYI_S


class PolitikaTablosu:
    """Bir düğümün bütün alanlarının postürü `Π_i[K]`."""

    __slots__ = ("koruma_izni", "posturler", "sayac")

    def __init__(self, koruma_izni: bool = False) -> None:
        self.koruma_izni = koruma_izni
        self.posturler: dict[int, Postur] = {}
        self.sayac: dict[str, int] = {
            "caution_girdi": 0, "caution_hazard": 0, "caution_belirsizlik": 0,
            "protect_girdi": 0, "protect_izinsiz": 0,
            "steady_dondu": 0, "protect_cikti": 0, "protect_zorunlu_cikis": 0,
            "ardil_degisti_kanit": 0, "etkisiz_kaldi": 0,
        }

    def durum(self, hedef: int) -> str:
        p = self.posturler.get(hedef)
        return STEADY if p is None else p.durum

    def degerlendir(self, hedef: int, t: float, ardil: int, o: Olcum,
                    ek_ardil: bool) -> bool:
        """İletilebilir alanın epoch değerlendirmesi. CAUTION'a GİRİLDİYSE
        `True` döner — çağıran ardıla doğrulama oturumu açar (K-150 §4)."""
        p = self.posturler.setdefault(hedef, Postur())
        if p.ardil != ardil:
            if p.ardil is not None:
                self.sayac["ardil_degisti_kanit"] += 1
            p.ardil = ardil
            p.kaniti_sifirla()
        kanit = (uyari_kaniti(o), koruma_kaniti(o) and ek_ardil,
                 toparlanma_kaniti(o))
        self._kanit(p, t, *kanit)
        eski = p.durum
        self._gecis(p, t, ek_ardil)
        if p.durum != eski:
            p.kaniti_sifirla()
            self._kanit(p, t, *kanit)       # yeni postürde bu epochtan başlar
        girdi = eski == STEADY and p.durum == CAUTION
        if girdi:
            # 🔎 K-150 §3 madde 4: boşta bağda U yapısal olarak 128 — girişin
            # sebebi ayrı sayılır (bozunma mı, yalnız belirsizlik mi).
            self.sayac["caution_hazard" if o.h >= H_UYARI
                       else "caution_belirsizlik"] += 1
        return girdi

    def _kanit(self, p: Postur, t: float, uyari: bool, koruma: bool,
               toparlanma: bool) -> None:
        p.uyari_bas = _surer(p.uyari_bas, uyari, t)
        p.koruma_bas = _surer(p.koruma_bas, koruma, t)
        p.toparlanma_bas = _surer(p.toparlanma_bas, toparlanma, t)
        if p.koruma_bas is None:
            p.izinsiz_sayildi = False

    def _gecis(self, p: Postur, t: float, ek_ardil: bool) -> None:
        """Epoch başına en çok BİR geçiş."""
        if p.durum == STEADY:
            if _doldu(p.uyari_bas, t, T_CAUTION_EVIDENCE_S):
                self._gec(p, CAUTION, "caution_girdi")
        elif p.durum == CAUTION:
            if _doldu(p.koruma_bas, t, T_PROTECT_EVIDENCE_S):
                if self.koruma_izni:
                    self._gec(p, PROTECT, "protect_girdi")
                    p.koruma_giris = t
                elif not p.izinsiz_sayildi:
                    self.sayac["protect_izinsiz"] += 1
                    p.izinsiz_sayildi = True
            elif _doldu(p.toparlanma_bas, t, T_RECOVERY_EVIDENCE_S):
                self._gec(p, STEADY, "steady_dondu")
        elif not ek_ardil:                          # PROTECT, güvenlik kaybı
            self._gec(p, CAUTION, "protect_zorunlu_cikis")
        elif (t - p.koruma_giris >= T_PROTECT_MIN_S - ZAMAN_PAYI_S
              and _doldu(p.toparlanma_bas, t, T_RECOVERY_EVIDENCE_S)):
            self._gec(p, CAUTION, "protect_cikti")

    def etkisiz(self, hedef: int) -> None:
        """Alan REPAIRING ya da UNREACHABLE oldu: kanıt sıfırlanır."""
        p = self.posturler.get(hedef)
        if p is not None:
            p.kaniti_sifirla()
            self.sayac["etkisiz_kaldi"] += 1

    def yeniden(self, hedef: int) -> None:
        """Alan yeniden iletilebilir: STEADY'den, yeni kanıtla."""
        self.posturler[hedef] = Postur()

    def _gec(self, p: Postur, yeni: str, ad: str) -> None:
        p.durum = yeni
        self.sayac[ad] += 1
