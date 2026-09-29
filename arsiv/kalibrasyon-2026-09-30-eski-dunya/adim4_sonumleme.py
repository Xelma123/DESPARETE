"""ADIM 4 — SÖNÜMLEME PARAMETRELERİNİN TÜRETİLMESİ ve DOĞRULANMASI.

Üretici:  PYTHONIOENCODING=utf-8 python kalibrasyon/adim4_sonumleme.py

🔴 NEDEN BU BETİK VAR
=====================
Devir belgesi parça süresini **30 m/s'lik bir VARSAYIMDAN** türetiyordu.
Bizim artık ölçülmüş bir bağıl hız dağılımımız var; parça süresi ondan
türetilir. Betik dört şey yapar:

    A. Bağıl hız dağılımı → Doppler → tutarlılık süresi
    B. Parça süresinin türetimi ve çerçeve başına parça sayısı
    C. Sönümlemenin ölçülen istatistiği (ortalama · varyans · otokorelasyon)
    D. MALİYET — risk 1'in "%15'i aşarsa memo" eşiği
"""
from __future__ import annotations

import math
import pathlib
import statistics as ist
import sys
import time

KOK = pathlib.Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))
if str(KOK / "kalibrasyon") not in sys.path:
    sys.path.insert(0, str(KOK / "kalibrasyon"))
# 🔒 Denetimli bagil hizli topoloji taslagi testlerde tanimli. Burada YENIDEN
# yazilsaydi iki kopya ayrisabilir ve olculen sey ile test edilen sey farkli
# olurdu — bu projenin kacindigi hata sinifi.
if str(KOK / "tests2") not in sys.path:
    sys.path.insert(0, str(KOK / "tests2"))

from mobilite_gercekcilik import bagil_hizlar, izler  # noqa: E402
from sim2.cekirdek.rng import Akislar  # noqa: E402
from sim2.dunya.topoloji import topoloji_kur  # noqa: E402
from sim2.kanal.cerceve import cerceve_kur  # noqa: E402
from sim2.kanal.sonumleme import (BAGIL_HIZ_TABANI_MS,  # noqa: E402
                                  FIR_EN_COK_KATSAYI, Sonumleme)
from sim2.kanal.yayilim import ISIK_HIZI  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402
from kalibrasyon import dunya_secimi as DS  # noqa: E402  (K-183)

TOHUMLAR = range(1, 11)


# ==========================================================================
# 🔴 BU BETİK K-102'Yİ KAÇIRMIŞTI — 9 Eylül 2026'da bulundu ve onarıldı.
# ==========================================================================
# Bölüm A/B, T_c'yi **ÖLÇEKLİ** bağıl hızdan hesaplıyordu. K-102 (8 Eylül)
# Doppler'i **TAM ÖLÇEK** hızına bağladı — dalga boyu ölçeklenemediği için.
# Betik güncellenmedi ve sonuç şuydu:
#
#     bolum B'nin ilan ettigi olcut : T_c(p99)/4
#     betigin hesapladigi           : 38 666 us / 4 = 9 666 us
#     KONFIGDEKI deger              :               190 us     (51 kat fark)
#
# İkisi yan yana basılıyor ve **fark hiç açıklanmıyordu**. Yani
# `sonumleme_parca_suresi_s` kaydının (`OLCULMUS`) gösterdiği üretici,
# bugün kaydın değerinden 51 kat farklı bir sayı üretiyordu — D15'in tam
# olarak tarif ettiği tehlike: *"sayıyı doğrulamak için onu koşturan biri
# başka bir cevap alır ve nedenini bilemez."*
#
# 🔒 ÇÖZÜM İKİNCİ BİR FORMÜL DEĞİL, MODELİN KENDİSİ. Aşağıdaki fonksiyon
# `Sonumleme.tutarlilik_suresi_s`i ÇAĞIRIR; ölçek dönüşümü tek yerde kalır
# ve bir daha ayrışamaz.
def tutarlilik_s(v_ms: float, konfig: Konfig) -> float:
    """T_c — MODELİN KENDİ hesabından (ölçek dâhil). İkinci gerçekleme YOK.

    `v_ms` ÖLÇEKLİ bağıl hızdır; ölçeğe çevirmeyi model yapar.
    """
    from test_kanal_sonumleme import SabitHizTopoloji
    return Sonumleme(konfig, SabitHizTopoloji(max(v_ms, 1e-9))
                     ).tutarlilik_suresi_s(0, 1, 0.0)


def _tc_formul(v_ms: float, lam: float) -> float:
    """🔒 SAF FORMÜL — yalnız bölüm C'nin FIR sınavı için.

    Bölüm C, FIR'ın verilen bir ρ'yu doğru üretip üretmediğini sınar; ρ
    orada bir **sınav girdisidir**, modelin çalışma noktası değil. Bu yüzden
    burada ölçek çarpanı YOKTUR ve olmamalıdır — sınav, kullanışlı bir ρ
    aralığı (0,83…0,996) taramak zorunda.
    """
    return 0.423 * lam / max(v_ms, 1e-9)


def bolum_a_b():
    k = DS.konfig(kol="kalib")
    lam = ISIK_HIZI / k.frekans_hz
    cerceve = cerceve_kur(k, "veri")
    print("=" * 76)
    print("A - BAGIL HIZ -> DOPPLER -> TUTARLILIK SURESI")
    print("=" * 76)
    print(f"  dalga boyu {lam*100:.2f} cm . veri cercevesi "
          f"{cerceve.sure_s*1e6:.0f} us")
    p99 = None
    for senaryo, ad in (("bagimsiz-yok", "bagimsiz"), ("gorev-yok", "gorev")):
        h = []
        for t in TOHUMLAR:
            h.extend(bagil_hizlar(izler(senaryo, t)))
        h.sort()
        def q(p):
            return h[min(int(p * len(h)), len(h) - 1)]
        print(f"  {ad:9s} ortanca {ist.median(h):5.1f} . p95 {q(.95):5.1f} . "
              f"p99 {q(.99):5.1f} m/s")
        for etiket, v in (("ortanca", ist.median(h)), ("p95", q(.95)),
                          ("p99", q(.99))):
            tc = tutarlilik_s(v, k)
            print(f"      {etiket:8s} v={v:5.1f} -> f_d {v/lam:6.1f} Hz . "
                  f"T_c {tc*1e3:5.2f} ms . cerceve/T_c {cerceve.sure_s/tc:5.2f}")
        if ad == "bagimsiz":
            p99 = q(.99)

    print()
    print("=" * 76)
    print("B - PARCA SURESI TURETIMI")
    print("=" * 76)
    tc99 = tutarlilik_s(p99, k)
    print(f"  OLCUT (ilan): parca suresi = T_c(p99) / 4")
    print(f"    T_c(p99) = {tc99*1e6:.0f} us -> parca = {tc99/4*1e6:.0f} us")
    print(f"    KONFIGDEKI deger : {k.sonumleme_parca_suresi_s*1e6:.0f} us")
    son = Sonumleme(k, topoloji_kur(DS.konfig(kol="k", senaryo="bagimsiz-yok"),
                                    Akislar(1)))
    for tip in ("veri", "onay", "beacon"):
        c = cerceve_kur(k, tip)
        print(f"    {tip:7s} cercevesi {c.sure_s*1e6:6.0f} us -> "
              f"{son.parca_sayisi(c.sure_s):3d} parca")
    print(f"  ESKI varsayilan 80 us olsaydi: veri cercevesi "
          f"{math.ceil(cerceve.sure_s/80e-6):d} parca (3 kat pahali)")


def bolum_c():
    print()
    print("=" * 76)
    print("C - SONUMLEMENIN OLCULEN ISTATISTIGI")
    print("=" * 76)
    k = DS.konfig(kol="kalib")
    lam = ISIK_HIZI / k.frekans_hz
    k_lin = 10.0 ** (k.rician_k_db / 10.0)
    beklenen_var = (1.0 + 2.0 * k_lin) / (1.0 + k_lin) ** 2
    print(f"  Rician K = {k.rician_k_db} dB -> analitik E|g|2 = 1,000 . "
          f"Var|g|2 = {beklenen_var:.3f}")
    print(f"{'hiz':>5s} {'T_c(ms)':>8s} {'rho':>7s} {'M':>4s} "
          f"{'E|g|2':>8s} {'Var|g|2':>9s} {'rho olculen':>12s}")

    from test_kanal_sonumleme import SabitHizTopoloji  # noqa: E402
    for v in (1.0, 5.0, 25.0, 50.0):
        son = Sonumleme(k, SabitHizTopoloji(v))
        dt = k.sonumleme_parca_suresi_s
        tc = _tc_formul(max(v, BAGIL_HIZ_TABANI_MS), lam)
        ro = math.exp(-dt / tc)
        m = min(FIR_EN_COK_KATSAYI,
                max(1, math.ceil(math.log(0.01) / (2.0 * math.log(ro)))))
        g = [son.guc_kazanci(0, 1, n * dt) for n in range(60000)]
        iz = [son._fir("sonumleme_i", 0, 1, n, ro, m) for n in range(20000)]
        ort = ist.mean(iz)
        var = ist.pvariance(iz)
        r1 = (sum((iz[n] - ort) * (iz[n + 1] - ort)
                  for n in range(len(iz) - 1)) / (len(iz) - 1)) / var
        print(f"{v:5.0f} {tc*1e3:8.2f} {ro:7.4f} {m:4d} "
              f"{ist.mean(g):8.4f} {ist.pvariance(g):9.4f} "
              f"{r1:8.4f}/{ro:.4f}")
    print("  (son sutun: olculen 1-gecikme otokorelasyonu / analitik rho)")


def bolum_d():
    print()
    print("=" * 76)
    print("D - MALIYET  (risk 1: pay %15'i asarsa memo zorunlu)")
    print("=" * 76)
    k = DS.konfig(kol="kalib", senaryo="bagimsiz-yok")
    top = topoloji_kur(k, Akislar(1))
    cerceve = cerceve_kur(k, "veri")
    son = Sonumleme(k, top)
    parca = son.parca_sayisi(cerceve.sure_s)

    # Memo SICAK: aynı bağ, ardışık parçalar (gerçek kullanım deseni)
    t0 = time.perf_counter()
    n = 0
    for cerceve_no in range(2000):
        bas = 50.0 + cerceve_no * 0.008
        for sinir in son.parca_sinirlari(bas, cerceve.sure_s)[:-1]:
            son.guc_kazanci(0, 1, sinir)
            n += 1
    sicak = time.perf_counter() - t0

    # Memo SOGUK: her cagri farkli bag (en kotu hal)
    son2 = Sonumleme(k, top)
    t0 = time.perf_counter()
    m = 0
    for cerceve_no in range(2000):
        bas = 50.0 + cerceve_no * 0.008
        i, j = cerceve_no % 40, (cerceve_no * 7 + 3) % 40
        if i == j:
            j = (j + 1) % 40
        for sinir in son2.parca_sinirlari(bas, cerceve.sure_s)[:-1]:
            son2.guc_kazanci(i, j, sinir)
            m += 1
    soguk = time.perf_counter() - t0

    print(f"  cerceve basina parca      : {parca}")
    print(f"  memo SICAK (ayni bag)     : {sicak/2000*1e6:8.1f} us/cerceve "
          f"({sicak/n*1e6:.2f} us/parca)")
    print(f"  memo SOGUK (her bag yeni) : {soguk/2000*1e6:8.1f} us/cerceve "
          f"({soguk/m*1e6:.2f} us/parca)")
    # ⚠️ ETIKET DUZELTILDI (5 Eylul 2026): onbellek artik TAVANLI, dolayisiyla
    # bu sayi "toplam cekim" degil "su an tutulan girdi"dir. Tahliye sayisiyla
    # birlikte okunur; ikisi olmadan sayi sessizce yanlis anlasilirdi.
    rapor = son2.onbellek_raporu()
    print(f"  onbellekte TUTULAN girdi  : {rapor['girdi']}  "
          f"(tavan {rapor['sinir']}, tahliye {rapor['tahliye']}, "
          f"iskalama~{rapor['iskalama_tahmini']})")
    print()
    print("  Kiyas: 10 akis x 4 pkt/s x 3,0 atlama = 120 iletim/s,")
    print("  350 s kosu -> ~42 000 veri cercevesi (+ onay, beacon, girisim).")
    print(f"  Kaba tahmin: {42000*soguk/2000:.1f} s/kosu (soguk ust sinir).")


def main() -> None:
    bolum_a_b()
    bolum_c()
    bolum_d()


if __name__ == "__main__":
    main()
