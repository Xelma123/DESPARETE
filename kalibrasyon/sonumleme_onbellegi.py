"""
SÖNÜMLEME ÖNBELLEĞİ — sınır neden var, neden 250 000, ve neden zararsız.

Üretici:
    PYTHONIOENCODING=utf-8 python kalibrasyon/sonumleme_onbellegi.py

🔴 NEDEN BU ÖLÇÜM VAR
=====================
5 Eylül 2026: sönümleme yenilik önbelleği SINIRSIZDI. Hareketli bir kolda
saniyede yüz binlerce girdi biriktiriyor ve tam uzunlukta (350 s) bir koşu
makinenin belleğini aşıyordu. Yani 18 senaryonun 12'si — bütün hareketli
kollar — koşulamıyordu. Statik kolda sönümleme donduğu için önbellek birkaç
bin girdide kalıyor ve sorun GÖRÜNMÜYORDU; bugüne kadarki tam uzunluk
ölçümlerinin hepsi statik koldaydı.

🔒 SINIRLAMANIN ZARARSIZLIĞI YAPISALDIR, ÖLÇÜM DEĞİL
====================================================
`_yenilik`, saf bir fonksiyonun memo'sudur: değer yalnız anahtara bağlıdır.
Bir girdiyi atmak onu yeniden HESAPLATIR. Yine de ölçülür, çünkü kanıtlanan
şey matematik değil UYGULAMADIR.

⚠️ ÖLÇÜMÜN DOĞRU REJİMDE KOŞMASI ŞART
=====================================
Statik kolda sınır hiç devreye girmez; orada yapılan bir "değişmedi"
ölçümü hiçbir şey kanıtlamaz. Bu yüzden aşağıdaki bütün kollar
HAREKETLİDİR ve koşular sınırı defalarca doldurmaya yetecek uzunluktadır.
"""

from __future__ import annotations

import ctypes
import gc
import json
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.cekirdek.rng import normal_cekimi  # noqa: E402
from sim2.kanal import sonumleme as SM  # noqa: E402
from sim2.kanal import yayilim as YM  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.kosum.sonuc import sonuc_satiri  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402
from kalibrasyon import dunya_secimi as DS  # noqa: E402  (K-183)
from kalibrasyon.kahin import EnKisaYolKahin, KanalGrafigi  # noqa: E402

# Sonuç satırının koşudan koşuya MEŞRU olarak değişen alanları.
OYNAK = ("calisma_kimligi", "zaman_damgasi_utc")

# 🔴 BU KAPI 8 EYLÜL'DEN BERİ YANLIŞ ALARM VERİYORDU — 9 Eylül 2026.
# ==================================================================
# Bölüm 2 *"sınırı değiştirmek sonucu değiştiriyor mu"* diye soruyor ve
# cevabı TAM SONUÇ SATIRINI karşılaştırarak veriyordu. K-106 (8 Eylül)
# sonuç satırına `teshis.sonumleme_onbellegi`ni ekledi — yani önbelleğin
# KENDİ durumunu (sınır · tahliye · girdi · ıskalama tahmini). O alan
# sınır değişince **tanım gereği** değişir.
#
# Sonuç: karşılaştırma o günden beri HER SATIRDA `🔴 HAYIR` diyordu ve
# betik ~35 dakika sürdüğü için kimse koşmamıştı. Ölçüldü (9 Eylül,
# `bagimsiz-yok`, tohum 1000, 15 s, sınır 1e9 ↔ 100 000):
#
#     ham teslim dizisi                    : BİREBİR AYNI
#     tam satır                            : farklı
#     `sonumleme_onbellegi` çıkarılınca    : BİREBİR AYNI
#
# 🔒 Yani önbellek gerçekten saf bir memo ve iddia AYAKTA; kırılan şey
# kapıydı. K-109'un kuralı burada geçerli: *doğru çalışan işi kırmızıya
# boyayan bir kapı, kapısızlıktan kötüdür* — insanları kapıyı görmezden
# gelmeye alıştırır.
#
# ⚠️ ALAN KARŞILAŞTIRMADAN ÇIKARILIYOR, RAPORDAN DEĞİL: tahliye ve
# ıskalama sütunları tabloda duruyor, çünkü sınırın FİİLEN devreye
# girdiğini gösteren kanıt onlar. Çıkarılmasaydı kapı boş geçerdi
# (K-110'un `aktarilan_paket = 0` dersi).
TESHIS_OYNAK = ("sonumleme_onbellegi",)


class _Bellek(ctypes.Structure):
    _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                ("ullTotalPhys", ctypes.c_ulonglong),
                ("ullAvailPhys", ctypes.c_ulonglong),
                ("ullTotalPageFile", ctypes.c_ulonglong),
                ("ullAvailPageFile", ctypes.c_ulonglong),
                ("ullTotalVirtual", ctypes.c_ulonglong),
                ("ullAvailVirtual", ctypes.c_ulonglong),
                ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]


def bos_ram_bayt() -> int:
    m = _Bellek()
    m.dwLength = ctypes.sizeof(_Bellek)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return int(m.ullAvailPhys)


def kos(senaryo: str, tohum: int, bitis: float, sinir: int | None = None):
    """Kâhin yönlendirmeli bir koşu. `sinir=None` → modülün varsayılanı."""
    ek: dict[str, object] = {}
    if not senaryo.endswith("-yok"):
        ek["karistirici_guc_override_dbm"] = 0.0
    konfig = DS.konfig(kol="onbellek", senaryo=senaryo, tohum=tohum,
                    isinma_s=0.1 * bitis, olcum_bitis_s=0.85 * bitis,
                    kosu_bitis_s=bitis, **ek)
    kur = kurulum_yap(konfig)
    if sinir is not None:
        kur.kanal.sonumleme._sinir = sinir
    grafik = KanalGrafigi(kur)
    onceki_ram = bos_ram_bayt()
    t0 = time.perf_counter()
    kosu = Kosu(kur, lambda i: EnKisaYolKahin(i, grafik))
    kosu.kostur()
    sure = time.perf_counter() - t0
    kullanilan = onceki_ram - bos_ram_bayt()
    satir = sonuc_satiri(kur, kosu.dugumler, EnKisaYolKahin.ad)
    for alan in OYNAK:
        satir["kimlik"].pop(alan, None)
    for alan in TESHIS_OYNAK:
        satir["teshis"].pop(alan, None)
    # 🔴 EK İMZA: satırın özetlemediği ham teslim dizisi. Satır eşit çıkıp bu
    # farklı çıkarsa, satır yeterince duyarlı değil demektir.
    imza = [(t.kimlik, t.akis_kimligi, repr(t.gecikme_s))
            for t in kur.paket_defteri.kayitlar()]
    rapor = dict(kur.kanal.sonumleme.onbellek_raporu())
    gecerli = bool(satir["korunum"]["gecerli"])
    del kur, kosu, grafik
    gc.collect()
    return satir, imza, sure, rapor, kullanilan, gecerli


def bolum(baslik: str) -> None:
    print("\n" + "=" * 78)
    print(baslik)
    print("=" * 78)


# ==========================================================================
def buyume() -> None:
    """Sınırsız hâlde önbellek ne hızla büyüyor, girdi başına kaç bayt?"""
    bolum("1 - SINIRSIZ BUYUME  (sinir kaldirilir)")
    print(f"  {'kol':<18} {'sim_s':>6} {'girdi':>12} {'girdi/sim_s':>12} "
          f"{'RAM_MB':>9} {'bayt/girdi':>11}")
    for bitis in (20.0, 40.0):
        _, _, _, rapor, ram, _ = kos("bagimsiz-yok", 1000, bitis,
                                     sinir=10 ** 9)
        n = rapor["girdi"]
        print(f"  {'bagimsiz-yok':<18} {bitis:>6.0f} {n:>12,} "
              f"{n / bitis:>12,.0f} {ram / 2 ** 20:>9.0f} "
              f"{ram / max(n, 1):>11.0f}")
    print("\n  🔴 Buyume DOGRUSAL. 350 s'lik bir hareketli kosunun istedigi")
    print("     bellek buradan turetilir ve makinenin RAM'ini asar.")


def sinir_taramasi() -> None:
    """Sinir isabet oranini bozuyor mu? Ve sonuc DEGISIYOR mu?"""
    bolum("2 - SINIR TARAMASI  (isabet, sure ve BIREBIR AYNILIK)")
    kollar = (("bagimsiz-yok", 1000, 20.0),
              ("bagimsiz-surekli", 1001, 15.0),
              ("statik-yok", 1002, 20.0))
    referans: dict[str, tuple] = {}
    print(f"  {'sinir':>10} {'kol':<18} {'sure_s':>7} {'tahliye':>8} "
          f"{'iskalama~':>11} {'iska/sim_s':>11} {'ayni_mi':>8}")
    for sinir in (10 ** 9, 1_000_000, 250_000, 100_000):
        for senaryo, tohum, bitis in kollar:
            satir, imza, sure, rapor, _, _ = kos(senaryo, tohum, bitis, sinir)
            anahtar = f"{senaryo}|{tohum}"
            simdi = (json.dumps(satir, sort_keys=True, default=list), imza)
            if sinir == 10 ** 9:
                referans[anahtar] = simdi
                ayni = "REFERANS"
            else:
                ayni = "EVET" if simdi == referans[anahtar] else "🔴 HAYIR"
            etiket = "sinirsiz" if sinir == 10 ** 9 else f"{sinir:,}"
            print(f"  {etiket:>10} {senaryo:<18} {sure:>7.1f} "
                  f"{rapor['tahliye']:>8} {rapor['iskalama_tahmini']:>11,} "
                  f"{rapor['iskalama_tahmini'] / bitis:>11,.0f} {ayni:>8}")
    print("\n  🔒 'ayni_mi' hem TAM sonuc satirini hem ham teslim dizisini")
    print("     (paket kimligi, akis, tam duyarlikli gecikme) karsilastirir.")


def tam_uzunluk() -> None:
    """🔴 ASIL KAPI: tam uzunlukta bir HAREKETLI kosu artik koşuyor mu?"""
    bolum("3 - TAM UZUNLUK  (350 s hareketli — sinirin var olma sebebi)")
    satir, imza, sure, rapor, ram, gecerli = kos("bagimsiz-yok", 1000, 350.0)
    m = satir["metrikler"]
    print(f"  sure                : {sure:.0f} s")
    # ⚠️ Bos-RAM farki 20+ dakikalik bir kosuda GURULTULU bir alettir:
    # sistemin geri kalani da bellek alip birakir, sayi eksi bile cikabilir.
    # Baglayici kanit bu degil, onbellegin sinirini hic asmamasidir.
    print(f"  bos-RAM farki (gurultulu): {ram / 2 ** 20:.0f} MB")
    print(f"  onbellek girdi/sinir: {rapor['girdi']:,} / {rapor['sinir']:,}")
    print(f"  tahliye             : {rapor['tahliye']:,}")
    print(f"  iskalama~ / sim_s   : {rapor['iskalama_tahmini'] / 350.0:,.0f}")
    print(f"  pdr / psr           : {(m['pdr'] or 0):.3f} / {(m['psr'] or 0):.3f}")
    print(f"  teslim              : {len(imza)}")
    print(f"  korunum + mutabakat : {'TAMAM' if gecerli else '🔴 KIRIK'}")


# 🔒 Gölgeleme köşe önbelleğinin sınır adayları. Varsayılan 1<<19.
KOSE_SINIRLARI: tuple[int, ...] = (1 << 22, 1 << 19, 1 << 14, 1 << 10)


def kose_onbellegi() -> None:
    """🔴 `KOSE_ONBELLEK_SINIRI` SINANMAMIŞTI — kaydı bunu açıkça söylüyordu:
    *"saf memo olduğu için sonucu değiştiremez ama DEĞERİ ölçülmedi;
    sönümleme önbelleğinin aksine birebir aynılık kanıtı yok."*

    🔒 Bu bölüm o kanıtı üretir ve ölçüt ÖNCEDEN yazılıdır: sınır ne olursa
    olsun sonuç satırı ve ham teslim imzası **BİREBİR** aynı çıkmalı. Bir
    fark çıkarsa memo saf değildir ve sınır bir MODEL parametresidir —
    o zaman değeri ayrıca kalibre edilmek zorundadır.

    ⚠️ Hareketli kol seçildi: statik kolda konumlar donduğu için köşeler hiç
    değişmez ve önbellek hiç zorlanmaz — orada ölçmek boş geçmek olurdu.
    """
    bolum("4 - GOLGELEME KOSE ONBELLEGI  (SINANMAMIS sinirin BIREBIR kanitı)")
    varsayilan = YM.KOSE_ONBELLEK_SINIRI
    print(f"  modul varsayilani : {varsayilan:,}")
    print(f"  olcut (ONCEDEN)   : satir VE ham teslim imzasi BIREBIR ayni")
    temel_satir = temel_imza = None
    tamam = True
    try:
        for sinir in KOSE_SINIRLARI:
            YM.KOSE_ONBELLEK_SINIRI = sinir
            satir, imza, sure, _r, _ram, gecerli = kos(
                "bagimsiz-yok", 1000, 50.0)
            if temel_satir is None:
                temel_satir, temel_imza = satir, imza
                durum = "TABAN"
            else:
                ayni = (json.dumps(satir, sort_keys=True, default=str)
                        == json.dumps(temel_satir, sort_keys=True,
                                      default=str)
                        and imza == temel_imza)
                durum = "BIREBIR" if ayni else "🔴 FARKLI"
                tamam &= ayni
            print(f"  sinir {sinir:>10,}  sure {sure:>6.1f} s  "
                  f"teslim {len(imza):>5}  korunum "
                  f"{'TAMAM' if gecerli else '🔴 KIRIK'}  {durum}")
            tamam &= gecerli
    finally:
        YM.KOSE_ONBELLEK_SINIRI = varsayilan
    print(f"  → {'🟢 SAF MEMO KANITLANDI' if tamam else '🔴 KAPI KALDI'}"
          f" — sinir sonucu degistirmiyor" if tamam else "")
    if not tamam:
        raise SystemExit("🔴 kose onbellegi sinira DUYARLI — yukarisi okunmali")


if __name__ == "__main__":
    # 🔒 Bolumler ayri ayri kosulabilir: tamami ~35 dk surer ve isletme
    # kurali 30 dk'yi asan kosumlar icin once soru sorulmasini istiyor.
    #   python kalibrasyon/sonumleme_onbellegi.py 1 2     → ~15 dk
    #   python kalibrasyon/sonumleme_onbellegi.py 3       → ~20 dk
    BOLUMLER = {"1": buyume, "2": sinir_taramasi, "3": tam_uzunluk,
                "4": kose_onbellegi}
    secim = sys.argv[1:] or list(BOLUMLER)
    bilinmeyen = [s for s in secim if s not in BOLUMLER]
    if bilinmeyen:
        raise SystemExit(f"bilinmeyen bolum: {bilinmeyen} — "
                         f"secenekler {sorted(BOLUMLER)}")
    print(f"YENILIK_ONBELLEK_SINIRI (modul varsayilani) = {SM.YENILIK_ONBELLEK_SINIRI:,}")
    for s in secim:
        BOLUMLER[s]()
