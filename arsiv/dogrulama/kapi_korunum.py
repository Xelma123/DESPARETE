"""
Ç1 KAPISI — korunum denklemi, gerçek MAC yolundan.

    Ç1.1  6 senaryo × 3 trafik × 30 tohum = 540 koşu, korunum 540/540
    Ç1.2  dört düşme sebebinin HER BİRİ en az bir yapılandırmada tetikleniyor
    Ç1.4  boşaltma sonunda boruda kalan paket oranı < %1

Ç1.3 (mutasyon kontrolü) ayrı dosyada: `mutasyon_paketi.py`.

Kullanım:
    python dogrulama/kapi_korunum.py
"""

from __future__ import annotations

import sys
import time
from dataclasses import replace
from multiprocessing import Pool, cpu_count
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dogrulama.aktaricilar import AKTARICILAR  # noqa: E402
from sim.config import SENARYOLAR, TRAFIK_SEVIYELERI, Konfig  # noqa: E402
from dogrulama.olcum import (aktif_yazici, kayit, olc,  # noqa: E402
                            yaz_sonuc)

# 🔴 KAPI KOSULARI AYARLAMA TOHUMLARINDA KOSAR (1-30).
# Ana deney tohumlari (2000-2029) muhurden once HICBIR amacla kosulmaz;
# korunum dogrulamasi da bir "amac"tir. Bkz. K-025.
KAPI_TOHUMLARI = range(1, 31)
CEKIRDEK = min(10, cpu_count())           # K-002: 10 çekirdek


# --------------------------------------------------------------------------
# Ç1.2 — uç durum yapılandırmaları
#
# Normal parametrelerde yalnızca `iletim_basarisiz` tetikleniyor. Diğer üç
# sebebin de tetiklendiğini göstermek zorundayız; yoksa o kod yolları HİÇ
# koşulmamış olur ve orada sessiz bir kayıp saklanabilir.
# --------------------------------------------------------------------------
UC_DURUMLAR = [
    ("dar_kuyruk",   dict(kuyruk_kapasitesi=1, trafik="yogun",
                          cbr_araligi_s=0.05), "en_kisa_yol",  "kuyruk_tasmasi"),
    ("kisa_ttl",     dict(ttl_baslangic=2),     "dongu_yapan",  "ttl"),
    ("rota_yok",     dict(),                    "olu",          "hedef_yok"),
    ("denemesiz",    dict(yeniden_deneme_siniri=0, senaryo="S2"),
                                                "en_kisa_yol",  "iletim_basarisiz"),
]


def _kosu(arg) -> tuple[dict, dict]:
    """🔴 İŞÇİ — yazıcısız ölçer, TAM `sonuc` sözlüğünü DÖNDÜRÜR (D-13).

    Eski hâli özeti burada çıkarıyor ve tam sonucu ATIYORDU. İki kusur
    birleşti: `spawn` altında alt sürecin `olcum._AKTIF[0]`ı `None`dır,
    yani `olc()` satır yazmaz — ve yazılacak sonuç zaten geri
    dönmüyordu. Sonuç: kapının **540 koşusu** hiçbir yere kaydolmadı
    (`aile0_kapi_raporu.jsonl` = 0 bayt) ve kapı yine 13/13 dedi.

    🔒 Yazıcı bir dosya tanıtıcısı taşır, picklenemez; alt sürece
    GEÇİRİLEMEZ. Tek doğru şekil: işçi döndürür, ebeveyn yazar.
    """
    senaryo, trafik, tohum, aktarici_adi, ek = arg
    kon = Konfig(kol=f"kapi_{aktarici_adi}", senaryo=senaryo,
                 trafik=trafik, tohum=tohum, **ek)
    sonuc = olc(kon, AKTARICILAR[aktarici_adi], aktarici=aktarici_adi)
    return ({"senaryo": senaryo, "trafik": trafik, "tohum": tohum,
             "aktarici": aktarici_adi}, sonuc)


def _ozet(et: dict, s: dict) -> dict:
    """Kapının Ç1 yüklemlerinin okuduğu özet — TAM SONUÇTAN türetilir.

    Ayrı bir fonksiyon çünkü artık iki tüketici var: özet (kapı) ve
    satır (sözleşme 5). İkisi aynı koşudan çıkmak zorunda; ayrı
    koşulardan çıksalardı `03` B5'in *"ikinci doğru kaynağı"* tuzağı
    doğardı.
    """
    r = s["korunum"]
    return {
        **et,
        "korunum_tamam": r["korunum_tamam"], "fark": r["fark"],
        "dusen": r["dusen"], "uretilen": r["uretilen"],
        "boruda_kalan": s["boruda_kalan"],
        "teslim_orani": s["teslim_orani"],
        "yakinsadi": s["yakinsama"]["yakinsadi"],
        "en_buyuk_fark": s["yakinsama"]["en_buyuk_fark"],
    }


def _havuzda_kos(isler: list[tuple], **ek_etiket) -> list[dict]:
    """🔒 D-13'ÜN DÜZELTMESİ — İŞÇİLER DÖNDÜRÜR, EBEVEYN YAZAR.

    Şekli tahmin değil: `dogrulama/literatur_eksenleri.py` bu deseni
    **300 işte 300 satır** yazarak ölçtü (`10` §7b).

    🔴 İDDİA ÜRETİM YOLUNDA DOĞRULANIYOR. `assert` yalnızca bir yazıcı
    BEKLENİYORSA kurulur: birim testler yazıcısız çağırır ve orada
    "0 satır" doğru davranıştır. Ayrım `aktif_yazici()` ile yapılır —
    yoksa iddia ya sürekli patlar ya hiç konuşmaz (Y7).
    """
    yazici_bekleniyor = aktif_yazici() is not None
    ozetler: list[dict] = []
    yazilan = 0
    # 🔴 İŞÇİ SAYISI İŞ SAYISINI AŞMAZ. Uç durum matrisi havuz başına
    # yalnızca **5** iş taşıyor; `Pool(10)` Windows `spawn` altında 10
    # süreç doğurup yarısını boş bekletiyordu. Kapının ölçtüğü hiçbir
    # şey değişmez, doğan süreç sayısı değişir.
    with Pool(min(CEKIRDEK, len(isler))) as p:
        # `imap` (sırasız değil): satır sırası koşudan koşuya değişmesin.
        for et, sonuc in p.imap(_kosu, isler, chunksize=1):
            if yaz_sonuc(sonuc, **et, **ek_etiket):
                yazilan += 1
            ozetler.append(_ozet(et, sonuc))
    if yazici_bekleniyor:
        assert yazilan == len(isler), (
            f"yazılan satır ({yazilan}) iş sayısına ({len(isler)}) eşit "
            f"değil — D-13 sınıfı bir kaçak var: koşu yapıldı, sözleşme 5 "
            f"sağlanmadı.")
    return ozetler


def ana_matris(tohumlar=None, senaryolar=None, trafikler=None) -> list[dict]:
    """Ç1.1'in ana matrisi. Varsayılanlar **birebir** bugünkü kapı matrisi.

    ⚠️ Parametreler yalnızca DAVRANIŞSAL TEST içindir: D-13'ün koruması
    satır sayısını ölçmek zorunda ve bunu 540 koşu koşmadan yapabilmeli.
    Kapı hiçbirini vermez, yani kapının ölçtüğü şey değişmez.
    """
    isler = [(sen, tr, t, "en_kisa_yol", {})
             for sen in (SENARYOLAR if senaryolar is None else senaryolar)
             for tr in (TRAFIK_SEVIYELERI if trafikler is None else trafikler)
             for t in (KAPI_TOHUMLARI if tohumlar is None else tohumlar)]
    return _havuzda_kos(isler, matris="ana")


def uc_durum_matrisi() -> list[tuple[str, str, list[dict]]]:
    cikti = []
    for ad, ham_ek, aktarici, beklenen in UC_DURUMLAR:
        # 🔴 KOPYA ÜZERİNDE ÇALIŞ (denetim §7-2).
        # Önceki hâli `ek.pop("senaryo", …)` ile MODÜL SEVİYESİNDEKİ
        # `UC_DURUMLAR` sözlüğünü kalıcı olarak değiştiriyordu. Tek çağrıda
        # zararsızdı (çıkarılan değer varsayılanla aynıydı), ama
        # `uc_durum_matrisi()` iki kez çağrılırsa ya da bir uç durumun
        # senaryosu "S2"den farklı yazılırsa İKİNCİ ÇAĞRI SESSİZCE BAŞKA
        # BİR SENARYO KOŞARDI. Denetçi bunu "bilinçli mi, fark edilmemiş mi
        # belirleyemedim" diye bırakmıştı; fark edilmemiş.
        ek = dict(ham_ek)
        senaryo = ek.pop("senaryo", "S2")
        isler = [(senaryo, ek.get("trafik", "orta"), t, aktarici,
                  {k: v for k, v in ek.items() if k != "trafik"})
                 for t in list(KAPI_TOHUMLARI)[:5]]
        cikti.append((ad, beklenen,
                      _havuzda_kos(isler, matris="uc_durum", uc_durum=ad)))
    return cikti


def main() -> None:
    print("=" * 74)
    print("Ç1 KAPISI — korunum denklemi, gerçek MAC yolundan")
    print("=" * 74)

    t0 = time.perf_counter()
    ana = ana_matris()
    ana_sure = time.perf_counter() - t0

    tutan = sum(1 for r in ana if r["korunum_tamam"])
    print(f"\n--- Ç1.1  ana matris ({len(ana)} koşu, {ana_sure:.0f} s) ---")
    print(f"    korunum tutan koşu : {tutan}/{len(ana)}")
    if tutan != len(ana):
        for r in ana:
            if not r["korunum_tamam"]:
                print(f"    🔴 {r['senaryo']}/{r['trafik']}/{r['tohum']} "
                      f"fark={r['fark']}")

    print(f"\n--- Ç1.4  boşaltma ---")
    oranlar = [r["boruda_kalan"] / r["uretilen"] for r in ana if r["uretilen"]]
    print(f"    boruda kalan / üretilen : en büyük {max(oranlar)*100:.3f} %")

    print(f"\n--- yakınsama (K5, bilgi amaçlı) ---")
    yakinsamayan = [r for r in ana if r["yakinsadi"] is False]
    print(f"    yakınsamayan koşu : {len(yakinsamayan)}/{len(ana)}")
    if yakinsamayan:
        en_kotu = max(yakinsamayan, key=lambda r: r["en_buyuk_fark"])
        print(f"    en büyük dilim farkı : {en_kotu['en_buyuk_fark']:.4f} "
              f"({en_kotu['senaryo']}/{en_kotu['trafik']})")

    print(f"\n--- Ç1.2  düşme sebeplerinin tetiklenmesi ---")
    toplam = {}
    for r in ana:
        for s, v in r["dusen"].items():
            toplam[s] = toplam.get(s, 0) + v
    print("    ana matriste:")
    for s, v in sorted(toplam.items()):
        print(f"      {s:20s} {v:8d}  {'✅' if v else '❌ tetiklenmedi'}")

    uc = uc_durum_matrisi()
    print("    uç durumlarda:")
    tetiklenen = set(s for s, v in toplam.items() if v)
    for ad, beklenen, sonuclar in uc:
        v = sum(r["dusen"][beklenen] for r in sonuclar)
        kor = all(r["korunum_tamam"] for r in sonuclar)
        if v:
            tetiklenen.add(beklenen)
        print(f"      {ad:14s} → {beklenen:20s} {v:8d}  "
              f"{'✅' if v else '❌'}   korunum {'✅' if kor else '🔴'}")

    print("\n" + "=" * 74)
    eksik = set(toplam) - tetiklenen
    print(f"Ç1.1  korunum 540/540          : {'✅' if tutan == len(ana) else '🔴 GEÇMEDİ'}")
    print(f"Ç1.2  dört sebep de tetiklendi : "
          f"{'✅' if not eksik else '🔴 eksik: ' + str(eksik)}")
    print(f"Ç1.4  boruda kalan < %1        : "
          f"{'✅' if max(oranlar) < 0.01 else '🔴 GEÇMEDİ'}")


if __name__ == "__main__":
    with kayit("kapi_korunum"):
        main()
