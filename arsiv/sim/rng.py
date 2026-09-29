"""
Rastgelelik akışları.

NEDEN BU DOSYA AYRI VE NEDEN BU KADAR YORUM VAR
------------------------------------------------
Bu dosyadaki bir hata, "kod doğru, testler geçiyor, sonuç sessizce yanlış"
sınıfına girer. Sıradan kod incelemesiyle bulunamaz.

İki ayrı mekanizma var ve KARIŞTIRILMAMALIDIR:

1) AYRIK AKIŞLAR (sıralı, durum tutan)
   Her rastgelelik kaynağı kendi akışını kullanır. Tek bir akış kullanılsaydı,
   keşif yapan bir protokol keşif yapmayandan daha çok sayı çekerdi; sonraki
   tüm çekimler kayardı; protokoller FARKLI SENARYOLAR görürdü. 30 tohum bunu
   kurtarmaz. (03-YONTEM-KURALLARI.md, Bölüm C)

2) SAYAÇ TABANLI KANAL (durumsuz)
   Kanal hatası her iletim denemesinde bir sayı çeker. Bu sıralı bir akıştan
   gelseydi, daha çok deneme yapan protokol akışı kaydırırdı ve aynı tohumda
   FARKLI KANAL GERÇEKLEMESİ oluşurdu.

   Çözüm: kanal çekimi hash(tohum, gönderen, alan, zaman_dilimi)'dir.
   Sıralı durum yok. Aynı anda aynı çift arasındaki iletim, hangi protokol
   koşarsa koşsun aynı sonucu görür.

   Kazanç: iki kol arasındaki fark artık kanal gürültüsünün farklı
   çekilmesinden değil, YALNIZCA protokol davranışından gelir.
"""

from __future__ import annotations

import hashlib
import random
import struct


# 07-SIMULATOR-ARAYUZ.md, "RASTGELELİK AKIŞLARI" tablosu.
# Bu liste kapalıdır: yeni bir rastgelelik kaynağı eklemek, bu listeye
# eklemeyi ve NEDEN-BOYLE.md'ye kayıt düşmeyi gerektirir.
AKIS_ADLARI = (
    "yerlesim",           # düğüm konumları
    "trafik_ciftleri",    # kaynak-hedef seçimi
    "trafik_zamani",      # CBR titreşimi
    "beacon_faz",         # beacon başlangıç fazı — 🔴 B-10'da eklendi
    "mac_geri_cekilme",   # çakışma sonrası bekleme
    "karistirici_faz",    # darbeli karıştırıcının başlangıç fazı
    "protokol_kesif",     # keşif kararları — protokole özel
)

# 🔴 B-10 — "beacon_faz" NEDEN EKLENDİ (19 Ağustos 2026, K-040)
# ---------------------------------------------------------------------------
# `Kosu._beaconlari_basla` beacon fazlarını "trafik_zamani" akışından
# çekiyordu. O akışın tanımı ise "CBR titreşimi"dir. Yani belgelenmemiş bir
# rastgelelik kaynağı, başka bir kaynağın akışına biniyordu.
#
# Bugün eşleştirmeyi bozmuyordu (beacon çekim sayısı `dugum_sayisi`den, yani
# konfigürasyondan belirlenir; protokolden değil). AMA akış paylaşımı tam
# olarak bu dosyanın önlemek için yazıldığı kuplajı geri getiriyordu: akış
# üzerindeki çekim sırasını değiştiren HERHANGİ bir gelecek değişiklik
# (beacon zamanlamasına titreşim eklemek, ısınma öncesi ek bir kaynak) CBR
# titreşim dizisini de kaydırırdı.
#
# ⚠️ BEDELİ ÖDENDİ: ayrı akışa geçmek çekim sırasını değiştirdiği için
# 19 Ağustos'tan önce ölçülmüş TÜM sayılar biraz kaydı. Aile 0 kapanışında
# hepsi zaten yeniden koşulacaktı; şimdi yapmak sonra yapmaktan ucuzdu
# (`03` Bölüm C: "ayrık RNG akışları SONRADAN EKLENEMEZ").

# Bildirilmiş ama henüz hiçbir yerden çekim almayan akışlar.
# `tests/test_rng.py::test_b10_her_akis_ya_kullaniliyor_ya_beyan_edilmis`
# bu listeyi zorlar: bir akış ya fiilen kullanılır ya BURADA yazılıdır.
# "protokol_kesif" Aile 1'in protokolleri için ayrılmıştır.
HENUZ_KULLANILMAYAN = ("protokol_kesif",)

_UINT64 = (1 << 64) - 1


def _hash64(*parcalar: bytes) -> int:
    """Parçalardan 64 bitlik belirlenimci bir tam sayı üretir.

    blake2b kullanılıyor çünkü Python'un yerleşik hash()'i çalışmalar arasında
    tuzlanır (PYTHONHASHSEED) ve BELİRLENİMCİ DEĞİLDİR. hash() kullanmak bu
    projede sessiz bir belirlenimsizlik kaynağı olurdu.
    """
    h = hashlib.blake2b(digest_size=8)
    for p in parcalar:
        h.update(p)
        h.update(b"\x1f")  # parça ayırıcı: ("ab","c") ile ("a","bc") ayrışsın
    return int.from_bytes(h.digest(), "big")


class Akislar:
    """Ayrık, sıralı rastgelelik akışları.

    Kullanım:
        akislar = Akislar(ana_tohum=1000)
        akislar["yerlesim"].uniform(0, 1000)
    """

    def __init__(self, ana_tohum: int) -> None:
        self.ana_tohum = int(ana_tohum)
        self._akislar: dict[str, random.Random] = {}
        for ad in AKIS_ADLARI:
            tohum = _hash64(str(self.ana_tohum).encode(), ad.encode())
            self._akislar[ad] = random.Random(tohum)

    def __getitem__(self, ad: str) -> random.Random:
        if ad not in self._akislar:
            # Sessizce yeni akış yaratmıyoruz: listede olmayan bir akış,
            # belgelenmemiş bir rastgelelik kaynağı demektir.
            raise KeyError(
                f"bilinmeyen akış: {ad!r}. Yeni akış AKIS_ADLARI'na eklenmeli "
                f"ve NEDEN-BOYLE.md'ye kayıt düşülmeli."
            )
        return self._akislar[ad]

    def __contains__(self, ad: str) -> bool:
        return ad in self._akislar


def kanal_cekimi(
    ana_tohum: int,
    gonderen: int,
    alan: int,
    zaman_s: float,
    dilim_s: float,
) -> float:
    """Kanal hatası için [0, 1) aralığında DURUMSUZ bir çekim.

    Aynı (tohum, gönderen, alan, zaman dilimi) dörtlüsü her zaman aynı sayıyı
    verir — hangi protokolün koştuğundan, kaç iletim yapıldığından bağımsız.

    ZAMAN DİLİMİ NEDEN VAR
    ----------------------
    İki protokol aynı iletimi birbirinden mikrosaniyelerle farklı anlarda
    başlatabilir. Zaman ham hâliyle hash'e girseydi, bu minik fark farklı bir
    çekim üretir ve mekanizmanın amacı boşa giderdi.

    Dilim iki yönden sıkışıktır:
      - fazla İNCE olursa protokoller arası mikrosaniyelik zaman farkını
        yutamaz ve eşleştirme zayıflar
      - fazla KABA olursa aynı çiftin ardışık denemeleri aynı dilime düşer,
        AYNI çekimi alır ve yeniden deneme mekanizması sessizce işlevsizleşir

    🔴 VARSAYILAN DEĞER YOKTUR — bilerek. Bir varsayılan, `Konfig` ile ikinci
    bir "doğru" kaynağı yaratırdı: biri güncellenirken diğeri unutulurdu.
    Bu tam olarak bir kez yaşandı (K-024: konfig 100 µs'ye indi, rng'nin
    varsayılanı 1 ms'de kaldı). Çağıran `kon.kanal_dilimi_s` geçmek zorunda.
    """
    dilim = int(zaman_s // dilim_s)
    ham = _hash64(
        struct.pack("<q", int(ana_tohum)),
        struct.pack("<i", int(gonderen)),
        struct.pack("<i", int(alan)),
        struct.pack("<q", dilim),
    )
    return ham / (_UINT64 + 1)
