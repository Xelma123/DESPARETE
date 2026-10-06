"""AOMDV kara deliği — paket rotası olmayan ara düğüme NASIL gidiyor?

    PYTHONIOENCODING=utf-8 py -3.11 -u arsiv/teshis/aodv_sadakat_2026-09-30/aomdv_kara_delik.py [desen] [kol] [tohum]

Her veri kararını paket başına kaydeder. Ara düğüm X'te "girdi yok" olan
paketlerde önceki düğüm U'yu ve U'nun o hedefe girdisini (yollar, sıra), U'nun
o girdiyi değiştiren son işlemlerini ve X'in o hedefe girdisinin geçmişini
(kuruldu, geçersizleşti, silindi) basar. Simülatöre dokunmaz.
"""
import collections
import os
import pathlib
import sys

KOK = pathlib.Path(__file__).resolve().parents[3]
DESEN = sys.argv[1] if len(sys.argv) > 1 else "esler_arasi"
KOL = sys.argv[2] if len(sys.argv) > 2 else "statik-yok"
TOHUM = int(sys.argv[3]) if len(sys.argv) > 3 else 1001
sys.path.insert(0, str(KOK))
os.environ["DESPARETE_DUNYA"] = "referans_2026"

from kalibrasyon import dunya_secimi as DS  # noqa: E402
from kalibrasyon.aodv_uygunluk import _fabrika  # noqa: E402
from protokoller import aodv as A  # noqa: E402
from protokoller import aomdv as M  # noqa: E402
from sim2.kosum.dugum import Dugum  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402

kfg = DS.konfig(kol="u1", senaryo=KOL, tohum=TOHUM, trafik_deseni=DESEN)
kur = kurulum_yap(kfg)


def ozet(r):
    if r is None:
        return None
    return (dict(r.yollar), r.hedef_sira, r.gecerli, round(r.son_gecerli_s, 2))


yol: dict[int, list] = collections.defaultdict(list)
gecmis: dict[tuple[int, int], list] = collections.defaultdict(list)
olay = collections.Counter()
asil_karar = Dugum.sonraki_atlama


def karar(self, paket, t_s):
    k = asil_karar(self, paket, t_s)
    yol[paket.kimlik].append((round(kur.olaylar.simdi, 3), self.kimlik,
                              paket.hedef, k.sonraki,
                              self.protokol._rota.get(paket.hedef) is None))
    return k


def sar(sinif, ad):
    asil = getattr(sinif, ad)

    def sarili(self, *a, **k):
        once = {h: ozet(r) for h, r in self._rota.items()}
        sonuc = asil(self, *a, **k)
        sonra = {h: ozet(r) for h, r in self._rota.items()}
        for h in set(once) | set(sonra):
            if once.get(h) != sonra.get(h):
                gecmis[(self.kimlik, h)].append(
                    (round(kur.olaylar.simdi, 3), ad, once.get(h), sonra.get(h)))
        return sonuc
    setattr(sinif, ad, sarili)


for ad in ("_rreq_isle", "_rrep_isle", "_rerr_isle", "_komsu_rotasi",
           "_bag_koptu", "_bakim", "sonraki_atlama"):
    sar(M.AOMDV if hasattr(M.AOMDV, ad) and ad in M.AOMDV.__dict__ else A.AODV, ad)
Dugum.sonraki_atlama = karar
Kosu(kur, _fabrika("aomdv", kfg)).kostur()

# --- girdi yok olayları: önceki düğüm ve geçmiş ----------------------------
ornek = 0
sayac = collections.Counter()
for pk, v in yol.items():
    for i, (t, x, h, s, girdisiz) in enumerate(v):
        if not girdisiz or i == 0:
            continue
        u = v[i - 1][1]
        sayac[(u, x, h)] += 1
        if sayac[(u, x, h)] > 1 or ornek >= 5:
            continue
        ornek += 1
        print(f"\n=== paket {pk} · t {t} · U {u} → X {x} · hedef {h}")
        print(f"  U'nun girdisi (son 4 değişiklik ≤ t):")
        for e in [e for e in gecmis[(u, h)] if e[0] <= t][-4:]:
            print(f"     {e[0]:>8} {e[1]:<14} {e[2]} → {e[3]}")
        print(f"  X'in girdisi (son 4 değişiklik ≤ t):")
        for e in [e for e in gecmis[(x, h)] if e[0] <= t][-4:]:
            print(f"     {e[0]:>8} {e[1]:<14} {e[2]} → {e[3]}")
print(f"\ngirdi yok olayı {sum(sayac.values())} · ayrı (U, X, hedef) {len(sayac)}")
print("en sık:", sayac.most_common(8))
