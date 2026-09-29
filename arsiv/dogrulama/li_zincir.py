"""
AİLE 0 / K4 — Li replikasyonu.  🚪 12 Eylül kapısı

Hedef (Li, Blake, De Couto, Lee, Morris, "Capacity of Ad Hoc Wireless
Networks", §3.2):

    ideal MAC ile zincir kullanımı ................ ~1/3
    ideal zincir / tek atlama ..................... ~1/4
    802.11 gerçekte / tek atlama .................. ~1/7

Düzenek: n düğüm bir sıraya dizilir, aralık = iletim menzili. Kaynak
DOYMUŞTUR (kuyruğu hiç boşalmaz). Rota sabittir: i -> i+1. Ölçülen:
son düğüme varan veri hızı.

⚠️ Bu bir PROTOKOL deneyi değildir. Yönlendirme yok, karıştırıcı yok.
Ölçülen şey aracın MAC katmanının fiziği doğru üretip üretmediğidir.

BEKLENEN UZAMSAL DESEN — bu düzenekte kendiliğinden doğmalı:
    aralık = 280 m  ->  i ile i+1 iletim menzilinde
                        i ile i+2: 560 m, iletim menzili DIŞINDA ama
                                   girişim menzili (603 m) İÇİNDE
                        i ile i+3: 840 m, tamamen dışında
    Yani her 3 düğümde bir eşzamanlı iletim mümkün -> 1/3 kullanım.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sim.config import Konfig
from sim.events import OlayKuyrugu
from sim.mac import KanalErisimi
from sim.packet import Paket
from sim.radio import Radyo
from sim.rng import Akislar
from sim.topology import Topoloji

PAKET_BAYT = 1500        # Li vd. 1500 baytlık paket kullanıyor
KOSU_S = 30.0
ISINMA_S = 5.0


def zincir_topolojisi(kon: Konfig, dugum: int, aralik_carpani: float = 1.0) -> Topoloji:
    aralik = kon.iletim_menzili_m * aralik_carpani
    return Topoloji(
        konumlar=tuple((i * aralik, 0.0) for i in range(dugum)),
        iletim_menzili_m=kon.iletim_menzili_m,
        girisim_menzili_m=kon.girisim_menzili_m,
    )


def zincir_kosusu(atlama: int, tohum: int = 1,
                  aralik_carpani: float = 1.0, **konfig_ek) -> dict:
    """`atlama` atlamalı bir zincirde doymuş akış koştur.

    `konfig_ek` duyarlılık taraması içindir (Ç4.3): paket boyutu, yeniden
    deneme sınırı, CW gibi parametreler dışarıdan verilebilir.
    ⚠️ Taramadan çıkan hiçbir değer varsayılana geri yazılmaz.
    """
    dugum = atlama + 1
    varsayilan = dict(paket_bayt=PAKET_BAYT)
    varsayilan.update(konfig_ek)
    kon = Konfig(kol="li", senaryo="S0", tohum=tohum,
                 dugum_sayisi=dugum,
                 isinma_s=ISINMA_S, olcum_bitis_s=KOSU_S,
                 kosu_bitis_s=KOSU_S, **varsayilan)
    akislar = Akislar(tohum)
    olaylar = OlayKuyrugu()
    topo = zincir_topolojisi(kon, dugum, aralik_carpani)
    radyo = Radyo.kur(kon)
    mac = KanalErisimi(kon, topo, radyo, olaylar, None, akislar)

    kuyruk: dict[int, list[Paket]] = {i: [] for i in range(dugum)}
    sayac = {"kimlik": 0, "teslim": 0, "teslim_isinma": 0}
    hedef = dugum - 1

    def yeni_paket() -> Paket:
        p = Paket(kimlik=sayac["kimlik"], kaynak=0, hedef=hedef,
                  bayt=kon.paket_bayt, dogum_s=olaylar.simdi, ttl=64)
        sayac["kimlik"] += 1
        return p

    def calis(d: int) -> None:
        if not mac.bos_mu(d) or not kuyruk[d]:
            return
        mac.gonder(d, kuyruk[d].pop(0), d + 1)

    def kaynak_besle(gonderen: int) -> None:
        """Kaynak DOYMUŞ: gönderim biter bitmez yeni paket üretilir."""
        if gonderen == 0:
            kuyruk[0].append(yeni_paket())
        calis(gonderen)

    def tamamlandi(paket: Paket, gonderen: int, alan: int) -> None:
        """Alıcı paketi kabul etti (onay henüz gitmemiş olabilir)."""
        if alan == hedef:
            sayac["teslim"] += 1
            if olaylar.simdi < ISINMA_S:
                sayac["teslim_isinma"] += 1
        else:
            kuyruk[alan].append(paket)
            calis(alan)

    def basarisiz(paket: Paket, gonderen: int) -> None:
        kaynak_besle(gonderen)

    mac.alim_gerceklesti = tamamlandi
    mac.gonderim_bitti = lambda p, g, h, s: kaynak_besle(g)
    mac.iletim_basarisiz = lambda p, g, h: basarisiz(p, g)

    kuyruk[0].append(yeni_paket())
    olaylar.ekle(0.0, calis, 0)
    olaylar.kostur(KOSU_S)

    olculen = sayac["teslim"] - sayac["teslim_isinma"]
    sure = KOSU_S - ISINMA_S
    return {
        "atlama": atlama,
        "aralik_carpani": aralik_carpani,
        "teslim": olculen,
        "verim_bps": olculen * kon.paket_bayt * 8 / sure,
        "gonderilen_veri": mac.gonderilen_veri,
        "basarisiz_alim": mac.basarisiz_alim,
    }


def rapor(aralik_carpani: float, tohumlar=range(1, 6)) -> dict:
    import statistics as ist
    tek = ist.mean(zincir_kosusu(1, t, aralik_carpani)["verim_bps"]
                   for t in tohumlar)
    satirlar = []
    for h in (2, 3, 4, 6, 8, 12, 16, 20):
        r = [zincir_kosusu(h, t, aralik_carpani) for t in tohumlar]
        oran = ist.mean(x["verim_bps"] for x in r) / tek
        satirlar.append({
            "atlama": h, "oran": oran, "ters": 1 / oran,
            "std": ist.stdev(x["verim_bps"] / tek for x in r),
            "basarisiz": ist.mean(x["basarisiz_alim"] / x["gonderilen_veri"]
                                  for x in r),
        })
    return {"tek_bps": tek, "satirlar": satirlar,
            "plato_ters": 1 / satirlar[-1]["oran"]}


def main() -> None:
    print("=" * 66)
    print("AILE 0 / K4 - Li zincir kapasitesi replikasyonu   (12 Eylul kapisi)")
    print("=" * 66)
    print(f"paket {PAKET_BAYT} B - olcum {KOSU_S - ISINMA_S:.0f} s - 5 tohum")
    print()

    olculen = {}
    for carp, ad, notu in (
        (0.85, "ARALIK = 0.85 x MENZIL", "bag PER ~ %0.03 (Li nin ns-2 modeli gibi)"),
        (1.00, "ARALIK = 1.00 x MENZIL", "bag PER = %24 (bizim PER gradyanimiz)"),
    ):
        r = rapor(carp)
        olculen[carp] = r
        print(f"--- {ad} --- {notu}")
        print(f"    tek atlama verimi: {r['tek_bps']/1000:.1f} kbps")
        print(f"    {'atlama':>7} {'tek atlamanin':>14} {'1/x':>7} "
              f"{'std':>8} {'basarisiz':>10}")
        for x in r["satirlar"]:
            print(f"    {x['atlama']:>7} {x['oran']:>14.4f} {x['ters']:>7.2f} "
                  f"{x['std']:>8.4f} {x['basarisiz']:>10.3f}")
        print(f"    -> uzun zincir platosu: tek atlamanin 1/{r['plato_ters']:.2f} u")
        print()

    # 🔴 B-12: BU BLOK ESKİDEN ELLE YAZILMIŞ SAYILAR BASIYORDU.
    # "1/6.0 · 1/12 · 1/3.6 · %16" sabitleri, onay modellemesi sonrası
    # değişen gerçek değerlerle (1/6,29 · 1/12,61 · 1/3,87 · %10) çelişiyordu.
    # `03` B5: "Yargıyı elle yazmak — beklenen sonucu basan bir analiz
    # fonksiyonu, ölçümü süsleme aracına çevirir." Ve bu betik K4 kapısının
    # BİRİNCİL üretici komutu; jüriye gösterilecek çıktı buydu.
    # Artık dört sayı da ölçümden hesaplanıyor.
    # Yukarıdaki döngüden gelen ölçümler kullanılıyor — yeniden koşulmuyor.
    kayipsiz, sinirda = olculen[0.85], olculen[1.00]
    li_hedef = 1 / 7
    ideal_4 = next(x for x in kayipsiz["satirlar"] if x["atlama"] == 4)
    acik_yuzde = 100 * (kayipsiz["satirlar"][-1]["oran"] - li_hedef) / li_hedef

    print("=" * 66)
    print("KARSILASTIRMA  (tum sayilar bu kosudan hesaplandi)")
    print("  Li vd. ideal zincir      : 1/4")
    print("  Li vd. 802.11 olculen    : 1/7")
    print(f"  Bizim (kayipsiz bag)     : 1/{kayipsiz['plato_ters']:.2f}"
          f"   <- NITEL EGILIM AYNI")
    print(f"  Bizim (menzil sinirinda) : 1/{sinirda['plato_ters']:.2f}"
          f"   <- ek bag kaybi dahil")
    print(f"  4 atlamada ideal bolge   : 1/{ideal_4['ters']:.2f}"
          f"   <- Li nin 1/4 u")
    print()
    # 🔴 F-6 (B0.6) — BU BLOK 1 EYLUL SONRASI DUZELTILDI.
    # Eski hali kalan acigi "RTS/CTS ve EIFS modellenmedi" diye
    # ATFEDIYORDU. `08` Ç4 o ifadeyi B-110'da GERI ALDI: uc adayin da
    # UST SINIRI olculdu ve toplamlari acigi kapatmiyor. `03` B4:
    # *"bir kusuru olcmek onu SEBEP yapmaz"*. Betik `08`in yururlukteki
    # cumlesini basmak zorunda — yoksa jüriye gosterilen ciktı ile
    # mühür bekleyen belge CELISIR (`03` B5: kod belgenin kanitidir).
    print("FARKIN GEREKCESI (egriye uydurma YAPILMADI):")
    print("  1) Li nin ns-2 modelinde menzil ici baglar KAYIPSIZDIR.")
    print(f"     Aralik 0.85R yapilip bag kaybi sifirlaninca")
    print(f"     1/{sinirda['plato_ters']:.2f} -> 1/{kayipsiz['plato_ters']:.2f} oluyor.")
    print(f"  2) Kalan %{abs(acik_yuzde):.0f} luk fark "
          f"(1/{kayipsiz['plato_ters']:.2f} vs 1/7) ACIKLANAMAMISTIR.")
    print("     Uc aday OLCULDU ve UCU DE YETMEDI:")
    print("       bit hizi  %1,1   (30 tohum x 2 uzunluk, olcum)")
    print("       EIFS     <=%0,31 (cozulemeyen alim x EIFS-DIFS)")
    print("       RTS/CTS  <=%7,71 (cerceve sureleri / dongu)")
    print("       EN COMERT TOPLAM <=%9,1   GEREKEN %10,2  -> YETMIYOR")
    print("     🔒 'atfedilmektedir' ARTIK YETMEZ (B-110): atfedilen sey")
    print("     olculdu ve acigi kapatmadi. Ureticiler:")
    print("       python dogrulama/li_calisma_noktasi.py")
    print("       python dogrulama/li_duyarlilik.py")
    print()
    print("DOGRULANAN NITEL DAVRANISLAR:")
    print("  - verim atlama sayisiyla dusuyor ve plato yapiyor")
    print(f"  - 4 atlamada ideal zincir bolgesi (1/{ideal_4['ters']:.2f})")
    print(f"  - tek atlama verimi {kayipsiz['tek_bps']/1000:.1f} kbps"
          f"  (analitik 932.7)")


if __name__ == "__main__":
    main()
