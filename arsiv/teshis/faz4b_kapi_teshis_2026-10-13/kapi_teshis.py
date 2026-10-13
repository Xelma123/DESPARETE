"""G1ç ve G4ç'nin JarmRout yüzünden kalması — sebebin teşhisi.

Beklenti `arsiv/teshis/faz4b_kapanis2_2026-10-12/beklenti.md` (C): "JarmRout
yüzünden kalırsa sebep ölçülür ve yürütücüye bildirilir". Salt okur: simülatörün
ve protokolün kodu değişmez, sarmalar yalnız sayar (RNG'ye ve dönüş değerine
dokunmaz).

Hücre G1ç'ninki: formasyon-yok · yere toplama · hayalet çizelge (`evre_kapi_c`).
Koşu `evre_metrikleri_kapilari._ciz_is`in kendisidir; satırın alanları
`G1c.txt`deki KAYIT'la birebir olmalı, değilse teşhis geçersiz.

Ölçülen:
  1. gecikme — teslim edilen her pencere paketinin rota bekleyişi (doğumdan
     rota tamponundan son çıkışa) ve kalanı (yol); p99 kuyruğu
  2. keşif süresi — kaynakta keşfin başlangıcından ilk RREP'e
  3. zaman dizisi (5 s kova) — doğum, doğumuna göre teslim, RREQ üretimi ve
     yeniden yayını, RERR, tampon girişi, düşüş sebepleri
  4. 15 s pencere PDR'sinin oynaklığı — TEMİZ'deki s_L (kapının kullandığı),
     bütün koşudaki dağılım, blok ortalamalarının ölçek yasası, özilinti ve
     RREQ yeniden yayınıyla ilinti

    (dondurulmuş kopyanın içinden)
    py -3.11 -u <yol>/kapi_teshis.py <tohum> [<tohum> ...] --kayit <dosya>
"""
import json
import statistics as ist
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

# Kod ÇALIŞMA DİZİNİNDEN alınır: teşhis dondurulmuş kopyanın içinden koşar.
sys.path.insert(0, str(Path.cwd()))
import kalibrasyon.evre_metrikleri_kapilari as EMK  # noqa: E402
import protokoller.jarmrout as J  # noqa: E402
from sim2.kosum.dugum import Dugum  # noqa: E402

KOVA_S = 5.0
L_S = 15.0
KUR: list = []
tampon_ilk: dict[int, float] = {}
tampon_son: dict[int, float] = {}
kesif_bas: dict[tuple[int, int], float] = {}
kesif_sure: list[tuple[float, float]] = []
seri: dict[str, Counter] = defaultdict(Counter)


def simdi() -> float:
    return KUR[-1].olaylar.simdi


def kova(t: float) -> int:
    return int(t // KOVA_S)


_o_kur = EMK.kurulum_yap


def _kurulum_yap(kfg):
    k = _o_kur(kfg)
    KUR.append(k)
    return k


EMK.kurulum_yap = _kurulum_yap

_o_bek = Dugum.beklemeye_al


def _beklemeye_al(self, paket, t_s, olaylar):
    tampon_ilk.setdefault(paket.kimlik, t_s)
    seri["tampon_giris"][kova(t_s)] += 1
    return _o_bek(self, paket, t_s, olaylar)


Dugum.beklemeye_al = _beklemeye_al

_o_dok = Dugum.tamponu_kuyruga_dok


def _tamponu_kuyruga_dok(self):
    once = {p.kimlik for p in self.bekleyenler}
    r = _o_dok(self)
    if once:
        t = simdi()
        for k in once - {p.kimlik for p in self.bekleyenler}:
            tampon_son[k] = t
    return r


Dugum.tamponu_kuyruga_dok = _tamponu_kuyruga_dok

_o_dus = Dugum.dus


def _dus(self, sebep, nereden):
    seri["dus:" + sebep][kova(simdi())] += 1
    return _o_dus(self, sebep, nereden)


Dugum.dus = _dus

_o_rg = J.JarmRout._rreq_gonder


def _rreq_gonder(self, hedef):
    seri["rreq_uretim"][kova(simdi())] += 1
    return _o_rg(self, hedef)


J.JarmRout._rreq_gonder = _rreq_gonder

_o_ri = J.JarmRout._rreq_isle


def _rreq_isle(self, gozlem, gonderen, y):
    n = self._sayac["rreq_iletilen"]
    r = _o_ri(self, gozlem, gonderen, y)
    if self._sayac["rreq_iletilen"] > n:
        seri["rreq_ilet"][kova(simdi())] += 1
    return r


J.JarmRout._rreq_isle = _rreq_isle

_o_ib = J.JarmRout.iletim_basarisiz


def _iletim_basarisiz(self, *a, **k):
    n = self._sayac["rerr_uretilen"]
    r = _o_ib(self, *a, **k)
    if self._sayac["rerr_uretilen"] > n:
        seri["rerr"][kova(simdi())] += 1
    return r


J.JarmRout.iletim_basarisiz = _iletim_basarisiz

_o_kb = J.JarmRout._kesif_baslat


def _kesif_baslat(self, hedef, simdi_):
    if hedef not in self._kesif:
        kesif_bas[(self.kimlik, hedef)] = simdi()
    return _o_kb(self, hedef, simdi_)


J.JarmRout._kesif_baslat = _kesif_baslat

_o_rr = J.JarmRout._rrep_isle


def _rrep_isle(self, y, simdi_):
    if y["ip_hedef"] == self.kimlik:
        d = y["yol"][-1]
        if d in self._kesif and (self.kimlik, d) in kesif_bas:
            t0 = kesif_bas.pop((self.kimlik, d))
            kesif_sure.append((t0, simdi() - t0))
    return _o_rr(self, y, simdi_)


J.JarmRout._rrep_isle = _rrep_isle


def _yuzde(x: list[float], q: float) -> float | None:
    if not x:
        return None
    x = sorted(x)
    return x[min(len(x) - 1, int(q / 100.0 * len(x)))]


def _ilinti(a: list[float], b: list[float]) -> float | None:
    if len(a) < 3 or ist.pstdev(a) == 0 or ist.pstdev(b) == 0:
        return None
    ma, mb = ist.fmean(a), ist.fmean(b)
    return (sum((x - ma) * (y - mb) for x, y in zip(a, b))
            / (len(a) * ist.pstdev(a) * ist.pstdev(b)))


def _pencere_pdr(dogan: dict, teslim: dict, a: float, b: float):
    n = sum(v for t, v in dogan.items() if a <= t < b)
    m = sum(v for t, v in teslim.items() if a <= t < b)
    return (m / n) if n else None, n


def kos(tohum: int, ek: tuple = (), ham_yolu: str | None = None) -> dict:
    """Koşu ve HAM veri — analizden önce diske yazılır (analizdeki bir hata
    saatlik koşuyu boşa harcatmasın). `ek` yalnız duman sınaması için."""
    t0 = time.perf_counter()
    satir = EMK._ciz_is(("formasyon-yok", "jarmrout", tohum, ek))
    kur = KUR[-1]
    kfg = kur.konfig
    bas, bitis = kfg.olcum_penceresi
    defter = kur.paket_defteri
    kay = [[r.kimlik, r.dogum_s, r.teslim_s] for r in defter.kayitlar(True)]
    dog = [[k, d] for k, _, d in defter.dogumlar(True)]
    pencere = {k for k, _ in dog}
    ham = {"tohum": tohum, "sure_s": round(time.perf_counter() - t0, 1),
           "satir": satir, "bas": bas, "bitis": bitis,
           "acilma": kfg.karistirici_baslangic_s,
           "kayitlar": kay, "dogumlar": dog,
           "tampon": {str(k): [tampon_ilk[k], tampon_son.get(k)]
                      for k in tampon_ilk if k in pencere},
           "kesif_sure": kesif_sure,
           "seri": {ad: dict(c) for ad, c in seri.items()}}
    if ham_yolu:
        Path(ham_yolu).write_text(json.dumps(ham), encoding="utf-8")
    return ham


def analiz(ham: dict) -> dict:
    satir = ham["satir"]
    bas, bitis, acilma = ham["bas"], ham["bitis"], ham["acilma"]
    tampon = {int(k): v for k, v in ham["tampon"].items()}
    seri_ = {ad: Counter({int(k): v for k, v in c.items()})
             for ad, c in ham["seri"].items()}

    # 1 · gecikme ayrıştırması
    gec, bek, yol_ = [], [], []
    kuyruk = []                       # gecikme ≥ L (açık süre)
    for kimlik, dogum, teslim in ham["kayitlar"]:
        g = teslim - dogum
        ilk_son = tampon.get(kimlik)
        b = (max(0.0, min(ilk_son[1], teslim) - dogum)
             if ilk_son and ilk_son[1] is not None else 0.0)
        gec.append(g)
        bek.append(b)
        yol_.append(g - b)
        if g >= L_S:
            kuyruk.append((g, b))
    tamponlu = sum(1 for k, _, _ in ham["kayitlar"] if k in tampon)
    gecikme = {
        "teslim": len(ham["kayitlar"]), "tampondan_gecen": tamponlu,
        "p50_s": _yuzde(gec, 50), "p90_s": _yuzde(gec, 90),
        "p99_s": _yuzde(gec, 99), "p99_kapi_s": satir["p99_s"],
        "yol_p99_s": _yuzde(yol_, 99), "bekleyis_p99_s": _yuzde(bek, 99),
        "gecikme_15s_ustu": len(kuyruk),
        "gecikme_15s_ustu_tampondan": sum(1 for g, b in kuyruk if b > 0),
        "gecikme_15s_ustu_bekleyis_payi_medyan":
            ist.median(b / g for g, b in kuyruk) if kuyruk else None,
    }

    # 2 · keşif süresi
    ks = [s for _, s in ham["kesif_sure"]]
    kesif = {"n": len(ks), "medyan_s": _yuzde(ks, 50), "p90_s": _yuzde(ks, 90),
             "p99_s": _yuzde(ks, 99), "en_cok_s": max(ks) if ks else None,
             "15s_ustu": sum(1 for s in ks if s >= L_S)}

    # 3 · zaman dizisi (doğum kovası)
    teslim_kimlik = {k for k, _, _ in ham["kayitlar"]}
    dogan_k, teslim_k = Counter(), Counter()
    dogan_s, teslim_s = Counter(), Counter()
    for kimlik, dogum in ham["dogumlar"]:
        dogan_k[kova(dogum)] += 1
        dogan_s[int(dogum)] += 1
        if kimlik in teslim_kimlik:
            teslim_k[kova(dogum)] += 1
            teslim_s[int(dogum)] += 1
    kovalar = list(range(kova(bas), kova(bitis)))
    tablo = {"kova_s": [k * KOVA_S for k in kovalar],
             "dogan": [dogan_k[k] for k in kovalar],
             "teslim": [teslim_k[k] for k in kovalar]}
    for ad in sorted(seri_):
        tablo[ad] = [seri_[ad][k] for k in kovalar]

    # 4 · 15 s pencere PDR'si — 1 s ızgarada kayan, doğum anına göre
    def kayan(a: float, b: float, uzunluk: float) -> list[float]:
        out = []
        t = a
        while t + uzunluk <= b + 1e-9:
            p, _ = _pencere_pdr(dogan_s, teslim_s, t, t + uzunluk)
            if p is not None:
                out.append(p)
            t += 1.0
        return out

    def sd(x: list[float]) -> float | None:
        return ist.stdev(x) if len(x) >= 2 else None

    s_l_temiz = sd(kayan(bas, acilma, L_S))
    olcek = {}
    for u in (15.0, 30.0, 60.0, 90.0):
        x = kayan(bas, bitis, u)
        olcek[str(int(u))] = {"sd": sd(x), "n_pencere": len(x)}
    sd15 = olcek["15"]["sd"]
    for u, v in list(olcek.items()):
        if v["sd"] is None or sd15 is None:
            del olcek[u]
            continue
        v["bagimsiz_beklenen"] = sd15 * (15.0 / float(u)) ** 0.5
        v["oran"] = v["sd"] / v["bagimsiz_beklenen"]
    # örtüşmeyen 15 s pencereler — özilinti ve RREQ ilintisi
    pdr15, ilet15 = [], []
    t = bas
    while t + L_S <= bitis + 1e-9:
        p, _ = _pencere_pdr(dogan_s, teslim_s, t, t + L_S)
        if p is not None:
            pdr15.append(p)
            ilet15.append(sum(seri_.get("rreq_ilet", Counter())[k]
                              for k in range(kova(t), kova(t + L_S))))
        t += L_S
    ozilinti = {str(g): _ilinti(pdr15[:-g], pdr15[g:]) for g in (1, 2, 3)}
    ort = ist.fmean(pdr15) if pdr15 else None
    oynaklik = {
        "s_L_temiz": s_l_temiz, "sd_15_tum": sd15,
        "binom_sd_15": (None if ort is None
                        else (ort * (1 - ort) / (40.0 * L_S)) ** 0.5),
        "olcek": olcek, "ozilinti_15s": ozilinti,
        "ilinti_pdr_rreq_ilet": _ilinti(pdr15, ilet15),
        "pdr_15": pdr15, "rreq_ilet_15": ilet15,
    }
    return {"tohum": ham["tohum"], "sure_s": ham["sure_s"], "satir": satir,
            "gecikme": gecikme, "kesif": kesif, "oynaklik": oynaklik,
            "tablo": tablo}


def _kos_is(is_) -> dict:
    tohum, kayit = is_
    return kos(tohum, ham_yolu=f"{kayit}.ham_{tohum}.json")


def _f(x, b: str = ".4f") -> str:
    return "—" if x is None else format(x, b)


def _ozet(r: dict) -> None:
    s, g, k, o = r["satir"], r["gecikme"], r["kesif"], r["oynaklik"]
    print(f"tohum {r['tohum']} · {r['sure_s']:.0f} s")
    print(f"  satir: temiz {_f(s['pdr_temiz'])} · acik {_f(s['pdr_acik'])} · "
          f"sessiz {_f(s['pdr_sessiz'])} · D {_f(s['d'], '+.4f')} (2 SE "
          f"{_f(s['d_se'] and 2 * s['d_se'])}) · M1 {_f(s['sok'], '+.4f')} · "
          f"p99 {_f(s['p99_s'], '.3f')} · sizinti {_f(s['sizinti'])}")
    print(f"  gecikme: teslim {g['teslim']} · tampondan gecen "
          f"{g['tampondan_gecen']} · p50 {_f(g['p50_s'], '.3f')} · p90 "
          f"{_f(g['p90_s'], '.3f')} · p99 {_f(g['p99_s'], '.3f')} · yol p99 "
          f"{_f(g['yol_p99_s'], '.3f')} · bekleyis p99 "
          f"{_f(g['bekleyis_p99_s'], '.3f')}")
    print(f"  gecikme >= 15 s: {g['gecikme_15s_ustu']} paket · tampondan "
          f"{g['gecikme_15s_ustu_tampondan']} · bekleyis payi medyan "
          f"{_f(g['gecikme_15s_ustu_bekleyis_payi_medyan'], '.3f')}")
    print(f"  kesif: n {k['n']} · medyan {_f(k['medyan_s'], '.2f')} · p90 "
          f"{_f(k['p90_s'], '.2f')} · p99 {_f(k['p99_s'], '.2f')} · en cok "
          f"{_f(k['en_cok_s'], '.2f')} · >= 15 s {k['15s_ustu']}")
    print(f"  oynaklik: s_L temiz {_f(o['s_L_temiz'])} · 15 s SD (tum) "
          f"{_f(o['sd_15_tum'])} · binom SD {_f(o['binom_sd_15'])}")
    for u, v in o["olcek"].items():
        print(f"    blok {u:>2} s: SD {_f(v['sd'])} · bagimsizsa "
              f"{_f(v['bagimsiz_beklenen'])} · oran {_f(v['oran'], '.2f')}")
    oz = {g_: _f(v, "+.2f") for g_, v in o["ozilinti_15s"].items()}
    print(f"    ozilinti (15/30/45 s): {oz} · ilinti(PDR, RREQ yeniden "
          f"yayini) {_f(o['ilinti_pdr_rreq_ilet'], '+.2f')}")
    print("    15 s PDR: " + " ".join(f"{p:.2f}" for p in o["pdr_15"]))
    print("    15 s RREQ yeniden yayini: "
          + " ".join(map(str, o["rreq_ilet_15"])))


if __name__ == "__main__":
    # Kip: `<tohum> ... --kayit <dosya>` koşar; `--analiz <ham.json> ...`
    # yalnız kayıtlı ham veriyi yeniden analiz eder.
    import traceback
    from multiprocessing import Pool
    arg = sys.argv[1:]
    if arg and arg[0] == "--analiz":
        hamlar = [json.loads(Path(a).read_text(encoding="utf-8"))
                  for a in arg[1:]]
        kayit = None
    else:
        kayit = arg[arg.index("--kayit") + 1]
        tohumlar = [int(a) for a in arg[:arg.index("--kayit")]]
        with Pool(len(tohumlar)) as havuz:
            hamlar = havuz.map(_kos_is, [(t, kayit) for t in tohumlar],
                               chunksize=1)
    sonuc = []
    for h in hamlar:
        try:
            r = analiz(h)
            _ozet(r)
            sonuc.append(r)
        except Exception:
            print(f"tohum {h['tohum']}: ANALIZ HATASI (ham veri diskte)")
            traceback.print_exc()
    if kayit:
        Path(kayit).write_text(json.dumps(sonuc, ensure_ascii=False),
                               encoding="utf-8")
