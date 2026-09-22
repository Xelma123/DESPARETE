"""
ÜST REFERANS — teslim olasılığı kâhini ve kâhin zarfı.

Üretici:
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/ust_referans.py --kapi [--tohum N]
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/ust_referans.py olc <etiket> [--tohum N] [--devam]
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/ust_referans.py analiz <etiket>
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/ust_referans.py teshis [--profil]

Bağlam: `v2/07-SIMULATOR-TASARIMI.md` §07.2 · §18 Y9 · K-110 (tavan iddiası
çürüdü) · K-114 — öğrenci: *"bu iddia önemli; istatistik sunulurken üst
referans verilmesi güzel olur"* (öneri onaylandı).

🔴 SORUN
========
ETX kâhini beklenen İLETİM sayısını küçültür, TESLİM olasılığını değil.
Yeniden deneme sınırı sonlu olduğu için toplam ETX'i düşük bir yol, beş
denemede de geçemeyen bir bağ taşıyabilir. K-110'da ölçüldü: atlama kâhini,
bağ eşiği 0,99'da 15 tohumun 6'sında ETX kâhinini geçti.

🔒 ÖNERİ — TESLİM OLASILIĞI KÂHİNİ
=================================
Bir bağın deneme sınırı içinde geçme olasılığı `s = 1 − (1 − p)^(sınır+1)`;
bir yolun uçtan uca teslim olasılığı `Π s`. Kâhin `Σ −ln s`yi en küçük yapan
yolu seçer; eşit olasılıklı yollar arasında daha az atlamalı olanı (sözlük
sırası — serbest parametre yok). `p`, kâhin grafiğinin ETX değerlerinden geri
türetilir (`p = 1/ETX`) — K-110'un bağ kümesi aletinde kullanılan yöntem.
Kanal İKİNCİ KEZ hesaplanmaz.

🔒 KÂHİN ZARFI — raporlanacak üst referans
==========================================
Tohum başına üç kâhinin en yüksek PDR'si. Dürüst adı "üst referans (kâhin)":
KESİN BİR SINIR DEĞİLDİR. Kâhin grafiği MAC çekişmesini, kuyruğu ve girişim
dinamiğini görmez; bir protokolün referansı geçmesi bir kusur işareti
değildir ve öyle raporlanır.

⚠️ ÖLÇÜLDÜ (11 Eylül 2026, `teshis`, tek tohum): teslim olasılığı kâhini iyi
bağlı UZUN yolları seçer, çünkü `−ln s` iyi bağda ~0'dır. bagimsiz-surekli'de
paket başına atlama isteği 4,65 (ETX 1,97), PDR +0,057, ortalama gecikme ~3,3
kat. Zarf PDR İÇİN üst referanstır, gecikme için değil. Atlama cezası
eklenmedi: serbest parametre olurdu.

🔒 KARAR ÖLÇÜTÜ — ÖLÇÜMDEN ÖNCE YAZILDI (11 Eylül 2026)
======================================================
  · Her durumda raporlanan üst referans kâhin ZARFIDIR.
  · Teslim olasılığı kâhini, TEK BAŞINA referans kâhin olarak ETX kâhininin
    yerine geçer ⇔ her kolda (a) zarfı veren tohum oranı ETX kâhininkinden
    düşük değil VE (b) eşleştirilmiş ortalama fark (teslim − ETX) − 2·SE
    > −R. R = 40 tohumluk çözünürlük (`onay_semantigi.COZUNURLUK_R` ile aynı
    kaynak; burada ayrıca kopyalanmaz).

⚠️ GEÇİCİ YER — beyan edilir
============================
Sınıflar bugünkü kâhin modülüne ALT SINIF olarak burada yazıldı ki o modül bu
ölçüm sırasında değişmesin. Üst referans benimsenirse `kalibrasyon/kahin.py`ye
taşınır ve iki Dijkstra tek gövdeye indirilir. O zamana kadar ikinci Dijkstra
bu dosyadadır.

🔒 ALETİN KENDİ KAPISI (`--kapi`, kısa pencere, tek tohum)
=========================================================
  1. Alt sınıf grafiğinde ETX ve atlama kâhinlerinin parmak izi, bugünkü
     grafikteki ile BİREBİR aynı — alt sınıf mevcut kâhinleri değiştirmiyor.
  2. Teslim olasılığı kâhini en az bir senaryoda ETX kâhininden FARKLI bir
     parmak izi veriyor — aynıysa yeni kâhin hiçbir şey ölçmüyor demektir.
  3. Bütün koşularda korunum + mutabakat + iletim sonucu geçerli.
"""

from __future__ import annotations

import cProfile
import heapq
import io
import json
import math
import pstats
import statistics as ist
import sys
import time
from multiprocessing import Pool
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.gozlem.karar import Karar  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.kosum.sonuc import SatirYazici, korunum_bolumu  # noqa: E402
from sim2.olcum.metrikler import metrik_sozlugu  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402
from kalibrasyon.kahin import (ETX_TAVANI, EnGuvenilirKahin,  # noqa: E402
                               EnKisaYolKahin, KanalGrafigi, _KahinTabani)
from kalibrasyon.onay_semantigi import COZUNURLUK_R  # noqa: E402

DIZIN = KOK / "ciktilar2" / "ust_referans"
SENARYOLAR = ("statik-yok", "statik-surekli", "bagimsiz-yok",
              "bagimsiz-surekli")
METRIKLER = ("pdr_pencere", "psr_pencere", "gecikme_ort_s_pencere",
             "gecikme_p95_s_pencere", "mac_deneme", "teslim_paket")


# ==========================================================================
class TeslimGrafigi(KanalGrafigi):
    """Kâhin grafiği + bağ başına teslim olasılığı ağırlığı.

    🔒 Kanal yeniden hesaplanmaz: ağırlık, üst sınıfın ETX değerlerinden geri
    türetilir (`p = 1/ETX`). ETX tavanındaki (p ≈ 0) bağlar dışarıda kalır.
    """

    __slots__ = ("_teslim_agirlik",)

    def __init__(self, kur, dilim_s: float | None = None) -> None:
        super().__init__(kur, dilim_s)
        self._teslim_agirlik: list[dict[int, float]] = []

    def _kur(self, t_s: float) -> None:
        super()._kur(t_s)
        deneme = self.kur.konfig.yeniden_deneme_siniri + 1
        agirlik: list[dict[int, float]] = []
        for komsular in self._etx:
            satir: dict[int, float] = {}
            for j, etx in komsular.items():
                if etx >= ETX_TAVANI:
                    continue
                s = 1.0 - (1.0 - 1.0 / etx) ** deneme
                if s > 0.0:
                    satir[j] = -math.log(s)
            agirlik.append(satir)
        self._teslim_agirlik = agirlik

    def en_olasi_teslim_sonraki(self, kaynak: int, hedef: int) -> int | None:
        """En yüksek uçtan uca teslim olasılığı; eşitlikte en az atlama."""
        self._tazele(self.kur.olaylar.simdi)
        if kaynak == hedef:
            return None
        n = self.kur.dugum_sayisi
        uzaklik: list[tuple[float, int]] = [(math.inf, 0)] * n
        onceki: list[int | None] = [None] * n
        uzaklik[kaynak] = (0.0, 0)
        yigin: list[tuple[float, int, int]] = [(0.0, 0, kaynak)]
        gorulen = [False] * n
        while yigin:
            w, h, u = heapq.heappop(yigin)
            if gorulen[u]:
                continue
            gorulen[u] = True
            if u == hedef:
                break
            for v, agirlik in self._teslim_agirlik[u].items():
                yeni = (w + agirlik, h + 1)
                if yeni < uzaklik[v]:
                    uzaklik[v] = yeni
                    onceki[v] = u
                    heapq.heappush(yigin, (yeni[0], yeni[1], v))
        if uzaklik[hedef][0] == math.inf or onceki[hedef] is None:
            return None
        dugum = hedef
        while onceki[dugum] != kaynak:
            dugum = onceki[dugum]  # type: ignore[assignment]
            if dugum is None:
                return None
        return dugum


class EnOlasiTeslimKahin(_KahinTabani):
    """KÂHİN — mükemmel bağ bilgisi, EN YÜKSEK TESLİM OLASILIĞI ölçütü."""

    ad = "en_olasi_teslim_kahin"
    __slots__ = ()

    def sonraki_atlama(self, gozlem) -> Karar:
        if gozlem.paket is None:
            return Karar()
        return Karar(sonraki=self._grafik.en_olasi_teslim_sonraki(
            self.kimlik, gozlem.paket.hedef))


KAHINLER = {EnGuvenilirKahin.ad: EnGuvenilirKahin,
            EnKisaYolKahin.ad: EnKisaYolKahin,
            EnOlasiTeslimKahin.ad: EnOlasiTeslimKahin}


# ==========================================================================
def _kisa_pencere() -> dict:
    """Duyarlılık denetiminin penceresi — karıştırıcı ölçüm boyunca açık."""
    return dict(karistirici_baslangic_s=5.0, isinma_s=10.0,
                olcum_bitis_s=40.0, kosu_bitis_s=50.0)


def _kos(senaryo: str, tohum: int, kahin: str, grafik_turu: str) -> dict:
    """Tek koşu. `grafik_turu`: `eski` (bugünkü grafik) · `yeni` (alt sınıf)."""
    kfg = Konfig(kol="ust_referans", senaryo=senaryo, tohum=tohum,
                 **_kisa_pencere())
    kur = kurulum_yap(kfg)
    grafik = TeslimGrafigi(kur) if grafik_turu == "yeni" else KanalGrafigi(kur)
    tip = KAHINLER[kahin]

    def fabrika(i):
        return tip(i, grafik)

    kosu = Kosu(kur, fabrika)
    t0 = time.perf_counter()
    kosu.kostur()
    sure = time.perf_counter() - t0
    m = metrik_sozlugu(kur.sayaclar.disa_ver(), kur.paket_defteri,
                       kur.rota_defteri)
    k = korunum_bolumu(kur, kosu.dugumler)
    cikti = {ad: m.get(ad) for ad in METRIKLER}
    cikti.update(gecerli=bool(k["gecerli"]), sure_s=sure,
                 iz=[m.get("teslim_paket"), m.get("mac_deneme"),
                     m.get("kontrol_cerceve"),
                     repr(m.get("gecikme_ort_s_pencere")),
                     repr(m.get("pdr_pencere"))])
    return cikti


def _is(gorev):
    """Havuz işçisi. 🔒 Modül düzeyinde — Windows `spawn`."""
    try:
        return gorev, _kos(*gorev), None
    except Exception as hata:                       # noqa: BLE001
        return gorev, None, f"{type(hata).__name__}: {hata}"


def _baslik(metin: str) -> None:
    print()
    print("=" * 96)
    print(metin)
    print("=" * 96)


def _gorevler(tohum_sayisi: int) -> list[tuple]:
    """Mevcut iki kâhin BUGÜNKÜ grafikte, yeni kâhin alt sınıf grafiğinde."""
    return [(s, t, k, "yeni" if k == EnOlasiTeslimKahin.ad else "eski")
            for t in range(1000, 1000 + tohum_sayisi)
            for s in SENARYOLAR for k in KAHINLER]


# ==========================================================================
def kapi(isci: int, tohum_sayisi: int) -> bool:
    _baslik("K - ALETIN KENDI KAPISI  (kisa pencere · tek tohum)")
    senaryolar = ("statik-surekli", "bagimsiz-surekli")
    eski_kahinler = (EnGuvenilirKahin.ad, EnKisaYolKahin.ad)
    gorevler = ([(s, 1000, k, tur) for s in senaryolar for k in eski_kahinler
                 for tur in ("eski", "yeni")]
                + [(s, 1000, EnOlasiTeslimKahin.ad, "yeni")
                   for s in senaryolar])
    with Pool(min(isci, len(gorevler))) as havuz:
        ham = havuz.map(_is, gorevler, chunksize=1)
    hatalar = [(g, h) for g, _, h in ham if h is not None]
    for g, h in hatalar:
        print(f"  🔴 {g}: {h}")
    if hatalar:
        return False
    sonuc = {(g[0], g[2], g[3]): c for g, c, _ in ham}
    g1 = all(sonuc[(s, k, "eski")]["iz"] == sonuc[(s, k, "yeni")]["iz"]
             for s in senaryolar for k in eski_kahinler)
    g2 = any(sonuc[(s, EnOlasiTeslimKahin.ad, "yeni")]["iz"]
             != sonuc[(s, EnGuvenilirKahin.ad, "eski")]["iz"]
             for s in senaryolar)
    g3 = all(c["gecerli"] for c in sonuc.values())
    for s in senaryolar:
        print(f"  {s:<18} PDR  etx {sonuc[(s, EnGuvenilirKahin.ad, 'eski')]['pdr_pencere']:.4f}"
              f" · atlama {sonuc[(s, EnKisaYolKahin.ad, 'eski')]['pdr_pencere']:.4f}"
              f" · teslim {sonuc[(s, EnOlasiTeslimKahin.ad, 'yeni')]['pdr_pencere']:.4f}")
    print()
    for ad, ok in (("1) alt sinif mevcut kahinleri degistirmiyor", g1),
                   ("2) yeni kahin farkli bir sey olcuyor", g2),
                   ("3) korunum + mutabakat + iletim sonucu", g3)):
        print(f"  {ad:<46} {'OK' if ok else '🔴 KALDI'}")
    en_uzun = max(c["sure_s"] for c in sonuc.values())
    n = len(_gorevler(tohum_sayisi))
    # Bant katsayıları ölçümden: aynı dört kolda, aynı kısa pencerede, 10
    # işçiyle veri onayı ölçümü `n · en_uzun / isci`nin 1,21 katı (80 koşu,
    # 28,0 dk) ve 1,27 katı (48 koşu, 17,3 dk) sürdü (K-114 §4.2). Eski üst
    # katsayı 1,3 ancak yetmişti.
    merkez = n * en_uzun / isci / 60
    print()
    print(f"  kisa pencerede en uzun kosu : {en_uzun:.1f} s")
    print(f"  {tohum_sayisi} tohumla olcum ({n} kosu, {isci} isci) · BANT "
          f"{merkez * 0.9:.0f}–{merkez * 1.6:.0f} dk "
          f"(tum kosular; --devam'da yalniz kalanlar kosar)")
    hepsi = g1 and g2 and g3
    print()
    print(f"  {'🟢 KAPI GECTI' if hepsi else '🔴 KAPI GECMEDI'}")
    return hepsi


def olc(etiket: str, tohum_sayisi: int, isci: int, devam: bool) -> int:
    yol = DIZIN / f"{etiket}.jsonl"
    if yol.exists() and not devam:
        print(f"  🔴 {yol} zaten var. Kaldigi yerden surdurmek icin --devam.")
        return 1
    yapilmis = set(_oku(etiket)) if yol.exists() else set()
    kalan = [g for g in _gorevler(tohum_sayisi)
             if (g[0], g[2], g[1]) not in yapilmis]
    _baslik(f"O - UST REFERANS  (kalan {len(kalan)} kosu · {yol.name})")
    t0 = time.perf_counter()
    adim = max(1, len(kalan) // 10)
    with SatirYazici(yol) as yazici, Pool(isci) as havuz:
        for i, (g, c, h) in enumerate(
                havuz.imap_unordered(_is, kalan, chunksize=1), start=1):
            if h is not None:
                print(f"  🔴 HATA {g}: {h}")
            else:
                yazici.yaz({"senaryo": g[0], "tohum": g[1], "kahin": g[2],
                            "cikti": c})
            if i % adim == 0 or i == len(kalan):
                print(f"  ilerleme {i}/{len(kalan)} · "
                      f"{(time.perf_counter() - t0) / 60.0:.1f} dk",
                      flush=True)
    return analiz(etiket)


def _oku(etiket: str) -> dict:
    degerler: dict = {}
    with open(DIZIN / f"{etiket}.jsonl", encoding="utf-8") as dosya:
        for metin in dosya:
            s = json.loads(metin)
            degerler[(s["senaryo"], s["kahin"], s["tohum"])] = s["cikti"]
    return degerler


def analiz(etiket: str) -> int:
    degerler = _oku(etiket)
    _baslik(f"A - ANALIZ  ({etiket} · {len(degerler)} kosu · R = "
            f"{COZUNURLUK_R})")
    print(f"  gecersiz kosu : {sum(1 for c in degerler.values() if not c['gecerli'])}")
    etx, atl, tes = (EnGuvenilirKahin.ad, EnKisaYolKahin.ad,
                     EnOlasiTeslimKahin.ad)
    benimsenir = True
    for s in SENARYOLAR:
        tohumlar = sorted({a[2] for a in degerler if a[0] == s})
        tam = [t for t in tohumlar
               if all((s, k, t) in degerler for k in (etx, atl, tes))]
        if not tam:
            continue
        pdr = {k: [float(degerler[(s, k, t)]["pdr_pencere"]) for t in tam]
               for k in (etx, atl, tes)}
        zarf = [max(pdr[k][i] for k in pdr) for i in range(len(tam))]
        pay = {k: sum(1 for i in range(len(tam)) if pdr[k][i] == zarf[i])
               / len(tam) for k in pdr}
        gecilen = sum(1 for i in range(len(tam))
                      if max(pdr[etx][i], pdr[atl][i]) > pdr[tes][i])
        fark = [pdr[tes][i] - pdr[etx][i] for i in range(len(tam))]
        n = len(fark)
        se2 = 2.0 * ist.stdev(fark) / math.sqrt(n) if n > 1 else math.inf
        ort_fark = ist.mean(fark)
        kosul_a = pay[tes] >= pay[etx]
        kosul_b = ort_fark - se2 > -COZUNURLUK_R
        benimsenir = benimsenir and kosul_a and kosul_b
        _baslik(f"{s} · {n} tohum")
        for k, ad in ((etx, "ETX"), (atl, "atlama"), (tes, "teslim olasiligi")):
            v = pdr[k]
            se = 2.0 * ist.stdev(v) / math.sqrt(n) if n > 1 else math.inf
            print(f"  {ad:<17} PDR ort {ist.mean(v):.4f} ± {se:.4f} · "
                  f"zarfi veren tohum orani {pay[k]:.2f}")
        print(f"  kahin zarfi       PDR ort {ist.mean(zarf):.4f} · zarf − ETX "
              f"{ist.mean(zarf) - ist.mean(pdr[etx]):+.4f}")
        print(f"  teslim − ETX (eslestirilmis) {ort_fark:+.4f} ± {se2:.4f}")
        print(f"  teslim kahinini gecen tohum : {gecilen}/{n}")
        print(f"  (a) zarf payi ≥ ETX : {'EVET' if kosul_a else 'HAYIR'} · "
              f"(b) fark − 2SE > −R : {'EVET' if kosul_b else 'HAYIR'}")
    print()
    print(f"  KARAR: raporlanan ust referans = KAHIN ZARFI · teslim olasiligi "
          f"kahini tek basina referans olarak "
          f"{'BENIMSENIR' if benimsenir else 'BENIMSENMEZ'}")
    return 0


# ==========================================================================
def _teshis_is(gorev):
    """Teşhis işçisi: bir kâhin, `bagimsiz-surekli`, tohum 1000, kısa pencere.

    🔒 Modül düzeyinde — Windows `spawn`. Profil istenirse süre profil altında
    ölçülür ve şişer; kâhinler arası oranlar yine karşılaştırılabilir.
    """
    kahin, profilli = gorev
    kfg = Konfig(kol="ust_referans_teshis", senaryo="bagimsiz-surekli",
                 tohum=1000, **_kisa_pencere())
    kur = kurulum_yap(kfg)
    grafik = (TeslimGrafigi(kur) if kahin == EnOlasiTeslimKahin.ad
              else KanalGrafigi(kur))
    tip = KAHINLER[kahin]

    def fabrika(i):
        return tip(i, grafik)

    kosu = Kosu(kur, fabrika)
    profil = cProfile.Profile() if profilli else None
    t0 = time.perf_counter()
    if profil is not None:
        profil.enable()
    kosu.kostur()
    if profil is not None:
        profil.disable()
    sure = time.perf_counter() - t0
    m = metrik_sozlugu(kur.sayaclar.disa_ver(), kur.paket_defteri,
                       kur.rota_defteri)
    alanlar = ("pdr_pencere", "teslim_paket", "mac_gonderim_istegi",
               "mac_deneme", "gecikme_ort_s_pencere", "gecikme_p95_s_pencere",
               "hedef_yok")
    metin = ""
    if profil is not None:
        akis = io.StringIO()
        pstats.Stats(profil, stream=akis).sort_stats("tottime").print_stats(12)
        metin = akis.getvalue()
    return kahin, sure, {a: m.get(a) for a in alanlar}, metin


def teshis(profilli: bool) -> int:
    """Teslim olasılığı kâhini neden yavaş? — K-114 §4.3.

    Hipotez: `−ln s` iyi bağda ~0 → uzun yol → paket başına daha çok çerçeve.
    Paket başına atlama vekili `mac_gonderim_istegi / teslim_paket` (istek
    sayacı paket-atlama başına bir kez artar); atlama başına deneme
    `mac_deneme / mac_gonderim_istegi`. Atlama kâhini profilsiz koşar ve
    süre referansıdır.
    """
    _baslik(f"T - TESHIS  (bagimsiz-surekli · tohum 1000 · kisa pencere"
            f"{' · cProfile' if profilli else ''})")
    gorevler = [(k, profilli and k != EnKisaYolKahin.ad) for k in KAHINLER]
    with Pool(len(gorevler)) as havuz:
        for kahin, sure, m, metin in havuz.imap_unordered(
                _teshis_is, gorevler, chunksize=1):
            istek = m["mac_gonderim_istegi"]
            teslim = m["teslim_paket"]
            print(f"  {kahin:<24} sure {sure:6.1f} s"
                  f"{' (cProfile)' if metin else ''}"
                  f" · PDR {m['pdr_pencere']:.4f} · teslim {teslim}"
                  f" · istek/teslim {istek / teslim:.2f}"
                  f" · deneme/istek {m['mac_deneme'] / istek:.2f}"
                  f" · gecikme ort {m['gecikme_ort_s_pencere']:.4f}"
                  f" p95 {m['gecikme_p95_s_pencere']:.4f}"
                  f" · hedef_yok {m['hedef_yok']}", flush=True)
            if metin:
                print(metin, flush=True)
    return 0


if __name__ == "__main__":
    # 🔒 Windows `spawn` korumasi — Pool bu blok disinda acilmaz.
    arguman = sys.argv[1:]
    if arguman and arguman[0] == "teshis":
        raise SystemExit(teshis(profilli="--profil" in arguman))
    isci_sayisi = 10
    tohum = 10
    if "--tohum" in arguman:
        tohum = int(arguman[arguman.index("--tohum") + 1])
    if "--kapi" in arguman:
        raise SystemExit(0 if kapi(isci_sayisi, tohum) else 1)
    if len(arguman) >= 2 and arguman[0] == "analiz":
        raise SystemExit(analiz(arguman[1]))
    if len(arguman) >= 2 and arguman[0] == "olc":
        if not kapi(isci_sayisi, tohum):
            print("  🔴 KAPI GECMEDI — olcum baslatilmadi")
            raise SystemExit(1)
        raise SystemExit(olc(arguman[1], tohum, isci_sayisi,
                             devam="--devam" in arguman))
    print(__doc__)
    raise SystemExit(2)
