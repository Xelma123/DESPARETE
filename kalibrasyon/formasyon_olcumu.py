"""
FORMASYON ÖLÇÜMÜ — Y6 formasyon kolunun istasyon tutma davranışı.

Üretici:
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/formasyon_olcumu.py

Bağlam: `v2/07-SIMULATOR-TASARIMI.md` §18 Y6 · `v2/04` K-118.

  A) istasyondan sapma ve duvar teması — 10 tohum × 350 s, tik çözünürlüğü
  B) komşu çiftlerin bağıl hızı — statik · bağımsız · görev · formasyon

🔴 B BİR TEŞHİSTİR, Θ DEĞİL. Θ kanal tabanlı bağ ömründen ölçülür (C4). Çift
eşiği (`YARICAP_M`) kullanılabilir bağ yarıçapının mertebesidir ve bir ÖLÇÜT
değildir: çiftleri "komşu olabilecek" diye süzer.
"""

from __future__ import annotations

import math
import statistics as ist
import sys
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.cekirdek.rng import Akislar  # noqa: E402
from sim2.dunya.geometri import mesafe  # noqa: E402
from sim2.dunya.topoloji import topoloji_kur  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402

TOHUMLAR = range(1000, 1010)
# Teşhis eşiği: kullanılabilir bağ yarıçapının mertebesi (`konfig.py`
# `gorev_grup_yaricapi_m` notu, ~530 m). Bir ölçüt değil.
YARICAP_M = 530.0
# Bağıl hız örnekleme aralığı; mobilite tikinden (0,5 s) büyük, ölçüm
# penceresinden (270 s) çok küçük.
ORNEK_ADIM_S = 5.0


def _yuzdelik(sirali: list[float], q: float) -> float:
    return sirali[int(q * (len(sirali) - 1))]


def sapma_ve_temas(tohum: int) -> dict:
    """Bir tohumda istasyondan sapma dağılımı ve duvar teması."""
    k = Konfig(kol="formasyon_olcumu", senaryo="formasyon-yok", tohum=tohum)
    m = topoloji_kur(k, Akislar(tohum)).mobilite
    s, yat, dik = [], [], []
    for i in range(k.dugum_sayisi):
        for j, p in enumerate(m.tik_konumlari(i)):
            h = m.istasyon_konumu(i, j * k.gm_adim_s)
            dx, dy, dz = p.x - h.x, p.y - h.y, p.z - h.z
            s.append(math.sqrt(dx * dx + dy * dy + dz * dz))
            yat.append(math.hypot(dx, dy))
            dik.append(abs(dz))
    s.sort()
    return {"ort": ist.mean(s), "p99": _yuzdelik(s, 0.99), "maks": s[-1],
            "yatay": ist.mean(yat), "dikey": ist.mean(dik),
            "temas": m.duvar_temasi,
            "dugum_tik": k.dugum_sayisi * (m.tik_sayisi - 1)}


def bagil_hiz(senaryo: str, tohum: int) -> list[float]:
    """Ölçüm penceresinde, eşiğin içindeki çiftlerin bağıl hızları (m/s)."""
    k = Konfig(kol="formasyon_olcumu", senaryo=senaryo, tohum=tohum)
    top = topoloji_kur(k, Akislar(tohum))
    n, dt = k.dugum_sayisi, k.gm_adim_s
    cikti: list[float] = []
    t = k.isinma_s
    while t <= k.olcum_bitis_s:
        p0 = [top.konum(i, t) for i in range(n)]
        p1 = [top.konum(i, t + dt) for i in range(n)]
        v = [((b.x - a.x) / dt, (b.y - a.y) / dt, (b.z - a.z) / dt)
             for a, b in zip(p0, p1)]
        for i in range(n):
            for j in range(i + 1, n):
                if mesafe(p0[i], p0[j]) <= YARICAP_M:
                    cikti.append(math.dist(v[i], v[j]))
        t += ORNEK_ADIM_S
    return cikti


def main() -> None:
    k = Konfig(kol="formasyon_olcumu")
    print("FORMASYON OLCUMU — Y6 (K-118)")
    print(f"  {len(TOHUMLAR)} tohum ({TOHUMLAR.start}–{TOHUMLAR.stop - 1}) × "
          f"{k.kosu_bitis_s:.0f} s · gm_alfa {k.gm_alfa} · gm_hiz_sigma_ms "
          f"{k.gm_hiz_sigma_ms} · adim {k.gm_adim_s} s")
    print()
    print("  A) ISTASYONDAN SAPMA ve DUVAR TEMASI")
    print(f"  {'tohum':>6} {'ort':>7} {'p99':>7} {'maks':>7} {'yatay':>7} "
          f"{'dikey':>7} {'temas':>6}")
    satirlar = []
    for t in TOHUMLAR:
        r = sapma_ve_temas(t)
        satirlar.append(r)
        print(f"  {t:>6} {r['ort']:>6.2f}m {r['p99']:>6.2f}m {r['maks']:>6.2f}m "
              f"{r['yatay']:>6.2f}m {r['dikey']:>6.2f}m {r['temas']:>6}")
    temas = sum(r["temas"] for r in satirlar)
    tik = sum(r["dugum_tik"] for r in satirlar)
    print(f"  TOPLAM: temas {temas} / {tik} dugum-tik "
          f"(%{100.0 * temas / tik:.4f}) · sapma ort "
          f"{ist.mean(r['ort'] for r in satirlar):.2f} m · p99 ort "
          f"{ist.mean(r['p99'] for r in satirlar):.2f} m · en buyuk "
          f"{max(r['maks'] for r in satirlar):.2f} m")
    print()
    print(f"  B) KOMSU CIFTLERIN BAGIL HIZI (TESHIS) — cift mesafesi ≤ "
          f"{YARICAP_M:.0f} m, pencere [{k.isinma_s:.0f}, "
          f"{k.olcum_bitis_s:.0f}] s, {ORNEK_ADIM_S:.0f} s ornekleme")
    print(f"  {'kol':>10} {'cift-an':>9} {'ort m/s':>8} {'p50':>7} {'p95':>7}")
    for kol in ("statik", "bagimsiz", "gorev", "formasyon"):
        tum: list[float] = []
        for t in TOHUMLAR:
            tum.extend(bagil_hiz(f"{kol}-yok", t))
        tum.sort()
        print(f"  {kol:>10} {len(tum):>9} {ist.mean(tum):>8.3f} "
              f"{_yuzdelik(tum, 0.5):>7.3f} {_yuzdelik(tum, 0.95):>7.3f}")


if __name__ == "__main__":
    main()
