"""
`06` BÖLÜM 9 — DÖRT GEÇERLİLİK ÖN KOŞULUNU **KOL BAŞINA** ÖLÇER.

🔴 NEDEN BU DOSYA VAR
=====================
`06` Bölüm 9: *"**Dördü birden** sağlanmayan hiçbir SONUÇ raporlanmaz."*
Bu tablo 1 Eylül 2026'ya kadar **hiç denetlenmemişti**; denetlendiğinde
ikisi düştü. Üçü de bu araçla, **tek bir iş matrisinden** ölçülür:

    koşul 1  sonuç koşu uzunluğundan bağımsız      (kısa 200 s ↔ tam 350 s)
    koşul 2  metriğin ne ölçtüğü doğrulanmış       (S0 ↔ S2, ham ↔ ortak)
    koşul 3  kollar arasında gizli asimetri yok    (kontrol payı, pencere)

*(Koşul 4 — regresyon testi — bir koşu değil bir depo özelliğidir; `12`
B0.5'in denetimi onu kapsar.)*

🔒 KOL BAŞINA — `06` Bölüm 9'un kendi şartı
============================================
*"Her protokol farklı hızda yakınsar; bir kol için sağlanması diğeri için
sağlandığı anlamına gelmez."* Bu yüzden `KOLLAR` bir parametredir:
**Faz 1'de AODV/OLSR/AOMDV eklenir ve aynı araç yeniden koşar.**

🔒 ÖLÇÜT KOŞMADAN ÖNCE İLAN EDİLDİ — `dogrulama/isaret_testi.py`
================================================================
Çift yönlü kesin işaret testi (α = 0,05) + dağılımdan bağımsız medyan
GA'sı. Ölçüt bugünkü yargıları BİREBİR üretiyor (15/30 geçer, 8/30
geçmez), yani geriye dönük bir gevşetme DEĞİLDİR (`03` kural 3).

🔴 D-13 ŞEKLİ
=============
İşçiler yazıcısız ölçer ve TAM sonucu döndürür; ebeveyn yazar. Yazıcı bir
dosya tanıtıcısı taşır, alt sürece geçirilemez.

Kullanım:
    python dogrulama/gecerlilik.py --tahmin
    python dogrulama/gecerlilik.py
"""

from __future__ import annotations

import random
import statistics as ist
import sys
import time
from multiprocessing import Pool, cpu_count
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dogrulama.aktaricilar import AKTARICILAR                     # noqa: E402
# 🔴 DV `AKTARICILAR`da YOK; `08` md 25'in kolunu buradan alıyoruz (B-135).
from dogrulama.kontrol_payi import mesafe_vektoru                 # noqa: E402
from dogrulama.gecikme import yuzdelik                             # noqa: E402
from dogrulama.isaret_testi import (ayak1_etiketi,   # noqa: E402
                                    ga_estimandi, isaret_testi)
from dogrulama.olcum import kayit, olc, yaz_sonuc                  # noqa: E402
from sim.config import Konfig                                      # noqa: E402
from sim.karsilastirma import (KarsilastirmaHatasi,                # noqa: E402
                               kontrol_payi_yuzde, ortak_alt_kume)

CEKIRDEK = min(10, cpu_count())          # K-002
TOHUMLAR = range(1, 31)                  # ayarlama tohumlari (K-025)

# 🔴 B-135 (yedinci denetim) — KOL KAYDI ARTIK BIR SOZLUK.
#
# Onceki hali yalnizca `AKTARICILAR`dan secebiliyordu ve `mesafe_vektoru`
# (DV) orada YOK — o `dogrulama/kontrol_payi.py`de tanimli. Sonucu:
# kosul 3'u olcen arac, `08` md 25'in BAGLAYICI oranini ureten kolu
# OLCEMIYORDU ve iki arac iki farkli sayi basiyordu:
#     kontrol_payi.py -> DV <-> gozlem      : 4,0 - 38,0 kat
#     gecerlilik.py   -> kahin <-> gozlem   : 1,53 - 3,62 kat
# Hangisinin baglayici oldugu hicbir belgede yaziliydi.
#
# 🔒 KARAR (danismana devredildi, K-088): **DV <-> gozlem BAGLAYICIDIR.**
# Kosul 3 *"karsilastiracagimiz kollar arasinda gizli asimetri var mi"*
# diye soruyor; Faz 1'in AODV'si KONTROL DUZLEMI AGIR bir protokol —
# DV gibi. `en_kisa_yol` bir KAHIN ve protokol degil, dolayisiyla onun
# uzerinden olculen asimetri Faz 1'i temsil etmiyor.
#
# 🔒 Faz 1'de bu sozluge AODV, OLSR, AOMDV eklenir. Arac degismez.
KOLLAR: dict[str, object] = {
    "en_kisa_yol": AKTARICILAR["en_kisa_yol"],          # kâhin — taban
    "gurultuden_kacan": AKTARICILAR["gurultuden_kacan"],  # saf gözlem
    "DV": mesafe_vektoru,        # 🔒 kontrol düzlemi ağır — BAĞLAYICI çift
}

# 🔒 Koşul 3'ün BAĞLAYICI kol çifti (`08` md 25 ile aynı).
BAGLAYICI_CIFT = ("DV", "gurultuden_kacan")

# Isinma AYNI birakilir (50 s): degisen sey OLCUM PENCERESININ UZUNLUGU,
# isinmanin yeterliligi degil. `10` §7b.3 ile birebir ayni kurgu.
UZUNLUKLAR = {
    "tam":  (50.0, 320.0, 350.0),        # deponun bugunku hali
    "kisa": (50.0, 170.0, 200.0),        # literatur medyani (~200 s)
}
SENARYOLAR = ("S0", "S2")                # kontrol kolu + birincil nokta


def _isler() -> list[tuple]:
    isler = []
    for tohum in TOHUMLAR:
        for kol in KOLLAR:
            for senaryo in SENARYOLAR:
                for uzunluk, (i_s, o_s, k_s) in UZUNLUKLAR.items():
                    isler.append((
                        {"kol_adi": kol, "senaryo_etiket": senaryo,
                         "uzunluk": uzunluk},
                        dict(senaryo=senaryo, trafik="orta", tohum=tohum,
                             isinma_s=i_s, olcum_bitis_s=o_s,
                             kosu_bitis_s=k_s),
                        kol))
    # IC ICE: sira karistirilir ki bir eksen makinenin yavas donemine
    # sistematik olarak denk gelmesin (K-075: ardisik olcum "+819 sn"
    # demisti, ic ice olcumde gercek fark +45 sn cikti).
    random.Random(20260901).shuffle(isler)
    return isler


def _kosu(arg) -> tuple[dict, dict]:
    """ISCI — yazicisiz olcer, TAM sonucu DONDURUR (D-13)."""
    etiketler, kwargs, kol = arg
    kon = Konfig(kol="gecerlilik", **kwargs)
    return etiketler, olc(kon, KOLLAR[kol], aktarici=kol)


# --------------------------------------------------------------------------
# ANALIZ
# --------------------------------------------------------------------------

def _gecikme_olcutleri(m: dict) -> dict:
    """Bir kosudan gecikme okumalari — HEPSI ayni listeden turer."""
    g = m.get("teslim_gecikmeleri_s") or []
    if not g:
        return {"ortalama": None, "p50": None, "p95": None, "p99": None}
    return {"ortalama": ist.mean(g), "p50": yuzdelik(g, 0.50),
            "p95": yuzdelik(g, 0.95), "p99": yuzdelik(g, 0.99)}


def kosul1(veri: dict) -> list[dict]:
    """KOSUL 1 — sonuc kosu uzunlugundan bagimsiz mi? (kisa vs tam)"""
    cikti = []
    for kol in KOLLAR:
        for senaryo in SENARYOLAR:
            for ad, cikar in (
                ("teslim_orani", lambda m: m["teslim_orani"]),
                ("gecikme ort", lambda m: _gecikme_olcutleri(m)["ortalama"]),
                ("gecikme p95", lambda m: _gecikme_olcutleri(m)["p95"]),
            ):
                farklar, tam_degerler = [], []
                for t in TOHUMLAR:
                    a = veri.get((kol, senaryo, "kisa", t))
                    b = veri.get((kol, senaryo, "tam", t))
                    if not a or not b:
                        continue
                    va, vb = cikar(a), cikar(b)
                    if va is None or vb is None:
                        continue
                    farklar.append(va - vb)          # kisa - tam
                    tam_degerler.append(vb)
                if not farklar:
                    continue
                std = ist.stdev(tam_degerler) if len(tam_degerler) > 1 else None
                r = isaret_testi(farklar, tohum_std=std)
                r.update(kol=kol, senaryo=senaryo, metrik=ad, tohum_std=std)
                cikti.append(r)
    return cikti


def kosul2(veri: dict) -> list[dict]:
    """KOSUL 2 — gecikme metrigi ne olcuyor? (S0 -> S2, HAM vs ORTAK)

    DORT okuma birden: ham ortalama, HAM p95, ortak alt kume ortalamasi,
    ortak alt kume p95. `08` md 16'nin uyardigi secilim yanliligi yalnizca
    ORTAK alt kumede ortadan kalkar.

    🔴 HAM p95 B-121 ile eklendi: `06` §8.1b'nin TASIYICI satiri oydu ve
    bu uretici onu basmiyordu (uc okuma bastiriyordu, tablo dort satir
    tasiyordu). Sayi dogruydu ama URETILEMIYORDU — `03` kural 1.
    """
    cikti = []
    for kol in KOLLAR:
        # 🔴 B-121 (yedinci denetim) — HAM p95 EKLENDİ.
        # `06` §8.1b'nin taşıyıcı satırı *(HAM p95: +7,11 ms · 17/30 ·
        # p = 0,5847)* bu üreticiden ÇIKMIYORDU: fonksiyon üç okuma
        # basıyordu, tablo dört satır taşıyordu. Sayı doğruydu ama
        # `03` kural 1 anlamında ÜRETİLEMİYORDU — ve o satır olmadan
        # *"sorun p95 değil, karşılaştırılan KÜME"* iddiası kurulamaz.
        # B-80/B-81'in aynı örüntüsü, mühre giden bir sayfada.
        ham_ort, ham_p95, ortak_ort, ortak_p95, kesisimler = [], [], [], [], []
        reddedilen = 0
        pay_tanimsiz = 0          # 🔴 B-152 · `08` md 35
        for t in TOHUMLAR:
            a = veri.get((kol, "S0", "tam", t))
            b = veri.get((kol, "S2", "tam", t))
            if not a or not b:
                continue
            try:
                o = ortak_alt_kume(a, b)
            except KarsilastirmaHatasi:
                reddedilen += 1
                continue
            if o.ortak_paket == 0:
                reddedilen += 1
                continue
            # 🔴 B-152 (sekizinci denetim) — `08` md 35'IN GUVENCESI
            # URETIM YOLUNA BAGLANDI. Madde *"okuyan, `ozet()`in
            # TANIMSIZ etiketini gormek ZORUNDADIR"* diyordu ama
            # `ortak_alt_kume`in tek uretim cagirani BURASI ve burasi
            # `kontrol_payi_a/b`yi hic okumuyordu; `ozet()`i zorlayan tek
            # sey bir TESTTI. Bugun 88 karsilastirmanin 0'inda tanimsiz,
            # ama Faz 1'in AODV'si D-11'in birebir profili.
            if o.kontrol_payi_a is None or o.kontrol_payi_b is None:
                pay_tanimsiz += 1
            kesisimler.append(o.kesisim_orani_pencere)
            ham_ort.append(o.ham_fark_s)
            # HAM p95: her kolun KENDİ teslim ettiklerinden — ortak alt
            # kümeden DEĞİL. Karşılaştırılan kümelerin farklı olduğu
            # okuma budur ve §8.1b'nin gösterdiği şey tam olarak onun
            # anlamsız çıkması.
            ham_p95.append(yuzdelik(b["teslim_gecikmeleri_s"], 0.95)
                           - yuzdelik(a["teslim_gecikmeleri_s"], 0.95))
            ortak_ort.append(o.gecikme_farki_s)
            ortak_p95.append(o.p95_farki_s)
        if not ortak_ort:
            continue
        for ad, farklar in (("HAM ortalama", ham_ort),
                            ("HAM p95", ham_p95),
                            ("ORTAK ortalama", ortak_ort),
                            ("ORTAK p95", ortak_p95)):
            r = isaret_testi([1e3 * x for x in farklar])
            r.update(kol=kol, metrik=ad, reddedilen=reddedilen,
                     pay_tanimsiz=pay_tanimsiz,
                     kesisim_ort=ist.mean(kesisimler),
                     kesisim_min=min(kesisimler), kesisim_max=max(kesisimler))
            cikti.append(r)
    return cikti


def kosul3(veri: dict) -> list[dict]:
    """KOSUL 3 — kollar arasinda gizli asimetri var mi? (kontrol payi)

    PENCEREDEN okunur (`08` md 31). Tum kosu hali teshis icindir.
    """
    cikti = []
    for kol in KOLLAR:
        for senaryo in SENARYOLAR:
            baytlar, airtimeler, dejenere = [], [], 0
            for t in TOHUMLAR:
                m = veri.get((kol, senaryo, "tam", t))
                if not m:
                    continue
                # 🔴 B-134: TANIMSIZ artik `None` doner, istisna DEGIL.
                p = kontrol_payi_yuzde(m)
                if p is None:
                    dejenere += 1
                    continue
                baytlar.append(p["bayt"])
                airtimeler.append(p["airtime"])
            if baytlar:
                cikti.append({
                    "kol": kol, "senaryo": senaryo, "n": len(baytlar),
                    "dejenere": dejenere,
                    "bayt_ort": ist.mean(baytlar),
                    "bayt_min": min(baytlar), "bayt_max": max(baytlar),
                    "airtime_ort": ist.mean(airtimeler),
                    "airtime_min": min(airtimeler),
                    "airtime_max": max(airtimeler),
                })
    return cikti


def eslesmis_kol_orani(veri: dict) -> dict:
    """Iki kolun AYNI tohum/senaryodaki kontrol payi ORANI (`08` md 25).

    Eslestirilmis olmak zorunda: eski olcum bir kolun en kucugunu
    digerinin en buyugune boluyordu ve ikisi FARKLI senaryolardandi
    (`03` B2 ihlali, B-80'de duzeltildi).
    """
    a_kol, b_kol = BAGLAYICI_CIFT     # 🔒 B-135: DV <-> gozlem
    if a_kol not in KOLLAR or b_kol not in KOLLAR:
        return {}
    oranlar: list[float] = []
    yonlu: list[float] = []
    ters = dejenere = 0
    for senaryo in SENARYOLAR:
        for t in TOHUMLAR:
            ma = veri.get((a_kol, senaryo, "tam", t))
            mb = veri.get((b_kol, senaryo, "tam", t))
            if not ma or not mb:
                continue
            pa, pb = kontrol_payi_yuzde(ma), kontrol_payi_yuzde(mb)
            if pa is None or pb is None:      # 🔴 B-134
                dejenere += 1
                continue
            # 🔴 B-155 (sekizinci denetim) — DEJENERE PAYDA TIPLI REDDEDILIR.
            # `kontrol_payi_yuzde` `vb == 0`i `None`a ceviriyor ama
            # `kb == 0` (kol pencerede HIC kontrol bayti uretmemis)
            # gecerli bir donus olan `bayt = 0.0` veriyordu ve buradaki
            # bolme ZeroDivisionError firlatiyordu — olculdu ve
            # tetiklendi. Komsusu `kontrol_payi.eslestirilmis_oranlar`
            # ayni vakayi `b == 0` ile ACIKCA eliyor; D-11'in dersi iki
            # aractan birine uygulanmis, komsusuna uygulanmamisti.
            if pa["bayt"] == 0 or pb["bayt"] == 0:
                dejenere += 1
                continue
            # 🔴 B-153 — TEK YUKLEM, IKI OKUMA. `08` md 25'in orani iki
            # aracta iki FARKLI yuklemle hesaplaniyordu:
            #     kontrol_payi.py -> a / b   (YONLU, < 1 olabilir)
            #     gecerlilik.py   -> max/min (YONSUZ, >= 1)
            # Bugun 58/58 hucrede ayni cikiyorlar CUNKU DV her hucrede
            # gozlemden buyuk — tesadufen. Mutasyonum `X9` ikisini
            # ayristirdi ve 473 testin hicbiri kirilmadi.
            # 🔒 Ikisi de tutulur ve YON DEGISIMI ayrica sayilir; Faz 1'de
            # sessiz senaryodaki reaktif AODV gozlem kolundan AZ kontrol
            # bayti uretebilir ve o an iki okuma AYRISIR.
            y = pa["bayt"] / pb["bayt"]
            yonlu.append(y)
            oranlar.append(max(pa["bayt"], pb["bayt"])
                           / min(pa["bayt"], pb["bayt"]))
            if y < 1.0:
                ters += 1
    if not oranlar:
        return {}
    return {"n": len(oranlar), "min": min(oranlar), "max": max(oranlar),
            "ortanca": ist.median(oranlar), "kollar": (a_kol, b_kol),
            # 🔒 B-153: YONLU okuma ve yon degisimi ayrica raporlanir.
            "yonlu_min": min(yonlu), "yonlu_max": max(yonlu),
            "yonlu_ortanca": ist.median(yonlu),
            "ters_yon": ters, "dejenere": dejenere}


# --------------------------------------------------------------------------
# RAPOR
# --------------------------------------------------------------------------

def _yaz_kosul1(sonuclar: list[dict]) -> set[tuple[str, str]]:
    print()
    print("=" * 126)
    print("KOSUL 1 — SONUC KOSU UZUNLUGUNDAN BAGIMSIZ MI  (kisa 200 s vs tam 350 s)")
    print("OLCUT (kosmadan once ilan edildi): IKI AYAKLI — `06` 9.2(a)")
    print("  ayak 1 YON      : cift yonlu kesin isaret testi, alfa = 0,05  <- asagidaki sutun")
    print("  ayak 2 BUYUKLUK : |GA uclari| <= k x tohum std                <- k BOS (B4)")
    print("BU TABLO BIR TABAN CIZGISIDIR. Kosul 1 bugun HICBIR KOL icin")
    print("'saglandi' SAYILAMAZ — olcut EKSIKTIR (`06` 9.2(a) · B-125/K3).")
    print("=" * 126)
    print(f"{'kol':<18}{'sen':<4}{'metrik':<13}{'n+':>7}{'p':>9}  "
          f"{'ayak1(yon)':<11}{'med HAM':>11}{'med GA':>11}"
          f"{'GA (medyan)':>24}{'GA / std':>18}{'eps_rel':>10}")
    dusen = set()
    for r in sonuclar:
        ga = r["ga"]
        ga_m = "yok" if ga is None else f"[{ga[0]:+.5f}, {ga[1]:+.5f}]"
        kat = ("" if r["ga_std_kati"] is None
               else f"[{r['ga_std_kati'][0]:+.2f}, {r['ga_std_kati'][1]:+.2f}]")
        # B-146 (sekizinci denetim) — GA'NIN ESTIMANDI HAM MEDYAN DEGIL.
        # Beraberlik varsa GA, NET farklardan kurulur; HAM medyan kendi
        # GA'sinin DISINDA kalabilir. Olculdu: 18 satirin 7'si ayrisiyor,
        # 2'sinde ISARET TERS (DV/S2/teslim_orani: HAM +0.00000, estimand
        # -0.00005). Ayrisinca IKISI DE basilir.
        # Sozlesme `isaret_testi.ga_estimandi`dedir — TEK KAYNAK, cunku
        # B-124'un duzeltmesi `satir()`e yazilmis ve `satir()`in deposunda
        # SIFIR cagirani vardi (B-146).
        est = ga_estimandi(r)
        ayni = (r["medyan_fark"] is not None and est is not None
                and abs(r["medyan_fark"] - est) <= 1e-12)
        est_m = "= HAM" if ayni else f"{est:+.5f}"
        # 🔴 B-158: `06` Bolum 7'nin durdurma kurali (eps_rel <= %10)
        # kosul 1'e HIC UYGULANMAMISTI ve uygulanmadigi da
        # yazilmamisti. Artik her satirda uretilip basiliyor.
        eps = r["eps_rel"]
        eps_m = "TANIMSIZ" if eps is None else f"%{eps:.0f}"
        print(f"{r['kol']:<18}{r['senaryo']:<4}{r['metrik']:<13}"
              f"{str(r['pozitif']) + '/' + str(r['n']):>7}{r['p']:>9.4f}  "
              f"{ayak1_etiketi(r):<11}"
              f"{r['medyan_fark']:>11.5f}{est_m:>11}{ga_m:>24}{kat:>18}"
              f"{eps_m:>10}")
        if not r["gecti"]:
            dusen.add((r["kol"], r["metrik"]))
    return dusen


def _yaz_kosul2(sonuclar: list[dict]) -> None:
    print()
    print("=" * 110)
    print("KOSUL 2 — GECIKME METRIGI NE OLCUYOR  (S0 -> S2, ayni tohum)")
    print("`08` md 16: gecikme yalnizca TESLIM EDILENDEN olculur; kumeler farkliysa")
    print("karsilastirma HAYATTA-KALAN YANLILIGI tasir. Ortak alt kume onu kaldirir.")
    print("=" * 126)
    print(f"{'kol':<18}{'okuma':<15}{'n+':>7}{'n_red':>6}{'p':>9}  {'yon':<8}"
          f"{'med HAM (ms)':>14}{'med GA (ms)':>13}{'GA (ms)':>24}{'kesisim':>21}")
    for r in sonuclar:
        ga = r["ga"]
        ga_m = "yok" if ga is None else f"[{ga[0]:+.2f}, {ga[1]:+.2f}]"
        kes = (f"%{100*r['kesisim_ort']:.1f} "
               f"[%{100*r['kesisim_min']:.1f}-%{100*r['kesisim_max']:.1f}]")
        # B-146 — kosul 1'le AYNI SOZLESME (tek kaynak).
        est = ga_estimandi(r)
        ayni = (r["medyan_fark"] is not None and est is not None
                and abs(r["medyan_fark"] - est) <= 1e-12)
        est_m = "= HAM" if ayni else f"{est:+.2f}"
        # B-166 — `reddedilen` HESAPLANIYORDU ama BASILMIYORDU; komsusu
        # `_yaz_kosul3` `dejenere` sutununu basiyor. `03` B2: "ust sinir
        # verirken KAC GOZLEMLE hesaplandigini da yaz." Olculdu: DV'nin
        # n'i 30 degil 26 (2 bos kesisim + 2 beraberlik) ve sebep hicbir
        # belgede yaziliydi.
        yon = "ARTTI" if r["medyan_fark"] > 0 else "DUSTU"
        anlamli = "" if r["gecti"] else "*"
        print(f"{r['kol']:<18}{r['metrik']:<15}"
              f"{str(r['pozitif']) + '/' + str(r['n']):>7}{r['reddedilen']:>6}"
              f"{r['p']:>9.4f}  "
              f"{yon + anlamli:<8}{r['medyan_fark']:>14.2f}{est_m:>13}"
              f"{ga_m:>24}{kes:>21}")
    print("  (* = isaret testi REDDETTI, yani yon sistematik)")
    print("  (n_red = ortak alt kumesi BOS ya da sema disi oldugu icin DUSEN")
    print("   tohum sayisi. n = 30 - n_red - beraberlik.)")
    # 🔴 B-152 — `08` md 35'in guvencesi URETIM YOLUNDA.
    tanimsiz = sum(r.get("pay_tanimsiz", 0) for r in sonuclar) // 4
    if tanimsiz:
        print(f"  🔴 KONTROL PAYI TANIMSIZ: {tanimsiz} hucre (D-11 · `08` md 35).")
        print("     O hucrelerin gecikme farki URETILDI ama kontrol payi")
        print("     BILINMIYOR — kosul 3 o hucreler icin olculemez.")
    else:
        print("  (kontrol payi TANIMSIZ hucre: 0 — `08` md 35)")
    # B-148 — `kosul2`de AYAK 2 YAPISAL OLARAK BOS: `isaret_testi`ye
    # `tohum_std` gecirilmiyor, yani dislanan etki buyuklugu (sigma kati)
    # uretilemiyor. `kosul1`de 18/18 dolu, burada 0/12. Beyan artik
    # CIKTIDA da duruyor, sadece `06`da degil.
    if all(r.get("ga_std_kati") is None for r in sonuclar):
        print("  AYAK 2 YOK: bu tabloda dislanan etki buyuklugu (sigma kati)")
        print("  HESAPLANMIYOR — `kosul2` tohumlar arasi std uretmiyor (B-148).")


def _yaz_kosul1_ozeti(dusen: set[tuple[str, str]]) -> None:
    """KOSUL 1 OZETI — `main()`ten CIKARILDI ki test edilebilsin.

    🔴 B-145 (sekizinci denetim). Blok `main()`in icindeydi; capa testi
    `main()`i cagirmiyor (dosyanin kendi kapsam tablosu bunu yaziyor),
    yani hicbir dusen cift olmadiginda basilan *"hepsi gecti"* cumlesi
    KORUMASIZDI — ve o cumle `06` 9.2(a)'nin
    (*"kosul 1 bugun HICBIR KOL icin saglandi sayilamaz"*) tam tersiydi.

    `03` B5: *"karar ureten yuklemlerini AYRI ve test edilebilir yaz."*
    """
    print("=" * 126)
    print("KOSUL 1 OZETI — hangi kol/metrik cifti AYAK 1'i (yon) GECMEDI")
    if dusen:
        for kol, metrik in sorted(dusen):
            print(f"    YON-RED: {kol} / {metrik}")
    else:
        print("    ayak 1'i dusuren cift yok")
    # 🔒 BU IKI SATIR KOSULSUZDUR ve oyle kalmalidir: ayak 2'nin esigi
    # `k` B4'e kadar BOS oldugu icin hicbir kol "saglandi" sayilamaz.
    print("    AYAK 2 ESIGI (`k`) BOS — bu yuzden hicbir kol")
    print("    'kosul 1 SAGLANDI' sayilamaz (`06` 9.2(a) · B-125/K3).")
    print("=" * 126)


def _yaz_kosul3(sonuclar: list[dict], oran: dict) -> None:
    print()
    print("=" * 110)
    print("KOSUL 3 — KOLLAR ARASINDA GIZLI ASIMETRI  (kontrol payi, OLCUM PENCERESINDEN)")
    print("`08` md 31: Aile 1'in her karsilastirmasi `*_pencere` alanlarini kullanmak zorunda.")
    print("=" * 110)
    print(f"{'kol':<18}{'sen':<5}{'n':>4}{'dej':>5}"
          f"{'bayt %':>10}{'bayt araligi':>22}"
          f"{'airtime %':>12}{'airtime araligi':>22}")
    for r in sonuclar:
        bayt_aralik = "[{:.3f} - {:.3f}]".format(r["bayt_min"], r["bayt_max"])
        air_aralik = "[{:.3f} - {:.3f}]".format(r["airtime_min"],
                                                r["airtime_max"])
        print(f"{r['kol']:<18}{r['senaryo']:<5}{r['n']:>4}{r['dejenere']:>5}"
              f"{r['bayt_ort']:>10.3f}{bayt_aralik:>22}"
              f"{r['airtime_ort']:>12.3f}{air_aralik:>22}")
    if oran:
        print()
        print(f"  ESLESTIRILMIS KOL ORANI ({oran['kollar'][0]} vs {oran['kollar'][1]}, "
              f"bayt, n={oran['n']}):")
        print(f"    YONSUZ (max/min): ortanca {oran['ortanca']:.2f} kat"
              f"  |  aralik {oran['min']:.2f} - {oran['max']:.2f} kat")
        # 🔴 B-153 — AYNI ADIN IKI YUKLEMI ARTIK YAN YANA BASILIYOR.
        print(f"    YONLU  (a/b)    : ortanca {oran['yonlu_ortanca']:.2f} kat"
              f"  |  aralik {oran['yonlu_min']:.2f} - "
              f"{oran['yonlu_max']:.2f} kat")
        print(f"    ters yon (a < b): {oran['ters_yon']}/{oran['n']} hucre"
              f"  |  dejenere: {oran['dejenere']}")
        if oran["ters_yon"]:
            print("    🔴 YON DEGISTI — iki okuma AYRISIYOR; `08` md 25'in")
            print("       hangi yuklemle okunacagi artik farkediyor (B-153).")


def _kalibrasyon_ornekleri(isler: list[tuple]) -> list[tuple]:
    """Kalibrasyon icin UC EKSENI DE ornekleyen is listesi (B-154).

    🔴 F-11 tek-is kalibrasyonunu kaldirdi ama yalnizca KOL eksenini
    ornekledi; aracin KENDI maliyet eksenleri UZUNLUK (200 s <-> 350 s)
    ve SENARYO. Sekizinci denetim olctu: uc ornegin **3'u de S0**,
    **2'si kisa** -> ortalama `kosu_bitis_s` **250 s**, is listesinde
    **275 s** (**-%9,1**). Tahmin sistematik olarak IYIMSER cikiyordu ve
    `03` kural 7'nin *"30 dk'yi asarsa SOR"* kapisi tam olarak bu
    tahmine bagli — iyimser bir tahmin, SORULMASI GEREKEN bir kosuyu
    sorulmadan baslatir. F-9'un teshisinin birebir aynisi, F-11'in
    duzeltmesinin ICINDE.

    🔒 Her (kol, senaryo, uzunluk) uclusunden bir ornek: eksen dagilimi
    is listesiyle BIREBIR ayni olur.

    🔒 AYRI FONKSIYON cunku `03` B5: *"karar ureten yuklemlerini AYRI ve
    test edilebilir yaz."* `main()` icinde kalsaydi capa testi onu
    goremezdi (dosyanin kendi kapsam tablosu: *"main() cagrilmiyor"*).
    """
    return [next(i for i in isler
                 if i[0]["kol_adi"] == kol
                 and i[0]["senaryo_etiket"] == senaryo
                 and i[0]["uzunluk"] == uzunluk)
            for kol in KOLLAR
            for senaryo in SENARYOLAR
            for uzunluk in UZUNLUKLAR]


def main(argv: list[str]) -> int:
    isler = _isler()
    print("`06` BOLUM 9 — GECERLILIK ON KOSULLARI, KOL BASINA")
    print(f"is sayisi: {len(isler)} tam kosu | cekirdek: {CEKIRDEK} | "
          f"kollar: {', '.join(KOLLAR)} | tohum: {TOHUMLAR.start}-{TOHUMLAR.stop - 1}")

    # `03` kural 7 — SURE TAHMINI ONCE YAZDIRILIR, tek sayi degil BANT.
    # 🔴 F-9 — KALİBRASYON TEK İŞTE YAPILMAZ.
    # `pencere_kapsami.py`de ölçüldü: tek işten kurulan tahmin 900
    # koşu için "1,8-3,8 dk" dedi, koşu 10 dk'da BİTMEDİ. Maliyet
    # KOL ve TRAFİĞE bağlı; tek örnek onu temsil etmiyor. Bu, deponun
    # "süre tahmini beş kez tutmadı" örüntüsünün altıncısıydı ve
    # `03` kural 7'yi doğrudan zayıflatıyor: iyimser bir tahmin,
    # SORULMASI GEREKEN bir koşuyu sorulmadan başlatır.
    # 🔴 B-154 (sekizinci denetim) — KALIBRASYON UC EKSENI DE ORNEKLER.
    # F-11 tek-is kalibrasyonunu kaldirdi ama yalnizca KOL eksenini
    # ornekledi; aracin KENDI maliyet eksenleri UZUNLUK (200 s <-> 350 s)
    # ve SENARYO. Olculdu: uc ornegin 3'u de S0, 2'si kisa ->
    # ortalama `kosu_bitis_s` 250 s, is listesinde 275 s (-%9,1).
    # Tahmin sistematik olarak IYIMSER cikiyordu ve `03` kural 7'nin
    # "30 dk'yi asarsa SOR" kapisi tam olarak bu tahmine bagli.
    # 🔒 Artik her (kol, senaryo, uzunluk) uclusunden bir ornek: 3x2x2=12,
    # yani is listesinin eksen dagilimiyla BIREBIR ayni.
    ornekler = _kalibrasyon_ornekleri(isler)
    t0 = time.perf_counter()
    for o in ornekler:
        _kosu(o)
    tek = (time.perf_counter() - t0) / len(ornekler)
    alt = len(isler) * tek / CEKIRDEK / 60.0
    print(f"kalibrasyon: {len(ornekler)} hucre ortalamasi {tek:.2f} sn/kosu"
          f"  (kol x senaryo x uzunluk — B-154)")
    print(f"TAHMIN BANDI: {alt:.1f} - {alt * 2.10:.1f} dk "
          f"(2,10x makine oynakligi, K-075)")
    if "--tahmin" in argv:
        print("(--tahmin: yalnizca tahmin istendi, kosulmadi)")
        return 0
    if alt * 2.10 > 30.0:
        print()
        print("UST BANT 30 DK'YI ASIYOR — `03` kural 7 geregi DURULDU.")
        print("   Ogrenciye sorulmadan kosulmaz. Devam icin: --zorla")
        if "--zorla" not in argv:
            return 2

    bas = time.perf_counter()
    veri: dict = {}
    # Yazici EBEVEYNDE acilir; isciler yazmaz, DONDURUR (D-13).
    with kayit("gecerlilik") as yazici:
        with Pool(CEKIRDEK) as p:
            for etiketler, sonuc in p.imap_unordered(_kosu, isler, chunksize=1):
                yaz_sonuc(sonuc, yazici=yazici, **etiketler)
                veri[(etiketler["kol_adi"], etiketler["senaryo_etiket"],
                      etiketler["uzunluk"], sonuc["konfig"]["tohum"])] = sonuc
        yazilan = yazici.yazilan
    sure = (time.perf_counter() - bas) / 60.0

    print(f"kosuldu: {sure:.1f} dk | yazilan satir: {yazilan}")
    # Sozlesme 5'in DAVRANISSAL dogrulamasi (D-13).
    assert yazilan == len(isler), (
        f"yazilan satir ({yazilan}) is sayisina ({len(isler)}) esit degil "
        f"— D-13 sinifi bir kacak var")

    bozuk = [k for k, s in veri.items() if not s["korunum"]["korunum_tamam"]]
    print(f"korunum: {len(veri) - len(bozuk)}/{len(veri)} tamam")
    if bozuk:
        print(f"  BOZUK: {bozuk[:5]}")

    dusen = _yaz_kosul1(kosul1(veri))
    _yaz_kosul2(kosul2(veri))
    _yaz_kosul3(kosul3(veri), eslesmis_kol_orani(veri))

    print()
    _yaz_kosul1_ozeti(dusen)
    return 0


if __name__ == "__main__":        # Windows `spawn` — devir teslim §6.2
    raise SystemExit(main(sys.argv[1:]))
