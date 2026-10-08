"""
Rastgelelik — iki ayrı mekanizma, karıştırılmaz.

Bu dosyadaki bir hata *"kod doğru, testler geçiyor, sonuç sessizce yanlış"*
sınıfına girer ve sıradan kod incelemesiyle bulunamaz.

┌─ 1) SIRALI AKIŞLAR (`AKIS_ADLARI`) — durum tutar, SIRA DUYARLI
│  Her kaynak kendi akışını kullanır. Tek akış olsaydı, keşif yapan bir
│  protokol keşif yapmayandan çok sayı çeker, sonraki tüm çekimler kayar ve
│  protokoller FARKLI SENARYOLAR görürdü. 30 tohum bunu kurtarmaz —
│  eşleştirme *yapısal* olarak kırılır.
│
│  ⚠️ BURADAKİ AÇIKLAMA 4 EYLÜL 2026'DA DÜZELTİLDİ — önceki hâli KODLA
│  ÇELİŞİYORDU. Şöyle diyordu: *"Bu listeye akış eklemek çekim sırasını
│  kaydırır ve daha önce ölçülmüş HER SAYIYI bayatlatır."* Ölçüldü ve
│  YANLIŞ çıktı: listenin ortasına yeni bir akış eklendiğinde eski 15
│  akışın 50'şer çekiminin **hiçbiri** değişmiyor. Sebep aşağıda, `Akislar.
│  __init__`te: her akış KENDİ ADINDAN tohumlanır
│  (`Random(blake2b(ana_tohum, akış_adı))`), akışlar arasında paylaşılan bir
│  sıra yoktur.
│
│  🔴 GERÇEK TEHLİKE BAŞKA ve daha incedir: sırayı kaydıran şey listeye ad
│  eklemek değil, **var olan bir akıştan fazladan çekim yapmaktır**. Bir kol
│  bir akıştan 3, öteki 4 kez çekerse o akışın kalan dizisi kollar arasında
│  ayrışır. `protokol_kesif`in düğüm başına alt akış zorunluluğu tam bu
│  yüzdendir.
│
│  🔒 Liste yine de **kapalı ve küçük** tutulur, ama gerekçesi artık doğru
│  olanı: liste değişince `akis_listesi_hash` değişir ve iki sonuç satırı
│  BİÇİMSEL olarak karşılaştırılamaz hâle gelir — sayılar kaymasa bile.
│  Yani bedel fiziksel değil, kayıt disiplinine ait.
│
└─ 2) HASH ALANLARI (`HASH_ALANLARI`) — DURUMSUZ, sıra duyarsız
   Çekim `hash(alan, tohum, *anahtarlar)`tır. Sıralı durum yok; kaç kez
   çekildiği önemsiz. 🟢 **Yeni bir hash alanı eklemek hiçbir eski çekimi
   kaydırmaz.**

🔒 KURAL: yeni bir rastgelelik kaynağı **önce hash alanı olarak** denenir.
Sıralı akış ancak gerçekten durum taşımak zorunluysa açılır. Eski simülatörde
bu ayrım yoktu; gölgeleme ve mobilite tam bu yüzden eklenemiyordu.

⭐ Kanal çekiminin durumsuz olması, literatürün *"ön-üretilmiş iz dosyası"*
önerisinden güçlüdür: desenkronizasyon **yapısal olarak imkânsızdır**, bir
dosyayı doğru okumaya bağlı değildir.
"""

from __future__ import annotations

import hashlib
import math
import random
import struct

import numpy as np

__all__ = [
    "AKIS_ADLARI", "HASH_ALANLARI", "HENUZ_KULLANILMAYAN",
    "Akislar", "hash_cekimi", "normal_cekimi", "blok_anahtari",
    "normal_dizisi",
    "akis_listesi_hash",
]

# ===========================================================================
# 1 · SIRALI AKIŞLAR — sıra duyarlı, liste KAPALI
# ===========================================================================
AKIS_ADLARI: tuple[str, ...] = (
    # dünya kurulumu
    "yerlesim",              # düğüm x, y
    "irtifa",                # düğüm z — ayrı akış: irtifa bandı bir eksendir
    # mobilite — üç yenilik AYRI akışta, çünkü tek akışta güncelleme
    # sırası (hız → azimut → pitch) anlam kazanır ve sıra bir modelleme
    # kararı olmadığı hâlde sonucu etkilerdi
    "mobilite_hiz",
    "mobilite_azimut",
    "mobilite_pitch",
    # görev tabanlı kol — müfreze merkezleri, istasyon konumları, üye titreşimi
    "gorev_merkez",
    "gorev_istasyon",
    "gorev_jitter",
    # formasyon kolu — istasyon kayma yönü ve manevra gürültüsü (`v2/07` §18 Y6)
    "formasyon_jitter",
    # saat — düğüm başına kayma ve sapma, kurulumda bir kez
    "saat_ofset",
    "saat_sapma",
    # trafik
    "trafik_ciftleri",
    "trafik_zamani",
    # MAC ve kontrol düzlemi
    "beacon_faz",
    "mac_geri_cekilme",
    # karıştırıcı — kurulumda çekilenler (konum, faz); tepki verenler HASH'te
    "karistirici_yerlesim",
    "karistirici_faz",
    # protokol
    "protokol_kesif",        # 🔒 düğüm başına ALT AKIŞ zorunlu (aşağı bak)
    # ölçüm — karara giremez
    "olcum_orneklemesi",
)

# Bildirilmiş ama henüz çekim almayan akışlar. Bir akış ya fiilen kullanılır
# ya BURADA yazılıdır — "bildirim ≠ kullanım" tuzağının RNG'deki karşılığı.
HENUZ_KULLANILMAYAN: tuple[str, ...] = (
    # Adım 4 — kanal/karistirici. Karıştırıcının konumu ve fazı ŞU AN sabit
    # (alanın merkezi, faz 0); rastgeleleştirilirse bu akışlar açılır.
    "karistirici_yerlesim", "karistirici_faz",
    # 🔒 `beacon_faz` 5 Eylül 2026'da listeden ÇIKTI (`kosum/kurulum.py` düğüm
    # başına beacon fazını ondan çekiyor); `protokol_kesif` 14 Eylül 2026'da
    # çıktı (Y3 · R4: `kosum/kontrol.py` titreşimi düğüm alt akışından çeker).
    # Adım 8 — olcum
    "olcum_orneklemesi",
)

# ===========================================================================
# 2 · HASH ALANLARI — durumsuz, serbestçe genişletilebilir
# ===========================================================================
HASH_ALANLARI: tuple[str, ...] = (
    "kanal_karar",       # (tohum, gönderen, alan, zaman_dilimi)
    "golgeleme",         # (tohum, min(i,j), max(i,j), hücre_x, hücre_y, hücre_z)
    "sonumleme_i",       # (tohum, i, j, yenilik_indeksi)  — I bileşeni
    "sonumleme_q",       # (tohum, i, j, yenilik_indeksi)  — Q bileşeni
    "reaktif_sezme",     # 🔴 sıralı OLAMAZ: iletim sayısı protokole göre değişir
    "taramali_konak",    # (tohum, konak_indeksi)
    "aldatici_icerik",   # (tohum, sahte_çerçeve_indeksi)
)

_UINT64 = (1 << 64) - 1
_AYIRICI = b"\x1f"


def _hash_bit(*parcalar: bytes, bayt: int = 8) -> int:
    """Parçalardan belirlenimci bir tam sayı.

    🔒 `blake2b`, Python'un `hash()`i DEĞİL: `hash()` çalışmalar arasında
    `PYTHONHASHSEED` ile tuzlanır ve belirlenimci değildir. Bu projede
    `hash()` kullanmak sessiz bir belirlenimsizlik kaynağı olurdu.

    Parça ayırıcı zorunlu: ("ab", "c") ile ("a", "bc") aynı özeti vermemeli.
    """
    h = hashlib.blake2b(digest_size=bayt)
    for p in parcalar:
        h.update(p)
        h.update(_AYIRICI)
    return int.from_bytes(h.digest(), "big")


def _anahtar_baytlari(anahtarlar: tuple) -> list[bytes]:
    """Anahtarları sabit genişlikli bayta çevirir.

    Sabit genişlik şart: `(1, 23)` ile `(12, 3)` metin olarak birleştirilseydi
    aynı diziyi verirdi.
    """
    cikti: list[bytes] = []
    for a in anahtarlar:
        if isinstance(a, bool):
            cikti.append(struct.pack("<?", a))
        elif isinstance(a, int):
            cikti.append(struct.pack("<q", a))
        elif isinstance(a, float):
            cikti.append(struct.pack("<d", a))
        elif isinstance(a, str):
            cikti.append(a.encode("utf-8"))
        else:
            raise TypeError(
                f"hash anahtarı int/float/str/bool olmalı: {type(a).__name__}")
    return cikti


# ---------------------------------------------------------------- sıralı
class Akislar:
    """Ayrık, sıralı rastgelelik akışları.

        akislar = Akislar(ana_tohum=1000)
        akislar["yerlesim"].uniform(0, 1000)
        akislar.dugum("protokol_kesif", 7).random()
    """

    __slots__ = ("ana_tohum", "_akislar", "_dugum_akislari")

    def __init__(self, ana_tohum: int) -> None:
        self.ana_tohum = int(ana_tohum)
        self._akislar: dict[str, random.Random] = {}
        self._dugum_akislari: dict[tuple[str, int], random.Random] = {}
        for ad in AKIS_ADLARI:
            self._akislar[ad] = random.Random(
                _hash_bit(struct.pack("<q", self.ana_tohum), ad.encode()))

    def __getitem__(self, ad: str) -> random.Random:
        try:
            return self._akislar[ad]
        except KeyError:
            # Sessizce yeni akış yaratmıyoruz: listede olmayan bir akış,
            # belgelenmemiş bir rastgelelik kaynağı demektir.
            raise KeyError(
                f"bilinmeyen akış: {ad!r}. Önce HASH_ALANLARI'nı dene; "
                f"gerçekten durum gerekiyorsa AKIS_ADLARI'na ekle — ve bunun "
                f"daha önce ölçülmüş her sayıyı bayatlattığını bil.") from None

    def __contains__(self, ad: str) -> bool:
        return ad in self._akislar

    def dugum(self, ad: str, dugum: int) -> random.Random:
        """Düğüm başına alt akış.

        🔒 `protokol_kesif` için **zorunlu**: tek akışta düğüm A'nın çektiği
        sayı adedi düğüm B'nin dizisini kaydırır ve düğümler arası sessiz bir
        kuplaj doğar.
        """
        if ad not in self._akislar:
            raise KeyError(f"bilinmeyen akış: {ad!r}")
        anahtar = (ad, int(dugum))
        akis = self._dugum_akislari.get(anahtar)
        if akis is None:
            akis = random.Random(_hash_bit(
                struct.pack("<q", self.ana_tohum), ad.encode(),
                struct.pack("<q", int(dugum))))
            self._dugum_akislari[anahtar] = akis
        return akis


# --------------------------------------------------------------- durumsuz
def hash_cekimi(alan: str, ana_tohum: int, *anahtarlar) -> float:
    """`[0, 1)` aralığında DURUMSUZ çekim.

    Aynı `(alan, tohum, anahtarlar)` her zaman aynı sayıyı verir — hangi
    protokolün koştuğundan, kaç çekim yapıldığından bağımsız.

    🔒 Alan adı özete girer: iki farklı alan aynı anahtarlarla çağrılsa bile
    çakışmaz.
    """
    if alan not in HASH_ALANLARI:
        raise KeyError(
            f"bilinmeyen hash alanı: {alan!r}. HASH_ALANLARI'na eklemek "
            f"serbesttir ve eski çekimleri KAYDIRMAZ.")
    ham = _hash_bit(alan.encode(), struct.pack("<q", int(ana_tohum)),
                    *_anahtar_baytlari(anahtarlar))
    return ham / (_UINT64 + 1)


def normal_cekimi(alan: str, ana_tohum: int, *anahtarlar) -> float:
    """Standart normal `N(0, 1)` — durumsuz, Box-Muller.

    İki bağımsız düzgün çekim **tek bir 128 bitlik özetin iki yarısından**
    alınır; ikinci bir hash çağrısı gerekmez ve alan/anahtar aynı kalır.

    Gölgeleme (X_σ) ve sönümleme yenilikleri bunu kullanır: ikisi de bağa ve
    zamana göre yeniden üretilebilir olmak zorunda.
    """
    if alan not in HASH_ALANLARI:
        raise KeyError(f"bilinmeyen hash alanı: {alan!r}")
    ham = _hash_bit(alan.encode(), struct.pack("<q", int(ana_tohum)),
                    *_anahtar_baytlari(anahtarlar), bayt=16)
    ust = (ham >> 64) & _UINT64
    alt = ham & _UINT64
    # u1 asla 0 olmamalı (log(0)); en küçük pozitif değere kelepçele.
    u1 = max(ust / (_UINT64 + 1), 1.0 / (_UINT64 + 1))
    u2 = alt / (_UINT64 + 1)
    return math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)


# ---------------------------------------------------------- durumsuz · blok
# 🔒 K-198 · SAYAÇ TABANLI BLOK ÜRETECİ (28 Eylül 2026, öğrenci onayı).
# `normal_cekimi` her yenilik için bir blake2b özeti hesaplıyor (~10 µs);
# birincil hücrede sönümleme yeniliklerinin üretimi koşunun ~%30'uydu.
# Burada bağ başına BİR blake2b özeti anahtar olur; indeks `n`in değeri
# SplitMix64'ün `n`inci çıktısıdır: `karıştır(anahtar + (n + 1)·γ)` — saf,
# rastgele erişimli, sıra duyarsız (durumsuzluk sözleşmesi aynı). Normal,
# ardışık iki indeksin çiftinden Box-Muller'ın cos ve sin kolu: çift
# `(2p, 2p+1)` hep birlikte üretilir, yani bir indeksin değeri hangi
# pencereden okunursa okunsun AYNIDIR (pencere başı çift olmak zorunda).
# SplitMix64: Steele, Lea ve Flood 2014 (OOPSLA, "Fast splittable
# pseudorandom number generators"); Java `SplittableRandom`ın çekirdeği.
_GAMA = np.uint64(0x9E3779B97F4A7C15)
_KARISTIR_1 = np.uint64(0xBF58476D1CE4E5B9)
_KARISTIR_2 = np.uint64(0x94D049BB133111EB)
_KAYDIR = (np.uint64(30), np.uint64(27), np.uint64(31), np.uint64(11))
_IKI_UZERI_53 = 1.0 / 9007199254740992.0


def blok_anahtari(alan: str, ana_tohum: int, *anahtarlar) -> int:
    """Bir bağın blok üreteci anahtarı — 64 bit, blake2b.

    🔒 Alan adı ve `b"blok"` etiketi özete girer: aynı alanın `normal_cekimi`
    çekimleriyle ve öteki bağların anahtarlarıyla çakışmaz."""
    if alan not in HASH_ALANLARI:
        raise KeyError(f"bilinmeyen hash alanı: {alan!r}")
    return _hash_bit(alan.encode(), struct.pack("<q", int(ana_tohum)), b"blok",
                     *_anahtar_baytlari(anahtarlar))


def normal_dizisi(anahtarlar: np.ndarray, bas: int, uzunluk: int
                  ) -> np.ndarray:
    """İndeks `bas … bas + uzunluk − 1` için `N(0, 1)` yenilikler.

    `anahtarlar` `(s, 1)` biçiminde `uint64` (her satır bir akış, ör. I ve
    Q); dönüş `(s, uzunluk)`. `bas` ve `uzunluk` ÇİFT olmalı — Box-Muller
    çifti bölünmesin. `bas` negatif olabilir (64 bitte sarılır).
    """
    if bas % 2 or uzunluk % 2:
        raise ValueError("blok başı ve uzunluğu çift olmalı (Box-Muller çifti)")
    sayac = (np.arange(uzunluk, dtype=np.uint64)
             + np.uint64(bas & _UINT64) + np.uint64(1))
    z = anahtarlar + sayac * _GAMA
    z = (z ^ (z >> _KAYDIR[0])) * _KARISTIR_1
    z = (z ^ (z >> _KAYDIR[1])) * _KARISTIR_2
    z = z ^ (z >> _KAYDIR[2])
    u = (z >> _KAYDIR[3]).astype(np.float64) * _IKI_UZERI_53     # [0, 1)
    r = np.sqrt(-2.0 * np.log(1.0 - u[:, 0::2]))                 # (0, 1]
    teta = (2.0 * math.pi) * u[:, 1::2]
    cikti = np.empty(u.shape, dtype=np.float64)
    cikti[:, 0::2] = r * np.cos(teta)
    cikti[:, 1::2] = r * np.sin(teta)
    return cikti


def akis_listesi_hash() -> str:
    """İki listenin parmak izi — sonuç satırına yazılır.

    Listeler sessizce değişirse iki sonuç satırı **karşılaştırılamaz** hâle
    gelir; bu özet o karşılaştırmayı bir kapıya bağlar.
    """
    h = hashlib.blake2b(digest_size=8)
    for ad in AKIS_ADLARI:
        h.update(b"S")
        h.update(ad.encode())
        h.update(_AYIRICI)
    for ad in HASH_ALANLARI:
        h.update(b"H")
        h.update(ad.encode())
        h.update(_AYIRICI)
    return h.hexdigest()
