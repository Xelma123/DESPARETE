"""
DÜĞÜM SAYISI — C1 (`v2/12` §3 C1 · `v2/04` K-124 · `v2/07` §09.4).

Üretici:
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/dugum_sayisi.py

🔒 ÖLÇÜT TARAMADAN ÖNCE İLAN EDİLDİ — öğrenci onayı 15 Eylül 2026 (K-124):

    SERT KISIT 1 — statik kolda tohumların HİÇBİRİNDE ulaşılamaz çift yok.
    SERT KISIT 2 — yere toplama deseninde kaynakların ≥ %90'ı için geçide
                   DÜĞÜM-AYRIK İKİNCİ bir yol var. Karıştırma altında yeniden
                   yönlendirmeye yer kalmasının ölçüsü budur: tek yolu olan
                   bir kaynak için yönlendirme protokolünün yapabileceği bir
                   şey yoktur ve ölçülen şey protokol değil, topolojidir.
    AMAÇ         — iki kısıtı da geçen adaylar arasında KOŞU MALİYETİ EN
                   KÜÇÜK olan N.

🔒 ALAN N İLE ÖLÇEKLENİR, AYRICA TARANMAZ: yoğunluk sabit kalsın diye
`alan(N) = ALAN_CAPASI_M × √(N / CAPA_N)`. 1800 m, N = 40 için ölçülmüş
çapadır (`calisma_noktasi.py`: kopukluğun sıfır kaldığı en büyük alan) ve
aynı yoğunluğu korumak alanın √N ile büyümesi demektir — `bag_kumesi.py` §J
bu kuralı zaten kullanıyor. Alanı N başına yeniden taramak, aynı ölçütü beş
kez koşturmak olurdu (~2 saat) ve yoğunluk çapası zaten ölçülmüş.

⚠️ MALİYET ÖLÇÜLÜR, VARSAYILMAZ. "N² ile büyür" bir kestirimdir; gerçek
maliyet kanal hesabının yoğunluğuna ve trafiğe de bağlıdır. Her aday için
kısa pencereli bir koşu ZAMANLANIR (aynı protokol, aynı tohum, yere toplama).

🔴 BAĞ TANIMI KÂHİN GRAFİĞİDİR (gölgeleme ve sönümleme dâhil, yeniden
denemelerle atlama başarısı ≥ `ATLAMA_ESIGI`). Geometrik disk DEĞİL: K-096 o
diskin veri yolunda hiçbir yeri kapamadığını ölçtü.
"""

from __future__ import annotations

import math
import statistics as ist
import sys
import time
from collections import defaultdict, deque
from multiprocessing import Pool
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from kalibrasyon.kahin import KanalGrafigi  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402

# Aday düğüm sayıları — `12` §3 C1'in aralığı (30–50), beş nokta.
ADAYLAR: tuple[int, ...] = (30, 35, 40, 45, 50)
# Kısıtların ölçüldüğü tohum sayısı; alan seçimindeki ölçütle AYNI (30 tohum).
TOHUMLAR = range(1000, 1030)
# Yoğunluk çapası: N = 40 için ölçülmüş alan (`calisma_noktasi.py`).
ALAN_CAPASI_M: float = 1800.0
CAPA_N: int = 40
# Sert kısıt 2'nin eşiği: kaynakların en az bu payı için ikinci yol.
ALTERNATIF_ORAN: float = 0.90
# 🔒 Ana deney tohumları (`06` §2). Yalnız GRAFİK ölçümü için — hiçbir kol
# koşulmaz, mühür bozulmaz (`ana_deney_bolunmesi`).
ANA_DENEY_TOHUMLARI = range(2000, 2040)
# 🔒 B6 ölçümünün kolları ve anları. Kollar `MOBILITE_KOLLARI`nin tamamı:
# bölünme yalnız hareketle doğabilir, o yüzden statik kol bir KONTROLDÜR
# (orada sıfır çıkmazsa ölçümün kendisi bozuktur).
BOLUNME_KOLLARI: tuple[str, ...] = ("statik", "bagimsiz", "gorev", "formasyon")
# Ölçüm penceresi [50; 320) — dokuz an, `karistirici_gucu.py`nin ızgarasıyla
# aynı mantık: periyodik bir yapıyla ÖRTÜŞMEYEN aralık.
BOLUNME_ANLARI: tuple[float, ...] = tuple(50.0 + k * 31.1 for k in range(9))


def alan_m(n: int) -> float:
    """Yoğunluğu sabit tutan alan — çapadan TÜRETİLİR, taranmaz."""
    return ALAN_CAPASI_M * math.sqrt(n / CAPA_N)


def _konfig(n: int, tohum: int, **ek) -> Konfig:
    a = alan_m(n)
    return Konfig(kol="dugum_sayisi", tohum=tohum, dugum_sayisi=n,
                  alan_en_m=a, alan_boy_m=a, trafik_deseni="yere_toplama",
                  **ek)


# ==========================================================================
def _bilesenler(komsu: list[list[int]]) -> list[list[int]]:
    n = len(komsu)
    gorulen = [False] * n
    cikti: list[list[int]] = []
    for s in range(n):
        if gorulen[s]:
            continue
        yigin, uyeler = [s], []
        gorulen[s] = True
        while yigin:
            u = yigin.pop()
            uyeler.append(u)
            for v in komsu[u]:
                if not gorulen[v]:
                    gorulen[v] = True
                    yigin.append(v)
        cikti.append(uyeler)
    return cikti


def _ulasilamaz_cift(komsu: list[list[int]]) -> int:
    """Birbirine ULAŞAMAYAN düğüm çifti sayısı — sert kısıt 1."""
    n = len(komsu)
    toplam = n * (n - 1) // 2
    icinde = sum(len(b) * (len(b) - 1) // 2 for b in _bilesenler(komsu))
    return toplam - icinde


def _iki_ayrik_yol_var_mi(komsu: list[list[int]], kaynak: int,
                          hedef: int) -> bool:
    """Kaynaktan hedefe DÜĞÜM-AYRIK iki yol var mı?

    🔒 Düğüm bölmeli akış: her ara düğüm `giriş → çıkış` kenarıyla bir
    KAPASİTEYE indirgenir, böylece "düğüm-ayrık" kısıtı kenar akışına döner.
    Açgözlü "bir yol bul, düğümlerini sil, tekrar ara" yöntemi ikinci yolu
    OLDUĞUNDAN AZ bulur; ölçüt bir kapı olduğu için tam cevap gerekir.
    """
    n = len(komsu)
    kap: dict[tuple[int, int], int] = defaultdict(int)
    bag: dict[int, list[int]] = defaultdict(list)

    def ekle(u: int, v: int, c: int) -> None:
        if kap[(u, v)] == 0 and kap[(v, u)] == 0:
            bag[u].append(v)
            bag[v].append(u)
        kap[(u, v)] += c

    for i in range(n):
        ekle(2 * i, 2 * i + 1, 2 if i in (kaynak, hedef) else 1)
        for j in komsu[i]:
            ekle(2 * i + 1, 2 * j, 2)

    bas, son = 2 * kaynak + 1, 2 * hedef
    for _ in range(2):
        onceki: dict[int, int | None] = {bas: None}
        kuyruk = deque([bas])
        while kuyruk and son not in onceki:
            u = kuyruk.popleft()
            for v in bag[u]:
                if kap[(u, v)] > 0 and v not in onceki:
                    onceki[v] = u
                    kuyruk.append(v)
        if son not in onceki:
            return False
        v = son
        while onceki[v] is not None:
            u = onceki[v]
            kap[(u, v)] -= 1
            kap[(v, u)] += 1
            v = u
    return True


def _is(gorev):
    """Bir (N, tohum) — iki kısıtın ölçümü. Havuz işçisi."""
    n, tohum = gorev
    try:
        kfg = _konfig(n, tohum)
        kur = kurulum_yap(kfg)
        g = KanalGrafigi(kur)
        g.ozet(0.0)                       # grafiği bu an için kurar
        komsu = [list(k) for k in g._komsu]
        gecit = kfg.gecit
        # Kaynağın geçide ulaşıp ulaşmadığı bileşenden okunur.
        bilesen = {u: i for i, b in enumerate(_bilesenler(komsu)) for u in b}
        ulasan = [s for s in range(n)
                  if s != gecit and bilesen[s] == bilesen[gecit]]
        ikili = sum(1 for s in ulasan
                    if _iki_ayrik_yol_var_mi(komsu, s, gecit))
        return {
            "n": n, "tohum": tohum,
            "ulasilamaz": _ulasilamaz_cift(komsu),
            "gecide_ulasan": len(ulasan),
            "iki_yollu": ikili,
            "derece": sum(len(k) for k in komsu) / n,
        }, None
    except Exception as hata:                       # noqa: BLE001
        return None, f"{type(hata).__name__}: {hata}"


def _bolunme_isi(gorev):
    """Bir (mobilite kolu, tohum) — pencere boyunca bölünme. Havuz işçisi.

    🔒 BAĞ TANIMI KÂHİN GRAFİĞİDİR ve bu bir düzeltmedir (16 Eylül 2026).
    İlk denemede bölünme `sim2/olcum/kopma.py`nin YAVAŞ SINR tanımıyla, koşu
    içinde sayılmıştı. Ölçüldü ve geri alındı: aynı tohumda, aynı anda yavaş
    SINR grafiği 55 bağ / derece 2,75 ve TEK PARÇA DEĞİL, kâhin grafiği ise
    162 bağ / derece 8,10 ve TEK PARÇA. Yani yavaş SINR grafiği zaten hep
    bölünmüştür ve o tanımla "bölünme" her satıra %100 yazardı — ölçtüğü şey
    ağın bölünmesi değil, tek denemelik bir eşiğin seyrekliği olurdu.

    🔒 Kâhin grafiği çalışma noktasının SEÇİLDİĞİ tanımdır (C1 ve
    `calisma_noktasi.py`), yani bu sayı o kararla doğrudan kıyaslanabilir.
    """
    kol, tohum = gorev
    try:
        kfg = _konfig(CAPA_N, tohum, senaryo=f"{kol}-yok")
        kur = kurulum_yap(kfg)
        g = KanalGrafigi(kur)
        bolunmus = 0
        en_cok = 0
        dereceler = []
        for t in BOLUNME_ANLARI:
            g.ozet(t)                      # grafiği bu an için kurar
            komsu = [list(k) for k in g._komsu]
            u = _ulasilamaz_cift(komsu)
            dereceler.append(sum(len(k) for k in komsu) / CAPA_N)
            if u > 0:
                bolunmus += 1
                en_cok = max(en_cok, u)
        return {"bolunmus_an": bolunmus, "an": len(BOLUNME_ANLARI),
                "en_cok_ulasilamaz": en_cok,
                "derece": ist.mean(dereceler)}, None
    except Exception as hata:                       # noqa: BLE001
        return None, f"{type(hata).__name__}: {hata}"


def _maliyet_s(n: int) -> float:
    """Kısa pencereli bir koşunun duvar saati — maliyet ÖLÇÜLÜR."""
    from protokoller.kosum_kosumu import DogrudanKomsu
    kfg = _konfig(n, 1000, senaryo="statik-surekli",
                  karistirici_baslangic_s=5.0, isinma_s=10.0,
                  olcum_bitis_s=40.0, kosu_bitis_s=50.0)
    kur = kurulum_yap(kfg)
    t0 = time.perf_counter()
    Kosu(kur, lambda i: DogrudanKomsu()).kostur()
    return time.perf_counter() - t0


def ana_deney_bolunmesi(isci: int = 6) -> int:
    """ANA DENEY TOHUMLARI (2000–2039) — kanal grafiği bölünmüş mü? (denetim B6)

    🔴 NEDEN. C1 (K-125) çalışma noktasının **uçurumun kenarında** olduğunu
    ölçtü: 1800 m / N = 40'ta kopukluk olasılığı 120 tohumla **%0,8**.
    40 tohumluk ana deneyde en az bir kopuk tohum görme olasılığı
    `1 − 0,992^40 ≈ %27`. Böyle bir tohumda teslim oranı **protokolden
    bağımsız** bir sebeple çöker — ve sonuç satırının kapsam bölümünde bunu
    söyleyen hiçbir alan yoktu.

    🔒 MÜHRÜ BOZMAZ. `06` §0.2'nin kuralı *"ana deney tohumları mühürden önce
    HİÇBİR KOLDA KOŞULMAZ"*tır. Burada hiçbir kol koşulmuyor: yalnız kanal
    grafiği kuruluyor (`KanalGrafigi`), hiçbir protokol çalışmıyor, hiçbir
    metrik üretilmiyor, hiçbir paket doğmuyor. Grafik protokolden bağımsızdır
    ve sonuç hakkında bilgi VERMEZ — hangi protokolün kazanacağına dair tek
    bir bit bile sızmaz. ⚠️ Bu yüzden bu bölüm `_maliyet_s`i ÇAĞIRMAZ: o
    gerçek bir koşu başlatır ve kuralı çiğnerdi.

    🔒 Tanım C1'inkinin AYNISI — aynı işçi (`_is`), aynı kâhin grafiği, aynı
    "kopuk tohum = ulaşılamaz çift > 0" ölçütü. İkinci bir tanım yazmak, iki
    tanımın bir gün ayrışması demek olurdu.
    """
    tohumlar = list(ANA_DENEY_TOHUMLARI)
    print("ANA DENEY TOHUMLARININ BOLUNMESI — B6 (`v2/12` §3)")
    print(f"  N = {CAPA_N} · alan = {ALAN_CAPASI_M:.0f} m · "
          f"tohumlar {tohumlar[0]}–{tohumlar[-1]} ({len(tohumlar)} tohum)")
    print(f"  kollar: {BOLUNME_KOLLARI}")
    print(f"  pencere boyunca {len(BOLUNME_ANLARI)} an: "
          f"{BOLUNME_ANLARI[0]:.0f}–{BOLUNME_ANLARI[-1]:.0f} s")
    print("  bag: KAHIN GRAFIGI · bolunmus an = ulasilamaz cift > 0")
    print("  🔒 HICBIR KOL KOSULMUYOR — yalniz grafik kuruluyor (muhur bozulmaz)")
    print()
    gorevler = [(kol, t) for kol in BOLUNME_KOLLARI for t in tohumlar]
    with Pool(isci) as havuz:
        ham = havuz.map(_bolunme_isi, gorevler, chunksize=1)
    ozet: dict[str, list] = {kol: [] for kol in BOLUNME_KOLLARI}
    hatali = []
    for (kol, tohum), (sonuc, hata) in zip(gorevler, ham):
        if hata is not None:
            hatali.append((kol, tohum, hata))
            continue
        ozet[kol].append((tohum, sonuc))
    print(f"  {'kol':<20}{'bolunmus tohum':>16}{'bolunmus an payi':>18}"
          f"{'derece ort':>12}")
    toplam_kopuk = 0
    for kol in BOLUNME_KOLLARI:
        kayit = ozet[kol]
        if not kayit:
            continue
        kopuk = [(t, s) for t, s in kayit if s["bolunmus_an"] > 0]
        toplam_kopuk += len(kopuk)
        pay = ist.mean(s["bolunmus_an"] / s["an"] for _t, s in kayit)
        der = ist.mean(s["derece"] for _t, s in kayit)
        isaret = " 🔴" if kopuk else ""
        print(f"  {kol:<20}{len(kopuk):>10}/{len(kayit):<5}{pay:>17.2%}"
              f"{der:>12.2f}{isaret}")
        for t, s in kopuk:
            print(f"      🔴 tohum {t}: {s['bolunmus_an']}/{s['an']} anda "
                  f"bolunmus · en cok {s['en_cok_ulasilamaz']} ulasilamaz cift")
    print()
    print(f"  bolunmus (kol, tohum) cifti : {toplam_kopuk}/{len(gorevler)}")
    if hatali:
        print(f"  🔴 HATA: {hatali[:3]}")
        return 1
    print()
    print("  🔒 Bu sayi bir KAPI DEGIL, bir BEYANDIR: kopuk bir tohum")
    print("     'kotu tohum' degildir ve ATILMAZ — atmak secilim yanliligi")
    print("     olurdu. Bolunmus bir (kol, tohum) ciftinde teslim kaybinin")
    print("     bir kismi YONLENDIRMEDEN BAGIMSIZDIR ve o tohum raporda")
    print("     ISIMLE anilir; betimleyici tablolar ve evre metrikleri")
    print("     orada ayrica okunur.")
    print("  ⚠️ KARISTIRICI BU TANIMIN DISINDA: olculen sey TOPOLOJININ")
    print("     bolunmesidir. Karistirmanin actigi gecici kopukluk evre")
    print("     metrikleriyle olculur.")
    return 0


def main(isci: int = 6) -> int:
    tohumlar = list(TOHUMLAR)
    print("DUGUM SAYISI — C1 (olcut taramadan ONCE ilan edildi, K-124)")
    print(f"  adaylar {ADAYLAR} · {len(tohumlar)} tohum · alan = "
          f"{ALAN_CAPASI_M:.0f} m × sqrt(N/{CAPA_N}) · bag: kahin grafigi")
    print(f"  KISIT 1: ulasilamaz cift = 0 (her tohumda)")
    print(f"  KISIT 2: gecide dugum-ayrik ikinci yolu olan kaynak orani >= "
          f"{ALTERNATIF_ORAN:.0%}")
    print("  AMAC   : iki kisiti gecenler arasinda maliyeti EN KUCUK N")
    print()

    gorevler = [(n, t) for n in ADAYLAR for t in tohumlar]
    with Pool(isci) as havuz:
        ham = havuz.map(_is, gorevler, chunksize=1)
    hata = next((h for _s, h in ham if h is not None), None)
    if hata:
        print(f"  🔴 gorev PATLADI: {hata[:200]}")
        return 1

    print(f"  {'N':>4} {'alan m':>8} {'derece':>8} {'kopuk tohum':>12} "
          f"{'iki yollu':>10} {'maliyet s':>10} {'kisit1':>7} {'kisit2':>7}")
    gecenler: list[tuple[float, int]] = []
    ozet: dict[int, dict] = {}
    for i, n in enumerate(ADAYLAR):
        dilim = [s for s, _h in ham[i * len(tohumlar):(i + 1) * len(tohumlar)]]
        kopuk = sum(1 for s in dilim if s["ulasilamaz"] > 0)
        ulasan = sum(s["gecide_ulasan"] for s in dilim)
        ikili = sum(s["iki_yollu"] for s in dilim)
        oran = ikili / ulasan if ulasan else 0.0
        maliyet = _maliyet_s(n)
        k1, k2 = kopuk == 0, oran >= ALTERNATIF_ORAN
        if k1 and k2:
            gecenler.append((maliyet, n))
        ozet[n] = {"derece": ist.mean(s["derece"] for s in dilim),
                   "kopuk": kopuk, "oran": oran, "maliyet": maliyet}
        print(f"  {n:>4} {alan_m(n):>8.0f} {ozet[n]['derece']:>8.2f} "
              f"{kopuk:>12} {oran:>9.1%} {maliyet:>10.1f} "
              f"{'EVET' if k1 else '🔴 HAYIR':>7} "
              f"{'EVET' if k2 else '🔴 HAYIR':>7}")

    print()
    if not gecenler:
        print("  🔴 HICBIR ADAY IKI KISITI BIRDEN GECMEDI — bu bir BULGUDUR:")
        print("     bu calisma noktasinda yere toplama deseni yeniden")
        print("     yonlendirmeye yer birakmiyor. Alan ya da guc yeniden")
        print("     secilmeden N secilemez.")
        return 1
    maliyet, secilen = min(gecenler)
    print(f"  🟢 SECILEN: N = {secilen} · alan {alan_m(secilen):.0f} m · "
          f"maliyet {maliyet:.1f} s · derece {ozet[secilen]['derece']:.2f} · "
          f"iki yollu {ozet[secilen]['oran']:.1%}")
    print("     Iki sert kisiti da gecen EN UCUZ aday. Sayi ELLE KONMADI.")
    return 0


if __name__ == "__main__":
    # 🔒 Windows `spawn` korumasi — Pool bu blok disinda acilmaz.
    if "--bolunme" in sys.argv:
        raise SystemExit(ana_deney_bolunmesi())
    # 🔒 Windows `spawn` korumasi — Pool bu blok disinda acilmaz.
    raise SystemExit(main())
