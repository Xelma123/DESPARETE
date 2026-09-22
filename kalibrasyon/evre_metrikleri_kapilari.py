"""
EVRE METRİKLERİNİN DOĞRULAMA KAPILARI — adım ⑤, `08-EVRE-METRIKLERI.md` §05.

Üretici:
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/evre_metrikleri_kapilari.py

🔴 NEDEN VAR
============
Bu projede bir ölçüm aleti, ölçtüğü şey kadar sınanır. Evre metrikleri
protokolleri ayırt etmek için kullanılacak; kullanılmadan ÖNCE kendilerinin
doğru şeyi ölçtüğü gösterilmelidir.

    G1 · BOŞ KOL      karıştırıcısız kolda metrikler SUSUYOR mu
    G2 · TEKDÜZELİK   şok derinliği ŞİDDETLE artıyor mu
    G3 · IZGARA FAZI  sonuç örnekleme fazına bağlı mı
    G4 · BULANIKLIK   doğum-anına-göre kovalama geçerli mi

⚠️ G1'in üç maddesi burada koşuyor, DÖRDÜNCÜSÜ KOŞAMIYOR ve bu beyan edilir:
tespit gecikmesi bir protokolün KOPMA BEYANINI gerektiriyor ve depodaki iki
koşum aletinin ikisi de hiç beyan etmiyor (`beyan_etmiyor = True`). Yani
M4'ün boş kol kapısı Faz 2'ye ERTELENMİŞTİR; bugünkü kapsamı
`tests2/test_evre.py`in sentetik testleridir.

🔒 KÂHİN KULLANILIYOR, koşum aleti değil. Sebep: kâhin karıştırıcısız statik
kolda PDR 1,000 veriyor, yani "şok derinliği sıfır olmalı" iddiası ORADA
keskin. Aptal bir koşum aletiyle PDR zaten 0,1–0,4 olurdu ve sıfırdan sapma
metriğin mi yoksa protokolün mü olduğu ayırt edilemezdi.
"""

from __future__ import annotations

import statistics as ist
import sys
import time
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.olcum.evre import IZGARA_ADIMI_S, Evreler, evre_sozlugu  # noqa: E402
from sim2.olcum.metrikler import yuzdelik  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402
from kalibrasyon.kahin import EnGuvenilirKahin, KanalGrafigi  # noqa: E402

TOHUMLAR = (1000, 1001, 1002)


def _kos(senaryo: str, tohum: int, **ek):
    kfg = Konfig(kol="evre_kapi", senaryo=senaryo, tohum=tohum, **ek)
    kur = kurulum_yap(kfg)
    grafik = KanalGrafigi(kur)
    t0 = time.perf_counter()
    Kosu(kur, lambda i: EnGuvenilirKahin(i, grafik)).kostur()
    return kur, kfg, time.perf_counter() - t0


def _evre(kur, kfg, izgara_kaymasi_s: float = 0.0):
    bas, bitis = kfg.olcum_penceresi
    p99 = yuzdelik(kur.paket_defteri.gecikmeler(True), 99)
    return evre_sozlugu(kur.paket_defteri, kur.rota_defteri,
                        bas_s=bas,
                        acilma_s=kfg.karistirici_baslangic_s
                        + izgara_kaymasi_s,
                        bitis_s=bitis, gecikme_p99_s=p99)


def _baslik(metin: str) -> None:
    print("\n" + "=" * 78)
    print(metin)
    print("=" * 78)


# ==========================================================================
def g1_bos_kol() -> bool:
    """Karıştırıcısız kolda metrikler susuyor mu?

    🔴 Bir metrik, karıştırıcı YOKKEN bir şok gösteriyorsa karıştırmayı
    değil BAŞKA bir şeyi ölçüyordur. Bu kapı, geri kalan her sayının
    okunabilir olup olmadığını belirler.
    """
    _baslik("G1 - BOS KOL  (statik-yok, en guvenilir kahin)")
    print("  OLCUT (KOL DUZEYINDE): ortalama sok_derinligi 0'dan 2 SE icinde")
    print("         her tohumda toparlanma_suresi = 0 · tespit SANSURLU")
    print()
    print("  🔴 VERDIKT TOHUM BASINA DEGIL, KOL ORTALAMASINDA VERILIR.")
    print("     Tohum basina 2 SE testi TANIM GEREGI tohumlarin ~%5'inde")
    print("     kalir; uc tohumda en az birinin kalma olasiligi ~%14. Yani")
    print("     tohum basina bir kapi, DOGRU bir metrigi rastgele reddeder.")
    print("     Sok derinligi zaten kol duzeyinde okunuyor (08 §06/2).")
    print()
    print(f"  {'tohum':>6} {'pdr_temiz':>10} {'sok_der':>9} {'2SE':>8} "
          f"{'tamlik':>8} {'top_sure':>9} {'tespit':>8}")
    derinlikler, seler = [], []
    zaman_ok = True
    for tohum in TOHUMLAR:
        kur, kfg, _ = _kos("statik-yok", tohum)
        s = _evre(kur, kfg)
        d, se = s["sok_derinligi"], s["sok_derinligi_se"]
        derinlikler.append(d)
        seler.append(se or 0.0)
        zaman_ok &= (s["toparlanma_suresi_s"] == 0.0
                     and s["tespit_gecikmesi_s"] is None)
        print(f"  {tohum:>6} {s['pdr_temiz']:>10.4f} {d:>+9.5f} "
              f"{2.0 * (se or 0.0):>8.5f} {s['toparlanma_tamligi']:>8.4f} "
              f"{s['toparlanma_suresi_s']!s:>9} "
              f"{s['tespit_gecikmesi_s']!s:>8}")
    ort = ist.mean(derinlikler)
    ort_se = ist.mean(seler) / len(derinlikler) ** 0.5
    icinde = abs(ort) <= 2.0 * ort_se
    hepsi = icinde and zaman_ok
    print(f"\n  KOL ORTALAMASI  sok_derinligi {ort:+.6f}  "
          f"2 SE {2.0 * ort_se:.6f}  "
          f"{'ICINDE' if icinde else '🔴 DISINDA'}")
    print(f"  zaman metrikleri (her tohumda) : "
          f"{'TAMAM' if zaman_ok else '🔴 KIRIK'}")
    print(f"\n  G1 : {'GECTI' if hepsi else 'KALDI'}")
    print("  ⚠️ TESPIT SUTUNU BOS YERE GECIYOR: depodaki iki kosum aleti de")
    print("     hic kopma BEYAN ETMIYOR, dolayisiyla metrik tanim geregi")
    print("     None doner. M4'un bos kol kapisi FAZ 2'YE ERTELENMISTIR.")
    return hepsi


# ==========================================================================
def g2_tekduzelik() -> bool:
    """Şok derinliği karıştırıcı şiddetiyle tekdüze artıyor mu?

    ⚠️ KISA PENCERE KULLANILIR ve bu beyan edilir: sorulan şey çalışma
    noktasındaki bir DEĞER değil, bir SIRALAMA. Tam uzunluk koşular dört
    güç × üç tohumda saatler sürerdi ve sıralamayı değiştirmezdi.
        ısınma 20 · açılma 80 · ölçüm sonu 110 · koşu sonu 130
    TEMİZ 60 s · ŞOK 15 s (tam pencere) · TOPARLANMA 15 s
    """
    _baslik("G2 - TEKDUZELIK  (sok derinligi siddetle artiyor mu)")
    print("  OLCUT: hicbir DUSUS, iki noktanin BIRLESIK 2 SE'sini asmayacak")
    print()
    print("  🔴 ILK YAZDIGIM OLCUT 'KESIN MONOTON ARTIS' IDI — ve o olcut")
    print("     SINANAMAZ. Iki noktanin gercek degeri de sifirsa (zayif")
    print("     karistiricida oyle), gurultu yuzunden ~%50 olasilikla dusus")
    print("     gorunur; yani DOGRU bir metrik yarisi yarisina kalirdi.")
    print("     Duzeltilen sey esik degil TANIM: 'artis' bir olcumdur ve")
    print("     olculen her sey hata payiyla birlikte okunur.")
    print()
    kisa = dict(isinma_s=20.0, karistirici_baslangic_s=80.0,
                olcum_bitis_s=110.0, kosu_bitis_s=130.0)
    print(f"  {'guc_dBm':>9} {'sok_derinligi (3 tohum ort)':>30} {'SE':>9} "
          f"{'onceki ile fark':>16} {'karar':>18}")
    onceki, onceki_se, hepsi = None, None, True
    for guc in (-30.0, -21.0, -15.0, -9.0):
        derinlikler, seler = [], []
        for tohum in TOHUMLAR:
            kur, kfg, _ = _kos("statik-surekli", tohum,
                               karistirici_guc_override_dbm=guc, **kisa)
            s = _evre(kur, kfg)
            if s["sok_derinligi"] is not None:
                derinlikler.append(s["sok_derinligi"])
                seler.append(s["sok_derinligi_se"])
        ort = ist.mean(derinlikler)
        se = ist.mean(seler) / len(derinlikler) ** 0.5
        if onceki is None:
            karar = "—"
        else:
            fark = ort - onceki
            bant = 2.0 * (se ** 2 + onceki_se ** 2) ** 0.5
            if fark >= 0.0:
                karar = "artis"
            elif -fark <= bant:
                karar = "fark YOK (gurultu)"
            else:
                karar = "🔴 GERCEK DUSUS"
                hepsi = False
            print(f"  {guc:>9.1f} {ort:>30.5f} {se:>9.5f} "
                  f"{fark:>+16.5f} {karar:>18}")
            onceki, onceki_se = ort, se
            continue
        print(f"  {guc:>9.1f} {ort:>30.5f} {se:>9.5f} "
              f"{'—':>16} {karar:>18}")
        onceki, onceki_se = ort, se
    print(f"\n  G2 : {'GECTI' if hepsi else 'KALDI'}")
    if not hepsi:
        print("  🔴 Olcum hatasini ASAN bir dusus var — metrik 'sok")
        print("     derinligi' adini hak etmiyor.")
    return hepsi


# ==========================================================================
def g3_izgara_fazi() -> bool:
    """Izgarayı yarım adım kaydır — kararlar değişiyor mu?

    🔒 Bu kapı doğrudan 8 Eylül dersinden geliyor: ρ'nun üç sabit örnekleme
    anı darbe periyoduyla ÖRTÜŞÜYORDU ve bu sonradan fark edilmişti. Aynı
    hatayı bu sefer yapıdan önce sınıyoruz.
    """
    _baslik("G3 - IZGARA FAZI  (yarim adim kaydir, karar degismesin)")
    print("  OLCUT: hicbir karar kendi hata payindan fazla degismeyecek\n")
    print(f"  {'tohum':>6} {'sok_der':>10} {'kaydirilmis':>12} "
          f"{'fark':>9} {'2SE':>9} {'gecti':>7}")
    hepsi = True
    for tohum in TOHUMLAR:
        kur, kfg, _ = _kos("statik-surekli", tohum)
        a = _evre(kur, kfg)
        b = _evre(kur, kfg, izgara_kaymasi_s=0.5 * IZGARA_ADIMI_S)
        fark = abs(a["sok_derinligi"] - b["sok_derinligi"])
        bant = 2.0 * (a["sok_derinligi_se"] or 0.0)
        gecti = fark <= bant
        hepsi &= gecti
        print(f"  {tohum:>6} {a['sok_derinligi']:>10.5f} "
              f"{b['sok_derinligi']:>12.5f} {fark:>9.5f} {bant:>9.5f} "
              f"{'EVET' if gecti else 'HAYIR':>7}")
    print(f"\n  G3 : {'GECTI' if hepsi else 'KALDI'}")
    return hepsi


# ==========================================================================
def g4_bulaniklik() -> bool:
    """Doğum anına göre kovalamanın bulanıklığı bir ızgara adımını aşıyor mu?

    🔴 Bugün geçmesi bir GARANTİ DEĞİLDİR: koşum aletleri rota beklemez.
    Gerçek bir AODV rota keşfi sırasında paketi kuyrukta tutar ve p99'u
    saniyelere çıkabilir. Bu kapı HER KOLDA, HER PROTOKOLLE yeniden koşar.
    """
    _baslik("G4 - BULANIKLIK  (gecikme p99 / izgara adimi)")
    print("  OLCUT: oran < 1 — yoksa evre atfetme kurali yeniden yazilmali\n")
    print(f"  {'senaryo':>18} {'p99_s':>10} {'oran':>8} {'gecti':>7}")
    hepsi = True
    for senaryo in ("statik-yok", "statik-surekli"):
        kur, kfg, _ = _kos(senaryo, 1000)
        s = _evre(kur, kfg)
        oran = s["bulaniklik_orani"]
        gecti = oran is not None and oran < 1.0
        hepsi &= gecti
        print(f"  {senaryo:>18} {oran * IZGARA_ADIMI_S:>10.6f} "
              f"{oran:>8.4f} {'EVET' if gecti else 'HAYIR':>7}")
    print(f"\n  G4 : {'GECTI' if hepsi else 'KALDI'}")
    return hepsi


if __name__ == "__main__":
    KAPILAR = {"1": g1_bos_kol, "2": g2_tekduzelik,
               "3": g3_izgara_fazi, "4": g4_bulaniklik}
    secim = sys.argv[1:] or list(KAPILAR)
    bilinmeyen = [s for s in secim if s not in KAPILAR]
    if bilinmeyen:
        raise SystemExit(f"bilinmeyen kapi: {bilinmeyen}")
    sonuc = {s: KAPILAR[s]() for s in secim}
    _baslik("SONUC")
    for s, gecti in sonuc.items():
        print(f"  G{s} : {'GECTI' if gecti else '🔴 KALDI'}")
    print("\n  🔒 Dordu de gecmeden evre metrikleri bir SONUC icin")
    print("     kullanilmaz. Kosulmayan kapi 'gecti' sayilmaz.")
    # 🔒 VERDİKT ÇIKIŞ KODUNDA — 16 Eylül 2026.
    # Bu alet 50–70 dakika koşuyor ve verdikti yalnız SON SATIRDA basıyordu;
    # süreç kalan bir kapıda bile 0 ile çıkıyordu. O uzunlukta bir çıktının
    # içindeki tek satırlık `KALDI`, Aşama 2–4 boyunca onlarca kez koşulacak
    # bir listede eninde sonunda kaçırılır. Projenin dersinin ikizi:
    # OKUNMAYAN KAPI DA KAPI DEĞİLDİR.
    if not all(sonuc.values()):
        raise SystemExit("🔴 EVRE METRIKLERI KAPISI KALDI — yukarisi okunmali")
