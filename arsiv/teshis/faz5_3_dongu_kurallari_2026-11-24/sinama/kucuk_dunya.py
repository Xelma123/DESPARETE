"""Küçük test dünyasında iki kuralın davranışı (aletin ve kodun sınaması;
ölçüm değil, karara girmez). 12 düğüm, `tests2/test_desparete5.py`'nin
dünyası, tohum 1000, tek koşu.

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz5_3_dongu_kurallari_2026-11-24/sinama/kucuk_dunya.py > .../sinama/kucuk_dunya.txt

Bölüm 1: dört profil (19 Kasım · yalnız geri · yalnız sınır · ikisi) iki
senaryoda; teslim ve yol seçimi sayaçları.
Bölüm 2: yalnız sınır açıkken her yükselme kopmasının anı, düğüm, L, eski
maliyet, ardıl üzerinden yeni maliyet, ardılın kendi ardılı (döngü mü?).
"""
import sys
from dataclasses import replace
from pathlib import Path

KOK = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(KOK / "tests2"))
sys.path.insert(0, str(KOK))

from protokoller import desparete5_egim as EG                 # noqa: E402
from protokoller.desparete5_bicim import (                     # noqa: E402
    CEKIRDEK, CEKIRDEK_19K, maliyet_topla)
import test_desparete5 as T                                     # noqa: E402

SAYAC = ("rota.dongu", "rota.son_care", "rota.yol_yok", "rota.tavan_asimi",
         "rota.geri_yasagi", "rota.geri_bekletme", "rota.yukselme_kopma")
PROFIL = (("19 Kasım", CEKIRDEK_19K),
          ("yalnız geri", replace(CEKIRDEK, sinirli_yukselme=False)),
          ("yalnız sınır", replace(CEKIRDEK, geri_yasagi=False)),
          ("ikisi", CEKIRDEK))

print("== 1 · dört profil ==")
for sen in ("statik-surekli", "statik-yok"):
    for ad, b in PROFIL:
        s = T._kos(sen, b)
        t, r = s["toplam"], s["korunum"]
        print(f"{sen:<15} {ad:<13} teslim {r['teslim']}/{r['uretilen']} · "
              + " · ".join(f"{k.split('.')[1]} {t[k]}" for k in SAYAC))

print("\n== 2 · yükselme kopmaları (statik-surekli, yalnız sınır) ==")
print("t · düğüm · eski ardıl · L · eski C · ardıl üzerinden yeni m (ETX) · "
      "eski ardılın ardılı · yeni ardıl")
kayit, rotalar = [], {}
asil_sec, asil_init = EG.Egim.sec, EG.Egim.__init__


def init(self, *a, **kw):
    asil_init(self, *a, **kw)
    rotalar[self.kimlik] = self


def sec(self, t, baglar, kd):
    once = self.sayac["yukselme_kopma"]
    eski, C0, L = self.ardil, self.C, self._L(t)
    m = (maliyet_topla(baglar.maliyet(eski), self.ilanlar[eski])
         if eski is not None and eski in self.ilanlar else None)
    asil_sec(self, t, baglar, kd)
    if self.sayac["yukselme_kopma"] > once:
        a = rotalar.get(eski)
        kayit.append((round(t, 2), self.kimlik, eski, round(L / 64, 3),
                      round(C0 / 64, 3), None if m is None else round(m / 64, 3),
                      None if a is None else a.ardil, self.ardil))


EG.Egim.sec, EG.Egim.__init__ = sec, init
try:
    T._kos("statik-surekli", replace(CEKIRDEK, geri_yasagi=False))
finally:
    EG.Egim.sec, EG.Egim.__init__ = asil_sec, asil_init
for k in sorted(kayit):
    print(k)
