"""
Ç4.4 KURULUM DENETİMİ — onay modeli neden bandın dışına çıktı?

Ön-kayıt: plato [1/6,5 · 1/8,0] bandına düşerse onay eksikliği kalan farkın
açıklamasıdır. Ölçülen 1/8,86 — bandın DIŞINDA. Ön-kayıt bu durumda
"açıklama arama, KURULUMU DENETLE" diyor.

Bu betik açıklama üretmez; sayaçları çıkarır ve airtime bütçesinin tutup
tutmadığını kontrol eder.
"""

from __future__ import annotations

import statistics as ist
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dogrulama.li_zincir import (  # noqa: E402
    ISINMA_S, KOSU_S, PAKET_BAYT, zincir_topolojisi,
)
from sim.config import Konfig  # noqa: E402
from sim.events import OlayKuyrugu  # noqa: E402
from sim.mac import KanalErisimi  # noqa: E402
from sim.packet import Paket  # noqa: E402
from sim.radio import Radyo  # noqa: E402
from sim.rng import Akislar  # noqa: E402


def sayacli_kosu(atlama: int, tohum: int, aralik_carpani: float) -> dict:
    dugum = atlama + 1
    kon = Konfig(kol="denetim", senaryo="S0", tohum=tohum,
                 paket_bayt=PAKET_BAYT, dugum_sayisi=dugum,
                 isinma_s=ISINMA_S, olcum_bitis_s=KOSU_S, kosu_bitis_s=KOSU_S)
    ak, ol = Akislar(tohum), OlayKuyrugu()
    topo = zincir_topolojisi(kon, dugum, aralik_carpani)
    mac = KanalErisimi(kon, topo, Radyo.kur(kon), ol, None, ak)

    kuyruk: dict[int, list[Paket]] = {i: [] for i in range(dugum)}
    sayac = {"kimlik": 0, "teslim": 0, "teslim_isinma": 0}
    hedef = dugum - 1

    def yeni() -> Paket:
        p = Paket(kimlik=sayac["kimlik"], kaynak=0, hedef=hedef,
                  bayt=PAKET_BAYT, dogum_s=ol.simdi, ttl=64)
        sayac["kimlik"] += 1
        return p

    def calis(d: int) -> None:
        if mac.bos_mu(d) and kuyruk[d]:
            mac.gonder(d, kuyruk[d].pop(0), d + 1)

    def besle(g: int) -> None:
        if g == 0:
            kuyruk[0].append(yeni())
        calis(g)

    def kabul(paket: Paket, g: int, a: int) -> None:
        if a == hedef:
            sayac["teslim"] += 1
            if ol.simdi < ISINMA_S:
                sayac["teslim_isinma"] += 1
        else:
            kuyruk[a].append(paket)
            calis(a)

    mac.alim_gerceklesti = kabul
    mac.gonderim_bitti = lambda p, g, h, s: besle(g)
    mac.iletim_basarisiz = lambda p, g, h: besle(g)

    kuyruk[0].append(yeni())
    ol.ekle(0.0, calis, 0)
    ol.kostur(KOSU_S)

    teslim = sayac["teslim"] - sayac["teslim_isinma"]
    return {
        "teslim": teslim,
        "verim_bps": teslim * PAKET_BAYT * 8 / (KOSU_S - ISINMA_S),
        "veri_gonderim": mac.gonderilen_veri,
        "onay_gonderim": mac.gonderilen_onay,
        "veri_basarisiz": mac.basarisiz_alim,
        "kayip_onay": mac.kayip_onay,
        "kopya_alim": mac.kopya_alim,
        "kon": kon,
    }


def main() -> None:
    print("=" * 78)
    print("Ç4.4 KURULUM DENETİMİ — onay sayaçları (aralık 0.85 R, 5 tohum)")
    print("=" * 78)
    print(f"{'atlama':>7} {'veri gön.':>10} {'onay gön.':>10} {'veri hata':>10} "
          f"{'ONAY KAYBI':>11} {'kopya':>8} {'onay kayıp %':>13}")
    print("-" * 78)

    for h in (1, 2, 4, 8, 16):
        r = [sayacli_kosu(h, t, 0.85) for t in range(1, 6)]
        vg = ist.mean(x["veri_gonderim"] for x in r)
        og = ist.mean(x["onay_gonderim"] for x in r)
        vh = ist.mean(x["veri_basarisiz"] for x in r)
        ko = ist.mean(x["kayip_onay"] for x in r)
        kp = ist.mean(x["kopya_alim"] for x in r)
        print(f"{h:>7} {vg:>10.0f} {og:>10.0f} {vh:>10.0f} {ko:>11.0f} "
              f"{kp:>8.0f} {(ko/og*100 if og else 0):>12.1f}%")

    print()
    print("=" * 78)
    print("AIRTIME BÜTÇESİ — tek atlama, çekişmesiz")
    print("=" * 78)
    r = sayacli_kosu(1, 1, 0.85)
    kon = r["kon"]
    difs, geri = kon.difs_s, (kon.cw_min / 2) * kon.slot_s
    veri, sifs, onay = kon.cerceve_suresi_s(PAKET_BAYT), kon.sifs_s, kon.onay_suresi_s
    dongu = difs + geri + veri + sifs + onay
    print(f"  DIFS {difs*1e6:6.0f} + geri çekilme {geri*1e6:6.0f} + veri "
          f"{veri*1e6:7.0f} + SIFS {sifs*1e6:4.0f} + onay {onay*1e6:5.0f} "
          f"= {dongu*1e6:8.0f} µs")
    print(f"  beklenen verim : {PAKET_BAYT*8/dongu/1000:8.1f} kbps")
    print(f"  ölçülen verim  : {r['verim_bps']/1000:8.1f} kbps")
    print(f"  oran           : {r['verim_bps']/(PAKET_BAYT*8/dongu):8.4f}"
          f"   (1.0'a yakın olmalı)")

    print()
    print("KONTROL: onay kaybı sıfıra yakınsa suçlu onay KAYBI değil,")
    print("         onayın kanalı MEŞGUL ETMESİ ve çekişmeyi artırmasıdır.")


if __name__ == "__main__":
    main()
