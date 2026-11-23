"""
Faz 5-3 · DÖNGÜ KURALLARI — eğime geri gönderme yasağı (KK-04/13) ve sınırlı
yükselme (KK-04/14) eklenmiş çekirdeğin ölçümü (`beklenti.md`). Ölçüm aleti;
protokolün parçası değildir. `../faz5_3_yeni_cekirdek_2026-11-19/olcum.py`'den
uyarlandı: kaydedici aynı, yalnız kollar değişti.

    cd <kod kökü: dondurulmuş kopya ya da depo kökü>
    PYTHONIOENCODING=utf-8 py -3.11 -u <bu dosya> --dunya referans_2026 \
        --hucre ikiz|birincil --kollar geri_sinir[,geri,c19] \
        --tohumlar 1003,…,1010 --isci 8 --kayit <yol.json> [--kisa]

Kod ÇALIŞMA DİZİNİNDEN içe aktarılır (`kosu.sh` dondurulmuş kopyaya geçer);
hangi dosyadan geldiği çıktının başına yazılır.

🔒 KOŞU AYNI KOŞUDUR. Her koşu kayıp anatomisi aletinin işçisiyle
(`kalibrasyon/kayip_anatomisi.py::_is`) olduğu gibi yapılır: sonuç satırı,
kayıp grupları ve sayaçlar ilk ölçümünkiyle aynı yoldan çıkar. Kaydedici
protokolün sınıflarına YALNIZ OKUYAN sarmalayıcılar takar ve koşudan sonra
geri alır: protokolün hiçbir alanına yazmaz, okurken sıfırlayan yöntemleri
çağırmaz. Denetim (`beklenti.md`, kural 0): duman koşusunda `geri_sinir` kolu
kaydediciyle ve doğrudan kayıp anatomisi aletiyle birebir; `c19` kolu yeni
çekirdeğin ölçümünün (`../faz5_3_yeni_cekirdek_2026-11-19/`) `cekirdek`
duman satırıyla birebir.

🔒 KOLLAR (ikinci sütun kayıttaki `protokol` etiketi)
    geri_sinir  desparete5_cekirdek      CEKIRDEK (20 Kasım): 19 Kasım'ın
                                         çekirdeği + geri gönderme yasağı +
                                         sınırlı yükselme
    geri        desparete5_geri          aynısı, `sinirli_yukselme` kapalı
    c19         desparete5_cekirdek_19k  19 Kasım'ın çekirdeği (CEKIRDEK_19K);
                                         yalnız duman
  geri işçinin içinde `aodv_uygunluk.DESPARETE5_PROFILLERI`ne o koşu
  süresince eklenir ve çıkarılır. Etiket koşunun rastgele akışlarına
  girmez (`DS.konfig` etiketi almaz): kollar aynı tohumda aynı dünyayı görür.

🔒 HÜCRELER (ilk ölçümle aynı; `formasyon · yere_toplama`, tam pencere)
    ikiz      karıştırıcısız (`--sinif yok`), hayalet çizelge 10:20
    birincil  `derin_sizma` (`--sinif surekli`)

🔒 KAYDEDİLENLER (zaman simülatörün saati, saniye)
    tetik   vazgeçme tetiğinin her çalışması (`BagTablosu._vud_gir`): düğüm,
            komşu, t, o an ardıl mıydı, bekleme süresi, kâhinin o andaki tek
            deneme başarısı (i→j, sönümleme dâhil, girişim hariç;
            `kalibrasyon/kahin.py`), ardılsa işaret sürerken ardılın değiştiği
            ana kadar geçen süre (değişmediyse boş), işaret sürerken o bağa
            yazılan veri sonucu ve vazgeçme sayısı
    paket   geçide giden her telemetri paketi: doğum anı, kaynağın ilk
            kararındaki geçide maliyeti (`rota.C`, ETX × 64), kararlarda
            görülen en büyük atlama sayısı (TTL'den: başlangıç − kalan).
            Teslim edilen paketin atlama sayısı = en büyük + 1. Kaynakta hiç
            karar görmeden düşen paket (kuyruk taşması) kayda girmez.
    Özet: tetik listesi; penceredeki telemetri paketlerinin kaynak maliyeti
    dağılımı (1 ETX'lik kutular, `inf` ∞) ve teslim edilenlerin atlama
    sayısı dağılımı; bütün koşuda kararlarda görülen en büyük atlama sayısı
    (telemetri ve komut).

İç denetimler: tetik sayısı = `bag.vaz_tetik`; işaretliyken vazgeçme ≤
`bag.vazgecme`; vazgeçme tetiği kapalı kollarda tetik yok; ilk kararı
kaynakta görülmeyen telemetri paketi yok.
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

ETIKET = {"geri_sinir": "desparete5_cekirdek", "geri": "desparete5_geri",
          "c19": "desparete5_cekirdek_19k"}
# CEKIRDEK'ten farkları; bu kollar koşu süresince profillere eklenir.
FARK = {"geri": {"sinirli_yukselme": False}}
TETIKSIZ: tuple[str, ...] = ()
HUCRE = {"ikiz": ("yok", "10:20"), "birincil": ("surekli", "")}


class Kaydedici:
    """Bir koşunun kaydı. `tak()` sarmalayıcıları takar, dönen işlev geri
    alır."""

    def __init__(self) -> None:
        self.kur = None
        self._sahip: dict[int, object] = {}      # id(BagTablosu) → protokol
        # [düğüm, komşu, t, ardıl mı, bekleme, kâhin p, ardıl değişti (s),
        #  işaretliyken veri sonucu, işaretliyken vazgeçme]
        self.tetik: list[list] = []
        self._son: dict[tuple[int, int], list] = {}
        self.paket: dict[int, list] = {}         # kimlik → [doğum, C, atlama]
        self.en_atlama = 0

    # ------------------------------------------------------------------
    def tak(self):
        import sim2.kosum.kurulum as KM
        from protokoller.desparete5 import Desparete5
        from protokoller.desparete5_bag import BagTablosu
        from protokoller.desparete5_egim import Egim
        from sim2.kosum.dugum import Dugum

        k = self
        asil = {
            "kurulum": KM.kurulum_yap, "init": Desparete5.__init__,
            "_vud_gir": BagTablosu._vud_gir,
            "_vazgecme_yaz": BagTablosu._vazgecme_yaz,
            "sec": Egim.sec, "karar": Dugum.sonraki_atlama,
        }

        def kurulum_yap(*a, **kw):
            kur = asil["kurulum"](*a, **kw)
            k.kur = kur
            return kur

        def init(self, *a, **kw):
            asil["init"](self, *a, **kw)
            k._sahip[id(self.bag)] = self

        # --- vazgeçme tetiği (KK-01/6–7) --------------------------------
        def _vud_gir(self, bag, t):
            sonuc = asil["_vud_gir"](self, bag, t)
            p = k._sahip.get(id(self))
            if p is not None:
                kayit = [p.kimlik, bag.komsu, round(float(t), 4),
                         p.rota.ardil == bag.komsu, round(bag.vud_sure, 3),
                         None, None, 0, 0]
                k.tetik.append(kayit)
                k._son[(p.kimlik, bag.komsu)] = kayit
            return sonuc

        def _vazgecme_yaz(self, bag, t, vazgecildi):
            kayit = None
            if t < bag.vud_bitis_t:                 # işaret sürüyor
                p = k._sahip.get(id(self))
                if p is not None:
                    kayit = k._son.get((p.kimlik, bag.komsu))
            sonuc = asil["_vazgecme_yaz"](self, bag, t, vazgecildi)
            if kayit is not None:
                kayit[7] += 1
                if vazgecildi:
                    kayit[8] += 1
            return sonuc

        # --- eğim: işaret sürerken ardıl değişti mi ---------------------
        def sec(self, t, baglar, kendi_donuk):
            eski = self.ardil
            sonuc = asil["sec"](self, t, baglar, kendi_donuk)
            if eski is not None and self.ardil != eski:
                kayit = k._son.get((self.kimlik, eski))
                if (kayit is not None and kayit[3] and kayit[6] is None
                        and t < kayit[2] + kayit[4]):
                    kayit[6] = round(float(t) - kayit[2], 4)
            return sonuc

        # --- telemetri paketi: kaynak maliyeti ve atlama sayısı ---------
        def karar(self, paket, t_s):
            sonuc = asil["karar"](self, paket, t_s)
            if paket is not None and paket.kaynak is not None:
                kfg = k.kur.konfig
                a = kfg.ttl_baslangic - paket.ttl_kalan
                if a > k.en_atlama:
                    k.en_atlama = a
                if paket.hedef == kfg.gecit:
                    kayit = k.paket.get(paket.kimlik)
                    if kayit is None:
                        C = (int(self.protokol.rota.C)
                             if self.kimlik == paket.kaynak else None)
                        k.paket[paket.kimlik] = [float(paket.dogum_s), C, a]
                    elif a > kayit[2]:
                        kayit[2] = a
            return sonuc

        KM.kurulum_yap = kurulum_yap
        Desparete5.__init__ = init
        BagTablosu._vud_gir = _vud_gir
        BagTablosu._vazgecme_yaz = _vazgecme_yaz
        Egim.sec = sec
        Dugum.sonraki_atlama = karar

        def geri():
            KM.kurulum_yap = asil["kurulum"]
            Desparete5.__init__ = asil["init"]
            BagTablosu._vud_gir = asil["_vud_gir"]
            BagTablosu._vazgecme_yaz = asil["_vazgecme_yaz"]
            Egim.sec = asil["sec"]
            Dugum.sonraki_atlama = asil["karar"]
        return geri

    # ------------------------------------------------------------------
    def ozet(self) -> dict:
        from kalibrasyon.kahin import KanalGrafigi
        from protokoller.desparete5_bicim import SONSUZ

        kfg = self.kur.konfig
        if self.tetik:
            grafik = KanalGrafigi(self.kur)
            for c in self.tetik:
                c[5] = round(grafik._tek_deneme_basarisi(c[0], c[1], c[2]), 4)
        bas, bitis = kfg.olcum_penceresi
        teslim = {kd.kimlik for kd in self.kur.paket_defteri.kayitlar()}
        maliyet: Counter = Counter()
        atlama: Counter = Counter()
        en_C = 0
        for kimlik, (dogum, C, a) in self.paket.items():
            if not bas <= dogum < bitis:
                continue
            if C is None:
                maliyet["?"] += 1
            elif C >= SONSUZ:
                maliyet["inf"] += 1
            else:
                maliyet[str(C // 64)] += 1           # [n, n+1) ETX
                en_C = max(en_C, C)
            if kimlik in teslim:
                atlama[str(a + 1)] += 1
        return {
            "pencere": list(kfg.olcum_penceresi),
            "deneme": kfg.yeniden_deneme_siniri + 1,
            "ttl": kfg.ttl_baslangic,
            "bayraklar": (list(next(iter(self._sahip.values())).b.degerler())
                          if self._sahip else None),
            "tetik": self.tetik,
            "maliyet": dict(maliyet),
            "en_maliyet_etx": round(en_C / 64.0, 3),
            "atlama": dict(atlama),
            "en_atlama": self.en_atlama,
            "telemetri_pencerede": sum(maliyet.values()),
        }

    def denetle(self, t: dict, kol: str, ozet: dict) -> list[str]:
        """İç denetimler — boş liste: hepsi geçti."""
        hata = []
        tetik = t.get("bag.vaz_tetik", 0)
        if len(self.tetik) != tetik:
            hata.append(f"tetik {len(self.tetik)} ↔ bag.vaz_tetik {tetik}")
        isaretli = sum(c[8] for c in self.tetik)
        if isaretli > t.get("bag.vazgecme", 0):
            hata.append(f"işaretliyken vazgeçme {isaretli} > bag.vazgecme "
                        f"{t.get('bag.vazgecme', 0)}")
        if kol in TETIKSIZ and (self.tetik or tetik):
            hata.append(f"{kol} kolunda vazgeçme tetiği çalıştı")
        if ozet["maliyet"].get("?", 0):
            hata.append(f"ilk kararı kaynakta görülmeyen telemetri paketi "
                        f"{ozet['maliyet']['?']}")
        return hata


def _is(is_) -> dict:
    """Havuz işçisi — bir (kol, hücre, tohum) koşusu: anatomi + kayıt."""
    import traceback
    from dataclasses import replace

    import kalibrasyon.aodv_uygunluk as AU
    import kalibrasyon.kayip_anatomisi as KA

    kol, hucre, tohum, kisa = is_
    etiket = ETIKET[kol]
    sinif, hayalet = HUCRE[hucre]
    t0 = time.perf_counter()
    kay = Kaydedici()
    eklendi = False
    geri = kay.tak()
    try:
        if kol in FARK:
            if etiket in AU.DESPARETE5_PROFILLERI:
                raise RuntimeError(f"{etiket} profillerde zaten var")
            AU.DESPARETE5_PROFILLERI[etiket] = replace(
                AU.DESPARETE5_PROFILLERI["desparete5_cekirdek"], **FARK[kol])
            eklendi = True
        r = KA._is((etiket, tohum, "formasyon", "derin_sizma", kisa, sinif,
                    KA._cizelge_oku(hayalet)))
        ozet = kay.ozet()
        r["kol"] = kol
        r["hucre"] = hucre
        r["kaydedici"] = ozet
        r["kaydedici_denetim"] = kay.denetle(r["teshis_toplam"], kol, ozet)
        r["sure_s"] = round(time.perf_counter() - t0, 1)
        return r
    except Exception as hata:                               # noqa: BLE001
        return {"kol": kol, "hucre": hucre, "protokol": etiket,
                "tohum": tohum, "hata": f"{type(hata).__name__}: {hata}",
                "iz": traceback.format_exc()[-2000:]}
    finally:
        if eklendi:
            del AU.DESPARETE5_PROFILLERI[etiket]
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
    kollar = _arg(argv, "--kollar", "geri_sinir").split(",")
    tohumlar = [int(t) for t in _arg(argv, "--tohumlar", "1003").split(",")]
    isci = int(_arg(argv, "--isci", "8"))
    kayit_yolu = _arg(argv, "--kayit", "")
    dogrula(not argv, f"tanınmayan argüman: {argv}")
    dogrula(hucre in HUCRE, f"hücre {tuple(HUCRE)}: {hucre}")
    dogrula(all(k in ETIKET for k in kollar), f"kollar {tuple(ETIKET)}: "
            f"{kollar}")
    dogrula(not any(2000 <= t <= 2039 for t in tohumlar),
            "ana deney tohumları (2000–2039) mühürden önce koşulmaz")
    sinif, hayalet = HUCRE[hucre]
    print("=" * 78)
    print(f"DÖNGÜ KURALLARI — dünya {DS.secili()} · formasyon-{sinif} "
          f"({hucre}{', hayalet ' + hayalet if hayalet else ''}) · kollar "
          f"{kollar} · tohum {tohumlar}{' · KISA PENCERE' if kisa else ''}")
    print(f"  kod: {Path(P5.__file__).resolve()}")
    print("=" * 78, flush=True)
    isler = [(k, hucre, t, kisa) for k in kollar for t in tohumlar]
    ara = Path(kayit_yolu + "l") if kayit_yolu else None
    sonuc: list[dict] = []
    if ara is not None and ara.exists():
        for satir in ara.read_text(encoding="utf-8").splitlines():
            if satir.strip():
                r = json.loads(satir)
                if "hata" not in r:
                    sonuc.append(r)
        bitti = {(r["kol"], r["tohum"]) for r in sonuc}
        isler = [i for i in isler if (i[0], i[2]) not in bitti]
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
                z = r["kaydedici"]
                denetim = r["kaydedici_denetim"]
                print(f"  {n:>3}/{len(isler)} {r['kol']:<8} {r['tohum']} · "
                      f"PDR(pencere) {r['pdr_pencere']:.4f} · tetik "
                      f"{len(z['tetik'])} · en çok atlama {z['en_atlama']} · "
                      f"denetim {'tamam' if not denetim else denetim} · "
                      f"{r['sure_s']:.0f} s", flush=True)
    if kayit_yolu:
        Path(kayit_yolu).write_text(
            json.dumps({"dunya": DS.secili(), "hucre": hucre, "sinif": sinif,
                        "kisa": kisa,
                        "sonuc": sorted(sonuc, key=lambda r: (r["kol"],
                                                              r["tohum"]))},
                       ensure_ascii=False), encoding="utf-8")
    print(f"\n  {len(sonuc)} koşu kayıtta · hata {hatalar}")
    return 1 if hatalar else 0


if __name__ == "__main__":
    sys.exit(main())
