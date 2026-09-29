"""k196'nın eksik vakalarını AYNI dondurulmuş koddan üretip ekler (ajan, 28 Eylül).

Neden: `dondur.py` `tests2/`yi kopyalamıyordu; `yuklu` ve `kontrol_sinav`
vakaları sınav protokollerini oradan alır ve `uret` onlarda
`ModuleNotFoundError` verdi. `tests2/` kopyaya eklendikten sonra yalnız bu
vakalar `regresyon_satirlari._is` ile (aynı işçi, aynı satır) koşulur ve
`SatirYazici` ile (ekleme kipi) aynı dosyaya yazılır. Zaten dosyada olan vaka
yeniden yazılmaz.

    cd <kopya> && python <bu dosya> k196
"""
import json
import sys
from multiprocessing import Pool
from pathlib import Path

KOK = Path.cwd()
sys.path.insert(0, str(KOK))
sys.path.insert(0, str(KOK / "tests2"))

from kalibrasyon import regresyon_satirlari as R  # noqa: E402
from sim2.kosum.sonuc import SatirYazici  # noqa: E402


def main() -> int:
    yol = R.DIZIN / f"{sys.argv[1]}.jsonl"
    var = {json.loads(s)["konfig"]["not_"] for s in
           yol.read_text(encoding="utf-8").splitlines() if s.strip()}
    eksik = [v for v in R.vakalar() if v[0] not in var]
    print(f"dosyada {len(var)} vaka · eksik {len(eksik)}: "
          f"{[v[0] for v in eksik]}", flush=True)
    hata = 0
    with SatirYazici(yol) as yazici, Pool(max(1, len(eksik))) as havuz:
        for vaka, satir, h, sure in havuz.imap_unordered(R._is, eksik):
            if h is not None:
                hata += 1
                print(f"  🔴 {vaka[0]}: {h}", flush=True)
                continue
            yazici.yaz(satir)
            print(f"  {vaka[0]:<52} gecerli={satir['korunum']['gecerli']} · "
                  f"{sure:.0f} s", flush=True)
    return 1 if hata else 0


if __name__ == "__main__":
    raise SystemExit(main())
