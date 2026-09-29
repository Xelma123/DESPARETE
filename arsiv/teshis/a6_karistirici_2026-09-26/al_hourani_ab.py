"""Al-Hourani, Kandeepan, Lardner 2014 (`02` G6) — S-eğrisi a, b katsayıları.

Makalenin denklem (6)'sı ve Tablo I–II'si. Ortam parametreleri (α, β, γ)
Şekil 2'nin metninden: banliyö (0,1; 750; 8) · kentsel (0,3; 500; 15) ·
yoğun kentsel (0,5; 300; 20) · yüksek yapılı (0,5; 300; 50).
P(LoS, θ) = 1 / (1 + a·exp(−b[θ − a])), θ derece.

🔴 İNDEKS OKUMASI. Metin z = Σ C_ij (αβ)^i γ^j diyor ve tablonun sütunu i,
satırı j. Bu okuma (A) b'yi NEGATİF verir: P(LoS) açıyla AZALIR —
fiziksel olarak imkânsız (yükseldikçe görüş hattı artar; Şekil 2'nin bütün
eğrileri artan). Ters okuma (B) — sütun indeksi γ'nın, satır indeksi αβ'nın
üssü — banliyöde a ≈ 4,88, b ≈ 0,43 verir ve Şekil 2 ile tutarlı: P(LoS)
≈ 0,5 yaklaşık 9°'de, 20°'de ≈ 1. Simülatör (B)'yi kullanır; seçimin
gerekçesi bu karşılaştırmadır.

Kullanım:
    PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 python \
        arsiv/teshis/a6_karistirici_2026-09-26/al_hourani_ab.py
"""

import math

# Tablo I — a · Tablo II — b ; anahtar (sütun, satır) = tablodaki (i, j)
C_A = {(0, 0): 9.34e-01, (1, 0): 2.30e-01, (2, 0): -2.25e-03, (3, 0): 1.86e-05,
       (0, 1): 1.97e-02, (1, 1): 2.44e-03, (2, 1): 6.58e-06,
       (0, 2): -1.24e-04, (1, 2): -3.34e-06,
       (0, 3): 2.73e-07}
C_B = {(0, 0): 1.17e+00, (1, 0): -7.56e-02, (2, 0): 1.98e-03, (3, 0): -1.78e-05,
       (0, 1): -5.79e-03, (1, 1): 1.81e-04, (2, 1): -1.65e-06,
       (0, 2): 1.73e-05, (1, 2): -2.02e-07,
       (0, 3): -2.00e-08}
ORTAMLAR = {"banliyo": (0.1, 750.0, 8.0), "kentsel": (0.3, 500.0, 15.0),
            "yogun": (0.5, 300.0, 20.0), "yuksek": (0.5, 300.0, 50.0)}


def polinom(c: dict, sutun_taban: float, satir_taban: float) -> float:
    return sum(v * sutun_taban ** i * satir_taban ** j
               for (i, j), v in c.items())


def ab(alfa: float, beta: float, gama: float) -> tuple[float, float]:
    """(B) okuması — simülatörün kullandığı."""
    return (polinom(C_A, gama, alfa * beta), polinom(C_B, gama, alfa * beta))


def p_los(a: float, b: float, teta_derece: float) -> float:
    return 1.0 / (1.0 + a * math.exp(-b * (teta_derece - a)))


if __name__ == "__main__":
    for okuma, fn in (("A metin", lambda al, be, ga: (
            polinom(C_A, al * be, ga), polinom(C_B, al * be, ga))),
                      ("B ters ", ab)):
        print(f"--- okuma {okuma}")
        for ad, (alfa, beta, gama) in ORTAMLAR.items():
            a, b = fn(alfa, beta, gama)
            p = [p_los(a, b, th) for th in (5, 10, 20, 45)]
            print(f"  {ad:<8} a = {a:8.3f} · b = {b:8.4f} · P(LoS) "
                  f"θ=5/10/20/45°: " + " / ".join(f"{x:.3f}" for x in p))
