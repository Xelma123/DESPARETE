"""
Çerçeve — süre ve hataya açık bit **TEK YERDE**.

🔒 NEDEN TEK YER
================
Eski simülatörde iki PER tanımı vardı (yalnız yük ↔ süre × bit hızı) ve kâhin
ile gerçek alım sistematik olarak ayrışıyordu (512 B @ 2 Mb/s'te %9,38).
`sure_s` ve `hataya_acik_bit` yalnız burada hesaplanır; `Kanal.per()` tek
gövdedir ve kâhin ile gerçek alım **aynı fonksiyonu** çağırır. Bir test
(`test_kanal.py`) `sim2/` altında `bit_hizi_bps` veya `onbelge_s` ile yapılan
her aritmetiği AST ile tarar ve buradan başkasını reddeder.

🔴 ÖNBELGE GÖVDE HATASINA KATILMAZ — bir fizik kararı
====================================================
802.11b'de PLCP önbelgesi ve başlığı **1 Mb/s DBPSK** ile gönderilir, gövde
veri hızında. Önbelge alıcı zincirinin **kilit aşamasına** aittir
(`mac/alici.py`): yakalanamazsa çerçeve hiç alınmaz (`alim_red_onbelge`),
gövde PER'iyle karıştırılmaz. Önbelgenin kendi bit sayısı 192 µs × 1 Mb/s =
192 bit, DBPSK ile; "kilitlenemedi" ile "kilitlendi ama gövde bozuldu" iki
ayrı başarısızlık kipidir.

⚠️ `sure_s` yine de önbelgeyi İÇERİR: kanalı o kadar süre meşgul eder, MAC ve
girişim hesabı onu görmek zorundadır.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from sim2.cekirdek.degismezler import dogrula
from sim2.yapilandirma.konfig import Konfig

__all__ = ["CERCEVE_TIPLERI", "KONTROL_KAPSULLEME", "Cerceve", "cerceve_kur",
           "kontrol_kapsulleme_bayt"]

CerceveTipi = Literal["veri", "onay", "beacon", "kontrol"]

# Kapalı küme: "diğer" diye bir çerçeve tipi yoktur. Sayılamayan bir çerçeve,
# NRL'nin paydasına ya da payına sessizce girer ve metriği bozar.
CERCEVE_TIPLERI: tuple[str, ...] = ("veri", "onay", "beacon", "kontrol")

# Veri düzlemi mi kontrol düzlemi mi — NRL'nin pay/payda ayrımı BURADAN gelir,
# çağrı yerinde elle karar verilmez.
_VERI_DUZLEMI: frozenset[str] = frozenset({"veri"})

# 🔒 KONTROL MESAJI KAPSÜLLEMESİ — TEK KAYNAK (K-112, sözleşme kararı 1).
# Yönlendirme mesajının kendi boyutu RFC alanlarından türer
# (`gozlem/kontrol.py::MesajBicimi`); onu havaya taşıyan yığının başlıkları
# YALNIZ burada yazılır. AODV (RFC 3561 §3: UDP 654), OLSR (RFC 3626 §3.1:
# UDP 698) ve OLSRv2 (RFC 7181; RFC 5498'in MANET portu) UDP/IP üzerinden
# koşar. DSR ailesi (RFC 4728 §6.1; JarmRout) gerçekte UDP değil IP seçenek
# başlığı kullanır; burada bütün protokollerin kontrol mesajı aynı yığınla
# faturalanır (DSR'de fark mesaj başına UDP'nin 8 B'ı).
#
# ⚠️ BEYAN EDİLEN ASİMETRİ: `veri` (`paket_bayt`), `onay` ve `beacon`
# boyutları bugün Konfig'te TOPLAM çerçeve olarak duruyor ve bu tabloyu
# KULLANMIYOR — değiştirmek ölçülmüş her sonucu değiştirirdi. Yani kontrol
# çerçevesi kapsüllemesiyle, veri çerçevesi Konfig boyutuyla faturalanır.
# Yönü: kontrol düzlemini veriye göre en çok bu tablo kadar PAHALI gösterir.
KONTROL_KAPSULLEME: tuple[tuple[str, int, str], ...] = (
    ("802.11 MAC başlığı (veri, 3 adres)", 24, "IEEE 802.11-2016 §9.3.2.1"),
    ("802.11 FCS", 4, "IEEE 802.11-2016 §9.2.4.8"),
    ("LLC/SNAP", 8, "RFC 1042"),
    ("IPv4 başlığı (seçeneksiz)", 20, "RFC 791 §3.1"),
    ("UDP başlığı", 8, "RFC 768"),
)


def kontrol_kapsulleme_bayt() -> int:
    """Kapsüllemenin toplamı — tablodan TÜRETİLİR, elle yazılmaz."""
    return sum(b for _, b, _ in KONTROL_KAPSULLEME)


@dataclass(frozen=True, slots=True)
class Cerceve:
    """Havadaki bir çerçeve. Dondurulmuş: kimse süresini sonradan değiştiremez."""

    tip: str
    bayt: int
    sure_s: float
    hataya_acik_bit: int
    onbelge_s: float
    onbelge_bit: int
    # 🔒 Eb/N0 = SINR · çarpan — `v2/15` A2 (K-173). İşlem kazancı kapalıyken
    # TAM 1,0 (bugünkü model, çarpma birebir). Açıkken B / bit hızı: gövde
    # 22/2 = 11, önbelge 22/1 = 22. Bit hızıyla aritmetik bu dosyada kalır.
    govde_ebn0_carpani: float = 1.0
    onbelge_ebn0_carpani: float = 1.0
    # 🔒 A4 (K-177) — gövdenin hızı ve modülasyonu. Hız uyarlaması kapalıyken
    # `Konfig.bit_hizi_bps` ve `Konfig.modulasyon` (bugünkü model).
    hiz_bps: float = 0.0
    govde_modulasyonu: str = "dqpsk"

    @property
    def veri_duzlemi_mi(self) -> bool:
        return self.tip in _VERI_DUZLEMI

    @property
    def govde_suresi_s(self) -> float:
        """Önbelge sonrası, gövdenin havada olduğu süre."""
        return self.sure_s - self.onbelge_s

    def onbelge_araligi(self, bas_s: float) -> tuple[float, float]:
        """`bas_s`te başlayan çerçevenin ÖNBELGE aralığı `(baş, bitiş)`.

        🔒 `govde_araligi` ile aynı sebeple burada: önbelgenin nerede başlayıp
        bittiği tek yerde tanımlı kalsın.
        """
        return (bas_s, bas_s + self.onbelge_s)

    def govde_araligi(self, bas_s: float) -> tuple[float, float]:
        """`bas_s`te başlayan çerçevenin GÖVDE aralığı `(baş, bitiş)`.

        🔒 Önbelge aritmetiği de bu dosyada kalsın diye burada. Çağıran
        `bas_s + cerceve.onbelge_s` yazsaydı önbelgenin nereye ait olduğu
        ikinci bir yerde tanımlanmış olurdu — kusur 1'in aynı sınıfı.
        """
        return (bas_s + self.onbelge_s, bas_s + self.sure_s)


# 🔒 A4 (K-177) — hız → gövde modülasyonu (G1 · G2).
HIZ_MODULASYONU: dict[float, str] = {1e6: "dbpsk", 2e6: "dqpsk",
                                     5.5e6: "cck", 11e6: "cck"}


def cerceve_kur(konfig: Konfig, tip: str, bayt: int | None = None,
                mesaj_bayt: int | None = None,
                hiz_bps: float | None = None) -> Cerceve:
    """🔒 Çerçeve süresinin ve hataya açık bit sayısının TEK tanımı.

    `bayt` verilmezse tipin `Konfig`teki boyutu kullanılır — çağrı yerinde
    elle boyut yazmak, ikinci bir doğru kaynağı açardı.
    """
    if tip not in CERCEVE_TIPLERI:
        raise ValueError(f"bilinmeyen çerçeve tipi: {tip!r} — "
                         f"seçenekler: {CERCEVE_TIPLERI}")
    if tip == "kontrol":
        # 🔒 Kontrol çerçevesinin boyutu MESAJDAN türer: çağıran toplam bayt
        # yazamaz, yalnız RFC biçiminden hesaplanmış mesaj boyutunu verir.
        dogrula(bayt is None, "kontrol çerçevesinde `bayt` verilemez — "
                              "boyut `mesaj_bayt` + kapsüllemeden türer")
        dogrula(isinstance(mesaj_bayt, int) and not isinstance(mesaj_bayt, bool)
                and mesaj_bayt > 0, "kontrol mesaj boyutu pozitif tamsayı")
        bayt = mesaj_bayt + kontrol_kapsulleme_bayt()
    else:
        dogrula(mesaj_bayt is None, "`mesaj_bayt` yalnız kontrol çerçevesinde")
    if bayt is None:
        bayt = {"veri": konfig.paket_bayt,
                "onay": konfig.onay_bayt,
                "beacon": konfig.beacon_bayt}[tip]
    dogrula(bayt > 0, "çerçeve boyutu pozitif olmalı")

    # ⬇⬇⬇ BU İKİ SATIR PROJEDE TEKTİR. Başka hiçbir yerde `bit_hizi_bps` ya da
    # `onbelge_s` ile aritmetik yapılmaz; bir test bunu AST ile denetler.
    # A4: hız verilmezse — onay ve beacon temel hızda (hız uyarlaması
    # açıkken), geri kalan `bit_hizi_bps`te (bugünkü model).
    if hiz_bps is None:
        hiz_bps = (konfig.temel_bit_hizi_bps
                   if konfig.hiz_uyarlamasi and tip in ("onay", "beacon")
                   else konfig.bit_hizi_bps)
    sure_s = konfig.onbelge_s + (bayt * 8) / hiz_bps
    hataya_acik_bit = bayt * 8
    # Önbelge TEMEL hızda gönderilir; bit sayısı oradan türer (192 µs × 1 Mb/s
    # = 192 bit). Elle yazılsaydı süreyle ikinci bir doğru kaynağı olurdu.
    onbelge_bit = round(konfig.onbelge_s * konfig.temel_bit_hizi_bps)
    # İşlem kazancı (A2): bit başına enerji, işaretin bandındaki gürültüye.
    govde_carpan = onbelge_carpan = 1.0
    if konfig.islem_kazanci:
        govde_carpan = konfig.bant_genisligi_hz / hiz_bps
        onbelge_carpan = konfig.bant_genisligi_hz / konfig.temel_bit_hizi_bps
    modulasyon = konfig.modulasyon
    if konfig.hiz_uyarlamasi:
        dogrula(hiz_bps in HIZ_MODULASYONU,
                f"802.11b hızı değil: {hiz_bps}")
        modulasyon = HIZ_MODULASYONU[hiz_bps]
    # ⬆⬆⬆
    dogrula(onbelge_bit > 0, "önbelge bit sayısı pozitif olmalı")

    return Cerceve(tip=tip, bayt=int(bayt), sure_s=sure_s,
                   hataya_acik_bit=int(hataya_acik_bit),
                   onbelge_s=konfig.onbelge_s, onbelge_bit=int(onbelge_bit),
                   govde_ebn0_carpani=govde_carpan,
                   onbelge_ebn0_carpani=onbelge_carpan,
                   hiz_bps=hiz_bps, govde_modulasyonu=modulasyon)
