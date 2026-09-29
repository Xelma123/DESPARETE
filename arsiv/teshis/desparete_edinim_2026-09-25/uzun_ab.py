"""K-167 §4 — K-1'in düzeltme adayı (V8 · V9) uzun pencerede, dört profil.

Üretici: PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python -u arsiv/teshis/desparete_edinim_2026-09-25/uzun_ab.py
Küçük dünya (14 düğüm, tests2 KUCUK), yere toplama, C, 300 s (ısınma 60 ·
ölçüm 60–240 · boşalma 60); GELİŞTİRME tohumları 1003–1005 (U1'in
1000–1002'si değil); `bagimsiz-yok` · `formasyon-yok`.
Profiller AÇIKÇA verilir: bayraklar hep PROFIL_V02 ·
  v02  = SECENEK_YOK · v03 = SECENEK_V03 ·
  v03+V8 = SECENEK_V03 + istek_tanidik · v03+V8V9 = SECENEK_V03_EDINIM.

Gözlem yalnız OKUR: alt sınıf her düğümün kendi kancasında, 10 s'lik
sınırı geçince kendi durumunu (geçit alanı durumu · ACTIVE komşu sayısı ·
güvenli aday sayısı · açlık) kaydeder. Kararlar değişmez.
"""
import sys
import time
from collections import Counter
from dataclasses import replace
from multiprocessing import Pool

sys.path.insert(0, ".")
sys.path.insert(0, "tests2")

BITIS, ISINMA, OLCUM = 300.0, 60.0, 240.0
KOLLAR = ("bagimsiz-yok", "formasyon-yok")
TOHUMLAR = (1003, 1004, 1005)
PROFILLER = ("v02", "v03", "v03+V8", "v03+V8V9")
DILIM_S = 30.0
ORNEK_S = 10.0


def _secenek(profil):
    from protokoller.desparete_bayrak import (SECENEK_V03, SECENEK_V03_EDINIM,
                                              SECENEK_V04, SECENEK_YOK)
    return {"v02": SECENEK_YOK, "v03": SECENEK_V03,
            "v03+V8": replace(SECENEK_V03, istek_tanidik=True),
            "v03+V8V9": SECENEK_V03_EDINIM,
            "v03+V8V10": SECENEK_V04}[profil]


def kos(is_):
    kol, tohum, profil = is_
    from test_kosum import KUCUK
    from protokoller.desparete import DESPARETE
    from protokoller.desparete_bayrak import PROFIL_V02
    from protokoller.desparete_alan import FORWARDABLE
    from sim2.kosum.kosu import Kosu
    from sim2.kosum.kurulum import kurulum_yap
    from sim2.kosum.sonuc import sonuc_satiri
    from sim2.yapilandirma.konfig import Konfig
    kfg = Konfig(kol="k167", senaryo=kol, tohum=tohum,
                 trafik_deseni="yere_toplama", isinma_s=ISINMA,
                 olcum_bitis_s=OLCUM, kosu_bitis_s=BITIS, **KUCUK)
    sec = _secenek(profil)
    t0 = time.perf_counter()
    kur = kurulum_yap(kfg)
    g = kfg.gecit
    ornek: dict = {}                 # (dilim, düğüm) → (durum, aktif, aday, açlık)

    class Gozlemci(DESPARETE):
        __slots__ = ("_sonraki",)

        def _ornekle(self, gozlem):
            t = float(gozlem.saat_s)
            try:
                sonraki = self._sonraki
            except AttributeError:
                sonraki = self._sonraki = 0.0
            while t >= sonraki:
                a = self.alanlar.alanlar.get(g)
                aday = (len(self.alanlar._guvenli_adaylar(a, t))
                        if a is not None and not a.kendi and a.dfsn is not None
                        else 0)
                ornek[(int(sonraki // ORNEK_S), self.kimlik)] = (
                    None if a is None else a.durum,
                    len(self.komsular.aktifler()), aday,
                    self.alanlar.aclik_mi(g, t))
                sonraki += ORNEK_S
            self._sonraki = sonraki

        def uyandi(self, gozlem, etiket):
            self._ornekle(gozlem)
            return super().uyandi(gozlem, etiket)

        def kontrol_alindi(self, gozlem, gonderen, bicim, yuk, yayin):
            self._ornekle(gozlem)
            return super().kontrol_alindi(gozlem, gonderen, bicim, yuk, yayin)

    kosu = Kosu(kur, lambda i: Gozlemci(i, g, bayraklar=PROFIL_V02,
                                        secenekler=sec))
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "k167")
    m = satir["metrikler"]
    p = [d.protokol for d in kosu.dugumler]
    top = lambda ad: sum(q._sayac[ad] for q in p)
    # doğuma göre dilimli teslim
    dogan, teslim = Counter(), Counter()
    for _k, _a, d in kur.paket_defteri.dogumlar():
        dogan[int(d // DILIM_S)] += 1
    for tk in kur.paket_defteri.kayitlar():
        teslim[int(tk.dogum_s // DILIM_S)] += 1
    dilim_pdr = tuple(round(teslim[i] / dogan[i], 3) if dogan[i] else None
                      for i in range(int(BITIS // DILIM_S)))
    # 30 s'lik dilimde röle düğümlerin (geçit hariç) ortalama durumu
    dilim_dur = []
    for i in range(int(BITIS // DILIM_S)):
        s = [v for (o, n), v in ornek.items()
             if n != g and int(o * ORNEK_S // DILIM_S) == i]
        if not s:
            dilim_dur.append(None)
            continue
        ilet = sum(1 for d, *_ in s if d == FORWARDABLE) / len(s)
        aktif = sum(v[1] for v in s) / len(s)
        aday = sum(v[2] for v in s) / len(s)
        aclik = sum(1 for v in s if v[3]) / len(s)
        dilim_dur.append((round(ilet, 2), round(aktif, 1), round(aday, 2),
                          round(aclik, 2)))
    kv = (m.get("kontrol_airtime_s") or 0.0) / (m.get("veri_airtime_s") or 1e-9)
    return {
        "is": is_, "sure_s": round(time.perf_counter() - t0),
        "gecerli": satir["korunum"]["gecerli"],
        "pdr_pencere": round(m["pdr_pencere"], 4), "pdr": round(m["pdr"], 4),
        "kv": round(kv, 3), "p95": m.get("gecikme_p95_s"),
        "gecit_hedefte": p[g]._sayac["hedefte_istek"],
        "gecit_tur": p[g].alanlar.sayac["tur_artirildi"],
        "ulasilamaz": sum(q.alanlar.sayac["ulasilamaz"] for q in p),
        "onarim": sum(q.alanlar.sayac["onarima_girdi"] for q in p),
        **{ad: top(ad) for ad in ("istek_gonderilen", "istek_iletilen",
                                  "istek_aktif_disi", "istek_tanidik_kabul",
                                  "solicit_gonderilen", "solicit_yanitlanan",
                                  "soru_nitelik", "istek_aclik",
                                  "hedefte_aclik")},
        "probe_nitelik": sum(q.komsular.sayac["probe_nitelik"] for q in p),
        "probe_olcum": sum(q.komsular.sayac["probe_olcum"] for q in p),
        "dilim_pdr": dilim_pdr, "dilim_durum": dilim_dur,
    }


if __name__ == "__main__":
    # argüman verilirse yalnız o profiller (K-167 §6: `v03+V8V10 v03+V8`)
    secilen = tuple(sys.argv[1:]) or PROFILLER
    isler = [(k, t, pr) for k in KOLLAR for t in TOHUMLAR for pr in secilen]
    # uzun (v0.2) işler önce
    isler.sort(key=lambda g: g[2] != "v02")
    t0 = time.perf_counter()
    with Pool(8) as havuz:
        for r in havuz.imap_unordered(kos, isler):
            print(r, flush=True)
    print(f"duvar {time.perf_counter() - t0:.0f} s")
