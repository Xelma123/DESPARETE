"""
TEK KANONİK ÖLÇÜM YOLU — `03` Bölüm C sözleşme 5.

🔴 NEDEN BU DOSYA VAR — B-106 (ALTINCI DENETİM)
===============================================
`03` Bölüm C: *"Her sonuç KENDİ TAM KONFİGÜRASYONUYLA saklanır"* ve
*"her satır ANINDA diske yazılır"*. Sözleşmeyi karşılayacak sınıf
(`sim/results.py::SonucYazici`) **yazılmış, belgelenmiş, test edilmiş —
ve HİÇ ÇAĞRILMAMIŞTI.**

Altıncı denetim ölçtü: `SonucYazici`nin geçtiği tüm yerler —

    sim/results.py            tanım
    sim/__init__.py           dışa aktarım
    tests/test_results.py     TEK kullanıcı (3 birim testi)
    dogrulama/sag_kalan_ayikla.py:191   bir YORUM

`dogrulama/` altındaki **hiçbir** ölçüm aracı sonuç yazmıyordu: ne kapı
raporu, ne korunum matrisi, ne kalibrasyon, ne mekanizma kapısı, ne
kontrol payı, ne Li. `03` B5'in *"bildirim ≠ kullanım"* tuzağının
**dördüncü** örneğiydi (öncekiler: `UYGULANMAMIS_BAYRAKLAR` ·
`rng.HENUZ_KULLANILMAYAN` · B-27b).

🔒 KARAR (öğrenci, 27 Ağustos 2026)
====================================
> *"`SonucYazici` üretim yolunun ZORUNLU parçası. Bugün kullanılmaması
> tasarım tercihi değil, EKSİK BAĞLANTI. 9 `Kosu()` çağrı yerini tek
> kanonik `olc(...)` yoluna taşı."*

⚠️ Ölçüldü: `dogrulama/` altında **9 değil, 11** `Kosu(` çağrı yeri var
(8 dosya; ikisi `sag_kalan_ayikla.py`nin gömülü betiğinde). Kararın kapsamı
değişmedi; 11'i de bu yoldan geçiyor.

🔴 NEDEN YAZICI `olc()` İÇİNDE KURULMUYOR
==========================================
Kurulsaydı, testler de dosya yazardı: `tests/` altında `dogrulama/`
araçlarını çağıran testler var ve her koşu `ciktilar/` altına satır
düşürürdü — depoyu kirletir, mutant kopyalarında gereksiz G/Ç yapar ve
`ciktilar/CIKTILAR.md`nin *"bir çıktı dosyası tarihini ve kod durumunu
taşımıyorsa silinir"* politikasını (B-64) yönetilemez hâle getirirdi.

Bunun yerine: **yazıcıyı araçların `main()`i kurar**, `olc()` yalnızca
verilirse yazar. *"Üretim yolunun zorunlu parçası"* şartını zorlayan şey
bir varsayılan değil, iki ucuz test:

    tests/test_kapi_secimleri.py::test_b106_dogrulama_altinda_CIPLAK_Kosu_YOK
    tests/test_kapi_secimleri.py::test_b106_araclarin_main_i_SONUC_YAZIYOR

⚠️ KAPSAMI (Y11 — koruma kendi sınırıyla birlikte yazılır):
| vaka                                                  | yakalanır mı |
| `dogrulama/` altında `Kosu(` doğrudan çağrılması      | ✅ evet      |
| bir aracın `main()`inde yazıcı kurulmaması            | ✅ evet      |
| 🔴 yazıcının kurulup `olc()`e GEÇİRİLMEMESİ           | ✅ evet      |
| 🔴 `tests/` altında doğrudan `Kosu(` kullanımı        | ❌ **HAYIR** |
|    (kasten: birim testler tek koşuyu izole ölçer)     |              |
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

KOK = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(KOK))

from sim.config import Konfig                                    # noqa: E402
from sim.kosucu import Kosu                                      # noqa: E402
from sim.results import SonucYazici                              # noqa: E402

# Sonuç satırları buraya düşer. `ciktilar/CIKTILAR.md` politikası: bir çıktı
# üretildiği koşunun kod durumunu taşımak zorunda — `SonucYazici` her satıra
# `kaynak_hash` yazdığı için politika satır düzeyinde sağlanıyor.
SONUC_DIZINI = KOK / "ciktilar" / "sonuclar"

# `konfig` ve `korunum` ayrı alanlara gider; `metrikler`de tekrarlanmazlar.
_AYRI_ALANLAR = ("konfig", "korunum")


def yazici_ac(arac: str) -> SonucYazici:
    """Bir aracın sonuç dosyasını açar: `ciktilar/sonuclar/<arac>.jsonl`."""
    return SonucYazici(SONUC_DIZINI / f"{arac}.jsonl")


# 🔴 ETKİN YAZICI — araçlar `main()`lerini `with kayit("<arac>"):` ile sarar.
#
# Alternatif, `yazici`yi her çağrı zincirinden geçirmekti; reddedildi çünkü
# `mekanizma_kapisi._kos` gibi iki katman aşağıdaki yardımcılara kadar imza
# değiştirmek gerekiyordu ve her imza bir sessiz atlama fırsatıdır. Bağlam
# yöneticisi tek satırlık ve **atlanması AST ile görülebilir**.
_AKTIF: list[SonucYazici | None] = [None]


class kayit:
    """`with kayit("arac"):` — blok içindeki HER `olc()` satırını yazar.

    ⚠️ Yeniden girilebilir DEĞİLDİR ve olmasına gerek yok: bir araç kendi
    `main()`ini bir kez sarar. İç içe kullanım sessizce dıştakini gölgelerdi,
    bu yüzden açıkça reddedilir.
    """

    def __init__(self, arac: str, *, dosya: "Path | None" = None) -> None:
        self.arac = arac
        # 🔴 `dosya` YALNIZCA TESTLER İÇİNDİR ve üretim yolunu değiştirmez.
        # Neden gerekli: D-13'ün koruması DAVRANIŞSAL olmak zorunda —
        # gerçek `Pool` sınırını geçip satırların düştüğünü görmeli. Ama
        # `ciktilar/sonuclar/` altına yazan bir test, `ciktilar/CIKTILAR.md`
        # politikasını ("bir çıktı üretildiği koşunun kod durumunu taşımak
        # zorunda") yönetilemez hâle getirirdi. Test kendi `tmp_path`ine
        # yazar; üretim aracı bu parametreyi HİÇ vermez.
        self.dosya = dosya
        self.yazici: SonucYazici | None = None

    def __enter__(self) -> SonucYazici:
        if _AKTIF[0] is not None:
            raise RuntimeError(
                "iç içe `kayit(...)` — dıştaki yazıcı sessizce gölgelenirdi")
        self.yazici = (SonucYazici(self.dosya) if self.dosya is not None
                       else yazici_ac(self.arac))
        _AKTIF[0] = self.yazici
        return self.yazici

    def __exit__(self, *_: object) -> None:
        _AKTIF[0] = None
        if self.yazici is not None:
            self.yazici.kapat()


def aktif_yazici() -> SonucYazici | None:
    """O an etkin olan yazıcı, ya da `None`.

    🔴 Neden var: bir aracın *"satır yazmam BEKLENİYOR mu"* sorusunu
    sorabilmesi için. D-13'ün gözden kaçma sebebi, hiç kimsenin bunu
    sormamasıydı — yazıcı yoktu, `olc()` sessizce geçti, kapı 13/13 dedi.
    Yazıcı beklenen bir yolda `yazilan == len(isler)` iddiası ancak bu
    ayrım yapılabilirse kurulabilir (birim testlerde yazıcı YOKTUR ve
    orada böyle bir iddia yanlış olurdu).
    """
    return _AKTIF[0]


def yaz_sonuc(sonuc: dict, *, yazici: SonucYazici | None = None,
              **etiketler: Any) -> bool:
    """🔒 SONUÇ SATIRINI YAZAN TEK YER. `olc()` de buradan geçer.

    🔴 NEDEN AYRI BİR FONKSİYON — D-13
    ===================================
    `Pool` kullanan bir ölçüm aracında koşu ALT SÜREÇTE, yazıcı ise
    EBEVEYNDE yaşar: `SonucYazici` açık bir dosya tanıtıcısı taşır,
    picklenemez, işçiye geçirilemez. `spawn` altında işçinin `_AKTIF[0]`ı
    `None`dır ve `olc()` sessizce HİÇBİR ŞEY YAZMAZ — `kapi_korunum`un
    540 koşusu tam olarak böyle kayboldu (D-13: `aile0_kapi_raporu.jsonl`
    = **0 bayt**, ve kapı yine 13/13 dedi).

    🔒 Doğru şekil: **işçi tam `sonuc` sözlüğünü DÖNDÜRÜR, ebeveyn yazar.**
    O ebeveynin elinde `olc()` yoktur — elinde yalnızca sonuç vardır. Bu
    fonksiyon o adımı kanonik yapar; olmasaydı her araç `_AYRI_ALANLAR`
    filtresini kendi kopyalardı ve `olcum.py` değiştiğinde sessizce
    ayrışırdı (B-07'nin "ikinci doğru kaynağı" tuzağı —
    `literatur_eksenleri.py` bu yüzden filtreyi kopyalamayıp içe aktarıyordu).

    Yazıcı yoksa (birim testler) **hiçbir şey yazılmaz** ve `False` döner;
    dönüş değeri var ki çağıran "yazıldı mı" sorusunu ÖLÇEBİLSİN — D-13'ün
    gözden kaçma sebebi tam olarak bu sorunun hiç sorulmamasıydı.
    """
    yazici = yazici if yazici is not None else _AKTIF[0]
    if yazici is None:
        return False
    yazici.yaz(
        konfig_sozluk=sonuc["konfig"],
        korunum=sonuc["korunum"],
        metrikler={a: d for a, d in sonuc.items() if a not in _AYRI_ALANLAR},
        **etiketler,
    )
    return True


def olc(kon: Konfig, fabrika, *, yazici: SonucYazici | None = None,
        hazirla=None, **etiketler: Any) -> dict:
    """🔒 TEK KANONİK ÖLÇÜM. `dogrulama/` altındaki her koşu buradan geçer.

    `yazici` verilirse satır **anında** diske yazılır ve `fsync` edilir —
    uzun bir matris yarıda kesilse bile tamamlanan koşular kaybolmaz
    (`03` Bölüm C, `results.py`nin ikinci kuralı).

    `etiketler` satıra olduğu gibi eklenir (ör. `kol="DV"`, `adim="taban"`)
    — hangi ölçümün hangi satır olduğu sonradan sorulabilsin diye.

    🔴 `hazirla(kosu)` — KOŞMADAN ÖNCE KOŞUYU DEĞİŞTİREN TEK MEŞRU KAPI.
    Bugün **iki** kullanıcısı var ve ikisi de karıştırıcı FAZINI elle
    sabitleyen teşhis betikleri (`denetim_b03.py`, `denetim_b03_sonrasi.py`):
    faz normalde kendi akışından çekilir, o iki ölçüm ise fazı taramak için
    onu geçersiz kılmak zorunda.

    ⚠️ Bu bir KÂHİN kapısıdır ve `dogrulama/` altında olduğu için meşrudur
    (`aktaricilar.py` de kâhindir). 🔴 Bir PROTOKOLE bu kapıdan geçilemez —
    B-68'in kapattığı sızıntı tam olarak buydu: bir fabrikanın `__dict__`ine
    `Kosu` enjekte edilirse protokol `topo`, `karistirici` ve
    `bag_gercek_per`e ulaşır (`03` kural 5).
    """
    kosu = Kosu(kon, fabrika)
    if hazirla is not None:
        hazirla(kosu)
    sonuc = kosu.kostur()
    yaz_sonuc(sonuc, yazici=yazici, **etiketler)
    return sonuc
