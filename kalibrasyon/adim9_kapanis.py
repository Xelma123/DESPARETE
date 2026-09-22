"""
Adım 9 kapanışı — `kosum/`. Uçtan uca bir koşu, defter ve BÜTÇE.

Üretici:
    PYTHONIOENCODING=utf-8 python kalibrasyon/adim9_kapanis.py

Üç şey ölçülür:

  1. UÇTAN UCA   tam uzunlukta (350 s) gerçek koşular, gerçek `.jsonl`
                 satırları, korunum + mutabakat kapıları.
  2. BÜTÇE       koşu maliyeti neye orantılı? Tarama planı buna dayanacak.
  3. KARIŞTIRILMIŞ KOLDA KORUNUM — defter, karıştırıcı DEVREDEYKEN de
                 kapanıyor mu? Bölüm 1'in altı koşusunun altısı da
                 `statik-yok`tur; yani 8 Eylül'e kadar korunum defteri
                 karıştırılmış bir tam uzunluk koşusunda hiç sınanmadı.

🔴 BÖLÜM 3 DEĞİŞTİ — 8 Eylül 2026 sonrası denetim
=================================================
Eskiden burada *"KARIŞTIRICI GÜCÜ — kalibre edilmedi, burası ilk bakış"*
diye bir tablo vardı ve **iki ayrı şekilde ölüydü**:

  1. Ölçütü BAYATTI. O bölüm *"teslim oranını dinamik aralığın ortasına
     getiren güç; kısıt ulaşılabilirlik ≥ %90"* ölçütünü ilan ediyordu.
     O ölçüt `kalibrasyon/karistirici_gucu.py`de ÇÜRÜTÜLDÜ ve yerine
     *"30 tohumun hiçbirinde birden fazla çok üyeli bileşen yokken ρ en
     büyük"* geldi (K-103). Depoda aynı sayı için iki ayrı ölçüt duruyordu.
  2. Ölçümü BOŞTU. `bitis = 10 s` ile koşuyordu, karıştırıcı ise
     `karistirici_baslangic_s = 150 s`te devreye giriyor. Yani dokuz satırın
     dokuzu da KAPALI bir karıştırıcı ölçüyordu.

🔒 Yerine gerçek bir kapı kondu ve `_kos` artık bu hatayı YAPISAL olarak
engelliyor: karıştırıcılı bir senaryo, karıştırıcı devreye girmeden biten
bir koşuyla istenirse **patlar**.

🔴 BURADA KULLANILAN PROTOKOLLER TABAN ÇİZGİSİ DEĞİLDİR
=======================================================
`protokoller/kosum_kosumu.py` simülatörün test aletidir. Bütçe sayıları
gerçek bir yönlendirme protokolüyle değişecek; bu yüzden aşağıda saniye
değil, **iletim başına maliyet** raporlanır.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from protokoller.kosum_kosumu import DogrudanKomsu, EnYakinKimlik  # noqa: E402
from sim2.cekirdek.degismezler import dogrula  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.kosum.sonuc import SatirYazici, sonuc_satiri  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402
from sim2.yapilandirma.senaryolar import KARISTIRICI_SINIFLARI  # noqa: E402

CIKTI = KOK / "ciktilar2" / "adim9_kapanis.jsonl"


def _kos(senaryo, protokol, tohum, bitis=None, **ek):
    # 🔴 GÜÇ ARTIK ÖLÇÜLDÜ — `setdefault(..., 0.0)` KALKTI.
    # `senaryolar.KARISTIRICI_GUCU_DBM` 8 Eylül 2026'da dolduruldu
    # (−15,0 dBm). Buradaki eski varsayılan onu EZİYORDU: her karıştırıcılı
    # koşu, kalibre edilmiş çalışma noktasının 15 dB üstünde koşuyordu —
    # taramada −6 dBm'in bile 30 tohumun 19'unda ağı ikiye ayırdığı bir
    # yerde. Override isteyen artık AÇIKÇA vermek zorunda.
    if bitis is not None:
        ek.update(isinma_s=0.2 * bitis, olcum_bitis_s=0.8 * bitis,
                  kosu_bitis_s=bitis)
    konfig = Konfig(kol="adim9", senaryo=senaryo, tohum=tohum, **ek)
    # 🔴 KAPI: karıştırıcı devreye girmeden biten bir koşu, karıştırıcıyı
    # ÖLÇMÜŞ SAYILMAZ. Bu betiğin iki bölümü tam olarak bu yüzden sessizce
    # boşalmıştı; kapı olmasa üçüncüsü de aynı yoldan geçerdi.
    if konfig.karistirici_sinifi != "yok":
        dogrula(konfig.kosu_bitis_s > konfig.karistirici_baslangic_s,
                f"'{senaryo}' kosusu {konfig.kosu_bitis_s:.1f} s'de bitiyor "
                f"ama karistirici {konfig.karistirici_baslangic_s:.1f} s'de "
                "devreye giriyor: bu kosu KAPALI bir karistirici olcer")
    kur = kurulum_yap(konfig)
    t0 = time.perf_counter()
    kosu = Kosu(kur, lambda i: protokol())
    kosu.kostur()
    return kur, kosu, time.perf_counter() - t0


def bolum(baslik: str) -> None:
    print("\n" + "=" * 74)
    print(baslik)
    print("=" * 74)


# ==========================================================================
def uctan_uca() -> bool:
    """Tam uzunlukta koşular — gerçek çalışma noktası, gerçek `.jsonl`."""
    bolum("1 - UCTAN UCA  (350 s, 40 dugum, varsayilan calisma noktasi)")
    CIKTI.unlink(missing_ok=True)
    tamam = True
    print(f"  {'tohum':>6} {'sure_s':>7} {'olay':>9} {'uretilen':>9} "
          f"{'teslim':>7} {'pdr':>7} {'psr':>7}  gecerli")
    with SatirYazici(CIKTI) as yazici:
        for tohum in range(1000, 1006):
            kur, kosu, sure = _kos("statik-yok", DogrudanKomsu, tohum)
            satir = sonuc_satiri(kur, kosu.dugumler, DogrudanKomsu.ad)
            yazici.yaz(satir)
            k, m = satir["korunum"], satir["metrikler"]
            tamam &= bool(k["gecerli"])
            pdr = m["pdr"] or 0.0
            psr = m["psr"] or 0.0
            print(f"  {tohum:>6} {sure:>7.1f} "
                  f"{int(kur.sayaclar.oku('islenen_olay')):>9} "
                  f"{k['uretilen']:>9} {k['teslim']:>7} "
                  f"{pdr:>7.3f} {psr:>7.3f}  {k['gecerli']}")
    satir_sayisi = len(CIKTI.read_text(encoding="utf-8").splitlines())
    print(f"\n  yazilan satir : {satir_sayisi}  ->  {CIKTI.name}")
    print(f"  korunum + mutabakat : {'HEPSI TAMAM' if tamam else 'KIRIK'}")
    return tamam


# ==========================================================================
def butce() -> None:
    """Maliyet neye orantılı? Tarama planı buna dayanacak."""
    bolum("2 - BUTCE  (maliyet ILETIM basina, saniye degil)")
    print(f"  {'senaryo':<18} {'protokol':<16} {'bitis':>6} {'sure_s':>8} "
          f"{'iletim':>8} {'us/iletim':>10}")
    olculen = []
    # 🔴 KARIŞTIRICILI SATIR AÇILMA ANINI DA TAŞIMAK ZORUNDA. Eskiden
    # `bitis = 10 s` ile koşuyordu ve karıştırıcı 150 s'de devreye girdiği
    # için satır aslında `bagimsiz-yok`un kopyasıydı: ölçülen maliyet
    # karıştırıcının maliyetini HİÇ içermiyordu. Hareketli bir kolu 150 s
    # koşturmak dakikalar sürdüğü için doğru düzeltme koşuyu uzatmak değil,
    # AÇILMA ANINI bu ölçüme taşımaktır — burada aranan şey çalışma noktası
    # değil, iletim başına maliyettir.
    for senaryo, protokol, bitis, ek in (
            ("statik-yok", DogrudanKomsu, 60.0, {}),
            ("statik-yok", EnYakinKimlik, 10.0, {}),
            ("bagimsiz-yok", EnYakinKimlik, 10.0, {}),
            ("bagimsiz-reaktif", EnYakinKimlik, 10.0,
             dict(karistirici_baslangic_s=2.0))):
        kur, _, sure = _kos(senaryo, protokol, 1000, bitis=bitis, **ek)
        iletim = (kur.sayaclar.oku("mac_deneme")
                  + kur.sayaclar.oku("kontrol_cerceve"))
        us = 1e6 * sure / max(iletim, 1)
        olculen.append(us)
        print(f"  {senaryo:<18} {protokol.ad:<16} {bitis:>6.0f} {sure:>8.1f} "
              f"{int(iletim):>8} {us:>10.0f}")
    print("\n  🔒 Maliyet iletim sayısına orantılı; iletim sayısı da")
    print("     protokolün ne kadar konuştuğuna. Gerçek bir yönlendirme")
    print("     protokolü koşum aletinden AZ konuşur, çünkü koşum aleti")
    print("     paketleri döngüye sokuyor. Tarama bütçesi Adım 11'de,")
    print("     gerçek protokolle yeniden ölçülmeli.")
    ort = sum(olculen) / len(olculen)
    print(f"\n  ortalama {ort:.0f} us/iletim  ·  1 milyon iletim ≈ "
          f"{ort:.0f} saniye")


# ==========================================================================
def karistirilmis_korunum() -> bool:
    """🔴 DEFTER, KARIŞTIRICI DEVREDEYKEN DE KAPANIYOR MU?

    Bölüm 1'in altı koşusunun altısı da `statik-yok`tur. Yani korunum ve
    mutabakat kapıları bugüne kadar **karıştırıcısız** bir dünyada sınandı.
    Karıştırıcı girişim yoluna, taşıyıcı dinlemeye ve (aldatıcı sınıfta)
    geri çekilmeye dokunuyor; defterin orada da kapandığı bir İDDİA idi.

    🔒 GÜÇ OVERRIDE YOK: koşular kalibre edilmiş çalışma noktasında
    (`senaryolar.KARISTIRICI_GUCU_DBM` → −15,0 dBm taban) koşar. Sınanan
    şey, gerçekten koşulacak olan konfigürasyondur.

    🔒 UZUNLUK: `bitis = 200 s` → ısınma 40 · ölçüm 160 · koşu 200.
    Karıştırıcı 150 s'de devreye girdiği için ölçüm penceresinin son 10 s'si
    KARIŞTIRILMIŞ evrededir. Tam uzunluk (350 s) gerekmiyor — sınanan şey
    çalışma noktası değil, defterin karıştırılmış yolda kapanması.
    """
    bolum("3 - KARISTIRILMIS KOLDA KORUNUM  (calisma noktasi, override YOK)")
    tamam = True
    print(f"  {'senaryo':<20} {'sure_s':>7} {'uretilen':>9} {'teslim':>7} "
          f"{'dusen':>7} {'pdr':>7}  gecerli")
    for sinif in [s for s in KARISTIRICI_SINIFLARI if s != "yok"]:
        senaryo = f"statik-{sinif}"
        kur, kosu, sure = _kos(senaryo, EnYakinKimlik, 1000, bitis=200.0)
        satir = sonuc_satiri(kur, kosu.dugumler, EnYakinKimlik.ad)
        m, k = satir["metrikler"], satir["korunum"]
        tamam &= bool(k["gecerli"])
        # `dusen` bir SAYI DEĞİL, sebep kırılımıdır (ttl · hedef_yok ·
        # iletim_basarisiz · kuyruk_tasmasi). Toplamı yazılır.
        dusen = sum(k["dusen"].values())
        print(f"  {senaryo:<20} {sure:>7.1f} {k['uretilen']:>9} "
              f"{k['teslim']:>7} {dusen:>7} "
              f"{(m['pdr'] or 0.0):>7.3f}  {k['gecerli']}")
    print(f"\n  korunum + mutabakat (5 sinif, karistirilmis) : "
          f"{'HEPSI TAMAM' if tamam else 'KIRIK'}")
    print("  ⚠️ PDR sutunu bir SONUC DEGILDIR: kosum aletiyle, tek tohumla,")
    print("     200 s'de alindi. Burada aranan tek sey defterin kapanmasi.")
    return tamam


if __name__ == "__main__":
    # 🔒 Bölüm seçilebilir: `python kalibrasyon/adim9_kapanis.py 3`.
    # Üç bölümü de koşmak ~30 dk; tek bir bölümü doğrulamak için hepsini
    # tekrar koşturmak, ölçüm maliyetini gereksiz yere sonuca katar.
    _secim = set(sys.argv[1:]) or {"1", "2", "3"}
    _bilinmeyen = _secim - {"1", "2", "3"}
    if _bilinmeyen:
        raise SystemExit(f"bilinmeyen bolum: {sorted(_bilinmeyen)}")
    tamam = uctan_uca() if "1" in _secim else None
    if "2" in _secim:
        butce()
    kirli_tamam = karistirilmis_korunum() if "3" in _secim else None
    bolum("SONUC")
    print("  Adim 9 kapanis olcutleri:")

    # 🔴 KOSULMAYAN BIR OLCUT "KIRIK" DEGILDIR. Bolum secimi eklenince
    # `None` degeri sessizce "KIRIK" yaziyordu; yani olculmemis bir sey
    # basarisiz gibi raporlanacakti. Uc durum var, iki degil.
    def _durum(deger) -> str:
        return "KOSULMADI" if deger is None else ("TAMAM" if deger
                                                  else "KIRIK")

    print(f"    korunum + mutabakat (6 tohum, tam uzunluk) : {_durum(tamam)}")
    print(f"    korunum + mutabakat (5 sinif, karistirilmis): "
          f"{_durum(kirli_tamam)}")
    print("    kosu.py <= 150 kod satiri                   : teste bagli")
    print("    sonuc.py'de sozluk literali yok             : teste bagli")
    print("    satir basina fsync                          : SatirYazici")
