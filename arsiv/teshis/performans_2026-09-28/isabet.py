"""Sönümleme kazancı için saf önbelleğin isabet oranı ne olurdu? (ajan, 28 Eylül)

Birincil hücre, AODV, 1003, karıştırıcı 1 s'de açılır, 4 s koşu. Kod
DEĞİŞTİRMEZ: `Sonumleme.guc_kazanci` ve `karistirici_kazanci` bu süreçte
sarılır ve anahtarlar sayılır — anahtar, değerin bağlı olduğu TAM girdi:
(uçlar, parça k, ρ, M). Aynı anahtar aynı değeri verir (saf fonksiyon).
"""
import math
import os
import pathlib
import sys
import time
from collections import Counter

KOK = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KOK))
os.environ["DESPARETE_DUNYA"] = "referans_2026"

from kalibrasyon import dunya_secimi as DS  # noqa: E402
from kalibrasyon.aodv_uygunluk import _fabrika  # noqa: E402
from sim2.kanal import sonumleme as S  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402

anahtar_d, anahtar_k = Counter(), Counter()
asil_g, asil_k = S.Sonumleme.guc_kazanci, S.Sonumleme.karistirici_kazanci


def g(self, i, j, t_s):
    alt, ust = (i, j) if i <= j else (j, i)
    k = int(math.floor(t_s / self._dt))
    tc = self.tutarlilik_suresi_s(alt, ust, t_s)
    anahtar_d[(alt, ust, k, tc)] += 1
    return asil_g(self, i, j, t_s)


def kk(self, kimlik, dugum, t_s, v):
    k = int(math.floor(t_s / self._dt))
    anahtar_k[(kimlik, dugum, k, v)] += 1
    return asil_k(self, kimlik, dugum, t_s, v)


S.Sonumleme.guc_kazanci = g
S.Sonumleme.karistirici_kazanci = kk
kfg = DS.konfig(kol="isabet", senaryo="formasyon-surekli", tohum=1003,
                trafik_deseni="yere_toplama", tehdit_senaryosu="derin_sizma",
                karistirici_baslangic_s=1.0, isinma_s=0.5, olcum_bitis_s=3.5,
                kosu_bitis_s=4.0)
kur = kurulum_yap(kfg)
bas = time.perf_counter()
Kosu(kur, _fabrika("aodv", kfg)).kostur()
print(f"4 s koşu {time.perf_counter() - bas:.0f} s")
for ad, c in (("düğüm bağı", anahtar_d), ("karıştırıcı bağı", anahtar_k)):
    top = sum(c.values())
    print(f"{ad}: çağrı {top} · farklı anahtar {len(c)} · olası isabet "
          f"{1 - len(c) / top:.1%}" if top else f"{ad}: çağrı yok")
