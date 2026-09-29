"""
🔴 KAPININ BEKLENEN TEST SAYILARI GÜNCEL Mİ — pahalı kapının UCUZ koruması.

NEDEN BU DOSYA VAR
==================
`dogrulama/aile0_kapi_raporu.py` her kapı kriteri için **beklenen test
sayısını** yazılı tutar (K-033'ün kuralı). Bir seçim sessizce daralırsa ya da
o dosyaya yeni test eklenirse, kapı bunu `!!SEÇİM n≠m` ile yakalar ve kriteri
düşürür. **Mekanizma çalışıyor.** Yakalayamadığı şey ZAMAN:

    kapı raporu bir tam koşuda 71 dk sürüyor.

Bu yüzden sayı iki kez sessizce bayatladı ve ikisi de ancak kapı fiilen
koşturulduğunda görüldü:

| ne zaman | ne oldu |
|---|---|
| K-036 | B-01/B-02 regresyonları eklendi, Ç5 beklenen sayısı 11'de kaldı |
| 20 Ağu 2026 | B-27b'nin dört `test_b27b_*` içerik testi eklendi, Ç5 beklenen sayısı 14'te kaldı. **Kapı `!!SEÇİM 18≠14` ile düştü** — 40 bulguluk iki bağımsız denetim boyunca kimse görmedi |

Bu dosya **aynı kontrolü saniyeler içinde** yapar. Y3'ün ("kapı çıktısı bir
TEST'tir, betik değil") ve K-042'nin ("pahalı koşudan önce ucuz ön kontrol")
birleşimi.

⚠️ BU BİR KAPI DEĞİLDİR. Kapının yerine geçmez; yalnızca kapının bu tek
sebepten düşüp düşmeyeceğini önceden söyler.

⏱️ Bedeli ölçüldü: her kontrol bir `pytest --collect-only` alt süreci açar.
"""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path

import pytest

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK))

from dogrulama.aile0_kapi_raporu import (  # noqa: E402
    BEKLENEN_MUTASYON, KAPI_SECIMLERI, TAM_DOSYA_KRITERLERI, KapiSecimi,
    ToplamaHatasi, eksik_zorunlu, toplanan_test_kimlikleri,
    toplanan_test_sayisi,
)

# Kapının beklenen sayı taşıyan BÜTÜN kriterleri. Sözlük kazayla küçülürse
# parametrik test sessizce daralır ve hiçbir şey söylemez — Ç1.3'ün
# `{toplam}/{toplam}` tuzağının (B-32) bu dosyadaki hâli.
# 🆕 Ç1.5 — B-144 (sekizinci denetim): üç üreticinin çapa testi
# (`tests/test_gecerlilik_araclari.py`) kapının HİÇBİR kriterinde
# yoktu; bir `skip` kapıyı düşürmüyordu.
BEKLENEN_KRITERLER = {"Ç1.5", "Ç2", "Ç3", "Ç5", "Ç4.1", "Ç6.2"}


def test_kapi_secimleri_sozlugu_daralmamis():
    """🔴 Y7 — parametrik testin KENDİ girdisi doğrulanır.

    Aşağıdaki parametrik test `KAPI_SECIMLERI`nin üzerinden geçiyor. Sözlük
    boşalsa ya da bir kriter düşse, o test **hiç koşmaz ve hiçbir şey
    söylemez.** "0 hata" ile "0 kontrol" ayrımı burada yapılır.
    """
    assert set(KAPI_SECIMLERI) == BEKLENEN_KRITERLER, (
        f"kapı seçimleri değişmiş: {sorted(set(KAPI_SECIMLERI))}. "
        f"Bir kriter eklendi/çıkarıldıysa BEKLENEN_KRITERLER de güncellenmeli."
    )


@pytest.mark.parametrize("kod", sorted(BEKLENEN_KRITERLER))
def test_kapi_beklenen_test_sayisi_guncel(kod: str):
    """Kapının yazılı beklediği sayı, BUGÜN toplanan sayıya eşit mi?

    Eşit değilse kapı bu kriteri `!!SEÇİM` ile düşürür — ve bunu öğrenmek
    için 71 dakika beklemek gerekmez.
    """
    sec = KAPI_SECIMLERI[kod]
    toplanan = toplanan_test_sayisi(sec.yollar, sec.secim)
    assert toplanan == sec.adet, (
        f"{kod} ({sec.ad}): kapı {sec.adet} test bekliyor, bugün {toplanan} "
        f"toplanıyor.\n"
        f"Üretici: python -m pytest {' '.join(sec.yollar)}"
        f"{f' -k {sec.secim!r}' if sec.secim else ''} --collect-only -q\n"
        f"Test EKLENDİYSE `KAPI_SECIMLERI` güncellenmeli ve gerekçesi "
        f"`04-NEDEN-BOYLE.md`ye yazılmalı. Test KAYBOLDUYSA kapı haklı: "
        f"bir koruma sessizce daralmış."
    )


# ==========================================================================
# SAYACIN KENDİSİ — Y7 ve Y8
# ==========================================================================
# `toplanan_test_sayisi` bu dosyadaki her iddianın altında duruyor. Sabit bir
# sayı döndürseydi ya da hata durumunda sessizce 0 verseydi, yukarıdaki
# testlerin hepsi yanlış sebeple geçerdi.

def test_y7_bos_secim_sifir_donuyor_hata_gizlemiyor():
    """Hiçbir şeye uymayan bir seçim: 0 döner — ve bu 0, bir HATA değildir."""
    assert toplanan_test_sayisi(
        ["tests/test_gozlem.py"], "asla_eslesmeyecek_bir_test_adi_zzz") == 0


def test_y7_var_olmayan_yol_ISTISNA_firlatiyor():
    """🔴 Y7'nin kalbi: "0 test" ile "araç çalışmadı" AYNI ŞEY DEĞİLDİR.

    Bu ayrım yapılmasaydı, yol adı bozulan bir kapı seçimi 0 döndürür ve
    `0 == 0` ile geçerdi. Bu depoda tam olarak bu hata yedi kez yapıldı.
    """
    with pytest.raises(ToplamaHatasi):
        toplanan_test_sayisi(["tests/boyle_bir_dosya_yok_zzz.py"], None)


def test_y11_KISMI_toplama_sessizce_sayi_dondurmuyor(tmp_path):
    """🔴 Y11 — korumanın YAKALAYABİLDİĞİ durumun DIŞINDA bir vaka.

    `test_y7_var_olmayan_yol_ISTISNA_firlatiyor` yalnızca "hiç toplanamadı"
    vakasını sınıyor ve onu iki koruma birden yakalıyor (çıkış kodu **ve**
    ayrıştırma). Yani o test, çıkış kodu kontrolünün bağlayıcı olduğunu
    **göstermiyor** — ölçüldü: kontrolü kaldıran bir mutasyon o testten sağ
    çıkıyor.

    Asıl tehlikeli vaka bu: bir dosya toplanır, bir dosya **import hatası**
    verir. pytest o zaman hem "N tests collected" basar hem sıfırdan farklı
    çıkış kodu döndürür. Ayrıştırma tek başına burada **eksik bir sayı**
    döndürürdü — ve kapı o eksik sayıyı `!!SEÇİM` sanırdı ya da tam tersi,
    daralmış bir seçimi doğru sanırdı.
    """
    (tmp_path / "test_saglam_zzz.py").write_text(
        "def test_bir():\n    assert True\n", encoding="utf-8")
    (tmp_path / "test_bozuk_zzz.py").write_text(
        "import boyle_bir_modul_yok_zzz\n", encoding="utf-8")

    with pytest.raises(ToplamaHatasi):
        toplanan_test_sayisi([str(tmp_path)], None)


def test_y7_beklenmedik_CIKTI_BICIMI_de_istisna_firlatiyor(monkeypatch):
    """rc=0, ama "N tests collected" satırı yok — ileriki bir pytest sürümü.

    🔴 NEDEN BU TEST VAR — ölçüldü, tahmin edilmedi:
    ayrıştırma kontrolünü kaldıran bir mutasyon *(M6)* bu dosyanın diğer
    **on bir** testinin hepsinden sağ çıkıyordu. Sebep: "hiç toplanamadı"
    vakasını çıkış kodu kontrolü zaten yakalıyor, dolayısıyla ayrıştırma
    dalına hiçbir gerçek çağrı ulaşmıyor. Y11'in tam tanımı: **bir koruma,
    yalnızca yakalayabildiği durumla sınanamaz.**

    ⚠️ Burada bir SAHTE HOST kullanılıyor ve `03` B6 bunu uyarıyor:
    *"bir test ikizi, tam da ölçmek istediğin şeyi devre dışı
    bırakabilir."* Meşru olmasının sebebi, ikizin **konusunun** çıktı
    biçiminin kendisi olması — gerçek pytest'i bugün bu biçime sokmanın
    yolu yok.
    """
    import types

    import dogrulama.aile0_kapi_raporu as kr

    class _SahteSonuc:
        returncode = 0
        stdout = "pytest 9.0 — 7 adet test derlendi\n"
        stderr = ""

    monkeypatch.setattr(
        kr, "subprocess", types.SimpleNamespace(run=lambda *a, **k: _SahteSonuc()))

    with pytest.raises(kr.ToplamaHatasi):
        kr.toplanan_test_sayisi(["tests/test_gozlem.py"], None)


def test_y8_sayac_SECIME_duyarli():
    """Sayaç gerçekten seçimi mi okuyor, yoksa dosyayı mı sayıyor?

    Y8'in ruhu: bir ölçütün doğru olduğunu göstermek, onun **değişmesi
    gereken yerde değiştiğini** göstermektir. Aynı dosya, üç farklı seçim.
    """
    tum = toplanan_test_sayisi(["tests/test_kapi_aile0.py"], None)
    c2 = toplanan_test_sayisi(["tests/test_kapi_aile0.py"], "c2_")
    c3 = toplanan_test_sayisi(["tests/test_kapi_aile0.py"], "c3_")
    assert tum > 0 and c2 > 0 and c3 > 0
    assert c2 < tum and c3 < tum, "seçim daraltmıyor — sayaç `-k`yı okumuyor"
    assert c2 != c3, "iki farklı seçim aynı sayıyı veriyor"


# ==========================================================================
# KAYNAK DENETİMİ — grep'tir ve adı bunu söyler (B-09'un dersi)
# ==========================================================================

def test_kaynak_denetimi_kapi_sayilari_main_icinde_gomulu_degil():
    """Beklenen sayılar TEK KAYNAKTA mı, yoksa `main()`e geri sızmış mı?

    ⚠️ Bu bir DEĞİŞMEZ değil, bir **kaynak denetimidir**: `_pytest` çağrısına
    doğrudan dosya listesi geçen bir satır, `KAPI_SECIMLERI`ni atlamış
    demektir ve bu dosya onu koruyamaz.
    """
    kaynak = (KOK / "dogrulama" / "aile0_kapi_raporu.py").read_text(
        encoding="utf-8")
    gomulu = re.findall(r"_pytest\(\s*\[", kaynak)
    assert not gomulu, (
        f"{len(gomulu)} yerde `_pytest([...])` doğrudan çağrılıyor; beklenen "
        f"sayı `KAPI_SECIMLERI` dışında kalmış olabilir."
    )


# ==========================================================================
# B-41 — Ç1.3'ÜN EŞİĞİ
# ==========================================================================

def test_b41_beklenen_mutasyon_sabiti_listeyle_ayni():
    """🔴 Kapının Ç1.3 eşiği, ölçtüğü listenin KENDİSİNDEN türeyemez.

    K-044 bu sabiti *eklediğini yazdı*; sabit koda hiç girmedi ve eşik iki
    oturum boyunca `{toplam}/{toplam}` kaldı (B-41). Üçüncü denetim ölçtü:
    liste 35 -> 5'e düşse kapı **"5/5 · OK · 13/13"** diyordu.

    Bu test, aynı sürüklenmeyi 71 dakika değil **milisaniyeler** içinde
    yakalar. Mutasyon paketi büyüdüğünde `BEKLENEN_MUTASYON` de büyümeli ve
    gerekçesi `04-NEDEN-BOYLE.md`ye yazılmalı.
    """
    from dogrulama.mutasyon_paketi import MUTASYONLAR
    assert len(MUTASYONLAR) == BEKLENEN_MUTASYON, (
        f"mutasyon listesi {len(MUTASYONLAR)}, kapı {BEKLENEN_MUTASYON} "
        f"bekliyor. Mutasyon EKLENDİYSE sabit güncellenmeli; "
        f"KAYBOLDUYSA kapı haklı — bir koruma sessizce daralmış."
    )


# ==========================================================================
# B-42 — KAPSAM: sayı değil, NE ÖLÇÜLDÜĞÜ
# ==========================================================================

def test_b42_zorunlu_kumeleri_BOS_DEGIL():
    """🔴 Y7 — boş bir `zorunlu` kümesi, kapsam kontrolünü `0 == 0` yapar.

    Aşağıdaki parametrik kapsam testi, kümesi boş bir kriter için hiçbir şey
    iddia etmez ve sessizce geçer. Bu depoda tam olarak bu hata yedi kez
    yapıldı; kontrolün kendisi de kontrol edilmeli.
    """
    bos = [k for k, v in KAPI_SECIMLERI.items() if not v.zorunlu]
    assert not bos, f"şu kriterlerin zorunlu kümesi boş: {bos}"


@pytest.mark.parametrize("kod", sorted(KAPI_SECIMLERI))
def test_b42_kapi_kapsami_zorunlu_testleri_iceriyor(kod: str):
    """Kriterin ÖLÇTÜĞÜ küme sessizce daraldı mı?

    🔴 Sayı kontrolü bunu göremez: seçim ve sayı **birlikte** değiştirilirse
    `toplanan == adet` tutmaya devam eder. Üçüncü denetim bunu ölçtü (U10):
    Ç5'i `-k "not test_b27b"` + `adet=14` yapınca 284/284 test, ucuz koruma
    ve kapının kendisi — **üçü de** sustu.
    """
    sec = KAPI_SECIMLERI[kod]
    eksik = eksik_zorunlu(sec)
    assert not eksik, (
        f"{kod} ({sec.ad}): şu zorunlu testler kapsamdan DÜŞMÜŞ: "
        f"{sorted(eksik)}\n"
        f"Üretici: python -m pytest {' '.join(sec.yollar)}"
        f"{f' -k {sec.secim!r}' if sec.secim else ''} --collect-only -q"
    )


def test_b42_tam_dosya_kriterleri_k_secimi_KULLANMIYOR():
    """Dosyasını paylaşmayan bir kriterde `-k`, kapsamı daraltmanın en ucuz yolu.

    Ç5 ve Ç4.1 kendi dosyalarının TAMAMINI ölçer. `-k` eklemek, o dosyaya
    yarın eklenecek bir testi sessizce kapsam dışında bırakır — ve bu, U10'un
    tam olarak yaptığı şeydir.
    """
    for kod in TAM_DOSYA_KRITERLERI:
        sec = KAPI_SECIMLERI[kod]
        assert sec.secim is None, (
            f"{kod} tam dosya kriteri ama `-k {sec.secim!r}` kullanıyor. "
            f"Kapsam daraltılmış olabilir."
        )
        assert len(sec.yollar) == 1, (
            f"{kod} tam dosya kriteri ama {len(sec.yollar)} yol taşıyor."
        )


# ==========================================================================
# Y11 — İKİ EKSENİN BİRBİRİNİ KORUMADIĞI GÖSTERİLİYOR
# ==========================================================================
# 🔴 Y11: bir koruma, yalnızca yakalayabildiği durumla sınanamaz.
# Aşağıdaki iki test, sayı ve kapsam eksenlerinin BAĞIMSIZ olduğunu ve her
# birinin diğerinin kör noktasını kapattığını ÖLÇEREK gösterir. Biri
# olmasaydı diğeri o vakayı geçirirdi.

def test_y11_KAPSAM_daralmasi_sayi_KORUNSA_BILE_yakalaniyor():
    """U10'un birebir yeniden üretimi — depoya dokunmadan.

    Ç5'i kendi içinde TUTARLI biçimde daraltıyoruz: seçim `not test_b27b`,
    adet 18 -> 14. Sayı ekseni **susuyor** (ve bu doğru davranış), kapsam
    ekseni **konuşuyor**.
    """
    gercek = KAPI_SECIMLERI["Ç5"]
    # 🔴 Adet ÖLÇÜLÜR, yazılmaz: saldırgan da böyle yapardı — daralttığı
    # seçimin bugünkü sayısını okuyup satıra yazar, kontrol tutarlı kalır.
    # (İlk yazımda burada sabit 14 vardı; dosyaya beş test eklenince test
    # KENDİ VARSAYIMINI yakaladı — Y5.)
    daralmis_adet = toplanan_test_sayisi(gercek.yollar, "not test_b27b")
    daraltilmis = KapiSecimi(
        gercek.ad, gercek.yollar, "not test_b27b", daralmis_adet,
        gercek.zorunlu)

    # Kurulum gerçekten bir DARALTMA mı?
    assert 0 < daralmis_adet < gercek.adet, (
        f"kurulum varsayımı tutmuyor: {daralmis_adet} vs {gercek.adet}")

    # 1) SAYI ekseni: tutarlı daraltma bu kontrolden SAĞ ÇIKAR.
    assert toplanan_test_sayisi(
        daraltilmis.yollar, daraltilmis.secim) == daraltilmis.adet

    # 2) KAPSAM ekseni: aynı daraltmayı YAKALAR.
    eksik = eksik_zorunlu(daraltilmis)
    assert "test_b27b_" in eksik, (
        f"kapsam kontrolü U10'u yakalamıyor — eksik={sorted(eksik)}")


def test_y11_SAYI_daralmasi_kapsam_KORUNSA_BILE_yakalaniyor():
    """Tersi: kapsam tam, sayı yanlış.

    Ç5'in bütün zorunlu desenlerini koruyan ama fazladan test kaybeden bir
    kurulum. Kapsam ekseni **susuyor** (doğru), sayı ekseni **konuşuyor**.
    Bu olmasaydı, bir dosyadan sessizce kaybolan testler görülmezdi.
    """
    gercek = KAPI_SECIMLERI["Ç5"]
    # 🔴 Seçim, `zorunlu` kümesinin KENDİSİNDEN türetilir — elle yazılan bir
    # `-k` dizgisi, kümeye yeni bir çapa eklendiği gün sessizce bayatlar.
    # (İlk yazımda elle yazılmıştı; iki çapa eklenince test KENDİ VARSAYIMINI
    # yakaladı — Y5, bu dosyada ikinci kez.)
    kirpilmis = KapiSecimi(
        gercek.ad, gercek.yollar,
        " or ".join(sorted(gercek.zorunlu)),
        gercek.adet, gercek.zorunlu)

    # 1) KAPSAM ekseni: bütün zorunlular hâlâ içeride → SUSAR.
    assert not eksik_zorunlu(kirpilmis), "kurulum varsayımı tutmuyor"

    # 2) SAYI ekseni: kaybolan testleri YAKALAR.
    toplanan = toplanan_test_sayisi(kirpilmis.yollar, kirpilmis.secim)
    assert toplanan != kirpilmis.adet, (
        f"sayı kontrolü kırpılmayı yakalamıyor: {toplanan} == {kirpilmis.adet}")


# ==========================================================================
# Y7 — YENİ TOPLAYICININ KENDİSİ
# ==========================================================================

def test_y7_kimlik_toplayici_var_olmayan_yolda_ISTISNA_firlatiyor():
    """`toplanan_test_kimlikleri` sessizce boş liste dönmemeli.

    Dönseydi, `eksik_zorunlu` **bütün** desenleri "eksik" sanır ve kapı
    yanlış sebeple düşerdi — ya da tam tersi bir yeniden yazımda boş liste
    "hiçbir şey eksik değil" diye okunurdu.
    """
    with pytest.raises(ToplamaHatasi):
        toplanan_test_kimlikleri(["tests/boyle_bir_dosya_yok_zzz.py"], None)


def test_y8_kimlik_toplayici_SECIME_duyarli():
    """Toplayıcı gerçekten seçimi okuyor mu — yoksa dosyayı mı listeliyor?"""
    tum = toplanan_test_kimlikleri(["tests/test_kapi_aile0.py"], None)
    c2 = toplanan_test_kimlikleri(["tests/test_kapi_aile0.py"], "c2_")
    assert len(c2) < len(tum), "seçim daraltmıyor — toplayıcı `-k`yı okumuyor"
    assert all("::" in x for x in c2), "kimlikler test kimliği gibi görünmüyor"


# ==========================================================================
# 🔴 B-52 — SAĞ KALAN GİRDİLERİNİN `yol` ALANI
#
# B-36'nın düzeltmesi 7 girdinin yalnızca 2'sini kapsıyordu; kalan 5'i
# `yol=None` ile tetiklenme kontrolünü **tamamen atlıyor** ve yine
# "eşdeğer" damgası alıyordu. `03` B5: "etiketi elle taşımak".
# ==========================================================================

def test_b52_her_sag_kalan_girdisi_YOL_tasiyor():
    """`yol=None` ile kontrolü atlamak artık mümkün olmamalı."""
    from dogrulama.sag_kalan_ayikla import SAG_KALANLAR, YOLSUZ

    assert SAG_KALANLAR, "sağ kalan listesi boş — kontrol dejenere"
    for m in SAG_KALANLAR:
        assert m.yol is not None and m.yol != "", (
            f"{m.ad}: `yol` boş — tetiklenme kontrolü atlanır ve mutasyon "
            f"yanlışlıkla 'eşdeğer' damgası alır (B-36'nın kendi dersi)")
        assert isinstance(m.yol, str)

    # Y7 — kontrol dejenere olmasın: hem gerçek yol hem YOLSUZ beyanı olmalı
    yollu = [m for m in SAG_KALANLAR if m.yol != YOLSUZ]
    assert yollu, "hiçbir girdi gerçek bir sayaç yolu taşımıyor"


def test_b52_YOLSUZ_beyani_esdeger_sayilmiyor():
    """`YOLSUZ` girdiler 'eşdeğer' kovasına DÜŞMEMELİ.

    Ölçüm onlar hakkında bir şey söyleyemez; "fark yok" ile "o kod hiç
    koşulmadı" aynı çıktıyı verir (Y8).

    🔴 27 AĞUSTOS — BU TEST BİR GREP'Tİ VE DEĞİŞTİRİLDİ.
    Altıncı denetimin B-113'teki tespiti: *"onu koruyan test bir GREP —
    dalın VAR OLDUĞUNU doğruluyor, ULAŞILABİLİR olduğunu değil. `03`ün
    'tetiklenemeyen kontrol' kuralı, korumanın kendisinde."*

    Denetçi haklıydı ve ölçümle gösterildi: dal gerçekten ulaşılamazdı
    (`kaynak_hash` her hücreyi farklılaştırıyordu), **ama bu test
    geçiyordu** — çünkü aradığı dizgi kodda duruyordu.

    Artık karar YÜKLEMİ doğrudan çağrılıyor. Kaynak denetimi
    `test_b113_ARAC_KENDI_YUKLEMLERINI_kullaniyor`a devredildi
    (orası yüklemin FİİLEN çağrıldığını AST ile bağlıyor).
    """
    from dogrulama.sag_kalan_ayikla import YOLSUZ, karar_ver

    # `ttl_olumu` bu tabanda TETİKLENİYOR — yani "karar_yok" yolu kapalı;
    # tek ayrım YOLSUZ beyanının kendisi olmalı.
    taban = {"ana/S2/orta/1": {"ttl_olumu": 5, "teslim_orani": 0.5}}

    assert karar_ver([], YOLSUZ, taban) == "yolsuz", (
        "YOLSUZ girdi 'yolsuz' kovasına düşmüyor")
    assert karar_ver([], "ttl_olumu", taban) == "esdeger", (
        "Y8 — karşılaştırma anlamsız: tetiklenen bir yol da 'yolsuz' "
        "çıkıyorsa ölçüt ayırt etmiyor")


# ==========================================================================
# 🔴 B-78 / Y12 — ZAMAN AŞIMI BÜTÇESİ, ELLE TUTULAN KAPI SABİTİ
#
# 25 Ağustos 2026: kapı Ç1.3'te düştü, 35 mutasyonun 31'i "geçersiz" sayıldı.
# Sebep bir desen uyuşmazlığı DEĞİLDİ — paket 324 → 354 teste (8,6–10,2 dk →
# 12,7 dk) büyümüştü, `timeout` 1200 sn'de kalmıştı ve `Pool(8)` çekişmesi
# altında mutant başına gerçek süre 18,5–20+ dk'ya çıkmıştı.
#
# 🔴 O sabiti HİÇBİR ŞEY KORUMUYORDU. Ucuz ön kontrol (`mutasyon_on_kontrol`)
# her mutantı `-k beklenen_test` ile koşar — saniyeler sürer, tam paketin
# süresini YAPISAL OLARAK göremez. Bu yüzden "ön kontrol geçti, kapı düştü"
# vakası ÜÇÜNCÜ kez yaşandı (K-042, K-046, K-058).
#
# Aşağıdaki test sabit bir sayıyı sabit bir sayıyla karşılaştırmaz —
# GÜNCEL test sayısını ölçüp oranlar. Paket büyüdüğünde kendiliğinden bağlar.
# ==========================================================================


def _gereken_zaman_asimi_s(test_sayisi: int) -> float:
    """Ölçülmüş tabandan, VERİLEN test sayısı için gereken zaman aşımı."""
    from dogrulama.mutasyon_paketi import (
        CEKISME_CARPANI, EMNIYET_PAYI, TEST_BASINA_EN_KOTU_S,
    )
    # 🔴 26 AĞU (K-067): SON okuma değil, **EN KÖTÜ GÖZLENEN** test başına
    # maliyet. Dört temiz koşu ölçüldü ve makine %15,2 oynuyor; en küçük
    # okumayı kullanmak marjı OLDUĞUNDAN İYİ gösterir — K-058'in yönü.
    return TEST_BASINA_EN_KOTU_S * test_sayisi * CEKISME_CARPANI * EMNIYET_PAYI


def test_b57_yeni_karar_kaydi_URETICI_satiri_TASIMAK_ZORUNDA():
    """🔴 B-57 — `04`teki her ÖLÇÜM bir üreticiye bağlı olmalı.

    `03` kural 1: *"Her sayının yanında üretici komut ve kaynak dosya."*

    ⚠️ B-57 üç denetim boyunca açık kaldı ve sayısı **DÖRT KEZ** yanlış
    ölçüldü. Dördüncüsü 26 Ağustos'ta bulundu: tarama `2026` *(tarih)*,
    `K-004` *(çapraz atıf)*, `802.11` *(standart)* ve `1000–1029` *(tohum
    kümesi ADI)* gibi şeyleri de **"sayı"** sayıyordu.

        GEVŞEK ölçüt : 37 üreticisiz   <- üç denetimin yazdığı sayı
        SIKI  ölçüt  : **28** üreticisiz

    ⚖️ Bu, B-74'ün açıldığı sınıfın **öteki yüzü**: B-74 *"üretici"*
    kelimesini prozada sayan gevşek taramayı yakalamıştı; burada gevşek olan
    **sayı dedektörüydü.**

    🔒 KAPANIŞ BİÇİMİ (K-053 + Y14): eski kayıtlara komut **UYDURULMAZ**.
    Bu test **kanamayı durdurur**: bugünkü 28 kayıt donduruldu, YENİ bir
    kayıt ölçüm taşıyorsa üretici satırı **zorunludur**.
    """
    from dogrulama.karar_kaydi_denetimi import DEVRALINAN_URETICISIZ, denetle

    s = denetle()
    eksik = set(s["eksik"])

    # 🔴 Y8 — ÖLÇÜM GERÇEKTEN BİR ŞEY BULUYOR MU: boş kümede her şey doğrudur
    assert len(s["olcum_tasiyan"]) > 40, (
        f"yalnızca {len(s['olcum_tasiyan'])} kayıt ölçüm taşıyor gibi "
        f"görünüyor — tarama FAZLA DAR olabilir (B-74'ün üçüncü hatası)")
    assert len(s["uretici_var"]) > 20, (
        f"yalnızca {len(s['uretici_var'])} kayıtta üretici satırı bulundu — "
        f"tarama hedefini kaçırıyor olabilir (B-74'ün ilk hatası)")

    yeni = sorted(eksik - DEVRALINAN_URETICISIZ)
    assert not yeni, (
        f"🔴 ÜRETİCİ SATIRI OLMAYAN YENİ KARAR KAYDI: {yeni}. "
        f"`03` kural 1: ölçüm taşıyan her kayıt üretici komutunu taşır. "
        f"Devralınan boşluk DONDURULDU ve büyüyemez (B-57 · K-069).")

    kurtulan = sorted(DEVRALINAN_URETICISIZ - eksik)
    assert not kurtulan, (
        f"🟢 şu kayıtlar üreticisine kavuşmuş: {kurtulan}. "
        f"`DEVRALINAN_URETICISIZ` listesinden ÇIKARILMALI — bayat bir "
        f"muafiyet listesi, gerçek boşluğu olduğundan büyük gösterir.")


def test_b57_URETICILI_bir_kayit_muafiyet_listesinde_OLAMAZ():
    """🔴 Y11 — muafiyet listesi *"üreticisi YOK"* demektir.

    Üreticisi olan bir kaydı listeye koymak, listeyi anlamsızlaştırır ve
    gerçek boşluğu gizler. (B-99'da aynı delik ölçüldü ve mutasyondan sağ
    çıkmıştı — burada baştan kapatılıyor.)
    """
    from dogrulama.karar_kaydi_denetimi import DEVRALINAN_URETICISIZ, denetle

    s = denetle()
    celiski = sorted(DEVRALINAN_URETICISIZ & set(s["uretici_var"]))
    assert not celiski, (
        f"{celiski} hem muafiyet listesinde hem üretici satırı VAR. "
        f"Muafiyet *'henüz üreticisi yok'* demektir (B-57).")

    # Y8 — liste boş DEĞİL, yoksa yukarıdaki değişmez boştur
    assert DEVRALINAN_URETICISIZ, (
        "muafiyet listesi BOŞ — ya B-57 kapandı ve bu test kaldırılmalı, "
        "ya liste sessizce silinmiş")


def test_b93_sim_altindaki_ASSERT_sayisi_BEYANLA_ayni():
    """🔴 Y12 — `08` madde 29'un saydığı `assert`ler ELLE yazılmış bir sayı.

    B-93 (beşinci denetim): `sim/` altındaki değişmezlerin **hepsi** `assert`
    ve `python -O` altında **sessizce kalkıyor**; hiçbir belgede beyan yoktu.
    Beyan `08` madde 29 olarak yazıldı — ama içindeki SAYI elle yazılmıştır
    ve paket büyüdükçe sessizce bayatlar (Y12'nin tam sınıfı).

    ⚠️ Denetçi **beş** saymıştı; **altıncısı** B-98'in düzeltmesiyle eklendi.
    Yani beyan daha yazılmadan bir kez bayatladı — bu test onu bağlar.

    🔴 26 AĞUSTOS → BUGÜN, D-7 (ALTINCI DENETİMİN DEVRALINMASI):
    BEYAN **(dosya, SATIR NUMARASI)** demetiydi ve bu, B-100 düzeltmesiyle
    birlikte bir Y8 ihlali doğuruyordu. Ölçüldü: **35 hedefli mutasyonun
    9'u** `sim/` altında satır kaydırıyor. `v2/` artık mutant kopyalarına
    girdiği için bu test orada da koşuyor — satır numarasına bağlı kalsaydı
    o dokuz mutantta **bedava "yakalandı"** üretirdi. Denetçi bunu M10'da
    tek örnekle ölçmüştü: *"yakalama davranışsal değil, DEFTER TUTMAYDI."*

    Ölçüt artık `assert`in **İFADESİDİR**. Satırın kayması bir değişmezi
    değiştirmez; ifadenin değişmesi değiştirir.

    ⚠️ `08` madde 29 hâlâ `dosya:satır` yazıyor. Bu test artık o satırları
    KİLİTLEMİYOR — bağladığı şey **dosya kümesi** (aşağıda). Madde 29'un
    satır numaraları Faz 5'te içerik beyanına çevrilecek (Y14).
    """
    import ast
    import re

    # (dosya, `assert` ifadesinin AST kaynağı) — satır numarası YOK
    #
    # ⚠️ 27 Ağu — ALTI → SEKİZ: B-116 (`mac.py`) ve B-112 (`gozlem.py`)
    # ölü dalları `assert`e çevrildi. `gozlem.py` kümeye İLK KEZ girdi.
    BEYAN = {
        ("events.py", "zaman >= self.simdi"),
        ("traffic.py", "simdi <= self.kon.olcum_bitis_s"),
        ("kosucu.py", "self.olaylar.simdi <= self.kon.kosu_bitis_s"),
        ("kosucu.py", "all((p.dogum_s <= bit for p in pencere))"),
        ("mac.py", "per is not None"),
        ("mac.py", "not (baska is not il and baska.gonderen == alici and "
                   "(baska.baslangic_s <= an_s < baska.bitis_s))"),
        ("mac.py", "ber < 0.5"),
        ("gozlem.py",
         "math.isnan(deger) or deger == _tek_duyarliga_kirp(deger)"),
    }
    olculen = set()
    for yol in sorted((KOK / "sim").glob("*.py")):
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        for d in ast.walk(agac):
            if isinstance(d, ast.Assert):
                olculen.add((yol.name, ast.unparse(d.test)))

    assert olculen == BEYAN, (
        "🔴 `sim/` altındaki `assert` değişmezleri DEĞİŞTİ.\n"
        "  ölçülen: %s\n  beyan  : %s\n"
        "`08` madde 29 bunları tek tek sayıyor ve `python -O` altında "
        "SESSİZCE kalktıklarını beyan ediyor. Liste değiştiyse beyan da "
        "güncellenmeli (B-93 · Y12)." % (sorted(olculen), sorted(BEYAN)))

    # 🔴 Y8 — TARAMA GERÇEKTEN BİR ŞEY BULUYOR MU
    assert len(olculen) >= 5, "tarama `assert` bulamıyor — ölçüt bozuk (Y7)"

    # 🔴 `08` MADDE 29 İLE CANLI BAĞ — satır değil, DOSYA kümesi.
    # Satır numaraları bayatlayabilir (ve bugün bayat); dosya kümesi
    # bayatlarsa beyan gerçekten yanlış olur: yeni bir dosyada `assert`
    # belirirse madde 29 onu saymıyor demektir.
    # ⚠️ 27 Ağu — desen `dosya:satır`dan DOSYA ADINA indirildi. Madde 29'un
    # satır numaraları kaldırıldı (D-7): hiçbir test onları kilitlemiyordu,
    # bayatlıyorlardı ve satır tabanlı ölçüt 35 mutasyonun 7'sinde bedava
    # yakalama üretiyordu. Bağlanan şey artık DOSYA KÜMESİ — yeni bir
    # dosyada `assert` belirirse beyan gerçekten yanlış olur.
    kapsam29 = (KOK / "v2" / "08-AILE0-KAPSAM.md").read_text(encoding="utf-8")
    madde29 = kapsam29.split("| **29** |", 1)[1].split("\n| **30**", 1)[0]
    beyan_dosyalari = set(re.findall(r"`(\w+\.py)`", madde29))
    assert beyan_dosyalari and beyan_dosyalari == {a for a, _ in olculen}, (
        "🔴 `08` madde 29'un saydığı DOSYALAR ölçülenle aynı değil.\n"
        f"  ölçülen dosyalar: {sorted({a for a, _ in olculen})}\n"
        f"  `08`de geçenler : {sorted(beyan_dosyalari)}")

    # 🔴 Y11 — `08` bu maddeyi GERÇEKTEN taşıyor mu (beyan ile test aynı
    # satırdan okunmalı — B-73'ün dersi)
    kapsam = (KOK / "v2" / "08-AILE0-KAPSAM.md").read_text(encoding="utf-8")
    assert "python -O" in kapsam, (
        "`08` `python -O` beyanını taşımıyor — madde 29 kaybolmuş olabilir")


def test_b88_cokme_sebebi_UC_OLAYI_AYIRT_ediyor():
    """🔴 B-88 — DÖRDÜNCÜ geçersizlik yolu artık üreticiye bağlı.

    Beşinci denetim ölçtü: raporlama katmanında **elle yazılmış** bir etiket
    vardı ve K-058'in kapattığı hatanın birebir aynısını, bir katman yukarıda
    tekrarlıyordu — **üç ayrı olay tek etikete iniyordu.** Denetçi o etiketi
    K-058'in *yanlış olduğu ölçülen* etiketiyle değiştirdi ve **367 testin
    367'si geçti**: kapı aynı yanlış teşhisi bir daha yapabilirdi.

    ⚖️ A-9 KISMEN ÇÜRÜTÜLDÜ (K-068): denetçi *"`AssertionError` içinde
    'ERROR' geçer, yani ölçüt testleri kıran HER mutantta True"* demişti.
    Ölçüldü — **yanlış**: `"AssertionError"` BÜYÜK HARFLİ `"ERROR"`
    içermez (`Error` ≠ `ERROR`). Eski ölçüt yine de bir **alt dizgi
    aramasıydı**, teşhis değildi; tipli hâle getirildi.
    """
    from dogrulama.mutasyon_paketi import cokme_sebebi

    collect = cokme_sebebi(2, "!!!! Interrupted: 1 error during collection !!!!")
    hata_bolumu = cokme_sebebi(
        1, "ERROR tests/x.py::t" + chr(10) + "1 error in 0.1s")
    cikis_kodu = cokme_sebebi(3, "3 passed")

    # üçü de ÇÖKME sayılmalı
    assert collect and hata_bolumu and cikis_kodu

    # 🔴 ASIL DEĞİŞMEZ: üç olay ÜÇ FARKLI şey söylemeli. Aynı metni
    # verirlerse etiket yeniden tek etikete iner ve B-88 geri gelir.
    assert len({collect, hata_bolumu, cikis_kodu}) == 3, (
        f"üç geçersizlik olayı AYNI etikete iniyor: "
        f"{ {collect, hata_bolumu, cikis_kodu} }. K-058'in hatası budur.")

    # ⚠️ *"Farklı olsun"* YETMEZ — üç ANLAMSIZ dizgi de farklıdır. Her
    # etiket, ayırt ettiği OLAYA bağlı olmalı. (Mutasyonla ölçüldü: yalnızca
    # farklılık arayan ilk hâli SAĞ KALDI.)
    assert "collect" in collect.lower(), (
        f"collect hatasının etiketi olayı ADLANDIRMIYOR: {collect!r}")
    assert ("kurulum" in hata_bolumu.lower()
            or "error" in hata_bolumu.lower()), (
        f"ERROR bölümünün etiketi olayı adlandırmıyor: {hata_bolumu!r}")
    assert "3" in cikis_kodu, (
        f"çıkış kodu etiketi KODU taşımıyor: {cikis_kodu!r} — teşhis, "
        f"okuyanı doğru yere göndermelidir (Y7)")

    # çökme OLMAYAN durumlar
    assert cokme_sebebi(0, "382 passed in 852.18s") is None
    assert cokme_sebebi(1, "4 failed, 378 passed") is None

    # 🔴 Y11 — KAPSAM DIŞI: `AssertionError` bir ÇÖKME DEĞİLDİR.
    # (A-9'un önermesi buydu ve ölçümle yanlış çıktı; değişmez yine de
    # yazılıyor ki biri ölçütü `lower()` ile gevşetirse yakalansın.)
    assert cokme_sebebi(1, "E   AssertionError: assert 1 == 2") is None, (
        "başarısız bir `assert` ÇÖKME sayılıyor — mutant testleri kırdı, "
        "koşamadı değil")
    assert cokme_sebebi(1, "FAILED tests/x.py::t - AssertionError") is None


def test_b88_raporlama_ELLE_YAZILMIS_etiket_KULLANMIYOR():
    """🔴 B-88'in ASIL değişmezi: etiket ÜRETİCİDEN gelmeli.

    Bir üreticinin **var olması**, raporlama katmanının onu **kullandığını**
    göstermez. Beşinci denetimin bulduğu şey tam olarak buydu:
    `gecersiz_sebebi()` vardı ve **dördüncü yol onu atlıyordu.**

    ⚠️ Bu test, ilk yazımdaki boşluktan doğdu: `cokme_sebebi()`yi doğrudan
    sınayan bir test, çağrı yerinin sabit bir dizgiye dönmesini **göremez**
    (mutasyonla ölçüldü — SAĞ KALDI).

    Kaynak taranıyor: `gecersiz.append((ad, SEBEP))` çağrılarının hiçbirinde
    `SEBEP` **çıplak bir dizgi sabiti** olamaz.
    """
    import ast

    src = (KOK / "dogrulama" / "mutasyon_paketi.py").read_text(encoding="utf-8")
    sabit_etiketler = []
    for d in ast.walk(ast.parse(src)):
        if not (isinstance(d, ast.Call)
                and isinstance(d.func, ast.Attribute)
                and d.func.attr == "append"
                and isinstance(d.func.value, ast.Name)
                and d.func.value.id == "gecersiz"):
            continue
        if not d.args:
            continue
        arg = d.args[0]
        if isinstance(arg, ast.Tuple) and len(arg.elts) == 2:
            sebep = arg.elts[1]
            if isinstance(sebep, ast.Constant):
                sabit_etiketler.append((d.lineno, sebep.value))

    assert not sabit_etiketler, (
        f"🔴 geçersizlik etiketi ELLE yazılmış: {sabit_etiketler}. "
        f"K-058'de tam olarak bu oldu: sabit bir etiket ÜÇ AYRI OLAYI aynı "
        f"şeye indirdi ve kapı düşme sebebini YANLIŞ raporladı (B-88).")

    # 🔴 Y8 — TARAMA GERÇEKTEN BİR ŞEY BULUYOR MU: `gecersiz.append`
    # çağrıları var olmalı, yoksa yukarıdaki değişmez boş kümede doğrudur.
    cagrilar = [d for d in ast.walk(ast.parse(src))
                if isinstance(d, ast.Call)
                and isinstance(d.func, ast.Attribute)
                and d.func.attr == "append"
                and isinstance(d.func.value, ast.Name)
                and d.func.value.id == "gecersiz"]
    assert len(cagrilar) >= 2, (
        f"yalnızca {len(cagrilar)} `gecersiz.append` bulundu — tarama "
        f"hedefini kaçırıyor olabilir (Y7)")


def test_b90_cekisme_carpani_OLCULEN_MAKSIMUMUN_ALTINA_dusemez():
    """🔴 Y12 — elle tutulan çarpan, ÖLÇÜLEN veriye bağlı.

    B-90 (beşinci denetim): `CEKISME_CARPANI` 1,60 idi ve **11 gözlemin
    10'u onun ÜSTÜNDEYDİ** (1,548–1,780, ortanca 1,744). Yani gereken zaman
    aşımı sistematik olarak EKSİK tahmin ediliyordu — K-058'in kapıyı
    düşürüp sebebini yanlış raporlayan hatasının aynı sınıfı.

    Bu test sabiti veriye bağlar: biri çarpanı düşürürse, ölçümün kendisiyle
    çelişir ve burada durur.
    """
    from dogrulama.mutasyon_paketi import CEKISME_CARPANI, OLCULEN_CEKISME

    assert OLCULEN_CEKISME, "ölçüm listesi BOŞ — sabit hiçbir şeye bağlı değil"
    assert CEKISME_CARPANI >= max(OLCULEN_CEKISME), (
        f"🔴 çarpan {CEKISME_CARPANI} ölçülen maksimumun "
        f"({max(OLCULEN_CEKISME)}) ALTINDA. Gereken zaman aşımı eksik "
        f"hesaplanır ve kapı YANLIŞ SEBEPLE düşer (B-90 · K-058).")

    # Y8 — ölçümün kendisi anlamlı mı: çekişme koşuyu HIZLANDIRAMAZ
    assert min(OLCULEN_CEKISME) > 1.0, (
        "ölçülen çarpanlardan biri ≤ 1,0 — çekişme koşuyu hızlandıramaz, "
        "ölçüm bozuk")

    # 🔴 K-067 — TEST BAŞINA MALİYET DE VERİYE BAĞLI OLMALI.
    # Dört temiz koşu ölçüldü ve makine %15,2 oynuyor. En küçük okumayı
    # kullanmak marjı OLDUĞUNDAN İYİ gösterir — K-058'in yönü.
    from dogrulama.mutasyon_paketi import (
        OLCULEN_KOSULAR, TEST_BASINA_EN_KOTU_S,
    )

    assert len(OLCULEN_KOSULAR) >= 3, (
        "üçten az temiz koşu ölçülmüş — koşudan koşuya değişkenlik "
        "GÖRÜLEMEZ ve en kötü maliyet bilinemez")
    assert all(n > 0 and s > 0 for n, s in OLCULEN_KOSULAR)
    assert abs(TEST_BASINA_EN_KOTU_S
               - max(s / n for n, s in OLCULEN_KOSULAR)) < 1e-9, (
        "🔴 `TEST_BASINA_EN_KOTU_S` ölçümlerden TÜRETİLMİYOR — elle "
        "yazılmış bir sayı sessizce bayatlar (Y12).")

    # Y8 — değişkenlik GERÇEKTEN var mı: yoksa "en kötü" seçmek boş bir
    # ihtiyattır ve yukarıdaki gerekçe yanlıştır.
    tb = [s / n for n, s in OLCULEN_KOSULAR]
    assert max(tb) / min(tb) > 1.05, (
        f"koşular arası yayılım yalnızca %{100*(max(tb)/min(tb)-1):.1f} — "
        f"'en kötüyü al' gerekçesi ölçümle desteklenmiyor")

    # 🔴 Y11 — kapsamın DIŞI: çarpan ölçüme bağlı ama SINIRSIZ da olamaz;
    # yazılı zaman aşımı bugünkü paketi hâlâ kaldırmalı.
    #
    # ⚠️ 27 AĞUSTOS — BURADA ELLE YAZILMIŞ BİR `3600` VARDI ve sabit
    # büyütülür büyütülmez BAYATLADI: test, korumanın kendisini `3600 sn`e
    # çivilemişti. Bu, A-12'nin (`_T_975_7` iki dosyada) ve B-07'nin
    # *"ikinci doğru kaynağı"* dersinin aynısı — bu kez KORUMANIN İÇİNDE.
    # Artık sabitin kendisinden okunuyor.
    from dogrulama.mutasyon_paketi import MUTANT_ZAMAN_ASIMI_S

    guncel = toplanan_test_sayisi(["tests"], None)
    assert _gereken_zaman_asimi_s(guncel) < MUTANT_ZAMAN_ASIMI_S, (
        f"çarpan o kadar büyüdü ki {MUTANT_ZAMAN_ASIMI_S} sn artık yetmiyor "
        f"— zaman aşımı da büyütülmeli, yoksa kapı Ç1.3'te düşer")


def test_b78_mutant_zaman_asimi_GUNCEL_test_sayisini_kaldiriyor():
    """🔴 Y12 — zaman aşımı, BUGÜNKÜ paketi koşturmaya yetmeli.

    Sabit ↔ sabit karşılaştırması değil: test sayısı `--collect-only` ile
    ÖLÇÜLÜR ve ölçülmüş süre tabanı o orana göre büyütülür.
    """
    from dogrulama.mutasyon_paketi import MUTANT_ZAMAN_ASIMI_S

    guncel = toplanan_test_sayisi(["tests"], None)
    gereken = _gereken_zaman_asimi_s(guncel)

    assert MUTANT_ZAMAN_ASIMI_S >= gereken, (
        f"🔴 ZAMAN AŞIMI YETMİYOR — kapı Ç1.3'te düşecek ve sebebi "
        f"YANLIŞ raporlanacak.\n"
        f"    güncel test sayısı : {guncel}\n"
        f"    gereken zaman aşımı: {gereken:.0f} sn ({gereken/60:.1f} dk)\n"
        f"    yazılı zaman aşımı : {MUTANT_ZAMAN_ASIMI_S} sn "
        f"({MUTANT_ZAMAN_ASIMI_S/60:.1f} dk)\n"
        f"    Ya `MUTANT_ZAMAN_ASIMI_S` büyütülür, ya paket süresi "
        f"YENİDEN ÖLÇÜLÜP `PAKET_SURESI_S`/`PAKET_TEST_SAYISI` tazelenir.")


def test_b78_taban_zaman_asimi_de_yetiyor():
    """Taban koşusu TEK başına koşar — çekişme yok, ama paket yine büyür."""
    from dogrulama.mutasyon_paketi import (
        EMNIYET_PAYI, PAKET_SURESI_S, PAKET_TEST_SAYISI, TABAN_ZAMAN_ASIMI_S,
    )
    guncel = toplanan_test_sayisi(["tests"], None)
    gereken = PAKET_SURESI_S * (guncel / PAKET_TEST_SAYISI) * EMNIYET_PAYI
    assert TABAN_ZAMAN_ASIMI_S >= gereken, (
        f"taban zaman aşımı yetmiyor: {gereken:.0f} sn gerekiyor, "
        f"{TABAN_ZAMAN_ASIMI_S} sn yazılı")


def test_b78_olcum_sabitleri_DEJENERE_DEGIL():
    """🔴 Y7 — kontrolün KENDİ girdisi doğrulanır.

    Çarpanlardan biri 0 ya da 1 olursa test her zaman geçer ve hiçbir şey
    korumaz. `PAKET_TEST_SAYISI` 0 olursa bölme çöker.
    """
    from dogrulama.mutasyon_paketi import (
        CEKISME_CARPANI, EMNIYET_PAYI, PAKET_SURESI_S, PAKET_TEST_SAYISI,
    )
    assert PAKET_TEST_SAYISI > 0
    assert PAKET_SURESI_S > 0
    assert CEKISME_CARPANI >= 1.0, "çekişme koşuyu HIZLANDIRAMAZ"
    assert EMNIYET_PAYI >= 1.0, "emniyet payı 1'in altında olamaz"
    # Ölçülen değerler; biri sessizce 1,0'a çekilirse koruma boşalır
    assert CEKISME_CARPANI > 1.0, (
        "çekişme çarpanı 1,0 — 8 yollu koşunun yavaşlamadığı iddia ediliyor, "
        "ölçüm bunun tersini söylüyor (18,5 dk / 12,7 dk = 1,46; ≥1,57)")
    assert EMNIYET_PAYI > 1.0


def test_b78_Y11_koruma_YETERSIZ_sabiti_reddediyor():
    """🔴 Y11 — koruma, yakalayamadığı bir vakayla değil, KAÇIRDIĞI vakayla
    sınanır: 25 Ağustos'ta fiilen kullanılan 1200 sn REDDEDİLMELİ.

    Bu, korumanın "bugünkü değer geçiyor" demekten fazlasını yaptığının
    kanıtı: gerçekten düşmüş bir yapılandırmayı düşürüyor.
    """
    guncel = toplanan_test_sayisi(["tests"], None)
    gereken = _gereken_zaman_asimi_s(guncel)
    DUSEN_SABIT = 1200          # 25 Ağu 2026'da kapıyı düşüren değer
    assert DUSEN_SABIT < gereken, (
        f"koruma dejenere: kapıyı fiilen düşüren {DUSEN_SABIT} sn'lik sabit "
        f"bu ölçütten GEÇİYOR ({gereken:.0f} sn gerekiyor)")


# ==========================================================================
# 🔴 B-79 / Y7 — RAPOR, ARACIN YAPMADIĞI TEŞHİSİ BASAMAZ
#
# Kaynak grep'i DEĞİL, davranış: `gecersiz_sebebi` üç olay türünü de ayırt
# etmeli. Sabit etiket basan bir sürüm bu testlerden GEÇEMEZ.
# ==========================================================================


def test_b79_zaman_asimi_DESEN_HATASI_gibi_raporlanmiyor():
    """🔴 25 Ağustos'ta kapıyı yanlış yöne saptıran tam olarak buydu."""
    from dogrulama.mutasyon_paketi import gecersiz_sebebi

    sebep = gecersiz_sebebi({
        "ad": "M1_dus_silindi", "tur": "zaman_asimi",
        "hata": "ZAMAN AŞIMI — 3600 sn içinde bitmedi "
                "(mutasyon UYGULANDI, paket bitiremedi)"})

    assert "ZAMAN AŞIMI" in sebep, (
        f"zaman aşımı sebebi kayboldu: {sebep!r}")
    assert "uygulanamadı" not in sebep, (
        f"🔴 zaman aşımı, KAYNAK DESENİ hakkında bir iddiayla raporlanıyor — "
        f"mutasyon UYGULANMIŞTI: {sebep!r}")


def test_b79_desen_hatasi_KENDI_sebebini_koruyor():
    from dogrulama.mutasyon_paketi import gecersiz_sebebi

    sebep = gecersiz_sebebi({
        "ad": "X", "tur": "desen",
        "hata": "mutasyon uygulanamadı (desen kaynakta yok): sim/mac.py"})
    assert "desen kaynakta yok" in sebep
    assert "sim/mac.py" in sebep, "hangi dosya olduğu kayboldu"


def test_b79_beklenmedik_istisna_da_GORUNUR_kaliyor():
    from dogrulama.mutasyon_paketi import gecersiz_sebebi

    sebep = gecersiz_sebebi({
        "ad": "X", "tur": "istisna", "hata": "OSError(28, 'No space left')"})
    assert "OSError" in sebep and "No space left" in sebep, (
        f"gerçek istisna yutuldu: {sebep!r}")


def test_b79_Y11_UC_TUR_birbirinden_AYIRT_EDILEBILIR():
    """🔴 Y11 — koruma, yakalayabildiği tek vakayla sınanamaz.

    Üç sebep birbirinden farklı olmalı; sabit etiket basan bir sürümde
    üçü de AYNI dizge olur ve bu test kırılır.
    """
    from dogrulama.mutasyon_paketi import gecersiz_sebebi

    sebepler = {
        gecersiz_sebebi({"ad": "X", "tur": "desen",
                         "hata": "mutasyon uygulanamadı (desen kaynakta yok): a.py"}),
        gecersiz_sebebi({"ad": "X", "tur": "zaman_asimi",
                         "hata": "ZAMAN AŞIMI — 3600 sn içinde bitmedi"}),
        gecersiz_sebebi({"ad": "X", "tur": "istisna",
                         "hata": "OSError(28)"}),
    }
    assert len(sebepler) == 3, (
        f"üç farklı olay {len(sebepler)} farklı sebep üretiyor — "
        f"rapor bunları ayırt edemiyor: {sebepler}")


def test_b79_Y7_sebep_BILDIRILMEMISSE_sessizce_dogru_gorunmuyor():
    """Boş bir `hata` alanı 'sorun yok' gibi okunmamalı."""
    from dogrulama.mutasyon_paketi import gecersiz_sebebi

    sebep = gecersiz_sebebi({"ad": "X", "tur": "istisna", "hata": ""})
    assert "BİLDİRİLMEDİ" in sebep, f"boş sebep sessizce geçti: {sebep!r}"


def test_b79_ZAMAN_ASIMI_METNINI_URETEN_yer_de_korunuyor():
    """🔴 Y11 — sınıflandırıcıyı test etmek YETMİYOR.

    Beni 25 Ağustos'ta yanlış yöne saptıran etiket `gecersiz_sebebi`de
    değil, mesajı ÜRETEN yerde doğuyordu. Sentetik sözlükle yapılan test
    o yeri hiç çalıştırmıyor: metni "mutasyon uygulanamadı"ya çeviren
    mutasyon (M-C7) sağ kalmıştı.
    """
    from dogrulama.mutasyon_paketi import zaman_asimi_sebebi

    metin = zaman_asimi_sebebi(3600)
    assert "ZAMAN AŞIMI" in metin, f"zaman aşımı ilan edilmiyor: {metin!r}"
    assert "3600" in metin, "kaç saniyede aşıldığı kayboldu"
    assert "uygulanamadı" not in metin, (
        f"🔴 zaman aşımı, KAYNAK DESENİ hakkında bir iddiayla raporlanıyor — "
        f"oysa mutasyon UYGULANMIŞTI: {metin!r}")
    assert "UYGULANDI" in metin, (
        "metin, mutasyonun uygulandığını AÇIKÇA söylemeli — 25 Ağustos'ta "
        "kaybolan bilgi tam olarak buydu")


def test_b79_DESEN_METNINI_URETEN_yer_de_korunuyor():
    from dogrulama.mutasyon_paketi import desen_tutmadi_sebebi

    metin = desen_tutmadi_sebebi("sim/mac.py")
    assert "sim/mac.py" in metin, "hangi dosya olduğu kayboldu"
    assert "desen" in metin.lower(), (
        f"sebebin DESEN olduğu söylenmiyor: {metin!r}")


def test_b79_Y11_iki_uretici_AYNI_metni_vermiyor():
    """İki üretici çakışırsa rapor yine ayırt edemez."""
    from dogrulama.mutasyon_paketi import (
        desen_tutmadi_sebebi, zaman_asimi_sebebi,
    )
    assert zaman_asimi_sebebi(3600) != desen_tutmadi_sebebi("sim/mac.py")


def test_b79_Y7_uretici_fonksiyonlar_KULLANILIYOR_beyanda_kalmiyor():
    """🔴 `03` B5 — "bildirim ≠ kullanım".

    Fonksiyonlar var ama `_kosu` onları çağırmıyorsa koruma sahtedir:
    testler geçer, kapı yine sabit etiket basar. AST ile denetlenir —
    docstring/yorum metnine bakan bir tarama kendi metnini yakalar (B-68).
    """
    import ast

    kaynak = (KOK / "dogrulama" / "mutasyon_paketi.py").read_text(
        encoding="utf-8")
    agac = ast.parse(kaynak)

    kosu = next((d for d in ast.walk(agac)
                 if isinstance(d, ast.FunctionDef) and d.name == "_kosu"), None)
    assert kosu is not None, "_kosu bulunamadı"

    cagrilan = {d.func.id for d in ast.walk(kosu)
                if isinstance(d, ast.Call) and isinstance(d.func, ast.Name)}
    for ad in ("zaman_asimi_sebebi", "desen_tutmadi_sebebi"):
        assert ad in cagrilan, (
            f"🔴 `{ad}` TANIMLI ama `_kosu` onu ÇAĞIRMIYOR — koruma beyanda "
            f"kalmış. _kosu içinde çağrılanlar: {sorted(cagrilan)}")


# ==========================================================================
# 🔴 B-100 (ALTINCI DENETİM) — DEPO KOPYALAMA KURALI TEK KAYNAKTA
#
# Dört ölçüm aracı depoyu geçici bir dizine kopyalar. Kural altı ayrı yere
# elle yazılmıştı ve altısı da `"v2"`yi dışlıyordu. 26 Ağustos oturumunun
# yazdığı ÜÇ test `v2/` altındaki belgeleri okuyor:
#
#     depoda         : 45 passed          v2'siz kopyada : 3 failed, 42 passed
#
# `paketi_kostur()` taban kırıkken erken döner → kapı Ç1.3'te `!!TABAN`
# yazar ve KAPANMAZ. Ucuz ön kontrol bunu YAPISAL OLARAK göremez (`-k` ile
# koştuğu için o üç test hiç toplanmaz) — deponun DÖRDÜNCÜ "ön kontrol
# geçti, kapı düştü" vakası (K-042 · K-046 · K-058).
#
# 🔴 Y12: bu, elle tutulan bir kapı sabitidir ve ucuz bir testle korunur.
# Altı kopyadan biri ayrıştı ve kimse fark etmedi; yedincisi de ayrışırdı.
# ==========================================================================

_KOPYALAYAN_ADLAR = frozenset({"copytree", "ignore_patterns"})


def _kopyalayan_cagrilar(kaynak: str) -> list[str]:
    """Bir kaynak metninde depo kopyalayan çağrılar — AST'den.

    🔴 Metin araması DEĞİL: bu dosyanın kendi yorumları `copytree` kelimesini
    içeriyor ve düz bir `in` taraması kendi metnini yakalardı (B-68'in dersi,
    B-89'un çözümü). Yorum ve docstring AST'ye hiç girmez.
    """
    import ast

    bulunan = []
    for d in ast.walk(ast.parse(kaynak)):
        if not isinstance(d, ast.Call):
            continue
        f = d.func
        ad = (f.attr if isinstance(f, ast.Attribute)
              else f.id if isinstance(f, ast.Name) else None)
        if ad in _KOPYALAYAN_ADLAR:
            bulunan.append(ad)
    return bulunan


def test_b100_KOPYA_KURALI_TEK_KAYNAKTA():
    """🔴 `dogrulama/` altında depoyu kopyalayan TEK yer `kopya.py`dir.

    Y8 + Y11 aynı testte: taramanın canlı olduğu (gerçek çağrıyı buluyor) ve
    kapsamı dışındaki bir vakayı REDDETTİĞİ (sentetik bir ikinci kopya)
    birlikte gösterilir. Yoksa "0 bulundu" ile "tarama bozuk" aynı çıktıyı
    verir (Y7 · K-033'ün dersi).
    """
    kopya_yolu = KOK / "dogrulama" / "kopya.py"

    # 🔴 Y8 — TARAMA GERÇEKTEN BİR ŞEY BULUYOR MU
    gercek = _kopyalayan_cagrilar(kopya_yolu.read_text(encoding="utf-8"))
    assert gercek, (
        "tarama `dogrulama/kopya.py` içindeki gerçek `copytree` çağrısını "
        "bulamıyor — ölçüt bozuk, 'ihlal yok' sonucu ANLAMSIZ (Y7)")

    # 🔴 Y11 — KAPSAM DIŞI BİR VAKA ÜRETİLİP REDDEDİLİYOR
    sentetik = ('import shutil\n'
                'def kotu(h):\n'
                '    shutil.copytree("a", h, '
                'ignore=shutil.ignore_patterns("v2"))\n')
    assert _kopyalayan_cagrilar(sentetik), (
        "tarama İKİNCİ bir kopyalama uygulamasını yakalayamıyor — "
        "koruma yalnızca kendi tanıdığı vakayı görüyor (Y11)")

    # asıl ölçüt
    ihlal = {}
    for yol in sorted((KOK / "dogrulama").glob("*.py")):
        if yol.name == "kopya.py":
            continue
        bulunan = _kopyalayan_cagrilar(yol.read_text(encoding="utf-8"))
        if bulunan:
            ihlal[yol.name] = bulunan

    assert not ihlal, (
        "🔴 `dogrulama/` altında İKİNCİ bir depo kopyalama uygulaması var: "
        f"{ihlal}\n"
        "Kopyalama kuralı yalnızca `dogrulama/kopya.py::depoyu_kopyala` "
        "içinde olabilir. B-100 tam olarak altı ayrı kopyanın ayrışmasından "
        "doğdu ve 150 dakikalık kapıyı düşürüyordu.")


def _v2_bagimliliklari() -> set[str]:
    """`KOK / "v2" / <ad>` biçiminde okunan belge adları — AST'den TÜRETİLİR.

    🔴 Elle yazılmaz. Yarın dördüncü bir test `v2/` altından bir belge daha
    okursa bu küme kendiliğinden büyür; elle yazılan bir liste sessizce
    bayatlardı (`03` B5: "etiketi elle taşımak").
    """
    import ast

    adlar: set[str] = set()
    for dizin in ("tests", "dogrulama"):
        for yol in sorted((KOK / dizin).glob("*.py")):
            for d in ast.walk(ast.parse(yol.read_text(encoding="utf-8"))):
                if not (isinstance(d, ast.BinOp)
                        and isinstance(d.op, ast.Div)
                        and isinstance(d.right, ast.Constant)
                        and isinstance(d.right.value, str)):
                    continue
                ic = d.left
                if (isinstance(ic, ast.BinOp) and isinstance(ic.op, ast.Div)
                        and isinstance(ic.right, ast.Constant)
                        and ic.right.value == "v2"):
                    adlar.add(d.right.value)
    return adlar


def test_b100_KOPYA_v2_BELGELERINI_TASIYOR(tmp_path):
    """🔴 Ölçüt SABİT DEĞİL, DAVRANIŞTIR: kopya gerçekten kuruluyor mu?

    `"v2" not in KOPYA_DISLAMA` demek yetmez — dışlama başka bir yoldan da
    olabilir. Burada depo fiilen kopyalanır ve `v2/` altından okunan her
    belgenin kopyada BULUNDUĞU ölçülür. Bedeli ölçüldü: **0,20 sn**.
    """
    from dogrulama.kopya import KOPYA_DISLAMA, depoyu_kopyala

    assert "v2" not in KOPYA_DISLAMA, (
        "🔴 `v2` dışlama listesine geri konmuş — kapı Ç1.3'te `!!TABAN` ile "
        "düşer (B-100)")

    gerekli = _v2_bagimliliklari()
    # 🔴 Y8 — tarama gerçekten bir bağımlılık buluyor mu (boş küme tuzağı)
    assert gerekli, (
        "`v2/` bağımlılığı taraması BOŞ döndü — ölçüt bozuk. Bugün en az "
        "`04-NEDEN-BOYLE.md` ve `08-AILE0-KAPSAM.md` okunuyor (Y7)")

    hedef = depoyu_kopyala(tmp_path / "depo")
    eksik = sorted(a for a in gerekli if not (hedef / "v2" / a).exists())
    assert not eksik, (
        f"🔴 kopyada `v2/` altındaki şu belgeler YOK: {eksik}\n"
        "Onları okuyan testler kopyada `FileNotFoundError` alır; taban "
        "kırılır ve kapı YANLIŞ SEBEPLE düşer (B-100).")


def test_b100_TABAN_ile_MUTANTLAR_AYNI_ORTAMDA_kosuyor():
    """🔴 Y7 — bir doğrulama aracı NE KOŞTUĞUNU kendisi doğrular.

    `taban_kontrolu()`nun docstring'i *"mutantlarla AYNI YOLDAN — aynı
    `copytree`"* diyordu ve bu ÖLÇÜLMEMİŞTİ: `_kosu` `"*.txt"`i dışlamıyor,
    `taban_kontrolu` dışlıyordu. İki farklı dosya ortamında koşan bir
    karşılaştırma, kopyalama kaynaklı bir kırıklığı göremez.

    Ölçüt: ikisi de AYNI fonksiyonu çağırır — ayrışacak ikinci liste yok.
    """
    import ast

    kaynak = (KOK / "dogrulama" / "mutasyon_paketi.py").read_text(
        encoding="utf-8")
    agac = ast.parse(kaynak)

    for ad in ("_kosu", "taban_kontrolu"):
        fn = next((d for d in ast.walk(agac)
                   if isinstance(d, ast.FunctionDef) and d.name == ad), None)
        assert fn is not None, f"{ad} bulunamadı"
        cagrilan = {d.func.id for d in ast.walk(fn)
                    if isinstance(d, ast.Call) and isinstance(d.func, ast.Name)}
        assert "depoyu_kopyala" in cagrilan, (
            f"🔴 `{ad}` depoyu KENDİ yolundan kopyalıyor. Taban ile mutantlar "
            f"aynı ortamda koşmuyorsa 'yakalandı' sayımı anlamsızdır (Y7).")


# ==========================================================================
# 🔴 B-111 (ALTINCI DENETİM) — Ç6.1 VE Ç6.3 KANDIRILABİLİYORDU
#
# Denetçi dört denemeyi de ÖLÇTÜ ve ikisi yanlış pozitif, ikisi yanlış
# negatifti. Yüklemler AST'ye bağlandı; burada altı vaka birden sınanıyor.
#
# ⚖️ Y11'in tam tanımı: bir koruma, yalnızca yakalayabildiği durumla
# sınanamaz. Bu yüzden hem KAPSAM DIŞI iki vaka (b1 · b2 — geçmeli) hem
# KANDIRMA üç vakası (a1 · a2 · c1 — düşmeli) birlikte ölçülür.
#
# 🔴 Ve bu test kapıyı 150 dk koşturmadan konuşur (Y12).
# ==========================================================================

def _mac_kaynagi() -> str:
    return (KOK / "sim" / "mac.py").read_text(encoding="utf-8")


# `_iletim_bitir`in KİMLİKLE çıkarma bloğu ve DEĞERLE yapan kandırma hâli.
# Satır satır yazılıyor: gömülü kaçış dizileri bir kez sessizce bozuldu.
_CIKARMA_BLOGU = "\n".join((
    "            if x is il:",
    "                del self.aktif[i]",
    "                break",
))
_CIKARMA_BLOGU_DEGERLE = "\n".join((
    "            if x is il:",
    "                pass",
    "            if x == il:",
    "                del self.aktif[i]",
    "                break",
))
_CIKARMA_BLOGU_REMOVE = "\n".join((
    "            pass",
    "        self.aktif.remove(il)",
))


def test_b111_C61_ve_C63_dokunulmamis_kaynakta_GECIYOR():
    """🔴 Y8/Y7 — ölçüt canlı mı: sağlam kaynakta İKİSİ de True olmalı.

    Bu olmadan "kandırma denemesi düştü" cümlesi anlamsızdır: her zaman
    False dönen bir yüklem de dört denemeyi "yakalar".
    """
    from dogrulama.aile0_kapi_raporu import (
        c61_onay_yonu_dogru, c63_iletim_kimlikle_karsilastiriliyor,
    )
    s = _mac_kaynagi()
    assert c61_onay_yonu_dogru(s), "Ç6.1 sağlam kaynakta düşüyor"
    assert c63_iletim_kimlikle_karsilastiriliyor(s), "Ç6.3 sağlam kaynakta düşüyor"


def test_b111_YANLIS_POZITIF_kapali_yorum_kandiramiyor():
    """🔴 (a1) ve (a2) — davranış bozuldu, aynı dizgi YORUMA kondu.

    Eski dizgi araması ikisinde de GEÇİYORDU: kapı bozuk bir MAC'i onaylardı.
    """
    from dogrulama.aile0_kapi_raporu import (
        c61_onay_yonu_dogru, c63_iletim_kimlikle_karsilastiriliyor,
    )
    s = _mac_kaynagi()

    # (a1) onay YÖNÜ ters çevrildi, eski dizgi yorumda duruyor
    a1 = s.replace(
        "onay = Iletim(alici, veri_gonderen,",
        "# Iletim(alici, veri_gonderen  <- YALNIZCA YORUMDA\n"
        "        onay = Iletim(veri_gonderen, alici,", 1)
    assert a1 != s, "a1 deseni tutmadı — deneme kurulamadı (Y7)"
    assert not c61_onay_yonu_dogru(a1), (
        "🔴 Ç6.1 onay YÖNÜ ters çevrilmiş bir MAC'i onayladı (B-111/a1)")

    # (a2) kimlik → DEĞER karşılaştırması, eski dizgi yorumda duruyor
    a2 = s.replace(
        "            if x is il:",
        "            # if x is il:  <- YALNIZCA YORUMDA\n"
        "            if x == il:", 1)
    assert a2 != s, "a2 deseni tutmadı — deneme kurulamadı (Y7)"
    assert not c63_iletim_kimlikle_karsilastiriliyor(a2), (
        "🔴 Ç6.3 DEĞER karşılaştırmasına dönmüş bir MAC'i onayladı (B-111/a2)")

    # 🔴 (a3) KİMLİK KARŞILAŞTIRMASI DURUYOR AMA ÇIKARMA DEĞERLE YAPILIYOR.
    #
    # ⚖️ BU VAKA Y2'NİN İLK TURUNDA DOĞDU ve bir DELİK kapattı: yüklemin
    # `==` reddi başta HİÇBİR TESTÇE TETİKLENMİYORDU (a2'de `is` zaten
    # kayboluyor, yani ikinci koşul tek başına yetiyordu). Yani koruma,
    # deponun üç kez `assert`e çevirdiği "tetiklenemeyen kontrol" sınıfına
    # girmişti — dördüncüsü B-112'de bulunmuştu, beşincisini bu tur önledi.
    # Bu vaka `is`i YERİNDE bırakır ve gerçek çıkarmayı `==` ile yapar.
    a3 = s.replace(_CIKARMA_BLOGU, _CIKARMA_BLOGU_DEGERLE, 1)
    assert a3 != s, "a3 deseni tutmadı — deneme kurulamadı (Y7)"
    assert not c63_iletim_kimlikle_karsilastiriliyor(a3), (
        "🔴 Ç6.3 `is`i vitrinde tutup çıkarmayı `==` ile yapan bir MAC'i "
        "onayladı (B-111/a3) — `==` reddi TETİKLENMİYOR demektir")

    # (c1) gerçek `.remove(il)` — `list.remove` `==` kullanır
    c1 = s.replace(_CIKARMA_BLOGU, _CIKARMA_BLOGU_REMOVE, 1)
    assert c1 != s, "c1 deseni tutmadı — deneme kurulamadı (Y7)"
    assert not c63_iletim_kimlikle_karsilastiriliyor(c1), (
        "🔴 Ç6.3 `.remove(il)` kullanan bir MAC'i onayladı (B-111)")


def test_b111_YANLIS_NEGATIF_esdeger_yeniden_yazim_dusurmuyor():
    """🔴 (b1) ve (b2) — davranış BİREBİR aynı, kriter yine de GEÇMELİ.

    Eski dizgi araması ikisinde de DÜŞÜYORDU: kapı sağlam bir MAC'i
    reddederdi ve düşme sebebi YANLIŞ olurdu (K-058'in sınıfı).
    """
    from dogrulama.aile0_kapi_raporu import (
        c63_iletim_kimlikle_karsilastiriliyor as c63,
    )
    s = _mac_kaynagi()

    # (b1) operand sırası ters — `x is il` yerine `il is x`
    b1 = s.replace("            if x is il:", "            if il is x:", 1)
    assert b1 != s, "b1 deseni tutmadı — deneme kurulamadı (Y7)"
    assert c63(b1), (
        "🔴 Ç6.3 davranışı BİREBİR aynı bir yeniden yazımı reddetti "
        "(B-111/b1) — yanlış negatif")

    # (b2) yorumda `.remove(il)` geçiyor, kod değişmedi
    b2 = s.replace("        # Kimlik uzerinden cikar:",
                   "        # `.remove(il)` KULLANILMAZ:", 1)
    assert b2 != s, "b2 deseni tutmadı — deneme kurulamadı (Y7)"
    assert c63(b2), (
        "🔴 Ç6.3 YALNIZCA YORUMDA geçen bir dizgi yüzünden düştü "
        "(B-111/b2) — yanlış negatif")


def test_b111_YUKLEMLER_KAPIDA_FIILEN_KULLANILIYOR():
    """🔴 `03` B5 — bildirim ≠ kullanım.

    İki yüklem tanımlı olup kapı hâlâ dizgi araması yapıyorsa koruma
    sahtedir: testler geçer, kapı yine kandırılabilir. AST ile denetlenir.
    """
    import ast

    kaynak = (KOK / "dogrulama" / "aile0_kapi_raporu.py").read_text(
        encoding="utf-8")
    ana = next(
        (d for d in ast.walk(ast.parse(kaynak))
         if isinstance(d, ast.FunctionDef) and d.name == "main"), None)
    assert ana is not None, "main() bulunamadı"

    cagrilan = {d.func.id for d in ast.walk(ana)
                if isinstance(d, ast.Call) and isinstance(d.func, ast.Name)}
    for ad in ("c61_onay_yonu_dogru", "c63_iletim_kimlikle_karsilastiriliyor"):
        assert ad in cagrilan, (
            f"🔴 `{ad}` TANIMLI ama kapı onu ÇAĞIRMIYOR — Ç6 yeniden dizgi "
            f"aramasına dönmüş olabilir (B-111 · `03` B5)")


# ==========================================================================
# 🔴 B-106 (ALTINCI DENETİM) — `SonucYazici` HİÇBİR ÖLÇÜM YOLUNDA KURULMUYORDU
#
# `03` Bölüm C sözleşme 5: *"Her sonuç KENDİ TAM KONFİGÜRASYONUYLA
# saklanır"* + *"her satır ANINDA diske yazılır"*. Sınıf yazılmış,
# belgelenmiş, test edilmiş — ve hiç çağrılmamıştı. Tek kullanıcısı kendi
# birim testiydi; `dogrulama/` altındaki hiçbir araç sonuç yazmıyordu.
#
# 🔒 Karar (öğrenci, 27 Ağu): *"üretim yolunun ZORUNLU parçası; 9 `Kosu()`
# çağrı yerini tek kanonik `olc(...)` yoluna taşı."*
# ⚠️ Ölçüldü: 9 değil **11** çağrı yeri, 8 dosya. Kapsam değişmedi.
# ==========================================================================

def _dogrulama_modulleri():
    for yol in sorted((KOK / "dogrulama").glob("*.py")):
        if yol.name in ("kopya.py", "olcum.py"):
            continue
        yield yol


def test_b106_dogrulama_altinda_CIPLAK_Kosu_YOK():
    """🔴 `dogrulama/` altında `Kosu(...)` doğrudan çağrılamaz.

    Çağrılabilseydi sözleşme sessizce atlanırdı: koşu yapılır, sonuç satırı
    YAZILMAZ ve kimse fark etmez — B-106 tam olarak bu şekilde altı denetim
    boyunca görülmedi.

    AST ile denetlenir: bu dosyanın kendi yorumları `Kosu(` metnini içeriyor
    ve düz bir tarama kendi metnini yakalardı (B-68'in dersi).
    """
    import ast

    ihlal = {}
    for yol in _dogrulama_modulleri():
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        satirlar = [d.lineno for d in ast.walk(agac)
                    if isinstance(d, ast.Call)
                    and isinstance(d.func, ast.Name) and d.func.id == "Kosu"]
        if satirlar:
            ihlal[yol.name] = satirlar

    assert not ihlal, (
        f"🔴 `dogrulama/` altında ÇIPLAK `Kosu(` çağrısı: {ihlal}\n"
        f"Her ölçüm `dogrulama/olcum.py::olc(...)` üzerinden geçmek zorunda "
        f"(B-106 · `03` Bölüm C sözleşme 5).")


# 🔒 YAZICI KURMAYAN `olc` KULLANICILARI — beyan edilmiş boşluk.
# Liste BÜYÜYEMEZ: yeni bir araç `olc` çağırıyorsa ya `kayit(...)` sarar ya
# bu listeye gerekçesiyle girer. (`karar_kaydi_denetimi.DEVRALINAN_URETICISIZ`
# ile aynı desen: beyan edilmemiş bir boşluk, beyan edilmişten tehlikelidir.)
_YAZICISIZ_MUAF = {
    # Tek seferlik TEŞHİS betikleri: karıştırıcı fazını elle tarayan iki
    # ölçüm. Ürettikleri şey bir sonuç satırı değil, bir faz duyarlılığı
    # eğrisi; `04`teki K-035/K-026 kayıtlarına bağlılar.
    "denetim_b03.py",
    "denetim_b03_sonrasi.py",
    # `olc` çağrıları GÖMÜLÜ betikte ve o betik geçici bir KOPYADA koşuyor;
    # yazılan satır koşu sonunda kopyayla birlikte silinirdi. Aracın çıktısı
    # sonuç satırı değil, mutant/taban karşılaştırma matrisidir.
    "sag_kalan_ayikla.py",
    # 🔴 Koşuları ENSTRUMANLIDIR: üç gözlem sınıfının
    # `__getattribute__`i sarmalanmış hâlde koşar. O koşulardan çıkan
    # satır TEMSİLİ DEĞİLDİR — sonuç dosyasına yazılırsa "bu sayı hangi
    # koddan çıktı" sorusuna YANLIŞ cevap verir.
    "gozlem_tuketim.py",
}


def test_b106_URETIM_YOLLARI_sonuc_YAZIYOR():
    """🔴 `03` B5 — bildirim ≠ kullanım. `olc` var diye satır yazılmıyor.

    `olc()` yazıcıyı `kayit(...)` bağlamından alır. Bir araç bağlamı
    kurmazsa koşar, ölçer ve **hiçbir satır yazmaz** — yani B-106 geri
    gelir, üstelik `olc` kullanıyor göründüğü için fark edilmez.
    """
    import ast

    eksik = []
    for yol in _dogrulama_modulleri():
        kaynak = yol.read_text(encoding="utf-8")
        agac = ast.parse(kaynak)
        # 🔴 TAKMA AD DA SAYILIR. `from ... import olc as _olc` yapıp
        # `_olc(...)` çağıran bir araç, kanonik adı aramayan bir ölçütte
        # GÖRÜNMEZ olurdu — yazıcısız ölçüm yapar ve kimse fark etmez.
        # (Bu delik `dogrulama/gozlem_tuketim.py` yazılırken fark edildi.)
        baglar = {a.asname or a.name
                  for d in ast.walk(agac) if isinstance(d, ast.ImportFrom)
                  for a in d.names if a.name == "olc"}
        olc_cagriyor = any(
            isinstance(d, ast.Call) and isinstance(d.func, ast.Name)
            and d.func.id in baglar for d in ast.walk(agac))
        if not olc_cagriyor:
            continue
        kayit_kuruyor = any(
            isinstance(d, ast.Call) and isinstance(d.func, ast.Name)
            and d.func.id == "kayit" for d in ast.walk(agac))
        if not kayit_kuruyor and yol.name not in _YAZICISIZ_MUAF:
            eksik.append(yol.name)

    assert not eksik, (
        f"🔴 `olc()` çağırıp `kayit(...)` KURMAYAN araç: {eksik}\n"
        f"Ya giriş noktası `with kayit(\"<arac>\"):` ile sarılır, ya araç "
        f"gerekçesiyle `_YAZICISIZ_MUAF`a girer (B-106).")

    # 🔴 Y8 — tarama gerçekten bir şey buluyor mu (boş küme tuzağı)
    sarilan = [y.name for y in _dogrulama_modulleri()
               if "kayit(" in y.read_text(encoding="utf-8")]
    assert len(sarilan) >= 4, (
        f"yalnızca {len(sarilan)} araç yazıcı kuruyor — tarama hedefini "
        f"kaçırıyor olabilir (Y7)")

    # 🔴 Muafiyet listesi BÜYÜYEMEZ: içindeki her ad gerçekten var olmalı,
    # yoksa liste bayatlar ve sessizce genişler.
    mevcut = {y.name for y in _dogrulama_modulleri()}
    hayalet = sorted(_YAZICISIZ_MUAF - mevcut)
    assert not hayalet, f"muafiyet listesinde OLMAYAN dosya: {hayalet}"


def test_b106_olc_YAZICI_verilince_SATIR_yaziyor(tmp_path):
    """🔴 Y10 — sözleşme KIRILABİLİR olmalı: satır gerçekten diske düşüyor mu?

    "Yazıcı kuruldu" demek yetmez; `olc()` onu kullanmıyorsa hiçbir şey
    değişmez. Satır okunur ve `05` §E'nin beş alanı içinde aranır.
    """
    from sim.results import SonucYazici, satirlari_oku
    from dogrulama.olcum import olc
    from dogrulama.aktaricilar import AKTARICILAR
    from sim.config import Konfig

    yol = tmp_path / "deneme.jsonl"
    with SonucYazici(yol) as y:
        olc(Konfig(kol="t", senaryo="S2", tohum=1, isinma_s=5.0,
                   olcum_bitis_s=15.0, kosu_bitis_s=20.0),
            AKTARICILAR["en_kisa_yol"], yazici=y, adim="deneme")

    satirlar = list(satirlari_oku(yol))
    assert len(satirlar) == 1, f"{len(satirlar)} satır yazıldı, 1 bekleniyordu"
    r = satirlar[0]
    assert r["kaynak_hash"]
    assert r["konfig"]["tohum"] == 1
    assert r["korunum"]["korunum_tamam"] is True
    assert r["adim"] == "deneme"
    assert r["metrikler"]["olcum_penceresi_s"] == [5.0, 15.0]

    # 🔴 Y11 — KAPSAM DIŞI VAKA: yazıcı YOKKEN satır yazılmamalı, ve `olc`
    # sessizce çökmemeli. (Birim testler bu yoldan geçiyor.)
    s = olc(Konfig(kol="t", senaryo="S2", tohum=1, isinma_s=5.0,
                   olcum_bitis_s=15.0, kosu_bitis_s=20.0),
            AKTARICILAR["en_kisa_yol"])
    assert s["korunum_tamam"] is True
    assert len(list(satirlari_oku(yol))) == 1, "yazıcısız çağrı satır yazdı"


# ==========================================================================
# 🔴 D-13 (27 Ağustos 2026) — KAPININ Ç1 YOLU SONUÇ SATIRI YAZMIYORDU
#
# Kapı `with kayit("aile0_kapi_raporu"):` içinde koştu ve **13/13** verdi,
# ama `ciktilar/sonuclar/aile0_kapi_raporu.jsonl` **0 BAYT** kaldı: Ç1'in
# 540 koşusu `Pool` alt süreçlerinde çalışıyor ve `spawn` altında işçinin
# `olcum._AKTIF[0]`ı `None`. Yazıcı ebeveynde açık, koşular çocukta.
# `03` Bölüm C sözleşme 5 ihlal edildi ve kapı bunu GÖRMEDİ.
#
# 🔴 ASIL DERS BU: `test_b106_URETIM_YOLLARI_sonuc_YAZIYOR`
# `kapi_korunum`u **GEÇİRİYORDU** — çünkü o test `kayit(...)`ın
# KURULDUĞUNU (AST) doğrular, satırın YAZILDIĞINI değil. Yani
# *"bildirim ≠ kullanım"* bulgusunu kapatan düzeltmenin **kendi koruması**
# aynı tuzağa düştü (K-076 §2: oturumun 12. hatası, sınıfın 3. tekrarı).
#
# 🔒 Bu yüzden aşağıdaki birinci test DAVRANIŞSALDIR ve gerçek `Pool`
# sınırını GEÇER: geçmeseydi D-13'ü yakalayamazdı (Y11 — bir koruma
# yalnızca yakalayabildiği durumla sınanamaz).
# ==========================================================================

def test_d13_HAVUZLU_MATRIS_SATIR_SAYISI_KOSU_SAYISINA_ESIT(tmp_path):
    """🔴 DAVRANIŞSAL — `Pool`un ötesinde satır fiilen diske düşüyor mu?

    Ölçüt tek cümle: **yazılan satır sayısı = koşu sayısı.**
    D-13'te bu oran 0/540'tı ve hiçbir test konuşmadı.

    ⚠️ KAPSAMI (Y11 — koruma kendi sınırıyla birlikte yazılır):
    | vaka                                                | yakalanır mı |
    | yazma ebeveynden İŞÇİYE taşınırsa (spawn → `None`)  | ✅ 0 satır   |
    | `yaz_sonuc` çağrısı tamamen silinirse               | ✅ 0 satır   |
    | havuz atlanıp seri koşulursa                        | ❌ **HAYIR** |
    |   (satır sayısı yine tutar; ama o zaman D-13 de     |              |
    |    doğmazdı — sonraki test delegasyonu denetler)    |              |
    """
    from dogrulama.kapi_korunum import _havuzda_kos, _kosu
    from dogrulama.olcum import kayit
    from sim.results import satirlari_oku

    # Kısa koşu: ölçülen şey satır MUHASEBESİ, fizik değil.
    kisa = dict(isinma_s=5.0, olcum_bitis_s=15.0, kosu_bitis_s=20.0)
    isler = [("S2", "seyrek", t, "en_kisa_yol", kisa) for t in (1, 2)]
    yol = tmp_path / "d13.jsonl"

    with kayit("d13_davranissal", dosya=yol):
        ozetler = _havuzda_kos(isler, matris="deneme")

    satirlar = list(satirlari_oku(yol))
    assert len(satirlar) == len(isler), (
        f"🔴 D-13 GERİ GELDİ: {len(isler)} koşu yapıldı, {len(satirlar)} "
        f"satır yazıldı. `03` Bölüm C sözleşme 5 ihlal ediliyor ve kapı "
        f"bunu göremez.")
    assert len(ozetler) == len(isler), "özet ile satır aynı koşulardan gelmiyor"

    # Satır `05` §E'nin sonuç sözleşmesini taşıyor mu
    r = satirlar[0]
    assert r["kaynak_hash"]
    assert r["korunum"]["korunum_tamam"] is True
    assert r["konfig"]["tohum"] in (1, 2)
    assert r["aktarici"] == "en_kisa_yol"
    assert r["matris"] == "deneme"
    assert r["metrikler"]["olcum_penceresi_s"] == [5.0, 15.0]

    # 🔴 Y8 — YAZAN EBEVEYN, İŞÇİ DEĞİL. İşçi tek başına çağrıldığında
    # (ortamda yazıcı yok) HİÇBİR satır düşmemeli; düşseydi yazma
    # sorumluluğu ikiye bölünmüş olurdu ve `Pool` altında biri sessizce
    # kaybolurdu — D-13'ün tam mekanizması.
    _kosu(isler[0])
    assert len(list(satirlari_oku(yol))) == len(isler), (
        "işçi KENDİ BAŞINA satır yazdı — yazma sorumluluğu ikiye bölünmüş")


def test_d13_matris_giris_noktalari_HAVUZDA_KOS_A_DELEGE_EDIYOR():
    """⚠️ Bu bir KAYNAK DENETİMİDİR, davranış testi değil — etiketi bunu söyler.

    Yukarıdaki test `_havuzda_kos`u doğrular. Ama kapının FİİLEN çağırdığı
    şey `ana_matris` / `uc_durum_matrisi`; biri kendi `Pool`unu kurarsa
    yazma yolu yeniden atlanır ve davranışsal test bunu GÖRMEZ (kendi
    kapsam tablosunda yazılı).

    Gerçek koşuyla denetlemek 540 koşu ya da tam uzunlukta bir koşu
    demekti (~9 sn × 35 mutant ≈ +5 dk kapıya). `08` madde 30: tek bir
    pahalı test, zaman aşımı korumasının öngördüğünden fazla süre ekler.
    Bedeli olmayan ölçüt seçildi ve **ne ölçtüğü yazıldı**.
    """
    import ast as _ast

    kaynak = (KOK / "dogrulama" / "kapi_korunum.py").read_text(encoding="utf-8")
    agac = _ast.parse(kaynak)
    fonksiyonlar = {d.name: d for d in agac.body
                    if isinstance(d, _ast.FunctionDef)}

    for ad in ("ana_matris", "uc_durum_matrisi"):
        fn = fonksiyonlar.get(ad)
        assert fn is not None, f"`{ad}` kayboldu"
        cagrilar = {d.func.id for d in _ast.walk(fn)
                    if isinstance(d, _ast.Call) and isinstance(d.func, _ast.Name)}
        assert "_havuzda_kos" in cagrilar, (
            f"🔴 `{ad}` artık `_havuzda_kos`a delege etmiyor — kendi havuzunu "
            f"kuruyorsa yazma yolu yeniden atlanmış olabilir (D-13).")
        # ⚠️ Y11 — BU KORUMANIN SINIRI (sekizinci denetim, kapsam
        # beyanı): yüklem yalnızca `Name` çağrılarına bakar.
        # `multiprocessing.Pool(...)` (bir `Attribute` çağrısı) ya da
        # `from multiprocessing import Pool as P` bu denetimden
        # SAĞ ÇIKAR. Bulgu değil, beyan edilmemiş bir sınırdı.
        assert "Pool" not in cagrilar, (
            f"🔴 `{ad}` KENDİ `Pool`unu kuruyor; yazma tek yerde olmalı.")

    # 🔴 Y8 — tarama gerçekten bir şey buluyor mu (boş küme tuzağı)
    havuz = fonksiyonlar.get("_havuzda_kos")
    assert havuz is not None and any(
        isinstance(d, _ast.Call) and isinstance(d.func, _ast.Name)
        and d.func.id == "Pool" for d in _ast.walk(havuz)), (
        "`_havuzda_kos` bir `Pool` kurmuyor — tarama hedefini kaçırıyor (Y7)")


# ==========================================================================
# 🔴 D-11 (27 Ağustos 2026) — DEJENERE PAYDA SESSİZ BİR `100.0` ÜRETİYORDU
#
# `08` madde 25'in BAĞLAYICI oranı `kontrol_payi()`den geçiyor ve Aile 1'in
# ilk karşılaştırması ona dayanacak. Ölçüldü (B-105 ölçümünün bir hücresi):
#
#     DV · S2/seyrek/t11 : kontrol_bayt=533 870  veri_bayt=0  teslim=0/1078
#     kontrol_payi()     -> 100.0        (nan değil, hata değil)
#     eşleştirilmiş oran -> 37,8 kat     (tamamen anlamsız)
#
# `03` B2: *"`nan` = ölçüm yok"*. Burada `nan` bile yoktu.
# ==========================================================================

def test_d11_dejenere_payda_TIPLI_reddediliyor():
    """🔴 Veri baytı sıfırken oran bir SAYI olarak dönmemeli."""
    from dogrulama.kontrol_payi import DejenereOlcum, kontrol_payi

    saglam = {"kontrol_bayt": 100, "veri_bayt": 900, "teslim_orani": 0.9}
    assert kontrol_payi(saglam) == pytest.approx(10.0, rel=1e-9)

    dejenere = {"kontrol_bayt": 533870, "veri_bayt": 0, "teslim_orani": 0.0}
    with pytest.raises(DejenereOlcum):
        kontrol_payi(dejenere)

    # 🔴 Y11 — KAPSAM DIŞI VAKA: payda küçük ama SIFIR DEĞİLSE ret YOK.
    # Bu bilinerek böyle; sınır `08` madde 25'in çalışma noktası beyanıyla
    # yönetilir ve burada YAZILI olduğu için sessiz değildir.
    kucuk = {"kontrol_bayt": 999, "veri_bayt": 1, "teslim_orani": 0.001}
    assert kontrol_payi(kucuk) > 99.0


def test_d11_dejenere_hucre_ORANA_girmiyor():
    """🔴 Dejenere hücre orana GİRMEZ ve AYRICA SAYILIR — davranışsal.

    ⚠️ İlk yazımı `ast.unparse(main)` METNİNDE *"dejenere"* arıyordu ve
    mutasyondan (`dejenere.append` → `pass`) **SAĞ ÇIKTI**: değişken adı
    metinde duruyordu. Metin kontrolü, davranış kontrolü değildir —
    deponun B-09/B-89/B-111'de üç kez öğrendiği ders.

    Yüklem `main()`ten ayrıldı ve burada SENTETİK girdiyle sınanıyor:
    tam koşu gerekmiyor.
    """
    from dogrulama.kontrol_payi import eslestirilmis_oranlar

    paylar = {
        ("DV", "S2", 1): 13.71, ("gurultuden_kacan", "S2", 1): 1.65,
        ("DV", "S2", 2): 100.0, ("gurultuden_kacan", "S2", 2): None,
        ("DV", "S0", 1): None, ("gurultuden_kacan", "S0", 1): 1.87,
        ("DV", "S0", 2): 20.0, ("gurultuden_kacan", "S0", 2): 0.0,
    }
    oranlar, dejenere = eslestirilmis_oranlar(
        paylar, senaryolar=("S2", "S0"), tohumlar=(1, 2))

    assert len(oranlar) == 1, (
        f"🔴 {len(oranlar)} oran hesaplandı, 1 bekleniyordu — dejenere "
        f"hücre orana KARIŞTI (D-11)")
    assert oranlar[0] == pytest.approx(13.71 / 1.65, rel=1e-9)
    assert sorted(dejenere) == [("S0", 1), ("S0", 2), ("S2", 2)], (
        f"🔴 dejenere hücreler AYRICA SAYILMIYOR: {dejenere}. Sessizce "
        f"atlanan hücre, aralığın kaç gözlemden çıktığını görünmez yapar "
        f"(`03` B2).")

    # 🔴 Y8 — yüklem sağlam girdide de bir şey üretiyor mu (boş küme tuzağı)
    temiz = {("DV", "S2", 1): 10.0, ("gurultuden_kacan", "S2", 1): 2.0}
    o, d = eslestirilmis_oranlar(temiz, senaryolar=("S2",), tohumlar=(1,))
    assert o == [5.0] and d == []


def test_b106_KANONIK_olc_GOLGELENEMEZ():
    """🔴 Bu test, BU OTURUMDA yapılan bir hatadan doğdu.

    B-106'nın taşımasında `dogrulama/kontrol_payi.py`ye
    `from dogrulama.olcum import olc` eklendi — ama o modülün **kendi
    `def olc()`i vardı** ve içe aktarılanı modül kapsamında GÖLGELEDİ.
    Gölgelenen hâlde fonksiyon kendini çağırıyor ve `TypeError` veriyordu.

    🔴 Hiçbir test görmedi: o fonksiyonu yalnızca `main()` çağırıyor ve
    `main()` test paketinde koşmuyor. `03` kural 15'in tam tarifi —
    *"eşleşmeyen bir `replace` sessizce hiçbir şey yapmaz ve betik yine
    'güncellendi' yazar"*; burada eşleşme TUTTU ve yine de kırıldı.

    Ölçüt: `olc`u içe aktaran hiçbir modül aynı adı yeniden TANIMLAYAMAZ.
    """
    import ast

    ihlal = {}
    for yol in _dogrulama_modulleri():
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        # 🔴 BAĞLANAN AD önemli, içe aktarılan ad değil: `import olc as _olc`
        # kanonik adı bağlamaz ve gölgeleme YARATMAZ. İlk yazım `a.name`e
        # bakıyordu ve güvenli bir takma adı da ihlal sayıyordu (Y5).
        iceri_aktardi = any(
            isinstance(d, ast.ImportFrom)
            and any((a.asname or a.name) == "olc" for a in d.names)
            for d in ast.walk(agac))
        if not iceri_aktardi:
            continue
        yeniden_tanim = [d.name for d in agac.body
                         if isinstance(d, ast.FunctionDef) and d.name == "olc"]
        if yeniden_tanim:
            ihlal[yol.name] = yeniden_tanim

    assert not ihlal, (
        f"🔴 kanonik `olc` GÖLGELENİYOR: {ihlal}\n"
        f"İçe aktarılan ad yeniden tanımlanırsa çağrılar sessizce YEREL "
        f"fonksiyona gider (B-106 · `03` kural 15).")

    # 🔴 Y8 — tarama gerçekten `olc` içe aktaran modül buluyor mu
    aktaran = sum(
        1 for yol in _dogrulama_modulleri()
        if any(isinstance(d, ast.ImportFrom)
               and any((a.asname or a.name) == "olc" for a in d.names)
               for d in ast.walk(ast.parse(yol.read_text(encoding="utf-8")))))
    assert aktaran >= 6, (
        f"yalnızca {aktaran} modül `olc` içe aktarıyor — tarama hedefini "
        f"kaçırıyor olabilir (Y7)")


# ==========================================================================
# 🔴 B-113 (ALTINCI DENETİM) — AYIKLAYICININ KARAR KANALI SATÜREYDİ
#
# B-46/K-051 `sonuc()`e `kaynak_hash` ekledi; hash `sim/` altındaki TÜM
# `.py` içeriğini kapsıyor. Araç ise TAM sonuç sözlüğünü karşılaştırıyordu.
#   ⇒ `sim/` altındaki HER mutasyon `kaynak_hash`i değiştirir
#   ⇒ `esdeger` / `karar_yok` / `yolsuz` dalları ULAŞILAMAZ
#
# Denetçi aracın KENDİ `_kosu`/`_imza`sıyla ölçtü: üç mutantın üçünde de
# tek fark `['kaynak_hash']`. Yayımlanan "7/7 eşdeğer" çıktısı B-46'dan
# BİR GÜN ÖNCEYE ait.
#
# 🔴 Ve onu koruyan `test_b52_*` bir GREP'ti: dalın VARLIĞINI doğruluyordu,
# ULAŞILABİLİRLİĞİNİ değil. Aşağıdaki testler dördünü de ÜRETİYOR.
# ==========================================================================

def _hucre(**alanlar):
    """Bir matris hücresi — `kaynak_hash` her zaman var (B-46'dan beri)."""
    taban = {"kaynak_hash": "AAAA", "ttl_olumu": 0, "teslim_orani": 0.5}
    taban.update(alanlar)
    return taban


def test_b113_kaynak_hash_KARSILASTIRMA_DISI():
    """🔴 Tek farkı `kaynak_hash` olan iki matris AYNI sayılmalı.

    Aksi hâlde `sim/` altındaki her mutasyon "davranış değişti" çıkar ve
    araç hiçbir şey ayıklayamaz — B-113'ün ta kendisi.
    """
    from dogrulama.sag_kalan_ayikla import KARSILASTIRMA_DISI, imza_karsilastir

    assert "kaynak_hash" in KARSILASTIRMA_DISI

    taban = {"ana/S2/orta/1": _hucre()}
    mutant = {"ana/S2/orta/1": _hucre(kaynak_hash="BBBB")}
    assert imza_karsilastir(taban, mutant) == [], (
        "🔴 tek farkı `kaynak_hash` olan matris FARKLI sayıldı — karar "
        "kanalı yine satüre (B-113)")

    # 🔴 Y11 — KAPSAM DIŞI VAKA: GERÇEK bir fark hâlâ görülmeli
    gercek = {"ana/S2/orta/1": _hucre(kaynak_hash="BBBB", ttl_olumu=7)}
    farklar = imza_karsilastir(taban, gercek)
    assert farklar == [("ana/S2/orta/1", ["ttl_olumu"])], farklar

    # `konfig` KASTEN karşılaştırma dışı DEĞİL: mutasyon konfigi
    # değiştiriyorsa bu gerçek bir farktır
    assert "konfig" not in KARSILASTIRMA_DISI


def test_b113_DORT_KARAR_DALININ_DORDU_DE_URETILEBILIYOR():
    """🔴 `03` — tetiklenemeyen bir kontrol, koruma sağlamadan koruma
    İZLENİMİ verir. `test_b52_*` dalın VARLIĞINA bakıyordu; bu test
    dördünü de FİİLEN ÜRETİYOR.
    """
    from dogrulama.sag_kalan_ayikla import YOLSUZ, karar_ver

    # taban: `ttl_olumu` TETİKLENİYOR, `hedef_yok` tetiklenmiyor
    taban = {"ana/S2/orta/1": _hucre(ttl_olumu=5, hedef_yok=0)}

    assert karar_ver([("x", ["ttl_olumu"])], "ttl_olumu", taban) == "degisti"
    assert karar_ver([], YOLSUZ, taban) == "yolsuz"
    assert karar_ver([], "hedef_yok", taban) == "karar_yok"
    assert karar_ver([], "ttl_olumu", taban) == "esdeger"

    # 🔴 Y8 — dördü de AYRI çıktı mı (aynı kovaya düşmediler)
    kararlar = {
        karar_ver([("x", ["ttl_olumu"])], "ttl_olumu", taban),
        karar_ver([], YOLSUZ, taban),
        karar_ver([], "hedef_yok", taban),
        karar_ver([], "ttl_olumu", taban),
    }
    assert len(kararlar) == 4, f"dört dal {len(kararlar)} kovaya düştü: {kararlar}"


def test_b113_ARAC_KENDI_YUKLEMLERINI_kullaniyor():
    """🔴 `03` B5 — bildirim ≠ kullanım.

    Yüklemler ayrılıp test edilse bile `_kosu` onları çağırmıyorsa
    koruma sahtedir: testler geçer, araç yine satüre karar verir.
    """
    import ast

    kaynak = (KOK / "dogrulama" / "sag_kalan_ayikla.py").read_text(
        encoding="utf-8")
    fn = next((d for d in ast.walk(ast.parse(kaynak))
               if isinstance(d, ast.FunctionDef) and d.name == "_kosu"), None)
    assert fn is not None, "_kosu bulunamadı"

    cagrilan = {d.func.id for d in ast.walk(fn)
                if isinstance(d, ast.Call) and isinstance(d.func, ast.Name)}
    for ad in ("imza_karsilastir", "karar_ver"):
        assert ad in cagrilan, (
            f"🔴 `{ad}` TANIMLI ama `_kosu` onu ÇAĞIRMIYOR — karar mantığı "
            f"yine gömülü ve sınanamaz (B-113 · `03` B5)")


# ==========================================================================
# 🔴 B-102 + D-12 — `08` MADDE 22'NİN ÜRETİCİSİ DÜZYAZIYDI
#
# Madde 22 *"DOKUZ alanın hiçbir tüketicisi yok"* diyordu ve üreticisini
# **düzyazıyla** tarif ediyordu: *"`g.<alan>` deseni taraması"*. Bu tarif
# yeniden üretilebilir DEĞİLDİ — 27 Ağustos'ta üç farklı statik okuyuş
# **8 · 9 · 11** verdi, hiçbiri doğru değildi.
#
# Sebep yapısal: `PaketGorunumu.bayt` ile gerçek `Paket.bayt`,
# `Gozlem.kuyruk_kapasitesi` ile `Konfig.kuyruk_kapasitesi` **aynı adı
# taşıyor.** İsimden tüketici çıkarmak bir TAHMİNDİR (`03` kural 1).
#
# 🔒 Ölçüt artık ÇALIŞMA ANI: `dogrulama/gozlem_tuketim.py` üç sınıfın
# `__getattribute__`ini sarmalayıp 20 tam koşuda hangi alanın OKUNDUĞUNU
# kaydediyor. Ölçülen: **14** (Gozlem 9 · KomsuKaydi 1 · PaketGorunumu 4).
#
# ⚖️ **Altıncı denetimin bir iddiası ÇÜRÜDÜ:** B-102 `duyulan_beacon`ı da
# tüketicisiz saymıştı; çalışma anında OKUNUYOR.
# 🔴 **Ve ikisinin de kaçırdığı bir boşluk çıktı (D-12):** `PaketGorunumu`nun
# beş alanından DÖRDÜ taşınıyor ama hiç okunmuyor.
#
# ⚠️ Bu test ÖLÇÜMÜ KOŞTURMAZ (20 tam koşu, pakete ~5 dk eklerdi — Y12'nin
# öteki yüzü). Beyanı `08` ile ARACIN kendi listesi arasında bağlar; ölçüm
# `python dogrulama/gozlem_tuketim.py` ile ayrıca tazelenir.
# ==========================================================================

def test_b102_madde22_ARACIN_BEYANIYLA_ayni():
    """🔴 `08` madde 22, aracın ölçülmüş listesini BİREBİR taşımalı.

    İkisi ayrışırsa `08` bir sayı iddia ediyor ve o sayının üreticisi başka
    bir şey söylüyor demektir — B-57'nin kapatmaya çalıştığı sınıf.
    """
    import re

    from dogrulama.gozlem_tuketim import HIC_OKUNMAYAN

    beklenen = sorted(a for kume in HIC_OKUNMAYAN.values() for a in kume)
    assert len(beklenen) == 14, (
        f"aracın beyanı {len(beklenen)} alan taşıyor — ölçüm değiştiyse "
        f"`08` madde 22 de güncellenmeli (Y14)")

    kapsam = (KOK / "v2" / "08-AILE0-KAPSAM.md").read_text(encoding="utf-8")
    madde = kapsam.split("| **22** |", 1)[1].split("\n| **23**", 1)[0]

    # 🔴 ÖLÇÜT BEYAN BÖLGESİ, TÜM HÜCRE DEĞİL.
    # Maddenin anlatı kısmı ÇÜRÜTÜLEN bir iddiayı kaydediyor
    # (`duyulan_beacon` tüketicisiz SANILMIŞTI) ve o adı anmak zorunda.
    # Tüm hücreye bakan bir ölçüt, kaydı silmeye zorlardı — oysa bu depoda
    # çürütülen bir iddia SİLİNMEZ, revizyonla düzeltilir (K-053).
    beyan = madde.split("**Üretici:**", 1)[0]
    assert "HİÇ OKUNMUYOR" in beyan, "beyan bölgesi bulunamadı — ölçüt bozuk"

    eksik = [a for a in beklenen if f"`{a}`" not in beyan]
    assert not eksik, (
        f"🔴 `08` madde 22 şu alanları ANMIYOR: {eksik}. Araç onları "
        f"'hiç okunmayan' diye ölçüyor (B-102 · D-12).")

    # 🔴 Y11 — TERS YÖN: `08` aracın ölçmediği bir alanı SAYMAMALI.
    # Aksi hâlde madde şişer ve bir alan okunmaya başladığında kimse fark
    # etmez (`duyulan_beacon` tam olarak böyle yanlış sayılmıştı).
    from sim.gozlem import (
        IZINLI_GOZLEM_ALANLARI, IZINLI_KOMSU_ALANLARI, IZINLI_PAKET_ALANLARI,
    )
    tum = (set(IZINLI_GOZLEM_ALANLARI) | set(IZINLI_KOMSU_ALANLARI)
           | set(IZINLI_PAKET_ALANLARI))
    okunanlar = sorted(tum - set(beklenen))
    fazla = [a for a in okunanlar if re.search(rf"`{re.escape(a)}`", beyan)]
    assert not fazla, (
        f"🔴 `08` madde 22 OKUNAN alanları da sayıyor: {fazla}. Araç onları "
        f"tüketiciSİ VAR diye ölçüyor — beyan şişmiş (B-102).")

    # 🔴 Y8 — madde gerçekten bir SAYI iddia ediyor mu (boş metin tuzağı)
    assert re.search(r"ON\s?DÖRT|\*\*14\*\*", beyan), (
        "madde 22 bir toplam sayı beyan etmiyor — 'kaç alan' sorusu "
        "cevapsız kalır")


def test_b102_araci_SUREYI_bozmadan_geri_aliyor():
    """🔴 Y7 — bir doğrulama aracı, ölçtüğü şeyi BOZAMAZ.

    `gozlem_tuketim` üç sınıfın `__getattribute__`ini sarmalıyor. Geri
    alınmazsa paketin geri kalanı sarmalanmış sınıflarla koşar ve hem
    yavaşlar hem ölçülemez hâle gelir.
    """
    import sim.gozlem as G
    from dogrulama import gozlem_tuketim  # noqa: F401  (içe aktarım yeter)

    for sinif in (G.Gozlem, G.KomsuKaydi, G.PaketGorunumu):
        assert sinif.__getattribute__ is object.__getattribute__, (
            f"🔴 {sinif.__name__}.__getattribute__ SARMALANMIŞ kalmış — "
            f"araç kendi izini temizlemiyor (Y7)")


# ==========================================================================
# 🔴 B-137 · B-139 (YEDİNCİ BAĞIMSIZ DENETİM) — İKİ BEYAN, İKİ UCUZ KORUMA
#
# Y12: *"elle tutulan her kapı sabiti ucuz bir testle korunur; yalnızca
# pahalı bir koşuda konuşan koruma pratikte susuyordur."*
#
# İkisi de aynı sınıftan: bir kural **yorumda** yazılıydı ve hiçbir şey
# onu zorlamıyordu — `03` B5'in *"bildirim ≠ kullanım"* deseni.
# ==========================================================================

def test_b137_kayit_dosya_parametresi_URETIMDE_kullanilmiyor():
    """🔴 B-137 — `kayit(dosya=…)` YALNIZCA testler içindir.

    `dogrulama/olcum.py`de bu kural bir **yorumda** yazılıydı:
    *"üretim aracı bu parametreyi HİÇ vermez"*. Onu zorlayan hiçbir şey
    yoktu. Bir üretim aracı `dosya=` verirse sonuç satırı
    `ciktilar/sonuclar/` DIŞINA düşer ve `03` Bölüm C sözleşme 5 sessizce
    ihlal edilir — D-13'ün tam olarak yaptığı şey.
    """
    import ast

    ihlal = {}
    for yol in _dogrulama_modulleri():
        agac = ast.parse(yol.read_text(encoding="utf-8"))
        satirlar = [d.lineno for d in ast.walk(agac)
                    if isinstance(d, ast.Call)
                    and isinstance(d.func, ast.Name) and d.func.id == "kayit"
                    and any(k.arg == "dosya" for k in d.keywords)]
        if satirlar:
            ihlal[yol.name] = satirlar

    assert not ihlal, (
        f"🔴 üretim aracı `kayit(dosya=…)` kullanıyor: {ihlal}\n"
        f"O parametre yalnızca testler içindir; üretim satırı "
        f"`ciktilar/sonuclar/` altına düşmek zorunda (sözleşme 5).")

    # 🔴 Y8 — tarama gerçekten bir şey buluyor mu (boş küme tuzağı)
    kayit_kuran = [y.name for y in _dogrulama_modulleri()
                   if "kayit(" in y.read_text(encoding="utf-8")]
    assert len(kayit_kuran) >= 4, (
        f"yalnızca {len(kayit_kuran)} araç `kayit(` çağırıyor — tarama "
        f"hedefini kaçırıyor olabilir (Y7)")


def test_b139_kor_havuz_sayisi_08_ILE_AYNI():
    """🔴 B-139 — `08`in *"N mutant hiç sınanmadı"* satırı İKİ KEZ bayatladı.

    Kör havuz **koddan üretilir ve kodla büyür**: 185 → 203 → 253 → 255.
    `08` md 30 o sayıyı **elle** taşıyor ve `sim/` her değiştiğinde
    bayatlıyor. Bu test, sabiti ölçülen havuzla bağlar.

    ⚠️ Ölçüt: `08`in yazdığı *"sınanmamış"* sayısı = havuz −
    `kor_mutasyon.VARSAYILAN_ORNEKLEM`. 🔴 **B-151:** burada `24` yazılıydı
    ve o sayı kodda YOKTU (araç varsayılanı **16**); tek kaynağı bayat bir
    çıktı dosyasıydı.
    """
    import re

    from dogrulama.kor_mutasyon import VARSAYILAN_ORNEKLEM, mutantlari_uret

    havuz = len(mutantlari_uret())
    # 🔴 B-151 (sekizinci denetim) — ÖRNEKLEM ARTIK KODDAN.
    # Burada `ORNEKLEM = 24` yazıyordu ve o sayı `kor_mutasyon.py`de
    # YOKTU (aracın varsayılanı 16). 24'ün tek kaynağı, başlığında
    # *"🔴 DURUM: BAYAT … Bir sayıyı buradan OKUMA"* yazan
    # `ciktilar/kor_cikti.txt` idi. Yani BAYATLAMAYI ÖNLEMEK için
    # yazılan bu Y12 koruması, ikinci bir elle tutulan sabit getirmişti.
    beklenen = havuz - VARSAYILAN_ORNEKLEM

    metin = (KOK / "v2" / "08-AILE0-KAPSAM.md").read_text(encoding="utf-8")
    bulunan = re.findall(r"\*\*(\d+) mutant hiç sınanmadı\*\*", metin)
    assert bulunan, (
        "`08`de *'N mutant hiç sınanmadı'* satırı bulunamadı — beyan "
        "kaybolmuş olabilir")
    yazili = {int(x) for x in bulunan}
    assert yazili == {beklenen}, (
        f"🔴 `08` **{sorted(yazili)}** diyor, ölçülen **{beklenen}** "
        f"(havuz {havuz} − örneklem {VARSAYILAN_ORNEKLEM}).\n"
        f"Kör havuz koddan üretilir ve `sim/` her değiştiğinde büyür; "
        f"bu satır bu depoda İKİ KEZ bayatladı (B-114, B-139).\n"
        f"Üretici: python -c \"import sys;sys.path.insert(0,'.');"
        f"from dogrulama.kor_mutasyon import mutantlari_uret;"
        f"print(len(mutantlari_uret()))\"")


# ==========================================================================
# 🔴 B-149 · B-150 (SEKİZİNCİ DENETİM) — MUTASYON PAKETİNİN İKİ KOD YOLU
# ==========================================================================

def test_b149_MUTASYON_bloklari_MAIN_korumasinin_USTUNDE():
    """🔴 B-149 — paket iki farklı sayıyla koşuyordu.

    Altı yeni mutasyon `if __name__ == "__main__": main()` bloğunun
    **ALTINA** eklenmişti. Ölçüldü (AST ile, modül gövdesi koruma
    düğümüne kadar çalıştırılarak):

        içe aktarma yolu (kapının yolu)  : 41  ✅
        betik yolu (belgelenmiş komut)   : 35  🔴

    ve `python dogrulama/mutasyon_paketi.py` `✅ Ç1.3 GEÇTİ — 35/35`
    basıp çıkış kodu **0** veriyordu.

    🔒 Bu test **metne değil YAPIYA** bakar (AST): koruma modül
    gövdesinin **son düğümü** olmak zorunda. Yeni bir `MUTASYONLAR += [`
    altına eklenirse bu yüklem kırılır.
    """
    kaynak = (KOK / "dogrulama" / "mutasyon_paketi.py").read_text(
        encoding="utf-8")
    agac = ast.parse(kaynak)
    koruma = [i for i, n in enumerate(agac.body)
              if isinstance(n, ast.If) and isinstance(n.test, ast.Compare)
              and isinstance(n.test.left, ast.Name)
              and n.test.left.id == "__name__"]
    assert len(koruma) == 1, f"`__main__` koruması {len(koruma)} kez"
    assert koruma[0] == len(agac.body) - 1, (
        f"🔴 `__main__` koruması modül gövdesinin SONUNDA değil "
        f"({koruma[0] + 1}/{len(agac.body)}). Altında kalan her düğüm "
        f"BETİK yolunda çalışmaz; `main()` eksik listeyle koşar (B-149).")


def test_b149_main_BEKLENEN_MUTASYONU_denetliyor():
    """🔴 B-149 (Y7) — araç NE KOŞTUĞUNU kendisi doğrular.

    `main()` `BEKLENEN_MUTASYON`u hiç okumuyordu; o kontrol yalnızca
    `aile0_kapi_raporu.py`deydi. Yani betik yolu eksik listeyle koşup
    *"GEÇTİ"* diyebiliyordu — kapının yolu değil ama **aracın kendi
    belgelenmiş komutu** buydu.
    """
    from dogrulama.mutasyon_paketi import MUTASYONLAR, liste_dogrula

    # 🔴 DAVRANIŞSAL, metin değil. İlk yazımda bu test `main()` gövdesinde
    # `BEKLENEN_MUTASYON` ADININ geçtiğini sınıyordu ve kontrolü
    # `if False:` yapan bir mutasyonu YAKALAYAMADI — ad, hata METNİNDE
    # duruyordu. `03` B5'in "bildirim ≠ kullanım" tuzağı, korumanın
    # kendisinde. (Y11: koruma kendi sınırıyla birlikte yazılır.)
    assert liste_dogrula() is None, (
        "bugünkü liste kapının beklediğiyle uyuşmuyor")
    assert liste_dogrula(len(MUTASYONLAR) - 6) is not None, (
        "🔴 liste 6 EKSİKken yüklem hiçbir şey söylemiyor — B-149'un "
        "birebir vakası (betik yolu 35, kapı 41)")
    assert liste_dogrula(0) is not None, "boş liste de reddedilmeli (Y7)"


def test_b150_mutasyon_NUMARALARI_tekil():
    """🔴 B-150 — `D26` `D27` `D28` İKİŞER mutasyon adlandırıyordu.

    Tam adlar benzersiz olduğu için araç çalışıyordu, ama karar
    kayıtlarındaki *"D26"* göndermesi artık **tekil değildi**: bir
    okuyucu `D26`yı arayınca iki farklı dosyada iki farklı mutasyon
    buluyordu (`radio.py` ↔ `karsilastirma.py`).
    """
    import re

    from dogrulama.mutasyon_paketi import MUTASYONLAR

    numara = {}
    for m in MUTASYONLAR:
        k = re.match(r"^([A-Z]+\d+)", m.ad)
        assert k, f"mutasyon adı numarayla başlamıyor: {m.ad}"
        numara.setdefault(k.group(1), []).append(m.ad)
    cakisan = {k: v for k, v in numara.items() if len(v) > 1}
    assert not cakisan, (
        f"🔴 mutasyon numarası TEKİL DEĞİL: {cakisan}. Kayıtlardaki "
        f"gönderme belirsizleşir (B-150).")
