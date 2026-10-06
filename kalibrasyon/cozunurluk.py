"""
DENEYİN ÇÖZÜNÜRLÜĞÜ — n tohumlu bir hücre EN KÜÇÜK hangi farkı görebilir?

Üretici:
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/cozunurluk.py
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/cozunurluk.py --tohum 40

🔴 NEDEN
========
Duyarlılık taraması bir parametreyi *"duyarsız"* ilan ederken iki şeye
birden bakmak zorunda:

  1. etki, kendi hata payından küçük mü *(istatistiksel)*
  2. etki, DENEYİN GÖREBİLECEĞİ en küçük farktan küçük mü *(pratik)*

🔴 İkincisi olmadan tarama büyük ama TUTARSIZ etkileri aklar. Ölçüldü:
`irtifa_maks_m` PDR'yi iki yönde de **8 puan** oynatıyor ama tohumlar arası
yayılımı büyük olduğu için band testini geçiyordu — yani 8 puanlık bir etki
"duyarsız" diye etiketlenecekti. Bu, aklamanın en kötü hâlidir.

🔒 ÇÖZÜM: eşik SEÇİLMEZ, TÜRETİLİR. Çekirdek hücre n tohumla koşacak;
o hücrenin kol düzeyi 2 SE'si, deneyin iddia edebileceği EN KÜÇÜK farktır.
Ondan küçük bir etki hiçbir sonucu değiştiremez — çünkü deney onu zaten
göremez.

    R = 2 · SD_tohum / √n

⚠️ R bir "önemlilik eşiği" DEĞİL, bir GÖRÜNÜRLÜK eşiğidir. R'nin altındaki
bir etki gerçek olabilir; sadece bu deneyle ayırt edilemez, ve bu beyan
edilir.

10 Eylül 2026 (K-113): öğrenci ana deneyin tohum sayısını 40'a çıkardı.
Varsayılan 30 tohum olarak kaldı — K-107'nin kayıtlı sayısı argümansız
komutla yeniden üretilir. 40 tohumluk çözünürlük `--tohum 40` ile ölçülür.
"""

from __future__ import annotations

import statistics as ist
import sys
from multiprocessing import Pool
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from kalibrasyon import dunya_secimi as DS  # noqa: E402  (K-183)
from kalibrasyon.duyarlilik import HUCRE_EKLERI, R_ESLESTIRILMIS, _is  # noqa: E402

TOHUMLAR = tuple(range(1000, 1030))
SENARYO = "statik-surekli"
# `--hucre birincil` (K-211 sonrası Faz 4.4): eski çekirdek hücre referans
# dünyada tabana yapışık (kâhin PDR 0,029, K-206); R ve taramalar birincil
# hücrede (`duyarlilik.py::HUCRE_EKLERI` ile aynı tanım).
EK: dict = {}


def main(isci: int = 8) -> None:
    print("=" * 78)
    print(f"DENEYIN COZUNURLUGU — {SENARYO} · {len(TOHUMLAR)} tohum")
    print("=" * 78)
    aletler = ("en_guvenilir_kahin", "en_kisa_yol_kahin")
    gorevler = [(SENARYO, t, a, dict(EK)) for a in aletler for t in TOHUMLAR]
    with Pool(isci) as havuz:
        ham = havuz.map(_is, gorevler, chunksize=1)
    n = len(TOHUMLAR)
    pdr = {}
    for (_, t, a, _e), (s, h) in zip(gorevler, ham):
        if h is None:
            pdr[(a, t)] = s[0]
    print()
    print(f"  {'cikti':>14} {'ortalama':>10} {'SD_tohum':>10} "
          f"{'R = 2 SD/sqrt(n)':>19}   (n = {n})")
    sonuc = {}
    for ad, alet in (("pdr_etx", aletler[0]), ("pdr_atlama", aletler[1])):
        v = [pdr[(alet, t)] for t in TOHUMLAR if (alet, t) in pdr]
        sd = ist.stdev(v)
        r = 2.0 * sd / len(v) ** 0.5
        sonuc[ad] = r
        print(f"  {ad:>14} {ist.mean(v):>10.4f} {sd:>10.4f} {r:>19.4f}")
    fark = [pdr[(aletler[0], t)] - pdr[(aletler[1], t)]
            for t in TOHUMLAR if (aletler[0], t) in pdr and
            (aletler[1], t) in pdr]
    sd = ist.stdev(fark)
    r = 2.0 * sd / len(fark) ** 0.5
    sonuc["olcut_bedeli"] = r
    print(f"  {'olcut_bedeli':>14} {ist.mean(fark):>10.4f} {sd:>10.4f} "
          f"{r:>19.4f}")
    print()
    print("  🔒 `olcut_bedeli` ESLESTIRILMIS oldugu icin cok daha keskin:")
    print("     iki kahin ayni tohumda ayni dunyayi gorur, tohumlar arasi")
    print("     varyans ortak-mod olarak duser. Deneyin asil ayirt edici")
    print("     ekseni de budur.")
    print()
    # 🔴 BU ALET KENDİ KENDİSİYLE ÇELİŞİYORDU — 16 Eylül 2026 (denetim B5).
    # Üstteki cümle *"deneyin asıl ayırt edici ekseni EŞLEŞTİRİLMİŞ olandır"*
    # diyor, sonra alt satır EN GEVŞEK çıktıyı seçiyordu (`max`). İki sebeple
    # yanlıştı:
    #   1. Ön-kayıttaki BİRİNCİL TEST eşleştirilmiştir (Wilcoxon, `06` §7).
    #   2. Duyarlılık aleti de eşleştirilmiş çalışır — tohum başına FARK
    #      ölçer, ortalamaların farkını değil (`duyarlilik.py::_esli_fark`).
    # Yani aklamalar, deneyin gerçekte kullanacağından GEVŞEK bir eşiğe karşı
    # yazılıyordu. K-128 eşiği 0,036 → 0,0316'ya çekmişti; 0,0316 da TEK KOL
    # çözünürlüğüdür ve aynı hatanın daha küçük hâliydi.
    # 🔒 BAYATLIK KAPISI — 16 Eylül 2026 (K-132). `duyarlilik.py` kararını
    # `R_ESLESTIRILMIS` sabitine göre veriyor. O sabit bu ölçümden geliyor;
    # ölçüm değişip sabit kalırsa aklamalar sessizce BAYAT bir eşiğe karşı
    # yapılır — K-128'in bulduğu hatanın ta kendisi, ama bu kez kodda.
    # Burası onu her koşumda karşılaştırır.
    olculen = sonuc["olcut_bedeli"]
    sapma = abs(olculen - R_ESLESTIRILMIS)
    print(f"  {'saklanan R':>14} {R_ESLESTIRILMIS:>10.4f}  "
          f"(`duyarlilik.py::R_ESLESTIRILMIS`)")
    if sapma > 0.0005:
        print(f"  🔴 BAYAT SABIT: olculen {olculen:.4f} ile saklanan "
              f"{R_ESLESTIRILMIS:.4f} ayrismis (sapma {sapma:.4f}).")
        print("     `duyarlilik.py::R_ESLESTIRILMIS` guncellenmeli ve")
        print("     koken defterindeki `DUYARSIZ` aklamalari YENIDEN")
        print("     denetlenmeli — esik degisince siniflandirma degisebilir.")
    else:
        print(f"  🟢 saklanan sabit TAZE (sapma {sapma:.4f} <= 0,0005)")
    print()
    print(f"  🟢 KULLANILACAK ESIK R = {olculen:.4f} "
          f"(ESLESTIRILMIS — birincil testin cozunurlugu)")
    print(f"     Tek kol cozunurlukleri karsilastirma icin: "
          f"pdr_etx {sonuc['pdr_etx']:.4f} · "
          f"pdr_atlama {sonuc['pdr_atlama']:.4f}")
    print("     Bir parametre, ETKISI R'DEN KUCUK **ve** kendi hata payi")
    print("     icindeyse `DUYARSIZ` olur. Ikisinden biri yetmez.")
    print()
    print("  ⚠️ BU SAYI BUGUNUN EN IYI ESLESTIRILMIS KESTIRIMIDIR, nihai")
    print("     degil: burada olculen kontrast IKI KAHIN arasindadir. Ana")
    print("     deneyin kontrasti PROTOKOL KOLLARI arasinda olacak ve onun")
    print("     gurultusu Asama 2'de taban protokollerle olculecek")
    print("     (`06` §7 guc analizi).")


if __name__ == "__main__":
    # 30 Eylül 2026 (Faz 4 kapanışı B7): `--dunya` — ölçüm gövdesi
    # (`duyarlilik._kos`) dünyayı seçimden kurar; seçim havuz işçilerine
    # ortam değişkeniyle geçer ve başlıkta basılır.
    DS.secimi_oku()
    print(f"  DUNYA: {DS.secili()}")
    # `--tohum N`: çözünürlüğü N tohumla ölçer; ilk tohum aynı kalır.
    if "--hucre" in sys.argv:
        _h = sys.argv[sys.argv.index("--hucre") + 1]
        if _h != "birincil":
            raise SystemExit(f"bilinmeyen hucre: {_h!r} (yalniz `birincil`)")
        SENARYO = "formasyon-surekli"
        EK = dict(HUCRE_EKLERI["birincil"])
        print(f"  HUCRE: {SENARYO} · {EK}")
    if "--tohum" in sys.argv:
        _n = int(sys.argv[sys.argv.index("--tohum") + 1])
        TOHUMLAR = tuple(range(TOHUMLAR[0], TOHUMLAR[0] + _n))
    main()
