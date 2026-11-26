"""
B5 teşhisinin saf işlevlerinin sınaması (`../iletim.py`). Yapay örnekler,
beklenen değerler elle hesaplandı. Simülatör kullanılmaz.

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz5_3_b5_iletim_kaybi_2026-11-26/sinama/saf.py
"""

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import iletim as L  # noqa: E402

SAY = [0]
INF = math.inf


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


print("1 · aralıklar")
o = []
L.aralik_ekle(o, 1.0, 2.0)
L.aralik_ekle(o, 2.0, 3.0)            # bitişik → birleşir
L.aralik_ekle(o, 2.5, 2.8)            # içinde → değişmez
L.aralik_ekle(o, 5.0, 6.0)
L.aralik_ekle(o, 7.0, 7.0)            # boş → eklenmez
esit("birleşme", o, [(1.0, 3.0), (5.0, 6.0)])
esit("içinde: baş dâhil", L.icinde(o, 1.0), True)
esit("içinde: son hariç", L.icinde(o, 3.0), False)
esit("içinde: arada", L.icinde(o, 4.0), False)
esit("aralığın başı", L.aralik_basi(o, 5.5), 5.0)
esit("aralığın başı yok", L.aralik_basi(o, 4.0), None)
L.aralik_kes(o, 5.4)
esit("kesme", o, [(1.0, 3.0), (5.0, 5.4)])
L.aralik_kes(o, 5.0)
esit("kesme başta: aralık silinir", o, [(1.0, 3.0)])

print("2 · B2'nin durumu: kanal kilidi")
kod, ed, g = L.durum_dizileri([0.1, 0.6, 0.7, 0.2, 0.1], [50] * 5, [None] * 5)
esit("kod", kod, "-EE--")
esit("girişim yok (s tanımsız)", g, [False] * 5)
esit("aralık: girişten 1 s geriye, 'yok'a dönülen saniyede biter",
     L.kendi_araliklar(ed, g), [(1.0, 3.0)])
esit("sınır: m = 0,55 işaret", L.durum_dizileri([0.55], [1], [None])[0], "E")

print("3 · B2'nin durumu: girişim G(0,4 · 0,6 · 2 · 1)")
m = [0.1] * 10
c = [100] * 5 + [30, 30, 30, 100, 100]
s = [0.1] * 5 + [0.7, 0.7, 0.7, 0.1, 0.1]
kod, ed, g = L.durum_dizileri(m, c, s)
esit("iki işaretli saniyede giriş, bir işaretsizde çıkış", kod, "------GG--")
esit("aralık: girişten 2 s geriye", L.kendi_araliklar(ed, g), [(5.0, 8.0)])
c2 = [100] * 5 + [40] * 3 + [100] * 2           # c = 0,4 · c̄: işaret değil
esit("sınır: c = 0,4 · c̄ işaret değil",
     L.durum_dizileri(m, c2, s)[0], "-" * 10)
s2 = [0.1] * 5 + [0.6] * 3 + [0.1] * 2          # s = 0,6: işaret
esit("sınır: s = 0,6 işaret", L.durum_dizileri(m, c, s2)[0], "------GG--")
kod, _, _ = L.durum_dizileri([0.1] * 3, [10, 0, 0], [0.9] * 3)
esit("c̄ tanımsızken (ilk saniye) işaret yok; sonra c̄ = 10", kod, "--G")

print("4 · öncelik ve birleşme")
m = [0.1] * 5 + [0.9, 0.9, 0.1, 0.1, 0.1]
c = [100] * 5 + [10, 10, 10, 10, 100]
s = [0.1] * 5 + [0.9] * 4 + [0.1]
kod, ed, g = L.durum_dizileri(m, c, s)
esit("aynı anda ikisi: kanal kilidi önce, sonra girişim", kod, "-----EEGG-")
esit("aralık: erken başlangıç (kilit 5), tek aralık",
     L.kendi_araliklar(ed, g), [(5.0, 9.0)])
ed = [False, False, True, False, False, False, False]
g = [False, False, False, False, True, True, False]
esit("bitişik aralıklar birleşir (girişimin başı 3 = kilidin sonu)",
     L.kendi_araliklar(ed, g), [(2.0, 6.0)])
esit("sürüyorsa bitiş ∞", L.kendi_araliklar([False, True], [False, False]),
     [(1.0, INF)])

print("5 · durumun bilinmesi")
kod = "-EE--"
esit("t = 2,5: T 1", L.durum_ani(kod, 2.5), "E")
esit("t = 1,9: T 0", L.durum_ani(kod, 1.9), "-")
esit("t = 0,5: henüz karar yok", L.durum_ani(kod, 0.5), "-")
esit("bilinme anı (t 3,5)", L.durum_bilinme_ani(kod, 3.5), 2.0)
esit("bilinme anı (t 2,0)", L.durum_bilinme_ani(kod, 2.0), 2.0)
esit("bilinme anı yok", L.durum_bilinme_ani(kod, 4.5), None)

print("6 · bildirim, gerçekçi biçim")
esit("1'li selamla başlar, 0'lıyla biter",
     L.bildirim_gercekci([(1, False), (2, True), (3, True), (4, False)], []),
     [(2, 4)])
esit("susarsa silmeye kadar sürer", L.bildirim_gercekci([(1, True)], []),
     [(1, 31.0)])
esit("onay silmeyi erteler", L.bildirim_gercekci([(1, True)], [20.0]),
     [(1, 50.0)])
esit("silmeden sonra yeni 1'li selam yeni aralık",
     L.bildirim_gercekci([(1, True), (40, True)], []),
     [(1, 31.0), (40, 70.0)])
esit("kayıtsızken onay yok sayılır",
     L.bildirim_gercekci([(1, True)], [35.0]), [(1, 31.0)])

print("7 · gönderici sebebi (DEN7x3, B3 kural 6)")
r = [(1, 7, False), (2, 7, False), (3, 7, False)]
esit("üçüncü tam denemede olay, 5 s", L.gonderici_araliklari(r, []), [(3, 8)])
esit("tam deneme kanıtı uzatır",
     L.gonderici_araliklari(r + [(6, 7, False)], []), [(3, 11)])
esit("süresi dolunca yeni tam deneme yeniden açar",
     L.gonderici_araliklari(r + [(6, 7, False), (12, 7, False)], []),
     [(3, 11), (12, 17)])
esit("başarılı kayıt kanıtı kaldırır",
     L.gonderici_araliklari(r + [(4, 2, True)], []), [(3, 4)])
esit("olaydan önce başarılı kayıt sayımı kırar",
     L.gonderici_araliklari([(1, 7, False), (2, 3, True), (3, 7, False),
                             (4, 7, False)], []), [])
esit("onay son denemede: tam denemeli sayılır",
     L.gonderici_araliklari([(1, 7, True), (2, 7, True), (3, 7, True)], []),
     [(3, 8)])
r4 = [(1, 7, False), (2, 7, False), (3, 7, False), (4, 7, False),
      (5, 7, False)]
esit("kendi aralığımdaki kayıt sayılmaz, sayım sıfırlanır",
     L.gonderici_araliklari(r4, [(1.5, 2.5)]), [(5, 10)])
esit("zincirde kendi aralığımdaki başarılı kayıt kanıtı kaldırmaz",
     L.gonderici_araliklari(r + [(4, 1, True)], [(3.5, 4.5)]), [(3, 8)])

print("8 · veri yok (B3 kural 7)")
v = [(1, 7, False), (2, 7, False), (3, 7, False), (4, 7, False)]
esit("dört vazgeçme: 5 s", L.veri_yok_araliklari(v, []), [(4, 9)])
esit("yeni vazgeçme sürdürür",
     L.veri_yok_araliklari(v + [(6, 7, False)], []), [(4, 11)])
esit("başarılı kayıtta biter",
     L.veri_yok_araliklari(v + [(5, 2, True)], []), [(4, 5)])
esit("pencere: en eski 30 s'den eskiyse yok",
     L.veri_yok_araliklari([(1, 7, False), (2, 7, False), (3, 7, False),
                            (35, 7, False)], []), [])
esit("pencere aralığı kısaltır",
     L.veri_yok_araliklari([(1, 7, False), (2, 7, False), (3, 7, False),
                            (28, 7, False)], []), [(28, 31)])
esit("kendi aralığımdaki kayıt sayılmaz",
     L.veri_yok_araliklari(v + [(5, 7, False)], [(3.5, 4.5)]), [(5, 10)])

print("9 · uygulanabilirlik ve maliyet")
esit("FD yokken", L.uygulanabilir(3, 500, None), True)
esit("∞ her zaman", L.uygulanabilir(3, L.SONSUZ, (5, 10)), True)
esit("daha yeni tur", L.uygulanabilir(6, 900, (5, 100)), True)
esit("aynı turda küçük maliyet", L.uygulanabilir(5, 99, (5, 100)), True)
esit("aynı turda eşit maliyet değil", L.uygulanabilir(5, 100, (5, 100)),
     False)
esit("eski tur değil", L.uygulanabilir(4, 1, (5, 100)), False)
esit("tur taşması 65535 → 0", L.uygulanabilir(0, 900, (65535, 100)), True)
esit("M: 1,0 ETX", L.maliyet_M(1.0), 64)
esit("M: yukarı yuvarlama", L.maliyet_M(1.39), 89)
esit("M: ∞", L.maliyet_M(INF), L.SONSUZ)
esit("M: tanımsız", L.maliyet_M(None), L.SONSUZ)
esit("M: tavanda doyar", L.maliyet_M(5000.0), L.SONLU_EN_COK)
esit("toplam: ∞", L.maliyet_topla(64, L.SONSUZ), L.SONSUZ)
esit("toplam: doyma", L.maliyet_topla(0xFFF0, 0x20), L.SONLU_EN_COK)

print("10 · ilanın ömrü ve aday")
esit("3,5 × a içinde taze", L.ilan_taze(17.0, 10.0, 2.0), True)
esit("3,5 × a'dan eski bayat", L.ilan_taze(17.01, 10.0, 2.0), False)
ilan = (10.0, 5, 300, 2.0)                  # (an, tur, C, aralık)
esit("aday", L.aday_mi(True, 80, ilan, 11.0, (5, 400)), True)
esit("kayıtsız değil", L.aday_mi(False, 80, ilan, 11.0, (5, 400)), False)
esit("bağ kullanılmaz değil", L.aday_mi(True, L.SONSUZ, ilan, 11.0, None),
     False)
esit("ilan bayat değil", L.aday_mi(True, 80, ilan, 18.0, None), False)
esit("uygulanamaz değil", L.aday_mi(True, 80, ilan, 11.0, (5, 300)), False)
esit("∞ ilan değil", L.aday_mi(True, 80, (10.0, 5, L.SONSUZ, 2.0), 11.0,
                               None), False)
esit("ilan yok değil", L.aday_mi(True, 80, None, 11.0, None), False)

print("11 · adayların sırası")
a = [(7, 300, 90, "S"), (3, 400, 80, "O"), (5, 300, 100, "O"),
     (2, 300, 100, "O")]
esit("önce O, sonra S; m, M, adres", [x[0] for x in L.sirala(a)], [2, 5, 3, 7])
a = [(4, 300, 70, "O"), (6, 300, 60, "O")]
esit("eşit m'de küçük M", [x[0] for x in L.sirala(a)], [6, 4])

print("12 · sınıflar")
esit("U1", L.sinif(False, False, False, True, True, False), "U1")
esit("U2: k1 yok", L.sinif(False, False, True, False, False, False), "U2")
esit("U2: k1 kirli", L.sinif(False, False, False, True, False, False), "U2")
esit("J5", L.sinif(True, True, True, True, True, True), "J5")
esit("J1", L.sinif(True, False, True, True, True, True), "J1")
esit("J2", L.sinif(True, False, False, True, True, True), "J2")
esit("J3: kanıt yok, k1 kirli", L.sinif(True, False, False, True, False,
                                        False), "J3")
esit("J3: kanıt var, O temiz değil", L.sinif(True, False, True, True, True,
                                             False), "J3")
esit("J4", L.sinif(True, False, False, False, False, False), "J4")

print("13 · tetikler ve sapma")
r = [(1, 7, False), (2, 3, True), (3, 7, True), (4, 7, False), (5, 2, True)]
esit("DEN7x1", L.tetik_anlari(r, [], "den", 1), [1, 3, 4])
esit("VAZ1", L.tetik_anlari(r, [], "vaz", 1), [1, 4])
esit("DEN7x2: kayan", L.tetik_anlari(r, [], "den", 2), [4])
r = [(1, 7, False), (2, 7, False), (3, 7, False)]
esit("DEN7x2: her ardışık ikilide", L.tetik_anlari(r, [], "den", 2), [2, 3])
esit("kendi aralığım sayımı sıfırlar",
     L.tetik_anlari(r, [(1.5, 2.5)], "den", 2), [])
esit("sapma aralıkları", L.sapma_araliklari([1.0, 1.5, 5.0], 1.0),
     [(1.0, 2.5), (5.0, 6.0)])
esit("altı aday", len(L.SAPMA_ADAYLARI), 6)

print("14 · alana giriş, p₇, temiz")
esit("dizinin başı", L.alan_girisi("UUGGGU", 1.5, 4.2), 2.0)
esit("dönemin başıyla sınırlı", L.alan_girisi("UUGGGU", 2.7, 4.2), 2.7)
esit("alan U", L.alan_girisi("UUGGGU", 1.5, 5.5), None)
esit("p₇(0,5)", L.p7(0.5), 1 - 0.5 ** 7)
esit("temiz", L.temiz("U", 0.95), True)
esit("temiz değil: alan", L.temiz("G", 0.99), False)
esit("temiz değil: bant", L.temiz("U", 0.85), False)
esit("temiz değil: ölçü yok", L.temiz("U", None), False)

print(f"\n{SAY[0]} denetim geçti")
