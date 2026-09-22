"""
OLSR mesaj biçimleri ve RFC 3626 sabitleri — TEK KAYNAK.

🔒 NEDEN AYRI DOSYA
===================
`aodv_bicim.py` ile aynı gerekçe: biçimler ve sabitler RFC'nin **alıntısıdır**,
protokolün mantığı değildir. Uygunluk testleri boyutları protokolü hiç
kurmadan sınayabiliyor ve bir sabitin nereden geldiği tek yerde okunuyor.

🔒 BİRİNCİL BELGE — ham metinden, özetten DEĞİL
===============================================
19 Eylül 2026'da RFC 3626'nın ham metni tarayıcıda okundu (`02` §R2.1). Önce
bir web getirme aracının özeti denendi ve **üç hata** taşıyordu (paket başlığı
"16 bayt", HELLO'nun Reserved alanı "13 bit", MAXJITTER "0,04 s"); üçü de ham
metinle karşılaştırılınca yakalandı. Aşağıdaki her genişlik ve her sabit ham
metinden.

🔴 BOYUT RFC ALANLARINDAN TÜRER — PROTOKOL BİR BAYT YAZAMAZ
============================================================
`MesajBicimi` alanları BİT genişliğiyle listeler ve boyutu kendisi hesaplar
(`13` §02.1). Bir OLSR PAKETİ = paket başlığı + mesaj başlığı + gövde:

    paket başlığı   4 bayt   (§3.3)   Packet Length 16 · Packet Seq Number 16
    mesaj başlığı  12 bayt   (§3.3)   Type 8 · Vtime 8 · Size 16 · Originator 32
                                      · TTL 8 · Hop Count 8 · Message Seq 16
    HELLO gövdesi   4 + Σ(4 + 4n)     (§6.1)
    TC gövdesi      4 + 4n            (§9.1)

🔒 **Öz-sınama sayısı belgenin kendisinde:** §3.4 adım 1 *"Packet Length < 16
olan paket sessizce atılır"* der — 16 = 4 + 12. Bu eşitlik bir TESTLE bağlıdır.

🔴 HELLO'NUN BLOK YAPISI BAYT BAYT KORUNUR
==========================================
HELLO, komşu adreslerini bağ koduna göre BLOKLAR hâlinde taşır; her bloğun
kendi 4 baytlık başlığı vardır (Link Code 8 · Reserved 8 · Link Message Size
16). Kontrol düzlemi sözleşmesi her tekrarlı alanı BAĞIMSIZ uzunlukta sayar
(`gozlem/kontrol.py::MesajBicimi.bit`) ve bu yapıyı birebir taşıyabiliyor:
blok başlığı alanları blok sayısı kadar, adres alanı adres sayısı kadar.
Hangi adresin hangi bloğa ait olduğu RFC'deki gibi `Link Message Size`dan
geri çözülür — ek bir alan, dolayısıyla ek bir bayt YOKTUR.

🔴 UYGULANMAYAN RFC ÖZELLİKLERİ — beyan edilir (`06` §4.4 madde 4)
==================================================================
Kural öğrencinin (19 Eylül 2026): **SHOULD uygulanır, MAY beyan edilir.**

🔴 **TEK İSTİSNA — §13 bağ katmanı bildirimi UYGULANIYOR** (öğrenci, 22 Eylül
2026, `04` K-147). Beyanlı sapmayken ÖLÇÜLDÜ (K-146): statik kolun iki
hücresini eşiğin altına itiyordu (0,859 · 0,866; §13 ile 0,926 · 0,908).
AODV bu bilgiyi RFC 3561'in çekirdeği olarak kullanıyor; §13'süz OLSR bilgi
yüzeyi daha dar tek taban olurdu (`03` kural 4).

| özellik | RFC | sözü | neden yok | OLSR'ı zayıflatır mı |
|---|---|---|---|---|
| mesaj birleştirme (piggyback) | §3.4 · §3.5 | MAY | kural; her mesaj kendi paketinde | hayır — yön: her mesaj kendi 4 baytlık paket başlığını öder, OLSR'ı olduğundan **PAHALI** gösterir |
| MPR buluşsalının 5. adımı (fazla MPR'yi ele) | §8.3.1 | MAY | kural | iki yönlü: MPR kümesi en küçükten biraz büyük kalır → TC'yi daha çok düğüm iletir (pahalı) ama taşma daha sağlam |
| MPR kümesi değişince ek HELLO | §8.5 | MAY | kural | küçük: yeni MPR seçimi bir sonraki HELLO'ya (≤ 2 s) kalır |
| MID · HNA | §5 · §12 | — | tek arayüz, dış ağ yok | hayır (uygulanamaz) |
| `TC_REDUNDANCY` > 0 · `MPR_COVERAGE` > 1 | §15 · §16 | — | RFC varsayılanı 0 ve 1 | hayır — varsayılan |
| kısmi HELLO/TC | §6.2 · §9.3 | — | mesaj boyu sınırı yok | hayır |

⚠️ UYGULANAN SHOULD'LAR — kural gereği: bağ histerezisi (§14) · titreşim hem
üretimde hem iletmede (§3.5) · ANSN'nin eklemede de artması (§9.2) · boş
TC'nin `TOP_HOLD_TIME` boyunca sürmesi ve bağ kaybına bağlı MPR seçici
değişikliğinde erken TC (§9.3).
"""

from __future__ import annotations

import math
from fractions import Fraction

from sim2.gozlem.kontrol import MesajBicimi

__all__ = [
    "HELLO", "TC",
    "TIP_HELLO", "TIP_TC",
    "UNSPEC_LINK", "ASYM_LINK", "SYM_LINK", "LOST_LINK",
    "NOT_NEIGH", "SYM_NEIGH", "MPR_NEIGH",
    "WILL_NEVER", "WILL_LOW", "WILL_DEFAULT", "WILL_HIGH", "WILL_ALWAYS",
    "HELLO_INTERVAL_S", "REFRESH_INTERVAL_S", "TC_INTERVAL_S",
    "NEIGHB_HOLD_TIME_S", "TOP_HOLD_TIME_S", "DUP_HOLD_TIME_S",
    "C_S", "MAXJITTER_S", "TC_REDUNDANCY", "MPR_COVERAGE",
    "HYST_THRESHOLD_HIGH", "HYST_THRESHOLD_LOW", "HYST_SCALING",
    "TC_TTL", "BASLIK_BAYT", "bag_kodu", "bag_kodu_coz",
    "zaman_kodla", "zaman_coz",
]

# ==========================================================================
# RFC 3626 §18 · Proposed Values for Constants — ham metinden, birebir
# ==========================================================================
# §18.2 · emission intervals
HELLO_INTERVAL_S: float = 2.0
REFRESH_INTERVAL_S: float = 2.0
TC_INTERVAL_S: float = 5.0
# §18.3 · holding times — RFC'nin kendi TÜRETMELERİ
NEIGHB_HOLD_TIME_S: float = 3 * REFRESH_INTERVAL_S          # 6 s
TOP_HOLD_TIME_S: float = 3 * TC_INTERVAL_S                  # 15 s
DUP_HOLD_TIME_S: float = 30.0
# §18.1 · Vtime/Htime ölçeği
C_S: float = 1.0 / 16.0
# §18.4 · mesaj tipleri
TIP_HELLO: int = 1
TIP_TC: int = 2
# §18.5 · bağ tipleri
UNSPEC_LINK: int = 0
ASYM_LINK: int = 1
SYM_LINK: int = 2
LOST_LINK: int = 3
# §18.6 · komşu tipleri
NOT_NEIGH: int = 0
SYM_NEIGH: int = 1
MPR_NEIGH: int = 2
# §18.7 · bağ histerezisi (§14 — SHOULD, uygulanıyor)
HYST_THRESHOLD_HIGH: float = 0.8
HYST_THRESHOLD_LOW: float = 0.3
HYST_SCALING: float = 0.5
# §18.8 · istek (willingness)
WILL_NEVER: int = 0
WILL_LOW: int = 1
WILL_DEFAULT: int = 3
WILL_HIGH: int = 6
WILL_ALWAYS: int = 7
# §18.9 · çeşitli
TC_REDUNDANCY: int = 0
MPR_COVERAGE: int = 1
MAXJITTER_S: float = HELLO_INTERVAL_S / 4                   # 0,5 s
# §9.1 · *"The time to live SHOULD be set to 255 (maximum value)"*
TC_TTL: int = 255

# §3.4 adım 1 · *"Packet Length < 16 MUST silently be discarded"* — 4 + 12.
BASLIK_BAYT: int = 16


def bag_kodu(komsu_tipi: int, bag_tipi: int) -> int:
    """§6.1.1 · Link Code = komşu tipi (bit 3–2) · bağ tipi (bit 1–0)."""
    return (komsu_tipi << 2) | bag_tipi


def bag_kodu_coz(kod: int) -> tuple[int, int]:
    """(komşu tipi, bağ tipi)."""
    return (kod >> 2) & 0b11, kod & 0b11


# ==========================================================================
# §18.3 · Vtime / Htime — mantis-üs kodlaması
#
#     değer = C · (1 + a/16) · 2^b      a: üst dört bit · b: alt dört bit
#
# 🔒 KODLAMA YUKARI YUVARLAR (RFC: *"rounded up"*). Kesir aritmetiğiyle
# yapılır: 15 s için 16·(240/128 − 1) tam olarak 14'tür ve kayan nokta onu
# 14,0000001'e kaydırırsa tavan 15 verir — bir bitlik kodlama hatası.
# 🔒 Belge dört çözülmüş örnek veriyor ve bunlar bir TESTLE bağlı:
#     2 s → (0, 5) · 6 s → (8, 6) · 15 s → (14, 7) · 30 s → (14, 8)
# ==========================================================================
def zaman_kodla(t_s: float) -> int:
    """Saniye → bir baytlık Vtime/Htime alanı."""
    x = Fraction(t_s).limit_denominator(1 << 20) / Fraction(1, 16)
    if x < 1:
        raise ValueError(f"{t_s} s, C'den küçük — kodlanamaz")
    b = 0
    while Fraction(2) ** (b + 1) <= x:
        b += 1
    a = math.ceil(16 * (x / Fraction(2) ** b - 1))
    if a == 16:
        a, b = 0, b + 1
    if not (0 <= a <= 15 and 0 <= b <= 15):
        raise ValueError(f"{t_s} s kodlama aralığının dışında (a={a}, b={b})")
    return a * 16 + b


def zaman_coz(bayt: int) -> float:
    """Bir baytlık Vtime/Htime alanı → saniye."""
    a, b = bayt >> 4, bayt & 0x0F
    return C_S * (1 + a / 16) * (2 ** b)


# ==========================================================================
# RFC 3626 §3.3 · §6.1 · §9.1 · Message Formats
#
# 🔒 Her biçim önce paket başlığını, sonra mesaj başlığını, sonra gövdeyi
# taşır: bu modelde bir paket TEK bir mesaj taşır (birleştirme MAY, beyanlı).
# Paket başlığı atlama başınadır — iletirken düğüm KENDİ paket sırasını yazar;
# mesaj başlığı mesajla birlikte yolculuk eder (§3.4.1 adım 8: *"the remaining
# fields of the message header SHOULD be left unmodified"*).
# ==========================================================================
_BASLIK: tuple[tuple[str, int], ...] = (
    # §3.3.1 · paket başlığı — 32 bit
    ("paket_boyu", 16),
    ("paket_sira", 16),
    # §3.3.2 · mesaj başlığı — 96 bit
    ("mesaj_tipi", 8),
    ("vtime", 8),
    ("mesaj_boyu", 16),
    ("kaynak", 32),            # Originator Address
    ("ttl", 8),
    ("atlama", 8),             # Hop Count
    ("mesaj_sira", 16),
)

# §6.1 — Reserved(16) · Htime(8) · Willingness(8), sonra bağ kodu blokları.
HELLO = MesajBicimi("HELLO", _BASLIK + (
    ("ayrilmis", 16),
    ("htime", 8),
    ("istek", 8),              # Willingness
), tekrarli=(
    # Blok başına: Link Code(8) · Reserved(8) · Link Message Size(16).
    ("blok_kodu", 8),
    ("blok_ayrilmis", 8),
    ("blok_boyu", 16),
    # Adres başına: Neighbor Interface Address(32). Hangi bloğa ait olduğu
    # `blok_boyu`ndan geri çözülür — RFC'nin kendi yolu, ek bayt yok.
    ("komsu_adresi", 32),
))

# §9.1 — ANSN(16) · Reserved(16), sonra ilan edilen komşu adresleri.
TC = MesajBicimi("TC", _BASLIK + (
    ("ansn", 16),
    ("ayrilmis", 16),
), tekrarli=(
    ("komsu_adresi", 32),      # Advertised Neighbor Main Address
))
