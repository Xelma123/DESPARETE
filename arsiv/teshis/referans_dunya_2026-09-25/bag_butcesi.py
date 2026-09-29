"""Referans dünya (Faz 0) — 802.11b bağ bütçesi, yalnız aritmetik.

Kaynaklar (`protokol_kaynaklari/README.md`, `v2/02` G1 · G2):
  · BER ve Eb/N0 eşlemesi: Pei & Henderson 2009 (ns-3 802.11b, CMU ölçümüyle
    karşılaştırılmış) — DBPSK Eb/N0 = SNR·22, DQPSK Eb/N0 = SNR·11,
    gürültü 22 MHz'de, gürültü figürü 7 dB (raporun kendi ayarı).
  · ED eşikleri, duyarlılık, slot: Boer 1996 (IEEE P802.11-96/49E).
Soruları: gerçek bir 802.11b telsizi (a) hangi alınan güçte çerçeveyi
çözer, (b) serbest uzayda hangi mesafeye kadar, (c) karıştırıcı hangi
mesafeden bir bağı keser — işlem kazancı hesaba katılarak.

Çalıştırma: python arsiv/teshis/referans_dunya_2026-09-25/bag_butcesi.py
"""
import math

K_BOLTZMANN = 1.380649e-23
T0 = 290.0
B_HZ = 22e6                  # 802.11b kanal genişliği (G1)
NF_DB = 7.0                  # Pei & Henderson'ın ns-3 ayarı (G1)
F_HZ = 2.437e9               # kanal 6
C = 299_792_458.0
DIPOL_DBI = 2.15             # yarım dalga dipol, en büyük kazanç
CERCEVE_BIT = (512 + 64) * 8 # veri 512 B + kapsülleme 64 B (bugünkü model)
PER_HEDEF = 0.10             # "çözülür" tanımı: PER ≤ %10


def dbm(w: float) -> float:
    return 10 * math.log10(w * 1e3)


def gurultu_dbm() -> float:
    return dbm(K_BOLTZMANN * T0 * B_HZ) + NF_DB


def ber_dbpsk(ebn0: float) -> float:
    return 0.5 * math.exp(-ebn0)


def ber_dqpsk(ebn0: float) -> float:
    # Ferrari–Corazza yaklaşımı (Pei & Henderson denklem 1.5–1.6)
    if ebn0 <= 0:
        return 0.5
    return min(0.5, (math.sqrt(2) + 1) / math.sqrt(8 * math.pi * math.sqrt(2))
               / math.sqrt(ebn0) * math.exp(-(2 - math.sqrt(2)) * ebn0))


KIPLER = {"1 Mb/s DBPSK": (ber_dbpsk, 22.0), "2 Mb/s DQPSK": (ber_dqpsk, 11.0)}


def gereken_snr_db(ber, carpan: float) -> float:
    """PER ≤ PER_HEDEF için gereken SNR (22 MHz'de), ikiye bölmeyle."""
    alt, ust = -20.0, 30.0
    for _ in range(80):
        orta = (alt + ust) / 2
        snr = 10 ** (orta / 10)
        per = 1 - (1 - ber(snr * carpan)) ** CERCEVE_BIT
        alt, ust = (orta, ust) if per > PER_HEDEF else (alt, orta)
    return ust


def fspl_db(d_m: float) -> float:
    return 20 * math.log10(4 * math.pi * d_m * F_HZ / C)


def mesafe_m(kayip_db: float) -> float:
    return C / (4 * math.pi * F_HZ) * 10 ** (kayip_db / 20)


def main() -> None:
    n = gurultu_dbm()
    print(f"gürültü tabanı (22 MHz, NF {NF_DB:.0f} dB): {n:.1f} dBm")
    print(f"çerçeve {CERCEVE_BIT} bit · 'çözülür' = PER ≤ {PER_HEDEF:.0%}\n")
    esik = {}
    for ad, (ber, carpan) in KIPLER.items():
        snr = gereken_snr_db(ber, carpan)
        esik[ad] = snr
        print(f"{ad}: gereken SNR {snr:+.1f} dB (22 MHz) · "
              f"Eb/N0 {snr + 10 * math.log10(carpan):.1f} dB · "
              f"duyarlılık {n + snr:.1f} dBm")
    print("\n(Boer 1996: standardın alt sınırı −80 dBm @ 2 Mb/s, FER 0,08, 1024 B)")

    print("\nserbest uzay menzili, 2 Mb/s (alıcıda dipol 2,15 dBi):")
    print("  verici EIRP                               sönümsüz   10 dB pay   20 dB pay")
    # 🔒 AB/TR sınırı EIRP'dir (anten dâhil) — Boer 1996 "100 mW Europe",
    # Doodle Labs RM-2450 veri sayfası "In Europe, the max EIRP is 100mW".
    for ad, eirp in (("AB/TR sınırı 20 dBm (iletilen 17,85 + dipol)", 20.0),
                     ("Doodle Labs Pro 27 dBm + dipol", 27.0 + DIPOL_DBI),
                     ("Doodle Labs Xtreme 33 dBm + dipol", 33.0 + DIPOL_DBI)):
        butce = eirp + DIPOL_DBI - (n + esik["2 Mb/s DQPSK"])
        satir = [mesafe_m(butce - pay) / 1000 for pay in (0.0, 10.0, 20.0)]
        print(f"  {ad:44s} {satir[0]:6.1f} km   {satir[1]:6.2f} km   "
              f"{satir[2]:6.2f} km")

    print("\nED eşiği (Boer): verici >100 mW → −80 dBm · >50 mW → −76 · ≤50 mW → −70")

    print("\nkarıştırıcının bir bağı kestiği mesafe (2 Mb/s, gürültü benzeri karıştırıcı,")
    print("işlem kazancı dâhil: karıştırıcı gürültü gibi SNR'a girer):")
    gerek = 10 ** (esik["2 Mb/s DQPSK"] / 10)
    print("(düğüm EIRP 20 dBm — AB/TR sınırı; karıştırıcı dipolü 2,15 dBi EIRP'e dâhil sayılmaz,")
    print(" alıcı dipolü eklenir)")
    for bag_km in (0.5, 1.0, 2.0):
        s = 20.0 + DIPOL_DBI - fspl_db(bag_km * 1000)            # dBm
        s_w = 10 ** (s / 10) / 1e3
        n_w = 10 ** (n / 10) / 1e3
        j_izin_w = s_w / gerek - n_w                           # S/(N+J) = gerek
        for eirp in (30.0, 40.0, 47.0):
            if j_izin_w <= 0:
                print(f"  bağ {bag_km} km: gürültüyle zaten kopuk")
                break
            kayip = eirp + DIPOL_DBI - dbm(j_izin_w)
            print(f"  bağ {bag_km:.1f} km (S {s:.1f} dBm) · karıştırıcı EIRP "
                  f"{eirp:.0f} dBm ({10 ** (eirp / 10) / 1e3:.0f} W) → "
                  f"{mesafe_m(kayip) / 1000:.1f} km'den keser")


if __name__ == "__main__":
    main()
