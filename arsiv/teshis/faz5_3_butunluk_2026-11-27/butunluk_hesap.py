"""
Faz 5-3 · Aşama 3 · bütünlük denetimi için hesap. Yeni koşu yok; B5
teşhisinin kayıtlarından okur (`eğim0` kolu, birincil, 8 tohum).

    PYTHONIOENCODING=utf-8 py -3.11 <bu dosya> > butunluk_hesap.txt

H1 · İlanın ömrü ile son çarenin birleşimi: açık dönemde alıcısı karıştırılan
     (alanı G ya da E) kararlarda ardılın ilanı bayatsa (B4 kural 4) ve
     ardıldan başka aday yoksa, yeni tasarımda ardıl aday olmaktan çıkar ve
     düğüm açlığa düşer. Bu kararların payı ve bugünkü kodda o atlamanın
     onay payı (ardıla gönderilseydi ne olurdu): ilanın ömrünün son çareyi
     (E1) kesmesinin bedelinin üst sınırı.
"""

from __future__ import annotations

import statistics as ist
import sys
from pathlib import Path

D = Path(__file__).resolve().parent
B5 = D.parent / "faz5_3_b5_iletim_kaybi_2026-11-26"
sys.path.insert(0, str(B5))

import iletim as L  # noqa: E402
import sonuc_hesap as SH  # noqa: E402


def main() -> None:
    rs = SH.oku(B5)["birincil"]
    print("== H1 · ilanın ömrü ile son çarenin birleşimi (birincil, açık "
          "evre, pencere içi, alıcı geçit değil) ==")
    for alan in ("G", "E"):
        top = bay = tek = tek_ok = tek_b = tek_b_ok = 0
        pay: list[float] = []
        for r in rs:
            lo, hi = r["kaydedici"]["pencere"]
            n = SH.dogan(r)
            w = 0.0
            for o in SH.kararlar(r):
                if (o.evre != "a" or o.zj != alan or o.gecit
                        or not lo <= o.t < hi):
                    continue
                top += 1
                if not o.kanit & L.K_ILAN_BAYAT:
                    continue
                bay += 1
                if o.k1 >= 0:
                    continue
                tek += 1
                tek_ok += o.ok == 1
                w += o.ok == 1
                if o.kanit & L.K_BILDIRIM_A:
                    tek_b += 1
                    tek_b_ok += o.ok == 1
            pay.append(w / n)
        print(f"  alan {alan}: açık karar {top} · ardılın ilanı bayat "
              f"{bay} ({SH.yuzde(bay / top)}) · bayat ve başka aday yok {tek} "
              f"({SH.yuzde(tek / top)})")
        print(f"    bu kararlarda atlamanın onayı {SH.yuzde(tek_ok / max(1, tek))}"
              f" · bildirimli olanlarda {SH.yuzde(tek_b_ok / max(1, tek_b))} "
              f"({tek_b} karar)")
        print(f"    onaylanan bu atlamalar açık doğana oranla (bedelin üst "
              f"sınırı): {ist.mean(pay):.4f}")


if __name__ == "__main__":
    main()
