"""4.2 · Bianchi referans dünyanın zamanlamalarıyla — sayılar (test ±%15).

    PYTHONIOENCODING=utf-8 PYTHONDONTWRITEBYTECODE=1 \
        python arsiv/teshis/faz4_2026-09-26/b_bianchi.py
"""
import pathlib
import sys

KOK = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(KOK))
sys.path.insert(0, str(KOK / "tests2"))

from test_mac_dcf import _zamanlar, bianchi_verim, doygunluk_kosumu  # noqa: E402
from sim2.kanal.cerceve import cerceve_kur  # noqa: E402
from sim2.kanal.dunya import referans_2026  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402

if __name__ == "__main__":
    for ad, k in (("olcek_1_50", Konfig(kol="t", yeniden_deneme_siniri=1000)),
                  ("referans_2026", referans_2026(kol="t",
                                                  yeniden_deneme_siniri=1000))):
        z = _zamanlar(k)
        yuk_s = cerceve_kur(k, "veri").govde_suresi_s
        print(f"{ad}: slot {z.slot_s * 1e6:.0f} µs · başarı turu "
              f"{z.basari_turu_s * 1e3:.3f} ms · çarpışma turu "
              f"{z.carpisma_turu_s * 1e3:.3f} ms")
        for n in (5, 10, 20, 40):
            a = bianchi_verim(n, k.cw_min + 1, 5, z.slot_s, z.basari_turu_s,
                              z.carpisma_turu_s, yuk_s)
            o = doygunluk_kosumu(n, k)
            print(f"  n={n:>2} ölçülen {o:.4f} · Bianchi {a:.4f} · "
                  f"bağıl fark %{100 * (o - a) / a:+.1f}")
