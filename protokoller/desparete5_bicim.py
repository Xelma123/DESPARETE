"""
DESPARETE 5 · değerler, bayraklar, ileti biçimleri ve birimler — TEK KAYNAK.

Kural kâğıtları `v2/kural/KK-00`…`KK-05`; tasarım kararları `v2/17` (T-n).
Kod yorumları kâğıdın kural numarasına (`KK-01/7`) ve karara (`T-2`) atıf
verir. v0.4.1'in dosyaları (`desparete*.py`) karşılaştırma için durur; bu
sürüm onlardan hiçbir şey içe aktarmaz.

🔒 DEĞERLER BAŞLANGIÇTIR (KK-00 "Başlangıç değerleri")
Değerler `Degerler` içinde tek yerde durur; A/B'de `dataclasses.replace` ile
değişir ve koşu kimliğine girer (`kimlik_parametreleri`). Hiçbiri tek bir
karıştırıcı çizelgesine göre seçilmez (`17` İlke 3).

🔒 BAYRAKLAR (KK-00 "Mekanizmalar, bayraklar, sınıflar")
Karıştırmaya karşı: `karistirma_durumu` · `alici_bildirimi` ·
`hatirlanan_kalite` · `cogaltma`. Genel: `veri_kotu_tetigi` ·
`uyarlanir_aralik` · `istege_bagli_esik` · `bekletme`. Çekirdek
mekanizmaların (selamdan ETX, iki eşik, silme, ara ilan, döngüsüzlük, geri iz)
bayrağı yoktur.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, fields

from sim2.gozlem.kontrol import MesajBicimi

__all__ = [
    "OLCEK", "SONLU_EN_COK", "SONSUZ", "maliyet_birimi", "maliyet_topla",
    "sira_artir", "sira_farki", "sira_buyuk", "Degerler", "Bayraklar",
    "TAM", "CEKIRDEK", "SELAM", "TUR_ISTEGI", "ADRES_BIT", "ORAN_EN_COK",
    "ARALIK_BIRIMI_S",
]

# ==========================================================================
# BİRİMLER — KK-00 genel kural 3
# ==========================================================================
OLCEK: int = 64                 # maliyet = ETX × 64, tamsayı
SONLU_EN_COK: int = 0xFFFE      # sonlu maliyetin tavanı
SONSUZ: int = 0xFFFF            # ∞ (geri çekme)
ADRES_BIT: int = 8              # selamdaki komşu adresi (≤ 255 düğüm)
ORAN_EN_COK: int = 255          # `d_r` × 255, aşağı yuvarlanır
ARALIK_BIRIMI_S: float = 0.01   # selamın `aralik` alanının birimi


def maliyet_birimi(etx: float) -> int:
    """ETX → ETX × 64, yukarı yuvarlanır; sonlu en çok 0xFFFE, ∞ → 0xFFFF."""
    if not math.isfinite(etx):
        return SONSUZ
    # Kayan noktanın 64·1,5 = 96,00000001 gibi artığı yukarı yuvarlamayı
    # bozmasın: 1e-9'luk pay.
    return min(SONLU_EN_COK, max(0, math.ceil(etx * OLCEK - 1e-9)))


def maliyet_topla(a: int, b: int) -> int:
    """İki maliyetin toplamı; biri ∞ ise ∞, sonlu toplam 0xFFFE'de doyar."""
    if a >= SONSUZ or b >= SONSUZ:
        return SONSUZ
    return min(SONLU_EN_COK, a + b)


def sira_artir(s: int, n: int = 1) -> int:
    """16 bitlik sıra ya da tur: s + n (mod 2^16)."""
    return (s + n) & 0xFFFF


def sira_farki(yeni: int, eski: int) -> int:
    """(yeni − eski) mod 2^16, işaretli: [−32768, 32767]. KK-01/2'nin
    boşluğu ve geri alması bu farktan okunur."""
    f = (yeni - eski) & 0xFFFF
    return f - 0x10000 if f >= 0x8000 else f


def sira_buyuk(a: int, b: int) -> bool:
    """a > b (mod 2^16) — tur karşılaştırması (KK-04/1)."""
    return sira_farki(a, b) > 0


# ==========================================================================
# DEĞERLER — KK-00 "Başlangıç değerleri (tek yer)"
# ==========================================================================
@dataclass(frozen=True, slots=True)
class Degerler:
    # --- KK-01 · bağın ölçüsü ve durumu ---------------------------------
    N: int = 16                         # selam geçmişi
    ORNEK_EN_AZ: int = 4                # KÖTÜ → OLAĞAN ve listeye giriş
    E_CIK: float = 4.0                  # ETX bunu aşınca kullanılmaz
    E_DON: float = 3.0                  # bunun altına inince döner
    VERI_PENCERE: int = 8               # son veri çerçevesi sayısı
    VERI_PENCERE_S: float = 10.0        # ... en çok bu kadar geriye
    VERI_EN_AZ: int = 4                 # pencerede en az çerçeve
    ASKIDA_TAVAN_S: float = 10.0        # ASKIDA_SURE = min((k+1)·a, tavan)
    ASKIDA_TABAN_S: float = 1.0         # ... en az (Y-1 karıştırma A/B'sinden önce)
    T_HATIRA_S: float = 30.0            # KARIŞTIRILIYOR'un üst süresi
    T_CEZA_S: float = 10.0              # veriyle KÖTÜ'nün en kısa süresi
    T_CEZA_EN_COK_S: float = 40.0
    CEZA_YINELEME_S: float = 60.0       # bu sürede yinelenirse ×2
    T_SILME_S: float = 30.0             # hiç duyulmazsa silinir
    ZAMAN_ASIMI_KATSAYI: float = 1.5    # × komşunun aralığı
    # --- KK-02 · selam ----------------------------------------------------
    I_MIN_S: float = 0.5
    I_MAX_S: float = 2.0
    TITRESIM_ORANI: float = 0.1         # titreşim U(0, 0,1·I)
    ARALIK_PAYI: float = 1.1            # `aralik` alanı = 1,1 × sonraki I
    ILAN_ESIGI: float = 0.15            # maliyet değişiminin "önemli"si
    # --- KK-03 · karıştırma kanıtı ---------------------------------------
    ED_ESIGI: float = 0.62              # kanal meşgul payı
    DUSUS_ORANI: float = 0.5            # c < oran · c̄
    KAYIP_ESIGI: float = 0.6            # selam kaybı payı s
    GIRIS_SANIYE: int = 2               # girişim işareti ardışık saniye
    CIKIS_SANIYE: int = 3               # girişim kaynaklı çıkış
    ED_GIRIS_SANIYE: int = 1
    ED_CIKIS_SANIYE: int = 1
    TANIDIK_S: float = 16.0             # "tanıdık komşu" penceresi
    KAYIP_PENCERE_S: float = 4.0        # s'nin penceresi
    ORTALAMA_SANIYE: int = 30           # c̄: son işaretsiz saniyeler
    MAC_ARDISIK: int = 3                # ardışık vazgeçme
    KENDI_UST_SURE_S: float = 30.0      # Y-6 (18 Kasım): T_HATIRA ile aynı
    # --- KK-04 · rota -----------------------------------------------------
    GECIS_ORANI: float = 0.10           # isteğe bağlı geçiş
    ISTEK_YINELEME: int = 3             # tur isteği kaç kez
    ISTEK_YINELEME_ARA_S: float = 0.5
    ISTEK_ARA_S: float = 5.0            # dizinin yinelenmesi · yok saymanın üst süresi
    ISTEK_ANIMSA_S: float = 4.0         # iletilen isteğin kaydı (Y-11)
    ISTEK_TEKRAR_S: float = 1.0         # aynı tur için ikinci iletim yok
    ISTEK_ATLAMA: int = 64
    # --- KK-05 · bekletme ve geri iz --------------------------------------
    TUTMA_EN_COK_S: float = 2.0         # atlama başına
    YENIDEN_SOR_S: float = 0.5          # tamponu yeniden sorma aralığı
    IZ_TAZELIK_S: float = 3.0

    def __post_init__(self) -> None:
        if not (0.0 < self.E_DON < self.E_CIK):
            raise ValueError("iki eşik: 0 < E_DON < E_CIK olmalı (T-3)")
        if not (0.0 < self.I_MIN_S <= self.I_MAX_S):
            raise ValueError("0 < I_MIN ≤ I_MAX olmalı")
        if self.N < self.ORNEK_EN_AZ or self.N > 64:
            raise ValueError("ORNEK_EN_AZ ≤ N ≤ 64 olmalı")

    @classmethod
    def adlar(cls) -> tuple[str, ...]:
        return tuple(f.name for f in fields(cls))

    def degerler(self) -> tuple:
        return tuple(getattr(self, ad) for ad in self.adlar())


# ==========================================================================
# BAYRAKLAR — KK-00 "Mekanizmalar, bayraklar, sınıflar"
# ==========================================================================
@dataclass(frozen=True, slots=True)
class Bayraklar:
    """Açık = mekanizma çalışır. Kapalıyken davranış KK-00'ın tablosundaki
    "kapalıyken" sütunudur."""

    # genel
    veri_kotu_tetigi: bool = True       # KK-01/6–8, 11
    uyarlanir_aralik: bool = True       # KK-02/2
    istege_bagli_esik: bool = True      # KK-04/5
    bekletme: bool = True               # KK-05/1–5
    # karıştırmaya karşı
    karistirma_durumu: bool = True      # KK-03/1–9 · KK-01/9–10, 13 · KK-02/5 · KK-04/8
    alici_bildirimi: bool = True        # KK-02 alanı · KK-03/5
    hatirlanan_kalite: bool = True      # KK-01/10
    cogaltma: bool = False              # (ileride; T-14)

    def __post_init__(self) -> None:
        # Bağımlı bayraklar: `karistirma_durumu` kapalıyken KARIŞTIRILIYOR'a
        # hiç girilmez; bit ve hatıra anlamsız kalırdı. Anlamsız bir kolun
        # adıyla koşu yapılmasın diye reddedilir.
        if not self.karistirma_durumu and (self.alici_bildirimi
                                           or self.hatirlanan_kalite):
            raise ValueError("`alici_bildirimi` ve `hatirlanan_kalite` "
                             "`karistirma_durumu`na bağlıdır")
        if self.cogaltma:
            raise ValueError("seçici çoğaltma bu sürümde yok (T-14)")

    @classmethod
    def adlar(cls) -> tuple[str, ...]:
        return tuple(f.name for f in fields(cls))

    def degerler(self) -> tuple[bool, ...]:
        return tuple(getattr(self, ad) for ad in self.adlar())


TAM = Bayraklar()
# Karıştırmaya karşı mekanizmalar kapalı, genel bayraklar açık. Mekanizma
# kapısının "hepsi kapalı" kolu da budur (KK-00; `06` §0.4.5).
CEKIRDEK = Bayraklar(karistirma_durumu=False, alici_bildirimi=False,
                     hatirlanan_kalite=False)


# ==========================================================================
# İLETİLER — `13` §02.1; KK-02 alan tablosu · KK-04/11
# ==========================================================================
# Sabit 65 bit + komşu başına 16 bit: 9 bayt + 2 bayt × komşu.
SELAM = MesajBicimi(
    "D5_SELAM",
    alanlar=(("sira", 16), ("aralik", 16), ("tur", 16), ("maliyet", 16),
             ("karistiriliyorum", 1)),
    tekrarli=(("komsu", ADRES_BIT), ("oran", 8)))

TUR_ISTEGI = MesajBicimi(
    "D5_TUR_ISTEGI", alanlar=(("istenen", 16), ("kalan", 8)))
