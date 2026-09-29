"""
Ç4 ÇALIŞMA NOKTASI — Li replikasyonu, Li'nin KENDİ bit hızında.

🔴 NEDEN BU DOSYA VAR — F-4 (`10` §8)
=====================================
`08` Ç4'ün "çalışma noktası" bloğu şu iki mutlak sayıyı taşıyor:

    tek atlama tavanı   : 1,761 Mbps   (Li vd. 1,7 Mbps  -> %3,6 fark)
    uzun zincir verimi  : 0,277 Mbps   (Li vd. 0,25 Mbps -> %10,8 fark)

ve üreticisi olarak `python scratchpad/b109_li.py` yazıyor.
🔴 **`scratchpad/` dizini depoda YOK.** Ölçüldü (`10` §8): 9 betiğe 14
referans var, 6 dosyada; ikisi `08`in **mühür bekleyen** sayfasında.

Bu, B-25 · B-80 · B-81'in birebir aynı örüntüsüdür: *"üretici satırı var,
sayı üretilemiyor"* — `03` kural 1'in ihlali. Y14: **mühürlenecek bir
belgedeki sayı, yeniden koşulmadan mühürlenemez.**

🔒 NEDEN VARSAYILAN BİT HIZI DEĞİŞMİYOR
========================================
`v2/kaynak_doğrulama.txt` Li vd.'nin cümlesini birebir taşıyor: *"…1/7 of
the maximum of **1.7 Mbps**"*. 1500 baytta 1,7 Mbps tek atlama tavanı
**2 Mbit/s'lik 802.11** demektir; depo **1 Mbit/s**'te koşuyor.

R-10 varsayılanı 2 Mb/s'e çekmeyi önerdi ve **REDDEDİLDİ**: bedeli Faz 0'ın
TÜM sayılarının yeniden koşulması + kapı (165-330 dk). Kazancın tamamı
koşu noktasını değiştirmeden elde edilebiliyor — bu betik onu yapıyor.
Depo 1 Mbit/s'te kalır; Li'nin noktası **ayrı bir ölçüm** olarak raporlanır.

Kullanım:
    python dogrulama/li_calisma_noktasi.py --tahmin
    python dogrulama/li_calisma_noktasi.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dogrulama.li_duyarlilik import TOHUM_TAM, plato_olc          # noqa: E402

# Li vd., "Capacity of Ad Hoc Wireless Networks" §3.2 — RAPOR EDİLEN
# değerler. Bunlar bizim ölçümümüz DEĞİLDİR; karşılaştırma hedefidir.
# `03`: literatürden gelen bir sayı bu araçta ölçülmeden projeye giremez —
# o yüzden burada yalnızca KARŞILAŞTIRMA tarafında duruyorlar.
LI_TEK_ATLAMA_MBPS = 1.7
LI_UZUN_ZINCIR_MBPS = 0.25
LI_PLATO_TERS = 7.0


def plato_bit_hizinda(bit_hizi_bps: float) -> dict:
    # Ad KANONIK `olc` DEGIL: `dogrulama/olcum.py::olc` adini
    # golgelemek B-106'da gercek bir hataya yol acmisti.
    return plato_olc(TOHUM_TAM, bit_hizi_bps=bit_hizi_bps)


def _satir(ad: str, olculen: float, li: float) -> str:
    fark = 100.0 * (olculen - li) / li
    return f"{ad:<24s}{li:>12.3f}{olculen:>14.3f}{fark:>+11.1f} %"


def main(argv: list[str]) -> int:
    print("=" * 78)
    print("Ç4 ÇALIŞMA NOKTASI — Li replikasyonu iki bit hızında")
    print("=" * 78)
    print(f"tohum: {TOHUM_TAM.start}-{TOHUM_TAM.stop - 1} | "
          f"paket 1500 B | 2 uzunluk (1 ve 20 atlama)")

    # `03` kural 7 — süre tahmini ÖNCE, ve BANT olarak.
    t0 = time.perf_counter()
    plato_olc(range(1, 3))
    birim = (time.perf_counter() - t0) / 4          # 2 tohum × 2 uzunluk
    alt = birim * 2 * len(TOHUM_TAM) * 2 / 60.0     # 2 bit hızı
    print(f"TAHMIN BANDI: {alt:.1f} - {alt * 2.10:.1f} dk "
          f"(2,10x makine oynaklığı, K-075)")
    if "--tahmin" in argv:
        print("(--tahmin: yalnızca tahmin istendi, koşulmadı)")
        return 0

    sonuc = {}
    for hiz in (1e6, 2e6):
        bas = time.perf_counter()
        sonuc[hiz] = plato_bit_hizinda(hiz)
        print(f"  {hiz/1e6:.0f} Mbit/s koşuldu ({time.perf_counter()-bas:.0f} sn)")

    print()
    print("=" * 78)
    print("DEPONUN VARSAYILANI — 1 Mbit/s  (🔒 DEĞİŞMİYOR, R-10 reddedildi)")
    print("=" * 78)
    r1 = sonuc[1e6]
    print(f"  tek atlama tavanı  : {r1['tek_kbps']/1000:.3f} Mbps")
    print(f"  uzun zincir verimi : {r1['uzun_kbps']/1000:.3f} Mbps")
    print(f"  plato oranı        : 1/{r1['ters']:.2f}  "
          f"(GA genişliği %{r1['ga_genislik_yuzde']:.2f})")

    print()
    print("=" * 78)
    print("Lİ'NİN KENDİ ÇALIŞMA NOKTASI — 2 Mbit/s")
    print("🔴 Depo bugüne kadar yalnızca ORANI karşılaştırdı; iki MUTLAK")
    print("   sayının da tuttuğu hiç yazılmadı — replikasyon OLDUĞUNDAN")
    print("   ZAYIF sunuldu (B-109).")
    print("=" * 78)
    r2 = sonuc[2e6]
    print(f"{'büyüklük':<24s}{'Li vd.':>12s}{'bu araç':>14s}{'fark':>13s}")
    print(_satir("tek atlama tavanı (Mbps)", r2["tek_kbps"] / 1000,
                 LI_TEK_ATLAMA_MBPS))
    print(_satir("uzun zincir (Mbps)", r2["uzun_kbps"] / 1000,
                 LI_UZUN_ZINCIR_MBPS))
    print(_satir("plato (1/x)", r2["ters"], LI_PLATO_TERS))
    print(f"  plato %95 GA genişliği: %{r2['ga_genislik_yuzde']:.2f}")

    print()
    print("=" * 78)
    print("🔴 AÇIK KAPANMIYOR — `08` Ç4'ün yürürlükteki cümlesi")
    print("=" * 78)
    print("  Nitel eğilim 🟢 SAĞLANDI (düşüş + plato + 4 atlamada ~1/4).")
    print("  Farkın gerekçesi 🔴 SAĞLANMADI: üç aday ölçüldü (bit hızı %1,1 ·")
    print("  EIFS ≤%0,31 · RTS/CTS ≤%7,71), en cömert toplam ≤%9,1 ve gereken")
    print("  %10,2 — YETMİYOR. Fark bugün AÇIKLANAMAMIŞTIR.")
    print("  🔒 'atfedilmektedir' YETMEZ: atfedilen şey ölçüldü ve yetmedi.")
    return 0


if __name__ == "__main__":       # Windows `spawn` — devir teslim §6.2
    raise SystemExit(main(sys.argv[1:]))
