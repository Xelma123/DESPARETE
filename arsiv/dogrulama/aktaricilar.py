"""
🔴 DOĞRULAMA AKTARICILARI — sim/ ALTINDA DEĞİLDİR, OLAMAZ.

Bunlar deney kolu DEĞİLDİR. Varlık sebepleri:
  - korunum, belirlenimcilik ve MAC yollarını gerçek protokoller yazılmadan
    önce sınamak
  - iki farklı davranışlı kol gerektiren kapı testlerini beslemek (Ç2.3)

KÂHİNLİK BURADA AÇIKÇA YAPILIR
==============================
`Kosu`, protokole karar anında yalnızca bir `Gozlem` verir ve fabrikaya
topoloji vermez. Buradaki bazı aktarıcılar topolojiyi `Konfig`ten YENİDEN
ÜRETEREK elde eder — `Topoloji.uret(kon, Akislar(kon.tohum))` aynı topolojiyi
belirlenimci olarak verir.

Bu apaçık bir kâhin hamlesidir ve bilerek **görünür** bırakılmıştır:
`dogrulama/` altında, adı `_KAHIN` ile başlayan bir yardımcıda. Aile 1'in
gerçek rakip protokolleri `sim/` altında olacak ve YALNIZCA `Gozlem`
kullanacak.

⚠️ Buradan çıkan hiçbir sayı bir hipoteze cevap veremez.
"""

from __future__ import annotations

from collections import deque

from sim.config import Konfig
from sim.gozlem import Gozlem
from sim.rng import Akislar
from sim.topology import Topoloji


# ==========================================================================
# 🔴 KALİTE ABLASYONU — `03` B1'in null modeli, YAPI ve KALICILIK korunarak
#
# NEDEN VAR (B-65, K-056)
# -----------------------
# H1.1'in mekanizma kapısı iki kez yanlış şey ölçtü:
#
#   B-45 · `ara_bolge_karar` oranı → bilgiyi değil YOL GEOMETRİSİNİ ölçüyordu
#   B-65 · `secim_avantaji_ortalama` mutlak eşiği → bilgiyi değil SEÇİMİN
#          KALICILIĞINI ölçüyordu; eşik TEK TOHUMDA kalibre edilmişti ve
#          ayarlama tohumlarının 7/8'inde düşüyordu
#
# ÖLÇÜLDÜ (S2 · orta · 8 tohum · `secim_avantaji_ortalama`):
#
#   gurultuden_kacan (bilgili)              +0,0876 ± 0,0431
#   KALICI ablasyon (yapı+kalıcılık aynı)   +0,0599 ± 0,0232   ← sıfır DEĞİL
#   karar-başına ablasyon                   −0,0006 ± 0,0015   ← YANILTICI
#   projenin _null_rastgele'si              +0,0540 ± 0,0677
#
# 🔴 KALICILIK TEK BAŞINA +0,06 AVANTAJ SATIN ALIYOR. Karar başına karıştıran
# bir null bunu göremez ve her kalıcı kolu "bilgili" sanır. Bu yüzden ablasyon
# permütasyonu (düğüm, komşu kümesi) başına BİR KEZ sabitlenir.
#
# Eşleştirilmiş fark (bilgili − kalıcı ablasyon): +0,0277 ± 0,0231,
# **8/8 tohumda pozitif** (işaret testi, tek yönlü p = 0,0039).
#
# ⚠️ Bu bir DENEY KOLU DEĞİLDİR; ölçüm aracıdır ve `dogrulama/` altındadır.
# ==========================================================================

def kalite_ablasyonu(fabrika, alan: str = "bildirdigi_gurultu_w",
                     tuz: int = 0):
    """Bir protokolün KALİTE GİRDİSİNİ yok eden ablasyon sarmalayıcısı.

    Protokol aynı kalır; yalnızca gördüğü komşu kayıtlarında `alan`ın
    değerleri komşular arasında **permüte** edilir. Dağılım, yapı, kalıcılık
    **ve komşu demetinin SIRASI** korunur — yok edilen tek şey *"hangi değer
    hangi komşuya ait"* bilgisidir.

    🔴 B-84: sıranın korunması 26 Ağustos 2026'da eklendi. Öncesinde demet
    `sorted(..., key=dugum)` hâliyle geri veriliyordu ve bu ablasyonun
    **ikinci ekseniydi** — bilgi dışında bir fark. Sıraya duyarlı bir kol
    için gürültü tabanı, kapının ayırt etmesi gereken sinyalin **2,9 katıydı.**

    🔴 Permütasyon `(düğüm, komşu kümesi)` başına BİR KEZ çekilir ve
    saklanır. Karar başına yeniden çekilseydi, kalıcılığı da yok ederdi ve
    null yapay olarak sıfıra inerdi — ölçüldü: −0,0006 vs +0,0599.

    Aile 1'in her kalite temelli kolu bununla ablate edilir; kapı, kolun
    KENDİ ablasyonuna karşı **eşleştirilmiş** okunur.
    """
    import dataclasses
    import random

    def sarmalanmis(kon: Konfig):
        ic = fabrika(kon)
        perm: dict = {}

        def sonraki(g: Gozlem):
            if not g.komsular:
                return ic(g)
            ks = sorted(g.komsular, key=lambda k: k.dugum)
            anahtar = (g.dugum, tuple(k.dugum for k in ks))
            if anahtar not in perm:
                idx = list(range(len(ks)))
                # Belirlenimci: aynı tohum → aynı permütasyon (Ç2 korunur)
                # 🔴 A-5: `tuz` AYNI tohumda BAĞIMSIZ bir null çekmeyi
                # mümkün kılar. `tuz=0` bugünkü davranışın BİREBİR
                # aynısıdır (x ^ 0 == x) — ön-kayıtlı kapının sayıları
                # DEĞİŞMEZ. Ablasyon çekiminin KENDİ varyansı ancak
                # böyle ölçülebilir; öncesinde topolojiyle karışıktı.
                random.Random((hash(anahtar) & 0xFFFFFFFF) ^ tuz).shuffle(idx)
                perm[anahtar] = idx
            degerler = [getattr(ks[i], alan) for i in perm[anahtar]]
            # 🔴 B-84 (beşinci denetim): permüte edilen DEĞERLER, komşuların
            # ORİJİNAL sırasına geri yazılır. Eskiden demet `sorted(...)`
            # hâliyle geri veriliyordu ve bu, ablasyonun **İKİNCİ EKSENİ**
            # oluyordu: sağlam koşuda `g.komsular` %92,8 oranında SIRASIZ
            # geliyor. Ölçüldü — sıraya duyarlı bir kolda ölçülen farkın
            # %100'ü yeniden sıralama artefaktıydı (std 0,081; kapının ayırt
            # etmesi gereken gerçek sinyal +0,0283, std 0,0230).
            #
            # `06`'nın *"Tek fark BİLGİ"* cümlesi ancak bu düzeltmeyle doğru
            # olur. `03` B1: *"Ablasyonu yanlış yerden bölmek — tasarım
            # metninin cümlelerinden değil, MEKANİZMA SINIRLARINDAN böl."*
            # Sıralama bir mekanizma sınırı değil, uygulama ayrıntısıdır.
            #
            # 🔒 Değer ataması BİREBİR aynı kalıyor: `ks[i]` yine
            # `ks[perm[i]]`in değerini alır. Değişen tek şey, demetin hangi
            # SIRAYLA geri verildiğidir.
            harita = {ks[i].dugum: d for i, d in enumerate(degerler)}
            yeni = tuple(dataclasses.replace(k, **{alan: harita[k.dugum]})
                         for k in g.komsular)
            return ic(dataclasses.replace(g, komsular=yeni))

        return sonraki

    _ek = "" if tuz == 0 else f"_tuz{tuz}"
    sarmalanmis.__name__ = (
        f"ablasyon_{alan}{_ek}_{getattr(fabrika, '__name__', 'kol')}")
    return sarmalanmis


def _KAHIN_topoloji(kon: Konfig) -> Topoloji:
    """🔴 KÂHİN: topolojiyi konfigürasyondan yeniden üretir.

    Gerçek bir protokol bunu yapamaz — düğüm konumlarını ancak beacon'dan
    öğrenir ve karıştırma altında beacon kaybolur.
    """
    return Topoloji.uret(kon, Akislar(kon.tohum))


# --------------------------------------------------------------------------
# KÂHİN aktarıcılar
# --------------------------------------------------------------------------

def en_kisa_yol(kon: Konfig):
    """🔴 KÂHİN. Atlama sayısını en küçükleyen yol; bağ kalitesine KÖR.

    Karıştırıcının zehirli bölgesinden bile bile geçer.
    """
    topo = _KAHIN_topoloji(kon)
    onbellek: dict[tuple[int, int], int | None] = {}

    def sonraki(g: Gozlem) -> int | None:
        if g.paket is None:
            return None
        anahtar = (g.dugum, g.paket.hedef)
        if anahtar in onbellek:
            return onbellek[anahtar]
        onceki: dict[int, int] = {g.dugum: g.dugum}
        q = deque([g.dugum])
        while q:
            d = q.popleft()
            if d == g.paket.hedef:
                break
            for k in topo.geometrik_komsular(d):
                if k not in onceki:
                    onceki[k] = d
                    q.append(k)
        if g.paket.hedef not in onceki:
            onbellek[anahtar] = None
            return None
        adim = g.paket.hedef
        while onceki[adim] != g.dugum:
            adim = onceki[adim]
        onbellek[anahtar] = adim
        return adim

    return sonraki


def hedefe_en_yakin(kon: Konfig):
    """Yarı-kâhin: hedefin konumu kâhinden, KOMŞULAR ise BEACON'dan.

    `en_kisa_yol`dan farklı kararlar verir ve farklı sayıda iletim yapar —
    Ç2.3 (iki kol aynı kanal gerçeklemesini görüyor mu) için gereken budur.
    Beacon'a bağlı olduğu için karıştırma altında komşusuz kalabilir; bu
    kasıtlıdır ve `hedef_yok` yolunu tetikler.
    """
    topo = _KAHIN_topoloji(kon)

    def sonraki(g: Gozlem) -> int | None:
        if g.paket is None or not g.komsular:
            return None
        hedef_konum = topo.konumlar[g.paket.hedef]
        adaylar = [k for k in g.komsular]
        for k in adaylar:
            if k.dugum == g.paket.hedef:
                return k.dugum

        def uzaklik(k):
            if k.bildirdigi_konum is None:
                return float("inf")
            dx = k.bildirdigi_konum[0] - hedef_konum[0]
            dy = k.bildirdigi_konum[1] - hedef_konum[1]
            return (dx * dx + dy * dy) ** 0.5

        return min(sorted(adaylar, key=lambda k: k.dugum), key=uzaklik).dugum

    return sonraki


# --------------------------------------------------------------------------
# Saf gözlem aktarıcıları — kâhin DEĞİL
# --------------------------------------------------------------------------

def dongu_yapan(kon: Konfig):
    """Kasten döngü kuran aktarıcı: en küçük numaralı komşuya atıp durur.

    ⭐ Bu aktarıcı KÂHİN DEĞİL: yalnızca `gozlem.komsular` kullanıyor.
    TTL yolunu tetiklemek için var.
    """
    def sonraki(g: Gozlem) -> int | None:
        if not g.komsular:
            return None
        return min(k.dugum for k in g.komsular)
    return sonraki


def olu(kon: Konfig):
    """Hiç rota bulamayan aktarıcı — `hedef_yok` yolunu tetiklemek için."""
    def sonraki(g: Gozlem) -> int | None:
        return None
    return sonraki


def gurultuden_kacan(kon: Konfig):
    """⭐ TAMAMEN GÖZLEM TABANLI örnek: en az gürültü bildiren komşuyu seçer.

    Kâhin hiçbir bilgi kullanmaz. Gerçek bir protokolün nasıl yazılacağının
    minimal örneği — ve gözlem penceresinin yeterli olduğunun kanıtı.
    """
    def sonraki(g: Gozlem) -> int | None:
        if g.paket is None or not g.komsular:
            return None
        for k in g.komsular:
            if k.dugum == g.paket.hedef:
                return k.dugum
        return min(sorted(g.komsular, key=lambda k: k.dugum),
                   key=lambda k: k.bildirdigi_gurultu_w).dugum
    return sonraki


AKTARICILAR = {
    "en_kisa_yol": en_kisa_yol,
    "hedefe_en_yakin": hedefe_en_yakin,
    "dongu_yapan": dongu_yapan,
    "olu": olu,
    "gurultuden_kacan": gurultuden_kacan,
}
