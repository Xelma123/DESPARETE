"""
VERİ ONAYI SEMANTİĞİNİN ETKİSİ — seyirci kredisi kalibrasyon sayılarını ne kadar oynatıyor?

Üretici:
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/onay_semantigi.py --kapi [--tohum N]
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/onay_semantigi.py olc <etiket> [--tohum N] [--tam] [--devam]
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/onay_semantigi.py analiz <etiket>
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/onay_semantigi.py y2kapi <etiket> [--tohum N]

Bağlam: `v2/13-KONTROL-DUZLEMI.md` §06 R1 · K-112 §3 · K-113/K-114 — öğrenci
kararı: *"önce etkisini ayrı ölçelim, sonra karar verelim."*

🔴 NE ÖLÇÜLÜYOR
===============
Veri yolunda bir onay çerçevesi, onu ÇÖZEN herhangi bir düğümde işleniyor:
işleyici onayı kimin çözdüğünü sormuyor. Aynı anda biten alımlar düğüm
sırasıyla işlendiği için, onayı ilk çözen SEYİRCİ göndereni "başarılı"
sayabiliyor — gönderen o onayı hiç çözemese bile. Kontrol düzlemindeki onay
bunu doğru yapıyor (yalnız gönderenin kendisi).

Bu betik iki semantiği AYNI tohum, AYNI senaryo ve AYNI kâhinle koşar:

  · mevcut      — bugünkü kod. Bir `Kosu` alt sınıfıyla koşulur ama davranış
                  birebir aynıdır (kapı 1 bunu sınar); alt sınıf yalnız sayar.
  · duzeltilmis — veri onayı YALNIZ gönderenin kendisi çözdüğünde işlenir.

`sim2/`ye dokunulmaz: iki semantiğin tek farkı, olay döngüsünün çerçeve-bitti
işleyicisinin onay dalındadır.

Sayılanlar:
  · seyirci kredisi — onayı gönderenden BAŞKA bir düğüm işledi ve gönderen o
    anda gerçekten o onayı bekliyordu, yani kredi verildi
  · hayalet kredi   — seyirci kredilendirdi VE gönderenin kendi alıcısı o onay
    çerçevesini hiç çözemedi (K-112'nin tanımı)

🔒 KARAR ÖLÇÜTÜ — ÖLÇÜMDEN ÖNCE YAZILDI (10 Eylül 2026)
======================================================
Kalibrasyon sayıları kâhin kollarında üretiliyor; soru, düzeltmenin onları
deneyin görebileceği kadar oynatıp oynatmadığıdır. Her (senaryo, kâhin,
metrik) için tohum başına eşleştirilmiş fark d = düzeltilmiş − mevcut:

    |ort(d)| + 2·SE(d) <  R   → ÇÖZÜNÜRLÜK ALTINDA  (kayıtlı sayılar ayakta)
    |ort(d)| − 2·SE(d) >  R   → ÇÖZÜNÜRLÜK ÜSTÜNDE  (etkilenen kalibrasyonlar
                                 düzeltmeden sonra yeniden koşulur)
    arada                     → KARAR YOK            (tohum artırılır)

R = `COZUNURLUK_R`, 40 tohumluk çözünürlük. Karar metrikleri PDR biriminde
olanlardır: `pdr_pencere` · `sok_derinligi` · `toparlanma_tamligi` (son ikisi
yalnız tam uzunlukta tanımlı). PSR ve MAC sayaçları tanımları gereği değişir;
betimleyici raporlanır.

⚠️ Bir hücrede mevcut kolda seyirci kredisi hiç yoksa o hücrenin farkı tanım
gereği sıfırdır ve "etki yok" DEĞİL "kusur bu hücrede tetiklenmedi" diye
raporlanır (K-110'un boş geçen kapı dersi).

🔴 11 EYLÜL 2026 — İLK TASARIM DURDURULDU ve bu kayda geçer
===========================================================
İlk sürüm 160 koşuyu TAM UZUNLUKTA koşuyordu ve sonuçları yalnız sonda
basıyordu. Süreyi koşu başına ~2 dk tahmin etmiştim; gerçekte kâhin kolunda
tam uzunlukta bir koşu ~20–25 dk sürdü (hareketli kolda kâhin grafiği her
dilimde yeniden kuruluyor). 79 dakikada 32/160'a gelmişti, yani toplam ~6
saat — 30 dakikalık çalışma anlaşmasının çok üstünde. Durduruldu; sonuçlar
diske yazılmadığı için KAYBOLDU (`03` B5 "ara kayıt tutmamak").

🔒 Düzeltme üç parça:
  1. Her koşunun sonucu ANINDA `ciktilar2/onay_semantigi/<etiket>.jsonl`e
     yazılır; `--devam` yarıda kalan ölçümü kaldığı yerden sürdürür.
  2. Varsayılan ölçüm KISA pencerededir (duyarlılık denetiminin penceresi:
     karıştırıcı 5 s'de açık, ölçüm [10; 40), koşu 50 s). PDR, PSR, MAC ve
     gecikme burada tanımlıdır; evre metrikleri tanımlı değildir.
  3. Kapı koşu başına süreyi ÖLÇER ve seçilen tohum sayısı için bandı basar.
     Evre metriklerini ölçen tam uzunluk kipi (`--tam`) yalnız ETX kâhini ve
     iki karıştırıcılı kolla sınırlıdır; bandı 30 dk'yı aşıyorsa önce sorulur.

🔒 ALETİN KENDİ KAPISI (`--kapi`, kısa pencere, tek tohum)
=========================================================
  1. Düz `Kosu`, `duzeltilmis` kiple BİREBİR aynı parmak izini verir. Y2'den
     önceki kodda (11 Eylül 2026 öncesi) karşılaştırma `mevcut` kiple
     yapılıyordu, çünkü o gün düz koşu kusurlu semantiği taşıyordu.
  2. `mevcut` kolda seyirci kredisi en az bir senaryoda > 0 — kusur bu
     kurulumda gerçekten var (Y2'den sonra bilerek yeniden üretiliyor);
     yoksa ölçüm boş geçerdi.
  3. `duzeltilmis` kolda seyirci kredisi = 0 — düzeltme gerçekten uygulanıyor.
  4. Bütün koşularda korunum + mutabakat + iletim sonucu kapalı kümesi geçerli.
Kapı geçmeden ölçüm başlamaz.

🔒 Y2 KAPISI (`y2kapi <etiket>`) — `v2/07` §18 Y2
=================================================
Simülatördeki düzeltmenin, Y2'den ÖNCE ölçülmüş `duzeltilmis` kipin aynısı
olduğunu sınar: düz koşunun parmak izi, kayıttaki `duzeltilmis` satırla her
kol × kâhin × tohumda birebir aynı olmalı.
"""

from __future__ import annotations

import json
import math
import statistics as ist
import sys
import time
from multiprocessing import Pool
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.kosum.gonderim import alim_say  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.kosum.sonuc import SatirYazici, korunum_bolumu  # noqa: E402
from sim2.kosum.teslim import onay_alindi  # noqa: E402
from sim2.olcum.metrikler import metrik_sozlugu  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402
from kalibrasyon import dunya_secimi as DS  # noqa: E402  (K-183)
from kalibrasyon.kahin import (EnGuvenilirKahin,  # noqa: E402
                               EnKisaYolKahin, KanalGrafigi)

# 🔒 40 tohumluk çözünürlük — köken defterinde `OLCULMUS`.
# Üretici: `python -u kalibrasyon/cozunurluk.py --tohum 40` (10 Eylül 2026).
COZUNURLUK_R = 0.0318

DIZIN = KOK / "ciktilar2" / "onay_semantigi"

# Kalibrasyon sayılarının üretildiği kollar: iki mobilite × karıştırıcısız ve
# referans karıştırıcı sınıfı.
SENARYOLAR = ("statik-yok", "statik-surekli", "bagimsiz-yok",
              "bagimsiz-surekli")
TAM_SENARYOLAR = ("statik-surekli", "bagimsiz-surekli")
KAHINLER = {EnGuvenilirKahin.ad: EnGuvenilirKahin,
            EnKisaYolKahin.ad: EnKisaYolKahin}
KARAR_METRIKLERI = ("pdr_pencere", "sok_derinligi", "toparlanma_tamligi")
# ⚠️ `psr_pencere` 11 Eylül 2026'daki `kisa_2026-09-11` ölçümünde ONAYA DAYALI
# orandı (`mac_gonderim_basarili / mac_deneme`). Y1'den sonra (`v2/07` §18,
# K-115) aynı ad alıcı tarafındaki PSR'dir; onaya dayalı oran
# `mac_basari_orani_pencere` adını taşır. Eski dosya yeniden analiz edilirse
# sütun eski tanımla okunur.
BETIMLEYICI = ("psr_pencere", "gecikme_ort_s_pencere",
               "gecikme_p95_s_pencere", "mac_deneme", "mac_gonderim_basarili",
               "mac_onaysiz_onay", "mac_onaysiz_veri", "mac_vazgecme",
               "teslim_paket")
KIPLER = ("mevcut", "duzeltilmis")


def _kisa_pencere() -> dict:
    """Duyarlılık denetiminin penceresi — karıştırıcı ölçüm boyunca açık."""
    return dict(karistirici_baslangic_s=5.0, isinma_s=10.0,
                olcum_bitis_s=40.0, kosu_bitis_s=50.0)


# ==========================================================================
class OlcenKosu(Kosu):
    """Veri onayı dalını SAYAN ve istenirse DÜZELTEN `Kosu`.

    🔒 Onay dışındaki her çerçeve tipi hiç değişmeden `Kosu`ya gider. Onay
    dalı `Kosu._cerceve_bitti`nin satır satır aynısıdır; tek eklemeler sayım
    ve `duzeltilmis` kipte seyirci onayının işlenmemesidir.
    """

    def __init__(self, kur, protokol_fabrikasi, duzeltilmis: bool) -> None:
        super().__init__(kur, protokol_fabrikasi)
        self.duzeltilmis = duzeltilmis
        self.seyirci_kredisi = 0
        self.gonderen_kredisi = 0
        self._seyirci_kredili: set = set()
        self._gonderen_cozdu: set = set()

    def _cerceve_bitti(self, n: int, iletim, yuk) -> None:
        tip, bilgi = yuk
        if tip != "onay":
            Kosu._cerceve_bitti(self, n, iletim, yuk)
            return
        d = self.dugumler[n]
        sonuc = d.alici.cerceve_bitti(iletim, self.olaylar.simdi)
        alim_say(self, sonuc)
        if sonuc is None or not sonuc.basarili:
            return
        d.alim_kaydet(iletim.cerceve.bayt)
        hedef, ucus_no = bilgi
        # Onay çerçevesinin kimliği: kime ait, kim gönderdi, ne zaman başladı.
        anahtar = (hedef, iletim.gonderen, iletim.baslangic_s)
        g = self.dugumler[hedef]
        kabul = g.onay_bekleniyor and ucus_no == g.ucus_no
        if n == hedef:
            self._gonderen_cozdu.add(anahtar)
            if kabul:
                self.gonderen_kredisi += 1
        else:
            if self.duzeltilmis:
                return
            if kabul:
                self.seyirci_kredisi += 1
                self._seyirci_kredili.add(anahtar)
        # 🔒 Y2'den sonra (11 Eylül 2026) `teslim.onay_alindi` onayı yalnız
        # çözen düğüm göndericinin kendisiyse işler. `mevcut` kip eski kusuru
        # BİLEREK yeniden üretir: seyircinin çözdüğü onayı gönderen çözmüş
        # gibi işler. Gönderenin kendi çözdüğü onayda iki çağrı aynıdır.
        onay_alindi(self, hedef, bilgi)

    @property
    def hayalet_kredi(self) -> int:
        """Seyircinin kredilendirdiği ve gönderenin hiç çözemediği onaylar."""
        return len(self._seyirci_kredili - self._gonderen_cozdu)


# ==========================================================================
def _kos(senaryo: str, tohum: int, kahin: str, kip: str,
         pencere: dict) -> dict:
    """Tek koşu. `kip`: `duz` (saf `Kosu`) · `mevcut` · `duzeltilmis`."""
    kfg = DS.konfig(kol="onay_semantigi", senaryo=senaryo, tohum=tohum,
                 **pencere)
    kur = kurulum_yap(kfg)
    grafik = KanalGrafigi(kur)
    tip = KAHINLER[kahin]

    def fabrika(i):
        return tip(i, grafik)

    if kip == "duz":
        kosu = Kosu(kur, fabrika)
    else:
        kosu = OlcenKosu(kur, fabrika, duzeltilmis=(kip == "duzeltilmis"))
    t0 = time.perf_counter()
    kosu.kostur()
    sure = time.perf_counter() - t0
    m = metrik_sozlugu(kur.sayaclar.disa_ver(), kur.paket_defteri,
                       kur.rota_defteri,
                       acilma_s=kfg.karistirici_baslangic_s)
    k = korunum_bolumu(kur, kosu.dugumler)
    olcen = isinstance(kosu, OlcenKosu)
    cikti = {ad: m.get(ad) for ad in KARAR_METRIKLERI + BETIMLEYICI}
    cikti.update(
        gecerli=bool(k["gecerli"]),
        sure_s=sure,
        seyirci_kredisi=kosu.seyirci_kredisi if olcen else None,
        gonderen_kredisi=kosu.gonderen_kredisi if olcen else None,
        hayalet_kredi=kosu.hayalet_kredi if olcen else None,
        # PARMAK İZİ — kapı 1: alt sınıf ölçüleni değiştiriyor mu?
        iz=[m.get("teslim_paket"), m.get("mac_deneme"),
            m.get("kontrol_cerceve"), m.get("mac_gonderim_basarili"),
            repr(m.get("gecikme_ort_s_pencere")), repr(m.get("pdr_pencere"))],
    )
    return cikti


def _is(gorev):
    """Havuz işçisi. 🔒 Modül düzeyinde — Windows `spawn` başka türlü seçemez."""
    try:
        return gorev, _kos(*gorev), None
    except Exception as hata:                       # noqa: BLE001
        return gorev, None, f"{type(hata).__name__}: {hata}"


def _baslik(metin: str) -> None:
    print()
    print("=" * 96)
    print(metin)
    print("=" * 96)


def _gorevler(tohum_sayisi: int, tam: bool) -> list[tuple]:
    tohumlar = range(1000, 1000 + tohum_sayisi)
    if tam:
        return [(s, t, EnGuvenilirKahin.ad, kip, {})
                for t in tohumlar for s in TAM_SENARYOLAR for kip in KIPLER]
    return [(s, t, k, kip, _kisa_pencere())
            for t in tohumlar for s in SENARYOLAR
            for k in KAHINLER for kip in KIPLER]


# ==========================================================================
def kapi(isci: int, tohum_sayisi: int) -> bool:
    """Aletin kendi dört kapısı + koşu başına süre ve ölçüm bandı."""
    _baslik("K - ALETIN KENDI KAPISI  (kisa pencere · tek tohum · ETX kahini)")
    kahin = EnGuvenilirKahin.ad
    senaryolar = ("statik-surekli", "bagimsiz-surekli")
    gorevler = [(s, 1000, kahin, kip, _kisa_pencere())
                for s in senaryolar for kip in ("duz",) + KIPLER]
    with Pool(min(isci, len(gorevler))) as havuz:
        ham = havuz.map(_is, gorevler, chunksize=1)
    sonuc = {(g[0], g[3]): (c, h) for g, c, h in ham}

    hatalar = [(g, h) for g, c, h in ham if h is not None]
    for g, h in hatalar:
        print(f"  🔴 {g[0]} {g[3]}: {h}")
    if hatalar:
        return False

    g1 = g3 = g4 = True
    # 🔒 Y2'den sonra (11 Eylül 2026) düz `Kosu` DÜZELTİLMİŞ semantiği taşır;
    # kapı 1 düz koşuyu `duzeltilmis` kiple karşılaştırır. Y2'den önce
    # `mevcut` kiple karşılaştırıyordu — K-114 §4.2'deki ölçüm o kodla koştu.
    print(f"  {'senaryo':<18} {'iz duz==duzelt.':>15} {'seyirci(mevcut)':>16} "
          f"{'hayalet':>8} {'seyirci(duzelt.)':>17} {'gecerli':>8} "
          f"{'sure_s':>8}")
    for s in senaryolar:
        duz = sonuc[(s, "duz")][0]
        mev = sonuc[(s, "mevcut")][0]
        dzl = sonuc[(s, "duzeltilmis")][0]
        ayni = duz["iz"] == dzl["iz"]
        gecerli = duz["gecerli"] and mev["gecerli"] and dzl["gecerli"]
        g1 = g1 and ayni
        g3 = g3 and dzl["seyirci_kredisi"] == 0
        g4 = g4 and gecerli
        print(f"  {s:<18} {'EVET' if ayni else 'HAYIR':>15} "
              f"{mev['seyirci_kredisi']:>16} {mev['hayalet_kredi']:>8} "
              f"{dzl['seyirci_kredisi']:>17} "
              f"{'EVET' if gecerli else 'HAYIR':>8} {mev['sure_s']:>8.1f}")
    g2 = any(sonuc[(s, "mevcut")][0]["seyirci_kredisi"] > 0
             for s in senaryolar)
    print()
    for ad, ok in (("1) duz kosu = duzeltilmis kip (Y2)", g1),
                   ("2) kusur bu kurulumda tetikleniyor", g2),
                   ("3) duzeltme uygulaniyor", g3),
                   ("4) korunum + mutabakat + iletim sonucu", g4)):
        print(f"  {ad:<42} {'OK' if ok else '🔴 KALDI'}")
    hepsi = g1 and g2 and g3 and g4

    # 🔒 SÜRE ÖLÇÜLÜR, TAHMİN EDİLMEZ — ilk tasarımın dersi.
    # Bant katsayıları da ölçümden: bu aletin kısa ölçümü `n · en_uzun / isci`nin
    # 1,21 katı (80 koşu, 28,0 dk) ve 1,27 katı (48 koşu, 17,3 dk) sürdü
    # (K-114 §4.2). İlk sürümün 0,6–1,3 bandı ancak yetmişti.
    en_uzun = max(c["sure_s"] for c, _ in sonuc.values())
    n_kisa = len(_gorevler(tohum_sayisi, tam=False))
    merkez = n_kisa * en_uzun / isci / 60
    print()
    print(f"  kisa pencerede en uzun kosu : {en_uzun:.1f} s")
    print(f"  {tohum_sayisi} tohumla kisa olcum ({n_kisa} kosu, {isci} isci) "
          f"· BANT {merkez * 0.9:.0f}–{merkez * 1.6:.0f} dk "
          f"(tum kosular; --devam'da yalniz kalanlar kosar)")
    print()
    print(f"  {'🟢 KAPI GECTI' if hepsi else '🔴 KAPI GECMEDI'}")
    return hepsi


# ==========================================================================
def olc(etiket: str, tohum_sayisi: int, isci: int, tam: bool,
        devam: bool) -> int:
    yol = DIZIN / f"{etiket}.jsonl"
    if yol.exists() and not devam:
        print(f"  🔴 {yol} zaten var. Kaldigi yerden surdurmek icin --devam.")
        return 1
    gorevler = _gorevler(tohum_sayisi, tam)
    yapilmis = set(_oku(etiket)) if yol.exists() else set()
    kalan = [g for g in gorevler if (g[0], g[2], g[3], g[1]) not in yapilmis]
    _baslik(f"O - ONAY SEMANTIGI  ({'TAM UZUNLUK' if tam else 'KISA PENCERE'}"
            f" · {len(gorevler)} kosu · kalan {len(kalan)} · {yol.name})")
    t0 = time.perf_counter()
    hata_sayisi = 0
    adim = max(1, len(kalan) // 10)
    with SatirYazici(yol) as yazici, Pool(isci) as havuz:
        for i, (g, c, h) in enumerate(
                havuz.imap_unordered(_is, kalan, chunksize=1), start=1):
            if h is not None:
                hata_sayisi += 1
                print(f"  🔴 HATA {g[:4]}: {h}")
            else:
                # 🔒 ANINDA YAZILIR — ilk tasarımın kaybettiği şey.
                yazici.yaz({"senaryo": g[0], "tohum": g[1], "kahin": g[2],
                            "kip": g[3], "cikti": c})
            if i % adim == 0 or i == len(kalan):
                print(f"  ilerleme {i}/{len(kalan)} · "
                      f"{(time.perf_counter() - t0) / 60.0:.1f} dk",
                      flush=True)
    if hata_sayisi:
        print(f"  🔴 {hata_sayisi} kosu hata verdi")
    return analiz(etiket)


def _oku(etiket: str) -> dict:
    degerler: dict = {}
    with open(DIZIN / f"{etiket}.jsonl", encoding="utf-8") as dosya:
        for metin in dosya:
            s = json.loads(metin)
            degerler[(s["senaryo"], s["kahin"], s["kip"], s["tohum"])] = \
                s["cikti"]
    return degerler


def _esli(degerler: dict, senaryo: str, kahin: str, metrik: str
          ) -> tuple[float, float, float, float, int] | None:
    """(ort mevcut, ort düzeltilmiş, ort fark, 2·SE fark, n) — eşleştirilmiş."""
    tohumlar = sorted({a[3] for a in degerler if a[0] == senaryo
                       and a[1] == kahin})
    cift = []
    for t in tohumlar:
        a = degerler.get((senaryo, kahin, "mevcut", t))
        b = degerler.get((senaryo, kahin, "duzeltilmis", t))
        if a is None or b is None:
            continue
        x, y = a.get(metrik), b.get(metrik)
        if x is None or y is None:
            continue
        cift.append((float(x), float(y)))
    if not cift:
        return None
    farklar = [y - x for x, y in cift]
    n = len(farklar)
    se2 = 2.0 * ist.stdev(farklar) / math.sqrt(n) if n > 1 else math.inf
    return (ist.mean(x for x, _ in cift), ist.mean(y for _, y in cift),
            ist.mean(farklar), se2, n)


def _karar(fark: float, se2: float) -> str:
    if abs(fark) + se2 < COZUNURLUK_R:
        return "COZUNURLUK ALTINDA"
    if abs(fark) - se2 > COZUNURLUK_R:
        return "🔴 COZUNURLUK USTUNDE"
    return "⚠️ KARAR YOK"


def analiz(etiket: str) -> int:
    degerler = _oku(etiket)
    _baslik(f"A - ANALIZ  ({etiket} · {len(degerler)} kosu · "
            f"R = {COZUNURLUK_R})")
    gecersiz = sum(1 for c in degerler.values() if not c["gecerli"])
    print(f"  gecersiz kosu : {gecersiz}")
    if degerler:
        print(f"  kosu basina   : ort {ist.mean(c['sure_s'] for c in degerler.values()):.1f} s"
              f" · en uzun {max(c['sure_s'] for c in degerler.values()):.1f} s")
    hucreler = sorted({(a[0], a[1]) for a in degerler})
    ozet = []
    for s, k in hucreler:
        _baslik(f"{s} · {k}")
        mev = [c for a, c in degerler.items()
               if a[0] == s and a[1] == k and a[2] == "mevcut"]
        seyirci = ist.mean(c["seyirci_kredisi"] for c in mev) if mev else 0.0
        hayalet = ist.mean(c["hayalet_kredi"] for c in mev) if mev else 0.0
        gonderen = ist.mean(c["gonderen_kredisi"] for c in mev) if mev else 0.0
        print(f"  mevcut kolda kredi (tohum ort.): gonderen {gonderen:.1f} · "
              f"seyirci {seyirci:.1f} · hayalet {hayalet:.1f}")
        print(f"  {'metrik':<24} {'mevcut':>12} {'duzeltilmis':>12} "
              f"{'fark':>12} {'2SE':>10} {'n':>3}  karar")
        for metrik in KARAR_METRIKLERI + BETIMLEYICI:
            r = _esli(degerler, s, k, metrik)
            if r is None:
                print(f"  {metrik:<24} {'—':>12}  (bu kipte tanimli degil)")
                continue
            a, b, fark, se2, n = r
            if metrik in KARAR_METRIKLERI:
                karar = _karar(fark, se2) if seyirci > 0 else \
                    "KUSUR TETIKLENMEDI"
                ozet.append((s, k, metrik, fark, se2, karar))
            else:
                karar = "(betimleyici)"
            print(f"  {metrik:<24} {a:>12.5g} {b:>12.5g} {fark:>+12.5g} "
                  f"{se2:>10.3g} {n:>3}  {karar}")
    _baslik("OZET — karar metrikleri")
    for s, k, metrik, fark, se2, karar in ozet:
        print(f"  {s:<18} {k:<20} {metrik:<20} {fark:>+9.5f} "
              f"±{se2:<8.5f} {karar}")
    ustunde = sum(1 for o in ozet if "USTUNDE" in o[5])
    kararsiz = sum(1 for o in ozet if "KARAR YOK" in o[5])
    print()
    print(f"  cozunurluk ustunde : {ustunde} · karar yok : {kararsiz} · "
          f"toplam : {len(ozet)}")
    return 0


# ==========================================================================
def y2_kapisi(etiket: str, isci: int, tohum_sayisi: int) -> bool:
    """Y2 kapısı — `sim2`deki düzeltme, ölçülen `duzeltilmis` kipin AYNISI mı?

    🔒 Karşılaştırılan şey, Y2'den ÖNCE kod değişmeden kaydedilmiş satırlardır
    (`<etiket>.jsonl`, kip `duzeltilmis`). Bugünkü düz `Kosu` aynı kol, kâhin
    ve tohumda aynı parmak izini vermiyorsa düzeltme ölçülenden farklı bir şey
    yapıyordur. Aradaki Y1'in davranışı değiştirmediği ayrıca regresyonla
    denetlenir (K-115).
    """
    kayit = _oku(etiket)
    gorevler = [(s, t, k, "duz", _kisa_pencere())
                for t in range(1000, 1000 + tohum_sayisi)
                for s in SENARYOLAR for k in KAHINLER]
    _baslik(f"Y2 - DUZ KOSU = KAYITLI DUZELTILMIS KIP  ({etiket} · "
            f"{len(gorevler)} kosu)")
    eksik = [g[:3] for g in gorevler
             if (g[0], g[2], "duzeltilmis", g[1]) not in kayit]
    if eksik:
        for g in eksik:
            print(f"  🔴 kayitta yok: {g}")
        return False
    with Pool(min(isci, len(gorevler))) as havuz:
        ham = havuz.map(_is, gorevler, chunksize=1)
    hepsi = True
    for g, c, h in ham:
        if h is not None:
            print(f"  🔴 {g[:3]}: {h}")
            hepsi = False
            continue
        beklenen = kayit[(g[0], g[2], "duzeltilmis", g[1])]["iz"]
        ayni = c["iz"] == beklenen and c["gecerli"]
        hepsi = hepsi and ayni
        print(f"  {g[0]:<18} {g[2]:<20} tohum {g[1]}  "
              f"{'BIREBIR' if ayni else '🔴 FARKLI'}")
        if not ayni:
            print(f"      bugun   : {c['iz']} · gecerli {c['gecerli']}")
            print(f"      kayitli : {beklenen}")
    print()
    print(f"  {'🟢 Y2 KAPISI GECTI' if hepsi else '🔴 Y2 KAPISI GECMEDI'}")
    return hepsi


if __name__ == "__main__":
    # 🔒 Windows `spawn` korumasi — Pool bu blok disinda acilmaz.
    arguman = sys.argv[1:]
    isci_sayisi = 10
    tohum = 8
    if "--tohum" in arguman:
        tohum = int(arguman[arguman.index("--tohum") + 1])
    if len(arguman) >= 2 and arguman[0] == "y2kapi":
        raise SystemExit(0 if y2_kapisi(
            arguman[1], isci_sayisi,
            tohum if "--tohum" in arguman else 2) else 1)
    if "--kapi" in arguman:
        raise SystemExit(0 if kapi(isci_sayisi, tohum) else 1)
    if len(arguman) >= 2 and arguman[0] == "analiz":
        raise SystemExit(analiz(arguman[1]))
    if len(arguman) >= 2 and arguman[0] == "olc":
        if not kapi(isci_sayisi, tohum):
            print("  🔴 KAPI GECMEDI — olcum baslatilmadi")
            raise SystemExit(1)
        raise SystemExit(olc(arguman[1], tohum, isci_sayisi,
                             tam="--tam" in arguman,
                             devam="--devam" in arguman))
    print(__doc__)
    raise SystemExit(2)
