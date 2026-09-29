"""
LITERATUR EKSENLERI — paket boyutu ve kosu uzunlugu, OLCULMUS.

🔴 NEDEN BU DOSYA VAR
=====================
`v2/yeni_detaylı_arastırma/` taramasi iki eksende depodan ayriliyor:

  1. PAKET BOYUTU. `FANET Standart Simülasyon Parametreleri (N≤40).md` §4:
     *"512 bayt, MANET/FANET simulasyonlarinda STANDART KABUL edilen
     boyuttur"*; 1024 bayt "video/buyuk veri" bandinda listeleniyor.
     Depo: `Konfig.paket_bayt = 1024`.

  2. KOSU UZUNLUGU. Ayni taramanin IKI dosyasi CELISIYOR:
       `FANET Sim. Parametreleri (2021-2026).md` §B : medyan ~200 s (100-600)
       `Baseline Simülasyon Kurgusu.md` §2          : 900-1000 s
     Depo: 350 s (50 isinma + 270 olcum + 30 bosaltma).

🔴 BU BETIK BIR KARAR VERMEZ. Iki eksenin metriklere ETKISINI olcer; hangi
degerin secilecegi ogrencinindir (`03` kural 8). Amac, `11-REFACTORING-
ONERISI.md`nin *"bu degisiklik ucuz"* / *"pahali"* cumlelerinin TAHMIN degil
OLCUM olmasi.

🔴 IC ICE OLCUM — ARDISIK DEGIL (K-075, oturum hatasi 9)
========================================================
Tum kollar TEK bir `Pool` yiginina konur ve is listesi KARISTIRILIR. Ardisik
olcum bu depoda yalan soyledi: iki kod durumu 40 dk arayla olculup
*"+819 sn fark"* denmisti; ic ice olcumde gercek fark **+45 sn** cikti.
Ayni tuzak iki KONFIGURASYON arasinda da gecerlidir — makine 2,10x oynuyor.

🔴 D-13 TUZAGINA DUSMEZ
========================
`kapi_korunum.py` `Pool` alt sureclerinde `olc()` cagiriyor ve yazici orada
`None`; 540 kosu sonuc satiri YAZMIYOR (D-13). Bu betik o sekli tekrarlamaz:

    isciler  : `olc(kon, fabrika)` — yazicisiz, tam `sonuc` sozlugunu DONDURUR
    ebeveyn  : `with kayit(...)` baglaminda satirlari KENDISI yazar

Yazici bir dosya tanitiicisi tasidigi icin alt surece gecirilemez; tek dogru
sekil budur. ⚠️ Bu, D-13'un ONERILEN duzeltmesiyle ayni sekildir ama
**D-13'u UYGULAMAZ** — `kapi_korunum.py`ye dokunulmamistir (R-1, onay bekler).

Kullanim:
    PYTHONIOENCODING=utf-8 python dogrulama/literatur_eksenleri.py
    PYTHONIOENCODING=utf-8 python dogrulama/literatur_eksenleri.py --tahmin
"""

from __future__ import annotations

import random
import statistics as ist
import sys
import time
from multiprocessing import Pool, cpu_count
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dogrulama.aktaricilar import AKTARICILAR                    # noqa: E402
# 🔴 SATIR BURADA KURULMAZ, `yaz_sonuc` CAGRILIR. Onceki hali `_AYRI_ALANLAR`
# filtresini ice aktarip yazma cagrisini KENDI kuruyordu; filtre tek kaynakti
# ama CAGRI iki yerdeydi. D-13'un duzeltmesiyle cagrinin kendisi de tek
# kaynaga tasindi (`olcum.yaz_sonuc`) — B-07'nin "ikinci dogru kaynagi"
# tuzagi filtre kadar cagri icin de gecerli.
from dogrulama.olcum import kayit, olc, yaz_sonuc                # noqa: E402
from sim.config import Konfig                                     # noqa: E402

CEKIRDEK = min(10, cpu_count())        # K-002: 10 cekirdek

# 🔴 AYARLAMA TOHUMLARI (1-30). Ana deney tohumlari (2000-2029) muhurden
# once HICBIR amacla kosulmaz (K-025).
TOHUMLAR = range(1, 31)

# Karsilastirilan kollar. IKISI birden kosuluyor cunku eksenin etkisi kola
# BAGLI olabilir ve tek kolla olculen bir etki, kolun ozelligi sanilabilir
# (`03` B1: kontrol kolu olmadan etki olculmez).
KOLLAR = ("en_kisa_yol", "gurultuden_kacan")

# Kosu uzunlugu eksenleri: (ad, isinma_s, olcum_bitis_s, kosu_bitis_s)
# "kisa" = literatur medyani ~200 s; isinma AYNI birakildi (50 s) cunku
# degisen sey OLCUM PENCERESININ UZUNLUGU, isinmanin yeterliligi degil.
UZUNLUKLAR = {
    "tam":  (50.0, 320.0, 350.0),      # deponun bugunku hali
    "kisa": (50.0, 170.0, 200.0),      # literatur medyani (~200 s)
}

PAKET_BOYUTLARI = (512, 1024)


def _isler() -> list[tuple]:
    """Is listesi. Her oge: (etiket_sozlugu, konfig_kwargs, kol)."""
    isler = []
    for tohum in TOHUMLAR:
        for kol in KOLLAR:
            # --- EKSEN 1: paket boyutu (S0 ve S2, tam uzunluk) ---
            for senaryo in ("S0", "S2"):
                for bayt in PAKET_BOYUTLARI:
                    isler.append((
                        {"eksen": "paket_boyutu", "kol_adi": kol,
                         "paket_bayt": bayt, "uzunluk": "tam",
                         "senaryo_etiket": senaryo},
                        dict(senaryo=senaryo, trafik="orta", tohum=tohum,
                             paket_bayt=bayt),
                        kol,
                    ))
            # --- EKSEN 2: kosu uzunlugu (S2, 1024 B) ---
            # "tam" hali EKSEN 1'de zaten var; burada yalnizca "kisa" eklenir
            # ve karsilastirma o satirla yapilir. Ayni kosuyu iki kez
            # kosturmak makine oynakligini olcume sokardi.
            i_s, o_s, k_s = UZUNLUKLAR["kisa"]
            isler.append((
                {"eksen": "kosu_uzunlugu", "kol_adi": kol,
                 "paket_bayt": 1024, "uzunluk": "kisa",
                 "senaryo_etiket": "S2"},
                dict(senaryo="S2", trafik="orta", tohum=tohum,
                     paket_bayt=1024, isinma_s=i_s,
                     olcum_bitis_s=o_s, kosu_bitis_s=k_s),
                "gurultuden_kacan" if kol == "gurultuden_kacan" else "en_kisa_yol",
            ))
    # 🔴 IC ICE OLCUM: sira karistirilir ki bir eksen sistematik olarak
    # makinenin yavas/hizli donemine denk gelmesin.
    random.Random(20260901).shuffle(isler)
    return isler


def _kosu(arg) -> tuple[dict, dict]:
    """ISCI — yazicisiz olcer, tam sonucu DONDURUR (D-13'un dogru sekli)."""
    etiketler, kwargs, kol = arg
    kon = Konfig(kol="lit_" + etiketler["eksen"], **kwargs)
    sonuc = olc(kon, AKTARICILAR[kol], aktarici=kol)
    return etiketler, sonuc


# 🔴 B-128 (yedinci denetim) — `_yuzdelik` GOVDESI SILINDI.
# `yuzdelik` bu depoda UC ayri govdede tanimliydi ve K-086
# *"tek govde"* diyordu — YANLISTI. Ustelik `06` §8.1'in
# tablosunu ureten govde BURADAKIYDI. Tek govde artik
# `sim/karsilastirma.py`de; buradan ICE AKTARILIYOR
# (B-07'nin "ikinci dogru kaynagi" tuzagi).
from sim.karsilastirma import yuzdelik as _yuzdelik  # noqa: E402


def _ozet(satirlar: list[tuple[dict, dict]]) -> None:
    """Eslestirilmis ozet. Her tohum bir gozlem birimidir."""
    # (eksen, kol, senaryo, uzunluk, bayt) -> {tohum: sonuc}
    gruplar: dict[tuple, dict] = {}
    for et, s in satirlar:
        anahtar = (et["eksen"], et["kol_adi"], et["senaryo_etiket"],
                   et["uzunluk"], et["paket_bayt"])
        gruplar.setdefault(anahtar, {})[s["konfig"]["tohum"]] = s

    def esli(a: tuple, b: tuple, alan: str):
        """A ve B gruplarinin AYNI tohumdaki farklari."""
        ga, gb = gruplar.get(a, {}), gruplar.get(b, {})
        ortak = sorted(set(ga) & set(gb))
        farklar = []
        for t in ortak:
            va, vb = ga[t].get(alan), gb[t].get(alan)
            if va is not None and vb is not None:
                farklar.append(va - vb)
        return farklar, len(ortak)

    print()
    print("=" * 100)
    print("EKSEN 1 — PAKET BOYUTU  (512 B  -  1024 B), eslestirilmis, 30 tohum")
    print("=" * 100)
    print(format("kol", "<18s") + format("senaryo", "<9s")
          + format("metrik", "<22s")
          + format("512 ort", ">10s") + format("1024 ort", ">10s")
          + format("fark ort", ">11s") + format("fark std", ">10s")
          + format("n+", ">5s"))
    for kol in KOLLAR:
        for sen in ("S0", "S2"):
            for alan, ad in (("teslim_orani", "teslim orani"),
                             ("ortalama_gecikme_s", "ort. gecikme (s)"),
                             ("kontrol_bayt_pencere", "kontrol bayt (pencere)")):
                a = ("paket_boyutu", kol, sen, "tam", 512)
                b = ("paket_boyutu", kol, sen, "tam", 1024)
                farklar, n = esli(a, b, alan)
                if not farklar:
                    continue
                va = [v[alan] for v in gruplar[a].values() if v.get(alan) is not None]
                vb = [v[alan] for v in gruplar[b].values() if v.get(alan) is not None]
                pozitif = sum(1 for d in farklar if d > 0)
                print(format(kol, "<18s") + format(sen, "<9s")
                      + format(ad, "<22s")
                      + format(ist.mean(va), ">10.4f")
                      + format(ist.mean(vb), ">10.4f")
                      + format(ist.mean(farklar), ">11.4f")
                      + format(ist.stdev(farklar) if len(farklar) > 1 else 0.0, ">10.4f")
                      + format(str(pozitif) + "/" + str(n), ">5s"))

    print()
    print("=" * 100)
    print("EKSEN 2 — KOSU UZUNLUGU  (kisa ~200 s  -  tam 350 s), S2, 1024 B")
    print("🔴 `06` Bolum 5 kosul 1: *sonuc kosu uzunlugundan BAGIMSIZ olmali*")
    print("=" * 100)
    print(format("kol", "<18s") + format("metrik", "<22s")
          + format("kisa ort", ">10s") + format("tam ort", ">10s")
          + format("fark ort", ">11s") + format("fark std", ">10s")
          + format("n+", ">5s"))
    for kol in KOLLAR:
        for alan, ad in (("teslim_orani", "teslim orani"),
                         ("ortalama_gecikme_s", "ort. gecikme (s)")):
            a = ("kosu_uzunlugu", kol, "S2", "kisa", 1024)
            b = ("paket_boyutu", kol, "S2", "tam", 1024)
            farklar, n = esli(a, b, alan)
            if not farklar:
                continue
            va = [v[alan] for v in gruplar[a].values() if v.get(alan) is not None]
            vb = [v[alan] for v in gruplar[b].values() if v.get(alan) is not None]
            pozitif = sum(1 for d in farklar if d > 0)
            print(format(kol, "<18s") + format(ad, "<22s")
                  + format(ist.mean(va), ">10.4f")
                  + format(ist.mean(vb), ">10.4f")
                  + format(ist.mean(farklar), ">11.4f")
                  + format(ist.stdev(farklar) if len(farklar) > 1 else 0.0, ">10.4f")
                  + format(str(pozitif) + "/" + str(n), ">5s"))

    # --- GECIKME YUZDELIKLERI: semadan TUREVDIR, sema degismez ---
    print()
    print("=" * 100)
    print("GECIKME YUZDELIKLERI — `teslim_gecikmeleri_s`den TUREV (sema degismez)")
    print("🔴 `FANET'te EH...md` §3.2 + RFC 7679: karistirmada ORTALAMA gecikme")
    print("   hayatta-kalan yanliligi tasir; yuzdelikler raporlanmali.")
    print("=" * 100)
    print(format("kol", "<18s") + format("senaryo", "<9s")
          + format("teslim", ">8s") + format("ort (ms)", ">10s")
          + format("p50 (ms)", ">10s") + format("p95 (ms)", ">10s")
          + format("p99 (ms)", ">10s"))
    for kol in KOLLAR:
        for sen in ("S0", "S2"):
            g = gruplar.get(("paket_boyutu", kol, sen, "tam", 1024), {})
            havuz = [d for s in g.values()
                     for d in (s.get("teslim_gecikmeleri_s") or [])]
            if not havuz:
                continue
            teslimler = [s["teslim_orani"] for s in g.values()
                         if s.get("teslim_orani") is not None]
            print(format(kol, "<18s") + format(sen, "<9s")
                  + format(ist.mean(teslimler), ">8.4f")
                  + format(1e3 * ist.mean(havuz), ">10.3f")
                  + format(1e3 * _yuzdelik(havuz, 0.50), ">10.3f")
                  + format(1e3 * _yuzdelik(havuz, 0.95), ">10.3f")
                  + format(1e3 * _yuzdelik(havuz, 0.99), ">10.3f"))


def main(argv: list[str]) -> int:
    isler = _isler()
    print("LITERATUR EKSENLERI")
    print("is sayisi: " + str(len(isler)) + " tam kosu | cekirdek: "
          + str(CEKIRDEK) + " | tohum: " + str(TOHUMLAR.start) + "-"
          + str(TOHUMLAR.stop - 1))

    # 🔴 `03` kural 7 — SURE TAHMINI ONCE YAZDIRILIR.
    # Tek bir kosu olculur; bant makinenin OLCULMUS 2,10x oynakligindan
    # turetilir (K-075), tek nokta tahmini yazilmaz.
    # 🔴 F-9 — KALİBRASYON TEK İŞTE YAPILMAZ.
    # `pencere_kapsami.py`de ölçüldü: tek işten kurulan tahmin 900
    # koşu için "1,8-3,8 dk" dedi, koşu 10 dk'da BİTMEDİ. Maliyet
    # KOL ve TRAFİĞE bağlı; tek örnek onu temsil etmiyor. Bu, deponun
    # "süre tahmini beş kez tutmadı" örüntüsünün altıncısıydı ve
    # `03` kural 7'yi doğrudan zayıflatıyor: iyimser bir tahmin,
    # SORULMASI GEREKEN bir koşuyu sorulmadan başlatır.
    ornekler = [next(i for i in isler if i[0]["kol_adi"] == kol)
                for kol in KOLLAR]
    t0 = time.perf_counter()
    for o in ornekler:
        _kosu(o)
    tek = (time.perf_counter() - t0) / len(ornekler)
    alt = len(isler) * tek / CEKIRDEK / 60.0
    print("kalibrasyon: " + str(len(ornekler)) + " kol ortalamasi "
          + format(tek, ".2f") + " sn/kosu")
    print("TAHMIN BANDI: " + format(alt, ".1f") + " - "
          + format(alt * 2.10, ".1f") + " dk  (2,10x makine oynakligi, K-075)")
    if "--tahmin" in argv:
        print("(--tahmin: yalnizca tahmin istendi, kosulmadi)")
        return 0
    if alt * 2.10 > 30.0:
        print()
        print("🔴 UST BANT 30 DK'YI ASIYOR — `03` kural 7 geregi DURULDU.")
        print("   Ogrenciye sorulmadan kosulmaz. Devam icin: --zorla")
        if "--zorla" not in argv:
            return 2

    bas = time.perf_counter()
    # 🔴 Yazici EBEVEYNDE acilir; isciler yazmaz, DONDURUR (D-13).
    with kayit("literatur_eksenleri") as yazici:
        with Pool(CEKIRDEK) as p:
            satirlar = []
            for etiketler, sonuc in p.imap_unordered(_kosu, isler, chunksize=1):
                yaz_sonuc(sonuc, yazici=yazici, **etiketler)
                satirlar.append((etiketler, sonuc))
        yazilan = yazici.yazilan
    sure = (time.perf_counter() - bas) / 60.0

    print("kosuldu: " + format(sure, ".1f") + " dk | yazilan satir: "
          + str(yazilan))

    # 🔴 Sozlesme 5'in DAVRANISSAL dogrulamasi: satir SAYISI ise esit mi?
    # "`kayit()` kuruldu" demek yetmez — D-13 tam olarak oyle gozden kacti.
    assert yazilan == len(isler), (
        "yazilan satir (" + str(yazilan) + ") is sayisina (" + str(len(isler))
        + ") esit degil — D-13 sinifi bir kacak var")

    bozuk = [e for e, s in satirlar if not s["korunum"]["korunum_tamam"]]
    print("korunum: " + str(len(satirlar) - len(bozuk)) + "/"
          + str(len(satirlar)) + " tamam")

    _ozet(satirlar)
    return 0


if __name__ == "__main__":        # 🔴 Windows `spawn` — devir teslim §0.2
    raise SystemExit(main(sys.argv[1:]))
