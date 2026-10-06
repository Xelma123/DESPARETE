"""
Hız uyarlaması — ARF, komşu başına. `v2/15` A4 · K-177.

Kaynak: ns-3 `ArfWifiManager` (`v2/02` G14; `protokol_kaynaklari/
uygulama_kaynaklari/ns-3/arf-wifi-manager.cc`), Kamerman & Monteban
1997'nin ARF'sinin paket sayaçlı hâli. Bu dosya o kodun BİREBİR aktarımıdır:

  · başlangıç en düşük hız;
  · başarı: sayaç++, başarı++, başarısız = 0, kurtarma kapanır; başarı
    eşiğe (10) ya da sayaç eşiğe (15) ulaşırsa ve en yüksekte değilse →
    bir hız yukarı, sayaç = başarı = 0, KURTARMA kipi;
  · başarısızlık: sayaç++, başarısız++, başarı = 0;
      kurtarmada: başarısız == 1 ise bir hız aşağı; sayaç = 0;
      normalde : (başarısız − 1) tekse (2., 4., … başarısızlık) bir hız
                 aşağı; başarısız ≥ 2 ise sayaç = 0.

Her iletim DENEMESİ ayrı bildirilir (yeniden denemeler dâhil) — ns-3'ün
notu: *"ARF handles each data transmission independently"*.
🔒 `mac/` fizik yapmaz: burada yalnız sayaç mantığı var; hangi hızın hangi
PER'i verdiği `kanal/`dadır.
"""

from __future__ import annotations

from sim2.cekirdek.degismezler import dogrula

__all__ = ["Arf"]


class Arf:
    """Komşu başına ARF durumu: `[hız sırası, başarı, başarısız, kurtarma,
    sayaç]`."""

    __slots__ = ("_hizlar", "_basari_esigi", "_sayac_esigi", "_durum")

    def __init__(self, hizlar: tuple[float, ...], basari_esigi: int,
                 sayac_esigi: int) -> None:
        dogrula(len(hizlar) >= 1 and list(hizlar) == sorted(hizlar),
                "hızlar artan sırada olmalı")
        dogrula(basari_esigi >= 1 and sayac_esigi >= 1,
                "ARF eşikleri pozitif olmalı")
        self._hizlar = tuple(hizlar)
        self._basari_esigi = basari_esigi
        self._sayac_esigi = sayac_esigi
        self._durum: dict[int, list] = {}

    def _st(self, komsu: int) -> list:
        return self._durum.setdefault(komsu, [0, 0, 0, False, 0])

    def hiz(self, komsu: int) -> float:
        return self._hizlar[self._st(komsu)[0]]

    def basarili(self, komsu: int) -> None:
        s = self._st(komsu)
        s[4] += 1
        s[1] += 1
        s[2] = 0
        s[3] = False
        if ((s[1] == self._basari_esigi or s[4] == self._sayac_esigi)
                and s[0] < len(self._hizlar) - 1):
            s[0] += 1
            s[4] = 0
            s[1] = 0
            s[3] = True

    def basarisiz(self, komsu: int) -> None:
        s = self._st(komsu)
        s[4] += 1
        s[2] += 1
        s[1] = 0
        if s[3]:
            if s[2] == 1 and s[0] != 0:
                s[0] -= 1
            s[4] = 0
        else:
            if (s[2] - 1) % 2 == 1 and s[0] != 0:
                s[0] -= 1
            if s[2] >= 2:
                s[4] = 0

    def dagilim(self) -> dict[float, int]:
        """Teşhis: komşuların şu anki hızlarının dağılımı."""
        cikti: dict[float, int] = {h: 0 for h in self._hizlar}
        for s in self._durum.values():
            cikti[self._hizlar[s[0]]] += 1
        return cikti
