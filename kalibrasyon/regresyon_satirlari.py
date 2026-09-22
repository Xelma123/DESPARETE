"""
REGRESYON SATIRLARI — bir `sim2` değişikliği ölçülmüş sonuçları değiştirdi mi?

Üretici:
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/regresyon_satirlari.py uret <etiket>
    PYTHONIOENCODING=utf-8 python -u kalibrasyon/regresyon_satirlari.py karsilastir <a> <b> [--izin onek,onek] [--yeni onek,onek]

Bağlam: `v2/07-SIMULATOR-TASARIMI.md` §18 Y0 · K-114.

🔴 NEDEN BU ALET VAR
====================
K-112 kontrol düzlemini eklerken 35 sonuç satırını "önce/sonra" alan alan
karşılaştırdı ve birebir aynı buldu — ama karşılaştırma betiği geçici bir
dizinde kaldı, depoya girmedi. Yani "35/35 birebir" iddiası bugün yeniden
üretilemiyor. Bu alet onun depodaki hâlidir ve Aşama 1'deki her `sim2`
değişikliğinden önce ve sonra koşar.

🔒 NE YAPAR
===========
  · `uret <etiket>` — sabit bir vaka matrisini koşar ve her koşunun TAM
    sonuç satırını `ciktilar2/regresyon/<etiket>.jsonl`e yazar (satır başına
    `fsync`). Dosya zaten varsa DURUR: satırlar üst üste eklenirse çoğalır.
  · `karsilastir <a> <b>` — satırları vaka kimliğiyle (`not_`) eşler, bütün
    bölümleri alan alan karşılaştırır ve farkları üç sınıfa ayırır:
        her koşuda değişen   → çalışma kimliği, zaman damgası
        kaynak koduna bağlı  → araç özeti ve onu içeren koşu kimliği
        BULGU                → geri kalan her fark
    `--izin` ile önceden ilan edilmiş, BİLEREK değişen alan önekleri verilir
    (ör. tanımı değişen `metrikler.psr`). İzinli fark ayrı basılır, gizlenmez.
    `--yeni` ile matrise BİLEREK eklenmiş vakaların kimlik önekleri verilir;
    yalnız sonraki dosyada bulunmaları bulgu sayılmaz ama ayrı basılırlar.

🔒 VAKA MATRİSİ — hangi yolu neden sınıyor
===========================================
  · 3 statik kol × en yakın kimlik, kısa pencere — çok atlama, döngü, TTL
  · 12 hareketli kol × doğrudan komşu, kısa — bağımsız ve görev kollarının
    bütün karıştırıcı kolları (süre gerekçesi `vakalar()` içinde)
  · formasyon × 2, kısa — tek atlama ve kâhin grafiği (Y6; kimliği `h-` ile
    başlar, çapraz çarpıma girmez — gerekçe `vakalar()` içinde)
  · tehdit aileleri × 5, kısa — cephe hattı · derin sızma · hedef koruma ·
    hava eşlik (Y5b; kimliği aile adıyla biter, hava eşlik ayrıca kâhinle)
  · 6 karıştırıcı × doğrudan komşu, kısa — tek atlama, kuyruk taşması,
    hedef yok dalı
  · 3 mobilite kolu × iki kâhin, kısa — kâhin grafiği yolu
  · yüklü beacon × 2, kısa — beacon yükünün kanalda ödenmesi (K-111)
  · kontrol düzlemi sınav protokolü × 2, kısa — K-112 mekanizmasının her yolu
  · yere toplama × 2, kısa — geçit, telemetri ve komut akışları, kayıp yeri
    (Y4; kimliği `-yere_toplama` ile biter)
  · 4 tam uzunluk — evre metrikleri, ham bölüm, tam pencere. Süreye göre
    seçildi: statik kolda ETX kâhini, hareketli kollarda doğrudan komşu
    (ölçülen süreler ve gerekçe `vakalar()` içinde)

Vaka başına duvar saati basılır ama satıra yazılmaz; sonraki koşumun bandı
bu sayılardan verilir.

⚠️ SINIR: bu bir KAPI değil, bir karşılaştırma aletidir. "Birebir aynı"
yalnız bu matrisin yolları için geçerlidir; matrisin dokunmadığı bir yol
değişmiş olabilir. Yeni bir mekanizma eklendiğinde matrise vakası da eklenir.
"""

from __future__ import annotations

import json
import sys
import time
from multiprocessing import Pool
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent
for _yol in (KOK, KOK / "tests2"):
    if str(_yol) not in sys.path:
        sys.path.insert(0, str(_yol))

from sim2.kosum.kosu import Kosu  # noqa: E402
from sim2.kosum.kurulum import kurulum_yap  # noqa: E402
from sim2.kosum.sonuc import SatirYazici, sonuc_satiri  # noqa: E402
from sim2.yapilandirma.konfig import Konfig  # noqa: E402
from sim2.yapilandirma.senaryolar import (KARISTIRICI_SINIFLARI,  # noqa: E402
                                          MOBILITE_KOLLARI, SENARYOLAR,
                                          TEHDIT_SENARYOLARI)

DIZIN = KOK / "ciktilar2" / "regresyon"

# Her koşuda değişmesi GEREKEN alanlar — fark değil, tanım.
HER_KOSUDA_DEGISEN = ("kimlik.calisma_kimligi", "kimlik.zaman_damgasi_utc")
# Kaynak kodunun özetine bağlı alanlar — kod değişince değişmeleri GEREKİR.
KOD_KIMLIGI = ("kimlik.arac_hash", "kimlik.kosu_kimligi")

# 🔴 ÜÇÜNCÜ BİR SINIF VAR AMA OTOMATİK DEĞİL — 15 Eylül 2026'da öğrenildi.
# `teshis.koken_kovalari.*` her satırda taşınır ve KÖKEN DEFTERİ her
# değiştiğinde 44 vakada birden oynar. O gün beklenen farklar ilan edilirken
# *"köken metin eklemeleri yalnız `arac_hash`e girer"* denmişti — YANLIŞ; ve
# karşılaştırma beyanı aştı (K-127).
#
# 🔒 BU SINIF BİLEREK OTOMATİK DEĞİL. Otomatik izin verilseydi bir
# parametrenin sessizce TEDAVI'den DUYARSIZ'a kayması da görünmez olurdu —
# oysa görünmesi gereken tam olarak odur. Doğru kullanım: taban alındığından
# beri köken defteri değiştiyse, farkı ilan ederken HANGİ kayıtların
# değiştiği tek tek yazılır ve `--izin teshis.koken_kovalari` ile geçilir.


# ==========================================================================
def vakalar() -> tuple[tuple[str, str, str, int, bool], ...]:
    """(vaka kimliği, senaryo, protokol, tohum, tam uzunluk mu)."""
    cikti: list[tuple[str, str, str, int, bool]] = []
    # 🔒 DÖNGÜ/TTL YALNIZ ÜÇ STATİK KOLDA — 11 Eylül 2026, ölçüldü.
    # İlk üretimde 18 senaryonun hepsi `en_yakin_kimlik`le koştu ve üretim
    # 32,4 dk sürdü. Bu vakalar toplam sürenin %65'iydi; en uzunu
    # `a-bagimsiz-reaktif` 1330 s (10 işçi 8 fiziksel çekirdekte, süreç başına
    # ~2,1 kat yavaş). Döngü ve TTL dalları mobilite × karıştırıcıdan
    # bağımsızdır. Mobilite × karıştırıcı kolları tek atlamalı `m-`
    # vakalarında, hareketli kolda çok atlama `c-` kâhin vakalarında sınanır.
    for s in ("statik-yok", "statik-surekli", "statik-surekli_darbeli"):
        cikti.append((f"a-{s}-en_yakin_kimlik", s, "en_yakin_kimlik", 1000,
                      False))
    # 🔒 FORMASYON KOLU ÇAPRAZ ÇARPIMA GİRMEZ — 11 Eylül 2026 (Y6).
    # Kol yalnız mobilite yolunu değiştirir; mobilite × karıştırıcı ve kâhin
    # grafiği etkileşimi öteki hareketli kollarda sınanıyor. Tam çarpım 8 vaka
    # (~1 900 işlemci-saniye) ekler ve üretimin üst bandını 30 dk'nın üstüne
    # taşırdı. Kolun kendi yolu aşağıdaki iki `h-` vakasıyla sınanır.
    carpimda = tuple(m for m in MOBILITE_KOLLARI if m != "formasyon")
    for s in sorted(SENARYOLAR):
        if (not s.startswith("statik-")
                and SENARYOLAR[s].mobilite_kolu in carpimda):
            cikti.append((f"m-{s}-dogrudan_komsu", s, "dogrudan_komsu", 1000,
                          False))
    for j in KARISTIRICI_SINIFLARI:
        s = f"statik-{j}"
        cikti.append((f"b-{s}-dogrudan_komsu", s, "dogrudan_komsu", 1001,
                      False))
    for m in carpimda:
        s = f"{m}-surekli"
        for k in ("en_guvenilir_kahin", "en_kisa_yol_kahin"):
            cikti.append((f"c-{s}-{k}", s, k, 1002, False))
    # Y6 · formasyon: tek atlama ve kâhin grafiği; karıştırıcılı ve kısa.
    for k in ("dogrudan_komsu", "en_guvenilir_kahin"):
        cikti.append((f"h-formasyon-surekli-{k}", "formasyon-surekli", k,
                      1006, False))
    # Y5b · tehdit aileleri: statik kolda tek atlama, kısa; hava eşlik kâhinle
    # de (hareketli karıştırıcıda kâhin tazelemesi). Kimliği aile adıyla biter.
    for aile in TEHDIT_SENARYOLARI:
        if aile != "tekli_merkez":
            cikti.append((f"i-statik-surekli-dogrudan_komsu-{aile}",
                          "statik-surekli", "dogrudan_komsu", 1007, False))
    cikti.append(("i-statik-surekli-en_guvenilir_kahin-hava_eslik",
                  "statik-surekli", "en_guvenilir_kahin", 1007, False))
    for s in ("statik-surekli", "bagimsiz-surekli"):
        cikti.append((f"d-{s}-yuklu", s, "yuklu", 1003, False))
        cikti.append((f"e-{s}-kontrol_sinav", s, "kontrol_sinav", 1004, False))
    # 🔒 TAM UZUNLUK VAKALARI SÜREYE GÖRE SEÇİLDİ — 11 Eylül 2026, ölçüldü.
    # Kısa pencerede koşu süresi; tam uzunluk (350 s) bunun en çok ~7 katı:
    #   protokol            statik-surekli  bagimsiz-surekli  gorev-surekli_darbeli
    #   en_yakin_kimlik          117,7 s         378,6 s            175,2 s
    #   en_guvenilir_kahin        ~53 s          ~170 s                —
    #   dogrudan_komsu            11,7 s          76,1 s             64,4 s
    # Döngü üreten `en_yakin_kimlik` tam uzunlukta hareketli kolda ~44 dk
    # sürerdi; ilk düzeltme onu ölçmeden seçmişti (K-114 §2.4). Tam uzunluğun
    # sınadığı şey (evre metrikleri, ham bölüm, tam pencere) protokolden
    # bağımsızdır. Çok atlama ve kâhin grafiği tam uzunlukta ucuz olan statik
    # kolda, hareketli kollarda ise kısa vakalarda sınanır.
    cikti.append(("f-statik-yok-dogrudan_komsu-tam", "statik-yok",
                  "dogrudan_komsu", 1000, True))
    cikti.append(("f-statik-surekli-en_guvenilir_kahin-tam", "statik-surekli",
                  "en_guvenilir_kahin", 1000, True))
    cikti.append(("f-bagimsiz-surekli-dogrudan_komsu-tam",
                  "bagimsiz-surekli", "dogrudan_komsu", 1001, True))
    cikti.append(("f-gorev-surekli_darbeli-dogrudan_komsu-tam",
                  "gorev-surekli_darbeli", "dogrudan_komsu", 1002, True))
    # Y4 · yere toplama (`v2/07` §18 Y4). Kimliği `-yere_toplama` ile biten
    # vaka bu desenle koşar (`_kos`). Çok atlama geçide kâhinle statik kolda,
    # hareketli kolda tek atlama; ikisi de karıştırıcılı ve kısa.
    cikti.append(("g-statik-surekli-en_guvenilir_kahin-yere_toplama",
                  "statik-surekli", "en_guvenilir_kahin", 1005, False))
    cikti.append(("g-bagimsiz-surekli-dogrudan_komsu-yere_toplama",
                  "bagimsiz-surekli", "dogrudan_komsu", 1005, False))
    return tuple(cikti)


def _fabrika(protokol: str, kur):
    """Protokol fabrikası — İŞÇİDE kurulur, havuzdan geçmez."""
    if protokol == "dogrudan_komsu":
        from protokoller.kosum_kosumu import DogrudanKomsu
        return lambda i: DogrudanKomsu()
    if protokol == "en_yakin_kimlik":
        from protokoller.kosum_kosumu import EnYakinKimlik
        return lambda i: EnYakinKimlik()
    if protokol in ("en_guvenilir_kahin", "en_kisa_yol_kahin"):
        from kalibrasyon.kahin import (EnGuvenilirKahin, EnKisaYolKahin,
                                       KanalGrafigi)
        grafik = KanalGrafigi(kur)
        tip = (EnGuvenilirKahin if protokol == "en_guvenilir_kahin"
               else EnKisaYolKahin)
        return lambda i: tip(i, grafik)
    if protokol == "yuklu":
        from test_kosum import _YukluProtokol
        return lambda i: _YukluProtokol()
    if protokol == "kontrol_sinav":
        from test_kontrol_duzlemi import SinavProtokolu, yeni_kayit
        kayit = yeni_kayit()
        return lambda i: SinavProtokolu(i, kayit)
    raise ValueError(f"bilinmeyen protokol: {protokol!r}")


def _kos(vaka: tuple[str, str, str, int, bool]) -> dict:
    kimlik, senaryo, protokol, tohum, tam = vaka
    pencere = {} if tam else dict(karistirici_baslangic_s=5.0, isinma_s=10.0,
                                  olcum_bitis_s=40.0, kosu_bitis_s=50.0)
    # Y4: kimliği `-yere_toplama` ile biten vaka o desenle koşar.
    desen = ({"trafik_deseni": "yere_toplama"}
             if kimlik.endswith("-yere_toplama") else {})
    # Y5b: kimliği bir tehdit ailesinin adıyla biten vaka o aileyle koşar.
    tehdit = next(({"tehdit_senaryosu": a} for a in TEHDIT_SENARYOLARI
                   if a != "tekli_merkez" and kimlik.endswith(f"-{a}")), {})
    kfg = Konfig(kol="regresyon", senaryo=senaryo, tohum=tohum, not_=kimlik,
                 **pencere, **desen, **tehdit)
    kur = kurulum_yap(kfg)
    kosu = Kosu(kur, _fabrika(protokol, kur))
    kosu.kostur()
    return sonuc_satiri(kur, kosu.dugumler, protokol)


def _is(vaka):
    """Havuz işçisi. 🔒 Modül düzeyinde — Windows `spawn`.

    Duvar saati satıra YAZILMAZ (her koşuda değişir, karşılaştırmayı bozardı);
    yalnız basılır ki sonraki koşumun bandı ölçümden gelsin.
    """
    t0 = time.perf_counter()
    try:
        return vaka, _kos(vaka), None, time.perf_counter() - t0
    except Exception as hata:                       # noqa: BLE001
        return (vaka, None, f"{type(hata).__name__}: {hata}",
                time.perf_counter() - t0)


# ==========================================================================
def uret(etiket: str, isci: int) -> int:
    yol = DIZIN / f"{etiket}.jsonl"
    if yol.exists():
        print(f"  🔴 {yol} zaten var — üstüne yazılmaz, satırlar çoğalırdı. "
              f"Başka bir etiket seçin.")
        return 1
    liste = vakalar()
    print(f"REGRESYON SATIRLARI — {len(liste)} vaka → {yol}")
    t0 = time.perf_counter()
    hatalar = 0
    en_uzun = (0.0, "")
    with SatirYazici(yol) as yazici, Pool(isci) as havuz:
        for i, (vaka, satir, hata, sure) in enumerate(
                havuz.imap_unordered(_is, liste, chunksize=1), start=1):
            en_uzun = max(en_uzun, (sure, vaka[0]))
            if hata is not None:
                hatalar += 1
                print(f"  🔴 {vaka[0]}: {hata}")
                continue
            yazici.yaz(satir)
            print(f"  {i:>3}/{len(liste)} {vaka[0]:<52} "
                  f"gecerli={satir['korunum']['gecerli']} · {sure:.0f} s",
                  flush=True)
    print(f"  sure: {(time.perf_counter() - t0) / 60.0:.1f} dk · en uzun vaka: "
          f"{en_uzun[1]} {en_uzun[0]:.0f} s · hata: {hatalar}")
    return 1 if hatalar else 0


def _duzlestir(nesne, onek: str = "") -> dict[str, object]:
    """İç içe sözlüğü noktalı yollara açar. Listeler DEĞER olarak kalır."""
    cikti: dict[str, object] = {}
    if isinstance(nesne, dict):
        for anahtar, deger in nesne.items():
            yol = f"{onek}.{anahtar}" if onek else str(anahtar)
            cikti.update(_duzlestir(deger, yol))
    else:
        cikti[onek] = nesne
    return cikti


def _oku(etiket: str) -> dict[str, dict]:
    yol = DIZIN / f"{etiket}.jsonl"
    satirlar: dict[str, dict] = {}
    with open(yol, encoding="utf-8") as dosya:
        for no, metin in enumerate(dosya, start=1):
            satir = json.loads(metin)
            kimlik = satir["kimlik"]["not_"]
            if kimlik in satirlar:
                raise ValueError(f"{yol}:{no} vaka iki kez yazılmış: {kimlik}")
            satirlar[kimlik] = satir
    return satirlar


def karsilastir(a: str, b: str, izin: tuple[str, ...],
                yeni: tuple[str, ...] = ()) -> int:
    sa, sb = _oku(a), _oku(b)
    print(f"REGRESYON KARSILASTIRMASI — {a} ({len(sa)} satir) ↔ "
          f"{b} ({len(sb)} satir)")
    # 🔒 `--yeni` önekindeki vaka YALNIZ SONRAKİ dosyada olabilir: matrise
    # bilerek eklenmiştir ve karşılaştıracağı satır yoktur. Ayrı basılır,
    # gizlenmez; geçersizse bulgudur. Önceki dosyada olup sonrakinde olmayan
    # vaka her zaman bulgudur.
    eksik: list[str] = []
    for kimlik in sorted(set(sa) ^ set(sb)):
        if kimlik in sb and any(kimlik.startswith(o) for o in yeni):
            gecerli = sb[kimlik]["korunum"]["gecerli"]
            print(f"  (yeni vaka) yalniz {b}: {kimlik} · gecerli={gecerli}")
            if gecerli:
                continue
        eksik.append(kimlik)
        print(f"  🔴 yalniz bir dosyada ya da gecersiz: {kimlik}")
    birebir = 0
    bulgu: dict[str, list[str]] = {}
    izinli: dict[str, list[str]] = {}
    beklenen: dict[str, int] = {}
    for kimlik in sorted(set(sa) & set(sb)):
        da, db = _duzlestir(sa[kimlik]), _duzlestir(sb[kimlik])
        vaka_bulgu = False
        for alan in sorted(set(da) | set(db)):
            if da.get(alan, "<yok>") == db.get(alan, "<yok>"):
                continue
            if alan in HER_KOSUDA_DEGISEN or alan in KOD_KIMLIGI:
                beklenen[alan] = beklenen.get(alan, 0) + 1
                continue
            # Yıldızsız önek yalnız TAM bir yol bölümüyle eşleşir
            # (`metrikler.psr`, `metrikler.psr_pencere`yi kapsamaz); `*` ile
            # biten önek düz metin önekidir (`metrikler.kontrol_*`).
            if any(alan.startswith(o[:-1]) if o.endswith("*")
                   else (alan == o or alan.startswith(o + "."))
                   for o in izin):
                izinli.setdefault(alan, []).append(kimlik)
                continue
            bulgu.setdefault(alan, []).append(kimlik)
            vaka_bulgu = True
        birebir += 0 if vaka_bulgu else 1
    print()
    print(f"  bulgusuz vaka : {birebir}/{len(set(sa) & set(sb))}")
    for alan, n in sorted(beklenen.items()):
        print(f"  (beklenen) {alan:<48} {n} vakada farkli")
    for alan, vakalar_ in sorted(izinli.items()):
        print(f"  (izinli)   {alan:<48} {len(vakalar_)} vakada farkli")
    for alan, vakalar_ in sorted(bulgu.items()):
        print(f"  🔴 BULGU   {alan:<48} {len(vakalar_)} vakada farkli "
              f"· ilk: {vakalar_[0]}")
    temiz = not bulgu and not eksik
    print()
    print(f"  {'🟢 BIREBIR (izinli farklar disinda)' if temiz else '🔴 FARK VAR'}")
    return 0 if temiz else 1


if __name__ == "__main__":
    # 🔒 Windows `spawn` korumasi — Pool bu blok disinda acilmaz.
    arguman = sys.argv[1:]
    if len(arguman) >= 2 and arguman[0] == "uret":
        # 🔒 Varsayılan 8 işçi — `03` §1: *"ağır koşumda makine kullanılabilir
        # kalır"* (17 Eylül: 4 işçi · 21 Eylül öğrenci: 8 çekirdek). Önceden
        # 10'a SABİTTİ ve kural yazıldıktan sonra da öyle kaldı; kapanış
        # paketi hazırlanırken görüldü. Başka sayı isteyen `--isci N` verir.
        isci = 8
        if "--isci" in arguman:
            isci = int(arguman[arguman.index("--isci") + 1])
        raise SystemExit(uret(arguman[1], isci=isci))
    if len(arguman) >= 3 and arguman[0] == "karsilastir":
        def _onekler(bayrak: str) -> tuple[str, ...]:
            if bayrak not in arguman:
                return ()
            return tuple(o for o in arguman[arguman.index(bayrak) + 1]
                         .split(",") if o)
        raise SystemExit(karsilastir(arguman[1], arguman[2],
                                     _onekler("--izin"), _onekler("--yeni")))
    print(__doc__)
    raise SystemExit(2)
