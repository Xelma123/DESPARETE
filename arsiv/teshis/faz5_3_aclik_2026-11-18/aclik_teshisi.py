"""
Faz 5-3 · AÇLIK TEŞHİSİ — çekirdeğin açlık bölümleri neden başlıyor, neden
uzuyor (`beklenti.md`). Ölçüm aleti; protokolün parçası değildir.

    cd <kod kökü: dondurulmuş kopya ya da depo kökü>
    PYTHONIOENCODING=utf-8 py -3.11 -u <bu dosya> --dunya referans_2026 \
        --kollar cekirdek[,vtk0] --tohumlar 1003,…,1010 --isci 8 \
        --kayit <yol.json> [--kisa]

Kod, ÇALIŞMA DİZİNİNDEN içe aktarılır (`kosu.sh` dondurulmuş kopyaya geçer);
hangi dosyadan geldiği çıktının başına yazılır.

🔒 KOŞU AYNI KOŞUDUR. Her koşu kayıp anatomisi aletinin işçisiyle
(`kalibrasyon/kayip_anatomisi.py::_is`) olduğu gibi yapılır: sonuç satırı,
kayıp grupları ve sayaçlar ilk ölçümünkiyle aynı yoldan çıkar. Kaydedici
protokolün sınıflarına YALNIZ OKUYAN sarmalayıcılar takar ve koşudan sonra
geri alır: protokolün hiçbir alanına yazmaz, okurken sıfırlayan yöntemleri
(`bayraklari_oku`, `olay_oku`, `istekleri_al`) çağırmaz. Denetim: çekirdek
kolunun her tohumdaki sonucu ilk ölçümün kaydıyla birebir (`beklenti.md`,
kural 0).

🔒 KOLLAR
    cekirdek  `desparete5_cekirdek` (CEKIRDEK bayrakları), ilk ölçümle aynı
    vtk0      aynısı, yalnız `veri_kotu_tetigi` kapalı; işçinin içinde
              `aodv_uygunluk.DESPARETE5_PROFILLERI` o koşu süresince
              değiştirilir ve geri alınır (bayraklar koşu kimliğine girer)

🔒 KAYDEDİLENLER (zaman simülatörün saati, saniye)
    kayip   ardılın uygun aday olmaktan çıktığı her seçim: düğüm, eski ardıl,
            t, sebep, sonuç (`aclik` ya da başka komşuya `gecis`). Sebep:
              silindi       komşu kaydı silindi (`T_SILME`)
              bag:<çıkış>   bağ OLAĞAN'dan çıktı (aşağıdaki çıkış sebebi)
              geri_cekme    ardıl ∞ ilan etti
              yoksay_doldu  yok sayma süresi doldu, son ilan uygulanamaz
              maliyet       toplam maliyet taştı
    bolum   açlık bölümü: ardıl kaybı açlıkla sonuçlanınca açılır, ardıl
            yeniden seçilince kapanır. Başlangıçta: sebep, `ust` (sebep
            geri_cekme ise eski ardılın o an açık bölümü), komşu sayımı
            (eski ardıl hariç; durum × ilan sınıfı), FD, geçidin turu, istek
            dizisi başladı mı. Süresince: bu düğümde rotasızlıktan düşen
            telemetri paketlerinin doğum anları. Sonda: t, yeni ardıl, eski
            ardılın kendisi mi, yeni tur mu (rotanın turu başlangıçtaki
            FD'nin turundan büyük).
            Komşu sayımının ilan sınıfları: `sonsuz` · `uygulanabilir` ·
            `eski_tur` (turu FD'ninkinden küçük) · `pahali` (aynı tur,
            maliyet ≥ FD); durum `olagan` ya da `kotu` (OLAĞAN değil).
    cikis   bağın OLAĞAN'dan her çıkışı: düğüm, komşu, t, sebep, d_f, d_r,
            o an ardıl mıydı, OLAĞAN'a dönüş anı, kâhinin o andaki tek deneme
            başarısı (i→j, sönümleme dâhil, girişim hariç, ARF tabanında;
            `kalibrasyon/kahin.py`). Çıkış sebebi `_kotu`yu çağırana göre:
              selam_asim   beklenen selam gelmedi, ETX_selam > E_CIK
              selam_alim   selam alındı (boşluk ya da düşen d_f), ETX > E_CIK
              veri         veri tetiği (`_askida_gir`)
              df_bayat     komşu beni `T_SILME` boyunca listelemedi (Y-12)
              silindi      kayıt silindi
              karisma      karıştırma durumu (çekirdekte kapalı)
    tur     geçidin her tur artışı (t, yeni tur); her düğümün seçili rotasının
            turunun yükseldiği anlar
    bolumsuz  bölüm açık değilken rotasızlıktan düşen telemetri paketleri
            (açılıştan beri hiç rotası olmayan düğüm)

İç denetimler: bölüm sayısı = düğümlerin `rota.aclik` sayaçlarının toplamı;
kayıp sayısı = `rota.aclik` + `rota.zorunlu_gecis`; çıkışların `veri`
sebeplileri = `bag.veri_kotu` (çekirdekte); `vtk0` kolunda `bag.veri_kotu`
= 0.
"""

from __future__ import annotations

import json
import os
import sys
import time
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

# Kod çalışma dizininden (dondurulmuş kopya); bu dosyanın dizini değil.
if os.getcwd() not in sys.path[:1]:
    sys.path.insert(0, os.getcwd())

PROTOKOL = "desparete5_cekirdek"
HAYALET = ((10.0, 20.0),)                # ilk ölçümün `--hayalet 10:20`si
KOLLAR = ("cekirdek", "vtk0")

# `_kotu`yu çağıran yöntem → çıkış sebebi
_CAGIRAN = {"_z_asim": "selam_asim", "selam_al": "selam_alim",
            "_askida_gir": "veri", "_z_askida": "veri",
            "_z_df": "df_bayat", "_z_hatira": "karisma",
            "_karisma_cik": "karisma"}


class Kaydedici:
    """Bir koşunun kaydı. `tak()` sarmalayıcıları takar, dönen işlev geri
    alır. `kur` koşunun kurulumu (`kurulum_yap` sarmalayıcısı yakalar ya da
    elle verilir)."""

    def __init__(self) -> None:
        self.kur = None
        self.protokoller: list = []
        self._sahip: dict[int, object] = {}      # id(bag|rota) → protokol
        self.kayip: list = []
        self.bolum: list[dict] = []
        self.acik: dict[int, dict] = {}          # düğüm → açık bölüm
        self.cikis: list[list] = []
        self._acik_cikis: dict[tuple[int, int], list] = {}
        self._son_cikis: dict[tuple[int, int], str] = {}
        self.gecit_tur: list[tuple[float, int]] = []
        self.rota_tur: dict[int, list[tuple[float, int]]] = {}
        self._rota_tur_en: dict[int, int] = {}
        self.bolumsuz: list[tuple[int, float, float]] = []
        self.tutarsiz = 0                        # sebebi bulunamayan kayıp
        self._derinlik = 0

    def saat(self) -> float:
        return float(self.kur.olaylar.simdi)

    # ------------------------------------------------------------------
    def tak(self):
        import sim2.kosum.kurulum as KM
        from protokoller.desparete5 import Desparete5
        from protokoller.desparete5_bag import OLAGAN, BagTablosu
        from protokoller.desparete5_bicim import (
            SONSUZ, maliyet_topla, sira_buyuk)
        from protokoller.desparete5_rota import Rota
        from sim2.kosum.dugum import Dugum

        k = self
        asil = {
            "kurulum": KM.kurulum_yap, "init": Desparete5.__init__,
            "sec": Rota.sec, "istek_al": Rota.istek_al,
            "_kotu": BagTablosu._kotu, "_askida_gir": BagTablosu._askida_gir,
            "_karisma_gir": BagTablosu._karisma_gir,
            "_sil": BagTablosu._sil, "_kotu_donus": BagTablosu._kotu_donus,
            "_karisma_cik": BagTablosu._karisma_cik,
            "karar": Dugum.sonraki_atlama,
        }

        def kurulum_yap(*a, **kw):
            kur = asil["kurulum"](*a, **kw)
            k.kur = kur
            return kur

        def init(self, *a, **kw):
            asil["init"](self, *a, **kw)
            k.protokoller.append(self)
            k._sahip[id(self.bag)] = self
            k._sahip[id(self.rota)] = self

        # --- bağ çıkışları ve dönüşleri --------------------------------
        def _cikis_yaz(tablo, bag_, j: int, sebep: str, d_f, d_r) -> None:
            p = k._sahip.get(id(tablo))
            if p is None:
                return
            kayit = [p.kimlik, j, k.saat(), sebep,
                     None if d_f is None else round(d_f, 4),
                     None if d_r is None else round(d_r, 4),
                     p.rota.ardil == j, None, None]
            k.cikis.append(kayit)
            k._acik_cikis[(p.kimlik, j)] = kayit
            k._son_cikis[(p.kimlik, j)] = sebep

        def sarmala_cikis(ad: str, sebep_sabit: str | None):
            def sarmal(self, bag_, *a, **kw):
                once = bag_.durum == OLAGAN
                k._derinlik += 1
                try:
                    if sebep_sabit is None:
                        cagiran = sys._getframe(1).f_code.co_name
                        sebep = _CAGIRAN.get(cagiran, cagiran)
                    else:
                        sebep = sebep_sabit
                    sonuc = asil[ad](self, bag_, *a, **kw)
                finally:
                    k._derinlik -= 1
                if (once and bag_.durum != OLAGAN and k._derinlik == 0):
                    _cikis_yaz(self, bag_, bag_.komsu, sebep, bag_.d_f,
                               bag_.d_r)
                return sonuc
            return sarmal

        def _sil(self, j):
            bag_ = self.baglar.get(j)
            once = bag_ is not None and bag_.durum == OLAGAN
            d_f = None if bag_ is None else bag_.d_f
            d_r = None if bag_ is None else bag_.d_r
            sonuc = asil["_sil"](self, j)
            if once and k._derinlik == 0:
                _cikis_yaz(self, bag_, j, "silindi", d_f, d_r)
            return sonuc

        def sarmala_donus(ad: str):
            def sarmal(self, bag_, *a, **kw):
                once = bag_.durum == OLAGAN
                sonuc = asil[ad](self, bag_, *a, **kw)
                if not once and bag_.durum == OLAGAN:
                    p = k._sahip.get(id(self))
                    if p is not None:
                        kayit = k._acik_cikis.pop((p.kimlik, bag_.komsu),
                                                  None)
                        if kayit is not None:
                            kayit[7] = k.saat()
                return sonuc
            return sarmal

        # --- rota seçimi: ardıl kaybı ve açlık bölümleri ----------------
        def _sebep(rota, baglar, eski, kabul, ilan) -> str | None:
            durum = baglar.durum(eski)
            if durum is None:
                return "silindi"
            if durum != OLAGAN:
                return "bag:" + k._son_cikis.get((rota.kimlik, eski), "?")
            tur, C = kabul if kabul is not None else ilan
            if C >= SONSUZ:
                return "geri_cekme"
            if not rota.uygulanabilir(tur, C):
                return "yoksay_doldu"
            if maliyet_topla(baglar.maliyet(eski), C) >= SONSUZ:
                return "maliyet"
            return None                         # uygun: isteğe bağlı geçiş

        def _sayim(rota, baglar, eski) -> dict:
            fd = rota.fd
            s: Counter = Counter()
            for j, (tur, C) in sorted(rota.ilanlar.items()):
                if j == eski:
                    continue
                if C >= SONSUZ:
                    sinif = "sonsuz"
                elif rota.uygulanabilir(tur, C):
                    sinif = "uygulanabilir"
                elif fd is not None and sira_buyuk(fd[0], tur):
                    sinif = "eski_tur"
                else:
                    sinif = "pahali"
                durum = "olagan" if baglar.kullanilir_mi(j) else "kotu"
                s[f"{durum}_{sinif}"] += 1
            return dict(s)

        def sec(self, t, baglar, kendi_donuk):
            if self.gecit_mi:
                return asil["sec"](self, t, baglar, kendi_donuk)
            eski, kabul = self.ardil, self.kabul
            ilan = self.ilanlar.get(eski) if eski is not None else None
            sonuc = asil["sec"](self, t, baglar, kendi_donuk)
            yeni = self.ardil
            if yeni == eski:
                k._tur_izle(self)
                return sonuc
            ts = k.saat()
            ben = self.kimlik
            if eski is not None:
                sebep = _sebep(self, baglar, eski, kabul, ilan)
                if sebep is not None:
                    k.kayip.append([ben, eski, ts, sebep,
                                    "aclik" if yeni is None else "gecis"])
                elif yeni is None:
                    k.tutarsiz += 1
                    sebep = "?"
                if yeni is None:
                    ust = (k.acik.get(eski) if sebep == "geri_cekme"
                           else None)
                    fd = self.fd
                    gecit = k._gecit_rota()
                    b = {"id": len(k.bolum), "dugum": ben, "t": ts,
                         "sebep": sebep, "eski": eski,
                         "ust": None if ust is None else ust["id"],
                         "sayim": _sayim(self, baglar, eski),
                         "fd": None if fd is None else list(fd),
                         "gecit_tur": (None if gecit is None
                                       else gecit.tur_gecit),
                         "istek": self.aclik is not None,
                         "komsu": len(baglar.baglar),
                         "olagan": len(baglar.kullanilir_kume()),
                         "dusen": [], "t_son": None, "yeni": None,
                         "ayni_komsu": None, "yeni_tur": None}
                    k.bolum.append(b)
                    k.acik[ben] = b
            if eski is None and yeni is not None:
                b = k.acik.pop(ben, None)
                if b is not None:
                    b["t_son"] = ts
                    b["yeni"] = yeni
                    b["ayni_komsu"] = yeni == b["eski"]
                    b["yeni_tur"] = (None if b["fd"] is None else
                                     sira_buyuk(self.kabul[0], b["fd"][0]))
            k._tur_izle(self)
            return sonuc

        def istek_al(self, g, t, istenen, kalan):
            once = self.tur_gecit
            sonuc = asil["istek_al"](self, g, t, istenen, kalan)
            if self.gecit_mi and self.tur_gecit != once:
                k.gecit_tur.append((k.saat(), self.tur_gecit))
            return sonuc

        # --- rotasızlıktan düşen telemetri paketleri --------------------
        def karar(self, paket, t_s):
            sonuc = asil["karar"](self, paket, t_s)
            if (paket is not None and sonuc.sonraki is None
                    and not sonuc.beklet
                    and paket.hedef == k.kur.konfig.gecit
                    and paket.kaynak is not None):
                b = k.acik.get(self.kimlik)
                if b is not None:
                    b["dusen"].append(round(float(paket.dogum_s), 4))
                else:
                    k.bolumsuz.append((self.kimlik, round(float(t_s), 4),
                                       round(float(paket.dogum_s), 4)))
            return sonuc

        KM.kurulum_yap = kurulum_yap
        Desparete5.__init__ = init
        Rota.sec = sec
        Rota.istek_al = istek_al
        BagTablosu._kotu = sarmala_cikis("_kotu", None)
        BagTablosu._askida_gir = sarmala_cikis("_askida_gir", "veri")
        BagTablosu._karisma_gir = sarmala_cikis("_karisma_gir", "karisma")
        BagTablosu._sil = _sil
        BagTablosu._kotu_donus = sarmala_donus("_kotu_donus")
        BagTablosu._karisma_cik = sarmala_donus("_karisma_cik")
        Dugum.sonraki_atlama = karar

        def geri():
            KM.kurulum_yap = asil["kurulum"]
            Desparete5.__init__ = asil["init"]
            Rota.sec = asil["sec"]
            Rota.istek_al = asil["istek_al"]
            for ad in ("_kotu", "_askida_gir", "_karisma_gir", "_sil",
                       "_kotu_donus", "_karisma_cik"):
                setattr(BagTablosu, ad, asil[ad])
            Dugum.sonraki_atlama = asil["karar"]
        return geri

    def _gecit_rota(self):
        for p in self.protokoller:
            if p.rota.gecit_mi:
                return p.rota
        return None

    def _tur_izle(self, rota) -> None:
        if rota.ardil is None or rota.kabul is None:
            return
        from protokoller.desparete5_bicim import sira_buyuk
        tur = rota.kabul[0]
        en = self._rota_tur_en.get(rota.kimlik)
        if en is None or sira_buyuk(tur, en):
            self._rota_tur_en[rota.kimlik] = tur
            self.rota_tur.setdefault(rota.kimlik, []).append(
                (round(self.saat(), 4), tur))

    # ------------------------------------------------------------------
    def kahin_ekle(self) -> None:
        """Her bağ çıkışına kâhinin o andaki tek deneme başarısı (i→j)."""
        from kalibrasyon.kahin import KanalGrafigi
        grafik = KanalGrafigi(self.kur)
        for c in self.cikis:
            c[8] = round(grafik._tek_deneme_basarisi(c[0], c[1], c[2]), 4)

    def ozet(self) -> dict:
        kfg = self.kur.konfig
        return {
            "pencere": list(kfg.olcum_penceresi),
            "deneme": kfg.yeniden_deneme_siniri + 1,
            "gecit": kfg.gecit,
            "bayraklar": (list(self.protokoller[0].b.degerler())
                          if self.protokoller else None),
            "bayrak_adlari": (list(self.protokoller[0].b.adlar())
                              if self.protokoller else None),
            "kayip": self.kayip,
            "bolum": self.bolum,
            "cikis": self.cikis,
            "gecit_tur": self.gecit_tur,
            "rota_tur": {str(d): v for d, v in sorted(self.rota_tur.items())},
            "bolumsuz": self.bolumsuz,
            "acik_kalan": len(self.acik),
            "tutarsiz": self.tutarsiz,
        }

    def denetle(self, teshis_toplam: dict, kol: str) -> list[str]:
        """İç denetimler — boş liste: hepsi geçti."""
        hata = []
        t = teshis_toplam
        aclik = t.get("rota.aclik", 0)
        zorunlu = t.get("rota.zorunlu_gecis", 0)
        if len(self.bolum) != aclik:
            hata.append(f"bölüm {len(self.bolum)} ↔ rota.aclik {aclik}")
        if len(self.kayip) != aclik + zorunlu:
            hata.append(f"kayıp {len(self.kayip)} ↔ aclik + zorunlu_gecis "
                        f"{aclik + zorunlu}")
        if self.tutarsiz:
            hata.append(f"sebebi bulunamayan açlık {self.tutarsiz}")
        veri = sum(1 for c in self.cikis if c[3] == "veri")
        if veri != t.get("bag.veri_kotu", 0):
            hata.append(f"veri sebepli çıkış {veri} ↔ bag.veri_kotu "
                        f"{t.get('bag.veri_kotu', 0)}")
        if kol == "vtk0" and t.get("bag.veri_kotu", 0) != 0:
            hata.append("vtk0 kolunda veri tetiği çalıştı")
        return hata


def _is(is_) -> dict:
    """Havuz işçisi — bir (kol, tohum) koşusu: anatomi + açlık kaydı."""
    import traceback
    from dataclasses import replace

    import kalibrasyon.aodv_uygunluk as AU
    import kalibrasyon.kayip_anatomisi as KA

    kol, tohum, kisa = is_
    t0 = time.perf_counter()
    kay = Kaydedici()
    profil = AU.DESPARETE5_PROFILLERI[PROTOKOL]
    geri = kay.tak()
    try:
        if kol == "vtk0":
            AU.DESPARETE5_PROFILLERI[PROTOKOL] = replace(
                profil, veri_kotu_tetigi=False)
        r = KA._is((PROTOKOL, tohum, "formasyon", "derin_sizma", kisa, "yok",
                    HAYALET))
        kay.kahin_ekle()
        r["kol"] = kol
        r["aclik"] = kay.ozet()
        r["aclik_denetim"] = kay.denetle(r["teshis_toplam"], kol)
        r["sure_s"] = round(time.perf_counter() - t0, 1)
        return r
    except Exception as hata:                               # noqa: BLE001
        return {"kol": kol, "protokol": PROTOKOL, "tohum": tohum,
                "hata": f"{type(hata).__name__}: {hata}",
                "iz": traceback.format_exc()[-2000:]}
    finally:
        AU.DESPARETE5_PROFILLERI[PROTOKOL] = profil
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
    kollar = _arg(argv, "--kollar", "cekirdek").split(",")
    tohumlar = [int(t) for t in _arg(argv, "--tohumlar", "1003").split(",")]
    isci = int(_arg(argv, "--isci", "8"))
    kayit_yolu = _arg(argv, "--kayit", "")
    dogrula(not argv, f"tanınmayan argüman: {argv}")
    dogrula(all(k in KOLLAR for k in kollar), f"kollar {KOLLAR}: {kollar}")
    dogrula(not any(2000 <= t <= 2039 for t in tohumlar),
            "ana deney tohumları (2000–2039) mühürden önce koşulmaz")
    print("=" * 78)
    print(f"AÇLIK TEŞHİSİ — dünya {DS.secili()} · formasyon-yok (ikiz) · "
          f"kollar {kollar} · tohum {tohumlar}"
          f"{' · KISA PENCERE' if kisa else ''}")
    print(f"  kod: {Path(P5.__file__).resolve()}")
    print("=" * 78, flush=True)
    isler = [(k, t, kisa) for k in kollar for t in tohumlar]
    ara = Path(kayit_yolu + "l") if kayit_yolu else None
    sonuc: list[dict] = []
    if ara is not None and ara.exists():
        for satir in ara.read_text(encoding="utf-8").splitlines():
            if satir.strip():
                r = json.loads(satir)
                if "hata" not in r:
                    sonuc.append(r)
        bitti = {(r["kol"], r["tohum"]) for r in sonuc}
        isler = [i for i in isler if (i[0], i[1]) not in bitti]
        print(f"  ara kayıttan {len(sonuc)} koşu okundu, {len(isler)} koşu "
              f"kaldı ({ara})", flush=True)
    hatalar = 0
    if isler:
        with Pool(min(isci, len(isler))) as havuz:
            for n, r in enumerate(havuz.imap_unordered(_is, isler,
                                                       chunksize=1), 1):
                if ara is not None:
                    with ara.open("a", encoding="utf-8") as f:
                        f.write(json.dumps(r, ensure_ascii=False) + "\n")
                if "hata" in r:
                    hatalar += 1
                    print(f"  HATA {n}/{len(isler)} {r['kol']} {r['tohum']}: "
                          f"{r['hata']}\n{r['iz']}", flush=True)
                    continue
                sonuc.append(r)
                a = r["aclik"]
                print(f"  {n:>3}/{len(isler)} {r['kol']:<9} {r['tohum']} · "
                      f"PDR(pencere) {r['pdr_pencere']:.4f} · bölüm "
                      f"{len(a['bolum'])} · kayıp {len(a['kayip'])} · çıkış "
                      f"{len(a['cikis'])} · tur artışı {len(a['gecit_tur'])}"
                      f" · denetim "
                      f"{'tamam' if not r['aclik_denetim'] else r['aclik_denetim']}"
                      f" · {r['sure_s']:.0f} s", flush=True)
    if kayit_yolu:
        Path(kayit_yolu).write_text(
            json.dumps({"dunya": DS.secili(), "kisa": kisa,
                        "sonuc": sorted(sonuc, key=lambda r: (r["kol"],
                                                              r["tohum"]))},
                       ensure_ascii=False), encoding="utf-8")
    print(f"\n  {len(sonuc)} koşu kayıtta · hata {hatalar}")
    return 1 if hatalar else 0


if __name__ == "__main__":
    sys.exit(main())
