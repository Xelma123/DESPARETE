"""
Kat 5 — GÖZLEM PENCERESİ.

🔴 BU DOSYA BİR SÖZLEŞMEDİR.
Yönlendirme katmanının görebileceği HER ŞEY burada. Bu nesnede olmayan hiçbir
bilgi bir protokol kararına giremez.

`v2/05-GOZLEM-PENCERESI.md` ile birebir eşleşir. Belge değişirse burası da
değişir; **sonradan daraltmak, o zamana kadarki tüm ölçümleri geçersiz kılar.**

NEDEN AYRI BİR NESNE
====================
Protokole simülatörün kendisi verilseydi, bir gün biri `topo.mesafe(...)` ya
da `karistirici.konum` yazardı ve hiçbir test bunu yakalamazdı. Sonuçlar makul
görünmeye devam ederdi.

Bu nesne:
  - donmuştur (frozen) — protokol içeriğini değiştiremez
  - simülatöre GERİ REFERANS TAŞIMAZ
  - yüzeyi otomatik test edilir (`tests/test_gozlem.py`)

⭐ EN ÖNEMLİ ALAN: `son_iletim_sonucu`
=====================================
"Onay geldi" / "zaman aşımı" ikilisi, bu pencerenin EN UCUZ ve EN ÖNEMLİ
bilgisidir. Sıfır bayta mal olur — zaten sahip olunan bir gözlemdir.
Karıştırma altında en sık gerçekleşen olay budur.

🔴 GÖREMEYECEKLERİ — burada olmadıkları için görülemezler
=========================================================
karıştırıcının konumu/gücü/açık olup olmadığı · diğer düğümlerin gerçek
konumu · ağın gerçek topolojisi · bir bağın gerçek kalitesi · gerçek en kısa
yol · bir paketin ileride teslim edilip edilmeyeceği · başka bir düğümün
tablosu · simülatörün iç durumu · menzil içindeki düğümlerin listesi.
"""

from __future__ import annotations

import math
import struct
from dataclasses import dataclass, field


@dataclass(frozen=True)
class KomsuKaydi:
    """Bir komşu hakkında YALNIZCA beacon'dan öğrenilenler.

    ⚠️ Bu kaydın var olması, komşunun ŞU AN hayatta olduğunu göstermez.
    `son_duyulma_s` bayattır ve karıştırma altında bayatlar. Bir protokol
    bunu tazelik ölçüsü olarak kullanmak zorundadır.
    """
    dugum: int
    son_duyulma_s: float          # KENDİ saatine göre
    duyulan_beacon: int           # bu komşudan alınan toplam beacon sayısı
    # Beacon'ın taşıdığı alanlar — her biri BAYTA mal olur (kontrol yüküne yazılır)
    bildirdigi_gurultu_w: float   # komşunun kendi antenindeki gürültü
    bildirdigi_kuyruk: int        # komşunun kuyruk uzunluğu
    bildirdigi_konum: tuple[float, float] | None   # varsa; bayta sayılır
    # 🔴 B-47 (K-049) — PROTOKOLÜN KENDİ KOYDUĞU ALANLAR.
    # `05` §A2: *"Komşusunun girişim seviyesini veya kuyruk durumunu
    # kullanmak isteyen bir protokol, o alanları başlığa KOYMAK ve bedelini
    # ÖDEMEK zorundadır."* Bu hak belgede vardı, **kod karşılığı yoktu**:
    # beacon içeriği simülatör tarafından sabitlenmişti ve protokolün
    # herhangi bir çerçeveye bilgi koyma yolu yoktu. Üçüncü bağımsız denetim
    # ölçtü: saf gözlemle yazılan bir ETX protokolü S0'da 0,0997 teslim ve
    # 1,00 ortalama atlama veriyordu — çok atlamalı çalışmıyordu.
    #
    # Sıralı demet olarak taşınır: donmuş, simülatöre geri referans taşımaz.
    bildirdigi_yuk: tuple[tuple[str, object], ...] = ()

    def yas_s(self, simdi_s: float) -> float:
        """Bilginin yaşı. v1'in teşhisi tam olarak buydu: karar anında
        kullanılan bilginin yaşı 3,95 s, rakibinki 1,00 s."""
        return simdi_s - self.son_duyulma_s


@dataclass(frozen=True)
class PaketGorunumu:
    """Paketin başlığında YAZAN alanlar. Başka bir şey görünmez.

    `dogum_s` YOKTUR: saatler senkron olmadığı için başka bir düğüm onu
    kendi saatiyle karşılaştıramaz. Ölçüm tarafı paketin doğum anını bilir
    ama protokol bilemez.
    """
    hedef: int
    kaynak: int
    ttl: int
    atlama_sayisi: int
    bayt: int


@dataclass(frozen=True)
class Gozlem:
    """Bir düğümün bir karar anında görebildiği HER ŞEY."""

    # --- kimlik ve zaman ---------------------------------------------------
    dugum: int
    saat_s: float                 # 🔴 KENDİ saati. Düğümler arası SENKRON DEĞİL.

    # --- kendi donanımından ölçtükleri -------------------------------------
    olculen_gurultu_w: float      # kendi antenindeki toplam gürültü + girişim
    kanal_mesgul_mu: bool         # taşıyıcı dinleme, şu an
    kuyruk_uzunlugu: int
    kuyruk_kapasitesi: int

    # --- iletim geçmişi ----------------------------------------------------
    # ⭐ En ucuz ve en önemli bilgi. Sıfır bayt.
    son_iletim_sonucu: str | None      # "onay" | "zaman_asimi" | None
    son_iletim_hedefi: int | None
    gonderilen_bayt: int
    alinan_bayt: int

    # --- komşular: YALNIZCA beacon'dan -------------------------------------
    komsular: tuple[KomsuKaydi, ...] = field(default_factory=tuple)

    # --- taşınan paket -----------------------------------------------------
    paket: PaketGorunumu | None = None

    # ------------------------------------------------------------------ yardım
    def komsu(self, dugum: int) -> KomsuKaydi | None:
        for k in self.komsular:
            if k.dugum == dugum:
                return k
        return None

    @property
    def kuyruk_doluluk(self) -> float:
        return self.kuyruk_uzunlugu / self.kuyruk_kapasitesi


# --------------------------------------------------------------------------
# İZİN VERİLEN YÜZEY — testin dayandığı liste
#
# `tests/test_gozlem.py` bu listeyi kullanarak nesnenin yüzeyini tarar.
# Listede olmayan bir alan eklenirse test KIRILIR ve `05-GOZLEM-PENCERESI.md`
# güncellenmeden geçilemez.
# --------------------------------------------------------------------------
IZINLI_GOZLEM_ALANLARI = frozenset({
    "dugum", "saat_s",
    "olculen_gurultu_w", "kanal_mesgul_mu",
    "kuyruk_uzunlugu", "kuyruk_kapasitesi",
    "son_iletim_sonucu", "son_iletim_hedefi",
    "gonderilen_bayt", "alinan_bayt",
    "komsular", "paket",
})

# 🔴 B-27b — HER ALANIN İÇERİK TESTİ OLMAK ZORUNDA.
# ---------------------------------------------------------------------------
# İkinci bağımsız denetim şunu ölçtü: dört alanın ne bir TÜKETİCİSİ
# (okuyan aktarıcı) ne bir İÇERİK TESTİ (değerinin gerçek büyüklüğe eşit
# olduğunu gösteren) vardı. `kanal_mesgul_mu`u sabit `False`,
# `kuyruk_uzunlugu`u sabit `0` yapan mutasyonlar **240/240 test geçiyordu**.
#
# ⚠️ Doğru okuma "eşdeğer" değil **"tüketicisiz"**dir (Y8): alan karar anında
# 7 342 kez üretiliyor ve `kanal_mesgul_mu` bunların 1 417'sinde `True` —
# yani ÜRETİM yolu tetikleniyor, TÜKETİM yolu yok.
#
# Bu, `03` B5'in "bildirim ≠ kullanım" tuzağının gözlem sözleşmesindeki
# hâli. Proje bu tuzağa karşı iki koruma yazmıştı
# (`Konfig.UYGULANMAMIS_BAYRAKLAR`, `rng.HENUZ_KULLANILMAYAN`) ama gözlem
# penceresine uygulamamıştı. Bu, o desenin üçüncüsü.
#
# KURAL: `IZINLI_GOZLEM_ALANLARI`ndaki her alan **ya** değerinin bağımsız
# hesaplanmış gerçek büyüklüğe eşit olduğunu gösteren bir teste bağlanır,
# **ya** aşağıda açıkça beyan edilir. Üçüncü seçenek yoktur.
# Zorlayan test: `tests/test_gozlem.py::test_b27b_her_gozlem_alaninin_icerik_testi_var`
HENUZ_ICERIK_TESTI_OLMAYAN: frozenset[str] = frozenset()

# 🔴 B-99 (BEŞİNCİ DENETİM, 26 Ağustos 2026) — KURAL YALNIZCA `Gozlem`E
# UYGULANIYORDU. `IZINLI_KOMSU_ALANLARI` (7 alan) ve `IZINLI_PAKET_ALANLARI`
# (5 alan) yalnızca bir YÜZEY testinden geçiyordu (alan adları eşleşiyor mu),
# içerik kuralının DIŞINDAYDI.
#
# Denetçi ölçtü: `KomsuKaydi.duyulan_beacon` sabit `1` yapıldığında **gözlem
# penceresi parmak izi DEĞİŞTİ** ve **367 testin 367'si geçti** (mutasyon X04).
# `08` madde 22 dokuz tüketicisiz `Gozlem` alanı beyan ediyor; `duyulan_beacon`
# ONUNCUSUDUR ve `KomsuKaydi` seviyesinde olduğu için o beyanın dışındaydı.
#
# 🔒 Kural artık ÜÇ kümeye de uygulanıyor. Aşağıdaki iki küme, henüz içerik
# testi olmayan alanları **görünür ve sayılabilir** kılar — beyan edilmemiş
# bir boşluk, beyan edilmiş bir boşluktan tehlikelidir.
HENUZ_ICERIK_TESTI_OLMAYAN_KOMSU: frozenset[str] = frozenset({
    "dugum",                 # kimlik; `KomsuKaydi.dugum == gonderen` yüzeyde
    "son_duyulma_s",         # tazelik; `yas_s()` üzerinden dolaylı sınanıyor
    "bildirdigi_kuyruk",     # tüketicisi yok
    "bildirdigi_konum",      # tüketicisi yok
})
HENUZ_ICERIK_TESTI_OLMAYAN_PAKET: frozenset[str] = frozenset({
    "hedef", "kaynak", "ttl", "atlama_sayisi", "bayt",
})

IZINLI_KOMSU_ALANLARI = frozenset({
    "dugum", "son_duyulma_s", "duyulan_beacon",
    "bildirdigi_gurultu_w", "bildirdigi_kuyruk", "bildirdigi_konum",
    # 🔴 B-47: protokolün KENDİ koyduğu alanlar. Genişletme DEĞİL — `05`
    # §A2'nin zaten verdiği hakkın kod karşılığı. Üç kural kendiliğinden
    # geçerli: bayta sayılır · bayattır · kaybolabilir.
    "bildirdigi_yuk",
})

IZINLI_PAKET_ALANLARI = frozenset({
    "hedef", "kaynak", "ttl", "atlama_sayisi", "bayt",
})

# ==========================================================================
# 🔴 B-47 — BEACON YÜKÜNÜN BAYT MALİYETİ
#
# `05` §A2 kural 1: *"Başlıktaki her alan BAYT OLARAK SAYILIR ve kontrol
# yüküne yazılır."* Maliyet **gerçek serileştirmeden** hesaplanır; protokolün
# kendi beyanına bırakılmaz. Beyan edilseydi, ucuz görünmek isteyen bir
# protokol az beyan ederdi — `03` B5'in *"bildirim ≠ kullanım"* tuzağının
# kontrol düzlemi bütçesindeki hâli, ve K-009'un *"eşit kontrol düzlemi
# bütçesi"* adalet şartı denetlenemez olurdu.
#
# 🔴 21 AĞUSTOS 2026 — BEDEL TİPE DEĞİL BOYUTA BAĞLANDI (B-66, K-056).
#
# ÖNCEKİ BİÇİM KAÇAK VERİYORDU: alan adı **uzunluğundan bağımsız** 1 bayt,
# `int` **büyüklüğünden bağımsız** 4 bayt sayılıyordu. İkisi de sınırsız.
# Dördüncü bağımsız denetim ölçtü (B-66) ve devralan ajan birebir üretti:
#
#     {"etx": 1.5}                    5 bayt ödendi,      3 bayt taşındı
#     {"a": 2**8192}                  5 bayt ödendi,  1 026 bayt taşındı   205×
#     {"z"*100000: 0}                 5 bayt ödendi, 100 000 bayt taşındı 20 000×
#     tam koşu (212 karakterlik ad)  10 bayt/beacon, ≥1 236 bayt taşındı   124×
#
# Yani `05` §A2 kural 1 *("her alan BAYT OLARAK SAYILIR")* ve K-009'un
# *"eşit kontrol düzlemi bütçesi"* adalet şartı **zorlanmıyordu**: bir
# protokol tüm yönlendirme tablosunu tek bir alan ADINDA taşıyıp bütçenin
# %0,8'ini ödeyebilirdi.
#
# TEL ÜZERİNDEKİ BİÇİM (açıkça ilan edilir, ölçüm bundan çıkar):
#   · alan adı  : **UTF-8 bayt uzunluğu** (eskiden sabit 1)
#   · bool      : 1 bayt
#   · int       : **max(1, ceil(bit_length/8))** — büyüklüğüyle (eskiden 4)
#   · float     : 4 bayt  (tek duyarlık — telemetride tipik)
#   · demet     : elemanların toplamı
#
# 🔒 DEĞİŞMEZ: **ödenen bayt ≥ taşınan bilgi.** `yuk_bayt` bunu her çağrıda
# kendisi doğrular (Y7) ve sağlanmıyorsa `YukHatasi` fırlatır.
#
# ⚠️ MODELLEME KARARI, `08`de beyan edilir: gerçek bir uygulama alan adları
# için 1 baytlık bir KİMLİK TABLOSU kullanırdı; burada tablonun varlığı
# doğrulanamadığı için **adın kendisi** faturalanır. Yön: dürüst bir
# protokolü gerçeğe göre biraz FAZLA ücretlendirir — kaçağa değil, güvenli
# tarafa doğru. Hizalama/dolgu hâlâ yok.
# ==========================================================================

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
        assert math.isnan(deger) or deger == _tek_duyarliga_kirp(deger), (
            f"kırpılmamış bir float ölçüm yoluna ulaştı: {deger!r}. "
            f"`yuku_dondur`un kırpması kalkmış olabilir (B-83/B-112).")
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


# ==========================================================================
# 🔴 B-87 (BEŞİNCİ DENETİM, 26 Ağustos 2026) — `teshis`İN SÖZLEŞMESİ YOKTU
#
# K-056/B-68 kancayı açarken şöyle demişti: *"Kanca `beacon_yuku`nun
# deseniyle **birebir aynı**."* Değildi.
#
#   · `beacon_yuku` → `yuk_bayt()`ten geçer: tip, boyut ve bedel denetlenir,
#     ihlalde **ANINDA** ve **TİPLİ** bir hata fırlar (`YukHatasi`).
#   · `teshis`     → **hiçbir denetimden geçmiyordu.**
#
# Denetçi sekiz sözleşme dışı yük denedi: **8'i de kabul edildi**, **4'ü**
# sonuç yazıcısını **koşu bittikten SONRA** ham bir `TypeError`/`ValueError`
# ile düşürdü — o noktada koşu zaten harcanmıştır. Biri `YASAK_TIPLER`den
# bir **`Konfig`** örneğini sonuç sözlüğüne taşıdı.
#
# 🔒 Şema `05` §D için DONDURULDU (`kosucu.py`: "SLOT ŞİMDİ AÇILIYOR: şema
# Aile 1 başladıktan sonra değiştirilemez"). Sözleşmesi ŞİMDİ yazılmazsa
# sonra yazılamaz.
#
# YÖN: sözleşme, `yuk_bayt`ınkiyle aynı felsefede — **beyan değil ölçüm**.
# Protokolün ne koyduğuna değil, koyduğu şeyin NE OLDUĞUNA bakılır.
# ==========================================================================

TESHIS_EN_UZUN_AD_BAYT = 64      # sayaç adı; sonuç şemasında anahtar olur
TESHIS_EN_UZUN_DIZGI_BAYT = 256  # dizgi değerler
TESHIS_EN_COK_ALAN = 32          # düğüm başına sayaç
TESHIS_EN_COK_ELEMAN = 64        # demet/liste uzunluğu


class TeshisHatasi(ValueError):
    """Protokolün `teshis` kancasından dönen veri sözleşmeye uymuyor."""


def _teshis_deger_dogrula(ad: str, deger, derinlik: int = 0) -> None:
    if isinstance(deger, bool):
        return
    if isinstance(deger, (int, float)):
        # 🔴 Y11 — TİP denetimi bunu KAÇIRIR: `nan` da bir `float`tır.
        # `03` B2: *"NaN'ın sessizce zehirlemesi"* — tek bir NaN, ortalamayı
        # ve düzeltilmiş p'lerin tümünü bozar. `karsilastirma.py` gecikmelerde
        # zaten reddediyor (B-67); teşhis kanalı da reddetmeli, yoksa aynı
        # zehir başka kapıdan girer.
        if isinstance(deger, float) and not math.isfinite(deger):
            raise TeshisHatasi(
                f"{ad!r}: {deger!r} — sonlu olmayan sayı taşınamaz. "
                f"`03` B2: tek bir NaN düzeltilmiş p'lerin tümünü 1,00 yapar.")
        return
    if isinstance(deger, str):
        if len(deger.encode("utf-8")) > TESHIS_EN_UZUN_DIZGI_BAYT:
            raise TeshisHatasi(
                f"{ad!r}: dizgi değer {len(deger.encode('utf-8'))} bayt, "
                f"en çok {TESHIS_EN_UZUN_DIZGI_BAYT}")
        return
    if isinstance(deger, (tuple, list)) and derinlik == 0:
        if len(deger) > TESHIS_EN_COK_ELEMAN:
            raise TeshisHatasi(
                f"{ad!r}: {len(deger)} elemanlı dizi, en çok "
                f"{TESHIS_EN_COK_ELEMAN}. Sonuç şeması teşhis taşır, VERİ değil.")
        for x in deger:
            _teshis_deger_dogrula(ad, x, derinlik + 1)
        return
    raise TeshisHatasi(
        f"{ad!r}: taşınamaz tip {type(deger).__name__}. İzinli: "
        f"bool · int · float · str · bunların düz dizisi. "
        f"(Sonuç sözlüğü JSON'a yazılır; serileştirilemeyen bir değer koşu "
        f"BİTTİKTEN SONRA yazıcıyı düşürür ve koşu harcanmış olur.)")


def teshis_dogrula(dugum: int, veri) -> dict:
    """🔴 `protokol.teshis(dugum)` çıktısının sözleşmesi (B-87).

    `beacon_yuku`nun `yuk_bayt`ı gibi: ihlalde **anında** ve **tipli**
    fırlar. Boş/None kabul edilir ve atlanır.
    """
    if not veri:
        return {}
    if not isinstance(veri, dict):
        raise TeshisHatasi(
            f"düğüm {dugum}: `teshis` bir sözlük döndürmeli, "
            f"{type(veri).__name__} geldi")
    if len(veri) > TESHIS_EN_COK_ALAN:
        raise TeshisHatasi(
            f"düğüm {dugum}: {len(veri)} teşhis alanı, en çok "
            f"{TESHIS_EN_COK_ALAN}")
    for ad, deger in veri.items():
        if not isinstance(ad, str) or not ad:
            raise TeshisHatasi(
                f"düğüm {dugum}: teşhis adı boş olmayan bir DİZGİ olmalı, "
                f"{ad!r} ({type(ad).__name__}) geldi. Sonuç sözlüğü JSON'a "
                f"yazılır ve dizgi olmayan anahtar yazıcıyı düşürür.")
        if len(ad.encode("utf-8")) > TESHIS_EN_UZUN_AD_BAYT:
            raise TeshisHatasi(
                f"düğüm {dugum}: teşhis adı {len(ad.encode('utf-8'))} bayt, "
                f"en çok {TESHIS_EN_UZUN_AD_BAYT}")
        _teshis_deger_dogrula(ad, deger)
    return veri


# Bu tiplerden birine ULAŞILABİLİYORSA sözleşme kırılmıştır.
YASAK_TIPLER = (
    "Kosu", "Topoloji", "KanalErisimi", "Radyo", "Karistirici",
    "OlayKuyrugu", "KorunumDefteri", "Kuyruk", "TrafikUreteci", "Akislar",
    "Konfig", "Paket",
)
