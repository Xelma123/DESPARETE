"""AOMDV değişmez denetimi — kapanış paketinden ÖNCE (22 Eylül 2026).

Her kancadan sonra düğümün kendi durumunu denetler; ihlal SAYILIR, koşu
durmaz. Protokolün davranışını DEĞİŞTİRMEZ (yalnız okur).

  D1 geçerli girdinin en az bir yolu var       D2 geçersiz girdinin yolu yok
  D3 geçerli girdinin her yolunun sonraki atlaması `_komsu`da
  D4 hedefin kendisinden geçen yol 1 atlamalı  D5 düğüm kendine rota tutmaz
  D6 bir düğüm aynı RREP anahtarını (kaynak, hedef, sıra) en çok 20 kez iletir
     — aşarsa RREP bir döngüde dönüyor demektir

Kullanım: `python degismez_denetimi.py kucuk` (küçük dünya, statik + hareketli,
60 s) · `python degismez_denetimi.py tam` (N = 40, dört `-yok` kolu, kısa
pencere 10/40/50 s — U1 aletinin duman penceresi).
"""
import sys
import time
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KOK))
sys.path.insert(0, str(KOK / "tests2"))

from protokoller.aomdv import AOMDV  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.kosum.sonuc import sonuc_satiri  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402


class Denetimli(AOMDV):
    def __init__(self, kimlik):
        super().__init__(kimlik)
        self.ihlal = Counter()
        self.rrep_ilet = Counter()

    def _denetle(self):
        for h, r in self._rota.items():
            if h == self.kimlik:
                self.ihlal["D5"] += 1
            if r.gecerli:
                if not r.yollar:
                    self.ihlal["D1"] += 1
                for s, a in r.yollar.items():
                    if s not in self._komsu:
                        self.ihlal["D3"] += 1
                    if s == h and a != 1:
                        self.ihlal["D4"] += 1
            elif r.yollar:
                self.ihlal["D2"] += 1

    def _rrep_isle(self, gonderen, y, simdi):
        n = super()._rrep_isle(gonderen, y, simdi)
        for x in n:
            if getattr(x, "bicim", None) is not None and x.bicim.ad == "RREP":
                k = (y["kaynak"], y["hedef"], y["hedef_sira"])
                self.rrep_ilet[k] += 1
                if self.rrep_ilet[k] == 21:
                    self.ihlal["D6"] += 1
        return n


def _sar(ad):
    asil = getattr(AOMDV, ad)

    def kanca(self, *a, **k):
        n = asil(self, *a, **k)
        self._denetle()
        return n
    setattr(Denetimli, ad, kanca)


for _ad in ("kontrol_alindi", "sonraki_atlama", "iletim_basarisiz",
            "zamanlayici_doldu", "uyandi"):
    _sar(_ad)


def _is(gorev):
    tur, senaryo, tohum = gorev
    t0 = time.perf_counter()
    if tur == "kucuk":
        from test_kosum import _konfig
        kfg = _konfig(senaryo, tohum, 60.0)
    else:
        kfg = Konfig(kol="u1", senaryo=senaryo, tohum=tohum, isinma_s=10.0,
                     olcum_bitis_s=40.0, kosu_bitis_s=50.0)
    kur = kurulum_yap(kfg)
    kosu = Kosu(kur, Denetimli)
    kosu.kostur()
    s = sonuc_satiri(kur, kosu.dugumler, "d")
    ihlal, top = Counter(), Counter()
    for d in kosu.dugumler:
        ihlal.update(d.protokol.ihlal)
    for t in s["teshis"]["dugum"]:
        for a, v in t.items():
            if isinstance(v, (int, float)):
                top[a] += v
    return (tur, senaryo, tohum, s["metrikler"]["pdr"], s["korunum"]["gecerli"],
            s["korunum"]["dusen"], dict(ihlal),
            {a: top[a] for a in ("yedek_yola_gecis", "rreq_yeni_yol",
                                 "rrep_iletilen", "cok_yollu_girdi")},
            time.perf_counter() - t0)


if __name__ == "__main__":
    tur = sys.argv[1] if len(sys.argv) > 1 else "kucuk"
    kollar = (("statik-yok", "bagimsiz-yok") if tur == "kucuk" else
              ("statik-yok", "bagimsiz-yok", "gorev-yok", "formasyon-yok"))
    gorevler = [(tur, k, 1000) for k in kollar]
    with Pool(len(gorevler)) as havuz:
        sonuc = havuz.map(_is, gorevler, chunksize=1)
    toplam = Counter()
    for tur_, k, t, pdr, gecerli, dusen, ihlal, ek, sure in sonuc:
        toplam.update(ihlal)
        print(f"{tur_:<6}{k:<15}{t}  pdr {pdr:.4f}  gecerli {gecerli}  "
              f"ihlal {ihlal or 0}  {ek}  {sure:.0f} s")
        print(f"      dusen {dusen}")
    print("TOPLAM IHLAL:", dict(toplam) or 0)
    raise SystemExit(1 if toplam else 0)
