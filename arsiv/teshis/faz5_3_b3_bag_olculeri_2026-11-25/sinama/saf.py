"""
B3 teşhisinin saf işlevlerinin sınaması (`../bag.py`). Yapay örnekler,
beklenen değerler elle hesaplandı. Simülatör kullanılmaz.

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz5_3_b3_bag_olculeri_2026-11-25/sinama/saf.py
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import bag as B  # noqa: E402

SAY = [0]


def esit(ad, gercek, beklenen, tol=1e-9):
    def yakin(a, b):
        if isinstance(a, float) or isinstance(b, float):
            if a is None or b is None:
                return False
            if math.isinf(a) or math.isinf(b):
                return a == b
            return abs(a - b) <= tol
        if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
            return len(a) == len(b) and all(yakin(x, y) for x, y in zip(a, b))
        return a == b
    if not yakin(gercek, beklenen):
        raise AssertionError(f"{ad}: {gercek!r} ≠ {beklenen!r}")
    SAY[0] += 1
    print(f"  tamam · {ad}")


print("1 · sıra farkı")
esit("65535 → 0", B.sira_farki(0, 65535), 1)
esit("0 → 65535", B.sira_farki(65535, 0), -1)
esit("3 → 5", B.sira_farki(5, 3), 2)

print("2 · düzenli selam, d_f ve zaman aşımı")
gel = [(0.5 + i, i, 1.1, 0.9) for i in range(10)]
s = B.b1_selam(gel, [], [10.0, 12.0])
esit("T=10: 10 örnek, hepsi 1", s[0], (1.0, 10, 0.9, True))
esit("T=12: 11,15'te bir zaman aşımı sıfırı", s[1], (10 / 11, 11, 0.9, True))

print("3 · ileri sarma: sıfırlar araya, oran en yeni oranlı örnekten")
s = B.b1_selam([(0.0, 0, 2.0, None), (1.0, 3, 2.0, 0.5)], [], [1.5])
esit("T=1,5: [1 0 0 1]", s[0], (0.5, 4, 0.5, True))

print("4 · geri alma (zaman aşımının fazla saydığı sıfırlar)")
s = B.b1_selam([(0.0, 0, 1.0, 0.8), (3.8, 1, 1.0, None)], [], [3.0, 4.0])
esit("T=3: 1,5 ve 2,5'te iki sıfır", s[0], (1 / 3, 3, 0.8, True))
esit("T=4: 3,5'teki sıfır da eklendi, selam üçünü sildi", s[1],
     (1.0, 2, 0.8, True))

print("5 · yeniden başlama (fark > 64)")
s = B.b1_selam([(0.0, 0, 1.0, None), (1.0, 100, 1.0, None)], [], [1.2])
esit("T=1,2: örnekler silindi, oran yok", s[0], (1.0, 1, None, True))

print("6 · silme (30 s duyulmama), yeniden kayıt")
gel = [(0.0, 0, 2.0, 0.7), (40.0, 5, 2.0, None)]
s = B.b1_selam(gel, [], [29.0, 31.0, 41.0])
esit("T=29: 3, 5, …, 27'de 13 sıfır", s[0], (1 / 14, 14, 0.7, True))
esit("T=31: 30'da silindi", s[1], (None, 0, None, False))
esit("T=41: yeni selamla yeniden kayıt", s[2], (1.0, 1, None, True))

print("7 · tazeleme silmeyi erteler; d_f 30 s'de unutulur")
s = B.b1_selam(gel, [25.0], [31.0])
esit("T=31: kayıt duruyor, 14 sıfır, oran 31 s eski", s[0],
     (1 / 15, 15, None, True))

print("8 · N_SELAM penceresi")
gel = [(0.5 * i, i, 0.6, None) for i in range(20)]
s = B.b1_selam(gel, [], [10.0])
esit("T=10: 20 selam, son 16'sı", s[0], (1.0, 16, None, True))

print("9 · aynı anda zaman aşımı ve selam: net etki yok")
s = B.b1_selam([(0.0, 0, 1.0, None), (1.5, 1, 1.0, None)], [], [2.0])
esit("T=2: önce sıfır, sonra geri alma", s[0], (1.0, 2, None, True))

print("10 · sorgu nedensel: sorgu anındaki selam sayılmaz")
s = B.b1_selam([(0.0, 0, 1.0, None), (1.0, 1, 1.0, None)], [], [1.0, 1.0001])
esit("T=1,0: yalnız ilk selam", s[0], (1.0, 1, None, True))
esit("T=1,0001: ikisi", s[1], (1.0, 2, None, True))

print("11 · kayıt yokken")
s = B.b1_selam([(5.0, 0, 1.0, None)], [], [4.0])
esit("T=4: ilk selamdan önce", s[0], (None, 0, None, False))

print("12 · E_selam ve E_veri")
esit("E_selam(0,9 · 0,5)", B.e_selam(0.9, 0.5), 1 / 0.45)
esit("E_selam d_f tanımsız", B.e_selam(None, 0.5), math.inf)
esit("E_selam d_r 0", B.e_selam(0.9, 0.0), math.inf)
esit("E_veri 5/3", B.e_veri(5, 3, 4), 5 / 3)
esit("E_veri G = 0", B.e_veri(7, 0, 1), math.inf)
esit("E_veri kayıt yok", B.e_veri(0, 0, 0), None)

print("13 · kodlama ve özet")
esit("kod 1 onaylı", B.kod(1, True), "1")
esit("kod 7 onaylı", B.kod(7, True), "7")
esit("kod vazgeçme", B.kod(7, False), "x")
esit("özet en yeni 2 (x3)", B.ozet("12x3", 2), (2, 10, 1))
esit("özet en eski 3 (12x)", B.ozet("12x3", 3, sondan=False), (3, 10, 2))
esit("özet boş", B.ozet("", 4), (0, 0, 0))
esit("özet n = 0", B.ozet("123", 0), (0, 0, 0))
esit("özet n > uzunluk", B.ozet("12", 16), (2, 3, 2))

print("14 · hata")
esit("2 ↔ 4: 1 bit", B.hata(2.0, 4.0), 1.0)
esit("4 ↔ 2: 1 bit", B.hata(4.0, 2.0), 1.0)
esit("∞ ↔ ∞", B.hata(math.inf, math.inf), 0.0)
esit("2 ↔ ∞: log2(64/2)", B.hata(2.0, math.inf), 5.0)

print(f"\n{SAY[0]} denetim geçti")
