"""
Regresyon k243 · beklenti dışı değişen vakanın sebep doğrulaması.

`p-statik-surekli-dogrudan_komsu-karistirici_gercekci-cephe_hatti` vakasını,
yer–hava kanalı k236'daki zaman dilimli modele (`e5cd1b7~1`, dilim 1 s)
döndürülmüş hâlde bugünkü kodla koşar ve k236 satırıyla alan alan
karşılaştırır. Kalan farklar yalnız kimlik ve beklentideki izinli alanlarsa
vakadaki değişimin tek sebebi DD-01'dir (kalıcı görüş hattı).

    py -3.11 arsiv/teshis/regresyon_k243/eski_gorus_hatti.py
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ANA = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ANA))
VAKA = "p-statik-surekli-dogrudan_komsu-karistirici_gercekci-cephe_hatti"


def _eski_yer_hava():
    kaynak = subprocess.run(
        ["git", "show", "e5cd1b7~1:sim2/kanal/yer_hava.py"], cwd=ANA,
        check=True, capture_output=True).stdout
    with tempfile.TemporaryDirectory() as d:
        yol = Path(d) / "yer_hava_k236.py"
        yol.write_bytes(kaynak)
        spec = importlib.util.spec_from_file_location("yer_hava_k236", yol)
        modul = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(modul)
    return modul


def main() -> int:
    eski = _eski_yer_hava()
    import sim2.kanal.karistirici as K
    K.YerHavaKanali = lambda tohum, ortam: eski.YerHavaKanali(tohum, ortam,
                                                              1.0)

    def _kayip_db(self, dugum, dugum_konum, t_s):
        kaynak = self.konum_t(t_s)
        kayip = self.yayilim.yavas_kayip_db(self._golge_kimligi, dugum,
                                            kaynak, dugum_konum)
        if self._a2g is not None:
            kayip += self._a2g.ek_kayip_db(self._golge_kimligi, dugum, kaynak,
                                           dugum_konum, t_s)
        return kayip
    K.KaristiriciTabani._kayip_db = _kayip_db

    import kalibrasyon.regresyon_satirlari as R
    taban, yeni = R._oku("k236"), R._oku("k243")
    vaka = {v[0]: v for v in R.vakalar()}[VAKA]
    t0 = time.time()
    satir = json.loads(json.dumps(R._kos(vaka), default=list))
    da, db, dy = (R._duzlestir(taban[VAKA]), R._duzlestir(satir),
                  R._duzlestir(yeni[VAKA]))
    fark = sorted(a for a in set(da) | set(db)
                  if da.get(a, "<yok>") != db.get(a, "<yok>"))
    print(f"{VAKA}")
    print(f"süre {time.time() - t0:.0f} s · gecerli="
          f"{satir['korunum']['gecerli']}")
    print(f"eski görüş hattı modeliyle k236'ya göre farklı alan: {len(fark)}")
    for a in fark:
        print(f"    {a} | {str(da.get(a, '<yok>'))[:40]} -> "
              f"{str(db.get(a, '<yok>'))[:40]}")
    print(f"pdr_pencere · k236 {da.get('metrikler.pdr_pencere')} · eski "
          f"modelle {db.get('metrikler.pdr_pencere')} · k243 "
          f"{dy.get('metrikler.pdr_pencere')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
