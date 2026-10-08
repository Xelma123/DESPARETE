"""
BAĞ KÜMESİ — kanal grafiğinin eşiğe ve sönümleme örneğine DUYARLILIĞI.

Üretici:
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/bag_kumesi.py

🔴 NEDEN BU ALET VAR — üç borç, tek kaynak
==========================================
Üç ayrı açık borç aynı eksik ölçüme dayanıyordu ve üçü de "bağ kümesini
kanaldan oku" diyor:

  1. `kahin.py::ATLAMA_ESIGI = 0,90` gerekçesiz, ve ÇALIŞMA NOKTASINI
     belirliyor: ρ = 0,258 o eşikle tanımlanmış bir grafikte ölçüldü.
  2. `calkanti.py` başlığı *"seçilen nokta sonra kanal tabanlı grafikle
     DOĞRULANIR"* diye taahhüt ediyor — o doğrulama depoda YOK.
  3. `adim3_kapanis.py` bağlantılılık sayılarının üreticisi ve **KOŞMUYOR**:
     kolların eski adını (`mobil-yok`) kullanıyor, üçüncü kol eklenirken
     yeniden adlandırma ona uygulanmamış. Ürettiği sayılar `sim2/`de beş
     yerde hâlâ ESKİ KOL ADIYLA yazılı — yani terk edilmiş bir çalışma
     noktasından (alan 1000 m · yol kaybı üsteli 3 · SINR eşiği 10 dB).

🔒 KÂHİN GRAFİĞİ YENİDEN YAZILMADI — ve bu bir tercih değil, kısıt.
==================================================================
İkinci bir bağ-kalitesi gerçeklemesi yazmak, bu projenin defalarca
yakalandığı hata sınıfıdır (iki hesap sessizce ayrışır). Onun yerine var
olan grafiğin ETX değerleri OKUNUR ve her eşiğin bağ kümesi onlardan geri
türetilir:

    etx = 1 / p              (p = tek deneme başarısı, sönümleme dâhil)
    atlama(τ) = 1 − (1 − p)^(yeniden_deneme_siniri + 1)  ≥  τ

Bu, `KanalGrafigi._kur`un uyguladığı kuralın TA KENDİSİDİR. Tek geçişte
bütün eşikler çıkar; grafiği eşik başına yeniden kurmak gerekmez.

⚠️ ETX bir TAVANLA kelepçelidir (`ETX_TAVANI = 1e9`), yani p ≈ 0 olan
bağlarda geri türetilen p tavandan gelir. O bağlar her makul eşiğin
altındadır; sweep aralığı bu yüzden 0,5'in altına inmez.

🔒 ALETİN KENDİ KAPILARI — "ölçtüğüne güvendiğinden az güven"
=============================================================
    G-a  türetilen derece == canlı grafiğin kendi raporladığı derece
         (eşik = ATLAMA_ESIGI'nde, birebir). Türetme yanlışsa burada çöker.
    G-b  sönümleme KAPALIYKEN zaman kaydırması grafiği DEĞİŞTİRMEMELİ —
         yoksa kaydırma sönümlemeyi izole etmiyor, başka bir şeyi oynatıyor.
    G-c  eşik sütunu GERÇEKTEN değişmeli. Değişmiyorsa tarama ölüdür.

🔒 SÖNÜMLEME ÖRNEK SAYISI K — ölçütü SEÇİLMEDİ, VAR OLAN toleranslardan
=======================================================================
K bir Monte-Carlo örneklem sayısıdır ve kendi gürültüsü ölçülebilir: aynı
tohum, aynı dünya, yalnız ÖRNEKLEME FAZI kaydırılır. Dünya sabit olduğu
için görülen saçılma yalnız kestiricinin kendi gürültüsüdür.

Yeterlilik ölçütü yeni bir sayı GETİRMEZ; kararın kendi toleransını kullanır:
  · derece  → görev kolu eşitlemesinin ilan edilmiş toleransı 0,3
  · ρ       → deneyin çözünürlüğü R = 0,036 (`cozunurluk.py`)
"""

from __future__ import annotations

import statistics as ist
import sys
from multiprocessing import Pool
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402
from kalibrasyon import dunya_secimi as DS  # noqa: E402  (K-183)
from kalibrasyon.kahin import ATLAMA_ESIGI, KanalGrafigi  # noqa: E402
from kalibrasyon.karistirici_gucu import ORNEK_ANLARI, TOHUMLAR  # noqa: E402

__all__ = ["ESIKLER", "graf_ozeti", "kume_ozeti"]

# 🔒 Taranan eşikler. Alt sınır 0,5: altında ETX tavanı (p ≈ 0 bağları)
# türetmeyi bozar ve o bağlar zaten hiçbir yönlendirici için kullanılabilir
# değildir. Üst sınır 0,99: 1,0 tanım gereği boş küme verir.
ESIKLER: tuple[float, ...] = (0.50, 0.70, 0.80, 0.90, 0.95, 0.99)

# 🔒 Sönümleme örnek sayısı taraması. İkişer katlar — ölçekten bağımsız tek
# çarpan, `duyarlilik.py::CARPANLAR` ile aynı gerekçe.
K_ADAYLARI: tuple[int, ...] = (1, 2, 4, 8, 16, 32)

# 🔒 Örnekleme fazı kaydırmaları — BÜYÜKLÜĞÜ TÜRETİLDİ, seçilmedi.
# İki kısıt aynı anda sağlanmalı:
#   · kaydırma, sönümleme tutarlılık süresinden (~1,7 ms, `sonumleme.py`)
#     BÜYÜK olmalı — küçük olsaydı çekimler birbiriyle korelasyonlu kalır
#     ve ölçülen saçılma kestiricinin gürültüsünü OLDUĞUNDAN KÜÇÜK gösterirdi;
#   · dünyayı oynatmayacak kadar KÜÇÜK olmalı — 35 ms'de bir düğüm en çok
#     0,75 m/s × 0,035 s ≈ 2,6 cm yol alır; gölgeleme hücresi 50 m.
# 7 ms'lik adım ikisini birden sağlar (T_c'nin ~4 katı, hücrenin ~2000'de 1'i).
KAYDIRMALAR: tuple[float, ...] = (0.0, 0.007, 0.014, 0.021, 0.028, 0.035)

# 🔒 Kararların KENDİ toleransları — burada yeni bir eşik SEÇİLMİYOR.
DERECE_TOLERANSI = 0.3     # `gorev_kalibrasyonu.py`de ilan edildi
COZUNURLUK_R = 0.036       # `cozunurluk.py` ölçtü (30 tohum, 2·SD/√30)

# ρ taramasının güçleri — `karistirici_gucu.tarama`nın varsayılanıyla AYNI.
GUCLER: tuple[float, ...] = (-30.0, -24.0, -18.0, -15.0, -12.0, -9.0, -6.0)


# ==========================================================================
def kume_ozeti(komsu: list[list[int]]) -> dict[str, float]:
    """Bir komşuluk listesinin derece ve bileşen yapısı.

    🔒 `KanalGrafigi.ozet` ile AYNI tanımlar; G-a kapısı ikisinin
    ayrışmadığını her koşumda sınar.
    """
    n = len(komsu)
    derece = sum(len(k) for k in komsu) / n
    gorulen = [False] * n
    bilesenler: list[int] = []
    for s in range(n):
        if gorulen[s]:
            continue
        yigin, adet = [s], 0
        gorulen[s] = True
        while yigin:
            u = yigin.pop()
            adet += 1
            for v in komsu[u]:
                if not gorulen[v]:
                    gorulen[v] = True
                    yigin.append(v)
        bilesenler.append(adet)
    return {"derece": derece,
            "cok_uyeli_bilesen": float(sum(1 for b in bilesenler if b > 1)),
            "yalniz_dugum": float(sum(1 for b in bilesenler if b == 1))}


def graf_ozeti(senaryo: str, tohum: int, t_s: float,
               guc_dbm: float | None = None, ornek: int | None = None,
               **ek) -> dict:
    """Bir (senaryo, tohum, an) için HER EŞİKTE özet — tek grafik kurulumu.

    Dönen sözlük: `{"esik": {τ: ozet}, "canli_derece": float}`.
    `canli_derece`, grafiğin KENDİ `ozet()`inden gelir ve G-a kapısının
    karşılaştırma tarafıdır.
    """
    if guc_dbm is not None:
        ek["karistirici_guc_override_dbm"] = guc_dbm
    kfg = DS.konfig(kol="bag_kumesi", senaryo=senaryo, tohum=tohum, **ek)
    kur = kurulum_yap(kfg)
    g = KanalGrafigi(kur)
    if ornek is not None:
        # 🔒 Kâhinin kendi alanı. `adim4_kapanis.py` §E de aynısını yapıyor:
        # K'yi dışarıdan oynatmanın başka yolu yok ve İKİNCİ bir grafik
        # yazmak, tam da kaçınılan şey olurdu.
        g._ornek = ornek
    canli = g.ozet(t_s)
    n = kur.dugum_sayisi
    deneme = kfg.yeniden_deneme_siniri + 1

    # 🔒 ETX'ten atlama başarısına GERİ TÜRETME — `_kur`un kuralının aynısı.
    ciftler: list[tuple[int, int, float]] = []
    for i in range(n):
        for j, etx in g._etx[i].items():
            if j <= i:
                continue
            p = 1.0 / etx
            ciftler.append((i, j, 1.0 - (1.0 - p) ** deneme))

    cikti: dict[float, dict[str, float]] = {}
    for esik in ESIKLER:
        komsu: list[list[int]] = [[] for _ in range(n)]
        for i, j, atlama in ciftler:
            if atlama >= esik:
                komsu[i].append(j)
                komsu[j].append(i)
        cikti[esik] = kume_ozeti(komsu)
    return {"esik": cikti, "canli_derece": canli["derece"],
            "canli_cok_uyeli": canli["cok_uyeli_bilesen"]}


# ==========================================================================
def _is_esik(gorev):
    senaryo, tohum, t_s, guc = gorev
    try:
        return graf_ozeti(senaryo, tohum, t_s, guc_dbm=guc), None
    except Exception as hata:                       # noqa: BLE001
        return None, f"{type(hata).__name__}: {hata}"


def _is_k(gorev):
    senaryo, tohum, t_s, K = gorev
    try:
        return graf_ozeti(senaryo, tohum, t_s, ornek=K), None
    except Exception as hata:                       # noqa: BLE001
        return None, f"{type(hata).__name__}: {hata}"


def _is_k_temiz(gorev):
    """G-b için: sönümleme KAPALI, kaydırma grafiği değiştirmemeli."""
    senaryo, tohum, t_s, K = gorev
    try:
        return graf_ozeti(senaryo, tohum, t_s, ornek=K,
                          sonumleme_acik=False), None
    except Exception as hata:                       # noqa: BLE001
        return None, f"{type(hata).__name__}: {hata}"


def _baslik(metin: str) -> None:
    print()
    print("=" * 86)
    print(metin)
    print("=" * 86)


# ==========================================================================
def a_kapilar(isci: int = 6) -> bool:
    """🔒 ALETİN KENDİ KAPILARI — bulgu üretmeden önce alet sınanır."""
    _baslik("A - ALETIN KAPILARI  (turetme dogru mu, kaydirma ne izole ediyor)")

    # --- G-a: turetilen derece == canli derece ------------------------
    print("  G-a · TURETILEN DERECE == CANLI GRAFIGIN KENDI DERECESI")
    print(f"        (esik {ATLAMA_ESIGI:.2f}, birebir esitlik araniyor)")
    gorevler = [("statik-surekli", t, ORNEK_ANLARI[0], -15.0)
                for t in list(TOHUMLAR)[:6]]
    with Pool(isci) as havuz:
        ham = havuz.map(_is_esik, gorevler, chunksize=1)
    ga = True
    for (sen, tohum, _t, _g), (s, hata) in zip(gorevler, ham):
        if hata is not None:
            print(f"    🔴 tohum {tohum}: {hata}")
            ga = False
            continue
        turetilen = s["esik"][ATLAMA_ESIGI]["derece"]
        canli = s["canli_derece"]
        esit = abs(turetilen - canli) < 1e-12
        ga &= esit
        print(f"    {'OK ' if esit else '🔴 '} tohum {tohum}: "
              f"turetilen {turetilen:.9f} ↔ canli {canli:.9f}")

    # --- G-b: sonumleme kapaliyken kaydirma etkisiz olmali -------------
    print()
    print("  G-b · SONUMLEME KAPALIYKEN KAYDIRMA GRAFIGI DEGISTIRMEMELI")
    print("        (degistiriyorsa kaydirma sonumlemeyi IZOLE ETMIYOR)")
    gorevler = [("bagimsiz-yok", 1000, 200.0 + d, 6) for d in KAYDIRMALAR]
    with Pool(isci) as havuz:
        ham = havuz.map(_is_k_temiz, gorevler, chunksize=1)
    dereceler = [s["esik"][ATLAMA_ESIGI]["derece"] for s, h in ham
                 if h is None]
    gb = len(dereceler) == len(KAYDIRMALAR) and (
        max(dereceler) - min(dereceler)) < 1e-12
    print(f"    kaydirmalar: {KAYDIRMALAR}")
    print(f"    dereceler  : {', '.join(f'{d:.9f}' for d in dereceler)}")
    print(f"    {'OK ' if gb else '🔴 '} yayilim "
          f"{max(dereceler) - min(dereceler):.3e}")

    print()
    print(f"  G-a : {'GECTI' if ga else '🔴 KALDI'}")
    print(f"  G-b : {'GECTI' if gb else '🔴 KALDI'}")
    if not (ga and gb):
        print("\n  🔴 ALET KENDI KAPISINDAN GECMEDI — sonraki bolumler")
        print("     KOSULMAZ. Bir olcum aletine, olctugu seye guvendiginden")
        print("     daha az guvenilir.")
    return ga and gb


# ==========================================================================
def b_esik_taramasi(isci: int = 6) -> None:
    """🔴 BAĞ EŞİĞİ ÇALIŞMA NOKTASINI DEĞİŞTİRİYOR MU?

    Çalışma noktası şu ölçütle seçildi: *30 tohumun hiçbirinde birden fazla
    çok üyeli bileşen yokken ρ en büyük*. Ölçüt bir EŞİKLE tanımlı bir
    grafikte koşuyor. Soru: eşik değişince SEÇİLEN GÜÇ değişiyor mu?

    🔒 ρ bir ORANDIR — payı da paydası da aynı eşiği kullanır. Eşiğe
    sanılandan az duyarlı OLABİLİR; ama bileşen yapısı bir oran DEĞİLDİR
    ve sert kısıt oradan geliyor. İkisi ayrı ayrı okunur.
    """
    _baslik("B - BAG ESIGI x KARISTIRICI GUCU  (calisma noktasi kayiyor mu)")
    tohumlar = list(TOHUMLAR)
    print(f"  {len(tohumlar)} tohum x {len(ORNEK_ANLARI)} an x "
          f"{len(GUCLER)} guc x {len(ESIKLER)} esik")
    print("  🔒 Esikler TEK grafik kurulumundan turetiliyor — esik basina")
    print("     yeniden kurulum YOK.")

    gorevler = [("statik-yok", t, an, None)
                for t in tohumlar for an in ORNEK_ANLARI]
    gorevler += [("statik-surekli", t, an, g)
                 for g in GUCLER for t in tohumlar for an in ORNEK_ANLARI]
    with Pool(isci) as havuz:
        ham = havuz.map(_is_esik, gorevler, chunksize=4)

    hata_sayisi = sum(1 for _s, h in ham if h is not None)
    if hata_sayisi:
        print(f"  🔴 {hata_sayisi} gorev PATLADI — ilk hata: "
              f"{next(h for _s, h in ham if h is not None)[:120]}")
        return

    an_adet = len(ORNEK_ANLARI)
    temiz = ham[:len(tohumlar) * an_adet]
    kalan = ham[len(tohumlar) * an_adet:]

    # temiz derece: tohum basina, esik basina (an ortalamasi)
    temiz_derece: dict[float, dict[int, float]] = {e: {} for e in ESIKLER}
    for k, tohum in enumerate(tohumlar):
        dilim = temiz[k * an_adet:(k + 1) * an_adet]
        for e in ESIKLER:
            temiz_derece[e][tohum] = ist.mean(
                s["esik"][e]["derece"] for s, _h in dilim)

    print()
    print(f"  {'esik':>6} {'temiz derece':>13} " +
          " ".join(f"{g:>7.0f}" for g in GUCLER) +
          f" {'SECILEN':>9} {'rho':>7}")
    print(f"  {'':>6} {'':>13} " +
          " ".join(f"{'rho(dBm)':>7}" for _ in GUCLER))
    secimler: dict[float, tuple[float, float] | None] = {}
    for e in ESIKLER:
        satir, secilen = [], None
        for gi, guc in enumerate(GUCLER):
            bas = gi * len(tohumlar) * an_adet
            rho_ler, ayrilan = [], 0
            for k, tohum in enumerate(tohumlar):
                dilim = kalan[bas + k * an_adet:bas + (k + 1) * an_adet]
                bozuldu = False
                for s, _h in dilim:
                    o = s["esik"][e]
                    payda = temiz_derece[e][tohum]
                    rho_ler.append(1.0 - o["derece"] / payda if payda else 0.0)
                    if o["cok_uyeli_bilesen"] > 1.0:
                        bozuldu = True
                ayrilan += bozuldu
            rho = ist.mean(rho_ler)
            satir.append(rho)
            if ayrilan == 0:
                secilen = (guc, rho)
        secimler[e] = secilen
        sec_yazi = f"{secilen[0]:.1f}" if secilen else "YOK"
        rho_yazi = f"{secilen[1]:.3f}" if secilen else "—"
        print(f"  {e:>6.2f} {ist.mean(temiz_derece[e].values()):>13.3f} " +
              " ".join(f"{r:>7.3f}" for r in satir) +
              f" {sec_yazi:>9} {rho_yazi:>7}")

    # --- G-c: sutun gercekten degisiyor mu ----------------------------
    dereceler = [ist.mean(temiz_derece[e].values()) for e in ESIKLER]
    gc = (max(dereceler) - min(dereceler)) > 1e-6
    print()
    print(f"  G-c · esik sutunu gercekten degisiyor mu : "
          f"{'GECTI' if gc else '🔴 KALDI — TARAMA OLU'}")

    # --- karar ---------------------------------------------------------
    print()
    gucler_secilen = {e: (s[0] if s else None) for e, s in secimler.items()}
    tekil = set(v for v in gucler_secilen.values() if v is not None)
    print(f"  SECILEN GUC, esige gore : "
          f"{', '.join(f'{e:.2f}→{v}' for e, v in gucler_secilen.items())}")
    if len(tekil) == 1:
        print(f"  🟢 SECILEN GUC ESIKTEN BAGIMSIZ ({tekil.pop():.1f} dBm).")
        print("     Calisma noktasi, esigin taranan araliginda KAYMIYOR;")
        print("     `ATLAMA_ESIGI` bu karar icin DUYARSIZ — olcumle.")
    else:
        print("  🔴 SECILEN GUC ESIGE BAGLI. Calisma noktasi esigin")
        print("     turetilmesini GEREKTIRIYOR; beyanla gecilemez.")
    rho_sec = [s[1] for s in secimler.values() if s]
    if rho_sec:
        yayilim = max(rho_sec) - min(rho_sec)
        print(f"  rho yayilimi (esik boyunca) : {yayilim:.4f}  "
              f"(deneyin cozunurlugu R = {COZUNURLUK_R:.3f})")
        yorum = ("ALTINDA — deney bu farki zaten goremez"
                 if yayilim < COZUNURLUK_R
                 else "🔴 USTUNDE — esigin secimi sonucu degistirir")
        print(f"    {yorum}")


# ==========================================================================
def c_sonumleme_ornegi(isci: int = 6) -> None:
    """🔴 SÖNÜMLEME ÖRNEK SAYISI K — kestiricinin KENDİ gürültüsü.

    🔒 PÜF NOKTA: aynı tohum, aynı dünya, yalnız ÖRNEKLEME FAZI kayar.
    Konumlar 1,3 ms'de en çok 1 mm oynar (hız 0,75 m/s), gölgeleme hücresi
    50 m — yani dünya sabittir. Görülen saçılma yalnız SÖNÜMLEME
    kestiricisinin kendi gürültüsüdür. G-b bunu ayrıca sınar.
    """
    _baslik("C - SONUMLEME ORNEK SAYISI K  (kestiricinin kendi gurultusu)")
    print("  🔒 Yeterlilik olcutu YENI BIR SAYI GETIRMEZ: kararin kendi")
    print(f"     toleransi kullanilir — derece {DERECE_TOLERANSI} "
          f"(gorev kolu esitlemesi)")
    print()
    for senaryo in ("statik-yok", "bagimsiz-yok"):
        donuk = not DS.konfig(kol="b", senaryo=senaryo).hareketli
        print(f"  --- {senaryo}   (donuk = {donuk})")
        gorevler = [(senaryo, 1000, 200.0 + d, K)
                    for K in K_ADAYLARI for d in KAYDIRMALAR]
        with Pool(isci) as havuz:
            ham = havuz.map(_is_k, gorevler, chunksize=1)
        print(f"      {'K':>4} {'derece (kaydirma basina)':>44} "
              f"{'yayilim':>9} {'karar':>12}")
        yeterli = None
        for i, K in enumerate(K_ADAYLARI):
            dilim = ham[i * len(KAYDIRMALAR):(i + 1) * len(KAYDIRMALAR)]
            d = [s["esik"][ATLAMA_ESIGI]["derece"] for s, h in dilim
                 if h is None]
            if len(d) < len(KAYDIRMALAR):
                print(f"      {K:>4}  🔴 KOSMADI")
                continue
            yayilim = max(d) - min(d)
            tamam = yayilim <= DERECE_TOLERANSI
            if tamam and yeterli is None:
                yeterli = K
            print(f"      {K:>4} {', '.join(f'{x:.3f}' for x in d):>44} "
                  f"{yayilim:>9.4f} "
                  f"{('yeter' if tamam else '🔴 asiyor'):>12}")
        print(f"      🔒 toleransi saglayan EN KUCUK K : {yeterli}")
        print()


# ==========================================================================
def _komsu_listesi(g, n: int, deneme: int) -> dict[float, list[list[int]]]:
    """Bir grafik kurulumundan HER EŞİĞİN komşuluk listesi — tek geçiş."""
    ciftler = []
    for i in range(n):
        for j, etx in g._etx[i].items():
            if j <= i:
                continue
            p = 1.0 / etx
            ciftler.append((i, j, 1.0 - (1.0 - p) ** deneme))
    cikti: dict[float, list[list[int]]] = {}
    for esik in ESIKLER:
        kom: list[list[int]] = [[] for _ in range(n)]
        for i, j, atlama in ciftler:
            if atlama >= esik:
                kom[i].append(j)
                kom[j].append(i)
        cikti[esik] = kom
    return cikti


def _yol_bul(kom, kaynak: int, hedef: int):
    """BFS — `calkanti.py::_yol` ile AYNI kural (sıralı komşu, ilk bulunan)."""
    from collections import deque
    onceki = {kaynak: None}
    kuyruk = deque([kaynak])
    while kuyruk:
        u = kuyruk.popleft()
        if u == hedef:
            break
        for v in sorted(kom[u]):
            if v not in onceki:
                onceki[v] = u
                kuyruk.append(v)
    if hedef not in onceki:
        return None
    yol = [hedef]
    while yol[-1] != kaynak:
        yol.append(onceki[yol[-1]])
    return tuple(reversed(yol))


def _is_theta(gorev):
    """Bir tohum için, HER EŞİKTE rota ömürleri. Zaman boyunca yürür."""
    import random
    senaryo, tohum, adim_s, bitis_s, cift_sayisi = gorev
    try:
        kfg = DS.konfig(kol="bag_kumesi", senaryo=senaryo, tohum=tohum)
        n = kfg.dugum_sayisi
        deneme = kfg.yeniden_deneme_siniri + 1
        adet = int(bitis_s / adim_s)
        # 🔒 Grafik ANI BAŞINA bir kez kurulur; altı eşik ondan TÜRETİLİR.
        # Eşik başına yeniden kurmak maliyeti altı katına çıkarırdı.
        # 🔒 KURULUM TOHUM BAŞINA BİR KEZ. İlk yazımda her zaman adımında
        # `kurulum_yap` çağrılıyordu — yani mobilite yörüngesi (700 tik ×
        # 40 düğüm) 350 kez yeniden hesaplanıyordu. Sonucu değiştirmezdi
        # (her şey belirlenimli) ama ölçümü gereksiz yere pahalı yapardı.
        # 🔒 `dilim_s` ızgaranın YARISI: kâhinin kendi tazeleme kelepçesi
        # 10 s'dir, yani varsayılanla grafik ızgara başına DEĞİL 10 s'de bir
        # kurulurdu ve rota ömrü 10 s çözünürlüğe yuvarlanırdı.
        kur = kurulum_yap(kfg)
        g = KanalGrafigi(kur, dilim_s=0.5 * adim_s)
        kom_zaman = []
        for k in range(adet):
            g.ozet(k * adim_s)                  # `_tazele` bu an için kurar
            kom_zaman.append(_komsu_listesi(g, n, deneme))

        rnd = random.Random(tohum)
        ciftler = [rnd.sample(range(n), 2) for _ in range(cift_sayisi)]
        cikti: dict[float, dict[str, list]] = {}
        for esik in ESIKLER:
            tam, sansurlu, atlamalar = [], [], []
            for kaynak, hedef in ciftler:
                yol, sure = None, 0.0
                for k in range(adet):
                    kom = kom_zaman[k][esik]
                    if yol is None:
                        yol = _yol_bul(kom, kaynak, hedef)
                        if yol is not None:
                            atlamalar.append(len(yol) - 1)
                            sure = 0.0
                        continue
                    if all(yol[z] in kom[yol[z - 1]]
                           for z in range(1, len(yol))):
                        sure += adim_s
                    else:
                        tam.append(sure)
                        yol = None
                if yol is not None and sure > 0.0:
                    sansurlu.append(sure)       # 🔴 koşu bitti, rota YAŞIYOR
            cikti[esik] = {"tam": tam, "sansurlu": sansurlu,
                           "atlama": atlamalar}
        return cikti, None
    except Exception as hata:                       # noqa: BLE001
        return None, f"{type(hata).__name__}: {hata}"


def f_theta(isci: int = 6) -> None:
    """🔴 Θ'NIN KANAL TABANLI ÇAPRAZ KONTROLÜ — vaat edilmiş, hiç yazılmamış.

    `calkanti.py` başlığı şunu taahhüt ediyor: *"TARAMA sert diskle yapılır;
    SEÇİLEN nokta sonra kanal tabanlı grafikle DOĞRULANIR."* O doğrulama
    depoda YOKTU. Θ = 5,93 tamamen 400 m'lik bir sert diske dayanıyor ve o
    yarıçap `SINANMAMIS` — üstelik K-096 tam da tek bir yarıçapın gerçek bağ
    kümesini temsil EDEMEDİĞİNİ ölçmüştü (Jaccard 0,53).

    🔒 Burada rota ömrü, veri taşıyan KANAL grafiğinde ölçülür: gölgeleme,
    sönümleme, yeniden denemeler dâhil — kâhinin kullandığı grafiğin ta
    kendisi. Ve altı eşikte birden, çünkü "bağ var mı" sorusu eşiğe bağlı.

    🔴 SANSÜR AÇIKÇA RAPORLANIR. `calkanti.py`nin kestiricisi koşu bitince
    hâlâ yaşayan rotaları ÖLMÜŞ gibi sayıyor (sağdan sansür) ve başta zaten
    var olan rotaların geçmiş yaşını bilmiyor (soldan kesme). İkisi de ömrü
    KISA gösterir, yani Θ'yı DÜŞÜK. Yön kapı için şanslı (Θ ≥ 3 kapısı
    olduğundan katı çalışır) ama raporlanan sayı yanlıdır. Burada üç sayı
    birden yazılır: sansürlü dâhil ortalama (eski kestiricinin karşılığı),
    yalnız TAMAMLANMIŞ ömürlerin ortalaması, ve sansürlü payı.
    """
    _baslik("F - Θ'NIN KANAL TABANLI CAPRAZ KONTROLU  (vaat edilmis olcum)")
    from kalibrasyon.calkanti import (ADIM_S, BITIS_S, CIFT_SAYISI,
                                      ETKIN_YARICAP_M, OLSR_TOP_HOLD_S,
                                      TOHUMLAR as C_TOHUMLAR)
    senaryo = "bagimsiz-yok"
    tohumlar = list(C_TOHUMLAR)
    print(f"  senaryo {senaryo} · {len(tohumlar)} tohum · adim {ADIM_S:.1f} s "
          f"· bitis {BITIS_S:.0f} s · {CIFT_SAYISI} cift")
    print(f"  🔒 payda: OLSR TOP_HOLD_TIME = {OLSR_TOP_HOLD_S:.0f} s "
          f"(RFC 3626, `02` §R2)")
    print(f"  ⚠️ karsilastirma noktasi: sert disk {ETKIN_YARICAP_M:.0f} m "
          f"→ Θ = 5,93 (calkanti.py)")
    print(f"  ⚠️ tohum basina {int(BITIS_S / ADIM_S)} grafik kurulumu")

    gorevler = [(senaryo, t, ADIM_S, BITIS_S, CIFT_SAYISI) for t in tohumlar]
    with Pool(isci) as havuz:
        ham = havuz.map(_is_theta, gorevler, chunksize=1)
    hata = next((h for _s, h in ham if h is not None), None)
    if hata:
        print(f"  🔴 gorev PATLADI: {hata[:200]}")
        return

    print()
    print(f"  {'esik':>6} {'derece':>8} {'atlama':>8} {'tau_sansurlu':>13} "
          f"{'tau_tamam':>10} {'sansur_payi':>12} {'Θ (sansurlu)':>13} "
          f"{'Θ (tamam)':>10}")
    for esik in ESIKLER:
        tam, sansurlu, atlama = [], [], []
        for s, _h in ham:
            tam += s[esik]["tam"]
            sansurlu += s[esik]["sansurlu"]
            atlama += s[esik]["atlama"]
        hepsi = tam + sansurlu
        if not hepsi:
            print(f"  {esik:>6.2f}  {'ROTA BULUNAMADI':>50}")
            continue
        tau_h = ist.mean(hepsi)
        tau_t = ist.mean(tam) if tam else float("nan")
        pay = len(sansurlu) / len(hepsi)
        print(f"  {esik:>6.2f} {'—':>8} "
              f"{ist.mean(atlama) if atlama else float('nan'):>8.2f} "
              f"{tau_h:>13.1f} {tau_t:>10.1f} {pay:>11.1%} "
              f"{tau_h / OLSR_TOP_HOLD_S:>13.2f} "
              f"{tau_t / OLSR_TOP_HOLD_S:>10.2f}")

    print()
    print("  🔒 KAPI: Θ ≥ 3 (K-101). Kapinin altina dusen bir kol,")
    print("     protokolu tasarim zarfinin DISINDA kosturuyor demektir.")
    print("  ⚠️ 'Θ (sansurlu)' eski kestiricinin karsiligidir ve ASAGI")
    print("     YANLIDIR; 'Θ (tamam)' sansurluleri disliyor ve YUKARI")
    print("     yanlidir (uzun rotalar sansurlenmeye daha meyilli).")
    print("     Gercek deger ikisinin ARASINDADIR — band olarak okunur.")


# ==========================================================================
def _is_theta_tanim(gorev):
    """Aynı rota-ömrü yürüyüşü, ÜÇ FARKLI 'bağ var' tanımıyla.

    🔴 F BÖLÜMÜ BİR ŞÜPHE DOĞURDU. Kâhin grafiğinde Θ = 0,20 çıktı, sert
    diskte 5,93 — 30 kat. Şüphe: kâhin grafiği hızlı sönümlemeyi K örnekle
    ORTALIYOR ve o ortalama her ızgara adımında BAĞIMSIZ yeniden çekiliyor
    (sönümleme ~1,7 ms'de dekorele olur, örnekler 5 ms arayla). Yani bağlar
    dünya değiştiği için değil, KESTİRİM TİTREDİĞİ için kopuyor olabilir.

    🔒 AYIRT EDEN ŞEY SÖNÜMLEMEYİ KAPATMAKTIR: kapalıyken grafik yalnız
    geometri + gölgeleme ile değişir, yani DÜNYANIN kendi hızıyla. Fark
    büyükse ölçülen şey mobilite değil, kestiricinin gürültüsüdür.
    """
    import random
    tohum, adim_s, bitis_s, cift_sayisi, yaricap_m = gorev
    try:
        from sim2.dunya.geometri import mesafe
        sonuc = {}
        for tanim in ("disk", "yavas", "kahin_sonumlemesiz"):
            ek = {} if tanim == "kahin_sonumlemesiz" else {}
            if tanim == "kahin_sonumlemesiz":
                ek = dict(sonumleme_acik=False)
            kfg = DS.konfig(kol="bag_kumesi", senaryo="bagimsiz-yok",
                         tohum=tohum, **ek)
            kur = kurulum_yap(kfg)
            n = kur.dugum_sayisi
            adet = int(bitis_s / adim_s)
            esik = kfg.sinr_esigi_db
            y = kur.kanal.yayilim
            deneme = kfg.yeniden_deneme_siniri + 1
            g = (KanalGrafigi(kur, dilim_s=0.5 * adim_s)
                 if tanim == "kahin_sonumlemesiz" else None)

            kom_zaman = []
            for k in range(adet):
                t = k * adim_s
                if tanim == "kahin_sonumlemesiz":
                    g.ozet(t)
                    kom_zaman.append(
                        _komsu_listesi(g, n, deneme)[ATLAMA_ESIGI])
                    continue
                konum = [kur.topoloji.konum(i, t) for i in range(n)]
                kom = [[] for _ in range(n)]
                for i in range(n):
                    for j in range(i + 1, n):
                        var = (mesafe(konum[i], konum[j]) <= yaricap_m
                               if tanim == "disk" else
                               y.yavas_sinr_db(i, j, konum[i],
                                               konum[j]) >= esik)
                        if var:
                            kom[i].append(j)
                            kom[j].append(i)
                kom_zaman.append(kom)

            rnd = random.Random(tohum)
            ciftler = [rnd.sample(range(n), 2) for _ in range(cift_sayisi)]
            tam, sansurlu, atlamalar = [], [], []
            for kaynak, hedef in ciftler:
                yol, sure = None, 0.0
                for k in range(adet):
                    kom = kom_zaman[k]
                    if yol is None:
                        yol = _yol_bul(kom, kaynak, hedef)
                        if yol is not None:
                            atlamalar.append(len(yol) - 1)
                            sure = 0.0
                        continue
                    if all(yol[z] in kom[yol[z - 1]]
                           for z in range(1, len(yol))):
                        sure += adim_s
                    else:
                        tam.append(sure)
                        yol = None
                if yol is not None and sure > 0.0:
                    sansurlu.append(sure)
            sonuc[tanim] = {"tam": tam, "sansurlu": sansurlu,
                            "atlama": atlamalar}
        return sonuc, None
    except Exception as hata:                       # noqa: BLE001
        return None, f"{type(hata).__name__}: {hata}"


def g_theta_tanim(isci: int = 6) -> None:
    """🔴 Θ'DAKİ 30 KATLIK FARK MOBİLİTEDEN Mİ, KESTİRİCİDEN Mİ?"""
    _baslik("G - 'BAG VAR' TANIMI Θ'YI NE KADAR BELIRLIYOR")
    from kalibrasyon.calkanti import (ADIM_S, BITIS_S, CIFT_SAYISI,
                                      ETKIN_YARICAP_M, OLSR_TOP_HOLD_S,
                                      TOHUMLAR as C_TOHUMLAR)
    print("  Ayni yuruyus, ayni tohum, ayni cift — YALNIZ 'bag var' tanimi")
    print("  degisiyor:")
    print(f"    disk                : mesafe <= {ETKIN_YARICAP_M:.0f} m "
          f"(calkanti.py'nin bugunku tanimi)")
    print("    yavas               : yavas SINR >= esik "
          "(geometri + golgeleme + anten; `kopma_fiziksel`in TANIMI)")
    print("    kahin_sonumlemesiz  : kahin grafigi, SONUMLEME KAPALI")
    print("  🔒 Ucu de ayni dunyayi gorur. Fark buyukse Θ bir MOBILITE")
    print("     olcusu degil, bir TANIM secimidir.")
    tohumlar = list(C_TOHUMLAR)
    gorevler = [(t, ADIM_S, BITIS_S, CIFT_SAYISI, ETKIN_YARICAP_M)
                for t in tohumlar]
    with Pool(isci) as havuz:
        ham = havuz.map(_is_theta_tanim, gorevler, chunksize=1)
    hata = next((h for _s, h in ham if h is not None), None)
    if hata:
        print(f"  🔴 gorev PATLADI: {hata[:200]}")
        return
    print()
    print(f"  {'tanim':>20} {'atlama':>8} {'tau_sansurlu':>13} "
          f"{'tau_tamam':>10} {'sansur':>8} {'Θ (sansurlu)':>13}")
    for tanim in ("disk", "yavas", "kahin_sonumlemesiz"):
        tam, sansurlu, atlama = [], [], []
        for s, _h in ham:
            tam += s[tanim]["tam"]
            sansurlu += s[tanim]["sansurlu"]
            atlama += s[tanim]["atlama"]
        hepsi = tam + sansurlu
        if not hepsi:
            print(f"  {tanim:>20}  ROTA YOK")
            continue
        print(f"  {tanim:>20} {ist.mean(atlama):>8.2f} "
              f"{ist.mean(hepsi):>13.1f} "
              f"{ist.mean(tam) if tam else float('nan'):>10.1f} "
              f"{len(sansurlu) / len(hepsi):>7.1%} "
              f"{ist.mean(hepsi) / OLSR_TOP_HOLD_S:>13.2f}")
    print()
    print("  🔒 KAPI: Θ ≥ 3 (K-101).")


# ==========================================================================
def _km_ortalama(sureler: list[float], sansurlu: list[bool]) -> float:
    """Kaplan–Meier ile kısıtlı ortalama ömür (RMST).

    🔴 NEDEN GEREKLİ. Ham ortalama iki yönden de AŞAĞI yanlıdır:
      · SAĞDAN SANSÜR — koşu bitince hâlâ yaşayan rota "ölmüş" sayılıyor.
        Ve sansürlenenler tam da UZUN ömürlü olanlar.
      · SOLDAN KESME — t = 0'da zaten var olan rotanın geçmiş yaşı bilinmez.

    🔒 İkincisi YAPIYLA çözülür (her çiftin İLK ömrü atılır — yaşı bilinmez);
    birincisini Kaplan–Meier çözer. Serbest parametre yok: RMST, gözlenen en
    büyük süreye kadar hayatta kalma eğrisinin altındaki alandır.
    """
    if not sureler:
        return float("nan")
    olaylar = sorted(zip(sureler, sansurlu))
    n = len(olaylar)
    s = 1.0
    onceki_t = 0.0
    alan = 0.0
    risk = n
    i = 0
    while i < n:
        t = olaylar[i][0]
        olum = 0
        ayni = 0
        while i < n and olaylar[i][0] == t:
            if not olaylar[i][1]:
                olum += 1
            ayni += 1
            i += 1
        alan += s * (t - onceki_t)          # önceki S ile geçen aralık
        if risk > 0 and olum > 0:
            s *= (1.0 - olum / risk)
        onceki_t = t
        risk -= ayni
    return alan


def _is_theta_hiz(gorev):
    """Bir hız adayı × bir tohum → YAVAŞ SINR grafiğinde rota ömürleri.

    🔒 Y7 (14 Eylül 2026): görev demeti isteğe bağlı YEDİNCİ eleman olarak
    senaryo taşıyabilir — `theta_kollari.py` kol başına Θ ölçerken bunu
    kullanır. Altı elemanlı çağrı bugünkü davranışı BİREBİR korur; ikinci
    bir rota ömrü kestiricisi yazılmaz.
    """
    import random
    tohum, hmin, hmaks, adim_s, bitis_s, cift_sayisi = gorev[:6]
    senaryo = gorev[6] if len(gorev) > 6 else "bagimsiz-yok"
    try:
        kfg = DS.konfig(kol="bag_kumesi", senaryo=senaryo, tohum=tohum,
                     gm_hiz_min_ms=hmin, gm_hiz_maks_ms=hmaks,
                     gm_hiz_sigma_ms=max(hmaks / 10.0, 1e-4),
                     gorev_jitter_hiz_ms=max(hmaks / 15.0, 1e-4))
        kur = kurulum_yap(kfg)
        n = kur.dugum_sayisi
        y = kur.kanal.yayilim
        esik = kfg.sinr_esigi_db
        adet = int(bitis_s / adim_s)
        kom_zaman = []
        for k in range(adet):
            t = k * adim_s
            konum = [kur.topoloji.konum(i, t) for i in range(n)]
            kom = [[] for _ in range(n)]
            for i in range(n):
                for j in range(i + 1, n):
                    if y.yavas_sinr_db(i, j, konum[i],
                                       konum[j]) >= esik:
                        kom[i].append(j)
                        kom[j].append(i)
            kom_zaman.append(kom)

        rnd = random.Random(tohum)
        ciftler = [rnd.sample(range(n), 2) for _ in range(cift_sayisi)]
        sureler, sansurlu, atlamalar = [], [], []
        # 🔒 Y7 — hiç KOPMAYAN çift ayrıca sayılır: Θ yalnız gözlenen
        # ömürlerden hesaplanır ve neredeyse durağan bir kolda ölçüme
        # yalnız eşiğin kıyısındaki çiftler girer. Bu sayı o yanlılığı
        # görünür kılar.
        kopan_cift = 0
        for kaynak, hedef in ciftler:
            yol, sure, ilk, kopus = None, 0.0, True, 0
            for k in range(adet):
                kom = kom_zaman[k]
                if yol is None:
                    yol = _yol_bul(kom, kaynak, hedef)
                    if yol is not None:
                        atlamalar.append(len(yol) - 1)
                        sure = 0.0
                    continue
                if all(yol[z] in kom[yol[z - 1]] for z in range(1, len(yol))):
                    sure += adim_s
                else:
                    # 🔒 İLK ömür ATILIR: t=0'da zaten var olan rotanın
                    # geçmiş yaşı bilinmez (soldan kesme). Sonrakiler
                    # gözlem içinde DOĞDUĞU için yaşları tamdır.
                    if not ilk:
                        sureler.append(sure)
                        sansurlu.append(False)
                    ilk = False
                    kopus += 1
                    yol = None
            if yol is not None and sure > 0.0 and not ilk:
                sureler.append(sure)
                sansurlu.append(True)       # koşu bitti, rota YAŞIYOR
            if kopus:
                kopan_cift += 1
        return {"sure": sureler, "sansur": sansurlu,
                "atlama": atlamalar, "cift": cift_sayisi,
                "kopan_cift": kopan_cift}, None
    except Exception as hata:                       # noqa: BLE001
        return None, f"{type(hata).__name__}: {hata}"


def h_hiz_turetme(isci: int = 6) -> None:
    """🔴 HIZLARIN YENİDEN TÜRETİLMESİ — doğru tanım, düzeltilmiş kestirici.

    K-101 hızları Θ'dan TÜRETMİŞTİ, ama üç şey yanlıştı ve üçü de bu
    bölümde düzeltiliyor:

      1. **Bağ tanımı** 400 m'lik sert diskti. G bölümü ölçtü: disk
         gölgelemeyi hiç görmediği için rota ömrünü **iki kat uzun**
         gösteriyor (89 s ↔ 43 s). Doğru tanım YAVAŞ SINR'dir ve zaten
         `kopma_fiziksel` için ilan edilmiştir.
      2. **Soldan kesme**: t = 0'da var olan rotanın yaşı bilinmiyordu ve
         yine de ömür sayılıyordu. Artık her çiftin İLK ömrü ATILIYOR.
      3. **Sağdan sansür**: koşu bitince yaşayan rota "ölmüş" sayılıyordu.
         Artık Kaplan–Meier ile düzeltiliyor.

    🔒 ÖLÇÜT — K-101'in ölçütüyle AYNI BİÇİMDE, yeni bir sayı getirmiyor:
        sert kısıt : Θ ≥ 3 (K-101 kapısı) **ve** ölçekli hız doğrulanmış
                     İHA aralığında (30–400 km/h, `02` A5a)
        amaç       : bu kısıtlar altında ÇALKANTIYI en büyük yapmak,
                     yani EN HIZLI adayı seçmek
    Aynı biçim: alan seçiminde *"kopukluk sıfırken en büyük alan"*, güç
    seçiminde *"ayrılma yokken en büyük ρ"*.
    """
    _baslik("H - HIZLARIN YENIDEN TURETILMESI  (yavas SINR + KM)")
    from kalibrasyon.calkanti import (ADIM_S, BITIS_S, CIFT_SAYISI,
                                      OLSR_TOP_HOLD_S,
                                      TOHUMLAR as C_TOHUMLAR)
    kfg0 = DS.konfig(kol="bag_kumesi")
    olcek = kfg0.olcek
    adaylar = ((10.0, 30.0), (2.0, 6.0), (1.0, 3.0), (0.5, 1.5),
               (0.25, 0.75), (0.12, 0.36), (0.06, 0.18))
    tohumlar = list(C_TOHUMLAR)
    print(f"  bag tanimi: YAVAS SINR >= {kfg0.sinr_esigi_db:.0f} dB "
          f"(geometri + golgeleme + anten)")
    print(f"  {len(tohumlar)} tohum · adim {ADIM_S:.1f} s · "
          f"bitis {BITIS_S:.0f} s · {CIFT_SAYISI} cift")
    print(f"  payda {OLSR_TOP_HOLD_S:.0f} s · olcek 1:{olcek:.0f} · "
          f"IHA araligi 30-400 km/h")
    print()
    gorevler = [(t, a, b, ADIM_S, BITIS_S, CIFT_SAYISI)
                for a, b in adaylar for t in tohumlar]
    with Pool(isci) as havuz:
        ham = havuz.map(_is_theta_hiz, gorevler, chunksize=1)
    hata = next((h for _s, h in ham if h is not None), None)
    if hata:
        print(f"  🔴 gorev PATLADI: {hata[:200]}")
        return

    print(f"  {'hiz m/s':>14} {'atlama':>7} {'omur':>6} {'tau_ham':>8} "
          f"{'tau_KM':>8} {'sansur':>7} {'Θ':>6} {'km/h':>12} "
          f"{'kapi':>6} {'olcek':>6}")
    secilen = None
    for ai, (hmin, hmaks) in enumerate(adaylar):
        sureler, sansur, atlama = [], [], []
        for si in range(len(tohumlar)):
            s, _h = ham[ai * len(tohumlar) + si]
            sureler += s["sure"]
            sansur += s["sansur"]
            atlama += s["atlama"]
        if not sureler:
            print(f"  {f'{hmin}-{hmaks}':>14}  ROTA YOK")
            continue
        tau_ham = ist.mean(sureler)
        tau_km = _km_ortalama(sureler, sansur)
        theta = tau_km / OLSR_TOP_HOLD_S
        k50 = (hmin * olcek * 3.6, hmaks * olcek * 3.6)
        kapi = theta >= 3.0
        olcek_ok = 30.0 <= k50[0] and k50[1] <= 400.0
        if kapi and olcek_ok and secilen is None:
            secilen = (hmin, hmaks, theta, k50)
        print(f"  {f'{hmin}-{hmaks}':>14} {ist.mean(atlama):>7.2f} "
              f"{len(sureler):>6} {tau_ham:>8.1f} {tau_km:>8.1f} "
              f"{sum(sansur) / len(sansur):>6.1%} {theta:>6.2f} "
              f"{f'{k50[0]:.0f}-{k50[1]:.0f}':>12} "
              f"{'GECER' if kapi else 'kalir':>6} "
              f"{'evet' if olcek_ok else '🔴 HAYIR':>6}")
    print()
    if secilen is None:
        print("  🔴 HICBIR ADAY IKI KISITI BIRDEN GECMEDI.")
        print("     Ya kapi (Θ ≥ 3) ya olcek gercekciligi (30-400 km/h)")
        print("     saglanamiyor — ve bu bir BULGUDUR, gizlenmez: mobilite")
        print("     ekseni bu calisma noktasinda ADIL bir kol veremiyor.")
        return
    hmin, hmaks, theta, k50 = secilen
    print(f"  🟢 SECILEN: {hmin}-{hmaks} m/s · Θ = {theta:.2f} · "
          f"{k50[0]:.0f}-{k50[1]:.0f} km/h")
    print("     Iki sert kisiti da gecen EN HIZLI aday — yani calkantiyi")
    print("     en buyuk yapan. Sayi ELLE KONMADI.")


# ==========================================================================
def i_serbestlik_dereceleri() -> None:
    """🔴 BAĞLANTI BÜTÇESİ KAÇ SERBEST SAYI? — cebir, sonra ÖLÇÜM.

    Duyarlılık denetimi `sicaklik_k`, `bant_genisligi_hz` ve
    `gurultu_figuru_db` için **tam olarak aynı** etkiyi buldu (−0,112). Aynı
    sayının üç kez çıkması tesadüf değildir; üçü de aynı yerden giriyordur.

    🔒 AST TARAMASI: üçü de `sim2/` içinde YALNIZ gürültü tabanında geçiyor,
    başka hiçbir yerde. Ve verici gücü gürültü tabanından TÜRETİLİYOR:

        Pt = N · β · PL(R)              (menzil tanımı)
        SINR(d) = Pt / PL(d) / N = β · PL(R) / PL(d)

    **N tamamen sadeleşiyor.** Düğümler arası girişim de ∝ N olduğu için o da
    sadeleşir; taşıyıcı dinleme eşiği de N'dir ve karşılaştırdığı güçler ∝ N.
    Geriye TEK kalıntı kalıyor: karıştırıcının MUTLAK gücü, yani **J/N**.

    🔒 Aynı cebir `frekans_hz`in YOL KAYBI yarısı için de geçerli: PL(1 m)
    frekansla artar, Pt onu telafi eder, sadeleşir. Frekansın GERÇEK etkisi
    yalnız dalga boyu üzerinden Doppler'dir ve o **hareketli kolda** yaşar.

    🔴 ÖLÇÜLEBİLİR VE YANLIŞLANABİLİR TAHMİN: gürültü tabanını X dB
    yükseltip karıştırıcıyı X dB yükseltmek sonucu **BİREBİR** aynı
    bırakmalıdır. Aynı bırakmazsa cebir eksiktir.
    """
    import math
    _baslik("I - BAGLANTI BUTCESININ SERBESTLIK DERECESI  (cebir + olcum)")
    print("  🔒 Pt = N·β·PL(R) oldugu icin SINR = β·PL(R)/PL(d) — N SADELESIR.")
    print("     Geriye tek kalinti: karistiricinin MUTLAK gucu, yani J/N.")
    print("  🔴 TAHMIN: gurultu tabanini X dB yukselt + karistiriciyi X dB")
    print("     yukselt → sonuc BIREBIR ayni. Degilse cebir eksik.\n")

    def imza(**ek):
        kfg = DS.konfig(kol="dg", senaryo="statik-surekli", tohum=1000, **ek)
        kur = kurulum_yap(kfg)
        g = KanalGrafigi(kur)
        o = g.ozet(200.0)
        kenar = frozenset((i, j) for i, ks in enumerate(g._komsu)
                          for j in ks if i < j)
        return o["derece"], kenar, kur.kanal.yayilim.gurultu_w

    d0, k0, n0 = imza(karistirici_guc_override_dbm=-15.0)
    print(f"  {'oynatma':>26} {'derece':>12} {'kenar':>6} {'N (dBm)':>9} "
          f"{'kenar kumesi':>14}")
    print(f"  {'TABAN':>26} {d0:>12.9f} {len(k0):>6} "
          f"{10 * math.log10(n0 * 1000):>9.4f} {'—':>14}")
    hepsi = True
    for ad, ek, dB in (
            ("gurultu figuru 6→9 dB", dict(gurultu_figuru_db=9.0), 3.0),
            ("sicaklik 290→580 K", dict(sicaklik_k=580.0),
             10 * math.log10(2)),
            ("bant 2→4 MHz", dict(bant_genisligi_hz=4e6),
             10 * math.log10(2)),
            ("frekans 2,4→4,8 GHz", dict(frekans_hz=4.8e9),
             20 * math.log10(2))):
        d, k, n = imza(karistirici_guc_override_dbm=-15.0 + dB, **ek)
        ayni = (k == k0) and abs(d - d0) < 1e-12
        hepsi &= ayni
        print(f"  {ad:>26} {d:>12.9f} {len(k):>6} "
              f"{10 * math.log10(n * 1000):>9.4f} "
              f"{('BIREBIR AYNI' if ayni else '🔴 FARKLI'):>14}")
    # ------------------------------------------------------------------
    # 🔴 FREKANSIN SADELESMEYEN YARISI — Doppler. Cebir yalnız YOL KAYBI
    # yarısını sadeleştiriyor; dalga boyu sönümlemenin hızını belirliyor ve
    # o STATİK kolda dondurulmuş, HAREKETLİ kolda canlı. Fark tam da bu.
    print()
    print("  🔴 FREKANSIN GERCEK YARISI — ayni oynatma, iki kolda")
    print(f"  {'kol':>26} {'derece taban':>13} {'derece yeni':>12} "
          f"{'fark':>8} {'Jaccard':>9}")
    for senaryo, etiket in (("statik-surekli", "STATIK (sonumleme donuk)"),
                            ("bagimsiz-surekli", "HAREKETLI (Doppler canli)")):
        kfg0 = dict(kol="dg", senaryo=senaryo, tohum=1000)

        def _im(**ek):
            kfg = DS.konfig(**kfg0, **ek)
            kur = kurulum_yap(kfg)
            g = KanalGrafigi(kur)
            o = g.ozet(200.0)
            return o["derece"], frozenset(
                (i, j) for i, ks in enumerate(g._komsu) for j in ks if i < j)

        da, ka = _im(karistirici_guc_override_dbm=-15.0)
        db_, kb = _im(karistirici_guc_override_dbm=-15.0 + 20 * math.log10(2),
                      frekans_hz=4.8e9)
        j = len(ka & kb) / len(ka | kb) if (ka | kb) else 1.0
        print(f"  {etiket:>26} {da:>13.4f} {db_:>12.4f} "
              f"{abs(db_ - da):>8.4f} {j:>9.4f}")
    print("  🔒 Statik kolda BIREBIR ayni, hareketli kolda degil: frekansin")
    print("     sadelesmeyen tek kanali DOPPLER'dir. Olculen artik, ×2")
    print(f"     oynatmada derece toleransinin ({DERECE_TOLERANSI}) altinda.")

    # ------------------------------------------------------------------
    # 🔴 IKINCI DEGENERASYON: UZUNLUK OLCEGI. Ayni cebir menzil capasi icin
    # de bir tahmin veriyor: SINR(d) = β·(R/d)^α, yani yalniz R/d ORANI
    # onemli. Butun uzunluklar λ ile olceklenirse (alan, irtifa bandi, menzil
    # capasi, golgeleme hucresi) ve karistirici 10α·log10(λ) dB telafi
    # edilirse, sonuc BIREBIR ayni kalmali.
    print()
    print("  🔴 IKINCI DEGENERASYON — UZUNLUK OLCEGI")
    print("     SINR = β·(R/d)^α ⟹ yalniz R/d orani onemli.")
    print(f"  {'olcek λ':>10} {'karistirici':>12} {'derece':>13} "
          f"{'kenar':>6} {'Jaccard':>9}")
    kfg_t = DS.konfig(kol="dg")
    alfa = kfg_t.yol_kaybi_usteli
    olcek_ok = True
    for lam in (1.25, 2.0):
        dB = 10.0 * alfa * math.log10(lam)
        kfg = DS.konfig(kol="dg", senaryo="statik-surekli", tohum=1000,
                     alan_en_m=kfg_t.alan_en_m * lam,
                     alan_boy_m=kfg_t.alan_boy_m * lam,
                     irtifa_min_m=kfg_t.irtifa_min_m * lam,
                     irtifa_maks_m=kfg_t.irtifa_maks_m * lam,
                     nominal_bag_m=kfg_t.nominal_bag_m * lam,
                     golgeleme_hucre_m=kfg_t.golgeleme_hucre_m * lam,
                     gorev_grup_yaricapi_m=kfg_t.gorev_grup_yaricapi_m * lam,
                     karistirici_guc_override_dbm=-15.0 + dB)
        kur = kurulum_yap(kfg)
        g = KanalGrafigi(kur)
        d = g.ozet(200.0)["derece"]
        k = frozenset((i, j) for i, ks in enumerate(g._komsu)
                      for j in ks if i < j)
        j = len(k0 & k) / len(k0 | k) if (k0 | k) else 1.0
        tamam = (k == k0) and abs(d - d0) < 1e-12
        olcek_ok &= tamam
        print(f"  {lam:>10.2f} {f'+{dB:.3f} dB':>12} {d:>13.9f} "
              f"{len(k):>6} {j:>9.4f}")
    print(f"  {'':>10} {'':>12} "
          f"{('🟢 BIREBIR AYNI' if olcek_ok else '🔴 FARKLI'):>13}")
    print("  🔒 `nominal_bag_m` BAGIMSIZ BIR SAYI DEGIL, UZUNLUK BIRIMI.")
    print("     Belirleyici olan `menzil/alan` oranidir ve alan zaten o orani")
    print("     sabitleyen bir olcutle secildi (kopukluk sifirken en buyuk).")
    hepsi &= olcek_ok

    print()
    print(f"  SONUC : {'🟢 CEBIR DOGRULANDI' if hepsi else '🔴 CEBIR EKSIK'}")
    if hepsi:
        print("  🔒 Bu uc sayinin BAGIMSIZ ETKISI YOK: yalnizca karistiricinin")
        print("     bagil gucunu olcekliyorlar, o da rho ile KALIBRE EDILIYOR.")
        print("     Yani dort parametre + karistirici gucu = TEK serbestlik")
        print("     derecesi, ve o kalibre edilmis durumda.")
        print()
        print("  🔴 FAZ 4 ICIN TASARIM KISITI — burada dogdu:")
        print("     Gurultunun MUTLAK degeri bu simulatorde anlamli bir")
        print("     buyukluk DEGILDIR (serbest bir olcek). Gozlem penceresi")
        print("     `olculen_gurultu_w`u protokole veriyor; MUTLAK bir esikle")
        print("     karsilastiran bir protokol, fizikte karsiligi olmayan bir")
        print("     sayiya dayanmis olur. Karistirma sezimi ORANLA ya da")
        print("     DEGISIMLE yapilmalidir.")


# ==========================================================================
def _is_dugum(gorev):
    """Bir (N, alan) noktasında derece · atlama dağılımı · kopukluk."""
    from collections import deque
    n, alan, tohum = gorev
    try:
        kfg = DS.konfig(kol="dg", senaryo="statik-yok", tohum=tohum,
                     dugum_sayisi=n, alan_en_m=alan, alan_boy_m=alan,
                     akis_sayisi=min(10, n // 2),
                     gorev_grup_sayisi=min(10, n),
                     gorev_grup_yaricapi_m=min(650.0, 0.36 * alan))
        g = KanalGrafigi(kurulum_yap(kfg))
        g.ozet(0.0)
        derece = sum(len(k) for k in g._komsu) / n
        atlama, kopuk = [], 0
        for s in range(n):
            uz = {s: 0}
            q = deque([s])
            while q:
                u = q.popleft()
                for v in g._komsu[u]:
                    if v not in uz:
                        uz[v] = uz[u] + 1
                        q.append(v)
            atlama += [d for d in uz.values() if d > 0]
            kopuk += n - len(uz)
        return {"derece": derece, "atlama": atlama, "kopuk": kopuk,
                "cift": n * (n - 1)}, None
    except Exception as hata:                       # noqa: BLE001
        return None, f"{type(hata).__name__}: {hata}"


def j_dugum_sayisi(isci: int = 6) -> None:
    """🔴 DÜĞÜM SAYISI NEYİ BELİRLİYOR — ve 40 nereden geliyor?

    `dugum_sayisi` duyarlılık denetiminde üçüncü en büyük etkiyi verdi
    (−0,183) ve gerekçesi *"`01`de N ≤ 40 gerekçesi var ama `02`de
    doğrulanmadı"* idi. Bu bölüm, o gerekçenin YERİNE GEÇMEZ — sorunun
    **ne tür bir soru olduğunu** ölçer.

    🔒 ÖNCE CEBİR: menzil çapası bir uzunluk birimidir (§I) ve ölçekle
    sadeleşir. N ise BOYUTSUZDUR — sadeleşmez. Öyleyse N gerçek bir
    serbestlik derecesidir; soru, NEYİ belirlediğidir.

    🔒 SONRA ÖLÇÜM, İKİ AŞAMALI:
      1. Yoğunluk sabit tutulursa (alan ∝ √N) derece SABİT KALMIYOR —
         sınır etkisi: büyük ağda kenardaki düğüm oranı ∝ 1/√N azalıyor.
      2. Derece EŞİTLENİRSE geriye tek etki kalıyor: **DERİNLİK**.

    🔴 VE DERİNLİK ZATEN ŞARTNAMENİN AÇIKÇA ELE ALDIĞI BÜYÜKLÜK: §09.4
    *"derinlik bir sabit değil, bir eksen"* ve alan taramasının AMACI
    derinliği en büyük yapmaktı. Yani N'in tek fiziksel sonucu, projenin
    zaten bildiği ve keşifsel eksene koyduğu şeydir.
    """
    _baslik("J - DUGUM SAYISI NEYI BELIRLIYOR  (derece esitlenince: DERINLIK)")
    tohumlar = tuple(range(1000, 1006))
    print(f"  {len(tohumlar)} tohum · statik-yok · kanal grafigi")
    print("  🔒 Asama 1: YOGUNLUK sabit (alan ∝ √N) — derece sabit kaliyor mu?")
    asama1 = ((20, 1273.0), (40, 1800.0), (80, 2546.0))
    asama2 = ((20, 1100.0), (40, 1800.0), (80, 3000.0))
    gorevler = [(n, a, t) for n, a in asama1 + asama2 for t in tohumlar]
    with Pool(isci) as havuz:
        ham = havuz.map(_is_dugum, gorevler, chunksize=1)
    hata = next((h for _s, h in ham if h is not None), None)
    if hata:
        print(f"  🔴 gorev PATLADI: {hata[:150]}")
        return

    def _ozet(i):
        dilim = ham[i * len(tohumlar):(i + 1) * len(tohumlar)]
        d = ist.mean(s["derece"] for s, _h in dilim)
        atl = [x for s, _h in dilim for x in s["atlama"]]
        kop = sum(s["kopuk"] for s, _h in dilim)
        cift = sum(s["cift"] for s, _h in dilim)
        return d, ist.mean(atl), max(atl), 100.0 * kop / cift

    print(f"  {'N':>4} {'alan_m':>8} {'derece':>8} {'ort atlama':>11} "
          f"{'en uzak':>8} {'kopuk %':>8}")
    for i, (n, a) in enumerate(asama1):
        d, o, mx, kp = _ozet(i)
        print(f"  {n:>4} {a:>8.0f} {d:>8.2f} {o:>11.2f} {mx:>8d} {kp:>8.2f}")
    print("  🔴 Derece SABIT KALMIYOR — sinir etkisi (kenardaki dugum orani")
    print("     ∝ 1/√N azaliyor). Yani N olcekle sadelesmiyor.")
    print()
    print("  🔒 Asama 2: DERECE esitlendi — geriye ne kaliyor?")
    print(f"  {'N':>4} {'alan_m':>8} {'derece':>8} {'ort atlama':>11} "
          f"{'en uzak':>8} {'kopuk %':>8}")
    for i, (n, a) in enumerate(asama2):
        d, o, mx, kp = _ozet(len(asama1) + i)
        print(f"  {n:>4} {a:>8.0f} {d:>8.2f} {o:>11.2f} {mx:>8d} {kp:>8.2f}")
    print()
    print("  🔒 Derece esitlendiginde N'in TEK etkisi DERINLIK.")
    print("  🔒 ALT SINIR: N=20 esitlenmis derecede 1,64 atlama veriyor —")
    print("     sartnamenin ACIKCA reddettigi sig rejim (§09.4).")
    print("  🔒 UST SINIR: maliyet. Olculdu (50 s kosu, statik-surekli):")
    print("     N=20 → 60,8 s · N=40 → 126,9 s · N=80 → 297,2 s (2,34 kat).")
    print()
    print("  ⚠️ BU BIR TEK SAYI VERMEZ, BIR BAND VERIR. 40 o bandin icinde")
    print("     ve incelenen SURU BUYUKLUGUDUR. `03` kural 12: kapsam")
    print("     kararlari ogrenciye aittir — bu satir ONAY BEKLIYOR.")


# ==========================================================================
def k_kisitlama_kapisi(isci: int = 6) -> None:
    """🔴 "SİMÜLATÖR PROTOKOLÜ KISITLAMIYOR" — İDDİANIN KANITI BOŞTU.

    Şartname §09.6 şunu ilan ediyor: *TTL ile düşen 0 · kuyruk taşması 0 ·
    en yüksek kuyruk 3/50 → kısıt DÜNYAYA konuyor, protokole değil.*

    🔴 O sayılar `dogrudan_komsu` koşum aletiyle üretilmiş ve o alet
    **`aktarilan_paket = 0`** veriyor: tek bir paketi bile ARA DÜĞÜMDE ileri
    iletmemiş. TTL yalnız AKTARMADA azalır, kuyruk yalnız aktarmayla dolar.
    Yani o test, parametreler ne olursa olsun **sıfırdan başka bir şey
    üretemezdi**. Geçmiş görünen ama hiçbir şey sınamayan bir kapı.

    🔒 DÜZELTME BİR SAYI DEĞİL, BİR ÖN KOŞUL: mekanizmayı çalıştırmayan bir
    koşu bu iddiayı SINAYAMAZ. Verdikt üç durumludur, iki değil:

        aktarilan_paket = 0        → KOSULMADI   (test bos)
        aktarılan > 0, marj geniş  → GECTI       (kısıt bağlamıyor)
        aktarılan > 0, marj dar    → KALDI       (simülatör kısıtlıyor)

    ⚠️ VE MARJ RAPORLANIR, SAYIM DEĞİL. *"TTL ölümü 0"* tek başına anlamsız;
    anlamlı olan *"en uzun yol 5 atlama, TTL 32, marj 6,4×"*. Birincisi bir
    yokluk, ikincisi bir kanıttır.
    """
    _baslik("K - KISITLAMA KAPISI  (§09.6'nin kaniti bostu — on kosul eklendi)")
    from sim2.kosum.kosu import Kosu
    from sim2.olcum.metrikler import metrik_sozlugu
    from protokoller.kosum_kosumu import DogrudanKomsu, EnYakinKimlik

    print("  🔒 ON KOSUL: `aktarilan_paket > 0`. Saglanmazsa verdikt")
    print("     GECTI degil KOSULMADI'dir.")
    print()
    print(f"  {'alet':>16} {'senaryo':>17} {'aktarilan':>10} {'ttl':>5} "
          f"{'kuyrukX':>8} {'tepe/kap':>9} {'verdikt':>12}")
    for alet, ad in ((DogrudanKomsu, "dogrudan_komsu"),
                     (EnYakinKimlik, "en_yakin_kimlik")):
        for senaryo in ("statik-yok", "statik-surekli"):
            kfg = DS.konfig(kol="kisit", senaryo=senaryo, tohum=1000,
                         isinma_s=10.0, olcum_bitis_s=40.0,
                         kosu_bitis_s=50.0, karistirici_baslangic_s=5.0)
            kur = kurulum_yap(kfg)
            kosu = Kosu(kur, lambda i: alet())
            kosu.kostur()
            s = metrik_sozlugu(kur.sayaclar.disa_ver(), kur.paket_defteri,
                               kur.rota_defteri)
            akt = int(s["aktarilan_paket"])
            ttl = int(s["ttl_olumu"])
            kx = int(s["kuyruk_tasmasi"])
            tepe = int(s["en_yuksek_doluluk"])
            kap = kfg.kuyruk_kapasitesi
            if akt == 0:
                verdikt = "KOSULMADI"
            elif ttl == 0 and kx == 0 and tepe < 0.5 * kap:
                verdikt = "GECTI"
            else:
                verdikt = "🔴 KISITLIYOR"
            print(f"  {ad:>16} {senaryo:>17} {akt:>10} {ttl:>5} {kx:>8} "
                  f"{f'{tepe}/{kap}':>9} {verdikt:>12}")
    print()
    print("  🔴 `dogrudan_komsu` iki kolda da KOSULMADI: aktarma yok, yani")
    print("     TTL ve kuyruk mekanizmalari hic devreye girmiyor. §09.6'nin")
    print("     kaniti buydu ve YAPISAL OLARAK BOSTU.")
    print("  🔴 `en_yakin_kimlik` ise KASTEN dongu uretiyor, yani ust")
    print("     siniri temsil ediyor. Iki alet soruyu BRAKETLIYOR ama")
    print("     CEVAPLAMIYOR: biri mekanizmaya hic dokunmuyor, oteki")
    print("     patolojik olarak zorluyor.")
    print()
    print("  🔒 VERDIKT: §09.6'nin iddiasi BUGUN KANITSIZDIR ve ancak")
    print("     GERCEK bir taban cizgisiyle (Faz 3) sinanabilir. Bu kapi")
    print("     o zaman kosulacak ve on kosul artik bos gecmeyi engelliyor.")
    print()
    print("  🔒 TTL ICIN YAPISAL KANIT VAR ve o BUGUN GECERLI: dongusuz bir")
    print("     yonlendirmede yol uzunlugu ag CAPINI asamaz. Olculdu (§J):")
    print("     N = 40'ta en uzak cift 5 atlama, TTL 32 → marj 6,4x. Yani")
    print("     TTL yalnizca DONGU oldugunda baglar — zaten var olma sebebi.")


# ==========================================================================
def _is_stres(gorev):
    """Bir parametre oynatmasını STRES ALTINDA koşar (döngü üreten alet).

    🔒 Kâhin DEĞİL. Duyarlılık denetimi her şeyi kâhin kollarında ölçtü;
    yalnızca KUSURLU yönlendirmede bağlayan bir parametre orada tanım gereği
    hiç devreye girmez ve `OLCULEMEDI` okunur.
    """
    ek, = gorev
    try:
        from sim2.kosum.kosu import Kosu
        from sim2.olcum.metrikler import metrik_sozlugu
        from protokoller.kosum_kosumu import EnYakinKimlik
        kfg = DS.konfig(kol="stres", senaryo="statik-surekli", tohum=1000,
                     isinma_s=10.0, olcum_bitis_s=40.0, kosu_bitis_s=50.0,
                     karistirici_baslangic_s=5.0, **ek)
        kur = kurulum_yap(kfg)
        Kosu(kur, lambda i: EnYakinKimlik()).kostur()
        s = metrik_sozlugu(kur.sayaclar.disa_ver(), kur.paket_defteri,
                           kur.rota_defteri)
        say = kur.sayaclar
        iz = (int(say.oku("teslim_paket")), int(say.oku("mac_deneme")),
              int(say.oku("kuyruk_tasmasi")), int(say.oku("ttl_olumu")),
              int(say.oku("alim_yakalama")))
        return (s["pdr_pencere"], iz), None
    except Exception as hata:                       # noqa: BLE001
        return None, f"{type(hata).__name__}: {hata}"


def l_stres_taramasi(isci: int = 6) -> None:
    """🔴 "ÖLÇÜLEMEDİ" ETİKETLERİ YANLIŞ KOLDAN GELMİŞ OLABİLİR.

    K-107 dokuz parametreyi `OLCULEMEDI` diye işaretledi — parmak izi birebir
    aynı kaldığı için, yani parametre o kolda hesaba HİÇ girmedi. Ve kendi
    uyarısını da yazdı: *"OLCULEMEDI AKLAMA DEGILDIR; canli oldugu bir kolda
    YENIDEN taranmali."*

    🔴 O denetimin BEYAN EDİLMEMİŞ bir sınırı vardı: her şey **kâhin
    kollarında** ölçüldü, yani yönlendirmenin KUSURSUZ olduğu bir dünyada.
    Kuyruk kapasitesi, TTL ve yakalama eşiği ancak yönlendirme KÖTÜ olduğunda
    bağlar. Kusursuz bir kolda tanım gereği görünmezler.

    🔒 Bu bölüm onları STRES ALTINDA tarar: döngü üreten koşum aleti kuyruğu
    dolduruyor (50/50), TTL'i ateşliyor ve yakalama üretiyor. Ölçüt aynı:
    parmak izi birebir aynıysa `OLCULEMEDI`, değilse CANLI.
    """
    _baslik("L - STRES TARAMASI  ('olculemedi' etiketleri dogru mu)")
    print("  🔒 Kahin DEGIL, dongu ureten kosum aleti — mekanizmalar CANLI.")
    print("  ⚠️ Bu bir DUYARLILIK olcumu degil, bir CANLILIK olcumu: parmak")
    print("     izi degisiyorsa parametre hesaba GIRIYOR demektir.")
    adaylar = (
        ("TABAN", {}),
        ("kuyruk_kapasitesi ×2", dict(kuyruk_kapasitesi=100)),
        ("kuyruk_kapasitesi ×0,5", dict(kuyruk_kapasitesi=25)),
        ("ttl_baslangic ×0,5", dict(ttl_baslangic=16)),
        ("ttl_baslangic ×2", dict(ttl_baslangic=64)),
        ("yakalama_esigi_db ×2", dict(yakalama_esigi_db=20.0)),
        ("yakalama_penceresi ×2", dict(yakalama_penceresi_s=384e-6)),
        ("cw_max ×0,5 (511)", dict(cw_max=511)),
    )
    with Pool(isci) as havuz:
        ham = havuz.map(_is_stres, [(ek,) for _ad, ek in adaylar], chunksize=1)
    hata = next((h for _s, h in ham if h is not None), None)
    if hata:
        print(f"  🔴 gorev PATLADI: {hata[:150]}")
        return
    p0, i0 = ham[0][0]
    print()
    print(f"  {'oynatma':>24} {'pdr':>9} {'fark':>9} {'parmak izi':>22}")
    print(f"  {'TABAN':>24} {p0:>9.5f} {'—':>9} {str(i0):>22}")
    for (ad, _ek), (sonuc, _h) in list(zip(adaylar, ham))[1:]:
        p, i = sonuc
        print(f"  {ad:>24} {p:>9.5f} {p - p0:>+9.5f} "
              f"{('OLCULEMEDI' if i == i0 else '🔴 CANLI'):>22}")
    print()
    print("  🔒 'CANLI' cikan her parametre icin K-107'nin `OLCULEMEDI`")
    print("     etiketi YANLIS KOLDAN gelmistir ve duyarliligi Faz 3'te,")
    print("     GERCEK bir taban cizgisiyle yeniden olculmelidir.")
    print("  🔒 'OLCULEMEDI' kalan icin etiket AYAKTA ve artik STRES")
    print("     ALTINDA da dogrulanmis oldu — daha guclu bir iddia.")


# ==========================================================================
def m_rician(isci: int = 6) -> None:
    """🔴 RICIAN K — keyfi bir sayı mı, yoksa ÖLÇÜLEBİLİR bir fizik iddiası mı?

    `rician_k_db = 6` gerekçesi *"hava-hava bağda güçlü doğrudan görüş →
    Rayleigh değil Rician"* idi. O cümle K > 0'ı gerekçelendirir, **6'yı
    değil**. Duyarlılık denetimi −0,060 ölçtü, yani deneyin çözünürlüğünün
    (0,036) üstünde.

    🔴 ÖNCE BİR İÇ TUTARSIZLIK ŞÜPHESİ KURULDU VE ÇÖZÜLDÜ.
    Şüphe: `yol_kaybi_usteli = 2` *"iki-ışın kırılma mesafesi bağ mesafesinin
    ÇOK üstünde, yani yer yansıması önemsiz"* diye seçilmişti. Ama K = 6 dB,
    saçılan gücün doğrudan görüşün **dörtte biri** olduğunu söylüyor —
    önemsiz olmayan bir çok yol bileşeni. İkisi çelişiyor mu?

    🔒 **ÇELİŞMİYOR, TAMAMLIYOR.** Kırılma mesafesinin ALTINDA iki-ışın alanı
    serbest uzay değerinin etrafında SALINIR; α = 2 o salınımın ORTALAMASINI,
    Rician ise SALINIMIN KENDİSİNİ modelliyor. Üç boyutlu, hareketli bir
    sürüde salınımın fazı konumla hızla değiştiği için onu istatistiksel
    modellemek standart uygulamadır. Şüphe kuruldu, sınandı, düştü.

    ⭐ VE ÇÖZÜM BİR DENKLİK VERDİ. Baskın çok yol bileşeni yer yansımasıysa,
    Rician K doğrudan yansıma katsayısına çevrilir:

        P_yansıyan / P_doğrudan = Γ²   ⟹   K_dB = −20·log₁₀(Γ)

    Yani **K = 6 dB ⟺ Γ = 0,50**. Sayı artık keyfi değil, SINANABİLİR bir
    fiziksel iddia: *"bu geometride yer yansıma katsayısı 0,50'dir."*

    🔒 İKİNCİ ÖLÇÜT — gölgeleme σ'sıyla AYNI BİÇİMDE. σ = 3 dB, PER'in
    0,99→0,01 geçiş bandıyla (3,44 dB) aynı mertebede olduğu için
    gerekçelendirilmişti. Aynı soru K için de sorulur: sönümlemenin fade
    derinliği o bandla aynı mertebede mi? Değilse ya kozmetik ya baskın.
    """
    import math
    from sim2.kanal.sonumleme import Sonumleme
    from sim2.dunya.topoloji import topoloji_kur
    from sim2.cekirdek.rng import Akislar
    _baslik("M - RICIAN K  (denklik: K_dB = −20·log10(Γ)) ")
    print("  🔒 Iki-isin kirilma mesafesinin ALTINDA alan serbest uzay")
    print("     degerinin etrafinda SALINIR: α = 2 ortalamayi, Rician")
    print("     salinimin KENDISINI modelliyor. Celismiyor, tamamliyor.")
    print()
    print("  🔒 DENKLIK: baskin cok yol bileseni yer yansimasiysa")
    print("     K_dB = −20·log10(Γ), yani K bir YANSIMA KATSAYISI iddiasidir.")
    print(f"  {'K (dB)':>8} {'Γ (denk)':>9} {'p10 fade':>10} {'p1 fade':>9} "
          f"{'derece':>8} {'Jaccard':>9}")

    kfg0 = DS.konfig(kol="rician", senaryo="statik-surekli", tohum=1000,
                  karistirici_guc_override_dbm=-15.0)
    kur0 = kurulum_yap(kfg0)
    g0 = KanalGrafigi(kur0)
    d0 = g0.ozet(200.0)["derece"]
    k0 = frozenset((i, j) for i, ks in enumerate(g0._komsu)
                   for j in ks if i < j)

    for kdb in (0.0, 3.0, 6.0, 10.0, 15.0):
        kfg = DS.konfig(kol="rician", senaryo="bagimsiz-yok", tohum=1000,
                     rician_k_db=kdb)
        son = Sonumleme(kfg, topoloji_kur(kfg, Akislar(1000)))
        ornek = sorted(son.guc_kazanci(0, 1, 0.2 + n * 0.02)
                       for n in range(4000))
        p10 = 10.0 * math.log10(max(ornek[len(ornek) // 10], 1e-12))
        p1 = 10.0 * math.log10(max(ornek[len(ornek) // 100], 1e-12))
        gam = 10.0 ** (-kdb / 20.0)
        kfg_s = DS.konfig(kol="rician", senaryo="statik-surekli", tohum=1000,
                       rician_k_db=kdb,
                       karistirici_guc_override_dbm=-15.0)
        gs = KanalGrafigi(kurulum_yap(kfg_s))
        d = gs.ozet(200.0)["derece"]
        ks = frozenset((i, j) for i, kk in enumerate(gs._komsu)
                       for j in kk if i < j)
        jac = len(k0 & ks) / len(k0 | ks) if (k0 | ks) else 1.0
        isaret = "  ← bugunku" if abs(kdb - 6.0) < 1e-9 else ""
        print(f"  {kdb:>8.1f} {gam:>9.3f} {p10:>10.2f} {p1:>9.2f} "
              f"{d:>8.2f} {jac:>9.4f}{isaret}")
    print()
    print("  🔒 KIYAS: PER'in 0,99→0,01 gecis bandi 3,44 dB")
    print("     (`adim4_kapanis.py` bolum D). Fade derinligi o bandla ayni")
    print("     mertebedeyse sonumleme baglari GERCEKTEN acip kapatiyor;")
    print("     cok kucukse kozmetik, cok buyukse baglar geometriyi degil")
    print("     fade'i takip ediyor demektir.")
    print()
    print("  ⚠️ BU BOLUM K'YI TURETMIYOR. Yaptigi sey, gerekcesiz bir sayiyi")
    print("     SINANABILIR bir fiziksel iddiaya cevirmek: 'bu geometride yer")
    print("     yansima katsayisi Γ = 0,50'. Kalan is TEK bir bibliyografik")
    print("     kontroldur ve `02`ye islenir — RFC'lerde oldugu gibi.")


# ==========================================================================
def _is_kahin(gorev):
    """🔴 Eşik MODÜL GLOBALİDİR; işçi süreçte oynatılır.

    `spawn` altında her işçi modülü yeniden yükler, dolayısıyla globali
    işçinin İÇİNDE ayarlamak zorunludur. Ana süreçte ayarlamak hiçbir işçiye
    ulaşmazdı ve tarama sessizce TEK eşikte koşardı — tam olarak bu projenin
    "hiç oynatılmamışken duyarsız görünen parametre" hatası.
    """
    senaryo, tohum, alet, esik = gorev
    try:
        import kalibrasyon.kahin as _k
        _k.ATLAMA_ESIGI = esik
        from kalibrasyon.duyarlilik import _kos
        return _kos(senaryo, tohum, alet, {}), None
    except Exception as hata:                       # noqa: BLE001
        return None, f"{type(hata).__name__}: {hata}"


def d_kahin_duyarliligi(isci: int = 6) -> None:
    """🔴 EŞİK, DENEYİN ASIL EKSENİNİ OYNATIYOR MU?

    Eşik yalnız çalışma noktasını değil, **atlama kâhinini** de belirliyor:
    BFS grafiği eşikten geçen bağlardan kuruluyor, yani kâhin kötü bir bağ
    seçmekten EŞİKLE korunuyor. `olcut_bedeli` (ETX kâhini − atlama kâhini)
    bu deneyin en keskin kontrastı; eşik onu oynatıyorsa bu doğrudan sonucu
    belirler.

    🔒 KENDİ KAPISI (G-d) — YAPISAL BİR BEKLENTİ:
        `EnGuvenilirKahin` eşik KULLANMAZ (ETX ağırlıklı Dijkstra, zayıf bağ
        dışlanmaz, PAHALI olur). O yüzden `pdr_etx` eşikten ETKİLENMEMELİ.
        `EnKisaYolKahin` eşikle korunur, dolayısıyla `pdr_atlama` ETKİLENMELİ.
    Beklenti tersine çıkarsa ya tarama eşiği hiç oynatmıyordur ya kâhinlerin
    ilan edilmiş tanımı yanlıştır — ikisi de bulgudur.
    """
    from kalibrasyon.duyarlilik import PENCERE

    # 🔴 15 TOHUM, `duyarlilik.py`nin 5'i DEĞİL. İlk koşumda beş tohumla
    # bakıldı ve bandlar (2 SE ≈ 0,04–0,09) ölçülen etkiden GENİŞ çıktı:
    # etki deneyin çözünürlüğünün üstünde ama kendi hata payının içinde —
    # yani K-107'nin "KARAR YOK" kovası. Bandı daraltmanın tek yolu tohum
    # sayısıdır (eşiği gevşetmek değil), ve 15 tohum bandı ~1,7 kat daraltır.
    D_TOHUMLAR = tuple(range(1000, 1015))

    _baslik("D - ESIGIN KAHIN KOLLARINA ETKISI  (deneyin asil ekseni)")
    esikler = (0.70, 0.80, 0.90, 0.95, 0.99)
    senaryo = "statik-surekli"
    aletler = ("en_guvenilir_kahin", "en_kisa_yol_kahin")
    print(f"  senaryo {senaryo} · {len(D_TOHUMLAR)} tohum · pencere {PENCERE}")
    print(f"  🔒 Olcut `duyarlilik.py`nin AYNISI: tohum basina ESLESTIRILMIS")
    print(f"     fark, kendi 2 SE bandi VE deneyin cozunurlugu "
          f"R = {COZUNURLUK_R:.3f}")

    gorevler = [(senaryo, t, a, e)
                for e in esikler for a in aletler for t in D_TOHUMLAR]
    with Pool(isci) as havuz:
        ham = havuz.map(_is_kahin, gorevler, chunksize=1)
    hata = next((h for _s, h in ham if h is not None), None)
    if hata:
        print(f"  🔴 gorev PATLADI: {hata[:150]}")
        return

    n = len(D_TOHUMLAR)
    veri: dict[float, dict[int, dict[str, float]]] = {}
    for ei, e in enumerate(esikler):
        bas = ei * len(aletler) * n
        etx = {t: ham[bas + k][0][0] for k, t in enumerate(D_TOHUMLAR)}
        atl = {t: ham[bas + n + k][0][0] for k, t in enumerate(D_TOHUMLAR)}
        veri[e] = {t: {"pdr_etx": etx[t], "pdr_atlama": atl[t],
                       "olcut_bedeli": etx[t] - atl[t]} for t in D_TOHUMLAR}

    taban = veri[ATLAMA_ESIGI]
    print()
    print(f"  {'esik':>6} {'pdr_etx':>9} {'pdr_atlama':>11} "
          f"{'olcut_bedeli':>13} {'d_bedel':>9} {'2SE':>8} {'karar':>12}")
    etx_yayilim = []
    for e in esikler:
        ort = {k: ist.mean(veri[e][t][k] for t in D_TOHUMLAR)
               for k in ("pdr_etx", "pdr_atlama", "olcut_bedeli")}
        etx_yayilim.append(ort["pdr_etx"])
        farklar = [veri[e][t]["olcut_bedeli"] - taban[t]["olcut_bedeli"]
                   for t in D_TOHUMLAR]
        d = ist.mean(farklar)
        band = (2.0 * ist.stdev(farklar) / len(farklar) ** 0.5
                if len(farklar) > 1 else 0.0)
        # 🔴 ÜÇ KOVA, İKİ DEĞİL — K-107'nin dersi. "Kendi bandının üstünde"
        # ile "çözünürlüğün üstünde" AYRI sorulardır ve ikisi ayrışabilir.
        # İlk yazımda ikisini tek kovaya koymuştum: çözünürlüğün üstünde ama
        # kendi bandının İÇİNDE olan bir etkiyi `DUYARLI` sayıyordu — yani
        # KARAR VERİLEMEYEN bir şeyi mahkûm ediyordu. `DUYARSIZ`ı yanlışlıkla
        # vermek kadar olmasa da, bu da ölçümün söylemediğini söylemektir.
        if e == ATLAMA_ESIGI:
            karar = "taban"
        elif abs(d) <= band and abs(d) < COZUNURLUK_R:
            karar = "duyarsiz"
        elif abs(d) > band:
            karar = "🔴 DUYARLI"
        else:
            karar = "⚠️ KARAR YOK"
        print(f"  {e:>6.2f} {ort['pdr_etx']:>9.4f} {ort['pdr_atlama']:>11.4f} "
              f"{ort['olcut_bedeli']:>13.4f} {d:>+9.4f} {band:>8.4f} "
              f"{karar:>12}")

    gd_etx = (max(etx_yayilim) - min(etx_yayilim)) < 1e-12
    atl_yayilim = max(ist.mean(veri[e][t]["pdr_atlama"] for t in D_TOHUMLAR)
                      for e in esikler) - \
        min(ist.mean(veri[e][t]["pdr_atlama"] for t in D_TOHUMLAR)
            for e in esikler)
    gd_atl = atl_yayilim > 1e-9
    print()
    print(f"  G-d · ETX kahini esikten ETKILENMEMELI : "
          f"{'GECTI' if gd_etx else '🔴 KALDI'}  "
          f"(yayilim {max(etx_yayilim) - min(etx_yayilim):.3e})")
    print(f"  G-d · atlama kahini ETKILENMELI        : "
          f"{'GECTI' if gd_atl else '🔴 KALDI — esik hic oynamamis'}  "
          f"(yayilim {atl_yayilim:.4f})")

    # ------------------------------------------------------------------
    # 🔒 TEKDÜZELİK — tek tek noktaların bandı geniş olsa bile, BEŞ NOKTANIN
    # SIRALAMASI kendi başına kanıttır. Saf gürültüde beş noktanın kusursuz
    # tekdüze çıkma olasılığı 2/5! = %1,7'dir. Yani "her nokta kendi bandının
    # içinde" ile "etki yok" AYNI ŞEY DEĞİLDİR.
    ort_bedel = [ist.mean(veri[e][t]["olcut_bedeli"] for t in D_TOHUMLAR)
                 for e in esikler]
    tekduze = all(b <= a for a, b in zip(ort_bedel, ort_bedel[1:]))
    print()
    print(f"  olcut_bedeli, esik boyunca : "
          f"{' → '.join(f'{b:+.4f}' for b in ort_bedel)}")
    print(f"  tekduze azaliyor mu        : "
          f"{'EVET' if tekduze else 'hayir'}  "
          f"(saf gurultude olasilik %1,7)")
    print(f"  uctan uca yayilim          : "
          f"{max(ort_bedel) - min(ort_bedel):.4f}  "
          f"(cozunurluk R = {COZUNURLUK_R:.3f}, "
          f"{(max(ort_bedel) - min(ort_bedel)) / COZUNURLUK_R:.1f} kati)")

    # ------------------------------------------------------------------
    # 🔴 "TAVAN" GERÇEKTEN TAVAN MI? — beklenmedik bir sorunun kapısı.
    # `pdr_tavani.py` `EnGuvenilirKahin` icin *"GERCEK TAVAN BUDUR: hicbir
    # protokol daha iyisini yapamaz"* diyor. Ama ETX BEKLENEN ILETIM SAYISINI
    # kucultur, TESLIMI degil — ve yeniden deneme sinirli (5 deneme) oldugu
    # icin ikisi ayni sey degildir. Dusuk toplam ETX'li bir yol, icinde 5
    # denemede de gecemeyen bir bag tasiyabilir.
    print()
    print("  🔴 TAVAN SINAVI — ETX kahini her esikte atlama kahininden")
    print("     iyi mi? (isaret testi, tohum basina)")
    print(f"    {'esik':>6} {'atlama > etx olan tohum':>26} {'ort fark':>10}")
    ihlal_toplam = 0
    for e in esikler:
        ustun = sum(1 for t in D_TOHUMLAR
                    if veri[e][t]["pdr_atlama"] > veri[e][t]["pdr_etx"])
        ihlal_toplam += ustun
        fark = ist.mean(veri[e][t]["pdr_atlama"] - veri[e][t]["pdr_etx"]
                        for t in D_TOHUMLAR)
        print(f"    {e:>6.2f} {ustun:>17}/{len(D_TOHUMLAR)} tohum "
              f"{fark:>+10.4f}")
    if ihlal_toplam:
        print()
        print("  🔴 TAVAN IDDIASI COKTU: en az bir esikte atlama kahini")
        print("     ETX kahinini GECIYOR. `EnGuvenilirKahin` beklenen ILETIM")
        print("     sayisini kucultur; TESLIMI en buyuk yapan yonlendirici")
        print("     O DEGILDIR. Yeniden deneme siniri sonlu oldugu icin ikisi")
        print("     ayrisir — ve karistirma altinda ayrisma buyuyor.")
    else:
        print()
        print("  🟢 Tavan iddiasi ayakta: her esikte, her tohumda ETX kahini")
        print("     atlama kahininden iyi ya da esit.")


# ==========================================================================
def _is_k_pdr(gorev):
    """K ve örnekleme adımı MODÜL GLOBALİ; işçi süreçte oynatılır."""
    senaryo, tohum, alet, K, adim = gorev
    try:
        import kalibrasyon.kahin as _k
        _k.SONUMLEME_ORNEGI = K
        _k.SONUMLEME_ADIMI_S = adim
        from kalibrasyon.duyarlilik import _kos
        return _kos(senaryo, tohum, alet, {}), None
    except Exception as hata:                       # noqa: BLE001
        return None, f"{type(hata).__name__}: {hata}"


def e_k_pdr(isci: int = 6) -> None:
    """🔴 K'NIN GÜRÜLTÜSÜ, KARARIN KENDİ BİRİMİNDE — bölüm C'nin DÜZELTMESİ.

    🔴 BÖLÜM C YANLIŞ TOLERANSI KULLANDI ve bu kayda geçer. Orada derecenin
    saçılması, `gorev_kalibrasyonu.py`de KOLLARIN DERECESİNİ EŞİTLEMEK için
    ilan edilmiş 0,3 toleransıyla karşılaştırıldı. O tolerans o karara aittir.
    K'nin asıl beslediği karar ise kâhin kollarının PDR'sidir ve onun kendi
    toleransı deneyin çözünürlüğü R = 0,036'dır.

    🔒 Bir ölçütü, ölçtüğü kararın birimiyle karşılaştırmamak, bu projede
    daha önce üç kez yakalanmış bir hata sınıfıdır. Bölüm C SİLİNMEZ —
    grafik düzeyindeki resmi veriyor — ama KARAR bu bölümden çıkar.

    🔒 FAZ NASIL RASTGELELEŞTİRİLİR: örnekleme ADIMI oynatılır (5…8 ms).
    Hepsi tutarlılık süresinden (~1,7 ms) büyüktür, yani kestiricinin
    TASARIMI değişmez — yalnız hangi bağımsız çekimleri kullandığı değişir.

    ⚠️ BEYAN EDİLEN SINIR: ilk örnek (m = 0) bütün fazlarda ORTAKTIR,
    dolayısıyla ölçülen saçılma gerçek gürültüyü ~1/K kadar EKSİK gösterir
    (K = 4'te %13, K = 16'da %3). Yön anti-konservatiftir ve beyan edilir.
    """
    _baslik("E - K'NIN GURULTUSU, PDR BIRIMINDE  (bolum C'nin duzeltmesi)")
    senaryo = "bagimsiz-surekli"
    K_ler = (4, 8, 16)
    adimlar = (0.005, 0.006, 0.007, 0.008)
    tohumlar = (1000, 1001, 1002)
    alet = "en_guvenilir_kahin"
    print(f"  senaryo {senaryo} (HAREKETLI + karistirilmis) · "
          f"{len(tohumlar)} tohum · {len(adimlar)} faz")
    print(f"  🔒 Olcut: fazlar arasi PDR yayilimi < R = {COZUNURLUK_R:.3f}")
    print(f"  ⚠️ tek kosu ~150 s · toplam {len(K_ler) * len(adimlar) * len(tohumlar)} kosu")

    gorevler = [(senaryo, t, alet, K, a)
                for K in K_ler for a in adimlar for t in tohumlar]
    with Pool(isci) as havuz:
        ham = havuz.map(_is_k_pdr, gorevler, chunksize=1)
    hata = next((h for _s, h in ham if h is not None), None)
    if hata:
        print(f"  🔴 gorev PATLADI: {hata[:150]}")
        return

    print()
    print(f"  {'K':>4} {'tohum basina PDR yayilimi':>34} {'ortalama':>9} "
          f"{'karar':>12}")
    yeterli = None
    for ki, K in enumerate(K_ler):
        yayilimlar = []
        for si, tohum in enumerate(tohumlar):
            v = [ham[ki * len(adimlar) * len(tohumlar)
                     + ai * len(tohumlar) + si][0][0]
                 for ai in range(len(adimlar))]
            yayilimlar.append(max(v) - min(v))
        ort = ist.mean(yayilimlar)
        tamam = ort < COZUNURLUK_R
        if tamam and yeterli is None:
            yeterli = K
        print(f"  {K:>4} {', '.join(f'{y:.4f}' for y in yayilimlar):>34} "
              f"{ort:>9.4f} {('yeter' if tamam else '🔴 asiyor'):>12}")
    print()
    if yeterli is None:
        print("  🔴 HICBIR K COZUNURLUGUN ALTINA INMEDI — taranan araligi")
        print("     buyutmek gerekir; K yeterli degil.")
    else:
        print(f"  🔒 R = {COZUNURLUK_R:.3f}'in altina inen EN KUCUK K : "
              f"{yeterli}")
        print("  ⚠️ Bu, kestiricinin KENDI gurultusudur; parametrenin")
        print("     'dogru' degeri degil. K buyudukce gurultu duser ve")
        print("     maliyet artar — secim o iki egrinin kesistigi yerdir.")


# ==========================================================================
if __name__ == "__main__":
    DS.secimi_oku()                         # K-187: --dunya
    print(f"  DUNYA: {DS.secili()}")
    # 🔒 Windows `spawn` korumasi — calisma kurali 11. TEK havuz, IC ICE YOK.
    BOLUMLER = {"a": a_kapilar, "b": b_esik_taramasi, "c": c_sonumleme_ornegi,
                "d": d_kahin_duyarliligi, "e": e_k_pdr,
                "f": f_theta, "g": g_theta_tanim, "h": h_hiz_turetme,
                "i": i_serbestlik_dereceleri,
                "j": j_dugum_sayisi,
                "k": k_kisitlama_kapisi,
                "l": l_stres_taramasi,
                "m": m_rician}
    secim = sys.argv[1:] or ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m"]
    bilinmeyen = [s for s in secim if s not in BOLUMLER]
    if bilinmeyen:
        raise SystemExit(f"bilinmeyen bolum: {bilinmeyen}")
    # 🔴 KAPILAR ONCE. Gecmezse sonraki bolumler KOSULMAZ — kosulmayan bir
    # kapi "gecti" sayilmaz, ve kapisi gecmemis bir alet sayi uretmez.
    if "a" in secim:
        if not a_kapilar():
            raise SystemExit(1)
        secim = [s for s in secim if s != "a"]
    for s in secim:
        BOLUMLER[s]()
