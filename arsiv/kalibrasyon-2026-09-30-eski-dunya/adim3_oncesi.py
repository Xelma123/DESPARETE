"""ADIM 3 ÖNCESİ ÇALIŞMA NOKTASI ÖLÇÜMÜ.

Üretici:  PYTHONIOENCODING=utf-8 python kalibrasyon/adim3_oncesi.py

Bu betik, `Konfig` parametreleri kararlaştırılmadan ÖNCE bilinmesi gereken
her sayıyı üretir. Hiçbiri elle yazılmadı.

Ölçülenler
----------
A. Çalışma noktası (derece · bağlı oran) — 500 tohum + tohum sayısına duyarlılık
B. Atlama sayısı dağılımı ve ondan türeyen KANAL YÜKÜ
C. Kusur 1'in (iki PER tanımı) yeni parametrelerdeki büyüklüğü
D. PER geçiş bandının genişliği — gölgeleme sigmasıyla karşılaştırma
E. Düğüm verici gücü ve karıştırıcının eski çalışma noktasının karşılığı
"""
from __future__ import annotations

import collections
import math
import pathlib
import statistics as ist
import sys

KOK = pathlib.Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.cekirdek.rng import Akislar  # noqa: E402
from sim2.dunya.geometri import Nokta3, mesafe  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402

# ⚠️ AŞAĞIDAKİ SABİTLER TARİHSELDİR — 4 Eylül 2026'nın ADAY değerleridir.
# `Konfig` daha yokken, hangi değerlerin seçileceğine karar vermek için
# koşulmuştu. Bu yüzden `Konfig`den okunmazlar: okunsalardı betik artık
# o günkü ölçümü değil, bugünkü çalışma noktasını ölçerdi.
#
# 🔴 AMA BAYATLADILAR ve bunu SESSİZ bırakmak, ikinci bir doğru kaynağı
# tutmakla aynı şey olurdu. `bayatlik_raporu()` her koşumda hangi sabitin
# güncel `Konfig`den ayrıştığını yazar.

# 🔒 SÖZLEŞME BEYANI — mimari denetimi D14 bunu arar.
# Fiziğin kopyasını tutan bir modül, bunu açıkça beyan etmek ve her koşumda
# bayatlığını raporlamak zorundadır. Kopya meşru (tarihsel bir ölçümü yeniden
# üretmek için gerekli); SESSİZ kalması meşru değil.
TARIHSEL_FIZIK = True

# --- çalışma noktası adayı -------------------------------------------------
N, R = 40, 280.0
EN = BOY = 1000.0
YUKSEKLIK = 120.0

# --- fiziksel katman adayı (literatür hizalaması) --------------------------
BIT_HIZI = 2e6
PAKET_BAYT = 512
ONBELGE_S = 192e-6
BANT_HZ = 2e6
FREKANS_HZ = 2.4e9
YOL_KAYBI_USTELI = 3.0
SINR_ESIGI_DB = 10.0
GURULTU_FIGURU_DB = 6.0
SICAKLIK_K = 290.0
SLOT_S, SIFS_S, CW_MIN = 20e-6, 10e-6, 31
ONAY_BAYT, BEACON_BAYT = 14, 32

BOLTZMANN = 1.380649e-23
ISIK_HIZI = 299792458.0


# ==========================================================================
# Yerleşim ve graf
# ==========================================================================
def yerlesim(n, tohum, en, boy, zmin, zmaks):
    a = Akislar(tohum)
    return [Nokta3(a["yerlesim"].uniform(0.0, en),
                   a["yerlesim"].uniform(0.0, boy),
                   a["irtifa"].uniform(zmin, zmaks)) for _ in range(n)]


def komsuluk(p, r=R):
    n = len(p)
    return [[j for j in range(n) if j != i and mesafe(p[i], p[j]) <= r]
            for i in range(n)]


def bilesenler(kom):
    n = len(kom)
    gorulen, cikti = [False] * n, []
    for s in range(n):
        if gorulen[s]:
            continue
        yigin, say = [s], 0
        gorulen[s] = True
        while yigin:
            u = yigin.pop()
            say += 1
            for v in kom[u]:
                if not gorulen[v]:
                    gorulen[v] = True
                    yigin.append(v)
        cikti.append(say)
    return cikti


def bfs(kom, s):
    d = {s: 0}
    kuyruk = collections.deque([s])
    while kuyruk:
        u = kuyruk.popleft()
        for v in kom[u]:
            if v not in d:
                d[v] = d[u] + 1
                kuyruk.append(v)
    return d


def calisma_noktasi(en, boy, zmin, zmaks, tohumlar, r=R, n=N):
    dereceler, bagli, en_buyuk = [], 0, []
    for t in tohumlar:
        kom = komsuluk(yerlesim(n, t, en, boy, zmin, zmaks), r)
        dereceler.append(sum(len(k) for k in kom) / n)
        c = bilesenler(kom)
        bagli += (len(c) == 1)
        en_buyuk.append(max(c))
    sayi = len(tohumlar)
    p = bagli / sayi
    return dict(derece=ist.mean(dereceler),
                derece_se=ist.stdev(dereceler) / math.sqrt(sayi),
                bagli=p, bagli_se=math.sqrt(p * (1 - p) / sayi),
                en_buyuk=ist.mean(en_buyuk))


# ==========================================================================
# Radyo — kapalı formlar
# ==========================================================================
def dbm(w):
    return 10.0 * math.log10(w * 1000.0)


def yol_kaybi_db(d, ustel=YOL_KAYBI_USTELI, f=FREKANS_HZ):
    """PL(d) = PL(1 m) + 10*alfa*log10(d),  PL(1 m) = 20*log10(4*pi*f/c)."""
    ref = 20.0 * math.log10(4.0 * math.pi * 1.0 * f / ISIK_HIZI)
    return ref + 10.0 * ustel * math.log10(max(d, 1.0))


def gurultu_w(bant_hz):
    """N = k*T*B*F."""
    return (BOLTZMANN * SICAKLIK_K * bant_hz
            * 10.0 ** (GURULTU_FIGURU_DB / 10.0))


def verici_gucu_dbm(bant_hz, menzil=R):
    """Pt, MENZİL TANIMINDAN türetilir: menzilde SINR tam olarak esige esit."""
    hedef_alinan = gurultu_w(bant_hz) * 10.0 ** (SINR_ESIGI_DB / 10.0)
    return dbm(hedef_alinan * 10.0 ** (yol_kaybi_db(menzil) / 10.0))


def per_dbpsk(sinr_lin, bit):
    """PER = 1 - (1 - BER)^bit,  BER = 0,5*e^(-gama)  (esevresiz DBPSK)."""
    ber = 0.5 * math.exp(-sinr_lin)
    if ber >= 0.5:
        return 1.0
    return -math.expm1(bit * math.log1p(-ber))


def sinr_icin_db(hedef_per, bit):
    alt, ust = 0.05, 200.0
    for _ in range(300):
        orta = (alt + ust) / 2.0
        if per_dbpsk(orta, bit) > hedef_per:
            alt = orta
        else:
            ust = orta
    return 10.0 * math.log10(alt)


# ==========================================================================
def bolum_a():
    print("=" * 74)
    print("A - CALISMA NOKTASI (500 tohum)")
    print("=" * 74)
    print(f"{'kurulum':33s} {'ort. derece':>15s} {'bagli oran':>15s} {'en buyuk':>10s}")
    kurulumlar = (
        ("2B 1000x1000 (ESKI)",             (EN, BOY, 0.0, 0.0)),
        ("3B 1000x1000x300",                (EN, BOY, 0.0, 300.0)),
        ("3B 1000x1000x120  irtifa 0-120",  (EN, BOY, 0.0, 120.0)),
        ("3B 1000x1000x120  irtifa 20-120", (EN, BOY, 20.0, 120.0)),
        ("3B 1000x1000x120  irtifa 40-120", (EN, BOY, 40.0, 120.0)),
    )
    for ad, (en, boy, zmin, zmaks) in kurulumlar:
        s = calisma_noktasi(en, boy, zmin, zmaks, range(1, 501))
        print(f"{ad:33s} {s['derece']:9.3f}+-{s['derece_se']:.3f}"
              f" {100 * s['bagli']:9.1f}%+-{100 * s['bagli_se']:.1f}"
              f" {s['en_buyuk']:10.2f}")
    print()
    print("Tohum sayisina duyarlilik (3B 120 m, irtifa 0-120):")
    for sayi in (30, 60, 120, 250, 500):
        s = calisma_noktasi(EN, BOY, 0.0, 120.0, range(1, sayi + 1))
        print(f"  {sayi:4d} tohum : derece {s['derece']:.3f}+-{s['derece_se']:.3f}"
              f" . bagli %{100 * s['bagli']:.1f}+-{100 * s['bagli_se']:.1f}")


def bolum_b():
    print()
    print("=" * 74)
    print("B - ATLAMA SAYISI ve KANAL YUKU (30 tohum)")
    print("=" * 74)
    atlamalar, ulasilir = [], []
    for t in range(1, 31):
        kom = komsuluk(yerlesim(N, t, EN, BOY, 0.0, YUKSEKLIK))
        for s in range(N):
            d = bfs(kom, s)
            ulasilir.append((len(d) - 1) / (N - 1))
            atlamalar.extend(h for hedef, h in d.items() if hedef != s)
    ort_atlama = ist.mean(atlamalar)
    sirali = sorted(atlamalar)
    print(f"ulasilabilir cift : %{100 * ist.mean(ulasilir):.1f}")
    print(f"atlama ortalamasi : {ort_atlama:.3f}   (ortanca "
          f"{ist.median(atlamalar):.0f} . p95 {sirali[int(0.95 * len(sirali))]})")

    difs = SIFS_S + 2 * SLOT_S
    geri = (CW_MIN / 2.0) * SLOT_S
    veri_s = ONBELGE_S + PAKET_BAYT * 8 / BIT_HIZI
    onay_s = ONBELGE_S + ONAY_BAYT * 8 / BIT_HIZI
    beacon_s = ONBELGE_S + BEACON_BAYT * 8 / BIT_HIZI
    tur_s = difs + geri + veri_s + SIFS_S + onay_s
    print(f"veri cercevesi {veri_s * 1e6:.0f} us . onay {onay_s * 1e6:.0f} us"
          f" . basarili tur {tur_s * 1e6:.0f} us")
    beacon_yuk = N * 1.0 * (difs + geri + beacon_s)
    for akis in (10, 15):
        havada = akis * 4 * ort_atlama * tur_s
        print(f"  {akis:2d} akis x 4 pkt/s -> {akis * 4 * ort_atlama:5.0f} iletim/s"
              f" . veri %{100 * havada:.1f} + beacon %{100 * beacon_yuk:.1f}"
              f" = TEK CARPISMA ALANININ %{100 * (havada + beacon_yuk):.1f}'i")
    eski_veri = 192e-6 + 1024 * 8 / 1e6
    eski_onay = 192e-6 + 14 * 8 / 1e6
    eski_tur = difs + geri + eski_veri + SIFS_S + eski_onay
    print(f"  ESKI (10 cift x 1 pkt/s x 1024 B @ 1 Mb/s) :"
          f" %{100 * 10 * ort_atlama * eski_tur:.1f}")


def bolum_c():
    print()
    print("=" * 74)
    print("C - KUSUR 1'IN BUYUKLUGU (iki PER tanimi)")
    print("=" * 74)
    for bayt, hiz in ((1024, 1e6), (PAKET_BAYT, BIT_HIZI)):
        yalniz = 8 * bayt
        esdeger = 8 * bayt + ONBELGE_S * hiz
        print(f" {bayt} B @ {hiz / 1e6:.0f} Mb/s : yalniz yuk {yalniz:.0f} bit"
              f" <-> sure x bit_hizi {esdeger:.0f} bit"
              f"  = %{100 * (esdeger / yalniz - 1):.2f} fark")
        print(f"      PER(SINR=10 dB) : {per_dbpsk(10.0, yalniz):.4f}"
              f" <-> {per_dbpsk(10.0, esdeger):.4f}")


def bolum_d():
    print()
    print("=" * 74)
    print("D - PER GECIS BANDI")
    print("=" * 74)
    bit = 8 * PAKET_BAYT
    for h in (0.99, 0.9, 0.5, 0.1, 0.01):
        print(f"   PER={h:<5} -> SINR {sinr_icin_db(h, bit):6.2f} dB")
    bant = sinr_icin_db(0.01, bit) - sinr_icin_db(0.99, bit)
    print(f"   0,01 <-> 0,99 BANT GENISLIGI : {bant:.2f} dB"
          f"   (golgeleme sigma = 2-4 dB)")


def bolum_e():
    print()
    print("=" * 74)
    print("E - GUCLER (karistiricinin eski calisma noktasi tasinamaz)")
    print("=" * 74)
    eski_pt = verici_gucu_dbm(1e6)
    yeni_pt = verici_gucu_dbm(BANT_HZ)
    print(f" gurultu tabani : 1 MHz {dbm(gurultu_w(1e6)):.2f} dBm"
          f"  .  2 MHz {dbm(gurultu_w(BANT_HZ)):.2f} dBm")
    print(f" dugum Pt (R={R:.0f} m'den TURETILIR) :"
          f" eski {eski_pt:+.2f} dBm  .  yeni {yeni_pt:+.2f} dBm")
    print(f" eski S2 karistirici +2,00 dBm -> dugume gore {2.0 - eski_pt:+.2f} dB")
    print(f" ayni FARKI koruyan yeni guc   -> {yeni_pt + (2.0 - eski_pt):+.2f} dBm")
    print(" BASLANGIC NOKTASI, cevap DEGIL: golgeleme + sonumleme teslim")
    print(" egrisini kaydirir; guc, ilan edilmis olcutle TARANARAK secilir.")


def main() -> None:
    bolum_a()
    bolum_b()
    bolum_c()
    bolum_d()
    bolum_e()


def bayatlik_raporu() -> None:
    """Bu betikteki tarihsel sabitler güncel `Konfig`den ne kadar ayrıştı?"""
    k = Konfig(kol="kalib")
    esleme = (
        ("N", N, k.dugum_sayisi), ("R", R, k.iletim_menzili_m),
        ("EN", EN, k.alan_en_m), ("YUKSEKLIK", YUKSEKLIK, k.irtifa_maks_m),
        ("BIT_HIZI", BIT_HIZI, k.bit_hizi_bps),
        ("PAKET_BAYT", PAKET_BAYT, k.paket_bayt),
        ("ONBELGE_S", ONBELGE_S, k.onbelge_s),
        ("BANT_HZ", BANT_HZ, k.bant_genisligi_hz),
        ("FREKANS_HZ", FREKANS_HZ, k.frekans_hz),
        ("YOL_KAYBI_USTELI", YOL_KAYBI_USTELI, k.yol_kaybi_usteli),
        ("SINR_ESIGI_DB", SINR_ESIGI_DB, k.sinr_esigi_db),
        ("GURULTU_FIGURU_DB", GURULTU_FIGURU_DB, k.gurultu_figuru_db),
        ("SICAKLIK_K", SICAKLIK_K, k.sicaklik_k),
        ("ONAY_BAYT", ONAY_BAYT, k.onay_bayt),
        ("BEACON_BAYT", BEACON_BAYT, k.beacon_bayt),
    )
    ayrisan = [(ad, a, b) for ad, a, b in esleme if float(a) != float(b)]
    print("=" * 76)
    print("0 - BAYATLIK RAPORU  (bu betigin sabitleri 4 Eylul 2026 ADAYLARIDIR)")
    print("=" * 76)
    if not ayrisan:
        print("  Hicbiri ayrismadi.")
        return
    print(f"  🔴 {len(ayrisan)} sabit guncel Konfig'den AYRISTI:")
    for ad, tarihsel, guncel in ayrisan:
        print(f"    {ad:<20} bu betik {tarihsel:<12} ↔ Konfig {guncel}")
    print("  Asagidaki olcumler TARIHSEL degerlerle uretilmistir; bugunku")
    print("  calisma noktasi icin `kalibrasyon/calisma_noktasi.py`ye bak.")


if __name__ == "__main__":
    bayatlik_raporu()
    main()
