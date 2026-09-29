"""
Ç4.2 + Ç4.3 — Li replikasyonunun güven aralığı ve duyarlılığı.

İKİ İŞ GÖRÜR
============
1. Ç4.2 — plato değeri 30 tohumla, güven aralığıyla
2. Ç4.3 — dört eksende duyarlılık: sonuç tek bir noktada mı tutuyor?

⭐ İKİNCİ İŞ AYRICA K-028'İN ADAYLARINI ÖLÇER
Ç4.4 ön-kayıtlı bandı tutmadı; onay eksikliği Li farkının açıklaması
çıkmadı. Ön-kayıtta adlandırılan sıradaki adaylar:

    yeniden deneme sınırı  (bizde 4, ns-2 varsayılanı uzun çerçevede 7)
    RTS/CTS                (modellenmiyor)
    EIFS                   (modellenmiyor)

Bu tarama birincisini DOĞRUDAN ölçer. Diğer ikisi modellenmediği için
ölçülemez; kapsam beyanına yazılırlar.

🔴 HİÇBİR PARAMETRE BANDI TUTTURMAK İÇİN DEĞİŞTİRİLMEZ.
Çıkan tablo rapora FARK ANALİZİ olarak girer, eğri uydurma olarak değil.
Varsayılanlar taramadan SONRA da değişmeyecektir.
"""

from __future__ import annotations

import statistics as ist
import sys
import time
from multiprocessing import Pool, cpu_count
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dogrulama.li_zincir import zincir_kosusu  # noqa: E402

CEKIRDEK = min(10, cpu_count())
TOHUM_HIZLI = range(1, 6)
TOHUM_TAM = range(1, 31)
PLATO_ATLAMA = 20
ARALIK_VARSAYILAN = 0.85


def _is(arg):
    atlama, tohum, carpan, ek = arg
    return zincir_kosusu(atlama, tohum, carpan, **ek)


def plato_olc(tohumlar, carpan=ARALIK_VARSAYILAN, **ek) -> dict:
    """Tek atlama ve plato verimini ölçer, oranı ve GA'sını döndürür."""
    isler = ([(1, t, carpan, ek) for t in tohumlar]
             + [(PLATO_ATLAMA, t, carpan, ek) for t in tohumlar])
    with Pool(CEKIRDEK) as p:
        sonuc = p.map(_is, isler)
    n = len(list(tohumlar))
    tek = [x["verim_bps"] for x in sonuc[:n]]
    uzun = [x["verim_bps"] for x in sonuc[n:]]
    # Tohum başına eşleştirilmiş oran — tohumlar arası değişimi doğru yakalar
    oranlar = [u / t for u, t in zip(uzun, tek)]
    ort = ist.mean(oranlar)
    if len(oranlar) > 1:
        sh = ist.stdev(oranlar) / (len(oranlar) ** 0.5)
        ga = (ort - 1.96 * sh, ort + 1.96 * sh)
    else:
        ga = (ort, ort)
    # 🔴 `uzun_kbps` EKLENDİ (B0.6 · F-4). Onceki hali yalnizca ORANI ve
    # tek atlama verimini donduruyordu; Li'nin ikinci MUTLAK sayisi
    # (uzun zincir verimi, 0,25 Mbps) disariya hic cikmiyordu. `08` Ç4'un
    # calisma noktasi tablosu o sayiyi iceriyor ama ureticisi
    # `scratchpad/b109_li.py`ydi ve o dizin depoda YOK (F-4).
    # Kapinin okudugu iki anahtar (`ters`, `ga_genislik_yuzde`) DEGISMEDI.
    return {"oran": ort, "ters": 1 / ort, "ga": ga,
            "ga_genislik_yuzde": 100 * (ga[1] - ga[0]) / ort,
            "tek_kbps": ist.mean(tek) / 1000,
            "uzun_kbps": ist.mean(uzun) / 1000}


def main() -> None:
    # Rule 7: süre tahmini ÖNCE yazdırılır
    t0 = time.perf_counter()
    _ = plato_olc(range(1, 3))
    birim = (time.perf_counter() - t0) / 4       # 2 tohum × 2 uzunluk
    tahmini = birim * (2 * len(TOHUM_TAM) + 2 * len(TOHUM_HIZLI) * 13) / CEKIRDEK
    print(f"Tahmini süre: ~{tahmini/60:.1f} dk ({CEKIRDEK} çekirdek)\n")

    print("=" * 76)
    print("Ç4.2 — PLATO, 30 TOHUM, GÜVEN ARALIĞI")
    print("=" * 76)
    r = plato_olc(TOHUM_TAM)
    print(f"  tek atlama verimi : {r['tek_kbps']:.1f} kbps")
    print(f"  plato oranı       : {r['oran']:.4f}  = 1/{r['ters']:.2f}")
    print(f"  %95 GA            : [{r['ga'][0]:.4f}, {r['ga'][1]:.4f}]"
          f"  = [1/{1/r['ga'][1]:.2f}, 1/{1/r['ga'][0]:.2f}]")
    print(f"  GA genişliği      : {r['ga_genislik_yuzde']:.2f} %"
          f"   {'✅ < %5' if r['ga_genislik_yuzde'] < 5 else '🔴 > %5'}")

    print()
    print("=" * 76)
    print("Ç4.3 — DUYARLILIK: sonuç tek bir noktada mı tutuyor?")
    print("=" * 76)

    eksenler = [
        ("paket boyutu (B)", "paket_bayt", [512, 1024, 1500, 2048], {}),
        ("yeniden deneme sınırı", "yeniden_deneme_siniri", [2, 4, 7], {}),
        ("CW min", "cw_min", [15, 31, 63], {}),
    ]

    for ad, anahtar, degerler, _ek in eksenler:
        print(f"\n--- {ad} ---")
        print(f"{'değer':>10} {'plato':>10} {'1/x':>8} {'GA gen. %':>11}")
        for v in degerler:
            s = plato_olc(TOHUM_HIZLI, **{anahtar: v})
            isaret = "  ← varsayılan" if v in (1500, 4, 31) else ""
            ns2 = "  ← ns-2 değeri" if (anahtar == "yeniden_deneme_siniri"
                                        and v == 7) else ""
            print(f"{v:>10} {s['oran']:>10.4f} {s['ters']:>8.2f} "
                  f"{s['ga_genislik_yuzde']:>11.2f}{isaret}{ns2}")

    print(f"\n--- aralık çarpanı (bağ kaybı) ---")
    print(f"{'çarpan':>10} {'plato':>10} {'1/x':>8} {'GA gen. %':>11}")
    for c in (0.80, 0.85, 0.90, 1.00):
        s = plato_olc(TOHUM_HIZLI, carpan=c)
        isaret = "  ← varsayılan" if c == 0.85 else ""
        print(f"{c:>10.2f} {s['oran']:>10.4f} {s['ters']:>8.2f} "
              f"{s['ga_genislik_yuzde']:>11.2f}{isaret}")

    print()
    print("=" * 76)
    print("YORUM ÇERÇEVESİ (sonuç görülmeden yazıldı)")
    print("  • Plato tüm eksenlerde 1/5–1/12 bandında kalıyorsa: sonuç sağlam,")
    print("    tek noktaya bağlı değil.")
    print("  • Tek bir eksen platoyu bu bandın dışına taşıyorsa: o eksen")
    print("    Li farkının baskın kaynağıdır ve rapora öyle yazılır.")
    print("  • 🔴 Hiçbir varsayılan bu taramaya bakılarak değiştirilmeyecek.")
    print(f"\nToplam süre: {(time.perf_counter()-t0)/60:.1f} dk")


if __name__ == "__main__":
    main()
