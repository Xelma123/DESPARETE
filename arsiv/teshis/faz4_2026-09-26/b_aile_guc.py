"""4.1b · Aile × güç, "büyük bölünme" ile (ajan, K-186) — 35 km referans.

Her aile ve taban güçte: ρ, ulaşılabilirlik, eski AYRILAN (birden fazla çok
üyeli bileşen) ve BÜYÜK bölünme (ikinci bileşen ≥ N/10 = 4 İHA) tohum sayısı,
en kötü anın en büyük bileşeni. 30 tohum × 9 an, sürekli sınıf.

    PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
        python -u arsiv/teshis/faz4_2026-09-26/b_aile_guc.py <kod_koku>
"""
import os
import sys

KOD = sys.argv[1] if len(sys.argv) > 1 else os.environ["FAZ4_KOD_KOKU"]
os.environ["FAZ4_KOD_KOKU"] = KOD
sys.path.insert(0, KOD)

AILELER = ("tekli_merkez", "hava_eslik", "cephe_hatti", "hedef_koruma",
           "derin_sizma")
GUCLER = (20.0, 25.0, 30.0, 33.0, 37.0, 40.0, 44.0, 47.0)

if __name__ == "__main__":
    os.environ["DESPARETE_DUNYA"] = "referans_2026"
    import kalibrasyon.karistirici_gucu as KG
    print(f"kod: {KOD}")
    print(f"{'aile':>13} {'guc':>5} {'rho':>6} {'ulas':>6} {'AYRILAN':>8} "
          f"{'BUYUK':>6} {'enbuyuk_min':>11}")
    for aile in AILELER:
        for guc in GUCLER:
            s = KG._olc_tohumlar("statik-surekli", guc, aile)
            print(f"{aile:>13} {guc:>5.0f} {s['rho']:>6.3f} "
                  f"{s['ulasilabilirlik']:>6.3f} "
                  f"{int(s['ayrilan_tohum']):>5}/30 "
                  f"{int(s['buyuk_ayrilan_tohum']):>3}/30 "
                  f"{s['en_buyuk_min']:>11.3f}", flush=True)
