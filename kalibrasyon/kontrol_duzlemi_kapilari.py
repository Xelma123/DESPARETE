"""
KONTROL DÜZLEMİ KAPILARI — P1–P8, TAM BOYUTLU dünyada gerçek kontrol trafiğiyle.

Üretici:
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/kontrol_duzlemi_kapilari.py

🔒 BAĞLAYICI KAPILAR TESTLERDİR (`tests2/test_kontrol_duzlemi.py`); bu betik
aynı kapıları 40 düğümlük çalışma noktasında koşturur ve KANITINI sayıyla
basar. Casus (bağımsız gözlem) testtekinin AYNISIDIR — içe aktarılır, ikinci
bir gerçeklemesi yazılmadı.

⚠️ Senaryo ayarları `main()` içinde durur ve bir kalibrasyon sayısı DEĞİLDİR:
hiçbir köken kaydı bu betiğin çıktısına dayanmaz. Kapılar istatistiksel değil,
KESİN eşitliklerdir; tohum sayısı bir karar belirlemez.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parent.parent
for _y in (KOK, KOK / "tests2"):
    if str(_y) not in sys.path:
        sys.path.insert(0, str(_y))

from sim2.gozlem.pencere import (IZINLI_GOZLEM_ALANLARI,  # noqa: E402
                                 IZINLI_KOMSU_ALANLARI, IZINLI_PAKET_ALANLARI)
from sim2.gozlem.protokol import KontrolluProtokol  # noqa: E402
from sim2.kosum import kontrol as KM  # noqa: E402
from sim2.kosum.kontrol_durum import (KontrolDuzlemiHatasi,  # noqa: E402
                                      UyandirmaTavaniAsildi)
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.kosum.sonuc import sonuc_satiri  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402
import test_kontrol_duzlemi as T  # noqa: E402


def _kos(kfg, fabrika_uret, casus_ile: bool):
    mp = pytest.MonkeyPatch()
    casus = T.Casus(mp) if casus_ile else None
    try:
        kur = kurulum_yap(kfg)
        kayit = T.yeni_kayit()
        kosu = Kosu(kur, fabrika_uret(kayit))
        kosu.kostur()
        satir = sonuc_satiri(kur, kosu.dugumler, "kontrol_sinav")
    finally:
        mp.undo()
    return kur, satir, kayit, casus


def _kanit(ad: str, kfg) -> dict:
    kur, satir, kayit, c = _kos(
        kfg, lambda k: (lambda i: T.SinavProtokolu(i, k)), True)
    s, k = satir["metrikler"], satir["korunum"]
    d = satir["teshis"]["kontrol_duzlemi"]["defter"]
    kt = ("beacon", "onay", "kontrol")
    n_kontrol = sum(1 for _, t, *_ in c.iletimler if t == "kontrol")
    p1 = (s["kontrol_bayt"] == sum(b for _, t, b, _, _ in c.iletimler if t in kt)
          and abs(s["kontrol_airtime_s"]
                  - sum(x for _, t, _, x, _ in c.iletimler if t in kt)) < 1e-9
          and s["veri_bayt"] == sum(b for _, t, b, _, _ in c.iletimler
                                    if t == "veri")
          and d["iletim"] == n_kontrol and n_kontrol > 0)
    konay = sum(1 for _, cb, a in c.olaylar
                if cb.__name__ == "gonder" and a and a[-1][0] == "konay")
    yeniden = d["iletim"] - (d["yayin_gonderilen"] + d["unicast_onaylanan"]
                             + d["unicast_vazgecilen"] + k["kontrol_ucusta"])
    beklenen, gorulen, kayip, baska = [], set(), 0, 0
    for n, g, istek, no, ok in c.kontrol_alimlari:
        if not ok:
            kayip += 1
            continue
        if not istek.yayin_mi and istek.hedef != n:
            baska += 1
            continue
        if not istek.yayin_mi:
            if (n, g, no) in gorulen:
                continue
            gorulen.add((n, g, no))
        beklenen.append((n, g, istek.bicim.ad, dict(istek.yuk)["sira"],
                         istek.yayin_mi))
    per = [(z, a) for z, cb, a in c.olaylar if cb is KM._zamanlayici_ates]
    zincir: dict = {}
    for z, (_k, n, e, p) in per:
        zincir.setdefault((n, e), []).append((z, p))
    zincir_ok = all(0.0 <= a[0][0] < a[0][1]
                    and all(y[0] == x[0] + x[1] for x, y in zip(a, a[1:]))
                    for a in zincir.values())
    istek_anlari: dict = {}
    for n, _e, saat, g in kayit["dinamik_istek"]:
        istek_anlari.setdefault(n, []).append(saat + g)
    dinamik_hata = max((min(abs(saat - x) for x in istek_anlari[n])
                        for n, _e, saat in kayit["dinamik_ates"]), default=0.0)
    return {
        "ad": ad, "n_kontrol": n_kontrol, "p1": p1,
        "konay": konay, "konay_beklenen": d["teslim_unicast"]
        + d["tekrar_bastirilan"], "yeniden": yeniden,
        "teslim": len(kayit["teslim"]), "p3": sorted(kayit["teslim"])
        == sorted(beklenen), "kayip": kayip, "baska": baska,
        "baska_defter": d["baskasina_adresli"],
        "periyodik": len(kayit["periyodik"]), "zincir_ok": zincir_ok,
        "dinamik": len(kayit["dinamik_ates"]), "dinamik_hata": dinamik_hata,
        "ayrim_ok": ({e for _, e, _ in kayit["periyodik"]}
                     == {"hello", "sessiz"}
                     and {e for _, e, _ in kayit["dinamik_ates"]}
                     == {"zaman_asimi"}),
        "tepe_bekleyen": satir["teshis"]["kontrol_duzlemi"][
            "tepe_bekleyen_uyandirma"],
        "veri_defteri": bool(k["korunum_tamam"] and k["mutabakat_tamam"]
                             and k["iletim_sonucu_tamam"]),
        "kontrol_defteri": bool(k["kontrol_mesaj_tamam"]
                                and k["kontrol_uyandirma_tamam"]),
        "gecerli": bool(k["gecerli"]), "defter": d,
        "metrik": {a: s[a] for a in ("mac_deneme", "teslim_paket",
                                     "alim_red_mesgul")},
        "kfg": kfg,
    }


def main() -> None:
    tam = dict(isinma_s=5.0, karistirici_baslangic_s=20.0, olcum_bitis_s=55.0,
               kosu_bitis_s=60.0)
    senaryolar = (("statik-surekli", 1000), ("bagimsiz-surekli", 1001))
    print("=" * 78)
    print("KONTROL DUZLEMI KAPILARI — 40 dugum, gercek kontrol trafigi")
    print("=" * 78)
    kanitlar = []
    for senaryo, tohum in senaryolar:
        kfg = Konfig(kol="kontrol_kapi", senaryo=senaryo, tohum=tohum, **tam)
        print(f"  kosuluyor: {senaryo} · tohum {tohum} · {tam['kosu_bitis_s']} s")
        kanitlar.append(_kanit(senaryo, kfg))

    ikiz = _kos(kanitlar[0]["kfg"], lambda k: (lambda i: T.VeriIkizi(i)),
                False)[1]["metrikler"]
    ikiz_farkli = {a: ikiz[a] for a in kanitlar[0]["metrik"]} \
        != kanitlar[0]["metrik"]

    def tavan():
        try:
            T._kos(bitis=5.0, fabrika=lambda i: T.Tasan(i, T.yeni_kayit()))
        except UyandirmaTavaniAsildi as h:
            return str(h)
        return None
    t1, t2 = tavan(), tavan()

    kismi_red = False
    try:
        T._kos(bitis=5.0, fabrika=lambda i: type(
            "Kismi", (T.VeriIkizi,), {"__slots__": (),
                                     "zamanlayicilar": lambda self: {}})(i))
    except KontrolDuzlemiHatasi:
        kismi_red = True
    a, b = T._satir_json(**T.KAYIPLI), T._satir_json(**T.KAYIPLI)

    for k in kanitlar:
        d = k["defter"]
        print()
        print(f"--- {k['ad']} ---")
        print(f"  P1 bedel      : kontrol iletimi {k['n_kontrol']} · sayac == havaya "
              f"cikan (bayt/sure/cerceve) : {'EVET' if k['p1'] else 'HAYIR'}")
        print(f"  P2 MAC        : konay {k['konay']} == unicast teslim+tekrar "
              f"{k['konay_beklenen']} · yeniden deneme {k['yeniden']}")
        print(f"  P3 teslim     : teslim {k['teslim']} · fiziksel basariyla birebir "
              f"{'EVET' if k['p3'] else 'HAYIR'} · kayip alim {k['kayip']} · "
              f"baskasina {k['baska']}=={k['baska_defter']}")
        print(f"  P4 zamanlayici: periyodik {k['periyodik']} (zincir "
              f"{'kesin' if k['zincir_ok'] else 'BOZUK'}) · dinamik {k['dinamik']}"
              f" (en buyuk anlik hata {k['dinamik_hata']:.2e} s) · ayrim "
              f"{'EVET' if k['ayrim_ok'] else 'HAYIR'}")
        print(f"  P8 uctan uca  : veri defteri {'TAMAM' if k['veri_defteri'] else 'KIRIK'}"
              f" · kontrol defteri {'TAMAM' if k['kontrol_defteri'] else 'KIRIK'}"
              f" · gecerli {k['gecerli']} · tepe bekleyen uyandirma "
              f"{k['tepe_bekleyen']}/{KM.BEKLEYEN_UYANDIRMA_TAVANI}")
        print(f"                  defter {json.dumps(d, sort_keys=True)}")
    print()
    print("--- ortak ---")
    print(f"  P2 MAC        : veri ikizine gore veri sayaclari farkli "
          f"{'EVET' if ikiz_farkli else 'HAYIR'} · kontrol {kanitlar[0]['metrik']}"
          f" · ikiz { {x: ikiz[x] for x in kanitlar[0]['metrik']} }")
    print(f"  P5 tavan      : iki kosuda ayni FAIL {'EVET' if t1 and t1 == t2 else 'HAYIR'}"
          f" — {t1}")
    print(f"  P6 yuzey      : pencere {len(IZINLI_GOZLEM_ALANLARI)}/"
          f"{len(IZINLI_KOMSU_ALANLARI)}/{len(IZINLI_PAKET_ALANLARI)} · tip "
          f"{isinstance(T.SinavProtokolu(0, T.yeni_kayit()), KontrolluProtokol)}"
          f" · kismi kanca reddi {kismi_red}")
    print(f"  P7 belirlenim : ayni tohum ayni satir {'EVET' if a == b else 'HAYIR'}")

    # 🔒 VERDİKT ÇIKIŞ KODUNDA — 16 Eylül 2026.
    # Bu betik 16–20 dakika koşuyor, `EVET/HAYIR` basıyor ve her hâlükârda 0
    # ile çıkıyordu. Bağlayıcı karşılığı test takımındadır ve orası geçiyor;
    # ama bu betik kapıları 40 DÜĞÜMLÜK çalışma noktasında koşturur ve
    # testlerin görmediği bir ayrışma burada görünür. Görüneni okunur kılmak
    # bir satırlık iştir.
    #
    # ⚠️ P6'nın alan SAYILARI burada bir eşiğe bağlanmadı ve bu bilinçli:
    # yüzeyin genişliği `v2/05` ile `gozlem/pencere.py`nin izin listelerinde
    # TEK KAYNAK olarak duruyor ve yüzey taraması testi onu bağlıyor. Sayıyı
    # buraya da yazmak ikinci bir kopya olurdu (`v2/03` §B5) ve iki kopya bir
    # gün ayrışır. Burada yalnız KANIT basılır.
    kapilar: dict[str, bool] = {}
    for k in kanitlar:
        ad = k["ad"]
        kapilar[f"P1 bedel · {ad}"] = bool(k["p1"])
        kapilar[f"P2 MAC · {ad}"] = k["konay"] == k["konay_beklenen"]
        kapilar[f"P3 teslim · {ad}"] = bool(k["p3"])
        kapilar[f"P4 zincir · {ad}"] = bool(k["zincir_ok"])
        kapilar[f"P4 ayrim · {ad}"] = bool(k["ayrim_ok"])
        kapilar[f"P8 veri defteri · {ad}"] = bool(k["veri_defteri"])
        kapilar[f"P8 kontrol defteri · {ad}"] = bool(k["kontrol_defteri"])
        kapilar[f"P8 gecerli · {ad}"] = bool(k["gecerli"])
    kapilar["P2 veri ikizi farkli"] = bool(ikiz_farkli)
    kapilar["P5 tavan ayni FAIL"] = bool(t1) and t1 == t2
    kapilar["P6 kismi kanca reddi"] = bool(kismi_red)
    kapilar["P6 tip uyumu"] = isinstance(
        T.SinavProtokolu(0, T.yeni_kayit()), KontrolluProtokol)
    kapilar["P7 belirlenimcilik"] = a == b

    print()
    print("--- KAPI OZETI ---")
    for ad, gecti in kapilar.items():
        if not gecti:
            print(f"  🔴 KALDI : {ad}")
    print(f"  {sum(kapilar.values())}/{len(kapilar)} GECTI")
    if not all(kapilar.values()):
        raise SystemExit("🔴 KONTROL DUZLEMI KAPISI KALDI — yukarisi okunmali")


if __name__ == "__main__":
    main()
