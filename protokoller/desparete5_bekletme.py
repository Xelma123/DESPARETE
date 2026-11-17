"""
DESPARETE 5 · bekletme ve komutun yolu — KK-05 (T-18 · T-20).

Saf modül.

🔒 BEKLETME (KK-05/1–5)
Yol yokken paket simülatörün bekletme tamponunda tutulur (`Karar.beklet`);
sınır atlama başınadır (`TUTMA_EN_COK`). Paketin yaşı protokole görünmez
(`05` §3.2); ilk bekletildiği an paket kimliğiyle `(kaynak, kaynak_sira)`
burada tutulur. Simülatör tamponu yalnız bir uyandırmadan sonra döker (K-135);
yeniden sorma uyandırmasını ana sınıf kurar.

🔒 GERİ İZ (KK-05/6–9; v0.4.1'in V11'i, K-172)
Her röle, geçide giden telemetriyi hangi komşudan aldığını hatırlar; o kaynağa
giden komut o komşuya verilir. İz yalnız DAHA YENİ bir paket sırasıyla
güncellenir (v0.4.1'in kuralı; 18 Kasım, kodlamada G-1): izden ize ilerleyen
her adımda sıra azalmaz, çapraz giden iki paket iki düğümü birbirine
gösteremez; döngü ancak aynı paketin yolunda olabilir, o yol da döngüsüzdür.
"""

from __future__ import annotations

from protokoller.desparete5_bicim import Bayraklar, Degerler

__all__ = ["Bekletme", "GeriIz", "GONDER", "BEKLET", "DUS"]

GONDER, BEKLET, DUS = "gonder", "beklet", "dus"


class Bekletme:
    """`ilk`: paket kimliği → bu düğümde ilk bekletildiği an."""

    __slots__ = ("d", "b", "ilk", "sayac")

    def __init__(self, degerler: Degerler, bayraklar: Bayraklar) -> None:
        self.d = degerler
        self.b = bayraklar
        self.ilk: dict[tuple[int, int], float] = {}
        self.sayac = {"bekletilen": 0, "bekletmeden_giden": 0,
                      "suresi_dolan": 0, "bayrak_kapali_dusen": 0}

    def karar(self, kimlik: tuple[int, int], t: float, yol_var: bool) -> str:
        """KK-05/1–2. Yol varsa gönderilir; yoksa bayrak kapalıyken düşer;
        açıkken `TUTMA_EN_COK` dolana kadar beklenir, dolunca düşer."""
        if yol_var:
            if self.ilk.pop(kimlik, None) is not None:
                self.sayac["bekletmeden_giden"] += 1
            return GONDER
        if not self.b.bekletme:
            self.sayac["bayrak_kapali_dusen"] += 1
            return DUS
        t0 = self.ilk.get(kimlik)
        if t0 is None:
            self.ilk[kimlik] = t
            self.sayac["bekletilen"] += 1
            return BEKLET
        if t - t0 >= self.d.TUTMA_EN_COK_S:
            del self.ilk[kimlik]
            self.sayac["suresi_dolan"] += 1
            return DUS
        return BEKLET

    def temizle(self, t: float) -> None:
        """KK-05/4: `TUTMA_EN_COK + 1 s`'den yaşlı kayıt silinir; simülatörün
        sayı tavanıyla düşen paketin kaydı kalmaz, gereksiz uyanma üretmez."""
        sinir = t - self.d.TUTMA_EN_COK_S - 1.0
        for k in [k for k, t0 in self.ilk.items() if t0 <= sinir]:
            del self.ilk[k]

    @property
    def bekleyen_var(self) -> bool:
        return bool(self.ilk)


class GeriIz:
    """`iz`: kaynak → (komşu, kaynak_sira, an)."""

    __slots__ = ("d", "iz", "sayac")

    def __init__(self, degerler: Degerler) -> None:
        self.d = degerler
        self.iz: dict[int, tuple[int, int, float]] = {}
        self.sayac = {"iz_ogrenilen": 0, "iz_eski_sira": 0}

    def ogren(self, kaynak: int, komsu: int, kaynak_sira: int,
              t: float) -> None:
        """KK-05/6: geçide giden telemetri bana `komsu`dan geldi."""
        eski = self.iz.get(kaynak)
        if eski is not None and kaynak_sira <= eski[1]:
            self.sayac["iz_eski_sira"] += 1
            return
        self.iz[kaynak] = (komsu, kaynak_sira, t)
        self.sayac["iz_ogrenilen"] += 1

    def sonraki(self, hedef: int, t: float, kullanilir) -> int | None:
        """KK-05/7–8: iz var, `IZ_TAZELIK` içinde ve gösterdiği komşu OLAĞAN
        ise o komşu; değilse `None` (iz bayat ya da yok)."""
        kayit = self.iz.get(hedef)
        if kayit is None or t - kayit[2] > self.d.IZ_TAZELIK_S:
            return None
        return kayit[0] if kullanilir(kayit[0]) else None

    def biliniyor(self, hedef: int) -> bool:
        return hedef in self.iz
