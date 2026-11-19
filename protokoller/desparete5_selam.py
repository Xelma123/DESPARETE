"""
DESPARETE 5 · selam ve ara ilan — KK-02 (T-1 · T-16 · T-17).

Saf modül. Selamın zamanlaması (`SelamZamanlayici`), iletinin kurulması ve
çözülmesi (`selam_yuku` · `selam_coz`) ve "önemli değişim" ölçütü
(`onemli_degisim`).

🔒 ARALIK (KK-02/1–2; Trickle [62], bastırması alınmadı)
Olaysız geçen her selamdan sonra I ← min(2·I, I_MAX); bir değişim olayında
I ← I_MIN ve selam hemen gider. Selamın `aralik` alanı bir sonraki selama
kadarki üst sınırdır: bu selamdan sonra geçerli I'nın titreşim dâhil 1,1
katı (RFC 8966 §4.6.5). `uyarlanir_aralik` kapalıyken I sabit I_MAX'tır ve
ara ilan I'yı değiştirmez (Y-5).

🔒 SELAM ANINDA KURULUR (G-5)
Titreşim uyandırmaya eklenir; ileti uyandırma anında, o anki bilgiyle
kurulur. Böylece içerik bayatlamaz ve "gönderemezken selam kurulmaz"
(KK-02/5) kurma anında denetlenir.
"""

from __future__ import annotations

import math

from sim2.gozlem.kontrol import Uyandirma
from protokoller.desparete5_bicim import (
    ARALIK_BIRIMI_S, ORAN_EN_COK, SONSUZ, Bayraklar, Degerler, sira_artir)

__all__ = ["SelamZamanlayici", "selam_yuku", "selam_coz", "onemli_degisim",
           "ETIKET"]

ETIKET = "selam:"
_INF = math.inf


class SelamZamanlayici:
    """KK-02/1–5. Uyandırmalar iptal edilemediği için her plan bir nesil
    numarası taşır; eski nesilden gelen uyandırma yok sayılır."""

    __slots__ = ("d", "b", "I", "son_t", "planli_t", "nesil", "olay_var",
                 "sira", "ed_bekliyor", "sayac")

    def __init__(self, degerler: Degerler, bayraklar: Bayraklar) -> None:
        self.d = degerler
        self.b = bayraklar
        # Başlangıç aralığı I_MIN (Trickle; G-6); bayrak kapalıyken I_MAX.
        self.I = (degerler.I_MIN_S if bayraklar.uyarlanir_aralik
                  else degerler.I_MAX_S)
        self.son_t = -_INF          # son selamın kurulduğu an
        self.planli_t = _INF        # geçerli planın hedef anı
        self.nesil = 0
        self.olay_var = False       # son selamdan beri değişim olayı oldu mu
        self.sira = 0               # `sira` 0'dan başlar (KK-00 genel kural 3)
        self.ed_bekliyor = False
        self.sayac = {"selam": 0, "ara_ilan": 0, "ed_atlanan": 0}

    def _planla(self, hedef_t: float, t: float) -> Uyandirma | None:
        """Hedef, mevcut plandan erkense yeni plan (yeni nesil)."""
        if hedef_t >= self.planli_t:
            return None
        self.planli_t = hedef_t
        self.nesil += 1
        return Uyandirma(max(hedef_t - t, 1e-3), f"{ETIKET}{self.nesil}",
                         jitter_s=self.d.TITRESIM_ORANI * self.I)

    def baslat(self, t: float) -> Uyandirma | None:
        """İlk selam (açılış): hemen, titreşimle."""
        return self._planla(t, t)

    def olay(self, t: float) -> Uyandirma | None:
        """KK-02/3: değişim olayı. I ← I_MIN (bayrak açıkken) ve selam
        hemen; iki selam arasında en az `I_MIN` geçer, bu arada olan
        olaylar bir sonraki selamda birleşir."""
        self.olay_var = True
        if self.b.uyarlanir_aralik:
            self.I = self.d.I_MIN_S
        return self._planla(max(t, self.son_t + self.d.I_MIN_S), t)

    def guncel_mi(self, etiket: str) -> bool:
        return etiket == f"{ETIKET}{self.nesil}"

    def kur(self, t: float, gonderemez: bool
            ) -> tuple[tuple[int, float] | None, Uyandirma | None]:
        """Güncel uyandırma doldu. Döner: ((sıra, ilan edilen aralık) ya da
        `None`, sonraki uyandırma).

        KK-02/5: `gonderemez` (kendi ED kaynaklı durumum) iken selam
        kurulmaz ve yeniden planlanmaz; durum bitince `ed_bitti` hemen bir
        selam ister."""
        self.planli_t = _INF
        if gonderemez:
            self.ed_bekliyor = True
            self.sayac["ed_atlanan"] += 1
            return None, None
        if self.olay_var:
            self.sayac["ara_ilan"] += 1
        elif self.b.uyarlanir_aralik:
            self.I = min(2.0 * self.I, self.d.I_MAX_S)
        self.olay_var = False
        sira = self.sira
        self.sira = sira_artir(self.sira)
        self.son_t = t
        self.sayac["selam"] += 1
        aralik = self.d.ARALIK_PAYI * self.I
        return (sira, aralik), self._planla(t + self.I, t)

    def ed_bitti(self, t: float) -> Uyandirma | None:
        """KK-02/5: gönderemediğim durum bitti → hemen bir selam. Bitişi
        bir değişim olayı sayarım (T-10: karıştırmanın bittiği çabuk
        duyulsun)."""
        self.ed_bekliyor = False
        return self.olay(t)


# ==========================================================================
# İleti — KK-02 alan tablosu
# ==========================================================================
def selam_yuku(sira: int, aralik_s: float, tur: int | None, maliyet: int,
               karistiriliyorum: bool, komsu: tuple[int, ...],
               oran: tuple[int, ...]) -> dict:
    """`KontrolIstegi.kur` için yük. `aralik` 0,01 s biriminde, yukarı
    yuvarlanır (üst sınır olduğu için). `tur` `None` ise eğimin biçimi
    (`SELAM_E`, tur alanı yok; KK-02, 19 Kasım), değilse 18 Kasım'ın
    `SELAM`ı."""
    aralik_cs = min(0xFFFF, max(1, math.ceil(aralik_s / ARALIK_BIRIMI_S
                                             - 1e-9)))
    if tur is None:
        return {"sira": sira & 0xFFFF, "aralik": aralik_cs,
                "maliyet": min(int(maliyet), SONSUZ),
                "karistiriliyorum": bool(karistiriliyorum),
                "komsu": tuple(komsu), "oran": tuple(oran)}
    return {"sira": sira & 0xFFFF, "aralik": aralik_cs, "tur": tur & 0xFFFF,
            "maliyet": min(int(maliyet), SONSUZ),
            "karistiriliyorum": bool(karistiriliyorum),
            "komsu": tuple(komsu), "oran": tuple(oran)}


def selam_coz(yuk, ben: int) -> tuple[int, float, int | None, int, bool,
                                      float | None]:
    """Döner: (sıra, aralık s, tur ya da `None` — eğimin biçiminde tur yok,
    maliyet, bit, benim için bildirilen oran ya da `None` — gönderen beni
    listelemiyorsa)."""
    y = dict(yuk)
    bildirilen = None
    for j, r in zip(y["komsu"], y["oran"]):
        if j == ben:
            bildirilen = r / ORAN_EN_COK
            break
    tur = int(y["tur"]) if "tur" in y else None
    return (int(y["sira"]), y["aralik"] * ARALIK_BIRIMI_S, tur,
            int(y["maliyet"]), bool(y["karistiriliyorum"]), bildirilen)


def onemli_degisim(yeni: int, ilan: int | None, esik: float) -> bool:
    """KK-02/3 ilk madde: geçide maliyetim son ilan ettiğimden `ILAN_ESIGI`
    kadar farklı ya da ∞ ↔ sonlu. Hiç ilan etmediysem değişimdir."""
    if ilan is None:
        return True
    if (yeni >= SONSUZ) != (ilan >= SONSUZ):
        return True
    if yeni >= SONSUZ:
        return False
    if ilan == 0:                       # geçit: maliyeti hep 0
        return yeni != 0
    return abs(yeni - ilan) >= esik * ilan
