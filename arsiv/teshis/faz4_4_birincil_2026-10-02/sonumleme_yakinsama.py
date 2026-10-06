"""Kâhinin sönümleme örnek sayısı yakınsıyor mu? (Faz 4.4, K-214)

    TESHIS_KOK=<kopya> PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
        py -3.11 -u arsiv/teshis/faz4_4_birincil_2026-10-02/sonumleme_yakinsama.py

Neden: T2 taramasında `kahin.py::SONUMLEME_ORNEGI` DUYARLI çıktı ve ETX
kâhininin (U1 paydası) kendisini oynattı: 6 → 3 örnek pdr_etx −0,060, 6 → 12
örnek +0,030 (band 14,7×). Örnek sayısı kâhinin bağ başına ortalama başarı
KESTİRİMİNİN örneklemidir — bir dünya parametresi değil, sayısal bir
parametre; değeri yakınsadığı yerde seçilmelidir.

Koşular: ETX kâhini · iki hücre (birincil; U1'in en sınırdaki hareketli
hücresi `bagimsiz-yok` yere toplama) · N = 6 · 12 · 24 · 48 · tohum
1000–1004 · duyarlılık taramasının kısa penceresi (40 koşu).

Ölçüt ölçmeden: hücre başına N → 2N adımında tohum başına farkın ortalaması
|Δ| < R (0,0188) VE |Δ| ≤ band (2·SD/√5) ise N'de PLATO. En küçük platolu N
raporlanır; 48'e kadar plato yoksa YAKINSAMADI (sonraki adım 96).
Hüküm öğrencinindir: sabit platoya çekilirse ETX kâhininin bütün sayıları
(U1 paydası, G2ç, çözünürlük R) değişir — statik kol hariç (orada tek örnek).
"""
import os
import pathlib
import statistics as ist
import sys
import time
from multiprocessing import Pool

KOK = pathlib.Path(os.environ.get("TESHIS_KOK")
                   or pathlib.Path(__file__).resolve().parents[3])
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))
os.environ["DESPARETE_DUNYA"] = "referans_2026"

from kalibrasyon import duyarlilik as D  # noqa: E402

AD = "kalibrasyon/kahin.py::SONUMLEME_ORNEGI"
HUCRELER = {"birincil": ("formasyon-surekli", D.HUCRE_EKLERI["birincil"]),
            "bagimsiz-yok": ("bagimsiz-yok", {"trafik_deseni": "yere_toplama"})}
N_DEGERLERI = (6, 12, 24, 48)
TOHUMLAR = (1000, 1001, 1002, 1003, 1004)


def _is(gorev):
    hucre, n, tohum = gorev
    senaryo, ek = HUCRELER[hucre]
    t0 = time.perf_counter()
    sonuc, hata = D._is((senaryo, tohum, "en_guvenilir_kahin", {**ek, AD: n}))
    return gorev, sonuc, hata, time.perf_counter() - t0


def main() -> None:
    gorevler = [(h, n, t) for h in HUCRELER for n in N_DEGERLERI for t in TOHUMLAR]
    print(f"kopya: {KOK}\ntoplam kosu {len(gorevler)} · 8 isci · R {D.R_ESLESTIRILMIS}")
    t0 = time.perf_counter()
    with Pool(8) as havuz:
        ham = havuz.map(_is, gorevler, chunksize=1)
    print(f"sure {(time.perf_counter() - t0) / 60:.1f} dk\n")
    pdr, sure = {}, {}
    for gorev, sonuc, hata, s in ham:
        if hata:
            print("  HATA", gorev, hata)
            continue
        pdr[gorev] = sonuc[0]
        sure.setdefault(gorev[:2], []).append(s)
    for h in HUCRELER:
        print(f"== {h}")
        for n in N_DEGERLERI:
            d = [pdr[(h, n, t)] for t in TOHUMLAR if (h, n, t) in pdr]
            print(f"  N {n:>2}: pdr_etx {ist.mean(d):.4f}  "
                  f"(tohumlar {' '.join(f'{x:.3f}' for x in d)})  "
                  f"kosu {ist.mean(sure[(h, n)]) / 60:.1f} dk")
        plato = None
        for n, n2 in zip(N_DEGERLERI, N_DEGERLERI[1:]):
            fark = [pdr[(h, n2, t)] - pdr[(h, n, t)] for t in TOHUMLAR
                    if (h, n, t) in pdr and (h, n2, t) in pdr]
            if len(fark) < len(TOHUMLAR):
                print(f"  {n}→{n2}: eksik tohum")
                continue
            ort = ist.mean(fark)
            band = 2 * ist.stdev(fark) / len(fark) ** 0.5
            ok = abs(ort) < D.R_ESLESTIRILMIS and abs(ort) <= band
            print(f"  {n:>2}→{n2:>2}: Δ {ort:+.4f}  band {band:.4f}  "
                  f"{'PLATO' if ok else 'degisiyor'}")
            if ok and plato is None:
                plato = n
        print(f"  → {'en kucuk platolu N = ' + str(plato) if plato else 'YAKINSAMADI (48e kadar)'}\n")


if __name__ == "__main__":
    main()
