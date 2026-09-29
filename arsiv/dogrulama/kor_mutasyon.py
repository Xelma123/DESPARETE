"""
KÖR MUTASYON TARAYICI — seçim yanlılığının panzehiri.

🔴 SORUN: `mutasyon_paketi.py` ELLE SEÇİLMİŞ mutasyonlar içerir. Bağımsız
denetim gösterdi ki bu seçim **yanlıydı**: kendi 7 mutasyonum 7/7
yakalanıyordu ama denetçinin bağımsız 10 mutasyonunun 8'i sağ çıktı.
Sebep basit — kendi mutasyonlarımı **zaten test ettiğimi bildiğim** yollardan
seçmiştim.

ÇÖZÜM: mutasyonu KÖR üret. Kaynak dosyalar mekanik kurallarla bozulur;
hangi yolun test edildiği bilinmez.

🔴 BU BİR KAPI DEĞİLDİR — VE OLAMAZ
====================================
Kör üretim **eşdeğer mutant** (equivalent mutant) üretir: davranışı hiç
değiştirmeyen değişiklikler. Onların sağ çıkması bir kusur DEĞİLDİR.
Dolayısıyla %100 mutasyon skoru ulaşılabilir bir hedef değildir.

Bu betiğin çıktısı iki şeydir:
  1. **mutasyon skoru** — zaman içinde izlenecek bir sayı
  2. **sağ kalan mutant listesi** — ELLE AYIKLANACAK

Ayıklamada gerçek bir boşluk çıkarsa, ona bir regresyon testi yazılır ve
mutasyon `mutasyon_paketi.py`ye KÜRE EDİLMİŞ liste olarak eklenir. Kapı
orada kalır; burası besleyicidir.

Kullanım:
    python dogrulama/kor_mutasyon.py [adet]
"""

from __future__ import annotations

import os
import random
import re
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from multiprocessing import Pool
from pathlib import Path

# 🔴 ALT SÜREÇ ÇIKTISI UTF-8 OLARAK ÇÖZÜLÜR (20 Ağu 2026).
# `subprocess.run(..., text=True)` kodlama verilmezse çıktıyı YEREL KOD
# SAYFASIYLA çözer. Bu makinede o cp1254 ve çocuk süreç UTF-8 basıyor
# (PYTHONIOENCODING ayarlı). Türkçe "Ş" (U+015E → C5 9E) gibi karakterler
# cp1254'te TANIMSIZ olduğu için ebeveyn `UnicodeDecodeError` fırlatır ve
# araç, işini bitirmişken çöker. Ölçüldü: bir doğrulama koşusu tam olarak
# böyle düştü. `errors="replace"` ile ayrıştırma asla çökmez.

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK))

# 🔴 B-100 — kopyalama kuralı TEK KAYNAKTAN (`dogrulama/kopya.py`).
from dogrulama.kopya import depoyu_kopyala                       # noqa: E402

HEDEF_DIZIN = KOK / "sim"
TOHUM = 20260819          # üretim belirlenimci — aynı tohum aynı mutant kümesi


@dataclass(frozen=True)
class KorMutant:
    dosya: str
    satir_no: int
    eski: str
    yeni: str
    kural: str

    @property
    def ad(self) -> str:
        return f"{Path(self.dosya).stem}:{self.satir_no}:{self.kural}"


# --------------------------------------------------------------------------
# Mutasyon kuralları — mekanik, kör
# --------------------------------------------------------------------------
KURALLAR: list[tuple[str, str, str]] = [
    (r"(?<![<>=!])>=(?!=)", ">", "ge_gt"),
    (r"(?<![<>=!])<=(?!=)", "<", "le_lt"),
    (r"(?<![<>=!])>(?!=)", ">=", "gt_ge"),
    (r"(?<![<>=!])<(?!=)", "<=", "lt_le"),
    (r"\band\b", "or", "and_or"),
    (r"\bor\b", "and", "or_and"),
    (r"\bTrue\b", "False", "true_false"),
    (r"\bFalse\b", "True", "false_true"),
    (r"(?<![\w.])\+=", "-=", "arti_eksi"),
]

# Bu satırları hiç kurcalama — mutasyon değil, gürültü üretirler.
ATLA = re.compile(
    r"^\s*(#|\"\"\"|'''|from |import |@|def |class )|"
    r"(noqa|type: ignore)"
)


def mutantlari_uret() -> list[KorMutant]:
    mutantlar: list[KorMutant] = []
    for yol in sorted(HEDEF_DIZIN.glob("*.py")):
        if yol.name == "__init__.py":
            continue
        satirlar = yol.read_text(encoding="utf-8").splitlines()
        belge_ici = False
        for i, satir in enumerate(satirlar, start=1):
            # Kaba docstring takibi
            if satir.count('"""') % 2 == 1:
                belge_ici = not belge_ici
                continue
            if belge_ici or ATLA.search(satir) or not satir.strip():
                continue
            for kalip, degistir, ad in KURALLAR:
                if re.search(kalip, satir):
                    yeni = re.sub(kalip, degistir, satir, count=1)
                    if yeni != satir:
                        mutantlar.append(KorMutant(
                            f"sim/{yol.name}", i, satir, yeni, ad))
    return mutantlar


def _kosu(m: KorMutant) -> dict:
    gecici = Path(tempfile.mkdtemp(prefix="kor_"))
    try:
        hedef = depoyu_kopyala(gecici / "depo")
        yol = hedef / m.dosya
        satirlar = yol.read_text(encoding="utf-8").splitlines(keepends=True)
        if satirlar[m.satir_no - 1].rstrip("\r\n") != m.eski:
            return {"m": m, "durum": "uygulanamadi"}
        son = "\n" if satirlar[m.satir_no - 1].endswith("\n") else ""
        satirlar[m.satir_no - 1] = m.yeni + son
        yol.write_text("".join(satirlar), encoding="utf-8")

        # Sözdizimi kırıldıysa bu mutant bilgi taşımaz
        d = subprocess.run([sys.executable, "-m", "py_compile", str(yol)],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        if d.returncode != 0:
            return {"m": m, "durum": "sozdizimi"}

        p = subprocess.run(
            [sys.executable, "-m", "pytest", "tests", "-q", "--tb=no",
             "-p", "no:cacheprovider", "-x"],
            cwd=hedef, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        oldu = p.returncode != 0
        return {"m": m, "durum": "yakalandi" if oldu else "sag_kaldi"}
    except subprocess.TimeoutExpired:
        # Sonsuz döngüye sokan mutant da bir yakalamadır
        return {"m": m, "durum": "yakalandi"}
    except Exception as e:                       # noqa: BLE001
        return {"m": m, "durum": f"hata:{e!r}"[:80]}
    finally:
        shutil.rmtree(gecici, ignore_errors=True)


def taban_kontrolu() -> tuple[bool, str]:
    """🔴 Y7 — TARAYICI NE ÖLÇTÜĞÜNÜ KENDİSİ DOĞRULAMALI.

    Mutasyonsuz bir kopyada test paketi GEÇMELİ. Geçmiyorsa "yakalandı"
    sayımı anlamsızdır: kopyalama, yol, ortam ya da izolasyon sorunu her
    koşuyu başarısız yapar ve tarayıcı %100 skor uydurur.

    Bu kontrol, %100'lük ilk sonucun ardından eklendi — çünkü kör taramada
    sıfır sağ kalan FAZLA İYİ bir sonuçtur (kural Y6).
    """
    gecici = Path(tempfile.mkdtemp(prefix="taban_"))
    try:
        hedef = depoyu_kopyala(gecici / "depo")
        p = subprocess.run(
            [sys.executable, "-m", "pytest", "tests", "-q", "--tb=line",
             "-p", "no:cacheprovider"],
            cwd=hedef, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=900,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"})
        son = [x for x in p.stdout.splitlines()
               if " passed" in x or " failed" in x]
        return p.returncode == 0, (son[-1] if son else p.stdout[-300:])
    finally:
        shutil.rmtree(gecici, ignore_errors=True)


# 🔴 B-151 (SEKIZINCI DENETIM) — ORNEKLEM SAYISI ARTIK ADLANDIRILMIS.
# `tests/test_kapi_secimleri.py::test_b139` `ORNEKLEM = 24` diye ELLE
# tutulan bir sabit tasiyordu ve o sayi bu dosyada YOKTU: aracin
# varsayilani 16'ydi. 24'un tek kaynagi, basliginda
# *"🔴 DURUM: BAYAT ... Bir sayiyi buradan OKUMA"* yazan
# `ciktilar/kor_cikti.txt` idi. Yani BAYATLAMAYI ONLEMEK icin yazilan
# Y12 korumasi, ikinci bir elle tutulan sabit getirmisti.
# 🔒 Tek kaynak burasi; test bunu ICE AKTARIR.
VARSAYILAN_ORNEKLEM = 16


def main() -> None:
    adet = int(sys.argv[1]) if len(sys.argv) > 1 else VARSAYILAN_ORNEKLEM
    havuz = mutantlari_uret()
    rnd = random.Random(TOHUM)
    secilen = rnd.sample(havuz, min(adet, len(havuz)))

    print("=" * 78)
    print("KÖR MUTASYON TARAYICI")
    print("=" * 78)
    print(f"Üretilen mutant havuzu : {len(havuz)}")
    print(f"Bu koşuda sınanan      : {len(secilen)}  (tohum {TOHUM})")
    print(f"Tahmini süre           : ~{len(secilen)*2.6/8:.0f} dk\n")
    print("⚠️ Bu bir KAPI DEĞİLDİR. Eşdeğer mutantlar sağ çıkar ve bu")
    print("   normaldir. Çıktı: skor + ELLE AYIKLANACAK sağ kalan listesi.\n")

    print("TABAN KONTROLU - mutasyonsuz kopyada test paketi geciyor mu?")
    tamam, ozet = taban_kontrolu()
    print(f"  {ozet}")
    if not tamam:
        print()
        print("!! TABAN KIRIK - mutasyonsuz kopyada testler gecmiyor.")
        print("   'Yakalandi' sayimi ANLAMSIZ olurdu; tarama durduruldu.")
        sys.exit(1)
    print("  OK taban temiz - 'yakalandi' sayimi anlamli")
    print()

    t0 = time.perf_counter()
    with Pool(8) as p:
        sonuclar = p.map(_kosu, secilen)

    yakalandi = [r for r in sonuclar if r["durum"] == "yakalandi"]
    sag = [r for r in sonuclar if r["durum"] == "sag_kaldi"]
    gecersiz = [r for r in sonuclar if r["durum"] in ("sozdizimi", "uygulanamadi")]

    gecerli = len(yakalandi) + len(sag)
    print(f"{'sonuç':>12}  {'adet':>5}")
    print("-" * 30)
    print(f"{'yakalandı':>12}  {len(yakalandi):>5}")
    print(f"{'sağ kaldı':>12}  {len(sag):>5}")
    print(f"{'geçersiz':>12}  {len(gecersiz):>5}   (sözdizimi/uygulanamadı)")
    if gecerli:
        print(f"\nMUTASYON SKORU: {100*len(yakalandi)/gecerli:.1f} % "
              f"({len(yakalandi)}/{gecerli})")

    if sag:
        print("\n" + "=" * 78)
        print("SAĞ KALANLAR — ELLE AYIKLANACAK")
        print("=" * 78)
        print("Her biri için sor: davranışı gerçekten değiştiriyor mu?")
        print("  Hayır → eşdeğer mutant, sorun yok")
        print("  Evet  → GERÇEK BOŞLUK, regresyon testi yaz\n")
        for r in sag:
            m = r["m"]
            print(f"  {m.dosya}:{m.satir_no}  [{m.kural}]")
            print(f"      -  {m.eski.strip()[:88]}")
            print(f"      +  {m.yeni.strip()[:88]}")

    print(f"\nSüre: {(time.perf_counter()-t0)/60:.1f} dk")


if __name__ == "__main__":
    main()
