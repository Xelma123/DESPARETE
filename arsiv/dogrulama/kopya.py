"""
DEPO KOPYALAMA — TEK KAYNAK.

🔴 NEDEN BU DOSYA VAR — B-100 (ALTINCI DENETİM, 26 Ağustos 2026)
================================================================
`dogrulama/` altındaki dört araç, ölçüm yapmak için depoyu geçici bir
dizine kopyalar. Kopyalama kuralı **altı ayrı yere elle yazılmıştı** ve
altısı da `"v2"`yi dışlıyordu:

    mutasyon_paketi.py:458  (_kosu)          mutasyon_on_kontrol.py:86
    mutasyon_paketi.py:688  (taban_kontrolu) kor_mutasyon.py:120, 165
                                             sag_kalan_ayikla.py:283

26 Ağustos oturumu `v2/` altındaki iki belgeyi okuyan **üç test** yazdı:

    test_b57_yeni_karar_kaydi_URETICI_satiri_TASIMAK_ZORUNDA  -> v2/04
    test_b57_URETICILI_bir_kayit_muafiyet_listesinde_OLAMAZ   -> v2/04
    test_b93_sim_altindaki_ASSERT_sayisi_BEYANLA_ayni         -> v2/08

Depoda **45/45 geçiyorlar**; `v2`siz bir kopyada **3'ü de** `FileNotFoundError`
alıyor. Ölçüldü (altıncı denetim ve devralan oturum, ikisi de bağımsız):

    depoda            : 45 passed in 15,5 sn
    v2'siz kopyada    : 3 failed, 42 passed in 16,8 sn

`mutasyon_paketi.paketi_kostur()` taban kırıkken **erken döner**; kapı
Ç1.3'ü `!!TABAN` yazar ve **kapanmaz.** Yani bu tek satırlık dışlama,
150 dakikalık kapıyı düşürüyordu.

🔴 VE UCUZ ÖN KONTROL BUNU YAPISAL OLARAK GÖREMEZ: `mutasyon_on_kontrol`
her mutantı `-k <beklenen_test>` ile koşar, bu üç test hiç toplanmaz.
Bu, deponun *"ön kontrol geçti, kapı düştü"* vakasının **DÖRDÜNCÜSÜDÜR**
(K-042 · K-046 · K-058) — ve ilk kez **koşmadan önce** görüldü.

🔴 İKİNCİ KUSUR — TABAN İLE MUTANTLAR AYNI ORTAMDA KOŞMUYORDU (Y7)
==================================================================
Altı listeden **beşi** `"*.txt"`i dışlıyordu, `mutasyon_paketi._kosu`
dışlamıyordu. Yani `taban_kontrolu()` bir dosya kümesini, mutantlar
**başka** bir dosya kümesini görüyordu. Bir doğrulama aracı **ne koştuğunu
kendisi doğrulamak zorundadır** (Y7) — iki farklı ortamda koşan bir
karşılaştırma bunu yapamaz.

Ölçüldü: `tests/` ve `dogrulama/` altında `.txt` okuyan **hiçbir kod yok**,
yani dışlama davranışı değiştirmiyor; değiştirdiği tek şey **tutarlılık**.

🔒 KURAL — Y12'NİN BU DOSYADAKİ HÂLİ
====================================
Depoyu kopyalamayı bilen **tek yer burasıdır.** `dogrulama/` altında
başka bir `shutil.ignore_patterns(` çağrısı **olamaz**; bunu ucuz bir
test AST ile zorlar:

    tests/test_kapi_secimleri.py::test_b100_KOPYA_KURALI_TEK_KAYNAKTA

Sebep basit ve ölçülmüştür: altı kopya vardı, biri ayrıştı ve **kimse fark
etmedi**. Yedincisi de ayrışırdı.

⚠️ KAPSAMI (Y11 — koruma kendi sınırıyla birlikte yazılır):
| vaka                                              | yakalanır mı |
| `dogrulama/` altında yeni bir `ignore_patterns(`  | ✅ evet      |
| `KOPYA_DISLAMA`ya `"v2"` geri konması             | ✅ evet      |
| 🔴 `tests/` altında yazılan bir kopyalama         | ❌ **HAYIR** |
| 🔴 `copytree`siz elle kurulan bir kopya           | ❌ **HAYIR** |
"""

from __future__ import annotations

import shutil
from pathlib import Path

KOK = Path(__file__).resolve().parent.parent

# 🔴 B-100 — `"v2"` BU LİSTEDE DEĞİLDİR VE OLAMAZ.
# `v2/` altındaki belgeleri okuyan testler var; onlarsız bir kopyada taban
# kırılır ve kapı YANLIŞ SEBEPLE düşer (K-058'in birebir sınıfı).
KOPYA_DISLAMA: tuple[str, ...] = (
    "__pycache__",
    ".pytest_cache",
    "*.pyc",
    ".git",
    "*.txt",
)


def depoyu_kopyala(hedef: Path) -> Path:
    """Depoyu `hedef`e kopyalar ve `hedef`i döndürür.

    Tüm ölçüm araçları bunu çağırır — kopyalama kuralının tek uygulaması.
    """
    shutil.copytree(KOK, hedef,
                    ignore=shutil.ignore_patterns(*KOPYA_DISLAMA))
    return hedef
