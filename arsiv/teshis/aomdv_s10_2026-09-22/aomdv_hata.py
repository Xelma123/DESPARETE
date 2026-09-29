import sys
from collections import Counter
from pathlib import Path
KOK = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KOK)); sys.path.insert(0, str(KOK / "tests2"))
from protokoller.aodv import AODV
from protokoller.aomdv import AOMDV
from sim2.kosum.kosu import Kosu
from sim2.kosum.kurulum import kurulum_yap
from sim2.kosum.sonuc import sonuc_satiri
from test_kosum import _konfig

IZ = Counter()


def izle(taban):
    class I(taban):
        def sonraki_atlama(self, g):
            k = super().sonraki_atlama(g)
            if g.paket is not None and k.beklet:
                t = float(g.saat_s)
                r = self._rota.get(g.paket.hedef)
                if r is None:
                    IZ[taban.__name__, "beklet:girdi_yok"] += 1
                elif not r.gecerli:
                    IZ[taban.__name__, "beklet:gecersiz"] += 1
                elif r.son_gecerli_s <= t:
                    IZ[taban.__name__, "beklet:suresi_dolmus_gecerli"] += 1
                elif r.sonraki not in self._komsu:
                    IZ[taban.__name__, "beklet:birincil_komsu_degil"] += 1
                else:
                    IZ[taban.__name__, "beklet:BASKA"] += 1
                IZ[taban.__name__, "kesif_suruyor" if g.paket.hedef in self._kesif
                   else "kesif_yok"] += 1
            return k

        def _rrep_isle(self, gonderen, y, simdi):
            if y["kaynak"] == self.kimlik and y["kaynak"] != y["hedef"]:
                once = self._rota.get(y["hedef"])
                once_kul = once is not None and self._taze_mi(once, simdi)
                n = super()._rrep_isle(gonderen, y, simdi)
                sonra = self._rota_al(y["hedef"], simdi) is not None
                uy = any(getattr(x, "etiket", "") == "tampon" for x in n)
                IZ[taban.__name__, f"kaynak_rrep once_kul={once_kul} sonra_kul={sonra} uyandirma={uy}"] += 1
                return n
            return super()._rrep_isle(gonderen, y, simdi)
    return I


for sinif in (AODV, AOMDV):
    kur = kurulum_yap(_konfig("bagimsiz-yok", 1000, 60.0))
    kosu = Kosu(kur, izle(sinif))
    kosu.kostur()
    s = sonuc_satiri(kur, kosu.dugumler, "d")
    print(sinif.__name__, "pdr", round(s["metrikler"]["pdr"], 4), s["korunum"]["dusen"],
          "tampon_giris", s["metrikler"]["tampon_giris"])
for k, v in sorted(IZ.items()):
    print(" ", k, v)
