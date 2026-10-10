"""Faz 5.0 başlangıç çizgisi — mevcut kayıtlardan, simülasyon yok.

G1ç (karıştırıcısız ikiz, hayalet çizelge) ve G2ç (birincil hücre) kapı
koşularının KAYIT satırlarından `PDR_açık`, karıştırma kaybı (birincil −
ikiz) ve fark-içinde-fark (`06` §0.4.5). Kod K-224 (7 deneme, `OLSR-d`),
tohum 1003 · 1004, tam pencere.

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz5_0_2026-10-10/baslangic_cizgisi.py
"""
import json
import re
from pathlib import Path

KOK = Path(__file__).resolve().parents[3]
KAYNAK = KOK / "arsiv/teshis/denetim_duzeltme_2026-10-09"
KOLLAR = ("en_guvenilir_kahin", "aodv", "aomdv", "olsr", "desparete")
TOHUMLAR = (1003, 1004)


def kayitlar(yol: Path) -> list[dict]:
    metin = yol.read_text(encoding="utf-8")
    return [r for m in re.finditer(r"KAYIT (\[.*\])", metin)
            for r in json.loads(m.group(1))]


def main() -> None:
    rs = kayitlar(KAYNAK / "B3_G1c.txt") + kayitlar(KAYNAK / "B3_G2c.txt")
    P = {(r["senaryo"], r["protokol"], r["tohum"]): r["pdr_acik"] for r in rs}
    B, I = "formasyon-surekli", "formasyon-yok"
    print("PDR_acik: birincil | ikiz (hayalet cizelge) | karistirma kaybi")
    for p in KOLLAR:
        for s in TOHUMLAR:
            b, i = P[(B, p, s)], P[(I, p, s)]
            print(f"  {p:>20} {s}  {b:.3f} | {i:.3f} | {b - i:+.3f}")
    print("fark-icinde-fark: [D - R]_birincil - [D - R]_ikiz")
    for r in ("aodv", "aomdv", "olsr", "en_guvenilir_kahin"):
        dd = [(P[(B, "desparete", s)] - P[(B, r, s)])
              - (P[(I, "desparete", s)] - P[(I, r, s)]) for s in TOHUMLAR]
        print(f"  desparete - {r:<20} " + "  ".join(f"{s} {d:+.3f}"
                                                  for s, d in zip(TOHUMLAR,
                                                                  dd)))


if __name__ == "__main__":
    main()
