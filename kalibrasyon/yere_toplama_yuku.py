"""
YERE TOPLAMA YÜKÜ — C3 (`v2/12` §3 C3 · `v2/04` K-124 · `v2/07` §06.2).

Üretici:
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/yere_toplama_yuku.py

🔒 ÖLÇÜT TARAMADAN ÖNCE İLAN EDİLDİ — öğrenci onayı 15 Eylül 2026 (K-124):

    Karıştırıcısız kolda, KÂHİN yönlendirmeyle uçtan uca teslim ≥ 0,95
    tutan EN BÜYÜK telemetri hızı. Komut hızı bugünkü oranıyla birlikte
    gider (komut = telemetri × KOMUT_ORANI).

🔒 NEDEN BU ÖLÇÜT: karıştırıcı gücü ölçütünün KARDEŞİ. Yük tek başına ağı
çökertirse karıştırıcının etkisi ölçülemez hâle gelir — taban zaten kusurlu
olur ve protokol farkı sıkışır. Kâhin kullanılır çünkü ölçülen şey YÜKÜN
kapasitesi olmalı, aptal bir koşum aletinin yönlendirme kusuru değil.

🔴 ÖLÇÜT HANGİ KOLDA UYGULANIR — ve neden hareketli kolda DEĞİL
==============================================================
İlk tasarım taramayı `bagimsiz-yok`ta koşuracaktı: *yük hem çarpışmayı hem
rota kopmasını birlikte görür* diye. Koşmadan önce ölçülmüş bir sayı bunu
çürüttü: o kolda kâhinin YÜKSÜZ PDR tavanı zaten **0,917** (`pdr_tavani.py`,
10 tohum). Yani `≥ 0,95` ölçütü orada EN DÜŞÜK yükte bile sağlanamaz ve
tarama *hiçbir aday geçmedi* derdi — ölçülen şey yük değil, mobilite olurdu.

🔒 Bu yüzden ölçüt, kâhin tavanı ≈ 1,000 olan `statik-yok` kolunda uygulanır:
orada PDR'yi 1'den aşağı çeken TEK şey yüktür. Ölçüt metni (K-124)
değişmedi; yalnız onu ölçen kol adlandırıldı.

⚠️ Seçilen hız `bagimsiz-yok`ta da koşulur ve raporlanır — ama bir KAPI
olarak değil, YAN GÖZLEM olarak: o koldaki sayı yükün değil, mobilitenin
tavanını taşır. Maliyeti yüzünden kısa pencerede koşulur ve bu beyan edilir.

⚠️ Bugünkü varsayılan (telemetri 1,0 · komut 0,25 pkt/s) kaynaksız bir
varsayımdı (`02` §S4). Bu tarama onu ya doğrular ya değiştirir.
"""

from __future__ import annotations

import statistics as ist
import sys
from multiprocessing import Pool
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from kalibrasyon.kahin import EnGuvenilirKahin, KanalGrafigi  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.kosum.sonuc import sonuc_satiri  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402
from kalibrasyon import dunya_secimi as DS  # noqa: E402  (K-183)

# Telemetri hızı TARAMASININ ekseni (pkt/s). Bugünkü değer (1,0) içeride.
ADAYLAR_HZ: tuple[float, ...] = (0.5, 1.0, 1.5, 2.0, 3.0)
# Komut hızı telemetriye ORANLA gider; bugünkü oran 0,25 / 1,0.
KOMUT_ORANI: float = 0.25
# İlan edilmiş eşik (K-124).
TESLIM_ESIGI: float = 0.95
TOHUMLAR = range(1000, 1003)
# Ölçütün uygulandığı kol: kâhin tavanı ≈ 1,000 (yukarıdaki nota bak).
OLCUT_KOLU = "statik-yok"
# Yan gözlem kolu: tavanı 0,917, kapı DEĞİL.
YAN_GOZLEM_KOLU = "bagimsiz-yok"
# Yan gözlem kısa pencerede koşar — tam uzunluk kâhin koşusu orada
# 10 dakikanın üstünde sürüyor (ölçüldü) ve bir kapı taşımıyor.
YAN_GOZLEM_PENCERESI = {"isinma_s": 10.0, "olcum_bitis_s": 40.0,
                        "kosu_bitis_s": 50.0}

# 🔒 MARJ ÖLÇÜMÜ — seçilen hızı BÜYÜTEMEZ, yalnız uçurumun yerini bulur.
# `ADAYLAR_HZ`de 2,0 ile 3,0 arasında hiçbir nokta yoktu; "2,0 geçti, 3,0
# çöktü" çalışma noktasının uçuruma uzaklığını söylemiyordu (C1'in dersi).
MARJ_HIZLARI: tuple[float, ...] = (2.25, 2.5)
# 🔒 EKSENİN ÖTEKİ YARISI — `trafik_deseni` bir TEDAVİ ekseni ve C3 ölçütü
# yalnız `yere_toplama` seviyesinde koşmuştu. Bugünkü yük (10 × 4,0 = 40
# pkt/s) ve iki katı; ikincisi "iki deseni 80'de eşitlemek mümkün mü"
# sorusunun cevabıdır.
ESLER_HIZLARI: tuple[float, ...] = (4.0, 8.0)


def _is(gorev):
    """Bir (senaryo, hız, tohum, pencere) — kâhin yönlendirmeli koşu.

    `pencere` boşsa tam uzunluk; yan gözlemde kısa pencere verilir ve bu
    çıktıda ayrıca yazılır.
    """
    senaryo, hiz, tohum, pencere = gorev
    try:
        kfg = DS.konfig(kol="yere_toplama_yuku", senaryo=senaryo, tohum=tohum,
                     trafik_deseni="yere_toplama",
                     telemetri_paket_hizi_hz=hiz,
                     komut_paket_hizi_hz=hiz * KOMUT_ORANI, **pencere)
        kur = kurulum_yap(kfg)
        grafik = KanalGrafigi(kur)
        kosu = Kosu(kur, lambda i: EnGuvenilirKahin(i, grafik))
        kosu.kostur()
        satir = sonuc_satiri(kur, kosu.dugumler, "en_guvenilir_kahin")
        return {"senaryo": senaryo, "hiz": hiz, "tohum": tohum,
                "pdr": satir["metrikler"]["pdr"],
                "sunulan": kfg.sunulan_paket_hizi_hz,
                "gecerli": satir["korunum"]["gecerli"]}, None
    except Exception as hata:                       # noqa: BLE001
        return None, f"{type(hata).__name__}: {hata}"


def _is_esler(gorev):
    """`esler_arasi` deseninde bir (hız, tohum) — kâhin yönlendirmeli koşu."""
    hiz, tohum = gorev
    try:
        kfg = DS.konfig(kol="esler_arasi_yuku", senaryo=OLCUT_KOLU, tohum=tohum,
                     trafik_deseni="esler_arasi", akis_paket_hizi_hz=hiz)
        kur = kurulum_yap(kfg)
        grafik = KanalGrafigi(kur)
        kosu = Kosu(kur, lambda i: EnGuvenilirKahin(i, grafik))
        kosu.kostur()
        satir = sonuc_satiri(kur, kosu.dugumler, "en_guvenilir_kahin")
        return {"hiz": hiz, "tohum": tohum,
                "pdr": satir["metrikler"]["pdr"],
                "sunulan": kfg.sunulan_paket_hizi_hz,
                "gecerli": satir["korunum"]["gecerli"]}, None
    except Exception as hata:                       # noqa: BLE001
        return None, f"{type(hata).__name__}: {hata}"


def _tablo(ham, hizler, tohumlar, komut: bool) -> None:
    """Hız başına PDR ortalaması, 2·SE ve tohum tek tek."""
    for i, hiz in enumerate(hizler):
        dilim = [s for s, _h in ham[i * len(tohumlar):(i + 1) * len(tohumlar)]]
        pdrler = [s["pdr"] for s in dilim]
        ort = ist.mean(pdrler)
        se2 = (2.0 * ist.stdev(pdrler) / len(pdrler) ** 0.5
               if len(pdrler) > 1 else 0.0)
        tek = " ".join(f"{q:.4f}" for q in pdrler)
        sol = (f"{hiz:>10.2f} {hiz * KOMUT_ORANI:>7.2f}" if komut
               else f"{hiz:>10.2f} {'—':>7}")
        print(f"  {sol} {dilim[0]['sunulan']:>9.1f} {ort:>7.4f} {se2:>7.4f} "
              f"{'GECER' if ort >= TESLIM_ESIGI else 'kalir':>7}  {tek}")


def marj(isci: int = 6) -> int:
    """🔒 UÇURUM NEREDE — KAPI DEĞİL, MARJ ölçümü.

    Bu bölüm seçilen hızı BÜYÜTEMEZ: ölçüt (K-124) ilan edilmiş ızgarada
    koştu. Burada ölçülen tek şey, seçilen noktanın çöküşe uzaklığıdır.
    Sebep: C1'de çalışma noktasının uçurum kenarında olduğu ancak SONRADAN
    ölçülünce görüldü (K-125); aynı hatayı burada tekrarlamamak için.
    """
    tohumlar = list(TOHUMLAR)
    print("C3 MARJ — ucurum 2,0 ile 3,0 arasinda NEREDE? (KAPI DEGIL)")
    print(f"  kol {OLCUT_KOLU} · tohum {tohumlar} · esik {TESLIM_ESIGI:.2f}")
    print()
    gorevler = [(OLCUT_KOLU, h, t, {}) for h in MARJ_HIZLARI for t in tohumlar]
    with Pool(isci) as havuz:
        ham = havuz.map(_is, gorevler, chunksize=1)
    hata = next((h for _s, h in ham if h is not None), None)
    if hata:
        print(f"  🔴 gorev PATLADI: {hata[:200]}")
        return 1
    print(f"  {'telemetri':>10} {'komut':>7} {'sunulan':>9} {'PDR':>7} "
          f"{'2SE':>7} {'olcut':>7}  tohum tek tek")
    _tablo(ham, MARJ_HIZLARI, tohumlar, komut=True)
    return 0


def esler(isci: int = 6) -> int:
    """🔒 EKSENİN ÖTEKİ YARISI — `esler_arasi` AYNI ölçütle sınanır.

    `akis_sayisi` ve `akis_paket_hizi_hz` kökende SINANMAMIS ve gerekçeleri
    ESKİ çalışma noktasından (1000 m, α = 3) kalma. Ölçüt orada hiç
    uygulanmamıştı. ⚠️ Bu ölçüm `yere_toplama` seçimini DEĞİŞTİREMEZ.
    """
    tohumlar = list(TOHUMLAR)
    print("C3 SIMETRIK YARI — `esler_arasi`, AYNI olcut (K-124)")
    print(f"  kol {OLCUT_KOLU} · tohum {tohumlar} · esik {TESLIM_ESIGI:.2f}")
    print()
    gorevler = [(h, t) for h in ESLER_HIZLARI for t in tohumlar]
    with Pool(isci) as havuz:
        ham = havuz.map(_is_esler, gorevler, chunksize=1)
    hata = next((h for _s, h in ham if h is not None), None)
    if hata:
        print(f"  🔴 gorev PATLADI: {hata[:200]}")
        return 1
    print(f"  {'akis hizi':>10} {'komut':>7} {'sunulan':>9} {'PDR':>7} "
          f"{'2SE':>7} {'olcut':>7}  tohum tek tek")
    _tablo(ham, ESLER_HIZLARI, tohumlar, komut=False)
    return 0


def duman() -> int:
    """🔒 UCUZ KESİT — duman koşusu için. SAYIYI ÜRETMEZ.

    Tek hız × tek tohum, KISA pencerede. Sorduğu tek soru: *bu üretici
    hâlâ koşuyor mu*. Ölçütün seçtiği hızı bu bölüm üretemez ve üretmeye
    kalkışması da yanlış olurdu — 15 dakikalık bir kesit, kesit değildir.
    """
    tohum = list(TOHUMLAR)[0]
    print("YERE TOPLAMA YUKU — DUMAN KESITI (sayiyi URETMEZ)")
    print(f"  tek hiz {1.0:.2f} · tek tohum {tohum} · KISA pencere")
    s, hata = _is((OLCUT_KOLU, 1.0, tohum, YAN_GOZLEM_PENCERESI))
    if hata:
        print(f"  🔴 PATLADI: {hata[:200]}")
        return 1
    print(f"  PDR {s['pdr']:.4f} · sunulan {s['sunulan']:.1f} pkt/s · "
          f"gecerli {s['gecerli']}")
    print("  🟢 uretici kosuyor.")
    return 0 if s["gecerli"] else 1


def main(isci: int = 6) -> int:
    tohumlar = list(TOHUMLAR)
    print("YERE TOPLAMA YUKU — C3 (olcut taramadan ONCE ilan edildi, K-124)")
    print(f"  OLCUT: karistiricisiz kolda kahin PDR >= {TESLIM_ESIGI:.2f} "
          f"tutan EN BUYUK telemetri hizi")
    print(f"  olcut kolu {OLCUT_KOLU} (kahin tavani ~1,000) · "
          f"{len(tohumlar)} tohum · komut = telemetri x {KOMUT_ORANI}")
    print(f"  yan gozlem {YAN_GOZLEM_KOLU} (tavan 0,917) — KAPI DEGIL")
    print()

    gorevler = [(OLCUT_KOLU, h, t, {}) for h in ADAYLAR_HZ
                for t in tohumlar]
    with Pool(isci) as havuz:
        ham = havuz.map(_is, gorevler, chunksize=1)
    hata = next((h for _s, h in ham if h is not None), None)
    if hata:
        print(f"  🔴 gorev PATLADI: {hata[:200]}")
        return 1

    print(f"  {'telemetri':>10} {'komut':>7} {'sunulan pkt/s':>14} "
          f"{'PDR':>7} {'2SE':>7} {'gecerli':>8} {'olcut':>7}")
    gecen: list[float] = []
    for i, hiz in enumerate(ADAYLAR_HZ):
        dilim = [s for s, _h in ham[i * len(tohumlar):(i + 1) * len(tohumlar)]]
        pdrler = [s["pdr"] for s in dilim]
        ort = ist.mean(pdrler)
        se2 = (2.0 * ist.stdev(pdrler) / len(pdrler) ** 0.5
               if len(pdrler) > 1 else 0.0)
        tamam = all(s["gecerli"] for s in dilim)
        if ort >= TESLIM_ESIGI and tamam:
            gecen.append(hiz)
        print(f"  {hiz:>10.2f} {hiz * KOMUT_ORANI:>7.2f} "
              f"{dilim[0]['sunulan']:>14.1f} {ort:>7.4f} {se2:>7.4f} "
              f"{'EVET' if tamam else '🔴 HAYIR':>8} "
              f"{'GECER' if ort >= TESLIM_ESIGI else 'kalir':>7}")

    print()
    if not gecen:
        print("  🔴 HICBIR ADAY OLCUTU GECMEDI — bu bir BULGUDUR: bu calisma")
        print("     noktasinda yere toplama deseni kahinle bile 0,95'i")
        print("     tutturamiyor. Yuk degil, calisma noktasi sorgulanmali.")
        return 1
    secilen = max(gecen)
    print(f"  🟢 SECILEN: telemetri {secilen:.2f} pkt/s · komut "
          f"{secilen * KOMUT_ORANI:.2f} pkt/s — olcutu gecen EN BUYUK hiz.")

    yan = [(YAN_GOZLEM_KOLU, secilen, t, YAN_GOZLEM_PENCERESI)
           for t in tohumlar]
    with Pool(min(isci, len(yan))) as havuz:
        ham2 = havuz.map(_is, yan, chunksize=1)
    hata = next((h for _s, h in ham2 if h is not None), None)
    if hata:
        print(f"  🔴 yan gozlem PATLADI: {hata[:200]}")
        return 1
    ort2 = ist.mean(s["pdr"] for s, _h in ham2)
    print(f"  YAN GOZLEM ({YAN_GOZLEM_KOLU}, kisa pencere): PDR {ort2:.4f}")
    print("     ⚠️ KAPI DEGIL: o koldaki tavan (0,917) yukun degil,")
    print("        mobilitenin sinuridir.")
    return 0


if __name__ == "__main__":
    DS.secimi_oku()                         # Faz 4 (K-183): --dunya
    print(f"  DUNYA: {DS.secili()}")
    # 🔒 Windows `spawn` korumasi — Pool bu blok disinda acilmaz.
    BOLUMLER = {"tarama": main, "marj": marj, "esler": esler,
                "duman": duman}
    _secim = sys.argv[1:] or ["tarama"]
    raise SystemExit(max(BOLUMLER[_a]() for _a in _secim))
