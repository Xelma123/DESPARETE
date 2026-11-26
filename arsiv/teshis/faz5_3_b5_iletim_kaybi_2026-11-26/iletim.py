"""
Faz 5-3 · B5 teşhisi — saf işlevler (`beklenti.md` "Tanımlar"). Simülatörü
bilmez; birim sınaması `sinama/saf.py`. Ölçüm aleti `olcum.py` ve karar hesabı
`sonuc_hesap.py` buradan içe aktarır.

Önceki teşhislerden DEĞİŞTİRİLMEDEN alınanlar:
  · B2 teşhisinin `isaret.py`'si: girişim işareti (`g_isareti`), giriş ve
    çıkış ardışıklığı (`durum`), B1'in selam sayımıyla selam kaybı payı
    (`bag_simule`, `selam_kaybi`);
  · B3 teşhisinin `bag.py`'si: B1'in selam sayımı ve `d_f`'si (`b1_selam`),
    `E_selam` (`e_selam`).

Buradakiler:
  1. B2'nin kendi durumu (kanal kilidi · girişim) ve kendi aralıklar (kural 2–8).
  2. B3'ün SON ÇARE sebepleri: bildirim (iki biçim), gönderici, veri yok
     (kural 5–8).
  3. B4'ün aday kümesi: ilanın ömrü, uygulanabilirlik, sıra (kural 1–5).
  4. Sınıflar (J1–J5, U1–U2) ve hızlı sapmanın tetikleri.

Zaman simülasyon saatidir (saniye); aralıklar yarı açık [başlangıç, bitiş).
"""

from __future__ import annotations

import bisect
import math
import sys
from pathlib import Path

BURASI = Path(__file__).resolve().parent
B2_KLASOR = BURASI.parent / "faz5_3_b2_isaretler_2026-11-24"
B3_KLASOR = BURASI.parent / "faz5_3_b3_bag_olculeri_2026-11-25"
for _y in (B2_KLASOR, B3_KLASOR):
    if str(_y) not in sys.path:
        sys.path.append(str(_y))

import bag as B1S  # noqa: E402  (B3 teşhisi)
import isaret as I  # noqa: E402  (B2 teşhisi)

# --- yeni tasarımın değerleri (`v2/bilesen/00-DIZIN.md`) ----------------------
ED_ESIK = 0.55                 # B2 kural 2
G_ALFA, G_BETA = 0.4, 0.6      # B2 kural 5
G_GIRIS, G_CIKIS = 2, 1        # B2 kural 6
ED_GIRIS, ED_CIKIS = 1, 1      # B2 kural 6 (kanal kilidi)
GK_DENEME, GK_ARDISIK = 7, 3   # B2 kural 12
KANIT_OMUR_S = 5.0             # B3 kural 6–7
VERI_YOK_N = 4                 # B3 kural 7
VERI_PENCERE_S = 30.0          # B1 kural 14 · B3 kural 7
ILAN_OMUR_KAT = 3.5            # B4 kural 4
MALIYET_BIRIM = 64             # B3 kural 2
SONLU_EN_COK, SONSUZ = 0xFFFE, 0xFFFF
ORNEK_EN_AZ = 4                # B1 kural 17 · B3 kural 1
T_SILME = 30.0                 # B1 kural 3
# --- teşhisin değerleri (`beklenti.md`) ----------------------------------------
DENEME = 7                     # referans dünyada MAC'in deneme sayısı (K-223)
IYI_P7 = 0.90                  # "iyi" bant: 7 denemelik başarı ≥ 0,90
TETIKLER = (("DEN7x1", "den", 1), ("VAZ1", "vaz", 1), ("DEN7x2", "den", 2))
PENCERELER = (1.0, 3.0)        # sapma süresi W (s)
SAPMA_ADAYLARI = tuple((ad, aile, n, W) for ad, aile, n in TETIKLER
                       for W in PENCERELER)          # altı aday (K3)
# Kanıt bit maskesi (karar satırı)
K_BILDIRIM_G, K_BILDIRIM_A, K_GONDERICI = 1, 2, 4
K_VERI_YOK, K_ILAN_BAYAT, K_KULLANILMAZ = 8, 16, 32
KANIT_A = K_BILDIRIM_A | K_GONDERICI | K_VERI_YOK | K_ILAN_BAYAT | K_KULLANILMAZ
KANIT_G = K_BILDIRIM_G | K_GONDERICI | K_VERI_YOK | K_ILAN_BAYAT | K_KULLANILMAZ

INF = math.inf


# ==============================================================================
# Aralıklar
# ==============================================================================
def aralik_ekle(out: list, bas: float, bitis: float) -> None:
    """Zaman sırasıyla gelen [bas, bitis)'i sıralı, ayrık listeye ekler;
    çakışan ya da bitişik olanla birleştirir."""
    if bitis <= bas:
        return
    if out and bas <= out[-1][1]:
        if bitis > out[-1][1]:
            out[-1] = (out[-1][0], bitis)
    else:
        out.append((bas, bitis))


def aralik_kes(out: list, t: float) -> None:
    """Son aralık t'yi kapsıyorsa t'de keser (boş kalırsa siler)."""
    if out and out[-1][0] <= t < out[-1][1]:
        if t <= out[-1][0]:
            out.pop()
        else:
            out[-1] = (out[-1][0], t)


def icinde(araliklar: list, t: float) -> bool:
    """t, sıralı ve ayrık [bas, bitis) aralıklarından birinde mi?"""
    k = bisect.bisect_right(araliklar, (t, INF)) - 1
    return k >= 0 and araliklar[k][0] <= t < araliklar[k][1]


def aralik_basi(araliklar: list, t: float) -> float | None:
    """t'yi kapsayan aralığın başı; kapsayan yoksa None."""
    k = bisect.bisect_right(araliklar, (t, INF)) - 1
    if k >= 0 and araliklar[k][0] <= t < araliklar[k][1]:
        return araliklar[k][0]
    return None


# ==============================================================================
# 1 · B2'nin kendi durumu ve kendi aralıklar
# ==============================================================================
def durum_dizileri(m: list[float], c: list[int], s: list[float | None]
                   ) -> tuple[str, list[bool], list[bool]]:
    """Saniye başına (kod, kanal kilidi alt durumu, girişim alt durumu).

    T'nin değeri T saniyesinin SONUNDA (T + 1'de) verilen karardır. Kod "E"
    kanal kilidi, "G" girişim, "-" yok; kanal kilidi önceliklidir (B2 kural 7).
    Kanal kilidi: m ≥ `ED_ESIK`, 1 s giriş ve çıkış. Girişim: c < α · c̄ ve
    s ≥ β, `G_GIRIS` ardışık işaretli saniyede giriş, `G_CIKIS` işaretsizde
    çıkış; c̄ işaretsiz saniyelerden (B2 kural 4; `isaret.g_isareti`).
    """
    n = len(m)
    sifir = [0] * n
    g_isaret = I.g_isareti(m, c, s, sifir, sifir, sifir, G_ALFA, G_BETA,
                           False)
    g = I.durum(g_isaret, G_GIRIS, G_CIKIS)
    ed = I.durum([x >= ED_ESIK for x in m], ED_GIRIS, ED_CIKIS)
    kod = "".join("E" if e else ("G" if gg else "-") for e, gg in zip(ed, g))
    return kod, ed, g


def kendi_araliklar(ed: list[bool], g: list[bool]) -> list[tuple[float, float]]:
    """B2 kural 8: durumun "yok" olmadığı her kesintisiz dönem bir aralıktır.

    Başlangıç geriye dönük: kanal kilidinde girişten 1 s, girişimde `G_GIRIS`
    s geriye (girişe yol açan işaretli saniyelerin ilkinin başı); iki alt
    durum aynı saniyede girerse erken olan. Bitiş: "yok"a dönülen saniyenin
    başı (son işaretli saniyenin sonu); dönem sürüyorsa ∞. Çakışan ya da
    bitişik aralıklar birleşir.
    """
    out: list[tuple[float, float]] = []
    n = len(ed)
    T = 0
    while T < n:
        if not (ed[T] or g[T]):
            T += 1
            continue
        aday = []
        if ed[T]:
            aday.append(T + 1 - ED_GIRIS)
        if g[T]:
            aday.append(T + 1 - G_GIRIS)
        bas = float(max(0, min(aday)))
        while T < n and (ed[T] or g[T]):
            T += 1
        bitis = float(T) if T < n else INF
        aralik_ekle(out, bas, bitis)
    return out


def durum_ani(kod: str, t: float) -> str:
    """t anında bilinen durum: son tamamlanan saniyenin (⌊t⌋ − 1) kararı."""
    T = math.floor(t) - 1
    return kod[T] if 0 <= T < len(kod) else "-"


def durum_bilinme_ani(kod: str, t: float) -> float | None:
    """t'de durum "yok" değilse, bu kesintisiz dönemin bilindiği an (dönemin
    ilk saniyesi T0'ın sonu, T0 + 1); "yok"sa None."""
    T = math.floor(t) - 1
    if not (0 <= T < len(kod)) or kod[T] == "-":
        return None
    while T - 1 >= 0 and kod[T - 1] != "-":
        T -= 1
    return float(T + 1)


# ==============================================================================
# 2 · B3'ün SON ÇARE sebepleri
# ==============================================================================
def bildirim_gercekci(selamlar: list[tuple[float, bool]],
                      duyulma: list[float]) -> list[tuple[float, float]]:
    """Bağ (i ← j), gerçekçi biçim (B2 kural 10–11, B3 kural 5).

    `selamlar`: j'nin i'ye ulaşan selamları [(an, bit)], zaman sırasında;
    `duyulma`: j'nin selam dışındaki duyulma anları (sıralı; i'nin j'ye
    onaylanan çerçeveleri). Bildirim bit 1'li selamla başlar, bit 0'lı selamla
    biter; j B1'de silinirse (son duyulmadan `T_SILME` sonra; B1 kural 3)
    silinme anında biter. Kayıt yeniden ilk selamla açılır.
    """
    olay = sorted([(t, 1, b) for t, b in selamlar]
                  + [(t, 0, None) for t in duyulma])
    out: list[tuple[float, float]] = []
    kayitli = False
    son = -INF
    bas: float | None = None
    for t, tur, bit in olay:
        if kayitli and t - son > T_SILME:           # silme
            if bas is not None:
                aralik_ekle(out, bas, son + T_SILME)
                bas = None
            kayitli = False
        if tur == 0:                                 # duyulma
            if kayitli:
                son = max(son, t)
            continue
        kayitli = True                               # selam
        son = max(son, t)
        if bit and bas is None:
            bas = t
        elif not bit and bas is not None:
            aralik_ekle(out, bas, t)
            bas = None
    if bas is not None:
        aralik_ekle(out, bas, son + T_SILME)
    return out


def gonderici_araliklari(kayitlar: list[tuple[float, int, bool]],
                         haric: list[tuple[float, float]]
                         ) -> list[tuple[float, float]]:
    """Bağ (i → j): B2 kural 12–13 ve B3 kural 6.

    `kayitlar` [(an, deneme 1–7, onay geldi mi)] zaman sırasında; `haric`
    kendi aralıklarım. Kendi aralığıma düşen kayıt sayılmaz ve sayımı
    sıfırlar. Art arda `GK_ARDISIK` tam denemeli (deneme == `GK_DENEME`)
    kayıtta olay e oluşur. e'den sonra her tam denemeli kayıt r kanıtı
    [r, r + `KANIT_OMUR_S`) uzatır (süresi dolmuş olsa da yeniden açar);
    tam denemesiz (başarılı) bir kayıt kanıtı o anda kaldırır ve sayım
    yeniden başlar.
    """
    out: list[tuple[float, float]] = []
    sayim = 0
    zincir = False
    for t, den, _ok in kayitlar:
        if icinde(haric, t):
            sayim = 0
            continue
        tam = den >= GK_DENEME
        if zincir:
            if tam:
                aralik_ekle(out, t, t + KANIT_OMUR_S)
            else:
                aralik_kes(out, t)
                zincir = False
                sayim = 0
            continue
        if tam:
            sayim += 1
            if sayim >= GK_ARDISIK:
                zincir = True
                aralik_ekle(out, t, t + KANIT_OMUR_S)
        else:
            sayim = 0
    return out


def veri_yok_araliklari(kayitlar: list[tuple[float, int, bool]],
                        haric: list[tuple[float, float]]
                        ) -> list[tuple[float, float]]:
    """Bağ (i → j): B3 kural 7.

    Kendi aralığıma düşmeyen kayıtların son `VERI_YOK_N`'i (son
    `VERI_PENCERE_S` içinde) hepsi vazgeçme ve en yenisi `KANIT_OMUR_S`
    içinde ise etkin. k'ıncı kayıttan başlayan aralık, bir sonraki kayda, en
    yeninin ömrüne ve en eskinin pencereden çıkışına kadar sürer.
    """
    gec = [(t, ok) for t, _den, ok in kayitlar if not icinde(haric, t)]
    out: list[tuple[float, float]] = []
    for k in range(VERI_YOK_N - 1, len(gec)):
        son = gec[k - VERI_YOK_N + 1:k + 1]
        if any(ok for _, ok in son):
            continue
        t_k = gec[k][0]
        bitis = min(t_k + KANIT_OMUR_S, son[0][0] + VERI_PENCERE_S)
        if k + 1 < len(gec):
            bitis = min(bitis, gec[k + 1][0])
        aralik_ekle(out, t_k, bitis)
    return out


# ==============================================================================
# 3 · B4'ün aday kümesi
# ==============================================================================
def sira_buyuk(a: int, b: int) -> bool:
    """16 bitlik modüler karşılaştırma: a, b'den yeni mi?"""
    f = (a - b) & 0xFFFF
    return 0 < f < 0x8000


def uygulanabilir(tur: int, C: int, fd: tuple[int, int] | None) -> bool:
    """B4 kural 1 (RFC 8966 §3.5.1)."""
    if C >= SONSUZ or fd is None:
        return True
    return sira_buyuk(tur, fd[0]) or (tur == fd[0] and C < fd[1])


def maliyet_M(e: float | None) -> int:
    """B3 kural 2: M = min(⌈64 · E⌉, 0xFFFE); ∞ ya da tanımsız → 0xFFFF.
    Yuvarlama bugünkü kodun birimiyle aynı (`maliyet_birimi`)."""
    if e is None or math.isinf(e):
        return SONSUZ
    return min(SONLU_EN_COK, max(0, math.ceil(e * MALIYET_BIRIM - 1e-9)))


def maliyet_topla(a: int, b: int) -> int:
    """B4 kural 2: biri ∞ ise ∞; 0xFFFE'de doyar."""
    if a >= SONSUZ or b >= SONSUZ:
        return SONSUZ
    return min(SONLU_EN_COK, a + b)


def ilan_taze(t: float, ilan_t: float, aralik_s: float) -> bool:
    """B4 kural 4: son ilan `ILAN_OMUR_KAT` · a'dan eski değil."""
    return t - ilan_t <= ILAN_OMUR_KAT * max(aralik_s, B1S.ARALIK_EN_AZ)


def aday_mi(kayitli: bool, M: int, ilan: tuple | None, t: float,
            fd: tuple[int, int] | None) -> bool:
    """B4 kural 3: kayıtlı, kullanılır (M sonlu), ilanı taze ve sonlu,
    uygulanabilir, yol maliyeti sonlu. `ilan` (an, tur, C, aralık)."""
    if not kayitli or M >= SONSUZ or ilan is None:
        return False
    ilan_t, tur, C, aralik = ilan
    if C >= SONSUZ or not ilan_taze(t, ilan_t, aralik):
        return False
    if not uygulanabilir(tur, C, fd):
        return False
    return maliyet_topla(M, C) < SONSUZ


def sirala(adaylar: list[tuple[int, int, int, str]]
           ) -> list[tuple[int, int, int, str]]:
    """B4 kural 5'in sırası. Aday (k, m, M, sınıf): önce O, sonra S; sınıf
    içinde m, eşitlikte küçük M, sonra küçük adres."""
    return sorted(adaylar,
                  key=lambda x: (0 if x[3] == "O" else 1, x[1], x[2], x[0]))


# ==============================================================================
# 4 · Sınıflar ve tetikler
# ==============================================================================
def p7(p: float) -> float:
    """7 denemelik başarı 1 − (1 − p)^7."""
    return 1.0 - (1.0 - p) ** DENEME


def temiz(alan: str, p7_: float | None) -> bool:
    """Temiz aday: alanı U ve bağı iyi bantta (p₇ ≥ 0,90)."""
    return alan == "U" and p7_ is not None and p7_ >= IYI_P7


def sinif(karisik: bool, gecit: bool, kanit: bool, k1_var: bool,
          k1_temiz: bool, en_o_temiz: bool) -> str:
    """`beklenti.md` "Sınıflar". `karisik`: alıcı karar anında E ya da G
    (karıştırıcı açık); `kanit`: ardılın kanıtı; `en_o_temiz`: en iyi O
    adayı var ve temiz."""
    if not karisik:
        return "U1" if (k1_var and k1_temiz) else "U2"
    if gecit:
        return "J5"
    if kanit and en_o_temiz:
        return "J1"
    if not k1_var:
        return "J4"
    if not kanit and k1_temiz:
        return "J2"
    return "J3"


def tetik_anlari(kayitlar: list[tuple[float, int, bool]],
                 haric: list[tuple[float, float]], aile: str, n: int
                 ) -> list[float]:
    """Kayan tetik: kendi aralığıma düşmeyen kayıtlarda, son n'inin hepsi kötü
    olduğu her kayıt. "den": deneme == `DENEME` (tam denemeli); "vaz":
    vazgeçme. Kendi aralığıma düşen kayıt sayımı sıfırlar."""
    out: list[float] = []
    ardisik = 0
    for t, den, ok in kayitlar:
        if icinde(haric, t):
            ardisik = 0
            continue
        kotu = (den >= DENEME) if aile == "den" else (not ok)
        ardisik = ardisik + 1 if kotu else 0
        if ardisik >= n:
            out.append(t)
    return out


def sapma_araliklari(anlar: list[float], W: float) -> list[tuple[float, float]]:
    """Her tetikten sonra [t, t + W) (birleşik)."""
    out: list[tuple[float, float]] = []
    for t in anlar:
        aralik_ekle(out, t, t + W)
    return out


def alan_girisi(z: str, donem_bas: float, t: float) -> float | None:
    """Alıcının bu dönemde alana (E ya da G) girişi: ⌊t⌋ saniyesini içeren
    E/G dizisinin başı, dönemin başıyla sınırlı. ⌊t⌋'de alan U ise None."""
    T = math.floor(t)
    if not (0 <= T < len(z)) or z[T] not in "EG":
        return None
    ilk = math.floor(donem_bas)
    while T - 1 >= ilk and z[T - 1] in "EG":
        T -= 1
    return max(float(T), donem_bas)
