"""
Faz 5-3 · B3 TEŞHİSİ — bağın iki ölçüsü aynı bağda, bizim çekirdeğimizin
trafiğinde (`beklenti.md`). Ölçüm aleti; protokolün parçası değildir.

    cd <kod kökü: dondurulmuş kopya ya da depo kökü>
    PYTHONIOENCODING=utf-8 py -3.11 -u <bu dosya> --dunya referans_2026 \
        --hucre ikiz|birincil --tohumlar 1003,…,1010 --isci 8 \
        --kayit <yol.json.gz> [--kisa]

Kod ÇALIŞMA DİZİNİNDEN içe aktarılır (`kosu.sh` dondurulmuş kopyaya geçer);
saf işlevler (`bag.py`) bu dosyanın dizininden. Hangi dosyadan geldikleri
çıktının başına yazılır.

🔒 KOŞU AYNI KOŞUDUR. Her koşu kayıp anatomisi aletinin işçisiyle
(`kalibrasyon/kayip_anatomisi.py::_is`) olduğu gibi yapılır; kol ve hücre
tanımları B2 teşhisininkiyle aynı. Kaydedici simülatörün ve protokolün
yöntemlerine YALNIZ OKUYAN sarmalayıcılar takar, koşudan sonra geri alır. Tek
ek: düğümlerin kanal meşgul integrali açılır (`Dugum._doluluk`; B2 teşhisinde
birebir olduğu denetlendi). Denetim (`beklenti.md` K0): satırlar B2 teşhisinin
satırlarıyla (aynı kod, aynı tohum) birebir.

🔒 KOL: `desparete5_cekirdek` (karıştırmaya karşı mekanizmalar kapalı; geri
gönderme yasağı ve sınırlı yükselme açık).

🔒 HÜCRELER (`formasyon · yere_toplama`, tam pencere)
    ikiz      karıştırıcısız (`--sinif yok`), hayalet çizelge 10:20
    birincil  `derin_sizma`, 15 s açık · 15 s sessiz

🔒 KAYDEDİLENLER (simülatörün saati; kâhin, evre ve etki alanı yalnız
değerlendirmede, `05` §8)
    veri örneği — her bağda (gönderen i → alıcı j), ölçüm penceresinin her tam
        saniyesindeki İLK veri kaydında: B1'in selam ölçüsü (d_r, n_s, d_f;
        kayıttan önceki olaylarla) · önceki veri kayıtları (en çok 16, son
        30 s; kodlu) ve en yenisinin yaşı · sonraki veri kayıtları (bu kayıt
        dâhil en çok 16, 30 s içinde; kodlu) · kâhinin tek deneme başarısı
        (5 s'lik dilimin ortasında; kayıp anatomisinin ölçüsü) · göndericinin
        ve alıcının son 10 s'deki kanal meşgul payı · evre · alıcının alanı.
    ızgara örneği — her 5 s'lik dilimin ortasında, B1'de kayıtlı her bağ için:
        B1'in selam ölçüsü · önceki veri kayıtları (son 30 s) · kâhinin tek
        deneme başarısı · evre · alıcının alanı.

İç denetimler: dilimlere yazılan meşgul süresi düğümlerin toplamına, MAC
sonucu sayısı simülatörün sayacına eşit; selam alındı; veri örneği var.

⚠️ Ana deney tohumları (2000–2039) KOŞULMAZ.
"""

from __future__ import annotations

import bisect
import gzip
import json
import math
import os
import sys
import time
from collections import defaultdict
from multiprocessing import Pool
from pathlib import Path

# Kod çalışma dizininden (dondurulmuş kopya); saf işlevler bu dizinden.
if os.getcwd() not in sys.path[:1]:
    sys.path.insert(0, os.getcwd())
BURASI = Path(__file__).resolve().parent
if str(BURASI) not in sys.path:
    sys.path.insert(1, str(BURASI))

import bag as B  # noqa: E402

ETIKET = "desparete5_cekirdek"
# hücre → (sınıf, aile, hayalet çizelge, konfig farkı) — B2 teşhisinin tanımı
HUCRE = {
    "ikiz": ("yok", "derin_sizma", "10:20", ""),
    "birincil": ("surekli", "derin_sizma", "", ""),
}
YUK_S = 10                    # göndericinin ve alıcının yükü: son 10 s


def _dagit(tablo: dict, anahtar: int, bas: float, bitis: float) -> None:
    """[bas, bitis) aralığını 1 s'lik dilimlere oranla böler."""
    if bitis <= bas:
        return
    k = int(math.floor(bas))
    while bas < bitis:
        sinir = min(bitis, float(k + 1))
        tablo[(anahtar, k)] += sinir - bas
        bas = sinir
        k += 1


def _bin(x: float | None) -> int:
    return -1 if x is None else int(round(1000.0 * x))


class Kaydedici:
    """Bir koşunun kaydı. `tak()` sarmalayıcıları takar, dönen işlev geri
    alır."""

    def __init__(self) -> None:
        self.kur = None
        self.kosu = None
        self.mesgul: defaultdict = defaultdict(float)   # (düğüm, dilim) → s
        self.mac: list = []          # (gönderen, alıcı, onay, deneme, t, tür)
        self.selam_al: list = []     # (alıcı, gönderen, t, sıra, aralık, oran)

    # ------------------------------------------------------------------
    def tak(self):
        import sim2.kosum.kurulum as KM
        from protokoller.desparete5 import Desparete5
        from protokoller.desparete5_bicim import SELAM_E
        from protokoller.desparete5_selam import selam_coz
        from sim2.kosum import kontrol
        from sim2.kosum.dugum import Dugum
        from sim2.kosum.kosu import Kosu

        k = self
        asil = {
            "kurulum": KM.kurulum_yap, "kostur": Kosu.kostur,
            "mesgul": Dugum.mesgul_guncelle,
            "sonuc": kontrol.iletim_sonucu,
            "kontrol": Desparete5.kontrol_alindi,
        }

        def kurulum_yap(*a, **kw):
            kur = asil["kurulum"](*a, **kw)
            k.kur = kur
            return kur

        def kostur(self):
            k.kosu = self
            for d in self.dugumler:
                d._doluluk = True
            sonuc = asil["kostur"](self)
            for d in self.dugumler:
                d.mesgul_guncelle(self.kur.konfig.kosu_bitis_s)
            return sonuc

        def mesgul_guncelle(self, t_s):
            """`Dugum.mesgul_guncelle`in AYNISI (B2 teşhisinin sarmalayıcısı);
            meşgul parçalar dilimlere de yazılır."""
            if not self._doluluk:
                return
            bas = self._mesgul_son_s
            if t_s <= bas:
                return
            self._mesgul_son_s = t_s
            sinirlar = {bas, t_s}
            kr = self.kur.kanal.karistirici
            if kr is not None:
                sinirlar.update(kr.gecis_anlari(bas, t_s))
                if kr.hareketli:
                    adim = self.kur.konfig.karistirici_denetim_araligi_s
                    sinirlar.update(bas + i * adim for i in
                                    range(1, int((t_s - bas) / adim) + 1))
            s = sorted(a for a in sinirlar if bas <= a <= t_s)
            for a, b in zip(s, s[1:]):
                if b > a and self.kanal_mesgul_mu(0.5 * (a + b)):
                    self._mesgul_toplam_s += b - a
                    _dagit(k.mesgul, self.kimlik, a, b)

        def iletim_sonucu(kosu, d, hedef, basarili, deneme, tur):
            if hedef is not None and d.sonuc_kancasi:
                k.mac.append((d.kimlik, int(hedef), bool(basarili),
                              int(deneme), kosu.olaylar.simdi, tur))
            return asil["sonuc"](kosu, d, hedef, basarili, deneme, tur)

        def kontrol_alindi(self, gozlem, gonderen, bicim, yuk, yayin):
            if bicim == SELAM_E.ad:
                sira, aralik, _, _, _, oran = selam_coz(yuk, self.kimlik)
                k.selam_al.append((self.kimlik, int(gonderen),
                                   k.kur.olaylar.simdi, int(sira),
                                   float(aralik),
                                   None if oran is None else float(oran)))
            return asil["kontrol"](self, gozlem, gonderen, bicim, yuk, yayin)

        KM.kurulum_yap = kurulum_yap
        Kosu.kostur = kostur
        Dugum.mesgul_guncelle = mesgul_guncelle
        kontrol.iletim_sonucu = iletim_sonucu
        Desparete5.kontrol_alindi = kontrol_alindi

        def geri():
            KM.kurulum_yap = asil["kurulum"]
            Kosu.kostur = asil["kostur"]
            Dugum.mesgul_guncelle = asil["mesgul"]
            kontrol.iletim_sonucu = asil["sonuc"]
            Desparete5.kontrol_alindi = asil["kontrol"]
        return geri

    # ------------------------------------------------------------------
    def ozet(self) -> dict:
        from kalibrasyon.kahin import KanalGrafigi
        from kalibrasyon.kayip_anatomisi import BAG_DILIMI_S, _etki_alani
        from sim2.kanal.yayilim import dbm_to_w

        kur = self.kur
        kfg = kur.konfig
        N = kfg.dugum_sayisi
        S = int(math.floor(kfg.kosu_bitis_s + 1e-9))
        bas_s, bitis_s = kfg.olcum_penceresi
        ilk = int(math.ceil(bas_s - 1e-9))
        son = int(math.floor(bitis_s + 1e-9))            # [ilk, son)
        kar = kur.kanal.karistirici
        uyeler = getattr(kar, "uyeler", (kar,)) if kar is not None else ()
        acilma = kfg.karistirici_baslangic_s
        ed_w = dbm_to_w(kfg.ed_esigi_dbm)

        def devrede(t_s: float) -> bool:
            return any(u.devrede_mi(t_s) for u in uyeler)

        # --- evre (B2 teşhisinin tanımı) ----------------------------------
        ev = []
        for T in range(S):
            a, b = float(T), float(T + 1)
            if kar is None:
                e = "i"
            elif b <= acilma:
                e = "o"
            elif a < acilma:
                e = "g"
            else:
                d3 = {devrede(a + 1e-6), devrede(a + 0.5), devrede(b - 1e-6)}
                e = "g" if len(d3) > 1 else ("a" if d3.pop() else "s")
            ev.append(e)
        evre = "".join(ev)

        def gecis_ani(sol: float, sag: float) -> float:
            ilk_durum = devrede(sol)
            for _ in range(40):
                orta = 0.5 * (sol + sag)
                if devrede(orta) == ilk_durum:
                    sol = orta
                else:
                    sag = orta
            return sag

        donemler: list[list[float]] = []      # açık dönemler (B2 teşhisinin yolu)
        if kar is not None:
            T = ilk
            while T < son:
                if evre[T] != "a":
                    T += 1
                    continue
                T0 = T
                while T < son and evre[T] == "a":
                    T += 1
                if devrede(float(T0 - 1)):
                    continue                 # pencereden önce başlamış dönem
                a = gecis_ani(float(T0 - 1), T0 + 1e-6)
                b = (float(son) if T >= son
                     else gecis_ani(T - 1e-6, float(T + 1)))
                donemler.append([round(a, 6), round(b, 6)])

        # --- etki alanı (düğüm × saniye) ----------------------------------
        if kar is None:
            z = ["-" * S for _ in range(N)]
        else:
            kd = {"ed": "E", "girisim": "G", "uzak": "U"}
            z = ["".join(kd[_etki_alani(kur, n, T + 0.5, ed_w)]
                         for T in range(S)) for n in range(N)]

        # --- düğüm-saniye meşgul payı ve son 10 s'nin ortalaması ----------
        m = [[self.mesgul.get((n, T), 0.0) for T in range(S)] for n in range(N)]
        birikim = []
        for n in range(N):
            b = [0.0]
            for T in range(S):
                b.append(b[-1] + m[n][T])
            birikim.append(b)

        def yuk(n: int, T: int) -> int:
            a = max(0, T - YUK_S)
            if T <= a:
                return -1
            return int(round(1000.0 * (birikim[n][T] - birikim[n][a]) / (T - a)))

        # --- bağlar: veri kayıtları, duyulma anları, selamlar -------------
        cerceve: defaultdict = defaultdict(list)      # (i, j) → [(t, d, ok)]
        tazele: defaultdict = defaultdict(list)       # (i, j) → [t]
        for i, j, ok, den, t, tur in self.mac:
            if tur == "veri":
                cerceve[(i, j)].append((t, den, ok))
            if ok:
                tazele[(i, j)].append(t)              # j'nin onayı (B1 kural 2)
        gelis: defaultdict = defaultdict(list)        # (i, j) → [(t, s, a, r)]
        for i, j, t, sira, aralik, oran in self.selam_al:
            gelis[(i, j)].append((t, sira, aralik, oran))
        for x in (cerceve, tazele, gelis):
            for v in x.values():
                v.sort()

        # --- kâhin: tek deneme başarısı, 5 s'lik dilimin ortasında --------
        grafik = KanalGrafigi(kur)
        onbellek: dict = {}

        def p_tek(i: int, j: int, dilim: int) -> int:
            anahtar = (i, j, dilim)
            p = onbellek.get(anahtar)
            if p is None:
                p = onbellek[anahtar] = grafik._tek_deneme_basarisi(
                    i, j, (dilim + 0.5) * BAG_DILIMI_S)
            return int(round(1000.0 * p))

        # --- veri örnekleri ----------------------------------------------
        veri: list = []
        for (i, j), liste in sorted(cerceve.items()):
            anlar = [x[0] for x in liste]
            kodlar = "".join(B.kod(d, ok) for _, d, ok in liste)
            secili, onceki_T = [], None
            for k_, t in enumerate(anlar):
                T = int(math.floor(t))
                if ilk <= T < son and T != onceki_T:
                    secili.append(k_)
                    onceki_T = T
            if not secili:
                continue
            b1 = B.b1_selam(gelis.get((i, j), []), tazele.get((i, j), []),
                            [anlar[k_] for k_ in secili])
            for k_, (dr, ns, df, kayitli) in zip(secili, b1):
                t = anlar[k_]
                T = int(math.floor(t))
                a0 = bisect.bisect_left(anlar, t - B.VERI_PENCERE_S)
                bas = max(a0, k_ - B.VERI_PENCERE)
                yas = (int(round(1000.0 * (t - anlar[k_ - 1])))
                       if k_ > bas else -1)
                u = bisect.bisect_left(anlar, t + B.GELECEK_S)
                veri.append([
                    int(round(1000.0 * t)), i, j, _bin(dr), ns, _bin(df),
                    int(kayitli), kodlar[bas:k_], yas,
                    kodlar[k_:min(u, k_ + B.GELECEK_K)],
                    p_tek(i, j, int(t / BAG_DILIMI_S)), yuk(i, T), yuk(j, T),
                    evre[T], z[j][T]])

        # --- ızgara örnekleri --------------------------------------------
        izgara_anlari = [(q + 0.5) * BAG_DILIMI_S
                         for q in range(int(ilk / BAG_DILIMI_S),
                                        int(son / BAG_DILIMI_S) + 1)
                         if ilk <= (q + 0.5) * BAG_DILIMI_S < son]
        izgara: list = []
        for (i, j), g in sorted(gelis.items()):
            b1 = B.b1_selam(g, tazele.get((i, j), []), izgara_anlari)
            liste = cerceve.get((i, j), [])
            anlar = [x[0] for x in liste]
            kodlar = "".join(B.kod(d, ok) for _, d, ok in liste)
            for t, (dr, ns, df, kayitli) in zip(izgara_anlari, b1):
                if not kayitli:
                    continue
                T = int(math.floor(t))
                k_ = bisect.bisect_left(anlar, t)
                a0 = bisect.bisect_left(anlar, t - B.VERI_PENCERE_S)
                bas = max(a0, k_ - B.VERI_PENCERE)
                izgara.append([
                    int(round(1000.0 * t)), i, j, _bin(dr), ns, _bin(df),
                    kodlar[bas:k_], p_tek(i, j, int(t / BAG_DILIMI_S)),
                    evre[T], z[j][T]])

        return {
            "pencere": [ilk, son], "S": S, "N": N, "evre": evre,
            "donemler": donemler, "alan": z,
            "veri_alanlar": ["t_ms", "i", "j", "dr", "ns", "df", "kayitli",
                             "once", "yas_ms", "gelecek", "p", "yuk_i",
                             "yuk_j", "evre", "alan"],
            "izgara_alanlar": ["t_ms", "i", "j", "dr", "ns", "df", "once", "p",
                               "evre", "alan"],
            "veri": veri, "izgara": izgara,
            "sayim": {
                "mesgul_s": round(sum(self.mesgul.values()), 6),
                "mesgul_dugum": round(sum(d._mesgul_toplam_s
                                          for d in self.kosu.dugumler), 6),
                "mac": len(self.mac), "selam_al": len(self.selam_al),
                "bag_veri": len(cerceve), "bag_selam": len(gelis),
                "kahin_cagri": len(onbellek)},
        }

    @staticmethod
    def denetle(r: dict) -> list[str]:
        """İç denetimler — boş liste: hepsi geçti."""
        z = r["kaydedici"]["sayim"]
        s = r["sayaclar"]
        hata = []
        if abs(z["mesgul_s"] - z["mesgul_dugum"]) > 1e-6 * max(
                1.0, z["mesgul_dugum"]):
            hata.append(f"meşgul dilimler {z['mesgul_s']} ≠ düğümler "
                        f"{z['mesgul_dugum']}")
        if z["mac"] != int(s.get("sonuc_bildirimi", 0)):
            hata.append(f"mac {z['mac']} ≠ sonuc_bildirimi "
                        f"{s.get('sonuc_bildirimi')}")
        if z["selam_al"] <= 0:
            hata.append("hiç selam alınmadı")
        if not r["kaydedici"]["veri"]:
            hata.append("veri örneği yok")
        return hata


def _is(is_) -> dict:
    """Havuz işçisi — bir (hücre, tohum) koşusu: anatomi + kayıt."""
    import traceback

    import kalibrasyon.kayip_anatomisi as KA

    hucre, tohum, kisa = is_
    sinif_, aile, hayalet, fark = HUCRE[hucre]
    etiket = ETIKET + (f"@{fark}" if fark else "")
    t0 = time.perf_counter()
    kay = Kaydedici()
    geri = kay.tak()
    try:
        r = KA._is((etiket, tohum, "formasyon", aile, kisa, sinif_,
                    KA._cizelge_oku(hayalet)))
        r["kol"] = "cekirdek"
        r["hucre"] = hucre
        t1 = time.perf_counter()
        r["kaydedici"] = kay.ozet()
        r["kaydedici_denetim"] = kay.denetle(r)
        r["sure_s"] = round(time.perf_counter() - t0, 1)
        r["ozet_s"] = round(time.perf_counter() - t1, 1)
        return r
    except Exception as hata:                               # noqa: BLE001
        return {"kol": "cekirdek", "hucre": hucre, "protokol": etiket,
                "tohum": tohum, "hata": f"{type(hata).__name__}: {hata}",
                "iz": traceback.format_exc()[-2000:]}
    finally:
        geri()


def _arg(argv: list[str], ad: str, varsayilan: str) -> str:
    if ad in argv:
        i = argv.index(ad)
        deger = argv[i + 1]
        del argv[i:i + 2]
        return deger
    return varsayilan


def main() -> int:
    from kalibrasyon import dunya_secimi as DS
    from sim2.cekirdek.degismezler import dogrula
    import protokoller.desparete5 as P5

    argv = sys.argv[1:]
    DS.secimi_oku(argv)
    kisa = "--kisa" in argv
    if kisa:
        argv.remove("--kisa")
    hucre = _arg(argv, "--hucre", "ikiz")
    tohumlar = [int(t) for t in _arg(argv, "--tohumlar", "1003").split(",")]
    isci = int(_arg(argv, "--isci", "8"))
    kayit_yolu = _arg(argv, "--kayit", "")
    dogrula(not argv, f"tanınmayan argüman: {argv}")
    dogrula(hucre in HUCRE, f"hücre {tuple(HUCRE)}: {hucre}")
    dogrula(not any(2000 <= t <= 2039 for t in tohumlar),
            "ana deney tohumları (2000–2039) mühürden önce koşulmaz")
    dogrula(not kayit_yolu or kayit_yolu.endswith(".json.gz"),
            "kayıt `.json.gz` olmalı")
    sinif_, aile, hayalet, fark = HUCRE[hucre]
    print("=" * 78)
    print(f"B3 TEŞHİSİ — dünya {DS.secili()} · {hucre} (formasyon-{sinif_}"
          f"{', ' + aile if sinif_ != 'yok' else ''}"
          f"{', hayalet ' + hayalet if hayalet else ''}"
          f"{', ' + fark if fark else ''}) · kol {ETIKET} · tohum {tohumlar}"
          f"{' · KISA PENCERE' if kisa else ''}")
    print(f"  kod: {Path(P5.__file__).resolve()}")
    print(f"  saf işlevler: {Path(B.__file__).resolve()}")
    print("=" * 78, flush=True)
    isler = [(hucre, t, kisa) for t in tohumlar]
    ara = Path(kayit_yolu[:-len(".json.gz")] + ".jsonl.gz") if kayit_yolu else None
    sonuc: list[dict] = []
    if ara is not None and ara.exists():
        with gzip.open(ara, "rt", encoding="utf-8") as f:
            for satir in f:
                if satir.strip():
                    r = json.loads(satir)
                    if "hata" not in r:
                        sonuc.append(r)
        bitti = {r["tohum"] for r in sonuc}
        isler = [i for i in isler if i[1] not in bitti]
        print(f"  ara kayıttan {len(sonuc)} koşu okundu, {len(isler)} koşu "
              f"kaldı ({ara})", flush=True)
    hatalar = 0
    if isler:
        with Pool(min(isci, len(isler))) as havuz:
            for n, r in enumerate(havuz.imap_unordered(_is, isler,
                                                       chunksize=1), 1):
                if ara is not None:
                    with gzip.open(ara, "at", encoding="utf-8") as f:
                        f.write(json.dumps(r, ensure_ascii=False,
                                           separators=(",", ":")) + "\n")
                if "hata" in r:
                    hatalar += 1
                    print(f"  HATA {n}/{len(isler)} {r['tohum']}: "
                          f"{r['hata']}\n{r['iz']}", flush=True)
                    continue
                sonuc.append(r)
                denetim = r["kaydedici_denetim"]
                kd = r["kaydedici"]
                print(f"  {n:>3}/{len(isler)} {r['tohum']} · PDR(pencere) "
                      f"{r['pdr_pencere']:.4f} · veri örneği {len(kd['veri'])}"
                      f" · ızgara {len(kd['izgara'])} · denetim "
                      f"{'tamam' if not denetim else denetim} · "
                      f"{r['sure_s']:.0f} s (özet {r['ozet_s']:.0f} s)",
                      flush=True)
    if kayit_yolu:
        with gzip.open(kayit_yolu, "wt", encoding="utf-8") as f:
            f.write(json.dumps(
                {"dunya": DS.secili(), "hucre": hucre, "kisa": kisa,
                 "sonuc": sorted(sonuc, key=lambda r: r["tohum"])},
                ensure_ascii=False, separators=(",", ":")))
    print(f"\n  {len(sonuc)} koşu kayıtta · hata {hatalar}")
    return 1 if hatalar else 0


if __name__ == "__main__":
    sys.exit(main())
