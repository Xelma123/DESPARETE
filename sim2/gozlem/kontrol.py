"""
Kontrol düzlemi niyetleri — protokolün simülatöre YAPTIRABİLDİĞİ her şey.

Sözleşme: `v2/13-KONTROL-DUZLEMI.md`. Karar kaydı: K-111 §3, K-112.

🔒 PROTOKOL ÇAĞIRMAZ, NİYET DÖNDÜRÜR
===================================
`gozlem/pencere.py` protokolün ne GÖRECEĞİNİ kilitler; bu dosya ne
YAPABİLECEĞİNİ. Protokol simülatör nesnelerine hiç dokunmaz: gönderilecek
bir kontrol mesajını ya da bir uyandırmayı DONMUŞ bir değer olarak döndürür,
simülatör onu uygular. `Karar.beyan` ile aynı biçim — geri referans
yapısal olarak imkânsızdır (K1).

🔒 MESAJ BOYUTU RFC ALANLARINDAN TÜRER (karar 1)
===============================================
`MesajBicimi` bir mesajın alanlarını BİT GENİŞLİĞİYLE listeler (RFC'nin
paket biçimi tablosu). Boyut bu listeden hesaplanır; protokol bir toplam
bayt YAZAMAZ. Her değer kendi alanına SIĞMAK zorundadır — sığmazsa hata.
Böylece taşınan bilgi ödenen bitten fazla olamaz: beacon yükünün
"sayaçta ödenip kanalda ödenmemesi" (K-111 EK-2) burada yapısal olarak
kapalıdır. Kapsülleme (IP/UDP/LLC/MAC/FCS) ve PHY önbelgesi bu dosyada
DEĞİL, tek kaynak olarak `kanal/cerceve.py::cerceve_kur()`dadır.

🔒 İKİ AYRI ZAMANLAYICI (karar 5)
=================================
  · PERİYODİK — `zamanlayicilar()` ile kurulumda BİR KEZ ilan edilir,
    `zamanlayici_doldu()` kancasına gelir. Düğüm başına etiket başına tam bir
    bekleyen olay; tavan gerekmez, ilanla sınırlıdır.
  · DİNAMİK — `Uyandirma` niyetiyle istenir, `uyandi()` kancasına gelir.
    Sayısı protokol davranışına bağlıdır; düğüm başına bekleyen sayısı bir
    GÜVENLİK TAVANIYLA sınırlıdır ve aşımda koşu deterministik olarak
    DURUR (karar 2) — `kosum/kontrol.py`.

🔒 TİTREŞİMİ SİMÜLATÖR ÇEKER, PROTOKOL DEĞİL (Y3 · R4)
======================================================
`KontrolIstegi` ve `Uyandirma` isteğe bağlı bir `jitter_s` taşır; simülatör
`U(0, jitter_s)` gecikmesini `protokol_kesif` akışının DÜĞÜM ALT AKIŞINDAN
çeker. Protokol bir rastgelelik nesnesi görmez, yani geri referans yasağı
sürer. Titreşim kullanmayan protokolde o akıştan hiç çekim yapılmaz ve
satırlar birebir aynı kalır.

⚠️ KANCALAR İSTEĞE BAĞLIDIR AMA HEPSİ-YA-HİÇ
===========================================
Kontrol düzlemini kullanmayan bir protokol (bugünkü dört gerçekleme) bu
kancaları taşımaz ve davranışı BİREBİR aynı kalır. Kancalardan BİRİNİ
taşıyıp ötekini taşımayan protokol kurulumda reddedilir: aksi hâlde örneğin
mesaj gönderip `kontrol_alindi` yazmayı unutan bir protokol, gelen her
cevabı sessizce yutardı.
"""

from __future__ import annotations

import math
import struct
from dataclasses import dataclass
from typing import Literal

from sim2.cekirdek.degismezler import dogrula
from sim2.gozlem.yuk import yuku_dondur

__all__ = ["KONTROL_KANCALARI", "KontrolHatasi", "MesajBicimi",
           "KontrolIstegi", "Uyandirma", "niyetleri_dogrula",
           "BEYAN_TIPLERI", "Beyan"]

KONTROL_KANCALARI: tuple[str, ...] = (
    "zamanlayicilar",    # () -> dict[str, float]      periyodik ilan, BİR KEZ
    "zamanlayici_doldu",     # (dugum, etiket, saat_s) -> tuple[niyet, ...]
    "uyandi",            # (dugum, etiket, saat_s) -> tuple[niyet, ...]
    "kontrol_alindi",    # (dugum, gonderen, bicim, yuk, yayin, saat_s)
                         #   -> tuple[niyet, ...]
    "iletim_basarisiz",  # (dugum, hedef, tur, saat_s) -> tuple[niyet, ...]
)


class KontrolHatasi(ValueError):
    """Kontrol düzlemi sözleşmesi ihlal edildi. Sessizce geçilmez."""


def _tek_duyarlik_sigar_mi(v: float) -> bool:
    if not math.isfinite(v):
        return True
    try:
        return math.isfinite(struct.unpack("<f", struct.pack("<f", v))[0])
    except OverflowError:
        return False


@dataclass(frozen=True, slots=True)
class MesajBicimi:
    """Bir kontrol mesajının TEL BİÇİMİ — RFC paket tablosunun karşılığı.

    `alanlar`   : `(ad, bit)` — sabit genişlikli alanlar
    `tekrarli`  : `(ad, eleman_basina_bit)` — değeri sayı demeti olan alanlar
                  (RERR'in ulaşılamaz hedef listesi, OLSR HELLO'nun komşu
                  listesi gibi). Boyuta `eleman_sayisi × bit` olarak girer.
    """

    ad: str
    alanlar: tuple[tuple[str, int], ...]
    tekrarli: tuple[tuple[str, int], ...] = ()

    def __post_init__(self) -> None:
        dogrula(isinstance(self.ad, str) and bool(self.ad),
                "mesaj biçiminin adı boş olamaz")
        adlar = [a for a, _ in self.alanlar] + [a for a, _ in self.tekrarli]
        dogrula(bool(adlar), "alansız mesaj biçimi olamaz")
        dogrula(len(set(adlar)) == len(adlar), "mesaj alan adı tekrarlı")
        for ad, bit in self.alanlar + self.tekrarli:
            dogrula(isinstance(ad, str) and bool(ad), "alan adı boş olamaz")
            dogrula(isinstance(bit, int) and not isinstance(bit, bool)
                    and bit > 0, f"{ad!r}: bit genişliği pozitif tamsayı")

    @property
    def sabit_bit(self) -> int:
        return sum(b for _, b in self.alanlar)

    def bit(self, yuk: dict) -> int:
        return self.sabit_bit + sum(len(yuk[a]) * b for a, b in self.tekrarli)

    def bayt(self, yuk: dict) -> int:
        """🔒 Boyutun TEK hesabı: bitler sekize yukarı yuvarlanır."""
        return (self.bit(yuk) + 7) // 8


def _jitter_dogrula(jitter_s: float) -> None:
    """🔒 Titreşim negatif olmayan ve sonlu olmalı; sıfır = titreşim yok."""
    dogrula(isinstance(jitter_s, (int, float))
            and not isinstance(jitter_s, bool)
            and math.isfinite(jitter_s) and jitter_s >= 0.0,
            "titreşim negatif olmayan ve sonlu olmalı")


def _deger_sigar_mi(ad: str, deger, bit: int) -> None:
    if isinstance(deger, bool):
        return
    if isinstance(deger, int):
        if not 0 <= deger < (1 << bit):
            raise KontrolHatasi(
                f"{ad!r}: {deger.bit_length()} bitlik değer {bit} bitlik "
                f"alana sığmıyor (işaretsiz, [0, 2^{bit}))")
        return
    if isinstance(deger, float):
        if bit != 32:
            raise KontrolHatasi(
                f"{ad!r}: float yalnız 32 bitlik alanda taşınır, alan {bit} bit")
        if not _tek_duyarlik_sigar_mi(deger):
            raise KontrolHatasi(f"{ad!r}: {deger!r} tek duyarlığa sığmıyor")
        return
    raise KontrolHatasi(f"{ad!r}: taşınamaz tip {type(deger).__name__}")


def _yuku_dogrula(bicim: MesajBicimi, yuk: dict) -> None:
    """🔒 Alanlar biçimle aynı, her değer kendi alanına sığar. `kur()` ve
    doğrudan kurulum (`__post_init__`) bu TEK denetimden geçer (denetim
    DD-06, K-242: doğrudan kurucu yalnız boyutu denetliyordu; 1 baytlık
    bedelle sınırsız tamsayı ve değişebilir liste taşınabiliyordu)."""
    beklenen = {a for a, _ in bicim.alanlar} | {a for a, _ in bicim.tekrarli}
    if set(yuk) != beklenen:
        raise KontrolHatasi(
            f"{bicim.ad}: yük alanları biçimle aynı olmalı — eksik "
            f"{sorted(beklenen - set(yuk))} · fazla "
            f"{sorted(set(yuk) - beklenen)}")
    for ad, bit in bicim.alanlar:
        _deger_sigar_mi(ad, yuk[ad], bit)
    for ad, bit in bicim.tekrarli:
        if not isinstance(yuk[ad], tuple):
            raise KontrolHatasi(f"{ad!r}: tekrarlı alan bir demet olmalı")
        for x in yuk[ad]:
            _deger_sigar_mi(ad, x, bit)


@dataclass(frozen=True, slots=True)
class KontrolIstegi:
    """"Bu mesajı gönder." `hedef=None` → YAYIN, `hedef=n` → UNICAST.

    🔒 Doğrudan kurulmaz; `KontrolIstegi.kur(...)` alanları doğrular, boyutu
    biçimden türetir ve yükü dondurur.
    """

    hedef: int | None
    bicim: MesajBicimi
    yuk: tuple[tuple[str, object], ...]
    mesaj_bayt: int
    # 🔒 Y3 · R4 — kuyruğa girmeden önceki `U(0, jitter_s)` gecikmesi.
    jitter_s: float = 0.0

    @staticmethod
    def kur(hedef: int | None, bicim: MesajBicimi, yuk: dict,
            jitter_s: float = 0.0) -> "KontrolIstegi":
        if not isinstance(bicim, MesajBicimi):
            raise KontrolHatasi("biçim bir `MesajBicimi` olmalı")
        if not isinstance(yuk, dict):
            raise KontrolHatasi("yük bir sözlük olmalı")
        _yuku_dogrula(bicim, yuk)
        return KontrolIstegi(hedef=hedef, bicim=bicim, yuk=yuku_dondur(yuk),
                             mesaj_bayt=bicim.bayt(yuk), jitter_s=jitter_s)

    def __post_init__(self) -> None:
        dogrula(self.hedef is None or (isinstance(self.hedef, int)
                                       and not isinstance(self.hedef, bool)
                                       and self.hedef >= 0),
                "kontrol hedefi None (yayın) ya da negatif olmayan düğüm")
        dogrula(isinstance(self.bicim, MesajBicimi),
                "biçim bir `MesajBicimi` olmalı")
        dogrula(isinstance(self.yuk, tuple)
                and all(isinstance(p, tuple) and len(p) == 2 for p in self.yuk),
                "yük dondurulmuş olmalı")
        yuk = dict(self.yuk)
        dogrula(len(yuk) == len(self.yuk), "yük alan adı tekrarlı")
        _yuku_dogrula(self.bicim, yuk)
        dogrula(self.mesaj_bayt == self.bicim.bayt(yuk),
                "mesaj boyutu biçimden türetilmemiş — `KontrolIstegi.kur` kullan")
        _jitter_dogrula(self.jitter_s)

    @property
    def yayin_mi(self) -> bool:
        return self.hedef is None


@dataclass(frozen=True, slots=True)
class Uyandirma:
    """"Beni `gecikme_s` sonra `etiket` ile uyandır." — DİNAMİK zamanlayıcı.

    ⚠️ Alt sınır (bir MAC slotu) ve düğüm başına bekleyen tavanı `Konfig`e
    bağlıdır ve simülatör tarafından uygulanır; ihlal koşuyu durdurur.
    """

    gecikme_s: float
    etiket: str
    # 🔒 Y3 · R4 — gecikmenin ÜSTÜNE eklenen `U(0, jitter_s)`.
    jitter_s: float = 0.0

    def __post_init__(self) -> None:
        _jitter_dogrula(self.jitter_s)
        dogrula(isinstance(self.etiket, str) and bool(self.etiket),
                "uyandırma etiketi boş olamaz")
        dogrula(isinstance(self.gecikme_s, (int, float))
                and not isinstance(self.gecikme_s, bool)
                and math.isfinite(self.gecikme_s) and self.gecikme_s > 0.0,
                "uyandırma gecikmesi pozitif ve sonlu olmalı")


def niyetleri_dogrula(niyetler, beyan_izinli: bool = False) -> tuple:
    """Kanca dönüşü: `KontrolIstegi | Uyandirma` (+ kancalarda `Beyan`).

    🔴 `beyan_izinli` 16 EYLÜL 2026'DA EKLENDİ — ÖLÇÜLMÜŞ BİR ASİMETRİ
    YÜZÜNDEN (`04` K-134).
    ======================================================================
    `Karar.beyan` bir protokolün *"rotam koptu"* diyebildiği TEK kanaldı ve o
    kanal yalnız **veri gönderme kararında** açılıyordu (`kosum/dugum.py`ün
    `sonraki_atlama`sı — tüm depoda tek çağrı yeri). Ama protokol kopmayı
    orada ÖĞRENMEZ: MAC bir iletimden vazgeçtiğinde (`iletim_basarisiz`) ya da
    komşusundan HELLO gelmeyi kestiğinde öğrenir.

    🔴 Sonucu YAPISAL ve AİLEYE GÖRE FARKLIYDI: kuyruğu boş bir düğüm hiçbir
    şey bildiremezdi. AODV kopmayı zaten GÖNDERİRKEN öğrenir ve birazdan
    bildirebilirdi; OLSR onu HELLO zaman aşımıyla öğrenir ve o düğümün
    gönderecek paketi olmayabilir. Yani ön-kayıtlı
    `algilama_duyarliligi = kopma_algilanan / kopma_fiziksel` **proaktif
    aileyi sistematik olarak düşük** gösterirdi — `06` §8'in üçüncü
    geçerlilik koşulunun (*"gizli asimetri yok"*) ihlali ve denetimin B1/B2
    bulgularıyla aynı sınıf.

    🔒 `Beyan` yalnız KANCALARDA serbesttir, `Karar.niyetler`de DEĞİL:
    `Karar`ın zaten bir `beyan` alanı var ve iki yol açmak aynı şeyi iki
    yerden söylemek olurdu (`03` §B5).
    """
    if not isinstance(niyetler, tuple):
        raise KontrolHatasi(
            f"kontrol kancası bir demet döndürmeli, "
            f"{type(niyetler).__name__} döndü (boşsa `()`)")
    izinli = ((KontrolIstegi, Uyandirma, Beyan) if beyan_izinli
              else (KontrolIstegi, Uyandirma))
    for n in niyetler:
        if not isinstance(n, izinli):
            if isinstance(n, Beyan):
                raise KontrolHatasi(
                    "`Karar.niyetler` içinde `Beyan` olamaz — `Karar.beyan` "
                    "alanını kullan. Beyan yalnız KANCA dönüşlerinde niyet "
                    "demetine girebilir.")
            raise KontrolHatasi(
                f"bilinmeyen niyet tipi: {type(n).__name__}")
        if isinstance(n, Beyan) and n.tip == "politika":
            raise KontrolHatasi(
                "`Beyan('politika')` kancada verilemez — elde düşürülecek "
                "paket yok; yalnız `Karar.beyan`da, `sonraki=None` ile.")
    return niyetler

# ==========================================================================
# BEYAN — protokolün *"şu oldu"* dediği şey. 🔴 YALNIZ ÖLÇÜME GİDER.
#
# 🔒 NEDEN BU DOSYADA (16 Eylül 2026, `04` K-134)
# `Beyan` önce `gozlem/karar.py`deydi. 16 Eylül'de kancaların da beyan
# döndürebilmesi gerekti ve `karar.py` BU modülü içe aktardığı için tersi bir
# döngü olurdu. Tip bir katman aşağı taşındı; `karar.py` onu yeniden dışa
# veriyor, yani `from sim2.gozlem.karar import Beyan` YAZAN HER YER
# çalışmaya devam ediyor.
# ==========================================================================
BeyanTipi = Literal["kopma", "rota_kuruldu", "rota_gecersiz", "politika"]

# Kapalı küme. Protokol keyfi bir olay adı uyduramaz: uydurabilseydi sonuç
# şeması protokole göre değişir ve kollar karşılaştırılamaz olurdu.
# 🔒 `politika` — 25 Eylül 2026 (`v2/15` A1, K-171): *"bu paketi bilerek
# taşımıyorum"*. Bir rota olayı DEĞİLDİR; yalnız `Karar`da, `sonraki=None`
# ile gelir ve paketin düşme sebebini `politika` yapar. Kancada anlamı yok
# (elde paket yok) ve orada reddedilir.
BEYAN_TIPLERI: tuple[str, ...] = ("kopma", "rota_kuruldu", "rota_gecersiz",
                                  "politika")


@dataclass(frozen=True, slots=True)
class Beyan:
    """Protokolün *"şu oldu"* dediği şey. 🔴 YALNIZ ÖLÇÜME GİDER.

    Simülatörün davranışını değiştirmez; yalnız düşme SEBEBİNİ seçen iki
    istisna var (`politika` için yukarıdaki not). İlki `rota_gecersiz`dir ve
    o istisna 16 Eylül 2026'da GERÇEKTEN UYGULANDI (`04` K-134): aynı kararda
    `sonraki is None` ile birlikte verilirse paket `hedef_yok` yerine
    `rota_gecersiz` sebebiyle düşer. Öncesinde bu cümle belgede yazıyordu ama
    KODDA YOKTU — ölçüldü: 320 beyan, `rota_gecersiz` sebebiyle **0** düşüş.
    """

    tip: str
    komsu: int | None = None      # hangi bağ/komşu hakkında

    def __post_init__(self) -> None:
        dogrula(self.tip in BEYAN_TIPLERI,
                "bilinmeyen beyan tipi — küme kapalıdır")


dogrula(len(set(BEYAN_TIPLERI)) == len(BEYAN_TIPLERI), "beyan tipi tekrarlı")

