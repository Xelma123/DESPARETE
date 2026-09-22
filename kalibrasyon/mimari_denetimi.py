"""BÜTÜNCÜL MİMARİ DENETİMİ — `sim2/` MODELİ ve `kalibrasyon/` ALETLERİ.

Üretici:  PYTHONIOENCODING=utf-8 python kalibrasyon/mimari_denetimi.py

Testlerin yakalamadığı YAPISAL şeyleri denetler. Testler davranışı ölçer;
bu betik mimariyi ölçer. Hiçbir kontrol metin eşleşmesiyle yapılmaz — hepsi
AST üzerinden, çünkü metin arayan bir denetim kendi yorumuna takılır.
"""
from __future__ import annotations

import ast
import dataclasses
import pathlib
import sys

KOK = pathlib.Path(__file__).resolve().parent.parent
if str(KOK) not in sys.path:
    sys.path.insert(0, str(KOK))
# Konfig alan taramasi testten ithal edilir (asagida, d5).
if str(KOK / "tests2") not in sys.path:
    sys.path.insert(0, str(KOK / "tests2"))

SIM2 = KOK / "sim2"

# 🔒 Katman sırası — tek yönlü. Bir katman YALNIZ kendinden ÖNCEKİLERİ
# içe aktarabilir. Yön kırılırsa döngüsel bağımlılık ve "kim kimi bilir"
# belirsizliği doğar; kâhin sızıntılarının yarısı bu belirsizlikten çıkar.
KATMANLAR = ("cekirdek", "yapilandirma", "dunya", "kanal", "mac", "ag",
             "gozlem", "olcum", "kosum")

bulgular: list[str] = []
notlar: list[str] = []


def dosyalar():
    for yol in sorted(SIM2.rglob("*.py")):
        if "__pycache__" not in yol.parts:
            yield yol


def katman(yol: pathlib.Path) -> str | None:
    p = yol.relative_to(SIM2).parts
    return p[0] if len(p) > 1 else None


def basliklar(baslik: str) -> None:
    print()
    print("=" * 74)
    print(baslik)
    print("=" * 74)


# ==========================================================================
def d1_katman_yonu() -> None:
    basliklar("1 - KATMAN YONU  (cekirdek -> yapilandirma -> dunya -> ...)")
    sira = {ad: i for i, ad in enumerate(KATMANLAR)}
    ihlal = 0
    for yol in dosyalar():
        k = katman(yol)
        if k is None or k not in sira:
            continue
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        for n in ast.walk(agac):
            if isinstance(n, ast.ImportFrom) and n.module \
                    and n.module.startswith("sim2."):
                hedef = n.module.split(".")[1]
                if hedef in sira and sira[hedef] > sira[k]:
                    bulgular.append(
                        f"katman yonu: {yol.relative_to(KOK).as_posix()}:"
                        f"{n.lineno} {k} -> {hedef}")
                    ihlal += 1
    print(f"  denetlenen dosya : {sum(1 for _ in dosyalar())}")
    print(f"  ihlal            : {ihlal}")


def d2_ciplak_assert() -> None:
    basliklar("2 - CIPLAK `assert`  (-O altinda sessizce kalkar)")
    say = 0
    for yol in dosyalar():
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        for n in ast.walk(agac):
            if isinstance(n, ast.Assert):
                bulgular.append(
                    f"ciplak assert: {yol.relative_to(KOK).as_posix()}:{n.lineno}")
                say += 1
    print(f"  bulunan : {say}")


def d3_hash_kullanimi() -> None:
    basliklar("3 - BELIRLENIMSIZ KAYNAKLAR  (hash() · time · random · id)")
    yasak = {"hash", "id"}
    yasak_modul = {"time", "datetime", "uuid", "os"}
    say = 0
    for yol in dosyalar():
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        for n in ast.walk(agac):
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) \
                    and n.func.id in yasak:
                bulgular.append(
                    f"belirlenimsiz: {yol.relative_to(KOK).as_posix()}:"
                    f"{n.lineno} {n.func.id}()")
                say += 1
            if isinstance(n, (ast.Import, ast.ImportFrom)):
                adlar = ([a.name.split(".")[0] for a in n.names]
                         if isinstance(n, ast.Import)
                         else [(n.module or "").split(".")[0]])
                for a in adlar:
                    if a in yasak_modul:
                        notlar.append(
                            f"{yol.relative_to(KOK).as_posix()}:{n.lineno} "
                            f"import {a}  (kimlik/zaman damgasi disinda "
                            f"kullanilmamali)")
    print(f"  hash()/id() cagrisi : {say}")
    print(f"  zaman/ortam iceri aktarimi : {len(notlar)}")
    for s in notlar:
        print(f"    . {s}")


def d4_olu_kod() -> None:
    """🔴 BU KAPI 29 CANLI ADI 'OLU' DIYE NOT DUSUYORDU — 9 Eylul 2026.

    Eski esik `kullanim <= 2` idi ve yanindaki yorum sunu iddia ediyordu:
    *"tanim + `__all__` girisi = 2; ustu kullanimdir."* **Ikisi de yanlis:**

      · `__all__` girisi bir `ast.Constant` (dizgi) — sayaca HIC girmiyor.
      · `def`/`class` adi `FunctionDef`/`ClassDef` — `ast.Name` DEGIL,
        o da girmiyor.
      · Yalnizca modul duzeyindeki ATAMALAR (sabitler) Store baglaminda
        bir `ast.Name` uretiyor, yani 1 sayiliyor.

    Sonuc: esik cagrilabilirler icin ~2, sabitler icin ~1 fazlaydi ve kapi
    her kosumda **30 ad** bildiriyordu. Olculdu (9 Eylul 2026): bunlarin
    **yalnizca 1'i** gercekten hic okunmuyor; `karistirici_kur`,
    `veri_gonder`, `kapsam_bolumu`, `fiziksel_kopma_say` gibi 29 ad
    fiilen CAGRILIYOR.

    🔒 K-109'un kurali: *dogru calisan isi kirmiziya boyayan bir kapi,
    kapisizliktan KOTUDUR* — insanlari notlari atlamaya alistirir. Bu kapi
    denetimin 41 notunun 29'unu tek basina uretiyordu.

    DUZELTME iki parcali:
      1. Yalniz **LOAD** baglamindaki okumalar sayilir; esik `== 0`.
      2. Kapsam `kalibrasyon/` ve `protokoller/`u de icerir — yalniz bir
         olcum aleti tarafindan kullanilan bir ad OLU DEGILDIR.
         (Tek ornegi cikti: `kokenler.duyarlilik_borcu`.)

    ⚠️ GENISLEMENIN KOR NOKTASI ARANDI VE BULUNAMADI: kapsami genisletmek,
    TERK EDILMIS bir betigin (`adim3_oncesi.py`) tek basina bir adi 'canli'
    gostermesine yol acabilirdi. Olculdu (9 Eylul 2026): tarihsel betik
    kapsamdan cikarildiginda HICBIR ad olulesmiyor — yani boyle bir ad yok.
    """
    basliklar("4 - OLU KOD  (`__all__`da olup HIC OKUNMAYAN ad)")
    kullanim: dict[str, int] = {}
    kokler = [SIM2, KOK / "tests2", KOK / "kalibrasyon", KOK / "protokoller"]
    for kok in kokler:
        for yol in sorted(kok.rglob("*.py")):
            if "__pycache__" in yol.parts:
                continue
            agac = ast.parse(yol.read_text(encoding="utf-8"))
            for n in ast.walk(agac):
                # 🔒 Yalniz OKUMA sayilir. Tanim (Store) bir kullanim degildir.
                if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Load):
                    kullanim[n.id] = kullanim.get(n.id, 0) + 1
                elif (isinstance(n, ast.Attribute)
                      and isinstance(n.ctx, ast.Load)):
                    kullanim[n.attr] = kullanim.get(n.attr, 0) + 1
                elif isinstance(n, ast.alias):
                    kullanim[n.name] = kullanim.get(n.name, 0) + 1

    olu: list[str] = []
    for yol in dosyalar():
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        for n in agac.body:
            if not (isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == "__all__"
                            for t in n.targets)):
                continue
            if not isinstance(n.value, (ast.List, ast.Tuple)):
                continue
            for e in n.value.elts:
                if isinstance(e, ast.Constant) and isinstance(e.value, str):
                    # 🔒 Esik SIFIR: bir kez bile OKUNMUSSA olu degildir.
                    if kullanim.get(e.value, 0) == 0:
                        olu.append(f"{yol.relative_to(KOK).as_posix()} "
                                   f"-> {e.value}")
    print(f"  taranan agac             : sim2 · tests2 · kalibrasyon · protokoller")
    print(f"  hic OKUNMAYAN dis ad     : {len(olu)}")
    for s in olu:
        print(f"    . {s}")
    if olu:
        notlar.extend(olu)


def d5_konfig_alanlari() -> None:
    basliklar("5 - KONFIG ALANLARI  (bildirim != kullanim)")
    # 🔴 TARAMA TESTTEN ITHAL EDILIYOR. Ilk yazimda burada AYRI bir (ve ada
    # bakan, kaba) gerceklemesi vardi; test keskinlestirilince ikisi
    # AYRISTI ve denetim `kuyruk_kapasitesi`ni yanlis okudu. Iki gerceklemeli
    # bir kontrol, tam da bu projenin kacindigi seydir.
    from sim2.yapilandirma.konfig import HENUZ_OKUNMAYAN, Konfig
    from test_yapilandirma import _okunan_alanlar
    alanlar = {f.name for f in dataclasses.fields(Konfig)}
    okunan = _okunan_alanlar()
    fiilen = sorted(alanlar & okunan)
    sahipsiz = sorted(alanlar - okunan - HENUZ_OKUNMAYAN)
    print(f"  toplam alan          : {len(alanlar)}")
    print(f"  fiilen okunan        : {len(fiilen)}")
    print(f"  HENUZ_OKUNMAYAN'da   : {len(HENUZ_OKUNMAYAN)}")
    print(f"  sahipsiz (HATA)      : {len(sahipsiz)}  {sahipsiz}")
    print(f"  okunanlar: {', '.join(fiilen)}")
    if sahipsiz:
        bulgular.append(f"sahipsiz Konfig alani: {sahipsiz}")


def d6_rng_akislari() -> None:
    basliklar("6 - RNG AKISLARI  (bildirilen vs cekim alan)")
    from sim2.cekirdek.rng import (AKIS_ADLARI, HASH_ALANLARI,
                                   HENUZ_KULLANILMAYAN)
    kullanilan: set[str] = set()
    for yol in dosyalar():
        if yol.name == "rng.py":
            continue
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        for n in ast.walk(agac):
            if isinstance(n, ast.Constant) and isinstance(n.value, str):
                if n.value in AKIS_ADLARI or n.value in HASH_ALANLARI:
                    kullanilan.add(n.value)
    bos = sorted(set(AKIS_ADLARI) - kullanilan - set(HENUZ_KULLANILMAYAN))
    print(f"  sirali akis        : {len(AKIS_ADLARI)}")
    print(f"  hash alani         : {len(HASH_ALANLARI)}")
    print(f"  cekim alan akis    : {sorted(kullanilan & set(AKIS_ADLARI))}")
    print(f"  HENUZ_KULLANILMAYAN: {list(HENUZ_KULLANILMAYAN)}")
    print(f"  bildirilmemis bos akis : {len(bos)}  {bos}")
    if bos:
        notlar.append(
            f"su akislar hicbir modulde cekim almiyor ve HENUZ_KULLANILMAYAN'da "
            f"da yazmiyorlar: {bos}  (Adim 4-11'de dolacaklar; simdilik BEKLENEN)")


def d7_kahin_sizintisi() -> None:
    basliklar("7 - KAHIN YUZEYLERI  (kimin neyi gorebildigi)")
    kahin_moduller = ("dunya.topoloji", "dunya.yerlesim", "olcum", "gozlem")
    print("  Kontrol edilen: kahin yuzeylerinin ne oldugu BEYAN EDILMIS mi.")
    for m in kahin_moduller:
        yol = SIM2 / (m.replace(".", "/") + ".py")
        dizin = SIM2 / m.replace(".", "/")
        if dizin.is_dir():
            parcalar = [y.read_text(encoding="utf-8")
                        for y in sorted(dizin.rglob("*.py"))
                        if "__pycache__" not in y.parts]
            metin = "\n".join(parcalar)
        elif yol.exists():
            metin = yol.read_text(encoding="utf-8")
        else:
            print(f"    . {m:22s} HENUZ YOK")
            continue
        beyan = "KÂHİN" in metin or "kâhin" in metin or "KAHIN" in metin
        print(f"    . {m:22s} beyan {'VAR' if beyan else '🔴 YOK'}")
        if not beyan:
            bulgular.append(f"kahin beyani yok: {m}")


def d8_sayisal_saglik() -> None:
    basliklar("8 - SAYISAL SAGLIK  (turetilenler tutarli mi)")
    from sim2.yapilandirma.konfig import Konfig
    k = Konfig(kol="denetim")
    kontroller = [
        ("girisim orani > 1 (gizli terminal mumkun)",
         k.girisim_orani > 1.0),
        ("girisim menzili > iletim menzili",
         k.girisim_menzili_m > k.iletim_menzili_m),
        ("DIFS > SIFS", k.difs_s > k.sifs_s),
        ("olcum penceresi kosu icinde",
         k.olcum_penceresi[1] <= k.kosu_bitis_s),
        ("tepe telafisi: d=1 -> 0 dB",
         abs(dataclasses.replace(k, darbe_gorev_cevrimi=1.0).tepe_telafisi_db)
         < 1e-12),
        ("tepe telafisi: d=0,5 -> 3,0103 dB",
         abs(k.tepe_telafisi_db - 3.0103) < 1e-3),
        ("karistirici gucu None (olculmedi)",
         k.karistirici_guc_dbm is None),
        ("irtifa bandi pozitif genislik",
         k.irtifa_maks_m > k.irtifa_min_m),
        ("sunulan yuk = akis x hiz",
         abs(k.sunulan_paket_hizi_hz - 40.0) < 1e-12),
        # 🔴 KOSULLU ATALETIN KAPISI — 9 Eylul 2026, K-110.
        # `cw_max` koken defterinde `TURETILMIS`: yeniden deneme siniri
        # verildiginde ERISILEMEZ oldugu icin. Cekisme penceresi her
        # basarisizlikta 2c+1 oluyor, yani `limit` katlanmadan sonra en cok
        # 2^limit·(cw_min+1) − 1 olabiliyor. Bugun 2^4·32 − 1 = 511 < 1023.
        # 🔒 Sinir yukselirse `cw_max` CANLI hale gelir ve o koken kaydi
        # SESSIZCE yanlislasir. Bu satir onu sessiz birakmiyor.
        (f"cw_max erisilemez (en cok CW = "
         f"{2 ** k.yeniden_deneme_siniri * (k.cw_min + 1) - 1} < {k.cw_max})",
         2 ** k.yeniden_deneme_siniri * (k.cw_min + 1) - 1 < k.cw_max),
    ]
    for ad, sonuc in kontroller:
        print(f"    {'OK ' if sonuc else '🔴 '} {ad}")
        if not sonuc:
            bulgular.append(f"sayisal saglik: {ad}")


def d9_belirlenimcilik() -> None:
    basliklar("9 - BELIRLENIMCILIK  (ayni tohum -> ayni dunya)")
    from sim2.cekirdek.rng import Akislar
    from sim2.dunya.topoloji import topoloji_kur
    from sim2.yapilandirma.konfig import Konfig
    for senaryo in ("statik-yok", "bagimsiz-yok", "gorev-yok",
                    "formasyon-yok"):
        a = topoloji_kur(Konfig(kol="d", senaryo=senaryo, tohum=7), Akislar(7))
        b = topoloji_kur(Konfig(kol="d", senaryo=senaryo, tohum=7), Akislar(7))
        ayni = all(a.anlik(t).konumlar == b.anlik(t).konumlar
                   for t in (0.0, 111.1, 350.0))
        print(f"    {'OK ' if ayni else '🔴 '} {senaryo}")
        if not ayni:
            bulgular.append(f"belirlenimcilik: {senaryo}")
    # farkli tohum farkli dunya
    a = topoloji_kur(Konfig(kol="d", senaryo="bagimsiz-yok", tohum=7), Akislar(7))
    b = topoloji_kur(Konfig(kol="d", senaryo="bagimsiz-yok", tohum=8), Akislar(8))
    print(f"    {'OK ' if a.anlik(0.0).konumlar != b.anlik(0.0).konumlar else '🔴 '}"
          f" farkli tohum -> farkli dunya")


def d10_sabit_konum_bagimsizligi() -> None:
    basliklar("10 - MOBILITE KOLU YERLESIMI DEGISTIRMIYOR")
    from sim2.cekirdek.rng import Akislar
    from sim2.dunya.topoloji import topoloji_kur
    from sim2.yapilandirma.konfig import Konfig
    # 🔴 Mobilite bir EKSEN. Iki kolun t=0 yerlesimi AYNI olmali, yoksa
    # olculen fark hareketin degil yerlesimin farki olur.
    ayni = True
    for tohum in range(1, 11):
        s = topoloji_kur(Konfig(kol="d", senaryo="statik-yok", tohum=tohum),
                         Akislar(tohum)).anlik(0.0).konumlar
        m = topoloji_kur(Konfig(kol="d", senaryo="bagimsiz-yok", tohum=tohum),
                         Akislar(tohum)).anlik(0.0).konumlar
        f = topoloji_kur(Konfig(kol="d", senaryo="formasyon-yok", tohum=tohum),
                         Akislar(tohum)).anlik(0.0).konumlar
        ayni = ayni and s == m == f
    print(f"    {'OK ' if ayni else '🔴 '} statik, bagimsiz ve formasyon kolu "
          f"AYNI t=0 yerlesiminden basliyor (10 tohum)")
    print("    NOT: gorev kolu paylasamaz — 'mufrezede' ile 'duzgun")
    print("         rastgele' farkli dagilimlardir. Kollari")
    print("         karsilastirilabilir yapan sey yerlesimin ayniligi degil,")
    print("         YOGUNLUGUN esitligidir (derece olcutle esitlendi).")
    if not ayni:
        bulgular.append("mobilite kolu t=0 yerlesimini degistiriyor — "
                        "eksenin iki ucu karsilastirilamaz")


def _skaler_sayi_mi(dugum: ast.expr) -> bool:
    """Tek bir SAYI mı — işaretlisi dâhil.

    🔴 `-15.0` AST'de bir `Constant` DEĞİLDİR: `UnaryOp(USub, Constant(15.0))`.
    Yalnız `Constant` arayan bir tarayıcı bütün negatif sabitleri kaçırır ve
    bu SESSİZ bir kaçıştır — kaçan sabit köken defterine hiç girmez, yani
    "gerekçesiz parametre depoya giremez" kuralı onun için hiç işlemez.
    """
    if isinstance(dugum, ast.UnaryOp) and isinstance(dugum.op,
                                                     (ast.USub, ast.UAdd)):
        dugum = dugum.operand
    return (isinstance(dugum, ast.Constant)
            and isinstance(dugum.value, (int, float))
            and not isinstance(dugum.value, bool))


def _sayi_tablosu_mu(dugum: ast.expr) -> bool:
    """Sabit bir SAYI TABLOSU mu — dict/list/tuple/set, içinde en az bir sayı?

    🔒 Bir güç tablosu, tek bir güç kadar davranış belirleyicidir. Ayrımı
    "kaç sayı içerdiği" yapmaz; kökeni yazılmalıdır.
    """
    if not isinstance(dugum, (ast.Dict, ast.List, ast.Tuple, ast.Set)):
        return False
    return any(isinstance(a, ast.Constant) and isinstance(a.value, (int, float))
               and not isinstance(a.value, bool)
               for a in ast.walk(dugum))


def d12_parametre_kokenleri() -> None:
    """🔴 HER DAVRANIŞ BELİRLEYEN SAYININ KÖKENİ YAZILI MI?

    8 Eylul 2026'da olculdu: davranis belirleyen parametrelerin cogunun
    DEGERI gerekcesizdi. Yorumlar "bu parametre neden VAR" sorusunu
    cevapliyordu, "neden BU DEGER" sorusunu degil. O gunun butun kusurlari
    bu bosluktan cikti.

    🔒 `Konfig` alanlari icin kapsama `konfig.py`de ICE AKTARMA aninda
    denetlenir — eksik alan varsa modul hic yuklenmez. Bu kapi MODUL DUZEYI
    sabitleri denetler ve kova dagilimini raporlar.

    ⚠️ `SINANMAMIS` bir BULGU DEGILDIR, bir BORCTUR: beyan edilmis ve
    sayilmistir. Bulgu olan sey, kovasi HIC YAZILMAMIS bir sabittir.

        🔒 On-kayit muhurlenmeden once SINANMAMIS sayisi SIFIR olmalidir.
    """
    basliklar("D12 - PARAMETRE KOKENLERI  (her sayi bir kovada mi)")
    import re
    from sim2.yapilandirma.kokenler import (KOKENLER, KOVALAR, MODUL_KOKENLERI,
                                            duyarlilik_borcu, kova_sayimi)

    sayisal = re.compile(r"^[-\d.eE_ ()*/+<]+$")
    bulunan: list[str] = []
    for yol in dosyalar():
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        for n in agac.body:
            hedef = None
            if isinstance(n, ast.AnnAssign) and isinstance(n.target, ast.Name):
                hedef = n.target.id
            elif (isinstance(n, ast.Assign) and len(n.targets) == 1
                  and isinstance(n.targets[0], ast.Name)):
                hedef = n.targets[0].id
            if not hedef or not hedef.isupper() or hedef.startswith("_"):
                continue
            try:
                deger = ast.unparse(n.value)
            except Exception:            # noqa: BLE001
                continue
            # 🔴 KÖR NOKTA KAPATILDI — 8 Eylül 2026. Önce yalnız SKALER
            # sabitler taranıyordu; sayı TABLOLARI (dict/list/tuple/set)
            # köken defterinden tamamen kaçıyordu. `KARISTIRICI_GUCU_DBM`
            # bunu ortaya çıkardı: tehdit modelinin en davranış belirleyici
            # sabiti hiç görülmüyordu, ve kaydını yazınca "ölü kayıt" sayıldı.
            if not (sayisal.match(deger) or _sayi_tablosu_mu(n.value)):
                continue
            bulunan.append(f"{yol.relative_to(KOK).as_posix()}::{hedef}")

    # 🔴 DEFTER ARTIK İKİ AĞACI KAPSIYOR — canlılık kontrolü de kapsamalı.
    # 9 Eylül 2026: `kalibrasyon/` sabitleri deftere eklenince D12 onların
    # 27'sini birden "ölü kayıt" ilan etti, çünkü yalnız `sim2/` tarıyordu.
    # Bir denetimin kendi kapsamı, denetlediği defterin kapsamından dar
    # olamaz — yoksa doğru kaydı kusur diye işaretler.
    # 🔒 MUAFIYET TEK KAYNAKTAN: `TARIHSEL_FIZIK` beyanli moduller D14'un
    # yonetiminde. Ayni kurali iki kapida ayri ayri yazmak, ikisinin
    # ayrismasi demekti — nitekim ilk yazimda ayristilar ve D12, D13'un muaf
    # tuttugu 14 sabiti "kokeni yazilmamis" ilan etti.
    _tarihsel = _tarihsel_moduller()
    for yol, ad, _ in _kalibrasyon_sabitleri():
        if yol.name in _tarihsel:
            continue
        bulunan.append(f"kalibrasyon/{yol.name}::{ad}")

    kayitli = set(MODUL_KOKENLERI)
    eksik = sorted(set(bulunan) - kayitli)
    olu = sorted(kayitli - set(bulunan))
    for ad in eksik:
        if ad.startswith("kalibrasyon/"):
            continue          # D13'un isi; iki yerde iki kez raporlanmasin
        bulgular.append(f"{ad} KOKENI YAZILMAMIS — "
                        f"sim2/yapilandirma/kokenler.py'ye eklenmeli")
    for ad in olu:
        bulgular.append(f"{ad} icin koken kaydi var ama SABIT YOK — "
                        f"olu kayit, defterin guvenilirligini bitirir")

    print(f"  taranan modul sabiti : {len(bulunan)}")
    print(f"  kokeni yazilmamis    : {len(eksik)}")
    print(f"  olu koken kaydi      : {len(olu)}")
    sayim = kova_sayimi()
    toplam = sum(sayim.values())
    print(f"\n  KOVA DAGILIMI ({toplam} parametre — Konfig + modul sabitleri)")
    for kova in KOVALAR:
        n = sayim[kova]
        isaret = "🔴" if kova == "SINANMAMIS" and n else "  "
        print(f"    {isaret} {kova:<12} {n:>3}  ({100 * n / toplam:.0f}%)")
    if sayim["SINANMAMIS"]:
        notlar.append(f"{sayim['SINANMAMIS']} parametre SINANMAMIS kovasinda "
                      f"— on-kayit muhurlenmeden once sifirlanmali")

    # 🔴 IKINCI SAYAC — `SINANMAMIS`in kardesi. `KOL_TANIMI` kovasi hic
    # bosalmaz (bir kolun tanimi silinmez), ama DUYARLILIK BORCU bosalir.
    # Borcu duzyaziya birakmak, 8 Eylul 2026'da olcumsuz bir borc dususu
    # uretmisti (50 -> 46); artik sayiliyor.
    borc = duyarlilik_borcu()
    print()
    print(f"  DUYARLILIK BORCU ({len(borc)} kol tanimi sabiti "
          f"acik)")
    for ad in borc:
        print(f"    🔴 {ad}")
    if borc:
        notlar.append(f"{len(borc)} kol tanimi sabitinin duyarlilik "
                      f"borcu ACIK — on-kayit muhurlenmeden once bosalmali")

    # 🔴 ÜÇÜNCÜ SAYAÇ — `DUYARSIZ` AKLAMASI SAYIYI TAŞIYOR MU? (16 Eylul 2026)
    #
    # `DUYARSIZ` kovasinin tanimi *"olcumle hak edilir"*. Hak edildigini
    # gosteren sey olculen |Δ|dir; tasimayan bir kayit defterden yeniden
    # DENETLENEMEZ. Bu sayi uc belgede (`DEVIR` §1 · `v2/12` §3 C7 · bu
    # dosyanin basligi) duzyaziyla yaziliydi ve UCU DE YANLISTI: "15'in
    # 7'sinde var" deniyordu, olculdu — 15'in 15'inde var. Duzyaziya birakilan
    # her sayi bir gun bayatlar; artik her kosumda sayiliyor.
    # `|Δ| = 0,0nn` ya da `|D| = 0,0nn` — defterde iki yazim da var (bazi
    # kayitlar ASCII'ye dusuruldu). Ikisi de KABUL EDILIR; aranan sey bir
    # SAYININ varligidir, harfin degil.
    delta = re.compile(r"\|\s*[ΔD]\s*\|\s*=\s*\d+[,.]\d+")
    kayitlar = [(ad, ger) for ad, (kova, ger) in KOKENLER.items()
                if kova == "DUYARSIZ"]
    modul_duyarsiz = [ad for ad, (kova, _g) in MODUL_KOKENLERI.items()
                      if kova == "DUYARSIZ"]
    sayisiz = [ad for ad, ger in kayitlar if not delta.search(ger)]
    print()
    print(f"  `DUYARSIZ` AKLAMALARI — olculen |Δ| yazili mi")
    print(f"    Konfig kaydi        : {len(kayitlar)}")
    print(f"    olculen |Δ| tasiyan : {len(kayitlar) - len(sayisiz)}/"
          f"{len(kayitlar)}")
    print(f"    modul sabiti (ayri) : {len(modul_duyarsiz)} — "
          f"{', '.join(modul_duyarsiz) if modul_duyarsiz else 'yok'}")
    for ad in sayisiz:
        print(f"    🔴 {ad} — aklamayi veren sayi YAZILI DEGIL")
    if sayisiz:
        notlar.append(f"{len(sayisiz)} `DUYARSIZ` kaydi olculen |Δ| "
                      f"tasimiyor — defterden denetlenemez")


def d11_ice_aktarilabilirlik() -> None:
    """🔴 HER MODUL ICE AKTARILABILIYOR MU?

    5 Eylul 2026'da toplu bir metin degisimi (`_tavan` -> `_sinir`) istemeden
    `pdr_tavani` modul adini da `pdr_siniri` yapti; icinde `_tavan` gecen bir
    ad oldugu icin. Betik "5 degisim" yazdi, AST dogrulamasi yuvalari ve
    rapor anahtarlarini kontrol etti ve GECTI — cunku kirilan sey bir ICE
    AKTARIMDI. Test paketi de yakalamadi: o dosya testlerden cagrilmiyor.

    🔒 Bu kapi ucuzdur ve o hata sinifinin tamamini kapatir. `kalibrasyon/`
    ve `protokoller/` altindaki hicbir sey testlerden cagrilmadigi icin,
    oradaki bir sozdizimi ya da ad hatasi bugune kadar SESSIZ kalirdi.

    ⚠️ Modul duzeyinde kod calistiran bir dosya varsa bu kapi onu da
    calistirir; o yuzden her betik `if __name__ == "__main__":` ile
    korunmalidir. Korunmuyorsa burasi yavaslar ve bu bir bulgudur.
    """
    basliklar("D11 - ICE AKTARILABILIRLIK  (her modul import edilebiliyor mu)")
    import importlib
    paketler = ("sim2", "tests2", "kalibrasyon", "protokoller")
    sayi = kirik = 0
    for paket in paketler:
        kok = KOK / paket
        if not kok.exists():
            continue
        for yol in sorted(kok.rglob("*.py")):
            if "__pycache__" in yol.parts:
                continue
            ad = ".".join(yol.relative_to(KOK).with_suffix("").parts)
            sayi += 1
            try:
                importlib.import_module(ad)
            except Exception as hata:  # noqa: BLE001 - hepsi bulgudur
                kirik += 1
                bulgular.append(f"{ad} ICE AKTARILAMIYOR -> "
                                f"{type(hata).__name__}: {str(hata)[:70]}")
    print(f"  taranan modul    : {sayi}")
    print(f"  ice aktarilamayan: {kirik}")


# ==========================================================================
KALIBRASYON = KOK / "kalibrasyon"


def _tarihsel_moduller() -> set[str]:
    """`TARIHSEL_FIZIK` beyan eden kalibrasyon modulleri."""
    cikti = set()
    for yol in sorted(KALIBRASYON.glob("*.py")):
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        if any(isinstance(d, (ast.Assign, ast.AnnAssign))
               and any(isinstance(t, ast.Name) and t.id == "TARIHSEL_FIZIK"
                       for t in ([d.target] if isinstance(d, ast.AnnAssign)
                                 else d.targets))
               for d in agac.body):
            cikti.add(yol.name)
    return cikti


def _kalibrasyon_sabitleri():
    """`kalibrasyon/` altındaki modül düzeyi SAYISAL sabitler.

    🔒 D12 ile aynı tarama, farklı dizin. Ayrı yazılmasının sebebi kapsam:
    D12 `sim2/`nin MODELİNİ denetler, bu kapı ÖLÇÜM ALETLERİNİ.
    """
    for yol in sorted(KALIBRASYON.glob("*.py")):
        if "__pycache__" in yol.parts:
            continue
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        for dugum in agac.body:
            if isinstance(dugum, ast.AnnAssign):
                hedefler, deger = [dugum.target], dugum.value
            elif isinstance(dugum, ast.Assign):
                hedefler, deger = dugum.targets, dugum.value
            else:
                continue
            if deger is None:
                continue
            # 🔴 KURAL İKİ YERDE YAZILMIŞTI VE YİNE AYRIŞTI — 9 Eylül 2026.
            # Burada tablo denetimi `deger.elts`e DOĞRUDAN bakıyordu; D12'nin
            # `_sayi_tablosu_mu`su ise `ast.walk` ile İNİYOR. Fark NEGATİF
            # sayılarda ortaya çıktı: `-15.0` AST'de bir `Constant` değil,
            # `UnaryOp(USub, Constant)`tır. Yani yalnız negatif sayılardan
            # oluşan bir tablo (`GUCLER = (-30.0, …)`) bu kapıdan SESSİZCE
            # kaçıyordu — ve ancak köken kaydı YAZILDIĞINDA "ölü kayıt" diye
            # görünür oldu. Kayıt yazılmasaydı hiç fark edilmeyecekti.
            #
            # 🔒 Aynı hata bu dosyada İKİNCİ KEZ: muafiyet kuralı da iki
            # kapıda ayrı yazılmış ve ayrışmıştı. Kural artık TEK KAYNAKTAN.
            tablo = _sayi_tablosu_mu(deger)
            skaler = _skaler_sayi_mi(deger)
            if not (skaler or tablo):
                continue
            for hedef in hedefler:
                if isinstance(hedef, ast.Name) and hedef.id.isupper():
                    yield yol, hedef.id, deger


def d13_kalibrasyon_kokenleri() -> None:
    """🔴 ÖLÇÜM ALETLERİNİN SAYILARI DA KÖKENE BAĞLI MI?

    9 Eylül 2026'da ölçüldü ve sebebi buydu: `sim2/` 52 dosya ve 12 kapıyla
    korunuyordu, `kalibrasyon/` 24 dosya ve **tek** kapıyla ("import
    edilebiliyor mu"). O oturumdaki kusurların HEPSİ korumasız yarıdaydı.

    🔴 Ve tarandığında 41 davranış belirleyen sabit çıktı, hiçbiri köken
    defterinde değildi. İçlerinden biri doğrudan çalışma noktasını
    belirliyor: `kahin.py::ATLAMA_ESIGI`. ρ = 0,258, o eşikle tanımlanmış
    bir grafikte ölçüldü — yani sonucu belirleyen bir sayı, hiçbir kovada
    değildi.

    🔒 KURAL AYNI: bir ölçüm aletinin sayısı da nereden geldiğini söylemek
    zorunda. Bir aletin gerekçesiz sabiti, modelin gerekçesiz sabitinden
    daha az tehlikeli değildir — ölçtüğü şeyi o belirliyor.
    """
    from sim2.yapilandirma.kokenler import MODUL_KOKENLERI
    basliklar("D13 - KALIBRASYON KOKENLERI  (olcum aletlerinin sayilari)")

    # 🔒 `TARIHSEL_FIZIK` beyanli modul MUAF — ve sebebi kapsam:
    # oradaki sayilar CANLI bir olcum parametresi degil, terk edilmis bir
    # aday calisma noktasinin DONMUS anlik goruntusudur. Koken defteri
    # "bu sayi bugunku davranisi neden boyle belirliyor" sorusunu cevaplar;
    # donmus bir tarih icin o soru anlamsizdir. Onlari D14 yonetiyor:
    # beyan + her kosumda bayatlik raporu.
    # 🔴 AMA MUAFIYET BEDAVA DEGIL: boyle bir modul CANLI bir uretici olarak
    # gosterilemez — D15 onu denetler.
    tarihsel = _tarihsel_moduller()

    eksik = []
    toplam = muaf = 0
    for yol, ad, _ in _kalibrasyon_sabitleri():
        if yol.name in tarihsel:
            muaf += 1
            continue
        toplam += 1
        anahtar = f"kalibrasyon/{yol.name}::{ad}"
        if anahtar not in MODUL_KOKENLERI:
            eksik.append(anahtar)
    print(f"  taranan sabit      : {toplam}")
    print(f"  tarihsel (muaf)    : {muaf}  ({', '.join(sorted(tarihsel))})")
    print(f"  kokeni yazilmamis  : {len(eksik)}")
    for a in eksik:
        print(f"    🔴 {a}")
    if eksik:
        notlar.append(f"{len(eksik)} kalibrasyon sabiti koken defterinde YOK "
                      f"— olcum aletinin sayisi da gerekce ister")


def d14_golge_fizik() -> None:
    """🔴 KALIBRASYON KENDİ FİZİĞİNİ TAŞIYOR MU? — ikinci doğru kaynağı

    9 Eylül 2026'da bulundu: `adim3_oncesi.py` fizik sabitlerinin KENDİ
    kopyasını taşıyordu ve **dördü ayrışmıştı** — alan 1000 ↔ 1800 m, yol
    kaybı üsteli 3,0 ↔ 2,0, SINR eşiği 10 ↔ 16 dB. Yani ölçek kapısının
    eleyip attığı α = 3 orada hâlâ yaşıyordu.

    🔴 Ve o betik `sim2/` içinde ON YERDE "üretici" olarak gösteriliyordu —
    köken defterinin kendisi dâhil. Bir sayıyı doğrulamak için onu koşturan
    biri BAŞKA bir cevap alır ve nedenini bilemez.

    🔴 AMA BU KAPININ İLK HÂLİ YANLIŞ ALARM VERDİ — ve o da kayda geçer.
    `adim3_oncesi.py` bu durumu ZATEN beyan ediyordu: sabitler "tarihsel"
    diye işaretli ve modül her koşumda `bayatlik_raporu()` basarak hangi
    sabitin güncel `Konfig`den ayrıştığını söylüyor. Yani doğru yapılmış bir
    işi kusur diye işaretledim. Doğru çalışan işi kırmızıya boyayan bir kapı,
    kapısızlıktan KÖTÜDÜR: insanları kapıyı görmezden gelmeye alıştırır.

    🔒 DÜZELTİLMİŞ KURAL — yasak değil, SÖZLEŞME:
        Fiziğin kopyasını tutan bir modül, bunu AÇIKÇA beyan etmek ve her
        koşumda bayatlığını RAPORLAMAK zorundadır.

            TARIHSEL_FIZIK = True          modül düzeyinde beyan
            def bayatlik_raporu(): ...     ve `__main__`den çağrılıyor

    Beyanı olan bir kopya NOT'tur (görünür kalır); beyanı olmayan BULGUDUR.
    Kopyanın kendisi meşru olabilir — tarihsel bir ölçümü yeniden üretmek
    için gerekir — ama sessiz kalması meşru değildir.
    """
    from sim2.yapilandirma.konfig import Konfig
    basliklar("D14 - GOLGE FIZIK  (kalibrasyon kendi sabitini tasiyor mu)")
    kfg = Konfig(kol="denetim")
    alanlar = {f.name for f in dataclasses.fields(Konfig)}

    def _beyanli(yol) -> bool:
        """Modül kopyayı BEYAN edip bayatlığını RAPORLUYOR mu? (AST ile)"""
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        beyan = any(
            isinstance(d, (ast.Assign, ast.AnnAssign))
            and any(isinstance(t, ast.Name) and t.id == "TARIHSEL_FIZIK"
                    for t in ([d.target] if isinstance(d, ast.AnnAssign)
                              else d.targets))
            for d in agac.body)
        raporlu = any(isinstance(d, ast.FunctionDef)
                      and d.name == "bayatlik_raporu" for d in agac.body)
        # Rapor `__main__`den cagriliyor mu — beyan dekoratif olmasin.
        cagrili = any(
            isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
            and n.func.id == "bayatlik_raporu"
            for n in ast.walk(agac))
        return beyan and raporlu and cagrili

    beyanli, sessiz = 0, 0
    for yol, ad, deger in _kalibrasyon_sabitleri():
        alan = ad.lower()
        if alan not in alanlar or not isinstance(deger, ast.Constant):
            continue
        gercek = getattr(kfg, alan)
        anahtar = f"kalibrasyon/{yol.name}::{ad}"
        durum = "AYRISMIS" if deger.value != gercek else "ayni"
        if _beyanli(yol):
            beyanli += 1
            isaret = "⚠️" if durum == "AYRISMIS" else "  "
            if durum == "AYRISMIS":
                notlar.append(f"{anahtar} = {deger.value} ↔ Konfig.{alan} = "
                              f"{gercek} — BEYANLI tarihsel kopya, ayrismis")
            print(f"    {isaret} {anahtar:42s} {deger.value!s:>12} "
                  f"{durum:<9} (beyanli)")
        else:
            sessiz += 1
            bulgular.append(f"{anahtar} = {deger.value} SESSIZ golge fizik "
                            f"(Konfig.{alan} = {gercek}) -> `TARIHSEL_FIZIK` "
                            f"beyani ve `bayatlik_raporu()` sart")
            print(f"    🔴 {anahtar:42s} {deger.value!s:>12} "
                  f"{durum:<9} SESSIZ")
    print(f"  beyanli tarihsel kopya : {beyanli}")
    print(f"  🔴 SESSIZ golge fizik  : {sessiz}")
    if sessiz == 0:
        print("  🟢 Fiziginin kopyasini tutan her modul bunu BEYAN ediyor ve")
        print("     bayatligini her kosumda raporluyor.")


def d15_bayat_uretici() -> None:
    """🔴 TARİHSEL BİR BETİK, CANLI BİR SAYININ ÜRETİCİSİ OLARAK GÖSTERİLEMEZ.

    D13 `TARIHSEL_FIZIK` beyanlı modülleri köken defterinden muaf tutuyor —
    çünkü oradaki sayılar donmuş bir anlık görüntü. Ama muafiyetin bedeli
    var: o modül **terk edilmiş bir çalışma noktasında** hesaplıyor
    (ölçüldü: yol kaybı üsteli 3,0 ↔ 2,0, SINR eşiği 10 ↔ 16 dB).

    🔴 9 Eylül 2026'da bulundu: `adim3_oncesi.py` `sim2/` içinde ON YERDE
    "Üretici" olarak gösteriliyordu — **köken defterinin kendisi dâhil**.
    `golgeleme_sigma_db` `OLCULMUS` kovasındaydı ve üreticisi oydu. Yani
    canlı bir kova iddiası, farklı bir fizikle hesaplayan bir betiğe
    dayanıyordu. Sayıyı doğrulamak için onu koşturan biri BAŞKA bir cevap
    alır ve nedenini bilemez.

    🔒 KURAL: `OLCULMUS` bir kaydın gerekçesi, tarihsel bir modülü üretici
    gösteremez. Modül başlıklarındaki TARİHSEL atıflar meşrudur (geçmişi
    anlatıyorlar) ama NOT olarak görünür kalır.
    """
    from sim2.yapilandirma.kokenler import KOKENLER, MODUL_KOKENLERI
    basliklar("D15 - BAYAT URETICI  (tarihsel betik canli sayiya kaynak mi)")
    tarihsel = _tarihsel_moduller()
    print(f"  tarihsel modul: {', '.join(sorted(tarihsel)) or 'yok'}")
    if not tarihsel:
        print("  🟢 Tarihsel modul yok — kontrol edilecek bir sey de yok.")
        return

    kirik = 0
    for defter, etiket in ((KOKENLER, "Konfig"), (MODUL_KOKENLERI, "modul")):
        for ad, (kova, gerekce) in defter.items():
            if kova != "OLCULMUS":
                continue
            for modul in tarihsel:
                if modul not in gerekce:
                    continue
                # 🔒 BAYAT OLDUĞU YAZILMIŞSA ATIF TARİHSELDİR, BULGU DEĞİL.
                # İlk hâlim salt metin araması yapıyordu ve düzeltilmiş bir
                # kaydı — "ESKİ ÜRETİCİ BAYATTI: …" diye açıkça işaretlenmiş
                # olanı — hâlâ kusur sayıyordu. Bir kapının, düzeltilmiş işi
                # kırmızıya boyaması onu işe yaramaz kılar.
                if "BAYAT" in gerekce.upper():
                    notlar.append(
                        f"{etiket} `{ad}` gerekcesinde `{modul}` geciyor ama "
                        f"BAYAT diye isaretli — tarihsel atif, canli uretici "
                        f"degil")
                    continue
                kirik += 1
                bulgular.append(
                    f"{etiket} `{ad}` OLCULMUS ama uretici `{modul}` "
                    f"TARIHSEL (terk edilmis calisma noktasi) -> ya "
                    f"yeniden olculmeli ya kova dusurulmeli")
                print(f"    🔴 {ad}  (OLCULMUS ← {modul})")
    # Modul basliklarindaki atiflar: NOT, bulgu degil.
    atif = 0
    for yol in dosyalar():
        metin = yol.read_text(encoding="utf-8")
        for modul in tarihsel:
            if modul in metin:
                atif += 1
                break
    print(f"  OLCULMUS kaydinda bayat uretici : {kirik}")
    print(f"  sim2/ icinde tarihsel atif      : {atif} dosya")
    if atif:
        notlar.append(f"{atif} `sim2/` dosyasi tarihsel bir kalibrasyon "
                      f"betigine atif yapiyor — gecmisi anlatiyorlar, ama "
                      f"okuyucu betigin terk edilmis bir calisma noktasinda "
                      f"kostugunu satirdan goremiyor")
    if kirik == 0:
        print("  🟢 Hicbir OLCULMUS kaydi tarihsel bir ureticiye dayanmiyor.")


# ==========================================================================
def d16_tekrarli_tanim() -> None:
    """🔴 BU TARAMA BİR BULGUDAN SONRA YAZILDI — 16 Eylül 2026.

    `sim2/gozlem/yuk.py` iki kez `yuku_dondur` tanımlıyordu; gövdeler birebir
    aynıydı ve ikincisi birincisini sessizce gölgeliyordu. Bugün zararsızdı —
    ama `v2/03` §B5'in kendi hata sınıfı budur: *"aynı kuralı iki yerde
    yazmak; iki kopya bir gün ayrışır."* Ayrışsalardı Python İKİNCİSİNİ
    seçerdi ve dosyayı yukarıdan okuyan biri BİRİNCİSİNİ okurdu.

    🔒 Python bunu bir hata saymaz ve bu depoda linter yok; yani tek yapısal
    panzehir bu taramadır. `sim2` DIŞINA da bakar: aynı kusur bir ölçüm
    aletinde olsaydı sessiz bir yanlış sayı üretirdi ve yanlış sayı
    çalışmayan koddan tehlikelidir (`v2/03` §B5).

    ⚠️ Sınıf gövdeleri ayrı birer ad uzayıdır ve ayrı taranır; iki sınıfın
    aynı adlı metodu taşıması normaldir, BİR sınıfın taşıması değildir.
    """
    basliklar("16 - TEKRARLI TANIM  (ayni ad uzayinda iki def/class)")
    say = 0
    kokler = [k for k in (SIM2, KALIBRASYON, KOK / "tests2",
                          KOK / "protokoller") if k.exists()]
    for kok in kokler:
        for yol in sorted(kok.rglob("*.py")):
            if "__pycache__" in yol.parts:
                continue
            agac = ast.parse(yol.read_text(encoding="utf-8"))
            govdeler = [("", agac.body)]
            govdeler += [(f"{n.name}.", n.body) for n in ast.walk(agac)
                         if isinstance(n, ast.ClassDef)]
            for onek, govde in govdeler:
                gorulen: dict[str, int] = {}
                for n in govde:
                    if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef,
                                          ast.ClassDef)):
                        continue
                    if n.name in gorulen:
                        bulgular.append(
                            f"tekrarli tanim: "
                            f"{yol.relative_to(KOK).as_posix()}:{n.lineno} "
                            f"`{onek}{n.name}` — ilk tanim satir "
                            f"{gorulen[n.name]}, ikincisi onu golgeliyor")
                        say += 1
                    gorulen[n.name] = n.lineno
    print(f"  taranan kok : {len(kokler)}")
    print(f"  bulunan     : {say}")


def main() -> None:
    d1_katman_yonu()
    d2_ciplak_assert()
    d3_hash_kullanimi()
    d4_olu_kod()
    d5_konfig_alanlari()
    d6_rng_akislari()
    d7_kahin_sizintisi()
    d8_sayisal_saglik()
    d9_belirlenimcilik()
    d10_sabit_konum_bagimsizligi()
    d11_ice_aktarilabilirlik()
    d12_parametre_kokenleri()
    d13_kalibrasyon_kokenleri()
    d14_golge_fizik()
    d15_bayat_uretici()
    d16_tekrarli_tanim()

    basliklar("SONUC")
    if bulgular:
        print(f"  🔴 {len(bulgular)} BULGU:")
        for b in bulgular:
            print(f"    . {b}")
    else:
        print("  Yapisal ihlal YOK.")
    if notlar:
        print(f"\n  {len(notlar)} not (hata degil, bilgi):")
        for s in notlar:
            print(f"    . {s}")


if __name__ == "__main__":
    main()
