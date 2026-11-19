"""Faz 5-3 · 19 Kasım kodu · EŞDEĞERLİK: yeni kod 18 Kasım'ın bayraklarıyla
(`ESKI_CEKIRDEK` · eski tam sürüm, `DEGERLER_ESKI`) eski kodu birebir üretiyor
mu? Küçük test dünyası (12 düğüm, `tests2/test_desparete5.py`'nin dünyası);
ölçüm değil, kodun denetimi.

    PYTHONIOENCODING=utf-8 py -3.11 arsiv/teshis/faz5_3_kod_2026-11-19/esdegerlik.py <eski kod kökü>

Eski kod kökü: 18 Kasım'ın protokol kodunu taşıyan bir kopya (ör. açlık
teşhisinin dondurulmuş kopyası `arsiv/teshis/faz5_3_aclik_2026-11-18/kopya`,
commit 8c9bbf7; ya da `git worktree add <yol> 8c9bbf7`). Yeni kod: bu deponun
çalışma ağacı. Her koşu ayrı bir süreçte, kodun kendi kökünden yapılır.

Karşılaştırılan: korunum bölümü, sonuç satırının metrikleri, tanı
sayaçlarının toplamı. Eski kodda olmayan yeni sayaçlar (vazgeçme tetiği)
yeni kodda 0 olmalı.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

SENARYOLAR = ("statik-yok", "statik-surekli", "formasyon-yok",
              "formasyon-surekli")
PROFILLER = ("cekirdek", "tam")

COCUK = r'''
import json, math, sys
sys.path.insert(0, ".")
import protokoller.desparete5_bicim as B
from protokoller.desparete5 import Desparete5
from sim2.kosum.kosu import Kosu
from sim2.kosum.kurulum import kurulum_yap
from sim2.kosum.sonuc import korunum_bolumu, sonuc_satiri
from sim2.yapilandirma.konfig import Konfig

senaryo, profil = sys.argv[1], sys.argv[2]
yeni_kod = hasattr(B, "ESKI_CEKIRDEK")
if yeni_kod:
    deg = B.DEGERLER_ESKI
    bay = (B.ESKI_CEKIRDEK if profil == "cekirdek" else
           B.Bayraklar(vazgecme_tetigi=False, egim=False, duzgun_gecis=False,
                       veri_kotu_tetigi=True))
else:
    deg = None
    bay = B.CEKIRDEK if profil == "cekirdek" else B.TAM
V = Konfig(kol="t")
N = 12
EN = V.alan_en_m * (N / V.dugum_sayisi) ** 0.5
kfg = Konfig(kol="test", senaryo=senaryo, tohum=1000, isinma_s=50.0,
             olcum_bitis_s=70.0, kosu_bitis_s=75.0, dugum_sayisi=N,
             trafik_deseni="yere_toplama", alan_en_m=EN, alan_boy_m=EN,
             gorev_grup_sayisi=2, karistirici_baslangic_s=20.0,
             gorev_grup_yaricapi_m=(V.gorev_grup_yaricapi_m * EN
                                    / V.alan_en_m))
kur = kurulum_yap(kfg)
pr = []
def fabrika(i):
    p = Desparete5(i, kfg.gecit, bayraklar=bay, degerler=deg)
    pr.append(p)
    return p
kosu = Kosu(kur, fabrika)
kosu.kostur()
toplam = {}
for p in pr:
    t = p.teshis(p.kimlik)
    for ad in ("protokol", "bag", "rota", "selam", "kendi", "bekletme", "iz"):
        for k, v in zip(t[f"{ad}_adlari"], t[f"{ad}_sayac"]):
            toplam[f"{ad}.{k}"] = toplam.get(f"{ad}.{k}", 0) + v
satir = sonuc_satiri(kur, kosu.dugumler, "desparete5")
def temiz(x):
    if isinstance(x, float) and math.isnan(x):
        return "nan"
    if isinstance(x, dict):
        return {str(k): temiz(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [temiz(v) for v in x]
    return x
print(json.dumps({"yeni_kod": yeni_kod,
                  "korunum": temiz(korunum_bolumu(kur, kosu.dugumler)),
                  "metrikler": temiz(satir["metrikler"]),
                  "toplam": toplam}, sort_keys=True, default=str))
'''


def kos(kok: Path, senaryo: str, profil: str) -> dict:
    cikti = subprocess.run(
        [sys.executable, "-c", COCUK, senaryo, profil], cwd=kok,
        capture_output=True, text=True, encoding="utf-8",
        env={**__import__("os").environ, "PYTHONIOENCODING": "utf-8",
             "PYTHONDONTWRITEBYTECODE": "1"})
    if cikti.returncode != 0:
        raise SystemExit(f"{kok} {senaryo} {profil}:\n{cikti.stderr[-3000:]}")
    return json.loads(cikti.stdout.strip().splitlines()[-1])


def main() -> int:
    eski_kok = Path(sys.argv[1]).resolve()
    yeni_kok = Path(__file__).resolve().parents[3]
    print(f"eski kod: {eski_kok}\nyeni kod: {yeni_kok}")
    hepsi_ayni = True
    for senaryo in SENARYOLAR:
        for profil in PROFILLER:
            e = kos(eski_kok, senaryo, profil)
            y = kos(yeni_kok, senaryo, profil)
            assert not e["yeni_kod"] and y["yeni_kod"], "kökler karışmış"
            fark = []
            for bolum in ("korunum", "metrikler"):
                if e[bolum] != y[bolum]:
                    anahtar = sorted(k for k in set(e[bolum]) | set(y[bolum])
                                     if e[bolum].get(k) != y[bolum].get(k))
                    fark.append(f"{bolum}: {anahtar[:8]}")
            ortak = set(e["toplam"]) & set(y["toplam"])
            sayac_fark = sorted(k for k in ortak
                                if e["toplam"][k] != y["toplam"][k])
            eksik = sorted(set(e["toplam"]) - set(y["toplam"]))
            yeni_sifirdan_farkli = sorted(
                k for k in set(y["toplam"]) - set(e["toplam"])
                if y["toplam"][k] != 0)
            if sayac_fark:
                fark.append(f"sayaç: {sayac_fark[:8]}")
            if eksik:
                fark.append(f"yeni kodda olmayan sayaç: {eksik[:8]}")
            if yeni_sifirdan_farkli:
                fark.append(f"yeni sayaç 0 değil: {yeni_sifirdan_farkli}")
            ayni = not fark
            hepsi_ayni &= ayni
            pdr = e["metrikler"].get("pdr")
            print(f"{senaryo:<18} {profil:<9} PDR {pdr} · ortak sayaç "
                  f"{len(ortak)} · yeni sayaç "
                  f"{len(set(y['toplam']) - set(e['toplam']))} → "
                  + ("BİREBİR" if ayni else "FARKLI: " + " · ".join(fark)))
    print("SONUÇ:", "hepsi birebir" if hepsi_ayni else "FARK VAR")
    return 0 if hepsi_ayni else 1


if __name__ == "__main__":
    sys.exit(main())
