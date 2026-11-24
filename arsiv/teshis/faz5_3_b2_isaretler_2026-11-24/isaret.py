"""
Faz 5-3 · B2 teşhisi — saf işlevler (`beklenti.md` "Tanımlar"). Simülatörü
bilmez; birim sınaması `sinama/saf.py`. Ölçüm aleti `olcum.py` ve karar hesabı
`sonuc_hesap.py` buradan içe aktarır.

1. `bag_simule`: B1'in selam sayımı (`v2/bilesen/B1-KOMSU-VE-BAG.md` kural
   4–6, 20) bir bağ için (alıcı i, j'nin selamlarını sayar). Saniye sınırlarında
   NEDENSEL anlık görüntü (o anda kayıtta olan örnekler) ve her zaman aşımı
   sıfırında sessizlik bilgisi.
2. Göndericinin bağ kuralları: VAZ · DEN · BIR (veri çerçevelerinden), SES
   (komşunun selam sessizliğinden).
3. Kendi durumum kuralları: ED · G · GM (düğüm-saniye dizilerinden), giriş ve
   çıkış ardışıklığıyla.

Değerler B1'inkilerdir (`v2/bilesen/00-DIZIN.md`); B2'nin adaylarının ızgarası
`beklenti.md`dedir ve burada `KURALLAR`/`IZGARA` olarak durur.
"""

from __future__ import annotations

import bisect
import math
from collections import deque

# --- B1'in değerleri (`v2/bilesen/00-DIZIN.md`) -------------------------------
ZAMAN_ASIMI_KATSAYI = 1.5
ARALIK_EN_AZ = 0.01
BOSLUK_EN_COK = 64
N_SELAM = 16
SELAM_SAKLA = 128
T_SILME = 30.0
# --- önceki KK-03 kural 2'nin tanımları (B2'nin adayları için başlangıç) -----
KAYIP_PENCERE_S = 4.0         # selam kaybı payının penceresi
TANIDIK_S = 16.0              # "tanıdık": son 16 s'de gerçek selamı alınmış
ED_ISARETSIZ = 0.62           # c̄'nin "işaretsiz saniye"si için ED işareti
ORTALAMA_SANIYE = 30          # c̄: son 30 işaretsiz saniye
KULLANILABILIR_DR = 0.5       # SES biriminin koşulu: sessizlikten önce d_r ≥ 0,5

INF = math.inf


def sira_farki(yeni: int, eski: int) -> int:
    """(yeni − eski) mod 2^16, [−32768, 32767] aralığına çevrilmiş."""
    f = (yeni - eski) & 0xFFFF
    return f - 0x10000 if f >= 0x8000 else f


def _ekle(o: list, t: float, v: int) -> None:
    """Zaman sıralı örnek listesine ekler; `SELAM_SAKLA`'yı aşan en eski atılır."""
    if not o or o[-1][0] <= t:
        o.append((t, v))
    else:
        bisect.insort(o, (t, v))
    if len(o) > SELAM_SAKLA:
        del o[0]


def sondaki(o: list) -> tuple[int, float | None, float | None]:
    """(sondaki ardışık sıfır sayısı, ilkinin anı, sessizlikten önceki d_r):
    d_r, sondaki sıfırlar hariç en yeni `N_SELAM` örnekten; yoksa None."""
    i = len(o)
    while i and o[i - 1][1] == 0:
        i -= 1
    n = len(o) - i
    ilk = o[i][0] if n else None
    once = o[max(0, i - N_SELAM):i]
    dr = sum(v for _, v in once) / len(once) if once else None
    return n, ilk, dr


def k_uyarlanir(dr: float | None) -> int:
    """Önceki KK-03 kural 6: k = min(N, max(3, ⌈log 0,01 / log(1 − d_r)⌉))."""
    if dr is None or dr <= 0.0:
        return N_SELAM
    if dr >= 1.0:
        return 3
    x = math.log(0.01) / math.log(1.0 - dr)
    return min(N_SELAM, max(3, math.ceil(x - 1e-9)))


def bag_simule(gelisler: list[tuple[float, int, float]], son_s: float):
    """Bir bağın (alıcı i ← gönderen j) B1 sayımı.

    `gelisler`: [(an, sıra, ilan edilen aralık s)], zaman sırasında.
    Döner `(goruntu, sifirlar)`:
      goruntu[T] — T anında (T tamsayı, 0…⌊son_s⌋) kayıt varsa
          (n1, n0, sondaki, dr_once, son_selam_t, a): son `KAYIP_PENCERE_S`
          içindeki (T−4, T] 1 ve 0 örnek sayısı, sondaki ardışık sıfır,
          sessizlikten önceki d_r, son gerçek selamın anı, ilan edilen aralık;
          kayıt yoksa None;
      sifirlar — her zaman aşımı sıfırında (an, sondaki, dr_once).
    Sıra kural 20'dir: aynı anda önce zaman aşımı, sonra silme, en son geliş.
    Silme yalnız selamlardan (`T_SILME` boyunca selam yok); veri çerçevesi
    duyulması kaydı tazelemez (beyan: teşhisin yaklaşığı).
    """
    S = int(math.floor(son_s))
    goruntu: list = [None] * (S + 1)
    sifirlar: list = []
    o: list = []
    beklenen = None
    son_t = a = None
    asim = sil = INF
    gi, n = 0, len(gelisler)
    for T in range(S + 1):
        while True:
            t_g = gelisler[gi][0] if gi < n else INF
            t_a = asim if asim < sil else INF
            t_ev = min(t_g, t_a, sil)
            if t_ev > T:
                break
            if t_a <= t_g and t_a <= sil:            # zaman aşımı (kural 5)
                _ekle(o, asim, 0)
                beklenen = (beklenen + 1) & 0xFFFF
                sk, _, dr = sondaki(o)
                sifirlar.append((asim, sk, dr))
                asim += a
            elif sil <= t_g:                         # silme (kural 3)
                o = []
                beklenen = son_t = a = None
                asim = sil = INF
            else:                                    # selam (kural 4)
                t, sira, aralik = gelisler[gi]
                gi += 1
                aralik = max(float(aralik), ARALIK_EN_AZ)
                if beklenen is None:
                    o = [(t, 1)]
                else:
                    fark = sira_farki(sira, beklenen)
                    if fark == 0:
                        _ekle(o, t, 1)
                    elif 0 < fark <= BOSLUK_EN_COK:
                        for k in range(1, fark + 1):
                            _ekle(o, son_t + k * (t - son_t) / (fark + 1), 0)
                        _ekle(o, t, 1)
                    elif -BOSLUK_EN_COK <= fark < 0:
                        del o[max(0, len(o) + fark):]
                        _ekle(o, t, 1)
                    else:
                        o = [(t, 1)]
                beklenen = (sira + 1) & 0xFFFF
                son_t, a = t, aralik
                asim = t + ZAMAN_ASIMI_KATSAYI * a
                sil = t + T_SILME
        if beklenen is not None:
            alt = bisect.bisect_right(o, (T - KAYIP_PENCERE_S, 2))
            n1 = sum(v for _, v in o[alt:])
            n0 = len(o) - alt - n1
            sk, _, dr = sondaki(o)
            goruntu[T] = (n1, n0, sk, dr, son_t, a)
    return goruntu, sifirlar


def selam_kaybi(goruntuler: list, T: int) -> float | None:
    """Düğümün T anındaki selam kaybı payı: tanıdık komşuların (son gerçek
    selamı T − `TANIDIK_S`'den yeni) son `KAYIP_PENCERE_S`'deki örneklerinde
    sıfırların payı (önceki KK-03 kural 2'nin B1 sayımıyla hâli)."""
    gelen = kacan = 0
    for g in goruntuler:
        x = g[T] if T < len(g) else None
        if x is None or x[4] < T - TANIDIK_S:
            continue
        gelen += x[0]
        kacan += x[1]
    toplam = gelen + kacan
    return kacan / toplam if toplam else None


# ==============================================================================
# Göndericinin bağ kuralları
# ==============================================================================
def _kurallar() -> tuple[tuple[str, str, tuple], ...]:
    k: list = [(f"VAZ{n}", "vaz", (n,)) for n in (1, 2, 3)]
    k += [(f"DEN{a}x{r}", "den", (a, r)) for a in (4, 5, 6, 7) for r in (1, 2, 3)]
    k += [(f"BIR{a}_{int(x * 10)}x{r}", "bir", (a, x, r))
          for a in (4, 6) for x in (1.0, 1.5) for r in (1, 2)]
    k += [(f"SES{n}", "ses", (n,)) for n in (2, 3, 4)] + [("SESu", "ses", (None,))]
    return tuple(k)


KURALLAR = _kurallar()                     # (ad, aile, parametreler)
VERI_KURALLARI = tuple(k for k in KURALLAR if k[1] != "ses")
SES_KURALLARI = tuple(k for k in KURALLAR if k[1] == "ses")


def son_selam(gelis_t: list[float], gelis_a: list[float], t: float
              ) -> tuple[float | None, float | None]:
    """t anından önceki (≤ t) son selamın anı ve ilan ettiği aralık."""
    i = bisect.bisect_right(gelis_t, t)
    return (gelis_t[i - 1], gelis_a[i - 1]) if i else (None, None)


def veri_ates(cerceveler: list[tuple[float, int, bool]],
              gelis_t: list[float], gelis_a: list[float]) -> dict[str, list]:
    """Veri kurallarının ateşlenme anları. `cerceveler` [(an, deneme 1–7,
    onay geldi mi)] zaman sırasında; `gelis_*` göndericinin bu komşudan aldığı
    selamlar (BIR'in "selam gecikti" koşulu için). Bir kural, koşulunun art
    arda sağlandığı dizinin eşiğe ULAŞTIĞI çerçevede bir kez ateşlenir; dizi
    kırılınca yeniden sayılır."""
    ates: dict[str, list] = {ad: [] for ad, _, _ in VERI_KURALLARI}
    dizi = {ad: 0 for ad, _, _ in VERI_KURALLARI}
    for t, den, gitti in cerceveler:
        st = sa = None
        for ad, aile, p in VERI_KURALLARI:
            if aile == "vaz":
                kosul, esik = (not gitti), p[0]
            elif aile == "den":
                kosul, esik = den >= p[0], p[1]
            else:
                if st is None:
                    st, sa = son_selam(gelis_t, gelis_a, t)
                gecikti = (st is None or t - st > T_SILME
                           or t - st > p[1] * sa)
                kosul, esik = (den >= p[0] and gecikti), p[2]
            dizi[ad] = dizi[ad] + 1 if kosul else 0
            if dizi[ad] == esik:
                ates[ad].append(t)
    return ates


def ses_ates(sifirlar: list) -> dict[str, list]:
    """SES kurallarının ateşlenme anları ve o andaki dr_once:
    ad → [(an, dr_once)]. SESn sondaki sıfır n'ye ulaşınca, SESu
    `k_uyarlanir(dr_once)`'a ulaşınca ateşlenir."""
    ates: dict[str, list] = {ad: [] for ad, _, _ in SES_KURALLARI}
    for t, sk, dr in sifirlar:
        for ad, _, p in SES_KURALLARI:
            esik = k_uyarlanir(dr) if p[0] is None else p[0]
            if sk == esik:
                ates[ad].append((t, dr))
    return ates


def ilk_ates(anlar: list, bas: float, bitis: float) -> float | None:
    """[bas, bitis) içindeki ilk ateşlenmenin bas'tan gecikmesi (yoksa None)."""
    for t in anlar:
        t0 = t[0] if isinstance(t, tuple) else t
        if bas <= t0 < bitis:
            return t0 - bas
        if t0 >= bitis:
            break
    return None


# ==============================================================================
# Kendi durumum kuralları (düğüm-saniye dizileri)
# ==============================================================================
def g_isareti(m: list[float], c: list[int], s: list[float | None],
              a: list[int], f: list[int], k: list[int],
              alfa: float, beta: float, oy: bool) -> list[bool]:
    """Her saniyenin girişim işareti. C: c < alfa·c̄ · S: s ≥ beta ·
    M: en az 2 ayrı komşuya başarısız deneme ve başarısız deneme payı ≥ 0,5.
    G (oy=False): C ve S. GM (oy=True): üçünden en az ikisi.
    c̄: son `ORTALAMA_SANIYE` işaretsiz saniyenin c ortalaması (işaretsiz:
    ne m ≥ `ED_ISARETSIZ` ne bu işaret; 30'dan azsa olanların, hiç yoksa
    tanımsız ve C yok) — önceki KK-03 kural 1, 3."""
    gecmis: deque = deque(maxlen=ORTALAMA_SANIYE)
    toplam = 0.0
    out: list[bool] = []
    for T in range(len(c)):
        cbar = toplam / len(gecmis) if gecmis else None
        C = cbar is not None and c[T] < alfa * cbar
        S = s[T] is not None and s[T] >= beta
        if oy:
            M = k[T] >= 2 and a[T] > 0 and f[T] >= 0.5 * a[T]
            isaret = (C + S + M) >= 2
        else:
            isaret = C and S
        if not isaret and m[T] < ED_ISARETSIZ:
            if len(gecmis) == gecmis.maxlen:
                toplam -= gecmis[0]
            gecmis.append(c[T])
            toplam += c[T]
        out.append(isaret)
    return out


def durum(isaret: list[bool], kin: int, kout: int) -> list[bool]:
    """Saniye sonundaki durum: `kin` ardışık işaretli saniye tamamlanınca
    girilir, `kout` ardışık işaretsiz saniye tamamlanınca çıkılır."""
    out: list[bool] = []
    icinde = False
    ardisik_var = ardisik_yok = 0
    for x in isaret:
        if x:
            ardisik_var += 1
            ardisik_yok = 0
        else:
            ardisik_yok += 1
            ardisik_var = 0
        if not icinde and ardisik_var >= kin:
            icinde = True
        elif icinde and ardisik_yok >= kout:
            icinde = False
        out.append(icinde)
    return out


def donem_olcusu(dur: list[bool], bas: float, bitis: float,
                 sonraki_bas: float | None) -> tuple[float | None, float | None]:
    """Bir açık dönem için (giriş gecikmesi, çıkış gecikmesi).
    Giriş: [⌊bas⌋, bitis) içinde durumda olunan ilk saniye T; kararın anı
    T + 1 (saniye sonu), gecikme max(0, T + 1 − bas); karar bitis'ten sonraysa
    None. Çıkış: girilmişse, ⌊bitis⌋'ten sonra durumda OLUNMAYAN ilk saniye
    T; gecikme T + 1 − bitis; sonraki dönemin başına kadar çıkılmazsa None."""
    giris = None
    for T in range(int(math.floor(bas)), len(dur)):
        if T + 1 > bitis + 1e-9:
            break
        if dur[T]:
            giris = max(0.0, T + 1 - bas)
            break
    if giris is None:
        return None, None
    ust = len(dur) if sonraki_bas is None else int(math.floor(sonraki_bas))
    for T in range(int(math.floor(bitis)), min(ust, len(dur))):
        if not dur[T]:
            return giris, T + 1 - bitis
    return giris, None


def izgara() -> list[tuple]:
    """Kendi durumum kurallarının ızgarası (`beklenti.md`):
    ("ED", θ) · ("G"|"GM", α, β, kin, kout)."""
    k: list = [("ED", th) for th in (0.50, 0.55, 0.60, 0.62, 0.65, 0.70, 0.80)]
    for aile in ("G", "GM"):
        for al in (0.4, 0.5, 0.6, 0.7):
            for be in (0.5, 0.6, 0.7, 0.8):
                for kin in (1, 2, 3):
                    for kout in (1, 2, 3):
                        k.append((aile, al, be, kin, kout))
    return k


ESKI_KURAL = ("G", 0.5, 0.6, 2, 3)        # önceki KK-03'ün kuralı (kıyas için)
