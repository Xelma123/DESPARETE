"""
DESPARETE 5 · karıştırma kanıtı, kendi durumum — KK-03 A (kural 1–4; T-5 ·
T-6 · T-8 · T-10). Bağa ait kanıt (KK-03 B) `desparete5_bag.py`dedir.

Saf modül. Saniyelik zamanlayıcıda bir kez `saniye(t, mesgul, cozulen, s)`
çağrılır: `mesgul` kanalın meşgul kaldığı toplam süre (`mesgul_sure_s`,
802.11k sayacı), `cozulen` çözülen çerçeve sayacı (`alinan_cerceve`), `s`
bağ tablosunun selam kaybı payı. Açık kurallar, eğitilmiş sınıflandırıcı yok
(T-8).

🔒 KAYNAK (KK-03/4; Y-3)
ED alanında girişim işaretinin iki koşulu da her saniye sağlanır (çözülen
çerçeve düşer, selamlar gelmez). "Son görülen işaret" kuralı aynı saniyede
tanımsız kalırdı ve kaynak girişime dönerdi. Bu yüzden: ED işareti görülen
saniyede kaynak ED'dir; kaynak girişime yalnız ED işaretinin olmadığı bir
saniyede geçer.

🔒 ÜST SÜRE (KK-01/13; Y-6, 18 Kasım)
Durum `KENDI_UST_SURE` (30 s) sürünce DONDURMA biter (`dondurma` False olur);
bit ve "gönderemezken selam kurulmaz" durum sürdükçe sürer.
"""

from __future__ import annotations

import math
from collections import deque

from protokoller.desparete5_bicim import Bayraklar, Degerler

__all__ = ["KendiDurum", "ED", "GIRISIM"]

ED, GIRISIM = "ed", "girisim"
_INF = math.inf


class KendiDurum:
    """KK-03/1–4. `saniye` olayları döndürür; durum alanlardan okunur."""

    __slots__ = ("d", "b", "karistiriliyorum", "kaynak", "giris_t",
                 "dondurma", "_isaretli_ardisik", "_isaretsiz_ardisik",
                 "_onceki", "_c_gecmis", "sayac")

    def __init__(self, degerler: Degerler, bayraklar: Bayraklar) -> None:
        self.d = degerler
        self.b = bayraklar
        self.karistiriliyorum = False
        self.kaynak: str | None = None
        self.giris_t = _INF
        self.dondurma = False             # KK-01/13 yürürlükte
        self._isaretli_ardisik = 0        # girişim işaretli ardışık saniye
        self._isaretsiz_ardisik = 0       # durumdayken işaretsiz ardışık saniye
        self._onceki: tuple[float, float, int] | None = None
        # c̄: son ORTALAMA_SANIYE işaretsiz saniyenin çözülen çerçevesi
        self._c_gecmis: deque = deque(maxlen=degerler.ORTALAMA_SANIYE)
        self.sayac = {"isaret_ed": 0, "isaret_girisim": 0, "giris_ed": 0,
                      "giris_girisim": 0, "cikis": 0, "ust_sure": 0,
                      "kaynak_degisti": 0, "durum_saniye": 0}

    @property
    def gonderemez(self) -> bool:
        """KK-02/5: kendi ED kaynaklı durumum — kanal meşgul, gönderemem."""
        return self.karistiriliyorum and self.kaynak == ED

    @property
    def c_ort(self) -> float | None:
        g = self._c_gecmis
        return sum(g) / len(g) if g else None

    def saniye(self, t: float, mesgul: float | None, cozulen: int,
               s: float | None) -> set[str]:
        """Döner: olaylar — "basladi" · "bitti" · "dondurma_bitti" ·
        "ed_bitti" (gönderemez durumundan çıkış; selam hemen)."""
        olay: set[str] = set()
        if not self.b.karistirma_durumu:
            return olay
        onceki, self._onceki = self._onceki, (t, mesgul or 0.0, cozulen)
        if onceki is None or t <= onceki[0]:
            return olay
        d = self.d
        dt = t - onceki[0]
        m = ((mesgul or 0.0) - onceki[1]) / dt     # KK-03/1: meşgul payı
        c = cozulen - onceki[2]                     # son saniyede çözülen
        ed = m >= d.ED_ESIGI
        c_ort = self.c_ort
        girisim = (c_ort is not None and s is not None
                   and c < d.DUSUS_ORANI * c_ort and s >= d.KAYIP_ESIGI)
        if ed:
            self.sayac["isaret_ed"] += 1
        if girisim:
            self.sayac["isaret_girisim"] += 1
        if not ed and not girisim:
            self._c_gecmis.append(c)                # yalnız işaretsiz saniye
        self._isaretli_ardisik = self._isaretli_ardisik + 1 if girisim else 0
        gonderemezdi = self.gonderemez
        if not self.karistiriliyorum:
            if ed and d.ED_GIRIS_SANIYE <= 1:
                self._gir(t, ED, olay)
            elif self._isaretli_ardisik >= d.GIRIS_SANIYE:
                self._gir(t, GIRISIM, olay)
        else:
            self.sayac["durum_saniye"] += 1
            if ed or girisim:
                self._isaretsiz_ardisik = 0
                yeni = ED if ed else GIRISIM        # Y-3
                if yeni != self.kaynak:
                    self.kaynak = yeni
                    self.sayac["kaynak_degisti"] += 1
            else:
                self._isaretsiz_ardisik += 1
                gerek = (d.ED_CIKIS_SANIYE if self.kaynak == ED
                         else d.CIKIS_SANIYE)
                if self._isaretsiz_ardisik >= gerek:
                    self._cik(olay)
            if (self.karistiriliyorum and self.dondurma
                    and t - self.giris_t >= d.KENDI_UST_SURE_S):
                self.dondurma = False               # Y-6
                self.sayac["ust_sure"] += 1
                olay.add("dondurma_bitti")
        if gonderemezdi and not self.gonderemez:
            olay.add("ed_bitti")
        return olay

    def _gir(self, t: float, kaynak: str, olay: set[str]) -> None:
        self.karistiriliyorum = True
        self.kaynak = kaynak
        self.giris_t = t
        self.dondurma = True
        self._isaretsiz_ardisik = 0
        self.sayac["giris_" + kaynak] += 1
        olay.add("basladi")

    def _cik(self, olay: set[str]) -> None:
        if self.dondurma:
            olay.add("dondurma_bitti")
        self.karistiriliyorum = False
        self.kaynak = None
        self.giris_t = _INF
        self.dondurma = False
        self._isaretsiz_ardisik = 0
        self._isaretli_ardisik = 0
        self.sayac["cikis"] += 1
        olay.add("bitti")
