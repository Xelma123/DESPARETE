"""OKUMA DENETİMİ — yeni ajan gerekli belgelerin ve kod tabanının HEPSİNİ okudu mu?

Öğrencinin isteği (29 Eylül 2026): devir istemi, yeni ajanın doğru ve gerekli
belgelerin ve kod tabanının hepsini okuduğundan EMİN olmayı sağlamalı.

Liste elle tutulmaz, DEPODAN türer (dosya eklenince bayatlamaz). Ajan okuduğu
her dosyayı okuma defterine yazar (her satır: `yol` — ne yapar, önemli
noktalar, bulduğu çelişki). Bu betik listede olup defterde geçmeyen dosyaları
basar.

    python arsiv/dogrulama/okuma_denetimi.py --liste           # okunacaklar, sırayla
    python arsiv/dogrulama/okuma_denetimi.py <defter.md>       # eksik var mı (çıkış 1)
"""
import sys
from pathlib import Path


def _kok() -> Path:
    burasi = Path(__file__).resolve()
    for aday in [burasi, *burasi.parents]:
        if (aday / "v2" / "04-KARARLAR.md").is_file():
            return aday
    raise SystemExit("depo kökü bulunamadı (v2/04-KARARLAR.md yok)")


KOK = _kok()

# Bugün kullanılan kalibrasyon araçları — TAMAMI satır satır okunur.
AKTIF_ARACLAR = (
    "dunya_secimi.py", "kahin.py", "aodv_uygunluk.py", "kayip_anatomisi.py",
    "regresyon_satirlari.py", "mimari_denetimi.py", "evre_metrikleri_kapilari.py",
    "duyarlilik.py", "cozunurluk.py", "li_replikasyonu.py", "calisma_noktasi.py",
    "ust_referans.py", "karistirici_gucu.py", "kontrol_duzlemi_kapilari.py",
    "anlamlilik_sabitleri.py", "theta_kollari.py",
)

# Proje belgeleri — okuma sırası nedenden nereye.
BELGELER = (
    "DEVIR-PROMPT.md", "README.md", "v2/README.md",
    "v2/01-PROBLEM-VE-AMAC.md", "v2/12-YOL-HARITASI.md", "v2/04-KARARLAR.md",
    "v2/14-REFERANS-DUNYA.md", "v2/07-SIMULATOR-TASARIMI.md",
    "v2/05-GOZLEM-PENCERESI.md", "v2/13-KONTROL-DUZLEMI.md",
    "v2/06-ON-KAYIT.md", "v2/08-EVRE-METRIKLERI.md", "v2/09-LI-REPLIKASYONU.md",
    "v2/03-YONTEM-KURALLARI.md", "v2/02-DOGRULANMIS-KAYNAKLAR.md",
    "v2/16-KAYNAKCA.md", "protokol_kaynaklari/README.md",
)

# DESPARETE tasarım paketi listede YOK (öğrenci, 29 Eylül): öğrencinin ilk
# taslak fikirleri; ajanın bilmesi gereken bugünkü yapı, o da kodda.

KAYNAKLAR = (
    "protokol_kaynaklari/rfc3561_aodv.txt", "protokol_kaynaklari/rfc3626_olsr.txt",
    "protokol_kaynaklari/marina_das_2001_aomdv_icnp.pdf",
)

# sim2/ okuma sırası: çekirdek → dünya → kanal → mac → ağ → gözlem → koşum
# → ölçüm → yapılandırma.
SIM2_SIRA = ("cekirdek", "yapilandirma", "dunya", "kanal", "mac", "ag",
             "gozlem", "kosum", "olcum")


def _py(dizin: Path) -> list[Path]:
    """Boş dosyalar (içi boş `__init__.py`) listeye girmez."""
    return sorted(p for p in dizin.rglob("*.py")
                  if "__pycache__" not in p.parts and p.stat().st_size > 0)


def liste() -> list[tuple[str, list[str]]]:
    """(grup başlığı, yollar) — sırayla okunur."""
    r = lambda p: p.relative_to(KOK).as_posix()  # noqa: E731
    gruplar = [("1 · Belgeler (tamamı)", [b for b in BELGELER
                                          if (KOK / b).is_file()])]
    sim2 = KOK / "sim2"
    yollar = [r(p) for p in sorted(sim2.glob("*.py"))]
    for alt in SIM2_SIRA:
        yollar += [r(p) for p in _py(sim2 / alt)]
    yollar += [r(p) for p in _py(sim2) if r(p) not in yollar]
    gruplar.append(("2 · Simülatör `sim2/` (tamamı, satır satır)", yollar))
    gruplar.append(("3 · Protokoller (tamamı: DESPARETE, AODV, AOMDV, OLSR, "
                    "koşum protokolleri)",
                    [r(p) for p in _py(KOK / "protokoller")]))
    gruplar.append(("4 · Analiz (tamamı)", [r(p) for p in _py(KOK / "analiz")]))
    kal = KOK / "kalibrasyon"
    aktif = [f"kalibrasyon/{a}" for a in AKTIF_ARACLAR if (kal / a).is_file()]
    gruplar.append(("5 · Bugün kullanılan ölçüm araçları (tamamı)", aktif))
    gruplar.append(("6 · Testler `tests2/` (tamamı — sözleşmelerin kendisi)",
                    [r(p) for p in _py(KOK / "tests2")]))
    tarihsel = [r(p) for p in _py(kal) if r(p) not in aktif]
    gruplar.append(("7 · Eski dünyanın kalibrasyon adımları (tamamı; SAYILARI "
                    "BUGÜN GEÇERLİ DEĞİL — yöntemi ve tarihçeyi gösterirler)",
                    tarihsel))
    gruplar.append(("8 · Karar günlüğü: indeks + K-186'dan sona her kayıt",
                    ["v2/kayit/KARAR-GUNLUGU.md"]))
    kaynak = [k for k in KAYNAKLAR if (KOK / k).is_file()]
    gruplar.append(("9 · Taban protokollerin birincil kaynakları — ilgili "
                    "bölümler: RFC 3561 §3–§6, §10 · RFC 3626 §3–§10, §13–§14, "
                    "§18 · Marina–Das 2001 (çok yollu güncelleme kuralı, Şekil 3)",
                    kaynak))
    return gruplar


def main() -> int:
    arg = sys.argv[1:]
    if not arg or arg[0] == "--liste":
        toplam = 0
        for baslik, yollar in liste():
            print(f"\n## {baslik} — {len(yollar)} dosya")
            for y in yollar:
                if y.endswith(".pdf"):
                    print(f"- `{y}` (PDF)")
                    continue
                satir = sum(1 for _ in (KOK / y).open(encoding="utf-8",
                                                      errors="replace"))
                print(f"- `{y}` ({satir} satır)")
            toplam += len(yollar)
        print(f"\nTOPLAM {toplam} dosya")
        return 0
    defter = Path(arg[0])
    metin = defter.read_text(encoding="utf-8")
    eksik = [(b, y) for b, ys in liste() for y in ys if f"`{y}`" not in metin]
    toplam = sum(len(ys) for _, ys in liste())
    print(f"okuma defteri: {defter} · listede {toplam} dosya · defterde "
          f"geçmeyen {len(eksik)}")
    for b, y in eksik:
        print(f"  EKSIK  [{b.split(' · ')[0]}] {y}")
    print("TAMAM — bütün liste defterde" if not eksik else "EKSİK VAR")
    return 1 if eksik else 0


if __name__ == "__main__":
    raise SystemExit(main())
