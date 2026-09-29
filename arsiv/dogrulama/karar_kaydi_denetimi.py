# -*- coding: utf-8 -*-
"""KARAR KAYDI DENETİMİ — `04`teki her ÖLÇÜM bir üreticiye bağlı mı? (B-57)

==========================================================================
🔴 NEDEN BU DOSYA VAR

`03` kural 1: *"Ölçülmemiş bir şeyi ölçülmüş gibi sunma. Her sayının yanında
**üretici komut** ve **kaynak dosya** yazılır."*

B-57 üç denetim boyunca açık kaldı ve sayısı **ÜÇ KEZ yanlış ölçüldü**
(21 Ağu "55'in 25'i" · 25 Ağu "56'nın 18'i" · 25 Ağu "57'nin 13'ü").
Dördüncü denetim (B-74) taramayı sıkılaştırdı ve **"60 kayıt · 23 üretici ·
37 eksik"** dedi; beşinci denetim bunu doğruladı.

🔴 26 AĞUSTOS 2026 — DÖRDÜNCÜ KEZ YANLIŞ ÖLÇÜLDÜĞÜ BULUNDU (K-069).

O taramanın SAYI dedektörü `%\\d|\\d+,\\d|\\b\\d{3,}\\b` idi. Üçüncü
şıkkı — **çıplak üç haneli tamsayı** — şunları da "sayı" sayıyordu:

    2026      → TARİH            (her kayıtta var)
    K-004     → ÇAPRAZ ATIF
    802.11    → STANDART ADI
    1000–1029 → TOHUM KÜMESİ ADI

⚖️ Bu, **B-74'ün açıldığı sınıfın ÖTEKİ YÜZÜ**: B-74 *"üretici"* kelimesini
prozada sayan gevşek taramayı yakalamıştı; burada gevşek olan **sayı**
dedektörüydü. Ölçüldü: dokuz kayıt (K-001 · K-002 · K-003 · K-007 · K-009 ·
K-010 · K-012 · K-016 · K-029) yalnızca **tarih ve çapraz atıf** yüzünden
sayılıyordu. Dokuzu da tek tek okundu; **ölçüm taşımıyorlar.**

    GEVŞEK ölçüt : 68 kayıt · 37 üreticisiz
    SIKI  ölçüt  : 58 ölçüm taşıyan · **28** üreticisiz

🔴 VE BİR ŞEY DAHA ÖLÇÜLDÜ — İLK YAZIMDAKİ ELEME FİLTRELERİ ÖLÜYDÜ.

Bu aracın ilk hâlinde altı "eleme" deseni vardı (yıl · atıf · standart ·
tohum kümesi …) ve gerekçesi *"bunları metinden çıkarıyoruz"* idi. Altısı da
tek tek ve topluca kaldırıldı: **sonuç DEĞİŞMEDİ (58 / 28).**

Sebebi yapısal: sıkı ölçüt **OLUMLU** bir desendir — yüzde, ondalık, oran ya
da **BİRİMLİ** büyüklük ister. `2026`, `802`, `004` bunların hiçbiri değildir
ve zaten eşleşmezler. Eleme filtreleri hiçbir şey elemiyordu.

⚖️ Deponun kendi kuralı uygulandı: *"tetiklenemeyen bir kontrol, koruma
sağlamadan koruma İZLENİMİ verir."* Filtreler **kaldırıldı** ve fark
gerçek sebebine bağlandı.

==========================================================================
🔒 B-57'NİN KAPANIŞ BİÇİMİ (K-053 + Y14)

K-053 şunu karara bağlamıştı: **eski bir kayda üretici komut UYDURULAMAZ** —
bir komutun o sayıyı ürettiği gösterilemiyorsa yazılamaz. Y14 ekledi:
üretici satırı olması yeterli değil, **yeniden koşu** gerekir.

Bu yüzden kapanış "37 satır ekle" değil, **kanamayı durdurmak**tır:

    · Bugünkü 28 kayıt açıkça SAYILIYOR ve listeleniyor (aşağıda)
    · YENİ bir kayıt ölçüm taşıyorsa üretici satırı ZORUNLU
    · Liste BÜYÜYEMEZ — `test_b57_*` bunu kırar

Bu, `08` madde 22'nin ve `HENUZ_ICERIK_TESTI_OLMAYAN`ın desenidir: beyan
edilmemiş bir boşluk, beyan edilmiş bir boşluktan **tehlikelidir**.
==========================================================================
"""
from __future__ import annotations

import pathlib
import re
import sys

# 28 Eylül 2026: kök sabit üst dizin sayısıyla türüyordu ve betik `arsiv/`e
# taşınınca kök `arsiv/` oluyordu (kayit_indeksi.py'nin 17 Eylül'de onarılan
# kusurunun aynısı). Kök artık aranan dosyadan türer.
def _kok() -> pathlib.Path:
    burasi = pathlib.Path(__file__).resolve()
    for aday in [burasi, *burasi.parents]:
        if (aday / "v2" / "kayit" / "KARAR-GUNLUGU.md").is_file():
            return aday
    raise SystemExit("`v2/kayit/KARAR-GUNLUGU.md` bulunamadi")


KOK = _kok()
# 28 Eylül 2026 (belge temizliği): tam günlük `v2/kayit/`e taşındı;
# `v2/04-KARARLAR.md` yalnız bugün geçerli kararları tutar.
KAYIT_DOSYASI = KOK / "v2" / "kayit" / "KARAR-GUNLUGU.md"

# ÖLÇÜM: yüzde · ondalık · oran · birimli büyüklük
_OLCUM = re.compile(
    r"%\s?\d"
    r"|\b\d+,\d+\b"
    r"|\b\d+\s*/\s*\d+\b"
    r"|\b\d+\s*(?:×|kat|dk|sn|s\b|m\b|dBm|W\b|µs|ms|bayt|test|tohum|koşu)"
)

_URETICI = re.compile(r"\*\*Üretici:?\*\*")


def kayitlar() -> list[tuple[str, str]]:
    t = KAYIT_DOSYASI.read_text(encoding="utf-8")
    p = re.split(r"(?m)^# (K-\d\d\d)", t)
    return [(p[i], p[i + 1]) for i in range(1, len(p), 2)]


def _olcum_tasiyor_mu(govde: str) -> bool:
    """Bu kayıt bir ÖLÇÜM taşıyor mu?

    🔴 Eleme filtresi YOKTUR ve olmasına gerek yoktur — ölçüldü. Desen
    OLUMLU: yüzde · ondalık · oran · BİRİMLİ büyüklük. Tarih, çapraz atıf
    ve standart adı zaten eşleşmez.
    """
    return bool(_OLCUM.search(govde))


def denetle() -> dict:
    kay = kayitlar()
    uretici_var = {k for k, g in kay if _URETICI.search(g)}
    olcum_tasiyan = [k for k, g in kay if _olcum_tasiyor_mu(g)]
    eksik = [k for k in olcum_tasiyan if k not in uretici_var]
    return {
        "toplam": len(kay),
        "uretici_var": sorted(uretici_var),
        "olcum_tasiyan": olcum_tasiyan,
        "eksik": eksik,
    }


# --------------------------------------------------------------------------
# 🔒 DEVRALINAN BOŞLUK — 26 Ağustos 2026'da ölçüldü ve DONDURULDU.
#
# Bu kayıtlar ölçüm taşıyor ve üretici satırı YOK. K-053 gereği onlara komut
# UYDURULMAZ. Liste **büyüyemez**: yeni bir kayıt ölçüm taşıyorsa üretici
# satırı zorunludur. Bir kayıt üreticisine kavuşursa listeden ÇIKARILIR.
# --------------------------------------------------------------------------
DEVRALINAN_URETICISIZ: frozenset[str] = frozenset({
    "K-004", "K-005", "K-006", "K-008", "K-011", "K-013", "K-014", "K-015",
    "K-017", "K-018", "K-019", "K-021", "K-023", "K-025", "K-026",
    # 🟢 K-024 27 Ağustos 2026'da ÇIKARILDI: sayısı bağımsız olarak
    # yeniden ölçüldü ve üreticisine kavuştu (B-108).
    # ⚠️ Sayı TUTMADI — n = 6'lık ölçüm 54 463 çiftte üretilemedi —
    # ama KARAR ayakta ve daha güçlü. Kayıt silinmedi, REVİZE edildi
    # (K-053: eski bir kayda komut UYDURULMAZ; ölçülürse kavuşur).
    "K-027", "K-028", "K-031", "K-033", "K-035", "K-036", "K-040", "K-041",
    "K-044", "K-045", "K-046", "K-050",
})


def main() -> int:
    s = denetle()
    print("=" * 74)
    print("KARAR KAYDI DENETİMİ — `04`teki ölçümler üreticiye bağlı mı (B-57)")
    print("=" * 74)
    print("  toplam karar kaydı              : %d" % s["toplam"])
    print("  `**Üretici:**` satırı olan      : %d" % len(s["uretici_var"]))
    print("  ÖLÇÜM taşıyan                   : %d" % len(s["olcum_tasiyan"]))
    print("  ÖLÇÜM taşıyıp üreticisi YOK     : %d" % len(s["eksik"]))
    print()
    yeni = sorted(set(s["eksik"]) - DEVRALINAN_URETICISIZ)
    kurtulan = sorted(DEVRALINAN_URETICISIZ - set(s["eksik"]))
    if yeni:
        print("  🔴 DEVRALINAN LİSTEDE OLMAYAN (YENİ boşluk): %s" % yeni)
    else:
        print("  ✅ yeni boşluk YOK — kanama durmuş")
    if kurtulan:
        print("  🟢 üreticisine kavuşan (listeden çıkarılmalı): %s" % kurtulan)
    print()
    print("🔒 K-053: eski bir kayda üretici komut UYDURULMAZ.")
    print("🔒 Y14  : üretici satırı yetmez — mühürden önce YENİDEN KOŞULUR.")
    return 1 if (yeni or kurtulan) else 0


if __name__ == "__main__":
    sys.exit(main())
