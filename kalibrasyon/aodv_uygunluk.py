"""
U1 — AODV'nin teslim oranı kâhin referansına YAKIN mı? (`v2/06` §4.3)

Üretici:
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/aodv_uygunluk.py
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/aodv_uygunluk.py --protokol olsr
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/aodv_uygunluk.py duman
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/aodv_uygunluk.py hukum [kayit]
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/aodv_uygunluk.py u3

🔒 BÜTÜN TABAN PROTOKOLLERİN U1 KAPISI — adı TARİHSELDİR (19 Eylül 2026)
Eşikler üç taban protokolü birden bağlar (K-136); dolayısıyla hüküm kodu TEK
kalmalı — OLSR için ikinci bir alet yazmak, iki hükmün bir gün ayrışması
demek olurdu. Protokol bir argümandır; açıklanmış düşük hücre listesi
protokol başınadır. Dosya adı AODV ilk protokol olduğu için böyle kaldı:
adı değiştirmek köken defterindeki ve belgelerdeki atıfları kırardı.

🔴 BU DOSYA NEDEN VAR — BİR KAPI YANLIŞ YERDE KURULMUŞTU
========================================================
U1'in ilk hâli `tests2/test_aodv.py` içinde MUTLAK bir eşikti: `PDR ≥ 0,95`.
Eşik gevşek ya da sıkı olduğu için değil, **yanlış dünyada** durduğu için
yanlıştı. `06` §4.3'ün ölçütü *"teslim oranı KÂHİN REFERANSINA yakın"*dır ve
o referans konfigürasyona bağlıdır; tam ölçekte ölçülmüş bir referans
(0,996–1,000) 14 düğümlük test dünyasına taşınmıştı. Aynı dünyada ölçünce:

    kâhin 0,9687  ·  AODV 0,8512  ·  oran 0,879

Yani test kırmızıydı ama gösterdiği şey protokolün kusuru değil, kapının
kendi kusuruydu. Bir kapı neyi ölçtüğünü bilmiyorsa, kırmızı yanması bir
teşhis değildir.

🔒 ÖLÇÜT ORANDIR, MUTLAK DEĞER DEĞİL
====================================
Kapı AODV'yi **aynı konfigürasyonda** koşan ETX kâhinine oranlar:

    oran = PDR(AODV) / PDR(EnGuvenilirKahin)

Oranın üç kazancı var:
  1. *"Yakın"* sözcüğü ölçülebilir hâle gelir — neye yakın olduğu yazılıdır.
  2. §4.3'ün *"bağlı ağ"* ön koşulu **kendini nötrler**: kâhinin geçemediği
     bir bölünme paydayı da düşürür, dolayısıyla topolojinin kusuru
     protokolün hanesine yazılmaz. Ayrı bir bağlantılılık taraması gerekmez.
  3. Kâhin MAC'i, kanalı, kuyruğu ve TTL'i değiştirmez (`pdr_tavani.py`);
     yani payda *"yönlendirme hiç hata yapmasaydı"* demektir ve oran tam
     olarak **yönlendirmenin payını** ölçer.

🔒 EŞİKLER — ÖĞRENCİ KARARI, 17 Eylül 2026 (`04` K-136)
=======================================================
    statik kol     oran ≥ 0,90
    hareketli kol  oran ≥ 0,60

Hareketli kolun eşiği neden bu kadar düşük: kâhin her an en güvenilir yolu
BİLİR; gerçek bir protokol o yolu HELLO gecikmesi kadar sonra öğrenir ve
hareket, bağları kâhinin hiç ödemediği bir hızda kırar. `06` §4.3 bunu zaten
söylüyordu — *"«≈ 1» yalnız statik kolda anlamlıdır"*.

🔴 EŞİK, SAYILAR GÖRÜLDÜKTEN SONRA SEÇİLDİ — VE BU BİR ZAYIFLIKTIR
==================================================================
Ön-kayıt disiplini ölçütün ölçümden ÖNCE yazılmasını ister (`03` §2). Burada
öyle olmadı: öğrenciye dört ölçülmüş oran gösterildi ve eşiği onların üstünde
seçti. Bu gizlenmiyor; üç hafifletici sebeple birlikte yazılıyor:

  1. U1 bir **kabul kapısıdır**, bir hipotez testi değil. `06` §4.4 onu
     *"geçilmeden protokol kabul edilmez"* diye tanımlar; hiçbir sonuç
     iddiası bu eşiğe dayanmıyor ve dayanmayacak.
  2. Eşik **üç taban protokolü de** bağlayacak. AODV'ye göre ayarlanmış
     olması OLSR ve AOMDV'ye bir avantaj sağlamaz — tersine, AODV'nin
     bugünkü değerine yakın bir eşik onlar için DAHA sıkıdır.
  3. Seçenekler, hangisinin bugün geçtiği açıkça yazılarak sunuldu.

⚠️ AÇIK BORÇ: eşiğin seçildiği dört sayı KISA PENCEREDE ölçülmüştü
(`ısınma 10 · ölçüm 40 · koşu 50 s`); bu alet GERÇEK pencerede koşar
(`50 · 320 · 350`). Aynı koşu tam pencerede 0,9875 değil **0,9777** verdi —
yön aşağı. Eşik buna rağmen DEĞİŞTİRİLMEDİ: sonuç görüldükten sonra bir
ölçütü gevşetmek de sıkmak da aynı hatadır (`03` §2.1). Tam pencerede ölçülen
değerler aşağıda basılıyor; OLSR ve AOMDV yazıldığında eşik onların da
karşısında sınanacak ve gerekirse KARAR YENİDEN ALINIP kayda geçirilecek.

🔴 KAPI İKİ PARÇADIR (17 Eylül 2026, K-137 · öğrenci kararı "A")
================================================================
İlk hâlinde U1 iki ayrı soruyu tek kapıya bağlıyordu — *"gerçekleme RFC'ye
sadık mı"* ve *"protokol iyi teslim ediyor mu"*. İkincisi bir kabul ölçütü
DEĞİL, deneyin kendi sonucudur: AODV'nin zayıf bağlı bir topolojide kötü
teslim vermesi, gerçeklemenin bozuk olduğunu göstermez — RFC 3561 atlama
sayısıyla yönlendirir ve **bağ kalitesi eşiği yoktur**.

    U1-U · UYGUNLUK   defter kapanıyor · teslim var · kâhin AŞILMIYOR
                      → kalırsa protokol KABUL EDİLMEZ
    U1-B · BAŞARIM    oran eşikleri
                      → kalırsa protokol reddedilmez, ama hücre
                        AÇIKLANMADAN geçemez

🔒 "AÇIKLANMADAN GEÇEMEZ" KAPININ DİŞİDİR — ve üç yönlü denetlenir:
  1. Eşiğin altındaki hücre `ACIKLANMIS_DUSUK`ta yoksa kapı KIRMIZI yanar.
  2. Listedeki bir hücre ARTIK düşük değilse o bir **ölü kayıttır** ve kapı
     yine KIRMIZI yanar — bir muafiyet listesi kendi bayatlığını gizleyemez
     (köken defterinin D12 taramasıyla aynı disiplin).
  3. Uygunluk parçası her hâlükârda bağlayıcıdır ve gevşetilemez.

🔒 KAPI ÇIKIŞ KODUNA BAĞLIDIR — geçti 0, kaldı 1.
"""

from __future__ import annotations

import json
import statistics as ist
import sys
import time
from multiprocessing import Pool
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
for _yol in (KOK, KOK / "tests2"):
    if str(_yol) not in sys.path:
        sys.path.insert(0, str(_yol))

from kalibrasyon.kahin import EnGuvenilirKahin, KanalGrafigi  # noqa: E402
from protokoller.aodv import AODV  # noqa: E402
from protokoller.olsr import OLSR  # noqa: E402
from protokoller.aomdv import AOMDV  # noqa: E402
from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.kosum.sonuc import sonuc_satiri  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402

__all__ = ["U1_ESIK_STATIK", "U1_ESIK_HAREKETLI", "KOLLAR", "TOHUMLAR", "u1",
           "hukum", "PROTOKOLLER"]

# Kapının sınadığı taban protokoller — ad → sınıf.
PROTOKOLLER = {"aodv": AODV, "olsr": OLSR, "aomdv": AOMDV}

# 🔒 Tam koşumun ölçtüğü hücreler buraya yazılır (`regresyon_satirlari.py`
# ile aynı gelenek). Sebebi ölçüldü, 19 Eylül 2026: açıklanmış hücre listesi
# değiştiğinde verdikti yeniden üretmek için 4 SAATLİK koşumu tekrarlamak
# gerekiyordu — oysa simülasyon deterministik ve ölçülen sayılar değişmez.
# `hukum` kipi aynı DEĞERLENDİRME KODUNU kayıtlı sayılara uygular; ikinci
# bir hüküm gerçeklemesi yazılmaz.
DIZIN = KOK / "ciktilar2" / "aodv_uygunluk"

# 🔒 ÖLÇÜTÜN KENDİSİ — öğrenci kararı (K-136). Tek kaynak burasıdır; başka
# hiçbir dosya bu iki sayıyı yeniden yazmaz.
U1_ESIK_STATIK: float = 0.90
U1_ESIK_HAREKETLI: float = 0.60

# 🔒 U1 KARIŞTIRICISIZDIR (`06` §4.3) — dört hareketlilik kolunun `-yok`
# senaryosu. Karıştırma altındaki davranış U1'in işi değil; onu H1 ailesi
# ölçer ve orada kâhin de bozulur.
KOLLAR: tuple[str, ...] = ("statik-yok", "bagimsiz-yok",
                           "gorev-yok", "formasyon-yok")
# 🔒 GELİŞTİRME TOHUMLARI. Ana deney tohumları (2000–2039) burada KOŞULMAZ —
# `06` §0.2: *"hiçbir kolda koşulmaz"*, mühür bozulmaz.
TOHUMLAR: tuple[int, ...] = (1000, 1001, 1002)
# 🔒 AÇIKLANMIŞ DÜŞÜK HÜCRELER (`06` §4.4 madde 3 · `04` K-137 §4).
# Bir hücrenin buraya girmesinin ŞARTI, kaybın bir yazılım kusurundan DEĞİL
# protokolün kendi mekanizmasından geldiğinin ÖLÇÜLMÜŞ olmasıdır. Üretici:
# yapısal ölçüm simülasyon koşmaz, doğrudan kanal grafiğinden okur.
# 🔴 Ayıran değişken TEK: eşiksiz en kısa yolun uçtan uca teslimi. AODV'nin
# bağ kalitesi kabul eşiği yoktur; hedef ilk ulaşan RREQ kopyasının ters
# yoluna cevap verir ve o kopya genelde en az atlamalı, yani en uzun bağlı
# olandır. Dört kolun DÖRDÜNDE de en düşük eşiksiz atlama yoluna sahip hücre,
# en düşük U1 oranına sahip.
# 🔒 PROTOKOL BAŞINA: bir protokolün açıklaması öbürünü aklamaz — her
# protokolün düşük hücresi KENDİ ölçümüyle açıklanır.
# 🔴 İKİ KAYIT ÖLÜ KAYIT TARAMASIYLA SİLİNDİ (19 Eylül 2026, `04` K-145).
# RFC §6.11 öncül kuralı düzelince (K-143, AODV-e) iki hücre eşiği geçti ve
# kapı onları kendiliğinden yakaladı — tasarlandığı gibi:
#     statik-yok/1002     0,897 → 0,932   (eşik 0,90)
#     formasyon-yok/1002  0,572 → 0,646   (eşik 0,60)
# ⚠️ statik-yok/1002'nin açıklaması (eşiksiz en kısa yol kolun en düşüğü)
# YANLIŞ DEĞİLDİ — hücre hâlâ statik kolun en düşüğü. Ama eşiğin altında
# kalmasının sebebi o yapıyla §6.11 kusurunun BİRLEŞİMİYDİ; kusur gidince
# hücre geçti. Açıklamanın TEK BAŞINA yeterli sayılması bir hataydı.
ACIKLANMIS_DUSUK: dict[str, dict[tuple[str, int], str]] = {"aodv": {
    ("bagimsiz-yok", 1002):
        "esiksiz en kisa yol 0,2386 (kolun en dusugu; 1000'de 0,4589). "
        "Ag hicbir anda bolunmuyor. K-137 §4",
    ("gorev-yok", 1001):
        "esiksiz en kisa yol 0,2502 (kolun en dusugu; 1000'de 0,5519). "
        "Ag hicbir anda bolunmuyor. K-137 §4",
}, "olsr": {}, "aomdv": {
    # 🔒 AOMDV, AODV'nin atlama sayısıyla yönlendirmesini miras alır; bağ
    # kalitesi kabul eşiği YOKTUR. Ölçüm tam pencerede, bu hücrede yapıldı
    # (22 Eylül 2026; `arsiv/teshis/aomdv_gorev1001_2026-09-22/`, ön-kayıtlı
    # dört hipotez).
    ("gorev-yok", 1001):
        "esiksiz en kisa yol 0,2502 (kolun en dusugu; 1000'de 0,5519; "
        "K-137 §4). Tam pencerede OLCULDU: veri basarisizliklarinin %70'i, "
        "atlama teslim olasiligi 0,90'in ALTINDAKI baglarda — o baglar "
        "kullanimin yalniz %23'u. Rota boslugu yok (hedef_yok 0), tampon "
        "tavani baglamiyor (dusen 0), kayip birkac akista yogun (10 akisin "
        "3'u neredeyse hic teslim etmiyor, 2'si tam). AODV ayni hucrede ayni "
        "desen (%72 / %25) ve daha dusuk. K-149",
}}

DUMAN_KOLLARI: tuple[str, ...] = ("statik-yok",)
DUMAN_TOHUMLARI: tuple[int, ...] = (1000,)
# 🔴 DUMAN KESİTİ SAYIYI ÜRETMEZ — ve bunun sebebi ölçüldü: tam pencerede
# TEK bir (AODV, kâhin) çifti 505 s sürüyor, yani `uretici_duman.py`nin
# *"ucuz kesit"* sözleşmesi tam pencereyle tutturulamaz. Kesit bu yüzden
# KISA pencere koşar ve bastığı oran KAPININ ORANI DEĞİLDİR.
# 🔒 Kısa pencere `yere_toplama_yuku.py::YAN_GOZLEM_PENCERESI` ile aynı
# idiomdur ve orada da aynı beyanla duruyor.
DUMAN_PENCERESI: dict[str, float] = {
    "isinma_s": 10.0, "olcum_bitis_s": 40.0, "kosu_bitis_s": 50.0}


def _pdr(kfg: Konfig, kahin: bool, protokol: str = "aodv") -> tuple:
    """Bir koşu — (PDR, korunum geçerli mi, tampon teşhisi).

    🔒 TAMPON TEŞHİSİ AYNI KOŞUMDAN OKUNUYOR ve sebebi bir çalışma kuralı
    (`03` §1, 17 Eylül 2026): *bir iş bitirilir, sonra ölçülür* — aynı
    dört saatlik koşumu iki ayrı soru için iki kez koşmak yerine, kapanış
    koşumu iki soruyu birden cevaplar.

    ⚠️ İkinci soru: `rota_tamponu_kapasitesi` (64) ve `rota_tamponu_omru_s`
    (30 s) NS-2 geleneğinden geldi ve bu projede HİÇ ölçülmedi (ikisi de
    `SINANMAMIS`). Eğer tampon hiçbir kolda dolmuyor ve hiçbir paket süre
    tavanından düşmüyorsa, sonuç bu iki parametreye DUYARSIZ demektir ve
    borç ölçümle kapanır.
    """
    kur = kurulum_yap(kfg)
    if kahin:
        grafik = KanalGrafigi(kur)
        kosu = Kosu(kur, lambda i: EnGuvenilirKahin(i, grafik))
    else:
        kosu = Kosu(kur, PROTOKOLLER[protokol])
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "u1")
    m = satir["metrikler"]
    tampon = {ad: m.get(ad) for ad in
              ("tampon_giris", "tampon_dusen", "en_yuksek_tampon")}
    return m["pdr"], satir["korunum"]["gecerli"], tampon


def _is(gorev):
    """Havuz işçisi: (kol, tohum, kâhin mi, pencere, protokol) → ölçüm."""
    kol, tohum, kahin, pencere, protokol = gorev
    try:
        t0 = time.perf_counter()
        pdr, gecerli, tampon = _pdr(
            Konfig(kol="u1", senaryo=kol, tohum=tohum, **dict(pencere)), kahin,
            protokol)
        return {"pdr": pdr, "gecerli": gecerli, "tampon": tampon,
                "sure": time.perf_counter() - t0}, None
    except Exception as e:                       # noqa: BLE001
        return None, f"{type(e).__name__}: {e}"


def u1(kollar=KOLLAR, tohumlar=TOHUMLAR, isci: int = 8,
       pencere: dict[str, float] | None = None,
       protokol: str = "aodv") -> int:
    """U1 kapısı. Çıkış kodu: 0 geçti, 1 kaldı.

    ⚠️ `pencere` YALNIZ duman kesiti içindir ve verildiğinde bastığı oran
    kapının oranı DEĞİLDİR; başlıkta bir uyarı satırı basılır.
    """
    print("=" * 78)
    print(f"U1 — {protokol.upper()} / ETX KAHINI ORANI  (`06` §4.3 · tam olcek)")
    print("=" * 78)
    if pencere:
        print("  ⚠️ DUMAN KESITI — KISA PENCERE. Bastigi oran KAPININ")
        print("     orani DEGILDIR; yalniz aletin kostugunu gosterir.")
    ornek = Konfig(kol="u1", senaryo=kollar[0], tohum=tohumlar[0],
                   **dict(pencere or {}))
    print(f"  N = {ornek.dugum_sayisi} · pencere "
          f"({ornek.isinma_s:.0f}; {ornek.olcum_bitis_s:.0f}) s · "
          f"kosu {ornek.kosu_bitis_s:.0f} s")
    print(f"  kollar: {list(kollar)}")
    print(f"  tohumlar: {list(tohumlar)}  (GELISTIRME — ana deney tohumu YOK)")
    print(f"  🔒 OLCUT: statik oran >= {U1_ESIK_STATIK:.2f} · "
          f"hareketli oran >= {U1_ESIK_HAREKETLI:.2f}")
    print()

    sabit = tuple(sorted((pencere or {}).items()))
    gorevler = [(kol, t, kahin, sabit, protokol)
                for kol in kollar for t in tohumlar for kahin in (False, True)]
    # 🔒 Havuza UZUN işler ÖNCE verilir: hareketli kollar, protokol kâhinden
    # önce. Yalnız süreyi etkiler, sonucu değil — kayıt ve hüküm aşağıda
    # yine kanonik sırayla kurulur. Ölçülmüş gerekçe (`AODV-e` kaydının iş
    # süreleri, K-145): kanonik sırada statik işler başta biter ve sonda
    # uzun hareketli işler tek başına kalır; 8 işçide çekişmesiz tahmin
    # 2,58 → 2,14 sa (alt sınır 1,91).
    sira = sorted(gorevler, key=lambda g: (g[0].startswith("statik"), g[2]))
    t0 = time.perf_counter()
    with Pool(isci) as havuz:
        ham = dict(zip(sira, havuz.map(_is, sira, chunksize=1)))
    sonuc = {g[:4]: ham[g] for g in gorevler}
    if not pencere:
        _kaydet(sonuc, protokol)
    return _degerlendir(sonuc, kollar, tohumlar, sabit,
                        time.perf_counter() - t0, len(gorevler), protokol)


# ==========================================================================
# U3 · YÜK PROFİLİ — ölçüm, KAPI DEĞİL (`06` §4.3 · K-142 · K-143 · K-144)
# ==========================================================================
# 🔒 Aynı küçük dünyada 60 s ve 120 s koşulur; kontrol çerçevesi oranı
# yükün süreyle nasıl büyüdüğünü söyler: ~2 sabit hız (periyodik yük),
# belirgin biçimde 2'nin altı başta yığılan yük (keşif susar).
# ⚠️ Küçük test dünyası `tests2/test_kosum.py::_konfig` — ikinci bir tanım
# yazılmaz; `kontrol_duzlemi_kapilari.py` ile aynı gelenek.
U3_SURELERI_S: tuple[float, ...] = (60.0, 120.0)


def _u3_is(gorev):
    protokol, bitis = gorev
    from test_kosum import _konfig
    kur = kurulum_yap(_konfig("statik-yok", 1000, bitis))
    kosu = Kosu(kur, PROTOKOLLER[protokol])
    kosu.kostur()
    satir = sonuc_satiri(kur, kosu.dugumler, "u3")
    bicim = satir["teshis"]["kontrol_duzlemi"]["bicim"]["tum"]
    teshis: dict[str, float] = {}
    for d in satir["teshis"]["dugum"]:
        for k, v in d.items():
            if isinstance(v, (int, float)):
                teshis[k] = teshis.get(k, 0) + v
    return (protokol, bitis, {n: v["cerceve"] for n, v in bicim.items()},
            satir["metrikler"]["pdr"], teshis)


def u3() -> int:
    """Taban protokollerin yük profilini yan yana basar. Çıkış 0 — bir ÖLÇÜMDÜR."""
    print("=" * 78)
    print("U3 — KONTROL YUKU SUREYLE NASIL BUYUYOR  (kucuk dunya, statik-yok)")
    print("=" * 78)
    gorevler = [(p, b) for p in PROTOKOLLER for b in U3_SURELERI_S]
    with Pool(len(gorevler)) as havuz:
        sonuc = havuz.map(_u3_is, gorevler, chunksize=1)
    tablo = {(p, b): (c, pdr, t) for p, b, c, pdr, t in sonuc}
    kisa, uzun = U3_SURELERI_S
    for p in PROTOKOLLER:
        for b in U3_SURELERI_S:
            c, pdr, t = tablo[(p, b)]
            ek = (f"  kesif {t.get('kesif_basarili', 0):.0f} · "
                  f"rerr_onculsuz {t.get('rerr_onculsuz', 0):.0f}"
                  if p in ("aodv", "aomdv") else "")
            print(f"  {p:<5}{b:>6.0f} s  pdr {pdr:.4f}  {c}{ek}")
        oran = (sum(tablo[(p, uzun)][0].values())
                / sum(tablo[(p, kisa)][0].values()))
        print(f"  → {p} oran ({uzun:.0f}/{kisa:.0f} s): {oran:.3f}")
        print()
    return 0


def _kaydet(sonuc: dict, protokol: str) -> None:
    """Ölçülen hücreleri diske yazar — `<protokol>_son.json` ve damgalı kopya."""
    DIZIN.mkdir(parents=True, exist_ok=True)
    satirlar = [{"kol": kol, "tohum": t, "kahin": kahin,
                 "olcum": olcum, "hata": hata}
                for (kol, t, kahin, _s), (olcum, hata) in sonuc.items()]
    metin = json.dumps({"kaynak": "tam kosum", "protokol": protokol,
                        "hucreler": satirlar}, ensure_ascii=False, indent=1)
    damga = time.strftime("%Y%m%d_%H%M%S", time.gmtime())
    (DIZIN / f"{protokol}_{damga}.json").write_text(metin, encoding="utf-8")
    (DIZIN / f"{protokol}_son.json").write_text(metin, encoding="utf-8")


def hukum(yol: Path | None = None, protokol: str = "aodv") -> int:
    """Kayıtlı bir ölçüme BUGÜNKÜ hüküm kodunu uygular. Çıkış kodu = verdikt.

    🔒 Ölçmez, yalnız değerlendirir. Açıklanmış hücre listesi ya da eşikler
    değiştiğinde verdikti yeniden üretmenin yolu budur. Kaydın KAYNAĞI
    başlıkta basılır: tam koşumun kendi kaydı mı, yoksa yazdırılmış bir
    tablodan mı kuruldu.
    """
    yol = yol or DIZIN / f"{protokol}_son.json"
    veri = json.loads(Path(yol).read_text(encoding="utf-8"))
    # Kayıt kendi protokolünü söyler; eski kayıtlar (alan yok) AODV'dir.
    protokol = veri.get("protokol", "aodv")
    print("=" * 78)
    print("U1 — HUKUM KIPI  (olcmez, kayitli olcume bugunku kodu uygular)")
    print("=" * 78)
    print(f"  kayit  : {yol}")
    print(f"  protokol: {protokol}")
    print(f"  kaynak : {veri.get('kaynak')}")
    sonuc = {}
    kollar: list[str] = []
    tohumlar: list[int] = []
    for h in veri["hucreler"]:
        sonuc[(h["kol"], h["tohum"], h["kahin"], ())] = (h["olcum"], h["hata"])
        if h["kol"] not in kollar:
            kollar.append(h["kol"])
        if h["tohum"] not in tohumlar:
            tohumlar.append(h["tohum"])
    print(f"  🔒 OLCUT: statik oran >= {U1_ESIK_STATIK:.2f} · "
          f"hareketli oran >= {U1_ESIK_HAREKETLI:.2f}")
    print()
    return _degerlendir(sonuc, tuple(kollar), tuple(tohumlar), (),
                        0.0, len(sonuc), protokol)


def _degerlendir(sonuc: dict, kollar, tohumlar, sabit, sure_s: float,
                 n_gorev: int, protokol: str = "aodv") -> int:
    """🔒 Hükmün TEK gerçeklemesi — tam koşum da `hukum` kipi de buradan geçer."""
    aciklanmis = ACIKLANMIS_DUSUK[protokol]
    print(f"  {'kol':<16}{'tohum':>6}{protokol.upper():>9}{'ETX kahin':>11}"
          f"{'oran':>8}{'esik':>7}{'karar':>18}")
    uygunluk = True            # U1-U — kalirsa protokol KABUL EDILMEZ
    basarim_temiz = True       # U1-B — aciklanmamis dusuk ya da olu kayit
    olculen_dusuk: set = set()
    kol_oranlari: dict[str, list[float]] = {}
    for kol in kollar:
        esik = (U1_ESIK_STATIK if kol.startswith("statik-")
                else U1_ESIK_HAREKETLI)
        for t in tohumlar:
            a, a_hata = sonuc[(kol, t, False, sabit)]
            k, k_hata = sonuc[(kol, t, True, sabit)]
            if a_hata is not None or k_hata is not None:
                print(f"  {kol:<16}{t:>6}  🔴 HATA: {a_hata or k_hata}")
                uygunluk = False
                continue
            # 🔒 BOS GECMEYE KAPALI: korunum defteri kapanmadiysa satirin
            # PDR'si bir sayi degil, bir artiktir.
            if not (a["gecerli"] and k["gecerli"]):
                print(f"  {kol:<16}{t:>6}  🔴 KORUNUM KAPANMADI  [U1-U]")
                uygunluk = False
                continue
            if not a["pdr"] or not k["pdr"]:
                print(f"  {kol:<16}{t:>6}  🔴 PDR YOK  [U1-U] "
                      f"({protokol.upper()}={a['pdr']} kahin={k['pdr']})")
                uygunluk = False
                continue
            oran = a["pdr"] / k["pdr"]
            kol_oranlari.setdefault(kol, []).append(oran)
            if oran >= esik:
                karar = "GECTI"
            elif (kol, t) in aciklanmis:
                # 🟡 U1-B · dusuk AMA aciklamasi OLCULMUS ve kayitli.
                karar = "DUSUK (aciklanmis)"
                olculen_dusuk.add((kol, t))
            else:
                # 🔴 Yeni bir dusuk hucre SESSIZCE gecemez.
                karar = "🔴 ACIKLANMAMIS"
                basarim_temiz = False
            print(f"  {kol:<16}{t:>6}{a['pdr']:>9.4f}{k['pdr']:>11.4f}"
                  f"{oran:>8.3f}{esik:>7.2f}{karar:>18}")
    print()
    print(f"  {'kol':<16}{'oran ort':>10}{'en dusuk':>10}")
    for kol, oranlar in kol_oranlari.items():
        print(f"  {kol:<16}{ist.mean(oranlar):>10.3f}{min(oranlar):>10.3f}")
    print()
    # 🔒 TAMPON — `SINANMAMIS` iki parametrenin ölçümü (yukarıdaki beyan).
    print("  ROTA TAMPONU  (kapasite 64 · omur 30 s — ikisi de SINANMAMIS)")
    print(f"  {'kol':<16}{'tohum':>6}{'giris':>9}{'dusen':>8}{'tepe':>7}")
    tepe_en = 0.0
    dusen_top = 0.0
    for kol in kollar:
        for t in tohumlar:
            a, a_hata = sonuc[(kol, t, False, sabit)]
            if a_hata is not None or a is None:
                continue
            tm = a.get("tampon") or {}
            g, d, tp = (tm.get("tampon_giris"), tm.get("tampon_dusen"),
                        tm.get("en_yuksek_tampon"))
            tepe_en = max(tepe_en, tp or 0.0)
            dusen_top += (d or 0.0)
            print(f"  {kol:<16}{t:>6}{(g or 0):>9.0f}{(d or 0):>8.0f}"
                  f"{(tp or 0):>7.0f}")
    print(f"  → en yuksek doluluk {tepe_en:.0f}/64 · "
          f"toplam sure tavanindan dusen {dusen_top:.0f}")
    print()
    print(f"  toplam {n_gorev} kosum · {sure_s:.0f} s")
    print()
    # ⚠️ KAHINI GECMEK DE BIR HATADIR: kahin her seyi bilir. Asiliyorsa
    # kahin bilgisi protokole sizmis demektir ve bu bir KAZANC degil, bir
    # kacaktir. Kapinin ikinci yarisi budur.
    asan = [(kol, o) for kol, oranlar in kol_oranlari.items()
            for o in oranlar if o > 1.0]
    if asan:
        print(f"  🔴 [U1-U] {protokol.upper()} KAHINI GECTI — kahin bilgisi "
              f"sizmis olabilir:")
        for kol, o in asan:
            print(f"     {kol}  oran = {o:.3f}")
        uygunluk = False

    # 🔴 OLU ACIKLAMA TARAMASI — bu kosumda OLCULEN ama artik dusuk OLMAYAN
    # bir kayit. Muafiyet listesi kendi bayatligini gizleyemez (D12 emsali).
    # ⚠️ Bu kosumda hic olculmemis hucre (duman kesiti) olu SAYILMAZ.
    olculen = {(kol, t) for kol in kollar for t in tohumlar}
    olu = sorted((olculen & set(aciklanmis)) - olculen_dusuk)
    if olu:
        print("  🔴 [U1-B] OLU ACIKLAMA — artik dusuk degil, kayit silinmeli:")
        for kol, t in olu:
            print(f"     {kol} / {t}")
        basarim_temiz = False

    print("=" * 78)
    print(f"  U1-U uygunluk : {'GECTI 🟢' if uygunluk else 'KALDI 🔴'}"
          f"   (kalirsa protokol KABUL EDILMEZ)")
    print(f"  U1-B basarim  : {'TEMIZ 🟢' if basarim_temiz else 'KALDI 🔴'}"
          f"   (aciklanmamis dusuk / olu aciklama yok mu)")
    if olculen_dusuk:
        print(f"  🟡 aciklanmis dusuk hucre: {len(olculen_dusuk)} — "
              f"BULGU olarak raporlanir, kusur DEGIL")
    print("=" * 78)
    return 0 if (uygunluk and basarim_temiz) else 1


if __name__ == "__main__":
    # 🔒 Windows `spawn` korumasi — Pool bu blok disinda acilmaz.
    arg = sys.argv[1:]
    protokol = "aodv"
    if "--protokol" in arg:
        i = arg.index("--protokol")
        protokol = arg[i + 1]
        del arg[i:i + 2]
    if protokol not in PROTOKOLLER:
        raise SystemExit(f"bilinmeyen protokol: {protokol} — {sorted(PROTOKOLLER)}")
    if arg and arg[0] == "u3":
        raise SystemExit(u3())
    if arg and arg[0] == "hukum":
        raise SystemExit(hukum(Path(arg[1]) if len(arg) > 1 else None,
                               protokol))
    if "duman" in arg:
        # ⚠️ UCUZ KESIT — SAYIYI URETMEZ, yalniz aletin kostugunu gosterir.
        raise SystemExit(u1(DUMAN_KOLLARI, DUMAN_TOHUMLARI, isci=4,
                            pencere=DUMAN_PENCERESI, protokol=protokol))
    raise SystemExit(u1(protokol=protokol))
