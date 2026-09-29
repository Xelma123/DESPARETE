"""4.1 · Alan × karıştırıcı gücü ortak taraması (ajan, K-185).

Soru: kaynak bandındaki karıştırıcı (İHA taşıyıcılı 1–5 W) ağı BÖLMEDEN
kısmi karıştırma yapıyorken çok atlamalılık hangi alanda en büyük? 35 km
(bağlılığın kenarı) 20 dBm'de bile bölünüyordu (`b_karistirici_tarama.txt`).

Ölçüm `karistirici_gucu.olc` ile AYNI (ρ, ulaşılabilirlik, boğulan, ayrılan
tohum; 30 tohum × 9 an; kâhin grafiği ED susturması dâhil). Sınıf sürekli,
aile `tekli_merkez` (en kötü durum: merkezde).

    PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
        python -u arsiv/teshis/faz4_2026-09-26/b_alan_guc.py <kod_koku>
"""
import os
import sys

KOD = sys.argv[1] if len(sys.argv) > 1 else os.environ["FAZ4_KOD_KOKU"]
os.environ["FAZ4_KOD_KOKU"] = KOD          # havuz işçileri de görsün
sys.path.insert(0, KOD)

ALANLAR = (10000.0, 15000.0, 20000.0, 25000.0, 30000.0)
GUCLER = (30.0, 33.0, 37.0)

if __name__ == "__main__":
    os.environ["DESPARETE_DUNYA"] = "referans_2026"
    import kalibrasyon.karistirici_gucu as KG
    print(f"kod: {KOD}")
    print(f"{'alan_km':>8} {'guc':>6} {'rho':>7} {'ulas':>7} {'bogulan':>8} "
          f"{'AYRILAN':>9}")
    for alan in ALANLAR:
        os.environ["DESPARETE_ALAN_M"] = repr(alan)
        for guc in GUCLER:
            s = KG.olc("surekli", guc)
            print(f"{alan / 1000:>8.0f} {guc:>6.1f} {s['rho']:>7.3f} "
                  f"{s['ulasilabilirlik']:>7.3f} {s['yalniz_dugum']:>8.2f} "
                  f"{int(s['ayrilan_tohum']):>6}/30", flush=True)
