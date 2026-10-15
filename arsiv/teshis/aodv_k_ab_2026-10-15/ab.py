"""AODV-k'nin U1 düşüşü — hangi değişiklik? (K-244 kuyruğu, yere toplama)

Varyantlar (her biri AODV-k'nin TEK bir değişikliğini geri alır; `j` eski
kodun tamamı, git `e5cd1b7~1`):
    k              AODV-k (K-243 · K-244)
    j              AODV-j (K-242'den önceki kod)
    g_yok          G bayrağı ve karşılıksız RREP yok (K-244)
    rerr_yayin     RERR her zaman yayın (K-244 öncesi teslim biçimi)
    dusurme_yok    başarısız keşfin tamponu düşmez (K-242)
    mrt_6          MY_ROUTE_TIMEOUT 6 s (K-242 öncesi)
    titresim_yok   yayın titreşimi yok (K-242)
§6.2 önceki atlama tazelemesi ayrıca geri alınmaz: `j` ile öteki varyantların
farkından okunur.

Hücreler U1'in yapılandırmasıyla (`aodv_uygunluk._is`): referans dünya, yere
toplama, `statik-yok` 1000 · 1001 · 1002, tam pencere. Kâhin PDR'leri K-244
kuyruğunun U1 kaydından. Ölçüt ve yorum kuralı `beklenti.md`de.

    KOK=<donmuş kopya> py -3.11 -u arsiv/teshis/aodv_k_ab_2026-10-15/ab.py
"""
from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys
import tempfile
import time
from multiprocessing import Pool

ANA = pathlib.Path(__file__).resolve().parents[3]
KOK = pathlib.Path(os.environ.get("KOK") or ANA)
BURA = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(KOK))
os.environ["DESPARETE_DUNYA"] = "referans_2026"

VARYANTLAR = ("k", "j", "g_yok", "rerr_yayin", "dusurme_yok", "mrt_6",
              "titresim_yok")
HUCRELER = (("statik-yok", 1000), ("statik-yok", 1001), ("statik-yok", 1002))
KAHIN = {("statik-yok", 1000): 0.9905, ("statik-yok", 1001): 0.9868,
         ("statik-yok", 1002): 0.9945}
SAYACLAR = ("rreq_uretilen", "rreq_iletilen", "rrep_uretilen",
            "rrep_iletilen", "rerr_uretilen", "rerr_tek_yayin",
            "rrep_karsiliksiz", "kesif_basarisiz", "kesif_basarisiz_dusen",
            "kara_liste_eklenen", "komsu_zaman_asimi",
            "rota_gecersizlestirilen")


def _aodv_j():
    """AODV-j: git `e5cd1b7~1`deki `aodv.py` ve `aodv_bicim.py`."""
    d = pathlib.Path(tempfile.mkdtemp())
    (d / "aodvj").mkdir()
    (d / "aodvj" / "__init__.py").write_text("")
    for ad in ("aodv.py", "aodv_bicim.py"):
        kaynak = subprocess.run(
            ["git", "show", f"e5cd1b7~1:protokoller/{ad}"], cwd=ANA,
            check=True, capture_output=True).stdout.decode("utf-8")
        kaynak = kaynak.replace("from protokoller.aodv_bicim import",
                                "from aodvj.aodv_bicim import")
        (d / "aodvj" / ad).write_text(kaynak, encoding="utf-8")
    sys.path.insert(0, str(d))
    from aodvj.aodv import AODV
    return AODV


def _rerr_yayin(self, hedefler, simdi_s, oncul_suz=True, veri_kaynagi=None):
    """K-244 öncesi `_rerr_kur`: RERR her zaman yayın."""
    import protokoller.aodv as A
    onculu = (tuple(h for h in hedefler
                    if h in self._rota and self._rota[h].oncular)
              if oncul_suz else tuple(hedefler))
    self._sayac["rerr_onculsuz"] += len(hedefler) - len(onculu)
    hedefler = onculu
    if not hedefler or self._hiz_sinirli_mi(self._rerr_pencere,
                                            A.RERR_RATELIMIT, simdi_s):
        return ()
    siralar = tuple(self._rota[h].hedef_sira if h in self._rota
                    else A.SONSUZ_SIRA for h in hedefler)
    self._sayac["rerr_uretilen"] += 1
    self._son_yayin_s = simdi_s
    return (A.KontrolIstegi.kur(None, A.RERR,
                                jitter_s=A.YAYIN_TITRESIMI_S, yuk={
        "tip": A.TIP_RERR, "bayraklar": 0, "ayrilmis": 0,
        "hedef_sayisi": len(hedefler), "ulasilamaz": hedefler,
        "ulasilamaz_sira": siralar}),)


def _sinif(v: str):
    if v == "j":
        return _aodv_j()
    import protokoller.aodv as A
    if v == "g_yok":
        A.BAYRAK_G = 0
    elif v == "mrt_6":
        A.MY_ROUTE_TIMEOUT_S = 6.0
    elif v == "titresim_yok":
        A.YAYIN_TITRESIMI_S = 0.0
    elif v == "rerr_yayin":
        A.AODV._rerr_kur = _rerr_yayin
    elif v == "dusurme_yok":
        eski = A.AODV.uyandi

        def uyandi(self, gozlem, etiket):
            r = eski(self, gozlem, etiket)
            self._dusurulecek.clear()
            return r
        A.AODV.uyandi = uyandi
    return A.AODV


def _is(gorev):
    v, kol, t = gorev
    t0 = time.perf_counter()
    try:
        from kalibrasyon import dunya_secimi as DS
        from sim2.kosum.kosu import Kosu
        from sim2.kosum.kurulum import kurulum_yap
        from sim2.kosum.sonuc import sonuc_satiri
        sinif = _sinif(v)
        kfg = DS.konfig(kol="u1", senaryo=kol, tohum=t,
                        trafik_deseni="yere_toplama")
        kur = kurulum_yap(kfg)
        kosu = Kosu(kur, lambda i: sinif(i))
        kosu.kostur()
        satir = sonuc_satiri(kur, kosu.dugumler, "u1")
        top = {s: 0 for s in SAYACLAR}
        for d in satir["teshis"]["dugum"]:
            for s in SAYACLAR:
                top[s] += d.get(s, 0)
        m = satir["metrikler"]
        return {"varyant": v, "kol": kol, "tohum": t, "pdr": m["pdr"],
                "gecerli": satir["korunum"]["gecerli"],
                "hedef_yok": m.get("hedef_yok"),
                "iletim_basarisiz": satir["korunum"]["dusen"].get(
                    "iletim_basarisiz"),
                "sayac": top, "sure_s": time.perf_counter() - t0,
                "hata": None}
    except Exception as e:                      # noqa: BLE001
        return {"varyant": v, "kol": kol, "tohum": t,
                "hata": f"{type(e).__name__}: {e}"}


def main() -> int:
    kayit = BURA / "ab.jsonl"
    bitti = set()
    if kayit.exists():
        for s in kayit.read_text(encoding="utf-8").splitlines():
            r = json.loads(s)
            if r.get("hata") is None:
                bitti.add((r["varyant"], r["kol"], r["tohum"]))
    isler = [(v, k, t) for v in VARYANTLAR for k, t in HUCRELER
             if (v, k, t) not in bitti]
    print(f"kok {KOK} · {len(isler)} kosu kaldi")
    with Pool(8, maxtasksperchild=1) as havuz:
        for r in havuz.imap_unordered(_is, isler):
            with kayit.open("a", encoding="utf-8") as f:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
            print(f"  {r['varyant']:>13} {r['kol']} {r['tohum']} · "
                  f"{'PDR %.4f' % r['pdr'] if r.get('hata') is None else r['hata']}"
                  f" · {r.get('sure_s', 0) / 60:.0f} dk", flush=True)
    sonuc = [json.loads(s) for s in kayit.read_text(encoding="utf-8").splitlines()]
    print("\nvaryant        " + "  ".join(f"{k[:6]}/{t}" for k, t in HUCRELER)
          + "   (oran = PDR / ETX kâhini)")
    for v in VARYANTLAR:
        hucre = []
        for k, t in HUCRELER:
            r = next((x for x in sonuc if x["varyant"] == v and x["kol"] == k
                      and x["tohum"] == t and x.get("hata") is None), None)
            hucre.append("   —   " if r is None else
                         f"{r['pdr'] / KAHIN[(k, t)]:.4f}")
        print(f"  {v:>13}  " + "  ".join(f"{h:>11}" for h in hucre))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
