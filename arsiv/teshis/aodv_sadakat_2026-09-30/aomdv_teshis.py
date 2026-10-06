"""AOMDV-c neden kötüleşti? — eşler arası statik-yok 1001 (0,991 → 0,870).

    PYTHONIOENCODING=utf-8 py -3.11 -u arsiv/teshis/aodv_sadakat_2026-09-30/aomdv_teshis.py [kok] [desen] [kol] [tohum]

`kok` verilirse o kod ağacı koşar (U1 kopyası = AOMDV-b). Tam pencere, U1'in
konfigürasyonu. Basılan: PDR, düşüş sebepleri, AOMDV sayaçları ve (yeni kodda)
`sonraki_atlama`nın ara düğümde rotasız kaldığı durumların türü.
"""
import collections
import os
import pathlib
import sys

KOK = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 and sys.argv[1] != "-" \
    else pathlib.Path(__file__).resolve().parents[3]
DESEN = sys.argv[2] if len(sys.argv) > 2 else "esler_arasi"
KOL = sys.argv[3] if len(sys.argv) > 3 else "statik-yok"
TOHUM = int(sys.argv[4]) if len(sys.argv) > 4 else 1001
sys.path.insert(0, str(KOK))
os.environ["DESPARETE_DUNYA"] = "referans_2026"

from kalibrasyon import dunya_secimi as DS  # noqa: E402
from kalibrasyon.aodv_uygunluk import _fabrika  # noqa: E402
from protokoller import aomdv as M  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.kosum.sonuc import sonuc_satiri  # noqa: E402

kfg = DS.konfig(kol="u1", senaryo=KOL, tohum=TOHUM, trafik_deseni=DESEN)
kur = kurulum_yap(kfg)
durum = collections.Counter()
asil = M.AOMDV.sonraki_atlama


def izle(self, gozlem):
    p = gozlem.paket
    if p is not None and p.kaynak != self.kimlik:
        simdi = float(gozlem.saat_s)
        r = self._rota.get(p.hedef)
        if r is None:
            durum["ara: girdi yok"] += 1
        elif not r.gecerli:
            durum["ara: gecersiz"] += 1
        elif r.son_gecerli_s <= simdi:
            durum["ara: suresi dolmus"] += 1
        elif r.sonraki not in self._komsu:
            durum["ara: sonraki komsu degil"] += 1
        else:
            durum["ara: rota var"] += 1
    k = asil(self, gozlem)
    if k.beklet and p is not None and p.kaynak != self.kimlik:
        durum["ara: TAMPONLADI"] += 1
    return k


# `ESKI_KARAR=1`: yalnız veri kararı (H8) U1 kopyasındaki eski hâliyle —
# nedensellik sınaması; geri kalan kod yeni.
if os.environ.get("ESKI_KARAR"):
    import importlib.util
    yol = pathlib.Path(__file__).resolve().parents[1] / "u1_2026-09-29" / "kopya" / "protokoller" / "aodv.py"
    spec = importlib.util.spec_from_file_location("aodv_eski", yol)
    eski = importlib.util.module_from_spec(spec)
    sys.modules["aodv_eski"] = eski
    spec.loader.exec_module(eski)
    asil = eski.AODV.sonraki_atlama
    print("veri karari: ESKI (U1 kopyasi)")
M.AOMDV.sonraki_atlama = izle
kosu = Kosu(kur, _fabrika("aomdv", kfg))
kosu.kostur()
satir = sonuc_satiri(kur, kosu.dugumler, "aomdv")
toplam = collections.Counter()
for d in kosu.dugumler:
    toplam.update(d.protokol._sayac)
print(f"kod {KOK.name} · {DESEN} {KOL} {TOHUM} · pdr {satir['metrikler']['pdr']:.4f}")
print("  dusus:", {k: v for k, v in kur.korunum.dusen.items() if v})
print("  sayac:", {k: v for k, v in sorted(toplam.items()) if v})
print("  ara dugum:", dict(durum))
