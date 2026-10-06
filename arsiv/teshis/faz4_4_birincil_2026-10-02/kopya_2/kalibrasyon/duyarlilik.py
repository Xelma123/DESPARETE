"""
DUYARLILIK DENETİMİ — hangi sayılar sonucu belirliyor?

Üretici:
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/duyarlilik.py statik
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/duyarlilik.py hareketli

Şartname karşılığı: `v2/07-SIMULATOR-TASARIMI.md` §11.3.

🔴 NEDEN
========
Köken defterinde **48 parametre `SINANMAMIS`** ve **5'i duyarlılık borcu**.
Hepsini gerekçelendirmek imkânsız; gerekmiyor da. Gereken şey ikiye
ayırmaktır:

    duyarlı  + gerekçesiz → 🔴 ENGEL, çözülmeden ilerlenmez
    duyarsız + gerekçesiz → beyan et, geç

🔒 `DUYARSIZ` kovası **ölçümle hak edilir, iddiayla değil.**

🔴 NE ÖLÇÜLÜYOR — ve NE ÖLÇÜLMÜYOR
==================================
Ölçülen: bir parametreyi oynatmak **çalışma noktasının çıktısını** ve
**yönlendirme ölçütünün bedelini** ne kadar oynatıyor.

⚠️ ÖLÇÜLMEYEN: **protokol SIRALAMASININ** duyarlılığı. Bir parametre mutlak
PDR'yi hiç oynatmadan hangi protokolün kazandığını değiştirebilir. O ölçüm
gerçek protokoller gerektirir ve **Faz 3'e aittir**. Bu yüzden buradan çıkan
etiket `DUYARSIZ (çalışma noktası çıktılarına)`dır; daha fazlası değil.

🔒 İKİ ALET, ÜÇ ÇIKTI — ve üçüncüsü asıl olan
=============================================
    y1 = PDR(`en_guvenilir_kahin`)   mükemmel yönlendirme — TAVAN
    y2 = PDR(`en_kisa_yol_kahin`)    BAŞKA bir yönlendirme ölçütü
    y3 = y1 − y2                     ÖLÇÜTÜN BEDELİ

`y3` sıralama duyarlılığının bugün ölçülebilen en iyi VEKİLİDİR: iki kâhin
aynı dünyayı, aynı trafiği, aynı kanalı görür ve **yalnız yönlendirme
ölçütleri** farklıdır. Bir parametre `y3`ü oynatıyorsa, yönlendirme
stratejileri arasındaki dengeyi oynatıyor demektir — yani protokol
sıralamasını da oynatabilir.

Tek bir çıktıya bakmak yetmezdi: `y1` ve `y2` birlikte hareket edip `y3`ü
sabit bırakabilir *(dünya zorlaştı, ikisi de düştü — ama denge değişmedi)*.

🔒 KARŞILAŞTIRMA EŞLEŞTİRİLMİŞTİR — ilk yazımda DEĞİLDİ ve neredeyse
   taramayı işe yaramaz hâle getiriyordu
=========================================================================
İlk hâli, bozulmamış koşumun tohumlar arası yayılımını gürültü bandı olarak
kullanıyordu. Ölçüldü: o band `pdr_atlama` için **0,134**, ölçüt bedeli için
**0,196** — yani hiçbir parametre duyarlı çıkamazdı ve tarama *"her şey
duyarsız"* diye makul görünen, tamamen gürültüden ibaret bir cevap üretirdi.

🔒 Oysa bu simülatörün RNG mimarisi zaten eşleştirmeyi YAPISAL kılıyor: aynı
tohumda iki kol aynı dünyayı, aynı trafiği, aynı kanalı görür. Dolayısıyla
doğru istatistik **tohum başına FARK**tır; tohumlar arası varyans ortak-mod
olarak düşer. Bandı ortalamaların yayılımından değil, **farkların** kendi
yayılımından hesaplamak gerekir.

⚠️ Bu, oturumda üçüncü kez tekrarlanan bir hata sınıfıdır: ölçütü ölçümün
YAPISINA bakmadan yazmak.

🔒 EŞİK YOK — GÜRÜLTÜ BANDI VAR
===============================
*"Ne kadar oynarsa duyarlıdır"* bir serbest parametredir ve serbest bir
parametre sonuçlar görüldükten sonra seçilir. Onun yerine: bir parametre,
eşleştirilmiş farkın ortalamasını **kendi 2 SE bandından** dışarı çıkarıyorsa
duyarlıdır. Band, koşumun kendi tohumlarından hesaplanır.

🔴 ÖLÇÜT KASTEN ASİMETRİKTİR — ve yönü seçilmiştir
==================================================
Beş tohumla `2 SE`, katı bir anlamda %95'lik bir test DEĞİLDİR *(o t-çarpanı
2,78 isterdi)*. Yani ölçüt **duyarlılığı fazla çağırmaya** meyillidir. Bu bir
kusur değil, seçilmiş bir yön:

    yanlışlıkla `DUYARLI` demek  → parametre gerekçelendirme yığınında kalır
    yanlışlıkla `DUYARSIZ` demek → gerekçesiz bir sayı AKLANIR

İkinci hata bu projede pahalıdır — `DUYARSIZ` bir **iddiadır** ve iddia
edilen şey hak edilmelidir. Dolayısıyla ucuz hatayı seçiyoruz: eleyici
davranmak yerine kuşkucu davranmak.

⚠️ Sonucu: `DUYARLI` listesi **fazla geniş** olacaktır ve bu beyan edilir.
Listeyi daraltmanın yolu eşiği gevşetmek değil, tohum sayısını artırmaktır.

🔴 "DUYARSIZ" İLE "ÖLÇÜLEMEDİ" AYRI ŞEYLERDİR — en tehlikeli tuzak
==================================================================
Bir parametre bu kolda **hiç devrede değilse** çıktıyı oynatmaz — ve saf bir
tarama onu `DUYARSIZ` diye işaretler. `darbe_periyodu_s`i karıştırıcısız bir
kolda taramak tam olarak bunu yapardı: 20 parametre haksız yere aklanırdı.

🔒 AYIRAN ŞEY PARMAK İZİ: simülasyon konfigüre edilmiş dünyada tamamen
belirlenimlidir, dolayısıyla hesaba GERÇEKTEN giren bir parametre çıktının
**bir yerini** değiştirir — 15. ondalığı bile olsa. Çıktı parmak izi
**birebir aynı** kalıyorsa parametre o koşuma hiç girmemiştir.

    parmak izi aynı        → `OLCULEMEDI (bu kolda etkisiz)`
    farklı ama band içinde **ve** |Δ| < R → `DUYARSIZ`
    band dışında **ya da** |Δ| ≥ R        → `DUYARLI`

🔴 İKİNCİ AYAK 16 EYLÜL 2026'DA EKLENDİ — kural YARIM uygulanıyordu.
`cozunurluk.py` kuralı iki ayaklı yazmıştı: *"Bir parametre, ETKİSİ R'DEN
KÜÇÜK **ve** kendi hata payı içindeyse `DUYARSIZ` olur. İkisinden biri
yetmez."* Bu alet yalnız BAND ayağını uyguluyordu; R yalnız köken defterinin
DÜZYAZISINDA vardı, yani ikinci ayak insan hafızasına bağlıydı.

Ölçüldü ve tam o boşluğa düşüldü (`golgeleme_hucre_m`, 20 tohum):
`d_atlama = −0,0605` — **6 PDR puanı**, eşleştirilmiş çözünürlüğün 2,6 katı —
ama tohumlar arası yayılım büyük olduğu için band testini geçiyor ve alet
*"duyarsiz"* basıyordu. `cozunurluk.py`nin başlığı bu senaryoyu kelimesi
kelimesine tarif ediyor ve *"aklamanın en kötü hâli"* diyor.

Bu ayrım el yazımı bir "hangi parametre hangi koldadır" listesi gerektirmez —
öyle bir liste bayatlardı.

⚠️ OAT TARAMASIDIR — birlikte etkiler görülmez
==============================================
Her parametre TEK BAŞINA oynatılıyor (one-at-a-time). İki parametrenin
birlikte oynadığında yaptığı şey görülmez. Bu, tarama taramalarının bilinen
sınırıdır ve beyan edilir: buradan çıkan `DUYARSIZ`, *"tek başına oynatınca
duyarsız"* demektir.

🔒 OYNATMA MİKTARI ×2 ve ×0,5 — ÖLÇEKTEN BAĞIMSIZ
=================================================
Süre, sayı, mesafe, oran — hepsinde aynı anlama gelen tek çarpan budur.
Mutlak bir ±X seçmek her parametre için ayrı bir gerekçe isterdi. Tam sayılar
yuvarlanır, geçersiz değerler `GECERSIZ` diye raporlanır (bastırılmaz).
"""

from __future__ import annotations

import dataclasses
import importlib
import math
import statistics as ist
import sys
import time
from multiprocessing import Pool
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))

from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.olcum.metrikler import metrik_sozlugu  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402
from kalibrasyon import dunya_secimi as DS  # noqa: E402  (K-183)
from sim2.yapilandirma.kokenler import KOKENLER  # noqa: E402
from kalibrasyon.kahin import (EnGuvenilirKahin,  # noqa: E402
                               EnKisaYolKahin, KanalGrafigi)

TOHUMLAR = (1000, 1001, 1002, 1003, 1004)
CARPANLAR = (0.5, 2.0)

# 🔒 DENEYİN ÇÖZÜNÜRLÜĞÜ — TEK KAYNAK (16 Eylül 2026, K-132).
# Bu sayı düzyazıda dolaşıyordu (köken defteri başlığı, karar kayıtları,
# `12` §1) ve bu alet ona HİÇ bakmıyordu. Artık bir sabittir ve karar
# mantığında KULLANILIR.
#     Üretici : `py -3.11 -u kalibrasyon/cozunurluk.py --dunya referans_2026
#               --hucre birincil --tohum 40`
#     Ölçüldü : 2 Ekim 2026 (Faz 4.4, K-213) · referans dünya, BİRİNCİL hücre
#               (formasyon-sürekli · yere_toplama · derin_sizma) ·
#               eşleştirilmiş `olcut_bedeli` · kâhin PDR 0,834 (taban değil).
#     Eski dünyanın 0,0230'u (15 Eylül, K-128) arşivde:
#               `arsiv/teshis/faz4_4_2026-09-30/beklenti.md`.
# ⚠️ EŞLEŞTİRİLMİŞ olan seçildi, en gevşek olan değil: ön-kayıttaki birincil
# test de (Wilcoxon, `06` §7), bu aletin kendi farkı da (`_esli_fark`)
# eşleştirilmiştir. Tek kol çözünürlüğü (0,0316) buraya YAZILSAYDI aklamalar
# deneyin gerçekte görebileceğinden gevşek bir eşiğe karşı yapılırdı —
# K-128'in düzelttiği hatanın daha küçük hâli.
# 🔒 BAYATLIK KAPISI `cozunurluk.py`dedir: o alet R'yi yeniden ölçer ve bu
# sabitle karşılaştırır; ayrışırsa kırmızı yanar. Sabit burada durur çünkü
# `cozunurluk.py` bu modülü içe aktarıyor — ters yön bir döngü olurdu.
R_ESLESTIRILMIS: float = 0.0188

# 🔒 KISA PENCERE, TAMAMEN KARIŞTIRILMIŞ EVREDE. Sorulan şey çalışma
# noktasındaki bir DEĞER değil, bir parametrenin çıktıyı oynatıp
# oynatmadığı. Karıştırıcı pencere açılmadan devrede olduğu için her koşu
# karıştırıcılı bir dünyayı ölçer — karıştırıcı parametreleri de canlıdır.
PENCERE = dict(karistirici_baslangic_s=5.0, isinma_s=10.0,
               olcum_bitis_s=40.0, kosu_bitis_s=50.0)

# 🔒 Adlandırılmış hücreler — senaryo adının taşımadığı TEDAVİ alanlarıyla
# (30 Eylül 2026, Faz 4.4): birincil hücre `formasyon · yere_toplama ·
# derin_sizma · sürekli` (K-186). Taban ve bozuk koşular aynı ekleri alır.
HUCRE_EKLERI: dict[str, dict] = {
    "birincil": {"trafik_deseni": "yere_toplama",
                 "tehdit_senaryosu": "derin_sizma"},
}

# Kova `TEDAVI` olanlar deneyin EKSENİDİR, taranmaz.
ADAYLAR: tuple[str, ...] = tuple(sorted(
    ad for ad, (kova, _) in KOKENLER.items()
    if kova in ("SINANMAMIS", "KOL_TANIMI") and "::" not in ad))

_ALANLAR = {f.name: f for f in dataclasses.fields(Konfig)}

# 🔴 K-198 · OYNATMANIN TABANI SEÇİLİ DÜNYANIN DEĞERİ. Eskiden taban dataclass
# varsayılanıydı — yani ESKİ dünyanın değeri. Referans dünyada (`referans_2026`
# pek çok alanı ezer: irtifa, frekans, yeniden deneme, karıştırıcı gücü…)
# "×0,5" referans değerin yarısı değil, eski değerin yarısı olurdu. Eski
# dünyada davranış birebir aynı kalır (taban yine dataclass varsayılanı).
_TABAN_KONFIG: list = []


def _taban_degeri(ad: str, varsayilan):
    if not DS.referans_mi():
        return varsayilan
    if not _TABAN_KONFIG:
        _TABAN_KONFIG.append(DS.konfig(kol="duyarlilik",
                                       senaryo="statik-surekli",
                                       tohum=TOHUMLAR[0], **PENCERE))
    return getattr(_TABAN_KONFIG[0], ad)


# 🔴 OLASILIK EŞİKLERİ (2 Ekim 2026, K-213). `ATLAMA_ESIGI = 0,90` düz
# çarpılınca ×2 → 1,8 olur: hiçbir bağ eşiği geçmez, kâhin boş grafikte
# koşar ve "etki" bir yapay sıfırdan ölçülür. Çarpılan, TOLERE EDİLEN KAYIP
# payıdır (1 − p): ×0,5 → 0,95 · ×2 → 0,80.
OLASILIK_SABITLERI: frozenset[str] = frozenset({
    "kalibrasyon/kahin.py::ATLAMA_ESIGI",
})


def _modul_sabiti(ad: str):
    """`"sim2/dunya/mobilite.py::ISTASYON_TUTMA_S"` → (modül, ad, değer)."""
    yol, _, sabit = ad.partition("::")
    modul = importlib.import_module(yol.removesuffix(".py").replace("/", "."))
    return modul, sabit, getattr(modul, sabit)


def _oynat(ad: str, carpan: float):
    """Parametrenin oynatılmış değeri; oynatılamıyorsa `None`.

    🔒 Tür KONFİGDEN okunur, elle eşlenmez: yeni bir alan eklendiğinde bu
    fonksiyon onu kendiliğinden doğru oynatır.
    🔒 Faz 4.4 (2 Ekim 2026): `yol::AD` bir MODÜL SABİTİDİR (köken
    defterindeki adıyla); türü değerinden okunur, işçide koşudan önce
    yamalanır ve sonra geri alınır (`_kos`).
    """
    if "::" in ad:
        _m, _a, deger = _modul_sabiti(ad)
        if ad in OLASILIK_SABITLERI:
            return 1.0 - (1.0 - deger) * carpan
        if isinstance(deger, bool):
            return not deger
        if isinstance(deger, int):
            yeni = round(deger * carpan)
            return yeni if yeni != deger else None
        return deger * carpan
    alan = _ALANLAR.get(ad)
    if alan is None:
        return None
    # 🔴 OYNATMA, TARAMANIN KULLANDIĞI DEĞERE GÖRE — dataclass
    # varsayılanına göre DEĞİL. `PENCERE` üç zaman alanını eziyor; onları
    # varsayılana göre oynatmak "x0,5" etiketiyle 2,5 kat büyütmek demekti.
    varsayilan = PENCERE.get(ad, _taban_degeri(ad, alan.default))
    tip = str(alan.type)
    if tip == "bool":
        return not varsayilan
    if tip == "int":
        yeni = int(round(varsayilan * carpan))
        return yeni if yeni != varsayilan else None
    if tip == "float":
        return varsayilan * carpan
    if ad == "modulasyon":
        # 🔴 İLK TARAMADA HİÇ OYNATILMAMIŞTI: `str` hiçbir dala girmiyordu ve
        # parametre "OLCULEMEDI" diye raporlandı — yani ölçülmediği hâlde
        # "bu kolda etkisiz" gibi göründü. Tam da mekanizmanın engellemek
        # için var olduğu hata.
        from sim2.kanal.kanal import MODULASYONLAR
        digeri = [m for m in MODULASYONLAR if m != varsayilan]
        return digeri[0] if digeri else None
    if ad == "karistirici_guc_override_dbm":
        # 🔴 dBm LOGARİTMİKTİR — çarpmak anlamsız. Taban güç eski dünyada
        # −15,0 dBm, referans dünyada o dünyanın ETKİN gücü (K-198);
        # ±3 dB (yani güçte iki kat) oynatılır.
        taban = (_taban_degeri("karistirici_guc_dbm", -15.0)
                 if DS.referans_mi() else -15.0)
        return taban + (3.0 if carpan > 1.0 else -3.0)
    if ad == "karistirici_konum":
        # Varsayılan `None` = alan merkezi. Oynatma = köşeye taşı — alanın
        # ÇEYREĞİ (eski dünyanın 450 / 1350 m'si 1800 m'lik alanın ¼ ve ¾'ü;
        # referans dünyada aynı oran, K-198).
        en = (_taban_degeri("alan_en_m", 1800.0) if DS.referans_mi()
              else 1800.0)
        return (0.25 * en, 0.25 * en) if carpan > 1.0 else (0.75 * en,
                                                             0.75 * en)
    return None


def _kos(senaryo: str, tohum: int, alet: str, ek: dict):
    # 🔴 `ek`, PENCERE alanlarını EZEBİLMELİ. İlk yazımda ikisi de ayrı ayrı
    # geçiyordu ve `isinma_s` gibi bir pencere alanı oynatıldığında koşum
    # `TypeError` ile patlıyordu — üstelik hata "GECERSIZ" diye düşülüp
    # parametre "OLCULEMEDI" kovasına girdiği için SESSİZCE AKLANIYORDU.
    modul_ek = {a: d for a, d in ek.items() if "::" in a}
    ek = {a: d for a, d in ek.items() if "::" not in a}
    eskiler = []
    try:
        for ad, deger in modul_ek.items():
            modul, sabit, eski = _modul_sabiti(ad)
            eskiler.append((modul, sabit, eski))
            setattr(modul, sabit, deger)
        kfg = DS.konfig(kol="duyarlilik", senaryo=senaryo, tohum=tohum,
                        **{**PENCERE, **ek})
        kur = kurulum_yap(kfg)
        if alet == "en_guvenilir_kahin":
            g = KanalGrafigi(kur)
            kosu = Kosu(kur, lambda i: EnGuvenilirKahin(i, g))
        else:
            g = KanalGrafigi(kur)
            kosu = Kosu(kur, lambda i: EnKisaYolKahin(i, g))
        kosu.kostur()
    finally:
        for modul, sabit, eski in reversed(eskiler):
            setattr(modul, sabit, eski)
    s = metrik_sozlugu(kur.sayaclar.disa_ver(), kur.paket_defteri,
                       kur.rota_defteri)
    say = kur.sayaclar
    # 🔒 PARMAK İZİ — "duyarsız" ile "ölçülemedi"yi ayıran şey.
    # Belirlenimli bir simülasyonda hesaba giren her parametre burada bir
    # şeyi değiştirir; hiçbirini değiştirmiyorsa hiç girmemiştir.
    izi = (int(say.oku("teslim_paket")), int(say.oku("mac_deneme")),
           int(say.oku("kontrol_cerceve")),
           repr(s["gecikme_ort_s_pencere"]))
    return (s["pdr_pencere"], izi)


def _is(gorev):
    """Havuz işçisi. 🔒 Modül düzeyinde — Windows `spawn` başka türlü
    seçemez (çalışma kuralı 11)."""
    senaryo, tohum, alet, ek = gorev
    try:
        return _kos(senaryo, tohum, alet, ek), None
    except Exception as hata:                       # noqa: BLE001
        return None, f"{type(hata).__name__}: {hata}"


CIKTILAR = ("pdr_etx", "pdr_atlama", "olcut_bedeli")


def _tohum_ciktilari(pdr: dict) -> dict[str, float]:
    """Bir tohumun üç çıktısı. `pdr[(alet, tohum)]` sözlüğünden."""
    etx, atl = pdr["en_guvenilir_kahin"], pdr["en_kisa_yol_kahin"]
    return {"pdr_etx": etx, "pdr_atlama": atl, "olcut_bedeli": etx - atl}


def _esli_fark(bozuk: dict, taban: dict) -> dict[str, tuple[float, float]]:
    """🔒 TOHUM BAŞINA fark; ortalama ve 2 SE.

    Eşleştirme yapısaldır: aynı tohumda iki koşu aynı dünyayı görür,
    dolayısıyla tohumlar arası varyans ortak-mod olarak DÜŞER. Ortalamaların
    farkını almak o varyansı bandın içinde bırakırdı — ve band, ölçülmek
    istenen etkiden büyük olurdu.
    """
    cikti: dict[str, tuple[float, float]] = {}
    for ad in CIKTILAR:
        farklar = [bozuk[t][ad] - taban[t][ad]
                   for t in sorted(taban) if t in bozuk]
        if not farklar:
            continue
        ort = ist.mean(farklar)
        band = (2.0 * ist.stdev(farklar) / math.sqrt(len(farklar))
                if len(farklar) > 1 else 0.0)
        cikti[ad] = (ort, band)
    return cikti


def tarama(senaryo: str, isci: int = 8, adaylar=None,
           taban_ek: dict | None = None) -> None:
    adaylar = tuple(adaylar or ADAYLAR)
    taban_ek = dict(taban_ek or {})
    aletler = ("en_guvenilir_kahin", "en_kisa_yol_kahin")
    print("=" * 100)
    print(f"DUYARLILIK TARAMASI — senaryo '{senaryo}' · {len(adaylar)} aday "
          f"· {len(TOHUMLAR)} tohum · carpanlar {CARPANLAR}")
    print("=" * 100)
    print("  OLCUT — IKI AYAK, biri yeterse DUYARLI (`cozunurluk.py`):")
    print("    band : etki KENDI hata payindan buyuk mu (istatistiksel)")
    print(f"    R    : |D| >= {R_ESLESTIRILMIS:.4f} mi — deneyin gorebilecegi")
    print("           en kucuk ESLESTIRILMIS fark (pratik)")
    print("  🔴 parmak izi BIREBIR ayniysa 'DUYARSIZ' DEGIL 'OLCULEMEDI'")
    print()

    gorevler, etiketler = [], []
    for alet in aletler:
        for tohum in TOHUMLAR:
            gorevler.append((senaryo, tohum, alet, dict(taban_ek)))
            etiketler.append(("__taban__", 1.0, alet, tohum))
    for ad in adaylar:
        for carpan in CARPANLAR:
            deger = _oynat(ad, carpan)
            if deger is None:
                continue
            for alet in aletler:
                for tohum in TOHUMLAR:
                    gorevler.append((senaryo, tohum, alet,
                                     {**taban_ek, ad: deger}))
                    etiketler.append((ad, carpan, alet, tohum))

    print(f"  toplam kosu: {len(gorevler)}  ·  {isci} isci")
    t0 = time.perf_counter()
    with Pool(isci) as havuz:
        ham = havuz.map(_is, gorevler, chunksize=1)
    print(f"  kosum suresi: {(time.perf_counter() - t0) / 60:.1f} dk\n")

    # --- topla: (parametre, carpan, alet, tohum) -----------------------
    pdr: dict[tuple, float] = {}
    izler: dict[tuple, tuple] = {}
    hatalar: dict[tuple, str] = {}
    for (ad, carpan, alet, tohum), (sonuc, hata) in zip(etiketler, ham):
        if hata is not None:
            hatalar.setdefault((ad, carpan), hata)
            continue
        pdr[(ad, carpan, alet, tohum)] = sonuc[0]
        izler[(ad, carpan, alet, tohum)] = sonuc[1]

    def _tohumlar(ad, carpan):
        """`{tohum: {cikti: deger}}` — tohum başına üç çıktı."""
        cikti = {}
        for tohum in TOHUMLAR:
            a = pdr.get((ad, carpan, "en_guvenilir_kahin", tohum))
            b = pdr.get((ad, carpan, "en_kisa_yol_kahin", tohum))
            if a is None or b is None:
                continue
            cikti[tohum] = {"pdr_etx": a, "pdr_atlama": b,
                            "olcut_bedeli": a - b}
        return cikti

    taban = _tohumlar("__taban__", 1.0)
    taban_izi = {(alet, tohum): izler[("__taban__", 1.0, alet, tohum)]
                 for alet in aletler for tohum in TOHUMLAR
                 if ("__taban__", 1.0, alet, tohum) in izler}
    ort_taban = {k: ist.mean(t[k] for t in taban.values()) for k in CIKTILAR}

    print(f"  TABAN: " + " · ".join(f"{k} {v:.4f}"
                                    for k, v in ort_taban.items()))
    print("  🔒 Band artik TOHUM BASINA FARKLARIN yayilimindan; ortalamalarin")
    print("     yayilimindan DEGIL. Esleştirme yapisal oldugu icin tohumlar")
    print("     arasi varyans ortak-mod olarak dusuyor.")
    print()
    print(f"  {'parametre':<30} {'carpan':>7} {'d_pdr_etx':>10} "
          f"{'d_atlama':>10} {'d_bedel':>10} {'|D|/band':>10} "
          f"{'|D|/R':>8} {'karar':>12}")

    # 🔴 `GECERSIZ` EN YÜKSEK ÖNCELİK — ve sebebi ilk taramada görüldü:
    # üç pencere alanı `TypeError` verdi, hata düşüldü ama karar
    # `OLCULEMEDI` kaldı. Yani ÖLÇÜLEMEYEN bir şey "bu kolda etkisiz" diye
    # raporlandı. Bir ölçüm aracının kendi arızasını, ölçtüğü şeyin özelliği
    # gibi göstermesi bu projedeki en pahalı hata sınıfıdır.
    ONCELIK = {"OLCULEMEDI": 0, "duyarsiz": 1, "DUYARLI": 2, "GECERSIZ": 3}
    kararlar: dict[str, str] = {}
    satirlar = []
    for ad in adaylar:
        en = "OLCULEMEDI"
        for carpan in CARPANLAR:
            if (ad, carpan) in hatalar:
                satirlar.append((ad, carpan, None, "GECERSIZ"))
                en = "GECERSIZ"
                continue
            bozuk = _tohumlar(ad, carpan)
            if not bozuk:
                # 🔴 Oynatma üretilemediyse parametre HİÇ SINANMADI —
                # "etkisiz" değil. İkisi ayrı kovaya gider.
                satirlar.append((ad, carpan, None, "OYNATILAMADI"))
                en = "GECERSIZ"
                continue
            farklar = _esli_fark(bozuk, taban)
            ayni = all(
                izler.get((ad, carpan, alet, tohum)) == taban_izi[(alet, tohum)]
                for (alet, tohum) in taban_izi
                if (ad, carpan, alet, tohum) in izler)
            # 🔒 En büyük "band kaç katı" oranı — hangi çıktının konuştuğunu
            # da gösterir. Band sıfırsa (üç tohumda tam aynı fark) sıfırdan
            # farklı her etki duyarlıdır.
            oran = 0.0
            en_buyuk = 0.0
            for k, (fark, band) in farklar.items():
                en_buyuk = max(en_buyuk, abs(fark))
                if band > 0.0:
                    oran = max(oran, abs(fark) / band)
                elif abs(fark) > 0.0:
                    oran = float("inf")
            if ayni:
                karar = "OLCULEMEDI"
            elif oran > 1.0 or en_buyuk >= R_ESLESTIRILMIS:
                # 🔒 İKİ AYAK, BİRİ YETERSE `DUYARLI` (`cozunurluk.py`):
                #   band — etki KENDİ hata payından büyük mü (istatistiksel)
                #   R    — etki DENEYİN görebileceğinden büyük mü (pratik)
                # R ayağı olmadan, yayılımı büyük bir çıktıdaki 6 puanlık bir
                # etki "duyarsız" diye aklanıyordu.
                karar = "DUYARLI"
            else:
                karar = "duyarsiz"
            satirlar.append((ad, carpan, (farklar, oran, en_buyuk), karar))
            if ONCELIK[karar] > ONCELIK[en]:
                en = karar
        kararlar[ad] = en

    for ad, carpan, veri, karar in satirlar:
        isaret = "🔴 " if karar == "DUYARLI" else ""
        if veri is None:
            print(f"  {ad:<30} {carpan:>7.2f} {'—':>10} {'—':>10} "
                  f"{'—':>10} {'—':>15} {isaret + karar:>12}")
            continue
        farklar, oran, en_buyuk = veri
        o = "∞" if oran == float("inf") else f"{oran:.1f}x"
        r = f"{en_buyuk / R_ESLESTIRILMIS:.1f}R"
        print(f"  {ad:<30} {carpan:>7.2f} "
              f"{farklar['pdr_etx'][0]:>+10.5f} "
              f"{farklar['pdr_atlama'][0]:>+10.5f} "
              f"{farklar['olcut_bedeli'][0]:>+10.5f} {o:>10} {r:>8} "
              f"{isaret + karar:>12}")

    print()
    print("=" * 100)
    print("OZET")
    print("=" * 100)
    for etiket in ("GECERSIZ", "DUYARLI", "duyarsiz", "OLCULEMEDI"):
        adlar = sorted(a for a, k in kararlar.items() if k == etiket)
        isaret = "🔴 " if etiket in ("DUYARLI", "GECERSIZ") else ""
        print()
        print(f"  {isaret}{etiket}  ({len(adlar)})")
        for a in adlar:
            print(f"    · {a}")
    if hatalar:
        print()
        print(f"  GECERSIZ OYNATMA ({len(hatalar)}) — bastirilmadi:")
        for (ad, carpan), h in sorted(hatalar.items()):
            print(f"    · {ad} x{carpan}: {h[:90]}")
    print()
    print("  🔴 'OLCULEMEDI' AKLAMA DEGILDIR: o parametre bu kolda hesaba")
    print("     hic girmedi. Canli oldugu bir kolda YENIDEN taranmali.")
    print("  ⚠️ 'duyarsiz' = TEK BASINA oynatinca duyarsiz (OAT sinirlamasi)")
    print("     ve YALNIZ calisma noktasi ciktilarina. Protokol SIRALAMASININ")
    print("     duyarliligi gercek protokoller gerektirir — Faz 3.")


if __name__ == "__main__":
    # 30 Eylül 2026 (Faz 4 kapanışı B7): `--dunya` okunur ve basılır;
    # `_kos` dünyayı seçimden kurar (K-183), işçilere ortam değişkeniyle.
    DS.secimi_oku()
    print(f"  DUNYA: {DS.secili()}")
    # 🔒 Windows `spawn` bu korumasiz havuzu kilitler — calisma kurali 11.
    # 🔒 HER PARAMETRE, CANLI OLDUĞU KOLDA TARANIR. `statik-surekli`de
    # darbeli/taramalı/reaktif sabitleri hesaba hiç girmez ve "OLCULEMEDI"
    # çıkar — bu bir aklama DEĞİL, "yanlış kolda baktın" demektir.
    SENARYOLAR = {"statik": "statik-surekli",
                  "darbeli": "statik-surekli_darbeli",
                  "taramali": "statik-taramali",
                  "reaktif": "statik-reaktif",
                  "hareketli": "bagimsiz-surekli",
                  "gorev": "gorev-surekli",
                  "birincil": "formasyon-surekli"}
    argv = sys.argv[1:] or ["statik"]
    # 🔒 `--tohum N` — 16 Eylül 2026 (B5). Beş tohum, bir |Δ| KESTİRİMİ verir
    # ve o kestirimin kendi hata payı vardır. Eşik eşleştirilmiş çözünürlüğe
    # bağlandıktan sonra (K-132) eşiğin KIYISINDAKİ kayıtların daha çok
    # tohumla yeniden ölçülmesi gerekti; sayıyı sabit tutmak o ölçümü
    # imkânsız kılıyordu. İlk tohum DEĞİŞMEZ, yalnız sayı büyür.
    if "--tohum" in argv:
        i = argv.index("--tohum")
        TOHUMLAR = tuple(range(TOHUMLAR[0], TOHUMLAR[0] + int(argv[i + 1])))
        argv = argv[:i] + argv[i + 2:]
    anahtar = argv[0]
    if anahtar not in SENARYOLAR:
        raise SystemExit(f"bilinmeyen: {anahtar} — {list(SENARYOLAR)}")
    secili = argv[1:] or None
    print(f"  tohum sayisi: {len(TOHUMLAR)} "
          f"({TOHUMLAR[0]}–{TOHUMLAR[-1]})")
    tarama(SENARYOLAR[anahtar], adaylar=secili,
           taban_ek=HUCRE_EKLERI.get(anahtar))
