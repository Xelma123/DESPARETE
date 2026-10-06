"""
Yük muhasebesi — protokolün beacon'a koyduğu bilginin BAYT bedeli.

🔒 DENETLENEREK TAŞINDI (eski `sim/gozlem.py`den, 4 Eylül 2026)
==============================================================
Bu modül eski depoda beş bağımsız denetimden geçti ve iki gerçek kaçak
kapattı. Taşıma kopyala-yapıştır DEĞİL: her kapının onu kıran pozitif bir
testi olduğu doğrulandı ve **bir kural ihlali düzeltildi** (aşağıda).

🔴 TAŞIMADA BULUNAN İHLAL: `_olculen_deger_bayt` içinde ÇIPLAK `assert` vardı.
`python -O` altında sessizce kalkar — yani kırpılmamış bir float ölçüm yoluna
ulaşsa koruma hiç konuşmazdı. `dogrula()`ya çevrildi.

🔴 NEDEN İKİ AYRI HESAP VAR
===========================
`yuk_bayt` bir TARİFE uygular (bool 1, float 4, int büyüklüğüne göre).
`_tasinan_bilgi_bayt` ise tarifeyi HİÇ kullanmaz: `yuku_dondur`un ürettiği
demetten okur ve her değeri **deneyerek** ölçer (`to_bytes` / `struct`).
İkisi geçerli girdide aynı sayıyı verir ama AYRI YOLLARDAN; tarifenin
herhangi bir parçası bozulursa ölçüm yolu değişmez ve koruma konuşur.

Bu bağımsızlık bir kez ÖLMÜŞTÜ ve ölçümle bulundu: iki hesap aynı formülleri
kullandığı için `assert odenen >= tasinan` fiilen `x >= x` idi (200 000
rastgele yükte 0 kez ateşledi). Ve aynı körlük gerçek bir kaçağı saklıyordu:
`float` 4 bayta faturalanıyor ama pencereye çift duyarlıklı (8 bayt) hâliyle
giriyordu — **aynı bilgi, iki kodlama, 2,00× fiyat farkı**.

🔒 `yuku_dondur` float'ı TEL BİÇİMİNE (tek duyarlık) KIRPAR. Beyan edilen
"float = 4 bayt" ancak böyle doğru olur.

🔴 `yuku_dondur` İKİ KEZ TANIMLIYDI — 16 Eylül 2026'da bulundu ve silindi.
============================================================================
Dosyanın sonunda aynı adla, aynı gövdeyle İKİNCİ bir tanım duruyordu ve
birincisini sessizce gölgeliyordu. Silmeden önce iki gövdenin BİREBİR aynı
olduğu programla doğrulandı, yani davranış değişmedi ve hiçbir ölçülmüş sayı
bayatlamadı.

Zararsız olması kusuru küçültmez: `v2/03` §B5'in hata sınıfı tam olarak
budur — *"aynı kuralı iki yerde yazmak; iki kopya bir gün ayrışır."*
Ayrışsalardı Python İKİNCİSİNİ seçerdi, dosyayı yukarıdan okuyan biri
BİRİNCİSİNİ okurdu, ve bu dosyada okunan şey BEDEL TARİFESİDİR.

🔒 Yapısal panzehir: `kalibrasyon/mimari_denetimi.py` → D16. Aynı ad
uzayında iki tanım artık her koşumda taranıyor; sınıf bir daha sessizce
doğamaz.

⚠️ MODELLEME KARARI, kapsam belgesinde beyan edilir: gerçek bir uygulama alan
adları için 1 baytlık bir kimlik tablosu kullanırdı; tablonun varlığı
doğrulanamadığı için **adın kendisi** faturalanır. Yön: dürüst bir protokolü
gerçeğe göre biraz FAZLA ücretlendirir — kaçağa değil, güvenli tarafa doğru.
Hizalama/dolgu modellenmez.
"""

from __future__ import annotations

import math
import struct

from sim2.cekirdek.degismezler import dogrula

__all__ = ["YUK_BOOL_BAYT", "YUK_FLOAT_BAYT", "YUK_INT_TABAN_BAYT",
           "YukHatasi", "yuk_bayt", "yuku_dondur"]


YUK_BOOL_BAYT = 1
YUK_FLOAT_BAYT = 4          # tek duyarlık
YUK_INT_TABAN_BAYT = 1      # en küçük tamsayı bile bir bayt eder


def _int_bayt(v: int) -> int:
    """Bir tamsayının BÜYÜKLÜĞÜNE göre bayt maliyeti (B-66)."""
    return max(YUK_INT_TABAN_BAYT, (int(v).bit_length() + 7) // 8)


# ==========================================================================
# 🔴 B-82 · B-83 (BEŞİNCİ DENETİM) — Y7 ÖZ-DENETİMİ YAPISAL OLARAK ÖLÜYDÜ
#
# B-66 iki hesap yazdı ve *"biri bozulunca diğeri konuşsun"* dedi. Beşinci
# bağımsız denetim ölçtü: **konuşamıyordu.** İki hesap aynı formülleri, aynı
# `_int_bayt()`i ve aynı `YUK_FLOAT_BAYT`ı kullanıyordu; `yuk_bayt`ın kabul
# ettiği HER girdide sonuç birebir aynıydı:
#
#     200 000 rastgele yük -> 105 943 kabul -> iki hesap FARKLI:        0
#                                           -> `toplam < tasinan` ATEŞ: 0
#
# Yani `assert odenen >= tasinan` fiilen **`x >= x`** idi — Y10'un tam tanımı
# *("bir yaklaşık-eşitlik iddiası, KIRILABİLİR olduğu gösterilmeden
# yazılmaz")*.
#
# 🔴 VE AYNI KÖRLÜK GERÇEK BİR KAÇAĞI SAKLIYORDU (B-83): `float` **4 bayta**
# faturalanıyor ama gözlem penceresine **çift duyarlıklı (8 bayt) hâliyle,
# kırpılmadan** giriyordu. Ölçüldü: 8 keyfi bayt bir `float`a kondu ve
# **birebir** geri okundu. Aynı 8 bayt `int` olarak 8 bayt öderken `float`
# olarak 4 — **aynı bilgi, iki kodlama, 2,00× fiyat farkı.**
#
# İKİ DÜZELTME, TEK KÖK:
#
#   1. `yuku_dondur` float'ı TEL BİÇİMİNE (tek duyarlık) **kırpar.** Böylece
#      beyan edilen *"float = 4 bayt"* **doğru** olur: pencereye ulaşan değer
#      tam olarak 4 baytın taşıyabildiğidir.
#   2. `_tasinan_bilgi_bayt` artık **TARİFEYİ KULLANMIYOR.** Girdiden değil
#      `yuku_dondur`un ÜRETTİĞİNDEN okuyor ve her değeri **deneyerek**
#      ölçüyor (`to_bytes` / `struct`). `_int_bayt` ve `YUK_FLOAT_BAYT` bu
#      yolda hiç geçmiyor.
#
# 🔒 BAĞIMSIZLIK ARTIK ÖLÇÜLEBİLİR: ikisi geçerli girdide aynı sayıyı verir
# ama AYRI YOLLARDAN. Tarifenin herhangi bir parçası bozulursa ölçüm yolu
# değişmez ve koruma **konuşur.** Zorlayan test:
# `tests/test_gozlem.py::test_b82_iki_hesap_GERCEKTEN_ayri`
# ==========================================================================


def _tek_duyarliga_kirp(v: float) -> float:
    """Bir float'ı TEL BİÇİMİNE (tek duyarlık, 4 bayt) indirger (B-83)."""
    try:
        return struct.unpack("<f", struct.pack("<f", v))[0]
    except OverflowError:                    # tek duyarlığa sığmıyor
        return math.inf if v > 0 else -math.inf


def _olculen_int_bayt(v: int) -> int:
    """Bir tamsayının GERÇEKTEN kapladığı bayt — DENEYEREK ölçülür.

    🔴 B-82: `_int_bayt`in formülünü KULLANMAZ. İkisi geçerli girdide aynı
    sayıyı verir ama AYRI YOLLARDAN; biri bozulursa diğeri konuşur.
    """
    m = abs(int(v))
    alt = ust = 1
    while True:                              # üstel arama: sığan bir genişlik
        try:
            m.to_bytes(ust, "little")
            break
        except OverflowError:
            alt = ust + 1
            ust *= 2
    while alt < ust:                         # ikili arama: EN KÜÇÜĞÜ
        orta = (alt + ust) // 2
        try:
            m.to_bytes(orta, "little")
            ust = orta
        except OverflowError:
            alt = orta + 1
    return alt


def _olculen_deger_bayt(deger) -> int:
    """Gözlem penceresine ULAŞAN bir değerin ÖLÇÜLEN genişliği (B-82)."""
    if isinstance(deger, bool):
        return len(struct.pack("<?", deger))
    if isinstance(deger, int):
        return _olculen_int_bayt(deger)
    if isinstance(deger, float):
        # 🔴 B-112 (ALTINCI DENETİM) — 8 BAYT DALI ÖLÜYDÜ, `assert`E ÇEVRİLDİ.
        #
        # Burada `return len(struct.pack("<d", deger))` vardı ve ASLA
        # çalışmıyordu: `_tasinan_bilgi_bayt` değerleri `yuku_dondur`dan
        # okuyor, `yuku_dondur` ise B-83'ten beri her float'ı TEK DUYARLIĞA
        # KIRPIYOR. Kırpılmış bir float her zaman sığar.
        #
        # ⚖️ B-83'ün kapanışı, B-82'nin ölçüm yolundaki bu dalı öldürmüştü —
        # yani bir kapanış bir sonraki bulguyu doğurdu.
        #
        # Ölçüldü (27 Ağu, bağımsız olarak): 200 000 rastgele yük →
        # 149 212 float değeri → 4 bayt dalı 149 212 · **8 bayt dalı 0**.
        #
        # 🔴 KAPSAMI DAR TUTULUYOR (Y11): B-82'nin ÖZ-DENETİMİ ÖLMEDİ —
        # `YUK_FLOAT_BAYT` 4'ten 2'ye indirilse ölçüm yolu yine 4 döner ve
        # koruma konuşur. Ölen tek şey *"tel biçimine sığmayan bir değeri
        # yakalama"* yeteneğiydi; kırpmadan sonra öyle bir değer pencereye
        # ULAŞAMAZ.
        # 🔴 TAŞIMADA DÜZELTİLDİ: burada ÇIPLAK `assert` vardı ve `-O`
        # altında sessizce kalkıyordu. Koruma ancak her zaman koşarsa korumadır.
        dogrula(math.isnan(deger) or deger == _tek_duyarliga_kirp(deger),
                "kırpılmamış bir float ölçüm yoluna ulaştı — "
                "`yuku_dondur`un kırpması kalkmış olabilir")
        return len(struct.pack("<f", deger))         # tel biçimine SIĞIYOR
    if isinstance(deger, tuple):
        return sum(_olculen_deger_bayt(x) for x in deger)
    return 0


def _tasinan_bilgi_bayt(yuk: dict) -> int:
    """Gözlem penceresine ULAŞAN bilginin ÖLÇÜLEN genişliği.

    🔴 Y7 (B-82): `yuk_bayt` kendi çıktısını buna karşı doğrular. Bu hesap
    tarifeden DEĞİL, `yuku_dondur`un ürettiği demetten okur ve her değeri
    **deneyerek** ölçer — biri bozulduğunda diğeri konuşabilsin diye.
    """
    toplam = 0
    for ad, deger in yuku_dondur(yuk):
        toplam += len(ad.encode("utf-8"))
        toplam += _olculen_deger_bayt(deger)
    return toplam


class YukHatasi(ValueError):
    """Protokolün beacon'a koymaya çalıştığı yük sözleşmeye uymuyor."""


def _tel_bicimine_sigmali(ad: str, v: float) -> None:
    """🔴 B-83 — tel biçimi TEK DUYARLIKTIR.

    Taşan bir float sessizce sonsuza dönemez: sığmayan değer taşınamaz,
    kırpılıp yutulamaz. Aksi hâlde `yuku_dondur`un kırpması bir bilgi
    kaybını SESSİZCE yapardı.
    """
    if math.isfinite(v) and not math.isfinite(_tek_duyarliga_kirp(v)):
        raise YukHatasi(
            f"{ad!r}: {v!r} tel biçimine (tek duyarlık, {YUK_FLOAT_BAYT} "
            f"bayt) sığmıyor — kırpılınca sonsuza taşar. "
            f"Sözleşme: |v| <= ~3,4e38.")


def yuk_bayt(yuk: dict) -> int:
    """Bir beacon yükünün TEL ÜZERİNDEKİ bayt maliyeti.

    🔴 Y7 — ARAÇ NE SAYDIĞINI KENDİSİ DOĞRULAR: sözleşme dışı bir değer
    sessizce 0 bayt saymaz, `YukHatasi` fırlatır. Aksi hâlde bir protokol
    beacon'a keyfi bir nesne koyup bedelini ödemeden taşırdı — ve bu, hem
    kontrol yükü muhasebesini hem kâhin korumasını delerdi.
    """
    if not isinstance(yuk, dict):
        raise YukHatasi(f"yük bir sözlük olmalı, {type(yuk).__name__} geldi")
    toplam = 0
    for ad, deger in yuk.items():
        if not isinstance(ad, str) or not ad:
            raise YukHatasi(f"alan adı boş olmayan bir dizgi olmalı: {ad!r}")
        # 🔴 B-66: alan adı UZUNLUĞUYLA faturalanır, sabit 1 baytla değil.
        toplam += len(ad.encode("utf-8"))
        if isinstance(deger, bool):
            toplam += YUK_BOOL_BAYT
        elif isinstance(deger, int):
            toplam += _int_bayt(deger)          # 🔴 B-66: BÜYÜKLÜĞÜYLE
        elif isinstance(deger, float):
            _tel_bicimine_sigmali(ad, deger)          # 🔴 B-83
            toplam += YUK_FLOAT_BAYT
        elif isinstance(deger, tuple):
            if not deger:
                raise YukHatasi(f"{ad!r}: boş demet taşınamaz")
            for x in deger:
                if isinstance(x, bool) or not isinstance(x, (int, float)):
                    raise YukHatasi(
                        f"{ad!r}: demet yalnızca sayı taşıyabilir, "
                        f"{type(x).__name__} var")
                if isinstance(x, float):
                    _tel_bicimine_sigmali(ad, x)      # 🔴 B-83
                    toplam += YUK_FLOAT_BAYT
                else:
                    toplam += _int_bayt(x)
        else:
            raise YukHatasi(
                f"{ad!r}: taşınamaz tip {type(deger).__name__}. "
                f"İzinli: bool · int · float · sayı demeti")

    # 🔴 Y7 — ARAÇ KENDİ ÇIKTISINI DOĞRULAR (B-66).
    # Ödenen bayt, taşınan bilginin alt sınırından küçük olamaz. İki hesap
    # ayrı yazılmıştır; biri bozulursa diğeri konuşur.
    tasinan = _tasinan_bilgi_bayt(yuk)
    if toplam < tasinan:
        raise YukHatasi(
            f"BEDEL KAÇAĞI: {toplam} bayt ödeniyor ama en az {tasinan} bayt "
            f"bilgi taşınıyor ({tasinan/max(toplam,1):.0f}×). `05` §A2 kural 1 "
            f"ihlal edilir ve K-009'un eşit bütçe şartı denetlenemez olur.")
    return toplam


def yuku_dondur(yuk: dict) -> tuple[tuple[str, object], ...]:
    """Yükü sıralı, DONMUŞ bir demete çevirir — gözlem yüzeyine öyle girer.

    🔴 B-83: `float` burada TEL BİÇİMİNE (tek duyarlık) **kırpılır.** Beyan
    edilen bedel 4 bayttır; pencereye ulaşan değer de tam olarak 4 baytın
    taşıyabildiği olmalıdır. Kırpma olmadan 8 baytlık bir çift duyarlık
    değeri 4 bayt bedelle taşınıyordu — ölçüldü: **2,00× kaçak**, ve
    `yuk_bayt`ın Y7 öz-denetimi bunu **yapısal olarak göremiyordu** (B-82).
    """
    def kirp(d):
        if isinstance(d, bool) or isinstance(d, int):
            return d
        if isinstance(d, float):
            return _tek_duyarliga_kirp(d)
        if isinstance(d, tuple):
            return tuple(kirp(x) for x in d)
        return d

    return tuple(sorted(((ad, kirp(d)) for ad, d in yuk.items()),
                        key=lambda p: p[0]))
