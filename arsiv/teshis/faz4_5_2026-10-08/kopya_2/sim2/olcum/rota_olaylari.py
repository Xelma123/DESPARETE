"""
Rota olayları — üç kopma sayacı, Δ ve COR.

🔴 RİSK 3: `Beyan` KANALI KÂHİN SIZINTISININ YENİ KAPISI
========================================================
Tehlike şu: hiç beyan etmeyen bir protokolün `kopma_algilanan` sayacı **0**
çıkar ve tabloda *"hiç kopma yaşamadı"* gibi görünür. Oysa yalnızca
susmuştur — ve susmak, ölçülen her şeyde onu haksız yere iyi gösterir.

🔒 ÜÇ ÖLÇÜM BUNU KAPATIR ve üçü de ön-kayıtta ilan edilir:

  a) **`algilama_duyarliligi = kopma_algilanan / kopma_fiziksel`** her koşuda
     raporlanır. Payda KÂHİN sayaçtır: gerçekte kaç bağ koptuğunu simülatör
     bilir. Oran 0 ise kol `beyan_etmiyor=True` diye ETİKETLENİR ve Δ `None`
     döner — 0 değil.
  b) 30 tohumda beyan sayısı ↔ PDR korelasyonu ölçülür (`analiz/`).
  c) `olcum/` dışında hiçbir modül `Beyan`ı içe aktaramaz (AST testi).

🔒 Δ = T_r − T_d
================
Kopmanın BEYAN edildiği an ile rotanın yeniden kurulduğu anın farkı. Ölçülen
şey protokolün *kendi gördüğü* kesintidir; fiziksel kopmadan başlatılsaydı
protokolün fark etmediği süre de ona yazılırdı ve algılamayan protokol
haksız yere iyi görünürdü.

🔴 Δ HİÇ BEYAN EDİLMEZSE `None`, SIFIR DEĞİL. *"Ölçüm yok"* ile *"gecikme
sıfır"* aynı şey değildir; sıfır döndürmek ölçülmemiş bir hücreyi ortalamaya
sokmak olurdu.

🔒 COR = rota_kurtarildi / rota_etkilendi
========================================
İletişim kurtarma oranı. Payda da protokolün beyanıdır: hangi rotaların
etkilendiğini o bildirir. Bu yüzden COR tek başına okunmaz —
`algilama_duyarliligi` ile birlikte okunur.

🔴 PAY VE PAYDA AYNI BİRİMİ SAYAR — KOPMA DÖNGÜSÜ (19 Eylül 2026, `04` K-141)
Önceden pay kapanan döngüleri (`len(_delta)`), payda FARKLI BAĞLARI
sayıyordu. Aynı bağ beş kez kopup beş kez kurtarılırsa COR = 5/1 = 5 —
"kurtarılan / etkilenen" diye tanımlı bir oran 1'i aşıyordu. AODV'nin beyan
anahtarları düzeltilip Δ gerçekten kapanmaya başlayınca ölçüldü:
`bagimsiz-yok` **3,26**. Payda artık AÇILAN döngü sayısıdır ve bir değişmez
bunu bağlar: `kapanan + kapanmamış == açılan`.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from sim2.cekirdek.degismezler import dogrula
from sim2.gozlem.karar import Beyan
from sim2.olcum.kahin import Kahin, kahin

__all__ = ["RotaOlayi", "RotaDefteri"]


@dataclass(frozen=True, slots=True)
class RotaOlayi:
    """Beyan edilmiş bir rota olayı."""

    tip: str
    dugum: int
    komsu: int | None
    t_s: float


@dataclass
class RotaDefteri:
    """Kopma/kurtarma olayları ve onlardan türeyen Δ, COR, duyarlılık."""

    _olaylar: list[RotaOlayi] = field(default_factory=list)
    # Açılan kopma döngüsü — COR'un paydası (K-141).
    _acilan: int = 0
    # 🔴 KÂHİN: gerçekte kaç bağ koptu. Protokol bunu göremez.
    _fiziksel_kopma: int = 0
    _bekleyen: dict[tuple[int, int | None], float] = field(default_factory=dict)
    _delta: list[float] = field(default_factory=list)

    # ------------------------------------------------------------ kayıt
    def fiziksel_kopma(self, adet: int = 1) -> None:
        """🔴 Simülatörün gördüğü gerçek kopma — `kanal/yayilim`ın yavaş
        SINR'i eşiğin altına indiğinde. Protokolün beyanından BAĞIMSIZ."""
        dogrula(adet >= 0, "kopma sayısı negatif olamaz")
        self._fiziksel_kopma += adet

    def beyan_isle(self, dugum: int, beyan: Beyan, t_s: float) -> str | None:
        """Protokolün beyanını deftere geçirir.

        `kopma` bir bekleyen kayıt açar; aynı `(düğüm, komşu)` için gelen ilk
        `rota_kuruldu` onu kapatır ve Δ üretir.

        🔒 Döner: `"acildi"` (yeni bir kopma döngüsü) · `"kapandi"` (bir Δ
        üretildi) · `None`. Sayaç kütüğü COR'un ikizini (`cor`, `cor_pencere`)
        bu dönüşten besler — iki COR hesabı AYNI tanımdan gelsin diye (K-141).
        """
        self._olaylar.append(RotaOlayi(beyan.tip, dugum, beyan.komsu, t_s))
        anahtar = (dugum, beyan.komsu)
        if beyan.tip == "kopma":
            # Aynı bağ için ikinci kopma beyanı ilkini EZMEZ: protokol
            # tekrar beyan ederse ölçülen şey ilk kesintinin süresi olmalı.
            if anahtar in self._bekleyen:
                return None
            self._bekleyen[anahtar] = t_s
            self._acilan += 1
            return "acildi"
        if beyan.tip == "rota_kuruldu":
            baslangic = self._bekleyen.pop(anahtar, None)
            if baslangic is not None:
                dogrula(t_s >= baslangic, "kurtarma kopmadan önce olamaz")
                self._delta.append(t_s - baslangic)
                return "kapandi"
        return None

    # ---------------------------------------------------------- sayımlar
    def sayim(self, tip: str) -> int:
        return sum(1 for o in self._olaylar if o.tip == tip)

    def beyan_anlari(self, tip: str) -> tuple[float, ...]:
        """Bir beyan tipinin ZAMAN DAMGALARI — evre metrikleri için.

        🔒 Sayım yetmiyor: tespit gecikmesi *"beyan hızı ne zaman yükseldi"*
        diye soruyor ve bunun için anlar gerekiyor. Salt okunur bir görünüm;
        defterin durumunu değiştirmez.

        🔴 Bu bir KÂHİN sızıntısı DEĞİLDİR: içerik protokolün KENDİ
        beyanıdır, simülatörün gördüğü gerçek değil. Kâhin olan
        `kopma_fiziksel` zaten `Kahin[int]` sarmalayıcısıyla dönüyor.
        """
        return tuple(o.t_s for o in self._olaylar if o.tip == tip)

    @property
    def kopma_algilanan(self) -> int:
        return self.sayim("kopma")

    @property
    def kopma_rota_gecersiz(self) -> int:
        return self.sayim("rota_gecersiz")

    @property
    def rota_kurtarildi(self) -> int:
        return len(self._delta)

    @property
    def rota_etkilendi(self) -> int:
        """COR'un paydası: AÇILAN kopma döngüsü sayısı (K-141).

        🔴 Önceden *"kopma beyan edilen ayrı bağ sayısı"*ydı ve pay döngü
        saydığı için COR 1'i aşabiliyordu. Aynı bağın ikinci kopması, ilki
        kapandıysa, yeni bir döngüdür ve yeni bir paydadır.
        """
        return self._acilan

    def kopma_fiziksel(self) -> Kahin[int]:
        """🔴 KÂHİN SARMALAYICI ile döner: protokol bunu okuyamaz."""
        return kahin(self._fiziksel_kopma)

    # ------------------------------------------------------- türetilenler
    @property
    def beyan_etmiyor(self) -> bool:
        """🔴 Kol hiç kopma beyan etmediyse `True` — ve etiketlenir.

        Hiç beyan etmemek bir başarı değildir; ölçülmemiş olmaktır.
        """
        return self.kopma_algilanan == 0

    def algilama_duyarliligi(self) -> float | None:
        """Protokol gerçek kopmaların ne kadarını GÖRÜYOR.

        Payda kâhin sayaçtır. Fiziksel kopma hiç olmadıysa `None` — oran
        tanımsızdır ve 0 döndürmek onu ortalamaya sokardı.
        """
        if self._fiziksel_kopma == 0:
            return None
        return self.kopma_algilanan / self._fiziksel_kopma

    def delta_ler(self) -> tuple[float, ...]:
        """🔴 Hiç beyan yoksa BOŞ döner; çağıran `None` yazar, 0 değil."""
        return tuple(self._delta)

    def cor(self) -> float | None:
        payda = self.rota_etkilendi
        # 🔒 Değişmez: her açılan döngü ya kapandı ya hâlâ bekliyor.
        dogrula(self.rota_kurtarildi + len(self._bekleyen) == payda,
                "kopma döngüsü muhasebesi ayrıştı — kapanan + bekleyen ≠ açılan")
        if payda == 0:
            return None
        return self.rota_kurtarildi / payda

    def kapanmamis_kopma(self) -> int:
        """Beyan edilip hiç kurtarılmamış kopmalar — Δ'nın sansürlü kuyruğu.

        ⚠️ Bunlar Δ ortalamasına GİRMEZ (süreleri bilinmiyor) ama sayıları
        rapora yazılır: girmediklerini bilmeden Δ okumak, kurtarılamayan
        kopmaları yok saymak olur.
        """
        return len(self._bekleyen)
