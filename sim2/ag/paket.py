"""
Paket — veri düzleminin taşınan birimi.

🔒 DONDURULMUŞ ve KİMLİĞİ DEĞİŞMEZ
==================================
Bir paketin kimliği doğduğu anda belirlenir ve hiçbir atlamada değişmez.
TTL azalması yeni bir nesne üretir; kimlik aynı kalır. Böylece "aynı paket"
sorusu her katmanda aynı cevabı verir — teslim defteri, gecikme ölçümü ve
korunum denklemi hepsi bu kimliğe bağlı.

🔴 ÜÇ ALAN ŞEMA TAAHHÜDÜ — sonradan eklenemezler
================================================
Sonuç şemasına sonradan alan eklemek, daha önce yazılmış satırları
karşılaştırılamaz yapar. Bu üçü metrikler yazılmadan ÖNCE burada:

  · `akis_kimligi` — IPDV (gecikme titreşimi) **akış içi** sıralama ister.
    Akış kimliği olmadan iki akışın paketleri karışır ve ölçülen titreşim
    trafiğin değil, akışların birbirine göre kaymasının titreşimi olur.
  · `dogum_s` — uçtan uca gecikmenin sıfır noktası. Kuyruğa giriş anı
    değil DOĞUM anı: kuyrukta beklemek gecikmenin parçasıdır.
  · `ttl_kalan` — TTL olmadan döngüye giren paket "uçuşta" olarak sonsuza
    dek asılı kalır ve korunum denklemi sessizce tutar (kaybı gizler).

⚠️ `boyut_bayt` paketin KENDİ boyutudur; çerçeve süresi ondan `kanal/cerceve`
tarafından türetilir. Burada bir süre hesabı YOKTUR — kusur 1'in kuralı.

`kaynak_sira` (K-157) — paketin, kaynağın KENDİ ürettiği paketler arasındaki
sırası. Başlıkta yazar (IPv4 kimlik alanı, DESPARETE Data Sequence); gözlem
penceresine açılan kimlik budur, küresel `kimlik` DEĞİL (`v2/05` §3.3).
`kopya` (D-23 · K-231) — 0 asıl paket; ≥ 1, protokolün `Karar.kopyalar` ile
istediği uçtan uca eş. Eşin kimliği AYNIDIR: hedefte ilk varan teslim
sayılır, sonraki eşler bastırılır (`kosum/teslim.py`). Gözlem penceresine
açılmaz.

⚠️ Varsayılan 0 yalnız trafik üreticisini kullanmayan kalibrasyon ve test
kurucuları içindir: orada her paket aynı sırayı taşır ve paket kimliğine
dayanan bir protokol mantığı bu kurucularla ölçülemez.
"""

from __future__ import annotations

from dataclasses import dataclass, replace

from sim2.cekirdek.degismezler import dogrula

__all__ = ["Paket", "PaketSayaci"]


@dataclass(frozen=True, slots=True)
class Paket:
    """Tek bir veri paketi. Kimliği koşu boyunca değişmez."""

    kimlik: int
    akis_kimligi: int
    kaynak: int
    hedef: int
    dogum_s: float
    boyut_bayt: int
    ttl_kalan: int
    kaynak_sira: int = 0
    kopya: int = 0

    def __post_init__(self) -> None:
        dogrula(self.kaynak != self.hedef,
                "paketin kaynağı ve hedefi aynı olamaz")
        dogrula(self.boyut_bayt > 0, "paket boyutu pozitif olmalı")
        dogrula(self.ttl_kalan >= 0, "TTL negatif olamaz")
        dogrula(self.kaynak_sira >= 0, "kaynak sırası negatif olamaz")
        dogrula(self.kopya >= 0, "kopya numarası negatif olamaz")

    # ------------------------------------------------------------------
    def ttl_azalt(self) -> "Paket":
        """TTL'i bir azaltılmış YENİ paket — kimlik aynı kalır.

        Yerinde değiştirmek yerine yeni nesne: paket dondurulmuş olduğu için
        bir katman ötekinin gördüğü TTL'i sessizce değiştiremez.
        """
        dogrula(self.ttl_kalan > 0, "TTL tükenmiş paketin TTL'i azaltılamaz")
        return replace(self, ttl_kalan=self.ttl_kalan - 1)

    @property
    def ttl_tukendi_mi(self) -> bool:
        return self.ttl_kalan <= 0

    def gecikme_s(self, teslim_ani_s: float) -> float:
        """Uçtan uca gecikme — DOĞUMDAN teslime.

        Kuyruğa giriş anından değil: kuyrukta beklemek gecikmenin parçasıdır
        ve onu dışarıda bırakmak yükü gizler.
        """
        dogrula(teslim_ani_s >= self.dogum_s,
                "teslim anı doğumdan önce olamaz")
        return teslim_ani_s - self.dogum_s


class PaketSayaci:
    """Koşu boyunca artan benzersiz paket kimliği.

    🔒 Tek örnek: iki sayaç olsaydı iki paket aynı kimliği taşıyabilir ve
    teslim defteri sessizce yanlış sayardı.
    """

    __slots__ = ("_sonraki",)

    def __init__(self) -> None:
        self._sonraki = 0

    def yeni(self) -> int:
        kimlik = self._sonraki
        self._sonraki += 1
        return kimlik

    @property
    def uretilen_toplam(self) -> int:
        return self._sonraki
