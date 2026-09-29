# -*- coding: utf-8 -*-
"""H1.1 MEKANİZMA KAPISI — Aile 1'in her kolu buradan geçer.

==========================================================================
🔴 NEDEN AYRI BİR ARAÇ (A-5, beşinci bağımsız denetim · K-064)

`tests/test_mekanizma_kapisi.py::test_b65_*` kapıyı **tohum başına TEK null
çekimiyle** uyguluyor. Beşinci denetim A-5'te sordu: ablasyon permütasyonu
`hash((dugum, komşular))` ile tohumlanıyor ve `kon.tohum` içermiyor — yani
aynı tohumda **ikinci bir bağımsız null çekilemiyor** ve çekimin kendi
varyansı topolojininkiyle **karışık** kalıyor.

🔒 ÖLÇÜLDÜ (26 Ağu 2026, 8 tohum × 5 bağımsız çekim = 48 tam koşu):

    eşleştirilmiş farkın toplam varyansı (tek null) : std 0,02298
      · bunun ABLASYON ÇEKİMİNDEN geleni            : std 0,01566  (%46,4)
      · TOPOLOJİDEN geleni                          : std 0,01682  (%53,6)

**Ablasyon çekimi, kapının ayırt etmeye çalıştığı farkın varyansının
neredeyse yarısı.** Tohum başına tek null, gürültülü bir kestirimdir ve
**güç boşa harcanır.**

⚖️ İki şey bu değişikliği temiz kılıyor:
  1. Nokta kestirimi OYNAMIYOR: +0,02827 → +0,02845. Etki gerçek.
  2. 🔴 **Kapı iki hâlde de GEÇİYOR.** Yani m, başarısız bir kapıyı
     kurtarmak için büyütülmedi — iki olası sonuç da ÖLÇÜMDEN ÖNCE ilan
     edildi (K-064).

## 🔒 MÜHÜRLÜ KARAR — m = 5

`test_b65_*` tam pakette kalır ve **m = 1** ile aracın **regresyon testi**
olur *(ucuz: mutasyon kapısı 150 dk'da kalır; m=5 olsaydı ~318 dk)*.
Aile 1'in her kolunu fiilen geçiren kapı **budur ve m = 5 kullanır.**

🔴 **m SONRADAN BÜYÜTÜLEMEZ** *(`03` kural 3)*. Bir kol kapıdan geçemezse
m artırılarak yeniden denenmez — bu, eşiği geriye dönük gevşetmektir.
m = 5, `06`da mühürlenmiştir.

## ÖLÇÜT — `test_b65_*` ile BİREBİR AYNI

    1. Eşleştirilmiş fark ≥ 8 tohumun 7'sinde pozitif
    2. Farkın %95 güven aralığı sıfırı dışlar

Değişen TEK şey: null, **m bağımsız çekimin ortalamasıdır.**
==========================================================================
"""
from __future__ import annotations

import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from sim.config import Konfig                                    # noqa: E402
from dogrulama.olcum import kayit, olc                           # noqa: E402
from dogrulama.aktaricilar import AKTARICILAR, kalite_ablasyonu  # noqa: E402

# 🔒 MÜHÜRLÜ SABİTLER — `06` ile aynı satırdan okunur
KAPI_TOHUMLARI = (1, 2, 3, 4, 5, 6, 7, 8)
NULL_CEKIM_SAYISI = 5           # 🔒 m — A-5, K-064. SONRADAN BÜYÜTÜLEMEZ.
EN_AZ_POZITIF = 7               # 8 tohumun 7'si
_T_975_7 = 2.365                # t, %95 iki yönlü, 7 serbestlik derecesi

SENARYO = "S2"
OLCUT_ALANI = "secim_avantaji_ortalama"


def _kos(fabrika, tohum: int) -> float:
    return olc(Konfig(kol="t", senaryo=SENARYO, tohum=tohum),
               fabrika)[OLCUT_ALANI]


def kapiyi_uygula(fabrika, ad: str = "kol", alan: str = "bildirdigi_gurultu_w",
                  m: int = NULL_CEKIM_SAYISI, ayrinti: bool = True) -> dict:
    """Bir kola H1.1 kapısını uygular. Null, `m` bağımsız çekimin ortalaması.

    Döner: {"gecti": bool, "ort": float, "std": float, "poz": int,
            "ga_alt": float, "cekim_std": float}
    """
    farklar = []
    ic_stdler = []
    for t in KAPI_TOHUMLARI:
        kol = _kos(fabrika, t)
        nuller = [_kos(kalite_ablasyonu(fabrika, alan=alan, tuz=s), t)
                  for s in range(m)]
        farklar.append(kol - statistics.mean(nuller))
        if m > 1:
            ic_stdler.append(statistics.stdev(nuller))
        if ayrinti:
            print("   tohum %d : kol=%+.5f  null(m=%d)=%+.5f  fark=%+.5f"
                  % (t, kol, m, statistics.mean(nuller), farklar[-1]))

    ort = statistics.mean(farklar)
    std = statistics.stdev(farklar)
    poz = sum(1 for x in farklar if x > 0)
    ga_alt = ort - _T_975_7 * std / len(farklar) ** 0.5
    cekim_std = ((sum(x * x for x in ic_stdler) / len(ic_stdler)) ** 0.5
                 if ic_stdler else float("nan"))

    gecti = (poz >= EN_AZ_POZITIF) and (ga_alt > 0)

    if ayrinti:
        print()
        print("   %-28s %s" % ("KOL", ad))
        print("   %-28s %d (mühürlü — büyütülemez)" % ("null çekimi m", m))
        print("   %-28s %+.5f" % ("eşleştirilmiş fark (ort)", ort))
        print("   %-28s %.5f" % ("std (tohumlar arası)", std))
        print("   %-28s %.5f" % ("std (ablasyon ÇEKİMİ, havuz)", cekim_std))
        print("   %-28s %d/%d  %s" % ("koşul 1 · pozitif", poz,
                                      len(KAPI_TOHUMLARI),
                                      "✅" if poz >= EN_AZ_POZITIF else "🔴"))
        print("   %-28s %+.5f  %s" % ("koşul 2 · %95 GA alt", ga_alt,
                                      "✅" if ga_alt > 0 else "🔴"))
        print()
        print("   🔒 KAPI: %s" % ("🟢 GEÇTİ" if gecti else "🔴 GEÇMEDİ"))
        if not gecti:
            print("   ⚠️ `06`: bu kolun teslimdeki farkının sebebi MEKANİZMA")
            print("      DEĞİLDİR ve sonucuna BAKILMAZ. m artırılarak yeniden")
            print("      denenemez (kural 3).")

    return {"gecti": gecti, "ort": ort, "std": std, "poz": poz,
            "ga_alt": ga_alt, "cekim_std": cekim_std}


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    kol = argv[0] if argv else "gurultuden_kacan"
    if kol not in AKTARICILAR:
        print("bilinmeyen kol: %r\nizinli: %s" % (kol, sorted(AKTARICILAR)))
        return 2
    print("=" * 74)
    print("H1.1 MEKANİZMA KAPISI — kol: %s · m = %d · %d tohum"
          % (kol, NULL_CEKIM_SAYISI, len(KAPI_TOHUMLARI)))
    print("=" * 74)
    print("%d tam koşu · tahmini ~%.0f dk"
          % (len(KAPI_TOHUMLARI) * (1 + NULL_CEKIM_SAYISI),
             len(KAPI_TOHUMLARI) * (1 + NULL_CEKIM_SAYISI) * 9 / 60.0))
    print()
    s = kapiyi_uygula(AKTARICILAR[kol], ad=kol)
    return 0 if s["gecti"] else 1


if __name__ == "__main__":
    with kayit("mekanizma_kapisi"):
        raise SystemExit(main())
