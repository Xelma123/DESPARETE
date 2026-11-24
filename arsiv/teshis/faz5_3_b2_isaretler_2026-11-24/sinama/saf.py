"""
B2 teşhisinin saf işlevlerinin sınaması (`../isaret.py`). Yapay örnekler,
beklenen değerler elle hesaplandı. Simülatör kullanılmaz.

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz5_3_b2_isaretler_2026-11-24/sinama/saf.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import isaret as I  # noqa: E402

SAY = [0]


def esit(ad, gercek, beklenen, tol=1e-9):
    def yakin(a, b):
        if isinstance(a, float) or isinstance(b, float):
            return a is not None and b is not None and abs(a - b) <= tol
        if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
            return len(a) == len(b) and all(yakin(x, y) for x, y in zip(a, b))
        return a == b
    if not yakin(gercek, beklenen):
        raise AssertionError(f"{ad}: {gercek!r} ≠ {beklenen!r}")
    SAY[0] += 1
    print(f"  tamam · {ad}")


print("1 · sıra farkı")
esit("65535 → 0", I.sira_farki(0, 65535), 1)
esit("0 → 65535", I.sira_farki(65535, 0), -1)
esit("3 → 5", I.sira_farki(5, 3), 2)

print("2 · düzenli selam ve zaman aşımı")
gel = [(0.5 + i, i, 1.1) for i in range(10)]
g, z = I.bag_simule(gel, 12.0)
esit("T=10 (n1, n0, sondaki, dr, son, a)", g[10], (4, 0, 0, 1.0, 9.5, 1.1))
esit("T=12", g[12], (2, 1, 1, 1.0, 9.5, 1.1))
esit("sıfırlar", z, [(11.15, 1, 1.0)])

print("3 · ileri sarma (sıfırlar araya dağıtılır)")
g, z = I.bag_simule([(0.0, 0, 2.0), (1.0, 3, 2.0)], 2.0)
esit("T=0", g[0], (1, 0, 0, 1.0, 0.0, 2.0))
esit("T=1", g[1], (2, 2, 0, 0.5, 1.0, 2.0))
esit("zaman aşımı sıfırı yok", z, [])

print("4 · geri alma (zaman aşımının fazla saydığı sıfırlar)")
g, z = I.bag_simule([(0.0, 0, 1.0), (3.8, 1, 1.0)], 5.0)
esit("sıfırlar", z, [(1.5, 1, 1.0), (2.5, 2, 1.0), (3.5, 3, 1.0)])
esit("T=3", g[3], (1, 2, 2, 1.0, 0.0, 1.0))
esit("T=4 (sıfırlar silindi)", g[4], (1, 0, 0, 1.0, 3.8, 1.0))

print("5 · yeniden başlama (fark > 64)")
g, z = I.bag_simule([(0.0, 0, 1.0), (1.0, 100, 1.0)], 1.0)
esit("T=1", g[1], (1, 0, 0, 1.0, 1.0, 1.0))

print("6 · silme (30 s selam yok) ve yeniden kayıt")
g, z = I.bag_simule([(0.0, 0, 2.0), (40.0, 5, 2.0)], 41.0)
esit("sıfır sayısı (3, 5, …, 29)", len(z), 14)
esit("T=29 sondaki", g[29][2], 14)
esit("T=30 silindi", g[30], None)
esit("T=35 kayıt yok", g[35], None)
esit("T=40 yeni kayıt", g[40], (1, 0, 0, 1.0, 40.0, 2.0))

print("7 · selam kaybı payı (tanıdık komşular)")
A = [None] * 21
B = [None] * 21
A[20] = (3, 1, 0, 0.9, 19.0, 1.0)
B[20] = (0, 2, 2, 0.8, 2.0, 1.0)          # son selamı 18 s önce: tanıdık değil
esit("s", I.selam_kaybi([A, B], 20), 0.25)
esit("hiç tanıdık yok", I.selam_kaybi([B], 20), None)

print("8 · uyarlanır k (önceki KK-03 kural 6)")
esit("d_r 0,9", I.k_uyarlanir(0.9), 3)
esit("d_r 0,6", I.k_uyarlanir(0.6), 6)
esit("d_r 0,5", I.k_uyarlanir(0.5), 7)
esit("d_r 0,25", I.k_uyarlanir(0.25), 16)
esit("tanımsız", I.k_uyarlanir(None), 16)

print("9 · veri kuralları")
cer = [(1.0, 1, True), (2.0, 7, False), (3.0, 7, False), (4.0, 7, False),
       (5.0, 1, True)]
a = I.veri_ates(cer, [0.0], [1.0])
esit("kural sayısı", len(I.KURALLAR), 27)
esit("VAZ1", a["VAZ1"], [2.0])
esit("VAZ2", a["VAZ2"], [3.0])
esit("VAZ3", a["VAZ3"], [4.0])
esit("DEN4x2", a["DEN4x2"], [3.0])
esit("DEN7x3", a["DEN7x3"], [4.0])
esit("BIR6_10x1 (selam 2 s önce)", a["BIR6_10x1"], [2.0])
esit("BIR6_15x2", a["BIR6_15x2"], [3.0])
a = I.veri_ates(cer, [1.9], [1.0])
esit("BIR6_10x1 (selam taze)", a["BIR6_10x1"], [3.0])
esit("BIR6_10x2", a["BIR6_10x2"], [4.0])
esit("BIR6_15x1", a["BIR6_15x1"], [4.0])
esit("BIR6_15x2", a["BIR6_15x2"], [])
esit("ilk ateş [4, 8)", I.ilk_ates([1.0, 5.0, 9.0], 4.0, 8.0), 1.0)
esit("ilk ateş yok", I.ilk_ates([1.0, 5.0, 9.0], 10.0, 12.0), None)

print("10 · sessizlik kuralları")
s = I.ses_ates([(3.0, 1, 0.9), (5.0, 2, 0.9), (7.0, 3, 0.9), (9.0, 4, 0.9)])
esit("SES2", s["SES2"], [(5.0, 0.9)])
esit("SES3", s["SES3"], [(7.0, 0.9)])
esit("SES4", s["SES4"], [(9.0, 0.9)])
esit("SESu (d_r 0,9 → k 3)", s["SESu"], [(7.0, 0.9)])

print("11 · girişim işareti ve c̄")
n = 45
m = [0.3] * n
c = [100] * 40 + [30] * 5
sk = [0.3] * 40 + [0.8] * 5
sif = [0] * n
G = I.g_isareti(m, c, sk, sif, sif, sif, 0.5, 0.6, oy=False)
esit("ilk 40 s işaretsiz", G[:40], [False] * 40)
esit("son 5 s işaretli", G[40:], [True] * 5)
c2 = [100] * 41
s2 = [0.3] * 40 + [0.8]
a2 = [0] * 40 + [4]
f2 = [0] * 40 + [3]
k2 = [0] * 40 + [2]
esit("G: yalnız S", I.g_isareti([0.3] * 41, c2, s2, a2, f2, k2, 0.5, 0.6,
                                oy=False)[40], False)
esit("GM: S ve M", I.g_isareti([0.3] * 41, c2, s2, a2, f2, k2, 0.5, 0.6,
                               oy=True)[40], True)
esit("c̄ yokken C yok", I.g_isareti([0.3], [0], [0.9], [0], [0], [0],
                                    0.5, 0.6, oy=False), [False])

print("12 · durum (giriş 2, çıkış 2)")
x = [False, True, True, False, True, True, True, False, False, False]
esit("durum", I.durum(x, 2, 2),
     [False, False, True, True, True, True, True, True, False, False])

print("13 · dönem ölçüsü")
d = [False] * 20
for T in range(6, 10):
    d[T] = True
esit("giriş 2 s, çıkış 3 s", I.donem_olcusu(d, 5.0, 8.0, None), (2.0, 3.0))
esit("yakalanmadı", I.donem_olcusu(d, 12.0, 15.0, None), (None, None))
d2 = [False] * 20
d2[8] = d2[9] = True
esit("karar dönem bitince: yok", I.donem_olcusu(d2, 5.0, 8.5, None),
     (None, None))

print("14 · ızgara")
esit("kendi durumum kural sayısı", len(I.izgara()), 7 + 2 * 144)
esit("eski kural ızgarada", I.ESKI_KURAL in I.izgara(), True)

print(f"\n{SAY[0]} denetim geçti")
